---
status: open
created: 2026-08-20
---

# The preliminary-extraction appendix entries — `app:cooccurrence`

**Goal:** fill the existing `app:cooccurrence` appendix chapter with the two
brief entries §4.2.1 already cites: the co-occurrence mining runs (single-digit
edge counts above a confidence threshold) and the keyword-mining/regex tests
(poor fidelity). **(Ruled 2026-08-20: keep — the entry is load-bearing; the
abandonment claim cites `\ref{app:cooccurrence}`.)**

## State of play

- The chapter stub exists (dissertation.tex ~l.1023) with the owed-entries
  comment; the §4.2.1 citation is live prose, so this appendix is the one
  §4.2 placeholder already carrying a real label.
- **The numbers are not yet pinned.** The prose comment says "80 % confidence
  threshold — CONFIRM"; the runs predate the current pipeline layout (early
  GAP-era work, likely on `feat/gap-schema`-era artefacts or in git history).

## Approach

1. **Locate the run artefacts first**: search the repo record and git history
   for the co-occurrence and keyword-mining outputs (edge counts, thresholds,
   the fidelity judgement's evidence). The research-record annal
   ([`../implementation/research_record/`](../implementation/research_record/))
   and the GAP investigation records are the places to look before any re-run.
2. **If the numbers cannot be recovered, re-run minimally** — enough to pin
   the two claims the chapter makes (edge counts at threshold; the
   poor-fidelity examples), with the script committed so the entry is
   reproducible. Flag before re-running: a re-run on today's corpus snapshot
   may not reproduce the historical numbers, and the entry must then say which
   it reports.
3. Each entry: a small table or a short numbers paragraph slot + Marc's
   framing prose (flagged, never written). Brief is the ruling — these anchor
   an abandonment claim, they do not relitigate it.

## Considerations

1. **The 80 % CONFIRM is the gate**: the threshold cited must come off an
   artefact or a recovered record, not the comment's memory.
2. Version-stamp what the runs consumed (corpus snapshot, ATT&CK pin) in the
   entry — dated evidence, per the annal's own rule.
3. NLP-class approaches were ruled out *as a class* in the prose with
   citations — this appendix covers only the two attempted approaches; don't
   let it grow a survey.

## Validation gate

Both entries drafted (floats + flagged prose slots); every number traced to an
artefact, a recovered record, or a committed re-run script; the 80 % CONFIRM
resolved; the §4.2.1 citation reads correctly against the finished entries.

## Reading list

1. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md)
2. `docs/thesis/dissertation.tex` §4.2.1 + the `app:cooccurrence` stub comment
3. [`../implementation/research_record/`](../implementation/research_record/) — the annal (prompt-dated evidence of the early extraction work)
4. [`../implementation/pipeline/gap/gap_schema.md`](../implementation/pipeline/gap/gap_schema.md) — construction decisions context
