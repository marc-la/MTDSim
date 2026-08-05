"""D-28 regression: ENUM_HOST must not attack a host it cannot reach.

IS-PRC-01 makes an internal host visible "only if a path exists through a
compromised or exposed internal host". SCAN_HOST enforced that when it built the
queue; nothing re-checked it afterwards, and
``sort_by_distance_from_exposed_and_pivot_host`` only *sorts* — an unreachable
host scored ``LARGE_INT``, sorted last, and was popped and attacked anyway.

The native FSM never exhibited it (0 of 873 pops, boundary review 1), because a
network-layer MTD forces ``_handle_interrupt -> _scan_host()`` and the rebuilt
queue flushes stale entries. The movement driver owns its own succession and does
not re-scan, so the queue survived every topology shuffle: **9.7 % of ENUM_HOST
pops undefended and 22.4 % under MTD** targeted a host with no path from any
exposed endpoint, voiding part of what Complete Topology Shuffle had just done.

The guard lives in the shared core (``visible_host_stack`` +
``_do_enum_host``/``assert_action_context``), so both driving arms inherit it.

These are the assertions whose absence let the defect survive, per the boundary
brief's gate 5:

1. ENUM_HOST never sets ``curr_host`` to a host outside the hacker-visible graph
   — asserted over full runs of **both** arms, defended and undefended.
2. The precondition rejects a queue of only-unreachable hosts, so a driven caller
   gets ``PRECONDITION_UNMET`` rather than a silent attack.
3. The native raise routes an all-unreachable queue to SCAN_HOST (Brown Fig 3
   box 10 -> box 1) rather than dispatching ENUM_HOST.
4. The filter is read-only and order-preserving, and leaves a fully-reachable
   queue untouched (so the guard is inert when it should be).
"""

from __future__ import annotations

import functools
import os
import random
import sys

import numpy as np
import pytest
import simpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.operation.attack_operation import (
    ActionContextError,
    AttackOperation,
)

GEOMETRY = dict(
    total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4,
    target_layer=4, total_database=2, terminate_compromise_ratio=0.8,
)


def _fresh_sim(seed=1234):
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    end_event = env.event()
    tn = TimeNetwork(**GEOMETRY)
    adv = Adversary(network=tn, attack_threshold=ATTACKER_THRESHOLD)
    ao = AttackOperation(env=env, end_event=end_event, adversary=adv, proceed_time=0)
    return env, end_event, tn, adv, ao


def _install_pop_recorder(violations, pops):
    """Record every ENUM_HOST pop whose host lies outside the visible graph.

    Read-only: delegates unchanged and draws no randomness, so an instrumented
    run is the run it instruments.
    """
    original = AttackOperation._do_enum_host

    @functools.wraps(original)
    def recording_do_enum_host(self):
        result = original(self)
        adversary = self.adversary
        network = adversary.get_network()
        popped = adversary.get_curr_host_id()
        pops.append(popped)
        if popped not in set(network.get_hacker_visible_graph().nodes()):
            violations.append(popped)
        return result

    AttackOperation._do_enum_host = recording_do_enum_host
    return lambda: setattr(AttackOperation, "_do_enum_host", original)


# --- 1. the invariant, over whole runs of both arms ------------------------


@pytest.mark.parametrize("scheme", [None, "simultaneous"])
def test_native_arm_never_enumerates_an_unreachable_host(scheme):
    violations, pops = [], []
    undo = _install_pop_recorder(violations, pops)
    try:
        from mtdnetwork.trace import run_trace

        for seed in range(3):
            run_trace(scheme=scheme or "none", seed=3000 + seed,
                      mtd_interval=200 if scheme else None, finish_time=5000.0)
    finally:
        undo()

    assert pops, "no ENUM_HOST activity — the test would pass vacuously"
    assert violations == [], (
        f"{len(violations)} of {len(pops)} native ENUM_HOST pops targeted a host "
        f"outside the hacker-visible graph (IS-PRC-01, D-28): {violations[:10]}"
    )


@pytest.mark.parametrize("scheme", [None, "simultaneous"])
def test_movement_arm_never_enumerates_an_unreachable_host(scheme):
    """The arm the defect actually appeared in (9.7 % / 22.4 % before the guard)."""
    violations, pops = [], []
    undo = _install_pop_recorder(violations, pops)
    try:
        from mtdsim.l3_simulation.movement.run import run_movement

        for seed in range(3):
            run_movement("aggregate", seed=seed, mtd_scheme=scheme,
                         mtd_interval=200 if scheme else None,
                         mapping_version="v2_partial", retrace_sinks=True)
    finally:
        undo()

    assert pops, "no ENUM_HOST activity — the test would pass vacuously"
    assert violations == [], (
        f"{len(violations)} of {len(pops)} movement ENUM_HOST pops targeted a host "
        f"outside the hacker-visible graph (IS-PRC-01, D-28): {violations[:10]}"
    )


# --- 2/3. the precondition and the native re-route ------------------------


def test_precondition_rejects_an_all_unreachable_queue():
    """A driven caller must get PRECONDITION_UNMET, not a silent attack."""
    _env, _end, tn, adv, ao = _fresh_sim()

    # A deep host with no compromised foothold: nothing is reachable, so the
    # hacker-visible graph is the exposed endpoints alone.
    deep = max(
        (h for h in tn.nodes if h not in tn.exposed_endpoints),
        key=lambda h: tn.get_path_from_exposed(h, graph=tn.graph)[1],
    )
    adv.set_host_stack([deep])

    assert deep not in set(tn.get_hacker_visible_graph().nodes()), (
        "test setup: expected the deep host to be invisible with no foothold"
    )
    assert ao.visible_host_stack() == []

    with pytest.raises(ActionContextError, match="visible"):
        ao.assert_action_context("ENUM_HOST")


def test_native_raise_routes_an_all_unreachable_queue_to_scan_host():
    """Brown Fig 3 box 10 -> box 1: no host to target means re-run discovery."""
    _env, _end, tn, adv, ao = _fresh_sim()
    deep = max(
        (h for h in tn.nodes if h not in tn.exposed_endpoints),
        key=lambda h: tn.get_path_from_exposed(h, graph=tn.graph)[1],
    )
    adv.set_host_stack([deep])

    ao._enum_host()

    assert adv.get_curr_process() == "SCAN_HOST", (
        "an all-unreachable queue must re-run host discovery, not dispatch "
        f"ENUM_HOST (got {adv.get_curr_process()!r})"
    )


# --- 4. the filter itself -------------------------------------------------


def test_filter_is_inert_on_a_fully_reachable_queue():
    """The guard must not perturb a queue SCAN_HOST would have accepted."""
    _env, _end, tn, adv, ao = _fresh_sim()
    adv.set_host_stack(list(tn.exposed_endpoints))

    assert ao.visible_host_stack() == list(tn.exposed_endpoints), (
        "exposed endpoints are always reachable and must survive unreordered"
    )


def test_filter_is_read_only():
    """`visible_host_stack` reports; only `_do_enum_host` acts on it."""
    _env, _end, tn, adv, ao = _fresh_sim()
    deep = max(
        (h for h in tn.nodes if h not in tn.exposed_endpoints),
        key=lambda h: tn.get_path_from_exposed(h, graph=tn.graph)[1],
    )
    stack = list(tn.exposed_endpoints) + [deep]
    adv.set_host_stack(list(stack))

    filtered = ao.visible_host_stack()

    assert adv.get_host_stack() == stack, "the filter must not mutate the queue"
    assert deep not in filtered
    assert filtered == list(tn.exposed_endpoints)


def test_empty_queue_filters_to_empty_without_touching_the_network():
    _env, _end, _tn, adv, ao = _fresh_sim()
    adv.set_host_stack([])
    assert ao.visible_host_stack() == []
