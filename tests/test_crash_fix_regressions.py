"""Regression tests for the Phase-2b crash-fix bundle.

Covers the two invariants the inherited code silently violated; if either
of these fails again, every headline metric is suspect.

  R1 — TimeNetwork.is_compromised must honour `terminate_compromise_ratio`
       (it was hard-coded to >0.25 from the 2024 "debug" commit).
  R3 — _mtd_execute_action must not leak its simpy.Resource slot when it
       early-returns on compromise (the abort path used to skip release()).

These run as a plain script (`python tests/test_crash_fix_regressions.py`)
and also as pytest (`pytest tests/test_crash_fix_regressions.py`).
"""

from __future__ import annotations

import os
import random
import sys

import numpy as np
import simpy

# Allow running directly from the repo root without `pip install -e .`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.operation.mtd_operation import MTDOperation
from mtdnetwork.statistic.security_metric_statistics import (
    SecurityMetricStatistics,
)


def _build_time_network(ratio: float) -> TimeNetwork:
    # Use the Phase-0 default geometry (50/8/4); 10/4/4 trips Finding F-06's
    # gen_graph infinite-loop guard. The threshold logic under test is
    # geometry-independent.
    random.seed(42)
    np.random.seed(42)
    return TimeNetwork(
        total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4,
        target_layer=4, total_database=2, terminate_compromise_ratio=ratio,
    )


def test_r1_is_compromised_honours_constructor_arg() -> None:
    """R1: the constructor's terminate_compromise_ratio must control the threshold."""
    tn_low = _build_time_network(ratio=0.5)
    assert tn_low.is_compromised(list(range(20))) is False  # 20/50 = 0.4 < 0.5
    assert tn_low.is_compromised(list(range(30))) is True   # 30/50 = 0.6 > 0.5

    tn_high = _build_time_network(ratio=0.9)
    assert tn_high.is_compromised(list(range(30))) is False  # 0.6 < 0.9
    assert tn_high.is_compromised(list(range(50))) is True   # 1.0 > 0.9


def test_r1_default_is_zhang_ncr() -> None:
    """Default termination ratio is 0.8 (Zhang 2023 §5 NCR), not the 0.25 debug leftover."""
    random.seed(42)
    np.random.seed(42)
    tn = TimeNetwork(
        total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4,
        target_layer=4, total_database=2,
    )
    assert tn.is_compromised(list(range(20))) is False  # 0.4 < 0.8
    assert tn.is_compromised(list(range(45))) is True   # 0.9 > 0.8


def test_r3_resource_released_when_sim_runs_to_compromise() -> None:
    """R3: every simpy.Resource slot must be free once the sim drains.

    Runs the PRIMARY 100-node config out to 15ks, then asserts both layer
    resources have zero held users. Pre-fix the early-return on
    `is_compromised` leaked one slot per layer, permanently parking the
    application and network resources.
    """
    random.seed(42)
    np.random.seed(42)

    env = simpy.Environment()
    end_event = env.event()
    tn = TimeNetwork(
        total_nodes=100, total_endpoints=5, total_subnets=8, total_layers=4,
        target_layer=4, total_database=2, terminate_compromise_ratio=0.8,
    )
    adv = Adversary(network=tn, attack_threshold=ATTACKER_THRESHOLD)
    ao = AttackOperation(env=env, end_event=end_event, adversary=adv,
                         proceed_time=0)
    ao.proceed_attack()
    mo = MTDOperation(
        security_metrics_record=SecurityMetricStatistics(),
        env=env, end_event=end_event, network=tn, scheme='random',
        attack_operation=ao, proceed_time=0,
        mtd_trigger_interval=200, custom_strategies=None, adversary=adv,
    )
    mo.proceed_mtd()

    env.run(until=15000)

    assert len(mo.network_layer_resource.users) == 0, (
        "R3 regression: network_layer_resource has held users at sim end"
    )
    assert len(mo.application_layer_resource.users) == 0, (
        "R3 regression: application_layer_resource has held users at sim end"
    )


if __name__ == "__main__":
    test_r1_is_compromised_honours_constructor_arg()
    print("R1 (constructor arg honoured): OK")
    test_r1_default_is_zhang_ncr()
    print("R1 (default = 0.8): OK")
    test_r3_resource_released_when_sim_runs_to_compromise()
    print("R3 (no resource leak at sim end): OK")
