"""The within-run learning capability (criterion axis 7).

The hard gate is the same one the seam ships with: **the ablation arm reproduces
today bit for bit**. Everything about the ablation, the S2 argument and the
sweep rests on ``kappa = 0`` being not merely similar but field-for-field
identical to a run with no attacker state at all, so that is tested first,
across every profile, several seeds and both MTD conditions.

The rest pin the rule's own claims: the Laplace prior keeps an unvisited place
at exactly 0.5 and every factor strictly positive (so ``may_zero = False`` is a
proven claim rather than a hopeful one), the belief responds to evidence in the
right direction, the defence degrades it at the declared fraction and at the
declared moment, the learner introduces no new randomness, and the declared
values reproduce from their rules.

Design record: docs/implementation/pipeline/ogasp/learning_capability.md.
"""
from __future__ import annotations

import dataclasses

import pytest

from mtdsim.l3_simulation.movement.learning import (
    LearningModulator,
    check_worked_view,
    load_learning_parameters,
)
from mtdsim.l3_simulation.movement.measures import blocked_fraction_trend
from mtdsim.l3_simulation.movement.net import PROFILES
from mtdsim.l3_simulation.movement.run import run_movement
from mtdsim.l3_simulation.movement.state import AttackerState

SEEDS = (0, 7, 42, 1234, 9001)
MAPPINGS = (None, "v2_partial")  # the default (total) mapping and the partial one


def _fields(records):
    return [dataclasses.asdict(r) for r in records]


def _state(kappa: float, rho: float, seed: int) -> AttackerState:
    return AttackerState(
        seed=seed, modulators=(LearningModulator(kappa=kappa, rho=rho),)
    )


# --- 1. the ablation arm is bit-identical to today (validation gate 1) -------


@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("mapping", MAPPINGS)
def test_kappa_zero_reproduces_the_current_record_stream_field_for_field(
    profile, mapping
) -> None:
    """The load-bearing guarantee, re-checked with *this* modulator attached
    rather than with an empty state. A learner at zero capability observes the
    whole run and acts on none of it, so the walk must be the walk that has
    always run — otherwise the ablation arm is measuring the wiring instead of
    the parameter.
    """
    for seed in SEEDS:
        for scheme in (None, "simultaneous"):
            kwargs = dict(seed=seed, mapping_version=mapping, mtd_scheme=scheme)
            without = run_movement(profile, horizon=3_000, **kwargs)
            ablated = run_movement(
                profile, horizon=3_000,
                attacker_state=_state(kappa=0.0, rho=0.5, seed=seed), **kwargs,
            )
            assert _fields(ablated.records) == _fields(without.records), (
                f"kappa=0 perturbed {profile}/{mapping}/seed={seed}/mtd={scheme}"
            )
            assert ablated.reached_objective == without.reached_objective
            assert ablated.termination_time == without.termination_time


def test_the_ablated_learner_still_accumulated_its_belief() -> None:
    """Bit-identical does not mean inert. At ``kappa = 0`` the learner gathers
    the same evidence it would at any other capability — it simply never acts on
    it, which is what makes the arm an ablation of the *capability* rather than
    of the mechanism."""
    learner = LearningModulator(kappa=0.0, rho=0.0)
    run_movement("aggregate", seed=42, horizon=3_000, mapping_version="v2_partial",
                 attacker_state=AttackerState(seed=42, modulators=(learner,)))
    assert learner.success or learner.failure
    assert any(q != 0.5 for q in learner.snapshot()["q"].values())


def test_a_declared_learner_visibly_changes_the_walk() -> None:
    """The capability is live: at the declared values the record stream differs
    from the ablation arm's. If this passed identically the modulator would not
    be reaching the routing."""
    seed = 1234
    kwargs = dict(seed=seed, horizon=3_000, mapping_version="v2_partial")
    declared = load_learning_parameters()
    ablated = _fields(run_movement(
        "aggregate", attacker_state=_state(0.0, declared.rho, seed), **kwargs).records)
    learning = _fields(run_movement(
        "aggregate",
        attacker_state=AttackerState(
            seed=seed, modulators=(LearningModulator.declared(),)),
        **kwargs).records)
    assert ablated != learning


# --- 2. the estimator ---------------------------------------------------------


def test_an_unvisited_place_sits_at_the_prior_and_is_never_zeroed() -> None:
    """Exploration survives by construction: with no evidence the belief is
    exactly 0.5, so no destination is ever removed from the net by ignorance.
    This is the failure mode a bare success ratio would have — an unvisited
    place undefined or at zero, and never tried again."""
    learner = LearningModulator(kappa=4.0, rho=0.5)
    assert learner.q("never-seen") == 0.5
    assert learner.factors(None, "a", {"never-seen": 1.0})["never-seen"] == 0.5**4


def test_the_belief_moves_with_the_evidence_and_stays_strictly_positive() -> None:
    """Successes raise the estimate, failures lower it, and the Laplace prior
    keeps it strictly inside (0, 1) however lopsided the evidence — which is why
    the modulator declares ``may_zero = False``."""
    learner = LearningModulator(kappa=1.0, rho=0.0)
    for _ in range(3):
        learner.observe_verdict("pays", "success")
    for _ in range(3):
        learner.observe_verdict("does-not", "failure")
    assert learner.q("pays") > 0.5 > learner.q("does-not")
    assert 0.0 < learner.q("does-not") < 1.0
    for _ in range(500):
        learner.observe_verdict("does-not", "failure")
    assert learner.q("does-not") > 0.0


def test_a_dwell_only_none_verdict_is_silence_not_evidence() -> None:
    """A place that dispatches nothing neither confirms nor refutes anything, so
    its belief stays at the prior. Counting it as failure would encode a claim
    that non-action does not pay — an incentive/stealth claim, not a learning
    one."""
    learner = LearningModulator(kappa=1.0, rho=0.0)
    for _ in range(5):
        learner.observe_verdict("dwell-place", "none")
    assert learner.q("dwell-place") == 0.5
    assert "dwell-place" not in learner.success
    assert "dwell-place" not in learner.failure


def test_the_capability_exponent_sharpens_the_preference() -> None:
    """What ``kappa`` buys: the ratio between a believed-good and a
    believed-bad destination grows as its power, so a large capability is
    near-greedy — the behaviour the declared band has to contain in order to
    show the trade against strategic plurality."""
    def ratio(kappa: float) -> float:
        learner = LearningModulator(kappa=kappa, rho=0.0)
        for _ in range(4):
            learner.observe_verdict("good", "success")
            learner.observe_verdict("bad", "failure")
        f = learner.factors(None, "src", {"good": 1.0, "bad": 1.0})
        return f["good"] / f["bad"]

    assert ratio(0.5) < ratio(1.0) < ratio(2.0) < ratio(4.0)


# --- 3. the defence degrades the belief --------------------------------------


def test_rho_zero_is_a_learner_the_defence_cannot_touch() -> None:
    learner = LearningModulator(kappa=1.0, rho=0.0)
    learner.observe_verdict("b", "success")
    learner.observe_mtd_interrupt("network")
    assert learner.success["b"] == 1.0
    assert learner.forgettings == 0


def test_rho_one_is_total_amnesia_and_returns_the_belief_to_the_prior() -> None:
    """At the far pole a single mutation erases everything, so every place is
    back at 0.5 — the factor is then a constant across the out-set and cancels
    in the renormalisation, which is the arithmetic statement that a fully
    forgetful learner routes exactly as an unlearning one until it observes
    something new."""
    learner = LearningModulator(kappa=2.0, rho=1.0)
    for _ in range(5):
        learner.observe_verdict("b", "success")
        learner.observe_verdict("c", "failure")
    learner.observe_mtd_interrupt("application")
    assert learner.q("b") == learner.q("c") == 0.5
    factors = learner.factors(None, "a", {"b": 1.0, "c": 1.0})
    assert factors["b"] == factors["c"]


def test_the_declared_fraction_is_applied_multiplicatively_per_mutation() -> None:
    """The rule is a scaling, not a reset: after n mutations a count retains
    ``(1 - rho)^n`` of itself, which is the ladder the compiled worked view
    tabulates."""
    learner = LearningModulator(kappa=1.0, rho=0.5)
    for _ in range(8):
        learner.observe_verdict("b", "success")
    for n in range(1, 4):
        learner.observe_mtd_interrupt("network")
        assert learner.success["b"] == pytest.approx(8.0 * 0.5**n)
    assert learner.forgettings == 3


def test_the_belief_only_perishes_under_mtd() -> None:
    """The perishing must be *caused by the defence*: with no MTD running there
    is no interrupt, so nothing is forgotten however long the run goes on."""
    learner = LearningModulator(kappa=1.0, rho=1.0)
    run_movement("aggregate", seed=7, horizon=3_000, mapping_version="v2_partial",
                 attacker_state=AttackerState(seed=7, modulators=(learner,)))
    assert learner.forgettings == 0
    assert learner.success or learner.failure


def test_an_mtd_run_reports_its_interrupts_to_the_state() -> None:
    """The third seam works end to end: every interrupt the attacker absorbs
    reaches the state, and the count matches the driver's own record stream —
    so the forgetting rule fires exactly as often as the defence acted."""
    learner = LearningModulator(kappa=1.0, rho=0.5)
    state = AttackerState(seed=3, modulators=(learner,))
    res = run_movement("aggregate", seed=3, horizon=6_000,
                       mapping_version="v2_partial",
                       mtd_scheme="simultaneous", mtd_interval=150,
                       attacker_state=state)
    recorded = sum(1 for r in res.records if r.interrupted)
    assert recorded > 0, "no interrupt in this configuration — the test proves nothing"
    assert state.mtd_interrupts == recorded == learner.forgettings


def test_rho_is_inert_without_mtd_but_not_with_it() -> None:
    """The mechanism check the sweep's third conclusion rests on: changing the
    forgetting fraction cannot move a run with no defence in it, and does move
    one with a defence in it."""
    kwargs = dict(seed=11, horizon=6_000, mapping_version="v2_partial")

    def walk(rho: float, scheme: str | None):
        return _fields(run_movement(
            "aggregate", attacker_state=_state(1.0, rho, 11),
            mtd_scheme=scheme, mtd_interval=150, **kwargs).records)

    assert walk(0.0, None) == walk(1.0, None)
    assert walk(0.0, "simultaneous") != walk(1.0, "simultaneous")


# --- 4. determinism (validation gate 5) --------------------------------------


def test_the_learner_draws_no_randomness_at_all() -> None:
    """The belief is a deterministic function of the run's own history, so no
    fourth RNG stream is needed. Proven by consuming the state's stream: if the
    learner drew from it, the run would move."""
    def walk(burn: int):
        state = _state(1.0, 0.5, 5)
        for _ in range(burn):
            state.rng.random()
        return _fields(run_movement(
            "aggregate", seed=5, horizon=3_000, mapping_version="v2_partial",
            mtd_scheme="simultaneous", mtd_interval=150,
            attacker_state=state).records)

    assert walk(0) == walk(500)


def test_a_learning_run_is_deterministic_end_to_end() -> None:
    """SIM-05 with the capability live: same seed, same walk, twice."""
    def walk():
        return _fields(run_movement(
            "aggregate", seed=7, horizon=3_000, mapping_version="v2_partial",
            mtd_scheme="simultaneous", mtd_interval=150,
            attacker_state=AttackerState(
                seed=7, modulators=(LearningModulator.declared(),))).records)

    assert walk() == walk()


def test_the_learner_never_zeroes_an_out_edge_across_a_long_run() -> None:
    """``may_zero = False`` is a claim about the whole parameter space, not
    about a lucky run: the state refuses an undeclared zero factor loudly, so a
    long run at the band's top capability completing at all is the proof."""
    learner = LearningModulator(kappa=4.0, rho=0.0)
    res = run_movement("aggregate", seed=99, horizon=8_000,
                       mapping_version="v2_partial",
                       mtd_scheme="simultaneous", mtd_interval=150,
                       attacker_state=AttackerState(seed=99, modulators=(learner,)))
    assert res.records
    assert all(q > 0.0 for q in learner.snapshot()["q"].values())


# --- 5. the declared values reproduce from their rules -----------------------


def test_the_worked_view_reproduces_from_the_rules() -> None:
    """Requirement 1 of the declared-value precedent, enforced by tracked code:
    every cell of the compiled view re-derives from the rules artefact."""
    differing, total, examples = check_worked_view()
    assert total > 0
    assert differing == 0, f"{differing}/{total} cells differ, e.g. {examples}"


def test_the_declared_values_sit_inside_their_own_swept_bands() -> None:
    """A declared value on the edge of its band is not bracketed by the sweep —
    the defect the weight study had to re-cut a band to fix."""
    p = load_learning_parameters()
    assert min(p.kappa_band) < p.kappa < max(p.kappa_band)
    assert min(p.rho_band) < p.rho < max(p.rho_band)
    assert 0.0 in p.kappa_band, "the ablation arm must be a swept point"


def test_the_parameters_are_validated_at_construction() -> None:
    with pytest.raises(ValueError, match="kappa"):
        LearningModulator(kappa=-0.1, rho=0.5)
    with pytest.raises(ValueError, match="rho"):
        LearningModulator(kappa=1.0, rho=1.5)


# --- 6. the learning-signal measure ------------------------------------------


def test_the_within_run_trend_reads_quartiles_over_events() -> None:
    """The measure gate 2 reports: an improving attacker's last quarter blocks
    less than its first. Checked on a run rather than on a fixture, so the
    quartile arithmetic is exercised against a real record stream."""
    res = run_movement("aggregate", seed=0, horizon=6_000,
                       mapping_version="v2_partial")
    trend = blocked_fraction_trend(res)
    assert trend is not None
    assert trend.n_events >= 4
    assert 0.0 <= trend.first_quartile <= 1.0
    assert 0.0 <= trend.last_quartile <= 1.0
    assert trend.change == trend.last_quartile - trend.first_quartile
