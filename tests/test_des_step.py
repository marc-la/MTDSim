"""The DES step debugger must observe the simulation without changing it.

`tools/des_step.py` instruments the substrate to label each scheduled event with
what the simulator was doing. Instrumentation that perturbs the run would be worse
than none at all — every conclusion drawn by stepping through would be about a
different simulation than the one that produces the results. These tests pin the
non-interference, and pin the Brown 2023 behaviours the debugger is used to verify.
"""

from __future__ import annotations

import os
import random
import sys

import numpy as np
import pytest
import simpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACK_DURATION, ATTACKER_THRESHOLD
from mtdnetwork.operation.attack_operation import AttackOperation
from tools.des_step import GEOMETRY, DESDebugger


def _untraced_native(seed: int, horizon: float, mtd: str | None = None):
    """The same run the debugger builds, with no instrumentation at all."""
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(env=env, end_event=end_event, adversary=adversary,
                                proceed_time=0)
    if mtd:
        from mtdnetwork.operation.mtd_operation import MTDOperation
        from mtdnetwork.statistic.security_metric_statistics import (
            SecurityMetricStatistics,
        )
        MTDOperation(
            security_metrics_record=SecurityMetricStatistics(), env=env,
            end_event=end_event, network=network, attack_operation=attack_op,
            scheme=mtd, adversary=adversary, proceed_time=0, mtd_trigger_interval=200,
        ).proceed_mtd()
    attack_op.proceed_attack()
    env.run(until=horizon)
    return adversary


@pytest.mark.parametrize("mtd", [None, "simultaneous"])
def test_tracing_does_not_perturb_the_simulation(mtd) -> None:
    """A traced run and an untraced run of the same seed are byte-identical."""
    horizon = 4000.0
    untraced = _untraced_native(1234, horizon, mtd=mtd)

    dbg = DESDebugger.native(seed=1234, mtd=mtd)
    try:
        dbg.run_until(None, horizon=horizon)
        traced_record = dbg.adversary.get_attack_stats().get_record().to_csv(index=False)
        traced_hosts = list(dbg.adversary.get_compromised_hosts())
    finally:
        dbg.close()

    assert traced_record == untraced.get_attack_stats().get_record().to_csv(index=False), (
        "the debugger changed the attack record; instrumentation must be read-only"
    )
    assert traced_hosts == list(untraced.get_compromised_hosts())


def test_debugger_steps_one_event_at_a_time() -> None:
    """`step()` advances the SimPy queue by exactly one event and never rewinds."""
    dbg = DESDebugger.native(seed=1234)
    try:
        times = []
        for _ in range(40):
            state = dbg.step()
            if state is None:
                break
            times.append(state.now)
        assert len(times) == 40
        assert times == sorted(times), "simulated time went backwards"
        assert [s.step_index for s in dbg.trace] == list(range(1, 41))
    finally:
        dbg.close()


# --- the Brown 2023 behaviours the debugger is used to verify ---------------

def test_network_layer_mtd_costs_the_penalty_and_the_host_connection() -> None:
    """Brown B-INT-01 + B-ATK-07: a network-layer mutation (IP / host-topology
    shuffle) costs the attacker its connection to the host and a confusion penalty,
    so it must re-run host discovery."""
    dbg = DESDebugger.native(seed=0, mtd="simultaneous")
    try:
        hit = dbg.run_until(
            lambda w: "MTD INTERRUPT (network)" in w.note, horizon=15_000
        )
        assert hit is not None, "no network-layer interrupt occurred"
        # Step past the penalty and confirm both consequences landed.
        served = None
        for _ in range(30):
            state = dbg.step()
            if state is None:
                break
            if "penalty served" in state.note:
                served = state
                break
        assert served is not None, "the confusion penalty was never served"
        assert "cursor=cleared" in served.note, (
            "a network-layer mutation must clear the host cursor (B-INT-01)"
        )
        assert served.curr_host_id == -1
        assert served.now > hit.now, "the penalty consumed no simulated time"
    finally:
        dbg.close()


def test_application_layer_mtd_costs_the_penalty_but_keeps_the_host() -> None:
    """Brown B-INT-02: an application-layer mutation costs the *service* connection,
    not the host — the attacker re-runs the port scan on the host it still holds."""
    dbg = DESDebugger.native(seed=1234, mtd="simultaneous")
    try:
        hit = dbg.run_until(
            lambda w: "MTD INTERRUPT (application)" in w.note, horizon=15_000
        )
        assert hit is not None, "no application-layer interrupt occurred"
        served = None
        for _ in range(30):
            state = dbg.step()
            if state is None:
                break
            if "penalty served" in state.note:
                served = state
                break
        assert served is not None
        assert "cursor=kept" in served.note, (
            "an application-layer mutation must NOT clear the host cursor (B-INT-02)"
        )
        assert served.curr_host_id >= 0
    finally:
        dbg.close()


def test_a_host_is_given_up_at_brown_s_bound() -> None:
    """Brown B-ATK-06 / Table I: give up on a host after 10 attempts."""
    dbg = DESDebugger.native(seed=0, mtd="simultaneous")
    try:
        hit = dbg.run_until(lambda w: w.given_up > 0, horizon=15_000)
        assert hit is not None, "no host was ever given up"
        assert hit.max_attempt == ATTACKER_THRESHOLD, (
            f"a host was given up at {hit.max_attempt} attempts, not "
            f"{ATTACKER_THRESHOLD}"
        )
    finally:
        dbg.close()


def test_a_host_is_only_compromised_after_it_is_actually_attacked() -> None:
    """No compromise by contagion: every compromise is preceded by the adversary
    running a verb against *that* host.

    Vulnerability instances used to be shared between hosts, so exploiting one host
    marked the same vulnerability exploited everywhere and hosts fell without ever
    being touched.
    """
    dbg = DESDebugger.native(seed=1234)
    try:
        attacked: set[int] = set()
        compromised_without_attack = []
        for _ in range(6000):
            state = dbg.step()
            if state is None:
                break
            for verb in ("SCAN_PORT(host=", "EXPLOIT_VULN(host=", "BRUTE_FORCE(host="):
                if verb in state.note:
                    fragment = state.note.split(verb, 1)[1]
                    host_txt = fragment.split(")")[0].split(",")[0]
                    try:
                        attacked.add(int(host_txt))
                    except ValueError:
                        pass
            if "COMPROMISED host [" in state.note:
                host_id = int(state.note.split("COMPROMISED host [", 1)[1].split("]")[0])
                if host_id not in attacked:
                    compromised_without_attack.append((host_id, state.now))
        assert not compromised_without_attack, (
            f"hosts compromised without ever being attacked (contagion): "
            f"{compromised_without_attack[:5]}"
        )
        assert attacked, "the trace captured no attack activity at all"
    finally:
        dbg.close()


def test_verbs_cost_their_declared_durations() -> None:
    """The fixed-cost verbs consume exactly their `ATTACK_DURATION` in sim time."""
    dbg = DESDebugger.native(seed=1234)
    try:
        dbg.run_until(lambda w: "SCAN_PORT(host=" in w.note, horizon=15_000)
        # SCAN_HOST at t=5, ENUM_HOST at t=10, SCAN_PORT completing at t=35.
        noted = [s for s in dbg.trace if s.note]
        assert noted[0].now == ATTACK_DURATION["SCAN_HOST"]
        assert noted[1].now == (ATTACK_DURATION["SCAN_HOST"]
                                + ATTACK_DURATION["ENUM_HOST"])
        assert noted[2].now == (ATTACK_DURATION["SCAN_HOST"]
                                + ATTACK_DURATION["ENUM_HOST"]
                                + ATTACK_DURATION["SCAN_PORT"])
    finally:
        dbg.close()
