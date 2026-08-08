"""A reader over the movement layer's records — MTTC / ASR per profile.

Strictly a **reader** (M7 handoff): it consumes :class:`MovementRecord`s and
per-run metadata and derives the movement-layer metrics. It does **not** touch the
inherited :class:`~mtdnetwork.statistic.attack_statistics.AttackStatistics` maths,
which continues to serve the 6-phase baseline and the goldens unchanged (D5).

Two metrics, within-substrate only (internal MTTC — no cross-paper magnitude
claim, ``metrics_semantics.md`` §(d)):

- **ASR** (attack success rate) — the fraction of a profile's runs that reached
  the substrate's compromise objective (the network-compromised termination the
  substrate's own ``end_event`` fires; carried on the run result).
- **MTTC** (mean time to compromise) — the mean, over a profile's runs, of the
  sim time of the *first* host compromise the walk drove. A run that never
  compromised a host contributes to the ASR denominator but not the MTTC mean
  (stated, not hidden — a degenerate run has no compromise time to average).

A "compromise event" is read from the records by the substrate outcome a success
verdict carried: an ``EXPLOIT_VULN`` that returned ``EXPLOIT_COMPROMISED``, a
``BRUTE_FORCE`` that returned ``TRUE``, or a ``SCAN_PORT`` credential-reuse hit
(``TRUE``). These are the three verb outcomes that compromise a host in the carved
substrate (anatomy §2.2 / controller.md §4).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
from typing import Sequence

from mtdsim.l3_simulation.movement.attacker import MovementRecord

# (verb, outcome tag) pairs that mark a host compromise in the carved substrate.
_COMPROMISE_EVENTS: frozenset[tuple[str, str]] = frozenset(
    {
        ("EXPLOIT_VULN", "EXPLOIT_COMPROMISED"),
        ("BRUTE_FORCE", "TRUE"),
        ("SCAN_PORT", "TRUE"),
    }
)
# Public name for the sibling measures module (measures.py) and any other reader;
# the single definition of "compromise event" stays here.
COMPROMISE_EVENTS = _COMPROMISE_EVENTS


@dataclass(frozen=True)
class MTDExecution:
    """One executed mutation, snapshotted verbatim from the substrate's own
    per-operation record (``MTDStatistics``): the mechanism's name, the window
    during which its resource layer was held for deployment, and that layer.
    The substrate holds the layer's SimPy resource for exactly
    ``[start_time, finish_time]`` while the mutation deploys, so ``duration``
    is the time that layer was under active reconfiguration — the raw material
    of the derived defender-disruption ledger (``measures.disruption_ledger``).
    Known blind spot, inherited from the substrate: a mutation aborted
    mid-execution because the network was compromised appends no record, so its
    partial window is invisible here too."""

    name: str
    start_time: float
    finish_time: float
    duration: float
    layer: str  # the substrate resource type: network / application / reserve


@dataclass(frozen=True)
class MTDDecision:
    """One reactive-defender decision, snapshotted from ``MTDAIOperation``'s own
    per-decision ledger.

    Only the ``mtd_ai`` scheme produces these: every other scheme deploys on a
    timer and takes no decision to record. The ledger exists because the
    execution records cannot supply it — they hold only mutations that *ran*, so
    a decision forced by the static-degrade guard, one drawn by exploration and
    one chosen by the policy are indistinguishable after the fact, and the
    no-op share is not recoverable from them at all.

    ``source`` is one of ``greedy`` / ``random`` / ``forced``. The distinction is
    load-bearing rather than diagnostic: at any epsilon above zero the pooled
    no-op share is floored by ``epsilon / n_actions`` whatever the policy has
    learned, so a share read over all three reports the exploration schedule and
    not the defender's behaviour.
    """

    time: float
    action: int  # 0 is the no-op; 1..4 index the deploying action space
    source: str


@dataclass(frozen=True)
class MovementRunResult:
    """One run's outcome: the movement records plus the substrate metadata a
    reader needs to compute MTTC / ASR."""

    profile: str
    seed: int
    with_synthetic_overlay: bool
    records: tuple[MovementRecord, ...]
    reached_objective: bool  # the substrate end_event fired (network compromised)
    termination_time: float  # sim time at which the run stopped
    compromised_count: int  # hosts compromised (substrate ground truth)
    # How many times the S5 retrace policy fired. Surfaced rather than budgeted:
    # the design declined a declared retrace budget on the argument that the
    # one-shot suppression and the time cost already bound the behaviour, so the
    # frequency has to be visible for that argument to stay falsifiable
    # (sink_retrace_design.md §3.4). Always 0 when the policy is off.
    retrace_count: int = 0
    # Defender-side observability, snapshotted from the substrate's own
    # MTDStatistics after the run (no behaviour touched; empty when no MTD ran).
    # The attacker-side records above cannot carry these — a mutation the
    # attacker never collided with leaves no MovementRecord trace — and the
    # disruption ledger needs every executed mutation, not the intersecting ones.
    mtd_executions: tuple[MTDExecution, ...] = ()
    mtd_suspended_count: int = 0        # mutations deferred on resource contention
    mtd_attack_interrupted: int = 0     # substrate's own interrupt tally (cross-check
                                        # against the records' interrupted count)
    # The reactive defender's per-decision ledger — empty under every scheme but
    # ``mtd_ai``, which is the only one that takes a decision rather than firing
    # on a timer. Carried on the result because the whole point of running the
    # movement attacker against that defender is to read what the defender
    # *chose*, and ``mtd_executions`` above records only what it deployed.
    mtd_decisions: tuple[MTDDecision, ...] = ()

    def first_compromise_time(self) -> float | None:
        """Sim time of the first compromise the walk drove, or None if the run
        never compromised a host."""
        for rec in self.records:
            if (rec.verb, rec.outcome) in _COMPROMISE_EVENTS:
                return rec.end_time
        return None


@dataclass(frozen=True)
class ProfileSummary:
    """Aggregated movement-layer metrics for one profile over its runs."""

    profile: str
    n_runs: int
    asr: float  # fraction of runs that reached the objective
    mttc: float | None  # mean first-compromise time (None if no run compromised)
    n_compromising_runs: int  # runs with >=1 compromise (the MTTC denominator)
    mean_events: float  # mean number of recorded events per run (non-degeneracy)
    mean_compromised_hosts: float

    def as_dict(self) -> dict:
        return {
            "profile": self.profile,
            "n_runs": self.n_runs,
            "asr": self.asr,
            "mttc": self.mttc,
            "n_compromising_runs": self.n_compromising_runs,
            "mean_events": self.mean_events,
            "mean_compromised_hosts": self.mean_compromised_hosts,
        }


def summarise_profile(results: Sequence[MovementRunResult]) -> ProfileSummary:
    """Aggregate one profile's runs into a :class:`ProfileSummary`.

    Requires a non-empty, single-profile run set (raises otherwise — a summary
    over mixed profiles would silently mislead)."""
    if not results:
        raise ValueError("summarise_profile needs at least one run result")
    profiles = {r.profile for r in results}
    if len(profiles) != 1:
        raise ValueError(f"mixed profiles in one summary: {sorted(profiles)}")

    n_runs = len(results)
    asr = mean(1.0 if r.reached_objective else 0.0 for r in results)
    compromise_times = [
        t for t in (r.first_compromise_time() for r in results) if t is not None
    ]
    mttc = mean(compromise_times) if compromise_times else None
    return ProfileSummary(
        profile=next(iter(profiles)),
        n_runs=n_runs,
        asr=asr,
        mttc=mttc,
        n_compromising_runs=len(compromise_times),
        mean_events=mean(len(r.records) for r in results),
        mean_compromised_hosts=mean(r.compromised_count for r in results),
    )


def summarise(results: Sequence[MovementRunResult]) -> dict[str, ProfileSummary]:
    """Per-profile summaries keyed by profile name, over a mixed run set."""
    by_profile: dict[str, list[MovementRunResult]] = {}
    for r in results:
        by_profile.setdefault(r.profile, []).append(r)
    return {p: summarise_profile(rs) for p, rs in sorted(by_profile.items())}


def decision_summary(results: Sequence[MovementRunResult]) -> dict:
    """The reactive defender's choice distribution over a run set.

    This is the statistic the axis-8 falsifier is built around: *does what the
    defender chooses differ across attacker profiles at all?* It is reported as
    a distribution over the action space rather than as an outcome, because a
    defender whose choices are unmoved by a large spread in attacker behaviour
    cannot be steered by a smaller, deliberate one, and one cheap run says so.

    The greedy share is separated from the pooled share for the reason
    :class:`MTDDecision` records: the pooled one is floored by the exploration
    rate and would report the schedule rather than the policy. Runs with no
    ledger (any scheme but ``mtd_ai``) contribute nothing and are counted, so a
    caller can tell an empty ledger from a defender that never acted.
    """
    ledger = [d for r in results for d in r.mtd_decisions]
    greedy = [d for d in ledger if d.source == "greedy"]

    by_action: dict[int, int] = {}
    for decision in ledger:
        by_action[decision.action] = by_action.get(decision.action, 0) + 1
    by_source: dict[str, int] = {}
    for decision in ledger:
        by_source[decision.source] = by_source.get(decision.source, 0) + 1

    n_noop = sum(1 for d in ledger if d.action == 0)
    n_greedy_noop = sum(1 for d in greedy if d.action == 0)

    return {
        "n_runs": len(results),
        "n_runs_with_ledger": sum(1 for r in results if r.mtd_decisions),
        "n_decisions": len(ledger),
        "action_counts": dict(sorted(by_action.items())),
        "source_counts": dict(sorted(by_source.items())),
        "noop_share": n_noop / len(ledger) if ledger else float("nan"),
        # The verdict statistic. Read it against the two floors rather than
        # against zero: the static-degrade guard forces a deployment after its
        # idle period whatever the policy wants, and a uniform random selector
        # over a five-action space sits at 0.2.
        "greedy_noop_share": (
            n_greedy_noop / len(greedy) if greedy else float("nan")
        ),
        "n_greedy": len(greedy),
        "n_forced": by_source.get("forced", 0),
    }


__all__ = [
    "COMPROMISE_EVENTS",
    "MTDDecision",
    "MTDExecution",
    "MovementRunResult",
    "ProfileSummary",
    "decision_summary",
    "summarise",
    "summarise_profile",
]
