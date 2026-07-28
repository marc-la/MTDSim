"""The event-log tracer must observe the simulation without changing it, and must
narrate every actor in the contest.
"""

from __future__ import annotations

import random

import numpy as np
import pytest
import simpy

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.trace import run_trace

GEOMETRY = dict(
    total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4,
    target_layer=4, total_database=2, terminate_compromise_ratio=0.8,
)


def _untraced(seed: int, horizon: float, scheme: str | None = None):
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(env=env, end_event=end_event, adversary=adversary,
                                proceed_time=0)
    if scheme:
        from mtdnetwork.operation.mtd_operation import MTDOperation
        from mtdnetwork.statistic.security_metric_statistics import (
            SecurityMetricStatistics,
        )
        MTDOperation(
            security_metrics_record=SecurityMetricStatistics(), env=env,
            end_event=end_event, network=network, attack_operation=attack_op,
            scheme=scheme, adversary=adversary, proceed_time=0,
            mtd_trigger_interval=None,
        ).proceed_mtd()
    attack_op.proceed_attack()
    env.run(until=horizon)
    return adversary


@pytest.mark.parametrize("scheme", ["none", "simultaneous"])
def test_tracing_does_not_perturb_the_simulation(scheme) -> None:
    """A traced run and an untraced run of the same seed agree exactly.

    Instrumentation that changed the run would make every conclusion drawn from
    the log a conclusion about a different simulation.
    """
    horizon = 2000.0
    tracer, _ = run_trace(scheme=scheme, seed=1234, finish_time=horizon)
    untraced = _untraced(1234, horizon, scheme=None if scheme == "none" else scheme)

    assert list(tracer.adversary.get_compromised_hosts()) == \
        list(untraced.get_compromised_hosts())
    assert (tracer.adversary.get_attack_stats().get_record().to_csv(index=False)
            == untraced.get_attack_stats().get_record().to_csv(index=False))


def test_events_are_in_simulated_time_order() -> None:
    tracer, _ = run_trace(scheme="random", seed=1234, finish_time=1500)
    times = [e.time for e in tracer.events]
    assert times == sorted(times), "the log is not chronological"
    assert len(tracer.events) > 10


def test_all_three_actors_are_narrated_under_a_defence() -> None:
    """A defended run must show the attacker working, the defence firing, the
    network mutating, and the attacker being set back — otherwise the log cannot
    show how the contest went."""
    tracer, _ = run_trace(scheme="simultaneous", seed=1234, finish_time=2000)
    actors = {e.actor for e in tracer.events}
    for required in ("ATTACKER", "DEFENDER", "MUTATION", "INTERRUPT", "COMPROMISE"):
        assert required in actors, f"no {required} events were narrated"


def test_undefended_run_narrates_no_defender_activity() -> None:
    tracer, _ = run_trace(scheme="none", seed=1234, finish_time=1500)
    assert not [e for e in tracer.events if e.actor in ("DEFENDER", "MUTATION")]
    assert tracer.mtd_triggered == 0
    assert tracer.interrupts == 0
    assert tracer.penalty_time == 0.0


def test_defence_delays_the_attacker_s_foothold() -> None:
    """The headline the tool exists to show: the same attacker, same seed, takes
    materially longer to get its first host when a defence is running."""
    undefended, _ = run_trace(scheme="none", seed=1234, finish_time=2000)
    defended, _ = run_trace(scheme="simultaneous", seed=1234, finish_time=2000)

    assert undefended.first_compromise is not None, "control run never got in"
    assert defended.first_compromise is not None, "defended run never got in"
    assert defended.first_compromise > undefended.first_compromise, (
        "the defence did not delay the foothold at all"
    )
    assert defended.interrupts > 0
    assert defended.penalty_time > 0


def test_tallies_are_consistent_with_the_event_stream() -> None:
    tracer, _ = run_trace(scheme="simultaneous", seed=1234, finish_time=2000)
    caught = [e for e in tracer.events if e.message.startswith("CAUGHT")]
    assert len(caught) == tracer.interrupts
    completed = [e for e in tracer.events if e.message.startswith("COMPLETE")]
    assert len(completed) == tracer.mtd_completed
    footholds = [e for e in tracer.events if e.message.startswith("FOOTHOLD")]
    assert len(footholds) <= 1
