# Mechanical bundle, run 1 (M01)

**Scope:** the abstract, Chapter 1, Chapters 5–7 and Appendix D, read from `docs/thesis/dissertation.tex` with comments stripped, plus every table they `\input`. The figures are PDFs, so I checked every figure-borne number against the data the figure is drawn from (`data/results/ch5_s531_unopposed`, `ch5_defended`, `ch6_further_analyses`).

**Result:** 14 rows in `mechanical.jsonl`. One is a wrong number, two are interval formats, five are wording or rounding problems in medium-confidence claims, four are low, and two are leads from other agents (one confirmed, one cleared).

## Fix first (high)

1. **L7615, "19 to 32 s".** IP shuffle's time lost per later deployment is 18.48 s, so the prose should read "18 to 32 s". The comment trail rounded it to 18.5 first, then to 19.
2. **L7831, "ρ … [−0.19, 0.05]".** This interval is still in square brackets after yesterday's change to parentheses. The values are right.
3. **L935 against Table `tab:lineage-configurations`** (lead from another agent). The prose says "more than 80 %", but the table and Zhang p. 33 say "reaching 0.8".

## Medium

4. **L10361.** A third interval form, "(95 % interval 0.09 to 0.12)". Harmonise it to "(0.09, 0.12)".
5. **L8597 and L9192, "about two thirds".** Appendix D.6 gives 0.63 (0.61, 0.65), and that interval excludes 2/3.
6. **L8983–8985, the random strategy at 33 % and 75 %.** These numbers come from the seven-mechanism random row. Appendix D.1 and L8997 name random over MTDShield's own four mechanisms as the control, and that row gives 56 % and 80 %. The qualitative claims hold on either row.
7. **L7869 and L9242, the MTDShield decision shares.** These come from 100 runs, which Appendix D.1 says. The body says every configuration runs on 1 000 seeds and does not say 100.
8. **L7856–7859, "the host-layer mechanisms … 0.96 or more" and "the service-layer mechanisms … 0.84 or more".** These are true only of the layer means. Taken mechanism by mechanism they are false: complete and host topology shuffle reach 0.95, and OS diversity reaches 0.68.
9. **Table `tab:experiment`, "Target hosts: 2"** (lead from another agent). Not a mismatch, because L6151 says "two target hosts in place of five". But the table cell alone reads as if it conflicts with §2.2.1.

## Low

- **L10380, "the five".** A sixth row, "random, MTDShield's four", also reaches 1.00.
- **L10493, "four mean durations that several tactics share".** There are five; the fifth, 22.5 s, moves with the 45 s.
- **L8911.** `subsec:dwell-times` does not say the attack flows "almost never" record durations.
- **L9358, "four MTD attacker models".** Elsewhere the text says three, beside ours.
- **L8598, "all of it for c₁".** The point estimate closes 94 % of c₁'s gap; the intervals meet.

## Checked and fine (not in the jsonl)

- **Abstract and Chapter 1:** 92 % and 36 %; seven mechanisms at six intervals; 38 attack flows; six attack actions; two properties in full and three in part, against at most one.
- **Table 5.2's ratios:** 5–16× ASP, 2.4–3.3× NCR.
- **The aio-coverage figure:** unmapped steps 26–47 %; 179–947 distinct openings; the baseline attacker's 3 openings; parting at step 2 (c₁) to step 4 (c₃).
- **Disruption:** blocked attack actions 0.35–0.39, 0.95/0.15 and 0.07/0.01; time lost 242–324, 493, 60 and ≤26 s; first deployment 204–232 s.
- **ρ range:** −0.24 to 0.25.
- **The attack-profile spread claims (§5.3.3):** within 0.14 and ≥0.24, and c₃ furthest at 500 and 1 000 s.
- **Ablation counts:** 29/7/24 of 60; 0.25–1.47; six to ten of ten.
- **Failure matrix:** 0.76–0.83 against 0.08–0.10; the time-lost intervals include zero.
- **Vulnerability memory:** 0.73/0.69 and 0.92/0.69.
- **Appendix D.6's numbers and Chapter 6's restatements of them:** 2.18–4.59 per minute, 32–56 %, 15–30 %, 0.09→0.45 against 0.66.
- **MTDShield against random and the ASP-reduction layer order:** hold at every interval.
- **Appendix D.3:** the 0.11 lead at 500 s.
- **The tactic-to-action mapping:** 8 of 15 tactics mapped.
- **Every chapter, section, table, equation, appendix and threat `\ref` in scope:** each target says what the sentence says, except L8911 above.
