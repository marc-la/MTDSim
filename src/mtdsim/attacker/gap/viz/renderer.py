"""
Render a ``GeneralisedAttackProfile`` to a self-contained interactive HTML
file powered by Cytoscape.js.

The Python side only emits the payload JSON + inlines the static assets
(HTML shell, JS, CSS). All filtering, layout, legends, and panels live in
``assets/app.js`` so the viewer is trivially previewable/debuggable in a
browser without touching Python.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import networkx as nx

from mtdsim.attacker.gap.schema import GeneralisedAttackProfile
from mtdsim.attacker.gap.viz.payload import build_payload


_ASSET_DIR = Path(__file__).parent / "assets"


class MITRETechniqueDependencyVisualiser:
    """
    GAP visualiser that produces a Cytoscape.js-powered HTML file.

    The class name/API mirror the pre-0.4 pyvis-based visualiser so existing
    notebooks continue to work unchanged.
    """

    def __init__(self, gap: GeneralisedAttackProfile) -> None:
        self.gap = gap
        self._payload: Optional[dict] = None
        self._graph: Optional[nx.DiGraph] = None

    # -----------------------------------------------------------------
    # Public helpers

    def payload(self) -> dict:
        if self._payload is None:
            self._payload = build_payload(self.gap)
        return self._payload

    def to_networkx(self) -> nx.DiGraph:
        if self._graph is None:
            g = nx.DiGraph()
            for tid, n in self.gap.nodes.items():
                g.add_node(tid, **{
                    "name": n.technique_name,
                    "tactic": n.primary_tactic,
                    "layer": n.tactic_layer,
                })
            for e in self.gap.edges:
                g.add_edge(e.source_id, e.target_id,
                           confidence=e.confidence,
                           evidence_type=e.evidence_type,
                           consensus=e.source_count >= 2)
            self._graph = g
        return self._graph

    def summary(self) -> dict:
        """Backwards-compatible structural summary (same keys as pre-0.4)."""
        gap = self.gap
        payload = self.payload()
        evidence_breakdown: dict[str, int] = {}
        for e in gap.edges:
            for ev in e.evidence:
                evidence_breakdown[ev.source_type] = evidence_breakdown.get(ev.source_type, 0) + 1
        per_tactic = {}
        for tid, node in gap.nodes.items():
            per_tactic[node.primary_tactic] = per_tactic.get(node.primary_tactic, 0) + 1
        return {
            "version": gap.version,
            "total_techniques": gap.total_techniques,
            "techniques_with_edges": gap.techniques_with_edges,
            "orphan_techniques": gap.orphan_techniques,
            "edge_count": gap.edge_count,
            "consensus_edge_count": gap.consensus_edge_count,
            "backward_edge_count": gap.backward_edge_count,
            "intra_tactic_unresolved": gap.intra_tactic_unresolved,
            "entry_nodes": len(gap.entry_nodes),
            "objective_nodes": len(gap.objective_nodes),
            "per_tactic_counts": per_tactic,
            "evidence_breakdown": evidence_breakdown,
            "motivation_coverage": {
                "groups_total": len(gap.groups),
                "groups_with_motivation": sum(1 for g in gap.groups.values() if g.motivations),
            },
            "co_occurrence_params": {
                "min_support": gap.min_support,
                "min_confidence": gap.min_confidence,
                "median_threshold": gap.confidence_threshold,
            },
        }

    # -----------------------------------------------------------------
    # HTML rendering

    def render_interactive(
        self,
        output_path: str,
        evidence_types: Optional[set[str]] = None,
        min_confidence: float = 0.0,
        only_consensus: bool = False,
        hide_isolated: bool = True,
        initial_preset: str = "attack_flow",
    ) -> str:
        """
        Write a self-contained HTML file with the Cytoscape viewer.

        The legacy pyvis-era filter arguments are retained so existing calls
        keep working; they seed the initial filter state in the HTML.
        """
        html_template = (_ASSET_DIR / "index.html").read_text()
        css = (_ASSET_DIR / "style.css").read_text()
        app_js = (_ASSET_DIR / "app.js").read_text()

        initial_filter = {
            "evidence_types": sorted(evidence_types) if evidence_types else None,
            "min_confidence": min_confidence,
            "only_consensus": only_consensus,
            "hide_isolated": hide_isolated,
            "preset": initial_preset,
        }

        payload = self.payload()
        payload_json = json.dumps(payload, default=str)
        filter_json = json.dumps(initial_filter)

        # Offline-safe: load Cytoscape from jsDelivr CDN with SRI-compatible
        # tags. If the machine is offline the viewer still renders nodes via
        # the fallback DOM but graph layout won't run — documented.
        html = (
            html_template
            .replace("__CSS__", css)
            .replace("__APP_JS__", app_js)
            .replace("__PAYLOAD__", payload_json)
            .replace("__INITIAL_FILTER__", filter_json)
            .replace("__BUILD_DATE__", payload["meta"]["build_date"])
            .replace("__VERSION__", payload["meta"]["version"])
        )

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        return str(out)
