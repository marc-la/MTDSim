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

## 9. Rulings (Marc 2026-10-15)

All five questions of §6 are yes: the SQ3-first ranking rule; the types glossed in brackets; MTDShield as its own internal item; T2 cause extended to §6.1; T2 conditions dissolved. The §6.4 fix ("either" → "each") is **applied**. Marc's additions, each checked before use:

| Marc's point | Checked | Goes to |
|---|---|---|
| Code: AI-assisted, inherited code, tech debt, iterated on since 2023, too much to review in full | The AI Use Declaration covers only scoring by language models, **not code** (flag §12). The lineage is in ch2 l.~783 | T1 |
| MTDShield has no concept of an unmapped tactic | App D.1: it is told the attacker's current attack action; it reads an unmapped tactic as nothing detected. At 200 s it chose nothing in 29 % of decisions against the APT attacker model and 23 % against the baseline attacker. The alternative explanation predicts that rise, so it gets **partial support** | T3 |
| NCR does not say whether the targeted attack scenario succeeded; NCR and ASP correlate but can diverge | **Verified:** at 500 s and 1 000 s the host layer reduces the baseline attacker's NCR (0.16, 0.06; Table D.3) but raises its ASP (−0.10, −0.06; Table D.5). None of these cells is greyed | T4 |
| Disruption is what the model defines; the service layer disrupts only three attack actions; "we made those really short" | **Corrected:** the APT attacker model's attack actions are not shorter across the board (Table B.4b: brute force 4.5 s against 20 s, but scan port 35 s against 25 s and the exploit 4.5–22.5 s against 4.5 s). What sets disruption is the **share of its time** spent in those attack actions, because the tactic durations keep it in unmapped tactics between them (§6.2 ¶3) | T6 |
| The marks are hard to defend; read them as a direction, not as absolutes | Each mark follows a predicate printed in App B, which is the transparency to cite | T7 |
| Runs on one network treated as independent: "I don't know how bad that is" | **Measured** (read-only, scratchpad `seed_boot.py`; resampling seeds, the four attack profiles averaged per seed, 2 000 resamples). Host minus service layer: APT attacker model +0.22 to +0.75, baseline attacker −0.11 to −0.45, and **no interval reaches zero at any deployment interval**. The closest is the baseline attacker at 500 s: −0.106 [−0.120, −0.092]. The points match Table D.3. Scott–Knott and ρ already resample seeds (analyse.py `per_seed`); ch5 does not say so | T8 (mitigation) |
| Only the tactic-durations ablation is post hoc; the other ablations are planned, in §5.4 | Agreed: App D.6 alone | T9 |
| "The rules: the attack actions, is that correct?" | Yes. The rules say which of the six attack actions each MTD layer disrupts | T10 unchanged |
| Corpus: meaning stripped, e.g. confidence; a confidence-0 step still in the graph; the pre-intrusion steps | **Verified:** of 853 attack actions in the 38 flows, 69 carry a confidence and 16 carry confidence 0 (Muddy Water, OceanLotus, ToolShell). The L3 build ignores confidence (no use in src/mtdsim/l3_simulation). App C.3 already prints c₁'s Impact edge, drawn with confidence 0. Reconnaissance is in 10 of 38 flows, hence the overlay (ch4 l.~4038) | T11 (confidence); overlay stays in T5 |

## 10. Drafts, item by item (proposed, not applied)

Each item makes the three moves. Pointers are given as printed numbers here and become `\ref`s in the tex. Words are approximate.

**Opener (~150).** Each threat below names a claim of Sections 6.1 to 6.4, what could make it wrong, what we did to mitigate it, and what remains. The limitations are the scope we chose: *[list as on disk]*. Each is a direction of future work (Section 7.2). We group the threats by the four types of Wohlin et al.: internal (the causes we give), construct (our metrics and the parts we declared), conclusion (our statistics) and external (beyond MTDSim and the 38 attack flows). Within each type, threats to the answer to SQ3 come first.

### Internal validity

**T1 code (~90).** The code may not do what Chapters 2 and 4 say it does. MTDSim's code was inherited from the studies that built it, and much of ours was written with AI assistance, so we checked the code by what it does. An event tracer replays any run step by step against the text, an audit compared MTDSim's code with what its papers describe, unit tests cover the Petri net and the simulator, and fixed seeds reproduce every run exactly. The defects the audit found in MTDSim were repaired, so the results are not compared numerically with earlier MTDSim studies. The threat remains for behaviour no check exercised.

**T2 cause (v5 as on disk, +1 sentence, ~150).** *[v5 unchanged]* Added at the end: With no MTD, only the tactic durations were changed on their own (Appendix D.6), so the share of the gap that Section 6.1 gives the order of its tactics could also come from these two components.

**T3 MTDShield (~100).** That MTDShield most likely learned to deploy the MTD mechanism that disrupts its training attacker most (Section 6.4) has a plausible alternative explanation. MTDShield is told the attacker's current attack action at each decision, and it was trained against the baseline attacker alone, so it has no input for a tactic that runs no attack action and reads one as nothing detected (Appendix D.1). It chose service diversity in most decisions against either attacker, 76 and 70 %, which is consistent with our explanation, but it chose nothing more often against the APT attacker model, 29 against 23 %. We cannot rule out the alternative without MTDShield retrained against the APT attacker model (Section 7.2).

### Construct validity

**T4 NCR reduction (~115).** NCR reduction, the measure of the answer to SQ3, measures how MTD performs only in part. It counts the hosts an attacker compromises, whereas the targeted attack scenario succeeds when a target host is compromised, which ASP counts. A run also ends at the first target host compromised, which cuts NCR short in 656 of the baseline attacker's 1 000 runs with no MTD. The two metrics can diverge: at 500 and 1 000 s, the host layer reduces the baseline attacker's NCR but raises its ASP (Tables D.3 and D.5). To mitigate this, we also computed ASP reduction, which does not depend on when a run ends, and each attacker's layer order holds on it at every deployment interval. The threat remains for rank 1 against the APT attacker model: up to 500 s, ASP reduction reaches 0.99 or more for every host-layer mechanism and cannot order them.

**T5 declared parts (~115).** CTI records no tactic durations, failure-matrix values or factor for the vulnerability memory, and no mapping from tactics to MTDSim's attack actions, so these parts represent an APT only as far as our judgement does (Table C.4). To mitigate this, we declared them before any result and varied, substituted or removed each one at a time: only the 45 s mean duration changes NCR much (Table D.9), and the rankings hold at both ends of its band (T2). Their interactions, the weights of the pre-intrusion overlay and the choice of one attack flow per APT group were not tested, and nor was any other partial mapping. In ours, Command and Control is the only tactic mapped to scan neighbours, the attack action that finds new hosts, so it alone sets how fast the APT attacker model spreads.

**T6 disruption measures (~95).** Time lost and attack actions blocked per MTD deployment, by which Section 6.2 explains each layer, measure disruption only as MTDSim defines it. A service-layer deployment disrupts an attacker only while it scans ports, exploits or brute-forces (T10). How often it disrupts therefore follows from the share of the attacker's time spent in those attack actions, which for the APT attacker model our tactic durations set (T5). Both measures are taken at 2 000 s only, because the next MTD deployment caps time lost at the deployment interval, so Section 6.2 explains the service layer at every deployment interval from measures taken at one.
*(Cut: the baseline attacker's time lost below zero at the first deployment; Section 5.3.1 carries it.)*

**T7 §6.3's marks (~120).** The marks of Section 6.3 measure each attacker model's properties only against our yardstick. The eight properties are our reading of the APT definition and two surveys, weighed equally though not equally important. One scorer marked all four attacker models, and the three MTD attacker models are our choice, none of them the attacker of a game-theoretic model, the dominant MTD modelling approach (cho2020). To mitigate this, each mark follows a predicate printed in Appendix B, and language models scored the attacker models blind (AI Use Declaration). Distinct openings, behind the full mark for choice of attack strategy, counts any variety, in tactics for the APT attacker model and in attack actions for the baseline attacker; recounted in attack actions, the attack profiles still have 190 to 844 against 3. We make no claim for the marks beyond comparing the four attacker models on the same predicates.

### Conclusion validity

**T8 layer order (~85).** The statistics support the layer order of Section 6.2 at every deployment interval. Its confidence intervals resample runs, so they treat the four attack profiles' runs on one seed's network as independent. To mitigate this, we resampled seeds instead: the host layer and the service layer remain apart at every deployment interval against both attackers (Appendix D.3). What remains is the order of single MTD mechanisms against the baseline attacker. Every service-layer mechanism reduces its NCR more than every host-layer mechanism only up to 100 s, and from 500 s the service layer's lead is service diversity's alone (Table D.3).

**T9 analyses behind the explanations (~90).** The ablations behind the explanations of Sections 6.1 and 6.2 are weaker tests than the rankings. A negligible effect is Cohen's default of ±0.2, not a bound set for hosts compromised. The ablations leave 24 of 60 cells inconclusive for the attack profiles, with no correction for the number of cells compared. The attack profiles compromise more hosts than all ten random partitions with no MTD, which chance alone would give one time in eleven (Section 5.4). The ablation of the tactic durations (Appendix D.6) was chosen after the results of Chapter 5 were seen, and it changes none of them. We treat these analyses as exploratory.

### External validity

**T10 rules (v6 as on disk, ~140).** Unchanged.

**T11 corpus (~140).** The results may not generalise to APT attackers beyond the 38 attack flows. The attack flows record campaigns that were detected and reported, each only as far as its threat report describes, and only 18 are attributed to a group in ATT&CK, criminal groups among them (Section 4.1). The base weights count each drawn edge the same, whatever the analyst's confidence in its steps: c₁'s one edge into Impact comes from a step drawn with confidence 0 (Appendix C.3). We chose attack flows because CTI and ATT&CK rarely record the order of an attack's techniques, at the cost of volume: three of the four attack profiles are drawn from 5 to 7 attack flows, each assigned to its attack profile by one coder (Appendix C.2). Without the attack profiles the host layer still reduces NCR most (T2), so that assignment does not decide the answer to SQ3. We make no claim about APT behaviour the attack flows do not record, and a run may join parts of several attack flows into a campaign no attacker ran.

**T12 observation (~65).** No APT campaign against MTD can be observed, so the APT attacker model cannot be validated against one. For a system that cannot be observed, Sargent advises exploring the model's behaviour as thoroughly as possible and comparing it with other models (sargent2011). The sensitivity analysis (Appendix D.5) and the ablations explore it, and the baseline attacker is the other model. The threat remains.

**Size.** About 1 450 words against 1 624 on disk. The §4 estimate of 1 130 was too low: T2 and T10 are ratified at about 150 and 140 words. The cut pass comes after the content is ruled. The first candidates are T4's run-end sentence (the ASP check covers it), T7's distinct-openings sentence, and T11's last clause.

## 11. Homes and flags owed before applying

- **Seed check (T8)** needs a home. Proposal: one sentence in App D.3 after Table D.3, "Resampling seeds instead of runs, the host layer and the service layer remain apart at every deployment interval against both attackers; the closest is the baseline attacker at 500 s, −0.11 [−0.12, −0.09]" (appendix: auto after ruling). Optional ch5 §5.x statistics clause (gated): Scott–Knott and ρ use one value per seed.
- **190 to 844 (T7)** is printed only in §6.5 (B3, homeless since the A3 ruling). Either home it in App D or drop the number and keep "recounted in attack actions, the gap holds".
- **AI Use Declaration** says nothing on AI-assisted code, so T1 cannot point to it. The rewording is owed (memory: ai-greenflag); one sentence on how the code was written and checked.
- **App C.4 l.~9861** cites `thr:conditions`: retarget to `thr:cause` when T2 conditions is dissolved.
- **§7.2** "MTDShield retrained against the APT attacker model (\ref{thr:observation})": retarget to `thr:mtdshield`.

## 12. Round 2 (Marc 2026-10-15): fewer, bigger threats

Marc: the big general threats read clearly; the specific ones "get into the weeds of the implementation" and become vague. "Do we have the biggest threats?"

**Verdicts on the specific items.**
- **T6 disruption measures: cut.** The real threat is that disruption is whatever the model defines it to be. That is T10 (MTDSim's rules) together with T5 (our tactic durations). The "2 000 s only" scope is a measurement choice: the deployment interval caps time lost, as Marc notes, and the float captions already state it. It is not a risk to a claim.
- **T8 layer order + T9 analyses: merged into one conclusion item.** With 1 000 seeds and the seed-level check, conclusion validity is the strongest part of the study. The honest item says so. It then names the two residuals: layer means hide single mechanisms, and the ablations are weaker, exploratory tests (Cohen's default, no correction, D.6 post hoc). Both labels stay on the one item.
- **T3 MTDShield, reasoned through.** Against either attacker it chose almost only service diversity or nothing: 76 + 23 % against the baseline attacker and 70 + 29 % against the APT attacker model. How we ran it (an unmapped tactic read as nothing detected) can therefore account only for the roughly 6-point shift from service diversity to nothing. Its main choice, service diversity, is the same against both attackers, so it comes from its policy, which is E3. The alternative explanation is real but bounded. What remains is whether MTDShield trained against the APT attacker model would choose differently.
- **T5 declared parts: widened** (Marc: "CTI wasn't designed for this … how much can we trust the weights"). The base weights are a construction of ours too: counts of drawn edges turned into probabilities of the next tactic. Before, they appeared only as T2's "taken as given". This is the construct threat with the most leverage on the model.

**Coverage, checked against de França & Travassos's simulation threats and the six cold examiners (§111).**
- By risk to what the dissertation claims, not by position, the largest are: T5 (most of the model's behaviour is our construction from CTI); T10 (MTDSim's rules produce the layer result); T11 (corpus); T2 (cause); T1 (code).
- Low: statistics, NCR reduction (ASP agrees on the layer order) and the marks (already hedged as a comparison).
- Missing: one limitation. Every run is the targeted attack scenario (ch2 l.~744, ch5 l.~6107), and the opener's list omits it. Add it there.
- The rival "would any slower attacker show the same layer order?" is T2's untested residual (uniform base weights). No new item is needed.

**Ten items now.**
- Internal: T1 code, T2 cause, T3 MTDShield.
- Construct: T4 NCR reduction, T5 the model's construction from CTI, T6 marks.
- Conclusion: T7 statistics.
- External: T8 rules, T9 corpus, T10 observation.

**Revised drafts (proposed, not applied).**

**T1 code.** The code may not do what Chapters 2 and 4 say it does. MTDSim's code was inherited from the studies that built it, and much of ours was written with AI assistance, so we checked the code by what it does. An event tracer replays any run step by step against the text, unit tests cover the Petri net and the simulator, and fixed seeds reproduce every run exactly. Getting MTDSim to run took repairing defects. Before we called a behaviour a defect, we checked it against what MTDSim's papers describe, so that a design choice was kept and only an error was repaired. The repairs mean the results are not compared numerically with earlier MTDSim studies. The threat remains for behaviour no check exercised.

**T3 MTDShield.** That MTDShield most likely learned to deploy the MTD mechanism that disrupts its training attacker most (Section 6.4) has a plausible alternative explanation in how we ran it. MTDShield is told the attacker's current attack action at each decision, and it reads the APT attacker model's unmapped tactics, which run none, as nothing detected (Appendix D.1). Against either attacker it chose almost only service diversity or nothing. Against the APT attacker model it chose nothing in 29 % of its decisions, against 23 % for the baseline attacker. How we ran it can therefore explain at most that shift, and not its choice of service diversity. We cannot rule out that MTDShield trained against the APT attacker model would choose differently (Section 7.2).

**T5 the model's construction from CTI.** CTI was not recorded to drive an attacker model, so much of what the APT attacker model does is our construction. Attack flows record the order of an attack's steps. They do not record how likely each next step is, how long a step took, what the attacker did after a step failed, or which of MTDSim's attack actions a tactic runs. We turned counts of drawn edges into the base weights, and we declared the tactic durations, the failure matrix, the vulnerability memory's factor and the tactic-to-action mapping by judgement (Table C.4). To mitigate this, we declared them before any result and varied, substituted or removed each one at a time: only the 45 s mean duration changes NCR much (Table D.9), and the rankings hold at both ends of its band (T2). Uniform base weights, the interactions between the parts, the weights of the pre-intrusion overlay and any other partial mapping were not tested.

**T7 statistics.** The statistics are strongest for the answer to SQ3. Each host-layer and service-layer mechanism ran on the same 1 000 seeds against both attackers. Resampling seeds in place of runs leaves the host layer and the service layer apart at every deployment interval (Appendix D.3). The layer means hide single MTD mechanisms: against the baseline attacker, every service-layer mechanism reduces NCR more than every host-layer mechanism only up to 100 s (Table D.3). The ablations are weaker tests. A negligible effect is Cohen's default of ±0.2, with no correction for the 60 cells compared, and the ablation of the tactic durations (Appendix D.6) was chosen after the results of Chapter 5 were seen. We treat the ablations as exploratory.

**T10 observation.** No data set records APT campaigns against MTD, so the APT attacker model cannot be validated against one, and what MTD does to an APT is inferred. For a system that cannot be observed, Sargent advises exploring the model's behaviour as thoroughly as possible and comparing it with other models (sargent2011). The sensitivity analysis (Appendix D.5) and the ablations explore it, and the baseline attacker is the other model. The threat remains. An emulated APT campaign against MTD could supply the data (Section 7.2).

Unchanged from §10: T2 (v5 + 1), T4, T6 (was T7, marks), T8 rules (v6), T9 corpus. The cut T6's labels: `thr:metrics` has no inbound reference outside §6.5 and is retired.

## 13. Round 3 (Marc 2026-10-15): T8 rules and T9 corpus

**T8 rules: v6 kept.** Marc: the rules allow the comparison but limit how far the APT attacker model represents an APT and has the eight properties. The comparison-and-limit pair is already v6's structure: "the same rules, so the comparison is fair" … "written for the baseline attacker's six attack actions". The property ceiling (no actions on objectives; a failure that cannot tell that MTD caused it) belongs to the attack actions. That is the opener's first limitation, and §6.3 states it where the marks are given. Repeating it in T8 would duplicate §6.3. The split Marc noticed is the clean one:
- T5 covers what we built from CTI.
- T8 covers what we inherited from MTDSim.

**T9 corpus v2 (proposed).** Marc: only dependency and sequencing are used; analyst nuance is stripped (confidence among it); flows are used as is; manual flows were chosen for the analyst's trust over automatic methods. Checked: ch4 l.~3923 already gives the reason (an analyst drew the order of every step; co-occurrence and keyword mining recovered 10 % and 14 % of tactic-to-tactic edges, against 50 %), so T9 points to it. The places are tactics (ch4 l.~4324), and the L3 build reads no confidence.

> The results may not generalise to APT attackers beyond the 38 attack flows. The attack flows record campaigns that were detected and reported, each only as far as its threat report describes, and only 18 are attributed to a group in ATT&CK, criminal groups among them (Section 4.1). We used each attack flow as its analyst drew it, and the APT attacker model keeps only which tactic follows which. It drops the techniques, the analyst's descriptions and their confidence in each step, so c₁'s one edge into Impact comes from a step drawn with confidence 0 (Appendix C.3). Analysts' attack flows record the order of steps that automatic alternatives could not recover (Section 4.1), at the cost of volume: three of the four attack profiles are drawn from 5 to 7 attack flows, each assigned to its attack profile by one coder (Appendix C.2). Without the attack profiles the host layer still reduces NCR most (T2), so that assignment does not decide the answer to SQ3. We make no claim about APT behaviour the attack flows do not record.

(About 140 words. Cut from the §10 draft: "a run may join parts of several attack flows into a campaign no attacker ran". It is minor beside the stripping, and it is a cut candidate if Marc wants it back.)

## 14. Full draft v2 applied for reading (Marc 2026-10-15: "get the full draft down … recompile the PDF")

Not ratified; the item-by-item rounds follow.
- **§6.5** has the opener and T1–T10 as in §10, §12 and §13. T2 is v5 + 1 sentence; T8 is v6 verbatim. Each item carries a `%` provenance comment.
- **Labels:**
  - `thr:values` + `thr:mapping` are on T5, and `thr:statistics` + `thr:posthoc` are on T7.
  - `thr:ncr` and `thr:mtdshield` are new.
  - `thr:conditions` and `thr:metrics` are retired.
- **Consequential edits:**
  - App C (dwell derivation) `thr:conditions` → `thr:values`.
  - §7.2 "MTDShield retrained" `thr:observation` → `thr:mtdshield` (a re-pointed `\ref` only).
  - App D.3 gains the seed-check sentence. Its source is `data/results/ch5_defended/seed_layer_check.py` (+ `.log`, `_numbers.json`), which reproduces the §9 figures exactly.
- **Fixes made on reading the page:**
  - T7 "the 60 cells compared" → "the number of cells compared". 60 is the attack profiles' ablation alone.
  - T4 "up to 500 s, 0.99 or more" → "up to 200 s, ASP reduction is 1". A printed 0.99 at 500 s could be below 0.99; at 50–200 s all three host-layer mechanisms print 1.00, which means exactly 1.
- **Build:** 83 pages (was 82), 0 undefined, no new overfull box. §6.5 is on pp. 43–46. About 1 600 words against 1 624; the cut pass comes after the rounds.

**Still owed (Marc rules):**
- the 190–844 home (T6);
- the AI Use Declaration's code sentence (T1 does not cite it until then);
- ch7 §7.2: the targeted attack scenario, now a limitation, has no future-work line ("Each is a direction of future work"). Proposal: add "and other attack scenarios" to the second bullet's head (ch7 gated).

## 15. Hedging audit of draft v2 against threats_terminology.md (Marc 2026-10-15; review only, nothing applied)

| Item | Threat | Mitigation | What remains | Defect (guide §) | Proposed fix |
|---|---|---|---|---|---|
| Opener | — | — | — | none | — |
| T1 code | "may not do what … say it does" ✓ | named checks ✓, not signposted | "The threat remains for behaviour no check exercised" ✓ (§a) | signpost missing | "To mitigate this threat, we checked the code by what it does" |
| T2 cause | "a plausible explanation of why" ✓ (§b) | ablations ✓ | "we cannot rule out either as a cause of" ✓ | the added sentence uses a second hedge ("could also come from") for the same residual (one hedge per claim, §b) | "…so we cannot rule out the same two components as a cause of the share of the gap that Section 6.1 gives the order of its tactics" |
| T3 MTDShield | "a plausible alternative explanation" ✓ | missing: the evidence is stated as a verdict | **mismatched**: "we cannot rule out that MTDShield trained against the APT attacker model would choose differently" is a counterfactual about retraining, not the residual of the stated threat | (1) four stacked hedges ("most likely", "plausible", "can explain at most", "cannot rule out"); (2) "can therefore explain at most that shift, and not its choice" asserts a counterfactual as fact and uses the not-X form; (3) the residual does not answer the threat (§a: "we cannot rule out X as a cause of Y") | "The shift is consistent with how we ran it; its choice of service diversity, the same against both attackers, is consistent with our explanation. We cannot rule out how we ran it as a cause of part of MTDShield's smaller reduction; MTDShield retrained against the APT attacker model would separate the two (Section 7.2)." |
| T4 NCR | "measures how MTD performs only in part", construct and operation named ✓ (§a, Sjøberg) | "To mitigate this threat, we …" ✓ | "The threat remains for rank 1 …" ✓ | none | — |
| T5 model from CTI | **not in construct form**: "CTI was not recorded to drive an attacker model, so much … is our construction" names neither the construct nor "only in part" | "To mitigate this threat" ✓ | **weak**: "were not tested" gives no consequence | §a construct form; §a untested form | S1: "The APT attacker model represents an APT attacker only in part, because CTI records little of what it needs." Last: "We have not tested uniform base weights, …, so we cannot rule out that they change the rankings." |
| T6 marks | "measure … only against our yardstick" ✓ (adapted "only in part") | "To mitigate this threat" ✓ | "We make no claim … beyond" ✓ (§a) | order: a second threat (distinct openings) comes after the mitigation, so the item reads threat → mitigation → threat → mitigation → residual | move the distinct-openings sentence before "To mitigate this threat", so the two mitigations sit together |
| T7 statistics | **missing**: v2 cut the threat sentence, so "Resampling seeds in place of runs" is a mitigation with no threat stated (§e). "The ablations are weaker tests" is vague; the field's names are *violated assumptions of a test* (independence) and *fishing and the error rate* (§d) | seed check ✓, not signposted | "We treat the ablations as exploratory" ✓ | §e mitigation without threat; §d unnamed threats; "hide" is figurative; the opener "strongest for" is a verdict, not a threat | "The confidence intervals resample runs, so they assume the four attack profiles' runs on one seed's network are independent. To mitigate this threat, we resampled seeds in place of runs, and the host layer and the service layer remain apart at every deployment interval (App D.3). The layer order does not hold for every single MTD mechanism: … The ablations compare many cells with no correction for the number compared, against Cohen's default of ±0.2, … so we treat them as exploratory." |
| T8 rules (ratified v6) | "rest on" is one of the guide's **invented residual verbs** (§e). v6 was ratified (§132) before the guide was written (§135) | "the same rules, so the comparison is fair" ✓ | "either would narrow the host layer's lead" ✓ | §e "rests on"; the external form ("may not generalise to") is absent, so it reads as internal | word-level only: "rest on MTDSim's rules" → "assume MTDSim's rules" (§a "we assumed"; §c assumption). Optional: "…so the results may not generalise to MTD as it would disrupt an APT" |
| T9 corpus | "may not generalise to" ✓ (§a external) | the reason for attack flows ✓; the assignment ruled out ✓ | "We make no claim about …" ✓ | none | — |
| T10 observation | "cannot be validated against one … inferred" ✓ | Sargent ✓, not signposted | "The threat remains." ✓ | signpost missing | "To mitigate this threat, we followed Sargent's advice for a system that cannot be observed: …" |

**Across the section.**
- **The mitigation signpost is used unevenly.** "To mitigate this threat" appears in T4, T5 and T6 only. An examiner scanning for the three moves finds them only in those three. *Recommend* using it in every item that has a mitigation (T1, T7 and T10 gain it; T2's ablations and T9's ruled-out assignment can keep their sentences and take the signpost too).
- **The "what remains" wording is from the guide's list** (§a: the threat remains / cannot rule out / no claim beyond), except T5 ("were not tested") and T3 (mismatched). With those two fixed, every residual is conventional.
- **Upstream causal attributions** (flag only; ch6 §6.1–§6.4, and Marc rules): §6.1 "most likely accounts for the rest"; §6.2 "likely explain", "most likely fail", "likely explains its 60 s"; §6.4 "most likely learned", "likely decide", "can therefore likely change"; ch7 contribution 2 "likely explain why". Guide §b treats "likely explains" as a causal attribution. T2 now says "a plausible explanation" of the same claim §6.2 calls "likely", so the reader meets two words for one hedge. Either §6.2 moves to the guide's vocabulary ("are a plausible explanation of", "is consistent with"), or T2 quotes §6.2's word. *Recommend* the former, as a one-word sweep, after Marc rules.
- **Not-X forms:** T3's "and not its choice of service diversity" (fixed above). T4's "whereas" clause names construct against operation, which is the Sjøberg form, so it stays.
