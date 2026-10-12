---
status: durable
created: 2026-09-30
updated: 2026-09-30
provenance: distilled from the chapter 2 scrutiny and redraft of 2026-09-30 (seven rounds of Marc's walk-throughs); the worked record is docs/handoffs/2026-09-30_ch2_background_scrutiny.md, or git once that handoff is retired
---

# Chapter scrutiny: heavily scrutinise one chapter, then redraft it for clarity and relevance

**Invocation.** Marc pipes this file in with a chapter number, for example
"run chapter_scrutiny.md on chapter 3". Everything below applies to that chapter
and nothing else. Out-of-chapter findings are *flagged*, never fixed, except for
the consequential edits a fix forces elsewhere (a re-pointed `\ref`, a term
swept dissertation-wide on Marc's ruling).

**The goal, in Marc's words.** "Clarity and relevance are the two main games."
Clarity comes from relevance, and relevance comes from "more is less". Every
sentence, float, cell and label either does something a reader needs at that
point, or it goes.

## 0. Load before touching anything

1. The six read-first files in [`../../CLAUDE.md`](../../CLAUDE.md), and
   [`voice.md`](voice.md) §(0), the five checks. Then run the session-start
   checks.
2. The chapter's contract, from the table below: its notes README (the shape
   authority, which may be stale; check it against the tex) and its genre
   yardstick.
3. [`terminology.md`](terminology.md), [`connective_prose.md`](connective_prose.md)
   (for the opener and the close), [`critique_protocol.md`](critique_protocol.md)
   (edit tiers), [`draft_scrutiny.md`](draft_scrutiny.md) (corpus map),
   [`figure_table_conventions.md`](figure_table_conventions.md), and
   `.claude/skills/scrutinise-figure/diagram_best_practice.md` §4 (the pitfall
   catalogue).

| Chapter | Notes README | Genre yardstick |
|---|---|---|
| 1 Introduction | none (a synthesis) | [`connective_prose.md`](connective_prose.md), [`../notes/_writing_guide.md`](../notes/_writing_guide.md) |
| 2 Background | `ch2_background/` | [`background_conventions.md`](background_conventions.md) |
| 3 Literature review | `ch3_lit_review/` | [`literature_review_conventions.md`](literature_review_conventions.md) |
| 4 APT attacker model | `ch4_methods/` | [`model_chapter_conventions.md`](model_chapter_conventions.md), [`literature_conventions.md`](literature_conventions.md), [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md) |
| 5 Evaluation | `ch5_experimental_setup/`, `ch6_results/` | [`evaluation_conventions.md`](evaluation_conventions.md), [`results_section_workflow.md`](results_section_workflow.md) |
| 6 Discussion | `ch7_discussion/` | none yet: commission one |
| 7 Conclusion | `ch8_future_work/` | `_writing_guide.md`; commission if thin |

## 1. Read the chapter as the reader meets it

- Read the chapter's tex range, prose and `%` comment trails. The comments are
  the ruling history; the prose is what ships.
- Render the chapter's PDF pages and read them as images.
  - Take the chapter's page numbers from `dissertation.toc`.
  - The front matter shifts the physical index; find the offset by rendering one
    page first.
  - Render with `pypdfium2`, into the scratchpad. The build command is in
    `docs/thesis/README.md` (pdflatex, bibtex, pdflatex ×2; there is no latexmk).
- Measure prose words, caption words and float count per unit against the ledger
  in `_writing_guide.md`.

## 2. Build the yardstick (a background agent, in parallel with step 3)

If the genre yardstick exists, load it. If not, commission one. A general-purpose
agent researches published guidance for *this chapter's genre*:

- purpose;
- what a CS student and the examiner expect of it;
- structure;
- named pitfalls;
- figures;
- a checklist of 10–15 items.

Its sources: Evans, Gruba & Zobel; Zobel; Paltridge & Starfield; examiner studies
(Golding et al. 2014, Mullins & Kiley, Holbrook); CS thesis guides (UWA CSSE
marking guides, Cambridge, Edinburgh). The agent reads the existing workflow
files first so it adds rather than repeats. It cites what it read and marks what
it didn't. Distil its report into `docs/workflows/<genre>_conventions.md`, in
the shape of `background_conventions.md`, and register it in
[`docs_map.md`](docs_map.md).

## 3. The forward and backward audit (a background agent)

A read-only agent audits the chapter against the whole tex. It reports:

- **A. Inbound references.** Every `\ref` to the chapter's labels from outside
  it, and labels nothing references.
- **B. The lean test, fact by fact.** For each fact, term, table row and figure,
  the first later line that uses it, or "not used later".
- **C. Terms.** Terms used before they are defined, or never defined. Synonym
  drift within the chapter and against other chapters.
- **D. Contradictions and duplication.** Contradictions with other chapters,
  duplication of chapter 1 or of later chapters, and repeats inside the chapter.
- **E. Verdict.** What can be cut with no downstream loss, and what later chapters
  need that this chapter lacks.

For chapters 3 onward, "later" means later chapters, and the backward use is
checked too: is every object this chapter uses already defined in an earlier
chapter (the ch5 antecedent rule, generalised)?

## 4. Verify before calling anything a defect

Every claim the redraft will state, and every "this is wrong", is checked against
the source that owns it:

- simulator behaviour against the code (with file:line);
- a cited claim against its extraction in `docs/sources/extractions/`, or the
  source markdown;
- a term against the registry.

On chapter 2 this caught several errors, among them:

- a misparaphrased definition;
- "discrete-event" credited to the wrong paper;
- a false "no detection channel";
- a caption asserting a graph structure the code does not build;
- four phase descriptions that did not match what each phase does.

Marc asks "are those right?". The answer must already be yes, with the locator.

## 5. The ledger (a handoff, `docs/handoffs/YYYY-MM-DD_chN_<topic>_scrutiny.md`)

- **§1, the yardstick in five lines:** purpose, context, audience, the lean test,
  the float test.
- **§2, the chapter verdict and at most three priority moves.**
- **§3–§9, entries by ID.** G chapter-level. S structure and headings. F figures.
  T tables. Prose, by unit. C content the chapter lacks, named and never drafted.
  X factual corrections with evidence.
- Each prose entry is `before → after`, with a word delta, its tier, and any prior
  ruling it re-opens, named.
- A minimal set Marc can take alone.
- The validation gate and a reading list.

The chat reply is short and thesis-framed: what the chapter is missing and what
it carries that it shouldn't. Point at the ledger for the rest.

## 6. Apply on Marc's rulings, then iterate on his walk-through

Marc reads, rules, and licenses overturning any prior ruling ("happy to do so").
Apply in one pass, then expect several rounds of walk-through comments; each
round is applied, rebuilt, re-rendered and checked on the page. Figures go
through their generators, and a figure rebuild can go to a background agent
with an exact brief (terms allowed, marks to remove, transitions to keep). Re-read
every regenerated PNG before accepting it. Record each round in the handoff's
*Applied* section, the terms in the registry, and the shape in the chapter README.

## 7. What Marc wants: standing preferences from the chapter 2 rounds

**Relevance: the lean test.**

- Nothing enters that a later chapter does not lean on. Cut it even when it is
  true and cited, and say where the fact survives if anywhere.
- Add what later chapters need and this chapter lacks. A definition used before
  it is given belongs at its first use; the later chapter then refers back.
- A decision the dissertation made is not background or context. It moves to
  the chapter that makes the choice.
- A table or figure the text already carries, or that repeats another float, goes
  (the "no duplicate floats" rule).

**Clarity: sentences.**

- Lead with the subject ("The exposed endpoints keep …", not "No MTD mechanism
  changes an endpoint's …").
- One idea per sentence. Cut restatements of the introduction, and cut
  "details the reader does not need" (for example, the interval's exponential
  term became "200 s by default, and near-periodic").
- Signposting names exactly what each section holds, in the words of that
  section's heading.
- A lead-in or close does its purpose only. A hand-over says what the next
  chapter does with what this one gave. It does not pre-empt that chapter's
  content: the eight properties were ch3's to introduce, so naming them in ch2's
  close "lost sight of its purpose".
- Spell terms out in full where they are introduced ("when to move", not "when").

**Terms.**

- One term per thing, italicised at first use and then repeated verbatim,
  dissertation-wide.
- A swept term is swept everywhere it appears, including generators and floats
  in other chapters. Regenerate and diff so that only labels change.
- Check the registry before choosing a word. Some are reserved: *objective* is
  the attack profiles'; *deployment strategy*, not execution scheme; *reconfigure*,
  not rewrite; *phase* for the baseline's six.
- No code names on the surface (`SCAN_HOST` and the like). The supervisor flagged
  them as undefined decoration; use the plain names.
- Headings mirror their counterparts in other chapters (§2.2.2 = §5.3.3,
  "MTD mechanisms and deployment strategies").

**Tables.**

- Each cell answers its column heading. Put the shared qualifier in the heading
  ("What it deploys at each interval"), not in every cell.
- Cells are short, precise and concrete. Marc finds table text hard to read.
- Group rows with indented members, never a value repeated down a column.
- No self-evident caption rules. A fact that is not table-shaped moves into the
  prose. Rows speak the chapter's own terms ("Time limit", not "Run ends").
- Watch float placement: no table stranded after the chapter's last sentence.

**Figures.**

- Plain and purposeful. Fewer marks, with labels in place in the prose's terms.
  Each figure must show what the text uses; for example, a host's parts, each
  labelled with the mechanism that reconfigures it.
- Colour only where it carries meaning, one colour for one story. On chapter 2,
  red means the attacker (its route and what it compromised); everything else is
  ink or grey. No accent colour used to single things out.
- Boxes are sized to their contents, never enlarged to fill space, and in the
  style of the dissertation's other figures (Figure 4.1).
- Captions say how to read the figure. The account of what is happening lives in
  the prose, and the caption does not repeat it.
- A figure may be silent on a nuance; it may not assert a falsehood. Verify
  every drawn edge, label and description against the code.

## 8. Git and scope

Commit per the session workflow, on a branch for the chapter; ask which branch if
the checkout is parked on another session's. Never push. Keep the tex edits to
the chapter, plus the consequential edits named at the top.
