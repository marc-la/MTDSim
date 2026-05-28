"""Top-level GASP build: GAP + audit CSV → 4 × SubgraphView + classification.csv.

Mirrors ``mtdsim.l1_construction.build``. Reads:

- ``data/gap/gap_v0.5.json`` (the L1 artefact),
- ``docs/notes/2026-05-28_l2_metadata_audit.csv`` (the load-bearing class-
  membership input — see spec §c).

Writes under ``data/gasp/``:

- ``classification.csv`` — flow_id, class_name (computed), plus ``metadata_confidence``
  carried through from the audit CSV.
- ``gasp_<class>.json`` × 4 — one ``SubgraphView`` per class.
"""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

from mtdsim.l2_subgraph.schema import CLASS_NAMES, SubgraphView
from mtdsim.l2_subgraph.selector import (
    CSV_LABEL_TO_CLASS,
    OperationalObjectiveSelector,
    load_classification,
)

_REPO_ROOT = Path(__file__).resolve().parents[3]
GAP_PATH = _REPO_ROOT / "data" / "gap" / "gap_v0.5.json"
AUDIT_CSV_PATH = _REPO_ROOT / "docs" / "notes" / "2026-05-28_l2_metadata_audit.csv"
GASP_OUT_DIR = _REPO_ROOT / "data" / "gasp"


def build_gasp(
    gap_path: Path = GAP_PATH,
    audit_csv_path: Path = AUDIT_CSV_PATH,
) -> dict[str, SubgraphView]:
    """Return ``{class_name: SubgraphView}`` for all four classes."""
    with open(gap_path) as f:
        gap = json.load(f)
    classification = load_classification(audit_csv_path)

    if set(classification) != {fid for n in gap["nodes"].values() for fid in n["flow_ids"]}:
        raise RuntimeError(
            "CSV ↔ GAP flow-set mismatch — re-run the L1 build or re-check the audit CSV"
        )

    extras = {
        "audit_csv_path": str(audit_csv_path.relative_to(_REPO_ROOT)),
        "gap_path": str(gap_path.relative_to(_REPO_ROOT)),
        "build_date": date.today().isoformat(),
    }
    return {
        cls: OperationalObjectiveSelector(cls).select(
            gap, classification, provenance_extras=extras
        )
        for cls in CLASS_NAMES
    }


def persist(views: dict[str, SubgraphView], out_dir: Path = GASP_OUT_DIR) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for cls, view in views.items():
        view.to_json(out_dir / f"gasp_{cls}.json")
    _persist_classification_csv(views, out_dir / "classification.csv")


def _persist_classification_csv(
    views: dict[str, SubgraphView], path: Path
) -> None:
    audit_rows = {}
    with open(AUDIT_CSV_PATH) as f:
        for row in csv.DictReader(f):
            audit_rows[row["flow_id"]] = row

    rows = []
    for cls, view in views.items():
        for fid in view.provenance["flow_ids"]:
            audit = audit_rows[fid]
            rows.append(
                {
                    "flow_id": fid,
                    "class_name": cls,
                    "metadata_confidence": audit["metadata_confidence"],
                    "attribution": audit["attribution"],
                }
            )
    rows.sort(key=lambda r: (r["class_name"], r["flow_id"]))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "flow_id",
                "class_name",
                "metadata_confidence",
                "attribution",
            ],
        )
        w.writeheader()
        w.writerows(rows)


__all__ = ["build_gasp", "persist", "GAP_PATH", "AUDIT_CSV_PATH", "GASP_OUT_DIR"]
