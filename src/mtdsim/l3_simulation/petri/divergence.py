"""Divergence-from-aggregate report (absorbs the Tier-0 structural probe).

Measures whether the four weighted class nets differ from the aggregate
(null) profile beyond chance — the *structural* half of the "do the four
profiles differ" verification (the behavioural half is the timeline runner's).

Three instruments, all on the W-A weight layer
(:mod:`mtdsim.l3_simulation.petri.weights`):

- **Per-place out-distribution Jensen-Shannon divergence** between each class
  net and the aggregate net, on the primary (operator-deduplicated, n = 29)
  corpus; the raw (n = 38) corpus is the robustness column. Convention matches
  the L2 gate: ``scipy jensenshannon(p, q, base=2) ** 2`` (divergence in
  [0, 1]). A place is *comparable* when both nets have a flow-backed
  out-distribution there; the class summary is the unweighted mean over its
  comparable places.
- **Weighted structural discriminators** per net, computed on the
  positive-weight support (transitions whose primary weight > 0 — the
  transitions a weighted traversal can actually take): reachable sets,
  entry -> objective chains, branching factor, distinct-path count, sinks and
  islands. Zero-weight structural transitions are *retained in the nets* (no
  synthesis, no deletion); they are only excluded from these traversal-facing
  statistics.
- **Shuffled-class-label null.** Flows are reassigned to the four classes at
  random (class sizes preserved, on the deduplicated corpus), the tactic-pair
  quotient is rebuilt per shuffled class, and the mean per-place JSD against
  the (fixed) aggregate is recomputed. The observed class divergence is judged
  against the p95 of its class-size-matched null band. Seeded and
  deterministic.

Framing (hard constraints carried from ``metrics_semantics.md`` §(f)):
weights are workflow-recurrence over a survivorship-biased corpus — each
class net is a behavioural **envelope** for an operational objective, never
an actor's policy, never step efficacy. And the accepted tradeoff to record,
not fix: aggregating techniques -> tactics is what makes the weights
groundable at this corpus size, and it **loses AND-gate/join structure** —
the accepted mechanism, not a defect.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from scipy.spatial.distance import jensenshannon

from mtdsim.l3_simulation.petri.analysis import (
    OBJECTIVE_TACTICS,
    PathResult,
    StructuralReport,
    _bfs,
    _longest_simple_path,
    _shortest_path,
)
from mtdsim.l3_simulation.petri.build import (
    AGGREGATE,
    CLASS_NAMES,
    GapIndex,
    StructuralNet,
)
from mtdsim.l3_simulation.petri.weights import (
    PRIMARY_VARIANT,
    TransitionWeights,
)

# Shuffled-label null parameters — fixed so the report is deterministic.
NULL_TRIALS = 200
NULL_SEED = 20260703


# ---------------------------------------------------------------------------
# Out-distributions and JSD
# ---------------------------------------------------------------------------


def out_distributions(
    snet: StructuralNet, tw: dict[str, TransitionWeights]
) -> dict[str, dict[str, float]]:
    """``place -> {dst_tactic: weight}`` for places with a defined (flow-
    backed) out-distribution under this weight layer."""
    dists: dict[str, dict[str, float]] = {}
    for spec in snet.transitions:
        w = tw[spec.name].weight
        if w is None:
            continue
        dists.setdefault(spec.src_tactic, {})[spec.dst_tactic] = w
    return dists


def _jsd(p_dist: dict[str, float], q_dist: dict[str, float]) -> float:
    """JSD (base 2, in [0, 1]) between two out-distributions over the union
    of their supports — the L2 convention (``jensenshannon ** 2``)."""
    support = sorted(set(p_dist) | set(q_dist))
    p = np.array([p_dist.get(t, 0.0) for t in support])
    q = np.array([q_dist.get(t, 0.0) for t in support])
    return float(jensenshannon(p, q, base=2) ** 2)


def per_place_jsd(
    class_dists: dict[str, dict[str, float]],
    agg_dists: dict[str, dict[str, float]],
) -> dict[str, float]:
    """JSD per comparable place (defined out-distribution in both nets)."""
    return {
        place: _jsd(class_dists[place], agg_dists[place])
        for place in sorted(set(class_dists) & set(agg_dists))
    }


# ---------------------------------------------------------------------------
# Shuffled-class-label null
# ---------------------------------------------------------------------------


def quotient_out_dists(
    edge_flows: dict[tuple[str, str], frozenset[str]],
    tactic_of: dict[str, str],
    flows: frozenset[str] | set[str],
) -> dict[str, dict[str, float]]:
    """The tactic-pair flow quotient for an arbitrary flow set: out-edge-
    normalised W-A distributions, computed straight from the GAP edges.

    For a *class* flow set this equals the class net's weighted
    out-distributions: every edge a class flow draws has both endpoints in the
    class node set (surface construction), and zero-backed structural
    transitions carry zero probability either way. This is what lets the
    shuffled-label null rebuild distributions without rebuilding nets.
    """
    pair_flows: dict[tuple[str, str], set[str]] = {}
    for (u, v), efs in edge_flows.items():
        f = efs & flows
        if not f:
            continue
        a, b = tactic_of[u], tactic_of[v]
        if a == b:
            continue  # self-loops dropped, as at structural build time
        pair_flows.setdefault((a, b), set()).update(f)

    by_place: dict[str, dict[str, int]] = {}
    for (a, b), f in pair_flows.items():
        by_place.setdefault(a, {})[b] = len(f)
    return {
        place: {b: n / den for b, n in dsts.items()}
        for place, dsts in by_place.items()
        if (den := sum(dsts.values()))
    }


def shuffled_label_null(
    edge_flows: dict[tuple[str, str], frozenset[str]],
    tactic_of: dict[str, str],
    class_flows: dict[str, frozenset[str]],
    agg_dists: dict[str, dict[str, float]],
    n_trials: int = NULL_TRIALS,
    seed: int = NULL_SEED,
) -> dict[str, dict[str, float]]:
    """Per class label: the null band of mean per-place JSD vs the aggregate.

    Each trial reassigns the pooled flows to the four labels at random with
    class sizes preserved, rebuilds each label's quotient distributions, and
    records its mean JSD against the (fixed) aggregate distributions.
    Returns ``{class: {p50, p95, max}}`` over ``n_trials`` trials.
    """
    rng = random.Random(seed)
    pooled = sorted(frozenset().union(*class_flows.values()))
    sizes = [(cls, len(class_flows[cls])) for cls in CLASS_NAMES]

    samples: dict[str, list[float]] = {cls: [] for cls in CLASS_NAMES}
    for _ in range(n_trials):
        shuffled = pooled[:]
        rng.shuffle(shuffled)
        cursor = 0
        for cls, size in sizes:
            trial_flows = frozenset(shuffled[cursor : cursor + size])
            cursor += size
            dists = quotient_out_dists(edge_flows, tactic_of, trial_flows)
            jsds = per_place_jsd(dists, agg_dists)
            samples[cls].append(
                float(np.mean(list(jsds.values()))) if jsds else 0.0
            )
    return {
        cls: {
            "p50": float(np.percentile(vals, 50)),
            "p95": float(np.percentile(vals, 95)),
            "max": float(np.max(vals)),
        }
        for cls, vals in samples.items()
    }


# ---------------------------------------------------------------------------
# Weighted structural discriminators (positive-weight support)
# ---------------------------------------------------------------------------


@dataclass
class WeightedDiscriminators:
    """Traversal-facing statistics of one net on its positive-weight support
    (primary corpus variant)."""

    profile: str
    n_transitions: int
    n_supported_transitions: int  # weight > 0
    n_zero_weight_transitions: int  # retained structure a weighted walk never takes
    reachable_from_recon_seed: tuple[str, ...]
    reachable_from_initial_access: tuple[str, ...]
    objective_reachable_from_initial_access: dict[str, bool]
    shortest_entry_to_objective: PathResult
    longest_entry_to_objective: PathResult
    branching_factor: float  # mean positive out-degree over branching places
    distinct_entry_to_objective_paths: int  # simple paths, exact (bitmask DP)
    sink_places: tuple[str, ...]  # no positive-weight out-transition
    island_places: tuple[str, ...]  # no positive-weight in or out

    def to_dict(self) -> dict[str, Any]:
        from dataclasses import asdict

        return asdict(self)


def _supported_adjacency(
    snet: StructuralNet, tw: dict[str, TransitionWeights]
) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {t: set() for t in snet.tactics}
    for spec in snet.transitions:
        w = tw[spec.name].weight
        if w:
            adj[spec.src_tactic].add(spec.dst_tactic)
    return adj


def _count_simple_paths(
    tactics: tuple[str, ...],
    adj: dict[str, set[str]],
    starts,
    targets,
) -> int:
    """Exact count of distinct simple entry -> objective paths (bitmask DP
    over the <=15 places). A tactic that is both entry and objective counts
    its zero-hop path."""
    n = len(tactics)
    idx = {t: i for i, t in enumerate(tactics)}
    adj_mask = [0] * n
    for u, vs in adj.items():
        for v in vs:
            adj_mask[idx[u]] |= 1 << idx[v]
    target_mask = 0
    for t in targets:
        if t in idx:
            target_mask |= 1 << idx[t]

    # ways[(mask, end)] = number of simple paths from some start visiting
    # exactly ``mask`` and ending at ``end``.
    ways: dict[tuple[int, int], int] = {}
    for s in starts:
        if s in idx:
            i = idx[s]
            ways[(1 << i, i)] = ways.get((1 << i, i), 0) + 1

    total = 0
    frontier = ways
    while frontier:
        nxt: dict[tuple[int, int], int] = {}
        for (mask, end), cnt in frontier.items():
            if (1 << end) & target_mask:
                total += cnt
            out = adj_mask[end] & ~mask
            while out:
                lb = out & -out
                out ^= lb
                w = lb.bit_length() - 1
                key = (mask | lb, w)
                nxt[key] = nxt.get(key, 0) + cnt
        frontier = nxt
    return total


def weighted_discriminators(
    snet: StructuralNet,
    report: StructuralReport,
    tw: dict[str, TransitionWeights],
) -> WeightedDiscriminators:
    """Compute the discriminator block for one net (primary weight layer)."""
    adj = _supported_adjacency(snet, tw)
    supported = [s for s in snet.transitions if tw[s.name].weight]
    objectives = OBJECTIVE_TACTICS[snet.class_name]
    entries = report.entry_tactics
    tactic_set = set(snet.tactics)

    reach_recon = (
        tuple(sorted(_bfs(adj, ["reconnaissance"])))
        if "reconnaissance" in tactic_set
        else ()
    )
    reach_ia = (
        tuple(sorted(_bfs(adj, ["initial-access"])))
        if "initial-access" in tactic_set
        else ()
    )

    out_degrees = [len(vs) for vs in adj.values() if vs]
    branching = float(np.mean(out_degrees)) if out_degrees else 0.0

    has_in = {v for vs in adj.values() for v in vs}
    sinks = tuple(t for t in snet.tactics if not adj[t])
    islands = tuple(t for t in snet.tactics if not adj[t] and t not in has_in)

    return WeightedDiscriminators(
        profile=snet.class_name,
        n_transitions=len(snet.transitions),
        n_supported_transitions=len(supported),
        n_zero_weight_transitions=len(snet.transitions) - len(supported),
        reachable_from_recon_seed=reach_recon,
        reachable_from_initial_access=reach_ia,
        objective_reachable_from_initial_access={
            o: o in reach_ia for o in objectives
        },
        shortest_entry_to_objective=_shortest_path(adj, entries, objectives),
        longest_entry_to_objective=_longest_simple_path(
            snet.tactics, adj, entries, objectives
        ),
        branching_factor=branching,
        distinct_entry_to_objective_paths=_count_simple_paths(
            snet.tactics, adj, entries, objectives
        ),
        sink_places=sinks,
        island_places=islands,
    )


# ---------------------------------------------------------------------------
# The report object
# ---------------------------------------------------------------------------


@dataclass
class DivergenceReport:
    """Everything the markdown report and its test gate consume."""

    primary_variant: str
    n_flows: dict[str, dict[str, int]]  # profile -> {raw, dedup}
    per_place_jsd: dict[str, dict[str, float]]  # class -> place -> JSD (primary)
    mean_jsd: dict[str, float]  # class -> mean over comparable places (primary)
    mean_jsd_raw: dict[str, float]  # robustness column (raw vs raw aggregate)
    null_band: dict[str, dict[str, float]]  # class -> {p50, p95, max}
    null_trials: int
    null_seed: int
    exceeds_null_p95: dict[str, bool]
    aggregate_dedup_vs_raw_jsd: float  # robustness of the null profile itself
    discriminators: dict[str, WeightedDiscriminators] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary_variant": self.primary_variant,
            "n_flows": self.n_flows,
            "per_place_jsd": self.per_place_jsd,
            "mean_jsd": self.mean_jsd,
            "mean_jsd_raw": self.mean_jsd_raw,
            "null_band": self.null_band,
            "null_trials": self.null_trials,
            "null_seed": self.null_seed,
            "exceeds_null_p95": self.exceeds_null_p95,
            "aggregate_dedup_vs_raw_jsd": self.aggregate_dedup_vs_raw_jsd,
            "discriminators": {
                k: v.to_dict() for k, v in self.discriminators.items()
            },
        }


def build_divergence_report(
    nets: dict[str, StructuralNet],
    reports: dict[str, StructuralReport],
    weights: dict[str, dict[str, dict[str, TransitionWeights]]],
    edge_flows: dict[tuple[str, str], frozenset[str]],
    gap: GapIndex,
    profile_flows: dict[str, frozenset[str]],
    dedup_kept: frozenset[str],
    n_trials: int = NULL_TRIALS,
    seed: int = NULL_SEED,
) -> DivergenceReport:
    """Assemble the full divergence-from-aggregate report."""
    agg_primary = out_distributions(
        nets[AGGREGATE], weights[AGGREGATE][PRIMARY_VARIANT]
    )
    agg_raw = out_distributions(nets[AGGREGATE], weights[AGGREGATE]["raw"])

    place_jsd: dict[str, dict[str, float]] = {}
    mean_jsd: dict[str, float] = {}
    mean_jsd_raw: dict[str, float] = {}
    for cls in CLASS_NAMES:
        primary = per_place_jsd(
            out_distributions(nets[cls], weights[cls][PRIMARY_VARIANT]),
            agg_primary,
        )
        raw = per_place_jsd(
            out_distributions(nets[cls], weights[cls]["raw"]), agg_raw
        )
        place_jsd[cls] = primary
        mean_jsd[cls] = float(np.mean(list(primary.values()))) if primary else 0.0
        mean_jsd_raw[cls] = float(np.mean(list(raw.values()))) if raw else 0.0

    dedup_class_flows = {
        cls: profile_flows[cls] & dedup_kept for cls in CLASS_NAMES
    }
    null_band = shuffled_label_null(
        edge_flows, gap.tactic_of, dedup_class_flows, agg_primary,
        n_trials=n_trials, seed=seed,
    )

    agg_self = per_place_jsd(agg_primary, agg_raw)
    return DivergenceReport(
        primary_variant=PRIMARY_VARIANT,
        n_flows={
            p: {
                "raw": len(profile_flows[p]),
                "operator_dedup": len(profile_flows[p] & dedup_kept),
            }
            for p in nets
        },
        per_place_jsd=place_jsd,
        mean_jsd=mean_jsd,
        mean_jsd_raw=mean_jsd_raw,
        null_band=null_band,
        null_trials=n_trials,
        null_seed=seed,
        exceeds_null_p95={
            cls: mean_jsd[cls] > null_band[cls]["p95"] for cls in CLASS_NAMES
        },
        aggregate_dedup_vs_raw_jsd=(
            float(np.mean(list(agg_self.values()))) if agg_self else 0.0
        ),
        discriminators={
            p: weighted_discriminators(
                nets[p], reports[p], weights[p][PRIMARY_VARIANT]
            )
            for p in nets
        },
    )


__all__ = [
    "NULL_SEED",
    "NULL_TRIALS",
    "DivergenceReport",
    "WeightedDiscriminators",
    "build_divergence_report",
    "out_distributions",
    "per_place_jsd",
    "quotient_out_dists",
    "shuffled_label_null",
    "weighted_discriminators",
]
