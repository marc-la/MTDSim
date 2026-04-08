"""
Phase 2: Co-occurrence mining with tactic-ordering directionality.

Implements the core edge-derivation method of the Attack Graph Design
Schema v0.3 (Section 3.1, 5). Uses FP-Growth association rule mining
(via mlxtend) over the binary group + software usage matrix, then
assigns direction to each rule using canonical tactic ordering.
"""

from __future__ import annotations

import statistics
from typing import Iterable

import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

from mtdsim.attacker.gap.schema import (
    DependencyEdge,
    Evidence,
    TechniqueNode,
)


def build_usage_matrix(
    nodes: dict[str, TechniqueNode],
    index: dict,
) -> pd.DataFrame:
    """
    Build a binary (entity x technique) usage matrix.

    Rows are ATT&CK intrusion-sets and software (malware/tool) entries —
    the 115 groups + 484 software setup from Rahman et al. (2022).
    Columns are parent technique IDs.

    Parameters
    ----------
    nodes : dict[str, TechniqueNode]
        Output of ``parse_stix_bundle``.
    index : dict
        STIX bookkeeping also returned by ``parse_stix_bundle``.
    """
    stix_to_tid = index["stix_to_tid"]
    entity_stix_ids = set(index["group_ids"]) | set(index["software_ids"])

    # entity stix id -> set of technique ids it uses
    entity_techs: dict[str, set[str]] = {e: set() for e in entity_stix_ids}

    for source_ref, target_ref in index["relationships"]:
        if source_ref not in entity_stix_ids:
            continue
        tid = stix_to_tid.get(target_ref)
        if tid and tid in nodes:
            entity_techs[source_ref].add(tid)

    # Drop entities that use zero techniques
    entity_techs = {e: ts for e, ts in entity_techs.items() if ts}

    all_techs = sorted(nodes.keys())
    rows = []
    for entity, techs in entity_techs.items():
        rows.append({t: (t in techs) for t in all_techs})

    return pd.DataFrame(rows, index=list(entity_techs.keys()), columns=all_techs)


def mine_cooccurrence_edges(
    usage_matrix: pd.DataFrame,
    nodes: dict[str, TechniqueNode],
    min_support: float = 0.1,
    min_confidence: float = 0.6,
    confidence_filter: str = "median",
) -> tuple[list[DependencyEdge], list[tuple[str, str, float]], dict]:
    """
    Mine directed edges from a usage matrix via FP-Growth.

    Returns
    -------
    edges : list[DependencyEdge]
        Directed co-occurrence edges with tactic-ordering direction applied.
    intra_tactic_pairs : list[(tid_a, tid_b, confidence)]
        Rules where both techniques share the same tactic layer (unresolved).
    meta : dict
        ``{min_support, min_confidence, confidence_threshold, n_rules, n_rules_filtered}``
    """
    # FP-Growth expects boolean frame
    frame = usage_matrix.astype(bool)
    frequent = fpgrowth(frame, min_support=min_support, use_colnames=True)

    if frequent.empty:
        meta = {
            "min_support": min_support,
            "min_confidence": min_confidence,
            "confidence_threshold": 0.0,
            "n_rules": 0,
            "n_rules_filtered": 0,
        }
        return [], [], meta

    rules = association_rules(
        frequent, metric="confidence", min_threshold=min_confidence
    )

    # Keep only simple rules: single-item antecedent and single-item consequent
    simple_mask = (
        rules["antecedents"].apply(len) == 1
    ) & (rules["consequents"].apply(len) == 1)
    simple = rules[simple_mask].copy()

    if simple.empty:
        meta = {
            "min_support": min_support,
            "min_confidence": min_confidence,
            "confidence_threshold": 0.0,
            "n_rules": 0,
            "n_rules_filtered": 0,
        }
        return [], [], meta

    # Filter by confidence threshold (median by default, per Section 5)
    if confidence_filter == "median":
        threshold = float(statistics.median(simple["confidence"].tolist()))
    else:
        threshold = float(confidence_filter)

    filtered = simple[simple["confidence"] >= threshold]

    edges: list[DependencyEdge] = []
    intra_tactic: list[tuple[str, str, float]] = []
    seen: dict[tuple[str, str], DependencyEdge] = {}

    for _, row in filtered.iterrows():
        a = next(iter(row["antecedents"]))
        b = next(iter(row["consequents"]))
        if a == b or a not in nodes or b not in nodes:
            continue

        layer_a = nodes[a].tactic_layer
        layer_b = nodes[b].tactic_layer

        if layer_a < 0 or layer_b < 0:
            continue

        if layer_a < layer_b:
            src, tgt = a, b
        elif layer_a > layer_b:
            src, tgt = b, a  # reverse to respect tactic flow (Section 3.1 step 5)
        else:
            intra_tactic.append((a, b, float(row["confidence"])))
            continue

        key = (src, tgt)
        if key in seen:
            # Keep highest-confidence version
            if row["confidence"] > seen[key].confidence:
                seen[key].confidence = float(row["confidence"])
                seen[key].support = float(row["support"])
                seen[key].lift = float(row["lift"])
            continue

        edge = DependencyEdge(
            source_id=src,
            target_id=tgt,
            evidence_type="co_occurrence",
            confidence=float(row["confidence"]),
            support=float(row["support"]),
            lift=float(row["lift"]),
            evidence=[
                Evidence(
                    source_type="co_occurrence",
                    source_url="Rahman et al. (2022) arXiv:2211.06495",
                    description=(
                        f"FP-Growth rule: support={row['support']:.3f}, "
                        f"confidence={row['confidence']:.3f}, lift={row['lift']:.3f}"
                    ),
                )
            ],
            source_count=1,
            is_backward=False,  # direction was imposed by tactic ordering
        )
        seen[key] = edge
        edges.append(edge)

    meta = {
        "min_support": min_support,
        "min_confidence": min_confidence,
        "confidence_threshold": threshold,
        "n_rules": int(len(simple)),
        "n_rules_filtered": int(len(filtered)),
    }
    return edges, intra_tactic, meta
