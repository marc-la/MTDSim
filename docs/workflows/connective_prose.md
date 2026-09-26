---
status: durable
created: 2026-09-25
updated: 2026-09-26
provenance: distilled from two surveys run 2026-09-25 — the published guidance on thesis metatext (handbooks, applied-linguistics corpus studies, examiner-report studies, UWA guidance) and the chapter/section preambles of the four MTDSim lineage documents plus the supervisor's own papers; sources at the foot, access status marked
---

# Connective prose — chapter openers, section preambles, bridges

**Status:** durable. The conventions for the prose whose job is to join the
dissertation together: the **chapter opener** (between `\chapter` and the first
`\section`), the **section preamble** (between a `\section` and its first
`\subsection`), and the **bridge** (a sentence or short paragraph at the close of
a section or chapter that states what is now established and what it sets up).
Load before drafting, generating or critiquing any of them. It is also the
specification of the *integration check* that
[`drafting_pipeline.md`](drafting_pipeline.md) names after pass 6: that check
reads these units.

Division of labour: [`voice.md`](voice.md) governs how every sentence sounds
(its §h already bans empty signposting — this file says what replaces it);
[`academic_register.md`](academic_register.md) owns person, tense and numerals;
[`critique_protocol.md`](critique_protocol.md) owns reviewer conduct. Session
generation of these units is licensed (Marc, 2026-09-02: connective prose only,
ratify on read); this file is the bar that generated connective prose must
clear.

## (a) The one rule

**A connective sentence names what a part does for the argument, or what it has
established — never only what it is about.** Every source that prescribes
agrees on this: the overview must give "the logical connection between the
various sections", and one written as a table of contents "is far from helpful"
(Evans, Gruba & Zobel 2014, p. 48); sections are stated "not simply as topics,
but actually how they build up the internal chapter argument" (Thomson 2014);
previews "that read like a scrunched-up table of contents are there to help the
writer, not the reader" (Pinker 2014, via secondary quotation). The linguistic
form of the rule is Bunton's split between *writer acts* (how the text is
organised) and *research acts* (what was decided, derived, found): a connective
sentence that reports only a writer act has told the reader nothing the table
of contents did not (Bunton 1999, via Hyland 2005, p. 47).

The two failure modes the rule sits between:

| Under-dressed: the **laundry list** | Over-dressed: the **flourish** |
|---|---|
| "Section 2 presents X. Section 3 discusses Y. Section 4 presents Z." — one clause per section, identical syntax, no dependency between items. Swales & Feak use exactly this as their outline to critique (2012, p. 361, Task 18). | Significance asserted instead of named: *lays the foundation, sets the stage, provides valuable insights, crucial, a comprehensive overview* — the lineage's weakest preambles close this way. Zobel names the teaser form: interest "baited" with "surprising insights … with no hint as to what the surprises … were" (2014, p. 58). |
| Topic nouns only: *the network model, the defence mechanisms, the metrics*. | Metaphor doing the work of a claim: *thread, spine, lens, journey, landscape, bridge*. |
| Every subsection enumerated, even where its heading already says it. | The LLM tells in transitional prose (Wikipedia, *Signs of AI writing*): trailing *-ing* clause (*…, ensuring that…*); *not X but Y*; rule-of-three; *serves as / represents* for *is*; *Additionally* openers. |

The fix for both is the same move: replace the topic noun with **the operation
the part performs on the argument, and its dependency on the part before it.**

> Laundry list: *Section 4.1 describes the attack graph. Section 4.2 describes the attack profiles. Section 4.3 describes the Petri net.*
> Flourish: *Section 4.1 lays the foundation on which the profiles of Section 4.2 are built, before Section 4.3 brings them to life.*
> Functional: *Section 4.1 builds one attack graph from the corpus; Section 4.2 partitions it by objective into attack profiles; Section 4.3 gives each profile an execution semantics.*

(Schematic — the functional line illustrates the pattern, it is not ruled
text.) The functional line is not longer than the list; it carries the
dependency (*it* = the graph just built) and a verb that names a real
operation.

## (b) What each unit does

### Chapter opener — three moves, in this order

The handbook model is link → aim → how (Evans et al. 2014, p. 48; restated
p. 58–59), independently the same as Thomson's LINK → FOCUS → OVERVIEW (2014)
and Aitchison's backward → current → forward (2014):

1. **Link — why this chapter follows.** One clause or sentence stating what the
   previous chapter *established* that makes this chapter necessary: a finding,
   a gap, a commitment — not a topic ("the previous chapter reviewed…"). Evans
   et al.'s model link restates findings ("As found, …"), and "therefore"
   carries the new chapter from them (p. 49). Dunleavy's objection ("never link
   back"; "As I discussed in the previous chapter, dum de dum" is the ultimate
   low-energy opener) is an objection to topic links; a link that states a
   finding satisfies both camps. In the first chapter after the introduction the
   link is to the research question.
2. **Aim — what the chapter establishes, and for which part of the research
   question.** Stated as the chapter's job in the argument. Context before
   contribution: an opener that starts "This chapter…" before the reader knows
   why tends to state its content out of context (Zobel 2014, p. 97). Aim before
   substance: if the reader meets pages of material before learning why the
   chapter is there, they are confused (Evans et al. 2014, p. 49).
3. **How — the sections by the role each plays, connected.** One clause per
   section, carrying the dependency between them (see §a). A figure that already
   draws the chapter's structure may carry this move; the opener then points at
   the figure once instead of re-walking it.

**Scale.** Evans et al.'s "about three paragraphs" is PhD scale. Hyland's
corpus shows metatext density scales with length (2005, p. 56); at honours
scale the three moves fit **one paragraph, roughly 60–150 words** — the lineage
theses' openers have a median of about 105 words (Zhang 2023; Tay 2024).

### Section preamble — required, short, and carrying the shared frame

1. **It exists.** "It is bad form to immediately follow a section heading with a
   subsection heading … Every component of your thesis needs an introduction"
   (Evans et al. 2014, p. 49). A heading followed only by a figure or only by
   another heading fails this (Wikipedia's *Signs of AI writing* also lists
   "headings only containing other headings").
2. **It states the section's job and the logical connection between its
   subsections** — the chapter-opener rule one level down, which Evans et al.
   license explicitly ("the same principle should be applied at a more
   fine-grained level", p. 128).
3. **It may carry what every subsection shares** — a definition, a common frame,
   the assumption the subsections rest on. The lineage's best section preambles
   do exactly this: a single definition whose parts *are* the subsections
   (*what, when, how to move*: Zhang 2023 §2.1; Tay 2024 ch2), or each component
   with its modelling choice (Brown 2023 §III). The supervisor's own papers put
   the argument or assumption first and the section list last (Hong et al.
   2018, §3, §4, §6).
4. **Brief.** Signposts "are informative but brief … not previews or
   mini-guidebooks to an argument to come" (Dunleavy, LSE 2014). Two to four
   sentences, roughly 30–90 words (lineage median about 72).

### Bridge — what is now established, what it sets up

1. **Where.** At a section close or chapter close, only where the next unit
   depends on a result of this one (Aitchison 2014; Thomson 2011: meta-commentary
   at the beginning and end, "once or twice in the middle").
2. **What it says.** What is *established now that was not at the start* (Evans
   et al. 2014, p. 50) — and, optionally, what that sets up next. Never a list of
   what was covered: examiners' most common complaint about chapter summaries is
   that "the author is still writing a list of the chapter contents" (p. 128).
3. **How long.** One or two sentences at section level; "about a paragraph" at
   chapter level (Thomson 2023). A bridge restating the section is cut.
4. **Built from content, not connectives.** The link is the old-information
   noun carried across, not *Moreover* or *Having discussed X* (Swales & Feak
   2012, pp. 48–49: if there is no content bridge, make one before reaching for
   a linking word).

## (c) Person, tense, reference

1. **Present tense for what a chapter or section does**: *Section 4.2 derives…*
   Future is marked wrong for outlining contents (Evans et al. 2014, p. 30); the
   lineage's *will introduce* is one of its defects.
2. **Person follows the standing ruling** ([`academic_register.md`](academic_register.md)
   §b2): chapters 1–3 impersonal, *we* licensed from chapter 4. The only
   UWA-specific marking rule on this is **consistency** — "a consistent style,
   person and tense" (CITS4001 marking guide).
3. **Section-as-agent takes presentational verbs** (*defines, derives, builds,
   compares, lists, measures*); **arguing verbs belong to an author** (*we
   argue*) or the claim is stated flatly. Zobel objects to "this section argues"
   because it implies the text, not the author, is arguing (2014, pp. 81–82);
   Evans et al. and Paltridge & Starfield model *This chapter + present verb*.
   The reconciliation is the verb class.
4. **References are `\ref`, never typed numbers, and every one resolves.** The
   stale roadmap — a preview naming a section that does not exist or has
   moved — recurs across the lineage and the papers (Tay 2024 §4.3; Reti 2022;
   Zaffarano 2015). After any restructure, re-read every connective unit.
5. **Terms are the body's terms.** A preview is where a reader first meets the
   name of what is coming, so it must use the registry term
   ([`terminology.md`](terminology.md)); a preview that names a thing
   differently from its heading or its section is the sloppiness signal
   [`academic_register.md`](academic_register.md) §i10 warns about.

## (d) Density and variation

- **Explicit signposting is the CS norm, not a lapse.** Computer science had the
  highest rate of frame markers of six disciplines in Hyland's 240-dissertation
  corpus (35.4 per 10 000 words; 2005, p. 57); outlining structure is common in
  technological fields and obligatory in theses (Swales & Feak 2012, p. 360).
  Examiners mark *too little* signposting down as well: a high-quality thesis
  "consistently (but not repetitively) reminds the reader of the purpose,
  argument, or overall thrust" (McDonald, via Evans et al. 2014, p. 153).
- **But not a nagging GPS.** Over-signposting is the named opposite failure
  (Haag, via Thomson 2023; Guerin 2014: "don't become too repetitive in
  announcing what will be done and what has just been done"). Scaffolding that
  helped drafting is removed in revision (Thomson 2025). No sentence previews
  what the next sentence says anyway ([`academic_register.md`](academic_register.md) §e).
- **Vary the structure, never the terms.** UWA's own checklist asks whether each
  chapter's introduction and conclusion is "varied enough" (STUDYSmarter HM6);
  Zobel warns that a synonym is usually less specific (2014, p. 108). Vary the
  entry point and syntax across the chapter openers; hold every technical term.

## (e) The check — run on every connective unit

Yes/no, per unit. A *no* is a finding; cite the item.

1. **Exists?** Every chapter with sections has an opener; every section with
   subsections has a preamble (§b).
2. **Link carries a finding?** The opener's link states what was established, not
   what was covered (§b opener 1).
3. **Aim stated as a job?** The reader learns what the chapter or section
   establishes, and for which part of the research question, before its
   substance (§b opener 2).
4. **Roles, not topics?** Every clause naming a part carries a verb for the
   operation it performs — no clause is a bare topic (§a).
5. **Dependency shown?** At least one clause says how one part follows from or
   feeds another; the parts are not an unordered list (§a; Evans et al. p. 48).
6. **No flourish?** No significance assertion, teaser, value close, metaphor for
   a claim, or §a LLM tell; no *not X but Y* (§a; voice.md §h).
7. **No duplication?** Nothing the heading, the figure it points at, or the next
   sentence already says (§d).
8. **Tense, person, agent right?** Present; person per the ruling; section-as-agent
   with presentational verbs only (§c1–3).
9. **References resolve and terms match?** Every `\ref` points at the section it
   describes; every name is the registry and heading term (§c4–5).
10. **Scale right?** Opener one paragraph, section preamble two to four sentences,
    bridge one or two (§b).
11. **Varied?** Set the chapter openers side by side: the same skeleton three
    times is a redraft signal (§d; voice.md §h symmetric openers).

## (f) Rulings (Marc, 2026-09-26)

The sources and the lineage disagreed on three points; Marc ruled each on
2026-09-26, and these rulings bind every later connective unit.

1. **Chapter-closing bridges: only where the next chapter depends on a
   result.** The prescriptive sources want every chapter to close on what it
   established (Evans et al. 2014, p. 50; Dunleavy, LSE 2014; Thomson 2023);
   no lineage document does. Ruled middle course: chapter 2 closes on one
   sentence handing its baseline attacker to chapter 3's scoring; chapter 3
   closes on the gap chapter 4 answers; chapter 4 has no close, because
   chapter 5's opener carries the link. A close is one sentence, and "as long
   as it's clear".
2. **Chapter 1 carries a thesis-structure overview**, placed last in the
   introduction, after the contributions. The structure step is the final
   move of a thesis introduction (Bunton 2002, via Paltridge & Starfield 2007,
   p. 83; Swales & Feak 2012, p. 360); after the contribution list it need not
   repeat what the contributions say of the chapters they point at. It is
   written as a synopsis of the storyline, not a table of contents (Evans et
   al. 2014, p. 67): each chapter by what it does, and the dependency carried
   between them. A clause describing an undrafted chapter is re-checked when
   that chapter is drafted (§c4).
3. **Section or chapter as the subject of a preview** (*Section 4.2
   partitions…*); *we* is kept for decisions (*We chose…*), per §c3.

## Sources

Access status: **read** = the session read the source; **secondary** = the claim
is reported by a source that was read; the survey records are in the session
scratchpad of 2026-09-25, not committed.

- Evans, D., Gruba, P. & Zobel, J. (2014). *How to Write a Better Thesis*, 3rd
  ed. Springer — **read**; pp. 30, 48–50, 58–59, 67, 123, 128, 153. The single
  most specific source; Australian, with a CS co-author.
- Zobel, J. (2014). *Writing for Computer Science*, 3rd ed. Springer — **read**;
  pp. 58, 81–82, 97–98, 108, 242.
- Swales, J. M. & Feak, C. B. (2012). *Academic Writing for Graduate Students*,
  3rd ed. — **read**; pp. 48–49, 148, 324, 360–361.
- Hyland, K. (2005). *Metadiscourse*. Continuum — **read**; pp. 47, 55–59
  (the 240-dissertation corpus, same study as Hyland 2004, *JSLW* 13).
- Paltridge, B. & Starfield, S. (2007). *Thesis and Dissertation Writing in a
  Second Language*. Routledge — **read**; pp. 49–50, 78–79, 83–91, 135–136.
- Bunton, D. (1999). The use of higher level metatext in PhD theses. *ESP* 18,
  S41–S56; Bunton, D. (2002). Generic moves in PhD thesis introductions —
  **secondary**, via Paltridge & Starfield and Hyland 2005.
- Thomson, P., *patter* (blog): "signposting your journal articles and chapters"
  (2011); "connecting chapters/chapter introductions" and ".../chapter
  conclusions" (2014); "can you have too much signposting?" (2023);
  "productive redundancy" (2025) — **read**.
- Dunleavy, P. (2003). *Authoring a PhD*. Palgrave — **secondary**, via the LSE
  *Writing for Research* posts "start each chapter cleanly. Never link back"
  (24 Jan 2014) and "Seven questions to ask about how your chapter ends"
  (12 Feb 2014).
- Pinker, S. (2014). *The Sense of Style*, ch. 2 — **secondary** (quoted in
  blogs; no page).
- Aitchison, C. (2014); Guerin, C. (2014), *DoctoralWriting SIG*; Cayley, R.
  (2011), *Explorations of Style* — **read**.
- UWA CSSE, CITS4001 *Dissertation Marking Guide* — **read** (page header says
  2016; confirm no newer rubric); UWA STUDYSmarter, *Survival Guide: Thesis
  checklist and tips* (HM6) — **read**.
- Wikipedia, "Signs of AI writing" (fetched 2026-09-25) — **read**; the
  transitional-prose tells in §a.
- The lineage: Brown et al. 2023; Zhang 2023; Ho 2024; Tay 2024; and Hong et al.
  2018 — every opener, preamble and closing paragraph coded for its moves
  (`docs/sources/lit_review/`, gitignored). Headline counts: chapter openers in
  10 of 15 sectioned chapters (median about 105 words); section preambles in 11
  of 19 sections with subsections (median about 72 words); chapter-closing
  summaries or bridges in 0 of 15.
