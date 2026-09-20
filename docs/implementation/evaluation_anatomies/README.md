---
status: durable
created: 2026-09-09
updated: 2026-09-09
---

# Evaluation anatomies — the section-level survey behind the evaluation conventions

**What this is.** One file per paper, recording *how that paper's evaluation is
built and reported* — the verbatim heading skeleton of its experimental portion,
everything it declares before a result, every figure and table in its results,
the claims it makes in order, its sensitivity or parameter analysis, its
discussion and limitations placement, and a closing split between what transfers
to this dissertation and what is an artefact of that paper's own purpose. Every
claim carries a page or line locator into the source.

**Why it exists.** [`../../workflows/evaluation_conventions.md`](../../workflows/evaluation_conventions.md)
states the conventions; these files are the evidence for them. A convention in
that file should be checkable here without re-reading the papers, and the census
tables there (where setup sits; what results are organised by; who declares a run
count) are counts over this directory.

**How it was built** (2026-09-09). One paper per pass, finished and written
before the next was opened, so nothing is cross-attributed — the standing
multi-paper rule in [`../../workflows/guardrails.md`](../../workflows/guardrails.md).
Never guess: a point the paper does not state is recorded as "not stated", which
is why the absence census in the conventions file is usable. Record, do not
judge: these files say what a paper does, never whether it is any good. The
scaffold is [`_template.md`](_template.md).

## What is covered

Twenty-five papers have their own file. The lineage: `brown2023`, `zhang2023`,
`ho2024`, `tay2024`. MTD evaluations the review cites: `hong2018`, `masud2025`,
`he2025`, `kim2026`, `alavizadeh2022`, `chobenasher2018`, `zaffarano2015`.
Formal-model cousins: `bland2020`, `outkin2023`, `anderson2016`, `torquato2022`,
`maleki2016`, `venkatesan2016`. Network-layer MTD: `carroll2014`, `crouse2015`,
`jafarian2015`, `wang2017rdam`, `reti2022`. Critiques and surveys, which carry a
different shape because they have no experiment of their own: `cho2020`,
`jalowski2026`. Metric-definition genre: `manadhatawing2011tse`.

Two files are not per-paper:

- [`extraction_only_sources.md`](extraction_only_sources.md) — twelve extraction
  records read for evaluation-design content, each flagged extraction-only
  because the primary is not in the repo, plus a term census across the whole
  source tree. That census is where the finding that no formal
  sensitivity-analysis vocabulary appears anywhere in the corpus comes from.
- [`timed_models_sensitivity.md`](timed_models_sensitivity.md) — a
  parameter-and-sensitivity-focused pass over the timed attack-model family
  (stochastic Petri nets, semi-Markov, the modelling-language papers), in a
  shorter per-paper block rather than the full template. **Incomplete:** four of
  the ten planned papers are written and the cross-paper synthesis section is
  not, because the pass was interrupted.

## What is not covered

The survey was cut short by a session limit, so these were planned and never
written: `cremonini2005`, `sharma2025`, `li2020`, `sun2025`, `jafarian2012`,
`alshaer2012`, `manadhatawing2011` (the companion to the TSE version),
`zhang2023drl`, `barach2026`, `ma2026`, `yuldosh2025`, and six of the ten timed
models. The sources for all of them are in the repo, so any of these is a
resumable pass against `_template.md` rather than new research.

None of the conventions in the conventions file rests on a paper in that list.
A finished pass could add exemplars; it is not expected to overturn a census,
though a count stated there would need re-checking if one did.
