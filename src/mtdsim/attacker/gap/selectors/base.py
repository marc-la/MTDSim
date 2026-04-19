"""Subgraph selectors — shared types and helpers.

A ``Selector`` takes a ``GeneralisedAttackProfile`` and returns a
``SubgraphView`` describing a restricted node/edge set. Selectors are pure:
they do not mutate the GAP and perform no I/O. The view is agnostic to
which selector produced it, so payload serialisation stays selector-blind.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

import networkx as nx

from mtdsim.attacker.gap.schema import GeneralisedAttackProfile


@dataclass(frozen=True)
class SubgraphView:
    node_set: frozenset[str]
    edge_set: frozenset[tuple[str, str]]
    provenance: dict = field(default_factory=dict)


class Selector(Protocol):
    def select(self, gap: GeneralisedAttackProfile) -> SubgraphView: ...


def _build_digraph(gap: GeneralisedAttackProfile) -> nx.DiGraph:
    g = nx.DiGraph()
    for tid in gap.nodes:
        g.add_node(tid)
    for e in gap.edges:
        g.add_edge(e.source_id, e.target_id)
    return g


def ancestor_subgraph(
    gap: GeneralisedAttackProfile,
    target_nodes: list[str],
) -> tuple[set[str], set[tuple[str, str]]]:
    """Return (node_set, edge_set) of all ancestors of any target + the targets.

    Edge set is induced on the node set. Targets missing from the GAP are
    silently skipped so callers can pass unvalidated technique IDs.
    """
    g = _build_digraph(gap)
    nodes: set[str] = {t for t in target_nodes if t in g}
    for t in list(nodes):
        nodes.update(nx.ancestors(g, t))
    edges = {
        (e.source_id, e.target_id)
        for e in gap.edges
        if e.source_id in nodes and e.target_id in nodes
    }
    return nodes, edges
