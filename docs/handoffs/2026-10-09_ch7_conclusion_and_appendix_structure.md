# Chapter 7 and the appendices: structure before drafting

**Status:** NOT RULED. Structure only; no prose. Opened 2026-10-09 (Marc: "a rough overdraft ... think about the structure ... what questions do I need to answer ... future work ... which [registry items] should we actually put into the appendix ... look at the structure of the appendix as a whole").

**Line numbers** are for `docs/thesis/dissertation.tex` at commit `0a61f2c6`: ch6 8431, registry 9508–9727, ch7 9732, AI Use Declaration 9833, appendices 9838 (A 9840, B 9872, C 10101, D 10369, E 10550).

**Standing rule:** every line inserted outside chapter 6 is proposed first (before/after) and applied only on Marc's yes. That covers ch7 and the appendices. §6 holds the proposals.

---

## 1. What an examiner expects of the conclusion

- **UWA has no separate Conclusion criterion** (CITS4001 marking guide; harvest `2026-10-07_ch6_discussion_assembly_harvests/D_examiner_benchmarks.md` §1). Ch7 is marked under *General* ("well-structured", consistent) and under *Discussion* items 1, 5 and 6: results tied to the introduction; improvements suggested; further work and loose ends named.
- **Evans, Gruba & Zobel 2014:** "summaries are not conclusions". Ch7 states answers and their consequence. It does not walk the chapters again.
- **Bunton 2005 (JEAP 4(3); planning source, not in references.bib), thesis conclusion moves:** restate the purpose; consolidate the findings as claims; give implications; recommend future research; close. These map onto preamble → contributions → future work.
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
