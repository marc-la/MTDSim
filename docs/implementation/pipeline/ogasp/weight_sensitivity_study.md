---
status: durable
created: 2026-07-28
updated: 2026-07-28
topic: "L3 S1 (study half) — the lifecycle-distance term folded into the outcome-overlay rules, and the sensitivity sweep over its declared magnitudes: the fold-in decision, the composed-net validation, the re-examined caveats, and a mixed stability verdict"
---

# The routing-weight re-derivation and sensitivity study — folding lifecycle distance into the outcome overlay, and sweeping what it declares

**Status:** durable. Executes the study half of **S1**
([`supervisor_decision_register.md`](supervisor_decision_register.md) §S1), the
half its literature counterpart
([`lifecycle_consensus.md`](lifecycle_consensus.md)) was built to feed. Two
separable things are delivered, and they answer different questions:

1. **A re-derivation.** The outcome overlay's rules now carry a *distance*
   dependency, so a transition's likelihood falls with how far it travels across
   the campaign lifecycle. This is the correction the supervisor directed.
2. **A sensitivity study.** The declared magnitudes are swept over their declared
   bands and the experiment's conclusions are checked for movement. This is the
   discipline the evaluation's burden-of-proof note
   ([`../../../notes/ch5_evaluation/evaluation_burden.md`](../../../notes/ch5_evaluation/evaluation_burden.md))
   has been promising since before the numbers existed, and the first declared
   family for which it has actually been run.

**The verdict is mixed, and that is the result.** Two of the four conclusions the
study tested hold across the whole sweep; two move. The sweep also exposed three
things nobody had on a list, including that one of the three declared parameters
— the zero floor carrying the supervisor's "close to, or exactly, zero" ruling —
is **behaviourally inert on this corpus**. None of that is softened into a
caveat below; §6 and §7 state it as findings.

**Reproduce, and the one boundary on every number below.** Workspace
`data/results/s1_weight_sensitivity/` (gitignored by design — regenerable). The
2 600 runs were executed against commit `e84bd2a`, in an isolated worktree, and
that pin is load-bearing rather than incidental: the **S3 stochastic-timing
regime landed at `6696189` while this study was running**, replacing each
tactic's fixed dwell with a draw about its declared mean. Every number here is
therefore from the **fixed-dwell** regime, which is the regime experiment 1's
recorded findings were produced in — the right comparator for a stability verdict
against those findings, and the wrong one for predicting experiment 2. Re-running
the sweep under stochastic dwell would answer a different and also worth-asking
question; it is the sibling study's
(`../../../handoffs/2026-07-28_tactic_rate_feasibility_study.md`), which sweeps
the timing family and should share this study's reporting shape.

```
PYTHONPATH=src python data/results/s1_weight_sensitivity/validate.py
PYTHONPATH=src python data/results/s1_weight_sensitivity/run_sweep.py --stage oat
PYTHONPATH=src python data/results/s1_weight_sensitivity/run_sweep.py --stage corners
PYTHONPATH=src python data/results/s1_weight_sensitivity/analyse.py
```

---

## 1. What changed in the rules, and what did not

**No R2 rule value changed.** The fold-in adds one multiplicative term and
re-sources one existing term. The five success and nine failure rules, their
values, and their rationales are exactly as finalised at R2
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §2).

### 1.1 The fold-in decision: where the relationship comes from

§5 of the consensus record left one decision open — whether the fold-in
recomputes the `relationship` term (forward / lateral / backward) from the
consensus stages, or keeps it on the five-band prior and adds distance
separately. **Decided: recompute from the consensus stages.** The reasoning, and
its cost, are recorded in the rules artefact (`model.relationship`) and here:

- **The two terms would otherwise disagree about direction on 40 of the 210
  pairs.** The distance kernel is defined on the signed consensus stage offset,
  so its sign *is* a relationship claim. Keeping the bands for relationship means
  a pair like `command-and-control → discovery` is "backward" (band 4 → 3) while
  the distance term reads it as travelling nowhere (both consensus stage 2) — the
  backward tier firing on a transition the same value's other term calls lateral.
  One ordering, one direction.
- **It is the better-grounded ordering.** The bands are a declared assumption
  (register §M3, and `success_failure_overlay_design.md` §2.1 labels them
  declared-not-sourced). The consensus seats 9 of 15 tactics from model
  agreement, resolves 5 more by declared rules over sourced inputs, and declares
  1. Re-sourcing the relationship term raises its provenance tier rather than
  adding a second declared layer beside it.
- **It is also what the consensus already ruled.** The band-2/band-3 split
  (consolidate ≺ expand) and command-and-control's band-4 seat did not survive
  the overlay. Keeping the bands for relationship would have preserved exactly
  the two orderings the literature pass found unsupported.

**The cost, stated rather than buried.** The consensus's post-intrusion middle is
one weakly-ordered stage, so 34 of the 40 re-classed pairs move *into* the
lateral class and the middle flattens: success values move 0.6 → 0.5
(forward → lateral) or 0.25 → 0.5 (backward → lateral), failure 0.35 → 0.7 or
0.9 → 0.7. That is a real loss of discrimination. It is accepted because the
discrimination it removes was asserting an order no reviewed lifecycle model
supports, and because the `enables` term still discriminates inside the middle —
40 of the 66 within-stage pairs are enabled, hence 1.0, so the middle is not
uniform.

**The choice was made before any net was walked**, on coherence and provenance
grounds. The study nonetheless *reports* the rejected variant (the distance
kernel over the old band relationship) as one sweep arm, so the record can say
whether the choice matters behaviourally — §8. That arm is a report, never the
selection criterion.

### 1.2 The distance term

```
    d(a,b) = 1                       Δ = 0     (within stage)
             γ^(Δ−1)                 Δ ≥ 1     (forward kernel)
             δ^(|Δ|−1)               Δ ≤ −1    (backward kernel)
    floor:   d < z  reads as exactly 0

    overlay_v(a→b) = rule_value_v(a→b) · d(a,b)
```

with `Δ = s(b) − s(a)` over the consensus stages and the declared parameters
`γ = 0.25`, `δ = 0.5`, `z = 0.1` read from
`data/ogasp/controller/lifecycle_consensus.json` rather than restated. Three
decisions ride with it, each recorded in the artefact:

- **It multiplies both verdicts.** How far a transition travels is a property of
  the pair, not of the verdict. The asymmetry the verdicts need is already in the
  two kernels: forward decay is sharp, backward decay gentle, so the failure
  side's dominant backward moves are barely touched while the success side's long
  forward jumps collapse.
- **It multiplies the dependency gates too.** A gated pair can be implausible for
  two independent reasons — the foothold it needs was not won, *and* it is a
  two-stage leap. Both apply, so both multiply.
- **The floor comparison is strict** (`d < z`), so a value exactly on the floor
  survives. This is load-bearing at one swept corner: `γ = 0.1` puts the two-stage
  forward skip at exactly `0.1`, which under `z = 0.1` survives rather than
  zeroing.

### 1.3 The compiled tables, charted

Three figures, in the same register as the existing v1 matrices, generated by
`data/misc/_viz/outcome_overlay/outcome_overlay_v2_matrix_viz.py`:

| figure | what it shows |
|---|---|
| `outcome_overlay_v2_success_matrix.png` | all 210 declared success values, rows and columns grouped by consensus stage |
| `outcome_overlay_v2_failure_matrix.png` | the same for the failure treatment |
| `outcome_overlay_v2_distance_profile.png` | every pair's value against how many stages it crosses, v1 beside v2, with the suppressed tail on its own 0–0.2 axis |
| `aggregate_lifecycle_graph.png` (`aggregate_lifecycle_graph_viz.py`) | the aggregate profile's 15 tactic places as a node-edge graph, laid out in four stage columns, so an arc's horizontal span **is** its Δ and the distances are verifiable by counting columns |

The graph figure is the one to reach for when the question is "are these distances
real". It shows the 114 transitions that carry mass — 30 forward one stage, 6
forward two, 48 within a stage, 24 backward one, 6 backward two — and it shows,
visually, that **no arc spans three columns**, which is §2's corpus finding in a
form that does not require reading a census table.

The matrices are stage-grouped rather than laid out in the v1 figures' five-band
order, so distance from the diagonal block reads as lifecycle distance; order
*within* a stage is the familiar ATT&CK reading order and asserts nothing, since
the consensus declares stage 2 unordered. The third figure carries the zoom row
because on a 0–1 axis a strongly-suppressed value and an exact zero are
indistinguishable, and §2.1 is precisely about a case where they differ.

**A caveat on the figures themselves:** `data/misc/_viz/` is gitignored, so these
scripts and PNGs are local-only — as every other figure in this project is. Any
figure bound for the dissertation needs its generator tracked first; that is a
repo-wide gap, not this study's, and it is flagged rather than fixed here.

### 1.4 What the compiled table looks like afterwards

Of the 210 ordered pairs, per verdict:

| Δ | pairs | factor at the declared parameters | effect |
|--:|--:|--:|---|
| +3 | 6 | 0.0625 → **0** (floored) | the canonical long jump, now exactly zero — *derived* from the floor, not asserted per pair |
| +2 | 22 | 0.25 | a two-stage skip: suppressed, not banned |
| +1, 0, −1 | 154 | 1.0 | untouched |
| −2 | 22 | 0.5 | a deep fallback: reduced |
| −3 | 6 | 0.25 | full-campaign collapse: clearly distinguishable from the adjacent backward move |

An independent cross-check fell out of the compilation and is worth recording:
**no pair in `enables_on_success` crosses two or more stages** (the offset
histogram over enabled pairs is 4 at −1, 40 at 0, 25 at +1). The `enables` sets
were built from MITRE tactic semantics and the AAR get-in/spread sequences with
no lifecycle model in hand, so their being adjacency-respecting corroborates the
consensus ordering rather than following from it — and it is why the distance
term leaves the enablement tier untouched at the declared parameters.

### 1.4 Reproducibility, and why the values are now versioned

The declared-value precedent requires that values be **rule-generated and
reproducible, not post-hoc**
([`../../declared_value_provenance.md`](../../declared_value_provenance.md) §1).
That claim is now enforced by tracked code rather than by an in-session script:
`mtdsim.l3_simulation.controller.rules` compiles the rules into the 210-pair
views, and `--check` re-compiles **every registered version** and reports any
cell that differs from what is committed. It reports **0 of 420 differing cells
per version**, and a test pins it.

Because experiment 1 ran on the pre-distance values, overwriting them in place
would have made a published result unreproducible from the repo. The compiled
views are therefore a **registry**, in the same shape and on the same ruling as
the controller mapping registry
([`controller_mapping_v2.md`](controller_mapping_v2.md)):
`data/ogasp/controller/overlays/`, one directory per value set, a manifest
recording each version's compilation recipe and what consumed it, selection by
name, and the default deliberately left at experiment 1's value so an unqualified
load still reproduces what has always run.

| version | relationship from | distance | consumed by |
|---|---|---|---|
| `v1_band_relationship` | the five-band prior | — | experiment 1 |
| `v2_lifecycle_distance` | the consensus stages | `γ=0.25, δ=0.5, z=0.1` | this study; experiment 2 next |

Regenerating `v1_band_relationship` from the rules reproduces the experiment-1
artefact **cell for cell** (0 of 420 differences; only the `_meta` provenance
block changed), which is the check that the registry did not quietly alter a
published arm.

---

## 2. The motivating pairs behave — and one of them never mattered

The pairs S1 named, as raw declared values:

| pair | Δ | success v1 → v2 | failure v1 → v2 | reading |
|---|--:|---|---|---|
| `reconnaissance → impact` | +3 | 0.60 → **0.00** | 0.05 → **0.00** | the canonical long jump collapses to exactly zero |
| `reconnaissance → initial-access` | +1 | 1.00 → 1.00 | 0.40 → 0.40 | the adjacent forward step is untouched, as required |
| `initial-access → reconnaissance` | −1 | 0.10 → 0.10 | 0.90 → 0.90 | the failure-side regression bridge survives intact |
| `initial-access → exfiltration` | +2 | 0.60 → 0.15 | 0.02 → 0.005 | a skip: suppressed, not banned |
| `impact → reconnaissance` | −3 | 0.10 → 0.025 | 0.25 → 0.0625 | full-campaign collapse: reduced, still reachable |
| `persistence → lateral-movement` | 0 | 1.00 → 1.00 | 0.35 → 0.70 | a re-classed pair (forward → lateral under the consensus) |

Composed on the real nets, the intended redistribution is visible: in the
`aggregate` profile the adjacent forward step `reconnaissance → initial-access`
takes **45.5% → 76.9%** of the success mass out of reconnaissance, because its
two-stage siblings (`command-and-control`, `lateral-movement`, both at Δ=+2 with
base weights of 0.33) are quartered. The failure-side regression bridge holds its
mass exactly — 75.0% on `pure_steal`, 83.3% on `double_extortion` and
`infrastructure_setup`, 64.3% → 65.0% on `aggregate`.

**But the pair that motivated the ruling never routed any mass.** No profile net
carries a three-stage transition at all. The base-edge census over the five
composed nets, by signed stage offset, is:

| Δ | −3 | −2 | −1 | 0 | +1 | +2 | +3 |
|---|--:|--:|--:|--:|--:|--:|--:|
| edges with base mass | **0** | 12 | 65 | 146 | 84 | 16 | **0** |

`reconnaissance → impact`, `→ exfiltration` and `→ collection` are not edges in
any profile. So the defect S1 named was real **in the declared value table** — a
weight that said a lifecycle-length leap was as likely as an adjacent step — and
was **never exercised by this corpus**. Two consequences, both recorded rather
than smoothed over:

1. The observable effect of the distance term is entirely at Δ=±2, which is `γ`'s
   and `δ`'s work. The floor `z` has nothing to act on (§7.1 measures this
   independently).
2. The correction is nonetheless worth having: it is the *declared layer* that has
   to be defensible against a different corpus, and the overlay is authored
   corpus-agnostically for exactly that reason. What must not be claimed is that
   fixing it changed how this corpus routes.

**One more limit on what the term can do at all.** Composition renormalises
within a source's out-set, so a factor common to every destination cancels.
Distance therefore only moves mass at a place whose out-set spans more than one
distance class: **48 of the 56 multi-out places** across the five nets, with 8
inert — including `pure_steal`'s reconnaissance place, whose only two
destinations are both at Δ=+2, so the profile's entry routing is unchanged by any
value of `γ`.

**The stall check.** Under the distance term a pair can now carry an exact zero,
so a verdict zeroing a whole out-set is *representable* rather than
arithmetically impossible (it was not, before — the previous record's claim of
zero zero-valued cells no longer holds, and
[`runtime_verification.md`](runtime_verification.md) §P7 is updated). Checked
across all 27 parameter combinations of the declared bands × 5 nets × 2
verdicts: **0 stalls**. The guard stays in the composition; it does not fire.

---

## 3. The five recorded caveats, re-examined under the new term

The handoff's instruction was to re-check them rather than assume they survive.
Each is confirmed, resolved, or replaced:

| caveat (R2 wording) | verdict | evidence |
|---|---|---|
| **Failure routes more mass than success to some objective-band destinations** | **confirmed, cause re-diagnosed** | The count falls from 12 to 9 inverted (profile, source, objective-destination) triples, so distance helps but does not fix it. The residual is entirely `execution → collection / impact` and `initial-access → collection`. R2 attributed the inversion to "the flat backward/lateral ladder"; that reading is wrong. The cause is the **flat enablement tier**: the success side concentrates mass on its 1.0 destinations, so a non-enabled destination keeps relatively less success mass than failure mass, where no tier reaches 1.0. Distance is a common factor and cannot alter it — only a graded enablement tier could, and that was tried at R2 and found empirically counterproductive. |
| **`ia_gate` is a soft-floor, not zero (≈13% residual to `execution`)** | **confirmed, and slightly worse in one profile** | The residual is unchanged where the gated destinations are all at one distance (`aggregate` 12.9% → 13.0%), and *rises* where they are not: `pure_impediment` 40.0% → **47.1%**, because the gate's distant destinations shrink faster than its near ones, so renormalisation hands the near one more. This is a direct and previously unrecorded consequence of multiplying the gates by distance, and it is the honest price of doing so. |
| **The C2-hub `privilege-escalation` arm is base-inert in 3/5 profiles** | **confirmed, unchanged** | A base/corpus property. `command-and-control` moves from band 4 to consensus stage 2, which re-classes its out-pairs, but a base weight of zero routes nothing under any overlay value. |
| **Point masses are non-conditionable** | **confirmed, unchanged, and enumerated** | 6 single-out-edge places across the five nets (`pure_steal/resource-development`, `pure_impediment/collection`, `double_extortion/{reconnaissance, resource-development}`, `infrastructure_setup/{reconnaissance, resource-development}`). They renormalise to 1.0 for any value, distance included. |
| **The `enabled = 1.0` tier is flat** | **replaced** | R2 recorded this as an unresolved flatness. Under the consensus ordering it is not a defect to grade: no enabled pair crosses two or more stages (§1.3), so distance *cannot* discriminate within the tier — there is no distance for it to see. The caveat is therefore replaced by a positive statement: the enablement tier is flat because the relations it encodes are all adjacent, which is an independent corroboration of the ordering. What survives is the R2 empirical finding that a hand-graded tier performed worse. |
| **Objective sets are per-profile** | **confirmed, unchanged** | `infrastructure_setup` carries only `collection`; `pure_impediment` carries `collection` and `impact`; the other three carry all of `collection`, `exfiltration`, `impact`. Objective reachability must still be scored per profile. |

One check improved in passing: an enabled destination takes the largest success
share in **46 of 48** multi-out places that have one (was 45 of 48 before the
fold-in), counting only destinations with non-zero base weight. The two
exceptions (`double_extortion/discovery`, `infrastructure_setup/discovery`) are
places where a large base weight on a non-enabled destination outweighs the
enablement tier — a corpus property, not an overlay one.

---

## 4. The sweep design, declared before the numbers

| | |
|---|---|
| **swept** | `γ` over 0.1–0.5, `δ` over 0.25–0.75, `z` over {0, 0.05, 0.1} — the bands declared in `lifecycle_consensus.json`, and **only** these three (§7 of that record fixes the sweep set; a challenge to a rule-resolved stage seat is a re-argument of R-1/R-2, not a sweep dimension) |
| **sampling** | one-at-a-time across each band with the others held at their declared values, then the corners of the most influential *pair*, chosen by the one-at-a-time pass's own influence ranking. A full factorial over three constants is not affordable at this matrix size and is not what identifiability requires |
| **reference arms** | `v1_reference` — the shipped pre-distance values, so the fold-in's own effect is separable from the sweep's; `bands_distance` — the rejected fold-in variant, reported to say whether the relationship-source decision matters behaviourally |
| **mappings** | both registered controller mappings. `v1_ckc_total` is experiment 1's, so the verdict speaks to experiment 1's recorded findings; `v2_partial` is experiment 2's, so the verdict is usable by the experiment that consumes this study. Running both also separates "the weights moved the answer" from "the mapping moved the answer" |
| **matrix** | 13 points × 2 mappings × 5 profiles × {no MTD, random-multi @ 200 s} × 10 seeds = **2 600 runs**, horizon 15 000 s — the same design as experiment 1 so the arms are comparable |
| **not powered for** | the ranking of MTD *mechanisms* under a profiled attacker. That needs the full defence-family sweep, which is experiment 2's. Ten seeds and one scheme is directional, not powered |

The four conclusions tested, each with its criterion fixed in advance:

- **C1** — the two failure modes, and profile deciding which. A profile is
  *friction* if its blocked fraction is at or above 30%, *sink* if the majority of
  its runs terminate at a sink, *churn* otherwise. Holds if every profile keeps
  its mode at every swept point.
- **C2** — the outcome is invariant to MTD. Holds if no swept point produces a
  profile whose objective-reach separates the two MTD conditions.
- **C3** — the ordering of profiles by how far they get. Holds if the ordering is
  preserved. Reported twice: the full rank list, and the *claimable* ordering —
  only those adjacent pairs whose 95% confidence intervals are disjoint, since a
  swap between two profiles the data cannot separate is noise at ten seeds rather
  than a conclusion moving.
- **C4** — attack success rate is zero throughout.

---

## 5. The stability verdict

### C4 — attack success rate: **HELD**

**0 of 2 600 runs** reached the substrate objective, at every parameter point, on
both mappings, under both MTD conditions. Experiment 1's headline is not a
property of where the routing weights sit.

### C2 — invariance of the outcome to MTD: **HELD**, with a finding attached

No swept point makes MTD change whether the profiled attacker reaches the
objective. But on the `v2_partial` mapping a large **host-count** effect appears
that experiment 1's mapping could not show: roughly **4.2 hosts without MTD
against 0.3 with it**, a ~90% suppression, and it is present at *every* swept
point (the largest gap is 5.1 → 0.7 on `aggregate` at `γ = 0.5`). Two things
follow, and only the first is this study's to claim:

1. **The MTD signal that does exist is not an artefact of where the weights
   sit.** It survives the whole sweep, including both corners of the influential
   pair. That is precisely what the stability half of the evaluation's burden
   asks of a declared family.
2. **Whether it is an MTD *result*** is experiment 2's question. It is a
   mapping-driven appearance — under `v1_ckc_total` the profiled attacker barely
   compromised anything, so there was nothing for MTD to suppress — and one
   scheme at ten seeds cannot rank mechanisms. Flagged for experiment 2, not
   claimed here.

### C1 — the two failure modes: **HELD on `v2_partial`, MOVED on `v1_ckc_total`**

On experiment 1's mapping the conclusion moves, on the criterion fixed in
advance. The anatomy matters more than the verdict:

| profile (`v1_ckc_total`, no MTD) | blocked fraction across the sweep | mode |
|---|---|---|
| `pure_steal` | 96.9% – 97.5% | friction, unambiguously, everywhere |
| `aggregate` | 82.3% – 98.0% | friction, unambiguously, everywhere |
| `double_extortion` | 0.0% | sink, everywhere |
| `infrastructure_setup` | 0.0% | churn, everywhere |
| `pure_impediment` | **25.0% – 63.1%** | **crosses the 30% threshold** |

So the *extremes* are rock-stable and the classification of the one
**intermediate** profile is parameter-dependent. That is consistent rather than
surprising: experiment 1 itself recorded `pure_impediment` at 37% blocked and
described it as sitting between the two modes
([`experiment_01_findings.md`](experiment_01_findings.md) §3). The sweep says its
position on that continuum is set by the declared weights, and `δ` moves it
furthest — 25.0% at `δ = 0.75` against 63.1% at `γ = 0.5, δ = 0.25`.

The honest statement of the conclusion is therefore narrower than experiment 1's:
*two distinct failure surfaces exist and profiles at the extremes are assigned to
them robustly; a profile in the middle is not robustly assigned, and the
assignment of the middle case must not be reported as a finding about the
profile.* On `v2_partial` every profile stays put at every point, so the
narrowing is specific to the coarse mapping.

### C3 — the ordering of profiles by how far they get: **MOVED**

| metric | `v1_ckc_total` | `v2_partial` |
|---|---|---|
| deepest lifecycle stage reached | stable — and **degenerate** | stable — and near-degenerate |
| distinct hosts compromised | full ordering UNSTABLE | full ordering UNSTABLE |
| distinct places visited | full ordering UNSTABLE | full ordering UNSTABLE |

The ordering does not survive the sweep, and the reason is not mainly the
weights:

- **The lifecycle-depth measure does not discriminate at all.** Every profile
  reaches consensus stage 3 — the objective band — in the net, on both mappings
  (`double_extortion` on `v2_partial` averages 2.9, the only departure). Its
  ordering is "stable" only because every value is the same. Read positively,
  this corroborates experiment 1's finding 2 from a new angle: the profiles are
  not failing to *traverse* the campaign structure, they traverse it and fail at
  the substrate. Read as a metric, it is saturated and cannot carry the "how far
  they get" claim.
- **The measures that do vary cannot be separated at ten seeds.** At the declared
  point, on four of the six (mapping × metric) combinations, **no adjacent pair
  of profiles has disjoint 95% intervals**. Host counts range over 0.0–5.1 with
  intervals that overlap almost everywhere. The instability is between values the
  data cannot distinguish.

So C3's failure is a **power** finding as much as a weights finding, and it is
actionable: the ordering half of the evaluation's burden cannot be discharged at
ten seeds on either mapping, whatever the weights do. Experiment 2 needs more
seeds for this specific claim, or it needs a discriminating progression metric
that lifecycle depth is not.

### The verdict in one paragraph

The conclusions that survive the declared uncertainty are the ones experiment 1
actually rested on: the profiled attacker reaches the objective in no run at any
parameter point, and MTD does not change that — including the substantial
host-count suppression the new mapping reveals, which is stable across the whole
sweep. The conclusions that move are the finer ones: which failure mode the
*intermediate* profile is in, and any ordering of profiles by how far they get.
The second of those moves for a reason the weights do not control — ten seeds
cannot separate the profiles on the metrics that vary, and the metric that would
have been the right one is saturated. The declared magnitudes are therefore
defensible for the claims the evaluation makes, and are **not** yet defensible
for a per-profile ordering claim, which the evaluation should not make until it
is powered.

---

## 6. What the sweep exposed that was not on anyone's list

### 6.1 The zero floor `z` is behaviourally inert on this corpus

Across `z ∈ {0, 0.05, 0.1}` the sweep measures a **0.0% shift on every
statistic, in every profile, on both mappings**. The reason is structural and was
confirmed independently of the sweep: `z` only ever zeroes Δ=±3 pairs, and no
profile net carries a three-stage transition (§2).

This matters for what may be claimed. The supervisor's ruling was that far jumps
should fall close to, or exactly, zero, and `z` is the parameter that makes
"exactly" representable — both poles of the ruling are in the value table, as
designed. On *this* corpus the choice between them is unobservable, and the
suppression that is observable is `γ`'s at Δ=+2. `z` should be reported as a
declared parameter whose sensitivity is **zero by corpus structure**, not as one
whose sensitivity was tested and found small; a corpus containing a
lifecycle-length edge would make it live immediately.

### 6.2 The influence ranking

| parameter | largest relative shift versus the declared point | where |
|---|--:|---|
| `δ` (backward decay) | **101%** on actions-per-host | `v1_ckc_total` / `aggregate` at `δ = 0.75` (49.5 → 99.5) |
| `γ` (forward decay) | **36%** on actions per run | `v1_ckc_total` / `pure_steal` at `γ = 0.5` (450 → 290) |
| `z` (floor) | **0%** on everything | — |

The backward kernel dominating the forward one is worth noting: the failure side
routes most of the mass in these runs (the profiles fail far more often than they
succeed), so the parameter governing *fallback* distance moves behaviour more
than the parameter governing forward suppression — even though forward
suppression is what S1 was about. The corner set was chosen from this ranking
rather than by preference.

### 6.3 The `deepest_stage` metric is saturated

Recorded in §5's C3 and repeated here because it is a measurement finding, not a
sweep finding: lifecycle depth reached cannot discriminate these profiles,
because all five traverse to the objective band. Any future "how far did it get"
measurement needs to be substrate-side (hosts, breadth) or needs a finer
progression measure than stage index — which is exactly the M8b measurement gap
the APT criterion's axis 1 names
([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d)).

---

## 7. Reported separately: the fold-in's own effect, and the rejected variant

Neither is a stability result. Both are reported because the study's design
separated them out, and because they say things the record needs.

**The fold-in changed behaviour materially, and helpfully, under the mapping that
can act.** On `v2_partial`, `pure_steal` goes from 1.2 to **4.0** mean hosts and
from 67.5 to **193.7** actions per run, and its terminal mode moves off the sink
in 7 of 10 seeds. On `v1_ckc_total` the same change raises `pure_steal`'s action
count from 209.7 to 450.1 while leaving it at zero hosts, and *lowers*
`infrastructure_setup` from 1.7 to 0.9 hosts. Read together: concentrating mass
on near transitions helps a profile that has a usable verb at the near
destination, and merely lengthens the walk for one that does not. That is the
H-coupling story of experiment 1's finding 1, now visible as a weights effect.

**The rejected fold-in variant is materially different**, so the
relationship-source decision is load-bearing rather than cosmetic:
`pure_impediment`'s blocked fraction is 44.9% under the consensus relationship
against **72.9%** under bands-plus-distance (`v1_ckc_total`), and `pure_steal`'s
host count is 4.0 against 3.2 (`v2_partial`). This is reported, not acted on: the
decision was made a priori in §1.1 on coherence and provenance grounds, and a
behavioural difference is not a reason to revisit it. It is a reason the decision
had to be recorded with its reasoning, which is what §1.1 does.

---

## 8. The CTI-independence statement

Required by the handoff's gate 6, and by the boundary the whole declared layer
rests on ([`../../declared_value_provenance.md`](../../declared_value_provenance.md)
§5):

**No value in this fold-in was selected to improve any profile's traversal.** The
kernel family and the three magnitudes were declared by the literature half and
greenlit on 2026-07-27, before any of this study's runs existed; the fold-in
decision in §1.1 was made on coherence and provenance grounds before any net was
walked; the composed-net checks in §2 are semantic validations of pairs named in
advance, not tuning targets; and the only behavioural comparisons that could have
served as a fitting signal — the sweep, the pre-distance arm, the rejected
variant — are reported as outputs, with none of them fed back into a value. The
`bands_distance` arm is the sharpest test of this: it produces different, in
places more suppressive, behaviour, and the decision against it was not revisited
on that evidence.

---

## 9. Where this connects, and when to update

- **Consumes:** [`lifecycle_consensus.md`](lifecycle_consensus.md) (the ordering,
  the kernel, the sweep bands, and the §5 fold-in question this answers);
  [`success_failure_overlay_design.md`](success_failure_overlay_design.md) §1–2
  (the composition rule and the R2 value model, both unchanged);
  [`../../declared_value_provenance.md`](../../declared_value_provenance.md) (the
  three requirements, and the ledger this appends to);
  [`controller_mapping_v2.md`](controller_mapping_v2.md) (the two mappings swept
  against); [`experiment_01_findings.md`](experiment_01_findings.md) (the
  conclusions tested).
- **Feeds:** the experiment-2 handoff — which should name `v2_lifecycle_distance`
  as its overlay version alongside `v2_partial` as its mapping, and which
  inherits three things from §5 and §6: the host-count MTD effect to confirm, the
  seed count the ordering claim needs, and the saturated progression metric to
  replace. Also
  [`../../../notes/ch5_evaluation/evaluation_burden.md`](../../../notes/ch5_evaluation/evaluation_burden.md),
  whose stability half now has its first instalment.
- **Artefacts:** `data/ogasp/controller/outcome_rules.json` (the rules, plus the
  `distance_rule` ledger entry and the `model.relationship` / `model.distance`
  decision blocks); `data/ogasp/controller/overlays/` (the registry and both
  compiled versions); `src/mtdsim/l3_simulation/controller/rules.py` (the
  generator and the reproduction check); provenance row in
  [`../../provenance.md`](../../provenance.md).
- **When to update:** if experiment 2 runs against `v2_lifecycle_distance` (the
  C2 host-count finding is then either confirmed as an MTD result or withdrawn);
  if the ordering claim is re-run at a higher seed count (C3's verdict is then
  re-decided, and its current MOVED verdict is a power statement, not a
  permanent one); if a corpus revision introduces a three-stage edge (`z` stops
  being inert and §6.1 must be re-run); if Marc re-cuts a rule-resolved stage
  seat, or revises the `enables` sets or a rule value (regenerate both versions
  and re-run the reproduction check); and when the rate feasibility study reports,
  since a re-run of this sweep under the stochastic-dwell regime would be the
  natural cross-check on whether the two declared families interact.
