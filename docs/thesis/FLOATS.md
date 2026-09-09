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
| §2.2 MTDSim | `fig_2-2a_mtdsim_model` (.pdf; .png preview is gitignored) | `fig:mtdsim-model` | `tools/mtdsim_model_figure.py` (SVG in `tools/mtdsim_model_figure.html`) |
| §3.1.2 MITRE ATT&CK | `fig_3-1-2a_attack_matrix` | `fig:attack-matrix` | `tools/attack_matrix_figure.py` (reads `data/gap/_attack/enterprise-attack-19.1.json`) |
| §3.1.3 Attack profiling | `fig_3-1a_attack_flow_volt_typhoon` (.pdf from .svg) | `fig:attack-flow-volt-typhoon` | hand-authored (`data/gap/hand_curated/`), restyled by `tools/restyle_attackflow_svg.py`; stem predates its 2026-09-02 move from §3.1.2 --- position here is authoritative |
| Ch 4 opening | `fig_4-0a_pipeline_ladder` (.pdf; the tool's .html intermediate is tracked beside it, .png preview gitignored) | `fig:pipeline` | `tools/pipeline_ladder_figure.py` (SVG assembled from the artefacts, Chromium print; rebuilt 2026-09-08 as a schematic worked example) |
| §4.4.3 tactic-to-verb mapping | `fig_4-4a_controller_mapping` | `fig:controller-mapping` | `tools/controller_mapping_figure.py` |
| §4.4.4 failure matrix | `fig_4-4b_failure_weight_matrix` | `fig:failure-weight-matrix` | `tools/failure_weight_decomposition_figure.py --layout matrix` (plain chapter geometry since 2026-09-08: values to two significant figures, no rule letters, no key; `--chapter-letters` restores the old form) |
| §4.4.1 runtime mechanics | `fig_4-4c_runtime_loop` | `fig:runtime-loop` | `tools/runtime_loop_figure.py` (restored 2026-09-08 from the ladder's lower half; imports the ladder's net-window rule) |
| §B.1 attack graph | `fig_B-1a_gap_flow_exemplar` | `fig:app-flow-exemplar` | `tools/gap_appendix_figures.py --only gap_flow_exemplar` |
| §B.1 attack graph | `fig_B-1b_gap_technique_graph` | `fig:app-technique-graph` | `tools/gap_appendix_figures.py --only gap_technique_graph` |
| §B.1 attack graph | `fig_B-1c_gap_technique_core` | `fig:app-technique-core` | `tools/gap_appendix_figures.py --only gap_technique_core` |
| §B.1 attack graph | `fig_B-1d_gap_tactic_graph` | `fig:app-tactic-graph` | `tools/gap_appendix_figures.py --only gap_tactic_graph` |
| §B.6 weight sets | `fig_B-6a_failure_weight_decomposition` | `fig:failure-weight-decomposition` | `tools/failure_weight_decomposition_figure.py --layout decomposition` |
| §B.6 weight sets | `fig_B-6b_distance_kernel_bands` | `fig:distance-kernel-bands` | `tools/failure_weight_decomposition_figure.py --layout bands` |

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

Inline (typed directly in `dissertation.tex`, no file): `tab:experiment-one` (§B.7),
`tab:anchor-sensitivity` (§C.1), `tab:shape-substitution` (§C.2),
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

**Count, and the cut.** Fifteen figures and seven tables is above the corpus norm
for a chapter of this length (Brown two figures and one table; Zhang about seven
figures; Tay five and none; Ho about eight and eight; Reti six and two), and the
chapter currently runs about twelve pages of floats against roughly 3 000 words.
The nine figures and four tables marked **core** carry the argument on their own;
the rest are marked **cut or appendix** and should be the first things surrendered
when the page budget bites. Nothing marked core can be dropped without leaving a
claim unevidenced.

| Position | Label | Standing | What it is for |
|---|---|---|---|
| §5.1 | `tab:parameter-register` | **core** | every declared quantity, swept-with-a-band or held-with-a-reason, in one place |
| §5.1.1 | `fig:sens-dwell-anchor` | **core** | the one dwell anchor whose movement changes an outcome |
| §5.1.1 | `fig:sens-dwell-shape` | cut or appendix | where the exponential dwell stops being innocuous; a narrow claim |
| §5.1.2 | `fig:sens-mapping` | **core** | the mapping is a discrete choice, not a band — the standing bound |
| §5.1.3 | `fig:sens-failure-matrix` | cut or appendix | headline verdicts hold across the decay bands; the finer ordering does not |
| §5.2 | `tab:factors-varied` | **core** | the factor space every later result is located in |
| §5.2 | `tab:factors-fixed` | **core** | what was held, and why; inherited constants marked as inherited |
| §5.3.1 | `fig:aio-coverage` | **core** | the clearest single picture of what the attacker model added |
| §5.3.1 | `fig:aio-divergence` | **core** | profiles differ by more than a profile differs from itself |
| §5.3.1 | `tab:unopposed-summary` | **core** | the reference every suppression figure is a difference from; carries the pruning rule |
| §5.3.2 | `fig:aio-adaptivity` | cut or appendix | the adaptive loop operating, against a verdict-blind control |
| §5.3.3 | `fig:aio-disengagement` | **core** | where a cost-sensitive attacker abandons |
| §5.3.3 | `fig:aio-learning` | **core** | the measured negative: breadth falls as learning strengthens |
| §5.4.1 | `fig:eff-suppression-profiles` | **core** | which defences reach this attacker, and whether it is profile-dependent |
| §5.4.1 | `tab:eff-conditions` | cut or appendix | the three disruption channels per condition, with intervals |
| §5.4.2 | `fig:eff-cross-arm` | **core** | the chapter's central comparison, in one figure |
| §5.4.2 | `fig:eff-delay` | cut or appendix | the delay channel; separates stopping from slowing |
| §5.4.2 | `tab:eff-orderings` | **core** | the two orderings and the grade the evidence carries |
| §5.4.3 | `fig:eff-lineage` | cut or appendix | prior findings re-run under both attackers |
| §5.5 | `fig:eff-frontier` | **core** | what each defence buys against what it spends; arm-invariant on the cost axis |
| §5.5 | `fig:eff-cost-decomposition` | cut or appendix | whether a defence makes the attacker do more, or take longer |
| §5.5 | `tab:eff-cost` | cut or appendix | both sides of the exchange, event-wise across arms |
