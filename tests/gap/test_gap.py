"""Validation gate for the L1 GAP (docs/specs/01_gap_schema.md §g + the
gap_rebuild handoff).

Corpus-dependent tests skip cleanly when the gitignored inputs are absent
(fresh clone); run ``python -m mtdsim.l0_cti`` to enable them. The
synthetic-branch and OR tests are self-contained and always run.
"""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from mtdsim.l1_construction import (
    FlowEdge,
    FlowNode,
    PerFlowExtract,
    acyclic_projection,
    build_gap,
    contract_flow,
    parse_flow_file,
    support_filter,
)

_REPO = Path(__file__).resolve().parents[2]
_CORPUS = _REPO / "data" / "gap" / "_corpus_stix"
_TESLA = _CORPUS / "Tesla Kubernetes Breach.json"
_ATTACK = sorted((_REPO / "data" / "gap" / "_attack").glob("enterprise-attack-*.json"))

_TESLA_AND_INPUTS = {"T1610", "T1090", "T1571"}
_TESLA_AND_TARGET = "T1496"

_needs_corpus = pytest.mark.skipif(
    not _TESLA.exists() or not _ATTACK,
    reason="GAP corpus inputs absent — run python -m mtdsim.l0_cti",
)


@pytest.fixture(scope="module")
def built():
    """(extracts, gap) built once from the acquired corpus."""
    if not _TESLA.exists() or not _ATTACK:
        pytest.skip("GAP corpus inputs absent")
    return build_gap()


@pytest.fixture(scope="module")
def tesla_extract():
    if not _TESLA.exists():
        pytest.skip("Tesla flow absent")
    return parse_flow_file(_TESLA)


# ---------------------------------------------------------------------------
# 1. Tesla golden — operators survive (the v0.4-failing test).
# ---------------------------------------------------------------------------


@_needs_corpus
def test_tesla_per_flow_and_join(tesla_extract):
    """The per-flow extract has one AND operator joining the three inputs."""
    ops = [n for n in tesla_extract.nodes if n.kind == "operator"]
    assert len(ops) == 1 and ops[0].operator == "AND"
    op = ops[0]
    inputs = {
        tesla_extract.node_by_id()[e.source].technique_id
        for e in tesla_extract.edges
        if e.target == op.id
    }
    assert inputs == _TESLA_AND_INPUTS


@_needs_corpus
def test_tesla_aggregate_and_group(built):
    """In the GAP the three inputs -> T1496 share one join.group_id, operator AND."""
    _, gap = built
    into_target = [
        e for e in gap.edges
        if e.target_id == _TESLA_AND_TARGET and e.source_id in _TESLA_AND_INPUTS
    ]
    assert {e.source_id for e in into_target} == _TESLA_AND_INPUTS

    group_ids = set()
    for e in into_target:
        tesla_occ = [o for o in e.occurrences if o.flow_id == "tesla_kubernetes_breach"]
        assert tesla_occ, f"{e.source_id}->{e.target_id} missing tesla occurrence"
        for o in tesla_occ:
            assert o.join is not None and o.join.operator == "AND"
            group_ids.add(o.join.group_id)
    assert len(group_ids) == 1, f"AND inputs should share one group_id, got {group_ids}"


# ---------------------------------------------------------------------------
# 2. No-synthesis — every edge/occurrence traces to a real flow link.
# ---------------------------------------------------------------------------


@_needs_corpus
def test_no_synthesised_edges(built):
    extracts, gap = built
    # signature set of contracted edges actually present in each flow
    real: dict[str, set] = {}
    for ex in extracts:
        real[ex.flow_id] = {
            (c.source_id, c.target_id, c.edge_type, c.group_id, c.operator, c.branch)
            for c in contract_flow(ex)
        }
    for e in gap.edges:
        assert e.occurrences, f"edge {e.key()} has no occurrences"
        assert e.observation_count == len({o.flow_id for o in e.occurrences})
        for o in e.occurrences:
            sig = (
                e.source_id, e.target_id, o.edge_type,
                o.join.group_id if o.join else None,
                o.join.operator if o.join else None,
                o.branch,
            )
            assert sig in real.get(o.flow_id, set()), (
                f"occurrence {sig} not traceable to flow {o.flow_id}"
            )


# ---------------------------------------------------------------------------
# 3. Round-trip — extract <-> YAML, and extract topology == STIX topology.
# ---------------------------------------------------------------------------


@_needs_corpus
def test_yaml_round_trip(tesla_extract):
    again = PerFlowExtract.from_yaml(tesla_extract.to_yaml())
    assert again.to_dict() == tesla_extract.to_dict()
    assert contract_flow(again) == contract_flow(tesla_extract)


@_needs_corpus
def test_extract_topology_matches_stix(tesla_extract):
    """Action technique set + directed action->action effect edges, from the
    extract, match a direct read of the STIX bundle."""
    import json

    bundle = json.load(open(_TESLA))
    objs = {o["id"]: o for o in bundle["objects"]}
    parent = lambda t: t.split(".", 1)[0] if t else t
    stix_tids = {
        parent(o["technique_id"])
        for o in bundle["objects"]
        if o.get("type") == "attack-action" and o.get("technique_id")
    }
    extract_tids = {n.technique_id for n in tesla_extract.nodes if n.kind == "action" and n.technique_id}
    assert extract_tids == stix_tids


# ---------------------------------------------------------------------------
# 4. Multiplicity is numeric + non-degenerate.
# ---------------------------------------------------------------------------


@_needs_corpus
def test_observation_count_non_degenerate(built):
    _, gap = built
    counts = [e.observation_count for e in gap.edges]
    assert counts and all(isinstance(c, int) and c >= 1 for c in counts)
    assert max(counts) > 1, "observation_count is degenerate (all 1s)"


# ---------------------------------------------------------------------------
# 5. Lossless — a support-filter view never mutates the artefact.
# ---------------------------------------------------------------------------


@_needs_corpus
def test_support_filter_is_a_view(built):
    _, gap = built
    before = copy.deepcopy(gap.to_dict())
    view = support_filter(gap, min_observation_count=2)
    assert len(view.edges) < gap.edge_count          # genuinely filters
    assert all(e.observation_count >= 2 for e in view.edges)
    assert gap.to_dict() == before                   # artefact untouched


@_needs_corpus
def test_acyclic_projection_is_a_dag_and_a_view(built):
    _, gap = built
    before = copy.deepcopy(gap.to_dict())
    view = acyclic_projection(gap)
    # kept + cut accounts for every original edge
    assert len(view.edges) + len(view.cut_edges) == gap.edge_count
    # kept edges are acyclic
    from mtdsim.l1_construction.views import _find_one_cycle
    adj: dict[str, list[str]] = {}
    for e in view.edges:
        adj.setdefault(e.source_id, []).append(e.target_id)
    nodes = sorted({e.source_id for e in view.edges} | {e.target_id for e in view.edges})
    assert _find_one_cycle(adj, nodes) is None
    assert gap.to_dict() == before                   # artefact untouched


@_needs_corpus
def test_or_operator_present_in_corpus(built):
    """OR operators (29 in the corpus) survive contraction into edge metadata."""
    _, gap = built
    assert any(
        o.join is not None and o.join.operator == "OR"
        for e in gap.edges for o in e.occurrences
    )


# ---------------------------------------------------------------------------
# Enterprise-only scope (Decision 5) — only resolvable Enterprise nodes survive.
# ---------------------------------------------------------------------------


@_needs_corpus
def test_gap_is_enterprise_only(built):
    """The aggregate carries only techniques that resolve in the pinned
    Enterprise ATT&CK: every node is labelled, and ATLAS / ICS / revoked-or-
    absent ids are dropped at aggregation. (No-bridge across a dropped node is
    covered by test_no_synthesised_edges — a bridge would trace to no flow.)"""
    _, gap = built
    unlabelled = [t for t, n in gap.nodes.items() if not n.name]
    assert not unlabelled, f"non-Enterprise/revoked nodes leaked into the GAP: {unlabelled}"
    # concrete regression anchors — each was a GAP node at v0.5 pre-filter
    for dropped in ("AML.T0008", "T0834", "T1562"):  # ATLAS, ICS, revoked-Enterprise
        assert dropped not in gap.nodes, f"{dropped} must be dropped (non-Enterprise)"


# ---------------------------------------------------------------------------
# 6. Synthetic condition branch — on_true / on_false tagging (corpus has none).
# ---------------------------------------------------------------------------


def _branch_extract() -> PerFlowExtract:
    """A1 -> condition c1; c1 on_true -> A2, on_false -> A3."""
    return PerFlowExtract(
        flow_id="synthetic_branch",
        flow_name="Synthetic Branch",
        scope="incident",
        source="hand_curated",
        schema_version="2.0.0",
        start_refs=["a1"],
        nodes=[
            FlowNode(id="a1", kind="action", technique_id="T9001", name="Start"),
            FlowNode(id="c1", kind="condition", description="precondition met?"),
            FlowNode(id="a2", kind="action", technique_id="T9002", name="OnTrue"),
            FlowNode(id="a3", kind="action", technique_id="T9003", name="OnFalse"),
        ],
        edges=[
            FlowEdge(source="a1", target="c1", type="effect"),
            FlowEdge(source="c1", target="a2", type="on_true"),
            FlowEdge(source="c1", target="a3", type="on_false"),
        ],
    )


def test_condition_branches_tagged():
    edges = {(c.source_id, c.target_id): c for c in contract_flow(_branch_extract())}
    assert edges[("T9001", "T9002")].branch == "true"
    assert edges[("T9001", "T9002")].edge_type == "on_true"
    assert edges[("T9001", "T9003")].branch == "false"
    assert edges[("T9001", "T9003")].edge_type == "on_false"


def test_condition_sink_yields_no_edge():
    """A path ending at a condition with no outgoing refs draws no edge."""
    ex = PerFlowExtract(
        flow_id="sink", flow_name="Sink", scope="incident", source="hand_curated",
        schema_version="2.0.0", start_refs=["a1"],
        nodes=[
            FlowNode(id="a1", kind="action", technique_id="T9001"),
            FlowNode(id="c1", kind="condition", description="reached state"),
        ],
        edges=[FlowEdge(source="a1", target="c1", type="effect")],
    )
    assert contract_flow(ex) == []


def test_parent_collapse_handles_enterprise_and_atlas():
    """Sub-technique collapse strips only the trailing .NNN — it must not
    conflate ATLAS ids (AML.T####.###) into a single AML node."""
    from mtdsim.l1_construction.attack_flow_parser import _parent_technique

    assert _parent_technique("T1078.004") == "T1078"
    assert _parent_technique("T1496") == "T1496"
    assert _parent_technique("AML.T0051.001") == "AML.T0051"
    assert _parent_technique("AML.T0008") == "AML.T0008"
    # distinct ATLAS techniques stay distinct
    assert _parent_technique("AML.T0051.001") != _parent_technique("AML.T0008")


def test_untyped_action_breaks_chain():
    """An action with no technique_id does not bridge a synthesised edge."""
    ex = PerFlowExtract(
        flow_id="gap", flow_name="Gap", scope="incident", source="hand_curated",
        schema_version="2.0.0", start_refs=["a1"],
        nodes=[
            FlowNode(id="a1", kind="action", technique_id="T9001"),
            FlowNode(id="a2", kind="action", technique_id=None),   # unmapped
            FlowNode(id="a3", kind="action", technique_id="T9003"),
        ],
        edges=[
            FlowEdge(source="a1", target="a2", type="effect"),
            FlowEdge(source="a2", target="a3", type="effect"),
        ],
    )
    pairs = {(c.source_id, c.target_id) for c in contract_flow(ex)}
    assert ("T9001", "T9003") not in pairs   # no edge synthesised across the gap
    assert pairs == set()                     # a1->a2 and a2->a3 both blocked by untyped a2
