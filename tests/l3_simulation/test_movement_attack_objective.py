"""The ``attack_objective`` input — wired vacuously (2026-08-30).

Brown's two scenarios (IS-SCN-02 general, IS-SCN-03 targeted) get one named
top-level input on the attack model. Today it is a label: validated, carried,
echoed onto the result, consulted by no control flow. These tests pin exactly
that, so the day the targeted policy lands the *third* test is the one that
must be retired (it asserts the two objectives are bit-identical).
"""

from __future__ import annotations

import pytest

from mtdsim.l3_simulation.movement.attacker import ATTACK_OBJECTIVES
from mtdsim.l3_simulation.movement.run import run_movement

CFG = dict(seed=3, horizon=1500, mapping_version="v2_partial")


def _fields(result):
    return [
        (r.place, r.verb, r.start_time, r.end_time, r.outcome, r.n_compromised)
        for r in result.records
    ]


def test_objectives_are_exactly_browns_two() -> None:
    assert ATTACK_OBJECTIVES == ("general", "targeted")


def test_default_is_general_and_is_echoed_on_the_result() -> None:
    res = run_movement("aggregate", **CFG)
    assert res.attack_objective == "general"
    res_t = run_movement("aggregate", attack_objective="targeted", **CFG)
    assert res_t.attack_objective == "targeted"


def test_targeted_is_vacuous_today_bit_identical_to_general() -> None:
    """Retire this test when the targeted host-selection policy lands."""
    general = run_movement("aggregate", attack_objective="general", **CFG)
    targeted = run_movement("aggregate", attack_objective="targeted", **CFG)
    unset = run_movement("aggregate", **CFG)
    assert _fields(general) == _fields(unset)
    assert _fields(targeted) == _fields(general)
    assert targeted.compromised_count == general.compromised_count
    assert targeted.database_hosts_reached == general.database_hosts_reached


def test_unknown_objective_is_refused() -> None:
    with pytest.raises(ValueError, match="attack_objective"):
        run_movement("aggregate", attack_objective="apt", **CFG)
