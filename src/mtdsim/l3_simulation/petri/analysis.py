"""Structural analyses over the single-token tactic-place nets (the MVP payoff).

No weights are needed for any of this — it is all reachability/connectivity of
the single black token over the place graph:

- reachable tactic-set from the entry marking (and from *any* entry tactic);
- is the class objective tactic reachable? (class-semantic objective per the
  handoff: exfiltration / impact / impact+exfiltration / command-and-control);
- deadlock / sink tactics (places with no outgoing transition);
- shortest and longest entry -> objective tactic paths;
- the recon -> initial-access **prefix-gap probe** — the deduction the next
  decision rests on (handoff / feasibility study sec.4).

Reachability of one black token reduces to graph reachability over the places,
so the analyses use a plain BFS over the place graph derived from the
transitions. A SNAKES ``StateGraph`` cross-check (``reachable_marking_count``)
confirms the net agrees with the BFS at the marking level.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from snakes.nets import StateGraph

from mtdsim.l2_subgraph.schema import SubgraphView
from mtdsim.l3_simulation.petri.build import GapIndex, StructuralNet

# Class-semantic objective tactic(s). The operational objective of each GASP
# class, per the handoff "Step 4" and the feasibility study sec.4:
# - pure_steal           -> exfiltration (steal the data);
# - pure_impediment      -> impact (disrupt/destroy);
# - double_extortion     -> exfiltration AND impact (steal then encrypt);
# - infrastructure_setup -> command-and-control (no impact/exfiltration exists;
#   its absorbing condition is C2-established, a foothold, not an attacker goal
#   in the impact sense -- feasibility study sec.4 / F3).
# This is distinct from the broad node-level ``is_objective`` flag (reported
# separately as ``objective_tactics_data`` for transparency).
# The aggregate (null) profile has no single operational objective; its
# declared objective set is the union of the four class-semantic objectives
# (a recorded choice — the timeline-runner handoff requires the aggregate's
# objective set to be declared, and union is the null-envelope reading).
OBJECTIVE_TACTICS: dict[str, tuple[str, ...]] = {
    "pure_steal": ("exfiltration",),
    "pure_impediment": ("impact",),
    "double_extortion": ("exfiltration", "impact"),
    "infrastructure_setup": ("command-and-control",),
    "aggregate": ("command-and-control", "exfiltration", "impact"),
}

RECONNAISSANCE = "reconnaissance"
INITIAL_ACCESS = "initial-access"


@dataclass
class PathResult:
    """An entry -> objective path over the place graph, or ``None`` fields when
    no such path exists. ``n_places`` counts tactics on the path; ``n_hops`` =
    ``n_places - 1`` is the number of transitions fired."""

    reachable: bool
    n_places: int | None = None
    n_hops: int | None = None
    path: tuple[str, ...] | None = None
    entry: str | None = None
    objective: str | None = None


@dataclass
class PrefixGapProbe:
    """The recon -> initial-access connectivity probe (handoff Step 4).

    ``direct_edges`` are the GASP technique-edges from a reconnaissance
    technique straight to an initial-access technique; ``recon_reaches_ia`` is
    whether the recon place can reach the initial-access place at all over the
    net. Expected on the observed-only base: near-disconnected (feasibility
    study sec.4)."""

    reconnaissance_present: bool
    initial_access_present: bool
    direct_edges: tuple[tuple[str, str], ...]
    recon_reaches_initial_access: bool
    interpretation: str


@dataclass
class StructuralReport:
    class_name: str
    entry_tactic: str
    n_places: int
    n_transitions: int
    n_inter_tactic_edges: int
    n_intra_tactic_selfloops_dropped: int
    objective_tactics: tuple[str, ...]
    objective_tactics_data: tuple[str, ...]
    reachable_from_entry_marking: tuple[str, ...]
    objective_reachable_from_entry: dict[str, bool]
    any_objective_reachable_from_entry: bool
    all_objectives_reachable_from_entry: bool
    reachable_from_any_entry: tuple[str, ...]
    entry_tactics: tuple[str, ...]
    sink_tactics: tuple[str, ...]
    shortest_entry_to_objective: PathResult
    longest_entry_to_objective: PathResult
    prefix_gap: PrefixGapProbe
    reachable_marking_count: int  # SNAKES StateGraph cross-check

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def analyse(
    snet: StructuralNet, view: SubgraphView, gap: GapIndex
) -> StructuralReport:
    """Compute the full structural report for one built class net."""
    tactics = snet.tactics
    tactic_set = set(tactics)
    adj = _place_adjacency(snet)

    entry_tactics = tuple(
        sorted(
            {
                gap.tactic_of[t]
                for t in view.node_set
                if t in gap.entry_techniques
            }
        )
    )
    objective_tactics = OBJECTIVE_TACTICS[snet.class_name]
    missing = [o for o in objective_tactics if o not in tactic_set]
    if missing:
        raise ValueError(
            f"{snet.class_name}: declared objective tactic(s) {missing} are not "
            f"places in the class -- OBJECTIVE_TACTICS has drifted from the data"
        )
    objective_tactics_data = tuple(
        sorted(
            {
                gap.tactic_of[t]
                for t in view.node_set
                if t in gap.objective_techniques
            }
        )
    )

    reach_marking = _bfs(adj, [snet.entry_tactic])
    reach_any_entry = _bfs(adj, entry_tactics)
    obj_reach = {o: (o in reach_marking) for o in objective_tactics}

    sinks = tuple(t for t in tactics if not adj.get(t))

    shortest = _shortest_path(adj, entry_tactics, objective_tactics)
    longest = _longest_simple_path(tactics, adj, entry_tactics, objective_tactics)

    prefix_gap = _prefix_gap_probe(snet, adj)

    return StructuralReport(
        class_name=snet.class_name,
        entry_tactic=snet.entry_tactic,
        n_places=len(tactics),
        n_transitions=len(snet.transitions),
        n_inter_tactic_edges=sum(len(t.edges) for t in snet.transitions),
        n_intra_tactic_selfloops_dropped=snet.selfloops_dropped,
        objective_tactics=objective_tactics,
        objective_tactics_data=objective_tactics_data,
        reachable_from_entry_marking=tuple(sorted(reach_marking)),
        objective_reachable_from_entry=obj_reach,
        any_objective_reachable_from_entry=any(obj_reach.values()),
        all_objectives_reachable_from_entry=all(obj_reach.values()),
        reachable_from_any_entry=tuple(sorted(reach_any_entry)),
        entry_tactics=entry_tactics,
        sink_tactics=sinks,
        shortest_entry_to_objective=shortest,
        longest_entry_to_objective=longest,
        prefix_gap=prefix_gap,
        reachable_marking_count=_reachable_marking_count(snet),
    )


# ---------------------------------------------------------------------------
# Place graph + reachability
# ---------------------------------------------------------------------------


def _place_adjacency(snet: StructuralNet) -> dict[str, set[str]]:
    """``src_tactic -> {dst_tactic}`` over the transitions (the place graph).

    Unions the observed transitions with the synthetic overlay
    (``synthetic_transitions`` — empty on an observed-only build), so a
    composed net's reachability reports the bridged truth."""
    adj: dict[str, set[str]] = {t: set() for t in snet.tactics}
    for spec in snet.transitions + snet.synthetic_transitions:
        adj[spec.src_tactic].add(spec.dst_tactic)
    return adj


def _bfs(adj: dict[str, set[str]], starts) -> set[str]:
    seen = set(starts)
    stack = list(starts)
    while stack:
        u = stack.pop()
        for v in sorted(adj.get(u, ())):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def _shortest_path(
    adj: dict[str, set[str]], starts, targets
) -> PathResult:
    """Shortest place-path from any entry tactic to any objective tactic.

    Multi-source BFS; deterministic via sorted neighbour expansion and a
    sorted seeding of the frontier. ``starts`` may include a target (a tactic
    that is both entry and objective) -> a zero-hop path."""
    target_set = set(targets)
    # Each frontier entry: (node, path-so-far). Sorted seeding + sorted
    # expansion make the first-found shortest path deterministic.
    from collections import deque

    frontier = deque((s, (s,)) for s in sorted(starts))
    seen = set(sorted(starts))
    while frontier:
        node, path = frontier.popleft()
        if node in target_set:
            return PathResult(
                reachable=True,
                n_places=len(path),
                n_hops=len(path) - 1,
                path=path,
                entry=path[0],
                objective=node,
            )
        for nxt in sorted(adj.get(node, ())):
            if nxt not in seen:
                seen.add(nxt)
                frontier.append((nxt, path + (nxt,)))
    return PathResult(reachable=False)


def _longest_simple_path(
    tactics: tuple[str, ...], adj: dict[str, set[str]], starts, targets
) -> PathResult:
    """Longest *simple* (no repeated tactic) entry -> objective path.

    Exact via bitmask dynamic programming over the <=15 places: ``reach[mask]``
    is a bitmask of the end-nodes for which some simple path visiting exactly
    ``mask`` ends there. Cycles in the place graph make an unconstrained longest
    path ill-defined, so the "no repeated tactic" constraint is what makes the
    quantity well-posed. Deterministic: lowest mask number, then lowest index,
    breaks ties on reconstruction."""
    n = len(tactics)
    idx = {t: i for i, t in enumerate(tactics)}
    adj_mask = [0] * n
    for u, vs in adj.items():
        for v in vs:
            adj_mask[idx[u]] |= 1 << idx[v]
    start_idx = [idx[s] for s in starts]
    target_mask = 0
    for t in targets:
        target_mask |= 1 << idx[t]

    reach = [0] * (1 << n)
    for s in start_idx:
        reach[1 << s] |= 1 << s

    best_mask = best_end = -1
    best_pc = 0
    for mask in range(1 << n):
        ends = reach[mask]
        if not ends:
            continue
        e = ends
        while e:
            low = e & -e
            end = low.bit_length() - 1
            e ^= low
            if (1 << end) & target_mask:
                pc = bin(mask).count("1")
                if pc > best_pc:
                    best_pc, best_mask, best_end = pc, mask, end
            nxt = adj_mask[end] & ~mask
            w = nxt
            while w:
                lb = w & -w
                w ^= lb
                reach[mask | lb] |= lb

    if best_mask < 0:
        return PathResult(reachable=False)

    path_idx = _reconstruct_longest(best_mask, best_end, adj_mask, reach)
    path = tuple(tactics[i] for i in path_idx)
    return PathResult(
        reachable=True,
        n_places=len(path),
        n_hops=len(path) - 1,
        path=path,
        entry=path[0],
        objective=path[-1],
    )


def _reconstruct_longest(mask, end, adj_mask, reach) -> list[int]:
    """Walk a witnessing longest path back to its start (lowest-index
    predecessor at each step -> deterministic)."""
    path = [end]
    cur_mask, cur = mask, end
    while bin(cur_mask).count("1") > 1:
        prev_mask = cur_mask ^ (1 << cur)
        cand = prev_mask
        chosen = -1
        while cand:
            lb = cand & -cand
            cand ^= lb
            p = lb.bit_length() - 1
            if (adj_mask[p] & (1 << cur)) and (reach[prev_mask] & (1 << p)):
                chosen = p
                break
        if chosen < 0:  # unreachable in theory; guards against silent loop
            break
        path.append(chosen)
        cur_mask, cur = prev_mask, chosen
    path.reverse()
    return path


def _prefix_gap_probe(
    snet: StructuralNet, adj: dict[str, set[str]]
) -> PrefixGapProbe:
    """Surface whether reconnaissance reaches initial-access (handoff Step 4)."""
    tactic_set = set(snet.tactics)
    recon_present = RECONNAISSANCE in tactic_set
    ia_present = INITIAL_ACCESS in tactic_set

    direct_edges: tuple[tuple[str, str], ...] = ()
    for spec in snet.transitions:
        if spec.src_tactic == RECONNAISSANCE and spec.dst_tactic == INITIAL_ACCESS:
            direct_edges = spec.edges
            break
    # ``direct_edges`` stays observed-only (GASP provenance). The synthetic
    # overlay bridges recon -> initial-access via its pre-intrusion chain
    # (recon -> resource-development -> initial-access): the bridge is the
    # overlay's when observed-only cannot reach IA but the composed net can.
    observed_adj: dict[str, set[str]] = {t: set() for t in snet.tactics}
    for spec in snet.transitions:
        observed_adj[spec.src_tactic].add(spec.dst_tactic)
    observed_reaches = INITIAL_ACCESS in _bfs(observed_adj, [RECONNAISSANCE])
    synthetic_bridge = bool(snet.synthetic_transitions) and not observed_reaches

    recon_reaches_ia = (
        recon_present
        and ia_present
        and INITIAL_ACCESS in _bfs(adj, [RECONNAISSANCE])
    )

    if not (recon_present and ia_present):
        interpretation = "reconnaissance or initial-access absent from this class"
    elif not recon_reaches_ia:
        interpretation = (
            "DISCONNECTED -- reconnaissance cannot reach initial-access; the "
            "recon place is an island (the observed-only prefix gap)"
        )
    elif synthetic_bridge:
        interpretation = (
            "BRIDGED synthetically -- the synthetic overlay supplies the "
            "pre-intrusion chain reconnaissance -> resource-development -> "
            "initial-access (declared routing share, no flow backing; "
            "synthetic_overlay.py)"
        )
    elif direct_edges:
        interpretation = (
            f"BRIDGED by {len(direct_edges)} direct recon->initial-access "
            f"edge(s) {list(direct_edges)} -- a thin, fragile prefix link"
        )
    else:
        interpretation = (
            "reconnaissance reaches initial-access only indirectly (no direct "
            "recon->initial-access edge)"
        )
    return PrefixGapProbe(
        reconnaissance_present=recon_present,
        initial_access_present=ia_present,
        direct_edges=direct_edges,
        recon_reaches_initial_access=recon_reaches_ia,
        interpretation=interpretation,
    )


def _reachable_marking_count(snet: StructuralNet) -> int:
    """Number of reachable markings of the single-token net, via SNAKES
    ``StateGraph`` -- a cross-check that the formal net agrees with the BFS
    (with one token, #reachable markings == #reachable places from the seed)."""
    sg = StateGraph(snet.net)
    sg.build()
    return len(list(sg))


__all__ = [
    "OBJECTIVE_TACTICS",
    "PathResult",
    "PrefixGapProbe",
    "StructuralReport",
    "analyse",
]
