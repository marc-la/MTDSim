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
  `ch7_discussion/refusing_the_baseline_race.md`."*
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

### The flag taxonomy for inline comments (ratified by Marc, 2026-08-17)

Every inline comment opens with **one flag** from this closed set, then its
priority (`M1`–`M3` or `[minor]`), then the grounding document. The flag tells
Marc what *he* does with it; the set is deliberately small so it becomes
reflex. Flags name the action, never supply the words.

| flag | meaning | what Marc does |
|---|---|---|
| `[WRONG]` | a fact, number or attribution contradicts the record / data — the correct value and its source are named | replace the fact; wording his |
| `[INSERT]` | an argument or disclosure the record has earned is missing here — named, with its document | dictate the missing point |
| `[SCOPE]` | overclaim, badge-ceiling breach, or a claim that belongs to another chapter (pre-claiming ch5/ch6, re-describing ch2) | pull the claim back to what is earned, or move it |
| `[REFRAME]` | right content, wrong frame or emphasis — the frame the record supports is named | re-cast the point |
| `[REORDER]` | the sentence/paragraph belongs elsewhere — where, and why | move it |
| `[TIGHTEN]` | the point is made twice, or in more words than it earns — which sentence carries it is named | cut to that sentence |
| `[EXPAND]` | too terse / abrupt — a claim without its evidence leg or its "so what" — what it needs is named | add the leg |
| `[CUT]` | does not earn its budget or is ruled out (appendix material, apology, flourish) | delete |
| `[VERIFY]` | a number or citation gated on a validation artefact or an anchor not yet in the bib | confirm before it enters prose |
| `[KEEP]` | works — and *why* (calibrates the scrutineer as much as a negative flag) | nothing |
| `[3b]` | word choice / hedge / self-correction left for Marc's register walk (inherited from `repair-dictation`) | choose |

Rules: one flag per comment (if two apply, split the comment); the three
priority moves are still at most three, each built from the flags it bundles;
`[KEEP]` is used, not hoarded — a draft with no `[KEEP]` is under-calibrated.

## Split-stream mode — white box + black box (ratified by Marc, 2026-09-02)

On request ("black box this", "split stream", "two independent approaches"),
the pass runs twice, independently, and merges in the main thread:

- **White box — the main thread.** Full session context: the dictation trail,
  the same-day rulings, the handoffs already loaded. Its edge is
  ruling-awareness (it will not re-open what Marc ruled an hour ago); its
  blind spot is authorship anchoring — it under-audits content the session
  itself produced (captions, table cells, clauses assembled from ruling
  audio).
- **Black box — one subagent.** Gets ONLY: the relevant skill file(s), the
  governing workflow contract(s), the pack/context documents, and the draft's
  location. No session history. Instruct it to read `%` comments ONLY as a
  do-not-re-flag list — the comment trail records rulings and partially
  de-blinds it (observed on the 2026-09-02 pilot: the black box endorsed a
  same-day ruling it had read in a comment). For a fully blind run, hand it
  comment-stripped prose.
- **The merge — main thread, before anything reaches Marc.** (1) Verify every
  *novel* black-box fact against its named source before endorsing — zero
  trust (the pilot's two caption findings, the Zhang scheme count and the CTS
  attribution, were both novel and both verified true). (2) Reject black-box
  proposals that re-open same-session rulings, and say so explicitly (the
  pilot's W-6 endpoint rider). (3) Convergent findings are the strongest
  signal — present them as a block for blanket ruling. (4) Return ONE merged
  set, tagged WB / BB / both, still under this skill's prioritisation cap.

The mode's measured value: the black box catches what the white box authored;
the white box protects what the black box cannot know. Marc rules on the
merged set, never on two raw streams.

## Boundaries

- **Not prose review** — rhythm, tells, and voice belong to `voice.md` and
  `critique_protocol.md`; note a content gap inside a paragraph but leave wording to
  them.
- **Not a re-decision** — where the draft contradicts the record, flag it for Marc;
  the record is dated evidence and the draft is his current intent, and he rules.
  Never "correct" the draft to match an old thread.
- **Not generation** — restated because it is the whole point.
