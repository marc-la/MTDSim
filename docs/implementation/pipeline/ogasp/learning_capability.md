---
status: durable
created: 2026-07-29
topic: "L3 criterion axis 7 — the within-run learning capability: the declared rule (place-keyed Laplace belief, exponent kappa), the defence-caused forgetting (fraction rho), the CTI-independence argument, the within-run boundary, and the sweep whose conclusions are pre-registered here before any output exists"
---

# The learning capability — an attacker that reweights its own routing from what has worked, and a defence that destroys what it learned

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

*(To be completed by the run. Nothing is written here until the runs exist.)*

## 8. Where this connects, and when to update

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
