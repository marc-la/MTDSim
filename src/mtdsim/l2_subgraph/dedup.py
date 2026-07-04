"""Operator deduplication of the flow corpus (Mitigation 1).

The corpus is not operator-uniform: 16 of the 38 flows belong to 8
multi-flow operator clusters (spec §(g),
``docs/notes/2026-05-28_l2_operator_aggregation_concern.md``). Mitigation 1
collapses each cluster to one representative — the flow with the highest
``n_actions`` in the audit CSV, tie-broken lexicographically — leaving the
**n = 29 operator-deduplicated corpus**. This module is the single source of
truth for that rule; the L2 JSD re-check (``tests/l2_subgraph/test_gasp.py``)
and the L3a weight build both consume it.

The clusters are hardcoded (rather than derived from the CSV ``attribution``
column) because the CISA AA22-138B cluster has no shared G-ID — its members
share an advisory, not an actor.
"""

from __future__ import annotations

import csv
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
AUDIT_CSV_PATH = _REPO_ROOT / "docs" / "notes" / "2026-05-28_l2_metadata_audit.csv"

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


def read_n_actions(audit_csv_path: Path = AUDIT_CSV_PATH) -> dict[str, int]:
    """``flow_id -> n_actions`` from the audit CSV (all 38 flows)."""
    out: dict[str, int] = {}
    with open(audit_csv_path) as f:
        for row in csv.DictReader(f):
            out[row["flow_id"]] = int(row["n_actions"])
    return out


def operator_deduplicated_flows(
    audit_csv_path: Path = AUDIT_CSV_PATH,
) -> frozenset[str]:
    """The n = 29 kept set: every flow outside a cluster, plus one
    representative per cluster (highest ``n_actions``; flow_id tie-break)."""
    n_actions = read_n_actions(audit_csv_path)
    drop: set[str] = set()
    for members in OPERATOR_CLUSTERS.values():
        ranked = sorted(members, key=lambda f: (-n_actions[f], f))
        drop.update(ranked[1:])
    return frozenset(n_actions) - drop


__all__ = [
    "AUDIT_CSV_PATH",
    "OPERATOR_CLUSTERS",
    "operator_deduplicated_flows",
    "read_n_actions",
]
