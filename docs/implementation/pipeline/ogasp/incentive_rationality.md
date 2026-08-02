---
status: durable
created: 2026-07-29
topic: "Criterion axis 6 (incentive-driven rationality) — the attacker utility modulator: a declared per-tactic benefit over the already-declared duration catalogue, entering routing as a rationality exponent whose zero recovers today's model exactly. Records the model, the one new declared family and why it is not a restatement of the distance kernel, the pre-registered sweep conclusions, and the honest size of the claim."
updated: 2026-08-01
---

# The attacker utility modulator — design, declared values, and the pre-registered sweep (axis 6)

**Status:** durable design-and-build record. It ships the first modulator with a
declared value on the attacker-state seam
([`attacker_state_seam.md`](attacker_state_seam.md)), and it consumes the cost
ledger from [`measurement_suite.md`](measurement_suite.md), which the criterion
names as the prerequisite measurement for any claim on this axis. It discharges
the handoff `2026-07-28_axis6_incentive_rationality.md`.

**The governance question is the seam's, and it is still open.** The seam record
§7 asks Jin to confirm that a within-run, movement-layer, null-equivalent
attacker state is refinement of the movement layer under M7 rather than the
attacker-state change S2 defers. This build inherits that argument and does not
re-litigate it. What is safe to *build* under the null-equivalence guarantee is
built here; what is gated on the confirmation is wiring a non-zero λ into a
reported experiment.

## 1. The axis, and what the model scored before this

Cho et al. model the sophisticated attacker as "a rational actor that is
sensitive to incentives, such as attack success with minimum cost", and name the
asymmetry as an under-developed dimension: the rational-actor framing is applied
to defenders and seldom to attackers. Every model in the criterion's
cross-section scores negative on it, and this one added nothing — the movement
layer's transition weights are flow-proportion frequencies (evidence of what
campaigns did, not a cost/benefit calculation) and the outcome overlay is a
declared policy, not a utility. The RoA-ordered exploit selection survives inside
the inherited action layer, so the model inherited exactly the partial credit the
lit review gives Brown and Tay, which that review calls **rationality without
capability**: a defender-computed ordering the attacker optimises without being
able to sequence, adapt, or remember.

Why it matters beyond the rubric: MTD's economic argument *is* raising attacker
cost, and that is only measurable against an attacker that has a cost model and
conditions decisions on it. Every result this project had produced measured MTD's
effect on an attacker to whom cost was invisible.

## 2. The mechanism

One modulator on the seam. At a routing decision from place `a`, the factor
applied to destination `b` is

```
    m(a→b)  =  ( u(b) / ū )^λ        where    u(b) = benefit(b | profile) / max(cost(b), cost_floor_s)
```

with `ū` the mean utility over the source's out-set. It multiplies the composed
distribution and the composition renormalises, exactly as the seam's §2 rule
specifies — multiplicative, never additive, for the reason the overlay design
won on: multiply-then-renormalise conditions the grounded proportions without
inventing a magnitude or inverting the corpus's within-class ordering.

Three properties of that expression are load-bearing:

- **λ is the rationality exponent, and λ = 0 recovers today exactly.** `x ** 0.0`
  is exactly 1.0 in IEEE arithmetic for any finite positive `x`, so at λ = 0 the
  product is exactly 1 and the arithmetic reduces to the current two-factor rule.
  The current model is therefore the λ = 0 *special case* of this one, which
  gives the ablation for free and makes the comparison honest: the conditioned
  and unconditioned arms differ by one declared parameter, never by wiring. The
  implementation deliberately does **not** special-case zero — the identity is a
  property of the maths, and testing it that way is a stronger claim than
  short-circuiting it.
- **Normalising by the out-set mean is what makes λ scale a ratio** rather than
  an absolute magnitude. It is behaviourally free (the composition renormalises,
  so any common rescaling cancels); it is there for the parameter's meaning and
  for the legibility of the state's per-decision log, where a factor then reads
  as "how much this destination beat the local average".
- **No factor can reach zero.** Benefit is `rho^(1+gap)` with `0 < rho < 1` and
  cost is floored above zero, so utility is strictly positive. The seam's stall
  rule — a modulator may not return 0.0 without declaring `may_zero` and re-running
  the no-stall check — is therefore never engaged, and the modulator can suppress
  an out-edge's share but never remove it. This is asserted over every profile's
  every out-set at both ends of both declared bands, not argued.

**Determinism (SIM-05).** The factor is a pure function of declared data and the
current place: it reads no history off the state and draws from no random stream,
so the seam's fourth RNG stream is left untouched and a conditioned run
reproduces exactly.

## 3. The cost term — reused, not re-declared

`cost(b)` is the tactic's declared duration from
[`tactic_durations.json`](../../../../data/ogasp/tactic_durations.json). This is
a deliberate reuse rather than a new family: a parallel cost catalogue that could
drift from the durations would be worse than no cost model at all, and reusing
the catalogue means this factor's cost half inherits the durations' tier badges
and their already-completed sensitivity sweep instead of needing a fresh one.
The positioning is the cleanest available: Ho 2024 defines return on attack cost
as reward over attack cost with **cost defined as time to exploit**, so time is
the cost term the lineage already uses — this is its attacker-side,
tactic-granularity analogue.

**The declared floor, and why it is not 1.0.** `resource-development` is declared
`duration_s = 0.0`, so the ratio needs a floor. The floor is a **named declared
parameter** (`cost_floor_s`), reported in the compiled view and in the sweep
design, never a silent `max()` buried in the modulator. Its value follows from
what the catalogue's zero *means*: the tactic's real effort — weeks to months of
tool and infrastructure preparation — happens **off the simulator's clock**, not
for free. A floor chosen to make an un-metered tactic read as costless would
invert exactly the quantity this axis exists to model. The floor is therefore set
at the cheapest *metered* action in the catalogue, the exploit-shaped anchor at
**4.5 s**, so an un-metered tactic reads as no cheaper than the cheapest thing
the simulator does price. The band brackets that between the naive reading of the
zero (1.0 s, effectively free) and the low-and-slow anchor (45.0 s).

The floor is expected to be load-bearing — it alone decides whether the off-clock
tactic sits at the top or the middle of the utility ordering — which is why it is
swept rather than merely declared. That expectation is pre-registered below as
conclusion C6.

## 4. The benefit term — the one new declared family

Fifteen values per profile, rule-generated from a stated model, never hand-set
per tactic. The rule is **objective proximity within the profile**:

- `objective` — a tactic in the profile's own declared objective set carries the
  unit of benefit, 1.0;
- `instrumental` — every other tactic is instrumental, worth `rho^(1 + gap)`,
  where `gap` is the minimum number of consensus lifecycle stages separating it
  from the profile's nearest objective. The `+1` is structure, not a magnitude:
  even a same-stage non-objective sits one decay step below the objective it
  serves, because value accrues *at* the objective.

`gap` is unsigned on purpose — proximity to an objective is a distance, and a
tactic seated past the objective's stage is no closer to achieving it than one
seated the same separation before it.

Every input is read from its own home rather than restated: the objective sets
from the GASP class-semantic declarations (`petri/analysis.OBJECTIVE_TACTICS`),
the stage ordering from
[`lifecycle_consensus.json`](../../../../data/ogasp/controller/lifecycle_consensus.json),
the cost from the duration catalogue.

### 4.1 Why this is not the lifecycle-distance kernel wearing a hat

The most serious design risk on this axis: the routing weights **already** grade
a transition by how far it travels, and if benefit does the same thing again the
model double-counts distance and this factor is not measuring incentive at all.
Two properties separate them, and both are regression-guarded in the test suite
rather than argued in prose:

| | outcome overlay's distance kernel | this benefit family |
|---|---|---|
| what it grades | the **jump**: a signed source→destination stage offset | the **destination**, relative to this profile's objective |
| depends on the source | yes, necessarily | **no** — the utility of arriving at `b` is one number whatever `a` was |
| varies between profiles | **no** — identical for all five | **yes** — that is the whole point |

The sharpest case is `command-and-control`: benefit 1.0 under
`infrastructure_setup`, whose declared objective it *is*, and 0.25 under
`pure_steal`, where it is merely instrumental. `impact` inverts between the two
single-objective profiles the same way. The kernel cannot express either, because
it never sees which profile is walking.

Per-profile is also a necessity, not a refinement: `infrastructure_setup`
contains no exfiltration or impact node at all, so a benefit model keyed on a
universal objective would be meaningless there.

### 4.2 Tier, honestly

Every value in this family sits at **`declared-judgement`** — the honest floor
tier of [`declared_value_provenance.md`](../../declared_value_provenance.md) §2.
No source in the corpus assigns a per-tactic benefit. What the literature
supplies is a *mechanism* and not a magnitude:

- **FlipIt** (via [`persistence_reset_models.md`](../../../sources/extractions/persistence_reset_models.md))
  gives the citable cost/benefit mechanism — each player's benefit is the
  fraction of time controlling the resource minus the average move cost, and at
  the periodic-game equilibrium **the player with the higher move cost has
  benefit zero**. This is the anchor for "cost is decisive to an attacker", and
  a far stronger citation than a general appeal to rationality.
- **RoA / RoAC** ([`ho2024.md`](../../../sources/extractions/ho2024.md)) is the
  positioning precedent already inside the lineage, cited and deliberately **not
  consumed** — see §7.
- **MAL / coreLang** is the published precedent for assigning each attack step a
  declared distribution for the effort to complete it.
- **Maleki 2016** gives the one row linking attacker expenditure to outcome:
  MTD-defeat probability rises with attacker time and cost.

None of these fixes a number. Because the tier is the floor tier, the **sweep,
not the argument, is what these values' defence rests on** — and unlike the
outcome overlay, which carries review rounds R0–R4, this family has had **no
adversarial cross-examination round at all**. That gap is stated in the ledger
rather than implied, and a cross-examination round is the obvious next
maintenance step.

> **Discharged 2026-08-01 (round R1).** The cross-examination ran as an
> attempted removal: a pre-registered reproduction check replaced the graded
> family with binary objective-membership and the binary attacker failed to
> reproduce in 31 of 40 cells, in exactly the direction the rule predicts —
> the stage-gap term is what holds the attacker's preference tilted toward
> its own objective's neighbourhood, and the divergence is absent precisely
> where the stage gaps are smallest (`infrastructure_setup`, all eight cells
> reproduce) and largest for `double_extortion`, this family's recorded
> outlier. The
> family survives its first adversarial round with its complexity shown to be
> load-bearing. Verdict and evidence:
> [`cost_model_plain.md`](cost_model_plain.md) §2.1; ledger entry in
> `attacker_utility.json`.

### 4.3 The three requirements, discharged

The declared-value precedent asks that a declared family be reproducible, tiered
and scrutinised.

1. **Reproducible.** The table is rule-generated by a tracked generator,
   `mtdsim.l3_simulation.movement.utility`, with `--write` / `--check` mirroring
   the overlay compiler's contract: **0 of 75 cells differ** between a fresh
   compilation and what is committed, checked in the test suite rather than by an
   in-session script. Coverage is complete — every seated tactic under every
   profile, including tactics a profile's net has no place for, because the
   declared layer authors the whole space and the data layer decides which cells
   route mass.
2. **Tiered.** §4.2; every entry `declared-judgement`, stated as such.
3. **Scrutinised.** §5's sweep, with the conclusions committed before any output
   existed. The absent cross-examination round is recorded as the gap it is.

## 5. The pre-registered sweep — conclusions committed before the numbers

**This section was written and committed before the sweep was run.** The git
history is the audit trail; `data/results/axis6_rationality/run_sweep.py` carries
the same conclusions and criteria, and `analyse.py` computes a held/moved verdict
per conclusion from the rows rather than asserting one.

This is where the axis is most exposed. A cost-sensitive attacker that gets
further is a nicer result, and choosing λ because of that is exactly the
reverse-engineering the declared-value guardrails forbid
([`declared_value_provenance.md`](../../declared_value_provenance.md) §5). So λ's
band is declared from what the parameter *means* — λ = 0 is indifference, λ = 1
is preference proportional to normalised utility (the canonical rational-actor
reading and the only value in the band whose interpretation is not arbitrary),
and large λ is near-greedy — and the conclusions are fixed in advance.

**Design.** Nine sweep points (λ ∈ {0, 0.5, 1, 2, 4}; then `rho` and
`cost_floor_s` one at a time at the declared λ = 1), five profiles, both MTD
conditions, both controller mappings, ten seeds — matching experiment 1 and the
S1 sweep exactly, so the verdicts speak to the recorded findings rather than to a
differently-shaped experiment. The inherited baseline attacker rides along so the
cost ledger is reported per *arm* and not only per profile. Two limits are stated
in advance: the study is **not powered** for any ranking of MTD mechanisms under a
cost-sensitive attacker (that is experiment 2's defence-family sweep), and **no
conclusion rests on ASR**, which discriminates nothing at the 200 s operating
interval per the rate feasibility study's degenerate-region finding.

| | Conclusion | Criterion |
|---|---|---|
| **C1** | The ablation is exact | at λ = 0 the record stream is field-for-field identical to a run with no modulator; zero differing runs |
| **C2** | The mechanism is live | pooled visit-distribution JSD between λ = 0 and λ = 1 exceeds 0.01 on ≥ 3 of 5 profiles, in **both** MTD conditions |
| **C3** | Rising λ collapses traversal diversity (the axis-3 trade, shown not assumed) | mean per-run path entropy at λ = 4 below λ = 0 with disjoint 95 % intervals, on ≥ 3 of 5 profiles |
| **C4** | The action-mix shift is **larger under MTD** — the result the axis exists to produce | JSD(λ=0, λ=1 \| MTD) > JSD(λ=0, λ=1 \| no MTD) on ≥ 3 of 5 profiles |
| **C5** | Cost sensitivity does **not** buy progress | no statistic among {distinct hosts, deepest successful stage, distinct places} shows a CI-separated monotone increase across λ on a majority of profiles |
| **C6** | The declared cost floor is load-bearing | action-mix JSD across the `cost_floor_s` band exceeds that across the `rho` band, on ≥ 3 of 5 profiles |

Two of these deserve their reasoning stated, because their direction is the
guardrail:

- **C4 is the question, and C5 is the trap.** The interesting question is not
  whether a cost-sensitive attacker performs better; it is whether **MTD's
  measured effect changes when the attacker can see cost**. MTD raises the cost
  of some tactics and not others — an interrupted action pays the confusion
  penalty and produces nothing — so a cost-sensitive attacker should shift its
  action mix away from the tactics MTD is taxing. If C4 holds, the project has an
  economic MTD result no attacker in the criterion's cross-section could have
  produced. **If it moves, that is a finding about how coarsely MTD's costs are
  distributed on this substrate**, and it is reported as that rather than
  softened.
- **C5 is committed in the direction that would embarrass a flattering result.**
  "The attacker gets further" is the outcome most tempting to reach for, so the
  pre-registration says it is not expected. A held C5 means the mechanism is not
  being sold on a performance gain it was never entitled to claim.

*(Results and per-conclusion verdicts: §6, added by the commit that ran the
sweep.)*

## 6. Results

> **Magnitudes describe the pre-disposition substrate; conclusions re-verified
> on the current one (2026-08-01).** Two ruled fixes landed *after* this
> sweep's rows were captured on 2026-07-29: `6181305` (the intent-audit
> dispositions — RoA stack, diversity re-roll, User Shuffle blocking) and
> `816b300` (MTD instances registered once per scheme, which legitimately
> moves the `random` scheme's cross-mutation composition). On today's
> substrate most MTD-arm rows and a minority of no-MTD rows no longer
> reproduce, so the figures below stand as the record of that run, per the
> experiment-1 precedent. A fresh 600-run re-run of λ ∈ {0, 1, 4} (Part 1 of
> the rational-attacker handoff) reproduced every qualitative verdict: the
> entropy collapse in all ten profile × mapping cells, the blocked-fraction
> rise to ~99 % at the band end, and C4's absence within ±15 % on eight of
> ten cells with `double_extortion` again the exception. Record:
> [`cost_model_plain.md`](cost_model_plain.md) §2.1.

1 800 movement runs (9 points × 2 mappings × 5 profiles × 2 MTD conditions × 10
seeds) plus 20 baseline reference runs, at the 15 000 s horizon and the 200 s
mutation interval. Workspace: `data/results/axis6_rationality/`
(untracked/regenerable per the experiment-workspace convention) — `run_sweep.py`,
`analyse.py`, and `mtd_tax_anatomy.py`, which was written *after* the verdicts to
diagnose C4 and is labelled as the post-hoc diagnostic it is.

### 6.1 Verdicts

| | Conclusion | `v1_ckc_total` | `v2_partial` |
|---|---|---|---|
| C1 | the ablation is exact | **held** (0 of 30 runs differ) | **held** (0 of 30) |
| C2 | the mechanism is live | **held** (5/5 profiles, both conditions) | **held** (5/5, both) |
| C3 | rising λ collapses traversal diversity | **held** (5/5 CI-disjoint) | **held** (5/5) |
| C4 | the shift is larger under MTD | *held* (3/5) — **but see §6.3** | **MOVED** (2/5) |
| C5 | cost sensitivity does not buy progress | **held** (no statistic improved) | **held** |
| C6 | the declared cost floor is load-bearing | **held** (4/5) | **held** (4/5) |

**C4's threshold verdict is a split, and the split is not the finding — the
continuum is.** Reporting it as "held on one mapping, moved on the other" would
be exactly the failure the sensitivity-study precedent warns about (a threshold
verdict on a continuum, reported without the continuum beside it). The
per-profile ratios of the MTD shift to the no-MTD shift are 0.99, 1.01, 1.27,
0.89 and 1.89 under `v1_ckc_total`, and 0.93, 0.96, 1.00, 1.38 and 0.87 under
`v2_partial`. Eight of ten sit within ±15 % of 1.0. **The honest reading is that
the effect is absent on both mappings**, `double_extortion` excepted, and that
C4's 3/5 under `v1_ckc_total` is a coin-flip on noise rather than evidence. C4 is
recorded as **moved**, on both mappings, and §6.3 gives the anatomy.

### 6.2 What did happen — the mechanism is live and its direction is legible

C2 and C3 are unambiguous, and the shift they measure has a single coherent
shape: **the cost-sensitive attacker moves its effort onto the cheap
exploit-shaped tactics and off the expensive low-and-slow ones.** Under
`v2_partial` at λ = 1 against λ = 0, `pure_steal` moves +0.19 of its visit share
onto credential-access and +0.16 onto lateral-movement (both declared 4.5 s),
while stealth (−0.07), execution (−0.09), command-and-control (−0.06),
persistence (−0.05) and discovery (−0.06) all fall. `infrastructure_setup` shows
the same shape more sharply (+0.25 credential-access, +0.17 lateral-movement;
−0.10 command-and-control, −0.08 collection). This is precisely what a
benefit-per-cost attacker should do, and it is visible without needing a
statistical test.

C3's collapse is severe and worth stating in magnitude: pooled path entropy falls
from 2.23 bits at λ = 0 to 0.24 at λ = 4 for `pure_steal`, and from 1.45 to 0.01
for `infrastructure_setup`. **The near-greedy end of the band does collapse
traversal diversity, shown rather than assumed** — which is the axis-3 trade made
visible, and the reason λ = 4 is a band end and not a candidate operating value.

**C5 held, and it held in a stronger direction than pre-registered.** Cost
sensitivity does not merely fail to buy progress; it *costs* progress. Under
`v2_partial` on the MTD arm the mean distinct hosts fall from 1.42 at λ = 0 to
0.10 at λ = 4, successful actions from 103 to 8, and — the diagnostic number —
**blocked actions rise from 135 of 273 attempts (49 %) to 2 165 of 2 196
(99 %)**. The greedy attacker piles into the cheap tactics, and the cheap tactics
are cheap precisely because the substrate prices them as exploit-shaped, while
being the most tightly precondition-coupled things it can attempt. Recording it
matters because it is the opposite of the flattering result the
pre-registration was written to guard against.

> **The *interpretation* of C5 is qualified, 2026-08-01 (Marc's objection); the
> measurement is not.** This paragraph originally closed by reading the result
> as "experiment 1's H-coupling finding restated in economic terms — on this
> substrate, an attacker that optimises declared cost optimises its way into a
> wall", which attributes the self-defeat to the *terrain*. That reading is
> only available if the denominator is a defensible model of attacker cost, and
> it is not established that it is. The declared-duration cost and the
> objective-proximity benefit penalise instrumental tactics **twice over** —
> reconnaissance is both the slowest tier (35 s against 4.5 s) and the furthest
> from any objective, giving `pure_steal` a 31-fold preference against the very
> tactic that satisfies the precondition for the tactics it prefers — and
> neither term can express *this is worth its price because of what it
> unlocks*. So the competing reading, excluded by nothing measured here, is
> that the wall is a property of the **denominator**. C5's verdict stands as
> recorded (cost sensitivity did not buy progress); the causal attribution does
> not, and no claim of the form *cost-sensitivity costs an attacker progress*
> may be made without this qualification. Diagnosis:
> [`cost_model_plain.md`](cost_model_plain.md) §2.2a. The remedy is designed in
> the iterated-cost-model handoff and is a disposition for Marc, not a
> session's judgement.

### 6.3 Why C4 moved — the anatomy, and why it is not "no signal"

Two mechanisms could produce C4's negative and they have opposite implications,
so the verdict is unreadable until they are separated: either MTD's tax is
undifferentiated across tactics (a finding about the substrate), or it is
differentiated but invisible to this attacker (a finding about the model).
`mtd_tax_anatomy.py` measures which, per tactic-place, over 35 MTD runs.

**MTD's tax is strongly differentiated in absolute terms.** The interrupted
fraction spans 0.011 (lateral-movement) to 0.201 (stealth) — an 18-fold spread —
and the derived confusion penalty per visit spans 0.23 s to 4.13 s. So the first
mechanism is refuted: there is a great deal of signal.

**But the tax is near-proportional to the declared dwell, and a normalised ratio
cannot see a proportional surcharge.** The correlation between a tactic's
declared cost and its interrupt rate is Spearman 0.87, which is mechanically
unsurprising — a longer dwell is likelier to straddle a mutation at a 200 s
interval. Expressed *relatively*, the tax is nearly flat: penalty ÷ declared cost
ranges only 0.032–0.113 about a mean of 0.086, a roughly uniform ~9 % surcharge.
A utility built as a **ratio**, normalised across the out-set, is invariant to a
uniform proportional inflation of its denominator. Re-pricing every tactic's cost
at its MTD-*realised* value rather than its declared one leaves the attacker's
preference ordering essentially unchanged (Spearman 0.95–0.97 across profiles;
the only movement is a swap inside the top three, all of which are the same 4.5 s
exploit-shaped tactics).

**The finding, stated plainly:** on this substrate MTD's cost is levied in
near-proportion to a tactic's declared dwell, so a cost-sensitive attacker
already avoids the MTD-taxed tactics *as a side effect of avoiding the expensive
ones* — and it does so by exactly the same amount whether MTD is running or not.
The economic MTD effect the axis exists to produce is therefore not reachable by
this mechanism on this defence, and the reason is structural rather than a lack
of power or a lack of signal.

Two things follow, and they are the useful half of a negative result:

- **The static-belief explanation is the primary one — CORRECTED 2026-07-29.**
  As first written this bullet claimed the negative "survives the obvious fix",
  on the evidence that re-pricing each tactic at its run-averaged realised cost
  reorders almost nothing. That tests **one** candidate fix and was overstated
  into a general result. Two later measurements move the weight of the
  explanation:
  (i) the modulator is a pure function of declared data and the current place,
  so its factor table is precomputable — proven by a spike that folded the table
  into a plain overlay and reproduced the stateful run **30/30 bit-identical**
  (`data/results/axis6_rationality/collapse_test.py`). The MTD condition is not
  among its inputs, so no parameter choice could have made it respond to MTD.
  That, not the proportional tax, is the first-order reason C4 moved.
  (ii) the **cost** channel is closed but the **realised-success** channel is
  wide open: MTD's per-tactic success ratio spans 0.08–1.02, a 13-fold spread
  that no normalisation cancels. An attacker conditioning on realised success —
  as distinct from realised cost — is not ruled out by anything measured here.
  Full record: [`targeted_attacker_feasibility.md`](targeted_attacker_feasibility.md) §2.
- **What would produce the effect** is therefore either a defence whose cost is
  *not* proportional to dwell (a scheme that taxes particular tactics rather than
  particular durations), or a utility that conditions on something the
  proportional surcharge does not cancel — realised *success* rate per tactic
  rather than realised time. The seam already observes both; that is the
  successor work, not this handoff's.

### 6.4 The cost ledger, per run and per arm (validation gate 3)

The ledger the attacker is now optimising against is reported per run
(`numbers/sweep_per_run.jsonl`) and aggregated per arm
(`numbers/cost_ledger.json`), so the optimised quantity is externally visible
rather than implicit in the modulator. Means over 50 runs per point,
`v2_partial`, MTD arm:

| λ | attempted | blocked | interrupted | successes | dwell (s) | MTD penalty (s) | time in MTD-cut events (s) | hosts |
|---|---|---|---|---|---|---|---|---|
| 0 | 273 | 135 | 44 | 103 | 9 713 | 903 | 2 501 | 1.42 |
| 0.5 | 384 | 220 | 44 | 107 | 9 561 | 910 | 2 397 | 0.92 |
| 1 | 641 | 514 | 48 | 68 | 10 174 | 977 | 2 473 | 0.44 |
| 2 | 1 396 | 1 353 | 49 | 15 | 10 866 | 1 011 | 2 067 | 0.14 |
| 4 | 2 196 | 2 165 | 49 | 8 | 11 112 | 1 012 | 1 468 | 0.10 |

Two readings worth recording. First, `time_residual` is **0.00 at every point**,
so the S3-R regime tripwire the measurement suite installed did not fire: the
substrate is not pricing movement-arm actions behind the movement layer's back.
Second, the interrupt *count* is almost flat across λ (44 → 49) while attempted
actions rise eightfold — the attacker is not being interrupted more, it is
failing more, which corroborates §6.2's precondition-wall reading directly from
the ledger.

The inherited baseline rides along as the per-arm reference: 1 411 attempted
actions and 39.2 distinct hosts without MTD, against 1 743 attempts and 13.1
hosts under it. Its time field (`time_total`) is substrate-priced and is **not**
comparable to the movement arm's under S3-R; only the event-wise quantities are
cross-arm safe, per the measurement suite's enforced comparable type.

### 6.5 C6 — the floor is load-bearing, as pre-registered

The action-mix distance across the `cost_floor_s` band exceeds the distance
across the `rho` band on 4 of 5 profiles under both mappings (e.g.
`infrastructure_setup`: 0.215 against 0.029). The floor is confirmed as the more
influential of the two declared magnitudes, which is why §3 spends its argument
on what the catalogue's zero *means* rather than on convenience. `double_extortion`
is the exception on both mappings (0.114 against 0.122), and the reason is
visible in the benefit table: it is the only profile with two objectives at the
same lifecycle stage, so its benefit spread is the narrowest and `rho` has
correspondingly more room to act.

### 6.6 What the sweep does not license

- **No ordering of profiles** is claimed from any statistic here; the sweep was
  not designed for one and `interval_report` refuses it where it was checked.
- **No ranking of MTD mechanisms** under a cost-sensitive attacker — one scheme,
  one interval, ten seeds; directional, not powered. That is experiment 2's.
- **No ASR-shaped claim**: at the 200 s operating interval the run sits inside
  the degenerate region and ASR discriminates nothing.
- **No operating λ is recommended.** λ = 1 is the declared value because it is
  the only one in the band with a non-arbitrary interpretation, not because the
  sweep preferred it — and nothing here was chosen because it improved an
  outcome. Given C5, the outcome it "improves" is negative anyway.

## 7. Alternatives considered and rejected

- **Lift the substrate's RoA into the attacker's routing directly.** Attractive
  because it is already computed, but it is a *defender-computed* per-host
  ordering inside the action layer, keyed on hosts and vulnerabilities rather
  than tactics; reaching into it would put substrate quantities in the portable
  layer, which is the boundary S3-R was careful to draw in the opposite
  direction. RoA is cited as the positioning precedent and deliberately not
  consumed.
- **A full game-theoretic solve (FlipIt-style equilibrium over the tactic net).**
  Out of scope by project direction, and the extraction that carries FlipIt
  already records the apparatus as out of scope while the mechanism is usable.
- **An additive utility bias rather than a multiplicative exponent.** Rejected
  for the reason the overlay design rejected additive bias: it can invert the
  grounded ordering and needs an arbitrary clamp.
- **A second cost catalogue.** Rejected in favour of reuse — see §3.
- **A cost ledger with no decision rule.** Not an alternative: that is the
  measurement suite's deliverable, and on its own it leaves the axis NOT
  ADDRESSED because nothing consumes it.

## 8. The size of the claim

What this builds is an attacker that is rational **over its own declared beliefs
about cost and benefit** — a rationality *shape*, not a calibrated utility. It
answers Cho's asymmetry; it does not claim the utility is a real adversary's, and
it is not a claim about any real adversary at all. Envelope, not actor, as
everywhere else in this project.

Three limits travel with any use of it:

- the benefit family is `declared-judgement` throughout, and has survived one
  adversarial review round — R1, the attempted removal (§4.2) — while R2
  found a defect (below);
- the cost term is the duration catalogue, whose own tiers are mixed and whose
  scale is *shape-not-scale* — the utility ratio inherits both;
- λ is declared and swept, never fitted, and the swept band is the defence.

**A fourth limit, and it is the one to state first (R2, 2026-08-01).** The two
terms **cannot represent instrumental necessity**, and they fail on it in the
same direction, so the failure compounds rather than cancelling. Benefit grades
proximity to the profile's objective, which scores an enabling tactic as though
unlocking a later step were worth nothing; cost grades declared duration, which
penalises those same enabling tactics again for being slow. A tactic whose
entire value is making another one possible is therefore doubly discounted, and
sharpening λ routes effort away from the prerequisites and into the actions
that depend on them. This is a defect of the *model*, not of the values inside
it — no setting of ρ, `cost_floor_s` or λ repairs it, because the quantity that
would have to be expressed is absent from both terms. It bears directly on how
§6.2's C5 result may be read (see the banner there) and it is the same gap the
axis-6 M8b field names from the MTD-invariance side. Diagnosis:
[`cost_model_plain.md`](cost_model_plain.md) §2.2a; remedy designed in the
iterated-cost-model handoff, gated on Marc's disposition and the freeze.

> **Ruled on, built and swept 2026-08-02 (R3;
> [`iterated_cost_model.md`](iterated_cost_model.md)). This model is unchanged
> and remains the model of record — the repair was built beside it, selectable
> by arm, and its `declared` arm reproduces this modulator's factors exactly.**
> Three results bear on this record and none of them moves the badge.
>
> The fourth limit above is confirmed and partly redirected. The defect is
> repairable with no new declared magnitude, and repairing it measurably works:
> pooled on `v2_partial`, the blocked-fraction rise this mechanism causes is
> 73–89 % undone and successes per attempted action roughly double. But the
> **numerator** turned out to be the load-bearing half — repairing cost alone
> fails outright, while measuring benefit through the profile's own routing net
> instead of the lifecycle-stage ordering is what pays. The limit's claim that
> the two terms compound stands; its implicit weighting toward the cost term does
> not.
>
> **§6.3's diagnosis of C4 gains a harder edge.** That section explains C4 by the
> mechanism's blindness to MTD, and the iterated model was built to open exactly
> that channel. The channel opened and **C4's statistic did not respond in a
> readable way** — because the statistic itself does not discriminate. The
> repair's U3 took C4's criterion verbatim and was passed at 4 of 5 profiles by
> the `declared` arm, the very model F6 proved cannot see MTD at all. So C4's
> recorded verdict was right for a better reason than it knew: not merely that
> this mechanism cannot respond to MTD, but that the measure used to ask would
> not have shown it either. Anyone re-using the action-mix-JSD-under-MTD
> statistic needs a negative control beside it.
>
> **§6.2's entropy collapse is partly re-attributed.** C3 records pooled path
> entropy falling from 2.23 bits to 0.24 across the band and reads it as the
> axis-3 price of cost-sensitivity. Measuring benefit in the profile's net
> instead holds 1.008 bits at the same band end where this family holds 0.655,
> and *raises* entropy against this model in 5 of 5 profiles on both mappings at
> the declared λ. C3's measurement stands as recorded; a substantial part of what
> it measured is now attributable to the benefit family's **graph** rather than
> to cost-sensitivity as such.

## 9. What this does not do

- **No substrate change.** Every line is under `src/mtdsim/l3_simulation/`; the
  literal MTDSim code is untouched, and the substrate's RoA machinery is neither
  consumed nor modified.
- **No change to the durations**, no second cost family.
- **No cross-run memory.** The modulator does not even use the within-run state —
  it is a pure function of declared data and the current place.
- **The badge moves from NOT ADDRESSED to DESIGNED, not to DEMONSTRATED**, and
  the reasoning is recorded here because neither label fits cleanly. NOT
  ADDRESSED ("absent, with no design commitment") no longer describes the axis: a
  declared, tiered, rule-generated, swept cost/benefit decision rule exists, runs,
  and is on record changing both behaviour (C2, C3) and outcome (C5). But
  DEMONSTRATED is **withheld**, because the outcome the axis exists to produce —
  a change in MTD's *measured effect* when the attacker can see cost — did not
  reproduce (C4, §6.3), and the one measured-outcome change the mechanism does
  produce is that the attacker does worse. Calling that DEMONSTRATED would let a
  reader infer the economic MTD result, which the evidence does not support.
  DESIGNED with §6.3 attached is the honest badge; what would move it to
  DEMONSTRATED is stated in the criterion's axis-6 M8b field.
