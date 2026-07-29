"""The unified L3 tracer must observe a movement run without changing it, and
must narrate all three layers — token, controller, substrate — on one clock.
"""

from __future__ import annotations

import pytest

from mtdsim.l3_simulation.movement.run import run_movement
from mtdsim.l3_simulation.movement.state import AttackerState, RevisitAversionDemo
from mtdsim.l3_simulation.trace import L3_ACTORS, run_l3_trace


@pytest.mark.parametrize("scheme", [None, "simultaneous"])
def test_tracing_does_not_perturb_the_run(scheme) -> None:
    """A traced run and run_movement at the same configuration agree record for
    record — the parity gate every extension must keep green."""
    kwargs = dict(seed=1234, horizon=3_000, mtd_scheme=scheme)
    tracer, traced = run_l3_trace("aggregate", **kwargs)
    untraced = run_movement("aggregate", **kwargs)

    assert traced.records == untraced.records
    assert traced.reached_objective == untraced.reached_objective
    assert traced.termination_time == untraced.termination_time
    assert traced.compromised_count == untraced.compromised_count


def test_events_are_in_simulated_time_order_and_all_layers_speak() -> None:
    tracer, _ = run_l3_trace("aggregate", seed=1234, horizon=3_000,
                             mtd_scheme="simultaneous")
    times = [e.time for e in tracer.events]
    assert times == sorted(times), "the log is not chronological"
    actors = {e.actor for e in tracer.events}
    for required in L3_ACTORS + ("ATTACKER", "DEFENDER", "MUTATION"):
        assert required in actors, f"no {required} events were narrated"


def test_dwell_only_places_are_narrated_under_the_partial_mapping() -> None:
    """v2_partial declares 7 tactics dwell-only; a walk long enough to visit one
    must say so rather than showing an unexplained silent step."""
    tracer, result = run_l3_trace("aggregate", seed=1234, horizon=3_000,
                                  mapping_version="v2_partial")
    dwell_only_records = [r for r in result.records
                          if r.place_class == "dwell-only"]
    if not dwell_only_records:
        pytest.skip("this seed's walk visited no dwell-only place")
    assert tracer.dwell_only_steps == len(dwell_only_records)
    assert any("dwell-only" in e.message for e in tracer.events
               if e.actor == "CONTROLLER")


def test_tallies_are_consistent_with_the_record_stream() -> None:
    tracer, result = run_l3_trace("aggregate", seed=7, horizon=3_000)
    assert tracer.steps == len(result.records)
    assert tracer.verdict_successes == sum(
        1 for r in result.records if r.verdict == "success")
    assert tracer.verdict_failures == sum(
        1 for r in result.records if r.verdict == "failure")
    assert tracer.blocked_dispatches == sum(1 for r in result.records if r.blocked)
    assert tracer.interrupted_steps == sum(
        1 for r in result.records if r.interrupted)
    assert tracer.dwell_time == pytest.approx(
        sum(r.dwell for r in result.records))


def test_a_stateful_run_traces_identically_to_run_movement() -> None:
    """The parity gate extends to the state seam: a traced stateful run and a
    run_movement stateful run at the same configuration and the same modulator
    agree record for record. Two independent states are constructed (the tracer
    cannot share the driver's), so this also pins that the state seed reproduces
    the walk regardless of who holds the state."""
    kwargs = dict(seed=1234, horizon=3_000, mapping_version="v2_partial")
    tracer, traced = run_l3_trace(
        "aggregate",
        attacker_state=AttackerState(seed=1234, modulators=(RevisitAversionDemo(),)),
        **kwargs,
    )
    untraced = run_movement(
        "aggregate",
        attacker_state=AttackerState(seed=1234, modulators=(RevisitAversionDemo(),)),
        **kwargs,
    )
    assert traced.records == untraced.records
    assert traced.termination_time == untraced.termination_time
    # The state actually reweighted something on this seed, or the parity is vacuous.
    assert tracer.modulated_decisions > 0


def test_a_stateful_run_narrates_the_state_evolving() -> None:
    """A stateful run whose narration does not show the state moving is a run
    nobody can debug (validation gate 5). With the demo modulator on, the STATE
    actor must both observe and reweight."""
    tracer, _ = run_l3_trace(
        "aggregate", seed=1234, horizon=3_000, mapping_version="v2_partial",
        attacker_state=AttackerState(seed=1234, modulators=(RevisitAversionDemo(),)),
    )
    state_events = [e for e in tracer.events if e.actor == "STATE"]
    assert any("OBSERVE" in e.message for e in state_events)
    assert any("MODULATE" in e.message for e in state_events)


def test_a_stateless_run_narrates_no_state_actor() -> None:
    """The STATE actor is silent when no state is attached — a stateless run's
    actor set is exactly what it was before this seam existed."""
    tracer, _ = run_l3_trace("aggregate", seed=7, horizon=2_000)
    assert not [e for e in tracer.events if e.actor == "STATE"]
    assert tracer.attacker_state is None


def test_undefended_run_narrates_no_defender_activity() -> None:
    tracer, _ = run_l3_trace("aggregate", seed=1234, horizon=2_000)
    assert not [e for e in tracer.events if e.actor in ("DEFENDER", "MUTATION")]
    assert tracer.mtd_triggered == 0
    assert tracer.penalty_time == 0.0
