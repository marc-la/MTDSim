"""
Interactive visualisation for the Generalised Attack Profile.

``MITRETechniqueDependencyVisualiser`` produces a single self-contained HTML
file built on pyvis/vis.js with an injected Cyber Situational Awareness UI:
filter panel, detail panel, in-view legend, header counts, and an attack-path
generator. All nodes and edges are emitted to the browser; filtering happens
client-side so the analyst can compare views without reloading.

Design principles (Endsley 1995; Angelini et al. 2019; Noel & Jajodia 2005):
  - one coordinated view (preset toggles instead of separate files)
  - explicit encoding legend
  - overview + detail on demand
  - show what's excluded as greyed context
  - hypothesis support via interactive path queries
"""

from __future__ import annotations

import json as _json
from typing import Optional

import networkx as nx

from mtdsim.attacker.gap.schema import (
    TACTIC_ORDER,
    DependencyEdge,
    GeneralisedAttackProfile,
    TechniqueNode,
)


# 14-colour categorical palette for tactic layers (0-13).
_TACTIC_PALETTE = [
    "#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462",
    "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
    "#1f78b4", "#e31a1c",
]

_EVIDENCE_COLOUR = {
    "co_occurrence":    "#1f77b4",  # blue
    "attack_flow":      "#2ca02c",  # green
    "caldera_sequence": "#ff7f0e",  # orange
    "ontology":         "#9467bd",  # purple
    "documentation":    "#7f7f7f",  # grey
    "cti_report":       "#17becf",  # teal
}

_EVIDENCE_LABELS = {
    "attack_flow":      "Attack Flow (MITRE)",
    "co_occurrence":    "Co-occurrence (mined)",
    "ontology":         "Ontology (STIX descriptions)",
    "documentation":    "Documentation",
    "cti_report":       "CTI report",
    "caldera_sequence": "CALDERA sequence",
}

_TACTIC_LABELS = [t.replace("-", " ").title() for t in TACTIC_ORDER]

# Fallback colour for edges whose primary evidence type is unknown.
_EVIDENCE_FALLBACK = "#999999"

# Brand accent used for highlighted attack paths.
_PATH_HIGHLIGHT = "#ff006e"


class MITRETechniqueDependencyVisualiser:
    """
    Unified CSA-oriented visualiser for a ``GeneralisedAttackProfile``.

    Usage
    -----
    >>> viz = MITRETechniqueDependencyVisualiser(gap)
    >>> viz.render_interactive("gap.html")

    The resulting HTML provides in-browser controls — no need to render
    multiple files for different views.
    """

    _X_SPACING = 340
    _Y_SPACING = 78

    def __init__(self, gap: GeneralisedAttackProfile):
        self.gap = gap
        self._nx_graph: Optional[nx.DiGraph] = None

    # ------------------------------------------------------------------ #
    # NetworkX view
    # ------------------------------------------------------------------ #

    def to_networkx(self) -> nx.DiGraph:
        """Materialise a NetworkX DiGraph view, caching the result."""
        if self._nx_graph is not None:
            return self._nx_graph
        g = nx.DiGraph()
        for tid, node in self.gap.nodes.items():
            g.add_node(
                tid,
                label=node.technique_name,
                tactic_layer=node.tactic_layer,
                primary_tactic=node.primary_tactic,
                campaign_count=node.campaign_count,
                group_count=node.group_count,
            )
        for e in self.gap.edges:
            g.add_edge(
                e.source_id,
                e.target_id,
                evidence_type=e.evidence_type,
                confidence=e.confidence,
                support=e.support,
                source_count=e.source_count,
                is_backward=e.is_backward,
            )
        self._nx_graph = g
        return g

    # ------------------------------------------------------------------ #
    # Legacy Python-side filter (kept for API compatibility)
    # ------------------------------------------------------------------ #

    def _filtered_edges(
        self,
        evidence_types: Optional[set[str]] = None,
        min_confidence: float = 0.0,
        only_consensus: bool = False,
    ) -> list[DependencyEdge]:
        edges = self.gap.edges
        if evidence_types is not None:
            edges = [
                e for e in edges
                if any(ev.source_type in evidence_types for ev in e.evidence)
            ]
        if min_confidence > 0:
            edges = [e for e in edges if e.confidence >= min_confidence]
        if only_consensus:
            edges = [e for e in edges if e.source_count >= 2]
        return edges

    # ------------------------------------------------------------------ #
    # Unified payload (client-side filtering)
    # ------------------------------------------------------------------ #

    def _build_payload(self) -> dict:
        """Serialise the full GAP for in-browser filtering and detail lookup."""
        nodes = []
        for tid, n in self.gap.nodes.items():
            nodes.append({
                "id": tid,
                "name": n.technique_name,
                "tactic": n.primary_tactic,
                "tactic_layer": max(n.tactic_layer, 0),
                "tactics": list(n.tactics),
                "platforms": list(n.platforms),
                "campaign_count": n.campaign_count,
                "group_count": n.group_count,
                "campaigns": list(n.campaign_ids),
                "groups": list(n.group_ids),
                "software": list(n.software_ids),
                "sub_count": len(n.sub_technique_ids),
            })

        edges = []
        for e in self.gap.edges:
            sources = sorted({ev.source_type for ev in e.evidence}) or [e.evidence_type]
            edges.append({
                "source": e.source_id,
                "target": e.target_id,
                "primary": e.evidence_type,
                "confidence": round(e.confidence, 4),
                "support": round(e.support, 4) if e.support is not None else None,
                "lift": round(e.lift, 4) if e.lift is not None else None,
                "source_count": e.source_count,
                "is_backward": bool(e.is_backward),
                "sources": sources,
                "evidence": [
                    {
                        "type": ev.source_type,
                        "url": ev.source_url,
                        "desc": ev.description,
                    }
                    for ev in e.evidence
                ],
            })

        return {
            "version": self.gap.version,
            "build_date": self.gap.build_date,
            "nodes": nodes,
            "edges": edges,
            "tactic_order": list(TACTIC_ORDER),
            "tactic_labels": list(_TACTIC_LABELS),
            "tactic_palette": list(_TACTIC_PALETTE),
            "evidence_palette": dict(_EVIDENCE_COLOUR),
            "evidence_labels": dict(_EVIDENCE_LABELS),
            "entry_nodes": list(self.gap.entry_nodes),
            "objective_nodes": list(self.gap.objective_nodes),
            "totals": {
                "techniques": self.gap.total_techniques,
                "edges": self.gap.edge_count,
                "consensus": self.gap.consensus_edge_count,
                "entry": len(self.gap.entry_nodes),
                "objective": len(self.gap.objective_nodes),
            },
        }

    # ------------------------------------------------------------------ #
    # Layout helpers
    # ------------------------------------------------------------------ #

    def _layered_positions(self) -> tuple[dict[str, tuple[int, int]], dict[int, int]]:
        """
        Compute (x, y) pixel positions for every node.

        Nodes are grouped by ``tactic_layer``; within a column they are
        sorted by descending ``campaign_count`` (then by technique id) so the
        most-prevalent techniques sit at the top of each column.

        Returns (positions, per_layer_count).
        """
        by_layer: dict[int, list[TechniqueNode]] = {}
        for tid, n in self.gap.nodes.items():
            by_layer.setdefault(max(n.tactic_layer, 0), []).append(n)

        positions: dict[str, tuple[int, int]] = {}
        per_layer_count: dict[int, int] = {}
        for layer, items in by_layer.items():
            items.sort(
                key=lambda n: (-n.campaign_count, n.technique_id)
            )
            per_layer_count[layer] = len(items)
            for idx, n in enumerate(items):
                positions[n.technique_id] = (
                    layer * self._X_SPACING,
                    idx * self._Y_SPACING,
                )
        return positions, per_layer_count

    # ------------------------------------------------------------------ #
    # Interactive HTML (pyvis)
    # ------------------------------------------------------------------ #

    def render_interactive(
        self,
        output_path: str,
        evidence_types: Optional[set[str]] = None,
        min_confidence: float = 0.0,
        only_consensus: bool = False,
        hide_isolated: bool = True,
        notebook: bool = False,
        height: str = "100vh",
        width: str = "100%",
    ) -> str:
        """
        Write a unified interactive HTML visualisation to ``output_path``.

        The ``evidence_types``, ``min_confidence``, ``only_consensus`` and
        ``hide_isolated`` arguments set the *initial* filter state of the
        client-side UI; all nodes and edges are still emitted to the page.
        """
        from pyvis.network import Network

        positions, per_layer_count = self._layered_positions()

        # Determine which techniques have at least one edge under *no* filter.
        connected_tids: set[str] = set()
        for e in self.gap.edges:
            connected_tids.add(e.source_id)
            connected_tids.add(e.target_id)

        net = Network(
            height=height,
            width=width,
            directed=True,
            notebook=notebook,
            cdn_resources="in_line",
            bgcolor="#ffffff",
            font_color="#222222",
        )
        net.toggle_physics(False)

        # ---- Nodes ----
        for tid, node in self.gap.nodes.items():
            layer = max(node.tactic_layer, 0)
            x, y = positions[tid]
            colour = _TACTIC_PALETTE[layer % len(_TACTIC_PALETTE)]
            is_orphan = tid not in connected_tids
            size = 14 + min(node.campaign_count, 25)

            short_name = node.technique_name
            if len(short_name) > 16:
                short_name = short_name[:15] + "…"
            label = f"{tid}\n{short_name}"

            net.add_node(
                tid,
                label=label,
                color={"background": colour, "border": "#222222"},
                borderWidth=1,
                borderWidthSelected=3,
                shape="diamond" if is_orphan else "dot",
                size=size,
                x=x,
                y=y,
                physics=False,
                font={"multi": False, "size": 11, "color": "#111111",
                      "vadjust": -2, "face": "Segoe UI, Tahoma, sans-serif"},
            )

        # ---- Edges (non-consensus first, consensus last so they paint on top) ----
        node_ids = set(net.get_nodes())
        sorted_edges = sorted(
            self.gap.edges,
            key=lambda e: (e.source_count, e.confidence),
        )
        for e in sorted_edges:
            if e.source_id not in node_ids or e.target_id not in node_ids:
                continue
            colour = _EVIDENCE_COLOUR.get(e.evidence_type, _EVIDENCE_FALLBACK)
            base_width = 1 + 4 * e.confidence
            if e.source_count >= 2:
                base_width += 2

            # Edge dash pattern encodes evidence quality:
            #   backward loops → long dashes
            #   co-occurrence only (lower trust) → dotted
            #   otherwise solid
            if e.is_backward:
                dashes: list | bool = [12, 6]
            elif e.evidence_type == "co_occurrence" and e.source_count == 1:
                dashes = [2, 4]
            else:
                dashes = False

            # Route long-span edges with more curvature so adjacent-layer
            # edges stay straight and distant links don't overlap.
            span = abs(
                self.gap.nodes[e.target_id].tactic_layer
                - self.gap.nodes[e.source_id].tactic_layer
            )
            roundness = min(0.1 + 0.1 * max(span - 1, 0), 0.5)

            net.add_edge(
                e.source_id,
                e.target_id,
                id=f"{e.source_id}|{e.target_id}",
                color=colour,
                width=base_width,
                dashes=dashes,
                arrows="to",
                smooth={"type": "curvedCCW", "roundness": roundness},
            )

        net.set_options(
            """
            var options = {
              "interaction": {"hover": true, "tooltipDelay": 2000000,
                              "navigationButtons": true, "keyboard": true},
              "edges": {"smooth": {"type": "cubicBezier", "forceDirection": "horizontal"}},
              "physics": {"enabled": false}
            }
            """
        )
        net.write_html(output_path, notebook=notebook, open_browser=False)

        payload = self._build_payload()
        initial_filter = {
            "evidence_types": sorted(evidence_types) if evidence_types else None,
            "min_confidence": float(min_confidence),
            "only_consensus": bool(only_consensus),
            "hide_isolated": bool(hide_isolated),
        }
        self._post_process_html(
            output_path, per_layer_count, payload, initial_filter
        )
        return output_path

    # ------------------------------------------------------------------ #
    # HTML post-processing — CSA shell injection
    # ------------------------------------------------------------------ #

    def _post_process_html(
        self,
        html_path: str,
        per_layer_count: dict[int, int],
        payload: dict,
        initial_filter: dict,
    ) -> None:
        with open(html_path, "r") as f:
            html = f.read()

        # Expose the vis.js Network as a global for the UI module.
        html = html.replace("drawGraph();", "window._gapNetwork = drawGraph();", 1)

        # Tactic-layer metadata for the canvas overlay.
        layer_data = []
        for layer_idx in range(len(TACTIC_ORDER)):
            count = per_layer_count.get(layer_idx, 0)
            if count == 0:
                continue
            layer_data.append({
                "x": layer_idx * self._X_SPACING,
                "count": count,
                "label": _TACTIC_LABELS[layer_idx],
                "layer": layer_idx,
            })
        max_y = max(
            (c * self._Y_SPACING for c in per_layer_count.values()), default=0
        )

        custom_css = _CUSTOM_CSS
        header_html = _header_html(payload)
        css_block = f"<style>{custom_css}</style>"

        payload_json = _json.dumps(payload, separators=(",", ":"))
        initial_json = _json.dumps(initial_filter)
        layer_json = _json.dumps(layer_data)
        palette_json = _json.dumps(_TACTIC_PALETTE)

        ui_script = _UI_SCRIPT_TEMPLATE.format(
            payload_json=payload_json,
            initial_json=initial_json,
            layer_json=layer_json,
            palette_json=palette_json,
            x_spacing=self._X_SPACING,
            max_y=max_y,
            path_highlight=_PATH_HIGHLIGHT,
        )

        # Inject CSS right before </head> (fall back to </style> if no head).
        if "</head>" in html:
            html = html.replace("</head>", css_block + "\n</head>", 1)
        else:
            html = html.replace("</style>", custom_css + "\n</style>", 1)

        # Inject the header/shell HTML right after <body>.
        html = html.replace("<body>", "<body>\n" + header_html, 1)

        # Inject the UI script right before </body>.
        html = html.replace("</body>", ui_script + "\n</body>", 1)

        with open(html_path, "w") as f:
            f.write(html)

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #

    def summary(self) -> dict:
        g = self.gap
        per_layer = {}
        for layer_idx, tids in sorted(g.layers.items()):
            tactic = TACTIC_ORDER[layer_idx] if 0 <= layer_idx < len(TACTIC_ORDER) else "unknown"
            per_layer[tactic] = len(tids)

        evidence_breakdown: dict[str, int] = {}
        for e in g.edges:
            for ev in e.evidence:
                evidence_breakdown[ev.source_type] = evidence_breakdown.get(ev.source_type, 0) + 1

        return {
            "version": g.version,
            "total_techniques": g.total_techniques,
            "techniques_with_edges": g.techniques_with_edges,
            "orphan_techniques": g.orphan_techniques,
            "edge_count": g.edge_count,
            "consensus_edge_count": g.consensus_edge_count,
            "backward_edge_count": g.backward_edge_count,
            "intra_tactic_unresolved": g.intra_tactic_unresolved,
            "entry_nodes": len(g.entry_nodes),
            "objective_nodes": len(g.objective_nodes),
            "per_tactic_counts": per_layer,
            "evidence_breakdown": evidence_breakdown,
            "co_occurrence_params": {
                "min_support": g.min_support,
                "min_confidence": g.min_confidence,
                "median_threshold": g.confidence_threshold,
            },
        }


# ---------------------------------------------------------------------- #
# CSS (injected)
# ---------------------------------------------------------------------- #

_CUSTOM_CSS = """
/* === GAP CSA shell === */
html, body {
    margin: 0; padding: 0; height: 100%; overflow: hidden;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 13px; color: #222;
    background: #f5f5f7;
}
#loadingBar { display: none !important; }
div.vis-tooltip { display: none !important; }

.card {
    position: fixed !important;
    top: 56px; left: 272px; right: 332px; bottom: 108px;
    margin: 0 !important; border: none !important;
    background: #ffffff !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    border-radius: 6px;
    overflow: hidden;
}
#mynetwork {
    height: 100% !important; width: 100% !important;
    border: none !important;
}

/* Header ---------------------------------------------------------------- */
#gap-header {
    position: fixed; top: 0; left: 0; right: 0; height: 48px;
    background: #1a1a2e; color: #e0e0e0;
    display: flex; align-items: center; padding: 0 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    z-index: 100;
}
#gap-header .title { font-size: 15px; font-weight: 600; color: #fff; }
#gap-header .title small { color: #9bb; font-weight: 400; margin-left: 8px; }
#gap-header .counts {
    margin-left: auto; font-size: 12px; color: #cde;
    display: flex; gap: 18px;
}
#gap-header .counts b { color: #fff; }

/* Filter panel ---------------------------------------------------------- */
#gap-filters {
    position: fixed; top: 56px; left: 0; width: 260px; bottom: 108px;
    background: #ffffff; border-right: 1px solid #e0e0e4;
    overflow-y: auto; padding: 14px 14px 20px 14px;
    box-sizing: border-box; z-index: 50;
}
#gap-filters h3 {
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;
    color: #666; margin: 14px 0 6px 0;
}
#gap-filters h3:first-child { margin-top: 0; }
#gap-filters label {
    display: flex; align-items: center; gap: 6px;
    padding: 2px 0; cursor: pointer; font-size: 12px;
}
#gap-filters label:hover { color: #1a1a2e; }
#gap-filters input[type="checkbox"],
#gap-filters input[type="radio"] { cursor: pointer; }
#gap-filters input[type="text"],
#gap-filters select {
    width: 100%; padding: 5px 8px; box-sizing: border-box;
    border: 1px solid #d0d0d4; border-radius: 4px; font-size: 12px;
    font-family: inherit;
}
#gap-filters input[type="range"] { width: 100%; }
#gap-filters .slider-row {
    display: flex; align-items: center; gap: 6px; font-size: 11px;
    color: #666;
}
#gap-filters .sw {
    display: inline-block; width: 10px; height: 10px; border-radius: 2px;
    border: 1px solid #888; margin-right: 2px;
}
#gap-filters button {
    width: 100%; padding: 6px 8px; margin-top: 6px;
    background: #1a1a2e; color: #fff; border: none; border-radius: 4px;
    cursor: pointer; font-size: 12px; font-weight: 500;
}
#gap-filters button:hover { background: #2a2a4e; }
#gap-filters button.secondary {
    background: #e5e5ea; color: #333;
}
#gap-filters button.secondary:hover { background: #d0d0d6; }
#gap-filters .hint {
    font-size: 10px; color: #888; margin-top: 4px; line-height: 1.4;
}
#gap-filters details.gap-help {
    margin-top: 6px; font-size: 11px;
    background: #f7f7fa; border: 1px solid #e0e0e4; border-radius: 4px;
    padding: 4px 8px;
}
#gap-filters details.gap-help summary {
    cursor: pointer; color: #1a1a2e; font-weight: 500;
    list-style: none; outline: none;
}
#gap-filters details.gap-help summary::before {
    content: 'ⓘ '; color: #666;
}
#gap-filters details.gap-help[open] summary { color: #0066cc; }
#gap-filters details.gap-help .hint {
    color: #444; font-size: 11px; margin-top: 6px; line-height: 1.5;
}
#gap-filters #p-info {
    background: #f0f4f8; border-left: 3px solid #0066cc;
    padding: 4px 8px; border-radius: 0 4px 4px 0; color: #234;
}
#gap-filters select option:disabled {
    color: #bbb; font-style: italic;
}

/* Detail panel ---------------------------------------------------------- */
#gap-detail {
    position: fixed; top: 56px; right: 0; width: 320px; bottom: 108px;
    background: #ffffff; border-left: 1px solid #e0e0e4;
    overflow-y: auto; padding: 14px 16px 20px 16px;
    box-sizing: border-box; z-index: 50;
}
#gap-detail .empty {
    color: #999; font-style: italic; font-size: 12px;
    text-align: center; padding: 40px 10px;
}
#gap-detail h2 {
    font-size: 14px; margin: 0 0 4px 0; color: #1a1a2e;
}
#gap-detail h4 {
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;
    color: #666; margin: 12px 0 4px 0;
}
#gap-detail .kv {
    display: flex; justify-content: space-between;
    font-size: 12px; padding: 2px 0; border-bottom: 1px dotted #eee;
}
#gap-detail .kv span:first-child { color: #666; }
#gap-detail .kv span:last-child { color: #111; font-weight: 500; }
#gap-detail .chip {
    display: inline-block; padding: 1px 6px; margin: 1px 2px 1px 0;
    background: #eef; border-radius: 10px; font-size: 10px; color: #336;
}
#gap-detail ul { margin: 4px 0 8px 16px; padding: 0; font-size: 12px; }
#gap-detail li { margin: 1px 0; }
#gap-detail a { color: #0066cc; text-decoration: none; word-break: break-all; }
#gap-detail a:hover { text-decoration: underline; }
#gap-detail .ev-block {
    background: #f7f7fa; border-left: 3px solid #bbb;
    padding: 6px 8px; margin: 4px 0; font-size: 11px;
    border-radius: 0 4px 4px 0;
}
#gap-detail .ev-block .t {
    font-weight: 600; text-transform: uppercase; font-size: 10px;
    letter-spacing: 0.4px;
}
#gap-detail .path-item {
    background: #f7f7fa; border-left: 3px solid #ff006e;
    padding: 6px 8px; margin: 4px 0; font-size: 11px;
    border-radius: 0 4px 4px 0; cursor: pointer;
}
#gap-detail .path-item:hover { background: #fff0f6; }
#gap-detail .path-item .pstep { color: #333; font-family: monospace; font-size: 11px; }
#gap-detail .path-item .pmeta { color: #888; font-size: 10px; margin-top: 2px; }

/* Legend ---------------------------------------------------------------- */
#gap-legend {
    position: fixed; bottom: 0; left: 0; right: 0; height: 96px;
    background: #ffffff; border-top: 1px solid #e0e0e4;
    display: flex; align-items: center; gap: 24px;
    padding: 8px 18px; box-sizing: border-box;
    overflow-x: auto; font-size: 11px; z-index: 50;
}
#gap-legend .lg-section { display: flex; flex-direction: column; gap: 3px; min-width: fit-content; }
#gap-legend .lg-section h4 {
    font-size: 10px; text-transform: uppercase; letter-spacing: 0.4px;
    color: #666; margin: 0 0 3px 0;
}
#gap-legend .lg-row { display: flex; align-items: center; gap: 6px; font-size: 10px; }
#gap-legend .swatch {
    display: inline-block; width: 12px; height: 12px; border-radius: 2px;
    border: 1px solid #888;
}
#gap-legend .dot { width: 12px; height: 12px; border-radius: 50%; border: 1px solid #222; }
#gap-legend .diamond {
    width: 10px; height: 10px; transform: rotate(45deg); border: 1px solid #222;
    background: #ddd;
}
#gap-legend .line {
    display: inline-block; width: 30px; height: 0; border-top: 2px solid #444;
}
#gap-legend .line.thick { border-top-width: 5px; }
#gap-legend .line.dashed { border-top-style: dashed; }
#gap-legend .line.dotted { border-top-style: dotted; }
#gap-legend .size-dot {
    display: inline-block; background: #80b1d3; border: 1px solid #222;
    border-radius: 50%;
}

/* Tooltip (kept from v1) ------------------------------------------------ */
#gap-tooltip {
    position: absolute; display: none;
    background: #1a1a2e; color: #e0e0e0;
    border: 1px solid #555; border-radius: 8px;
    padding: 10px 14px; font-size: 12px; line-height: 1.5;
    max-width: 360px; box-shadow: 0 4px 24px rgba(0,0,0,0.35);
    z-index: 9999; pointer-events: none;
}
#gap-tooltip b { color: #ffffff; }
"""


# ---------------------------------------------------------------------- #
# Header / shell HTML
# ---------------------------------------------------------------------- #

def _header_html(payload: dict) -> str:
    t = payload["totals"]
    return f"""
<div id="gap-header">
    <div class="title">GAP v{payload['version']}
        <small>build {payload['build_date']} · {t['techniques']} techniques · {t['edges']} edges</small>
    </div>
    <div class="counts">
        <span>Techniques <b id="c-tech">{t['techniques']}</b></span>
        <span>Edges <b id="c-edge">{t['edges']}</b></span>
        <span>Consensus <b id="c-cons">{t['consensus']}</b></span>
        <span>Entry <b id="c-entry">{t['entry']}</b></span>
        <span>Objective <b id="c-obj">{t['objective']}</b></span>
    </div>
</div>
<div id="gap-filters"></div>
<div id="gap-detail"><div class="empty">Click a node or edge to see details.</div></div>
<div id="gap-legend"></div>
<div id="gap-tooltip"></div>
"""


# ---------------------------------------------------------------------- #
# UI JavaScript module
# ---------------------------------------------------------------------- #

_UI_SCRIPT_TEMPLATE = r"""
<script type="text/javascript">
window._gapPayload = {payload_json};
window._gapInitial = {initial_json};

(function() {{
  var PAYLOAD = window._gapPayload;
  var TACTIC_PALETTE = {palette_json};
  var LAYER_DATA = {layer_json};
  var X_SPACING = {x_spacing};
  var MAX_Y = {max_y};
  var PATH_HIGHLIGHT = "{path_highlight}";
  var EV_PALETTE = PAYLOAD.evidence_palette;
  var EV_LABELS = PAYLOAD.evidence_labels;
  var TACTIC_LABELS = PAYLOAD.tactic_labels;

  var network = window._gapNetwork;
  if (!network) {{ console.error("vis.js network not found"); return; }}

  /* ---- Indexes ---- */
  var nodeById = {{}};
  PAYLOAD.nodes.forEach(function(n) {{ nodeById[n.id] = n; }});

  var edgeById = {{}};
  var adjOut = {{}};   /* adjacency for path finding (filtered rebuilt per query) */
  var allEvidenceTypes = new Set();
  PAYLOAD.edges.forEach(function(e) {{
    var id = e.source + "|" + e.target;
    e._id = id;
    edgeById[id] = e;
    e.sources.forEach(function(s) {{ allEvidenceTypes.add(s); }});
  }});
  allEvidenceTypes = Array.from(allEvidenceTypes).sort();

  /* ---- Filter state ---- */
  var initial = window._gapInitial || {{}};
  var _filterState = {{
    preset: 'full',
    sources: {{}},
    minConfidence: initial.min_confidence || 0.0,
    onlyConsensus: !!initial.only_consensus,
    tactics: {{}},
    hideOrphans: initial.hide_isolated === undefined ? true : !!initial.hide_isolated,
    showExcluded: false,
    search: '',
    highlight: null,  /* set of edge ids to highlight (path results) */
  }};
  allEvidenceTypes.forEach(function(s) {{ _filterState.sources[s] = true; }});
  if (initial.evidence_types) {{
    allEvidenceTypes.forEach(function(s) {{ _filterState.sources[s] = false; }});
    initial.evidence_types.forEach(function(s) {{ _filterState.sources[s] = true; }});
  }}
  for (var i = 0; i < TACTIC_LABELS.length; i++) _filterState.tactics[i] = true;

  /* ---- Build filter panel UI ---- */
  var filters = document.getElementById('gap-filters');

  function sectionTitle(text) {{
    var h = document.createElement('h3');
    h.textContent = text;
    filters.appendChild(h);
  }}

  /* Preset radios */
  sectionTitle('View preset');
  var presetWrap = document.createElement('div');
  ['full','curated','consensus','custom'].forEach(function(p) {{
    var lbl = document.createElement('label');
    lbl.innerHTML = '<input type="radio" name="preset" value="'+p+'">'+p.charAt(0).toUpperCase()+p.slice(1);
    presetWrap.appendChild(lbl);
  }});
  filters.appendChild(presetWrap);
  var presetHint = document.createElement('div');
  presetHint.className = 'hint';
  presetHint.textContent = 'Full = all sources. Curated = manually-sourced only. Consensus = edges backed by ≥2 source types.';
  filters.appendChild(presetHint);

  /* Evidence sources */
  sectionTitle('Evidence sources');
  var srcWrap = document.createElement('div');
  allEvidenceTypes.forEach(function(s) {{
    var col = EV_PALETTE[s] || '#999';
    var lbl = document.createElement('label');
    lbl.innerHTML =
      '<input type="checkbox" data-src="'+s+'" '+(_filterState.sources[s]?'checked':'')+'>'+
      '<span class="sw" style="background:'+col+'"></span>'+
      (EV_LABELS[s] || s);
    srcWrap.appendChild(lbl);
  }});
  filters.appendChild(srcWrap);

  /* Min confidence slider */
  sectionTitle('Min confidence');
  var sliderRow = document.createElement('div');
  sliderRow.className = 'slider-row';
  sliderRow.innerHTML =
    '<input type="range" id="f-conf" min="0" max="1" step="0.05" value="'+_filterState.minConfidence+'">'+
    '<span id="f-conf-v">'+_filterState.minConfidence.toFixed(2)+'</span>';
  filters.appendChild(sliderRow);

  /* Consensus only */
  var consLabel = document.createElement('label');
  consLabel.innerHTML = '<input type="checkbox" id="f-cons" '+(_filterState.onlyConsensus?'checked':'')+'>Consensus only (≥2 sources)';
  filters.appendChild(consLabel);

  /* Confidence derivation help */
  var confHelp = document.createElement('details');
  confHelp.className = 'gap-help';
  confHelp.innerHTML =
    '<summary>How is confidence derived?</summary>'+
    '<div class="hint">'+
    '<b>Attack Flow</b> = 1.0 (manually curated MITRE Attack Flow .afb files).<br>'+
    '<b>Co-occurrence</b> = P(target|source) from FP-Growth association rule mining over the binary group + software usage matrix from STIX. Values vary; the build threshold is the median rule confidence.<br>'+
    '<b>Ontology</b> = 0.8 (heuristic precondition keyword extraction from STIX technique descriptions; lower trust).<br>'+
    '<b>Multi-source</b> = max(confidence) across all contributing evidence types. <i>source_count ≥ 2</i> means consensus.'+
    '</div>';
  filters.appendChild(confHelp);

  /* Tactic layers */
  sectionTitle('Tactic layers');
  var tacWrap = document.createElement('div');
  TACTIC_LABELS.forEach(function(lbl, idx) {{
    var col = TACTIC_PALETTE[idx % TACTIC_PALETTE.length];
    var el = document.createElement('label');
    el.innerHTML =
      '<input type="checkbox" data-tac="'+idx+'" checked>'+
      '<span class="sw" style="background:'+col+'"></span>'+
      lbl;
    tacWrap.appendChild(el);
  }});
  filters.appendChild(tacWrap);

  /* Display options */
  sectionTitle('Display');
  var dispWrap = document.createElement('div');
  dispWrap.innerHTML =
    '<label><input type="checkbox" id="f-orphan" '+(_filterState.hideOrphans?'checked':'')+'>Hide orphan techniques</label>'+
    '<label><input type="checkbox" id="f-excl">Show excluded (greyed)</label>';
  filters.appendChild(dispWrap);

  /* Search */
  sectionTitle('Search');
  var searchInput = document.createElement('input');
  searchInput.type = 'text';
  searchInput.placeholder = 'Technique ID or name…';
  searchInput.id = 'f-search';
  filters.appendChild(searchInput);

  /* Path explorer */
  sectionTitle('Attack path explorer');
  var pathWrap = document.createElement('div');
  var srcOpts = PAYLOAD.entry_nodes.map(function(id) {{
    var n = nodeById[id];
    return '<option value="'+id+'">'+id+(n?' — '+n.name.substring(0,24):'')+'</option>';
  }}).join('');
  var tgtOpts = PAYLOAD.objective_nodes.map(function(id) {{
    var n = nodeById[id];
    return '<option value="'+id+'">'+id+(n?' — '+n.name.substring(0,24):'')+'</option>';
  }}).join('');
  pathWrap.innerHTML =
    '<label style="display:block;margin-top:4px">Source (entry)</label>'+
    '<select id="p-src">'+srcOpts+'</select>'+
    '<label style="display:block;margin-top:6px">Target (objective)</label>'+
    '<select id="p-tgt">'+tgtOpts+'</select>'+
    '<label style="display:block;margin-top:6px">Algorithm</label>'+
    '<select id="p-algo">'+
      '<option value="yen">k-shortest (by 1/confidence)</option>'+
      '<option value="all">All simple paths (bounded)</option>'+
    '</select>'+
    '<div class="slider-row" style="margin-top:6px"><span>k / max len</span>'+
      '<input type="range" id="p-k" min="1" max="8" step="1" value="1">'+
      '<span id="p-k-v">1</span></div>'+
    '<div id="p-info" class="hint" style="margin-top:4px">Select a source.</div>';
  filters.appendChild(pathWrap);
  var pathBtn = document.createElement('button');
  pathBtn.textContent = 'Find paths';
  filters.appendChild(pathBtn);
  var pathClr = document.createElement('button');
  pathClr.className = 'secondary';
  pathClr.textContent = 'Clear highlight';
  filters.appendChild(pathClr);

  /* ---- Wire events ---- */
  presetWrap.addEventListener('change', function(e) {{
    var p = e.target.value;
    _filterState.preset = p;
    if (p === 'full') {{
      allEvidenceTypes.forEach(function(s) {{ _filterState.sources[s] = true; }});
      _filterState.minConfidence = 0;
      _filterState.onlyConsensus = false;
    }} else if (p === 'curated') {{
      allEvidenceTypes.forEach(function(s) {{ _filterState.sources[s] = false; }});
      ['attack_flow','ontology','documentation','cti_report'].forEach(function(s) {{
        if (s in _filterState.sources) _filterState.sources[s] = true;
      }});
      _filterState.minConfidence = 0;
      _filterState.onlyConsensus = false;
    }} else if (p === 'consensus') {{
      allEvidenceTypes.forEach(function(s) {{ _filterState.sources[s] = true; }});
      _filterState.minConfidence = 0;
      _filterState.onlyConsensus = true;
    }}
    syncControlsFromState();
    applyFilters();
  }});
  // default preset = full
  presetWrap.querySelector('input[value="full"]').checked = true;

  srcWrap.addEventListener('change', function(e) {{
    if (e.target.dataset.src) {{
      _filterState.sources[e.target.dataset.src] = e.target.checked;
      markCustom();
      applyFilters();
    }}
  }});

  document.getElementById('f-conf').addEventListener('input', function(e) {{
    _filterState.minConfidence = parseFloat(e.target.value);
    document.getElementById('f-conf-v').textContent = _filterState.minConfidence.toFixed(2);
    markCustom();
    applyFilters();
  }});
  document.getElementById('f-cons').addEventListener('change', function(e) {{
    _filterState.onlyConsensus = e.target.checked;
    markCustom();
    applyFilters();
  }});
  tacWrap.addEventListener('change', function(e) {{
    if (e.target.dataset.tac) {{
      _filterState.tactics[parseInt(e.target.dataset.tac, 10)] = e.target.checked;
      applyFilters();
    }}
  }});
  document.getElementById('f-orphan').addEventListener('change', function(e) {{
    _filterState.hideOrphans = e.target.checked; applyFilters();
  }});
  document.getElementById('f-excl').addEventListener('change', function(e) {{
    _filterState.showExcluded = e.target.checked; applyFilters();
  }});
  searchInput.addEventListener('input', function(e) {{
    _filterState.search = e.target.value.trim().toLowerCase();
    applyFilters();
  }});
  document.getElementById('p-k').addEventListener('input', function(e) {{
    document.getElementById('p-k-v').textContent = e.target.value;
  }});
  document.getElementById('p-src').addEventListener('change', refreshPathControls);
  document.getElementById('p-tgt').addEventListener('change', refreshPathControls);
  document.getElementById('p-algo').addEventListener('change', refreshPathControls);
  pathBtn.addEventListener('click', runPathQuery);
  pathClr.addEventListener('click', function() {{
    _filterState.highlight = null;
    applyFilters();
  }});

  function markCustom() {{
    _filterState.preset = 'custom';
    var custom = presetWrap.querySelector('input[value="custom"]');
    if (custom) custom.checked = true;
  }}

  function syncControlsFromState() {{
    allEvidenceTypes.forEach(function(s) {{
      var cb = srcWrap.querySelector('input[data-src="'+s+'"]');
      if (cb) cb.checked = !!_filterState.sources[s];
    }});
    var cSlider = document.getElementById('f-conf');
    cSlider.value = _filterState.minConfidence;
    document.getElementById('f-conf-v').textContent = _filterState.minConfidence.toFixed(2);
    document.getElementById('f-cons').checked = _filterState.onlyConsensus;
  }}

  /* ---- Filter evaluation ---- */
  function edgePassesFilters(e) {{
    if (_filterState.onlyConsensus && e.source_count < 2) return false;
    if (e.confidence < _filterState.minConfidence) return false;
    var any = false;
    for (var i = 0; i < e.sources.length; i++) {{
      if (_filterState.sources[e.sources[i]]) {{ any = true; break; }}
    }}
    return any;
  }}
  function nodePassesTactic(n) {{
    return !!_filterState.tactics[n.tactic_layer];
  }}
  function nodeMatchesSearch(n) {{
    if (!_filterState.search) return true;
    var q = _filterState.search;
    return (n.id.toLowerCase().indexOf(q) !== -1) ||
           (n.name.toLowerCase().indexOf(q) !== -1);
  }}

  /* ---- Apply filters to vis.js ---- */
  function applyFilters() {{
    var visibleEdges = PAYLOAD.edges.filter(edgePassesFilters);
    var touching = new Set();
    visibleEdges.forEach(function(e) {{
      touching.add(e.source); touching.add(e.target);
    }});

    var nodeState = {{}};
    PAYLOAD.nodes.forEach(function(n) {{
      var tOK = nodePassesTactic(n);
      var sOK = nodeMatchesSearch(n);
      var connected = touching.has(n.id);
      var fullyVisible = tOK && sOK && (!_filterState.hideOrphans || connected);
      nodeState[n.id] = {{ visible: fullyVisible, connected: connected }};
    }});

    var edgeUpdates = PAYLOAD.edges.map(function(e) {{
      var ok = edgePassesFilters(e) &&
               nodeState[e.source] && nodeState[e.source].visible &&
               nodeState[e.target] && nodeState[e.target].visible;
      var hi = _filterState.highlight && _filterState.highlight.has(e._id);
      var dim = _filterState.highlight && !hi;
      var update = {{ id: e._id, hidden: !ok }};
      if (ok && hi) {{
        update.color = {{ color: PATH_HIGHLIGHT, highlight: PATH_HIGHLIGHT, inherit: false }};
        update.width = 7;
      }} else if (ok && dim) {{
        update.color = {{ color: 'rgba(190,190,200,0.18)', inherit: false }};
        update.width = 1;
      }} else if (ok) {{
        var col = EV_PALETTE[e.primary] || '#999';
        update.color = {{ color: col, inherit: false }};
        update.width = 1 + 4 * e.confidence + (e.source_count >= 2 ? 2 : 0);
      }}
      return update;
    }});

    var nodeUpdates = PAYLOAD.nodes.map(function(n) {{
      var st = nodeState[n.id];
      var base = TACTIC_PALETTE[n.tactic_layer % TACTIC_PALETTE.length];
      var isOrphan = !touching.has(n.id);
      if (st.visible) {{
        var hl = _filterState.highlight;
        if (hl) {{
          var inPath = false;
          hl.forEach(function(eid) {{
            var parts = eid.split('|');
            if (parts[0] === n.id || parts[1] === n.id) inPath = true;
          }});
          if (inPath) {{
            return {{ id: n.id, hidden: false, opacity: 1,
                     color: {{ background: base, border: PATH_HIGHLIGHT }},
                     borderWidth: 4 }};
          }}
          return {{ id: n.id, hidden: false, opacity: 0.18,
                   color: {{ background: '#dfdfe5', border: '#bbb' }}, borderWidth: 1 }};
        }}
        return {{ id: n.id, hidden: false, opacity: 1,
                 color: {{ background: base, border: '#222' }}, borderWidth: 1 }};
      }}
      if (_filterState.showExcluded) {{
        return {{ id: n.id, hidden: false, opacity: 0.18,
                 color: {{ background: '#dddddd', border: '#999999' }}, borderWidth: 1 }};
      }}
      return {{ id: n.id, hidden: true }};
    }});

    network.body.data.nodes.update(nodeUpdates);
    network.body.data.edges.update(edgeUpdates);

    /* Update header counts */
    var tc = 0, ec = 0, cc = 0, entC = 0, objC = 0;
    PAYLOAD.nodes.forEach(function(n) {{ if (nodeState[n.id].visible) tc++; }});
    PAYLOAD.edges.forEach(function(e) {{
      if (edgePassesFilters(e) &&
          nodeState[e.source].visible && nodeState[e.target].visible) {{
        ec++;
        if (e.source_count >= 2) cc++;
      }}
    }});
    PAYLOAD.entry_nodes.forEach(function(id) {{ if (nodeState[id] && nodeState[id].visible) entC++; }});
    PAYLOAD.objective_nodes.forEach(function(id) {{ if (nodeState[id] && nodeState[id].visible) objC++; }});
    document.getElementById('c-tech').textContent = tc + '/' + PAYLOAD.totals.techniques;
    document.getElementById('c-edge').textContent = ec + '/' + PAYLOAD.totals.edges;
    document.getElementById('c-cons').textContent = cc;
    document.getElementById('c-entry').textContent = entC;
    document.getElementById('c-obj').textContent = objC;

    /* Reachability of path-explorer targets follows the current filter state. */
    refreshPathControls();
  }}

  /* ---- Selection / detail panel ---- */
  var detail = document.getElementById('gap-detail');

  function escapeHtml(s) {{
    return (s || '').replace(/[&<>"']/g, function(c) {{
      return ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c];
    }});
  }}

  function renderNodeDetail(n) {{
    var deg = currentDegree(n.id);
    var mitreUrl = 'https://attack.mitre.org/techniques/' + n.id + '/';
    var html =
      '<h2><a href="'+mitreUrl+'" target="_blank">'+n.id+'</a> — '+escapeHtml(n.name)+'</h2>'+
      '<div class="kv"><span>Primary tactic</span><span>'+escapeHtml(n.tactic)+' (L'+n.tactic_layer+')</span></div>'+
      '<div class="kv"><span>All tactics</span><span>'+n.tactics.map(escapeHtml).join(', ')+'</span></div>'+
      '<div class="kv"><span>Platforms</span><span>'+(n.platforms.map(escapeHtml).join(', ')||'–')+'</span></div>'+
      '<div class="kv"><span>Campaigns</span><span>'+n.campaign_count+'</span></div>'+
      '<div class="kv"><span>Groups</span><span>'+n.group_count+'</span></div>'+
      '<div class="kv"><span>Sub-techniques</span><span>'+n.sub_count+'</span></div>'+
      '<div class="kv"><span>In / out (filtered)</span><span>'+deg.in_+' / '+deg.out+'</span></div>';
    if (n.groups.length) {{
      html += '<h4>Groups ('+n.groups.length+')</h4><ul>';
      n.groups.slice(0, 8).forEach(function(g) {{
        html += '<li><a href="https://attack.mitre.org/groups/'+g+'/" target="_blank">'+g+'</a></li>';
      }});
      if (n.groups.length > 8) html += '<li>…and '+(n.groups.length-8)+' more</li>';
      html += '</ul>';
    }}
    if (n.campaigns.length) {{
      html += '<h4>Campaigns ('+n.campaigns.length+')</h4><ul>';
      n.campaigns.slice(0, 8).forEach(function(c) {{
        html += '<li><a href="https://attack.mitre.org/campaigns/'+c+'/" target="_blank">'+c+'</a></li>';
      }});
      if (n.campaigns.length > 8) html += '<li>…and '+(n.campaigns.length-8)+' more</li>';
      html += '</ul>';
    }}
    detail.innerHTML = html;
  }}

  function renderEdgeDetail(e) {{
    var s = nodeById[e.source], t = nodeById[e.target];
    var html =
      '<h2>'+e.source+' → '+e.target+'</h2>'+
      '<div class="kv"><span>'+escapeHtml(s ? s.name : '')+'</span><span>'+escapeHtml(t ? t.name : '')+'</span></div>'+
      '<div class="kv"><span>Primary evidence</span><span>'+(EV_LABELS[e.primary]||e.primary)+'</span></div>'+
      '<div class="kv"><span>Source count</span><span>'+e.source_count+(e.source_count>=2?' (consensus)':'')+'</span></div>'+
      '<div class="kv"><span>Confidence</span><span>'+e.confidence.toFixed(3)+'</span></div>';
    if (e.support != null) html += '<div class="kv"><span>Support</span><span>'+e.support.toFixed(3)+'</span></div>';
    if (e.lift != null) html += '<div class="kv"><span>Lift</span><span>'+e.lift.toFixed(3)+'</span></div>';
    if (e.is_backward) html += '<div class="kv"><span>Direction</span><span>backward (loop)</span></div>';
    html += '<h4>Evidence ('+e.evidence.length+')</h4>';
    e.evidence.forEach(function(ev) {{
      var col = EV_PALETTE[ev.type] || '#999';
      html += '<div class="ev-block" style="border-left-color:'+col+'">'+
        '<div class="t" style="color:'+col+'">'+(EV_LABELS[ev.type]||ev.type)+'</div>'+
        (ev.desc ? '<div>'+escapeHtml(ev.desc)+'</div>' : '')+
        (ev.url  ? '<div><a href="'+escapeHtml(ev.url)+'" target="_blank">'+escapeHtml(ev.url)+'</a></div>' : '')+
      '</div>';
    }});
    detail.innerHTML = html;
  }}

  function currentDegree(nid) {{
    var inC = 0, outC = 0;
    PAYLOAD.edges.forEach(function(e) {{
      if (!edgePassesFilters(e)) return;
      if (e.source === nid) outC++;
      if (e.target === nid) inC++;
    }});
    return {{ in_: inC, out: outC }};
  }}

  network.on('click', function(params) {{
    if (params.nodes && params.nodes.length) {{
      var n = nodeById[params.nodes[0]];
      if (n) renderNodeDetail(n);
      return;
    }}
    if (params.edges && params.edges.length) {{
      var e = edgeById[params.edges[0]];
      if (e) renderEdgeDetail(e);
    }}
  }});

  /* ---- Tooltip on hover (lightweight; detail panel is the authoritative view) ---- */
  var tooltip = document.getElementById('gap-tooltip');
  network.on('hoverNode', function(params) {{
    var n = nodeById[params.node]; if (!n) return;
    tooltip.innerHTML = '<b>'+n.id+'</b> — '+escapeHtml(n.name)+'<br>'+
      escapeHtml(n.tactic)+' · '+n.campaign_count+' campaigns · '+n.group_count+' groups';
    tooltip.style.display = 'block';
  }});
  network.on('blurNode', function() {{ tooltip.style.display = 'none'; }});
  network.on('hoverEdge', function(params) {{
    var e = edgeById[params.edge]; if (!e) return;
    tooltip.innerHTML = '<b>'+e.source+' → '+e.target+'</b><br>'+
      (EV_LABELS[e.primary]||e.primary)+' · conf '+e.confidence.toFixed(2)+
      ' · '+e.source_count+' source(s)';
    tooltip.style.display = 'block';
  }});
  network.on('blurEdge', function() {{ tooltip.style.display = 'none'; }});
  document.getElementById('mynetwork').addEventListener('mousemove', function(ev) {{
    if (tooltip.style.display === 'block') {{
      tooltip.style.left = (ev.pageX + 15) + 'px';
      tooltip.style.top  = (ev.pageY + 15) + 'px';
    }}
  }});

  /* ---- Reachability and path-control updates ---- */
  function computeReachable(adj, src) {{
    var seen = new Set([src]);
    var stack = [src];
    while (stack.length) {{
      var cur = stack.pop();
      var neigh = adj[cur] || [];
      for (var i = 0; i < neigh.length; i++) {{
        if (!seen.has(neigh[i].target)) {{
          seen.add(neigh[i].target);
          stack.push(neigh[i].target);
        }}
      }}
    }}
    return seen;
  }}

  function countSimplePaths(adj, src, target, maxLen, cap) {{
    var count = 0;
    var visited = new Set([src]);
    function dfs(node, depth) {{
      if (count >= cap) return;
      if (node === target && depth > 0) {{ count++; return; }}
      if (depth >= maxLen) return;
      var neigh = adj[node] || [];
      for (var i = 0; i < neigh.length; i++) {{
        if (visited.has(neigh[i].target)) continue;
        visited.add(neigh[i].target);
        dfs(neigh[i].target, depth + 1);
        visited.delete(neigh[i].target);
        if (count >= cap) return;
      }}
    }}
    dfs(src, 0);
    return count;
  }}

  function refreshPathControls() {{
    var srcSel  = document.getElementById('p-src');
    var tgtSel  = document.getElementById('p-tgt');
    var info    = document.getElementById('p-info');
    var slider  = document.getElementById('p-k');
    var sliderV = document.getElementById('p-k-v');
    var src = srcSel.value;
    if (!src) {{ info.textContent = 'Select a source.'; return; }}

    var adj = buildAdjacency();
    var reachable = computeReachable(adj, src);

    /* Update target dropdown: disable unreachable, mark visually */
    Array.from(tgtSel.options).forEach(function(opt) {{
      if (!opt.dataset.origLabel) opt.dataset.origLabel = opt.text;
      var ok = (opt.value !== src) && reachable.has(opt.value);
      opt.disabled = !ok;
      opt.text = opt.dataset.origLabel + (ok ? '' : ' — unreachable');
    }});

    /* If currently selected target is now unreachable, jump to first reachable */
    var curOpt = tgtSel.options[tgtSel.selectedIndex];
    if (!curOpt || curOpt.disabled) {{
      for (var i = 0; i < tgtSel.options.length; i++) {{
        if (!tgtSel.options[i].disabled) {{ tgtSel.selectedIndex = i; break; }}
      }}
    }}

    var tgt = tgtSel.value;
    if (!tgt || !reachable.has(tgt)) {{
      info.innerHTML = '<b>No reachable objective</b> from '+src+' under current filters.<br>Relax filters or pick a different entry.';
      slider.max = 1;
      slider.value = 1;
      sliderV.textContent = '1';
      return;
    }}

    /* Count available simple paths up to length 6, cap at 50 */
    var n = countSimplePaths(adj, src, tgt, 6, 50);
    var label = (n >= 50 ? '50+' : String(n)) + ' path' + (n === 1 ? '' : 's');
    info.innerHTML = '<b>'+label+' available</b> from '+src+' to '+tgt+' (≤6 hops).';
    var maxK = Math.min(Math.max(n, 1), 8);
    slider.max = maxK;
    /* Default to 1 (the minimum viable configuration); never exceed available. */
    if (parseInt(slider.value, 10) > maxK) {{
      slider.value = maxK;
      sliderV.textContent = maxK;
    }}
  }}

  /* ---- Path finding ---- */
  function buildAdjacency() {{
    var adj = {{}};
    PAYLOAD.edges.forEach(function(e) {{
      if (!edgePassesFilters(e)) return;
      if (!adj[e.source]) adj[e.source] = [];
      adj[e.source].push({{ target: e.target, confidence: e.confidence, id: e._id }});
    }});
    return adj;
  }}

  function dijkstra(adj, src, target, blockedEdges) {{
    var dist = {{}}; var prevNode = {{}}; var prevEdge = {{}};
    dist[src] = 0;
    var visited = {{}};
    var pq = [{{n: src, d: 0}}];
    while (pq.length) {{
      pq.sort(function(a,b) {{ return a.d - b.d; }});
      var cur = pq.shift();
      if (visited[cur.n]) continue;
      visited[cur.n] = true;
      if (cur.n === target) break;
      var neigh = adj[cur.n] || [];
      for (var i = 0; i < neigh.length; i++) {{
        var ed = neigh[i];
        if (blockedEdges && blockedEdges.has(ed.id)) continue;
        var w = 1 / Math.max(ed.confidence, 0.01);
        var nd = cur.d + w;
        if (dist[ed.target] === undefined || nd < dist[ed.target]) {{
          dist[ed.target] = nd;
          prevNode[ed.target] = cur.n;
          prevEdge[ed.target] = ed.id;
          pq.push({{n: ed.target, d: nd}});
        }}
      }}
    }}
    if (dist[target] === undefined) return null;
    var nodes = [target], edges = [], cur = target;
    while (prevNode[cur] !== undefined) {{
      edges.unshift(prevEdge[cur]);
      cur = prevNode[cur];
      nodes.unshift(cur);
    }}
    return {{ nodes: nodes, edges: edges, cost: dist[target] }};
  }}

  /* Yen's k-shortest paths (simplified: blocked-edge iteration). */
  function yenKShortest(adj, src, target, k) {{
    var results = [];
    var first = dijkstra(adj, src, target, null);
    if (!first) return results;
    results.push(first);
    var candidates = [];
    for (var i = 1; i < k; i++) {{
      var last = results[results.length - 1];
      for (var j = 0; j < last.edges.length; j++) {{
        var blocked = new Set();
        blocked.add(last.edges[j]);
        /* also block the spur-prefix edges of previous results to avoid duplicates */
        results.forEach(function(r) {{
          var prefixMatches = true;
          for (var m = 0; m < j && m < r.edges.length; m++) {{
            if (r.edges[m] !== last.edges[m]) {{ prefixMatches = false; break; }}
          }}
          if (prefixMatches && r.edges.length > j) blocked.add(r.edges[j]);
        }});
        var spurSrc = last.nodes[j];
        var spurPath = dijkstra(adj, spurSrc, target, blocked);
        if (spurPath) {{
          /* concatenate root prefix with spur */
          var rootNodes = last.nodes.slice(0, j);
          var rootEdges = last.edges.slice(0, j);
          var total = {{
            nodes: rootNodes.concat(spurPath.nodes),
            edges: rootEdges.concat(spurPath.edges),
            cost: 0,
          }};
          /* recompute cost */
          total.cost = total.edges.reduce(function(acc, eid) {{
            var e = edgeById[eid];
            return acc + 1 / Math.max(e.confidence, 0.01);
          }}, 0);
          /* dedupe */
          var sig = total.nodes.join('>');
          if (!candidates.some(function(c) {{ return c.nodes.join('>') === sig; }}) &&
              !results.some(function(c) {{ return c.nodes.join('>') === sig; }})) {{
            candidates.push(total);
          }}
        }}
      }}
      if (!candidates.length) break;
      candidates.sort(function(a,b) {{ return a.cost - b.cost; }});
      results.push(candidates.shift());
    }}
    return results;
  }}

  function allSimplePaths(adj, src, target, maxLen) {{
    var results = [];
    var path = [src]; var edges = [];
    var visited = new Set([src]);
    function dfs(node) {{
      if (results.length >= 200) return; /* safety cap */
      if (path.length - 1 > maxLen) return;
      if (node === target && path.length > 1) {{
        results.push({{ nodes: path.slice(), edges: edges.slice(), cost: 0 }});
        return;
      }}
      var neigh = adj[node] || [];
      for (var i = 0; i < neigh.length; i++) {{
        var ed = neigh[i];
        if (visited.has(ed.target)) continue;
        visited.add(ed.target);
        path.push(ed.target); edges.push(ed.id);
        dfs(ed.target);
        path.pop(); edges.pop();
        visited.delete(ed.target);
      }}
    }}
    dfs(src);
    results.forEach(function(r) {{
      r.cost = r.edges.reduce(function(acc, eid) {{
        var e = edgeById[eid];
        return acc + 1 / Math.max(e.confidence, 0.01);
      }}, 0);
    }});
    results.sort(function(a,b) {{ return a.cost - b.cost; }});
    return results;
  }}

  function runPathQuery() {{
    var src = document.getElementById('p-src').value;
    var tgt = document.getElementById('p-tgt').value;
    var algo = document.getElementById('p-algo').value;
    var k = parseInt(document.getElementById('p-k').value, 10);
    if (!src || !tgt) return;
    var adj = buildAdjacency();
    var paths = algo === 'yen' ? yenKShortest(adj, src, tgt, k)
                               : allSimplePaths(adj, src, tgt, k);
    if (algo === 'all' && paths.length > 50) {{
      if (!confirm(paths.length + ' paths found. Rendering all (may be slow). Continue?')) {{
        paths = paths.slice(0, 50);
      }}
    }}
    renderPathResults(paths, src, tgt);
  }}

  function renderPathResults(paths, src, tgt) {{
    if (!paths.length) {{
      detail.innerHTML = '<h2>No paths</h2><p>No path from '+src+' to '+tgt+
        ' under the current filters. Try relaxing source selection or confidence threshold.</p>';
      _filterState.highlight = null;
      applyFilters();
      return;
    }}
    var highlightSet = new Set();
    var html = '<h2>Attack paths: '+src+' → '+tgt+'</h2>'+
               '<p style="font-size:11px;color:#666">'+paths.length+
               ' path(s). Weight = Σ 1/confidence (lower = higher-trust route).</p>';
    paths.forEach(function(p, i) {{
      p.edges.forEach(function(eid) {{ highlightSet.add(eid); }});
      var steps = p.nodes.join(' → ');
      html += '<div class="path-item"><div class="pstep">'+steps+'</div>'+
              '<div class="pmeta">len '+(p.nodes.length-1)+' · cost '+p.cost.toFixed(2)+'</div></div>';
    }});
    detail.innerHTML = html;
    _filterState.highlight = highlightSet;
    applyFilters();
  }}

  /* ---- Legend ---- */
  var legend = document.getElementById('gap-legend');

  function buildLegend() {{
    var html = '';
    /* Node colour */
    html += '<div class="lg-section"><h4>Node colour = tactic layer</h4>';
    for (var i = 0; i < TACTIC_LABELS.length; i += 1) {{
      var col = TACTIC_PALETTE[i % TACTIC_PALETTE.length];
      html += '<div class="lg-row" style="display:inline-flex;margin-right:8px">'+
              '<span class="swatch" style="background:'+col+'"></span>L'+i+' '+TACTIC_LABELS[i]+'</div>';
      if ((i+1) % 7 === 0) html += '<br>';
    }}
    html += '</div>';

    /* Node size */
    html += '<div class="lg-section"><h4>Node size = campaign count</h4>'+
            '<div class="lg-row">'+
              '<span class="size-dot" style="width:10px;height:10px"></span>rare&nbsp;'+
              '<span class="size-dot" style="width:18px;height:18px"></span>common&nbsp;'+
              '<span class="size-dot" style="width:26px;height:26px"></span>pervasive'+
            '</div>'+
            '<div class="lg-row"><span class="dot" style="background:#80b1d3"></span>has edges '+
              '&nbsp;<span class="diamond"></span>orphan</div>'+
            '</div>';

    /* Edge colour */
    html += '<div class="lg-section"><h4>Edge colour = primary evidence</h4>';
    allEvidenceTypes.forEach(function(s) {{
      var c = EV_PALETTE[s] || '#999';
      html += '<div class="lg-row"><span class="line" style="border-top-color:'+c+'"></span>'+
              (EV_LABELS[s] || s)+'</div>';
    }});
    html += '</div>';

    /* Edge width/style */
    html += '<div class="lg-section"><h4>Edge width = confidence</h4>'+
            '<div class="lg-row"><span class="line"></span>low</div>'+
            '<div class="lg-row"><span class="line thick"></span>high + consensus</div>'+
            '<div class="lg-row" style="font-size:9px;color:#666;max-width:180px;margin-top:2px">'+
              'Attack Flow=1.0, Ontology=0.8, Co-occurrence=P(t|s); merged = max'+
            '</div>'+
            '</div>'+
            '<div class="lg-section"><h4>Edge style</h4>'+
            '<div class="lg-row"><span class="line"></span>forward</div>'+
            '<div class="lg-row"><span class="line dashed"></span>backward (loop)</div>'+
            '<div class="lg-row"><span class="line dotted"></span>co-occurrence only (lower trust)</div>'+
            '</div>';

    legend.innerHTML = html;
  }}
  buildLegend();

  /* ---- Tactic layer canvas overlay (column backgrounds + headers) ---- */
  network.on('afterDrawing', function(ctx) {{
    ctx.save();
    var halfW = X_SPACING / 2 - 10;
    var topY  = -80;
    var botY  = MAX_Y + 40;
    LAYER_DATA.forEach(function(lyr) {{
      ctx.fillStyle = lyr.layer % 2 === 0
        ? 'rgba(0,0,0,0.025)' : 'rgba(0,0,0,0.055)';
      ctx.fillRect(lyr.x - halfW, topY - 60, X_SPACING - 20, botY - topY + 120);
    }});
    LAYER_DATA.forEach(function(lyr) {{
      var col = TACTIC_PALETTE[lyr.layer % TACTIC_PALETTE.length];
      var text = lyr.label;
      ctx.font = 'bold 13px "Segoe UI", Tahoma, sans-serif';
      var tw = ctx.measureText(text).width;
      var boxW = Math.max(tw + 24, 130);
      var boxH = 28;
      var boxX = lyr.x - boxW / 2;
      var boxY = topY - 58 - boxH;
      var r = 6;
      ctx.beginPath();
      ctx.moveTo(boxX + r, boxY);
      ctx.lineTo(boxX + boxW - r, boxY);
      ctx.quadraticCurveTo(boxX + boxW, boxY, boxX + boxW, boxY + r);
      ctx.lineTo(boxX + boxW, boxY + boxH - r);
      ctx.quadraticCurveTo(boxX + boxW, boxY + boxH, boxX + boxW - r, boxY + boxH);
      ctx.lineTo(boxX + r, boxY + boxH);
      ctx.quadraticCurveTo(boxX, boxY + boxH, boxX, boxY + boxH - r);
      ctx.lineTo(boxX, boxY + r);
      ctx.quadraticCurveTo(boxX, boxY, boxX + r, boxY);
      ctx.closePath();
      ctx.fillStyle = col + 'cc';
      ctx.fill();
      ctx.strokeStyle = col;
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillStyle = '#111111';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(text, lyr.x, boxY + boxH / 2);
      ctx.font = '11px "Segoe UI", Tahoma, sans-serif';
      ctx.fillStyle = '#666666';
      ctx.fillText('Layer ' + lyr.layer, lyr.x, boxY + boxH + 14);
    }});
    ctx.restore();
  }});

  /* ---- Initial render ---- */
  applyFilters();
  network.redraw();
  setTimeout(function() {{ network.fit(); }}, 100);
}})();
</script>
"""
