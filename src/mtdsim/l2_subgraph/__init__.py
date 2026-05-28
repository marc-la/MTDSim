"""L2 — GASP (operational-objective-conditioned APT Profile).

Canonical spec: [`docs/specs/02_gasp_schema.md`](../../../docs/specs/02_gasp_schema.md).
Construction is a deterministic function of the L1 GAP plus the audit-traced
class-membership CSV at
``docs/notes/2026-05-28_l2_metadata_audit.csv``.
"""

from mtdsim.l2_subgraph.schema import CLASS_NAMES, SubgraphView
from mtdsim.l2_subgraph.selector import (
    CSV_LABEL_TO_CLASS,
    OperationalObjectiveSelector,
    load_classification,
)

__all__ = [
    "CLASS_NAMES",
    "CSV_LABEL_TO_CLASS",
    "OperationalObjectiveSelector",
    "SubgraphView",
    "load_classification",
]
