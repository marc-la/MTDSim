---
status: durable
created: 2026-07-29
updated: 2026-08-01
topic: "L3 criterion axis 7 — the within-run learning capability: the declared rule (place-keyed Laplace belief, exponent kappa), the defence-caused forgetting (fraction rho), the CTI-independence argument, the within-run boundary, and the sweep whose conclusions are pre-registered here before any output exists"
---

# The learning capability — an attacker that reweights its own routing from what has worked, and a defence that destroys what it learned

> **Retired class labels.** This record is investigation history and is left as
> written: it reports the pre-2026-08-06 labels `pure_steal` / `pure_impediment` /
> `double_extortion` / `infrastructure_setup`, which the objective-tactic rename
> replaced with `objective_exfiltration` / `objective_impact` /
> `objective_exfiltration_impact` / `objective_none_c2`. Rewriting them would
> re-attribute evidence to labels that did not exist when it was taken. Crosswalk:
> [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

**Status:** durable design-and-build record. The mechanism landed at commit
`e9b5117`: `src/mtdsim/l3_simulation/movement/learning.py` (new), a third
observation wrapper and a modulator fan-out on
[`movement/state.py`](../../../../src/mtdsim/l3_simulation/movement/state.py),
one measure on
[`movement/measures.py`](../../../../src/mtdsim/l3_simulation/movement/measures.py),
wiring in
[`movement/run.py`](../../../../src/mtdsim/l3_simulation/movement/run.py) and
[`trace.py`](../../../../src/mtdsim/l3_simulation/trace.py), the declared values
at `data/ogasp/movement/learning_rules.json`, and
`tests/l3_simulation/test_movement_learning.py` (new). It discharges the axis-7
handoff.

**§6 is a pre-registration.** Its conclusions and their criteria were written and
committed before a single sweep run existed, which is the discipline the two
prior sweeps established and the only thing that makes a stability verdict
falsifiable. §7 records what the sweep found, whichever way it fell.

## 1. Why this axis is worth more than the others

Cho et al.'s first and sharpest under-developed dimension is that attackers are
assumed to follow fixed patterns "rather than that they learn and can launch
adaptive attacks", while defenders are routinely granted learning — an asymmetry
the survey calls contrary to practice (Cho 2020 §V-D). Jalowski's APT "learns
mutation patterns over time" (§4.3). No paper in this project's cross-section
models attacker learning at all, and the field-wide pattern both surveys name is
defender reinforcement learning everywhere and attacker learning nowhere.

The criterion's own fidelity placement turns on it
([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(e)): the model
sits at the **procedural** rung carrying two of the behavioural rung's three
components, and *that rung requires learning this model does not have*. **Axis 7
is the only axis whose demonstration would change the placement claim.** That is
the prize, and it is why the badge decision in §8 is made against a
pre-registered criterion rather than against how the numbers read.

## 2. Why it is also the mitigation, and why that is a methodological argument

Experiment 1's *friction* failure mode is the inherited substrate's rigid
precondition order punishing an attacker that walks CTI tactic-order instead:
`pure_steal` spent 95 % of its action budget on verbs the substrate refused
([`experiment_01_findings.md`](experiment_01_findings.md) §3). The driver
deliberately does **not** re-impose the native order, because doing so would
manufacture the very coupling the evaluation exists to expose.

That leaves a real dilemma, and the two obvious ways out are both bad. Hand-tune
the tactic→verb mapping until it works, and the modeller has fitted the model to
the substrate — exactly what the declared-value guardrails forbid. Report that it
does not work, which is what experiment 1 did, and the finding stands but nothing
is learned about whether the friction is *inherent* or merely *unlearned*.

Learning is a third option and a better one: it converts a modeller-side fitting
problem into a **modelled attacker capability**. An attacker that discovers the
substrate's order by trial and error is doing precisely what Cho asks for, and
the discovery is *the model's*, not the modeller's. This is the strongest
methodological argument available on this axis and it is the reason the mechanism
was built in this shape rather than as a routing patch.

It is also falsifiable, which matters more than it being attractive. If the
blocked fraction falls within runs as the learning capability rises, and is flat
when the capability is switched off, learning works on this terrain. If it does
not, that is a finding about how learnable this terrain is. §6's first conclusion
is written so that either answer is reportable, and §7 reports what happened.

## 3. The rule

### 3.1 What is learned — the destination place, and nothing longer

The unit of credit is the **destination place**, not the transition and not the
verb. The thing that succeeds or fails is the action at a place, so the attacker
learns which tactics pay on this terrain and biases its next move toward them.
Per place `b` the learner keeps within-run counts of the success and failure
verdicts observed at `b` and estimates

```
    Q(b) = (s_b + α) / (s_b + f_b + α + β)          α = β = 1  (Laplace)
```

An unvisited place therefore sits at exactly 0.5 and is never zeroed:
**exploration survives by construction**, rather than by a declared exploration
term that would be a third parameter to defend. It is also why the modulator can
declare `may_zero = False` as a proven claim — `Q` is strictly inside (0, 1)
however lopsided the evidence, so the learner can never remove an out-edge and
can never manufacture a stall.

Two rejections ride with the choice, recorded in the rules artefact so they are
not rediscovered. **Longer credit assignment** — propagating credit backwards
along the trajectory — needs an eligibility trace and a discount factor, which is
reinforcement learning proper: more declared parameters than this timeframe can
defend, and the machinery axis 8 is explicitly deferring. **Learning over
`(place, verb)` pairs** is nearly equivalent under the current mappings, where
several tactics share a verb, and strictly more parameters; it is worth revisiting
only if the place-keyed version is shown to be too coarse. **Learning the
tactic→verb mapping itself** is the most interesting rejected option, because the
mapping is the acknowledged coarse input — but it makes the controller a
runtime-mutable object and breaks the versioned-mapping discipline S4
established.

### 3.2 How strongly it is acted on — the learning capability κ

```
    m(a→b)  =  Q(b) ^ κ
```

composed multiplicatively as the third factor of the seam's rule
(`base · overlay_v · Π_m`), renormalised over the source's out-set. Multiplicative
rather than additive for the reason the overlay design already won: it conditions
the corpus-grounded proportions without inventing a magnitude or inverting the
within-class ordering, where an additive term would need an arbitrary clamp.

At **κ = 0** the modulator returns no factors at all, the product is 1, and the
arithmetic is the pre-existing two-factor rule. This is the ablation arm and the
seam's null guarantee, and it is asserted field for field rather than argued: the
test suite runs all five profiles at five seeds under both MTD conditions and both
mappings and compares the record streams as dataclasses.

### 3.3 What the defence does to it — the forgetting fraction ρ

This is the interesting half. MTD's entire claimed value is destroying what an
attacker has accumulated, and the criterion makes the point twice: an evaluation
whose attacker has no multi-stage knowledge to lose cannot register that value,
and MTD's protection degrades fastest against an attacker that accumulates
knowledge across mutations. So the belief **must** be perishable, and the
perishing must be caused by the defence:

```
    on an MTD interrupt:   s_b, f_b  ←  (1 − ρ) · s_b,  (1 − ρ) · f_b   for all b
```

`ρ = 0` is a learner MTD cannot touch; `ρ = 1` is total amnesia at every
mutation. This is where axis 7 and the thesis's central question meet: the
contest between κ and ρ is the attacker's learning rate against the defender's
mutation rate, which is the same shape as the rate contest the timing work
established the evaluation turns on.

A **per-layer refinement** — a network-layer mutation invalidating position
knowledge, an application-layer one invalidating service knowledge — is more
faithful, and it is named here as the considered alternative rather than silently
passed over. It does not map cleanly onto a belief keyed by tactic-place, which is
what the credit-assignment decision in §3.1 chose; approximating it would put a
host-shaped mechanism inside a tactic-shaped state. The single ρ is taken, and the
refinement is left to a later cycle.

### 3.4 The mechanism the rule needed, and the seam extension it took

The forgetting rule needs a signal the two routing seams cannot carry. By the time
the token routes, an MTD interrupt has become an ordinary failure verdict —
identical, at `compose`, to a verb the substrate refused on an unmet precondition.
A modulator responding to *the defence* rather than to *failure* therefore needs
the one place the two differ.

That place is `AttackOperation.apply_mtd_interrupt_cost`, which every interrupt
path in the driver funnels through exactly once per interrupt (mid-verb,
mid-dwell, mid-blocked-attempt). The seam gains a **third wrapper by the same
idiom as its first two** — `StatefulAttackOperation` reports the interrupt with
the mutating resource's layer and delegates the cost unchanged, consuming the
substrate's penalty and lost-cursor semantics rather than forking them. Only the
driver's view is wrapped; the MTD operation keeps the bare attack operation, so
nothing in the defence's own path reads through a proxy. **The driver is still not
edited.**

Two ordering decisions ride with it, both load-bearing and both recorded in the
rules artefact:

- The interrupt is reported **before** the substrate serves the confusion penalty,
  and therefore before the routing decision that follows. The mutation degrades
  what the attacker knows, and only then does it choose where to go next.
- The interrupted action's **own** failure verdict is recorded *after* the decay,
  so the evidence the attacker just observed survives the mutation that produced
  it. An attacker that forgot the failure it had that instant witnessed would be
  modelling something stranger than amnesia.

`AttackerState` also gains a **modulator fan-out**: a modulator declaring
`observe_visit` / `observe_verdict` / `observe_mtd_interrupt` receives the state's
observations. The learner keeps its own decayed counts rather than mutating the
state's, so the state stays a faithful record of what happened while the learner
holds a belief about it — the record and the belief are different things and are
stored as different things.

## 4. The declared values, and the boundary they must not cross

Both parameters are **declared judgement**: there is no measurement of how fast a
real intruder updates, nor of how much a single mutation costs it. That is the
same tier the durations and the routing weights sit at, and it is handled the same
way — a small rule model, a rules artefact carrying value / tier / rationale /
band argument / scrutiny / changelog, a tracked generator whose `--check`
re-derives the compiled worked view (186 cells, 0 differing), and a sweep over the
declared bands whose verdict is recorded whichever way it falls.

| parameter | declared | band | tier |
|---|--:|---|---|
| κ — learning capability | 1.0 | 0 – 4 | attested-pattern / declared-magnitude |
| ρ — forgetting fraction | 0.5 | 0 – 1 | declared-judgement |
| α = β — the Laplace prior | 1.0 | not swept | declared-judgement |

**The bands are argued from what the parameters mean, never from what produces a
readable number.** κ = 0 is no learning and is the ablation arm; κ = 1 is
proportional-to-belief, the assumption-free reading in which the multiplier *is*
the estimated success probability and no magnitude beyond the estimator is
asserted; κ = 2 is a doubled log-odds response, a plausible over-reaction; κ = 4
is where near-greedy behaviour must show itself — over the belief range this
corpus can produce it separates the best and worst destinations by roughly 1.3 ×
10⁵, so plurality should visibly collapse. A band that did not contain that
collapse could not demonstrate the trade against axis 3 that §6's fourth
conclusion owes. For ρ the band is the parameter's whole meaningful range,
because both endpoints are named positions rather than implausible extremes.

**The tiers differ, and the difference is the honest part.** κ takes the compound
tier because the *behaviour* is attested — Cho names attacker learning as a real
capability that models omit, Jalowski states an APT learns mutation patterns over
time — while the magnitude is declared. ρ takes the floor tier because
Alshamrani's MTD passage attests the *mechanism* (rearrangement "renders the
exploratory knowledge of the attacker useless") but its plain reading sits at the
ρ = 1 pole; the declared 0.5 is a modelling argument that a single mutation is
partial, not something the literature states.

α and β are **not swept**, and that is a decision rather than an omission. They
are a structural property of the estimator, not a magnitude: any α ≠ β asserts a
prior belief about how often tactics pay, which has no source and could only be
set by looking at the substrate — precisely the reverse-engineering the guardrails
forbid. Equal and positive is the only assumption-free choice, and its single
consequence, `Q(unvisited) = 0.5`, is the property §3.1's whole argument depends
on.

### 4.1 The CTI-independence argument, in the form that survives scrutiny

An examiner will say learning tunes the weights to fit the substrate, which is
what the declared-value guardrails forbid. The answer is written down here before
it is needed:

**The authored artefact is the learning rule, not the resulting weights.** The CTI
corpus supplies the prior — the base transition proportions drawn from the
analyst-curated flows. Learning is a declared likelihood update applied at
runtime, and κ = 0 recovers the prior exactly, bit for bit. The weights that
emerge during a run are a consequence of the model's own behaviour, in the same
category as the path the token takes; they are not an authoring act, and no
artefact in the repository stores them.

What *would* violate the boundary is choosing κ or ρ because they raise compromise
breadth or lower the blocked fraction. §6 exists to prove that was not done: the
conclusions and their criteria are committed before any output exists, both
parameters are swept over bands argued from meaning, and the verdict in §7 is
recorded as found.

### 4.2 The within-run boundary, stated rather than quietly crossed

**Nothing survives a run.** Cross-run memory is a different claim — the attacker
that studies the campaign across engagements — and it is already parked as future
work (M8d, and axis 8's beacon primitive, which the 2026-07-28 ruling put out of
scope for the life of the project). Within-run learning matches the APT
single-campaign framing the whole model rests on, and it is what the criterion's
own axis-7 M8b field asks for: *does success probability against a host class rise
with exposure?*

### 4.3 The tempting dead end, named so it is not rediscovered

The substrate contains a commented-out attacker-learning mechanism —
cross-instance vulnerability learning at `mtdnetwork/component/services.py`, the
ATK-04 divergence [`../../metrics_semantics.md`](../../metrics_semantics.md)
documents as unimplemented. It was considered and rejected on three independent
grounds: uncommenting it is a **substrate** change, it would move the 6-phase
baseline and every golden, and it collides squarely with the S2 freeze. It is also
the wrong kind of learning for this axis — a pricing discount, not a decision
capability. It is left alone.

## 5. What the mechanism is verified to do

| gate | evidence |
|---|---|
| κ = 0 is bit-identical to today | 5 profiles × 5 seeds × 2 MTD conditions × 2 mappings, record streams equal field for field (`dataclasses.asdict`), plus `reached_objective` and `termination_time` |
| the ablation is of the *capability*, not the mechanism | the κ = 0 learner still accumulates its belief; it simply never acts on it |
| the capability is live | at the declared values the record stream differs from the ablation arm's |
| exploration survives | an unvisited place is exactly 0.5; 500 consecutive failures leave `Q` strictly positive |
| a `"none"` verdict is silence | a dwell-only place's belief stays at the prior and enters neither count |
| forgetting is caused by the defence | with no MTD running, zero forgettings however long the run; with MTD, the state's interrupt count equals the driver's own record count equals the learner's forgetting count |
| ρ is inert without MTD and live with it | the same seed at ρ = 0 and ρ = 1 gives identical record streams with no defence and different ones with a defence |
| determinism (SIM-05) | the learner draws no randomness at all — burning 500 draws from the state's stream leaves the run identical — and the same seed gives the same walk twice |
| no undeclared zero | a long run at the band's top capability completes, and the state refuses an undeclared zero factor loudly |
| the values reproduce | `--check` re-derives 186 of 186 compiled cells |

Full suite: 474 passed.

## 6. Pre-registration — the conclusions, their criteria, and the sweep design

*Written and committed before any sweep output existed. Nothing below was
adjusted afterwards; §7 reports against these criteria as written.*

### 6.1 The sweep

| | |
|---|---|
| **swept** | κ over its declared band {0, 0.5, 1, 2, 4}, ρ over its declared band {0, 0.25, 0.5, 1}, and **only** these two — α and β are structural (§4) and a challenge to them is a re-argument of the estimator, not a sweep dimension |
| **sampling** | one-at-a-time across each band with the other held at its declared value, then the four non-degenerate corners of the pair. κ = 0 makes ρ inoperative by construction, so the (0, ρ) corners are the ablation arm and are run once |
| **points** | 12: the declared point (1, 0.5); κ ∈ {0, 0.5, 2, 4} at ρ = 0.5; ρ ∈ {0, 0.25, 1} at κ = 1; corners (0.5, 0), (0.5, 1), (4, 0), (4, 1) |
| **mappings** | both registered controller mappings. `v1_ckc_total` is experiment 1's and is where the friction failure mode this axis is the candidate mitigation for actually lives; `v2_partial` is experiment 2's, so the verdict is usable by the experiment that consumes this study |
| **overlay** | `v3_persistent_backward` — the go-forward version after Marc's persistence ruling, and the one experiment 2 will name |
| **matrix** | 12 points × 2 mappings × 5 profiles × {no MTD, random-multi @ 200 s} × 10 seeds = **2 400 runs**, horizon 15 000 s — the same design as experiment 1 and the two prior sweeps, so the arms are comparable |
| **not powered for** | any ordering of profiles by progress. Two independent sweeps have now failed that conclusion at ten seeds; it is not attempted here |

### 6.2 The conclusions, each with its criterion fixed in advance

- **L1 — the learner reduces its own blocked fraction within a run.** *This is
  validation gate 2 and the axis's substantive claim.* Criterion: on the profiles
  whose ablation-arm blocked fraction is at or above 30 % (experiment 1's friction
  threshold), the mean last-quartile blocked fraction at the declared (κ = 1,
  ρ = 0.5) is **lower** than the mean first-quartile blocked fraction, and that
  within-run reduction is **larger than at κ = 0**. HELD if both hold; MOVED
  otherwise. *A learner that does not reduce its own blocked fraction is not
  learning, whatever the routing does, and that verdict is reported rather than
  explained away.*
- **L2 — the effect is monotone in the capability.** Criterion: on the same
  friction profiles, at ρ = 0.5, the run-level blocked fraction is non-increasing
  across κ ∈ {0, 0.5, 1, 2, 4}. HELD if non-increasing at every step; MOVED if any
  step increases. A non-monotone result would say the capability is not acting
  through the mechanism the rule claims.
- **L3 — MTD erases the learner's advantage as ρ rises.** Criterion: at κ = 1 in
  the MTD-on condition, the reduction in blocked fraction relative to the κ = 0 arm
  is non-increasing across ρ ∈ {0, 0.25, 0.5, 1}. Reported together with the
  mechanism check that ρ moves **nothing** in the MTD-off condition, where the
  expected difference is exactly zero rather than small.
- **L4 — learning costs strategic plurality (the axis-3 trade).** Criterion: path
  entropy over the net at the declared κ is **lower** than at κ = 0, and lower
  again at κ = 4. Reported at every κ point whichever way it falls. *If learning
  buys progress at the cost of plurality that is an honest trade and an interesting
  one; discovering it in review would be much worse.*
- **L5 — attack success rate stays zero.** Criterion: no run at any point reaches
  the substrate objective. This is a check that nothing broke, not a claim — the
  operating mutation interval sits inside the degenerate region where ASR cannot
  discriminate anything.
- **L6 — the H-coupling finding survives the ablation.** Criterion: at κ = 0 the
  friction/churn split experiment 1 recorded is reproduced, so the coupling finding
  remains reportable at full strength and any reduction at κ > 0 is attributable to
  *the learner* rather than to the problem having gone away. HELD if the ablation
  arm's per-profile blocked fractions place the same profiles on the same side of
  the 30 % threshold as experiment 1 and the two prior sweeps did.

### 6.3 The badge criterion, fixed before the numbers

Axis 7 is re-scored to **DEMONSTRATED** only if **L1 holds** — the mechanism must
be shown to change an outcome, which on this axis means the attacker measurably
getting better within a run. If L1 moves, the honest badge is **DESIGNED**: the
mechanism exists and has not been shown to change an outcome, exactly as axes 1
and 4 are held today. A DESIGNED badge on this axis is a real result and is
reported as one, because it also fixes the fidelity placement claim in §(e) at the
procedural rung on evidence rather than by omission.

## 7. The sweep verdict

**Reproduce.** Workspace `data/results/axis7_learning/` (gitignored by design —
regenerable), run against commit `876bca2`, the pre-registration commit:

```
PYTHONPATH=src python data/results/axis7_learning/run_sweep.py --workers 6
PYTHONPATH=src python data/results/axis7_learning/analyse.py
```

**The verdict in one paragraph.** The mechanism works, in the precise sense the
axis asked for and in no other. On experiment 1's mapping — the one where the
friction failure mode actually lives — an attacker that reweights its routing from
what has worked drives its own blocked fraction from 91 % to 21 % on the aggregate
profile, and it does so *within runs*, which is the falsifiable form of the claim.
It also does something nobody pre-registered a conclusion about: on the mapping
where the attacker compromises hosts at all, learning **costs breadth badly** —
6.5 hosts down to 0.8 as the capability rises — because the binary verdict it
learns from is not a proxy for progress, and an attacker that maximises success
verdicts learns to stop exploiting. Learning is therefore demonstrated to operate
and demonstrated not to help, which is exactly the position axis 4 has been held
at since experiment 1, and the badge follows that precedent rather than the more
flattering reading (§8).

### 7.1 Per-conclusion verdicts

| | conclusion | verdict |
|---|---|---|
| **L1** | the learner reduces its own blocked fraction *within* a run | **HELD on `v1_ckc_total`, MOVED on `v2_partial`** |
| **L2** | the run-level blocked fraction is non-increasing in κ | **HELD on `v1_ckc_total` (all three friction profiles), MOVED on `v2_partial`** |
| **L3** | MTD erases the advantage as ρ rises | **HELD** for three of four friction profiles; the mechanism check is exact |
| **L4** | learning costs path entropy | **HELD**, on all ten profile × mapping cells without exception |
| **L5** | attack success rate stays zero | **HELD** — 0 of 2 400 runs |
| **L6** | the H-coupling finding survives the ablation | **HELD on `v1_ckc_total`**, the mapping experiment 1 ran |

**One ambiguity in the pre-registration, resolved in the open.** §6.2 said the
criterion applies to profiles whose ablation-arm blocked fraction is at or above
30 %, and did not say in which MTD condition. It is read in the **no-MTD** arm,
because that is the condition experiment 1's own table — the source of the 30 %
threshold — reports. Both readings are printed by the analysis so the choice is
visible: under MTD every profile clears the threshold on both mappings, because a
severed foothold makes the next verb's precondition fail, which is a fact about
the defence rather than about the profile.

### 7.2 L1 — the learning signal, measured

The friction profiles under `v1_ckc_total` are `aggregate`, `pure_impediment` and
`pure_steal`. Blocked fraction over the first against the last quarter of each
run's attempted actions, at the declared (κ = 1, ρ = 0.5) against the ablation
arm, with the 95 % interval on the within-run change:

| profile | arm | Q1 → Q4 | change |
|---|---|---|---|
| `aggregate` | ablation | 97.0 % → 92.9 % | −4.1 % [−0.136, +0.054] |
| `aggregate` | declared | 93.2 % → 69.5 % | **−23.7 %** [−0.391, −0.084] |
| `pure_impediment` | ablation | 89.7 % → 70.4 % | −19.3 % [−0.355, −0.031] |
| `pure_impediment` | declared | 91.4 % → 47.3 % | **−44.1 %** [−0.639, −0.242] |
| `pure_steal` | ablation | 96.5 % → 98.3 % | +1.8 % [+0.009, +0.028] |
| `pure_steal` | declared | 92.2 % → 95.8 % | +3.6 % [−0.005, +0.077] |

Two things in that table matter more than the verdict.

**The ablation arm already improves slightly**, and it is important that it does.
A run's early actions are blocked more often than its late ones even with no
learner at all, because the substrate's state accumulates — a foothold won early
makes later preconditions satisfiable. This is why the criterion was written as a
comparison against the ablation arm rather than as a bare within-run decline: the
bare decline would have "demonstrated" learning in a model with no learning in it.

**`pure_steal` is the counter-case, and it is not noise.** Its blocked fraction
gets slightly *worse* within runs at every capability, its host count is 0.00 at
every point, and its deepest successfully-actioned stage is 0.0 throughout. The
reason is structural rather than parametric: at 97.6 % blocked there is almost no
success anywhere in its net for the belief to steer toward, so the estimator has
nothing to discriminate with. **A belief-based learner needs at least one
destination that pays**, and on that profile's net under that mapping there is
none. That is a finding about how learnable this terrain is for that profile, and
it is precisely the outcome the handoff said to be prepared for.

`v2_partial`'s MOVED verdict rests on **one** profile — `double_extortion`, the
only one clearing 30 % there, and only just, at 36.3 %. Its change is −4.1 %
declared against −7.1 % ablated, with both intervals spanning zero. The
explanation is worth recording and is not an excuse: `v2_partial` makes seven
tactics dwell-only precisely to *remove* the friction this measure tracks, so the
criterion is being applied on a mapping that has almost no friction left to
reduce. It is the same shape as the weight study's finding that the zero floor
was inert because the corpus carried no structure for it to act on — a statement
about where the measurement can speak, not a small measured effect.

### 7.3 L2 — monotone in the capability, where there is friction to remove

Run-level blocked fraction across the κ ladder at ρ = 0.5, no MTD:

| profile (`v1_ckc_total`) | κ=0 | κ=0.5 | κ=1 | κ=2 | κ=4 |
|---|--:|--:|--:|--:|--:|
| `aggregate` | 91.4 % | 74.9 % | 70.3 % | 29.6 % | **21.1 %** |
| `pure_impediment` | 60.1 % | 41.2 % | 36.2 % | 15.5 % | **10.7 %** |
| `pure_steal` | 97.6 % | 95.3 % | 94.1 % | 89.6 % | 80.0 % |

Monotone at every step for all three. The magnitude on `aggregate` is the
headline number of this study: **the friction failure mode is largely
self-correcting, given an attacker allowed to learn.** Experiment 1 recorded that
mode as a property of the coupling between CTI tactic-order and the substrate's
precondition-order; this says a substantial part of it was a property of the
attacker *not being allowed to adapt to* that coupling. The discovery is the
model's — no mapping was hand-tuned, and the κ = 0 arm still reproduces the
original finding at full strength (L6), so the reduction is attributable to the
learner rather than to the problem having been defined away.

`double_extortion` on `v2_partial` is non-monotone (47.5 → 42.7 → 45.7 → 46.3 →
45.5 %), which is what drives L2's MOVED verdict there. It is the same marginal
single-profile cell as L1's, and the movement is inside the run-to-run spread.

### 7.4 L3 — the contest between learning and forgetting

At κ = 1 under MTD, the reduction in blocked fraction relative to the ablation arm,
as the forgetting fraction rises:

| profile | ρ=0 | ρ=0.25 | ρ=0.5 | ρ=1 |
|---|--:|--:|--:|--:|
| `aggregate` (`v1_ckc_total`) | +14.5 % | +5.2 % | +2.0 % | +1.7 % |
| `pure_impediment` (`v1_ckc_total`) | +13.8 % | +4.5 % | +2.5 % | +0.9 % |
| `double_extortion` (`v2_partial`) | +6.0 % | +2.4 % | +1.1 % | +0.7 % |
| `pure_steal` (`v1_ckc_total`) | +3.1 % | +1.9 % | +2.0 % | +0.7 % |

Monotone for the first three; `pure_steal` reverses by 0.1 percentage points
between ρ = 0.25 and ρ = 0.5, which is the MOVED verdict and is inside noise on
the profile that learns nothing anyway.

**This is the axis's most defence-relevant result, and it is a large effect.**
Most of the learner's advantage is gone by ρ = 0.25 — a quarter of the belief lost
per mutation — and by the declared ρ = 0.5 it is down to roughly a seventh of its
unimpeded value. At the operating mutation interval the attacker absorbs about
42 interrupts per run, so even gentle forgetting compounds. MTD is therefore
*extremely* effective against this learner, in a way none of the project's
existing metrics could register, because the thing being destroyed is not a
foothold or a scan result but an estimate.

The mechanism check is exact rather than approximate: with no MTD running, the
four ρ values produce **identical** run-level blocked fractions to twelve decimal
places on all five profiles and both mappings. The forgetting rule is coupled to
the defence and to nothing else. The instrumentation confirms it from the other
side — 41.9 MTD interrupts per run and 41.9 forgettings at ρ = 0.5; 33.7
interrupts and 0 forgettings at ρ = 0.

### 7.5 L4 — the trade against strategic plurality, which is worse than expected

Path entropy over the walk actually taken (bits, pooled over seeds, ρ = 0.5,
no MTD) falls at every step of the κ ladder in **all ten** profile × mapping
cells. On `v1_ckc_total`'s `aggregate` it goes 2.724 → 1.610; on `v2_partial`'s
`infrastructure_setup` it collapses 1.448 → 0.220. The band was chosen wide
enough to contain this collapse, and it contains it.

So the axis-3 trade is real and is reported rather than discovered in review:
**an attacker that learns branches less.** The two axes pull against each other,
and any future claim on either has to name the capability it was measured at.

### 7.6 What the sweep exposed that nobody pre-registered

**The learner optimises its reward and abandons the objective.** This is the
study's most consequential finding and it was not on any list. On `v2_partial`,
where the profiled attacker actually compromises hosts, breadth collapses as the
capability rises:

| profile (`v2_partial`, no MTD) | hosts at κ=0 | κ=1 | κ=4 |
|---|--:|--:|--:|
| `aggregate` | 6.50 | 5.60 | **0.80** |
| `pure_impediment` | 5.20 | 4.10 | **0.30** |
| `infrastructure_setup` | 3.50 | 2.20 | **0.20** |
| `pure_steal` | 3.90 | 4.60 | 3.30 |

Meanwhile the *success count* rises throughout, and the run gets longer (285.7 →
367.1 actions). More effort, more successes, fewer hosts — the effort-to-breadth
conversion that experiment 1's finding 2 measured gets dramatically worse.

The mechanism is unambiguous once the successes are decomposed by verb (aggregate
profile, four seeds, `v2_partial`):

| κ | successes | of which `EXPLOIT_VULN` | reconnaissance-shaped verbs | hosts |
|--:|--:|--:|--:|--:|
| 0 | 815 | 104 (13 %) | 82 % | 6.50 |
| 1 | 1 033 | 48 (5 %) | 92 % | 5.50 |
| 4 | 1 659 | 10 (1 %) | 98 % | 1.50 |

**The learner is correct and that is the problem.** Scanning succeeds far more
often than exploiting does, so a belief keyed on the binary verdict correctly
concludes that reconnaissance pays and exploitation does not — and a
sufficiently confident learner therefore stops attacking. The binary success /
failure verdict was never designed as a progress signal; it is the substrate's
answer to "did this verb return true", and experiment 1's churn failure mode was
already the observation that success verdicts and progress are different things.
Learning does not create that gap. It *finds* it, and then exploits it, which is
what an optimiser does to a misspecified reward.

Three things follow, and only the first is this study's to claim:

1. **A learning attacker cannot be scored on the verdict it learns from.** Any
   future work on this axis has to give the learner a reward with progress in it —
   host compromise, stage advance, breadth — rather than the routing verdict. That
   is not a parameter change; it is a different credit-assignment design, and
   §3.1's rejected alternatives do not cover it.
2. **The κ band's top is not a plausible operating point, and the sweep is why we
   know.** κ = 4 was included to make the plurality collapse visible; it also makes
   the reward misspecification visible. Both were invisible at the declared κ = 1,
   where breadth falls only 6.50 → 5.60.
3. **Whether this generalises beyond this substrate is untested.** The gap between
   verdict and progress is a property of the carved action layer's verb semantics.
   Flagged, not claimed.

**And the MTD host-suppression effect survives the whole sweep.** The ~90 %
suppression the weight study flagged for experiment 2 is present here at 69 % on
the ablation arm (4.32 hosts without MTD against 1.36 with) and holds at every
capability, narrowing to 45 % at κ = 4 only because the no-MTD arm has collapsed
to 1.02 hosts. It is not an artefact of where the learning parameters sit.

### 7.7 The CTI-independence statement

Required by §4.1 and by the guardrail the declared layer rests on. **No value in
this family was selected to improve any outcome.** The rule model, both
magnitudes, both bands and all six conclusions with their criteria were committed
at `876bca2`, before a single sweep run existed; the analysis transcribes those
criteria and does not adjust them; the one ambiguity the pre-registration left
(§7.1) is resolved to the reading that matches experiment 1's own table, with both
readings reported. The sharpest test of the boundary is §7.6: the sweep produced a
result that is *unflattering* to the mechanism — learning costs the evaluation's
headline breadth metric — and no parameter was revisited on that evidence. It is
recorded as the finding.

## 8. The badge, decided against the pre-registered criterion

**Axis 7 moves NOT ADDRESSED → DESIGNED.** Not DEMONSTRATED, and the reasoning is
the pre-registration's rather than a reading of the numbers.

§6.3 fixed the criterion: DEMONSTRATED only if L1 holds; otherwise DESIGNED. L1
held on one mapping and moved on the other, which is not "L1 holds", so the
fallback is taken. It would have been easy to argue the other way — the mechanism
plainly changes outcomes, and a badge that reads "has not been shown to change an
outcome" understates what §7.3 measures — and refusing that argument after seeing
the numbers is the whole point of having written the criterion down first.

The badge is also the right one on the criterion's own internal logic, which
matters more than the arithmetic of the gate. **Axis 4 is held at DESIGNED on
exactly this pattern**: the adaptive loop demonstrably operates and demonstrably
does not yet help, so reacting is on record and adapting is not. Axis 7 now sits
in the same place, with the evidence sharper in both directions: learning
demonstrably operates (blocked fraction falls within runs, monotonically in the
capability, on the mapping where friction exists to remove) and demonstrably does
not help (§7.6 — breadth falls, effort-to-breadth conversion worsens, and no run
at any parameter point reaches the objective). A capability that improves the
attacker's measured friction while reducing its compromise breadth has not been
shown to help the attacker, whatever it has been shown to do.

**What would move it to DEMONSTRATED**, stated so the next cycle does not have to
re-derive it: a learner whose credit signal contains progress rather than the
routing verdict (§7.6, consequence 1), shown to raise breadth or stage advance
against its own ablation arm. That is a credit-assignment redesign, not a
parameter change.

> **Followed up 2026-08-01 — the *other* candidate cause was tested first, and it
> was not sufficient.** §3.1's key was the second suspect: this learner is keyed on
> the destination place, so it holds the marginal success rate and cannot express a
> constraint that depends on state. That key has since been generalised to
> `(destination place, precondition-satisfied?)` and swept over 4 600 runs with
> this learner as a control arm
> ([`learning_readiness_findings.md`](learning_readiness_findings.md);
> the key was chosen against ranked alternatives in
> [`learning_representation.md`](learning_representation.md)).
>
> The representational defect was real — §7.6's breadth collapse is largely an
> artefact of the key, and the finer key recovers it (3.38 → 4.52 hosts at the
> declared point, 1.02 → 2.40 at κ = 4, with exploitation's share of successes back
> from 6 % to 9.5 %). **The badge still did not move**, because the no-learning
> ablation arm sits at 4.60 and the repaired learner does not pass it. So the
> requirement stated above stands unchanged and is now the *sole* one, and one
> caution belongs with it: the two keys are indistinguishable on every
> friction-shaped measure in this record, including §7.2's within-run trend, and
> separate only on breadth.

### 8.1 The fidelity placement — what does and does not move

The placement claim in the criterion's §(e) reads that the model sits at the
procedural rung and is not a behavioural model, because *"that rung requires
learning this model does not have"*. That sentence is now false as written: the
model has learning, it is declared, swept and ablatable, and its effect on
behaviour is measured.

**The placement itself does not move**, and the corrected statement is narrower
and more interesting than either the old one or the flattering one. The
behavioural rung's third component is not "contains a learning mechanism"; it is
an attacker whose accumulated knowledge makes it a better adversary. This model
now has the mechanism and has shown that, on this substrate and with the routing
verdict as its credit signal, the mechanism does not produce that adversary. The
honest form: *the model reaches the procedural rung carrying two of the
behavioural rung's three components and a learning mechanism that has been built,
declared, swept and found not to confer adversarial advantage on this terrain* —
which is a stronger claim about the field's gap than an unqualified absence was,
because it is a measured negative rather than an omission.

## 9. Where this connects, and when to update

- **Builds on:** [`attacker_state_seam.md`](attacker_state_seam.md) — the
  `AttackerState`, the modulator Protocol, the `Π_m` composition and the
  null-equivalence guarantee. This record extends it with a third observation
  wrapper and the modulator fan-out (§3.4).
- **Consumes:** [`measurement_suite.md`](measurement_suite.md) (path entropy and
  the interval helper; the within-run trend is added to it here),
  [`experiment_01_findings.md`](experiment_01_findings.md) §3 (the friction failure
  mode this is the candidate mitigation for),
  [`weight_sensitivity_study.md`](weight_sensitivity_study.md) §4 (the
  sweep-reporting shape copied here),
  [`../../declared_value_provenance.md`](../../declared_value_provenance.md) §1
  and §5 (the three requirements and the guardrails).
- **Artefacts:** `data/ogasp/movement/learning_rules.json` (the rules and the
  ledger), `data/ogasp/movement/learning_factors.json` (the compiled worked view),
  `src/mtdsim/l3_simulation/movement/learning.py` (the modulator and the
  generator).
- **When to update:** if experiment 2 runs a learning arm (the sweep's verdict is
  then either confirmed at scale or qualified); if the per-layer forgetting
  refinement in §3.3 is taken up; if the S2 governance question the seam record
  §7 raises is resolved either way; and if a corpus or mapping revision changes
  which places are dwell-only, since the `"none"`-is-silence decision in §3.1 has
  no effect where every place is action-bearing.
