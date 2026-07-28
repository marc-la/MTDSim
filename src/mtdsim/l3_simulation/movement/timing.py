"""Per-tactic firing times — the movement layer's timing source (S3).

**The movement layer supplies the time; the SimPy loop spends it.** That split is
the whole point of this module, and it is why the module imports no SimPy: a
tactic's time is a *parameter the movement layer declares*, and advancing the
clock is the discrete-event engine's job. A different simulator's event loop would
spend the same supplied durations, which is what keeps the movement layer portable
across substrates (design record §1, §2).

Under the generalised stochastic Petri net (GSPN) reading of the walk, a place's
dwell is a **timed transition** with **exponential** firing, and the
verdict-conditioned routing choice among its out-edges is a **weighted immediate
transition** consuming no simulated time. This module is the timed half. The
declared per-tactic value in the duration catalogue
(``data/ogasp/tactic_durations.json``) is read as the **mean** of an
``Exponential(rate = 1 / mean)`` draw rather than as a constant dwell; the
magnitudes are unchanged, so every tier badge, sweep band and group anchor carries
over untouched (design record §3).

**A declared mean of zero stays immediate, not degenerate.** ``Exponential(mean 0)``
has no meaning; a zero-duration tactic (``resource-development``, the off-network
prep null) is a GSPN *immediate* transition, so it returns zero time and consumes
no draw at all. The same holds for a tactic absent from the catalogue.

**Why exponential, stated honestly.** It is a tractable, precedented choice, not a
fidelity claim: memorylessness is nowhere defended in the surveyed stochastic-net
literature as faithful to attacker behaviour, and the one large-sample empirical
study of compromise timing finds a heavier tail than exponential. What the choice
buys is that the *mean* is the load-bearing quantity for a mean-based metric, and
the means are exactly what the catalogue declares and the sweep bands bracket. The
full argument, its literature grounding, and the condition under which it leaks
(distribution shape re-enters through the MTD-interrupt channel, because a long
dwell is likelier to be interrupted than a short one) are in the design record §3.2.

**Determinism (SIM-05).** The draws come from a stream of this module's own, seeded
by a pure transform of the run seed, so they neither read nor advance the token
sampler's stream or the substrate's global ``random`` / ``numpy`` dice. Same seed,
same sequence of dwells.
"""
from __future__ import annotations

import random
from typing import Mapping, Protocol

# The run seed is XOR-ed with this constant to seed the timing stream. XOR is a
# bijection, so distinct runs keep distinct timing streams, and the timing seed can
# never coincide with the run seed the token sampler uses — the two streams are
# always separately seeded, which is the isolation SIM-05 needs. The constant is
# ASCII "TIME"; any fixed non-zero value would do, and it is fixed rather than
# derived so a seed reproduces its dwells forever.
TIMING_STREAM_XOR = 0x54494D45


def derive_timing_seed(seed: int) -> int:
    """The run seed's timing-stream counterpart — pure, so a run is reproducible."""
    return int(seed) ^ TIMING_STREAM_XOR


class TimingSource(Protocol):
    """Supplies the simulated time a tactic's place consumes. Whoever holds one
    calls ``draw`` once per place visit and yields the result to the event loop."""

    def draw(self, tactic: str) -> float: ...


class TacticTiming:
    """The S3 regime: each tactic's declared duration is an exponential mean.

    ``means`` is the duration catalogue read as ``tactic -> mean dwell`` (simulated
    seconds). A tactic whose mean is zero or which is absent from the catalogue
    fires immediately and consumes no draw, so adding zero-duration places to a net
    cannot shift another run's dwell sequence.
    """

    def __init__(self, means: Mapping[str, float], *, seed: int = 0) -> None:
        self._means = {t: float(v) for t, v in means.items()}
        self._rng = random.Random(derive_timing_seed(seed))

    def mean_for(self, tactic: str) -> float:
        """The declared mean for a tactic — zero if it is immediate or unknown."""
        return max(0.0, self._means.get(tactic, 0.0))

    def draw(self, tactic: str) -> float:
        mean = self.mean_for(tactic)
        if mean <= 0.0:
            return 0.0  # an immediate transition: no time, and no draw consumed
        return self._rng.expovariate(1.0 / mean)


class ConstantTiming:
    """The pre-S3 regime — the catalogue value consumed as a fixed dwell.

    Kept as the **comparison arm** the S3 verification needs, not as a run
    configuration: swapping it in isolates the distribution change from everything
    else, which is how the tests show that introducing the draws leaves the token
    sampler's and the substrate's own draw sequences untouched, and how the
    comparability check reads the elapsed-time shift the regime causes. It is also
    the rollback: restoring the constant dwell is swapping the default back.
    """

    def __init__(self, means: Mapping[str, float], *, seed: int = 0) -> None:
        self._means = {t: float(v) for t, v in means.items()}

    def mean_for(self, tactic: str) -> float:
        return max(0.0, self._means.get(tactic, 0.0))

    def draw(self, tactic: str) -> float:
        return self.mean_for(tactic)


__all__ = [
    "TIMING_STREAM_XOR",
    "derive_timing_seed",
    "TimingSource",
    "TacticTiming",
    "ConstantTiming",
]
