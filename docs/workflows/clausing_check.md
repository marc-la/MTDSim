---
status: durable
created: 2026-10-18
updated: 2026-10-18
---

# Clausing check: the final register pass

**Status:** durable. This file defines the sentence-shape defects that AI redrafting leaves in academic prose, and grounds each one in style authority and measured evidence. It also sets the rules for fixing them by minimal edits. Built from Marc's read of pages i–15 on 2026-10-18; the first run (2026-10-18, applied in 80f64af9) is in `data/clausing_check/`.

**Division of labour.**
- [`voice.md`](voice.md) §h bans the *lexical* tells, such as *delve*, triads and "not X but Y".
- [`academic_register.md`](academic_register.md) §i screens *terms*.
- [`critique_protocol.md`](critique_protocol.md) §e holds Gopen & Swan's sentence diagnostics.
- This file covers the *structural* tells those lists miss: what punctuation is doing, where a nuance gets attached, and how a float or heading compresses. Each class below is something Marc found by reading, not by pattern matching. That is why they survived every earlier pass.

## 1. The eight classes

Each class gives its definition, Marc's instance, the rule it breaks (sources in §2), and the standard move.

**K1. The colon hinge.** A colon that joins a full clause to a sentence where the relation is really *because*, *so*, *for example*, or simply a second sentence.
- *Instance:* "Its attacker is the attacker model its training environment simulates: MTDShield's is the baseline attacker of Section 2.2.3."
- *Warranted colons stay.* They introduce:
  - a list the sentence announces by count or by *the following*;
  - an equation;
  - a quoted question;
  - the amplification of a claim, where the colon introduces the reasons the claim names. The reference case is §3.4's "depends on its attacker model: the attacker model decides…", which Marc read as acceptable.
- *Move:* split into two sentences, or rebuild the sentence around the real connective.

**K2. The appended phrase.** A short phrase after a sentence's last comma that attaches a nuance the sentence could have been built around.
- *Instances:* "…, by the part of the network each reconfigures"; "…and how each acts on the others"; "…, by the attacker's goal".
- *Rule:* the end of a sentence is its stress position, where the reader looks for the point. An appended qualifier puts a minor detail there.
- *Move:* make the nuance the head of the sentence, or cut it when the float or the next sentence already shows it.

**K3. The appositive gloss.** A definition slipped into a sentence about something else, as "X, a Y that Z, …".
- *Instances:* "with Attack Flow, a language from MITRE's CTID for recording…"; "an *impact*, the damage a successful exploit does"; "MTDShield, the reinforcement-learning agent of Tay".
- *Move:* a term the reader needs gets a copula sentence of its own ("Attack Flow is a language…"). A term the reader already has loses the gloss.

**K4. Narrative or figurative wording for a technical property.** A story or a metaphor where a defined term exists.
- *Instances:* "works deeper, level by level" (*levels of depth*); "opened down to" (*technique, sub-technique, procedure*); "the pool of Brown"; "stands for".
- *Move:* the defined term.

**K5. Vague or compressed float text and headings.** A caption or heading that compresses into a phrase naming nothing a reader could point to. Also:
- an unqualified head noun where a qualified term exists ("attacker models" beside *recent MTD attacker models*);
- sibling headings in different forms (Appendix C narrates; Appendix D labels without saying what it gives);
- a heading that carries its section's argument (§3.3.1).
- *Move:* a heading is one short noun phrase naming the topic, in the same form as its siblings. A caption's first sentence names what the float shows, in the body's terms. Its later sentences decode the encodings and nothing else ([`figure_table_conventions.md`](figure_table_conventions.md) §b2).

**K6. Term overload in one passage.** Several near-synonyms circling one idea.
- *Instance:* §2.1's *trigger, schedule, event, alert, move* for when an MTD moves. *Trigger* occurs twice in the whole dissertation and is never defined.
- *Move:* one term per concept, held verbatim ([`terminology.md`](terminology.md)). A word used once goes.

**K7. A needless definition, or an overclaimed mapping.**
- *Instances:* an emphasised definition of a term the dissertation barely uses (*impact*); a tidy correspondence that is not literally true. "Each word of the name stands for one property" announces three words and walks four properties.
- *Move:* drop the definition apparatus and keep the word. Delete the mapping.

**K8. Content the reader does not need.** A statement of absence nobody asked about, or a cell or column that carries nothing.
- *Instance:* "Tay states none."
- *Move:* delete. The test is [`academic_register.md`](academic_register.md) §e: would removing it change the reader's understanding?

**What is not a defect.** These stay ([`voice.md`](voice.md) §d):
- a semicolon in a deliberate paired opposition;
- Marc's parenthetical asides;
- a comma list that a count announces;
- a long sentence that is controlled and lands on a short one.

The comma itself is not the defect. §3 shows the dissertation uses *fewer* commas per sentence than the field. The defect is the job a comma is doing in K2 and K3.

## 2. What the literature says

This section was gathered on 2026-10-18. *(snippet)* marks a source seen only in search results, so it is not quotable. The Zobel page numbers are from a PDF copy; check them against the Springer edition before quoting any in the dissertation.

| Class | Style authority | LLM-text evidence | Grounded? |
|---|---|---|---|
| K1 colon hinge | Zobel p. 126: "Colons and semicolons are valuable but should not be overused." Trask: the colon's "only one major use" is that what follows is "an explanation or elaboration of what precedes it". Chicago 18th §6.65 limits it to "illustrating or amplifying" (via a secondary copy). Gopen & Swan: a *properly used* colon makes a secondary stress position, so the defect is overuse, not use. | **Runs against.** Desaire et al. 2023 found human scientists use colons *more* than ChatGPT in prose. LLM titles are colon-heavy (Sebo et al. 2026: 100 % vs 30 %). | Authority **yes**. Published LLM evidence **no** for prose. Our census (§3) shows the surplus in this text, not why it is there |
| K2 appended phrase | Gopen & Swan, "The Stress Position": readers "emphasize the material that arrives at the end of a sentence", so the new, emphasis-worthy information belongs there. Zobel p. 106: "the emphasis should be on the last two words, not the last five". Appending a fix to the end of a sentence "is clumsy. A complete revision is preferable". Zobel p. 125: "Sentences with many commas often have strangulated syntax; … consider breaking the sentence into shorter ones". | **Yes.** Reinhart et al. 2025 (*PNAS*): GPT-4o uses present participial clauses at 5.3× the human rate and nominalisations at 2.1×. The Wikipedia AI-cleanup catalogue (practitioner) names the "-ing" phrase "at the end of sentences". | **Yes / yes** |
| K3 appositive gloss | Zobel p. 102: "avoid nested sentences, that is, information embedded within a sentence that is not part of its main statement". Zobel p. 107: definitions "should be specific and concrete". | Indirect only: Reinhart's phrasal coordination (1.9×) and Herbold et al. 2023's "more complex sentences". | **Yes / partly** |
| K4 figurative wording | Zobel p. 77: "nuance, ambiguity, metaphor … are inappropriate for technical work". Zobel p. 115: idioms are "poor choices in scientific writing". Zobel p. 117: concepts "always described in the same way". APA 7 checklist §4.7–4.11: no "creative literary devices". | Style vocabulary is inflated: Kobak et al. 2025, 66 % of the excess words were verbs. Liang et al. 2024: "meticulous" ×34.7 in reviews. Figure-for-term substitution itself has not been measured. | **Yes / partly** |
| K5 captions and headings | Captions: Zobel pp. 176–177, captions "should be informative" and "fully describe the figure's major elements". Rougier et al. 2014 rule 4. The *Nature* guide: "a brief title … then a short description of each panel". Headings: Zobel pp. 95–96, "concise and informative, have specific rather than general terms"; "Accuracy is more important than catchiness"; sibling headings are parallel ("Lists" beside "Trees"). Zobel p. 196: "Is the style and wording of headings and captions consistent?" Thelwall 2020: poetic titles are "almost absent" from engineering. | LLM titles run longer (Sebo et al. 2026: a median of 16 words against 12.5). Captions and heading parallelism have not been measured. | **Yes / partly** |
| K6 term overload | Zobel p. 117: "not by a series of synonyms". ISO 704 §7.2 ([`academic_register.md`](academic_register.md) §i4). | Not measured. | **Yes / no** |
| K7 needless definition, overclaim | Zobel p. 120 and p. 196: an abbreviation used fewer than about four times should be removed. Extending this to defined terms is our inference. Zobel p. 83: "bold statements of conclusions based on flimsy evidence". | Indirect: Herbold et al. 2023, humans use more modals and epistemic markers. | **Partly / partly** |
| K8 unneeded content | Zobel p. 174: "be selective about the information you present". Zobel p. 177: "If you don't have anything to say about a figure or table, leave it out." Wilke ch. 23 on non-data ink, "within reason". | Practitioner only (Wikipedia, "unusual use of tables"). | **Yes / no** |
| Seamless editing (§4) | Zobel p. 192: "it is often preferable to make minimal changes: correct the presentation but retain the flavour of the original text." | Not measured. | **Yes** |

**What this licenses.**
- Every class rests on style authority. Zobel alone covers all eight, so the standard is academic convention, not taste.
- The LLM evidence is strong for K2 and K4, partial for K3, K5 and K7, and absent or contrary for the rest.
- So this file never claims a sentence is machine-written. It claims a sentence breaks a convention, and §3 shows where this text breaks it more often than its field does.
- The colon is the clearest case. The surplus is measured here, the convention is clear, and the published LLM evidence does not explain it.

## 3. What the census shows

`python tools/clause_census.py rates`, at HEAD 9b305af1. The baseline is 20 peer-reviewed field papers published before 2023, chosen as human-written text: 294 287 words from `_workspace/sources/_text/`.

**Colons, per 1 000 words.**

| | Colons | × field |
|---|---|---|
| Field papers before 2023 | 5.0 | 1.0 |
| All dissertation prose | 7.9 | 1.6 |
| Chapter 2 (Background) | 11.8 | 2.4 |
| Chapter 3 (Literature review) | 16.2 | 3.2 |
| Captions | 16.9 | 3.4 |
| Chapter 4 | 8.9 | 1.8 |
| Chapters 1, 5, 6 and 7 | 1.4–3.7 | ≤ 0.7 |

**Sentence shapes** (share of sentences, same heuristics run on both corpora):

| | Dissertation prose | Captions | Field |
|---|---|---|---|
| Words per sentence | 21.2 | 35.3 | 26.6 |
| Commas per sentence | 1.22 | 2.21 | 1.52 |
| Four or more commas | 4.4 % | 27.7 % | 11.4 % |
| Colon hinging a full clause (K1) | 2.1 % | 8.5 % | 0.1 % |
| Short phrase after the last comma (K2) | 7.7 % | 14.9 % | 2.2 % |
| Appositive gloss (K3) | 7.8 % | 6.4 % | 3.8 % |

**What follows.**

1. **Marc's colon finding holds, and it is concentrated.** Chapters 2 and 3 and the captions use colons at two to three times the field rate. Chapters 5–7 are at or below the field rate. The census measures this and does not explain it. Pages i–15 were the worst stretch to sample.
2. **The comma finding holds in shape, not count.** The prose has shorter sentences and fewer commas than the field. What is over-represented is the comma doing K2 (×3.5) and K3 (×2) work. A hunt for comma-heavy sentences would miss most of it and would flag the field's ordinary long sentences.
3. **Captions are the worst unit on every measure.** A quarter of caption sentences carry four or more commas, and nearly half a colon (44.7 %). Captions and headings are also where an examiner forms a first judgement.
4. **K4–K8 are invisible to the census.** They are found only by reading, which is why every caption and heading is read in full (§5).

**Caveats.**
- The heuristics are surface patterns: the K1 pattern needs a verb within four words of the colon; the K2 pattern is a preposition-led tail of at most seven words.
- The baseline text is extracted from PDF, so its sentence boundaries are noisier and its colon count is inflated by figure labels and pseudo-code. The ratios are therefore conservative.
- The numbers locate the work. They do not prove authorship, and no single sentence is judged by its count.

## 4. Seamless editing: the rules for every proposal

Marc's goal is minimal rework that improves the flow. The fix must not show.

1. **Rearrange before adding.** Build the sentence around its own words first. A new word enters only to restore a missing referent ([`voice.md`](voice.md) §0, the inverted U).
2. **Delta zero or negative.** The dissertation sits at its word-band ceiling. An item that adds words says why.
3. **No new terms, and no new commas.** Every *after* uses the body's registered terms. A fix that adds a comma, colon or semicolon has reproduced the defect.
4. **Split rather than connect.** A two-idea sentence becomes two sentences. Do not add *which*, *so that* or *while*.
5. **Keep every fact and citation.** The adversarial check on each proposal asks whether the *after* still says everything the *before* said that a reader needs. Is each cite still attached to the claim it supports?
6. **Never introduce a tell while removing one.** Check against [`voice.md`](voice.md) §h and [`critique_protocol.md`](critique_protocol.md) §f: no "not X but Y", no triads, no "serves as".
7. **Prior rulings are evidence, not authority.** Where an item reverses a ratified round, the ledger names the round.
8. **Floats change in their generator** under `tools/`, never in the PDF.

## 5. Procedure

**The thresholds** (`clause_census.py worklist`; ruled by Marc 2026-10-18). A unit is picked when any one holds:

| Flag | Threshold |
|---|---|
| K1 | any colon |
| K2 | at least 2 commas and a last segment of ≤ 7 words, or an "-ing" phrase after the last comma |
| K3 | the pattern ", a/an/the … ," |
| Comma job | 4 or more commas |
| K4 | a figurative-word cue from a fixed list |
| K7 | a term defined with `\emph` and reused at most twice |
| K8 | a "none" or "not stated" cue |
| K5 | every caption and heading, unconditionally |

**Ownership.** Each unit goes to exactly one cluster, in this order of precedence:
1. **F**, floats and headings;
2. **C**, any colon;
3. **A1/A2**, comma jobs, split at chapter 5;
4. **D**, word-level defects.

The owning agent fixes every defect in its sentence, so no sentence appears twice in the ruling file.

1. **Measure.** Run `python tools/clause_census.py rates` and record the numbers in the handoff.
2. **List.** Run `python tools/clause_census.py flags --chapter <name>` per chapter. This is the K1–K3 work list.
3. **Read in full, whatever the flags say:** every heading, every caption, and every first paragraph of a section. That is where K4–K8 live, and where the examiner reads first (Mullins & Kiley 2002).
4. **Classify.** Each flagged or read unit is a *keep*, with the warrant named (for example, "colon introduces an announced list"), or a *proposal*.
5. **Propose,** in the ledger form below. Where the move is not obvious, give 2–3 options with pros and cons and one recommendation.
6. **Check adversarially.** A second read of each proposal against §4's rules withdraws any that add a comma, a term or a fact gap.
7. **Marc rules.** Apply the ruled items, rebuild, re-run `rates`, and report the word delta.

**Order.**
1. Headings and captions, all chapters.
2. Chapters 2–3.
3. Chapter 4 and the appendices.
4. Chapters 1 and 5–7.

**The ledger form** (the claim-check review sheet's, adapted). One item per unit:
- the location: section, tex line and printed page;
- the class (K1–K8);
- the *before*, quoted;
- the *after*;
- Δ words;
- why, in one or two lines naming the rule;
- a **Mark:** ok / alt / keep / look line.

The calibration ledger in the handoff is the worked example.

## Sources

- Zobel J. *Writing for Computer Science*, 3rd ed., Springer 2014. doi:10.1007/978-1-4471-6639-9. The pages cited are 77, 83, 95–96, 101–102, 106–107, 115, 117, 120, 125–126, 174, 176–177, 192 and 196, all from a PDF copy; check them against the Springer edition.
- Gopen GD, Swan JA. "The science of scientific writing". *American Scientist* 78(6), 1990, pp. 550–558, section "The Stress Position".
- Trask RL. *Guide to Punctuation*, "The Colon". University of Sussex: sussex.ac.uk/informatics/punctuation/colonandsemi/colon
- *Chicago Manual of Style*, 18th ed., §6.65–6.71 (17th ed. §6.61–6.67). The paragraph titles were verified; the text was read only via a secondary copy.
- Reinhart A, et al. "Do LLMs write like humans? Variation in grammatical and rhetorical styles". *PNAS* 122(8):e2422455122, 2025. doi:10.1073/pnas.2422455122
- Herbold S, et al. "A large-scale comparison of human-written versus ChatGPT-generated essays". *Sci. Rep.* 13:18617, 2023. doi:10.1038/s41598-023-45644-9
- Desaire H, et al. "Distinguishing academic science writing from humans or ChatGPT with over 99% accuracy using off-the-shelf machine learning tools". *Cell Rep. Phys. Sci.* 4(6):101426, 2023. doi:10.1016/j.xcrp.2023.101426
- Kobak D, et al. "Delving into LLM-assisted writing in biomedical publications through excess vocabulary". *Sci. Adv.* 11(27), 2025. doi:10.1126/sciadv.adt3813
- Liang W, et al. "Monitoring AI-modified content at scale". ICML 2024. arXiv:2403.07183
- Sebo P, et al. "How ChatGPT writes scientific titles in medical research". *J. Med. Libr. Assoc.* 114(3):222–237, 2026. doi:10.5195/jmla.2026.2266
- Thelwall M. "Pot, kettle: nonliteral titles aren't (natural) science". arXiv:2006.07849, 2020.
- Rougier NP, Droettboom M, Bourne PE. "Ten simple rules for better figures". *PLoS Comput. Biol.* 10(9):e1003833, 2014, rule 4.
- Wilke CO. *Fundamentals of Data Visualization*, O'Reilly 2019, §22.1 and ch. 23.
- *Nature* formatting guide (figure legends): nature.com/nature/for-authors/formatting-guide
- APA. *Publication Manual*, 7th ed., Student Paper Checklist, §4.7–4.11.
- Mullins G, Kiley M. "'It's a PhD, not a Nobel Prize'". *Studies in Higher Education* 27(4), 2002 (via [`academic_register.md`](academic_register.md) §i).
- Wikipedia, "Signs of AI writing" (WikiProject AI Cleanup advice page, read 2026-10-18). A practitioner catalogue that calls itself "descriptive, not prescriptive". It is never cited in the dissertation.
