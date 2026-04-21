"""
Build the JSON payload consumed by the Cytoscape.js viewer.

The payload is pure serialisation: given a GAP (and optionally a
``SubgraphView`` restricting which nodes/edges appear), produce the
JSON consumed by ``assets/app.js``. Colour palettes and label maps
live in ``theme.py``; subgraph selection lives in ``gap/selectors/``.

Pre-computed subgraph membership lists (Strategy A — by terminal-objective
tactic; Strategy B — by platform profile) are embedded so the viewer can
restrict the view by either selector without re-running graph traversal
in the browser. These are the two primary strategies recommended by the
2026-04-17 subgraphing exploration notebook.

Per-group and per-campaign technique counts are also precomputed so the
UI can preview the selection size before the user clicks.
"""

from __future__ import annotations

from typing import Any, Optional

import networkx as nx

from mtdsim.attacker.gap.schema import GeneralisedAttackProfile, TACTIC_ORDER
from mtdsim.attacker.gap.selectors import (
    PLATFORM_PROFILES,
    SubgraphView,
    platform_profile,
)
from mtdsim.attacker.gap.viz.theme import (
    DEFAULT_VISIBLE_EVIDENCE,
    EVIDENCE_COLOUR,
    EVIDENCE_LABEL,
    TACTIC_PALETTE,
)


def _tactic_label(t: str) -> str:
    return t.replace("-", " ").title()


def _primary_evidence_type(edge) -> str:
    """Pick the most authoritative evidence type to use for edge colouring."""
    priority = ("attack_flow", "cti_report", "caldera_sequence",
                "ontology", "documentation", "co_occurrence")
    types = {ev.source_type for ev in edge.evidence}
    for p in priority:
        if p in types:
            return p
    return edge.evidence_type


def _full_digraph(gap: GeneralisedAttackProfile) -> nx.DiGraph:
    g = nx.DiGraph()
    for tid in gap.nodes:
        g.add_node(tid)
    for e in gap.edges:
        g.add_edge(e.source_id, e.target_id)
    return g


def build_payload(
    gap: GeneralisedAttackProfile,
    view: Optional[SubgraphView] = None,
) -> dict[str, Any]:
    """Return the full JSON payload dict for the Cytoscape viewer.

    When ``view`` is provided, nodes and edges are restricted to the
    view's sets and ``meta.view`` records the selector provenance so the
    UI can label the subgraph. Unrestricted GAP-wide totals are also
    reported so the UI can show "n / total" style counts.
    """

    if view is None:
        node_filter = lambda tid: True  # noqa: E731
        edge_filter = lambda e: True    # noqa: E731
    else:
        node_set = view.node_set
        edge_set = view.edge_set
        node_filter = lambda tid: tid in node_set           # noqa: E731
        edge_filter = lambda e: (e.source_id, e.target_id) in edge_set  # noqa: E731

    shown_nodes = [tid for tid in gap.nodes if node_filter(tid)]
    shown_edges = [e for e in gap.edges if edge_filter(e)]

    # ------------------------------------------------------------------
    # Pre-compute reachability + CSA subgraph membership over the FULL
    # graph (not the view) so client-side filters compose correctly when
    # no server-side view is applied.
    digraph = _full_digraph(gap)

    reachable_from_entry: set[str] = set(gap.entry_nodes)
    for entry in gap.entry_nodes:
        if entry in digraph:
            reachable_from_entry.update(nx.descendants(digraph, entry))

    objective_tactics_seen = sorted(
        {gap.nodes[t].primary_tactic for t in gap.objective_nodes
         if t in gap.nodes},
        key=lambda x: TACTIC_ORDER.index(x) if x in TACTIC_ORDER else 99,
    )
    subgraph_terminal: dict[str, list[str]] = {}
    for tactic in objective_tactics_seen:
        targets = [
            t for t in gap.objective_nodes
            if gap.nodes[t].primary_tactic == tactic
        ]
        if not targets:
            continue
        members = set(targets)
        for t in targets:
            if t in digraph:
                members.update(nx.ancestors(digraph, t))
        subgraph_terminal[tactic] = sorted(members)

    # Strategy 2b — per-technique terminal-objective ancestor subgraph.
    subgraph_terminal_technique: dict[str, list[str]] = {}
    for tid in gap.objective_nodes:
        if tid not in digraph:
            continue
        members = {tid}
        members.update(nx.ancestors(digraph, tid))
        subgraph_terminal_technique[tid] = sorted(members)

    # Strategy 2c — per-technique group-witnessed ancestor subgraph.
    # Constrains the ancestor cone to techniques that share at least one MITRE
    # group with the terminal. Chosen in the 2026-04-17 subgraph exploration
    # notebook over depth-bound / campaign-witnessed / platform-cross-product
    # variants (rubric 22/30) because it anchors each profile to an observed
    # APT. Keys mirror ``subgraph_terminal_technique`` so the UI can offer both
    # views from the same dropdown shape.
    subgraph_terminal_group_witnessed: dict[str, list[str]] = {}
    for tid in gap.objective_nodes:
        if tid not in digraph:
            continue
        target_groups = set(gap.nodes[tid].group_ids)
        ancestors = {tid} | set(nx.ancestors(digraph, tid))
        if not target_groups:
            members = {tid}
        else:
            members = {
                a for a in ancestors
                if a == tid or (set(gap.nodes[a].group_ids) & target_groups)
            }
        subgraph_terminal_group_witnessed[tid] = sorted(members)

    node_platform_profile = {
        tid: platform_profile(n.platforms) for tid, n in gap.nodes.items()
    }
    subgraph_platform: dict[str, list[str]] = {}
    for profile in PLATFORM_PROFILES:
        members = [tid for tid, p in node_platform_profile.items() if p == profile]
        if members:
            subgraph_platform[profile] = sorted(members)

    # --- Meta ---------------------------------------------------------------
    meta: dict[str, Any] = {
        "version": gap.version,
        "build_date": gap.build_date,
        "technique_source": gap.technique_source,
        "counts": {
            "techniques": len(shown_nodes),
            "edges": len(shown_edges),
            "consensus_edges": sum(1 for e in shown_edges if e.source_count >= 2),
            "backward_edges": sum(1 for e in shown_edges if e.is_backward),
            "groups": len(gap.groups),
            "campaigns": len(gap.campaigns),
        },
        "totals": {
            "techniques": gap.total_techniques,
            "edges": gap.edge_count,
        },
    }
    if view is not None:
        meta["view"] = dict(view.provenance)

    # --- Taxonomies ---------------------------------------------------------
    tactics = [
        {"id": t, "label": _tactic_label(t), "layer": i, "color": TACTIC_PALETTE[i]}
        for i, t in enumerate(TACTIC_ORDER)
    ]

    evidence_types_seen = sorted({
        ev.source_type for e in shown_edges for ev in e.evidence
    } | {e.evidence_type for e in shown_edges})
    evidence_types = [
        {
            "id": et,
            "label": EVIDENCE_LABEL.get(et, et),
            "color": EVIDENCE_COLOUR.get(et, "#999999"),
            "default_visible": et in DEFAULT_VISIBLE_EVIDENCE,
        }
        for et in evidence_types_seen
    ]

    # --- Groups & campaigns -------------------------------------------------
    # Per-group technique counts over the *shown* node set so the UI label
    # reflects what the user will actually see when they click the filter.
    group_tech_count: dict[str, int] = {}
    for tid in shown_nodes:
        for gid in gap.nodes[tid].group_ids:
            group_tech_count[gid] = group_tech_count.get(gid, 0) + 1

    groups = {
        gid: {
            "id": gid,
            "name": g.name,
            "aliases": g.aliases,
            "regions": g.regions,
            "suspected_origin": g.suspected_origin,
            "sources": g.sources,
            "description": (g.description or "")[:600],
            "technique_count": group_tech_count.get(gid, 0),
        }
        for gid, g in gap.groups.items()
    }

    campaigns = {
        cid: {
            "id": cid,
            "name": c.name,
            "group_ids": c.group_ids,
            "technique_ids": c.technique_ids,
            "source": c.source,
            "first_seen": c.first_seen,
            "description": (c.description or "")[:400],
            "technique_count": sum(1 for t in c.technique_ids if t in gap.nodes),
        }
        for cid, c in gap.campaigns.items()
    }

    # --- Nodes --------------------------------------------------------------
    edge_endpoints: set[str] = set()
    for e in shown_edges:
        edge_endpoints.add(e.source_id)
        edge_endpoints.add(e.target_id)

    entry_set = set(gap.entry_nodes)
    objective_set = set(gap.objective_nodes)

    nodes = []
    for tid in shown_nodes:
        n = gap.nodes[tid]
        nodes.append({
            "id": tid,
            "label": n.technique_name,
            "tactic": n.primary_tactic,
            "layer": n.tactic_layer,
            "tactics": n.tactics,
            "platforms": n.platforms,
            "platform_profile": node_platform_profile.get(tid, "unspecified"),
            "group_ids": n.group_ids,
            "group_count": n.group_count,
            "campaign_ids": n.campaign_ids,
            "campaign_count": n.campaign_count,
            "sub_technique_ids": n.sub_technique_ids,
            "orphan": tid not in edge_endpoints,
            "is_entry": tid in entry_set,
            "is_objective": tid in objective_set,
            "reachable_from_entry": tid in reachable_from_entry,
            "description": (n.description or "")[:400],
        })

    # --- Edges --------------------------------------------------------------
    edges = []
    for e in shown_edges:
        ev_types = sorted({ev.source_type for ev in e.evidence}) or [e.evidence_type]
        campaigns_for_edge: list[str] = []
        for ev in e.evidence:
            for c in ev.campaigns:
                if c not in campaigns_for_edge:
                    campaigns_for_edge.append(c)
        # Groups implicated via the campaigns that produced this edge (Attack
        # Flow: .afb name -> AF:<name> -> campaign.group_ids; MITRE native
        # campaigns carry group_ids directly from `attributed-to`).
        source_groups: list[str] = []
        for cname in campaigns_for_edge:
            for cid in (cname, f"AF:{cname}"):
                cprof = gap.campaigns.get(cid)
                if cprof:
                    for gid in cprof.group_ids:
                        if gid not in source_groups:
                            source_groups.append(gid)
                    break
        # Union groups via endpoint technique attribution for co-occurrence /
        # ontology edges (which have no campaign provenance).
        if not source_groups and not campaigns_for_edge:
            for gid in gap.nodes[e.source_id].group_ids:
                if gid in gap.nodes[e.target_id].group_ids and gid not in source_groups:
                    source_groups.append(gid)

        edges.append({
            "id": f"{e.source_id}__{e.target_id}",
            "source": e.source_id,
            "target": e.target_id,
            "evidence_types": ev_types,
            "primary_evidence": _primary_evidence_type(e),
            "confidence": e.confidence,
            "support": e.support,
            "lift": e.lift,
            "source_count": e.source_count,
            "consensus": e.source_count >= 2,
            "backward": e.is_backward,
            "campaigns": campaigns_for_edge,
            "source_groups": source_groups,
            "evidence": [
                {
                    "source_type": ev.source_type,
                    "source_url": ev.source_url,
                    "description": ev.description,
                    "campaigns": ev.campaigns,
                }
                for ev in e.evidence
            ],
        })

    # --- Entry / objective node summaries (for path-explorer dropdowns) -----
    def _layer_key(t: str) -> tuple[int, str]:
        return (gap.nodes[t].tactic_layer if t in gap.nodes else 99, t)

    entry_nodes_payload = [
        {
            "id": tid,
            "label": gap.nodes[tid].technique_name,
            "tactic": gap.nodes[tid].primary_tactic,
        }
        for tid in sorted(gap.entry_nodes, key=_layer_key)
        if tid in gap.nodes
    ]
    objective_nodes_payload = [
        {
            "id": tid,
            "label": gap.nodes[tid].technique_name,
            "tactic": gap.nodes[tid].primary_tactic,
            "reachable_from_entry": tid in reachable_from_entry,
        }
        for tid in sorted(gap.objective_nodes, key=_layer_key)
        if tid in gap.nodes
    ]

    return {
        "meta": meta,
        "tactics": tactics,
        "evidence_types": evidence_types,
        "groups": groups,
        "campaigns": campaigns,
        "nodes": nodes,
        "edges": edges,
        "entry_nodes": entry_nodes_payload,
        "objective_nodes": objective_nodes_payload,
        "subgraphs": {
            "terminal_objective": subgraph_terminal,
            "terminal_technique": subgraph_terminal_technique,
            "terminal_group_witnessed": subgraph_terminal_group_witnessed,
            "platform": subgraph_platform,
        },
    }
