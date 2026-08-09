---
status: open
created: 2026-08-09
---

# Axis 4, adaptivity to defender resistance — context only: the loop reacts, a verdict-blind ablation cannot be told from it, and the axis's own three measurements have never been run

## What this document is

**Context only.** The approach arrives in the session prompt; Marc brings the
ideas. No recommended approach, no validation gate, nothing commissioned. What it
supplies is what is built, what has been measured, and the bounds already
established — so a proposal lands against the real bar rather than re-deriving a
wall someone already hit.

**The approach arrived, 2026-08-09 (same day, after writing):**
[`2026-08-09_axis4_plural_recovery_instrumentation.md`](2026-08-09_axis4_plural_recovery_instrumentation.md)
commissions the axis's instrumentation — the failure column's recovery
repertoire measured *distributionally* (Hill diversity, redirect JSD against the
verdict-blind null), inside the bounds this document records: §3's wall stands
and is quoted as the ceiling, never contested. This document stays what it is —
the context that brief executes against; read both.

Siblings, same date and same purpose, one per axis:
[axis 6](2026-08-09_axis6_incentive_rationality_context.md),
[axis 7](2026-08-09_axis7_learning_context.md).

## 1. This axis is a measured negative, not an absence

Axes 1, 4, 6 and 7 all sit at DESIGNED for two different reasons, and the criterion
records that the badge cannot encode the difference
([`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
§(b)). Axis 1 records an *absence*. **This axis records a measured negative**: a
built, declared, ablatable mechanism shown to operate **without conferring
advantage**.

The consequence: the mechanism is not what is missing. A positive result here means
changing **what is measured** or **what the loop conditions on** — not adding
another modulator. Five declared modulators have now been swept and every one
narrows traversal, so a sixth of the same shape is the move with the most evidence
against it.

## 2. What is built

The minimal adaptive loop, and both halves are on record as operating:

- **M2 — outcome-reactive re-routing.** The substrate's verdict on each dispatched
  action selects between success and failure transition-weight sets at the current
  place.
- **M1 — position throw-back.** An MTD mutation that severs the attacker's position
  throws the net's state back.

Built at commit `48471b8`, verified in
[`runtime_verification.md`](../implementation/pipeline/ogasp/runtime_verification.md).

**The M8b field** asks for three response-shaped measurements: change in action mix
before versus after an MTD trigger, recovery time from an MTD-induced throw-back,
and whether failure-conditioned routing measurably redirects effort (weight-set
switch frequency against progress). These are the measurements that would
discriminate *reacts* from *adapts usefully*.

## 3. The bound that dominates everything — the verdict-blind ablation

**Experiment 2 gave this axis the control it had never had, and it failed cleanly**
([`experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
§11).

The arm: an overlay whose value tables are **empty**, so composition passes every
destination through at 1.0 — the adaptive loop off, built as a value change rather
than as new wiring. Run on identical seeds across the full matrix.

- At **200 s**, *none* of the three progression measures separates the
  verdict-conditioned arm from the verdict-blind arm on the pre-registered bar (two
  profiles and two defence conditions with disjoint intervals).
- At **2 000 s**, breadth reaches one profile and three conditions — the profile
  half of the bar is not met.
- Point estimates are quietly instructive: conditioning helps nominally on four of
  five profiles under no MTD (`objective_exfiltration_impact` 8.10 against 7.50,
  `aggregate` 6.40 against 5.80) and **hurts** on the fifth (`objective_none_c2`
  4.10 against 5.40), with **every interval overlapping**.

**The statement the pre-registration committed to reporting as a finding rather
than a soft pass: routing on the substrate's verdict is approximately free.** After
1 600 paired runs the loop has not been shown to change an outcome. Axis 4 had
previously held at DESIGNED on the argument that nothing separated *reacts* from
*adapts usefully*; that argument is retired, and the badge now holds on a control.

## 4. The axis's own next step is already discharged, and it did not move the badge

S1 named attacker-state-conditioned dynamic weights as the way forward. The axis-7
learner supplies exactly that: the routing weights **do** update from experience
(2026-07-29). What it produced was a sharper version of the same verdict rather than
a different one — the attacker measurably reduces its own friction as it learns, and
its compromise breadth falls as it does so. The mechanism operates and still confers
no adaptive *advantage*, which is what this badge has always turned on.

Read [axis 7's context](2026-08-09_axis7_learning_context.md) before proposing
anything that routes on accumulated experience; that programme has ~14 000 runs
behind it.

## 5. Built and never reported — the axis's own three measurements

This is the one clean gap on the axis. All of these exist in
[`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py) §3:

| reader | what it computes | run anywhere? |
|---|---|---|
| `interrupt_action_mix` | verb and place-class mixes in the *n* visits before versus after each interrupt, pooled within run and paired so seed variance cancels | **never** — appears nowhere outside the suite record |
| `recovery_times` | sim time from each interrupt to the next success verdict, censored at run end | validation harness only |
| `refoothold_times` / `refoothold_rate` | time to re-establish position after a severing interrupt | demonstration-arms workspace |
| `failure_routing_rate` | fraction of verdict-carrying routing decisions taken on the failure column | validation harness only |

Their recorded blind spots, which travel with any use: windows near run edges are
short and overlapping windows around interrupt bursts double-count visits;
"recovery" means *any* success, not recovery of the lost position specifically;
`failure_routing_rate` is a rate only, and the correlation with breadth plus its
interval is the caller's job via `interval_report`.

## 6. The standing boundary on what this axis is

Adaptation here is **outcome-reactive re-routing over static weight sets**. It does
**not** condition on the defence itself — that is axis 8, which is closed on
evidence (2026-08-09): triggering is clocked in every arm, so nothing the attacker
does changes *when* the defender deliberates, and the one defence that reads
attacker-derived metrics converges to constant-action policies that do not read
their state. Do not reach for a defence-conditioned variant of this loop without
reading that closure; it is the same wall.

## 7. Constraints that bind any proposal here

- **The degenerate region.** At 200 s neither attacker completes the objective, so
  success-rate-shaped measures discriminate nothing. This is precisely why the
  axis's three measurements are **windowed** rather than outcome-based.
- **Run the second control.** Axis 7's U3 is the standing demonstration: a mechanism
  that separates from a weak control and not from a matched one has not been shown
  to do anything.
- **Ten seeds separate almost nothing.** `interval_report`; `ordering_supported` is
  the gate.
- **Reader versus mechanism.** A reader changes nothing and moves no badge. A
  mechanism raises the S2 freeze question and a comparability argument.
- **Scores move on evidence only** — never change the model, weights, mapping or
  metrics to improve a row (S6;
  [`../workflows/guardrails.md`](../workflows/guardrails.md)).
- Determinism (SIM-05); envelope-not-actor; cross-arm comparisons
  effort-denominated, never time-denominated; Australian English; branch per
  session; commit locally; **never push** without an explicit ask.

## Reading list

- [`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
  §11 — the verdict-blind ablation, in full. The single most decision-relevant
  record for this axis.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(d) axis 4 (including the discharged S1 step), §(f2), §(d) axis 8's amendment for
  the defence-conditioning wall.
- [`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  §(b) — the four axis-4 readers and their blind spots.
- [`../implementation/pipeline/ogasp/runtime_verification.md`](../implementation/pipeline/ogasp/runtime_verification.md)
  — the loop verified as operating, which is not in question.

## Out of scope for this document

It commissions nothing, sets no gate, recommends no build and expresses no
preference. The approach arrives in the prompt.

## Return format

Default ([`../workflows/session_workflow.md`](../workflows/session_workflow.md#handoff-workflow)):
framed in terms of the thesis and succinct — which claim moves, which criterion row
is affected, what is now sayable. A null or inverted result reports the same way.
