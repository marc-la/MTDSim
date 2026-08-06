"""L3a W-A weight layer + aggregate profile + divergence report — validation gate.

Covers the weighting handoff's gate:

1. per-place out-weights sum to 1 (over retained, non-self-loop transitions),
   both corpus variants, all five profiles — the mechanical routing test;
2. no-synthesis: weighting adds metadata only — the committed JSONs carry the
   same places/transitions/provenance edges as a fresh structural build (no
   transition gained or lost), and every transition has a weight layer;
3. weights derive from **distinct-flow counts** (never ``observation_count``):
   the persisted numerators are independently reproduced from the GAP edges'
   ``flow_ids`` alone;
4. the aggregate (null) net exists with both corpus variants and a coherent
   entry -> objective path (D9);
5. the shuffled-label null quotient is genuinely comparable to the class
   nets' weighted out-distributions (identity check);
6. determinism (weights and null band).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mtdsim.l2_subgraph.dedup import operator_deduplicated_flows
from mtdsim.l3_simulation.petri.analysis import OBJECTIVE_TACTICS, analyse
from mtdsim.l3_simulation.petri.build import (
    AGGREGATE,
    PROFILE_NAMES,
    build_all_profiles,
    load_gap_index,
    load_profile_view,
)
from mtdsim.l3_simulation.petri.divergence import (
    _bfs,
    _supported_adjacency,
    out_distributions,
    quotient_out_dists,
    shuffled_label_null,
)
from mtdsim.l3_simulation.petri.render import PETRI_DIR
from mtdsim.l3_simulation.petri.weights import (
    PRIMARY_VARIANT,
    VARIANTS,
    compute_all_variants,
    load_edge_flows,
    profile_flow_sets,
    variant_flow_filter,
)

WEIGHT_KEYS = {
    "numerator",
    "denominator",
    "weight",
    "flows_leaving_source",
    "flow_proportion",
    "backing_flow_ids",
}


@pytest.fixture(scope="module")
def gap():
    return load_gap_index()


@pytest.fixture(scope="module")
def nets():
    return build_all_profiles()


@pytest.fixture(scope="module")
def edge_flows():
    return load_edge_flows()


@pytest.fixture(scope="module")
def profile_flows():
    return profile_flow_sets()


@pytest.fixture(scope="module")
def weights(nets, edge_flows, profile_flows):
    return {
        p: compute_all_variants(nets[p], edge_flows, profile_flows[p])
        for p in PROFILE_NAMES
    }


@pytest.fixture(scope="module")
def committed():
    out = {}
    for p in PROFILE_NAMES:
        with open(Path(PETRI_DIR) / f"{p}_structural.json") as f:
            out[p] = json.load(f)
    return out


# ---------------------------------------------------------------------------
# 0. The dedup discipline: n = 29, and the committed JSONs agree
# ---------------------------------------------------------------------------


def test_operator_dedup_corpus_size(profile_flows):
    kept = operator_deduplicated_flows()
    assert len(kept) == 29
    assert len(profile_flows[AGGREGATE]) == 38
    assert len(profile_flows[AGGREGATE] & kept) == 29


# ---------------------------------------------------------------------------
# 1. Per-place out-weights sum to 1 (the mechanical routing gate)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("profile", PROFILE_NAMES)
@pytest.mark.parametrize("variant", VARIANTS)
def test_out_weights_sum_to_one(nets, weights, profile, variant):
    snet = nets[profile]
    tw = weights[profile][variant]
    sums: dict[str, float] = {}
    for spec in snet.transitions:
        w = tw[spec.name]
        if w.weight is None:
            # Whole-place undefinedness only: every sibling out-transition
            # must be undefined too (denominator is a place-level quantity).
            assert w.denominator == 0
            continue
        sums[spec.src_tactic] = sums.get(spec.src_tactic, 0.0) + w.weight
    for place, s in sums.items():
        assert abs(s - 1.0) < 1e-9, f"{profile}/{variant}/{place}: sum {s}"


# ---------------------------------------------------------------------------
# 2. No-synthesis: weights are metadata on the shipped structure
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("profile", PROFILE_NAMES)
def test_committed_json_matches_fresh_structure(nets, committed, profile):
    """The committed JSON's structural fields equal a fresh build's — no
    transition gained or lost by the weighting pass (diff test)."""
    snet = nets[profile]
    doc = committed[profile]
    assert doc["places"] == list(snet.tactics)
    assert doc["entry_marking"] == snet.entry_tactic
    fresh = {
        t.name: (t.src_tactic, t.dst_tactic, [list(e) for e in t.edges])
        for t in snet.transitions
    }
    persisted = {
        t["name"]: (t["src_tactic"], t["dst_tactic"], t["gasp_edges"])
        for t in doc["transitions"]
    }
    assert persisted == fresh


@pytest.mark.parametrize("profile", PROFILE_NAMES)
def test_committed_weight_layer_complete(committed, profile):
    doc = committed[profile]
    assert doc["weighting"]["primary_variant"] == PRIMARY_VARIANT
    assert doc["weighting"]["counts_flows_not_observation_count"] is True
    assert doc["weighting"]["smoothing"] == "none"
    for t in doc["transitions"]:
        assert set(t["weights"]) == set(VARIANTS)
        for variant in VARIANTS:
            layer = t["weights"][variant]
            assert set(layer) == WEIGHT_KEYS
            # ``observation_count`` never appears as (or inside) a weight.
            assert "observation_count" not in json.dumps(layer)


# ---------------------------------------------------------------------------
# 3. Weights count distinct flows — reproduced from flow_ids alone
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("profile", PROFILE_NAMES)
@pytest.mark.parametrize("variant", VARIANTS)
def test_numerators_are_distinct_flow_counts(
    nets, weights, edge_flows, profile_flows, profile, variant
):
    snet = nets[profile]
    tw = weights[profile][variant]
    vf = variant_flow_filter(variant)
    eligible = (
        profile_flows[profile]
        if vf is None
        else profile_flows[profile] & vf
    )
    for spec in snet.transitions:
        w = tw[spec.name]
        expected = set()
        for uv in spec.edges:
            expected |= edge_flows[uv] & eligible
        assert set(w.backing_flow_ids) == expected
        assert w.numerator == len(expected)
        # Every transition still traces to >=1 GASP technique-edge; zero
        # backing zeroes the weight but never removes the transition.
        assert spec.edges
        if w.numerator == 0:
            assert w.weight in (0.0, None)


@pytest.mark.parametrize("profile", PROFILE_NAMES)
def test_committed_weights_match_fresh(committed, weights, profile):
    """The persisted weight layer is byte-equal to a fresh computation."""
    for t in committed[profile]["transitions"]:
        for variant in VARIANTS:
            fresh = weights[profile][variant][t["name"]].to_dict()
            assert t["weights"][variant] == fresh


# ---------------------------------------------------------------------------
# 4. The aggregate (null) profile — D9 coherence, both variants recorded
# ---------------------------------------------------------------------------


def test_aggregate_net_shape(nets, gap):
    snet = nets[AGGREGATE]
    view = load_profile_view(AGGREGATE)
    # Full GAP tactic-quotient: every GAP node/edge is in the union view.
    assert view.node_set == frozenset(gap.tactic_of)
    report = analyse(snet, view, gap)
    # Coherent entry -> objective path (D9): from initial-access the whole
    # declared objective set (union of the four class objectives) is
    # reachable on the *positive-weight* dedup support.
    assert report.prefix_gap.recon_reaches_initial_access


def test_aggregate_objectives_reachable_on_dedup_support(nets, weights):
    snet = nets[AGGREGATE]
    adj = _supported_adjacency(snet, weights[AGGREGATE][PRIMARY_VARIANT])
    reach = _bfs(adj, ["initial-access"])
    for objective in OBJECTIVE_TACTICS[AGGREGATE]:
        assert objective in reach, f"aggregate: {objective} unreachable"


def test_aggregate_committed_variants(committed):
    variants = committed[AGGREGATE]["weighting"]["variants"]
    assert variants[PRIMARY_VARIANT]["n_profile_flows"] == 29
    assert variants["raw"]["n_profile_flows"] == 38


# ---------------------------------------------------------------------------
# 5. Null comparability: the quotient equals the class nets' distributions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("profile", PROFILE_NAMES)
def test_quotient_identity(nets, weights, edge_flows, profile_flows, gap, profile):
    """The flow-quotient the shuffled null rebuilds equals the weighted
    out-distributions of the real net — so null trials and observed classes
    are scored by the same construction."""
    kept = operator_deduplicated_flows()
    flows = profile_flows[profile] & kept
    from_quotient = quotient_out_dists(edge_flows, gap.tactic_of, flows)
    from_net = out_distributions(nets[profile], weights[profile][PRIMARY_VARIANT])
    # Drop zero-weight entries from the net's dists — the quotient never
    # materialises unobserved pairs; zero mass either way.
    from_net = {
        place: {b: w for b, w in dsts.items() if w > 0}
        for place, dsts in from_net.items()
    }
    from_net = {p: d for p, d in from_net.items() if d}
    assert from_quotient.keys() == from_net.keys()
    for place in from_net:
        assert from_quotient[place] == pytest.approx(from_net[place])


# ---------------------------------------------------------------------------
# 6. Determinism
# ---------------------------------------------------------------------------


def test_weights_deterministic(nets, edge_flows, profile_flows):
    p = "objective_impact"
    a = compute_all_variants(nets[p], edge_flows, profile_flows[p])
    b = compute_all_variants(nets[p], edge_flows, profile_flows[p])
    assert a == b


def test_null_band_deterministic(nets, weights, edge_flows, profile_flows, gap):
    kept = operator_deduplicated_flows()
    agg = out_distributions(nets[AGGREGATE], weights[AGGREGATE][PRIMARY_VARIANT])
    class_flows = {
        c: profile_flows[c] & kept for c in PROFILE_NAMES if c != AGGREGATE
    }
    a = shuffled_label_null(
        edge_flows, gap.tactic_of, class_flows, agg, n_trials=5, seed=1
    )
    b = shuffled_label_null(
        edge_flows, gap.tactic_of, class_flows, agg, n_trials=5, seed=1
    )
    assert a == b


# ---------------------------------------------------------------------------
# 7. The committed divergence report is fresh and internally consistent
# ---------------------------------------------------------------------------


def test_divergence_report_consistent():
    with open(Path(PETRI_DIR) / "divergence_report.json") as f:
        d = json.load(f)
    assert d["primary_variant"] == PRIMARY_VARIANT
    for cls, mean in d["mean_jsd"].items():
        assert 0.0 <= mean <= 1.0
        assert d["exceeds_null_p95"][cls] == (
            mean > d["null_band"][cls]["p95"]
        )
    assert (Path(PETRI_DIR) / "divergence_report.md").exists()
