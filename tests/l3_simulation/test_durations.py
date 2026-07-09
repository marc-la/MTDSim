"""L3 state-duration catalogue — validation gate.

Covers the state-durations handoff gate: the catalogue's key set equals the
``data/ogasp/`` place-union (mechanical, from the committed structural JSONs);
every entry carries group + tier + source + justification + sweep_range; no
value derives from ``observation_count`` or any corpus frequency; Tier-1
tactics trace to a substrate constant and are flagged not-tuned; tuned tactics
name their group anchor; units are sane against ``ATTACK_DURATION`` magnitudes
and the anchor arithmetic is internally consistent.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mtdnetwork.data import constants
from mtdsim.l2_subgraph.schema import CLASS_NAMES
from mtdsim.l3_simulation.petri.build import AGGREGATE
from mtdsim.l3_simulation.petri.render import OGASP_DIR

CATALOGUE_PATH = Path(OGASP_DIR) / "tactic_durations.json"

REQUIRED_ENTRY_FIELDS = (
    "attack_tactic_id",
    "group",
    "anchor",
    "relative_multiplier",
    "duration_s",
    "tier",
    "not_tuned",
    "sweep_range",
    "source",
    "justification",
)

# Locked expectations — must agree with the profiles' §5 blocks and
# dissertation.tex §3.1 Table 3.2 (group, multiplier, tier). The profiles
# stay the single source of truth; a mismatch here means fixing catalogue
# and thesis table in the same commit, not editing this table first.
EXPECTED = {
    # tactic: (group, relative_multiplier, tier)
    "reconnaissance": ("scan-shaped", 1.0, 1),
    "resource-development": ("prep-off-network", 0.0, 3),
    "initial-access": ("exploit-shaped", 1.0, 1),
    "execution": ("stealth-low-and-slow", 0.5, 3),
    "persistence": ("stealth-low-and-slow", 1.0, 3),
    "privilege-escalation": ("exploit-shaped", 1.0, 1),
    "stealth": ("stealth-low-and-slow", 1.0, 3),
    "defense-impairment": ("stealth-low-and-slow", 0.5, 3),
    "credential-access": ("exploit-shaped", 1.0, 1),
    "discovery": ("scan-shaped", 1.0, 1),
    "lateral-movement": ("exploit-shaped", 1.0, 1),
    "collection": ("objective-execution", 1.0, 2),
    "command-and-control": ("stealth-low-and-slow", 1.0, 3),
    "exfiltration": ("objective-execution", 1.0, 2),
    "impact": ("objective-execution", 1.0, 2),
}


@pytest.fixture(scope="module")
def catalogue():
    with open(CATALOGUE_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def raw_text():
    return CATALOGUE_PATH.read_text()


@pytest.fixture(scope="module")
def place_union():
    union = set()
    for profile in (*CLASS_NAMES, AGGREGATE):
        with open(Path(OGASP_DIR) / f"{profile}_structural.json") as f:
            union.update(json.load(f)["places"])
    return union


# 1. Key set == the data/ogasp/ place-union (mechanical)

def test_key_set_matches_place_union(catalogue, place_union):
    assert set(catalogue["tactics"]) == place_union


# 2. Every entry is complete

def test_every_entry_complete(catalogue):
    for tactic, entry in catalogue["tactics"].items():
        for field in REQUIRED_ENTRY_FIELDS:
            assert field in entry, f"{tactic}: missing {field}"
        assert entry["source"].strip(), tactic
        assert entry["justification"].strip(), tactic
        lo, hi = entry["sweep_range"]
        assert lo <= entry["relative_multiplier"] <= hi, tactic


def test_locked_assignments(catalogue):
    for tactic, (group, mult, tier) in EXPECTED.items():
        entry = catalogue["tactics"][tactic]
        assert entry["group"] == group, tactic
        assert entry["relative_multiplier"] == mult, tactic
        assert entry["tier"] == tier, tactic


# 3. No value derives from the corpus (observation_count / flow frequency)

def test_no_corpus_timing(raw_text):
    assert "observation_count" not in raw_text
    assert "flow_proportion" not in raw_text


# 4. Tier-1 traces to a substrate constant, not tuned; tuned tactics
#    name a declared group anchor

def test_tier1_substrate_anchored(catalogue):
    for tactic, entry in catalogue["tactics"].items():
        if entry["tier"] == 1:
            assert entry["not_tuned"] is True, tactic
            assert (
                "ATTACK_DURATION" in entry["source"]
                or "exploit_time" in entry["source"]
            ), tactic
        else:
            assert entry["not_tuned"] is False, tactic


def test_tuned_tactics_name_their_anchor(catalogue):
    anchors = catalogue["anchors"]
    for tactic, entry in catalogue["tactics"].items():
        anchor = anchors[entry["anchor"]]
        assert entry["group"] == entry["anchor"], tactic
        if entry["tier"] in (2, 3) and entry["duration_s"] > 0:
            assert "declared" in anchor["status"], tactic


# 5. Anchor arithmetic + units sane vs ATTACK_DURATION magnitudes

def test_anchor_arithmetic(catalogue):
    anchors = catalogue["anchors"]
    for tactic, entry in catalogue["tactics"].items():
        expected = entry["relative_multiplier"] * anchors[entry["anchor"]]["duration_s"]
        assert entry["duration_s"] == pytest.approx(expected), tactic


def test_tier1_anchor_values_trace_to_constants(catalogue):
    anchors = catalogue["anchors"]
    scan_pass = (
        constants.ATTACK_DURATION["SCAN_HOST"]
        + constants.ATTACK_DURATION["SCAN_NEIGHBOR"]
        + constants.ATTACK_DURATION["SCAN_PORT"]
    )
    assert anchors["scan-shaped"]["duration_s"] == scan_pass
    median_complexity = (constants.VULN_MIN_COMPLEXITY + 1) / 2
    exploit_median = constants.ATTACK_DURATION["EXPLOIT_VULN"] * (1 - median_complexity)
    assert anchors["exploit-shaped"]["duration_s"] == pytest.approx(exploit_median)


def test_magnitudes_sane(catalogue):
    max_verb = max(constants.ATTACK_DURATION.values())
    trigger_mean = min(m for m, _ in constants.MTD_TRIGGER_INTERVAL.values())
    for tactic, entry in catalogue["tactics"].items():
        d = entry["duration_s"]
        assert d >= 0, tactic
        if d > 0:
            # same order of magnitude as the substrate's priced verbs, and
            # central dwells stay below the MTD trigger-interval mean so the
            # interval-vs-dwell ratio contest is live, not degenerate
            assert d <= 4 * max_verb, tactic
            assert d < trigger_mean, tactic
