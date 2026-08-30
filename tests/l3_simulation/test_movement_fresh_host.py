"""The fresh-host contract — the order-independent verb contract restored on
the movement seam (Marc's ruling, 2026-08-30; register T1 annotation; handoff
``2026-08-30_fsm_token_hold_rule`` §Design).

What these pin, in order of load-bearing-ness:

1. **The invariant.** Under the contract the movement arm never fires a
   compromise verb (SCAN_PORT / EXPLOIT_VULN / BRUTE_FORCE) on a host it already
   owns — across profiles, seeds and MTD conditions, read off the record's
   ``on_owned_host`` field (substrate ground truth sampled before ``step``).
2. **The off switch is the old attacker.** ``fresh_host_contract=False``
   reproduces the record streams captured on ``d127f443`` *before* the contract
   existed, field for field (``fixtures/movement_prechange_2026-08-30.json``).
   That fixture is the movement golden the re-baseline diffs against.
3. **The on switch is the new golden.** The same cells under the contract match
   ``fixtures/movement_contract_2026-08-30.json``, captured in the commit that
   landed the contract, so any later drift in the reported attacker is loud.
4. The three state-delta verdict rows, and the invariants the record fields
   carry (``enum_repops`` audits the clock-free loop; ENUM_HOST never reports
   an owned host under the contract).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from mtdsim.l3_simulation.controller import load_outcome_overlay
from mtdsim.l3_simulation.controller.verdict import (
    ENUM_EXHAUSTED,
    NEIGHBORS_NONE_FRESH,
    SCAN_PORT_EMPTY,
    verdict_for,
)
from mtdsim.l3_simulation.movement.net import PROFILES
from mtdsim.l3_simulation.movement.run import run_movement

FIXTURES = Path(__file__).resolve().parent / "fixtures"
COMPROMISE = {"SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE"}

# The fixture cells' configuration (experiment 2's, at a 3 000 t/u horizon).
CELL = dict(
    horizon=3000,
    mapping_version="v2_partial",
    retrace_sinks=True,
    mtd_interval=200,
)


def _overlay():
    return load_outcome_overlay(version="v3_persistent_backward")


def _fields(records):
    return [
        [
            r.step_index, r.place, r.verb, r.outcome, r.verdict, r.next_place,
            round(r.start_time, 6), round(r.end_time, 6), round(r.dwell, 6),
            r.interrupted, r.blocked, r.n_compromised,
        ]
        for r in records
    ]


def _fixture(name: str) -> list[dict]:
    return json.loads((FIXTURES / name).read_text())["cells"]


# --- 1. the invariant --------------------------------------------------------


@pytest.mark.parametrize("scheme", [None, "simultaneous"])
@pytest.mark.parametrize("seed", [0, 1234])
@pytest.mark.parametrize("profile", PROFILES)
def test_a_compromise_verb_never_fires_on_an_owned_host(profile, seed, scheme) -> None:
    """The contract's invariant, on the real substrate: every non-blocked
    compromise verb fired on a host the adversary did not yet own."""
    run = run_movement(profile, seed=seed, overlay=_overlay(), mtd_scheme=scheme, **CELL)
    fired = [r for r in run.records if r.verb in COMPROMISE and not r.blocked]
    assert fired, f"{profile}/{seed}/{scheme}: no compromise verb fired at all"
    offending = [r for r in fired if r.on_owned_host]
    assert not offending, (
        f"{profile}/{seed}/{scheme}: {len(offending)} compromise verb(s) fired on an "
        f"owned host under the contract, e.g. step {offending[0].step_index} "
        f"{offending[0].verb}"
    )


def test_without_the_contract_the_churn_is_measurable_from_the_record() -> None:
    """The field the invariant is asserted on is not vacuous: with the contract
    off, the same cell shows compromise verbs landing on owned hosts — the
    re-compromise churn the loop fix removes, now a per-record fact."""
    run = run_movement("aggregate", seed=0, overlay=_overlay(),
                       fresh_host_contract=False, horizon=15_000,
                       mapping_version="v2_partial", retrace_sinks=True)
    fired = [r for r in run.records if r.verb in COMPROMISE and not r.blocked]
    assert sum(r.on_owned_host for r in fired) > 0
    assert all(r.enum_repops == 0 and not r.reselected for r in run.records)


def test_enum_host_never_reports_an_owned_host_under_the_contract() -> None:
    """The retry-until-fresh loop: ENUM_HOST's bare ``True`` (popped an owned
    host) never reaches the record — it is re-popped to a fresh host (``FALSE``)
    or the queue runs dry (``ENUM_EXHAUSTED``). The pops are audited."""
    run = run_movement("aggregate", seed=0, overlay=_overlay(), horizon=15_000,
                       mapping_version="v2_partial", retrace_sinks=True)
    enums = [r for r in run.records if r.verb == "ENUM_HOST" and not r.blocked
             and not r.interrupted]
    assert enums
    assert all(r.outcome in {"FALSE", ENUM_EXHAUSTED} for r in enums), {
        r.outcome for r in enums
    }
    assert any(r.enum_repops > 0 for r in run.records), "the loop never re-popped"
    # Only ENUM_HOST itself and the guarded compromise verbs can carry re-pops.
    for r in run.records:
        if r.enum_repops:
            assert r.verb == "ENUM_HOST" or r.reselected, r


def test_the_guard_re_selects_and_never_changes_the_verb() -> None:
    """A re-selected visit keeps the verb the token chose; the guard is a
    pre-step inside the same visit (contract rule 2)."""
    run = run_movement("aggregate", seed=0, overlay=_overlay(), horizon=15_000,
                       mapping_version="v2_partial", retrace_sinks=True)
    reselected = [r for r in run.records if r.reselected]
    assert reselected, "the guard never fired at this seed"
    assert all(r.verb in COMPROMISE for r in reselected)
    # A guard that found a fresh host popped at least once; one that found the
    # visible queue already empty popped nothing and the visit blocked.
    assert all(r.enum_repops >= 1 or r.blocked for r in reselected)
    assert any(r.enum_repops >= 1 and not r.blocked for r in reselected)
    assert all(not r.on_owned_host for r in reselected)


# --- 2./3. the two movement goldens -------------------------------------------


@pytest.mark.parametrize("cell", _fixture("movement_prechange_2026-08-30.json"),
                         ids=lambda c: f"{c['profile']}/{c['seed']}/{c['scheme']}")
def test_contract_off_reproduces_the_pre_change_record_stream(cell) -> None:
    """``fresh_host_contract=False`` is the attacker every record before
    2026-08-30 was produced by — bit for bit, on the fixture captured from
    ``d127f443`` before the contract landed."""
    run = run_movement(cell["profile"], seed=cell["seed"], overlay=_overlay(),
                       mtd_scheme=cell["scheme"], fresh_host_contract=False, **CELL)
    assert _fields(run.records) == cell["records"]
    assert run.compromised_count == cell["compromised_count"]
    assert round(run.termination_time, 6) == cell["termination_time"]


@pytest.mark.parametrize("cell", _fixture("movement_contract_2026-08-30.json"),
                         ids=lambda c: f"{c['profile']}/{c['seed']}/{c['scheme']}")
def test_contract_on_matches_the_re_baselined_record_stream(cell) -> None:
    """The reported attacker since 2026-08-30 — the re-baseline, captured in
    the commit that landed the contract. Drift here is a claim-integrity
    failure, not a routine regression."""
    run = run_movement(cell["profile"], seed=cell["seed"], overlay=_overlay(),
                       mtd_scheme=cell["scheme"], **CELL)
    assert _fields(run.records) == cell["records"]
    assert run.compromised_count == cell["compromised_count"]


def test_the_contract_is_deterministic() -> None:
    a = run_movement("objective_exfiltration", seed=7, overlay=_overlay(), **CELL)
    b = run_movement("objective_exfiltration", seed=7, overlay=_overlay(), **CELL)
    assert a.records == b.records


# --- 4. the verdict rows -------------------------------------------------------


@pytest.mark.parametrize("verb, outcome", [
    ("ENUM_HOST", ENUM_EXHAUSTED),
    ("SCAN_PORT", SCAN_PORT_EMPTY),
    ("SCAN_NEIGHBOR", NEIGHBORS_NONE_FRESH),
])
def test_the_state_delta_rows_read_as_failure(verb, outcome) -> None:
    assert verdict_for(verb, outcome, False) == "failure"


@pytest.mark.parametrize("verb, outcome", [
    ("ENUM_HOST", False), ("ENUM_HOST", True),
    ("SCAN_PORT", False), ("SCAN_PORT", True),
    ("SCAN_NEIGHBOR", None),
])
def test_the_bare_rows_are_unchanged(verb, outcome) -> None:
    """The dormant path: with the contract off the bare outcomes reach the
    adapter and read exactly as they always did."""
    assert verdict_for(verb, outcome, False) == "success"
    assert verdict_for(verb, outcome, True) == "failure"


def test_the_rows_are_reached_on_a_real_run() -> None:
    run = run_movement("aggregate", seed=0, overlay=_overlay(), horizon=15_000,
                       mapping_version="v2_partial", retrace_sinks=True)
    outcomes = {r.outcome for r in run.records}
    assert NEIGHBORS_NONE_FRESH in outcomes
    for r in run.records:
        if r.outcome in {ENUM_EXHAUSTED, SCAN_PORT_EMPTY, NEIGHBORS_NONE_FRESH}:
            assert r.verdict == "failure"
