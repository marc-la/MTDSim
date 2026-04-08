"""
Phase 3: Supplementary edge sources.

- ``import_attack_flow_corpus``: Parse MITRE CTID Attack Flow ``.afb`` files
  and extract technique-to-technique sequencing edges. The ``.afb`` format
  is JSON: objects of ``id=="action"`` carry a ``technique_id`` property,
  and objects of ``id=="dynamic_line"`` connect action anchors.

- ``extract_ontology_edges``: Simplified DeepOP-style keyword extraction
  over STIX technique descriptions.
"""

from __future__ import annotations

import json
import os
import re
from typing import Iterable

from mtdsim.attacker.gap.schema import (
    DependencyEdge,
    Evidence,
    TechniqueNode,
)


# ---------------------------------------------------------------------------
# Attack Flow .afb corpus import
# ---------------------------------------------------------------------------


def _parse_afb(path: str, latch_max_distance: float = 400.0) -> list[tuple[str, str]]:
    """
    Return a list of (source_tid, target_tid) edges from a single .afb file.

    The Attack Flow Builder save format wires ``dynamic_line`` connectors
    between ``generic_latch`` objects rather than directly to action
    anchors. Latches are not back-referenced from anchors, so we resolve
    each latch to its owning action by spatial proximity in the embedded
    ``layout`` map (shortest Euclidean distance, capped at
    ``latch_max_distance``).

    Sub-technique IDs collapse to parent (T1059.001 -> T1059).
    """
    with open(path) as f:
        data = json.load(f)
    objects = data.get("objects", [])
    layout = data.get("layout") or {}

    # Collect actions with positions and technique IDs
    action_positions: list[tuple[str, float, float]] = []  # (instance, x, y)
    action_to_tid: dict[str, str] = {}
    for obj in objects:
        if obj.get("id") != "action":
            continue
        inst = obj.get("instance")
        if not inst:
            continue
        for p in obj.get("properties", []):
            if isinstance(p, list) and len(p) >= 2 and p[0] == "technique_id":
                tid = (p[1] or "").strip()
                if tid:
                    action_to_tid[inst] = tid.split(".", 1)[0]
                break
        pos = layout.get(inst)
        if pos and len(pos) >= 2 and inst in action_to_tid:
            action_positions.append((inst, float(pos[0]), float(pos[1])))

    # Resolve each latch to its closest action within distance threshold
    latch_to_action: dict[str, str] = {}
    for obj in objects:
        if obj.get("id") != "generic_latch":
            continue
        inst = obj.get("instance")
        pos = layout.get(inst) if inst else None
        if not pos or len(pos) < 2:
            continue
        lx, ly = float(pos[0]), float(pos[1])
        best_inst = None
        best_d2 = latch_max_distance ** 2
        for ainst, ax, ay in action_positions:
            d2 = (ax - lx) ** 2 + (ay - ly) ** 2
            if d2 < best_d2:
                best_d2 = d2
                best_inst = ainst
        if best_inst:
            latch_to_action[inst] = best_inst

    edges: list[tuple[str, str]] = []
    for obj in objects:
        if obj.get("id") != "dynamic_line":
            continue
        src_action = latch_to_action.get(obj.get("source"))
        tgt_action = latch_to_action.get(obj.get("target"))
        if not src_action or not tgt_action or src_action == tgt_action:
            continue
        src_tid = action_to_tid.get(src_action)
        tgt_tid = action_to_tid.get(tgt_action)
        if src_tid and tgt_tid and src_tid != tgt_tid:
            edges.append((src_tid, tgt_tid))
    return edges


def import_attack_flow_corpus(
    corpus_dir: str,
    nodes: dict[str, TechniqueNode],
) -> list[DependencyEdge]:
    """
    Walk a directory of Attack Flow ``.afb`` files and return dependency
    edges for every technique-to-technique transition.

    Edges are confidence=1.0 (curated). Sub-techniques collapse to parent,
    so self-loops at the parent level are dropped.
    """
    if not os.path.isdir(corpus_dir):
        return []

    # (src, tgt) -> list of flow names contributing this edge
    pair_sources: dict[tuple[str, str], list[str]] = {}
    for name in sorted(os.listdir(corpus_dir)):
        if not name.endswith(".afb"):
            continue
        path = os.path.join(corpus_dir, name)
        try:
            pairs = _parse_afb(path)
        except Exception:
            continue
        flow_name = os.path.splitext(name)[0]
        for src, tgt in pairs:
            if src in nodes and tgt in nodes:
                pair_sources.setdefault((src, tgt), []).append(flow_name)

    edges: list[DependencyEdge] = []
    for (src, tgt), flows in pair_sources.items():
        layer_src = nodes[src].tactic_layer
        layer_tgt = nodes[tgt].tactic_layer
        is_backward = layer_tgt <= layer_src
        edges.append(
            DependencyEdge(
                source_id=src,
                target_id=tgt,
                evidence_type="attack_flow",
                confidence=1.0,
                evidence=[
                    Evidence(
                        source_type="attack_flow",
                        source_url="https://center-for-threat-informed-defense.github.io/attack-flow/",
                        description=f"Observed in {len(flows)} Attack Flow(s): {', '.join(flows[:3])}"
                        + ("..." if len(flows) > 3 else ""),
                        campaigns=flows,
                    )
                ],
                source_count=1,
                is_backward=is_backward,
            )
        )
    return edges


# ---------------------------------------------------------------------------
# Ontology extraction from STIX descriptions
# ---------------------------------------------------------------------------

_TID_PATTERN = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")

_PRECONDITION_PHRASES = [
    "requires", "after", "following", "depends on",
    "using credentials obtained", "with access to",
    "once", "having obtained", "leveraging", "relies on",
]


def extract_ontology_edges(
    nodes: dict[str, TechniqueNode],
) -> list[DependencyEdge]:
    """
    Scan STIX technique descriptions for precondition language referencing
    another technique ID. Low yield (20-40 edges expected), but each edge
    is documentation-backed.

    A sentence containing a precondition keyword and another T#### ID
    generates a directed edge from the referenced technique to the current
    one (the referenced technique is the precondition).
    """
    edges: list[DependencyEdge] = []
    seen: set[tuple[str, str]] = set()

    for tid, node in nodes.items():
        desc = (node.description or "").lower()
        if not desc:
            continue
        # Split on sentence boundaries
        for sentence in re.split(r"(?<=[.!?])\s+", desc):
            if not any(kw in sentence for kw in _PRECONDITION_PHRASES):
                continue
            for match in _TID_PATTERN.findall(sentence.upper()):
                parent = match.split(".", 1)[0]
                if parent == tid or parent not in nodes:
                    continue
                key = (parent, tid)
                if key in seen:
                    continue
                seen.add(key)
                layer_src = nodes[parent].tactic_layer
                layer_tgt = nodes[tid].tactic_layer
                edges.append(
                    DependencyEdge(
                        source_id=parent,
                        target_id=tid,
                        evidence_type="ontology",
                        confidence=0.8,
                        evidence=[
                            Evidence(
                                source_type="ontology",
                                source_url=f"https://attack.mitre.org/techniques/{tid}/",
                                description=f"Precondition language in {tid} description: '{sentence.strip()[:120]}'",
                            )
                        ],
                        source_count=1,
                        is_backward=layer_tgt <= layer_src,
                    )
                )
    return edges
