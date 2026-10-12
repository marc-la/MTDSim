---
status: durable
created: 2026-10-02
updated: 2026-10-02
provenance: distilled from the thesis-writing and simulation-reporting literature for the chapter 4 scrutiny (handoff 2026-10-02_ch4_attacker_model_scrutiny.md); sources read unless marked second-hand
---

# Model chapter conventions: what a model-design chapter is for, and how it fails

**Status:** durable. Load this before drafting, scrutinising or cutting chapter 4.
It is the chapter-level yardstick. [`literature_conventions.md`](literature_conventions.md)
holds the field's norms for the same chapter, and
[`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md) the
ceiling on what it may claim. `background_conventions.md` §(e) (float rules),
`literature_review_conventions.md` (ch3), `literature_conventions.md` §d–e (metric definition,
threat-model subsection, version stamps), `evaluation_conventions.md` §k (a basis for every
value, run type, seeds) and `voice.md` §(0), §(c)3–10 already apply. This file does not repeat them.

## (a) What the chapter is for

- **It presents and argues for the contribution.** This part of a thesis is "where you begin to present and argue for that contribution" (Evans, Gruba & Zobel 2014, p. 83). The core is "a narrative leading from a proposition to an outcome, linked by evidence and argument" (EGZ p. 13).
- **For an innovation, the design comes with its expected properties and its criteria.** An innovation thesis needs "a discussion of the properties that the innovation is expected to have... and of criteria that it is intended to meet" (EGZ p. 85). The "hypothesis" is then "a complex bundle consisting of an innovation, discussion of anticipated properties... and explanation of criteria" (p. 89). Here the criteria are chapter 3's properties.
- **A described mechanism is worth nothing without the case that it works.** "An algorithm by itself is uninteresting; what is of value is an algorithm that has been shown to solve a problem" (Zobel 2004, p. 115). "When such demonstrations are absent, the reason for the absence should be clear" (p. 117).
- **It is the conceptual model, and it is judged against its purpose.** Conceptual model validity means the underlying "theories and assumptions" are correct and the representation is "'reasonable' for the intended purpose of the model" (Sargent 2011, pp. 185, 188). A model describes the system "relative to the particular issues that the model is to address", and "there should not be a one-to-one correspondence between the model and the system" (Law 2009, pp. 27–28).
- **It lets a reader rebuild the model.** Replication is "one of the key functions of this section" (Paltridge & Starfield 2007, p. 114). Algorithms are specified "in sufficient detail to allow them to be implemented without undue inventiveness" (Zobel p. 118). ODD's detail elements let a reader "completely re-implement" the model (Grimm et al. 2020, §1).
- **It lays the argument's foundations before results.** Here you address "likely sceptical concerns the examiners might have by examining and justifying your assumptions" (EGZ p. 93).

## (b) What the two readers expect

- **The student** needs the concepts before the steps. Prosecode "is only effective when the concepts underlying the algorithm have been discussed before the algorithm is given" (Zobel p. 117). "Mathematics should not take the place of text" (p. 73), and a symbol must be "familiar to, the reader" (p. 74). Specification languages such as Z are "cryptic to untrained readers", so ODD is written in plain English with equations where needed (Grimm et al. 2020, §3.3).
- **The examiner** checks five things:
  - *Justification.* "Examiners are specifically asked to check whether the methods you have adopted are appropriate, and whether you have justified your selection of them... the reader cannot read your mind" (EGZ p. 89). Justify the choice "even if it is standard for your discipline" (p. 95). Edinburgh lists "Justification of design decisions" and "Critical evaluation of one's own work" among its additional criteria (DISS, *Project Assessment*).
  - *Soundness.* UWA asks whether "the project, the set of experiments, development of the theoretical framework, method of implementation, or algorithm's design [is] sound", and whether the methods are "clearly described" (CITS4001 dissertation marking guide, *Methods*).
  - *Strengths and limits owned.* "A well-explained and justified approach, with clear acknowledgements of strengths and possible limitations, is more important than adhering to a predecided approach" (Golding, Sharmini & Lazarovitch 2014, §8).
  - *Declared equals done.* Examiners "looked to see that students were consistent and that they had actually done what they said they were going to do" (Mullins & Kiley 2002, p. 375; Golding et al. §8). Hence the model the chapter describes must be the model chapter 5 ran.
  - *Typical complaints.* King's examiner list (1996, via P&S p. 133): "insufficient justification for the choice of methodology"; "failure to recognize limits and parameters of methodology used"; "inadequate description of the development and testing of new instruments or techniques". "Mixed or confused theoretical and methodological perspectives" mark a poor thesis (Mullins & Kiley p. 379).
- **A thesis is more explicit than a paper.** Thesis methods are "more leisurely and explicit" than a paper's "extremely compressed" methods (Swales 2004, via P&S p. 115). The house rule "say more with less" (voice §0) resolves this: be explicit about choices, and let the floats carry the bulk.

## (c) Structure

1. **Purpose and criteria first.** ODD opens on "Purpose and patterns", the patterns being "model evaluation criteria" (Grimm et al. 2020, §1). Without "a list of the specific questions that the model is to answer, and the performance measures... it is impossible to decide on an appropriate level of model detail" (Law 2009, p. 27). The chapter opener can do this in two sentences that point back to Table 3.2.
2. **Overview, then parts.** ODD's hierarchy gives "an overview of the entire model before being asked to consider details" (§1). Zobel's *structure by specificity* suits a system with components: "begin with a review of this overall structure, then proceed to the detail of the elements" (p. 141). A chapter on a new algorithm may simply present its parts "in turn" (p. 147). STRESS item 2.1, the overview diagram, comes before item 2.2, the logic.
3. **State, then process.** ODD orders entities and state variables (element 2) before processes and scheduling (element 3), and both before the submodels (element 7). For chapter 4 that order is graph, then profiles, then formalism, then runtime traversal.
4. **The chosen design, then its rationale.** No source orders alternatives at the level of a single decision. EGZ's order, "first review the methods available to you, and then present reasons for selecting" (p. 89), is for the choice of *method*, and chapter 3 already makes it. ODD 2020 gives each element an optional *Rationale* subsection after its description (§4.2), and so supports putting the design first and each rejected alternative after it, in one clause. Alternatives are expected, but briefly:
   - "why a particular method was selected and not others" (P&S p. 119);
   - CS master's reports discuss procedures "that could have been followed but were not" (Harwood 2005, via P&S p. 123);
   - "Alternative solutions and their evaluation should also be included" (Edinburgh);
   - an exploratory choice between approaches can be "briefly sketch[ed]" with its outcome (Zobel p. 191).
5. **Measures: the sources disagree on placement.** STRESS defines outputs under *Objectives* (item 1.2), before the logic. Law also fixes performance measures at problem formulation (p. 27). ODD's *Observation* concept comes after the process overview. Either placement is defensible; what is fixed is that the measure is justified, which §(d) covers.
6. **Detail in the body only where it is needed for understanding.** ODD recommends a narrative *summary* in the main text and the full description in a supplement (§4.3). UWA limits this: material "essential to understand the dissertation... should not appear in an appendix", and large appendix text "may be considered as an attempt to circumvent the word limit" (CITS4001 project components). The test is whether chapter 5 can be followed without the appendix.
7. **Close by handing over.** Before results, "describe in detail the way that you applied the method, and why" (EGZ p. 94). The close names what chapter 5 runs.

## (d) Failure modes

| Failure | Test | Source |
|---|---|---|
| **Logbook narrative** | Does any paragraph tell the order in which things were built or tried? | EGZ p. 11 (Henry's "condensed diary"); Zobel p. 140 ("isn't a commentary on... day-to-day activities"), p. 142; Cambridge ("not... a day-by-day account") |
| **Implementation described instead of design** | Would the description survive a rewrite in another language? Are there code identifiers or programming notation? | STRESS Table 2, principle 3 ("software and hardware independent"); ODD §1; Zobel p. 123 ("Mathematical notation is preferable to programming notation"); Edinburgh (conceptual design apart from implementation) |
| **"We chose" without a reason** | Does each choice carry its reason, including standard ones? | EGZ pp. 89, 95; King 1996 via P&S p. 133 |
| **Rationale swamps description** | Can a reader find what the model *is* without reading why? | ODD §3.2–3.3 (rationale lengthens ODDs; keep it in its own subsection) |
| **Alternatives survey inside ch4** | Is a rejected option given more than a clause, or weighed against the literature? The weighing belongs in ch3 | Zobel pp. 146–147 (superseded alternatives are previous work); P&S p. 120 |
| **Unjustified simplification** | Is each non-trivial simplification stated with its reason? | Zobel p. 125 ("should be carefully justified"); Law p. 29 ("What simplifying assumptions were made and why") |
| **Hidden assumption** | Is every value or rule without a source declared as an assumption? | STRESS item 3.4; Sargent p. 187 (rationalism: "assumptions... clearly stated"); EGZ p. 93 ("dishonest to disguise the fact that some elements are essentially choices") |
| **Formalism whose conditions are unchecked** | Does the text show that the system meets the formalism's assumptions (e.g. the firing and timing semantics)? | Sargent p. 188 ("if a Markov chain is used, does the system have the Markov property") |
| **Measure without rationale** | Is each metric argued for, with the alternative measures it beat named? | EGZ pp. 90–92 ("measures are just too simplistic"); STRESS item 1.2 |
| **Too much or too little detail** | Could a reader implement each step without guessing, and is no loop spelled out that a formula says? | Zobel p. 118 (both directions) |
| **Limitations scattered or repeated** | Is each simplification owned once, beside the design, and restated once in the discussion? | Law p. 29 ("Limitations of the model"); P&S Fig. 8.1 (limitations a component of the chapter); Zobel p. 148 ("state (or restate)") |
| **Unrefuted objection left silent** | Is the objection an examiner would raise answered or conceded in the text? | Zobel p. 174 ("At the very least you should raise it yourself") |
| **Extension not separated from the inherited model** | Is the inherited model referenced and only the extension described? | STRESS §4.2 (the Yates et al. example: cite the original, describe the extension); Cambridge (declare the starting point) |
| **Description and code diverge** | Can each element be traced to the code that runs it? | ODD §4.6; Golding §8 |

Two consequences:
- **A limit of the model is owned in chapter 4; a limit of the findings in the discussion.** The sources place the *model's* simplifying assumptions and scope with the model (Law; Zobel p. 116, "the scope of application... and its limitations"; P&S Fig. 8.1). Limits of the *study's findings* go to the discussion. Chapter 4 therefore owns its design simplifications once, and §6.5 restates them once.
- **The parameter rule is already in `evaluation_conventions.md` §k1.** ODD adds only one thing: group parameters "according to the submodels in which they are used rather than providing a single large table" (§4.4).

## (e) Floats

1. **One overview figure of the whole model**, conceptual and simple in the body, with complex diagrams in supplementary material (STRESS item 2.1 and its §5 discussion of the logic section; ODD's "visual ODD", §4.3; Law p. 29, "process-flow... diagram").
2. **No flowcharts for algorithms.** Zobel gives five reasons, among them modularity, gotos and lack of room for text (p. 118). The runtime traversal reads best as numbered *prosecode* with explanatory text, or as *literate code* (pp. 117–122).
3. **Tables for lists.** Long lists of state variables go to tables (ODD §4.3). When there are many equations, summarise them "in tables and explain the rationale of each equation in the text" (§4.4). Group the parameter tables by submodel (§4.4).
4. **A worked trace.** *Structure by example* (Zobel p. 141) and Sargent's *traces* ("the tracking of entities through each submodel", p. 188) both justify one walked run of a single attack profile through the Petri net. It is both an example for the student and evidence of conceptual validity for the examiner.
5. **Optional: a conceptual-validity table.** Sargent recommends "an evaluation table for conceptual model validity", with a confidence column graded low, medium or high (§9, p. 193). It matches the per-axis badges in `apt_model_criterion.md`, if chapter 6 does not already carry them.
6. **Data structures as figures.** "Figures are an effective way of conveying the intricacies of data structures" (Zobel p. 119). This covers the attack graph and the failure matrix.

## (f) Checklist, run per chapter pass

1. The opener states the model's purpose and points to the criteria it answers (Table 3.2) before any design.
2. The whole model appears in one overview figure before any part is detailed.
3. State comes before process: graph and profiles, then formalism, then runtime traversal.
4. Each design element is described first, then given its rationale. Rejected alternatives get one clause each, and none is weighed against the literature.
5. Every choice carries a reason, including choices standard in the field.
6. Each non-trivial simplification is named with its reason. Each value with no source is declared as an assumption.
7. The formalism's conditions are shown to hold for the attacker process, or their failure is owned.
8. Each metric is defined, its direction stated, and argued for against at least one alternative measure.
9. No paragraph narrates build order or what was tried first. No code identifiers or programming notation appear.
10. Each step of the runtime traversal could be implemented without guessing. No step spells out what a formula already says.
11. Every symbol is introduced in words the reader already has. Text carries the argument, and the equations carry the precision.
12. Each simplification is owned once in chapter 4 and restated once in chapter 6, never repeated within the chapter.
13. The inherited simulator is referenced, and only the extension is described.
14. Everything chapter 5 needs is in the body. The appendix holds only detail needed for replication.
15. The described model is the model that ran: each element traces to code, and a worked trace shows one run.

## Sources and limits

Read (the cited pages):
- Evans, Gruba & Zobel 2014, *How to Write a Better Thesis*, 3rd ed., pp. 11–13, ch. 7 (pp. 83–95), p. 132 (OCR copy from the ch2 session).
- Zobel 2004, *Writing for Computer Science*, 2nd ed., pp. 69–75, ch. 7 (pp. 115–127), pp. 140–149, 173–175, 191–194.
- Paltridge & Starfield 2007, 1st ed., ch. 8 (pp. 114–133).
- Golding, Sharmini & Lazarovitch 2014, §8.
- Mullins & Kiley 2002, pp. 375, 378–379.
- Grimm et al. 2020, "The ODD protocol... second update", *JASSS* 23(2) 7 (`docs/sources/methodology/grimm2020_odd.md`).
- Monks et al. 2019, STRESS, *J. Simulation* 13(1), with checklist v1.1.
- Sargent 2011, WSC, pp. 183–194.
- Law 2009, "How to build valid and credible simulation models", WSC, pp. 24–33 (fetched from informs-sim.org/wsc09papers/003.pdf; not yet in `docs/sources/`).
- UWA CITS4001 dissertation marking guide and project-components page.
- Cambridge CST Part II, *The Dissertation*.
- Edinburgh DISS, *The Dissertation* and *Project Assessment*.

Second-hand:
- King 1996, Harwood 2005 and Swales 2004, all via P&S.
- Holbrook et al., via Golding et al.

Not read:
- Grimm et al. 2006 and 2010, known through the 2020 update and Monks et al.
- ODD supplements S1–S2 and TRACE (Augusiak et al. 2014).
- Law's 2007 textbook.

No source prescribes an order for the alternatives inside a single design decision, and none gives a length for a model chapter. §(c)4 rests on ODD's rationale placement, and EGZ pp. 93–94 say only that "practice varies a great deal between disciplines".
