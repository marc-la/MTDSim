"""Loader tests — schema enforcement, indexing, snapshot precompute."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mtdsim.viz.replay.log import EventLog, UnsupportedSchemaVersion


FIXTURE = Path(__file__).parent / "fixtures" / "mini_events.jsonl"


def test_load_parses_all_events_in_order():
    log = EventLog.load(FIXTURE)
    assert len(log.events) == 7
    assert log.events[0]["type"] == "sim_started"
    assert log.events[-1]["type"] == "sim_ended"
    assert log.event_ts == [0.0, 10.0, 50.0, 120.0, 230.0, 400.0, 500.0]
    assert log.t_min == 0.0
    assert log.t_max == 500.0


def test_hosts_and_techniques_indexed():
    log = EventLog.load(FIXTURE)
    assert log.hosts_seen == {1, 2, 3}
    assert log.techniques_seen == {"T1016", "T1190", "T1110"}


def test_index_at_time_is_last_event_not_after():
    log = EventLog.load(FIXTURE)
    assert log.index_at_time(-1.0) == -1
    assert log.index_at_time(0.0) == 0
    assert log.index_at_time(9.9) == 0
    assert log.index_at_time(10.0) == 1
    assert log.index_at_time(119.0) == 2
    assert log.index_at_time(500.0) == 6
    assert log.index_at_time(9999.0) == 6


def test_snapshots_every_100s_accumulate_host_states():
    log = EventLog.load(FIXTURE, snapshot_every=100.0)
    assert [s.t for s in log.snapshots] == [0.0, 100.0, 200.0, 300.0, 400.0, 500.0]

    by_t = {s.t: s for s in log.snapshots}
    assert by_t[0.0].host_states == {}
    assert by_t[100.0].host_states == {1: "targeted", 2: "targeted"}
    assert by_t[200.0].host_states == {1: "targeted", 2: "compromised"}
    assert by_t[300.0].host_states == {1: "targeted", 2: "compromised", 3: "targeted"}
    assert by_t[400.0].host_states == {1: "targeted", 2: "compromised", 3: "compromised"}


def test_snapshots_ignore_global_host_id_null_and_negative():
    log = EventLog.load(FIXTURE)
    final = log.snapshots[-1].host_states
    assert all(isinstance(h, int) and h >= 0 for h in final)


def test_load_rejects_missing_schema_version(tmp_path: Path):
    bad = tmp_path / "bad.jsonl"
    bad.write_text(json.dumps({
        "t": 0.0, "type": "sim_started", "host_id": None,
        "phase": None, "technique_id": None, "tactic": None, "meta": {}
    }) + "\n")
    with pytest.raises(UnsupportedSchemaVersion):
        EventLog.load(bad)


def test_load_rejects_unknown_schema_version(tmp_path: Path):
    bad = tmp_path / "bad.jsonl"
    bad.write_text(json.dumps({
        "schema_version": "99.0",
        "t": 0.0, "type": "sim_started", "host_id": None,
        "phase": None, "technique_id": None, "tactic": None, "meta": {}
    }) + "\n")
    with pytest.raises(UnsupportedSchemaVersion):
        EventLog.load(bad)


def test_load_skips_blank_lines(tmp_path: Path):
    p = tmp_path / "mini.jsonl"
    lines = FIXTURE.read_text().splitlines()
    p.write_text(lines[0] + "\n\n" + lines[1] + "\n")
    log = EventLog.load(p)
    assert len(log.events) == 2


def test_load_empty_file_is_not_an_error(tmp_path: Path):
    p = tmp_path / "empty.jsonl"
    p.write_text("")
    log = EventLog.load(p)
    assert log.events == []
    assert log.t_max == 0.0
    assert log.snapshots == []
    assert log.index_at_time(0.0) == -1


def test_sim_started_meta_and_topology_extracted():
    log = EventLog.load(FIXTURE)
    assert log.sim_meta["profile"] == "test"
    assert log.sim_meta["scheme"] == "no_mtd"
    assert log.topology is not None
    assert len(log.topology["nodes"]) == 5
    assert [e for e in log.topology["edges"] if 0 in e]
