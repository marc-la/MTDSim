"""Views over the lossless GAP — reduction without loss (§e).

None of these mutate the profile. Thresholding, acyclic projection, and tactic
layering are computed on demand, so the committed artefact stays lossless and
re-derivable across parameter choices (Decision 3). This is the honest
replacement for v0.4's build-time ``min_support`` / ``_break_cycles`` bakes.

All graph algorithms are stdlib (no ``networkx`` dependency) — the GAP package
is self-contained.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from mtdsim.l1_construction.schema import (
    DependencyEdge,
    GeneralisedAttackProfile,
)


@dataclass(frozen=True)
class GapView:
    """A non-mutating selection of edges + their induced technique nodes."""

    node_ids: tuple[str, ...]
    edges: tuple[DependencyEdge, ...]
    params: dict = field(default_factory=dict)


def _induced_nodes(edges) -> tuple[str, ...]:
    seen = set()
    for e in edges:
        seen.add(e.source_id)
        seen.add(e.target_id)
    return tuple(sorted(seen))


# ---------------------------------------------------------------------------
# Support filter — the honest replacement for min_support.
# ---------------------------------------------------------------------------


def support_filter(
    gap: GeneralisedAttackProfile, min_observation_count: int = 1
) -> GapView:
    """Edges observed in at least ``min_observation_count`` distinct flows."""
    kept = tuple(
        e for e in gap.edges if e.observation_count >= min_observation_count
    )
    return GapView(
        node_ids=_induced_nodes(kept),
        edges=kept,
        params={"min_observation_count": min_observation_count},
    )


# ---------------------------------------------------------------------------
# Acyclic projection — explicit, recorded cuts (never silent).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AcyclicView:
    node_ids: tuple[str, ...]
    edges: tuple[DependencyEdge, ...]        # kept (acyclic)
    cut_edges: tuple[DependencyEdge, ...]    # removed to break cycles, recorded
    policy: str


def _find_one_cycle(
    adj: dict[str, list[str]], nodes: list[str]
) -> list[tuple[str, str]] | None:
    """Return the edges of one directed cycle (DFS back-edge), or None."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {n: WHITE for n in nodes}
    parent: dict[str, str] = {}

    for root in nodes:
        if colour[root] != WHITE:
            continue
        stack = [(root, iter(adj.get(root, [])))]
        colour[root] = GREY
        while stack:
            node, it = stack[-1]
            advanced = False
            for nxt in it:
                if colour[nxt] == GREY:  # back edge -> reconstruct cycle
                    cyc = [(node, nxt)]
                    cur = node
                    while cur != nxt and cur in parent:
                        cyc.append((parent[cur], cur))
                        cur = parent[cur]
                    cyc.reverse()
                    return cyc
                if colour[nxt] == WHITE:
                    colour[nxt] = GREY
                    parent[nxt] = node
                    stack.append((nxt, iter(adj.get(nxt, []))))
                    advanced = True
                    break
            if not advanced:
                colour[node] = BLACK
                stack.pop()
    return None


def acyclic_projection(
    gap: GeneralisedAttackProfile, policy: str = "weakest_then_backward"
) -> AcyclicView:
    """A DAG view. Cuts the weakest edge on each cycle, recording every cut.

    Policy ``weakest_then_backward``: on each detected cycle, cut the edge with
    the lowest ``observation_count``; ties broken by preferring a ``backward``
    ``tactic_delta`` edge (a layer-regressing loop closure), then by
    ``(source_id, target_id)`` for determinism. The cut set is returned, never
    discarded — the profile itself is untouched.
    """
    edge_by_key = {e.key(): e for e in gap.edges}
    live = dict(edge_by_key)
    nodes = sorted({k[0] for k in live} | {k[1] for k in live})
    cut: list[DependencyEdge] = []

    def _rank(e: DependencyEdge):
        return (e.observation_count, e.tactic_delta != "backward", e.source_id, e.target_id)

    while True:
        adj: dict[str, list[str]] = {}
        for (s, t) in live:
            adj.setdefault(s, []).append(t)
        for v in adj.values():
            v.sort()
        cycle = _find_one_cycle(adj, nodes)
        if cycle is None:
            break
        weakest = min((live[e] for e in cycle if e in live), key=_rank)
        cut.append(weakest)
        del live[weakest.key()]

    kept = tuple(live[k] for k in sorted(live))
    return AcyclicView(
        node_ids=_induced_nodes(kept),
        edges=kept,
        cut_edges=tuple(cut),
        policy=policy,
    )


# ---------------------------------------------------------------------------
# Tactic layering — for layout.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TacticLayer:
    layer: int
    tactic: str
    technique_ids: tuple[str, ...]


def tactic_layering(gap: GeneralisedAttackProfile) -> list[TacticLayer]:
    """Group technique nodes by tactic layer, in kill-chain order.

    The layer -> tactic-name mapping is read back from the nodes' own
    ``primary_tactic`` (every node in a layer shares it), so the lane labels
    track whatever ATT&CK taxonomy built the GAP rather than a hardcoded table.
    ``tactic_delta`` on each edge already colours forward/back edges.
    """
    out = []
    for layer in sorted(gap.layers):
        tids = gap.layers[layer]
        name = next(
            (gap.nodes[t].primary_tactic for t in tids if t in gap.nodes and gap.nodes[t].primary_tactic),
            "(unmapped)",
        )
        out.append(TacticLayer(layer=layer, tactic=name, technique_ids=tuple(tids)))
    return out
