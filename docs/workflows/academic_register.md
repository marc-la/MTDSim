---
status: durable
created: 2026-08-20
updated: 2026-08-20
---

# Academic register — the target conventions for the section voice pass

**Status:** durable. The conventions of academic writing in computer science and
security that pass 6 (the `voice-pass` skill) converges dictation-derived prose
onto. Load before running pass 6 on any assembled section, alongside
[`voice.md`](voice.md) (what must survive the conversion) and
[`terminology.md`](terminology.md) (the one-term-per-concept registry).

Division of labour: [`voice.md`](voice.md) owns Marc's voice — the floor the
conversion may never sand through. [`critique_protocol.md`](critique_protocol.md)
owns reviewer conduct (edit tiers, banlist) and the Gopen & Swan sentence
diagnostics. [`literature_conventions.md`](literature_conventions.md) owns the
field-specific layer (ATT&CK referencing, metric discipline, methods genre).
This file owns the **general academic register** — what separates written
academic prose from careful speech — and the inventory of spoken residue the
dictation pipeline leaves behind. Sources for every rule are at the foot; none
of this is taste.

## (a) The calibration dial (Marc's ruling, 2026-08-20)

The draft arrives as repaired dictation: the voice is present by construction,
but so is speech. Two failure modes, named:

- **Under-converted** — reads as transcribed conversation: spoken idiom, vague
  quantifiers, conversational connectives. Fails the register.
- **Over-converted** — AI-flattened: the assessor-named defect that cost marks
  once (voice.md §b). Fails worse.

The middle ground sits **closer to the academic side**. The tiebreak: Marc's
voice survives in the *argument moves* (voice.md §c) and the *licensed devices*
(voice.md §d) — not in spoken idiom. When a sentence must lose one, it loses
the idiom, never the argument shape. A conversion that touches a §d device or
the working vocabulary has overshot.

## (b) Register conventions

1. **Contractions expand** (*don't* → *does not*) — universal in formal CS
   prose (Zobel; Day & Gastel). Marc's standing 3b global rules any exception.
2. **Person is a global, held consistently.** *We* is conventional in CS even
   for single-author theses; *I* is licensed where the decision is genuinely
   the author's own ruling. The choice per context is Marc's; the pass
   enforces only consistency with his rulings, never normalises unasked.
3. **No second person; no imperative address to the reader.**
4. **Vague quantifiers become numbers, calibrated scopes, or nothing** —
   *a lot of*, *quite*, *pretty*, *really*: the field writes the number
   (Zobel's economy; Day & Gastel's precision; literature_conventions §e2
   "numbers over adjectives").
5. **Colloquial and phrasal informality is proposed up only where register
   genuinely breaks** (*figure out* → *determine*, *deal with* → *address*,
   *get* → the specific verb). No reflexive Latinisation: plain words are good
   CS style (Zobel prefers them), and formality inflation is a flatten route.
6. **Anthropomorphism is bounded.** Cited authors act (*Brown models…*);
   artefacts may *do* mechanical things (*the controller selects*) but never
   *want*, *try*, *believe*, *care*.
7. **Boosters are removed** (*clearly*, *obviously*, *of course*, *very*) —
   the number or mechanism carries the force (Hyland on boosting;
   critique_protocol §e6).

## (c) Tense

Present for the artefact and for established knowledge (*the net carries*,
*ATT&CK defines*); past for actions taken and experiments run (*the corpus was
mined*, *runs were seeded*); present for cited claims with the author as
subject (voice.md §d). One tense regime per passage — drift between them inside
a paragraph is a defect (Day & Gastel; Zobel).

## (d) Hedging

Hedging is the genre's epistemic honesty, not weakness (Hyland): a claim
carries exactly the hedge its evidence needs, scoped to the uncertain
constituent, and commits on the rest. Over-hedging reads as evasion;
an unhedged claim past its evidence violates the modest-claim ceiling
(voice.md §c7). One calibrated hedge, then commit — hedge-stacking rules per
voice.md §h (epistemic layering stays licensed).

## (e) Economy — the vacuous-sentence test

Pass 6's cut sweep. A sentence survives if **all three** hold:

1. it advances the unit's question (the skeleton comment names it);
2. it says something no earlier sentence in the section already said;
3. removing it would change the reader's understanding.

Restatements, previews of what the next sentence says anyway, performative
frames (*it is worth noting…*), and content belonging to another chapter's job
(the section boundaries in the drafting handoff) are cut candidates. Never cut
candidates: must-carry disclosures, numbers, citations, ruled-in sentences
(the pass-5 never-cut list carries over).

## (f) Cohesion, sentence mechanics

Owned by [`critique_protocol.md`](critique_protocol.md) §e (Gopen & Swan:
topic position, stress position, subject–verb proximity, nominalisation,
proposition count) — apply from there; not duplicated here.

## (g) One term per concept

Owned by [`terminology.md`](terminology.md), the living registry. The rule
itself is the field's (Zobel: use terms consistently; elegant variation is for
objects, not concepts — already voice.md §e). Pass 6's sweep 3 enforces it.

## (h) The spoken-residue inventory (living — append survivors as they recur)

Residue that survives passes 2–5 into assembled sections, with the standard
move for each:

| Residue | Move |
|---|---|
| sentence-initial *So / Now / Again / And so* | delete, or replace with the logical connective the argument implies |
| *basically*, *essentially*, *sort of*, *kind of* (survivors) | delete |
| *a bit*, *a lot of*, *pretty*, *quite*, *really* | the number, a calibrated scope, or delete (§b4) |
| *thing(s)* as a content noun | give it its noun |
| naked *this / these / it* with ambiguous referent | attach the head noun (critique_protocol §e2) |
| *get / got*, *deal with*, *figure out*, *look at* (where informal in context) | the specific verb (§b5) |
| contractions | expand (§b1) |
| *obviously / of course / clearly* | remove the booster (§b7) |
| *etc.*, *and so on* in argumentative prose | close the list or bound it (*among others* only if the openness is the point) |
| spoken emphasis by repetition (*very, very*) | one word, or the mechanism |

What is **not** residue and never converts: Marc's parenthetical status asides,
paired opposition, short verdict sentences, two-beat anaphora, the working
vocabulary (*defensible, grounded, tradeoff, distil*), rhetorical questions
that are real and answered — the voice.md §d licence list, verbatim.

## Sources

- Zobel, *Writing for Computer Science*, 3rd ed., Springer 2014 — CS register,
  economy, terminological consistency (§b, §e, §g).
- Day & Gastel, *How to Write and Publish a Scientific Paper* — tense
  conventions, precision (§b, §c).
- Hyland, *Hedging in Scientific Research Articles*, Benjamins 1998; and
  "Boosting, hedging and the negotiation of academic knowledge" (1998) — §b7, §d.
- Gopen & Swan, "The Science of Scientific Writing" (1990) — via
  critique_protocol §e; local copy `../sources/gopen_swan_1990_science_of_scientific_writing.md`.
- Williams, *Style: Lessons in Clarity and Grace* — economy, cohesion.
- Swales & Feak, *Academic Writing for Graduate Students* — genre moves (via
  critique_protocol §d).
- The 2026-08-20 corpus survey — the field-specific layer, in
  [`literature_conventions.md`](literature_conventions.md).
- Canon re-checked against current web sources 2026-08-20; stable.
