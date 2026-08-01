---
status: durable
created: 2026-08-01
updated: 2026-08-01
topic: "The disruption frontier (Part 2 of the rational-attacker handoff) — a defender-side disruption measure derived from the substrate's own per-mutation records, paired with the attacker-side cost account, and reported as a frontier across the defence family and the mutation-interval dimension: the pre-registered design and conclusions, then the verdict as found"
---

# The disruption frontier — pricing what the defence family buys

**Status:** durable. **§1–§5 are a pre-registration**: the matrix, the declared
inputs, the measure's derivation and the five conclusions with their criteria
were written and committed **before a single result file existed**, per the
house discipline every sweep since the S1 study has run on. §6 onward reports
what the run found, whichever way it fell.

The run's workspace is `data/results/frontier_disruption/` (gitignored by
design: runner, numbers, figures — regenerable). This record is the tracked
account. It discharges Part 2 of the rational-attacker handoff
(`2026-07-29_rational_attacker_and_mtd_tradeoff.md`); Part 1's record is
[`cost_model_plain.md`](cost_model_plain.md).

## 1. What this is for

MTD's real proposition is a trade: mutation raises attacker cost **and**
imposes defender cost — downtime, churn, reconfiguration. Every result this
project has produced measures only the attacker's half, so every "this defence
suppresses the attacker by X %" conclusion has been unpriced: experiment 2
ranked the defence family per mechanism and its record is silent on what each
mechanism costs the defender to run. This work adds the defender's half and
reports the two together as a **frontier** — attacker-side effect against
defender-side disruption, per defence condition, per mutation interval — which
is the shape practitioners actually decide on. Deliberately **no composite
score**: weighting the two sides into one number needs an exchange rate no
source supplies, and would hide exactly the trade the measure exists to show.

This measurement scores **no criterion axis**, by design (the freeze's §5b
names it as the thread that "adds a defender-side measurement that scores no
axis at all"). No badge moves on any outcome below.

## 2. The design — declared inputs and matrix

Everything experiment 2 declared at this seam is inherited unchanged, so the
frontier prices the same defence family the ranking result came from:

| input | value | note |
|---|---|---|
| controller mapping | `v2_partial` | experiment 2's |
| outcome overlay | `v3_persistent_backward` | experiment 2's |
| sink policy | retrace — **the landed `retrace_sinks` implementation** | experiment 2's recorded rows ran under the superseded retrace; these are fresh runs under the reconciled code, so sink-bearing profiles are not row-comparable to the recorded matrix and are not pooled with it |
| timing regime | S3-R stochastic | movement layer prices all attacker time |
| horizon | 15 000 s | matches every prior run |
| geometry | standard 50-host network | unchanged |
| seeds | 0–9 | ten; see §5 |
| intervals | 200 s and 2 000 s | the operating point and the point outside the degenerate region, as a dimension |
| conditions | the eight of experiment 2 §2.2 | `none` + 4 single mechanisms + 3 multi schemes, trigger interval set explicitly on every one |
| attacker arms | inherited baseline; movement, **modulators null** | the freeze's reported configuration (§4); no learning, no utility modulator |

Matrix: (1 baseline + 5 profiles) × 8 conditions × 2 intervals × 10 seeds =
**960 runs**, all fresh on the current substrate (the recorded experiment-2
rows predate the `816b300` scheme-registration fix and carry no defender-side
record at all, so nothing is reused).

## 3. The measure — derived, not declared

**Everything on the defender side is read off the substrate's own
per-mutation operation record; no new declared value exists anywhere in this
work.** The substrate already logs, for every executed mutation, its name, its
resource layer, and the window `[start_time, finish_time]` during which that
layer's SimPy resource was held while the mutation deployed — the same window
its own contention rule treats the layer as busy for (competing mutations are
suspended or queued against it). A mutation's execution window therefore *is*
time that layer was under active reconfiguration, in the substrate's own
semantics rather than in a declared model of downtime. The reader
(`measures.disruption_ledger`, §5 of the measurement suite) derives:

- **Reconfiguration occupancy** (the normalised primary): the union of all
  execution windows — wall-clock during which at least one layer was being
  reconfigured — divided by the run's elapsed time. Dimensionless.
- **Layer and mechanism decomposition**: summed window time per resource layer
  (network / application / reserve) and per mechanism, plus counts. The sum
  can exceed the union where layers overlap; both are kept visible.
- **Churn tempo** (the event-denominated secondary): executed mutations per
  1 000 s.
- **Contention**: the suspended-mutation tally — demand the schedule placed
  that the infrastructure could not serve on time.

**Calibration, stated.** The measure is calibrated *to the simulator* in the
only sense this project's comparability rules allow: its inputs are the
substrate's own MTD execution durations (Zhang's Table 3 values for the five
documented mechanisms — the MTD-14 disposition), spent on the shared SimPy
clock, and it is reported normalised (occupancy) or event-denominated (churn)
rather than as raw seconds wherever it crosses a comparison. Within-substrate
readings only; no real-world downtime claim is made or implied — sim seconds
carry no calibrated mapping to operational hours (shape-not-scale), so the
frontier compares mechanisms against each other on one substrate, never
against deployment SLAs.

**Comparability across arms, argued rather than assumed** (the handoff's own
requirement). Defender-side time is substrate-priced on *every* arm — the
execution draws come from the identical machinery whichever attacker runs —
so, unlike attacker-side time, defender-side quantities are cross-arm safe;
occupancy additionally normalises away the elapsed-time difference between
arms that terminate early and arms that run to horizon. What remains invalid
under S3-R is pairing defender-side time with movement-arm attacker time in
any cross-arm statement; every cross-arm pairing below therefore puts
**event-wise attacker measures** (distinct hosts, breadth suppression,
attempted actions per distinct host) against the defender side. T2 tests the
arm-invariance claim rather than resting on it.

**Known blind spots, inherited from the substrate's record and stated up
front:** a mutation aborted mid-execution because the network was compromised
appends no record (its partial window is invisible); a same-priority mutation
discarded rather than suspended is tallied nowhere; queue wait under the
simultaneous scheme's serialisation is not part of the window. All three
undercount disruption, so occupancy is a floor, not a ceiling.

**The attacker side of the frontier** is the existing account, nothing new:
per-condition breadth suppression relative to `none` (the decision-facing
axis experiment 2 ranked by) and cell-total attempted actions per distinct
host (the attacker-cost axis proper, event-wise, defined on both arms). Both
computed from the same fresh runs as the disruption ledger, so the two sides
of every frontier point come from the same simulations.

## 4. The conclusions, each with its criterion fixed in advance

**T1 — the disruption axis is non-degenerate.** Occupancy must separate
conditions, or the frontier's x-axis carries no information. Criterion: at the
200 s interval, on each arm, at least one adjacent pair of the seven MTD
conditions is CI-disjoint on occupancy (`interval_report`, 95 %).

**T2 — disruption is a property of the defence, not of the attacker.** The
frontier wants one shared x-axis; that is a claim, so it is tested. Criterion:
occupancy's 95 % intervals overlap between the baseline arm and the pooled
movement arm in at least 11 of the 14 MTD condition × interval cells. If
moved, the frontier is reported with per-arm disruption axes and the
divergence is the finding (it would mean the attacker's behaviour feeds back
into the defence's realised cost, e.g. through early termination).

**T3 — the frontier is not a re-expression of one axis.** Committed in the
direction that would embarrass the deliverable: if suppression is simply
proportional to disruption, the frontier collapses to an exchange rate and
adds nothing over the existing ranking. Criterion: |Spearman| between
per-condition mean occupancy and mean breadth suppression, across the seven
MTD conditions at 200 s, is **below 0.9 on at least one arm**. At ≥ 0.9 on
both arms, say plainly that suppression is bought at a near-fixed disruption
price on this substrate and the frontier is a line.

**T4 — the payoff: the ranking inversion is priced.** Experiment 2 showed the
two attackers are best suppressed by different mechanism families; the
frontier asks whether that survives pricing. Criterion: the Pareto-efficient
set of MTD conditions (no other condition has both suppression at least as
high and occupancy at least as low, on cell means) at 200 s **differs by at
least one member** between the baseline arm and the movement arm. If held, an
evaluator choosing from the frontier buys a different defence depending on the
attacker model — the inversion with the defender's cost attached. If moved,
pricing does not change the choice, and that is reported as the finding.

**T5 — tempo is the price.** The interval dimension should read as movement
*along* the frontier: relaxing the mutation interval buys the defender out of
disruption and out of suppression together. Criterion: occupancy at 2 000 s
sits below its 200 s counterpart with disjoint 95 % intervals in all seven MTD
conditions on both arms; the suppression change is reported beside it,
direction stated per condition, with no threshold attached (experiment 2 §10
already establishes the suppression side collapses for the movement arm; what
is new here is the price falling with it).

Also committed: realised executions per run are reported beside the nominal
interval in every cell (the experiment-2 §10 confound — the simultaneous
scheme's realised tempo exceeds its nominal one — is measured here, not
assumed away); and the substrate's own attack-interrupted tally is carried per
run as a cross-check against the attacker-side records.

## 5. What this run is not powered for, and what it will not do

- **No ordering of profiles by progress** (two sweeps have failed it at ten
  seeds), and **no significance claim** on any ranking or Pareto set — ten
  seeds gives directional statements; T1/T2/T5's CI criteria are the only
  interval-backed claims.
- **No ASR-shaped claim at 200 s** (the degenerate region).
- **No cross-arm attacker-time comparison**; event-wise only, per S3-R.
- **No composite attacker-versus-defender score**, per the handoff's hard
  constraint. The frontier is the deliverable.
- **No golden moves.** The defender-side snapshot reads the substrate's
  statistics after the run; the movement arm runs modulators-null; nothing in
  the simulation's behaviour changes.

**On "the attacker gives up", ranked as the handoff requires.** Abandonment is
not representable in the current model and no give-up rule is introduced here.
The two honest options the handoff names are ranked: (1) **the measured
collapse in effective progress as the proxy for disengagement** — already
produced by the existing mechanisms and reported wherever it occurs; this is
the stance of record today. (2) **A declared, tiered, swept threshold** — now
designed properly as the projected-effort disengagement measure
(`2026-08-01_attacker_disengagement_measure.md`, a reader reporting a frontier
over the attacker's patience), and **blocked on the D-09 ruling**. Option 2
supersedes option 1 if and when D-09 clears it; neither puts a give-up rule
inside the utility model.

---

# The verdict, as found

*Everything above this line was committed before the run existed (`bfe874e`).
Everything below reports against those criteria without amending them.*

**The run.** 960 runs, zero errored cells, `data/results/frontier_disruption/`
(runner, `numbers/frontier_report.json`, figures). Verdicts computed by
`analyse.py`, never asserted: **T1 held, T2 moved, T3 held, T4 held, T5 held.**

## 6. The headline — the *shape* of the trade inverts with the attacker

Experiment 2 showed the two attackers are best suppressed by different
mechanism families. Priced, the result is sharper: **whether MTD involves a
trade-off at all depends on which attacker you evaluate against.**

- **Against the inherited attacker there is no trade.** Suppression falls as
  disruption rises (Spearman **−0.857** across the seven MTD conditions at
  200 s), and the Pareto-efficient set is a **singleton**: Service Diversity
  delivers the family's best suppression (90.4 %) at the family's lowest
  occupancy (0.353), dominating every other condition outright. An evaluator
  pricing the defence with this attacker concludes the best mechanism is also
  the cheapest — MTD as a free lunch.
- **Against the profiled attacker the trade is real and steep.** Suppression
  rises near-monotonically with disruption (Spearman **+0.964** — T3 held on
  the baseline arm only, exactly the split the criterion anticipated), and
  **six of the seven conditions are Pareto-efficient**: every additional
  increment of suppression is bought with additional occupancy, from Service
  Diversity's 35.4 % at 0.353 up to the simultaneous scheme's 89.5 % at 0.700.
  The ~90 % suppression of the position-destroying family costs occupancy
  0.50–0.70 — the top of the range.

T4 therefore held emphatically (`{service_diversity}` against six of seven),
and the experiment-2 inversion itself reproduces on the post-disposition
substrate for the first time: cross-arm suppression rank correlation
**−0.857** at 200 s (recorded run: −0.893) and +0.252 at 2 000 s (recorded:
+0.286). Fresh numbers, same shape.

Frontier table (200 s, cell means; suppression vs that arm's no-MTD baseline
of 38.40 / 5.88 hosts):

| condition | occupancy | suppression (inherited) | suppression (profiled) |
|---|--:|--:|--:|
| Service Diversity | 0.353 | **90.4 %** | 35.4 % |
| OS Diversity | 0.403 | 88.8 % | 39.1 % |
| random (multi) | 0.453 | 71.6 % | 70.1 % |
| alternative (multi) | 0.455 | 68.5 % | 68.4 % |
| IP Shuffle | 0.501 | 22.1 % | 87.8 % |
| Complete Topology | 0.552 | 18.2 % | **88.8 %** |
| simultaneous (multi) | 0.699 | 66.1 % | **89.5 %** |

## 7. The price of the operating point

**At the 200 s interval the substrate spends between a third and seven-tenths
of the entire run with a resource layer under active reconfiguration**
(occupancy 0.353–0.700). The interval every published run of this project
inherited is not only inside the success-degenerate region — it is an
extreme-disruption operating point, and every suppression figure previously
reported at it was earned at that unpriced cost. At 2 000 s occupancy falls to
0.038–0.113.

**T5 held (14 of 14 cells, disjoint CIs), and suppression falls with it in all
14** — so the mutation-interval dimension reads as movement *along* the
frontier: relaxing tempo buys the defender out of disruption and out of
protection together, on both arms.

**The realised-tempo confound is measured, as committed.** The simultaneous
scheme executes **150.0 mutations per run against 75.0** for every other
scheme at the same nominal interval, with 38.0 suspensions per run — the only
condition with non-zero contention — which is why it tops the occupancy range
(0.700). Its first-place suppression of the profiled attacker is bought at the
family's highest price, and (per experiment 2 §10) is substantially a pressure
effect. Occupancy decomposes cleanly by layer: single mechanisms are
single-layer by construction; the simultaneous scheme's union (0.700) is well
below its layer-sum (~0.90 of the horizon), the overlap being network- and
application-layer mutations deploying concurrently.

## 8. T2 moved — realised disruption is *almost* a defence property, and the exception is legible

Occupancy CIs overlap between arms in only **6 of 14** cells, under the
pre-registered bar of 11, so the frontier is reported with per-arm axes (as
the figures already are). Two mechanisms produce the divergence, and both are
worth having on record:

- **The defence stands down when it loses.** The substrate's trigger loops
  return once the network is compromised, so a baseline run that reaches the
  objective accrues no further mutation windows while the clock runs to the
  horizon: at 2 000 s (27 of 70 MTD-arm baseline runs reach the objective)
  objective-reaching runs average occupancy 0.046 against 0.058 for
  horizon-reaching ones. Realised disruption depends on how long the defence
  keeps operating, and the attacker's success curtails it — a genuine,
  attacker-dependent property of realised cost, not a measurement artefact.
- **Fourth-decimal separations under near-deterministic timing.** At 200 s the
  arm difference is ≤ 0.0015 absolute (e.g. 0.4026 vs 0.4034 under OS
  Diversity), yet CI-disjoint because the substrate's σ = 0.5 draws make
  intervals of ±0.0002. The two arms consume the shared substrate RNG stream
  differently, so execution-window draws differ microscopically. The letter of
  T2 moved; the practical divergence at 200 s is under 0.4 % of the measured
  value.

Bounded conclusion: a shared disruption axis would mis-state nothing by more
than 0.009 absolute anywhere in this matrix, but per-arm axes are kept, per
the pre-registration, and the stand-down effect above is the reason they
should stay.

## 9. Committed cross-checks

- **Interrupt tallies.** The substrate's own attack-interrupted count equals
  the movement records' interrupted count in 796 of 800 movement runs; the
  four exceptions are all `simultaneous_multi` at 200 s, off by exactly one,
  in runs terminating just short of the horizon (14 929–14 975 s) — an
  interrupt fired after the walk's final record. Boundary artefact, recorded.
- **`none` cells** read identically zero on every disruption field, both arms
  — the ledger's null is a true null.
- The profiled attacker reached the objective **0 of 800** times, consistent
  with every prior run; T3/T4's suppression axis is breadth, which
  discriminates inside the degenerate region.

## 10. What this licenses, and what it does not

The frontier prices the defence family **within this substrate**: occupancy is
a floor (three undercounting blind spots, §3), sim seconds map to no
real-world availability figure, and mechanism-level Pareto sets at ten seeds
are directional. The movement arm pools the five profiles; per-profile
frontiers inherit experiment 2's profile × mechanism interaction and are a
supplementary reading, not made here. **No composite score exists anywhere in
this work**, and no give-up rule was introduced (§5's ranking stands; the
disengagement measure remains with its own handoff, gated on D-09).

What it adds to the record: the project's evaluation now carries **both sides
of MTD's trade inside one run**, and its sharpest prior result gains a price
tag — behavioural fidelity does not merely invert which defence you would buy
(experiment 2); it decides **whether the purchase involves a trade-off at
all** (§6). That statement is invisible to any evaluation that measures only
the attacker's half.
