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
| `FLOATS.md` | Manifest of every figure and table: position, file, label, generator. |
| `uwa-crest.png` | UWA crest used on the title page. |
| `figures/` | Figures (`\graphicspath` points at it). Every file is named for its dissertation position — `fig_<chapter>-<section>-<subsection><order>_<name>` — see `FLOATS.md` for the full manifest (position, label, generator) and `docs/workflows/figure_table_conventions.md` §j for the rule. Generated, never hand-edited. |
| `tables/` | Generated table fragments to `\input`, named `tab_<position>_<name>.tex` on the same rule; manifest in `FLOATS.md`. Do not hand-edit. |

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
