"""Validation-gate tests for the action-layer carve.

The carve separates each of the six attack verbs' executable core (``_do_*``,
which performs the action and RETURNS its branch outcome) from the hard-coded
successor tail-call (now the ``_execute_*`` wrapper, which reads the outcome and
dispatches to the native successor). See
``docs/implementation/pipeline/ogasp/action_layer_anatomy.md`` §3.3 and the
handoff ``docs/handoffs/2026-07-16_l3_action_layer_carve.md``.

Covers the handoff's validation gate:

  G1 — baseline neutrality. The native FSM (entered via ``proceed_attack`` and
       driven by the ``_execute_*`` wrappers) still reproduces the seeded no-MTD
       golden headline (1676 attack events, 34 compromised on seed 1234), and is
       byte-deterministic across repeat runs (SIM-05). The primary G1 evidence
       is the bit-for-bit reproduction of all nine ``baseline/golden`` scenarios;
       this test is the in-repo regression guard against carve-induced drift.
  G2 — each core is invocable in isolation given its documented precondition
       context, and ``assert_action_context`` fails loudly (not silent
       degeneration / bare AttributeError) when that context is absent.
  G3 — a controller can drive a NON-NATIVE verb order end-to-end via ``step``
       (the third lever), one the tail-calls could never produce.

These run as a plain script (``python tests/test_action_layer_carve.py``) and
also as pytest (``pytest tests/test_action_layer_carve.py``).
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
from mtdnetwork.operation.attack_operation import (
    ActionContextError,
    AttackOperation,
    EXPLOIT_COMPROMISED,
    EXPLOIT_HALTED,
    EXPLOIT_UNCOMPROMISED,
)

# Phase-0 default geometry (50/8/4); 10/4/4 trips Finding F-06's gen_graph
# infinite-loop guard. Matches tests/test_crash_fix_regressions.py.
GEOMETRY = dict(
    total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4,
    target_layer=4, total_database=2, terminate_compromise_ratio=0.8,
)


def _fresh_sim(seed=1234):
    """A seeded (env, end_event, network, adversary, attack_operation) tuple."""
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    end_event = env.event()
    tn = TimeNetwork(**GEOMETRY)
    adv = Adversary(network=tn, attack_threshold=ATTACKER_THRESHOLD)
    ao = AttackOperation(env=env, end_event=end_event, adversary=adv,
                         proceed_time=0)
    return env, end_event, tn, adv, ao


def _record_names(adversary):
    """The ordered list of attack-action names in the attack-stats record."""
    return list(adversary.get_attack_stats().get_record()["name"])


# --- G1: baseline neutrality ------------------------------------------------

def test_g1_native_run_reproduces_no_mtd_golden_headline() -> None:
    """The carved native FSM reproduces the no-MTD golden headline exactly.

    1676 attack events and 34 compromised hosts is the committed
    ``baseline/golden/no-mtd`` result (seed 1234, 50-node geometry, 15 ks;
    re-baselined 2026-08-27 under the reinstated OS-gated exploit channel,
    D-19 — see baseline/CHANGELOG.md). If the carve perturbed the native path
    this count would move.
    """
    env, _end, _tn, adv, ao = _fresh_sim(seed=1234)
    ao.proceed_attack()
    env.run(until=15000)

    assert len(adv.get_attack_stats().get_record()) == 1676, (
        "G1 regression: no-MTD native run no longer produces 1676 attack events "
        "(carve is not baseline-neutral)"
    )
    assert len(adv.get_compromised_hosts()) == 34, (
        "G1 regression: no-MTD native run no longer compromises 34 hosts"
    )


def test_g1_native_run_is_deterministic() -> None:
    """SIM-05: same seed -> byte-identical attack record across repeat runs."""
    env_a, _e, _t, adv_a, ao_a = _fresh_sim(seed=1234)
    ao_a.proceed_attack()
    env_a.run(until=15000)

    env_b, _e2, _t2, adv_b, ao_b = _fresh_sim(seed=1234)
    ao_b.proceed_attack()
    env_b.run(until=15000)

    rec_a = adv_a.get_attack_stats().get_record().to_csv(index=False)
    rec_b = adv_b.get_attack_stats().get_record().to_csv(index=False)
    assert rec_a == rec_b, "SIM-05 regression: seeded run is not reproducible"


# --- G2: cores invocable in isolation; fail loudly when context absent ------

def test_g2_scan_host_callable_as_is() -> None:
    """SCAN_HOST is the root: it manufactures its own host_stack, no context."""
    _env, _end, _tn, adv, ao = _fresh_sim()
    assert adv.get_host_stack() == []
    found = ao._do_scan_host()
    assert found is True                      # exposed endpoints discovered
    assert len(adv.get_host_stack()) > 0      # stack now populated


def test_g2_chain_bound_cores_run_with_synthesised_context() -> None:
    """The four chain-bound cores run when handed a synthesised curr_host /
    curr_ports (item 2 of the gate)."""
    _env, _end, tn, adv, ao = _fresh_sim()

    # Synthesise the cursor a controller would set: an exposed endpoint host.
    host_id = tn.exposed_endpoints[0]
    adv.set_curr_host_id(host_id)
    adv.set_curr_host(tn.get_host(host_id))

    # SCAN_PORT: scans, returns a bool, populates curr_ports.
    reuse = ao._do_scan_port()
    assert reuse in (True, False)
    assert isinstance(adv.get_curr_ports(), list)

    # BRUTE_FORCE: attempts credential stuffing, returns a bool.
    brute = ao._do_brute_force()
    assert brute in (True, False)

    # SCAN_NEIGHBOR: discovers neighbours, no branch (returns None), mutates stack.
    assert ao._do_scan_neighbors() is None

    # ENUM_HOST: runs given a non-empty host_stack; sets the cursor.
    adv.set_host_stack([host_id])
    already = ao._do_enum_host()
    assert already in (True, False)
    assert adv.get_curr_host() is not None


def test_g2_exploit_core_runs_in_isolation_via_step() -> None:
    """EXPLOIT_VULN's core is a generator; drive it in isolation with step()
    after synthesising curr_host + a real port scan, and assert it returns a
    documented three-valued outcome (never a bare bool)."""
    env, _end, tn, adv, ao = _fresh_sim()
    host_id = tn.exposed_endpoints[0]
    adv.set_curr_host_id(host_id)
    adv.set_curr_host(tn.get_host(host_id))
    adv.set_curr_ports(tn.get_host(host_id).port_scan())

    captured = {}

    def driver():
        captured["outcome"] = yield from ao.step("EXPLOIT_VULN")

    env.process(driver())
    env.run()
    assert captured["outcome"] in (
        EXPLOIT_COMPROMISED, EXPLOIT_UNCOMPROMISED, EXPLOIT_HALTED,
    )


def test_g2_missing_context_fails_loudly() -> None:
    """assert_action_context raises ActionContextError when the precondition is
    absent — the anti-goal is silent degeneration (EXPLOIT with empty ports ->
    BRUTE_FORCE) or a bare AttributeError deep in the substrate."""
    _env, _end, _tn, adv, ao = _fresh_sim()

    # Fresh adversary: no curr_host, empty stack, empty ports.
    assert adv.get_curr_host() is None

    # SCAN_HOST never fails — it is the root.
    ao.assert_action_context("SCAN_HOST")

    # ENUM_HOST with an empty host_stack.
    for verb in ("ENUM_HOST",):
        try:
            ao.assert_action_context(verb)
        except ActionContextError:
            pass
        else:
            raise AssertionError(f"{verb} should fail loudly with an empty stack")

    # The chain-bound verbs with curr_host = None.
    for verb in ("SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE", "SCAN_NEIGHBOR"):
        try:
            ao.assert_action_context(verb)
        except ActionContextError:
            pass
        else:
            raise AssertionError(f"{verb} should fail loudly with curr_host=None")

    # EXPLOIT_VULN with curr_host set but empty curr_ports (the silent-degenerate
    # case the gate calls out explicitly).
    host_id = _tn_first_endpoint(ao)
    adv.set_curr_host_id(host_id)
    adv.set_curr_host(ao.adversary.get_network().get_host(host_id))
    adv.set_curr_ports([])
    try:
        ao.assert_action_context("EXPLOIT_VULN")
    except ActionContextError:
        pass
    else:
        raise AssertionError(
            "EXPLOIT_VULN should fail loudly with empty curr_ports"
        )


def _tn_first_endpoint(ao):
    return ao.adversary.get_network().exposed_endpoints[0]


# --- G3: a controller drives a NON-NATIVE order end-to-end ------------------

def test_g3_controller_drives_non_native_order() -> None:
    """A controller drives SCAN_HOST -> ENUM_HOST -> SCAN_PORT -> BRUTE_FORCE via
    step(): an order the tail-calls could NEVER produce.

    In the native FSM, SCAN_PORT's only successors are SCAN_NEIGHBOR (on
    credential reuse) or EXPLOIT_VULN (otherwise) — never BRUTE_FORCE directly.
    Driving straight from SCAN_PORT to BRUTE_FORCE, skipping EXPLOIT_VULN,
    demonstrates the third lever: controller-owned succession.
    """
    env, _end, _tn, adv, ao = _fresh_sim(seed=1234)
    order = ["SCAN_HOST", "ENUM_HOST", "SCAN_PORT", "BRUTE_FORCE"]
    trace = []

    def controller():
        for verb in order:
            outcome = yield from ao.step(verb)
            trace.append((verb, outcome))

    env.process(controller())
    env.run()

    # Every requested verb ran, in the requested order.
    assert [v for v, _ in trace] == order
    assert _record_names(adv) == order

    # The tell: BRUTE_FORCE follows SCAN_PORT with NO EXPLOIT_VULN between them —
    # the native machine would have inserted EXPLOIT_VULN there.
    names = _record_names(adv)
    assert "EXPLOIT_VULN" not in names
    assert names.index("BRUTE_FORCE") == names.index("SCAN_PORT") + 1


def test_g3_step_refuses_out_of_context_verb() -> None:
    """step() inherits the precondition guard: driving a chain-bound verb before
    any cursor exists fails loudly rather than crashing inside the substrate."""
    env, _end, _tn, _adv, ao = _fresh_sim()

    def bad_controller():
        yield from ao.step("EXPLOIT_VULN")   # no curr_host / curr_ports yet

    env.process(bad_controller())
    try:
        env.run()
    except ActionContextError:
        pass
    else:
        raise AssertionError("step(EXPLOIT_VULN) should fail loudly with no context")


if __name__ == "__main__":
    test_g1_native_run_reproduces_no_mtd_golden_headline()
    print("G1 (native run reproduces no-MTD golden headline 1676/34): OK")
    test_g1_native_run_is_deterministic()
    print("G1 (SIM-05 seeded determinism): OK")
    test_g2_scan_host_callable_as_is()
    print("G2 (SCAN_HOST callable-as-is): OK")
    test_g2_chain_bound_cores_run_with_synthesised_context()
    print("G2 (chain-bound cores run with synthesised context): OK")
    test_g2_exploit_core_runs_in_isolation_via_step()
    print("G2 (EXPLOIT_VULN core runs in isolation, 3-valued outcome): OK")
    test_g2_missing_context_fails_loudly()
    print("G2 (missing context fails loudly): OK")
    test_g3_controller_drives_non_native_order()
    print("G3 (controller drives non-native SCAN_PORT->BRUTE_FORCE order): OK")
    test_g3_step_refuses_out_of_context_verb()
    print("G3 (step refuses out-of-context verb): OK")
    print("\nall action-layer carve gate checks: OK")
