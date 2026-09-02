---
name: compress-to-ledger
description: >
  Pass 5 of the drafting pipeline: compression to the ledger. Take a unit
  that is through passes 2-4 (repaired, 3b-walked, scrutinised) and return a
  compression proposal ledger that brings it to its ledger budget (the
  skeleton comment's figure; ~250-300 words) — by DELETION and MERGING of
  Marc's own words, never by paraphrase or synonym substitution. Every
  proposal is before → after with a word delta and a technical-claim flag
  where one applies; NOTHING is applied unratified. Easy by design: draft 1
  was spoken long on purpose. Use when Marc says "compress to the ledger",
  "pass 5 on §X", "run the compression", "bring this to budget". Not for
  register/terminology (voice-pass), not for content gaps (scrutinise-draft),
  and never for generating prose.
---

# Compress to the ledger — pass 5, per unit

The job: the unit was spoken at 2–3× budget on purpose; this pass proposes
the cut back to the ledger. The pipeline's table assigns pass 5 to Marc; this
skill is the **structured delegation he ruled on 2026-09-02** (piloted on
§2.2.2 the same day): the session builds the cut as a proposal ledger, Marc
rules item by item, and only ratified items touch the tex. The ratification
gate is what keeps the pipeline's safety property — an unratified proposal is
never applied.

## The one rule

**Compression is deletion and merging of Marc's words.** Allowed: deleting
words, phrases, sentences; fusing two of his sentences at their own
conjunctions; folding a table/figure pointer into a neighbouring sentence as
a parenthetical. Banned: synonym substitution, new sentences, reordering
inside a sentence, paraphrase — except where a merge mechanically forces a
joint word, which is then flagged for his eye. A proposal that deletes a
**claim** (not just words) carries an explicit technical-claim flag naming
what is lost and where else (if anywhere) the record carries it.

## Load before proposing

1. The unit's skeleton comment and `% DRAFT STATE` / ruling trail in the tex
   — the budget figure, the must-carry disclosures, every do-not-re-flag
   ruling. A proposal that re-opens a ruled item has failed the pass.
2. [`../../../docs/workflows/drafting_pipeline.md`](../../../docs/workflows/drafting_pipeline.md)
   — pass 5's cut order and gates.
3. The unit's floats and captions, and the neighbouring units — duplication
   against them is the highest-value cut class.

## Method

1. **Sentence merit table.** Every sentence: what it contributes, what it
   duplicates (a float, a caption, a neighbouring unit, an earlier sentence),
   and a verdict — KEEP / CUT / MERGE(with which) / MOVE(where) /
   TIGHTEN(what to delete).
2. **The cut order** (pipeline pass 5): duplicates → re-explanations →
   second examples → qualifiers a citation, float, or appendix already
   carries. Sentence fusion only once whole-sentence cuts stall.
3. **Never cut:** must-carry disclosure sentences (skeleton comment is the
   authority), numbers, citations, sentences ruled in on the handoff record,
   and repairs ratified by an earlier pass (observed 2026-09-02: a black-box
   stream proposed cutting a same-day W-6 repair — the merge caught it).
4. **The ledger.** Numbered proposals, each `before → after` (or CUT) with
   its word delta; technical-claim flags inline; a projected final count; and
   the **minimal set** that just reaches budget, so Marc can take the floor
   instead of the full cut.

## Split-stream mode — white box + black box (ratified by Marc, 2026-09-02)

On request, run the compression twice, independently:

- **White box — the main thread**, with full session context (ruling-aware;
  anchored on its own authorship).
- **Black box — one subagent**, fed only this skill's rules, the unit, its
  floats, the neighbouring units, and the budget — no session history.
  Give it wide scope: the section's purpose, each paragraph's job, sentence
  merit, and rearrangement licence. Instruct it to ignore `%` comments (or
  read them only as do-not-re-flag rulings).
- **The merge — main thread**: verify novel black-box claims before
  endorsing; reject proposals that re-open same-session rulings, saying so;
  present convergent proposals as a block; tag everything WB / BB / both.
  Marc rules on the merged ledger only.

## The return

1. The merged proposal ledger (inline against the prose on request, so Marc
   can visualise the changes — strikethrough for cuts, bold for insertions).
2. Technical-claim flags, each naming what is lost and its carrier elsewhere.
3. Projected count vs the ledger budget, plus the minimal set.
4. Applied to the tex at return time: **nothing**.

## After Marc rules

Apply exactly the accepted items — no opportunistic extras riding an accepted
proposal. Update the unit's ruling-trail comment (what was cut, which claims
moved carriers), log rejections as do-not-re-flag entries, and hand off:
"unit is through pass 5; pass 6 (voice-pass) runs on the assembled section."

## The pipeline seat

Pass 1 speak (Marc) → 2+3a `repair-dictation` → 3b marker walk (Marc) →
4 `scrutinise-draft` → **5 this skill** → 6 `voice-pass` (section-level) →
integration check. First-completion overdraft is fine (Marc's 2026-08-18
ruling): the cut to the ledger may wait for the assembled section when the
overdrafts can be reconciled together.
