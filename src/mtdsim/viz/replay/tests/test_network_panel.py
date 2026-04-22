"""Network-panel smoke tests: state derivation + figure traces."""

from __future__ import annotations

from pathlib import Path

from mtdsim.viz.replay.log import EventLog
from mtdsim.viz.replay.panels.network import (
    _cumulative_host_states,
    build_network_figure,
    empty_figure,
)


FIXTURE = Path(__file__).parent / "fixtures" / "mini_events.jsonl"


def test_cumulative_host_states_evolve_with_event_index():
    log = EventLog.load(FIXTURE)
    assert _cumulative_host_states(log.events, event_index=-1) == {}
    assert _cumulative_host_states(log.events, event_index=1) == {1: "targeted"}
    assert _cumulative_host_states(log.events, event_index=3) == {1: "targeted", 2: "compromised"}
    assert _cumulative_host_states(log.events, event_index=5) == {
        1: "targeted",
        2: "compromised",
        3: "compromised",
    }


def test_build_network_figure_returns_edge_plus_three_state_traces():
    log = EventLog.load(FIXTURE)
    fig = build_network_figure(
        topology=log.topology,
        events=log.events,
        event_index=-1,
    )
    assert len(fig.data) == 4
    marker_names = [t.name for t in fig.data if t.mode == "markers"]
    assert marker_names == ["untouched", "targeted", "compromised"]


def test_empty_figure_is_returned_when_topology_missing():
    fig = build_network_figure(topology=None, events=[], event_index=-1)
    assert len(fig.data) == 0
    assert fig.layout.annotations


def test_scrubbing_back_returns_nodes_to_untouched():
    log = EventLog.load(FIXTURE)
    fig_end = build_network_figure(
        topology=log.topology, events=log.events, event_index=len(log.events) - 1
    )
    untouched_end = next(t for t in fig_end.data if t.name == "untouched").x
    fig_start = build_network_figure(
        topology=log.topology, events=log.events, event_index=-1
    )
    untouched_start = next(t for t in fig_start.data if t.name == "untouched").x
    assert len(untouched_start) == 5
    assert len(untouched_end) < len(untouched_start)
