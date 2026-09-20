---
status: findings — preliminary read 2026-09-15; the §6 changes APPLIED the same day (Marc: "do the necessary updates"): floats landed in the tex via tools/ch5_unopposed_figures.py; captions DRAFT STATE, voice pass owed
created: 2026-09-15
topic: "The §5.3.1 no-defence corpus at the chapter's declared configuration (targeted objective, database target, failure-only overlay, 100 seeds): what Figures 5.2 and 5.3 and Table 5.4 look like, what moved against the record and why, and the four changes the floats need before they are drawn in the house style"
---

# §5.3.1 Without defence — the preliminary read

**Design:** [`../../../handoffs/2026-09-15_ch5_s531_unopposed_runs.md`](../../../handoffs/2026-09-15_ch5_s531_unopposed_runs.md)
(accepted by Marc 2026-09-15, §1). **Workspace:** `data/results/ch5_s531_unopposed/`
(gitignored, as every `data/results/` study is): `run_corpus.py` → `runs.jsonl`
(1 700 runs, 151 MB); `analyse.py` → `numbers.json`, `preview_tab54.md`,
`preview_fig52.png`, `preview_fig53.png`. Every measure is the shipped suite's
(`movement/measures.py`); the analysis is a reader. Previews are matplotlib
for direction only; the house-style generators are owed (§6).

## 1. Configuration and sanity

Six arms × 100 seeds (0–99, shared) × {15 000 s core, 60 000 s extension}, no
defence, `attack_objective="targeted"` on the database set, `v2_partial`,
**`overlay_version="v4_failure_only"` passed by name** (the registry default is
still `v1_band_relationship`), synthetic overlay on, retrace on, fresh-host
contract on, modulators off. Diagnostic arm: the five movement arms at
15 000 s under `general`. Wall: 238 s on six workers. Zero error rows; every
cell at 100; no `max_events` termination. Bit-identical on re-invocation.

## 2. Table 5.4 — behaviour without defence, core horizon (15 000 s)

Mean [95 % interval]; openings at k = 5 out of 100 seeds; entropy pooled with
the largest single-place visit share beside it.

| attacker | distinct tactics | deepest stage acted on | openings k=5 | path entropy (hub share) | hosts reached | ended target / horizon | median time to target (s) |
|---|---|---|---|---|---|---|---|
| exfiltration | 13.60 [13.50, 13.70] | 2.00 [2.00, 2.00] | 76 | 2.244 (0.17) | 7.44 [6.86, 8.02] | 0.11 / 0.89 | 13 557 |
| impact | 11.81 [11.73, 11.89] | 2.00 [2.00, 2.00] | 35 | 2.014 (0.16) | 9.95 [9.05, 10.85] | 0.13 / 0.87 | 11 202 |
| double extortion | 14.00 [14.00, 14.00] | 2.00 [2.00, 2.00] | 14 | 2.059 (0.17) | 7.92 [6.98, 8.86] | 0.05 / 0.95 | 12 640 |
| no realised objective | 12.81 [12.73, 12.89] | 2.00 [2.00, 2.00] | 30 | 1.929 (0.20) | 7.21 [6.45, 7.97] | 0.07 / 0.93 | 11 170 |
| aggregate | 14.68 [14.59, 14.77] | 2.00 [2.00, 2.00] | 85 | 2.810 (0.14) | 8.74 [8.10, 9.38] | 0.17 / 0.83 | 10 508 |
| baseline attacker | 6 verbs (structural) | — | 1 (structural) | 0 (structural) | 24.34 [22.47, 26.21] | 0.58 / 0.40 (+0.02 on the 80 % ratio) | 9 360 |

- **Distinct-tactics ordering is supported** (every adjacent pair CI-disjoint):
  aggregate > double extortion > exfiltration > no realised objective > impact.
  Double extortion sits at exactly 14.00 in all 100 runs — its net has 14
  reachable places and the walk covers all of them every time.
- **Hosts ordering is not supported** — every adjacent pair overlaps, as the
  predesign's power arithmetic said it would at 100 seeds. The family-level
  contrast is the reportable object: the baseline at 24 hosts against 7–10.
- **Deepest stage acted on is 2.00 ± 0.00 on every profile** and no run has
  zero successes. Under the partial mapping the objective band is dwell-only,
  so the ceiling is 2 and every run reaches it: the column discriminates
  nothing, exactly as `measures.py` §(c) predicted. See §6.
- **The baseline's "objective" ending is two things.** Its `end_event` fires
  on the target *or* on the inherited 80 % compromise ratio (41 hosts): 2 of
  100 runs at the core horizon and 5 at the extension ended on the ratio with
  no database host held. The table splits them; the movement attacker never
  reaches the ratio (max ≈ 21 hosts).
- Time to target is a within-arm quantity (Table 5.3's comparability rule);
  it is read here for direction only.

## 3. Figure 5.2 — coverage and opening variety

**(a) Coverage.** Every profile enters 90 % of the tactics it will ever
enter by 1 500–2 000 s and 99 % by 7 000–11 000 s; the baseline's six verbs
are all reached by 500 s and the line is flat from 1 500 s. On a 15 000 s
linear axis the figure is a step at the origin and a plateau — the placeholder's
"overview + zoom if the early region is crowded" case has arrived (§6). The
right-censoring rule (a run that reaches the target holds its final value)
moves nothing visible: reaching runs are 5–17 % and reach late (10–14 ks).

**(b) Opening variety.** Every profile opens on one place at k = 1 (the
reconnaissance seed) and fans out at its own rate: aggregate and exfiltration
reach the 100-seed ceiling by k = 7–8; impact and no realised objective by
k = 8; double extortion holds 14 at k = 5 and 30 at k = 8. The baseline is 1
at every k, stated structurally. The record's ten-seed ordering
(`plurality_reporting.md` §2: exfiltration and aggregate fastest, double
extortion slowest) reproduces at 100 seeds; the impact / no-realised pair is
too close to order (35 vs 30 at k = 5, 65 vs 61 at k = 6).

## 4. Figure 5.3 — divergence against the split-half null

Visit-stream JSD, four profiles, 200 splits, q = 0.975. Diagonal = own null
ceiling.

| | exfiltration | impact | double extortion | no realised objective |
|---|---|---|---|---|
| exfiltration | **0.0004** | 0.137 | 0.137 | 0.078 |
| impact | 0.137 | **0.0005** | 0.071 | 0.156 |
| double extortion | 0.137 | 0.071 | **0.0007** | 0.208 |
| no realised objective | 0.078 | 0.156 | 0.208 | **0.0004** |

All six pairs clear both diagonals they meet by 100–500×; the closest pair is
impact ↔ double extortion (0.071), the farthest double extortion ↔ no realised
objective (0.208) — the same extremes as the 50-seed record (0.081 and 0.237).
The terminal-tactic half (not drawn) clears on 2 of 6 pairs and is inside the
null on the rest, as before: underpowered at 100 terminal draws.

**Consequence for the drawing:** the null ceilings are three orders of
magnitude below the off-diagonals, so "fill shaded from the null upward" makes
the diagonal white and the caption's rule is carried entirely by the printed
values. The printed-value matrix genre is right; the shading is decorative
here.

## 5. The extension and the diagnostic arm

**60 000 s.** Coverage and openings are unchanged (the walk has covered its
net by 10 ks). Hosts and target reach are not:

| attacker | hosts | ended target / horizon | median time to target (s) |
|---|---|---|---|
| exfiltration | 17.16 [15.53, 18.79] | 0.58 / 0.42 | 24 554 |
| impact | 21.31 [19.49, 23.13] | 0.64 / 0.36 | 24 271 |
| double extortion | 9.21 [7.91, 10.51] | 0.05 / 0.95 | 12 640 |
| no realised objective | 20.10 [18.34, 21.86] | 0.36 / 0.64 | 38 932 |
| aggregate | 20.07 [18.19, 21.95] | 0.60 / 0.40 | 24 609 |
| baseline | 25.17 [23.19, 27.15] | 0.67 / 0.28 (+0.05 ratio) | 10 277 |

Three profiles and the aggregate reach the database target in a majority of
unopposed runs at 60 000 s, at 17–21 hosts against the baseline's 25. Double
extortion does not move (9 hosts, 5 % reach at either horizon): its 100 runs
plateau — every one ends at the horizon, none sinks — so it is a campaign
that covers its net and then idles, not one that is cut short. That is the
profile the discussion's "structure runs, outcome does not follow" line is
about, and it is now one profile rather than all five.

**General objective (diagnostic, not a chapter cell).** Targeted minus
general: distinct tactics −0.02 to 0.00; path entropy within ±0.003 bits;
openings at k = 5 identical on every profile; every divergence cell within
±0.001; hosts −0.07 to −0.57 (targeted runs that reach end early); target
reach 0 → 0.05–0.17. The objective switch touches the terminal column and
nothing else in §5.3.1: Fig. 5.2 and Fig. 5.3 are objective-invariant.

## 6. What the floats need changed — for Marc (APPLIED 2026-09-15)

*Applied as recommended, with one substitution: the advance-after-first-success
share turned out to be saturated too (every run's first success is at stage 0,
reconnaissance, and every run later succeeds at stage 2, so it reads 1.00 on
every profile at both horizons and under both objectives). The column that took
the depth column's place is therefore* **successes per distinct host** *— the
repetition measure `measures.py` §(c) names as persistence-in-outcome (20–37 on
the profiles; 1–8 zero-host runs per profile excluded and counted). Fig. 5.2 is
three lettered panels (overview, first 3 000 s, openings); Fig. 5.3 a printed
matrix with a grey ramp on the off-diagonal; Tab. 5.4 gains target reached and
ended-at-horizon and loses the depth column; the baseline reference is six
activities and the caption says so. Generator: `tools/ch5_unopposed_figures.py`.*


1. **Fig. 5.2(a) needs a zoom or a log-time axis.** Saturation inside 2 000 s
   on a 15 000 s axis leaves the panel with no discriminating region.
   Recommended: overview + a 0–3 000 s zoom as lettered panels (the
   placeholder's own contingency), or a log-time axis, which the corpus does
   draw for time courses. The extension changes nothing in this panel and
   need not be drawn.
2. **Tab. 5.4's "deepest stage acted on" column is saturated** (2.00 ± 0.00
   on every row) under the partial mapping and should be replaced or dropped.
   The suite's replacement is the advance-after-first-success share
   (`advanced_after_first_success`), the measure the axis-1 criterion actually
   uses; recommended as the column, with the ceiling stated in the footnote.
3. **The "how runs ended" column is no longer all-horizon.** Under the
   targeted objective the profiles reach the database target unopposed in
   5–17 % of runs at 15 000 s and 36–64 % at 60 000 s. The sentence in §5.2
   that pins success-shaped measures at zero at the inherited interval was
   written on the general-objective record; whether it survives is a
   §5.3.2 / §5.4 question (under defence), but §5.3.1's own denominator
   sentence should say "reaches the target in a minority of unopposed runs at
   the lineage horizon", not "none". Target reach earns its column beside
   breadth in Table 5.4, as Table 5.2's objective row already allows.
4. **The baseline reference line in Fig. 5.2(a) is six verbs**, flat from
   1 500 s; the caption's "three activities" needs correcting to six, or the
   grouping decoded (Q4 in the handoff — Marc's ruling still owed; the preview
   draws six).

Two smaller items: Fig. 5.3's shading is decorative at these null magnitudes
(printed values carry the rule); and the aggregate's extra row in Table 5.4
reads as the largest coverage and the most openings, which is what a union
net should do and is not objective conditioning (the size confound stands).

## 7. Against the record

| quantity | record (config) | here | what moved it |
|---|---|---|---|
| pooled path entropy, five profiles | 2.195 / 2.033 / 1.972 / 1.451 / 2.714 (10 seeds, v1 overlay, general) | 2.244 / 2.014 / 2.059 / 1.929 / 2.810 | no-realised-objective +0.48 bits: the failure-only overlay and the fresh-host contract, not the objective (diagnostic arm) |
| openings at k = 5 | 10 / 9 / 2 / 4 / 7 of 10 seeds | 76 / 35 / 14 / 30 / 85 of 100 | same ordering; impact / no-realised now too close to order |
| between-class JSD range | 0.081–0.237 (50 seeds, v1, general) | 0.071–0.208 | same extreme pairs; every pair still clears its null by two orders |
| hosts, no defence | 6.0–6.8 (v1, general, pre-contract) | 7.2–10.0 | the fresh-host contract (board item 8: 5.13 → 7.92) |
| database reach, movement | 1.4 % (H5) → 9.7 % aggregate (Gate 0, v1, retrace off) | 17 % aggregate; 5–13 % profiles | overlay v4 + retrace on |

Nothing here re-scores a badge; the preliminary is for direction.

## 8. Validation

Zero error rows; 100 runs in every cell; baseline structural zeros present;
`ordering_supported` printed for the two orderable columns (hosts False,
tactics True); second invocation of `analyse.py` byte-identical.

## Addendum 2026-09-20 — the baseline's openings are measured, and the campaign figure is reworked

The analyser had the baseline attacker's distinct openings hard-coded to one at
every length and its path entropy to zero, both labelled structural. Measured
from the recorded runs (activity sequences, 100 runs, 15 000 s): one ordering up
to length 6, two at length 7, four at length 8; 94 % of runs on the commonest
length-8 opening; entropy 0.43 bits over activities. The branching is where an
exploit fails. `analyse.py` now measures both, and adds two measures the
reworked figure reads: `tactic_entry_share` (share of runs entering each tactic)
and `commonest_opening_share` (not capped by the run count, unlike the count of
distinct openings). Each profile's coverage plateau equals the number of tactics
it ever enters (14, 12, 14, 13), so the old coverage curves were construction
facts and are no longer drawn. Design and rulings: results context §8
(`docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md`).

### Same day, second pass — the baseline's step unit

The first measurement above counted every baseline record as a step; 77 % of
those are consecutive repeats of one phase, where a profile record never repeats
its predecessor. Counted as phases ENTERED (repeats collapsed), the baseline has
one opening to length 4 and two from length 5, 78 % of runs on the commonest
(after the exploit, 78 go to brute force and 22 to scanning neighbours); entropy
0.41 bits. These supersede the 1,1,1,1,1,1,2,4 and 94 % figures. `analyse.py`
also writes `tactic_visit_share`, which the figure's panel (a) now reads, with
held-and-never-entered tactics at 0.0.
