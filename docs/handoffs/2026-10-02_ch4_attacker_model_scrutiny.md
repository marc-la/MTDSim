---
status: open                  # 2026-10-02: ROUND 1 APPLIED on Marc's accept-all ("I accept all changes"); his section-by-section acceptance pass is next
created: 2026-10-02
updated: 2026-10-02            # supersedes the PRELIMINARY ledger of the same name (commit 3bd22b81); §11 lists what changed
companions: ../workflows/chapter_scrutiny.md, ../workflows/model_chapter_conventions.md (new, the yardstick), ../workflows/literature_conventions.md, ../implementation/apt_model_criterion.md, ../workflows/terminology.md, ../workflows/critique_protocol.md (tiers), 2026-09-25_ch4_mark_risk_ledger.md (its open M entries are absorbed here)
---

# Chapter 4 scrutiny: describe the model that ran, once, in the chapter's own words

**Goal.** Bring chapter 4 (APT attacker model) to the point where every sentence
does something chapter 5, chapter 6 or the examiner needs, and where the model it
describes is the model that ran. Each entry below is a proposal for Marc to rule
on. Nothing is applied until he rules. His dictated units change only by the
deletions and merges he ratifies; any rewording is his.

## 0. What was run

The full procedure of [`chapter_scrutiny.md`](../workflows/chapter_scrutiny.md):

- **§0 load.** The six read-first files and voice.md §(0); the ch4 notes README
  (stale, §10); the terminology registry, connective_prose.md, critique_protocol.md,
  draft_scrutiny.md's corpus map, figure_table_conventions.md and the pitfall
  catalogue.
- **§1 read.** The tex l.3451–5208, prose and `%` trails. PDF pages 16–32 rendered
  from `dissertation.pdf` (built 18:01, after the tex's last change at 18:00; the
  physical offset is +9) and read as images.
- **§2 yardstick.** The named yardstick (`literature_conventions.md`) carries the
  field's norms but not the genre's: purpose, examiner expectations, structure,
  failure modes, checklist. A methods-chapter yardstick was commissioned and
  distilled into [`model_chapter_conventions.md`](../workflows/model_chapter_conventions.md)
  (EGZ ch. 7, Zobel, P&S ch. 8, ODD 2020, STRESS, Sargent, Law, examiner studies,
  UWA/Cambridge/Edinburgh); registered in docs_map.md and the procedure's table.
- **§3 audit.** A read-only agent ran the forward and backward audit (A–F). Its
  report is the evidence behind the D, E and lean-test entries below; the
  findings this ledger relies on were spot-verified (§9).
- **§4 verify.** Every X entry is checked against its owner: the code and data
  (a second agent, with file:line), the extraction or source, or the registry.

### Measurements (prose words; floats, captions, display maths and headings excluded)

| Unit | Prose | Captions | Floats |
|---|---:|---:|---:|
| Opener | 157 | 46 | Fig 4.1 |
| §4.1 Attack graph construction | 501 | 33 | Fig 4.2 |
| §4.2 Attack profiles by objective | 466 | 29 | Fig 4.3 |
| §4.3 Generalised stochastic Petri-net formalism | 1 153 | 151 | Fig 4.4, Tab 4.1 |
| §4.4 preamble | 235 | 0 | |
| §4.4.1 Runtime loop | 588 | 197 | Fig 4.5 |
| §4.4.2 Tactic dwell times | 386 | — | Tab 4.2 (generated) |
| §4.4.3 Tactic-to-action mapping | 176 | 43 | Fig 4.6 |
| §4.4.4 Failure matrix | 419 | 0 | |
| §4.4.5 Vulnerability memory | 215 | 0 | |
| §4.5 Evaluation metrics (all) | 1 194 | — | Tab 4.3 (generated) |
| **Chapter** | **≈5 490** | **≈500** | **9** |

The writing-guide ledger gives the chapter 1 500 words (6 units) plus one claimed
unit of overdraft (2026-09-08). It predates §4.5 moving in (≈1 200) and §4.4.5
(≈215). (The preliminary pass measured 5 312 with a stricter tokeniser; the
difference is symbols counted as words, not new text.)

---

## 1. The yardstick, in five lines

- **Purpose.** Chapter 4 presents and argues for the APT attacker model so that a
  reader could rebuild it: what it is made of, how it runs, what it was given
  rather than measured, and the metrics chapter 5 reads (EGZ p. 83; Zobel p. 118;
  ODD §1).
- **Context.** One level above the code: the design, each choice with its reason
  once, each rejected alternative in one clause (ODD §4.2), and the simulator
  referenced, not re-described (STRESS §4.2).
- **Audience.** A fourth-year CS student arriving from chapters 2–3 with the
  baseline attacker, attack actions, disruption, the confusion penalty, ATT&CK,
  Attack Flow, attack profiling and the eight properties; and an examiner checking
  that every choice is justified and that "declared equals done" (Mullins & Kiley
  p. 375).
- **The lean test.** A fact stays only if chapter 5, chapter 6 or a later section
  of this chapter leans on it, and nothing is re-told that chapters 1–3 already
  established. A simplification is owned once, here; a limit of the findings is
  §6.5's.
- **The float test.** Each float carries what the prose points at and shows the
  model that ran. Its caption says how to read it; the account of what happens is
  the prose's.

## 2. Verdict and the three moves that matter most

**Chapter verdict: the right model, described twice over and in places not as it
ran.** The formal core holds: §4.3's definition, Figure 4.4, §4.4.4 and §4.5 read
as finished method prose, and every number checked in them is right (§9, last
paragraph). Three things cost marks.

1. **In six places the chapter describes a model other than the one that ran or
   that its appendix records** (X1–X5b): the classification rule (terminal tactic,
   where Table B.3 adopts the stated objective), the stopping rule (stated three
   ways; the code runs §4.5's), the pre-intrusion overlay (added to two profiles,
   not "each"), the corpus span, the dwell-time claim against chapters 1 and 3, and
   the property 7 claim against Table 3.2. Three appendix pointers promise reasons
   Appendix B does not hold (X6). This is the examiner's "declared equals done"
   check.
2. **It re-tells what chapters 2 and 3 established** (≈350 words): Attack Flow, CTID
   and the case against automated profiling (ch3 §3.1.3), the confusion penalty and
   disruption (ch2 §2.2.3), Zhang's halving and the CVSS odds (ch2). The yardstick's
   lean test and STRESS §4.2 both say: reference the inherited, describe the
   extension.
3. **It states each caveat and preview several times**: "our judgement" nine times,
   the ablation and sensitivity previews six times, roadmaps four times, fidelity
   versus coverage five times, the dwell-only no-verdict rule five times (audit
   D3). State each once, where it applies.

**Projected.** The cuts in §7 take ≈850 words (5 490 → ≈4 640) without touching a
must-carry. The rest of the distance to G1's target is Marc's own pass on §4.3 and
§4.4.1.

---

## 3. Chapter-level findings (G)

**G1. The budget: re-rule it (Marc's call).** 1 500 + 250 was set for four
sections before §4.5 (≈1 200) and §4.4.5 (≈215) moved in. No source gives a model
chapter's share (`model_chapter_conventions.md`, sources note).
*Recommendation:* ratify **≈3 000 for §4.1–§4.4 and ≈1 000 for §4.5**, funded by
the experiments chapter (which handed §4.5 its metrics), and record it in
`_writing_guide.md`'s reallocation record. Holding 1 750 means cutting ≈3 700
words, must-carries with them.

**G2. Declared equals done (X1–X6).** The examiner checks that the model described
is the model that ran (Golding §8; checklist item 15). Six descriptions fail that
check, and the opener's ruled promise, "Every assumption the model makes is stated
where the symbol it constrains is declared" (l.3711), is false until X6 is
closed. These come first, before any wording.

**G3. Inherited material re-told (the backward lean test).** Each item below is
already defined where the reader met it. Chapter 4 should point, not re-describe:

| ch4 lines | Already in | Entry |
|---|---|---|
| 3744–3749 Attack Flow, CTID, what a flow records | ch3 §3.1.3 l.1529–1535 | A1 |
| 3773–3778 automated (NLP) profiling ruled out | ch3 §3.1.3 l.1520–1527, which makes the choice | A1 |
| 4518–4521 disruption fails the attack action | ch2 l.858–866 | R3 |
| 4578–4584 the 20 s confusion penalty | ch2 l.863–864 | R5 |
| 4933–4934 Zhang's halving | ch2 l.854–855; ch3 l.3235 | V3 |
| 4941–4944 exploit odds from CVSS complexity | ch2 l.686–689 | V3 |

**G4. Each caveat and preview once.** The repeats (audit D3, verified on the page):

- *Our judgement*: the §4.4 preamble's four-bases paragraph (l.4413–4424) is the one
  list. It is re-told at l.4643, 4658–4659, 4775, 4860–4861, 4882–4883, 4891–4892,
  4955. Keep the list and each subsection's single clause where the value is
  declared; cut the restatements (D1, M1, F2).
- *Ablation and sensitivity previews*: l.4145–4146, 4429–4432, 4659–4660,
  4812–4813, 4887–4891, 4960–4964. Each subsection keeps its one pointer to the
  test of its own value; the preamble's list goes (I3).
- *Roadmaps*: l.3704–3713 (ratified opener), 4148–4150 (float pointers, keep),
  4285–4290 (ratified bridge), 4362–4367 (ratified preamble). Keep all four: they
  are ruled connective prose and each points at different things. Listed so that
  no further roadmap is added.
- *Fidelity versus coverage*: five tellings (l.3776–3778, 3789–3791, 3794–3796,
  3896–3897, 3916). Keep one, the resolution sentence (A2).
- *Dwell-only means no verdict*: l.4116–4117 (the definition of none), 4130–4132,
  Figure 4.5's caption, 4527–4533, 4779–4780. Keep the definition and §4.4.1's
  cost sentence (R4).
- *Not real-world*: the dwell must-carry (l.4746–4747) and the failure matrix's
  (l.4891–4892). One question (F3).

**G5. One term per thing, against chapter 3 and the registry.** Four collisions a
reader meets at the chapter boundary:

- **Attack profile.** Chapter 3 defines it as "the product of attack profiling"
  (l.1515–1516), which is one recovered order, so one flow. Chapter 4 uses it for
  an objective's subgraph of many flows (l.3906–3915). One clause in §4.2 binds
  the two ("an attack profile here combines the flows of one objective"), or ch3's
  definition widens. Marc's ruling (C1).
- **The objectives.** Chapter 3 names three: exfiltration, *impediment*,
  positioning (l.1091–1092, Alshamrani). Chapter 4's four are exfiltration,
  *impact*, double extortion, none. Nowhere are the two lists joined (C2).
- **The lifecycle.** Chapter 3 gives Alshamrani's five stages (l.1112–1114);
  §4.4.4 gives four consensus stages citing Alshamrani among others (l.4865–4867),
  and Figure 4.6 draws them before §4.4.4 defines them (C3).
- **Registry breaches** (all ratified rows): "threat-model parameters" (l.4891,
  row 68); "duration" and "all the tactic timing" for dwell time (l.4450–4451,
  row 54; the latter is a 2026-08-20 ruled wording, so the conflict is surfaced,
  not resolved); "compiles to a GSPN" for a profile's own net (l.4059, row 47);
  the failure matrix's long form never given (row 53); *flow* versus *attack flow*
  (≈22 sites; PROPOSED row 105 is still unruled, so this waits on that ruling).
  Inside chapter 4: *APT group* (l.3931) and *operator* (l.4086, 4422, 4434) name
  one thing; *sink* and *structural dead end* name one thing (l.4567–4568).

**G6. The chapter's appendix leans on vocabulary chapter 4 never gives** (flag,
out of chapter): Appendix B says "substrate" (three rows of Table B.5), "outcome
overlay" and "failure weight set" (Table B.6), "five routing nets … (323 in all)"
after $c_{\mathrm{agg}}$ was retired 2026-10-02, codenames (`v1_ckc_total`,
`v4_failure_only`, `objective_none_c2`), "ASR" for ASP; Appendix C says "distinct
hosts reached" for what §4.5 calls NCR. Appendix B is chapter 4's supplement, so
these are next after the body.

## 4. Structure and headings (S)

**S1. §4.1 opens on what the attack graph is.** Today the definition arrives at
l.3817, after the corpus, the alternatives, the aggregation and the resolution.
Move l.3817–3822 ("The attack graph, the aggregate of the 38 attack flows, is a
weighted directed graph …") to open the section; the corpus sentence (A1) follows.
T1 (sentences unchanged). Matches yardstick §(c)4 (design, then rationale).

**S2. §4.2 opens on the partition.** Lead with the four profiles and their counts
(l.3911–3915), then how flows were classified (X1's corrected sentence), then why
objective and not motivation (l.3885–3891), then operator concentration. T1.

**S3. §4.3: the pre-intrusion overlay is used before it is defined.** $M_0$ (l.4090)
says "(defined after Table~\ref{tab:gspn-notation})"; the overlay paragraph is at
l.4256. Move it to directly after the enumerated list, so $M_0$ points back. T1.

**S4. §4.4.1 holds seven topics in 588 words**, ordered by drafting history, not by
the loop: replaced cost; targeted scenario; verdict; dwell-only; sink-retrace and
stall; what the simulator owns; nothing carried between runs; the ceiling. Keep one
subsection, ordered as the loop runs: the clock (cost replaced), the verdict
(incl. dwell-only), the dead end, what the simulator owns, then the ceiling. The
targeted-scenario sentence moves to §4.4's preamble or stays first; its run-end
clause goes (X2). T1.

**S5. No chapter close.** Correct as it stands: connective_prose.md §(f)1 rules
"chapter 4 has no close, because chapter 5's opener carries the link", and
chapter 5's opener does ("Chapter 4 builds the APT attacker model and defines the
metrics …", l.5279). The preliminary ledger's C3 asked for a close; withdrawn.

**S6. Headings.** All five section headings and the five §4.4 subsection headings
follow the registry (row 47) and the heading conventions. The affinity board's open
item on the §4.4 subsection headings (its §6) stands; nothing here moves them.

## 5. Figures (F)

Each figure was read on the rendered page against the pitfall catalogue
(`diagram_best_practice.md` §4) and the registry.

- **F1. Figure 4.1 (overview), keep; one label.** The MTD → Network arrow reads
  "rewrites". *Reconfigure* replaced *rewrite* on the surface (registry row 64,
  2026-09-30; Figure 2.1's arrow already says it). Regenerate
  (`tools/ch4_overview_figure.py`). The figure meets yardstick §(e)1. Its caption
  is still DRAFT STATE (session stand-in): Marc's ratify-on-read.
- **F2. Figure 4.2 (attack graph construction), keep.** Its "88 % at technique
  level, 39 % at tactic level" is the number A2 needs; the prose may cite the
  figure instead of restating it. Caption DRAFT STATE.
- **F3. Figure 4.3 (profiles), keep.** Caption DRAFT STATE.
- **F4. Figure 4.4 (one tactic of a Petri net): the caption does the legend's
  work and the prose's.** Panel (a) carries a legend for every mark; the caption
  decodes them again (P12: four "X is Y" decodes), then narrates the 0.062 →
  0.750 account §4.4.4 gives (l.4874–4878). Cut the caption to how to read it:
  what (a), (b) and (c) show, that the blue column is $W_c(t_{pq} \mid
  \mathrm{failure})$, and the base weights stand under success. ≈−60 caption
  words. The prose keeps the worked example (examiner feedback asked for
  examples).
- **F5. Figure 4.5 (runtime loop): one stale label, an owed glyph, and the account
  lives in the caption.**
  - The MTDSim band reads "Attacker / Network / *Defender*". The module is *MTD*
    (Figure 2.1; Figure 4.1; registry row 73 bare *defence* sweep, 2026-09-30).
    P17 (family balance).
  - "The join's three declared inputs": the vulnerability memory is owed on the
    next regeneration (OWED 2026-09-28, l.4511).
  - The caption (197 words) narrates the six numbered steps. The 2026-09-08 pass cut
    the loop-as-prose paragraph because the figure carried it; the procedure (§7:
    "Captions say how to read the figure. The account … lives in the prose") and
    the yardstick (§(e)2: numbered steps in prose, not a flowchart) both point the
    other way. *Proposal:* the six steps become a short enumerated list in §4.4.1
    (≈+90 prose words), and the caption keeps the bands, accent versus grey, and
    "the numbers are the steps of Section 4.4.1" (≈−130 caption words). **Re-opens**
    the 2026-09-08 cut on merit. Run `scrutinise-figure` with the regeneration.
- **F6. Figure 4.6 (mapping), keep; one antecedent.** Its stage bands
  (preparation, intrusion, post-intrusion, objective) appear before §4.4.4 defines
  the stages. Either the caption points forward ("Bands are the lifecycle stages of
  Section~\ref{subsec:failure-matrix}"), or C3 places the stage definition earlier.
  "no mapping (7 of 15)" is verified.

## 6. Tables (T)

- **T1. Table 4.1 (symbols): two wrong rows and five unused ones.**
  - $v \in V$ says "declared in §4.4.1"; $V$ is declared at Equation 4.3 (§4.3,
    l.4113). Re-point.
  - $\mathcal{N}_c$ says "Eq. 4.1"; Eq. 4.1 is the generic $\mathcal{N}$, and
    $\mathcal{N}_c$ is declared in §4.3's list (l.4059). Re-point to §4.3.
  - $R$, $d$, $\gamma$, $\delta$, $z$ are used nowhere in the chapter's body (the
    2026-09-26 rewrite of §4.4.4 cut them). Move the two rows to Table B.6's
    caption or cut them. A notation table lists the chapter's symbols, and five
    of its fifteen rows are not the chapter's.
- **T2. Table 4.2 (dwell catalogue), generated: fix in
  `tools/dwell_catalogue_tables.py`.**
  - The caption says "Values are emitted from the declared catalogue
    (v0-uncalibrated)": a repo version string and repo register on the surface
    (voice.md §e; the registry's screen finding of 2026-09-22 flagged the same
    pattern in Figure 4.5). Cut the sentence.
  - "the mean dwell $\mu_p$ of Equation 4.1": $\mu_p$ is not in Eq. 4.1; it enters
    at §4.3's item 5 ($W_c(\tau_p) = 1/\mu_p$). Re-point to Section 4.3, as
    Table 4.1 does. The same wrong pointer is in the §4.4.2 prose (D2).
  - It is the one chapter 4 table outside the house style (`\tablestyle`,
    stripes; figure_table_conventions §k; commit abdda86b swept the others).
- **T3. Table 4.3 (metrics), keep.** The source column carries the s45
  verification's fixes ("this dissertation, after [26]").

---

## 7. Prose ledger

Line numbers are as of 2026-10-02 and drift with edits. Δ is approximate. Tiers
follow `critique_protocol.md`: T1 is a deletion or move, T2 a suggestion built
from Marc's words that he re-words or ratifies, and T3 is content. "Re-opens" names
the ruling an entry overturns on merit.

### Opener (157): keep

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| O1 | keep | 0 | Ratified connective prose (2026-09-26). Its last sentence ("Every assumption … is stated where the symbol it constrains is declared") holds only once X6 closes (G2). "our existing simulator" is a do-not-re-flag ruling |

### §4.1 Attack graph construction (501 → ≈320)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| A1 | l.3744–3778, the whole first paragraph ("We made the attack graph using Attack Flow. Attack Flow is maintained by the Center for Threat-Informed Defense (CTID), which sits under MITRE Engenuity … Attack Flow maintains a documented attack-behaviour corpus spanning 2017 to 2024. Other approaches were considered … NLP-based approaches we ruled out as a class … The strength of using Attack Flow's corpus is that a human analyst drew every dependency, so there is a degree of fidelity that other approaches could not provide.") → *suggestion:* "We built the attack graph from CTID's corpus of flows (Section~\ref{subsec:profiling}), because a human analyst drew every dependency in it. Co-occurrence mining gave low coverage and keyword mining poor fidelity (Appendix~\ref{app:cooccurrence})." | −115 | T1 + T2. G3: ch3 §3.1.3 introduces CTID, the corpus and what a flow records, and makes the manual-over-automated choice with the same two citations (l.1520–1535). Removes X3 (the span) and the Engenuity attribution (X7). Absorbs M19, M24, M27. The trail's AVAILABLE argument (co-occurrence can express no loop) stays Marc's call |
| A2 | l.3780–3798: cut "Instead of using each incident independently of the others --- where there is little insight in the corpus ---"; cut "preserving the logical AND/OR structure. But aggregation makes the logical AND vacuous, because there are many OR paths which an attacker can traverse."; "The node resolution, tactic or technique, trades fidelity for coverage: having chosen the input for its fidelity, we chose the resolution for coverage. We chose tactic, because 88\% … But once aggregated, the tactic-to-tactic edges had much greater coverage, and we judged this trade-off … necessary to capture the generalised behaviour of APT attackers." → *suggestion:* "We chose tactics as the nodes, trading fidelity for coverage: 88\,\% of the technique-to-technique edges came from a single flow, against 39\,\% of the tactic-to-tactic edges (Figure~\ref{fig:attack-graph-construction})." | −70 | T1 + T2, G4. The AND point is told three ways with two reasons (audit D1.17); §4.3's one-token sentence (l.4098–4100) is the one with its mechanism and stays. 39 % is Figure 4.2's own figure. M25 |
| A3 | S1's move: l.3817–3822 opens the section | 0 | T1 |
| A4 | l.3822–3826 "We are using human-analyst-drawn dependency graphs, and this is sparse input data. The edge weight is a recurrence value; therefore, we cannot rely on these weights alone to drive the APT attacker model. Instead, we treat the attack graph as a skeleton of behaviour." → *suggestion:* "The corpus is sparse, so an edge weight counts flows; it does not on its own drive the APT attacker model (Section~\ref{sec:petri-formalism})." | −20 | T2. "Skeleton of behaviour" is a metaphor doing a claim's work (connective_prose §a). Keeps "alone", which is what makes the sentence consistent with $w_c$ (audit D1.16) |
| A5 | l.3830–3836 "Another limitation we encountered was an issue with a lack of pre-intrusion dependencies: any tactics before initial access were sparse compared to the rest of the corpus." → "The corpus is sparsest before initial access."; "passive recon" → "passive reconnaissance"; cut "Hence," | −20 | T1 + T2. M41, M42 |
| A6 | l.3843 "The sparsity is persistent across CTI" | 0 | T3 flag. Uncited empirical claim inside ratified connective prose (2026-09-26). Cite or soften; the citation is Marc's, not supplied |

### §4.2 Attack profiles by objective (466 → ≈360)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| B1 | l.3863–3867 "The literature tells us that APT attackers are not a homogeneous group, and so they are distinguished by campaign-level intent. We cannot produce an APT attacker model that could be considered behavioural, because the attack graph carries so many different motivations and objectives which influence behaviour \citep{alshamrani2019}." → *suggestion:* "APT attackers differ by objective, and the objective shapes behaviour \citep{alshamrani2019}; one model of the whole attack graph would mix them." | −25 | T2. As written the sentence says the dissertation cannot build a behavioural model at all. Chapter 3 already argues the objective (l.1086–1092); this sentence only needs the consequence for the graph. C2 joins the objective names |
| B2 | l.3885–3886 "Motivation is something that we cannot ascertain. We can see what an APT group did; this is an analyst inference." → M32's suggestion: "Motivation is an analyst inference; what an APT attacker did is recorded." | −8 | T2. M32: "this" attaches to the observed act, so the sentence says the opposite of what it means. "STIX" is unexpanded and is not defined in ch1–3 (audit F): expand once or say "the ATT&CK data set" |
| B3 | l.3893–3903, the classification paragraph | see X1 | **X1.** The paragraph describes the rejected classifier. Its replacement is X1's; the "composite data … coverage is an issue" sentence (the fourth fidelity/coverage telling) goes with it |
| B4 | l.3906–3919: S2's move; cut "Hence,"; resolve the standing [3b] ("based on the shape of our corpus" vs "based on the terminal tactic", now moot under X1); cut "There are four, and"; l.3915–3917 "We have judged this partitioning the right balance for corpus coverage: the smallest attack profile has a minimum of five flows, which provides enough coverage." → "The smallest profile, $c_4$, holds five flows (Appendix~\ref{app:rejected-partitions} compares finer partitions)." | −30 | T1 + T2. M31. Verified: after one flow per operator the profiles carry 14 + 6 + 5 + 4 = 29 weighted flows (`src/mtdsim/l2_subgraph/dedup.py:25`), so $c_4$ runs on four. The nets run on the 29, so the sentence should give both ("five flows, four after one flow per operator") or point at §4.3's 29 |
| B5 | l.3929–3935, operator concentration: keep | 0 | Marc's pass-5b sentence and the Conti example (the section's one concrete case). "APT group" here and "operator" in §4.3 name one thing: pick one (G5) |

### §4.3 Generalised stochastic Petri-net formalism (1 153 → ≈990)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| P1 | l.3971–3986 "We needed a data structure to pipe in the attack profiles as an input, and this is what the Petri nets provide. We ruled out attack graphs … which provides the immediate transitions we are using. There is also a large precedent …" → *suggestion:* "The attack profiles need an executable form, and a Petri net gives one. We use the generalised stochastic Petri net (GSPN) \citep{marsan1984}, whose immediate transitions model the choice of the next tactic: a stochastic Petri net times every transition, a deterministic and stochastic Petri net adds a fixed delay the model does not need, and attack graphs and directed acyclic graphs carry no timing (and the latter no cycles). Stochastic Petri nets have precedent in MTD evaluation \citep{cai2016, chobenasher2018, mendonca2023}." | −20 | T2. The choice first, each alternative one clause (yardstick §(c)4; the 2026-08-17 contract, "a sentence each"). M12, M18. "large" goes (three citations). DAG expanded |
| P2 | l.4061–4064 "one decision place $\hat{p}$ for each (a vanishing place, left in zero time)" | 0 | T2. *Vanishing* and *tangible* are properties of markings in the definition four lines up (l.4051–4054), not of places (audit C1). *suggestion:* "one decision place $\hat{p}$ for each, which the token leaves in zero time". Same at "one tangible place $p$" → "one place $p$" |
| P3 | l.4094 "The implementation carries every pair the profile's Section~\ref{sec:attack-profiles} subgraph admits … so the two nets are the same object in execution." → cut, or a footnote | −60 | T1. An implementation-equivalence note, not a step of the definition (yardstick failure mode "implementation described instead of design"). M44 ("the two nets" has no antecedent) |
| P4 | l.4096–4097 "which is what makes the net plug and play: each attack profile is an input, and structure and semantics stay apart" → "so each attack profile is an input to one construction" | −10 | T2. M44 ("plug and play") |
| P5 | l.4097–4098 "One token is a choice about the attacker, not a property of the net. The attacker pursues one line …" → "One token is a choice about the attacker: it pursues one line …" | −8 | T2. The not-X-but-Y form, which Marc hears as a machine tell in short prose. The AND clause stays (A2 makes it the one account) |
| P6 | l.4143–4146 cut "Any further declared factor multiplies into Equation~\ref{eq:routing} in the same way and renormalises with it; none does in the runs this dissertation reports, and each arm of Chapter~\ref{ch:experiments} that adds one names it." | −35 | T1. Describes an extension slot no reported run uses; "arm" is undefined in chapter 4 (audit C1). **Re-opens** R3 of the 2026-09-08 formalism handoff (the slot as one prose sentence). The zero-factor sentence (l.4139–4140) is ruled to stay and stays |
| P7 | l.4256–4271, the overlay: S3's move; cut "The tactics reconnaissance and resource development, before initial access, are not well connected in our attack profiles." (A5 says it); cut "so that we could model the runtime behaviour of the APT attacker model"; M28 "We can assume that they perform these because we know they do that (Section~\ref{sec:apt-survey}), and it is defensible because nothing detects pre-intrusion activity anyway." → *suggestion:* "APT attackers reconnoitre before they intrude (Section~\ref{sec:apt-survey}), and no defence in MTDSim observes it." | −45 | T1 + T2. The 2026-08-16 do-not-re-flag ruling keeps the defender-validity sentence and the observability-boundary naming *out*; this entry adds neither. **X4** corrects what the paragraph says the overlay adds |
| P8 | l.4285 "But there are limits to what the Petri net can provide:" → "The Petri net leaves two things to the join:" | −5 | T2, minor. "Limits" reads as a weakness of the formalism when it means a division of labour. Ratified connective prose (2026-09-26): ratify-on-read |

### §4.4 preamble (235 → ≈190)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| I1 | l.4362–4367: keep, and land the OWED memory clause (C4) | +15 | "the three inputs the join carries" no longer counts §4.4.5 |
| I2 | l.4413–4424, the four bases: keep; add the memory's factor of three to the judgement list (C4); "Appendix~\ref{app:movement} gives the reason for each" is false for three of the five (X6) | +5 | Ruled 2026-09-25 |
| I3 | l.4429–4432 cut "Appendix~\ref{app:sensitivity} varies these values one at a time and reports what changes \citep{tenbroeke2016}. Section~\ref{sec:ablation} removes the partition into attack profiles, the failure matrix and the vulnerability memory in turn and reports what changes." | −45 | T1, G4. Each declared input already points at its own test (l.4659–4660, 4812–4813, 4888–4891, 4963–4964), and chapter 5 opens §5.4 on the same list (l.7914–7921). Keep "Three values are not tested: …", the only place that disclosure is made (a must-carry). The ten Broeke citation moves to the first subsection pointer. **Re-opens** the 2026-09-26 SIMPLIFIED placeholder ("for Marc's redraft") |

### §4.4.1 Runtime loop (588 → ≈520 with F5's list; ≈430 without)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| R1 | l.4449–4451 "and supplies its duration, so that the Petri net supplies all the tactic timing of the APT attacker model at runtime" | 0 | T2, **registry conflict surfaced**: "duration" and "tactic timing" are deprecated variants of *dwell time* (row 54), but "supplies all the tactic timing" is the RESOLVED 2026-08-20 wording. *suggestion:* "and supplies its dwell time, so that the Petri net supplies every dwell time of the APT attacker model at runtime". Marc rules which stands |
| R2 | l.4457–4460: keep the targeted-scenario sentence; cut "; the run ends when a target is compromised" | −7 | T1, **X2** |
| R3 | l.4516–4523 "Success or failure at runtime, the verdict $v \in V$ of Equation~\ref{eq:vc-net}, comes from MTDSim and is propagated up. … The same holds for the moving target defence: if MTD disrupts the attacker, then whatever attack action it is on fails." → "The verdict $v$ comes from MTDSim. An attack action fails if its preconditions were missing (for example, an exploit of a vulnerability not yet scanned for), or if an MTD deployment disrupts it (Section~\ref{subsec:attacker-model})." | −25 | T2, G3. $v$ is declared at Eq. 4.3; the re-declaration goes (audit D3.8; T1). "moving target defence" is re-expanded. The next sentence ("The join can tell a disruption from an unmet precondition …") is verified true (X8) and stays |
| R4 | l.4527–4533, dwell-only: cut "so this is not felt by the token in the Petri net" and "but there was no attack action in flight to lose and no verdict to route on: the token still leaves on the base weights" | −35 | T1, G4 (the fourth and fifth tellings). Keeps the definition, the cost sentence and the verdict sentence "At a dwell-only tactic MTD is felt as cost, never as a change of route." **X9**: the cost is the confusion penalty, which the APT attacker model pays here too, so "costs the attacker the time" → "costs the attacker the confusion penalty" (T2) |
| R5 | l.4566–4570 "We employed a sink-retrace policy, because the token would frequently hit sinks and terminate the run --- a concession to the thinness of the corpus; we retrace the edge travelled. The retrace is for a structural dead end, a place the corpus gave no exit." → *suggestion:* "When the token reaches a dead end, a place the corpus gave no exit, it retraces the edge it travelled, a concession to the thinness of the corpus." | −20 | T2. Definition before reason; "sink" and "structural dead end" become one term (G5); "We employed", "frequently" (M39) go. The stall sentence stays and joins X2's stopping list |
| R6 | l.4578–4586 "The simulator we are inheriting largely models the confusion and disruption of the attacker through a 20-second confusion penalty … How the defender thwarts the attacker is an invariant of the simulator, so we maintain that 20-second confusion penalty. Not all the timing is supplied by the Petri net: the confusion penalty is the exception. The same rule covers everything else the simulator owns. The six attack actions, the deployment schedule and the penalty are the environment's, held identical for both attackers, so that a difference between the arms is a difference in the attacker and nothing else." → *suggestion:* "The confusion penalty (Section~\ref{subsec:attacker-model}) is the one time the Petri net does not supply. It belongs to the simulator, with the six attack actions and the deployment schedule, and all three are held identical for both attackers, so that a difference between their runs is a difference in the attacker and nothing else." | −50 | T2, G3. Three sentences said "the simulator owns it"; ch2 defines the penalty. "arms" is undefined (M22). **Re-opens** the 2026-08-20 resolution ("all the tactic timing"); the suggestion keeps its logic |
| R7 | l.4598–4602 "Nothing carries between runs. Each run starts from $M_0$ knowing nothing of MTD: the attacker does not hold the deployment schedule, learns nothing about it within a run, and carries nothing from one run into the next. That is the scheme-aware attacker Jalowski et al.\ \citep{jalowski2026} ask for, and this model is not one; Section~\ref{sec:future-work} returns to it." → cut "Nothing carries between runs."; "That is the scheme-aware attacker Jalowski et al. ask for, and this model is not one;" → "It is therefore not scheme-aware (property 8, Table~\ref{tab:attacker-properties});" | −15 | T1 + T2. The first sentence and the last clause of the second say the same. Chapter 3 introduced Jalowski's ask (l.2808–2813). The OWED 2026-09-28 clause ("learns nothing about the defence within a run") is already met: "learns nothing about it" has the schedule as its object, and X10 verifies the sentence; the OWED comment closes |
| R8 | l.4613–4617: keep the ceiling sentence; cut "But it is extendable and modular: our Petri nets can be mapped to anything given an appropriate mapping, or a richer set of attack actions can be built that operationalises all of MITRE's tactics." | −35 | T1. The ceiling sentence is a MUST-CARRY (chapter 5 cites it). "Anything" overclaims (M33); the extension is §7.2's (the affinity board's §7.2 row carries "a richer action set"). The connective-prose audit already called the clause "a value close" |
| R9 | F5's enumerated loop (six steps from Figure 4.5's caption) | +90 | T1 move, if F5 is ruled |

### §4.4.2 Tactic dwell times (386 → ≈320)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| D1 | l.4632–4643 "We cannot derive the dwell times from anything built so far. The dwell times do not exist in the literature; they do not exist in CTI vendor reports. Prior papers describe this as inherently arbitrary: trying to put times on an attack \citep{bland2020, mcqueen2006, mendonca2023}. This is a parameter of the model itself, not an invariant." → *suggestion:* "Per-tactic dwell times are reported neither in the literature nor in CTI vendor reports, which give the length of a whole intrusion (Chapter~\ref{ch:intro}); models that time attack steps declare their values \citep{bland2020, mcqueen2006, mendonca2023}. Here they are parameters of the model." | −20 | T2. **X5.** "Invariant" is §4.4.1's word for what the simulator owns, so it is not reused here; the one-sentence paragraph merges. "declare" is what all three sources support (§9) |
| D2 | l.4631–4632 "Each tactic consumes some time in the simulator, of mean $\mu_p$ (Equation~\ref{eq:gspn})" → "(Section~\ref{sec:petri-formalism})" | 0 | T1. $\mu_p$ is not in Eq. 4.1 (T2) |
| D3 | l.4647–4649 "We derived our dwell times for the tactics from the dwell times of MTDSim. What we could take from the six attack actions, we used directly, and we extrapolated the rest." → "We derived the dwell times from MTDSim's six attack actions, using their costs directly where they apply and extrapolating the rest." | −12 | T2 |
| D4 | l.4649–4650 "The 15 tactics resolve onto four families." | 0 | X-minor, verified (`data/ogasp/tactic_durations.json`: resource development is a fifth group, `prep-off-network`): resource development (0 s, l.4729) sits in none of the four; Table B.4b lists it as a fifth row, "Off-network prep". *suggestion:* "The 14 tactics on the network resolve onto four families", and the 0 s sentence follows directly |
| D5 | l.4726–4733: cut "and the derivation is in Appendix~\ref{app:dwell-derivation}" (l.4659 gives it); "10 times" → "ten times"; M30: cut "we would assume," | −15 | T1. M48, M30. The 45.0 s and 0 s worked examples are ruled to stay (2026-08-20) |
| D6 | l.4740–4746 cut "the behaviour of APT attackers is stochastic, described by a probability distribution rather than a fixed value." and let "There is evidence in the literature for stochastic attack behaviour" carry the claim | −18 | T1. Two sentences, one claim. "The exponential is a modelling choice, not a claim …" is a not-X-but-Y opener (P5's note); Marc's ear. Keep the M46 must-carry (l.4746–4747) |

### §4.4.3 Tactic-to-action mapping (176 → ≈120)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| M1 | l.4774–4775 "No such mapping exists in the literature, so we used our best judgement." → "We found no published mapping, so $\varphi$ is declared." | −4 | T2. M35; G4 |
| M2 | l.4776–4779 cut "We use a direct mapping with certain constraints: a tactic can go to only zero or one attack actions, and a tactic can only execute either zero or one attack actions in the simulator at a time, so this problem remains tractable." | −35 | T1. l.4773 already says "to at most one". **Re-opens** the 2026-08-20 ruling (the zero-or-one sentence stays; re-proposal rejected 2026-09-08). Offered once, with its reason: the second constraint ("one at a time") is the one-token rule of §4.3, so the sentence states nothing §4.3 and l.4773 do not. If tractability is the point, keep "so the mapping stays tractable" |
| M3 | l.4781–4782 "many tactics are dwell-only" → "seven of the 15 tactics are dwell-only" | 0 | T2. M36. Verified: Figure 4.6 "no mapping (7 of 15)" and the reported mapping (X11) |
| M4 | l.4809–4814 "We tried other mappings: forcing a total mapping was just another input that did not work: it was running a tightly ordered finite state machine in an unordered but stochastic manner (Appendix~\ref{app:experiment-one}); … We also considered using MITRE Caldera~\citep{applebaum2016}, but this would introduce too much overhead." → *suggestion:* "A total mapping, one attack action for every tactic, ran the baseline attacker's ordered procedure in a stochastic order (Appendix~\ref{app:experiment-one}); Appendix~\ref{app:sensitivity} swaps it in." Caldera: keep only with its real reason, or cut | −25 | T2, G3. M37, M38. "We tried" is build-order narration (yardstick failure mode 1). Caldera's "overhead" is unexplained |

### §4.4.4 Failure matrix (419): keep, three small edits and one question

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| F1 | l.4870 "Eight of the 15 tactics (Figure~\ref{fig:attack-matrix})" → "(Figure~\ref{fig:controller-mapping})" | 0 | T1. Figure 3.1 draws ATT&CK's matrix; Figure 4.6 draws the stages. Verified 8 of 15 |
| F2 | l.4880–4881 "a move across two stages is scaled down by a declared rate" and l.4890–4891 "Appendix~\ref{app:sensitivity} varies the rate" | 0 | T2. Appendix C varies a forward rate, a backward rate and a floor (audit D1.9). "by declared rates" / "varies the rates" |
| F3 | l.4891–4892 "These are threat-model parameters for this simulator, not real-world values." | −12? | **Question for Marc.** Registry row 68 bars "threat model" outside quotations, so at least "threat-model" → "model". Is the sentence a second must-carry, or do "every value in it is our judgement" (l.4861) and the dwell must-carry already carry it? G4 |
| F4 | "foothold" (l.4863–4877) | 0 | T3, C5 |

### §4.4.5 Vulnerability memory (215 → ≈170)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| V1 | l.4929–4939, the property 7 sentences | see X5b | **X5b.** "the defender's patterns that Table~\ref{tab:attacker-properties} also names under property 7" misreads Table 3.2, whose row 7 names only learning from MTD deployments (l.2919). The memory learns the network, as Zhang's halving does, and ch3 scores that halving as learning *in part* (l.3235–3237). T3: what ch4 may claim here is Marc's. Gate 1 (open since 2026-09-29: the paragraph opens on motivation, "Any attacker learns", an uncited universal) is the same sentence |
| V2 | l.4959 cut "The idea is that the attacker compromises more of the network." | −10 | T1. The hypothesis sentence after it states the effect specifically (ruled 2026-09-29) |
| V3 | l.4933–4944 "Zhang's attacker already does this for time: exploitation time is halved on a vulnerability exploited on an earlier host \citep{zhang2023}. We extend the halving …" and "The exploit attack action (Figure~\ref{fig:attacker-model}) attempts each service's top vulnerabilities, and an exploit of each succeeds with a probability set by its CVSS complexity (Section~\ref{subsec:network-model})." → *suggestion:* "We extend Zhang's halving of the exploitation time (Section~\ref{subsec:attacker-model}) from a saving in time to a vulnerability memory …"; "Each earlier success on a vulnerability, on any host, triples the attacker's odds of exploiting it again (the odds its CVSS complexity sets, Section~\ref{subsec:network-model})" | −30 | T2, G3. Chapter 2 defines both (l.686–689, 854–855). Marc, 2026-09-30: "no need to lecture the reader". "Triples" stands: X12 verifies that each success multiplies the odds by three again |
| V4 | l.4955–4956 "(Appendix~\ref{app:movement})" | 0 | X6: Appendix B holds no entry for the factor of three |

### §4.5 Evaluation metrics (1 194 → ≈1 150)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| E1 | l.4982–4984, the stopping rule | see X2 | **X2.** The one place the full rule should stand |
| E2 | l.4984–4986 "Each metric is computed over a \emph{cell}: the runs of one attacker at one deployment interval, with no MTD or under one MTD mechanism or deployment strategy" | 0 | T2, G5. *Cell* is defined and never used again in this sense; chapter 5 says *combination* (Table 5.1, §5.1 "Every combination"). One term: "Each metric is computed over the runs of one combination of Table~\ref{tab:experiment}: …", or ch5 adopts *cell*. The pointer to `sec:dimensions` lands on ch5; the definition of mechanisms and strategies is ch2's (l.708) |
| E3 | l.5068–5072, the attack-outcome lead-in | 0 | Keep. voice.md §(0)'s worked case, Marc's own |
| E4 | l.5023–5026, the Hong et al. contrast | 0 | Keep. The preliminary ledger's question is withdrawn: the s45 verification (16_verify, 15_verify §2) recommended exactly this sentence, and it credits the supervisor's metric correctly |
| E5 | the word-equations | 0 | Keep. The preliminary question is withdrawn: literature_conventions §d1 requires a numbered display equation per metric, and the named-quantity form is the house form (voice.md §0) |
| E6 | l.5138–5140 "time lost records adaptivity" | 0 | Keep in ch4. Chapter 5 (l.7239–7240) says both per-deployment metrics record it: ch5 follows ch4 (out-of-chapter flag, §10) |

---

## 8. Content the chapter lacks (C), named, not drafted

- **C1. The two senses of *attack profile* joined** (G5). One clause, Marc's.
- **C2. Chapter 3's objectives joined to chapter 4's profiles.** Exfiltration
  matches; *impediment* is recorded under ATT&CK's *Impact* tactic; *positioning*
  has no profile, and whether $c_4$ (no realised objective) is where it lands is a
  claim for Marc to make or decline.
- **C3. The four lifecycle stages joined to chapter 3's five.** §4.4.4's stages
  cite Alshamrani, whose five stages ch3 gives. One clause saying how the four
  fold the five, at their first use, which is Figure 4.6 (F6).
- **C4. The vulnerability memory in the §4.4 preamble and Figure 4.5** (OWED
  2026-09-28): the "three inputs" sentence, the factor of three among the
  judgement values, the figure's glyph.
- **C5. What *foothold* means in the model.** §4.4.4's principle is stated in the
  attacker's state ("a failure without a foothold"), and the rules key on the
  *stage* of the failing tactic (Figure 4.4(b): a failed initial access). Ch3 uses
  the word for Alshamrani's lifecycle stage (l.1112). One clause saying that a
  foothold here means a tactic past the intrusion stage, or Marc's correction if
  the rules read host state. T3.
- **C6. The reasons Appendix B promises** (X6): σ = 0.1, one flow per operator, and
  the factor of three. Each needs a row in Appendix B (or its reason in the body),
  or the pointer goes.

## 9. Factual corrections and contradictions (X), verified

Each carries its evidence. "Verified" means checked this session against the
owner named.

- **X1. The classification rule is the rejected one (l.3894–3895, 3907).**
  - Chapter 4: "classify each flow by its terminal tactic, the last tactic it
    reaches"; "Terminal tactic is the primary evidence for objective, but we
    cross-checked against the CTID description, the ATT&CK page and vendor
    reports."
  - Table B.3 (`tab_B-3a`, l.25 and l.33): the terminal-tactic scheme is
    *dismissed* ("Disagrees with the attested objective on 19 of the 38 flows");
    the adopted scheme, "Stated objective, four disjoint classes", slices on the
    stated objective and yields 19/7/7/5.
  - So the 19 overrides are not cross-check corrections to a terminal-tactic
    classifier; they are the 19 flows on which the dismissed classifier disagrees
    with the adopted one. *Suggestion (T2):* "Following Alshamrani et al.
    \citep{alshamrani2019}, we treat the tactics before the objective as common
    to all APT attackers and classify each flow by the objective its sources
    state: the CTID description, the ATT&CK group page and vendor reports. The
    terminal tactic, the last tactic a flow reaches, disagrees with the stated
    objective on 19 of the 38 flows, often because the flow ends before its
    objective (Appendix~\ref{app:rejected-partitions})."
- **X2. When a run ends: three statements in chapter 4, a fourth in chapter 2.**
  - §4.4.1 l.4459–4460: "the run ends when a target is compromised".
  - §4.4.1 l.4570: "a stalled run ends"; l.4566–4567: sinks "terminate the run".
  - §4.5 l.4983–4984: at a target, at more than 80 % of hosts compromised, or at
    the time limit; Table 5.1 and ch5 l.6061–6062 agree with §4.5.
  - Chapter 2 l.828–830 adds "or can discover no new host" for the baseline;
    Appendix B l.9302–9303 says "at the objective, at the time limit, or at a
    Petri-net sink".
  - Code (verified): every targeted run of either attacker checks both the 80 %
    stop (`attack_operation.py:741–746`; `time_network.py:51–55`) and the target
    (`:754–757`), under a 15 000 s time limit (`HORIZON`). The APT walk also ends
    on a stall, an unresolvable sink or an event cap (`movement/attacker.py:566–571,
    633, 704`).
  - In the reported corpora the 80 % stop ends 38 of 1 000 unopposed and 1 072 of
    67 000 defended baseline runs, and never an APT run (at most 34 hosts). No
    unopposed APT run ends on a stall, a sink or the cap: each ends at a target
    (523) or at the time limit (4 477).
  - So §4.5 is right and §4.4.1's "the run ends when a target is compromised" is
    incomplete. The consolidation handoff's ruling H2 (remove the 80 % stop) was
    never applied.
  - *Fix:* §4.5's sentence stays the one full statement (E1); §4.4.1 drops its
    run-end clause (R2) and keeps the stall as a definition. Whether §4.5 adds "a
    stalled run also ends" is Marc's: it can end a run and in the reported runs
    never did.
  - *Flag for chapter 5:* in the unopposed corpus 29 of the 38 baseline runs that
    stop at 80 % never reached a database host, yet carry `reached_objective`
    true; ASP counts them apart (ruling H's facts). Confirm the ASP reader does.
- **X3. "A documented attack-behaviour corpus spanning 2017 to 2024" (l.3749) is
  false.** Table B.2 lists Shamoon, the Target breach, Sony and the SWIFT heist
  (2012–2016) and the ToolShell flow sourced to `unit42sharepoint2025`. Verified in
  `data/gap/_corpus_stix/`: the incidents run from 2013 (Target) to 2025
  (ToolShell). "2017 to 2024" comes from no artefact, only from the note
  `cti_corpus_as_snapshot.md:29`, which needs the same fix. A1 cuts the sentence;
  if a span is wanted, "2013 to 2025".
- **X4. The pre-intrusion overlay is added to two profiles, not "each".**
  - §4.3 l.4258–4263: the overlay draws "out-transitions from reconnaissance to
    resource development to initial access, as well as a backwards transition from
    initial access to reconnaissance … we add it to each attack profile's Petri
    net".
  - Code (verified): the overlay arm is on in every reported run
    (`with_synthetic_overlay=True`), and the token starts on reconnaissance in
    5 000 of 5 000 unopposed APT runs. But the overlay adds edges only where the
    corpus does not already bridge reconnaissance to initial access: $c_3$ and $c_4$.
    For $c_1$ and $c_2$, `synthetic_transitions` is empty
    (`data/ogasp/petri/synthetic_overlay.json`; `movement/net.py:186–193`).
  - So chapters 5 and 6 are right ($c_2$ has no move back to reconnaissance;
    ch6 l.8485–8486, ch5 l.8070–8071) and §4.3 is wrong. $c_1$'s 0.062 back edge in
    Figure 4.4 is the corpus's, not the overlay's.
  - *Fix (T2):* "we add it to each attack profile's Petri net" → "we add it where
    a profile's flows do not already lead from reconnaissance to initial access
    ($c_3$ and $c_4$)"; $M_0$'s "when the pre-intrusion overlay … is in place, and
    on initial access otherwise" → "on reconnaissance" (the other arm is never
    run; its clause is a configuration the dissertation does not report).
- **X5. "The dwell times do not exist … in CTI vendor reports" (l.4633–4635).**
  - Chapter 1 l.230–231 and chapter 3 l.1088–1090 cite M-Trends, a CTI vendor
    report, for how long whole intrusions go undetected. Only *per-tactic* dwell is
    absent.
  - "Prior papers describe this as inherently arbitrary": McQueen says "somewhat
    arbitrarily" (`extractions/mcqueen2006.md` l.99); Bland "notional and randomly
    selected" (`bland2020.md` l.50); Mendonça "reasonably estimated, as they were
    not found in the literature" (`mendonca2023.md` l.116). Only one says
    arbitrary; all three declare. D1's "declare" is supported by all three.
- **X5b. Property 7 (l.4937–4939)**: see V1. Out of chapter, the same misreading
  reaches chapter 6's verdict table (l.8554), which gives the model full marks on
  properties 6 and 7; chapter 4 claims no mechanism for property 6 (§10).
- **X6. Three appendix pointers promise reasons Appendix B does not hold.**
  l.4422–4424 ("Appendix B gives the reason for each") covers σ and one flow per
  operator; l.4955–4956 points the factor of three at Appendix B. Grep of Appendix
  B's prose and every `tab_B-*` file: no row or sentence on σ, on one flow per
  operator, or on the memory (verified). C6.
- **X7. "which sits under MITRE Engenuity" (l.3745–3746).** Chapter 3 says
  "MITRE's Center for Threat-Informed Defense" (l.1530), the bib entry carries
  `howpublished = {MITRE}`, and the ch3 ledger (P8) found "Engenuity" in neither
  the cited v3.2.0 document nor the bib. (The attackflow extraction's header says
  "MITRE Engenuity", but that header is session-written, not the source.) A1 cuts
  the sentence; this corrects the preliminary ledger's framing, which treated it
  as an error of fact rather than an unsupported attribution and a duplicate.
- **X8. One failure verdict, told two ways; chapter 4 is right.** §4.4.1
  l.4521–4523: "The join can tell a disruption from an unmet precondition, and it
  discards the distinction before routing." Verified: the record keeps
  `MTD_INTERRUPT` apart from `PRECONDITION_UNMET` (`movement/attacker.py:378–382`)
  and `controller/verdict.py` maps both to failure. Chapter 6 l.8486–8487 ("the
  simulator returns one failure verdict whatever the cause") misplaces the merge:
  it is the join's choice, not the simulator's (§10).
- **X9. The penalty at a dwell-only tactic; chapter 5 is wrong.** §4.4.1
  l.4529–4531 says a deployment there "cuts the dwell short and costs the attacker
  the time". Verified: the APT attacker model pays the confusion penalty there
  (`movement/attacker.py:1001–1009`, `_pay_interrupt_cost`), through the same call
  both attackers use (`attack_operation.py:177–212`). Chapter 5 l.7377–7378 ("The
  penalty is paid only by the deployments that disrupt an attack action") is false
  for the APT attacker model (§10). R4 names the cost. Also verified: the penalty is
  20 s plus a small exponential draw (mean 20.5 s, `time_generator.py:39–42`), so
  ch2's "about 20 s" is exact and ch4's "20-second" is close enough; which actions
  it interrupts depends on the mechanism's layer (`mtd_operation.py:217–264`).
- **X10. Nothing carries between runs: true.** The routing-belief learner
  (`movement/learning.py`) attaches only through `attacker_state`, which no reported
  runner passes; every run builds a fresh network, adversary (and memory) and
  attack operation (`run.py:104–108`). No entry beyond R7.
- **X11. Seven dwell-only tactics: true** for the reported mapping (`v2_partial`,
  both reported runners): resource development, persistence, stealth, defense
  impairment, collection, exfiltration, impact. M3 applies.
- **X12. "Each earlier success … triples the attacker's odds": true.**
  `adversary.py:290–305` computes odds × (1 + 2)^n, keyed per vulnerability across
  hosts, ON for the APT attacker model in the reported runs and off for the
  baseline. The §5.4 ablation corpora ran with it off (by design).
- **X13. "58 to 71 per cent" (l.4871–4872) are per-profile means.** Verified with
  `tools/gspn_gadget_figure.py`: c1 0.58, c2 0.64, c3 0.67, c4 0.71; single tactics
  range from 0 to 1.0. The sentence reads as a range over moves. *Fix (T2):* "carries
  on average 58 to 71 per cent".
- **X14. "An operator with several attack flows in the corpus counts once"
  (l.4086–4089): the operators are hard-coded groups, and two join different
  actors.** Verified: `src/mtdsim/l2_subgraph/dedup.py:25` (`OPERATOR_CLUSTERS`)
  is a fixed list, not the attribution column. One group is the CISA AA22-138B
  advisory, three flows covering two threat actors; "Lazarus" merges the Sony flow
  (G0032) with the SWIFT heist (G0082, APT38). The count of 29 is right; the
  sentence's reason ("one operator's repeated reports") holds only for the groups
  that are one operator. The dedup is also global, so a group's representative can
  sit in another profile (the SWIFT heist leaves $c_1$ because Sony sits in $c_2$).
  T3: whether the two mixed groups are split, or the sentence says "one reporting
  source or operator", is Marc's. The group list also needs a reason in Appendix B
  (C6).

**Verified and right** (no entry): 38 flows; 88 % of technique edges from one flow
(Figure 4.2, Appendix B 419 of 478); 10 of 38 flows mention reconnaissance;
19/7/7/5; 19 disagreements; Wizard Spider 3 of 7 (G0102); 29 weighted flows; σ = 0.1;
35 s / 4.5 s / ×10 / ×8 and every row of Table 4.2; 8 of 15 post-intrusion tactics; 0.062 → 0.750 and "about
a quarter" (Figure 4.4(b): 0.312 → 0.083, 0.250 → 0.067, 0.125 → 0.033); 50 hosts;
five attack actions in 60 s and its Jung §5.2 locator (the s45 verification corrected
§6 → §5.2); Zhang's MTTC and NCR quotations and pages; eleven metrics.

## 10. Out of chapter: flagged, not fixed

- **Chapter 1 l.505–507.** The contributions list promises "the rate at which it
  compromises hosts after each MTD deployment", a metric retired 2026-09-30
  (§4.5's round 6). Chapter 1 should name the two §4.5 per-deployment metrics.
- **Chapter 5.** l.7377–7378 says the penalty is paid only when an attack action
  is disrupted; the APT attacker model also pays it at a dwell-only tactic (X9).
  l.7239–7240 (adaptivity: both metrics, against §4.5's "time lost"); l.8043–8046
  restates §4.4.4's "fails upwards" sentence near-verbatim (refer instead); the ASP
  reader and the 29 baseline runs stopped at 80 % without a target (X2). On $c_2$,
  l.8070–8071 is right (X4).
- **Chapter 6.** l.8735 points to §4.5 for Cohen's $d$, which ch5 l.7924–7929
  defines; l.8486–8487 puts the one failure verdict in the simulator, where it is
  the join's merge (X8); the verdict table (l.8554) and X5b. On $c_2$, l.8485–8486
  is right (X4).
- **`docs/notes/ch4_methods/cti_corpus_as_snapshot.md:29`** is the source of "2017
  to 2024" (X3).
- **Appendix B** (G6) and the Attack Flow version: Appendix B's captions say
  "published export v3.1.1", the bib "Version 3.2.0". Both are true
  (`data/gap/README.md` l.30: release v3.1.1, package 3.2.0); one string, said once,
  is the fix.
- **`docs/notes/ch4_methods/README.md`** describes four sections, "L0–L4", and the
  retired name "movement attacker". Refresh once the rulings land.

---

## 11. What changed from the preliminary ledger

- **New:** X1 (classification rule), X3 (corpus span), X4 (the overlay reaches two
  profiles), X5b (property 7), X6 (appendix pointers), X8–X14 (X8 and X9 find
  chapters 6 and 5 wrong, not chapter 4); G2, G3 (the backward lean test),
  G5 (the term collisions at the ch3 boundary), G6; F1–F6, T1–T3; C1–C3, C5, C6.
- **Resolved:** the preliminary X3 (the stopping rule) is traced in code: §4.5 is
  right, the 80 % stop is live and ends only baseline runs (now X2).
- **Corrected:** X1 of the preliminary ("MITRE Engenuity is an error") is now X7, an
  unsupported attribution inside a duplicated sentence.
- **Withdrawn:** the preliminary C3 (a chapter close), against connective_prose
  §(f)1; the preliminary questions E2 (Hong) and E3 (word-equations), both answered
  by existing rulings; the preliminary C2 (OWED "learns nothing about the
  defence") is already met by the sentence as written (R7).
- **Kept:** G1, the budget re-rule, unchanged.

## 12. The minimal set Marc can take alone

If only one sitting: **X1, X2, X4, X5, X5b, X6** (the places the chapter is not the
model that ran), **A1** (the duplicated first paragraph of §4.1, which also removes
X3 and X7), **R8** (the extensibility clause) and **T2** (the codename in Table 4.2's
caption). Together ≈−200 words and every examiner-visible defect.

## Applied — round 1 (2026-10-02, Marc: "I accept all changes, integrate well")

Every entry in §3–§9 is applied to `dissertation.tex` as DRAFT STATE, each unit
carrying a `[CH4 SCRUTINY 2026-10-02 …]` comment that names its entries; prior
text is in git (3f6b4f8c). Marc's section-by-section acceptance pass follows, and
each unit is ratify-on-read.

**Measured after the apply:** 4 769 prose words (was ≈5 490): §4.1 273, §4.2 357,
§4.3 970, §4.4 preamble 252, §4.4.1 502, §4.4.2 345, §4.4.3 102, §4.4.4 460,
§4.4.5 166, §4.5 1 185; captions 299 (was ≈500). Chapter 4 is pp. 16–30 (was
16–32). The build has no undefined reference and no error; pages 16–30 were
re-rendered and read.

**Floats regenerated:**
- Figure 4.1 (`tools/ch4_overview_figure.py`): "reconfigures", and the MTD box
  narrowed so the label fits.
- Figure 4.5 (`tools/runtime_loop_figure.py`): "MTD" for "Defender", and the
  vulnerability memory drawn in the attacker box in the accent.
- Table 4.2 (`tools/dwell_catalogue_tables.py`): the caption fixed, house style.
  Its appendix siblings came out byte-identical.

**Where the apply departs from an entry, and why:**
- **C6 / X6.** No reason for σ, one flow per group or the factor of three exists in
  any record to put in Appendix B, and none was invented. Instead:
  - the §4.4 preamble now points each value at where its reason lives
    (Appendix B for the first three, §4.3 for σ and one flow per group);
  - §4.3 states σ's reason, the one the overlay record gives: a minority share,
    so the observed weights keep nine-tenths;
  - the factor of three stays "our judgement", tested by §5.4.3's ablation.
  **Owed, Marc's:** a reason for the factor of three (the memory handoff records
  only "the pre-check's λ = 2").
- **F3.** The failure matrix's "not real-world" sentence was kept, as a second
  must-carry, with "threat-model" → "model".
- **C2.** Joins exfiltration and impact (impediment recorded under ATT&CK's
  Impact). *Positioning* is not claimed for $c_4$, whose flows are loaders and
  adware.
- **C3.** "The first four of the five stages of Section 3.1.1 correspond to them
  in order". Cleanup, the fifth stage, is not placed.
- **C5.** The foothold clause follows Table B.6's rules A, C, E and I: initial
  access gains it, and a failure at reconnaissance or initial access has none.
- **X14.** "An APT group … or one advisory reporting several" covers the CISA
  advisory group. The "Lazarus" group (Sony with APT38's SWIFT heist) is left as
  built and unclaimed either way. Splitting it would change the 29, a re-run, out
  of scope; Marc's call.
- **R4.** The dwell-only cost is named as the confusion penalty (X9).
- **S4.** The §4.4.1 topics already run in loop order once the six steps lead. The
  targeted-scenario sentence stays second.
- **G5.** *Flow* versus *attack flow* waits on the unruled registry row 105.
- **Terms.** Three rows ratified in the registry: *APT group*, *dead end*,
  *combination*.

**Records updated:**
- `_writing_guide.md`: G1, chapter 4 6 → 16 units and experiments 12 → 8. The
  conservation breach of +1 500 words is recorded for Marc to fund or ratify.
- `notes/ch4_methods/README.md`: the shape.
- `notes/ch4_methods/cti_corpus_as_snapshot.md`: the corpus span, the source of
  X3.
- `workflows/terminology.md`.

**Not applied (out of chapter, §10 and G6, flagged as the procedure requires):**
- chapter 1's contribution metric;
- chapter 5's penalty sentence, adaptivity sentence and "fails upwards"
  restatement;
- chapter 6's verdict location, Cohen's $d$ pointer and verdict table;
- Appendix B's vocabulary, the Attack Flow version string and the codenames.

Each is a one-line fix when Marc wants it.

## Validation gate

- Every G / S / F / T / prose / C / X entry carries Marc's ruling: applied,
  declined or amended.
- The open M entries absorbed here (M12, M18, M19, M22, M24, M25, M27, M28, M30–M33,
  M35–M39, M41, M42, M44, M48) are each applied or declined, and the mark-risk
  ledger retires.
- A grep of the live prose finds none of: "Engenuity", "2017 to 2024",
  "threat-model", "v0-uncalibrated", "by its terminal tactic", "do not exist in
  CTI", "to each attack profile's Petri".
- One stopping rule is stated once (§4.5) and matches the code.
- Figures 4.1 and 4.5 regenerated, re-read as PNGs; Table 4.2 regenerated.
- The PDF builds with no undefined references and no new overfull boxes; pages
  16–32 are re-rendered and read.
- A cold reader holding only chapters 1–3 and the revised chapter 4 can say: what
  the attack graph is and where it came from; what an attack profile is, how its
  flows were classified and how many each holds; what fires when in one tactic of
  one Petri net; which values were judged and which measured; and how a run ends.
- Prose within ±5 % of the target G1 sets.

## Hard constraints

- Nothing applied unratified. Marc's dictated units change only by the deletions
  and merges ratified here.
- Must-carries stay: the ceiling sentence (§4.4.1); "model parameters anchored to
  this simulator, not real-world measurements" (M46, §4.4.2); "Three values are not
  tested" (§4.4 preamble); the 29-flow weighting (§4.3); the zero-factor sentence
  (§4.3, ruled 2026-09-08).
- Do-not-re-flag rulings in the tex trail hold unless an entry names what it
  re-opens: the defender-validity sentence (2026-08-16); the routing-ablatability
  must-carry (cut); the vulnerability-memory pass-5 cuts; "our existing
  simulator", "in the real world" and the opener's "it" (2026-09-04).
- Terms per the registry: *attack action*, *Petri net*, *base weight*, *decision
  place*, *failure matrix*, *dwell time*, *time limit*, *deployment*, *MTD*.

## Reading list

- `docs/thesis/dissertation.tex` l.3451–5208, prose and `%` trails; rendered
  pages 16–32.
- [`../workflows/model_chapter_conventions.md`](../workflows/model_chapter_conventions.md),
  the checklist in §(f).
- `docs/thesis/tables/tab_B-3a*.tex` (X1) and `tab_B-2a*.tex` (X3).
- [`2026-09-25_ch4_mark_risk_ledger.md`](2026-09-25_ch4_mark_risk_ledger.md) §M,
  for each absorbed M entry's original wording.
- `docs/sources/extractions/s45_metric_definitions/15_verify_*.md`,
  `16_verify_*.md`, `17_verify_*.md` (the §4.5 citations, already verified).

## Out of scope (explicitly)

- Re-running anything; any number in §4.5 or chapter 5.
- Figure and table regeneration (F1, F5, T2) until ruled.
- Drafting replacement prose. The *suggestions* above are built from Marc's words
  for him to re-word or ratify.
