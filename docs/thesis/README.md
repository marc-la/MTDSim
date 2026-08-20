# CITS4010 Honours Dissertation — boilerplate

Adaptive Moving Target Defence for Dynamic Networks
Marc Labouchardiere (23857377) — Supervisor: Dr Jin B. Hong — CSSE, UWA

Built on the UWA `cshonours` class. The title page has been reworked to add
the UWA crest and a `Supervised by` line, in the style of the sample thesis,
while keeping the cshonours look for the body (chapter headings, TOC, abstract
and acknowledgements pages, submission statement).

## Files

| File | Purpose |
|------|---------|
| `dissertation.tex` | Main document — edit this (renamed from `main.tex`). |
| `cshonours.cls` | UWA honours class; title page modified (changes tagged `%mtd`). |
| `references.bib` | Bibliography (renamed from `cshonours.bib`); replace the seed entries. |
| `uwa-crest.png` | UWA crest used on the title page. |
| `figures/` | Figures (`\graphicspath` points at it). Generated figures carry their generator: the four appendix attack graphs (`gap_flow_exemplar`, `gap_technique_graph`, `gap_technique_core`, `gap_tactic_graph`, each `.{tex,pdf}`) are written by `tools/gap_appendix_figures.py` from `data/gap/gap_v0.5.json` + `data/gap/flows/` — they replaced `l1_attack_graph.{tex,pdf}`, deleted 2026-08-20 on Marc's ruling; `failure_weight_matrix`, `failure_weight_decomposition` and `distance_kernel_bands` (`.{tex,pdf}`; `success_weight_matrix` is the retired pre-2026-08-19 success table, kept as a record and not wired) by `tools/failure_weight_decomposition_figure.py` from the outcome rules + lifecycle consensus + the routing nets through the tracked compiler and net loader — regenerate, never hand-edit. |
| `tables/` | Generated table fragments to `\input` (e.g. `objective_classification_audit.tex` from `tools/gasp_structural_baseline.py --tex`; `outcome_overlay_weights.tex` from `tools/failure_weight_decomposition_figure.py`); do not hand-edit. |

## Compile

```bash
latexmk -pdf dissertation.tex
```

Or manually:

```bash
pdflatex dissertation
bibtex dissertation
pdflatex dissertation
pdflatex dissertation
```

## Changing the front matter

Edit these commands in the preamble of `dissertation.tex`:

```latex
\title{Adaptive Moving Target Defence\\ for Dynamic Networks}
\author{Marc Labouchardiere \\ \normalsize\upshape (23857377)}
\supervisor{Dr Jin B.\ Hong}
\keywords{...}
\categories{...}
```

`\supervisor{}` is a small addition to the class — omit it and the
`Supervised by` line disappears. For two supervisors, separate them with
`\\`, e.g. `\supervisor{Dr A. One \\ Dr B. Two}`.

The chapters are placeholders tailored to the project; replace the italicised
`[...]` notes as you write. Remove `\listoffigures` / `\listoftables` if unused.
