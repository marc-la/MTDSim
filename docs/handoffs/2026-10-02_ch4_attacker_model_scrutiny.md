---
status: open                  # 2026-10-02: PRELIMINARY ledger, nothing applied; awaiting Marc's rulings and the owed procedure steps (§0)
created: 2026-10-02
companions: ../workflows/chapter_scrutiny.md, ../workflows/voice.md §(0), ../workflows/critique_protocol.md (tiers), ../workflows/terminology.md, 2026-09-25_ch4_mark_risk_ledger.md (its open M entries are absorbed here)
---

# Chapter 4 scrutiny (preliminary): one register, the chosen design before its alternatives, each caveat once

**Goal.** Bring chapter 4 (APT attacker model) to a length the ledger can carry
and to one register throughout. Every sentence should do something chapter 5 or
the examiner needs at that point. Each entry below is a proposal for Marc to rule
on. Nothing is applied until he rules, and his dictated units change only by the
deletions and merges he ratifies; any rewording is his.

## 0. What "preliminary" covers

This ledger comes from one session reading the chapter's prose (floats stripped)
together with its `%` comment trails (l.3451–5209, 2026-10-02). It also checks the
open M entries of [`2026-09-25_ch4_mark_risk_ledger.md`](2026-09-25_ch4_mark_risk_ledger.md)
against the current tex. Done from [`chapter_scrutiny.md`](../workflows/chapter_scrutiny.md):

- §1, partly. Words were measured per unit (below). The PDF pages were **not**
  rendered.
- §4, partly. Only the claims behind the X entries were verified, each with its
  locator.
- §5, the ledger.

**Still owed before the full pass:** §0, loading `ch4_methods/README.md` and
`literature_conventions.md`; §1, rendering and reading the PDF pages; §3, the
forward and backward audit agent; §4, verifying every claim the redraft will state;
and the F and T sections (§5–§6 below are stubs).

### Measurements (prose words; floats, captions, display maths, citations and headings excluded)

| Unit | Prose | Captions | Ledger |
|---|---:|---:|---|
| Opener | 140 | 46 | — |
| §4.1 Attack graph construction | 493 | 34 | 1 unit; signed off at ~400 on 2026-08-16, then "~1.6 units", open |
| §4.2 Attack profiles by objective | 464 | 30 | 1 unit |
| §4.3 Generalised stochastic Petri-net formalism | 1 125 | 148 | 1 unit |
| §4.4 preamble | 222 | 0 | §4.4 = 2 units + 1 slack + 1 overdraft (2026-09-08) |
| §4.4.1 Runtime loop | 581 | 197 | ″ |
| §4.4.2 Tactic dwell times | 378 | 0 | ″ |
| §4.4.3 Tactic-to-action mapping | 171 | 43 | ″ |
| §4.4.4 Failure matrix | 411 | 0 | ″ |
| §4.4.5 Vulnerability memory | 206 | 0 | not in the ledger (added 2026-09-28) |
| §4.5 Evaluation metrics | 1 119 | 0 | not in the ledger (drafted 2026-09-25 to 09-29) |
| **Chapter** | **5 312** | **498** | **1 500 + 250 overdraft** |

The body (chapters 1–7) is 14 437 words against the ledger's ≈14 050. Chapters 1,
6 and 7 are about 3 400 words under their budgets, and those words have to come
from somewhere.

---

## 1. The yardstick, in five lines

- **Purpose.** Chapter 4 defines the APT attacker model "as simply as possible"
  (`_writing_guide.md`, ch4 row). It covers how the model is captured from CTI, how
  it is made executable, how it joins MTDSim, and the metrics chapter 5 reads.
  Every declared value is stated where its symbol is declared.
- **Context.** What the dissertation built and why, one level above the code. Each
  choice gets its reason once, and the rejected alternatives get one clause each
  (the 2026-08-17 unit contract for §4.3: "the alternatives ranked in a sentence
  each"). Their detail is the appendix's.
- **Audience.** A fourth-year CS student who arrives from chapter 3 knowing ATT&CK,
  Attack Flow (§3.1.3), the eight properties (Table 3.2), and the baseline
  attacker and the confusion penalty (chapter 2). The examiner checks whether a
  reader could rebuild the model from this chapter and whether its caveats are
  honest.
- **The lean test.** Each fact is used by chapter 5, by §6.3's scoring, or by a
  later section of this chapter. A caveat is stated once, where it first applies.
  A limit of the work belongs to §6.5, and an extension to §7.2.
- **The float test.** Figures 4.1–4.5 and Tables 4.1–4.3 each carry what the prose
  points at, and their captions say how to read them. The account of what happens
  belongs in the prose (owed: §5–§6).

## 2. Verdict and the three moves that matter most

**Chapter verdict: right content, two registers.** §4.3's formal definition and
§4.4.4 read as finished method prose. §4.5 was ratified line by line only days ago.
§4.1, §4.2 and the opening of §4.4 still carry dictation: "we", "Hence", "just
another input", "anyway". There, the chosen design arrives after its alternatives,
and fidelity versus coverage is told four times. About 25 of the mark-risk
ledger's M entries are still open in the tex, and nearly all of them fall in these
three places.

**The three moves, in priority order:**

1. **Clear the open M entries and the X entries (§9).** These are the
   examiner-visible defects:
   - "MITRE Engenuity" contradicts chapter 3 and the bib (X1);
   - "the dwell times do not exist in CTI vendor reports" contradicts chapters 1
     and 3 (X2);
   - §4.4.1 and §4.5 give different stopping rules for a run (X3).
2. **The chosen design first, its alternatives one clause each** (G3). This
   applies to §4.1 (the corpus), §4.3 (the formalism) and §4.4.3 (the mapping).
3. **Each caveat once, and limits and extensions to their chapters** (G4). The
   §4.4.1 extensibility clause and the scheme-aware sentence go to §7.2, which
   already carries both (affinity board §7.2 row); chapter 4 keeps the must-carry
   ceiling sentence.

**Projected:** this ledger's proposals take about 700 words off (5 312 → ≈4 600).
Reaching the G1 target of about 4 000 needs a second pass that only Marc's words
can make, on §4.3 (≈980 after this ledger) and §4.4.1 (≈470).

---

## 3. Chapter-level findings (G)

**G1. The budget: re-rule it (Marc's call).** The ledger's 1 500 words for
chapter 4 predate §4.5 moving in (≈1 100 words, from the old experimental-setup
units), the vulnerability memory (≈200) and the 2026-09-08 overdraft. No source
gives a share; the conventions files say so for chapters 2 and 3.
*Recommendation:* ratify **≈3 000 for §4.1–§4.4 and ≈1 000 for §4.5**, about a
quarter of a 15 000-word body. Record it in `_writing_guide.md`'s reallocation
record, funded by the experiments chapter's §4.5 share. The alternative is to hold
the 1 750 and cut about 2 300 words, which would mean losing must-carries.

**G2. Two registers.** The formal units (§4.3's definition, §4.4.4, §4.5) speak
in the third person with named quantities. §4.1, §4.2, the §4.3 overlay and §4.4.1
speak in dictated first person. The open M entries are the symptom list. M12,
M18, M19, M22, M25–M28, M30–M33, M35–M39, M41, M42, M44 and M48 are still in the
tex (checked 2026-10-02). The prose entries below absorb each of them where it
falls, and the mark-risk ledger can retire once this one is ruled.

**G3. Alternatives before the choice.** About 250 words go to the routes not
taken:
- co-occurrence mining, keyword mining and NLP extraction (l.3750–3758);
- attack graphs, DAGs, SPNs and DSPNs (l.3968–3976);
- the six other partitions (l.3920);
- the total mapping and Caldera (l.4809–4814).

In §4.1, half the section passes before the reader learns what the attack graph
*is* (l.3817). The fix is to state the choice and its reason, give each
alternative one clause, and point to the appendix that holds the evidence. Every
alternative here already has an appendix home (Appendices D and B.3, Appendix B.7,
and the feasibility study).

**G4. Caveats repeated.**
- *Fidelity versus coverage* appears four times: l.3787–3796 (three times in one
  paragraph) and l.3896–3897.
- The *not real-world* must-carry appears twice: the dwell times (l.4747) and the
  failure matrix (l.4891–4892).
- *Our judgement* appears four times in prose, alongside "best judgement" and
  "rests on our judgement alone".
- §4.4's preamble already lists every judgement-based value (l.4419–4423), so the
  per-subsection repeats are a second telling.

Keep the preamble list and the M46 must-carry beside Table 4.2. Cut the rest
where the entries below say so.

**G5. Limits and extensions belong to chapters 6 and 7.** The affinity board's
§7.2 row already carries "a richer action set (ch4 l.5232)" and "scheme awareness
and retention across runs (property 8; ch4 l.5224)". §6.5's placeholder carries
"the six adopted attack actions … no scheme awareness". Once those land, chapter
4's versions are second tellings (R4, R5).

## 4. Structure and headings (S)

**S1. §4.1 order.** Today the order is: the corpus, then the alternatives, then
aggregation, then the resolution, then *what the graph is* (l.3817), then sparsity,
then the pre-intrusion gap. Propose: what the graph is (l.3817's sentence, first),
then the corpus and why, then aggregation and resolution, then sparsity and the
pre-intrusion gap. This is a T1 move: the sentences are unchanged.

**S2. §4.2 order.** Lead with the partition: the four profiles and their counts,
from l.3913–3917. Then how flows were classified (terminal tactic, cross-check,
19 of 38). Then why objective is used in place of motivation (l.3885–3891). Then
operator concentration. This answers the heading first (T1).

**S3. §4.3: the pre-intrusion overlay is used before it is defined.** The
definition's $M_0$ item says "(defined after Table~\ref{tab:gspn-notation})"
(l.4091). The overlay paragraphs (l.4256–4271) come after both floats. Propose
moving them to directly after the enumerated list, so that $M_0$ points back. This
is a T1 move.

**S4. §4.4.1 holds seven topics in 581 words:**
1. replaced cost;
2. the targeted scenario;
3. the verdict;
4. the dwell-only tactics;
5. sink-retrace and stall;
6. what the simulator owns;
7. nothing carried between runs, and the ceiling.

The affinity board leaves the §4.4 subsection headings open (its §6). Propose
keeping the one subsection, ordered as the runtime loop runs (1 → 3 → 4 → 5 → 6
→ 7). Topic 2 moves up to sit beside §4.4.1's first sentence, or into §4.5 (X3).

## 5. Figures (F): owed

Not scrutinised in this pass. Two flags for the full pass:

- **F1.** Figure 4.4's caption (the runtime loop, in §4.4.1) is 197 words. A
  legend-length caption means the figure is under-labelled. Run
  `scrutinise-figure`.
- **F2.** Figures 4.2 and 4.3 still carry "DRAFT STATE: session stand-in, Marc's
  to rewrite" captions (l.3806, l.3875).

## 6. Tables (T): owed

Not scrutinised in this pass. The notation table (`tab:gspn-notation`) defines
$\varphi$ before the §4.3 hand-over uses it (l.4240), so that use is **not** a
defect.

---

## 7. Prose ledger

Line numbers are as of 2026-10-02 and drift with edits. Δ is approximate. Tiers
follow `critique_protocol.md`: T1 is a deletion or move, T2 a suggestion built
from Marc's words that he must re-word or ratify, and T3 is content. "Re-opens"
names the ruling an entry overturns on merit.

### Opener (140): keep

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| O1 | keep | 0 | Ratified connective prose. It says what each section answers, in sub-question order |

### §4.1 Attack graph construction (493 → ≈335)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| A1 | l.3744–3749 "We made the attack graph using Attack Flow. Attack Flow is maintained by the Center for Threat-Informed Defense (CTID), which sits under MITRE Engenuity \citep{ctid2025attackflow}. This is a project that documents the per-incident behaviour of an APT attacker --- done by adding sequence and dependency to APTs' known tradecraft. Attack Flow maintains a documented attack-behaviour corpus spanning 2017 to 2024." → "We made the attack graph from the Attack Flow corpus (Section~\ref{…3.1.3}), which spans 2017 to 2024 \citep{ctid2025attackflow}." | −45 | T1 + T2. **X1**, M24. Chapter 3 introduces Attack Flow, CTID and what a flow records (§3.1.3); the ch3 ledger's §10 flagged this as "ch4's third introduction of Attack Flow" |
| A2 | l.3750–3758 "Other approaches were considered … other approaches could not provide." → *suggestion:* "A human analyst drew every dependency in Attack Flow's corpus. Co-occurrence mining gave low coverage and keyword mining poor fidelity (Appendix~\ref{app:cooccurrence}), and NLP-based approaches produce threat intelligence of too low a fidelity to defend \citep{rahman2025, buchel2025}." | −30 | T2, G3. Absorbs M19 and M27 ("over the life of the project"). The comment trail's AVAILABLE argument (co-occurrence can express no loop) stays Marc's call. **Re-opens** the 2026-08-16 sign-off at ~400 words |
| A3 | l.3780–3800: cut "Instead of using each incident independently of the others --- where there is little insight in the corpus ---"; cut "But aggregation makes the logical AND vacuous, because there are many OR paths which an attacker can traverse."; cut "having chosen the input for its fidelity, we chose the resolution for coverage" and "and we judged this trade-off between coverage and fidelity was necessary to capture the generalised behaviour of APT attackers" | −55 | T1, G4. The AND point is M25: §4.3 l.4108 keeps it with its mechanism (one token). The fidelity/coverage trade is stated once ("The node resolution, tactic or technique, trades fidelity for coverage") and the 88 % sentence carries the reason. Then S1's move |
| A4 | l.3821–3826 "We are using human-analyst-drawn dependency graphs, and this is sparse input data. The edge weight is a recurrence value; therefore, …" → "The corpus is sparse, so the edge weight is a recurrence value, and we cannot rely on these weights alone …" | −12 | T2 |
| A5 | l.3830–3846 "Another limitation we encountered was an issue with a lack of pre-intrusion dependencies" → "The corpus also lacks pre-intrusion dependencies"; "passive recon" → "passive reconnaissance"; cut "so we would have to address it regardless of our input" | −18 | T1 + T2. M41, M42. "persistent across CTI" stays uncited unless Marc has a source (flag, do not supply) |

### §4.2 Attack profiles by objective (464 → ≈370)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| B1 | l.3862–3866 "The literature tells us that APT attackers are not a homogeneous group … We cannot produce an APT attacker model that could be considered behavioural, because the attack graph carries so many different motivations and objectives which influence behaviour" → *suggestion:* "APT attackers are not a homogeneous group; they are distinguished by campaign-level intent. One model of the whole attack graph would mix objectives, and objectives influence behaviour \citep{alshamrani2019}." | −10 | T2. As written, the sentence reads as though the dissertation cannot build a behavioural model at all |
| B2 | l.3885–3886 "Motivation is something that we cannot ascertain. We can see what an APT group did; this is an analyst inference." → M32's suggestion: "Motivation is an analyst inference; what an APT attacker did is recorded." | −8 | T2. M32: "this" attaches to the observed act, so the sentence says the opposite of what it means |
| B3 | l.3895–3904: cut "Attack Flow is composite data, with structure and dependency manually drawn to a high level of fidelity; however, coverage is an issue."; "Attack Flow also uses and operationalises … because we could not rely on the terminal tactic alone." → *suggestion:* "Some flows end before their objective, because the attack graph's construction removed their nodes that ATT&CK does not name, so the terminal tactic alone could not be relied on." | −60 | T1 + T2, G4 (the fourth fidelity/coverage telling). **Claim flag:** is the removal of non-ATT&CK nodes the cause of incompleteness, or one cause among others? Verify against `objective_partition_rationale.md` before ruling |
| B4 | l.3906–3920: S2's move; "Hence, we settled on a four-way partition based on the shape of our corpus." → cut "Hence,"; resolve the standing [3b] marker ("based on the shape of our corpus" vs "based on the terminal tactic"); cut "There are four, and"; M31 "which provides enough coverage" → "Appendix~\ref{app:rejected-partitions} compares finer partitions" | −20 | T1 + T2. 19 of 38 is verified (tab_B-2a overrides: 12 + 1 + 6 + 0) |
| B5 | l.3929–3942, the operator-concentration paragraph: keep | 0 | Marc's pass-5b sentence and the Conti example |

### §4.3 Generalised stochastic Petri-net formalism (1 125 → ≈980)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| P1 | l.3966–3979 "We needed a data structure to pipe in the attack profiles as an input, and this is what the Petri nets provide. We ruled out attack graphs … which provides the immediate transitions we are using." → *suggestion:* "The attack profiles need an executable form, and a Petri net provides it. Attack graphs supply no timing, and directed acyclic graphs cannot hold the attack graph's cycles. A stochastic Petri net times every transition, and a deterministic and stochastic Petri net adds a fixed delay the model does not need; the generalised stochastic Petri net (GSPN) \citep{marsan1984} supplies the immediate transitions the model uses." | −25 | T2, G3. M12, M18; M17 is already applied. This keeps the 2026-08-17 contract (a sentence for the alternatives) |
| P2 | l.4094–4099 "The implementation carries every pair the profile's … subgraph admits … so the two nets are the same object in execution." → a footnote, or Appendix B | −60 | T1 move. An implementation-equivalence note for the examiner, not a step in the definition. M44 ("the two nets" has no antecedent) |
| P3 | l.4099–4102 "which is what makes the net plug and play: each attack profile is an input, and structure and semantics stay apart" → "so each attack profile is an input to one construction" | −10 | T2. M44 ("plug and play") |
| P4 | l.4256–4271, the overlay: S3's move; cut "The tactics reconnaissance and resource development, before initial access, are not well connected in our attack profiles." (§4.1 A5 says it); cut "so that we could model the runtime behaviour of the APT attacker model"; M28 "We can assume that they perform these because we know they do that …, and it is defensible because nothing detects pre-intrusion activity anyway." → M28's suggestion | −45 | T1 + T2. The comment trail rules the defender-validity sentence and the observability-boundary naming **out** (Marc, 2026-08-16, do not re-flag). This entry only cuts and does not add either |
| P5 | l.4285 "But there are limits to what the Petri net can provide:" → "The Petri net leaves two things to the join:" | −5 | T2, minor. "Limits" reads as a weakness of the formalism when it means a division of labour |

### §4.4 preamble (222 → ≈210)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| I1 | l.4362–4367: keep, and land the OWED clause (C1) | +15 | The "three inputs the join carries" no longer counts §4.4.5 |
| I2 | l.4413–4424, the four bases: keep, adding the memory's factor of three to the judgement list (C1) | +5 | Ruled 2026-09-25 |
| I3 | l.4429–4432: cut "Section~\ref{sec:ablation} removes the partition into attack profiles, the failure matrix and the vulnerability memory in turn and reports what changes." | −25 | T1. §4.4.4 (l.4888) and §4.4.5 (l.4964) each point at their own ablation, and §5.4 opens on the list. Keep "Three values are not tested: …", which is the only place that disclosure is made. **Re-opens** the 2026-09-26 SIMPLIFIED placeholder, which was "for Marc's redraft" |

### §4.4.1 Runtime loop (581 → ≈470)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| R1 | l.4457–4460: cut "; the run ends when a target is compromised" | −7 | T1, **X3** |
| R2 | l.4566–4568 "We employed a sink-retrace policy, because the token would frequently hit sinks and terminate the run --- a concession to the thinness of the corpus; we retrace the edge travelled." → "When the token reaches a sink, a place the corpus gave no exit, it retraces the edge it travelled, a concession to the thinness of the corpus." | −12 | T2. M39 ("frequently"); the definition comes before the reason |
| R3 | l.4578–4588 "The simulator we are inheriting largely models … so we maintain that 20-second confusion penalty. Not all the timing is supplied by the Petri net: the confusion penalty is the exception. The same rule covers everything else the simulator owns." → *suggestion:* "The simulator models the attacker's confusion through a 20-second confusion penalty during certain attack actions, the one time the Petri net does not supply." | −35 | T2. Three sentences say "the simulator owns it". M22 ("arms", not yet defined) stays open in the sentence after. **Re-opens** the 2026-08-20 resolution ("all the tactic timing"); the suggestion keeps its logic |
| R4 | l.4601–4602 "That is the scheme-aware attacker Jalowski et al.\ \citep{jalowski2026} ask for, and this model is not one; Section~\ref{sec:future-work} returns to it." → "This model is not scheme-aware (property 8, Table~\ref{tab:attacker-properties}); Section~\ref{sec:future-work} returns to it." | −10 | T2, G5. Chapter 3 introduced Jalowski's ask (l.2810–2816) |
| R5 | l.4615–4617: cut "But it is extendable and modular: our Petri nets can be mapped to anything given an appropriate mapping, or a richer set of attack actions can be built that operationalises all of MITRE's tactics." | −35 | T1, G5. M33 ("anything") goes with it, and §7.2 carries the richer set. **The ceiling sentence stays**: it is a MUST-CARRY that chapter 5 cites (2026-09-08). This re-opens only the extensibility clause, which the connective-prose audit already called "a value close" |

### §4.4.2 Tactic dwell times (378 → ≈315)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| D1 | l.4632–4643 "We cannot derive the dwell times from anything built so far. The dwell times do not exist in the literature; they do not exist in CTI vendor reports. Prior papers describe this as inherently arbitrary: trying to put times on an attack \citep{…}. This is a parameter of the model itself, not an invariant." → *suggestion:* "Per-tactic dwell times are reported neither in the literature nor in CTI vendor reports; prior models that time attack steps estimate them \citep{bland2020, mcqueen2006, mendonca2023}. They are parameters of the model." | −20 | T2. **X2**, M34. "Invariant" is §4.4.1's word for what the simulator owns, so it should not be reused here; the one-sentence paragraph merges |
| D2 | l.4647–4649 "We derived our dwell times for the tactics from the dwell times of MTDSim. What we could take from the six attack actions, we used directly, and we extrapolated the rest." → "We derived the dwell times from MTDSim's six attack actions, using their costs directly where they apply and extrapolating the rest." | −12 | T2 |
| D3 | l.4726–4733: cut the second pointer "and the derivation is in Appendix~\ref{app:dwell-derivation}" (l.4659 gives it); "10 times" → "ten times"; M30: cut "we would assume," | −15 | T1. M48, M30 |
| D4 | l.4740–4746: cut "the behaviour of APT attackers is stochastic, described by a probability distribution rather than a fixed value." and fold its citation into "There is evidence in the literature for stochastic attack behaviour" | −18 | T1. Two sentences make one claim. Keep the M46 must-carry (l.4746–4747) |

### §4.4.3 Tactic-to-action mapping (171 → ≈115)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| M-a | l.4774 "No such mapping exists in the literature, so we used our best judgement." → "No published mapping exists, so $\varphi$ is declared." | −4 | T2. M35 |
| M-b | l.4776–4779 cut "We use a direct mapping with certain constraints: a tactic can go to only zero or one attack actions, and a tactic can only execute either zero or one attack actions in the simulator at a time, so this problem remains tractable." | −35 | T1. l.4773 already says "to at most one of the simulator's attack actions". If tractability is the reason, keep only "so the mapping stays tractable" |
| M-c | l.4781 "many tactics are dwell-only" → "seven of the 15 tactics are dwell-only" | 0 | T2. M36 (verify the count against Figure 4.4 before applying) |
| M-d | l.4809–4814, the total mapping and Caldera → *suggestion:* "A total mapping, one attack action for every tactic, made the model a tightly ordered state machine run stochastically (Appendix~\ref{app:experiment-one})." Caldera: keep only with its real reason (M38) | −20 | T2 + T3, G3. M37, M38 |

### §4.4.4 Failure matrix (411): keep, one question

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| F-a | l.4891–4892 "These are threat-model parameters for this simulator, not real-world values." | −12? | **Question for Marc.** Is this a second must-carry, or does "every value in it is our judgement" (l.4861) together with the dwell must-carry already cover it? G4 |

### §4.4.5 Vulnerability memory (206 → ≈195)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| V-a | l.4959 cut "The idea is that the attacker compromises more of the network." | −10 | T1. The hypothesis sentence after it states the effect specifically, and that hypothesis stays (ruled 2026-09-29) |
| V-b | Gate 1, open since 2026-09-29: the paragraph opens on motivation ("Any attacker learns"), not on what the memory does | 0 | T2, already Marc's item. "Any attacker learns" is also an uncited universal |

### §4.5 Evaluation metrics (1 119 → ≈1 085)

| ID | Before → after | Δ | Tier / note |
|---|---|---|---|
| E1 | keep the opener's stopping rule, the authoritative one (X3) | 0 | |
| E2 | l.5023–5026, the Hong et al. contrast under *Distinct attack paths* | −35? | **Question.** It distinguishes a construct this dissertation no longer names after Hong (the metric is "distinct attack paths"). If the open call "APV keeps Hong's name; raise it with Dr Hong" is settled, the sentence may go |
| E3 | the word-equations for relative tactic occurrence, distinct attack paths, ASP and NCR reduction | 0 words | **Question.** Each restates the sentence above it (CLAUDE.md: "a symbol is used only where the prose needs it"). It costs page space, not words. Keeping them for uniformity across the eight metrics is defensible |

---

## 8. Content the chapter lacks (C), named, not drafted

- **C1. The vulnerability memory in the §4.4 preamble.** OWED 2026-09-28 at l.4368:
  the "three inputs the join carries" sentence, and the factor of three among the
  values based on judgement. Marc's wording.
- **C2. "Learns nothing about the defence within a run"** (l.4598–4600). OWED
  2026-09-28: the attacker now learns which vulnerabilities worked (§4.4.5), so
  "learns nothing about it" needs its object to stay MTD.
- **C3. A chapter close.** The chapter ends on time lost's sign (l.5205–5206). Chapters
  2 and 3 close with a hand-over (`connective_prose.md` (b)). One sentence on what
  chapter 5 runs the model on would do. It is session-generated connective prose
  under the 2026-09-25 green light, to be ratified on read.

## 9. Factual corrections and contradictions (X), verified

- **X1. "MITRE Engenuity" (l.3746).** The bib entry `ctid2025attackflow` gives the
  author as the Center for Threat-Informed Defense and `howpublished = {MITRE}`.
  Chapter 3's ruled wording is "MITRE's Center for Threat-Informed Defense" (ch3
  ledger P8: "'Engenuity' is in neither the cited v3.2.0 document nor the bib
  entry"). A1 removes it.
- **X2. "The dwell times do not exist … in CTI vendor reports" (l.4633–4635).**
  - Chapter 1 (l.231) and chapter 3 (l.1089) both cite M-Trends for how long whole
    intrusions last. Only *per-tactic* times are absent, so the sentence needs the
    qualifier. (The ch3 ledger G2 named this contradiction, and it is still open
    on chapter 4's side.)
  - Mendonça et al. call their unsourced values "reasonably estimated, as they
    were not found in the literature" (`extractions/mendonca2023.md` l.116). That
    supports *absent from the literature*, not *inherently arbitrary*. Bland
    ("notional and randomly selected") and McQueen ("somewhat arbitrarily") do say
    arbitrary (the tex trail at l.4636).
  - D1's suggestion uses "estimate", which all three support.
- **X3. When does a run end?**
  - §4.4.1 (l.4459–4460) says the run "ends when a target is compromised".
  - §4.5 (l.4981–4985) says it ends at a target, at more than 80 % of hosts
    compromised, or at the time limit.
  - The code holds the 80 % stop (`mtdnetwork/component/time_network.py:55`,
    `terminate_compromise_ratio=0.8`).
  - **Owed before applying:** trace whether the targeted path calls it. Then keep
    one statement, §4.5's (R1).
- **X4 (out of chapter, flag only).** Appendix B.2's captions give "Attack Flow
  published export v3.1.1", while the bib entry says "Version 3.2.0". The same
  captions still carry M47's `\texttt{objective_…}` keys.

## 10. Stale records to refresh once the rulings land

- `_writing_guide.md`: the ledger line and reallocation record (G1).
- `2026-09-25_ch4_mark_risk_ledger.md`: retire it once every M entry absorbed here
  carries a ruling. M47 (a generator change) is the only one not in this chapter's
  prose.
- `docs/notes/ch4_methods/README.md`: the shape, if S1–S4 move anything.
- The handoffs README: prune this line in the commit that ships the work.

## Validation gate

- Every G / S / prose / C / X entry carries Marc's ruling: applied, declined or
  amended.
- The open M entries listed in G2 have each been applied or declined, and the grep
  sweep (the phrases in the mark-risk ledger) shows none in live prose.
- The chapter's prose sits within ±5 % of the target G1 sets, measured as in §0.
- X3 is traced in code, and one stopping rule is stated once.
- The PDF builds with 0 undefined references and no new overfull boxes. The
  chapter's pages are re-rendered and read.
- A cold reader who holds only chapters 1–3 and the revised chapter 4 can state:
  what the attack graph is and where it came from; what an attack profile is and
  how many flows each holds; what fires when, in one tactic of one Petri net; which
  values were judged and which were measured; and how a run ends.

## Hard constraints

- Nothing applied unratified. Marc's dictated units change only by the deletions
  and merges ratified here.
- Must-carries stay:
  - the ceiling sentence (§4.4.1);
  - "model parameters anchored to this simulator, not real-world measurements"
    (M46, §4.4.2);
  - "Three values are not tested" (§4.4 preamble);
  - the 29-flow weighting (§4.3, B9).
- Do-not-re-flag rulings in the tex trail hold unless Marc reopens them: the
  defender-validity sentence (2026-08-16); the routing-ablatability must-carry
  (cut); the vulnerability-memory pass-5 cuts.
- Terms per the registry: *attack action*, *Petri net*, *base weight*, *decision
  place*, *failure matrix*, *time limit*, *deployment*.

## Reading list

- `docs/thesis/dissertation.tex` l.3451–5209, prose and `%` trails.
- [`2026-09-25_ch4_mark_risk_ledger.md`](2026-09-25_ch4_mark_risk_ledger.md) §M,
  for the before/after wording of each absorbed M entry.
- [`2026-09-15_ch6_discussion_affinity_board.md`](2026-09-15_ch6_discussion_affinity_board.md)
  §6 (the §4.4 headings) and the §7.2 row (G5).
- [`2026-09-30_ch3_lit_review_scrutiny.md`](2026-09-30_ch3_lit_review_scrutiny.md)
  §10 (its out-of-chapter flags on chapter 4).
- `docs/sources/extractions/mendonca2023.md` l.105–120 (X2).

## Out of scope (explicitly)

- Re-running anything, and any number in §4.5 or chapter 5.
- Figure regeneration: F1 and F2 go through `scrutinise-figure`.
- Drafting replacement prose. The *suggestions* above are built from Marc's words
  for him to re-word or ratify.
