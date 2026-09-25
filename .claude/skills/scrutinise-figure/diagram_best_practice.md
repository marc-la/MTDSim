# Schematic figures — the design reference for scrutiny

Loaded by the scrutinise-figure skill for any **schematic** float: a method
overview, pipeline, model or architecture diagram, mechanism drawing. Compiled
2026-09-25 for the Figure 4.1 scrutiny from two passes:

- **The literature** — full record with quotations and page locators in
  `docs/sources/methodology/figure_design/_findings.md`, the OA sources beside
  it (gitignored, local only; the paywalled list is at its foot). This file
  carries the citations it needs so it works without them.
- **The corpus** — how fifteen papers this dissertation cites draw their
  overview figure, every figure rendered and page-located:
  `docs/implementation/evaluation_anatomies/_overview_figures_survey.md`.

**Transfer caveat.** Almost none of the literature tests a thesis overview
figure. It comes from science and mechanical diagrams (Tversky, Heiser), data
graphs (Franconeri, Rougier, Wong, Kosslyn), narrated lessons (Mayer), modelling
notations (Moody, Yourdon, UML) and architecture documentation (C4, Garlan &
Shaw, Bachmann). Every application below is by analogy: cite the principle,
never claim an experiment tested overview figures. The declutter evidence is
mixed (Franconeri et al. 2021 p. 131): cut an element because it is
*irrelevant to the message*, not to save ink.

## 1. What an overview figure is for

One job: the reader leaves able to restate the method in one sentence, knowing
what each part is and how the parts link. It is drawn from the argument's
outline, not from the code (Whitesides 2004 p. 1375–1376; Rougier et al. 2014
rules 1–2: know the audience, identify the message *before* drawing). It is
the "overview first" object; detail is reached deliberately in later figures
(Shneiderman 1996 p. 337, by analogy; the house family ruling of 2026-09-09).

## 2. Principles (cite these)

| # | Principle | Source (verified locator) |
|---|---|---|
| A | Arrows are read as direction in space, time or causality; their presence turns a structural reading into a process one. | Tversky, Zacks, Lee & Heiser 2000 pp. 226–229; Heiser & Tversky 2006 (abstract) |
| B | One arrow style carrying several meanings causes misconceptions; textbooks do it "with no visual way to disambiguate". | Tversky 2011 *TopiCS* 3(3) p. 521; Wong 2011 "Arrows" *Nat Methods* 8:701 |
| C | Lines read as paths and group what they join; a line that carries nothing misleads. | Tversky 2011 pp. 519–520; Franconeri et al. 2021 *PSPI* 22(3) p. 125 |
| D | One symbol, one meaning: overload (one symbol, several constructs) is the worst anomaly; also redundancy, deficit, excess. | Moody, Heymans & Matulevičius 2009 (RE'09) pp. 172–173 (Moody's Physics of Notations restated) |
| E | Different kinds of thing need visibly different symbols; shape is the privileged cue; text alone never distinguishes. | Moody et al. 2009 pp. 174–175 |
| F | Enclosure means containment or scope: a frame says "these belong together, apart from the rest". | Tversky 2011 pp. 522–523 |
| G | One diagram, one level of abstraction; split a complex picture into a family that zooms. | Brown, C4 model ("Introduction", FAQ); Moody et al. 2009 pp. 175–176 (complexity management); Yourdon, *Just Enough Structured Analysis* ch. 9 §9.3 (levelled DFDs, balanced inputs and outputs) |
| H | About four chunks at once (three to five); about six distinct symbol types at most. Miller's seven is not a box budget. | Cowan 2010 *Curr Dir Psychol Sci* 19(1); Kosslyn et al. 2012 *Front Psychol* 3:230 pp. 3–4, Table 1 p. 7; Moody et al. 2009 p. 178 (graphic economy); Yourdon §9.2.3 ("half a dozen") |
| I | Weed interesting but extraneous material; signal the path; put words next to what they name. | Mayer & Moreno 2003 *Educ Psychol* 38(1) pp. 46–49 (coherence, signalling, spatial contiguity) |
| J | Label in place rather than through a key or legend; mapping symbols to a key taxes working memory. | Franconeri et al. 2021 pp. 129–130; Kosslyn et al. 2012 p. 4; Jambor et al. 2021 *PLoS Biol* 19(3) pp. 13, 17 |
| K | The caption says how to read the figure and adds what cannot be drawn; a long legend-like caption is a symptom. | Rougier et al. 2014 rule 4; Jambor et al. 2021 p. 15 (Fig. 11); Nature formatting guide |
| L | A figure (with caption) should stand alone; authors cannot simulate a naive reader ("curse of knowledge"), so test on one. | Jambor et al. 2021 p. 15; C4 "Notation"; Franconeri et al. 2021 p. 127; Rougier et al. 2014 rule 7 |
| M | Draw the states, label the action between them in text ("A to B"); account for every element added or removed between steps. | Wong 2011 "The overview figure" *Nat Methods* 8:365 (preview read) |
| N | Things the work *uses* but did not build (a simulator, a corpus, a third-party agent) are outside the system boundary, drawn as external. | Yourdon §9.1.4, §9.2.3 (terminators, context diagram); C4 "System context" |

### Naming the parts

- A sequence where each part consumes the previous part's whole output
  artefact is a **pipeline of stages** (Garlan & Shaw 1994 pp. 6–7; strictly
  "batch sequential", p. 7).
- A **layer** is a part *built on and allowed to use* the part below it, in a
  hierarchy of increasing abstraction (Garlan & Shaw 1994 p. 11; Bachmann et
  al. 2000 pp. 11–13: stacking boxes does not make layers, "architects have
  been calling such things layered when they are not"). **Tiers** are
  deployment (Bachmann et al. 2000 p. 23).
- A **level** in the diagram literature is zoom depth: each level shows more
  detail of a part of the level above (Yourdon §9.3; C4 "levels of zoom").
- So a label like "L0 … L4" on sequential stages borrows hierarchy vocabulary
  for a sequence. Flag the mismatch against what the parts actually are; the
  naming ruling is Marc's (and the terminology registry records which words
  are already taken in this thesis — check it before proposing any).
- Nouns and verbs: data (artefacts) and processes are different element
  kinds, drawn differently (Yourdon §9.1: process names are verb–object
  phrases; UML 2.5.1 §15.4.4.1 vs §15.5.4.1), or artefacts drawn and
  processes as labelled arrows (principle M).

## 3. Corpus norms for an overview figure

From the corpus survey (per-paper evidence and page locators there):

- **Two genres.** *Pipeline* (method papers): three to five top-level boxes,
  one arrow meaning ("feeds the next"), parts called *step* or *stage*.
  *Architecture* (the MTDSim lineage — Tay, Ho, Zhang reports): component
  containers, often a loop, labelled arrows of several meanings, parts called
  *module* or *component*.
- **Captions are short.** 2–9 words in seven of ten overview figures, saying
  only what the figure is; the two outliers (He 2025 Fig. 2, 68 words;
  AttacKG+ Fig. 3, 55 words) are also the two densest figures.
- **Legends are almost absent**; where colour means something it is labelled
  in place or explained in the body.
- **Exemplars.** Ferraz et al. 2024 Fig. 2 (p. 6): input shape → three stage
  shapes → output shape, a row of verb phrases above the noun shapes, one
  accent on the stage that carries the contribution, the emulation platform
  not drawn as a step, 9-word caption — the closest content match (CTI to
  executable adversary behaviour). Rodriguez et al. 2024 Fig. 1 (p. 4): each
  step a process header over the artefact it yields, all at one depth. For an
  existing simulator: Tay 2024 Fig. 1 (p. 13) and Ho 2024 Fig. 1 draw it as a
  **container** with the new part beside it, never as a step.
- **What the corpus gets wrong** (and a reader will recognise): example data
  inside the overview (AttacKG+ Fig. 3, Zhuang 2012 Fig. 3), several unlabelled
  arrow meanings (AttacKG+, He, the Zhang report), the platform drawn as a
  step (Rodriguez's "System under attack" as step 1, Ferraz Fig. 1's "SUT
  Binding"), the new part drawn in more detail than the old (Tay Fig. 1).

## 4. The pitfall catalogue — run every test, record hit or clear with the count

| # | Pitfall | Test | Sources |
|---|---|---|---|
| P1 | **Arrow overload** | List every arrow; write the relation each denotes. More than one relation per arrow style = hit. | B, D |
| P2 | **Unlabelled or generic relations** | Cover the boxes: can each arrow's label alone say what passes or happens? Blank, "uses", "feeds" = hit. | C4 Notation, checklist |
| P3 | **Nouns and verbs in one form** | Classify each box label as thing (artefact, system) or action. Both classes in one visual form = hit. | D, E, M; Yourdon §9.1 |
| P4 | **Arrows on structural relations** | For each arrow: does something happen or flow here, in this direction? Containment, membership, "zooms into" = hit. | A |
| P5 | **Lines implying a path that is not there** | Name what travels along each line end to end. A line only for tidiness = hit. | C |
| P6 | **Stages named as layers, levels or tiers** | Does part *k* consume part *k*−1's output (stage), use it as a service (layer), or show it in more detail (level)? Name and relation disagree = hit. | Naming §2 |
| P7 | **Mixed abstraction** | For each element: a part of the method, or a part of a part (a sub-step, example data, a parameter, a file)? Parts of parts = hit; they go to a zoom. | G |
| P8 | **Too many top-level groups** | Squint and count the groups. More than four to six without chunking = hit. | H |
| P9 | **Visual vocabulary too large** | Count the legend entries the figure would need (shapes, line styles, meaningful colours, borders, icons). More than six = hit. | H (Moody p. 178) |
| P10 | **Meaningless variation** | For every visual difference, say what it means. "Nothing" or "undecoded" = hit. | Kosslyn 2012 Table 1; Rougier rules 6, 8 |
| P11 | **Legend dependence** | How often must the eye leave an element to learn what it *is*? Any content lookup = hit (a small, stable notation key is tolerable). | J |
| P12 | **Caption doing the figure's work** | Delete every caption sentence of the form "X is shown as / denotes Y". Figure unreadable now = hit. Over two such decodes = hit. | K |
| P13 | **No single message** | Write the one sentence; compare it with the figure-only cold reader's. Mismatch = hit. | L; Rougier rules 1–2 |
| P14 | **Terms the reader does not have** | Underline every term not in the abstract, introduction or the text before the figure, and not defined by the figure itself. Each = hit. | Kosslyn 2012 p. 4; Jambor p. 13; Franconeri p. 127; house antecedent rule |
| P15 | **Implementation detail instead of the idea** | Would the element survive a rewrite in another tool or language? No = hit. | Tversky 2011 p. 516; C4 System context |
| P16 | **Ambiguous reading order** | Trace the main path: count direction reversals, backward edges, crossings. Each needs a reason. | Jambor p. 12; Larkin & Simon 1987 p. 65 |
| P17 | **Family out of balance** | Each part's inputs, outputs and name in the overview vs its zoom figure and section heading. Any mismatch = hit. | G (Yourdon §9.3 balancing); C4 Introduction |
| P18 | **External system drawn as a step** | For each element: did this work build it, or use it? Used things inside the chain = hit. | N |
| P19 | **Grouping cues contradicting the units** | Ask a cold reader to circle the groups; compare with the method's real units (e.g. built once vs run per experiment). | F; Wong 2010 Gestalt |
| P20 | **No entry point, or everything emphasised** | Where does the eye land first? Is it where the method starts or where the contribution is? More than one or two emphasised elements = hit. | I; Rougier rule 6 |
| P21 | **Incomplete story** (house) | Does the figure show everything the introduction's approach paragraph says the method is, in its order and words, and nothing it does not? Missing part or foreign word = hit. | L; house rule: introduction terms fixed thesis-wide |

## 5. How the skill uses this

- **Step 1 [S]**: the one-sentence restatement and the part inventory are
  written against §1 and the naming guidance in §2.
- **Step 2 [S]**: the session's inventory counts feed P1, P8, P9, P10, P12,
  P14 directly.
- **Step 3 [S]**: the diagram auditor gets this file and runs §4 mechanically.
- **Step 5**: every amendment names the pitfall(s) it clears and the corpus
  exemplar it follows. A redesign that clears a pitfall by adding a legend
  entry or a caption sentence has not cleared it.
