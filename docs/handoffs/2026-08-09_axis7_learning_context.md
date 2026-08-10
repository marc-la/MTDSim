---
status: open
created: 2026-08-09
---

# Axis 7, learning capability — context only: three sweeps and ~14 000 runs, one separated positive result sitting outside the gated cell, and a criterion that has never recorded the third sweep

## What this document is

**Context only.** The approach arrives in the session prompt; Marc brings the
ideas. No recommended approach, no validation gate, nothing commissioned. What it
supplies is what was tried, what each sweep returned, and the bounds already
established — so a proposal lands against the real bar rather than re-deriving a
wall someone already hit.

Sibling context handoff, same date and same purpose:
[axis 6](2026-08-09_axis6_incentive_rationality_context.md).

## 0. A documentation hazard, stated before anything else

**The criterion's axis 7 is stale.** It states that a learner whose credit signal
carries progress is *"the sole remaining item"*. That signal was built and swept on
2026-08-02 over **7 000 runs**, and all five pre-registered conclusions were not
confirmed, two refuted in the opposite direction. `progress_credit` appears nowhere
in [`apt_model_criterion.md`](../implementation/apt_model_criterion.md).

**Read [`progress_credit_findings.md`](../implementation/pipeline/ogasp/progress_credit_findings.md)
for this axis's current state, not the criterion.** A proposal built on the
criterion's text alone would re-commission work that has already run.

## 1. This axis is a measured negative, and it is where the live positive is

Axes 1, 4, 6 and 7 sit at DESIGNED for two different reasons
([`apt_model_criterion.md`](../implementation/apt_model_criterion.md) §(b)). Axis 1
records an *absence*; this axis records a **measured negative** — a built, declared,
ablatable mechanism shown to operate without conferring advantage.

It is also the axis carrying the **only separated positive result the project has
produced from a learning mechanism** (§3), and that result sits outside the cell its
sweep pre-registered as decisive. That combination is the whole picture here.

## 2. What is built, and what three sweeps settled

**The mechanism.** A within-run Laplace belief over the success and failure verdicts
observed at each tactic-place, entering routing as a declared exponent κ and
perishing by a declared fraction ρ on every MTD mutation. Declared, tiered, banded;
the zero-capability arm is **bit-identical** to a run without the mechanism, so the
arms differ by a parameter rather than by wiring.

**Sweep 1 — the original learner** (2 400 runs). *Operates*: the attacker drives its
own blocked fraction from 91 % to 21 % as capability rises, within runs, against an
ablation that improves only slightly on its own. *Does not help*: compromise breadth
falls 6.5 → 0.8 hosts, effort-to-breadth worsens, no run at any parameter point
reaches the objective.

**Why is the finding, and it is a statement about the measurement rather than about
learning.** The binary routing verdict the learner updates on **is not a progress
signal**. Scanning succeeds far more often than exploiting does, so the belief
correctly concludes that reconnaissance pays — and a confident learner therefore
stops attacking, with exploitation falling from 13 % of successes to 1 %. Experiment
1's churn failure mode was already the observation that success verdicts and progress
differ; a learner does not create that gap, it finds it and optimises into it.

Two results ride with that sweep. **MTD is severely effective against this learner** —
most of the advantage is gone once a quarter of the belief is lost per mutation, at
~42 interrupts per run — which is a defence effect no existing security metric could
register, because what the mutation destroys is an *estimate* rather than a foothold.
And **learning narrows traversal**: path entropy falls at every capability step in all
ten profile × mapping cells, so axes 3 and 7 pull against each other and a claim on
either must name the capability it was measured at.

**Sweep 2 — the readiness re-key** (4 600 runs). The learner re-keyed from the
destination tactic to `(destination tactic, precondition-satisfied?)`, the smallest
key that can express a state-dependent constraint, swept against both the ablation arm
and the destination-only learner as controls.

**The representation was a genuine blocker, and repairing it bought exactly the damage
the marginal key had done — and nothing beyond it.** Breadth at the declared capability
recovers 3.38 → 4.52 hosts, the collapse at high capability is arrested (1.02 → 2.40),
exploitation's share of successes returns 6.0 % → 9.5 %. **But the no-learning ablation
arm sits at 4.60**, and the readiness learner does not exceed it at any capability.
Stage advance is identical to the destination-only learner's and unseparated from the
ablation arm's at ten seeds.

The transferable claim: **representation and reward are independent requirements, and
satisfying one buys exactly the part of the failure it owns.** Representation owned the
*collapse*; reward owns the *ceiling*.

**Sweep 3 — progress credit** (2026-08-02, 7 000 runs, seven arms, 50 seeds, both
mappings, both MTD conditions, five profiles). The credit-signal redesign the criterion
still names as outstanding. **All five conclusions not confirmed; two refuted in the
direction opposite to their prediction.** The stopping rule was honoured — nothing
re-specified, no arm added, no criterion relaxed, no cell re-chosen.

| | conclusion | verdict |
|---|---|---|
| **U1** | the badge gate | **not confirmed**, as predicted — 4.54 ± 0.39 against ablation 4.11 ± 0.31; direction favourable at both MTD conditions, intervals overlapping at both |
| **U2** | the credit repair, like for like | **not confirmed** — direction favours progress in **8 of 10** profile × MTD cells, neither pooled comparison separates. A power statement, not a mechanism statement |
| **U3** | non-degeneracy — **the uncomfortable one** | **not confirmed.** Separates cleanly from `control_asymptotic` (JSD 0.2804); **does not separate from `control_matched`** (0.1196), a declared static bias matched to the learner's own observed aggression |
| **U4** | the instrument quantity | **sign opposite to prediction** — MTD's absolute effect marginally *larger* against the learner. The two readings differ and both are reported |
| **U5** | type-disciplined forgetting | **refuted, with separation, in the opposite direction** — `progress_r00` 1.06 ± 0.18 against `progress_r50` 1.49 ± 0.19, CI-disjoint. **Forgetting is better** |

**U3 is the axis's live problem, in its own words:** *"On the criterion an examiner
asks first — is this learning, or a lookup with extra steps — the answer here is not
yet established."* Running two controls rather than one is what produced it.

**U5 kills a literature-derived recommendation and the reason generalises.** ρ = 0 was
predicted better on the argument that the belief is tradecraft and MTD cannot destroy
tradecraft. Measured, a learner that never forgets becomes confidently committed to a
policy the defence has already invalidated, and the ρ decay is what restores
exploration after a mutation. The argument was about what an *operator* retains; it
does not follow that a within-run frequency estimate keyed on tactic-places is the
right object to make durable. **The argument was good and the object it was applied to
was wrong. Do not adopt ρ = 0.**

## 3. The one separated positive result, and it is a lead

**On `v1_ckc_total` with no MTD, `progress_r50` reaches 1.70 ± 0.29 against ablation
0.44 ± 0.08 and acceptance 0.47 ± 0.07 — CI-disjoint against both, a ~3.6×
improvement, and the only separated positive result in 7 000 runs.**

`v1_ckc_total` is the mapping that runs at 60–98 % blocked: the one where the
CTI-derived order and the substrate's procedural order disagree most.

The coherent reading — **and the record labels it a hypothesis, not a finding** — is
that progress credit pays in proportion to how badly the two orders mismatch. Where
the substrate barely obstructs the attacker there is little for a corrected credit
signal to recover; where it obstructs heavily there is a great deal. That is directly
a claim about porting behaviourally-grounded attackers onto procedurally rigid
substrates, which is the thesis's own subject.

**It carries no gate by pre-registration and must not be reported as a badge
argument.** It needs its own pre-registration with `v1_ckc_total` named as the
decision cell **in advance**. The findings record lists this as successor priority 1.

**A second lead, and the reason the discipline is worth its cost.** The ρ = 0 lead
from sweep 2 replicated on `v1_ckc_total` under MTD and **reversed on the decision
cell**. Naming `v2_partial` in advance is precisely what prevented a mapping-specific
artefact from being adopted as a declared-value change.

## 4. One profile is harmed, and the cause was identified before the sweep ran

Progress credit helps four profiles and **hurts `objective_none_c2` badly** — 3.40
against the ablation's, falling to 2.02. The watch item fired exactly where it was
flagged: the pivot (`lateral-movement` / `ENUM_HOST`) held a belief of 0.138 in the
pre-sweep demonstration on this very profile, and suppressing the pivot closes the
campaign early. The pooled `v2_partial` result is an average over a mechanism that
helps most profiles and harms one, and the pooled figure conceals a real interaction.
Crediting the pivot properly is a mechanism question, not a tuning one; the findings
record lists it as successor priority 2.

## 5. A measurement warning that binds any evaluation here

On **every friction-shaped measure** the destination-only and readiness
representations are indistinguishable to three decimal places, differing only on
breadth. The within-run blocked-fraction measure — which the M8b field recommends and
`blocked_fraction_trend` implements — **cannot discriminate between representations**
and must never be read as evidence for one. A study scoring attacker learning on the
attacker's own friction would conclude the representation makes no difference, which
is the reverse of what it does.

**Cross-mutation retention** — does the attacker re-acquire targets faster after the
nth shuffle? — remains unbuilt and is named as the natural companion measurement.
Cross-run memory is out of scope (M8d, and axis 8's beacon primitive, ruled future
work). The commented-out substrate learning (ATK-04) was considered and refused: a
substrate change that would move every golden, and a pricing discount rather than a
decision capability.

## 6. Constraints that bind any proposal here

- **Run the second control.** U3 is the standing demonstration; one control invites
  the near-miss.
- **Name the decision cell in advance.** Both leads in §3 exist because a cell was
  named before the run, and one of them reversed across mappings.
- **The degenerate region.** At 200 s no arm completes the objective; evidence must
  be breadth- or time-shaped.
- **Fifty seeds did not separate U2's 8-of-10 direction.** Power is a real constraint
  on this axis, not a formality.
- **The stopping rule.** No re-specification after a criterion fails to discriminate;
  a repair motivated by a published defect is exactly the circumstance in which
  criteria drift.
- **Axis 3 pulls against this one.** Learning narrows traversal in all ten cells; any
  claim on either axis names the capability it was measured at, and the reported
  configuration stays modulators-null.
- **Scores move on evidence only** — never change the model, weights, mapping or
  metrics to improve a row (S6;
  [`../workflows/guardrails.md`](../workflows/guardrails.md)).
- Determinism (SIM-05); envelope-not-actor; Australian English; branch per session;
  commit locally; **never push** without an explicit ask.

## Reading list

- [`../implementation/pipeline/ogasp/progress_credit_findings.md`](../implementation/pipeline/ogasp/progress_credit_findings.md)
  §2 (the five verdicts), §3 (both leads), §4 (the harmed profile), §6 (successor
  priorities), §8 (which negatives are real and which are the instrument). **The
  single most decision-relevant record for this axis.**
- [`../implementation/pipeline/ogasp/learning_readiness_findings.md`](../implementation/pipeline/ogasp/learning_readiness_findings.md)
  — representation versus reward, and the friction-measure warning.
- [`../implementation/pipeline/ogasp/learning_capability.md`](../implementation/pipeline/ogasp/learning_capability.md)
  §7.5 — the axis-3 trade, measured in all ten cells.
- [`../implementation/pipeline/ogasp/learning_axis_evaluation_findings.md`](../implementation/pipeline/ogasp/learning_axis_evaluation_findings.md)
  — what a learning attacker exposed about the evaluation apparatus: the substrate's
  success verdict, the atom every metric in this lineage is built on, is not a
  progress signal.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(d) axis 7 and §(e) — **stale, see §0**; read for the badge criterion and the
  fidelity placement, not for current state.

**The transferable method** — how to instrument an axis, extracted from all eight and
roughly 30 000 runs — is
[`axis_instrumentation_method.md`](../implementation/pipeline/ogasp/axis_instrumentation_method.md).
Read it before proposing an instrument, a control or a figure.

## Out of scope for this document

It commissions nothing, sets no gate, recommends no build and expresses no
preference. The approach arrives in the prompt.

## Return format

Default ([`../workflows/session_workflow.md`](../workflows/session_workflow.md#handoff-workflow)):
framed in terms of the thesis and succinct — which claim moves, which criterion row
is affected, what is now sayable. A null or inverted result reports the same way.
