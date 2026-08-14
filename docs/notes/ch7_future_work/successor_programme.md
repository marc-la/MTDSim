---
status: durable
chapter: ch7_future_work
created: 2026-08-14
updated: 2026-08-14
---

# The two substrate upgrades this work's closures point at — a reactive defence and a tactic-level action layer

## Position in the dissertation

The future-work chapter's central claim: that this project's ruled-out directions
are not scattered loose ends but converge on two specific extensions to the
inherited substrate, each of which this work's own negative results identify as a
binding constraint. The note names them, states the condition under which each
becomes worth building, and argues that a measured negative is a sharper
prescription for a successor than an unexplored idea. It is the material the
conclusion compresses into "the next step in the line of research".

## The idea

A future-work section is strongest when it is not speculation but the visible
remainder of a completed argument — the questions the work could not answer because
a specific piece of the apparatus was missing, named precisely enough that a
successor knows what to build first. This project's ruled-out directions share that
character. Several capabilities were built, swept, and found not to pay; several
axes of the attacker-fidelity criterion were closed rather than demonstrated. Read
together, their closures point at the same two absences in the inherited simulator,
and each absence is a self-contained programme with a stated trigger.

### A reactive defence, and the evaluations it would unlock

The first constraint is that every defence in the inherited pool moves on its own
clock and is blind to the attacker. This single fact closed two fidelity axes at
once. An attacker cannot gain advantage by *adapting to defender resistance* when
the defender never responds to it — there is nothing to adapt to, so adaptivity was
closed as intractable on this substrate rather than as a model deficiency. And an
attacker cannot exploit *awareness of the defence scheme* — timing a strike to a
mutation, or acting beneath a decision threshold — when the defence has no decision
process to read, so scheme-awareness was closed to future work on the same root
cause. A reactive, metrics-driven defence is the missing piece both closures name.
Its natural realisation already exists in the lineage as a reinforcement-learning
MTD orchestrator, but the available implementation was judged untrustworthy and its
retraining was ruled out for this work; standing it up faithfully — or building a
simple, honestly-calibrated event-based trigger that does not defeat its own purpose
through circularity — is the precondition for reopening either axis. With a defence
that responds, the adaptivity and scheme-awareness experiments this work could only
describe become runnable, and the attacker-side mechanisms already designed against
them (a recovery-pivot behaviour; a side-channel-informed tempo) become the natural
first experiments.

The condition is precise, which is what makes this a prescription rather than a
wish: the reactive defence must be trustworthy enough that a difference in the
attacker's behaviour against it is attributable to the attacker, not to the
defence's own miscalibration. A defender tuned on the very metrics the attacker
moves would make any result circular, and it was that circularity, not a lack of
ambition, that closed the scheme-awareness axis in the first place.

### A tactic-level action layer, and the fidelity ceiling it would lift

The second constraint is that the attacker's executable actions are the inherited
simulator's six scripted phases, which encode one intended procedure. Driving them
in the orders that threat intelligence records forces a mismatch — the campaign's
sequence and the simulator's precondition order disagree — and that mismatch
manufactures attacker failure the evaluation must be careful not to misread as
weakness. This project measured the mismatch and instrumented it, but could not
remove it, because removing it means building new attacker actions: a capability per
adversary tactic, rather than a mapping of fifteen tactics onto six phases built for
a different attacker. That is the extension a successor with more substrate time
than this project had would make, and it is the one this work most consistently
named as the route to a genuinely higher-fidelity model. Crucially, the framework
was designed to receive it — the attacker's structure, routing and parameters sit in
their own layer above the action vocabulary — so a richer action set slots in
without disturbing the model that drives it, which is the extensibility claim the
whole design rests on made concrete.

### Why the negatives are the load-bearing part

The temptation in a future-work section is to list capabilities not yet added. This
note deliberately does the opposite: its two programmes are defined by what was
*tried and measured to fail*, because a measured negative bounds the successor's
expectations in a way an untried idea cannot. The learning capability was built and
shown to reduce the attacker's own effectiveness on this substrate, for a diagnosable
reason — the outcome signal it learned from rewards reconnaissance over progress —
so a successor knows not to rebuild the same learner but to redesign its credit
signal. The incentive machinery was built twice and shown not to move the evaluation,
because the substrate gives the attacker nothing to be rational toward, so a successor
knows the missing piece is a located objective, not a cleverer decision rule. Each
negative hands the next researcher a narrowed problem rather than an open one, which
is the most useful thing a completed honours project can leave behind.

## Evidence and repo anchors

- The two axis closures that name the reactive defence:
  [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md)
  (axis 4 disposition, axis 8), and the intent arc
  [`../../implementation/research_record/threads/axis8_rise_and_fall.md`](../../implementation/research_record/threads/axis8_rise_and_fall.md).
- The action-layer ceiling and the extensibility design it would exercise:
  [`../ch4_methods/host_simulator_contract.md`](../ch4_methods/host_simulator_contract.md),
  [`procedural_mismatch_artefact.md`](../ch6_discussion/procedural_mismatch_artefact.md),
  [`../../implementation/research_record/threads/movement_objectives.md`](../../implementation/research_record/threads/movement_objectives.md).
- The measured negatives that bound each programme:
  [`../../implementation/research_record/threads/learning_capability.md`](../../implementation/research_record/threads/learning_capability.md),
  [`../../implementation/research_record/threads/incentive_rationality.md`](../../implementation/research_record/threads/incentive_rationality.md);
  siblings [`learning_without_context.md`](../ch6_discussion/learning_without_context.md),
  [`state_bounds_measurable_disruption.md`](../ch6_discussion/state_bounds_measurable_disruption.md).
- The lineage reinforcement-learning defence a reactive pool would revive: [`tay2024`](../../sources/extractions/tay2024.md).

## Revisit conditions

- If a reactive defence is built and the adaptivity or scheme-awareness axis is
  reopened, that axis moves from future work into the results, and this note narrows
  to the action-layer programme alone.
- If the action layer is extended and the procedural-mismatch penalty disappears,
  the fidelity-ceiling argument is discharged and the note reframes around what the
  richer attacker then reveals.
- If a successor shows either negative result was an artefact of this project's
  particular implementation rather than a substrate limitation, the corresponding
  programme's framing weakens and must be restated.
