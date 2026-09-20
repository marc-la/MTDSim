# anderson2016 — evaluation-section anatomy

Source read: /home/marc/GitHub/MTDSim/docs/sources/tactic_profiles/step_d/1_recon/Parameterizing_Moving_Target_Defenses.md (230 lines, IEEE NTMS 2016; md conversion clean, figure axis/legend text preserved as "picture text" blocks). Locators are md line numbers.

Paper's own research question / purpose: "we develop two analytical models based on closed-form solutions and Stochastic Petri Nets to analyze the effect of a dynamic platform technique based MTD on attack success rate" with the two models cross-validating one another, and the output "indicates the existence of parameter settings that decrease the security of the protected resource and settings that make MTD most effective" (line 15). Stated purpose of the model pair: "for the purpose of cross-validation" (line 21, 69).

## A. Skeleton of the evaluation portion

Whole paper is five sections; there is no separate setup section — parameters are declared inside the model section (III) and the results section (IV) is the entire evaluation.

- `### III. MODEL` (line 67) — model + parameter declaration (setup).
  - `### A. Closed-Form Mathematical Model` (line 75) — Eq. 1/2 and parameter semantics; Table I "CLOSED FORM MATHEMATICAL MODEL PARAMETERS" (lines 87–100).
  - `### B. Stochastic Petri Net` (line 81) — SPN construction; Table II "STOCHASTIC PETRI NET PARAMETERS" (lines 112–121).
- `### IV. RESULTS` (line 133) — results; the sweeps live entirely here.
  - `### A. Closed-Form Mathematical Model` (line 137) — Figs 3–6.
  - `### B. Stochastic Petri Net` (line 160) — Figs 7–10 (same scenarios re-run in the SPN).
- `### V. CONCLUSIONS` (line 195) — conclusions + future work; there is no discussion or limitations section.

Setup and results are two sections (III vs IV), with the result-section subsection headings mirroring the model-section subsection headings (A closed-form / B SPN in both).

## B. Setup — what is declared before any result

- Network configuration(s): none. The model is a single protected resource under a dynamic platform technique (DPT); the only "topology" quantity is `o`, "the number of MTD configurations; the defender chooses this value" (line 79). No network size or topology.
- Attacker model / scenarios: a single threat model with "four particular facets" (line 71): (1) "a persistent attack that takes a certain amount of time and can be resumed" (line 71); (2) "the attacker must implant some malware and persist on a targeted host" (line 71); (3) "detecting and attributing an attacker will deter further efforts" (line 71); (4) "a nondeterministic implant detection process" (line 73). Attacker strength is encoded in two parameters only: `e` ("a function of the budget and/or skill level of the attacker", line 79) and `c` cyber attack length ("The practitioner should use a high value for c (e.g., months) to model nation state attackers and a low value to model recreational hackers (e.g., hours)", line 79). Scenarios are not named; the paper refers to "DPT-based MTD scenarios" (line 135) without enumerating them. The six-phase attack sequence of Fig. 1 (survey, tool, implant, pivot, damage/exfiltration, cleanup; line 23) is motivation, not an evaluated scenario.
- Defence conditions: one mechanism (DPT-based MTD, i.e. VM reset / platform churn, line 77). Defender-chosen parameters: `o` configuration count and `h` churn time (line 79); `p` probability of implant detection is "a function of the skill level of the attacker and the skill level of the defender" (line 79). No-defence baseline: yes, but as a point on the curve rather than a separate condition: "The left most point in each curve (configuration count equal to 1) represents a protected resource without DPT-based MTD instrumented" (line 158).
- Parameter table: yes, two. Table I (lines 87–100) columns: Parameter Name | Description — seven rows (a, e, o, p, i, c, h). No values, no ranges, no defaults. Table II (lines 112–121) columns: Transition Name | Function — four rows (TCHURN = 1/churn time; TDETECTION = probability of detection; TSUCCESS = 1−probability of detection; TSUFFICIENT = cyber attack length·configuration count / (churn time·2)). Distributions: SPN underlying model is "a continuous-time semi-Markov process" (line 102); TCHURN is a timed transition (line 106), TDETECTION/TSUCCESS immediate transitions with probabilities (line 108). The closed-form model carries two explicit simplifying assumptions: "configurations are distributed uniformly so the attacker will need to wait out half of the configurations on average" and "the probability an exploit is available is the same for all configurations" (line 77).
- Replications: none — both models are analytical. The SPN is solved numerically ("solved using techniques such as SOR, Gauss Seidel or Uniformization [12]", line 129). Horizon: "the probability the cyber attack will be successful, as well as the expected values of PID, PSI1, PSI200 and PCAS at time t" (line 129); the value of t used for the figures is not stated. Results "reflect the probability of attack success at a given moment in time" (line 135) — the moment is not stated.
- Statistics: none per condition. The only statistic is the cross-model agreement: "The mean square error between the closed-form and stochastic results is on the order of 10^−9" (line 193).
- Anything else declared: analysis software SPNP [3] (line 65, 102), with an implementation constraint that shaped the model: "Due to a limitation of the analysis software [3] which restricts each place to 200 tokens, two places model the successful implant count component (PSI1 and PSI200)" (line 102). Hardware: not stated.

## C. Results — how the numbers are shown

- Order of results: closed-form model first (Figs 3–6, one figure per swept parameter in the order attack length → exploit availability → churn time → detection probability), then the SPN re-run of the same four (Figs 7–10 in the same order). The order appears to follow the order the parameters are introduced in the Eq. 1 prose (line 77: exploit availability, implant detection, attack length, churn time) only loosely; the closed-form-then-SPN ordering follows the cross-validation purpose.
- Every figure in the evaluation portion (all eight are the same chart type: line chart, x = configuration count 0–100, y = probability of cyber attack success, three series):
  - Fig. 3 (caption line 146): series = attack length 8 h / 24 h / 48 h; y range 0–0.45. Caption: "Probability of cyber attack success versus configuration count and cyber attack length (closed-form model)."
  - Fig. 4 (line 151): series = probability exploit available 0.20 / 0.10 / 0.05; y 0–0.4. "…versus configuration count and probability of exploit availability (closed-form model)."
  - Fig. 5 (line 162): series = churn time 240 / 60 / 30 minutes; y 0–0.6. "…versus configuration count and churn time (closed-form model)."
  - Fig. 6 (line 167): series = probability of detection 0.01 / 0.02 / 0.04; y 0–0.25. "…versus configuration count and probability of implant detection (closed-form model)."
  - Figs. 7, 8, 9, 10 (lines 172, 181, 186, 191): identical axes/series/ranges to 3–6, "(stochastic model)".
  - No facets, no error bars (analytical).
- Every table: Table I and Table II are parameter-definition tables in Section III (see B); no results tables.
- Baseline appears in each figure as the x = 1 point of every curve (line 158), not as a separate line.
- Comparisons in prose: direction-only, with a mechanism sentence attached to each: "This figure shows shorter cyber attacks are more likely to succeed. This is because a shorter attack will require fewer implants which provide less opportunities for an attack-ending detection" (line 156); "cyber attacks are more likely to succeed if an exploit is more likely to be available. This is because…" (line 156); "cyber attacks are more likely to succeed for higher churn times. This is because…" (line 156); "cyber attacks are more likely to succeed if the probability of detection is lower. This is because…" (line 156). No magnitudes ("reduced by X%") are given anywhere; the only number in the results prose is the 10^−9 MSE (line 193). Recommendation-style language appears in the conclusions: "given knowledge of the attacker strength and vulnerability in terms of attack length and exploit availability, we can identify the best defense parameter settings in terms of configuration count, implant detection probability, and churn time" (line 197).

## D. Narrative — the claims, in order

1. Scope disclaimer first: figures "reflect the probability of attack success at a given moment in time; they do not consider the attacker goals which may have more (nation state) or less (recreational) consequences" (line 135).
2. Four monotone "basic trends", one per swept parameter, each with its causal sentence (line 156; quoted in C).
3. "In addition to the expected basic trends, in all four graphs, we see two interesting phenomena" (line 158):
   - (a) "it is possible to make a system less secure by instrumenting a DPT-based MTD if the parameterization is unfavorable; this is because the attacker may have exploits for one platform in the MTD but not others" (line 158); a "breakeven point" in configuration count above which DPT-MTD is beneficial, which "is higher for shorter campaigns, higher exploit availabilities, higher churn times and lower probabilities of detection" (line 158).
   - (b) "there is an optimal configuration count for the attacker. This optimal configuration count is lower for longer cyber attacks, higher exploit availabilities, lower churn times and higher probabilities of detection" (line 158).
4. Cross-validation: "Figures 7 - 10 generated from the SPN model match Figures 3 - 6 generated from the closed-form solutions very closely. This close match validates the analysis results presented in these figures. The mean square error … is on the order of 10^−9" (lines 174, 193).
5. Conclusions restate (a) as "it is possible to mistakenly instrument an MTD in a way that makes the protected resource more vulnerable to attack" and turn it into a defender-tuning claim (line 197).

Claims about the ATTACKER from the data: yes, one — the "optimal configuration count for the attacker" (line 158), i.e. a value of the defender's parameter that maximises the attacker's success probability, read off the curve peaks. Attacker properties themselves (attack length, exploit availability) are inputs, not inferred; the paper explicitly declines to rank attackers by the output ("The lower success rate associated with higher cyber attack length does not mean that nation state attackers are less dangerous than recreational hackers because not all cyber attacks are equal", line 79).

## E. Sensitivity / parameter analysis

Present: yes — the parameter sweep IS the results section; there is no other result.

- Parameters varied and ranges (all read from figure legend/axis text; the prose never restates the values):
  - `o` configuration count — the x-axis of every figure, 0–100 by axis ticks of 10 (lines 144, 149, 154, 165); step of the underlying evaluation not stated. This is the only parameter swept continuously.
  - `c` cyber attack length — 8, 24, 48 hours (Fig. 3/7; lines 144, 170).
  - `e` probability exploit available — 0.05, 0.10, 0.20 (Fig. 4/8; lines 149, 179).
  - `h` churn time — 30, 60, 240 minutes (Fig. 5/9; lines 154, 184).
  - `p` probability of detection — 0.01, 0.02, 0.04 (Fig. 6/10; lines 165, 189).
- Design: one-at-a-time. Each figure varies configuration count (x) against one other parameter at three levels (series); the remaining three parameters are held fixed. The held-fixed default values are not stated anywhere in the paper — neither in Table I, the model text, nor the results prose. Not factorial.
- Range justification: not stated for any parameter. The only justification-flavoured text is the qualitative guidance on `c` ("months" for nation state, "hours" for recreational; line 79) and on `e` ("a function of the budget and/or skill level of the attacker", line 79). No citation, no "for illustration" phrase; the three-level values are simply presented.
- Reporting: figures only (eight line charts, x = configuration count, y = attack success probability, series = the second parameter at three levels), each captioned "…versus configuration count and <parameter> (<model>)". No sensitivity table.
- Where it sits: inside the results section (IV.A and IV.B); it is the whole of Section IV. No appendix.
- Claim supported: (i) the four monotone trends; (ii) the existence of a breakeven configuration count (MTD can be net-harmful below it) and of an attacker-optimal configuration count, both of which shift with each swept parameter in the direction stated at line 158; (iii) via the duplicate SPN sweep, the cross-validation of the closed-form model (line 174, 193).
- Distinctive convention: the whole evaluation is a 2-D "x = defender knob, series = one other knob at three levels" sweep repeated four times, then the entire set repeated in the second model so the two model families can be compared figure-for-figure (Fig. 3↔7, 4↔8, 5↔9, 6↔10).

## F. Discussion / limitations

No discussion section; interpretation is folded into the results prose as one causal sentence per trend (line 156) and the "two interesting phenomena" paragraph (line 158). Limitations appear only as future work in the conclusions:

- "First, we will instrument a simulation or emulation involving real, specific DPTs to further validate our models." (line 201)
- "Third, our future threat models will consider attacks that must be restarted." (line 201) — paired with the earlier admission "We note that in some cases attacks may have to restart from scratch; if this is the case, the attack can never succeed if the churn rate is faster than the completion rate" (line 71).
- "Finally, we will relax four assumptions: that dynamic platform configurations are uniformly distributed, that the probability an exploit is available is the same for all configurations, that the adversary must implant malware in order to prosecute a cyber attack and that detection and attribution will deter an attacker." (line 201)
- Attacker-realism concession: "our model does not apply to a DoS attack" (line 71); the CNE-vs-CNA distinction is drawn against Okhravi et al. (line 53) rather than as a limitation.
- Comparability caveat: the only one is the "given moment in time" disclaimer (line 135). No threats-to-validity language.

## G. Transferable vs purpose-specific

Transferable to an honours dissertation evaluating existing MTD mechanisms against a new attacker model on a simulator:
- Parameter-definition table with a one-line semantic gloss per symbol and an explicit note of who "chooses" each parameter (attacker vs defender vs joint; line 79, Table I) — cleanly separates attacker-model inputs from defender knobs.
- Threat model declared as a short enumerated list of facets (line 71–73) before any parameter is introduced.
- No-defence baseline embedded as the degenerate point of the swept defender parameter (configuration count = 1; line 158) rather than a separate condition.
- One figure per swept parameter with a fixed figure template (same x, same y, three series), and one causal sentence per trend in the prose (line 156).
- Naming non-monotone features (breakeven point, attacker-optimal point) and stating how each shifts with every other parameter (line 158).
- Stating explicitly what the output metric does not capture (line 135, 79).

Purpose-specific / venue artefacts:
- The duplicated sweep across two model families and the MSE-as-validation statistic (line 193) exist because the paper's purpose is cross-validation of two analytical models, not mechanism comparison.
- Absence of any replication, seed, CI or horizon reporting follows from the models being analytical; a simulator evaluation cannot inherit this.
- Not stating the held-fixed parameter values for each sweep, and not justifying the three-level ranges, is a gap rather than a convention to copy.
- The 200-token SPNP workaround (line 102) is tool-specific.
- Single-host, single-mechanism, topology-free scope (no network) — a consequence of modelling a DPT, not a template for a network simulator evaluation.
