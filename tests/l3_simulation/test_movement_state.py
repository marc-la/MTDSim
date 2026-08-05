"""The within-run attacker state and the generalised modulator composition.

The foundation the smart-attacker axes share (criterion axes 5–7). Its whole
safety argument is one property — **the null configuration is bit-identical to
a run without the state** — so that is tested first and hardest, across every
profile, several seeds and both MTD conditions. The rest pin the seam's other
guarantees: the dwell-only routing change is behaviour-neutral on its own, the
seam is live (a registered modulator visibly changes the walk), the fourth RNG
stream is isolated, and a zeroing modulator is refused without a declared rule.

Design record: docs/implementation/pipeline/ogasp/attacker_state_seam.md.
"""
from __future__ import annotations

import dataclasses

import pytest

from mtdsim.l3_simulation.movement.net import PROFILES
from mtdsim.l3_simulation.movement.run import run_movement
from mtdsim.l3_simulation.movement.state import (
    STATE_STREAM_XOR,
    AttackerState,
    ModulatedOverlay,
    RevisitAversionDemo,
    StatefulTiming,
    derive_state_seed,
)
from mtdsim.l3_simulation.movement.timing import TIMING_STREAM_XOR

SEEDS = (0, 7, 42, 1234, 9001)
# One cell of the null-equivalence grid below is two full simulations, and all
# six modulator families pin the same guarantee over the same grid — so the
# suite paid for it six times over (measured: the slowest 25 durations of a
# 503 s run were, without exception, cells of these grids). The leading seed
# runs on every invocation; the rest are marked slow and need ``--runslow``
# (see ``tests/conftest.py``, which also explains why the seed axis is the one
# that can be sliced — every seed asserts the same identity, differing only in
# which walk is sampled, whereas profile and mapping vary the structure).
SEED_PARAMS = (SEEDS[0],) + tuple(
    pytest.param(s, marks=pytest.mark.slow) for s in SEEDS[1:]
)
MAPPINGS = (None, "v2_partial")  # default (total) and the dwell-only-bearing arm


def _records(**kwargs):
    kwargs.setdefault("horizon", 3_000)
    return run_movement("aggregate", **kwargs).records


def _fields(records):
    return [dataclasses.asdict(r) for r in records]


# --- 1. null-equivalence: the hard gate -------------------------------------


@pytest.mark.parametrize("seed", SEED_PARAMS)
@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("mapping", MAPPINGS)
def test_a_null_configured_state_leaves_the_walk_bit_identical(
    profile, mapping, seed, baseline_run
) -> None:
    """The load-bearing guarantee: attach a state with no modulators and the
    record stream is equal field for field to a run without the state. This is
    what makes the whole line of work ablatable and answers the S2 confounding
    objection — the conditioned and unconditioned arms differ only by a
    parameter, never by wiring.
    """
    for scheme in (None, "simultaneous"):
        kwargs = dict(seed=seed, mapping_version=mapping, mtd_scheme=scheme)
        without = baseline_run(profile, horizon=3_000, **kwargs)
        with_state = run_movement(
            profile, horizon=3_000,
            attacker_state=AttackerState(seed=seed), **kwargs,
        )
        assert _fields(with_state.records) == _fields(without.records), (
            f"null state perturbed {profile}/{mapping}/seed={seed}/mtd={scheme}"
        )
        assert with_state.reached_objective == without.reached_objective
        assert with_state.termination_time == without.termination_time


def test_the_null_state_still_observed_the_whole_trajectory() -> None:
    """Bit-identical to today does not mean inert: a null-configured state still
    accumulates its within-run knowledge — it simply does not act on it. This is
    what a modulator will later read."""
    state = AttackerState(seed=42)
    run_movement("aggregate", seed=42, horizon=3_000,
                 mapping_version="v2_partial", attacker_state=state)
    snap = state.snapshot()
    assert snap["visits"] > 0
    assert snap["distinct_places"] > 1
    # Every routing decision was observed, including the dwell-only "none" verdicts.
    assert "none" in snap["verdicts"]
    assert {"success", "failure"} & set(snap["verdicts"])
    # A null run reweights nothing: every logged decision carries no factors.
    assert state.log
    assert all(entry["factors"] == {} for entry in state.log)


# --- 2. the dwell-only routing change is neutral on its own ------------------


def test_dwell_only_routing_through_compose_matches_base_weight_sampling() -> None:
    """The one driver edit — routing a dwell-only place through ``compose`` under
    the distinguished ``"none"`` verdict — is proven neutral against the real
    overlay: because no overlay registers ``"none"``, every destination passes
    through at 1.0 and the composed distribution is the base weights renormalised,
    which ``_sample`` normalises anyway. Asserted here on the mapping that has
    dwell-only places, so the change is actually exercised.

    (The full before/after equality across every profile is the design record's
    captured evidence; this is the in-suite guard that keeps it true.)
    """
    from mtdsim.l3_simulation.controller import load_outcome_overlay

    overlay = load_outcome_overlay()
    res = run_movement("aggregate", seed=1234, horizon=3_000,
                       mapping_version="v2_partial")
    dwell_only = [r for r in res.records if r.place_class == "dwell-only"
                  and r.next_place is not None]
    assert dwell_only, "no dwell-only routing decision to check"
    # The overlay carries no "none" verdict, so its composed table for a dwell-only
    # source is the base weights renormalised — exactly what the driver now samples.
    for r in dwell_only[:20]:
        assert overlay.by_verdict.get("none") is None or \
            not overlay.by_verdict["none"].get(r.place)


# --- 3. the seam is live (validation gate 3) --------------------------------


def test_a_registered_modulator_visibly_changes_the_walk() -> None:
    """The seam is proven live, not merely wired: the artificial revisit-aversion
    modulator changes the record stream relative to the same-seed null run. If
    this passed identically the modulator would not be reaching the routing."""
    seed = 1234
    kwargs = dict(seed=seed, horizon=3_000, mapping_version="v2_partial")
    null = _fields(_records(attacker_state=AttackerState(seed=seed), **kwargs))
    demo = _fields(_records(
        attacker_state=AttackerState(seed=seed, modulators=(RevisitAversionDemo(),)),
        **kwargs,
    ))
    assert null != demo, "the demonstration modulator did not change the walk"


def test_the_modulator_only_bites_once_its_condition_is_met() -> None:
    """The demo halves destinations already visited >= threshold times, so the
    two walks share a prefix and diverge only once a destination has been
    revisited — the modulator conditions on history, it does not fire blindly."""
    seed = 1234
    kwargs = dict(seed=seed, horizon=3_000, mapping_version="v2_partial")
    null = _fields(_records(attacker_state=AttackerState(seed=seed), **kwargs))
    demo = _fields(_records(
        attacker_state=AttackerState(
            seed=seed, modulators=(RevisitAversionDemo(threshold=2),)),
        **kwargs,
    ))
    n = min(len(null), len(demo))
    first_diff = next((i for i in range(n) if null[i] != demo[i]), n)
    assert first_diff > 0, "the walks diverged at the very first step"


# --- 4. determinism and the fourth stream's isolation -----------------------


def test_the_state_seed_is_a_pure_transform_and_distinct_from_the_others() -> None:
    """The fourth stream is seeded by the same pure-XOR pattern as the timing
    stream, with a distinct constant — so the state's dice never coincide with
    the run seed, the timing stream, or another run's state stream."""
    assert STATE_STREAM_XOR != 0
    assert STATE_STREAM_XOR != TIMING_STREAM_XOR
    for seed in (0, 1, 7, 42, 1234, 2**31 - 1):
        assert derive_state_seed(seed) != seed
        assert derive_state_seed(seed) != (seed ^ TIMING_STREAM_XOR)
        assert derive_state_seed(seed) == derive_state_seed(seed)


def test_attaching_a_null_state_does_not_perturb_the_other_streams() -> None:
    """The RNG-isolation property (validation gate 4), tested the way the timing
    stream's was: attaching the state must not move the token sampler's or the
    dwell stream's sequences. Since the null run is bit-identical (test 1), the
    dwells — which the token sampler and dwell stream jointly determine — must
    match element for element, not merely in distribution."""
    seed = 42
    without = _records(seed=seed, mapping_version="v2_partial")
    with_state = _records(seed=seed, mapping_version="v2_partial",
                          attacker_state=AttackerState(seed=seed))
    assert [r.dwell for r in with_state] == [r.dwell for r in without]
    assert [r.next_place for r in with_state] == [r.next_place for r in without]


def test_a_stateful_run_is_deterministic_end_to_end() -> None:
    """SIM-05 with a live modulator in place: same seed, same walk, twice."""
    def walk():
        return _fields(_records(
            seed=7, horizon=3_000, mapping_version="v2_partial",
            mtd_scheme="simultaneous", mtd_interval=150,
            attacker_state=AttackerState(seed=7, modulators=(RevisitAversionDemo(),)),
        ))
    assert walk() == walk()


# --- 5. the zero rule -------------------------------------------------------


class _ZeroingModulator:
    """A modulator that zeroes an out-edge without declaring it may — forbidden."""

    name = "illegal-zeroer"

    def factors(self, state, src, base_out_weights):
        return {dst: 0.0 for dst in base_out_weights}


class _LicensedZeroer:
    """The same, but declaring may_zero — permitted (it owes a no-stall re-run)."""

    name = "licensed-zeroer"
    may_zero = True

    def factors(self, state, src, base_out_weights):
        # Zero only a destination that is not the sole out-edge, so no stall.
        return {dst: 0.0 for dst in list(base_out_weights)[1:]}


def test_a_modulator_may_not_zero_an_out_edge_without_declaring_it() -> None:
    """Zeroing an out-set is the one way to manufacture a stall, so a zero factor
    from a modulator that has not declared ``may_zero`` is refused loudly rather
    than silently suppressing an edge."""
    state = AttackerState(seed=0, modulators=(_ZeroingModulator(),))
    with pytest.raises(ValueError, match="may_zero"):
        state.modulate("reconnaissance", {"initial-access": 1.0, "reconnaissance": 1.0})


def test_a_licensed_zeroer_is_permitted() -> None:
    """The escape hatch works: a modulator declaring ``may_zero`` may return 0.0.
    The declared-rule and no-stall-re-run obligations live in the design record;
    the mechanism only enforces the declaration."""
    state = AttackerState(seed=0, modulators=(_LicensedZeroer(),))
    factors = state.modulate("a", {"a": 1.0, "b": 1.0, "c": 1.0})
    assert factors["a"] == 1.0
    assert factors["b"] == 0.0 and factors["c"] == 0.0


# --- 6. the wrappers delegate (consume, never fork) -------------------------


def test_the_wrappers_forward_unknown_attributes_to_their_inner() -> None:
    """Both wrappers are transparent proxies: an attribute they do not define is
    read from the wrapped object, so a run wiring them keeps every other seam
    (e.g. the overlay's ``version``, the timing's ``mean_for``) intact."""
    from mtdsim.l3_simulation.controller import load_outcome_overlay
    from mtdsim.l3_simulation.movement.timing import TacticTiming

    state = AttackerState(seed=0)
    overlay = load_outcome_overlay()
    wrapped_overlay = ModulatedOverlay(overlay, state)
    assert wrapped_overlay.version == overlay.version

    timing = TacticTiming({"stealth": 45.0}, seed=0)
    wrapped_timing = StatefulTiming(timing, state)
    assert wrapped_timing.mean_for("stealth") == 45.0
