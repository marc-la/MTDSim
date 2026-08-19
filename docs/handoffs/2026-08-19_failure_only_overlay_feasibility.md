---
status: open
created: 2026-08-19
---

# Feasibility: collapse the outcome overlay to a failure-only matrix

**Goal (one line).** Test Marc's 2026-08-19 idea (L4 drafting, pass 4): replace
the success/failure weight-set *pair* with a **single failure matrix** (success
= pass-through, i.e. the base flow-proportions route unchanged on a success
verdict), because "one set of values is more defendable than two".

## State of play

- Reported configuration pins **`v3_persistent_backward`** with BOTH verdict
  tables active ([`../implementation/pipeline/ogasp/demonstration_arms_prereg.md`](../implementation/pipeline/ogasp/demonstration_arms_prereg.md)).
- The overlay is rule-generated: 5 success + 9 failure rules compiled to
  210-pair views; a `verdict_blind` (both-null) ablation already exists in
  memory ([`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md) §3, §6) —
  a success-null variant is a new, third point between them.
- **The counter-argument the feasibility verdict must weigh honestly:** the
  evidence-tier asymmetry runs the OTHER way — the *success* side is the
  better-grounded half (MITRE `enables` semantics + DFIR/AAR get-in/spread
  patterns); the failure side is the declared-judgement half (§4 of the design
  record). A failure-only overlay **keeps the declared half and drops the
  attested half**. The defensibility gain Marc names (fewer declared values)
  and this inversion must both appear in the verdict.

## Recommended approach

1. Generate a `success_null` overlay variant from the existing rule model
   (success table ≡ 1.0 everywhere; failure table unchanged). No hand-set
   values — extend the generator, keep it reproducible (declared-value ledger
   rules).
2. Dry-run the pinned arms (aggregate + the four objective profiles, the
   prereg seed set) under: current pair / success-null / verdict_blind.
   Report what moves (routing distributions, sink/retrace rates, breadth,
   the experiment-2 headline directionality if cheap).
3. **Blast radius before any adoption:** every published figure is keyed on
   `v3_persistent_backward`. Number the re-run cost, ask Marc once with a
   recommendation (membership-rulings convention).
4. **Third arm (Marc, 2026-08-19): kernel-only failure via asymmetric
   decay.** Encode failure PURELY as the distance kernel with a backward
   decay that differs from the forward one (delta != gamma) --- no failure
   semantics rules at all. Already representable as a parameter
   re-declaration (delta was 0.5 before the 2026-07-28 re-declaration to
   0.25). **What it cannot express, to be checked against outcomes:** the
   failure rules are destination-aware, not just direction-aware --- the
   foothold gates (IA-failure sends foothold-dependent destinations to 0.02
   while the IA->recon bridge carries 0.9; the validated 83% mass split)
   cannot come from a uniform per-offset decay, which gives every
   destination at the same offset the same factor. If those behaviours do
   not matter to outcomes, the simplification wins and the defensibility
   story collapses to one mechanism. **Marc has a concurrent session
   exploring exactly this --- sync with it before building anything here**
   (concurrent-sessions rule: re-verify artefact freshness).
5. Verdict framed for the dissertation: does success-conditioning do work the
   base weights do not already do? If success ≈ pass-through behaviourally,
   Marc's simplification is nearly free AND the asymmetry concession
   simplifies to one declared object.

## Validation gate

A written verdict (repo record beside the overlay design) with the three-arm
comparison numbers, the evidence-tier inversion addressed, and Marc's
adopt/decline ruling recorded. The chapter paragraph (see the sibling
provenance handoff) waits on this.

## Hard constraints

- No reverse-engineering the weights to make any net traverse well (the
  CTI-independence boundary, design record §1).
- Determinism (SIM-05); versioned overlay registry — never overwrite
  `v3_persistent_backward`.
- This is feasibility + evidence, not adoption: Marc rules.

## Reading list

1. `docs/implementation/pipeline/ogasp/success_failure_overlay_design.md` (§1–§4, §6)
2. `docs/implementation/pipeline/ogasp/weight_sensitivity_study.md` (what the sweep already showed)
3. `docs/implementation/pipeline/ogasp/demonstration_arms_prereg.md` (the pinned configuration)
4. `docs/notes/ch4_methods/outcome_overlay_directionality.md` (the asymmetry argument)
5. `docs/handoffs/2026-08-19_failure_weight_provenance.md` (sibling — the decomposition presentation)
