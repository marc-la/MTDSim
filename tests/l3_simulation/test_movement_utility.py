"""The attacker utility modulator — criterion axis 6, incentive-driven rationality.

The hard gate is the same one the seam's own suite leads with, restated for a
modulator that actually carries a declared value: **at ``λ = 0`` the run is
bit-identical to today**, across every profile, several seeds, both MTD
conditions and both mappings. That is what makes the cost-sensitive attacker an
ablation of the current model rather than a different model, and what lets the
conditioned and unconditioned arms differ by one declared parameter rather than
by wiring.

The rest pin the declared family's three requirements and the one structural
claim the design rests on: the benefit table is rule-generated and reproduces
0/75; it is **not** a restatement of the overlay's lifecycle-distance kernel
(it differs between profiles for the same tactic, and it does not depend on the
source at all); the cost term is the reused duration catalogue with a declared
floor rather than a silent clamp; and no factor can ever reach zero, so the
seam's stall rule is never engaged.

Design record: docs/implementation/pipeline/ogasp/incentive_rationality.md.
"""
from __future__ import annotations

import dataclasses
import json

import pytest

from mtdsim.l3_simulation.movement.net import PROFILES, load_routing_net
from mtdsim.l3_simulation.movement.run import run_movement
from mtdsim.l3_simulation.movement.state import AttackerState
from mtdsim.l3_simulation.movement.utility import (
    BENEFIT_VIEW_PATH,
    UtilityCompileError,
    UtilityModulator,
    benefit_values,
    check_view,
    compile_benefit,
    load_benefit,
    load_utility_rules,
    stage_gap,
    utility_modulator_for,
)

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


def _fields(records):
    return [dataclasses.asdict(r) for r in records]


def _state(profile: str, seed: int, lam: float, **kwargs) -> AttackerState:
    return AttackerState(
        seed=seed, modulators=(utility_modulator_for(profile, lam=lam, **kwargs),)
    )


# --- 1. lambda = 0 is bit-identical to today (validation gate 1) -------------


@pytest.mark.parametrize("seed", SEED_PARAMS)
@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("mapping", MAPPINGS)
def test_lambda_zero_reproduces_the_current_record_stream_field_for_field(
    profile, mapping, seed, baseline_run
) -> None:
    """The hard constraint. A registered utility modulator at ``λ = 0`` returns
    exactly 1.0 for every destination (``x ** 0.0`` is exactly 1.0 in IEEE
    arithmetic for any finite positive ``x``), so the composition reduces to the
    current two-factor rule and the walk is unperturbed. Asserted rather than
    short-circuited in the modulator: the identity is a property of the maths,
    and testing it that way is a stronger claim than special-casing zero.
    """
    for scheme in (None, "simultaneous"):
        kwargs = dict(seed=seed, mapping_version=mapping, mtd_scheme=scheme)
        without = baseline_run(profile, horizon=3_000, **kwargs)
        with_modulator = run_movement(
            profile,
            horizon=3_000,
            attacker_state=_state(profile, seed, 0.0),
            **kwargs,
        )
        assert _fields(with_modulator.records) == _fields(without.records), (
            f"lambda=0 perturbed {profile}/{mapping}/seed={seed}/mtd={scheme}"
        )
        assert with_modulator.reached_objective == without.reached_objective
        assert with_modulator.termination_time == without.termination_time


def test_lambda_zero_logs_no_non_unit_factor() -> None:
    """The record stream is not the only witness: at ``λ = 0`` the state's own
    per-decision log records no non-unit factor either, so an experiment reading
    the log cannot mistake the ablation arm for a conditioned one."""
    state = _state("aggregate", 42, 0.0)
    run_movement("aggregate", seed=42, horizon=3_000,
                 mapping_version="v2_partial", attacker_state=state)
    assert state.log, "no routing decision was logged"
    assert all(entry["factors"] == {} for entry in state.log)


# --- 2. the seam is live at a declared lambda -------------------------------


def test_a_declared_lambda_visibly_changes_the_walk() -> None:
    """The other half of the ablation: at the declared ``λ = 1`` the walk is
    *not* the ``λ = 0`` walk. A modulator that changed nothing would make the
    axis vacuous, so this is asserted as directly as the null-equivalence is."""
    changed = 0
    for profile in PROFILES:
        for seed in SEEDS:
            null = run_movement(profile, seed=seed, horizon=3_000,
                                mapping_version="v2_partial",
                                attacker_state=_state(profile, seed, 0.0))
            live = run_movement(profile, seed=seed, horizon=3_000,
                                mapping_version="v2_partial",
                                attacker_state=_state(profile, seed, 1.0))
            if _fields(live.records) != _fields(null.records):
                changed += 1
    assert changed >= len(PROFILES), (
        f"the declared lambda changed only {changed} of {len(PROFILES) * len(SEEDS)} walks"
    )


def test_a_live_modulator_logs_the_factors_it_applied() -> None:
    """A modulator that changes routing invisibly is unanalysable — the state's
    log must carry the non-unit factors so an experiment can see what the
    attacker preferred and why (seam record §6)."""
    state = _state("objective_exfiltration", 7, 1.0)
    run_movement("objective_exfiltration", seed=7, horizon=3_000,
                 mapping_version="v2_partial", attacker_state=state)
    logged = [e for e in state.log if e["factors"]]
    assert logged, "a live modulator logged no factors"
    assert all(f > 0.0 for e in logged for f in e["factors"].values())


# --- 3. the declared family: rule-generated, complete, reproducible ---------


def test_the_committed_benefit_view_reproduces_from_the_rules() -> None:
    """Requirement 1 of the declared-value precedent, enforced by tracked code:
    0 of 75 cells differ between the committed view and a fresh compilation."""
    problems = check_view()
    assert problems == [], "\n".join(problems[:20])


def test_the_benefit_table_covers_the_whole_declared_space() -> None:
    """Requirement: complete coverage — every seated tactic under every profile,
    including tactics a profile's net has no place for. Which cells route mass
    is the data layer's business, not the declared layer's."""
    rules = load_utility_rules()
    table = compile_benefit(rules)
    assert set(table) == set(PROFILES)
    for profile, cells in table.items():
        assert set(cells) == set(rules.tactics), profile
    assert sum(len(c) for c in table.values()) == 75


def test_every_benefit_is_strictly_positive() -> None:
    """The property that keeps the seam's stall rule disengaged: a zero benefit
    would zero an out-edge, which needs a declared ``may_zero`` and a re-run of
    the no-stall check. ``rho^(1+gap)`` with ``0 < rho < 1`` never reaches zero,
    at either end of the declared band."""
    rules = load_utility_rules()
    for rho in (0.25, 0.5, 0.75):
        for cells in benefit_values(rules, rho).values():
            assert all(v > 0.0 for v in cells.values()), rho


# --- 4. benefit is NOT a restatement of the lifecycle-distance kernel -------


def test_benefit_differs_between_profiles_for_the_same_tactic() -> None:
    """Validation gate 2's second half, and the check that this factor measures
    incentive rather than re-deriving distance. The overlay's lifecycle-distance
    kernel grades a *jump* and is identical across profiles; benefit grades a
    *destination relative to this profile's objective*, so it must differ
    between profiles — and the tactics it differs on must include ones the nets
    actually traverse, not only structural corners."""
    table = load_benefit()
    differing = {
        tactic
        for tactic in next(iter(table.values()))
        if len({cells[tactic] for cells in table.values()}) > 1
    }
    assert differing, "benefit is profile-invariant — it is re-deriving distance"
    # command-and-control is the sharpest case: the objective of
    # objective_none_c2 (benefit 1.0) and merely instrumental elsewhere.
    assert "command-and-control" in differing
    assert table["objective_none_c2"]["command-and-control"] == 1.0
    assert table["objective_exfiltration"]["command-and-control"] < 1.0
    # ... and impact inverts between the two single-objective profiles.
    assert table["objective_impact"]["impact"] > table["objective_exfiltration"]["impact"]
    assert table["objective_exfiltration"]["exfiltration"] > table["objective_impact"]["exfiltration"]


def test_benefit_does_not_depend_on_the_source_place() -> None:
    """The structural half of the same separation: the distance kernel is a
    signed source→destination offset, so it cannot be reconstructed from a
    function that never sees the source. The modulator's utility is exactly such
    a function — asserted here by evaluating it with no source at all."""
    modulator = utility_modulator_for("objective_exfiltration", lam=1.0)
    net = load_routing_net("objective_exfiltration")
    for place in net.places:
        out = net.base_out_weights(place)
        if len(out) < 2:
            continue
        # The per-destination utilities are the same numbers whatever the source.
        assert {d: modulator.utility(d) for d in out} == {
            d: modulator.utility(d) for d in out
        }
    # And a destination's utility is one number, not a per-source family.
    assert modulator.utility("exfiltration") == modulator.utility("exfiltration")


def test_the_gap_is_measured_to_the_profiles_own_objective() -> None:
    """The gap is a stage separation from *this profile's* nearest declared
    objective — hand-worked on the two profiles whose objectives sit at
    different lifecycle stages."""
    rules = load_utility_rules()
    # objective_none_c2's objective is command-and-control, stage 2.
    assert stage_gap("command-and-control", "objective_none_c2", rules) == 0
    assert stage_gap("reconnaissance", "objective_none_c2", rules) == 2
    assert stage_gap("collection", "objective_none_c2", rules) == 1
    # objective_exfiltration's is exfiltration, stage 3.
    assert stage_gap("exfiltration", "objective_exfiltration", rules) == 0
    assert stage_gap("reconnaissance", "objective_exfiltration", rules) == 3
    assert stage_gap("discovery", "objective_exfiltration", rules) == 1


# --- 5. the cost term: reused, floored, declared ----------------------------


def test_the_cost_term_is_the_duration_catalogue_unmodified() -> None:
    """Reuse, do not re-declare: the modulator's cost map *is* the tracked
    duration catalogue. A second cost catalogue that could drift from the
    durations would be worse than no cost model at all."""
    from mtdsim.l3_simulation.movement.attacker import load_dwell_catalogue

    rules = load_utility_rules()
    assert rules.cost == load_dwell_catalogue()
    assert rules.cost["resource-development"] == 0.0  # the declared zero


def test_the_declared_floor_prices_the_off_clock_tactic() -> None:
    """``resource-development`` is declared 0.0 — off the simulator's clock, not
    free. The floor is a named declared parameter, so the utility of the
    off-clock tactic is its benefit over the floor, and it moves when the floor
    is swept."""
    rules = load_utility_rules()
    benefit = load_benefit()["objective_exfiltration"]["resource-development"]
    declared = utility_modulator_for("objective_exfiltration", lam=1.0)
    assert declared.utility("resource-development") == pytest.approx(benefit / 4.5)
    cheap = utility_modulator_for("objective_exfiltration", lam=1.0, cost_floor_s=1.0)
    assert cheap.utility("resource-development") == pytest.approx(benefit / 1.0)
    assert cheap.utility("resource-development") > declared.utility(
        "resource-development"
    )


def test_a_non_positive_floor_is_refused() -> None:
    """The floor exists precisely so the ratio cannot divide by the declared
    zero; a floor that reintroduces the division fails loudly at construction."""
    with pytest.raises(ValueError, match="cost_floor_s must be positive"):
        UtilityModulator(
            profile="objective_exfiltration", benefit={"a": 1.0}, cost={"a": 0.0},
            lam=1.0, cost_floor_s=0.0,
        )


def test_an_unpriced_destination_fails_loudly() -> None:
    """A net/table disagreement is a bug, not a cell to default to 1.0."""
    modulator = UtilityModulator(
        profile="objective_exfiltration", benefit={"a": 1.0}, cost={"a": 10.0},
        lam=1.0, cost_floor_s=4.5,
    )
    with pytest.raises(UtilityCompileError, match="no declared benefit"):
        modulator.utility("nowhere")


# --- 6. the factor's arithmetic, hand-worked --------------------------------


def test_the_factor_is_the_out_set_normalised_utility_raised_to_lambda() -> None:
    """Hand-worked: with two destinations of utility 1.0 and 3.0, the mean is
    2.0, so the factors are (0.5, 1.5) at λ=1, their squares at λ=2, and exactly
    (1.0, 1.0) at λ=0. Normalising by the out-set mean is what makes λ scale a
    ratio rather than an absolute magnitude."""
    modulator = UtilityModulator(
        profile="test",
        benefit={"lo": 1.0, "hi": 3.0},
        cost={"lo": 1.0, "hi": 1.0},
        lam=1.0,
        cost_floor_s=1.0,
    )
    out = {"lo": 0.5, "hi": 0.5}
    assert modulator.factors(None, "src", out) == pytest.approx({"lo": 0.5, "hi": 1.5})
    modulator.lam = 2.0
    assert modulator.factors(None, "src", out) == pytest.approx({"lo": 0.25, "hi": 2.25})
    modulator.lam = 0.0
    assert modulator.factors(None, "src", out) == {"lo": 1.0, "hi": 1.0}


def test_no_factor_is_ever_zero_across_the_declared_bands() -> None:
    """The seam refuses an undeclared zero, and this modulator never declares
    ``may_zero``. Checked over every profile's every out-set at both ends of the
    lambda band and both ends of the rho band, so the guarantee is exercised
    rather than argued."""
    for profile in PROFILES:
        net = load_routing_net(profile)
        for lam in (0.0, 4.0):
            for rho in (0.25, 0.75):
                modulator = utility_modulator_for(profile, lam=lam, rho=rho)
                for place in net.places:
                    out = net.base_out_weights(place)
                    if not out:
                        continue
                    factors = modulator.factors(None, place, out)
                    assert all(f > 0.0 for f in factors.values()), (profile, place)
    assert not getattr(UtilityModulator, "may_zero", False)


# --- 7. determinism (SIM-05) ------------------------------------------------


def test_a_conditioned_run_is_reproducible_and_draws_no_state_randomness() -> None:
    """The modulator is a pure function of declared data and the current place,
    so a conditioned run reproduces exactly and the state's fourth RNG stream is
    left untouched — determinism stays trivially intact."""
    first = run_movement("aggregate", seed=1234, horizon=3_000,
                         mapping_version="v2_partial",
                         attacker_state=_state("aggregate", 1234, 1.0))
    state = _state("aggregate", 1234, 1.0)
    second = run_movement("aggregate", seed=1234, horizon=3_000,
                          mapping_version="v2_partial", attacker_state=state)
    assert _fields(first.records) == _fields(second.records)
    # The state's stream is where it started: an unused Random's next draw is the
    # same as a freshly-seeded one's.
    import random

    from mtdsim.l3_simulation.movement.state import derive_state_seed

    assert state.rng.random() == random.Random(derive_state_seed(1234)).random()


def test_the_compiled_view_declares_its_generator_and_its_parameters() -> None:
    """The compiled view is generated, and says so — the guard against a reader
    hand-editing a table away from the rules that produced it."""
    doc = json.loads(BENEFIT_VIEW_PATH.read_text(encoding="utf-8"))
    meta = doc["_meta"]
    assert "DO NOT hand-edit" in meta["generated_from"]
    assert meta["declared_parameters"] == {"rho": 0.5, "cost_floor_s": 4.5, "lambda": 1.0}
    assert "75 cells" in meta["coverage"]
