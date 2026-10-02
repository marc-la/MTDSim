# Results presentation conventions — extraction notes (multi-source)

> A multi-source evidence base for [`docs/workflows/results_presentation_standard.md`](../../workflows/results_presentation_standard.md): reporting standards and style guides (NCHS, ABS, UK Government Analysis Function, Australian Government Style Manual, APA 7, SI Brochure, SAMPL, CONSORT, Cole 2015, Arcuri and Briand 2014, Hoefler and Belli 2015, Wilke 2019, Cumming 2014, Rougier et al. 2014, Weissgerber et al. 2015, Lakens 2013).
> Compiled 2026-10-02 by a research subagent from open-access fetches only; confidence tags per item. Quote in the thesis only items tagged verified-quote; re-check paraphrase-verified items first.

---


Compiled 2026-10-02 for the chapter 5 results-presentation standard. Only open-access or free sources were fetched. Every quote below was read in the fetched text unless the tag says otherwise.

**Confidence tags**
- **verified-quote**: the words were read in the raw fetched text (PDF text extraction or raw HTML), and the locator was seen in that text.
- **paraphrase-verified**: the content was seen, but only through a fetch summariser or a secondary page that reproduces the source. The wording may not match the original, so re-check it before quoting it in the thesis.
- **unverified**: not seen in a fetched source. It is recorded only so the gap is visible.

**Locator convention**: the printed page or section where it was seen. "PDF p. N" means the Nth page of the PDF file. "Locator unverified" means no locator was visible.

---

## Part A — Priority-1 findings, verbatim

### (a) NCHS / NVSS small-number reliability conventions

There are **three distinct NCHS regimes**, and they must not be conflated:

1. **Vital-statistics rates, data years up to 2022: "fewer than 20 events" → asterisk in place of the rate (suppression).**
   - Kochanek KD, Murphy SL, Xu JQ, Arias E. *Implementation of New Data Presentation Standards for Rates and Counts for Mortality*. NCHS, 2024. URL: https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/mortality/presentation-standards-mortality-2024.pdf. Locator: Section 2, p. 6.
     > "Suppression of unreliable rates—Beginning with 1989 data, an asterisk is shown in place of a crude or age-specific death rate based on fewer than 20 deaths, the equivalent of an RSE of 23% or more. The limit of 20 deaths is a convenient, if somewhat arbitrary, benchmark, below which rates are considered to be too statistically unreliable for presentation."
     > "Rates are replaced by asterisks if the calculated RSE is 23% or more." (applies when the denominator is survey-based: ACS/CPS)
     — verified-quote
   - Klein RJ, Proctor SE, Boudreault MA, Turczyn KM. *Healthy People 2010 criteria for data suppression*. Statistical Notes no. 24, NCHS, July 2002. URL: https://www.cdc.gov/nchs/data/statnt/statnt24.pdf. Locator: p. 5.
     > "Rates, proportions, and simple ratios from NVSS are considered statistically unreliable and are suppressed if they are based on fewer than 20 events, which corresponds to an RSE of 23 percent or greater."
     — verified-quote
   - Parker JD, Talih M, Irimata KE, et al. *NCHS data presentation standards for rates and counts*. Vital Health Stat 2(200), 2023. DOI 10.15620/cdc:124368. URL: https://www.cdc.gov/nchs/data/series/sr_02/sr02-200.pdf. Locator: p. 3 ("Previous Guidelines — Vital statistics"). This source gives the rationale:
     > "the presentation guidance for NVSS was to suppress rates with fewer than 20 events in the numerator … This 20-event threshold for vital rates corresponds to an RSE of 23% for a Poisson-distributed count variable. For a Poisson variable, SE is the square root of the number of events." … "Rates with an RSE of 23% or more were suppressed or flagged for internal review."
     — verified-quote
     (The arithmetic: RSE = 100/√D, and D = 19 gives 22.9 %.)
   - The same page records the parallel survey rule, the **"30/30 rule"**: rates from the National Health Care Surveys "were suppressed when based on a sample size less than 30 … Rates were flagged as unreliable if RSEs were greater than 30%." — verified-quote (p. 3)
   - **Flagging without suppression** also occurs. CDC WONDER mortality help (https://wonder.cdc.gov/wonder/help/ucd.html, section "Crude Rates") says: "Rates are marked as 'unreliable' when the death count is less than 20," while counts of 0–9 are suppressed. — paraphrase-verified (through the fetch summariser)

2. **Vital-statistics rates, data years 2023 onwards: the threshold is now *10* events plus a relative-CI-width test.** The 20-event rule is retired.
   - Kochanek et al. 2024, Section 3, p. 18:
     > "Beginning with 2023 data, an asterisk is shown in place of a crude or age-specific death rate based on fewer than 10 deaths. The limit of 10 deaths is a minimum benchmark, below which rates are considered to be too statistically unreliable for presentation. … the relative width of the appropriate 95% confidence interval … should be less than or equal to 160% for the estimate to be presented. If the relative width is greater than 160%, an asterisk is presented."
     — verified-quote
   - Parker et al. 2023, Vital Health Stat 2(200), Table A, p. 4: "Estimated rates should be based on a minimum sample size and effective sample size (when applicable) of 10 in both numerator and denominator. … Estimated rates should have a relative CI width of 160% or lower." The same document (p. 7) says: "For vital statistics, a CI threshold of 135.9% … directly corresponds to the sample size criterion of 10 or more events." — verified-quote

3. **Proportions (any NCHS data system): no minimum number of events.** The standard instead sets denominator n ≥ 30 and Clopper–Pearson CI-width rules.
   - Parker JD, Talih M, Malec DJ, et al. *National Center for Health Statistics data presentation standards for proportions*. Vital Health Stat 2(175), August 2017 (revised 2018 and 2021). URL: https://www.cdc.gov/nchs/data/series/sr_02/sr02_175.pdf. Locator: Table, p. 2 (all verified-quote):
     > **Sample size:** "Estimated proportions should be based on a minimum denominator sample size and effective denominator sample size (when applicable) of 30. Estimates with either a denominator sample size or an effective denominator sample size (when applicable) less than 30 should be suppressed. If the number of events is 0 (or its complement), then the denominator sample size should be used to obtain confidence intervals. If all other criteria are met for presentation, an estimate based on 0 events (or its complement) should be flagged for statistical review by the clearance official. The review could result in either the presentation or the suppression of the proportion."
     > **Confidence interval:** "If the sample size criterion is met, calculate a 95% two-sided confidence interval using the Clopper-Pearson method, or the Korn-Graubard method for complex surveys, and obtain its width."
     > **Small absolute CI width:** "If the absolute confidence interval width is greater than 0.00 and less than or equal to 0.05, then the proportion can be presented if the number of events is greater than 0 and the degrees of freedom criterion (below) is met. If the number of events is 0 (or its complement) … then the estimate should be flagged for statistical review …"
     > **Large absolute CI width:** "If the absolute confidence interval width is greater than or equal to 0.30, then the proportion should be suppressed."
     > **Relative CI width:** "If the absolute confidence interval width is between 0.05 and 0.30 and the relative confidence interval width is more than 130%, then the proportion should be suppressed." / "… less than or equal to 130%, then the proportion can be presented if the degrees of freedom criterion below is met."
     > **Complementary proportions:** "If all criteria are met for presenting the proportion but not for its complement, then the proportion should be shown. A footnote indicating that the complement of the proportion may be unreliable should be provided."
   - **Suppressed and flagged are different outcomes**, and both get a footnote (p. 2): "estimates identified as unreliable will be suppressed. Other estimates will be flagged for statistical review by the clearance official. … When an estimate is flagged or suppressed, a footnote indicating the reason the estimate has been flagged or suppressed should be provided in the publication." Also p. 5: "In all publications, unreliable estimates, whether presented or suppressed, should be identified with a footnote." — verified-quote
   - **No event minimum for proportions; 20 events stays for vital rates** (p. 5): "For the NCHS Data Presentation Standards for Proportions, there is no minimum number of events (i.e., numerator size). … Rates calculated from vital statistics will continue to use the criterion of requiring 20 or more events for reporting." (Report no. 200 later replaced this with 10 events, from 2023.) — verified-quote
   - **Why proportions of 0 or 1 are flagged** (p. 3): "If the number of numerator events is 0 or equal to the denominator (the complement of 0 events), the estimated proportion will be 0 or 1, respectively. As a result, the estimated variance of the proportion will be 0, and the effective sample size will be undefined. In these cases, the sample size should be used … estimates based on 0 events (or the complement) that meet absolute CI and degrees of freedom criteria should be flagged and considered for presentation after statistical review … to confirm the validity of the point and interval estimates." — verified-quote
   - **Why RSE was dropped for proportions** (p. 3): "when dividing the SE by very small proportions, the RSE can be too conservative, and when dividing the SE by very large proportions, the RSE can be too liberal. … The NCHS Data Presentation Standards for Proportions rely on both the relative and absolute CI widths to reduce the impact of this property." — verified-quote
   - **Why not Wald intervals** (p. 3): "the commonly used Wald CI [p ± 1.96 × SE(p) for a two-sided 95% CI] is known to perform poorly for proportions … sometimes producing negative lower bounds for small proportions or upper bounds greater than 1 for large proportions … greater undercoverage for smaller and larger proportions." Also p. 5: "whenever space permits, appropriate CIs should be provided, rather than just SEs." — verified-quote
   - Departures are allowed when justified (p. 2): "Departures from the Standards should be justified. In reports in which estimates are evaluated individually, a particular estimate not meeting the Standards could be identified as unreliable but not be suppressed if it can be interpreted appropriately in the context of subject-specific factors and report objectives." — verified-quote

**Australian counterpart (ABS RSE flags)**: ABS uses an asterisk to *flag*, not suppress.
- ABS, Year Book Australia 2006 (cat. 1301.0), "Symbols and abbreviations". URL: https://abs.gov.au/ausstats/abs@.nsf/Previousproducts/F41289256D682C7CCA2570DD00827251?opendocument= — verified-quote:
  > "^ estimate has a relative standard error of between 10% and 25% and should be used with caution"; "* estimate has a relative standard error of between 25% and 50% and should be used with caution"; "** estimate has a relative standard error greater than 50% and is considered too unreliable for general use"
- ABS TableBuilder, "Confidentiality and relative standard error". URL: https://www.abs.gov.au/statistics/microdata-tablebuilder/tablebuilder/confidentiality-and-relative-standard-error — "Estimates with RSEs of 25% or more are not considered reliable for most purposes." … "Estimates with RSEs greater than 25% but less than or equal to 50% are annotated by an asterisk (*) to indicate they are subject to high standard errors and should be used with caution." — paraphrase-verified (through the fetch summariser)

### (b) A value that rounds to a bound it does not reach

- **APA 7th edition, *Numbers and Statistics Guide*** (APA instructional aid by T. Giuliano; source line: "American Psychological Association. (2020). Publication manual … (7th ed.)"). The APA site blocks automated fetches, so this copy was read: https://tpcjournal.nbcc.org/wp-content/uploads/2021/08/APA-Numbers-Statistics-Guide.pdf (the original lives at https://apastyle.apa.org/instructional-aids/numbers-statistics-guide.pdf). Locator: p. 2, "Decimals" (citing Publication Manual §6.36) and "Statistics" (§§6.40–6.45). — verified-quote
  > "Report exact p values to two or three decimals (e.g., p = .006, p = .03). However, report p values less than .001 as "p < .001."" (the line wraps across columns in the PDF; the words are as shown)
  > "In tables and figures, report exact p values (e.g., p = .015), unless p is < .001 (instead write as "<.001")."
  > "Do not use a zero before a decimal when the statistic cannot be greater than 1 (proportion, correlation, level of statistical significance)."
  > "Round as much as possible while considering prospective use and statistical precision."
- APA 6th ed. p. 114, quoted by JASP (https://jasp-stats.org/2017/07/20/exact-p-values-upon-request-breaking-apa-guideline/): "When reporting p values, report exact p values (e.g., p = .031) to two or three decimal places. However, report p values less than .001 as p < .001." — paraphrase-verified (secondary quotation)
- **Cole (2015)** extends the rule beyond p values. Cole TJ. Too many digits: the presentation of numerical data. *Arch Dis Child* 2015;100:608–609. doi:10.1136/archdischild-2014-307149 (CC BY). URL: https://discovery.ucl.ac.uk/1463751/1/Arch%20Dis%20Child-2015-Cole-608-9.pdf (also PMC4483789). Locator: Table 1, p. 609. — verified-quote
  > p value: "Round up to one significant digit, within the limits shown in the examples. The lower limit may be smaller than 0.001, but never 0.000." (examples shown: ">0.9 … <0.001")
  > Percentage: "Integers, or one decimal place for values under 10%. Values over 90% may need one decimal place if their complement is informative." (example: 99.6%)
- **SAMPL**: "The smallest P value that need be reported is P <0.001, save in studies of genetic associations." (Lang & Altman 2013, p. 5) — verified-quote
- **The explicit generalisation to proportions and percentages (UK Government Analysis Function)**: *Using symbols and shorthand in tables*, published 11 January 2022. URL: https://analysisfunction.civilservice.gov.uk/policy-store/symbols-in-tables-definitions-and-help/. Locator: "Recommended shorthand". — verified-quote
  > "low = a low figure but not a real zero. Use this shorthand to replace data points that appear as zero in a rounded table, but are not actually zero. … A zero or '0' should only be used when a data point is a true zero."
  > "Similarly, if you are producing a table of percentages and some round to 100% but are not actually 100%, you can use the shorthand [high] instead."
- Contrast: ABS uses one dash for both "nil" and "rounded to zero", so the two are *not* distinguished: "— nil or rounded to zero (including null cells)" (Year Book Australia 2006, symbols list). — verified-quote

### (c) Symbols for empty cells: not applicable vs not available

| Source | Not applicable | Not available / not obtained | Not published / suppressed | Nil or rounded to zero | Tag |
|---|---|---|---|---|---|
| APA 7 (Publication Manual §7.12, via TCS Education System LibGuide "Adapted from APA publication manual (7th ed.)", https://tcsedsystem.libguides.com/APA7/Tables) | **blank cell** | **dash**, explained in the general note | (none given) | (none given) | verified-quote (secondary reproduction; §7.12 locator unverified) |
| ABS, Year Book Australia 2006 symbols list | **". ."** | **"n.a."** | **"n.p."** "not for publication/not separately published" | **"—"** "nil or rounded to zero (including null cells)" | verified-quote |
| ABS current release (R&D, Government and PNP Organisations, 2024–25) https://www.abs.gov.au/statistics/industry/technology-and-innovation/research-and-experimental-development-government-and-private-non-profit-organisations-australia/latest-release | — | — | **"np"** "not available for publication but included in totals where applicable, unless otherwise indicated." | **"-"** "nil or rounded to zero." | verified-quote |
| ABS 5368.0.55.004 (2015) abbreviations | — | **"na"** "not available" | **"np"** "not for publication but included in totals where applicable" | **"–"** "nil or rounded to zero (includes null cells)" | verified-quote |
| UK Government Analysis Function (2022) | **[z]** | **[x]** | **[c]** confidential; **[u]** low reliability | **[low]** (not a true zero); **[high]** (rounds to 100%) | verified-quote |
| Australian Government Style Manual, "Tables" (updated 12 Dec 2024), https://www.stylemanual.gov.au/structuring-content/tables | "Don't leave cells empty. Use 'zero' or 'nil' or 'n/a' where there is no data. If it is numeric data, use the numeric zero (0). Only use zero if that is the true value." | (same sentence; no separate symbol) | — | — | verified-quote |

Exact APA 7 wording, from the LibGuide reproduction (verified-quote): "Empty Cells: If a cell cannot be filled because data are not applicable, leave the cell blank. Use a general or specific table note if you need to explain why the cell is blank or the element is inapplicable. If a cell cannot be filled because data were not obtained or are not reported, insert a dash in that cell and explain the use of the dash in the general note to the table."

An older wording (APA 6 era) runs the two cases together. Purdue OWL renders it as "Leave cells blank if the element is not applicable or if data were not obtained; use a dash in cells and a general note if it is necessary to explain why cells are blank." — paraphrase-verified (summariser). The APA 7 wording above, which separates the two cases, is the one to cite.

Rule against ambiguity (UK Analysis Function, "No to NA"; verified-quote): "We do not recommend using 'NA' to describe cells with no data. This is because this shorthand is ambiguous. Some people may read it as 'Not Applicable', while other people may read it as 'Not Available'." The same page says: "Whenever a table contains shorthand, you should mention it and explain what the shorthand means." It also says: "We do not recommend using symbols such as '. :', '*' or '†' anymore because they can be difficult to see" (accessibility).

**Is distinguishing the two required?**
- APA 7 requires it: blank for not applicable, dash for not obtained.
- ABS and the UK Analysis Function do it by convention, each with its own symbol.
- The Australian Style Manual does not; it lumps both under "zero/nil/n/a".
- No source allows the *same* symbol for both while also leaving that symbol undefined.

Not fetched: Chicago Manual of Style (paywalled) and ISO 80000-1 (paywalled). The SI Brochure has no empty-cell symbol convention.

---

## Part B — Rules by topic

### 1. Rounding and bounds

**R1.1 Round to significant digits set by the precision, not to a fixed number of decimals.**
Cole 2015, p. 608. URL above. Locator: p. 608 col. 1–2; Table 1, p. 609.
> "rules of the first type, specifying the number of decimal places and ignoring the number of significant digits, are inherently unsatisfactory" … "The general principle is to use two or three significant digits for effect sizes, and one or two significant digits for measures of variability."
— verified-quote

**R1.2 Means: give enough decimals for the SD to show two significant digits, or the SE to show one.**
Cole 2015, Table 1. "Mean: Use enough decimal places to give either the SD to two significant digits, or the SE to one significant digit." — verified-quote

**R1.3 A CI is rounded like its point estimate, perhaps with one fewer significant digit.**
Cole 2015, Table 1. "CI: Use the same rule as for the corresponding effect size … perhaps with one less significant digit." — verified-quote

**R1.4 Percentages: integers, or one decimal under 10 %. Choose decimals so that the range across groups shows two significant digits.**
Cole 2015, p. 608. "use enough decimal places to ensure two significant digits for the range of values across groups, eg, if the range is 10% or more use whole numbers, if less than 1% use two decimal places, and otherwise one. In practice percentages are usually given along with their corresponding frequencies, so precision is less critical as the exact values can be calculated." — verified-quote

**R1.5 A standardised mean difference (Cohen's d) takes one or two decimals.**
Cole 2015, Table 1. "For a standardised mean difference use one or two decimal places." — verified-quote

**R1.6 Ratios follow the "rule of four".**
Cole 2015, p. 608. "round the risk ratio to two significant digits if the leading non-zero digit is four or more, otherwise round to three." — verified-quote

**R1.7 Round only at reporting; compute at full precision.**
Cole 2015, p. 608–609. "It is important that any intermediate calculations are carried out to full precision, and that rounding is done only at the reporting stage." — verified-quote

**R1.8 Never print 0.000, 0 % or 100 % for a value that only rounds there. Print the bound ("< 0.001", "< .001") or a defined marker ([low], [high]).**
Sources: APA 7 guide p. 2; Cole Table 1; UK Analysis Function. Quotes in Part A(b). — verified-quote

**R1.9 Leading zero: SI and the Australian Style Manual always use one; APA omits it for statistics bounded by 1.** This is a declared choice and must be applied uniformly.
- BIPM, *The International System of Units (SI)*, 9th ed. 2019, §5.4.4, p. 145. URL: https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf. "If the number is between +1 and −1, then the decimal marker is always preceded by a zero. For example −0.234 but not −.234." — verified-quote
- Australian Government Style Manual, "Fractions and decimals" (updated 23 Aug 2022), https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/numbers-and-measurements/fractions-and-decimals: "Decimal values less than one have a '0' before the decimal point. Correct 0.59 Incorrect .59" — verified-quote
- APA 7 guide p. 2 (Part A(b)). — verified-quote

**R1.10 Grouping digits: SI uses a space ("1 000" is optional at four digits); APA and the Australian Style Manual use commas.**
- SI Brochure §5.4.4, p. 145: "for numbers with many digits the digits may be divided into groups of three by a space … Neither dots nor commas are ever inserted in the spaces between groups. … However, when there are only four digits before or after the decimal marker, it is customary not to use a space to isolate a single digit." — verified-quote
- APA 7 guide p. 1: "Use commas between groups of three digits in most figures of 1,000 or more." — verified-quote
- Australian Style Manual, "Choosing numerals or words", gives examples in comma style ("3,547.8 mm", "US$20,000"). — verified-quote (examples only; the rule is not stated)

**R1.11 One number format per table column.**
- SI Brochure §5.4.4, p. 145: "For numbers in a table, the format used should not vary within one column." — verified-quote
- APA 7 (LibGuide reproduction): "If possible, carry all comparable values to the same number of decimal places." — verified-quote

**R1.12 Precision follows the measurement; round as much as is reasonable.**
Lang T, Altman DG. *Basic statistical reporting for articles published in biomedical journals: the SAMPL guidelines*. In: Smart P, Maisonneuve H, Polderman A (eds). *Science Editors' Handbook*. EASE, 2013. URL: https://www.equator-network.org/wp-content/uploads/2013/03/SAMPL-Guidelines-3-13-13.pdf. Locator: p. 4, "Reporting numbers and descriptive statistics".
> "Report numbers—especially measurements—with an appropriate degree of precision. For ease of comprehension and simplicity, round as much as is reasonable."
— verified-quote

### 2. Empty cells and symbols

**R2.1 Not applicable gets a blank cell (APA) or a defined symbol. Not obtained gets a dash, explained in the general note.** (APA 7; Part A(c).) — verified-quote (secondary reproduction)

**R2.2 Use distinct, defined symbols for "not applicable", "not available", "suppressed/unreliable" and "rounds to zero". Never use the ambiguous "NA".** (UK Analysis Function; ABS; Part A(c).) — verified-quote

**R2.3 Define every symbol in the table, preferably above it or in its general note.**
- UK Analysis Function, "Layout of shorthand": "Whenever a table contains shorthand, you should mention it and explain what the shorthand means. The best place to do this is above the table." — verified-quote
- APA 7 general note (LibGuide): "A general note qualifies, explains, or provides information relating to the table as a whole and explains any abbreviations; symbols; special use of italics, bold, or parentheses; and the like." — verified-quote

**R2.4 Use 0 only for a true zero.**
- UK Analysis Function: "A zero or '0' should only be used when a data point is a true zero." — verified-quote
- Australian Style Manual, "Tables": "If it is numeric data, use the numeric zero (0). Only use zero if that is the true value." — verified-quote

**R2.5 A suppressed or flagged estimate carries a footnote that gives the reason.**
NCHS 2(175), p. 2. Quote in Part A(a). — verified-quote

**R2.6 Every suppression is either confidential or low-reliability; mark each with its own symbol.**
UK Analysis Function, under "u = low reliability": "reasons for suppression would either be for confidentiality purposes or low reliability. These are now identified separately in this list." — verified-quote

### 3. Small n and conditional summaries

**R3.1 Report the numerator and denominator of every percentage, and the n behind every summary.**
- SAMPL p. 4: "Report total sample and group sizes for each analysis. • Report numerators and denominators for all percentages." — verified-quote
- SAMPL p. 4, rates: "Identify the quantities represented in the numerator and denominator (e.g., the number of men with prostate cancer divided by the number of men capable of having prostate cancer)." — verified-quote
- CONSORT 2010 item 16: "For each group, number of participants (denominator) included in each analysis …". The Explanation adds: "For binary outcomes, (such as risk ratio and risk difference) the denominators or event rates should also be reported. … results should not be presented solely as summary measures, such as relative risks." (Moher D et al. CONSORT 2010 Explanation and Elaboration. *BMJ* 2010;340:c869, PMC2844943; read through Europe PMC: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC2844943/fullTextXML. Locator: Item 16.) — verified-quote
- CONSORT 2025 item 26 keeps this: "For each primary and secondary outcome, by group: the number of participants included in the analysis …" (Hopewell S et al. CONSORT 2025 statement. *PLoS Med* 2025, PMC11996237.) — verified-quote

**R3.2 Rate and proportion reliability: apply the NCHS thresholds for the estimator type, and footnote the outcome (Part A(a)).**
- Proportions: denominator ≥ 30; Clopper–Pearson 95 % CI; absolute width ≥ 0.30 → suppress; absolute width 0.05–0.30 with relative width > 130 % → suppress; 0 events or 100 % events → flag for review.
- Rates and counts (2023+): ≥ 10 events and relative CI width ≤ 160 %.
- Legacy vital rates: ≥ 20 events.
— verified-quote

**R3.3 A proportion of 0 or 1 has a degenerate SE, so its interval must not come from a Wald interval.** (NCHS 2(175), p. 3; Part A(a).) — verified-quote

**R3.4 A time-to-event mean computed only over runs that reached the event is a conditional summary.**
- State that it is conditional.
- State its denominator (the k runs with the event).
- Report it alongside the event proportion k/n, because the runs without the event are right-censored.

Sources:
- Arcuri A, Briand L. A Hitchhiker's guide to statistical tests for assessing randomized algorithms in software engineering. *Softw Test Verif Reliab* 2014;24(3):219–250. Author preprint: https://orbilu.uni.lu/bitstream/10993/1071/1/paper_stvr_icse_2012.pdf. Locator: §6 "Censored Data", preprint p. 15. — verified-quote
  > "if the goal is to cover a particular target … one can run a randomized algorithm with a time limit L … The above types of experiments are dealing with right-censored data, and their properties are equivalent to survival/failure time analysis … This is a case of right-censorship since, assuming a time limit L, one will not have observations Xi for the cases X > L."
  > "one can consider their success rate γ = k/n, i.e., the proportion of number of times k, out of the n runs, for which a valid solution is found."
  > "Another alternative to compare execution times is to apply a Mann-Whitney U-test … using only the times of successful runs, which have Xi and Yi values lower or equal to L."
  > §5.2 "Central Limit Theorem" (preprint p. 13): "a search algorithm can be prematurely stopped when reaching a time limit … in these cases, one is actually dealing with censored data (in particular, right-censorship) and this requires proper care in terms of statistical testing and the interpretation of results"
- Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. *Br J Cancer* 2003;89:232–238, PMC2394262 (read through Europe PMC). Locator: Introduction; section "Censoring". — verified-quote
  > "it is usual that at the end of follow-up some of the individuals have not had the event of interest, and thus their true time to event is unknown. Further, survival data are rarely Normally distributed, but are skewed … It is these features of the data that make the special methods called survival analysis necessary."
  > "Such censored survival times underestimate the true (but unknown) time to event."
  > The paper also gives the converse warning, for event proportions that ignore time: "these figures are potentially misleading as they ignore the duration spent in remission before these events occurred."
  > "The large skew encountered in the distribution of most survival data is the reason that the mean is not often used."
- Dudley WN, Wickham R, Coombs N. An introduction to survival statistics: Kaplan–Meier analysis. *J Adv Pract Oncol* 2016;7(1):91–100, PMC5045282. Locator: section on the K-M plot. — verified-quote
  > "Median survival is reported in most studies because survival times are usually skewed, and the median is a better measure of centrality than the mean. Furthermore, there is no way to know if or when patients who are alive and not censored at the end of a study will experience the event of interest, so a mean cannot be calculated."
  > "It has been recommended to halt estimations of survival curves when the proportion of patients who have not experienced the event becomes unduly small, perhaps when only 10% to 20% of an original large sample or fewer than 10 patients in a small study are still being followed."
- Not fetched (scanned or not open access): Altman & Bland, "Time to event (survival) data", *BMJ* 1998;317:468 (PMC1113717, scanned, no text layer); Pocock, Clayton & Altman 2002, *Lancet* (paywalled). — unverified

**R3.5 Show distributions, not only bars of means, whenever n per group is small. Say what n is.**
- Weissgerber TL, Milic NM, Winham SJ, Garovic VD. Beyond bar and line graphs: time for a new data presentation paradigm. *PLoS Biol* 2015;13(4):e1002128, PMC4406565. Locator: Abstract; "Recommendations for a New Data Presentation Paradigm". — verified-quote
  > "many different data distributions can lead to the same bar or line graph. The full data may suggest different conclusions from the summary statistics."
  > "The best option for small datasets is to show the full data, as summary statistics are only meaningful if there are enough data to summarize."
- Cumming G, Fidler F, Vaux DL. Error bars in experimental biology. *J Cell Biol* 2007;177(1):7–11, PMC2064100. Rule 2: "the value of n (i.e., the sample size, or the number of independently performed experiments) must be stated in the figure legend." — verified-quote

**R3.6 Number of runs for randomised algorithms: aim for n = 1 000 per artefact, or justify fewer. State the number of runs.**
Arcuri & Briand 2014, §11 "Practical Guidelines", preprint pp. 24–25. — verified-quote
> "When randomized algorithms are analyzed, clearly specify the number of runs and employed statistical tests."
> "On each artifact in the case study, run each randomized algorithm at least n = 1,000 times. If this is not possible, explain the reasons and report the total amount of time it took to run the entire case study."

### 4. Intervals and effect sizes

**R4.1 Give each estimate an interval (95 % by convention), and say which interval it is.**
- CONSORT 2010 item 17a: "For each primary and secondary outcome, results for each group, and the estimated effect size and its precision (such as 95% confidence interval)". The Explanation adds: "A 95% confidence interval is conventional, but occasionally other levels are used." — verified-quote
- SAMPL p. 3: "the estimate (or "effect size") associated with the P value, and a measure of precision for the estimate, usually a 95% confidence interval." — verified-quote
- Hoefler T, Belli R. Scientific benchmarking of parallel computing systems: twelve ways to tell the masses when reporting performance results. *SC '15*. doi:10.1145/2807591.2807644. URL: https://htor.inf.ethz.ch/publications/img/hoefler-scientific-benchmarking.pdf. Rule 5 (p. 4): "Report if the measurement values are deterministic. For nondeterministic data, report confidence intervals of the measurement." — verified-quote

**R4.2 For a comparison, interpret the CI *on the difference*, not the overlap of two separate CIs.**
- CONSORT 2010 E&E 17a: "Confidence intervals should be presented for the contrast between groups. A common error is the presentation of separate confidence intervals for the outcome in each group rather than for the treatment effect." — verified-quote
- Cumming G. The new statistics: why and how. *Psychol Sci* 2014;25(1):7–29, doi:10.1177/0956797613504966 (course-hosted copy: https://uopsych.github.io/psy611/readings/Cumming_2014.pdf). Table 1, p. 8, Guideline 15: "If your ES of interest is a difference, use the CI on that difference for interpretation. Only in the case of independence can the separate CIs inform interpretation." — verified-quote
- Wilke CO. *Fundamentals of Data Visualization*, ch. 16, https://clauswilke.com/dataviz/visualizing-uncertainty.html: "these rules of thumb are not reliable and should be avoided. The correct way to assess whether there are differences in mean rating is to calculate confidence intervals for the differences." — verified-quote

**R4.3 Report an effect size *with its CI*, and prefer estimation to dichotomous significance.**
- Cumming 2014, Table 1, Guideline 7: "Whenever possible, adopt estimation thinking and avoid dichotomous thinking." Guideline 14: "Prefer 95% CIs to SE bars. Routinely report 95% CIs, and use error bars to depict them in figures." Guideline 17: "When appropriate, use the CIs on correlations and proportions, and their differences, for interpretation." — verified-quote
- APA JARS-Quant, Table 1 (Appelbaum M et al. *Am Psychol* 2018;73(1):3–25. URL: https://www.apa.org/pubs/journals/releases/amp-amp0000191.pdf), p. 6: "Effect-size estimates and confidence intervals on those estimates that correspond to each inferential test conducted, when possible". — verified-quote
- Arcuri & Briand 2014, §11: "Always report standardized effect size measures. … It is also strongly advised to report effect size confidence intervals, e.g., by using a bootstrapping technique." — verified-quote

**R4.4 Name the effect-size variant and its standardiser. Treat Cohen's 0.2/0.5/0.8 as benchmarks of last resort.**
- Lakens D. Calculating and reporting effect sizes to facilitate cumulative science. *Front Psychol* 2013;4:863, PMC3840331. — verified-quote
  > "Reporting standardized effect sizes for mean differences requires that researchers make a choice about the standardizer of the mean difference …"
  > "A commonly used interpretation is to refer to effect sizes as small (d = 0.2), medium (d = 0.5), and large (d = 0.8) based on benchmarks suggested by Cohen (1988). However, these values are arbitrary and should not be interpreted rigidly … The only reason to use these benchmarks is because findings are extremely novel, and cannot be compared to related findings in the literature."
- Nature Portfolio Reporting Summary, Statistics item: "Estimates of effect sizes (e.g. Cohen's d, Pearson's r), indicating how they were calculated". URL: https://www.nature.com/documents/nr-reporting-summary-flat.pdf, p. 1. — verified-quote

**R4.5 Report the raw descriptives (means, SDs, counts) behind an effect size, not the effect size alone.**
- Arcuri & Briand 2014, §11: "report means and standard deviations (in case readers for some reasons want to calculate effect sizes in the d family). For dichotomous experiments, always report the values a and b". — verified-quote
- SAMPL p. 3: "reporting the descriptive statistics from which other statistics are derived, such as the numerators and denominators of percentages". — verified-quote

**R4.6 Do not use the SE to describe variability. Use the SD or percentiles for spread, and CIs for precision.**
SAMPL p. 4: "Do NOT use the standard error of the mean (SE) to indicate the variability of a data set. Use standard deviations, inter-percentile ranges, or ranges instead." — verified-quote

**R4.7 Exact p values if NHST is used. Report all of them, not only the significant ones.**
- Arcuri & Briand 2014, §11: "Report all the obtained p-values, whether they are smaller than α or not". — verified-quote
- JARS p. 6: "including exact p values if null hypothesis statistical testing (NHST) methods were employed". — verified-quote
- Nature Reporting Summary: "Give P values as exact values whenever suitable." — verified-quote

**R4.8 Use a CI method appropriate to the estimator. For proportions near 0 or 1, use exact (Clopper–Pearson) or similar, not Wald.** (NCHS 2(175); Part A(a).) — verified-quote

**R4.9 Check normality before using a normal-approximation interval around a mean.**
Hoefler & Belli Rule 6 (p. 5): "Do not assume normality of collected data (e.g., based on the number of samples) without diagnostic checking." — verified-quote

### 5. Relative measures (reductions, ratios, percent change)

**R5.1 Report absolute and relative effects together.**
- CONSORT 2010 item 17b (Schulz KF, Altman DG, Moher D. *BMJ* 2010;340:c332): "For binary outcomes, presentation of both absolute and relative effect sizes is recommended" — verified-quote (checklist read through the PMC2844940 summariser; the same item wording appears verbatim in the E&E full text, PMC2844943)
- CONSORT 2010 E&E, Item 17b explanation:
  > "both the relative effect (risk ratio (relative risk) or odds ratio) and the absolute effect (risk difference) should be reported (with confidence intervals), as neither the relative measure nor the absolute measure alone gives a complete picture of the effect and its implications. Different audiences may prefer either relative or absolute risk, but both doctors and lay people tend to overestimate the effect when it is presented in terms of relative risk."
  > "The size of the risk difference is less generalisable to other populations than the relative risk since it depends on the baseline risk in the unexposed group"
  — verified-quote
- CONSORT 2025 item 26 keeps this: "for binary outcomes, presentation of both absolute and relative effect size". — verified-quote

**R5.2 A ratio relative to a base must state the base and the base's absolute value.**
Hoefler & Belli Rule 1 (p. 3): "When publishing parallel speedup, report if the base case is a single parallel process or best serial execution, as well as the absolute execution performance of the base case. A simple generalization of this rule implies that one should never report ratios without absolute values." — verified-quote

**R5.3 The same benefit reads very differently as a relative and as an absolute change. Name the measure (percent vs percentage points).**
Schünemann HJ et al. Chapter 15: Interpreting results and drawing conclusions. *Cochrane Handbook for Systematic Reviews of Interventions* v6.5, 2024. URL: https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-15. §15.4.1. — verified-quote
> "Clinicians may be more inclined to prescribe an intervention that reduces the relative risk of death by 25% than one that reduces the risk of death by 1 percentage point, although both presentations of the evidence may relate to the same benefit (i.e. a reduction in risk from 4% to 3%)."
> §15.1: "even if relative effects are similar across subgroups, absolute effects will differ according to baseline risk."

**R5.4 Summarise the underlying quantities, then take the ratio. Do not average ratios.** (This also keeps a near-zero reference from blowing a reduction up.)
- Hoefler & Belli Rule 4 (p. 4): "Avoid summarizing ratios; summarize the costs or rates that the ratios base on instead. Only if these are not available use the geometric mean for summarizing ratios." — verified-quote
- Vickers AJ. The use of percentage change from baseline as an outcome in a controlled trial is statistically inefficient: a simulation study. *BMC Med Res Methodol* 2001;1:6, PMC34605. Conclusions: "Percentage change from baseline should not be used in statistical analysis. Trialists wishing to report this statistic should use another method, such as ANCOVA, and convert the results to a percentage change by using mean baseline scores." — verified-quote

**R5.5 A relative measure is unstable when its reference is small.** The NCHS gives this as its reason for not using RSE alone for small proportions. By analogy, the same applies to percentage reductions from a near-zero reference. (This is an inference, not a direct rule.)
NCHS 2(175), p. 3: "when dividing the SE by very small proportions, the RSE can be too conservative, and when dividing the SE by very large proportions, the RSE can be too liberal. … rely on both the relative and absolute CI widths to reduce the impact of this property." — verified-quote (the extension to percent reductions is paraphrase/derived)

**R5.6 Plain-language style: state the actual change, not only a percentage.**
Australian Government Style Manual, "Percentages" (updated 24 July 2024), https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/numbers-and-measurements/percentages: "Don't use percentages to describe change. Avoid using percentages to describe changes. Tell people what the actual increase or decrease is." — verified-quote

**R5.7 Report CIs on relative measures as well.**
SAMPL p. 4: "Consider reporting a measure of precision (a confidence interval) for estimated risks, rates, and ratios." Also CONSORT 17b (with confidence intervals). — verified-quote

### 6. Tables

**R6.1 A table must be intelligible without the text.**
- Australian Style Manual, "Tables": "Some people will look at tables before they read the text. For this reason, design tables so they are self-explanatory." — verified-quote
- APA (Purdue OWL rendering): "Each table and figure must be intelligible without reference to the text." — paraphrase-verified (summariser)

**R6.2 Three kinds of table note, in order: general, specific (superscript letters), probability.**
- APA 7 (TCS LibGuide reproduction): "Tables may have three kinds of notes, which are placed below the body of the table: general notes, specific notes, and probability notes." Specific: "Specific notes are indicated by superscript lowercase letters (e.g., a, b, c)." — verified-quote (general note), paraphrase-verified (the specific-note sentence came through the summariser)
- Probability note: "describes how asterisks and other symbols are used in a table to indicate p values". — paraphrase-verified

**R6.3 Align numbers on the decimal point. Keep decimals consistent within a column and across comparable values.**
- APA 7 (LibGuide): "Numerical values should be centered in the column and aligned on the decimal." — verified-quote
- Australian Style Manual: "Align numbers to the right. In addition, decimal points in the column should line up." — verified-quote
- Cole 2015 p. 608: "A useful trick when formatting table columns is to align the numbers by decimal point, which highlights differences in the number of decimal places." Cole adds that fixed-decimal columns are not mandatory: "tables ought not to be restricted to columns of numbers with fixed decimal places". — verified-quote
- Note the tension: APA wants "same number of decimal places … if possible", while Cole lets precision vary. SI wants one *format* per column.

**R6.4 Define every non-standard abbreviation. Standard statistical symbols (M, SD, n, p, df, OR) need no definition; CI, ANOVA and similar do.**
APA 7 guide p. 2: "Do not define symbols or abbreviations that represent statistics (e.g., M, SD, F, t, df, p, N, n, OR) … Define other abbreviations (e.g., AIC, ANOVA, BIC, CFA, CI, NFI, RMSEA, SEM)." — verified-quote

**R6.5 Do not repeat the same statistics in both text and table or figure.**
- APA 7 guide p. 2: "Do not repeat statistics in both the text and a table or figure." — verified-quote
- Australian Style Manual: "Your text comments on or interprets the table. Where possible, avoid repeating the text or data in the table word for word." — verified-quote

**R6.6 Tables give exact values; figures give the overall picture.**
SAMPL p. 4: "Display the data in tables or figures. Tables present exact values, and figures provide an overall assessment of the data." — verified-quote

**R6.7 Head a column with a quantity and its unit ("quantity/unit"), so the cells hold pure numbers. A unit symbol never carries information about the quantity.**
SI Brochure §5.4.1–5.4.2, pp. 143–144: "It is common practice to write the quotient of a quantity and a unit in this way for a column heading in a table, so that the entries in the table are simply numbers. … The axes of a graph may also be labelled in this way". And: "Unit symbols must not be used to provide specific information about the quantity and should never be the sole source of information on the quantity." — verified-quote

**R6.8 Percent sign spacing: SI puts a space before "%"; the Australian Style Manual uses none.** Pick one and declare it.
- SI §5.4.7, pp. 146–147: "The internationally recognized symbol % (per cent) may be used with the SI. When it is used, a space separates the number and the symbol %." — verified-quote
- Australian Style Manual, "Percentages": "Don't use a space between the number and the percentage sign." — verified-quote

**R6.9 Order table notes: abbreviations, then superscript-locator notes, then the general note, then the source.** (This is the Australian order and differs from APA's.)
Australian Style Manual, "Tables": "When writing table notes, list them in the following order: abbreviations; notes to superscript locators; general note to the table; source of data". — verified-quote

### 7. Figures

**R7.1 Bars on a linear scale start at 0. Bars on a log scale (ratios) start at 1. If 0 is impractical, use dots, not truncated bars.**
Wilke CO. *Fundamentals of Data Visualization*. O'Reilly, 2019; free online edition https://clauswilke.com/dataviz/. — verified-quote
- Ch. 17, https://clauswilke.com/dataviz/proportional-ink.html: "The principle of proportional ink: The sizes of shaded areas in a visualization need to be proportional to the data values they represent." "Bars on a linear scale should always start at 0." "Bars on a log scale represent ratios and must always start at 1, and bars on a linear scale represent amounts and must always start at 0."
- Ch. 6.3, https://clauswilke.com/dataviz/visualizing-amounts.html: "One important limitation of bars is that they need to start at zero, so that the bar length is proportional to the amount shown. For some datasets, this can be impractical or may obscure key features. In this case, we can indicate amounts by placing dots at the appropriate locations along the x or y axis."

**R7.2 Small multiples share the same axis ranges and scalings. If they cannot, the caption says so.**
Wilke ch. 21, https://clauswilke.com/dataviz/multi-panel-figures.html. — verified-quote
> "it is important that each panel uses the same axis ranges and scalings. The human mind expects this to be the case."
> "I generally recommend against using different axis scalings in separate panels of a small multiples plot. … at a minimum you need to draw the reader's attention to this issue in the figure caption."

**R7.3 Keep one visual language across figures: the same thing always looks the same.**
Wilke ch. 21: "we need to employ a consistent visual language. By "visual language," I mean the colors, symbols, fonts, and so on that we use to display the data. And keeping the language consistent means, in a nutshell, that the same things look the same or at least substantively similar across figures." — verified-quote

**R7.4 Every error bar or band says what it represents (SD, SE or CI, and the level).**
- Wilke ch. 16: "Whenever you visualize uncertainty with error bars, you must specify what quantity and/or confidence level the error bars represent." — verified-quote
- Cumming, Fidler & Vaux 2007, Rule 1: "when showing error bars, always describe in the figure legends what they are." — verified-quote

**R7.5 Connect points with lines only where interpolation is valid (a trend over an ordered factor). Plot as much as is needed to interpret the result.**
Hoefler & Belli Rule 12 (p. 10): "Plot as much information as needed to interpret the experimental results. Only connect measurements by lines if they indicate trends and the interpolation is valid. This rule does not require to always plot confidence intervals or other notions of spread/error. If these are always below a bound and would clutter the graph, they can simply be stated in the describing text or figure caption." — verified-quote

**R7.6 Do not mislead: watch for automatic rescaling, area encodings, 3-D and pie charts. Show the full range where relevant.**
Rougier NP, Droettboom M, Bourne PE. Ten simple rules for better figures. *PLoS Comput Biol* 2014;10(9):e1003833, PMC4161295. Rule 7, "Do Not Mislead the Reader": "make sure to always use the simplest type of plots that can convey your message and make sure to use labels, ticks, title, and the full range of values when relevant." — verified-quote

**R7.7 Settle a figure's message before designing it. Override software defaults. Avoid chartjunk. Use colour only with a reason.**
Rougier et al. 2014, Rule 2 ("Identify Your Message"), Rule 5 ("Do Not Trust the Defaults"), Rule 8 ("Avoid 'Chartjunk'"), Rule 6 ("Use Color Effectively"): "If you don't know the answer, just keep it black." — verified-quote

**R7.8 Label axes with the quantity and its unit.**
- SI §5.4.1 (R6.7).
- APA 7 (TCS LibGuide, Figures, "Adapted from APA publication manual (7th ed.)", https://tcsedsystem.libguides.com/APA7/Figures): "Use title case for axis labels. Abbreviate the words "number" to "no." and "percentage" to "%."" — verified-quote
- Note: APA uses title case for axis labels. The thesis's sentence-case house style is a declared departure.

**R7.9 A legend or key explains every symbol, line style and colour.**
APA 7 (TCS LibGuide, Figures): "A figure legend, or key, if present, should be positioned within the borders of the figure and explains any symbols used in the figure image." — verified-quote

**R7.10 Report the worst case or a percentile when the mean is not the decision-relevant summary. Show upper bounds where these exist.**
Hoefler & Belli Rule 8 (p. 6): "Carefully investigate if measures of central tendency such as mean or median are useful to report. Some problems, such as worst-case latency, may require other percentiles." Rule 11 (p. 9): "If possible, show upper performance bounds to facilitate interpretability of the measured results." — verified-quote

### 8. Captions and legends

**R8.1 Captions are not optional. A caption explains how to read the figure and supplies what the graphic cannot show. Where exact values matter, give them somewhere.**
Rougier et al. 2014, Rule 4 "Captions Are Not Optional": "The caption explains how to read the figure and provides additional precision for what cannot be graphically represented. … If the numeric values are important, they must be provided elsewhere in your article or be written very clearly on the figure." — verified-quote

**R8.2 The caption or legend states n, the centre statistic, what the uncertainty is (type and level), and the test or effect-size method.**
Nature Portfolio Reporting Summary, Statistics, p. 1: "For all statistical analyses, confirm that the following items are present in the figure legend, table legend, main text, or Methods section." Items include:
- "The exact sample size (n) for each experimental group/condition, given as a discrete number and unit of measurement"
- "A full description of the statistical parameters including central tendency (e.g. means) or other basic estimates (e.g. regression coefficient) AND variation (e.g. standard deviation) or associated estimates of uncertainty (e.g. confidence intervals)"
- "Estimates of effect sizes (e.g. Cohen's d, Pearson's r), indicating how they were calculated"

— verified-quote. Also Cumming, Fidler & Vaux Rules 1–2 (R3.5, R7.4).

**R8.3 Notes define every abbreviation and symbol not understood from the title, image and legend.**
APA 7 (TCS LibGuide, Figures): "Three types of notes (general, specific, and probability) can appear below the figure to describe contents of the figure that cannot be understood from the figure title, image, and/or legend alone (e.g., definitions of abbreviations, copyright attribution)." — verified-quote

**R8.4 If panels use different scales, the caption must say so.** (Wilke ch. 21; R7.2.) — verified-quote

**R8.5 Small spread may be stated in the caption instead of drawn, if it is bounded and would clutter.** (Hoefler & Belli Rule 12; R7.5.) — verified-quote

**R8.6 Where an estimate is flagged or suppressed, the footnote or caption gives the reason.** (NCHS 2(175), p. 2; R2.5.) — verified-quote

---

## Part C — Conflicts between sources (each must be resolved by a declared choice)

| Point | Position A | Position B |
|---|---|---|
| Leading zero on bounded statistics (p, proportions) | APA 7: omit ("p < .001", ".25") | SI §5.4.4 and Australian Style Manual: always "0." |
| Thousands separator | APA 7 and Australian Style Manual: comma (1,000) | SI §5.4.4: space (1 000), optional at four digits |
| Space before % | SI §5.4.7: "a space separates the number and the symbol %" | Australian Style Manual: no space |
| Decimals within a column | APA: same number of decimals where possible | Cole 2015: fixed decimals not required, align on the point; SI: one *format* per column |
| Empty cells | APA 7: blank = not applicable, dash = not obtained | Australian Style Manual: never leave empty; ABS: ". ." n/a, "n.a."/"na" not available, "np" not published |
| Rounds to zero | ABS: "—" for both nil and rounded to zero | UK Analysis Function: "0" only for a true zero, [low]/[high] otherwise |
| Asterisks | APA, NCHS, ABS: asterisks mark p values, unreliable estimates or RSE bands | UK Analysis Function: avoid "*" and "†" (accessibility); use bracketed letters |
| NVSS small-count rule | ≤ 2022 data: < 20 events → asterisk (RSE ≥ 23 %) | 2023+ data: < 10 events, or relative CI width > 160 % → asterisk |
| Axis-label case | APA 7: title case | the thesis house style (sentence case) is a declared departure |

## Part D — Derived implications for the audit (inferences, not sourced rules)

1. **The "20 events" rule is a Poisson-rate convention for vital statistics, and NCHS replaced it for 2023+ data with ≥ 10 events and a relative CI width ≤ 160 %.** For a *proportion* over 1 000 runs, the directly applicable NCHS standard is Vital Health Stat 2(175):
   - denominator ≥ 30;
   - Clopper–Pearson interval;
   - suppress if the absolute width is ≥ 0.30, or if it is 0.05–0.30 with relative width > 130 %;
   - flag (do not silently print) 0/n or n/n.

   For a conditional mean over k runs that reached the target, the closest NCHS analogue is the count/rate minimum (k ≥ 10 now, ≥ 20 historically). Citing the rule this way is an analogy and should be declared as one.
2. **A mean time to compromise over only the runs that reach a target is a right-censored time-to-event summary** (Arcuri & Briand §6; Clark et al. 2003). The defensible pairing is:
   - the event proportion k/n, with its interval;
   - the conditional mean (or median), labelled as conditional on the k runs, with k stated.

   An alternative is a Kaplan–Meier median, if the time cap is fixed.
3. **A reduction relative to the no-defence reference should be printed with the reference value and the absolute difference** (CONSORT 17b; Hoefler Rule 1; Cochrane §15.4.1). It should also be computed as a ratio of summaries, not a mean of per-run ratios (Hoefler Rule 4; Vickers 2001).
4. **A value that would print as 0.000, 0 % or 100 % but is not exactly that should be printed as "< 0.001", "< 0.1 %" or "> 99.9 %"** (APA; Cole; UK [low]/[high]), or with a defined marker.

## Part E — Not fetched, or gaps

- APA Publication Manual 7th ed. itself (apastyle.apa.org blocks automated fetches; the Internet Archive was offline). §§6.36 and 7.12 are cited through APA's own instructional aid and a LibGuide reproduction.
- Chicago Manual of Style; ISO 80000-1 (both paywalled).
- Kitchenham et al. reporting guidelines (not fetched).
- Scott-Knott ESD presentation conventions (Tantithamthavorn et al.) were outside this brief and not fetched.
- Altman & Bland 1998, "Time to event (survival) data", *BMJ* (scanned, no text layer); Pocock, Clayton & Altman 2002 (paywalled).
- Cohen 1988 (book; the benchmarks are cited through Lakens 2013).
