"""Persist the L3a nets: structural + weighted JSONs, the divergence report,
diagrams, and the ``data/ogasp/`` README.

Diagrams go to ``data/ogasp/_viz/`` (gitignored, regenerable). The summary
JSONs, the divergence report and the README under ``data/ogasp/`` are tracked
-- they are the structural + weight record (places, transitions, W-A weights
with full provenance, reachability, objective-reachability, prefix gap,
divergence-from-aggregate).
"""

from __future__ import annotations

import json
from pathlib import Path

from mtdsim.l3_simulation.petri.analysis import StructuralReport
from mtdsim.l3_simulation.petri.build import (
    AGGREGATE,
    CLASS_NAMES,
    StructuralNet,
)
from mtdsim.l3_simulation.petri.divergence import DivergenceReport
from mtdsim.l3_simulation.petri.weights import TransitionWeights

_REPO_ROOT = Path(__file__).resolve().parents[4]
OGASP_DIR = _REPO_ROOT / "data" / "ogasp"
VIZ_DIR = OGASP_DIR / "_viz"


def draw_net(snet: StructuralNet, viz_dir: Path = VIZ_DIR) -> Path:
    """Render the *formal* SNAKES net to ``_viz/<class>_snakes.png``.

    This is the faithful bipartite Petri object (places + transition bars), kept
    as a provenance artefact; the legible, idea-conveying figure is the
    tactic-state diagram in ``viz.render_tactic_state_diagram`` (``<class>.png``).
    Needs the graphviz ``dot`` binary on PATH (the ``gv`` plugin is loaded in
    ``build``)."""
    viz_dir = Path(viz_dir)
    viz_dir.mkdir(parents=True, exist_ok=True)
    out = viz_dir / f"{snet.class_name}_snakes.png"
    snet.net.draw(str(out))
    return out


def persist_summary(
    snet: StructuralNet,
    report: StructuralReport,
    weights_by_variant: dict[str, dict[str, TransitionWeights]] | None = None,
    weighting: dict | None = None,
    out_dir: Path = OGASP_DIR,
) -> Path:
    """Write ``data/ogasp/<profile>_structural.json`` -- the net shape + its
    structural report, every transition's GASP provenance inline, and (when
    provided) the W-A weight layer per transition per corpus variant."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "class_name": snet.class_name,
        "provenance": snet.provenance,
        "places": list(snet.tactics),
        "entry_marking": snet.entry_tactic,
        "transitions": [
            {
                "name": t.name,
                "src_tactic": t.src_tactic,
                "dst_tactic": t.dst_tactic,
                "gasp_edges": [list(e) for e in t.edges],
                **(
                    {
                        "weights": {
                            variant: tw[t.name].to_dict()
                            for variant, tw in weights_by_variant.items()
                        }
                    }
                    if weights_by_variant
                    else {}
                ),
            }
            for t in snet.transitions
        ],
        "report": report.to_dict(),
    }
    if weighting is not None:
        payload["weighting"] = weighting
    out = out_dir / f"{snet.class_name}_structural.json"
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return out


def _fmt_path(pr) -> str:
    if not pr.reachable:
        return "—"
    return f"{pr.n_hops} hops ({pr.entry} → {pr.objective})"


def write_divergence_report_md(
    div: DivergenceReport, out_dir: Path = OGASP_DIR
) -> Path:
    """Write ``data/ogasp/divergence_report.md`` — the human-readable half of
    the divergence-from-aggregate verification (numbers also persisted to
    ``divergence_report.json`` for the test gate)."""
    out_dir = Path(out_dir)
    lines = [
        "# Divergence-from-aggregate report — do the four class envelopes "
        "differ from the null profile?",
        "",
        "The structural half of the profile-discrimination verification (the",
        "behavioural half is the timeline runner's). Weights are the W-A",
        "flow-proportion layer (D3): out-edge-normalised distinct-flow counts",
        "on the **operator-deduplicated corpus (n = 29)** as primary, raw",
        "(n = 38) as the robustness column. JSD convention matches the L2 gate:",
        "`scipy jensenshannon(p, q, base=2) ** 2` (divergence in [0, 1]),",
        "per comparable place (a place where both nets have a flow-backed",
        "out-distribution), summarised as the unweighted mean per class.",
        "",
        "**Reading frame (metrics_semantics.md §(f)):** weights are",
        "workflow-recurrence over a survivorship-biased corpus. Each class net",
        "is a behavioural **envelope** for an operational objective — never an",
        "actor's policy, never step efficacy, never adversary optimality. Every",
        "claim below is envelope-relative.",
        "",
        "**Recorded tradeoff (accepted mechanism, not a defect):** aggregating",
        "techniques → tactics is precisely what makes these weights groundable",
        "at ~38 flows, and it **loses AND-gate/join structure** — the",
        "technique-level operator/join metadata stays in the GAP, untouched.",
        "",
        "## Divergence vs the shuffled-class-label null",
        "",
        f"Null: {div.null_trials} trials (seed {div.null_seed}); flows",
        "reassigned to the four labels at random with class sizes preserved on",
        "the deduplicated corpus; each trial's per-class quotient is scored",
        "against the fixed aggregate exactly as the observed classes are.",
        "",
        "| Class | flows (raw → dedup) | mean JSD vs aggregate (dedup) | raw robustness | null p50 | null p95 | exceeds null p95? |",
        "|---|---|--:|--:|--:|--:|---|",
    ]
    for cls in CLASS_NAMES:
        nf = div.n_flows[cls]
        nb = div.null_band[cls]
        verdict = "**yes**" if div.exceeds_null_p95[cls] else "**no**"
        lines.append(
            f"| `{cls}` | {nf['raw']} → {nf['operator_dedup']} | "
            f"{div.mean_jsd[cls]:.4f} | {div.mean_jsd_raw[cls]:.4f} | "
            f"{nb['p50']:.4f} | {nb['p95']:.4f} | {verdict} |"
        )
    agg_nf = div.n_flows[AGGREGATE]
    lines += [
        "",
        f"Aggregate (null profile): {agg_nf['raw']} → "
        f"{agg_nf['operator_dedup']} flows; its dedup-vs-raw self-divergence "
        f"is mean JSD **{div.aggregate_dedup_vs_raw_jsd:.4f}** (robustness of "
        "the null profile to the dedup discipline).",
        "",
        "## Per-place JSD vs the aggregate (dedup primary)",
        "",
    ]
    places = sorted({p for m in div.per_place_jsd.values() for p in m})
    header = "| Place | " + " | ".join(f"`{c}`" for c in CLASS_NAMES) + " |"
    lines += [header, "|---|" + "--:|" * len(CLASS_NAMES)]
    for place in places:
        row = [f"| {place} "]
        for cls in CLASS_NAMES:
            v = div.per_place_jsd[cls].get(place)
            row.append(f"| {v:.4f} " if v is not None else "| — ")
        lines.append("".join(row) + "|")
    lines += [
        "",
        "A `—` means the place has no flow-backed out-distribution in that",
        "class on the deduplicated corpus (thinness left visible, per D9).",
        "",
        "## Weighted structural discriminators (positive-weight support, dedup)",
        "",
        "Computed over the transitions a weighted traversal can actually take",
        "(primary weight > 0). Zero-weight structural transitions are retained",
        "in the nets; they are excluded from these statistics only.",
        "",
        "| Profile | supported / total transitions | reach from recon seed | reach from initial-access | objective from IA | shortest entry→obj | longest entry→obj | branching | distinct entry→obj paths | sinks | islands |",
        "|---|---|--:|--:|---|---|---|--:|--:|---|---|",
    ]
    for profile, d in div.discriminators.items():
        obj = ", ".join(
            f"{o}: {'yes' if ok else 'no'}"
            for o, ok in d.objective_reachable_from_initial_access.items()
        )
        lines.append(
            f"| `{profile}` | {d.n_supported_transitions} / {d.n_transitions} | "
            f"{len(d.reachable_from_recon_seed)} | "
            f"{len(d.reachable_from_initial_access)} | {obj} | "
            f"{_fmt_path(d.shortest_entry_to_objective)} | "
            f"{_fmt_path(d.longest_entry_to_objective)} | "
            f"{d.branching_factor:.2f} | "
            f"{d.distinct_entry_to_objective_paths:,} | "
            f"{', '.join(d.sink_places) or '—'} | "
            f"{', '.join(d.island_places) or '—'} |"
        )

    exceed = [c for c in CLASS_NAMES if div.exceeds_null_p95[c]]
    below = [c for c in CLASS_NAMES if not div.exceeds_null_p95[c]]
    verdict = [
        "",
        "## Verdict",
        "",
    ]
    if len(exceed) == len(CLASS_NAMES):
        verdict.append(
            "All four class envelopes diverge from the aggregate beyond the "
            "shuffled-label null p95: the weighted out-distributions carry "
            "class-conditioned structure that random class assignment does "
            "not reproduce. "
        )
    elif exceed:
        verdict.append(
            f"{', '.join('`%s`' % c for c in exceed)} diverge(s) from the "
            f"aggregate beyond the shuffled-label null p95; "
            f"{', '.join('`%s`' % c for c in below)} do(es) not — for the "
            "latter, the observed divergence from the aggregate is within "
            "what class-size-matched random flow assignment produces, so the "
            "structural signal alone does not separate that envelope from "
            "the null at this corpus size. "
        )
    else:
        verdict.append(
            "No class envelope diverges from the aggregate beyond the "
            "shuffled-label null p95 — the structural weight layer alone "
            "does not discriminate the envelopes at this corpus size; the "
            "behavioural (timeline-runner) half of the verification carries "
            "the question. "
        )
    verdict += [
        "Where a class's mean JSD sits relative to its null band is the",
        "class-size-honest reading: smaller classes (4 flows deduplicated)",
        "have wider null bands, so an identical JSD magnitude is weaker",
        "evidence for them — the table reports the bands rather than a single",
        "pooled threshold. The dedup-vs-raw robustness column and the",
        "aggregate's self-divergence bound how much the operator-dedup",
        "discipline itself moves the numbers.",
        "",
    ]
    lines += verdict

    out = out_dir / "divergence_report.md"
    out.write_text("\n".join(lines) + "\n")
    with open(out_dir / "divergence_report.json", "w") as f:
        json.dump(div.to_dict(), f, indent=2, ensure_ascii=False)
        f.write("\n")
    return out


def write_readme(
    reports: dict[str, StructuralReport],
    div: DivergenceReport,
    out_dir: Path = OGASP_DIR,
) -> Path:
    """Write ``data/ogasp/README.md`` -- what the artefacts are, how to rebuild,
    the weighting regime, and the headline structural findings."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# `data/ogasp/` — L3a OGASP weighted tactic-place Petri nets",
        "",
        "Five **weighted** structural tactic-place Petri nets — one per GASP",
        "class plus the **aggregate (null) profile** over the union of all",
        "flows — built in SNAKES with a single moving black token. Shape +",
        "W-A flow-proportion weights; no timing, rewards, MTD or CTMC (those",
        "are later stages). Stages 1–2 (L3a) of the OGASP Petri-net",
        "workstream.",
        "",
        "- **Build code:** [`src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri).",
        "- **Design / rationale:** [`docs/notes/2026-06-18_l3_petri_feasibility.md`](../../docs/notes/2026-06-18_l3_petri_feasibility.md)",
        "  (the base structural net is GO-unconditional, sec.8).",
        "- **Locked P/T/F/M mapping:** places = ATT&CK tactics; transitions =",
        "  inter-tactic tactic-pairs (each tracing to >=1 GASP technique-edge — the",
        "  no-synthesis invariant); flow = `place[a] -> T -> place[b]`; marking =",
        "  one black token in `reconnaissance` (else `initial-access`).",
        "- **Weight regime (D3, dispositioned in",
        "  [`docs/specs/metrics_semantics.md`](../../docs/specs/metrics_semantics.md) §(f)):**",
        "  per transition and corpus variant, `weight = numerator / denominator`",
        "  where the numerator counts **distinct attack flows** contributing >=1",
        "  technique-edge under the tactic-pair and the denominator sums the",
        "  numerators over the source place's out-transitions — the",
        "  out-edge-normalised flow proportion; per-place out-weights sum to 1.",
        "  The literal minuted per-flow proportion (`flow_proportion` =",
        "  numerator / `flows_leaving_source`) is stored beside it; where flows",
        "  branch it sums to >1 across a place, which is why the normalised",
        "  form is the routing weight. Raw numerators/denominators and backing",
        "  flow IDs stay inline so the thinness is visible (D9). Two variants",
        "  per net: `operator_dedup` (primary, n = 29 — the §(g) Mitigation-1",
        "  rule, one representative per operator cluster) and `raw` (n = 38,",
        "  robustness). `observation_count` is never normalised or consumed.",
        "  No smoothing. **Weights are workflow-recurrence, never efficacy or",
        "  actor-likelihood** — each net is a class **envelope**, and",
        "  tactic-level aggregation deliberately trades away AND-gate/join",
        "  structure for groundable weights (recorded tradeoff).",
        "",
        "## Rebuild",
        "",
        "```sh",
        "pip install snakes                 # not in environment.yml; needs graphviz `dot` for diagrams",
        "PYTHONPATH=src python -m mtdsim.l3_simulation.petri   # write <profile>_structural.json x5 + divergence report + _viz/",
        "PYTHONPATH=src python -m mtdsim.l3_simulation.timeline # seeded timeline library + example + behavioural report",
        "PYTHONPATH=src python -m pytest tests/l3_simulation/  # validation gate",
        "```",
        "",
        "## Contents",
        "",
        "| Path | Tracked? | What |",
        "|---|---|---|",
        "| `<class>_structural.json` × 4 | **computed** | net shape (places, transitions + per-transition GASP provenance) + W-A weight layer (both corpus variants, backing flow IDs) + structural report |",
        "| `aggregate_structural.json` | **computed** | the fifth (null) net over the union of all flows — same shape and weight layer |",
        "| `divergence_report.md` / `.json` | **computed** | class-vs-aggregate per-place JSD, weighted discriminators, shuffled-label null, verdict |",
        "| `_viz/<profile>.png` / `.svg` | gitignored | **tactic-state diagram** — kill-chain L→R; token in its seed; entry green, objective orange, sinks double-outlined; edge width/opacity = W-A weight (uniform absolute scale across the five nets); unreachable-from-token places dashed |",
        "| `_viz/<profile>_snakes.png` | gitignored | the **formal SNAKES net** (bipartite places + transition bars) — faithful but dense; kept as a provenance artefact |",
        "| `_viz/_reachability.png` | gitignored | **headline chart** — tactics reachable from the recon token vs from any entry, per profile |",
        "| `timeline_schema.md` | **committed** | the timeline-runner artefact contract (`ogasp-timeline/v1`): record schema, declared walk semantics, run matrix |",
        "| `timeline_example.jsonl` | **committed** | the shortest committed timeline of each outcome kind (objective / stalled / cap) — the contract's living companion |",
        "| `timeline_report.md` / `.json` | **computed** | behavioural verification report — per-cell summary stats, class-vs-aggregate comparison, verdict (the behavioural half of the divergence question) |",
        "| `_timelines/<cell>.jsonl` + `manifest.json` | gitignored | the seeded timeline library over the full run matrix — regenerable via `python -m mtdsim.l3_simulation.timeline` |",
        "",
        "All `_viz/` figures are gitignored (regenerable; mirrors the `data/gasp/_*`",
        "pattern). The diagrams need graphviz `dot` + the `graphviz` Python package;",
        "the headline chart needs `matplotlib` (both house dependencies of",
        "`data/gasp/_viz/gasp_viz.py`).",
        "",
        "## Structural summary",
        "",
        "| Profile | Flows (raw → dedup) | Places | Transitions | Inter-tactic edges | Self-loops dropped | Objective reachable from recon | recon→initial-access |",
        "|---|---|--:|--:|--:|--:|---|---|",
    ]
    for cls, r in reports.items():
        obj_reach = (
            "yes"
            if r.all_objectives_reachable_from_entry
            else ("partial" if r.any_objective_reachable_from_entry else "**no**")
        )
        prefix = (
            "bridged"
            if r.prefix_gap.recon_reaches_initial_access
            else "**disconnected**"
        )
        nf = div.n_flows[cls]
        lines.append(
            f"| `{cls}` | {nf['raw']} → {nf['operator_dedup']} | "
            f"{r.n_places} | {r.n_transitions} | "
            f"{r.n_inter_tactic_edges} | {r.n_intra_tactic_selfloops_dropped} | "
            f"{obj_reach} | {prefix} |"
        )

    lines += [
        "",
        "The aggregate's declared objective set is the union of the four",
        "class-semantic objectives (command-and-control, exfiltration, impact)",
        "— a recorded choice; the null envelope has no single operational",
        "objective. Note the operator clusters span classes (e.g. the CISA",
        "AA22-138B trio splits across `pure_steal` and `infrastructure_setup`),",
        "so deduplication can remove flows from several classes at once —",
        "dedup class sizes are 14 / 7 / 4 / 4 (Σ = 29).",
        "",
        "## Divergence from the aggregate (headline)",
        "",
    ]
    for cls in CLASS_NAMES:
        nb = div.null_band[cls]
        v = "exceeds" if div.exceeds_null_p95[cls] else "does NOT exceed"
        lines.append(
            f"- **{cls}** — mean per-place JSD {div.mean_jsd[cls]:.4f} vs "
            f"aggregate; {v} the shuffled-label null p95 ({nb['p95']:.4f})."
        )
    lines += [
        "",
        "Full tables, discriminators and the verdict paragraph:",
        "[`divergence_report.md`](divergence_report.md).",
        "",
        "## The prefix gap (inspect-the-base finding)",
        "",
        "The marking seeds the token in `reconnaissance`. On the observed-only",
        "base the corpus starts at the point of detection, so the",
        "`reconnaissance → initial-access` link is near-absent — and it shows up",
        "directly in the single-token reachability:",
        "",
    ]
    for cls, r in reports.items():
        lines.append(f"- **{cls}** — {r.prefix_gap.interpretation}")
    lines += [
        "",
        "Consequence: in the classes where recon is an island, a recon-seeded",
        "token cannot reach the objective; seeding at `initial-access` (the",
        "corpus's dominant real entry) is required. Whether to add the",
        "literature-grounded `recon → initial-access` inferred prefix bridge",
        "(GAP Decision 6 Option B) is a deferred decision — the weighted nets",
        "stay observed-only. See the feasibility study sec.4 / sec.9.",
        "",
        "In-tactic dwell is the duration catalogue's job",
        "(`tactic_durations.json`, the state-durations handoff), **not** a",
        "self-loop weight — intra-tactic edges were dropped at structural",
        "build time and carry no weight.",
        "",
    ]
    out = out_dir / "README.md"
    out.write_text("\n".join(lines) + "\n")
    return out


__all__ = [
    "OGASP_DIR",
    "VIZ_DIR",
    "draw_net",
    "persist_summary",
    "write_divergence_report_md",
    "write_readme",
]
