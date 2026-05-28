"""L2 GASP — sanity tests + the operator-deduplicated JSD re-check.

The JSD re-check is Mitigation 1 from
``docs/notes/2026-05-28_l2_operator_aggregation_concern.md``: collapse
multi-flow operator clusters to one representative each (highest
``n_actions``), then re-compute mean pairwise technique-JSD across the
four classes. If it survives above the random-shuffle null p95, the
per-class discrimination is operator-robust. If it collapses, the test
fails *as a finding*, not a bug — flag back to Marc per spec §g.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pytest
from scipy.spatial.distance import jensenshannon

from mtdsim.l2_subgraph import (
    CLASS_NAMES,
    OperationalObjectiveSelector,
    SubgraphView,
    load_classification,
)
from mtdsim.l2_subgraph.build import AUDIT_CSV_PATH, GAP_PATH


# Operator clusters from the operator-aggregation concern note. Hardcoded
# (rather than derived from CSV ``attribution``) because the CISA AA22-138B
# cluster has no shared G-ID — its members share an advisory, not an actor.
OPERATOR_CLUSTERS: dict[str, list[str]] = {
    "Conti": ["conti_cisa_alert", "conti_pwc", "conti_ransomware"],
    "Turla": ["turla_carbon_emulation_plan", "turla_snake_emulation_plan"],
    "FIN13": ["fin13_case_1", "fin13_case_2"],
    "CISA_AA22_138B": [
        "cisa_aa22_138b_vmware_workspace_alt",
        "cisa_aa22_138b_vmware_workspace_ta1",
        "cisa_aa22_138b_vmware_workspace_ta2",
    ],
    "OceanLotus": ["cobalt_kitty_campaign", "oceanlotus"],
    "Sandworm": ["notpetya", "whispergate"],
    "Lazarus": ["sony_malware", "swift_heist"],
}

EXPECTED_CLASS_COUNTS = {
    "pure_steal": 19,
    "pure_impediment": 8,
    "double_extortion": 6,
    "infrastructure_setup": 5,
}


@pytest.fixture(scope="module")
def gap() -> dict:
    with open(GAP_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def classification() -> dict[str, str]:
    return load_classification(AUDIT_CSV_PATH)


@pytest.fixture(scope="module")
def views(gap, classification) -> dict[str, SubgraphView]:
    return {
        cls: OperationalObjectiveSelector(cls).select(gap, classification)
        for cls in CLASS_NAMES
    }


def _read_n_actions() -> dict[str, int]:
    out: dict[str, int] = {}
    with open(AUDIT_CSV_PATH) as f:
        for row in csv.DictReader(f):
            out[row["flow_id"]] = int(row["n_actions"])
    return out


def _operator_deduplicated_flows() -> set[str]:
    n_actions = _read_n_actions()
    drop: set[str] = set()
    for members in OPERATOR_CLUSTERS.values():
        # Sort by (−n_actions, flow_id) — tie-break lexicographically. Deterministic.
        ranked = sorted(members, key=lambda f: (-n_actions[f], f))
        drop.update(ranked[1:])
    return set(n_actions) - drop


def _technique_dist(gap: dict, flow_ids: set[str]) -> np.ndarray:
    """P(technique | class) — pooled over flows.

    Each flow contributes 1 to each technique it uses; row-normalised so
    the class distribution sums to 1.
    """
    tids = sorted(gap["nodes"])
    counts = np.zeros(len(tids), dtype=float)
    for i, tid in enumerate(tids):
        node_flows = set(gap["nodes"][tid]["flow_ids"]) & flow_ids
        counts[i] = len(node_flows)
    total = counts.sum()
    if total == 0:
        return counts
    return counts / total


def _mean_pairwise_jsd(
    gap: dict, class_to_flows: dict[str, list[str]]
) -> float:
    dists = {
        c: _technique_dist(gap, set(fs)) for c, fs in class_to_flows.items()
    }
    classes = list(class_to_flows)
    pairs = [
        (classes[i], classes[j])
        for i in range(len(classes))
        for j in range(i + 1, len(classes))
    ]
    # ``jensenshannon`` returns the JS *distance* (sqrt of divergence). Square
    # to recover the divergence in [0, 1] (base 2 by default).
    return float(
        np.mean([jensenshannon(dists[a], dists[b]) ** 2 for a, b in pairs])
    )


# ---------------------------------------------------------------------------
# 1. Schema round-trip (cheap)
# ---------------------------------------------------------------------------

def test_subgraphview_roundtrip(tmp_path: Path) -> None:
    v = SubgraphView(
        class_name="pure_steal",
        node_set=frozenset(("T1001", "T1003")),
        edge_set=frozenset((("T1001", "T1003"),)),
        provenance={"flow_ids": ["a", "b"], "source_flow_count": 2},
    )
    p = tmp_path / "v.json"
    v.to_json(p)
    w = SubgraphView.from_json(p)
    assert w == v
    with pytest.raises((AttributeError, Exception)):
        # ``frozen=True`` — assignment must fail
        v.class_name = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 2. Classification counts (38 flows, 19:8:6:5 across the 4 classes)
# ---------------------------------------------------------------------------

def test_classification_counts(classification: dict[str, str]) -> None:
    assert len(classification) == 38
    counts: dict[str, int] = {}
    for cls in classification.values():
        counts[cls] = counts.get(cls, 0) + 1
    assert counts == EXPECTED_CLASS_COUNTS


# ---------------------------------------------------------------------------
# 3. Sanity: every class's nodes ⊆ GAP nodes; edges ⊆ GAP edges
# ---------------------------------------------------------------------------

def test_subgraphs_are_subsets_of_gap(
    gap: dict, views: dict[str, SubgraphView]
) -> None:
    gap_nodes = set(gap["nodes"])
    gap_edges = {(e["source_id"], e["target_id"]) for e in gap["edges"]}
    for cls, view in views.items():
        assert view.node_set <= gap_nodes, f"{cls}: extra nodes {view.node_set - gap_nodes}"
        assert view.edge_set <= gap_edges, f"{cls}: extra edges {view.edge_set - gap_edges}"
        # No empty subgraphs.
        assert view.node_set, f"{cls}: empty node_set"


# ---------------------------------------------------------------------------
# 4. Operator-deduplicated JSD re-check (the load-bearing test)
# ---------------------------------------------------------------------------

def test_operator_deduplicated_jsd_above_null(
    gap: dict, classification: dict[str, str]
) -> None:
    kept = _operator_deduplicated_flows()
    deduped = {fid: classification[fid] for fid in kept}
    class_to_flows: dict[str, list[str]] = {c: [] for c in CLASS_NAMES}
    for fid, cls in deduped.items():
        class_to_flows[cls].append(fid)

    observed = _mean_pairwise_jsd(gap, class_to_flows)

    # Null: random equal-sized binary partitions of the deduplicated corpus,
    # JSD between the two halves. Methodology aligned with spec §g's
    # full-corpus calibration ("random 19:19 partitions of the 38 flows").
    # Applied here to the n=29 deduplicated corpus → 14:15 splits.
    rng = np.random.default_rng(seed=20260528)
    flows = list(deduped)
    half = len(flows) // 2
    null_samples = []
    for _ in range(200):
        rng.shuffle(flows)
        d_a = _technique_dist(gap, set(flows[:half]))
        d_b = _technique_dist(gap, set(flows[half:]))
        null_samples.append(float(jensenshannon(d_a, d_b) ** 2))
    null_p95 = float(np.percentile(null_samples, 95))

    # Write the validation note to data/gasp/README.md — fixture side-effect
    # is fine here since the test is the canonical run.
    msg = (
        f"operator-dedup mean JSD = {observed:.4f}  "
        f"(null p95 = {null_p95:.4f}, n={len(kept)} flows kept; "
        f"see docs/notes/2026-05-28_l2_operator_aggregation_concern.md)"
    )
    print("\n" + msg)
    _write_validation_note(observed, null_p95, n_kept=len(kept))

    assert observed > null_p95, (
        f"operator-deduplicated JSD ({observed:.4f}) collapsed to or below "
        f"null p95 ({null_p95:.4f}). This is a real finding, not a bug — "
        f"the per-class discrimination is operator-dominated. Flag to Marc "
        f"per spec §g."
    )


def _write_validation_note(observed: float, null_p95: float, *, n_kept: int) -> None:
    """Refresh the operator-dedup line in data/gasp/README.md.

    The README is written by the build, but the JSD numbers come from this
    test. Idempotent: replaces the prior line if present, appends otherwise.
    """
    readme = (
        Path(__file__).resolve().parents[2] / "data" / "gasp" / "README.md"
    )
    if not readme.exists():
        return
    marker = "**Operator-dedup JSD re-check:**"
    line = (
        f"{marker} mean JSD = {observed:.4f}, null p95 = {null_p95:.4f}, "
        f"n_kept = {n_kept} flows. "
        f"See [`docs/notes/2026-05-28_l2_operator_aggregation_concern.md`]"
        f"(../../docs/notes/2026-05-28_l2_operator_aggregation_concern.md) "
        f"for the mitigation rationale.\n"
    )
    text = readme.read_text()
    if marker in text:
        new_lines = []
        for raw in text.splitlines(keepends=True):
            new_lines.append(line if marker in raw else raw)
        readme.write_text("".join(new_lines))
    else:
        sep = "" if text.endswith("\n") else "\n"
        readme.write_text(text + sep + "\n" + line)
