"""
Build the JSON payload consumed by the Cytoscape.js viewer.

The payload is the single source of truth for the browser: nodes, edges,
groups, campaigns, tactics, evidence types, and motivation taxonomy. All
filtering in the UI is client-side, operating on this payload.
"""

from __future__ import annotations

from typing import Any

from mtdsim.attacker.gap.schema import (
    GeneralisedAttackProfile,
    MOTIVATION_CATEGORIES,
    TACTIC_ORDER,
)


# 14-colour categorical palette for tactic layers (0-13) — ColorBrewer Set3+.
TACTIC_PALETTE = [
    "#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462",
    "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
    "#1f78b4", "#e31a1c",
]

EVIDENCE_COLOUR = {
    "attack_flow":      "#2ca02c",
    "co_occurrence":    "#1f77b4",
    "caldera_sequence": "#ff7f0e",
    "ontology":         "#9467bd",
    "documentation":    "#7f7f7f",
    "cti_report":       "#17becf",
}

EVIDENCE_LABEL = {
    "attack_flow":      "Attack Flow (MITRE CTID)",
    "co_occurrence":    "Co-occurrence (mined)",
    "ontology":         "Ontology (STIX descriptions)",
    "documentation":    "Documentation",
    "cti_report":       "CTI report",
    "caldera_sequence": "CALDERA sequence",
}

# Attack Flow is the default-visible evidence source per the research narrative.
DEFAULT_VISIBLE_EVIDENCE = {"attack_flow"}

MOTIVATION_COLOUR = {
    "information_theft_espionage": "#5e81ac",
    "financial_gain":              "#a3be8c",
    "financial_crime":              "#d08770",
    "sabotage_destruction":        "#bf616a",
}

MOTIVATION_LABEL = {
    "information_theft_espionage": "Espionage / Information theft",
    "financial_gain":              "Financial gain",
    "financial_crime":              "Financial crime",
    "sabotage_destruction":        "Sabotage / Destruction",
}


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


def build_payload(gap: GeneralisedAttackProfile) -> dict[str, Any]:
    """Return the full JSON payload dict for the Cytoscape viewer."""

    # --- Meta ---------------------------------------------------------------
    meta = {
        "version": gap.version,
        "build_date": gap.build_date,
        "technique_source": gap.technique_source,
        "counts": {
            "techniques": gap.total_techniques,
            "edges": gap.edge_count,
            "consensus_edges": gap.consensus_edge_count,
            "backward_edges": gap.backward_edge_count,
            "orphans": gap.orphan_techniques,
            "groups": len(gap.groups),
            "campaigns": len(gap.campaigns),
        },
    }

    # --- Taxonomies ---------------------------------------------------------
    tactics = [
        {"id": t, "label": _tactic_label(t), "layer": i, "color": TACTIC_PALETTE[i]}
        for i, t in enumerate(TACTIC_ORDER)
    ]

    evidence_types_seen = sorted({
        ev.source_type for e in gap.edges for ev in e.evidence
    } | {e.evidence_type for e in gap.edges})
    evidence_types = [
        {
            "id": et,
            "label": EVIDENCE_LABEL.get(et, et),
            "color": EVIDENCE_COLOUR.get(et, "#999999"),
            "default_visible": et in DEFAULT_VISIBLE_EVIDENCE,
        }
        for et in evidence_types_seen
    ]

    motivations = [
        {"id": m, "label": MOTIVATION_LABEL[m], "color": MOTIVATION_COLOUR[m]}
        for m in MOTIVATION_CATEGORIES
    ]

    # --- Groups & campaigns -------------------------------------------------
    groups = {
        gid: {
            "id": gid,
            "name": g.name,
            "aliases": g.aliases,
            "motivations": g.motivations,
            "misp_motivations": g.misp_motivations,
            "regions": g.regions,
            "suspected_origin": g.suspected_origin,
            "sources": g.sources,
            "description": (g.description or "")[:600],
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
        }
        for cid, c in gap.campaigns.items()
    }

    # --- Nodes --------------------------------------------------------------
    # Precompute per-node motivation union from attributed groups
    def _node_motivations(node_group_ids: list[str]) -> list[str]:
        found: list[str] = []
        for gid in node_group_ids:
            for m in (gap.groups.get(gid).motivations if gid in gap.groups else []):
                if m not in found:
                    found.append(m)
        return found

    edge_endpoints: set[str] = set()
    for e in gap.edges:
        edge_endpoints.add(e.source_id)
        edge_endpoints.add(e.target_id)

    nodes = []
    for tid, n in gap.nodes.items():
        nodes.append({
            "id": tid,
            "label": n.technique_name,
            "tactic": n.primary_tactic,
            "layer": n.tactic_layer,
            "tactics": n.tactics,
            "platforms": n.platforms,
            "group_ids": n.group_ids,
            "group_count": n.group_count,
            "campaign_ids": n.campaign_ids,
            "campaign_count": n.campaign_count,
            "sub_technique_ids": n.sub_technique_ids,
            "motivations": _node_motivations(n.group_ids),
            "orphan": tid not in edge_endpoints,
            "description": (n.description or "")[:400],
        })

    # --- Edges --------------------------------------------------------------
    edges = []
    for e in gap.edges:
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
        # Also union groups via endpoint technique attribution for
        # co-occurrence / ontology edges (which have no campaign provenance).
        if not source_groups and not campaigns_for_edge:
            for gid in gap.nodes[e.source_id].group_ids:
                if gid in gap.nodes[e.target_id].group_ids and gid not in source_groups:
                    source_groups.append(gid)

        motivations: list[str] = []
        for gid in source_groups:
            for m in (gap.groups.get(gid).motivations if gid in gap.groups else []):
                if m not in motivations:
                    motivations.append(m)

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
            "motivations": motivations,
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

    return {
        "meta": meta,
        "tactics": tactics,
        "evidence_types": evidence_types,
        "motivations": motivations,
        "groups": groups,
        "campaigns": campaigns,
        "nodes": nodes,
        "edges": edges,
    }
