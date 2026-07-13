---
status: durable
created: 2026-07-13
updated: 2026-07-13
---

# Notes rubric — the quality gate for `docs/notes/`

**Status:** durable. Every file in [`../notes/`](../notes/) must clear this rubric before it is committed, and existing notes are cross-examined against it whenever touched. The bar is deliberately high: notes feed the dissertation almost directly, and Marc reads this layer more than any other — a weak note costs more than no note.

## What a note is

A note is **a dissertation-shaped draft of one idea**: an argument, finding, defence, or framing that will become part of a chapter. Not fully-fleshed LaTeX paragraphs, but high-quality prose that is already *thought through* — reasoned, evidenced, and positioned — so that writing the chapter is assembly, not research.

A note is **not**: a session log, an investigation record, a decision register with commit hashes, a QA audit, a to-do list, or a plain-English companion to a spec. Those are real and valuable documents — they live in [`../implementation/`](../implementation/) or [`../handoffs/`](../handoffs/) per the [docs map](docs_map.md).

## The reader contract (the register)

Write for **a reader who knows the field but not this repo** — concretely, Marc's supervisor: fluent in MTD research, simulation, and MITRE ATT&CK, familiar with the published MTDSim lineage, but with **no knowledge of this codebase's internal terminology (GAP, GASP, OGASP, L0–L4, "the substrate", Tier 1–3, handoffs), its file layout, its branch names, or its session workflow**. That reader must be able to follow every sentence of the body without opening the repo.

Consequences:

- **Formal academic prose.** Complete sentences and paragraphs that argue, in Australian English. Tables only for genuinely tabular material. It should be reasonably interesting to read — an argument with stakes, not a memo. The sentence-level voice — argumentation moves, sentence signature, banned tells — is [`voice.md`](voice.md); write to it by default.
- **Define or drop internal terms.** Either introduce a project term in plain language at first use ("the aggregated technique-dependency graph — internally, the GAP") and use it sparingly, or write the plain description throughout. Never assume the codename.
- **No workflow plumbing in the body.** Commit hashes, handoff filenames, branch names, session dates, "this landed in …", `[fetched]`/`[search]` flags and file paths belong in the *Evidence and repo anchors* footer, not the argument. (Epistemic honesty stays in the body — "this figure is unverified against the primary source" is substance; "`WebFetch` returned 403" is plumbing.)
- **Cited, not asserted.** Empirical claims carry their source (author-year is fine; the footer anchors it to an extraction). A claim without a source is flagged in-text as a *citation anchor to reconcile* — never silently asserted. Per the guardrails: never assert a paper wrong; distinguish inherited facts from editorial choices.

## Structural requirements

- **Atomic — one idea per file.** If the file needs two "Why this matters" paragraphs, it is two notes. Split rather than accrete; cross-reference siblings.
- **Self-contained.** Opens with enough context that the note stands alone. A reader should not need another note first (links are enrichment, not prerequisites).
- **Positioned.** Every note declares where it lands in the dissertation: its chapter (the subdir it sits in) plus a one-to-two-line *Position* statement ("the motivation the introduction opens with"; "the threats-to-validity defence in the methodology chapter").
- **Honest about status.** What is demonstrated vs designed vs conjectured is explicit. A note whose claim depends on an unrun experiment says so.

### Template

Use [`../notes/_template.md`](../notes/_template.md). The shape:

```markdown
---
status: durable | superseded
chapter: ch3_design            # matches the subdir
created: YYYY-MM-DD
updated: YYYY-MM-DD
lineage: <original filename, if renamed/refactored — else omit>
---

# <Title — a claim or question in plain English>

## Position in the dissertation
<1–2 lines: which chapter, what role the idea plays there.>

## The idea
<The argument itself, self-contained, in the register above. Multiple
sections as the argument needs — but one idea.>

## Evidence and repo anchors
<The ONLY place repo paths appear: extractions cited, specs/implementation
docs that carry the technical detail, data artefacts, related notes.>

## Revisit conditions
<What would invalidate or reframe this note.>
```

- **Naming:** topical slug, no date prefix (`post_ingress_mtd_gap.md`, not `2026-07-07_post_ingress_mtd_gap.md`). Creation date lives in frontmatter; git carries the history. Underscore-prefixed files (`_template.md`, `_rubric.md`) are process scaffolding, exempt from the register.
- **Chapter subdirs:** see the chapter map in [`docs_map.md`](docs_map.md#notes--the-dissertations-staging-layer). Broad-brushstroke only — never encode section numbering below chapter; that structure is emergent.

## The cross-examination (run before committing a note)

1. **One-sentence claim.** Can the note's idea be stated in a single sentence? State it (the title should nearly do it). If not — split or keep thinking.
2. **Supervisor test.** Would Dr Hong follow the body without the repo and without a glossary? Every internal term defined or absent?
3. **Examiner test.** Is the claim defensible as written — evidence attached, counter-arguments acknowledged, scope honest? Would it survive "how do you know?"
4. **Register test.** Is it prose that argues, or fragments that gesture? Arrow-chains, bullet-salads, and table-only sections fail.
5. **Placement test.** Is any part of the body actually implementation record (needs the repo to follow)? Move that part to `implementation/` and keep the distilled argument.
6. **Position test.** Does the note say where it lands in the dissertation, and does that match its subdir?
7. **Anchor test.** Are repo paths confined to the footer? Are all empirical claims cited or explicitly flagged as anchors-to-reconcile?

A note failing any test is not committed to `notes/` — fix it, split it, or route it to the correct subtree.

## Lifecycle

- **Created** when a session surfaces something dissertation-worthy *and* it clears the rubric. Rubric-clearing is part of creating the note, not a later cleanup.
- **Updated** when the underlying truth changes and the note would mislead; bump `updated`.
- **Superseded, not deleted** when the dissertation absorbs it verbatim or a better note replaces it: set `status: superseded` with a pointer. (Notes are kept — they are the audit trail of the thesis's ideas. Deletion is reserved for notes that were misfiled process records, whose content lives on in `implementation/` or git history.)
