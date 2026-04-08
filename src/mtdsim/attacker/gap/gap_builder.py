"""
Phases 4-5: Combine edge sources, validate, and compute quality metrics.

``build_gap`` is the top-level entry point used by the notebook.
"""

from __future__ import annotations

import datetime as _dt
from typing import Iterable, Optional

import networkx as nx

from mtdsim.attacker.gap.schema import (
    DependencyEdge,
    GeneralisedAttackProfile,
    TechniqueNode,
)
from mtdsim.attacker.gap.stix_parser import parse_stix_bundle
from mtdsim.attacker.gap.cooccurrence_miner import (
    build_usage_matrix,
    mine_cooccurrence_edges,
)
from mtdsim.attacker.gap.edge_importer import (
    extract_ontology_edges,
    import_attack_flow_corpus,
)


def _merge_edges(edge_groups: list[list[DependencyEdge]]) -> list[DependencyEdge]:
    """
    Combine edges from multiple sources, merging duplicates by (source, target).

    Merged edges have ``source_count`` == number of distinct evidence source
    types and ``confidence`` == max(confidence) across contributors.
    """
    merged: dict[tuple[str, str], DependencyEdge] = {}
    for group in edge_groups:
        for edge in group:
            key = edge.key()
            if key not in merged:
                merged[key] = DependencyEdge(
                    source_id=edge.source_id,
                    target_id=edge.target_id,
                    evidence_type=edge.evidence_type,
                    confidence=edge.confidence,
                    support=edge.support,
                    lift=edge.lift,
                    evidence=list(edge.evidence),
                    source_count=1,
                    is_backward=edge.is_backward,
                )
            else:
                existing = merged[key]
                existing.evidence.extend(edge.evidence)
                existing.confidence = max(existing.confidence, edge.confidence)
                # Prefer statistical metadata if the new edge has it
                if existing.support is None and edge.support is not None:
                    existing.support = edge.support
                if existing.lift is None and edge.lift is not None:
                    existing.lift = edge.lift
                types_seen = {ev.source_type for ev in existing.evidence}
                existing.source_count = len(types_seen)

    return list(merged.values())


def _break_cycles(
    nodes: dict[str, TechniqueNode],
    edges: list[DependencyEdge],
) -> list[DependencyEdge]:
    """
    Remove the weakest-evidence backward edge on any cycle until the graph
    is acyclic. (Forward edges are never removed; backward edges encode
    loops such as Lateral Movement -> Discovery -> Lateral Movement.)
    """
    g = nx.DiGraph()
    for tid in nodes:
        g.add_node(tid)
    edge_by_key = {e.key(): e for e in edges}
    for e in edges:
        g.add_edge(e.source_id, e.target_id)

    kept_keys = set(edge_by_key.keys())

    while True:
        try:
            cycle = nx.find_cycle(g, orientation="original")
        except nx.NetworkXNoCycle:
            break
        # Pick the backward edge with lowest (source_count, confidence) on the cycle
        candidates = []
        for u, v, _ in cycle:
            e = edge_by_key.get((u, v))
            if e and e.is_backward:
                candidates.append(e)
        if not candidates:
            # No backward edge -> drop the lowest-confidence forward edge on the cycle
            candidates = [edge_by_key[(u, v)] for u, v, _ in cycle if (u, v) in edge_by_key]
        if not candidates:
            break
        weakest = min(candidates, key=lambda e: (e.source_count, e.confidence))
        g.remove_edge(weakest.source_id, weakest.target_id)
        kept_keys.discard(weakest.key())

    return [edge_by_key[k] for k in kept_keys]


def build_gap(
    stix_bundle_path: str,
    attack_flow_corpus_dir: Optional[str] = None,
    min_support: float = 0.1,
    min_confidence: float = 0.6,
    include_ontology: bool = True,
    break_cycles: bool = True,
    technique_source: str = "enterprise-attack",
    version: str = "0.3",
) -> tuple[GeneralisedAttackProfile, dict]:
    """
    Run the full GAP construction pipeline.

    Returns the GAP and an ``extras`` dict with diagnostic data
    (intra-tactic pairs, co-occurrence meta, raw usage matrix shape).
    """
    # Phase 1
    nodes, index = parse_stix_bundle(stix_bundle_path)

    # Phase 2
    matrix = build_usage_matrix(nodes, index)
    co_edges, intra_tactic, co_meta = mine_cooccurrence_edges(
        matrix, nodes,
        min_support=min_support,
        min_confidence=min_confidence,
    )

    # Phase 3
    edge_groups = [co_edges]
    if attack_flow_corpus_dir:
        edge_groups.append(import_attack_flow_corpus(attack_flow_corpus_dir, nodes))
    if include_ontology:
        edge_groups.append(extract_ontology_edges(nodes))

    edges = _merge_edges(edge_groups)

    # Phase 5 validation
    if break_cycles:
        edges = _break_cycles(nodes, edges)

    # Compute quality metrics
    incoming: dict[str, int] = {tid: 0 for tid in nodes}
    outgoing: dict[str, int] = {tid: 0 for tid in nodes}
    for e in edges:
        outgoing[e.source_id] = outgoing.get(e.source_id, 0) + 1
        incoming[e.target_id] = incoming.get(e.target_id, 0) + 1

    entry_nodes = [tid for tid in nodes if incoming.get(tid, 0) == 0 and outgoing.get(tid, 0) > 0]
    objective_nodes = [tid for tid in nodes if outgoing.get(tid, 0) == 0 and incoming.get(tid, 0) > 0]

    layers: dict[int, list[str]] = {}
    for tid, node in nodes.items():
        layers.setdefault(node.tactic_layer, []).append(tid)

    techniques_with_edges = sum(
        1 for tid in nodes if incoming.get(tid, 0) or outgoing.get(tid, 0)
    )
    orphans = len(nodes) - techniques_with_edges
    consensus = sum(1 for e in edges if e.source_count >= 2)
    backward = sum(1 for e in edges if e.is_backward)

    gap = GeneralisedAttackProfile(
        version=version,
        build_date=_dt.date.today().isoformat(),
        technique_source=technique_source,
        nodes=nodes,
        edges=edges,
        entry_nodes=entry_nodes,
        objective_nodes=objective_nodes,
        layers=layers,
        total_techniques=len(nodes),
        techniques_with_edges=techniques_with_edges,
        orphan_techniques=orphans,
        edge_count=len(edges),
        consensus_edge_count=consensus,
        intra_tactic_unresolved=len(intra_tactic),
        backward_edge_count=backward,
        min_support=min_support,
        min_confidence=min_confidence,
        confidence_threshold=co_meta["confidence_threshold"],
    )

    extras = {
        "intra_tactic_pairs": intra_tactic,
        "cooccurrence_meta": co_meta,
        "usage_matrix_shape": matrix.shape,
    }
    return gap, extras
