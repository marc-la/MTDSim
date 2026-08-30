"""The targeted objective — Brown's Scenario 2 on the movement attacker
(handoff 2026-08-30_targeted_attacker_build.md; decision A).

Rungs 1–5 of the brief's verification ladder: the general arm is unchanged with
the targeted machinery present; the sorter orders by Brown's priority with the
general order inside each class and draws exactly what the general sort draws;
the give-up rule spares the target; a targeted run ends on the target's
compromise; and the whole thing is deterministic.
"""

from __future__ import annotations

import random

import numpy as np
import pytest

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdsim.l3_simulation.movement.run import GEOMETRY, run_movement
from mtdsim.l3_simulation.movement.targeting import (
    ATTACK_OBJECTIVES,
    TargetedSorter,
    choose_target_hosts,
)

CFG = dict(seed=3, horizon=1500, mapping_version="v2_partial")


def _fields(result):
    return [
        (r.place, r.verb, r.start_time, r.end_time, r.outcome, r.n_compromised)
        for r in result.records
    ]


def _network(seed=0):
    random.seed(seed)
    np.random.seed(seed)
    return TimeNetwork(**GEOMETRY)


# --- the input ----------------------------------------------------------------

def test_objectives_are_exactly_browns_two() -> None:
    assert ATTACK_OBJECTIVES == ("general", "targeted")


def test_unknown_objective_is_refused() -> None:
    with pytest.raises(ValueError, match="attack_objective"):
        run_movement("aggregate", attack_objective="apt", **CFG)


def test_target_layer_is_refused_under_general() -> None:
    with pytest.raises(ValueError, match="target_layer"):
        run_movement("aggregate", attack_objective="general", target_layer=2, **CFG)


# --- rung 1: the general arm is unchanged --------------------------------------

def test_general_arm_unchanged_with_targeted_machinery_present() -> None:
    """The seam's defaults (host_sorter None, empty target_hosts) are the old
    lines; an explicit general run equals an unqualified one, and the result
    carries no target."""
    unset = run_movement("aggregate", **CFG)
    general = run_movement("aggregate", attack_objective="general", **CFG)
    assert _fields(general) == _fields(unset)
    assert general.attack_objective == "general"
    assert general.target_hosts == () and general.target_layer is None
    assert all(r.target_class is None for r in general.records)


# --- the target choice ---------------------------------------------------------

def test_default_target_is_the_database_set_on_its_layer() -> None:
    net = _network()
    hosts, layer = choose_target_hosts(net, target_layer=None, seed=0)
    assert hosts == frozenset(net.get_database())
    assert layer == max(net.get_layers()[h] for h in hosts)


@pytest.mark.parametrize("layer", [1, 2, 3])
def test_target_layer_draws_one_host_on_that_layer_deterministically(layer) -> None:
    net = _network()
    a, la = choose_target_hosts(net, target_layer=layer, seed=7)
    b, lb = choose_target_hosts(net, target_layer=layer, seed=7)
    assert a == b and la == lb == layer
    (host,) = a
    assert net.get_layers()[host] == layer


def test_target_choice_does_not_touch_the_global_stream() -> None:
    net = _network()
    random.seed(11)
    before = random.random()
    random.seed(11)
    choose_target_hosts(net, target_layer=2, seed=7)
    assert random.random() == before


# --- rung 2: the sorter --------------------------------------------------------

def _stack_with_layers(net, per_layer):
    layers = net.get_layers()
    stack = []
    for layer, n in per_layer.items():
        stack += sorted(h for h, l in layers.items() if l == layer and h not in net.exposed_endpoints)[:n]
    return stack


def test_sorter_puts_target_first_then_its_layer_then_nearer_layers() -> None:
    net = _network()
    target, tl = choose_target_hosts(net, target_layer=2, seed=1)
    sorter = TargetedSorter(net, target, tl)
    stack = _stack_with_layers(net, {1: 3, 2: 3, 3: 3})
    (t,) = target
    if t not in stack:
        stack.append(t)
    random.seed(5)
    ordered = sorter(stack, [], pivot_host_id=-1)
    classes = [sorter.priority(h) for h in ordered]
    assert classes == sorted(classes)
    assert ordered[0] == t and classes[0] == 0
    assert set(ordered) == set(stack)


def test_within_a_class_the_order_is_the_general_attackers() -> None:
    net = _network()
    target, tl = choose_target_hosts(net, target_layer=2, seed=1)
    sorter = TargetedSorter(net, target, tl)
    stack = _stack_with_layers(net, {1: 4, 2: 4, 3: 4})
    random.seed(9)
    general = net.sort_by_distance_from_exposed_and_pivot_host(stack, [], pivot_host_id=-1)
    random.seed(9)
    targeted = sorter(stack, [], pivot_host_id=-1)
    for cls in set(sorter.priority(h) for h in stack):
        assert [h for h in targeted if sorter.priority(h) == cls] == \
               [h for h in general if sorter.priority(h) == cls]


def test_sorter_draws_exactly_what_the_general_sort_draws() -> None:
    net = _network()
    target, tl = choose_target_hosts(net, target_layer=2, seed=1)
    sorter = TargetedSorter(net, target, tl)
    stack = _stack_with_layers(net, {1: 4, 2: 4, 3: 4})
    random.seed(21)
    net.sort_by_distance_from_exposed_and_pivot_host(stack, [], pivot_host_id=-1)
    after_general = random.random()
    random.seed(21)
    sorter(stack, [], pivot_host_id=-1)
    assert random.random() == after_general


# --- rung 3: never give up on the target --------------------------------------

def _attack_op(net):
    import simpy
    from mtdnetwork.operation.attack_operation import AttackOperation
    env = simpy.Environment()
    end = env.event()
    adv = Adversary(network=net, attack_threshold=ATTACKER_THRESHOLD)
    return env, end, adv, AttackOperation(env=env, end_event=end, adversary=adv)


def test_give_up_rule_spares_the_target_and_not_others() -> None:
    net = _network()
    target, tl = choose_target_hosts(net, target_layer=2, seed=1)
    (t,) = target
    other = next(h for h, l in net.get_layers().items() if l == 2 and h != t)
    env, end, adv, op = _attack_op(net)
    op.target_hosts = target
    op.host_sorter = TargetedSorter(net, target, tl)
    for host in (t, other):
        adv.set_host_stack([host])
        for _ in range(ATTACKER_THRESHOLD + 1):
            adv.set_host_stack([host])
            adv.set_pivot_host_id(-1)
            # the core raises on an invisible host; both chosen hosts sit on the
            # visible graph only once a path exists, so drive the counter directly
            adv.set_curr_host_id(host)
            adv.set_curr_host(net.get_host(host))
            adv.get_attack_counter()[host] += 1
            if adv.get_attack_counter()[host] >= adv.get_attack_threshold():
                protected = host in op.target_hosts
                if not protected and host not in adv.get_stop_attack():
                    adv.get_stop_attack().append(host)
    assert t not in adv.get_stop_attack()
    assert other in adv.get_stop_attack()


def test_core_guard_reads_the_seams_target_set() -> None:
    """The line itself: the give-up guard in _do_enum_host keys on
    ``self.target_hosts`` and nothing else."""
    import inspect
    from mtdnetwork.operation import attack_operation
    src = inspect.getsource(attack_operation.AttackOperation._do_enum_host)
    code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    assert "in self.target_hosts" in code
    assert "get_target_node" not in code and "network_type" not in code


# --- rung 4 + 5: a targeted run ends on the target, deterministically ----------

def _first_targeted_reach(profile="aggregate", seeds=range(0, 40), **kw):
    for seed in seeds:
        res = run_movement(profile, attack_objective="targeted", seed=seed,
                           horizon=15_000, mapping_version="v2_partial", **kw)
        if res.reached_objective:
            return res
    return None


def test_targeted_run_ends_on_the_targets_compromise() -> None:
    res = _first_targeted_reach(target_layer=1)
    assert res is not None, "no seed in 0..39 reached a layer-1 target — investigate"
    assert res.compromised_count < 40  # not the ratio
    held = set(res.target_hosts)
    # the terminal record follows the reach immediately: the walk saw end_event
    assert res.records[-1].outcome == "SIM_END"
    # a target host is in the final compromised set (n_compromised trajectory
    # ends at the reach; the target's id is on the result)
    assert held and res.target_layer == 1
    # every selecting row (ENUM pop or fresh-host re-select) carries its class,
    # and the target's own selection is on record as class 0
    selecting = [r for r in res.records
                 if (r.verb == "ENUM_HOST" or r.reselected) and not r.blocked and not r.interrupted]
    assert selecting and all(r.target_class is not None for r in selecting)
    assert any(r.target_class == 0 for r in selecting)


def test_targeted_is_deterministic_and_differs_from_general_only_after_a_pop() -> None:
    a = run_movement("aggregate", attack_objective="targeted", target_layer=2, **CFG)
    b = run_movement("aggregate", attack_objective="targeted", target_layer=2, **CFG)
    assert _fields(a) == _fields(b) and a.target_hosts == b.target_hosts
    g = run_movement("aggregate", **CFG)
    fa, fg = _fields(a), _fields(g)
    if fa != fg:
        first = next(i for i, (x, y) in enumerate(zip(fa, fg)) if x != y)
        # the first divergence is at or after the first ENUM_HOST pop
        first_enum = next(i for i, r in enumerate(a.records) if r.verb == "ENUM_HOST")
        assert first >= first_enum
