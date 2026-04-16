"""
Phase 1: Parse the MITRE ATT&CK STIX bundle into TechniqueNode objects.

Techniques are the default granularity; sub-techniques collapse to parent
(see Section 4.1, D7). Provenance metadata (campaign/group/software usage)
is attached to each node from STIX `relationship` objects of type `uses`.
"""

from __future__ import annotations

import json
from typing import Iterable

from mtdsim.attacker.gap.schema import (
    TACTIC_LAYERS,
    CampaignProfile,
    GroupProfile,
    TechniqueNode,
)


def _external_id(obj: dict) -> str:
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == "mitre-attack":
            return ref.get("external_id", "")
    return ""


def _tactics_from_phases(obj: dict) -> list[str]:
    return [
        p.get("phase_name", "")
        for p in obj.get("kill_chain_phases", [])
        if p.get("kill_chain_name") == "mitre-attack"
    ]


def _parent_technique_id(tid: str) -> str:
    """Collapse sub-technique IDs (e.g. T1059.001) to parent (T1059)."""
    return tid.split(".", 1)[0] if "." in tid else tid


def parse_stix_bundle(
    bundle_path_or_obj,
) -> tuple[dict[str, TechniqueNode], dict]:
    """
    Parse an Enterprise ATT&CK STIX bundle.

    Parameters
    ----------
    bundle_path_or_obj : str | dict
        Path to ``enterprise-attack.json``, or an already-loaded bundle dict.

    Returns
    -------
    (nodes, index)
        ``nodes`` maps parent technique ID ("T1059") -> TechniqueNode.
        ``index`` exposes STIX bookkeeping needed by downstream phases:
            - ``stix_to_tid``: STIX attack-pattern UUID -> parent technique ID
            - ``group_ids``: list of intrusion-set STIX UUIDs
            - ``software_ids``: list of malware/tool STIX UUIDs
            - ``campaign_ids``: list of campaign STIX UUIDs
            - ``relationships``: list of (source_ref, target_ref) `uses` tuples
            - ``campaign_to_tactic_id``: campaign STIX UUID -> external campaign ID (e.g. C0001)
            - ``group_to_gid``: group STIX UUID -> external group ID (e.g. G0007)
    """
    if isinstance(bundle_path_or_obj, (str, bytes)):
        with open(bundle_path_or_obj) as f:
            bundle = json.load(f)
    else:
        bundle = bundle_path_or_obj

    objects: list[dict] = bundle.get("objects", [])

    attack_patterns: dict[str, dict] = {}       # stix id -> obj
    intrusion_sets: dict[str, dict] = {}
    softwares: dict[str, dict] = {}             # malware + tool
    campaigns: dict[str, dict] = {}
    relationships: list[dict] = []

    for obj in objects:
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue
        t = obj.get("type")
        if t == "attack-pattern":
            attack_patterns[obj["id"]] = obj
        elif t == "intrusion-set":
            intrusion_sets[obj["id"]] = obj
        elif t in ("malware", "tool"):
            softwares[obj["id"]] = obj
        elif t == "campaign":
            campaigns[obj["id"]] = obj
        elif t == "relationship" and obj.get("relationship_type") == "uses":
            relationships.append(obj)

    # Build nodes (collapsing sub-techniques)
    nodes: dict[str, TechniqueNode] = {}
    stix_to_tid: dict[str, str] = {}

    for stix_id, ap in attack_patterns.items():
        raw_tid = _external_id(ap)
        if not raw_tid:
            continue
        parent_tid = _parent_technique_id(raw_tid)
        stix_to_tid[stix_id] = parent_tid

        tactics = _tactics_from_phases(ap)
        primary = min(
            (t for t in tactics if t in TACTIC_LAYERS),
            key=lambda t: TACTIC_LAYERS[t],
            default="",
        )
        layer = TACTIC_LAYERS.get(primary, -1)

        if parent_tid not in nodes:
            nodes[parent_tid] = TechniqueNode(
                technique_id=parent_tid,
                technique_name=ap.get("name", "") if parent_tid == raw_tid else "",
                tactics=list(tactics),
                primary_tactic=primary,
                tactic_layer=layer,
                platforms=list(ap.get("x_mitre_platforms", []) or []),
                description=(ap.get("description", "") or "") if parent_tid == raw_tid else "",
            )
        # If this IS the parent technique (not a sub-technique), fill its name/description
        if parent_tid == raw_tid:
            node = nodes[parent_tid]
            node.technique_name = ap.get("name", node.technique_name)
            node.description = ap.get("description", node.description) or node.description
            # Merge tactics in case parent already created from a sub-technique first
            for t in tactics:
                if t not in node.tactics:
                    node.tactics.append(t)
            # Recompute primary/layer from full tactic list
            node.primary_tactic = min(
                (t for t in node.tactics if t in TACTIC_LAYERS),
                key=lambda t: TACTIC_LAYERS[t],
                default=node.primary_tactic,
            )
            node.tactic_layer = TACTIC_LAYERS.get(node.primary_tactic, node.tactic_layer)
        else:
            nodes[parent_tid].sub_technique_ids.append(raw_tid)

    # Attach provenance from `uses` relationships
    group_to_gid = {sid: _external_id(o) for sid, o in intrusion_sets.items()}
    campaign_to_cid = {sid: _external_id(o) for sid, o in campaigns.items()}

    for rel in relationships:
        target = rel.get("target_ref", "")
        source = rel.get("source_ref", "")
        tid = stix_to_tid.get(target)
        if tid is None or tid not in nodes:
            continue
        node = nodes[tid]
        if source in intrusion_sets:
            gid = group_to_gid.get(source, source)
            if gid and gid not in node.group_ids:
                node.group_ids.append(gid)
        elif source in softwares:
            sid = _external_id(softwares[source]) or source
            if sid and sid not in node.software_ids:
                node.software_ids.append(sid)
        elif source in campaigns:
            cid = campaign_to_cid.get(source, source)
            if cid and cid not in node.campaign_ids:
                node.campaign_ids.append(cid)

    for node in nodes.values():
        node.group_count = len(node.group_ids)
        node.campaign_count = len(node.campaign_ids)

    # Build GroupProfile stubs (motivation fields filled later by enrichment)
    group_profiles: dict[str, GroupProfile] = {}
    for sid, obj in intrusion_sets.items():
        gid = group_to_gid.get(sid) or ""
        if not gid:
            continue
        group_profiles[gid] = GroupProfile(
            group_id=gid,
            name=obj.get("name", gid),
            aliases=list(obj.get("aliases", []) or []),
            description=obj.get("description", "") or "",
            sources=["mitre"],
        )

    # Build CampaignProfile stubs from MITRE-native campaigns. Campaign ->
    # group attribution is resolved via `attributed-to` relationships if present;
    # otherwise the campaign stays unattributed and UI shows it as such.
    attributed_to: dict[str, list[str]] = {}
    for rel in bundle.get("objects", []):
        if rel.get("type") != "relationship":
            continue
        if rel.get("relationship_type") != "attributed-to":
            continue
        src, tgt = rel.get("source_ref", ""), rel.get("target_ref", "")
        if src in campaigns and tgt in intrusion_sets:
            gid = group_to_gid.get(tgt)
            if gid:
                attributed_to.setdefault(src, []).append(gid)

    # Collect technique_ids per campaign from `uses` relationships
    campaign_techniques: dict[str, list[str]] = {}
    for rel in relationships:
        src = rel.get("source_ref", "")
        tgt = rel.get("target_ref", "")
        if src in campaigns:
            tid = stix_to_tid.get(tgt)
            if tid:
                lst = campaign_techniques.setdefault(src, [])
                if tid not in lst:
                    lst.append(tid)

    campaign_profiles: dict[str, CampaignProfile] = {}
    for sid, obj in campaigns.items():
        cid = campaign_to_cid.get(sid) or ""
        if not cid:
            continue
        campaign_profiles[cid] = CampaignProfile(
            campaign_id=cid,
            name=obj.get("name", cid),
            description=obj.get("description", "") or "",
            group_ids=list(attributed_to.get(sid, [])),
            first_seen=obj.get("first_seen", "") or "",
            technique_ids=list(campaign_techniques.get(sid, [])),
            source="mitre",
        )

    index = {
        "stix_to_tid": stix_to_tid,
        "group_ids": list(intrusion_sets.keys()),
        "software_ids": list(softwares.keys()),
        "campaign_ids": list(campaigns.keys()),
        "relationships": [(r["source_ref"], r["target_ref"]) for r in relationships],
        "campaign_to_cid": campaign_to_cid,
        "group_to_gid": group_to_gid,
        "group_profiles": group_profiles,
        "campaign_profiles": campaign_profiles,
    }
    return nodes, index
