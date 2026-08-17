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
| `figures/` | Figures (`\graphicspath` points at it). Generated figures carry their generator: `l1_attack_graph.{tex,pdf}` is written by `tools/l1_attack_graph_figure.py` from `data/gap/gap_v0.5.json` + one flow extract — regenerate, never hand-edit. |
| `tables/` | Generated table fragments to `\input` (e.g. `objective_classification_audit.tex` from `tools/gasp_structural_baseline.py --tex`); do not hand-edit. |

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
