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
the lit-review scrutiny brief (retired 2026-08-30; `git show c03231b4:docs/handoffs/2026-08-21_lit_review_scrutiny.md`) (the
verdicts on the source material). This file carries the **ch2 half of the same
split**: the passages of the 22 May 2026 review that belong to the background
chapter rather than the literature review, located precisely, plus an honest account
of how much of ch2 the review does *not* supply. A third companion,
[`2026-08-21_ch2_lineage_description_precedents.md`](2026-08-21_ch2_lineage_description_precedents.md),
carries the craft side: how the four lineage papers themselves described the
simulator, scrutinised into per-unit precedents and anti-patterns for the
dictation sessions. This file stays authoritative on shape and budget.

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
the lit-review scrutiny brief (retired 2026-08-30; `git show c03231b4:docs/handoffs/2026-08-21_lit_review_scrutiny.md`), and
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
  *2026-08-27:* still no pipeline figure — but the preamble now carries a
  three-module model diagram (Figure 2.1) beside Table 2.1, ruled by Marc; see
  [`2026-08-27_ch2_model_diagram_plan.md`](2026-08-27_ch2_model_diagram_plan.md).
- **Open questions 1 and 3 are answered** — 1 by (d.1) (narration cut, table kept
  under §2.2), 3 by (b) (metrics to ch4, on the evidence of the existing ch4
  skeleton). **Open question 2 stands**: how much network model the document needs is
  set by what ch4 and ch5 refer back to, and this brief does not settle it.

---

# Part 3 — §2.1 assembled from the review's own sentences (2026-08-21)

Executes the §2.1 half of the workshop with Marc in-session: a grey-box requirements
pass, §II-A measured against it, and the unit assembled sentence-by-sentence from
the submitted review. **Mode note:** every sentence below is Marc's — ported from
the review with locators — or a marked adaptation of one, awaiting his ratification;
no new sentence was composed (the drafting pipeline's authorised-assembly exception,
invoked by Marc: "assemble the section 2.1 from the lit review context; if you are
missing sentences, I can fill you in"). **Result: no missing sentences** — the
review supplies the full critical list.

## (a) What §2.1 must do — derived grey-box, then corroborated

Derived from the section's function alone (250 words; the reader next meets §2.2.2's
roster, ch3's survey, ch4's schemes), then found to match `literature_conventions.md`
§c3–c4 independently: the field expects each mechanism to arrive wearing its SDR
class and its trigger semantics, in those exact terms.

**The job in one line: install the field's vocabulary so the document can speak it —
every MTD term used from §2.2.2 onward must be parseable from these 250 words.**

Five critical functions, each named with the later passage that leans on it:

1. **Name the object** — MTD defined via the *attack surface* (the term itself
   recurs in ch3 §3.3's metric vocabulary). One sentence plus the defining gloss.
2. **One sentence of premise** — perfect security abandoned; configurations move so
   attacker knowledge decays. Load-bearing beyond politeness: the dissertation's
   whole evaluation is the contest between attacker reconnaissance and defender
   movement, and "reconnaissance decays faster than it can be acted upon" is the
   mechanism the movement attacker is built to actually experience.
3. **The three-questions frame** (what / how / when) — the sort order §2.2.2 uses;
   *when* is the axis the execution schemes (ch4) and the timing results (ch5) live
   on.
4. **SDR, one functional definition each, phrased as attacker-effect** — shuffling →
   completed reconnaissance invalidated; diversity → exploits do not transfer;
   redundancy → service preserved. The attacker-effect phrasing is not decoration:
   this thesis evaluates from the attacker side, so these are the clauses ch4/ch5
   reuse (position versus surface). Redundancy is defined *so its absence can be
   stated* — §2.2.2's shuffle-and-diversity-only scope note, which ch6 leans on, is
   meaningless to a reader who never met the third primitive.
5. **Trigger regimes + the cost–security tension** — proactive / reactive / hybrid
   in the field's exact terms, and the tension sentence (move too often → overhead;
   too rarely → reconnaissance stays valid), which is why *when to move* is a
   research question at all and why MTTC moves with interval.

Useful but displaceable: the movable-attribute examples (chosen as the simulator's
own, they foreshadow §2.2.2 for free) and the SDR complementarity clause (licenses
the combined deployments Brown's contribution and ch5's comparisons speak of).

Not this section's job, each with a home: field history beyond one citation;
survey-register claims (modelling traditions, research directions) → ch3; metrics
and validation methods → ch3/ch4; any named paper, verdict, or gap sentence → ch3;
the SDR relationship figure (illustrates a taxonomy discussion not being had);
anything attacker-side (ATT&CK, APT, profiling) → ch3. At 250 words, every
non-critical inclusion displaces a critical one.

**Success tests:** (1) *forward-use* — every term defined is used later, every MTD
term used later is defined here; (2) *roster* — a reader with only §2.1 can classify
each of the five inherited actions by family and trigger; (3) *the tripwire* — zero
works surveyed, citations definitional only.

## (b) The §II-A verdict — Marc's rating holds, made precise

**§II-A is the review's one purely definitional section — it was written to install
vocabulary for the review's own later sections, which is ch2's job too — so it ports
at ~90 % reuse where the rest of §II ports at ~25 %.** Function by function: the
object (line 43) verbatim-portable; the frame and attributes (line 45) portable with
a trim; SDR (line 47) supplies exactly the attacker-effect phrasing the framework
demands, needing only the figure reference and one survey-register sentence cut; the
trigger regimes and the tension sentence (line 49) near-verbatim. The premise is the
one function §II-A lacks — it lives in §I ¶1 (line 20), whose first two sentences
are pyramid-free (the scrutiny's rework verdict on §I falls on the frame, entering
at ¶3, not on these).

The arithmetic is the striking part: ~205 words of §II-A plus ~55 of §I ¶1 → ~233
assembled against 250 budgeted. **The port is nearly word-neutral — the compression
that funds the premise import is exactly the two survey-register cuts** ("Hybrid
combinations … are an active research direction"; the Fig. 1 apparatus) plus the
example trims.

One caveat bounds the verdict: the section is content-ratified but sentence-suspect.
The review is class-C at sentence level on the authored-prose record, and §II-A
carries six em-dashes in ~190 words — denser than the document-wide 1-per-73 the
scrutiny flagged as the loudest machine tell. The port therefore keeps Marc's
sentences and converts the punctuation, each conversion marked (D2).

## (c) The assembly — ~233 / 250 words

Three paragraphs; citation keys are the parked bib entries. Sentence numbers key the
ledger below.

> (S1) Moving target defence (MTD) is the timely manipulation of system
> configurations to modify and control the \emph{attack surface}: the set of points
> at which an attacker engages with the system \citep{cho2020}. (S2) It inverts the
> conventional assumption that vulnerabilities can be eliminated and system
> configurations held stable: no system is perfectly secure, so attacks can be
> thwarted but not prevented \citep{ghosh2009nitrd}. (S3) By continuously changing
> the configurations an attacker relies on, MTD shifts uncertainty onto the
> adversary, whose reconnaissance decays faster than it can be acted upon
> \citep{cho2020}.
>
> (S4) The MTD design space is organised around three questions: \emph{what} to
> move, \emph{how} to move it, and \emph{when} to move \citep{cho2020}. (S5) The
> first concerns the configurable attributes available to the defender: IP
> addresses, network topologies, operating systems, software stacks. (S6) The
> second is captured by the canonical shuffle–diversity–redundancy (SDR) taxonomy,
> whose three primitives are complementary rather than partitioned \citep{cho2020}.
> (S7) \emph{Shuffling} rearranges or randomises existing components (IP mutation,
> topology reconfiguration), invalidating reconnaissance the attacker has already
> performed. (S8) \emph{Diversity} deploys different implementations of the same
> function, so that an exploit against one variant is unlikely to apply to others.
> (S9) \emph{Redundancy} replicates components to preserve service while the other
> two operate.
>
> (S10) The third question, when to move, distinguishes proactive (time-triggered),
> reactive (event-triggered), and hybrid scheduling regimes \citep{cho2020}.
> (S11) This is the tension between cost and security: moving too often imposes
> overhead on legitimate users; moving too rarely leaves the attacker's
> reconnaissance valid for longer than it should be.

### The port ledger

| # | Source (`LIT_REVIEW.md`) | Status |
|---|---|---|
| S1 | :43 | adapted — first-use expansion moved here, sentence-case ("Moving target defence"); em-dash → colon [D2]; \emph at first fix (review italicises it too) |
| S2 | :20 s1 | adapted — subject → "It" (the definition now leads); "it proceeds from the premise that" folded into the colon; "so that" → "so" [D5] |
| S3 | :20 s2 | **verbatim** |
| — | :20 s3 | cut — "complement … rather than a replacement" [D4] |
| S4 | :45 s1 | **verbatim** |
| S5 | :45 s2 | adapted — em-dash → colon [D2]; list trimmed 6→4, keeping only original items the document reuses (ports, virtual machines dropped); all four attested in Cho's own technique families per the extraction (IP mutation / topology shuffle / OS rotation / software-stack diversity) [D3] |
| S6 | :47 s1 | adapted — "(Fig. 1)" cut (the figure does not travel); expansion lower-cased, en-dashed |
| S7 | :47 s2 | adapted — em-dash pair → parenthesis (voice.md: the parenthesis is the authored device) [D2]; "port hopping" trimmed [D3] |
| S8 | :47 s3 | **verbatim** |
| S9 | :47 s4 | **verbatim** |
| — | :47 s5 | cut — "Hybrid combinations … active research direction": the tripwire cut (survey register); S6's complementarity clause keeps combined deployments licensed, and the cut removes a two-sense collision ("hybrid" as SDR combination three sentences before "hybrid" as trigger regime) |
| S10 | :49 s1 | adapted — em-dash pair → commas [D2] |
| S11 | :49 s2 | **verbatim** — the section's one licensed vivid sentence; its colon-semicolon opposition is the signature move |

### Decisions for Marc

- **D1 — the premise's home (S2–S3 here, or ch1's?).** Recommendation: **here**. Ch2
  carries definitions (placement test 1), and ch1 — synthesised last — can motivate
  without defining; if ch1's dictation later wants the inversion line, the cut comes
  from ch1. Watch the overlap when ch1 is drafted.
- **D2 — em-dash policy.** All six of the source's em-dashes are converted (colon
  ×2, parenthesis ×1, comma pair ×1, two removed with cuts), leaving zero. One
  ruling covers the lot; per-sentence reversal available.
- **D3 — example trimming** (S5 6→4; S7 3→2). Recommendation: as shown — examples
  double as §2.2.2 foreshadowing. Alternative: verbatim lists (+7 words).
- **D4 — the complement-not-replacement sentence** (:20 s3, ~15 w). Recommendation:
  **omit** — nothing later leans on it; the float stays unspent.
- **D5 — S2's light compression.** Binary: keep as assembled, or restore verbatim
  ("…held stable: it proceeds from the premise that no system is perfectly secure,
  so that attacks can be thwarted but not prevented").

## (d) Read-over findings

1. **Coherence.** Reads as one unit. The one seam is S3 → S4 (premise paragraph to
   design-space paragraph — a section boundary in the review). Acceptable in
   background register; if Marc wants a stitch it is his sentence to write, but the
   recommendation is none.
2. **Enumeration.** "Three questions" announced at S4 and walked to completion, with
   the third crossing a paragraph break — deliberate, since *when to move* is the
   axis the thesis leans on hardest and earns the tension sentence beside it.
3. **Voice diagnostics** (§(f) run as diagnostic, not gate): claim-first holds per
   paragraph; zero banned tells; zero em-dashes after D2; exactly one vivid sentence
   (S11); italics only at first-fix terms; AU spelling throughout.
4. **The tripwire holds.** Zero works named, zero verdicts; two definitional
   citation keys. Hong 2018 correctly absent (README line fixed this session).
5. **Forward-use test passes both directions.** attack surface → ch3 §3.3;
   what/how/when → §2.2.2 order, ch4 schemes; shuffling/diversity → §2.2.2 roster;
   redundancy → §2.2.2/ch6 absence note; proactive/reactive/hybrid → §2.2.2 schemes
   and selector, ch4. Nothing defined is orphaned; nothing later-used is missing.
6. **One integration flag.** "moving target defence (MTD)" is already expanded in
   ch1's RQ box; at document integration one expansion survives (likely ch1's).
   Until ch1 is dictated, §2.1 keeps its own.
7. **Count:** ~233 of 250; both ledger float units untouched.

## (e) State landed this session (2026-08-21, evening — updated after ratification)

- **D1–D5 all ratified by Marc as recommended, same session** ("all your 5
  decisions are fine, insert on fix"), and **the unit is inserted**: the assembly
  in (c) now sits verbatim in `dissertation.tex` under `sec:mtd-concept`, with a
  `% DRAFT STATE` comment recording the port, the ratification, and the two
  pending items (pass 6 once the §2.2 units exist; the ch1 MTD-expansion dedupe).
  The voice §(f) gate was run at insertion — the nine checks from (d) on this
  exact text, calibration inherently satisfied (the sentences are Marc's
  submitted, audited prose plus his ratified adaptations).
- `dissertation.tex` restructured to the ratified nested shape — labels
  `sec:mtd-concept`, `sec:mtdsim`, `subsec:network-model` /
  `subsec:defence-mechanisms` / `subsec:attacker-model`; `sec:lineage` gone (zero
  `\ref`s confirmed before cutting). Skeleton comments carry the unit budgets and
  the Part 2 rulings.
- `references.bib`: `ghosh2009nitrd` and `cho2020` REACTIVATED (uncommented,
  `@` restored) now that §2.1's `\cite`s land; `hong2018` stays parked. Build verified: full
  `pdflatex → bibtex → pdflatex ×2` cycle exits clean, zero errors, both keys
  resolve in the aux.
- Remaining for §2.1: nothing until section assembly — pass 6 runs over the whole
  §2 once the §2.2 preamble and three subsections exist; the ch1 expansion dedupe
  rides the integration check.

## (f) Pass 6 on §2.1 — run and applied (2026-08-27)

Run on §2.1 alone at Marc's request (the §2.2 units do not yet exist; the
cross-unit duplication sweep and the roster / forward-use test stay pending).
Scrutiny and voice pass returned together; Marc ruled the same session and every
accepted item is applied to `dissertation.tex`.

| Item | Ruling | Applied |
|---|---|---|
| M1 structure — P2 announced three questions and delivered two, P3 carried the third alone (the (c) assembly had merged the review's `:45` and `:47` paragraphs; read-over finding (d).2 called the crossing "deliberate" — Marc disagreed) | **(a)**: one paragraph per axis after the object paragraph — P2 = S4–S5, P3 = S6–S9, P4 = S10–S11; the review's own break restored | yes |
| M3 SDR attribution — Cho adopts the taxonomy from Hong & Kim 2016 | cite the origin on S6, Cho keeps the complementarity clause | yes — `hongkim2016` added to `references.bib` (Marc supplied the BibTeX; TDSC 13(2) 2016, DOI 10.1109/TDSC.2015.2443790) |
| Voice 1 — S11 naked *This* | attach the head noun: *When to move is the tension…* (Marc's stated intent: the when-to-move axis *is* the cost–security tradeoff) | yes |
| Voice 2 — S9 *the other two* → *the other two primitives* | **rejected**: *primitives* does nothing there — do not re-flag | no |
| Voice 3 — S10 glosses proactive and reactive, not hybrid | not ruled; left as is — restate at the integration check | no |
| Voice 4 — cut sweep | no cuts; ratified | — |
| Voice 5 — S3 *adversary* vs *attacker* | *attacker*; registry row RATIFIED (`terminology.md`) | yes |
| Voice 6 — S7–S9 shared skeleton | keep: definitional list of three by design — do not re-flag | — |
| M2 forward-use test | fine; runs once §2.2.2 exists (Zhang's execution schemes are all proactive, the DDQN selector reactive — S10's regimes are the right hooks) | pending |

§(f) gate after application: checks 1 and 2 (claim-first, enumeration) now pass
under the four-paragraph shape; the other seven were passing before. Section
count ~233 words, unchanged. **§2.1 is through pass 6**; the integration check
(ch1 MTD-expansion dedupe, voice item 3) is next, once ch1 and §2.2 exist.

## (g) Pass 6 on §2.2.1 — run and applied (2026-08-27)

Run on the unit alone; every fact treated as false until verified against
the code (`network.py`, `host.py`, `services.py`, `constants.py`) and the
write-surface record. Marc ruled the same session; accepted items applied.

| Item | Ruling | Applied |
|---|---|---|
| Fact: BA builds *subnets* per level, joined level-to-level, not "the topology" | more precision — levels are subnets built with BA graphs, joined | yes — wording from the dictated ruling, **ratify on read** |
| Fact: *scale-free* is not Brown's word | keep *scale-free*; Brown's "mimics the characteristics of a real-world network" worked in; cite the originals from Brown's list | yes — `barabasi1999`, `watts1998` added (Brown [16], [24]); Marc verifies references later |
| Fact: endpoints "never mutated" over-claims (CTS moves their adjacency) | more precision — the endpoint hosts persist as a unit through the run while everything around them moves | yes — "never rewritten … persist unchanged … while everything around them can move", **ratify on read** |
| Fact: complexity sets success *and* exploit time | timing dropped — the movement attacker supplies its own times; keep only complexity → success | yes |
| Fact: compromise rule incomplete (threshold is per service; host falls on a compromised service adjacent to its internal target node) | accept, with precision; internal target node may be described | yes — **FLAG**: Marc's closing recollection ("impact doesn't accumulate, it's a dependency chain, exploit the one next to the internal node") does not match the code: `Service.is_exploited` sums exploited-vulnerability impact and compares to `SERVICE_COMPROMISED_THRESHOLD` (7); the host falls when such a service neighbours the internal target (`host.py:424`). The prose states the code's rule. Dependency (`dependent_vuln_id`, 10 % of vulns) is the precondition gate cut under C3, not the compromise rule |
| `hongkim2012harm` pages | use Cho 2020's | yes — 1–8 (Cho [72]); Zhang [7] says 74–81; bib note flags VERIFY |
| 1 *a handful* → *a small number of* | accept | yes |
| 2 P1 fragments → full sentences from Marc's words | accept | yes |
| 3 *will take* → present | accept (then mooted by the timing cut) | — |
| 4 *reachability between them is the edges* | accept | yes |
| 5 OS out of the service-graph clause | accept | yes |
| 7 *topology of the graph* → *topology* | accept | yes |
| 9 CVSS: no expansion, no citation | ruled — bare "CVSS complexity" | yes |
| 12 depth *layer* → **level** | accept (Brown's word); registry RATIFIED | yes |
| 13 endpoints: *exposed endpoints* at first fix, *the endpoints* after | accept; registry RATIFIED | yes |
| 14 figure + caption errors: layer names (network/host/vuln vs ruled host/service/vuln); vulnerability layer drawn as an attack tree with OR/AND gates (no tree in code — C3) | **booked, not fixed here** — redraw `tools/mtdsim_model_figure.html` labels and the vulnerability panel, then rewrite the caption from the ratified prose, facts verified | no |
| 11 cuts | none in the ledger; **follow-up ruling (Marc, same day):** P4's closer *Visibility grows outwards from the foothold* cut as a given adding nothing | yes |
| Follow-up: P2 opener carried five clauses | split into three sentences (*hosts are placed in levels of depth. / Each level is a set of subnets … joined to the level before it. / The construction mimics …*) | yes |

Count after application: 291 words against 250 (was 264): the three precision rulings (levels-of-subnets, endpoints-persist, compromise rule) cost ~32 words net of the timing cut. Over budget by 46 — a cut ledger is owed, or the float is spent. The unit is
through pass 6 pending the two ratify-on-read sentences; the forward-use
test against Figure 2.1 waits on item 14; the integration check carries P2's
soft claim-first opener and the endpoint sentence's placement.

## (h) §2.2.3 — dictated, repaired, scrutinised and through pass 6 (2026-08-27)

Dictated the same day; inserted with two floats (Table 2.2 states, Table 2.3
objectives) so the prose carries rules and assumptions, not the procedure.
Pass 4 (M1 recovery order fixed to the record; M2 targeted objective kept live
by Marc's ruling — the record is his to fix, not a session's; M3 pivot sentence
dictated, give-up exemption cut) and pass 6 rulings, all applied:

| Item | Ruling |
|---|---|
| 1 naked *This* + *moving forward* + duplicate opener | merged into one sentence from Marc's two |
| 2 progressive chain → present simple; 3 doubled *using*; 4 *drawn out* → *draws it* | accepted |
| 5 / 8 rhetorical-question openers | cut; **possessions sentence cut outright** — Marc: the knowledge/possession distinction collapses, the pivot sentence carries it. Do not re-flag |
| 6 imperative *see Brown* → *Brown gives*; 7 *at any given time* cut; 9 *stay compromised* (Zhang's phrase); 10 *returns to*; 11 recovery sentence rebuilt | accepted |
| 13–15 cuts (attribution frame, closing restatement, original-threat-model sentence) | accepted |
| Terminology: *phases* → *states*; *FSM* acronym dropped; *attacker model recovers* → *the attacker recovers* | accepted; **objective** RATIFIED over *scenario* |
| Triad *pivot / sight / keys* | ruled keep (pass 4) — do not re-flag |

**Unruled, parked as `% [pass 6 PROPOSED]` comments in the tex:** #12 the
interrupt-scope sentence rebuilt on the verified fact; a bridge sentence so
the states may be called *attack phases*; `\citep{zhang2023}` on Table 2.3's
80 %. **Owed by Marc:** the one metrics forward clause to `subsec:metrics`
(skeleton must-carry). Gate after application: 1, 4, 7 now pass; 3 pending the
caption cite; 9 recalibrated. ~185 prose words against 250.
