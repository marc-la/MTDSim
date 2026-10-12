---
status: durable
created: 2026-09-30
updated: 2026-09-30
provenance: distilled from the thesis-writing literature for the chapter 2 scrutiny (handoff 2026-09-30_ch2_background_scrutiny.md); sources read in full unless marked second-hand
---

# Background conventions: what a background chapter is for, and how it fails

**Status:** durable. Load this before drafting, scrutinising or cutting chapter 2.
It is the chapter-level yardstick. [`voice.md`](voice.md) §(0) governs the
sentences, [`connective_prose.md`](connective_prose.md) the opener and the close,
and `.claude/skills/scrutinise-figure/diagram_best_practice.md` the figures. This
file does not repeat them.

## (a) What the chapter is for

- **It holds the knowledge the reader needs in order to follow the contribution.
  It does not hold the alternatives the contribution supersedes** (Zobel 2004,
  *Writing for Computer Science*, 2nd ed., pp. 146–147). The first belongs in
  chapter 2 and the second in chapter 3. This is the published basis for the
  README's first placement test.
- Its content is the definitions and usages the thesis relies on, plus the
  existing theory and practice it builds on (Evans, Gruba & Zobel 2014, *How to
  Write a Better Thesis*, 3rd ed., p. 81). In a CS thesis that includes the earlier
  model the work extends (Nijssen, Leiden BSc CS guidance, slides 8–10).
- It is written for "the 'you' that you were at the start of the research
  project" (EGZ p. 73): a CS undergraduate who is not a specialist in the area
  (Cambridge CST Part II, *The Dissertation*).
- It is "not an end in [itself]… merely the context for your own work" (EGZ
  p. 81), and it "must directly foreshadow the core" (EGZ p. 11).

## (b) What the two readers expect

- **The student.** Every term is defined at first use, in words the student
  already has: "Don't create questions by defining in terms of concepts that are
  unknown" (Zobel 2004 p. 43). The standing risk is the "95 per cent syndrome".
  Writers assume the basics their field takes for granted and write only the 5
  per cent that is new (EGZ pp. 76–77).
- **The examiner.** Examiners form their first judgement within the first two
  chapters, and read more critically after a poor start (Golding, Sharmini &
  Lazarovitch 2014, *Assess. Eval. High. Educ.* 39(5), §3). Presentation errors
  make them doubt the research (§5).
  - A sound vocabulary is *expected*, so it loses marks when it is weak and earns
    none when it is strong (Boote & Beile 2005, *Educ. Researcher* 34(6)).
  - UWA's CSSE marking guide asks for "a full and sound description of the
    background", for concepts defined and their origin given, and for correctly
    presented figures (CITS4001 dissertation marking guide; CITS4002 criterion 2).
- **Both readers** need the inherited starting point declared, and kept apart from
  what the thesis built (Cambridge, *The Dissertation*; TU Darmstadt,
  *Requirements for Scientific Theses in CS*, p. 1).

## (c) Structure

1. **Context before detail.** The field comes before the instance, and why before
   what before how (Nijssen slide 12; Gopen & Swan 1990).
2. **Scope first, briefly.** "Keep this section short… it provides a map of the
   territory" (EGZ p. 74).
3. **Link both ways.** The opener says how the chapter builds on the introduction;
   pointers say where a term is used later; the close hands on to the next chapter
   (Zobel 2004 p. 147).
4. **Keep it short.** No source gives a percentage; all say condense (Edinburgh
   Informatics dissertation guidance; ANU Academic Skills). The ledger's 1 250 of
   about 14 000 words, roughly 9 %, is consistent with this.

## (d) Failure modes

| Failure | Test | Source |
|---|---|---|
| **Textbook dump** | Could this paragraph sit in any textbook on the topic? | EGZ p. 76; Cambridge |
| **Material never used later** | Name the later line that uses the fact. If there is none, cut it: "Be ruthless!" | EGZ pp. 81–82 |
| **Survey creep** | Does it name competing work or weigh limitations? If so, that is chapter 3's job | EGZ p. 81; Zobel 2004 pp. 146–147 |
| **Undefined or late-defined terms** | Is every term defined at or before first use, in known words? | Zobel 2004 p. 43; EGZ pp. 76–77 |
| **Everyday words as terms** | Do *shuffle*, *surface*, *layer*, *target* etc. have their technical sense pinned? | EGZ p. 80 |
| **Drifting terms** | One name per thing, the field's name kept unless there is reason to change it | Zobel 2004 pp. 52–53 |
| **The thesis's own design leaking in** | Is anything here chosen by the dissertation rather than inherited? Move it to chapters 4–5. A forward pointer names *where* a term is used, never what the thesis will build or find | EGZ pp. 81–82 |
| **Confusable neighbours** | Where a reader could merge two concepts, is the distinction stated? | EGZ p. 77 |
| **Missing links** | Examiners read in chunks and forget chapter 1 by chapter 5 | Zobel 2004 p. 147; Golding et al. §6 |

## (e) Floats

- **Every figure needs a job.** "If you don't have anything to say about an
  illustration, leave it out" (Zobel 2004 p. 112). Reserve figures for material
  that is central (p. 93).
- **Referenced before it appears, and standing alone with its caption.** The
  caption says how to read the figure (EGZ pp. 108–109, 133–134).
- **Complement, never duplicate.** A figure and a table carrying the same rows is
  one float too many (EGZ p. 108).
- **One view per diagram.** Show structure *or* process *or* state; combining them
  is "a common mistake" (Zobel 2004 p. 99).
- **Caption definitions.** Zobel (p. 111) allows a caption to expand notation. The
  supervisor's 2026-09-22 ruling, no definitions in captions, overrides this here.

## (f) The checklist, run per chapter pass

1. Every term, fact and float is used later, and the using line is named.
2. Everything a later chapter relies on without re-explaining is here.
3. The chapter names no competing work and weighs no limitations.
4. A non-specialist CS undergraduate can follow every paragraph.
5. Each term is defined at first use, in words the reader already has.
6. Each thing has one term, the field's where one exists.
7. Everyday words used as terms have their technical sense stated.
8. Each concept carries its origin (a citation).
9. Inherited work is kept apart from what the thesis built, and nothing the
   thesis chose is described as inherited.
10. Nothing from the thesis's own model, results or arguments appears.
11. Context comes before detail, and each paragraph opens on something already
    met.
12. The opener links back, the close hands on, and pointers say where a term is
    used.
13. Each float is referenced before it appears, carries what the prose does not,
    and stands alone.
14. No two floats carry the same content.
15. The chapter is brief and free of presentation errors.

## Sources and limits

Read in full:

- Evans, Gruba & Zobel 2014, ch. 6 (pp. 73–82) and the figure pages. The copy was
  OCR, so the page numbers could be off by one near p. 75.
- Zobel 2004, 2nd ed. Re-locate the pages before citing the 3rd ed.
- Golding, Sharmini & Lazarovitch 2014.
- Gopen & Swan 1990 (`../sources/`).
- The Cambridge, Edinburgh, ANU, TU Darmstadt, Leiden and Harvard guidance pages.
- The UWA CSSE marking guides.

Second-hand, through Golding et al.:

- Mullins & Kiley 2002.
- Holbrook et al. 2007 (abstract read).

Not read:

- Paltridge & Starfield's background-chapter chapter. Only Paltridge's Sydney
  handout was used.

No source gives a move sequence or a length specific to background chapters, so
§(c) is assembled from general guidance.
