"""Validation-gate tests for the movement-layer attacker (the SimPy net-walker).

Covers the M7 handoff's gates that live on the attacker:

  G2  determinism (SIM-05): same net + overlay + seed -> identical event records.
  G3  the feedback loop is real: a forced failure verdict (incl. an MTD interrupt
      mid-action) produces a backward/retry transition a forced success does not.
  consume-not-fork: the driver carries no verdict / composition semantics — it
      calls the injected controller collaborators (spied here).
  precondition-unmet: a verb the net dispatches without its substrate context is
      read as a failure and recorded, not crashed or silently degenerated.

The overlay ``compose`` and the verdict adapter are the controller-finalisation
handoff's surface; here they are injected as controlled fakes so the driver logic
is proven independently of the (still-in-flight) overlay numbers.
"""
from __future__ import annotations

import random

import numpy as np
import simpy
import pytest

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.operation.attack_operation import (
    EXPLOIT_COMPROMISED,
    AttackOperation,
)

from mtdsim.l3_simulation.controller import load_controller
from mtdsim.l3_simulation.movement.attacker import MovementAttacker
from mtdsim.l3_simulation.movement.net import RoutingNet, load_routing_net

GEOMETRY = dict(
    total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4,
    target_layer=4, total_database=2, terminate_compromise_ratio=0.8,
)


# --- controlled collaborators ----------------------------------------------
def outcome_verdict(verb, outcome, interrupted):
    """A realistic verdict adapter: an interrupt or a negative outcome is a
    failure; a compromise / positive outcome is a success."""
    if interrupted:
        return "failure"
    return "success" if outcome in (True, EXPLOIT_COMPROMISED) else "failure"


class RefOverlay:
    """A reference composer implementing the documented M2 multiply-renormalise
    rule with a simple factor table: success keeps the base distribution; failure
    biases toward the lexicographically-first destination (a stand-in 'retry')."""

    def __init__(self):
        self.calls = []

    def compose(self, src, verdict, base):
        self.calls.append((src, verdict, dict(base)))
        if verdict == "success":
            factor = {d: 1.0 for d in base}
        else:
            factor = {d: (1.0 if d == min(base) else 0.3) for d in base}
        num = {d: base[d] * factor[d] for d in base}
        z = sum(num.values())
        return {d: v / z for d, v in num.items()} if z > 0 else {}


class ForcedVerdict:
    """A verdict adapter forced to one verdict, counting its calls."""

    def __init__(self, verdict):
        self.verdict = verdict
        self.calls = 0

    def __call__(self, verb, outcome, interrupted):
        self.calls += 1
        return self.verdict


class SwitchOverlay:
    """success routes only forward, failure routes only backward — a crisp
    demonstration that the verdict selects the out-set."""

    def compose(self, src, verdict, base):
        if verdict == "success":
            keep = {d: w for d, w in base.items() if d == "fwd"}
        else:
            keep = {d: w for d, w in base.items() if d == "back"}
        z = sum(keep.values())
        return {d: w / z for d, w in keep.items()} if z > 0 else {}


class FakeMTD:
    def __init__(self, resource_type):
        self._rt = resource_type

    def get_resource_type(self):
        return self._rt

    def get_name(self):
        return "FakeMTD"


def _fresh(profile, seed, *, overlay, verdict_of, register=False,
           with_synthetic_overlay=True):
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(env=env, end_event=end_event, adversary=adversary,
                                proceed_time=0)
    routing_net = load_routing_net(profile, with_synthetic_overlay=with_synthetic_overlay)
    attacker = MovementAttacker(
        env=env, end_event=end_event, adversary=adversary, attack_operation=attack_op,
        routing_net=routing_net, controller=load_controller(), overlay=overlay,
        verdict_of=verdict_of, seed=seed, register_for_interrupts=register,
    )
    return env, end_event, attack_op, attacker


# --- G3: the feedback loop is real (forced verdict) -------------------------
def test_g3_forced_success_and_failure_select_different_transitions() -> None:
    """The routing feedback: at the same place, a success and a failure verdict
    select different out-sets. Deterministic — a directed unit test of _route."""
    net = RoutingNet(
        profile="unit", places=("a", "fwd", "back"), entry_place="a",
        with_synthetic_overlay=False,
        _out={"a": {"fwd": 0.5, "back": 0.5}, "fwd": {}, "back": {}},
    )
    attacker = MovementAttacker(
        env=simpy.Environment(), end_event=simpy.Environment().event(),
        adversary=None, attack_operation=None, routing_net=net,
        controller=None, overlay=SwitchOverlay(), verdict_of=outcome_verdict,
        dwell_catalogue={}, seed=1,
    )
    # Repeated draws are stable to the verdict, and the two verdicts diverge.
    assert {attacker._route("a", "success") for _ in range(20)} == {"fwd"}
    assert {attacker._route("a", "failure") for _ in range(20)} == {"back"}


def test_g3_interrupt_reads_as_failure_and_routes() -> None:
    """An MTD interrupt mid-walk produces a failure-verdict transition — the
    interrupt-as-failure feedback. Injected deterministically.

    Two outcome tags can carry an interrupt now that every place visit occupies
    time. ``MTD_INTERRUPT`` is a mutation that cut a running action or a
    dwell-only place short. ``PRECONDITION_UNMET`` is a mutation that landed while
    the attacker was spending the tactic's time on an attempt the substrate could
    not action — impossible before, when a blocked attempt consumed no time and so
    presented no window to interrupt. The blocked tag is kept rather than
    overwritten because the blocked fraction is the H-coupling finding; the
    defensive event is carried by the ``interrupted`` flag, which is what analyses
    key on.
    """
    env, end_event, attack_op, attacker = _fresh(
        "infrastructure_setup", 7, overlay=RefOverlay(),
        verdict_of=outcome_verdict, register=True,
    )
    attacker.start()

    def interrupter():
        for t in (30, 40, 50):
            yield env.timeout(t)
            attack_op.set_interrupted_mtd(FakeMTD("network"))
            proc = attack_op.get_attack_process()
            if proc is not None and proc.is_alive:
                proc.interrupt()

    env.process(interrupter())
    env.run(until=400)

    interrupted = [r for r in attacker.records if r.interrupted]
    assert interrupted, "no interrupt was read by the driver"
    for rec in interrupted:
        assert rec.outcome in {"MTD_INTERRUPT", "PRECONDITION_UNMET"}
        assert rec.verdict == "failure"
        assert rec.interrupted_by == "network"
        # Whichever tag it carries, an interrupted event never claims more time
        # than it occupied: the draw was cut short and the record says so.
        assert rec.dwell <= (rec.end_time - rec.start_time) + 1e-9


# --- G2: determinism (SIM-05) ----------------------------------------------
def test_g2_same_seed_identical_records() -> None:
    def run():
        env, _e, _ao, attacker = _fresh(
            "double_extortion", 1234, overlay=RefOverlay(),
            verdict_of=outcome_verdict,
        )
        attacker.start()
        env.run(until=3000)
        return [
            (r.step_index, r.place, r.verb, r.outcome, r.verdict, r.next_place)
            for r in attacker.records
        ]

    assert run() == run()
    assert len(run()) > 1  # non-degenerate


# --- consume-not-fork -------------------------------------------------------
def test_driver_delegates_verdict_and_composition() -> None:
    """The driver holds no verdict/composition logic: it calls the injected
    verdict adapter and overlay.compose. Spy on both."""
    overlay = RefOverlay()
    verdict = ForcedVerdict("success")
    env, _e, _ao, attacker = _fresh(
        "double_extortion", 5, overlay=overlay, verdict_of=verdict,
    )
    attacker.start()
    env.run(until=1500)

    assert verdict.calls > 0, "verdict adapter was never consulted"
    assert overlay.calls, "overlay.compose was never consulted"
    # Every composition the driver did was on a verdict the adapter returned.
    assert {v for _, v, _ in overlay.calls} <= {"success", "failure"}


# --- precondition-unmet is a recorded failure, not a crash ------------------
def test_precondition_unmet_is_recorded_failure() -> None:
    """Driving a chain-bound verb without its context reads as a failure and is
    recorded PRECONDITION_UNMET (the H-coupling surfaces as data, not silence)."""
    # The aggregate overlay-on arm routes off recon into verbs needing curr_host
    # before ENUM_HOST sets it, so blocks are guaranteed.
    env, _e, _ao, attacker = _fresh(
        "aggregate", 1234, overlay=RefOverlay(), verdict_of=outcome_verdict,
    )
    attacker.start()
    env.run(until=2000)
    blocked = [r for r in attacker.records if r.blocked]
    assert blocked, "expected at least one precondition-unmet block"
    for rec in blocked:
        assert rec.outcome == "PRECONDITION_UNMET"
        assert rec.verdict == "failure"


def test_records_end_with_a_terminal_event() -> None:
    """The walk's end (sim end / stall / max-events) is visible in the records."""
    env, _e, _ao, attacker = _fresh(
        "double_extortion", 2, overlay=RefOverlay(), verdict_of=outcome_verdict,
    )
    attacker.start()
    env.run(until=3000)
    assert attacker.records
    # A stall/sink ends the walk with next_place None; a terminal event carries an
    # empty verdict. Either way the last record marks the stop.
    last = attacker.records[-1]
    assert last.next_place is None or last.outcome in ("SIM_END", "MAX_EVENTS")
