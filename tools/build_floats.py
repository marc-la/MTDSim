"""Regenerate every generated figure and table in the dissertation.

Each entry below is one generator command and the float files it writes under
docs/thesis/. Inputs are committed files only (data/, experiments/*/numbers*.json)
plus the ATT&CK bundle that ``python -m mtdsim.l0_cti`` fetches. No simulation
runs here; the raw runs are summarised by the experiments' analysers first.

    python tools/build_floats.py            # every float (~10 min)
    python tools/build_floats.py --list     # the float -> command table
    python tools/build_floats.py --only tab_5-4a fig_5-3-2b

Needs: the [figures] extra (Playwright + ``playwright install chromium``,
CairoSVG), pdflatex, and Ghostscript. Tables 4.5 and 5.1 and ten inline tables
are typed in dissertation.tex and have no generator.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# (float files written, command). Order follows the dissertation.
FLOATS: list[tuple[tuple[str, ...], list[str]]] = [
    (("fig_2-2a", "fig_2-2-1a", "fig_2-2-3a"), ["tools/ch2_model_figures.py"]),
    (("tab_2-2b",), ["tools/ch2_lineage_configurations_table.py"]),
    (("fig_3-1-2a",), ["tools/attack_matrix_figure.py"]),
    (("fig_3-1-3a",), ["tools/attack_flow_figure.py"]),
    (("fig_4-0a",), ["tools/ch4_overview_figure.py"]),
    (("fig_4-1a",), ["tools/ch4_attack_graph_figure.py"]),
    (("fig_4-2b",), ["tools/ch4_profile_reach_figure.py"]),
    (("fig_4-3a",), ["tools/gspn_gadget_figure.py"]),
    (("fig_4-4c",), ["tools/runtime_loop_figure.py"]),
    (("fig_4-4a",), ["tools/controller_mapping_figure.py"]),
    (("tab_4-4a",), ["tools/dwell_catalogue_tables.py"]),
    (("fig_5-2-1a", "tab_5-2-1a"), ["tools/ch5_unopposed_figures.py"]),
    (("fig_5-2-2a", "tab_5-3-1b"), ["tools/ch5_disruption_figure.py"]),
    (("fig_5-3-2b", "tab_5-3-2d", "fig_5-3-3b", "fig_F-0b", "tab_F-0a", "tab_F-0c", "tab_F-0d"),
     ["tools/ch5_sweep_figures.py"]),
    (("tab_5-4a", "tab_F-4"), ["experiments/ch5_defended/ablation_table.py"]),
    (("tab_B-2a",), ["tools/gasp_structural_baseline.py", "--tex"]),
    (("fig_B-1c",), ["tools/gap_appendix_figures.py", "--only", "gap_technique_core"]),
    (("fig_4-2a",), ["tools/ch4_attack_profiles_figure.py"]),
    (("tab_B-4b",), ["tools/attack_action_times_table.py"]),
    (("tab_B-6a",), ["tools/failure_weight_decomposition_figure.py", "--layout", "tables"]),
    (("tab_C-0b",), ["tools/value_bases_table.py"]),
    (("tab_C-1a",), ["experiments/ch5_s51_sensitivity/analyse.py", "--tables-only"]),
    (("tab_C-1b",), ["tools/duration_ranking_table.py"]),
    (("tab_F-2",), ["experiments/ch5_defended/memory_ablation.py", "--table-only"]),
    (("tab_F-3",), ["experiments/ch5_defended/partition_ablation.py"]),  # TABLE_ONLY=1, below
    (("tab_FA-8",), ["tools/further_analyses_tables.py"]),
]
ENV = {"TABLE_ONLY": "1", "CORPUS": "reported"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="print the float -> command table and exit")
    ap.add_argument("--only", nargs="*", metavar="STEM", help="float stems to build (default: all)")
    args = ap.parse_args()

    if args.list:
        for floats, cmd in FLOATS:
            print(f"{', '.join(floats):58s} python {' '.join(cmd)}")
        return 0

    env = {**os.environ, **ENV,
           "PYTHONPATH": os.pathsep.join([str(REPO / "src"), str(REPO / "tools")]),
           # pin PDF timestamps so a rebuild of an unchanged figure is byte-stable
           "SOURCE_DATE_EPOCH": os.environ.get("SOURCE_DATE_EPOCH", "1760745600"),
           "FORCE_SOURCE_DATE": "1"}
    jobs = [(f, c) for f, c in FLOATS if not args.only or set(f) & set(args.only)]
    failed = []
    for floats, cmd in jobs:
        t0 = time.time()
        r = subprocess.run([sys.executable, *cmd], cwd=REPO, env=env,
                           capture_output=True, text=True)
        status = "ok" if r.returncode == 0 else f"FAILED ({r.returncode})"
        print(f"{status:12s} {time.time() - t0:6.1f}s  {', '.join(floats)}", flush=True)
        if r.returncode:
            failed.append(floats)
            print((r.stdout + r.stderr)[-2000:], file=sys.stderr)
    print(f"{len(jobs) - len(failed)} of {len(jobs)} generators ok")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
