---
status: durable
created: 2026-08-02
updated: 2026-08-02
topic: "L3 criterion axis 7 — the progress credit rule: the achievement terms added to the declared relation, the state-change credit arm built beside the shipped acceptance one, the declared-bias control the axis never had, and the pre-sweep demonstration that the belief's rank correlation with progress inverts from −0.266 to +0.778"
---

# Progress credit — crediting what an action achieved rather than that it was permitted

**Status:** durable build record. It reports what was built and what the mechanism
does to the belief. **It makes no outcome claim, moves no badge, and runs no
comparative experiment** — the sweep that asks whether this helps is
pre-registered separately, after this record, on the discipline the iterated cost
model set.

The defect it repairs was measured, not argued
([`learning_mechanism_feasibility.md`](learning_mechanism_feasibility.md) §8b):
the shipped learner's preference tracks whether an action was **permitted** at
rank correlation +0.921 and whether it **advanced the attacker** at −0.027. It
rates a tactic whose progress rate is 0.0000 at Q = 0.992 and one whose progress
rate is 0.448 at Q = 0.302. The learner is not badly tuned — it is succeeding at
the objective it was given, and the objective is wrong.

## 1. What was built

Three changes, no new mechanism. Every one is an edit to the existing modulator or
to a declared artefact; the key, the Laplace estimator, the multiplicative
composition and the κ = 0 null-equivalence are untouched.

### 1.1 Achievement terms in the declared relation (`v1_substrate` → `v2_achievement`)

The relation modelled **preconditions but not achievements**: `EXPLOIT_VULN` and
`BRUTE_FORCE` produced no capability, so the attacker's own knowledge model could
not represent *I accomplished something* and no progress notion defined over the
capability closure could reward attack at all (§4.1 horn 3 of the study). Both
attack verbs now produce `foothold` — established access on the current host —
cleared by `ENUM_HOST` (the cursor has moved to a different host) and by a
network-layer mutation, which severs it exactly as it severs `curr_host` and
`curr_ports`. Transcribed from the `_do_*` cores on the same basis as every other
entry: these are the two verbs whose success is a compromise event in
`movement/statistics.py`.

**Verified inert on everything already measured.** `foothold` is produced-only —
no verb requires it — so it cannot change a readiness verdict or an enabling cost.
Checked exhaustively rather than argued: **0 disagreements** on
`PreconditionModel.is_ready` across all held-subsets × verbs, and **0** on
`CapabilityCostModel.enabling_cost` on both mappings. The readiness bit's measured
prediction accuracy (1.0000 on `v1_ckc_total`, 0.9169–0.9428 on `v2_partial`) and
axis 6's recorded cost model therefore carry over **by construction**, not by
re-measurement.

A third `known_optimisms` entry travels with it, on the artefact's own precedent:
`foothold` is modelled as produced whenever the verb runs ready, but the
substrate's compromise is conditional on `check_compromised()`, so the declared
bit over-predicts achievement in the same bounded direction as the two existing
optimisms. Sensitivity to that is a validation gate, not an assumption.

### 1.2 The credit rule, as a selectable arm

`ReadinessLearningModulator` gains `credit ∈ {ACCEPTANCE, PROGRESS}`, defaulting
to `ACCEPTANCE` — **the shipped rule stays the default so every figure on record
reproduces**, the arm-selector idiom
[`iterated_cost_model.md`](iterated_cost_model.md) established for exactly this
reason.

Under `PROGRESS`, `observe_verdict` applies the capability effect **first**, then
credits on whether the phase-state moved:

- a permitted action that moved the phase-state scores a **success**;
- a permitted action that left the phase-state exactly as it found it scores a
  **failure** — this is the whole content of the change;
- a blocked attempt keeps landing in the `(place, not-ready)` cell, deliberately
  unchanged, because §8b measured that component's cost to expected progress at
  between 0.0 % and +1.8 %: suppressing attempts that would fail is free and
  correct.

The signal is contemporaneous and one-step. No eligibility trace, no horizon, no
discount, no value function — the no-RL constraint holds without argument, and by
the study's Gate 0 this is credit class (a).

**A clearing action counts as movement, and the reason is load-bearing rather
than a convenience.** `ENUM_HOST` drops the foothold and the port knowledge
because the cursor has moved to a different host. Under a strict *grew* test that
scores as no progress, the attacker would learn never to pivot and the campaign
would close after a single host. Counting any change as movement is also
self-limiting: an immediate second `ENUM_HOST` has nothing left to clear and
earns nothing.

What the rule does mechanically is why no new mechanism was needed. Scanning while
its capability is already held changes nothing and earns nothing, which retires
the reconnaissance-farming loop. Re-attacking a host already footholded changes
nothing and earns nothing, which is the **churn** failure mode — the half of the
model no block-driven mechanism reaches
([`experiment_01_findings.md`](experiment_01_findings.md) §3). And because a verb
pays only while it is still advancing the attacker, **the substrate's procedural
order stops having to be injected and becomes something the attacker discovers.**

### 1.3 The declared-bias control the axis never had

`DeclaredReadinessBias` subclasses the learner and overrides `q()` to return two
declared constants — `q_ready` when the destination's precondition is satisfied,
`q_unready` when it is not. Identical readiness tracking, identical severance,
identical exponent and composition; the inherited counts still accumulate and are
still logged, but they never reach a routing decision. Learner and control
therefore differ in **exactly one respect**: whether accumulated evidence moves
the factor.

It is criterion C3 of the study — *is this learning, or a lookup with extra
steps?* The readiness bit is a declared function of the trajectory with 1.0000
accuracy on `v1_ckc_total`, and an unmet precondition is a deterministic failure,
so a belief keyed on that bit converges toward a deterministic function of a
variable the mechanism already computes for free. The two rates are **constructor
arguments, not declared values** — this module declares nothing, and a sweep owns
the choice.

**It is a control arm and must never ship in a reported configuration.**

## 2. The mechanism does what it was designed to do — shown before the sweep

Precedent: `iterated_cost_model.md` §1.1. This reports the **belief**, which is
what the change is aimed at, and not any badge-bearing outcome measure.

`infrastructure_setup`, `v2_partial`, 6 seeds, horizon 15 000, κ = 1.0, ρ = 0.5.
`Q_ready` is the learner's end-of-run belief; `accept` and `progress` are ground
truth from the record stream (verdict success rate, and `COMPROMISE_EVENTS` per
attempt).

| | place | Q_ready | accept | progress | n |
|---|---|--:|--:|--:|--:|
| **acceptance** | command-and-control | **0.993** | 1.000 | **0.0000** | 803 |
| | lateral-movement | 0.988 | 1.000 | 0.0000 | 513 |
| | discovery | 0.988 | 1.000 | 0.1266 | 474 |
| | reconnaissance | 0.975 | 1.000 | 0.0000 | 227 |
| | privilege-escalation | 0.591 | 0.614 | 0.6136 | 44 |
| | **execution** | **0.503** | 0.527 | **0.5273** | 110 |
| | credential-access | 0.074 | 0.014 | 0.0143 | 70 |
| | initial-access | 0.028 | 0.000 | 0.0000 | 34 |
| **progress** | discovery | **0.828** | 1.000 | 0.0414 | 290 |
| | **execution** | **0.336** | 0.762 | **0.7623** | 122 |
| | lateral-movement | 0.138 | 1.000 | 0.0000 | 452 |
| | reconnaissance | 0.088 | 1.000 | 0.0000 | 111 |
| | credential-access | 0.026 | 0.000 | 0.0000 | 219 |
| | command-and-control | **0.025** | 1.000 | 0.0000 | 233 |

| credit rule | rank corr Q vs **acceptance** | rank corr Q vs **progress** |
|---|--:|--:|
| acceptance (shipped) | **+0.939** | **−0.266** |
| progress (built here) | +0.101 | **+0.778** |

**The sign inverts.** Under the shipped rule the belief is an almost perfect
ranking of what the substrate permits and is *negatively* related to what
advances the attacker; under the new rule that relationship reverses. The single
clearest row is `command-and-control`: acceptance 1.000, progress 0.0000, and its
belief falls from 0.993 to 0.025.

The ordering the new rule produces is the enabling chain — `discovery`
(SCAN_PORT, which re-establishes the port knowledge each pivot costs) above
`execution` (EXPLOIT_VULN), and both far above the tactics that are always
permitted and never achieve anything.

**This is a demonstration on 6 seeds, and it is a statement about the belief
only.** It is not evidence that the attacker performs better, and it must not be
read as any part of a badge argument.

## 3. Three things to watch, recorded now so they are not discovered later

1. **`Q` is a stricter progress measure than the proxy it is scored against.**
   `COMPROMISE_EVENTS` counts re-compromising a host already owned; the credit
   rule does not. So the +0.778 is measured against a proxy that mildly disagrees
   with the rule — in the direction that *understates* it. `execution` shows this
   directly: realised progress 0.7623 against a belief of 0.336.
2. **The pivot sits low.** `lateral-movement` (ENUM_HOST) holds 0.138. It earns
   only when it has something to clear, and is charged when inert. If a sweep
   shows the campaign closing after one host, this is the first place to look —
   suppressing the pivot would defeat the rule's own purpose.
3. **Mass has to go somewhere.** `credential-access` attempts rose 70 → 219
   despite a belief of 0.026 and an acceptance rate of 0.000. Downweighting the
   always-permitted-never-achieving tactics redistributes effort, and not all of
   it lands productively. Worth reporting in the sweep rather than only the
   headline.

## 4. Verification

- **169 tests passed at the time of the build** across
  `test_movement_learning_readiness.py`, `test_movement_utility_iterated.py`,
  `test_movement_state.py` and `test_movement_learning.py` — the four suites that
  then read the amended artefact or the amended modulator.

  > **Amended on merge to `dev`, 2026-08-02.** The second of those suites no
  > longer exists: axis 6 closed as DESIGNED and the iterated utility modulator
  > was deleted with it ([`iterated_cost_model.md`](iterated_cost_model.md) §0),
  > so the amended artefact now has three consumers rather than four. **The
  > verification below is unaffected**, and the reason is this record's own
  > inertness result — `foothold` is produced-only, so `enabling_cost` was
  > unchanged, which is exactly why the deleted modulator's recorded sweep stays a
  > valid record of the model it ran under. The count is left as it was measured
  > rather than restated, because restating it would imply a re-run that did not
  > happen.
- The 23 pre-existing readiness tests passed against the amended relation
  **before** any new test was written, which is the regression check that matters.
- New tests pin: acceptance credit is **bit-identical across all five profiles**
  after the reorder; κ = 0 stays bit-identical under either rule; an action that
  changes nothing earns no credit; re-attacking a footholded host earns nothing;
  pivoting is movement and re-opens the foothold; a blocked attempt still lands in
  the not-ready cell; `may_zero = False` survives 200 inert successes at κ = 4;
  and the control's counts provably never reach a routing decision.

## 5. What this licenses, and what it does not

**Licensed.** That the mechanism exists, is ablatable, declares no new magnitude,
and stays inside the no-RL constraint. That the achievement terms are inert on
every recorded measurement. That the belief's relationship to progress inverts
(§2) — a statement about the belief on 6 seeds.

**Not licensed.** No badge move. No claim that the attacker performs better, is
more breadth-productive, or absorbs MTD differently — none of that was measured
here. No re-reading of the readiness sweep or any recorded experiment. No
composition with axis 6's factor 7A/AB until the joint check in
[`modulator_composition.md`](modulator_composition.md) §2 has run — the bar is
unchanged and this build does not touch it. And **no reported configuration
change**: the headline arm still runs modulators null, and `ACCEPTANCE` remains
the modulator's default.

## 5b. The sweep has since run — all five conclusions not confirmed (2026-08-02)

[`progress_credit_findings.md`](progress_credit_findings.md), 7 000 runs. The
badge stays DESIGNED (U1, as predicted). The credit repair favours progress in 8
of 10 cells and does not separate on the decision cell (U2). The mechanism is not
distinguishable from an aggression-matched declared bias on `v2_partial` (U3),
which is now the axis's live problem. **§3's watch item 2 fired exactly as
flagged** — the pivot is suppressed and `infrastructure_setup` is the one profile
the mechanism harms (3.40 -> 2.02). And the type-discipline prediction was
**refuted with separation in the opposite direction**: forgetting helps.

One large separated effect exists and sits outside the gated cell: on
`v1_ckc_total` with no MTD the mechanism reaches 1.70 +/- 0.29 against an ablation
of 0.44 +/- 0.08. It is a lead requiring its own pre-registration, not a result.

## 6. What comes next, in order

~~1. Rule on the forgetting question.~~ **Answered by measurement, not by ruling:
   U5 refuted ρ = 0 with CI separation on the decision cell. Do not adopt it.**
~~2. Settle the seed count.~~ **Done — the sweep ran 50 seeds from the power
   calculation, and adjacent arms still did not separate on `v2_partial`.**
~~3. Pre-register, then sweep.~~ **Done** ([`progress_credit_prereg.md`](progress_credit_prereg.md),
   [`progress_credit_findings.md`](progress_credit_findings.md)).

The successor list is now §6 of the findings record. Its first item is the one
that matters: pre-register `v1_ckc_total` as the decision cell and test whether
the effect scales with the mapping's blocked fraction.

## 7. Where this connects

- **Builds on:** [`learning_mechanism_feasibility.md`](learning_mechanism_feasibility.md)
  (the rubric, the measured defect, and the ruling that no new mechanism is
  needed), [`learning_representation.md`](learning_representation.md) (the key
  this keeps unchanged), [`learning_capability.md`](learning_capability.md).
- **Registers:** a change to factor 4's credit rule and to factor 6's artefact —
  [`modulator_composition.md`](modulator_composition.md) owes a row revision in
  the same commit family.
- **Code:** `src/mtdsim/l3_simulation/movement/learning_readiness.py`,
  `data/ogasp/controller/precondition_relation.json`,
  `tests/l3_simulation/test_movement_learning_readiness.py`,
  `data/results/progress_credit/show_mechanism.py` (untracked/regenerable, per the
  experiment-workspace convention — §2's table is the tracked record of its output).
- **When to update:** when the forgetting ruling lands; when the pre-registered
  sweep reports; and if any of §3's three watch items fires.
