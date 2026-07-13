---
status: durable
chapter: <chN_label — matches the subdir this file sits in>
created: YYYY-MM-DD
updated: YYYY-MM-DD
# lineage: <original filename, only if this note was renamed/refactored from an older one>
---

# <Title — the note's claim or question, in plain English, no internal jargon>

<!-- Gate: this file must clear docs/workflows/notes_rubric.md before it is
     committed. Run the cross-examination checklist there. One idea per file;
     written for Marc's supervisor — no repo access assumed, no internal
     terminology (GAP/GASP/OGASP, L-numbers, handoffs, tiers) unless defined
     in plain language at first use. -->

## Position in the dissertation

One or two lines: which chapter this lands in (matching the subdir) and what role the idea plays there — e.g. "the motivation the introduction opens with", "the threats-to-validity defence in the methodology chapter".

## The idea

The argument itself, self-contained, in formal academic prose. Open with enough context that the note stands alone; define any project-specific concept in plain language at first use. Structure with subsections as the argument needs — but if a second, separable idea appears, split it into its own note. Empirical claims carry a source (author-year), or are explicitly flagged as citation anchors still to be reconciled — never silently asserted.

## Evidence and repo anchors

The **only** place repo paths appear:

- Extractions cited: [`../../sources/extractions/<key>.md`](../sources/extractions/)
- Technical detail carried by: the relevant [`../../implementation/`](../implementation/) doc(s), data artefacts, code.
- Related notes: siblings this note builds on or is built on by.

## Revisit conditions

What would invalidate or reframe this note (e.g. "if the discrimination probe shows the profiles do not separate"; "if the supervisor rejects the framing term").
