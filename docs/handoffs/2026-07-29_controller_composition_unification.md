---
status: open
created: 2026-07-29
---

# The last mechanism — an FSM-alignment factor on the controller seam, built as an instrument that measures procedural mismatch rather than as a capability that hides it

**Chain position: after
[`2026-07-29_reconcile_stranded_axis_work.md`](2026-07-29_reconcile_stranded_axis_work.md),
which is blocking.** Do not start this against a `dev` that still reports axes 6
and 7 as NOT ADDRESSED — the whole design argument below depends on what those
two sweeps found, and on `dev` today they found nothing.

Governed by [`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md).
This is the **only** remaining mechanism inside the freeze. Everything else is
future work by that record's §3.

## State of play

**The problem it addresses.** The profiled attacker fails partly because it walks
CTI-derived tactic order while the host simulator encodes a rigid procedural order
of its own, so it attempts actions whose preconditions a differently-ordered
attacker would have established. The driver deliberately refuses to re-impose the
native order, because doing so would manufacture the very coupling the evaluation
exists to expose. That refusal is correct and it leaves the coupling measured only
categorically — we know it costs the attacker, and we cannot say how much.

**Why the obvious framing is the wrong one.** The natural pitch is "a proxy for
learning, conceded because we cannot change the inherited attacker". Rejected,
because it invites the assumption that the existing learner is the better tool for
this job and this is the cheap stand-in. On the learning axis the learner *is* the
better mechanism — it accumulates, updates from evidence, perishes under mutation,
is substrate-independent, and was swept over 2 400 runs. On **procedural
rigidity**, which is what this handoff exists to address, it is not weaker but
incapable.

**Why the learner cannot address rigidity, which is the design fact this session
turns on.** Blocking is a function of *state*: an exploit fails because this host
has not yet been port-scanned. The quantity that would have to be learned is
therefore the success probability of a tactic **conditioned on the attacker's
current phase-state**. The learner is keyed on the destination tactic alone, so it
can only represent the marginal, averaged over every context — and marginalising
over phase-state discards precisely the variable the precondition depends on. This
is a representation limit, not a sample-size one; no number of runs repairs it.

What it does instead is route around the constraint. Unable to learn *exploit after
scanning*, it learns *exploit fails often* and moves weight onto tactics that
always succeed — which is exactly the swept result, blocked fraction falling
sharply while exploitation collapses to a fraction of its successes and breadth
falls with it. The monotonicity has a self-reinforcing loop behind it: avoiding
exploitation drives the phase-state distribution further from the states in which
exploitation would have worked.

An FSM-alignment factor conditions on the current phase — the state variable the
precondition turns on — so it can express what the learner structurally cannot.
The two do not compete on this problem, and the mechanism must not be presented as
though they do.

**The framing that survives scrutiny.** The learning record states precisely what
would move its axis: *a credit signal carrying progress rather than the routing
verdict*. The learner's failure was never its machinery — it was that the binary
verdict it learns from is not a proxy for progress, so a confident learner
optimises toward reconnaissance and away from the objective. The host simulator's
own successor relation **is** a declared statement about what constitutes
progress on that substrate. So this mechanism is best understood as supplying the
missing signal, not as substituting for the learner that consumes it. That
reframing matters practically: it says the cheap version tests the expensive
version's central hypothesis.

## Recommended approach

### Part A — decide what this is for, and write it down first

1. **Justify it as an instrument, not a capability.** Its strength parameter is a
   dial from pure CTI order to native procedural order. Sweeping the dial measures
   *how much a simulator's procedural rigidity penalises a differently-shaped
   attacker* — the coupling finding turned from a categorical observation into a
   quantity. Design the reporting around that curve. The endpoint is not the
   result; the slope is.
2. **Pre-register, in its own commit, before any output exists.** Four studies have
   now used this discipline and it has paid off every time, most recently by
   forcing a badge to be withdrawn after the numbers supported it. State in advance
   what would count as the coupling being expensive, what would count as it being
   cheap, and what result would make the mechanism not worth reporting at all.
3. **State the badge position up front: no badge moves.** Not axis 7 (this is not
   learning), not axis 4 (this responds to the substrate, not the defender), not
   axis 1. If the sweep shows breadth rising as alignment rises, that is *evidence
   for the learning record's hypothesis* about credit signals — a secondary finding,
   reported as such, and explicitly not a badge claim.

### Part B — the design

4. **Where it fires: non-action places only.** Places the mapping declares
   dwell-only dispatch no verb, raise no verdict, and currently route on base
   weights alone. They are the one surface where a bias overwrites no existing
   conditioning signal, and they carry real traffic. Confining the mechanism there
   is what keeps it a *sequencing* nudge rather than action substitution — the
   attacker is redirected only when it was not acting anyway.
5. **What it reads.** The attacker's own current phase, and a **declared successor
   map** transcribed from the host simulator's procedural structure. Do not read
   the successor live: transcribing it makes it a versioned controller artefact
   under the same discipline as the tactic-to-verb mapping, which is both more
   honest and the thing that makes the framework portable — to port to another
   simulator you declare its action vocabulary *and* its procedural order.
6. **Where it lives, and the argument against Marc's stated instinct.** It belongs
   on the **controller** seam, because it is substrate-coupled. But the proposal to
   unify the learning and cost modulators into that same sublayer should be
   **rejected**: those two are substrate-independent, and their independence is the
   portability claim. Moving portable machinery into the port makes it
   non-portable. The correct architecture is the one that already exists plus one
   factor — portable modulators on the movement seam, substrate-coupled modulators
   on the controller seam, one composition rule. That split is not a compromise; it
   is the clearest available statement of which parts an adopter keeps and which
   they must re-declare.
7. **Null-equivalence is non-negotiable.** At zero strength the composed routing
   must be bit-identical to the model without the factor, asserted field for field
   across profiles, seeds and defence conditions, exactly as the three existing
   null guarantees are.
8. **Declare and sweep the strength.** One new declared value, tiered honestly as
   judgement, argued from what the parameter means and never from what it produces.

### Part C — the objection that must be met head-on

9. **This mechanism risks dissolving the project's own coupling finding**, and the
   record must confront that rather than route around it. The mitigations are
   structural: the null arm must reproduce the coupling finding **at full
   strength**, so any reduction is attributable to the mechanism rather than to the
   problem having been defined away; and the finding must remain reportable in the
   dissertation at zero strength, with the swept curve presented as its
   quantification rather than its replacement. This is the same constraint the
   learning work operated under and it held there.
10. **Rule the observation question.** Two readings, and the supervisor should pick
    one. Reading A: the current phase is the attacker's *own* position in its own
    toolchain, so consuming it is self-knowledge and no more privileged than knowing
    which host it is on. Reading B: the successor relation is the host's model of
    how attacks proceed, so consuming it is the adapter knowing the host — which is
    what an adapter is for, and why it belongs in the controller layer. Both are
    defensible; what is *not* in question is that this reads nothing about the
    defender, so the scheme-awareness exclusion is untouched.

### Part D — the composition tidy-up, which is documentation not code

11. **The mechanisms are not fractured; the record is.** Three declared families
    now condition routing through one composition rule, and no single document
    states what the factors are, where each lives, why, and which are active in the
    reported configuration. Write that record. It is also where the freeze's
    configuration pin belongs.
12. **Run the joint-composition check that has never run.** The families have only
    ever been swept one at a time. Two are known to narrow traversal
    independently, so composing them compounds the narrowing, and the stealth
    design already warns that a slower attacker makes every tactic look more
    expensive — an emergent coupling or a hidden double-count, and nobody has
    looked. A small crossed arm at the declared values, reporting path entropy,
    settles it.

## Validation gate

Done when: the pre-registration exists as its own commit before any result; zero
strength is bit-identical to the model without the factor; the successor map is a
tracked, versioned, regenerable artefact; the strength is swept with
per-conclusion held/moved verdicts; the coupling finding is shown to survive at
zero strength; the alignment/coupling-cost curve is reported; the joint-composition
check has run; a tracked record exists; and the criterion is **not** edited,
because no badge moves.

## Hard constraints

- **No badge moves on this work.** If the record ends up arguing for one, that is a
  signal the framing slipped back to capability-from-instrument.
- **Zero strength is bit-identical to today**, and the coupling finding must be
  reportable at zero.
- **No substrate change**, and no change to the tactic-to-verb mapping.
- **The successor map is transcribed and declared**, never read live and never
  hand-tuned per tactic to improve an outcome.
- The freeze in [`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)
  holds: this is the last mechanism, and stealth, scheme awareness and the
  credit-assignment redesign stay future work.
- Determinism; envelope-not-actor phrasing; within-substrate comparability only;
  Australian English; never push.

## Out of scope

- Any claim that this is learning, adaptivity, or a fidelity improvement.
- Relocating the existing modulators into the controller layer.
- Building the stealth state, or anything reading defender behaviour.
- Dissertation prose.
