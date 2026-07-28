"""L3 controller map — the validation gate for the versioned mapping registry.

The controller is the ``tactic -> MTDSim-phase`` map the experiments vary. These
tests fix its contract now that the mapping is *selectable data* rather than one
hard-wired file:

* the registry loads, and a version is chosen by name — a data selection, not a
  code edit;
* the experiment-1 mapping is immutable and still resolves exactly as it did;
* **the relaxed S4 invariant** — every tactic either resolves to one of the six
  verbs or is *declared* dwell-only, and silence is still an error;
* each registered version covers precisely the net's tactic-places.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from mtdsim.l3_simulation.controller import (
    DWELL_ONLY,
    MAPPED,
    SIM_PHASES,
    Controller,
    load_controller,
    load_registry,
)
from mtdsim.l3_simulation.controller.controller import LEGACY_CSV

REPO_ROOT = Path(__file__).resolve().parents[2]
AGG_NET = REPO_ROOT / "data" / "ogasp" / "petri" / "aggregate_structural.json"

# The 15 tactics the aggregate net carries (full GAP tactic-quotient).
EXPECTED_TACTICS = 15


@pytest.fixture(scope="module")
def registry():
    return load_registry()


@pytest.fixture(scope="module")
def controller() -> Controller:
    """The default selection — experiment 1's mapping."""
    return load_controller()


@pytest.fixture(scope="module")
def v2() -> Controller:
    return load_controller(version="v2_partial")


# --- the registry: mappings are data, selected by name ----------------------


def test_registry_lists_both_versions_and_a_resolvable_default(registry) -> None:
    assert set(registry.names) == {"v1_ckc_total", "v2_partial"}
    assert registry.default in registry.names
    for version in registry.versions:
        assert version.path.is_file()
        assert version.rationale, f"{version.name} carries no rationale"


def test_default_is_the_experiment_1_value(registry, controller: Controller) -> None:
    """An unqualified load must reproduce what has always run.

    The default is deliberately *not* the newest version: promoting the newest to
    default would re-bake an experiment's choice into the pipeline, which is the
    coupling the registry exists to remove.
    """
    assert registry.default == "v1_ckc_total"
    assert controller.version == "v1_ckc_total"


def test_selecting_a_version_is_a_data_selection() -> None:
    """Switching mapping is choosing a name, and the two names differ in effect."""
    a = load_controller(version="v1_ckc_total")
    b = load_controller(version="v2_partial")
    assert a.as_dict() != b.as_dict()
    assert a.version != b.version


def test_unknown_version_raises() -> None:
    with pytest.raises(KeyError):
        load_controller(version="no-such-mapping")


def test_path_and_version_together_are_a_contradiction() -> None:
    with pytest.raises(ValueError):
        load_controller(path=LEGACY_CSV, version="v1_ckc_total")


# --- the relaxed S4 invariant, across every registered version --------------


@pytest.mark.parametrize("name", ["v1_ckc_total", "v2_partial"])
def test_every_tactic_is_mapped_or_declared_dwell_only(name: str) -> None:
    """The invariant that replaced complete coverage.

    A tactic may legally dispatch nothing — but it must *say* so. Mapped rows
    name one of the six verbs; dwell-only rows name none and declare themselves.
    Nothing is silent.
    """
    ctrl = load_controller(version=name)
    assert len(ctrl.rows) == EXPECTED_TACTICS
    for row in ctrl.rows:
        assert row.disposition in {MAPPED, DWELL_ONLY}
        if row.disposition == MAPPED:
            assert row.sim_phase in SIM_PHASES
        else:
            assert row.sim_phase is None
        assert row.reason, f"{name}: {row.tactic} states no reason"


@pytest.mark.parametrize("name", ["v1_ckc_total", "v2_partial"])
def test_map_tactics_match_the_net_places(name: str) -> None:
    """Every version covers precisely the tactic-places the aggregate net has."""
    net = json.loads(AGG_NET.read_text(encoding="utf-8"))
    assert set(load_controller(version=name).tactics) == set(net["places"])


def test_silence_is_still_an_error(tmp_path: Path) -> None:
    """A row with no verb that does not declare itself dwell-only must raise.

    This is the half of the old complete-coverage invariant that survives S4: an
    empty cell is indistinguishable from an unfinished one, so it stays illegal
    even though a *declared* absence is now legal.
    """
    bad = tmp_path / "silent.csv"
    bad.write_text(
        "tactic,sim_phase,disposition,reason\n"
        "reconnaissance,SCAN_HOST,mapped,fine\n"
        "impact,,,\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="does not declare"):
        load_controller(path=bad)


def test_dwell_only_row_may_not_also_name_a_verb(tmp_path: Path) -> None:
    bad = tmp_path / "contradiction.csv"
    bad.write_text(
        "tactic,sim_phase,disposition,reason\n"
        "impact,SCAN_NEIGHBOR,dwell-only,contradicts itself\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="still names a verb"):
        load_controller(path=bad)


def test_unknown_verb_raises(tmp_path: Path) -> None:
    bad = tmp_path / "unknown_verb.csv"
    bad.write_text(
        "tactic,sim_phase,disposition,reason\n"
        "impact,DO_THE_THING,mapped,not a verb\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unknown sim_phase"):
        load_controller(path=bad)


def test_unknown_tactic_raises(controller: Controller) -> None:
    with pytest.raises(KeyError):
        controller.phase_for("not-a-tactic")


# --- version 1: immutable, and unchanged in effect --------------------------


def test_v1_registry_file_matches_the_experiment_1_artefact() -> None:
    """The registry's v1 is a re-expression of ``data/ogasp/controller.csv``.

    Both files are kept — the original because experiment 1's record cites it,
    the registry copy because that is where the loader now reads from — so this
    pins them equal row-for-row and neither can drift.
    """
    with LEGACY_CSV.open(newline="", encoding="utf-8") as fh:
        legacy = {r["tactic"]: r["sim_phase"] for r in csv.DictReader(fh)}
    assert load_controller(version="v1_ckc_total").as_dict() == legacy


def test_v1_dispatch_matches_the_locked_brown_position_map(controller: Controller) -> None:
    """Experiment 1's mapping is frozen; guard against silent drift."""
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


def test_v1_is_total_no_dwell_only_tactics(controller: Controller) -> None:
    """Version 1 predates S4: it maps everything, which is still legal."""
    assert controller.dwell_only_tactics == ()
    assert len(controller.mapped_tactics) == EXPECTED_TACTICS


# --- version 2: the ratified partial mapping --------------------------------


def test_v2_is_partial_eight_mapped_seven_dwell_only(v2: Controller) -> None:
    assert len(v2.mapped_tactics) == 8
    assert set(v2.dwell_only_tactics) == {
        "resource-development",
        "persistence",
        "stealth",
        "defense-impairment",
        "collection",
        "exfiltration",
        "impact",
    }


def test_v2_dispatch_matches_the_ratified_map(v2: Controller) -> None:
    """The ratified value (controller_mapping_v2.md §2); guard against drift."""
    m = v2.as_dict()
    assert m["reconnaissance"] == "SCAN_HOST"
    assert m["initial-access"] == "EXPLOIT_VULN"  # not the port scan (v1's worst cell)
    assert m["execution"] == "EXPLOIT_VULN"
    assert m["privilege-escalation"] == "EXPLOIT_VULN"
    assert m["credential-access"] == "BRUTE_FORCE"
    assert m["discovery"] == "SCAN_PORT"
    assert m["lateral-movement"] == "ENUM_HOST"
    assert m["command-and-control"] == "SCAN_NEIGHBOR"
    for dwell_only in v2.dwell_only_tactics:
        assert m[dwell_only] is None


def test_v2_spread_pair_is_reachable(v2: Controller) -> None:
    """The substrate spreads by a neighbour-reveal *followed by* an enumeration.

    Experiment 1 fired the first without the second and never pivoted, so the two
    verbs sitting on distinct tactics is the point of this version rather than an
    accident of it.
    """
    assert v2.phase_for("command-and-control") == "SCAN_NEIGHBOR"
    assert v2.phase_for("lateral-movement") == "ENUM_HOST"


@pytest.mark.parametrize("name", ["v1_ckc_total", "v2_partial"])
def test_all_six_verbs_stay_reachable(name: str) -> None:
    """No version leaves a verb dead — a dead verb is an unexercised substrate
    path, and a comparison across versions would be measuring its absence."""
    ctrl = load_controller(version=name)
    assert set(ctrl.dispatch_map().values()) == set(SIM_PHASES)
