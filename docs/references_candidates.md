# References — Candidate List (Phase 2, Step 1)

**Source:** Bibliographies of four prior theses on MTD/MTDSim
**Compiled:** 29 April 2026
**Status:** Pre-screening. Not yet read. Tagged by likely lit-review section.

> **Methodology:** Extracted full bibliographies from Tay (2024, 37 refs), Zhang (UWA, 2022, 40 refs), Ho (2024, 38 refs), and Dunstall (BACS, 64 refs). Cross-referenced to identify convergence (papers cited by ≥2 theses → strong canonical signal). Tagged each candidate to lit-review section per `lit_review_plan_v2.md`. **Total deduplicated unique candidates: ~85.**

---

## 1. High-convergence canonical references (cited by 3+ theses)

These are the "everyone-cites-them" anchors. Treat as **must-include** unless a clear reason emerges to drop them.

| # | Reference | Cited by | Section | Notes |
|---|---|---|---|---|
| C1 | **Cho et al. 2020** "Toward Proactive, Adaptive Defense: A Survey on MTD" *IEEE Comm. Surv. Tutor.*, 22(1):709–745 | All 4 | §1.1, §1.3 | Canonical MTD survey. Q1. Foundational. |
| C2 | **Hong, Enoch, Kim et al. 2018** "Dynamic Security Metrics for Measuring the Effectiveness of MTD" *Comput. Secur.*, 79:33–52 | All 4 | §1.2, §3.2 | Jin's own paper. Direct lineage. Q1. |
| C3 | **Alshamrani et al. 2019** "A Survey on APTs" *IEEE Comm. Surv. Tutor.*, 21(2):1851–1877 | Zhang, Ho, Dunstall | §2.3 | Canonical APT survey. Q1. |
| C4 | **Sengupta, Chowdhary et al. 2020** "A Survey of MTD for Network Security" *IEEE Comm. Surv. Tutor.*, 22(3):1909–1941 | Tay, Zhang, Dunstall | §1.1 | Second canonical MTD survey. Q1. |
| C5 | **Cai, Wang et al. 2016** "Moving Target Defense: State of the Art and Characteristics" *Front. Inf. Technol. Electron. Eng.*, 17(11):1122–1153 | Tay, Zhang, Dunstall | §1.1 | Older but foundational. |
| C6 | **Alavizadeh, Hong, Jang-Jaccard, Kim 2018** "Evaluation for Combination of Shuffle and Diversity on MTD Strategy for Cloud" *TrustCom* | Tay, Zhang, Ho | §1.2, §1.3 | Direct lineage paper. SDR combinations. |
| C7 | **Alavizadeh, Kim, Hong, Jang-Jaccard 2017** "Effective Security Analysis for Combinations of MTD Techniques on Cloud" *ISPEC* | Tay, Zhang, Ho | §1.2 | Foundational SDR analysis. |
| C8 | **Yao et al. 2023** "Adversarial Decision-Making for MTD: A Multi-Agent Markov Game and RL Approach" *Entropy*, 25(4):605 | Tay, Ho, Dunstall | §1.3, §3.3 | RL+MTD; adversarial framing. Q2. |
| C9 | **Q. Zhang et al. 2023** "EVADE: Efficient MTD for Autonomous Network Topology Shuffling Using Deep RL" *ACNS* | Tay, Ho, Dunstall | §1.3 | Recent DRL-MTD. |

> **Read priority for these nine:** C1 (Cho), C3 (Alshamrani), C2 (Hong), C4 (Sengupta) **first** — they anchor §1.1, §1.3, §2.3, §1.2 respectively. The Alavizadeh papers (C6, C7) supply §1.2 examples. The RL papers (C8, C9) populate §1.3 and §3.3.

---

## 2. Direct UWA lineage / Hong-supervised

These are your immediate predecessors. Cite respectfully, position them as building the simulator paradigm you're now extending.

| # | Reference | Section | Notes |
|---|---|---|---|
| L1 | **Tay, J. K. 2024** *Using AI to Automate the Deployment of MTD Operations* — Master's thesis, UWA | §1.3, §3.1 | THE direct predecessor. RL-driven MTD selection. |
| L2 | **Ho, W. H. 2024** *Using AI to Automate the Deployment of MTD Operation* — Master's thesis, UWA | §1.3, §3.1 | Parallel UWA work. Metric-feature ablation. |
| L3 | **Zhang, W. 2023** *Evaluating Multiple Moving Target Defense in the Time Domain* — UWA work (cited by Ho [16]) | §1.2, §1.3 | Time-domain MTD evaluation; created MTDSimTime. |
| L4 | **Brown, Lee, Hong 2023** "Evaluating MTD against Realistic Attack Scenarios" *EnCyCriS workshop* | §1.2, §3.1 | The MTDSim-origin paper. Direct lineage. |
| L5 | **Brown, A. 2021** *MTDSim* — repo (cited Ho [17]) | §3.1 | Original MTDSim software artifact. |
| L6 | **Hong, J. & Kim, D. S. 2012** "HARMs: Hierarchical Attack Representation Models for Network Security Analysis" *AISM* | §1.2 | Foundational network-security modelling paper. Jin's own. |
| L7 | **Sharma, Enoch, Cho, Moore et al. 2020** "Dynamic Security Metrics for SDN-based MTD" *J. Netw. Comput. Appl.*, 170 | §1.2 | Hong-cluster collaboration. |
| L8 | **Enoch, Ge, Hong, Alzaid, Kim 2018** "A Systematic Evaluation of Cybersecurity Metrics for Dynamic Networks" *Comput. Netw.*, 144 | §1.2 | Hong-cluster. Dunstall [51]. |
| L9 | **Yusuf, Ge, Hong, Kim, Kim, Kim 2016** "Security Modelling and Analysis of Dynamic Enterprise Networks" *IEEE CIT* | §1.2 | Hong-cluster. |

---

## 3. MTD Orchestration & Adaptive Selection (§1.3)

Beyond the canonical surveys above. Includes IDS-aware / observation-driven and RL-driven adaptive MTD.

| # | Reference | Section | Notes |
|---|---|---|---|
| O1 | **Sun, Zhu, Fei, Chen 2023** "A Survey on MTD: Intelligently Affordable, Optimized and Self-Adaptive" *Appl. Sci.*, 13:5367 | §1.3 | Adaptive MTD survey. Ho [15], Dunstall [16]. |
| O2 | **Tan et al. 2023** "A Survey: When MTD Meets Game Theory" *Comput. Sci. Rev.*, 48 | §1.2 | Game-theoretic angle. Dunstall [15]. |
| O3 | **Eghtesad, Vorobeychik, Laszka 2020** "Adversarial Deep RL Based Adaptive MTD" *GameSec* | §1.3, §3.3 | Adversarial RL-MTD. Ho [13], Dunstall [21]. |
| O4 | **Sengupta & Kambhampati 2020** "Multi-agent RL in Bayesian Stackelberg Markov Games for Adaptive MTD" arXiv | §1.3 | Stackelberg-game adaptive MTD. Ho [26], Dunstall [32]. |
| O5 | **T. Zhang et al. 2023** "How to Disturb Network Reconnaissance: A MTD Approach Based on DRL" *IEEE TIFS*, 18 | §1.3 | DRL-MTD against reconnaissance. Q1. |
| O6 | **T. Zhang et al. 2023** "When MTD Meets Attack Prediction in Digital Twins" *IEEE JSAC*, 41(10) | §1.3 | Hierarchical RL + attack prediction. Q1. |
| O7 | **Yoon, Cho, Kim, Moore et al. 2021** "DESOLATER: DRL-based Resource Allocation and MTD Deployment" *IEEE Access*, 9 | §1.3 | DRL + MTD deployment. Dunstall [17]. |
| O8 | **Chowdhary, Huang et al. 2021** "SDN-based MTD using Multi-Agent RL" | §1.3 | MARL + SDN MTD. Ho [18]. |
| O9 | **Li & Zheng 2022** "Robust MTD Against Unknown Attacks: Meta-RL Approach" *GameSec* | §1.3 | Meta-RL for unknown-attack robustness. Dunstall [19]. |
| O10 | **Sengupta, Chakraborti, Kambhampati 2019** "MTDeep: Boosting Security of DNNs Against Adversarial Attacks with MTD" | §1.3 | MTD applied to ML defence (adjacent). Ho [14]. |
| O11 | **Lei, Zhang, Tan et al. 2018** "MTD Techniques: A Survey" *Secur. Commun. Netw.*, 2018 | §1.1 | Older taxonomy. Dunstall [14]. |

---

## 4. Foundational MTD Mechanisms (§1.1, §1.2 — context only, cite sparingly)

| # | Reference | Section | Notes |
|---|---|---|---|
| F1 | **Jajodia, Ghosh, Swarup, Wang, Wang 2011** *Moving Target Defense: Creating Asymmetric Uncertainty for Cyber Threats* — Springer book | §1.1 | The foundational MTD volume. Zhang [2]. |
| F2 | **Huang & Ghosh 2011** "Introducing Diversity and Uncertainty to Create Moving Attack Surfaces for Web Services" — *MTD Springer book* | §1.1 | Foundational diversity MTD. Tay [9]. |
| F3 | **Zhuang, Zhang, Bardas, DeLoach, Ou, Singhal 2013** "Investigating the Application of MTD to Network Security" *ISRCS* | §1.1 | Foundational MTD framework paper. Tay [11]. |
| F4 | **MacFarland & Shue 2015** "The SDN Shuffle: Creating a Moving-Target Defense Using Host-Based SDN" *MTD Workshop* | §1.1 | SDN MTD example. Tay [10]. |
| F5 | **Jafarian, Al-Shaer, Duan 2012** "OpenFlow Random Host Mutation: Transparent MTD Using SDN" *HotSDN* | §1.1 | IP shuffle classic. Zhang [30]. |
| F6 | **Albanese, De Benedictis, Jajodia, Sun 2013** "A MTD Mechanism for MANETs Based on Identity Virtualization" *IEEE CNS* | §1.1 | Dunstall [3]. |
| F7 | **Al-Shaer, Duan, Jafarian 2012** "Random Host Mutation for MTD" *SecureComm* | §1.1 | Dunstall [5]. |

---

## 5. MTD Performance / Evaluation (§1.2)

| # | Reference | Section | Notes |
|---|---|---|---|
| E1 | **Connell, Menascé, Albanese 2017** "Performance Modeling of MTDs" *MTD Workshop* | §1.2 | Performance modelling MTD. Zhang [19]. |
| E2 | **Connell, Menascé, Albanese 2021** "Performance Modeling of MTDs with Reconfiguration Limits" *IEEE TDSC*, 18(1) | §1.2 | Q1 extension of [E1]. Zhang [20]. |
| E3 | **Chen, Chang, Mišić et al. 2020** "Model-based Performance Evaluation of a MTD System" *GLOBECOM* | §1.2 | Zhang [18]. |
| E4 | **Cai et al. 2016** "A Model for Evaluating and Comparing MTD Techniques Based on Generalized Stochastic Petri Net" — Petri net + MTD! | §1.2 | **Highly relevant to your Petri-net direction.** Zhang [26]. |
| E5 | **Torquato, Maciel, Vieira 2021** "PyMTDEvaluator: A Tool for Time-Based MTD Evaluation" *IEEE ISSRE* | §1.2 | Adjacent simulator/tool. Zhang [22]. |
| E6 | **Xiong, Ma, Cui 2019** "Simulation Environment of Evaluation and Optimization for MTD: A SimPy Approach" | §1.2 | Pre-MTDSim simulator. Zhang [23]. |
| E7 | **Alhozaimy & Menascé 2022** "A Formal Analysis of Performance-Security Tradeoffs Under Frequent Task Reconfigurations" *FGCS*, 127 | §1.2 | Q1 formal analysis. Ho [10]. |
| E8 | **Nguyen, Kim, Lee, Min, Lee, Kim 2021** "Performability Evaluation of Switch-Over MTD Mechanisms in SDN Using Stochastic Reward Nets" *J. Netw. Comput. Appl.*, 199 | §1.2 | Stochastic-reward-net (Petri-net cousin). Ho [11]. |
| E9 | **Mendonça, Cho, Moore, Nelson, Lim, Kim 2021** "Performance Impact Analysis of Services Under a Time-Based MTD Mechanism" *J. Defense Modeling Simul.*, 20 | §1.2 | Ho [12]. |
| E10 | **Ben-Asher, Morris-King, Thompson, Glodek 2016** "Attacker Skill, Defender Strategies and the Effectiveness of Migration-Based MTD" *ICCWS* | §3.1 | Attacker-skill paper — relevant to your gap argument. Tay [8]. |
| E11 | **Winterrose, Carter, Wagner, Streilein 2020** "Adaptive Attacker Strategy Development Against MTD Cyber Defenses" | §3.1, §3.3 | Direct adaptive-attacker work. Tay [18]. |
| E12 | **Moghaddam, Kim, Cho et al. 2022** "A Practical Security Evaluation of a MTD Against Multi-Phase Cyberattacks" | §3.1 | **Very relevant — multi-phase attacker.** Ho [28]. |
| E13 | **Alavizadeh, Aref, Kim, Jang-Jaccard 2022** "Evaluating the Security and Economic Effects of MTD on the Cloud" *IEEE TETC*, 10(4) | §1.2 | Q1. Ho [23]. |
| E14 | **Alavizadeh, Kim, Jang-Jaccard 2020** "Model-Based Evaluation of Combinations of Shuffle and Diversity MTD on the Cloud" *FGCS*, 111 | §1.2 | Q1. Zhang [11], Ho [31]. |
| E15 | **Alavizadeh, Hong, Kim, Jang-Jaccard 2021** "Evaluating the Effectiveness of Shuffle and Redundancy MTD Techniques in the Cloud" *Comput. Secur.*, 102 | §1.2 | Q1. Zhang [9], Ho [7]. |

---

## 6. Threat Modelling, Cyber Kill Chain, ATT&CK (§2)

| # | Reference | Section | Notes |
|---|---|---|---|
| T1 | **Hutchins, Cloppert, Amin 2011** "Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains" — Lockheed Martin | §2.1, §2.3 | The Lockheed Cyber Kill Chain paper. Ho [20]. |
| T2 | **MITRE ATT&CK Framework** — primary reference (att&ck.mitre.org) | §2.1 | Cited by Zhang [15], Ho [21]. |
| T3 | **Lockheed Martin** "Cyber Kill Chain (CKC)" — original web reference | §2.1 | Zhang [14]. |
| T4 | **Cho & Ben-Asher 2018** "Cyber Defense in Breadth: Modeling and Analysis of Integrated Defense Systems" *J. Defense Modeling Simul.*, 15(2) | §3.3 | Dunstall [4]. |

> **GAP — what's missing from these bibliographies for §2:** None of the four theses cite Bianco's Pyramid of Pain, the MITRE Attack Flow corpus, Strom et al.'s ATT&CK design paper, Rahman's co-occurrence/FP-Growth work, or Zang et al.'s threat-intelligence fusion work. **These will need to be sourced via Connected Papers / direct search.** Items in your 26 March meeting list (Zhang 2025, Zang 2026, Rashid & Such 2025, Kim 2026, He 2025) also need to be added separately — they're not in any prior thesis.

---

## 7. Reinforcement Learning foundations (§1.3 background only — cite minimally)

> **Curation note:** The four theses cite ~30 RL-foundation references (Mnih DQN, Sutton & Barto, Van Hasselt double Q, etc.). For *your* lit review these are largely irrelevant — your contribution isn't an RL contribution and your gap isn't an RL-method gap. Cite at most 1–2 to anchor the "RL-MTD" thread in §1.3, or skip entirely and let the RL-MTD application papers (O1–O11) carry the weight.

| # | Reference | Section | Notes |
|---|---|---|---|
| R1 | **Mnih et al. 2015** "Human-Level Control Through DRL" *Nature*, 518 | §1.3 (optional) | DQN foundational. Tay [28], Dunstall [23]. |
| R2 | **Sutton & Barto 2014** *Reinforcement Learning: An Introduction* — MIT Press | §1.3 (optional) | The textbook. Tay [36]. |

*(All other RL-foundation refs from the four theses excluded from this candidate list — out of scope for your lit review.)*

---

## Cross-thesis convergence summary

| Refs cited by 4 theses | 2 (C1 Cho 2020, C2 Hong 2018) |
| Refs cited by 3 theses | ~7 (C3–C9) |
| Refs cited by 2 theses | ~14 (across O, E, F categories) |
| Unique-to-one-thesis | ~155 (most filtered out for your scope) |

**Strongest signal:** the Hong-cluster MTD evaluation lineage (C2, C6, C7, E14, E15, L1–L9). This is your scholarly inheritance — by the time you submit, examiners will expect you to have engaged with these critically and positioned your work in relation to them.

---

## What's NOT in the prior theses (gaps to fill)

These categories will need direct search via Connected Papers / Google Scholar / forward-citation chasing:

1. **CTI-derived attack profiling** (§2.4) — Rahman 2022 (FP-Growth), Zang et al. 2023 (CTI fusion), Attack Flow corpus papers, NLP-from-CTI work.
2. **Pyramid of Pain** (§2.2) — Bianco's original blog post + any academic uptake.
3. **2025–2026 state-of-the-art** — Zhang et al. 2025 MTD-meets-AI survey, Rashid & Such 2025, Kim et al. 2026, He et al. 2025, Zang et al. 2026, Swati et al. 2025 (already in Dunstall [56]). All flagged in your 26 March meeting minutes.
4. **APT campaigns at TTP fidelity** (§2.3, §2.4) — only Alshamrani 2019 from the prior theses; need 1–2 more recent APT-behavioural papers.
5. **MTD mapped to Pyramid of Pain levels** (§3.2) — likely doesn't exist; that's part of the gap argument.

---

## Triage targets for next phase

When you move into Phase 3 (screen-and-cull), aim to:

- **Keep all 9 high-convergence (§1)** — these are non-negotiable canonical anchors.
- **Keep all 9 UWA lineage (§2)** — required for positioning.
- **Cull category §3 (Adaptive MTD)** to ~4–5 — pick the ones that best illustrate "adaptive MTD evaluated against procedural attackers" for your §3.3 gap argument.
- **Cull §4 (Foundational mechanisms)** to ~3–4 — minimum needed to anchor the SDR taxonomy in §1.1.
- **Cull §5 (MTD evaluation)** to ~5–6 — including E4 (Petri-net + MTD, methodologically relevant) and E10/E11/E12 (attacker-realism critiques, directly support your gap).
- **§6 (ATT&CK / kill chain) — keep all 4**, add ~3–5 new from outside-thesis search.
- **§7 (RL foundations) — drop or keep 1.**

**Working target after triage: 25–30 references in deep-read pile, narrowing to ~14 cited in final lit review.**

---

## Next steps

1. ☐ Add the 26 March meeting candidates (Zhang 2025, Zang 2026, Rashid & Such 2025, Kim 2026, He 2025) to a parallel `references_external.md`.
2. ☐ Run Connected Papers on three anchors: **Cho 2020 (C1)**, **Tay 2024 (L1)**, **Zhang 2025 MTD-meets-AI** (once added).
3. ☐ Direct search for §2.4 candidates (Rahman 2022 co-occurrence, Attack Flow papers, Zang 2023 CTI fusion).
4. ☐ Direct search for Bianco Pyramid of Pain.
5. ☐ Move to Phase 3 (triage screen — abstract/intro/conclusion) with combined list.
