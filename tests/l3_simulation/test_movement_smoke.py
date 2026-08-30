"""Smoke matrix, boundary audit, and golden-neutrality for the movement layer.

Covers the M7 handoff's remaining gates:

  G1  goldens pass: the native 6-phase attacker still reproduces the no-MTD golden
      headline (1676 events / 34 compromised, seed 1234, 15 ks; re-baselined 2026-08-27, D-19/D-18) — the movement-layer
      additions changed no shared code path.
  G5  the smoke matrix: all five profiles (4 classes + aggregate) run to horizon on
      the smoke cell, emitting non-degenerate records the statistics reader turns
      into MTTC / ASR.
  G6  the action-set freeze (S2), asserted structurally: exactly six verbs,
      priced and dispatched, and no new attacker state.

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

    assert len(adversary.get_attack_stats().get_record()) == 1676
    assert len(adversary.get_compromised_hosts()) == 34


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
# exactly what the freeze forbids — save for the one deliberate lift below.
#
# The three `_exploit_learning_*` / `_exploit_type_*` fields carry the
# compound-exploit-learning memory. The S2 freeze is lifted for THIS ONE
# mechanism by Marc's disposition (2026-08-11) — a sanctioned substrate
# attack-model extension, not a bug fix
# (docs/implementation/pipeline/ogasp/exploit_learning.md). They are enumerated
# here rather than exempted so the guard still fails loudly on any *other*
# unsanctioned state addition.
_FROZEN_ADVERSARY_STATE = frozenset({
    "network", "_compromised_users", "_compromised_hosts", "_host_stack",
    "_attack_counter", "_stop_attack", "_attack_threshold", "_pivot_host_id",
    "_curr_host_id", "curr_host", "_curr_ports", "_curr_vulns",
    "_max_attack_attempts", "_curr_attempts", "target_compromised",
    "observed_changes", "_attack_stats", "_curr_process",
    "_exploit_learning_enabled", "_exploit_learning_rate", "_exploit_type_counts",
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


# ---------------------------------------------------------------------------
# The progress-trajectory field's three claimed properties, asserted on live runs
# rather than argued in the docstring. It is substrate ground truth sampled
# in-layer, so if any of these fails the disengagement reader is reading a
# quantity that is not what it says it is.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("scheme", [None, "random"])
def test_the_progress_trajectory_is_monotone_and_ends_at_the_run_total(scheme) -> None:
    """``n_compromised`` must be non-decreasing across a run and must finish at
    exactly ``compromised_count`` — the same substrate list, sampled per record
    against read once at the end. Checked under MTD as well, because a
    network-layer mutation remaps host ids in the compromised list and a remap
    that lost or duplicated an entry would show up here first."""
    from mtdsim.l3_simulation.controller import load_outcome_overlay
    from mtdsim.l3_simulation.movement.run import run_movement

    for profile in ("aggregate", "objective_exfiltration"):
        run = run_movement(
            profile, seed=5, horizon=6_000, mapping_version="v2_partial",
            overlay=load_outcome_overlay(version="v3_persistent_backward"),
            mtd_scheme=scheme, mtd_interval=200,
        )
        traj = [r.n_compromised for r in run.records]
        assert traj, f"no records for {profile}"
        assert all(b >= a for a, b in zip(traj, traj[1:])), (
            f"progress went backwards in {profile}/{scheme}: {traj}"
        )
        assert traj[-1] == run.compromised_count, (
            f"{profile}/{scheme}: trajectory ends at {traj[-1]}, "
            f"compromised_count is {run.compromised_count}"
        )


def test_compromise_events_over_count_distinct_hosts() -> None:
    """The measurement that justified widening the record, kept as a regression
    — and revisited on 2026-08-30, as its own docstring required.

    The suite's standing preference is to extend the reader rather than widen the
    schema, so the burden of proof sat on this: cumulative compromise *events*
    are not a sound proxy for distinct hosts, because the record carries no host
    identity and re-compromise is counted again. That over-count WAS the
    re-compromise churn, and the fresh-host contract (on by default since
    2026-08-30) removes it by construction: a compromise verb fires only on a
    fresh host, so every compromise event is a new host and the two counts
    coincide. Both halves are pinned — the over-count on the attacker the field
    was measured on (contract off, still reachable), and the equality the
    contract restores (which is the contract's invariant restated on the record,
    and the reason the field is now *verifiable* rather than merely necessary).
    """
    from mtdsim.l3_simulation.controller import load_outcome_overlay
    from mtdsim.l3_simulation.movement import measures as M
    from mtdsim.l3_simulation.movement.run import run_movement

    common = dict(
        horizon=15_000, mapping_version="v2_partial",
        overlay=load_outcome_overlay(version="v3_persistent_backward"),
        mtd_scheme=None, mtd_interval=200,
    )
    churning = run_movement("aggregate", seed=1, fresh_host_contract=False, **common)
    events = sum(1 for r in churning.records if M.is_compromise(r))
    assert churning.compromised_count > 0
    assert events > churning.compromised_count, (
        "compromise events no longer over-count distinct hosts on the contract-off "
        "attacker; the schema change's justification needs re-checking"
    )
    fixed = run_movement("aggregate", seed=1, **common)
    events = sum(1 for r in fixed.records if M.is_compromise(r))
    assert fixed.compromised_count > 0
    assert events == fixed.compromised_count, (
        "under the fresh-host contract every compromise event must be a fresh "
        "host — a compromise verb fired on an owned host"
    )
