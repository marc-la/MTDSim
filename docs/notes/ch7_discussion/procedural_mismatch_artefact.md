---
status: durable
chapter: ch7_discussion
created: 2026-08-01
updated: 2026-08-14
---

# Procedural mismatch manufactures attacker failure that an evaluation will misread as attacker weakness

## Position in the dissertation

A discussion-chapter interpretation of the profiled attacker's dominant failure
mode: what looked like a weak attacker is in substantial part a measurement
artefact of the host simulator's encoded procedure. It is the argument that
motivates the alignment instrument proposed as future work, and it is
transferable to any evaluation that imports an attacker into a simulator built
around a different one.

## The idea

Every simulator that executes attacker actions encodes a procedure. Somewhere in
its implementation there is an order in which state must be established — a
host must be discovered before it is scanned, scanned before it is exploited —
and that order is usually invisible, because the simulator's own attacker walks
it by construction. The attacker inherited with this project's simulator is
exactly such an actor: a scripted intruder whose six phases *are* the
simulator's precondition order, and which consequently never attempts an action
the environment refuses. Its refusal rate is not low; it is structurally zero.

Import an attacker whose ordering comes from somewhere else and the procedure
becomes visible as a wall. The attacker built here traverses adversary tactics
in the orders that analyst-curated threat intelligence records — orders chosen
by real campaigns, not by this simulator — and when it was first run, the
environment refused most of what it attempted. In the worst-affected profile,
ninety-five per cent of the actions attempted across a run were rejected before
they executed, because the tactic sequence the intelligence describes had not
established the state the simulator's procedure demands: the attacker arrives
at an exploitation-shaped action without having performed the particular
scanning step this implementation requires first. The refusals are not a
property of the defence — they occur identically with the defence switched off —
and they are not a property of the campaigns being modelled, whose recorded
sequences ran to completion in the incidents the intelligence documents. They
are a property of the coupling: two legitimate procedural
models, the campaign's and the simulator's, disagreeing about order.

The danger is what an evaluation makes of this. On every headline metric the
refusals read as attacker weakness — low compromise counts, zero success rate —
and nothing in those metrics distinguishes *the defence stopped the attacker*
from *the simulator's procedure stopped the attacker*. The distinction only
appears when the attacker's action budget is decomposed into refused, failed,
and succeeded attempts, a decomposition no conventional security metric
performs. An evaluation that skips it will fold the simulator's procedural
rigidity into the attacker's measured capability, and may then conclude either
that sophisticated attackers pose little threat on this terrain, or that the
defence deserves credit for failure it did not cause. Both conclusions
misattribute an artefact of the instrument to the thing being measured.

Two causes contribute, and they must be kept separate because one is fixable
and the other is structural. Part of the early refusal rate was a modelling
choice: the first mapping from adversary tactics onto the simulator's six
executable actions was deliberately coarse, and a finer mapping — under which
tactics with no sensible counterpart consume time without dispatching an
action — reduced the refusal rate severalfold. That part was this project's to
repair, and was repaired. What remains is structural: whether an action is
accepted depends on state the simulator's native order establishes, so *any*
foreign ordering pays a rigidity penalty that the native attacker, by
definition, does not. The penalty can be reduced by better mapping; it cannot be
removed by it.

The strongest corroboration that the constraint is real and behaviour-shaping
came from an unexpected direction. When the attacker was later given a learning
capability — a memory of which tactics' actions the environment accepts — it did
not learn to satisfy the procedure; it learned to avoid it, shifting its effort
onto reconnaissance actions that carry almost no preconditions and abandoning
exploitation almost entirely. An attacker capable of adapting, given only
outcome feedback, treats the procedural wall as terrain and routes around it. A
companion note takes up why that happens and what it says about learning
rewards; the point here is what it confirms about the wall.

This diagnosis converts into an instrument, and that is its productive form. If
the penalty is caused by the distance between a foreign ordering and the native
one, then a factor that biases the attacker's routing by a controllable amount —
from fully intelligence-derived order at one end to the simulator's native order
at the other — turns the categorical observation into a measured quantity: sweep
the dial and read off how much of the attacker's failure the simulator's
rigidity accounts for. The instrument is now built — a declared alignment dial
on the unit interval whose zero setting is bit-identical to a run without it, so
the original finding is reproduced at full strength by construction and the
sweep is an ablation rather than a repair. It must be reported as an instrument
for measuring the host's rigidity — not as a fidelity improvement, since at its
limiting end it tunes the attacker toward the host simulator's own procedural
order, which is the opposite of behavioural independence.

The transferable statement is a validity requirement rather than a result. Any
evaluation that drives a host simulator with an attacker the simulator was not
built around — a threat-intelligence-derived agent, a learning agent, an agent
ported from another platform — should establish how much of the attacker's
measured failure the host's procedural encoding accounts for, before any of that
failure is attributed to the defence or to the attacker. The check is cheap: run
without the defence and decompose the action budget. The mismatch is not an
argument against either component — the simulator's procedure is a legitimate
model of one attack style, and the imported ordering a legitimate record of
others — but their disagreement is a property of the experimental apparatus, and
apparatus effects belong in the error budget, not in the findings.

## Evidence and repo anchors

- The refusal quantification and the two failure modes:
  [`../../implementation/pipeline/ogasp/experiment_01_findings.md`](../../implementation/pipeline/ogasp/experiment_01_findings.md)
  §3–§4, §8 (the supervisor-agreed reading: two separable causes).
- The coarse first mapping and its deliberate coarseness:
  [`../../implementation/pipeline/ogasp/controller.md`](../../implementation/pipeline/ogasp/controller.md);
  the finer replacement:
  [`../../implementation/pipeline/ogasp/controller_mapping_v2.md`](../../implementation/pipeline/ogasp/controller_mapping_v2.md).
- The structural argument and the alignment instrument's design brief:
  [`../../implementation/pipeline/ogasp/model_scope_freeze.md`](../../implementation/pipeline/ogasp/model_scope_freeze.md)
  §5; open work in
  [`../../handoffs/2026-07-29_learning_under_procedural_rigidity.md`](../../handoffs/2026-07-29_learning_under_procedural_rigidity.md).
- The learner routing around the constraint:
  [`learning_without_context.md`](learning_without_context.md) (sibling note) and
  [`../../implementation/pipeline/ogasp/learning_capability.md`](../../implementation/pipeline/ogasp/learning_capability.md).
- The substrate's native order, attacker's-eye view:
  [`../../implementation/substrate_primer.md`](../../implementation/substrate_primer.md).

## Revisit conditions

- ~~If the alignment instrument is built…~~ **Built 2026-08-14 status:** the
  dial exists (declared, null bit-identical). When its rigidity sweep is run and
  reported: if the penalty is small, this note's "substantial part" weakens to
  "minor part" and the attacker-weakness reading regains ground; the note is
  rewritten either way, because the point of the instrument is to replace this
  note's categorical claim with a number.
- If a future mapping eliminates refusals entirely, the structural half of the
  diagnosis is falsified for this host and the note narrows to the mapping
  half.
- If the same decomposition is run on another host simulator and shows no
  mismatch penalty for a foreign attacker, the transferability claim needs a
  boundary it does not currently have.
