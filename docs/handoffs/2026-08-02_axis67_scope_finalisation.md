---
status: open
created: 2026-08-02
---

# Finalise the scope of axes 6 and 7 — the two rows the freeze released

The scope freeze's perimeter was narrowed 2026-08-02
([`model_scope_freeze.md` §0](../implementation/pipeline/ogasp/model_scope_freeze.md)):
incentive rationality (axis 6) and learning capability (axis 7) were frozen
before their scope was final, and every session since freeze day has had to
argue around the record to keep working on them. This handoff is the surface
that fight moves to: the open scope decisions for both axes, each with its
evidence pointer, so Marc can rule item by item. What this handoff ships is a
set of dated rulings — the closure amendment that re-adopts both rows into the
freeze — not a build.

## State of play

**Axis 6 (incentive rationality) — badge DESIGNED, disposition X (measurement
gap).** The mechanism exists twice over: the shipped declared cost family, and
the iterated cost model that repairs its R2 instrumental-value defect
([`iterated_cost_model.md`](../implementation/pipeline/ogasp/iterated_cost_model.md)).
The repair reaches the defect — the blocked-fraction rise is 73–89 % undone in
the pooled `v2_partial` cells and successes per attempted action roughly
double — and misses its own per-profile bar (U2: 3 of 30 cells CI-disjoint; the
stopping rule was honoured, nothing re-specified). The conclusion that would
have moved the badge (U3) was passed on the bare threshold by the `declared`
arm, which F6 proved cannot see MTD at all, so the badge was declined and the
axis now has no instrument in hand that can score it — its third measurement
failure. One measured surprise travels: change B (benefit through the profile's
own net) costs no plurality at all, the sole exception to "every modulator
narrows traversal".

**Axis 7 (learning) — badge DESIGNED, gap narrowed to the credit signal
alone.** The learner was re-keyed on `(destination tactic,
precondition-satisfied?)` and swept over 4 600 runs
([`learning_readiness_findings.md`](../implementation/pipeline/ogasp/learning_readiness_findings.md)):
the representational defect was real and is repaired, and the repaired learner
returns to — never past — the no-learning ablation arm (4.52 vs 4.60 hosts).
The sole remaining requirement is a progress-carrying credit signal, which the
freeze had classed a research project in itself; whether it is one this project
takes on is exactly the scope question still open.

## The scope decisions to take

Axis 6:

1. **Change B's standing.** The findings record ranks this first: cheap,
   stateless, costs no plurality, surrenders none of F6's precomputability, no
   claim attached ([`iterated_cost_model.md`](../implementation/pipeline/ogasp/iterated_cost_model.md)
   §8). Decide: a labelled arm in the model's configuration set, or recorded
   and shelved. (Change A failed its half of the repair — the brief's ranking
   inverted — so its standing is part of the same ruling.)
2. **The instrument.** Decide: build a validated MTD-sensitivity statistic
   (negative-control-gated before it can carry a badge, per §8.3), or accept
   the axis-1-shaped ending — mechanism runs, nothing in hand can score it —
   as the reported result.
3. **The enabling-condition arm.** One targeted arm at non-zero λ against the
   non-dwell-proportional defences above the operating mutation interval — the
   condition the axis's own record named as a route to a stronger badge.
   Decide whether the 2026-08-02 S2 clearance extends to it or a fresh ask is
   needed.
4. **U2 powering.** Ten seeds per profile cell cannot separate a difference of
   the measured size; the direction is consistent in 17 of 30 cells and pooled
   separation exists on `v2_partial`. Decide whether settling it is worth the
   runs — the record bars *re-specifying* U2, not powering it.

Axis 7:

5. **The credit signal: in scope or future work.** The one decision that
   changes what the remaining sessions build. If in: it is designed on the
   readiness key rather than the marginal
   ([`learning_readiness_findings.md`](../implementation/pipeline/ogasp/learning_readiness_findings.md)
   §4), stays inside the no-RL constraint (no eligibility trace, no discount
   factor, no value function), and the badge criterion is fixed in advance —
   breadth or stage advance must beat the 4.60-host ablation arm, no
   scoring-driven design.

Joint:

6. **Composition.** Change A and the readiness learner condition on the same
   readiness bit against the same artefact; any combined configuration is
   barred until a fresh joint check runs
   ([`modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md)).
   Decide whether that check is in scope.

## Validation gate

Each numbered item carries a dated ruling recorded against it in this file (in
/ out / deferred, with a sentence of why). When all six are ruled, the freeze
record takes its dated closure amendment re-adopting axes 6 and 7
([`model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)
§6), and this handoff is deleted in that commit.

## Hard constraints

- **S2 is the supervisor's ruling** and was cleared for the iterated-cost
  experiment specifically
  ([`supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md));
  an open scope licenses deciding, not building past it.
- **No-RL hard constraint** on any axis-7 design: no eligibility trace, no
  discount factor, no value function.
- **S6: badges move on evidence only** — never change the model, weights,
  mapping, or metrics to improve a row
  ([`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)).
- **The §4 pin holds regardless**: the reported headline configuration runs
  modulators null; any modulator-active arm is its own labelled arm.
- **No re-reading of recorded experiments** — the frontier, experiment 2 and
  the axis sweeps stand as records of the model they ran under.
- Branch, commit and push rules per
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md).

## Reading list

- [`model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)
  — §0 (the perimeter amendment), §2 rows 6–7, §5b.
- [`iterated_cost_model.md`](../implementation/pipeline/ogasp/iterated_cost_model.md)
  — §§7–8: what the sweep licenses and what a successor should do.
- [`learning_readiness_findings.md`](../implementation/pipeline/ogasp/learning_readiness_findings.md)
  — §4: the successor item the credit signal builds on.
- [`cost_model_plain.md`](../implementation/pipeline/ogasp/cost_model_plain.md)
  — §2.2a: the R2 defect the iterated model repairs.
- [`apt_model_criterion.md`](../implementation/apt_model_criterion.md) — axes 6
  and 7: the badge criteria that stay fixed while scope is decided.

## Out of scope (explicitly)

- **No build ships from this handoff.** It exists to produce rulings; each
  ruled-in item becomes its own brief or lands under its own pre-registration.
- **Axes 1–5 and 8** — still frozen; nothing here touches them.
- **Re-specifying U2** or relaxing any pre-registered criterion — the stopping
  rule fired and the result stands as measured.
