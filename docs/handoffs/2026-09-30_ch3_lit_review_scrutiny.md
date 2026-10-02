---
status: open                  # 2026-09-30: APPLIED on Marc's rulings (see "Applied"); residue listed there
created: 2026-09-30
companions: ../workflows/literature_review_conventions.md (the yardstick, new today), ../workflows/chapter_scrutiny.md, ../workflows/voice.md §(0), ../workflows/terminology.md, ../notes/ch3_lit_review/README.md
---

# Chapter 3 scrutiny: correct the scoring, cut what chapter 1 already told, supply what chapters 4–6 lean on

**Goal.** Bring chapter 3 (Literature review) to the point where every claim
survives a check against its source, every sentence and float does something a
later chapter needs, and one term names one thing across chapters 1–6. Each entry
below is a proposal for Marc to rule on. Nothing is applied until he rules.

## Applied, 2026-09-30

Marc accepted the whole ledger ("I accept all the changes that you found so far")
and ruled the three open questions the same day. The redraft is in the tex; each
change carries a `% [CH3 SCRUTINY 2026-09-30, <ID>]` comment, and the prior text is
in git. Session-drafted joints (C2, N1, N2, the selection sentence) are to be
ratified on read.

**Totals.** Prose 2 848 → 2 550 words. Floats unchanged at 5; Table 3.1 is two rows
shorter and has one new row. Chapter 3 runs pp. 8–16 → 8–15. The build is clean at
101 pages, with 0 undefined references and 13 overfull boxes (unchanged).

**Marc's three rulings:**

- **R1 selection rule:** no search was run ("I read both their papers"). The
  sentence now reads "The two most recent MTD evaluations found in this review
  that ground their attacker in MITRE ATT&CK are scored here, Masud et al. and
  Kim et al." "Found in this review" scopes his superlative.
- **R4 learning cell: stays partial.** The rule is Zhang's, and the dissertation
  re-implemented it (vulnerability memory, §4.4.5), which ch2 already attributes.
  Consequence applied: the mark decode (now in the prose, T3) reads "the attacker
  model does something under the property", not "the executed attacker", so the
  cell and its definition agree.
- **G2 *disruption*, everywhere** ("disrupt, 100 %"). The registry row is
  re-affirmed. ch2's drift to *interrupt* is swept back (l.~621, 829–834), with
  ch4 §4.4.1 and §4.5 (including the blocked-actions equation) and ch5 §5.3.1.
  Figures 2.1 and 4.1 were regenerated; each diff is the one label. Code names keep
  *interrupt*.

**Where the application differs from the ledger:**

- **T3 mark.** The ledger proposed half circles. The tex trail shows Marc rejected
  half circles on 2026-09-07 ("it looks like MTDSim does everything") and chose
  the small dot himself (66456ce3). The dot is kept and only enlarged from 55 % to
  full size; it is now legible on p. 14.
- **X13, Table 3.2 row 4:** Alshamrani dropped (NIST and Cho carry adaptivity)
  rather than re-located to II-B, whose text is weak support.
- **T1 option B:** kept two efficiency rows (resource spent; service to users), not
  one, so the rotated *Efficiency* label fits. The label needed a `[-2.2ex]` nudge.
- **P7:** the SoK figure now reads "about 80 % precision at 66 % recall" (Büchel's
  insight 1), not "near $F_1 = 0.70$".
- **R10:** CVE-2021-41773 kept as "one known vulnerability (CVE-2021-41773)"; the
  address count, port and Apache version cut.
- **Two findings added from the final §3.2–3.3 verification report, both applied as
  corrections:**
  - X21: "which is built on assumptions, at a high level of abstraction, to allow
    reinforcement-learning agents to be trained" is in neither Tay nor Ho, so it is
    cut.
  - X22: Jalowski says "ill-defined", so the close reads "The attacker models of
    the MTD literature are ill-defined".
- **Consequential, out of chapter:** ch4 l.~5190 "15 tactics" now points to
  Figure 3.1 (F1).

**Not applied (need Marc's words or are out of chapter):**

- E4, the rational-attacker tension (property 6 vs §3.2.1): T3, his clause.
- §10's out-of-chapter flags:
  - Table 7.1's ticks on properties 6 and 7, and its caption, which still decodes
    marks with "the executed attacker";
  - ch4's four stages vs ch3's five;
  - ch4's third introduction of Attack Flow;
  - ch4 l.~4591's pointer;
  - the positioning objective with no profile;
  - the repo records on the /2's commit;
  - the NERVE epoch note;
  - copying NIST SP 800-39 into `docs/sources/`.
- **Figure 4.1 still says "rewrites"** where the registry now says *reconfigures*.
  The longer word overlaps both box borders at that gap, so the swap needs a layout
  change in `tools/ch4_overview_figure.py`. Reverted and left for a figure pass.
- **Verification notes not acted on** (minor, recorded for the next pass):
  - Hong's "dictated by the threat model" (behind §3.2.2's hinge sentence) is said
    of intrusion-response approaches; Hong §1 l.35 is the closer anchor.
  - Cho V-D's third dimension borrows "cost-effective" from bullet 2.
- **Not committed.** The checkout is parked on `feat/ch5-1000-seeds` with the
  parallel ch2 session's uncommitted work in the same files; awaiting Marc's branch
  choice.

**Round 2 (Marc's walk-through, 2026-10-01): one narrative, then each unit against it.**

His diagnosis: "the narrative is a bit disjointed … we can't just write each
chapter in isolation and append them." Three symptoms:

- §3.1 asked whether a "specification" could be "produced", not *recovered*.
- §3.2 opened on "three choices", which read as a parallel of what / how / when
  to move.
- §3.3 introduced "properties" of an APT attacker as if §3.1.1 had not already
  defined one.

Chapter 2 is the register model. The redraft is in the tex, tagged
`% [CH3 REDRAFT ROUND 2, 2026-10-01, <unit>]`, session-drafted and to be ratified
on read. Prose 2 550 → 2 438 words.

- **The thread.** The research question asks how MTD performs against APT
  attackers, but MTD is evaluated against attacker models. The chapter compares
  those models with an APT attacker:
  - §3.1 defines the APT attacker and how its behaviour is recovered;
  - §3.2 shows where the attacker model enters an MTD evaluation;
  - §3.3 breaks the APT attacker into eight properties, scores recent models and
    states the gap.
  
  The opener and the three preambles now say this, each by what its part does
  (connective_prose.md (b)).
- **§3.1.2.** The catalogue IDs are cut ("the brackets break the flow"). The
  hierarchy is in plain words with no *what* / *how* italics, which had collided
  with Ferraz's what / how in §3.1.3. The worked example keeps its IDs
  (literature_conventions.md (a)3). The version is v19.1, matching the pinned
  bundle, ch4 and Appendix B.
- **§3.1.3** rewritten as one line of argument:
  - what profiling recovers;
  - the obstacle, named once and attributed (Ferraz's procedural-semantics gap);
  - two routes, automated (scale, not yet reliable) and manual (Attack Flow);
  - the corpus, and the flow this dissertation drew;
  - what a flow lacks (tempo), and where the apparatus sits.
  
  Changes: "That manual path's exemplar" is gone; the STIX sentence is cut (its bib
  entry `oasis2021stix` was an unverified draft); ChronoCTI and AttacKG+ take one
  clause each; *attack profiling* is italicised once, and its product is tied to
  ch1's attack profile.
- **§3.2 preamble.** "Three choices" is cut; the preamble says where the attacker
  model enters.
- **§3.2.2.** A metric is defined. Cho's two purposes are glossed in his §VII
  terms (effectiveness = performance under MTD, VII-A l.574; efficiency = the cost
  MTD imposes, VII-B l.640). The two ASP sentences are merged.
- **Table 3.1 is now Cho's 2 × 2 itself** (effectiveness / efficiency ×
  attacker / defender). The "What it counts" grouping column is gone. Each cell
  keeps the metrics later chapters use, plus enough of the rest to show the frame.
- **§3.2 closer** is now the bridge into §3.3: evaluations vary the MTD
  mechanism, not the attacker.
- **§3.3.1** opens on §3.1.1's definition, broken into properties a model has or
  lacks.
- **§3.3.2 terms in ch2's words.** "host by host" replaces "per-host loop";
  "stolen credentials, exploits and brute force" replaces "attack vectors"; Kim's
  "one fixed step" replaces "one fixed action" (*attack action* is reserved).
- **§3.3.3** tightened: the return-on-attack sentence is cut, the means are one
  sentence each, and the close is one clause.
- **Figures 3.1 and 3.2** went to a background rebuild:
  - 3.1: legible tactic names, and the zoom path as the eye's landing point, for
    the two takeaways (15 tactics; one technique opened to its procedures);
  - 3.2: the T / F tabs removed, with a caption that says only how to read it.

**Round 3 (Marc, 2026-10-01): the opener.**

- **The "but" is gone.** "MTD performs against APT attackers, *but* MTD is
  evaluated against attacker models" read as a false dichotomy, as if an APT
  attacker could not be modelled.
- **The aim is now the gap**, located but not stated: "This chapter locates the
  gap between MTD attacker models and APT attackers." The literature supplies
  that gap and the chapter re-derives it.
- **The sections in Marc's flow:**
  - §3.1, the APT attacker and how its behaviour is recovered;
  - §3.2, how MTD is evaluated and where the attacker model enters;
  - §3.3, what the literature says MTD attacker models lack, whether recent
    evaluations still lack it, and the research gap.
- **Grounds:**
  - connective_prose.md (b), link → aim → how, one paragraph of 60–150 words;
  - yardstick checklist 1, where the gap is drawn and not the gap itself
    (EGZ p. 78);
  - detail in the section preambles.
- **The §3.3 preamble and §3.3.1's first sentence mirror it.** "MTD attacker
  models" is Marc's term, used verbatim at all three sites.

**Round 4 (Marc, 2026-10-01): the opener's words.**

- "locates the gap" → "identifies the research gap".
- "where the attacker model enters" → "how attacker models are used in the
  evaluation".
- "draws from the literature" → "surveys", Marc's literal verb.
- "still lack it" is kept.

The §3.2 preamble now gives one verb per step: assumed by the defence modelling
approach, measured by the metrics, run by the evaluation method. The §3.3 preamble
takes "identifies the research gap" and "sets out eight properties … that the
literature says MTD attacker models lack".

**Rounds 5–6 (Marc, 2026-10-01): the opener's last sentence.**

The sentence named the gap a second time ("checks whether recent MTD evaluations
still lack it, and states the research gap"). The aim sentence now carries the
gap and the hand-over ("identifies the research gap between MTD attacker models
and APT attackers that motivates Chapter 4"). The §3.3 sentence says what the
section does: "sets out eight properties of an APT attacker from the literature,
and scores the attacker models of recent MTD evaluations against them".

§3.3's own structure (criteria → scoring → gap) is unchanged. It is the
conventional scored-review order (yardstick §(c)4; Bonneau et al. 2012), so the
clunkiness was in how the opener described the section, not in the section.

**Round 7 (Marc, 2026-10-01): the crux, §3.3's framing and the gap's place.**

- **The eight properties are the deficit, not a second definition.** They are
  the subset of the APT attacker of §3.1.1 that the surveys say MTD attacker
  models lack. The opener, the §3.3 preamble, §3.3.1's first sentence and
  Table 3.2's caption now all say so.
- **"Compares", not "survey".** The sample is two works plus the lineage, chosen
  by reading, so "survey" would claim a coverage the sample does not have.
- **The research gap is now its own section, §3.4** (was §3.3.3). It is the
  chapter-level close, drawn from all three strands (yardstick §(c)3), and §3.3
  does one job: set out the deficit, then compare. The label `subsec:research-gap`
  is kept, so every `\ref` resolves (ch6 l.~8803 now reads "Section 3.4").
- **Opener:** "Section 3.3 sets out the eight properties of an APT attacker that
  the literature says MTD attacker models lack, and compares the attacker models
  of recent MTD evaluations against them (SQ2). Section 3.4 states the research
  gap that the three sections leave, which motivates Chapter 4."
- **Build:** clean (0 undefined references, 13 overfull boxes).
- **Not yet done:** §3.4's first paragraph still opens on Table 3.3 alone. As a
  chapter-level section it could name the §3.1 and §3.2 strands in one clause
  each. Left for Marc's walk.

**Round 8 (Marc, 2026-10-01): the opener's last two sentences.** "Them" was
unclear and the §3.4 clause too verbose. Now: "Section 3.3 sets out eight
properties of an APT attacker missing from MTD attacker models, and scores recent
MTD evaluations on those properties (SQ2). Section 3.4 states the research gap
that motivates Chapter 4." "Scores" is Table 3.3's own verb, and §3.3.1 carries
the surveys as the source. The §3.3 preamble mirrors the wording.

**Round 9 (Marc, 2026-10-01): the §3.1 preamble.** "An APT attacker can be
modelled only from what is recorded of its behaviour" jumped to modelling. The
section is about recovering the behaviour of real attackers, which is SQ1's own
wording, and "what it still cannot recover" was vague. Now: "This section surveys
how, and how far, the behaviour of real APT attackers can be recovered from CTI.
Section 3.1.1 defines the APT attacker by its objective, lifecycle and tempo.
Section 3.1.2 describes MITRE ATT&CK, the knowledge base that records which
techniques each attacker group has used, but not in what order. Section 3.1.3
describes attack profiling, which recovers that order from CTI, but not the
tempo of the attack." Each subsection takes up the question the one before it
leaves open: which techniques, then their order, then the tempo it misses.
"Tempo" is the 3.1.3 exit's word.
- **Term drift, open:** §3.1.1 says "tempo" (P1) and "pacing" (P3) for one
  thing, and the 3.1.3 exit says "tempo". One term is owed.
- **Build:** clean (0 undefined references, 13 overfull boxes).

**Round 10 (Marc, 2026-10-01): the §3.1 preamble, nuance cut.** Marc: the
nuance weighs in, so give the reader only what they need. The limits ("how far",
"not in what order", "not the tempo") are cut, because §3.1.3 states them where
it argues them. Now: "This section surveys how the behaviour of APT attackers is
recovered from CTI. Section 3.1.1 defines the APT attacker. Section 3.1.2
describes MITRE ATT&CK, the knowledge base that records attacker behaviour as
techniques. Section 3.1.3 describes attack profiling, which recovers the order of
an attack's techniques from CTI." About 50 words. The build is clean.

**Round 11 (Marc, 2026-10-01): §3.1.1 restructured, approved.** The subsection
now has two paragraphs: what an APT attacker is, then how its operation unfolds.
- **Paragraph 1:** one definition instead of three overlapping ones. Each property
  is said once, in Table 3.2's words (persistent, adapts, stealth, objective).
  NIST is named and expanded at its first use; it was expanded nowhere before, and
  §3.3.1 points to "the NIST definition (Section 3.1.1)". "Low and slow" is kept
  because ch4's low-and-slow family rests on it. The M-Trends figures sit beside
  the stealth claim.
- **Paragraph 2:** the lifecycle, with Volt Typhoon as the instance of the
  positioning objective.
- **Paragraph 3 is dissolved.** "The pacing depends on the objectives" is cut,
  which overturns the pass-4 KEEP.
- About 170 words, down from about 225. No new claims. The tempo/pacing drift is
  gone with the cut.
- **Build:** clean (0 undefined references, 13 overfull boxes).
- **Open, minor:** ATT&CK v19.1 has a tactic named *Stealth* (Figure 3.1), and
  property 5 is also *Stealth*. This overlap predates the round.

**Round 12 (Marc, 2026-10-01): one sentence in §3.1.1.**
- "The name gives its three properties" was not specific. It is now "Each word of
  the name stands for one property."
- **Raised, not acted on:** the five-stage lifecycle sits beside ATT&CK's 15
  tactics. A campaign may use a tactic more than once, or not at all. Marc read
  this as fine. §3.1.3's claim that ATT&CK records no order already keeps the two
  apart, so no sentence was added.
- "Lifecycle" is spelled one way across the thesis.

**Round 13 (Marc, 2026-10-01): §3.1.2 and Figure 3.1, all proposals accepted.**
- **Prose:** paragraph 2 now says that ATT&CK holds the four-level hierarchy, and
  that the matrix lays out its top two levels (the 15 tactics as columns, each
  tactic's techniques beneath it). This was the caption's reading instruction,
  now moved into the prose. It also fixes an inexact sentence: procedures have
  no matrix cell. Paragraph 1 loses "their software", which is unused later.
- **Caption:** "The MITRE ATT&CK Enterprise matrix (v19.1), with the Initial
  Access tactic opened down to a Volt Typhoon procedure."
- **Figure:** the level tags are the level names alone (*techniques*,
  *sub-techniques*, *procedures*). They are changed in
  `tools/attack_matrix_figure.py` and the figure is regenerated; the type floor
  holds at 7.48 pt.
- **Placement:** `[!b]` was tried, then reverted to `[t]` on Marc's ruling.
  Top of page is the thesis's float convention: every other pinned figure is
  `[t]`, and the figure stays on the page where it is first mentioned.
- **No definition added for sub-technique.** The hierarchy sentence and the
  worked example show that a technique breaks down into sub-techniques.
- **Build:** clean (0 undefined references, 13 overfull boxes, 101 pages).

**Round 14 (Marc, 2026-10-01): §3.1.3 and Figure 3.2.**
- **Figure 3.2 is redrawn natively.** The new generator,
  `tools/attack_flow_figure.py`, reads the flow's STIX bundle; nothing is typed.
  - All ten techniques are kept, in order. The labels print at 8 pt (they were
    about 5.4 pt), with no technique IDs and no bold.
  - Each condition is cut to its first clause.
  - The OR node is neutral. Colour has one meaning, the two conditions, and the
    drawing names it with the tags *start condition* and *end condition*.
  - The Builder export (`restyle_attackflow_svg.py` → `fig_3-1a_*`) is no longer
    included. Its files stay.
- **New caption:** "A flow of the Volt Typhoon campaign, drawn for this
  dissertation from the joint advisory AA24-038A: its techniques in order, from
  an unpatched public-facing appliance to pre-positioning for OT disruption."
- **Prose: APPLIED** on Marc's read ("we're stringing the ideas together in the
  right way"), after one clarity pass.
  - The section has four paragraphs, each with one job: what attack profiling is
    and why it is needed; automated vs manual; Attack Flow and Figure 3.2; what it
    does not recover.
  - Its fixed terms are attack profiling (automated / manual), attack profile,
    order, Attack Flow / flow / corpus, and timing.
  - The Büchel figures are re-scoped to technique identification.
  - The exit leads with its claim. The uncited "sits within the
    threat-intelligence and incident-response literature, outside MTD
    evaluation" is narrowed to "None of the work surveyed in this section
    evaluates MTD": the cited works show it, and §3.3.2 shows whether MTD
    evaluations use attack profiles. The thesis is now 100 pages.

**Round 15 (Marc, 2026-10-01): §3.1.3 read-through, applied.**
- "written in Attack Flow" → "with Attack Flow": profiling is not written.
- "An attack profile recovers" → "Attack profiling recovers": the process
  recovers the order; the product only holds it.
- The residual closer "None of the work surveyed in this section evaluates MTD."
  is cut. The section now closes on the timing limit.
- **Figure 3.2 caption:** "A flow of the Volt Typhoon campaign." The prose
  carries the provenance ("drawn for this dissertation from the Volt Typhoon
  advisory"), and the drawing's own tags carry the start and end.
- **Why timing matters** was first left implicit. Round 16 makes it explicit.
- **Build:** clean.

**Round 16 (Marc, 2026-10-01): the timing line and the Figure 3.2 placement.**
- **New closer for §3.1.3:** "Timing matters because MTD deploys its mechanisms
  once every deployment interval (Section 2.2.2), so when the attacker acts
  decides which deployments disrupt it." It uses ch2's own terms.
- **Figure 3.2:** `[htbp]` → `[t]`, following the top-of-page ruling of round 13.
  It now heads p. 10.
- **Build:** clean (100 pages).

**Round 17 (Marc, 2026-10-01): the timing close, refined.**
- **New close:** "When to move, MTD's third design question (Section 2.1),
  depends on the attacker's timing. Deploying often costs service availability,
  deploying rarely gives the attacker time, and a defender that cannot tell when
  the attacker acts is better served by a fixed deployment interval [cho2020]."
- **Source:** Marc's read is that unknown attacker behaviour drives MTD towards
  adaptive triggers that balance the cost of moving against the risk of not
  moving. Cho Sec. II-B (the interval balances cost and security) and Sec. III
  (uncertainty about the attacker's activity → a fixed interval) both state it.
- **Recompiled** with Marc's acknowledgements edit. Clean: 100 pages,
  0 undefined references.

**Round 18 (Marc, 2026-10-01): the close in one sentence.** "Yet when to move,
the third of MTD's design questions (Section 2.1), depends on the attacker's
timing: deploying too often costs service availability, and deploying too rarely
gives the attacker time [cho2020]." The fixed-interval prescription is cut: it
answers a defender-design question the chapter does not ask.

**Round 19 (Marc, 2026-10-01): the close split for clarity.** "MTD must therefore
decide when to move (Section 2.1) without the attacker's timing. Deploying too
often costs service availability, and deploying too rarely gives the attacker
time [cho2020]." It leads with what MTD has to grapple with, then gives the
stakes.

**Round 20 (Marc, 2026-10-01): the §3.2 preamble and the §3.2.1 heading.**
- **Preamble:** it was a laundry list, then too many clauses. Now: "The research
  question asks how MTD performs, which is what an MTD evaluation measures. This
  section surveys how MTD is evaluated and shows that the result depends on the
  attacker model. MTD modelling approaches assume an attacker model
  (Section 3.2.1), metrics depend on it (Section 3.2.2), and evaluation methods
  run MTD against one or a few (Section 3.2.3)." The thread is the claim the
  §3.3 preamble reports back.
- **Heading:** *Defence modelling approaches* → *MTD modelling approaches*. The
  §3.2.1 prose and terminology.md row 69 are renamed with it; the label is
  unchanged.
- **Build:** clean (100 pages).

**Round 21 (Marc, 2026-10-01): the §3.2 preamble again.** Round 20 was vague and
read like a riddle. Now: "An MTD evaluation runs MTD against an attacker model and
measures how MTD performs. This section takes its three parts from Cho et al.'s
survey of MTD, and the attacker model enters each. Section 3.2.1 covers the MTD
modelling approaches and the attacker each assumes; Section 3.2.2 the metrics,
whose values depend on how the attacker is implemented; and Section 3.2.3 the
evaluation methods, which run MTD against a single attack or a few."
- **Why these three parts:** they are Cho Secs VI–VIII. Cho's technique sections
  are in ch2 §2.1, and his attack-model section (Sec. V) is §3.3's source.
- **MTDShield** is dropped from the preamble: it is a body-level instance.
- **Build:** clean.

**Round 22 (Marc, 2026-10-01): the §3.2 preamble, after compaction.** Rounds 20–21
were still unclear: "not on the right level of abstraction".
- **Diagnosis:** each round put a subsection's *conclusion* about the attacker into
  one clause ("the attacker each assumes", "whose values depend on how the attacker
  is implemented", "a single attack or a few"). A reader can't parse those
  conclusions without the subsection's concepts, so rewording didn't help. The
  "why three" answer was also provenance (Cho), not the subject.
- **Now:** "An MTD evaluation runs MTD against an attacker model and measures how MTD
  performs. This section surveys the three parts of an MTD evaluation that use the
  attacker model. Section 3.2.1 covers the MTD modelling approaches, which decide
  how and when MTD moves; Section 3.2.2 the metrics, which measure how MTD performs;
  and Section 3.2.3 the evaluation methods, which run MTD against the attacker model.
  Section 3.3 then surveys the attacker models."
  - The preamble says what each part *is*; each subsection's last sentence delivers
    how that part uses the attacker model.
  - "Use the attacker model" is the chapter opener's phrase for §3.2.
  - "How and when MTD moves" ties back to §3.1.3's close.
- **Build:** clean, 101 pages.

**Round 23 (Marc, 2026-10-01): the §3.2 preamble, two clauses.** S1, S2 and the
metrics and evaluation-method clauses are approved ("definitely on the right track").
- **The modelling-approach clause:** "decide how and when MTD moves" is not how Marc
  would describe them. It now reads "which find an optimal deployment strategy".
  - This is Cho Sec. VI's purpose: the approaches are "modeling and solution
    techniques" used "to develop MTD", each finding an optimal defence strategy or
    deployment.
  - It is put in ch2's ratified term, *deployment strategy*. MTDShield is a
    deployment strategy learned by a machine-learning approach.
- **The last sentence:** "which attacker models?" It now uses the §3.3 preamble's own
  words: "compares MTD attacker models with the APT attacker".
- **Body hole found (Marc):** §3.2.1 never says what an MTD modelling approach is
  *for*. P1 names the three approaches and how each works, but not that each is used
  to find MTD's strategy. This is a core element and is owed when §3.2.1 is walked.
- **Build:** clean, 101 pages.

**Round 24 (Marc, 2026-10-01): §3.2.1 restructured.** Marc called it "a pretty poor
section":
- S1 led with Cho, not the subject.
- P2 walked the three approaches a second time and did not flow from P1.
- The MTDShield line was inserted bare.
- The closer condemned the field with no evidence.

The new structure has three paragraphs:
- **P1, what an approach is for:** an MTD modelling approach is a method for finding
  an optimal deployment strategy (ch2's definition); Cho's three are named; each
  assumes an attacker.
- **P2, each approach once:** how it finds the strategy, then the attacker it assumes.
- **P3, the so-what, on Cho's own evidence:** two studies of diversity-based MTD found
  different optimal strategies, and Cho traces the difference to whether the attacker
  needed a persistent foothold (Sec. VI-A). This is tied explicitly to §3.1.1, and
  the paragraph closes on MTDShield being learned against the baseline attacker.

Cut:
- the "no agency … logic limited" closer, which had no citation;
- "hindering the attacker's own learning", which is off the deployment-strategy
  thread.

**Downstream:** §3.4's gap paragraph (l.~3691) already uses the same Cho
persistent-foothold claim. It is now surveyed in §3.2.1 first, so the gap can point
back instead of restating it. Raise this when §3.4 is walked.

**Build:** clean, 101 pages.

**Round 25 (Marc, 2026-10-01): §3.2.1, second pass.** Marc's points on round 24:
- "Each approach assumes an attacker": what does it mean?
- "Not necessarily rational or intelligent": why not?
- In ML, the attacker "just happened to be there".
- P3 opened vaguely, and the two-studies sentence lost him.
- MTDShield was vestigial.
- The dissertation's own strategies come from no approach: is that disjoint?

Changes:
- **P1:** the strategy is found *against a model of the attacker*.
- **Game theory:** Cho's reason and consequence. Many attackers aim only to exhaust
  resources, and a strategy found against a rational attacker may not work against
  them.
- **ML:** its attacker is the attacker model the training environment simulates.
- **P3:** opens on the claim (the attacker model decides which strategy is optimal),
  then:
  - Carter's finding, via Cho VI-A, as the concrete case;
  - Cho's persistent-foothold tracing;
  - the APT consequence, as its own sentence.
- **New P4** places Table 2.4. Only MTDShield comes from an approach (ML, against the
  baseline attacker); random, alternative and single follow a schedule and assume no
  attacker.
- **2026-09-05 guardrail** ("this thesis uses none of these" never appears here): not
  overturned. P4 places MTDSim's inherited strategies, not this dissertation's
  method.

**Build:** clean.

**Round 26 (Marc, 2026-10-01): §3.2.1 P3 trimmed.** Marc: give the nuance the reader
needs, not the nuance the writer wants. P3 now gives one piece of evidence, the
concrete one: platform migration helps against persistent attacks but hurts against
fast ones. Cho's persistent-foothold tracing is cut here; it stays in §3.4. The
"some" and "local" hedges are dropped. **Build:** clean.

**Round 27 (Marc, 2026-10-01): §3.2.1 P1 and P3.**
- **P1:** "against a model of the attacker" implied one portable attacker model,
  whereas GA's attacker is a fitness function and game theory's is an agent. It now
  reads "Each represents the attacker differently".
- **P3:** Carter's platform-migration case was too specific and ran the argument
  backwards. Cho's direction-neutral finding is restored in plain words, as §3.4
  states it.
- **P4** is accepted.
- **Open for P2:** the ML sentence's cites (Tay, Ho) are instances carrying a general
  claim. GT alone gets a limitation sentence.

**Build:** clean.

**Round 28 (Marc, 2026-10-01): §3.2.1 P3, the exemplar.** Marc: "persistent foothold"
is never explained to the reader, and round 27 lost him. The platform-migration case
was the clearer exemplar, so it is restored. The last sentence turns its direction
into the dissertation's: "a deployment strategy found against fast attacks may pass
over the one that defends against it". With this, the §3.4 duplicate flag (round 24)
lapses: §3.2.1 no longer carries the persistent-foothold claim. **Build:** clean.

**Round 29 (Marc, 2026-10-01): §3.2.1 P3 close.** Round 26's close is restored: "so a
deployment strategy found against another attacker may not be optimal against it".
Its negative framing carries the conclusion even to a reader who missed the example.
Round 28's direction-turning clause is dropped. **Build:** clean.

**Round 30 (Marc, 2026-10-01): RULING on citation pinpoints, thesis-wide.**

> A citation carries a page or section only when the reader needs it to find what is
> cited: (1) a direct quotation, or (2) something taken from the source as it
> stands: an equation, table, figure, algorithm or specific value. A paraphrased
> claim, however specific, carries the plain citation. The label is IEEE's: "Sec.",
> "p.", "Eq.", "Table", "Fig.".

Marc's reason: a page or section breaks up the sentence. Keep it only where it is
needed, not as a nice-to-have.

Applied to ch3 the same day; 22 pinpoints changed:
- **Stripped:**
  - §3.2.1 P3;
  - §3.2.3's closer;
  - the paraphrase in §3.3 (Cho V-A/V-D, Alshamrani II-C);
  - Kim's kill-chain sentence;
  - both gap-paragraph cites;
  - Table 3.2's source column, with adjacent cites merged into one bracket.
- **Kept:** the quotations (Jalowski p. 8, Brown p. 7, Masud p. 7, Kim pp. 7 and 9)
  and Masud's Algorithm 2 (its "Sec. 4" dropped).
- **The close** "Ill-defined attacker models [p. 8]" is Jalowski's own phrase (source
  l.191), so it is now a quotation: "The ``ill-defined attacker models'' of MTD".

**Build:** clean, 101 pages. Table 3.2's Source column (5.3 cm) is now wider than its
cells need; that is for the table pass.

**Round 31 (Marc, 2026-10-01): §3.2.2 Metrics redrafted.**

Marc's reading:
- P1 is disjoint: a heavy definition, the classification crammed into one sentence
  ("the cost MTD imposes on each"), the game-theory exception, and an aside on
  Cho's survey counts.
- P2 U-turns from metrics to "MTD mechanisms cannot be benchmarked".
- P3 is one lone sentence.
- The prose never works through Table 3.1.
- The terms are inconsistent: "split" in the text, "frame" in the caption.

Root cause: the section began as one paragraph plus a catalogue table. The later
additions (benchmarking, the attacker dependence) were bolted on, not threaded
through.

Now:
- **P1:**
  - defines a metric in the preamble's words;
  - gives Cho's classification in the table's own row and column names, with no
    meta-noun;
  - walks the table cell by cell with the metrics later chapters use (ASP, MTTC,
    NCR);
  - ends on the lack of a standard metric set, as a fact about metrics (Cho VII,
    Jalowski).
- **P2, the attacker thread made concrete:**
  - every effectiveness metric counts what the attacker does, so its value depends
    on how the attacker is implemented (Hong);
  - the consequence for an APT attacker, parallel to §3.2.1.
- **Caption:** "as Cho et al. classify them".
- **Cut:** the game-theory payoff exception.

**Table 3.1** is kept as round 2 left it, Cho's 2×2. It is the reader's map, not a
catalogue. On this build it floats to the top of the next page, after §3.2.3 has
begun.

**Build:** clean, 101 pages.

**Round 32 (Marc, 2026-10-01): §3.2.1 P4 and §3.2.2 tightened.**
- **§3.2.1 P4** is background, not literature.
  - MTDShield is kept as the surveyed instance of the ML approach, folded into P2's
    ML sentence ("MTDShield's is the baseline attacker of Section 2.2.3").
  - The scheduled-strategies clause is dropped: ch2 §2.2.2 already calls them
    proactive schedules.
  - P3 is the closer again.
- **§3.2.2, one clause per sentence where possible:**
  - the metrics are named, not redefined (definitions are §4.5's);
  - the efficiency sentence went from five clauses to one ("measure the cost of an
    attack or of MTD");
  - the no-standard sentence is split in two.
- **§3.2.2 P2:** "every effectiveness metric" plus a three-item list read as
  incomplete, and it was false: time since last MTD is not counted from the attacker.
  Now: "ASP, MTTC and NCR are all computed from what the attacker does, so their
  values depend on how the attacker is implemented".

**Build:** clean, 101 pages.

**Round 33 (Marc, 2026-10-01): §3.2.3 rewritten; the §3.2 strand closer folded in.**

Marc's reading: "a poorly written section ... short for the sake of being short".
- S1 led with Cho.
- The analytical split was never used again.
- The trade-off sentence read as a riddle.
- The simulation-limitation sentence was unreadable.
- The closer's five-paper mechanism clause was off-thread.

Now, from Cho Sec. VIII (pros and cons per method) and V-D:
- **P1:**
  - "An MTD evaluation method is how MTD is run against the attacker" (the
    preamble's words);
  - Cho's four methods, each said in one phrase;
  - the trade-off at its two ends: analytical models cheapest but most abstract;
    emulations and testbeds most realistic but hard to scale.
- **P2:**
  - simulation is dominant, and MTDSim is a simulation (Marc's ask);
  - the limitation: results may not hold on a real system;
  - the strength: specific attack behaviours, as parameters, modelled more flexibly
    than in an analytical model;
  - "Yet most MTD evaluations run MTD against a single attack or a small set of
    attacks", as the bridge into §3.3.
- **The `\medskip` strand closer is gone:** its attacker half is P2's last sentence,
  and the mechanism half and its five cites are cut (each is cited elsewhere).
- **Term:** "evaluation method" is Cho's own (Sec. VIII title, "evaluation methods
  for MTD").

**Build:** clean, 101 pages.

**Round 34 (Marc, 2026-10-01): §3.2.3 again.**
- **S1:** "the attacker" was vague. It now uses the preamble's phrase: "An MTD
  evaluation method runs MTD against an attacker model".
- **S2:** "Cho et al. name four" was too choppy. The four are now named in the same
  sentence.
- **P2** went in four directions and ended on a single-attack fact that read as a
  complaint. It now has one line of argument:
  - why simulation dominates (it models specific attack behaviours more flexibly);
  - its cost in plain words (a result may not be reproduced on a real network);
  - "MTDSim is a simulation, so an APT attacker model can be built in it".
- **Cut:** the "every variable" clause (that is what a model is) and the single-attack
  sentence (it belongs to §3.3, Cho V-D strategic plurality).

**Build:** clean.

**Round 35 (Marc, 2026-10-01): §3.2.3 P2, S2 and S3.**
- **S2:** "Its cost is that" was a dangling pointer. It now reads "Results found in
  simulation may not be reproduced on a real network".
- **S3:** "so an APT attacker model can be built in it" implied that no other method
  could build one. It now reads "so this dissertation's evaluation has the same
  flexibility and the same limitation".

**Build:** clean.

**Round 36 (Marc, 2026-10-01): §3.2.3 P2 close.**
- **S2** invited "why not?". It now gives Cho's reason in the sentence: "Real networks
  have uncertainty that no simulation fully captures, so results found in simulation
  may not be reproduced on them".
- **S3** tried to restate S1–S2. The reader needs only where this dissertation sits:
  "This dissertation evaluates MTD in MTDSim, a simulation (Section 2.2)."

**Build:** clean.

**Round 37 (Marc, 2026-10-01): §3.2.3 close, the strength the dissertation uses.** The
last sentence now adds "…and uses that flexibility to run an APT attacker model
through MTDSim's existing attack actions (Chapter 4)". This is the strength side of
the simulation trade-off. The limitation side is ch6's.

**Round 38 (Marc, 2026-10-01): §3.2.3 P2 filtered.** P2 now has three ideas, one
sentence each:
1. the strength (kept);
2. "Simulation results do not transfer directly to a real network, which no
   simulation fully captures";
3. "This dissertation uses MTDSim's flexibility to run an APT attacker model through
   its existing attack actions (Chapter 4)".

"MTDSim is a simulation" is dropped, as ch2 already says MTDSim simulates. **Build:**
clean.

**Round 39 (Marc, 2026-10-01): whole-§3.2 repetition read; preamble glosses cut.**
Read as one piece, each part's definition appeared three times within 1.5 pages:
- preamble S1 ("runs MTD against an attacker model and measures how MTD performs");
- the preamble's section list ("the metrics, which measure how MTD performs"…);
- the subsection's opening sentence.

All three list glosses are cut, including the modelling-approaches one (Marc: it
repeats §3.2.1's opening sentence too). Each part is now defined once, where its
subsection opens. This overturns round 23's glossed list on merit. Checked and kept:
- the §3.2.1 and §3.2.2 endings (same shape, different reasons);
- MTDShield's training attacker in §3.2.1 (new: ch2 does not say it);
- the §3.3 opener's one-clause summary of §3.2.

**Flagged for the §3.4 pass:** §3.4's first paragraph restates §3.2.1's
conclusion from the adjacent Cho sentence ("which MTD strategy is optimal depends
on whether the attacker's goal requires a persistent foothold"), using the term
dropped in round 28 because the reader is never told what it means. Proposed: a
pointer back to §3.2.1 in §3.2.1's own words. **Build:** clean, 0 undefined
references.

**Round 40 (Marc, 2026-10-01): §3.3 preamble read as a CS student.** The preamble
had two faults:
- **It led with a recap.** "Section 3.1 defined… Section 3.2 showed…" defined the
  section by what came before it, so it never introduced itself.
- **Its list sentence carried fluff:** "MTDSim's baseline attacker among them" and
  "missing from MTD attacker models".

The new text leads with the section's reason in its own terms, then gives the
section's job, then one plain sentence per subsection: "An MTD evaluation shows how
MTD performs against an APT attacker only if its attacker model behaves like one.
This section compares MTD attacker models with the APT attacker. Section 3.3.1 sets
out eight properties of an APT attacker. Section 3.3.2 scores the attacker models of
three recent MTD evaluations on these properties."

- The baseline attacker is still named in the chapter intro and in §3.3.2's opener.
- "Lack" is still stated by §3.3.1's opener.
- This overturns round 2's recap opener on merit, and the round 39 "kept" note on the
  §3.3 opener's summary of §3.2.

**Build:** clean, 0 undefined references.

**Round 41 (Marc, 2026-10-02): §3.3 relabelled as a comparative evaluation.**

Marc read §3.3 as the examiner. His lit review lost marks here, because the section
"wasn't structured in a defensible way". An examiner would ask four questions:

1. Why "attacker models in MTD", when the term is *MTD attacker model*?
2. Why define the APT attacker again, when §3.1 already did?
3. Why these three works, and why trust the scores?
4. Does the gap persist?

The section already runs in the conventional order for a scored review: criteria,
selection, marks, table, a reason for each cell, then the finding (yardstick §(c)4
and §(e); Bonneau et al. 2012). What failed was the labels and three missing
sentences.

- **Headings (RULED: "beautiful", "that's strong"):** "MTD attacker models",
  "Properties MTD attacker models lack" and "Recent MTD attacker models". The labels
  are unchanged.
- **Preamble:** "Two surveys of MTD find that MTD attacker models lack properties of
  an APT attacker [cho2020, jalowski2026]. This section checks whether recent MTD
  attacker models still lack them. Section 3.3.1 sets out eight such properties, and
  Section 3.3.2 scores three recent MTD attacker models on them." Marc asked whether
  *tests* was proper form; it is now *checks*, because three works are not an
  experiment.
- **§3.3.1 opener:** cut to the pointer at the table, since the preamble now states
  the surveys' finding once.
- **§3.3.2 opener:** the selection rule and the scorer, given in the table's row
  order:
  - the lineage, as the work this dissertation extends;
  - Masud and Kim, as the two most recent MTD evaluations found in this review that
    ground their attacker in MITRE ATT&CK;
  - **"An attacker model grounded in ATT&CK is the most likely to have the
    properties"**, which is session-drafted and is Marc's to own;
  - "The scores are this dissertation's reading of each paper."
- **§3.3.2 close:** the finding moved here from §3.4, so that §3.3 answers its own
  question: "The three recent MTD attacker models still lack the eight properties.
  None has any of them as Table 3.2 defines it, and only the MTDSim lineage has
  persistence, objective conditioning and adaptivity, each in part."
- **§3.4 P1:** now opens "An attacker model without persistence, objective
  conditioning and adaptivity…", with the three named outright.
- **Chapter intro:** "scores three recent MTD attacker models on them".

**Overturned on merit:**

- the round 40 lead sentence (a riddle);
- the 2026-09-26 P3 ruling that kept the cited survey claim out of the preamble (the
  claim is the section's reason, and it is still stated once);
- the 2026-09-30 S2 heading suggestion;
- the 2026-09-08 ruling that the verdict on the table is drawn in the gap section.

Marc now reviews §3.3.1 onwards unit by unit.

**Build:** clean, 0 undefined references, 0 errors. The TOC shows the three new
headings.

**Round 42 (Marc, 2026-10-02): §3.3.1 rebuilt for the CS student.** Marc read
§3.3.1 as a CS student and was lost at S1:

- it led with the table;
- "the two surveys" were not named;
- "the APT definition of Section 3.1.1" was not explained.

P1 re-defined the APT attacker. Cho's four characteristics restate §3.1.1, which
already gives persistence, adaptivity, stealth and the objective-conditioned
stages. "More or less" was a hedge, and the NIST/Alshamrani "overlap" sentence was
a machine-stitched join. P2 did not flow. Table 3.2 was tacked on: its caption
"are said to lack" was not declarative, "What it names" was vague, the Source
column took most of the row, and the cells were not specific to attacker models.

The diagnosis: the unit had no stated purpose. The reader is never told where the
eight come from or why four papers stand behind them.

- **P1, where the eight come from.** The §3.1.1 definition gives 1, 2, 4 and 5
  [nist, alshamrani]. The two surveys, now named (Cho, Jalowski), name what MTD
  attacker models lack and add 3, 6, 7 and 8. Then come the table's job and the
  synthesis flag.
- **P2, the surveys' evidence.** Cho's three limitations come first, then
  Jalowski's "most glaring flaw" with the Nmap and passive-reconnaissance contrast,
  then his call for scheme awareness. Each limitation ends with its property name
  in Table 3.2's words, so the table is woven into the prose. The 2026-09-07
  "(property n)" tags stay retired.
- **Cut:**
  - the walk through Cho's four characteristics (Cho stays cited in the table);
  - the NIST overlap sentence;
  - "more or less";
  - "not a scripted intruder oblivious to the defence" (not-X-but-Y).
- **Table 3.2:**
  - the caption is now "…that MTD attacker models lack, and their sources";
  - the column header is now "What an attacker model with it does";
  - each cell is a verb phrase with its meaning unchanged, so Table 3.3's scores
    stand;
  - "plural attack options" became "several attack strategies";
  - "cost/benefit signal" became "weighs the cost of an action against its
    benefit";
  - widths changed from 3.2/5.9/5.3 to 4.0/8.2/2.2 cm.
- **Table 3.3 caption:** "Recent MTD attacker models, scored…" (round 41's term,
  missed then).

The claims were re-read against `extractions/cho2020.md` (V-D) and
`jalowski2026.md` (§4.3).

**Build:** clean, 0 undefined references, 12 overfull boxes. Table 3.3 still
overruns the text width, a §3.3.2 item.

**Round 43 (Marc, 2026-10-02): §3.3.1, specific language.** Marc said P1 was "100 %
on the right track" but vague in three places:

- "what definition?";
- "the choice of eight" did not say why the eight are the dissertation's own;
- "defines each property by what an attacker model does" was not specific.

He also asked for:

- the surveys' years, because recency is the point;
- prose and Table 3.2 to agree;
- table cells that are "still so long and vague";
- guidance on the convention for bracketed property names.

Changes:

- **P1 leads with the claim, in Marc's own order:** "MTD attacker models lack eight
  properties of an APT attacker, drawn from the APT definition and from two surveys
  of MTD."
  - It spells out what §3.1.1 says for each of the four properties the definition
    gives.
  - It names the surveys with their years ("Cho et al.'s 2020 survey of MTD",
    "Jalowski et al.'s 2026 gap analysis of MTD"). These are descriptors; the
    timeline rhetoric cut on 2026-09-08 stays cut.
  - The synthesis now carries its reason: "No single source lists all eight."
  - The table's job is now "the behaviour Section 3.3.2 looks for in an attacker
    model".
- **The bracket convention, as ruled here:**
  - A term in brackets after its gloss *introduces* the term, which is the coinage
    convention. P1 uses it for the four properties from the definition.
  - Once a term is introduced, it is used as a word in the sentence, point first
    ("First, they lack adaptivity and learning: …").
  - Numbers are kept for compact keys only: Table 3.3's columns and §3.3.2's
    cell-by-cell walk.
- **P2.** Cho's third limitation now carries scheme awareness (V-D bullet 3,
  "leverage how MTD works", source l.462). Jalowski: "the same lack of learning and
  scheme awareness, and add stealth".
- **Table 3.2:**
  - The header is now "Definition".
  - The cells are cut to the behaviour that is scored.
  - Row 4 drops "changing conditions"; no cell in Table 3.3 rests on it.
  - Row 8 is now "models how and when the MTD scheme moves", the wording of
    §3.3.2's lineage cell (8).
  - Cho is cut from rows 1 and 5 (Marc: prose and table consistent). Every
    remaining citation has its sentence in the prose.
  - The scores are unchanged.

**Build:** clean, 0 undefined references.

**Round 44 (Marc, 2026-10-02): §3.3.1 P1 provenance, Table 3.2 specific.**

Marc's points on P1:

- Listing four properties "from the APT definition" under a claim about MTD attacker
  models misrepresents what backs them, because the definition is not MTD
  literature.
- §3.1.1 already gives the definition, so point back to it.
- Drop the formalities: the years, "survey of" and "gap analysis".
- Put the subject first: "This dissertation synthesises these eight properties".
- The table sentence read like a preamble.
- He asked whether bracket glosses are conventional.

Changes:

- **P1, now four sentences:**
  1. The synthesis, and the table that defines it.
  2. Cho's four characteristics of a sophisticated attacker (MTD literature). Cho
     returns to rows 1 and 5.
  3. A pointer to §3.1.1 by name only: it "also gives the first three, and adds
     objective conditioning".
  4. The three the surveys add as lacking.
- **Definitions live only in Table 3.2** (one term, defined once). The prose names
  and sources each property, and the bracket glosses are gone. This overturns
  round 43's P1.
- **P2:** Jalowski's "mutation patterns" became "deployment patterns", ch2's term
  (yardstick checklist 6: translate each work's terms).
- **Table 3.2 cells** now use ch2's terms (deployment, mechanism, disruption, attack
  action, foothold, campaign) and §3.1.1's objectives. The scores are unchanged:
  - **4:** "chooses its next attack action in response to an MTD disruption".
    *Chooses* keeps the lineage partial, because its re-scan is forced, not chosen.
  - **5:** "such as by passive reconnaissance instead of active scanning".
  - **7 and 8 are kept apart:** learning is from observed deployments; scheme
    awareness is a model of the scheme's logic.

**Open for Marc.** The surveys' evidence in P2 covers properties 3 to 8. That MTD
attacker models lack 1 (persistence) and 2 (objective conditioning) rests only on
the §3.3.2 scores. An examiner may ask who says so.

**Build:** clean, 0 undefined references.


**Round 45 (Marc, 2026-10-02): §3.3.1 P1 restored from round 43.** Marc: round 44
lost the narrative and the nuance; round 43 was the exemplar and needed only
targeted edits.

Root cause (the session's):

- Round 44 rewrote P1 wholesale instead of editing the sentences Marc flagged.
- It answered Marc's questions (a pointer or here? are brackets conventional? drop
  the years?) with cuts.
- It promoted his synthesis sentence to the lead, so the claim ("MTD attacker models
  lack eight properties") was lost.
- It re-added Cho V-A's four-characteristic walk, which round 42 had cut on Marc's
  word, partly to anchor Cho's citations on rows 1 and 5. A bookkeeping rule drove
  the prose.
- It named "objective conditioning", "adaptivity" and "stealth" as bare terms.
  §3.1.1 describes these but never names them, so the reader met unintroduced terms.
- It changed P1, the convention and five table cells in one round.

Changes (round 43 as the base):

- **S1 is the claim, alone.** The APT definition no longer shares a sentence with
  "lack", so it does not read as evidence for the lack (Marc's misrepresentation
  point). The evidence for the lack is P2 and §3.3.2.
- **S2 points to §3.1.1** and coins its four terms in §3.1.1's own words. The bracket
  is the coinage convention, kept because §3.1.1 never names them. The objective
  conditioning gloss now matches Table 3.2 row 2.
- **S3: "The two surveys add the other four"** ("the two surveys" are the
  preamble's). The years, "survey of" and "gap analysis" are cut.
- **S4: "This dissertation synthesises the eight in Table 3.2, because no single
  source lists them all."** It is subject first, in Marc's words, and the separate
  table sentence is folded in.
- **Table 3.2:** Cho is cut from rows 1 and 5 again. Round 44's cells are kept.
- This overturns round 44's P1.

**Open for Marc.** The prose glosses persistence and adaptivity in §3.1.1's words
(NIST's general sense). Table 3.2 rows 1 and 4 give the same properties in MTD
terms ("runs a multi-stage campaign", "chooses its next attack action in response to
an MTD disruption"). This is the source's meaning, then what is scored. Say if you
want the two worded identically.

**Build:** clean, 0 undefined references, 0 errors.

**Round 46 (Marc, 2026-10-02): §3.3.1 small rulings; the unit's logic reviewed.**

Applied:

- **P1 close:** "This dissertation synthesises the eight properties in Table 3.2."
  The reason clause is cut, because the four-plus-four split already shows it.
- **Table 3.2 row 5:** "avoids detection, for example by passive reconnaissance".
  "Instead of active scanning" restated "passive" for a CS reader.

Proposed, not applied (Marc rules):

- **L1, the unit's logic: it asserts its conclusion as its premise.**
  - The heading and S1 say MTD attacker models lack all eight properties. The
    surveys' evidence (P2) covers only six. The APT definition says what an APT
    attacker is, not what MTD attacker models lack. So nothing in the unit stands
    behind the lack of persistence or objective conditioning.
  - In the comparative-evaluation shape (Bonneau): the criteria section derives
    the criteria, and the lack is the evaluation's finding.
  - Fix:
    - S1 becomes the criterion: "An MTD attacker model needs eight properties to
      model an APT attacker." The definition and the surveys then stand behind it
      honestly.
    - P2 stays the surveys' evidence for six.
    - A P2 close says neither survey names persistence or objective conditioning
      as lacking, so §3.3.2 scores all eight.
    - The heading becomes "Properties an MTD attacker model needs". "APT attacker
      model" is avoided, because it is the name of this dissertation's model (ch4
      onward). This overturns round 41's heading ruling.
    - The preamble's "eight such properties" follows the new heading.
- **P2-a:** Jalowski's sentence promises stealth after its colon but delivers
  stealth, learning and scheme awareness. Split it: one sentence of evidence for
  learning and scheme awareness, one for stealth.
- **P2-b:** "the logic behind its movement" becomes "the logic of the MTD scheme",
  Table 3.2 row 8's words. "Movement" is not a ch2 term.

**Build:** clean, 0 undefined references, 0 errors.

**Round 47 (Marc, 2026-10-02): round 46's L1 and P2-a/b applied.** Marc: "well
thought through and well integrated … push that"; on P2: "write that in, I'll read
paragraph two and accept it or not".

- **L1, the criterion before the finding:**
  - The §3.3.1 heading is now "Properties an MTD attacker model needs". This
    overturns round 41's heading.
  - S1 is now "An MTD attacker model needs eight properties to model an APT
    attacker."
  - The Table 3.2 caption, the §3.3 preamble and the chapter intro now say the same.
  - The lack is now the surveys' finding for six properties, and §3.3.2's for all
    eight. That closes round 44's open item.
- **P2:**
  - Jalowski's sentence is split: learning and scheme awareness first, then
    stealth.
  - "The logic behind its movement" is now "the logic of the MTD scheme".
  - The close is "Neither survey names persistence or objective conditioning as
    lacking, so Section 3.3.2 scores all eight." This was checked against Cho V-D's
    three limitations and Jalowski §4.3.
  - The "most glaring flaw" quote stays.
- **Unchanged:**
  - §3.3.2's close ("still lack the eight properties"), which is the finding and
    now sits where it belongs;
  - §3.4 P1.

**Build:** clean, 0 undefined references, 0 errors. Pages 12–13 were read in the
render.

**Round 48 (Marc, 2026-10-02): §3.3.1 P2 close.** Marc accepted P2 up to its close,
which read as tacked on: it led with a negative ("Neither survey…") and ended on a
signpost.

The new close puts the point first: "Together, the two surveys find that MTD
attacker models lack six of the eight properties." §3.3.2's job then comes as the
subject: "Section 3.3.2 scores recent MTD attacker models on all eight, including
persistence and objective conditioning, which neither survey assesses."

The verb is "assesses", not "names", because Cho V-A does name persistence, as a
characteristic of an APT attacker.

**Build:** clean.

**Round 49 (Marc, 2026-10-02): P2 close cut.** Marc: the close read as circular ("you
can't read and write at the same time"), and asked whether the pointer was there
because the preamble was not doing its job. The preamble does that job.

- **"Six of the eight" is cut.** P1 sources four of the eight from the surveys, so
  the sentence read as the surveys declaring properties and finding them lacking in
  one breath. The count also repeats the evidence just given.
- **The pointer to §3.3.2 is cut.** It repeated the preamble. Its reason (neither
  survey assesses persistence or objective conditioning) went with round 47:
  §3.3.1 no longer claims a lack, and §3.3.2 scores all eight because they are the
  criterion.
- P2 now ends on Jalowski's stealth finding.

This overturns round 48.

**Build:** clean.

**Round 50 (Marc, 2026-10-02): §3.3.2 read as an examiner.** Marc: it leads with the
table again. The text is split across pages by the two floats. Table 3.3 is too wide,
and its dot "reads like black dots on a page". The key is in the prose, not the
caption. He also asked:

- Is the selection rule true?
- How should each paper's paragraph be signposted?
- The close contradicts the marks ("only MTDSim…" reads as a plug).
- Where is the bar? There are no ticks.

**Applied (formatting, ruled):**

- **Marks:** the partial mark is now a tilde (`$\sim$`). This overturns 66456ce3's
  dot.
- **Width:** the label column is a fixed 4.3 cm, ragged right, so only the lineage
  label wraps. The table is 14.8 cm, against 17.2 cm before; the 31.9 pt overfull
  box is gone.
- **Placement:** `[t]`, so Tables 3.2 and 3.3 stack at the top of p. 13.
- The same changes are applied to tab:fidelity-verdict, the twin table.

**Proposed (Marc rules):**

- **S1, the selection rule.** "Ground their attacker in ATT&CK" overstates both
  papers. Masud names ATT&CK in one sentence, and it is not in its reference list.
  Kim's attacker follows the Cyber Kill Chain, and ATT&CK maps Kim's defence. The
  true rule is "describe their attacker by the Cyber Kill Chain or ATT&CK" (the CKC
  is introduced in ch2, l.810). It also sets up the Masud finding: described, not
  modelled.
- **S2, the bar, in the text.**
  - A tick: the attacker model models the behaviour Table 3.2 defines.
  - A tilde, a "scripted stand-in": a fixed rule written at design time takes that
    behaviour's place. This is true of every tilde, and is "strict but generous"
    restated.
  - The bar is reachable: the twin table ticks six properties for this
    dissertation's model.
- **S3, the caption decodes the marks** (results standard S4; Bonneau's table legend).
  The text keeps the bar.
- **S4, a bold run-in head per model** (`\paragraph`, as in §4.5; Bonneau §IV).
  Each paragraph:
  - credits what the work does;
  - names each stand-in with the property name as the subject ("Persistence is one
    procedure repeated host by host");
  - ends with one sentence for the empty cells.
  - The (n) number keys and the "Six cells are partial" counts are cut. Numbers
    stay only in the column heads.
- **S5, the close.** "Only the MTDSim lineage has persistence, objective conditioning
  and adaptivity, each in part" is factually wrong, because Kim also has a tilde on
  persistence. It also read as a plug and contradicted the marks. Proposed: "All
  three recent MTD attacker models still lack the eight properties. Every mark in
  Table 3.3 is a scripted stand-in, and no model has anything for scheme
  awareness."

**Build:** clean, 0 undefined references, 0 errors.

**Round 51 (Marc, 2026-10-02): §3.3.2 re-scored and redrafted.** Marc: the old
reading wronged Masud ("presenting a paper like that is so bad … the properties are
flexible, they can be applied to many attacker models"). Make the playing field fair
for MTDSim and Kim too. "The rescored table looks right". Marks: mock-up set 1. For
(b) and (c): "whichever is most defensible".

- **Rule:**
  - The properties are model-agnostic. An attacker model, executed or computed, is
    scored on what enters it, and framing is reported separately.
  - Every row was re-read blind from the papers only. The evidence is in
    extractions/{brown2023,masud2025,kim2026}.md, "Fair re-score".
  - This overturns the 2026-09-07 "strict but generous" rule ("a paper that runs no
    attacker earns nothing").
- **Table 3.3** (and tab:fidelity-verdict, kept in step):

  | | Pers. | Obj. | Plur. | Adapt. | Stealth | Incent. | Learn. | Scheme |
  |---|---|---|---|---|---|---|---|---|
  | MTDSim | ✓ | P | P | P | ✗ | P | P | ✗ |
  | Masud | P | P | P | P | ✗ | P | ✗ | ✗ |
  | Kim | P | P | ✗ | ✗ | P | ✗ | ✗ | P |

  - **(b)** MTDSim's incentive-driven rationality is P, not the blind reader's ✓.
    Table 3.2 says "each attack action", and only the exploit order is weighed.
  - **(c)** Kim's scheme awareness is P. From the PDF, p. 10: T_k = T_MTD − T_ATK −
    ΣAST_i, the time left before the MTD fires, feeds ASP. It is the same rule as
    Masud's RoA.
- **Marks:** ✓ has / P in part / ✗ does not have. Blank means not applicable and a
  dash means not reported in the results standard, so neither fits. pifont glyphs.
  The decode is in the caption (results standard S4).
- **Table layout:**
  - the row label is "MTDSim" with its four citations;
  - the years have their own column;
  - eight equal 1.1 cm mark columns;
  - the table sits within the text width.
- **§3.3.2 prose:**
  - P1 is subject first, with the true selection rule ("describe their attacker by
    the Cyber Kill Chain or ATT&CK") and the bar stated once, model-agnostic.
  - Each model has a bold run-in head (`\paragraph`, as in §4.5; Bonneau §IV).
  - Each paragraph gives credit, then one sentence per property with its name first.
  - The (n) keys and cell counts are cut.
  - Masud is credited as an analytical model. "The kill chain and ATT&CK do not
    enter the computation" is stated as fact.
  - Close: "The three recent MTD attacker models still lack seven of the eight
    properties. Only the MTDSim attacker model has one in full, persistence; for
    every other mark, a fixed rule or assumption takes the place of the behaviour."
- **§3.4 S1:** "None of the three attacker models has objective conditioning or
  adaptivity in full, so none models what an APT attacker does after the foothold."
  The old sentence was false once MTDSim has persistence.
- **apt_model_criterion.md §(c):** the prior-work column is re-scored, with the
  2026-09-07 note kept for the trail.

**Open (§3.4 walk-through):** "MTD against an attacker with a foothold remains
unmeasured" needs re-reading, because MTDSim's attacker does hold footholds. The
precise gap is objective-conditioned, adaptive behaviour after the foothold.

**Build:** clean, 0 undefined references, 0 errors. The two tables are within the
text width.

**Round 52 (Marc, 2026-10-02): Table 3.3 small rulings.**

- **The caption names the scorer:** "scored by this dissertation on the eight
  properties…" (Marc: "has the property in our judgement").
- **The ch6 twin table:** our row is labelled "APT attacker model, this
  dissertation", year 2026, at the bottom below a rule.
- **Answered, not changed:**
  - The year stays its own column after the model's name. The model is the row's
    subject, and the chronological row order carries the recency.
  - The year is written "2023–2024" because the width allows it.
  - The run-in heads carry neither year nor citation, so the head matches the row
    label.
  - The run-in format (space above, no indent) is the class's `\paragraph`, as in
    §4.5.

**Flag (ch6, later):** the twin caption still says "beside the cross-section of
Table 3.3". Chapter 3 no longer uses the term "cross-section".

**Round 53 (Marc, 2026-10-02): run-in heads.** The session switched §3.3.2 to §5.1's
`\textbf` lead-ins. Marc: "don't override the convention". Reverted to `\paragraph`,
the class's own level-4 heading, as in §4.5.

**Flagged (ch5, out of scope):** §5.1's experimental setup imitates a run-in head
with `\textbf{Network.}` and so on. That is the departure from the class; the fix is
`\paragraph` there.

**Open for Marc:** under `\paragraph`, the §3.3.2 close sits inside Kim's run-in
unit.

**Round 54 (Marc, 2026-10-02): "please fix".**

- **§5.1:** the six hand-set `\textbf` lead-ins (Network, Attacker, MTD, Metrics, MTD
  ranking, Runs) are now the class's `\paragraph`. No wording changed. This closes
  round 53's flag.
- **§3.3.2's close** has its own run-in head, "Finding.", so it no longer sits inside
  Kim's unit. §3.3 still answers its own question (round 41).

**Build:** clean, 0 undefined references, 0 errors. p. 14 and p. 33 were read in the
render.

**Round 55 (2026-10-02, §3.3.2 P1, Table 3.3 row, Table 6.1 caption).** Marc, on reading P1 as a CS student and as the examiner: be specific about which eight properties, what "scored" means, who scored, and what "recent" means. Rename "the MTDSim lineage" to the ch2 term, the baseline attacker. Write the selection as a hypothesis, not a fact. Make the marks visibly the author's judgement, and make the scoring rule transparent. Applied:
- P1 now opens "This section scores three MTD attacker models, published from 2023 to 2026, on the eight properties an MTD attacker model needs (Table 3.2)".
- The first row is MTDSim's baseline attacker, cited [brown2023, zhang2023], Year 2023. Ho and Tay are dropped from the row because they reuse Zhang's attacker unchanged (brown2023.md re-score; Ho l.242, Tay l.206).
- The selection now reads "This dissertation chose them because it expects…". The superlative "the two most recent … found in this review" is cut, which overturns the 2026-09-30 R1 wording on Marc's "we kind of just chose two recent papers".
- "Executed or computed" is cut (§3.2 carries it).
- The marks are now "this dissertation's judgement from each paper", with all three marks defined and one worked example (baseline: persistence ✓, adaptivity P), plus a pointer to the evidence.
- The §3.3.2 unit head is now "Baseline attacker." and the Finding sentence follows it.
- The Table 3.3 caption now reads "Three MTD attacker models from 2023 to 2026".
- The ch6 twin row is renamed to match, and its caption now says "the three MTD attacker models of Table 3.3", which closes the "cross-section" flag.

Build clean. Ratify on read.

**Round 56 (2026-10-02, §3.3.2 P1, edits round 55).** Marc said round 55 was on track but still unclear, and asked why. Diagnosis:
- "needs" read as a prerequisite for any evaluation, not framed by the research question;
- "models the behaviour" left the verb that does the scoring undefined, so a reader could not apply the rule;
- the partial rule named one route (a fixed rule or assumption), while the marks use two: part of the definition (e.g. Kim's persistence) or a stand-in (e.g. the baseline's adaptivity);
- the rules sat in one sentence with the attacker model as subject, not the mark;
- "gives the marks" was a vague verb.

Applied:
- the phrase is now "needs to model an APT attacker", as in Table 3.2's caption;
- the baseline attacker now points to §2.2.3, whose heading is "Baseline attacker";
- there is one sentence per mark, mark first, each tied to the property's definition in Table 3.2 ("does all that … says" / "does part of that, or a fixed rule or assumption stands in for it" / "otherwise");
- the worked example is cut;
- the close is now "shows the marks … cites the evidence from its paper for each mark".

Flagged for Marc, not changed: the §3.3 preamble ("eight properties an MTD attacker model needs") and the §3.3.1 heading ("Properties an MTD attacker model needs") carry the same unqualified "needs".

Build clean. Ratify on read.

**Round 57 (2026-10-02, §3.3.2 P1 rule, §3.3 preamble).** Marc: standardise the term; the partial rule has "many different ways"; "shows the marks" of what?; add "to model an APT attacker" to the preamble. Applied:
- "score" is the act (P1 S1, the Table 3.3 caption) and "mark" is the symbol;
- each mark is named in the caption's words, which the per-model paragraphs already use ("has", "has … in part", "has no");
- the partial rule has one route, "does part of what the definition says". Every P in Table 3.3 meets it: checked row by row, each does part of its definition, and a fixed rule or assumption does the rest;
- the close now reads "shows each attacker model's mark on each property";
- the preamble now reads "needs to model an APT attacker". The §3.3.1 heading is unchanged.

Flagged: the Finding's "for every other mark, a fixed rule or assumption takes the place of the behaviour" is not true of the ✗ marks, where nothing stands in.

Build clean. Ratify on read.

**Round 58 (2026-10-02, §3.3.2 P1 rule).** Marc said round 57's P sentence said the same thing twice ("has it in part: does part of") and dropped round 56's second route. He asked to keep both routes, make "stands in for it" plain, and keep the bar conventional. Applied:
- the colon glosses are cut, since the caption decodes the marks;
- ✓ now reads "does all that the property's definition in Table 3.2 says";
- P now reads "does part of what the definition says, or its authors set the behaviour by a fixed rule, such as one response to each kind of disruption, or assume it";
- ✗ now reads "neither applies".
This overturns round 57's one-route rule. Build clean. Ratify on read.

**Round 59 (2026-10-02, §3.3.2 P1 example).** Marc said the P example was not hard-hitting. It is now "such as always re-scanning after a host-layer disruption": the baseline attacker's fixed response, in ch2's terms (§2.2.3), set against Table 3.2's "chooses". The Table 3.3 caption is unchanged: the caption names the marks, and P1 gives the rule (S4: a caption decodes, the prose defines). Marc is "pretty happy" with the rule. Build clean. Ratify on read.

**Round 60 (2026-10-02, §3.3.2 baseline attacker paragraph).** Marc's points:
- the opener said one thing twice ("runs a procedure" plus Brown's "always follow the attack procedure");
- "procedure" is no longer set against behaviour, since the scripted/behavioural taxonomy is gone;
- the Zhang sentence read as a timeline and raised "which model is scored?";
- the sentences should use ch2's attack-action language, and the P sentences should be tighter, using the P1 rule.

Applied:
- the paragraph opens on its tick;
- the Brown quote and the Zhang timeline are cut. §2.2.3 already describes the baseline attacker with Zhang's additions, and P1 points there;
- Zhang stays cited on the halved exploit, the learning evidence;
- Ho and Tay are not cited, because they reuse the attacker unchanged;
- each mark uses ch2's terms (six attack actions, goal, attack scenario, return on attack, host-layer disruption) and names the P1 route: "X, but not Y" or "a fixed rule sets …".

Marks unchanged. Next: apply the same pattern to the Masud and Kim paragraphs, and the Finding (its "every other mark" is false for ✗). Build clean. Ratify on read.

**Round 61 (2026-10-02, §3.3.2 Masud paragraph).** Marc's points:
- the "modeled after techniques in the cyber kill chain and MITRE ATT&CK" quote repeats P1's selection reason;
- the model description lost him (HARM, "a node joined to the entry virtual machines", Algorithm 2 named in prose);
- "the kill chain and ATT&CK do not enter the computation" read as an unexplained charge;
- do the crosses need a reason?

Applied:
- one context sentence (an analytical model evaluating a shuffle, diversity and redundancy MTD on an IoT cloud network, in §2.2 and §3.2 terms);
- one sentence on what the attacker model is (a computation listing every attack path to a target database per deployment interval, with each path's success probability, cost and RoA before and after the MTD deploys);
- each partial in the "X, but not Y" form;
- one shared reason for the three crosses, since P1 promises evidence for each mark;
- the quote and the framing sentence are cut.

Marks unchanged. Open for the Finding: whether the close answers P1's expectation (described by the kill chain or ATT&CK, yet lacks the properties). Build clean. Ratify on read.

**Round 62 (2026-10-02, §3.3.2 Masud refine).** Marc said round 61 was very strong, with a final push needed:
- "is a computation" is not specific: what is computed, and is "computation" the right word?
- the cross sentence's clauses are vague ("keeps anything from one interval to the next", "or when" broken by a comma);
- parrot the definitions.

Applied:
- the attacker model is now "the set of attack paths through a graph model of that network, from the Internet to a target database", in §3.2's "graph model" terms. Masud's own name for Algorithm 2 is "Security Metrics Calculation", and their graph model (THARM) is not introduced here;
- the metrics are now their own sentence, per deployment interval;
- "attack path" is used throughout;
- each cross is its own sentence in its definition's words.

Marks unchanged. Build clean. Ratify on read.

**Round 63 (2026-10-02, §3.3.2 Kim paragraph).** Marc: "same style as Masud". Applied:
- context in §3.2's terms (a real testbed, a software-defined network on physical hardware) and §2.2's (virtual IP shuffling, software diversity and redundancy);
- cut the defence's kill-chain mapping and the "we assume … CKC" quote, since both re-prove P1's selection, and the mapping is the defence's, not the attacker's;
- the attacker model is now named as one automated attack script with four stages in a fixed order, and "reverse shell" is glossed;
- "Poisson arrivals" is now "started at a random time";
- each partial follows the P1 rule: "X, but not Y", with the assumption route named for stealth ("so the evasion is assumed");
- each cross is its own sentence in its definition's words. Adaptivity ✗: a disrupted attack fails (Kim l.452). The scan Repeat parameter is a budget, not a response.

Marks unchanged. Open: the baseline paragraph bundles its two crosses in one sentence, while Masud and Kim give one sentence per cross; then the Finding. Build clean. Ratify on read.

**Round 64 (2026-10-02, §3.3.2 baseline crosses).** Marc ratified Kim's paragraph as drafted ("nothing ... that I would flag"). The baseline paragraph's two crosses are now one sentence each, as in the Masud and Kim paragraphs, and scheme awareness uses the Masud wording ("nothing in it uses which mechanism deploys next or when it deploys"). Build clean. Next: the Finding.

**Round 65 (2026-10-02, §3.3.2 Finding).** Marc asked for the Finding's purpose and how it differs from §3.4.
- **Purpose:** answer the §3.3 preamble's question from Table 3.3 alone, and close P1's expectation. §3.4 uses the Finding as evidence.
- **Now carries:** the answer and the one tick; the column reading (stealth, learning and scheme awareness rarest, one P each); the expectation answered (Masud and Kim have none in full).
- **Leaves to §3.4:** after-the-foothold, why it matters, and what this dissertation does.
- **Leaves to ch6:** our model.
- **Fixed:** "lack seven of the eight" (Masud and Kim lack all eight in full), and the false "every other mark, a fixed rule or assumption".

Build clean. Ratify on read.

**Ratified (2026-10-02).** Marc on the Finding: "really good really concise really easy to follow"; on §3.3.2 as a whole: "happy with ... as it is". Rounds 55–65 ratified on read. Next: §3.4 Research gap.

**Round 66 (2026-10-02, §3.4 Research gap; Marc: "accept").** Rebuilt as the conventional literature-review close (Swales's create-a-research-space moves), one paragraph of five sentences: what the chapter showed (§3.2.1 strategy, §3.2.2 effectiveness, §3.3.2 the three still lack the surveys' properties), the gap (the research question unanswered, verbatim), how the dissertation fills it (SQ1–SQ3 wording; Ch 4, Ch 5). No new evidence: Alshamrani's "exploratory knowledge", Cho's foothold clause, Bland, Outkin, the as-sampled scope sentence and the "ill-defined" quote cut. The "attacker with a foothold unmeasured" claim retired (false since the baseline's persistence ✓). "How effective MTD is", not "how MTD performs", in S1: §3.2.2 shows only effectiveness depends on the attacker model. Persistence qualifier dropped: "them" = the surveys' six, none held in full. Twins edited, ratify on read: ch3 intro ("states the research gap and how Chapters 4 and 5 fill it"); ch4 opener ("leave how MTD performs against APT attackers unmeasured"); ch1 ¶3 "persistence or" cut (now "fully captures an APT's adaptation to the defender"). Overturns the 2026-09-08 dictated P1/P3 and pass-5 C20 do-not-re-flag on merit. Build clean (0 undefined, 0 errors); §3.4 on printed p. 15.

**Round 67 and flag closures (2026-10-02, Marc).** §3.3.1 heading now "Properties an MTD attacker model needs to model an APT attacker" (accepted). Closed: Figure 3.1's rotated names (fine as is); ATT&CK's Stealth tactic beside property 5 (intentional: the property uses the APT definition's stealth). Deferred: the ch6 Threats-to-validity pairing (later, Marc). Chapters 2 and 3 committed (b5d67841, abdda86b) and pushed on Marc's ask.

**How to read the IDs.** G = chapter level, S = structure and headings, F = figure,
T = table, O / A / K / P / E / M / V / R / Q / H / N = prose in the opener, §3.1.1,
§3.1.2, §3.1.3, the §3.2 preamble, §3.2.1–§3.2.2, §3.2.3 and the closer, the §3.3
preamble and §3.3.1, §3.3.2, and §3.3.3. X = factual corrections verified against
a source or the code. C = content the chapter lacks, named and never drafted.
Tiers follow [`critique_protocol.md`](../workflows/critique_protocol.md) §(b): T1 is
a deletion or merge of Marc's own words, T2 a rewording offered as one suggestion,
T3 content (the gap named, not written). Line numbers are `dissertation.tex` at
commit ec761add plus the parallel ch2 session's uncommitted edits; they drift.

**Evidence base.**

- The PDF pages 8–16 as rendered, read as a reader meets them.
- A forward and backward audit of every chapter 3 fact, term, row and float against
  chapters 1–7 and the appendices.
- Five verification passes against the source markdown, the extractions, the ATT&CK
  v19.1 bundle, the hand-curated flow's builder, and the inherited code:
  - §3.1 claim by claim, with NIST SP 800-39 and Strom 2018 fetched from their
    official PDFs;
  - Table 3.1's roughly 60 (metric, source) pairs;
  - the MTDSim lineage paragraph against Brown's PDF (pp. 4, 7), Zhang and
    `mtdnetwork/`;
  - Masud and Kim against their PDFs;
  - the gap paragraph's Alshamrani, Bland and Outkin claims.
- The new yardstick [`literature_review_conventions.md`](../workflows/literature_review_conventions.md).

---

## 1. The yardstick, in five lines

- **Purpose.** Chapter 3 argues from the literature that MTD has not been evaluated
  against an attacker that behaves like an APT after its foothold, and it fixes the
  eight properties that chapter 4 builds toward and §6.3 scores against. It does not
  describe; it "interweave[s] … studies to build up the argument that the problem …
  is not yet solved" (Evans, Gruba & Zobel, p. 78).
- **Context.** What the field has done, one level above each paper: how APT
  behaviour is recovered from CTI, how MTD is evaluated, and what attacker those
  evaluations run. The dissertation's own choices are chapter 4's (EGZ p. 81).
- **Audience.** A fourth-year CS student arrives from chapter 1 already knowing
  Volt Typhoon, M-Trends, the plain APT definition and MTD, and from chapter 2
  knowing the baseline attacker, SDR, CVSS and return on attack. The examiner forms
  a first impression "often by the end of the literature review" (Mullins & Kiley,
  p. 377), and marks critical engagement above coverage (Golding et al. §7).
- **The lean test.** Nothing enters that a later chapter does not lean on, and
  nothing a later chapter leans on is missing. For a review this has a second edge:
  every property and limitation named here is taken up later, whether built,
  disclaimed or measured (yardstick checklist 12).
- **The float test.** A synthesis float earns its place only when a sentence draws
  a conclusion from it (Boote & Beile, criterion G). The scoring table fixes its
  criteria first, states its row rule, defines the partial mark in the text, and
  carries no aggregate (Bonneau et al. 2012 §V-D).

## 2. Verdict and the three moves that matter most

**Chapter verdict: correct, then tighten.** The shape is right and matches the
genre: three themed strands, each closing on its limitation, then criteria
(Table 3.2), scoring (Table 3.3) and the gap. The prose is on budget (2 848 words
against 3 000) but unevenly spread: §3.1 runs about 1 020 against 750, and §3.2
about 490 against 750. The defects are of three kinds.

- **Correctness.** Seventeen claims fail against their sources (§9). Five of them
  sit on the argument's spine, in the scoring and the gap:
  - Kim's shell is not severed by the MTD trigger (X1).
  - Masud's return on attack drives no selection (X2).
  - The lineage attacker was not "carried unchanged" (X3).
  - The gap says the lineage "cannot … remember", against its own partial learning
    cell (X4).
  - "An attacker that cannot adapt overstates MTD's effect" is uncited, and
    chapter 5 does not show it (X5).
- **The lean test fails both ways.**
  - About two-thirds of the chapter's facts are used nowhere later. §3.1.1 retells
    chapter 1's opening paragraph (Volt Typhoon, M-Trends, the APT definition), and
    Table 3.1 lists about 40 metrics of which six appear again.
  - Chapters 4–6 lean on things chapter 3 lacks: why the attacker model changes the
    MTD verdict (C1), the attacker MTDShield learned against (C2), and a field
    antecedent for the reduction metrics (C3).
- **One term, two things, across chapters (G2).** *Dwell time*, *action*,
  *attack profile*, *phase*, *effectiveness metrics*, *disruption* and *MTD
  interval* each mean something different in chapter 3 from what they mean in the
  chapter that owns them. The dwell-time collision produces an outright
  contradiction: chapter 4 (l.4953) says dwell times "do not exist in CTI vendor
  reports" two chapters after chapter 3 quoted one from M-Trends.

**The three moves, in priority order:**

1. **Fix the scoring and the gap (X1–X9, T3).** They are what an examiner checks
   hardest: every cell traceable, every sentence of the gap sourced. Also state the
   sample's selection rule as it was actually run (X9, C5).
2. **Lean both ways.**
   - Cut the chapter 1 restatements and the unused detail from §3.1 (A3, K2, K3, P6,
     P10): about −165 words.
   - Cut the fifth telling of "the attacker model is the weak link" from §3.3.3 (N4).
   - Add C1–C3, each a sentence, each with its source already located.
3. **One term per thing across chapters (G2).** Mostly word swaps at chapter 3's
   sites. Two need a registry ruling first: *disruption* against chapter 2's
   *interrupt*, and *effectiveness metrics* against chapter 4's grouping.

Projected: about 2 550 prose words, 5 floats, and Table 3.1 about a third shorter
(T1).

---

## 3. Chapter-level findings (G)

**G1. The lean test, both ways.** From the audit (`chapter_scrutiny.md` §3B), these
chapter 3 facts are used nowhere later:

- the NIST behavioural restatement (l.1038);
- M-Trends' 14 d and 122 d (l.1107); chapter 1 l.216 already gives "four months";
- Volt Typhoon's five years, NTDS.dit, OT pre-positioning and the espionage contrast
  (l.1118–1176); chapter 1 l.217–222 tells the first two;
- ATT&CK's catalogue IDs and the Enterprise / ICS / Mobile split (l.1214–1240);
- the "stable enough to model against" closer (l.1272); chapter 4 argues from
  coverage, not stability (l.4109–4118);
- process mining, ChronoCTI's 713 / 124, and AttacKG+ (l.1536–1560);
- the hand-curated flow's 57 of 73 edges (l.1650); it is not among the 38 flows;
- all of §3.2.1 except the machine-learning sentence (l.1981–2019);
- the benchmarking critique (l.2161–2201);
- the evaluation methods' trade-off pair (l.2671–2693);
- Masud's and Kim's operational detail (l.3591–3639), used only by Table 7.1's copy
  of Table 3.3;
- Bland and Outkin (l.3748–3755); Outkin is never cited again.

Not every unused fact should go. A review is also judged on coverage and critical
engagement, and some of these carry the argument inside the chapter:

- The Masud and Kim detail is the evidence for their cells.
- The benchmarking critique is the field-level diagnosis.
- Figure 3.2 is the chapter's only drawn example of a flow; examiner feedback on the
  lit review named missing images as a cost.

The per-item verdicts below say which to keep and why.

These are needed later and are not in chapter 3, or are there in a form the later
chapter cannot use:

- why the attacker model changes which MTD mechanism wins (ch5 §5.3.2, the ranking
  reversal; ch6 §6.2). Cho Sec. VI-A has the sentence (C1);
- the attacker MTDShield learned against (ch6 l.8526, placeholder) (C2);
- a before-and-after (reduction) family behind NCR and ASP reduction, the headline
  metrics (ch4 l.5456–5476) (C3);
- a bridge from chapter 3's objective triple (exfiltration, impediment,
  positioning) to chapter 4's four attack profiles (exfiltration, impact, double
  extortion, none). Positioning, the objective §3.1.1 spends 60 words on, has no
  profile and no sentence explaining why. This is a chapter 4 insertion; flagged.

**G2. One term, two things, across chapters.**

| Object | Chapter 3 says | The owning chapter says | Proposal |
|---|---|---|---|
| attacker time in an intrusion | "median dwell time" (l.1108, M-Trends' time-to-detection) | *dwell time* = time on a tactic (ch4 l.4141; registry row "dwell time"); "do not exist in CTI vendor reports" (l.4953) | ch3 says "go undetected for a median of …" (A3). Removes the contradiction without touching ch4 |
| an Attack Flow node | "actions (the ATT&CK techniques)" (l.1597), "per-action timestamps" (l.1753) | *action* = one of the simulator's six operations (registry row 72; ch1 l.387, ch2) | "techniques" at both sites (P7, P10) |
| the thing attack profiling produces | "Reusable attack profiles" (l.1495), the field's generic sense | *attack profiles* = $c_1$–$c_4$ (ch1 l.382, ch4 l.4232; registry) | "Reusable profiles" or "these representations" (P3) |
| the APT lifecycle bands | "five-phase lifecycle", "phases" (l.1061, 1064) | *stage* for the lifecycle, *phase* for the baseline attacker's six (registry row, 2026-09-08 and 2026-09-30) | "five-stage", "stages" (A2); ch4's four stages flagged (§10) |
| the MTD event that stops the attacker | "disruptions" (l.3575, 3577) | ch2 now says *interrupt* / *interruption* throughout (l.826–836); the registry ratified *disruption* (2026-09-08), and ch5's heading keeps it (l.7480) | **Registry ruling needed**: ch2's redraft overturned the row in practice. Whichever wins, ch3 follows |
| time between deployments | "MTD interval" (l.3639, own voice) | *deployment interval* (ch2 l.741; registry, ratified) | swap in own voice (R9) |
| Cho's purpose group | "the effectiveness metrics" (l.2134, 2240, 3089, 3740) = everything attacker- and defender-side under effectiveness, incl. ASP, NCR, MTTC | ch4 "MTD effectiveness" (l.5431) = the reductions and per-deployment metrics only; ASP, NCR, MTTC are "Attack outcome" | **Registry ruling needed.** Recommendation: ch3 keeps Cho's word, qualified once ("Cho et al.'s effectiveness metrics"), and ch4's §4.5 group heading is noted as a narrower sense |
| one MTD mechanism | "one defence against a single or small set of attacks" (l.2895) | *MTD mechanism* (registry row 206; the 2026-09-30 bare-*defence* sweep) | "one MTD mechanism" (Q5); the clause's other half already says "multiple MTD mechanisms" |
| the post-foothold campaign | "after initial access" (l.3720), "an attacker with a foothold" (l.3723, 3769) | *foothold* (ch1 l.224, Table 3.2 row 2, ch4 opener) | "after the foothold" (N2) |

**G3. Chapter 1 overlap.** §3.1.1 P3 retells chapter 1 P1:

- M-Trends' espionage median;
- Volt Typhoon's five years;
- valid credentials and living off the land.

§3.1.1 P1 restates chapter 1's APT definition with the same citation. Chapter 1
P1 also carries simulation's dominance and "attacker models far simpler than an
APT (Cho, Jalowski)", which §3.2.3 and §3.3.1 tell again.

The definition should stay: the review is where the formal definition and its
sources belong, and chapter 1's is the plain one. The Volt Typhoon and M-Trends
retelling should go, except the one fact chapter 4 leans on: pacing depends on the
objective (A3).

**G4. Repeats inside the chapter.** "The attacker model is the weak link" is told
five times:

- §3.2.1 close (l.2042);
- §3.2.2 close (l.2240);
- §3.2.3 (l.2798);
- the §3.3 preamble (l.3089);
- §3.3.3 (l.3740–3743), which restates the first two with section references.

Other repeats:

- The profiling apparatus sitting outside MTD evaluation: l.1759 and l.3745–3757.
- Simulation's dominance: l.2766 and l.2780, consecutive.
- The flexibility and validity ordering: l.2671 and l.2690.
- Cho Sec. V-D: l.2895 and l.3160.
- The §3.3 preamble and §3.3.1's first sentence, near verbatim.

N4, N5, Q1, Q2, Q3 and V1 each remove one.

**G5. The mark legibility and the counts in the gap.**

- Table 3.3's partial mark is `\scalebox{0.55}{\textbullet}` (l.81). On the printed
  page it reads as a stray full stop (p. 14).
- The gap opens on counts ("partially fulfils six of the eight properties, Masud et
  al. none, and Kim et al. two"). The yardstick's scoring-table rule 4 is Bonneau et
  al.'s refusal to aggregate: "we have resisted the temptation to produce an
  aggregate score … (e.g., by counting the number of benefits achieved)".
- See T3 and N1.

## 4. Structure and headings (S)

The three-strand structure, and its order (capture → evaluate → model, the model
strand last because it states the gap), are right and stay (port plan CONFIRM 1,
2026-08-31). The yardstick agrees: themes at the top, a funnel overall
(§(c)1). Four smaller points:

- **S1. The §3.1 heading and the opener disagree.** The heading reads "Survey of APT
  attackers"; the opener says §3.1 "surveys how APT attacker behaviour is recovered
  from CTI". The standing preference is for signposts to name each section in the
  words of its heading.
  - Suggestion: heading "APT attacker behaviour", with the opener unchanged.
  - Alternative: keep the heading and make the opener's clause "surveys APT
    attackers and how their behaviour is recovered from CTI".
  - Tier: heading, Marc's ruling.
- **S2. §3.3 and §3.3.2 headings are near-duplicates** ("Attacker models in MTD" /
  "Attacker models in recent MTD evaluations"). Low priority. §3.3.2 could read
  "Recent MTD evaluations", since the section heading already says what is scored.
  Marc's call.
- **S3. §3.3.1's two paragraphs run against the table's numbering.**
  - P1 walks Cho V-D's three under-developed dimensions and Jalowski, which give
    properties 3, 6, 7 and 8. P2 walks Cho V-A's four characteristics and NIST,
    which give 1, 4, 5 and 6.
  - The table lists 1–8, campaign half first. Swapping P1 and P2 (T1, move only)
    makes the reader meet what an APT attacker *is* before what the field *lacks*,
    in the table's order.
  - Re-opens nothing ruled: the 2026-09-07 rebuild set the paragraph contents, not
    their order.
- **S4. The §3.2 closer is a heading-less paragraph after `\medskip`** (l.2893). It
  reads as part of §3.2.3. Keep, but see Q5: its first half is the one sentence in
  §3.2 about the attacker, and it could carry the hinge into §3.3.

## 5. Figures (F)

Both figures were run against the pitfall catalogue
(`.claude/skills/scrutinise-figure/diagram_best_practice.md` §4). Only hits are
listed. A `scrutinise-figure` run is the gate after the fixes, not before.

### F1. Figure 3.1, the ATT&CK Enterprise matrix (p. 10): keep

- Referenced from §3.1.2 (l.1262). It is the only float that shows the 15 tactics
  chapter 4's attack graph is built over. Chapter 4 says "15 tactics" at l.5190
  without pointing here; add "(Figure 3.1)" there as a consequential edit (flagged,
  out of scope until ruled).
- The silhouette's per-tactic counts are unreadable in print ("shape only", ruled
  2026-09-02). Silent is licensed; nothing asserts a falsehood.
- The italic grey annotations ("the techniques of one tactic", …) are small but
  legible at 100 %.
- No change proposed.

### F2. Figure 3.2, the Volt Typhoon flow (p. 11): keep, relabel, own it

- **P2 / P12, the marks are undecoded.** The drawing uses marks a reader cannot
  read:
  - blue fill for conditions and the OR operator;
  - "T" / "F" tabs on the two conditions, which are Attack Flow's true / false
    outcomes (`tools/restyle_attackflow_svg.py` l.12);
  - the OR node.
  
  Neither the caption nor the prose says what they are. The prose (l.1597–1602)
  names effect edges, AND/OR operators and conditions, but not in the figure's
  terms.
  
  Proposal: the caption says how to read it. Suggestion: "… techniques in grey,
  conditions in blue with their true and false outcomes, joined by effect edges".
- **Own work presented inside the review (yardstick §(d), "own work leaking in").**
  The flow was built for this dissertation and is not in CTID's corpus, but the
  caption reads as if it were a source figure.
  - Proposal: "drawn for this dissertation from the joint advisory AA24-038A".
  - "Reduced to its spine" then becomes "reduced to 13 of its 73 edges"? Or cut:
    the drawing already shows what it holds. Recommendation: cut "and reduced to
    its spine"; P9 cuts the 73-edge sentence, and "spine" names nothing a reader
    can check.
- **Type size.** The labels print at about 5 pt against the ~8 pt guide (accepted
  2026-09-03 for portrait). Standing, not re-opened.
- **Verified clear.** The drawing holds 10 techniques, the OR node and 2 conditions:
  the README's 13-node induced subgraph. Every technique ID matches the builder.

## 6. Tables (T)

### T1. Table 3.1, metric families (p. 13)

- **Keep, as the field map.** Its sprawl is the evidence for Jalowski's "too many
  metric families with no agreement" (l.2166). Chapter 4 cites it for the three
  outcome metrics (l.5390). Two sentences draw conclusions from it: ASP dominates,
  and the split. It passes the float test.
- **Blocking, citation errors (X10).** The attack-paths cell cites `ho2024` and
  `tay2024` for APV, APN and APE.
  - Neither uses APV or APN. Both mention APV only in related work (ho:230,
    tay:186).
  - Each defines a *different* APE under Hong's name (ho:326, tay:238).
  - Proposal: `hong2018` alone on APV, APN and APE; Ho's and Tay's path-exposure
    scores either as their own entry or dropped.
- **Placement disputes, Marc's call (X11).**
  - Mission success [zaffarano2015] sits defender-side effectiveness, as Cho
    re-files it (cho:593). Zaffarano treats the difference as the cost to users of
    deploying MTD (zaff:350, 388).
  - Attack confidentiality and integrity [zaffarano2015] sit attacker-side, as
    Zaffarano files them. Cho files both under the defender's system security
    (cho:603–607).
  - The table follows Cho in one and Zaffarano in the other. Pick one authority for
    the whole table. Recommendation: Cho, since the caption cites him, which moves
    attack confidentiality defender-side. Chapter 4 uses attack confidentiality
    (l.5364) without referring to the table's side, so nothing downstream breaks.
- **The families are this dissertation's, not Cho's (X12).** Cho supplies the 2 × 2
  frame (perspective × purpose). The seven "Measures" rows (success events,
  attacker time, …) are a grouping Cho does not make.
  - Proposal: the caption credits the frame to Cho and the rows to this
    dissertation. Suggestion: "Metric families in MTD evaluation, in Cho et al.'s
    perspective × purpose frame [cho2020]; the grouping by what each counts is this
    dissertation's."
  - The header "Measures" breaches the *metric*-not-*measure* registry row. Say
    "What it counts".
- **Names, minor (T0).**
  - Ho names IPV *Network Address Variability* (ho:396); the acronym IPV is Masud's.
  - Hong never expands ACD; "attack compromise duration" is Zhang's gloss.
  - he2025's "detection rate" is its ADR / MDR.
  - Cho also lists MTTC (cho:584), uncited in that cell.
- **Length (T1 cut, Marc's call).** About 40 metrics across 22 citation groups; Marc
  has said table text is hard to read.
  - Option A: keep every row and apply only the fixes above.
  - Option B: cut the efficiency half to one row per perspective (attack cost and
    RoA / defence cost and QoS). No later chapter uses efficiency (the audit; RoA
    survives only in Appendix E).
  - Recommendation: B. It saves about a third of the table and keeps the frame, and
    §3.2.2's text never mentions efficiency after the split sentence.
- **Placement (T0).** The float lands at the top of p. 13, inside §3.3.1, splitting
  "The first / is the smart, learning-capable attacker". Move the `table` source
  above §3.2.2's first paragraph, or give it `[p]`, so it lands in §3.2.
- **C3 below:** the table has no before-and-after family, which the headline metrics
  need.

### T2. Table 3.2, the eight properties (p. 14): keep

It does exactly what the yardstick asks: criteria sourced and fixed in their own
float before any scoring (§(e)1), and the merge declared as the dissertation's own
synthesis (l.3196).

- **Locator, row 4 (X13).** Alshamrani Sec. II-A holds only the NIST quotation on
  adaptivity (alsh:53), so the row counts NIST twice. Alshamrani's own adaptivity
  point is Sec. II-B (alsh:77). Change the locator to II-B, or drop Alshamrani from
  row 4.
- **Row 7 against chapter 4.** "The defender's patterns learned over time and
  retained across deployments". Chapter 4 (l.5257–5259) puts the defender-pattern
  half out of scope. That is consistent, and a disclaimer, which the yardstick
  counts as "taken up". Table 7.1 (l.8771) then ticks property 7 as "has the
  property as Table 3.2 defines it", which contradicts both. Out of chapter,
  flagged (§10).

### T3. Table 3.3, the scoring (p. 14)

- **Blocking: the partial mark is unreadable.** `\propstandin` =
  `\scalebox{0.55}{\textbullet}` (l.81) prints as a full stop.
  - The 2026-09-07 redesign specified `\LEFTcircle` (the tex comment at l.3432) and
    it did not survive.
  - Proposal: a half-filled circle for partial and a filled circle for met, the
    feature-matrix genre the redesign chose. Change the two macros at l.80–81; this
    also fixes Table 7.1.
- **Definitions in the caption.** The caption decodes the three marks (l.3542–3546).
  - The supervisor's 2026-09-22 ruling is no definitions in captions (memory: *No
    invented terms*), and the yardstick's rule 3 says "the partial mark is defined
    in the text".
  - Proposal: move the decode to §3.3.2 P1's pointer sentence (one clause: "a
    filled circle where the attacker model has the property as Table 3.2 defines it,
    a half circle where the executed attacker does something under the property that
    falls short of that definition"), and cut the caption to its title.
  - **Re-opens** the 2026-09-08 *partial* ruling's placement (caption decode), not
    its word.
- **Cells to re-check after X1–X4.**
  - Lineage (2): true of Brown only; Zhang dropped the targeted scenario (X3).
  - Lineage (7): the rule is Zhang's, but the inherited code never charges a halved
    time (X4); Marc's disposition.
  - Kim (4): the cell's prose reason is false (X1); the cell stays empty.
- **The Masud row is empty in every column.** That is honest and the prose says why
  ("No attacker acts in the evaluation"). Keep.

## 7. Prose ledger

Word deltas are approximate, on the rendered text. "Ruling" marks a proposal that
re-opens a recorded ruling; the ruling is named.

### Opener (69 words; session-generated, ratified 2026-09-26)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| O1 | keep | 0 | Says what each section delivers, in SQ order, and why the model strand is last. Passes yardstick checklist 1: it says *where* the gap is drawn without stating it. S1 is the only change it would take |

### §3.1 preamble (62) and §3.1.1 Advanced persistent threat (273)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| A1 | "a *threat* defined by its objective: data exfiltration, impediment of mission-critical components, or positioning for future operations \citep{alshamrani2019}" → cite `nist2011sp80039` on the triple | 0 | **X6**, T0. The triple is NIST's (SP 800-39 App. B, p. B-1). Alshamrani relays it as "defined by NIST in [3]" (alsh:85), and his own *threat* term lists two. l.1176 already says "NIST's third objective class", so the chapter currently credits one triple to two owners |
| A2 | "five-phase lifecycle" → "five-stage lifecycle"; "The first two phases" → "The first two stages" | 0 | T2, G2; registry row *stage* (lifecycle) vs *phase* (baseline's six), ratified 2026-09-08. The five-vs-four clash with ch4 l.5185 is ch4's to reconcile (§10) |
| A3 | P3 (l.1106–1176, ~150 words) → keep "The pacing depends on the objectives." and one fact for each objective contrast. Suggestion from the paragraph's own words: "The pacing depends on the objectives: espionage intrusions go undetected for a median of 122 days, against 14 for all intrusions \citep{mtrends2026}. Volt Typhoon performed discovery without exfiltrating data, pre-positioning for possible future operational technology (OT) disruption \citep{cisaaa24038a}, NIST's third objective class \citep{nist2011sp80039}." | −80 | T1 cuts + one T2 joint. Claim flag. **Cut:** "APT attackers are still being documented today" (spoken residue); the five years and LOTL (ch1 l.217–222 tells both); NTDS.dit (unused; also drops the advisory's "likely" and single-compromise scope, X7); "This is not consistent with traditional cyber espionage, where there is exfiltration over a shorter time frame" (**X7**: the clause "over a shorter time frame" is not in AA24-038A). **Kept:** the pacing sentence ch4 l.4183 leans on, and the example of an objective that forgoes exfiltration, which pays off P2's rider. "Dwell time" leaves ch3 (G2). **Re-opens** the 2026-09-02 pass-5 R2 ("the currency opener stays") and E2 ("espionage-contrast keeps its pared form"), on duplication with ch1 and on X7. Add a cite to "The pacing depends on the objectives": it is currently uncited (the M-Trends blog, l.161, carries it) |

### §3.1.2 MITRE ATT&CK (227)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| K1 | "has become the lingua franca for attacker behaviour" → "has become the common language for attacker behaviour" | 0 | T2, minor. Neither cited paper says "lingua franca"; Büchel says "de facto standard … common language" |
| K2 | cut "The attack matrix decomposes into Enterprise, ICS, and Mobile; among public exports, the Enterprise bundle preserves the richest campaign-level structure \citep{ferraz2026}." | −24 | T1, claim flag. Unused later: ch4 states Enterprise v19.1 itself (l.4383). ICS is never expanded. "Exports" and "bundle" lean on STIX, defined only in §3.1.3. And the matrix does not "decompose": the three are separate domain matrices (Ferraz l.31; Rodríguez l.71) |
| K3 | cut "Behaviour at the technique-and-tactic level is stable enough to model an attacker against because it captures the persistent operational habits of APT attackers, distilled into the matrix from observed operations." | −30 | T1, claim flag. Uncited since its carrier (Sadlek) was cut on 2026-09-02, and a thesis sentence may not commit to an uncited claim (voice §(e)). Unused: ch4 picks the tactic level for coverage (l.4109–4118). **Re-opens** the 2026-09-02 ruling that assembled it ("rework that point into just one sentence"). Alternative: cite it, if a source is to hand |
| K4 | "ATT&CK organises behaviour into a four-level hierarchy of tactics, techniques and sub-techniques, and procedures" → "a hierarchy of tactics, techniques, sub-techniques and procedures \citep{strom2018mitre}"; keep `rodriguez2024` on the what / how / procedure definitions | −2 | **X8**, T0 + T1. Rodríguez frames three concepts and never defines sub-techniques; Strom §1 has all four. The "and … and" grouping also reads as three |
| K5 | keep the Volt Typhoon thread (G1017, S0002, C0035, the T1078.002 walk) | 0 | keep. Unused later, but it is the concrete instance the voice asks for (§(c)8), and Figure 3.1 draws it. Verified against the v19.1 bundle |

### §3.1.3 Attack profiling (457)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| P1 | keep the definition sentence | 0 | Verified: Rodríguez's trait triple, verbatim |
| P2 | "The persistent obstacle is a procedural-semantic gap" → "procedural-semantics gap" | 0 | T0. Ferraz's own term (title; l.60, 167) |
| P3 | "Reusable attack profiles can be operationalised …" → "Reusable profiles can be operationalised …" | −1 | T1, G2. *Attack profiles* is ch1's and ch4's name for $c_1$–$c_4$ |
| P4 | "The ATT&CK-in-STIX export encodes no temporal order …" → "does not directly encode temporal order …" | +1 | T2, minor. Ferraz l.78 says "does not directly encode"; campaign objects "typically encode time windows" (l.74) |
| P5 | "Automated extraction dominates the literature \citep{buchel2025} and spans three families: natural language processing (NLP), process mining (PM), and large language models (LLMs)." → "Automated extraction is the larger body of work \citep{buchel2025} and spans natural language processing (NLP) and large language models (LLMs)." | −4 | **X14**, T2. Büchel never compares automated extraction against manual curation ("a lot of research", "over 40 papers"), and its families are NER / classification / generation. "Process mining" has 0 hits in Büchel, so the NLP / PM / LLM triple is the dissertation's own. PM's only exemplar (Rodríguez) was cut on 2026-09-03 (R1), so PM is named and never used |
| P6 | cut "applied to 713 reports, ChronoCTI mines 124 recurring temporal patterns" → end the sentence at "at scale \citep{rahman2025}" | −10 | T1. Unused later; the SoK verdict carries the paragraph's point. Marc's call: the numbers are the paragraph's only concrete instance |
| P7 | "a Systematization of Knowledge (SoK) on TTP extraction finds that generative and embedder-based methods do not yet beat traditional NLP classifiers in realistic open-set evaluation" → "… finds that traditional NLP methods still outperform generative and embedder-based ones in realistic open-set evaluation" | 0 | **X15**, T2. Büchel's key insight 2 is "traditional NLP approaches still notably outperform"; the open-set winner is rule-based NER, and Büchel's own *classification* family is among the losers. "Near $F_1 = 0.70$" merges two statements (§9 "the F1-score bar set at 70 %"; insight 1, about 80 % precision at 66 % recall on the top 50). Keep it, or say "about 80 % precision at 66 % recall" |
| P8 | "released by MITRE Engenuity's Center for Threat-Informed Defense (CTID)" → "released by MITRE's Center for Threat-Informed Defense (CTID)" | 0 | T0. "Engenuity" is in neither the cited v3.2.0 document nor the bib entry |
| P9 | "In a flow, actions (the ATT&CK techniques) are joined by *effect* edges …" → "In a flow, ATT&CK techniques are joined by *effect* edges …" | −1 | T2, G2. *Action* is the registry's word for the simulator's six operations |
| P10 | "Volt Typhoon had no example flow in this corpus, so one was curated by hand from the joint advisory AA24-038A \citep{cisaaa24038a}. The advisory states the ordering behind 57 of the flow's 73 edges; the remaining 16 are inferred from its prose." → "Volt Typhoon has no flow in this corpus, so this dissertation drew one from the joint advisory AA24-038A \citep{cisaaa24038a}." | −20 | T1 + T2 joint, claim flag. Yardstick: own work in the review is marked as the dissertation's (EGZ p. 81). The 57 / 73 count is unused later, and it counts edges of a 73-edge flow while Figure 3.2 draws 13, so the reader cannot check it against the drawing. **Re-opens** the 2026-09-03 pass-4 M2 insert (session words, ratified on read) and its pass-6 option A |
| P11 | "The Attack Flow schema defines optional per-action start and end timestamps, but the public corpus leaves them all but empty, because breach reports rarely contain machine-usable timestamps; …" → "The Attack Flow schema defines optional start and end timestamps for each technique, but the public corpus leaves them all but empty; …" | −8 | T1 cut + T2 (G2, *action*). Claim flag: "because breach reports rarely contain machine-usable timestamps" is carried by neither cited source; its origin is the dissertation's own note (`tactic_duration_precedent_survey.md` l.35). The measured emptiness (36 of 38 flows) stands without it |
| P12 | keep the strand's last sentence ("The apparatus … sits within the threat-intelligence and incident-response literature, outside MTD evaluation.") | 0 | keep. It is SQ1's answer. N4 cuts its §3.3.3 repeat instead |

### §3.2 preamble (31), §3.2.1 Defence modelling approaches (177), §3.2.2 Metrics (139)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| E1 | "Evaluating an MTD mechanism involves three steps. The mechanism is designed under a defence modelling approach (§3.2.1), instrumented with metrics (§3.2.2), and evaluated under an evaluation method (§3.2.3)." | ±0 | T2, logic. Designing a mechanism is not a step in evaluating it. Suggestion: "An MTD evaluation rests on three choices: the defence modelling approach the mechanism is designed under (§3.2.1), the metrics it is instrumented with (§3.2.2), and the evaluation method (§3.2.3)." Session-generated connective prose, ratified 2026-09-26; ratify on read |
| E2 | "Mechanisms that are not built using these approaches are subsumed by the SDR operation alone \citep{cho2020}." | — | **Unverified**: "subsumed" has no match in Cho's source markdown, and the SDR passages (cho:96, 170, 274) do not say it. Pass-6 posed a clarity question (2026-09-07) that was never answered. Cut (−14), or locate it in Cho |
| E3 | "In machine-learning approaches the attacker model is supplied by the training environment, …" | +20 | T3 → **C2**. The one §3.2.1 sentence a later chapter leans on (ch6 l.8526). It lacks its instance: MTDShield learned against MTDSim's baseline attacker \citep{tay2024}. The 2026-09-07 pass-6 note already says "concreteness partial until … what MTDShield trained against"; G1, which was to carry it, was cut |
| E4 | "In game theory the attacker is a utility maximiser … However, attackers are not necessarily rational or intelligent \citep{cho2020}." against property 6 | — | T3, clarity. The chapter dismisses the rational attacker, then requires "incentive-driven rationality". Cho holds both (VI-A con; V-A characteristic), and Table 3.2's row 6 ("decisions conditioned on a cost/benefit signal") is compatible. The reader is not told. One clause at property 6's source sentence in §3.3.1 ("sensitive to incentives, not a payoff maximiser") would do; Marc's words |
| M1 | "The primary issue facing MTD mechanisms, in Jalowski et al.'s reading … : metrics are produced on an ad hoc basis, there is little consensus on how to measure and instrument, there are too many metric families with no agreement between them, and there is no common benchmark to measure effectiveness or efficiency." → end the colon list at "too many metric families with no agreement between them" | −22 | T1. The fourth clause restates "cannot be benchmarked" at the sentence's head, and the first two say one thing. Keep the family clause: Table 3.1 is its evidence (T1) |
| M2 | "The effectiveness metrics are dependent on how the attacker was implemented …" | 0 | keep; G2's registry ruling may qualify "effectiveness metrics". Hong's claim is the chapter's hinge into §3.3, and the 2026-09-07 cold read reduced it to this one sentence on purpose |

### §3.2.3 Evaluation methods (115) and the closer (25)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| Q1 | "Moving from analytical models to a real testbed, flexibility and validity rise. Scalability falls and cost climbs \citep{cho2020}. Simulation is high flexibility, high level of abstraction, but low validity, whereas a real testbed has high flexibility and validity but is not scalable and is high cost \citep{cho2020}." → keep the first two sentences; cut the third | −28 | T1, **X16**. The third restates the ordering at its endpoints. "High level of abstraction" is analytical models' con in Cho's Table VI, not simulation's; simulation's con is "inherent uncertainty toward real-world applications", which Q3 carries. The real testbed has the *highest* flexibility, so "high flexibility" for both does not show the rise the first sentence claims |
| Q2 | "Simulation remains the dominant method \citep{cho2020}. This dominance is because of the high flexibility, above all in modelling attack behaviours \citep{cho2020}, and low barrier to entry." → "Simulation remains the dominant method, for its flexibility above all in modelling attack behaviours \citep{cho2020}." | −14 | T1 merge. Claim flag: "low barrier to entry" is uncited (Cho's pro is "easy parameterization for sensitivity analysis"). "Above all in modelling attack behaviours" is VIII-B verbatim in sense, and it is the hinge into §3.3 (the pass-4 M2 insert of 2026-09-07) |
| Q3 | "However, as a trade-off, parameters that are not captured in a simulator \citep{cho2020} are not accounted for in MTD mechanism logic." → "Its cost is that variables a simulator does not capture limit what transfers to real systems \citep{cho2020}." | ±0 | T2, ceiling. Cho VIII-B: "all possible variables may not be captured … lessons … may not be realized in real testbed-based experiments". "Not accounted for in MTD mechanism logic" is an extension the cite does not carry, and it is the weak-link claim again (G4) |
| Q4 | keep S1 / S2 (Cho's four categories; the analytical split) | 0 | keep |
| Q5 | "MTD evaluation is mostly one defence against a single or small set of attacks \citep[Sec.~V-D]{cho2020}" → "one MTD mechanism against a single or small set of attacks" | +1 | T2, G2; registry row 206 (2026-09-30 sweep). The clause after it already says "multiple MTD mechanisms" |

### §3.3 preamble (52) and §3.3.1 Properties of an APT attacker (367)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| V1 | §3.3.1 S1 "Table 3.2 lists the eight properties of an APT attacker, drawn from what the two surveys say MTD's attacker models lack and from the APT definition of Section 3.1.1." → "Table 3.2 lists the eight properties of an APT attacker." | −22 | T1. The §3.3 preamble said the same one sentence earlier (l.3096). The preamble keeps it: its job is to name what each subsection holds |
| V2 | swap P1 (Cho V-D, Jalowski) and P2 (Cho V-A, NIST merge) | 0 | T1 move. S3 |
| V3 | "the agent optimising for a cost-effective outcome is modelled on the defender side and seldom on the attacker's" | 0 | keep; E4 is the clause property 6 needs |
| V4 | keep the Jalowski sentences | 0 | Verified: "the most glaring flaw in the MTD literature is the ill-defined attacker models" (jal:191); Nmap, passive reconnaissance, "mutation patterns", "the mathematical logic behind the movement" (jal:197). The mutation-patterns phrase is Jalowski's (ruled 2026-09-07, not re-flagged). The p. 8 locator is not checked against the PDF (the markdown has no page breaks); verify on read |

### §3.3.2 Attacker models in recent MTD evaluations (543)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| R1 | "Two works from 2025–2026 were selected using a keyword search for MITRE ATT&CK, as the works most likely to be grounded in attacker modelling." | — | **X9**, T3, blocking. The search appears nowhere in the record. The 2026-09-08 pass-4 M1 asked for the index and date range "as run", or for the sentence to say the works were chosen by reading. The ruling is not on record, and the prose still claims a method with no parameters. The yardstick's checklist 7 ("every sampled set states its selection rule") and Boote & Beile's criterion A are what an examiner tests. Marc: state the index, date range and hit count, or say how they were chosen. Also, the submitted review scored five works, and He et al. was cut 2026-09-07; if the sample was narrowed by a rule, state the rule |
| R2 | "MTDSim's attacker model is the baseline attacker of Section 2.2.3, carried unchanged through the later MTDSim studies except for Zhang's exploitation-time rule \citep{zhang2023}." | — | **X3**, T2. Zhang kept only the general attack scenario ("only the first attack scenario is selected", zhang:364) and moved the phase times onto an exponential draw (zhang:394). Suggestion: "… carried through the later MTDSim studies, which kept only its general attack scenario and added an exploitation-time rule \citep{zhang2023}." Cell (2)'s reason ("the two attack scenarios are fixed at design time") is then Brown's alone: "… the attack scenario is fixed at design time (2)" |
| R3 | "each kind of disruption triggers a scripted re-scan, in Brown et al.'s word ``forced'' (4)" → "each disruption of the host or service layer forces a scripted re-scan, in Brown et al.'s word (4)" | +3 | T2, **X17**. Brown's third kind, the user shuffle, forces the attacker "to look for vulnerabilities on the host" (brown:135), not to re-scan. Ch2 l.832–833 already says so, so the two chapters contradict each other now. *Disruption* vs *interrupt* per G2's ruling |
| R4 | "and exploitation time is halved on a vulnerability exploited before \citep{zhang2023} (7)" | — | **X4**, Marc's disposition. The rule is Zhang's (zhang:392, Eq. 2), but the inherited code never charges a halved time: `services.py:122-123` halves per vulnerability object, each host holds its own copies, and exploited copies are filtered out before any attempt (`services.py:286`). `metrics_semantics.md` l.229–240 measured 0 of 1 183 timing calls. Table 3.3's caption scores what "the executed attacker does". Either the cell rests on the paper's attacker (say so once, in the §3.3.2 P1 pointer), or cell (7) is empty and N2 loses its tension. Chapter 4 (l.5253) leans on the same rule for vulnerability memory |
| R5 | "a hybrid MTD" (Masud) → "an MTD combining shuffle, diversity and redundancy" | +3 | T2, G2. Masud's "hybrid" is S+D+R (masud:80), not ch2's trigger sense of *hybrid* (l.593). Closes the ch2 ledger's residue item |
| R6 | "and recomputes a CVSS-derived success probability, cost and RoA for each path before and after each MTD deployment \citep[Algorithm~2]{masud2025}" → "and recomputes a CVSS-derived success probability, risk and RoA before and after each MTD deployment \citep[Algorithm~2, Sec.~4]{masud2025}" | −1 | T2, X2's minor half. The attack cost has no stated CVSS derivation; ASP is per host in Algorithm 2; the before-and-after comparison is §3.5 and §4, not Algorithm 2 |
| R7 | "and RoA is a per-path metric (Eq.~4) consumed by the defender's selection (6)" → "and RoA is reported as an outcome; the defender selects by network centrality (Eq.~8) (6)" | +2 | **X2**, T2. Algorithm 3 lists RoC as an input, but the selection, Eq. 8, ranks hosts by closeness, degree and betweenness only (masud:466–468). The repo's own extraction says "not RoA" (`masud2025.md` l.75). Cell (6) stays empty, now for the right reason |
| R8 | "and holds a reverse shell until the next MTD trigger severs it: four kill-chain stages in fixed order, labelled with ATT&CK technique identifiers" → "and holds a reverse shell: four kill-chain stages in fixed order" | −11 | **X1**, T1 + T2. Kim's Table 5 shows the shell surviving past 600 s, at least two 300 s triggers, under IP shuffle, diversity and both. Only the redundancy configurations cut it (268 s, 199 s), through the 600 s resource reset (kim:310, 466). Kim: shuffling "is ineffective when attackers are already successful … via reverse connections" (kim:256). The run labels one ATT&CK ID, T1059, not "identifiers" |
| R9 | cell reasons: "the script does not observe the trigger that severs it (4)" → "the script does not observe the MTD (4)"; "and the scan range is sized to the MTD interval by the experimenters (8)" → "and the scan range is fixed by the experimenters (8)"; "run in sequence in one process" → "run in sequence" | −6 | **X1** (4), T2. (8): the link to the interval rests on one ambiguous parenthetical, "(e.g., MTD interval)" (kim:270); the 4096 figure is cited to prior work (kim:386). "In one process" is not in the source. This also removes the own-voice "MTD interval" (G2) |
| R10 | "scans 4096 virtual addresses for port 80 with up to five repeats, fingerprints the web service, fires the public exploit for CVE-2021-41773 where Apache 2.4.49 is found" → "scans for a web server, fingerprints it, and fires one public exploit where the vulnerable version is found" | −12 | T2, Marc's call. CVE is never expanded, and the version and address counts are unused. Counter-argument: the specifics are the evidence for cells (3) and (8). Recommendation: keep the CVE (it is what "one exploit" in (3) points at), expand CVE once, and cut "4096" / "port 80" / "2.4.49" |

### §3.3.3 Research gap (311)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| N1 | "The MTDSim lineage partially fulfils six of the eight properties, Masud et al. none, and Kim et al. two (Table 3.3)." → lead with which properties are missing. Suggestion: "No attacker model in Table 3.3 has any of the eight properties as Table 3.2 defines it, and only the MTDSim lineage has persistence, objective conditioning and adaptivity, each in part." | ±0 | T2, G5. Bonneau et al.'s no-aggregate rule (yardstick §(e)4). The counts invite the reader to rank rows by cells, which the gap does not argue. **Re-opens** Marc's 2026-09-08 dictation ("partially fulfils" ruled). Alternative: keep the counts and add nothing; the table carries them |
| N2 | "An attacker model without properties 1, 2 and 4 does not model an attack campaign after initial access: an attacker with no multi-stage knowledge to lose cannot register the value MTD claims \citep[Sec.~IV-C-2-B]{alshamrani2019}, and an attacker that cannot adapt overstates MTD's effect." → "An attacker model without properties 1, 2 and 4 does not model an attack campaign after the foothold. MTD's value is that it renders the attacker's exploratory knowledge useless \citep[Sec.~IV-C-2-B]{alshamrani2019}, and which MTD is best depends on whether the attacker's goal requires a persistent foothold \citep[Sec.~VI-A]{cho2020}." | +8 | **X5 + X18**, T2 → **C1**. Two defects, one move. (a) "Overstates MTD's effect" is uncited and ch5 does not show it: the rankings reverse between attackers (rank correlation −0.03, §5.3.2), and no uniform over- or under-statement appears. The sentence pre-claims a result. Cho VI-A (cho:479) carries the claim the chapter can make: "The differences between optimal strategies can be explained by the attack model each study used and more specifically whether the attacker's goal required a persistent foothold in the system." That is the field's own antecedent for ch5's finding. (b) Alshamrani IV-C-2-B says MTD renders "the exploratory knowledge of the attacker useless" (alsh:531), tied to reconnaissance; "multi-stage knowledge" is the dissertation's gloss, and the repo's extraction flags it (`alshamrani2019.md` l.143–148). **Re-opens** the 2026-09-08 pass-4 M1 legs (session-ported from the criterion, ratify on read) |
| N3 | "Where these models grant the attacker any rationality, it is a heuristic such as RoA \citep{brown2023}, optimised over exploits the attacker cannot sequence, adapt, or remember." → "… optimised over exploits the attacker cannot sequence." or cut | −4 / −25 | **X4 (tension)**, T1. Table 3.3 scores the lineage partial on adaptivity (4) and learning (7), and (7) is itself a memory rule. "Cannot … adapt, or remember" contradicts the table three paragraphs up. If R4 empties cell (7), "remember" can stay |
| N4 | cut "The assumptions about the attacker are baked into the logic of the MTD mechanisms (Section 3.2.1). Over the effectiveness metrics the attacker is the weakest link (Section 3.2.2): with a weak attacker model the MTD mechanisms cannot be evaluated, because the metrics are intertwined and computed over the attacker model." | −45 | T1, claim flag. G4: the fifth telling, and a recap of §3.2.1 and §3.2.2 with pointers. "Cannot be evaluated" outruns Hong's "dependent on how the attacker was implemented" (ceiling, voice §(c)7). **Re-opens** the 2026-09-07 pass-6 DO NOT RE-FLAG ("the three unit-closers on attacker assumptions … the strand's spine") and the 2026-09-26 connective pass P4, on merit: in §3.2 each closer is the strand's spine; in §3.3.3 the same claim is a recap. Alternative: keep one sentence, "Both the MTD mechanisms' logic and their metrics rest on the attacker model (Sections 3.2.1 and 3.2.2).", at −30 |
| N5 | cut "Attack profiling recovers TTP-level behaviour from raw CTI \citep{rahman2025, zhangY2025} and from runtime telemetry \citep{rodriguez2024}." | −17 | T1. G4: §3.1.3 surveyed all three, and §3.1's close already placed them outside MTD evaluation. The paragraph keeps its attacker-modelling means (Bland, Outkin) |
| N6 | "Outkin et al. \citep{outkin2022} address the parameters: they fit an attacker's per-step detection probabilities to MITRE ATT&CK Evaluations data." → "… they estimate per-step detection probabilities from MITRE ATT&CK Evaluations data." | −2 | **X19**, T2. Outkin computes each probability as the share of twelve vendors detecting the step (§5.2.1), indexed by defender type. Nothing is fitted, and the probabilities describe the defender's EDR, not the attacker |
| N7 | keep the negative-scope sentence and the close | 0 | keep. The scope sentence is the yardstick's gap-by-omission guard; the close hands over without pre-empting ch4 |

**Ledger arithmetic.** Cuts total about −345 words: A3, K2, K3, P5, P6, P10, P11,
M1, Q1, Q2, V1, R8, R9, R10, N3, N4, N5 and the small T2 deltas. Additions total
about +40: E3 / C2, N2 / C1, R5, R3. That gives about 2 540 words, within the
ledger with 460 to spare for C3 and C5.

**Minimal set**, if Marc takes only what an examiner would catch:

- the corrections on the spine: X1 (R8, R9), X2 (R7), X3 (R2), X4 (R4 and N3),
  X5 and X18 (N2), X9 (R1);
- the triple's owner (A1);
- the SoK reading (P7);
- Table 3.3's mark (T3);
- Table 3.1's path cites (T1, X10).

Each is a word-level change except R1 and R4, which need his facts.

## 8. Content the chapter lacks (C), named, not drafted

- **C1. Why the attacker model changes the MTD verdict, cited.** Cho Sec. VI-A
  (cho:479, on Carter et al. and Colbaugh and Glass): "The differences between
  optimal strategies can be explained by the attack model each study used and more
  specifically whether the attacker's goal required a persistent foothold in the
  system."
  - It replaces N2's uncited "overstates", and it is the literature's own
    antecedent for §5.3.2's ranking reversal and §6.2's close ("no single MTD
    mechanism … performs best against both attackers").
  - Home: §3.3.3 P1, or §3.2.2's hinge sentence (M2).
- **C2. The attacker MTDShield learned against.** §3.2.1's machine-learning sentence
  says the attacker comes from the training environment. Its instance is the
  deployment strategy chapter 5 runs: MTDShield trained against MTDSim's baseline
  attacker \citep{tay2024}.
  - §6.2 (l.8526, placeholder) leans on this ("trained against the baseline
    attacker"), and it is the concreteness the unit's own pass-6 note found missing.
  - One clause.
- **C3. A before-and-after family.** The headline metrics are NCR reduction and ASP
  reduction (ch4 l.5456–5476, after Alavizadeh's mitigation factor), and Table 3.1
  has no family they belong to.
  - Either one row ("change relative to no MTD", with its sources) or one §3.2.2
    clause.
  - **Verify first:** that `alavizadeh2022` defines the mitigation or reduction
    form ch4 attributes to it. The source markdown is `lit_review/alavizadeh2022.md`,
    with no extraction yet, so it has not been checked here.
- **C4. Acronyms owed.**
  - **TTP** is never bound (l.1561, 3746). Bind it once at §3.1.2's hierarchy
    sentence: "(tactics, techniques and procedures, TTPs)".
  - **CVE** (l.3624, if R10 keeps it) and **IoT** (l.3592) are never expanded.
  - **OT**, **PM** and **SDN** are each expanded and then used once, so the acronym
    does no work. Cut PM with P5. OT stays with A3. SDN: say "software-defined
    networking testbed" without the acronym.
  - RoA is expanded twice (Table 3.1, l.2528; l.3579) after ch2 defined *return on
    attack* without it. Bind the acronym once, at ch2's definition, or at l.2528.
- **C5. The selection rule, as run** (R1). Marc's facts: the index, the query, the
  date range and the hit count, or the reading-based rule. The yardstick's
  gap-by-omission test needs it before the negative-scope sentence (N7) can do its
  job.

## 9. Factual corrections (X), verified

Each is recorded with its evidence. The prose fix is in §7.

| ID | Claim (line) | Verdict | Evidence |
|---|---|---|---|
| X1 | Kim's shell "held until the next MTD trigger severs it" (l.3624, 3635) | wrong | Kim Table 5 (kim:459–464): ART_C2A ≫ 600 s under SvIP, DSW, SvIP+DSW at a 300 s interval; only RHSW cuts it (kim:310, 466); kim:256 shuffling "ineffective … via reverse connections" |
| X2 | Masud's RoA "consumed by the defender's selection" (l.3604) | wrong | Eq. 8 ranks by centrality (masud:466–468); RoC reported as outcome (masud:584–586); `extractions/masud2025.md` l.75 "not RoA" |
| X3 | the lineage attacker "carried unchanged … except for Zhang's exploitation-time rule" (l.3570) | wrong | Zhang keeps scenario 1 only (zhang:364, §4.4.1.1); exponential phase times (zhang:394). Ho and Tay add nothing on the attacker (extractions) |
| X4 | cell (7) and "cannot … adapt, or remember" (l.3727) | tension; code | the /2 is Zhang's (zhang:392); `services.py:122-123`, `:286` never charge it; 0 / 1 183 (`metrics_semantics.md` l.229–240); Table 3.3 scores 4 and 7 partial |
| X5 | "an attacker that cannot adapt overstates MTD's effect" (l.3722) | uncited; not shown by ch5 | §5.3.2: rankings reverse, rank correlation −0.03; ch6 placeholder l.8705–8711 (failure matrix changes "where the attacker goes … not what it achieves") |
| X6 | objective triple cited to Alshamrani (l.1036–1038) | wrong attribution | NIST SP 800-39 App. B p. B-1 (fetched; also a local copy at `C:\Users\marcl\Downloads`); alsh:85 "defined by NIST in [3]" |
| X7 | "not consistent with traditional cyber espionage, where there is exfiltration over a shorter time frame" (l.1168); NTDS.dit "was dumped" (l.1138) | added gloss; hedge dropped | AA24-038A: "not consistent with traditional cyber espionage or intelligence gathering operations" (no time frame); "in one compromise, Volt Typhoon likely extracted NTDS.dit …" |
| X8 | four-level hierarchy and sub-technique definition cited to Rodríguez (l.1250–1256) | wrong attribution | Rodríguez l.69 "three key concepts"; no sub-technique definition; Strom §1 has all four |
| X9 | "selected using a keyword search for MITRE ATT&CK" (l.3426) | not on the record | 2026-09-08 pass-4 M1 (tex l.3394–3406); the submitted review's §IV-B states no search |
| X10 | Table 3.1 attack paths: ho2024, tay2024 for APV / APN / APE (l.2515) | wrong | ho:226, 230, 326; tay:186, 238 |
| X11 | Table 3.1 Zaffarano placements (l.2507, 2521) | inconsistent authority | zaff:337, 350, 388, Table 4; cho:593, 603–607 |
| X12 | Table 3.1's families credited to Cho by the caption (l.2494) | own grouping | Cho's frame is §VII's 2 × 2; `extractions/cho2020.md` notes the partition is a reading of §VII, not a printed matrix |
| X13 | Table 3.2 row 4, Alshamrani Sec. II-A (l.3288) | weak locator | alsh:53 (II-A = the NIST quote); alsh:77 (II-B, Alshamrani's own adaptivity point) |
| X14 | NLP / PM / LLM families and "dominates" on Büchel (l.1534–1537) | wrong attribution; overreach | Büchel §8 (NER / classification / generation); 0 hits for process mining |
| X15 | SoK: generative / embedder "do not yet beat traditional NLP classifiers" (l.1562) | misparaphrased | Büchel insight 2 "notably outperform"; rule-based NER wins open-set; classification loses (§7, Fig. 4) |
| X16 | "Simulation is high flexibility, high level of abstraction …" (l.2690) | misparaphrased | Cho Table VI (`extractions/cho2020.md` l.103–112): abstraction is analytical's con; real testbed "highest flexibility and validity" |
| X17 | "each kind of disruption triggers a scripted re-scan" (l.3577) | overreach; contradicts ch2 | brown:135 (user shuffle → look for vulnerabilities); ch2 l.832–833; `attack_operation.py:255-264` |
| X18 | "multi-stage knowledge to lose", Alshamrani IV-C-2-B (l.3720) | misparaphrased | alsh:531 "exploratory knowledge of the attacker useless"; `extractions/alshamrani2019.md` l.143–148 |
| X19 | Outkin "fit an attacker's per-step detection probabilities" (l.3753) | misparaphrased | Outkin §5.2.1: vendor-share ratios, by defender type |

**Verified and holding** (so Marc's "are those right?" has its answer):

- every Brown and Zhang quotation and page (Brown's PDF, pp. 4 and 7);
- Kim's two quotations (pp. 7, 9) and Masud's two (p. 7);
- the Jalowski quotations;
- NIST's behavioural restatement;
- M-Trends' 14 d and 122 d;
- the G1017 / S0002 / C0035 / T1078.002 thread and "v19.1";
- ChronoCTI's 713 / 124;
- Attack Flow's semantics;
- the 57 / 73 count;
- 36 of 38 flows with no timestamps;
- the month-granularity campaign dates (110 of 112 on day 01);
- Bland's four elements;
- 53 of about 60 Table 3.1 pairs;
- every cell of Tables 3.2 and 3.3 against its paragraph.

## 10. Out of chapter: flagged, not fixed

**Simulation strength/limitation arc (round 37).** §3.2.3 now presents simulation's
flexibility as the strength the dissertation uses, and its real-network caveat
(Cho VIII-B). When ch6 §Threats to validity is drafted, its scope placeholder
("the six adopted attack actions … simulation only") should pair back to §3.2.3. The
APT attacker model is bound by the simulator's attack actions, and its results carry
simulation's caveat.

**Citation-pinpoint ruling (round 30), outside ch3: APPLIED 2026-10-01 (Marc: "remove those two ... keep the rest"; the relabels below applied with them under the ruling's IEEE-label clause).**
- **Ch4 §4.5, keep:**
  - Rodriguez Table 3 and Zaffarano Table 4 (a table; Table 4 is also a quote);
  - Hong Eqs. 1–5, Alavizadeh Eq. 13, Royston Eq. 1 (Royston's label is
    "Methods, Eq. 1" → "Eq. 1");
  - the quotations: Zhan Sec. III-B, Jung Sec. 2, Cho Sec. VII-A, Zhang pp. 32
    and 16;
  - Jung Sec. 5.2, the specific 60 s / five-address value.
- **Ch4 §4.5, strip:** Zaffarano Sec. 4.3 (paraphrase of the exposure rule) and Brown
  Secs. III-D, IV-A (paraphrase of the metric).
- **Appendix:**
  - keep Jung Sec. 5.2 (l.~9696, the value);
  - keep the three Tay citations (l.~9818–9836, reward form, hyperparameters,
    figures), relabelled "Section" → "Sec." and "Figures" → "Figs.".


- **The cost side of when to move is unmodelled** (Marc, 2026-10-01, from the
  §3.1.3 close). §3.1.3 now ends on Cho's trade-off: deploying too often costs
  service availability, and deploying too rarely gives the attacker time.
  - **Ch5 measures only one side.** In the interval sweep "every reduction except
    user shuffle's falls as the interval grows" (l.~7835). MTDSim models no
    defender cost: intent spec IS-LIM-07, "No QoS/performance-side modelling",
    Zhang §6.4, Ho §5.2. So read alone, the sweep says "deploy as often as
    possible".
  - **Owed in ch6 §Threats to validity**, construct and scope. MTD is measured on
    the attacker side only. Cho's efficiency side (defence cost, QoS; Table 3.1)
    is not, so the sweep shows the security half of the trade-off and cannot
    choose an interval. This is inherited from MTDSim; pair it with future work.
  - **Optional, in ch5:** one clause at the sweep, pointing back to §3.1.3.
  - **Related nuance:** a shorter interval need not mean more deployments,
    because a deployment occupies 20–110 s (IS-LIM-05, Zhang §6.1).
  - **Comparison tool for ch6 §Implications** (Marc, 2026-10-01: "a good
    comparison tool"; placement recommended as discussion, Marc to confirm). For
    each MTD mechanism, give the deployment interval at which the APT attacker
    model's reduction (NCR, ASP) matches the baseline attacker's at the default
    200 s.
    - It needs no invented threshold, and assumes only that, within one
      mechanism, deploying more often costs more.
    - It is read off the values ch5 already tables (the interval sweep;
      Appendix F), so ch5 gets no new metric. Report it as a bracket between
      sweep points.
    - Its reading: evaluating against the baseline understates how often MTD
      must deploy against an APT attacker.
    - It cannot be read for user shuffle (its reduction rises towards zero) or
      for MTDShield (no fixed interval).
    - Wait for the 1 000-seed numbers.
    - It moves to ch5 only if it becomes a headline result. That needs a ch4
      §4.5 definition first (ch5 antecedent rule).

- **Table 7.1** (l.8764–8771) ticks property 6, while the ch6 placeholder
  (l.8737–8739) says "Property 6: blank". It also ticks property 7 as Table 3.2
  defines it, while ch4 (l.5257–5259) disclaims the defender half.
- **Ch4 l.5185** "the four [stages] that lifecycle models … share", citing
  Alshamrani, whose lifecycle ch3 gives as five. One clause in ch4 reconciles them.
- **Ch4 l.4953** "dwell times … do not exist in CTI vendor reports": true in ch4's
  sense. A3 removes ch3's colliding use, so no ch4 edit is needed.
- **Ch4 l.4064–4098** re-introduces Attack Flow and CTID (with CTID expanded again)
  and re-argues ch3's extraction-fidelity point. That is the third telling, after
  ch1 l.379 and ch3. A pointer back to §3.1.3 would do.
- **Ch4 l.4591** points to `sec:apt-survey` for pre-intrusion behaviour. The passive
  reconnaissance support is in §3.3.1 (l.3175).
- **Ch4 l.5190** "15 tactics": add "(Figure 3.1)".
- **Ch4 profiles vs ch3's objectives** (G1): positioning has no profile; one
  sentence in §4.2.
- **Ch7 l.9040** merges properties 7 and 8 ("scheme awareness and learning across
  runs (property 8)").
- **Registry:**
  - *disruption* vs *interrupt*: ch2's redraft uses *interrupt*; the ratified row
    says *disruption*.
  - *effectiveness metrics*: ch3 means Cho's group, ch4 its own narrower group.
  - Both need Marc's ruling (G2).
- **Repo records, wrong:**
  - `services.py:118`, `provenance.md` l.48 and `metrics_semantics.md` l.250–251
    credit the exploit-time /2 to Brown's commit `a16db997`; git shows it arrived in
    `ef29978a` (2023-03-09).
  - `metrics_semantics.md` l.271–272 quotes Zhang with a string not in
    `zhang2023.md` (the actual wording is zhang:392).
  - `extractions/attackflow.md` Concept 5 and tex l.1731–1735 say MITRE NERVE
    carries 1970 epoch placeholders. It carries real dates, 2023-12-31 to
    2024-01-19, on all 33 actions. The shipped "all but empty" still holds.
- **Sources:**
  - NIST SP 800-39 is cited but held only outside the repo (Downloads). Copy it to
    `docs/sources/`.
  - `oasis2021stix` is still a DRAFT / VERIFY bib entry.
  - Ferraz and Rahman were checked against their preprints, not the versions the bib
    cites.

## 11. Stale records to refresh once the rulings land

[`../notes/ch3_lit_review/README.md`](../notes/ch3_lit_review/README.md) is the
declared shape authority. It is stale in three places:

- "a chronological story that narrows onto the gap … never a neutral catalogue". The
  2026-09-08 recast dropped the chronological rhetoric; the yardstick's §(c)1
  reconciles the two (themes at the top, chronology inside each).
- The three sections are listed in the old order (APT attackers, attacker models,
  how MTD is evaluated); the tex has MTD evaluation second.
- It does not mention Tables 3.2 and 3.3 or the eight properties, which are the
  chapter's main exports to chapters 4 and 6.

Refresh it in the commit that applies these rulings.

## Validation gate

- Every G / S / F / T / prose / C / X entry carries Marc's ruling: applied, declined
  or amended.
- Applied entries are in the tex. `\propmet` and `\propstandin` are redefined, and
  Tables 3.3 and 7.1 checked on the page.
- `tools/term_screen.py` shows 0 *dwell* in ch3 prose, 0 *phase* for the lifecycle
  in ch3, and 0 own-voice *MTD interval*.
- The PDF builds with 0 undefined references and no new overfull boxes. Table 3.1
  lands inside §3.2.
- A fresh cold reader who holds only chapters 1–2 and the revised chapter 3 can
  state, from the text and floats alone:
  - which of the eight properties each surveyed attacker model has, and why, from
    the cell reasons;
  - what the sample was and how it was chosen;
  - why the attacker model can change which MTD mechanism wins.
- The `scrutinise-figure` gate passes on Figure 3.2 once F2's caption lands.

## Hard constraints

- Nothing applied unratified. Marc's dictated units change only by the deletions and
  merges ratified here. Anything reworded is his.
- Guardrails: no paper is called wrong; a paper-versus-code mismatch (X4) is
  recorded both ways and disposed by Marc.
- Property numbers are never renumbered (the criterion's order, cited across the
  record).
- Registry rows 72, 81, 97, 206 and the *stage* row bind the terms. G2's two
  unregistered clusters need a ruling before N4 and T1's heading change.

## Reading list

- `docs/thesis/dissertation.tex` l.859–3771, and the rendered pages 8–16.
- [`../workflows/literature_review_conventions.md`](../workflows/literature_review_conventions.md):
  the yardstick; §(d) the failure modes, §(e) the scoring-table rules.
- `docs/sources/extractions/{kim2026,masud2025,cho2020,alshamrani2019,brown2023,zhang2023}.md`:
  the X evidence.
- `docs/sources/lit_review/1_1_cho2020toward.md` l.479 (C1) and l.698–712
  (Sec. VIII).
- The tex comment trails at l.3394–3406 (the selection-rule question) and l.3426–3440
  (Table 3.3's mark design).
