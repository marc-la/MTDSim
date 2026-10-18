# B: attribution of the host layer's lead, and the ablation under MTD (items 2, 3, 13)

**The rule.**
- *Purpose:* §6.2 answers SQ3 and explains the headline result. An examiner probes it for an explanation the text does not name (items 2 and 3) and for an explanation the text never tested (item 13). Each change names the alternative, or reports the test, where the claim is made.
- *Context:*
  - Items 2 and 3 rest on scoping already in the register.
  - Item 13 ran today: `data/results/ch6_further_analyses/run_unmapped_mtd.py`, 8 000 runs, 0 errors.
    - **Check 1:** with the declared durations, the harness reproduced the reported corpus exactly.
    - **Check 2:** with no MTD, the runs equal D.6's for all 80 compared.
  - Its numbers are in `unmapped_mtd_numbers.json`, read by `analyse_unmapped_mtd.py` under the criterion fixed before the run.
- *Audience:* the examiner at §6.2 and §6.5. Appendix D carries the detail, and appendix words are outside the band.

## What the run found (criterion fixed before the run: verdict **"mechanism only"**)

Service diversity and IP shuffle at 200 s, with the APT attacker model averaged over $c_1$ to $c_4$:

| | Declared durations | Unmapped tactics at 0 s | Baseline attacker |
|---|---|---|---|
| NCR reduction, IP shuffle | 0.96 (0.96, 0.96) | 0.85 (0.84, 0.85) | 0.68 (0.67, 0.70) |
| NCR reduction, service diversity | 0.36 (0.35, 0.38) | **0.29 (0.28, 0.31)** | 0.92 (0.91, 0.92) |
| Attack actions blocked per MTD deployment, IP shuffle | 0.11 | 0.27 | 1 |
| Attack actions blocked per MTD deployment, service diversity | 0.17 | **0.29** | 0.99 |

What the numbers say:
- **The mechanism moves, but not far.** Removing the time in unmapped tactics raises attack actions blocked per MTD deployment under service diversity from 0.17 to 0.29. That is still far from the baseline attacker's 0.99.
- **The outcome moves the other way.** Service diversity's NCR reduction **falls** from 0.36 to 0.29. In absolute terms too, the APT attacker model compromises 9.1 hosts under service diversity against 5.4 with the declared durations.
- **So the time in unmapped tactics does not explain the service layer's smaller reduction.**
- **The host layer's lead holds** (IP shuffle 0.85 against service diversity 0.29, intervals apart).
- **Where its time goes instead.** With unmapped tactics at 0 s, under service diversity the APT attacker model spends 80 % of its time in attack actions, but only **28 %** in the three a service-layer deployment disrupts (scan port, exploit, brute force). That matches the 0.29 blocked.
  - **45 %** goes on scan neighbours, the attack action of Command and Control.
  - Command and Control's declared mean duration is 45 s, and scan neighbours takes the baseline attacker 5 s (Appendix D.6).

**What this does to §6.2.** ¶3's opening claim, "We attribute the service layer's smaller reduction of its NCR to the APT attacker model's tactic durations", **survives**: the time sits in a mapped tactic's duration. Its mechanism sentence, "keep it between attack actions, in unmapped tactics that run none", is **what the run removes**. The smallest honest change is to replace that one sentence with the test and where the time actually goes. The paragraph's claim, ¶1's attribution, §6.4 and the abstract are untouched.

Still untested: whether Command and Control's 45 s causes the gap. That is D.6's second step under MTD, which was not run. **T2 keeps it as inferred.**

---

## The changes

| # | Location | Before | After | Why | Risk |
|---|---|---|---|---|---|
| B1 | §6.2 ¶2, after l.8764 ("…their preconditions are missing.") **APPLY ON RULING** | *(no sentence)* | **Part of the host layer's lead therefore comes through the tactic-to-action mapping (\ref{thr:cause}). The host layer's lead also reflects a disruption the APT attacker model does not adapt to: without the failure matrix, its time lost per MTD deployment under IP shuffle is unchanged (Section~\ref{sec:ablation}).** | **Item 2:** names the mapping where the mechanism is told, and points to T2. **Item 3:** draws the adaptivity conclusion from the 242–324 s, with the evidence beside it (§5.4, l.8376: the failure matrix, its only response, leaves time lost unchanged). Avoids "rather than" and a second "therefore". Agrees with adaptivity "in part". | +45. "Therefore" is earned by the sentence before. The paragraph then turns to service diversity, so the host-layer story closes on its conclusion first. |
| B2 | §6.2 ¶3, sentence 3 (l.8786–8787) **APPLY ON RULING** | The APT attacker model's tactic durations keep it between attack actions, in unmapped tactics that run none (Section~\ref{subsec:aio-disruption}). | *(cut, and its point moves into B3)* | The run removes this mechanism as an explanation of the outcome. | — |
| B3 | §6.2 ¶3, after the 0.15/0.95 sentence (l.8790) **APPLY ON RULING** | *(no sentence)* | **Rec.:** **The time it spends in unmapped tactics explains little of this: with those tactics at 0\,s, under service diversity at 200\,s, its attack actions blocked per MTD deployment rises only from 0.17 to 0.29, and its NCR reduction falls from 0.36 to 0.29 (Table~\ref{tab:fa-unmapped-mtd}). It then spends 45\,\% of its time in Command and Control, whose attack action, scan neighbours, a service-layer deployment cannot disrupt.**<br>**Alt. (leaner):** **With its unmapped tactics at 0\,s, under service diversity at 200\,s, its attack actions blocked per MTD deployment rises only from 0.17 to 0.29, and its NCR reduction falls (Table~\ref{tab:fa-unmapped-mtd}); most of its time then goes on Command and Control's scan neighbours.** | This reports the test Jin asked for, in the place the claim is made, and ends on where the time goes, which keeps ¶3's opening claim true. "Explains little" is the measured reading, not a causal one. Every term is already the reader's: unmapped tactic, attack actions blocked per MTD deployment, NCR reduction, Command and Control, scan neighbours (§4.4.1: "Command and Control is the only tactic that maps to scan neighbours"). | **+45 net** (Rec.; −20 from B2 and +65 here), or **+20** (Alt.). "Consistent with this" in the sentence before now refers to the rule sentence, which still reads. The 0.15 is at 2 000 s and the 0.17 at 200 s, so the new sentence names its interval. |
| B4 | T2 (thr:cause), l.9193–9196 **APPLY ON RULING** | We did not repeat this ablation under MTD, so the rest of our explanation is inferred. We never varied the tactic-to-action mapping, so we cannot rule it out as a cause of what we credit to the order of its tactics. | **Under MTD, we repeated only its first step, unmapped tactics at 0\,s, and the host layer still led (Appendix~\ref{app:fa-run-time}); the rest of our explanation is inferred.** We never varied the tactic-to-action mapping, so we cannot **separate its share of what we credit to the order of its tactics, the host layer's lead included.** | The first sentence was true yesterday and false today. The second now agrees with B1: §6.2 claims part of the lead for the mapping, so "cannot rule it out" understated it, while "cannot separate its share" is exact. "The rest … is inferred" still covers the untested step: Command and Control's 45 s under MTD. | +14. Threat wording holds: threat, mitigation, what remains. |
| B5 | Ch7 contribution 2, l.9804–9805 **PROPOSE** | Our ablation of the tactic durations ran with no MTD, and we never varied the tactic-to-action mapping (\ref{thr:cause}). | **Under MTD, we ablated only the time in unmapped tactics,** and we never varied the tactic-to-action mapping (\ref{thr:cause}). | The current sentence is now false. The replacement keeps its role as the bound on the attribution. | −1. It is ch7, so it is proposed first. |
| B6 | Appendix D: merge D.4 and D.6 (Marc's ruling) **APPLY ON RULING** | §D.4 *Ablation studies* (three tables of §5.4); §D.5 *Sensitivity analysis*; §D.6 *Ablation of the tactic durations* (text + Table D.6) | §D.4 *Ablation studies*: the three tables, then `\subsection{Ablation of the tactic durations}` carrying both labels (`app:further-analyses`, `app:fa-run-time`), D.6's paragraph and table unchanged, then the new paragraph (B7) and the new table. §D.5 *Sensitivity analysis* follows. | One section for every ablation; D.5's sensitivity analysis is a different method and stays separate. The labels move with the text, so every `\ref` follows. | The `\clearpage` before D.5 (2026-10-14 layout note) moves after the merged D.4; check the page breaks in the build. Appendix D's opening sentence still reads true ("D.1 to D.5 back Chapter 5, and D.4.1 backs Chapter 6"). |
| B7 | Appendix D.4.1, new paragraph after Table D.6 **APPLY ON RULING** | *(none)* | **Section~\ref{sec:disc-mtd-performance} explains the service layer's smaller reduction of the APT attacker model's NCR by its tactic durations, so the first step was repeated under IP shuffle and service diversity at 200\,s, on the same 1\,000 seeds (Table~\ref{tab:fa-unmapped-mtd}). With its unmapped tactics at 0\,s, attack actions blocked per MTD deployment under service diversity rises from 0.17 to 0.29, against the baseline attacker's 0.99, and NCR reduction falls from 0.36 to 0.29; under IP shuffle it is 0.85, so the host layer still leads. Under service diversity, the APT attacker model then spends 80\,\% of its time in attack actions: 45\,\% in scan neighbours, which Command and Control runs at a mean of 45\,s against the baseline attacker's 5\,s, and 28\,\% in scan port, exploit and brute force, the attack actions a service-layer deployment disrupts.** | It gives the full result where the reader looks for it, so §6.2 can stay short. The post-hoc status is already stated in this subsection's first paragraph and in T7. | Appendix: outside the band. The numbers are read from `unmapped_mtd_numbers.json`. |
| B8 | Appendix D.4.1, `\input{tables/tab_FA-9_unmapped_mtd}` after B7 **APPLY ON RULING** | *(none)* | New table (generated by `tools/further_analyses_tables.py`; see the table above for its values) | Two rows per measure: declared, unmapped at 0 s, baseline attacker. | Table numbering follows the build (D.7 or similar); check the caption fits. |

---

## In place

### §6.2 ¶2 (B1)

> On adaptivity, the APT attacker model loses time mainly to the host layer, 242 to 324 s per deployment, where the baseline attacker's time lost is at or below zero; the baseline attacker loses time only to service diversity, 493 s per deployment, where the APT attacker model loses 60 s (Figure 5.2(b)). After a host-layer deployment, neither attacker has a host to act on (Section 2.2.3). MTDSim sends the baseline attacker back to scan host, and its procedure runs enumerate host next. For the APT attacker model, only Lateral Movement runs enumerate host (Section 4.4.1), so it has no host until the order of its tactics next brings it to Lateral Movement, and meanwhile the attack actions of its other tactics can fail because their preconditions are missing. **Part of the host layer's lead therefore comes through the tactic-to-action mapping (T2). The host layer's lead also reflects a disruption the APT attacker model does not adapt to: without the failure matrix, its time lost per MTD deployment under IP shuffle is unchanged (Section 5.4).** Service diversity redraws every service, and MTDSim sends the baseline attacker back to scan port on the same host, so it exploits the host's new vulnerabilities from the start. The APT attacker model keeps the ports it had found and goes on to the tactic its Petri net picks, which is consistent with its 60 s.

### §6.2 ¶3 (B2 + B3, Rec.)

> We attribute the service layer's smaller reduction of its NCR to the APT attacker model's tactic durations. A service-layer deployment disrupts an attacker only while it scans ports, exploits or brute-forces (Section 2.2.3), which the baseline attacker does back to back. ~~The APT attacker model's tactic durations keep it between attack actions, in unmapped tactics that run none (Section 5.3.1).~~ Consistent with this, attack actions blocked per MTD deployment under every service-layer mechanism is 0.15 for the APT attacker model, against 0.95 for the baseline attacker (Figure 5.2(a)). **The time it spends in unmapped tactics explains little of this: with those tactics at 0 s, under service diversity at 200 s, its attack actions blocked per MTD deployment rises only from 0.17 to 0.29, and its NCR reduction falls from 0.36 to 0.29 (Table D.7). It then spends 45 % of its time in Command and Control, whose attack action, scan neighbours, a service-layer deployment cannot disrupt.**

*Read-aloud check.*
- The paragraph moves in one direction: claim (tactic durations), rule (what a service-layer deployment can disrupt), evidence (0.15 against 0.95), test (not the unmapped time), then where the time goes (Command and Control's scan neighbours). That last step makes the opening claim concrete, so the paragraph does not turn back.
- "Consistent with this" now follows the rule sentence directly, which reads more naturally than before.

### T2 (B4)

> Other components of the APT attacker model may confound our explanation of its results (Sections 6.1 and 6.2), which credits tactic durations and the order of its tactics. To mitigate this threat, we ablated the attack profiles, the failure matrix and the vulnerability memory one at a time, which rules out each as a cause of the host layer's lead (Section 5.4). A second ablation, with no MTD, replaced its tactic durations with the baseline attacker's times and closed almost two thirds of the gap in ASP between the two attackers (Appendix D.4.1). **Under MTD, we repeated only its first step, unmapped tactics at 0 s, and the host layer still led (Appendix D.4.1); the rest of our explanation is inferred.** We never varied the tactic-to-action mapping, so we cannot **separate its share of what we credit to the order of its tactics, the host layer's lead included.**

### Ch7 contribution 2 (B5, PROPOSE)

> The second contribution answers SQ3. In MTDSim, the most effective MTD mechanism depends on the attacker model. We attribute this dependence to the APT attacker model's tactic durations and the order of its tactics. **Under MTD, we ablated only the time in unmapped tactics,** and we never varied the tactic-to-action mapping (T2). The finding may not generalise beyond MTDSim's disruption rules or the 38 attack flows (T8, T9). …

---

## Considered, no change

- **§6.2 ¶1 (l.8742–8744), "We attribute the difference between the two attackers to the APT attacker model's tactic durations and the order of its tactics (T2)."** Still true: the run moves the duration from unmapped tactics to Command and Control's. T2 bounds it.
- **§6.4 l.9059–9063.** It attributes the layer ranking to "these two differences". Still true for the same reason. The mapping is how the order of its tactics reaches MTDSim, and T2 says its share cannot be separated.
- **§5.3.1 l.7594–7596**, "runs no attack action while in an unmapped tactic, so an MTD deployment then blocks none". A fact, still true.
- **Abstract, ch1.** They make no attribution.
- **T7 (thr:posthoc), l.9388–9390**, "The ablation of the tactic durations was also designed post hoc". This covers the new step, which belongs to the same ablation.
- **T5 (thr:values), "timing changes NCR most, but the rankings hold across its band".** Strengthened, not contradicted: the host layer's lead also holds with unmapped tactics at 0 s. No edit needed.
- **"The baseline loses none" (Jin's item 3 wording).** §6.2 keeps "at or below zero", which item 4's §5.3.1 sentence now explains. B1 does not restate the baseline.
- **The second step under MTD** (mapped tactics at the baseline attacker's times, which would test Command and Control's 45 s directly). Not run: it was outside Jin's request and the approved setup. T2 keeps it as inferred.

## Net

| | Words (body) |
|---|---|
| B1 (items 2 and 3) | +45 |
| B2 + B3 (Rec.) | +45 (Alt. +20) |
| B4 (T2) | +14 |
| B5 (ch7) | −1 |
| B6–B8 (Appendix D) | 0 (outside the band) |
| **Total** | **+103** (Alt. +78) |

**Citations:** none. **New label:** `tab:fa-unmapped-mtd`.
