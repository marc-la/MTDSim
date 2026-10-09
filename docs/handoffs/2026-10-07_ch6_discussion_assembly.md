---
status: open — structure ruled (§8); point sets in the ch6 placeholders for Marc's read; next: Marc triages 6.4 and marks points in or out, then slot-form dot points per paragraph
created: 2026-10-07
updated: 2026-10-08
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

### 10b. Paragraph 3 (drafted 2026-10-08)

Marc's frame: deployment intervals are secondary to "attacker models versus MTD"; MTD efficiency (overhead, loss of service) is not modelled, so faster is always better in MTDSim and the right interval cannot be known. The claim was reworded from "the attackers need different deployment intervals" (it implied a recommendation) to "a shorter deployment interval holds an attacker back more, and the interval at which that effect falls away depends on the attacker model". 6.4's interval implication now states the direction only (the "up to ten times" factor is dropped).

**Cut from the paragraph, kept here:**
- The suspension plateau: below about 100 s deployments overlap and MTDSim suspends the excess, so the curves flatten (service-layer mechanisms 148 executed at 50 s against 149 at 100 s; disruption_mechanism.md section 9). No chapter states the suspension rule; it re-enters only if chapter 2 or 5 gets a sentence on it.
- User shuffle holds the baseline attacker back at 50 s (NCR reduction 0.45) by a brute-force loop (checked; disruption_mechanism.md section 9). Below any practical interval.
- Topology shuffles (HYP, not traced): rebuilt links can hand the baseline attacker new neighbours, so its NCR rises above its no-MTD NCR from 1 000 s; IP shuffle, which rebuilds no links, does not.

**The retired LaTeX, verbatim.**

```latex
  % ------------------------------------------------------------------- P3
  \item \textbf{The attackers need different deployment intervals.}
  (Follows from P2.)
  \begin{itemize}
    \item Result (Figure~\ref{fig:eff-cross-arm},
    Table~\ref{tab:eff-interval-values}):
    \begin{itemize}
      \item the host layer keeps half or more of the APT attacker model's NCR
      off up to a far longer interval than it does the baseline
      attacker's;
      \item the service layer halves the baseline attacker's NCR only at
      short intervals, and never the APT attacker model's;
      \item the direction holds at a stricter threshold; the factor between
      the attackers does not.
    \end{itemize}
    \item Why (HYP): MTD holds an attacker back while the interval is
    shorter than the time the attacker needs to recover what a deployment
    took (P2):
    \begin{itemize}
      \item hence the cliffs, at different intervals for the two attackers;
      \item hence port shuffle and OS diversity near zero against both from
      500\,s.
    \end{itemize}
    \item Counterpoints:
    \begin{itemize}
      \item faster is always better here only because MTDSim charges a
      deployment no cost (6.5 scope); below the 200\,s default the intervals
      are the least practical;
      \item below about 100\,s deployments overlap and MTDSim suspends the
      excess, so the curves flatten (CH2 or CH5 FIRST: the suspension rule is
      stated nowhere);
      \item user shuffle holds the baseline attacker back at 50\,s by a
      brute-force loop (checked): one clause, or cut, since it sits below any
      practical interval.
      \item topology shuffles (HYP, not traced; moved from P2 2026-10-08):
      rebuilt links can hand the baseline attacker new neighbours, so its NCR
      rises above its no-MTD NCR from 1\,000\,s; IP shuffle, which rebuilds
      no links, does not.
    \end{itemize}
    \item So: the earlier MTDSim studies ran 50 to 200\,s, where both layers
    hold the baseline attacker back; an interval tuned against the baseline
    attacker is mis-set for an APT attacker. Bound: no interval is
    recommended (6.5).
  \end{itemize}

```

### 10c. Paragraph 4 (drafted 2026-10-08), and the point-set header

Marc's read: MTDShield is an Appendix D item; its line follows service diversity's and sits below it. Correction made in chat and in the draft: the gap is the doing-nothing share (23 % and 29 % at 200 s), not other mechanisms (IP shuffle, complete topology shuffle and OS diversity under 1 % together). The two strengthening facts (the host layer on its menu; inputs passed as measured at the other intervals) are already in Appendix D (Table D settings, Behaviour observed, the configuration paragraph): no appendix change needed. MTDShield against service diversity, baseline attacker, 200 s: 0.68 against 0.92 (Table E.2). Marc's closing lesson ("if we can model what we know about the attacker, we can work out how to hold it back"; reduce assumptions first) is a comment in the future-work placeholder. Not carried: "deploys less, NOT IN CH5" (about 55 against 75 deployments per run at 200 s) is now carried by the Appendix D doing-nothing shares.

**The retired LaTeX, verbatim (the dictation line, the header comment, and P4).**

```latex
\noindent\emph{[Points for dictation, reading Section~\ref{sec:effectiveness}.]}
% 2026-10-08: P1 and P2 drafted above; their point groups retired to the ch6
% handoff, section 10 (Marc: drafted ideas leave the LaTeX). P3 drafted and
% retired the same day; P4 remains.
% RESTRUCTURED 2026-10-08 (Marc ruled the four-paragraph chain): which MTD ->
% what a deployment costs -> how often MTD must deploy -> what a learned
% strategy does with it. Each paragraph is the next one's cause. The old
% "observations" paragraph is gone; its items are sub-points where they
% belong. Layout: bold = the paragraph's claim; level 2 = its elements
% (result, why, counterpoint, so); level 3 = the detail under each.
% Tags: (HYP) an explanation, written as one; (NOT IN CH5) a number chapter 5
% does not give: give it a chapter 5 home or drop it. Evidence for every
% check: docs/implementation/disruption_mechanism.md section 9; the ch6
% handoff section 9. Earlier point sets: git d736bbac, 7fe97e76, 33d2e16d.
\begin{itemize}
  % ------------------------------------------------------------------- P4
  \item \textbf{MTDShield favours the MTD mechanism that holds back the
  attacker it was trained against.}
  \begin{itemize}
    \item Result (Section~\ref{subsec:eff-cross-arm},
    Appendix~\ref{app:mtdshield-observed}):
    \begin{itemize}
      \item MTDShield holds back the baseline attacker more, up to 1\,000\,s;
      random and alternative hold back the APT attacker model more;
      \item MTDShield chooses service diversity in most decisions, against
      either attacker.
    \end{itemize}
    \item Why (HYP; Marc's ``overfits'' is this hypothesis):
    \begin{itemize}
      \item service diversity is what a reader of
      Table~\ref{tab:eff-interval-values} would pick against the baseline
      attacker, and it ranks mid-table against the APT attacker model;
      \item MTDShield was trained against the baseline attacker;
      \item random and alternative draw three of seven mechanisms from the
      host layer, so they carry no such bias.
    \end{itemize}
    \item Instance: under MTDShield all four attack profiles sit below the
    baseline attacker (Figure~\ref{fig:eff-suppression-profiles}(i)): Marc's
    ``slide underneath''.
    \item Counterpoints:
    \begin{itemize}
      \item one policy, run as released, outside its training conditions
      (Appendix~\ref{app:mtdshield-limitations});
      \item it also deploys less often, choosing no deployment at some
      intervals (NOT IN CH5).
    \end{itemize}
    \item So (to 6.4): train and test a learned deployment strategy against
    more than one attacker model.
  \end{itemize}
\end{itemize}
```

## 11. 6.1 point set refined, and a cold examiner's questions (2026-10-08)

**Ask (Marc).** Refine the 6.1 point set and arrange it logically, with nested points. First, give the floats 6.1 reads (Figure 5.1, both panels; Table 5.2), plus Figure 5.4 for the profiles point, to a cold examiner agent with no chapter 6. Its questions show what the discussion covers and what it misses, and may change the framing.

**New order in the tex (DRAFT STATE; old set at `861e74ee`).**
1. Quieter.
2. Compromises less by the time limit.
3. One attack path against hundreds.
4. The profiles differ (secondary).

1 → 2 is a chain with one cause: unmapped time makes it quiet, and the same time leaves it fewer attack actions by 15 000 s. This is the examiner's framing point, owned up front rather than left for the examiner to find.

**Two one-off checks (scripts not kept; re-runnable from the record layout in `run_corpus.py`).**
- *Openings by attack action.* `ch5_s531_unopposed/runs_reported.jsonl`, k = 8, dwell-only records dropped, consecutive repeats collapsed (the baseline row's rule): c1 844, c2 484, c3 190, c4 592, against the baseline attacker's 3. Keeping unmapped steps as one "none" symbol gives c1 814, c2 628, c3 100, c4 460. The tactic count reproduces Figure 5.1(b) (947, 748, 179, 662). The plurality point survives the unit change. **NOT IN CH5.**
- *Does rate order the profiles under MTD?* `ch5_defended/numbers_reported.json`, `sweep.by_interval.*.profile`. c3, the slowest, separates from 500 s: it is highest under the host layer (0.88 against 0.71–0.76 at 500 s) and lowest under service diversity (0.10 against 0.20–0.28). The other three move together and do not follow their attack rates (service diversity at 500 s: c2 0.20, c4 0.24, c1 0.28; host topology at 1 000 s: c1 0.49, c2 0.44, c4 0.38). Marc's "less frequent = further from the baseline" holds for c3 only.

**Examiner questions, triaged.**

*Already covered by the point set:*
- Tempo and the time limit (Q1, Q3).
- Stealth, or a side effect of time? (Q6)
- Openings: choice, or the walk's randomness? (Q7)
- Objective, or partition size? (Q14; Figure 5.4 "does objective matter")

*Added as bounds:*
- Attack rate and attack confidentiality are one effect read twice, through a rate rule (Q5).
- MTTC is over the successful runs only: 42–139 against 656 (Q12). c3's MTTC overlaps the baseline attacker's, so the claim is "only just longer", not "longer".
- **ASP scores the target host, not the profiles' own objectives, which are unmapped (Q2). This is new; it also belongs in 6.5 construct.**
- Openings are counted in different units (B).
- The openings count is capped by the runs (B).
- c3 alone follows the rate order under MTD (D).

*Belongs elsewhere:*
- Mapping semantics, e.g. command and control dispatches a neighbour scan (Q10): ch4 ceiling, 6.5 construct.
- Persistence unmapped (Q11): ch4 already says "a compromised host stays compromised".
- Figure 5.4's ceiling at 50–200 s, relative versus absolute reduction, the baseline attacker's cliff at 200–500 s, negative user shuffle and topology shuffle, and near-ties in "most effective" (D): 6.2; most are already in the 6.2 draft or §10.
- Long intervals limited by the time limit, about 7 deployments at 2 000 s (D): 6.5.

*Not covered. Recommend leaving out unless Marc wants them:*
- Why the baseline attacker fails about a third of its runs with no MTD (Q4). No mechanism on record. The 100-seed 60 000 s comment suggests a plateau, not the time limit, but that is undeclared.
- c4 has the highest attack rate of the profiles but the lowest ASP (Q8).
- ASP and NCR rank c1 and c3 differently (Q9).
- What each tactic mix predicts for MTD (Q13).

*Flag for the ch5 float owner (out of scope here):* Figure 5.1(a) prints "0" for resource development (c1, c2) as distinct from "<1" and blank. Either a reached-but-rounded cell needs a key, or it is a rounding artefact.

### 11a. Marc's answers to the four "leave out" questions (2026-10-08), and where each went

| Question | Marc's answer | Check (one-off; NOT IN CH5) | Routed to |
|---|---|---|---|
| Baseline attacker fails a third of its runs | A framing answer: CTI holds only detected, reported, mostly successful campaigns. So no claim on real-world success rates, only on modelled mechanisms and outcomes seen in MTDSim. New idea: each attacker's share of successful runs that stayed undetected. | Not computed; it needs a per-run detection rule, which is a new metric. | 6.1 point 2 frame bullet; candidate in the future-work comment |
| c4: highest rate, lowest ASP | Sparsity (five attack flows) limits the orders that meet an attack action's preconditions. | c4 makes 116 exploits per run, the most, and 66 % fail on an unmet precondition, the highest share (c3 52, c1 57, c2 60). The share follows exploit-dispatching steps per port-scan step (c3 1.0, c1 1.75, c2 1.9, c4 2.2): an exploit needs `curr_ports` from a port scan (`attack_operation.py` `assert_action_context`). Bound: c1 has as few successful exploits per run (6.38 against c4's 6.32) but three times the ASP. Random control, NCR with no MTD: the 19-flow groups give 0.16–0.21; the 7- and 5-flow groups give 0.02–0.18, lower and more spread. ASP is not recorded per group. | 6.1 point 4 (HYP); 6.5 external; future work (partition size) |
| ASP and NCR rank c1 and c3 oppositely | Breadth against depth: ASP needs one of two target hosts, NCR counts every host. | Hosts per run: c3 8.48 against c1 7.32 in failed runs, and 10.43 against 8.29 in successful runs. So c3 is broader either way, not only because success truncates the run. | 6.1 point 4 (HYP) |
| What the tactic mix predicts for MTD | Reread as an edge ablation: remove one tactic-to-tactic edge at a time and measure ASP and NCR. The most sensitive edge is where a mitigation that breaks that transition matters most, which lets mitigations be proposed from the attacker model. | — | Future-work comment |
| Attack flows have gaps | A technique that was not directly observed (theft implied by the report's narrative) is absent from the flow, which made a partition by terminal objective hard. | — | 6.5 external |

**Figure 5.1(a) "0" fixed.** The 0 is a true zero, not a rounding artefact. Resource development is in c1's and c2's attack flows, but no run can enter it: c1 has no incoming arc, and c2's one incoming arc has weight 0 (`data/ogasp/petri/*_structural.json`). The caption is keyed ("0: a tactic they reach that no run takes"); the cell is left as generated.

**Method kept (Marc):** for each discussion section, a cold examiner reads the floats the section reads. Its questions are triaged (covered / added as a bound / belongs elsewhere / not covered), and the uncovered ones go to Marc, each with a recommendation. His answers are routed to whichever section they belong in.

### 11b. 6.1 paragraphs 1–2 drafted (2026-10-08); point 1 retired; what makes a run succeed

**Point 1, retired verbatim** (drafted as paragraph 1; every idea carried, except the two points overturned on merit and named in the draft's comment: rate and confidentiality are not "one effect", per §4.5.1; MTDShield does deploy on detection):

```latex
  \item \textbf{With no MTD, the APT attacker model is quieter: fewer attack
  actions per minute, and fewer of them flagged by a scan detector.}
  \begin{itemize}
    \item Result: lower attack rate, higher attack confidentiality
    (Table~\ref{tab:unopposed-summary}).
    \item Why: unmapped tactics take time and dispatch no attack action, so
    they space out the attack actions the detector counts.
    \begin{itemize}
      \item Instance: the unmapped share orders all three. $c_3$ has the most
      (47\,\%), the lowest attack rate and the highest attack confidentiality;
      $c_4$ the least (26\,\%), and the reverse; $c_1$ and $c_2$ between
      (Figure~\ref{fig:aio-coverage}(a)). $c_3$ is the far end of the
      mechanism, not an exception.
      \item Stealth itself is unmapped (10 to 16\,\% of steps): the quiet comes
      from its time, not from hiding. (EXAMINER)
    \end{itemize}
    \item Bound:
    \begin{itemize}
      \item No detector: nothing in MTDSim watches the attacker
      (Section~\ref{subsec:tactic-verb-mapping}), so detection is read by
      proxy, through Snort's default scan rule.
      \item That rule counts a rate, so attack rate and attack confidentiality
      are one effect read twice; the claim is the ordering, which holds at six
      of nine detector settings (Appendix~\ref{app:sensitivity}). (EXAMINER)
      \item The spacing follows from declared tactic durations, not a choice
      to avoid detection, so property~5 is not met
      (Section~\ref{sec:fidelity-verdict}).
    \end{itemize}
    \item Compare (Marc 2026-10-07): Tay models detection by proxy on the
    defender's side, feeding his agent a varying share of the attacker's
    actions \citep{tay2024}; here the proxy is on the attacker's side. Neither
    closes the loop from detection to an MTD deployment
    (Section~\ref{sec:future-work}). CHECK antecedent: Tay's detection-rate
    experiment is only in the MTDShield appendix, not chapter 3.
  \end{itemize}
```

**The precondition CHECK, closed.** At 1 000 seeds, the share of the APT attacker model's attack actions that fail on an unmet precondition is c1 14 %, c2 27 %, c3 30 %, c4 28 %. Paragraph 2 gives the mechanism only (chapter 4's), so it needs no number.

**Marc's question for paragraph 2: what happens in a successful run that does not happen in a failed one?** This was a one-off analysis (NOT IN CH5; the scripts were not kept). It ran on `ch5_s531_unopposed/runs_reported.jsonl`, plus IP shuffle and service diversity at 200 s, grepped from `ch5_defended/runs_reported.jsonl`.

- *With no MTD, pace and tactic mix do not separate success from failure.* Within each attack profile, successful and failed runs have the same attack rate, unmapped share (e.g. c1 36 against 37 %) and lateral-movement share. Successful runs land their first compromise earlier (c1 1 686 against 2 492 s; c4 1 471 against 2 055 s).
- *The network the seed draws decides most of it.* Every attacker runs on the same 1 000 networks. Each profile's ASP on the seeds where the baseline attacker succeeds is 0.06–0.20; on the seeds where it fails, it is 0.000–0.017. Any two profiles succeed on the same seed 3–6× more often than chance (e.g. c3 and c4 on 14 seeds, against 2.4 expected). **The luck is the network, not the timing.**
- *The baseline attacker's failed runs are wide, not slow.* They compromise more hosts than its successful runs (26.6 against 24.0) and never reach a target.
- *Marc's MTD-timing hypothesis is not supported* ("the successful runs dodge the deployments"). Under service diversity at 200 s, the share of attack actions an MTD deployment interrupts is the same in successful and failed runs (c1 15.5 against 15.1 %; c2 17.5 against 18.0 %; c3 23.3 against 24.1 %). The runs that succeed sit mostly on seeds that also succeed with no MTD (33–100 %, against 4–12 % for failed runs). Under IP shuffle at 200 s no APT run succeeds at all, so the hypothesis cannot be tested there. Successful-run counts under MTD are thin (2–33).
- *Where it could go (Marc's call):*
  - an appendix "what a successful run looks like" (Supplementary results), with paragraph 2's optional sentence (in its DRAFT STATE comment);
  - or future work: which network features (the target's exposure, path length) decide success. That needs the network regenerated from the seed, which was not done here.

  Marc's real-world reading is a side channel: an attacker that learns the deployment interval and times its attack actions around it. That is deployment-strategy awareness (property 8), which the APT attacker model does not have. So it belongs in future work, not in a finding.

### 11c. 6.1 paragraph 3 drafted (2026-10-08); point 2 retired

**Point 2, retired verbatim** (ratified by Marc: "seems about right"). Its candidate "success given undetected" is registry item B7.

```latex
  \item \textbf{It compromises less by the time limit; the runs that reach a
  target reach it only just later.}
  \begin{itemize}
    \item Result: ASP and NCR well below the baseline attacker's; MTTC only
    just longer, and $c_3$'s overlaps the baseline attacker's
    (Table~\ref{tab:unopposed-summary}).
    \item Why:
    \begin{itemize}
      \item the same unmapped time leaves fewer attack actions in
      15\,000\,s;
      \item attack actions dispatched in its tactics' order, not the baseline
      attacker's procedure, find a precondition unmet and fail
      (Section~\ref{subsec:runtime-mechanics}). (CHECK: 14--28\,\% at 100
      seeds.)
    \end{itemize}
    \item Bound:
    \begin{itemize}
      \item read at the 15\,000\,s time limit (Table~\ref{tab:experiment}); a
      longer campaign was not run;
      \item MTTC is over the runs that reach a target, 42 to 139 of 1\,000
      against the baseline attacker's 656, so it compares the fastest
      successes (EXAMINER);
      \item ASP scores the target host for both attackers; the attack
      profiles' own objectives (collection, exfiltration, impact) are
      unmapped (Section~\ref{subsec:tactic-verb-mapping}), so whether an
      attack profile meets its objective is not scored (EXAMINER, new; to
      Section~\ref{sec:threats}, construct);
      \item the frame for every outcome claim (Marc 2026-10-08): the attack
      flows record campaigns that were detected, mostly succeeded and were
      reported (Section~\ref{subsec:failure-matrix}); how often APTs fail, or
      go undetected, is not in the record. No claim on which attacker is more
      successful in the world: the claims are on the mechanisms modelled and
      the outcomes seen in MTDSim.
      \begin{itemize}
        \item Candidate (Marc; appendix or Section~\ref{sec:future-work}):
        for each attacker, the share of its successful runs that stayed
        undetected. Not computed; it needs a per-run detection rule, a new
        metric.
      \end{itemize}
    \end{itemize}
    \item So:
    \begin{itemize}
      \item an APT is defined by persistence toward an objective, not by speed
      (Section~\ref{subsec:apt}); the APT attacker model is not competing with
      the baseline attacker, which is the reference;
      \item ASP and NCR alone read a quiet attacker as a weak one
      (Section~\ref{sec:evaluation-implications}).
    \end{itemize}
  \end{itemize}
```

**Paragraph 3 notes.**
- The term "attack path" is replaced by "opening" (§4.5's rename).
- "Not a strategy chosen against the defender" is replaced by the cost–benefit bound. The old wording read against Table 6.1's "choice of attack strategy, in full".
- The prose leans on the attack-action recount, now registry A3. It needs a ch5 footnote, or the clause goes.

**Network structure, Marc's future-work idea** (registry F3): which network features decide success; adversarial network structures; construction principles portable to other simulators. Check the literature first (network hardening, attack-graph-based network design) before calling it a field.

### 11d. 6.1 paragraph 4 drafted (2026-10-08); points 3 and 4 retired; 6.1 is prose only

**Points 3 and 4, retired verbatim** (with the "[Points for dictation]" line):

```latex
\noindent\emph{[Points for dictation, reading Section~\ref{sec:attacker-in-operation}.]}
\begin{itemize}
  \item \textbf{The baseline attacker gives MTD one attack path to defend
  against; the APT attacker model gives it hundreds.}
  \begin{itemize}
    \item Result: one shared opening over four steps, then one branch, against
    179 to 947 distinct openings over eight steps
    (Figure~\ref{fig:aio-coverage}(b)).
    \item Why: weighted choice at the Petri net's decision places, over the 5
    to 19 attack flows of each attack profile.
    \item Bound:
    \begin{itemize}
      \item The two are counted in different units: the APT attacker model's
      steps are tactics, the baseline attacker's attack actions. Counted by
      attack action, the attack profiles still have 190 to 844 against 3.
      (EXAMINER; one-off check, NOT IN CH5: one clause, or a ch5 footnote.)
      \item The count is capped by the runs: $c_1$'s 947 is near its 1\,000.
      \item Variety in proportion to how often the attack flows took each
      step, not a strategy chosen against the defender.
    \end{itemize}
    \item So: an MTD evaluated against the baseline attacker is tested on one
    attack path; Section~\ref{sec:disc-mtd-performance} reads what MTD does
    against many.
  \end{itemize}

  \item \textbf{The attack profiles differ from one another, but less than all
  four differ from the baseline attacker} (secondary).
  \begin{itemize}
    \item Result: ranges in ASP, NCR and attack confidentiality
    (Table~\ref{tab:unopposed-summary}) and in distinct openings
    (Figure~\ref{fig:aio-coverage}(b)).
    \item Why: each divides its steps over the tactics its attack flows reach
    (Figure~\ref{fig:aio-coverage}(a)).
    \item Two instances, each HYP (Marc 2026-10-08; one-off checks, NOT IN
    CH5):
    \begin{itemize}
      \item $c_4$ has the highest attack rate of the four and the lowest ASP.
      It tries the most exploits, and two-thirds find a precondition unmet,
      the most of any attack profile: an exploit needs a port scan first
      (Section~\ref{subsec:runtime-mechanics}), and across the four the share
      follows how often each exploits per port scan. Candidate cause: $c_4$
      rests on five attack flows. Bound: $c_1$ makes as few successful
      exploits per run and reaches the target three times as often, so this
      is not the whole story.
      \item ASP and NCR rank $c_1$ and $c_3$ oppositely. $c_3$ compromises more
      hosts than $c_1$ whether or not it reaches a target: breadth against
      depth. ASP needs one of two target hosts; NCR counts every host
      (Section~\ref{subsec:metrics-outcome}).
    \end{itemize}
    \item Carries under MTD (Marc): $c_3$, the slowest, is furthest from the
    baseline attacker from 500\,s (Figure~\ref{fig:eff-suppression-profiles});
    explained in Section~\ref{sec:disc-mtd-performance}.
    \begin{itemize}
      \item Bound (checked): $c_3$ only. The other three move together and do
      not follow their attack rates (service diversity at 500\,s: $c_2$ 0.20,
      $c_4$ 0.24, $c_1$ 0.28).
    \end{itemize}
    \item Bound: whether the objective or the partition's size causes the
    differences is the random-partition ablation's
    (Section~\ref{sec:fidelity-verdict}).
  \end{itemize}
\end{itemize}
```

**Marc's hypothesis for paragraph 4, tested and not supported** (registry B12). The hypothesis: the profiles' ASP follows how closely their attack actions keep to the baseline attacker's moves.
- *Move set:* the 12 transitions the baseline attacker takes with no MTD, after collapsing repeats. These match Figure 2.3.
- *Per run:* attack actions only (unmapped steps dropped), consecutive repeats collapsed, then the share of consecutive pairs that are baseline moves.
- *Results by profile* (moves followed / unmet-precondition share / ASP): c1 45.8 % / 14.5 % / 0.12; c2 39.2 / 26.9 / 0.14; c3 46.8 / 29.8 / 0.06; c4 39.4 / 28.3 / 0.04.
- *Within each profile,* successful and failed runs follow the moves equally (c1 45.8 against 45.8; c3 44.9 against 46.9). The correlation with the unmet-precondition share is −0.19 to +0.16.
- *Why it fails:* a precondition is state left by any earlier step, not only the step just before, so a pairwise test is too coarse. The finer reading, exploits per port scan (11a), stays as paragraph 4's hypothesis for c4. It is readable from Figure 5.1(a), so it needs no new number.

### 11e. The happy-path chain test (Marc, 2026-10-08), registry B12

Marc's refinement: test unbroken chains of successful attack actions in the baseline attacker's order, not single steps. No-MTD corpus; unmapped steps dropped (they leave the attacker's state untouched). A chain is a maximal run of successful attack actions, each linked by a baseline move or a repeat. A strict happy chain is enumerate → port scan → an exploit that compromises, all successful and consecutive. The script is at the session scratchpad only, so it is not kept; re-runnable from this definition.

| | mean chain | share of actions in chains of 3+ | longest | happy chains / run | ASP |
|---|---|---|---|---|---|
| c1 | 1.55 | 26 % | 5.5 | 0.27 | 0.12 |
| c2 | 1.66 | 34 % | 5.5 | 0.32 | 0.14 |
| c3 | 1.64 | 32 % | 5.3 | 0.72 | 0.06 |
| c4 | 1.31 | 12 % | 4.0 | 0.08 | 0.04 |
| baseline | one chain per run | 100 % | — | ~19 | 0.66 |

- **Supports c4.** It has the shortest chains and the fewest happy chains, and the lowest ASP. This agrees with paragraph 4's exploit-per-port-scan reading.
- **Does not explain c3** (most happy chains, second-lowest ASP), **or c1 against c2.**
- **Within each profile, chains do not separate success from failure.** Success against failure: c1 mean chain 1.57 against 1.55; c3 happy chains 0.59 against 0.73. So within a profile, the network decides (B1).
- **Marc's "3–4 actions" threshold** is never reached on average: no profile's mean is above 1.7, and the longest chains are 4–5.5.

No prose change. Paragraph 4's c4 sentence ("the cause is likely order") now has two agreeing readings behind it.

### 11f. The ideal tactic graph (Marc, 2026-10-08), registry B13

**Marc's ask:** translate the baseline attacker's state machine into a tactic graph through the tactic-to-action mapping (an edge where the two attack actions are a baseline move), measure each profile's overlap with it, and find the one-liner for why c1 and c2 succeed more.

**Method.**
- *Ideal graph:* 24 directed edges among the 8 mapped tactics. A pair counts when its attack actions are one of the baseline attacker's 12 moves (§11d) or the same attack action.
- *Effective edges:* each profile's net from `data/ogasp/petri/*_structural.json`, with weights > 0. A mapped tactic's next mapped tactic is found by walking through unmapped places, which leave the attacker's state untouched.
- The script is at the session scratchpad only, so it is not kept; re-runnable from this definition.

| | ASP | effective ideal edges / 24 | P(next follows an ideal edge): dedup / raw / runs | transitions (w > 0) | direct ideal edges |
|---|---|---|---|---|---|
| c1 | 0.12 | 23 | 0.54 / 0.53 / 0.52 | 74 | 17 |
| c2 | 0.14 | 15 | 0.51 / 0.51 / 0.49 | 43 | 6 |
| c3 | 0.06 | 12 | 0.55 / 0.55 / 0.56 | 47 | 6 |
| c4 | 0.04 | 10 | 0.43 / 0.45 / 0.48 | 39 | 8 |

**Reading (HYP).**
- Only the effective coverage separates ASP's two groups: c1 and c2 against c3 and c4. Their CIs are apart.
- Probability, size and direct edges do not.
- So **ASP follows how many of the baseline attacker's moves a profile's net can make, not how often it makes them.** More such edges give more ways to rebuild the state an exploit needs. Within a profile, the network decides which runs succeed (B1). So the coverage plausibly sets how many networks a profile can exploit.

**Bounds.**
- Four points.
- The 15-to-12 step between the groups is small.
- c1's 23 partly reflects its 19 attack flows. But c2 and c3 both have 7 flows and still differ (15 against 12).

**Use:** no prose change. This is the strongest candidate to replace paragraph 4's two "likely" sentences, if it gets a home (a column beside the profile-edges figure, or a chapter 5 sentence).

### 11g. What decides success, by level (synthesis, 2026-10-08)

Marc asked which levers matter most. The no-MTD corpus answers at three levels:
1. **APT attacker model against the baseline attacker:**
   - unmapped time (fewer attack actions by the time limit);
   - precondition failures, because the attack actions encode one order (paragraphs 2–3).
2. **Between attack profiles:** how many of the baseline attacker's moves a profile's net can make (B13, HYP). This explains only the two-group split, c1 and c2 against c3 and c4. That is all the ASP intervals separate: c1 against c2, and c3 against c4, overlap.
3. **Within an attack profile:** the network the seed draws (B1). Pace, tactic mix, chains and interruption by MTD do not separate successful from failed runs (B2, B12).

**Marc's ratio check.** Coverage over net size (23/74, 15/43, 12/47, 10/39) mixes units: the ideal edges are effective mapped edges, while the transitions include unmapped places. In consistent units (ideal over effective mapped edges: 48, 43, 55, 45 %) the share does not order ASP. **It is the count of usable moves that matters, not the share.**

**Interpretive link** (for paragraph 4 if B13 gets a home): plurality costs success (paragraph 3), and the attack profiles that keep more of the attack actions' moves pay less.

## 12. 6.3: the grading rule, rebuilt bottom-up (2026-10-08, RATIFIED)

**Marc's rulings (2026-10-08):** the two-layer rule is ratified ("honest and clear"); 2 and 4 go to P; 5 goes to P ("we model stealth by proxy"); the 5.4 "six to ten" sentence is fixed. The stale counts elsewhere (ch1, ch4, 6.1 P1, 7.1, the criterion doc) are NOT to be propagated yet: "I want to get this right first". Table 6.1's row follows when 6.3 is drafted.

Marc: "start with being transparent about our rules ... then regrade ... imagine the [current marks] don't exist ... grade by merit"; "how do our ablations feed into this"; "is compromising more the right metric ... we look at relatives".

Two cold examiners ran on 6.3's floats: the first on the floats only, the second on chapters 3–4 as well (packets examiner_6_3_packet{,2}.tex in the session scratchpad). Every claim below was checked against the tex.

**Defects found and fixed (00cb3f0f):**
- In 5.4, a comment line had swallowed the start of the sentence "Under IP shuffle and OS diversity"; the line break is restored.
- Table 6.1 moved to the head of 6.3.

**The proposed rule: two layers.**
1. **The mark** (the cells of Table 6.1, comparable across all four rows):
   - Chapter 3's rule, verbatim, scored from the method text alone (chapter 4 for ours, the papers for theirs). Tick: does all the definition says. P: does part of it, or a fixed rule or an assumption sets the behaviour. Cross: neither.
   - The caption's carve-out ("for the APT attacker model a tick marks a property the model implements") is deleted.
   - Our own evidence may LOWER a mark (a component that fails to produce its behaviour), never raise one. The comparators had no such check, so this is stricter on us, not looser.
2. **The evidence** (our row only, never folded into a mark; the comparators are "not tested"):
   - **Built:** the chapter 4 component.
   - **Seen:** a chapter 5 behaviour metric.
   - **Consequence:** does removing the component change the evaluation's answer, i.e. NCR reduction and which MTD mechanism is most effective? Absolute NCR is not used: "compromises more" measures strength, not fidelity (Marc), and chapter 4's opener asks whether the attacker "changes what an MTD evaluation measures".
   - Mirrors apt_model_criterion.md's badges and its Row B (evaluative consequence), which Table 6.1 had collapsed.

**The regrade, under layer 1 (the session's and the blind examiner's, agreeing):**

| # | Now | Regrade | Why (chapter 4, against chapter 3's comparator evidence) |
|---|---|---|---|
| 1 Persistence | ✓ | ✓ | the same loop as the baseline attacker's tick (column consistency); "extended period" is a bound, not a mark |
| 2 Objective-specific | ✓ | **P** | the route differs by objective, but exfiltration and impact are unmapped: no attack action after the foothold acts on the objective. This is the baseline attacker's P reason verbatim (and Kim's). Ours does more within P |
| 3 Choice of strategy | ✓ | ✓ | a weighted draw among several CTI-derived sequences; Masud's P was "every path, none chosen". Counted by attack action, still hundreds (A3, which now serves this too) |
| 4 Adaptivity | ✓ | **P** | the failure matrix is nine rules plus a distance factor, set by judgement (a fixed rule); it reads the verdict, not the MTD disruption; it is inert in unmapped tactics and after c2's failed initial access. The baseline attacker's P is "a fixed rule sets its response" |
| 5 Detection avoidance | ✗ | **P?** | Kim's P is evasion assumed with no detector. Ours: chapter 4 sets execution and defense impairment "paced to stay hidden" (an assumption), and pace is measured by proxy (5.2). Column consistency gives P; a strict "chooses" gives ✗, and then Kim's P must be revisited too (re-opens ch3) |
| 6 Cost–benefit | P | P | the RoA order is kept: the APT attacker model dispatches MTDSim's exploit, and host.get_vulns sorts by RoA (verified) |
| 7 Learning | P | P | the vulnerability memory learns vulnerabilities, not MTD deployments |
| 8 Deployment awareness | ✗ | ✗ | "can neither see nor change the MTD schedule" (4.4.1) |

Count: two in full (one kept, one built), five in part, one not met, against the field's at most one in full. Before the regrade: four in full and two in part.

**What the ablations do under the rule:**
- **Layer 1 (manipulation check, can only lower a mark):** all three components pass. The attack profiles' tactic mixes differ (Figure 5.1); the failure matrix's return to reconnaissance runs .76–.83 against .08–.10; the vulnerability memory's exploit success share is .73 against .69. No mark falls.
- **Layer 2 (consequence, B15):** no component changes which mechanism is most effective. The attack profiles shift NCR reduction by up to 14 points (IP shuffle at 1 000 s: 58 against 44 %); the failure matrix and the vulnerability memory shift it by at most 2 points. So contribution 2 does not rest on the judgement-set components. What it does rest on is 6.1's: unmapped time and order (and chapter 4 already says NCR rests most on the 45 s duration).
- **The attack-profile pair, reread (B14):** below the attack graph and above the random partitions. Random groups lose NCR with size (19 flows: median .181; 5 flows: median .120, minimum .022), while c2 (7 flows, .209) and c4 (5 flows, .154) do not, so grouping by objective keeps small groups working (HYP; B13's count is the test). Neither result is fidelity. The case for the split is the profiling assumption (objectives differ, chapter 4) and Figure 5.1, and the attack graph breaks that assumption by mixing objectives (Marc).
- **A caution the examiner raised:** random partitions 5 and 6 beat the attack profiles under IP shuffle at 200 s (d −0.48, −1.03, both not negligible). The 5.4 sentence "not negligible against six to ten" counts both directions.

**Blast radius if ratified** (rule on merit; this overturns the 2026-10-05 "honest claim" count of four in full):
- Table 6.1's row and caption;
- ch1 contribution 1 ("four in full and two in part");
- ch4 opener ("built for four ...: objective-specific behaviour, choice of attack strategy, adaptivity and, in part, learning"), and 4.4.3's "gives ... adaptivity, property 4";
- 6.1 paragraph 1 ("detection avoidance not met") if 5 becomes P;
- 7.1 contributions;
- apt_model_criterion.md's scorecard.

The abstract states no count.

**The examiner's other front-of-mind questions** (for 6.3 or 6.5):
- The corpus is not APT-only (18 of 38 flows attributed, criminal groups among them, one adware campaign), so the marks describe attackers reported in CTI. This is already stated in 4.1 and points to 6.5.
- "Extended period" against tactic durations of seconds and the time limit (a 6.1 paragraph 2 bound).
- Which component produces the gap to the baseline attacker (answered by B15 plus 6.1).

### 12a. 6.3 point set rebuilt (2026-10-08); Marc's answers to the examiner's questions, and where each went

Marc's answers (short): he scored the row and checked it, and a blind reader agreed. The marks were changed after the results. Not all eight properties are equally important, but they are presented as equal ("that's the literature review's question, not the discussion's"). He doesn't know whether a weighted draw counts as choosing. On the ceiling, there are two parts, the attack actions and the drivers; upgrade the attack actions and most marks lift, but an FSM caps plurality. Grounding in real data is assumed good and is not one of the eight. The properties may pull against each other, so the criteria are incomplete; threat modelling and MTD barely meet (future work). Properties without a chapter 5 metric: some are implicit by construction, some are not modelled, and this is worth saying. The Petri net is the data structure, so it can't be ablated. More marks, but a small sliver. The properties are those of any skilled, persistent attacker joined to the APT definition: neither complete nor APT-specific, and a model with all eight evaluates MTD above the current standard. The mapping is declared by logic, after a total mapping was tried. On objectives in outcome, the profiles should behave in line with their objectives: exfiltration and impact need the target's data, while pre-positioning doesn't.

Routed:
- **6.3 points:** the rule and the transparency line; persistence and choice in full (the draw follows frequency, with reasoning left to property 6); one token means a stochastic choice among tactics, so the mark is earned by the CTI branching, not the formalism; each in-part mark with its stop; the seen rung (metric / by construction / not modelled); the ablations (behaviour check, consequence on NCR reduction, the profile pair, the baseline attacker as the driver's "without"); the two-part ceiling; what the marks mean.
- **6.5 construct:** the yardstick's limits; the mapping declared by logic (Appendix B total mapping: 0.15 against 8.13 hosts).
- **Registry:** F7 (threat modelling into MTD), F8 (FSM against Petri net on the same attack actions; multi-token), F9 (upgraded attack actions).

**Session correction to Marc's c4 reading:** c4 is not mainly pre-positioning. Section 4.2 says three of its five attackers were removed before they acted, one positioned itself for future operations, and one ran adware. So c4's low ASP fits campaigns cut short. c3 (ransomware, which needs the data) is the one that does not fit the objective logic. This goes in 6.3 as "seen in outcome, in part", with a CHECK against Table 5.2, pointing back to 6.1 paragraph 4.

**Process note (Marc):** "now you're just attacking me"; "these are questions about the literature review, not specific to the discussion". Pose only questions the section's own floats raise; questions that re-open an earlier chapter's settled choices go to 6.5 as one line, not to Marc.

Retired point set (pre-rule), verbatim:

```latex
\noindent\emph{[Points for dictation, reading Table~\ref{tab:fidelity-verdict}
and Section~\ref{sec:ablation}.]}
\begin{itemize}
  \item \textbf{The eight properties were fixed from the literature before any
  attacker model was scored, and the APT attacker model is scored by the same
  rule as the three of Table~\ref{tab:attacker-cross-section}.}
  \begin{itemize}
    \item The three rows are Table~\ref{tab:attacker-cross-section}'s. The
    properties are a census, not a scale: more marks is not a better model.
  \end{itemize}

  \item \textbf{No MTD attacker model scored has more than one property in full;
  the APT attacker model has four, and two in part.} (Chapter 1, contribution 2.)
  \begin{itemize}
    \item In full: campaign persistence (kept from the baseline attacker),
    objective-specific behaviour, choice of attack strategy, adaptivity. In
    part: cost--benefit reasoning (kept) and learning
    (Table~\ref{tab:fidelity-verdict}). The only one built from CTI.
  \end{itemize}

  \item \textbf{Of the three components that rest on judgement, only the attack
  profiles change what the attacker achieves.}
  \begin{itemize}
    \item Result: without the attack profiles the APT attacker model compromises
    more; with them it compromises more than with any of ten random partitions
    of the same sizes (Section~\ref{subsec:ablation-attack-profiles},
    Table~\ref{tab:ablation-random-partitions}).
    \item Expected the reverse: the attack profiles drive MTDSim's six attack
    actions, so much of each objective's behaviour could be lost where the model
    joins MTDSim.
    \item Read: sorting the attack flows by objective changes the outcome beyond
    what the partition's sizes explain. (CHECK against Table~\ref{tab:ablation}
    after the 2026-10-07 redraw.)
    \item So: one attacker built from every attack flow does not stand in for
    attackers with one objective (Section~\ref{sec:evaluation-implications}).
  \end{itemize}

  \item \textbf{The failure matrix and the vulnerability memory operate and
  change no outcome, because MTDSim's attack actions already decide it.}
  \begin{itemize}
    \item Failure matrix: changes where the attacker goes after a failure, not
    its NCR (Section~\ref{subsec:failure-matrix}, Table~\ref{tab:ablation}).
    Why: an attack action without a foothold already fails its precondition,
    and the failure matrix only reweights the moves the attack flows give, so
    it picks the next documented move.
    \item Vulnerability memory: raises the share of exploits that succeed, not
    NCR, even with one service per operating system
    (Figure~\ref{fig:ablation-memory}). Why (HYP, CHECK at 1\,000 seeds): a host
    usually takes a second visit, after a port scan finds its next service; the
    detour costs time, not the odds.
    \item So: reported so others need not repeat them. The next gain is in
    MTDSim's attack actions, not the attacker's decisions
    (Section~\ref{sec:future-work}).
  \end{itemize}

  \item \textbf{Two properties come with the baseline attacker's attack actions,
  and learning is met in part.}
  \begin{itemize}
    \item Campaign persistence: it carries on through every disruption, and
    MTDSim never takes a compromise back. Cost--benefit reasoning: the exploit's
    order by RoA only. Learning: it learns vulnerabilities, not the MTD
    deployments it observes, the same partial Table~\ref{tab:attacker-cross-section}
    gives the baseline attacker.
  \end{itemize}

  \item \textbf{Detection avoidance and deployment-strategy awareness are not
  met, each for a reason MTDSim sets.}
  \begin{itemize}
    \item Detection avoidance: the spacing is measured
    (Section~\ref{sec:disc-behaviour}); the detector is missing.
    Deployment-strategy awareness: needs inference about the schedule, and
    MTDSim's near-periodic schedule would make it learnable. Both to
    Section~\ref{sec:future-work}.
  \end{itemize}

  \item \textbf{What the capture licenses.}
  \begin{itemize}
    \item 38 attack flows give an envelope of documented behaviour, not one
    named group; the model can only be as good as the attack actions it adopts
    (Section~\ref{subsec:tactic-verb-mapping}).
  \end{itemize}
\end{itemize}
```

### 12b. Marc on one token and on "is a draw a choice" (2026-10-08)

- **One token:** the Petri net can extend to more tokens (attack actions run at once) and to the scheduling of tactics. One token was kept to keep the results reasonable, and because the attack actions are not "thread safe". Verified: MTDSim's adversary keeps one context (adversary.py:84, 206–215: curr_host, curr_ports, curr_vulns), so two tokens would overwrite each other's exploit precondition. Section 4.3 gives only the behavioural reason (one line of the campaign at a time); the CHECK sits in the 6.3 points (the structural reason may belong in 4.3, not to be propagated yet).
- **Is a draw a choice?** It is the difference between simulation and emulation (ch2, subsec:evaluation-methods). An emulation replays one incident step by step. A simulation draws from the envelope, so no attack strategy is hard-coded into an attack scenario, and a run may splice several attack flows into a campaign no attacker ran ("frankenstein"), which gives plurality and flexibility.
- **Routed:** 6.3 choice sub-points (the draw as simulation's gain; the formalism's room to extend; the structural reason for one token); 6.5 scope (one token: no attacker acting on several fronts); 6.5 external (a run is a draw from an envelope, not a replay); registry F8 extended (per-token context, then scheduling).
- **Ruling:** the full mark on choice of attack strategy is KEPT.

### 12c. 6.3 condensed to three paragraphs; Marc on adaptivity, the statistics, the memory, plurality (2026-10-08)

**Marc's answers:**
- **Adaptivity is seen by construction.** The verdict returns success or failure (Figure 4.x, step 4). On failure the token must go back, or to an adjacent place, and re-run (e.g. the port scan before the exploit). On success it moves on. "The failure itself is the biggest impactor, a method choice." He suggests an example run, without MTD and with it, as an appendix item (registry B18).
  - *Checked:* without the failure matrix, the Petri net routes failure and success alike (5.4: "by the base weights, as it does after a success"). The difference comes from MTDSim's state: a failed attack action leaves its precondition unmet. That is a forced response, not a choice, so adaptivity stays in part.
  - The same point explains B16: time lost per MTD deployment does not move without the failure matrix, because the failure itself carries the cost.
- **Statistics:** Table 5.4 prints NCR as point values, plus d with its interval. NCR's own interval is narrower than the printed precision (ablation_table.py: half-width 0.0004–0.0026 at 1 000 seeds). B15's ranking has no test, so claim the rank only where the lead exceeds the interval.
- **Vulnerability memory:** "we tried this idea, it didn't work." It is a measured negative.
- **Plurality:** the attack profiles reduce it (B17), but the attack graph mixes objectives. True plurality would let any tactic lead to any of the other 14, weighted. Ours is bounded by what the reports document.

**Routed:** three paragraphs.
- P1: the rule and the verdict, with transparency and the frame.
- P2: what stops each mark is the ceiling; in full; stopped by the attack actions; stopped because nothing decides; how each is seen; the so-what (upgrade the attack actions).
- P3: the ablations, as behaviour check, adaptivity (B16), the memory as a measured negative, consequence (B15), and the profile pair (B14, B17).

Registry B18 is added.

Retired six-point set (2026-10-08, pre-condensation), verbatim:

```latex
% 2026-10-08 POINT SET REBUILT on the ratified two-layer rule (handoff 12, 12a):
% the mark is chapter 3's rule from the method text; our evidence may only lower
% it; the evidence ladder (built / seen / consequence on the evaluation's
% answer) is reported beside the mark, never folded into it. The old points are
% in handoff 12a. Table 6.1's row and caption updated to the regrade 2026-10-08.
\noindent\emph{[Points for dictation, reading Table~\ref{tab:fidelity-verdict}
and Section~\ref{sec:ablation}.]}
\begin{itemize}
  \item \textbf{The rule, and what it gives: two properties in full, five in
  part, one not met; no other MTD attacker model scored has more than one in
  full.}
  \begin{itemize}
    \item The eight properties were fixed in Chapter~\ref{ch:litreview} before
    any attacker model was scored. Our row is scored by
    Table~\ref{tab:attacker-cross-section}'s rule, from
    Chapter~\ref{ch:attacker-model}'s text, as theirs were from their papers.
    \item Our runs may lower a mark, never raise one: the other three had no
    runs to be checked against.
    \item Marc scored the row; a blind reader under the same rule agreed (the
    AI Use Declaration names the reader).
    \item Transparency: the first draft marked what the model implements.
    Scored by the rule, objective-specific behaviour and adaptivity fall to in
    part.
  \end{itemize}

  \item \textbf{In full: campaign persistence, kept, and choice of attack
  strategy, built.}
  \begin{itemize}
    \item Persistence: the same loop that earns the baseline attacker its
    mark. Seen by construction, with no metric.
    \item Choice: a weighted draw among the sequences the attack flows
    document; counted by attack action, still hundreds (registry A3). The draw
    follows documented frequency, not reasoning; reasoning is cost--benefit's.
    \item Is a draw a choice? (Marc 2026-10-08) It is what simulation buys over
    emulation (Section~\ref{subsec:evaluation-methods}). An emulation replays
    one incident step by step; a simulation draws from the envelope of every
    attack flow with the objective, so no attack strategy is hard-coded into an
    attack scenario, and one run may join parts of several attack flows into a
    campaign no attacker ran. The envelope is the attack strategies; the draw
    picks one per run.
    \item With one token, the Petri net makes a stochastic choice among
    tactics, which a stochastic finite state machine built from the same attack
    flows could also make: the mark comes from the attack flows' branching.
    What the Petri net adds is room to extend: more tokens for attack actions
    run at once, and the scheduling of tactics. One token was kept because
    MTDSim's attack actions share one context (the current host, its ports and
    their vulnerabilities), so two tokens would overwrite each other's
    precondition (CHECK: Section~\ref{sec:petri-formalism} gives the
    behavioural reason only, one line of the campaign at a time).
    What plurality costs is Section~\ref{sec:disc-behaviour}'s.
  \end{itemize}

  \item \textbf{In part: what stops each one short of in full.}
  \begin{itemize}
    \item Objective-specific behaviour: the route differs by objective
    (Figure~\ref{fig:aio-coverage}), but exfiltration and impact are unmapped,
    so no attack action acts on the objective. This is the baseline attacker's
    reason, word for word; ours does more within in part.
    \item Seen in outcome, in part (Marc 2026-10-08; CHECK against Table 5.2
    before use): the objectives that need the target's data, $c_1$ and $c_2$,
    reach the target host most; $c_4$'s attack flows mostly ended before the
    attacker acted (Section~\ref{sec:attack-profiles}); $c_3$, ransomware that
    needs the data too, does not fit. Point back to
    Section~\ref{sec:disc-behaviour}, paragraph 4.
    \item Adaptivity: the failure matrix is nine rules set by judgement; it
    reads the verdict, not the MTD deployment; it is inert during unmapped
    tactics.
    \item Detection avoidance, by proxy: the pace is assumed to hide the
    attacker (Section~\ref{subsec:dwell-times}) and is measured by two metrics
    (Section~\ref{sec:disc-behaviour}), but no detector exists to choose
    against: the partial mark Kim et al.\ earn for evasion they assume.
    \item Cost--benefit reasoning: the RoA order, kept. Learning:
    vulnerabilities, not MTD deployments. Both seen by construction.
    \item Not met: deployment-strategy awareness; the attacker cannot see the
    MTD schedule. Not modelled, so not seen.
  \end{itemize}

  \item \textbf{The ablations: each component works, and none changes which MTD
  mechanism is most effective.}
  \begin{itemize}
    \item Behaviour check: removing each changes the behaviour it was built
    for (Section~\ref{sec:ablation}); no mark falls.
    \item Consequence, read on the evaluation's measure (NCR reduction), not
    on absolute NCR: compromising more is strength, not fidelity. The attack
    profiles shift NCR reduction but not the most effective mechanism; the
    failure matrix and the vulnerability memory barely shift it (registry B15,
    NEEDS A HOME). So contribution 2 rests on unmapped time and order
    (Section~\ref{sec:disc-behaviour}), not on the components set by judgement.
    \item The attack-profile pair (below the attack graph, above the random
    partitions) is not fidelity either. The split rests on the profiling
    assumption; the attack graph mixes the objectives that assumption keeps
    apart. Size likely costs a random group more than an attack profile
    (registry B14, HYP).
    \item The Petri net's choice has no ablation of its own: the baseline
    attacker, on the same attack actions, is its ``without''.
  \end{itemize}

  \item \textbf{The ceiling has two parts: the attack actions and the driver.}
  \begin{itemize}
    \item The six attack actions cap objective-specific behaviour, adaptivity
    and detection avoidance: no attack action acts on an objective, sees an MTD
    deployment or avoids a detector. A deterministic finite state machine caps
    choice of attack strategy. Cost--benefit reasoning, learning and
    deployment-strategy awareness need decisions neither has.
    \item Upgrading the attack actions under the Petri net would lift the most
    marks (Section~\ref{sec:future-work}).
  \end{itemize}

  \item \textbf{What the marks mean.}
  \begin{itemize}
    \item Properties of a skilled, persistent attacker that two surveys find
    under-modelled, joined to the APT definition: neither complete nor
    specific to APT attackers, and weighed equally though not equally
    important.
    \item An attacker model with all eight would evaluate MTD above the
    standard of recent evaluations; ours has two in full, so much remains.
    \item The table does not score grounding in CTI, which this dissertation
    assumes is good; that claim rests on Chapter~\ref{ch:attacker-model}, not
    on Table~\ref{tab:fidelity-verdict}.
  \end{itemize}
\end{itemize}
```

### 12d. 6.3 paragraph 1 drafted (2026-10-08); P1 retired; a truly blind re-score

- **Correction:** the earlier points said "a blind reader agreed", but that reader was the second cold examiner, and its packet held Table 6.1's marks. So the session ran a truly blind scorer. Its packet (scratchpad blind_score_packet.tex) held chapter 3, 2870–3430, and chapter 4, 3840–5277, with comments stripped and three property claims redacted: chapter 4's opener ("built for four ..."), 4.4.3 ("gives ... adaptivity, property 4") and 4.4.4 ("gives ... learning, property 7, in part").
- **Result:** ✓ P ✓ P P P P ✗, the same as the ratified row. Close calls it named:
  - 3 drops to P if a frequency-weighted draw counts as a fixed rule (Marc's simulation-vs-emulation answer, 12b);
  - 4 rises only if the failure matrix were data-derived or keyed to the MTD disruption;
  - 5 drops to ✗ if a timed delay is not "choosing an action" (Kim picked a concrete action);
  - 6 rests on "the same attack actions" (verified in code: host.get_vulns sorts by RoA).
- **Owed:** the AI Use Declaration (currently empty) must name this use: a language model re-scored the row from chapters 3–4 with the claims redacted.
- **Retired P1 (verbatim):** "P1. Scored by Chapter 3's rule, the APT attacker model has two properties in full, five in part and one not met; no other MTD attacker model scored has more than one in full."
  - Scored by Table 3.3's rule from Chapter 4's text, as the others were from their papers. Our runs may lower a mark, never raise one: the others had no runs to be checked against.
  - Transparency: the first draft marked what the model implements; scored by the rule, objective-specific behaviour and adaptivity fall to in part. Marc scored the row; a blind reader under the same rule agreed (the AI Use Declaration names it).
  - Frame, one clause: eight properties the literature finds missing, not a complete standard (its limits in Section 6.5).

### 12e. 6.3 paragraph 2 drafted (2026-10-08); P2 retired

Retired P2 (verbatim):

```latex
  \item \textbf{P2. What stops each mark short of in full is the ceiling: the
  attack actions, or a decision no part of the model makes.}
  \begin{itemize}
    \item In full. Campaign persistence, kept: the baseline attacker's loop.
    Choice of attack strategy, built: a draw from the attack flows with the
    objective, which is what simulation buys over emulation
    (Section~\ref{subsec:evaluation-methods}); one run may join several attack
    flows. Plurality stays within what the reports document, not any tactic to
    any other; counted by attack action, still hundreds (registry A3). The
    mark comes from the attack flows' branching, not the Petri net: with one
    token, a stochastic finite state machine would make the same draw.
    \item Stopped by the attack actions. Objective-specific behaviour: the route
    differs by objective (Figure~\ref{fig:aio-coverage}), but exfiltration and
    impact are unmapped, so nothing acts on the objective (the baseline
    attacker's reason, word for word; ours does more within in part).
    Adaptivity: a failed attack action leaves its precondition unmet, so the
    attacker must rebuild it; the failure matrix reweights the next tactic on
    the verdict, by nine rules set by judgement, blind to whether MTD caused
    the failure. Detection avoidance: the pace is assumed to hide the attacker
    and measured by proxy (Section~\ref{sec:disc-behaviour}); no detector
    exists to choose against.
    \item Stopped because no part of the model decides. Cost--benefit
    reasoning: the RoA order, kept. Learning: of vulnerabilities, not MTD
    deployments. Deployment-strategy awareness: the attacker cannot see the
    schedule.
    \item How each is seen, one clause: by metric (objective-specific
    behaviour, choice, detection avoidance), by construction (persistence,
    adaptivity, cost--benefit reasoning, learning), not modelled
    (deployment-strategy awareness). An example run, with and without MTD,
    would show adaptivity (registry B18).
    \item So: upgrading the attack actions under the Petri net lifts the most
    marks (Section~\ref{sec:future-work}).
  \end{itemize}

```

### 12f. 6.3 paragraph 3 drafted (2026-10-08); P3 retired; 6.3 is prose only

- **Homes given first:**
  - B15 is a 5.4.1 sentence. The same three MTD mechanisms (IP, host topology and complete topology shuffle) reduce NCR the most with and without the attack profiles, at every interval. The fourth trails by 2.3–26.1 points with and 3.3–23.8 without. It is untested, so the sentence claims the set, not an order.
  - B16 is a 5.4.2 sentence: time lost per MTD deployment is unchanged without the failure matrix (both 2 000 s intervals include zero).
- **Not used:** B14 and B17 have no home, so the random-partition reading is a HYP with no number.
- **Overturned:** "the Petri net's without is the baseline attacker". It is only the nearest comparison, because the baseline attacker also differs in timing and failure response (6.5, internal).

Retired P3 and the itemize shell (verbatim):

```latex
\noindent\emph{[Points for dictation, reading Table~\ref{tab:fidelity-verdict}
and Section~\ref{sec:ablation}.]}
\begin{itemize}
  \item \textbf{P3. Each component works; none changes which MTD mechanism is
  most effective.}
  \begin{itemize}
    \item Behaviour check: removing each changes the behaviour it was built
    for (Section~\ref{sec:ablation}); no mark falls.
    \item Adaptivity: the failure matrix changes where the attacker goes after
    a failure, but not time lost per MTD deployment (registry B16, NEEDS A
    HOME). Likely, the cost of a disruption comes from the failure itself,
    which the attack actions force, not from the reweighting (Marc
    2026-10-08). This is why adaptivity is in part.
    \item Vulnerability memory: built, operates, changes no outcome; a measured
    negative only a model with the capability can report.
    \item Consequence, read on NCR reduction, not absolute NCR: compromising
    more is strength, not fidelity. No component changes the most effective
    mechanism (registry B15, NEEDS A HOME; claim the rank only where the lead
    exceeds the interval). So contribution 2 rests on unmapped time and order
    (Section~\ref{sec:disc-behaviour}), not on the components set by judgement.
    \item The attack-profile pair is not fidelity. The attack graph compromises
    more, and draws more openings (registry B17), because it mixes the
    objectives the profiling assumption keeps apart; size likely costs a random
    group more than an attack profile (registry B14, HYP). The Petri net's
    choice has no ablation of its own: its ``without'' is the baseline attacker.
  \end{itemize}
\end{itemize}
```

## 13. 6.5: six cold examiners, merged and ranked (2026-10-08, NOT RULED)

Marc: "spawn ... a cold really really harsh critical ... examiner of UWA ... chapter specific ... then we can ... rank". Six examiners, one brief
(UWA honours, 80-90 benchmark, harsh but fair, not pedantic; four validity types plus scope; check the text before saying "not addressed";
never shown 6.5 or the registry): ch1-2 framing; ch3 literature review; ch4 method with App B-C; ch5 with App D-E; 6.1-6.4; the whole
argument. Brief and transcripts in the session scratchpad (examiners/brief.md). Verified by the session: Table C.1a (the 45 s band moves
NCR reduction 0.44-0.90 at 200 s and -0.10 to 0.31 at 2 000 s under random; the cells, not stated in any float); End of run is "a target
host compromised, or 15 000 s" (Table 5.1); baseline ASP 5-16x the profiles' (~two thirds of its runs stop early); 6.2's MTDShield
"suggests a policy fitted to that attacker" stands against App D's degenerate inputs; 6.3 P3's "not on the components set by our
judgement" is wrong (the durations and the mapping are judgement) -- the session's sentence, to fix.

All six asked the same first oral question: give the baseline attacker the APT attacker model's idle time (or uniform weights to the
APT attacker model) -- does the reversal survive? If yes, what in the headline is about APTs?

Ranked (n = examiners raising it, of 6):
 1. Cause of the reversal not isolated: pace and order at the seam, not CTI behaviour; no pace-matched or uniform-weight control (6/6).
    Elephant. Partly addressed (6.2 P1, 6.3 P3). The abstract's "grounded in documented behaviour" outruns it.
 2. The headline untested across the judgement-set durations (45 s band; comparison with the baseline attacker not repeated) (4/6). Elephant.
 3. Property counts inconsistent across chapters (ch1 4+2, ch4 "four", 6.1 "does not have" detection avoidance vs Table 6.1) (5/6).
    Major; the propagation already owed.
 4. "APT attacker model" vs the corpus and the run (18/38 attributed, criminal, adware; 4-hour runs; objectives unmapped) (4/6).
 5. Choice of attack strategy in full is a weighted draw; distinct openings rewards any randomness; the net gain is one in full,
    one in part (5/6).
 6. Run ends at a target host compromised: NCR truncated by success for the baseline attacker (~2/3 of runs), censored by the time
    limit for the slow APT attacker model; NCR reduction not on a common footing across attackers (2/6). Not addressed.
 7. Time lost per MTD deployment as adaptivity's metric: drifting counterfactual, the cap, the restart artefact, 2 000 s only, and the
    failure-matrix ablation does not move it; 6.3 says "no metric of their own" vs ch4/ch5 (4/6).
 8. Yardstick and comparators: own rubric, three hand-picked comparators (no game-theoretic or FlipIt-style attacker), P too coarse,
    one scorer plus an LLM re-score of our row only, definitions mirror the components (2/6; the ch3 examiner's elephant). One line
    in 6.5 under the scope limit.
 9. "Identical conditions": action times differ, memory acts on odds vs time, NCR bases 0.17 vs 0.50 (3/6).
10. Ranking statistics: ten dependent items (three mixtures), rho ~ 0 is no agreement not a reversal, rank-1 ties (service diversity
    with port shuffle), bootstrap over correlated runs (3/6).
11. Ablation inference: d standardised near the floor, default +-0.2 bound, d type unstated, 6.3 "read on NCR reduction" vs 5.4's d on
    NCR, ten random partitions give p >= 1/11, partition size confounded (3/6).
12. MTDShield "fitted to that attacker" while its inputs are degenerate (4/6). Fix the 6.2 sentence.
13. Profiles thin, one coder, corpus weights never varied; c4 a residual bin; the leftmost-tactic rule; the overlay share untested (2/6).
14. The tactic-to-action mapping is one judgement; command and control -> scan neighbours carries the pace; only the total mapping tried (1/6).
15. 6.4's implications outrun one network, simulator and corpus (2/6). A constraint on drafting 6.4, not a 6.5 threat.
Below the cut: unreported numbers in 6.1-6.2 (registry A1, A3); a second cause of quietness (refused actions drop out of attack rate);
the inherited restart artefact (unflagged in ch2); post-hoc c3 story; run-level vs seed-level resampling; one network (well bounded).

### 13a. Marc's answers to the fifteen (2026-10-08, dictated; NOT RULED into prose yet)

1. Cause of the reversal. Pace and order are the biggest levers on attack outcome. Pace: MTDSim models no efficiency (no overhead, no
   detection), so the faster attacker (and the faster MTD) wins; in the real world speed raises alarms. Order: a concession of adopting
   Brown 2023's attack actions to keep the project tractable and defensible. The grounding in documented behaviour does choose what runs
   between the attack actions; it is a stepping stone for threat modelling in MTD. Answered in part.
   SESSION READ: holds as a bounded claim. NEW SPINE for 6.5: two roots, both inherited from MTDSim -- the attack actions (order,
   unmapped tactics, mapping) and a simulator that prices nothing (no MTD cost, no detection), so speed wins on both sides.
2. Headline untested across the judgement values. Marc read it as "the headline is not derived"; it is derived (5.3). SESSION
   CLARIFICATION: the ranking is shown at the declared durations only; Appendix C varies the durations on the APT attacker model's NCR
   under random, never the ranking against the baseline attacker. The baseline attacker uses no tactic duration, so only the APT arm
   needs re-running at the band ends. Decision owed: run (APT arm, 45 s band ends, ten MTD options, 200 s) or bound.
3. Counts: "on purpose ... happy for this to be fixed". Propagate.
4. Name and corpus. Major; conceded. Corpus issues (non-exhaustive): sparse; records incidents; not all APT (ransomware, ~20 of 38);
   incomplete; profiled by hand. Without the 20, too few flows. Idea: 18 attributed flows against 38 (appendix?).
   SESSION READ: the 18-flow subset cannot carry four attack profiles; at most an attack-graph-only arm. Future work, not now.
5. Choice of attack strategy. The Petri net offers several sequences of attack actions toward the same objective within a profile;
   an aggregate of documented behaviour, a plausible campaign per objective. Calling it a random draw extends the attack-action
   limitation dishonestly. (Also argued property 2: the profiles' differing post-intrusion edges, e.g. defence impairment in some
   profiles and not others, encode objective-specific behaviour.) SESSION READ: holds for 3 in full by the rule (Table 3.2's wording);
   P2 already carries simulation against emulation. 2 stays in part (the edges differ; the terminal actions on objectives are unmapped).
6. End-of-run rule. NCR reduction is relative within each attacker, normalised so attackers can be compared; MTTC cannot be standardised
   when one attacker is slower; NCR reduction is "the last man standing" despite its flaws. Successful-only / failed-only split as an
   appendix? SESSION READ: within-attacker argument holds for the rankings; 6.2 already shows the reversal on ASP reduction
   (tab:eff-interval-values-asp), which the end-of-run rule does not truncate. That is the answer; no new run.
7. Time lost per MTD deployment. Concern: 2 000 s, not the default 200 s; the first deployment's pull-forward (restart rule) weighs
   against ~6 later ones at 2 000 s but ~74 at 200 s, so negative time lost may be an artefact of the interval choice and "looks like
   a bug". SESSION CHECK (time_lost_first_deployment_numbers.json, on disk): baseline attacker, first deployment -204 to -232 s (every
   mechanism but user shuffle); later deployments (state differs) +19 to +31 s for the four shuffles, +648 s service diversity,
   -21 s OS diversity, -30 s user shuffle. The negative means come from the first deployment. Homes 6.2's "its later deployments cost
   it time" if given a chapter 5 sentence. Adaptivity: answered in part; 6.3's "no metric of their own" to reconcile with ch4.
8. Yardstick: not answered separately; one line in 6.5 (scope rule).
9. "Identical conditions": conceded. The tactic durations were set early, two from MTDSim's constants, the rest by reasoned
   extrapolation; too late to change after the results. Idea: an appendix table of each attack action's baseline time beside the
   tactic durations that drive it. A reusable point: the full set of tactic durations lets others use the APT attacker model as a
   second baseline without re-deriving times (6.4 candidate, modestly).
10. Rankings. A ranking is tied to the simulator's assumptions (how disruption is modelled between attacker, network and defence);
   MTDShield shows the same (it favours service diversity, the baseline attacker's rank 1; NOTE Marc's 96/89 % is 76/70 % in App D).
   User shuffle is weak because vulnerabilities, not credentials, are the currency of MTDSim's attacker. Rankings are used only to show
   that the two attackers' rank 1 do not line up, never as a verdict or to build an APT-optimised MTD. Rant (6.4 / ch7 candidate):
   ranking MTD mechanisms is close to a dead end; the field should move from effectiveness to efficiency, cost and simplicity; MTD is
   unadopted since 2009 because of cost, legacy systems, quality of service, technical debt; "MTD by default" needs frameworks and
   best practice; AI may help integrate legacy attack surfaces. LITERATURE TO CHECK before any claim on adoption barriers.
11. Ablation: the +-0.2 bound is Cohen's default, conceded; d type to state; ablations must be read on NCR reduction. SESSION CHECK:
   d is Cohen's d on per-seed means with the pooled SD, interval by resampling seeds (ablation.py); 5.4 reports d on NCR; 6.3 P3 says
   "read on NCR reduction" -- only B15 (the top-three set) is on NCR reduction. Fix the P3 sentence.
12. MTDShield: keep "as released"; AI models assume their training environment (cite Zhang/Cho, to check). SESSION: soften, not cut.
13. Profile data: conceded; LLMs could synthesise attack flows from APT-only reports with sequence and dependency (Attack Flow now
   ingests threat reports with AI -- TO VERIFY before citing); ATT&CK groups are membership only, no dependency or order, hence
   attack flows; traded volume for specificity. Future work (registry F10).
14. Mapping: one judgement, presented as such; total mapping tried and illogical. Stays.
15. 6.4 unwritten: constraint on drafting.
Authorised now: #3 propagation; "fix up those sentences" (6.3 P3 judgement clause, NCR-reduction clause). HOLD: any mark change
(adaptivity, choice of attack strategy) until Marc has read the session's reading.

### 13b. Applied in chapter 6, and proposals outside it (2026-10-08)

Marc: "every single line that you insert outside of chapter 6, propose to me ... inside chapter 6, I don't really care"; run B19; first-against-later split is ready; no re-run for #7 (the 2 000 s first/later split answers it).
APPLIED in ch6 (commit 3c9c559e and after): 6.1 P1 (detection avoidance in part; refused actions as a second cause of quiet); 6.2 MTDShield
("consistent with ... cannot tell", App D's four zero inputs); 6.3 P2 (adaptivity's metric reconciled); 6.3 P3 (NCR-reduction and judgement
clauses); 6.4 and 6.5 point sets rebuilt; registry B19-B21, F10-F13.
RUNNING: B19 (run_duration_ranking.sh; ~9-10 h from 2026-10-08 23:10; pgid file beside it).
PROPOSED, NOT APPLIED (each needs Marc's yes):
 P1 abstract l.197-198 "under identical conditions" -> "twice on the same networks" [T9]
 P2 abstract l.199-200 + ch1 P6: "service diversity is the most effective MTD mechanism" -> "service diversity and port shuffle are the most effective MTD mechanisms" [T10]
 P3 abstract l.203 + ch1 P6: "by only 36 %" -> "by 36 %" [T3 ch1 examiner]
 P4 abstract closer -> "...against more than one attacker model, including models grounded in documented behaviour" [T1]
 P5 ch1 contribution 1: "four in full and two in part" -> "two in full and five in part" [T3]
 P6 ch4 opener l.3860-3867: the regrade and detection avoidance by pace [T3]
 P7 ch4 time-lost definition: one clause on the counterfactual [T7]
 P8 ch5 5.1 stats: "Cohen's d with the pooled standard deviation" [T11]
 P9 ch5 5.3.1 after l.7538: "After the first, each host-layer and port-shuffle deployment costs it 19 to 32 s." [T7; B20; homes 6.2]
 P10 Appendix C: B19's section and sentence, after the run.
 P11 Appendix B: the durations-beside-MTDSim's-times table (B21), if wanted.

RULED 2026-10-09 (Marc): P1, P2, P3, P5, P6 APPLIED; P4 DECLINED ("that nuance is a bit lost on me"; the closer stays); P7 DECLINED
(the divergence after an interruption is implicit); P8 wording owed ("pooled" disliked; the session to give the right term); P9 APPLIED
as "After the first MTD deployment, each later host-layer or port-shuffle deployment costs it 19 to 32 s"; P10 after the run; P11
APPLIED (tools/attack_action_times_table.py -> tab_B-4b, one Appendix B sentence).

## 14. 6.4: six cold examiners, merged and ranked (2026-10-09, NOT RULED)

Marc: "spawn off critical internal UWA examiners that act on a dimension of this work and pose questions that will elicit an
implication for MTD evaluation ... rank". Brief: scratchpad examiners64/brief.md (questions that draw implications out; three
kinds: earned / overreach / builders; never 9022-9575 except examiner 6). Dimensions: results (ch5, App D-E); MTD evaluation
practice (ch1-3); the simulator's design choices; the method as something others adopt (ch4, App B-C, 5.4, 6.3); the defender's
side and the metrics; the whole argument plus the draft points (may read 6.4 points and 6.5).

Consensus (6/6): a ranking of MTD mechanisms is conditional on its attacker model; report it so and test against more than one.
Must-not-claim (5/6): CTI grounding caused the reversal or gives the "realistic" ranking; (3/6) host layer best against APTs, or
any mechanism or interval recommendation.

VERIFIED by the session (tab_5-3-2d, tab_F-0a NCR and ASP, mtd_scheme.py):
- NCR/ASP sign split: baseline attacker, IP shuffle NCR reduction 0.39/0.30/0.19 at 500/1000/2000 s, ASP reduction -0.09/-0.11/
  -0.10; complete topology 0.09 vs -0.23 at 500 s. App E l.10399-10400 "ASP reduction shows the order of NCR reduction" holds at
  200 s only (outside ch6: a proposal, if wanted).
- Worst case over the two attackers, NCR reduction: IP shuffle highest at every interval (0.88, 0.70, 0.68, 0.39, 0.30, 0.19). ASP
  reduction: service diversity higher from 100 s (0.93 vs 0.78; 0.62 vs -0.09 at 500 s).
- WRONG, corrected in 14a: "Random (pool: the lineage four) ... 0.33 below every member; MTDShield vs random 0.68 vs 0.33,
  0.28 vs 0.75". Random runs over all seven (run_corpus.py _strategies); MTDShield's control is random_four.
- User shuffle: NCR reduction negative against the APT attacker model at every interval (-0.13 to -0.04; ASP -0.34 at 200 s).
  Draft point 2's "barely touches it" understates: it helps the APT attacker model.
- ch4 l.4934: the nine judgement durations were kept under the 200 s default deployment interval (pace set against the interval).

Ranked questions (n = examiners raising it):
 1. Grounding or plurality? Is the case for CTI-grounded attacker models, or for more than one attacker model, given 6.3 puts the
    cause in unmapped time and order (4/6). Abstract closer: P4 DECLINED 2026-10-09; 6.4 can answer it without touching the abstract.
 2. What does the measurement add to Cho's argument that the attacker model decides the optimal strategy (ch3)? (2/6)
 3. Is the ranking the overlap of what each deployment takes and what each attacker depends on, predictable before running? Which
    "findings about MTD mechanisms" are about MTDSim (precondition chain; nothing taken back, so user shuffle and OS diversity
    never get their job; persistence unmapped)? (4/6)
 4. Which metric? NCR/ASP sign split; ASP ceiling for the APT attacker model; MTTC over 20 successful runs; blocks vs time lost
    (4/6; blocks vs time lost covered by draft point 3).
 5. Swapping in an attacker is not drop-in: what must another builder re-derive (mapping, durations anchored on MTDSim's times)
    and check (preconditions, restart rule, the defence's inputs)? Report the tactic-to-action interface (unmapped, refused share).
    (3/6)
 6. Learned strategies: test beside random over the same mechanisms and against an attacker not trained on; check the inputs for
    unobservable steps (4/6). Evidence = the random comparison, not "fitted".
 7. Intervals: no cost so no interval; the lineage's 50-200 s sits at the APT ceiling; sweep until reductions fall away (3/6).
 8. Robust choice: worst case over attacker models, and the metric decides it (2/6). Tension with "never a verdict".
 9. CTI is thinnest where MTD acts (reconnaissance in 10 of 38 flows; no failures in reports) (1/6).
10. Components that change behaviour but not outcome pay only if behaviour is reported (1/6).
11. Mixed strategies cannot be read off their members (1/6).
12. NCR at a fixed time limit measures delay, not prevention, for an attacker that never gives up (1/6; 6.5 P2 bounds it).
Draft-point triage (examiner 6, checked): 1 lead (MTDShield as method, not evidence; "dependence transfers, direction does not");
2 keep, cut "change the rule and the ranking changes" (never run), fix user shuffle, merge 7; 3 keep; 4 trim the adoption claims
(no result, literature unchecked); 5 merge into 1; 6 cut or one clause; 7 merge into 2.

### 14a. Marc's answers to the twelve (2026-10-09, dictated) and the rebuilt 6.4 point set

Marc's answers, condensed (his words in quotes):
- Q1 Grounding or plurality: neither framing. "It's really about looking [at] your own assumptions." CTI limits the assumption
  surface ("it's been observed ... we don't need to assume that"); simulation can aggregate incidents where emulation picks one.
  Plurality is not good in itself: the baseline attacker "was good for its purpose", the APT attacker model for its; neither is
  better. The risk is a learned deployment strategy over-fitting its training attacker, with assumptions "multiple layers down"
  in the metrics it reads (MTDShield's network metrics). Future work (7.2): technique-level graph ablation (cut edges/nodes, read
  NCR/ASP) on a larger corpus, tied to mitigations, so MTD can be built around the most sensitive edge.
- Q2 Cho: right in context; "optimal" is optimal for the simulator, like a model on its training set; a validation/test set from
  the same simulator encodes the same assumptions. Measured here: rank 1 disjoint on one simulator.
- Q3 Prediction: not possible beforehand (many integration assumptions; NCR reduction is relative); only the direction (more
  failure, fewer hosts, slower) and MTDShield. Persistence is unmapped; persistence is emergent (runs to 15 000 s). Accepts: fix
  the user-shuffle example, cut "change the rule and the ranking changes".
- Q4 Metric: NCR reduction for resolution (hosts per run vs one yes/no), ASP's wider intervals and ceiling at 1; reasoning in 4.5.
  Claims the two agree in which attacker is disrupted more.
- Q5 Drop-in: no; the two attackers are for different purposes. A builder supplies mapping, durations, failure handling (4.4's
  loop) and documents each; "we engaged in each assumption in good faith".
- Q6 Learned strategies: should recommend a fixed set of mechanisms rather than choose each deployment (opinion; 7.2). MTDShield
  beat random against the baseline attacker, not against the APT attacker model, on the same simulator.
- Q7 Intervals: the sweep is illustrative; which mechanisms keep disrupting at long intervals; faster always wins while free; an
  ASP reduction of 1 is unrealistic; cost, overhead, QoS are future work.
- Q8 Unknown attacker: IDS-paired, risk-based MTD (a colleague's area) is outside the simulator; otherwise "take the bottom of
  each" (worst case over attacker models) against the overhead an interval costs.
- Q9 CTI thin where MTD acts: the pre-intrusion overlay; MTD's post-intrusion blind spot (e.g. shuffle a database's logical name
  so a foothold's information expires): 7.2.
- Q10 Failure matrix: not worth building as is (210 values on nine rules); its effect is capped by the attack actions' fixed
  preconditions (failures loop back to the initial-access mapping); simpler stand-ins would do; different attack actions might
  let it matter.
- Q11 Random: disputed the session's numbers. Marc was right that they were wrong (see the corrections).
- Q12 NCR measures delay and disruption; fine.

Checked against numbers_reported.json (ranking.by_interval, sweep.by_interval):
- CORRECTION 1: random runs over all seven mechanisms. At 200 s, baseline attacker: random 0.33, members' mean 0.56, below six of
  seven (above only user shuffle, -0.05). APT attacker model: random 0.75, members' mean 0.48, above four of seven. So random is
  not its members' mean, and the gap changes sign with the attacker. Marc's rank reading (three ranks above, one below) is the
  rank view of the same fact. His 0.59 used the lineage four with OS diversity at 0.95; it is 0.07.
- CORRECTION 2: MTDShield's matched control is random over Tay's four: 0.68 vs 0.56 (baseline), 0.28 vs 0.80 (APT).
- Marc's Q4 claim HOLDS: which attacker is disrupted more agrees on NCR and ASP in 52 of 60 mechanism-interval cells; the 8
  others are within 0.04 on NCR. Distinct and also true: within the baseline attacker, NCR and ASP reductions split sign from
  500 s with ASP intervals clear of zero (IP shuffle 500/1000/2000 s; complete topology and OS diversity 500 s; host topology
  1000/2000 s the other way). The APT attacker model shows no clear split.
- "The APT attacker model is disrupted more" holds per mechanism, not overall: at 200 s more for the host layer, random,
  alternative; less for port shuffle, OS and service diversity, MTDShield, user shuffle.
- Sweep at 2 000 s: service diversity 0.30 (baseline), 0.06 (APT); IP shuffle 0.19 (baseline), 0.33 (APT).

Applied in ch6 (Marc: inside ch6 "I don't really care"): the 6.4 point set rebuilt as five points plus the cut candidate:
1 "optimal" for an attacker model, report the assumptions (Cho measured; CTI shrinks the assumption surface; neither attacker
better); 2 a deployment strategy inherits its attacker model (MTDShield vs random_four; random not its members' mean, optional);
3 integration is not a drop-in, report the interface on both sides (mapping, durations, failure; what a deployment takes; user
shuffle fixed; prediction only of direction; failure matrix as ablate-before-building; reuse as a second baseline); 4 lead with
the finer metric (52/60 agreement; the baseline sign split; worst case decided by the metric); 5 intervals, no cost so no
interval; detection out of scope. Old 6 kept as cut candidate.

Routed elsewhere (not applied):
- 7.2 future work: technique-level graph ablation on a larger corpus tied to mitigations; a learned strategy that recommends a
  fixed set; cost/overhead/QoS beside NCR reduction; IDS-paired risk-based MTD; post-intrusion MTD.
- 6.5: covers unmapped tactics, "nothing watches the attacker", the time limit; persistence by name is optional.
- Outside ch6, proposal only: App E "ASP reduction shows the order of NCR reduction" needs "at 200 s" (the baseline sign split).

### 14b. 6.4 drafted; P11 and P12 applied (2026-10-09)

6.4 drafted as four paragraphs from the plan (the dependence; where it travels; what to report; what the numbers cannot
decide), about 800 words; slots retired. Marc: "all the proposals are fine, no need for cut pass yet".
- P11 (a): random over MTDShield's four restored as a row of Tables E.1 and E.2 only (tools/ch5_sweep_figures.py
  VALUE_ROWS, MATCHED_DECODE in the caption); figures keep it out. Overturns the 2026-09-25 "a bit vacuous" cut for those
  tables, because Appendix D promises the comparison and 6.4 P2 recommends it. P2 now cites 0.68 vs 0.56 and 0.28 vs 0.80.
- P12: Appendix E "At 200 s, ASP reduction shows the order of NCR reduction" (the baseline sign split from 500 s).
- For the cut pass (not yet, Marc): 6.4 P2 and 6.2's MTDShield paragraph overlap on service diversity; P3 and P4 longest.

## 15. Ch6 structural pass (2026-10-09, NOT RULED)

Marc: "Are the points relevant where they are at, in a logical order, is there any duplication ... I'm not trying to
pare down sentences ... just logically arrange." Section order holds (6.1 and 6.2 follow ch5; 6.3 properties and
ablations; 6.4 implications; 6.5 threats). The faults are one point stated in two to four sections, and tangents in 6.1.
Rule proposed: **6.1–6.3 explain, 6.4 draws the implication, 6.5 bounds; a point has one home and the others point to it.**
Line numbers are dissertation.tex as of 1fcf80d9.

Duplicates (home in bold):
- D1 Literature link "attacker model decides which deployment strategy is optimal" + "a ranking carries its attacker
  model's assumptions": 6.2 ¶1 end (8718–8721), **6.4 ¶1**, 6.5 ¶5 (9414, cites 6.2; repoint to 6.4).
- D2 "Counting blocked attack actions would rank the host layer most disruptive against the baseline attacker": 6.2 ¶2
  end (8765–8769), **6.4 ¶4** (verbatim).
- D3 "Read alone, ASP and NCR call a quiet attacker weak": 6.1 ¶2 end (8578–8579), **6.4 ¶4** (verbatim, mutual refs).
- D4 MTDSim prices no deployment, so no interval is chosen: 6.2 ¶3 (8791–8796), 6.2 ¶4 bound (8830–8833), 6.4 ¶4 end,
  **6.5 ¶1** (design limit). 6.2 keeps one clause pointing to 6.5; 6.4 keeps the evaluator's implication.
- D5 Relative measure ("each ranking over that attacker's own NCR with no MTD") and the ASP check: 6.2 ¶1 (8713–8716),
  6.4 ¶3 (9131), 6.4 ¶4 ("agree on the reversal"), **6.5 ¶2** (9274–9282) and 6.5 ¶5. Cut from 6.2; 6.4 keeps the sign split.
- D6 MTDShield trained against the baseline attacker, service diversity at 70 % or more, one policy as released: 6.2 ¶4,
  6.4 ¶2, 6.5 ¶4. Proposal: **6.2 ¶4** holds the reading, and takes the matched-random numbers (0.68 vs 0.56; 0.28 vs
  0.80); 6.4 ¶2 opens on a pointer and keeps the detection input and the recommendation; 6.2 ¶4's last sentence ("only as
  faithful as ... comes first") is 6.4's. "One agent, as released" stays in 6.2 and 6.5.
- D7 "The difference rests on unmapped time and order": **6.3 ¶3**, 6.5 ¶1 (9217–9219), 6.5 ¶2 (9256–9260). 6.5 ¶2
  keeps "no run separates them"; 6.5 ¶1 keeps the "first step" point without re-deriving it.
- D8 The attack-action ceiling (order encoded, preconditions refused): **6.1 ¶3** explains it, 6.3 ¶2 uses it for the
  marks, 6.5 ¶1 re-explains it (9209–9212). 6.5 ¶1 points to 6.1.
- D9 Detection avoidance in part: 6.1 ¶1 argues the mark (8529–8533); **6.3 ¶2** owns marks.
- D10 Minor: "not a complete standard" 6.3 ¶1 and **6.5 ¶3**; "5 to 7 attack flows" 6.1 ¶4 and **6.5 ¶4**.

Misplaced or tangent:
- T1 6.1 ¶1 end (8533–8538): MTDShield's detection input and the IDS future-work line are MTD content in the no-MTD
  section; 6.4 ¶2 and 6.5 ¶1 ("nothing watches the attacker") cover both. Cut.
- T2 6.1 ¶4 (8649–8652): c3 under MTD from 500 s; 6.2 ¶1 holds it. Cut.
- T3 6.1 ¶3 (8621–8623): "an order hard-coded into attack actions passes to every extension" is an implication for
  simulator builders; move to 6.4 ¶3 (the interface).
- T4 6.2 ¶3 end (8796–8801): the earlier MTDSim studies' 50–200 s and the interval chosen against the wrong attacker is
  6.4's; move to 6.4 ¶4 beside "an interval needs a price".
- T5 Low: 6.4 ¶3 "Before the runs, we could predict only ..." (9128–9132) sits loosely in the interface paragraph; 6.2 ¶1
  "MTDSim has no redundancy mechanism" (8712).

Consistency (not a cut): 6.2 ¶1 and 6.5 ¶5 say ρ is "near zero"; 6.4 ¶1 says −0.24 to 0.25 (500 s is 0.25 [0.14, 0.38]).

## 16. Ch6: six cold examiners on the first overdraft, verified and triaged (2026-10-09, NOT RULED)

Brief: scratchpad examiners_ch6/brief.md (own benchmark dimensions, UWA bands, holes checked against the whole text,
overreach, placement; not told about vagueness or length; registry and handoffs hidden). Grades: 6.1 72, 6.2 72,
6.3 76, 6.4 74, 6.5 76, whole chapter 73 (all H2A). Marks lost on: positioning against prior work (whole: H3, five
\cite in the chapter); causal claims stronger than their evidence; repetition and overloaded paragraphs (6.2 ¶1 ~ten
moves, 6.3 ¶3 ~eight claims, 6.5 economy H2B at ~1 650 words); no tie to the RQ or SQs. Marked high: bounds (H1 in
6.1, 6.2, 6.5), explanation (whole H1), self-evaluation (whole H1). Nobody called the chapter vague. Their placement
lists reproduce §15 (MTDShield twice, price x4, metric arguments x2-3, attribution 6.3 vs 6.5, c3-under-MTD in 6.1).

Verified against the tex and tables (V = checked true):
- X1 (V) 6.2 ¶1 "exploiting them takes most of its time": ch2 942-944 says an exploit takes 0-9 s against 25 s for a
  port scan. No float supports the premise. Cut the clause.
- X2 (V) 6.2 ¶2 opener "by the time it costs it, not by the attack actions it blocks": Table 5.x disruption, baseline
  time lost IP shuffle -27, port shuffle -24, OS diversity -58 s, yet NCR reduction 0.68 / 0.91 / 0.68 at 200 s.
  Licensed: blocks and time lost rank the layers alike for the APT attacker model and part for the baseline attacker.
  6.4 ¶4's "which loses no time to it, so report time lost" inherits it.
- X3 (V) "unmapped time" mislabels the pace: ch4 4966-4970, the 45 s moves NCR "most likely through command and
  control", a MAPPED tactic (scan neighbours 45 s against 5 s, 6.5 ¶2). The attribution "unmapped time and order"
  (6.1, 6.3 ¶3, 6.5 ¶1-2) should be "tactic durations and order" (ch4's term).
- X4 (V) ablation reach: failure matrix ran under IP shuffle and OS diversity only, vulnerability memory under service
  and OS diversity only (tab 5-4a), so "none changes which MTD mechanisms are most effective" is measured for the
  attack profiles alone. And the attack profiles are not negligible under the host layer: d -0.70 / -0.76 under IP
  shuffle at 500 / 1 000 s against -0.28 with no MTD (tab F-3). Positive reading (6.3 examiner): the reversal survives
  on the attack graph, so it does not come from grouping by objective.
- X5 (V) "one network" (6.2, 6.4 ¶1, 6.5 ¶1 "one 50-host network"): each seed generates its own network (6105-6108).
- X6 (V) 6.5 internal contradictions: "comes from the attackers alone" (9224) against "do not run under identical
  conditions" (9267); "intervals resample runs, not seeds" against rho and Table E ablation intervals over seeds.
- X7 (V) 6.1 ¶3 "counted by attack action, ... hundreds of distinct openings" has no ch5 or appendix home (registry
  A3/B3: 190-844 against 3). Number-home rule.
- X8 (V) repairs to MTDSim are typeset only at 9287 and 9385; nothing says what was repaired. AI Use Declaration empty.
- X9 (V) ch3 2137-2140 Cho: platform diversity "defends against persistent attacks but can weaken the defence against
  fast ones"; here diversity ranks best against the fast baseline attacker. Unaddressed.
- X10 (V) ch3 2206 "mechanisms cannot be compared across evaluations" (Jalowski): 6.4 never answers it.

Holes, triaged (C = covered, B = bound to add, E = elsewhere, N = not covered):
- H-A N, high (6.4, 6.5, 6.2, whole): the reversal runs through MTDSim's deployment rules, written for the baseline
  attacker (host layer costs the APT attacker model its place until lateral movement). Is the dependence on the
  attacker model or on the attacker model meeting those rules? Rec: 6.4 ¶1 says the ranking depends on the attacker
  model as it meets the simulator's MTD rules; 6.5 ¶1 names the deployment rules as a third design root. Fits
  Marc's spine ("looking at your own assumptions").
- H-B N, high (6.3): the two marks gained over the baseline attacker (choice = order; detection avoidance = pace) are
  exactly where the difference rests, and the components behind adaptivity and learning moved no result. Rec: one
  synthesis sentence in 6.3 ¶3.
- H-C partly, high (whole, 6.1): the level answer. At 200 s the host layer and every deployment strategy remove more
  of the APT attacker model's NCR than the baseline attacker's (0.96 vs 0.49; random 0.75 vs 0.33), the service
  layer less (0.21 vs 0.84). Ch1's "advantage of time" premise is not revisited. Rec: one sentence in 6.2 ¶3; the RQ
  answer stays in ch7.
- H-D N, medium-high (6.2, 6.4, whole): positioning. X9 (Cho) in 6.2 ¶1; X10 (comparability) in 6.4 ¶1; prior
  MTDSim studies' rankings (check tab 5-3-3a lineage first). Game theory (6.4 H3) low.
- H-E partly, high (6.3): "choice of attack strategy in full" against the rule ("a fixed rule ... takes the place");
  6.1 bound 3 and 6.5 "whether it chooses well is not measured" concede it. Rec: 6.3 ¶2 defends it against ch3's
  definition in one sentence. Marc's ruling: the blind re-score already gave the same mark.
- H-F partly, medium (6.1): the plurality-price claim has no per-profile evidence (c1 has the most openings and the
  second-highest ASP; App B ties refusals to order, not variety). Rec: tie the refusals to order (24 % refused,
  Table B.7), drop "the more ways ... the more".
- H-G partly, medium (6.2, 6.5): the fall-off intervals and the duration band were tested at 200 s only; timescale
  ratio (tactic duration / deployment interval) as the bound on 15 000 s runs.
- H-H partly, medium (6.4): MTTC reporting (with the share of runs it covers); test against more than one attacker
  model; residual NCR beside the reduction (low).
- H-I N, medium (6.5): which analysis choices were fixed before results (200 s headline, Cohen's 0.2, NCR over ASP).
- H-J N, medium (preamble): one clause per section naming the SQ it bears on (Marc ruled ch6 answers none; a pointer
  is not an answer).
- Overreach to soften: "what transfers" / "optimal for one attacker model" (an existence proof: "can depend");
  6.4 ¶2 "the dependence travels" beside 6.2's "cannot tell a fitted policy from a fixed preference" (add the bound);
  6.2 ¶1 "attacker model matters more than the attack profile" (the profiles share durations, mapping and failure
  matrix); 6.4 ¶1 "CTI is one way to cut what an attacker model must assume" (Marc's Q1 ruling; examiners read the
  results as not supporting it -- keep as rationale, not result).
- To ch7 (6.4 examiner, agrees with §15 T5): 6.4 ¶3 "Before the runs, we could predict ..." and "Within MTDSim,
  another evaluation can run ..."; 6.3 ¶2 "Upgrading the attack actions would lift the most marks" (at most two).

## Validation gate

Done when Marc has answered §7, the structure in §3 is ruled, and every primary point in §4 has its evidence re-read on the 1 000-seed corpus, or is labelled a hypothesis. The next deliverable is per-paragraph dot points (slot form) for Marc's dictation.

## Reading list for the next session

1. This file.
2. The ch6 placeholders, `dissertation.tex` 8373–9033.
3. Harvest A §C (ch5 findings as stated).
4. Harvest D §2–§4 (benchmarks and move skeletons).
5. `docs/implementation/disruption_mechanism.md` §1 (6.2's mechanism).
