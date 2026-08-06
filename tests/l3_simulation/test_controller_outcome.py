"""Controller-library unit tests — the verdict adapter and the M2 composition.

These pin the two pure functions the movement layer consumes, against the *real*
controller artefacts (no injected fakes):

- ``verdict_for`` — the per-verb success/failure oracle (controller.md §4).
- ``OutcomeOverlay.compose`` — the multiply-renormalise rule with absent-vs-
  present-zero factor semantics and the stall (success_failure_overlay_design.md
  §1/§3).

Kept apart from ``test_controller.py`` (which fixes the dispatch map) so the two
concerns — dispatch vs outcome — read independently.
"""
from __future__ import annotations

import pytest

from mtdnetwork.operation.attack_operation import (
    EXPLOIT_COMPROMISED,
    EXPLOIT_HALTED,
    EXPLOIT_UNCOMPROMISED,
)
from mtdsim.l3_simulation.controller import (
    OutcomeOverlay,
    load_outcome_overlay,
    verdict_for,
)
from mtdsim.l3_simulation.movement.net import load_routing_net


# --- verdict_for (controller.md §4) ----------------------------------------
@pytest.mark.parametrize(
    "verb, outcome, interrupted, expected",
    [
        ("EXPLOIT_VULN", EXPLOIT_COMPROMISED, False, "success"),
        ("EXPLOIT_VULN", EXPLOIT_UNCOMPROMISED, False, "failure"),
        ("EXPLOIT_VULN", EXPLOIT_HALTED, False, "failure"),
        ("SCAN_HOST", True, False, "success"),
        ("SCAN_HOST", False, False, "failure"),
        ("BRUTE_FORCE", True, False, "success"),
        ("BRUTE_FORCE", False, False, "failure"),
        # Success unless interrupted (documented simplification).
        ("ENUM_HOST", False, False, "success"),
        ("SCAN_PORT", False, False, "success"),
        ("SCAN_NEIGHBOR", None, False, "success"),
    ],
)
def test_verdict_for_per_verb_outcome(verb, outcome, interrupted, expected) -> None:
    assert verdict_for(verb, outcome, interrupted) == expected


@pytest.mark.parametrize(
    "verb, outcome",
    [
        ("EXPLOIT_VULN", EXPLOIT_COMPROMISED),  # would be success uninterrupted
        ("SCAN_HOST", True),
        ("SCAN_NEIGHBOR", None),
        ("SCAN_PORT", True),
    ],
)
def test_an_interrupt_is_always_a_failure(verb, outcome) -> None:
    """An MTD interrupt reads as failure whatever the verb or its outcome — the
    net falls back (register §M1, the interrupt-as-failure feedback)."""
    assert verdict_for(verb, outcome, interrupted=True) == "failure"


def test_verdict_for_unknown_verb_raises() -> None:
    with pytest.raises(ValueError):
        verdict_for("NOT_A_VERB", True, False)


# --- OutcomeOverlay.compose (M2) -------------------------------------------
def test_compose_renormalises_to_one() -> None:
    overlay = load_outcome_overlay()
    net = load_routing_net("aggregate", with_synthetic_overlay=True)
    base = net.base_out_weights("initial-access")
    for verdict in ("success", "failure"):
        composed = overlay.compose("initial-access", verdict, base)
        assert composed
        assert abs(sum(composed.values()) - 1.0) < 1e-9


def test_compose_verdict_selects_different_out_sets() -> None:
    """A success and a failure at the same place produce different composed
    distributions — the two-way feedback the substrate outcome drives, through
    the real numbers."""
    overlay = load_outcome_overlay()
    net = load_routing_net("aggregate", with_synthetic_overlay=True)
    base = net.base_out_weights("initial-access")
    succ = overlay.compose("initial-access", "success", base)
    fail = overlay.compose("initial-access", "failure", base)
    assert succ != fail
    # The backward regression bridge (initial-access -> reconnaissance) is what a
    # failure amplifies ("back to the drawing board"); a success suppresses it.
    assert fail["reconnaissance"] > succ["reconnaissance"]


def test_compose_absent_pair_is_a_passthrough_present_zero_suppresses() -> None:
    """A base edge the overlay does not name keeps its base weight (absent = 1.0
    passthrough); a pair the overlay carries with value 0 is hard-suppressed. This
    is the plug-and-play robustness property."""
    overlay = OutcomeOverlay(
        by_verdict={"success": {"a": {"b": 0.0}}},  # (a,b) present-zero; (a,c) absent
        by_rule={"success": {"a": {"b": "test"}}},
    )
    base = {"b": 0.5, "c": 0.5}
    composed = overlay.compose("a", "success", base)
    # b suppressed (present-zero), c passes through (absent) -> all mass on c.
    assert composed == {"c": 1.0}


def test_compose_stall_when_every_out_edge_suppressed() -> None:
    """If the verdict zeroes every out-edge the composition returns {} — the stall
    (design §3), which the movement driver reads as walk-termination. No default
    rule does this today, so it is a guarded edge case."""
    overlay = OutcomeOverlay(
        by_verdict={"failure": {"a": {"b": 0.0, "c": 0.0}}},
        by_rule={"failure": {"a": {"b": "z", "c": "z"}}},
    )
    assert overlay.compose("a", "failure", {"b": 0.5, "c": 0.5}) == {}


def test_compose_is_deterministic() -> None:
    """Same inputs -> same composed weights (SIM-05 for the composition)."""
    overlay = load_outcome_overlay()
    net = load_routing_net("objective_exfiltration", with_synthetic_overlay=True)
    place = net.entry_place
    base = net.base_out_weights(place)
    a = overlay.compose(place, "failure", base)
    b = overlay.compose(place, "failure", base)
    assert a == b
