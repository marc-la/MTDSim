"""CLI for the L3a weighted Petri nets — ``python -m mtdsim.l3_simulation.petri``.

Builds the five profile nets (four GASP classes + the aggregate null profile)
from ``data/gap/gap_v0.5.json`` + the four ``data/gasp/gasp_<class>.json``,
computes the W-A flow-proportion weight layer (operator-dedup primary, raw
robustness), emits the structural report per profile, writes the tracked
JSONs + divergence-from-aggregate report + README under ``data/ogasp/petri/``,
and renders the figures to ``data/ogasp/petri/_viz/``.
"""

from __future__ import annotations

import sys

from mtdsim.l3_simulation.petri.analysis import analyse
from mtdsim.l3_simulation.petri.build import (
    PROFILE_NAMES,
    build_all_profiles,
    load_gap_index,
    load_profile_view,
)
from mtdsim.l3_simulation.petri.divergence import build_divergence_report
from mtdsim.l3_simulation.petri.prefix_join import (
    apply_prefix_join,
    write_overlay,
)
from mtdsim.l3_simulation.petri.render import (
    PETRI_DIR,
    VIZ_DIR,
    draw_net,
    persist_summary,
    write_divergence_report_md,
    write_readme,
)
from mtdsim.l3_simulation.petri.viz import (
    load_tactic_layers,
    render_reachability_chart,
    render_tactic_state_diagram,
)
from mtdsim.l3_simulation.petri.weights import (
    PRIMARY_VARIANT,
    compute_all_variants,
    load_edge_flows,
    profile_flow_sets,
    weighting_provenance,
)
from mtdsim.l2_subgraph.dedup import operator_deduplicated_flows


def main() -> int:
    gap = load_gap_index()
    tactic_layers = load_tactic_layers()
    # Observed-only: the *_structural.json record and every analysis below are
    # the observed corpus's; the M6 overlay is emitted as its own artefact.
    nets = build_all_profiles(with_prefix_join=False)
    edge_flows = load_edge_flows()
    profile_flows = profile_flow_sets()
    dedup_kept = operator_deduplicated_flows()

    reports = {}
    weights = {}
    for profile in PROFILE_NAMES:
        snet = nets[profile]
        view = load_profile_view(profile)
        report = analyse(snet, view, gap)
        w = compute_all_variants(snet, edge_flows, profile_flows[profile])
        reports[profile] = report
        weights[profile] = w
        persist_summary(
            snet,
            report,
            weights_by_variant=w,
            weighting=weighting_provenance(profile_flows[profile], w),
        )
        render_tactic_state_diagram(
            snet, report, view, gap, tactic_layers, VIZ_DIR,
            weights=w[PRIMARY_VARIANT],
        )
        draw_net(snet)  # formal SNAKES net (provenance artefact)
        n_supported = sum(
            1 for tw in w[PRIMARY_VARIANT].values() if tw.weight
        )
        prefix = (
            "recon→IA bridged"
            if report.prefix_gap.recon_reaches_initial_access
            else "recon→IA DISCONNECTED"
        )
        print(
            f"  {profile:<22} {report.n_places:>3} places  "
            f"{report.n_transitions:>3} transitions  "
            f"({n_supported} weight-supported on dedup; seed={snet.entry_tactic}; {prefix})"
        )

    joined = {p: apply_prefix_join(s) for p, s in nets.items()}
    overlay = write_overlay(joined)
    n_joined = sum(1 for s in joined.values() if s.synthetic_transitions)
    print(
        f"  M6 prefix-join overlay: {n_joined} profile(s) bridged "
        f"synthetically -> {overlay.name}"
    )

    div = build_divergence_report(
        nets, reports, weights, edge_flows, gap, profile_flows, dedup_kept
    )
    report_md = write_divergence_report_md(div)
    chart = render_reachability_chart(reports, VIZ_DIR / "_reachability.png")
    write_readme(reports, div)
    for cls, ok in div.exceeds_null_p95.items():
        print(
            f"  JSD vs aggregate: {cls:<22} {div.mean_jsd[cls]:.4f} "
            f"(null p95 {div.null_band[cls]['p95']:.4f}) -> "
            f"{'exceeds' if ok else 'below'}"
        )
    print(f"  -> {PETRI_DIR}/ ({report_md.name}; _viz/ diagrams; headline: {chart.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
