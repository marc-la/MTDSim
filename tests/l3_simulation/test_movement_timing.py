"""The per-tactic timing source, tested as a distribution before it is wired.

The S3 regime turns each declared per-tactic duration into the *mean* of an
exponential firing time. That is a statistical claim, so it is tested
statistically and in isolation — over many seeded draws, away from the walk —
because a bug in the draw would otherwise hide behind an integration bug in the
loop (design record §6/§7; implementation handoff, recommended approach step 1).

Four properties are pinned here:

1. **The declared mean is recovered** — per group anchor, over many draws.
2. **It is genuinely exponential**, not a constant wearing a mean: the
   coefficient of variation is 1 and the median sits at ``mean × ln 2``.
3. **Determinism (SIM-05)** — a seed reproduces its sequence exactly, and the
   stream is the timing source's own: interleaved global draws cannot move it.
4. **A zero mean stays immediate** — no time, and no draw consumed, so adding a
   zero-duration place cannot shift another run's dwell sequence.
"""
from __future__ import annotations

import math
import random
import statistics

import pytest

from mtdsim.l3_simulation.movement.attacker import load_dwell_catalogue
from mtdsim.l3_simulation.movement.timing import (
    TIMING_STREAM_XOR,
    ConstantTiming,
    TacticTiming,
    derive_timing_seed,
)

# The four declared group anchors (data/ogasp/tactic_durations.json), one
# representative tactic each, plus the immediate off-network null.
ANCHOR_TACTICS = {
    "reconnaissance": 35.0,  # scan-shaped
    "initial-access": 4.5,  # exploit-shaped
    "stealth": 45.0,  # stealth-low-and-slow
    "collection": 36.0,  # objective-execution
}

N_DRAWS = 40_000
# The standard error of the mean of n exponential draws is mean/sqrt(n), so at
# n = 40 000 a 2 % band is ~4 standard errors — tight enough to catch a wrong
# rate parameterisation (a 1/mean-vs-mean inversion is orders out), loose enough
# never to flake.
MEAN_TOLERANCE = 0.02


def _draws(tactic: str, mean: float, n: int = N_DRAWS, seed: int = 0) -> list[float]:
    timing = TacticTiming({tactic: mean}, seed=seed)
    return [timing.draw(tactic) for _ in range(n)]


# --- 1. the declared mean is recovered -------------------------------------


@pytest.mark.parametrize("tactic, mean", sorted(ANCHOR_TACTICS.items()))
def test_the_empirical_mean_recovers_the_declared_mean(tactic: str, mean: float) -> None:
    """The load-bearing property: the catalogue value is the distribution's mean.

    Every tier badge, sweep band and group anchor in the catalogue was declared
    about a *value*; S3 keeps those values and re-reads them as means, so if the
    draw did not centre on the declared value the whole validity framework would
    be describing a distribution it never sanctioned.
    """
    empirical = statistics.fmean(_draws(tactic, mean))
    assert empirical == pytest.approx(mean, rel=MEAN_TOLERANCE), (
        f"{tactic}: drew mean {empirical:.3f} against a declared mean of {mean}"
    )


def test_the_catalogue_is_read_as_means_verbatim() -> None:
    """The regime change is semantic, not numeric: the magnitudes the timing source
    centres on are the committed catalogue's own values, unmodified."""
    catalogue = load_dwell_catalogue()
    timing = TacticTiming(catalogue, seed=0)
    for tactic, declared in catalogue.items():
        assert timing.mean_for(tactic) == declared


# --- 2. it is genuinely exponential ----------------------------------------


def test_the_draw_is_exponential_not_a_constant() -> None:
    """An exponential has a coefficient of variation of exactly 1 and a median of
    ``mean × ln 2`` — both well away from a constant dwell (CV 0, median = mean).
    Without this a draw that merely returned the mean would pass the mean test."""
    mean = 45.0
    sample = _draws("stealth", mean)

    cv = statistics.stdev(sample) / statistics.fmean(sample)
    assert cv == pytest.approx(1.0, rel=0.05), f"coefficient of variation {cv:.3f}"

    median = statistics.median(sample)
    assert median == pytest.approx(mean * math.log(2), rel=0.05)


def test_the_mode_at_zero_and_the_long_tail_are_both_present() -> None:
    """The two consequences of memorylessness the design record names honestly: the
    single most probable dwell is near zero, and a small fraction of dwells run
    several times the declared mean. Pinning them keeps the regime's known shape
    weakness visible in the test suite rather than only in prose."""
    mean = 35.0
    sample = _draws("reconnaissance", mean)

    below_mean = sum(1 for x in sample if x < mean) / len(sample)
    assert below_mean == pytest.approx(1 - 1 / math.e, abs=0.02)

    beyond_triple = sum(1 for x in sample if x > 3 * mean) / len(sample)
    assert beyond_triple == pytest.approx(math.exp(-3), abs=0.01)


# --- 3. determinism and stream isolation ------------------------------------


def test_the_same_seed_reproduces_the_same_sequence_exactly() -> None:
    """SIM-05 at the source: identical seeds, identical dwells, element for
    element — not merely the same distribution."""
    first = _draws("stealth", 45.0, n=500, seed=1234)
    second = _draws("stealth", 45.0, n=500, seed=1234)
    assert first == second


def test_different_seeds_give_different_sequences() -> None:
    assert _draws("stealth", 45.0, n=500, seed=0) != _draws(
        "stealth", 45.0, n=500, seed=1
    )


def test_the_stream_is_its_own_and_the_global_dice_cannot_move_it() -> None:
    """The timing stream neither reads nor is read by the substrate's global
    ``random`` — the substrate draws its own dice constantly, and if the timing
    source shared them a run's dwells would depend on how many verbs happened to
    fire beforehand, which is not a reproducible function of the seed."""
    timing = TacticTiming({"stealth": 45.0}, seed=7)
    undisturbed = [timing.draw("stealth") for _ in range(200)]

    timing = TacticTiming({"stealth": 45.0}, seed=7)
    disturbed = []
    for _ in range(200):
        random.random()  # the substrate, drawing between two tactic dwells
        disturbed.append(timing.draw("stealth"))

    assert undisturbed == disturbed


def test_the_timing_seed_is_a_pure_transform_and_never_the_run_seed() -> None:
    """The derived seed keeps the timing stream separately seeded from the token
    sampler's ``Random(seed)`` for every run seed (XOR with a non-zero constant is
    a bijection with no fixed point), and is pure so a seed reproduces forever."""
    assert TIMING_STREAM_XOR != 0
    for seed in (0, 1, 7, 42, 1234, 2**31 - 1):
        assert derive_timing_seed(seed) != seed
        assert derive_timing_seed(seed) == derive_timing_seed(seed)
    seeds = (0, 1, 7, 42, 1234)
    assert len({derive_timing_seed(s) for s in seeds}) == len(seeds)


# --- 4. a zero mean stays immediate -----------------------------------------


def test_a_zero_duration_tactic_is_immediate_and_consumes_no_draw() -> None:
    """``resource-development`` is the off-network prep null: an exponential of
    mean zero is degenerate, so a zero-duration place is a GSPN *immediate*
    transition instead. It must also consume no draw, or the number of
    zero-duration places a net happens to contain would perturb every later dwell.
    """
    timing = TacticTiming({"resource-development": 0.0, "stealth": 45.0}, seed=3)
    reference = TacticTiming({"stealth": 45.0}, seed=3)

    assert timing.draw("resource-development") == 0.0
    assert timing.draw("stealth") == reference.draw("stealth")


def test_an_unknown_tactic_is_immediate() -> None:
    """A place with no catalogue entry costs nothing rather than raising: the
    catalogue's key set is guarded separately (``test_durations.py``), and a walk
    is not the place to discover a missing row."""
    assert TacticTiming({}, seed=0).draw("not-a-tactic") == 0.0


# --- the comparison arm ------------------------------------------------------


def test_constant_timing_reproduces_the_pre_s3_regime() -> None:
    """The rollback and comparison arm: the catalogue value, consumed whole, with
    no randomness at all. The tests that isolate the regime change swap this in."""
    catalogue = load_dwell_catalogue()
    constant = ConstantTiming(catalogue, seed=0)
    for tactic, declared in catalogue.items():
        assert constant.draw(tactic) == declared
        assert constant.draw(tactic) == declared  # no stream, so no drift


# --- the regime inside the walk ---------------------------------------------
#
# The properties above are the draw's; these are the loop's. They are the ones
# that would fail if the timing source were built correctly and then wired at the
# wrong place — the failure mode the design record's "one seam" instruction and
# the handoff's build-then-wire ordering exist to prevent.


@pytest.fixture(scope="module")
def clean_run():
    """One no-MTD walk at full horizon: nothing can cut a dwell short, so every
    recorded dwell is exactly the value drawn for that visit."""
    from mtdsim.l3_simulation.movement.run import run_movement

    return run_movement(
        "aggregate", seed=42, with_synthetic_overlay=True, horizon=15_000,
        mtd_scheme=None,
    )


def test_the_walk_draws_a_fresh_dwell_at_every_visit(clean_run) -> None:
    """The regime landed where it is measured: repeated visits to the same place
    cost different amounts of time. Under the old regime every visit to a place
    cost the identical catalogue constant."""
    by_place: dict[str, set[float]] = {}
    for r in clean_run.records:
        if r.dwell > 0:
            by_place.setdefault(r.place, set()).add(r.dwell)
    revisited = {p: v for p, v in by_place.items() if len(v) > 1}
    assert revisited, "no place was visited twice with a positive dwell"
    for place, values in revisited.items():
        assert len(values) > 1, f"{place} charged an identical dwell every visit"


def test_the_dwells_in_a_run_recover_the_declared_means() -> None:
    """End to end, the walk's dwells centre on the catalogue's declared values —
    the property that keeps the tier badges and sweep bands meaningful after the
    regime change, and the one that would break if a mean were wired to the wrong
    place.

    Pooled over several seeds, because one walk visits no single place often
    enough for its mean to be informative. The pooled statistic normalises each
    dwell by its own declared mean, so every place contributes to one sample whose
    expectation is exactly 1 regardless of which tactic it came from; the
    per-place check then catches a single mis-wired tactic that the pooled figure
    could average away.
    """
    from mtdsim.l3_simulation.movement.run import run_movement

    catalogue = load_dwell_catalogue()
    samples: dict[str, list[float]] = {}
    for seed in (0, 7, 42, 1234):
        res = run_movement(
            "aggregate", seed=seed, with_synthetic_overlay=True, horizon=15_000,
            mtd_scheme=None,
        )
        for r in res.records:
            if r.dwell > 0 and not r.interrupted:
                samples.setdefault(r.place, []).append(r.dwell)

    normalised = [d / catalogue[p] for p, values in samples.items() for d in values]
    assert len(normalised) > 1_000, "too few dwells pooled to judge the mean"
    assert statistics.fmean(normalised) == pytest.approx(1.0, rel=0.05), (
        f"pooled dwells averaged {statistics.fmean(normalised):.4f} of their "
        f"declared means over {len(normalised)} draws"
    )

    checked = 0
    for place, values in samples.items():
        if len(values) < 100:
            continue
        checked += 1
        declared = catalogue[place]
        # At n >= 100 the standard error is a tenth of the mean, so a 30 % band is
        # ~3 standard errors: tight enough to catch a wrong mean, wide enough never
        # to flake. The distribution itself is pinned tightly by the draw tests.
        assert statistics.fmean(values) == pytest.approx(declared, rel=0.30), (
            f"{place}: {len(values)} dwells averaged "
            f"{statistics.fmean(values):.2f} against a declared {declared}"
        )
    assert checked >= 5, "too few places were visited often enough to check"


def test_dwell_only_places_draw_their_time_like_any_other(clean_run) -> None:
    """A dwell-only tactic dispatches nothing, so its dwell is its *entire* cost —
    which makes it the place where the timing regime matters most. It draws from
    the same source as an action-bearing place: time passes, and it varies.
    """
    from mtdsim.l3_simulation.movement.run import run_movement

    res = run_movement(
        "aggregate", seed=1234, with_synthetic_overlay=True, horizon=15_000,
        mapping_version="v2_partial", mtd_scheme=None,
    )
    dwell_only = [
        r for r in res.records if r.place_class == "dwell-only" and r.dwell > 0
    ]
    assert dwell_only, "the walk reached no dwell-only place with a positive dwell"

    for r in dwell_only:
        assert r.verb == ""
        assert r.verdict == ""
        # No verb ran, so the event occupied exactly its drawn dwell.
        assert r.end_time - r.start_time == pytest.approx(r.dwell)

    assert len({r.dwell for r in dwell_only}) > 1, (
        "every dwell-only visit cost the same — the draw is not reaching them"
    )


def test_introducing_the_draws_leaves_the_other_streams_untouched() -> None:
    """RNG isolation (design record §6, test 3), asserted where it is falsifiable.

    Timing draws must neither read nor advance the token sampler's stream or the
    substrate's global dice. Under no MTD nothing in the simulation reads the
    clock to decide an outcome, so switching the timing regime may change *when*
    events happen but must not change *what* happens: the same places, verbs,
    outcomes, verdicts and routing decisions, in the same order. Any leak into a
    shared stream would reorder that sequence immediately.

    The two arms end at different clock positions, so the horizon censors them at
    different points — the shared prefix is the whole of the comparison.
    """
    from mtdsim.l3_simulation.movement.run import run_movement

    def walk(timing):
        return run_movement(
            "aggregate", seed=42, with_synthetic_overlay=True, horizon=15_000,
            mtd_scheme=None, timing=timing,
        ).records

    catalogue = load_dwell_catalogue()
    drawn = walk(None)  # the declared S3 regime
    constant = walk(ConstantTiming(catalogue))  # the pre-S3 regime

    def decisions(records):
        return [
            (r.place, r.verb, r.outcome, r.verdict, r.blocked, r.next_place)
            for r in records
        ]

    a, b = decisions(drawn), decisions(constant)
    shared = min(len(a), len(b))
    assert shared > 50, "too few events to compare the two regimes meaningfully"
    assert a[:shared] == b[:shared], (
        "changing the timing regime changed the walk's decisions, so the timing "
        "draws are perturbing the sampler or the substrate dice"
    )

def test_the_substrate_contributes_no_attacker_time() -> None:
    """The movement layer owns every unit of the attacker's time (S3-R).

    An event's whole elapsed time is the tactic's draw, so the residual — what the
    substrate would have charged for the verb — is zero. This is the assertion
    that would fail if any native ``ATTACK_DURATION`` or ``exploit_time`` charge
    crept back onto this arm, which is exactly the hybrid the ruling retired.

    Restricted to a no-MTD run, where nothing can cut an event short or add a
    confusion penalty on top.
    """
    from mtdsim.l3_simulation.movement.run import run_movement

    res = run_movement(
        "aggregate", seed=42, with_synthetic_overlay=True, horizon=15_000,
        mtd_scheme=None,
    )
    acting = [
        r for r in res.records
        if r.verb and r.outcome not in {"SIM_END", "MAX_EVENTS"}
    ]
    assert acting, "no dispatched actions to check"
    for r in acting:
        residual = (r.end_time - r.start_time) - r.dwell
        assert residual == pytest.approx(0.0, abs=1e-6), (
            f"{r.verb} at {r.place} cost {residual} beyond its tactic's time — "
            f"the substrate is still pricing the action"
        )


def test_one_verb_costs_different_amounts_under_different_tactics() -> None:
    """The intended consequence of the mapping being many-to-one: because the
    price belongs to the tactic rather than to the verb, the same verb invoked
    from two tactics with different declared durations takes different times.

    Compared as means over many visits, since each individual draw is random —
    what must differ is the tactics' central tendencies, not two single draws.
    """
    from mtdsim.l3_simulation.movement.run import run_movement

    catalogue = load_dwell_catalogue()
    by_verb_place: dict[tuple[str, str], list[float]] = {}
    for seed in (0, 7, 42, 1234):
        res = run_movement(
            "aggregate", seed=seed, with_synthetic_overlay=True, horizon=15_000,
            mtd_scheme=None,
        )
        for r in res.records:
            if r.verb and not r.interrupted and r.dwell > 0:
                by_verb_place.setdefault((r.verb, r.place), []).append(r.dwell)

    # Find a verb reached from two tactics whose declared durations differ.
    verbs: dict[str, list[str]] = {}
    for (verb, place), values in by_verb_place.items():
        if len(values) >= 30:
            verbs.setdefault(verb, []).append(place)

    compared = 0
    for verb, places in verbs.items():
        for i, first in enumerate(places):
            for second in places[i + 1:]:
                slow, fast = sorted(
                    (first, second), key=lambda p: catalogue[p], reverse=True
                )
                # Only compare tactics whose declared durations are separated by at
                # least a factor of two. An exponential has a coefficient of
                # variation of one, so a sample of this size carries a standard
                # error near a fifth of its mean; two tactics declared a few seconds
                # apart cannot be told apart at this sample size, and asserting they
                # can would be a flaky test rather than a stronger one.
                if catalogue[fast] <= 0 or catalogue[slow] < 2 * catalogue[fast]:
                    continue
                compared += 1
                mean_slow = statistics.fmean(by_verb_place[(verb, slow)])
                mean_fast = statistics.fmean(by_verb_place[(verb, fast)])
                assert mean_slow > mean_fast, (
                    f"{verb} averaged {mean_slow:.1f} from {slow} (declared "
                    f"{catalogue[slow]}) but {mean_fast:.1f} from {fast} (declared "
                    f"{catalogue[fast]}) — the tactic is not pricing the action"
                )
    assert compared, (
        "no verb was reached from two tactics whose declared durations differ "
        "by the factor of two this comparison needs"
    )


def test_a_blocked_attempt_still_costs_its_tactics_time() -> None:
    """An action the substrate cannot run from its current state still consumes
    the tactic's time: the attacker committed the procedure that tactic represents
    and it came to nothing.

    Without this a place whose precondition is unmet is a free move, and the
    profiles that block most — the blocked fraction runs to ~100% on some — would
    churn the net at no cost, which is the opposite of what the H-coupling finding
    should show.
    """
    from mtdsim.l3_simulation.movement.run import run_movement

    res = run_movement(
        "aggregate", seed=42, with_synthetic_overlay=True, horizon=15_000,
        mtd_scheme=None,
    )
    blocked = [r for r in res.records if r.blocked and not r.interrupted]
    assert blocked, "no blocked attempt was observed"

    catalogue = load_dwell_catalogue()
    for r in blocked:
        if catalogue[r.place] == 0:
            continue
        assert r.dwell > 0, f"blocked attempt at {r.place} cost nothing"
        assert r.end_time - r.start_time == pytest.approx(r.dwell)

    charged = [r.dwell / catalogue[r.place] for r in blocked if catalogue[r.place] > 0]
    assert statistics.fmean(charged) == pytest.approx(1.0, rel=0.25), (
        "blocked attempts are not being charged their tactic's declared mean"
    )


def test_the_regime_is_deterministic_end_to_end() -> None:
    """SIM-05 through the whole loop with the new stream in place: same seed, same
    walk, dwells included."""
    from mtdsim.l3_simulation.movement.run import run_movement

    def walk():
        return run_movement(
            "aggregate", seed=7, with_synthetic_overlay=True, horizon=3_000,
            mtd_scheme="simultaneous", mtd_interval=150,
        ).records

    first, second = walk(), walk()
    assert first == second
    assert [r.dwell for r in first] == [r.dwell for r in second]


def test_the_walks_whole_elapsed_time_is_accounted_for_by_the_movement_layer() -> None:
    """The point of S3-R, stated as an accounting identity: the run's elapsed time
    is the sum of the tactic times the movement layer supplied, plus the confusion
    penalties the substrate charged for MTD interrupts — and nothing else.

    Any third contributor would show up as an unexplained remainder, which is what
    the retired hybrid's native action costs were.
    """
    from mtdsim.l3_simulation.movement.run import run_movement

    res = run_movement(
        "aggregate", seed=42, with_synthetic_overlay=True, horizon=15_000,
        mtd_scheme=None,
    )
    records = [r for r in res.records if r.outcome not in {"SIM_END", "MAX_EVENTS"}]
    assert records

    supplied = sum(r.dwell for r in records)
    assert supplied > 0
    # No MTD, so no penalties: elapsed time is exactly what the movement layer
    # supplied, with no remainder for the substrate.
    elapsed = records[-1].end_time - records[0].start_time
    assert elapsed == pytest.approx(supplied, rel=1e-6)
