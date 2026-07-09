"""CLI for the timeline runner — ``python -m mtdsim.l3_simulation.timeline``.

Generates the full seeded timeline library over the run matrix (bulk JSONL +
manifest under the gitignored ``data/ogasp/_timelines/``), refreshes the
committed example (``timeline_example.jsonl``) and writes the behavioural
verification report (``timeline_report.md`` / ``.json``). Fully deterministic
— rerunning reproduces every byte.
"""

from __future__ import annotations

import sys

from mtdsim.l3_simulation.timeline.matrix import TIMELINES_DIR, generate_library
from mtdsim.l3_simulation.timeline.report import (
    build_report,
    write_example,
    write_report_md,
)


def main() -> int:
    manifest, library = generate_library()
    n_cells = len(manifest["cells"])
    n_runs = sum(c["n_runs"] for c in manifest["cells"])
    print(f"  timeline library: {n_cells} cells, {n_runs} runs -> {TIMELINES_DIR}/")
    for arm in manifest["impossible_arms"]:
        print(
            f"  recon arm impossible: {arm['profile']} "
            "(prefix gap; recorded, not skipped)"
        )
    report = build_report(manifest, library)
    example = write_example(library)
    report_md = write_report_md(report)
    order = report["orderings_by_median_net_time_to_objective"]["central"]
    print(f"  median net time-to-objective ranking (primary cell): {' < '.join(order)}")
    print(
        "  ranking survives sweep extremes: "
        f"{report['ordering_stable_across_sweep_extremes']}; "
        f"weighted vs uniform stable: {report['ordering_stable_weighted_vs_uniform']}; "
        f"dedup vs raw stable: {report['ordering_stable_dedup_vs_raw']}"
    )
    print(f"  -> {report_md} (+ .json); example: {example}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
