"""Classification + class-subgraph selection.

Two responsibilities, kept in one file since the collapsed scope keeps them
trivial:

- ``load_classification(audit_csv)`` — reads the audit CSV, applies the
  CSV ``stated_objective`` → spec class label remap (spec §c), returns
  ``flow_id → class_name``.
- ``OperationalObjectiveSelector(class_name).select(gap_dict, classification)``
  — computes the surface ``SubgraphView`` for the class per spec §(d).

The selector reads class membership from the audit-CSV-derived mapping and
the node-set from the GAP's per-node ``flow_ids`` (the spec's canonical
computation; equivalent to inverting the per-flow YAMLs, but cheaper).
"""

from __future__ import annotations

import csv
from pathlib import Path

from mtdsim.l2_subgraph.schema import CLASS_NAMES, SubgraphView

# CSV stated_objective → spec class label (spec §c).
CSV_LABEL_TO_CLASS = {
    "steal_data": "pure_steal",
    "impediment": "pure_impediment",
    "double_extortion": "double_extortion",
    "position_for_future": "infrastructure_setup",
}


def load_classification(audit_csv_path) -> dict[str, str]:
    """Return ``{flow_id: class_name}`` from the audit CSV.

    Raises ``ValueError`` on unknown ``stated_objective`` values — silent
    fallback would mask audit-CSV drift.
    """
    out: dict[str, str] = {}
    with open(audit_csv_path) as f:
        for row in csv.DictReader(f):
            raw = row["stated_objective"]
            if raw not in CSV_LABEL_TO_CLASS:
                raise ValueError(
                    f"unknown stated_objective {raw!r} for flow "
                    f"{row['flow_id']!r} in {audit_csv_path}"
                )
            out[row["flow_id"]] = CSV_LABEL_TO_CLASS[raw]
    return out


class OperationalObjectiveSelector:
    """``(gap, classification) → SubgraphView`` for one class.

    Surface subgraph (spec §d Decision 4): ``node_set`` is the union of
    techniques present in the class's flows; ``edge_set`` keeps GAP edges
    where both endpoints are in ``node_set``.
    """

    def __init__(self, class_name: str) -> None:
        if class_name not in CLASS_NAMES:
            raise ValueError(
                f"class_name must be one of {CLASS_NAMES}, got {class_name!r}"
            )
        self.class_name = class_name

    def select(
        self,
        gap: dict,
        classification: dict[str, str],
        *,
        provenance_extras: dict | None = None,
    ) -> SubgraphView:
        flow_ids = sorted(
            fid for fid, cls in classification.items() if cls == self.class_name
        )
        flow_set = set(flow_ids)
        node_set = frozenset(
            tid
            for tid, node in gap["nodes"].items()
            if any(fid in flow_set for fid in node["flow_ids"])
        )
        edge_set = frozenset(
            (e["source_id"], e["target_id"])
            for e in gap["edges"]
            if e["source_id"] in node_set and e["target_id"] in node_set
        )
        provenance = {
            "class_name": self.class_name,
            "flow_ids": flow_ids,
            "source_flow_count": len(flow_ids),
            "gap_version": gap.get("version"),
            "gap_build_date": gap.get("build_date"),
            **(provenance_extras or {}),
        }
        return SubgraphView(
            class_name=self.class_name,
            node_set=node_set,
            edge_set=edge_set,
            provenance=provenance,
        )
