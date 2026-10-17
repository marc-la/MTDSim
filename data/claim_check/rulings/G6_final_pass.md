# G6: the final pass

**Applied 2026-10-17 (Marc, all).**

Rule: the smallest change that makes each statement exact. Every item was re-verified on 2026-10-17. Chapters 3–5 are proposals; Chapter 6 and the appendix are applied after your ruling.

| # | Where | Before | After | Evidence |
|---|---|---|---|---|
| 1 | §3.3 (l. 3247) | … the paragraph on each attacker model below cites the evidence from its paper for each mark. | … below **gives** the evidence from its paper for each mark. | About a dozen mark sentences carry no citation. Each one rests on the paper its paragraph opens with (R3). |
| 2 | §4.4.2 (l. 4994) | No source times the other nine tactics, since threat reports time whole intrusions. | No source **we found** times the other nine tactics, since … | This is an absence claim. Without the hedge, it says no such source exists. |
| 3 | §4.4.3 (l. 5102) | … describe incidents that succeeded and were worth writing about, so **an attack flow draws** only the steps **its attacker** completed. | … so **the attack flows draw** only the steps **their attackers** completed. | The Attack Flow format can draw failure through a condition's false branch. **None of the 38 flows uses it** (0 conditions with a false branch), so the claim is true of the corpus but not of the format. |
| 4a | §5.3.2 (l. 7869) | At 200 s, MTDShield chooses service diversity in 70 % or more of its decisions against either attacker (Appendix D.1). | … of its decisions against either attacker **in 100 runs** (Appendix D.1). | App. D.1: "(100 runs each)". §5.1 says every configuration ran on 1 000 seeds. |
| 4b | §6.5 T-item (l. 9242) | … MTDShield chose to deploy nothing in 29 % of its decisions against it and 23 % against the baseline attacker. | … and 23 % against the baseline attacker, **in 100 runs (Appendix D.1)**. | As 4a. |
| 5 | §6.2 (l. 8983) | … MTDShield reduces the baseline attacker's NCR by 68 % and the APT attacker model's by 28 %; the random deployment strategy reduces them by 33 % and 75 % (Figure 5.3(d) and (e)). | … the random deployment strategy **over the same four MTD mechanisms** reduces them by **56 %** and **80 %** (Figure 5.3(e); **Table D.3**). | App. D.1 names the four-mechanism random strategy as the control that isolates "what the agent's policy adds". Table D.3 gives 0.56 and 0.80 at 200 s. The paragraph's opening ("more … at every deployment interval", "less") holds at all six intervals with this control. |
| 6 | §6.5 (l. 9359) | … language models that blindly scored all four **MTD** attacker models. | … blindly scored all four attacker models. | The four are the three MTD attacker models plus yours, the count used at lines 8898, 9362 and 9777. |
| 7 | §6.2 (l. 8992) | Tay **et al.** tested MTDShield in its training environment … | Tay tested MTDShield … | The report has one author. Both verifiers flagged it. |
| 8 | App. D.5 (l. 10493) | Each of the four mean durations **that several tactics share** was moved to both ends of its band … | Each of the four mean durations **of Table D.9** was moved … | Five durations are shared: 4.5, 35, 36, 45 and 22.5 s. Four were moved. The 22.5 s is half the 45 s (§4.4.2). The pointer is exact; the count was not. |
| 9 | App. D.3 (l. 10380) | … it cannot separate the **five** that reach 0.99 or more: every host-layer MTD mechanism and the random and alternative deployment strategies. | … the **six** that reach 0.99 or more: every host-layer MTD mechanism and the random, **random over MTDShield's four,** and alternative deployment strategies. | Table D.5 at 200 s: IP, complete topology and host topology shuffle each 1.00; random >0.99; random over MTDShield's four 1.00; alternative 0.99. |
| 10 | — | Cohen 1988: does he call 0.2 "small" or "negligible"? | **No edit.** Check your copy (the effect-size chapter). | The sentence now cites Cohen and Tantithamthavorn together, and Tantithamthavorn supplies the word "negligible". It holds either way. |

**Considered, no change.**

- **§6.3 (l. 8911), pointer to Section 4.4.2.** It supports "threat reports time only whole intrusions". "Almost never record" is §3.1's claim, which is itself cited.

**Net change:** about 25 words across 9 sentences. No sentence is restructured.
