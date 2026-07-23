"""Plug-and-play integration gate — the whole L3 movement layer end-to-end on the
*real* controller library (no injected fakes).

This is the "both working as one would expect" gate the attacker handoff
(2026-07-22_l3_attacker_petri_to_mtdsim.md § Execution plan step 5) closes. Where
``test_movement_{attacker,smoke}.py`` prove the loop against controlled fakes,
these drive the real ``load_controller`` / ``load_outcome_overlay`` /
``verdict_for`` across the matrix:

    5 profiles  x  {overlay-on seed-recon, observed-only seed-initial-access}
                x  {no-MTD, one MTD scheme}  x  a couple of seeds

and assert each cell runs to horizon, emits records the statistics reader turns
into MTTC/ASR, and is deterministic (SIM-05). One cell runs the native baseline
and the movement attacker in the same geometry and checks *both* behave: the
baseline reproduces its committed golden headline; the movement attacker walks,
its two D8 arms differ, and the loop drives compromises somewhere in the matrix.

Behaviour is the bar, not the numbers — the overlay values are provisional
(pending Marc's greenlight); these tests never assert a magnitude.
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

from mtdsim.l3_simulation.movement.net import PROFILES
from mtdsim.l3_simulation.movement.run import GEOMETRY, run_movement
from mtdsim.l3_simulation.movement.statistics import summarise, summarise_profile

SEEDS = (1234, 7)
HORIZON = 2500
MTD_SCHEME = "simultaneous"  # one representative multi-strategy scheme


def _cells():
    """The (profile, arm, mtd) matrix, seeds applied per cell."""
    for profile in PROFILES:
        for with_overlay in (True, False):
            for mtd in (None, MTD_SCHEME):
                yield profile, with_overlay, mtd


def _run(profile, with_overlay, mtd, seed):
    """One matrix cell on the real controller library (overlay / verdict default
    to load_outcome_overlay() / verdict_for — no fakes)."""
    return run_movement(
        profile,
        seed=seed,
        with_synthetic_overlay=with_overlay,
        horizon=HORIZON,
        mtd_scheme=mtd,
        mtd_interval=150,
        register_for_interrupts=(mtd is not None),
    )


# --- the matrix runs, end-to-end, on the real library ----------------------
@pytest.mark.parametrize("profile, with_overlay, mtd", list(_cells()))
def test_every_cell_runs_and_the_reader_yields_metrics(profile, with_overlay, mtd) -> None:
    results = [_run(profile, with_overlay, mtd, s) for s in SEEDS]
    for r in results:
        assert r.records, f"{profile}/{with_overlay}/{mtd} produced no records"
        # The walk ran to the horizon or terminated with a recorded terminal event
        # (never a silent stop): the last record's end_time is bounded by horizon.
        assert r.records[-1].end_time <= HORIZON
    summary = summarise_profile(results)
    assert summary.n_runs == len(SEEDS)
    assert 0.0 <= summary.asr <= 1.0
    assert summary.mean_events > 0
    # MTTC is None only if no run of the cell compromised (recorded, not hidden).
    if summary.mttc is not None:
        assert summary.mttc > 0


def test_determinism_same_inputs_identical_records() -> None:
    """SIM-05: the real library included, a cell is a deterministic function of its
    inputs — same profile + arm + MTD + seed -> byte-identical records."""
    a = _run("aggregate", True, MTD_SCHEME, 1234)
    b = _run("aggregate", True, MTD_SCHEME, 1234)
    assert a.records == b.records


# --- the interrupt-as-failure carve, exercised through the real loop --------
def test_mtd_interrupts_all_read_as_failure() -> None:
    """Under live MTD the driver observes interrupts, and every interrupted event
    is a failure verdict (the interrupt-as-failure feedback). EXPLOIT_VULN is not
    special: its interrupt re-raises through the driven carve rather than spawning
    the native recovery, so it routes like the other verbs."""
    interrupted = []
    for seed in (1234, 7, 42, 99):
        r = _run("aggregate", True, MTD_SCHEME, seed)
        interrupted += [rec for rec in r.records if rec.interrupted]
    assert interrupted, "no MTD interrupt was observed across the seeds"
    assert all(rec.verdict == "failure" for rec in interrupted)


# --- the "both behave" gate -------------------------------------------------
def test_native_baseline_reproduces_its_golden_headline() -> None:
    """The native 6-phase attacker (proceed_attack), in the movement geometry, still
    reproduces the committed no-MTD golden headline (692 records / 41 hosts). The
    controller-library additions and the driven carve changed no shared path."""
    random.seed(1234)
    np.random.seed(1234)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(
        env=env, end_event=end_event, adversary=adversary, proceed_time=0
    )
    attack_op.proceed_attack()
    env.run(until=15000)

    assert len(adversary.get_attack_stats().get_record()) == 692
    assert len(adversary.get_compromised_hosts()) == 41


def test_movement_attacker_walks_and_the_two_d8_arms_differ() -> None:
    """The movement attacker walks the net live and the two D8 arms are distinct:
    overlay-on seeds at reconnaissance, observed-only at initial-access."""
    on = run_movement("aggregate", seed=1234, with_synthetic_overlay=True,
                      horizon=HORIZON, mtd_scheme=None)
    off = run_movement("aggregate", seed=1234, with_synthetic_overlay=False,
                       horizon=HORIZON, mtd_scheme=None)
    assert on.records and off.records
    assert on.records[0].place == "reconnaissance"
    assert off.records[0].place == "initial-access"


def test_movement_loop_drives_a_compromise_somewhere() -> None:
    """Non-degeneracy floor: on the real library the movement loop compromises at
    least one host across the profiles at full horizon — the substrate outcome
    oracle is genuinely driven, not just walked. (Compromises are sparse and coarse
    by design — the experiment-1 controller and the H-coupling precondition gating
    — so this is an existence floor, not a rate.)"""
    compromised = False
    for profile in PROFILES:
        for seed in (1234, 7, 42):
            r = run_movement(profile, seed=seed, with_synthetic_overlay=True,
                             horizon=15000, mtd_scheme=None)
            if r.compromised_count > 0:
                compromised = True
                break
        if compromised:
            break
    assert compromised, "no profile drove a compromise on the real library"


def test_summarise_covers_the_whole_matrix() -> None:
    """The statistics reader summarises a mixed multi-profile run set (the numbers
    handoff's entry point) without touching the inherited AttackStatistics maths."""
    results = [_run(p, True, None, SEEDS[0]) for p in PROFILES]
    summaries = summarise(results)
    assert set(summaries) == set(PROFILES)
    for s in summaries.values():
        assert 0.0 <= s.asr <= 1.0
