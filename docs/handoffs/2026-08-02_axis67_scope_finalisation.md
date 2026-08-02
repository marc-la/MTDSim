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
   **Informed by [`learning_mechanism_feasibility.md`](../implementation/pipeline/ogasp/learning_mechanism_feasibility.md)
   (2026-08-02)**, which scores thirteen candidates against a first-principles
   rubric and finds the credit signal materially cheaper than "a research
   project" — the progress-carrying outcome tag is already computed and is
   projected to a bit in the seam (§4.1, Escape B).
7. **Type-disciplined forgetting (new, axis 7).** The ρ rule decays the
   *tradecraft* belief, which the literature says MTD cannot touch, while the
   perishable capability cursor is already handled separately. Decide whether to
   re-declare ρ by knowledge type. Note this is a **declared-value change with a
   literature justification**, and that the un-decayed arm is the only place in
   the 4 600-run sweep where the learner beats no-learning with CI separation
   (feasibility study §§3.1, 5) — which makes it both the cheapest candidate and
   the one most exposed to post-hoc-selection risk. Any use needs a fresh
   pre-registration, never a re-reading.
8. **Seed count (new, cross-cutting).** Four successive sweeps have failed to
   separate adjacent arms at ten seeds; the power calculation puts a 0.7-host
   difference at ~45 seeds (feasibility study §7). Decide whether to concentrate
   seeds on the decision cells. Raising *n* on an unchanged metric is not
   scoring-driven design, but it should be ruled on rather than assumed.
9. **The declared-bias control arm (new, axis 7).** The C3 test — does the
   learner differ from the best static modulator built from its own declared
   inputs? Cheap, S6-clean, never run, and the shipped mechanism plausibly fails
   it. Decide whether it runs before any further build.

Joint:

6. **Composition.** Change A and the readiness learner condition on the same
   readiness bit against the same artefact; any combined configuration is
   barred until a fresh joint check runs
   ([`modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md)).
   Decide whether that check is in scope.

## Rulings taken

### 2026-08-02 — item 5 ruled by Marc: the learner is a tested negative, not the default

**Ruling.** Static weights remain the default for the attack model. The learning
capability is **not deleted and not promoted** — it is maintained as a built,
declared, ablatable arm carrying a measured negative. No further implementation
effort on axis 7 mechanism.

**Why this is a position rather than a retreat.** The reported headline
configuration already ran modulators null (the §4 pin), so nothing changes in what
is reported. What the capability carries is evidence: an attacker rewarded for
*permitted* actions optimises away from its objective, measured at rank
correlation +0.921 with permission and −0.027 with progress, and the repair that
corrects the signal inverts that to +0.778
([`../implementation/pipeline/ogasp/progress_credit.md`](../implementation/pipeline/ogasp/progress_credit.md) §2).
Ablating the capability would delete the evidence for a claim the discussion
chapter has already committed to, not simplify the model.

**What remains open on this axis is measurement, not mechanism** — see the
evidence-resolved items below and §6 of the findings record.

### 2026-08-02 — items 7, 8 and 9 resolved by evidence rather than by ruling

- **Item 7 (type-disciplined forgetting): do not adopt.** U5 refuted it *with CI
  separation and in the opposite direction* on the decision cell — ρ = 0 gives
  1.06 ± 0.18 hosts against ρ = 0.5's 1.49 ± 0.19. The literature argument
  (tradecraft is durable) was sound about what an operator retains and wrong about
  the object it was applied to: a within-run frequency estimate keyed on
  tactic-places is not tradecraft, and a learner that never forgets stays
  committed to a policy the defence has already invalidated. **Had this been ruled
  on the earlier reasoning it would have been ruled incorrectly.**
- **Item 8 (seed count): superseded by a better finding.** The sweep ran 50 seeds
  from the power calculation and adjacent arms still did not separate — but the
  arms share seeds, and comparing arm means with independent CIs discards the
  pairing at a cost of 2.0× in variance. The question is no longer "how many
  seeds" but "paired or unpaired", and the answer is paired, pre-registered in
  advance ([`../implementation/pipeline/ogasp/progress_credit_findings.md`](../implementation/pipeline/ogasp/progress_credit_findings.md) §8).
- **Item 9 (declared-bias control): built and run.** It answers with a
  mapping-dependent verdict — the accumulated belief is indistinguishable from an
  aggression-matched static bias on `v2_partial` and clearly separated from it on
  `v1_ckc_total`. That is now the axis's live question, and it is better-posed
  than "does the attacker win".

**Items 1–4 and 6 (axis 6) remain open and unruled.**

## Validation gate

Each numbered item carries a dated ruling recorded against it in this file (in
/ out / deferred, with a sentence of why). **Four of nine are now settled — see
"Rulings taken" above: item 5 by Marc's ruling, items 7–9 by evidence.** When all
nine are ruled, the freeze
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
- [`learning_mechanism_feasibility.md`](../implementation/pipeline/ogasp/learning_mechanism_feasibility.md)
  — the axis-7 rubric, the four structural constraints, and the thirteen scored
  candidates. Read §§6, 8, 9 before ruling on items 5, 7 and 9.

## Out of scope (explicitly)

- **No build ships from this handoff.** It exists to produce rulings; each
  ruled-in item becomes its own brief or lands under its own pre-registration.
- **Axes 1–5 and 8** — still frozen; nothing here touches them.
- **Re-specifying U2** or relaxing any pre-registered criterion — the stopping
  rule fired and the result stands as measured.
