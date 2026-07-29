"""The S5 sink policy: retrace instead of censor.

The gates are the ones ``docs/implementation/pipeline/ogasp/sink_policy.md`` §7
names. The first is the important one — ``censor`` must be bit-identical to the
behaviour that has always run, so the two arms differ by a parameter rather than
by wiring, exactly as the null-equivalence guarantees for the state seam, the
utility modulator and the learner do.
"""
from __future__ import annotations

import dataclasses

import pytest

from mtdsim.l3_simulation.movement import measures as M
from mtdsim.l3_simulation.movement.attacker import RETRACE, SINK_CENSOR, SINK_RETRACE
from mtdsim.l3_simulation.movement.net import PROFILES, load_routing_net
from mtdsim.l3_simulation.movement.run import run_movement

# The profiles whose nets carry a reachable sink (sink_policy.md §3). The other
# two have none, so the policy is inert on them — which is itself asserted below.
SINK_PROFILES = ("pure_steal", "double_extortion", "infrastructure_setup")
NO_SINK_PROFILES = ("aggregate", "pure_impediment")

MAPPING = "v2_partial"
OVERLAY = "v3_persistent_backward"


def _run(profile, seed, policy, horizon=6_000, **kw):
    return run_movement(
        profile,
        seed=seed,
        horizon=horizon,
        mapping_version=MAPPING,
        overlay_version=OVERLAY,
        sink_policy=policy,
        **kw,
    )


def _stream(result):
    return [dataclasses.asdict(r) for r in result.records]


# -- gate 1: the censor arm is bit-identical to today -----------------------


@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("seed", (0, 1, 7))
def test_censor_is_the_default_and_reproduces_an_unqualified_run(profile, seed):
    """An unqualified run and an explicit ``censor`` run are the same run — the
    registry convention the mapping and overlay versions already follow."""
    unqualified = run_movement(
        profile, seed=seed, horizon=6_000,
        mapping_version=MAPPING, overlay_version=OVERLAY,
    )
    censored = _run(profile, seed, SINK_CENSOR)
    assert _stream(unqualified) == _stream(censored)
    assert unqualified.reached_objective == censored.reached_objective
    assert unqualified.termination_time == censored.termination_time


# -- gate 2: the policy is inert where there is no sink ---------------------


@pytest.mark.parametrize("profile", NO_SINK_PROFILES)
def test_retrace_changes_nothing_on_a_net_with_no_sink(profile):
    """The policy fires only at a sink, so on a net without one the two arms are
    the same run. This is what makes a sink-policy contrast attributable."""
    assert not any(
        load_routing_net(profile, with_synthetic_overlay=True).is_sink(p)
        for p in load_routing_net(profile, with_synthetic_overlay=True).places
    )
    assert _stream(_run(profile, 0, SINK_CENSOR)) == _stream(_run(profile, 0, SINK_RETRACE))


# -- gate 3: retrace fires where the censor arm died ------------------------


def test_retrace_continues_a_walk_that_censoring_ended():
    """The finding this policy exists to remove: a profile that dies at a sink
    now keeps walking, and observes a longer window for it."""
    censored = _run("double_extortion", 0, SINK_CENSOR, horizon=15_000)
    retraced = _run("double_extortion", 0, SINK_RETRACE, horizon=15_000)

    assert M.terminal_mode(censored) == "sink"
    assert M.terminal_mode(retraced) != "sink"
    assert M.retrace_count(censored) == 0
    assert M.retrace_count(retraced) >= 1
    assert len(retraced.records) > len(censored.records)
    assert retraced.termination_time > censored.termination_time


def test_the_two_arms_share_a_prefix_up_to_the_first_sink():
    """One factor moved: the walks are identical until the sink is reached, and
    diverge only there. Anything else would mean the policy perturbed the run's
    randomness rather than extending it."""
    censored = _run("double_extortion", 0, SINK_CENSOR, horizon=15_000)
    retraced = _run("double_extortion", 0, SINK_RETRACE, horizon=15_000)
    n = len(censored.records)
    assert _stream(retraced)[: n] == _stream(censored)[: n]


# -- gate 4: what a retrace costs and records -------------------------------


def test_a_retrace_record_consumes_no_time_and_dispatches_nothing():
    """sink_policy.md §4: the retreat itself is instantaneous and un-actioned;
    the cost is the re-visit it causes."""
    retraced = _run("double_extortion", 0, SINK_RETRACE, horizon=15_000)
    retraces = [r for r in retraced.records if r.place_class == RETRACE]
    assert retraces
    for r in retraces:
        assert r.dwell == 0.0
        assert r.start_time == r.end_time
        assert r.verb == ""
        assert r.verdict == ""
        assert r.next_place is not None


def test_the_walk_still_consumes_time_across_a_retrace():
    """The property that makes a retrace loop impossible in zero simulated time:
    the re-visit pays a dwell, so the clock strictly advances around the cycle."""
    retraced = _run("double_extortion", 0, SINK_RETRACE, horizon=15_000)
    records = retraced.records
    for i, r in enumerate(records):
        if r.place_class != RETRACE or i + 1 >= len(records):
            continue
        following = records[i + 1]
        assert following.place == r.next_place
        assert following.end_time > r.end_time


def test_a_retrace_is_excluded_from_every_action_denominator():
    """sink_policy.md §6: attempted-action counts, blocked fractions and verb
    mixes must not move because the policy did."""
    retraced = _run("double_extortion", 0, SINK_RETRACE, horizon=15_000)
    assert M.retrace_count(retraced) >= 1
    for record in M.action_records(retraced):
        assert record.place_class != RETRACE
    for record in M.visit_records(retraced):
        assert record.place_class != RETRACE
    for record in M.routed_records(retraced):
        assert record.place_class != RETRACE


def test_a_retrace_does_not_enter_the_diversity_measures():
    """A retrace is the policy moving the token, not the net branching, so it
    must not appear as a routing decision — otherwise a retraced run would score
    lower path entropy for a reason that is the policy's."""
    retraced = _run("double_extortion", 0, SINK_RETRACE, horizon=15_000)
    sequence = M.place_sequence(retraced)
    assert len(sequence) == len(retraced.records) - M.retrace_count(retraced)


# -- gate 5: no oscillation, as §3 predicts ---------------------------------


@pytest.mark.parametrize("profile", SINK_PROFILES)
def test_the_walk_does_not_cycle_into_the_max_events_backstop(profile):
    """The no-oscillation argument, checked rather than trusted: with retracing
    on, no profile with a sink runs away into the backstop."""
    result = _run(profile, 0, SINK_RETRACE, horizon=15_000)
    assert M.terminal_mode(result) != "max_events"


def test_retraces_are_rare_as_the_out_degree_argument_predicts():
    """§3 predicts about 1.1 retraces per sink encounter, because the heaviest
    edge into any sink carries weight 0.111. A run that retraced far more than
    it encountered sinks would falsify the structural argument, not just look
    untidy."""
    retraced = _run("double_extortion", 0, SINK_RETRACE, horizon=15_000)
    sink_arrivals = sum(
        1 for r in M.routed_records(retraced)
        if r.next_place is None or r.place == "credential-access"
    )
    assert M.retrace_count(retraced) <= 3 * max(1, sink_arrivals)


# -- gate 6: determinism (SIM-05) -------------------------------------------


@pytest.mark.parametrize("policy", (SINK_CENSOR, SINK_RETRACE))
def test_same_seed_same_walk_under_either_policy(policy):
    assert _stream(_run("double_extortion", 3, policy)) == _stream(
        _run("double_extortion", 3, policy)
    )


def test_the_policy_draws_no_randomness_of_its_own():
    """Retracing must not consume from the token sampler, or the two arms would
    diverge after the first sink for a reason that is not the policy. Checked by
    running a no-sink profile under both arms with everything else equal — any
    stream consumption would desynchronise it."""
    for profile in NO_SINK_PROFILES:
        for seed in (0, 5):
            assert _stream(_run(profile, seed, SINK_CENSOR)) == _stream(
                _run(profile, seed, SINK_RETRACE)
            )


# -- gate 7: the surface refuses what it does not know ----------------------


def test_an_unknown_policy_is_refused_loudly():
    with pytest.raises(ValueError, match="unknown sink_policy"):
        _run("aggregate", 0, "bounce")


def test_overlay_version_and_overlay_object_are_mutually_exclusive():
    """The symmetric partner to the mapping surface's own guard."""
    from mtdsim.l3_simulation.controller import load_outcome_overlay

    with pytest.raises(ValueError, match="not both"):
        run_movement(
            "aggregate", seed=0, horizon=1_000,
            overlay=load_outcome_overlay(version=OVERLAY),
            overlay_version=OVERLAY,
        )


def test_overlay_version_names_the_same_run_as_the_constructed_object():
    """Naming the version and passing the object must be the same run — the
    parameter is a convenience at the seam, not a second code path."""
    from mtdsim.l3_simulation.controller import load_outcome_overlay

    by_name = run_movement(
        "aggregate", seed=0, horizon=4_000,
        mapping_version=MAPPING, overlay_version=OVERLAY,
    )
    by_object = run_movement(
        "aggregate", seed=0, horizon=4_000,
        mapping_version=MAPPING, overlay=load_outcome_overlay(version=OVERLAY),
    )
    assert _stream(by_name) == _stream(by_object)
