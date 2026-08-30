"""The token-hold rule (register T1, Jin 2026-08-25) — the opaque hold as a
declared variant beside factor 9.

What these pin:

1. **The rule holds exactly the FSM-illegal draws and nothing else** (the V1
   hand-validation, mechanised): every rejected draw at a decision dispatches a
   verb outside the licensed set (or is dwell-only — the opaque reading), and
   every accepted draw is inside it, except where the decision abstained (no
   licensed destination existed) or fell through the declared bound.
2. **Null-equivalence.** No hold attached is today's run; a hold whose
   modulator sits at alpha = 0 changes routing *only* through holding.
3. **Abstention, the opaque reading, the interrupt re-key, and the bound**, as
   unit properties of the rule.
4. **Bookkeeping.** The record's hold fields sum to the rule's ledger; a held
   visit's dwell is the base draw plus the holds and never exceeds its elapsed
   time; determinism (SIM-05) holds with the hold attached.
5. ``run_movement`` refuses a hold whose modulator is not registered on the
   attacker state it reads.
"""
from __future__ import annotations

import pytest

from mtdsim.l3_simulation.controller import load_outcome_overlay
from mtdsim.l3_simulation.movement.learning_readiness import load_tactic_to_verb
from mtdsim.l3_simulation.movement.run import run_movement
from mtdsim.l3_simulation.movement.state import AttackerState
from mtdsim.l3_simulation.movement.succession import (
    FsmSuccessionModulator,
    TokenHoldRule,
    load_token_hold_parameters,
)

MAPPING = "v2_partial"
CELL = dict(horizon=3000, mapping_version=MAPPING, retrace_sinks=True, mtd_interval=200)


def _overlay():
    return load_outcome_overlay(version="v3_persistent_backward")


def _hold(seed: int, **kwargs):
    modulator = FsmSuccessionModulator(alpha=0.0, tactic_to_verb=load_tactic_to_verb(MAPPING))
    rule = TokenHoldRule(modulator, **kwargs)
    state = AttackerState(seed=seed, modulators=(modulator,))
    return rule, state


def _run(profile, seed, *, scheme=None, **kwargs):
    rule, state = _hold(seed, **kwargs)
    result = run_movement(profile, seed=seed, overlay=_overlay(), mtd_scheme=scheme,
                          attacker_state=state, token_hold=rule, **CELL)
    return rule, result


# --- 1. the hold is exactly the FSM-illegal draws -----------------------------


@pytest.mark.parametrize("scheme", [None, "simultaneous"])
@pytest.mark.parametrize("profile", ["aggregate", "objective_exfiltration", "objective_none_c2"])
def test_held_draws_are_exactly_the_unlicensed_ones(profile, scheme) -> None:
    rule, result = _run(profile, 0, scheme=scheme)
    assert rule.decisions > 0
    t2v = load_tactic_to_verb(MAPPING)
    held_decisions = 0
    for entry in rule.log:
        licensed = set(entry["licensed"])
        if entry["abstained"]:
            # No licensed destination — either from the start (no holds) or
            # after an interrupt mid-hold re-keyed the FSM state to a restart
            # verb this out-set cannot reach (holds already taken stay logged).
            assert not licensed
            held_decisions += bool(entry["rejected"])
            continue
        assert licensed, entry
        # Opaque: a dwell-only place is never a licensed destination.
        assert all(t2v.get(d) is not None for d in licensed), entry
        for rejected, licensed_then in entry["rejected"]:
            # Judged against the licensed set in force at that draw — an MTD
            # interrupt mid-hold may have re-keyed it since.
            assert rejected not in set(licensed_then), entry
            assert all(t2v.get(d) is not None for d in licensed_then), entry
        if entry["fell_through"]:
            assert len(entry["rejected"]) == rule.max_consecutive
        else:
            assert entry["accepted"] in licensed, entry
        held_decisions += bool(entry["rejected"])
    assert held_decisions == sum(1 for r in result.records if r.holds)
    assert rule.holds == sum(r.holds for r in result.records)
    assert rule.hold_dwell == pytest.approx(sum(r.hold_dwell for r in result.records))


def test_the_hold_visibly_changes_the_walk_and_costs_time() -> None:
    plain = run_movement("aggregate", seed=0, overlay=_overlay(), **CELL)
    rule, held = _run("aggregate", 0)
    assert rule.holds > 0
    assert [r.place for r in held.records] != [r.place for r in plain.records]
    # Fewer actions fit in the same horizon: the hold only ever delays.
    assert sum(1 for r in held.records if r.verb) < sum(1 for r in plain.records if r.verb)


# --- 2. null-equivalence -----------------------------------------------------


def test_no_hold_is_todays_run_even_with_the_tracking_modulator_attached() -> None:
    plain = run_movement("aggregate", seed=1234, overlay=_overlay(), **CELL)
    modulator = FsmSuccessionModulator(alpha=0.0, tactic_to_verb=load_tactic_to_verb(MAPPING))
    state = AttackerState(seed=1234, modulators=(modulator,))
    tracked = run_movement("aggregate", seed=1234, overlay=_overlay(),
                           attacker_state=state, **CELL)
    assert tracked.records == plain.records
    assert all(r.holds == 0 and r.hold_dwell == 0.0 for r in plain.records)


# --- 3. the rule's unit properties --------------------------------------------


def _modulator(targets, held):
    m = FsmSuccessionModulator(alpha=0.0, tactic_to_verb=load_tactic_to_verb(MAPPING))
    m.targets = frozenset(targets)
    m.cursor.held = frozenset(held)
    return m


def test_dwell_only_destinations_are_never_licensed_the_opaque_reading() -> None:
    rule = TokenHoldRule(_modulator({"BRUTE_FORCE"}, {"host_stack", "curr_host"}))
    composed = {"credential-access": 0.4, "collection": 0.3, "command-and-control": 0.3}
    assert rule.licensed_destinations(composed) == frozenset({"credential-access"})


def test_the_abstention_rule_no_licensed_destination_means_no_hold() -> None:
    rule = TokenHoldRule(_modulator({"BRUTE_FORCE"}, {"host_stack", "curr_host"}))
    composed = {"command-and-control": 0.5, "reconnaissance": 0.5}  # SCAN_NEIGHBOR, SCAN_HOST
    assert rule.licensed_destinations(composed) == frozenset()


def test_the_capability_fallback_re_aims_an_unrunnable_successor() -> None:
    """EXPLOIT_VULN licensed but nothing held: the licensed destinations are
    the ones that open a shortest route (SCAN_HOST), not the exploit."""
    rule = TokenHoldRule(_modulator({"EXPLOIT_VULN"}, set()))
    composed = {"reconnaissance": 0.5, "execution": 0.5}
    assert rule.licensed_destinations(composed) == frozenset({"reconnaissance"})


def test_an_interrupt_re_keys_the_licensed_set_before_the_next_verdict() -> None:
    """Mid-hold the substrate's interrupt handler overrides its dispatch, so a
    pending interrupt must be honoured by the hold immediately — while
    ``factors`` (which never sees one) is untouched."""
    modulator = _modulator({"EXPLOIT_VULN"}, {"host_stack", "curr_host", "curr_ports"})
    rule = TokenHoldRule(modulator)
    composed = {"execution": 0.5, "reconnaissance": 0.5}
    assert rule.licensed_destinations(composed) == frozenset({"execution"})
    modulator.observe_mtd_interrupt("network")
    assert rule.licensed_destinations(composed) == frozenset({"reconnaissance"})
    assert modulator.targets == frozenset({"EXPLOIT_VULN"})  # consumed only at the verdict


def test_the_bound_falls_through_and_is_counted() -> None:
    rule, result = _run("aggregate", 0, max_consecutive=1)
    assert rule.fall_throughs > 0
    assert rule.fall_throughs == sum(1 for r in result.records if r.hold_fell_through)
    assert all(r.holds <= 1 for r in result.records)


def test_the_declared_bound_is_read_from_the_rules_artefact() -> None:
    params = load_token_hold_parameters()
    assert params.max_consecutive_holds >= 1
    rule, _ = _hold(0)
    assert rule.max_consecutive == params.max_consecutive_holds
    with pytest.raises(ValueError):
        _hold(0, max_consecutive=0)


# --- 4. bookkeeping ------------------------------------------------------------


def test_a_held_visits_dwell_never_exceeds_its_elapsed_time() -> None:
    for scheme in (None, "simultaneous"):
        _, result = _run("aggregate", 7, scheme=scheme)
        for r in result.records:
            assert r.hold_dwell <= r.dwell + 1e-9
            assert r.dwell <= (r.end_time - r.start_time) + 1e-9, r


def test_the_hold_is_deterministic() -> None:
    _, a = _run("objective_impact", 42)
    _, b = _run("objective_impact", 42)
    assert a.records == b.records


# --- 5. wiring ---------------------------------------------------------------


def test_run_movement_refuses_an_unregistered_hold() -> None:
    modulator = FsmSuccessionModulator(alpha=0.0, tactic_to_verb=load_tactic_to_verb(MAPPING))
    rule = TokenHoldRule(modulator)
    with pytest.raises(ValueError):
        run_movement("aggregate", seed=0, overlay=_overlay(), token_hold=rule, **CELL)
    with pytest.raises(ValueError):
        run_movement("aggregate", seed=0, overlay=_overlay(), token_hold=rule,
                     attacker_state=AttackerState(seed=0), **CELL)
