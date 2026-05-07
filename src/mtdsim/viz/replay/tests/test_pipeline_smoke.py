"""End-to-end pipeline smoke test (§2).

Trivial-profile flow: GAP -> SubgraphView -> 6-phase mapping ->
SubgraphAttackerProfile -> sim run -> events.jsonl -> EventLog.load ->
network figure.

Skipped wholesale on machines without the GAP snapshot. The sim-run
section is gated behind ``MTDSIM_RUN_SMOKE_SIM=1`` so the default test
suite stays fast; run it explicitly when validating a release.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from mtdsim.attacker.profile_generator import PHASES, TACTIC_TO_PHASE
from mtdsim.attacker.subgraph_profile import (
    SubgraphAttackerProfile,
    is_subgraph_profile,
)
from mtdsim.viz.replay.fixtures import (
    TRIVIAL_SELECTOR_TAG,
    trivial_profile,
    trivial_profile_payload,
    trivial_subgraph_view,
)
from mtdsim.viz.replay.gap_source import resolve_gap_json, load_gap


def _gap_available() -> bool:
    return resolve_gap_json().exists()


pytestmark = pytest.mark.skipif(
    not _gap_available(),
    reason="GAP snapshot missing — run the GAP build notebook first.",
)


@pytest.fixture(scope="module")
def gap():
    return load_gap()


def test_trivial_subgraph_view_resolves_non_empty(gap):
    view = trivial_subgraph_view(gap)
    assert view.node_set, "trivial selector must resolve to a non-empty subgraph"


def test_every_subgraph_node_maps_to_a_simulator_phase(gap):
    view = trivial_subgraph_view(gap)
    unmapped = []
    for tid in view.node_set:
        node = gap.nodes.get(tid)
        if node is None:
            continue
        if TACTIC_TO_PHASE.get(node.primary_tactic) is None:
            unmapped.append((tid, node.primary_tactic))
    # The TACTIC_TO_PHASE dict covers every ATT&CK tactic, so this should
    # always be empty. If it isn't, the GAP has introduced a tactic the
    # simulator doesn't know about and the pipeline silently drops nodes.
    assert not unmapped, f"techniques with no phase mapping: {unmapped[:5]}"


def test_subgraph_attacker_profile_constructs(gap):
    prof = trivial_profile(gap)
    assert is_subgraph_profile(prof)
    assert prof.selector_tag == TRIVIAL_SELECTOR_TAG
    # Delegation to base profile must still work.
    assert prof.exploit_success_bonus == 0.0
    assert prof.brute_force_multiplier == 1.0
    # At least one of the six phases must have a sampleable technique,
    # otherwise the simulator will fall back to legacy behaviour for the
    # whole run and we haven't actually exercised the subgraph path.
    sampled = [p for p in PHASES if prof.sample_technique(p, executed=set())]
    assert sampled, "no phase has a sampleable technique under trivial profile"


def test_serialised_payload_round_trip(gap):
    payload = trivial_profile_payload(gap)
    assert payload["mode"] == "terminal_tactic"
    assert payload["node_set"]
    # Edge tuples serialise as 2-lists for JSON.
    assert all(isinstance(e, list) and len(e) == 2 for e in payload["edge_set"])


@pytest.mark.skipif(
    os.environ.get("MTDSIM_RUN_SMOKE_SIM") != "1",
    reason="Set MTDSIM_RUN_SMOKE_SIM=1 to run the (slower) sim leg.",
)
def test_full_pipeline_produces_loadable_log(gap, tmp_path: Path):
    """The slow leg: actually run a (DEMO) sim and load its log back."""
    from mtdsim.viz.replay.config import DEMO
    from mtdsim.viz.replay.log import EventLog
    from mtdsim.viz.replay.panels.network import build_network_figure
    from mtdsim.viz.replay.runner import run_canonical_sim

    profile = trivial_profile(gap)
    log_path = run_canonical_sim(
        DEMO, scheme="random", profile=profile, events_dir=tmp_path, force=True
    )
    assert log_path.exists() and log_path.stat().st_size > 0

    log = EventLog.load(log_path)
    assert log.events, "log must have at least one event"
    assert log.topology is not None, "sim_started.meta.topology missing"

    fig = build_network_figure(
        topology=log.topology, events=log.events, event_index=-1
    )
    assert fig.data, "network figure must have at least one trace"
