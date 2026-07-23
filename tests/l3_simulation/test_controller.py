"""L3 controller map — validation gate (experiment 1).

The controller is the CKC-mediated ``tactic -> MTDSim-phase`` position map, fed
to the movement layer as an input parameter. These tests fix its contract:
loads cleanly, every net tactic resolves to exactly one of the six verbs
(complete coverage), and the map's tactic set matches the built nets' places.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from mtdsim.l3_simulation.controller import SIM_PHASES, Controller, load_controller

REPO_ROOT = Path(__file__).resolve().parents[2]
AGG_NET = REPO_ROOT / "data" / "ogasp" / "petri" / "aggregate_structural.json"

# The 15 tactics the aggregate net carries (full GAP tactic-quotient).
EXPECTED_TACTICS = 15


@pytest.fixture(scope="module")
def controller() -> Controller:
    return load_controller()


def test_loads_and_is_non_empty(controller: Controller) -> None:
    assert len(controller.rows) == EXPECTED_TACTICS


def test_complete_coverage_every_tactic_one_verb(controller: Controller) -> None:
    """Every tactic resolves to exactly one of the six verbs — the whole point."""
    for tactic in controller.tactics:
        phase = controller.phase_for(tactic)
        assert phase in SIM_PHASES


def test_map_tactics_match_the_net_places(controller: Controller) -> None:
    """The controller covers precisely the tactic-places the aggregate net has."""
    net = json.loads(AGG_NET.read_text(encoding="utf-8"))
    net_places = set(net["places"])
    assert set(controller.tactics) == net_places


def test_dispatch_matches_the_locked_brown_position_map(controller: Controller) -> None:
    """The experiment-1 mapping is locked; guard against silent drift."""
    m = controller.as_dict()
    assert m["reconnaissance"] == "SCAN_HOST"
    assert m["resource-development"] == "ENUM_HOST"
    assert m["initial-access"] == "SCAN_PORT"
    assert m["execution"] == "EXPLOIT_VULN"
    assert m["persistence"] == "BRUTE_FORCE"
    assert m["command-and-control"] == "SCAN_NEIGHBOR"
    # Actions-on-Objectives band falls back to the neighbour-reveal verb.
    for objective in ("credential-access", "discovery", "lateral-movement",
                      "collection", "exfiltration", "impact"):
        assert m[objective] == "SCAN_NEIGHBOR"


def test_all_six_verbs_are_used(controller: Controller) -> None:
    """The map exercises the full verb set (no dead verb under this parameter)."""
    assert set(controller.as_dict().values()) == set(SIM_PHASES)


def test_unknown_tactic_raises(controller: Controller) -> None:
    with pytest.raises(KeyError):
        controller.phase_for("not-a-tactic")
