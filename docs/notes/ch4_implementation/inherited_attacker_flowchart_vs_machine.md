---
status: durable
chapter: ch4_implementation
created: 2026-07-16
updated: 2026-07-16
---

# The inherited attacker is a flowchart in intent but a self-driving state machine in code — which is why the new attacker is built beside it, not inside it

## Position in the dissertation

The implementation chapter's justification for a realisation choice: that the
behaviourally-grounded attacker is added *alongside* the simulator's original
attacker rather than by modifying it. The argument belongs where the chapter accounts
for what was inherited unchanged versus built fresh, and it doubles as an honest
statement of a constraint the inherited code imposes on the work.

## The idea

The moving-target-defence simulator this project extends, MTDSim, ships with an
attacker, and the project needs a different one — an attacker whose behaviour is drawn
from cyber threat intelligence rather than from a single generic routine. That poses a
build-time choice: modify the attacker already present, or leave it in place and drive
the simulator with a new attacker built beside it. The choice is not a matter of taste.
It is settled by a gap between how the original attacker is *specified* in the paper
that introduced it and how it is *realised* in the code, and the gap is worth stating
because it is invisible from the specification alone.

As specified, the attacker is a flowchart. Brown, Lee and Hong (2023) describe it as a
single decision procedure — discover hosts, reconnoitre a chosen host, attempt an
exploit, fall back to a brute-force attempt, move to the next host — inspired by the
Cyber Kill Chain and the MITRE ATT&CK framework, and followed identically by every
attacker in the simulation. The authors are explicit that this generality is a design
commitment and a limitation in one: every agent runs the same procedure, and an
attacker's *skill* is deliberately not parameterised, which they flag as future work.
Read at this altitude, replacing the attacker looks like redrawing a flowchart.

As realised, the attacker is a self-driving state machine, and the machine carries
structure the flowchart never mentions. The procedure is implemented as six actions —
host scan, host enumeration, port scan, neighbour scan, vulnerability exploitation, and
brute force — and each action, on finishing, *calls the next one itself*. The actions
exchange no arguments; they communicate through shared fields on the attacker object,
so that each action silently assumes an earlier one has already run and populated the
state it reads. Host enumeration, for instance, consumes a queue of hosts that the
host scan fills, and reaches for a "current host" cursor that only host
enumeration itself sets. The whole
chain is started once, from outside, and thereafter propagates under its own control
until the run ends; there is no external loop stepping it action by action. Even the
recovery behaviour is welded in: when a defensive mutation interrupts the attacker, the
action to restart from is hard-coded by the kind of mutation, not chosen by any policy.
None of this — the self-succession, the shared-state coupling, the fixed restart points
— appears in the flowchart. It is how the flowchart was made to run.

That gap decides the build. Modifying the attacker from the inside is hostile work,
because the thing being edited is not a sequence of decisions but a set of welds
between actions that assume each other's state; changing the order in which actions run
means re-cutting those welds, and an action entered out of turn either quietly returns
to the machine's own path or fails outright, since nothing validates that its
assumptions hold. Building the new attacker beside the original avoids that entirely,
and it happens to satisfy a second requirement the evaluation imposes independently: the
original attacker has to survive unchanged in any case, because it is the baseline the
new one is measured against, and a fair comparison needs it preserved exactly. The two
reasons point the same way. The new attacker is built to drive the simulator's existing
actions from outside, and the original attacker is left intact as the baseline.

Two things are worth separating here, because only one of them is demonstrated. That the
coupling is real, and that it makes inside-modification the harder and less faithful
path, is settled by reading the code. Whether the same coupling also *limits how
differently the new attacker can behave* — whether driving the actions from outside
still leaves them re-imposing their built-in order, flattening the new attacker back
toward the original's behaviour — is a live question, not a finding. It is one of two
competing explanations held open for the first experimental results to decide, the other
being that the new attacker behaves distinctly but the current metrics simply do not
reward the difference. The realisation choice defended here does not depend on which
explanation wins; the constraint it names does not need the coupling to bite, only to
exist.

### What this argument does not claim

It does not claim the original attacker is poorly built — the coupling is a reasonable
way to realise a fixed procedure, and it was never meant to be driven from outside. It
does not claim that building alongside escapes the coupling; it claims only that
building alongside is the faithful way to work with it and the way that keeps the
baseline intact. And it does not settle whether the coupling degrades the new attacker's
distinctiveness — that is deferred to the results, and named as a risk rather than
asserted as a cost.

## Evidence and repo anchors

- Design intent (the flowchart, the single generic procedure, skill deliberately
  un-parameterised): the Brown 2023 extraction
  [`../../sources/extractions/brown2023.md`](../../sources/extractions/brown2023.md)
  (artefacts B-ATK-01…08, B-INT-01…03, B-FW-01).
- The realisation, walked at the code level (per-action reads/mutations/successor calls,
  the transition diagram, the callability classification, the reordering ceiling):
  [`../../implementation/pipeline/ogasp/action_layer_anatomy.md`](../../implementation/pipeline/ogasp/action_layer_anatomy.md).
- The attacker's-eye account of the same inherited attacker and the defensive-reset model
  its interrupt behaviour embodies:
  [`../../implementation/substrate_primer.md`](../../implementation/substrate_primer.md)
  §(d)/§(e).
- The two competing explanations for the results, pre-registered:
  the action-layer record §6, and the supervisor decision register
  [`../../implementation/pipeline/ogasp/supervisor_decision_register.md`](../../implementation/pipeline/ogasp/supervisor_decision_register.md)
  §M8.
- The alongside-not-inside seam in the pipeline architecture:
  [`../../implementation/architecture.md`](../../implementation/architecture.md) §(f).

## Revisit conditions

- If the build takes the "carve" that separates each action's executable core from its
  built-in successor call (specified in the action-layer record §3.3), the actions
  become independently orderable and the inside/alongside distinction softens — the
  argument is then about *why the carve was needed*, not *why modification was avoided*.
- If the first results show the new attacker's behaviour is near-identical to the
  baseline's, the deferred risk in this note becomes a finding, and the coupling is
  reported as a demonstrated constraint on distinctiveness rather than a named risk.
- If the results instead show distinct behaviour that the metrics fail to reward, the
  coupling is exonerated as a limiter and this note's deferred question closes the other
  way.
