---
status: executing — corpus launched 2026-09-17 on Marc's instruction to iterate §5.3.2 → §5.5 in sequence with preliminary numbers (the stage-2 acceptance stop waived for this pass; the design is recorded here for ratification on read). Per-section findings records under docs/implementation/pipeline/ogasp/ch5_s5*_findings.md; floats land through tools/ch5_*_figures.py. OWED: Marc's rulings in §5, the caption voice passes, the 60 000 s defended extension (deployments held), the Overleaf paste set
created: 2026-09-17
topic: "The chapter 5 defended corpus: one run set at the chapter's pins over Table 5.2's defence conditions and both intervals, on both attacker arms, that populates §5.3.2 (the adaptivity figure and its verdict-blind control), §5.4.1 (suppression by profile; the conditions table), §5.4.2 (the cross-arm figure; the orderings table), §5.4.3 (the prior evaluations, re-run at the lineage's objective) and §5.5 (the frontier, the time decomposition, the cost table)"
---

# §5.3.2–§5.5 — the defended corpus and what each section reads off it

**Goal.** Record one corpus of defended runs at the chapter's declared
configuration and read the eight remaining chapter 5 floats off it in
sequence, preliminarily, following
[`../workflows/results_section_workflow.md`](../workflows/results_section_workflow.md).
§5.3.1's corpus (`ch5_s531_unopposed`) is the no-defence reference; this
corpus re-runs the no-defence cell on the same seeds so every analysis is
self-contained (the two agree bit for bit — same seam, same pins).

## 1. The cell set

| Factor (Table 5.2) | Level(s) run | Why |
|---|---|---|
| Attacker arm | **6**: baseline; movement on the four profiles and the aggregate | every float's series or rows |
| Defence condition | **10**: no defence; the seven mechanisms alone; random and alternative **over the seven** | Table 5.2's set; the substrate's default pool is the lineage four, so the seven are passed as `custom_strategies` |
| Mutation interval | **200 s; 2 000 s** (crossed) | no defence is interval-unread and runs once |
| Timing regime | quasi-periodic (core); **exponential at 200 s** (one at a time) | the memoryless draw produces overlapping deployments and suspensions at 200 s — read in the analysis, drawn nowhere |
| Horizon | 15 000 s | the 60 000 s defended extension with deployments held (interval × 4) is **not run** in this pass — owed |
| Objective | **targeted** (core); **opportunistic / general** (the lineage arm, §5.4.3 only) | Table 5.2's objective row |
| Verdict-blind control | the four profiles under IP shuffle and OS diversity at both intervals, and unopposed | §5.3.2's control; the unopposed blind cell carries the placebo null |
| Runs per cell | 100 seeds, 0–99, shared | — |

30 200 runs: core 11 400, lineage 11 400, regime 5 400, blind 2 000. Measured
cost 0.12–1.2 s per run (network-layer singles at 200 s the slowest); about
40 min on seven workers.

### Pins (Table 5.3 → the seam)

As §5.3.1's handoff, plus: `mtd_scheme` ∈ {`single`, `random`, `alternative`};
`custom_strategies` the mechanism class (single) or the seven-class list
(schemes); `mtd_interval` 200 / 2 000; `substrate_timing_regime` `"shifted"`
(core) / `"exponential"` (regime arm); `overlay=verdict_blind_overlay()` on the
blind arm in place of `overlay_version="v4_failure_only"`. The baseline arm is
the Gate 0 wiring with the substrate's `MTDOperation` on the shared
`end_event`, as the frontier study wired it.

## 2. What each section reads

**§5.3.2 Fig. 5.4** — `interrupt_action_mix(run, window=5)` pooled over the
four profiles: the verb mix (dwell as its own activity) in the five visits
before and after each MTD interrupt, treatment (failure-only overlay) beside
the verdict-blind control, in the 2 × 2 of {IP shuffle, OS diversity} ×
{200 s, 2 000 s}. Paired within run: the per-run after-minus-before share per
activity, mean ± CI over runs. Diagnostic (printed, not drawn): the placebo
null — the defended run's interrupt positions applied to the same seed's
unopposed run.

**§5.4.1 Fig. 5.5 / Tab. 5.5** — suppression = 1 − hosts(cond) / hosts(none)
per profile and condition, seeded bootstrap CI on the ratio of means (2 000
resamples); delay to first compromise (`first_compromise_time`; censored share
at the horizon); `blocked_fraction` mean ± CI. Adjacent overlap marked.

**§5.4.2 Fig. 5.6 / Tab. 5.6** — the same suppression per arm (movement pooled
over the four profiles vs baseline); the two orderings; Spearman ρ with a
seed-bootstrap CI; the family contrast (network-layer vs application-layer
conditions) as Cliff's δ with CI per arm, per the 2026-09-09 inference ruling.

**§5.4.3 Tab. 5.7** — the lineage arm (general objective): shuffle singles vs
diversity singles at 200 s (Zhang); best single vs best scheme (Brown);
diversity vs shuffle at 2 000 s (Ho). Direction per arm.

**§5.5 Fig. 5.7 / Fig. 5.8 / Tab. 5.8** — `disruption_ledger` occupancy per
condition per arm against suppression (frontier); `cost_ledger` time split
(dwell / MTD penalty / remainder) on the movement arm; actions and successes
per distinct host, occupancy and executions per 1 000 s by condition and arm.

## 3. Outputs

`data/results/ch5_defended/`: `run_corpus.py`, `runs.jsonl` (gitignored),
`analyse.py` → `numbers.json` (force-added) and `preview_*.png`. Findings:
`docs/implementation/pipeline/ogasp/ch5_s532_adaptivity_findings.md`,
`ch5_s54_effectiveness_findings.md`, `ch5_s55_efficiency_findings.md`.
Generators: `tools/ch5_adaptivity_figure.py`, `tools/ch5_effectiveness_figures.py`,
`tools/ch5_efficiency_figures.py`.

## 4. Rulings owed (recommendation each)

| # | Question | Recommendation |
|---|---|---|
| Q1 | Random and alternative over the seven (Table 5.2) rather than the lineage four (every recorded scheme run) | the seven; Table 5.2 rules it, and the pool restoration was ruled 2026-08-27 |
| Q2 | Fig. 5.4's activity vocabulary: the six verbs plus dwell | as stated; dwell is part of the mix (measures.py §3) |
| Q3 | Fig. 5.5 / 5.6 drawn at both intervals (four panels) or at 200 s only | both — the interval is a crossed factor |
| Q4 | The 60 000 s defended extension | run after the preliminary is read; interval × 4 holds deployments per run |
| Q5 | §5.4.3's lineage rows: the sources for "shuffle dominates" (Zhang) and "best single ≈ best combination" (Brown) are not carried in the extractions as result rows | Marc to confirm the claims and locators before the table's source column is final; marked *verify* in the fragment |
