---
status: open
created: 2026-09-25
---

# Rule on, then apply, the connective-prose proposals for chapters 2–4

Marc rules each proposal below (accept / amend / reject); a session then applies
the accepted ones to `dissertation.tex`, updates the DRAFT STATE comments, and
rebuilds. Every proposal here is a T2 suggestion — **nothing is applied yet**.

## State of play

- **The yardstick exists:** [`../workflows/connective_prose.md`](../workflows/connective_prose.md)
  (committed 2026-09-25), distilled from the published thesis-metatext guidance
  (Evans, Gruba & Zobel 2014; Zobel 2014; Swales & Feak 2012; Hyland 2005;
  examiner-report studies) and a move-coded survey of the lineage's preambles.
  Its one rule: a connective sentence names what a part does for the argument,
  or what it has established — never only its topic.
- **The audit ran:** [`../implementation/connective_prose_audit.md`](../implementation/connective_prose_audit.md)
  — 36 units across chapters 2–4, each with the eleven-item check, a verdict
  and at most one proposal. Tally: 18 keep, 12 tighten, 4 rework, 2 missing.
  Each reviewer read the chapter's DRAFT STATE rulings; where a proposal
  overturns one, it names it.
- **Not yet audited:** chapter 1 (it has no sections; see ruling R2) and
  chapter 5 (opener still a placeholder).

## Rulings needed first (they decide several proposals)

- **R1 — chapter-closing bridges** (`connective_prose.md` §f1). The handbooks
  want every chapter to close on what it established; no lineage document ever
  does. **Recommendation: (b), close only where the next chapter depends on a
  result.** Under (b): ch2 gains one sentence (P15 below), ch3 keeps its close
  (fixed, P2), ch4 gets none (ch5's opener carries the link).
- **R2 — a thesis-structure overview in chapter 1** (§f2). Obligatory in the
  thesis-introduction genre (Bunton 2002; Swales & Feak p. 360); the lineage
  uses a contribution list instead, and ch1's list points only at ch4, ch5 and
  the appendices. **Recommendation:** decide when ch1 is next opened; not
  drafted here.
- **R3 — section-as-agent vs *we*** (§f3). ch4 mixes them. **Recommendation:**
  section-as-agent with operation verbs for previews (*Section 4.2
  partitions…*), *we* for decisions (*We chose each input…*) — the reviewers'
  proposals already follow this.
- **R4 — *axes* → *properties*** (the PROPOSED registry row in
  `terminology.md`). The ch4 opener holds the last own-voice *axes*; ch3's
  heading, Table 3.2 and §4.5.1 say *properties*. Overturns the 2026-08-19
  "eight axes, keep it simple" ruling. **Recommendation: ratify.**

## The proposals, in priority order

### Chapter 4 — the opener's roadmap is stale (highest priority)

**P1 · ch4 opener, rework.** The map omits §4.5 (Figure 4.1 marks it), files
attack profiles under SQ2 (ch1's contribution 1 and §4.2's key say SQ1), calls
MTDSim's defences "our defence mechanisms", restates "the gap motivated" for
the third time without saying what the gap is, and the ruled 2026-09-13
signpost sentence ("the evaluation chapter takes the model as given") is
absent. Proposal (150 words; the either-or sentence moves out because Figure
4.1's caption and §4.4.1 already carry it — overturns its 2026-09-24
placement, not its wording; the last sentence stands in for Marc's signpost
dictation):

> The MTD evaluations surveyed in Chapter~\ref{ch:litreview} leave the performance of MTD against an attacker with a foothold unmeasured. The APT attacker model this chapter defines aims to meet the eight properties of Section~\ref{subsec:attacker-criterion}. The APT attacker model shares the baseline attacker's actions, but its choice of the next tactic is set at runtime by the Petri net of its attack profile. It is a proof of concept, testing whether behavioural fidelity changes existing MTD evaluation.
>
> Sections~\ref{sec:technique-graph} and~\ref{sec:attack-profiles} ground the model in CTI to recover the behaviour of APT attackers in the real world (\ref{sq:capture}). Sections~\ref{sec:petri-formalism} and~\ref{sec:execution} make that behaviour executable as Petri nets and join them to our existing simulator (\ref{sq:model}). Figure~\ref{fig:pipeline} draws each step, and Section~\ref{sec:evaluation-metrics} defines the metrics with which Chapter~\ref{ch:experiments} answers \ref{sq:evaluate}. Every assumption is declared with the symbol it constrains, and Chapter~\ref{ch:experiments} takes the model as given.

### Chapter 3 — the close hands chapter 4 the wrong gap

**P2 · ch3 close (last sentence of §3.3.3), rework.** "this research gap" has
the new Jalowski clause as its referent, not the gap §3.3.3 derives
(performance against an attacker with a foothold goes unmeasured); "attacker
model" should be the registry's *APT attacker model*. The Jalowski clause
stays (pass-5 C20 ruling). Proposal (33 words):

> The literature does not formally define its attacker models \citep[p.~8]{jalowski2026}; that absence and the unmeasured performance of MTD against an attacker with a foothold motivate the APT attacker model defined in Chapter~\ref{ch:attacker-model}.

*Coordination with P1:* P2 carries the forward link and the word
*motivate*; P1's first sentence restates the finding as its link (the Evans et
al. model) without saying *motivates* again. Accept both or neither.

**P3 · §3.3 preamble, tighten.** Its cited survey clause breaks the 2026-09-05
"diagnosis stated once, in the criterion" ruling and the no-citation-in-a-
signpost rule; the §3.2 → §3.3 hinge (effectiveness metrics are computed over
the attacker model) appears nowhere in the connective chain. Proposal (52
words; "two MTD surveys and the APT definition" checked against §3.3.1's first
sentence):

> This section surveys the attacker model that the effectiveness metrics of Section~\ref{subsec:mtd-metrics} are computed over. Section~\ref{subsec:attacker-criterion} derives the properties of a sophisticated attacker from two MTD surveys and the APT definition of Section~\ref{subsec:apt}; Section~\ref{subsec:recent-threat-models} scores recent evaluations against them; Section~\ref{subsec:research-gap} draws the research gap from that scoring.

**P4 · §3.3.3 back-link, tighten (a mis-aimed `\ref`).** The pointer to
§3.2.2 sits on the "logic of the defender" claim, which is §3.2.1's. Proposal
(Marc's wording otherwise untouched; "baked into" and "weakest link" stay as
ruled):

> The assumptions about the attacker are baked into the logic of the defence mechanisms (Section~\ref{subsec:defence-modelling-approaches}). Over the effectiveness metrics the attacker is the weakest link (Section~\ref{subsec:mtd-metrics}): with a weak attacker model the defence mechanisms cannot be evaluated, because the metrics are intertwined and computed over the attacker model.

**P5 · §3.2 preamble, tighten.** The third of four "This chapter/section
surveys…" openers in the chapter, and its S1 repeats the ch3 opener. Opens on
the frame instead (31 words; "involves … steps" is Marc's dictated phrase):

> Evaluating a defence mechanism involves three steps. The mechanism is designed under a defence modelling approach (Section~\ref{subsec:defence-modelling-approaches}), instrumented with metrics (Section~\ref{subsec:mtd-metrics}), and evaluated under an evaluation method (Section~\ref{subsec:evaluation-methods}).

**P6 · ch3 opener, tighten.** The three section clauses are topics under one
verb. Proposal (69 words; S1 unchanged; keeps the "last because" dependency):

> This chapter surveys the literature on evaluating MTD against APT attackers, along the three sub-questions of Chapter~\ref{ch:intro}. Section~\ref{sec:apt-survey} surveys how APT attacker behaviour is recovered from CTI (\ref{sq:capture}); Section~\ref{sec:mtd-evaluation-survey} how the field evaluates a defence mechanism, and where the attacker model enters that evaluation (\ref{sq:evaluate}); Section~\ref{sec:mtd-attacker-models} scores the attacker models of recent evaluations (\ref{sq:model}), last because that scoring states the gap that motivates Chapter~\ref{ch:attacker-model}.

**P7 · §3.1 close, tighten.** Two X-not-Y constructions in consecutive
sentences, the claim buried in a 45-word sentence. Split at the ruled colon;
the second becomes "outside MTD evaluation" (audit §C5 for the full text).

### Chapter 4 — the rest

**P8 · §4.4 preamble, rework (266 → 93 words).** About a third is connective;
the rest restates the §4.3 bridge, the opener, the caption and §4.4.1 (the
either-or design is stated five times by §4.4.1). Proposal — overturns the
2026-08-19 spine sentence's colon-list (the §4.3 bridge lists the inputs with
their symbols one line earlier) and cuts "We scoped it down", which the §4.4.1
ceiling paragraph carries:

> This section integrates the Petri nets $\mathcal{N}_c$ with MTDSim through the join. A Petri net run on its own produces a timeline of what the attacker did, with no input from the simulator; the join makes the run two-way. Section~\ref{subsec:runtime-mechanics} gives the runtime mechanics of the join, and Sections~\ref{subsec:dwell-times} to~\ref{subsec:failure-matrix} declare the three inputs the join carries. We chose each input to the best of our judgement after consulting the literature; whether any conclusion of the evaluation depends on where a chosen value sits is the question Appendix~\ref{app:sensitivity} answers.

**P9 · §4.5 preamble, tighten.** No link to SQ3; the dependency between the
behaviour metrics (no defence) and the effectiveness metrics (against those
no-defence runs) is left to the lead-ins. Proposal (91 words; also fixes
*this thesis*):

> This section defines the ten metrics with which Chapter~\ref{ch:experiments} answers \ref{sq:evaluate} (Table~\ref{tab:metrics}). The behaviour metrics of Section~\ref{subsec:metrics-behaviour} are read with no defence running, and the effectiveness metrics of Section~\ref{subsec:metrics-effectiveness} compare each defence with those no-defence runs. A metric the field defines is used as defined; where this dissertation adapts or introduces a metric, its definition states the change and why it is needed. Every metric is computed over a \emph{cell} $\mathcal{R}$, the runs of one attacker under one condition at one deployment interval, with $r \in \mathcal{R}$ one run.

**P10 · §4.3 close → §4.4, tighten.** Term mismatches ("parameters", "the
timings $\mu_p$", and "the exponential defence of the dwell times", which is a
justification, not something the join supplies). Audit §U6.

**P11 · §4.1 close, tighten.** Future tense and a dangling "This"; reason
before pointer. Audit §U2.

**P12 · §4.4 close, tighten.** "This is … this is … these" three paragraphs
from the failure matrix; nouns named. Audit §U8.

### Chapter 2

**P13 · ch2 opener, rework.** No link to the research question; S1 restates
the heading; same skeleton as the ch3 opener. Proposal (62 words; built from
SQ2 and SQ3's own words; avoids "beside", ruled wrong 2026-09-24):

> The APT attacker model is executed inside MTDSim, the MTD simulator this dissertation inherits, and compared with the simulator's baseline attacker. This chapter describes MTDSim and the defence it models. Section~\ref{sec:mtd-concept} defines moving target defence and its organising questions (what to move, how to move it, and when); Section~\ref{sec:mtdsim} describes the simulator's modules and classifies its defence mechanisms by the same questions.

**P14 · §2.2 preamble, tighten.** The "what … what … what" question list is a
run of three (voice.md §d licenses pairs) and a colon-list, and names topics.
Keeps the 2026-09-02 placement and content, overturns its interrogative form;
the Table 2.2 sentence (ratified 2026-09-23) is verbatim. Proposal (90 words):

> MTDSim is a discrete-event simulator built to evaluate defence mechanisms singly and in combination \citep{brown2023}. Figure~\ref{fig:mtdsim-model} draws its three modules and the couplings between them. Section~\ref{subsec:network-model} describes the network, Section~\ref{subsec:defence-mechanisms} the defence mechanisms and the deployment strategies that schedule them, and Section~\ref{subsec:attacker-model} the baseline attacker they are evaluated against. The simulator is the product of four studies over one evolving codebase; Table~\ref{tab:mtdsim-lineage} lists what each work added, and each addition is described where it is used. Table~\ref{tab:lineage-configurations} gives the configurations the studies evaluated on.

**P15 · ch2 close, missing (only if R1 = a or b).** Chapter 2 ends on the
disruption placeholder; §3.3.2 scores the baseline attacker §2.2.3 describes,
and nothing says why chapter 3 follows. Proposal (21 words; placed after the
drafted disruption paragraph):

> Chapter~\ref{ch:litreview} scores the scripted baseline attacker and the attacker models of recent MTD evaluations against the properties of a sophisticated attacker.

## Mechanical items (T1 — apply on a blanket accept)

- ch2 §2.2.2 close: cut ", such as an IDS-based scheme," (an example tail and a
  one-use unexpanded acronym).
- ch3 §3.1 preamble: "the methods that reconstruct" → "the attack-profiling
  methods that reconstruct" (§3.1.3's heading term).
- ch4 §4.5: *this thesis* → *this dissertation* at three sites (the ratified
  row).

## Flagged, not drafted (content — Marc's)

- **ch2/ch3:** a ch3 comment says "why the network model is not surveyed"
  now lives in the ch2 preamble; it does not. Decide which chapter states it.
- **ch4 §4.4.1:** "it is extendable and modular: our Petri nets can be mapped to
  anything" is a value close claiming more than the chapter shows.
- **ch4 §4.4 and §4.4.2:** "the mean dwell $\mu_p$ of Equation~\ref{eq:gspn}"
  points at an equation that does not contain $\mu_p$.
- **ch4 §4.3 head link:** "a data structure to pipe in the attack profiles" is
  weaker than the section's job (Figure 4.1's verb is *make executable*); ruled,
  flagged only.
- **ch3 §3.1.2 close:** "stable enough to model an attacker against" has had no
  citation since the Sadlek leg was cut.
- **Stale comments:** the ch2 opener's DRAFT STATE (claims an inherit/build
  opposition the prose no longer has); the MTD double expansion (ch1 and §2.1).

## Recommended approach

Rule R1–R4 first; then walk P1–P15 in order (P1 and P2 together). Apply
accepted proposals as line-level edits, one commit per chapter, each updating
the unit's DRAFT STATE comment (`SESSION-GENERATED / RATIFIED <date>`). The
alternative — a voice pass (pass 6) over each chapter first — was not chosen:
the connective units are few and self-contained, and pass 6 would re-flag what
is ruled here.

## Validation gate

- Every accepted proposal is in the tex; every rejected one is recorded as
  rejected in its DRAFT STATE comment so no later pass re-flags it.
- `connective_prose.md` §e re-run on each changed unit: no *N*.
- `latexmk -pdf dissertation.tex` builds with no undefined references;
  `python tools/term_screen.py census properties axes` shows no own-voice *axes*
  if R4 is ratified.

## Hard constraints

- Nothing unratified touches the tex (drafting_pipeline.md; connective prose is
  generable but ratify-on-read).
- Chapters 1–3 impersonal; *we* from chapter 4 (academic_register.md §b2).
- A concurrent session works on `chore/ch5-setup-defence-and-prose`; re-read the
  current tex before applying (line numbers in the audit are that branch's after
  commit 452008d5; cite units by `\label`).

## Reading list

- [`../workflows/connective_prose.md`](../workflows/connective_prose.md) — the rule and the check.
- [`../implementation/connective_prose_audit.md`](../implementation/connective_prose_audit.md) — per-unit checks and the full text of P7 and P10–P12.
- [`../workflows/voice.md`](../workflows/voice.md) §d, §h and [`../workflows/terminology.md`](../workflows/terminology.md).

## Out of scope (explicitly)

Body paragraphs; chapter 5's connective units (its opener is a placeholder —
audit it with the same check once drafted); chapter 1's structure overview
until R2 is ruled.
