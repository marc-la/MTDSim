"""L3a structural Petri nets — validation gate.

Covers the handoff's gate: the four nets build with the locked place /
transition / edge counts; the **no-synthesis invariant** holds mechanically
(every transition traces to >=1 real GASP edge; nothing invented; no
inter-tactic edge silently dropped); the build is deterministic; the single
black token is seeded correctly; the reachability / objective / prefix-gap
report is emitted and matches the inspect-the-base finding.
"""

from __future__ import annotations

import pytest

from mtdsim.l2_subgraph.schema import CLASS_NAMES
from mtdsim.l3_simulation.petri.analysis import OBJECTIVE_TACTICS, analyse
from mtdsim.l3_simulation.petri.build import (
    BLACK_TOKEN,
    GapIndex,
    StructuralNet,
    build_all,
    build_structural_net,
    load_gap_index,
    load_gasp_view,
)

# Locked expectations from the handoff component-mapping table.
EXPECTED_PLACES = {
    "pure_steal": 15,
    "pure_impediment": 14,
    "double_extortion": 14,
    "infrastructure_setup": 13,
}
EXPECTED_TRANSITIONS = {  # inter-tactic tactic-pairs
    "pure_steal": 109,
    "pure_impediment": 83,
    "double_extortion": 72,
    "infrastructure_setup": 57,
}
EXPECTED_INTER_TACTIC_EDGES = {
    "pure_steal": 363,
    "pure_impediment": 225,
    "double_extortion": 201,
    "infrastructure_setup": 136,
}
EXPECTED_SELFLOOPS_DROPPED = {
    "pure_steal": 50,
    "pure_impediment": 29,
    "double_extortion": 24,
    "infrastructure_setup": 12,
}
# The recon -> initial-access prefix gap, per the inspect-the-base finding:
# bridged (a single direct edge) in two classes, an island in the other two.
EXPECTED_RECON_REACHES_IA = {
    "pure_steal": True,
    "pure_impediment": True,
    "double_extortion": False,
    "infrastructure_setup": False,
}


@pytest.fixture(scope="module")
def gap() -> GapIndex:
    return load_gap_index()


@pytest.fixture(scope="module")
def nets(gap) -> dict[str, StructuralNet]:
    return build_all()


# ---------------------------------------------------------------------------
# 1. Counts — places, transitions, inter-tactic edges, dropped self-loops
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_place_count(nets, cls):
    assert len(nets[cls].tactics) == EXPECTED_PLACES[cls]
    # SNAKES net agrees with the spec metadata.
    assert len(list(nets[cls].net.place())) == EXPECTED_PLACES[cls]


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_transition_count(nets, cls):
    assert len(nets[cls].transitions) == EXPECTED_TRANSITIONS[cls]
    assert len(list(nets[cls].net.transition())) == EXPECTED_TRANSITIONS[cls]


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_inter_tactic_edge_and_selfloop_counts(nets, cls):
    snet = nets[cls]
    assert sum(len(t.edges) for t in snet.transitions) == EXPECTED_INTER_TACTIC_EDGES[cls]
    assert snet.selfloops_dropped == EXPECTED_SELFLOOPS_DROPPED[cls]


# ---------------------------------------------------------------------------
# 2. No-synthesis invariant (the load-bearing mechanical test)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_no_synthesis_invariant(nets, gap, cls):
    snet = nets[cls]
    view = load_gasp_view(cls)
    tactic_of = gap.tactic_of
    edge_set = set(view.edge_set)
    place_set = set(snet.tactics)

    # (a) No place is invented: every place is a tactic over the class node_set.
    node_tactics = {tactic_of[t] for t in view.node_set}
    assert place_set == node_tactics

    covered: set[tuple[str, str]] = set()
    for spec in snet.transitions:
        # (b) Every transition traces to >=1 GASP edge.
        assert spec.edges, f"{cls}:{spec.name} has no GASP provenance edge"
        # (c) The transition is not invented: its tactics are real places and
        #     it is genuinely inter-tactic.
        assert spec.src_tactic in place_set and spec.dst_tactic in place_set
        assert spec.src_tactic != spec.dst_tactic
        assert spec.name == f"{spec.src_tactic}__to__{spec.dst_tactic}"
        for u, v in spec.edges:
            # (d) Every provenance edge is a real GASP edge in this class...
            assert (u, v) in edge_set, f"{cls}: {(u, v)} not in class edge_set"
            # ...and it actually routes this tactic-pair.
            assert tactic_of[u] == spec.src_tactic
            assert tactic_of[v] == spec.dst_tactic
            covered.add((u, v))

    # (e) Completeness: every inter-tactic GASP edge is covered exactly once
    #     (no edge silently dropped); intra-tactic edges are the only omissions.
    inter_tactic = {
        (u, v) for (u, v) in edge_set if tactic_of[u] != tactic_of[v]
    }
    intra_tactic = {
        (u, v) for (u, v) in edge_set if tactic_of[u] == tactic_of[v]
    }
    assert covered == inter_tactic
    total_prov = sum(len(t.edges) for t in snet.transitions)
    assert total_prov == len(inter_tactic)  # exactly once -> no double-count
    assert len(intra_tactic) == EXPECTED_SELFLOOPS_DROPPED[cls]


# ---------------------------------------------------------------------------
# 3. SNAKES net structure — bipartite, one input + one output arc each
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_net_is_bipartite_single_arc_each(nets, cls):
    snet = nets[cls]
    net = snet.net
    for spec in snet.transitions:
        trans = net.transition(spec.name)
        inputs = list(trans.input())
        outputs = list(trans.output())
        # Exactly one input place (src) and one output place (dst).
        assert len(inputs) == 1 and len(outputs) == 1
        assert inputs[0][0].name == spec.src_tactic
        assert outputs[0][0].name == spec.dst_tactic


# ---------------------------------------------------------------------------
# 4. Marking — exactly one black token, in reconnaissance (all four classes)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_single_black_token_in_reconnaissance(nets, cls):
    snet = nets[cls]
    assert snet.entry_tactic == "reconnaissance"
    marking = snet.net.get_marking()
    # Exactly one marked place, holding exactly one token.
    marked = {p: m for p, m in marking.items()}
    assert list(marked) == ["reconnaissance"]
    tokens = list(marked["reconnaissance"])
    assert tokens == [BLACK_TOKEN]


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_token_moves_on_fire(nets, cls):
    """Firing an enabled transition moves the single token (path traversal)."""
    snet = nets[cls]
    # reconnaissance is a sink in two classes; fire from a place that has an
    # outgoing transition instead, to exercise the moving-token semantics.
    spec = snet.transitions[0]
    net = build_structural_net(load_gasp_view(cls), load_gap_index()).net
    # Seed the source place and fire.
    src = net.place(spec.src_tactic)
    src.reset([BLACK_TOKEN])
    for other in net.place():
        if other.name != spec.src_tactic:
            other.reset([])
    trans = net.transition(spec.name)
    modes = trans.modes()
    assert modes, f"{cls}:{spec.name} not enabled with token in {spec.src_tactic}"
    trans.fire(modes[0])
    marking = net.get_marking()
    assert list(marking) == [spec.dst_tactic]


# ---------------------------------------------------------------------------
# 5. Determinism — same inputs -> identical net
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_deterministic_build(cls):
    a = build_structural_net(load_gasp_view(cls), load_gap_index())
    b = build_structural_net(load_gasp_view(cls), load_gap_index())
    assert a.tactics == b.tactics
    assert a.entry_tactic == b.entry_tactic
    assert a.selfloops_dropped == b.selfloops_dropped
    assert a.transitions == b.transitions  # TransitionSpec is a frozen dataclass


# ---------------------------------------------------------------------------
# 6. Reachability / objective / prefix-gap report (emitted per class)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_report_emitted_and_consistent(nets, gap, cls):
    snet = nets[cls]
    report = analyse(snet, load_gasp_view(cls), gap)

    # Objective tactics are real places (guards the semantic mapping).
    for o in OBJECTIVE_TACTICS[cls]:
        assert o in snet.tactics

    # The entry marking's reachable set always includes the seed.
    assert "reconnaissance" in report.reachable_from_entry_marking
    # Any-entry reachability is a superset of entry-marking reachability.
    assert set(report.reachable_from_entry_marking) <= set(
        report.reachable_from_any_entry
    )

    # SNAKES StateGraph cross-check: with one token, #reachable markings ==
    # #reachable places from the seed.
    assert report.reachable_marking_count == len(
        report.reachable_from_entry_marking
    )

    # Paths, when reachable, are consistent (hops = places - 1; endpoints are
    # entry/objective tactics).
    for pr in (report.shortest_entry_to_objective, report.longest_entry_to_objective):
        if pr.reachable:
            assert pr.n_hops == pr.n_places - 1
            assert pr.path[0] in report.entry_tactics
            assert pr.path[-1] in OBJECTIVE_TACTICS[cls]


@pytest.mark.parametrize("cls", CLASS_NAMES)
def test_prefix_gap_matches_inspect_the_base_finding(nets, gap, cls):
    report = analyse(nets[cls], load_gasp_view(cls), gap)
    pg = report.prefix_gap
    assert pg.reconnaissance_present and pg.initial_access_present
    assert pg.recon_reaches_initial_access == EXPECTED_RECON_REACHES_IA[cls]
    # Where bridged, it is bridged by exactly the single direct edge T1593->T1195.
    if EXPECTED_RECON_REACHES_IA[cls]:
        assert ("T1593", "T1195") in pg.direct_edges
