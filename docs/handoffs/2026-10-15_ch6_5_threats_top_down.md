---
status: open
created: 2026-10-15
goal: Rebuild §6.5 (Threats to validity) top-down, from the claims of §6.1–§6.4 to one line per threat, before any item is expanded or reworded.
supersedes: the §114 sort and the item order in docs/handoffs/2026-10-11_ch6_1_redraft_scrutiny.md §109–§137 (that record keeps the T1 and T10 drafting rounds, which stand)
---

# §6.5 threats to validity: top-down review and skeleton

Marc 2026-10-15: "a formal critique … top-down … what are the threats we're bringing up … not retrofitting the one-liners into what's on file … why I rank them the way I do … the opener, internal, conclusion … bang, bang, bang". Nothing is applied to the tex. This record holds the frame, the diagnosis, the claim register, the skeleton for Marc's ruling, and the follow-through.

## 1. Frame (five lines)

- **Purpose.** For each claim of §6.1–§6.4: what could make it wrong, what we did about it, and what remains. Each residual gets a number that §7.1, §7.2 and the appendices can cite.
- **Context.** The reader has just read four sections of claims, some measured and some hedged ("likely explain"). §6.5 gives the reasons for those hedges. It does not argue the claims again.
- **Audience.** The examiner checks two things: that nothing unstated undermines the headline, and that every hedge in ch6 has its reason here. A CS student wants to know how far to trust each answer.
- **The unit is the claim, not the loose end.** Each item opens on the claim it bounds and then makes three moves: threat, mitigation, what remains (`threats_terminology.md` §a).
- **Lean test.** An item that names no claim of §6.1–§6.4 is not a threat. A mechanism §6.1–§6.4 already explains is pointed to and not re-explained.

## 2. Diagnosis: why rewording keeps failing

Each cause below is structural, so no amount of rewording fixes it. Evidence comes from the tex on disk and from the §109–§137 trail.

1. **Built from material, not from claims.** The items were collected bottom-up: §6.x paragraphs that were dropped, examiner questions, and audit gaps (§109–§113). Each is named after where it came from (conditions, metrics, statistics, values). So each item has to rebuild its claim in its first sentence, and several cannot because they own no single claim:
   - T2 *conditions* names no claim at all.
   - T6 *metrics* bounds three claims in three sections.
   - T8 *statistics* makes seven points about four claims.

   A sentence cannot name a claim its item does not own.
2. **No claim list, so the ranking rule cannot be applied.** The opener ranks "by how far each could change a claim", but the claims are never named and "how far" is never defined. So the T1/T2 order was argued twice (§117, §126) with no test to settle it.
3. **Results and explanations are mixed together.** Ch6 makes three kinds of claim:
   - **results** measured in MTDSim;
   - **explanations** of those results ("likely explain");
   - **reach** beyond MTDSim.

   Each threat type mostly bears on one kind. Conclusion and construct threats bear on results, internal threats on explanations, and external threats on reach. T1 took four rounds (§117–§124) to find that it bounds the explanation and not the result, because the section never sets this up as its spine. Every item has to work it out again.
4. **The types are used as labels, not as tests.** These items were filed by feel:
   - T2 sits under internal, but different action times are the treatment, not a confound (§114, §137).
   - T10 moved from internal to external (§129).
   - The mapping sits in two types (T1 and T5).
   - MTDShield's training mismatch sits under external (T12), but it is a plausible alternative explanation for §6.4's MTDShield claim, so it is internal.

   The opener defines the four types and then never uses them to sort.
5. **The headline is threatened in many places at once.** Six items touch the answer to SQ3: T2, T3, T4, T8, T10 and T11. None says that this answer is the claim at risk, so the reader cannot tell whether the headline is in doubt. In fact, in MTDSim only four things could falsify it: the code, NCR as the measure, the declared values, and the confidence intervals. All four are mitigated. Everything else bounds an explanation or the reach.
6. **Re-explaining.** With no claim to point to, an item shows what is at risk by retelling the mechanism (T2 S1–S2; T6's time-lost mechanics; T11's 18-of-38, which is ch4 verbatim). This was the T1 v2 failure Marc named: "reinventing the wheel" (§122).
7. **The opener does three jobs.** It lists eight limitations, defines four types as questions, and states a ranking rule, so it reads heavy. Defining the types pays off only if the items are then sorted by them.

## 3. The claims §6.5 bounds (the scaffold; this list does not go in the tex)

| ID | Claim | Where | Kind |
|---|---|---|---|
| R1 | At every deployment interval, the host layer reduces the APT attacker model's NCR more than the service layer does; the reverse holds for the baseline attacker; rank 1 shares no MTD mechanism (Table rank-one-intervals) | §6.2, SQ3 | result |
| R2 | With no MTD, the APT attacker model differs on three properties, and has lower ASP and NCR | §6.1 | result |
| R3 | The APT attacker model has more of the eight properties than the three MTD attacker models | §6.3, SQ1–2 | result |
| R4 | MTDShield reduces the baseline attacker's NCR more than random does, and the APT attacker model's less | §6.4 | result |
| E1 | Tactic durations and the order of its tactics cause R2 (durations about two thirds of the ASP gap; order "most likely" the rest) | §6.1 | explanation |
| E2 | The order of its tactics explains the host layer's lead; the tactic durations explain the service layer's smaller reduction | §6.2; §6.4 ¶3 and ch7 contribution 2 lean on it | explanation |
| E3 | MTDShield "most likely learned to deploy the MTD mechanism that disrupts its training attacker most" | §6.4 | explanation |
| G1 | Which MTD mechanism an evaluation finds most effective can depend on its attacker model | §6.4, ch7 | reach (an existence claim) |
| G2 | How MTD performs against APT attackers, via the APT attacker model as their stand-in | RQ, ch7 opener | reach |

**What the register shows.** G1 is an existence claim: one simulator is enough, provided R1 holds in it. So the external threats do not threaten G1. They bound G2. The threats that could sink the headline are the ones that could make R1 false in MTDSim, and those go first in each type.

**Type → claim kind (the sort test).**
- Internal: is the cause we give the cause? Applies to E1–E3. R1's attribution to the swap of attacker is controlled by design, because only the attacker changes. The code is the instrumentation threat to every result.
- Construct: do our metrics and the parts we declared stand for what we say? Applies to R1 (NCR), E2 (disruption measures), R3 (yardstick, distinct openings), and the APT attacker model as an APT (declared parts).
- Conclusion: do the statistics support the result? Applies to R1 (CIs and scope) and the analyses behind E1 and T2's mitigation.
- External: does it reach beyond MTDSim and the 38 attack flows? Applies to G2, and to E2's rules.

**Ranking rule (one line, checkable).** Within each type, items follow the order of the claims: the answer to SQ3 (R1, then E2), then §6.1, then §6.3, then §6.4. The reason is that SQ3's answer is the answer the ch7 opener gives to the RQ.

## 4. The skeleton (for ruling; one-liner, then the three moves)

Wording follows `threats_terminology.md`. These lines are a scaffold, not prose, and each is expanded later the way T1 and T10 were.

### Opener
**One-liner:** Each threat below names a claim of Sections 6.1 to 6.4, what could make it wrong, what we did to mitigate it, and what remains.
- S2: The limitations, the scope we chose, as one list (unchanged), each taken up in §7.2.
- S3: The threats grouped by Wohlin et al.'s four types, each glossed by its object in brackets: internal (the causes we give), construct (our metrics and the parts we declared), conclusion (our statistics), external (beyond MTDSim and the 38 attack flows). This replaces the four questions (Marc: "simplify").
- S4: Within each type, threats to the answer to SQ3 come first.

About 110 words, against 167 now.

### Internal validity
**One-liner:** Only the attacker changes between the runs compared, so what is open is whether the code runs the model we specified, and which part of the model causes each result.

| # | Claim | Threat | Mitigation | What remains |
|---|---|---|---|---|
| T1 code (`thr:code`) | every result | the code may not run the model Chapter 4 specifies | event tracer, audit against MTDSim's papers, unit tests, fixed seeds | defects found in MTDSim were repaired, so no numerical comparison with earlier MTDSim studies |
| T2 cause (`thr:cause`) | E2, and E1 (**extension**) | tactic durations and the order of its tactics are a plausible explanation; other parts of the model change with them | under MTD: failure matrix and vulnerability memory negligible; host layer still first without the attack profiles; the most sensitive durations ×¼ and ×4 at 200 s | base weights and the mapping never varied under MTD, so we cannot rule out either as a cause of the host layer's result (v5 as on disk) |
| T3 MTDShield (new `thr:mtdshield`, from T12's second half) | E3 | plausible alternative explanation: MTDShield reads an unmapped tactic as nothing detected, so it decides on less information against the APT attacker model | it chose service diversity about as often against either attacker (76 and 70 %; App D.1), which is consistent with E3 | we cannot rule out the alternative without retraining it (§7.2) |

### Construct validity
**One-liner:** The answer to SQ3 is measured as NCR reduction, against an APT attacker model whose parts at the points where MTD disrupts it we declared by judgement.

| # | Claim | Threat | Mitigation | What remains |
|---|---|---|---|---|
| T4 NCR reduction (new `thr:ncr`; absorbs T2's run end and T8's ASP clause) | R1 | NCR reduction measures how MTD performs only in part: a run ends at the first target host compromised, which cuts NCR short in 656 of the baseline attacker's 1 000 runs with no MTD; ASP is the field's dominant effectiveness metric | ASP reduction does not depend on when a run ends, and each attacker's layer order holds on it at every interval (Table D.5, checked) | up to 500 s, ASP reduction reaches 0.99 or more for every host-layer mechanism against the APT attacker model, so it cannot order them; rank 1 against the APT attacker model depends on NCR alone |
| T5 declared parts (`thr:values` + `thr:mapping`, both labels kept) | R1, E2 | tactic durations, failure matrix, the vulnerability memory's factor and the tactic-to-action mapping represent an APT only as far as our judgement does; CTI records none of them | declared before any result; each varied, substituted or removed one at a time; only the 45 s mean changes NCR much, and the rankings hold at both ends of its band (T2) | interactions, the overlay's weights, one attack flow per APT group, and any other partial mapping are untested |
| T6 disruption measures (`thr:metrics`, narrowed) | E2 | time lost and attack actions blocked per MTD deployment measure disruption only in part: both are taken at 2 000 s only (the next deployment caps time lost at the deployment interval), and time lost's run with no MTD matches the run under MTD only up to the first deployment | none possible at shorter intervals; the reason is stated | §6.2 explains the service layer at every interval from measures taken at one |
| T7 §6.3's marks (`thr:yardstick` + distinct openings) | R3 | the eight properties are our reading, weighed equally and scored by one scorer against three MTD attacker models we chose (none game-theoretic); distinct openings counts variety, in tactics for the APT attacker model against attack actions for the baseline attacker | language models scored blind (AI Use Declaration); recounted in attack actions, 190 to 844 against 3 | the marks measure APT fidelity against our yardstick only; distinct openings shows choice, not good choice |

Cut from construct: "attack rate and attack confidentiality measure detection avoidance by proxy", because §6.3 owns it and marks property 5 in part for that reason.

### Conclusion validity
**One-liner:** The statistics support the layer order at every deployment interval for both attackers. The analyses behind the explanations rest on weaker tests.

| # | Claim | Threat | Mitigation | What remains |
|---|---|---|---|---|
| T8 layer order (`thr:statistics`, narrowed) | R1 | violated independence: the CIs resample runs, not seeds, so the four attack profiles' runs on one seed's network count as independent and the intervals are too narrow | the layer means' intervals separate at every interval for both attackers (Figure 5.3, Table D.3) | per mechanism, the order against the baseline attacker is narrower: every service-layer mechanism leads only up to 100 s, and from 500 s the lead is service diversity's alone |
| T9 analyses behind the explanations (`thr:posthoc` + the ablation half of `thr:statistics`) | E1; the "negligible" in T2's mitigation | fishing and the error rate: 60 ablation cells with no correction, 24 inconclusive; "negligible" is Cohen's default ±0.2, not a bound set for hosts compromised; beating all ten random partitions happens by chance one time in eleven; the tactic-durations ablation was chosen after ch5's results | labelled post hoc; it changes no ch5 result | these analyses are exploratory |

Cut from conclusion:
- ρ "weaker than one inverting the other": vestigial, since §6.4 says "uncorrelated" (§81, §114).
- Different NCR with no MTD: each ranking is within one attacker, so the different NCR is the treatment, not a threat.

### External validity
**One-liner:** The answer holds for MTD as MTDSim models it, against an APT attacker model built from 38 attack flows, and no APT campaign against MTD can be observed to check either.

| # | Claim | Threat | Mitigation | What remains |
|---|---|---|---|---|
| T10 rules (`thr:rules`) | R1's reach, E2 | MTDSim's rules for how a deployment disrupts an attacker were written for the baseline attacker's six attack actions | the same rules for both attackers, so the comparison is fair; kept as MTDSim's papers describe them | Command and Control keeping a host, or a service-layer deployment taking one back, would narrow the host layer's lead. **v6 as ratified; no change** |
| T11 corpus (`thr:corpus` + the one-coder classification from T7) | G2 | the results may not generalise to APT attackers beyond the 38 attack flows: detected and reported campaigns, 18 attributed (criminal groups among them), three attack profiles on 5 to 7 flows, one coder assigning each flow to an attack profile | attack flows chosen because they record the order of techniques; without the attack profiles the host layer still reduces NCR most, so the assignment does not decide R1 | we make no claim about APT behaviour the attack flows do not record; a run may join several flows into a campaign no attacker ran |
| T12 observation (`thr:observation`, minus MTDShield) | G2 | no APT campaign against MTD can be observed, so the APT attacker model cannot be validated against one | Sargent: explore the model's behaviour (App C sensitivity, ablations) and compare it with another model (the baseline attacker) | the threat remains: the results describe MTDSim's model of an APT attacker |

**Count and size.** Still 12 items (internal 3, construct 4, conclusion 2, external 3), but now each item owns one claim. Estimated length is the opener at about 110 plus 12 × about 85, about 1 130 words, against 1 624 on disk. That meets the §109 target.

## 5. Old → new

| On disk | Becomes |
|---|---|
| T1 cause | T2; claim extended to §6.1's "order accounts for the rest" (proposal) |
| T2 conditions | dissolved. S1–S2 are the treatment (T2 covers its parts). The NCR-with-no-MTD point is cut. Run end goes to T4. Inbound App C.3 l.~9861 `\ref{thr:conditions}` is retargeted to `thr:cause` (appendix: auto after ruling) |
| T3 code | T1 |
| T4 values + T5 mapping | T5 |
| T6 metrics | split: disruption becomes T6; distinct openings goes to T7; the proxy sentence is cut |
| T7 yardstick | T7 (+ distinct openings); one coder goes to T11 |
| T8 statistics | split: CIs and per-mechanism scope become T8; Cohen, 24/60 and one-in-eleven go to T9; the ASP clause goes to T4; ρ and starting points are cut |
| T9 post-hoc | T9 |
| T10 rules | T10, unchanged |
| T11 corpus | T11 (+ coder) |
| T12 observation | T12; the MTDShield half becomes T3 |

## 6. Questions for Marc (recommendation first)

1. **Ranking rule:** within each type, threats to SQ3's answer come first. *Recommend yes.* It makes the order checkable, and it moves code to T1 and cause to T2. The alternative is to rank by the size of the residual, which is judgement and cannot be checked.
2. **Opener:** replace the four questions with a bracketed object per type. *Recommend yes.*
3. **MTDShield:** make it an internal item (T3) as a plausible alternative explanation for E3, or leave it as T12's last sentence. *Recommend T3.* It is the question an examiner would ask of §6.4's "most likely learned".
4. **T2 cause:** extend the claim at risk to §6.1's "the order of its tactics most likely accounts for the rest". *Recommend yes, one clause.* That attribution is unbounded on disk.
5. **Dissolve T2 conditions** as in §5. *Recommend yes* (already recommended in §114 and §137).

## 7. Flags outside §6.5 (verified; not applied)

- **§6.4 ¶2a** (l.~8965): "Ranking on ASP reduction instead gives the same layer order against either attacker" can be read as saying both attackers share one order. That is false: Table D.5 puts the host layer first against the APT attacker model and the service layer first against the baseline attacker, at every interval. Change "either" to "each". (ch6: auto after ruling.)
- **App C.3** (l.~9861) cites `thr:conditions`; retarget it if T2 conditions is dissolved.
- **ch7 §7.2** bullets cite `thr:rules`, `thr:observation` (MTDShield retrained → `thr:mtdshield` if Q3 is yes), `thr:cause` and `thr:corpus`. The §7.1 bound note's numbers follow automatically.

## 8. Process after ruling

1. Apply the skeleton as the item order and labels, with one-liners as `%` slots, and keep T2 (cause, v5) and T10 (rules, v6) as ratified.
2. Expand one item at a time through the three moves, using the T1/T10 lessons: claim in the reader's terms, point and don't re-explain, the frank reason for what was taken as given, one hedge from the guide.
3. Do one cut pass against the word band.

## Validation gate

- Every item opens on a claim in the register (§3).
- Every item makes the three moves, in the guide's wording.
- The order obeys the ranking rule.
- No item re-explains a mechanism §6.1–§6.4 gives.
- Labels resolve, and the build is clean.

## Reading list

- `docs/workflows/threats_terminology.md`
- `docs/handoffs/2026-10-11_ch6_1_redraft_scrutiny.md` §109–§137 (the T1/T10 rounds and their lessons)
- `docs/thesis/dissertation.tex` §6.1–§6.5 (l.~8460–9222) and ch7 §7.2
- `docs/thesis/tables/tab_F-0d_interval_values_asp.tex` (T4's check)
- App D.1 MTDShield (l.~9942) (T3)
