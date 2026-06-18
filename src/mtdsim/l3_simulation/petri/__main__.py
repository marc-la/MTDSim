"""CLI for the L3a structural Petri nets — ``python -m mtdsim.l3_simulation.petri``.

Builds all four class nets from ``data/gap/gap_v0.5.json`` + the four
``data/gasp/gasp_<class>.json``, emits the structural report per class, renders
the figures to ``data/ogasp/_viz/`` (a legible tactic-state diagram + the formal
SNAKES net per class, and the cross-class reachability headline chart), and
writes the tracked summary JSONs + README under ``data/ogasp/``.
"""

from __future__ import annotations

import sys

from mtdsim.l3_simulation.petri.analysis import analyse
from mtdsim.l3_simulation.petri.build import CLASS_NAMES, build_all, load_gap_index, load_gasp_view
from mtdsim.l3_simulation.petri.render import OGASP_DIR, VIZ_DIR, draw_net, persist_summary, write_readme
from mtdsim.l3_simulation.petri.viz import (
    load_tactic_layers,
    render_reachability_chart,
    render_tactic_state_diagram,
)


def main() -> int:
    gap = load_gap_index()
    tactic_layers = load_tactic_layers()
    nets = build_all()
    reports = {}
    for cls in CLASS_NAMES:
        snet = nets[cls]
        view = load_gasp_view(cls)
        report = analyse(snet, view, gap)
        reports[cls] = report
        persist_summary(snet, report)
        render_tactic_state_diagram(snet, report, view, gap, tactic_layers, VIZ_DIR)
        draw_net(snet)  # formal SNAKES net (provenance artefact)
        prefix = (
            "recon→IA bridged"
            if report.prefix_gap.recon_reaches_initial_access
            else "recon→IA DISCONNECTED"
        )
        obj = (
            "objective reachable from recon"
            if report.all_objectives_reachable_from_entry
            else (
                "objective partially reachable from recon"
                if report.any_objective_reachable_from_entry
                else "objective NOT reachable from recon"
            )
        )
        print(
            f"  {cls:<22} {report.n_places:>3} places  "
            f"{report.n_transitions:>3} transitions  "
            f"{report.n_inter_tactic_edges:>3} edges  "
            f"(seed={snet.entry_tactic}; {obj}; {prefix})"
        )
    chart = render_reachability_chart(reports, VIZ_DIR / "_reachability.png")
    write_readme(reports)
    print(f"  -> {OGASP_DIR}/ (+ _viz/ diagrams; headline: {chart.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
