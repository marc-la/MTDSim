# Chapter 7 and the appendices: structure before drafting

**Status:** NOT RULED. Structure only; no prose. Opened 2026-10-09 (Marc: "a rough overdraft ... think about the structure ... what questions do I need to answer ... future work ... which [registry items] should we actually put into the appendix ... look at the structure of the appendix as a whole").

**Line numbers** are for `docs/thesis/dissertation.tex` at commit `0a61f2c6`: ch6 8431, registry 9508–9727, ch7 9732, AI Use Declaration 9833, appendices 9838 (A 9840, B 9872, C 10101, D 10369, E 10550).

**Standing rule:** every line inserted outside chapter 6 is proposed first (before/after) and applied only on Marc's yes. That covers ch7 and the appendices. §6 holds the proposals.

---

## 1. What an examiner expects of the conclusion

- **UWA has no separate Conclusion criterion** (CITS4001 marking guide; harvest `2026-10-07_ch6_discussion_assembly_harvests/D_examiner_benchmarks.md` §1). Ch7 is marked under *General* ("well-structured", consistent) and under *Discussion* items 1, 5 and 6: results tied to the introduction; improvements suggested; further work and loose ends named.
- **Evans, Gruba & Zobel 2014:** "summaries are not conclusions". Ch7 states answers and their consequence. It does not walk the chapters again.
- **Bunton 2005 (JEAP 4(3); planning source, not in references.bib), thesis conclusion moves:** restate the purpose; consolidate the findings as claims; give implications; recommend future research; close. These map onto preamble → contributions → future work. *Corrected 2026-10-15 (§15): this is Bunton's humanities model; his science-and-technology model ends on future research. See `conclusion_conventions.md` §(f).*
- **Ch1 must match ch6 and ch7** (Marc 2026-10-09). The RQ and SQ wording is verbatim from ch1 356–368. The contributions are ch1's two, at 548–556.
- **Failure modes:**
  - repeating the abstract in the past tense;
  - a new number or claim that ch6 did not make;
  - hedging every sentence ("saying almost nothing");
  - a future-work list cut loose from the limits it lifts;
  - future work that leaves a ch6 promise unpaid.

**Budget: about 800 words.**

| Part | Words |
|---|---|
| Preamble | ~120 |
| Contribution 1 | ~170 |
| Contribution 2 | ~170 |
| Future work | ~330 |

## 2. The hedges that carry the most meaning per word

Each hedge is a phrase, never a sentence of its own. Use each one once, where its claim is made.

| Phrase | What it bounds | Home |
|---|---|---|
| "in MTDSim" | one simulator, its default network | 6.5 ¶1 |
| "the APT attacker model", never "APT attackers", for a measured result | the model is the behaviour the 38 attack flows document, not an APT | 6.5 ¶4 |
| "can depend" (general) / "depends" (in MTDSim) | measured on one simulator; the transferable form is 6.4's | 6.4 ¶1 |
| "changes what an evaluation finds, but is not sufficient on its own" | CTI grounding | 6.3 close |
| "at no cost" / "a deployment that costs nothing" | faster always wins; no interval is chosen | 6.5 ¶1 |
| "not which of its parts" | the bundle; the effect rests on tactic durations and order, which no run separates | 6.5 ¶2 |

## 3. Slot sheet (job + facts + ceiling; no content)

### Preamble: the RQ answered (3 sentences)

- **S1.** *Job:* answer "How does MTD perform against APT attackers?" at the measured scope. *Facts:* in MTDSim, MTD performs differently against the APT attacker model than against the baseline attacker. The difference runs by MTD layer: the host layer disrupts the APT attacker model more and the service layer less. No MTD mechanism ranks first against both at any deployment interval (6.2 close). *Ceiling:* "APT attacker model"; "in MTDSim"; no verdict on a mechanism; never "better".
- **S2.** *Job:* the part that reaches the RQ's "APT attackers". *Facts:* a ranking can depend on the attacker model, so how MTD performs against APT attackers cannot be read from an evaluation against a simplified attacker alone (6.4 ¶1). *Ceiling:* "can"; not "MTD fails against APTs".
- **S3 (optional).** *Job:* the bound that carries most. *Facts:* it rests on what MTDSim's attack actions and deployment rules let the model do, with deployments that cost nothing (6.5 ¶1). *Ceiling:* one clause per root, plus a pointer.
- *Skipped:* a restatement of the problem. Ch1 P3 carries it, and S1 can fold it into a subordinate clause if Marc wants one.

### Contributions: ch1's two, now as delivered

How it differs from ch1:
- Ch1 states each contribution as a promise in one or two sentences, with no evidence.
- Ch7 states each as delivered, answering its SQs, with its evidence, what it changes for whom, and its bound.
- The order and the nouns stay ch1's, so the reader can lay the two lists side by side.
- Each contribution is a paragraph, not a bullet. Each needs the room for its evidence and its bound.

**Contribution 1** (answers SQ1 and SQ2; ch6 6.3):
- **a. Claim.** An APT attacker model, recovered from 38 attack flows, aggregated and split by objective into four attack profiles. It is executed in MTDSim as a Petri net over its six attack actions, and it runs in place of the baseline attacker. *Ceiling:* "built", "runs"; never "reproduces APT behaviour".
- **b. Evidence against the field.**
  - Two properties in full and five in part. Three recent attacker models have at most one in full (Table 6.1).
  - The gains over the baseline attacker: choice of attack strategy in full, and detection avoidance in part.
- **c. Impact.** Another MTDSim evaluation can run its MTD against the APT attacker model beside the baseline attacker (routed from 6.4 ¶3, §16b). Another simulator would need the interface: the mapping, the tactic durations and the failure handling (6.4 ¶3).
- **d. Bound.** CTI grounding changes the finding but is not sufficient on its own. What it adds reaches the result only as far as the attack actions allow. The failure matrix and the vulnerability memory move NCR negligibly (6.3 close).

**Contribution 2** (answers SQ3; ch6 6.2 and 6.4):
- **a. Claim.** In MTDSim, the most effective MTD mechanism depends on the attacker model. The two attackers' rank 1 share no mechanism at any deployment interval. The host layer disrupts the APT attacker model most, and the service layer the baseline attacker. *At most one number;* candidate: the host layer keeps half of NCR off to 1 000 s against 100 s. The 0.92/0.36 pair is already in the abstract and ch1, so don't print it a third time.
- **b. What it is not.**
  - It is not that one attacker model is the better one.
  - Which part causes the reversal was not separated. It rests on the tactic durations and order.
- **c. Impact for evaluators** (6.4, compressed). An evaluation should report:
  - its ranking with the attacker model behind it;
  - shared attacker models, which comparability needs;
  - the lowest NCR reduction across attacker models as the lower bound where the attacker is unknown;
  - for a learned deployment strategy, a test against an attacker model it was not trained on (MTDShield).
  - *Optional,* routed from 6.4 ¶3: before the runs only the direction could be predicted, so an attacker model has to be run, not reasoned about.
- **d. Bound.** One simulator, its default network, deployments that cost nothing.

### Future work: ranked by the limit each item lifts, in 6.5's order

*Lead:* one sentence saying that each item lifts a limit of Section 6.5. *Close:* the dissertation's last sentence names the next step.

| # | Limit lifted (6.5) | Work | Registry and other sources |
|---|---|---|---|
| FW1 | The attack actions (root 1), and one token | Attack actions without a fixed order and with a context per token, which then allows more than one token (parallel lines of a campaign). Actions on objectives, and a failure that knows MTD caused it. Lifts at most two marks; detection avoidance also needs a detector. | F8, F9; placeholder items 1 and 4; 6.3 sentence routed in §16b |
| FW2 | Pricing nothing (root 3) and the deployment interval | A detector that depends on the attacker and drives MTD (IDS-paired, risk-based). Deployment overhead and loss of service beside NCR reduction, so a sweep can choose an interval. | F5, F11; placeholder item 2; §14a |
| FW3 | The bundle (internal) | The baseline attacker given the APT attacker model's tactic durations, and a uniform-weight Petri net: they separate pace from order from the CTI weights. Then an edge ablation tied to mitigations. | F13, F1 |
| FW4 | The corpus (external) | Attack flows drafted by language models from APT-only reports and checked against analysts'. The 18 attributed attack flows alone. A larger corpus for a partition-size sweep. | F10, F12, F2 |
| FW5 | Reach | Other networks, and which network features decide success. Longer runs. An attacker that times the deployment interval (property 8, Table 6.1's cross). Learned deployment strategies retrained and tested against an unseen attacker model. Emulation. | F3 (B1), F4, F6; placeholder items 3, 5 and 6; §14a |

**Promises ch6 makes with `\ref{sec:future-work}`, all of which must be paid:**
- one token (FW1);
- the default network (FW5);
- 15 000 s runs (FW5);
- simulation only (FW5);
- existing MTD at a deployment interval (FW2);
- the baseline attacker with the APT tactic durations (FW3);
- language-model attack flows and the 18 attributed flows (FW4).

All are covered.

**Left out on purpose:**
- B4, B5, B12, B13. These are hypotheses about ch5 floats, not directions.
- F7, threat modelling: its literature is unchecked.
- The ruled-out directions in the ch7 comment block (stealth semantics, MTD-scheme awareness, full incentive rationality). They are stale against Table 6.1.

**Literature to check before wording FW2, FW4 and FW5 as gaps:** F3, F10 ("Attack Flow now drafts flows with AI" is unverified) and F11 (adoption barriers). Until then, word each as a direction, never as "no one has".

## 4. Registry triage, under the rule at 9515–9523

**Rule (1), must have a home.**
- No live item remains. A3 is ruled.
- B15, B16, B19, B20 and B21 are homed.
- A1's sentence is cut, and A2 reads off Figure 5.1(a).
- Checked 2026-10-09 against the ch6 prose.

**Rule (2), may go in: answers a question a ch5 float raises.** Recommended, all on disk and needing no runs:

| Item | Answers | Supports in ch6 | Verdict |
|---|---|---|---|
| B9 + B10 | "How do you know a host-layer deployment costs the APT attacker model its foothold, and why does user shuffle help?" | 6.2 ¶1 and ¶2. Both mechanisms are hedged "most likely"/"each deployment gives it a fresh chance"; B9/B10 are their direct check. | **In.** One table: no-foothold share and compromises by held account, per attacker, at 50–200 s. |
| B1 (+B2 as one line) | "What makes a run succeed?" (6.1 cold examiner) | Earns FW5's network item (F3) | **In.** One paragraph and a small table. |
| B14 (+B8) | "Do the attack profiles beat random partitions because of group size?" (examiners' corpus-size question) | 6.3 close ("grouping by objective carries structure") | **In,** labelled as a hypothesis. Per-group NCR beside `tab:ablation-random-partitions`' d. |
| B18 | French's examples point; adaptivity is "seen by construction" | 6.2 ¶1 mechanism made concrete | **If time.** It needs a tracer replay and a figure; second tier. |

Everything else stays in the registry: B2 standalone, B3–B8, B11–B13, B17.

**Labelling (rule text):** one appendix section, opened with a sentence saying these were chosen after the results were seen. Each answers a question a float raises, never chosen because it helps the argument. Each item gets a pointer from the ch6 sentence it supports. Pointers inside ch6 are free; a ch5 pointer is a proposal.

## 5. Appendix audit: fit for purpose?

**Overall shape is sound:**
- A, the proposal;
- B, which backs ch4;
- C, sensitivity;
- D, MTDShield;
- E, which backs ch5.

Each appendix opens on what it backs. The main text cites every section, either directly or through a table: B.1 at 3999, B.2 at 4009, B.5 through the tactic-durations table's caption (tab_4-4a), C.2 through `tab:value-bases` and `tab:parameter-register`, C.3 only through the appendix-C pointers in ch5 and 6.5.

**Findings, ranked:**

1. **"ASP reduction" is defined only in Appendix E (10564), but 6.4 ¶4 and 6.5 use it as a term (9204–9219, 9342).** A reader of ch6 meets it undefined. Fix inside ch6, free: gloss it at first use in 6.4 ("the share of ASP that MTD removes, Appendix E") and cut the later glosses.
2. **C.4 still carries `\prelim{2.5}` and `\prelim{2}` (10335, 10338).** These are 100-seed numbers that are still flagged. Check them against the 1 000-seed detector table, then drop the marks. Owed before submission.
3. **E has no sections, and its header comment says "PRELIMINARY: 100 seeds" (10549).** The comment is stale. Proposed sections, mirroring ch5:
   - E.1 MTD against each attacker: `tab:disruption`, `tab:eff-interval-values` and its ASP twin, `fig:eff-cross-arm-asp`.
   - E.2 Every metric at every condition: `tab:full-movement`, `tab:full-baseline`.
   - E.3 Ablation studies: `tab:ablation-attack-profiles`, `tab:ablation-random-partitions`, `fig:ablation-memory`, `tab:ablation-memory`.
   - E.4 Exploratory analyses: the §4 items.
4. **B's order is not ch4's.** B.5, tactic durations, comes before B.6 and B.7 (the mapping), but ch4 has the mapping (4775) before the durations (4856), and B's own opener says "in the chapter's order". Swap B.5 to sit after B.7. Labels are unchanged, so only the letters move.
5. **Duplication between ch6 and the appendices.** These are cut levers for ch6, not for the appendices:
   - 6.5 ¶3's list of untested values repeats C's opener (10114). The appendix is the home, so 6.5 can point to it.
   - 6.4 ¶2's detection-input sentence repeats D.4's last bullet. The appendix is the home.
6. **Appendix A is cited nowhere.** That's fine if UWA requires it bound in. Otherwise one ch1 footnote. Low.
7. **Nothing to cut in B–D.** Each table or figure backs a cited claim. B.1's three graph figures are a family at descending abstraction (ruled 2026-09-09), not duplicates.
8. **The AI Use Declaration is empty, but 6.3 (8934) cites it for the blind re-score.** An examiner who follows the reference finds nothing. It is not an appendix, but it is the most visible gap in the back matter.

## 6. Proposals outside chapter 6 (before/after; apply on Marc's yes)

**P15. Ch7 placeholders become the slot sheet** (comments plus one visible placeholder per slot). After: §3 above, as `%` slot comments under each heading, with the visible `[Placeholder]` lines kept. No new headings. The stale comment block (9791–9825, "WHAT ch5 HANDS THIS CHAPTER", dated 2026-09-09) moves to this handoff.

**P16. Appendix E sectioned, with an exploratory section.**
Before: one unheaded run of floats (10550–10637).
After:
```
\chapter{Supplementary results}
\section{MTD against each attacker}            % tab:disruption, tab:eff-interval-values(-asp), fig:eff-cross-arm-asp
\section{Every metric at every condition}      % the two landscape tables
\section{Ablation studies}                      % tab:ablation-*, fig/tab:ablation-memory
\section{Exploratory analyses}
\label{app:exploratory}
\noindent\emph{[Placeholder --- analyses chosen after the results were seen,
each answering a question a float of Chapter~\ref{ch:experiments} raises.]}
\subsection{Footholds under the host layer}            % B9  TODO
\subsection{Accounts reused under user shuffle}        % B10 TODO
\subsection{Successful runs with no MTD}               % B1 (+B2) TODO
\subsection{Attack profiles against random groups by size}  % B14 (+B8) TODO
\subsection{One run of the APT attacker model under MTD}    % B18, if time
```
Each existing linking sentence stays under its new section, unchanged.

**P17. Appendix B order:** move "How each tactic duration was set" after "A total tactic-to-action mapping". The text is unchanged.

## 7. Questions for Marc

1. **Contributions:** keep ch1's two, with SQ1 and SQ2 answered by the first and SQ3 by the second, and 6.4's guidance as the second's impact? *Recommended: yes. A third contribution would break the match with ch1.*
2. **Future work format:** five bullets ranked by the limit lifted (2 sentences each), or run-in paragraphs? *Recommended: bullets. The items are parallel, the order shows the ranking, and bullets cut connective words.*
3. **Last sentence:** name the attack actions as the next step? *Recommended: yes. Every result rests on them (6.3 close, 6.5 ¶1). This follows Marc's 2026-10-08 line that MTD optimised against the APT attacker model comes only after the assumptions are reduced.*
4. **Appendix:** B9+B10, B1 and B14 into E.4, with B18 only if time? *Recommended: yes.*

## 8. Marc's rulings (2026-10-09)

- Q1 contributions: **yes**, ch1's two (SQ1+SQ2, then SQ3; 6.4's guidance as the second's impact).
- Q2 future work: **dot points**.
- Q3 last sentence: **yes**, the attack actions as the next step.
- Q4 further analyses: **approved** (B9+B10, B1, B14; B18 if time). Marc: the appendix must be structurally clear to the examiner, every entry logically arranged and relevant, each with the reason it did not make the main argument. The further analyses emerged after the discussion was written, so they are **kept separate** from the supplementary results: their own appendix, not E.4 (P16 revised: E gets its three ch5 sections only; Further analyses becomes Appendix F).
- Next: Marc reviews the appendix structure, then the runs/recomputes for Appendix F.

## 9. The appendix, whole (proposed 2026-10-09, NOT RULED)

**Ordering rule:** appendices follow the order in which the main text first calls on them, which is chapter order:
- B backs ch4 (first cited at line 3999);
- C backs ch4's declared values (4966);
- D backs ch5's set-up (6067);
- E backs ch5's results (7518);
- F backs ch6.

A is the record of the plan. **Each appendix opens with one sentence** naming what it backs and its order (B, C and D already do; E and F need one). **Each section states its reason for not being in the main text.**

| App | Backs | Sections, in order | Why it is not in the main text |
|---|---|---|---|
| A Original honours proposal | the plan | (the proposal) | record of scope as proposed |
| B Supplementary material for the APT attacker model | ch4, in its order | B.1 edges from mining; B.2 techniques or tactics as nodes; B.3 attack profile of each attack flow; B.4 edges of the attack profiles; **B.5 reasons for the mapping; B.6 a total mapping; B.7 how each tactic duration was set** (P17 swap); B.8 rules of the failure matrix | per-row reasons and rejected alternatives; ch4 states each choice |
| C Supplementary sensitivity analyses | ch4's declared values | C.1 tactic durations across their bands (+ the ranking at both band ends); C.2 the exponential delay; C.3 the failure matrix's distance factor; C.4 attack confidentiality and the scan detector | robustness, not results; the main text cites the verdict |
| D MTDShield as run | ch5's MTDShield arm | D.1 selection; D.2 settings; D.3 changes made to run it; D.4 known limitations; D.5 behaviour observed | reproducibility of a third-party agent |
| E Supplementary results | ch5, in its order | **E.1 every metric at every condition** (5.2, 5.3: `tab:full-movement`, `tab:full-baseline`); **E.2 MTD against each attacker at every deployment interval** (5.3: `tab:disruption`, `tab:eff-interval-values`, ASP reduction defined, `fig:eff-cross-arm-asp`, `tab:eff-interval-values-asp`); **E.3 ablation studies** (5.4: `tab:ablation-attack-profiles`, `tab:ablation-random-partitions`, `fig:ablation-memory`, `tab:ablation-memory`) | full grids; ch5 prints the comparison |
| **F Further analyses (new)** | ch6, in its order | F.1-F.5 below | emerged after the discussion was written, after the results were seen; kept apart from the planned evaluation |

**The opener for F** (slot, not prose): these analyses were run while ch6 was written, after the results were seen. Each answers a question a ch5 float raises. None enters the main argument: each checks a mechanism ch6 names, or sharpens a hypothesis. They follow ch6's order.

| Section | Question, from which float | Content | Supports | Why not in the main argument | Source; new runs? |
|---|---|---|---|---|---|
| F.1 Successful runs with no MTD | Why does each attacker succeed where it does? (`tab:unopposed-summary`) | Success by seed. The profiles succeed almost only where the baseline attacker does: ASP 0.06-0.20 there, at most 0.017 elsewhere. Pairs of profiles succeed on the same seed 3-6x more often than chance. One line from B2: under service diversity at 200 s, successes sit on seeds that succeed with no MTD. | 6.1 ¶2; FW5 (network features) | a property of MTDSim's networks, not of either attacker | recompute from `ch5_s531_unopposed/runs_reported.jsonl`; no runs |
| F.2 Footholds under the host layer | Why does the host layer reduce the APT attacker model's NCR most? (`fig:eff-cross-arm`) | Share of runs that compromise no host, per attacker, under the three host-layer mechanisms at 50-200 s: 0.69-0.89 against 0.03-0.20 | 6.2 ¶1 ("regains its place only at lateral movement") | checks a mechanism ch6 states; the claim stands on ch5's floats | recompute (`denied_share`) from `ch5_defended/runs_reported.jsonl`; no runs |
| F.3 Accounts reused under user shuffle | Why does user shuffle raise the APT attacker model's NCR? (`tab:eff-interval-values`, `tab:disruption`) | Compromises by a held account per run at 200 s, with no MTD against user shuffle: APT 1.30 -> 2.44, baseline 5.18 -> 7.56 | 6.2 ¶2; 6.4 ¶3 | a property of MTDSim's user-shuffle rule, not of MTD | recompute from the `records` field; the s9 count was ad hoc, so a script is needed; no runs expected (verify) |
| F.4 One run of the APT attacker model under MTD (if time) | What does one disruption look like? (`fig:aio-adaptivity`) | One seed traced with no MTD against IP shuffle at 200 s: the deployment, the failed attack action, the Petri net's route back, the time to the target | 6.2 ¶1-2; 6.3 (adaptivity seen by construction) | an illustration of one run, not a result | movement tracer replay of one seed, two conditions; minutes |
| F.5 Attack profiles against random groups by size | Do the attack profiles beat random partitions through their size? (`tab:ablation-random-partitions` prints only d) | NCR (and ASP) per group: random groups of 19, 7, 7 and 5 attack flows against c1-c4 (B14), with B8 | 6.3 close ("grouping by objective carries structure"); 6.5 corpus threat | a hypothesis on four points; says nothing of fidelity | `partition_control_numbers.json` (NCR); ASP recomputed from `runs_partition_control.jsonl`; no runs |

Each F table comes from a generator in `tools/` writing a numbers JSON, following `results_section_workflow.md`.

**Also owed in the back matter:**
- C.4's two `\prelim` values, to check at 1 000 seeds;
- E's stale "PRELIMINARY: 100 seeds" comment;
- a ch6 first-use gloss of ASP reduction that points to E.2;
- the AI Use Declaration.

### 9a. Headings read as table-of-contents lines (Marc 2026-10-09)

Marc: "the appendix is listed in the table of contents and vacuous or clearly unwarranted section headers is a bit hard to follow". The contents list every appendix section (dissertation.toc, lines 77-98).

**Test for each heading:**
- Read cold in the contents, it says what the section holds.
- It earns its own line: its own float, or its own question.

| Now | Problem | Proposed |
|---|---|---|
| C.2 The exponential delay | names a thing, not what is tested; breaks C's "Robustness ..." pattern | Robustness to the shape of the tactic durations |
| B.7 (now B.6) A total tactic-to-action mapping | reads as the mapping used | Mapping every tactic to an attack action |
| D.1 Selection | vacuous out of context | The agent chosen |
| D.2 Settings | vacuous | The agent's settings |
| D.3 Changes made to run it | "it" has no antecedent in the contents | Changes made to run the agent |
| D.4 Known limitations | whose? | Known limitations of the released agent |
| D.5 Behaviour observed | vacuous | The agent's choices in the runs |
| E (no sections) | eight floats behind one contents line | E.1 Every metric for each attacker; E.2 MTD's effect on each attacker at every deployment interval; E.3 The ablation studies in full |
| F (new) | -- | F.1 Where each attacker succeeds with no MTD; F.2 Runs with no foothold under the host layer; F.3 Accounts reused under user shuffle; F.4 One run under MTD, traced (if time); F.5 Attack profiles against random groups of the same size |

**Kept as they are:**
- A;
- B.1-B.5;
- B.8;
- C.1, C.3, C.4.

Each says what it holds and carries its own float.

**B.4 (edges of the attack profiles)** is one figure and one sentence, but ch4 cites it on its own (line 4203), so it keeps its line.

**No section is unwarranted** after these changes: each holds its own float or answers its own question.

### 9b. The three front lists read together (Marc 2026-10-09)

- Marc: the examiner reads the contents, the list of figures and the list of tables together.
- **Superseded 2026-10-14:** the list of figures and the list of tables are cut (Marc: three pages for little value). Only the contents remain; the short-caption proposals below are moot.
- The "Owed before submission" page was removed (commit 35db0030; no `\owed` mark remains).
- The contents print to subsection depth (cls `tocdepth` 2), so the run-in paragraph headings do not print.
- **The main-text contents read cleanly.** Each heading names its content, and ch5 and ch6 mirror each other in 5.2/6.1 and 5.3/6.2.

Short captions that fail the cold-read test (proposals; each changes only the `[...]` short caption):

| List | Now | Problem | Proposed |
|---|---|---|---|
| LoT E.4, E.5 | MTD mechanisms and deployment strategies against APT attacker model, with intervals | missing "the"; "intervals" reads as deployment intervals | Every metric for the APT attacker model (the baseline attacker), with 95 % intervals |
| LoT E.6 | ... at every MTD and deployment interval | "every MTD" | The APT attacker model with and without the attack profiles, at every MTD mechanism, deployment strategy and deployment interval |
| LoT E.2, E.3 | NCR (ASP) reduction under each attacker, by MTD and deployment interval | MTD acts against an attacker, not under it | NCR (ASP) reduction against each attacker, by MTD mechanism and deployment interval |
| LoT C.2 | The declared inputs and what moved | "what moved" is vague | The declared values of the APT attacker model and the effect of moving each |
| LoT C.5 | A less variable delay of the same mean | names no measure | NCR with a less variable tactic duration of the same mean |
| LoT B.2 | The sources that answered each attack flow | "answered" needs B.3's text | The sources behind each attack flow's attack profile |
| LoF E.2 | What removing the vulnerability memory changes | the one clause among noun phrases; it names no measure | NCR with and without the vulnerability memory, by services per operating system |
| LoT 3.1 | MTD metrics | the one entry without an article; it doesn't say whose metrics | The MTD metrics of the literature |

**Kept:** LoT E.1 and LoF 5.2 share a title on purpose: the table gives the figure's values. The same holds for E.2 and Figure 5.3.

**Order of work:**
1. Marc's yes on P15-P17, 9a and 9b.
2. Apply them and rebuild.
3. Generators for F.1-F.3 and F.5 (recomputes only).
4. F.4's tracer replay, if time.

### 9c. Chapter 7's tex block as it stood before P15 (moved here 2026-10-09; superseded by the slot sheet in section 3)

```latex
\chapter{Conclusion}
\label{ch:conclusion}



% Not the abstract in past tense: the impact of the specific technical
% move, and the next step in the line of research.

% RESTRUCTURED 2026-09-28 (handoff §10--§11): organised by the research
% question. Evans et al. 2014: "summaries are not conclusions"; the
% contributions are stated as answers with their impact, not recapped.
\noindent\emph{[Placeholder --- the research question answered directly, in
the introduction's words, in two or three sentences.]}

\section{Contributions}
\label{sec:contributions}

\noindent\emph{[Placeholder --- one paragraph per contribution of
Chapter~\ref{ch:intro}, each stated as the answer to its sub-question
(\ref{sq:capture}, \ref{sq:model}, \ref{sq:evaluate}) with its impact; the
bounds of Sections~\ref{sec:fidelity-verdict} and~\ref{sec:threats} travel
with each claim.]}

\section{Future work}
\label{sec:future-work}

% Was Chapter 7 (ch:futurework) until 2026-09-28. Each item opens on the
% limitation it lifts (Section~\ref{sec:threats}'s scope paragraph, in the
% same order); run-in paragraphs, no subsections. The dissertation's last
% sentence names the next step.
\noindent\emph{[Placeholder --- a richer set of attack actions (the binding
constraint); detection avoidance against a detector (property 5: the observer, not the
behaviour); deployment-strategy awareness and learning across runs (property 8); a
richer exploit attack action for the vulnerability memory to act on (the memory
operates and is blocked by the simulator's exploit attack action,
Section~\ref{sec:ablation}), and where vulnerability types recur more often; MTD selected or
optimised against the APT attacker model; other network sizes and
emulation.]}

% [ADDED 2026-10-08 (Marc, answering the 6.1 cold examiner's questions),
% candidates for the list above, DRAFT STATE:
%  - Edge ablation on the attack profiles: remove one tactic-to-tactic edge at a
%    time and measure ASP and NCR. The edge the outcome is most sensitive to is
%    where a mitigation that breaks that transition (initial access to a
%    post-intrusion tactic, say) would matter most: mitigations proposed from
%    the attacker model itself.
%  - Partition size: vary the size of the attack profiles' partitions and read
%    the effect on ASP (c4 rests on five attack flows).
%  - Success given undetected: each attacker's successful runs that a detector
%    would not have flagged (6.1, point 2's frame).]
% Marc 2026-10-08 (from 6.2 paragraph 4): MTD optimised against the APT
% attacker model comes after reducing assumptions: model what is known about
% the attacker faithfully, realistically and for the network in question;
% then "if I were the attacker, this is what I would do, and this is how to
% hold it back". A learned strategy trained on today's assumptions inherits
% them, as MTDShield inherits the baseline attacker's.



% The ruled-out directions, each with its reason: stealth semantics
% (blocked three independent ways), MTD-scheme awareness (ruled out of
% scope), event-based orchestration / retraining the reactive defender
% (V3), full incentive rationality. Collects the revisit conditions the
% notes carry.
%
% WHAT ch5 HANDS THIS CHAPTER (2026-09-09, third review pass). Each of these
% is an EXCLUSION ch5 makes explicitly, so the future-work claim is earned by
% a measurement or a stated scope rather than by a wish:
%  - THE ADAPTIVE DEFENDER. ch2 lists MTDShield in the roster and ch5 runs
%    none of it; the rebuild established that a cost-aware agent CAN trade
%    downtime against risk (the ladder's C1 held by a wide margin) but the go
%    is for a scaled training proposal, not for a trained model, and the
%    published figures characterise a uniform random selector. This is the
%    concrete form of the frozen-defender concession sec:dimensions
%    volunteers, and it is the first of the two substrate upgrades
%    notes/ch8_future_work/successor_programme.md names.
%  - A TACTIC-LEVEL ACTION LAYER. The second upgrade in the same note, and
%    the bind ch5's own ceiling sentence points at: the outcome is bounded by
%    the six inherited verbs, so a structure-rich attacker cannot convert
%    structure into outcome on this substrate.
%  - STEALTH SEMANTICS. Axis 5 stays blank because there is no detection
%    model for a tempo or spacing choice to matter against --- that is the
%    axis's own argument, held three times. WHAT MAKES THE FUTURE-WORK CLAIM
%    SHARP RATHER THAN GENERIC: the behaviour is already there and already
%    measured (spacing 1.5-1.8x wider, 45 % quieter on the level, the whole
%    margin attributable to the non-action tactics), so what is missing is
%    the DEFENDER-SIDE OBSERVER, not the attacker-side behaviour. Say it that
%    way; it converts a blank cell into a specified next experiment.
%  - THE TARGETED OBJECTIVE AT DEPTH. The Gate probe passed at layer 1 on the
%    aggregate envelope only and failed at every depth for the four
%    objective-conditioned profiles. That is a measured boundary on what this
%    attacker can be asked to do, not an untried idea.
%  - THE EMULATION RUNG (notes/ch8_future_work/emulation_rung.md): what
%    carries up the evaluation ladder and what must be re-derived.
```

## 10. Appendix cut audit (2026-10-13, NOT RULED)

Marc (2026-10-13): the appendix is "the biggest risk to my dissertation"; "what do we need in the appendix, what do we not need". The yardstick is [`../workflows/appendix_conventions.md`](../workflows/appendix_conventions.md) (UWA CITS4001 rule, verified 2026-10-13).

**Size now** (`dissertation.toc`, 118-page build): body pp. 1–49, AI Use Declaration p. 50, appendices pp. 51–103 (A is pp. 51–57; B–G are 46 pages), references pp. 104–118.

**Overturned on merit:**
- §5 item 7 ("Nothing to cut in B–D"). That test asked "does it back a cited claim?" UWA's rule asks more: is the item essential (then it goes in the body), and is it concise data (not prose)?
- The 2026-10-09 Q4 approval of five further analyses. Three of them say of themselves that they are not part of the argument (G.1 "describes MTDSim's networks rather than either attacker"; G.5 "not part of the main argument"; G.7 "not part of the main argument"). G.4 says "the claim stands … without it", and G.6 says "it is not a result".

**Main-text citation counts** below come from a `\ref` scan of the body, lines 1–9620.

| Now | Pages | Body cites | Verdict | Reason (appendix_conventions.md) |
|---|---|---|---|---|
| A Proposal | 7 | 0 | **Ask** | UWA does not require it in the dissertation. Keep it only if Jin or the coordinator says it must be bound in; otherwise cut it (7 pp.) |
| B Predicate tests: lead paragraph 1, Table B.1, counterpoints | ~4 | 3 (ch3, ch6) | **Keep** both tables | The ch3 marks are the contribution claim; B.1 is the evidence, and the counterpoints answer "did you score yourself kindly?" |
| B, paragraph 3 (re-scoring history, the language-model scorers, "eleven marks lowered") | ~0.7 | — | **Move to the AI Use Declaration** | Logbook. The Declaration is empty, yet ch3 and ch6 already cite it for exactly this. Fixes §5 item 8 |
| C.1 Edges from co-occurrence and keyword mining | ~0.5 | 1 | **Cut** | A rejected method in full. Ch4 states the choice; one clause there carries it |
| C.2 Exemplar flow (fig B-1a) | 1 | 0 | **Cut** | Ch4 Figure 4.1 already shows attack flows aggregated |
| C.2 Full technique graph (fig B-1b) | 1 | 0 | **Cut** | Duplicates the technique core (B-1c), which shows the sparsity readably; the 88 % figure is in the text |
| C.2 Technique core + tactic graph | 2 | 1 | **Keep** | The tactic graph is the model's input, drawn nowhere in the body |
| C.3 Attack profile of each attack flow | 2 | 2 | **Keep** | Per-flow classification: a concise data set |
| C.4 Edges of the attack profiles | 0.5 | 1 | **Keep** | Each Petri net's edges: replication data |
| C.5 Reasons for the tactic-to-action mapping | ~1 | 0 (table 1) | **Cut if** ch4 ¶ after Fig 4.x gives every row's reason | Marc: "we kind of discussed that". Check row by row; any reason ch4 lacks becomes a clause there |
| C.6 Mapping every tactic to an attack action | 0.5 | 0 (table 1, ch6) | **Cut**; one sentence in ch4 | A rejected alternative; the result (0.15 against 8.13 hosts) is one number, and the parameter register already carries it |
| C.7 How each tactic duration was set | 2 | via tab_4-4a; ch6 | **Keep**; merge the two tables if they fit | Declared values and reasons: replication |
| C.8 Rules of the failure matrix: tables | 1 | 1 | **Keep** | Replication |
| C.8 Decomposition figure | ~1.5 | 0 | **Cut** | About 5 pt type (`figure_table_conventions.md` §i); ch4 draws the matrix; the tables give the parts |
| D lead + value-bases table | ~1 | ch5, ch6 | **Keep** | Provenance and the test that covers each value |
| D parameter register (C-0a) | ~1 | via D | **Keep, as D's single robustness table** | It already gives every perturbation's outcome, including D.2 and D.3 |
| D.1 band protocol prose + C-1a table + C-1a figure | ~2 | 1 (ch4), ch6 | **Cut the figure and the C-1a table; cut the prose to two sentences** (bands fixed before the run; one at a time) | Same numbers as the register |
| D.1 ranking at both band ends (C-1b) | 0.5 | ch6 | **Keep** | ch6 cites it; the register does not carry it |
| D.2 Shape, D.3 distance factor | ~2 | 0 | **Cut** | The register carries both outcomes; neither is cited from the body |
| D.4 Detector robustness | ~1.5 | ch4, ch6 | **Keep**; resolve the two `\prelim` | A metric threshold's robustness |
| E lead + E.1 agent chosen + sweeps table | ~1.5 | ch5 | **Cut the sweeps table** (Tay's data: cite it); keep two sentences (which agent, why) | Someone else's data |
| E.2 Settings table | 1 | ch5 | **Keep** | Replication |
| E.3 Changes made | 0.5 | 0 | **Keep** | Replication; short |
| E.4 Known limitations | 0.5 | ch6 | **Keep the list.** The exploration-rate-1 finding and the detection-input finding go to the body (ch5 setup or 6.5) **if** ch6 argues from them; check 9230 | Essential where ch6 leans on them |
| E.5 Agent's choices | 0.5 | ch5 | **Keep** (ch5 states the 70 %) | Data behind a body number |
| F.1 tab:disruption, tab:eff-interval-values, rank-one | ~1.5 | 9 | **Keep** | The values behind ch5's figures: the textbook appendix item |
| F.1 ASP reduction: equation + table | 0.5 | ch6 (8972, 9084) | **Keep** | ch6 uses the term |
| F.1 ASP reduction figure | 0.5 | 0 | **Cut** | Same numbers as its table |
| F.2 Every metric for each attacker (2 landscape tables) | ~5 | **0** | **Cut**; one data-availability sentence | The data dump; it is the largest single block |
| F.3 Ablation tables (3) | ~2 | ch5 | **Keep** | ch5 cites each |
| F.3 Memory-ablation figure | 0.5 | ch5 (8462) | **Cut**; move the ch5 cite to the table | Same numbers as tab:ablation-memory |
| G lead | 0.3 | ch6 | Keep, shortened | — |
| G.1 Success by seed | 1.5 | ch7 only | **Cut** | Says it describes MTDSim, not either attacker; the ch7 future-work line can stand without it |
| G.2 Behaviour metrics in attack actions | 1 | ch6, B | **Keep** both tables; cut the prose to the lead | A construct check on two metrics |
| G.3 Tactic durations (run-time table + rerun table) | 2 | **5** (ch6 ×4, ch7) | **Keep the rerun table** (C-8). Cut the c3 paragraph. Keep tab:fa-run-time only if ch6's "15 to 30 %" needs it (it does: 8617) | ch6's explanation of the headline rests on it; the numbers are already in the body, so the appendix holds the data |
| G.4 No foothold under the host layer | 1 | 0 | **Cut** | "The claim stands … without it" |
| G.5 Accounts under user shuffle | 1.5 | 0 | **Cut** | "Not part of the main argument" |
| G.6 Traced run | 1.5 | ch6 (8727) | **Cut** (alternative: promote to ch4 as the worked example) | "It is not a result". Promotion costs a body page at the 50-page ceiling |
| G.7 Random groups of the same size | 1.5 | ch6 (8584) | **Cut**; drop the ch6 clause or keep its number bare | "A hypothesis … not part of the main argument"; long argumentative prose |

**Estimated effect:** about 21 of B–G's 46 pages go, leaving about 25 (about 32 with the proposal). Every surviving section is a float the body cites, under a lead of one or two sentences. These are page estimates from the contents' section starts; the build gives the real count.

**Structure after the cuts:** A Proposal (if required); B Scoring the attacker models; C The APT attacker model's values and data; D Robustness of the declared values; E MTDShield as run; F Values behind the chapter 5 figures; G Post-hoc checks (G.2, G.3). The headings stay as ruled in §9a; G's title follows its contents.

**Body edits the cuts force** (proposed before/after on the yes; ch1–5 edits are presented first):
- ch4: one clause for C.1, one sentence for C.6, and C.5's missing reasons, if any;
- ch5: the memory-ablation cite retargeted to the table;
- ch6: G.4, G.5, G.6 and G.7 citations removed or bared. Ch6 is auto after the ruling;
- ch7: the G.1 citation;
- one data-availability sentence (ch5 setup) for F.2.

**Questions for Marc** (one each, with the recommendation):
1. Apply §10 as a whole? *Recommended: yes.* The cuts are deletions, and none touches a body claim.
2. Is the proposal required in the bound dissertation? *Recommended: ask Jin. Cut it unless it is required.*
3. Traced run: cut it, or promote it to ch4 as the worked example? *Recommended: cut.* The body is at 49 of 50 pages.

## 11. Rulings on §10, and what was applied (2026-10-13)

**Marc's rulings:**
- Q1: apply §10 as a whole. **Yes.**
- Q2: the proposal is required, so **A stays**.
- Q3: the traced run is **cut**.

**Correction to §10.** C.8's reason said "ch4 draws the matrix". It does not: ch4 has no failure-matrix figure, and the decomposition figure was the only drawing of it. The cut still passes the test. No body sentence cites the figure, its type is about 5 pt, and the two rules tables fully determine every value. Flagged to Marc; reinstating it is a one-block revert.

**Applied (appendices, ch6, AI Use Declaration, generators).** The build is 101 pages, from 118. The appendices are now pp. 51–~86, with B–G about 29 pages, from 46.
- **B:** paragraph 3 (the scoring history) moved verbatim into the AI Use Declaration, with its two "(AI Use Declaration)" self-references dropped and a DRAFT STATE comment added.
- **C:** cut the mining section, the exemplar flow figure, the full technique graph, the mapping reasons and the total mapping. Cut the decomposition figure. The technique-core caption now carries the decode the full graph's caption gave.
- **D:** D.1 is cut to its protocol sentence, a pointer to the register and the Saltelli limit; its C-1a table and figure are gone. D.2 and D.3 are cut. The register (`analyse.py --tables-only`) and value-bases (`value_bases.json`) no longer point to cut sections. D.4's `\prelim` values are resolved against the 1 000-seed table: "at least 2.5 %" holds; "under 2 %" became "at most 2 %" (the 5/30 setting flags 2.0 %); "within about one point" became "within two points" (c3 at 5/30 is +1.7).
- **E:** the sweeps table is cut, with the held-settings sentence that read it.
- **F:** "every metric" (both landscape tables), the ASP-reduction figure and the memory-ablation figure are cut.
- **G:** G.1, G.4, G.5, G.6 and G.7 are cut. G.2 keeps its lead, and the number readings its tables carry are gone. G.3's c3 paragraph is cut, and its last sentence (NCR closes less of the gap) is kept.
- **ch6 (auto):**
  - 8584: the random-groups sentence is deleted, since its only evidence was G.7;
  - 8727: the traced-run citation is dropped (the hedge "most likely" stands);
  - 9105: `tab:anchor-sensitivity` becomes `tab:parameter-register`;
  - 9114: the total mapping is stated as NCR 0.003 against 0.163 from the register, in place of 0.15 against 8.13 hosts (the same result, over 50 hosts).
- **Generators:**
  - `attack_action_times_table.py`: the caption cites `fig:controller-mapping`;
  - `failure_weight_decomposition_figure.py`: the rules caption loses its letters sentence, and the kernel caption points to the register.
  All four generators were rerun, and the diffs are exactly the intended lines.

**The three questions, for every surviving item:** Q1, does a reader need it to follow the argument? Q2, is it the evidence for a body claim or number? Q3, neither, so cut.

| Item | Q1 | Q2: the body claim it backs |
|---|---|---|
| A Proposal | no | no. Kept because UWA requires it (Marc) |
| B lead + Table B.1 | no | the ch3 marks (3199; ch6 8825, 9139) |
| B counterpoints | no | the contested cells of B.1, so the same marks |
| C.1 technique core + tactic graph | no | ch4 4032: techniques too sparse for nodes (88 %); the tactic graph is the input ch4 describes but does not draw |
| C.2 profile of each attack flow | no | ch4 4178, ch6 9145: the classification of the 38 attack flows |
| C.3 edges of the attack profiles | no | ch4 4226: each Petri net takes only its own attack flows' edges |
| C.4 tactic durations + attack-action times | no | ch4's tactic-duration table; ch6 9076 |
| C.5 failure-matrix rules | no | ch4 5131 |
| D lead, value bases, register | no | ch5 6216; ch6 9100, 9105, 9114 |
| D.1 ranking at both band ends | no | ch6 9068: the rankings hold at both ends |
| D.2 detector | no | ch4 5452, ch6 9129: the IDS rule's threshold |
| E.1–E.3 agent, settings, changes | no | ch5 6092: "MTDShield runs as released" |
| E.4 limitations | no | ch6 9230: "outside its training conditions" |
| E.5 choices | no | ch5 7832: service diversity in 70 % or more of decisions |
| F.1 interval values, disruption, rank-one, ASP-reduction table | no | ch5 7546, 7792, 7801, 7932; ch6 8921–9156 |
| F.2 ablation tables | no | ch5 8224, 8268, 8444, 8462 |
| G lead | no | ch6 9172 (`thr:posthoc`) |
| G.1 behaviour metrics in attack actions | no | ch6 9133; B counterpoints |
| G.2 tactic durations | **closest to yes** | ch6 8559–8635: the explanation of the no-MTD gap. The body states every number it uses, so the tables are its evidence. Promote the rerun table only if an examiner should see the evidence without turning pages |

**Proposed, ch1–5 and ch7 (before/after; apply on Marc's yes).** Until then the build carries these six undefined references.
- **P-a, ch4 4022:** "against 50\,\% for the attack flows (Appendix~\ref{app:cooccurrence})." → "against 50\,\% for the attack flows."
- **P-b, ch4 4846:** delete "Table~\ref{tab:controller-mapping} gives the reason for each tactic." The preceding paragraph and the one after Figure 4.x give every row's reason.
- **P-c, ch5 8462:** "(Figure~\ref{fig:ablation-memory}, Table~\ref{tab:ablation-memory})" → "(Table~\ref{tab:ablation-memory})".
- **P-d, ch5 Table `tab:eff-cross-arm` caption** (`tools/ch5_sweep_figures.py` 507): delete "Tables~\ref{tab:full-movement} and~\ref{tab:full-baseline} give each value's confidence interval, ASP reduction and MTTC."
- **P-e, ch5 `Runs` paragraph (6135), new last sentence:** "Every metric at every configuration, with its interval, is published with the experiment scripts." Verify first that the ch1 footnote's repository serves `data/results/`.
- **P-f, ch7 9582:** "which features of a network decide success (Appendix~\ref{app:fa-success})" → "which features of a network decide success".

## 12. P-a to P-f applied; pointer sweep (2026-10-13)

Marc: "yes to all six, ensure no dangling pointers".

**Applied.** P-a to P-f as written in §11. P-d is applied in `tools/ch5_sweep_figures.py`, and `--only ranking` was rerun; the diff is the caption only.

**P-e is true once this branch is pushed.** The repository in the ch1 footnote is public (HTTP 200), and `data/results/ch5_defended/numbers_reported.json` (1 000 seeds) is tracked here. But `origin/dev` is 505 commits behind and carries only the 100-seed `numbers.json`. Push before submission, or the sentence overclaims.

**Pointer sweep.**
- Build: 101 pages; no undefined references or citations, nothing multiply defined. `briggs2012` drops from the bibliography; it was cited only in the cut D.1 sentence.
- No hard-coded appendix letters in live prose, tables or figure sources.
- Every remaining appendix float is cited. The uncited labels are chapter and section labels whose floats are cited (`app:movement`, `app:supplementary-results`, `app:sup-ablations`, `app:mtdshield-configuration`, `app:mtdshield-changes`), A (required, not cited), and `eq:asp-reduction`.
- Two leads were made true again:
  - D's "The sections that follow read the same perturbations value by value" is deleted, because they no longer do;
  - G's two sections are swapped to keep "They follow Chapter 6's order". Chapter 6 first cites the tactic durations at 8555 and the behaviour metrics at 9125.

## 13. Appendix B: B.2 removed; title, lead and caption proposed (2026-10-13)

**Ruled (Marc):** "it's hard to defend b.2 … all ai generated prose, I would remove". **Applied:**
- the counterpoints longtable and its lead sentence are removed, and with them the `longtable` package (its only user);
- the ch6 `tab:fidelity-verdict` caption now reads "gives the predicates behind each mark", in place of "the reasoning", since B no longer argues cells.

**Missed pointer, fixed.** ch6 9131 cited Appendix B for the language models' blind scoring, which moved to the AI Use Declaration in §11. It now reads "(AI Use Declaration)". The §12 sweep checked that references resolve, not what they point to; every other pointer into a section that lost content was re-read and still lands.

Build: 99 pages, 0 undefined.

**Proposed, NOT RULED:** the title, a lead cut to what ch3 does not already say, and the cell decode moved into B.1's caption. See the session record for the before/after.

**Out of scope, flagged:** ch7's slot list (the "Last sentence." and "Promises Chapter 6 makes" items, about 9589) prints in the PDF on p. 49.

**Applied (Marc, 2026-10-13: "short, sharp"; caption reads alone; title not rhetorical):**
- **Title:** "The attacker models scored on the eight properties". It reuses Table 3.3's caption wording; Marc's "comparative analysis" was weighed and rejected as vaguer than the term the reader already has.
- **Lead:** two sentences. What Table B.1 backs (Tables 3.3 and 6.1), and how the definitions split into predicates.
- **Caption:** now carries what the old lead said: the evidence source per attacker model; behaviour vs qualifier; the four cell values (with "assumed" folded into its definition); the mark rule.
- **Cut, no longer stated:** "an example in a definition is not a predicate", and the repeated ch3 mark definitions.

Build: 99 pages, 0 undefined. B is pp. 58–59, with the lead and the table on separate pages because the table does not fit under the lead.

**One-page fix (Marc, 2026-10-13: "do the 1 page fix"; caption compressed; split rule into the lead; "9.5 size"):**
- **Table B.1:** marks on each property's row, so the eight "mark" rows are gone; gaps in place of the rules between properties; predicate column 10.4 cm; table type 9 pt.
- **Caption:** cell key plus "✓ when every cell is yes, ✗ when every behaviour predicate is no, and P otherwise". That is exactly equivalent to the old P rule.
- **Lead:** what B.1 backs, where each attacker model's evidence comes from, and the predicate-split rule.
- **Type size:** 9.5 pt was tried. Computer Modern has no 9.5 pt (LaTeX substituted 9). `fix-cm` would give a true 9.5, but it rasterised a textcomp font at 10.95 pt elsewhere in the document (mktexpk Type 3 bitmap), so 9 pt was used.
- **Build:** 98 pages, 0 undefined. B is p. 58 alone, and C starts on p. 59.

**Table B.1 legibility (Marc, 2026-10-13: wrapped predicates not indented; the zebra is hard to follow):**
- Each predicate cell is set with `\leftskip` 1 em and a 1 em hanging indent, so wrapped lines hang under their predicate.
- The zebra is replaced by **shading by property**: properties 2, 4, 6 and 8 grey. This is a deliberate exception to the house `\rowcolors` zebra (`figure_table_conventions.md` §k). The house style separates groups with `\midrule`, and those rules were removed to fit the page. Shading by group takes their place at no height.
- Still one page; build 98 pages, 0 undefined.

**Appendix A without a heading page (Marc, 2026-10-13).** The proposal now starts on p. 51. The chapter counter, contents line and `app:proposal` label are set in `\includepdf`'s `pagecommand` on the proposal's first page. A one-line label ("Appendix A  Original honours proposal, as submitted in March 2026") sits in the top margin above the proposal's own title, and the "with its own reference list" note is dropped: the proposal's References section shows it. Build 97 pages, 0 undefined.

**C.1 (Marc, 2026-10-13: "let's cut that"; portrait or landscape?).**
- The tactic graph (`fig_B-1d`) is cut. The tactic edges the model runs on are drawn per attack profile in C.3, and nothing in the body cited the figure.
- The technique core is reflowed to portrait: `tools/gap_appendix_figures.py` now packs it into `PORTRAIT_BOX`, at 15.6 × 16.0 cm and 8 pt (the floor, unscaled), still 35 techniques and 55 edges.
- With no `landscape` environment forcing page breaks, C.2's opening fills p. 58, and the figure takes p. 59. The trailing `\FloatBarrier` is dropped; the one at C.2's end keeps the float inside C.
- Build: 95 pages, 0 undefined.

**Table C.1 (Marc, 2026-10-13: remove "Step notes" and "Decided by us").**
- `tools/gasp_structural_baseline.py --tex` now prints attack flow | ATT&CK group | threat report.
- "Step notes" was CTID's flow narrative (`ctid_flow_narrative`), part of CTID's own material, which ch4's frame (CTID description, then the group page or the threat report) does not name. The caption folds it in: "with the analyst's notes on its steps where needed".
- "Decided by us" ticked the three flows the C.2 prose names and justifies one by one, so the column repeated the prose.
- The caption now says what a blank row means (nothing beyond CTID was needed).
- The prose still does the one job a cell cannot: the reason each of the three open flows was decided as it was.
- Build: 95 pages, 0 undefined.

**Table C.1 two-up (Marc, 2026-10-13: "look at the full thing in total"; indent the names; cells not aligned).**
- c₁'s 19 attack flows sit on the left and c₂–c₄'s 19 on the right, so the table is half as tall with no row dropped; C.3 now starts on p. 60.
- Flow names are indented 1 em under their profile label (`\leftskip`); group and report cells are centred under stacked heads.
- Stripes kept (ruling of 2026-10-01); the first row, where both blocks open on a label, is white.
- Also fixed: Table B.1's predicate column 10.4 → 10.35 cm, clearing the 1.2 pt overflow the one-page fix introduced.
- Left as found: the pre-existing 2.5 pt overflow of the C.3 figure.
- **Figure C.1 end marks, NOT done (recommended no):** the generator outlines `is_objective` techniques (out-degree 0 across the whole graph), and none of the 15 is in the core. Marking "the last step of some attack flow" would be a new definition, a third use of the accent, and serves no part of the sparsity claim C.1 backs.

**C.3 (Marc, 2026-10-13/14).**
- **The heading is kept.**
- **Muddy Water sentence added to the lead:** c₁'s one edge into Impact is Muddy Water's T1486 Data Encrypted for Impact, which its analyst drew at confidence 0 (`data/gap/flows/muddy_water.yaml`, node a10). The Talos report, fetched 2026-10-13, describes no encryption or destructive activity in the campaign; ransomware appears only as the group's past attempts. The sentence paraphrases it.
- **Provenance flag:** the audit note in `data/gasp/metadata_audit.csv` quotes Talos as "no encryption, wiping, or ransom demands". That is not verbatim in the report, so do not quote it.
- **Figure:** `draw_grid` now draws the diagonal, a thin grey line through the never-filled same-tactic cells. It splits each grid into edges forward in the order of tactics (above) and back (below). The caption gains one decoding sentence. Type is still at the 8 pt floor; the build is 95 pages, 0 undefined.
- **Not done:** lifecycle-stage separators on the grids. Judged one structure too many on top of the diagonal; available if wanted.

**C.4 (Marc, 2026-10-14: "all the cuts are fine"; polish the table; retitle).**
- **Table C.2 cut** (reference, multiplier, band and reason per tactic). Ch4's prose and Table 4.4 give every value and reason. The per-tactic bands fed no test; Appendix D's register gives the ranges that were moved.
- **Applied by ruling:** the ch4 Table 4.4 caption loses "Appendix C.4 gives each tactic's reason" (`dwell_catalogue_tables.py`), and the value-bases rows now point to §4.4.2 (`value_bases.json`).
- **Heading:** "Tactic durations against the baseline attacker's times", in the text's terms; the baseline attacker has times, not tactic durations.
- **Lead:** gains one sentence. Six tactics take an attack action's time; we set the other nine by judgement (§4.4.2).
- **Table** (`attack_action_times_table.py`): now one row per tactic, grouped by attack action, with MTDSim's time and the mean duration in aligned columns. The unmapped group's time cell is blank, meaning not applicable.
- Build: 94 pages, 0 undefined.

**C.5 (Marc, 2026-10-14: rules opaque, distance table small, "can't we just say we assumed them").**
- **Heading:** "The rules and the distance factor of the failure matrix", ch4 §4.4.3's own terms.
- **Rules table:** "Applies to" is replaced by **Condition**, written as logic on the move. *f* is the failed tactic, *t* the candidate next tactic, Δ the signed number of lifecycle stages, *P* = {Reconnaissance, Resource Development, Initial Access} (no foothold); first match wins.
- `failure_weight_decomposition_figure.py` holds each condition as a predicate too, and checks it against `rules._failure_rule` on all 210 pairs, so a drift stops the build. The check passed.
- **Distance-factor table cut.** With γ = δ = 0.25 and z = 0.1 the factor says one thing, now one sentence: full value within a stage or to an adjacent one, quartered two stages away, zero three away. Its bands are in Appendix D's register.
- Build: 94 pages, 0 undefined.
- **Revised the same day** (Marc: the symbols were hard to read): Table C.3 is now a **decision table**, with columns Failed tactic | Next tactic | Move (back / within / forward by lifecycle stage), a blank cell matching any. The caption defines "needs a foothold" (every tactic except Reconnaissance, Resource Development and Initial Access) and first-match-wins. No symbols remain. The compiler check (all 210 pairs) still runs and passed.
- **Second revision** (Marc: "what is a foothold … what does back mean … assuming success?"). Four root causes, all fixed:
  - a blank read as "nothing" (and, under Failed tactic, as "no failure"), so "any" is now written out;
  - "needs a foothold" was ch4 vocabulary without its meaning, now "after Initial Access" / "up to Initial Access" in ATT&CK's order, the exact equivalent;
  - back/within/forward is now **Stage**: earlier / same / later, the next tactic's lifecycle stage against the failed one's;
  - the frame now leads the caption: after an attack action fails, the first rule from A down that applies gives the value.
  The compiler check passes.
- **Not fitted onto p. 62.** It is about 2 cm short. Trimming the reasons and narrowing columns did not close it, nor did 9 pt type; only cutting the Reason column would. Kept on p. 63; D starts on p. 64 either way, so fitting would save one page.
- **"Applies to N of 210 cells" column:** not added. It costs width, and Marc judged it too much.

**Appendix merge (Marc, 2026-10-14).** The sensitivity analyses are merged into the supplementary results, with MTDShield after them. The appendices are now:
- A the proposal;
- B scoring;
- C supplementary material for the APT attacker model;
- **D Supplementary material for the MTD evaluation**: D.1 MTD's effect at every interval, D.2 the ablations, D.3 the declared values and the effect of moving each (the old D lead, now a section carrying `app:sensitivity`), D.4 tactic-duration robustness, D.5 detector robustness;
- E MTDShield as run;
- F further analyses.

Results come before sensitivity, the usual reading order. This departs from the §9 first-citation convention, which was proposed, never ruled. The title uses ch2's defined term "MTD evaluation"; the session first said it was not a term and was wrong. Body references are unchanged (`app:sensitivity` now prints D.3). Build: 94 pages, 0 undefined.

**D.1 restructured (Marc, 2026-10-14: the title; what is needed; the ASP figure).**
- The old D.1 backed two ch5 subsections, so it is split and named as they are: **D.1 Disruption per MTD deployment** (5.3.1; new label `app:sup-disruption`) and **D.2 MTD ranking against each attacker** (5.3.2; it keeps `app:sup-mtd-effect`, the target of ch6's ASP-reduction pointer). The ablations become **D.3 Ablation studies**, as §5.4 is named.
- Every float passes Q2, so nothing is cut.
- **ASP-reduction figure restored** (`fig_F-0b`, drawn from the 1 000-seed numbers on 2026-10-06). Marc judged it adds, and it shows at a glance the pattern ch6 cites. The §10 cut applied "one float per fact"; that is overturned for this pair under Jin's headline/depth rule (each figure with its table).
- **Layout:** `\FloatBarrier` at the end of D.1 and D.2. The disruption and three ablation tables are now `[htbp]` (were `[tp]`), set in the generator and the output alike: `ch5_disruption_figure.py`, `partition_ablation.py`, `ablation_table.py`, `memory_ablation.py`. Each table now sits under its heading. None of the four is input in the body.
- Build: 94 pages, 0 undefined.

**D.2 captions (Marc, 2026-10-14: captions "abnormally large"; grey or bold; combine the NCR and ASP tables?).**
- **Tables D.2 and D.3** (`ch5_sweep_figures.py --only values`) now decode only. Cut, as ch5 already gives them: the metric's scale, the runs per cell and the interval method. The ASP table now reads "laid out as Table D.2: the values of Figure D.1"; its "panels (g) to (l) of Figure 5.3" was stale. Figure D.1's caption is cut the same way ("drawn as Figure 5.3 draws NCR reduction").
- **Grey kept.** Results standard S3 (ratified 2026-10-02) makes grey mean "interval includes zero" dissertation-wide, and bold already means rank 1. Grey also marks the minority.
- **Not combined.** The two tables have different jobs: NCR holds the values of Figure 5.3, cited in ch5; ASP is the robustness check ch6 cites. A joint 12-column table would double the rows.
- **The ASP split into its own section is withdrawn**; ASP stays in D.2 next to the ranking it checks.
- Build: 94 pages, 0 undefined.

**D.2 polish (Marc, 2026-10-14: rows wrap; stretch the tables; "why did that take a full page").**
- **Tables D.2/D.4 (NCR/ASP):** label column 3.75 → 4.25 cm, value columns 0.78 → 0.74 cm, so every row label sits on one line.
- **Table D.3 (rank 1):** stretched to the text width (7.8 + 5.4 cm, 4 pt gaps, no overhang). The widest cells, three tied mechanisms, still wrap; they cannot fit one line beside the other columns.
- **The lone page** was `\FloatBarrier` sending a deferred rank-1 table to a float page of its own.
- **Fix, which also reads better:** D.2 now sets the ranking first (NCR values, rank 1) and the ASP check after it. The generator writes the ASP table to its own file, `tab_F-0d_interval_values_asp.tex`.
- Build: **93 pages**, 0 undefined. D.3 opens at the top of p. 67 with its first two tables.

**D.3 dedupe (Marc, 2026-10-14: "the full set of data the ablation table summarises"; what do the prose and the captions each carry?).**
- **Three tables, three experiments.** Each expands an ablation that Table 5.4 summarises at a few conditions: D.5 the attack profiles at all 60 conditions, D.6 against the 10 random partitions, D.7 the vulnerability memory by services per OS. Each backs a distinct sentence of §5.4. Nothing cut.
- **Prose** now states the frame ("each table gives in full an ablation that Table 5.4 summarises") and the shared reading of *d* once: on NCR, the same 1 000 seeds, averaged over c₁–c₄, bold = not negligible (§5.1).
- **Captions** keep their own comparison plus "Bold: not negligible" (S4). Cut from them: d's definition, the ±0.2 rule and bootstrap method (§5.1), the 29/7/24 counts and the no-MTD *d* (both in §5.4).
- **Generators** (`partition_ablation.py`, `ablation_table.py`, `memory_ablation.py`) carry the same captions; edited in place, since they read multi-GB run files.
- Build: 93 pages, 0 undefined.

**D.4 (Marc, 2026-10-14: "argument based"; blank cells; "corpus"; buzzword test verbs; "how is the reader supposed to use this?").**
- **The argument is §6.5's** (`thr:values`), which cites both tables. D.4's lead now says only how to use them.
- **The reader's use:** from §6.5 the reader asks which values are our judgement and whether each was tested. Table D.8 now lists **our judgement first** (`value_bases.json` bases order), with column headers Comes from | Value | Reason in | Test.
- **Every test cell says what was done:** "moved to both ends of a band", "replaced by an Erlang-4 delay" or "replaced by a total mapping", "removed in the ablation", "not tested" (decoded in the caption as a judgement value left untested, §6.5), or "none: taken from its source". No blank cells.
- **Bases:** "Corpus" → "Attack Flow corpus".
- **Layout:** `\FloatBarrier` before D.5 keeps D.8/D.9 inside D.4. This costs a page, because D.6's detector table now sits alone on p. 72. Build: **94 pages**, 0 undefined.
- **Open:** D.5/D.6 prose also summarises results (§6.5 territory). Trimming D.5 to a lead would likely recover the page; offered to Marc.

**D.4/D.5 (Marc, 2026-10-14: "I don't think table D.9 is useful"; the Test column "not D.4's job").**
- **The register (old Table D.9, `tab:parameter-register`) is cut.**
- **D.8 loses its Test column.** It is now every value, where it comes from (our judgement first), and where its reason is given. The exponential delay moves to Literature (ch4 justifies it from GSPN timing and stochastic attack behaviour). D.4 is retitled "Where each value of the APT attacker model comes from".
- **The plain tactic-duration table (`tab:anchor-sensitivity`) is restored in D.5:** NCR at each band end, for no MTD and random at 200 and 2 000 s.
- **Retargeted:** ch6 `thr:values` now cites `tab:anchor-sensitivity` for "only the 45 s changes NCR much". C.5's lead loses "moving them leaves NCR inside its interval". ch6 `thr:mapping` loses the total-mapping sentence (0.003 against 0.163; Marc: the mapping test is unimportant), keeping "No other partial mapping was tested".
- **`\FloatBarrier` before D.6** keeps D.5's tables in D.5. Build: **93 pages**, 0 undefined.
- **For the §6.5 T-round:** `thr:values` still says each value was "varied, substituted or removed one at a time". That stays true, but the substitutions (Erlang-4 delay, total mapping) no longer have a displayed table. Decide in the T-round whether to keep "substituted" or drop it.

**Value table moved to C.6 (Marc, 2026-10-14: "you can move it").** "Where each value of the APT attacker model comes from" describes the model, not the evaluation, so it is now the last section of Appendix C. What it gives that §6.5 cannot: the complete list of 13 values (nothing else set by hand) and the ch4 section that justifies each. This is the parameter table model papers carry (Brown 2023 Table I). `app:sensitivity` moves to D's tactic-duration section (now D.4), which is what ch5 6214 and ch6 9219 describe. D's opener is fixed: the first three sections give the full data behind ch5's comparisons and ablations, the last two its sensitivity analyses. Build: 93 pages, 0 undefined.

**D.4 rewritten (Marc, 2026-10-14: "sensitivity analysis on tactic durations"; what is the verdict; the purpose unclear).**
- **Heading:** "Sensitivity analysis of the tactic durations".
- **Prose, three short paragraphs:** the purpose (our judgement sets the durations, so test how much the results depend on them) and method; the finding (the 45 s duration moves NCR most, by 0.208 with no MTD against ≤ 0.027 for the others); the ranking test (at both ends of the 45 s band, rank 1 shares no mechanism with the baseline attacker's, the host layer stays above the service layer, and ρ stays between −0.03 and 0.03).
- **Table D.8** (`analyse.py frag_families`): one row per duration with its tactics, the band, NCR at the low end, the declared value and the high end, and a **Change** column; no MTD and random at 200 s only. The Verdict column and the per-cell ± are gone; the caption states the widest interval (±0.014). Wrapped tactic lists hang-indent.
- **C.6 fitted onto p. 63** under Table C.3 (`value_bases_table.py` now `[!htbp]`). Build: **92 pages**, 0 undefined.
- **Table D.8 redesigned** (Marc: "that formatting is horrific"). One row per mean duration in rising order (4.5, 35, 36, 45 s), labelled with its band; two column groups (No MTD; Random, 200 s), each low end / declared / high end / change; the largest change in each group in bold (45 s: −0.208, −0.144). The tactic lists are gone: Table 4.2 (`tab:dwell-catalogue`) says which tactics take each duration, and the caption points to it. The "at half" note is now plain: "Execution and Defense Impairment have half the 45 s mean duration, 22.5 s, so moving the 45 s moves theirs too." No cell wraps. Build: 92 pages, 0 undefined.
- **Table D.9 kept and made legible** (Marc: "focus on the clarity of this table"). It is the half of the sensitivity analysis that protects the result, and ch6 `thr:cause` cites it as its main mitigation. Changes (`duration_ranking_table.py`):
  - rows grouped by layer (host, service, credentials, deployment strategies), so "host layer above service layer" reads down each column;
  - column heads "APT attacker model, 45 s mean duration at: 11.25 s (low end) | 45 s (declared) | 180 s (high end)", which Marc first read as deployment intervals;
  - the ρ row labelled "ρ with the baseline attacker", and the caption saying near 0 means the rankings are unrelated.
  Build: 92 pages, 0 undefined.
- **Tables C.2 and D.9 redesigned flat** (Marc: "looks tacky … iterate … for both"). The cause was three separators at once (group rules, group labels or blank cells, row stripes).
  - **C.2** (`attack_action_times_table.py`): one row per tactic in ATT&CK order; Tactic | Attack action | MTDSim's time (s) | Mean duration (s); "unmapped" in words, not blank; the exploit as its mean 4.5, with the 0–9 s spread once in the caption; no rules.
  - **D.9** (`duration_ranking_table.py`): a Layer column in place of group rows; two-line column heads (11.25 s / low end …); rank columns 1.95 cm, so nothing overflows; each ρ cell set as the value over its interval in smaller type; caption tightened.
  - Iterated four times against the rendered page. Fixed along the way: a 32 pt overflow, wrapped heads, broken ρ cells, a stripe gap, and stripe overhang.
  - Build: 92 pages, 0 undefined.
- **D.4 deduplicated** (Marc: "is there any dedup between the tables and the prose?").
  - **Prose:** why the test exists, the method once (both ends of a band, one at a time, the others held, interactions untested), finding 1 ("only the 45 s moves NCR much", no numbers, since bold shows it), finding 2 (the comparison holds at both ends; the test was fixed before the run), and why the baseline column does not move.
  - **Captions** decode the cells only: D.8 drops "the other three held"; D.9 drops "which uses no tactic duration".
  - **D.9:** the "Layer" column becomes **Group** (host layer, service layer, credentials, strategy), since a deployment strategy is not a layer.
  - Build: 92 pages, 0 undefined, no overflow.
- **D.9 ordered for its claim** (Marc): rows sorted by the declared ranking; columns declared (45 s) | low end (11.25 s) | high end (180 s) | baseline attacker, under the spanner "APT attacker model". "45 s mean duration at 11.25 s" contradicted itself, so the caption names the 45 s mean duration and its band ends once. Build: 92 pages, 0 undefined.

**D.5 cut (Marc, 2026-10-14: "not that important … we define the metric" by the declared rule).** The detector sensitivity section and its table are gone. ch6 `thr:metrics` keeps "a declared IDS rule", minus the pointer. D's opener: "…and the last its sensitivity analysis of the tactic durations". Build: **91 pages**.
- **PENDING Marc's yes (ch4):** delete ch4 5450, "Appendix~\ref{app:detector-memory} varies the count of five and the 60\,s window." Until then it is the build's one undefined reference.

**Appendix E folded into D as D.1 "MTDShield as run"** (Marc, 2026-10-14: used as released, part of the evaluation, not background or method; critiquing Tay's release is "not our place").
- **Kept:** which agent (Tay's highest-scoring of 38, his weights and input code); why random over its four mechanisms runs beside it; the settings table (training / Tay's evaluation / ch5); the two changes made to run it; how the APT attacker model meets its detection input (an unmapped tactic reads as nothing detected); its choices at 200 s and 2 000 s.
- **Cut:** Tay's sweeps, the exploration-rate-1 note on his scores, the release-defect list, the pre-registered falsification and the training-code input check.
- **Pointers:** all old labels sit on D.1, so ch5 6089 and 7827 resolve; ch6 9217 ("outside its training conditions") now cites the settings table.
- **Appendices now:** A proposal, B scoring, C APT attacker model, D MTD evaluation (D.1 MTDShield, D.2 disruption, D.3 ranking, D.4 ablations, D.5 tactic-duration sensitivity), E further analyses. Build: **90 pages**; one undefined reference, the pending ch4 5450 deletion.
- **D.1 cut to one page** (Marc: "chop, chop down … short, sharp, relevant"). The prose is two short paragraphs. Table D.1 now keeps only what differs between training and ch5 (hosts, run length, deployment interval, attacker, exploration). What is the same in both (the mechanisms, detection of the current attack action at every decision, the forced deployment after 2 000 s) is one caption sentence. Tay's evaluation column and the training hyperparameters are cut. Marc asked whether detection is used at all: it is, at rate 1, by `attacker_sensitivity` in `mtd_ai_operation.py`. Build: **89 pages**.
- **Table D.1 checked** (Marc: "did you change any facts? … do we need that?"). Every value is unchanged from the earlier table and matches the forensics record of Tay's release (`mtd_ai_forensics.md` §4: `finish_time = 5000`, `mtd_interval = 200`, `total_nodes = 100`, a new network every episode). The session's relabel "Run length" was wrong, since ch5 runs end at a target host or 15 000 s; it is back to **Time limit** ("5 000 s per episode" | "15 000 s per run"). The **Exploration** row is cut: it describes training, not a condition the agent meets. The table keeps the four rows behind ch6's "outside its training conditions": hosts, time limit, deployment interval, attacker.
- **D.5 on one page** (Marc: fit Table D.10 onto p. 69). D.10's caption is trimmed of what the page already says (the tactics behind the 45 s, the row order, "near 0 … unrelated"). The ρ row is one line, with the caption giving the interval range once ("every 95 % interval lies within −0.27 and 0.05"). The prose loses "the baseline attacker uses no tactic duration…", which the caption's "the baseline attacker's ranks are Table 5.3's" covers. Placement is `[!htbp]`. Build: **88 pages**; one undefined reference, the pending ch4 5450.

### 13.x Appendix E: "Post-hoc analyses"; E.1 as one table (Marc 2026-10-14)

- Ruling: E stays apart from D (D = planned, backs ch5; E = chosen after the results, backs ch6, bounded as a set by T9). Retitled "Post-hoc analyses"; opener cut to two sentences (the logbook line "run while Chapter 6 was written" removed).
- E.1 retitled "Ablation of the tactic durations". Old Table E.1 (tab:fa-run-time, tab_FA-7) cut: its failed-actions column duplicates the ablation table's declared rows, and ch6 cites none of its other columns (unmapped share of run time 34–57 %, attack rate with failed actions counted). t_time removed from tools/further_analyses_tables.py.
- Ablation table redesigned (t_durations): baseline attacker first as the reference row; group labels say what changed ("Unmapped tactics at 0 s"; "Unmapped tactics at 0 s, mapped tactics at the baseline attacker's times"; "the baseline attacker's tactic durations" rejected: the baseline attacker has no tactics); bold = past the baseline attacker's value with the 95 % intervals apart. Lead: the ch6 claim, the two steps, the averaged ASP 0.09 → 0.45 (0.63 [0.61, 0.65] of the gap). Cut from the prose: the paired-seed sentence and "NCR closes less of its gap" (argument, uncited).
- Flag, not actioned: per attack profile the second step closes 0.95, 1.10, 0.04 and 0.54 of the ASP gap (duration_ablation_numbers.json gap_closed). c3's ASP does not move with its tactic durations, which ch6's averaged "about two thirds" hides. For Marc.
- Build 87 pp.; one undefined reference (the pending ch4 app:detector-memory).

### 13.y Appendix E cut to the ablation (Marc 2026-10-14)

- Old E.2 (attacker behaviour metrics counted in attack actions; Tables tab:fa-openings, tab:fa-after-foothold) cut (Marc: "not that important"). f6 removed from main() in tools/further_analyses_tables.py, and the tab_FA-6/6b files deleted.
- Appendix E is now the single analysis: **"Post-hoc ablation of the tactic durations"**, with labels app:further-analyses and app:fa-run-time on the chapter and no section heading. The opener is merged into the lead.
- ch6 (auto): the metrics threat loses "recounted in attack actions, the gap holds (App. E.2)", so it now states the tactic/attack-action counting difference with no mitigation. T9 (thr:posthoc) is now singular and names the ablation and Table 5.2. §6.1 adds "all of it for c1 and c2 but almost none for c3" to "about two thirds of its gap in ASP" (Marc's yes).
- Build 86 pp.; one undefined reference (ch4 app:detector-memory, pending).

### 13.z The ablation moves into D as D.6 (Marc 2026-10-14)

- Appendix E is gone. Its single analysis is now **D.6, "Ablation of the tactic durations"** (Table D.11), after D.5's sensitivity analysis. The labels app:further-analyses and app:fa-run-time are on D.6, so every ch6 and ch7 pointer resolves.
- The post-hoc disclosure is kept: the lead's "chosen after the results of Chapter 5 were seen … Section 6.5 bounds its use (T9)", and T9 itself. Both were run on 2026-10-12, after the ch5 results.
- D opener: the first five sections back Chapter 5; the last, the ablation, backs Chapter 6.
- **Appendices now:** A proposal, B scoring, C APT attacker model, D MTD evaluation (D.1–D.6). Build 86 pp.; one undefined reference (ch4 app:detector-memory, pending).

### 13.aa Appendix B retitled (Marc 2026-10-14)

- "The attacker models scored on the eight properties" → **"Predicate tests of the attacker models"**. This overturns the earlier title, which reused Table 3.3's caption wording. Marc found it rhetorical: it restates what ch3 already does instead of naming what B adds, the level below the marks. "Predicate" and "mark" are ch3-defined terms (3.3.2); the new title matches the table's short caption ("Each attacker model tested on each predicate") and reads clearly on its own in the contents.

## 14. Chapter 7 first draft (2026-10-14, DRAFT STATE)

Marc: "get the draft conclusion down … short, sharp and relevant … everything up to about 6.4". The `draftnotes` slot blocks are replaced by prose; they stay in git at 42be1a7d.

**Shape.** The introduction's mirror, from specific to general (Bunton 2005's moves; Charles 2024, *Writing your Introduction & Conclusion chapters*, Digital Health CRC, after Mullins & Kiley 2002: examiners read the abstract, the introduction and then the conclusion first, so "write your conclusion with your introduction open"):
1. the RQ answered;
2. ch1's two contributions in ch1's order and nouns, each with its SQs, evidence, impact and bound;
3. future work, each item opening on the 6.5 limitation or threat it lifts;
4. a close that returns to ch1 P2's advantage of time.

**Words: 945 against ~800.** Preamble 106, C1 189, C2 212, future work 437. Cut candidates, in order:
- future work item 3 (four directions in one bullet);
- C2's third implication, if 6.4 ¶3 is judged enough;
- C1's sentence on the gains over the baseline attacker.

**Stale slot-sheet items, corrected in the draft against ch6 as of 42be1a7d:**
- "deployments that cost nothing" no longer appears in ch6; the bound now uses 6.5's "no efficiency metric";
- "another simulator needs the interface" is cut, since it was cut from 6.4 ¶3;
- the lowest-NCR-reduction lower bound is cut: it was parked in 6.4 and never drafted;
- C1's bound followed 6.3's close, which has since been cut. It now follows 6.3 ¶2 (threat reports give the order; judgement sets the tactic durations and the failure matrix) and ¶3 (no actions on objectives);
- §3's "five in part" is wrong: Table 6.1 and ch1 both give three in part;
- C2's candidate number (the host layer halving NCR to 1 000 s) is not in ch6, so it is not used.

**Future work: no F-labels.** No sentence refers back to a future-work item. Each item cites the threat it lifts instead (`\ref{thr:*}`).

**Open for Marc:**
- (a) Properties 6 and 7 (cost–benefit reasoning and learning) get no future-work item. No attacker model has them, but 6.5 names no limitation to open on.
- (b) The two closing sentences: keep the advantage-of-time return, or end on the attack actions alone?
- (c) The ch1 overview says ch7 "sets out future work". It still holds.

Build: 82 pp.; one undefined reference (ch4 `app:detector-memory`, pending).

### 13.bb The two passes merged; Marc's rulings applied; Table C.4 stale rows (2026-10-14/15)

- Both passes merged:
  - design: D.7, D.6 and C.4; record `2026-10-14_appendix_float_design.md`;
  - prose: record `2026-10-14_appendix_prose_pass.md`.
  The D.7 caption conflict was resolved to keep both passes' wording. The prose pass's dropped definition of a failed attack action (D.6 lead) was restored.
- Marc ruled the passes' questions 1–6 "plausible", applied:
  - C.2 lead kept;
  - D.2 precision loop fixed in `ch5_disruption_figure.py` (−0.2, not 0; widths rebalanced so nothing wraps);
  - D.6 caption names its negligible cells (generated);
  - ch6 §6.4 "same layer order";
  - ch4 §4.4.2 band sentence;
  - D.5 S1 "Most tactic durations are our judgement".
  The ch6 metrics threat gets the inline recount (190 to 844 distinct openings over eight attack actions against 3; from `further_analyses_numbers.json` f6).
- **Table C.4 audited for stale rows** (Marc: "per-tactic duration multipliers, we don't even use that anymore"):
  - "Mean durations set by judgement" → "Mean durations of nine tactics", since the group label already says judgement;
  - the "half the 45 s" row is cut: it is the code's `relative_multiplier` 0.5; 22.5 s is one of the nine and moves with the 45 s in D.5;
  - "Share of weight given to the pre-intrusion overlay" → "Weights of the pre-intrusion overlay" (§4.3: "Their weights are declared");
  - the MTDSim row reads "Mean durations of six tactics, from MTDSim's scans and exploit".
  thr:values: "two were not tested". The other rows were checked against ch4 and hold. "Membership of each attack profile" under Attack Flow corpus is borderline (§4.2 answers from the CTID descriptions, ATT&CK pages and threat reports, three by us), left as is.
- Layout: the D.6 caption lost its axis restatement, and D.5 starts on a new page (`\clearpage`). Build **82 pp.**; one undefined reference (ch4 app:detector-memory, awaiting Marc).

## 15. The draft against the yardstick (2026-10-15, NOT RULED)

Marc: "what is the convention for each of these … best practice … common pitfalls … then the structure and the ideas will become obvious … then I'll scope down to the preamble first". The yardstick is now [`docs/workflows/conclusion_conventions.md`](../workflows/conclusion_conventions.md) (three research passes; sources and read status there). It **corrects §1's Bunton line**: five moves ending on a close is Bunton's humanities model; his science-and-technology model ends on future research (a close in 1 of 25), while CS theses close on a recap in 60 % (Soler-Monreal 2016). Both are met by a last sentence that names the next step as the continuation of chapter 1's problem.

**Verdict.** The skeleton is the conventional one (unheaded preamble, Contributions, Future work, a close; Soler-Monreal's M1–M5 in order), so no heading moves. The defects are inside the parts: the answer is given twice, contribution 1 repeats chapter 1, contribution 2 replays 6.4, and two future-work items are lists. The chapter is ~1 020 prose words against the yardstick's 650–900 (4–6 %); the ledger says 1 250 and §1 says ~800.

| Part | Meets | Pitfall (yardstick §) |
|---|---|---|
| **Preamble** (~106 w) | RQ restated once in ch1's words, then answered in the same paragraph; concrete (layers, "no mechanism most effective against both"); the last clause mirrors ch1's "far simpler than an APT". | (1) Its last sentence is contribution 2's claim, so the answer is given twice (d2, "answered twice"). (2) "No MTD mechanism is the most effective against both" is the abstract's "the most effective MTD mechanism differs between the two attackers" (d1, "the abstract again"). (3) Says which outcome happened, but ch1 names no possible outcomes to choose from (UWA Introduction criterion): **ch1 matter, flagged, not actioned.** |
| **Contribution 1** (~189 w) | Ch1's noun and order; SQ1+SQ2 named; evidence back-referenced (Table 6.1); bound in its own paragraph (judgement for durations and failure matrix; no actions on objectives). | (1) Its first and fifth sentences are ch1's contribution sentences almost verbatim (d2, "verbatim repetition"; same nouns ≠ same sentences). (2) The middle walks the method (attack flows → Petri net → mapping): a recap, not a claim (d2, "activity list"; (e) "summary"). (3) Significance is ch1's "any study using MTDSim can run it", asserted, not argued: who changes what (d2 part 4). |
| **Contribution 2** (~212 w) | Refutable claim in ch1's noun; SQ3 named; the cause attributed and bounded at once (thr:cause); significance names its reader (an MTD evaluation). | (1) Three implications in full are 6.4 replayed (e, "further discussion", "repetitive cycles"). (2) The bound sentence stacks four limits (d4-style hedge stack; 6.5 owns the list). |
| **Future work** (~440 w + 2 placeholders) | Lead sentence names the anchor rule; each item opens on its 6.5 limit in one clause (Brutus G7 met); item 4 (cause of the host layer's result) answers an open question the results raised (UWA item 6); items 4 and 5 have objective, method and payoff. | (1) Items 2 and 3 each carry four directions: wish lists, and "other networks" has no method (d3, "wish list", "generic"). (2) The order principle (6.5's order) is in a comment, not the lead (d3). (3) **No forward pointer in chapter 6 exists** (`\ref{sec:future-work}` has no caller), so "unpaid promises" is vacuous and harvest D B11 is unmet: **ch6 edit, needs a ruling.** |
| **Close** (2 sentences) | Returns to ch1's advantage of time; names the next step (the attack actions); Marc's 2026-10-09 Q3 ruling. | (1) "MTD optimised against an attacker model inherits that model's assumptions" generalises 6.4: 6.4 argues only that MTDShield's choices are "consistent with a policy that learned to deploy the MTD mechanism that disrupts its training attacker most" ((e) "new material", mild; the MTDShield instance is earned, the general rule is not). (2) "can be tested only once the attacker model assumes less" ends on what the thesis could not do (d4, "ending on a deficit"); two hedges ("may", "only once"). |

**The decisions the structure turns on** (for Marc, one at a time, preamble first):

1. **Where the answer lives.** Recommended: the preamble gives the answer (the RQ answered, including the general "can depend" sentence); contribution 2 opens on the warrant and the impact, not on the claim again. Alternative: the preamble stops at the MTDSim finding and the general sentence moves to contribution 2.
2. **Budget.** Recommended: ~850 (preamble ~100, contributions ~150 each, future work ~350, close ~50), inside the yardstick's band and below the draft by ~170.
3. **Contribution 1's shape.** Restated as delivered: the claim (the model runs, against the field's at most one in full), what it lets an MTDSim evaluation do, its bound; the method walk cut to a clause.
4. **Contribution 2's implications.** Compressed to the one an evaluator acts on, with a pointer to 6.4 for the rest.
5. **Future work.** Each item carries anchor, objective, method and payoff; items 2 and 3 split or cut to one direction each; the lead names the order.
6. **Chapter 6's forward pointers** (ch6, auto after a ruling): one `\ref{sec:future-work}` from 6.5's scope paragraph.

## 16. The preamble, defined (2026-10-15, NOT RULED)

Marc: "what do we need to explain to the reader, what do we not … what is the preamble doing … it's giving the answer … currently it just seems like a stitch together of a lot of different ideas … so what?"

**Job, in one sentence.** Answer the research question: say what "performs" turned out to mean in MTDSim, and why that answers the question's "APT attackers" and not only the APT attacker model.

**Why the draft reads stitched.** Four sentences, four jobs, no single answer:
- S1 restates the question (fine).
- S2 says "performs differently", which is true but names nothing (voice §(0) check 5).
- S3 packs three findings. The third ("no MTD mechanism is the most effective against both") is the abstract's and ch1's highlight a third time; the first two (the layers) are the concrete answer but sit as evidence.
- S4 is the so-what, behind "therefore" and two hedges ("can", "may not").

**What the preamble adds that the abstract and ch1 do not.** Both already state that the most effective mechanism differs. The preamble's new content is (a) the statement *as the answer* to the question; (b) the layer pattern, 6.2's answer to SQ3, one level more concrete than the mechanism headline; (c) the step from the APT attacker model to APT attackers, with its one hedge.

**On the page / off the page** (audience: the examiner and a fourth-year CS student who has read, or skipped to, ch7):

| On the page | Off the page, and where it lives |
|---|---|
| The question, once, in ch1's words | The problem and the gap (ch1 P3) |
| "Performs differently", made concrete: which layer reduces NCR more, for each attacker, at every deployment interval | How the APT attacker model is built (contribution 1; ch4) |
| The measured scope: "in MTDSim", "the APT attacker model" | Why the layers differ: tactic durations and order (contribution 2's warrant; 6.2) |
| The step to the question's reach: which MTD an evaluation finds most effective can depend on its attacker model, so an evaluation against a simplified attacker alone cannot show how MTD performs against APT attackers | What an evaluator should do (contribution 2's impact; 6.4) |
| | The numbers: 92 % / 36 % is in the abstract and ch1 already |
| | Every bound beyond "in MTDSim" (contribution 2's bound; 6.5) |
| | Definitions of NCR, the layers, the baseline attacker (ch2, ch4): never re-defined |

**Slots** (job + facts + ceiling; ~80–100 words, three sentences):
- **P1, the question.** *Job:* put the RQ back in front of the reader as what was asked. *Facts:* "How does MTD perform against APT attackers?" (ch1). *Ceiling:* once; may fold into P2 as a clause.
- **P2, the answer at the measured scope.** *Job:* say what "differently" means. *Facts (6.2 ¶1):* at every deployment interval, the host layer reduces the APT attacker model's NCR more than the service layer does, and the service layer reduces the baseline attacker's more than the host layer does. *Ceiling:* "in MTDSim"; "the APT attacker model", never "APT attackers"; no cause; no number.
- **P3, the so-what.** *Job:* carry the answer from the model to the question's APT attackers. *Facts (6.4 ¶1, reworded, not copied):* the most effective MTD mechanism can depend on the attacker model, so an evaluation against a simplified attacker alone cannot show how MTD performs against APT attackers. *Ceiling:* one hedge ("can"); not "MTD fails against APTs"; not "the APT attacker model is the right one".

**Consequence for contribution 2 (decision 1):** it no longer opens on "the most effective MTD mechanism depends on the attacker model" as a fresh claim; it opens on the warrant (the cause and its bound) and the impact.

## 17. Contributions: how many, at what level (2026-10-15, NOT RULED)

Marc: "is having two contribution points the correct approach here … in terms of the guidance as well". Tested against `conclusion_conventions.md` (d2) and its sources.

| Guidance | What it asks | Two, at the knowledge level |
|---|---|---|
| EGZ p. 72 (single aim); Peyton Jones ("one ping") | Few, all serving one aim | Both serve the one RQ; the preamble is the one ping, contribution 1 its means |
| Trafford & Leshem p. 141 | "Restate the gap … then rephrase it as a contribution" | Ch1's gap has two halves: MTD is rarely tested against an APT (contribution 1 fills it) and is tested against far simpler attacker models (contribution 2 shows that matters) |
| Trafford & Leshem p. 142 | One sentence per aspect, "no more than two variables" | 1: the model × the eight properties; 2: the attacker model × the most effective mechanism |
| EGZ pp. 66–67, 72, four kinds of significance | Name the kind | 1: a contribution to a research programme (the next step in the MTDSim lineage, Brown → Zhang → Ho → Tay); 2: advancing knowledge |
| Dunleavy p. 39 | The commonest originality: an idea taken "for a walk" | 1: Attack Flow's CTI carried into an MTD simulator |
| Soler-Monreal Table 9 | CS conclusions present a product (66.67 %), evaluate it (37.5 %), give findings (93.75 %) | 1 = product + its evaluation; 2 = finding |
| SIGSOFT Engineering Research | An artefact contribution is evaluated; antipattern: "incidental implementation aspects" | 1 is evaluated (Table 6.1); the draft's method walk is the antipattern |
| Peyton Jones (refutable); Ernst (outcome, not activity) | A claim an examiner could falsify, not the work done | Both pass at the knowledge level; "we built / we ran" does not |
| EGZ p. 70; Golding p. 570 | Ch1 and ch7 match | Two, in ch1's order and nouns |

**Rejected:** three (capture has no measurement of its own, so fails the refutable test); one (discards an evaluated artefact); implications as a third (they are contribution 2's significance); the eight properties (folded 2026-10-07, the yardstick).

## 18. Overclaim check on the preamble's last sentence (2026-10-15, NOT RULED)

Marc: "did you evaluate its potential for overclaim … does 6.5 licence that sort of claim?" The sentence, "How MTD performs against APT attackers cannot be inferred from an evaluation against an attacker model far simpler than an APT", now also closes ch1 contribution 2 (l.597, front-three session, b0c0a278) and is the candidate for the abstract closer (front-three A4).

- **Licensed reading (epistemic):** a simplified-attacker evaluation is *insufficient evidence* about APT attackers. Entailed by sentence 4's "can depend" (an existence claim, shown in MTDSim): if the ranking can change with the attacker model, an evaluation against one model carries no evidence that its ranking holds for another. Survives T8 (rules) and T10 (observation), since it needs only that invariance is unestablished, not that the reversal recurs elsewhere.
- **Unlicensed reading (empirical):** such an evaluation *gets APT performance wrong*, in any simulator. That needs the reversal to generalise beyond MTDSim's disruption rules (T8) and the APT attacker model to stand for APT attackers (T9, T10); 6.5 grants neither. "Cannot be inferred" admits both readings.
- **Missed in §16:** the claim is in no ch6 paragraph. 6.4 ¶1 stops at "can therefore depend on its attacker model". Yardstick (g)4: every ch7 claim traces to ch6.
- **House scheme (threats handoff §23):** reach beyond MTDSim takes "may". The sentence is exempt only under the epistemic reading.

**Recommended:** say the epistemic reading outright, and give it a home in 6.4 ¶1 (ch6, auto after a ruling): *"An evaluation against an attacker model far simpler than an APT is therefore not enough to show how MTD performs against APT attackers."* Ch1 l.597 and the abstract closer then take the same words.

## 19. Contribution 1, defined (2026-10-15, NOT RULED)

**Format.** One plain paragraph per contribution, opened "The first contribution is …". Paragraph, not bullet: ch1's bullets are the promise list (Peyton Jones), a conclusion wants "a short summarizing paragraph" (Widom), and thesis corpora use prose. No bold run-in label: with two items the ordinal opener is the label, and nothing refers back to "Contribution 1" (the future-work rule, §14). Run-in labels stay where text cites them (6.5's threat types).

**Job.** Deliver ch1's first promise: the gap's first half filled (MTD "is rarely tested against [an APT]"), as a contribution to the earlier MTDSim studies, evaluated against the field.

**"Research programme".** EGZ's category, not on the page: the dissertation's term is "the earlier MTDSim studies" (ch2, Table 2.2). The sentence it licenses: the baseline attacker is the attacker MTDSim was built with (ch2 l.~823); the APT attacker model is the first that runs in its place. *Verify before drafting:* Zhang 2023's adversary profiles are variants of the baseline, not a second attacker (ch2 is silent).

**On the page / off the page:**

| On | Off, and where it lives |
|---|---|
| The claim, in ch1's noun: an APT attacker model any study using MTDSim can run in place of the baseline attacker | The attack graph, attack profiles, partition, 38 attack flows (ch4) |
| SQ1's answer as a finding about threat reports: they record the order of an attack's tactics by objective, almost never how long a step took, never what followed a failure. Strength and limit are one fact (voice §c5) | Petri-net mechanics, the mapping of 8 of 15 tactics (ch4, 6.3) |
| SQ2's answer in one clause: the order runs in MTDSim as a Petri net over the baseline attacker's six attack actions | The eight properties' definitions, each mark (ch3, Table 6.1) |
| Deciding evidence, more concrete than ch1: the only one of four attacker models with choice of attack strategy in full or any objective-specific behaviour (6.3 ¶1) | Ch1's "two in full and three in part … at most one in full", already said twice (ch1, 6.3) |
| Significance: what an MTDSim study can now do that the earlier ones could not | The gains over the baseline attacker list (6.3) |
| Bound: judgement where MTD disrupts it (6.3 ¶2 close); MTDSim's attack actions cap it, no actions on objectives (6.3 ¶3 close) | Code verification, sensitivity analysis, the public repository (ch1 footnote, 6.5) |

**Slots** (~130–150 words, five sentences):
- **C1-1 Claim + questions.** *Job:* name the contribution and what it answers. *Facts:* ch1's noun phrase; SQ1, SQ2. *Ceiling:* ch1's noun, not ch1's sentence; "built", "runs", never "reproduces APT behaviour".
- **C1-2 SQ1 answered, with its bound.** *Job:* what threat reports can give an attacker model. *Facts (6.3 ¶2):* the order of tactics by objective, yes; step durations, almost never; responses to failure, never; so the tactic durations and the failure matrix, where MTD disrupts it, rest on our judgement. *Ceiling:* one sentence, the concession in the same breath.
- **C1-3 SQ2 answered.** *Job:* how it runs. *Facts (6.3 ¶3):* a Petri net choosing its next tactic at runtime over MTDSim's six attack actions. *Ceiling:* one clause; may fold into C1-1.
- **C1-4 Evidence against the field.** *Facts:* Table 6.1; the only one of four with choice of attack strategy in full or any objective-specific behaviour. *Ceiling:* no count repeated from ch1; "more of the eight properties", never "an APT".
- **C1-5 Significance + ceiling.** *Job:* who can now do what, and how far. *Facts:* an MTDSim study can test MTD against an APT attacker model beside the attacker MTDSim was built with; limited to finding and compromising hosts, no actions on objectives. *Ceiling:* "can"; the ceiling as the last clause.

## 20. The lineage check for contribution 1 (2026-10-15, NOT RULED)

**Verified: every earlier MTDSim study ran one attacker, the baseline attacker.**
- Zhang 2023's "adversary profile" (§4.4.1, pp. 27–28) describes that one attacker along four dimensions (objectives, exploiting vulnerabilities, command and control, credentials); it is not a second attacker. It refactors only Brown's first scenario. `extractions/zhang2023.md` §A; intent spec IS-ADV-01 ("a description, not a configurable parameterisation, in every lineage paper").
- Ho 2024 and Tay 2024 reuse Zhang's attacker unchanged (Ho l.242, Tay l.206; ch3 round 55/60 comments; `extractions/tay2024.md`: "Nothing added on the attacker side").
- Two of the four ask for this work as future work: Zhang §6.3 (p. 42, `lit_review/zhang2023.md` l.519): "a more intelligent attack profile … enabling future works to evaluate the effectiveness of MTD techniques against a more advanced adversary"; Ho §5.1: "more complex adversaries", "only one type in the simulator" (`extractions/ho2024.md` H-FW-01).

**Wording options for the significance sentence:**
- A, superlative ("the first attacker other than the baseline attacker"): verified over the closed set, but a novelty word the SIGSOFT antipattern list flags.
- **B, fact form, recommended:** "Every earlier MTDSim study evaluated MTD against the baseline attacker alone." Verified, no superlative; the claim sentence's "any study using MTDSim can run [it] in place of the baseline attacker" then lands as the change.
- C, B plus the lineage's own call ("as Zhang and Ho proposed"): the strongest significance, but a citation first met in ch7 (yardstick (e) "new material"). Needs a home first, e.g. one clause in ch2's lineage paragraph (ch2: proposed first). Flagged, not actioned.

## 21. Contribution 2, defined (2026-10-15, NOT RULED)

**Job.** Deliver ch1's second promise: the gap's second half (MTD is tested "against attacker models far simpler than an APT") shown to matter. EGZ's kind: advancing knowledge. The preamble already gave the answer, so this paragraph carries the **warrant** (why, and how far) and the **impact** (what an MTD evaluation changes). It does not answer the question again.

**On the page / off the page:**

| On | Off, and where it lives |
|---|---|
| The claim as a label, ch1's noun, parallel to contribution 1's opener; answering SQ3 | The layer pattern and "at every deployment interval" (the preamble) |
| The cause, owned: "we attribute" the difference to the APT attacker model's tactic durations and the order of its tactics (6.2 ¶1, 6.4 ¶3) | The numbers: 92/36 (abstract, ch1, 6.4), ρ = 0.01, MTDShield's 68/28/33/75 (6.4) |
| The cause's bound in one clause: no run under MTD separates the two, or rules out the tactic-to-action mapping (thr:cause) | Why the host layer works: footholds, IP shuffle (6.2) |
| The finding's bound: MTDSim's disruption rules and the 38 attack flows, the two threats 6.5 states for SQ3 (thr:rules, thr:corpus) | Network size, scenario, simulation only (6.5 ¶1's scope; "in MTDSim" carries it) |
| The conceptual conclusion (6.4 ¶3): an attacker model that differs in little more than when and in what order it runs a simulator's attack actions can change how MTD is measured to perform | The efficiency implication (6.4 ¶2b, a hypothesis) |
| The impact, 6.4's two shoulds: report metrics against an attacker model other evaluations use; test a learned deployment strategy against one it was not trained on, with MTDShield as the one instance (beats random against the baseline attacker, not against the APT attacker model) | ASP agreement (thr:ncr); MTDShield's service-diversity choice and thr:mtdshield (6.4, 6.5) |

**Slots** (~150–160 words, six sentences; order: what we found → why → how far → what it means → what to do, ending on the concrete instance):
- **C2-1 Claim + SQ3.** ch1's noun phrase; "answering SQ3", as contribution 1.
- **C2-2 Cause, owned, with its bound.** "We attribute …" (house scheme); thr:cause in one clause.
- **C2-3 Finding's bound.** Disruption rules, the 38 attack flows; pointer to 6.5.
- **C2-4 Conceptual conclusion.** "can change" (shown to happen); same attack actions, different timing and order.
- **C2-5 Impact 1.** Report metrics against an attacker model other evaluations use.
- **C2-6 Impact 2 + instance.** A learned deployment strategy tested against an attacker model it was not trained against; MTDShield.

**Options for Marc:** (a) C2-4: keep (the conceptual step; it is what tells a simulator's users that a cheap attacker model matters) or cut (overlaps the preamble's "can depend"); *recommend keep*. (b) "The finding does not make either attacker model the better one": keep as negative scope (voice §c6) or leave in 6.2; *recommend leave*: C2-2's "we attribute" and the preamble's "not enough to show" already say the APT attacker model is evidence, not truth.

## 22. Future work against the yardstick (2026-10-15, NOT RULED)

Marc: "the opening line seems a bit vacuous … a bit vestigial … appending random things … I feel like future work probably has a number of taxonomies". Yardstick `conclusion_conventions.md` (d3), (d4).

**Kinds of item (the taxonomy).** UWA scores two: (5) improvements that lift a recognised shortcoming; (6) open questions the results raised. Hu & Wan 2015 (724 future-work sentences) code the object: the *problem* (extend, apply elsewhere, a new problem), the *method*, the *evaluation* (new data sets, metrics). Each item carries anchor → objective → method → payoff (Suray et al. 2024: specific means objective *and* method).

**Structure audit:**

| Element | Verdict | Why |
|---|---|---|
| Lead "Each direction below lifts a limitation or a threat of Section 6.5" | Rework | It names the anchor rule but not the order principle the guidance asks the lead to state; it describes the list, says nothing the items do not |
| Bullets | Keep | No source requires prose; parallel items, findable (Suray §6); Marc's 2026-10-09 ruling |
| Italic label naming the *limit* ("The six inherited attack actions, one line …") | Rework | It restates the limitation (Brutus G7, redundant); the label should name the *direction*, the `\ref` carries the limit |
| Closing "Of these directions … come first" paragraph | Keep as the close, rework its job | A close naming the next step is the convention (Dunleavy p. 207; Thomson); ranking the items is not. Defects as §15: generalises 6.4, ends on what the thesis could not do |

**Item audit:**

| Item | Verdict | Reason |
|---|---|---|
| 1 Attack actions | Keep, sharpen | The binding limit (6.3 close, 6.5 ¶1). Payoff concrete: Table 6.1's objective-specific behaviour and adaptivity, both in part |
| 2 Scenario, 50 hosts, 15 000 s, emulation | Split | Four directions (wish list). Emulation is an item of its own (cho2020's ladder, ch3 §3.2); other networks and longer runs have no method (generic); the general attack scenario is specific (thr:ncr) but small |
| 3 IDS, efficiency, deployment-strategy awareness, MTDShield retrained | Split | Four directions. Marc: IDS is a whole piece of work; efficiency on its own in simulation layers assumptions on assumptions, so it belongs where overhead is measurable, i.e. emulation (`notes/ch8_future_work/emulation_rung.md` says the same). MTDShield retrained is the open question 6.4 raised (UWA item 6) |
| 4 The cause of the host layer's result | Cut | Marc: no successor re-validates the thesis; it reads as unfinished work (Thomson 2018) and as future work standing in for a mitigation (Feldt & Magazinius). The residual stays in thr:cause. **Overturns** the 2026-10-15 "varying the mapping" placeholder |
| 5 The 38 attack flows | Keep, sharpen | Grounded already: ch3 sets automated profiling (ChronoCTI rahman2025, AttacKG+ zhangY2025) against manual, with buchel2025's 80 % precision at 66 % recall. The method is the hybrid: language models draft, analysts check |

**Proposed set (5 items), ordered by the dissertation's spine (capture → model → evaluate):**
1. *Capture:* attack flows drafted by language models and checked by analysts (thr:corpus) → each attack profile from more than 5–7 attack flows, and from APT reports alone.
2. *Model:* attack actions for the whole campaign (6.5 ¶1, thr:rules) → actions on objectives, a failure that knows MTD caused it, several lines at once; payoff: Table 6.1 properties 2 and 4.
3. *Model:* an IDS in the loop (6.5 ¶1) → the Snort rule (§4.5) raising alerts during a run; payoff: detection avoidance tested directly, and reactive MTD deploying on an alert.
4. *Evaluate:* MTDShield retrained against the APT attacker model (the question 6.4 raised) → does a learned deployment strategy beat random against the attacker model it learned?
5. *Evaluate:* emulation (simulation only, no efficiency metric, thr:rules, thr:observation) → overhead and loss of service beside NCR reduction, so an evaluation can choose a deployment interval; and whether the host layer's lead survives real disruption.

**Cut or folded:** item 4; other networks and longer runs (generic); the 18 attributed attack flows (a sub-case of item 1); deployment-strategy awareness (option: a clause in item 2); the general attack scenario (option: own short item, tied to thr:ncr). **Overturns** the 2026-10-15 general-scenario placeholder unless kept.

**Rulings on §22 (Marc 2026-10-15):** the five items and the capture → model → evaluate order: yes. Cause item: cut. General attack scenario: **cut** ("very study-specific … a very small study"). Deployment-strategy awareness: **left out**, and never framed as a gap: game-theoretic MTD models the defender and attacker as competing agents, so some have it, and the comparative survey (Table 6.1) covers none of them; "no attacker model has it" would mislead. Open: a sweep of every future-work idea raised during the ch6 sessions, so each is either in the five or excluded on a stated reason (§23).

## 23. Sweep of every ch6-era future-work idea (2026-10-15, NOT RULED)

A read-only sweep (registry F1–F13/B1–B21 at tex ~9459–9693; handoffs H-AFF, H-ASM and harvests, H-RED, H-THR, the memory handoff; notes ch7_discussion/ and ch8_future_work/; ch6–ch7 `%` comments) found **54 distinct ideas**: 20 in or folded into the five, 11 on the ruled-out list (+2 by class), 5 excluded earlier with a stated reason, **18 not covered**. Full ledger: the sweep's report of this date (agent return, not committed); the decisions are below.

**Two owed items the five dropped (verified at source):**
- **Dynamic weighting** (supervisor): H-RED §12, Q8 ruled yes, "Owed: dynamic weighting in Future work" — weights that change with what the attacker observes; the constant weights let it choose an exploit before a scan.
- **A memory that acts on the next hop** (ruled future work 2026-09-29, memory handoff §7.2/B4): dry run +3.55 hosts [+2.22, +4.88], 20 seeds, preliminary; a richer exploit action.

**Proposed restructure of the model step (follows from the two owed items):** one item per Table 6.1 property the APT attacker model has only in part (2, 4, 5), so each model item names the mark it lifts.
- *Attack actions* (property 2): actions on objectives, several lines of the campaign at once, a richer exploit (the next-hop memory).
- *A choice that depends on what the attacker observes* (property 4): dynamic weighting; a failure that knows an MTD deployment caused it.
- *An IDS in the loop* (property 5).
Capture (1) and evaluate (MTDShield retrained; emulation) unchanged: six items.

**Not covered, triaged:**

| Row | Idea | Proposed |
|---|---|---|
| 22 | Edge ablation tied to mitigations (Marc's "graph theory") | Marc's call; lean exclude: the literature (attack-graph hardening) is unchecked, it proposes defences beyond the RQ (existing MTD), and its first step is the edge ablation cut with the cause item |
| 21 | Real CVEs instead of synthetic vulnerabilities | Fold into emulation (real software carries real CVEs) |
| 17 | Simpler stand-ins (reversed edges, one duration), ruled 2026-10-07 to 6.5 with a §7.2 pointer | Exclude: the re-validation class; **overturns** the 2026-10-07 pointer ruling |
| 18 | Properties 6–7 (cost–benefit, learning) | Exclude on the awareness ruling's logic: game-theoretic and learning attackers outside the survey have them; 6.5 names no limit |
| 28 | Post-intrusion MTD (a new mechanism) | Exclude: a new defence is a different RQ (existing MTD only); new literature |
| 33 | Lowest NCR reduction across attacker models as a lower bound | Exclude: an evaluator guideline, never drafted in 6.4; not future work |
| 31 | Jalowski's state-of-the-art comparator | Exclude: evaluation design, not a 6.5 limit |
| 4, 5, 12, 34, 40 | Confidence weighting; second coder; FSM vs Petri net; open "why" questions; validating the property set | Exclude: re-validation / unfinished work (the cause item's class) |
| 6, 30, 44 | Threat modelling; "MTD by default"; optimal adversary | Exclude: no method, unchecked literature |
| 16, 19, 20, 26, 43, 53 | Costed port discovery; campaign give-up; single-actor nets; fixed-set learned strategy; order-aware divergence; IP addressing | Exclude: minor, no claim-changing payoff, or not raised in the ch6 sessions |

**Consequential fixes (outside ch7):**
- **Ch4 l.3935** promises "deployment-strategy awareness is left to future work", against the 2026-10-15 ruling. Ch4 (proposed first): cut the clause, or end the sentence at "slower than the baseline attacker".
- **Ch6 has no `\ref{sec:future-work}`** (§15, open).

**Rulings on §23 (Marc 2026-10-15):** six items, the model step split by the three in-part properties: yes. Edge ablation: excluded. Ch4 l.3935 clause: cut (applied). Ch6 forward pointer: one sentence at the end of 6.5's scope paragraph, "Section 7.2 proposes work that lifts each of these limits" (applied, ch6 auto-gate). Only the scope limits point forward; each threat keeps its mitigation and residual, and 7.2's items point back to them by `\ref`.

## 24. Future work, decomposed and drafted (2026-10-15, DRAFT STATE in the tex)

Marc: "frame each of these six items … in terms of the best practice … push a full change to the PDF". Each item in the yardstick's four parts; the tex carries the prose.

| Item (label) | Anchor | Objective | Method | Payoff |
|---|---|---|---|---|
| Attack flows drafted by language models (SQ1) | thr:corpus: 3 of 4 profiles on 5–7 flows, not all APT | More attack flows per profile, APT reports only | Automated attack profiling (ch3 §subsec:profiling) drafts from APT campaign reports (ATT&CK campaign entries); analysts check (ch3: automated is not yet reliable) | Tests whether the SQ3 finding holds beyond the 38 attack flows |
| Attack actions for the whole campaign (SQ2) | Property 2 in part: Collection, Exfiltration, Impact unmapped (6.3) | Actions on objectives; one token per line of the campaign; a richer exploit | New attack actions, each with its disruption rule (thr:rules); context per attack action | Each profile pursues its objective; several lines at once; the memory (negligible on NCR, §5.4) gets more to act on |
| A choice that depends on what the attacker observes (SQ2) | Property 4 in part: fixed failure matrix (6.3); constant weights (§4.3) | Next tactic depends on state; response to failure depends on cause | Weights that change with hosts, ports and credentials held (dynamic weighting, supervisor); a failure that records MTD as its cause | Adaptivity grounded in the run, not a fixed rule |
| An IDS in the loop (SQ2) | Property 5 in part: no IDS, detection by proxy; attack confidentiality counted after the run (§4.5.1) | Alerts during a run | Snort's port-scan rule applied in the run | Detection avoidance tested directly; MTDShield reads alerts, not the attack action |
| MTDShield retrained against the APT attacker model (SQ3, UWA item 6) | thr:mtdshield: worse than random, credited to training | Learned strategy trained on the APT attacker model | Retrain in its training environment; test against both attackers beside random | Whether a learned deployment strategy beats random against the attacker model it learned from |
| Emulation (SQ3) | Simulation only, no efficiency metric (6.5 ¶1), thr:rules | Run the attack profiles against MTD on real software and vulnerabilities | Emulation (ch3 §subsec:evaluation-methods) | Overhead and loss of service beside NCR reduction, so an interval can be chosen; whether the host layer's lead survives real disruption (C2 keeps a host) |

**Close:** attack actions first (Marc Q3, 2026-10-09), then a return to ch1's advantage of time as the next step's aim. Cut its generalisation of 6.4 and its deficit ending.

**Words:** chapter ≈ 900–925 (7.2 ≈ 530–550 with lead and close), just over the yardstick's 650–900. The close spills four lines onto p. 48; the cut pass (Marc 2026-10-08, overdraft then cut) is the lever. Candidates: item 2's third sentence (the richer exploit), item 6's last sentence, item 1's anchor sentence.

**Opener and close (Marc 2026-10-15, option C):** merged into one lead sentence carrying the priority ("Of the directions below, the attack actions come first, because every result of this dissertation rests on what they let the APT attacker model do"); the order sentence and the advantage-of-time close cut. The emulation item's last two sentences swapped so the chapter ends on its payoff. Overturns Q3's close (2026-10-09); the priority survives. Yardstick (d3), (f), (g)12–13 updated.

## 25. Item-by-item review of 7.2 (Marc 2026-10-15)

**Item 1 → "Automated attack profiling."** The old label named our input format and the tool. Chapter 3's term already covers language models. The verbs are now thr:corpus's own ("drawn from", "generalise"). The source is targeted by each attack profile's objective, which replaces the uncited "ATT&CK campaign entries".

**Item 2 → "Attack actions rebuilt for modelling APT tradecraft."** Marc: the attack actions need rebuilding from the ground up, not extending. "For the unmapped tactics" implies the mapped eight are right. Ch4 maps two of them by goal alone, and three share exploit. The anchor, objective, method and payoff were rebuilt from the yardstick, not regenerated to fit the label:
- **Anchor:** the model shares the baseline attacker's attack actions, so it stops at compromising hosts (6.1, by pointer).
- **Objective:** an open question (UWA item 6).
- **Method:** the ATT&CK techniques CTI records, not Attack Flow. Each needs what it acts on and a disruption rule (thr:rules).
- **Payoff:** actions on objectives (Table 6.1, property 2).

Retired, with reasons:
- *One token per line of the campaign:* covered by the rebuild; no 6.5 anchor.
- *The richer exploit for the vulnerability memory:* covered by the rebuild. This overturns its 2026-10-15 restoration as an owed item.
- *The comparability trade:* a rebuild gives up the shared attack actions that C2's attribution rests on. It is implied by the anchor, and Marc judges the better model worth it.
- *ATT&CK mitigations:* separate from MTD (Marc). Also absent from the dissertation, so naming them would be a new claim.
- *MTD aimed at technique dependencies:* a second study (MTD design), with no 6.5 anchor.
- *Defense Impairment:* would reintroduce deployment-strategy awareness, ruled not a gap.
- *ATT&CK Persistence:* the tactic must not be confused with property 1, campaign persistence, which is met in full.

Build: 82 pp, 0 undefined, overfull count unchanged at 62. Next: item 3.

**Item 3 ("A choice that depends on what the attacker observes"): dropped (Marc 2026-10-15).** The item failed every part of the yardstick:
- It had two anchors. Dynamic weighting is property 3's limit (Q8), which ch6 never states. The failure's cause belongs to property 4.
- It held two studies.
- It had no payoff. The failure-matrix ablation (subsec:ablation-failure-matrix) finds a negligible effect on NCR, and time lost per MTD deployment is unchanged.

Marc: "dynamic weighting is the failure matrix with more assumptions"; the approach we chose was the failure matrix. This overturns Q8's "owed: dynamic weighting in Future work" (2026-10-11). The supervisor does not expect it, though register S1 had recorded it as the deferred eventual direction. The failure's cause comes nearly free with item 2's rebuilt attack actions. 7.2 now has five items. No forward pointer in ch6 referred to item 3.

**Item 4 (formerly "An IDS in the loop") → "Intrusion detection and MTD" (Marc 2026-10-15).** "X and Y" names an intersection without deciding which side serves which. MTDSim is now the method, not the objective. A tool-specific objective reads as an engineering ticket that one component will fix (Marc).

Kept from the original:
- the anchor in 6.1's own words;
- an alert raised each time the attacker trips the rule.

Added:
- the field-level open question: which IDS, where on the network it watches, how its alerts change how often MTD deploys;
- property 5's IDS predicate as the testable payoff ("tested on", not "would have": meeting it needs item 2's Stealth actions);
- reactive MTD as the payoff that answers the open question.

Cut:
- Snort named (decoration: attack confidentiality already defines the flagging rule);
- "in the loop";
- "tested directly";
- the Stealth/Defense Impairment chain;
- attack-confidentiality bookkeeping;
- MTDShield reading alerts (derivative; the next item is MTDShield's own).

Not claimed: "few papers join IDS and MTD", an unverified gap (yardstick (d3)); posed as an open question instead. The 6.5 pointer ("an IDS") still holds. Build: 82 pp, 0 undefined. Next: the MTDShield item.
