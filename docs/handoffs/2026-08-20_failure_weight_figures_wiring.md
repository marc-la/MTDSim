---
status: open
created: 2026-08-20
---

# The failure-weight figure family — wiring under the 2026-08-20 ruling change

**Goal:** wire the failure-weight artefacts into §4.2.4.1 per Marc's 2026-08-20
ruling — **all three views in the chapter** (failure-rule kernel, the
distance/direction kernel, the aggregated committed matrix; "critical") — with
the appendix residue placed and the retired success-matrix figures removed.
Supersedes the 2026-08-19 split (chapter = committed matrix only).

## State of play

- Generated, unwired: `failure_weight_matrix.{tex,pdf}` (rule letters A–I in
  cells), `failure_weight_decomposition.{tex,pdf}`,
  `distance_kernel_bands.{tex,pdf}` — all from
  `tools/failure_weight_decomposition_figure.py`.
- **Three wiring blocks already exist, compile-checked but deliberately
  unapplied** (Marc verifies first) —
  [`../implementation/pipeline/ogasp/failure_weight_decomposition.md`](../implementation/pipeline/ogasp/failure_weight_decomposition.md)
  §5, which also carries the where-every-number-lives table. Start there;
  do not re-derive.
- `success_weight_matrix.{tex,pdf}` — **retired** (v4_failure_only ruling; the
  chapter never mentions the success matrix). Remove in the wiring commit.

## The gate before anything regenerates

**The experiment-2 re-key ruling is open** (handoffs README, first decisions
row): whether published records re-run under `v4_failure_only` or stand on `v3`
with the feasibility study as bridge. The chapter figure regenerates under
`--version v4_failure_only`; **check the ruling first** so the ch4 figure and
the ch5 numbers tell one version story. The figure caption pins the overlay
version either way.

## What goes where

- **Chapter (§4.2.4.1):** the three views. Whether that is the single
  decomposition figure or the matrix + decomposition pair depends on the
  generated panel composition — verify, then Marc rules at wiring.
- **Appendix:** `fig:distance-kernel-bands` (the declared point in its sweep
  bands), the rule ledger (A–I decode, ledger genre §e6), the kernel tables,
  and the full tactic-to-tactic weight sets (the prose already cites "the
  appendix, along with the full set…"; V6 routes the overlay declaration
  there).

## Considerations

1. **The A–I decode is mandatory** (§b2): every rule letter in a cell is an
   encoding the reader must be able to resolve — in the chapter caption, or a
   caption pointer to the appendix ledger. An undecoded letter is the corpus's
   most visible convention violation.
2. **The caveat sentence** (threat-model parameters, simulator-specific — not
   real-world values) is a must-carry beside the float, and it is **Marc's
   prose** — flag the slot, never write it.
3. **Legibility:** 15×14 cells with values + rule letters is at the §g
   anti-pattern boundary (brown2023's own 3pt labels are the named failure).
   Check printed size at inclusion width; landscape or a split is allowed,
   shrinking glyphs is not.
4. **The M3 floor-semantics flag** on the kernel paragraph remains Marc's to
   word — the bands figure draws the correct semantics; wiring must not
   silently resolve the prose flag.
5. Tactic labels: the Australianisation ruling applies before regeneration
   (parent handoff, cross-cutting).

## Validation gate

Chapter floats wired and referenced from the failure-matrix prose; appendix
residue placed with real labels; `success_weight_matrix.{tex,pdf}` gone;
overlay version pinned in every caption; A–I decoded; captions listed for
Marc's voice pass.

## Reading list

1. [`../implementation/pipeline/ogasp/failure_weight_decomposition.md`](../implementation/pipeline/ogasp/failure_weight_decomposition.md) §5 — wiring blocks + number provenance
2. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md)
3. [`../implementation/pipeline/ogasp/success_null_overlay_feasibility.md`](../implementation/pipeline/ogasp/success_null_overlay_feasibility.md) §8–9 — the v4 adoption
4. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §b2, §d7, §e6, §g
