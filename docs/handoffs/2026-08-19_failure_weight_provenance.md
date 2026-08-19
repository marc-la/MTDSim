---
status: open — deliverables 1–3 shipped 2026-08-19; only the kernel ruling (deliverable 4) remains, Marc's
created: 2026-08-19
updated: 2026-08-19
---

> **State 2026-08-19 (session close).** Shipped:
> `tools/failure_weight_decomposition_figure.py` → `docs/thesis/figures/failure_weight_decomposition.{tex,pdf}`
> (three aligned 15×14 panels, stage-grouped, one grey scale, every cell printed:
> failure kernel × distance kernel → committed set) and
> `docs/thesis/tables/outcome_overlay_weights.tex` (both rule ledgers, the kernel
> parameters, the complete success + failure sets, v3); the record
> [`../implementation/pipeline/ogasp/failure_weight_decomposition.md`](../implementation/pipeline/ogasp/failure_weight_decomposition.md)
> (two-pair walkthrough §2; §4.2.4.2 scaffold §5.1; the appendix wiring block
> §5.2, compile-checked in a scratch copy, **not applied** to the tex — Marc:
> "don't wire into my thesis before I verify"; the sweep's honest status as
> ch5 backing §6). **Open:** the kernel-discrepancy ruling, record §4 —
> keep-as-declared recommended; the re-declaration costed there (132/210
> failure cells move, 44 newly zero, the bridge 0.9 → 0.225, 28 mass-carrying
> edges hard-suppressed, v4 + re-sweep). Delete this handoff when Marc rules
> and the ruling is recorded in the record and the tex comment.

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
