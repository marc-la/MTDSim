# Threats-to-validity terminology

**Status:** durable (Marc, 2026-10-13). Load before drafting or scrutinising any item in §6.5 (T1–T12). Records the field's conventional wording for a threat item so each item uses standard verbs and nouns, not invented or rhetorical ones. It sits under `voice.md` and `terminology.md`: the dissertation's own terms (NCR, base weights, attack action, …) stay as ratified; this file governs the *validity* vocabulary around them.

Sources marked **[V]** were verified from full text (page/section given); **[M]** is from memory or a secondary source and must be checked against a print copy before it is quoted in the dissertation. Research record: handoff `2026-10-11_ch6_1_redraft_scrutiny.md` §135.

## (a) The item's moves and their standard wording

Order: **threat → mitigation → what remains** (Verdecchia & Bogner 2025 §3.10 [V]: state the threat, "supported by how you tried to mitigate it", then "discuss which threats remain and how likely it is that they impact your results").

| Move | Conventional wording | Source |
|---|---|---|
| State the threat (internal) | "X may confound Y"; "a third factor may affect …"; "X is a plausible alternative explanation for …" | Runeson & Höst 2009 p. 154 [V]; Shadish et al. 2002 ch. 1–2 [M] |
| State the threat (construct) | "X measures Y only in part"; name the construct and the operation separately | Sjøberg & Bergersen 2023 §3.4 [V]: "state threats and constructs clearly and explicitly" |
| State the threat (external) | "the results may not generalise to …"; "interaction of setting and treatment" | Wohlin et al. 2012 ch. 8 [M] |
| Mitigation | "to mitigate this threat, we …"; "this threat was lowered by …"; "countermeasure" | Runeson & Höst p. 154 [V]; Verdecchia & Bogner §3.10 [V] |
| Untested / assumed | "we cannot rule out X as a cause of …"; "we have not investigated …"; "we assumed …" | Shadish et al. [M] ("rule out"); Sjøberg & Bergersen p. 5 [V]: "a plausible model would be … However, we have not investigated the causes of our findings." |
| Residual / bound | "the threat remains"; "we make no claims of generalisation beyond …"; "results are as general as the supporting data" | Verdecchia & Bogner §3.10 [V]; Sjøberg & Bergersen p. 5 [V]; de França & Travassos 2015 §4.4 [V] |

## (b) Hedging a causal claim

- The canonical vocabulary is **plausibility**: an alternative explanation is *plausible* or *implausible*; a design *rules out* or *renders implausible* an alternative; an inference is *approximately true*, never proven (Shadish et al. [M]; validity as "the approximate truth of an inference", p. 34 [V via secondary]).
- **"Likely explains"** is a causal attribution; a threats section names what could also explain the result. Prefer: "is consistent with", "a plausible explanation is", "we cannot rule out".
- One hedge per inferred claim (voice rule) still holds; pick it from this vocabulary.

## (c) Nouns

| Use | For | Not |
|---|---|---|
| threat (to validity) | a reason the inference may be partly or completely wrong (Shadish et al. ch. 2 [M]) | risk, weakness, caveat |
| plausible alternative explanation | a rival cause (internal) | rival, competing story |
| confound / third factor | a variable that varies with the treatment | — |
| mitigation | what was done to reduce a threat | defence, guard |
| assumption | what was taken as given (de França & Travassos §4.2–4.3 [V]: "simulation model simplifications (assumptions)", "hidden underlying model assumptions") | — |
| limitation | a scope chosen on purpose; threats are "issues that are difficult to mitigate completely" (Verdecchia & Bogner §3.10 [V]) | — |
| intended purpose; domain of applicability | what a simulation model is valid *for* (Sargent 2011 pp. 183, 186 [V]) | — |

## (d) Each type's question (Shadish 2010 / 2002 Table 2.1 [V via secondary]; Wohlin ch. 8 [M])

- **Conclusion:** is the covariation between treatment and outcome correctly inferred? Named threats: low statistical power, violated assumptions of statistical tests, fishing and the error rate, reliability of measures, random heterogeneity. Simulation: "considering only one observation … rather than central tendency and dispersion" (de França & Travassos §4.1 [V]).
- **Internal:** does the covariation reflect a causal relationship, or a factor not controlled or measured? Named: history, instrumentation, selection, … Simulation: "simulation model simplifications (assumptions) forcing the desired outcomes"; "inappropriate experimental design (missing factors)" (§4.2 [V]).
- **Construct:** do the operations represent the constructs? Named: inadequate preoperational explication of constructs, mono-operation bias, mono-method bias, confounding constructs. Simulation: "inappropriate real-world representation by model parameters"; "inappropriate model calibration data and procedure" (§4.3 [V]).
- **External:** does the relationship hold over other persons, settings, treatments and measures? Named: interaction of selection / setting / history and treatment. Simulation: "simulation model not based on empirical evidence" (§4.4 [V]); without model validity "no conclusion can be draw[n] about the phenomenon, but only about the model itself" (§4.3 [V]).

## (e) Weak forms the critiques flag

- A "laundry list" of threats, "only superficially considered in a checklist-like manner" (Wyrich & Apel 2024, reporting Verdecchia et al. 2023 [V]).
- Threats as "an enforced afterthought" (Lago et al. 2024 [V, abstract]).
- A threat filed under the wrong type: "If a definition is introduced in a paper, it should be followed" (Sjøberg & Bergersen §3.2 [V]).
- A mitigation asserted from intuition with no evidence (Wyrich & Apel [V]).
- Invented verbs for the residual ("rests on", "hinges on", "is anchored in"): use (a)'s wording.

## Citations

- Shadish, W. R., Cook, T. D., Campbell, D. T. (2002). *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*. Houghton Mifflin.
- Wohlin, C. et al. (2012). *Experimentation in Software Engineering*, ch. 8. Springer. (In the bib as `wohlin2012`.)
- Runeson, P., Höst, M. (2009). Guidelines for conducting and reporting case study research in software engineering. *EMSE* 14:131–164.
- de França, B. B. N., Travassos, G. H. (2015). Simulation based studies in software engineering: a matter of validity. *CLEI EJ* 18(1), paper 4.
- Sargent, R. G. (2011). Verification and validation of simulation models. *Proc. WSC*, 183–198. (In the bib as `sargent2011`.)
- Verdecchia, R., Engström, E., Lago, P., Runeson, P., Song, Q. (2023). Threats to validity in software engineering research: a critical reflection. *IST* 164:107329.
- Verdecchia, R., Bogner, J. (2025). Notes on writing effective empirical software engineering papers. arXiv:2506.11002.
- Lago, P., Runeson, P., Song, Q., Verdecchia, R. (2024). ESEM '24, 314–324.
- Wyrich, M., Apel, S. (2024). Evidence Tetris in the pixelated world of validity threats. WSESE '24.
- Sjøberg, D. I. K., Bergersen, G. R. (2023). Improving the reporting of threats to construct validity. EASE '23. arXiv:2306.05336.
