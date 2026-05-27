#!/usr/bin/env python3
"""Build the L1 GAP artefacts from the acquired corpus.

Reads the gitignored inputs (run ``scripts/fetch_gap_corpus.py`` first), writes
the committed per-flow extracts + aggregate GAP, and prints a sanity summary.

Usage::

    PYTHONPATH=src python scripts/build_gap.py [--corpus DIR] [--attack FILE]
                                               [--flows-out DIR] [--gap-out FILE]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from mtdsim.attacker.gap.build import (  # noqa: E402
    CORPUS_STIX_DIR,
    FLOWS_OUT_DIR,
    GAP_OUT_PATH,
    build_gap,
    persist_extracts,
    persist_gap,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", default=CORPUS_STIX_DIR, help="dir of flow STIX bundles")
    ap.add_argument("--attack", default=None, help="ATT&CK enterprise STIX bundle")
    ap.add_argument("--flows-out", default=FLOWS_OUT_DIR)
    ap.add_argument("--gap-out", default=GAP_OUT_PATH)
    args = ap.parse_args()

    extracts, gap = build_gap(args.corpus, args.attack)
    persist_extracts(extracts, args.flows_out)
    persist_gap(gap, args.gap_out)

    hist: dict[int, int] = {}
    for e in gap.edges:
        hist[e.observation_count] = hist.get(e.observation_count, 0) + 1
    print(
        f"GAP v{gap.version} built from {gap.source_flow_count} flows\n"
        f"  nodes={gap.node_count}  edges={gap.edge_count}  "
        f"entries={len(gap.entry_nodes)}  objectives={len(gap.objective_nodes)}\n"
        f"  observation_count histogram: {dict(sorted(hist.items()))}\n"
        f"  -> {args.flows_out}/ ({len(extracts)} per-flow extracts)\n"
        f"  -> {args.gap_out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
