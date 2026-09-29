# What each source actually writes: equations, symbols, constants (2026-09-29)

Scope: the source behind each adapted or borrowed metric in `docs/thesis/dissertation.tex` §4.5 "Evaluation metrics" (l.5588ff.). Each paper is read on its own, with no attribution carried across papers. I read the prior records in `docs/sources/extractions/s45_metric_definitions/01..10` first, then re-checked every quote below against the source text.

**Sources not in `docs/sources/`:** zhan2013, cisar2010ewma and bruneau2003 are absent. All three are open access. I fetched them to `docs/sources/s45_fetched/` (gitignored) to verify them:
- zhan2013: https://arxiv.org/pdf/1603.07433v1, the authors' copy of IEEE TIFS 8(11). Saved as `zhan2013.pdf` / `.txt`.
- cisar2010ewma: https://univagora.ro/jour/index.php/ijccc/article/download/2471/938. Saved as `cisar2010.pdf` / `.txt`.
- bruneau2003: https://www.eng.buffalo.edu/~bruneau/EERI%202003%20Bruneau%20et%20al.pdf, the published article as posted on the first author's page. Saved as `bruneau2003.pdf` / `.txt`.

Recommendation: add the three to `docs/sources/` (the placement is Marc's call).

Note on locators: "md l.N" means a line in the source markdown. "PDF p." is the page of the PDF file. "p." alone is the printed page.

---

## 1. rodriguez2024: "Occur. (rel.)"

**Is there an equation? No.** The quantity appears only as a column of two ProM-generated tables. It has no symbol, no formula and no prose definition.

- **Locator:** `docs/sources/lit_review/2_4_rodriguez2024process.md` l.358–384 (Table 3, "Log Summary (ProM)"; PDF p. 8) and l.428–445 (Table 5, "Log Summary (Team 12)").
- **Verbatim (Table 3):** "Total number of process | instances: 21" / "Total number of events: | 7265" / "Event classes defined by Activity" / "|**class**|**Occur. (abs.)**|**Occur. (rel.)**|" / "|execution|3270|45.01%|" … "|Start|21|0.29%|" "|End|21|0.29%|".
- **What the column means.** It is implicit in the table: Occur. (rel.) = Occur. (abs.) / "Total number of events", pooled over the 21 process instances. 3270/7265 = 45.01 % (checked).
- **What an event is.** md l.169: "The log is exported as a CSV file, each row representing an event with columns containing event attributes, including the case ID, activity name, and timestamp."
- **The authors' only prose about the column.** md l.321 + l.298 (PDF p. 7): "The set of activities (class) shown in Table 3 refers to all actions performed by 21 participants in the experiment (not including team 12) and mapped to MITRE ATT&CK. In other words, during the attack, it is determined that the behavior of these 21 attackers is represented by the tactics expressed in the Class column of the log summary. Additionally, the frequency with which these tactics occur is provided in the information contained in the analyzed log."
- **How they use it.** md l.348: "Almost 79.88% of the activity is concentrated in 3 types of events: **execution** , **defense_evasion** , **persistence** ."
- **Repeats count.** md l.181 (§3.2): "cases may include repeated activities in sequence or duplicate tasks with the same taxonomy signature."
- **Constants: none.** There is no window and no bin. The whole log is pooled.
- **Point for the thesis.** "Occur. (rel.)" is a column label from the ProM tool's Log Summary. The authors did not define a metric. The thesis's Eq. `eq:rto` is therefore its own notation, and nothing in the source has to be quoted. The faithful statement is "the relative occurrence Rodríguez et al. tabulate (Table 3): a class's events over all events, pooled over process instances".

## 2. hong2018: APV, Eqs. 1–2

- **Locator:** `docs/sources/lit_review/1_2_hong2018dynamic.md` l.229–243, §5.1.1 "Scanning: path variation", p. 39 (PDF p. 7). The equations are pictures in the PDF. The md holds a hand transcription from the published PDF (header comment, l.1). The PDF text layer confirms Eq. 1's glyphs but not Eq. 2's.
- **Eq. (1), verbatim transcription:**
  $$\Delta AP_{i,i-1} = \frac{|AP_i - AP_{i-1}|}{|AP_i|} \quad (1)$$
- **Eq. (2), verbatim transcription:**
  $$APV = \frac{\sum_{i=1}^{|S|} \Delta AP_{i,i-1}}{|S| - 1} \quad (2)$$
- **Symbols, verbatim:**
  - "_APi_ represents the set of attack paths found in the _i[th]_ network state" (l.235).
  - Table 1 (l.198): "_S_ | A set of network states"; "_AP_ | A set of attack paths".
  - l.221: "| _S_ | represents the cardinality of the set of network states".
  - Paths are host sequences (l.406): "_AP_ 0 = {( _A, h_ 1 _, h_ 4 _, h_ 7 ) …} is the set of attack paths in _s_ 0".
- **Definition and reading, verbatim:**
  - "the attack path variation (APV) measures the shift in attack paths as the network changes when MTD techniques are deployed" (l.231).
  - "APV captures the change in the set of attack paths between the network states" (l.231).
  - "The metric has been normalized by the number of consecutive network state pairs" (l.240).
  - "Lower APV value means the set of attack paths tends to be more static" (l.408, §5.3.1, **p. 42**, not p. 39).
- **Constants, verbatim (l.240): "Hence, there are no arbitrary values that need to be assigned to compute APV."**
- **Glyph caution.** The printed index runs $i=1..|S|$ over $|S|-1$ pairs. The worked Eq. (18) (garbled table dump, l.402) gives "2/5 + 4/5 + 4/5 over 3 = 0.6667". The numerator therefore has $|S|-1$ terms. If Eq. 2 is quoted, quote it as printed, with "[sic]" or no comment. Do not silently correct it.

## 3. zhan2013: attack rate

**Is there an equation? No.** Attack rate is defined in words. The only notation is the process $\{X_t\}$.

- **Locator:** arXiv 1603.07433v1, p. 3, §III-B "Step 2: Basic statistical analysis" (`docs/sources/s45_fetched/zhan2013.txt` l.312–320).
- **Definition, verbatim:** "For stochastic cyber attack processes, the primary statistic is the attack rate, which describes the number of attacks that arrive at unit time (e.g., minute or hour or day). Note that attack rate can be instantiated at various resolutions of attack processes, such as: network-level attack rate, victim-level attack rate and port-level attack rate." The same paragraph continues: "The secondary statistic is the attack inter-arrival time, which describes the time intervals between two consecutive attack events."
- **Notation, verbatim** (p. 2, §III-A, l.217–221): "Formally, a stochastic cyber attack process is described as {Xt : t≥ 0}, where Xt is the random variable (e.g., attack rate) at time t." The same $X_t$ appears in Algorithm 1: "observed attack rates {X1,...,X t}".
- **Paraphrase in the introduction** (p. 1, l.80–81): "attack rate (i.e., number of attacks per time unit)".
- **What an attack is** (p. 3, l.237–240): "A TCP flow is uniquely identified from honeypot-collected raw pcap data via the attacker's IP address, the port used by the attacker, the victim IP address in the honeypot, and the port that is under attack."
- **Time unit and its justification, verbatim** (p. 5, §IV-B, l.493–497): "We consider the per-hour attack rate at three resolutions … The choice of per-hour is natural, while noting that per-day attack rate is not appropriate because each period is no more than 80 days."
- **Other constants** (pre-processing only, not part of the attack rate). p. 3 (l.254–260): "60 seconds would be reasonable for low-interaction honeypots that provide limited interactions [13]" for the *flow timeout*, and "300 seconds for low-interaction honeypots [13]" for the *flow lifetime*. p. 5 applies both. **Do not cite this 60 s for κ.** It is a flow-expiry parameter, a different quantity.

## 4. zaffarano2015: attack confidentiality and its siblings

**Is there an equation? Yes, one generic form, the same for all four metrics.** There is **no detection model, no time window and no threshold**. Exposure is a Boolean task attribute. In the initial experiments it is "visible in plaintext".

- **Locator:** `docs/sources/lit_review/zaffarano2015.md` (Ghostscript text, two-column interleave; the md header says the PDF is authoritative). PDF text layer read with pypdf.
- **Activity model and valuation (§3.2, printed p. 6, PDF p. 4; md l.149–160), verbatim:** "Symbolically, we represent an activity model as a tuple ⟨T,A⟩ where T = {τ1,... ,τn} is a set of n tasks, and A ={α1,... ,αm} is a set of m attributes. A run of a model is a process that produces a dataset, which is simply a mapping function ν : T×A→V which takes a task τ and an attribute α to a value from the permissible values for the attribute α."
- **The four attributes (§3.2, printed p. 7, PDF p. 5; md l.212–223), verbatim:**
  - "• duration: length of time to complete the task execution, values are non-negative real numbers;
  - • success: whether the task was successfully completed, values are 0 (task did not complete successfully) and 1 (task completed successfully);
  - • unexposed: whether task information was exposed, values are 0 (information was exposed) and 1 (information was not exposed);
  - • intact: whether task information was corrupted, values are 0 (information was corrupted) and 1 (information was not corrupted)."
- **Attacker tasks** (md l.203–205): "an attacker activity model, whose activities correspond to the types of actions an attacker would perform".
- **Table 4 (printed p. 9; md l.335–348), verbatim:** "Attack Confidentiality is a measure of how much attacker activity may be visible by detection mechanisms". The siblings:
  - "Attack Productivity is a measure of how quickly an attacker can perform and complete adversarial tasks";
  - "Attack Success is a measurement of how successful an attacker may be while attempting to attack a network";
  - "Attack Integrity is a measurement of the accuracy of the information viewed by an attacker".
- **§4.3 Confidentiality (printed pp. 9–10, PDF pp. 7–8; md l.380–398), verbatim:** "Conﬁdentiality is a measure of how much information is exposed by activity model tasks. For the mission model, exposing information is typically undesirable, whereas an attacker being exposed is desirable. Conﬁdentiality is computed similarly to the metrics above, with the same type of costs and beneﬁts derived from them. For a mission model M, we have:"
  $$\mathrm{Confidentiality}(M,\nu) = \frac{1}{|T|}\sum_{\tau\in T} \nu(\tau, \mathit{unexposed})$$
  (unnumbered). It continues: "In principle, there are many ways in which information could be exposed (e.g., being stored in a database in such a way that a web application presents it to users), but in these initial experiments, we simply refer to whether information is visible in plaintext in network traffic."
- **The sibling equations, same form (unnumbered):**
  - Productivity (§4.1, md l.312–318): $\frac{1}{|T|}\sum_{\tau\in T}\nu(\tau,\mathit{duration})$;
  - Success (§4.2, md l.379–386): "Success(M,ν) = 1/|T| Σ_{τ∈T} ν(τ,success)", with "the average over a number of tasks makes mission success and attacker success real-valued numbers in the range [0,1]";
  - Integrity (§4.4): $\frac{1}{|T|}\sum_{\tau\in T}\nu(\tau,\mathit{intact})$.
- **The attacker instance is named in §4.1** (md l.349–351): "when M is an instance of the attacker model, we call its productivity attacker productivity". The same naming applies by "computed similarly".
- **How the metric is read (with minus without MTD)** (§4.1, md l.351–354): "The diﬀerence between attacker productivity for a run with the MTD and a run without the MTD is the eﬀectiveness of the MTD with regard to attacker productivity". Also §4 (md l.290–299): "Runs with no MTD deployed represent a baseline run".
- **Time.** No time window, bin or decay appears anywhere in the metrics. The one timed quantity is a mission *workload* (md l.251–253): "Each task will be repeated at timed intervals. For instance, the client will send 60 emails, one every second." "Task begin time" appears only as an example attribute (l.157–159) and is not among the four attributes chosen.
- **Detection mechanism.** The "Potential Sensor" column of Table 2 lists the *attacker's tools* (nmap, ncrack, ncat), not detectors. Zaffarano specify no IDS and no alarm.
- **Adaptation, stated in Zaffarano's own notation.** Keep $\frac{1}{|T|}\sum_{\tau\in T}\nu(\tau,\mathit{unexposed})$ and state three substitutions:
  1. $T$ becomes the attacker's actions (starting in bin $b$, pooled over $\mathcal{R}$);
  2. $\nu(\tau,\mathit{unexposed})$ becomes $\mathbf{1}[D_r(j)<\theta]$, the declared detector in place of "visible in plaintext";
  3. the reading is taken per time bin and against the baseline attacker, where Zaffarano read it with minus without MTD.

  Zaffarano leave the exposure valuation open ("many ways in which information could be exposed"). Only $\nu$ changes, so this is the smallest adaptation in §4.5. Eq. `eq:confidentiality` is already exactly this form written as a ratio of counts. Writing it as $\frac{1}{|T_b|}\sum_{\tau\in T_b}\nu(\tau,\mathit{unexposed})$ with $\nu(\tau,\mathit{unexposed}) = \mathbf{1}[D_r(j)<\theta]$ would show the adaptation line for line.
- **Wording flag for the current tex.** l.~5680 says "Zaffarano et al. judge exposure by what is visible in network traffic". The source says "visible in *plaintext* in network traffic", scoped to "these initial experiments".

## 5. cisar2010ewma: EWMA in intrusion detection

- **Locator:** IJCCC 5(2):160–170, pp. 160–161 (`docs/sources/s45_fetched/cisar2010.txt` l.28–64).
- **Eq. (1), verbatim:** "EWMAt = λYt + (1 − λ)EWMAt−1  t = 1, 2, . . . , n (1)". Symbols, verbatim:
  - "EWMA0 is the mean of historical data (target)";
  - "Yt is the observation at time t";
  - "n is the number of observations to be monitored including EWMA0";
  - "0 < λ ≤ 1 is a constant that determines the depth of memory of the EWMA."

  Attribution (p. 161): "This equation has been established by Roberts as described in [4]."
- **Eq. (2):** "σ²_EWMA = λ/(2 − λ) · σ²", "where σ is the standard deviation calculated from the historical data".
- **Eq. (3), the alarm:** "UCL = EWMA0 + kσEWMA; LCL = EWMA0 − kσEWMA where the factor k is either set equal 3 (the 3-sigma control limits) or chosen using the Lucas and Saccucci tables (ARL = 370)."
- **What EWMA is for** (abstract, p. 160): "Many intrusions manifest in changes in the intensity of events occuring in computer networks. Because of the ability of exponentially weighted moving average (EWMA) control charts to monitor the rate of occurrences of events based on their intensity, this technique is appropriate for implementation in control limits based algorithms."
- **The smoothing constant and its justification, verbatim** (p. 161): "The parameter λ determines the rate at which "older" data enter into the calculation of the EWMA statistic. A value of λ = 1 implies that only the most recent measurement influences the EWMA. … The value of λ is usually set between 0.2 and 0.3 [2] although this choice is somewhat arbitrary. Lucas and Saccucci [3] have shown that although the smoothing factor λ used in an EWMA chart is usually recommended to be in the interval between 0.05 to 0.25, in practice the optimally designed smoothing factor depends not only on the given size of the mean shift δ, but also on a given in-control Average Run Length (ARL)."
- **Their own choice** (§2, p. 163): "The optimal value for λ is the value which results in the smallest mean of the squared errors (MSE)". p. 163–164: "the authors suggest for the overall optimal parameter λopt to accept the average of all the partial results (in this particular case it is 0.75)." Their Table 1 range is 0.72–0.82 over the initial value S2.
- **Their conclusion** (p. 168): "often proposed values for exponential smoothing factor in case of network application of the algorithm, may in some circumstances lead to the creation of false alarms". So they tune λ on data.
- **Time base.** λ is **dimensionless, a weight per observation**. Memory in seconds depends on the sampling interval. Their samples are MRTG averages (p. 165): "Daily - with calculation of 5-minute average; Weekly - with calculation of 30-minute average; Monthly - with calculation of 2-hour average". Also p. 164: "the smoothing constant should not be too small, so that a short-term trend in the intensity of events in the recent past can be detected."
- **Other constant.** A drift tolerance p = 0.25, measured from month-to-month variation ("the maximum change of mean value p is not greater than 25%", p. 167).
- **Link to κ (my derivation; Čisar do not state it).** For observations every Δ seconds, $\lambda = 1-e^{-\Delta/\kappa}$, so $\kappa = -\Delta/\ln(1-\lambda)$. The conventional λ = 0.2–0.3 gives κ ≈ 2.8Δ–4.5Δ. Čisar's λ = 0.75 gives κ ≈ 0.72Δ. **Čisar state no memory in seconds, so they cannot license κ = 60 s. They license only the family and the practice of tuning λ on data.**
- **Symbol collision (finding).** The thesis uses λ for attack rate (Eq. `eq:attack-rate`). Quoting Čisar's Eq. 1 with λ in the next paragraph collides with it. Either rename attack rate's symbol or quote Čisar's weight under another letter, with "[their λ]" noted.
- **Threshold contrast.** Čisar set the alarm as the reference mean plus kσ (k = 3), with the reference taken from historical data. The thesis sets θ at the *median* of the baseline attacker's $D$. The shared idea is "calibrated on a reference process". The rule differs, and that difference is an adaptation to state.

## 6. alavizadeh2022: mitigation factor

- **Locator:** `docs/sources/lit_review/alavizadeh2022.md` l.596–605; §V-D "Benefits of security", p. 1782 (PDF p. 11). Glyphs checked in the PDF text layer ("¼" is "=", "/C0" is "−").
- **Eq. (13), verbatim:**
  $$MF^m = \begin{cases} 1 - \dfrac{ALE^m_c}{ALE_c}, & \text{if } ALE^m_c < ALE_c \\ 0, & \text{otherwise} \end{cases} \quad (13)$$
- **Definition, verbatim:** "Another evaluation measurement that uses the ALE values of the cloud before and after deploying the MTD techniques is the mitigation factor. The mitigation factor, denoted by MFm, shows the ability of the defensive MTD techniques to impair the attack. MFm takes values within the range [0,1] as in Equation 13. Note that, a larger value of MFm is more desirable."
- **Symbols, verbatim:** "ALEm c denotes the ALE value of the cloud after deploying MTD techniques. m ⊆ {S, D, R} denotes a set of MTD used as defensive techniques." (with Eq. 12, $BS^m_c = ALE_c - ALE^m_c$).
- **ALE (§V-C, Eq. 11):** "Annual loss expectancy (ALE) can be defined as the expected financial loss due to an attack event, and can be computed by the product of SLE and the annualized rate of occurrence (ARO), which represents the estimated number of occurrences of a threat event per year [29]." The equation is $ALE_c = \sum_{ap\in AP}\sum_{vm_i\in ap} SLE_{vm_i}\times ARO_{vm_i}$.
- **Constants: none in MF.** The ALE inputs (asset values, the $20 per shuffle) are case-study costs, outside MF.
- **Adaptation:** $ALE \to \mathrm{NCR}$, $m \to$ one defence, and **the floor at 0 dropped**. The tex already says this.

## 7. bruneau2003: loss of resilience

- **Locator:** Earthquake Spectra 19(4). Q(t) is defined on p. 736 and the equation is on p. 737 (PDF pp. 4–5; `docs/sources/s45_fetched/bruneau2003.txt` l.171–197). Figure 1 (p. 737) is captioned "Measure of seismic resilience — conceptual definition."
- **Q(t), verbatim:** "This approach is based on the notion that a measure, Q(t), which varies with time, has been defined for the quality of the infrastructure of a community. Specifically, performance can range from 0% to 100%, where 100% means no degradation in service and 0% means no service is available."
- **t0 and t1, verbatim:** "If an earthquake occurs at time t0, it could cause sufficient damage to the infrastructure such that the quality is immediately reduced (from 100% to 50%, as an example, in Figure 1). Restoration of the infrastructure is expected to occur over time, as indicated in that figure, until time t1 when it is completely repaired (indicated by a quality of 100%)."
- **The equation (unnumbered), verbatim:** "Hence, community earthquake loss of resilience, R, with respect to that specific earthquake, can be measured by the size of the expected degradation in quality (probability of failure), over time (that is, time to recovery). Mathematically, it is defined by"
  $$R = \int_{t_0}^{t_1} [100 - Q(t)]\,dt$$
- **Window.** $t_0$ is the event and $t_1$ is complete repair. **Both come from the data. There is no fixed window, no bin width and no pre-event averaging window.** 100 % is the pre-event level.
- **Above 100 %, verbatim, straight after the equation:** "Furthermore, return to 100% pre-event levels may not be sufficient in many instances … and post-event recovery to more than 100% pre-earthquake levels are often desirable." Bruneau therefore anticipates quality above the pre-event level. This corrects record 10's "Bruneau caps quality at 100 %": the stated *range* is 0–100 %, but above-100 % recovery is named.
- **"Resilience triangle" does not occur in the paper** (0 hits). Do not attribute the name to bruneau2003.
- **Adaptation, stated in Bruneau's notation:**
  - $Q(t)/100 \to \tilde g(t)$, with the "100 % = pre-event level" normalisation made explicit through $\bar g_-$;
  - $t_0 \to t_d$ (0 in shifted time);
  - $t_1$ (full repair) $\to$ a fixed 1 250 s cut, so the value is a lower bound, as the tex says;
  - the placebo subtraction $L_{\text{none}}$, which has no counterpart in Bruneau.

## 8a. cho2020: ASP

**Is there an equation? No.** Cho's is a survey definition.

- **Locator:** `docs/sources/lit_review/1_1_cho2020toward.md` l.578, §VII-A, **p. 727** (PDF p. 19, running head "…SURVEY ON MTD 727", checked). Record 04's "p. 728" is the attack-confidentiality relay on the next page, not ASP.
- **Verbatim:** "**Attack success probability (ASP)** [3], [11], … : This metric refers to the probability that attacks are successfully performed. For example, it refers to the probability that a system component (or defender) is compromised or a target is successfully discovered or accessed by an attacker."
- Cho's MTTC (l.584): "Mean time to compromise a system (MTTC) [4], [26], [27], [32], [186]: This indicates how long an attacker takes to compromise an entire system."
- **Constants: none.**

## 8b. zhang2023: NCR (p. 32) and MTTC

**Is there an equation? No, for either.**

- **NCR.** `docs/sources/lit_review/zhang2023.md` l.420, §5, printed p. 32 (PDF p. 33). Verbatim: "we use Network Compromise Ratio (NCR) as the simulation checkpoint to evaluate MTD techniques and their combinations. NCR is the ratio of compromised hosts to the total number of hosts in the network. It helps us measure the effectiveness of our MTD techniques by measuring the time it takes for the adversary to compromise a certain proportion of hosts in the network. In this perspective, we set the terminating condition for the simulation as the NCR reaching 0.8 and run the simulation 100 times for each variable set to obtain statistically significant results."
- **MTTC.** l.250, §3.4, printed p. 16 (PDF p. 17). Verbatim: "Mean Time to Compromise (MTTC), which measures the time it takes for an attacker to compromise a target host on the network [4]." ([4] is Cho 2020.) The operational reading is at l.443, §5.1, p. 33: "the average time for the adversary to compromise 80% nodes of the target network". Fig. 8 caption, p. 34: "Mean Time to Compromise on 0.8 NCR".
- **Constants.** NCR 0.8 is given no reason beyond "a certain proportion". The 100 runs are justified only "to obtain statistically significant results". MTD intervals are "ranging from 50 to 200 seconds" (l.418).
- **Symbolic form.** The nearest held source is Ho 2024, Eq. (10) (PDF p. 20; **the md has it only as an omitted picture**, `ho2024.md` l.350; read from the PDF). Verbatim: "HCR = Ct / Thost (10) where Ct is the number of compromised hosts at time t and Thost is the total number of hosts in the network."

## 8c. mcqueen2006: time-to-compromise

**There is an equation, but it is an analytical expected value for one component. It is not a mean over runs, and it is never called "MTTC".**

- **Locator:** `docs/sources/tactic_profiles/step_c/mcqueen2006_time_to_compromise.md` (INL preprint, OSTI 911165).
- **Definition** (§3, PDF p. 4, l.149–152), verbatim: "The time-to-compromise (Tpi) is defined as the time needed for an attacker to gain some level of privilege p on some system component i. Tpi depends on the nature of the vulnerabilities and the attacker skill level. Tpi is modeled as a random process composed of the following three attacker subprocesses".
- **Eq. (6)** (§3.4, PDF p. 12, l.588–596), verbatim: "T = t1 P1 + t2 (1−P1)(1−u) + t3 u(1−P1). (6) where T is the expected value of time-to-compromise; t1 is the expected value of Process 1 (1 day); t2 is the expected value of Process 2 (from Equation 3); t3 is the expected value of process 3 (from Equation 5); u = (1 – (AM/V))^v probability that Process 2 is unsuccessful (u=1 if V=0)". Also l.578: "For now, the analysis only uses the expected value of the time-to-compromise."
- **Supporting equations:**
  - Eq. (1): "P1 = 1 − e^(−vm/k)", with "k is 9447 … the total number of nonduplicate-known vulnerabilities found in the ICAT database";
  - Eq. (3): "t2 = 5.8 ET";
  - Eq. (5): "t3 = ((V/AM) − 0.5) 30.42 + 5.8".
- **Constants and their justification, verbatim** (PDF p. 6, l.254–258): "Somewhat arbitrarily, we decided to use 8 hours (one working day) as the mean time for a successful attack in Process 1, since it is at least marginally more in line with Cohen's comment." The 5.8 days is "the average time from vulnerability announcement to exploit code availability, which according to [6] is 5.8 days" (PDF p. 8).

---

## Which sources state a time constant, and why

| Source | Time constant stated | Justification given |
|---|---|---|
| rodriguez2024 | none (whole log pooled) | — |
| hong2018 (APV) | none | "there are no arbitrary values that need to be assigned to compute APV" |
| zhan2013 | attack rate per unit time; per-hour in the case study. Flow timeout 60 s and lifetime 300 s (pre-processing) | "(e.g., minute or hour or day)"; "The choice of per-hour is natural, while noting that per-day attack rate is not appropriate because each period is no more than 80 days"; 60 s and 300 s cited to [13] |
| zaffarano2015 | none in any metric (only a workload of "60 emails, one every second") | — |
| cisar2010ewma | λ dimensionless (0.2–0.3 usual; 0.05–0.25 per Lucas & Saccucci; 0.75 tuned); sampling set by MRTG's 5 min / 30 min / 2 h averages; k = 3 | "somewhat arbitrary"; optimal λ "depends … on the given size of the mean shift δ, but also on a given in-control Average Run Length"; λ tuned by minimum MSE on their traffic |
| alavizadeh2022 | none in MF (ALE is annual by definition) | — |
| bruneau2003 | none: t0 is the event, t1 is complete repair (from the data) | — |
| cho2020 | none | — |
| zhang2023 | NCR 0.8 stop; 100 runs; MTD intervals 50–200 s | "a certain proportion"; "to obtain statistically significant results" |
| mcqueen2006 | t1 = 8 h (1 day); 5.8 days; k = 9 447; 30.42 | "Somewhat arbitrarily"; 5.8 d from [6] |

**For the author's six numbers:**
- **1 000 s** (attack-rate unit): licensed as a unit choice by Zhan's "unit time (e.g., minute or hour or day)". The value itself is presentational.
- **κ = 60 s:** no source fixes it. Čisar give only a dimensionless λ with "somewhat arbitrary" conventional values and tune λ on data. Zhan's 60 s is a flow timeout and must not be borrowed. κ needs its own reason, or the appendix sweep.
- **1 500 s** (confidentiality bins): no source. Zaffarano have no time dimension.
- **125 s, 750 s, 1 250 s:** no source. Bruneau's window runs from the event to full recovery, and he has no bins and no pre-event averaging window. The 1 250 s is defensible only as the thesis's own reason (the next deployment's window).

Two sources say outright that their constants are arbitrary: Čisar ("somewhat arbitrary") and McQueen ("Somewhat arbitrarily"). Hong claims the opposite for APV.

---

## Summary table

| Metric (tex) | Source has an equation? | Source notation (verbatim form) | Closest faithful way to present the adaptation |
|---|---|---|---|
| Relative tactic occurrence (rodriguez2024) | **n** (a ProM table column) | "Occur. (rel.)" = Occur. (abs.) / Total number of events | Keep Eq. `eq:rto` as the thesis's own notation. Say "the relative occurrence Rodríguez et al. tabulate (Table 3)", then the step-for-event change |
| APV (hong2018) | **y**, Eqs. 1–2 | $\Delta AP_{i,i-1}=\frac{\lvert AP_i-AP_{i-1}\rvert}{\lvert AP_i\rvert}$; $APV=\frac{\sum_{i=1}^{\lvert S\rvert}\Delta AP_{i,i-1}}{\lvert S\rvert-1}$ | Quote Eq. 2 as printed, then the mapping (network states → runs, available → taken paths). The literal transposition is pairwise (Gini–Simpson). The modal form is the code's and must be named as a change of form |
| Attack rate (zhan2013) | **n** (words; process $\{X_t\}$) | "number of attacks that arrive at unit time" | Quote the words. The equation is ours. Unit per Zhan's "unit time". **Rename λ** if Čisar's λ is quoted |
| Attack confidentiality (zaffarano2015) | **y**, generic (unnumbered) | $\mathrm{Confidentiality}(M,\nu)=\frac{1}{\lvert T\rvert}\sum_{\tau\in T}\nu(\tau,\mathit{unexposed})$; ν from a run; exposure = "visible in plaintext in network traffic" | Quote it, then substitute: $T\to$ actions in bin $b$ over $\mathcal{R}$, $\nu(\tau,\mathit{unexposed})\to\mathbf{1}[D_r(j)<\theta]$. Zaffarano have no detector or window, so both are declared as ours |
| Detector D (cisar2010ewma) | **y**, Eq. 1 (+ Eqs. 2–3) | $EWMA_t=\lambda Y_t+(1-\lambda)EWMA_{t-1}$, $0<\lambda\le1$ "depth of memory"; UCL $=EWMA_0+k\sigma_{EWMA}$ | Quote Eq. 1, then state the event-time limit ($\lambda=1-e^{-\Delta/\kappa}$, $D/\kappa$) as our derivation. θ as a reference-calibrated alarm (Čisar: mean + 3σ; ours: median) |
| ASP (cho2020) | **n** | "the probability that attacks are successfully performed" | Quote it, then Eq. `eq:asp` as the estimator (the current tex is right) |
| NCR (zhang2023; Ho Eq. 10) | Zhang **n**; Ho **y** | Zhang in words; Ho: $HCR=C_t/T_{host}$ | Quote Zhang's words, show Ho's Eq. 10 as the form, read at the run's end (a choice of $t$) |
| MTTC (zhang2023; mcqueen2006) | Zhang **n**; McQueen **y** (analytical) | Zhang: "time … to compromise a target host", read at 0.8 NCR; McQueen: $T=t_1P_1+t_2(1-P_1)(1-u)+t_3u(1-P_1)$ | Do not quote McQueen's Eq. 6 (a different estimator). Quote Zhang's words and state the checkpoint change (0.8 NCR → first host) |
| NCR reduction (alavizadeh2022) | **y**, Eq. 13 (piecewise) | $MF^m=1-ALE^m_c/ALE_c$ if $ALE^m_c<ALE_c$, else 0 | Quote Eq. 13 whole, then $ALE\to\mathrm{NCR}$ and the floor dropped |
| NCR growth rate / time lost (bruneau2003) | **y** (unnumbered) | $R=\int_{t_0}^{t_1}[100-Q(t)]\,dt$; $t_0$ event, $t_1$ complete repair; 100 % = no degradation | Quote it, then $Q/100\to\tilde g$ (normalised by $\bar g_-$), $t_0\to t_d$, $t_1\to$ fixed 1 250 s (lower bound), $-L_{\text{none}}$ added |
