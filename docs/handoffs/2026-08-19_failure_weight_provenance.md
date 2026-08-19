---
status: open
created: 2026-08-19
---

# Cement the failure weight set's provenance — the decomposition presentation

**Goal (one line).** Make the failure tactic-to-tactic weight set defensible on
the page (Marc, 2026-08-19: "right now it's not in a defensible position"), via
his decomposition idea: present the failure matrix as **(declared failure
kernel) × (lifecycle-distance kernel) → aggregated matrix**, decomposed then
aggregated, "so it is very clear how they got their results" — feeding a new
§4.2.4.2 paragraph Marc will dictate from it, plus the appendix table.

## State of play

- The record ALREADY has this structure — the presentation, not the mechanism,
  is what is missing: 9 failure semantic rules (gates / dampers / relationship
  defaults, one rationale each; `outcome_rules.json`) × the consensus distance
  kernel (γ = δ = 0.25, floor z = 0.1) compiled to 210-pair views; generator
  reproduces the table 0/123; adversarial-scrutiny ledger at
  `declared_value_provenance.md`.
- **Discrepancy to resolve first (Marc asked for the verification; flagged in
  the tex):** his dictated narrative penalises ONE stage away; the declared
  kernel does not (Δ = 1 → d = 1.0; penalisation starts at two stages: 0.25,
  then 0.0625 → 0 under the floor). His "and if not, that's how it should be
  done" is a candidate **re-declaration** — if he re-declares the kernel, the
  weight sensitivity study re-runs (its sweep bands were over the current
  form) and the fold-in re-compiles. Ask once, with a recommendation.
- The four consensus stages are preparation / intrusion / post-intrusion
  operations / objective; citation set now live in the bib
  (hutchins2011, alshamrani2019, mandiant2013, chemat2024; Ussath via
  Alshamrani's channel).

## Deliverables

1. **The decomposition artefact:** failure kernel (semantics-only values),
   distance kernel (stage-offset values), and the aggregated failure matrix,
   shown as three aligned 15×14 views (diagnostic register: no accentuation;
   uniform scales across the three panels). A generator script under `tools/`,
   never hand-drawn numbers.
2. **A repo record** (beside the overlay design) walking one or two pairs
   end-to-end: rule fired → distance applied → final value.
3. **Chapter inputs:** a content-point scaffold for the owed §4.2.4.2
   failure-encoding paragraph (Marc dictates; no prose), and the appendix
   table wiring (the full weight sets — the chapter already points at it).
4. The kernel-discrepancy ruling recorded (keep as declared / re-declare).

## Validation gate

Marc can answer "how did you get these failure values?" by pointing at the
decomposition figure and the two-pair walkthrough; the §4.2.4.2 paragraph slot
has its scaffold; the appendix artefact exists or is precisely specified.

## Hard constraints

- Values remain rule-generated and reproducible; no per-cell hand edits.
- Sweeping defends declared values, never produces them (declare-then-sweep,
  V6) — the presentation must not imply the sweep generated the numbers.
- Viz: no accentuation; uniform filtering/scales across compared panels.

## Reading list

1. `docs/implementation/pipeline/ogasp/success_failure_overlay_design.md` (§2 the rules; §3 compilation)
2. `docs/implementation/pipeline/ogasp/lifecycle_consensus.md` (§4 stages; §6 the kernel)
3. `docs/implementation/pipeline/ogasp/weight_sensitivity_study.md` (fold-in + sweep)
4. `docs/implementation/declared_value_provenance.md` (ledger discipline)
5. `docs/handoffs/2026-08-19_failure_only_overlay_feasibility.md` (sibling — run first or together; a failure-only ruling changes deliverable 1's shape)
