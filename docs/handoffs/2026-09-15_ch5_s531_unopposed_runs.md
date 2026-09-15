---
status: partially shipped — design accepted and corpus RUN 2026-09-15 (1 700 runs, zero errors); preliminary read recorded in ../implementation/pipeline/ogasp/ch5_s531_unopposed_findings.md; OWED: Marc's read of that record's §6 (four float changes), Q4, then the house-style generators (tools/ch5_unopposed_figures.py + the tab_5-3-1 fragment)
created: 2026-09-15
topic: "The §5.3.1 no-defence corpus: the cell set, pins and measures that populate fig:aio-coverage, fig:aio-divergence and tab:unopposed-summary with preliminary numbers, so the direction of the results can be read before the chapter commits to its floats"
---

# §5.3.1 Without defence — the run plan for Figures 5.2, 5.3 and Table 5.4

**Goal.** Record one no-defence corpus at the chapter's declared configuration
and read the three §5.3.1 floats off it, preliminarily: Fig. 5.2 (campaign
coverage; opening variety), Fig. 5.3 (pairwise divergence against its
split-half null) and Tab. 5.4 (behaviour without defence, by attacker). The
point is to see the direction before the prose is drafted and to learn what,
if anything, the floats need changed. Scope is §5.3.1 only; §5.3.2 (under
defence) and §5.4 read other cells.

**Why a fresh corpus and not a re-read.** Every recorded number that these
three floats are shaped on was taken at a configuration the chapter no longer
declares: the plurality table (`plurality_reporting.md` §2) and the divergence
corpus (`profile_divergence_findings.md`) ran the *general* objective, the
registry's **v1** overlay (the default `load_outcome_overlay` still returns),
and — for the plurality table — ten seeds pre-restoration. Table 5.3 pins the
targeted objective, the failure-only (v4) overlay and 100 seeds. The picture
may move; if it does, that is the declared configuration, not a bug.

## 1. The cell set — for acceptance

Every row is a cell of Table 5.2 read at the no-defence level, or a row of
Table 5.3. A level not listed is not run.

| Factor | Level(s) run here | Why |
|---|---|---|
| Attacker arm | **6**: the baseline attacker; the movement attacker on `objective_exfiltration`, `objective_impact`, `objective_exfiltration_impact`, `objective_none_c2`, and `aggregate` | the four profiles and the aggregate are the table's rows; the baseline is the reference line in both Fig. 5.2 panels and the last row of Tab. 5.4 |
| Defence condition | **no defence only** | §5.3.1 is read against no defence so that it is a statement about the model |
| Mutation interval | **not a dimension here** — a no-defence run never reads the interval, so one cell serves both of Table 5.2's levels | flag for the voice pass: §5.2's closing sentence ("reads the no-defence column at both intervals") is vacuous for §5.3.1 |
| Timing regime | moot (no schedule runs) | — |
| Objective | **targeted, the database set** (C37, C41) | the APT's objective on every cell; `attack_objective="targeted", target_layer=None` |
| Horizon | **15 000 s (core)** and **60 000 s (the one-at-a-time extension)** | the core draws the floats; the extension is free of the "longer run is more defence" confound under no defence, so it is the cheapest read of C36 ("the numbers decide") and of the terminal-mode column at campaign headroom |
| Runs per cell | **100 seeds, 0–99, the same on every arm** | cost is trivial (below); no reason to under-power a preliminary and then re-run |

Run count: 6 arms × 2 horizons × 100 seeds = **1 200 runs**. Measured wall
cost at this configuration: movement 0.13–0.34 s per run, baseline 0.05 s, so
about two minutes on six workers.

**Optional diagnostic arm (recommended, not a chapter cell).** The five
movement arms at 15 000 s under the *general* objective, 100 seeds, everything
else identical: 500 runs, one minute. It answers one question only — whether
the switch to the targeted objective moved the §5.3.1 picture against the
record — and is reported in the analysis output, never in a float.

### Pins (Table 5.3, translated to the seam)

| Held | Value passed | Note |
|---|---|---|
| tactic-to-verb mapping | `mapping_version="v2_partial"` | the partial mapping (Appendix B.5) |
| weight set | `overlay_version="v4_failure_only"` | **must be passed explicitly** — the registry default is `v1_band_relationship` |
| synthetic overlay (M6) | `with_synthetic_overlay=True` | the shipped model |
| sink retrace | `retrace_sinks=True` | Table 5.3 row |
| fresh-host contract | `fresh_host_contract=True` (default) | ruled into the reported configuration 2026-08-30 |
| cost model, memory, learning | `attacker_state=None`, `exploit_learning_rate=None`, `token_hold=None` | implemented, not exercised |
| geometry | `GEOMETRY` (50 / 5 / 8 / 4; two database hosts) | one terrain |
| max events | 50 000 (default) | unreached on record |
| substrate timing regime | `"shifted"` (default; unread with no defence) | — |
| baseline arm | the Gate 0 wiring: `_install_objective(..., "targeted", target_layer=None)` on the shared `AttackOperation`, then `proceed_attack()`; same seed discipline | `data/results/targeted_attacker_build/run_gate0.py` `run_baseline_cell` |

## 2. What is read off the corpus, per float

All measures are the shipped suite's (`movement/measures.py`); the analysis is
a reader over the recorded stream and simulates nothing. Intervals through
`interval_report` (mean ± 1.96 SEM); `ordering_supported` printed wherever an
ordering could be read.

**Fig. 5.2(a) — distinct tactics reached against simulated time.**
`distinct_place_curve` per run, stepped onto a common time grid (every 250 s
to the core horizon), averaged per profile with its interval. A run that
reaches the target ends early; its curve is **held at its final value** from
termination onward (right-censored, stated in the caption). The baseline
reference is the count of distinct *verbs* (`name` column of its attack
record) reached against time, drawn as a dashed grey line. Vocabulary caveat
for Marc: the caption says "a fixed loop over three activities"; the record
shows six verbs (`SCAN_HOST`, `ENUM_HOST`, `SCAN_PORT`, `EXPLOIT_VULN`,
`BRUTE_FORCE`, `SCAN_NEIGHBOR`). Either the reference line is drawn at six
and the caption corrected, or the six are grouped into the three activities
the caption means (scan / exploit / pivot) and the grouping decoded in the
caption. Ruling owed (§5, Q4).

**Fig. 5.2(b) — distinct opening sequences against depth.**
`distinct_prefixes(runs, k)` for k = 1…8 per profile at the core horizon; the
baseline is 1 at every k by construction (the suite's structural-zero
convention, stated in the caption, never measured). The ceiling is the seed
count (100).

**Fig. 5.3 — pairwise divergence, printed-value matrix.**
`divergence_report` over the **four profiles only** (the aggregate is excluded
by the fired size kill-criterion), visit-stream half, `n_splits=200`,
`q=0.975`. Off-diagonal: the pair's JSD. Diagonal: each profile's own null
ceiling. The `cleared` verdict is printed beside it; a pair is separated only
where its cell exceeds both diagonals it meets, as the caption says. The
terminal-tactic half is computed and printed (it is underpowered on record)
but not drawn.

**Tab. 5.4 — behaviour without defence, by attacker.** One row per arm at the
core horizon; the extension's columns printed beside for the read, not for
the table.

| Column | Measure | Baseline row |
|---|---|---|
| distinct tactics | `distinct_place_count`, mean [CI] | structural (no tactic vocabulary): distinct verbs, marked |
| deepest stage acted on | `deepest_successful_stage` against `lifecycle_consensus.json`, no-success runs at −1, mean [CI]; ceiling 2 under the partial mapping, footnoted | — |
| distinct openings at depth 5 | `distinct_prefixes(k=5)` / 100 | 1 (structural) |
| path entropy | `path_entropy` pooled; footnoted as hub-occupancy-tracking | 0 (structural) |
| hosts reached | `compromised_count`, mean [CI] | distinct `compromise_host_uuid`, mean [CI] |
| how runs ended | share by `terminal_mode` (objective / horizon / sink_exhausted / other) | objective vs horizon only |
| *read only, not a column:* target reach | fraction reaching the database set; time to target where reached (median; within-arm) | same, from the attack record |

The stealth-spacing column (C11) is **not** computed: the ruling is owed and
the axis-5 badge is blank. If ruled in, `exposure.py` reads the same stream.

## 3. Outputs and where they live

`data/results/ch5_s531_unopposed/` (the prior studies' convention: runner,
analyser and record side by side):

- `run_corpus.py` — the cell set of §1 as a job list; `ProcessPoolExecutor`;
  one JSONL row per run carrying the full per-visit stream (the
  `profile_divergence` row shape) for movement runs, and the attack-record
  rows the baseline adapter needs for baseline runs; errors written as rows,
  never dropped.
- `runs.jsonl` — the corpus (gitignored under `data/results/` as the others
  are; check before staging).
- `analyse.py` — every number for the three floats, printed and written to
  `numbers.json`; the sanity block first (runs per cell, error rows, the
  baseline's structural zeros present, the diagnostic-arm deltas against the
  record's published cells).
- `preview_fig52.png`, `preview_fig53.png`, `preview_tab54.md` — quick
  matplotlib / markdown previews for reading the direction. **Not** the house
  style: the 12 pt TikZ generator (`tools/ch5_unopposed_figures.py`, emitting
  `fig_5-3-1a_coverage_openings` and `fig_5-3-1b_divergence`) and the
  `\tablestyle` fragment follow acceptance of the direction, under
  `figure_table_conventions.md` and the no-accentuation rule.

## 4. What the preliminary read is for — the discussion in view

Three board items rest on what this corpus shows, and the read should say
which way each moved (board: `2026-09-15_ch6_discussion_affinity_board.md`):

- **B.1 profile-divergence attribution.** Fig. 5.3 is read for separation
  among the four profiles only; the aggregate's column stays out. If the four
  still clear their nulls by the record's margins at the chapter's overlay
  and objective, the L3-scoped claim holds at the chapter configuration.
- **Foundation-risk item 8 (stale magnitudes).** Hosts reached, distinct
  tactics and the terminal-mode split supersede every pre-contract, v1-overlay
  figure the notes quote; the analysis prints the deltas.
- **The denominator rule.** Tab. 5.4's last column decides whether "reaches
  none unopposed" still holds under the targeted objective and the database
  target. The probe at seed 0 already shows `objective_exfiltration` reaching
  the target at 10 929 s, so the column may not be all-horizon; if a
  non-degenerate share reaches, the §5.2 sentence that pins success-shaped
  measures at zero at the inherited interval needs the no-defence qualifier
  read carefully, and target reach earns its place beside breadth as Table 5.2
  already allows.

## 5. Rulings owed before launch

| # | Question | Recommendation |
|---|---|---|
| Q1 | The cell set of §1 as the §5.3.1 corpus | accept |
| Q2 | Run the 60 000 s extension in this batch | yes; free of the dose confound at no defence; reads C36 |
| Q3 | Run the general-objective diagnostic arm | yes; the only way to attribute a moved number to the objective switch |
| Q4 | The baseline reference in Fig. 5.2(a): six verbs, or three grouped activities | six verbs drawn, caption corrected — the honest count; grouping is an editorial choice that needs a decode |
| Q5 | Opening depth: fan k = 1…8; table column at k = 5 | as stated (k = 5 is the record's convention) |
| Q6 | Stealth-spacing column (C11) | not computed until ruled |

## Validation gate

`runs.jsonl` holds 1 200 rows (+ 500 diagnostic) with zero error rows;
`analyse.py` reproduces bit-for-bit on a second invocation; the baseline
rows show the structural zeros and only the objective / horizon terminal
pair; every interval printed; the three previews exist and each number a
caption could quote is in `numbers.json`.

## Hard constraints

- Readers only in the analysis: no simulation, no RNG outside the seeded
  split-half null.
- The overlay version is passed by name; a run at the registry default is a
  different configuration and is not this corpus.
- No float in the tex is populated from a preview; the TikZ generator and the
  table fragment are the only route into `docs/thesis/`.
- Same seeds on every arm; every cross-arm comparison unpaired (Table 5.3).
- Branch and commit rules per `session_workflow.md`; `data/results/` records
  stay unstaged if gitignored.

## Reading list

- `docs/thesis/dissertation.tex` §5.3.1 (`subsec:aio-unopposed`) — the three
  floats and their captions, which fix what is measured.
- `docs/thesis/tables/tab_5-2a_factors_varied.tex`, `tab_5-2b_factors_fixed.tex`
  — the levels and pins.
- `src/mtdsim/l3_simulation/movement/run.py` — `run_movement` and
  `_install_objective`.
- `src/mtdsim/l3_simulation/movement/measures.py` §1–§2, §7 — the measures.
- `data/results/profile_divergence/run_study.py`,
  `data/results/targeted_attacker_build/run_gate0.py` — the recorder shapes
  reused.
- `docs/implementation/pipeline/ogasp/plurality_reporting.md`,
  `profile_divergence_findings.md` — the record the preliminary is read
  against.

## Out of scope

§5.3.2's disruption cells; any defence condition; the §5.1 re-run; the
size-matched label-blind control (C19); the TikZ generators before the
direction is accepted; any change to the captions or prose in the tex.
