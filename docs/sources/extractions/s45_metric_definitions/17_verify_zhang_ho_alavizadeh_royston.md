# Verify C: Table 4.3 rows NCR, MTTC, ASP/NCR reduction, time lost

Checked 2026-09-30 against the source text itself, never against the extracts alone:
- Zhang: `docs/sources/lit_review/zhang2023.md` and the PDF `lit_review/original/GENG5512Report_Zhang_22792191.pdf`. Page numbers re-read with pypdf. "p." means the printed page; PDF page = printed + 1.
- Ho: `lit_review/ho2024.md` and `original/GENG5512Report_Ho_22701889.pdf`.
- Alavizadeh: `lit_review/alavizadeh2022.pdf`, cropped by column with pdfplumber.
- Sharma: `lit_review/sharma2025.md` and the PDF.
- Cho: `lit_review/1_1_cho2020toward.md`.
- McQueen 2006: `tactic_profiles/step_c/mcqueen2006_time_to_compromise.md`.
- McQueen 2006b: `tactic_profiles/step_c/mcqueen2006_scada_risk_reduction.md`.
- Royston & Parmar 2013: fetched from Europe PMC PMC3922847 full-text XML (saved beside this file as `royston2013.xml` and `royston2013.txt`).
- Dissertation text: `s45_current.tex`.
- Table: `docs/thesis/tables/tab_4-5a_metrics.tex`.
- Implementation: `data/results/ch5_defended/time_lost.py`.

---

## 1. Network compromise ratio (NCR): cited to zhang2023 and ho2024

**The source's name**
- Zhang: "Network Compromise Ratio (NCR)".
- Ho: "Host Compromised Ratio (HCR)" at Eq. 10, and "Host Compromise Ratio" in the Table 5 feature list (p. 22).
- Ho's full text never uses "NCR" or "network compromise".

**The source's definitions**

Zhang, §5 *Evaluation*, **p. 32** (PDF p. 33):
> "we use Network Compromise Ratio (NCR) as the simulation checkpoint to evaluate MTD techniques and their combinations. NCR is the ratio of compromised hosts to the total number of hosts in the network. It helps us measure the effectiveness of our MTD techniques by measuring the time it takes for the adversary to compromise a certain proportion of hosts in the network. In this perspective, we set the terminating condition for the simulation as the NCR reaching 0.8 and run the simulation 100 times for each variable set"

So Zhang uses NCR as a stopping checkpoint at 0.8, and the report never reports NCR as a result. Its only result metric is the time to reach that checkpoint. The Fig. 8 caption (p. 33) reads "Mean Time to Compromise on 0.8 NCR". Zhang gives no equation for NCR.

Ho, §3.3.2 *Features*, item 4, **Eq. (10), p. 19** (PDF p. 20):
> "4) Host Compromised Ratio (HCR): The ratio of hosts that are compromised in the system. The ratio is calculated by: HCR = C_t / T_host (10) where C_t is the number of compromised hosts at time t and T_host is the total number of hosts in the network."

HCR is one of the reinforcement-learning model's input features ("The following metrics that will be used for the reinforcement learning model", §3.3.2). It is not one of Ho's evaluation metrics. Ho §3.4.2 says: "The four evaluation metrics are Attack Success Rate (ASR), Return on Attack (ROA), Attack Path Exposure (APE), Risk (R)."

**The dissertation's text**
> "NCR is ``the ratio of compromised hosts to the total number of hosts in the network'' \citep[p.~32]{zhang2023}, read at the end of each run: [Eq. NCR = mean over runs of hosts compromised / 50]"

**Checks**
- **The quote is verbatim and the locator is correct:** printed p. 32.
- **"Read at the end of each run" is the dissertation's choice.** It is not Zhang's, and the text marks it as its own by its syntax. Ho's "at time t" permits any reading moment.
- **Zhang's use as a stop is disclosed, but in other paragraphs.** The §4.5 opener says "The simulator also keeps the general scenario's stop, at 80 % of the network's hosts". The MTTC paragraph says Zhang reads MTTC at 80 %. The NCR paragraph itself does not say that Zhang uses NCR only as a stopping rule.
- **Ho is cited in Table 4.3 but not in the text.** Ho's different name (HCR) is therefore unstated in §4.5. The earlier draft (`06_ncr.md`) had the clause "Ho calls it the host compromise ratio", and that clause has since been cut.

**Verdict**
- Zhang: faithful (the quantity and the name). The reading moment is adapted and stated.
- Ho: adapted but unstated (same quantity, different name, and a feature rather than an outcome).

**Is it the source an examiner expects?** Yes for Zhang: the name exists only in this lineage. Census F (`F_web_open_access.md` l.68, l.137) found no other source for the exact name "network compromise ratio". The canonical outside relatives are:
- Lippmann et al. 2006, *network compromise percentage* (NCP);
- Enoch et al. 2017, which uses NCP;
- Cheng 2014, *compromised host percentage* (CHP).

I have **not** verified these three: they are census-F leads only. A lineage citation is defensible for a lineage simulator.

**Confidence: high.** The quote, page and equation were read in both PDFs.

**Smallest fix:** either
- drop `ho2024` from the Table 4.3 NCR row (and from NCR reduction, if it is carried there), or
- restore six words in the text: "(Ho's host compromise ratio, \citep[Eq.~10]{ho2024})".

---

## 2. Mean time to compromise (MTTC): cited to zhang2023 only

**The source's name**
- Zhang: "Mean Time to Compromise (MTTC)".
- McQueen 2006: "time-to-compromise". McQueen never names the metric "mean time to compromise". The only "mean time-to-compromise" in McQueen is a sub-estimate for Process 1 (preprint PDF p. 6).
- Cho 2020: "Mean time to compromise a system (MTTC)".
- Leversage & Byres 2008 are the first to use "Mean Time-to-Compromise" (it is in their title). That paper is paywalled and not held, so this rests on the census-F record only.

**The source's definitions**

Zhang, §3.4 *MTD Evaluation Metrics*, **p. 16** (PDF p. 17):
> "Another static metric widely used is Mean Time to Compromise (MTTC), which measures the time it takes for an attacker to compromise a target host on the network [4]."

Zhang's [4] is Cho et al. 2020, not McQueen. Zhang's operational reading is at 80 %, §5.1, **p. 33**:
> "Figure 8 presents the average time for the adversary to compromise 80% nodes of the target network"

The p. 32 passage quoted under row 1 sets the terminating condition at NCR 0.8, over 100 runs. The Fig. 8 caption (p. 33) is "Mean Time to Compromise on 0.8 NCR".

Cho 2020, §VII-A (md l.584):
> "Mean time to compromise a system (MTTC) [4], [26], [27], [32], [186]: This indicates how long an attacker takes to compromise an entire system."

McQueen et al. 2006, §3 (preprint PDF p. 4):
> "The time-to-compromise (T_pi) is defined as the time needed for an attacker to gain some level of privilege p on some system component i."

This is an analytic expectation for each component, not a mean over simulated runs.

**The dissertation's text**
> "MTTC is the mean time from the start of a run to its first compromised host, over the runs that compromise one ... Zhang reads MTTC when 80\,\% of the hosts have fallen, the goal of the general scenario \citep{zhang2023}. Few targeted runs reach it, so MTTC is read at the first host and reported with the share of runs that compromise one."

**Checks**
- **"Zhang reads MTTC when 80 % of the hosts have fallen" is correct.** The locators are p. 32 and p. 33, but the sentence carries no page. Add "p.~33".
- **The first-host checkpoint is the dissertation's own, and it is stated.**
- **The text does not mention Zhang's own written definition,** "compromise a target host" (p. 16). In a *targeted* scenario, an examiner who opens Zhang will ask why MTTC is not the time to the target. That is the one unaddressed gap.
- **The first host is closest to McQueen's time to compromise one component.**
- **Table 4.3 is inconsistent with Table 3.1.** Table 3.1 (`dissertation.tex` l.2860) already cites MTTC as `\citep{mcqueen2006, zhang2023, ho2024, tay2024, sharma2025}`, so the dissertation itself names McQueen as the root.
- **The MTTC definition sentence has no citation at all.** The only citation is on the 80 % sentence.

**Verdict:** adapted and stated (the checkpoint), measured against Zhang's operational use. Measured against Zhang's written definition (a target host), the difference is unstated.

**Is it the source an examiner expects?** Only partly. The name in this lineage is Zhang's. For the concept, an examiner expects:
- McQueen et al. 2006, the origin of time-to-compromise, which the dissertation already holds and cites in Table 3.1;
- or Leversage & Byres 2008, the origin of the name "MTTC";
- plus Cho 2020 as the MTD survey that lists it.

A single citation to a master's thesis for a metric with a 2006 origin reads as loose.

**Confidence: high** on the quotes and locators. **Medium** on the Leversage origin claim, which rests on the census-F record (title and abstract only). That paper is on the download list.

**Smallest fix**
- Table 4.3: `\citep{mcqueen2006, zhang2023}`.
- Text: open with "MTTC, after McQueen et al.'s time to compromise \citep{mcqueen2006}, is ...".
- Add "p.~33" to the Zhang 80 % sentence.
- Optionally one clause on why the checkpoint is not the target: "the time to a target is ASP's event".

---

## 3. ASP reduction and NCR reduction: cited to alavizadeh2022, Eq. 13

**The source's name:** "mitigation factor", written MF^m.

**The source's definition:** Alavizadeh et al. 2022, *IEEE TETC* 10(4), §V-D *Benefits of Security*, **p. 1782** (PDF p. 11 of 17, left column):
> "Another evaluation measurement that uses the ALE values of the cloud before and after deploying the MTD techniques is the mitigation factor. The mitigation factor, denoted by MF^m, shows the ability of the defensive MTD techniques to impair the attack. MF^m takes values within the range [0,1] as in Equation 13. Note that, a larger value of MF^m is more desirable.
> MF^m = { 1 − ALE_c^m / ALE_c, if ALE_c^m < ALE_c ; 0, otherwise }   (13)"

The variables, §V-C and §V-D (p. 1781–1782):
- **ALE_c is the cloud's annual loss expectancy:** "Annual loss expectancy (ALE) can be defined as the expected financial loss due to an attack event, and can be computed by the product of SLE and the annualized rate of occurrence (ARO)" (Eq. 11).
- **ALE_c^m is the same after MTD:** "ALE_c^m denotes the ALE value of the cloud after deploying MTD techniques. m ⊆ {S, D, R} denotes a set of MTD used as defensive techniques."

The paper is an MTD paper. Its title is "Evaluating the Security and Economic Effects of Moving Target Defense Techniques on the Cloud", and MF measures a monetary expected loss before and after MTD.

**The dissertation's text**
> "ASP reduction is the share of an attacker's ASP that MTD removes. It takes the form of the mitigation factor of Alavizadeh et al.\ \citep[Eq.~13]{alavizadeh2022}, with ASP in place of their annual loss expectancy: [1 − ASP under MTD / ASP with no MTD] ... The mitigation factor is floored at 0; ASP reduction is not, so it is negative when MTD helps the attacker."

and
> "NCR reduction is the same comparison on NCR"

**Checks**
- The form, the variable name (annual loss expectancy), the floor at 0 and the [0,1] range all match Eq. 13 exactly.
- Both departures are stated: ASP or NCR in place of ALE, and no floor.
- "The form of the mitigation factor with ASP in place of ALE" is a fair adaptation. The arithmetic is identical; only the quantity changes (a probability instead of a monetary loss), and the text names the substitution.

**Verdict:** adapted and stated, for both rows.

**Is it the source an examiner expects?** Acceptable, but not the tightest fit. A relative reduction is generic arithmetic, and any MTD precedent will do. Two held sources fit more closely, and I verified both:
- **Sharma 2025, Eq. (17), p. 9** (*Electronics* 14:2205, §4.2). It is an MTD paper, named as a *reduction* with no floor: "Security Risk Reduction Percentage (SRRP): The SRRP can is expressed as a percentage, and can be obtained as follows: SRRP(h_i) = SRRM(h_i)/SR_no−mtd(h_i) × 100% = (1 − TTC_no−mtd(h_i)/TTC_mtd(h_i)) × 100%. (17)". Since SRRM = SR_no−mtd − SR_mtd (Eq. 16), this is 1 − SR_mtd/SR_no−mtd: the same form, with MTD and no MTD as the two arms. Sharma is already in the bib.
- **McQueen et al. 2006b (HICSS-39), §3.10, preprint p. 8.** The same form applied to the *same quantity* as ASP: "Risk reduction can be defined as ΔR = 1 – (Pnew/Pold) = 1 – (Oldtime/Newtime)", where "Pnew is the probability of a successful attack in the enhanced system, Pold is the probability of a successful attack in the baseline system". This is not an MTD paper, and it is **not in references.bib** (only `mcqueen2006`, the TTC paper, is).

**Confidence: high.** The equation was read from the PDF column-cropped, and the page was computed from the journal range 1772–1788.

**Smallest fix:** none is required. An optional improvement is to cite `\citep[Eq.~13]{alavizadeh2022}` together with `\citep[Eq.~17]{sharma2025}`: Sharma's is named a "reduction", is unfloored, and sets MTD against no MTD. One point in favour of keeping Alavizadeh alone: the text's "floored at 0" sentence is written against it.

---

## 4. Time lost per MTD deployment: "this dissertation, after royston2013"

**The source's name:** "restricted mean survival time (RMST)". The contrast is "the difference in RMST between arms, Δ".

**The source's definition:** Royston & Parmar 2013, *BMC Med Res Methodol* 13:152, **Methods → "Restricted mean survival time (RMST)" → "Definition of RMST", Eq. (1)**:
> "The restricted mean survival time, μ say, of a random variable T is the mean of the survival time X = min(T, t*) limited to some horizon t* > 0. It equals the area under the survival curve S(t) from t = 0 to t = t* [5, 7]: μ = E(X) = E[min(T, t*)] = ∫_0^{t*} S(t) dt   (1)"

The next sentence, in the same subsection (unnumbered):
> "In a two-arm clinical trial with survival functions S_0(t) and S_1(t) in the control and research arms, respectively, the difference in RMST between arms, Δ, is given by Δ = ∫_0^{t*} S_1(t)dt − ∫_0^{t*} S_0(t)dt = ∫_0^{t*} [S_1(t) − S_0(t)] dt i.e. Δ is the area between the survival curves."

Royston & Parmar's own sources for Eq. (1) are [5] Andersen & Perme 2010 and [7] Irwin 1949, the historical origin of the restricted mean.

**The dissertation's text**
> "Each time is counted up to the next deployment, so a deployment is charged only its own cost; a mean of such times is a restricted mean \citep[Methods, Eq.~1]{royston2013}."

**Checks**
- **"A mean of such times is a restricted mean" is correct.** Min(wait, cap) is exactly Royston's X = min(T, t*), with the event being the next compromise and the origin being the deployment's completion. The locator "Methods, Eq. 1" is correct.
- **The metric itself is a difference of two restricted means,** that is, Royston's Δ, "the area between the survival curves". The handoff states that Figure 5.3(a,b) draws that area. The citation therefore supports the paragraph more strongly if it also points at Δ. The current sentence claims only the restricted mean.
- **Faithfulness, point 1: the horizon is common only approximately.** Royston's t* is one common horizon. `time_lost.py:101` uses cap = min(gap to the next deployment, interval). The corpus gaps are 1 997–2 004 s at the 2 000 s interval (`10_time_lost.md` l.86), so the horizon is common to within ±4 s. The run's last deployment uses the interval. This is a faithful application in substance; "counted up to the next deployment (at most one interval)" would make it exact.
- **Faithfulness, point 2: the pairing.** Royston's arms are independent randomised groups, while here each deployment is paired with the same seed's no-MTD run from the same moment. A mean of paired differences equals the difference of the two means, so Δ is unchanged. The pairing is a design choice the text states, not a misuse of RMST.
- **Faithfulness, point 3: an unstated exclusion.** This is not an RMST issue, but it matters to an examiner. A deployment whose no-MTD twin has already ended is **dropped** (`time_lost.py:98–99`). That is up to 22 % of deployments (baseline, service diversity; handoff dry run). §4.5 does not say so. A second, minor gap: an MTD run that ends at the time limit charges its last deployment the full cap.
- **The credit phrasing.** "This dissertation, after [royston2013]" follows the table's own stated grammar: introduced here, with the source of its form. It is the right shape, because the metric (a per-deployment paired delay) is new and only its statistical form is borrowed. One risk: "after" can be read as "modelled on Royston's metric". "This dissertation; restricted mean from [royston2013]" is more literal, but the current wording is conventional and acceptable.
- **Novelty.** Among held MTD sources, the nearest relatives compare time to compromise with and without MTD over a whole run. None is per deployment. Examples are Sharma's TTC_mtd against TTC_no−mtd (Eq. 17) and McQueen's percentage increase in time to compromise. "This dissertation" is defensible.

**Is it the source an examiner expects?** Yes. Royston & Parmar (2011 and 2013) are standard modern references for the restricted mean survival time. Irwin 1949 is the historical origin, and Royston cites it, so no second citation is needed.

**Verdict:** faithful. The restricted-mean claim is exact up to the ±4 s cap variation. The metric as a whole is adapted and stated, apart from the dropped deployments.

**Confidence: high** on the source quote and locator (full text read). **High** on the implementation, read from `time_lost.py`.

**Smallest fix:** extend the cited sentence to "...a mean of such times is a restricted mean, and the difference between two is the area between their survival curves \citep[Methods, Eq.~1]{royston2013}." Then add one clause for the exclusion: "deployments after the no-MTD run has ended are left out".

---

## To download (paywalled, Marc's list)
- Leversage & Byres 2008, "Estimating a System's Mean Time-to-Compromise", *IEEE S&P* 6(1):52–60, DOI 10.1109/MSP.2008.9. Needed only if MTTC is credited with the name's origin.
- Optional: Lippmann et al. 2006, MILCOM, DOI 10.1109/MILCOM.2006.302434. Needed only to confirm "NCP" as an outside precedent for NCR.
