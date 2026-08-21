---
status: open                  # standing context for the ch2 workshop + drafting passes; retire when the chapter is drafted and scrutinised
created: 2026-08-21
---

# Standing context for workshopping the background chapter (ch2) — what the chapter is, and exactly what the submitted literature review can supply it

> **Mode note, first.** Marc drafts the prose; sessions scaffold and scrutinise
> ([`../workflows/draft_scrutiny.md`](../workflows/draft_scrutiny.md)). A session
> that returns finished background paragraphs has failed the mode. Every unit
> travels [`../workflows/drafting_pipeline.md`](../workflows/drafting_pipeline.md).

Companion to the two ch3 briefs of the same date —
[`2026-08-21_ch3_lit_review_design.md`](2026-08-21_ch3_lit_review_design.md) (the
literature review's structure) and
[`2026-08-21_lit_review_scrutiny.md`](2026-08-21_lit_review_scrutiny.md) (the
verdicts on the source material). This file carries the **ch2 half of the same
split**: the passages of the 22 May 2026 review that belong to the background
chapter rather than the literature review, located precisely, plus an honest account
of how much of ch2 the review does *not* supply.

## What the chapter is, in one line

**The inherited platform, described so a reader can follow the rest of the
document** — the simulator's lineage, its network model, its defence mechanisms and
its baseline attacker. Existing things, presented for comprehension. The arguments
*about* those components (the comparability boundary, the baseline's fairness, the
scoring of its threat model) are ch3's and ch4's; ch2 describes and hands over.

## Budget and skeleton

> **Superseded in part by Part 2 (below), 2026-08-21.** The chapter's scope opened
> after this section was written — moving-target-defence vocabulary was re-homed
> here from the literature review — and Part 2 proposes a revised skeleton at the
> same budget. The word budget, the unit count and the no-spare-section constraint
> below all still hold; the *section list* is the part under revision.

**1 250 words / 5 units** (writing guide ledger; ch2 was cut 6→5 on 2026-08-12 to
fund the methodology's 11-unit skeleton). The four sections in
[`../thesis/dissertation.tex`](../thesis/dissertation.tex) plus a short opener is
already the full five, so **there is no spare section**: any new heading has to name
what it displaces.

| Unit | Section | Job |
|---|---|---|
| opener | — (rides §2.1) | what the simulator is, in two or three sentences |
| 1 | Prior work | Brown → Zhang → Ho → Tay, what each added |
| 2 | Network model | topology, host/service structure, exposure |
| 3 | Defence mechanisms | the mechanism family, the execution schemes, the reactive learner |
| 4 | Attacker model | the scripted six-phase attacker and the inherited metric suite |

One standing discipline against ch2's failure mode, which is bloat: **nothing enters
this chapter that a later chapter does not lean on.** If ch4 and ch5 never refer back
to it, it is not background, it is a manual.

---

## The port map — what the review supplies, by ch2 section

Locators are section references into the submitted review plus line numbers in the
tracked markdown, [`../sources/lit_review/LIT_REVIEW.md`](../sources/lit_review/LIT_REVIEW.md).
**Nothing here ports one-to-one** — every passage was written to argue toward the
review's gap and has to be re-aimed at description. Word counts are of the source
passage, not of what should survive.

### §2.1 Prior work — **half supplied**

- **Brown / MTDSim / HARM** — §II-B ¶5, `LIT_REVIEW.md:61` (~90 w). Carries the
  discrete-event-simulator-on-three-layer-HARM description and the combined-MTD
  contribution. The paragraph's last sentence is a forward pointer into the review's
  §IV and does not travel.
- **Tay** — §II-C ¶3, `LIT_REVIEW.md:87` (~110 w) and §IV-B-2, `LIT_REVIEW.md:183`
  (~170 w). Between them: the DDQN orchestrator, what it replaced (Brown's
  fixed-interval scheduler), and that the attacker module is inherited unchanged.
- **Zhang 2023 and Ho 2024 are absent from the review entirely.** Neither is cited;
  neither has prose. This is the single biggest hole in the port — **half the
  lineage this chapter exists to narrate has no source text**. It comes from the
  extractions (`zhang2023`, `ho2024`) and the implementation records, not from here.

*Register warning:* the review introduces Brown and Tay in order to score them later.
Ch2 describes them as the platform. The evaluative clauses ("its principal
contribution is enabling…", "the contribution is defender-side") are fine; the
fidelity verdicts are not — those belong to ch3.

### §2.2 Network model — **essentially unsupplied**

The review contains one clause of relevance: "a discrete-event simulator built on a
three-layer Hierarchical Attack Representation Model (HARM)" (`LIT_REVIEW.md:61`),
plus "agnostic to specific network configurations" in §V-A (`LIT_REVIEW.md:225`).
There is no description anywhere of the topology, the host and service structure, or
the exposure model — the review never needed one.

**This unit is written from scratch**, against the implementation records
(`substrate_primer`, and the network/topology material in the pipeline records) and
against Brown 2023 directly. Budget accordingly: it is a full unit of new prose, not
a port.

### §2.3 Defence mechanisms — **partially supplied, and this is the best of it**

- **The vocabulary** — §II-A, `LIT_REVIEW.md:43` (attack surface), `:45`
  (what / how / when), `:47` (shuffling / diversity / redundancy), `:49`
  (proactive / reactive / hybrid). ~330 w of source.
  **Compress hard.** The ruling that governs this port: SDR and the what/when/how
  questions enter ch2 as *labels applied to the inherited mechanisms*, cited to Cho,
  not as a taxonomy discussed for its own sake — the field's conventions expect each
  mechanism to arrive with its class and its trigger semantics, and that expectation
  is the whole reason the vocabulary is here rather than in ch3. Perhaps eighty words
  survive. **Fig. 1 (the SDR relationship diagram) does not travel** — it illustrates
  a taxonomy discussion the dissertation is no longer having.
- **The mechanism set** — the only place the review enumerates MTDSim's actual
  operations is inside Tay's action list at `LIT_REVIEW.md:87`: IP shuffle, OS
  diversity, service diversity, complete topology shuffle, no-op. Useful as a
  checklist; it is not a description of the mechanisms.
- **The reactive learner** — §II-C ¶3, `LIT_REVIEW.md:87`. **The cleanest direct
  port in the whole review.** The DDQN, the five actions, and the observation that
  the no-op encodes restraint as a policy choice rather than a global interval
  parameter — all of it is ch2 material as written, needing register work rather
  than re-argument.
- **Execution schemes are absent.** That is Zhang's contribution and the review never
  covers it; it comes from the extraction and the implementation records.

### §2.4 Attacker model — **partially supplied**

- **The scripted attacker** — §IV-B-1, `LIT_REVIEW.md:181` (~150 w). Carries the two
  scenarios (general = network-wide compromise, targeted = specific-host), the
  finite-state machine "inspired by the Cyber Kill Chain and MITRE ATT&CK", and the
  RoA priority ordering over scanned exploits derived from CVSS.
  **Take the description; leave the verdict.** The passage ends by placing Brown at
  parametric fidelity and quoting the skill-homogeneity concession — both are ch3's
  cross-section, and repeating them here spends the argument twice.
- **The inherited metric suite is not supplied.** MTTC appears in the review only as
  a cell in Cho's field-level metric table (Table I, `LIT_REVIEW.md:68`), which is
  ch3 §3.3.2 material, not a description of what MTDSim computes. The internal
  definition and its divergences live in `metrics_semantics`.

---

## The coverage verdict, stated plainly

Roughly **450 words** of the review's 6 002 are ch2 material, expanding to a
1 250-word chapter. Three of the five units — the network model, half the lineage,
and the inherited metric suite — **have no source prose at all**.

The practical consequence for the workshop: do not open this chapter expecting a
quarry. The review supplies the *defence side* of ch2 reasonably well and almost
nothing else, because the defence side was the only part it needed. The rest is
written against the implementation records and the primary papers. (Those records
are named here as signposts from the docs index, not vouched for — this session was
run grey-box on Marc's instruction and did not read them.)

## Boundaries

- **Descriptive register throughout.** Ch2 states what the inherited components are
  and do. Where a component is later argued about, ch2 says what it is and stops.
- **Describe once.** Brown's attacker and Tay's agent are described *here* and
  referred back to from ch3's cross-section — not re-described there. This is the
  main double-writing risk in the port, because both currently live inside the
  review's scored entries.
- **No ATT&CK section.** ATT&CK is not needed to describe MTDSim, and ch2 has no
  spare unit; it is introduced in ch3 §3.1.2 where it does argumentative work. A
  framework earns a place in background only when the background cannot be written
  without it — SDR clears that bar, ATT&CK does not.
- **No lineage headlines.** Zhang's shuffle-dominant and Ho's diversity-dominant
  results are comparison points for the evaluation, per the skeleton comment in the
  tex, and do not appear in §2.1.
- **No gap talk.** The asymmetry line at `LIT_REVIEW.md:89` ("the adversary against
  which it is evaluated is inherited, not modelled") is the review's best sentence
  and it is *not* ch2's — it belongs to ch1 or the ch3 preamble, and only once.

## Open questions for the workshop

1. **Does §2.1 Prior work carry the lineage, or does §2.1 carry Brown and the other
   three ride their own sections?** Four papers in one 250-word unit is tight, and
   Zhang and Ho have no source prose to compress from.
2. **How much network model does the dissertation actually need?** The unit is
   written from scratch, so its scope is set by what ch4 and ch5 refer back to —
   worth deciding against the methodology skeleton before drafting, not after.
3. **Where does the inherited metric suite land — §2.4 or ch4's experimental
   setup?** The tex comment puts the description here and the comparability argument
   in ch4; confirm the split holds once the metrics' divergences are on the page.
4. **Does the opener need the pipeline figure**, or is that ch4's alone? The
   methodology brief has a live ladder figure at its chapter opening.

## Out of scope (explicitly)

Drafting ch2 prose; editing `dissertation.tex`; reading or reconciling the
implementation records named above; the ch3 briefs' open CONFIRMs.

---

# Part 2 — The widened scope, and a structure that carries it (2026-08-21)

Part 1 was written when ch2's only job was the inherited platform. It no longer is:
the moving-target-defence concept material — the review's §II-A, verdict
**relocate (ch2)** in
[`2026-08-21_lit_review_scrutiny.md`](2026-08-21_lit_review_scrutiny.md), and
CONFIRM 3 of [`2026-08-21_ch3_lit_review_design.md`](2026-08-21_ch3_lit_review_design.md)
— comes here. This part rules on whether that is right, sweeps the review for
anything else that is misfiled rather than merely weak, and proposes a skeleton.

## (a) Is the re-home the right call? Yes — and the reason is register, not topic

**The ruling that created this chapter is a register ruling.** V7's own words
(supervisor decision register): the simulator's description "is not methodology — it
describes existing things". The attack surface, the *what / how / when* questions,
the shuffle–diversity–redundancy family and the proactive / reactive / hybrid
trigger regimes are also existing things — definitional vocabulary, cited to Cho,
argued by nobody. V7's criterion admits them; no new ruling is needed to let them in.

The literature review cannot hold them, and the reason is its contract, not its
topic. Ch3 tells each category of prior work as a chronological story — a method,
its limitation, why the next method came — and narrows onto the demonstrated need.
Vocabulary has no such arc. Parked at the front of ch3 it is inert prose that
narrows nothing, and it spends ~250 of the survey's 3 000 words doing it.

**The placement test, stated once so it settles the next case too: ch2 carries the
terms and artefacts the rest of the document *uses*; ch3 carries the claims the
document *argues against*.** Descriptive and definitional here; evaluative and
narrowing there.

Two things the move buys beyond tidiness:

1. **It fixes a hole, not just a filing error.** Ch3 §3.2 is *attacker models in
   MTD* and §3.3 is *how MTD is evaluated*. Both presuppose a reader who knows what
   a shuffle is and where a trigger regime sits. Nothing in the current skeleton
   teaches that — the vocabulary was going to arrive by osmosis.
2. **It repairs the chapter order.** Background-before-literature-review read
   slightly oddly while ch2 was one artefact described before the field it belongs
   to. With the vocabulary here the sequence is a funnel: terms → survey → gap.

**The cost, plainly.** Ch2 becomes a two-register chapter and can drift into being a
second literature review. One tripwire holds it: **§2.1 surveys no works.** Every
claim in it is cited as a definition (Cho 2020; Hong 2018 where the metrics
partition is extended) and none is scored. The moment it starts naming papers and
their limitations it has become ch3, and the fix is to cut, not to balance.

## (b) The rest of the review, swept — what else is misfiled

The prompt's question was broader than MTD ("some other things that don't really
make sense to live in the lit review"). Swept against the scrutiny's section
verdicts, the answer is narrower than expected:

| Material | Ruling | Why |
|---|---|---|
| §II-A concept and taxonomy | **→ ch2 §2.1** | The one genuine migration. See (a). |
| §II-B, the MTDSim / HARM paragraph | **→ ch2 opener** | Already in Part 1's port map. |
| §II-C, the Tay DDQN paragraph | **→ ch2 defence mechanisms** | Already in Part 1's port map; the cleanest direct port in the review. |
| §II-B, the evaluation ladder + Table I | **stays ch3** (3.3.1 / 3.3.2) | Argumentative: it positions this work on the ladder and carries the metrics-are-scored-*over*-the-attacker hinge. Definitional-looking, evaluative in use. |
| §III-A ATT&CK, §III-B durability | **stays ch3** (3.1.2) | Ch3 needs them to license modelling at technique-and-tactic level. Ch2 names both frameworks only as attribution for the inherited attacker's design, with a forward pointer — a background chapter may name a framework it does not teach. |
| §II-C Masud (specified-pole orchestration) | **stays ch3** (3.2.4) | Evidence for the rhetoric-versus-execution pattern, not platform description. |
| The asymmetry sentence (`LIT_REVIEW.md:89`) | **ch1 or ch3 preamble, once** | Part 1's ruling stands. |
| §III-B the pyramid as a frame | **cut** | Scrutiny (a). Not a relocation. |
| **The inherited metric suite** | **→ ch4 §4.3.2** — *new ruling, answers open question 3* | Evidence, not preference: `dissertation.tex` already gives `subsec:metrics` "the inherited suite and its comparability boundary". Describing it in ch2 as well makes three metric touches in a 14 550-word document (ch3 field-level, ch2 inherited, ch4 inherited-plus-boundary). Description and its argument belong in one place. Ch2 keeps one forward-pointing clause. |

**So the only genuine ch3 → ch2 migration is the vocabulary.** Everything else the
review misplaces is a cut or a rework *inside* ch3. That is worth knowing before the
workshop: the widened scope is one unit of new material, not a general re-opening.

## (c) Why the current four headings stop working

They are MTDSim-shaped — a component-by-component walkthrough of one artefact — and
two things break under the wider scope:

1. **§2.3 would carry two registers in one heading.** The field's taxonomy *and*
   this simulator's operations, in 250 words. Part 1's ruling ("SDR enters as labels
   applied to the inherited mechanisms… perhaps eighty words survive") was correct
   for a platform-only chapter and is under-scoped for this one: eighty words cannot
   carry attack surface, *what / how / when*, SDR and the trigger regimes with
   citations.
2. **"Prior work" sits one page before a chapter called "Literature review".** A
   reader is entitled to ask why prior work is split across two chapters. The honest
   answer — ch2's four papers are not prior work in the survey sense, they are the
   *provenance of an artefact* — is exactly what the heading obscures.

## (d) The proposal — Marc's two-part shape, 5 units, ledger untouched

**Marc's shape (2026-08-21), adopted.** It supersedes the flat four-section version
first proposed in this brief, and it is better for a reason worth recording: the flat
version put §2.1 *Moving target defence* — a field — at the same heading level as
§2.2 *Network model*, one component of one simulator. Nesting the components fixes
the altitude mismatch. It is also **closer to V7 than the current tex is**: V7 names
exactly three components for this chapter (network model, defence model, procedural
attacker), and this shape gives them exactly three subsections.

| Heading | Job | Words |
|---|---|---|
| *(chapter opener, unnumbered)* | the frame, two sentences | ~60 |
| **§2.1 Moving target defence** | attack surface; *what / how / when*; SDR; proactive / reactive / hybrid. Cho 2020, Hong 2018. **Surveys nothing.** | 250 |
| **§2.2 MTDSim** *(preamble)* | what the simulator is — discrete-event, over a three-layer HARM — then the lineage in two sentences over **Table 2.1** | ~120 |
| §2.2.1 Network model | topology, host and service structure, exposure. Written from scratch | 250 |
| §2.2.2 Defence mechanisms | the roster wearing §2.1's labels; the execution schemes; the reactive selector | ~300 |
| §2.2.3 Attacker model | the scripted six-phase attacker, the two scenarios, the RoA-ordered exploit choice; metrics reduce to a forward clause | 250 |

≈1 230 words against a 1 250 budget; five heading-claims against five units. **No
ledger change, no float spent.** *(Heading form: `MTDSim` is a proper name, and the
tex already carries it in a ratified heading — `L4: The attacker-agent traversal in
MTDSim`. Alternative considered: `The simulator`, which loses the identification the
terminology registry asks for at first use.)*

**The shape pays for the dense unit.** Folding the chapter opener and the old
Prior-work section into one §2.2 preamble frees ~125 words, and §2.2.2 is where they
go — the unit carrying the roster, the labels, the execution schemes *and* the
learned selector. The overflow trigger named in the flat proposal is now unlikely to
fire, and the float stays unspent.

### (d.1) The lineage — narration cut, table kept

**Agreed on the narration.** Walking through the students' work is not relevant,
because everything relevant about it is described where it is used: Zhang's
execution schemes and Tay's selector in §2.2.2, Ho's metric suite in ch4. Attribution
rides as a clause — *the execution schemes Zhang added* — not as a section. That is
the "describe once" discipline in Part 1's Boundaries, applied.

**The table stays**, because it does three jobs no component sentence does, and it
costs nothing (floats sit outside the word budget):

1. **Ch4's comparability boundary** — cross-paper numeric comparison invalid,
   within-substrate comparison valid — presupposes a reader who knows these are four
   studies over one evolving codebase.
2. **Ch5's first experiment family re-runs the lineage's own published
   evaluations.** It introduces the headline results itself (V5 keeps
   shuffle-dominant / diversity-dominant out of ch2), but it should not also have to
   establish from scratch that the lineage exists.
3. **Research integrity.** A thesis extending three prior students' code needs one
   visible place where inherited and built are separated. Four rows do that better
   than four paragraphs, and an examiner looks for it.

Table 2.1 is therefore not a lineage section in disguise: *paper / what it added /
what this thesis inherits*, with the prose beside it carrying only the shape of the
evolution.

## (e) The other input — why Attack Flow does not come to ch2

The question is whether the attack-profiling material (the review's §III-D) and the
Attack Flow corpus should join the background, on the reasonable intuition that ch2
ought to describe *both* things this thesis joins rather than only the defence side.
**Recommendation: no** — on a distinction worth stating explicitly, because it will
recur:

> **Ch2 carries what is inherited. Ch3 earns what is chosen.**

MTDSim is inherited: no alternative was weighed, it arrived with the lineage.
Attack Flow was **chosen, and chosen by argument** — §III-D spends a full page
trading manual curation against automated extraction and concludes that automated
extraction "does not yet recover technique-level behaviour reliably enough to ground
an adversary on", which is why the analyst-curated corpus wins. The scrutiny record
calls that passage the review's internal exemplar. Three consequences:

1. **Pre-installing it in ch2 spends ch3's best argument early.** A reader who has
   already met Attack Flow as *the format this thesis uses* reads the page-long
   trade as retrospective justification for a settled decision. The review is meant
   to earn it.
2. **It cannot come alone.** Flow objects are keyed to ATT&CK techniques — the
   format cannot be described without the vocabulary. So Attack Flow into ch2 drags
   ATT&CK in, and ATT&CK's ch3 job (the durability argument licensing
   technique-and-tactic-level modelling — what justifies the pipeline's whole unit of
   analysis) is argumentative and cannot follow it. Definition in ch2, argument in
   ch3, is precisely the double-touch (b) has just finished cutting from the metrics.
3. **Nothing before ch4 needs it, and ch3 hands it over on the way.** Ch2's job is
   to make ch3 readable. The capture strand introduces the artefact as it argues for
   it, and the methodology uses it one chapter later.

**The asymmetry is real, and worth naming rather than repairing.** This thesis
inherits its defence side and builds its attacker side, so the defence side arrives
un-argued (background) while the attacker side is argued into existence (review →
methodology). Ch2 describing MTD but not CTI is that asymmetry showing through the
structure, not a gap in it. Expect the same test to keep returning a *yes* for
MTD-side material and a *no* for CTI-side material.

**The condition that reopens it.** If drafting §4.2.1 (L0→L1) turns out to need
~150 words explaining what a flow object *is* before the construction can be
described, the artefact needs an earlier definitional home — and the cheap fix then
is two definitional sentences in ch3 §3.1.3, where it is already being introduced,
not a new ch2 section.

## (f) Consequences to book if this is ratified

- **Three documents still describe ch2 as platform-only** and each needs one line
  changed: the writing guide's Background row, `docs/notes/ch2_background/README.md`,
  and the tex comment block above `\chapter{Background}`. The chapter's one-line job
  becomes *the vocabulary and the platform the rest of the document uses.*
- **The tex change is now a section restructure, not a heading swap** — four
  `\section` blocks become two, with three `\subsection`s under the second, and the
  `sec:lineage` label disappears (nothing currently `\ref`s it; verify before
  cutting). Still a separate, ratified pass; `dissertation.tex` is untouched by this
  brief.
- **Table 2.1 is a new float** and follows the figure/table conventions —
  `\caption[short]{long…}`, the short form a noun phrase for the List of Tables.
- **Nothing in the ch3 brief moves.** (e) leaves §3.1's three units intact; the
  vocabulary migration of (a) was already assumed by CONFIRM 3 of that brief.
- **Open question 4 (does the opener need the pipeline figure): recommend no.** The
  simulator's preamble now carries Table 2.1, and the pipeline belongs to the ladder
  figure at ch4's opening.
- **Open questions 1 and 3 are answered** — 1 by (d.1) (narration cut, table kept
  under §2.2), 3 by (b) (metrics to ch4, on the evidence of the existing ch4
  skeleton). **Open question 2 stands**: how much network model the document needs is
  set by what ch4 and ch5 refer back to, and this brief does not settle it.
