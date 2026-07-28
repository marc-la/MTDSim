---
status: open
created: 2026-07-28
---

# Build the measurement suite the APT criterion's claimed axes need — progression, diversity, defender-response and cost, computed from the records the movement layer already emits

**Chain position: wave 5, first.** Nothing depends on a ruling and nothing touches the
model. This is a **reader** over `MovementRecord` streams, and it is the prerequisite for
every badge decision in `2026-07-28_axis134_demonstration_arms.md`, for the cost half of
`2026-07-28_axis6_incentive_rationality.md`, and for the within-run learning signals in
`2026-07-28_axis7_learning_capability.md`. It should land **before experiment 2 runs**,
because experiment 2 already owes a supplementary-measurements review and the run
workspace is gitignored — a measurement not computed at run time means re-running.

## State of play

**The criterion can score axes the model holds no claim on, and cannot score the axes it
claims.** That sentence is `apt_model_criterion.md` §(f)'s own finding, and it is the
reason this handoff exists. Every axis in §(d) carries a fifth field — *what would
evidence a claim (M8b)* — and each of those fields names measurements that **do not
exist**. The suite below is that list, made concrete.

**What is measured today.** `src/mtdsim/l3_simulation/movement/statistics.py` is the whole
movement-arm reader: `MovementRunResult` (records + `reached_objective` +
`termination_time` + `compromised_count`, plus `first_compromise_time()`) and
`ProfileSummary` (`asr`, `mttc`, `n_compromising_runs`, `mean_events`,
`mean_compromised_hosts`). Six numbers. Experiment 1's more interesting figures — the
blocked/failed/recon-success/compromise-success action-budget decomposition, and the
actions-per-distinct-host ratio that produced finding 2 — were computed **ad hoc in the
gitignored run workspace** and exist nowhere in tracked code.

**What the records already carry.** `MovementRecord`
(`src/mtdsim/l3_simulation/movement/attacker.py:147-175`) is richer than the reader uses:
`place`, `verb`, `outcome`, `verdict`, `interrupted`, `blocked`, `next_place`,
`start_time`, `end_time`, `dwell`, `interrupted_by`, `place_class`, `step_index`.
Critically, since S3-R the record decomposes an event into behavioural dwell and the
dispatched verb's own cost (`end_time - start_time - dwell`), and `place_class`
distinguishes a dwell-only visit from a failed action — without which an action-budget
decomposition silently counts thinking as failing. **Almost every measurement below is
computable from these fields with no instrumentation at all.** The exceptions are named
in *Recommended approach* step 5.

**Three constraints from the two sweeps that bind what may be measured, not just how.**

1. **ASR is dead at the operating tempo.** The rate feasibility study established that at
   the 200 s mutation interval every published run of this project has used, *neither*
   attacker completes the objective — the baseline included, which was not previously
   known. The objective only becomes reachable above roughly 1 600 s. Inside that
   degenerate region success rate is pinned at zero and can no longer distinguish
   anything. **Host breadth and elapsed time remain informative throughout.** Any measure
   this suite adds must be one that still discriminates inside the degenerate region, or
   it must be documented as usable only outside it.
2. **The progression measure the criterion recommends is saturated.** `deepest_stage`
   (deepest consensus lifecycle stage reached) is degenerate on `v1_ckc_total` and
   near-degenerate on `v2_partial`: every profile reaches consensus stage 3 in its own
   campaign structure and then fails against the simulated network, not against its own
   model of the campaign. Axis 1's M8b recommendation names "deepest tactic band reached
   per run (kill-chain depth)" — that measurement, as written, **cannot discriminate**,
   and `apt_model_criterion.md` §(h) already records that it needs replacing with a finer
   progression measure. Supplying the replacement is this handoff's single most valuable
   deliverable.
3. **Ten seeds cannot separate adjacent profiles.** Two independent sweeps, over two
   unrelated parameter families, reached the same verdict: at ten runs per cell no
   ordering of profiles by progress survives, because the confidence intervals overlap
   almost everywhere. A measure that produces a rank list is not useful unless the suite
   also reports which adjacent pairs are actually separated. **Every aggregate this suite
   emits must carry its interval**, and the reporting helper must be able to answer "which
   adjacent pairs are CI-disjoint" without the caller re-deriving it.

**What is not blocked by anything.** No supervisor ruling is pending on measurement. S2
freezes attacker actions, abilities and states; a reader adds none of those. The M7
architecture constraint is that `statistics.py` is a **reader** and must not touch the
inherited `AttackStatistics` maths, which continues to serve the 6-phase baseline and the
goldens — that constraint holds here and is the main thing to be careful about.

## Recommended approach

**Extend `movement/statistics.py`, or add a sibling module beside it.** Prefer a sibling
(`movement/measures.py`) if the file would otherwise triple in size; the existing MTTC/ASR
reader is cited from several records and is easier to leave alone. Either way the contract
is the same: pure functions over `Sequence[MovementRunResult]`, no simulation, no I/O, no
mutation of anything.

**1. Progression (axis 1).** Four measures, of which the second is the replacement the
criterion is waiting for.

- **Distinct-tactic coverage over time** — the count of distinct places visited by sim
  time *t*, as a curve and as an end-of-run scalar. Discriminates inside the degenerate
  region.
- **Deepest *successfully actioned* stage** — the highest consensus lifecycle stage
  (`data/ogasp/controller/lifecycle_consensus.json`) at which the run recorded a
  **success verdict**, not merely a visit. This is the recommended replacement for the
  saturated `deepest_stage`: visiting saturates because every profile's net reaches stage
  3, but `pure_steal` succeeds at nothing at all and `infrastructure_setup` succeeds
  hundreds of times low in the lifecycle, so a success-gated depth should separate them.
  **Verify that it actually does** before adopting it — if it saturates too, report that
  and fall back to the coverage curve, because a second saturated measure adopted without
  checking is exactly the failure §(h) already recorded once.
- **Foothold-retention duration** — sim time between a compromise and the next MTD
  interrupt that severs the attacker's position (an `interrupted` record whose
  `interrupted_by` is a network-layer resource, which is where the substrate clears the
  host cursor). This is the measure that makes MTD's claimed mechanism — destroying
  accumulated position — visible at all.
- **Effort-to-breadth conversion** — successful actions per distinct host compromised.
  Experiment 1 computed this ad hoc and it carried finding 2; formalise it so the figure
  is reproducible from tracked code.

**2. Traversal diversity (axis 3).** The criterion asks for "distinct tactic-sequences
across seeds; path entropy over the net".

- **Path entropy** — Shannon entropy of the empirical out-transition distribution at each
  place, aggregated over a profile's runs, weighted by visits. A profile whose branching
  collapses to one route has near-zero entropy however plural its net looks.
- **Distinct tactic-sequences across seeds** — the count of unique place-sequences (and
  unique *prefixes* of length *k*, which is far less seed-sensitive than whole sequences).
- **Between-profile behavioural divergence** — Jensen–Shannon divergence between profiles'
  action streams and between their terminal-tactic distributions. This is also axis 2's
  stronger-claim measurement (§(d) axis 2, M8b: "mirroring the L2 corpus-level check at the
  execution level"), so it is one implementation serving two axes. Reuse the L2 JSD
  discrimination check's shape (`pipeline/gasp/gasp_schema.md` §(g)) rather than inventing
  a second convention.

**3. Defender response (axis 4).** The criterion's framing is the one to encode: these
measures exist to "discriminate *reacts* from *adapts usefully*".

- **Action-mix shift around an MTD event** — the distribution over verbs (and over
  `place_class`) in the *n* events before an interrupt against the *n* events after,
  paired within run so seed variance cancels.
- **Recovery time from an MTD-induced throwback** — sim time from an interrupt to the next
  success verdict; censored, and reported as such, when no success follows.
- **Failure-branch routing rate against progress** — the fraction of routing decisions
  taken on the failure column, correlated with breadth. If re-routing helps, the profiles
  that route on failure most should not be the profiles that get least far.

**4. Cost ledger (axis 6 prerequisite).** Per run: actions attempted (by verb, and split
by `blocked` / `place_class`), sim time spent (total, and decomposed into behavioural
dwell against dispatched-verb cost via `end_time - start_time - dwell`), re-work forced by
MTD (interrupt count, and the time consumed by interrupted events that produced no
success), and yield per unit cost (distinct hosts per unit sim time). The criterion is
explicit that the ledger alone is a *measurement*, not an axis-6 claim — the claim needs a
decision rule that consumes it, which is a separate handoff.

**5. Two instrumentation gaps to close or document.** These are the only places where a
reader is not enough.

- **The MTD confusion penalty is invisible as a line item on the movement arm.** It is
  consumed inside `apply_mtd_interrupt_cost` (`mtdnetwork/operation/attack_operation.py`)
  and shows only as a gap between one record's `end_time` and the next record's
  `start_time`. Either derive it from that gap (and test the derivation against a known
  seeded run) or record it on `MovementRecord` as its own field. Deriving is preferred —
  adding a field is a record-schema change that ripples into the trace tool.
- **The driven arm writes no interrupt row to `attack_record.csv`.** A cost ledger built
  from the substrate's CSV is therefore native-arm-only. Build the movement arm's ledger
  from `MovementRecord` instead, and state the asymmetry in the record rather than
  producing two ledgers that quietly measure different things.

**6. Report with intervals, always.** Provide one helper that takes a per-profile measure
and returns the mean, the 95 % interval, and the set of adjacent pairs whose intervals are
disjoint. Both sweeps failed their ordering conclusion for want of this being routine; make
it the default output shape so the next study cannot accidentally report an unseparated
ordering.

**Alternatives considered.** *Compute these in the experiment script instead* — rejected:
that is exactly what experiment 1 did, and the figures are now unreproducible because the
workspace is gitignored. *Extend the inherited `AttackStatistics`* — rejected: it serves
the baseline and every golden, and M7 pins it as untouched. *Wait for experiment 2 and
measure afterwards* — rejected: several measures (recovery time, action-mix shift around an
event, foothold retention) need the per-event stream, which only exists in memory during a
run unless the experiment persists it, so measuring afterwards means re-running.

## Validation gate

Done when:

1. Every measure above exists as a tested pure function over `MovementRunResult`s, with a
   unit test built on a hand-constructed record stream whose expected value is worked out
   by hand in the test.
2. **The suite reproduces experiment 1's ad-hoc figures**, re-derived from a fresh run of
   `data/results/exp01_movement_vs_baseline/run_experiment.py` on the current substrate:
   the blocked-fraction profile (`pure_steal` ≈ 95 %, `infrastructure_setup` 0 %) and the
   effort-to-breadth ratios (baseline ≈ 20 actions per distinct host,
   `infrastructure_setup` ≈ 210). Magnitudes will differ from the published table — the
   substrate has been re-baselined and the timing regime has changed since — so the gate is
   that the **shape** reproduces and the difference is explained, not that the numbers match.
3. **The replacement progression measure is shown to discriminate.** On the five profiles,
   deepest-successfully-actioned-stage must separate at least one adjacent pair that
   `deepest_stage` does not. If it does not, the handoff still ships, with that negative
   recorded and the coverage curve adopted instead — but the check must be run and
   reported either way.
4. The interval helper is used by at least one measure's own test, so the reporting shape
   is exercised rather than merely available.
5. The determinism suite still passes unchanged (readers cannot move SIM-05, and a
   regression here would mean something was not a reader).
6. A short tracked record under `docs/implementation/pipeline/ogasp/` naming each measure,
   which axis's M8b field it discharges, and its known blind spots — because the criterion
   will cite it.

## Hard constraints

- **Reader only.** No change to `MovementAttacker`, the controller, the overlay, the nets,
  or the substrate. If a measure seems to need a model change, it belongs in a different
  handoff — say so and move on.
- **`AttackStatistics` is untouched** (M7, D5). The baseline arm and every golden depend on
  it.
- **Do not report ASR at the operating mutation interval** as though it discriminates. It
  is inside the degenerate region. Either measure outside it, or report breadth and elapsed
  time and say why ASR was dropped.
- **No ordering claim without disjoint intervals.** Two sweeps have already established
  that ten seeds cannot separate adjacent profiles; the suite must make that visible rather
  than let a caller round it up.
- Determinism / SIM-05 unaffected — readers introduce no randomness and must not consume
  any RNG.
- Australian English in docs and comments; branch and commit rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.

## Reading list

- `src/mtdsim/l3_simulation/movement/statistics.py` — the existing reader, its contract,
  and the three `(verb, outcome)` pairs that count as a compromise.
- `src/mtdsim/l3_simulation/movement/attacker.py:147-175` — `MovementRecord`, field by
  field; note `place_class`, `dwell`, and the `end_time - start_time - dwell` decomposition.
- `docs/implementation/apt_model_criterion.md` §(d) — the *what would evidence a claim
  (M8b)* field of each axis; this handoff is that list turned into code. Also §(h), which
  already records the saturated-depth problem.
- `docs/implementation/pipeline/ogasp/experiment_01_findings.md` §3–§4 — the ad-hoc figures
  to reproduce, and why the action budget had to be decomposed for the two failure surfaces
  to be visible at all.
- `docs/implementation/pipeline/ogasp/rate_feasibility_study.md` §7 (C5) — the degenerate
  region table, which decides which measures are usable at which mutation interval.
- `docs/notes/ch5_evaluation/evaluation_burden.md` — the discipline every measurement here
  is eventually reported under.

## Out of scope (explicitly)

- Any change to the attacker model, the weights, the mapping, or the timing.
- Running experiment 2, or any new experiment. This handoff builds instruments; the arms
  that use them are `2026-07-28_axis134_demonstration_arms.md`.
- Moving any badge in `apt_model_criterion.md`. Badges move on evidence from a run, and no
  run happens here.
- A stealth exposure metric. It is listed in the criterion's axis-5 M8b field, but it
  presupposes a stealth semantics that does not exist yet — see
  `2026-07-28_axis5_stealth_conceptualisation.md`. Do not build a detectability proxy on
  the assumption of what stealth will mean.
- Dissertation prose.
