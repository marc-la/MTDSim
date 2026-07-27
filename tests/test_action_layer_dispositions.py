"""Characterisation tests pinning the action layer's audited dispositions.

These are **not** tests of intended behaviour. They pin behaviour that the
2026-07-27 action-layer audit dispositioned as *inherited divergence* or as a
*stated comparability limitation* — behaviour deliberately left in place under the
S2 change freeze. Their job is to make each fact **loud if it ever changes**, so a
future session changes it on purpose rather than by accident, and so the
dispositions in ``docs/implementation/pipeline/ogasp/action_layer_anatomy.md`` §4.2
cannot silently drift away from the code.

Each test therefore asserts *the current, divergent reality* and names, in its
docstring, the disposition it guards and who owns any change.

Audited items pinned here:

- **ATK-07, the give-up rule.** Brown 2023 (§III-C(2), Table I) specifies giving up
  on a host after 10 failed attempts. The code applies it only when
  ``network.network_type == 0``; every experiment to date runs ``TimeNetwork``,
  which is ``network_type == 1``. The rule is therefore inactive in every run, and
  it is not merely latent — hosts do exceed the threshold.
- **ATK-08, the global attack-attempt cap.** ``max_attack_attempts`` is computed and
  ``curr_attempts`` is incremented, but the enforcing guard is commented out. Left
  inert deliberately: it has a paper-free heuristic origin and restoring it would
  fire mid-run and break the 692/41 golden (a re-baseline is Marc's call).
- **ATK-05, the MTD confusion penalty.** The native arm pays it; the movement
  (driven) arm does not, because ``step()`` lets the interrupt propagate to the
  driver instead of running ``_handle_interrupt``. Stated as a comparability
  limitation; the fix is owned by the S3 stochastic-timing pair, which makes the
  penalty a movement-layer object.
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


def test_give_up_rule_never_fires_and_hosts_exceed_brown_s_bound() -> None:
    """``stop_attack`` stays empty across schemes, and the per-host attempt counter
    does exceed ``ATTACKER_THRESHOLD`` — so the rule's inactivity is consequential,
    not merely latent.

    Disposition: inherited divergence (ATK-07). Recorded, not fixed — activating it
    changes every golden and is Marc's re-baseline call.
    """
    exceeded_somewhere = False
    for seed, scheme in ((1234, None), (42, None), (1234, "simultaneous")):
        _tn, adv, _ao = _native_run(seed, scheme=scheme)
        assert adv.get_stop_attack() == [], (
            f"seed={seed} scheme={scheme}: a host was given up, but the give-up "
            f"rule is dispositioned inactive on the general network (ATK-07)"
        )
        if max(adv.get_attack_counter()) >= ATTACKER_THRESHOLD:
            exceeded_somewhere = True

    assert exceeded_somewhere, (
        "no host reached the give-up threshold in any sampled cell — if this "
        "becomes true the ATK-07 divergence is latent rather than consequential, "
        "and the anatomy register's wording should be softened accordingly"
    )


# --- ATK-08: the global attack-attempt cap is inert --------------------------

def test_global_attack_attempt_cap_is_inert() -> None:
    """``curr_attempts`` overruns ``max_attack_attempts`` and nothing happens.

    Disposition: inherited divergence, deliberately left inert. The cap has a
    paper-free heuristic origin (ATK-08) and, as this test shows, is exceeded by
    roughly 2x mid-run — restoring the guard would truncate the run and break the
    692/41 golden, which is a re-baseline and therefore Marc's call.
    """
    _tn, adv, _ao = _native_run(1234)

    assert adv.get_max_attack_attempts() == 250  # 5 x 50 nodes
    assert adv.get_curr_attempts() > adv.get_max_attack_attempts(), (
        "the global attack-attempt cap appears to be enforced again; it is "
        "dispositioned inert (ATK-08) and restoring it re-baselines the goldens"
    )
    # The run was NOT truncated by the cap: the golden headline still holds.
    assert len(adv.get_attack_stats().get_record()) == 692
    assert len(adv.get_compromised_hosts()) == 41


# --- ATK-05: the confusion penalty is paid by one arm only -------------------

class _PenaltyProbe:
    """Count ``_handle_interrupt`` entries and the simulated time they consume."""

    def __init__(self):
        self.entries = 0
        self.time_consumed = 0.0
        self._orig = AttackOperation._handle_interrupt

    def __enter__(self):
        probe = self

        def wrapped(self_ao, start_time, name):
            probe.entries += 1
            t0 = self_ao.env.now
            yield from probe._orig(self_ao, start_time, name)
            probe.time_consumed += self_ao.env.now - t0

        AttackOperation._handle_interrupt = wrapped
        return self

    def __exit__(self, *exc):
        AttackOperation._handle_interrupt = self._orig
        return False


def test_native_arm_pays_the_mtd_confusion_penalty() -> None:
    """The native FSM routes every interrupt through ``_handle_interrupt``, which
    consumes an ``exponential_variates(PENALTY=20, 0.5)`` draw of simulated time.

    This is the faithful half of ATK-05 and the reference the movement arm is
    compared against.
    """
    assert ATTACK_DURATION["PENALTY"] == 20
    with _PenaltyProbe() as probe:
        _tn, _adv, _ao = _native_run(1234, scheme="simultaneous", horizon=3000)

    assert probe.entries > 0, "no MTD interrupt reached the native attacker"
    assert probe.time_consumed > 0, (
        "the native arm consumed no confusion-penalty time; ATK-05 is recorded as "
        "faithful on this path"
    )


def test_movement_arm_pays_no_confusion_penalty_stated_limitation() -> None:
    """**The comparability limitation, pinned.** The driven arm observes MTD
    interrupts but consumes *zero* penalty time: ``step()`` has no interrupt
    handler, so the interrupt propagates to ``MovementAttacker._dispatch``, which
    records a failure verdict and routes. ``_handle_interrupt`` — which carries the
    penalty — never runs.

    The re-raise itself is deliberate and correct: ``_handle_interrupt`` also
    *hard-codes the next phase* (SCAN_HOST / SCAN_PORT), and running it behind the
    driver would re-impose the native succession the carve exists to remove. What
    was not deliberate is that the penalty went out with it.

    Disposition: **stated comparability limitation, not fixed here.** Restoring a
    penalty changes timing semantics, which this audit is explicitly barred from
    deciding; S3 (the stochastic-timing pair) makes the penalty a movement-layer
    object and owns the fix. Until then the two arms do not pay the same price for
    the same defensive event, and any cross-arm MTTC comparison must say so.

    When S3 lands, this test should FAIL and be replaced by one asserting the
    movement arm's own penalty semantics.
    """
    pytest.importorskip("mtdsim.l3_simulation.movement.run")
    from mtdsim.l3_simulation.movement.run import run_movement

    with _PenaltyProbe() as probe:
        res = run_movement(
            "pure_impediment", seed=42, with_synthetic_overlay=True,
            horizon=3000, mtd_scheme="simultaneous", mtd_interval=200,
        )

    interrupted = [r for r in res.records if r.interrupted]
    assert interrupted, "no MTD interrupt was observed on the movement arm"
    assert probe.entries == 0, (
        "the driven arm entered _handle_interrupt; the carve's contract is that an "
        "interrupt propagates to the driver instead, so no native succession runs "
        "behind it"
    )
    assert probe.time_consumed == 0.0, (
        "the movement arm now pays confusion-penalty time. If this is intended, S3 "
        "has landed — replace this characterisation test with one asserting the "
        "movement layer's own penalty semantics, and update ATK-05 in "
        "docs/implementation/mtdsim_spec.md and the anatomy register's §4.2."
    )
