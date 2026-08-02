---
status: durable
created: 2026-08-02
topic: "The iterated cost model — a state-conditioned expected cost and an enabling-value benefit, built against the R2 defect and swept over 4 200 runs. The verdicts, the stopping rule that fired, why the axis-6 badge does not move even though U3's threshold was passed, and the ranking inversion the measurement found in the brief's own recommendation"
---

# The iterated cost model — what the repair fixed, what it did not, and why the badge stays

**Status:** durable results record. It discharges the iterated-cost-model handoff
under Marc's disposition (option 4 of that brief's §2.3 — both changes, run as
three arms — with the S2 gate cleared for a reported experiment). The design and
the conclusions were pre-registered in
[`iterated_cost_model_prereg.md`](iterated_cost_model_prereg.md) and committed
before a single row existed; the mechanism is factor 7 of
[`modulator_composition.md`](modulator_composition.md).

**The headline, stated first because it is not the flattering one.** The repair
works, partially, and **in the half the brief expected least**. U2 — the
conclusion the whole build was aimed at — **moved**, which fires the
pre-registered stopping rule. The axis-6 badge **does not move**, and the reason
is stronger than a failed threshold: U3's criterion was passed by a *negative
control that cannot possibly carry the mechanism*, so it cannot be read as
evidence for anything. And the brief's own recommended minimum, change A, is the
change that fails; change B, which the brief ranked "weaker than A on every
axis", is the one that pays.

## 1. What was built

Two changes to the axis-6 decision model, each computed from artefacts already on
disk, neither declaring a new magnitude. ρ, `cost_floor_s` and λ keep their values
and their bands; what changed is what they are applied to.

**Change A — expected cost.** `cost*(b | s) = duration(b) + enabling_cost(verb(b), s)`.
`enabling_cost` is a shortest-path search over the declared precondition
relation's eight-state capability closure: the cheapest ordered verb sequence
taking the capabilities the attacker currently holds to a set satisfying
`verb(b)`'s requirement, each verb priced by the cheapest tactic dispatching it
under the run's controller mapping. A search rather than a sum, because
`ENUM_HOST` *clears* `curr_ports` while producing `curr_host`, so the chain has
ordering effects no unordered set of missing prerequisites can express.

**Change B — enabling value.** The benefit numerator's stage-gap distance is
measured through the profile's own routing net instead of the lifecycle-stage
ordering: 1.0 at an objective, `rho^(1 + hops)` elsewhere, and the shipped
stage-gap value where the net affords no directed path.

Both are selectable by arm, and the `declared` arm reproduces the shipped
modulator's factors exactly — asserted over every place of every profile's net
under both mappings — so the comparison baseline is the model every recorded
figure in this project was produced by.

### 1.1 The mechanism does what it was designed to do, shown before the sweep

Worked on the decision the defect record uses,
[`cost_model_plain.md`](cost_model_plain.md) §2.2a's own example —
`pure_steal` at *collection*, `v1_ckc_total`, λ = 1:

| candidate | shipped factor | iterated, unready | iterated, ready |
|---|--:|--:|--:|
| exfiltration (the objective) | 1.176 | **2.145** | 1.176 |
| credential-access (4.5 s, precondition-coupled) | **2.353** | 0.920 | **2.353** |
| command-and-control | 0.235 | 0.479 | 0.235 |
| stealth | 0.235 | 0.455 | 0.235 |

The shipped model prefers a tactic that cannot run over the objective it is
walking toward. The iterated model reverses that when the prerequisite is unmet
and **returns to the shipped preference exactly** once it is met, which is what
makes this a repair confined to the situation the defect concerns rather than a
different model. And the MTD response is layer-specific by construction: an
application-layer mutation leaves the factors bit-identical, a network-layer one
does not, because `mtd_clears` says the first destroys nothing and the second
destroys the position the chain was walked from.

## 2. The sweep

4 200 runs on the current substrate (freshness checked: nothing has touched it
since `816b300`). Main matrix 3 400 runs — λ ∈ {0, 0.5, 1, 2, 4} × 4 arms × 5
profiles × 2 mappings × 2 MTD conditions × 10 seeds, at the 15 000 s horizon and
the 200 s operating interval. Layer sub-study 800 runs — λ ∈ {0, 1} ×
{declared, A, AB} × 4 single-mechanism conditions × 5 profiles × 10 seeds on
`v2_partial`. Workspace `data/results/iterated_cost/` (untracked/regenerable per
the experiment-workspace convention).

### 2.1 Verdicts

| | Conclusion | Verdict |
|---|---|---|
| **U1** | the ablation is still exact | **held** — discharged as a test over the full configuration grid, per arm, rather than sampled |
| **U2** | the repair reaches the wall | **MOVED** on every arm and both mappings (best cell 1 of 5 profiles) |
| **U3** | MTD's measured effect changes with cost-sensitivity | **MOVED** — and see §4, which is the important part: the threshold was passed, by the control arm too |
| **U3b** | the response is layer-specific | **MOVED**, on the same reading and for the same reason |
| **U4** | the repair is not bought with plurality | **held for change B** (5/5, both mappings); **MOVED for change A** |
| **U5** | the attacker is not simply better | reported, no pass/fail sought — §6 |

**U2 moved, so the stopping rule fired.** No arm was added, no λ chosen, and no
criterion relaxed. §4's reading of U3 *tightens* a criterion rather than
loosening one — it declines a badge the bare threshold would have granted — which
is the opposite of the drift the rule exists to prevent.

## 3. U2 — the repair reaches the wall directionally, and misses its own bar

U2 required the blocked fraction at the declared λ to be **lower** than the
declared arm's with **disjoint 95 % intervals** on ≥ 3 of 5 profiles. Across the
six arm × mapping cells the bar is met on **3 of 30 profile cells**.

**The direction is nonetheless there, and reporting the threshold without the
continuum beside it would be the exact failure the sensitivity-study precedent
warns against.** Of the 30 profile cells, 17 are directionally lower; change AB
is lower on 4 of 5 profiles under both mappings. Pooled across profiles at the
declared λ (a **post-hoc** diagnostic, written after the verdicts and labelled as
one, n = 50):

| condition | λ = 0 | declared | A | B | AB |
|---|--:|--:|--:|--:|--:|
| `v1_ckc_total`, no MTD | 0.498 | 0.538 | 0.559 | 0.478 | **0.389** |
| `v1_ckc_total`, MTD | 0.925 | 0.903 | 0.884 | 0.901 | 0.887 |
| `v2_partial`, no MTD | 0.208 | 0.299 | 0.273 | 0.293 | **0.218** |
| `v2_partial`, MTD | 0.519 | 0.705 | 0.731 | 0.589 | **0.570** |

Pooled, `AB` sits CI-below the declared arm on both `v2_partial` conditions and
`B` on the MTD one. On `v2_partial` under MTD the repair undoes **73 %** of the
blocked-fraction rise the shipped model caused (0.519 → 0.705 → 0.570), and 89 %
of it without MTD. So the defect's signature is real and the repair reaches it;
what the study cannot do is separate it **per profile** at ten seeds. U2 stays
moved on its own terms, and the honest summary is *directionally confirmed,
not established at the pre-registered resolution*.

**Efficiency tells the same story more sharply.** Successes per attempted action,
`v2_partial` under MTD: λ = 0 arm 0.370, shipped model 0.119, change B **0.241**,
change AB 0.218. The shipped model wastes two of every three actions it added;
change B recovers half of that waste.

## 4. Why the badge does not move — U3 was passed by a negative control

This is the most important result in the record, and it is a result about the
**criterion**, not about the mechanism.

U3 took C4's criterion verbatim, deliberately, so the verdicts would be
comparable: the action-mix JSD between λ = 0 and λ = 1 must be larger under MTD
than without it, on ≥ 3 of 5 profiles. On the bare threshold it **passes** — 4 of
5 for `declared`, `B` and `AB` on `v2_partial`, 4 of 5 for `declared` and `B` on
`v1_ckc_total`.

**The `declared` arm passes it. That arm is the shipped model, which F6 proved by
spike cannot see MTD at all** — its factor table is precomputable and the MTD
condition is not among its inputs, reproducing the stateful run 30 of 30
bit-identical ([`fidelity_implications.md`](fidelity_implications.md) F6). A
criterion passed by a mechanism that provably lacks the property the criterion
tests is not measuring that property. It is measuring something else, and the
per-profile continuum says what:

| arm | per-profile ratio (MTD shift ÷ no-MTD shift), `v2_partial` | within ±15 % of 1.0 |
|---|---|--:|
| `declared` | 1.017, 1.034, 0.957, **1.839**, 1.040 | 4 of 5 |
| `A` | 1.016, 1.031, 0.785, **1.559**, 0.999 | 3 of 5 |
| `B` | 1.039, 0.994, 1.015, **2.474**, 1.006 | 4 of 5 |
| `AB` | 1.000, 1.043, 1.014, **2.462**, 1.052 | 4 of 5 |

Four of five ratios sit on 1.0 in every arm, and the pass is carried by
`double_extortion` — the single profile the shipped record already names as this
family's outlier under both C4 and C6. **This is C4's own artefact reproduced
exactly**, and the recorded reading of C4 settles how to read it: *"the honest
reading is that the effect is absent on both mappings, `double_extortion`
excepted, and C4's 3/5 is a coin-flip on noise rather than evidence"*
([`incentive_rationality.md`](incentive_rationality.md) §6.1).

**U3 is therefore recorded MOVED**, on the identical reading its parent criterion
is recorded moved on, and **axis 6 stays DESIGNED**. Reporting it as held —
which the bare threshold licenses — would move a badge on a statistic a negative
control passes.

### 4.1 U3b fails in the same way, and it was written to be able to

The layer sub-study asked whether the response is larger under the
position-destroying family (Complete Topology, IP Shuffle) than under the
diversity family (OS, Service). It passes at 4 of 5 for **all three** arms — again
including `declared`. The per-profile ratios are 1.055, 1.070, 0.973, 1.555,
1.030 for `declared` and 1.015, 1.065, 0.963, 2.318, 1.029 for `AB`: the same
shape, the same single outlier, and no separation between the arm that has the
mechanism and the arm that cannot.

The pre-registration said a uniform response across families would falsify the
mechanism's claim. What happened is stronger evidence than that: a **control arm
that cannot see either family reproduces the split**, which means the quantity
measures how much each mechanism disturbs the walk — a property of the substrate
— rather than how the cost term responds to it. **U3b moved, and it did the job
it was written for**: it stopped a held U3 from being read as mechanism.

## 5. The ranking inversion — the brief's recommended minimum is the change that fails

The handoff ranked change A "the **recommended minimum** … repairs the wall and
opens the MTD channel" and change B "weaker than A on every axis". **The
measurement inverts that ranking**, and this is the finding most worth carrying
forward.

**Change A alone fails on its own terms.** It *raises* the blocked fraction in
half the cells (`v1` no-MTD 0.559 against the declared arm's 0.538; `v2` under
MTD 0.731 against 0.705), it recovers no compromise breadth anywhere, it drops
success-per-action below the shipped model on `v2` (0.080 against 0.119), and it
is the only arm that **fails U4** — pooled path entropy falls against the
declared arm in 5 of 5 `v2_partial` profiles, by 0.06 to 0.31 bits. A change
justified as opening a channel to the defence bought a further collapse of
traversal and no progress.

**Change B alone is what pays.** It never costs plurality — U4 held 5 of 5 under
both mappings, with entropy *rising* 0.05 to 0.46 bits against the declared arm —
it recovers 36 % of the host loss under MTD on `v2_partial`, and it doubles
success-per-action there (0.119 → 0.241). Across the whole declared band the
contrast is starker still (`v2_partial`, pooled):

| λ | declared: entropy / hosts | change B: entropy / hosts |
|---|--:|--:|
| 0 | 2.613 / 3.01 | 2.613 / 3.01 |
| 1 | 2.002 / 1.38 | **2.209 / 1.72** |
| 2 | 1.102 / 0.64 | **1.522 / 0.56** |
| 4 | 0.655 / 0.22 | **1.008 / 0.23** |

**Change B substantially arrests the entropy collapse that the axis-3 trade rests
on** — at the near-greedy band end it holds 1.008 bits where the shipped model
holds 0.655. That is a genuine, unlooked-for result: the shipped record presents
the collapse as the price of cost-sensitivity, and half of it turns out to be the
price of measuring value in the *wrong graph*.

**Why the inversion happened, as far as the evidence supports.** Change A prices
the enabling chain but still values the destination by lifecycle proximity, so it
makes the enabling steps *expensive to skip* without making them *worth taking* —
it discourages the unready exploit and gives the attacker nowhere better to go,
and the routing mass lands on whatever is nearest the objective. Change B does
the opposite: it credits the tactic that leads somewhere, in the profile's own
net, which is where "what this unlocks" was always going to be legible. The
defect was diagnosed as two terms failing in the same direction; the repair says
the **numerator** was the load-bearing half. That is not what the design
predicted, and it is recorded as a correction to it.

`AB` sits between the two on most measures and is the best arm on blocked
fraction, which is consistent with A contributing the denominator's wall-pricing
while B supplies the direction to go instead.

## 6. U5 — the attacker is less self-defeating, not better

Committed in the direction that would embarrass the repair, and it does. Distinct
hosts at the declared λ, against **both** the declared arm and the λ = 0 arm
(pooled, `v2_partial`):

| condition | λ = 0 | declared | A | B | AB |
|---|--:|--:|--:|--:|--:|
| no MTD | **4.60** | 2.22 | 2.02 | 2.58 | 2.62 |
| MTD | **1.42** | 0.54 | 0.50 | 0.86 | 0.72 |

On the mapping where the attacker actually compromises hosts, **every arm sits
below the λ = 0 arm**, and no per-profile ordering is CI-supported in any of the
ten reported cells (`ordering_supported` is False throughout, so none is
claimed). The repair recovers 15–36 % of the breadth the shipped model gave up
and does not approach the cost-blind attacker.

**The honest statement is the one U5 was written to permit: the repaired attacker
is less self-defeating than the shipped one, and still worse than no cost model
at all.** No performance claim is made, and none was sought. On `v1_ckc_total`
without MTD `AB` does exceed the λ = 0 arm (0.64 against 0.54 hosts) — that cell
is reported for completeness and carries no claim: it is one condition of four,
the intervals do not separate, and the mapping is the one on which the attacker
compromises almost nothing in any arm.

## 7. What this licenses, and what it does not

**Licensed.**

- The R2 defect is real, is repairable without a new declared magnitude, and the
  repair is measurable: the blocked-fraction rise is 73–89 % undone in the
  pooled `v2_partial` cells and success-per-action roughly doubles.
- **The numerator was the load-bearing half of the defect** (§5), which inverts
  the design's own ranking and is the most transferable thing here.
- The entropy collapse attributed to cost-sensitivity is substantially an
  artefact of measuring benefit in the lifecycle ordering rather than in the
  profile's own net.
- **C4's criterion does not discriminate**, shown by a negative control passing
  it (§4). Any future use of the action-mix-JSD-under-MTD statistic needs a
  control arm beside it.

**Not licensed.**

- **No badge move.** Axis 6 stays DESIGNED. U3's threshold pass is not readable
  as mechanism, and U2 — the conclusion the build was aimed at — moved.
- **No claim that the attacker performs better**, and no operating λ
  recommendation. λ = 1 remains the declared value on its meaning alone.
- **No ranking of profiles or of MTD mechanisms.** The sub-study separates two
  families and is not powered to order four mechanisms.
- **No composition with the axis-7 readiness learner**, which was not run and is
  barred until a fresh joint check does — change A and the learner condition on
  the same readiness bit against the same artefact
  ([`modulator_composition.md`](modulator_composition.md)).
- **No re-reading of any recorded experiment.** The frontier, experiment 2 and
  the axis sweeps stand as records of the model they ran under.

## 8. What a successor should do, and what it should not

**Should not:** re-specify U2 and re-run. The stopping rule fired, and the reason
it exists is that a repair motivated by a published defect is exactly the
circumstance in which criteria drift. The result stands as measured.

**Should, in priority order:**

1. **Take change B seriously on its own.** It is cheap, stateless, costs no
   plurality, and is the half that paid. It surrenders none of F6's
   precomputability, so it is not even a candidate for the MTD channel — which
   makes it a clean axis-3-and-progress improvement with no claim attached.
2. **Power U2 properly if it is worth settling.** Ten seeds per profile cell
   cannot separate a difference this size; the direction is consistent in 17 of
   30 cells and pooled separation exists on `v2_partial`.
3. **Replace C4's statistic before anyone uses it again.** §4 shows it passes for
   a model that cannot see the defence. A measure of MTD-conditional response
   needs to be validated against a negative control before it can carry a badge.

## Evidence

- [`iterated_cost_model_prereg.md`](iterated_cost_model_prereg.md) — the design
  and the five conclusions, committed before any row existed.
- `data/results/iterated_cost/` (untracked/regenerable) — `run_sweep.py` carrying
  the same criteria in its docstring, `analyse.py` computing every verdict from
  the rows, `verdict.txt` and `verdicts.json`.
- [`utility_iterated.py`](../../../../src/mtdsim/l3_simulation/movement/utility_iterated.py)
  and its suite `tests/l3_simulation/test_movement_utility_iterated.py` — the
  mechanism and the four gates (λ = 0 exactness per arm, no new declared value,
  the laundering check, determinism).
- [`cost_model_plain.md`](cost_model_plain.md) §2.2a — the defect this repairs.
- [`incentive_rationality.md`](incentive_rationality.md) §6.1, §6.3 — C4's
  recorded verdict and the reading §4 applies to U3.
- [`fidelity_implications.md`](fidelity_implications.md) F6 — the precomputability
  property change A surrenders, and the negative control §4 rests on.
