---
status: guidance record (2026-10-05), gathered for the Section 4.4.2 redraft
created: 2026-10-05
topic: "How the field presents parameter values that have no data (judgement values) and the sensitivity test on them: best practice, pitfalls, structure"
---

# Presenting judgement parameters and their sensitivity test

Gathered 2026-10-05 after Section 4.4.2 rounds 1–5 (Marc: "we're just cycling
the same vague and hard-to-follow reasoning ... typically means the structure
is wrong"). Two sweeps: the methodology sources on disk
(`docs/sources/methodology/`, `docs/sources/extractions/`) and a web sweep.
Quotes were checked against full text unless marked. STRESS wording is from
the on-disk copy, so check it against the published version before citing.

## 1. What the field does

| Source | Guidance |
|---|---|
| Grimm et al. 2020, ODD second update (*JASSS* 23(2) 7; S1) | Parameter table: "name, meaning, units, type, default value, range of values analyzed ... where the values came from, e.g. literature, unpublished data, experiments, expert opinions"; give "the basis for all parameter values"; rationale "strongly recommended because it makes the model seem less arbitrary"; summary in the main text, detail in a supplement (§4.3). |
| Grimm et al. 2014, TRACE (*Ecol. Model.* 280, 129–139) | Table of "all model parameters, their meaning, units, reference values, range, and data source". Parameterisation, data evaluation and model analysis are **separate elements**. Values from "authors' own data and knowledge" must be identifiable. |
| Monks et al. 2019, STRESS (*J. Simulation* 13(1) 55–67) | Separate items: 3.3 input parameters (state ranges; justify the chosen distribution), 3.4 assumptions ("Where data or knowledge of the real system is unavailable what assumptions are included ... parameter values, distributions"). Experimentation is its own section (§4). Example table source cell: "Expert Opinion (n = 3)". |
| Briggs et al. 2012, ISPOR-SMDM TF-6 (*Med. Decis. Making* 32(5) 722–732) | One-way SA needs "the parameter's point estimate and a defensible range". VI-6: arbitrary ranges (±50 %) "can be used as a measure of sensitivity, [but] should not be used to represent uncertainty". VI-8: little information means a broad range; "Never exclude parameters ... on the grounds that there is insufficient information." VI-13: ranges "disclosed and justified", appendices appropriate. |
| Robinson 2008/2017 (conceptual modelling) | Assumptions fill gaps in knowledge, simplifications are deliberate; document as a list, appendix. |
| Law 2008 (WSC) | Assumptions document: "what simplifying assumptions were made and why"; technical analyses in appendices. |
| Sargent 2011 (WSC) | Assumptions "clearly stated"; "general knowledge" is a legitimate basis; "If behavior data are not available, high model confidence usually cannot be obtained." |
| McQueen et al. 2006 (time-to-compromise) | "We have used expert elicitation or have made simple assumptions when data is unavailable"; "Somewhat arbitrarily, we decided to use 8 hours (one working day)" after a published anchor. The anchor-then-stated-choice move in so many words. Mendonça 2023 marks unsourced rows "?"; Bland 2020: rates "notional". |

## 2. What the sensitivity test is for

- **Robustness of the conclusions**, not justification of the value (Leamer in
  Saltelli 2010: conclusions are sturdy only if "the neighborhood of
  assumptions is wide enough to be credible and the corresponding interval of
  inferences is narrow enough to be useful"; Pianosi 2016 §2.6; ten Broeke
  2016 §2.3).
- **Which assumptions matter**, i.e. ranking and screening (Pianosi §2.2.4; TRACE: "if
  the parameters to which the model is most sensitive are the most uncertain
  ones, the entire model will be quite uncertain").
- Not calibration (Pianosi §2.4). Not validation (Eddy et al. 2012).
- The output tested must be the output the claims rest on (Pianosi §4.1).

## 3. Pitfalls, against Section 4.4.2 as of round 5 (commit 7c3b9598)

| Pitfall | Source | 4.4.2 round 5 |
|---|---|---|
| Rationale and test in one unit | TRACE (separate elements), STRESS §3 vs §4 | **Hit.** P5 opens by re-arguing the judgement, then the design, criterion and result. |
| Walking each value in prose instead of a table | ODD, TRACE, STRESS | **Hit.** P4 walks the nine values, each sentence mixing what the tactic does, its bounds and its value. |
| Arbitrary uniform ranges presented as uncertainty | Briggs VI-6 | **At risk.** The bands are ×0.5–×2 and ×0.25–×4. Defensible only as a measure of sensitivity, so say so. |
| A one-at-a-time limitation left unstated | Saltelli et al. 2019; ten Broeke §6.2 | **Hit.** Interactions not tested, and not said. |
| Output not the claims' output | Pianosi §4.1 | **Partial.** Hosts reached for the APT attacker model only; chapter 5's APT-versus-baseline orderings are not tested across the bands. |
| Hiding that a value is judgement | McQueen, STRESS, TRACE | Avoided: "Judgement" in Table 4.2's source column. |
| Excluding no-data values from the test | Briggs VI-8 | Avoided: every shared value moved. |
| No criterion fixed before the run | Briggs VI-13 | Avoided: the criterion and bands were fixed before the run (`ch5_s51_sensitivity_findings.md` §2). |

## 4. Structure the sources point to (synthesis)

1. The principle: where values come from (MTDSim's attack-action times, else
   judgement), and the distribution with its reason (STRESS 3.3).
2. One parameter table: value, basis, the bounds that place it, and the band
   tested. The table carries the per-value reasons.
3. The values from MTDSim, briefly.
4. The judgement values: stated once as assumptions, with the shared logic (a
   range between known times, a value chosen inside it), one worked example and the McQueen
   precedent, and then stop.
5. The robustness test, as its own unit: purpose (are the conclusions robust,
   and which values matter); factors; bands and why; output and the criterion,
   fixed before the run; one-at-a-time, interactions untested; one line of
   finding. Detail in Appendix C.1.
