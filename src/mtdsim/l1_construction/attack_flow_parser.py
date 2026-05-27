"""Parse a single Attack Flow **STIX 2.1 bundle** into a :class:`PerFlowExtract`.

This is the lossless L0->per-flow step (§c). It reads the four Attack Flow SDO
types and their typed reference lists:

- ``attack-action``    -> action node (``technique_id``, ``name``, ``tactic``,
                          ``confidence``); ``effect_refs`` -> ``effect`` edges.
- ``attack-operator``  -> operator node (``operator`` AND/OR); ``effect_refs``.
- ``attack-condition`` -> condition node (``description``); ``on_true_refs`` ->
                          ``on_true`` edges, ``on_false_refs`` -> ``on_false``.
- ``attack-flow``      -> flow metadata (``name``, ``scope``, ``start_refs``,
                          ``external_references``).

We deliberately do **not** parse the ``.afb`` Builder format (a layout-oriented
serialisation where connectivity is implicit in anchors/latches — the source of
v0.4's pixel-proximity hack). The STIX export carries the dependency graph
explicitly, so the parser is exact.

Out of scope per §c: assets, command refs, infrastructure, notes — they carry no
sequencing. Refs to such objects are simply skipped (no edge created).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Union

from mtdsim.l1_construction.schema import (
    TACTIC_ID_TO_NAME,
    FlowEdge,
    FlowNode,
    PerFlowExtract,
)

# STIX type -> the local-id prefix we assign.
_KIND_BY_TYPE = {
    "attack-action": ("action", "a"),
    "attack-operator": ("operator", "op"),
    "attack-condition": ("condition", "c"),
}

# (ref field on a node) -> (edge type emitted).
_REF_FIELDS = (
    ("effect_refs", "effect"),
    ("on_true_refs", "on_true"),
    ("on_false_refs", "on_false"),
)

_AF_EXTENSION_ID = "extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4"


def slugify(name: str) -> str:
    """``"Tesla Kubernetes Breach"`` -> ``"tesla_kubernetes_breach"``."""
    s = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return re.sub(r"_+", "_", s)


def _parent_technique(tid: str) -> str:
    """Collapse a sub-technique id to its parent by stripping the trailing
    ``.NNN`` component only.

    Correct for both Enterprise (``T1078.004`` -> ``T1078``) and ATLAS
    (``AML.T0051.001`` -> ``AML.T0051``) ids — a naive split on the first ``.``
    would conflate every ATLAS technique into a single ``AML`` node.
    """
    return re.sub(r"\.\d+$", "", tid) if tid else tid


def parse_flow_bundle(
    bundle: dict,
    flow_id: Union[str, None] = None,
    source: str = "attack_flow_corpus",
    tactic_id_to_name: Union[dict, None] = None,
) -> PerFlowExtract:
    """Convert a loaded STIX bundle dict into a :class:`PerFlowExtract`.

    ``tactic_id_to_name`` maps the action ``tactic_id`` (``TA####``) to a
    kill-chain phase name for the descriptive per-flow ``tactic`` field. The
    builder passes the map derived from the pinned ATT&CK bundle; standalone
    callers (hand-authored flows, tests) fall back to the ``schema.py`` classic
    table.
    """
    if tactic_id_to_name is None:
        tactic_id_to_name = TACTIC_ID_TO_NAME
    objects = bundle.get("objects", [])
    by_stix_id = {o["id"]: o for o in objects if "id" in o}

    flow_obj = next((o for o in objects if o.get("type") == "attack-flow"), {})
    flow_name = flow_obj.get("name", "") or "(unnamed flow)"

    # Detect the Attack Flow extension schema version (provenance), if declared.
    schema_version = "2.0.0"
    ext = by_stix_id.get(_AF_EXTENSION_ID)
    if ext and ext.get("version"):
        schema_version = str(ext["version"])

    # --- assign deterministic local ids (by kind, sorted by STIX uuid) -------
    local_id: dict[str, str] = {}
    nodes: list[FlowNode] = []
    for stix_type, (kind, prefix) in _KIND_BY_TYPE.items():
        members = sorted(
            (o for o in objects if o.get("type") == stix_type),
            key=lambda o: o["id"],
        )
        for i, obj in enumerate(members, start=1):
            lid = f"{prefix}{i}"
            local_id[obj["id"]] = lid
            nodes.append(_build_node(lid, kind, obj, tactic_id_to_name))

    # --- edges from typed ref lists (in-scope endpoints only) ---------------
    edges: list[FlowEdge] = []
    for obj in objects:
        src = local_id.get(obj.get("id"))
        if src is None:
            continue
        for ref_field, edge_type in _REF_FIELDS:
            for tgt_stix in obj.get(ref_field, []) or []:
                tgt = local_id.get(tgt_stix)
                if tgt is not None:
                    edges.append(FlowEdge(source=src, target=tgt, type=edge_type))
    edges.sort(key=lambda e: (e.source, e.target, e.type))

    start_refs = [
        local_id[r] for r in flow_obj.get("start_refs", []) if r in local_id
    ]

    return PerFlowExtract(
        flow_id=flow_id or slugify(flow_name),
        flow_name=flow_name,
        scope=flow_obj.get("scope", ""),
        source=source,
        schema_version=schema_version,
        references=_clean_references(flow_obj.get("external_references", [])),
        start_refs=start_refs,
        nodes=nodes,
        edges=edges,
    )


def _build_node(lid: str, kind: str, obj: dict, tactic_id_to_name: dict) -> FlowNode:
    if kind == "action":
        raw_tid = obj.get("technique_id")
        tactic_id = obj.get("tactic_id")
        return FlowNode(
            id=lid,
            kind="action",
            technique_id=_parent_technique(raw_tid) if raw_tid else None,
            sub_technique_id=raw_tid,
            name=obj.get("name"),
            tactic=tactic_id_to_name.get(tactic_id) if tactic_id else None,
            confidence=obj.get("confidence"),
        )
    if kind == "operator":
        return FlowNode(id=lid, kind="operator", operator=obj.get("operator"))
    return FlowNode(id=lid, kind="condition", description=obj.get("description"))


def _clean_references(refs: list[dict]) -> list[dict]:
    """Keep only the human-meaningful provenance keys from external_references."""
    out = []
    for r in refs:
        kept = {k: r[k] for k in ("source_name", "url", "description") if r.get(k)}
        if kept:
            out.append(kept)
    return out


def parse_flow_file(
    path: Union[str, Path],
    flow_id: Union[str, None] = None,
    source: str = "attack_flow_corpus",
    tactic_id_to_name: Union[dict, None] = None,
) -> PerFlowExtract:
    """Parse a STIX bundle on disk; default ``flow_id`` is the filename slug."""
    path = Path(path)
    with open(path) as f:
        bundle = json.load(f)
    return parse_flow_bundle(
        bundle,
        flow_id=flow_id or slugify(path.stem),
        source=source,
        tactic_id_to_name=tactic_id_to_name,
    )
