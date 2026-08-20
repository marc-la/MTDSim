---
status: open
created: 2026-08-20
---

# The L2 classification appendix — audit table (Appendix [Y]) + rejected partitions (Appendix [X])

**Goal:** build the two appendix entries §4.2.2 already cites as placeholders:
the per-flow classification audit table (`Appendix~[Y]`, l.444) and the
rejected-partition comparison (`Appendix~[X]`, l.450 — note this is a
**different** `[X]` from §4.2.4.1's; labels assigned by the wiring handoff).

## The audit table (Appendix [Y])

- **Sources:** `data/gasp/classification.csv` + `data/gasp/metadata_audit.csv`
  (the load-bearing classification input), emitted not typed.
- **Columns (Marc's 2026-08-20 dictation, transcript-repaired):** one row per
  attack flow — flow, citation, CTID reference *(dictation had "the CGI" —
  read as the CTID blurb/ID; CONFIRM)*, terminal tactic, assigned objective
  class.
- **PROPOSAL — the override column replaces the confidence grade.** Marc mused
  "do away with the subjectivity"; recommendation: no subjective confidence
  column — carry instead *terminal-tactic read vs assigned class, and which
  cross-check source decided* (CTID blurb / ATT&CK page / vendor report). This
  discharges the recorded consistency obligation in the same stroke: **19 of
  38 land off the terminal read**, and the appendix must state the override
  rule or an examiner sees the inversion undefended. The repo record's own
  inversion history (narrative-primary; structural terminal the rejected P1)
  stays repo-side, unchanged.
- **Caption pins the Attack Flow corpus version** (read the pin from the
  tracked corpus metadata under `data/gap/`; §b5) and the 38-flow census.
- **Freshness check before emitting** (standing concurrent-sessions rule):
  the emitted classes must reproduce the validated post-ruling set —
  19 / 7 / 7 / 5, 38 / 38 high, terminal read 8 / 12 / 1 with 19 on neither
  ([`../implementation/pipeline/gasp/structural_baseline.md`](../implementation/pipeline/gasp/structural_baseline.md)).
  A mismatch is a stop-and-report, not a silent regeneration.

## The rejected partitions (Appendix [X] — §4.2.2's)

- Six alternative schemes, **one row each, why dismissed — no rubric** (ruled
  2026-08-17). The STIX ten-category taxonomy and the seven schemes detail
  land here; the chapter keeps its single sentence.
- Genre: approach-comparison table (§e2), prose cells, Ref(s). column where a
  scheme has one.
- Grounding: [`../implementation/pipeline/gasp/gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md)
  §(a) and the objective-partition notes.

## Considerations

1. **Connective prose is Marc's.** Each appendix entry needs a sentence or two
   framing the table; sessions emit the floats and flag the prose slots.
2. 38 rows × a citation column is wide — expect landscape or a two-part
   layout; citations as `\citep` keys resolving in the bibliography, not URLs.
3. The per-profile subgraph renders (Marc's 2026-08-20 "maybe") would live in
   this appendix neighbourhood **if** ruled in — gated on his ruling and on a
   prose citation existing; not part of this brief's gate.

## Validation gate

Both tables emitted from tracked artefacts under real labels; §4.2.2's two
placeholders resolve; the override-column proposal ruled by Marc (accept /
amend) before the audit table is finalised; corpus pin in the caption;
freshness check recorded.

## Reading list

1. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md)
2. `data/gasp/classification.csv`, `data/gasp/metadata_audit.csv`
3. [`../implementation/pipeline/gasp/structural_baseline.md`](../implementation/pipeline/gasp/structural_baseline.md) — the validated numbers
4. [`../implementation/pipeline/gasp/gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md) §(a), §(c)
5. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §b4, §b5, §e2
