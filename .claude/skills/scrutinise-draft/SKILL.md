---
name: scrutinise-draft
description: >
  Scrutinise a draft dissertation section (or produce content-point scaffolds for one
  Marc will write) against this repo's corpus — the research record, the chapter notes,
  the implementation records, and the paper extractions — to check whether it hits the
  right argument, the right framing, owns the concessions the work owns, respects the
  badge ceiling, and is not missing an argument the research already earned. Returns
  content points and the supporting documents that ground them; NEVER drafts the prose
  (that is Marc's, to preserve his voice). Use when Marc says "scrutinise this section",
  "am I missing arguments here", "does this hit the right framing", "content points for
  <section>", "cold-draft the arguments for <section>", "review my draft against the
  record". Not for prose/voice review (that is critique_protocol.md + voice.md) and not
  for generating dissertation text.
---

# Scrutinise a draft against the research record

The job: take a draft section (or a section Marc is about to write) and measure its
**content** against the corpus of what this research actually decided, tried, and
concluded — surfacing wrong framing, drifted intent, missing arguments, unowned
concessions, and overclaims, each tied to the supporting document that grounds it.
This is the content/intent layer of review; it sits above prose review, not instead
of it.

## The governing contract — load it first, in full

**[`docs/workflows/draft_scrutiny.md`](../../../docs/workflows/draft_scrutiny.md) is
the protocol. Read it before doing anything**, and follow it exactly where any
instinct here is thinner than it. The two things it carries that this file only
summarises: the **scrutiny question set** (§b — intent fidelity, reversal hygiene,
argument completeness, concession coverage, badge ceiling, evidence grounding) and
the **corpus map** (§c — which documents scrutinise which chapter). When the task
reaches prose-level comment, also load
[`docs/workflows/critique_protocol.md`](../../../docs/workflows/critique_protocol.md)
and [`docs/workflows/voice.md`](../../../docs/workflows/voice.md) — they own the
sentence and argument-quality layers this skill does not.

## The one rule that must not bend

**Scrutinise, never generate.** The corpus is a yardstick and an evidence base for
feedback; it is never a source of draft prose. Return content points — a named gap,
the document that grounds it, the drafting left to Marc. A cold-draft request is
answered with an **argument scaffold** (which claims, in what order, each with its
grounding document and badge ceiling), not with paragraphs. A run that returns
finished dissertation prose has failed, however good the prose — the value of the
dissertation is that it is in Marc's voice, and that is what this skill protects.

## The steps

1. **Locate the draft in the chapter map.** Identify which chapter/topic the draft
   belongs to (ask Marc if ambiguous — do not guess a chapter and pull the wrong
   pack). Read the draft in full yourself.
2. **Assemble the pack.** From `draft_scrutiny.md` §c, load the *whole row* for that
   topic — notes, research-record threads, implementation records, extractions —
   widening across rows if the draft reaches across them. Read them; the feedback is
   only as relevant as the documents behind it.
3. **Run the question set (§b) in order.** Every finding names the corpus document
   that grounds it — that document is the "supporting document" the finding attaches.
   Stop at naming; never draft the fix.
4. **For breadth, fan to scrutineers (optional).** Each subagent gets
   `draft_scrutiny.md`, its pack row, and the draft, and returns content points only
   (§d). A subagent that returns prose is discarded, not merged. Do not fan unless
   the draft's length or breadth warrants it — a single focused pass is usually
   better than a fan.
5. **Return a prioritised summary — at most three moves.** A scrutineer prioritises;
   a flat list of forty co-equal notes is the failure mode. Each of the three names
   the finding, its type (§b), and its grounding document.

## What a good return looks like

- *"Framing drift (intent fidelity): the section argues the movement attacker should
  match the baseline — the record shows this framing was reached and reversed on
  2026-07-29; the current position is the census reading. See
  `research_record/threads/comparability_and_census.md` and the note
  `ch6_discussion/refusing_the_baseline_race.md`."*
- *"Missing argument (completeness): the timing section states the durations are
  declared but does not carry the shape-not-scale defence the work already earned —
  `ch4_methods/operational_validation.md` §shape-not-scale. Without it an examiner
  reads the durations as arbitrary."*
- *"Overclaim (badge ceiling): 'the model demonstrates incentive rationality' — the
  criterion holds axis 6 at DESIGNED with two measured negatives. `demonstrated` is
  not earned; state it as designed-with-a-measured-negative. See
  `implementation/apt_model_criterion.md` axis 6."*

Each of those is a content point with a supporting document and no drafted prose —
that is the shape every finding takes.

## Alternate return format — the inline-annotated draft (on request)

When Marc asks for the scrutiny **as comments breaking up the draft** (so he can run
through and act on findings in real time), return his draft text **verbatim** with
the findings interleaved as clearly-delimited bracketed blocks — e.g.
`**[M1 — <question-set type>]** …` — inserted at the exact sentence each finding
attaches to. Rules unchanged, only the presentation moves:

- His sentences are never altered, trimmed, or reordered; comments sit *between*
  them, never inside them.
- Every comment still names its grounding document, and the at-most-three-moves
  prioritisation still holds — number comments by the move they belong to (`M1`–`M3`),
  and mark standing/minor notes as such (`[minor]`), so priority survives the
  interleaving.
- The no-generation rule binds inside comments too: a comment names the gap and the
  grounding document; it never supplies the fixed wording.

## Boundaries

- **Not prose review** — rhythm, tells, and voice belong to `voice.md` and
  `critique_protocol.md`; note a content gap inside a paragraph but leave wording to
  them.
- **Not a re-decision** — where the draft contradicts the record, flag it for Marc;
  the record is dated evidence and the draft is his current intent, and he rules.
  Never "correct" the draft to match an old thread.
- **Not generation** — restated because it is the whole point.
