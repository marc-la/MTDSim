"""W-A flow-proportion weights for the tactic-place nets (supervisor decision D3).

The weighting regime — dispositioned in
[`docs/implementation/metrics_semantics.md`](../../../../docs/implementation/metrics_semantics.md)
§(f) before this build committed a normalised weight anywhere:

- **What is counted: flows, never ``observation_count``.** For transition
  ``a -> b`` under profile ``P`` (a GASP class, or the aggregate), the
  ``numerator`` is the number of **distinct attack flows** in ``P`` that
  contribute >=1 technique-edge whose source tactic is ``a`` and target tactic
  is ``b``. Counting flows (not technique-edges) is robust to one flow drawing
  many parallel technique-edges under the same tactic-pair; the W-B edge-count
  alternative was rejected (it double-counts multi-edge flows and leans on
  ``observation_count`` magnitudes 88 % of which are 1 — the very thing §(f)
  warns against). This module never reads ``observation_count``.
- **Weight = out-edge-normalised flow proportion** (the §(f) D3 wording):
  ``weight = numerator / denominator`` where ``denominator`` sums the
  numerators over the source place's retained (inter-tactic) out-transitions.
  Per-place out-weights therefore sum to 1 mechanically — the routing
  distribution the timeline runner draws from.
- **The literal minuted proportion is stored beside it.** The minuted wording
  ("proportion of attack flows leaving each node") reads as
  ``numerator / |F_P(a->.)|`` with ``flows_leaving_source = |F_P(a->.)|`` the
  distinct flows contributing *any* out-edge from ``a``. When one flow
  branches from ``a`` to several destination tactics those proportions sum to
  more than 1, so they cannot be the routing distribution; both counts are
  stored (``flow_proportion`` beside ``weight``) so the thinness stays
  visible (D9: "looking thin is fine — but only if it *looks* thin").
  No smoothing; a smoothing scheme would be a new declared decision.
- **Two corpus variants, both recorded.** ``operator_dedup`` (primary; the
  n = 29 corpus of ``mtdsim.l2_subgraph.dedup``, spec §(g) Mitigation 1) and
  ``raw`` (n = 38; the robustness column).
- **No synthesis.** Weighting adds metadata to the existing transitions of the
  shipped structural nets; it never adds or removes structure. A transition
  whose backing flows all fall outside the profile/variant keeps weight 0 (or
  ``None`` where the whole place has no flow-backed out-edge). In-tactic dwell
  is the duration catalogue's job, not a self-loop weight (self-loops were
  dropped at structural build time).

Weights are **workflow-recurrence, never efficacy or actor-likelihood** — the
§(f) survivorship framing governs every reading: a weighted traversal samples
typical *observed* workflow under a class **envelope**, not an actor's policy.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from mtdsim.l2_subgraph.dedup import operator_deduplicated_flows
from mtdsim.l3_simulation.petri.build import GAP_PATH, StructuralNet

_REPO_ROOT = Path(__file__).resolve().parents[4]
CLASSIFICATION_CSV = _REPO_ROOT / "data" / "gasp" / "classification.csv"

# Corpus variants. ``operator_dedup`` is primary (handoff step 2); ``raw`` is
# the robustness column. Order is presentation order in JSON/report.
PRIMARY_VARIANT = "operator_dedup"
VARIANTS = (PRIMARY_VARIANT, "raw")


@dataclass(frozen=True)
class TransitionWeights:
    """The weight layer of one transition under one profile x corpus variant.

    ``weight = numerator / denominator`` (None when ``denominator == 0``) is
    the out-edge-normalised routing weight; ``flow_proportion = numerator /
    flows_leaving_source`` (None when 0) is the literal minuted per-flow
    proportion, which sums to >1 across a branching place. ``backing_flow_ids``
    are the distinct profile flows behind the numerator (provenance).
    """

    numerator: int
    denominator: int
    weight: float | None
    flows_leaving_source: int
    flow_proportion: float | None
    backing_flow_ids: tuple[str, ...]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["backing_flow_ids"] = list(self.backing_flow_ids)
        return d


def load_edge_flows(
    gap_path: Path = GAP_PATH,
) -> dict[tuple[str, str], frozenset[str]]:
    """``(source_id, target_id) -> flow_ids`` for every GAP technique-edge.

    Reads only the edge endpoints and ``flow_ids`` — the flow-counting W-A
    regime has no use for any other edge attribute.
    """
    with open(gap_path) as f:
        gap = json.load(f)
    return {
        (e["source_id"], e["target_id"]): frozenset(e["flow_ids"])
        for e in gap["edges"]
    }


def load_class_flows(
    classification_csv: Path = CLASSIFICATION_CSV,
) -> dict[str, frozenset[str]]:
    """``class_name -> flow_ids`` from ``data/gasp/classification.csv``,
    consumed unchanged (hard constraint — no re-derivation)."""
    by_class: dict[str, set[str]] = {}
    with open(classification_csv) as f:
        for row in csv.DictReader(f):
            by_class.setdefault(row["class_name"], set()).add(row["flow_id"])
    return {c: frozenset(fs) for c, fs in by_class.items()}


def profile_flow_sets(
    classification_csv: Path = CLASSIFICATION_CSV,
) -> dict[str, frozenset[str]]:
    """Flow sets per profile: the four classes plus ``aggregate`` = the union
    of all classified flows (the full corpus — built from the flow union, not
    an average of the class nets, so the null is corpus-grounded)."""
    class_flows = load_class_flows(classification_csv)
    out = dict(class_flows)
    out["aggregate"] = frozenset().union(*class_flows.values())
    return out


def variant_flow_filter(variant: str) -> frozenset[str] | None:
    """The corpus-variant filter: the dedup kept-set, or None (= no filter)."""
    if variant == PRIMARY_VARIANT:
        return operator_deduplicated_flows()
    if variant == "raw":
        return None
    raise ValueError(f"unknown corpus variant {variant!r}")


def compute_weights(
    snet: StructuralNet,
    edge_flows: dict[tuple[str, str], frozenset[str]],
    profile_flows: frozenset[str],
    variant_filter: frozenset[str] | None,
) -> dict[str, TransitionWeights]:
    """W-A weights for every transition of one net, keyed by transition name.

    Deterministic: transitions are iterated in their (sorted) build order and
    backing flow sets are sorted on storage.
    """
    eligible = (
        profile_flows if variant_filter is None else profile_flows & variant_filter
    )

    backing: dict[str, frozenset[str]] = {}
    for spec in snet.transitions:
        flows: set[str] = set()
        for uv in spec.edges:
            flows |= edge_flows[uv] & eligible
        backing[spec.name] = frozenset(flows)

    # Per-place aggregation over retained (inter-tactic) out-transitions.
    out_specs: dict[str, list[str]] = {}
    for spec in snet.transitions:
        out_specs.setdefault(spec.src_tactic, []).append(spec.name)
    denominator = {
        place: sum(len(backing[n]) for n in names)
        for place, names in out_specs.items()
    }
    flows_leaving = {
        place: len(frozenset().union(*(backing[n] for n in names)))
        for place, names in out_specs.items()
    }

    out: dict[str, TransitionWeights] = {}
    for spec in snet.transitions:
        num = len(backing[spec.name])
        den = denominator[spec.src_tactic]
        leaving = flows_leaving[spec.src_tactic]
        out[spec.name] = TransitionWeights(
            numerator=num,
            denominator=den,
            weight=(num / den) if den else None,
            flows_leaving_source=leaving,
            flow_proportion=(num / leaving) if leaving else None,
            backing_flow_ids=tuple(sorted(backing[spec.name])),
        )
    return out


def compute_all_variants(
    snet: StructuralNet,
    edge_flows: dict[tuple[str, str], frozenset[str]],
    profile_flows: frozenset[str],
) -> dict[str, dict[str, TransitionWeights]]:
    """``variant -> transition name -> TransitionWeights`` for one net."""
    return {
        v: compute_weights(snet, edge_flows, profile_flows, variant_flow_filter(v))
        for v in VARIANTS
    }


def weighting_provenance(
    profile_flows: frozenset[str],
    weights_by_variant: dict[str, dict[str, TransitionWeights]],
) -> dict:
    """The tracked ``weighting`` block: regime one-liner + per-variant corpus
    facts, so the JSON is self-describing about what a weight means."""
    per_variant = {}
    for variant, tw in weights_by_variant.items():
        vf = variant_flow_filter(variant)
        eligible = sorted(profile_flows if vf is None else profile_flows & vf)
        undefined_places = sorted(
            {
                name.split("__to__")[0]
                for name, w in tw.items()
                if w.weight is None
            }
        )
        per_variant[variant] = {
            "n_profile_flows": len(eligible),
            "profile_flow_ids": eligible,
            "places_without_flow_backed_out_edges": undefined_places,
        }
    return {
        "definition": (
            "W-A flow-proportion (D3): weight = numerator / denominator, "
            "numerator = distinct profile flows contributing >=1 technique-"
            "edge under this tactic-pair, denominator = sum of numerators "
            "over the source place's retained inter-tactic out-transitions "
            "(out-edge-normalised; per-place out-weights sum to 1). "
            "flow_proportion = numerator / flows_leaving_source is the "
            "literal minuted per-flow proportion (sums to >1 where flows "
            "branch). Weights are workflow-recurrence under a survivorship-"
            "biased corpus - never efficacy, transition probability of an "
            "actor, or adversary optimality (metrics_semantics.md s(f))."
        ),
        "counts_flows_not_observation_count": True,
        "smoothing": "none",
        "primary_variant": PRIMARY_VARIANT,
        "variants": per_variant,
    }


__all__ = [
    "CLASSIFICATION_CSV",
    "PRIMARY_VARIANT",
    "VARIANTS",
    "TransitionWeights",
    "compute_all_variants",
    "compute_weights",
    "load_class_flows",
    "load_edge_flows",
    "profile_flow_sets",
    "variant_flow_filter",
    "weighting_provenance",
]
