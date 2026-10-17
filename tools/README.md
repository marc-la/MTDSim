# Tools

**Figure and table generators.** `python tools/build_floats.py` runs every one;
`--list` prints which float each writes, and the top-level README maps them to
the dissertation's numbering. They read only committed inputs (`data/`,
`experiments/*/numbers*.json`) plus the ATT&CK bundle `make inputs` fetches, and
write into `docs/thesis/figures/` and `docs/thesis/tables/`.

- `_ch5_style.py` is the house style every results figure shares; `_tactic_axis.py`
  fixes the tactic order from the pinned ATT&CK bundle.
- `pipeline_ladder_figure.py`, `ch5_effectiveness_figures.py`, `ch5_ablation_figure.py`,
  `ch5_sensitivity_figure.py` and `restyle_attackflow_svg.py` are helpers the live
  generators import.
- `ch2_fig2*.html` are the hand-drawn sources of Figures 2.1–2.3 (rendered with Playwright).
- A few generators also write tables cut from the appendices (`tab_B-4a`, `tab_B-5a`,
  `tab_C-0a`, `tab_C-2a`, `tab_C-3a`, `tab_C-4a`, `tab_F-1_*`); the dissertation does
  not include them.

**Developer tools.**

| Script | Use |
|---|---|
| `mtd_golden_streams.py` | capture or check the golden event streams in `baseline/golden_movement/` (`tests/test_mtd_golden_streams.py`) |
| `des_step.py` | step through a SimPy run event by event |
| `mtd_cost_bench.py` | per-mechanism cost table for the MTD pool |
| `mtd_ai_run.py`, `mtd_ai_lambda_ladder.py` | train and evaluate the inherited reinforcement-learning defender |
| `exploit_learning_sweep.py`, `exploit_learning_analyse.py` | the pre-registered vulnerability-memory study (§4.4.4) |
| `gasp_tactic_profile_stats.py`, `gasp_tactic_restatement.py` | attack-profile statistics at tactic resolution (§4.2) |
