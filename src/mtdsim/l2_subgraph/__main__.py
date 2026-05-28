"""CLI for L2 GASP construction — ``python -m mtdsim.l2_subgraph``.

Reads ``data/gap/gap_v0.5.json`` + ``docs/notes/2026-05-28_l2_metadata_audit.csv``,
writes ``data/gasp/classification.csv`` + ``data/gasp/gasp_<class>.json`` × 4.
"""

from __future__ import annotations

import sys

from mtdsim.l2_subgraph.build import GASP_OUT_DIR, build_gasp, persist


def main() -> int:
    views = build_gasp()
    persist(views)
    for cls, view in views.items():
        print(
            f"  {cls:<22} {len(view.node_set):>3} nodes  "
            f"{len(view.edge_set):>3} edges  "
            f"({view.provenance['source_flow_count']} flows)"
        )
    print(f"  -> {GASP_OUT_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
