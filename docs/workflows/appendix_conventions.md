# Appendix conventions

**Status:** durable (Marc, 2026-10-13). Load before adding, moving or cutting anything in the dissertation's appendices. The first audit against it is in handoff `2026-10-09_ch7_conclusion_and_appendix_structure.md` §10.

Sources marked **[V]** were read in full on 2026-10-13 and can be quoted. **[S]** marks a general writing guide: it supports a convention, but it is not a UWA rule or a scholarly source.

## (a) The UWA rule [V]

CITS4001 *Project components* ([link](http://teaching.csse.uwa.edu.au/units/CITS4001/index.php?fname=project-components&project=yes)):

- "The dissertation is a 30-50 page document"; 24-point projects run "up to 15,000 words". "The word limits include the reference section", "excluding any appendices."
- "Appendices typically consist of derivations, theorems, lemmas, concise code extracts, concise data sets, series of graphs or tables, etc. considered non-essential to understanding the core material of the dissertation."
- "If the material is essential to understand the dissertation, it should not appear in an appendix; it should appear in the body of the dissertation."
- "Any large sections of text appearing as an appendix may be considered as an attempt to circumvent the word limit."

The page does not require the proposal to be bound into the dissertation, and it sets no page count for appendices. **The UWA template does require it:** the boilerplate built on `cshonours` (commit `4f3657f5`, 2026-07-09) carried the template's instruction "You must include as your first appendix an exact copy (in wording) of your original project proposal." Appendix A is therefore required, not an orphan, and is exempt from (b) and (d).

Two consequences:

- **An appendix holds data.** It is not a place for prose. A section that argues is either essential, so it belongs in the body, or unneeded, so it is cut.
- **Moving something into the body costs words and pages.** The body has a 15 000-word cap that includes the references, and a 30–50 page guide. Every promotion must be paid for by a cut.

## (b) The entry test: three questions, in order

1. **Does a reader need it to follow the argument?** That covers a chapter 5 result, or a chapter 6 explanation that has no evidence in the body. If yes, it goes in the **body**, compressed to what the argument uses.
2. **Does a body sentence state a claim or a number that this item is the evidence for, and would an examiner plausibly check it?** If yes, it goes in the **appendix as data**: a table or a figure, opened by one or two sentences naming the claim it backs.
3. **Neither?** Then **cut** it. The repository is the archive (`data/results/`, `docs/implementation/`), not the appendix. If the material matters for replication, one data-availability sentence can point to it.

## (c) Do

- **Use data, not prose.** Each section is its floats plus a lead of one or two sentences that names the body claim it backs.
- **Use one float per fact.** Show a set of numbers as a table or as a figure, never both. Show a perturbation once, in a summary table or in per-value tables, never both.
- **Cite every item from the body.** The citation says what to look at, not just "see Appendix X".
- **Order by first call.** Appendices follow the order in which the body first calls on them, and each opens on what it backs.
- **Keep replication detail here.** This means declared values, settings, and per-row reasons that the body states in summary.

## (d) Don't: pitfalls, and how to spot each

| Pitfall | How to spot it | Fix |
|---|---|---|
| Argument in the appendix | The section concludes ("therefore", "so", "likely", "a hypothesis"), and no body sentence states the conclusion | Apply (b)1: body or cut |
| Self-declared irrelevance | The section says "not part of the main argument", "it is not a result", or "the claim stands without it" | Cut. If the author says it is not needed, the examiner believes it |
| Logbook | It tells how the work evolved: re-scorings, earlier rules, rejected alternatives in full, "run while chapter 6 was written" | One sentence in the body, or the AI Use Declaration where the history is AI use |
| Duplicate floats | A figure and a table of the same numbers; a summary table plus per-value tables; two figure-family members that show the same thing | Keep the one the body cites |
| Data dump | A full grid (every metric at every condition) that no body sentence cites | Move it to the repository, with one data-availability sentence |
| Someone else's data | It reproduces a cited paper's tables or sweeps | Cite the paper |
| Orphan | Nothing in the body cites it, directly or through a float it contains | Cut, or cite it with a reason |
| Illegible float | Type under the figure floor (`figure_table_conventions.md` §h) | Rebuild it, or cut it if the body does not depend on it |

General guides agree on the orphan, padding and argument-in-appendix pitfalls [S] ([Scribbr](https://www.scribbr.com/dissertation/appendix/); [Editage](https://www.editage.com/blog/how-to-create-an-appendix-for-a-dissertation-example-templates-format/)).

## (e) What an examiner reads the appendix for

An examiner reads it to check a claim, or to judge **selection**. A curated appendix shows that the author chose what backs the argument. A long one tells the examiner the author could not choose, and under UWA's rule it can read as dodging the word limit. The budget is therefore not a page count. Every page must pass (b), and no section carries more prose than its lead.
