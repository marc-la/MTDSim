"""Smoke matrix, boundary audit, and golden-neutrality for the movement layer.

Covers the M7 handoff's remaining gates:

  G1  goldens pass: the native 6-phase attacker still reproduces the no-MTD golden
      headline (692 events / 41 compromised, seed 1234, 15 ks) — the movement-layer
      additions changed no shared code path.
  G5  the smoke matrix: all five profiles (4 classes + aggregate) run to horizon on
      the smoke cell, emitting non-degenerate records the statistics reader turns
      into MTTC / ASR.
  G6  boundary audit: no behavioural change under mtdnetwork/component or
      mtdnetwork/mtdai — the movement layer lives entirely in the src/mtdsim tree.

The overlay ``compose`` and verdict adapter are injected as controlled fakes (the
real ones are the controller-finalisation handoff's surface).
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
import random
import simpy
import pytest

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.operation.attack_operation import EXPLOIT_COMPROMISED, AttackOperation

from mtdsim.l3_simulation.movement.net import PROFILES
from mtdsim.l3_simulation.movement.run import run_smoke_matrix
from mtdsim.l3_simulation.movement.statistics import summarise

REPO_ROOT = Path(__file__).resolve().parents[2]

GEOMETRY = dict(
    total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4,
    target_layer=4, total_database=2, terminate_compromise_ratio=0.8,
)


def _verdict(verb, outcome, interrupted):
    if interrupted:
        return "failure"
    return "success" if outcome in (True, EXPLOIT_COMPROMISED) else "failure"


class _RefOverlay:
    """Reference multiply-renormalise composer (documented M2 rule)."""

    def compose(self, src, verdict, base):
        if verdict == "success":
            factor = {d: 1.0 for d in base}
        else:
            factor = {d: (1.0 if d == min(base) else 0.3) for d in base}
        num = {d: base[d] * factor[d] for d in base}
        z = sum(num.values())
        return {d: v / z for d, v in num.items()} if z > 0 else {}


# --- G5: the smoke matrix ---------------------------------------------------
def test_g5_smoke_matrix_all_profiles_emit_readable_records() -> None:
    seeds = (1234, 7)
    results = run_smoke_matrix(
        PROFILES, seeds, with_synthetic_overlay=True, horizon=2500,
        overlay=_RefOverlay(), verdict_of=_verdict, register_for_interrupts=False,
    )
    assert len(results) == len(PROFILES) * len(seeds)
    for r in results:
        assert r.records, f"{r.profile}/{r.seed} produced no records"

    summaries = summarise(results)
    assert set(summaries) == set(PROFILES)
    for profile, summary in summaries.items():
        assert summary.n_runs == len(seeds)
        assert 0.0 <= summary.asr <= 1.0
        assert summary.mean_events > 0
        # MTTC is None only if no run of the profile compromised a host (recorded,
        # not hidden); when present it is a positive sim time.
        if summary.mttc is not None:
            assert summary.mttc > 0


def test_g5_at_least_one_class_drives_a_compromise() -> None:
    """Non-degeneracy floor: the loop end-to-end compromises hosts on at least one
    profile (proving the substrate outcome oracle is actually driven)."""
    results = run_smoke_matrix(
        PROFILES, (1234,), with_synthetic_overlay=True, horizon=2500,
        overlay=_RefOverlay(), verdict_of=_verdict, register_for_interrupts=False,
    )
    assert any(r.compromised_count > 0 for r in results)


# --- G1: native golden neutrality ------------------------------------------
def test_g1_native_no_mtd_golden_headline_unperturbed() -> None:
    """The native 6-phase attacker (proceed_attack) still reproduces the committed
    no-MTD golden headline. The movement layer added no shared-path behaviour."""
    random.seed(1234)
    np.random.seed(1234)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(env=env, end_event=end_event, adversary=adversary,
                                proceed_time=0)
    attack_op.proceed_attack()
    env.run(until=15000)

    assert len(adversary.get_attack_stats().get_record()) == 692
    assert len(adversary.get_compromised_hosts()) == 41


# --- G6: the action-set freeze, as a structural invariant -------------------
#
# This replaced a git-diff check that asserted nothing under `mtdnetwork/component`
# or `mtdnetwork/mtdai` had changed. That guard was doubly wrong. Mechanically it
# compared the *working tree* against HEAD, so it passed the moment a change was
# committed — it could only ever catch uncommitted edits. And substantively it
# guarded the wrong thing: the S2 freeze is on **adapting the attacker's phases and
# verbs to the experiments**, not on repairing defects in the inherited simulator.
# Verified bug fixes under `mtdnetwork/` are sanctioned (supervisor, 2026-07-27); a
# seventh verb, a new attacker state, or a re-timed phase is not.
#
# So the invariant is asserted structurally instead, which holds regardless of what
# is committed.

# The six inherited verbs — the whole attacker vocabulary (S2).
_FROZEN_ACTION_SET = frozenset({
    "SCAN_HOST", "ENUM_HOST", "SCAN_PORT",
    "EXPLOIT_VULN", "BRUTE_FORCE", "SCAN_NEIGHBOR",
})

# The adversary's state fields. A new one means a new attacker ability, which is
# exactly what the freeze forbids.
_FROZEN_ADVERSARY_STATE = frozenset({
    "network", "_compromised_users", "_compromised_hosts", "_host_stack",
    "_attack_counter", "_stop_attack", "_attack_threshold", "_pivot_host_id",
    "_curr_host_id", "curr_host", "_curr_ports", "_curr_vulns",
    "_max_attack_attempts", "_curr_attempts", "target_compromised",
    "observed_changes", "_attack_stats", "_curr_process",
})


def test_g6_action_set_is_frozen() -> None:
    """S2: no attacker action added, removed, split or altered, and no new
    attacker state — asserted against the code, not against a git diff."""
    from mtdnetwork.data.constants import ATTACK_DURATION

    # One executable core per verb, and no more. (Names are not asserted against the
    # verb strings: the SCAN_NEIGHBOR core is spelled `_do_scan_neighbors`.)
    cores = {name for name in dir(AttackOperation) if name.startswith("_do_")}
    assert len(cores) == len(_FROZEN_ACTION_SET), (
        f"the attacker gained or lost an executable core (S2 freeze): {sorted(cores)}"
    )

    # Every verb is priced, and nothing else is (PENALTY is a cost, not a verb).
    priced = set(ATTACK_DURATION) - {"PENALTY"}
    assert priced == _FROZEN_ACTION_SET, (
        f"ATTACK_DURATION no longer prices exactly the six verbs: "
        f"{priced ^ _FROZEN_ACTION_SET}"
    )

    # proceed_attack still dispatches the same vocabulary and no more.
    import inspect
    import re

    source = inspect.getsource(AttackOperation.proceed_attack)
    dispatched = set(re.findall(r"get_curr_process\(\) == '([A-Z_]+)'", source))
    assert dispatched == _FROZEN_ACTION_SET, (
        f"proceed_attack dispatches a different vocabulary: "
        f"{dispatched ^ _FROZEN_ACTION_SET}"
    )


def test_g6_no_new_attacker_state() -> None:
    """S2: the adversary carries no state field beyond the inherited set."""
    random.seed(1234)
    np.random.seed(1234)
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)

    fields = {k for k in vars(adversary) if not k.startswith("__")}
    assert fields == _FROZEN_ADVERSARY_STATE, (
        f"attacker state changed (S2 freeze): {fields ^ _FROZEN_ADVERSARY_STATE}"
    )
