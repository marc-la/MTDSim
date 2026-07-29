"""The axis-measurement suite — a reader over movement records for the APT
criterion's M8b fields.

Sibling to :mod:`mtdsim.l3_simulation.movement.statistics` (the MTTC/ASR reader),
under the same contract: pure functions over :class:`MovementRunResult`s — no
simulation, no I/O (the two ``load_*`` helpers excepted), no mutation, no RNG.
The inherited ``AttackStatistics`` maths is untouched (M7, D5); the baseline arm
is reached only through the row *adapter* in §6, which reads its rows and changes
nothing.

Each section names the criterion axis whose *what-would-evidence-a-claim* (M8b)
field it discharges (``docs/implementation/apt_model_criterion.md`` §(d)):

1. **Progression** (axis 1) — distinct-place coverage over time; deepest
   *successfully actioned* consensus stage (the replacement for the saturated
   ``deepest_stage``, §(h)); foothold retention against network-layer MTD;
   effort-to-breadth conversion. The within-run trend
   (:func:`blocked_fraction_trend`) sits here too and serves axis 7: it is the
   only measure in the suite that asks whether the attacker got *better during
   a run*, which is what a learning claim rests on and what a run-level mean
   cannot show.
2. **Traversal diversity** (axis 3, and axis 2's stronger-claim measurement) —
   path entropy, distinct sequences/prefixes, between-profile Jensen–Shannon
   divergence in the L2 convention.
3. **Defender response** (axis 4) — action-mix shift around an MTD interrupt,
   recovery time from a throw-back (censored, and reported as such), and the
   failure-branch routing rate. These exist to discriminate *reacts* from
   *adapts usefully*.
4. **Cost ledger** (axis 6 prerequisite) — attempts, time decomposed into
   behavioural dwell / derived MTD confusion penalty / residual, re-work forced
   by MTD, yield. The ledger is a *measurement*, not an axis-6 claim: a claim
   additionally needs a decision rule that consumes it, which is out of scope.
5. **Cross-arm subset** (§6) — the event-wise measures computable on both arms,
   with the baseline arm reached through an adapter over ``AttackStatistics``
   rows. Event-wise vs time-normalised is enforced in the API:
   :class:`EventWiseComparable` carries **no time-denominated field**, because
   under S3-R the movement layer prices all of that arm's time while the
   baseline runs on substrate pricing, and the timing design record withdrew
   cross-arm comparability of time-normalised quantities rather than defending
   it. Time fields live only on the per-arm ledgers, which say so.
6. **Interval reporting** (§7) — every aggregate this suite feeds a claim from
   must carry its interval. :func:`interval_report` returns means, 95 %
   intervals and the adjacent pairs whose intervals are disjoint, so an
   unseparated ordering cannot be reported by accident (two sweeps failed their
   ordering conclusions for want of exactly this being routine).

Two standing constraints travel with every consumer:

- **The degenerate region.** At the operating mutation interval (200 s) neither
  attacker completes the objective (rate feasibility study §7 C5), so ASR
  discriminates nothing there. Nothing in this module computes ASR; use
  breadth- and event-shaped measures inside the region, or run outside it.
- **No ordering claim without disjoint intervals.** Ten seeds cannot separate
  adjacent profiles (two independent sweeps); report
  ``IntervalReport.separated_adjacent_pairs``, never a bare rank list.

**The MTD confusion penalty is derived, not recorded.** The penalty is consumed
inside the substrate's ``apply_mtd_interrupt_cost`` *before* the interrupted
event's record is appended, so it sits inside that record's
``end_time - start_time - dwell``; under S3-R every non-interrupted event's
value of that expression is ~0 (the movement layer supplies the whole
duration and ``step`` spends exactly it). :func:`mtd_penalty` reads the
penalty off interrupted records on that basis, and the seeded-run test in
``tests/l3_simulation/test_movement_measures.py`` verifies both halves of the
derivation rather than assuming them.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import numpy as np
from scipy.spatial.distance import jensenshannon

from mtdsim.l3_simulation.movement.attacker import DWELL_ONLY, MovementRecord
from mtdsim.l3_simulation.movement.statistics import (
    COMPROMISE_EVENTS,
    MovementRunResult,
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
CONSENSUS_PATH = _REPO_ROOT / "data" / "ogasp" / "controller" / "lifecycle_consensus.json"

# Terminal markers _emit_terminal writes so a walk's end is visible in the
# records. A *bare* marker (no verb, no dwell) names the place the token had
# just arrived at when the sim ended; it consumed nothing and dispatched
# nothing, so visit-denominated fractions exclude it (see visit_records).
TERMINAL_TAGS: frozenset[str] = frozenset({"SIM_END", "MAX_EVENTS"})

# The MTD resource type whose interrupt severs the attacker's position: the
# substrate clears the host cursor only on a network-layer mutation
# (apply_mtd_interrupt_cost, Brown B-INT-01). Application-layer mutations cost
# the service connection but leave the foothold.
NETWORK_RESOURCE = "network"


# ---------------------------------------------------------------------------
# Shared record views
# ---------------------------------------------------------------------------


def action_records(run: MovementRunResult) -> tuple[MovementRecord, ...]:
    """The run's *attempted actions*: every record that dispatched a verb —
    including a final verb the sim end cut short (it was committed), and
    blocked dispatches (the attempt was made; the substrate refused it).
    This is experiment 1's event definition, kept so its figures re-derive."""
    return tuple(r for r in run.records if r.verb)


def visit_records(run: MovementRunResult) -> tuple[MovementRecord, ...]:
    """Every place visit that consumed the attacker's time or dispatched a
    verb: all records except bare terminal markers (no verb, zero dwell).
    The denominator for visit-shaped fractions (e.g. dwell-only share)."""
    return tuple(r for r in run.records if r.verb or r.dwell > 0)


def is_compromise(record: MovementRecord) -> bool:
    """True when this record is a host-compromise event — one of the three
    (verb, outcome) pairs that compromise a host in the carved substrate."""
    return (record.verb, record.outcome) in COMPROMISE_EVENTS


def severs_position(record: MovementRecord) -> bool:
    """True when this record's MTD interrupt severed the attacker's position
    (network-layer resource: the substrate cleared the host cursor)."""
    return record.interrupted and record.interrupted_by == NETWORK_RESOURCE


def mtd_penalty(record: MovementRecord) -> float:
    """The MTD confusion penalty this record absorbed, derived (module
    docstring): for an interrupted record, ``end - start - dwell`` is the
    penalty the substrate charged after cutting the event short; for a
    non-interrupted record it is ~0 under S3-R and this returns 0.0."""
    if not record.interrupted:
        return 0.0
    return max(0.0, record.end_time - record.start_time - record.dwell)


@dataclass(frozen=True)
class CensoredDurations:
    """Durations with explicit right-censoring, never silently pooled:
    ``observed`` completed within the run; ``censored`` are lower bounds cut
    off at run termination. Report the two separately — a mean over the pool
    would understate every censored duration."""

    observed: tuple[float, ...]
    censored: tuple[float, ...]

    @property
    def n(self) -> int:
        return len(self.observed) + len(self.censored)


# ---------------------------------------------------------------------------
# §1 Progression (axis 1)
# ---------------------------------------------------------------------------


def load_stage_of(path: Path | str = CONSENSUS_PATH) -> dict[str, int]:
    """``tactic-place -> consensus lifecycle stage`` from the ratified S1
    consensus artefact (``lifecycle_consensus.json``). Loader, not a measure:
    pass the mapping into the stage measures so they stay pure."""
    with Path(path).open(encoding="utf-8") as fh:
        doc = json.load(fh)
    return {t: int(s) for t, s in doc["stage_of"].items()}


def distinct_place_curve(run: MovementRunResult) -> tuple[tuple[float, int], ...]:
    """Distinct-tactic coverage over time: ``(sim time of first visit,
    cumulative distinct-place count)`` per newly visited place, in visit
    order. Discriminates inside the degenerate region, where ASR cannot.
    The end-of-run scalar is :func:`distinct_place_count`."""
    seen: set[str] = set()
    curve: list[tuple[float, int]] = []
    for rec in run.records:
        if rec.place not in seen:
            seen.add(rec.place)
            curve.append((rec.start_time, len(seen)))
    return tuple(curve)


def distinct_place_count(run: MovementRunResult) -> int:
    """End-of-run distinct-tactic coverage (the curve's final value)."""
    return len({r.place for r in run.records})


def deepest_visited_stage(
    run: MovementRunResult, stage_of: Mapping[str, int]
) -> int | None:
    """The saturated measure, kept for the comparison the replacement must
    win: deepest consensus stage merely *visited*. §(h) records that every
    profile reaches stage 3 in its own campaign structure, so this cannot
    discriminate. None if no visited place is in the mapping."""
    stages = [stage_of[r.place] for r in run.records if r.place in stage_of]
    return max(stages) if stages else None


def deepest_successful_stage(
    run: MovementRunResult, stage_of: Mapping[str, int]
) -> int | None:
    """The replacement progression measure: deepest consensus stage at which
    the run recorded a **success verdict**, not merely a visit. Visiting
    saturates; succeeding should not (``pure_steal`` succeeds at almost
    nothing, ``infrastructure_setup`` succeeds hundreds of times low in the
    lifecycle). None when the run has no success at a mapped place — encode
    that as a depth *below* stage 0 (e.g. −1) before aggregating, rather than
    dropping the run, or the aggregate is biased toward the runs that
    succeeded. Adopt only if it separates a pair ``deepest_visited_stage``
    does not (validation gate 3)."""
    stages = [
        stage_of[r.place]
        for r in run.records
        if r.verdict == "success" and r.place in stage_of
    ]
    return max(stages) if stages else None


@dataclass(frozen=True)
class WithinRunTrend:
    """A quantity measured over the first against the last quarter of a run's
    attempted actions — the shape a *within-run* claim needs.

    A run-level mean cannot distinguish an attacker that was always mediocre
    from one that started badly and improved, and the difference between those
    two is exactly what a learning claim rests on. ``change`` is negative when
    the quantity fell over the run.
    """

    first_quartile: float
    last_quartile: float
    n_events: int

    @property
    def change(self) -> float:
        return self.last_quartile - self.first_quartile


def blocked_fraction(run: MovementRunResult) -> float | None:
    """Fraction of attempted actions the substrate refused on an unmet
    precondition — experiment 1's friction measure. None if nothing was
    attempted."""
    actions = action_records(run)
    if not actions:
        return None
    return sum(1 for r in actions if r.blocked) / len(actions)


def blocked_fraction_trend(run: MovementRunResult) -> WithinRunTrend | None:
    """The blocked fraction over the first against the last quarter of the
    run's attempted actions — **the learning signal, measured rather than
    assumed** (criterion axis 7's M8b field: does success against a class of
    target improve with exposure?).

    An attacker that reweights its routing from what has worked should refuse
    fewer of its own actions as a run proceeds; one that does not is not
    learning, whatever its routing does, and that verdict has to be reportable
    rather than explained away. Quartiles are taken over *events*, not time,
    because the claim is about accumulated experience and a run's events are
    not evenly spaced in time.

    None when the run attempted fewer than four actions (no quartile exists).
    """
    actions = action_records(run)
    n = len(actions)
    if n < 4:
        return None
    q = n // 4
    first = actions[:q]
    last = actions[-q:]
    return WithinRunTrend(
        first_quartile=sum(1 for r in first if r.blocked) / len(first),
        last_quartile=sum(1 for r in last if r.blocked) / len(last),
        n_events=n,
    )


def foothold_retentions(run: MovementRunResult) -> CensoredDurations:
    """Foothold-retention durations: sim time from each host-compromise event
    to the next MTD interrupt that severs the attacker's position (a
    network-layer resource — where the substrate clears the host cursor).
    No severing interrupt before run end → censored at ``termination_time``.
    This is the measure that makes MTD's claimed mechanism — destroying
    accumulated position — visible at all.

    Known blind spot: records carry no host identity, so this measures
    retention of *position*, not of a named host; several compromises before
    one sever each measure to that same sever."""
    observed: list[float] = []
    censored: list[float] = []
    records = run.records
    for i, rec in enumerate(records):
        if not is_compromise(rec):
            continue
        sever = next(
            (r for r in records[i + 1 :] if severs_position(r)), None
        )
        if sever is not None:
            observed.append(sever.end_time - rec.end_time)
        else:
            censored.append(run.termination_time - rec.end_time)
    return CensoredDurations(tuple(observed), tuple(censored))


def n_successes(run: MovementRunResult) -> int:
    """Success-verdict count over attempted actions."""
    return sum(1 for r in action_records(run) if r.verdict == "success")


def successes_per_distinct_host(run: MovementRunResult) -> float | None:
    """Effort-to-breadth conversion, movement-arm refinement: successful
    actions per distinct host compromised (experiment 1 finding 2, formalised).
    None when the run compromised no host — an infinite ratio is the finding,
    not a number; report it alongside :func:`n_successes`."""
    if run.compromised_count <= 0:
        return None
    return n_successes(run) / run.compromised_count


def actions_per_distinct_host(run: MovementRunResult) -> float | None:
    """Effort-to-breadth, cross-arm form: *attempted* actions per distinct
    host. The baseline counterpart (§6) counts its rows the same way — the
    native record has no success/failure verdict, so attempted-actions is the
    definition both arms can honour. Event-wise: safe across arms."""
    if run.compromised_count <= 0:
        return None
    return len(action_records(run)) / run.compromised_count


# ---------------------------------------------------------------------------
# §2 Traversal diversity (axis 3; axis 2's stronger-claim measurement)
# ---------------------------------------------------------------------------


def place_sequence(run: MovementRunResult) -> tuple[str, ...]:
    """The run's visited-place sequence (one entry per record; each record is
    one place visit, terminal markers naming the arrival the end cut off)."""
    return tuple(r.place for r in run.records)


def distinct_sequences(runs: Sequence[MovementRunResult]) -> int:
    """Count of unique whole place-sequences across runs (seed-sensitive;
    prefer :func:`distinct_prefixes` for cross-seed claims)."""
    return len({place_sequence(r) for r in runs})


def distinct_prefixes(runs: Sequence[MovementRunResult], k: int) -> int:
    """Count of unique length-``k`` place-sequence prefixes across runs — far
    less seed-sensitive than whole sequences."""
    return len({place_sequence(r)[:k] for r in runs})


def path_entropy(runs: Sequence[MovementRunResult]) -> float:
    """Shannon entropy (bits) of the empirical out-transition distribution at
    each place, aggregated over the runs, weighted by visits: places that are
    routed through often count for more. A profile whose branching collapses
    to one route scores near zero however plural its net looks. Transitions
    are read from the records (``place -> next_place``), so this measures the
    walk actually taken, not the net's declared branching."""
    out_counts: dict[str, Counter[str]] = {}
    for run in runs:
        for rec in run.records:
            if rec.next_place is not None:
                out_counts.setdefault(rec.place, Counter())[rec.next_place] += 1
    total = sum(sum(c.values()) for c in out_counts.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for counts in out_counts.values():
        n_place = sum(counts.values())
        h_place = -sum(
            (c / n_place) * math.log2(c / n_place) for c in counts.values()
        )
        entropy += (n_place / total) * h_place
    return entropy


def jsd(p_dist: Mapping[str, float], q_dist: Mapping[str, float]) -> float:
    """Jensen–Shannon divergence in the L2 convention —
    ``jensenshannon(p, q, base=2) ** 2``, in [0, 1], over the union of
    supports (mirrors ``petri/divergence._jsd``; one convention, per the
    GASP schema's discrimination check, not a second one)."""
    support = sorted(set(p_dist) | set(q_dist))
    p = np.array([p_dist.get(t, 0.0) for t in support])
    q = np.array([q_dist.get(t, 0.0) for t in support])
    return float(jensenshannon(p, q, base=2) ** 2)


def visit_distribution(runs: Sequence[MovementRunResult]) -> dict[str, float]:
    """Normalised place-visit frequencies pooled over the runs — the
    execution-level action stream (all visits, dwell-only included: engaging
    a tactic is behaviour whether or not a verb fired)."""
    counts: Counter[str] = Counter()
    for run in runs:
        for rec in visit_records(run):
            counts[rec.place] += 1
    total = sum(counts.values())
    return {p: c / total for p, c in counts.items()} if total else {}


def terminal_place_distribution(
    runs: Sequence[MovementRunResult],
) -> dict[str, float]:
    """Normalised distribution of each run's final place (its terminal
    tactic). Runs with no records are skipped."""
    counts: Counter[str] = Counter(
        run.records[-1].place for run in runs if run.records
    )
    total = sum(counts.values())
    return {p: c / total for p, c in counts.items()} if total else {}


@dataclass(frozen=True)
class ProfileDivergence:
    """Pairwise between-profile behavioural divergence (JSD, L2 convention),
    on the pooled action streams and on the terminal-tactic distributions.
    Keys are ``(profile_a, profile_b)`` with a < b. This is axis 2's
    stronger-claim measurement — the L2 corpus-level check mirrored at the
    execution level — and axis 3's between-profile column."""

    visit_stream: dict[tuple[str, str], float]
    terminal: dict[tuple[str, str], float]


def profile_divergence(
    results: Sequence[MovementRunResult],
) -> ProfileDivergence:
    """Compute :class:`ProfileDivergence` over a mixed run set, grouping by
    ``result.profile``."""
    by_profile: dict[str, list[MovementRunResult]] = {}
    for r in results:
        by_profile.setdefault(r.profile, []).append(r)
    visit_dists = {p: visit_distribution(rs) for p, rs in by_profile.items()}
    term_dists = {
        p: terminal_place_distribution(rs) for p, rs in by_profile.items()
    }
    profiles = sorted(by_profile)
    pairs = [
        (a, b) for i, a in enumerate(profiles) for b in profiles[i + 1 :]
    ]
    return ProfileDivergence(
        visit_stream={(a, b): jsd(visit_dists[a], visit_dists[b]) for a, b in pairs},
        terminal={(a, b): jsd(term_dists[a], term_dists[b]) for a, b in pairs},
    )


# ---------------------------------------------------------------------------
# §3 Defender response (axis 4)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ActionMixShift:
    """Verb and place-class mixes in the ``window`` visits before vs after
    each MTD interrupt, pooled over the run's interrupts (paired within run,
    so seed variance cancels). Dwell-only visits appear in the verb mix as
    ``""`` — thinking is part of the mix, not noise to drop. Compare the
    before/after pairs with :func:`jsd` (after normalising) or read the raw
    counts directly."""

    n_interrupts: int
    window: int
    before_verbs: dict[str, int]
    after_verbs: dict[str, int]
    before_class: dict[str, int]
    after_class: dict[str, int]


def interrupt_action_mix(
    run: MovementRunResult, window: int = 5
) -> ActionMixShift | None:
    """Action-mix shift around MTD interrupts (axis 4: does the attacker
    *change what it does* after the defender moves, or resume the same mix?).
    None when the run has no interrupt. The interrupted visit itself belongs
    to neither window."""
    visits = visit_records(run)
    interrupt_idx = [i for i, r in enumerate(visits) if r.interrupted]
    if not interrupt_idx:
        return None
    before_verbs: Counter[str] = Counter()
    after_verbs: Counter[str] = Counter()
    before_class: Counter[str] = Counter()
    after_class: Counter[str] = Counter()
    for i in interrupt_idx:
        for r in visits[max(0, i - window) : i]:
            before_verbs[r.verb] += 1
            before_class[r.place_class] += 1
        for r in visits[i + 1 : i + 1 + window]:
            after_verbs[r.verb] += 1
            after_class[r.place_class] += 1
    return ActionMixShift(
        n_interrupts=len(interrupt_idx),
        window=window,
        before_verbs=dict(before_verbs),
        after_verbs=dict(after_verbs),
        before_class=dict(before_class),
        after_class=dict(after_class),
    )


def normalise(counts: Mapping[str, int | float]) -> dict[str, float]:
    """Counts -> distribution (for feeding :func:`jsd`)."""
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()} if total else {}


def recovery_times(run: MovementRunResult) -> CensoredDurations:
    """Recovery time from an MTD-induced throw-back: sim time from each
    interrupted record to the next success verdict. No success before run end
    → censored at ``termination_time`` (and reported as such — a censored
    recovery is the strongest possible non-recovery signal, not missing
    data)."""
    observed: list[float] = []
    censored: list[float] = []
    records = run.records
    for i, rec in enumerate(records):
        if not rec.interrupted:
            continue
        recovery = next(
            (r for r in records[i + 1 :] if r.verdict == "success"), None
        )
        if recovery is not None:
            observed.append(recovery.end_time - rec.end_time)
        else:
            censored.append(run.termination_time - rec.end_time)
    return CensoredDurations(tuple(observed), tuple(censored))


def failure_routing_rate(run: MovementRunResult) -> float | None:
    """Fraction of the run's verdict-carrying routing decisions taken on the
    failure column (the overlay's failure out-set). Correlate against breadth
    across runs to ask whether routing on failure helps: if it does, the
    profiles that route on failure most should not be the ones that get least
    far. None when the run routed on no verdict at all (dwell-only routing is
    unconditioned and excluded by construction)."""
    routed = [r for r in run.records if r.next_place is not None and r.verdict]
    if not routed:
        return None
    return sum(1 for r in routed if r.verdict == "failure") / len(routed)


TERMINAL_MODES = ("objective", "sink", "sim_end", "max_events", "horizon", "empty")


def terminal_mode(run: MovementRunResult) -> str:
    """How the walk ended (experiment 1's vocabulary, formalised): objective /
    sink / sim_end / max_events / horizon / empty. The baseline arm has no
    counterpart derivable from its rows — its runner knows only objective vs
    horizon — so cross-arm terminal comparisons use that coarser pair."""
    if run.reached_objective:
        return "objective"
    if not run.records:
        return "empty"
    last = run.records[-1]
    if last.outcome == "MAX_EVENTS":
        return "max_events"
    if last.outcome == "SIM_END":
        return "sim_end"
    if last.next_place is None:
        return "sink"
    return "horizon"


# ---------------------------------------------------------------------------
# §4 Cost ledger (axis 6 prerequisite)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MovementCostLedger:
    """One movement run's attacker-side cost account. **Time fields are
    movement-arm only** — under S3-R this arm's time is priced by the
    movement layer while the baseline runs on substrate pricing, so nothing
    time-denominated here may be compared across arms
    (``metrics_semantics.md``; timing design record). The cross-arm subset is
    :func:`comparable_from_movement`. The ledger is a measurement, not an
    axis-6 claim — the claim needs a decision rule that consumes it."""

    # -- events (cross-arm-safe counts; fractions via comparable_from_movement)
    n_actions: int              # attempted actions (verb dispatches)
    n_blocked: int              # precondition-unmet attempts
    n_interrupted: int          # MTD-interrupted visits, dwell-only included
    n_dwell_only: int           # dwell-only visits (no verb to dispatch)
    n_success: int
    n_failure: int              # failure verdicts (blocked + interrupted included)
    attempts_by_verb: dict[str, int]
    blocked_by_verb: dict[str, int]
    success_by_verb: dict[str, int]
    # -- time, sim seconds (MOVEMENT-ARM ONLY)
    time_active: float          # sum over records of (end - start)
    time_dwell: float           # behavioural dwell actually served
    time_mtd_penalty: float     # derived confusion penalty (module docstring)
    time_residual: float        # non-interrupted (end - start - dwell); ~0 under
                                # S3-R — a returning value is a regime regression
    time_interrupted_events: float  # re-work: time consumed by MTD-cut events
                                    # (served dwell + penalty; none produced a success)
    # -- outcome
    n_distinct_hosts: int       # substrate ground truth (compromised_count)
    elapsed: float              # run termination time

    @property
    def hosts_per_ksec(self) -> float:
        """Yield per unit cost: distinct hosts per 1 000 s of sim time.
        Time-normalised — movement-arm only, never cross-arm."""
        return 1000.0 * self.n_distinct_hosts / self.elapsed if self.elapsed else 0.0


def cost_ledger(run: MovementRunResult) -> MovementCostLedger:
    """Build the per-run cost ledger from the records alone."""
    actions = action_records(run)
    visits = visit_records(run)
    attempts: Counter[str] = Counter(r.verb for r in actions)
    blocked: Counter[str] = Counter(r.verb for r in actions if r.blocked)
    success: Counter[str] = Counter(
        r.verb for r in actions if r.verdict == "success"
    )
    interrupted = [r for r in run.records if r.interrupted]
    return MovementCostLedger(
        n_actions=len(actions),
        n_blocked=sum(blocked.values()),
        n_interrupted=len(interrupted),
        n_dwell_only=sum(1 for r in visits if r.place_class == DWELL_ONLY),
        n_success=sum(success.values()),
        n_failure=sum(1 for r in actions if r.verdict == "failure"),
        attempts_by_verb=dict(attempts),
        blocked_by_verb=dict(blocked),
        success_by_verb=dict(success),
        time_active=sum(r.end_time - r.start_time for r in run.records),
        time_dwell=sum(r.dwell for r in run.records),
        time_mtd_penalty=sum(mtd_penalty(r) for r in run.records),
        time_residual=sum(
            max(0.0, r.end_time - r.start_time - r.dwell)
            for r in run.records
            if not r.interrupted
        ),
        time_interrupted_events=sum(
            r.end_time - r.start_time for r in interrupted
        ),
        n_distinct_hosts=run.compromised_count,
        elapsed=run.termination_time,
    )


# ---------------------------------------------------------------------------
# §6 Cross-arm subset — the baseline adapter and the comparable type
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EventWiseComparable:
    """The measures safe to compare across arms: event-wise (fractions of
    steps, counts, per-host ratios), **no time-denominated field by
    construction** — that is the API enforcing the event-wise/time-normalised
    distinction rather than leaving it to the caller.

    Structural zeros are reported, not omitted, because the structural zero
    *is* the contrast: the baseline attacker has no precondition to fail
    (``blocked_fraction`` 0.0 — its scripted order is the native
    precondition order) and no non-action concept (``dwell_only_fraction``
    0.0). A reader comparing arms sees the zero and its reason, not a
    missing row."""

    arm: str                    # "movement" | "baseline"
    profile: str
    n_events: int               # attempted actions (movement) / rows (baseline)
    verb_mix: dict[str, float]  # fraction of attempted actions per verb
    blocked_fraction: float     # baseline: 0.0, structural
    interrupted_fraction: float # share of events an MTD cut short
    dwell_only_fraction: float  # share of visits dispatching nothing; baseline: 0.0, structural
    n_distinct_hosts: int
    actions_per_distinct_host: float | None  # attempted actions / distinct hosts
    reached_objective: bool | None  # None when the source rows cannot say


def comparable_from_movement(run: MovementRunResult) -> EventWiseComparable:
    """The cross-arm subset of one movement run."""
    actions = action_records(run)
    visits = visit_records(run)
    n = len(actions)
    mix = Counter(r.verb for r in actions)
    return EventWiseComparable(
        arm="movement",
        profile=run.profile,
        n_events=n,
        verb_mix={v: c / n for v, c in mix.items()} if n else {},
        blocked_fraction=(sum(1 for r in actions if r.blocked) / n) if n else 0.0,
        interrupted_fraction=(
            (sum(1 for r in actions if r.interrupted) / n) if n else 0.0
        ),
        dwell_only_fraction=(
            sum(1 for r in visits if r.place_class == DWELL_ONLY) / len(visits)
            if visits
            else 0.0
        ),
        n_distinct_hosts=run.compromised_count,
        actions_per_distinct_host=actions_per_distinct_host(run),
        reached_objective=run.reached_objective,
    )


_NONE = "None"  # AttackStatistics' string sentinel in its CSV rows


@dataclass(frozen=True)
class BaselineCostLedger:
    """The baseline arm's counterpart ledger, built by :func:`baseline_ledger`
    from ``AttackStatistics`` rows — an **adapter**: the inherited class and
    its rows are read, never touched (M7, D5). The native record carries no
    success/failure verdict and no blocked concept, so the counterpart fields
    are the ones its rows can honour: attempts by verb, MTD re-work
    (interrupted rows), compromise events and distinct hosts. ``time_total``
    is substrate-priced — **not comparable** to any movement-arm time."""

    n_actions: int
    n_interrupted: int
    attempts_by_verb: dict[str, int]
    n_compromise_events: int
    n_distinct_hosts: int
    time_total: float  # sum of row durations (substrate pricing; arm-local only)


def _as_rows(rows) -> list[Mapping]:
    """Accept a pandas DataFrame (``AttackStatistics.get_record()``) or any
    iterable of row mappings (e.g. ``csv.DictReader``)."""
    if hasattr(rows, "to_dict"):
        return rows.to_dict("records")
    return list(rows)


def baseline_ledger(rows) -> BaselineCostLedger:
    """Build the baseline counterpart ledger from attack-record rows.

    Distinct hosts are counted on ``compromise_host_uuid`` (stable across
    topology shuffles, unlike the positional host id). Note the recorded
    asymmetry: the driven arm writes no interrupt row to this record, so a
    ledger from these rows is native-arm-only — the movement arm's ledger is
    built from ``MovementRecord`` instead (:func:`cost_ledger`)."""
    rs = _as_rows(rows)
    attempts: Counter[str] = Counter(str(r["name"]) for r in rs)
    compromises = [r for r in rs if str(r.get("compromise_host", _NONE)) != _NONE]
    return BaselineCostLedger(
        n_actions=len(rs),
        n_interrupted=sum(
            1 for r in rs if str(r.get("interrupted_in", _NONE)) != _NONE
        ),
        attempts_by_verb=dict(attempts),
        n_compromise_events=len(compromises),
        n_distinct_hosts=len(
            {str(r["compromise_host_uuid"]) for r in compromises}
        ),
        time_total=sum(float(r.get("duration", 0.0)) for r in rs),
    )


def comparable_from_baseline(
    rows, *, reached_objective: bool | None = None
) -> EventWiseComparable:
    """The cross-arm subset of one baseline run, from its attack-record rows.
    ``reached_objective`` is not derivable from the rows — pass it from the
    runner if known, else it is reported as unknown (None), never guessed."""
    led = baseline_ledger(rows)
    n = led.n_actions
    return EventWiseComparable(
        arm="baseline",
        profile="baseline",
        n_events=n,
        verb_mix={v: c / n for v, c in led.attempts_by_verb.items()} if n else {},
        blocked_fraction=0.0,       # structural: the native order IS the precondition order
        interrupted_fraction=(led.n_interrupted / n) if n else 0.0,
        dwell_only_fraction=0.0,    # structural: no non-action concept on this arm
        n_distinct_hosts=led.n_distinct_hosts,
        actions_per_distinct_host=(
            n / led.n_distinct_hosts if led.n_distinct_hosts else None
        ),
        reached_objective=reached_objective,
    )


# ---------------------------------------------------------------------------
# §7 Interval reporting
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Interval:
    """Mean with normal-approximation 95 % interval (the experiment-1
    convention: mean ± 1.96·SEM; ci95 = 0 at n = 1)."""

    n: int
    mean: float
    ci95: float

    @property
    def lo(self) -> float:
        return self.mean - self.ci95

    @property
    def hi(self) -> float:
        return self.mean + self.ci95


def mean_ci(values: Sequence[float]) -> Interval:
    """The experiment-1 mean/CI convention over a non-empty value sequence."""
    xs = list(values)
    if not xs:
        raise ValueError(
            "mean_ci needs at least one value; encode absent measurements "
            "explicitly (e.g. depth -1 for no-success) rather than passing "
            "an empty group"
        )
    m = sum(xs) / len(xs)
    if len(xs) == 1:
        return Interval(n=1, mean=m, ci95=0.0)
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))
    return Interval(n=len(xs), mean=m, ci95=1.96 * sd / math.sqrt(len(xs)))


@dataclass(frozen=True)
class IntervalReport:
    """The default output shape for any per-profile aggregate: per-group
    intervals sorted by mean, and the adjacent pairs whose intervals are /
    are not disjoint. An ordering claim is supported only where
    ``unseparated_adjacent_pairs`` is empty — both sweeps failed their
    ordering conclusions because this was not routine; the helper makes the
    unsupported case impossible to round up silently."""

    rows: tuple[tuple[str, Interval], ...]  # ascending by mean
    separated_adjacent_pairs: tuple[tuple[str, str], ...]
    unseparated_adjacent_pairs: tuple[tuple[str, str], ...]

    @property
    def ordering_supported(self) -> bool:
        """True only when every adjacent pair is CI-disjoint — the precondition
        for reporting the rows' order as an ordering at all."""
        return not self.unseparated_adjacent_pairs and len(self.rows) > 1


def interval_report(
    values_by_group: Mapping[str, Sequence[float]]
) -> IntervalReport:
    """Aggregate a per-group measure into the interval-carrying report shape.
    Groups must be non-empty (see :func:`mean_ci` on encoding absences).
    Adjacency is in mean order; a pair is separated when the intervals are
    strictly disjoint (``lo`` of the higher above ``hi`` of the lower)."""
    rows = sorted(
        ((g, mean_ci(vs)) for g, vs in values_by_group.items()),
        key=lambda kv: kv[1].mean,
    )
    separated: list[tuple[str, str]] = []
    unseparated: list[tuple[str, str]] = []
    for (g_lo, iv_lo), (g_hi, iv_hi) in zip(rows, rows[1:]):
        (separated if iv_hi.lo > iv_lo.hi else unseparated).append((g_lo, g_hi))
    return IntervalReport(
        rows=tuple(rows),
        separated_adjacent_pairs=tuple(separated),
        unseparated_adjacent_pairs=tuple(unseparated),
    )


__all__ = [
    "CONSENSUS_PATH",
    "NETWORK_RESOURCE",
    "TERMINAL_MODES",
    "TERMINAL_TAGS",
    # record views
    "action_records",
    "visit_records",
    "is_compromise",
    "severs_position",
    "mtd_penalty",
    "CensoredDurations",
    # §1 progression
    "load_stage_of",
    "distinct_place_curve",
    "distinct_place_count",
    "deepest_visited_stage",
    "deepest_successful_stage",
    "foothold_retentions",
    "n_successes",
    "successes_per_distinct_host",
    "actions_per_distinct_host",
    # §2 diversity
    "place_sequence",
    "distinct_sequences",
    "distinct_prefixes",
    "path_entropy",
    "jsd",
    "visit_distribution",
    "terminal_place_distribution",
    "ProfileDivergence",
    "profile_divergence",
    # §3 defender response
    "ActionMixShift",
    "interrupt_action_mix",
    "normalise",
    "recovery_times",
    "failure_routing_rate",
    "terminal_mode",
    # §4 cost ledger
    "MovementCostLedger",
    "cost_ledger",
    # §6 cross-arm
    "EventWiseComparable",
    "comparable_from_movement",
    "BaselineCostLedger",
    "baseline_ledger",
    "comparable_from_baseline",
    # §7 intervals
    "Interval",
    "mean_ci",
    "IntervalReport",
    "interval_report",
]
