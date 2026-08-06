"""Timeline runner — validation gate.

Covers the timeline-runner handoff gate: determinism (same seed + cell →
byte-identical timeline, SIM-05 extended to the runner); no-synthesis at run
time (every fired transition exists in the committed net JSON); declared
termination (objective / cap / stalled, cap enforced); the sweep arithmetic
in group-anchor units; D8 entries with the recon-arm impossibility recorded
as a result; and the committed contract artefacts (schema doc, example,
behavioural report).

Conventions follow ``test_durations.py``: committed JSONs loaded as plain
JSON, repo-root ``conftest.py`` supplies ``src/`` on the path.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mtdsim.l3_simulation.timeline.matrix import (
    Cell,
    build_matrix,
    generate_cell,
    seed_for,
)
from mtdsim.l3_simulation.timeline.report import (
    EXAMPLE_PATH,
    REPORT_JSON,
    REPORT_MD,
)
from mtdsim.l3_simulation.timeline.walk import (
    AGGREGATE,
    DURATION_VARIANTS,
    MAX_STEPS,
    PETRI_DIR,
    PROFILE_NAMES,
    SCHEMA_VERSION,
    TIMELINE_DIR,
    dwell_table,
    load_catalogue,
    load_net,
    serialise,
)

SCHEMA_DOC = Path(TIMELINE_DIR) / "timeline_schema.md"

OUTCOMES = {"objective", "cap", "stalled"}

REQUIRED_RECORD_FIELDS = (
    "schema",
    "run_id",
    "seed",
    "profile",
    "entry",
    "policy",
    "weight_variant",
    "duration_variant",
    "objective_rule",
    "objective_tactics",
    "outcome",
    "stall_reason",
    "completed_objectives",
    "objective_first_visit_s",
    "net_time_to_objective_s",
    "n_states",
    "total_duration_s",
    "sequence",
)

N_SMALL = 10  # runs per cell for the on-the-fly property library


@pytest.fixture(scope="module")
def catalogue():
    return load_catalogue()


@pytest.fixture(scope="module")
def nets():
    return {profile: load_net(profile) for profile in PROFILE_NAMES}


@pytest.fixture(scope="module")
def matrix(nets):
    return build_matrix(nets)


@pytest.fixture(scope="module")
def small_library(nets, catalogue, matrix):
    """The full matrix at N_SMALL runs per cell — regenerated, not read from
    the gitignored bulk outputs, so the gate holds on a fresh clone."""
    cells, _ = matrix
    return {
        cell: generate_cell(nets[cell.profile], catalogue, cell, N_SMALL)
        for cell in cells
    }


@pytest.fixture(scope="module")
def committed_transitions():
    """Per profile: transition name -> (src, dst) from the committed JSONs."""
    index = {}
    for profile in PROFILE_NAMES:
        with open(Path(PETRI_DIR) / f"{profile}_structural.json") as f:
            data = json.load(f)
        index[profile] = {
            t["name"]: (t["src_tactic"], t["dst_tactic"]) for t in data["transitions"]
        }
    return index


# 1. Determinism — same seed + profile + entry + policy + duration variant
#    → byte-identical timeline (SIM-05 discipline extended to the runner)

def test_determinism_byte_identical(nets, catalogue):
    for cell in (
        Cell("objective_exfiltration", "initial-access", "weighted", "operator_dedup", "central"),
        Cell("aggregate", "reconnaissance", "uniform", None, "sweep_low"),
        Cell("objective_exfiltration_impact", "initial-access", "weighted", "raw", "sweep_high"),
    ):
        first = generate_cell(nets[cell.profile], catalogue, cell, N_SMALL)
        second = generate_cell(nets[cell.profile], catalogue, cell, N_SMALL)
        assert [serialise(r) for r in first] == [serialise(r) for r in second], cell


def test_seed_derivation_locked():
    # the derivation is part of the v1 contract — a change here is a schema bump
    #
    # The pinned value moved once, in the 2026-08-06 objective-tactic rename,
    # because seeds are content-addressed on the run id and the run id embeds
    # the profile name: renaming ``pure_steal`` re-pointed this input string
    # and so re-seeded the whole timeline library. The *derivation* is
    # untouched — a failure here still means the algorithm changed.
    assert (
        seed_for("objective_exfiltration--initial-access--weighted-operator_dedup--central--000")
        == 14057210806463591956
    )


# 2. No-synthesis at run time — every fired transition exists in the
#    committed net JSON and connects the recorded states

def test_no_synthesis_and_sequence_consistency(small_library, committed_transitions):
    for cell, records in small_library.items():
        names = committed_transitions[cell.profile]
        for record in records:
            sequence = record["sequence"]
            assert sequence[0]["transition_fired"] is None
            assert sequence[0]["t_enter_s"] == 0.0
            for prev, state in zip(sequence, sequence[1:]):
                fired = state["transition_fired"]
                assert fired in names, (cell, fired)
                src, dst = names[fired]
                assert src == prev["tactic"], (cell, fired)
                assert dst == state["tactic"], (cell, fired)
            for state in sequence:
                assert state["t_exit_s"] == pytest.approx(
                    state["t_enter_s"] + state["dwell_s"]
                )
            for prev, state in zip(sequence, sequence[1:]):
                assert state["t_enter_s"] == pytest.approx(prev["t_exit_s"])


def test_weighted_policy_fires_only_supported(small_library, nets):
    for cell, records in small_library.items():
        if cell.policy != "weighted":
            continue
        weights = {
            t.name: (t.weights[cell.weight_variant]["weight"] or 0)
            for t in nets[cell.profile].transitions
        }
        for record in records:
            for state in record["sequence"][1:]:
                assert weights[state["transition_fired"]] > 0, cell


# 3. Termination — every run ends in a declared outcome; cap enforced

def test_termination_declared(small_library):
    for cell, records in small_library.items():
        for record in records:
            assert record["outcome"] in OUTCOMES, cell
            assert record["n_states"] <= MAX_STEPS, cell
            assert (record["stall_reason"] is not None) == (
                record["outcome"] == "stalled"
            ), cell
            if record["outcome"] == "objective":
                assert record["net_time_to_objective_s"] == pytest.approx(
                    record["total_duration_s"]
                )
                objectives = set(record["objective_tactics"])
                completed = set(record["completed_objectives"])
                if record["objective_rule"] == "all":
                    assert completed == objectives, cell
                else:
                    assert completed and completed <= objectives, cell
            else:
                assert record["net_time_to_objective_s"] is None, cell


# 4. The sweep arithmetic — extremes in group-anchor units, never
#    duration_s × bound (the handoff's worked example)

def test_sweep_arithmetic_anchor_units(catalogue):
    central = dwell_table(catalogue, "central")
    low = dwell_table(catalogue, "sweep_low")
    high = dwell_table(catalogue, "sweep_high")
    assert central["execution"] == pytest.approx(22.5)
    assert low["execution"] == pytest.approx(4.5)   # 45 × 0.1, not 22.5 × 0.1
    assert high["execution"] == pytest.approx(90.0)  # 45 × 2.0
    for variant in (central, low, high):
        assert variant["resource-development"] == 0.0
        assert all(d >= 0 for d in variant.values())
    assert set(central) == set(low) == set(high)


# 5. D8 entries — initial-access always; recon only where bridged; the
#    islanded classes' recon arm recorded as a result, not silently skipped

def test_matrix_entries_and_recon_impossibility(matrix, nets):
    cells, impossible = matrix
    by_profile = {}
    for cell in cells:
        by_profile.setdefault(cell.profile, set()).add(cell.entry)
    for profile in PROFILE_NAMES:
        assert "initial-access" in by_profile[profile]
        assert ("reconnaissance" in by_profile[profile]) == nets[profile].recon_bridged
    assert {arm["profile"] for arm in impossible} == {
        "objective_exfiltration_impact",
        "objective_none_c2",
    }
    for arm in impossible:
        assert arm["status"] == "impossible"
        assert arm["entry"] == "reconnaissance"
        assert arm["reason"].strip()


def test_objective_rules(nets):
    for profile in PROFILE_NAMES:
        expected = "any" if profile == AGGREGATE else "all"
        assert nets[profile].objective_rule == expected


# 6. The committed contract artefacts — schema doc, example, report

def test_schema_doc_committed():
    text = SCHEMA_DOC.read_text()
    assert SCHEMA_VERSION in text
    assert "net\n  time-to-objective" in text or "net time-to-objective" in text
    assert "anchors[group].duration_s × sweep_bound" in text


def test_committed_example(committed_transitions):
    lines = EXAMPLE_PATH.read_text().splitlines()
    assert 1 <= len(lines) <= 3
    for line in lines:
        record = json.loads(line)
        assert record["schema"] == SCHEMA_VERSION
        for field in REQUIRED_RECORD_FIELDS:
            assert field in record, field
        names = committed_transitions[record["profile"]]
        for state in record["sequence"][1:]:
            assert state["transition_fired"] in names


def test_behavioural_report_committed():
    assert REPORT_MD.exists()
    report = json.loads(REPORT_JSON.read_text())
    for key in (
        "cell_stats",
        "orderings_by_median_net_time_to_objective",
        "ordering_stable_across_sweep_extremes",
        "impossible_arms",
    ):
        assert key in report
    # gate: recon-arm impossibility is recorded as a result in the report
    assert {arm["profile"] for arm in report["impossible_arms"]} == {
        "objective_exfiltration_impact",
        "objective_none_c2",
    }
    text = REPORT_MD.read_text()
    assert "net time-to-objective" in text
    assert "MTTC" in text  # the not-the-DES-MTTC discipline is stated
    # class-vs-aggregate comparison (the behavioural half) is present
    assert "Class vs aggregate" in text
    assert "## Verdict" in text


# 7. The runner never touches MTDSim

def test_runner_never_imports_mtdnetwork():
    import ast

    package_dir = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "mtdsim"
        / "l3_simulation"
        / "timeline"
    )
    for path in package_dir.glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                assert not name.startswith("mtdnetwork"), (path.name, name)
