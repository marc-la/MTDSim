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
| Ch 4 opening | `fig_4-0a_pipeline_ladder` | `fig:pipeline` | `tools/pipeline_ladder_figure.py` |
| §4.2.4 L4 execution | `fig_4-2-4a_controller_mapping` | `fig:controller-mapping` | `tools/controller_mapping_figure.py` |
| §4.2.4 L4 execution | `fig_4-2-4b_failure_weight_matrix` | `fig:failure-weight-matrix` | `tools/failure_weight_decomposition_figure.py --layout matrix` (chapter geometry, natural size) |
| §4.2.4 L4 execution | `fig_4-2-4c_movement_dataflow` | `fig:movement-dataflow` | `tools/movement_dataflow_figure.py` |
| §B.1 attack graph | `fig_B-1a_gap_flow_exemplar` | `fig:app-flow-exemplar` | `tools/gap_appendix_figures.py --only gap_flow_exemplar` |
| §B.1 attack graph | `fig_B-1b_gap_technique_graph` | `fig:app-technique-graph` | `tools/gap_appendix_figures.py --only gap_technique_graph` |
| §B.1 attack graph | `fig_B-1c_gap_technique_core` | `fig:app-technique-core` | `tools/gap_appendix_figures.py --only gap_technique_core` |
| §B.1 attack graph | `fig_B-1d_gap_tactic_graph` | `fig:app-tactic-graph` | `tools/gap_appendix_figures.py --only gap_tactic_graph` |
| §B.6 weight sets | `fig_B-6a_failure_weight_decomposition` | `fig:failure-weight-decomposition` | `tools/failure_weight_decomposition_figure.py --layout decomposition` |
| §B.6 weight sets | `fig_B-6b_distance_kernel_bands` | `fig:distance-kernel-bands` | `tools/failure_weight_decomposition_figure.py --layout bands` |

## Tables (`tables/`, via `\input{tables/...}`)

| Position | File | Label(s) | Generator |
|---|---|---|---|
| §4.2.4 L4 execution | `tab_4-2-4a_dwell_catalogue.tex` | `tab:dwell-catalogue` | `tools/dwell_catalogue_tables.py` |
| §B.2 objective classification | `tab_B-2a_objective_classification_audit.tex` | `tab:objective-audit-{exfiltration,impact,exfiltration-impact,none-c2}` | `tools/gasp_structural_baseline.py --tex` |
| §B.3 partition schemes | `tab_B-3a_rejected_partitions.tex` | `tab:rejected-partitions` | `tools/gasp_partition_candidates.py` |
| §B.4 dwell derivation | `tab_B-4a_dwell_derivation.tex` | `tab:dwell-derivation` | `tools/dwell_catalogue_tables.py` |
| §B.5 tactic mapping reasons | `tab_B-5a_controller_mapping_reasons.tex` | `tab:controller-mapping` | `tools/controller_mapping_figure.py` |
| §B.6 weight sets | `tab_B-6a_outcome_overlay_weights.tex` | `tab:overlay-failure-rules`, `tab:overlay-distance-kernel`, `tab:overlay-failure-set` | `tools/failure_weight_decomposition_figure.py` |
| App. D preliminary extraction | `tab_D-0a_preliminary_extraction.tex` | `tab:preliminary-extraction` | `tools/preliminary_extraction_table.py` |

Inline (typed directly in `dissertation.tex`, no file): `tab:experiment-one` (§B.7),
`tab:anchor-sensitivity` (§C.1), `tab:shape-substitution` (§C.2).
