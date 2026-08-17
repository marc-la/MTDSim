"""The S5 sink-retrace policy — its seven design gates, as tests.

A token reaching a place the corpus drew no exit from steps back to where it
came from, with that one edge suppressed for one selection, instead of the run
being censored there. The policy's whole risk is that it turns a censored walk
into an *uninformative* one — a token oscillating between two places for the
rest of the run — so the oscillation guard, the time cost and the disjointness
from the substrate's own precondition failures are each pinned rather than
argued.

Design record: docs/implementation/pipeline/ogasp/sink_retrace_design.md; the
gates below are its §6, in order.
"""
from __future__ import annotations

import dataclasses

import pytest

from mtdsim.l3_simulation.movement.attacker import MovementAttacker, MovementRecord
from mtdsim.l3_simulation.movement.measures import terminal_mode
from mtdsim.l3_simulation.movement.net import PROFILES, load_routing_net
from mtdsim.l3_simulation.movement.run import run_movement

SEEDS = (0, 7, 42, 1234)
HORIZON = 15_000

# The profiles whose nets carry a sink under the overlay-on arm, and those that
# do not — the second group is the internal control on the whole change.
# Re-pinned 2026-08-17 after Marc's membership rulings (19/8/6/5 -> 19/7/7/5):
# `objective_impact` lost SearchAwesome and with it `collection`'s only
# out-edge, so it now carries a sink (`collection`) and is no longer a control;
# `objective_none_c2`'s sink moved from `defense-impairment` to
# `privilege-escalation`. Only the aggregate is sinkless now.
SINK_PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
)
SINKLESS_PROFILES = ("aggregate",)

# Carrying a sink and *reaching* it are different things, and the difference is a
# fact about the synthetic pre-intrusion overlay rather than about the policy.
# Before 2026-08-17 `objective_none_c2` had `defense-impairment` as a structural
# sink but never walked into it with the overlay on (0 retraces over 10 seeds),
# retracing only with the overlay off (stranding at `reconnaissance` /
# `resource-development`). Its post-ruling sink `privilege-escalation` is
# reached on both arms (~20 retraces per seed), so every class now retraces
# with the overlay on; the arm is still part of the case, and the tests that
# would otherwise pass vacuously say which arm they mean.
RETRACING_ARMS = (
    ("objective_exfiltration", True),
    ("objective_impact", True),
    ("objective_exfiltration_impact", True),
    ("objective_none_c2", True),
    ("objective_none_c2", False),
)


def _run(profile, *, retrace, seed=0, **kwargs):
    kwargs.setdefault("mapping_version", "v2_partial")
    kwargs.setdefault("mtd_scheme", None)
    return run_movement(
        profile, seed=seed, horizon=HORIZON, retrace_sinks=retrace, **kwargs
    )


def _fields(records):
    return [dataclasses.asdict(r) for r in records]


# --- gate 4 (first, because it bounds the blast radius) ----------------------


@pytest.mark.parametrize("profile", SINKLESS_PROFILES)
@pytest.mark.parametrize("seed", SEEDS)
def test_gate4_sinkless_profiles_are_bit_identical(profile, seed) -> None:
    """A profile whose net has no sink cannot be reached by this policy, so its
    record stream must be equal field for field with the policy on and off.

    This is what makes the two sinkless profiles the internal control on the
    change: if their numbers move in experiment 2, something other than the
    retrace moved them.
    """
    for scheme in (None, "simultaneous"):
        off = _run(profile, retrace=False, seed=seed, mtd_scheme=scheme)
        on = _run(profile, retrace=True, seed=seed, mtd_scheme=scheme)
        assert _fields(off.records) == _fields(on.records)
        assert on.retrace_count == 0


@pytest.mark.parametrize("profile", PROFILES)
def test_policy_off_is_todays_behaviour(profile) -> None:
    """The default is off, so an unqualified run reproduces what has always run —
    the same discipline the mapping and overlay registries follow."""
    default = _run(profile, retrace=False, seed=0)
    unqualified = run_movement(
        profile, seed=0, horizon=HORIZON, mapping_version="v2_partial", mtd_scheme=None
    )
    assert _fields(default.records) == _fields(unqualified.records)


# --- gate 2: the profiles that died at a sink now continue -------------------


@pytest.mark.parametrize("profile", SINK_PROFILES)
@pytest.mark.parametrize("seed", SEEDS)
def test_gate2_sink_profiles_no_longer_terminate_at_a_sink(profile, seed) -> None:
    """The reason the policy exists. A walk that ended at a sink must now end for
    a reason that belongs to the experiment (the horizon, the objective, the
    event backstop) rather than to the corpus running out of edges."""
    on = _run(profile, retrace=True, seed=seed)
    assert terminal_mode(on) != "sink"
    assert terminal_mode(on) != "sink_exhausted"


def test_gate2_the_truncated_window_actually_opens() -> None:
    """Stated as the effect the handoff predicted rather than as a bare mode
    change. The censored profiles observed a truncated *window*: they stopped
    early in sim time, which is what shortened their per-profile denominator
    relative to the profiles that ran the full horizon. So the assertion is on
    the window, not on the event count — the event count is a consequence."""
    for profile in ("objective_exfiltration", "objective_exfiltration_impact"):
        off = _run(profile, retrace=False)
        on = _run(profile, retrace=True)
        assert terminal_mode(off) == "sink"
        assert on.termination_time > off.termination_time
        assert on.termination_time > 0.9 * HORIZON
        assert len(on.records) > len(off.records)


# --- gate 1: no walk loops without consuming time ---------------------------


@pytest.mark.parametrize("profile,overlay", RETRACING_ARMS)
def test_gate1_every_retrace_costs_time_and_the_count_is_finite(profile, overlay) -> None:
    """A zero-time retrace is an infinite loop in zero simulated time — a hang,
    not a result. Each retraced visit is an ordinary visit and pays an ordinary
    draw, so every one of them must have consumed time, and the run must end.

    Pooled over seeds because whether a given seed reaches a given sink is
    itself stochastic, and run on the arm where each profile actually strands
    (RETRACING_ARMS) so that no cell passes vacuously.
    """
    total_retraces = 0
    for seed in SEEDS:
        on = _run(profile, retrace=True, seed=seed, with_synthetic_overlay=overlay)
        retraced = [r for r in on.records if r.retrace]
        total_retraces += len(retraced)
        for record in retraced:
            assert record.end_time > record.start_time
            assert record.dwell > 0.0
        # Bounded in practice, without a declared budget: the one-shot
        # suppression forces a different move each time and each retrace pays
        # the horizon down.
        assert on.retrace_count < len(on.records)
    assert total_retraces, f"{profile} never retraced — the gate would pass vacuously"


@pytest.mark.parametrize("profile,overlay", RETRACING_ARMS)
def test_gate1_retraces_are_a_small_fraction_of_the_walk(profile, overlay) -> None:
    """The design declined a retrace budget on the argument that the policy
    cannot oscillate. That argument is only worth keeping if the observed
    frequency stays low — so the frequency is asserted, not assumed. A failure
    here is the design's premise breaking, and the response is to re-open §3.4,
    not to raise the threshold."""
    total = 0
    for seed in SEEDS:
        on = _run(profile, retrace=True, seed=seed, with_synthetic_overlay=overlay)
        # Whether a given seed reaches a sink at all is stochastic (exfiltration
        # seed 42 does not, post-2026-08-17); non-vacuity is asserted pooled.
        total += on.retrace_count
        assert on.retrace_count / len(on.records) < 0.10
    assert total > 0, f"{profile} never retraced — the gate would pass vacuously"


# --- gate 3: determinism (SIM-05), and no new RNG stream --------------------


@pytest.mark.parametrize("profile", SINK_PROFILES)
@pytest.mark.parametrize("seed", SEEDS)
def test_gate3_determinism(profile, seed) -> None:
    """Same seed, same walk. The policy is a deterministic function of the walk's
    own history, so it introduces no randomness of its own."""
    first = _run(profile, retrace=True, seed=seed)
    second = _run(profile, retrace=True, seed=seed)
    assert _fields(first.records) == _fields(second.records)


def test_gate3_prefix_before_the_first_sink_is_untouched() -> None:
    """The stronger form of "no new RNG stream": up to the moment the policy
    first fires, the retrace-on and retrace-off walks must be the *same walk*.
    A policy that perturbed a shared random stream would diverge earlier than
    its first intervention."""
    for profile, overlay in RETRACING_ARMS:
        off = _run(profile, retrace=False, with_synthetic_overlay=overlay)
        on = _run(profile, retrace=True, with_synthetic_overlay=overlay)
        shared = len(off.records)
        # The off-arm's last record is where it was censored; everything before
        # it must match the on-arm record for record.
        assert _fields(on.records[: shared - 1]) == _fields(off.records[: shared - 1])


# --- gate 5: the suppression is one-shot ------------------------------------


def test_gate5_suppression_is_one_shot() -> None:
    """The edge that led into the sink is removed from the next selection and
    from no other. Asserted directly on the driver's own routing seam, because
    the property is about a single selection and a run-level statistic cannot
    see it."""
    net = load_routing_net("objective_exfiltration", with_synthetic_overlay=True)
    attacker = MovementAttacker.__new__(MovementAttacker)  # no sim needed
    attacker.routing = net
    attacker._visited = ["execution", "impact"]
    attacker._suppressed_edge = None
    attacker._retrace_pending = False
    attacker.retrace_count = 0
    attacker.retrace_sinks = True

    destination, exhausted = MovementAttacker._maybe_retrace(attacker, "impact", None)
    assert destination == "execution" and not exhausted
    assert attacker._suppressed_edge == ("execution", "impact")

    # Consumed by the next selection at that place...
    class _Passthrough:
        def compose(self, src, verdict, base):
            return dict(base)

    attacker.overlay = _Passthrough()
    import random

    attacker._rng = random.Random(0)
    for _ in range(200):
        assert attacker._route("execution", "failure") != "impact"
        # ...and only the first of those selections was suppressed.
        assert attacker._suppressed_edge is None
        if "impact" in attacker.routing.base_out_weights("execution"):
            break
    # A later occasion sees the full out-set again: with the suppression cleared,
    # the sink is reachable from `execution` once more.
    seen = {attacker._route("execution", "failure") for _ in range(2_000)}
    assert "impact" in seen


def test_gate5_a_retrace_flag_lands_on_exactly_one_record() -> None:
    """The flag belongs to the record the retraced-to visit writes, and to that
    record only — otherwise the retrace count read off the records would not
    match the driver's."""
    on = _run("objective_exfiltration", retrace=True)
    assert on.retrace_count > 0
    assert sum(1 for r in on.records if r.retrace) == on.retrace_count


# --- gate 6: retrace and PRECONDITION_UNMET stay disjoint -------------------


@pytest.mark.parametrize("profile,overlay", RETRACING_ARMS)
def test_gate6_retrace_never_routes_around_an_unmet_precondition(profile, overlay) -> None:
    """The H-coupling finding is a result this evaluation exists to expose, and a
    policy that quietly routed around unmet preconditions would hide it. A
    retrace answers a structural dead end in the corpus; a blocked verb still
    costs its time, still records PRECONDITION_UNMET and still routes on the
    failure column exactly as before.
    """
    on = _run(profile, retrace=True, with_synthetic_overlay=overlay)
    # The retraced visit is an ordinary visit: it may itself be blocked, but the
    # retrace is never *triggered* by a block. The trigger is always a sink.
    net = load_routing_net(profile, with_synthetic_overlay=overlay)
    for previous, record in zip(on.records, on.records[1:]):
        if record.retrace:
            assert net.is_sink(previous.place), (
                "a retrace fired somewhere other than a sink"
            )
    # And blocking is still visible and still priced.
    blocked = [r for r in on.records if r.blocked]
    for record in blocked:
        assert record.outcome == "PRECONDITION_UNMET"
        assert record.verdict == "failure"


# --- gate 7: the degenerate paths, on a constructed net ---------------------


class _StubNet:
    """A net the corpus cannot produce: a sink whose only predecessor has no
    other way out, so the policy must walk further back — and, at the end of the
    chain, run out of places entirely."""

    profile = "stub"
    entry_place = "a"

    def __init__(self, out):
        self._out = out
        self.places = tuple(out)

    def base_out_weights(self, place):
        return dict(self._out[place])

    def out_places(self, place):
        return tuple(sorted(self._out.get(place, {})))

    def is_sink(self, place):
        return not self._out.get(place)


def _stub_attacker(net, visited):
    attacker = MovementAttacker.__new__(MovementAttacker)
    attacker.routing = net
    attacker._visited = list(visited)
    attacker._suppressed_edge = None
    attacker._retrace_pending = False
    attacker.retrace_count = 0
    attacker.retrace_sinks = True
    return attacker


def test_gate7_walks_further_back_when_suppression_empties_an_out_set() -> None:
    """`b` leads only to the sink `c`, so suppressing b→c leaves it with nothing;
    the policy must step back past it to `a`, suppressing a→b instead."""
    net = _StubNet({"a": {"b": 1.0, "d": 1.0}, "b": {"c": 1.0}, "c": {}, "d": {}})
    attacker = _stub_attacker(net, ["a", "b", "c"])
    destination, exhausted = MovementAttacker._maybe_retrace(attacker, "c", None)
    assert destination == "a" and not exhausted
    assert attacker._suppressed_edge == ("a", "b")


def test_gate7_stack_exhausted_is_recorded_distinctly() -> None:
    """When the whole chain is exhausted the walk ends — but as SINK_EXHAUSTED,
    never as a plain sink. Collapsing the two would let a policy that never fired
    read as a policy that fired and failed."""
    net = _StubNet({"a": {"b": 1.0}, "b": {"c": 1.0}, "c": {}})
    attacker = _stub_attacker(net, ["a", "b", "c"])
    destination, exhausted = MovementAttacker._maybe_retrace(attacker, "c", None)
    assert destination is None and exhausted is True


def test_gate7_a_stall_is_not_absorbed_by_this_policy() -> None:
    """A stall (the overlay suppressing every out-edge at a place that *has* base
    edges) and a sink (the corpus drawing no edge at all) differ in what they
    mean — one is the verdict speaking, the other is the corpus. The retrace
    deliberately declines the stall."""
    net = _StubNet({"a": {"b": 1.0}, "b": {"a": 1.0}})
    attacker = _stub_attacker(net, ["a", "b"])
    # `b` is not a sink, so routing returning None there is a stall, and the
    # policy must leave it alone.
    destination, exhausted = MovementAttacker._maybe_retrace(attacker, "b", None)
    assert destination is None and exhausted is False
    assert attacker.retrace_count == 0


def test_gate7_first_place_a_sink_terminates_without_a_predecessor() -> None:
    """No predecessor exists to step back to. Unreachable on the current nets
    (every entry place has an out-set) and handled anyway."""
    net = _StubNet({"a": {}})
    attacker = _stub_attacker(net, ["a"])
    destination, exhausted = MovementAttacker._maybe_retrace(attacker, "a", None)
    assert destination is None and exhausted is True


# --- the record schema addition ---------------------------------------------


def test_retrace_defaults_false_on_the_record() -> None:
    """Every existing construction site keeps working, and a record that says
    nothing about retracing is not a retrace."""
    record = MovementRecord(
        profile="p",
        step_index=0,
        place="a",
        verb="",
        outcome="DWELL_ONLY",
        verdict="",
        interrupted=False,
        blocked=False,
        next_place=None,
        start_time=0.0,
        end_time=1.0,
        dwell=1.0,
        interrupted_by="",
    )
    assert record.retrace is False
