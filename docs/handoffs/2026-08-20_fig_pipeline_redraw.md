---
status: open
created: 2026-08-20
---

# The chapter-opening pipeline figure — redraw to the thesis ladder

**Goal:** draw the box-and-flow pipeline figure (V7) that replaces the
commented-out `fig:pipeline` placeholder (`movement_controller_action.png`) at
the ch4 opening. **(Re-flagged 2026-08-20: the existing pipeline diagram is
too large — rework, not reuse.)**

## Why this figure is load-bearing

**This figure is the definition of the thesis ladder** (ratified 2026-08-16):
L0–L1 intelligence→graph, L2 profiles, **L3 = the GSPN formalism, L4 = the
attacker-agent traversal in MTDSim**, and evaluation carries **no layer
number**. The §4.2 preamble deliberately does not re-narrate the ladder — the
figure owns it. Two consequences:

1. **Thesis numbering only.** The repo's numbering (repo-L3 = OGASP traversal,
   repo-L4 = evaluation) must not leak into the drawing; the divergence is
   recorded once in [`../implementation/architecture.md`](../implementation/architecture.md)
   §(b) and neither document family is "corrected" to the other.
2. **The caption does definitional work** — long, self-contained, and owed
   Marc's voice pass with more care than any other §4.2 caption. The preamble's
   live sentence ("L0 to L2 are structure, L3 and L4 are semantics and
   parameterisation, and execution…") is what the drawing must agree with.

## Spec

Genre §d1 — plain rectangles, left→right in ladder order, stage labels, no
icons. Per-stage content kept to a phrase (the "too large" complaint is about
detail: the mechanics belong to the model/data-flow diagram, not here). Grey
ramp + accent; `\textwidth` inclusion.

## Considerations

1. Keep it disjoint from the model/data-flow diagram's job: this figure is the
   *ladder* (what the stages are); that one is the *runtime loop* (how L4
   runs). Duplicated content between them is the current placeholder's failure
   mode.
2. Evaluation drawn as manipulation of the L4 object — visually subordinate,
   never a fifth rung.
3. Retire `movement_controller_action.png` in the same commit that wires the
   replacement.

## Validation gate

`fig:pipeline` live (uncommented) with the generated graphic; the preamble's
`Figure~\ref{fig:pipeline}` resolves; no repo-numbering leak; placeholder PNG
retired; caption flagged for Marc's voice pass.

## Reading list

1. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md)
2. `docs/thesis/dissertation.tex` — the ladder comment block (~l.206–237) and the preamble
3. [`../implementation/architecture.md`](../implementation/architecture.md) §(b) — the numbering divergence record
4. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §d1, §h
