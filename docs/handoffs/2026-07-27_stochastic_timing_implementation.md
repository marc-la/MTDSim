---
status: open
created: 2026-07-27
---

# Implement the stochastic timing regime — per-tactic exponential firing owned by the movement layer, dwell-only tactics that consume time, and the confusion penalty as a net place, built to the design record and validated against the untouched baseline

**Chain position: wave 3 — strictly after the timing design.** This handoff has
no authority to make design decisions; if a question arises that the design
record does not answer, the answer goes back into that record first. Executes
the build half of **S3**.

## State of play

**The design record is the specification.** It was written as a separate handoff
precisely so that the decisions — formalism, where the clock lives, the rate
parameterisation, the penalty place, the comparability argument, the determinism
scheme — are settled and reviewable before any code exists. Read it as the
contract. If it turns out to be under-specified, that is a defect in the record,
and the correct response is to fix the record rather than to improvise in code
and document afterwards.

**What is being replaced.** Time on the movement arm currently comes from a fixed
per-tactic dwell taken from the catalogue plus the dispatched verb's native cost;
the dwell is interruptible, and an MTD interrupt propagates to the driver as a
failure verdict. After this change, the per-tactic time is a draw from a
declared exponential rather than a constant, dwell-only tactics consume time
without dispatching anything, and the confusion penalty exists as a place in the
net.

**One artefact will contradict itself until this lands.** The duration
catalogue's own metadata declares its values to be plain per-state dwell and
explicitly *not* stochastic firing rates, citing the deferral that S3 has now
reversed. Updating that metadata — and the test that guards the catalogue's
shape — is part of this work, not a tidy-up afterwards.

**The tests that already exist are the safety net.** Determinism is pinned, the
native baseline's golden headline is pinned, and the four layer seams each have a
check that fails loudly if a future edit blurs them. Timing changes are exactly
the kind of edit that blurs seams — putting time on the movement layer must not
put simulation-library dependencies into the controller, and must not give the
net knowledge of verdicts.

## Recommended approach

1. **Build the draw first, in isolation, and test it as a distribution.** A
   seeded generator that turns a declared per-tactic mean into a draw, with its
   own random stream. Test it the way a distribution is tested: over many draws
   with a fixed seed, the empirical mean recovers the declared mean within a
   stated tolerance, and the same seed reproduces the same sequence exactly.
   Doing this before wiring keeps a statistical bug from hiding behind an
   integration bug.
2. **Wire it at the single point where time is currently taken**, so the change
   is one seam rather than several, and so reverting is a one-line proposition.
3. **Make dwell-only places pay time and produce no verdict** — the behaviour the
   controller rebuild made legal, now given its cost. The event record must
   distinguish a dwell-only step from an action step, or the action-budget
   decomposition that made the first experiment legible stops working.
4. **Add the penalty place exactly as specified, and prove the charge is single.**
   The failure mode to test for is paying twice — once through the substrate's own
   interrupt handling and once through the net — or, if the movement arm
   currently pays nothing, silently continuing not to. A test that counts penalty
   charges per interrupt on both arms is the cheapest guard.
5. **Re-verify the comparability claim empirically, not by argument.** The design
   record makes the case on paper; a run should show that the metric on the
   baseline arm is unchanged and that the movement arm's metric composes as the
   record predicts. If they disagree, the record wins and the code is wrong —
   or the record's argument had a hole, which is a finding worth recording.
6. **Update the documentation in the same commit as the behaviour.** The
   catalogue metadata, the provenance row's duration-regime disposition, the
   runtime lifecycle description, and the validity note's revisit condition all
   describe the old regime today.

## Validation gate

Done when:

1. Per-tactic times are drawn from the declared distribution, with a test that
   recovers the declared mean over many seeded draws and a test that the same
   seed reproduces the same sequence.
2. The native baseline reproduces its golden headline exactly — the arm is
   untouched, demonstrably.
3. Dwell-only tactics consume time, dispatch nothing, produce no verdict, route
   on base weights, and are distinguishable in the event records.
4. The confusion penalty is charged once per interrupt, and the two arms' penalty
   behaviour is stated and tested, whether or not they are made identical.
5. Determinism holds end to end, and the new random stream is isolated — it
   neither reads nor perturbs the substrate's dice or the token sampler.
6. The four seam invariants still pass.
7. The full test suite is green, and every document that describes the old timing
   regime is updated in the same commit — catalogue metadata included.

## Hard constraints

- **Build to the design record; do not re-decide in code.** Any gap goes back to
  the record first.
- **The baseline arm's timing is untouchable.** Its golden is the contract with
  every prior result.
- **Determinism (SIM-05)** and **attacker-only changes (D5)**.
- **The action-set freeze (S2) still holds.** Timing semantics are not an action
  change, and nothing here licenses a new verb or attacker state.
- No re-baselining a golden without Marc's explicit call; never bypass a failing
  pre-commit hook. Australian English; branch hygiene; never push without an
  explicit ask.

## Reading list

- **The design record — the specification** (shipped 2026-07-28, replacing the
  design handoff):
  [`../implementation/pipeline/ogasp/stochastic_timing_design.md`](../implementation/pipeline/ogasp/stochastic_timing_design.md).
  Read §7 (the build checklist) and §0 (the probe-confirmed state of play — note
  the penalty-asymmetry premise is now stale, so the penalty place must *preserve*
  single-charge, not establish it) before anything else.
- [`../implementation/pipeline/ogasp/runtime_verification.md`](../implementation/pipeline/ogasp/runtime_verification.md)
  — the four seam invariants and their checks; §P5 for where the dwell sits in the
  step lifecycle.
- [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  §6 — the lifecycle, determinism argument, and event-record schema being changed.
- `data/ogasp/tactic_durations.json` and its guard test — the artefact whose
  declared semantics this work inverts.
- [`../implementation/provenance.md`](../implementation/provenance.md) — the
  duration-regime row and the confusion-penalty row.

## Out of scope (explicitly)

- Recalibrating the per-tactic values. They become distribution means at their
  current magnitudes; calibration is separate work under the existing validity
  framework.
- Changing the distribution family per tactic, unless the design record specifies
  it.
- The reset-fraction parameter family.
- Running the comparative experiment — that is experiment 2.
