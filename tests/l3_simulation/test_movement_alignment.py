"""The FSM-alignment overlay (composition-register factor 8).

The factor scores no axis. What these tests pin is the instrument's arithmetic
and the two properties that decide whether its band is usable at all.

The hard gate is the same one every modulator carries: the null arm (``α = 0``)
reproduces today bit for bit across every profile, several seeds, both mappings
and both MTD conditions, so the sweep measures the parameter and not the wiring.

The rest pin the distance model against the capability closure computed by hand
(the handoff's §3 table), the MTD *set contraction* that is the whole reason this
shape was built, the exhaustive no-stall check that licenses the limiting end of
the band, and the one defect that check actually caught — a zero-weight base edge
being allowed to set the minimum, which would have starved every live candidate.

Design record: docs/implementation/pipeline/ogasp/fsm_alignment_overlay.md.
"""
from __future__ import annotations

import dataclasses

import pytest

from mtdsim.l3_simulation.movement.alignment import (
    OBJECTIVE_VERBS,
    AlignmentError,
    CapabilityCursor,
    FsmAlignmentModulator,
    ObjectiveDistance,
    load_alignment_parameters,
    stall_report,
)
from mtdsim.l3_simulation.movement.learning_readiness import (
    PreconditionModel,
    ReadinessLearningModulator,
    load_tactic_to_verb,
)
from mtdsim.l3_simulation.movement.net import PROFILES
from mtdsim.l3_simulation.movement.run import run_movement
from mtdsim.l3_simulation.movement.state import AttackerState

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
MAPPINGS = (None, "v2_partial")


def _fields(records):
    return [dataclasses.asdict(r) for r in records]


def _modulator(alpha, mapping=None, **kwargs):
    return FsmAlignmentModulator(
        alpha=alpha, tactic_to_verb=load_tactic_to_verb(mapping), **kwargs
    )


def _state(alpha, seed, mapping=None, **kwargs):
    return AttackerState(seed=seed, modulators=(_modulator(alpha, mapping, **kwargs),))


# --- 1. the null arm is bit-identical to today (validation gate 1) -----------


@pytest.mark.parametrize("seed", SEED_PARAMS)
@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("mapping", MAPPINGS)
def test_alpha_zero_reproduces_the_current_record_stream_field_for_field(
    profile, mapping, seed, baseline_run
) -> None:
    """The load-bearing guarantee. At α = 0 the modulator tracks its capability
    cursor and computes nothing with it, so the walk must be the walk that has
    always run — asserted over profiles × seeds × mappings × MTD conditions as a
    test rather than as a run (the standing U1/C1 discipline)."""
    for scheme in (None, "simultaneous"):
        kwargs = dict(seed=seed, mapping_version=mapping, mtd_scheme=scheme)
        without = baseline_run(profile, horizon=3_000, **kwargs)
        null = run_movement(
            profile,
            horizon=3_000,
            attacker_state=_state(0.0, seed, mapping),
            **kwargs,
        )
        assert _fields(null.records) == _fields(without.records), (
            f"alpha=0 perturbed {profile}/{mapping}/seed={seed}/mtd={scheme}"
        )
        assert null.reached_objective == without.reached_objective
        assert null.termination_time == without.termination_time
        assert null.compromised_count == without.compromised_count


def test_the_null_arm_returns_no_factors_at_all() -> None:
    """Null-equivalence is arithmetic, not approximate: the modulator returns an
    empty mapping, so the seam's product is untouched rather than multiplied by
    a table of 1.0s."""
    assert _modulator(0.0).factors(None, "reconnaissance", {"execution": 1.0}) == {}


# --- 2. the distance model against the closure computed by hand -------------


@pytest.fixture(scope="module")
def distances() -> ObjectiveDistance:
    return ObjectiveDistance.load()


def test_the_declared_target_set_is_the_three_compromise_causing_verbs() -> None:
    """The transcription, pinned so a silent edit is a failing test. ENUM_HOST
    also calls the substrate's progress hook, but under a guard that only fires
    for a host already owned, so it is deliberately not a target."""
    assert OBJECTIVE_VERBS == {"SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE"}
    assert "ENUM_HOST" not in OBJECTIVE_VERBS


@pytest.mark.parametrize(
    "held, legal, steps",
    [
        (frozenset(), 1, 2),
        (frozenset({"host_stack"}), 2, 1),
        (frozenset({"curr_host"}), 4, 0),
        (frozenset({"curr_host", "host_stack"}), 5, 0),
        (frozenset({"curr_host", "host_stack", "curr_ports"}), 6, 0),
    ],
)
def test_the_capability_closure_matches_the_hand_computed_table(
    distances, held, legal, steps
) -> None:
    """The handoff's §3 table, recomputed by the closure rather than asserted
    from it: with nothing held only SCAN_HOST runs and two steps separate the
    attacker from a productive action; the host cursor alone puts it at zero."""
    assert len(distances.legal_verbs(held)) == legal
    assert distances.steps_to_capable(held) == steps


def test_a_blocked_verb_and_a_dwell_only_place_cost_a_step_and_move_nothing(
    distances,
) -> None:
    """The model's one opinion. Both are strictly worse than any move that
    advances, and neither is worse than the other — an action the substrate
    refuses and an action the mapping never dispatches leave the attacker in the
    same place, having spent the same step."""
    empty = frozenset()
    assert distances.distance("EXPLOIT_VULN", empty) == 3  # blocked
    assert distances.distance(None, empty) == 3  # dwell-only
    assert distances.distance("SCAN_HOST", empty) == 2  # legal and enabling


def test_a_productive_verb_that_would_run_now_is_at_distance_zero(distances) -> None:
    held = frozenset({"curr_host", "curr_ports"})
    assert distances.distance("SCAN_PORT", held) == 0
    assert distances.distance("BRUTE_FORCE", held) == 0
    assert distances.distance("EXPLOIT_VULN", held) == 0
    # Reconnaissance is legal here and buys nothing, so it costs its own step.
    assert distances.distance("SCAN_HOST", held) == 1


def test_an_objective_verb_outside_the_relation_is_refused_loudly() -> None:
    model = PreconditionModel.load()
    with pytest.raises(AlignmentError):
        ObjectiveDistance.of(model, objective_verbs={"EXFILTRATE"})
    with pytest.raises(AlignmentError):
        ObjectiveDistance.of(model, objective_verbs=set())


# --- 3. MTD is a set contraction, not a scalar surcharge ---------------------


def test_a_network_mutation_contracts_the_legal_verb_set_and_regresses_the_distance(
    distances,
) -> None:
    """The property the whole shape exists for. A normalised utility *ratio* is
    invariant to a proportional inflation of its denominator; a set contraction
    is not, and this is the contraction stated as an assertion."""
    cursor = CapabilityCursor(PreconditionModel.load(), load_tactic_to_verb("v2_partial"))
    cursor.held = frozenset({"host_stack", "curr_host", "curr_ports", "foothold"})
    assert len(distances.legal_verbs(cursor.held)) == 6
    assert distances.steps_to_capable(cursor.held) == 0

    cursor.observe_mtd_interrupt("network")
    assert cursor.held == frozenset({"host_stack"})
    assert len(distances.legal_verbs(cursor.held)) == 2
    assert distances.steps_to_capable(cursor.held) == 1


def test_an_application_mutation_clears_nothing_structural(distances) -> None:
    cursor = CapabilityCursor(PreconditionModel.load(), load_tactic_to_verb("v2_partial"))
    cursor.held = frozenset({"host_stack", "curr_host", "curr_ports"})
    cursor.observe_mtd_interrupt("application")
    assert cursor.held == frozenset({"host_stack", "curr_host", "curr_ports"})
    assert distances.steps_to_capable(cursor.held) == 0


# --- 4. the routing factor's arithmetic -------------------------------------


def test_the_minimum_is_one_and_everything_above_it_is_one_minus_alpha() -> None:
    modulator = _modulator(0.75, "v2_partial")
    out = {"reconnaissance": 0.5, "execution": 0.3, "collection": 0.2}
    factors = modulator.factors(None, "resource-development", out)
    # With nothing held, reconnaissance is the only step that advances (d = 2);
    # the exploit is blocked and collection dispatches nothing (both d = 3).
    assert factors == {"reconnaissance": 1.0, "execution": 0.25, "collection": 0.25}


def test_the_limiting_end_zeroes_every_candidate_off_a_shortest_path() -> None:
    modulator = _modulator(1.0, "v2_partial")
    out = {"reconnaissance": 0.5, "execution": 0.5}
    assert modulator.factors(None, "resource-development", out) == {
        "reconnaissance": 1.0,
        "execution": 0.0,
    }


def test_may_zero_is_claimed_only_at_the_limiting_end() -> None:
    """Declared per instance, so the seam's stall guard stays a live proof for
    every arm of the sweep except the one that actually needs the licence."""
    assert _modulator(0.0).may_zero is False
    assert _modulator(0.5).may_zero is False
    assert _modulator(0.99).may_zero is False
    assert _modulator(1.0).may_zero is True
    assert _modulator(1.0, off_floor=0.01).may_zero is False


def test_a_zero_weight_base_edge_cannot_set_the_minimum() -> None:
    """The regression for the defect the no-stall check caught. A net may carry
    an out-edge at weight zero; the composition drops it before this factor's
    product applies, so letting it set the minimum would leave every *live*
    candidate off-band and, at the limiting end, empty the out-set."""
    modulator = _modulator(1.0, "v2_partial")
    out = {"reconnaissance": 0.0, "execution": 0.5, "collection": 0.5}
    factors = modulator.factors(None, "resource-development", out)
    assert set(factors) == {"execution", "collection"}
    assert max(factors.values()) == 1.0, "every live candidate was suppressed"


def test_alpha_outside_the_unit_interval_is_refused() -> None:
    for bad in (-0.1, 1.1):
        with pytest.raises(ValueError):
            _modulator(bad)
    with pytest.raises(ValueError):
        _modulator(1.0, off_floor=1.0)


# --- 5. the exhaustive no-stall check (validation gate 2) --------------------


def test_the_no_stall_check_is_empty_across_the_whole_declared_space() -> None:
    """The licence for ``may_zero`` at the limiting end, and the reason the
    declared off-band floor is 0.0. Static rather than sampled: a run-based check
    could only say the stall was not reached, this says it is not reachable —
    every profile net × mapping × overlay version × verdict × capability subset ×
    one-shot retrace suppression retains a minimal-distance destination."""
    assert stall_report() == []


def test_the_no_stall_check_has_teeth() -> None:
    """A checker that cannot fail proves nothing. Hand it an overlay built to
    hard-suppress exactly the destinations the distance model would keep — the
    one shape that empties an out-set at the limiting end — and it must say so."""
    from mtdsim.l3_simulation.controller.outcome import OutcomeOverlay
    from mtdsim.l3_simulation.movement.net import load_routing_net

    net = load_routing_net("aggregate", with_synthetic_overlay=True)
    t2v = load_tactic_to_verb("v2_partial")
    model = ObjectiveDistance.load()

    # Find a source with a choice to make, and suppress its whole minimal set.
    for src in sorted(net.places):
        live = {d: w for d, w in net.base_out_weights(src).items() if w > 0.0}
        if len(live) < 2:
            continue
        distance = {d: model.distance(t2v.get(d), frozenset()) for d in live}
        minimum = min(distance.values())
        minimal = {d for d, v in distance.items() if v == minimum}
        if len(minimal) < len(live):
            break
    else:  # pragma: no cover - no such source would make the check untestable
        pytest.fail("no source place offers a non-trivial minimal set")

    sabotaged = OutcomeOverlay.from_values(
        {"success": {src: {d: 0.0 for d in minimal}}}, version="sabotaged"
    )
    findings = stall_report(
        profiles=("aggregate",),
        mapping_versions=("v2_partial",),
        overlays={"sabotaged": sabotaged},
        include_retrace_suppression=False,
    )
    assert findings, "the no-stall check accepted a configuration that stalls"
    assert any(f.src == src and f.verdict == "success" for f in findings)


# --- 6. the capability cursor agrees with the readiness learner's ------------


@pytest.mark.parametrize("profile", ("pure_steal", "double_extortion"))
def test_the_duplicated_cursor_tracks_the_readiness_learner_step_for_step(
    profile,
) -> None:
    """This factor carries its own copy of the capability-tracking rule rather
    than sharing the readiness learner's, so that each factor stays independently
    ablatable. The drift that duplication risks is answered here by agreement of
    *behaviour* — both are driven over the same run and must hold the same
    capabilities at every observation."""
    mapping = "v2_partial"
    t2v = load_tactic_to_verb(mapping)
    alignment = FsmAlignmentModulator(alpha=0.0, tactic_to_verb=t2v)
    learner = ReadinessLearningModulator(kappa=0.0, rho=0.5, tactic_to_verb=t2v)
    disagreements: list[str] = []

    class _Witness:
        name = "cursor-witness"

        def factors(self, state, src, base_out_weights):
            if alignment.cursor.held != frozenset(learner.held):
                disagreements.append(
                    f"{src}: {sorted(alignment.cursor.held)} != {sorted(learner.held)}"
                )
            return {}

    state = AttackerState(seed=7, modulators=(alignment, learner, _Witness()))
    run = run_movement(
        profile,
        seed=7,
        horizon=3_000,
        mapping_version=mapping,
        mtd_scheme="simultaneous",
        attacker_state=state,
    )
    assert run.records, "the run produced no decisions to compare over"
    assert not disagreements, disagreements[:5]


# --- 7. the declared parameter ----------------------------------------------


def test_the_declared_value_is_the_null_and_the_band_reaches_both_poles() -> None:
    """α has no defensible operating point and is not supposed to have one: the
    declared value is the null arm, and the band's endpoints are the two named
    positions (pure CTI order, and the host's native procedural order)."""
    params = load_alignment_parameters()
    assert params.alpha == 0.0
    assert params.sweep[0] == 0.0 and params.sweep[-1] == 1.0
    assert len(params.sweep) >= 5, "a dose-response curve needs interior points"
    assert params.off_floor == 0.0, "the no-stall check passed; no floor is needed"


def test_the_declared_modulator_is_the_null_arm_unless_an_arm_overrides_it() -> None:
    assert FsmAlignmentModulator.declared(
        tactic_to_verb=load_tactic_to_verb("v2_partial")
    ).alpha == 0.0
    assert FsmAlignmentModulator.declared(
        tactic_to_verb=load_tactic_to_verb("v2_partial"), alpha=0.5
    ).alpha == 0.5


# --- 8. the factor visibly changes the walk at a non-zero alpha --------------


def test_a_non_zero_alpha_changes_the_walk() -> None:
    """The seam is live: the dial is not merely registered, it routes. Asserted
    as a difference, never as an improvement — which direction it moves is the
    sweep's question and is pre-registered rather than tested for here."""
    kwargs = dict(seed=0, mapping_version="v2_partial", mtd_scheme="simultaneous")
    null = run_movement("pure_steal", horizon=3_000, **kwargs)
    biased = run_movement(
        "pure_steal",
        horizon=3_000,
        attacker_state=_state(1.0, 0, "v2_partial"),
        **kwargs,
    )
    assert [r.place for r in biased.records] != [r.place for r in null.records]
