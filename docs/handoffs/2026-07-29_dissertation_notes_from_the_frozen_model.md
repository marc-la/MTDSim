---
status: open
created: 2026-07-29
---

# Draft the five dissertation notes the frozen model has earned — the argument is settled, the prose is not, and the notes are the last thing standing between the results and the chapters

**Chain position: after
[`2026-07-29_reconcile_stranded_axis_work.md`](2026-07-29_reconcile_stranded_axis_work.md).**
Every note below cites results that `dev` cannot currently see. Drafting them
first would produce prose whose evidence footer points at nothing.

## State of play

The model is frozen
([`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)).
The remaining work is almost entirely writing, and the project's staging layer for
dissertation prose is thin relative to what the implementation records now hold.

The framing this work now defends has shifted, and the shift should be reflected
in what gets written. **The attacker model is instrumental, not terminal.** The
contribution is not "a more faithful attacker exists"; it is (a) what greater
fidelity captures about APT behaviour that prior threat models in this space do
not, and (b) how that changes MTD evaluation — via a result about defence
rankings, and via a framework other researchers can port. The criterion is the
warranty on (a), not the contribution itself.

Each note below is one idea, positioned, and each already has its evidence. None
requires new work. Load the notes rubric in full and the voice contract before
drafting any of them.

## The notes to write, in priority order

**1. The defence ranking inverts between attacker models.** `ch5_evaluation`.
The strongest result the project has, and the one the criterion cannot score. The
claim in one sentence: two attackers that depend on different substrate properties
are protected against by different defences, so an MTD evaluation's recommendation
is a function of its threat model. Carries the effort-to-breadth crossover as its
mechanism and the ten-seed, interval-dependence and mapping caveats as its
boundary. **Write this one first** — the other four position around it.

**2. Procedural mismatch is a measurement artefact that evaluations mistake for
attacker weakness.** `ch6_discussion`. Simulators encode a native precondition
order; an attacker that does not walk it manufactures failure that has nothing to
do with the defence. Transferable to any host simulator, and it is the argument
that motivates the alignment instrument.

**3. Operating points that cannot discriminate.** `ch5_evaluation`. Every run this
project published sat at a mutation interval where the headline success metric is
pinned at zero for both attackers, and that was not known until it was checked.
The transferable rule — establish that your operating point can discriminate your
metric before reporting it — is embarrassingly basic and, on the evidence of the
surrounding literature, not standard practice. Short, sharp, high value.

**4. An attacker given learning without a progress-carrying reward optimises away
from the objective.** `ch6_discussion`. A design warning for exactly the learning
attacker this literature keeps asking for: the learner correctly concludes that
reconnaissance pays and stops attacking, so compromise breadth falls as the
capability rises. Flag honestly that whether this generalises beyond this
substrate is untested.

**5. What a host simulator must expose for a CTI-derived attacker to drive it.**
`ch4_implementation` or `ch3_design` — decide when drafting. The portability claim
made concrete and therefore falsifiable: an action vocabulary, a per-action
verdict, an interrupt signal, and a time channel. Must state the integration cost
honestly — porting required carving an action-dispatch interface into the host and
later re-homing all attacker timing — because a named cost is more useful and more
credible than a portability adjective. Must also state the ceiling: fidelity is
bounded by the host's action vocabulary, not by the richness of the CTI, so a
technique-grained attacker over a six-verb host gains sequencing resolution and no
behavioural resolution.

## Two things to check while drafting, not after

- **The measurement-failure thread runs through notes 1, 3 and 4** — four
  progression or credit measures have now failed for structurally different
  reasons (saturation twice, an inverted sign, a misspecified reward). Decide
  deliberately whether that is a sixth note or a recurring motif inside the
  others. It is currently scattered across implementation records and is arguably
  the project's most transferable methodological output.
- **Notes 1 and 5 are the two that carry the "means, not end" reframing.** If the
  dissertation still reads as "we built a better attacker" after these are
  absorbed, the reframing did not land.

## Validation gate

Done when each note clears the rubric's cross-examination in full, sits in the
chapter subdir matching its position statement, confines repo paths to its
evidence footer, and states honestly what is demonstrated as against designed or
conjectured. A note that cannot yet clear the rubric is not committed — park it.

## Hard constraints

- **Load the notes rubric in full and the voice contract before drafting.** The
  voice contract is a default for notes and a hard gate for thesis prose.
- **No new results.** Every claim traces to a record that already exists.
- **Envelope, not actor**, throughout; within-substrate comparability only; no
  cross-paper magnitude claims.
- Australian English; never push.

## Out of scope

- Any new experiment, mechanism or metric.
- LaTeX chapter assembly — notes feed the chapters; they are not the chapters.
