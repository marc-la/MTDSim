# Verify B: attack rate, attack confidentiality, ASP (Table 4.3)

Read-only session, 2026-09-30. Every quote below was re-read in this session from the source text.
Dissertation text is §4.5 of `docs/thesis/dissertation.tex` at commit 36999e59 (the live-text extract) l.49-99.

Sources read:
- Zhan, Xu, Xu 2013: `docs/sources/s45_fetched/zhan2013.txt` (arXiv 1603.07433, the authors' copy of IEEE TIFS 8(11):1775-1789). Page numbers below are arXiv PDF pages.
- Pendleton et al. 2016: `docs/sources/methodology/pendleton2016_security_metrics_survey.md` (arXiv 1601.05792v1, the only arXiv version; published CSUR version not obtainable: ACM and ResearchGate both returned a bot-challenge page).
- Kim et al. 2026: `docs/sources/lit_review/3_2_kim2026mtdid.md`.
- Zaffarano et al. 2015: `docs/sources/lit_review/zaffarano2015.md` + `zaffarano2015.pdf` (8 PDF pages = proceedings pp. 3-10; pages below are proceedings pages, from pypdf).
- Jung et al. 2004: `docs/sources/s45_fetched/trw.txt` (IEEE S&P 2004, open copy).
- Cho et al. 2020: `docs/sources/lit_review/1_1_cho2020toward.md` + `lit_review/original/1.1_cho2020toward.pdf` (page numbers from the PDF running header).
- Cho & Ben-Asher 2018: `docs/sources/lit_review/chobenasher2018.md`.

---

## 1. Attack rate, cited to zhan2013

**Source's name:** "attack rate". It is Zhan's own term: it appears in the abstract, the introduction and every table.

**Source's definition (verbatim).** §III-B "The Framework", Step 2 "Basic statistical analysis", arXiv p. 3 (zhan2013.txt l.313-318):
> "For stochastic cyber attack processes, the primary statistic is the attack rate, which describes the number of attacks that arrive at unit time (e.g., minute or hour or day). Note that attack rate can be instantiated at various resolutions of attack processes, such as: network-level attack rate, victim-level attack rate and port-level attack rate."

Also §I, p. 1 (l.80-81): "attack rate (i.e., number of attacks per time unit)".

**Unit and perspective (verbatim).**
- What an attack is: §III-B Step 1, p. 3: "It is now a common practice to treat honeypot-captured data as attacks because there are no legitimate services and the honeypot computers passively wait for incoming events." Also: "we advocate using flows, rather than IP packets, to represent attacks". An attack is a TCP/UDP flow arriving at a honeypot IP.
- Perspective: the victim's side, with many attackers arriving. Fig. 1 caption, p. 3: "a victim is attacked by N attackers (or attacking computers) at some ports and the attacks arrive at time t1,...,t9."
- Unit: free ("e.g., minute or hour or day"). The case study uses per hour (§IV, p. 5, l.493: "We consider the per-hour attack rate at three resolutions").
- Zhan's "attacker-level attack process" (§IV-E, p. 10) is **not** a per-attacker rate: "we only consider the first attack launched by each attacker, while disregarding the subsequent attacks launched by the same attacker". It counts distinct attackers arriving at one victim. Do not use it to claim that Zhan has a one-attacker rate.

**Dissertation's text:**
> "Attack rate is ``the number of attacks that arrive at unit time'' \citep[Sec.~III-B]{zhan2013}. Here it is the number of an attacker's actions per minute. [...] A higher rate is a more aggressive attack \citep{pendleton2016}."

- The quote is an exact substring of Zhan's sentence. The locator Sec. III-B is correct.
- The Pendleton claim: arXiv v1 §5.1 "Measuring the threat landscape", p. 15 (l.770-772): "Another related attack rate metric measures the number of attacks that arrive at a system of interest per unit time [Zhan et al. 2013; Zhan et al. 2015]. These metrics reflect the aggressiveness of cyber attacks." The paraphrase is faithful. Two caveats: Pendleton's scope is the threat landscape (many attackers), not one attacker, and the wording is confirmed only in arXiv v1. The bib entry is the published CSUR version, and the bib's own VERIFY comment is still open.

**Verdict: adapted, and stated only weakly.** "Here it is" marks a change, but the text never says what changed. The quote says "attacks that arrive", and the reader is not told that these are flows from many attackers arriving at a honeypot, not one attacker's own actions. An examiner who opens Zhan will see the perspective flip: victim-side arrivals from many sources become attacker-side emissions from one source. Nothing is misattributed. The counting operation (events per unit time) is Zhan's, and the unit (minute) is one Zhan lists.

**Is it the source an examiner expects?** Yes, as the definitional origin. Pendleton's security-metrics survey credits attack rate to Zhan 2013, so Zhan plus Pendleton is the canonical pair. No source I read defines a one-attacker action rate as a named output metric. Alternatives an examiner might raise:
- **Kim et al. 2026** is in the MTD lineage and uses the same perspective and unit: Table 4, p. 9 (kim2026 md l.363): "ATK_λ | Attack rate per 1 min. | 0.2 [#/min.]". §6.1.1 (l.382): "the attack workloads follow the Poisson distribution with the attack rate ( ATK_λ ) of 0.2 [#/min.]". There it is a declared **input** for one attacker, not a measured metric. It is useful as a supporting cite for "one attacker's rate, per minute, in MTD evaluation". It cannot replace Zhan.
- **Zaffarano 2015's "attack productivity"** is the same paper as row 2. Table 4, p. 9: "Attack Productivity is a measure of how quickly an attacker can perform and complete adversarial tasks". §4.1, p. 9: "Attacker productivity is the rate at which attacker tasks are completed". Its formula, however, is the mean task *duration* ("the average of the duration attribute over the tasks in M"), so it is not an action count per time. An MTD examiner could ask why this sibling metric was not used. It is not a better citation for the quantity the dissertation computes.

**Confidence: high** that the quote, locator and Pendleton paraphrase are correct (read verbatim). **Medium** on "examiner expects": the choice is defensible, but no source defines the one-attacker version.

**Smallest fix:** state the adaptation in one clause. For example: "Zhan et al. count the attacks arriving at a honeypot; here it is the number of one attacker's own actions per minute." Optionally add `kim2026` to the second sentence for the one-attacker, per-minute precedent. Keep `pendleton2016` on the "to download" list (published CSUR wording) and resolve its bib VERIFY before submission.

---

## 2. Attack confidentiality, cited to zaffarano2015

**Source's name:** "Attack Confidentiality". The general metric is "Confidentiality", and its attacker-model instance is "Attack Confidentiality".

**Source's definition (verbatim).**
- Table 4 "MTD Effectiveness Metrics", p. 9: "Attack Confidentiality is a measure of how much attacker activity may be visible by detection mechanisms".
- §4.3 "Confidentiality", p. 9-10: "Confidentiality is a measure of how much information is exposed by activity model tasks. For the mission model, exposing information is typically undesirable, whereas an attacker being exposed is desirable. Confidentiality is computed similarly to the metrics above, with the same type of costs and benefits derived from them. For a mission model M, we have: Confidentiality(M,ν) = 1/|T| Σ_{τ∈T} ν(τ,unexposed)".
- The indicator, §3.2, p. 7: "unexposed: whether task information was exposed, values are 0 (information was exposed) and 1 (information was not exposed)".
- Their exposure rule, §4.3, p. 10: "In principle, there are many ways in which information could be exposed [...] but in these initial experiments, we simply refer to whether information is visible in plaintext in network traffic."

**Direction.** The formula averages the *unexposed* indicator, so a higher value means fewer tasks exposed, which for the attacker model means a stealthier attacker. Zaffarano prints the formula only "For a mission model M". The attacker version follows from "computed similarly" and from the parallel productivity and success definitions ("when M is an instance of the attacker model, we call its productivity attacker productivity"). "A higher attack confidentiality is a stealthier attacker" is therefore faithful. Warning: Cho 2020 §VII-A (p. 728) relays this metric with the opposite polarity: "attack confidentiality means the degree of attack behaviors detected by a defender". Do not cite Cho for it.

**Dissertation's text:**
> "Attack confidentiality is ``how much attacker activity may be visible by detection mechanisms'' \citep[Table~4]{zaffarano2015}, the share of the attacker's actions that are not exposed. MTDSim has no detection mechanism, so an action is exposed here when a standard scan detector would flag it. Scan detectors flag ``N events within a time interval of T seconds'' \citep[Sec.~2]{jung2004}; the default port-scan rule of the Snort intrusion detection system flags a source that connects to five addresses within 60\,s \citep[Sec.~6]{jung2004}. An action is flagged when it is at least the attacker's fifth action within one minute [...] A higher attack confidentiality is a stealthier attacker"

- The Table 4 quote is exact and the locator is correct.
- "the share of the attacker's actions that are not exposed" matches the §4.3 formula (mean of ν(τ, unexposed)), with tasks become actions.

**Verdict: adapted-and-stated for the exposure criterion, but Zaffarano's own criterion goes unmentioned.** The text says why a detector is substituted ("MTDSim has no detection mechanism"). It does not say that Zaffarano judge exposure as "visible in plaintext in network traffic". This matters little, because the Table 4 definition itself says "visible by detection mechanisms", so a detector is closer to Table 4's intent than Zaffarano's own plaintext rule. An examiner who reads §4.3 may still ask. The earlier draft (extract `04_attack_confidentiality.md`) carried that clause; the current text dropped it.

**Is it the source an examiner expects?** Yes. Zaffarano 2015 originates the metric under this name, at the ACM MTD workshop, and Cho 2020 surveys it as [173]. No alternative is needed.

**Jung 2004 defects (the detector citations inside this paragraph):**
1. **Wrong locator.** The Snort default is in **§5.2 "Comparison with Bro and Snort"** (PDF p. 11), not §6. §6 is "Discussion and Future Work" and never mentions Snort. Verbatim, §5.2: "For Snort, we consider its portscan2 scan-detection preprocessor [...] We use Snort's default settings, for which it flags a source IP address that has sent connections to 5 different IP addresses within 60 seconds." The error comes from `extractions/s45_metric_definitions/14_detector_conventions.md` l.29, which also says "§6". **Fix: `Sec.~5.2`.**
2. **The Snort default is dated.** It is Snort 2.0.2's portscan2 as of 2004 (§2, p. 3: "Snort [6] implements similar methods. Version 2.0.2 uses two preprocessors"). The present-tense "the default port-scan rule of the Snort intrusion detection system" reads as current Snort, whose Snort 3 `port_scan` defaults differ (record 14, l.21-28). Fix: "Snort's portscan2 default at the time".
3. **Actions are substituted for distinct addresses without saying so.** Snort counts connections to 5 *different IP addresses*. The dissertation flags an action when it is "at least the attacker's fifth action within one minute", so every action counts, repeats and non-connection actions included. That is a stated rule, but its difference from the quoted Snort rule is unstated.
4. The §2 quote "N events within a time interval of T seconds" is exact (§2, p. 3), and the locator is correct.
5. Jung supports the closing claim that "a slower attacker leaves more of its actions unflagged". §5.2: Snort "can also be easily evaded by a scanner who probes a network no faster than 5 addresses/minute." §2: "once the window size is known it is easy for attackers to evade detection by simply increasing their scanning interval." Either could be cited there.

**Confidence: high** on Zaffarano (verbatim, with page and formula checked). **High** on the Jung locator error (section headings checked in the text).

**Smallest fix:** (a) change `Sec.~6` to `Sec.~5.2`. (b) Add one clause after the Zaffarano sentence: "(Zaffarano et al. count a task exposed when it is visible in plaintext in network traffic [Sec. 4.3])". (c) Write "whose default at the time flags [...]" and "counting actions for addresses".

---

## 3. Attack success probability (ASP), cited to cho2020

**Source's name:** "Attack success probability (ASP)", as a bold-faced named entry in the attacker's metrics list.

**Source's definition (verbatim).** §VII-A "Metrics for Measuring MTD Effectiveness", **p. 727** (cho md l.578):
> "Attack success probability (ASP) [3], [11], [22], [25], [26], [28], [32], [45], [49], [136], [147], [173]: This metric refers to the probability that attacks are successfully performed. For example, it refers to the probability that a system component (or defender) is compromised or a target is successfully discovered or accessed by an attacker."

§VII-A, p. 729 (l.636): "the attack success probability (e.g., whether an attacker achieved its goal of a launched attack such as finding a vulnerable target) is a dominant metric used for the effectiveness of MTD aiming to minimize this metric".

**Origin or survey?** Cho surveys it and does not originate it. The twelve works Cho cites for it include Al-Shaer 2012 [3], Carroll 2014 [25], Carter 2014 [26], Cho & Ben-Asher 2018 [32], DeLoach/Zhuang 2014 [45], Evans 2011 [49] and Zaffarano 2015 [173]. The acronym and the one-line definition are Cho's synthesis. No single originating paper exists: ASP is a generic probability name used across MTD work. Of the cited works held locally:
- **Cho & Ben-Asher 2018** (`chobenasher2018`, in the bib) uses the name: "Attack success probability (PAS): Assuming that the system will fail when any one of VNs is compromised by an attacker, PAS is defined by:" (§4).
- **Al-Shaer 2012** uses "mutation success probability", a defender-side quantity, not ASP.
- **Kim 2026** uses ASP by name, split per kill-chain phase (ASP_REC, ASP_DEI).
- None of the MTDSim lineage papers (Brown 2023, Zhang 2023, Ho 2024, Tay 2024, Alavizadeh 2022) uses "attack success probability". Ho's ASR is a per-attempt rate.

**Dissertation's text:**
> "ASP is ``the probability that attacks are successfully performed'' \citep[Sec.~VII-A]{cho2020}. In the targeted scenario an attack succeeds when the attacker compromises a target host: ASP = runs that compromise a target host / runs."

- The quote is an exact substring. **The locator Sec. VII-A is correct**; if a page is wanted, it is p. 727.
- The success event (a target host compromised) is one of Cho's own examples ("a system component [...] is compromised or a target is successfully [...] accessed"). The share of runs is the standard relative-frequency estimate of a probability; Cho gives no estimator.

**Verdict: faithful.**

**Is it the source an examiner expects?** Yes, for a generic, field-standard metric: a canonical MTD survey that names it, defines it and calls it "a dominant metric" is the expected cite. An examiner would not demand an origin, because none exists. An optional strengthener is one primary use, `chobenasher2018` (held, in the bib, uses the name, and its success event is the compromise of any one target, like the dissertation's targeted scenario).

**Confidence: high.** The quote, section and page were read from both the markdown and the PDF.

**Smallest fix:** none required. Optionally write `\citep[Sec.~VII-A]{cho2020}` as `[Sec.~VII-A, p.~727]`, and add `chobenasher2018` as a named-use example.

---

## To download (paywalled or unobtainable here)
- Pendleton et al. 2016, ACM CSUR 49(4):62, doi 10.1145/3005714: confirm the §5.1 "aggressiveness" wording in the published version (bib VERIFY is open). ACM and ResearchGate blocked the fetch.
- Zhan et al. 2013, IEEE TIFS published version: only for page numbers. The arXiv copy carries the definition, and a section locator suffices.
