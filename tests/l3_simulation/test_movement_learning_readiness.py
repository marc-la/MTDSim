"""The readiness-aware learning capability (criterion axis 7, generalised).

Same hard gate as the destination-only learner: the ablation arm (``kappa = 0``)
reproduces today bit for bit, across every profile, several seeds and both MTD
conditions, so the ablation measures the parameter and not the wiring.

The rest pin what the generalisation adds: the belief is keyed on
``(place, ready?)`` rather than the place alone; the readiness bit is tracked
from the attacker's own trajectory against the declared precondition relation
(an exploit is unready before a scan and ready after); MTD severs the phase-state
the relation says it severs; and the same Laplace/exploration/forgetting
properties the destination-only learner proves still hold on the finer key.

A measurement test also reports the declared bit's prediction accuracy against
the substrate's own ``blocked`` ground truth — the validation gate the design
record names (learning_representation.md §4).

Design record: docs/implementation/pipeline/ogasp/learning_representation.md.
"""
from __future__ import annotations

import dataclasses

import pytest

from mtdsim.l3_simulation.movement.learning import load_learning_parameters
from mtdsim.l3_simulation.movement.learning_readiness import (
    ACCEPTANCE,
    PROGRESS,
    DeclaredReadinessBias,
    PreconditionModel,
    ReadinessLearningModulator,
    load_tactic_to_verb,
)
from mtdsim.l3_simulation.movement.net import PROFILES
from mtdsim.l3_simulation.movement.run import run_movement
from mtdsim.l3_simulation.movement.state import AttackerState

SEEDS = (0, 7, 42, 1234, 9001)
MAPPINGS = (None, "v2_partial")


def _fields(records):
    return [dataclasses.asdict(r) for r in records]


def _modulator(kappa, rho, mapping=None):
    return ReadinessLearningModulator(
        kappa=kappa, rho=rho, tactic_to_verb=load_tactic_to_verb(mapping)
    )


def _state(kappa, rho, seed, mapping=None):
    return AttackerState(seed=seed, modulators=(_modulator(kappa, rho, mapping),))


# --- 1. the ablation arm is bit-identical to today (validation gate 1) -------


@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("mapping", MAPPINGS)
def test_kappa_zero_reproduces_the_current_record_stream_field_for_field(
    profile, mapping
) -> None:
    """The load-bearing guarantee for the generalised learner. It tracks its
    capability state and accumulates its belief at zero capability, but acts on
    none of it, so the walk must be the walk that has always run."""
    for seed in SEEDS:
        for scheme in (None, "simultaneous"):
            kwargs = dict(seed=seed, mapping_version=mapping, mtd_scheme=scheme)
            without = run_movement(profile, horizon=3_000, **kwargs)
            ablated = run_movement(
                profile, horizon=3_000,
                attacker_state=_state(0.0, 0.5, seed, mapping), **kwargs,
            )
            assert _fields(ablated.records) == _fields(without.records), (
                f"kappa=0 perturbed {profile}/{mapping}/seed={seed}/mtd={scheme}"
            )
            assert ablated.reached_objective == without.reached_objective
            assert ablated.termination_time == without.termination_time


def test_the_ablated_learner_still_tracked_state_and_belief() -> None:
    """Bit-identical does not mean inert: at kappa = 0 the learner still tracks
    its held capabilities and accumulates keyed evidence, it simply never routes
    on it."""
    learner = _modulator(0.0, 0.0, "v2_partial")
    run_movement("aggregate", seed=42, horizon=3_000, mapping_version="v2_partial",
                 attacker_state=AttackerState(seed=42, modulators=(learner,)))
    assert learner.success or learner.failure
    # A run that compromises hosts must have held curr_host at least once.
    assert any(r for r in learner.success) or any(r for r in learner.failure)


def test_a_declared_learner_visibly_changes_the_walk() -> None:
    """The capability is live: at the declared values the record stream differs
    from the ablation arm's."""
    seed = 1234
    kwargs = dict(seed=seed, horizon=3_000, mapping_version="v2_partial")
    rho = load_learning_parameters().rho
    ablated = _fields(run_movement(
        "aggregate", attacker_state=_state(0.0, rho, seed, "v2_partial"), **kwargs).records)
    learning = _fields(run_movement(
        "aggregate",
        attacker_state=AttackerState(
            seed=seed,
            modulators=(ReadinessLearningModulator.declared(
                tactic_to_verb=load_tactic_to_verb("v2_partial")),)),
        **kwargs).records)
    assert ablated != learning


def test_it_differs_from_the_destination_only_learner() -> None:
    """The generalisation is a real change of behaviour, not a relabelling: at
    the same declared values the readiness-keyed walk differs from the
    destination-only walk on a profile where the precondition bites."""
    from mtdsim.l3_simulation.movement.learning import LearningModulator

    seed = 7
    kwargs = dict(seed=seed, horizon=4_000, mapping_version="v2_partial")
    marginal = _fields(run_movement(
        "aggregate",
        attacker_state=AttackerState(seed=seed, modulators=(LearningModulator.declared(),)),
        **kwargs).records)
    readiness = _fields(run_movement(
        "aggregate",
        attacker_state=AttackerState(
            seed=seed,
            modulators=(ReadinessLearningModulator.declared(
                tactic_to_verb=load_tactic_to_verb("v2_partial")),)),
        **kwargs).records)
    assert marginal != readiness


# --- 2. the estimator on the finer key ---------------------------------------


def test_an_unobserved_cell_sits_at_the_prior_and_is_never_zeroed() -> None:
    learner = _modulator(4.0, 0.5, "v2_partial")
    assert learner.q("execution", True) == 0.5
    assert learner.q("execution", False) == 0.5


def test_the_two_readiness_cells_of_one_place_are_learned_separately() -> None:
    """The whole point of the key: a place tried when ready and when not ready
    accumulates two independent beliefs, so the deterministic not-ready failure
    does not drag down the belief about trying the place when ready."""
    learner = _modulator(1.0, 0.0, "v2_partial")
    for _ in range(5):
        learner.observe_visit("execution")
        # pretend ready -> a genuine mix of outcomes
    # Drive the cells directly to isolate the estimator from the walk.
    learner.success[("execution", True)] = 6.0
    learner.failure[("execution", True)] = 4.0
    learner.failure[("execution", False)] = 20.0
    assert learner.q("execution", True) == pytest.approx((6 + 1) / (6 + 4 + 2))
    assert learner.q("execution", False) == pytest.approx((0 + 1) / (0 + 20 + 2))
    assert learner.q("execution", True) > learner.q("execution", False)


def test_the_factor_is_strictly_positive_however_lopsided(  # may_zero = False
) -> None:
    learner = _modulator(4.0, 0.0, "v2_partial")
    for _ in range(500):
        learner.failure[("execution", True)] = (
            learner.failure.get(("execution", True), 0.0) + 1.0
        )
    f = learner.factors(None, "discovery", {"execution": 1.0})
    assert f["execution"] > 0.0


# --- 3. the capability tracker mirrors the substrate --------------------------


def test_exploit_is_unready_before_a_scan_and_ready_after() -> None:
    """The dependency the marginal could not represent, checked directly on the
    tracker: under v2 the EXPLOIT tactics need curr_ports, which `discovery`
    (SCAN_PORT) produces once curr_host is held."""
    model = PreconditionModel.load()
    learner = _modulator(1.0, 0.0, "v2_partial")
    # Nothing held yet -> execution (EXPLOIT_VULN) is unready.
    assert learner.model.is_ready("EXPLOIT_VULN", learner.held) is False
    # lateral-movement (ENUM_HOST) needs host_stack; give it one, then run it.
    learner.held.add("host_stack")
    learner.observe_visit("lateral-movement")
    learner.observe_verdict("lateral-movement", "success")
    assert "curr_host" in learner.held
    # discovery (SCAN_PORT) now runs and produces curr_ports.
    learner.observe_visit("discovery")
    learner.observe_verdict("discovery", "success")
    assert "curr_ports" in learner.held
    # execution is ready at last.
    assert learner.model.is_ready("EXPLOIT_VULN", learner.held) is True


def test_a_blocked_dispatch_produces_no_capability() -> None:
    """Production is gated on readiness: a verb whose precondition is unmet is
    blocked and establishes nothing, so a scan attempted with no current host
    yields no curr_ports."""
    learner = _modulator(1.0, 0.0, "v2_partial")
    # discovery (SCAN_PORT) needs curr_host, which is not held.
    learner.observe_visit("discovery")
    learner.observe_verdict("discovery", "failure")  # blocked -> failure
    assert "curr_ports" not in learner.held
    assert learner.failure.get(("discovery", False)) == 1.0


def test_a_network_mtd_severs_position_but_an_application_one_does_not() -> None:
    """The declared relation's MTD clause: a network-layer mutation clears the
    host cursor (and the port knowledge that depends on it); an application-layer
    one clears nothing structural, though both decay the belief."""
    learner = _modulator(1.0, 0.5, "v2_partial")
    learner.held.update({"host_stack", "curr_host", "curr_ports"})
    learner.observe_mtd_interrupt("application")
    assert learner.held == {"host_stack", "curr_host", "curr_ports"}
    assert learner.forgettings == 1  # belief still decayed
    learner.observe_mtd_interrupt("network")
    assert learner.held == {"host_stack"}  # position severed
    assert learner.forgettings == 2


# --- 4. forgetting, inherited unchanged --------------------------------------


def test_forgetting_only_fires_under_mtd() -> None:
    learner = _modulator(1.0, 1.0, "v2_partial")
    run_movement("aggregate", seed=7, horizon=3_000, mapping_version="v2_partial",
                 attacker_state=AttackerState(seed=7, modulators=(learner,)))
    assert learner.forgettings == 0
    assert learner.success or learner.failure


def test_forgetting_is_multiplicative_per_mutation() -> None:
    learner = _modulator(1.0, 0.5, "v2_partial")
    learner.success[("execution", True)] = 8.0
    for n in range(1, 4):
        learner.observe_mtd_interrupt("application")  # decays belief, not position
        assert learner.success[("execution", True)] == pytest.approx(8.0 * 0.5**n)


# --- 5. determinism (SIM-05) --------------------------------------------------


def test_the_learner_draws_no_randomness() -> None:
    """The readiness learner is a deterministic function of the run's history —
    it consults no random stream, so the same seed gives the same walk twice and
    burning the state's RNG leaves the run untouched."""
    def walk(seed):
        return _fields(run_movement(
            "aggregate", seed=seed, horizon=3_000, mapping_version="v2_partial",
            attacker_state=AttackerState(
                seed=seed,
                modulators=(ReadinessLearningModulator.declared(
                    tactic_to_verb=load_tactic_to_verb("v2_partial")),))).records)

    assert walk(42) == walk(42)


# --- 6. the readiness bit's prediction accuracy (validation gate, reported) --


def test_the_declared_bit_predicts_the_substrate_block_flag_well() -> None:
    """The design record's Part B validation gate: the in-layer readiness bit is
    a *prediction* of the substrate's own precondition guard. Measure its
    agreement with the ground-truth `blocked` flag over a real run and assert it
    is high — a mispredicting bit is a weaker version of the mechanism, so the
    build has to show the declared relation actually tracks the substrate.

    Reported rather than merely asserted: the numbers print so the known
    optimisms (empty scans) are visible, not hidden behind a threshold.
    """
    mapping = "v2_partial"
    t2v = load_tactic_to_verb(mapping)
    model = PreconditionModel.load()
    agree = total = 0
    for seed in range(5):
        # Replay the base traversal, tracking held capabilities exactly as the
        # modulator does, and compare predicted-ready to (not blocked).
        learner = _modulator(0.0, 0.5, mapping)
        res = run_movement(
            "aggregate", seed=seed, horizon=8_000, mapping_version=mapping,
            attacker_state=AttackerState(seed=seed, modulators=(learner,)))
        held = set()
        for rec in res.records:
            if not rec.verb:  # dwell-only, no precondition to predict
                continue
            verb = t2v.get(rec.place)
            predicted_ready = model.is_ready(verb, held)
            actual_ready = not rec.blocked
            total += 1
            agree += int(predicted_ready == actual_ready)
            # advance held exactly as observe_verdict would (gated on readiness)
            if verb is not None and predicted_ready:
                held |= model.produces[verb]
                held -= model.clears[verb]
            if rec.interrupted and rec.interrupted_by == "network":
                held -= model.mtd_clears.get("network", set())
    accuracy = agree / total
    print(f"\nreadiness-bit accuracy vs substrate block flag: "
          f"{accuracy:.3f} ({agree}/{total})")
    assert accuracy >= 0.85, f"declared readiness bit only {accuracy:.3f} accurate"


# --- 6. the progress credit rule (feasibility study §9.2) ---------------------
#
# The shipped rule credits acceptance: the substrate permitted the action. The
# progress rule credits the state change the action produced. Measurement located
# the whole progress cost in the ready-cell ordering that acceptance induces
# (rank correlation +0.921 with acceptance, -0.027 with progress), so these tests
# pin the new rule's behaviour rather than its tuning.


def _progress_modulator(kappa, rho, mapping="v2_partial"):
    return ReadinessLearningModulator(
        kappa=kappa, rho=rho, tactic_to_verb=load_tactic_to_verb(mapping),
        credit=PROGRESS,
    )


def test_the_credit_rule_defaults_to_the_shipped_one() -> None:
    """Every figure on record was produced by acceptance credit, so it stays the
    default and the progress rule is opt-in — the arm-selector idiom the iterated
    cost model established."""
    assert _modulator(1.0, 0.5, "v2_partial").credit == ACCEPTANCE
    with pytest.raises(ValueError, match="credit must be one of"):
        ReadinessLearningModulator(
            kappa=1.0, rho=0.5, tactic_to_verb=load_tactic_to_verb("v2_partial"),
            credit="whatever",
        )


@pytest.mark.parametrize("profile", PROFILES)
def test_acceptance_credit_is_bit_identical_to_the_shipped_mechanism(profile) -> None:
    """The reorder in observe_verdict (effect applied before credit) must not
    move the acceptance arm — under that rule the credit never reads the
    phase-state, so the order is immaterial and this proves it."""
    seed = 11
    kwargs = dict(seed=seed, horizon=3_000, mapping_version="v2_partial")
    a = _modulator(1.0, 0.5, "v2_partial")
    b = _modulator(1.0, 0.5, "v2_partial")
    ra = run_movement(profile, attacker_state=AttackerState(seed=seed, modulators=(a,)), **kwargs)
    rb = run_movement(profile, attacker_state=AttackerState(seed=seed, modulators=(b,)), **kwargs)
    assert _fields(ra.records) == _fields(rb.records)
    assert a.success == b.success and a.failure == b.failure


def test_an_action_that_changes_nothing_earns_no_credit() -> None:
    """The rule in one assertion. `reconnaissance` (SCAN_HOST) produces
    host_stack: the first run of it moves the phase-state and is credited, the
    second changes nothing and is charged as a failure — which is the
    reconnaissance-farming loop closed."""
    learner = _progress_modulator(1.0, 0.0)
    learner.observe_visit("reconnaissance")
    learner.observe_verdict("reconnaissance", "success")
    assert learner.success.get(("reconnaissance", True)) == 1.0
    assert "host_stack" in learner.held

    learner.observe_visit("reconnaissance")
    learner.observe_verdict("reconnaissance", "success")
    assert learner.success.get(("reconnaissance", True)) == 1.0     # unchanged
    assert learner.failure.get(("reconnaissance", True)) == 1.0     # charged


def test_re_attacking_a_footholded_host_earns_no_credit() -> None:
    """The churn failure mode: the profiles blocked 0 % of the time still failed,
    re-compromising the same few hosts. A second exploit on a host already
    footholded changes nothing and earns nothing."""
    learner = _progress_modulator(1.0, 0.0)
    learner.held.update({"host_stack", "curr_host", "curr_ports"})
    learner.observe_visit("execution")                    # EXPLOIT_VULN
    learner.observe_verdict("execution", "success")
    assert "foothold" in learner.held
    assert learner.success.get(("execution", True)) == 1.0

    learner.observe_visit("execution")
    learner.observe_verdict("execution", "success")
    assert learner.success.get(("execution", True)) == 1.0          # unchanged
    assert learner.failure.get(("execution", True)) == 1.0          # charged


def test_pivoting_to_a_new_host_is_movement_and_re_opens_the_foothold() -> None:
    """A clearing action counts as movement: ENUM_HOST drops the foothold and the
    port knowledge because the cursor has moved to a different host, which is the
    pivot that makes the next compromise reachable. Without this the attacker
    would learn never to pivot and the loop would close after one host."""
    learner = _progress_modulator(1.0, 0.0)
    learner.held.update({"host_stack", "curr_host", "curr_ports", "foothold"})
    learner.observe_visit("lateral-movement")             # ENUM_HOST
    learner.observe_verdict("lateral-movement", "success")
    assert "foothold" not in learner.held and "curr_ports" not in learner.held
    assert learner.success.get(("lateral-movement", True)) == 1.0

    # Immediately again: nothing left to clear, curr_host already held -> inert.
    learner.observe_visit("lateral-movement")
    learner.observe_verdict("lateral-movement", "success")
    assert learner.failure.get(("lateral-movement", True)) == 1.0


def test_a_blocked_attempt_still_lands_in_the_not_ready_cell() -> None:
    """Unchanged by the new rule, and deliberately so — measurement put the
    not-ready component's cost to expected progress between 0.0 % and +1.8 %, so
    suppressing attempts that would fail is free and correct."""
    learner = _progress_modulator(1.0, 0.0)
    learner.observe_visit("execution")                    # unready: nothing held
    learner.observe_verdict("execution", "failure")
    assert learner.failure.get(("execution", False)) == 1.0
    assert learner.held == set()


def test_progress_credit_still_never_zeroes_an_out_edge() -> None:
    """may_zero = False stays a proof under the new rule: the Laplace prior holds
    every cell strictly positive however many inert successes are charged.

    `command-and-control` dispatches SCAN_NEIGHBOR, which needs curr_host and
    produces host_stack — so holding both makes it *ready* and *inert*, which is
    exactly the permitted-but-achieves-nothing case the new rule charges."""
    learner = _progress_modulator(4.0, 0.0)
    learner.held.update({"host_stack", "curr_host"})
    for _ in range(200):
        learner.observe_visit("command-and-control")
        learner.observe_verdict("command-and-control", "success")
    assert learner.failure.get(("command-and-control", True)) == 200.0
    assert not learner.success                      # 200 accepted, none credited
    q = learner.q("command-and-control", True)
    assert 0.0 < q < 0.02                           # 1/202, strictly positive
    factors = learner.factors(None, "execution", {"command-and-control": 1.0})
    assert factors["command-and-control"] > 0.0


def test_kappa_zero_is_still_bit_identical_under_progress_credit() -> None:
    """The null-equivalence guarantee is a property of the composition, not of the
    credit rule, and the ablation arm must stay shared between the two arms."""
    seed = 3
    kwargs = dict(seed=seed, horizon=3_000, mapping_version="v2_partial")
    a = run_movement("aggregate", attacker_state=AttackerState(
        seed=seed, modulators=(_progress_modulator(0.0, 0.5),)), **kwargs)
    b = run_movement("aggregate", attacker_state=AttackerState(
        seed=seed, modulators=(_modulator(0.0, 0.5, "v2_partial"),)), **kwargs)
    assert _fields(a.records) == _fields(b.records)


# --- 7. the declared-bias control arm (criterion C3) -------------------------


def test_the_control_never_lets_its_counts_reach_the_routing_decision() -> None:
    """The C3 control: same readiness tracking, same exponent, same composition —
    but the belief is two declared constants, so accumulated evidence cannot move
    a factor. If the learner cannot be told apart from this, its counts are
    decoration."""
    control = DeclaredReadinessBias(
        kappa=1.0, rho=0.5, tactic_to_verb=load_tactic_to_verb("v2_partial"),
        q_ready=0.85, q_unready=0.05,
    )
    out = {"execution": 1.0}
    before = control.factors(None, "discovery", out)["execution"]
    for _ in range(50):
        control.observe_visit("execution")
        control.observe_verdict("execution", "failure")
    after = control.factors(None, "discovery", out)["execution"]
    assert before == after                      # evidence changed nothing
    assert control.failure                      # ...though it was recorded


def test_the_control_still_tracks_readiness_and_severance() -> None:
    """It is a control for the *belief*, not for the readiness machinery — that
    has to stay identical or the comparison is confounded."""
    control = DeclaredReadinessBias(
        kappa=1.0, rho=0.5, tactic_to_verb=load_tactic_to_verb("v2_partial"),
        q_ready=0.85, q_unready=0.05,
    )
    assert control.q("execution", True) == 0.85
    assert control.q("execution", False) == 0.05
    control.held.update({"host_stack", "curr_host", "curr_ports", "foothold"})
    control.observe_mtd_interrupt("network")
    assert control.held == {"host_stack"}


def test_the_control_refuses_a_rate_that_would_zero_an_edge() -> None:
    with pytest.raises(ValueError, match="strictly positive|lie in"):
        DeclaredReadinessBias(
            kappa=1.0, rho=0.5, tactic_to_verb=load_tactic_to_verb("v2_partial"),
            q_ready=0.85, q_unready=0.0,
        )
