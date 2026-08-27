"""Tests for the action-layer behaviours the 2026-07-27 audit examined.

Originally these were *characterisation* tests: they pinned divergences the audit
had found but was not licensed to fix, so the facts could not drift silently. The
supervisor then authorised fixing verified defects in the simulator, and two of the
three were repaired — so those two are now **regression** tests of Brown-faithful
behaviour, and say so in their docstrings. One disposition survives unchanged.

What each guards:

- **ATK-07, the give-up rule — FIXED.** Brown B-ATK-06 (§III-C(2), Table I; §V-C)
  specifies giving up on a host after 10 failed attempts in Scenario 1, and never
  giving up on the target node in Scenario 2. The guard was inverted, applying the
  rule only in the *targeted* network — unreachable here — so no host was ever given
  up and hosts were re-enumerated up to 50 times against a bound of 10. Now
  bounded, and the give-up list survives lateral expansion.
- **ATK-05, the MTD confusion penalty — FIXED.** Brown B-ATK-07 (§V-A) makes the
  penalty unconditional. The driven arm paid none, because ``step()`` has no
  interrupt handler and ``_handle_interrupt`` never ran. Both arms now consume the
  same ``apply_mtd_interrupt_cost``, so neither gets MTD cheaper than the other.
- **ATK-08, the global attack-attempt cap — still inert, deliberately.** The cap is
  computed and counted but its single guard stays commented out. It has a
  paper-free heuristic origin, so there is no source to be unfaithful to, and it is
  overrun roughly two-fold mid-run — enforcing it would truncate every run. This
  one remains a characterisation test of an accepted divergence.
"""

from __future__ import annotations

import os
import random
import sys

import numpy as np
import pytest
import simpy

# Allow running directly from the repo root without `pip install -e .`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACK_DURATION, ATTACKER_THRESHOLD
from mtdnetwork.operation.attack_operation import AttackOperation

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


def _native_run(seed, scheme=None, horizon=15000, interval=200):
    """One native (6-phase FSM) run, optionally under MTD."""
    env, end_event, tn, adv, ao = _fresh_sim(seed)
    if scheme is not None:
        from mtdnetwork.operation.mtd_operation import MTDOperation
        from mtdnetwork.statistic.security_metric_statistics import (
            SecurityMetricStatistics,
        )

        MTDOperation(
            security_metrics_record=SecurityMetricStatistics(), env=env,
            end_event=end_event, network=tn, attack_operation=ao, scheme=scheme,
            adversary=adv, proceed_time=0, mtd_trigger_interval=interval,
        ).proceed_mtd()
    ao.proceed_attack()
    env.run(until=horizon)
    return tn, adv, ao


# --- ATK-07: the give-up rule is inactive in the general network ------------

def test_experiments_run_the_general_network_not_the_targeted_one() -> None:
    """The give-up guard requires ``network_type == 0``. Both arms build a
    ``TimeNetwork`` (``baseline/run_baseline.py`` and
    ``src/mtdsim/l3_simulation/movement/run.py``), which is ``network_type == 1``.

    Disposition: inherited divergence from Brown Table I. Changing it means
    running the targeted scenario, which is a scenario choice, not a bug fix.
    """
    random.seed(1234)
    np.random.seed(1234)
    tn = TimeNetwork(**GEOMETRY)
    assert tn.network_type == 1, (
        "the experiments are expected to run the GENERAL network (type 1); if this "
        "is now 0 the give-up rule has become active and ATK-07's disposition, the "
        "goldens, and the anatomy register all need re-deriving"
    )
    # The target-node exemption is vacuous here: there is no target node at all.
    assert tn.get_target_node() is None


def test_give_up_rule_is_active_and_bounds_attempts_per_host() -> None:
    """Brown B-ATK-06: give up on a host after ``ATTACKER_THRESHOLD`` (10) failed
    attempts in Scenario 1, and never give up on the target node in Scenario 2.

    **Was a characterisation test of the divergence; now a regression test of the
    fix.** The guard previously read ``curr_host_id != target_node and
    network_type == 0``, which applied the rule only in the *targeted* network — the
    inverse of Brown, who specifies it for the general one. Since every network this
    repository constructs is ``network_type == 1``, no host was ever given up and
    hosts were re-enumerated up to 50 times against a stated bound of 10.

    The counter is now genuinely bounded, which is the observable consequence.
    """
    for seed, scheme in ((1234, None), (42, None), (1234, "simultaneous")):
        _tn, adv, _ao = _native_run(seed, scheme=scheme)
        assert max(adv.get_attack_counter()) <= ATTACKER_THRESHOLD, (
            f"seed={seed} scheme={scheme}: a host was enumerated "
            f"{max(adv.get_attack_counter())} times against Brown's bound of "
            f"{ATTACKER_THRESHOLD} — the give-up rule is not bounding attempts"
        )
        # Any host that reached the bound must actually be on the give-up list
        # (no target-node exemption applies: the general network has no target).
        at_bound = [i for i, c in enumerate(adv.get_attack_counter())
                    if c >= ATTACKER_THRESHOLD]
        for host_id in at_bound:
            assert host_id in adv.get_stop_attack(), (
                f"host {host_id} hit the give-up bound but was not given up"
            )


def test_a_given_up_host_is_not_re_queued_by_scan_neighbor() -> None:
    """The give-up list must survive lateral expansion.

    ``stop_attack`` is consulted when ``SCAN_HOST`` builds the queue, but
    ``SCAN_NEIGHBOR`` used to prepend raw discovery output straight back onto the
    stack — so a blacklisted host re-entered the queue and was attacked again,
    defeating the rule from a sibling verb.
    """
    _tn, adv, _ao = _native_run(1234, scheme="simultaneous")
    given_up = set(adv.get_stop_attack())
    if not given_up:
        pytest.skip("no host was given up in this cell")
    assert not (given_up & set(adv.get_host_stack())), (
        "a host on the give-up list is back in the work queue"
    )


# --- ATK-08: the global attack-attempt cap is inert --------------------------

def test_global_attack_attempt_cap_is_inert() -> None:
    """``curr_attempts`` overruns ``max_attack_attempts`` and nothing happens.

    Disposition: inherited divergence, deliberately left inert. The cap has a
    paper-free heuristic origin (ATK-08) and, as this test shows, is exceeded by
    roughly 2x mid-run — restoring the guard would truncate the run and break the
    goldens, which is a re-baseline in its own right.
    """
    _tn, adv, _ao = _native_run(1234)

    assert adv.get_max_attack_attempts() == 250  # 5 x 50 nodes
    assert adv.get_curr_attempts() > adv.get_max_attack_attempts(), (
        "the global attack-attempt cap appears to be enforced again; it is "
        "dispositioned inert (ATK-08) and restoring it re-baselines the goldens"
    )
    # The run was NOT truncated by the cap — it ran on past it to the committed
    # no-MTD golden headline (34 hosts since the 2026-08-27 re-baseline under the
    # reinstated OS-gated exploit channel, D-19; 41 before it).
    assert len(adv.get_compromised_hosts()) == 34


# --- ATK-05: the confusion penalty is paid by one arm only -------------------

class _InterruptCostProbe:
    """Count entries to the shared MTD-interrupt cost and the sim time it consumes.

    Both arms route through ``apply_mtd_interrupt_cost``, so measuring it compares
    like with like: the native FSM reaches it from ``_handle_interrupt``, the
    movement driver from ``_read_interrupt``.
    """

    def __init__(self):
        self.entries = 0
        self.time_consumed = 0.0
        self._orig = AttackOperation.apply_mtd_interrupt_cost

    def __enter__(self):
        probe = self

        def wrapped(self_ao, interrupted_mtd):
            probe.entries += 1
            t0 = self_ao.env.now
            yield from probe._orig(self_ao, interrupted_mtd)
            probe.time_consumed += self_ao.env.now - t0

        AttackOperation.apply_mtd_interrupt_cost = wrapped
        return self

    def __exit__(self, *exc):
        AttackOperation.apply_mtd_interrupt_cost = self._orig
        return False


def test_native_arm_pays_the_mtd_confusion_penalty() -> None:
    """The native FSM routes every interrupt through ``_handle_interrupt``, which
    consumes an ``exponential_variates(PENALTY=20, 0.5)`` draw of simulated time.

    This is the faithful half of ATK-05 and the reference the movement arm is
    compared against.
    """
    assert ATTACK_DURATION["PENALTY"] == 20
    with _InterruptCostProbe() as probe:
        _tn, _adv, _ao = _native_run(1234, scheme="simultaneous", horizon=3000)

    assert probe.entries > 0, "no MTD interrupt reached the native attacker"
    assert probe.time_consumed > 0, (
        "the native arm consumed no confusion-penalty time; ATK-05 is recorded as "
        "faithful on this path"
    )


def test_movement_arm_pays_the_same_confusion_penalty_as_the_native_arm() -> None:
    """Brown B-ATK-07 (§V-A): a time penalty applies **whenever** an attacker is
    blocked by an MTD. It is not conditional on which attacker is driving.

    **Was a characterisation test of the divergence; now a regression test of the
    fix.** The driven arm used to consume *zero* penalty time — ``step()`` has no
    interrupt handler, so the interrupt propagated to the driver, and
    ``_handle_interrupt``, which carried the penalty, never ran. MTD was therefore
    materially cheaper for the movement attacker than for the baseline it is
    compared against, and the arm also kept exploiting a host it had just lost.

    The driver now consumes the substrate's own ``apply_mtd_interrupt_cost``, so
    both arms pay the same price and lose the same position for the same event. The
    driver still owns *succession* — that asymmetry is the carve, and is intended.
    """
    pytest.importorskip("mtdsim.l3_simulation.movement.run")
    from mtdsim.l3_simulation.movement.run import run_movement

    probe = _InterruptCostProbe()
    with probe:
        # seed 1 (was 42 before 2026-08-17): after Marc's membership rulings the
        # objective_impact net carries a sink at `collection`, which seed 42
        # reaches at t≈13 before any MTD fires; seed 1 walks the horizon with
        # 24 interrupts.
        res = run_movement(
            "objective_impact", seed=1, with_synthetic_overlay=True,
            horizon=3000, mtd_scheme="simultaneous", mtd_interval=200,
        )

    interrupted = [r for r in res.records if r.interrupted]
    assert interrupted, "no MTD interrupt was observed on the movement arm"
    assert probe.entries >= len(interrupted), (
        "the movement arm observed interrupts without paying the confusion penalty "
        "for each; Brown B-ATK-07 makes the penalty unconditional"
    )
    assert probe.time_consumed > 0, (
        "the movement arm consumed no confusion-penalty time"
    )
    # And the price per interrupt is the same draw both arms use (mean PENALTY=20).
    mean_penalty = probe.time_consumed / probe.entries
    assert 5 < mean_penalty < 80, (
        f"mean penalty per interrupt was {mean_penalty:.1f}, which is not an "
        f"exponential draw about PENALTY={ATTACK_DURATION['PENALTY']}"
    )


def test_the_confusion_penalty_is_charged_once_per_interrupt() -> None:
    """The single-charge property, pinned tightly — the failure mode is paying
    *twice* for one defensive event, once through the substrate's own interrupt
    handling and once through the driver.

    S3 ruled that the penalty stays substrate-side rather than becoming a place in
    the movement net, precisely so that this property is one to **protect** rather
    than to re-establish; this test is that protection. It tightens the
    ``entries >= interrupts`` inequality above to an exact accounting: every
    interrupt the driver records is charged exactly once, and the only permitted
    excess is a single charge in flight when the simulation horizon cuts the run —
    that event begins its penalty but never reaches the record.

    The tolerance is exactly one because the movement driver is a single SimPy
    process: at most one event can be mid-penalty when the clock stops.
    """
    pytest.importorskip("mtdsim.l3_simulation.movement.run")
    from mtdsim.l3_simulation.movement.run import run_movement

    horizon = 15_000
    for seed in (0, 7, 42, 1234):
        probe = _InterruptCostProbe()
        with probe:
            res = run_movement(
                "aggregate", seed=seed, with_synthetic_overlay=True,
                horizon=horizon, mtd_scheme="simultaneous", mtd_interval=200,
            )
        recorded = sum(1 for r in res.records if r.interrupted)
        assert recorded > 0, f"seed {seed}: no MTD interrupt was observed"

        excess = probe.entries - recorded
        assert 0 <= excess <= 1, (
            f"seed {seed}: {probe.entries} penalty charges against {recorded} "
            f"recorded interrupts — the penalty is being paid more than once per "
            f"defensive event"
        )
        if excess == 1:
            # The in-flight charge must genuinely be the horizon cutting the run,
            # not an unrecorded double charge mid-walk: the last record has to sit
            # within one penalty draw of the horizon.
            assert res.records[-1].end_time > horizon - 200, (
                f"seed {seed}: an extra penalty charge that the horizon does not "
                f"explain (last record ended at {res.records[-1].end_time})"
            )
