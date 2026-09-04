---
status: durable
created: 2026-08-02
updated: 2026-08-02
topic: "L3 criterion axis 7 — a feasibility study over thirteen candidate learning mechanisms: the first-principles rubric they are scored against, the four structural facts that kill most of them outright, the measured lead already sitting in the readiness sweep, and the recommended stacked MVP"
---

# The learning-capability feasibility study — what the mechanism has to be, and which candidates can be it

> **Retired class labels.** This record is investigation history and is left as
> written: it reports the pre-2026-08-06 labels `pure_steal` / `pure_impediment` /
> `double_extortion` / `infrastructure_setup`, which the objective-tactic rename
> replaced with `objective_exfiltration` / `objective_impact` /
> `objective_exfiltration_impact` / `objective_none_c2`. Rewriting them would
> re-attribute evidence to labels that did not exist when it was taken. Crosswalk:
> [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

**Status:** durable investigation record. It builds nothing, moves no badge, declares
no value and re-reads no committed experiment. It exists because axis 7's scope is
open ([`model_scope_freeze.md`](model_scope_freeze.md) §0) and the decision about what
to build next has been taken twice on incomplete grounds — once when the chain
proposal was rejected against the wrong question, and once when the credit signal was
classed a research project without anyone checking what the signal costs to obtain.

It is written against the project's single research question — *what does greater
attacker fidelity imply for current evaluation methods of MTD* — and the scoring
reflects that. **A mechanism is good here if it makes MTD's own effect more legible,
not if it makes the attacker win more.** That distinction is derived in §3 and it
reorders the candidates substantially.

## 1. What was asked for across the week, and what shipped

The axis has been steered continuously since 2026-07-28. Eleven distinct concerns are
identifiable in the session record; four were addressed, seven were not, and the seven
share a shape.

**Addressed.** Learning as runtime weight updates from prior success and failure
(both learners); MTD-driven forgetting (the ρ rule); a scalar capability input (κ, with
κ = 0 as the bit-identical ablation); and the no-RL constraint, honoured throughout.

**Not addressed, and the omissions rhyme.** The attacker still does not beat its own
ablation arm in the pre-registered cell. Chain and workflow memory — proposed
repeatedly from 2026-07-29 onward as *the* remedy for procedural ordering — was never
evaluated as a workflow claim. Direct next-phase injection was designed and then
dissolved into the readiness bit, so the diagnostic half shipped and the directive half
did not. The generality ask ("adapt to the substrate's shape at runtime") was answered
with a hand-transcribed substrate model, which is a porting surface but not an adaptive
one. The unification ask was refused on portability grounds
([`modulator_composition.md`](modulator_composition.md) §3) — defensibly, but the
"fractured" complaint stands, since composing the learner with the repaired cost model
is currently *barred* pending a joint check. The failed-early-but-critical-later case
was partly retired by the readiness key (§6, C4) and never addressed as a positive
pull. And the non-action-only scope question was never evaluated at all.

**Nine of the eleven concerns are about *sequence*.** What shipped is a
state-conditioned *marginal*: it knows whether it is ready, never what makes it ready,
and never what worked before. That gap is not named in any current record — the
project's own account of the remaining work names the *reward*
([`learning_without_context.md`](../../../notes/ch7_discussion/learning_without_context.md))
and treats the representation half as discharged. It is discharged only for the
narrower reading of "representation" as *situation*; as *sequence* it is untouched.

## 2. The diagnosis has three parts, not two, and the model has two failure modes

### 2.1 Three defects, one repaired

1. **Regime conflation** — the marginal mixed a paying regime with a certain-failure
   one. **Repaired** by the readiness key. This was never the defect the steering named.
2. **Misspecified credit** — the signal is *was this action accepted*; the objective is
   *did this action advance me*. **Open**, and named as the sole remaining requirement.
3. **No representation of sequence** — nothing in the model holds ordering knowledge.
   **Open, and unnamed anywhere.**

### 2.2 Two failure modes, and a mechanism keyed on blocking only reaches one

[`experiment_01_findings.md`](experiment_01_findings.md) §3 records that the profiled
attacker fails in two distinct ways and that the profile decides which:

- **Friction.** `pure_steal` (95 % of actions blocked) and `aggregate` (76 %) spend
  their budget on verbs the substrate refuses.
- **Churn.** `infrastructure_setup` and `double_extortion` are blocked **0 %** of the
  time and still fail — 931 host-compromise events over 10 runs landing on 22 distinct
  hosts, the same few re-compromised ~40 times each.

**This is load-bearing for the whole catalogue.** On a churn profile the attacker is
always ready, so the readiness bit is constant and the learner is inert by
construction; and every candidate whose signal is *the block* is equally inert there.
Churn is precisely "accepted but not advancing", which only a progress-carrying signal
can see. Any mechanism proposed as *the* axis-7 answer must state which failure mode it
addresses, and a block-driven mechanism alone addresses half the model.

## 3. First principles — the instrument derivation

### 3.1 What an operator learns, and which part this axis owns

The literature separates three objects, and the separation is sharper in the sources
than in this project's records.

- **(a) Target-specific facts** — which hosts exist, which ports are open. Alshamrani
  names exactly this as MTD's target: rearranging components *renders the exploratory
  knowledge of the attacker useless*. Short half-life **by definition** — MTD is the
  thing that destroys it.
- **(b) Tradecraft** — which procedures work on terrain of this kind. Hutchins: APT
  actors *attempt intrusion after intrusion, adjusting their operations based on the
  success or failure of each attempt*. Bianco's apex: responding at TTP level forces the
  adversary to *learn new behaviours*. Long half-life. **MTD cannot touch it** — that is
  the entire content of the pyramid-of-pain argument the lit review already uses.
- **(c) The defence's own pattern** — Cho's and Jalowski's "learn mutation patterns".
  This is axis 8, ruled out of scope.

Two consequences follow, and both are uncomfortable.

**The axis's own cited anchors are mostly (c).** Both headline sentences the criterion
doc quotes for axis 7 describe capability the project has excluded. The in-scope
residue of Cho is the second half of the same section — *an attacker has been less
considered as a rational decision maker with learning ability … attackers with learning
capability and their mental models have been rarely studied* — plus Cho's own metric
definition, learning measured *toward the payoff*. Ferguson-Walter supplies the
operational content: operators form mental models from personal experience, and
notably *repeatedly retry a failed exploit attempt, often blaming themselves or their
tools*. Bromiley/SANS quantifies the skill this axis is really about: only **38 %** of
professional operators can pivot to a new method more than half the time when the first
vector is blocked, and pivot ability rises with experience.

**The forgetting fraction is applied to the wrong object.** The shipped modulator holds
two things. `held`, the capability cursor, is a type-(a) object and is handled
correctly — `mtd_clears` severs `curr_host` and `curr_ports` on a network mutation,
which is Alshamrani's mechanism exactly. `Q(b, ready?)`, a per-tactic success rate, is a
type-(b) object: a statement about which procedures pay on terrain of this kind. The ρ
rule decays it on **every** interrupt. The module docstring states the intent plainly —
*"the belief is what the attacker knows, the phase-state is what it currently holds, and
MTD takes both"* — and the literature says MTD takes the first and cannot take the
second.

One consequence rides with that and should be flagged rather than asserted: the axis's
recorded result that *MTD is severely effective against this learner* is currently a
consequence of a modelling declaration, not a measured property of MTD. What MTD
destroys in this model is tradecraft, because the model declared tradecraft perishable.

### 3.2 The instrument property — the derivation that reorders everything

MTD's protective claim is a claim about knowledge invalidation. For an evaluation to
test that claim, four things must hold together: the attacker holds knowledge; the
knowledge is *consequential*; mutation degrades it; and the degradation shows up in a
**progress-shaped** measure. The fourth is not optional and the project has paid for it
twice — the blocked-fraction trend moved −0.474 for the readiness learner against
−0.476 for the destination-only one, indistinguishable to three decimals, while breadth
differed by 34 %. A friction measure registers the attacker's comfort, not the defence's
effect.

From those four, the instrument property follows, and it is an **interaction, not a main
effect**:

> A learning mechanism is a good instrument for MTD evaluation to the degree that it
> changes **MTD's measured effect**, not to the degree that it changes the attacker's
> performance.

With `P` a progress measure:

```
I  =  [P(MTD off, mech) − P(MTD on, mech)]  −  [P(MTD off, abl) − P(MTD on, abl)]
```

**This inverts the current gate**, which scores `P(mech) − P(abl)` at a fixed MTD
condition — the attacker's main effect. The instrument quantity is the cross term, and
it has never been reported as a gate.

The quantity is computable from figures already on record. On `v2_partial`, breadth:

| arm | no MTD | MTD @200 s | MTD's measured effect | retained |
|---|--:|--:|--:|--:|
| ablation | 4.60 ± 0.73 | 1.42 ± 0.36 | −3.18 | 30.9 % |
| readiness learner | 4.52 ± 0.70 | 1.70 ± 0.48 | −2.82 | 37.6 % |

MTD's measured effect is **smaller** against the learning attacker. Neither difference
is CI-separated at ten seeds, so the sign is not established, and this is raised as a
quantity to pre-register — **not** as a re-grading of committed numbers.

**Note what a robust reading would mean.** If a faithful learning attacker genuinely
absorbs MTD better than a memoryless one, that is not a disappointment; it is the thesis
result in its strongest form — *greater attacker fidelity implies current MTD
evaluations overstate MTD's benefit*. Which is why the rubric below demands a
**declared and tested sign**, never a particular sign.

**Preference ordering, stated bluntly.** A mechanism that raises breadth 30 % and is
invariant to mutation is worthless here — a better attacker and an inert instrument. A
mechanism that raises breadth 5 % and loses half of that gain to mutation is the better
instrument, because the loss *is* the MTD effect made measurable. A candidate that
argues for itself primarily on attacker performance is arguing on the wrong axis.

### 3.3 Learning versus state-conditioning, and the control that settles it

The charge against the shipped mechanism is nearly provable. An unmet precondition is a
*deterministic* failure (0.000 over 14 000+ observations), so `Q(b, not-ready)`
converges to `1/(f+2)` for every `b` alike, while `Q(b, ready)` converges to each `b`'s
ready-regime rate. Asymptotically the learner computes `ready?(b) ? q_b : ≈0` — and
`ready?(b)` is a **declared** function of the trajectory whose accuracy against ground
truth is **1.0000 over 12 281 dispatches** on `v1_ckc_total`. A quantity converging to a
deterministic function of a variable the mechanism already computes for free is a lookup
with extra steps. The only learned residue is the ordering of the ready-regime rates,
and that residue has never been isolated.

**The criterion.** A mechanism is *learning* rather than *state-conditioning* if,
holding its declared inputs fixed, its behaviour differs from the best policy
constructible from those declared inputs alone, in a direction determined by the run's
outcomes.

**The test.** A **declared-bias control arm**: the static modulator applying the
mechanism's declared structure with no accumulation — for the shipped learner,
`f(b) = (ready?(b) ? q_hi : q_lo)^κ` with `q_hi, q_lo` declared constants. Compare on
breadth *and* on the realised transition distribution (`jsd` and
`path_entropy_from_transitions` already exist and `transitions` is already tallied per
run). Indistinguishable means the counts are decoration. It is cheap, it is a *control*
rather than a metric so it is S6-clean, and it has never been run.

## 4. Four structural facts that constrain every candidate

Verified against the working tree; each kills or reshapes at least one candidate.

### 4.1 The credit trilemma — all three obvious progress signals are structurally dead

1. **Credit at the profile's declared objective place.** Objective tactics are declared
   per class in `petri/analysis.py`. Under `v2_partial`, `exfiltration`, `impact` and
   `collection` are all **dwell-only** — no verb, no verdict, the trigger can never fire.
   Under `v1_ckc_total` all of them fall back onto **`SCAN_NEIGHBOR`**, so the trigger
   fires on a scan. *The attacker's ends live precisely where the substrate is empty.*
2. **Credit on substrate progress (breadth).** Circular — it optimises the attacker on
   the metric that scores it.
3. **Credit on the declared capability closure.** The closure is
   `{host_stack, curr_host, curr_ports}`, and **`EXPLOIT_VULN` and `BRUTE_FORCE` produce
   nothing**. A progress notion over the declared closure is structurally incapable of
   rewarding attack and would reproduce the pathology in a purer form.

**The relation models preconditions but not achievements.** That is the single sharpest
finding in this study: the attacker's own knowledge model cannot represent *I
accomplished something*.

Two escapes, both declared-artefact work rather than machinery:

- **Escape A — extend the relation with achievement terms.** Give `EXPLOIT_VULN` a
  produced capability (a foothold), cleared by `ENUM_HOST` and by network `mtd_clears`,
  derived from `_do_*` exactly as the existing entries were. Progress becomes
  *attacker-believed* progress, wholly in-layer, and its accuracy against actual
  compromise becomes a measurable validation gate on the precedent of the readiness
  bit's 92–100 %.
- **Escape B — stop discarding the signal that already exists.** The driver computes
  `outcome_tag` and `verdict` at the same instant and records both in `MovementRecord`.
  The compromise definition is already a `(verb, outcome)` set in `statistics.py`, and
  it discriminates *within* a verb — `("SCAN_PORT", "TRUE")` is a compromise while an
  ordinary port scan is not. That is the acceptance/advancement separation, already
  computed. But the modulator channel is `observe_verdict(place, verdict)` with
  `verdict ∈ {success, failure, none}`, so **the outcome tag is projected to a bit one
  function call before any learner can see it.** The progress signal is not missing; it
  is being thrown away in the seam. "A research project in itself" describes what to
  *do* with the signal, not what it costs to *obtain* it — the obtaining is ~12 lines.

### 4.2 The capability graph is a total chain of depth three

Six verbs, three capabilities. Only **4 of 8** capability states are reachable from ∅,
and they form a total chain:

```
∅ ──SCAN_HOST──▶ {host_stack} ──ENUM_HOST──▶ {host_stack,curr_host} ──SCAN_PORT──▶ {all three}
```

Unit-cost hops-to-ready for `EXPLOIT_VULN` is therefore **3 / 2 / 1 / 0** by level. A
network mutation drops the full state back to `{host_stack}`, i.e. distance 2; an
application mutation changes nothing.

**Consequence:** "distance to ready" is an integer in `{0,1,2,3}` — a four-valued strict
generalisation of today's one bit, over the *same* artefact, with **no new declared
magnitude**. `CapabilityCostModel.enabling_cost` already computes it if built with an
empty cost table and `cost_floor_s = 1.0`, which prices every verb at exactly 1.0. That
construction takes only `tactic_to_verb` and the `PreconditionModel`, so it carries **no
axis-6 coupling**.

The reverse index — *which tactic produces capability C* — **does not exist anywhere**
in `src/`, `tests/` or `data/`. It is a three-line comprehension:
`host_stack ← {SCAN_HOST, SCAN_NEIGHBOR}`, `curr_host ← {ENUM_HOST}`,
`curr_ports ← {SCAN_PORT}`.

### 4.3 The chain key is sparser, not too sparse — with one named failure

A run makes ~421 (`v1`) / ~438 (`v2`) routing decisions and covers 43–79 % of the
structurally reachable edges. Median observations per cell under `(prev, dst)` is
6.2–6.6, against 27.4/35.2 for the marginal; 29–32 % of cells sit below three
observations and ~70 % below ten.

| profile | v1 cells / median obs / frac < 3 |
|---|---|
| infrastructure_setup | 36.1 / 11.6 / 0.13 |
| pure_impediment | 49.3 / 8.6 / 0.15 |
| pure_steal | 61.0 / 5.2 / 0.29 |
| aggregate | 93.9 / 3.8 / 0.34 |
| **double_extortion** | 32.6 / **2.0** / **0.69** |

**`double_extortion` is the failure case** — a chain learner there is essentially the
prior. Elsewhere it is workable. The design record's own §3 already said as much
("the run is long enough that even the pairwise key is not catastrophically sparse — but
there is no *faithfulness* gain"), and its rejection was faithfulness-per-density **for
the precondition question**. The workflow question is different and remains open.

### 4.4 The observation seam needs no restructuring

Fan-out order per visit is strictly `observe_visit` → (`observe_mtd_interrupt` if
interrupted) → `observe_verdict` → `factors`. `AttackerState._notify` dispatches by
`getattr`, so **none of M1–M8 requires changing the `Modulator` Protocol**. Only the
outcome-tag hook adds an `AttackerState` method, and it is purely additive — existing
modulators are untouched and the null configuration is unaffected.

`state.history` already carries the full ordered trajectory, so **the predecessor place
and the whole tactic chain are available today with zero seam change.**

## 5. The lead already sitting in the readiness sweep

The 4 600-run sweep is reported against its pre-registered cell (`v2_partial`, no MTD),
where nothing beats the ablation arm — 4.60 ablation against 4.52 for the best learner.
Scanning the other three mapping × MTD cells changes the picture.

**`v1_ckc_total`, random MTD @200 s, `infrastructure_setup`, breadth (n = 10 seeds):**

| arm | hosts | raw per-seed |
|---|--:|---|
| ablation, κ = 0 | 1.70 | `[1,1,1,1,1,1,2,3,3,3]` |
| readiness κ=1, **ρ = 0** | **5.70** | `[3,4,5,5,6,6,6,7,7,8]` |
| readiness κ=1, ρ = 0.25 | 3.80 | `[2,3,3,3,3,4,5,5,5,5]` |
| readiness κ=1, ρ = 0.5 *(declared)* | 2.60 | `[1,1,2,2,2,3,3,3,4,5]` |
| readiness κ=1, ρ = 1.0 | 2.10 | `[1,1,1,2,2,2,2,3,3,4]` |

Every seed of the ρ = 0 arm meets or exceeds the ablation arm's **maximum**, and the
gain is monotone in retention. The same profile **without** MTD shows ablation 1.10
against learner 1.10 — the effect is **MTD-specific and vanishes when the defence is
off**.

**This is exactly what §3.1 predicts.** The tradecraft belief is the durable object;
decaying it at the declared ρ = 0.5 destroys most of the capability, and the arm where
it is *not* decayed is the only place in 4 600 runs where the learner beats no-learning
with CI separation. The first-principles argument and the data point at the same fix,
and neither was looking for the other.

**Four caveats travel with it, and they are not optional.**

1. **Post-hoc.** The pre-registration fixed the decision cell on `v2_partial` at
   (κ = 1.0, ρ = 0.5), resolved to the no-MTD arm. Surfacing this as a badge argument
   would be the S6 violation the pre-registration exists to prevent. It is a **lead for
   a fresh pre-registration**, never a re-reading.
2. **Measurement, not attribution.** What is measured is breadth in one
   (mapping × MTD × ρ) cell. Two declared choices could explain it — the mapping
   (`v1_ckc_total` runs at 60–98 % blocked) and ρ itself. Neither is licensed by the
   number.
3. **One profile carries it.** `pure_steal` sits at 0.00 throughout and
   `double_extortion` at 0.40; the pooled `aggregate` separation (0.00 → 0.50) is
   trivial against a zero-variance zero.
4. **Ten seeds.** See §7.

## 6. The rubric

**Gate 0 — credit-machinery declaration (admissibility).** The candidate must state
whether its credit assignment is (a) contemporaneous, (b) propagated over the *declared
structure*, or (c) propagated over the *temporal trace*. Test: does it have a horizon, a
window, a queue, a per-step decay, or an estimate updated toward another estimate? Any
yes → (c) → **inadmissible under the constraint as written**, unless the constraint is
relaxed explicitly and in advance.

| | criterion | demands | must-pass |
|---|---|---|---|
| **C1** | **MTD-conditional consequence** | the learned state must interact with MTD on a *progress-shaped* measure; the candidate derives and pre-registers the predicted **sign** of `I` | **yes** |
| **C2** | **Type discipline** | partition state into what a mutation invalidates (facts) and what it cannot (tradecraft); decay only the former. Uniform decay over a tactic-level belief is an automatic fail | **yes** |
| **C3** | **Non-degeneracy vs the declared-bias control** | behaviour must differ from the best static modulator constructible from the same declared inputs (§3.3) | **yes** |
| **C4** | Constraint/preference factorisation | an unmet precondition must not depress the action's desirability | desirable |
| **C5** | Non-absorbing exploration | no base-supported edge may become behaviourally unreachable through experience — tested on **realised** routing probability, post-exponentiation and post-renormalisation | desirable |
| **C6** | Portability by declaration | reconstructible by editing declared artefacts only, with a measured prediction-accuracy gate and a stated degradation story | desirable |
| **C7** | Plurality non-regression | must not narrow traversal more than the shipped learner at comparable capability | tie-breaker |

**C5 has a hard sub-test that the shipped mechanism's `may_zero = False` invites people
to skip.** `Q > 0` is true of the *factor*; it is not true of the *realised routing
probability*. At κ = 4 with twenty failures, `Q ≈ 1/22` and `Q⁴ ≈ 4×10⁻⁶` — an edge
arithmetically alive and behaviourally dead. This is Marc's "failed early, critical
later" made falsifiable.

**On C4 and that same worry:** context-scoped blame *already substantially answers it
for the readiness key* — early failures land in the `(b, not-ready)` cell and leave
`(b, ready)` at the prior, so a tactic that failed unready is not written off for the
moment it becomes viable. The concern is fully live for the marginal key and largely
retired for the readiness key. **A candidate proposing to abandon the readiness key
reopens it.**

**Scored against C1–C3, the shipped mechanism fails C2 outright and plausibly fails C3;
C1 is undetermined.**

## 7. The power problem, which precedes every criterion question

`mean_ci` reports mean ± 1.96·SEM. From `4.60 ± 0.73` at ten seeds, σ ≈ 1.18.
Detecting a 0.7-host difference (~15 %) at 80 % power needs roughly **45 seeds per
arm**; 0.5 hosts needs ~89; 1.0 host needs ~22. **Every sweep has run ten, and four
successive sweeps have failed to separate adjacent arms.** That is a power failure, not
a finding about mechanisms, and reporting it a fifth time would be a methodological
error rather than a result.

Raising the seed count is **not** changing a metric to improve a row — it gives an
unchanged metric the power to discriminate, and under S6 it is arguably obligatory.
Concentrate seeds on the decision cells (ablation / declared-bias control / candidate at
the declared point on one named mapping and one named MTD condition) rather than
widening the grid.

Separately: **`advanced_after_first_success` should be prospectively excluded from the
gate.** It is a boolean per run, reads 0.960/0.980 on `v2_partial` (saturated), and
returns 0.720 ± 0.126 for two mechanisms differing by 34 % on breadth. The axis-6 record
already refuses to move a badge on *a statistic that cannot discriminate*; that ruling
cuts here too.

## 8. The catalogue — thirteen candidates

M1–M3 are the mechanisms raised in the session record; M4–M13 are added by this study.
"Seam" means a change to the `Modulator` Protocol or `AttackerState`'s hook set.

| | mechanism | gate 0 | C1 | C2 | C3 | LOC | seam | verdict |
|---|---|---|---|---|---|--:|---|---|
| **M1** | non-action-only learning | (a) | ? | — | ? | 5–20 | no | **dead as framed** |
| **M2** | FSM next-step injection | (b) | ? | — | **fail** | 60–80 | no | superseded by M4 |
| **M3a** | pairwise `(prev,dst)` key | (a) | ok | — | **pass** | ~10 | no | **viable** |
| **M3b** | bounded success-chain memory | **(c)** | ok | — | pass | ~50 | no | **inadmissible as written** |
| **M4** | need-inference on block | (b) | ? | — | **at risk** | ~40 | no | strong intuition, weak on C3 |
| **M5** | progress-carrying credit | (a) | **strong** | — | **pass** | 12+40 | additive | **the core** |
| **M6** | distance-to-ready `{0,1,2,3}` | (b) | ? | — | **fail** | ~30 | no | free, but a lookup |
| **M7** | closure credit propagation | (b) | ? | — | ok | ~15 | no | admissible, low ceiling |
| **M8/M12** | type-disciplined forgetting | (a) | **strong** | **pass** | — | ~20 | no | **the other core** |
| **M9** | blocked ≠ failed in credit | (a) | ok | — | ok | ~8 | no | cheap, pairs with M4 |
| **M10** | count-based novelty bonus | (a) | weak | — | pass | ~15 | no | RL-adjacent; declare it |
| **M11** | belief keyed on capability | (a) | ? | — | pass | ~25 | no | best generalisation story |
| **M13** | blocked-attempt budget | (b) | ? | — | at risk | ~35 | no | vivid, adds a declared *k* |

Notes on the entries that need them:

**M1 is dead as framed, for two independent structural reasons.** `v1_ckc_total` has
**zero** dwell-only tactics, so any v1 arm is an identity modulator and the sweep
collapses to v2-only, weakening the portability claim. And a dwell-only place emits
`VERDICT_NONE`, which `observe_verdict` does not count — **there is no credit signal at
a dwell-only place at all.** It survives only if respecified as *apply the factor only
when routing out of a dwell-only place* (~5 lines, well defined), which makes it a
sweepable **variant switch** on "when does an operator re-plan" rather than a mechanism.
That is worth having; it is not an answer to axis 7.

**M2 is superseded rather than wrong.** Injecting a declared successor is a static
lookup, so it fails C3 by construction, and it makes the attacker behave more like the
host expects — which is anti-fidelity, and the freeze's own objection. M4 achieves the
same redirection from *experience* rather than from declaration.

**M3 splits, and the split is the answer to "is this ML/RL?".** A **one-step pairwise
key** (M3a) is credit to the transition just taken: no window, no horizon, no
bootstrapping. It is gate-0 (a) and admissible — and Marc's disagreement with the "that's
RL" framing is **correct for this form**. A **bounded queue of recent transitions
credited when a later success arrives** (M3b) is an eligibility trace with a rectangular
kernel — every-visit Monte Carlo with a truncated horizon. It has no bootstrapping and no
discount, so it is the mildest possible form and emphatically not deep RL, but *"no
eligibility traces"* is listed explicitly and this is one. If M3b is wanted, **relax the
constraint on record and in advance** — to "no bootstrapping, no value function, no
discount" — rather than smuggling it through on the grounds that it has one parameter.

**M4 is the best intuition in the catalogue and its risk is C3.** On a block at `b`
requiring `c ∉ held`, do not downweight `b`; upweight the tactics whose verb produces
`c`. It is self-limiting (the pull expires when `c` is acquired), dense, portable, and it
converges on the golden path without representing chains — the FSM ordering *emerges
from trial and error*, which is the 2026-07-29 ask exactly. But the pull is computable
statically from the relation plus `held`, so a declared-bias control would reproduce it.
It becomes learning only if the *magnitude* is learned — e.g. from how often each
capability has actually blocked this run. **And it is inert on the churn profiles**
(§2.2), which is half the model.

**M5 is the core, and it is far cheaper than "a research project".** Its zero-cost
variant needs **no seam change at all**: credit "did my `held` set grow", which is
already tracked in-layer. Its stronger variant needs the ~12-line outcome-tag hook and
Escape A's achievement terms. It is the only candidate that addresses **both** failure
modes, and it is the only one whose learned quantity is declared nowhere — the strongest
C3 position in the table.

**M6 is free and is a lookup.** The four-level ladder derives entirely from the existing
artefact with no new magnitude, which makes it attractive — and it is a deterministic
function of declared inputs, so it fails C3 as a *learning* claim. It is a good
**declared-bias control arm** for C3, which is arguably its real value.

**M7 stays inside the constraint and has a low ceiling.** Assignment over a static
relation with no temporal window is inverse planning, not TD. But it can only credit the
three capability-producing verbs, so under §4.1 horn 3 it cannot reward attack.

**M8/M12 is the other core, and it is the cheapest thing in the table with existing
measured support.** Split the belief by knowledge type and decay only the perishable
half. It is the C2 must-pass by construction, it is what §3.1 derives from the
literature, and §5 shows the un-decayed arm is the only place in 4 600 runs where the
learner beats no-learning with CI separation. ~20 lines, no seam change.

## 8b. The absorption audit — measured 2026-08-02, and it moves the recommendation

§6's C5 raised belief absorption as a defect, and the natural MVP reading is that
absorption is the lever: tune it and most of the pathology goes. **That was measured
directly and it is false at the declared parameters.** The audit instrumented the
realised routing probability after full composition and renormalisation — not the
factor — against a *state-matched in-run counterfactual* (`base·overlay` renormalised
over the same support inside the same `compose` call, so trajectory, phase-state and
RNG are identical, which is strictly better than a separate κ = 0 run that diverges
after the first decision). 3–8 seeds × 4 cells × 4 κ values, ~5 700–14 500 edge
observations per cell.

**Verdict: at κ = 1.0 / ρ = 0.5, absorption is a non-issue — not a secondary defect, a
non-defect.** The worst suppression any live destination receives is **11×** (minimum
realised/counterfactual ratio 0.089 on `v2_partial · infrastructure_setup`), and
**0.00 %** of edge observations fall below the 1 %-of-counterfactual criterion. Onset
is between κ = 2 and κ = 4, where the minimum ratio falls three orders of magnitude
(0.026 → 5.8×10⁻⁶ on `v1_ckc · aggregate`) and 1–15 % of observations absorb. Under
random MTD the ρ = 0.5 decay holds every `Q` in [0.32, 0.66] and the mechanism is
nearly inert.

**The required floor is 0.0.** Clipping `Q` to `[floor, 1]`, the smallest value keeping
every edge above 10 % of its counterfactual is **0.0 in 22 of 24 run-cells at κ = 1**
and 0.1 in the other two. At κ = 4 it is uniformly ≈ 0.5, which clips the factor's
range to [0.0625, 1] and destroys most of the mechanism's discriminative power. So the
floor is a genuine one-parameter fix for a problem that only exists at κ ≥ 2, and at
κ = 4 the value that fixes it approximates disabling the learner.

**And a floor cannot move the badge, which is the decisive part.** Behavioural arms
(n = 8, `v2_partial · infra · no-MTD`, hosts): full learner 3.62, floor = 0.2 → 4.00,
floor = 0.5 → 4.12, **ablation 4.12**. A floor walks the learner back to the ablation
arm and does not carry it past — the same shape as the readiness repair, and it would
reproduce the same non-result.

### What the defect actually is, located precisely

The three-way decomposition (full / ready-cells-only / not-ready-cells-only), scored on
**readiness-conditional** acceptance and progress rates:

| cell | component | Δ E[progress] | Δ E[acceptance] |
|---|---|--:|--:|
| `v2_partial · infra · no-MTD` | not-ready only | **+1.8 %** | +6.6 % |
| | **ready only** | **−23.7 %** | **+40.5 %** |
| `v2_partial · infra · random` | not-ready only | +1.7 % | +4.7 % |
| | ready only | −7.5 % | +17.2 % |
| `v1_ckc · infra · no-MTD` | not-ready only | +0.0 % | +0.0 % |
| | ready only | −10.8 % | +3.9 % |
| `v1_ckc · aggregate · no-MTD` | not-ready only | +0.0 % | +41.6 % |
| | ready only | −10.5 % | +17.1 % |

**In every cell measured the not-ready component costs between 0.0 % and +1.8 % of
expected progress — it never costs progress.** Suppressing attempts that would fail is
*free and correct*. The ready-cell ordering costs 3.7–23.7 %, and on `v2_partial` it
carries **85–90 %** of the total routing distortion; recon-verb routing mass goes
0.342 → 0.534 under the full learner, of which ready-cell beliefs alone deliver 86 %.

The mechanism, at the place where it hurts:

| place \| ready | n | acceptance | progress | `Q_ready` |
|---|--:|--:|--:|--:|
| command-and-control | 783 | 1.000 | **0.0000** | **0.992** |
| lateral-movement | 506 | 0.996 | 0.0000 | 0.984 |
| execution | 87 | 0.448 | **0.4483** | **0.302** |
| privilege-escalation | 37 | 0.459 | 0.4595 | 0.345 |

Rank correlation of `Q_ready` against acceptance is **+0.921**; against progress it is
**−0.027** (and −0.330 on `aggregate`). **The learner assigns 0.992 to a tactic whose
progress rate is 0.0000 and 0.302 to a tactic whose progress rate is 0.448** — a 3.3×
routing preference pointing away from progress.

**Two honest qualifications.** `credential-access|ready` has acceptance 0.000 over 73
ready attempts and `initial-access|ready` 0.000 over 124, so the learner suppressing
*those* is correct, and they account for the two largest single-place suppressions — a
flat reading of "the learner suppresses exploitation" over-counts, because the
suppression is right for two of the four action tactics and wrong for the other two.
And the progress proxy here is `COMPROMISE_EVENTS`, which credits nothing for
capability acquisition, so reconnaissance scores 0.0000 by construction; a defender of
the current learner could fairly argue that recon has instrumental value this proxy
cannot see. **That qualification is itself an argument for the §9 credit rule**, which
credits capability acquisition — but only the first time, so instrumental value is
recognised and farming is not.

**Sample-size discipline.** The routing-distribution measurements rest on thousands of
decisions per cell and are solid. The behavioural arms are n = 8 and the static and
behavioural decompositions *disagree on the sign of the not-ready component's outcome
effect*. The direction question — which component moves routing away from progress —
is settled; the outcome question is not settled at this sample size, and the 4 600-run
sweep remains authoritative on host counts.

## 9. Recommendation — transform the shipped mechanism in place; build nothing new

**No candidate in §8 needs to be built.** Every change below is an edit to
`ReadinessLearningModulator` or to a declared artefact, keeping the key, the Laplace
estimator, the multiplicative composition and the κ = 0 null-equivalence exactly as
they are. The catalogue's purpose was to establish that nothing *else* is required;
having established it, the MVP is a repair, not an addition.

### 9.1 The audit-and-transform table

| criterion | current status | minimal transformation | cost |
|---|---|---|---|
| **C1** MTD-conditional consequence | undetermined | none — *measure* the 2×2 interaction and pre-register its sign | analysis only |
| **C2** type discipline | **fail** | apply ρ to the perishable object only; `held` severance stays MTD's channel | 0–20 lines |
| **C3** non-degeneracy | **at risk** | add the declared-bias control **arm** (not a mechanism change) | ~20 lines, separate class |
| **C4** constraint/preference | **pass** | none — the readiness key already delivers it, and §8b measures the not-ready component at 0.0 to +1.8 % progress | — |
| **C5** non-absorbing | pass at κ ≤ 1, fail at κ ≥ 2 | optional one-line clip of `Q` to `[ε, 1]`; **measured worthless at the declared point** | 1 line |
| **C6** portability | **pass** | none | — |
| **C7** plurality | unmeasured | none — report pooled path entropy beside the result | analysis only |
| *(the named gap)* credit signal | **misspecified** | achievement terms in the relation + progress-gated credit | JSON edit + ~6 lines |

### 9.2 The two changes that matter, in order

**Change 1 — progress-gated credit. This is the whole repair.** §8b locates the entire
progress cost in the ready-cell ordering, and §4.1 explains why the ordering is wrong:
the credit signal is acceptance. Two edits fix it, and both are provably inert on
everything already measured.

*(a) Achievement terms in the declared relation.* Give `EXPLOIT_VULN` and
`BRUTE_FORCE` a produced `foothold` capability, cleared by `ENUM_HOST` and by network
`mtd_clears`, derived from the `_do_*` cores exactly as the existing entries were. **A
produces-only capability that no verb requires cannot change any readiness verdict or
any enabling cost, and this was verified rather than argued** — 0 disagreements on
`is_ready` across all 8 held-states × 6 verbs, and 0 disagreements on
`CapabilityCostModel.enabling_cost` on both mappings. So the readiness bit's measured
accuracy (1.0000 on `v1`, 0.9169–0.9428 on `v2`) and axis 6's recorded cost model are
untouched by construction.

*(b) Credit on state change rather than acceptance.* In `observe_verdict`, apply the
capability effect first, then credit: a success that grew `held` scores a success; a
success that grew nothing scores a failure; a blocked attempt continues to land in the
`(b, not-ready)` cell, which §8b measures as correct. Contemporaneous, one-step, no
window and no horizon — gate 0 (a), inside the no-RL constraint without argument.

What the rule does mechanically is why it is worth preferring to any of §8's
mechanisms. Scanning while `host_stack` is already held earns nothing, which retires
the recon-farming loop the rank correlation exposes. Re-compromising a host already
owned earns nothing, which is the **churn** failure mode (§2.2) — the half of the model
no block-driven candidate reaches. Moving to a new host clears the foothold so the next
exploit can earn again. And because each verb pays only while it is still advancing the
attacker, **the FSM ordering becomes emergent rather than injected**: this is the
generalisation to procedural rigidity, reached without chains, without next-step
injection and without an eligibility trace.

**Change 2 — type-disciplined forgetting.** The C2 must-pass. `Q(b, ready?)` is a
tradecraft object and the literature says MTD cannot destroy tradecraft (§3.1); ρ
should govern the perishable object only, leaving `held` severance as MTD's channel
into the attacker. The minimal form is a **re-declared ρ with a literature
justification and no code change at all**; the principled form partitions the belief.
Either way it is the change with existing measured support (§5) and the one exposed to
post-hoc-selection risk, so it needs a fresh pre-registration and never a re-reading.

### 9.3 What to run beside them, and what to drop

**Run the declared-bias control arm.** It is the C3 test, it is a comparison arm rather
than a mechanism, it is S6-clean, and it has never been run. Without it no version of
this mechanism can answer an examiner who asks whether it is really learning.

**Settle the seed count first (§7).** Four sweeps have failed to separate adjacent arms
at ten seeds. Changing the mechanism again without changing the power is the fifth.

**Do not build:** M2, M3a, M3b, M4, M6, M7, M10, M11, M13. Each was assessed and none
is needed once the credit signal is right. **Do not spend the C5 floor at the declared
point** — §8b measures the required floor at 0.0 and shows a floor walks the learner
back to the ablation arm without carrying it past. Keep M1 only as an optional variant
switch on *when an operator re-plans*, never as an answer to the axis, and note it is
degenerate on `v1_ckc_total`, which has no dwell-only tactics.

## 10. What this record licenses, and what it does not

**Licensed.** The rubric and its must-pass set; the four structural facts in §4, all
verified against the working tree; the observation that the relation models
preconditions but not achievements; the catalogue's gate-0 classifications; the
identification of the §5 cell as a lead; **§8b's routing-distribution measurements**
(thousands of decisions per cell) — that absorption is a non-defect at the declared
point, that the not-ready component costs no progress, and that the ready-cell
ordering tracks acceptance at ρ = +0.921 and progress at ρ = −0.027; and the
verified inertness of the achievement terms on `is_ready` and `enabling_cost`.

**Explicitly refuted by measurement.** That belief absorption is the dominant defect at
the declared parameters, and that tuning it would remediate most of the pathology. The
required floor is 0.0 at κ = 1, and a floor returns the learner to the ablation arm
without carrying it past.

**Not licensed.** No badge move. No re-reading of the readiness sweep, the frontier,
experiment 2 or any recorded experiment — §5 is a lead for a *fresh* pre-registration
and nothing else. No claim that any candidate will work; every C1 entry in §8 is a
prediction to be pre-registered, not a result. **No outcome claim from §8b's
behavioural arms** — they are n = 8, they disagree with the static decomposition on the
sign of the not-ready component's outcome effect, and the 4 600-run sweep remains
authoritative on host counts. §8b settles *direction*, not *outcome*. No relaxation of the no-RL constraint —
§8 states what M3b would need, and that disposition is Marc's. And no composition of any
new modulator with axis 6's factor 7A/AB until the joint check in
[`modulator_composition.md`](modulator_composition.md) §2 has run.

## 11. Where this connects

- **Scores:** the axis-7 criterion in [`../apt_model_criterion.md`](../apt_model_criterion.md)
  §(d), whose gate §7 argues should be amended *prospectively* rather than re-read.
- **Builds on:** [`learning_capability.md`](learning_capability.md),
  [`learning_representation.md`](learning_representation.md) (whose chain rejection §4.3
  re-scopes), [`learning_readiness_findings.md`](learning_readiness_findings.md) (§5's
  lead), [`experiment_01_findings.md`](experiment_01_findings.md) §3 (the two failure
  modes), [`attacker_state_seam.md`](attacker_state_seam.md) (the observation surface).
- **Constrained by:** [`model_scope_freeze.md`](model_scope_freeze.md) §0 (axis 7 open),
  [`modulator_composition.md`](modulator_composition.md) (the composition bar and the
  seam-split portability argument), and the no-RL constraint.
- **Fed:** item 5 of the axis-6/7 scope-finalisation handoff — the decision this
  study exists to inform. That item was **ruled 2026-08-02** (static weights stay
  the default; the learner is kept as a built, declared, ablatable arm carrying a
  measured negative; no further axis-7 mechanism effort), and the handoff has
  since been retired with all nine items settled. This study's standing is
  therefore evidence behind a taken decision rather than input to an open one.
- **When to update:** when a candidate is ruled in or out; if the declared-bias control
  runs; if the relation gains achievement terms; and when the seed-count question in §7
  is settled.
