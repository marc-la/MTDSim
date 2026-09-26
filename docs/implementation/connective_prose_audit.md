---
status: durable
created: 2026-09-25
updated: 2026-09-26
topic: "The first run of the connective-prose check (connective_prose.md §e) over chapters 2–5: every chapter opener, section preamble and bridge, with the eleven-item check per unit, verdicts, and proposed revisions"
---

# Connective-prose audit, chapters 2–5 (2026-09-25/26)

**Status:** investigation record — immutable history; annotate, don't rewrite.
Three independent reviewers, one per chapter, each loaded
[`../workflows/connective_prose.md`](../workflows/connective_prose.md),
`critique_protocol.md`, `voice.md`, `academic_register.md` and
`terminology.md`, read the chapter's DRAFT STATE rulings, and reviewed the
tex read-only. Nothing here has been applied to `dissertation.tex`. The
decisions it needs, and the proposals in priority order, are in the handoff
[`../handoffs/2026-09-25_connective_prose_rulings.md`](../handoffs/2026-09-25_connective_prose_rulings.md).

**Annotation (2026-09-26).** Marc ruled R1–R4 and the chapter 2–4 proposals
were applied the same day (commit 4b97216e), with the §4.4 preamble change
narrowed to leave the 2026-09-25 "four bases" paragraph untouched. Chapter 5
was added on Marc's ask the same day. Its first critique ran against a draft
that a parallel session rewrote an hour later (commit 28cab9ca, "plain
description"), so the chapter 5 record below is the **second** critique, of
the rewritten text; it records which first-critique findings survived.
Applied from it: the six connective units and the non-held mark-costing items
(the false statements S1, S2, S3, S5, S12; S4; S6). Held for Marc: see the
rulings handoff.

**Line numbers** are those of `docs/thesis/dissertation.tex` on
`chore/ch5-setup-defence-and-prose` after commit 452008d5 (which added 29
lines ahead of chapter 1 during the review; the chapter 2 section was
reviewed before it and its numbers are 29 lower). Cite units by `\label`,
not by line.

**Annotation (main session, 2026-09-25).** Chapter 4 §U13's optional close
reads "runs the model beside the baseline attacker"; Marc ruled *built
beside* wrong for the two attackers' relation (2026-09-24, tex comment at the
ch4 opener). If that close is ever used, read "runs the model and the
baseline attacker". Chapter 3 §C11's "two MTD surveys and the APT definition
of Section 3.1.1" was checked against §3.3.1's first sentence and matches.


---

## Chapter 2 (Background): critique of the connective prose

Yardstick: `MTDSim-preambles/docs/workflows/connective_prose.md` (§a rule, §b units, §e eleven-item check). Conduct: `critique_protocol.md`. Voice: `voice.md` §c, §d, §h. Register: `academic_register.md` §b, §i. Terms: `terminology.md`.
Text: `docs/thesis/dissertation.tex`, lines 448–1055, checked against the built PDF (`dissertation.pdf`, pp. 3–10). Read only; no repo file edited.

---

### 1. Inventory

Chapter 2 has two sections. §2.1 has no subsections. §2.2 has three: 2.2.1, 2.2.2 and 2.2.3. The PDF shows every heading followed by prose, so no heading is followed only by a float. The one exception is §2.2, where Figure 2.1 breaks into the preamble mid-sentence at the page turn. That is ordinary float behaviour.

| # | Unit | Lines | Words | Binding ruling (one line) |
|---|---|---|---|---|
| U1 | Chapter opener (`ch:background`) | 469–473 | 45 | DRAFT STATE 2026-09-02: session-generated, ratify on read. Marc's **altitude ruling**: state the sections' content plainly, no "builds on two things" frame. The asymmetry sentence **stays ruled to ch1/ch3**. |
| U2 | §2.1 close (`sec:mtd-concept`, last ¶) | 523–529 | 48 | Pass 6 2026-08-27: four-paragraph shape, one paragraph per question (Marc). |
| U3 | §2.2 preamble (`sec:mtdsim`) | 582–599 | 98 | DRAFT STATE 2026-09-02: session-generated, ratify on read. **The question frame lives here at parent level** (Marc, 2026-09-02). **Table 2.2 sentence RATIFIED 2026-09-23** ("that's fine"). |
| U4 | §2.2.1 close (`subsec:network-model`, last ¶) | 737–739 | 27 | Pass 6 2026-08-27, Marc-ruled items applied. |
| U5 | §2.2.2 close (`subsec:defence-mechanisms`, last ¶) | 874–889 | 90 | Timing sentences session-drafted 2026-09-20 and 2026-09-25, accepted, ratify on read. "DO NOT RE-FLAG" the endpoint rider and the lineage-pool clause. |
| U6 | §2.2.3 close (`subsec:attacker-model`, last ¶ + placeholder) | 1017–1038 | 44 + placeholder | Pass 6 #12 and reorder, 2026-08-27: "persistence sentence closes the disruption paragraph as the contrast … Do not re-flag." Placeholder: Marc 2026-09-24, "I'll get back to it". |
| U7 | **Chapter close: MISSING** (§2.2 close and chapter close coincide) | after 1038 | 0 | None. connective_prose §f1 (whether chapters get closing bridges) is **open for Marc's ruling**. |

Verbatim current prose (comments and floats stripped):

- **U1.** "This chapter sets out the background the rest of this dissertation assumes. Section~\ref{sec:mtd-concept} defines moving target defence and its organising questions (what to move, how to move it, and when); Section~\ref{sec:mtdsim} describes MTDSim, the simulator this dissertation inherits, in which the evaluation runs."
- **U2.** "The third question, when to move, distinguishes proactive (time-triggered), reactive (event-triggered), and hybrid scheduling regimes \citep{cho2020}. When to move is the tension between cost and security: moving too often imposes overhead on legitimate users; moving too rarely leaves the attacker's reconnaissance valid for longer than it should be."
- **U3.** "MTDSim is a discrete-event simulator built to evaluate defence mechanisms singly and in combination \citep{brown2023}. Figure~\ref{fig:mtdsim-model} draws its three modules, and the subsections describe them in turn: what network is being defended (Section~\ref{subsec:network-model}), what defence mechanisms are implemented and how their deployment is orchestrated (Section~\ref{subsec:defence-mechanisms}), and what attacker the defence is evaluated against (Section~\ref{subsec:attacker-model}). The simulator is the product of four studies over one evolving codebase; Table~\ref{tab:mtdsim-lineage} lists what each work added to the codebase, and each addition is described where it is used. Table~\ref{tab:lineage-configurations} gives the configurations the studies evaluated on."
- **U4.** "The attacker never sees the whole topology. It only sees a visible subgraph, which comprises the endpoints plus all the compromised hosts and all of their neighbours."
- **U5.** "The interval between deployments is 200\,s plus a small exponentially drawn term, half a second on average, so deployments arrive close to periodically. A deployment takes time to complete, from 20\,s to 110\,s depending on the mechanism; four of the seven values are Zhang's \citep{zhang2023} and the rest are the simulator's. Two mechanisms rewriting the same layer cannot operate concurrently \citep{zhang2023}. There are no purely reactive deployment strategies in the simulator: no detection channel is encoded, so a detection-triggered strategy, such as an IDS-based scheme, is not possible."
- **U6.** "A network-layer mechanism disrupts the attacker at any state; an application-layer one only while it is scanning ports, exploiting, or brute-forcing. After a network-layer mechanism the attacker returns to scanning hosts, after an application-layer one to scanning ports \citep{brown2023}. Compromised hosts stay compromised \citep{zhang2023}." This is followed by the visible placeholder "[Placeholder --- how a disruption is modelled, owed here for Section 5.3.1: …]", which is the last thing on p. 10 of the PDF.
- **U7.** None. The chapter ends on the U6 placeholder, and the next page is `\chapter{Literature review}`.

---

### 2. Per unit

#### U1: Chapter opener. Verdict: **rework**

§e check:

1. Exists? **Y**.
2. Link carries a finding? **N.** There is no link at all. For the first chapter after the introduction, the link is to the research question (§b opener 1). \ref{sq:model} and \ref{sq:evaluate} already name this chapter's objects in their own words: "an existing MTD simulator" and "the simulator's baseline attacker".
3. Aim stated as a job? **N.** "sets out the background the rest of this dissertation assumes" is a writer act (Bunton, §a). It does not say which part of the research question the chapter serves.
4. Roles, not topics? **Y.** Both section clauses carry a presentational verb, and §2.2's clause carries its role ("in which the evaluation runs").
5. Dependency shown? **N.** The two sections are joined by a semicolon only. §2.2 classifies its mechanisms by §2.1's questions: Table 2.3's column is "*What* to move" and Table 2.4's is "*When* to move". The opener never says so.
6. No flourish? **Y.**
7. No duplication? **N.** Sentence 1 restates the heading "Background" and adds nothing.
8. Tense, person, agent? **Y.** Present tense, impersonal, presentational verbs.
9. References and terms? **Y.** Both \ref resolve, and the terms are the heading terms.
10. Scale? **N.** 45 words, below the 60–150 floor. The missing words are the link.
11. Varied? **N.** The ch3 opener has the same skeleton ("This chapter surveys …. Section 3.1 surveys …; Section 3.2 …; Section 3.3 …"), and so do all three ch3 section preambles ("This section surveys …").

Moves present: aim (weak), how. Missing: link, dependency.

Findings:
1. **(§e2, §e3)** The opener starts "This chapter …" before the reader knows why the chapter is there. Zobel p. 97 names this as the reason such openers state content out of context. The fix is a link sentence built from SQ2 and SQ3's own words (the simulator, its baseline attacker). That sentence also carries the aim.
2. **(§e7, §e11)** Sentence 1 is heading-restatement. Cutting it and opening on the link also breaks the skeleton that ch3 repeats.
3. **(§e5)** Add one clause saying that §2.2 classifies MTDSim's mechanisms by §2.1's questions. That dependency is real, and the tables already print it.

Ruling note: Marc's altitude ruling (plain content, no narrative frame) stands, and the proposal keeps to it. The DRAFT STATE comment is **stale**: it says the opener "keeps one flourish, the inherit/build opposition", but the prose now carries only "inherits". Nothing is built. The comment wants updating on ratification.

**Proposal (62 words):**
> The APT attacker model is executed inside MTDSim, the MTD simulator this dissertation inherits, and compared with the simulator's baseline attacker. This chapter describes MTDSim and the defence it models. Section~\ref{sec:mtd-concept} defines moving target defence and its organising questions (what to move, how to move it, and when); Section~\ref{sec:mtdsim} describes the simulator's modules and classifies its defence mechanisms by the same questions.

Where the words come from:
- Sentence 1 uses SQ2's "executed inside" and SQ3's "compared with the simulator's baseline attacker".
- "the MTD simulator this dissertation inherits" is the opener's own clause. The registry requires the inheritance to be established once in ch2, and this is where it happens.
- "Beside" was avoided on purpose, because Marc ruled "built beside" wrong for the two attackers' relation (ch4 comment, 2026-09-24).
- The parenthesis is the author's own, and it is not in the opening sentence.
- No new claim is made.

#### U2: §2.1 close. Verdict: **keep** (no bridge needed)

§e check: 1 is N/A (§2.1 has no subsections, so no preamble is required). 2–11: not a connective unit, and **no bridge function**. It closes the "when" paragraph on the cost–security trade-off.

Why keep: a bridge belongs only where the next unit depends on a result of this one (§b bridge 1). §2.2 does depend on §2.1's vocabulary, but that link is already carried at the head of the next unit, which is the lineage's own pattern. §2.2.2's first sentence, "MTDSim implements shuffle and diversity only; there is no redundancy", carries §2.1's nouns across. That is the content bridge §b bridge 4 asks for. Adding a bridge here would repeat it. The U1 proposal states the same dependency once, at chapter level.

#### U3: §2.2 preamble. Verdict: **tighten**

§e check:

1. Exists? **Y.**
2. Link? **N/A.** The link from §2.1 is carried at the head of §2.2.2 (see U2).
3. Aim as a job? **Y.** The identity sentence states what the simulator is for.
4. Roles, not topics? **N.** The three subsection clauses are indirect questions naming topics ("what network is being defended"). The only verb for the parts is the writer act "the subsections describe them in turn".
5. Dependency shown? **N.** One partial link exists ("what attacker the defence is evaluated against"). The network is unlinked, and the coupling appears only in Figure 2.1's caption.
6. No flourish? **N.** "what … what … what" is a run of three anaphora. voice.md §d licenses anaphora "in pairs, never runs of three". It is also colon-then-list, one of Marc's standing tells.
7. No duplication? **N.** "lists what each work added to the codebase" repeats Table 2.1's caption ("what each added to the codebase"). The question list re-walks the subsection headings and the module names Figure 2.1 already prints.
8. Tense, person, agent? **Y.**
9. References and terms? **Y.** All four \ref resolve. "How their deployment is orchestrated" skirts the registry covering term, **deployment strategy** (RATIFIED 2026-09-02). This is not a breach, but it is the obvious word to use.
10. Scale? **Y (marginal).** Four sentences and 98 words: over §b's 30–90, inside the ch2 ledger's ~120.
11. Varied? **Y.** It opens on the identity sentence, not "This section …".

Moves present: shared frame (identity sentence), how (the question list), and two float pointers.

Findings:
1. **(§e6, §e4)** The interrogative list carries the right content in the wrong form. Its form triggers two of Marc's tells: the run of three and the colon-list. Its clauses name topics, not operations.
2. **(§e5)** One relative clause each can carry the dependency the later chapters use: deployment strategies schedule the mechanisms, and the baseline attacker is what they are evaluated against. The figure keeps the couplings, and the preamble points at it once.
3. **(§e7)** Deleting "to the codebase" after "added" is a T1 cut. The caption carries it.

**Ruling overturned, named:** Marc's 2026-09-02 ruling placed "the question-frame (what / implemented+orchestrated / evaluated-against)" here. The proposal keeps its **placement and content** (network; mechanisms and how they are deployed; the attacker evaluated against). It overturns only its **interrogative form**, on merit. The form breaks voice.md §d's pairs-only rule for anaphora and his later colon-list ruling, and it names topics where §a wants operations. The Table 2.2 sentence (ratified 2026-09-23) is kept verbatim.

**Proposal (90 words):**
> MTDSim is a discrete-event simulator built to evaluate defence mechanisms singly and in combination \citep{brown2023}. Figure~\ref{fig:mtdsim-model} draws its three modules and the couplings between them. Section~\ref{subsec:network-model} describes the network, Section~\ref{subsec:defence-mechanisms} the defence mechanisms and the deployment strategies that schedule them, and Section~\ref{subsec:attacker-model} the baseline attacker they are evaluated against. The simulator is the product of four studies over one evolving codebase; Table~\ref{tab:mtdsim-lineage} lists what each work added, and each addition is described where it is used. Table~\ref{tab:lineage-configurations} gives the configurations the studies evaluated on.

#### U4: §2.2.1 close. Verdict: **keep**

§e check: 1–11 N/A as a formal unit. It has **bridge function by content**, not by connective.

Why keep: this closing paragraph fixes *visible subgraph*. §2.2.3 then picks the term up with a back-reference: "The knowledge the attacker holds is the visible subgraph (Section 2.2.1)". That is the old-information noun carried across a seam, which is exactly what §b bridge 4 prescribes. No connective sentence is needed. "It" in sentence 2 has an immediate referent ("The attacker").

#### U5: §2.2.2 close. Verdict: **tighten** (one T1 edit)

§e check: N/A as a formal unit. The last sentence does backward connective work: it closes the reactive branch of §2.1's when-question, so §2.1's triad is fully accounted for.

Findings:
1. **(voice §h; Marc's "such as" tail tell; academic_register §i5)** "such as an IDS-based scheme" is an example tail, and it introduces *IDS* unexpanded, used once, which is a one-use acronym. Deleting it loses nothing: "detection-triggered" is the claim.

**T1 edit:**
`…so a detection-triggered strategy, such as an IDS-based scheme, is not possible.` → `…so a detection-triggered strategy is not possible.`

#### U6: §2.2.3 close. Verdict: **keep** (the prose); the unit it should hand to is U7

§e check: N/A as a formal unit. There is no bridge function, and none is expected mid-disruption.

Why keep: Marc ruled the reset-versus-kept contrast as the paragraph's closer ("Do not re-flag"). It works: the short verdict sentence lands after the long rule.

One seam finding for the placeholder (item iv, which already books it) under **§e9**. §2.2.3 says *network-layer / application-layer*, while §2.2.2's Table 2.3 and Figure 2.3 say *host layer / service layer / credentials*. The old-information noun changes across the §2.2.2 → §2.2.3 seam. The placeholder's own vocabulary fix settles this. It is not re-drafted here.

#### U7: Chapter close. Verdict: **missing**

§e check: 1 **N** (it does not exist). 2–11 N/A.

Why it is missing, not optional: §f1 leaves chapter closes to Marc. Option (b) is "closes only where the next chapter depends on a result", and it applies here. §3.3.2 scores "MTDSim's attacker model … the baseline attacker of Section 2.2.3" (l. ~3723). That is a direct dependency on this chapter's last subsection. The ch3 opener does not carry the link either: it links to ch1's sub-questions only. Right now a reader goes from a bracketed placeholder about disruption costs straight into "This chapter surveys the literature on evaluating MTD against APT attackers", and nothing says why.

Constraints the proposal respects:
- **no gap talk in ch2** (ch2 README, "Deliberately absent");
- **the asymmetry sentence stays ruled to ch1/ch3** (U1 DRAFT STATE). A rich-defence/scripted-attacker contrast was therefore withdrawn (see §5).

**Proposal (21 words; placed after the drafted disruption paragraph):**
> Chapter~\ref{ch:litreview} scores the scripted baseline attacker and the attacker models of recent MTD evaluations against the properties of a sophisticated attacker.

What the words do:
- "Scripted" carries this chapter's established fact (l. 936).
- "scores" is ch3's own verb (the §3.3 preamble).
- "properties of a sophisticated attacker" is the §3.3.1 heading term.

If Marc rules §f1 option (c) instead, this sentence's job moves to the ch3 opener's link. That unit is out of scope here.

---

### 3. Chapter view

**The chain, read alone.** Opener → §2.2 preamble → (nothing). A reader of only these learns that the chapter defines MTD and describes MTDSim, and that MTDSim has three modules and a four-study lineage. They do **not** learn:
- why the chapter follows the introduction. The research question's own words ("existing MTD simulator", "the simulator's baseline attacker") are never used;
- that §2.2 depends on §2.1 (the same three questions sort the mechanisms);
- what the chapter hands to chapter 3.

The real dependencies are all present in the bodies:
- §2.2.2's first sentence picks up §2.1's labels.
- §2.2.3 back-references §2.2.1's visible subgraph.
- Tables 2.3 and 2.4 are headed *What* and *When*.

The connective layer simply does not say any of them. With the three proposals, the chain reads: link to SQ2/SQ3 → §2.1 gives the questions and §2.2 sorts the simulator by them → the three modules and what couples them → the scripted baseline attacker goes to ch3 to be scored.

**Stale references.** None. Every \ref in U1 and U3 resolves (checked in the PDF) and describes its target. Two stale **comments**, not prose:
- U1's DRAFT STATE claims an inherit/build opposition the text no longer has.
- l. 491–492 says to dedupe the MTD expansion "when ch1 is drafted". Ch1 is now drafted: MTD is expanded at l. 219 (ch1 P2) and again at l. 496 (§2.1 S1). That duplication is live.

**Duplication with figures and ch1.**
- U3's Table 2.1 sentence repeats that table's caption (a T1 cut in the proposal).
- The current question list re-walks Figure 2.1's module names. The proposal points at the figure once and lets the caption keep the couplings.
- Ch1 duplication in bodies adjacent to the connective layer, flagged only:
  - the MTD expansion (above);
  - §2.2.3's first sentence, "is what this dissertation terms the baseline attacker". It re-names what ch1 P5 already named by apposition ("MTDSim's original scripted attacker, the baseline attacker"), a naming sentence of the kind the E2 ruling removed elsewhere.
- The ch2 README and the §2.2.3 unit comment (l. 895–896) still plan "one forward-pointing clause" to the metric suite. It is not in the text, and ch1 P5 already points at §4.5. The plan looks retired; Marc's call.

**Handover to ch3.**
- Ch2 ends on a visible placeholder, and ch3 opens on ch1's sub-questions. No sentence on either side of the break names what ch3 takes from ch2.
- A comment in ch3 (l. ~1990) records that "the dropped dispatch sentence was ch3's only statement of why the network model is not surveyed here --- **the carrier is now ch2's preamble**." Ch2's preamble does not carry it. Only the opener's "the simulator this dissertation inherits" implies it. That is a **T3 content gap** (a claim about what is fixed and not surveyed), so it is named here, not drafted. Marc decides whether ch2 or ch3 states it.
- Openers side by side (§e11): ch2 and ch3 share the "This chapter + verb; Section X + verb" skeleton. Ch4 opens on the model and ch5 is a placeholder. The U1 proposal opens on the link, which ends the repeat.

---

### 4. Priority (three moves)

1. **Give the opener its link (U1).** Open on SQ2 and SQ3's own words: the APT attacker model is executed inside the simulator this dissertation inherits and compared with its baseline attacker. Cut the heading-restating first sentence. This single change fixes §e2, e3, e7, e10 and e11.
2. **Close the chapter, or rule §f1 (U7).** §3.3.2 scores the baseline attacker described in §2.2.3, so option (b) applies. The one-sentence proposal hands it over without gap talk. With it, settle where the "network model and defence mechanisms are not surveyed because they are inherited" statement lives. Ch3's comment believes ch2 carries it, and ch2 does not.
3. **Turn the §2.2 preamble's three-"what" question list into a declarative walk (U3).** Keep the list's content and its 2026-09-02 placement. Carry the two dependencies later chapters use: deployment strategies schedule the mechanisms, and the baseline attacker is what they are evaluated against. Use the registry term *deployment strategy*.

---

### 5. Tell audit

Withdrawn from my own drafts before writing them down:
- **U1:** a version with "beside the simulator's baseline attacker". Marc ruled "built beside" wrong for the two attackers' relation on 2026-09-24.
- **U1:** a version whose second sentence re-said "describes MTDSim" from the third (repetition).
- **U3:** a version keeping the colon before the subsection list.
- **U7:** a close contrasting the simulator's range of defences with its one scripted attacker. That is the asymmetry sentence ruled to ch1/ch3, and it risked a not-X-but-Y.
- **U7:** a "beside" interpolation, replaced by "and".

Retained knowingly:
- the three-subsection walk in U3, which is structural, not a rhetorical triplet;
- U1 sentence 1's compound predicate ("is executed … and compared"), built from SQ2 and SQ3's own verbs.

Otherwise, tier audit: clean.

---

## Chapter 3 (Literature review): critique of the connective prose

Read-only review. Yardstick: `MTDSim-preambles/docs/workflows/connective_prose.md` §e (items 1–11). Conduct: `critique_protocol.md`. Voice: `voice.md` §c/§d/§h. Register: `academic_register.md` §b and §i. Terms: `terminology.md`.

Line numbers are those of `docs/thesis/dissertation.tex` as of commit 452008d5 (2026-09-25 22:33). A parallel commit moved chapter 3 down by 29 lines while this review ran. I diffed the chapter 3 prose (comments stripped) before and after that commit, and it is identical. Chapter 3 runs from l.1086 to l.3945.

How to read the checks. In the §e rows, *n/a* means the item does not apply to that kind of unit (items 2 and 3 are opener and preamble moves) and counts as no finding. Word counts leave out `\cite` keys. They count `Section~\ref{}` as two words and an SQ tag as one.

---

### 1. Inventory

| ID | Unit | Lines | Words | Binding ruling (one line) |
|---|---|---|---|---|
| C1 | Chapter opener | 1193–1201 | 60 | Recast 2026-09-09 (Marc): frame it as MTD against APT attackers keyed to the SQs; "brought to the ch2 preamble's register (two sentences, plain, by pointer)"; "two literatures", the selection rule and the coverage claim are all cut. Ratify on read. |
| C2 | §3.1 preamble (`sec:apt-survey`) | 1228–1234 | 61 | Ruled 2026-09-04: "surveys" (not asks/looks at), "machine-usable", "current limitations"; no SQ keying; pass 6 made no proposals. "Do not re-flag." |
| C3 | §3.1.1 close (`subsec:apt`) | 1333–1391 | — | Pass 4 KEEP: the close "pays off" the lifecycle's "may forgo exfiltration". |
| C4 | §3.1.2 close (`subsec:attack`) | 1487–1490 | 30 | [3b] open: the joint "because it captures" was chosen by a session, "ratify or re-dictate". |
| C5 | §3.1.3 close = §3.1 bridge (`subsec:profiling`) | 1962–1971 | 69 | Exit rework ruled 2026-09-04 ("looks good"): the opener "The curated record supplies order and dependency, not tempo:" is session wording that Marc ratified. |
| C6 | §3.2 preamble (`sec:mtd-evaluation-survey`) | 2038–2043 | 43 | 2026-09-07: S1 is Marc's dictation ("looks at" became "surveys"); S2 was assembled by a session. "Each step carries assumptions of its own" was CUT as too strong. No citation in a signpost. |
| C7 | §3.2.1 close | 2241–2242 | 21 | "DO NOT RE-FLAG: the three unit-closers on attacker assumptions (the strand's spine)" (pass 6, 2026-09-07). |
| C8 | §3.2.2 close | 2439–2441 | 20 | The same spine ruling. The hong2018 scope is already flagged at the site. |
| C9 | §3.2.3 close | 2997–2999 | 20 | The same spine ruling. "the 'trade-off' echo stays". |
| C10 | §3.2 strand closer (unnumbered) | 3092–3097 | 27 | C1 and C2 approved 2026-09-07: "hitting the frontier" deleted, "where the recent work sits" stays. TECHNICAL-CLAIM FLAG: the old hinge into §3.3 (Tay's training-attacker clause) left with the superseded sentence. |
| C11 | §3.3 preamble (`sec:mtd-attacker-models`) | 3281–3287 | 49 | Recast 2026-09-08 to the sibling pattern of §3.1 and §3.2 ("one sentence of purpose, one of parts by pointer"). Session-drafted, ratify on read. The 2026-09-05 ruling that governs it: "the diagnosis stated ONCE, in the criterion". |
| C12 | §3.3.1 close | 3379–3381 | 19 | The folded synthesis flag (2026-09-07); the exclusion slot was dropped by ruling. |
| C13 | §3.3.2 opener pointer and close | 3610–3615; 3803–3824 | 48 | P1 was re-dictated 2026-09-08 and the "favourable pick" clause ruled out. Pass-4 M1 [VERIFY] on the keyword search is still open (body). |
| C14 | §3.3.3 back-link paragraph | 3918–3923 | 47 | Dictated 2026-09-08 by Marc ("scissors clause"). "weakest link" KEPT by choice (a deliberate symmetry with ch6). |
| C15 | §3.3.3 "means" paragraph, frame sentences | 3925, 3936–3939 | 51 | Pass 5 class C (C19, the surveys tail) REJECTED: "do not re-flag". |
| C16 | Chapter close (last sentence of §3.3.3) | 3941–3943 | 21 | Marc re-ruled the forward pointer as the closer. Pass 5 C20 (the hand-off clause "does not formally define") REJECTED: keep. |
| — | Missing units | — | — | **None.** Every section with subsections has a preamble. No heading is followed only by a float. The chapter has a close. |

### Verbatim current text (comments and floats stripped)

**C1.** This chapter surveys the literature on evaluating MTD against APT attackers, along the three sub-questions of Chapter~\ref{ch:intro}. Section~\ref{sec:apt-survey} surveys how APT attacker behaviour is recovered (\ref{sq:capture}); Section~\ref{sec:mtd-evaluation-survey} how the field evaluates a defence mechanism (\ref{sq:evaluate}); Section~\ref{sec:mtd-attacker-models} how the attacker is modelled in those evaluations (\ref{sq:model}), last because it closes on the gap that motivates Chapter~\ref{ch:attacker-model}.

**C2.** This section surveys the literature for whether a machine-usable specification of an APT campaign can be produced from it, and which elements such a specification still lacks. Section~\ref{subsec:apt} defines the APT attacker and its lifecycle; Section~\ref{subsec:attack} the knowledge base its behaviour is recorded in; Section~\ref{subsec:profiling} the methods that reconstruct that behaviour as structured representations, and their current limitations.

**C3** (last sentence of the last paragraph). Pre-positioning is NIST's third objective class \citep{nist2011sp80039}.

**C4.** Behaviour at the technique-and-tactic level is stable enough to model an attacker against because it captures the persistent operational habits of APT attackers, distilled into the matrix from observed operations.

**C5.** The curated record supplies order and dependency, not tempo: the Attack Flow schema defines optional per-action start and end timestamps, but the public corpus leaves them all but empty, because breach reports rarely contain machine-usable timestamps; ATT\&CK campaign records carry only month-granularity first- and last-seen dates \citep{ctid2025attackflow, mitre2026attackkb}. The apparatus for reconstructing behaviour from CTI, automated and manual alike, sits within the threat-intelligence and incident-response literature, not within MTD evaluation.

**C6.** This section surveys how the field evaluates a defence mechanism and the steps involved in such an evaluation. A defence mechanism is designed under a defence modelling approach (Section~\ref{subsec:defence-modelling-approaches}), instrumented with metrics (Section~\ref{subsec:mtd-metrics}), and evaluated under an evaluation method (Section~\ref{subsec:evaluation-methods}).

**C7.** If attacker models have no agency and are based on unrealistic assumptions, then the logic of the defence mechanisms is limited.

**C8.** The effectiveness metrics are dependent on how the attacker was implemented, and therefore on the assumptions that underlie it \citep{hong2018}.

**C9.** However, as a trade-off, parameters that are not captured in a simulator \citep{cho2020} are not accounted for in defence mechanism logic.

**C10.** MTD evaluation is mostly one defence against a single or small set of attacks \citep[Sec.~V-D]{cho2020}; evaluating multiple defence mechanisms together is where the recent work sits \citep{alavizadeh2022, brown2023, masud2025, tay2024, kim2026}.

**C11.** This section surveys the attacker model that MTD evaluation is scored over, which both MTD surveys name as a primary limitation of the field \citep{cho2020, jalowski2026}. Section~\ref{subsec:attacker-criterion} derives the properties of a sophisticated attacker from the literature; Section~\ref{subsec:recent-threat-models} scores recent evaluations against them; Section~\ref{subsec:research-gap} states the gap.

**C12.** The selection of the eight and the merge of the definition onto the enumeration are this dissertation's own synthesis.

**C13** (P1). Two works from 2025--2026 were selected using a keyword search for MITRE ATT\&CK, as the works most likely to be grounded in attacker modelling. The simulator lineage this dissertation extends \citep{…} is scored in the same way. Table~\ref{tab:attacker-cross-section} scores the three against the eight properties of Section~\ref{subsec:attacker-criterion}.

**C14.** The assumptions about the attacker are baked into the logic of the defender (Section~\ref{subsec:mtd-metrics}). Over the effectiveness metrics the attacker is the weakest link: with a weak attacker model the defence mechanisms cannot be evaluated, because the metrics are intertwined and computed over the attacker model.

**C15** (frame sentences). The means to close the gap already exist in MTD-adjacent literatures. […] The apparatus is in place; it has not been brought to the MTD evaluations surveyed here. The claim is about MTD evaluation as sampled, not about the field's attacker models at large; the field-level diagnosis rests on the two surveys.

**C16.** The literature does not formally define its attacker models \citep[p.~8]{jalowski2026}; this research gap motivates the attacker model defined in Chapter~\ref{ch:attacker-model}.

---

### 2. Per unit

#### C1: Chapter opener. **tighten**

| # | | Reason for N |
|---|---|---|
| 1 | Y | |
| 2 | Y | The link is to the research question's sub-questions. That is licensed here, because ch2 describes existing things and establishes no finding for ch3 to carry. |
| 3 | Y | Keyed to SQ1–SQ3. The job (the gap that motivates ch4) arrives only in the final clause. |
| 4 | **N** | Every section clause is a bare topic ("surveys how APT attacker behaviour is recovered … how the field evaluates … how the attacker is modelled"). Only the tail of the last clause names an operation. |
| 5 | Y | "last because it closes on the gap that motivates Chapter 4". |
| 6 | Y | |
| 7 | Y | |
| 8 | Y | Present tense, impersonal, "surveys" is presentational. |
| 9 | Y | All refs resolve. "recovered" is the registry verb for SQ1. |
| 10 | Y | One paragraph, 60 words. |
| 11 | **N** | Same skeleton as the ch2 opener ("This chapter … Section X …; Section Y …"). It is also the first of four "This chapter/section surveys" openers in the chapter (C1, C2, C6, C11). |

**Moves:** link (to the SQs), aim, how. The final clause does a bridge's job into ch4.

**Verdict: tighten.** The moves are right and in order, and the reason the order departs from SQ order is stated. What fails is §a: the "how" is three topics under one verb, so the reader learns what each section is *about* but not what it contributes.

**Findings**
1. §e4, the laundry-list half of §a. Give §3.1 and §3.2 the object they deliver (what the recovered record lacks; where the attacker model enters an evaluation) and give §3.3 its actual operation ("scores"). All three are already on the page in the sections' own closers (C5, C8, C13).
2. §e11. The same skeleton as ch2. This was a deliberate choice (the 2026-09-09 ruling asked for "the ch2 preamble's register"), so I flag it and do not overturn it at chapter level. The variation is better bought in the section preambles (see C6).

**Proposed revision** (69 words; S1 unchanged; S2 keeps Marc's semicolon shape and his "last because" dependency)
> This chapter surveys the literature on evaluating MTD against APT attackers, along the three sub-questions of Chapter~\ref{ch:intro}. Section~\ref{sec:apt-survey} surveys how APT attacker behaviour is recovered from CTI (\ref{sq:capture}); Section~\ref{sec:mtd-evaluation-survey} how the field evaluates a defence mechanism, and where the attacker model enters that evaluation (\ref{sq:evaluate}); Section~\ref{sec:mtd-attacker-models} scores the attacker models of recent evaluations (\ref{sq:model}), last because that scoring states the gap that motivates Chapter~\ref{ch:attacker-model}.

Ceiling note: "where the attacker model enters that evaluation" is narrower than the cut "Each step carries assumptions of its own". It poses a question and asserts nothing about every step. 3.2.1 P2 and C8 answer it.

---

#### C2: §3.1 preamble. **tighten**

| # | | Reason for N |
|---|---|---|
| 1 | Y | |
| 2 | n/a | |
| 3 | Y | Stated as the question the section answers. C5 pays it off. |
| 4 | Y | "defines", "reconstruct" (the second clause is gapped under "defines"). |
| 5 | Y | "its behaviour" → "that behaviour" chains the three subsections. |
| 6 | Y | |
| 7 | Y | |
| 8 | Y | |
| 9 | **N** | §3.1.3's heading term *attack profiling* never appears. "the methods that reconstruct…" paraphrases it (§c5; register §i10). |
| 10 | Y | Two sentences, 61 words. |
| 11 | Y | Its "This section surveys" is ruled, and C6's revision breaks the run. |

**Moves:** aim (as a question), how with dependency, a shared thread (the specification and its missing elements).

**Verdict: tighten.** This is the chapter's best preamble. It states a question, carries one noun through all three subsections, and the section closes on the answer ("order and dependency, not tempo"). The only fault is the missing heading term.

**Findings**
1. §e9. Name *attack profiling* where the preview reaches §3.1.3.

**Proposed revision** (62 words; one word added. Marc's ruled words "surveys", "machine-usable" and "current limitations" are untouched.)
> This section surveys the literature for whether a machine-usable specification of an APT campaign can be produced from it, and which elements such a specification still lacks. Section~\ref{subsec:apt} defines the APT attacker and its lifecycle; Section~\ref{subsec:attack} the knowledge base its behaviour is recorded in; Section~\ref{subsec:profiling} the attack-profiling methods that reconstruct that behaviour as structured representations, and their current limitations.

---

#### C3: §3.1.1 close. **keep** (no bridge owed)

Checks: 1 Y; the rest n/a or Y.

§3.1.2 depends on no *result* of §3.1.1. The dependency (the knowledge base "its behaviour" is recorded in) is already carried by C2 (§b bridge 1). The last paragraph works as the subsection's payoff: pre-positioning closes the lifecycle's "may forgo exfiltration". That is body work, and the pass-4 KEEP stands. No proposal.

---

#### C4: §3.1.2 close. **keep**

| # | | |
|---|---|---|
| 1, 4–11 | Y | Items 2 and 3 are n/a. |

**Moves:** a bridge (what is established, and the level §3.1.3 works at).

**Verdict: keep.** In one sentence it states what the subsection establishes: technique-and-tactic behaviour is modellable. It hands that level to §3.1.3, whose first sentence picks up "ATT&CK's tactics, techniques, and procedures". This is §b bridge 4 (built from content) at its most economical.

Outside this check (T3, body): the claim "stable enough to model an attacker against" has had no citation since the Sadlek leg was cut (the tex's own TECHNICAL-CLAIM FLAG), and the [3b] on "because it captures" is still open. Both are Marc's to close. No proposal.

---

#### C5: §3.1 close (bridge). **tighten**

| # | | Reason for N |
|---|---|---|
| 1 | Y | |
| 2–3 | n/a | |
| 4 | Y | |
| 5 | Y | "not within MTD evaluation" hands over to §3.2's heading noun. "The apparatus" is carried to C15. |
| 6 | **N** | Two X-not-Y constructions in consecutive sentences ("order and dependency, not tempo"; "…literature, not within MTD evaluation"). Voice §d: the device "dulls with overuse". Marc hears the form as a tell. |
| 7 | Y | |
| 8 | Y | |
| 9 | Y | |
| 10 | **N** | The bridge claim is buried. It sits at the head of a 45-word sentence carrying four propositions behind a colon (critique §e5). A bridge should be one or two sentences whose claim a reader can find. |
| 11 | Y | |

**Moves:** a bridge. It states what is established (the missing element: tempo) and where the apparatus lives, and it hooks §3.2 and §3.3.3.

**Verdict: tighten.** The function is exactly right: it answers C2's "which elements such a specification still lacks". Two edits are needed.

**Findings**
1. §e6. The second X-not-Y is not ruled. The ruled one is the first ("not tempo", 2026-09-04), and it stays. Rewrite the second as a plain locative.
2. §e10. Split at the ruled colon (a T1 split at a marked point). The verdict then stands as its own short sentence (voice §d, "verdict sentences are short") and the evidence follows.

**Proposed revision** (68 words; wording is Marc's except "outside")
> The curated record supplies order and dependency, not tempo. The Attack Flow schema defines optional per-action start and end timestamps, but the public corpus leaves them all but empty, because breach reports rarely contain machine-usable timestamps; ATT\&CK campaign records carry only month-granularity first- and last-seen dates \citep{ctid2025attackflow, mitre2026attackkb}. The apparatus for reconstructing behaviour from CTI, automated and manual alike, sits within the threat-intelligence and incident-response literature, outside MTD evaluation.

---

#### C6: §3.2 preamble. **tighten**

| # | | Reason for N |
|---|---|---|
| 1 | Y | |
| 2 | n/a | |
| 3 | **N** | "surveys how the field evaluates a defence mechanism" is a topic. What the section establishes for SQ3 goes unsaid. Ruled: the S3 synthesis was cut as too strong, so this stays a flag. C11's revision carries the section's result forward instead. |
| 4 | Y | "designed … instrumented … evaluated". |
| 5 | Y | A sequence whose parts *are* the subsections: the shared-frame pattern of §b preamble 3. |
| 6 | Y | |
| 7 | **N** | S1's "and the steps involved in such an evaluation" previews S2, and "surveys how the field evaluates a defence mechanism" repeats C1 verbatim. |
| 8 | Y | |
| 9 | Y | All three nouns are ratified registry terms. |
| 10 | Y | |
| 11 | **N** | The third "This section surveys" opener in the chapter, and the second in a row at section level. Voice §d licenses the two-beat but never a run of three. |

**Moves:** aim (topic), how, and the shared frame (the three-step anatomy).

**Verdict: tighten.** S2 is the preamble. It carries a frame whose parts are the subsections, which is the lineage's best pattern. S1 adds only duplication, and it is the unit that makes the chapter's openers identical.

**Findings**
1. §e7. Cut S1's clause that previews S2. Its "surveys how the field evaluates a defence mechanism" is C1's phrase for §3.2.
2. §e11. Open on the frame. Voice §c2's enumerate-then-walk gives a one-clause opener with no brackets, which also avoids Marc's three-clause-opener tell.

**Proposed revision** (31 words; S2 is the ratified-on-read text with its subject renamed)
> Evaluating a defence mechanism involves three steps. The mechanism is designed under a defence modelling approach (Section~\ref{subsec:defence-modelling-approaches}), instrumented with metrics (Section~\ref{subsec:mtd-metrics}), and evaluated under an evaluation method (Section~\ref{subsec:evaluation-methods}).

"involves … steps" is Marc's own dictated phrase ("the steps involved in such evaluation"). "three" is the announced count that S2 walks. This overturns nothing: the 2026-09-07 rulings (no citation, no synthesis, the network and attacker models not named) all hold.

---

#### C7: §3.2.1 close. **keep**

Checks: 1, 4–11 Y (items 2 and 3 n/a). Ruled as part of the strand's spine, and it does not plainly break the guidance. In Marc's conditional, it states what 3.2.1 P2 walked approach by approach. C14 later points back to it ("the logic of the defender"). The pointer in C14 is currently mis-aimed (see C14). No proposal.

#### C8: §3.2.2 close. **keep**

Checks: 1, 4–11 Y. This is the sentence §3.3 is built on: the effectiveness metrics depend on how the attacker was implemented. It ends §3.2.2 on the noun ("attacker") that §3.3's heading takes up. The hong2018 scope is flagged at the site (body). No proposal.

#### C9: §3.2.3 close. **keep**

Checks: 1, 4–11 Y. Ruled. The hinge clause two sentences earlier ("above all in modelling attack behaviours") makes "parameters that are not captured in a simulator" read as attacker-facing, so §3.2.3 ends pointing the right way. No proposal.

#### C10: §3.2 strand closer. **keep** (as content; no bridge owed here)

| # | | |
|---|---|---|
| 1, 4, 6–11 | Y | |
| 5 | Y | See below. |

**Verdict: keep.** It is not a bridge, and it need not be one. §b bridge 1 asks for a close only where the next unit depends on a result, and here the head of §3.3 can carry that link (§f option c). What it does well: it introduces, as "the recent work", the evaluations whose attacker models §3.3.2 scores (brown2023, masud2025, kim2026, and tay2024 in the lineage row). The reader meets Table 3.3's rows here first.

Condition: since the Tay sentence was superseded, the hand-off into §3.3 rests on C11's "scored over" alone. C11's revision makes that link explicit. Without it, the chain jumps from "multiple defence mechanisms together" to the attacker with no stated reason. The one-home overlap with 3.3.1 P1 (Cho V-D) is already logged in the tex as a body item. No proposal.

---

#### C11: §3.3 preamble. **tighten**

| # | | Reason for N |
|---|---|---|
| 1 | Y | |
| 2 | n/a | |
| 3 | Y | "states the gap" shows the job. |
| 4 | Y | derives / scores / states. |
| 5 | **N** (partial) | The parts depend on each other ("against them"). But the preamble names neither of the two dependencies the section actually has. One is on §3.2's result: "scored over" carries no pointer. The other is on §3.1.1's APT definition, which 3.3.1 uses: "from the literature" hides it. |
| 6 | **N** | A tacked-on trailing relative clause ("which both MTD surveys name…"): one of Marc's tells. |
| 7 | **N** | The clause restates the diagnosis that 3.3.1 P1 gives in full, with locators. That breaks the 2026-09-05 ruling "the diagnosis stated ONCE, in the criterion". It also repeats ch1 P3 ("attacker models far simpler than an APT \citep{cho2020, jalowski2026}"). Separately, it puts a cited claim in a signpost, against the rule ruled for C6 ("a signpost carries no cited claim — the 3.1 rule"). |
| 8 | Y | |
| 9 | Y | |
| 10 | Y | |
| 11 | Y | Once C6 changes, this forms the licensed pair with C2. |

**Moves:** aim, and how with dependency. The link is implicit.

**Verdict: tighten.** The skeleton is right: derive, then score, then state, each a real operation. The unit should spend its link on the finding §3.2 hands it, not on a diagnosis the next subsection owns.

**Findings**
1. §e7 and the 2026-09-05 ruling. Cut the survey clause. 3.3.1 P1 carries it.
2. §e5 / §b bridge 4. Make "scored over" a pointed link to 3.2.2's result, in 3.3.3's own words ("computed over the attacker model"). Name the APT definition of §3.1.1 as a source of the properties. This is the chapter's only strand-1 → strand-3 dependency, and the chain currently never shows it.
3. §e4 (minor). "states the gap" becomes "draws the research gap from that scoring", so the last part carries its dependency on the one before.

**Proposed revision** (52 words)
> This section surveys the attacker model that the effectiveness metrics of Section~\ref{subsec:mtd-metrics} are computed over. Section~\ref{subsec:attacker-criterion} derives the properties of a sophisticated attacker from two MTD surveys and the APT definition of Section~\ref{subsec:apt}; Section~\ref{subsec:recent-threat-models} scores recent evaluations against them; Section~\ref{subsec:research-gap} draws the research gap from that scoring.

"effectiveness metrics", not "metrics": this keeps Marc's 2026-09-07 ruling that "every metric" is false from Table 3.1 itself. "two MTD surveys" is indefinite on purpose, because the cited clause that introduced them is gone. 3.3.1 names them in its next sentence.

---

#### C12: §3.3.1 close. **keep** (no bridge owed)

Checks: 1, 4–11 Y. This is the ownership flag (voice §c5 and §c10), not a bridge. None is needed, because C13's pointer sentence carries "the eight properties of Section 3.3.1" into §3.3.2. No proposal.

#### C13: §3.3.2 opening pointer and close. **keep**

Checks: 1, 4–11 Y. The pointer sentence names the operation ("scores") and what it depends on ("the eight properties of Section 3.3.1"). The Table 3.3 caption says the same, but a caption must stand alone, so this is not duplication. The subsection closes on the Kim paragraph with no bridge, which is right: §3.3.3 opens by reading the table across. The pass-4 M1 [VERIFY] on "a keyword search" is a body and evidence matter, outside this check. No proposal.

---

#### C14: §3.3.3 back-link paragraph. **tighten**

| # | | Reason for N |
|---|---|---|
| 1, 4, 5, 8, 10, 11 | Y | |
| 6 | **N** (flag only) | Metaphor carries the claim (§a): "baked into", "weakest link". Both are Marc's dictation, and "weakest link" is ruled (the ch6 symmetry). I flag them and do not rewrite. |
| 7 | Y | Its restatement of C8 is ruled (pass 5 C15: "S6's because-clause keeps it here"). |
| 9 | **N** | `\ref{subsec:mtd-metrics}` hangs on "the logic of the defender". That claim is §3.2.1's close (C7, "the logic of the defence mechanisms is limited"), not §3.2.2's. The metrics claim that §3.2.2 does carry is the next sentence, which has no pointer. The tex comment shows how this happened: the stale "3.2 closer" pointer was re-aimed at 3.2.2 for the scored-over claim, then parked on the wrong sentence. "the defender" also differs from §3.2.1's noun, *defence mechanisms*. |

**Moves:** a back-link. It joins strand 2 to the gap.

**Verdict: tighten.** This paragraph is where the chapter's two literatures meet. Its pointer sends the reader to the wrong subsection, which is a sloppiness signal an examiner will act on (register §i10).

**Findings**
1. §c4 and §e9. Re-aim the first `\ref` at §3.2.1 and put the §3.2.2 pointer on the metrics sentence.
2. §c5. Use §3.2.1's own noun: "the logic of the defence mechanisms".

**Proposed revision** (50 words; Marc's wording otherwise untouched)
> The assumptions about the attacker are baked into the logic of the defence mechanisms (Section~\ref{subsec:defence-modelling-approaches}). Over the effectiveness metrics the attacker is the weakest link (Section~\ref{subsec:mtd-metrics}): with a weak attacker model the defence mechanisms cannot be evaluated, because the metrics are intertwined and computed over the attacker model.

---

#### C15: §3.3.3 "means" frame. **keep**

Checks: 1, 4–11 Y. "The apparatus is in place; it has not been brought to the MTD evaluations surveyed here" carries §3.1's closing noun ("The apparatus for reconstructing behaviour from CTI") across two sections. It is the chapter's one explicit bridge between strands, built from content rather than a connective (§b bridge 4). "MTD-adjacent literatures" is rightly wider than C5's "threat-intelligence and incident-response literature", because Bland and Outkin are neither. The negative-scope sentence is ruled (C19). No proposal.

---

#### C16: Chapter close (hand-over to ch4). **rework**

| # | | Reason for N |
|---|---|---|
| 1 | Y | |
| 4 | Y | |
| 5 | Y | "motivates … Chapter 4". |
| 6 | Y | |
| 7 | **N** | Double handshake. Ch4's first sentence says it again ("the model that the research gap motivated"). |
| 8 | Y | |
| 9 | **N** | "the attacker model defined in Chapter 4" is not the registry and ch4-title term, *APT attacker model* (a ratified row). "this research gap" has as its immediate referent the Jalowski clause, which is new cited content. It is not the gap §3.3.3 derived (P1: properties 1, 2 and 4; "the performance of MTD against an attacker with a foothold … remains unmeasured"). |
| 10 | Y | |
| 11 | Y | |

**Moves:** a bridge, forward only.

**Verdict: rework.** The text is short, but the defect is in the argument. §b bridge 2 asks the close to state what is *now established*. Instead, this close introduces a fresh citation and names *it* as the gap. A reader of the connective chain never learns what the gap is, and ch4 is handed "does not formally define" in place of the unmeasured performance against a persistent, objective-driven, adaptive attacker that the chapter derived.

**Findings**
1. §b bridge 2 and §e9 (referent). Keep the ruled Jalowski clause (C20 rejected; no overturn). Replace the anaphor with the derived gap in P1's own words, so the close hands over both halves.
2. §e9 (term). Use *APT attacker model*.
3. §e7 (cross-chapter). One side of the ch3/ch4 handshake should go. I recommend this sentence keep the forward link (Marc re-ruled it as the closer). Ch4's first sentence would then carry a finding-link instead, the properties it aims at, and say *properties*, not *axes* (the registry's PROPOSED row, raised by the §3.3.1 rebuild). That is ch4's unit; it is noted here only for the hand-over.

**Proposed revision** (33 words)
> The literature does not formally define its attacker models \citep[p.~8]{jalowski2026}; that absence and the unmeasured performance of MTD against an attacker with a foothold motivate the APT attacker model defined in Chapter~\ref{ch:attacker-model}.

---

### 3. Chapter view

**The chain, read alone.**
- C1: three strands keyed to the SQs, the attacker strand last because it holds the gap.
- C2: can the literature yield a machine-usable specification of a campaign, and what does it lack?
- C5: order and dependency but not tempo, and the apparatus sits outside MTD evaluation.
- C6: three steps of evaluating a defence mechanism.
- C10: defence evaluation is moving to several mechanisms together.
- C11: the attacker model evaluation is scored over, which the surveys call a limitation. Derive, score, gap.
- C15: the means exist but have not been brought into MTD.
- C16: the literature does not define its attacker models, so ch4.

A reader of this chain alone learns strand 1's result (C5) and the fact that a gap exists. Two things are missing:

1. **Strand 2's result.** That the effectiveness metrics are computed over the attacker model appears nowhere in the chain. It sits in the body (C8) and in 3.3.3 (C14), and C11 only hints at it with "scored over". This is also the hinge the tex's own TECHNICAL-CLAIM FLAG says was lost with the Tay sentence. C11's revision puts it back as a `\ref` link, with no new sentence.
2. **The gap itself.** C16 names a different gap from the one 3.3.3 derives. C16's revision fixes it.

With both revisions, the chain states what each strand establishes and why §3.3 follows §3.2. C15 already carries strand 1 into the gap ("The apparatus").

**Stale or mis-aimed `\ref`.** Every `\ref` in the chapter's connective units resolves. One is mis-aimed: C14's `subsec:mtd-metrics` sits on a §3.2.1 claim. No unit previews a section that has moved.

**Duplication**
- With ch1: ch1 P3 already cites Cho and Jalowski for "attacker models far simpler than an APT". C11's survey clause is a third home for that diagnosis, after ch1 P3 and 3.3.1 P1. Ch1 P3 names persistence and adaptation (properties 1 and 4). 3.3.3 names 1, 2 and 4. That is consistent, since ch1 says "fully captures", but an examiner comparing the two will see objective conditioning missing from ch1.
- With captions: none that matters. The Table 3.3 caption and C13's pointer sentence say the same thing, which is acceptable because the caption must stand alone.
- Within the chapter: C6 S1 repeats C1's clause for §3.2.

**Skeleton (§e11).** Four openers read "This chapter/section surveys …" (C1, C2, C6, C11). Two of them were ruled deliberately: C2's verb, and C11's "sibling pattern". Changing C6 alone leaves the licensed pair (C2, C11) under a chapter opener, and breaks the run of three that voice §d and §h rule out.

**Headings (not connective prose; one line).** "Survey of APT attackers" is the only section heading with a "Survey of" prefix (the others are "MTD evaluation" and "Attacker models in MTD"). Marc's call.

**Hand-over to ch4.**
- The ch4 opener's first prose sentence (l.4167–4169, after Figure 4.1's float) is "The APT attacker model that we have produced is the model that the research gap motivated; it aims to meet the axes from Section 3.3.1".
- Taken together with C16, the handover repeats the motivation from both sides and switches term mid-hand-over: ch3 says *properties* throughout, while ch4 says *axes*.
- The ch2→ch3 link is carried by C1's appeal to the SQs rather than to anything ch2 establishes. That is appropriate for a background chapter. Ch2 has no close, and its last visible text is a placeholder (l.~1060). That is ch2's matter.

---

### 4. Priority (at most three)

1. **C16: make the chapter close hand ch4 the gap the chapter derived.** Replace the "this research gap" anaphor with P1's unmeasured-performance clause (the Jalowski clause stays, per the C20 ruling). Use *APT attacker model*. Then settle the ch3/ch4 double handshake from ch4's side, where *axes* should read *properties*.
2. **C11 with C14: restore the §3.2 → §3.3 hinge.** Replace C11's survey clause, which breaks the 2026-09-05 "diagnosis once" ruling and the no-citation-in-signposts rule, with a pointed link to §3.2.2's finding and to §3.1.1's APT definition. Re-aim C14's `\ref` at §3.2.1.
3. **C6, then C1: break the four-fold "surveys" skeleton and give the previews operations.** C6 opens on the three-step frame. C1's three clauses name what each section delivers.

---

tier audit: clean. I withdrew one draft before writing it down: a C6 revision that opened on the three-part "designed…, instrumented…, and evaluated…" sentence, because that is a three-clause opener. I also considered and dropped two C10 bridges. One revived the cut signature line ("The defender has grown more sophisticated; the attacker … has not"); the other added a forward pointer to §3.3.2's sample. Both would have restated the diagnosis 3.3.1 owns, or duplicated C11's pointer. None of the proposals introduces "not X but Y", a colon list, "such", a new trailing clause, era vocabulary, an em-dash, or a pre-ch4 *we*.

---

## Chapter 4 (APT attacker model): critique of the connective prose

Read-only review, 2026-09-25. Yardstick: `MTDSim-preambles/docs/workflows/connective_prose.md` (§a rule, §b units, §c reference, §e eleven-item check). Conduct: `critique_protocol.md`. Voice, register and terms: `voice.md` §c/§d/§h, `academic_register.md` §b/§i, `terminology.md` (with the 2026-09-25 Figure 4.1 sweep).

**Line numbers** are the current `docs/thesis/dissertation.tex`. A parallel session added 29 lines ahead of chapter 1 while this review ran. Its diff touches only the front matter and chapter 5, so no chapter 4 text changed, but every chapter 4 line number is 29 higher than it was at session start. Chapter 4 runs from l.3946 (`\chapter{APT attacker model}`) to l.5647.

**Reference check.** All 24 labels the connective units cite resolve (`grep` of every `\label`). `dissertation.log` (21:41) has no undefined references. So no unit has a broken `\ref`. The stale references below are stale in content: they resolve, but to the wrong thing or with a gap.

---

### 1. Inventory

Word counts are for prose only (comments and float bodies stripped; a `\ref`, a citation or a maths span counts as one word).

| # | Unit | Label / heading | Lines | Words | Binding ruling (one line) |
|---|---|---|---|---|---|
| U1 | Chapter opener (Figure 4.1 + two paragraphs) | `ch:attacker-model`, `fig:pipeline` | 4020–4029 (fig), 4167–4182 (P1), 4189–4196 (P2) | 160 (98 + 62) | 2026-09-04 pass 6, the *do not re-flag* list: "our existing simulator", "in the real world", "the P2 opener's 'it'". 2026-09-24: the either-or sentence is Marc's correction. 2026-09-13 SIGNPOST SLOT: "the chapter's opening roadmap carries ONE sentence … the evaluation chapter takes the model as given" (**not present in the live text**) |
| U2 | Bridge, §4.1 close (last two sentences of the pre-intrusion paragraph) | `sec:technique-graph` | 4313–4323 (bridge 4320–4323) | 104 (bridge 37) | 2026-08-16: "the defender-validity sentence and the observability-boundary naming stay OUT" (not touched) |
| U3 | Head link, §4.2 (the section's first paragraph carries the link from §4.1) | `sec:attack-profiles` | 4341–4345 | 47 | Pass 5b 2026-08-17: "deletions + his dictated sentences only" |
| U4 | Head link, §4.3 | `sec:petri-formalism` | 4449–4450 | 22 | 2026-08-18: "topic sentence (b), Marc's own words … chosen over (a) the question" |
| U5 | Mid-section bridge, §4.3 (the notation is fixed) | `sec:petri-formalism` | 4623–4625 | 28 | 2026-09-08 round 2: "a closing sentence declares the symbols the chapter's vocabulary" (session, ratify on read) |
| U6 | Bridge, §4.3 close → §4.4 | `sec:petri-formalism` | 4747–4753 | 77 | 2026-08-18: "the ceiling paragraph's 'L4 deals with this' carries the boundary"; 2026-09-08: "two symbol bindings on Marc's sentence, nothing else touched" |
| U7 | Section preamble, §4.4 | `sec:execution` "Integration with MTDSim" | 4817–4822 (P1), 4834–4858 (P2) | 266 (72 + 194) | Registry 2026-09-25: "its first sentence binds the two" (heading ↔ join). Spine sentence "The join carries three things" is Marc's dictation, 2026-08-19. P2 is E2 sweep DRAFT STATE. Insertion A (2026-09-18) is DRAFT STATE, ratify on read |
| U8 | Bridge, §4.4 close (= §4.4.4 close) | `subsec:failure-matrix` | 5372–5375 | 39 | 2026-08-20: "the ruled promoted close … one sentence at the end"; rescoped 2026-09-18 ("plausible" kept) |
| U9 | Section preamble, §4.5 | `sec:evaluation-metrics` "Evaluation metrics" | 5412–5417 | 63 | Round 2, 2026-09-25: "DRAFT STATE --- ratify on read" |
| U10 | Subsection lead-in, §4.5.1 (over `\paragraph` heads) | `subsec:metrics-behaviour` | 5422–5427 | 50 | as U9 |
| U11 | Subsection lead-in, §4.5.2 | `subsec:metrics-outcome` | 5509–5512 | 47 | as U9 |
| U12 | Subsection lead-in, §4.5.3 | `subsec:metrics-effectiveness` | 5556–5561 | 64 | as U9 |
| U13 | **MISSING**: chapter close | after l.5645 | — | 0 | none. `connective_prose.md` §f1 leaves chapter-closing bridges open for Marc |

No other missing units. §4.1–§4.3 have no subsections, so they need no preamble. §4.4 and §4.5 both have one. In the PDF (p. 41) the §4.5 heading is followed by prose, and Table 4.3 floats to p. 42, so no heading stands over only a float. Figure 4.1 is `[t]` and the opener's prose follows it.

### Verbatim current text

**U1, P1** (4167–4182):
> The APT attacker model that we have produced is the model that the research gap motivated; it aims to meet the axes from Section~\ref{subsec:attacker-criterion}. MTDSim can run either the APT attacker model or the baseline attacker of Section~\ref{subsec:attacker-model}, on the same network and under the same defences, so that the two can be compared. The APT attacker model shares the baseline attacker's actions, but its choice of the next tactic is set at runtime by the Petri net of its attack profile. This is a proof of concept, testing whether behavioural fidelity changes existing MTD evaluation.

**U1, P2** (4189–4196):
> We are grounding it in CTI to recover the behaviour of APT attackers in the real world (\ref{sq:capture}, Sections~\ref{sec:technique-graph} and~\ref{sec:attack-profiles}). We are distilling that behaviour into attack profiles and their Petri nets, which we join to our existing simulator (\ref{sq:model}, Sections~\ref{sec:petri-formalism} and~\ref{sec:execution}), to evaluate our defence mechanisms (\ref{sq:evaluate}, Chapter~\ref{ch:experiments}). Figure~\ref{fig:pipeline} is the pipeline that answers them.

**U1, Figure 4.1 caption**: "The APT attacker model: built from 38 attack flows and joined to MTDSim, which runs either it or the baseline attacker; both are measured. Blue marks the APT attacker model and how it is built; each arrow marked with a section is described in that section." (The figure's arrows read: combine §4.1, split by objective §4.2, make executable §4.3, join to MTDSim §4.4, measure §4.5. Source: `tools/ch4_overview_figure.py`.)

**U2** (4313–4323; the bridge is the last two sentences):
> Another limitation we encountered was an issue with a lack of pre-intrusion dependencies: any tactics before initial access were sparse compared to the rest of the corpus. […] Hence, in the corpus, reconnaissance only has a mention in 10 out of the 38 attack flows. **But since we are producing an attacker model for defender evaluation, we will later have to draw these edges in (Section~\ref{sec:petri-formalism}). This is persistent across CTI, so we would have to address it regardless of our input.**

**U3** (4341–4345):
> The literature tells us that APT attackers are not a homogeneous group, and so they are distinguished by campaign-level intent. We cannot produce an APT attacker model that could be considered behavioural, because the attack graph carries so many different motivations and objectives which influence behaviour \citep{alshamrani2019}.

**U4** (4449–4450):
> We needed a data structure to pipe in the attack profiles as an input, and this is what the Petri nets provide.

**U5** (4623–4625):
> The rest of this chapter and the evaluation are stated in these terms; Table~\ref{tab:gspn-notation} collects the symbols, and Figure~\ref{fig:gspn-gadget} draws one tactic of one Petri net.

**U6** (4747–4753):
> But there are limits to what the Petri net can provide: parameters (the timings $\mu_p$ of how long the attacker dwells at a tactic; the exponential defence of the dwell times; the mapping $\varphi$; the failure matrix $F_{\text{failure}}$) and mechanics (the verdict $v$ by which $F_v$ reweights the out-transitions a token may choose at runtime, based on the success of the APT attacker model in the simulator; sink retrace policy). Section~\ref{sec:execution} supplies these through the join.

**U7, P1** (4817–4822):
> This section integrates the Petri nets $\mathcal{N}_c$ of Equation~\ref{eq:gspn} with MTDSim through the join, which supplies what the nets cannot. The Petri nets can act as inputs, but like source code they cannot run against the simulator without a join. A Petri net run on its own produces a timeline of what the attacker did; such a run is one-way, with no input from the simulator. The join is therefore two-way.

**U7, P2** (4834–4858):
> Sections~\ref{sec:technique-graph} to~\ref{sec:petri-formalism} produce the Petri net: the token is moving through all these tactics. Within the simulator, MTDSim, the baseline attacker has its actions and has six phases, as outlined in Chapter~\ref{ch:background}. To produce results, we have to join the two. We scoped it down: for this dissertation we adopt the existing actions from the simulator. The APT attacker model and the baseline attacker are two different attackers, built for different purposes, with the baseline attacker as the reference: neither replaces the other. MTDSim runs either one, on the same network and under the same defences, so that the defence mechanisms can be evaluated against each attack profile and compared across the two attackers. The join carries three things: the dwell times, the mean dwell $\mu_p$ of Equation~\ref{eq:gspn}; the tactic-to-action mapping, $\varphi$; and the failure matrix, $F_{\text{failure}}$ of Equation~\ref{eq:vc-net}. These are the three inputs we had to declare to join the attack profiles to MTDSim. We chose each of them to the best of our judgement after consulting the literature; whether any conclusion of the evaluation depends on where a chosen value sits is the question Appendix~\ref{app:sensitivity} answers.

**U8** (5372–5375):
> This is verdict-conditioned re-weighting (Equation~\ref{eq:routing}); this is what encodes direction. We judged these a plausible set of values to feed into the APT attacker model, and Appendix~\ref{app:sensitivity} reports what it would cost to be wrong about them.

**U9** (5412–5417):
> This section defines the ten metrics that Chapter~\ref{ch:experiments} reports (Table~\ref{tab:metrics}). A metric the field defines is used as defined; where this thesis adapts or introduces a metric, its definition states the change and why it is needed. Every metric is computed over a \emph{cell} $\mathcal{R}$, the runs of one attacker under one condition at one deployment interval, with $r \in \mathcal{R}$ one run.

**U10** (5422–5427):
> Three properties of a sophisticated attacker concern how it acts, which the outcome metrics of Section~\ref{subsec:metrics-outcome} do not record: objective conditioning, strategic plurality and stealth (Table~\ref{tab:attacker-properties}). Relative tactic occurrence records the first, APV the second, and attack rate and attack confidentiality the third, each with no defence running.

**U11** (5509–5512):
> Three metrics record what the attacker achieves: ASP whether it takes a target, NCR how much of the network it takes, and MTTC how soon it takes its first host. All three are established in MTD evaluation (Table~\ref{tab:mtd-metrics}), so the results are comparable with the field's.

**U12** (5556–5561):
> Three metrics record what a defence changes, each against the same attacker's runs with no defence. NCR reduction records the net change over a run and ranks the defences. The NCR growth rate and time lost record the attacker's response to each deployment, which a net measure cannot show: this response is adaptivity (Table~\ref{tab:attacker-properties}), and no cited metric records it for the attacker.

### Section and subsection closes checked that are not bridges and need none

| Close | Lines | What it does | Bridge needed? |
|---|---|---|---|
| §4.2 (the Wizard Spider paragraph) | 4407–4413 | ends on a characteristic of the partition, with Conti as the example | No. U4, §4.3's first sentence, carries the link through "the attack profiles". The comment trail records that Marc declined to reinstate "what distinguishes them" |
| §4.4.1 (the ceiling paragraph) | 5030–5034 | the must-carry concession: "the APT attacker model can only be as good as what we adopt" | No, the next subsection is a parallel input, not a dependent one. One flag on a body sentence, raised only: "But it is extendable and modular: our Petri nets can be mapped to anything" is a value close (§e6), and "anything" claims more than the chapter shows |
| §4.4.2 (the exponential must-carry + Table 4.2) | 5155–5162 | the caveat "model parameters anchored to this simulator, not real-world measurements" | No |
| §4.4.3 (the alternative mappings, Caldera) | 5224–5229 | the rejected alternatives | No |
| §4.5.1–§4.5.3 last paragraphs | — | metric definitions | No. Each sibling's lead-in carries the relation |
| §4.5.4 (the Spearman sentence) | 5636–5645 | the last sentence of the chapter | See U13 |

---

### 2. Per unit

Check items follow `connective_prose.md` §e: 1 exists · 2 link carries a finding · 3 aim as a job · 4 roles, not topics · 5 dependency shown · 6 no flourish · 7 no duplication · 8 tense, person and agent · 9 references and terms · 10 scale · 11 varied. "n/a" marks an item that does not apply to the unit type (for example, a bridge has no link or aim move).

#### U1: Chapter opener. Verdict: **rework**

**Check:**
1 Y.
2 **N**: "is the model that the research gap motivated" names the gap as a topic without stating it. Chapter 3 has already made this link twice: its opener says it "closes on the gap that motivates Chapter 4", and its last sentence says "this research gap motivates the attacker model defined in Chapter 4". The finding itself, "the performance of MTD against an attacker with a foothold therefore remains unmeasured" (ch3), appears nowhere in chapter 4.
3 **N**: P1 states the model's aim ("aims to meet the axes"), not the chapter's job. The job only comes through indirectly, via the SQ tags in P2.
4 Y: every clause has a verb (ground, recover, distil, join, evaluate).
5 Y: "that behaviour" carries SQ1 into SQ2.
6 Y. "Figure 4.1 is the pipeline that answers them" is thin, but it is not a flourish.
7 **N**: S2 ("MTDSim can run either …") repeats Figure 4.1's caption on the same page ("joined to MTDSim, which runs either it or the baseline attacker"). §4.4's preamble repeats it again, as does ch1 P5 ("Both attackers run on the same network and under the same defences").
8 **N**: "We are grounding", "We are distilling" are progressive. The present simple is the convention for what a chapter does (§c1). The 2026-08-19 "'we are going to' stays" ruling covered a sentence that no longer exists.
9 **N**: four problems.
   - The roadmap is **stale**. §4.5 is not mentioned at all, although Figure 4.1 marks "measure §4.5", and SQ3 points only at Chapter 5.
   - The attack profiles, which §4.2 builds, sit in the SQ2 clause, while §4.2 is tagged SQ1. This also breaks ch1's contribution 1, which files attack profiles under SQ1.
   - "axes" is the only own-voice *axes* left in the prose. Section 3.3.1's heading, Table 3.2, the ch3 gap ("six of the eight properties") and §4.5.1 all say *properties*. The registry has a PROPOSED row for exactly this site.
   - "pipeline" is not the figure's word: its caption title is "The APT attacker model and where it runs", its frame "Building the APT attacker model".
10 **N**, borderline: 160 words in two paragraphs, against one paragraph of 60–150 words. The 2026-09-04 note already recorded this as "Marc's cut, if any".
11 Y. Ch2 and ch3 open with "This chapter sets out/surveys…"; ch4 opens on the model.

**Moves present:**
- Link: a topic link only.
- Aim: implicit.
- How: a map keyed by sub-question, missing §4.5.
- Shared frame: the model's relation to the baseline attacker and its proof-of-concept scope. This is the unit's strongest material.
- Bridge: n/a.

**Findings:**
1. **Stale roadmap (§e9, §c4; §e4).** Two restructures changed the chapter after this map was written: the 2026-09-22/25 sweep brought the metrics into chapter 4, and the Figure 4.1 redesign mapped every section. The prose map missed both:
   - §4.5 is unannounced, and "to evaluate our defence mechanisms (SQ3, Chapter 5)" skips the section that defines how SQ3 is measured.
   - "our defence mechanisms" misattributes MTDSim's defences. Chapter 1 says this dissertation "proposes no new defence".
   - Filing the profiles under SQ2 contradicts both the section key and ch1's contribution 1.
2. **Link without the finding (§e2, §e7).** A back-link is right. Marc re-ruled at ch3's close that "ch4's first sentence makes the same link back". But it should carry ch3's result in ch3's own words ("remains unmeasured") and not add a third statement that the gap motivates the model.
3. **Terms and referents (§e9, §e8).** Three rulings to overturn, and one ruled sentence missing:
   - "axes" → "properties". This overturns Marc's 2026-08-19 "eight axes, keep it simple" on merit: the ch3 rebuild of 2026-09-07 made *properties* the reader's word, and the PROPOSED registry row awaits his call.
   - P2's "it" now points three sentences back, past "a proof of concept". This overturns the 2026-09-04 "the P2 opener's 'it'" do-not-re-flag on merit: the antecedent it was ruled against was deleted by the E2 sweep, and the sweep's own DRAFT STATE note says the run of "It" is residue.
   - The ruled 2026-09-13 signpost sentence ("the evaluation chapter takes the model as given") is missing.

**Proposal** (150 words; two paragraphs, as ruled 2026-09-04):

> The MTD evaluations surveyed in Chapter~\ref{ch:litreview} leave the performance of MTD against an attacker with a foothold unmeasured. The APT attacker model this chapter defines aims to meet the eight properties of Section~\ref{subsec:attacker-criterion}. The APT attacker model shares the baseline attacker's actions, but its choice of the next tactic is set at runtime by the Petri net of its attack profile. It is a proof of concept, testing whether behavioural fidelity changes existing MTD evaluation.
>
> Sections~\ref{sec:technique-graph} and~\ref{sec:attack-profiles} ground the model in CTI to recover the behaviour of APT attackers in the real world (\ref{sq:capture}). Sections~\ref{sec:petri-formalism} and~\ref{sec:execution} make that behaviour executable as Petri nets and join them to our existing simulator (\ref{sq:model}). Figure~\ref{fig:pipeline} draws each step, and Section~\ref{sec:evaluation-metrics} defines the metrics with which Chapter~\ref{ch:experiments} answers \ref{sq:evaluate}. Every assumption is declared with the symbol it constrains, and Chapter~\ref{ch:experiments} takes the model as given.

**What the proposal does:**
- **Every word comes from existing text.** S1 uses ch3's words. S3 is kept verbatim. S4 is Marc's, with "This is" → "It is", his own 2026-09-04 move. The two P2 verbs "make executable" and "join" are Figure 4.1's.
- **Kept:** the do-not-re-flag items "our existing simulator" and "in the real world".
- **Overturned:**
  - The 2026-09-24 either-or sentence moves out of the opener, on merit. It duplicates the caption of the figure the opener points at, and §4.4.1 already states the controlled comparison ("held identical for both attackers, so that a difference between the arms is a difference in the attacker and nothing else"). This changes where the sentence sits, not its wording. If Marc keeps it, the opener is 179 words, over scale.
- **Stand-in:** the last sentence stands in for the 2026-09-13 SIGNPOST SLOT ("Marc's sentence") and is built from the ruling's own words. His dictation replaces it.
- **Depends on his ruling:** "properties" needs Marc's call on the PROPOSED registry row.

#### U2: §4.1 close (bridge part). Verdict: **tighten**

**Check:** 1 n/a · 2 n/a · 3 n/a · 4 Y ("draw these edges in") · 5 Y (→ §4.3) · 6 Y · 7 Y · 8 **N** ("we will later have to": future tense for what a later section does, §c1) · 9 Y · 10 Y (two sentences) · 11 n/a.

**Moves present:** a forward bridge to §4.3. It does not bridge to §4.2 and does not need to, because U3 carries that link.

**Findings:**
1. The last sentence, "This is persistent across CTI, so we would have to address it regardless of our input.", is tacked on after the forward pointer. Its "This" has no immediate referent (critique §e2). It is the reason the pointer exists, so it belongs before the pointer.
2. The future tense (§c1).

**Proposal** (33 words, replacing the two sentences; moved and nouned, Marc's words otherwise):

> The sparsity is persistent across CTI, so we would have to address it regardless of our input. Because we are producing an attacker model for defender evaluation, Section~\ref{sec:petri-formalism} draws these edges in.

#### U3: §4.2 head link. Verdict: **keep**

**Check:** 1 n/a · 2 Y (it states why §4.1's product is not enough: "the attack graph carries so many different motivations and objectives") · 3 Y · 4 Y · 5 Y · 6 Y · 7 Y · 8 Y · 9 Y · 10 Y · 11 n/a.

**Why it works:** it is the content bridge §b bridge-4 asks for. The old-information noun ("the attack graph") is carried across, and the reason for partitioning is a research act, not a signpost.

**Minor, not blocking:**
- "The literature tells us" is spoken register.
- The citation sits on S2 but grounds S1's claim.
- "could be considered behavioural" is vague.

Marc's pass-5b text. No proposal.

#### U4: §4.3 head link. Verdict: **keep (flagged)**

**Check:** 1 n/a · 2 Y (picks up "the attack profiles") · 3 **N** (weak) · 4 Y · 5 Y · 6 Y · 7 Y · 8 Y · 9 Y · 10 Y · 11 n/a.

**Flag only** (ruled 2026-08-18, Marc's words; it does not plainly break the guidance):
- The need it names, "a data structure to pipe in the attack profiles as an input", is weaker than the section's real job. That job is timing and stochastic choice (the next sentence) and "make executable" (Figure 4.1's verb for §4.3). Any structure takes an input.
- "pipe in" is spoken register.

If Marc reopens the sentence, the figure's verb is the one to use. No proposal.

#### U5: §4.3 mid-section bridge. Verdict: **keep**

**Check:** 1 n/a · 2 n/a · 3 n/a · 4 Y · 5 Y ("the rest of this chapter and the evaluation are stated in these terms") · 6 Y · 7 Y · 8 Y · 9 Y · 10 Y · 11 n/a.

**Why it works:** it states a research act, that the notation is now fixed for everything that follows, and points once at each float. Optional T1: "the evaluation" → "Chapter~\ref{ch:experiments}". No proposal.

#### U6: §4.3 close → §4.4. Verdict: **tighten**

**Check:**
1 n/a · 2 n/a · 3 n/a · 4 Y · 5 Y (→ §4.4) · 6 Y.
7 **N**: U7's preamble repeats the unit twice, one line later. S1 of U7 ("which supplies what the nets cannot") repeats "Section 4.4 supplies these through the join", and U7's spine sentence re-lists the same three inputs with the same symbols.
8 Y.
9 **N**: three problems.
   - "parameters" is not the term §4.4 and the registry use ("the join (its three declared inputs)").
   - "the exponential defence of the dwell times" is in the list, but the registry records it as "the justification, not the mechanism". The join does not supply a justification.
   - "the timings $\mu_p$ of how long the attacker dwells" is not the notation table's "mean dwell".
10 Y (two sentences), though S1 carries about eight propositions (critique §e5).
11 n/a.

**Moves present:** what is established (the net lacks inputs and mechanics) plus the forward link. This is the chapter's best bridge.

**Findings:**
1. The term mismatches (§e9, §c5).
2. The back-to-back repetition with U7 (§e7). Keep the bridge, and cut the repetition in U7.
3. The gloss "based on the success of the APT attacker model in the simulator" repeats what $v$ already says.

**Proposal** (53 words; Marc's colon and both parentheses kept):

> But there are limits to what the Petri net can provide: the declared inputs (the mean dwell $\mu_p$ of each tactic, the mapping $\varphi$, the failure matrix $F_{\text{failure}}$) and the mechanics (the verdict $v$ by which $F_v$ reweights the token's out-transitions at runtime; the sink-retrace policy). Section~\ref{sec:execution} supplies these through the join.

#### U7: §4.4 preamble. Verdict: **rework**

**Is it connective prose?** Partly. About a third of the 266 words does preamble work.
- **Connective:**
  - S1 binds the heading to *the join*, as the registry requires.
  - The one-way/two-way sentences give the section's job.
  - The spine sentence and Insertion A give the shared frame of §b preamble-3: all three subsections are declared inputs, and all three were chosen by judgement and tested in Appendix C.
- **Body content in the preamble slot:**
  - A recap of §4.1–§4.3 and of ch2.
  - The scope decision, which the §4.4.1 ceiling paragraph also states.
  - The design of the two-attacker comparison. That is a chapter-level frame already said in the opener, the caption, ch1 and §4.4.1.

So it is a shared-frame preamble swollen by restatement. The frame is legitimate; the restatement is not.

**Check:**
1 Y.
2 **N**: P2 opens with a topic recap ("Sections 4.1 to 4.3 produce the Petri net: the token is moving through all these tactics").
3 Y (S1, and the two-way reason).
4 **N**: §4.4.1's role is never named. The three inputs arrive as a colon-list of topics.
5 Y ("These are the three inputs we had to declare to join…").
6 **N**: "like source code they cannot run against the simulator" is a simile doing a claim's work (§a).
7 **N**: six repetitions.
   - "supplies what the nets cannot" repeats U6.
   - "To produce results, we have to join the two" repeats S1.
   - "neither replaces the other … MTDSim runs either one" repeats the opener, Figure 4.1's caption and §4.4.1.
   - "we adopt the existing actions" repeats the opener's S3 and the ceiling paragraph.
   - The input list repeats U6.
   - "Within the simulator … six phases, as outlined in Chapter 2" repeats ch2.
8 **N**: "the token is moving" is progressive.
9 **N**: "the mean dwell $\mu_p$ of Equation~\ref{eq:gspn}". $\mu_p$ is not in Equation 4.1; it enters in the where-list and Table 4.1. §4.4.2's first sentence repeats the same pointer.
10 **N**: 266 words and 12 sentences, against 2–4 sentences and 30–90 words.
11 n/a.

**Findings:**
1. The scale and the repetition (§e10, §e7). This is the chapter's largest connective defect.
2. The subsections are not given roles (§e4). §4.4.1 is the join held fixed; §4.4.2–§4.4.4 are its three inputs. The heading notes of 2026-09-08 say this split in so many words ("the runtime mechanics (the join, held fixed), then one unit per declared input"), but the preamble never tells the reader.
3. The simile and the recap (§e6, §e2).

**Proposal** (93 words; S1 is the ruled binding with its repeated tail cut; S2 is Marc's two sentences merged at a semicolon; S4 is Insertion A verbatim except "each of them" → "each input"):

> This section integrates the Petri nets $\mathcal{N}_c$ with MTDSim through the join. A Petri net run on its own produces a timeline of what the attacker did, with no input from the simulator; the join makes the run two-way. Section~\ref{subsec:runtime-mechanics} gives the runtime mechanics of the join, and Sections~\ref{subsec:dwell-times} to~\ref{subsec:failure-matrix} declare the three inputs the join carries. We chose each input to the best of our judgement after consulting the literature; whether any conclusion of the evaluation depends on where a chosen value sits is the question Appendix~\ref{app:sensitivity} answers.

**Overturned on merit:**
- **Marc's 2026-08-19 spine sentence.** Its colon-list gives way to the subsection-role clause. U6 gives the list with its symbols one line earlier, and the three subsection headings name the inputs.
- **"We scoped it down: for this dissertation we adopt…".** The sentence is cut. The ceiling paragraph ("the actions that we are adopting from the simulator") and the opener's S3 both carry the scope. The ceiling paragraph's comment, which cites "the preamble's 'scoped it down'", should then drop that pointer.
- **The second home of the 2026-09-24 either-or design.**

Nothing new is added.

#### U8: §4.4 close (= §4.4.4 close). Verdict: **tighten**

**Check:** 1 n/a · 2 n/a · 3 n/a · 4 Y · 5 Y · 6 Y ("plausible" was kept by Marc on 2026-09-18) · 7 Y · 8 Y · 9 Y · 10 Y · 11 n/a.

**Finding:** "This is … this is … these". The unit opens after Figure 4.7. The prose sentence before the float is "These are threat-model parameters…", and the referent, the failure matrix, is three paragraphs up. This plainly breaks Marc's standing rule to name the noun (critique §e2). So the ruled close gets a minimal noun fix and no reword.

It does not bridge to §4.5, and it need not: U9 should carry that link.

**Proposal** (43 words; nouns named, Marc's words otherwise):

> The failure matrix enters the routing as verdict-conditioned re-weighting (Equation~\ref{eq:routing}); it is what encodes direction. We judged its values a plausible set to feed into the APT attacker model, and Appendix~\ref{app:sensitivity} reports what it would cost to be wrong about them.

#### U9: §4.5 preamble. Verdict: **tighten**

**Check:**
1 Y.
2 **N**: no link from the model just built, and no tie to SQ3. The unit names Chapter 5 but not the question the metrics answer.
3 Y (partial).
4 Y.
5 **N**: the relation between the subsections is left to their own lead-ins. The behaviour metrics are read with no defence, and the effectiveness metrics are measured against those same no-defence runs; that is the two-phase logic of Chapter 5.
6 Y.
7 Y.
8 Y.
9 **N**: two problems.
   - "this thesis" breaches the ratified *this dissertation* row (Marc, 2026-09-24). Two more §4.5 sites in the body do the same: "this thesis declares a detector" and "this thesis reads it at the first host".
   - "condition" is not defined. The sweep-4 screen already flagged *defence condition*. Flag only.
10 Y (63 words, three sentences).
11 n/a.

**Findings:**
1. The SQ3 link (§e2/§e3).
2. The dependency between §4.5.1 and §4.5.3 (§e5).
3. The registry breach (§e9).

**Proposal** (91 words; S1 extended; the new S2 builds on the lead-ins' own words, "with no defence running" and "against the same attacker's runs with no defence"; S3 and S4 unchanged apart from the registry fix):

> This section defines the ten metrics with which Chapter~\ref{ch:experiments} answers \ref{sq:evaluate} (Table~\ref{tab:metrics}). The behaviour metrics of Section~\ref{subsec:metrics-behaviour} are read with no defence running, and the effectiveness metrics of Section~\ref{subsec:metrics-effectiveness} compare each defence with those no-defence runs. A metric the field defines is used as defined; where this dissertation adapts or introduces a metric, its definition states the change and why it is needed. Every metric is computed over a \emph{cell} $\mathcal{R}$, the runs of one attacker under one condition at one deployment interval, with $r \in \mathcal{R}$ one run.

#### U10–U12: §4.5.1–§4.5.3 lead-ins. Verdict: **keep** (all three)

**Check:** Y on items 4–10 for all three.

**Why they work:** each is claim-first and ties its metrics to the properties or the field.
- **U10 (§4.5.1):** names what the outcome metrics miss (properties 2, 3 and 5) and maps each metric to one of them.
- **U11 (§4.5.2):** states comparability with the field as the reason for the choice.
- **U12 (§4.5.3):** is the best lead-in in the chapter. It states the dependency on the no-defence runs and why two metrics are new ("this response is adaptivity … no cited metric records it for the attacker").

On item 11: U11 and U12 open alike ("Three metrics record what…"). That is two-beat anaphora, licensed in pairs by voice.md §d. U10's "Three properties…" varies it enough not to count as a run of three.

**Minor flags, no proposal:**
- APV, ASP, NCR and MTTC appear in the lead-ins before their run-in heads expand them. Their earlier expansion is a bold cell in Table 3.1, which `term_screen` reads as never expanded.
- U10 and U11 each have a colon-then-list, the form the author hears as a tell.

#### U13: Chapter close. Verdict: **missing**, recommend leaving it absent

The chapter ends on "Spearman's $\rho$ between the two attackers' NCR reductions compares their rankings." (l.5645). `connective_prose.md` §f1 leaves chapter-closing bridges to Marc.

**Recommendation: option (c), no chapter 4 close.** Three reasons:
- The last sentence already names the comparison Chapter 5 makes.
- The opener's signpost sentence says that Chapter 5 takes the model as given.
- Chapter 5's placeholder opener links back ("Chapter 4 declares the model. This chapter declares the experiment …").

A close would repeat both the signpost and Chapter 5's link.

**Proposed text, only if Marc rules (a) or (b)** (33 words):

> This chapter has declared the APT attacker model and the ten metrics it is read by. Chapter~\ref{ch:experiments} runs the model beside the baseline attacker, first with no defence and then under MTD.

---

### 3. Chapter view

**Read in sequence without the bodies**, the connective units form this chain:

- **Opener:** the gap as a topic, then a map that stops at §4.4.
- **§4.1** begins plainly ("We made the attack graph using Attack Flow."; the opener's map carries the link). **U2** closes it with a forward pointer to §4.3.
- **U3** says the attack graph mixes objectives, so it must be split.
- **U4** says the profiles need an executable structure.
- **U5** fixes the notation.
- **U6** says what the net lacks and hands it to §4.4.
- **U7** restates all of that at length.
- **U8** names what the failure matrix encodes.
- **U9** says "the metrics Chapter 5 reports".
- **U10–U12** follow; there is no close.
- **Chapter 5:** "Chapter 4 declares the model."

**From §4.1 to §4.4 the chain works.** Each link carries an old-information noun forward: attack graph → attack profiles → Petri net → the join. That is exactly the §b bridge-4 pattern, and U6 is a model bridge. A reader of only these units learns what is built and why each step needs the one before.

**Two breaks:**
1. **§4.5 arrives unannounced and unmotivated.** The opener's map omits it. Its preamble says neither that the metrics are how SQ3 is answered nor how the behaviour and effectiveness metrics depend on one another. The same reader would not learn that chapter 4 also fixes the measures, including the two new ones that ch1's contribution 3 claims ("two new measures of disruption").
2. **The §4.3 → §4.4 seam says one thing three times:** U6's last sentence, U7's S1 tail, and U7's "To produce results, we have to join the two".

**Stale references:**
- None are unresolved.
- Stale by content:
  - The opener's roadmap is missing §4.5.
  - The attack profiles sit in the SQ2 clause.
  - "the mean dwell $\mu_p$ of Equation 4.1" (U7; §4.4.2's first sentence says the same) points at an equation that does not contain $\mu_p$.
  - "Figure 4.1 is the pipeline" names the figure by a word neither its caption nor its title uses.

**Duplication:**
- **The fact that "MTDSim runs either attacker under identical conditions"** is stated five times by the end of §4.4.1:
  - ch1 P5;
  - Figure 4.1's caption;
  - the opener's S2;
  - U7's P2;
  - §4.4.1 ("held identical for both attackers").

  The proposals keep it in ch1, the caption and §4.4.1.
- **Against ch1's contribution list:**
  - The opener's SQ tags agree with contributions 1–2 except for the profiles clause.
  - Contribution 3's new measures are §4.5.3, which the current opener never reaches.

**Hand-over to chapter 5:**
- **Chapter 5's placeholder:** its link ("Chapter 4 declares the model") is a topic link (§e2). When Marc dictates it, it should name what chapter 4 fixed, the model and the metrics.
- **The signpost said once on each side:** the ch4 opener states that "Chapter 5 takes the model as given", and chapter 5's link restates it from the other side. That is option (c) of §f1.

**Agent form (§f3, Marc's open call):**
- Chapter 4 mixes forms. The opener's P2 and the bodies use *we*; U7 and U9 use the section as agent ("This section integrates / defines").
- The proposals follow §c3's verb-class reconciliation. Section-as-agent takes operation verbs for previews ("Sections 4.1 and 4.2 ground…", "This section defines…"). *We* is kept for decisions ("We chose each input…").

**Variation (§e11):**
- Ch2 opens "This chapter sets out…" and ch3 "This chapter surveys…"; chapter 5's placeholder opens "Chapter 4 declares…".
- The proposed ch4 opener starts from ch3's finding, so the four openers do not share a skeleton.

---

### 4. Priority

1. **Rework the opener (U1).**
   - Re-key the map to all five sections, with §4.5 as the metrics for SQ3 and the profiles under SQ1.
   - Put chapter 3's finding in the link, not a third "the gap motivates".
   - Fix "our defence mechanisms", "axes" and the stray "it".
   - Land the ruled 2026-09-13 signpost sentence.
   - This matters most because the opener is the one unit an examiner reads first, and its roadmap is currently stale.
2. **Cut the §4.4 preamble (U7) from 266 to about 93 words.**
   - Keep the ruled binding sentence, the one-way/two-way reason, the roles of the four subsections and Insertion A's frame.
   - Drop the recap, the simile, and the either-or design and scope that are said elsewhere.
   - Let U6, tightened, be the one handover from §4.3.
3. **Make §4.5 connect (U9), and rule on the chapter close.**
   - Add the SQ3 link and the behaviour → effectiveness dependency.
   - Change *this thesis* to *this dissertation* at the three §4.5 sites.
   - Rule §f1 for chapter 4's close; recommend none (U13).

---

### 5. Tell audit

**Withdrawn from my own drafts before writing them down:**
- "the only part of the APT attacker model that touches MTDSim": a claim the chapter does not make.
- "…, with the baseline attacker as the reference": a tacked-on trailing clause in the opener.
- "combining … and splitting …": participial tails in the opener's map.
- "the whole method": filler.
- "38" in the opener: a decorative number, since the caption and ch1 carry it.
- A third consecutive sentence opening "Section(s)" in P2: a run of three.
- "Figure 4.1 draws each step with its section": duplicates the caption; cut to "draws each step".

**Retained and flagged, not introduced** (all are the author's own words):
- "testing whether …", a trailing *-ing* clause from Marc's 2026-09-04 re-dictation.
- The colon-then-list in U6, which is his sentence.
- The SQ parentheses in P2's opening sentence, which is his 2026-09-04 ruling (f).

All interventions are T2 suggestions. None has been applied to the repo.

**tier audit: clean** (after the withdrawals above).


---

## Chapter 5 (Evaluation), second critique: connective prose, flourish and accuracy

Text: `/home/marc/GitHub/MTDSim-preambles/docs/thesis/dissertation.tex` (branch `chore/preamble-interstitial-guidance` at 4ed41907, which carries the plain-description rewrite 28cab9ca). Chapter 5 runs from l.5852 to l.8312. All line numbers below are that file's. Read-only: no repo file was edited.

Loaded in this order: `connective_prose.md` (§a, §b, §e, §f), `critique_protocol.md`, `voice.md` §c/§d/§h, `academic_register.md` §b/§c/§e/§i, `evaluation_conventions.md` §e/§f2/§j/§k, and `terminology.md`. One more rule is in force on `dev` but has not reached this branch: the **§j2 amendment of 2026-09-26**, commit 53937cc4. Under it, each results paragraph opens on the float, gives its numbers and names the property. It also bans metaphor and inversion openers ("The two attackers reverse …"). This critique applies it.

Context read: ch1 SQ3 (l.343), contribution 3 and the thesis overview (l.444–505), the ch4 opener with the 2026-09-24 relation ruling (l.4285–4331), the §4.5 preamble through §4.5.4 (l.5608–5849), and the ch6 plan comments (l.8313 on).

**Numbers were checked against the tracked artefacts:**
- `data/results/ch5_s531_unopposed/numbers.json`;
- `data/results/ch5_defended/{numbers,disruption_numbers}.json`;
- the generated tables `tab_5-2-1a`, `tab_5-3-2c` and `tab_5-3-2d`.

---

### 1. Status of the earlier findings (critique_ch5.md)

**Connective units**
- **U1 opener, "takes its place"**: still present and now **worse**. The text now says "replaces it" outright (l.5918), which is the word Marc ruled wrong on 2026-09-24.
- **U1, topic link (the metrics are not picked up)**: still present (l.5914).
- **U1, comparison stated twice**: fixed. It is now stated once ("beside it under every condition", l.5915). The roadmap has turned into four one-clause sentences in a row, though (new, see §2).
- **U2, §5.1 Runs (keep)**: unchanged (l.6648–6653).
- **U3, §5.2 head repeats the opener**: still present, reworded (l.6996–6997). It has also lost its ties to §4.5.1 and §4.5.2.
- **U4, §5.2 close (the reference said again)**: still present, shortened (l.7389–7390).
- **U5(a), the false "Each effect is the NCR reduction"**: fixed (the sentence is gone).
- **U5(b), colon-then-list roadmap**: fixed. The roadmap is now one sentence with the verb elided.
- **U5(c), heading says "execution schemes" while the preamble says "deployment strategy"**: still present (heading l.8153, preamble l.7655).
- **U5, scale**: improved from 150 to 108 words, still over the 90-word range.
- **U6, §5.3.1 close ("thus", a restatement, an unclear "that")**: "thus" has become "therefore" and the restatement stays (l.7910–7911). The referent is fixed ("the same").
- **U7, §5.3.2 close (teaser)**: the teaser is fixed. Its replacement is a bare preview that repeats the preamble and §5.3.3's first sentence (l.8131–8132). New defect.
- **U8, no chapter close (keep)**: unchanged. The chapter still ends on the `\owed` timing-distribution sentence (l.8256).

**Sweep items**
- **F1, the "with …" tail in Network**: still present (l.6324–6327).
- **F2, "rather than five"**: still present (l.6330).
- **F3, three-clause lineage sentence (ruled)**: still present (l.6330–6334).
- **F4, "Eleven conditions:"**: still present (l.6389).
- **F5, "run as released: … choosing"**: still present (l.6394–6395).
- **F6, "Where one interval is reported it is 200 s"**: still present (l.6401). §5.3.1 now states outright that it reads 2 000 s (l.7796), so the contradiction is sharper.
- **F7, "ten times the 100 runs … of Zhang" (ruled)**: still present (l.6648–6649).
- **F8, "many" / ambiguous "them"**: fixed ("26 to 47 % of its steps", l.7141).
- **F9, "that campaign" with no antecedent**: fixed.
- **F10, "part ways / open alike"**: fixed.
- **F11, booster "only"**: fixed. The sentence was rewritten with a "Because …" reason (see S13).
- **F12, "the one property the no-defence runs cannot show"**: still present in new words, "the one property that needs a defence to be seen" (l.7793–7795).
- **F13, "has recovered from the last"**: moved into the head's interval clause (l.7797–7798). Still present.
- **F14, "knocks each attacker down"**: fixed.
- **F15, "stays down"**: fixed.
- **F16, "whiskers apart"**: fixed.
- **F17, "Every line falls … except user shuffle"**: over-corrected. The exception was dropped and the universal is now **false** (l.8044, see S2).
- **F18, "saturate"**: fixed (sentence cut).
- **F19, MTDShield sentence**: moved to l.8063–8066. The split fixed the subject–verb gap. The juxtaposition still implies the mechanism.
- **F20, "User shuffle is the exception"**: fixed. User shuffle is now one sentence (l.8047–8050), repeated in §5.3.3.
- **F21, rank-1 antithesis**: fixed (the MTTC sentence was cut).
- **F22, decision-rule synonym drift**: partly fixed. "matches", "move together" and "separates" remain (l.8239–8243). A new drift appears in the preamble: "taken to differ from no effect" (l.7648–7649).
- **F23, MTDShield claim in two subsections**: moved. The service-diversity choice now appears in §5.3.2 (l.8063) and again as a reason in §5.3.3 (l.8254–8255).
- **F24, construction reason attached to no observation**: the sentence is fixed (cut). No sentence reads Figure 5.6's two execution schemes.

**Chapter-view items**
- **Stale ch6 plan comments** (`subsec:aio-capabilities`; stealth "nothing"; adaptivity from "action mix"): still present (l.8335–8350).
- **Ch1 contribution 3, "in two phases … two new measures of disruption"**: still present (l.455–456).

Of the earlier findings, **16 survive or have moved, and 3 of those are worse** (U1 "replaces", F6, and F17 now false). Another **16 are fixed**.

---

### 2. Connective units

### Inventory

| # | Unit | Lines | Words | Binding ruling |
|---|---|---|---|---|
| U1 | Chapter opener | 5914–5923 | 86 | DRAFT STATE (rewrite 2026-09-26). **Marc 2026-09-24 (l.4285):** "replaces" and "built beside" are wrong; "MTDSim runs either under identical conditions". Connective R1: ch4 has no close, so this opener carries the ch4→ch5 link. |
| U2 | §5.1 (no preamble, by ruling) | n/a | 0 | Marc 2026-09-18: no lead sentence ("it reads like a caption … just cut it"). §5.1 has no subsections. |
| U3 | §5.2 head | 6996–6997 | 15 | DRAFT STATE (rewrite). §5.2 has no subsections (Marc 2026-09-23). |
| U4 | §5.2 close | 7389–7390 | 10 | DRAFT STATE; no Marc wording ruling. |
| U5 | §5.3 preamble | 7645–7655 | 108 | DRAFT STATE (rewrite). "Reference" is reserved for the no-defence runs (conventions §f2). |
| U6 | §5.3.1 close | 7910–7913 | 40 | DRAFT STATE (rewrite). |
| U7 | §5.3.2 close | 8131–8132 | 9 | DRAFT STATE (rewrite). |
| U8 | Chapter end | 8252–8264 | n/a | Slot plan: "No chapter summary; no pointer to chapter 6". R1: a close only where the next chapter depends on a result. |

Verbatim prose, with comments stripped:

- **U1:** "This chapter runs the APT attacker model of Chapter 4 against MTD, with the baseline attacker beside it under every condition. The baseline attacker is the attacker the MTDSim lineage evaluated MTD against (Section 3.3.2), and SQ3 asks how MTD's performance changes when the APT attacker model replaces it. Section 5.1 sets out the experiment. Section 5.2 compares the two attackers with no defence running, which gives the reference every later effect is measured from. Section 5.3 compares them under MTD. Chapter 6 interprets the results."
- **U3:** "This section compares the APT attacker model with the baseline attacker with no defence running."
- **U4:** "These no-defence runs are the reference for Section 5.3."
- **U5:** "This section runs both attackers under MTD. Every figure and table shows the APT attacker model beside the baseline attacker. Where the APT attacker model is one line or column, it pools c1 to c4 with equal weight; c_agg appears separately in Section 5.3.3. An effect is taken to differ from no effect when its 95 % interval excludes zero, and defences that share a Scott–Knott rank are not told apart (Section 4.5.4). Section 5.3.1 shows what a single deployment does to each attacker, Section 5.3.2 the NCR reduction of each defence across the deployment interval, and Section 5.3.3 the same by mechanism, attack profile and deployment strategy."
- **U6:** "The mechanisms that cost an attacker most therefore depend on the attacker: the host layer for the APT attacker model, service diversity for the baseline attacker. Section 5.3.2 reads whether the same holds for NCR reduction across the deployment interval."
- **U7:** "Section 5.3.3 shows each mechanism and attack profile separately."
- **U8** (last live sentences): "…MTDShield stays within 0.12 of service diversity at every interval, which follows from its choice of service diversity at most decisions. [\owed: the exponential timing distribution at 200 s …]"

**Missing units: none.** Only §5.3 has subsections, and it has a preamble.

#### U1, chapter opener: **rework**

| §e | Y/N | Reason for N |
|---|---|---|
| 1 exists | Y | |
| 2 link carries a finding | **N** | "the APT attacker model of Chapter 4" is a topic link. The ch4 opener hands over two things, the model and "the metrics with which Chapter 5 answers SQ3" (l.4322), and "Chapter 5 takes the model as given". The opener picks up only the model. Under R1, ch4 has no close, so this is the only hand-over. |
| 3 aim as a job | **N** | The aim reaches the reader through an SQ3 paraphrase that changes the question. SQ3 (l.343) asks "how does MTD perform … compared with the simulator's baseline attacker"; the paraphrase asks what changes when the model "replaces it". The opener also starts "This chapter …" before any context (§b opener 2). |
| 4 roles | Y | "sets out", though, is a writer act. |
| 5 dependency | Y | "which gives the reference every later effect is measured from" |
| 6 no flourish | Y | |
| 7 no duplication | Y | |
| 8 tense/person/agent | Y | |
| 9 refs + terms | **N** | "replaces" breaches the 2026-09-24 ruling word for word. "beside it" echoes the ruled-out "built beside". "under every condition" uses *condition* before §5.1 defines the 11 conditions. |
| 10 scale | Y | 86 words |
| 11 varied | **N** | Four one-clause sentences in a row ("Section 5.1 sets out… Section 5.2 compares… Section 5.3 compares… Chapter 6 interprets…") are the §a laundry-list skeleton and voice §h symmetric openers. The "This chapter + verb; Section + verb" frame is ch3's skeleton (l.1264). Ch2 and ch4 open on context. |

Findings:
1. **§e9, the ruling breach.** "SQ3 asks how MTD's performance changes when the APT attacker model replaces it" reinstates, verbatim, the relation Marc overturned on 2026-09-24. It is the first description of the design an examiner reads in the chapter. Ch2's opener already uses the ruled form ("compared with the simulator's baseline attacker", l.537), and the abstract does too ("run under identical conditions", l.182).
2. **§e2.** The link names chapter 4's object instead of what chapter 4 fixed, the model and its metrics. Ch1's overview says it in one clause: "defines the metrics that measure MTD's performance. With those metrics, Chapter 5 runs…" (l.496–498).
3. **§e11 / §a.** The roadmap is a run of identical "Section X verb" sentences.

Proposal (T2, 85 words). It is built from ch4's hand-over, SQ3 verbatim, Marc's ruled relation, and the draft's own S2, S4 and S6. Only two sentences open on "Section".

> Chapter~\ref{ch:attacker-model} builds the APT attacker model and defines the metrics that measure MTD's performance. \ref{sq:evaluate} asks how MTD performs against the APT attacker model compared with the simulator's baseline attacker, the attacker the MTDSim lineage evaluated MTD against (Section~\ref{subsec:recent-threat-models}). MTDSim runs either attacker under identical conditions, which Section~\ref{sec:dimensions} sets out. Section~\ref{sec:attacker-in-operation} compares the two attackers with no defence running, which gives the reference every later effect is measured from. Section~\ref{sec:effectiveness} compares them under MTD, and Chapter~\ref{ch:discussion} interprets the results.

#### U2, §5.1: **keep (no preamble, no bridge)**

A setup declares and stops (conventions §a). No lead sentence, by Marc's ruling of 2026-09-18. §5.2 depends on no *result* of §5.1, so §b bridge 1 licenses no bridge. The Defence unit's closing sentence, "The no-defence runs are the reference for every effect this chapter reports" (l.6403), is the setup's own declaration of the reference and is the right home for it.

#### U3, §5.2 head: **tighten**

| §e | Y/N | Reason |
|---|---|---|
| 1 | n/a | no subsections |
| 3 | Y | |
| 4 | Y | "compares" |
| 6 | Y | |
| 7 | **N** | The opener's S4 ("compares the two attackers with no defence running") and the heading ("APT attacker model versus baseline attacker") already say all of it. The one word the heading lacks, *no defence*, the opener already gave. |
| 8, 9, 10 | Y | 15 words |

Findings:
1. **§e7.** The sentence says nothing the reader has not just read. It also doubles *with* ("with the baseline attacker with no defence").
2. **Lost content.** The pre-rewrite head tied the section to the two §4.5 metric classes ("how each acts … what it achieves"). Those are §4.5's own glosses (l.5616, l.5708), and they are what the four paragraphs below walk.

Proposal (T2, 19 words; the draft's verb and the earlier draft's two reads):

> With no defence running, this section compares how each attacker acts (Section~\ref{subsec:metrics-behaviour}) and what it achieves (Section~\ref{subsec:metrics-outcome}).

#### U4, §5.2 close: **cut, and move its link into U5**

| §e | Y/N | Reason |
|---|---|---|
| 2 | **N** | It restates a design fact, not what §5.2 established. |
| 7 | **N** | This is the third statement of the reference: the opener's S4, the §5.1 Defence unit (l.6403), and here. |
| others | Y | |

Findings:
1. **§d, the "nagging GPS" problem, and conventions §j8.10.** The same claim appears in three places.
2. **Placement.** The sentence follows an `\owed` about counting dwell-only steps as actions, so it has nothing to do with the sentence before it.
3. **§5.3 still needs the link at its head.** The rewrite dropped the old preamble's "from that attacker's no-defence runs (Section 5.2)". U5's proposal below restores it there, where the reader meets the effects.

Proposal (T1): "…in Chapter 6}. These no-defence runs are the reference for Section~\ref{sec:effectiveness}." → "…in Chapter 6}." (10 → 0 words.)

#### U5, §5.3 preamble: **tighten**

| §e | Y/N | Reason |
|---|---|---|
| 1 | Y | |
| 2 | **N** | Nothing links the effects to §5.2's runs, and that clause was lost in the rewrite. S1 only restates the heading. |
| 3 | Y | S1, plainly |
| 4 | Y | "shows" |
| 5 | Y | "the same by …" (weak) |
| 6 | Y | |
| 7 | **N** | S1 repeats the opener's S5 and the heading. S2 ("Every figure and table shows the APT attacker model beside the baseline attacker") talks about float layout, which every caption already states ("with the baseline attacker dashed for comparison"). |
| 8 | Y | |
| 9 | **N** | (a) The decision rule is declared as "taken to differ from no effect", but the body tests it as "told apart from zero" (l.7907, l.7910, l.8240). That is two phrasings of the one rule. (b) The preamble correctly says "deployment strategy", but the §5.3.3 heading says "execution schemes", and §5.3.3 carries MTDShield (Figure 5.6). The ratified row (Marc 2026-09-02) says *scheme* is never applied to MTDShield. |
| 10 | **N** | 108 words and five sentences, against 30–90 words and two to four sentences. The pooling rule and the decision rule are the shared frame §b preamble 3 licenses; S1 and S2 are not. |
| 11 | n/a | |

Findings:
1. **§e2 / §e7.** Replace S1 and S2 with the one frame fact §5.3 needs, that every effect is taken against §5.2's no-defence runs. This carries U4's link, so U4 can go.
2. **§e9(a).** Declare the rule in the word the body uses: "told apart from zero".
3. **§e9(b), the heading.** Rename §5.3.3 "Defence mechanisms and deployment strategies". **HOLD-FOR-MARC:** this overturns the 2026-09-20 heading ruling ("Mechanisms and schemes" → "Defence mechanisms and execution schemes"). That ruling predates MTDShield joining the subsection on 2026-09-25, and the ratified *deployment strategy* row is the covering term.

Proposal (T2, 99 words; S1 is ch4's §4.5.3 frame "each against the same attacker's runs with no defence" (l.5760), and S2 to S4 are the draft's words):

> Every effect is taken against the same attacker's no-defence runs of Section~\ref{sec:attacker-in-operation}. Where the APT attacker model is one line or column, it pools $c_1$ to $c_4$ with equal weight; $c_{\mathrm{agg}}$ appears separately in Section~\ref{subsec:eff-under-defence}. An effect is told apart from zero when its 95\,\% interval excludes zero, and defences that share a Scott--Knott rank are not told apart (Section~\ref{subsec:metrics-statistics}). Section~\ref{subsec:aio-disruption} shows what a single deployment does to each attacker, Section~\ref{subsec:eff-cross-arm} the NCR reduction of each defence across the deployment interval, and Section~\ref{subsec:eff-under-defence} the same by mechanism, attack profile and deployment strategy.

The 9 words over 90 are the shared frame. The roadmap stays one sentence because it lists three parts, which is an enumeration and not a decorative triplet.

#### U6, §5.3.1 close: **tighten**

§e: 1 Y; 2 Y (states the result); 4 Y; 5 Y (the same attacker-dependence, tested again on NCR reduction); **6 N**; **7 N**; 8 Y; 9 Y; 10 Y (40 words).

Findings:
1. **§e6.** "therefore" presents as a derivation what is a restatement of the three sentences before it. The sentence is also a colon-then-list.
2. **§e7 is licensed here.** Mensh and Kording (conventions §j4) want the paragraph to end on its answer, so the summary sentence earns its place. Only its form needs changing.

Proposal (T2, 34 words; the second sentence is unchanged):

> The host layer costs the APT attacker model the most time, and service diversity costs the baseline attacker the most. Section~\ref{subsec:eff-cross-arm} reads whether the same holds for NCR reduction across the deployment interval.

#### U7, §5.3.2 close: **cut**

§e: **2 N** (it states nothing established; a writer act only); 4 Y; **7 N**; 8 Y; 9 Y; 10 Y.

Findings:
1. **§e7.** The sentence says the same thing three times across the text:
   - the preamble roadmap ("Section 5.3.3 the same by mechanism, attack profile …");
   - this close;
   - §5.3.3's first sentence ("Figure 5.5 shows each mechanism separately, for each attack profile").

   It also leaves out the deployment strategies that §5.3.3 carries.
2. **§b bridge 1.** §5.3.3 depends on no result that this sentence hands over. The preamble has already given §5.3.3 its object.

Proposal (T1): "…close to zero}. Section~\ref{subsec:eff-under-defence} shows each mechanism and attack profile separately." → "…close to zero}." (9 → 0 words.) §5.3.2 then ends on its last observation, which conventions §e allows.

#### U8, chapter end: **keep, no close needed**

Under R1 a close is owed only where chapter 6 depends on a result that the last section does not hand over. The ch6 plan draws on results from all three sections. The opener's "Chapter 6 interprets the results" carries the hand-over.

Two cautions sit outside the close question:
- **The last live sentence is an attribution (S7).** If the `\owed` timing sentence moves to the appendix, as its note suggests, the chapter ends on "which follows from its choice of service diversity at most decisions".
- **The ch6 plan still maps properties to retired sections.** Properties 6 and 7 point to `subsec:aio-capabilities`, stealth reads "nothing; blank by ruling", and adaptivity reads "action mix … recovery time". Ch5 now reports stealth (§5.2 P4) and reads adaptivity on the NCR growth rate and time lost. Re-point these before the ch6 opener is drafted.

---

### 3. Sweep (body prose)

Connective units are excluded (§2). Captions and `\owed` second arguments are not swept.

**Mark-costing**

| # | Line | Sentence (verbatim) | Defect | Edit |
|---|---|---|---|---|
| S1 | 7383–7385 | "Attack rate and attack confidentiality together record stealth (Section 4.5.1), and the APT attacker model scores higher on both." | **False by the section's own table.** The APT attacker model's attack rate is *lower* (11.7–20.7 against 28.4, l.7356; tab:unopposed-summary). | T2: "…record stealth (Section~\ref{subsec:metrics-behaviour}), and the APT attacker model has the lower attack rate and the higher attack confidentiality." |
| S2 | 8044–8045 | "Every reduction falls as the interval grows." | **False universal.** In tab:eff-interval-values, user shuffle against the APT attacker model rises from −0.14 at 50 s to −0.04 at 2 000 s. The pre-rewrite draft carried this exception; the rewrite dropped it. | T2 (the earlier draft's clause): "Every reduction falls as the interval grows, except user shuffle's against the APT attacker model, which rises towards zero." |
| S3 | 7793–7795 | "Adaptivity, the attacker's response to a deployment (Table 3.2), is the one property that needs a defence to be seen." | **False by Table 3.2.** Property 7 (learning, "retained across deployments") and property 8 (scheme awareness) also need a defence (F12). | T1: "is the one property" → "is a property" |
| S4 | 7797–7798 | "…; at 200 s the next deployment arrives before the attacker has recovered from the last." | **Attribution beyond measurement, contradicted by the chapter's own number.** After IP shuffle the baseline attacker "is back to its earlier rate within 125 s" (l.7891), which is inside 200 s. The true reason for reading at 2 000 s is by construction: §4.5.3's 1 250 s window (F13). | T2, using §4.5.3's words (l.5800–5802): "…; at 200\,s the next deployment falls inside the 1\,250\,s over which the rate is read." |
| S5 | 6401–6403 | "Where one interval is reported it is 200 s, the longest Zhang ran, …" | **A false claim the chapter makes about itself.** §5.3.1 reports one interval, and it is 2 000 s (l.7796) (F6). | T2 (the slot plan's word): "Where one interval is tabled it is 200\,s, …". Alternatively, add "; Section~\ref{subsec:aio-disruption} reads 2\,000\,s". |
| S6 | 6389 | "Eleven conditions: no defence, each of the seven defence mechanisms …, and MTDShield." | A number is spelt out at the start of a sentence to dodge the numerals rule (register §b8, supervisor E5). It is also a colon-then-list (F4). | T2: "The 11 defence conditions are no defence, each of the seven defence mechanisms under the single scheme, …, and MTDShield." |
| S7 | 8253–8255 | "Against the APT attacker model, MTDShield stays within 0.12 of service diversity at every interval, which follows from its choice of service diversity at most decisions." | **A mechanism in the results.** It fails §j3's test: the gap could stand with the other 24–30 % of MTDShield's choices doing the work. It also compares across floats (service diversity is in Figure 5.5) and repeats §5.3.2's choice-share fact (l.8063). The handoff's record of Marc's by-construction points lists only the dwell pace and the unmet preconditions. **HOLD-FOR-MARC** if this was his reading. | T1: delete ", which follows from its choice of service diversity at most decisions". |
| S8 | 8239–8243 | "Port shuffle matches it up to 200 s and OS diversity up to 100 s; … The four attack profiles move together under every mechanism, with one exception: $c_3$ separates from the others under the host-layer mechanisms from 500 s." | **Undeclared separation criterion.** The preamble declares two tests: an interval that excludes zero, and a shared Scott–Knott rank. *matches*, *move together* and *separates* use neither. At 200 s, port shuffle shares service diversity's rank (tab:eff-cross-arm), but OS diversity at 50–100 s (0.92–0.93 against 0.99) and $c_3$'s split have no stated test (F22 residue). | **T3, HOLD-FOR-MARC:** state each separation by its rank or interval, which needs per-interval ranks and per-profile intervals not in the text. Then use "told apart" / "not told apart". |

**Minor**

| # | Line | Sentence (verbatim) | Defect | Edit |
|---|---|---|---|---|
| S9 | 7893; 8042; 8127 | "After service diversity the order reverses: …"; "Against the baseline attacker the order is reversed: …"; "The order is not simply reversed: Spearman's ρ …" | The reversal frame appears three times. The §j2 amendment bans inversion openers, and the third instance is a *not X* lead-in. | T1 at l.7893: "After service diversity the order reverses: the baseline attacker drops" → "After service diversity the baseline attacker drops". T1 at l.8127: delete "The order is not simply reversed:" and start "Spearman's $\rho$ …". T2 at l.8042, in the parallel form of the sentence before: "Against the baseline attacker the service layer gives the larger reduction, 0.82 to 0.97 up to 200\,s, against 0.49 to 0.72 for the host layer." |
| S10 | 8058 | "The deployment strategies split the same way." | Figurative, with an unclear referent: which way? The next two sentences state the split. | T1: delete the sentence. |
| S11 | 8047–8050 with 8241 | "User shuffle reduces neither attacker's NCR beyond 50 s, and …" / "User shuffle reduces neither attacker's NCR from 100 s." | The same claim appears in two subsections (conventions §j8.10). "beyond 50 s" also implies it reduces the APT attacker model's NCR at 50 s, where it is −0.14. | T1 at l.8241: delete "User shuffle reduces neither attacker's NCR from 100\,s." T2 at l.8047: "User shuffle reduces the baseline attacker's NCR only at 50\,s (0.47), and against the APT attacker model it is below zero up to 500\,s: …" |
| S12 | 7349–7351 | "…: its ASP is under a quarter of the baseline attacker's, its NCR at most two-fifths, and its MTTC about three times as long." | "at most two-fifths" is false by a hair ($c_2$: 0.20/0.49 = 0.41). It is also a colon-then-list of three. | T2: "On each of $c_1$ to $c_4$ the APT attacker model achieves less than the baseline attacker, and more slowly. Its ASP is under a quarter of the baseline attacker's, its NCR 0.14 to 0.20 against 0.49, and its MTTC about three times as long." |
| S13 | 7353–7355 | "Because a run ends when a target is taken, 40 % of the baseline attacker's runs last to the time limit, against 87 to 95 % …" | The reason is incomplete: 2 % of baseline runs end at NCR 0.8 (§4.5.2, l.5735). The "because" explains the other 60 %, not the 40 %. | T2: "The time limit ends \prelim{40}\,\% of the baseline attacker's runs, against \prelim{87} to \prelim{95}\,\% of the APT attacker model's." |
| S14 | 7355–7357 | "Its attack rate is lower by less, 11.7 to 20.7 actions per 1 000 s against 28.4." | "Its" is ambiguous after a sentence naming both attackers, and "lower by less" is a comparative with a hidden referent. | T2: "The APT attacker model's attack rate is \prelim{11.7} to \prelim{20.7} actions per 1\,000\,s, against \prelim{28.4}." |
| S15 | 7357–7362 | "The model dispatches … so 14 to 28 % … fail before they run, and the attack rate does not count them (…). This follows from a design choice of Chapter 4: the model reuses the simulator's six actions (…)." | Bare *the model* twice (a watched variant in the registry). Four propositions in S1. "This" has no clear referent. Two reasons are given for one fact. The by-construction content is Marc's (handoff, 2026-09-26); only the form is flagged. | T2: "The APT attacker model reuses the simulator's six actions (Section~\ref{subsec:tactic-verb-mapping}) and dispatches them in the order its tactics call them. As a result, 14 to 28\,\% of the actions it dispatches find a precondition unmet and fail before they run; the attack rate does not count them (Section~\ref{subsec:metrics-behaviour})." |
| S16 | 7141–7143 | "…takes 26 to 47 % of its steps in seven tactics that map to no action, from resource development to impact, which the baseline attacker has no counterpart for." | Three stacked post-modifiers. The referent of "which" is unclear (the tactics or the steps). | T1, split at "which": "…from resource development to impact. The baseline attacker has no counterpart for these seven tactics." |
| S17 | 7891–7896 | "…back to its earlier rate within 125 s; … still at 72 % after 1 250 s, …" | The two sentences use different 125 s bin conventions. The first bin after IP shuffle is 22 % and the recovery is in the second (125–250 s). The 72 % is the last bin (1 125–1 250 s), and nothing is read "after 1 250 s" (disruption_numbers.json, relative_pct[6..7], [15]). | T2: "within 250\,s"; "still at 72\,\% at the end of the 1\,250\,s window". |
| S18 | 6650–6651 | "Section 4.5.4 gives the reason for the count, the seeds and the intervals reported." | One word, two senses (register §i4). Two units above, "Where one interval is reported" means a deployment interval; here *intervals* means the 95 % intervals. | T1: "the intervals reported" → "the 95\,\% intervals" |
| S19 | 7907–7910 | "On the service layer, service diversity costs … Port shuffle, OS diversity and user shuffle cost neither attacker …" | User shuffle is not a service-layer mechanism (tab:eff-interval-values groups it under *credentials*), but the sentence follows "On the service layer". | T2: "The other three, port shuffle, OS diversity and user shuffle, cost neither attacker an amount told apart from zero." |
| S20 | 8061–8066 | "MTDShield gives the baseline attacker the larger reduction at every interval (…). It chooses service diversity at 70 to 76 % of its decisions (Appendix E), the mechanism that costs the baseline attacker the most time in Section 5.3.1." | Setting the two facts side by side implies the mechanism (F19 residue). At 2 000 s, neither of MTDShield's cells is told apart from zero (0.06 and 0.03, grey). **HOLD-FOR-MARC** if it is his reading. | T1: delete ", the mechanism that costs the baseline attacker the most time in Section~\ref{subsec:aio-disruption}". T1: "at every interval" → "at every interval to 1\,000\,s". |
| S21 | 8233–8235 | "…and less at longer intervals, IP shuffle keeping the most (0.33 at 2 000 s against 0.16 and 0.17); against the baseline attacker, …" | A tacked-on *-ing* clause. | T2: "…and less at longer intervals. IP shuffle keeps the most (\prelim{0.33} at 2\,000\,s against \prelim{0.16} and \prelim{0.17}); against the baseline attacker, …" |
| S22 | 6324–6327; 6330; 6330–6334; 6394–6395 | F1 "…, with the network regenerated for each seed and the two database hosts … as the target."; F2 "…rather than five."; F3 the three-clause lineage sentence (ruled 2026-09-23); F5 "run as released: …, choosing its own action …" | Unchanged since the first critique: a *with* tail, *X rather than Y*, three clauses, a colon plus an *-ing* tail. | As proposed in critique_ch5.md F1, F2, F3 (flag only) and F5. |
| S23 | 6648–6649 | "…run 1 000 times, ten times the 100 runs per condition of Zhang [11]; …" | A decorative comparison. §4.5.4 now grounds the count (Arcuri and Briand). **Ruled** (E5, 2026-09-23). | **HOLD-FOR-MARC:** T1 delete ", ten times the 100 runs per condition of Zhang \citep{zhang2023}". This overturns the E5 clause, which was added when no basis for the count was cited. |
| S24 | 8232–8264 | (Figures 5.5 and 5.6) | Floats not read (conventions §j8.4). The preamble promises "$c_{\mathrm{agg}}$ appears separately in Section 5.3.3", but no sentence reads $c_{\mathrm{agg}}$. No sentence reads Figure 5.6's two execution schemes by profile either. | T3: one observation each is Marc's to state. Otherwise drop the preamble's $c_{\mathrm{agg}}$ clause. |

**Counts:** 8 mark-costing (S1–S8) and 16 minor rows (S9–S24; S22 groups four carried-over items). HOLD-FOR-MARC: S7, S8, S20 and S23, plus the U5 heading rename.

**Clean categories:**
- no hype adjectives;
- no *Moreover/Furthermore* chains;
- no em-dash interpolations;
- no *substrate*, no L-labels, no US spellings;
- no sentence opening on a numeral except S6;
- *reference* is used only for the no-defence runs (conventions §f2 holds).

**What is left after the rewrite** is accuracy, not rhetoric. The rewrite removed the metaphor (knock-down, part ways, saturate, whiskers), but four sentences now state something the tables contradict (S1, S2, S3, S12), and two carry an unmeasured mechanism (S4, S7).

---

### 4. Priority (at most three moves)

1. **Remove "replaces" from the opener and give it chapter 4's hand-over** (U1). State the link as the model and its metrics, give SQ3 in ch1's words, and add "MTDSim runs either attacker under identical conditions". This is the one breach of a standing Marc ruling in the chapter, and it sits in the chapter's second sentence. Proposal in §2, 85 words.
2. **Fix the four sentences the tables contradict, and the one false self-description.**
   - S1: "scores higher on both" (the model's attack rate is lower).
   - S2: "Every reduction falls" (user shuffle against the model rises).
   - S3: "the one property" (learning and scheme awareness also need a defence).
   - S12: "at most two-fifths" (the ratio is 0.41).
   - S5: "Where one interval is reported it is 200 s" (§5.3.1 reads 2 000 s).

   All five are T1 or T2 edits.
3. **Remove the two unmeasured mechanisms and tidy the §5.3 frame.**
   - S4: replace "before the attacker has recovered" with the by-construction window reason.
   - S7: delete "which follows from its choice …" (HOLD if the reading is Marc's).
   - Cut U4 and U7, and move U4's link into the U5 preamble. Declare the rule as "told apart from zero", the word the body uses.
   - Put the §5.3.3 heading rename ("deployment strategies") to Marc.

---

### 5. Tell audit

Tier audit: two suggestions withdrawn and rebuilt; the rest clean.
- The first U6 proposal kept a colon-then-list ("…depend on the attacker: the host layer …, service diversity …"). It was withdrawn and rebuilt as two coordinated clauses.
- The first S1 suggestion ("…is the stealthier on both: a lower attack rate and a higher attack confidentiality") kept a colon-list. It was withdrawn and rebuilt without the colon.

Every remaining T1/T2 was re-scanned against critique §f and the author's list. None contains:
- *not X but Y* or *rather than*;
- a rule-of-three flourish (the U5 roadmap's three parts are a real enumeration of three subsections, kept from the draft);
- *serves as*, significance words or era vocabulary;
- an *-ing* tail, an em-dash, or brackets in an opening sentence;
- a sentence opening on a numeral;
- content beyond the chapter, ch1, ch4 or the tracked tables.

The colons in S11's T2 ("…below zero up to 500 s: more hosts …") and in the S9 rebuilds are the author's own.
