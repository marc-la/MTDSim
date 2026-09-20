# Floats manifest — every figure and table, by dissertation position

Naming rule: [`docs/workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §j
(`<fig|tab>_<chapter>-<section>-<subsection><order>_<name>`). Position = the heading
the float is included under in `dissertation.tex`; order letter = order of
appearance under that heading. Regenerate with the tool named; never hand-edit
a generated file. Update this table in the same commit as any rename, move or
new float.

## Figures (`figures/`, included via `\graphicspath{{figures/}}`)

| Position | File (stem) | Label | Generator |
|---|---|---|---|
| §2.2 MTDSim | `fig_2-2a_mtdsim_model` (.pdf; .png preview is gitignored) | `fig:mtdsim-model` | `tools/ch2_model_figures.py --only fig_2-2a_mtdsim_model` (SVG in `tools/ch2_fig21_mtdsim_model.html`) |
| §2.2.1 Network model | `fig_2-2-1a_network_model` | `fig:network-model` | `tools/ch2_model_figures.py --only fig_2-2-1a_network_model` (SVG in `tools/ch2_fig22_network_model.html`) |
| §2.2.2 Defence mechanisms | `fig_2-2-2a_defence_module` | `fig:defence-module` | `tools/ch2_model_figures.py --only fig_2-2-2a_defence_module` (SVG in `tools/ch2_fig23_defence_module.html`; fails the build on any drift in either MTD pool) |
| §2.2.3 Attacker model | `fig_2-2-3a_attacker_model` | `fig:attacker-model` | `tools/ch2_model_figures.py --only fig_2-2-3a_attacker_model` (SVG in `tools/ch2_fig24_attacker_model.html`) |
| §3.1.2 MITRE ATT&CK | `fig_3-1-2a_attack_matrix` | `fig:attack-matrix` | `tools/attack_matrix_figure.py` (reads `data/gap/_attack/enterprise-attack-19.1.json`) |
| §3.1.3 Attack profiling | `fig_3-1a_attack_flow_volt_typhoon` (.pdf from .svg) | `fig:attack-flow-volt-typhoon` | hand-authored (`data/gap/hand_curated/`), restyled by `tools/restyle_attackflow_svg.py`; stem predates its 2026-09-02 move from §3.1.2 --- position here is authoritative |
| Ch 4 opening | `fig_4-0a_pipeline_ladder` (.pdf; the tool's .html intermediate is tracked beside it, .png preview gitignored) | `fig:pipeline` | `tools/pipeline_ladder_figure.py` (SVG assembled from the artefacts, Chromium print; rebuilt 2026-09-08 as a schematic worked example) |
| §4.4.3 tactic-to-verb mapping | `fig_4-4a_controller_mapping` | `fig:controller-mapping` | `tools/controller_mapping_figure.py` |
| §4.4.4 failure matrix | `fig_4-4b_failure_weight_matrix` | `fig:failure-weight-matrix` | `tools/failure_weight_decomposition_figure.py --layout matrix` (plain chapter geometry since 2026-09-08: values to two significant figures, no rule letters, no key; `--chapter-letters` restores the old form) |
| §4.4.1 runtime mechanics | `fig_4-4c_runtime_loop` | `fig:runtime-loop` | `tools/runtime_loop_figure.py` (restored 2026-09-08 from the ladder's lower half; imports the ladder's net-window rule) |
| §5.2.1 Without defence | `fig_5-2-1a_coverage_openings` | `fig:aio-coverage` | `tools/ch5_unopposed_figures.py` (reads `data/results/ch5_s531_unopposed/numbers.json`; three lettered panels: coverage, its first 3 000 s, opening variety; landed 2026-09-15) |
| §5.2.1 Without defence | `fig_5-2-1b_divergence` | `fig:aio-divergence` | `tools/ch5_unopposed_figures.py` (printed-value 4 × 4 visit-stream matrix, split-half null on the diagonal; landed 2026-09-15) |
| §5.2.2 Under disruption | `fig_5-2-2a_adaptivity` | `fig:aio-adaptivity` | `tools/ch5_adaptivity_figure.py` (reads `data/results/ch5_defended/numbers.json`; 2 × 2 of IP shuffle / OS diversity × 200 s / 2 000 s, activity shares before and after each interrupt, model beside the verdict-blind control; landed 2026-09-17) |
| §5.3.1 Defence mechanisms and execution schemes | `fig_5-3-1a_suppression_profiles` | `fig:eff-suppression-profiles` | `tools/ch5_effectiveness_figures.py --only fig55` (reads `data/results/ch5_defended/numbers.json`; 2 × 2 of singles / schemes × 200 s / 2 000 s, suppression of hosts reached per profile with bootstrap whiskers; landed 2026-09-17) |
| §5.3.2 Effect of the attacker model | `fig_5-3-2a_cross_arm` | `fig:eff-cross-arm` | `tools/ch5_effectiveness_figures.py --only fig56` (same corpus; the same 2 × 2, series = attacker arm, the baseline hatched grey, the model pooled over four profiles; landed 2026-09-17) |
| §5.4 Defence efficiency | `fig_5-4a_frontier` | `fig:eff-frontier` | `tools/ch5_efficiency_figures.py --only fig57` (same corpus; suppression against reconfiguration occupancy, labelled markers, shape = arm, one panel per interval on its own x range; landed 2026-09-17) |
| §5.4 Defence efficiency | `fig_5-4b_time_split` | `fig:eff-cost-decomposition` | `tools/ch5_efficiency_figures.py --only fig58` (same corpus; the attacker model's elapsed time split into completed activity, activity a mutation cut short and the imposed delay, values printed, one panel per interval; landed 2026-09-17) |
| §B.1 attack graph | `fig_B-1a_gap_flow_exemplar` | `fig:app-flow-exemplar` | `tools/gap_appendix_figures.py --only gap_flow_exemplar` |
| §B.1 attack graph | `fig_B-1b_gap_technique_graph` | `fig:app-technique-graph` | `tools/gap_appendix_figures.py --only gap_technique_graph` |
| §B.1 attack graph | `fig_B-1c_gap_technique_core` | `fig:app-technique-core` | `tools/gap_appendix_figures.py --only gap_technique_core` |
| §B.1 attack graph | `fig_B-1d_gap_tactic_graph` | `fig:app-tactic-graph` | `tools/gap_appendix_figures.py --only gap_tactic_graph` |
| §B.6 weight sets | `fig_B-6a_failure_weight_decomposition` | `fig:failure-weight-decomposition` | `tools/failure_weight_decomposition_figure.py --layout decomposition` |
| §B.6 weight sets | `fig_B-6b_distance_kernel_bands` | `fig:distance-kernel-bands` | `tools/failure_weight_decomposition_figure.py --layout bands` |
| §C.1 dwell robustness | `fig_C-1a_sens_dwell_family` | `fig:sens-dwell-anchor` | `tools/ch5_sensitivity_figure.py --csv data/results/ch5_s51_sensitivity/per_run.csv --anchor stealth --stem fig_C-1a_sens_dwell_family` (moved from §5.1 on 2026-09-17, Marc's ruling: the body keeps the table; label kept) |

## Tables (`tables/`, via `\input{tables/...}`)

| Position | File | Label(s) | Generator |
|---|---|---|---|
| §4.4.2 dwell times | `tab_4-4a_dwell_catalogue.tex` (one panel since 2026-09-08: tactic + mean dwell) | `tab:dwell-catalogue` | `tools/dwell_catalogue_tables.py` |
| §B.2 objective classification | `tab_B-2a_objective_classification_audit.tex` | `tab:objective-audit-{exfiltration,impact,exfiltration-impact,none-c2}` | `tools/gasp_structural_baseline.py --tex` |
| §B.3 partition schemes | `tab_B-3a_rejected_partitions.tex` | `tab:rejected-partitions` | `tools/gasp_partition_candidates.py` |
| §B.4 dwell derivation | `tab_B-4b_dwell_anchors.tex` (the former chapter panel (a): families, badges) | `tab:dwell-anchors` | `tools/dwell_catalogue_tables.py` |
| §B.4 dwell derivation | `tab_B-4a_dwell_derivation.tex` (gained the multiplier column 2026-09-08) | `tab:dwell-derivation` | `tools/dwell_catalogue_tables.py` |
| §B.5 tactic mapping reasons | `tab_B-5a_controller_mapping_reasons.tex` | `tab:controller-mapping` | `tools/controller_mapping_figure.py` |
| §B.6 weight sets | `tab_B-6a_outcome_overlay_weights.tex` | `tab:overlay-failure-rules`, `tab:overlay-distance-kernel`, `tab:overlay-failure-set` | `tools/failure_weight_decomposition_figure.py` |
| App. D preliminary extraction | `tab_D-0a_preliminary_extraction.tex` | `tab:preliminary-extraction` | `tools/preliminary_extraction_table.py` |
| §5.1 Experimental setup | `tab_5-1a_experiment.tex` (RESTRUCTURED 2026-09-20: Parameter · Value, one value column, thirteen rows in four groups, varied rows first, semicolons for levels; caption's design sentence matched to run_corpus.py — handoff §AJ; hand-set 2026-09-18; one table, both kinds of row — conventions §c; row-grouped by the simulation's moving parts, the justification column deleted; replaces `tab_5-1a_factors_varied` and `tab_5-1b_factors_fixed`) | `tab:experiment` | none yet — `tools/ch5_setup_tables.py` owed (ch5 design handoff C39), reads the run matrix; one table fewer to emit |
| §5.1 Experimental setup | `tab_5-1b_metrics.tex` (hand-set 2026-09-18, rebuilt 2026-09-20 on handoff §AK: Measures · Metric · Definition under Table 3.1's two purposes, ten rows named as the results floats name them, deployment tempo out; replaces `tab_5-1c_measures`) | `tab:metrics` | as above |
| §5.2.1 Without defence | `tab_5-2-1a_unopposed_summary.tex` | `tab:unopposed-summary` | `tools/ch5_unopposed_figures.py` (same corpus; depth column replaced by successes per host, target reached added — findings §6; landed 2026-09-15) |
| §5.3.1 Defence mechanisms and execution schemes | `tab_5-3-1a_conditions.tex` | `tab:eff-conditions` | `tools/ch5_effectiveness_figures.py --only tab55` (same corpus; nine conditions per interval ordered by suppression, delay with the no-compromise share, blocked fraction; overlapping neighbours daggered; landed 2026-09-17) |
| §5.3.2 Effect of the attacker model | `tab_5-3-2a_orderings.tex` | `tab:eff-orderings` | `tools/ch5_effectiveness_figures.py --only tab56` (same corpus; ranks per arm at each interval, Spearman's rho with a seed-bootstrap interval and the family contrast as Cliff's delta in the footnote; landed 2026-09-17) |
| §5.3.3 Comparison with prior evaluations | `tab_5-3-3a_lineage.tex` | `tab:eff-lineage` | `tools/ch5_effectiveness_figures.py --only tab57` (the lineage arm of the same corpus, general objective; one row per published claim, direction per arm on suppression of hosts reached, Ho read at 200 s with the named pair; Zhang and Brown locators marked to verify; landed 2026-09-17) |
| §5.4 Defence efficiency | `tab_5-4a_cost.tex` | `tab:eff-cost` | `tools/ch5_efficiency_figures.py --only tab58` (same corpus at 200 s; actions and successes per host reached as cell totals with bootstrap intervals, occupancy and mutations per 1 000 s, both arms; landed 2026-09-17) |
| App. C lead (was §5.1, section cut 2026-09-20) | `tab_C-0a_declared_inputs.tex` | `tab:parameter-register` | `data/results/ch5_s51_sensitivity/analyse.py` (the §5.1 re-run at the chapter's pins, 33 000 runs; ten rows in three groups, four columns in words; landed 2026-09-17) |
| §C.1 dwell robustness | `tab_C-1a_family_sensitivity.tex` | `tab:anchor-sensitivity` | as above (band ends against the declared value per family and condition) |
| §C.2 exponential family | `tab_C-2a_shape_substitution.tex` | `tab:shape-substitution` | as above (paired Erlang-4 against exponential, declared dwell and the ×4 corner) |
| §C.3 decay robustness | `tab_C-3a_decay_sensitivity.tex` | `tab:decay-sensitivity` | as above (the two rates and the floor at band ends, then the four corners) |

Inline (typed directly in `dissertation.tex`, no file): `tab:experiment-one` (§B.7),
`tab:mtd-metrics` (§3.2.1, Table 3.1).

## Planned — Chapter 5, placeholder floats (2026-09-09)

Every float below exists in `dissertation.tex` as a framed `\placeholderbox`
with its intended caption written long, so the chapter's visual argument can be
read and cut before any prose is drafted (writing guide: figures, then captions,
then text). None has a generator yet. Replacing one is a single-line swap of
`\placeholderbox` for `\includegraphics`; the stem is then named by the §j rule
from the position column, and this block folds into the tables above.

**Placement, while they are placeholders.** Every float in this block carries
`[H]` (the `float` package) rather than `[htbp]`. With no prose between them the
float queue flushed ahead of the headings and each one rendered *before* the
subsection it belonged to — Figures 5.1–5.4 on pp. 28–29 against subsections on
p. 30, and 5.4.1–5.4.3 all on p. 37 with their figures on pp. 34–36 — which
defeats the purpose of placing them early. `[H]` pins each box under its own
heading so the visual argument can be read in position. **Revert each `[H]` to
`[htbp]` as that subsection's prose lands**: with text to flow around, `[htbp]`
is the right specifier and `[H]` strands whitespace.

**Count, and the ruling that governs it.** Fifteen figures and eight tables is
above the corpus norm for a chapter of this length (Brown two figures and one
table; Zhang about seven figures; Tay five and none; Ho about eight and eight;
Reti six and two). **That is not a constraint here.** Marc ruled on 2026-09-09:
*"I don't care how many floats exist — I just need as many as relevant and
reasonable and comprehensive enough."* So no float is cut to hit a norm, and the
corpus counts above are context, not a quota.

The test is **relevance**, applied one float at a time: a float that carries a
claim stays, however many that makes; a float that only decorates a claim another
float already carries goes, however few remain. The **core** marks below are read
on that basis — they name the floats without which a claim goes unevidenced. The
**cut or appendix** marks are no longer a page-budget cut list; they mark floats
whose claim is carried elsewhere, and each still has to fail the relevance test
on its own before it goes.

| Position | Label | Standing | What it is for |
|---|---|---|---|
| App. C (the cut sensitivity section) | `tab:parameter-register` | **core — LANDED 2026-09-17** | generated from the §5.1 re-run: ten rows in three groups (dwell times, mapping, failure matrix), four columns in words, symbols in the caption; the fragment is in the Tables list above |
| App. C (the cut sensitivity section) | `fig:sens-dwell-anchor` | **moved to App. C.1, 2026-09-17** | the low-and-slow family across its band (the re-run's one mover by an order of magnitude); a figure re-enters the body only if its form is one a sentence cannot carry (Marc's ruling) |
| App. C (the cut sensitivity section) | `fig:sens-dwell-shape` | **removed 2026-09-13** | a swap, not a band: a register row + `tab:shape-substitution` |
| App. C (the cut sensitivity section) | `fig:sens-mapping` | **removed 2026-09-13** | a swap: a register row + `tab:experiment-one` |
| App. C (the cut sensitivity section) | `fig:sens-failure-matrix` | **removed 2026-09-13** | register rows + `tab:decay-sensitivity` (App. C.3, added) |
| App. C.3 | `tab:decay-sensitivity` | **core (appendix) — LANDED 2026-09-17** | generated; every rate inert at both ends and all four corners at the chapter's pins; the floor zero by structure |
| §5.1 | `tab:factors-varied` | **core — LANDED 2026-09-14** | six rows in two groups: crossed (attacker arm, defence condition, mutation interval) and one at a time (timing regime, horizon, objective); `simultaneous` dropped (C34); the fragment is in the Tables list above |
| §5.1 | `tab:factors-fixed` | **core — LANDED 2026-09-14** | eleven rows in four groups: environment, replication, attacker, defender; inherited marks and the three version pins in the footnote row |
| §5.2.1 | `fig:aio-coverage` | **core — LANDED 2026-09-15** | three lettered panels: coverage over time (a), its first 3 000 s (b), opening variety against depth (c) — the ruled plurality exhibit; the fragment is in the Figures list above |
| §5.2.1 | `fig:aio-divergence` | **core — LANDED 2026-09-15** | printed-value 4 × 4 matrix, split-half null on the diagonal (aggregate deliberately absent) |
| §5.2.1 | `tab:unopposed-summary` | **core — LANDED 2026-09-15** | + aggregate row (the objective-conditioning contrast) and baseline row; entropy footnoted; depth column replaced by successes per host (saturated, findings §6); target reached added |
| §5.2.2 | `fig:aio-adaptivity` | **core — LANDED 2026-09-17** | 2 × 2 mechanism × tempo, control beside the treatment; the subsection's only float; a null result (the control moves identically, findings §4) |
| §5.2.3 | `fig:aio-disengagement` | **removed 2026-09-13** | the ablation subsection is gone (design C31); see the ch5 design handoff §16 |
| §5.2.3 | `fig:aio-learning` | **removed 2026-09-13** | as above |
| §5.2.3 | `tab:ablation-ladder` | **removed 2026-09-13** | as above |
| §5.3.1 | `fig:eff-suppression-profiles` | **core — LANDED 2026-09-17** | four lettered panels: singles / schemes at each interval (the interval is a crossed factor); the aggregate drawn as the fifth series |
| §5.3.1 | `tab:eff-conditions` | **core — LANDED 2026-09-17** (was cut-or-appendix) | the numbers behind the bars, with intervals; the delay column's no-compromise share is the denied-all-hosts share (one column); no-defence reference once |
| §5.3.2 | `fig:eff-cross-arm` | **core — LANDED 2026-09-17** | the central comparison; same four-panel split as fig:eff-suppression-profiles; arm by hatch |
| §5.3.2 | `fig:eff-delay` | **removed 2026-09-13** | survival curves are no corpus genre; a column of `tab:eff-conditions`. Zhang-form bars if checkpoint time becomes the primary (handoff §15) |
| §5.3.2 | `tab:eff-orderings` | **core — LANDED 2026-09-17** | ranks per arm at each interval; the family contrast (Cliff's delta) is the primary and the rank correlation its companion, per the 2026-09-09 inference ruling |
| §5.3.3 | `tab:eff-lineage` | **core — LANDED 2026-09-17** (converted from `fig:eff-lineage`) | comparison table: published claim, direction per arm, boundary in the footnote; the third row is Ho at 200 s (the extraction's locator), not "at long intervals" |
| §5.4 | `fig:eff-frontier` | **core — LANDED 2026-09-17** | labelled markers, shape = arm; two panels, one per interval, the 2 000 s panel on its own x range; key below the panels |
| §5.4 | `fig:eff-cost-decomposition` | **keep — LANDED 2026-09-17** (was cut-or-appendix) | attacker model only, and the caption says why; the third segment is activity a mutation cut short, the remainder being structurally empty (findings §2) |
| §5.4 | `tab:eff-cost` | **keep — LANDED 2026-09-17** | at 200 s; the 2 000 s rows are in the record |

**2026-09-13.** §5.1's three subsections are retired (one section, one unit), so its four floats now sit under §5.1 pending the stage-2 placeholder audit; §5.3.3's three floats are removed with the subsection. Marks above are otherwise unchanged until that audit rules each float.

**Stage-2 float audit, 2026-09-13 (ch5 design handoff §18).** Convention first, then reconciled: 8 figures + 8 tables in the body (from 15 + 8) plus one appendix table. Every remaining float is in an attested genre (figure_table_conventions.md §d–§f); the two that were not — survival curves and small-multiple claim panels — became a table column and a comparison table. The chapter-head FLOAT CONTRACT comment in the tex is the series/legend/label contract every generator follows.
