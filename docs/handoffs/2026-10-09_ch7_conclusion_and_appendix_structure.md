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
