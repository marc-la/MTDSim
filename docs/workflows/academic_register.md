---
status: durable
created: 2026-08-20
updated: 2026-09-22   # §(i) added: the reader-overhead term screen (pass 6, sweep 4) with its sources; register E2
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
   prose (Zobel; Day & Gastel). **Ratified as a standing global (Marc,
   2026-08-20): expand, everywhere in dissertation-bound prose** — no longer a
   3b item; executed mechanically at pass 2/3a (`repair-dictation`). This
   supersedes the earlier §4.2-preamble "contractions stay" ruling.
2. **Person is a global, held consistently.** *We* is conventional in CS even
   for single-author theses; *I* is licensed where the decision is genuinely
   the author's own ruling. The choice per context is Marc's; the pass
   enforces only consistency with his rulings, never normalises unasked.
   **Ruled 2026-09-08 (Marc, on §3.3.2 P1):** chapters 1–3 are the
   objective view and stay impersonal — the agent is *this thesis* /
   *this section* / the cited authors; *we* is licensed from chapter 4 on,
   where the thesis's own model is the subject. Quoted *we* inside a
   citation is exempt. The pass flags a pre-ch4 *we* as a [3b], never
   normalises it.
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

## (i) Reader overhead — the term screen (pass 6, sweep 4)

**Why it exists.** The supervisor's 2026-09-22 ruling (register E2) named the
marking mechanism: every term a reader has to carry without a reason is
"another step of confusion", and each one lowers the top of the mark range.
The examiner literature says the same of presentation defects generally —
sloppiness "flips" an examiner from reading for content to reading for fault,
and the judgement forms in the first pages (Mullins & Kiley 2002; Golding,
Sharmini & Lazarovitch 2014; Johnston 1997). Clarity is the main game;
anything that detracts from it is the low-hanging fruit an examiner reaches
for first. This section is the screen a session runs on a section, as yes/no
checks; `tools/term_screen.py` is its mechanical half. It binds to no thesis
term — it is a filter, and a rule that would *add* a term to satisfy it has
misread it.

**The checks.** Each: the question, the source, the standard move.

1. **Needs basis.** Does every name this thesis introduces (as opposed to a
   field term) do work no plain description would — one object the reader
   must track, used often enough to be worth naming? If not, the name goes
   and the description stays; no naming sentence replaces it (E2; Zobel
   pp. 115, 120 — "consider whether your terminology conveys the intended
   meaning (or any meaning at all) to likely readers"; Strunk rule 13).
2. **Field term first.** Where the field has a term, is it the one used, and
   is a coinage made only where none exists — and then said to be a coinage
   at the coining? (Zobel p. 115: existing terminology "should only be changed
   with good reason … any change is likely to make your paper harder to
   read"; ISO 704 §7.4.2.3–4.)
3. **Defined once, at first use, in one format.** Is every term, symbol and
   acronym defined the first time the reader meets it — headings and captions
   included, since a caption is often the first place a term is met — and is
   the definition never moved or restated differently? (Zobel pp. 107, 119,
   192; IEEE Editorial Style Manual §II.E.)
4. **One name per concept, one concept per name.** No synonym rotation on a
   technical thing; no ordinary word given a technical sense without saying
   so (*layer*, *phase*, *level* all carry an everyday reading); no word used
   in two senses in one section. (Zobel pp. 108, 115–117: "technical concepts
   should always be described in the same way, not by a series of synonyms";
   ISO 704 §7.2 monosemy; voice.md §e.)
5. **Acronyms earn their place.** Expanded at first use in the body (and in
   the abstract), used often enough to repay the flip-back, few in total; a
   one-use acronym is written out. (Zobel pp. 119–120; IEEE §II.E; Barnett &
   Doubleday 2020 — 79 % of acronyms in the literature appear fewer than ten
   times, and the surfeit is what makes papers hard to read.)
6. **Qualifiers mean something.** A qualified name beside its unqualified
   parent (*APT attacker model* beside *attacker model*) carries an adjective
   that states the relationship, and the two name distinct objects — never a
   fancy name for the same thing. (Zobel p. 115: "choose a meaningful
   adjective"; the registry's distinct-objects rule.)
7. **Floats speak the text's words.** Every label, key entry, tick name,
   column header, row group and caption uses the body's exact term;
   abbreviations on a float are expanded in its caption or the sentence that
   reads it. (Zobel pp. 158, 176–177; Rougier, Droettboom & Bourne 2014, rule
   4; the UWA CSSE marking guide's "figures and their legends … correctly
   presented".)
8. **Notation minimal and fixed.** A symbol is introduced once, in the
   notation table or at its defining sentence, and never renamed; new
   notation only where prose cannot carry the object. (Zobel pp. 137, 192.)
9. **The first pages agree with the chapters.** Abstract, introduction and
   conclusion use the chapters' names — examiners read those first and form
   the judgement there. (Mullins & Kiley 2002 p. 376; Golding et al. 2014
   p. 574.)
10. **No sloppiness signals.** A stale name in a heading, a caption that no
    longer matches its figure, a typo, a referencing slip: each is read as
    evidence about the research, not the prose, and flips the examiner into
    fault-searching. (Mullins & Kiley 2002 pp. 378, 383–385; Golding et al.
    §5; Johnston 1997.)

**The mechanical half.** `python tools/term_screen.py` — `census <terms>`
(per-term counts by body / heading / caption / float / comment: the validation
gate after any re-terming); `acronyms --chapter N` (first use, and whether an
expansion accompanies it — check 5; it reads only the parenthetical form, so a
bold in-cell expansion is a false "never"); `phrases --chapter N` (multi-word
phrases first appearing in the chapter and recurring there — the candidates
for checks 1–3: each is a field term, a term defined at first use, or a term
to remove); `variants` (one two-word concept spelt more than one way — check
4). What the tool cannot judge — whether a phrase is a field term, whether a
definition is adequate, whether a qualifier means something — the session
judges and Marc rules.

**The ledger form.** One row per finding: the term → the check it fails →
one proposal (remove; replace with the field term; define at first use;
expand; re-key the float), with the census. Grouped: names that do no work
first (the mark-costing class), then definitions, then acronyms, then floats.

## Sources

- Zobel, *Writing for Computer Science*, 3rd ed., Springer 2014 — CS register,
  economy, terminological consistency (§b, §e, §g); definitions, jargon,
  acronyms, notation, floats and consistency editing (§i: pp. 107–120, 137,
  158, 176–177, 192–193).
- Mullins & Kiley, "'It's a PhD, not a Nobel Prize': how experienced examiners
  assess research theses", *Studies in Higher Education* 27(4), 2002 — the
  reading order (p. 376), sloppiness as a rigour signal and the "flip"
  (pp. 378, 383–385) (§i).
- Golding, Sharmini & Lazarovitch, "What examiners do: what thesis students
  should know", *Assessment & Evaluation in Higher Education* 39(5), 2014 —
  the synthesis of the examiner-report studies: first impressions, presentation
  errors, fault-searching (§5, p. 574) (§i).
- Johnston, "Examining the examiners", *Studies in Higher Education* 22(3),
  1997 — "reader-friendly" presentation; abstract and secondary quotation
  only (paywalled). Holbrook, Bourke, Lovat & Dally 2004 and Kiley & Mullins
  2004 (*IJER* 41(2)) are cited through Golding et al.; not read.
- ISO 704:2009, *Terminology work — principles and methods*, §7.2 (monosemy,
  one preferred term per concept), §7.3.3, §7.4.2.3–4 (§i).
- IEEE, *Editorial Style Manual for Authors*, §II.E — acronyms defined at
  first use in the abstract and the body (§i).
- Barnett & Doubleday, "The growth of acronyms in the scientific literature",
  *eLife* 9:e60080, 2020 (§i).
- Rougier, Droettboom & Bourne, "Ten simple rules for better figures", *PLoS
  Comput Biol* 10(9), 2014 — rule 4, captions (§i).
- UWA CSSE, *CITS4001 Dissertation Marking Guide* (teaching.csse.uwa.edu.au)
  — the presentation criteria, verbatim (§i).
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
