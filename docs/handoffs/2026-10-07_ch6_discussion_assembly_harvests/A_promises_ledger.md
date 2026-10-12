# What chapters 1 to 5 owe the discussion: ledger

**Line numbering.** All line numbers are for `docs/thesis/dissertation.tex` at commit **9e69e1c2** (2026-10-07, "Chapter 1 and abstract: headline at 1 000 seeds…"). A parallel session committed that change to the abstract and chapter 1 while this harvest was running. It added 30 lines before chapter 2, so every line from chapter 2 on is 30 higher than in the brief's chapter map: ch2 587, ch3 956, ch4 3521, ch5 5543 (5.1 6003, 5.2 6460, 5.3 7172, 5.4 8042), ch6 8373 (6.1 8418, 6.2 8444, 6.3 8487, 6.4 8818, 6.5 8916), ch7 9034, appendices from 9117. Chapter 1 is quoted from the new commit. If the file moves again, check before citing a line number.

Tags: **PROSE** means the examiner sees it, so it is a hard obligation. **COMMENT** means a planning note, a soft obligation. **STALE** marks a comment that the current prose or a later ruling has overtaken.

---

## A. Research question, sub-questions, contributions, promises (chapter 1 prose, verbatim)

**Gap sentence (288–295):** "MTD has been proposed as a defence against APTs \citep{alshamrani2019}, yet it is rarely tested against one. Most tests run in simulation, against attacker models far simpler than an APT \citep{cho2020, jalowski2026}. None of the recent attacker models reviewed in Chapter~\ref{ch:litreview} fully captures an APT's adaptation to the defender. This gap motivates the research question of this dissertation:"

**Research question (354):** "*How does MTD perform against APT attackers?*"

**Sub-questions (356–366):** "The question breaks down into three sub-questions:
- SQ1 `\label{sq:capture}` (361–362): How can the behaviour of APT attackers be recovered from published threat reports?
- SQ2 `\label{sq:model}` (363–364): How can the recovered behaviour be executed as an APT attacker model inside an existing MTD simulator?
- SQ3 `\label{sq:evaluate}` (365–366): How does MTD perform against the APT attacker model compared with the simulator's baseline attacker?"

**Approach paragraph, P5 (396–412).** It defines CTI, the attack flows, the attack profiles, the baseline attacker and "perform". Key sentences:
- "Our source is 38 attack flows, graphs of an attack's steps that analysts drew by hand from CTI reports" (398–400).
- "The APT attacker model shares the attack actions of MTDSim's original scripted attacker, the baseline attacker, but its profile decides which attack action comes next, when, and what to do after one fails." (405–408)
- "Both attackers run on the same network. We first run both with no MTD, to test whether the APT attacker model behaves differently. We then run both under each of MTDSim's MTD mechanisms and deployment strategies at different deployment intervals. We measure MTD's performance by how much it holds back each attacker's progress through the network." (408–412)

**Headline, P6 (435–439), new at 1 000 seeds:** "With no MTD, the APT attacker model takes fewer attack actions per minute than the baseline attacker and makes less progress through the network. At every deployment interval, changing the network's addresses and layout holds back the APT attacker model most, and changing the network's software holds back the baseline attacker most."

**Contributions (523–536), rewritten 2026-10-07:**
- "We synthesise eight properties an attacker model needs to model an APT attacker, from the definition of an APT and two surveys of MTD." (526–527)
- "We build an APT attacker model that any study using MTDSim can run in place of the baseline attacker.[footnote: repo] The APT attacker model has four of the eight properties in full and two in part; three recent attacker models have at most one in full." (528–533). **Hard obligation:** `tab:fidelity-verdict` in section 6.3 must show this count (it does: properties 1–4 ticked, 6–7 partial).
- "We find that, in MTDSim, the MTD mechanism that holds back the attacker most depends on the attacker model." (534–535). **Hard obligation:** sections 6.2 and 6.4 must carry this, scoped to MTDSim.

**Chapter-map promises for chapters 6 and 7 (576–580):** "Chapter~\ref{ch:discussion} explains the results and their limits, checks which of the eight properties the APT attacker model has, and states what the results mean for MTD evaluation. Chapter~\ref{ch:conclusion} answers the research question and sets out future work." This promises four jobs for chapter 6: explain the results, state their limits (6.5), check the properties (6.3), state the implications (6.4). It also promises the conclusion's direct answer and its future work. The comment at 560–567 says to "Re-check ch6-7 clauses when drafted".

**Abstract promises (190–207):** "Changing the network's addresses and layout most reduces the share of the network the new model takes over. Changing the network's software most reduces the simplified attacker's share, but reduces the new model's far less. These results make a case for evaluating MTD against attacker models grounded in documented behaviour." (204–207). The "make a case" closer now lives only in the abstract (comment 432–434), so section 6.4 and the conclusion have to earn it.

**Chapter 1 comments that bind chapters 6 and 7 (COMMENT):**
- 329–333: the RQ is displayed "so the sentence the conclusion answers is findable at a glance". The conclusion answers it in the introduction's words.
- 340–350: the SQs use names, not pronouns, "so each SQ reads alone when quoted in ch5-ch7". Phase one (no MTD) "answers SQ2 as the check that the model behaves differently". There are no hypotheses.
- 418–421: the ceiling on headline claims: "never 'weak'/'realistic'/'inverts'; direction only, no ranks or numbers".
- 513–522: contributions third pass. "The attack-action bottleneck (ablation) is left to ch6-7: its cause is explanation, not measurement, and its terms are undefined here." The one metric of the dissertation's own (time lost per MTD deployment) is "support, not a contribution".
- 549–556: chapters 6–8 were undrafted when the overview was written, so it carries a stale-roadmap risk.

---

## B. Forward-reference ledger (chapters 1–5 and appendices, into chapters 6 and 7)

### B1. `\ref` to chapter 6 or 7 labels in PROSE (hard)

| Line | Label | Promise | Tag |
|---|---|---|---|
| 576–578 | `ch:discussion` | Explains the results and their limits, checks which of the eight properties the model has, states what the results mean for MTD evaluation. | PROSE |
| 579–580 | `ch:conclusion` | Answers the RQ and sets out future work. | PROSE |
| 3978 | `sec:threats` | "so the attack graph records attackers reported in CTI, not APT attackers alone." Section 6.5 must say the corpus is not limited to APT attackers: 18 of 38 attributed to an ATT&CK group, criminal groups among them; 20 name no group; one is adware (3973–3977). | PROSE |
| 5665–5666 | `ch:discussion` | (ch5 opener) "Chapter 6 reads the results against the eight properties and what they mean for MTD evaluation." Sections 6.3 and 6.4. The comment at 5644–5649 calls this "ch1's roadmap sentence for chapter 6, verbatim". Chapter 1 now words it differently ("explains the results and their limits…"), so the two no longer match. | PROSE |

No other `\ref` from chapters 1–5 or the appendices reaches `sec:disc-behaviour`, `sec:disc-mtd-performance`, `sec:fidelity-verdict`, `sec:evaluation-implications`, `sec:future-work` or `sec:contributions`. I grepped every label.

### B2. Implicit PROSE promises (no `\ref`, but the examiner will expect chapters 6 and 7 to close them)

| Line | Promise | Owed to |
|---|---|---|
| 3845–3847 (ch4 opener) | "It is a proof of concept: it tests whether an attacker that behaves like an APT changes what an MTD evaluation measures." The test needs a verdict. | 6.2, 6.4, conclusion |
| 3847 | "Detection avoidance and deployment-strategy awareness are left to future work." | `sec:future-work` |
| 3840–3845 | "built for four of the eight properties … objective-specific behaviour, choice of attack strategy, adaptivity and, in part, learning … keeps the baseline attacker's campaign persistence and, in part, its cost–benefit reasoning." Each claim has to be scored. | 6.3 / `tab:fidelity-verdict` |
| 4821–4822 | "These gaps set the ceiling of this dissertation: the APT attacker model can only be as good as the attack actions it adopts." This is the standing bound. The comment at 4569 says "the chapter 6 pointer follows", but no pointer is in the prose. | 6.3 (capture licence), 6.5 construct |
| 4946–4948 | "…so Chapter~\ref{ch:experiments}'s NCR rests most on this one value" (the 45 s mean duration). | 6.5 construct |
| 4174–4181, 5107–5109, 5201–5203 | Chapter 4 announces the three ablation results ("changes where the attacker goes after a failure, but not what it achieves"; the memory "raises the share of exploits that succeed … but leaves what the attacker achieves unchanged"). Chapter 5 states them, and chapter 6 owes the reason. | 6.3 |
| 5190–5192 | "we expect the memory to matter more when the diversity pool … is small." Chapter 5 answers yes on the share of exploits that succeed, no on NCR (8367–8371). | 6.3, property 7 |
| 5372–5373 | "MTDSim detects no attacker, so the two metrics for detection avoidance measure it by proxy". | 6.1(2), 6.5 construct |
| 2117–2121 (ch3) | "Migrating a service across diverse platforms … defends against persistent attacks but can weaken the defence against fast ones \citep{cho2020}. An APT attacker is persistent …, so a deployment strategy found against another attacker may not be optimal against it." The results put service diversity at rank 4 of 10 against the APT attacker model (0.36) and rank 1 against the baseline attacker (0.92). This runs against the diversity-favours-persistent half of Cho's example, so the discussion should address it. | 6.2(1) |
| 2187–2190 (ch3) | "ASP, MTTC and NCR are all computed from what the attacker does … MTD that is effective against one attacker may therefore not be effective against an APT attacker." The C5 ranking answers this. | 6.2 close, 6.4 |
| 2183–2185 (ch3) | "No standard set of metrics exists … so MTD mechanisms cannot be compared across evaluations \citep{jalowski2026}." | 6.4 |
| 2598–2601 (ch3) | "Simulation results do not transfer directly to a real network, which no simulation fully captures \citep{cho2020}." | 6.5 external |
| 1851–1858 (ch3) | "Attack profiling recovers the order of an attack's techniques, but not their timing … MTD must therefore decide when to move … without the attacker's timing." This sets up the judgement-set tactic durations and the deployment-interval sweep. | 6.2 (interval), 6.5 |
| 3478–3490 (ch3, research gap) | "How MTD performs against APT attackers therefore remains unmeasured. This dissertation … measures how MTD performs against the APT attacker model compared with the baseline attacker". Closing the gap is the conclusion's job. The 6.4 placeholder says it closes "the first half of the gap". | 6.4, conclusion |
| 7517 | `\owed{(Appendix~\ref{app:supplementary-results})}`: the worked first-deployment trace (Appendix, not chapter 6). It is in prose and in the "Owed before submission" list, so the build fails while it is open. | Appendix E, then read in 6.2(2) |
| 9671–9673 (App. D) | "Chapter 5 runs the random deployment strategy over the same four mechanisms beside MTDShield … the difference between the two is what the agent's policy adds." **Inconsistency:** chapter 5 reports no random-over-four arm. Comments at 7597–7598 and 7873 say it was "dropped from every float", and Table 5.1 lists random over all seven. Either restore it or drop the sentence. 6.2(4) needs it. | 6.2(4), or fix App. D |
| 9473–9475 (App. C) | "Moving one value at a time leaves interactions between the values untested, and the comparison with the baseline attacker was not repeated across the bands." | 6.5. **Conflict:** the 6.5 construct placeholder's residual "the orderings are what is claimed" (8966–8967) is not tested by App. C, which re-ran the APT attacker model alone. |
| 9388–9390 (App. C) | "Three values of our judgement are not tested: the per-tactic duration multipliers, the pre-intrusion overlay's share and the choice of one attack flow per APT group." | 6.5 |
| 9592–9600 (App. C.4) | Attack confidentiality's ordering holds at the six detector settings that flag ≥2.5 % of the baseline attacker's attack actions. At the other three the profiles lie within about one point of it. | 6.1(2), 6.5 |
| 9752–9776 (App. D, Known limitations) | MTDShield was run as released. Its scores came from runs at exploration rate 1. The evaluation code reads four inputs as zero. Its batch-norm variances are zero (output about 30-fold). It never learned the "do nothing" choice. **An unmapped tactic reads as "nothing detected".** It was trained at one interval, against the baseline attacker, on 100-host networks. | 6.2(4), 6.5 external |
| 9802–9805 (App. D) | With the training code's inputs, the agent stops in 435 of 500 runs against the APT attacker model, because it divides by port scans and the APT attacker model compromises without one. | 6.2(4) |
| 9829–9834 (App. E) | ASP reduction reaches its ceiling of 1 against the APT attacker model, whose ASP with no MTD is low, "so Chapter 5 ranks on NCR reduction." | 6.5 conclusion validity |

### B3. COMMENT obligations (soft), chapters 1–4

| Line | Phrase | Promise | Tag |
|---|---|---|---|
| 513–522 | "left to ch6-7" | The attack-action bottleneck: its cause is explanation. | COMMENT |
| 2602 (ch3 3.2.3) | "the limitation side is ch6's (sec:threats placeholder already lists 'the six adopted attack actions' and 'simulation only')" | 6.5 scope. | COMMENT |
| 2816 | "Property-matrix marks (Table 3.3 and its ch7 return)" | `tab:fidelity-verdict` reuses Table 3.3's glyphs. "ch7" here means today's ch6, after the 2026-09-08 renumbering. | COMMENT (old numbering) |
| 2821 | "the scoring discipline --- badges, pre-commitment, rows A/B --- opens sec:fidelity-verdict, NEVER here" | 6.3 opens with the scoring rule and states that the properties were fixed before scoring. | COMMENT |
| 2970–2980, 3023, 3183–3207 | "ch7's fidelity verdict is the badge summary on the eight properties"; "The ch7 copy adds the movement attacker's row"; "the fixed-before-scoring provenance (ch7's)" | Same as above: today's 6.3. | COMMENT (old numbering) |
| 3448–3450 | "weakest link KEPT … the discussion's use of the same phrase for the movement attacker's own action layer is the deliberate symmetry … the ch6 sentence should point back here" | **STALE:** "weakest link" is no longer in the chapter 3 prose (grep finds it nowhere outside comments). | COMMENT, STALE |
| 3551–3555 | "the scoring discipline (badge vocabulary; axes fixed before the model was scored) opens sec:fidelity-verdict" | 6.3 opener. | COMMENT |
| 3800–3815 | "(stealth's [reason] lives in §4.5 and ch6, scheme awareness's in ch7)"; "'Six of the eight' is design intent and holds whichever way stealth is scored in ch6"; "Stealth partial vs none: Marc's ruling, open" | 6.3 rules on property 5 (`tab:fidelity-verdict` currently shows none). Property 8 goes to future work. | COMMENT |
| 3834 | "persistence and incentive-driven rationality come with the baseline attacker's attack actions (Chapter 6 placeholder, verified in code: the exploit's RoA order, host.py:388) … eight, matching Table 6.x mark for mark" | The 6.3 properties 1 and 6 paragraph. | COMMENT |
| 3909 | "[CORPUS DISCLOSURE] … Points to ch6 threats (its placeholder carries the line). OPEN for Marc: the preamble and ch1 say 'recover the behaviour of APT attackers from CTI'; this sentence scopes it." | 6.5 external. The scoping tension with SQ1's wording is still open. | COMMENT |
| 4000–4003 | "if the term is wanted, L3 or ch6 coins it" (an observability boundary for the synthetic pre-intrusion structure) | Optional for 6.5. | COMMENT |
| 4569 | "the ceiling to 4.4.2 … (the chapter 6 pointer follows)" | No pointer exists in the prose (see B2). | COMMENT |
| 4624–4635 | Commented-out placeholder: "what a disruption does to the APT attacker model, explicit and emergent". The action in flight fails, the confusion penalty is charged and the host is lost (the same for both attackers). The token is not moved, later actions fail their preconditions, and the failure matrix routes. The baseline attacker restarts in a phase set by the layer. | 6.2(2) mechanism. Not landed in chapter 4. | COMMENT |
| 4661 | "routing-ablatability … guarantee stays repo-side (attacker_state_seam.md); ch6 cites it there." | Optional. | COMMENT |
| 4665–4668 | "ch7 has the future work" (changing the action layer) | `sec:future-work`: a richer set of attack actions. | COMMENT |
| 5353 | "(the chapter 6 placeholder)" renamed to distinct openings | Terminology only. | COMMENT |

### B4. COMMENT obligations (soft), chapter 5. "Chapter 6's" deferrals

| Line | Phrase | What is deferred | Tag |
|---|---|---|---|
| 5673–5678 | "the discussion interprets … the fidelity verdict EMERGES from the results and is read in the discussion (sec:fidelity-verdict, its table)" | 6.3 reads the verdict off the results and does not defend it from the design. | COMMENT |
| 5893–5907 | "WHAT THIS CHAPTER OWES ch6, section by section": app:sensitivity → sec:fidelity-verdict (honesty about the declared parameters: which parameter the conclusions are exposed to); sec:dimensions → sec:evaluation-implications (comparability boundary; "operating-point finding"); sec:effectiveness → sec:captured (properties 2 and 3 read off the no-defence arm) and sec:evaluation-implications (the argument that results depend on the attacker model); sec:efficiency → sec:captured (property 6); sec:supplementary → sec:captured (properties 1, 3, 4, 7) and the badge walk | Planning map. **Partly STALE:** `sec:captured` was retired, and the label map at 8397–8400 points it to `sec:disc-behaviour`/`sec:fidelity-verdict`. sec:efficiency and sec:supplementary no longer exist. | COMMENT |
| 5919–5922 | "OWED (Marc): one sentence where the 200 s suppression figure is reported, or in sec:fidelity-verdict, that its size is exposed to the low-and-slow dwell (44 to 89 per cent across the band against 75 at the chosen value…)" | 6.3 or 6.5: the magnitude of NCR reduction rests on the 45 s mean duration. Also the S33-e candidate at 7999–8006: random's reduction at 200 s runs 0.44 to 0.90 across the band. | COMMENT (old numbers) |
| 5980 | "VOLUNTEER THE CONCESSION": Jalowski's third guideline (compare against the state of the art); "which half of the attacker-realism demand the work answers … and which it does not (scheme-aware --- … future work)" | 6.4 / 6.5, future work. | COMMENT |
| 6230 | "§5.4.3 … re-runs the published claims, so the observation [that the dissertation's confidence intervals go beyond lineage practice] belongs there or in ch6" | Optional for 6.4. | COMMENT, partly STALE |
| 6265–6267 | "the adaptive selector is not exercised … pointing at future work" | **STALE:** MTDShield is now run. | COMMENT, STALE |
| 6270–6278 | "THE DEFENDER'S HALF OF THE MODEL IS UNDECLARED" (goal: disrupt, not detect; knowledge: none of the attacker; capability: seven mechanisms on a schedule) | 6.5 scope ("the defender held to its schedule"). | COMMENT |
| 6286–6334 | Coverage map: "on the field's own taxonomy this evaluation is strong on cost …, adequate on containment and delay, and silent on surface, payoff and service --- … a property of the simulator" | Optional for 6.5 or 6.4. Partly stale (efficiency section cut). | COMMENT |
| 6390, 6428 | "ch6's fidelity walk points at one section"; "this is the section ch6's sec:captured points at" (§5.2) | 6.1, 6.3. | COMMENT |
| 6443–6447 | Property map: "5 stealth -> absent, ruled; ch7"; "8 MTD-scheme awareness -> absent, ruled; ch7" | Future work. ("ch7" is still the conclusion here.) | COMMENT |
| 6457 | "the verdict they add up to is ch6's" | 6.3. | COMMENT |
| 6596–6639 | Axis-5 detectability contrast: "THE RULING OWED … IF THE RULING IS NO: it goes to ch7 as a named future-work condition" | Ruled since: attack rate and attack confidentiality are reported, and property 5 stays blank. | COMMENT, largely resolved |
| 6754 | "c_3 sits nearer impact than exfiltration … an observation, marked, not explained (chapter 6)" | 6.1(3). Old 100-seed divergence numbers. | COMMENT |
| 6755–6765 | "CEILINGS, for chapter 6": mean divergence rises as flow count falls (size confound); the size-matched label-blind control had not run (it has since: section 5.4 random partitions); profile divergence may not be read as objective conditioning changing an outcome | 6.1(3), 6.5 internal. | COMMENT, partly superseded |
| 6819–6820 | "WHY the gap is this size is not measured here and is chapter 6's" (the baseline attacker's outcome gap with no MTD) | 6.1(1). | COMMENT |
| 6829–6845 | "THE GAP IS READ AT THE 15 000 s TIME LIMIT AND DEPENDS ON IT. … at 60 000 s … target reached 0.58 … against the baseline attacker's 0.67"; the baseline attacker adds no host after about 20 000 s, while the APT attacker model is still climbing at 60 000 s | **Major for 6.1(1) and 6.5:** the outcome gap is a pace effect, and the time limit decides how large it looks. These are 100-seed provenance numbers, and 60 000 s is declared nowhere in the prose. | COMMENT |
| 6843–6845, 6859 | "DOUBLE EXTORTION [c_3] STALLS … the cause is chapter 6's"; "double extortion is an exception here and chapter 6's to discuss" | 6.1(3), "why c_3 stalls" (also in the 6.1 placeholder). | COMMENT |
| 6908–6909 | "'The MTTC of the APT attacker model rests on the tactic durations of Section 4.x' … the attribution is Chapter 6's." | 6.1(1). | COMMENT |
| 6932 | "M3: the concession to Section 6.5" | 6.5: counting unmapped steps as attack actions lowers attack confidentiality to the baseline attacker's level (handoff 2026-10-06 M3, ruling F13). This stands on an untracked dry run. Comment 6926–6929 gives 100-seed values (c1 0.77, c2 0.79, c3 0.83, c4 0.68; baseline 0.83), and App. C comment 9608–9610 gives "51–65 % against 50". | COMMENT |
| 7259 | "the cheapest form of the state-bounds argument the discussion carries": the shuffle–diversity–redundancy (SDR) classes do not span the effect the attacker feels (shuffle crosses both layers) | 6.2(1). | COMMENT |
| 7265 | "THE PURE-INTERRUPT PAIR … already noted in the discussion notes": IP shuffle and port shuffle reach the attacker by interrupt alone | Optional for 6.2(2). | COMMENT |
| 7358 | "now the fact alone, its mechanism to Appendix E and Chapter 6" (the first deployment's negative time lost) | 6.2(2). Handoff 2026-10-06 §8: the forced rescan gives the baseline attacker a second attempt at host 0. Intent spec IS-INT-01/05/07 classes this as `conforms`, and Marc's disposition of "sounds like a bug" is still owed. | COMMENT |
| 7373 | "[the verb-level activity mix null] is now one body sentence here and a limitation for chapter 6" (wrong resolution: the verb sits downstream of the mapping) | 6.5 construct. The body sentence is gone from the current prose. | COMMENT |
| 7440 | "Plain description only; the mechanism behind the numbers is chapter 6's (docs/implementation/disruption_mechanism.md section 1)" | 6.2(2). | COMMENT |
| 7525–7547 | "THE ANSWER IS MECHANISTIC": the APT attacker model depends on its position in the network, the baseline attacker on its exploits; "same action set" does not imply "same defence response" | 6.2(1), the core mechanism. Its numbers come from the pre-restoration substrate. | COMMENT |
| 7566–7571 | Timing distribution (exponential level): the baseline attacker's NCR reduction falls (port shuffle 0.90 → 0.14), and the APT attacker model's ordering holds | 6.5. Q8 ruling at 7996–7997: "Section 6.5 carries it (content point there)". | COMMENT |
| 7973 | "Why c_3 is Chapter 6's." (c_3 has the widest host-over-service margin) | 6.1(3)/6.2. | COMMENT |
| 7887 | "No chapter summary; no pointer to chapter 6 (the chapter ends on the last result)." | Rule: chapter 5 ends without a hand-off. | COMMENT |
| 8113–8122 | "His expectation (outcomes similar, because the profiles drive the simulator's existing attack actions) is chapter 6's, with the why." | 6.3, property 2. The 6.3 placeholder has it ("you can speak, but you can only say three words"). | COMMENT |
| 8147 | "what the random partitions keep and drop (why NCR moves, Chapter 6's…)" | 6.3, property 2. | COMMENT |
| 8206–8207, 8215 | "the interpretation, why the failure matrix changes little, is chapter 6's"; "why is chapter 6's" | 6.3, property 4. | COMMENT |
| 8262 | "§11.11 of the ch6 board: the memory operates … the OS check refuses about half of all exploit attempts, and removing it adds about two hosts" | 6.3, property 7 (affinity board handoff 2026-09-15). | COMMENT |
| 8275–8279 | "The why (a host needs two exploit visits; the failure verdict routes the token away and a later port scan reveals the next hop) is Chapter 6's … ch5 describes, ch6 explains." | 6.3, property 7. The handoff calls it "a hypothesis, to check before it is written". | COMMENT |

### B5. Appendix comments

No appendix comment points to chapter 6 or 7 by name. Two soft obligations matter for 6.5:
- App. C, exponential delay (9507–9547): the exponential is defended as "a tractable, precedented family, never a fidelity claim". Holm 2014 (Pareto fit) is counter-evidence. The Erlang-4 delay is worse for the attacker.
- App. C.4 (9603–9623): an owed detector sweep over τ, and the alarm-quantile sensitivity.

### B6. Off-tex record that maps chapter 5 findings to chapter 6 sections

`docs/handoffs/2026-10-06_ch5_results_prose_redraft.md` §1 assigns every chapter 5 finding to a 6.x slot. Findings marked "Headline": A4, B2, C1, C5, E1. §7 lists the content points moved to chapter 6:
- MTDShield overfitting to the baseline attacker (6.2(4), 6.4);
- random and alternative drawing three of seven from the host layer (6.2(4));
- "the model itself is more important than the profile" (6.1(3));
- the failure matrix as something the simulator already enforces (6.3);
- the memory, if a host takes about two exploits (6.3, a hypothesis);
- rankings tied to one simulator (6.4);
- the same-clock-time comparison caveat on time lost (6.5; handoff §8 point 5).

---

## C. Current findings (chapter 5 prose as it stands)

**Chapter 5 opener (5650–5666).** "This chapter answers \ref{sq:evaluate} by evaluating MTD in MTDSim against the APT attacker model and the baseline attacker. Both attackers are measured with the attacker behaviour, attack outcome and MTD effectiveness metrics…". Section 5.2 "compares the attacker behaviour and attack outcome of the two attackers with no MTD"; 5.3 "measures the MTD effectiveness of each MTD mechanism and deployment strategy against both attackers"; 5.4 "compares the APT attacker model with and without each of three components". The prose never uses the word "phase". The two phases are framed only by the 5.2/5.3 headings and by ch1 P5's "We first run both with no MTD … We then run both under each of MTDSim's MTD mechanisms…". The 6.x placeholder at 8413 uses "the two phases of Chapter 5", which has no prose antecedent.

**5.1 setup facts that bound interpretation (6038–6165):**
- Four deployment strategies; single runs once per each of the seven mechanisms; MTDShield runs as released.
- Six deployment intervals: 50, 100, 200 s (the earlier studies) and 500, 1 000, 2 000 s ("up to ten times their longest").
- Targeted attack scenario, default 50-host network, **two target hosts in place of five** (from Tay's code).
- End of run: a target compromised, or 15 000 s (from Ho; Table 5.1).
- 1 000 seeds, the same networks for every configuration.
- Statistics: Clopper–Pearson for ASP; normal approximation for means; percentile bootstrap otherwise; Cohen's d, negligible within ±0.2; Scott–Knott ESD ranking; Spearman's ρ.
- Ablation verdict by interval: negligible / not negligible / inconclusive (Lakens).
- "The tactic durations cannot be removed, so Appendix~\ref{app:sensitivity} varies their values instead." (6164)

**5.2 APT attacker model versus baseline attacker, no MTD (`fig:aio-coverage`, `tab:unopposed-summary`):**
1. *Objective-specific behaviour* (6683–6690). The baseline attacker takes only its six attack actions. Every attack profile spends **26 to 47 %** of its steps in unmapped tactics, which dispatch no attack action. These include collection, exfiltration and impact. The profiles divide their steps differently (Fig. 5.1(a)).
2. *Choice of attack strategy* (6701–6709). The baseline attacker's runs share one opening over their first **four** steps. All but **two** of its 1 000 runs then branch once (brute force or scan neighbours). The profiles part ways from the **second** step (c1) to the **fourth** (c3), with **179 to 947** distinct openings over eight steps (Fig. 5.1(b)).
3. *Attack outcome* (6902–6907; Table 5.2). The baseline attacker's ASP is **5 to 16 times** a profile's (0.66 against 0.04–0.14) and its NCR **2.4 to 3.3 times** (0.497 against 0.149–0.209). Its MTTC, **9 100 s**, "is just shorter than" the profiles' **9 700 to 11 300 s** (c3's 9 700 ± 900 interval overlaps 9 100 ± 200).
4. *Detection avoidance* (6937–6944; Table 5.2). Attack rate is **1.709** per minute for the baseline attacker against **0.680 to 1.228**. Attack confidentiality is **82.2 %** against **89.4 to 98.1 %**. "Across the four attack profiles and the baseline attacker, attack confidentiality falls as attack rate rises."

Where the prose stops short: no "why" for the outcome gap, the pace, c3's stall, or the confidentiality/rate relation. Only the by-construction fact that unmapped tactics dispatch no attack action is given.

**5.3 APT attacker model versus MTD (7208–7209):** "compares the two attackers with each MTD mechanism and deployment strategy running."

**5.3.1 Disruption per MTD deployment** (single strategy at 2 000 s, because the next deployment caps time lost; `fig:aio-adaptivity`, `tab:disruption` in App. E):
1. Attack actions blocked per MTD deployment (7494–7502). Host layer: **1** for the baseline attacker against **0.35–0.39**. Service layer: **0.95 against 0.15**. User shuffle: **0.07 against 0.01**. The by-construction reason is given: the APT attacker model runs no attack action in an unmapped tactic.
2. *Adaptivity*, time lost (7504–7510). The APT attacker model loses **242–324 s** per host-layer deployment and the baseline attacker none, "though every host-layer deployment blocks its attack action". The baseline attacker loses **493 s** per service-diversity deployment, the APT attacker model **60 s**. Under every other mechanism the APT attacker model loses **26 s or less**.
3. Negative time lost (7514–7520). The baseline attacker's time lost is below zero under every mechanism but service diversity. The first deployment brings its first compromise **204–232 s** forward (`\owed` App. E item).

Where the prose stops short: no mechanism for the layer split, for "blocked but no time lost", or for the negative values.

**5.3.2 MTD ranking against each attacker** (200 s; `tab:eff-cross-arm`, `fig:eff-cross-arm`, App. `tab:eff-interval-values`):
1. (7722–7728) "No MTD mechanism or deployment strategy ranks first against both attackers at the default deployment interval, 200 s." Rank 1 against the APT attacker model: IP shuffle (0.96), host topology shuffle (0.95), complete topology shuffle (0.95). Rank 1 against the baseline attacker: service diversity (0.92), port shuffle (0.91). **ρ = 0.01 [−0.19, 0.05]** at 200 s, between **−0.24 and 0.25** at every interval.
2. (7749–7758) The host-layer mechanisms reduce the APT attacker model's NCR more than the service-layer mechanisms at every interval, and the reverse holds for the baseline attacker. Up to 200 s: host ≥ **0.96** for the APT attacker model; service ≥ **0.84** for the baseline attacker. The APT attacker model's host-layer reduction stays above 0.5 up to **1 000 s**, the baseline attacker's service-layer reduction only up to 200 s. **User shuffle reduces the APT attacker model's NCR below zero at every interval** (marked, not explained).
3. (7760–7766) Random and alternative reduce the APT attacker model's NCR more at every interval. MTDShield reduces the baseline attacker's more, at every interval up to **1 000 s**. At 200 s MTDShield chooses service diversity in **70 % or more** of its decisions against either attacker (App. D.5: 76 % baseline, 70 % APT).

Where the prose stops short: why the order of the layers reverses, why user shuffle helps the APT attacker model, and why MTDShield favours service diversity (training against the baseline attacker is a 6.2(4) hypothesis).

**5.3.3 MTD effectiveness by attack profile** (`fig:eff-suppression-profiles`):
1. (7957–7967) At 50–200 s the four profiles' NCR reductions differ from one another less than the baseline attacker's differs from the nearest profile's, under every mechanism and strategy. At 200 s the profiles lie within **0.14** of one another, and the baseline attacker **0.24 or more** from the nearest, except under user shuffle. Under the deployment strategies the baseline attacker lies outside the profiles' range up to **1 000 s**.
2. (7980–7986) c3 is furthest from the baseline attacker at **500 and 1 000 s** under the host layer and service diversity. Under the host layer the baseline attacker is below all four and c3 highest. Under service diversity the baseline attacker is above all four and c3 lowest.

Where the prose stops short: why c3 differs ("Why c_3 is Chapter 6's", comment 7973).

**5.4 Ablation studies** (`tab:ablation`; App. `tab:ablation-attack-profiles`, `tab:ablation-random-partitions`, `tab:ablation-memory`, `fig:ablation-memory`):
1. *Attack profiles by objective* (8151–8158). Without them the model runs on the attack graph and "compromises more without them, by an effect on NCR that is not negligible". No MTD: NCR **0.171 with, 0.189 without, d = −0.28**. Over the 60 MTD configurations: not negligible in **29**, negligible in **7**, inconclusive in **24**.
2. *Random partitions* (8186–8196). With no MTD the model "compromises more with the attack profiles than with any of the ten, by an effect on NCR that is not negligible, a d of **0.25 to 1.47**". Under IP shuffle and OS diversity, not negligible against **six to ten of the ten** in each configuration. (Re-read 2026-10-07 after the redraw.)
3. *Failure matrix* (8242–8249). It "changes where the APT attacker model goes after a failure, and its effect on NCR is negligible". After a failed initial access the model returns to reconnaissance in **0.76–0.83** of cases (c1, c3, c4) with it and **0.08–0.10** without. (Table 5.4 d: +0.07, +0.13, +0.12, −0.01, +0.06.)
4. *Vulnerability memory* (8347–8353, 8367–8371). It "raises the share of exploits that succeed, and its effect on NCR is negligible". Share **0.73 with, 0.69 without**. With one service per operating system, **0.92 against 0.69**, "and its effect on NCR is still negligible".

Where the prose stops short: every "why" (handoff E1 headline: of the three components that rest on judgement, only the partition changes a result).

---

## D. Chapter 4 concessions and design bounds (prose)

| Line | Item | Paraphrase |
|---|---|---|
| 3840–3847 | Scope | Built for four properties (2, 3, 4, and 7 in part), keeps 1 and 6 (part) from the baseline attacker's attack actions, leaves 5 and 8 to future work. "A proof of concept". |
| 3922–3931 | Tactics as nodes | A technique stands for its leftmost tactic. Steps within a tactic are not edges: they become tactic duration. |
| 3966–3978 | Corpus of 38 attack flows | Mining alternatives recovered 10 % and 14 % of tactic edges against 50 %. **18 of 38 attributed to an ATT&CK group (criminal groups among them), 20 to none, one adware**. All 38 kept, "so the attack graph records attackers reported in CTI, not APT attackers alone" (→ `sec:threats`). |
| 3980–3988 | Resolution traded | 88 % of technique edges come from one flow against 39 % of tactic edges. The mapping covers 15 tactics, not 124 techniques. |
| 3990–3997 | Sparse before intrusion | Reconnaissance appears in 10 of 38 flows, "any CTI corpus shares the gap". The pre-intrusion overlay is added to fill it. |
| 4078–4106 | Objective classification | Two yes/no questions give c1–c4 (19/7/7/5). c3 is mostly ransomware. c4 "did neither, whatever the reason": three attackers removed before they acted, one positioning, one adware. |
| 4126–4134 | Classification sources | From the CTID description, the ATT&CK group page or the cited report. Three flows were decided by the author (App. B). Answers were not read off the flows: only 10 of 19 c1 flows reach exfiltration. |
| 4165–4172 | Profiles share their core tactics | Execution, stealth, discovery and C2 appear in more than half the flows of every profile. The profiles differ in actions on objectives. |
| 4296–4299 | Base weights | One attack flow per APT group (the longest). "They rest on 29 of the 38 attack flows." |
| 4300–4302 | Single token | One line of the campaign at a time. Parallel branches collapse. |
| 4305–4314 | Pre-intrusion overlay | Three declared transitions for c3 and c4 that no flow draws. The one-tenth share is declared (and untested, App. C). |
| 4324–4330 | Verdict | The base weights describe where an attacker goes after success only. A GSPN cannot route on the verdict, hence the failure matrix extension. |
| 4351–4353 | Disruption | A deployment cuts a timed transition short. An action in flight fails. |
| 4557–4559 | Failure causes | Missing preconditions or an MTD disruption. One verdict covers both. |
| 4583–4590 | Inputs not from the corpus | The mapping, the durations and the failure matrix are declared "from MTDSim's constants where they exist and otherwise from the literature or our judgement". The memory extends the exploit. |
| 4781–4797 | Tactic-to-action mapping | Declared from ATT&CK. Lateral movement → enumerate host and C2 → scan neighbours are the author's choice ("we chose"). |
| 4814–4822 | **Unmapped tactics and the ceiling** | Seven unmapped: collection, exfiltration, impact (nothing to act on), stealth (nothing watches), defense impairment (cannot see or change the schedule), persistence (a host stays compromised), resource development (off-network). "These gaps set the ceiling … can only be as good as the attack actions it adopts." |
| 4828–4830 | Unmapped tactics cannot fail | A deployment cuts the duration and charges the penalty but "never changes which tactic comes next". |
| 4852–4867 | Tactic durations | Exponential delay. One mean per tactic. Six from MTDSim, nine by judgement. |
| 4903–4922 | Durations set by judgement | Kept on the baseline attacker's scale and under the 200 s default interval. 45 s for persistence, stealth, C2; 36 s for collection, exfiltration, impact; 22.5 s for execution and defense impairment; 0 s for resource development. |
| 4939–4948 | Sensitivity | Halving or doubling each mean duration: "Only the 45 s changes NCR much", most likely through C2 → scan neighbours. "Chapter 5's NCR rests most on this one value." |
| 5004–5012 | Failure matrix not in the corpus | Reports describe incidents "that succeeded and were worth writing about". |
| 5063–5087 | Failure matrix values | Three assumptions (no foothold → back to preparation, citing Hutchins; foothold → same stage; seldom skip a stage), nine rules plus a distance factor, 210 factors, "their values are our judgement". |
| 5099–5109 | Adaptivity claim and its limits | Reads only the verdict, so an MTD failure routes like any other. It can only reweight edges the flows give: in c2 a failed initial access still goes on into the network. Dead ends retrace. The ablation preview says "changes where … not what it achieves". |
| 5174–5192 | Vulnerability memory | The tactic duration replaces the exploit time, so the baseline attacker's halving saves no time. The memory "triples the attacker's odds" (factor of three is judgement), lasts the whole run, and gives "learning … in part: it learns about vulnerabilities, not about the MTD deployments it observes". It is expected to matter more with a small diversity pool. |
| 5241–5249 | Metrics frame | No adopted metric measures behaviour. Metrics are added for properties 2, 3 and 5. Time lost per MTD deployment covers property 4. |
| 5321–5329 | Counting rules | An action that fails on missing preconditions "never reaches the network" and does not count. The baseline attacker's exploit counts once per host. |
| 5372–5402 | Detection by proxy | "MTDSim detects no attacker". Attack confidentiality uses Snort's default port-scan rule (5 in 60 s) as a stand-in detector. |
| 5483–5485, 5525–5539 | Pairing | NCR reduction and time lost compare runs on the same seeds. Time lost is capped at the next deployment and compares the same clock moment (the source of the same-clock caveat). |
| App. B.7, 9328–9334 | Total mapping | Out of the fixed order most actions are refused: 0.15 hosts against 8.13 hosts (NCR 0.003 against 0.163). This backs the partial mapping. |
| App. C, 9388–9390 | Untested values | Per-tactic multipliers, the overlay share, one flow per APT group. |
| App. C, 9473–9475 | One factor at a time | Interactions untested. **The baseline attacker comparison was not repeated across the bands.** |
| App. C, tab:parameter-register | Results | The 45 s band moves NCR 0.267 / 0.163 / 0.059 (no MTD). The 35 s and 36 s bands move it a little. 4.5 s is inert. γ, δ are inert. Erlang-4 lowers NCR by ≤ 0.005 under MTD. |

---

## E. Chapter 2 and 3 set-ups the discussion should close

**Research gap, 3.4 (`subsec:research-gap`, 3409; prose 3478–3490), verbatim:** "An MTD evaluation's result depends on its attacker model: the attacker model decides which deployment strategy is optimal (Section~\ref{subsec:defence-modelling-approaches}) and how effective MTD is (Section~\ref{subsec:mtd-metrics}). Two surveys find that MTD attacker models lack properties of an APT attacker \citep{cho2020, jalowski2026}, and the three recent MTD attacker models scored in Section~\ref{subsec:recent-threat-models} still lack them. How MTD performs against APT attackers therefore remains unmeasured. This dissertation recovers the behaviour of APT attackers from CTI by attack profiling (Section~\ref{subsec:profiling}) and executes it as an APT attacker model inside MTDSim (Chapter~\ref{ch:attacker-model}). It then measures how MTD performs against the APT attacker model compared with the baseline attacker (Chapter~\ref{ch:experiments})."

**The eight properties (`tab:attacker-properties`, 2981–3009; numbers never renumbered):**
1. Campaign persistence
2. Objective-specific behaviour
3. Choice of attack strategy
4. Adaptivity
5. Detection avoidance
6. Cost–benefit reasoning
7. Learning
8. Deployment-strategy awareness

Definitions are at 2998–3006. Sources: properties 1, 2, 4, 5 come from the APT definition (NIST, Alshamrani); 3, 6, 7, 8 come from the surveys (2880–2884).

**Scoring rule (3159–3166).** Met = "does all that the property's definition … says". Stand-in = does part, "or its authors set the behaviour by a fixed rule … or assume it". None = neither. Section 6.3 must apply the same rule to the APT attacker model; the placeholder at 8961–8965 says so.

**Scores (`tab:attacker-cross-section`, 3275–3296)** and the **Finding (3391–3395):** "only the baseline attacker has one in full, campaign persistence. Detection avoidance, learning and deployment-strategy awareness are the rarest … The attacker models of Masud et al. and Kim et al., which this dissertation expected to be the most likely to have the properties, have none in full." Chapter 1 contribution 2 sets "at most one in full" against the APT attacker model's four.

**Baseline attacker scoring (3309–3320) that 6.3 inherits:** persistence full ("carries on through every disruption"); objective in part ("no attack action for exfiltration or impediment"); strategy in part (a fixed rule orders credentials, exploit, brute force); adaptivity in part ("a fixed rule sets its response to each kind of disruption, such as always re-scanning after a host-layer disruption"); cost–benefit in part (RoA ordering of exploits only); learning in part ("learns about vulnerabilities, not about the MTD deployments it observes"); none for 5 and 8.

**Tensions and expectations in chapters 2 and 3 that the results speak to:**
- *Cho via Jalowski: the survey critiques (2889–2901).* Attackers "follow fixed attack patterns while the defender adapts and learns"; "the most glaring flaw in the MTD literature" (Jalowski p. 8); an APT attacker "learns the MTD's deployment patterns … looks for the logic of the deployment strategy"; "MTD is typically tested against active scanning, such as Nmap, while an APT attacker uses passive reconnaissance". The results speak to the first (the baseline attacker's fixed openings against the model's 179–947) and to stealth (attack rate and attack confidentiality by proxy), and leave property 8 open.
- *Which deployment strategy is optimal depends on the attacker (2094–2121).* "The attacker model therefore decides which deployment strategy is optimal." "MTDShield's [attacker] is the baseline attacker" (2109–2110). These set up C5 and 6.2(4) MTDShield.
- *Cho's diversity example (2117–2121).* Cho says diversity defends against persistent attacks. The results show service diversity is weak against the persistent APT attacker model. This tension is unaddressed in the placeholders.
- *Attacker-dependent outcome metrics (2187–2190)* and *no standard metric set (2183–2185, Jalowski)*. These feed 6.4. ASP is "the dominant effectiveness metric" (2180), and the dissertation ranks on NCR reduction because ASP reduction saturates (App. E 9829–9834).
- *Simulation transfer (2598–2601)* and *flexibility used (2599–2601)* feed 6.5 external.
- *Low and slow (1150–1152).* Espionage goes undetected for a median of 122 days, against 14. This sets up the quieter, slower finding.
- *Objective-dependent stages (1196–1210).* Preparation and intrusion are the same for every APT attacker; post-intrusion and actions on objectives depend on the objective; positioning stays post-intrusion. This sets up property 2, and the limit that unmapped actions on objectives cannot differ in MTDSim.
- *Manual profiling covers only drawn incidents (1617–1618)*; *automated profiling is unreliable (1611–1616)*. These feed 6.5 external.
- *Timing not recovered (1851–1858).* This sets up the judgement durations and the interval sweep.
- *Lineage configurations (`tab:lineage-configurations`, Table 2.2, at 939).* Brown: interval uniform 1–5 s, 200 hosts. Zhang: exponential 50–200 s, 100 runs, ends at 80 % NCR. Ho: 150 hosts, 15 000 s time limit. Runs are mostly unstated. This feeds the comparability point in 6.4/6.5 ("no numeric comparison with the lineage papers", 8972–8973).
- *Disruption mechanics (2.2.3, 919–928).* Host layer → back to scan host; service layer → back to scan port; user shuffle → brute force to exploit; about 20 s confusion penalty; "A deployment never takes back a compromised host or a stolen credential; the attacker loses only its place". This is the basis of 6.2(2). The retry rule (901–904: if all three attacks fail it moves to the next host; when the list runs out it re-scans, including hosts already tried; gives up after ten attempts, never on a target) is the antecedent for the first-deployment negative time lost.
- *Exposed endpoints never change (718–721)*: "no MTD mechanism changes them, although a topology shuffle can change their links". This bears on the first-deployment effect.
- *Near-periodic interval (793–795)*: 200 s plus a delay of 0.5 s on average. This feeds the Q8 timing-distribution item in 6.5.
- **Antecedent gaps for the 6.2 placeholder.** "the lineage's own disagreement (Zhang favours shuffle, Ho diversity)" (8476–8477) and Brown's "simply needs to reconnect" (8478–8479) have **no antecedent anywhere in chapters 2–3 prose** (grep: no "favour", "reconnect", or Zhang/Ho result statement). Either introduce them in chapter 2 or 3, or cite them fresh in chapter 6.

---

## F. Terminology fixed in the prose (definition line)

**Attackers**
- **APT attacker model**: ch1 405 ("as the APT attacker model"). The full term is used everywhere. The abstract alone says "the new model" (201–206).
- **Baseline attacker**: ch1 406 ("MTDSim's original scripted attacker, the baseline attacker"); ch2 851. The abstract alone says "simplified attacker". "Movement attacker" is a repo and comment name only, never prose.
- **Attack profile**: generic, ch3 1606 (the product of attack profiling). The four are **$c_1$ to $c_4$**, ch4 4089, Table 4.1 (4108–4124). The house form for pooling is "**averaged over $c_1$ to $c_4$**" (captions; the 2026-10-06 ruling). "The attack graph" (ch4 3922) is what the attack-profile ablation runs on. `c_agg` is no longer a prose term.
- **APT / APT attacker**: ch1 246–248; ch3 1143–1154 (advanced / persistent / low and slow / threat).

**MTD**
- **MTD**: ch1 269; ch2 623–626 (what/how/when to move). SDR: **shuffling / diversity / redundancy** (632–637). Triggers **proactive / reactive / hybrid** (639–642).
- **MTD mechanism** (seven), ch2 745–749, Table 2.1 (`tab:defence-mechanisms`, 751–780). Groups are **host layer** (IP shuffle, complete topology shuffle, host topology shuffle), **service layer** (OS diversity, service diversity, port shuffle) and **credentials** (user shuffle). The prose calls the third "the users' credentials" or "credentials", not a layer (747). Chapter 5 says "host-layer mechanisms" and "service-layer mechanisms". Layers defined at 704/706.
- **Deployment**: 748 ("one run of one mechanism", 20–110 s).
- **Deployment strategy**: 782; Table 2.2 `tab:deployment-strategies` (800–817). The four are **random**, **alternative**, **single** (proactive) and **MTDShield** (hybrid; "a reinforcement-learning agent", 785–791). "No deployment strategy is reactive" (791). Lower-case strategy names. "Execution scheme" is retired.
- **Deployment interval**: 793 (200 s default, near-periodic).
- **No MTD**: the reference condition (house form "with no MTD").

**Model parts (chapter 4)**
- **Attack action**: ch2 852 (the six: scan host, enumerate host, scan port, exploit, brute force, scan neighbours). The full term is used everywhere, never "phase".
- **Tactic** / technique / procedure: ch3 1376–1378 ("A tactic is what an attacker does to achieve a goal, a technique is how it does it"). There are 15 tactics in ATT&CK v19.1.
- **Attack flow**: ch3 1623. **Attack graph**: ch4 3922.
- **Lifecycle stages** (four): preparation, intrusion, post-intrusion operations, actions on objectives (ch3 1196–1198). **Foothold** is used from 1201.
- **Petri net**: first used ch4 3843. Formalised as a **GSPN** (4245; tuple 4262). **Timed / immediate transition** (4256–4258); **rate**; **base weight** (4290); **token** (4249); **decision place**; **pre-intrusion overlay** (4307); **verdict** (4325); extended tuple with **failure matrix F** (4332–4340). "Petri net" is not a chapter 1 term.
- **Loop** (six steps, `fig:runtime-loop`): 4532–4552. "Runtime loop" is the figure name; "join" is retired.
- **Tactic-to-action mapping**: 4781. **Unmapped tactic** (seven): 4814.
- **Tactic durations** / **mean duration $\mu_p$**: 4852 / 4860. Use the full terms, not "dwell times" (a repo word).
- **Failure matrix**: 5004 (nine rules plus the **distance factor**, 5075–5080). **Dead end**: 5106.
- **Vulnerability memory**: 5174. **Diversity pool**: 5191.

**Metrics (`tab:metrics`, Table 4.3, at 5256; ten metrics in three groups, defined 5321–5539)**
- *Attacker behaviour* (built on **step**, 5321, and **attack action**): **relative tactic occurrence** (5331), **distinct openings** (5356; **opening** = first $k$ steps, 5358; "attack path" keeps its chapter 3 meaning), **attack rate** (5372), **attack confidentiality** (5384).
- *Attack outcome*: **attack success probability (ASP)** (5434; acronym defined ch3 2179), **network compromise ratio (NCR)** (5442), **mean time to compromise (MTTC)** (5451).
- *MTD effectiveness*: **NCR reduction** (5489), **attack actions blocked per MTD deployment** (5513), **time lost per MTD deployment** (5525; **wait**, 5527). "The metric for adaptivity" (5526).
- **ASP reduction** is defined only in App. E (9822–9828), not in Table 4.3.
- **Return on attack (RoA)**: ch2 891. **Confusion penalty**: ch2 925. **Disrupt** (not "interrupt") and **block**: ch2 919ff and 4.5.3.

**Setup and statistics (chapter 5)**
- **Seed**/**run** (6081–6085).
- **Cohen's d**, **negligible / not negligible / inconclusive** (6119–6120, 6157–6160).
- **Scott–Knott effect size difference test**, **rank** (6120–6123).
- **Spearman's ρ** (6124).
- **Ablation study** (heading 5.4). "The ablated model" is retired (comment 8076–8080).
- **Phases**: not a prose term (see C).

---

## G. Inconsistencies and stale items found while harvesting (for whoever drafts chapter 6)

1. The ch5 opener's chapter 6 sentence (5665–5666) no longer matches chapter 1's new wording (576–578), though its comment says it is verbatim.
2. App. D (9671–9673) promises a random-over-four arm beside MTDShield that chapter 5 does not report.
3. The 6.5 placeholder's "Spearman's $\rho$ without an interval" (8979) is stale: chapter 5 now gives ρ = 0.01 [−0.19, 0.05] (7726–7727). The same placeholder points "negligible below d = 0.2" to `sec:evaluation-metrics`, but it is defined in 5.1 (6119–6120, 6157–6160).
4. The 6.5 construct residual "the orderings are what is claimed" (8966–8967) is not backed by App. C, which did not repeat the baseline attacker comparison across the bands (9474–9475).
5. The 6.2 placeholder relies on "Zhang favours shuffle, Ho diversity" and Brown's "simply needs to reconnect", neither introduced in chapters 2–3.
6. Chapter 3's Cho example (2117–2121: diversity defends against persistent attacks) runs against C1 and is not yet picked up in any placeholder.
7. The time-limit dependence of the no-MTD outcome gap (comments 6829–6845: at 60 000 s target reached 0.58 against 0.67; old 100-seed numbers) is not in the 6.5 placeholder. It belongs in 6.1(1) or 6.5.
8. The 6.1 opener placeholder (8413) says "two phases", which chapter 5 prose never names.
9. Old ch3 and ch5 comments say "ch7" for the fidelity verdict (pre-2026-09-08 numbering, now 6.3) and use `sec:captured` (retired). The label map is at 8397–8400.
10. Comment 3448–3450 ("weakest link" symmetry) is stale. The phrase is no longer in chapter 3 prose.
