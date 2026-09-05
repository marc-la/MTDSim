---
status: open
created: 2026-09-05
---

# Bring the generated and appendix tables onto the house table style

## State of play

The house table style was ruled 2026-09-05 and is written up in
[`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md)
§k: one type size (`\footnotesize`), zebra rows instead of body hairlines,
rotated `\rowgroup` labels for the outer row key, `P{}` ragged-right columns,
a raised float-page threshold. It lives as three preamble macros in
`docs/thesis/dissertation.tex` (`\tablestyle`, `\rowgroup`, the `P` column
type). Every hand-set *chapter* table (2.1–2.5, 3.1, 3.2) is on it.

What is not: every table a generator in `tools/` emits, and the three
hand-typed appendix tables.

| Table | File / label | Emitter | Today |
|---|---|---|---|
| 4.1 dwell catalogue | `tables/tab_4-4a_dwell_catalogue.tex` | `tools/dwell_catalogue_tables.py` | `\footnotesize`, no stripes, two tabulars with `(a)`/`(b)` label rows |
| B.1–B.4 classification audit | `tables/tab_B-2a_…` | `tools/gasp_structural_baseline.py --tex` | `\scriptsize`, 4 pt colsep, own `A{}` column type |
| B.5 rejected partitions | `tables/tab_B-3a_…` | `tools/gasp_partition_candidates.py` | `\scriptsize`, 4 pt, own `R{}` column type |
| B.6 dwell derivation | `tables/tab_B-4a_…` | `tools/dwell_catalogue_tables.py` | `\scriptsize`, 4 pt, a `\multicolumn` footnote row |
| B.7 mapping reasons | `tables/tab_B-5a_…` | `tools/controller_mapping_figure.py` | `\footnotesize` |
| B.8–B.10 overlay weights | `tables/tab_B-6a_…` | `tools/failure_weight_decomposition_figure.py` | `\scriptsize`; B.10 is 16 columns at 2.2 pt colsep |
| B.11, C.1, C.2 | inline in `dissertation.tex` | hand-typed | `\small` / `\footnotesize` |
| D.1 preliminary extraction | `tables/tab_D-0a_…` | `tools/preliminary_extraction_table.py` | `\footnotesize`, 4 pt |

## Recommended approach

One pass, generator by generator, regenerating each fragment and diffing it:

1. Each generator emits the §k skeleton: `\tablestyle` in place of its own
   size command, `P{}` in place of its private `A{}`/`R{}` column types
   (drop the `\newcolumntype` lines — the preamble owns the type now), no
   `\cmidrule` inside a striped body.
2. Rows that are *not* data rows — the `(a)`/`(b)` panel labels in 4.1, the
   footnote row in B.6 — must not take a stripe. `\hiderowcolors` before
   and `\showrowcolors` after is the colortbl mechanism; note that a
   `\multicolumn` row still counts as a row, so the stripe parity below it
   is unaffected only if the hidden row is left in the count.
3. Tables that genuinely cannot fit `\textwidth` at `\footnotesize` keep
   `\scriptsize` + 4 pt together (§k rule 1) — B.1–B.4 and B.5 probably;
   measure rather than assume. B.10 (16 numeric columns) is the one
   candidate for `pdflscape`, which the preamble already loads.
4. The three inline appendix tables convert by hand in the same commit.
5. Update [`../thesis/FLOATS.md`](../thesis/FLOATS.md) only if a file or
   label changes (none should).

Alternative considered: leave the appendix as is on the argument that
appendix ledgers are a different genre (§e6). Rejected — Marc's ruling is
one look for every table, and the appendix is where the size discipline
matters most.

## Validation gate

- `pdflatex` clean of new overfull boxes (the three pre-existing ones at
  lines ~303, ~433, ~1944 are prose, not tables).
- Every `\begin{table}` in `dissertation.tex` and `tables/*.tex` is
  followed by `\tablestyle` and contains no `\small`, `\footnotesize`,
  `\scriptsize` of its own except a `\scriptsize` immediately after
  `\tablestyle` where rule 1 applies (`grep -n` across both).
- A page render of §B.2–B.7 shows stripes starting on the first body row of
  every table (parity check — a `\cmidrule` or an uncounted hidden row
  shifts them).
- The chapter-4 table (4.1) and Table 3.1 look like the same document.

## Hard constraints

- Generators only; never hand-edit a generated fragment (the header of each
  says so). Values still flow from tracked artefacts — this pass changes
  typography, not one number.
- The stripe colour, `black!5`, and the greys grammar are fixed (§h, §k).
- Branch / commit / push rules in
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md).

## Reading list

- [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md)
  §k — the style, and the `\cmidrule`-counts-as-a-row measurement.
- `docs/thesis/dissertation.tex`, preamble block "house table style" and
  `tab:defence-mechanisms` (Table 2.2) — the worked conversion.
- `tools/dwell_catalogue_tables.py` — the simplest generator; do it first.
- [`../thesis/FLOATS.md`](../thesis/FLOATS.md) — which generator owns which
  fragment.

## Out of scope (explicitly)

- Folding Table 2.5 into prose, or any other table-count reduction — that is
  Marc's content call (§k rule 9), flagged in the 2026-09-05 return.
- Re-drawing any figure.
