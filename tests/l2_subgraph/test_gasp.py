"""L2 GASP — sanity tests + the two discrimination checks.

1. The operator-deduplicated technique-JSD re-check (Mitigation 1 from
   ``docs/notes/ch4_methods/operator_concentration.md``): collapse multi-flow
   operator clusters to one representative each (highest ``n_actions``), then
   re-compute mean pairwise technique-JSD across the four classes against a
   random **half-split** null. This is the historical calibration (spec §g);
   Marc's 2026-08-17 ruling records its null as the lenient one for a
   19:8:6:5 partition — a half-split compares two 14–19-flow halves, while
   the observed statistic averages pairs that include 4–8-flow classes, whose
   sparse distributions sit far apart by sampling alone.

2. The **size-matched label-shuffle** check at **tactic-to-tactic
   (transition-share) resolution** — the null L3 ``divergence.py`` uses and
   the resolution the L3 nets quotient into. This is the load-bearing check
   after the 2026-08-17 ruling. Its recorded verdict is that the four
   profiles' transition-share distributions do **not** separate beyond
   chance at this corpus size (mean pairwise JSD sits at the null median);
   the test pins that verdict and the cited numbers, so a corpus change that
   flips it fails loudly and reopens
   ``docs/implementation/pipeline/gasp/tactic_profile_statistics.md``.

JSD unit: **bits** (``jensenshannon(..., base=2) ** 2``, in [0, 1]) — the L3
convention. Numbers recorded before 2026-08-17 (spec §g's 0.317 / 0.148, the
README's 0.3149 / 0.1849) were computed with scipy's default natural-log base
and are in nats; divide by ln 2 to compare (0.3149 nats = 0.454 bits).
"""

from __future__ import annotations

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
from mtdsim.l2_subgraph.dedup import (
    OPERATOR_CLUSTERS,
    operator_deduplicated_flows,
)

EXPECTED_CLASS_COUNTS = {
    "objective_exfiltration": 19,
    "objective_impact": 8,
    "objective_exfiltration_impact": 6,
    "objective_none_c2": 5,
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


# The dedup rule itself lives in ``mtdsim.l2_subgraph.dedup`` (single source
# of truth — the L3a weight build consumes the same rule).
_operator_deduplicated_flows = operator_deduplicated_flows


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
    # to recover the divergence; ``base=2`` puts it in bits, in [0, 1] (scipy's
    # default base is e, which is what the pre-2026-08-17 numbers were in).
    return float(
        np.mean([_jsd(dists[a], dists[b]) for a, b in pairs])
    )


def _jsd(p: np.ndarray, q: np.ndarray) -> float:
    return float(jensenshannon(p, q, base=2) ** 2)


# ---------------------------------------------------------------------------
# 1. Schema round-trip (cheap)
# ---------------------------------------------------------------------------

def test_subgraphview_roundtrip(tmp_path: Path) -> None:
    v = SubgraphView(
        class_name="objective_exfiltration",
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
# 4. Operator-deduplicated JSD re-check (historical calibration — half-split null)
# ---------------------------------------------------------------------------

def test_operator_deduplicated_jsd_above_null(
    gap: dict, classification: dict[str, str]
) -> None:
    # sorted() so the seeded shuffle below starts from a deterministic order
    # — _operator_deduplicated_flows returns a set, whose iteration order
    # depends on hash randomisation.
    kept = sorted(_operator_deduplicated_flows())
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
        null_samples.append(_jsd(d_a, d_b))
    null_p95 = float(np.percentile(null_samples, 95))

    # Write the validation note to data/gasp/README.md — fixture side-effect
    # is fine here since the test is the canonical run.
    msg = (
        f"operator-dedup mean JSD = {observed:.4f}  "
        f"(null p95 = {null_p95:.4f}, n={len(kept)} flows kept; "
        f"see docs/notes/ch4_methods/operator_concentration.md)"
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
        f"{marker} mean JSD = {observed:.4f} bits, half-split null p95 = {null_p95:.4f}, "
        f"n_kept = {n_kept} flows. "
        f"See [`docs/notes/ch4_methods/operator_concentration.md`]"
        f"(../../docs/notes/ch4_methods/operator_concentration.md) "
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


# ---------------------------------------------------------------------------
# 5. Size-matched null at tactic-to-tactic resolution (the load-bearing check
#    after Marc's 2026-08-17 ruling; pins the recorded verdict + cited numbers)
# ---------------------------------------------------------------------------

SIZE_MATCHED_TRIALS = 2000
SIZE_MATCHED_SEED = 20260528
# Recorded in docs/implementation/pipeline/gasp/tactic_profile_statistics.md;
# tools/gasp_tactic_profile_stats.py reproduces them.
RECORDED_TRANSITION_JSD = {"full": 0.501, "dedup": 0.534}


def _transition_share(gap: dict, flow_ids: set[str], pairs: list[tuple[str, str]]) -> np.ndarray:
    """P(tactic-pair transition | class): distinct flows drawing each
    inter-tactic pair (primary_tactic; intra-tactic edges dropped, as the L3
    quotient drops them), normalised over all pairs. Flow-presence pooling —
    the count the L3 W-A weight layer is built from."""
    tactic_of = {t: n["primary_tactic"] for t, n in gap["nodes"].items()}
    idx = {p: i for i, p in enumerate(pairs)}
    seen: set[tuple[str, tuple[str, str]]] = set()
    counts = np.zeros(len(pairs), dtype=float)
    for e in gap["edges"]:
        a, b = tactic_of[e["source_id"]], tactic_of[e["target_id"]]
        if a == b:
            continue
        for f in e["flow_ids"]:
            if f in flow_ids and (f, (a, b)) not in seen:
                seen.add((f, (a, b)))
                counts[idx[(a, b)]] += 1
    total = counts.sum()
    return counts / total if total else counts


def _inter_tactic_pairs(gap: dict) -> list[tuple[str, str]]:
    tactic_of = {t: n["primary_tactic"] for t, n in gap["nodes"].items()}
    return sorted({
        (tactic_of[e["source_id"]], tactic_of[e["target_id"]])
        for e in gap["edges"]
        if tactic_of[e["source_id"]] != tactic_of[e["target_id"]]
    })


def _mean_pairwise_transition_jsd(gap, pairs, groups: list[list[str]]) -> float:
    dists = [_transition_share(gap, set(g), pairs) for g in groups]
    return float(np.mean([
        _jsd(dists[i], dists[j])
        for i in range(len(dists)) for j in range(i + 1, len(dists))
    ]))


@pytest.mark.parametrize("corpus", ["full", "dedup"])
def test_transition_share_size_matched_null_verdict(
    gap: dict, classification: dict[str, str], corpus: str
) -> None:
    flows = sorted(classification) if corpus == "full" else sorted(_operator_deduplicated_flows())
    pairs = _inter_tactic_pairs(gap)
    assert len(pairs) == 122
    groups = [[f for f in flows if classification[f] == c] for c in CLASS_NAMES]
    sizes = [len(g) for g in groups]
    observed = _mean_pairwise_transition_jsd(gap, pairs, groups)

    rng = np.random.default_rng(seed=SIZE_MATCHED_SEED)
    pool = list(flows)
    null = np.empty(SIZE_MATCHED_TRIALS)
    for i in range(SIZE_MATCHED_TRIALS):
        rng.shuffle(pool)
        cur, trial = 0, []
        for s in sizes:
            trial.append(pool[cur:cur + s]); cur += s
        null[i] = _mean_pairwise_transition_jsd(gap, pairs, trial)
    p95 = float(np.percentile(null, 95))
    p_value = float(np.mean(null >= observed))
    msg = (
        f"[{corpus} n={len(flows)}] transition-share mean pairwise JSD = {observed:.4f} bits; "
        f"size-matched null p50 = {np.percentile(null, 50):.4f}, p95 = {p95:.4f}, p = {p_value:.3f}"
    )
    print("\n" + msg)
    if corpus == "dedup":
        _write_size_matched_note(observed, p95, p_value, n=len(flows))

    # Pin the cited number (3 d.p.). A drift here means the corpus or the
    # quotient changed: regenerate tactic_profile_statistics.md.
    assert abs(observed - RECORDED_TRANSITION_JSD[corpus]) < 0.0015, msg
    # Pin the recorded verdict: no separation beyond chance at this
    # resolution. If this fires, the profiles now clear the strict null —
    # a corpus change worth a new record, not a bug.
    assert observed <= p95, (
        f"transition-share separation now clears the size-matched null p95 — "
        f"reopen tactic_profile_statistics.md. {msg}"
    )


def _write_size_matched_note(observed: float, p95: float, p_value: float, *, n: int) -> None:
    readme = Path(__file__).resolve().parents[2] / "data" / "gasp" / "README.md"
    if not readme.exists():
        return
    marker = "**Size-matched null, tactic-to-tactic resolution:**"
    line = (
        f"{marker} mean pairwise transition-share JSD = {observed:.4f} bits, "
        f"size-matched null p95 = {p95:.4f}, p = {p_value:.3f}, n = {n} flows "
        f"(does not clear — the recorded verdict; see "
        f"[`docs/implementation/pipeline/gasp/tactic_profile_statistics.md`]"
        f"(../../docs/implementation/pipeline/gasp/tactic_profile_statistics.md)).\n"
    )
    text = readme.read_text()
    if marker in text:
        readme.write_text("".join(line if marker in raw else raw for raw in text.splitlines(keepends=True)))
    else:
        sep = "" if text.endswith("\n") else "\n"
        readme.write_text(text + sep + line)
