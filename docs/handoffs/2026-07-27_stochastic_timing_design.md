---
status: open
created: 2026-07-27
---

# Design the move to stochastic timing on the Petri nets — choose the timed-net semantics, settle where the clock lives, parameterise the per-tactic exponential rates, place the confusion penalty in the net, and prove out the comparability argument, all on paper before any code is written

**Chain position: wave 2 — after the controller rebuild, before the timing
build.** It needs the dwell-only tactic set to know which places carry time
without an action. **This handoff writes no code.** That separation is
deliberate and was asked for explicitly: the planning is the deliverable, and the
implementation handoff
([`./2026-07-27_stochastic_timing_implementation.md`](./2026-07-27_stochastic_timing_implementation.md))
is gated on it. Executes the design half of **S3**.

## State of play

**The ruling.** Timing may be taken from either layer and currently comes from
the inherited simulator, but the direction is for the **movement layer to be the
timing source**: a time per tactic, drawn from an **exponential distribution**,
with **non-action tactics consuming time and doing nothing else**. The
simulator's MTD confusion penalty is to be replicable the same way — a place in
the net carrying the same base duration under the same stochastic regime. The
supervisor's caveat is the operative constraint and should shape the whole
design: the numbers are **inherently arbitrary, so justifying them is the key**.

**This lifts a standing deferral.** Timed-net firing semantics were explicitly
deferred; the per-tactic catalogue was built as *plain dwell, not a stochastic
firing rate*, and the artefact says so in its own metadata. S3 reverses that, and
the catalogue's declared semantics will need to change with it.

**Where time comes from today — establish this precisely before designing, since
the whole handoff turns on it.** Grep-level reading of the current loop says a
tactic costs the per-tactic dwell **plus** the dispatched verb's native cost, and
that the movement arm does **not** pay the simulator's confusion penalty on an
MTD interrupt while the baseline arm does. Both need confirming by test, not by
reading. If both hold, this design has to resolve a double-charge and an
inter-arm asymmetry, and neither is a detail — the primary metric is a mean over
action durations, so anything that changes what time an action costs changes the
headline number on one arm and not the other.

**The precedent is favourable and already surveyed.** The background survey
establishes that the field norm for timed adversary models is to declare rates
and sweep them, with the closest executed stochastic-Petri-net precedent stating
outright that its rates are arbitrary pending expert determination, while its
*structure* was face-validated. Moving to exponential firing therefore moves this
work *towards* the surveyed precedent rather than away from it — worth saying in
the design record, because it converts "our timings are arbitrary" from an
apology into a position the literature already occupies.

**The validity framework is also already written** and survives the change: the
tiered badges, the four anti-circularity rules, and shape-not-scale all carry
over. What changes is that a declared value becomes a **distribution's mean**, so
the calibration target moves from a single emergent timeline to the shape of a
distribution of them.

## Recommended approach

Work through these in order; each is a decision the record must state with its
alternatives, not a step to perform.

1. **Choose the formalism, and say what it buys.** The live options are a
   stochastic Petri net with every transition exponentially timed, a generalised
   stochastic Petri net separating immediate (weighted, zero-time) transitions
   from timed ones, and a deterministic-and-stochastic hybrid. The generalised
   form looks the closest fit to what already exists — the *place* holds the
   time, the *routing choice among enabled transitions* is already a weighted
   immediate selection, and the existing weight composition already behaves like
   firing probabilities among enabled transitions. Rank the options on how much
   of the current stepping loop survives, and pick from both directions: why not
   the simpler, why not the more expressive.
2. **Settle where the clock lives — the central decision.** Three coherent
   positions: the movement layer owns all time and the verb's native cost is
   suppressed; the layers own different things (the place prices the tactic, the
   verb prices the action) and both are charged; or the movement layer owns time
   only for dwell-only places and mapped places keep the substrate's price. Each
   has a different consequence for the comparability of the primary metric
   against the baseline arm, and that consequence — not elegance — should decide
   it. State the ruling in one sentence a reader cannot misread.
3. **Parameterise the rates from the existing catalogue.** Recommend that each
   tactic's current declared duration becomes the **mean** of its exponential
   draw, because that preserves every tier badge, every sweep band, and the
   group-anchor structure that keeps the parameter count identifiable. State
   what an exponential assumes — memorylessness, a mode at zero, a long tail —
   and whether that is defensible for a tactic like a slow, paced concealment
   dwell, where a heavier-shouldered distribution would arguably be more
   faithful. Where it is not defensible, say so rather than papering over it: an
   honest "exponential for tractability and precedent, acknowledged as a poor
   shape for tactic X" is a stronger position than a silent assumption.
4. **Place the confusion penalty in the net.** Design it as an entered-on-interrupt
   place carrying the substrate's own base duration under the same exponential
   regime. The trap to design against is **double-charging** — if the substrate
   still applies its own penalty on the native path and the net adds one, the
   movement arm pays twice; if the movement arm currently pays nothing, adding
   the place *removes* an asymmetry rather than creating a cost. Decide which
   world we are in first (see State of play), then specify accordingly.
5. **Write the comparability argument before writing any code.** The primary
   metric is defined over the substrate's action durations, and the baseline arm
   must remain untouched and byte-identical. Show explicitly how a movement-arm
   run's timing composes into that metric under the chosen ruling, and whether a
   cross-arm comparison remains valid, needs re-definition, or needs a second
   reported quantity. If the honest answer is that the two arms stop being
   directly comparable on the primary metric, that is a finding to state, not a
   reason to abandon the move.
6. **Specify determinism, the migration, and the rollback.** A new random stream
   with its own seed, isolated from both the substrate's dice and the existing
   token sampler, so the arms stay independently seedable. Name which tests pin
   which property, how the change is toggled, and what reverting costs.

## Validation gate

Done when a design record exists that:

1. Chooses the formalism, with the rejected alternatives and the reason each was
   rejected.
2. Rules on where the clock lives, in one unambiguous sentence, and states the
   consequence for the primary metric.
3. Specifies the per-tactic rate parameterisation, its relationship to the
   existing catalogue, and the distributional assumption — including where that
   assumption is weak.
4. Specifies the confusion-penalty place, and resolves the double-charge
   question against confirmed facts about the current behaviour rather than
   against a reading of the code.
5. Carries the written comparability argument against the baseline arm.
6. Names the determinism scheme, the test set, the migration path, and the
   rollback.
7. Lists what the implementation handoff must build, in enough detail that a cold
   session could build it without re-deriving any decision.

**And: no source file, test, or data artefact has been modified.** Confirming the
current behaviour with a throwaway probe is fine and expected; changing behaviour
is not.

## Hard constraints

- **Planning only.** The deliverable is a record. The next handoff builds.
- **The baseline arm is untouchable** — its golden is the contract with every
  prior result, and the whole comparison rests on it.
- **The justification is the deliverable, not the numbers.** Per the supervisor:
  the values are inherently arbitrary, so the defence is what has to be strong.
  The existing validity framework — tiers, anti-circularity rules,
  shape-not-scale — is the frame to write it in, not a separate concern.
- **Determinism (SIM-05)** must survive; a new random stream needs its own seed
  and must not perturb existing ones.
- **Attacker-only (D5)**; the action-set freeze (S2) still holds — timing
  semantics are not an action change, but nothing here licenses a new verb.
- Australian English; branch hygiene; never push without an explicit ask.

## Reading list

- [`../implementation/pipeline/ogasp/petri_feasibility.md`](../implementation/pipeline/ogasp/petri_feasibility.md)
  §3 (how this field uses Petri nets) and §5–§7 (the candidate encodings and the
  layered design) — the formalism groundwork already done.
- [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  §6 — the current lifecycle, determinism argument, and per-event record schema.
- [`../implementation/pipeline/ogasp/runtime_verification.md`](../implementation/pipeline/ogasp/runtime_verification.md)
  §P5 (when the verdict is read relative to the dwell) and §P8 (what the metric
  comparability rests on).
- [`../notes/ch3_design/operational_validation.md`](../notes/ch3_design/operational_validation.md)
  and [`../notes/ch2_background/tactic_duration_precedent_survey.md`](../notes/ch2_background/tactic_duration_precedent_survey.md)
  — the validity framework and the declare-and-sweep precedent this move sits in.
- `data/ogasp/tactic_durations.json` — the catalogue, including the metadata
  field that currently declares the opposite of S3 and will need changing.

## Out of scope (explicitly)

- Writing the implementation. Deliberately.
- Re-deriving the per-tactic values. They become means; recalibration is separate
  work under the existing validity framework.
- The reset-fraction parameter family. Related, argued in the tactic profiles,
  and not part of this move.
- Any change to the baseline attacker's timing.
