---
status: open
created: 2026-08-01
updated: 2026-08-05
---

# Make attacker disengagement measurable — a projected-effort reading over existing runs, reported as a frontier over patience, so MTD's own economic claim becomes scorable

## This is now axis 6's metric — the incentive-rationality measure (2026-08-05)

**Marc's direction, from the Jin discussion:** this measure is the attack-cost
metric for **incentive rationality** — the instrument that answers *where would
the APT eventually give up*. That framing promotes it from "a useful reader" to
**the** measurement axis 6 has been missing, and it settles a question that has
been open since the axis-6 sweep returned its negative.

**It also absorbs the iterated cost model handoff, which is retired.**
`2026-08-01_iterated_cost_model.md` proposed repairing the axis-6 *decision
model* — a state-conditioned expected cost and an enabling-value benefit — so the
attacker could express instrumental value. That was a mechanism rebuild on a
frozen model, blocked on a disposition, and comparable in size to the axis-7
readiness work. **Measurement comes first**, and this measure is the one that
tells you whether the mechanism rebuild is worth its cost at all. What survives
from that brief is recorded in §2.8 below; the rest is superseded.

The reasoning is the same one this brief already makes in §1 and it is worth
stating as the ruling it now is: **the axis-6 utility modulator prices MTD as a
cost-raising defence, and MTD is not one.** Its cost effect is a roughly uniform
9 % surcharge, proportional to dwell and therefore invisible to a normalised
ratio. What MTD destroys is the attacker's *productive capacity* — position,
discovered services, reachability — not its accumulated gains. A measure built on
progress-per-effort sees exactly that; a ratio cannot. So the route to axis 6 is
through **measuring disengagement**, not through a better decision rule.

**Blocked on one ruling: D-09.** This handoff implements a generalisation of an
unimplemented lineage requirement, and whether that generalisation is wanted is
Marc's disposition, not a session's. Read
[`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md)
D-09 and §IS-INT-06 before anything else. If D-09 rules for a literal
interruption counter instead, **stop** — §"Alternatives" explains why the literal
build produces a tautology, but that argument is input to the ruling, not a
licence to ignore it.

Governed by
[`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md).
This is a **reader**, not a mechanism: no run changes, no golden moves, no
attacker capability is added, so the freeze holds by construction.

## 1. State of play — why this exists

Every attacker-side metric in this lineage is conditioned on the attacker
**continuing**. Attack success rate, mean time to compromise, host compromise
ratio — each asks how well an attack that persists to the horizon performed. On
the Cho extraction's reading of §VII, the field's attacker-metric taxonomy has
exactly two families, effectiveness and efficiency, and neither has a cell for
the attacker leaving. *(That reading is flagged in
[`../sources/extractions/cho2020.md`](../sources/extractions/cho2020.md) as a
synthesised reading of §VII rather than a literal Cho table, with an open
question already logged — confirm against the source before the dissertation
leans on it.)*

Yet abandonment is the outcome MTD's economic argument is *about*: raise the
attacker's cost until this network is no longer worth the effort. Bianco's
Pyramid of Pain names campaign abandonment as the apex defensive outcome
([`../sources/extractions/bianco2013.md`](../sources/extractions/bianco2013.md)).
FlipIt supplies the equilibrium in which the higher-move-cost player's benefit
is zero. The simulator can currently represent neither, so every "MTD works"
conclusion it produces is silent on the mechanism its own literature claims.

**The lineage already started this and stopped halfway.** Brown's per-host
give-up rule is implemented and conforms — `ATTACKER_THRESHOLD = 10`
([`constants.py:106`](../../mtdnetwork/data/constants.py)), applied per host with
the target node exempted in targeted mode
([`attack_operation.py:358`](../../mtdnetwork/operation/attack_operation.py)),
audited as IS-SCN-04 CONFORMS with a unit delta (the counter ticks per
enumeration, not per failed exploitation). But that is *local* abandonment —
stop attacking this box, try another one. **Campaign-level abandonment is
IS-INT-06, classified DIVERGES-DOCUMENTED-NOWHERE:** Zhang specified a threshold
on MTD interruptions, it was never built, and its value was never stated in the
source.

**Why this is the right shape for incentive rationality on this substrate**, and
not a second attempt at the cost model. The axis-6 utility modulator prices MTD
as a *cost-raising* defence. It is not one: its cost effect is a roughly uniform
9 % surcharge, proportional to dwell and therefore invisible to a normalised
ratio (`incentive_rationality.md` §6.3). What MTD actually destroys is the
attacker's **productive capacity** — position, discovered services, reachability
— not its accumulated gains: `_compromised_hosts` is append-only, and what a
network-layer interrupt clears is the host cursor. So the economically visible
signature of MTD here is a **stall**: progress flattens while effort keeps
accruing. A measure built on progress-per-effort sees exactly that, and unlike a
normalised utility ratio it has units, so it can be compared against a
reservation value — which is what abandonment requires and what the axis-6
mechanism structurally cannot express. Full argument:
[`../implementation/pipeline/ogasp/cost_model_plain.md`](../implementation/pipeline/ogasp/cost_model_plain.md).

## 2. The design

### 2.1 The quantity

At each attempted action `t` in a run, compute the attacker's **projected total
campaign effort**:

```
    T(t)  =  t  +  ( W − h(t) ) / r(t)
                   └────────────────┘
                    projected remaining effort

    r(t)  =  ( h(t) + α ) / ( t + α / r₀ )        smoothed progress rate
```

- `t` — attempted actions spent so far (**effort**).
- `h(t)` — cumulative progress so far (**hosts compromised**; §2.3).
- `W` — total work the objective requires: `0.8 × 50 = 40` hosts under the
  movement runner's geometry (`terminate_compromise_ratio`, `total_nodes`).
- `r₀`, `α` — the attacker's prior rate and its strength (§2.4).

**Abandonment.** For an effort budget `B`, the run abandons at the **first** `t`
where `T(t) > B`; if no such `t` exists before termination, the run is
**censored** at that budget, not "did not abandon".

Four properties earn this form, and an implementer should be able to see each
one in the arithmetic:

- **Stalling raises `T`, progress lowers it.** An action with no progress
  increments `t` and decrements `r`, so `T` rises twice over. A compromise
  raises `h` and `r`, so `T` falls — an attacker close to the objective
  rationally persists through a stall that would rightly send an empty-handed
  attacker away. Both level and rate are therefore live, which is what "expected
  payoff" needs and a bare rate does not give.
- **It has units** (actions), so a reservation value is expressible.
- **It does not cancel under MTD.** Interrupts add to the denominator without
  adding to the numerator; suppressed compromise holds the numerator down. This
  is the non-proportional response the criterion's axis-6 M8b field names as a
  route to DEMONSTRATED.
- **`T` is not monotone**, deliberately. First-crossing is the honest reading:
  an attacker decides in real time and does not get to wait and see whether its
  prospects recover.

### 2.2 Read it, do not run it

**Do not implement an attacker that stops.** Implement a measure that reports
when it *would have*. This is strictly better on five counts, and the fifth is
the one that matters:

1. No declared threshold is load-bearing — the budget becomes an axis of the
   result (§2.6).
2. No behaviour change, so no re-baseline and no golden churn.
3. Pure functions over records: deterministic, no RNG, no ablation arm needed.
4. **One run yields the entire budget-family**, because `T(t)` is a trajectory
   and every `B` is a threshold read off it. The existing recorded runs can be
   re-read without re-simulating.
5. It cannot be accused of building in its own conclusion, because the runs it
   reads are unchanged runs.

This follows the suite's strongest precedent: the MTD confusion penalty was
closed by *derivation* rather than a schema change
([`measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
§(b)), and every measure there is a pure reader.

The obvious objection — the rational-attacker handoff warns that this project has
already shipped a measurement with no decision rule to consume it — does not
apply. The cost ledger measured an *input* an attacker might have conditioned on;
this measures an *outcome* that answers a research question standing alone: does
this defence induce earlier disengagement than that one. A decision rule that
consumes it is a later, separate build, and §7 states why it must come second.

### 2.3 Progress, and an instrumentation question to settle first

**Progress is distinct hosts compromised.** Two facts collide and the session must
resolve them before writing the estimator:

- `MovementCostLedger.n_distinct_hosts` is `run.compromised_count` — substrate
  ground truth, but an **end-of-run scalar**. There is no trajectory.
- `is_compromise(record)` gives compromise **events** over time, but
  `MovementRecord` carries **no host identity** (the blind spot
  `foothold_retentions` already documents), so cumulative events may over-count
  distinct hosts through re-compromise.

**Settle it with a cheap check before building anything:** over existing recorded
runs, compare `len([r for r in run.records if is_compromise(r)])` against
`run.compromised_count`. If the ratio is at or near 1.0, cumulative compromise
events are a sound trajectory proxy and the reader stays a reader — **report the
ratio either way**. If it is materially above 1.0, do *not* silently accept the
over-count: record it as instrumentation gap 3 in `measurement_suite.md`, and
raise widening `MovementRecord` with a host identifier as a decision for Marc.
The suite's own guidance is to prefer extending the reader over widening the
record, so the burden of proof sits on the schema change.

The baseline arm has no such problem: `baseline_ledger` already counts distinct
hosts on `compromise_host_uuid`, stable across topology shuffles, so its
trajectory is exact. **State the asymmetry in the record rather than smoothing
over it.**

### 2.4 The declared values — three, all swept, none free

| Name | Meaning | Proposed value | Tier | Band |
|---|---|---|---|---|
| `r0_prior_rate` | the attacker's prior belief about hosts per action before evidence | the **unimpeded baseline attacker's realised rate** — measure it, do not invent it: ≈ 39.2 hosts / 1 411 actions ≈ **0.028** | `attested-pattern/declared-magnitude` — the behaviour (an attacker arrives with an expectation) is attested; the magnitude is measured within-substrate | ±½× and ×2 about the measured value |
| `alpha_prior_strength` | pseudo-count controlling how fast evidence overrides the prior | **1.0** (one pseudo-host) | `declared-judgement` | [0.5, 5.0] |
| `B` effort budget | the reservation value — total campaign effort the attacker will tolerate | **not declared** — swept as the reporting axis (§2.6) | — | expressed as a multiple `k` of the unimpeded effort-to-objective `U ≈ 1 430` actions; sweep `k ∈ [1, 10]` |

Two rules travel with these. **The prior is anchored within-substrate, never to
real-world figures** — the duration catalogue is explicitly shape-not-scale, so
sim units carry no calibrated mapping to real campaign durations, and anchoring
patience to breach-report hours would be exactly the cross-scale comparison the
project forbids. And **no value here may be chosen because it improves an
outcome**; log the family in the ledger schema of
[`../implementation/declared_value_provenance.md`](../implementation/declared_value_provenance.md)
§3 with an R0 authoring round, as the overlay, learning and benefit families each
did.

### 2.5 Units and the cross-arm trap

**The primary measure is effort-denominated (actions), not time-denominated —
and this is not a preference.** Under S3-R the movement layer prices all of its
own time while the baseline runs on substrate pricing, so
`EventWiseComparable` carries no time field *by construction* and the unit test
asserts its absence. An abandonment measured in seconds would be arm-local and
could not be compared to the baseline; measured in actions it is event-wise and
therefore cross-arm safe.

Report a time-denominated view **only** as an arm-local secondary, labelled as
such, per `measurement_suite.md` §(f).

### 2.6 The reporting shape — a frontier over patience, never a chosen threshold

Zhang never stated the threshold value, so it cannot be declared honestly. Turn
that into the reporting form rather than a gap: for each defence mechanism and
mutation interval, report **mean abandonment effort as a function of the budget
multiple `k`**, with its 95 % interval and its censoring fraction at every point.

The reader picks their own reservation and reads off the answer. No declared
value is load-bearing, and this is the same discipline the rational-attacker
handoff imposes on the disruption metric: *a frontier, never a composite score.*

**Censoring is data, not a nuisance.** At low `k` almost every run abandons; at
high `k` most censor. `CensoredDurations` already models exactly this split, and
its convention — observed and censored reported separately, never pooled into one
mean — is mandatory here, because a pooled mean understates every censored run
and the censoring fraction itself varies along the curve.

### 2.7 Both arms, and they are expected to disagree

Run the measure on the **inherited baseline attacker as well as the profiled
one**, and treat their disagreement as the result rather than as noise.

- The **baseline** is where the measure should demonstrate *validity*: that arm
  actually progresses, and MTD cuts it from 39.2 to 13.1 distinct hosts — a
  threefold rate reduction that abandonment effort ought to register. If it does
  not register there, the measure is broken, not the finding.
- The **profiled** arm carries the *research question*: does behavioural fidelity
  change when and why an attacker disengages? Given that this attacker's
  projected requirement is roughly 8 000 actions against a run length of ~263
  (§3, C2), it may abandon early under every condition including none.

That contrast is the interesting outcome and would mirror experiment 2's ranking
inversion: a measure that registers MTD against the inherited attacker and not
against the profiled one is a statement about what each attacker's failure is
made of.

### 2.8 What survives from the retired iterated-cost-model brief

Absorbed 2026-08-05. Three things are worth carrying; the rest is superseded by
the measurement-first ruling above.

1. **The defect is real and is itself a finding**, independent of whether the
   mechanism is ever repaired: the current model's two terms — declared duration
   as cost, objective proximity as benefit — penalise *instrumental* tactics in
   the same direction, so reconnaissance is discounted twice and `pure_steal`
   prefers a precondition-coupled exploit over it by a factor of **31**. No
   declared value repairs it; it is a defect of the model's *form*. Recorded in
   [`cost_model_plain.md`](../implementation/pipeline/ogasp/cost_model_plain.md)
   §2.2a and already banked as a transferable warning (F5): *an evaluation that
   gives its attacker a cost model without asking whether that model can express
   instrumental value will measure the attacker defeating itself.*
2. **The falsifiable prediction, preserved for whoever picks the mechanism up.**
   The proposed expected-cost term could only respond to **network-layer**
   mutations (`mtd_clears` declares that an application-layer mutation clears
   nothing), so it predicted a cost-sensitivity effect under the
   position-destroying family and **little or none** under the diversity family —
   the same split the headline ranking inversion turns on. That is a good
   prediction and it should be pre-registered if the mechanism is ever built.
3. **The composition hazard stands.** Any readiness-conditioned cost term would
   condition on the same signal as axis 7's readiness learner, which is the hidden
   double-count the composition register exists to catch. The existing joint check
   does **not** transfer — it measured the *declared-duration* modulator and found
   the two pulling opposite ways.

**What is explicitly not carried forward:** the mechanism build itself, its five
ranked options and its U1–U5 pre-registration. If measurement shows the mechanism
is worth rebuilding, that brief is re-opened from the git history rather than
re-derived — `2026-08-01_iterated_cost_model.md`, retired in the same commit as
this update.

## 3. Pre-registered conclusions — commit these in their own commit, before any output exists

This is the house discipline and it is not optional here: the axis-6 sweep, the
S1 study, the rate study and the axis-7 build all committed conclusions and
criteria before running, and `analyse.py` computed held/moved verdicts rather
than asserting them. Do the same. Every aggregate goes through `interval_report`;
`ordering_supported` is the gate, never the sorted means.

| | Conclusion | Criterion |
|---|---|---|
| **C1** | The measure is non-degenerate | mean abandonment effort varies across the `k` band by more than its own 95 % interval width, on ≥ 3 of 5 profiles. A flat curve means the budget axis carries no information and the measure is useless whatever else holds |
| **C2** | **THE KILL CRITERION — the defence is attributable** | at ≥ 1 budget level, mean abandonment effort under ≥ 1 MTD mechanism is CI-disjoint from the no-MTD arm, on ≥ 3 of 5 profiles. **If C2 moves, stop and report** — the measure cannot attribute disengagement to the defence, and the honest output is that finding, not a third attempt |
| **C3** | Mechanisms differ from one another | the ranking of mechanisms by mean abandonment effort is not uniform — ≥ 1 adjacent pair separates at the operating interval. Otherwise the measure only reads MTD on/off, which host-compromise count already does |
| **C4** | **The payoff — it discriminates where ASR cannot** | at the 200 s operating interval, inside the degenerate region where ASR is pinned at 0.00 for every arm, abandonment effort separates ≥ 1 adjacent pair of conditions |
| **C5** | **Committed in the direction that would embarrass it** — the measure is not a restatement of breadth | Spearman correlation between mean abandonment effort and mean distinct hosts, across all cells, is **below 0.9**. At or above 0.9 the measure is a monotone re-expression of a quantity already reported, and adds nothing — say so plainly rather than shipping it |

**C2 moving is a result, not a failed study.** If disengagement on this substrate
is driven by procedural friction rather than by MTD, that is the same family of
finding as the axis-6 negative and the learning study's credit-signal result, and
it belongs in
[`../implementation/pipeline/ogasp/fidelity_implications.md`](../implementation/pipeline/ogasp/fidelity_implications.md)'s
ledger. Write it up as such. **Do not** respond to a moved C2 by re-specifying the
measure until it separates — that is the scoring-driven design the criterion's own
standing constraint forbids.

## 4. Validation gates

1. **Unit gate.** Hand-constructed record streams with hand-worked expected
   values, in `tests/l3_simulation/test_movement_measures.py` alongside the
   existing 27: a run with steady progress (T falls), a run that stalls (T rises
   monotonically), a run with no progress at all (T rises from the prior alone), a
   run that crosses and then recovers (first-crossing is taken, not the last), and
   a censored run (returns `None`, not a sentinel integer).
2. **Instrumentation gate.** §2.3's compromise-events-versus-`compromised_count`
   ratio computed and reported over existing runs, with the disposition recorded.
3. **Reader gate.** The full `tests/l3_simulation` suite and the substrate/carve/
   golden suites pass **unchanged** — this measure moves nothing. A moved golden
   means something was built that should not have been.
4. **Cross-arm gate.** The measure computes on one seeded run of each arm,
   field-for-field, same keys both sides, with no time-denominated field in the
   comparable subset (assert it, as the suite already asserts for
   `EventWiseComparable`).
5. **Determinism.** Re-derivation from re-created runs is exact — the measure
   draws from no stream.

## 5. Build order

1. Read D-09 and confirm the ruling. Nothing below is licensed without it.
2. Settle §2.3's instrumentation question (cheap; existing runs; no new sim).
3. Add the reader to
   [`../../src/mtdsim/l3_simulation/movement/measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py)
   as a new section, keeping the pure-function contract. Suggested names:
   `progress_trajectory`, `projected_effort_curve`, `abandonment_effort`,
   `abandonment_curve`, plus a `baseline_progress_trajectory` reading rows through
   the existing adapter.
4. Unit gate (gate 1) before any experiment run.
5. Commit the pre-registered conclusions of §3 **in their own commit**.
6. Re-read the existing recorded runs first — experiment 2's matrix already spans
   the defence family and both intervals, so the frontier may be derivable with no
   new simulation at all. Only run fresh cells for what the recorded set cannot
   cover. **Check freshness first**: the axis-6 sweep's rows no longer reproduce
   after commits `6181305` and `816b300`
   ([`cost_model_plain.md`](../implementation/pipeline/ogasp/cost_model_plain.md)
   §2.1), so verify before reusing any stored arm.
7. Analyse with computed held/moved verdicts per conclusion, never asserted.
8. Write the record as
   `docs/implementation/pipeline/ogasp/attacker_disengagement.md`; bump
   `measurement_suite.md` §(g) and its `updated`; log the declared family in the
   value-provenance ledger; delete this handoff in the commit that ships the work
   and prune its line from `handoffs/README.md`.

## 6. Alternatives considered and rejected

- **Zhang's interruption counter, literally** (abandon after N MTD interrupts).
  Rejected for research use, and the reason is fatal rather than practical: it
  makes "MTD causes attackers to give up" definitional, so the only available
  finding is "more MTD, faster give-up", which is arithmetic dressed as a result.
  It is also a direct observation of the defence, which is axis 8 — ruled out of
  scope 2026-07-28. **The projected-effort rule is the strict generalisation** in
  which Zhang's counter is the special case where the only thing that can stall
  the attacker is MTD; it removes the hard-wiring and admits a null arm, which is
  what makes C2 a real test. That argument is input to D-09.
- **A windowed progress rate.** Rejected on measured sparsity: the profiled
  attacker compromises ~1.26 distinct hosts over ~263 actions, so almost every
  window contains zero progress and the rate degenerates. The smoothed cumulative
  form is the same Laplace device the axis-7 learner already uses — house
  precedent, never zero, degrades gracefully.
- **Time since last progress** (a renewal-process rule). Robust to sparsity and
  worth keeping as the **robustness comparator** reported alongside, but rejected
  as primary because it discards the work-remaining term, so it cannot distinguish
  an attacker one host short from one with nothing.
- **An absolute reservation value declared once and defended.** Rejected: the
  source never states it, so any value is unfalsifiable. Sweeping it as the
  reporting axis dissolves the problem instead of hiding it.
- **Anchoring patience to real APT campaign durations** (`apt_campaign_duration`,
  `breach_reports_macro_timing`). Rejected on shape-not-scale: sim seconds carry
  no calibrated mapping to real hours, and this would import exactly the
  cross-scale comparison the project forbids. The within-substrate anchor (§2.4)
  does the same job legitimately.
- **Running the targeted attacker instead.** Rejected for now, on the audit's
  evidence rather than on effort: IS-SCN-03 records that the targeted *strategy*
  has **no live code path** — `get_host_id_priority` and `tag_priority` are never
  called from the attack chain, and `network_type == 0` gates only target
  selection at generation, attack-path-exposure bookkeeping and give-up
  protection. `TimeNetwork` hardcodes `network_type = 1`, matching Zhang's
  documented descoping. Flipping the flag yields a target node but *not* a
  targeted attacker, and making it real is a substrate change under freeze that
  moves every golden. Distance-to-a-named-objective would be the cleaner economic
  signal and is the natural successor study — second, and only if the general
  form discriminates.

## 7. Out of scope (explicitly)

- **An attacker that actually stops.** The decision rule that *consumes* this
  measure is a separate build, gated on this one discriminating: if abandonment
  effort does not separate across the defence family, a mechanism conditioned on
  it would have nothing to find. Measure first.
- **Any badge move.** This is a measurement; axis 6 reaches DEMONSTRATED only when
  the attacker *conditions on* something the proportional surcharge does not
  cancel. Say plainly in the record that the reader does not move the badge.
- **A composite score** trading attacker disengagement against defender
  disruption. The frontier is the deliverable, here as in the rational-attacker
  handoff.
- **Changing the cost model, the duration catalogue, the benefit family, or λ.**
  Part 1 of the rational-attacker handoff settled those and the freeze holds.
- **Fixing IS-SCN-04's unit delta** (the give-up counter ticking per enumeration
  rather than per failed exploitation). Flag it if it obstructs; do not action it —
  it is a conformance disposition for Marc.
- Dissertation prose.

## 8. Reading list

- [`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md)
  — **D-09** (the blocking ruling), IS-INT-06, IS-SCN-04, IS-SCN-03. Read these
  four rows before anything else.
- [`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  — the reader contract this extends, §(b)'s blind-spot discipline, §(d)'s
  cross-arm event-wise enforcement, §(f)'s consumer rules, §(g)'s lifecycle.
- [`../implementation/pipeline/ogasp/cost_model_plain.md`](../implementation/pipeline/ogasp/cost_model_plain.md)
  — why the cost model cannot express abandonment, and the substrate-freshness
  warning about reusing stored runs.
- [`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
  — §9 the ranking inversion, §15 the dwell-proportionality result, §17 the
  degenerate region. The recorded matrix this may be able to re-read.
- [`../implementation/declared_value_provenance.md`](../implementation/declared_value_provenance.md)
  — §2 tiers, §3 ledger schema, §5 the guardrails the three declared values must
  not cross.

## 9. Hard constraints

- **D-09 gates everything.** No build before the ruling.
- **Reader only** — pure functions over records, no RNG, no mutation, no
  behaviour change. The inherited `AttackStatistics` maths stays untouched (M7,
  D5), and no golden may move.
- **No time-denominated cross-arm comparison.** Effort-denominated primary;
  time views arm-local and labelled.
- **Censoring reported separately**, never pooled.
- **No ordering claim without disjoint intervals** — `interval_report` is the
  gate.
- **No declared value chosen because it improves an outcome**; the budget is
  swept as a reporting axis and never selected.
- **A moved C2 is reported, not engineered around.**
- Determinism (SIM-05); envelope-not-actor; within-substrate comparability only;
  Australian English; branch per session; never push.
