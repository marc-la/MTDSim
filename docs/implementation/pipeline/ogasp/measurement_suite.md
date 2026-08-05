---
status: durable
created: 2026-07-28
updated: 2026-08-05
topic: "The axis-measurement suite (movement/measures.py) — the M8b measurements the APT criterion's claimed axes need, built as a reader over MovementRecord streams with a baseline-arm adapter; which axis each measure discharges, its validation gates, and its known blind spots. Now also carries the defender-side disruption ledger (§5 of the module), which scores no axis and prices the frontier"
---

# The axis-measurement suite — what each measure is, which M8b field it discharges, and where it is blind

**Status:** durable; the tracked account of the measurement suite the
wave-5 handoff `2026-07-28_axis_measurement_suite.md` commissioned (closed by
the commit that ships this record). The criterion
([`../../apt_model_criterion.md`](../../apt_model_criterion.md)) cites this file
when a badge decision needs a measurement; the demonstration-arms handoff and
the axis-6/axis-7 builds consume the functions it names.

**The module:** `src/mtdsim/l3_simulation/movement/measures.py`, sibling to the
existing MTTC/ASR reader (`statistics.py`, left intact apart from a public
alias for its compromise-event set). **Reader contract throughout:** pure
functions over `MovementRunResult`s — no simulation, no RNG, no mutation; the
inherited `AttackStatistics` maths is untouched (M7, D5) and the baseline arm
is reached only through a row adapter. The unit gate is
`tests/l3_simulation/test_movement_measures.py` (hand-constructed record
streams with hand-worked expected values; two seeded integration checks).

## (a) Why these measures exist

The criterion's §(f) finding: the metric suite could score axes the model holds
no claim on, and could not score the axes it claims. Every claimed axis's
*what-would-evidence-a-claim* (M8b) field names measurements that did not
exist; this suite is that list built. Three constraints from the two sweeps
bind every consumer:

1. **The degenerate region** (rate feasibility study §7 C5): at the operating
   200 s mutation interval neither attacker completes the objective, so ASR
   discriminates nothing there. The suite computes no ASR; its measures are
   breadth-, event- and time-shaped quantities that stay informative inside
   the region.
2. **The saturated depth measure** (criterion §(h)): deepest *visited*
   lifecycle stage cannot discriminate. §(c) below reports the replacement and
   the check it was required to pass.
3. **Ten seeds separate almost nothing**: every aggregate is reported through
   `interval_report`, which returns means, 95 % intervals and the adjacent
   pairs whose intervals are disjoint — `ordering_supported` is true only when
   every adjacent pair separates, so an unseparated ordering cannot be
   rounded up silently.

## (b) The measures, by axis

| Measure (function) | Axis / M8b field discharged | Definition | Known blind spots |
|---|---|---|---|
| `distinct_place_curve` / `distinct_place_count` | 1 — "distinct-tactic coverage over time" | count of distinct places visited by sim time *t* (curve + end scalar) | counts engagement, not success; saturates only at 15 places |
| `deepest_successful_stage` | 1 — replacement for the saturated kill-chain depth | deepest consensus stage (`lifecycle_consensus.json`) with a **success verdict**; no-success runs encode as −1, never dropped | under `v2_partial` the objective band is dwell-only, so stage 3 can hold no verdict and the ceiling is 2 (§(c)); stage model is the declared consensus, not ATT&CK's |
| `deepest_visited_stage` | 1 — kept only as the saturated comparator | deepest stage merely visited | saturated by construction; do not report as progression |
| `foothold_retentions` | 1 — "foothold-retention duration across MTD mutations" | sim time from each compromise event to the next **network-layer** interrupt (where the substrate clears the host cursor); censored at run end otherwise, censoring reported | records carry no host identity → measures retention of *position*, not of a named host |
| `successes_per_distinct_host` / `actions_per_distinct_host` | 1 — "effort-to-breadth conversion ratio" (experiment 1 finding 2, formalised) | successful (resp. attempted) actions per distinct host; `None` at zero hosts — the infinite ratio is the finding | per-run form undefined at zero hosts; use cell totals alongside |
| `path_entropy` | 3 — "path entropy over the net" | visit-weighted Shannon entropy (bits) of empirical out-transitions, from the records (the walk taken, not the net's declared branching) | pools places; a single high-traffic hub can dominate |
| `distinct_sequences` / `distinct_prefixes` | 3 — "distinct tactic-sequences across seeds" | unique place-sequences / length-*k* prefixes across runs | whole sequences are seed-sensitive; prefer prefixes for cross-seed claims |
| `profile_divergence` (via `jsd`, `visit_distribution`, `terminal_place_distribution`) | 2 (stronger claim) + 3 — "mirroring the L2 corpus-level check at the execution level" | pairwise Jensen–Shannon divergence between profiles' pooled visit streams and terminal-tactic distributions, in the L2 convention (`jensenshannon(p,q,base=2)**2`, union support) | no null band yet (the L2 check calibrates one; an execution-level null is future work) |
| `interrupt_action_mix` | 4 — "change in action mix before vs after an MTD trigger" | verb and place-class mixes in the *n* visits before vs after each interrupt, pooled within run (paired, so seed variance cancels); dwell-only visits appear as `""` | windows near run edges are short; overlapping windows around interrupt bursts double-count visits |
| `recovery_times` | 4 — "recovery time from an MTD-induced state throw-back" | sim time from each interrupt to the next success verdict; censored at run end, reported as such | "recovery" = any success, not recovery of the lost position specifically |
| `failure_routing_rate` | 4 — "does failure-conditioned routing measurably redirect effort" | fraction of verdict-carrying routing decisions taken on the failure column (correlate with breadth across runs) | rate only; the correlation and its interval are the caller's, via `interval_report` |
| `terminal_mode` | 4 / reporting | experiment 1's terminal vocabulary formalised (objective / sink / sim_end / max_events / horizon / empty) | baseline rows cannot say more than objective-vs-horizon; cross-arm terminal comparison uses that coarser pair |
| `cost_ledger` | 6 prerequisite — "a cost ledger per run (actions, time, re-work forced by MTD)" | attempts by verb (split blocked / dwell-only), time decomposed into behavioural dwell + derived MTD confusion penalty + residual, re-work (interrupt count and the time MTD-cut events consumed), distinct hosts, yield per ksec | the ledger is a *measurement*, not an axis-6 claim — the claim needs a decision rule that consumes it (separate handoff); time fields are movement-arm-only |
| `disruption_ledger` / `disruption_from_run` (+ `union_time`) | **no axis, deliberately** — the defender-side cost the frontier trades attacker measures against ([`mtd_disruption_frontier.md`](mtd_disruption_frontier.md)) | per run, derived entirely from the substrate's own per-mutation operation records: reconfiguration **occupancy** (union of mutation deployment windows ÷ elapsed), summed window time by resource layer and by mechanism, churn tempo (executions per ksec), and the suspended-mutation contention tally. The run result snapshots the record read-only after the run (`run.mtd_snapshot`); both arms read the identical machinery, so defender-side quantities are cross-arm safe — unlike attacker-side time | a mutation aborted mid-execution on compromise appends no record; a same-priority discard is tallied nowhere; queue wait under the simultaneous scheme is outside the window — all three undercount, so occupancy is a floor |
| `progress_trajectory` / `projected_effort_curve` / `abandonment_effort` / `abandonment_curve` / `disengagement_snapshot` (+ `baseline_progress_trajectory`) | **6's economic claim, scored as an *outcome* — deliberately no badge move.** Axis 6 asks whether the attacker *conditions on* cost and closed as DESIGNED; this reads where it would have quit | **Projected Campaign Effort** `T(t) = t + (W − h(t))/r(t)`, `r(t) = (h(t)+α)/(t+α/r₀)` — projected total campaign effort after each attempted action. **Abandonment Effort** `A(k)` is the *first* `t` where PCE exceeds `B = k·U` (`U = W/r₀ = 1 440` actions, the unimpeded effort to the objective), censored otherwise. Reported as the **Disengagement Frontier**: mean `A(k)` against patience `k`, per condition, censoring beside every point ([`attacker_disengagement.md`](attacker_disengagement.md) §1.2 names all three) | the conditional mean conditions on abandoning — the censoring fraction moves with the defence where the mean does not, and that half is un-pre-registered (§5 there); the horizon caps observable patience, so `k ≥ 7.5` is mostly censored and `k = 10` pins at the horizon in every condition; movement-arm progress is a sampled substrate count (`n_compromised`) while the baseline's is a deduplicated identity count — equally exact by different routes, and the asymmetry is stated, not smoothed |
| `baseline_ledger` / `comparable_from_baseline` / `comparable_from_movement` | cross-arm subset (Jin's stealthy-vs-baseline framing) | see §(d) | see §(d) |
| `mean_ci` / `interval_report` | reporting discipline (every axis) | experiment-1 mean ± 1.96·SEM convention; adjacent-pair disjointness made routine | normal approximation; n = 1 reads as a zero-width interval |

**The confusion-penalty derivation (instrumentation gap 1, closed by
derivation, not schema change).** The penalty is consumed inside the
substrate's `apply_mtd_interrupt_cost` *before* the interrupted event's record
is appended, so it sits inside that record's `end_time − start_time − dwell`;
under S3-R every non-interrupted event's value of that expression is 0 (the
movement layer's draw is the whole duration and `step` spends exactly it).
`mtd_penalty(record)` reads the penalty off interrupted records on that basis.
The seeded-run test verifies both halves rather than assuming them: on a live
MTD run, non-interrupted records close at `start + dwell` to 1 e−9, the record
stream is gapless (the penalty cannot hide between records), and the ledger
reconciles `time_active = time_dwell + time_mtd_penalty + time_residual`.
`time_residual` is kept visible as a regime tripwire: a returning nonzero
value on non-interrupted events means the substrate is pricing movement-arm
actions again, which would be an S3-R regression.

**Instrumentation gap 2, stated rather than papered over.** The driven arm
writes no interrupt row to `attack_record.csv`, so a ledger built from the
substrate CSV is native-arm-only. The movement arm's ledger is built from
`MovementRecord`s; the baseline's from its rows via the adapter. The two
ledgers say what they are; there is no pretence of one ledger measuring both.

## (c) Gate 3 — the replacement progression measure, checked, with a split verdict

Required check: on the five profiles, deepest-*successfully-actioned* stage
must separate at least one adjacent pair that deepest-visited stage does not
(a second saturated measure adopted unchecked being exactly the failure §(h)
records). Run on the no-MTD arm, ten seeds (0–7, 42, 1234), horizon 15 000 s,
under both mappings; no-success runs encoded as depth −1.

- **Deepest visited stage: exactly saturated, both mappings.** All five
  profiles read 3.0 ± 0.0. Zero adjacent pairs separate — §(h)'s finding
  reproduced by the suite itself.
- **Under `v1_ckc_total` (experiment 1's mapping): the replacement
  discriminates.** `pure_steal` 0.0 ± 0.0, `aggregate` 1.5 ± 0.98,
  `pure_impediment` 2.7 ± 0.59, `double_extortion` 3.0 ± 0.0,
  `infrastructure_setup` 3.0 ± 0.0. One adjacent pair is CI-disjoint
  (`pure_steal`–`aggregate`); the gate's criterion (≥ 1 pair that visited
  depth cannot separate) is met.
- **Under `v2_partial` (the go-forward mapping): no adjacent pair separates —
  and half of that is structural, not power.** Seven tactics are dwell-only
  under `v2_partial`, including the objective band, so a stage-3 place can
  dispatch no verb and hold no success verdict: the measure's ceiling drops
  to 2, and four profiles sit at exactly 2.0 ± 0.0 with `double_extortion` at
  1.6 ± 0.52. This is mapping-induced censoring of the top stage, recorded
  here as the measure's principal blind spot under partial mappings.

**Disposition:** `deepest_successful_stage` is adopted as the axis-1
progression measure, with two riders that must travel with any use: (i) under
a mapping whose objective band is dwell-only its range is truncated and it
must be read jointly with the coverage curve (`distinct_place_curve`), which
discriminates in exactly the band the depth measure cannot see; (ii) no
ordering of the five profiles is claimable from it at ten seeds — one
separated pair is not an ordering, and `interval_report` says so.

## (d) The cross-arm subset — event-wise enforced in the API

The supervisor's stealth framing needs the profiled attacker compared against
the inherited baseline on behaviour-shaped qualities, which is impossible if
the measures exist for one arm only. The baseline emits `AttackStatistics`
rows, not `MovementRecord`s, so the suite carries an **adapter**
(`baseline_ledger`, reading rows — DataFrame or dict-rows — and touching
nothing) and one comparable type:

- **`EventWiseComparable` carries no time-denominated field, by
  construction.** Under S3-R the movement layer prices all of that arm's time
  while the baseline runs on substrate pricing, and the timing design record
  withdrew cross-arm comparability of internal MTTC rather than defending it.
  Fractions-of-steps, counts and per-host ratios are invariant to that; a
  per-unit-time rate is not. Time quantities exist only on the per-arm
  ledgers, whose docstrings say they are arm-local. The unit test asserts the
  comparable type has no `time` field, so the enforcement is regression-guarded.
- **Structural zeros are reported, not omitted.** The baseline's
  `blocked_fraction` is 0.0 because its scripted order *is* the native
  precondition order (the H-coupling contrast); its `dwell_only_fraction` is
  0.0 because it has no non-action concept. The zero with its reason is the
  contrast the comparison exists to show.
- **What the baseline rows cannot say is surfaced as unknown**, never guessed:
  `reached_objective` is `None` unless the runner supplies it; terminal modes
  collapse to objective-vs-horizon on that arm.

Gate 4b ran as a test: the subset computes on one seeded run of each arm,
field-for-field, same keys both sides.

## (e) Validation record (gates 1–5)

1. **Unit gate:** 27 tests, every measure on a hand-worked stream
   (`test_movement_measures.py`); the interval helper is exercised by a
   measure's own aggregation test (three synthetic profiles; the report
   exposes exactly which adjacent pair separates and refuses the ordering).
2. **Reproduction gate:** `run_experiment.py` was re-run fresh on the current
   substrate (2026-07-28; prior workspace numbers preserved at
   `numbers_2026-07-23_prebaseline_backup/`), then the suite re-derived its
   figures from re-created runs (determinism ⇒ identical records):
   **50 runs × 5 fields cross-checked with zero mismatches** (blocked
   fraction, event count, success count, hosts, terminal mode). The published
   shape reproduces with moved magnitudes, as the gate anticipated — the
   substrate was re-baselined (`dd8c5ec` / `06ed8d9`) and the timing regime
   became S3-R after experiment 1's numbers were taken:
   - blocked-fraction profile: `pure_steal` 94.7 % ± 2.3 (published ≈ 95 %),
     `infrastructure_setup` and `double_extortion` 0.0 % (published 0 %),
     `aggregate` 74.9 %, `pure_impediment` 34.0 %;
   - effort-to-breadth (cell totals, no-MTD): baseline ≈ 36 attempted
     actions per distinct host (published ≈ 20) against
     `infrastructure_setup` ≈ 314 attempted (≈ 277 successful) per distinct
     host (published ≈ 210) — the order-of-magnitude gap holds;
     `pure_steal` still converts its whole budget into zero hosts.
3. **Gate 3:** §(c) above — run and reported under both mappings.
4. **Gate 4/4b:** interval helper exercised in-suite; cross-arm subset
   computed on both arms by test.
5. **Determinism:** the full `tests/l3_simulation` suite (332 tests, SIM-05
   determinism cells included) and the substrate/carve/golden suites (43
   tests) pass unchanged — the suite is a reader and moved nothing.

Regeneration: `PYTHONPATH=src python data/results/measure_suite_validation/validate.py`
(after a fresh `run_experiment.py`); outputs land untracked in that workspace's
`numbers/validation_report.json`, per the experiment-workspace convention. The
MTD-condition demonstration block in the same report shows the defender-response
and foothold measures operating on real interrupts (e.g. `pure_impediment`
under random MTD @ 200 s: ~58 interrupts/run, ~1 190 s/run of derived confusion
penalty and ~3 340 s/run of MTD-destroyed event time — the re-work line items
axis 6's decision rule will consume; `infrastructure_setup`'s 65 foothold
retentions all end in a network-layer sever, none censored, which is the MTD
mechanism made visible).

## (f) What consumers must respect

- **No ASR at the operating interval** — measure outside the degenerate
  region or report breadth/elapsed time and say why ASR was dropped.
- **No ordering claim without disjoint intervals** — report
  `IntervalReport.separated_adjacent_pairs`; `ordering_supported` is the
  gate, not the sorted means.
- **No time-denominated cross-arm comparison** — use `EventWiseComparable`;
  if a time quantity must be shown across arms, it carries the S3-R pricing
  asymmetry explicitly.
- **Censoring is data** — `CensoredDurations.observed` and `.censored` are
  reported separately; a pooled mean understates every censored duration.

## (g) Lifecycle

Extend this suite (and bump `updated`) when: the demonstration-arms handoff
pre-registers its badge criteria (it consumes §(b)'s measures verbatim);
~~the axis-6 decision rule lands (it consumes the ledger)~~ **fired 2026-07-29
— the ledger was consumed as designed and needed no extension, reported per run
and per arm across the rationality-exponent sweep
([`incentive_rationality.md`](incentive_rationality.md) §6.4). Two things the
consumption verified rather than assumed: `time_residual` read 0.00 at every
sweep point, so the S3-R regime tripwire this suite installed did not fire under
a conditioned attacker; and the near-flat interrupt count against an eightfold
rise in attempted actions is what let the sweep separate "interrupted more" from
"failed more" straight off the ledger. One gap the consumption exposed and did
not close: the ledger carries no **per-tactic** cost decomposition, so the
question of whether MTD taxes some tactics more than others had to be answered
by a separate diagnostic (`mtd_tax_anatomy.py` in that workspace). A per-place
interrupt/penalty breakdown is the natural extension if a second consumer needs
it**; experiment 2 fixes its
mutation interval (re-check which measures sit inside the degenerate region at
the chosen tempo); or a stealth semantics is ruled (axis 5's exposure metric is
deliberately absent here — it presupposes that ruling). If `MovementRecord`
gains fields, prefer extending the reader over widening the record: the
penalty derivation shows a gap can close without a schema change.

**Fired 2026-08-01 — the defender side joined the suite.** The rational-attacker
handoff's Part 2 needed the defence's own cost, and no reader could reach it:
`run_movement` discarded the network, so the substrate's per-mutation operation
record (name, deployment window, resource layer — kept by `MTDStatistics` since
the lineage began) was invisible. The gap closed **half by widening, half by
derivation**: the run *result* (not `MovementRecord`) gained a read-only
post-run snapshot of that record, and everything else is derived in the reader
(`disruption_ledger`, §(b) row). The record/reader preference above was
honoured in the way that matters — the per-event schema is untouched, and the
widening carries raw substrate rows, never a computed quantity.

**Fired 2026-08-02 — the disengagement readers joined the suite (§8 of the
module), and this is the one time the record/reader preference lost on
evidence.** The design assumed cumulative compromise *events* could proxy the
distinct-host trajectory; measured before anything was built, 837 events stood
against 155 distinct hosts, and the over-count was itself MTD-dependent (5.4–8.8
without MTD against 1.8–3.5 with it), so using events would have biased exactly
the MTD-versus-no-MTD comparison the measure exists to make. `MovementRecord`
therefore gained one integer, `n_compromised`, asserted monotone, duplicate-free
and equal to `compromised_count` at the horizon. That is the burden of proof this
suite puts on a schema change, discharged by measurement rather than argued
around — and no golden moved, because the field is popped from the golden
serialisation exactly as `retrace` is, on the principle that only behaviour may
move a digest.

**Naming ratified 2026-08-05**, after the readers had shipped: **Projected
Campaign Effort** (the trajectory), **Abandonment Effort** `A(k)` (the scalar,
never quoted without its `k`) and the **Disengagement Frontier** (the report).
Use those terms in prose; `attacker_disengagement.md` §1.2 carries the mapping to
the function names and the three usages that are wrong.
