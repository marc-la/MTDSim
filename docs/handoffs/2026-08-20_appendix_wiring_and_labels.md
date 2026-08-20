---
status: open
created: 2026-08-20
---

# Appendix wiring and labels — the plumbing the other §4.2 components hang off

**Goal:** the structural pass that lets every other figure/table handoff land
cleanly: appendix chapters created, labels assigned, placeholders resolved,
list-of-floats hygiene. **Run this early** — the content handoffs need the
labels.

## The work

1. **Resolve the double `Appendix~[X]`**: §4.2.2 l.450 (rejected partitions)
   and §4.2.4.1 l.738 (experiment-1 poor-performance record) are distinct
   entries sharing a placeholder name. Assign distinct `\label`s; fix both
   prose refs and `Appendix~[Y]` (l.444) in the same pass.
2. **Create the appendix chapters the ledger needs** (against the existing
   `app:proposal` / `app:sensitivity` / `app:cooccurrence`): homes for the L2
   classification tables, the dwell derivation, the weight sets + ledgers, the
   full technique graph, the experiment-1 record. Whether these are one
   "supplementary material for the movement attacker" chapter with sections or
   several chapters is **Marc's ordering/structure call — ask once with a
   recommendation** (recommend: one chapter, sectioned in pipeline order, so
   the appendix mirrors §4.2's spine; `app:sensitivity` stays its own).
3. **`Figure~[data-flow]` → real label** once the model-diagram handoff lands
   its figure (coordinate; the label can be reserved here).
4. **Amend stale tex comments** the rulings superseded: the `[data-flow]` slot
   comment's "and the L3 figure" clause (L3 ruled figure-free 2026-08-20).
5. **List-of-floats hygiene**: long decoding captions flood the Lists of
   Figures/Tables — give every float a `\caption[short]{long…}` short form
   (`\listoffigures` and `\listoftables` are both already in the preamble;
   verified 2026-08-20).
6. **The subcaption decision** (conventions §i): only if some float actually
   uses lettered subfigures. `fig:l1-graph` draws its panel letters in-TikZ —
   recommend keeping that pattern family-wide and *not* loading `subcaption`,
   so the decision closes rather than lingers. Record the ruling in
   `figure_table_conventions.md` §i either way.
7. **The experiment-1 poor-performance entry itself** (the §4.2.4.1
   `Appendix~[X]`): distil from
   [`../implementation/pipeline/ogasp/experiment_01_findings.md`](../implementation/pipeline/ogasp/experiment_01_findings.md)
   — the `v1_ckc_total` forced-total mapping's friction/churn numbers, brief,
   floats + flagged prose slots (Marc's framing sentences). It rides this
   handoff because it is small and label-bound; promote to its own brief only
   if it grows.

## Considerations

1. Appendix chapters render after `app:proposal` (the included PDF) — check
   `\includepdf` page-numbering interaction once real chapters follow it.
2. Every new subtree/label scheme is a one-commit change with the refs that
   consume it — never leave a half-wired state across commits (concurrent
   sessions read the tex).
3. `pdflatex` clean after each wiring commit is the cheap invariant.

## Validation gate

No `Appendix~[X|Y]` or `[data-flow]` placeholder left in §4.2; chapter
structure ruled by Marc and built; short captions present on wired floats;
subcaption ruling recorded; compile clean.

## Reading list

1. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md) — the ledger this wires
2. `docs/thesis/dissertation.tex` — the appendix skeleton (l.993+) and the placeholder sites
3. [`../implementation/pipeline/ogasp/experiment_01_findings.md`](../implementation/pipeline/ogasp/experiment_01_findings.md)
4. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §c, §i
