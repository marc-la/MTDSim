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


__all__ = [
    "MovementRunResult",
    "ProfileSummary",
    "summarise",
    "summarise_profile",
]
