---
status: open
created: 2026-08-20
---

# The dwell-time catalogue — chapter table, appendix derivation, exponential entry

**Goal:** three artefacts from one declared family **(ruled 2026-08-20)**: the
in-prose dwell parameter table (§4.2.4.1), the appendix dwell-derivation table
(debt dictated 2026-08-19 — the prose already points: "You can see the appendix
for this"), and the exponential-shape justification entry in `app:sensitivity`.

## Sources

`data/ogasp/tactic_durations.json` (the declared catalogue). Derivation
rationale from the record: the anchor-verb / multiplier / shape reasoning per
tactic ([`../implementation/pipeline/ogasp/`](../implementation/pipeline/ogasp/)
timing records; the §4.2.4.1 prose narrates the tiering — verb constants where
sufficient, multipliers where not, judged shape otherwise; e.g. 45.0 s = 10×
the exploit shape; resource-development 0 s as off-network).

## The chapter table (§4.2.4.1)

- Parameter-table genre (§e3): booktabs, tactic rows **in shared tactic-axis
  order**, value column right-aligned, units bracketed, distribution stated as
  math (`Exp(mean)` semantics as the record words it).
- Emitted by a `tools/` script from the JSON — **no value typed** (conventions
  §h generalises the L3 no-value-typed rule).
- **The caveat sentence beside it is a must-carry and is Marc's prose**: model
  parameters anchored to this simulator, not real-world measurements. Flag the
  slot.
- Keep it minimal (tactic | dwell | note-at-most); the *why* lives in the
  appendix table.

## The appendix derivation table

Columns (proposal, Marc rules): tactic | anchor (verb/constant) | multiplier |
declared value | shape rationale. Footnote row for provenance (§b4). The
vocabulary discipline is load-bearing: values are **declared and justified
against the literature — never "calibrated", never "from the literature"**
(standing ruling; the operational_validation "calibrated" vocabulary is
aspirational and stays out).

## The exponential entry (`app:sensitivity`)

**(Ruled 2026-08-20:** how the exponential was settled is additional
sensitivity analysis, not chapter prose.**)** The chapter keeps its live
declaration + stochastic-evidence citations (`holm2014, madan2004, bland2020` —
the VERIFY-the-subset flag on those is Marc's, still open). The 2026-08-19
ruling already routes the sweep pointer to the appendix; the standing V6
tension (results preamble vs appendix for swept parameters) is recorded as
Marc's to reconcile — **do not re-open**. A sweep-wiring handoff remains a
MAYBE (his 2026-08-19 "leave that as a handoff as well") — owed when this
appendix is actually built.

## Considerations

1. Zero-dwell rows (resource-development 0 s) need a formatting decision that
   doesn't read as missing data — "0" with the off-network footnote, not a dash.
2. Same-verb-different-dwell is the table's quiet argument (different tactics
   sharing an anchor still carry different times) — the derivation table's
   multiplier column is what shows it; don't collapse those rows.
3. Artefact freshness: emit at build time from the tracked JSON; concurrent
   sessions mutate `data/` (standing rule).

## Validation gate

Chapter table wired in §4.2.4.1 with the caveat slot flagged for Marc; appendix
derivation table placed with a real label the prose's "see the appendix"
resolves to; exponential entry drafted as structure + numbers (prose Marc's);
every value traceable to the JSON or the record.

## Reading list

1. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md)
2. `data/ogasp/tactic_durations.json`
3. [`../implementation/pipeline/ogasp/`](../implementation/pipeline/ogasp/) — `stochastic_timing_design.md`, `operational_validation.md` (vocabulary boundary)
4. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §e3, §b4, §h
