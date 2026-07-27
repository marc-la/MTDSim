"""Regression tests for the two driver defects fixed in the 2026-07-27 action-layer
audit (``docs/implementation/pipeline/ogasp/action_layer_audit.md``, rows D1 and D2).

Both were in the carve/driver — code this project wrote, not inherited substrate —
so both were fixed rather than dispositioned. Neither touches the native FSM, so all
nine ``baseline/golden`` scenarios are unaffected.
"""

from __future__ import annotations

import pytest

from mtdsim.l3_simulation.movement.run import GEOMETRY, run_movement

MTD_KWARGS = dict(mtd_scheme="simultaneous", mtd_interval=200)


# --- D1: a verb that completes AND fires end_event must keep its outcome ----

def test_objective_completing_compromise_is_not_discarded_as_a_sim_end() -> None:
    """The compromise that *ends the run* must still be recorded as a compromise.

    Three verb cores call ``update_compromise_progress``, which fires ``end_event``
    once the objective is met. The driver used to infer "the sim ended mid-verb"
    from ``end_event.triggered``, so a verb that ran, succeeded, and completed the
    run was reclassified as a ``SIM_END`` abort and its outcome thrown away.

    The damage was a structural inconsistency between the two headline metrics: the
    run counted toward ASR (which reads ``end_event``) while contributing nothing to
    MTTC (which reads compromise events), so the single most important event in the
    run was the one event the reader could never see.

    Driven with a 1-host objective so the objective is actually reachable; at the
    experiment-1 ratio of 0.8 the movement arm never gets there, which is why this
    stayed invisible.
    """
    geometry = dict(GEOMETRY)
    geometry["terminate_compromise_ratio"] = 0.01  # objective = 1 host

    res = run_movement(
        "aggregate", seed=42, with_synthetic_overlay=True, horizon=15_000,
        mtd_scheme=None, geometry=geometry,
    )

    assert res.reached_objective, "expected this cell to reach the 1-host objective"
    assert res.compromised_count >= 1

    assert res.first_compromise_time() is not None, (
        "the objective-completing compromise was discarded: ASR counts this run a "
        "success while MTTC has no compromise event to average"
    )

    compromises = [
        r for r in res.records
        if (r.verb, r.outcome) in {
            ("EXPLOIT_VULN", "EXPLOIT_COMPROMISED"),
            ("BRUTE_FORCE", "TRUE"),
            ("SCAN_PORT", "TRUE"),
        }
    ]
    assert compromises, "no compromise event survived in the movement records"
    # The run still terminates visibly rather than just stopping.
    assert res.records[-1].outcome in ("SIM_END", "MAX_EVENTS")


def test_step_abort_sentinel_is_distinct_from_a_verbs_own_none() -> None:
    """``SCAN_NEIGHBOR`` legitimately returns ``None``; an abort must not."""
    from mtdnetwork.operation.attack_operation import STEP_ABORTED

    assert STEP_ABORTED is not None
    assert STEP_ABORTED != "NONE"


# --- D2: a dwell cut short by an MTD interrupt must not be over-reported ---

@pytest.mark.parametrize("profile, seed", [("aggregate", 42), ("pure_impediment", 0)])
def test_recorded_dwell_never_exceeds_the_events_elapsed_time(profile, seed) -> None:
    """``dwell`` is the time *consumed* at the place, so it can never exceed the
    event's own elapsed time.

    An MTD interrupt abandons the remaining dwell, but the driver used to record the
    full catalogue value regardless — leaving ~15 % of records under live MTD
    claiming more dwell than the whole event occupied, and making
    ``end_time - start_time - dwell`` (the verb's time cost) spuriously negative.
    """
    res = run_movement(
        profile, seed=seed, with_synthetic_overlay=True, horizon=15_000, **MTD_KWARGS
    )

    offenders = [
        r for r in res.records if (r.end_time - r.start_time) < r.dwell - 1e-9
    ]
    assert not offenders, (
        f"{len(offenders)}/{len(res.records)} records report more dwell than elapsed "
        f"time; first: {offenders[0]}"
    )

    # And the derived verb-time is non-negative everywhere.
    assert all((r.end_time - r.start_time) - r.dwell >= -1e-9 for r in res.records)


def test_uninterrupted_dwell_still_reports_the_catalogue_value_exactly(profile="aggregate") -> None:
    """The fix must not perturb the ~85 % of events whose dwell runs to completion —
    those still carry the catalogue value bit-for-bit, so prior analyses of clean
    events are unaffected."""
    from mtdsim.l3_simulation.movement.attacker import load_dwell_catalogue

    catalogue = load_dwell_catalogue()
    res = run_movement(
        profile, seed=42, with_synthetic_overlay=True, horizon=15_000, mtd_scheme=None
    )

    clean = [r for r in res.records if not r.interrupted and r.verb]
    assert clean, "no uninterrupted events to check"
    for r in clean:
        expected = float(catalogue.get(r.place, 0.0))
        assert r.dwell == expected, (
            f"uninterrupted event at {r.place} reported dwell {r.dwell}, "
            f"catalogue says {expected}"
        )
