---
name: voice-pass
description: >
  Pass 6 of the drafting pipeline: the section-level voice pass. Take an
  assembled dissertation section (every unit through pass 5), read it end to
  end, and return ONE proposal ledger — register conversion toward academic
  conventions, vacuous/irrelevant sentence cuts, terminology standardisation
  against the living registry, and the reader-overhead screen (names that do
  no work, undefined or late-defined terms, unexpanded acronyms, floats that
  do not speak the text's words) — plus the voice.md §(f) gate report. Every
  change is a proposal Marc rules on before it touches the tex; NOTHING is
  applied unratified. Use when Marc says "run the voice pass", "pass 6 on
  §X", "academic register pass", "standardise the terminology in this
  section", "sweep the section", "screen the terms", "what here would cost a
  mark". Not for unit-level dictation repair
  (repair-dictation), not for content scrutiny (scrutinise-draft), and not
  for flow/ordering/transitions (the integration check that follows this
  pass).
---

# Voice pass — pass 6, per section: register, cuts, terminology, the gate

The job: the first end-to-end read of an assembled section. The units were
dictated, repaired, scrutinised, and compressed one at a time; this pass is
where the section becomes one piece of academic writing that is still Marc's.
It sits after every unit's pass 5 and **before the integration check** — flow,
ordering, and transitions are the integration check's job and are out of scope
here; this pass works at the sentence.

## The licence, and the one rule

The pipeline's safety property is *no pass after draft 1 writes prose*. Pass 6
holds a **structured exception, ruled by Marc (2026-08-20)**: the session may
*propose* rewordings — register conversions, cuts, re-termings — because every
proposal is ruled by Marc item by item before it is applied. The ratification
gate is what keeps the property: **an unratified proposal is never applied,
and a proposal without a named rule behind it is never made.**

The failure mode is over-conversion: AI-flatten arriving through "register
polish". When in doubt between Marc's phrasing and a smoother one, Marc's
wins. The dial and its tiebreak are `academic_register.md` §(a): closer to
academic than to speech, and the conversion takes idiom, never argument shape
or a licensed voice device.

## Load order — before reading the draft, always

1. [`docs/workflows/voice.md`](../../../docs/workflows/voice.md) — in full; §(f) is the gate this pass runs.
2. [`docs/workflows/academic_register.md`](../../../docs/workflows/academic_register.md) — the target register and residue inventory; §(i) is the reader-overhead screen sweep 4 runs.
3. [`docs/workflows/terminology.md`](../../../docs/workflows/terminology.md) — the registry; only RATIFIED rows are enforced.
4. [`docs/workflows/critique_protocol.md`](../../../docs/workflows/critique_protocol.md) — §(b) edit tiers and §(f) banlist govern this pass's own proposals.
5. The section's `% DRAFT STATE` / skeleton comments in the tex, and the
   active drafting handoff — **honour every "do not re-flag" ruling**; a
   proposal that re-opens a ruled item has failed the pass.

## Step 0 — the end-to-end read

Read the assembled section once, continuously, before proposing anything.
Collect: register breaks, cut candidates, term variants, cross-unit
duplication. Note flow problems if they leap out — as a one-line handover to
the integration check, never as proposals here.

## Sweep 1 — register

Against `academic_register.md` (§b–§d, §h). Each finding:

- **quote → named rule → one proposal**, the proposal built as far as
  possible from Marc's own words (critique_protocol T2 discipline);
- no named rule, no finding — "this could be smoother" is not a defect;
- where the right conversion is genuinely Marc's word choice, pose it as a
  question (his-noun-here), not a proposal.

## Sweep 2 — vacuous and non-relevant sentences

The three-part survival test (`academic_register.md` §e): advances the unit's
question / not already said / removal would change understanding. Plus
**cross-unit duplication** — the same claim carried by two units survives in
one place; say which occurrence to keep and why. Each cut proposal quotes the
sentence and names which test it fails. Never propose cutting: must-carry
disclosures (the skeleton comments are the authority), numbers, citations,
sentences ruled in on the handoff record.

## Sweep 3 — terminology

Census the section against the registry:

1. **RATIFIED rows** — every non-canonical variant listed in one mechanical
   batch table: line, variant → canonical. (Still proposals: Marc applies or
   green-lights the batch.)
2. **PROPOSED rows** — enforce nothing; restate the pending ruling in one
   line so the ruling pass stays visible.
3. **Unregistered clusters** — two names for one concept found in the
   section: add a PROPOSED row to `terminology.md` (census counts + one
   recommendation), bump its `updated`. The registry growing is this pass's
   only direct write.
4. **Conflations** — distinct objects blurred (token vs movement attacker,
   profile vs net) are flagged as errors for Marc, never standardised.

## Sweep 4 — reader overhead (the term screen; added 2026-09-22, register E2)

Against `academic_register.md` §(i): the ten yes/no checks, with
`tools/term_screen.py` as the mechanical half. The class this sweep exists
for is the name that does no work — the supervisor's marking mechanism is
that every term a reader carries for no reason lowers the top of the range.

1. Run the tool on the section's chapter: `phrases --chapter N` (the phrases
   the chapter introduces and repeats), `acronyms --chapter N`, `variants
   --chapter N`; and `census` on every deprecated string in the registry's
   rows. Read the output as candidates, never as findings.
2. For each candidate, decide which it is: a **field term** (no finding), a
   term **defined at its first use** (no finding, or a check-3 finding if the
   definition comes later or moves), or a **name to remove** — a coinage with
   no needs basis, an ordinary word given a technical sense, a qualified form
   of an existing term that names the same object. Each finding: term → the
   §(i) check it fails → one proposal (remove; the field term; define at first
   use; expand; re-key the float) with the census.
3. Floats included: every key, tick, header, row group and caption in the
   section against the body's words (check 7). A float that needs
   regenerating is a proposal on its generator, never a hand edit.
4. The first-pages check (9) runs once per chapter, not per section: the
   abstract, introduction and conclusion against the chapter's names.

Prioritise: the names that do no work go first, then definitions, then
acronyms, then floats. A candidate the tool raised that the session judges a
field term is listed once, in a line, so Marc sees the judgement. Nothing
here hard-codes a thesis term: the tool derives its candidates from the text
and the registry rows carry the rulings (mechanism, not exception).

## The gate — voice.md §(f)

Run all nine checks over the assembled section; report a per-check verdict
with the failing instance quoted. This is the hard gate the section must pass
before its LaTeX is commit-ready; failures feed the ledger. ("Your gate,
against voice.md" — the pass exists so the gate is actually run, per section,
every time.)

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

## The return

1. **The proposal ledger** — numbered, grouped by sweep; each item
   `before → after` (or `cut`), rule anchor, one-line reason. Prioritise: name
   the top handful that most move the section; forty co-equal comments is a
   failure (critique_protocol §c).
2. **The §(f) gate report** — nine verdicts.
3. **Registry deltas** — new PROPOSED rows written, pending rulings restated.
4. **The screen report** (sweep 4) — the tool's candidate lists reduced to
   findings, the field-term judgements in a line each, and the census the
   validation gate will re-run after Marc rules.
5. Word count against the ledger budget, stated once.
6. **Self-audit close** (critique_protocol §b): every proposal re-checked
   against the §(f) banlist; report "tier audit: clean" or what was withdrawn.

Applied to the tex at return time: **nothing**.

## After Marc rules

Apply exactly the accepted items — no opportunistic extras riding an accepted
proposal. Log accepted/rejected in the active drafting handoff (rejections
become do-not-re-flag entries), flip any registry statuses he ruled, bump
`terminology.md`'s `updated`. Then hand off: "section is through pass 6; the
integration check is next."
