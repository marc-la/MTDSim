---
status: open — structure ruled (§8); point sets in the ch6 placeholders for Marc's read; next: Marc triages 6.4 and marks points in or out, then slot-form dot points per paragraph
created: 2026-10-07
updated: 2026-10-07
topic: "Chapter 6 (Discussion) assembly: every discussion idea on disk, in the session logs and in Marc's dictation, in one place, vetted against the current chapter 4–5 prose, arranged by section and by importance, with the contradictions to fix and the questions only Marc can answer"
supersedes: "2026-09-15_ch6_discussion_affinity_board.md for CONTENT (its §10–§11 structure research and rulings stand and are summarised in §1 and §3 below)"
---

# Chapter 6 assembly: one place for the discussion

**Goal.** One vetted inventory of what chapter 6 says, so that the chapter can be arranged and written once. Pipeline: **inventory (this file) → Marc answers §7 → structure fixed → dot points per paragraph → Marc dictates → repair → compress → voice pass.**

**Line numbers** are for `docs/thesis/dissertation.tex` at commit `9e69e1c2` (ch2 587, ch3 956, ch4 3521, ch5 5543, ch6 8373, ch7 9034, appendices 9117). Re-check before quoting: parallel sessions edit the file.

**Raw harvests** are kept alongside in [`2026-10-07_ch6_discussion_assembly_harvests/`](2026-10-07_ch6_discussion_assembly_harvests/) and cited below by ID:
- **A**: what ch1–5 promise ch6, ch5 findings as stated in prose, and the terminology.
- **B**: about 150 repo ideas (R-IDs), each marked live, stale or ruled.
- **C**: 96 of Marc's own ideas (M-IDs) from all 869 unique session messages, with quotes. **Kept out of the repo (it is public; the file quotes private supervisor exchanges)**: `~/mtdsim-meeting-minutes/2026-10-07_ch6_session_ideas_harvest.md`.
- **D**: examiner benchmarks, including the UWA marking guide verbatim.

Status key: **LIVE** (current prose supports it) · **CHECK** (needs a re-read on the 1 000-seed corpus, or a trace) · **RULED** (Marc ruled; date given) · **HYP** (an explanation, to be stated as one).

---

## 1. What the examiner checks

The UWA CSSE *Dissertation Marking Guide* ("Discussion" criterion, D §1) asks six questions:

1. Are the results related to what the introduction set up?
2. Are **all** the results taken into account?
3. Are the conclusions justified, or over-stated?
4. Are shortcomings recognised?
5. Are improvements suggested?
6. Are further work and **loose ends** named?

Questions 5 and 6 are marked under *Discussion*, not under the conclusion. So every shortcoming in 6.5 points visibly forward to §7.2.

The benchmarks that decide this chapter (D §2–§3):
- **Interpret, never replay.** State each result in words with a `\ref`. Give only the numbers the interpretation turns on.
- **Mechanism, then the rival explanation.** Name the cause, then say why the alternative is set aside, or label the cause a hypothesis.
- **Compare with the literature met in ch3.** The comparison is qualitative, never numeric across papers.
- **Bound every implication by 6.5** (the ACM anti-pattern is implications written as though the limitations do not exist).
- **Threats specific to this study, typed, each with mitigation and residual.** Never mitigated by future work alone.
- **Easy to navigate.** A roadmap opener, a claim as each section's first sentence, one term per thing, no headings below the section.
- **One concrete instance where a mechanism is abstract** (French's examples point): a named run or deployment in prose, never a new results float.

Failure modes:
- replaying ch5;
- new results in ch6;
- over-claiming ("fidelity causes X");
- running down the baseline attacker or the lineage;
- a laundry list of limitations;
- implications that ignore 6.5;
- repeating the conclusion.

---

## 2. Hard obligations (examiner-visible prose that ch6/ch7 must cash)

From A §A–§B2:

- **ch1 contribution 2** (528–533): "four of the eight properties in full and two in part; three recent attacker models have at most one in full". Shown in 6.3 / Table 6.1.
- **ch1 contribution 3** (534–535): "in MTDSim, the MTD mechanism that holds back the attacker most depends on the attacker model". Carried by 6.2, generalised (bounded) in 6.4.
- **ch1 chapter map** (576–580): ch6 "explains the results and their limits, checks which of the eight properties …, and states what the results mean for MTD evaluation". These are the four jobs; the opener says them in this order.
- **Abstract** (204–207): "These results make a case for evaluating MTD against attacker models grounded in documented behaviour." 6.4 must earn this sentence.
- **ch4 opener** (3845–3847): "a proof of concept: it tests whether an attacker that behaves like an APT changes what an MTD evaluation measures." The test needs a verdict (6.2 close, 6.4).
- **ch4 ceiling** (4821–4822): "can only be as good as the attack actions it adopts". 6.3 close and 6.5 lead.
- **ch4 4946–4948**: "Chapter 5's NCR rests most on this one value" (the 45 s mean duration). 6.5 construct.
- **ch4 3978 → `sec:threats`**: the corpus is not APT-only. 6.5 external.
- **ch4 5190–5192**: the memory "expected to matter more when the diversity pool is small". Answered in ch5; 6.3 reads why.
- **ch3 2117–2121 (Cho)**: diversity "defends against persistent attacks". The results run against this. 6.2 must engage it (see 6.2-P1).
- **ch3 2187–2190**: "MTD that is effective against one attacker may therefore not be effective against an APT attacker". Answered in 6.2 and 6.4.
- **ch3 2598–2601**: simulation results do not transfer to a real network. 6.5 external.
- **Every ch5 float is read somewhere in ch6.** This includes §5.4's four ablation results, the negative time lost (ch5 7514–7520; the appendix `\owed`) and user shuffle below zero.
- **ch5 opener** (5665–5666) says ch6 "reads the results against the eight properties and what they mean". It no longer matches ch1's new wording: re-sync one of the two.

---

## 3. Structure (proposed; Marc rules in §7 Q1–Q3)

**The answer to "where do the ablations go":** in 6.3. The ablations test the three components that rest on judgement, and each one backs a property: the attack profiles back property 2, the failure matrix property 4, the vulnerability memory property 7. 6.3 is where "does the model have it, and does it matter" is answered, so the ablation results are its evidence.

**The de-duplication rule** (it resolves the 6.1-versus-6.3 overlap): **each ch5 finding is explained exactly once, in the section that mirrors its ch5 section.** 6.3 then scores, and points back for the explanation.

| Section | Reads | Its one job | Ends by handing on |
|---|---|---|---|
| Opener (~100 words) | — | The four jobs of ch1 576–580, in order | — |
| 6.1 APT attacker model versus baseline attacker | §5.2 | Why the APT attacker model behaves and succeeds differently with no MTD | the behaviour it carries, into 6.2 |
| 6.2 APT attacker model versus MTD | §5.3 | Why the MTD that holds back one attacker most is not the one that holds back the other | the dependence on the attacker model, into 6.4 |
| 6.3 Properties of the APT attacker model | Table 6.1 + §5.4 (and pointers to 6.1/6.2 for properties 2, 3, 4, 5) | The verdict against the field; which components change an outcome and why the others do not | the ceiling (the attack actions), into 6.5 and §7.2 |
| 6.4 Implications for MTD evaluation | 6.1–6.3 | What someone running an MTD evaluation should now do differently, each with its bound | — |
| 6.5 Threats to validity | everything | What caps each claim: the scope, then internal, construct, external and conclusion validity | each limitation, into §7.2 |

**Headings.**
- 6.1 and 6.2 mirror ch5 verbatim (RULED 2026-09-28).
- 6.3 "Properties of the APT attacker model" is already concise, at five words. The verbose heading is ch3's §3.3.1 ("Properties an MTD attacker model needs to model an APT attacker"), which is out of this scope; flag it to the ch3 owner if wanted.
- 6.3 does not mirror "Ablation studies", because its job is the verdict and the ablations are its evidence (see Q2).

---

## 4. The inventory, by section, primary points first

### Opener
- The four jobs in ch1's order. Say that 6.1–6.2 follow ch5's order.
- Do not say "the two phases": ch5 prose never names them. Use "with no MTD" and "under MTD" (A §C).

### 6.1 APT attacker model versus baseline attacker (reads §5.2)

**6.1-P1 Less success, not a slower path to the goal** (PRIMARY · LIVE, with CHECKs). This is Jin's set-up (i); B R66, C M14–M16.
- *Result:* ASP 5–16× and NCR 2.4–3.3× lower for the APT attacker model. MTTC is only "just" longer (9 700–11 300 s against 9 100 s; c3 overlaps) (Table 5.2).
- *Mechanism:*
  - 26–47 % of its steps are in unmapped tactics, which dispatch no attack action and only take time.
  - Attack actions dispatched in the tactics' order, not the baseline's procedure, meet unmet preconditions and fail before they run: 14–28 % at 100 seeds (**CHECK at 1 000**; ch4 4557–4559, App. B.7 total-mapping control).
- *Rival explanation, and the bound:* the gap is read at the 15 000 s time limit. At 60 000 s the target was reached in 0.58 of runs against 0.67, and the baseline adds no host after about 20 000 s while the APT attacker model still climbs (ch5 comment 6829–6845). That figure is at **100 seeds and declared nowhere in prose: CHECK, or leave it out** (Q5). If it holds, the gap is mostly pace times the time limit, and pace is declared (tactic durations).
- *Deduction:* the APT attacker model is not competing with the baseline attacker. An APT is defined by persistence toward an objective, not by speed (ch3 1143–1154). RULED 2026-09-09 ("we are not trying to beat the inherited model").
- *Fix in the placeholder:* "more slowly" is wrong for time to the goal (commit 9e69e1c2). The APT attacker model is slower only in **attack rate**.

**6.1-P2 Quieter** (PRIMARY · LIVE). Jin: "success rate may be crappy … but much harder to detect"; C M14, M17.
- *Result:*
  - attack rate 0.68–1.23 against 1.71 per minute;
  - attack confidentiality 89.4–98.1 % against 82.2 %;
  - confidentiality falls as rate rises across all five attackers.
- *Mechanism:* time spent in unmapped tactics spaces out the attack actions the scan rule counts.
- *Why it matters:* the field's outcome metrics read a quiet attacker as a weak one. That is the case for an APT attacker model (handed to 6.4-I3).
- *Bound:*
  - Attack confidentiality goes through a declared detector (Snort's default scan rule); the ordering holds at six of nine settings (App. C.4).
  - Counting unmapped steps as attack actions closes the gap (M3: a dry run only, untracked; **CHECK before any number**).
  - The quietness is a consequence of declared durations, not a choice to avoid detection, so property 5 stays a cross.

**6.1-P3 One attack path against many** (PRIMARY · LIVE). B R13–R14, C M18.
- *Result:* the baseline attacker's runs share one opening over four steps, then branch once. The profiles part from step 2 (c1) to step 4 (c3), with 179–947 distinct openings over eight steps (Fig. 5.1(b)).
- *Mechanism:* weighted choice at the Petri net's decision places, drawn from 5–19 attack flows per profile.
- *Bound:* this is variety drawn by documented frequency, not a strategy chosen against the defender (honest reading of property 3). The distinct-openings count also grows with the seed count (R119).
- *Deduction:* an MTD evaluated against the baseline attacker is evaluated against one attack path.

**6.1-P4 Behaviour differs by objective** (SECONDARY · LIVE / CHECK). B R11, R68; C M26.
- The profiles divide their steps differently (Fig. 5.1(a)).
- c3 opens latest and is furthest from the baseline under MTD at 500–1 000 s.
- *Why c3:* no mechanism on record. Its sparsity (7 flows, mostly ransomware) is a candidate. RULED "chapter 6's to discuss", 2026-09-21; see Q6.
- *Bound:* corpus size. The random-partition ablation reads it, in 6.3.

*Tone (not a paragraph):* credit the baseline attacker. It has campaign persistence in full, and every lineage paper used it (C M87).

### 6.2 APT attacker model versus MTD (reads §5.3)

**6.2-P1 The layer reversal: a deployment takes only the state the attacker carries** (PRIMARY, the headline · LIVE + HYP). B K1, R02/R04/R38; C M03, M27–M28; `disruption_mechanism.md` §1, verified in code 2026-09-30.
- *Result:*
  - The host layer holds back the APT attacker model most; the service layer holds back the baseline attacker most, at every interval.
  - No MTD mechanism or deployment strategy ranks first against both.
  - ρ = 0.01 [−0.19, 0.05] at 200 s, and between −0.24 and 0.25 at every interval (Table 5.3, Fig. 5.3).
- *Mechanism:* a deployment never takes back a host or a stolen credential; the attacker "loses only its place" (ch2 919–928).
  - The host layer takes the attacker's position. The APT attacker model's tactics keep dispatching host actions that cannot run until lateral movement restores its position, which costs it 242–324 s. The baseline attacker restarts its procedure at once and loses about 0 s.
  - Service diversity undoes exploit progress, which is the baseline's working state (493 s), and costs the APT attacker model little (60 s).
- *Compare:* Cho (ch3 2117–2121) has diversity defending against persistent attacks. Here the persistent attacker is the one service diversity holds back least. Read it as: the state the attacker carries decides the effect, not its persistence. **HYP**; Q7.
- *Cut:* "Zhang favours shuffle, Ho diversity, read as different attackers". Both ran the inherited attacker, and neither result is introduced in ch2–3 (B C5).
- *Bound:* one simulator and one network. The SDR classes are not the split the attacker feels (one clause).

**6.2-P2 A blocked attack action need not cost time** (PRIMARY · RULED Q14, 2026-10-06). B K2, R51; C M20–M21.
- *Result:* every host-layer deployment blocks the baseline attacker's attack action and costs it no time.
  - For the host layer, actions blocked per deployment are 1 against 0.35–0.39; for the service layer, 0.95 against 0.15.
- *Mechanism:* the APT attacker model is blocked less because it runs no attack action while in an unmapped tactic. That is **by construction, not resilience**. Drop the "resilience" reading (C M20; Marc raised both sides on 10-06 without connecting them).
- *Compare:* Brown's attacker "simply needs to reconnect". This has no ch2/ch3 antecedent, so cite it fresh or add it to ch2.
- *Handed to 6.4-I3:* measure time lost, not only attack actions blocked.

**6.2-P3 MTDShield and the deployment strategies** (PRIMARY · RULED as HYP, 2026-09-26 and 2026-10-06). B K7; C M06–M07, M60.
- *Result:*
  - Random and alternative hold back the APT attacker model more, at every interval.
  - MTDShield holds back the baseline attacker more, up to 1 000 s.
  - MTDShield chooses service diversity in ≥70 % of decisions against either attacker.
- *HYP:* MTDShield was trained against the baseline attacker at 200 s, on 100-host networks (App. D), so its policy favours what works against that attacker. Write "trained against", never "overfits", unless worded as the hypothesis.
- *Random and alternative:* they draw three of seven mechanisms from the host layer, each costing the APT attacker model 242–324 s per deployment. **HYP; CHECK** (Marc's "five of seven" reading differs).
- *Bound:*
  - MTDShield was run as released, with degenerate inputs.
  - It reads an unmapped tactic as nothing detected.
  - It is outside its training conditions (App. D known limitations).

**6.2-P4 Interval** (SECONDARY · LIVE). C M29–M31.
- *Result:* the gap between the attackers is widest at short intervals.
  - Against the APT attacker model, the host layer keeps NCR reduction above 0.5 up to 1 000 s.
  - Against the baseline attacker, the service layer does so only up to 200 s.
- *Bound:* MTD cost is not modelled, so "deploy as often as possible" is not a recommendation (6.5 scope).
- *Optional:* Marc's equal-effect comparison, the interval at which each line falls to 0.5. It can be read off Table E.2 without new runs (Q9).

**6.2-P5 The profiles move together under MTD** (SECONDARY · LIVE). Jin; C M25; RULED 2026-10-06, "the model itself is more important than the profile".
- At 200 s the profiles lie within 0.14 of one another, and the baseline attacker ≥0.24 from the nearest.
- One sentence; it ties to 6.3-P2.

**6.2-P6 Loose ends** (SECONDARY; each needs a decision, Q8).
- **Negative time lost.** The first deployment brings the baseline attacker's first compromise 204–232 s forward, because the forced rescan gives it a second attempt on its first host. The intent spec classes this *conforms* (IS-INT-01/05/07); Marc said "sounds like a bug". Disposition owed; the appendix item is `\owed`.
- **User shuffle reduces the APT attacker model's NCR below zero at every interval.** It is untraced; the candidate is a credential re-seat. Trace it, or state it as unexplained.
- **Inconsistency.** App. D 9671–9673 promises a random-over-four arm that ch5 does not report. Drop the sentence.

### 6.3 Properties of the APT attacker model (reads Table 6.1 and §5.4)

**6.3-P0 Discipline** (one sentence each · LIVE).
- The eight properties were fixed from the literature (§3.3.1) before any model was scored.
- The scoring rule is the same as Table 3.3's.
- The properties are a census, not a scale: more ticks is not a better model.

**6.3-P1 The verdict against the field first** (PRIMARY · RULED 2026-10-05, "credit where credit is due").
- No MTD attacker model of Table 3.3 has more than one property in full.
- The APT attacker model has four in full: 1 (kept), 2, 3, 4. It has two in part: 6 (kept) and 7.
- It is the only one built from CTI (38 attack flows).
- This cashes ch1 contribution 2.

**6.3-P2 Only the attack profiles change an outcome** (PRIMARY · LIVE; the numbers were re-read after the 2026-10-07 redraw). B R27, R98–R99; C M45.
- *Result:*
  - Without the profiles (the attack graph alone), NCR is 0.189 against 0.171 (d −0.28). Over the MTD configurations, 29 of 60 are not negligible.
  - Against ten random partitions of the same sizes, the profiles compromise more than any of them (d 0.25–1.47).
- *Read:* sorting the flows by objective changes the outcome beyond what partition size explains.
- *Marc's expectation was the reverse.* The profiles drive MTDSim's existing attack actions: "you can speak, but you can only say three words" (RULED as the framing, 2026-10-02). Say it as an expectation that was falsified; that is the honest move.
- **Explain the sign carefully:**
  - the profiles compromise *less* than the attack graph, but *more* than random partitions;
  - size explains the shift in NCR reduction;
  - the objective explains the extra compromise.
  - **CHECK** the post-redraw NCR-reduction means before writing (B C18).
- *Handed to 6.4:* one attacker built from the whole corpus does not stand in for attackers with one objective.

**6.3-P3 Adaptivity and learning operate and change no outcome** (PRIMARY · RULED 2026-09-28 and 2026-09-29). B K5, R89, R95–R96; C M43–M44.
- *Failure matrix:* it changes where the attacker goes after a failed initial access (back to reconnaissance in 0.76–0.83 of cases with it, against 0.08–0.10 without). Its effect on NCR is negligible.
  - *Why* (HYP): the simulator already refuses what the failure matrix forbids. An attack action without a foothold fails its precondition: "the failure itself does the work".
- *Vulnerability memory:* exploit success rises from 0.69 to 0.73 (0.92 at one service per OS); the effect on NCR is negligible.
  - *Why* (HYP): a host usually needs a second visit after a scan port reveals the next service. The cost is the detour, not the odds. This four-step chain rests on 20 seeds: **CHECK at 1 000**, and never write "exploit 1 typically fails".
- *One root:* the adopted attack actions decide whether anything the attacker is given matters.
- Told frankly: an idea tested and found not to matter here, so others need not repeat it (C M44: "presenting ideas that didn't work is good").

**6.3-P4 Properties 1, 6 and 7 in one sentence each** (LIVE · RULED 2026-10-05).
- *1 Campaign persistence:* kept from the baseline attacker. It carries on through every disruption, and MTDSim never takes a compromise back. No metric is owed.
- *6 Cost–benefit reasoning, in part:* the RoA order of MTDSim's exploit only. Nothing the model adds weighs cost.
- *7 Learning, in part:* it learns vulnerabilities, not the MTD deployments it observes. This matches Table 3.3's partial for Zhang's halving.

**6.3-P5 Properties 5 and 8: crosses, each with its reason and a pointer to §7.2** (LIVE).
- *5 Detection avoidance:* the behaviour is measured (6.1-P2), but MTDSim has no detector, so the observer is missing, not the behaviour.
- *8 Deployment-strategy awareness:* it needs inference about the schedule. The near-periodic default (200 s plus about 0.5 s) would make the schedule easy to learn (B R86), so the future-work item is specific.

**6.3-P6 What the capture licenses** (PRIMARY close · LIVE).
- 38 attack flows give an envelope of documented behaviour, not one named group.
- One token over a profile's flows can join steps no single actor ran (the strength and the limit are the same fact; define it if used).
- The model is only as good as the attack actions it adopts (the pointer back to ch4 4821–4822 is owed).
- The next gain is in the simulator's attack actions, not in the attacker's decisions. Hand on to §7.2.

### 6.4 Implications for MTD evaluation

Present tense, addressed to anyone running an MTD evaluation. Each implication follows one pattern: the finding, who it changes practice for, a conditional recommendation, and its bound. The opener scopes what transfers: **the dependence and the method, not the numbers.**

**6.4-I1 The attacker model is a variable of the evaluation** (PRIMARY · RULED headline 2026-10-06). Source: 6.2-P1; C M01, M03–M05.
- The rank-1 mechanism changed and the orderings are unrelated.
- *So:* name the attacker model, and evaluate against more than one before recommending an MTD mechanism or deployment strategy.
- *Bound:* shown for two attacker models in one simulator. The direction is what transfers.
- This earns the abstract's "make a case".

**6.4-I2 A learned deployment strategy inherits the attacker it was trained against** (PRIMARY, or merge into I1 · HYP). Source: 6.2-P3; C M06–M07.
- *So:* train and test learned MTD against more than one attacker model.
- *Bound:* one agent, run as released.

**6.4-I3 Report attacker behaviour beside outcome, and time lost beside blocks** (PRIMARY). Source: 6.1-P2 and 6.2-P2; C M12.
- Outcome metrics alone read a slow, quiet attacker as a weak one.
- A blocked attack action is not a cost to the attacker.

**6.4-I4 Declare the attacker model against the eight properties** (SECONDARY). Table 3.3 works as a reporting device; this answers ch3's research gap.

**6.4-I5 Re-check the measures and the defender's inputs when the attacker changes** (SECONDARY · LIVE instances).
- MTDShield's training-code inputs stop 435 of 500 runs against the APT attacker model, because it divides by port scans.
- Its detection input reads an unmapped tactic as nothing detected.
- Also the 80 % stop bug, found and fixed (B R37, R122).

**6.4-I6 Measure how much failure the simulator's own procedure causes before attributing failure to the attacker** (SECONDARY). Run with no MTD and decompose the failures (B R73; ch4 5326–5329). It could fold into I5.

*Cut or demote:*
- the "operating point" implication: its premise, that neither attacker completes, is stale. ASP saturation goes to 6.5 conclusion validity;
- the grading vocabulary (magnitude, ordering, recommendation): it is a new term set; use it only if 6.2 needs it.

### 6.5 Threats to validity

Order: scope first, then internal validity first (the headline is causal). Each threat gives the mitigation already done, with a `\ref`, and the residual it leaves. Define the four types once, citing Wohlin et al. 2012 and de França & Travassos 2015 (**neither is in references.bib**) and Sargent 2011 (in the bib). Use Cook & Campbell's sense of "internal" only.

**Scope** (the artefact's limits by design; each points to §7.2):
- **The one root: the six adopted attack actions** (PRIMARY · RULED 2026-09-28, "literally the underlying attack phases that we're adopting"; C M49–M51). State it once, with its consequences:
  - the tactic-to-action mapping (a chosen input with no interval);
  - seven unmapped tactics;
  - the outcome ceiling;
  - the caps on adaptivity and learning (6.3-P3);
  - precondition failures (6.1-P1).
  - Marc's "blunt instrument" image has never been written; it can earn one plain sentence here.
- MTD runs on its schedule, and **MTD cost is not modelled**, so the interval sweep shows the security half only (B R105; C M30; **in no placeholder**).
- There is no detector, and no deployment-strategy awareness.
- **One 50-host network with two target hosts, and synthetic vulnerabilities** ("the limit an examiner raises first"; B R108; **in no placeholder**).
- Simulation only (pairs with ch3 2598–2601).
- Existing MTD mechanisms only; no new defence.

**Internal:**
- *The bundle.* The APT attacker model differs from the baseline attacker in order, timing and failure response at once. *Mitigation:* the same network, MTD, attack actions and seeds for both attackers; the three ablations. *Residual:* the claim is "the APT attacker model changes the answer", not which of its parts does (RULED 2026-09-25).
- *Corpus size against objective.* *Mitigation:* the random partitions (6.3-P2).
- *Disruption reaches the two attackers differently, by design.* Cite §5.3.1's design; do not raise it as a new threat (RULED 2026-09-28).
- **Verification**, one or two sentences. Named, repeatable checks: the tracer, the intent-spec audit, the tests, determinism. Inherited simulator defects were repaired, and the 80 % stop bug was found and fixed. RULED 2026-10-03; **in no placeholder**.

**Construct:**
- *The 45 s mean duration and the mapping.* Only the 45 s band moves NCR, most likely through command and control mapped to scan neighbours. Halving or doubling it moves no-MTD NCR 0.267 / 0.163 / 0.059. *Residual:* magnitudes move.
  - **Fix the placeholder's residual "the orderings are what is claimed".** App. C did not repeat the baseline comparison across the bands (9473–9475), so whether the cross-attacker orderings survive is untested (B R78, R115).
- *Judgement values.* The failure matrix (210 factors; its ablation shows a negligible effect), the factor of three, the overlay share, one flow per APT group. Declare them as judgement and do not defend them (C M52).
- *Attack confidentiality through a declared detector* (M3, CHECK).
- *Time lost compares the two runs at the same clock time, not the same point in the campaign* (T1, RULED 2026-10-06).
- *Objective classification by one coder,* with Table B.2 as the audit trail (RULED 2026-09-25).
- *The eight properties are this dissertation's own synthesis.* *Mitigation:* each property is sourced; all eight were fixed before scoring and scored by the same rule as the others; two of them are crosses.
- *Optional:* there is no face-validity check of the runs against the corpus's tactic reach (B R110). As run, the Petri net is a continuous-time Markov chain (one token, no concurrency) (B R111, C M64).

**External:**
- *The corpus.* Of the 38 flows, 18 are attributed to an ATT&CK group (criminal groups among them), 20 to none, and one is an adware campaign. They are detected, reported, mostly successful campaigns, so survivorship and selection bias apply. The flows are sparse before intrusion, and several share an operator. They are an envelope of behaviour, not one actor.
- *The adversary.* MTD is measured against documented workflow, not an optimal adversary (B R129; in no placeholder).
- *The schedule.* Only near-periodic deployment timing was run; the exponential was run at 200 s only and is not reported (RULED 2026-10-06, "second-rate").
- *MTDShield* runs outside its training conditions.
- *No numeric comparison with the lineage.* The simulator was repaired, so its numbers differ from the published ones.
- Close with Sargent's ceiling: explore as thoroughly as possible.

**Conclusion:**
- 1 000 seeds; negligible below |d| = 0.2; 24 of 60 cells inconclusive for the profile ablation.
- No correction across the comparisons; Scott–Knott ranking.
- ρ over few entries.
- ASP is rare per profile and its reduction saturates at 1, so the ranking uses NCR reduction.
- **Delete "Spearman's ρ without an interval"** (stale: ch5 now gives the interval).

**§7.2 pointers that 6.5 must make visible**, ordered by the limitation each lifts:
- a richer set of attack actions (the binding constraint);
- a detector;
- deployment-strategy awareness;
- MTD optimised against the APT attacker model, with MTDShield retrained (Jin: "the next step");
- a memory that acts on the next hop;
- MTD cost;
- other network sizes;
- emulation;
- concurrency.

---

## 5. Contradictions to fix in the placeholders before drafting

| # | Placeholder says | Current truth | Source |
|---|---|---|---|
| C1 | "less success, more slowly" | slower in attack rate only, not in MTTC | ch5 6905–6907; 9e69e1c2 |
| C2 | the penalty is paid only by deployments that disrupt an attack action | the APT attacker model also pays it in an unmapped tactic | ch4 4828–4830 |
| C3 | "the simulator returns one failure verdict whatever the cause" | the model's join merges the interrupt and the precondition verdicts; that is the model's choice | B C3 |
| C4 | Zhang vs Ho read as attacker-dependence | both used the inherited attacker; cut | B C5 |
| C5 | "ρ without an interval" | ρ = 0.01 [−0.19, 0.05] | ch5 7726–7727 |
| C6 | property-2 random-partition numbers (0.35 against 0.33) | pre-redraw; re-read | e40956f4 |
| C7 | "the orderings are what is claimed" (construct residual) | the cross-attacker orderings are untested across the bands | App. C 9473–9475 |
| C8 | old FED-BY and PARKED blocks (`subsec:aio-capabilities`, `sec:captured`, the movement attacker, the operating point, the learning exponent, the disengagement frontier) | retired; strip them when the placeholders are rewritten | B (iv) tail |
| C9 | the ch5 opener's ch6 sentence is called "verbatim ch1" | ch1 was reworded on 10-07 | A §G1 |

## 6. Cut list (stale or retired: do not draft)

- *MTD's post-intrusion blind spot:* retired as false in ch3 round 66 (the baseline attacker has campaign persistence); Marc downgraded it 2026-10-07.
- *"Resilience" from fewer blocks:* by construction.
- *Profile-dependent best MTD:* the profiles keep one layer order.
- *The −0.893 inversion and "very nearly opposite":* now "unrelated".
- *"Neither attacker completes":* the targeted scenario completes.
- *The utility λ, learning κ, forgetting, disengagement and alignment dials; the routing learner:* no longer in the model.
- *Target-seeking failing at depth:* a pre-targeted-scenario probe.
- *"Weakest link" symmetry with ch3:* the phrase is no longer in ch3 prose. Marc's framing (C M01) can live in 6.4's opener only if he wants it there (Q4).
- *The simultaneous scheme, the 13-fold per-tactic variation, cost-denominated metrics, belief destruction, the two MTTCs:* retired.

---

## 7. Questions for Marc (each with a recommendation)

**Structure**
- **Q1.** Use the de-duplication rule (§3): each ch5 finding explained once, in its mirror section, with 6.3 scoring and pointing back? *Recommend yes.* It removes the 6.1/6.3 overlap you felt.
- **Q2.** The ablations go in 6.3 as the evidence for properties 2, 4 and 7, with the heading kept as is? *Recommend yes.* The alternative, a "6.3 Ablation studies" mirror plus a 6.4 verdict, splits the verdict from its evidence.
- **Q3.** Should 6.4 carry three primary implications (I1, I3, and I2 folded into I1) with I4–I6 as one sentence each, or fewer? *Recommend I1 (with I2) and I3 as the primary implications.* They are the ones the abstract and Jin's set-ups lean on.
- **Q4.** Is the "the attacker model is the weakest link of an MTD evaluation" framing (C M01, your own) the opener of 6.4? It has been cut from ch3 prose, so it would be fresh here.

**Content only you can settle**
- **Q5.** Does the time-limit point go in 6.1-P1? At 60 000 s the gap nearly closes (100-seed, comment only). Including it is the strongest rival explanation and the most honest reading, but it needs a 1 000-seed run, or a careful "at the declared time limit" bound. *Recommend:* bound the claim to the time limit in one clause now, and decide on the run once the rest is drafted.
- **Q6.** Why does c3 differ? Do you have a mechanism in mind (ransomware flows reaching impact, which is unmapped?), or do we state it as an observation bounded by sparsity? *Recommend the observation plus sparsity, unless you want a trace.*
- **Q7.** The Cho contrast (6.2-P1). Do you want to engage ch3's "diversity defends against persistent attacks" directly? *Recommend yes.* It is the one place the results speak back to a cited claim, which is the comparison move examiners look for. How do you read it?
- **Q8.** Negative time lost: bug or design? The intent spec says it conforms to Brown's design. And user shuffle: trace it or call it unexplained? *Recommend:* design (leave it, explain it in one sentence); user shuffle unexplained unless a trace fits the schedule.
- **Q9.** Your equal-effect comparison (the interval at which each attacker's NCR reduction falls to 0.5): is it in 6.2-P4? It reads off Table E.2 with no new runs.
- **Q10.** In 6.5, what would *you* expect an examiner to attack first, beyond the attack actions? Four candidates are in no placeholder: synthetic vulnerabilities, MTD cost not modelled, verification, and documented workflow rather than an optimal adversary. Which are in?
- **Q11.** "What I would do differently" (reversing the edges for the failure matrix, adopting MTDSim's own durations): put it in future work as an improvement (UWA question 5), in 6.5, or leave it out? *Recommend future work, one sentence, phrased as an improvement, never as regret.* Clarify first whether the reversal was Jin's original ruling or not (C M53 records both).
- **Q12.** Does the conclusion close on Volt Typhoon (ch1's hook)? Yes or no. Careful: the model is not an answer to Volt Typhoon (C M95).

**What I could not find, which only you may hold**
- **Q13.** Is any discussion point from your conversations with Jin missing from §4? Is there an idea you have had since 10-06 that no session recorded?

---

## 8. Marc's answers, round 2 (2026-10-07), and what was done

- **Explain-once rule: yes.** The ablations go in 6.3. The five sections and headings stand. The old placeholders were stale and AI-generated, "not the Bible".
- **Register:** chapter 5's short, sharp sentences and fixed terms, plus the moves chapter 5 forbade: "because", one calibrated hedge per claim, the chapter 3 comparison, the bound.
- **No reruns** (a 60 000 s run is 4–5 days). The no-MTD gap is bounded "at the 15 000 s time limit".
- **c3:** Marc's reading verified on `ch5_s531_unopposed/numbers_reported.json`. Unmapped share of steps / time, against attack rate and attack confidentiality:
  - c4: 26/34 %, 1.23, 89.4 %
  - c1: 36/50 %, 1.09, 92.4 %
  - c2: 37/51 %, 0.89, 96.0 %
  - c3: 47/57 %, 0.68, 98.1 %

  c3 is the far end of the quieter mechanism, not an anomaly. Into 6.1 point 2.
- **Cho:** scoped to MTDSim. No blanket claim about diversity; MTDSim's implementation of each mechanism fixes what it takes.
- **Negative time lost:** not a bug (Marc). It is surfaced as a 6.2 point.
- **Equal-effect comparison:** in 6.2, read off Table E.2.
  - Host layer: ≥0.5 up to 1 000 s against the APT attacker model, against 100 s for the baseline attacker.
  - Service layer: to 200 s against the baseline attacker; never 0.5 against the APT attacker model.
- **Examiner targets, in Marc's order:**
  1. the attack actions ("adopted from a published simulator, shared by both attackers");
  2. the failure matrix and the vulnerability memory (ablated: no outcome);
  3. the tactic durations;
  4. the partition (a declared model parameter);
  5. the metrics' provenance and numbers;
  6. Table 6.1 agreeing with ch3's scores (sync obligation).
- **"What I'd do differently":** goes in 6.5 construct as *simpler alternatives not tried*, framed as improvements pointing to §7.2 (reversed edges for the failure matrix; one duration for every unmapped tactic). Never as regret.
- **Volt Typhoon:** a circular close is wanted. Recommended home: the conclusion's opener, before Contributions. Not yet drafted.
- **Jin:** no new input; ch1–5 feedback pending (up to a week). Draft on ch1–5 as fact, judging repo ideas on merit.
- **Done:** ch6 placeholders and planning comments replaced by point sets (bold claim; result, why, compare, bound, so). Table 6.1 and all labels kept; the old blocks are at `644dbf03`. Build clean, 102 pages, ch6 pp. 39–45.

## 9. Marc's read of 6.2 against the data (2026-10-07), checked on the 1 000-seed corpus

Marc dictated a read of Figures 5.2–5.4 and Tables 5.3, E.2 against the 6.2 point set. Each claim he asked to be checked, with the evidence. Sources: `data/results/ch5_defended/numbers_reported.json` (`sweep.by_interval.*.attacker.*`: `point/lo/hi`, `hosts_none`, `hosts_cond`, `denied_share` = share of runs with no host compromised), `time_lost_first_deployment_numbers.json`, and two scans of `runs_reported.jsonl` (compromising verb per record; the scripts were one-offs, re-runnable from the field layout in `run_corpus.py` 247–253: record = place, verb, outcome, verdict, blocked, interrupted, dwell, start, end, class).

| Marc's claim | Verdict | Evidence |
|---|---|---|
| NCR reduction masks starting points | **Holds for sizes across attackers, not for the rankings.** | No-MTD NCR: 8.5 hosts (APT) vs 24.8 (baseline). At 200 s IP shuffle removes 8.2 APT hosts, 17.0 baseline hosts. A ranking is within one attacker (one denominator), so the reversal is not an artefact of the relative form. |
| Why NCR, not ASP | **Already ruled (2026-10-06 Q3; 2026-09-29 L): do not reopen in ch6.** | ASP saturates at 1.00 for the APT attacker model under the host layer (≤500 s), so it cannot order mechanisms; Scott–Knott needs a continuous measure. The layer reversal holds on ASP reduction at every interval (`tab:eff-interval-values-asp`) — a one-clause robustness bound. NCR and ASP move together except the baseline's host layer from 500 s (NCR reduction > 0, ASP reduction < 0). |
| APT thwarted before a foothold under the host layer | **Holds.** | `denied_share`, 50–200 s: APT 0.69–0.89 under the three host-layer mechanisms; baseline 0.03–0.20. Not in ch5 prose: CH5 FIRST if used. |
| Random and alternative should match over 1 000 runs | **False premise; the gap is real, not noise; no re-run.** | `mtd_scheme.py` 124–130: alternative is a fixed round-robin (CTS → HTS → IP → OS → port → SD → US, `run_corpus.py` MODULES order); random draws with replacement. Gap ≤ 0.06; CIs exclude each other (e.g. baseline 100 s: 0.52 [0.50, 0.54] vs 0.58 [0.56, 0.60]). Scott–Knott one rank apart. Use: 6.5 conclusion validity (large n separates trivial gaps; read ranks as groups). |
| User shuffle below zero is the first-deployment second try | **Does not hold for the APT attacker model; the credential re-draw does.** | First deployment costs the APT model +9.9 s (2 000 s); later deployments −44.9 s ("state differs"), and 0.01 actions blocked per deployment. `usershuffle.py`: every internal host's accounts re-drawn, attacker's held accounts valid (D-02 ruling); `host.py` `can_auto_compromise_with_users` / `compromise_with_users` log in with held accounts. Compromises by credential reuse at SCAN_PORT, 200 s: APT 1.30 → 2.44 per run (NCR +0.85 hosts); baseline 5.18 → 7.56. Credentials do matter to both attackers' attack actions, contrary to the dictated "they don't rely on credentials". |
| Thresholds 0.5 / 0.8 | **Direction holds at both; the factor does not.** | 0.5: APT host-layer mean to 1 000 s, baseline host-layer to 100 s, baseline service-layer to 200 s, APT service-layer never. 0.8: APT host-layer to 200 s (0.79 at 500 s), baseline host-layer never (max 0.72); baseline service-layer to 200 s, APT service-layer never (max 0.35). Marc's per-mechanism 0.8 readings for the baseline (port 200–500, OS 100–200, SD 200–500) match. |
| Port shuffle / OS diversity merge near zero | **Holds, both attackers.** | By 500 s: APT port 0.07, OS 0.00; baseline port 0.10, OS 0.04. Baseline service-layer mean 0.84 (200 s) → 0.27 (500 s). HYP: MTD holds back only while the interval is shorter than the time to rebuild what a deployment takes. |
| Blocked actions "divorced from" time lost | **Holds for the baseline only.** | APT: blocked host 0.35–0.39 > service 0.15 > user 0.01; time lost host 242–324 > SD 60 / port 26 / OS −8 > user −26 (same order by layer). Baseline: blocked 1 / 0.95 / 0.07; time lost ≤ 0 except SD 493. |
| MTDShield picks what one would pick against the baseline | **Holds.** | SD first or tied first against the baseline at every interval; rank 4 against the APT model (Table 5.3); MTDShield ≥ 70 % SD. "Overfit" stays the hypothesis's word. |
| Tay modelled IDS by proxy | **Holds, defender side.** | `extractions/tay2024.md` T-EVAL-04/05: a varying fraction of attacker-action information fed to the agent; nothing about the attacker changes. Antecedent only in App. D. |

**Placement.** The 6.2 point set in `dissertation.tex` now carries these (P2 and old P3 merged; user shuffle no longer "open"; random vs alternative added as a loose end for 6.5). 6.1's quieter point gained the Tay compare. **2026-10-08:** the App. E first-deployment item is ruled out; its key points are in 6.2-P2 and the rest in `docs/implementation/disruption_mechanism.md` §9.

## 10. Retired point groups: 6.2 paragraphs 1 and 2 (drafted 2026-10-08)

Marc's ruling (2026-10-08): once a paragraph is drafted and every idea in its point group is carried, the point group leaves the LaTeX and is kept here as context. Paragraph 1 was drafted from the group below (commit 4326af94); paragraph 2 from the arrangement Marc approved in chat the same day.

**What the drafts carry, and what they leave out.**
- P1 carries every point but one: the optional instance (up to 200 s the host layer leaves most of the APT attacker model's runs with no host compromised; 69 to 89 % against 3 to 20 %) is NOT IN CH5 and is left out. Give it a chapter 5 sentence first if wanted.
- P2 drops the 2 000 s bound (Section 5.3.1 states it) and leaves the same-clock-time caveat to 6.5 (still listed in the tex "TO 6.5" comment). The topology-shuffle point (HYP: rebuilt links hand the baseline attacker new neighbours; above its no-MTD NCR from 1 000 s) moved to P3's counterpoints, since it reads Figure 5.3.
- P2 adds what the arrangement added: OS diversity as the third way a deployment helps the attacker (HYP, not traced; -8 s for the APT attacker model, CI includes zero; -58 s for the baseline attacker, its later deployments about -21 s against port shuffle's +21 s, from `time_lost_first_deployment_numbers.json` `state_differs`); "changing the IP does not help: the restart after the first deployment does".
- Writing notes the drafts follow: across attackers say "a larger share", never "more hosts"; lead each "deployment helps the attacker" case with its rule, so none reads as a bug; "holds back" for the effect on NCR.

**The retired LaTeX, verbatim.**

```latex
  % ------------------------------------------------------------------- P1
  \item \textbf{In MTDSim, which MTD mechanism holds an attacker back depends
  on the attacker model.} (Lead-in and headline; chapter 1, contribution 3.)
  \begin{itemize}
    \item Result (Table~\ref{tab:eff-cross-arm},
    Figure~\ref{fig:eff-cross-arm}):
    \begin{itemize}
      \item the host layer reduces the APT attacker model's NCR most, the
      service layer the baseline attacker's, at every deployment interval;
      \item no MTD mechanism or deployment strategy ranks first against both;
      $\rho$ between the two rankings is near zero.
    \end{itemize}
    \item Why, the frame (Marc: ``what do we actually change''):
    \begin{itemize}
      \item MTDSim writes each deployment's effect against the baseline
      attacker's procedure: the attack actions it blocks, and the attack
      action it sends the attacker back to
      (Section~\ref{subsec:attacker-model}, Figure~\ref{fig:attacker-model});
      \item the APT attacker model keeps the attack actions and drops the
      procedure: its Petri net chooses the next tactic, and its unmapped
      tactics take time without an attack action
      (Section~\ref{sec:execution});
      \item so one deployment takes a different state from each attacker.
    \end{itemize}
    \item Why, per layer (one line each):
    \begin{itemize}
      \item service layer, baseline attacker: service diversity redraws every
      service, so the vulnerabilities it was exploiting, and the impact it had
      built up on them, are gone. Vulnerabilities are the currency of
      MTDSim's attacker (Marc), and exploiting is most of its time;
      \item host layer, APT attacker model: a deployment costs either attacker
      only its place. The baseline attacker finds it again at once, by
      rescanning. The APT attacker model regains it only when its Petri net
      next reaches lateral movement; until then its attack actions fail for
      missing preconditions (HYP in prose: chapter 5 shows the time lost,
      not the failed dispatches);
      \item service layer, APT attacker model: blocks only port scans,
      exploits and brute force, which the APT attacker model runs less often,
      between unmapped tactics (point back to Section~\ref{sec:disc-behaviour}).
    \end{itemize}
    \item Counterpoints:
    \begin{itemize}
      \item not shuffle against diversity: the split runs by layer (port
      shuffle, a shuffle, ties first with service diversity against the
      baseline attacker); shuffling, diversity and redundancy serve different
      purposes (Section~\ref{sec:mtd-concept}). No verdict on diversity;
      \item not the relative measure: a ranking compares MTD mechanisms
      against one attacker, over one denominator; across attackers say ``a
      larger share'', never ``more hosts'';
      \item not the choice of NCR: the reversal also holds on ASP reduction
      (Table~\ref{tab:eff-interval-values-asp}); one clause;
      \item agrees with Cho et al.: the attacker model decides which
      deployment strategy is optimal
      (Section~\ref{subsec:defence-modelling-approaches}).
    \end{itemize}
    \item Sub-point, the attack profiles
    (Figure~\ref{fig:eff-suppression-profiles}):
    \begin{itemize}
      \item they move together at 50 to 200\,s, far from the baseline
      attacker: the attacker model matters more than the attack profile (Marc
      2026-10-06);
      \item from 500\,s $c_3$ separates, highest under the host layer and
      lowest under the service layer (HYP): it spends the most steps in
      unmapped tactics and the fewest in lateral movement
      (Figure~\ref{fig:aio-coverage}(a)), the far end of the same mechanism.
    \end{itemize}
    \item Instance, optional (NOT IN CH5): up to 200\,s the host layer stops
    most of the APT attacker model's runs before its first compromise.
    \item Bound: one simulator and one network; what each MTD mechanism takes
    is MTDSim's implementation; MTDSim has no redundancy mechanism.
    \item So: an evaluation's ranking carries its attacker model's
    assumptions (Section~\ref{sec:evaluation-implications}).
  \end{itemize}

  % ------------------------------------------------------------------- P2
  \item \textbf{MTD holds an attacker back by the time it costs it, not by
  the attack actions it blocks.}
  \begin{itemize}
    \item Result (Figure~\ref{fig:aio-adaptivity}, Table~\ref{tab:disruption}):
    \begin{itemize}
      \item for the APT attacker model, attack actions blocked and time lost
      order the MTD layers the same way;
      \item for the baseline attacker they do not: every host-layer
      deployment blocks it and costs it no time; the three service-layer
      mechanisms block it equally, and only service diversity costs it time.
    \end{itemize}
    \item Why (Marc 2026-10-08): every block ends the attack action as a
    failure, so the cost is what the attacker does after the failure:
    \begin{itemize}
      \item the baseline attacker restarts its procedure: cheap after the host
      layer; expensive only after service diversity, which erases its exploit
      progress (port shuffle leaves the vulnerabilities in place; OS
      diversity redraws only some services, Table~\ref{tab:defence-mechanisms});
      \item the APT attacker model's failure matrix routes its token, and after
      the host layer it waits for lateral movement (P1);
      \item it is blocked less by construction, not resilience: no attack
      action runs during an unmapped tactic;
      \item the blocked bars match within a layer by construction: one rule
      per layer decides what a deployment blocks.
    \end{itemize}
    \item Counterpoint, a deployment can help the attacker (lead with the
    rule, then the consequence, so none reads as a bug):
    \begin{itemize}
      \item the restart: Brown's design sends the baseline attacker back to
      its first attack action after a block, whatever its progress
      (cite \citep{brown2023}). The first deployment lands while it exploits
      its first host, so the restart gives it a second attempt there, and its
      first compromise comes earlier (Section~\ref{subsec:aio-disruption}).
      The APT attacker model gets no second attempt;
      \item user shuffle: it re-draws every host's accounts and leaves the
      attacker's accounts valid, so each deployment re-rolls the hosts the
      attacker could not log into; it raises the APT attacker model's NCR at
      every interval (checked; NOT IN CH5 for the credential counts);
      \item topology shuffles (HYP, not traced): rebuilt links can hand the
      baseline attacker new neighbours, above its no-MTD NCR from 1\,000\,s;
      IP shuffle, which rebuilds no links, does not.
    \end{itemize}
    \item Bound: Figure~\ref{fig:aio-adaptivity} is at 2\,000\,s because the
    next deployment caps time lost (one clause); run and twin are compared at
    the same clock time (6.5).
    \item So: time lost per MTD deployment, not attack actions blocked,
    measures what MTD costs an attacker
    (Section~\ref{sec:evaluation-implications}).
  \end{itemize}

```

## Validation gate

Done when Marc has answered §7, the structure in §3 is ruled, and every primary point in §4 has its evidence re-read on the 1 000-seed corpus, or is labelled a hypothesis. The next deliverable is per-paragraph dot points (slot form) for Marc's dictation.

## Reading list for the next session

1. This file.
2. The ch6 placeholders, `dissertation.tex` 8373–9033.
3. Harvest A §C (ch5 findings as stated).
4. Harvest D §2–§4 (benchmarks and move skeletons).
5. `docs/implementation/disruption_mechanism.md` §1 (6.2's mechanism).
