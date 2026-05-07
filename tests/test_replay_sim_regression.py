"""Regression test for the MTD CM "techniques run forever after ~6000s" bug.

Before the P1 fix, PRIMARY/random/seed=42 hit TimeNetwork.is_compromised at
~t=6087s and the trigger loop kept spawning MTDs that bailed out of
_mtd_execute_action without emitting mtd_completed, leaving 9 ks of orphan
mtd_deployed events. After the fix, the trace is balanced and the sim
terminates either via end_event or finish_time with no orphans.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from mtdsim.stats.event_log import EventLogger
from mtdsim.stats.event_log_validator import validate_event_log
from mtdsim.viz.replay.config import PRIMARY
from mtdsim.viz.replay.runner import run_canonical_sim


@pytest.fixture
def primary_random_log(tmp_path: Path) -> list[dict]:
    out_path = run_canonical_sim(PRIMARY, scheme="random", events_dir=tmp_path, force=True)
    return EventLogger.load_jsonl(str(out_path))


def test_event_log_is_well_formed(primary_random_log):
    """Every mtd_deployed pairs with mtd_completed or mtd_aborted."""
    issues = validate_event_log(primary_random_log)
    assert issues == [], f"event log has invariants violations: {issues}"


def test_no_orphan_mtd_deploys(primary_random_log):
    """Direct check on the bug we hit: orphan mtd_deployed events."""
    deployed = sum(1 for e in primary_random_log if e["type"] == "mtd_deployed")
    completed = sum(1 for e in primary_random_log if e["type"] == "mtd_completed")
    aborted = sum(1 for e in primary_random_log if e["type"] == "mtd_aborted")
    assert deployed == completed + aborted, (
        f"orphan deploys: deployed={deployed} completed={completed} aborted={aborted}"
    )


def test_sim_terminates_within_horizon(primary_random_log):
    """Sim ends at t<=finish_time, terminated by either end_event or finish_time."""
    sim_ended = primary_random_log[-1]
    assert sim_ended["type"] == "sim_ended"
    assert sim_ended["t"] <= PRIMARY.finish_time
    assert sim_ended["meta"]["terminated_by"] in {"end_event", "finish_time"}


def test_terminate_compromise_ratio_is_honored():
    """TimeNetwork should respect the threshold the caller passes."""
    from mtdsim.network.time_network import TimeNetwork

    net = TimeNetwork(total_nodes=100, total_endpoints=5, total_subnets=8,
                      total_layers=4, total_database=2,
                      terminate_compromise_ratio=0.8)
    assert not net.is_compromised(list(range(25)))   # 25% — below the new 0.8
    assert not net.is_compromised(list(range(80)))   # exactly at threshold (>, not >=)
    assert net.is_compromised(list(range(81)))       # above threshold
