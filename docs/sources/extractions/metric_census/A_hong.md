# Census A: metrics in Jin B. Hong's locally held papers

Read-only census, 2026-09-23. No repo file edited.

## Scope and method

**Held and Hong-authored (the census proper):**
1. `hong2018`: J. B. Hong, S. Y. Enoch, D. S. Kim, A. Nhlabatsi, N. Fetais, K. M. Khan, "Dynamic security metrics for measuring the effectiveness of moving target defense techniques", *Computers & Security* 79 (2018) 33–52.
2. `brown2023`: A. Brown, T.-W. Lee, J. B. Hong, "Evaluating Moving Target Defenses against Realistic Attack Scenarios", IEEE/ACM EnCyCriS 2023, pp. 1–8.

**Search for others.** I grepped the author lines (the first 40 lines) of every `.md` under `docs/sources/**`, plus the full text of every `lit_review/*.md`, for "Hong". I also ran a `find` for Hong, HARM, Enoch and Alavizadeh files under `/home/marc`. No third Hong-authored paper is held:
- `alavizadeh2022` (`lit_review/alavizadeh2022.md`, IEEE TETC 2022, "Evaluating the Security and Economic Effects of MTD Techniques on the Cloud"). The authors are Hooman Alavizadeh, Samin Aref, Dong Seong Kim and Julian Jang-Jaccard. **Hong is not an author.** He is cited as "[23] Hong et al.", so the paper is excluded.
- `zhang2023`, `ho2024` and `tay2024` are UWA student reports that Hong **supervised**. He is not an author, so they are excluded. (They are the metric-richest MTDSim documents, but they belong in a separate census.)
- `masud2025`, `cho2020`, `kim2026mtdid`, `jalowski2026`, `chobenasher2018`, `added_mendonca2023`, `sharma2025` and the `tactic_profiles` hits only **cite** Hong. `sharma2025` is by D. P. Sharma alone.
- **hongkim2016** (Hong & Kim, "Assessing the effectiveness of moving target defenses using security models", IEEE TDSC 13(2):163–177): **NOT HELD.**
- **hongkim2012harm** (Hong & Kim, "HARMs: Hierarchical attack representation models for network security analysis", AISM/SECAU 2012): **NOT HELD.**

**Locators.** hong2018 locators come from the PDF (`docs/sources/lit_review/original/1.2_hong2018dynamic.pdf`). The source markdown drops every equation as an omitted image, so I rendered pp. 36, 37 and 39–44 as images and transcribed the equations from them. Journal page = PDF page + 32. brown2023 printed pages equal PDF pages 1–8, and Figs. 4 and 5 were checked on the rendered p. 6.

**Direction convention (hong2018).** "For attack efforts, a metric value toward one is making the attack more difficult, and for defense efforts, a metric value toward zero is making the defense more difficult" (§6.1.1, p. 45). All ten headline hong2018 metrics are normalised to [0, 1].

---

## Paper 1: hong2018

### 1A. Hong 2018's own metrics (headline, intermediate and compound)

| paper | metric name as written | acronym | definition / formula | perspective | measures | unit | locator |
|---|---|---|---|---|---|---|---|
| hong2018 | difference in attack paths | ΔAP_{i,i−1} (per-pair term of APV) | Eq. (1): ΔAP_{i,i−1} = \|AP_i − AP_{i−1}\| / \|AP_i\|. "The set of difference from the previous network state to the current one reveals the new attack paths which were not in the previous network state." | attacker-side (attack-effort framing; computed from network state) | attack paths | per consecutive state pair (analytic) | §5.1.1, Eq. (1), p. 39 |
| hong2018 | attack path variation ("Scanning: path variation") | APV | Eq. (2): APV = Σ_{i=1}^{\|S\|} ΔAP_{i,i−1} / (\|S\| − 1). "measures the shift in attack paths as the network changes when MTD techniques are deployed". "Lower APV value means the set of attack paths tends to be more static." Worked example = 0.6667. | attacker-side (Reconnaissance → Scanning) | attack paths | analytic, over state sequence S, [0, 1] | §5.1.1, Eq. (2), p. 39; worked Eq. (18), §5.3.1, p. 42 |
| hong2018 | changes in the number of attack paths | Δ\|AP\|_{i,i−1} (per-pair term of APN) | Eq. (3): 1 − (\|AP_i\| − \|AP_{i−1}\|) / \|AP_i\|. "If the number of attack paths stays the same, then it equates to value 1. But if the previous network state had no attack paths, then it equates to 0." Eq. (4), the reduced-path case with no attacker advantage: 1 − max(\|AP_i\| − \|AP_{i−1}\|, 0) / \|AP_i\|. | attacker-side | attack paths | per consecutive state pair (analytic) | §5.1.2, Eqs. (3)–(4), p. 40 |
| hong2018 | "Scanning: path number" (acronym never expanded in the text) | APN | Eq. (5): APN = Σ_{i=1}^{\|S\|} Δ\|AP\|_{i,i−1} / (\|S\| − 1). "measures the differences between the numbers of attack paths for all network states". "if the APN value tends towards zero, then the number of attack paths is increasing". Worked example = 1. | attacker-side (Reconnaissance → Scanning) | attack paths | analytic, [0, 1] | §5.1.2, Eq. (5), p. 40; worked Eq. (19), §5.3.2, p. 42 |
| hong2018 | attack path exposure ("Frequency: exposure") | APE | Eq. (6): APE = 1 − Σ_{i=0}^{\|S\|} t(ap_j) / (\|AP\| × Σ_{i=1}^{\|S\|} t(s_i)), ∀ap_j ∈ AP_i. The goal is "to compute the duration of each attack path exposed", "normalized by the number of attack paths and the total number of network states". Best case 1 − 1/\|S\|; tends to 0 if the initial paths persist across all states. Worked example = 0.5455. Note: Table 2 glosses t(ap_i) as "The time duration of an attack exploiting the attack path ap_i", but §5.1.3 uses it as path-exposure duration. | attacker-side (Reconnaissance → Frequency) | attack paths (exposure duration, a window of opportunity) | analytic, [0, 1] | §5.1.3, Eq. (6), p. 40; worked Eq. (20), §5.3.3, p. 42 |
| hong2018 | attack cost of exploitation (per state) | AC_i | Eq. (7): AC_i = 1 − Π_{j=1}^{\|AP_i\|} (1 − Π_{k=1}^{\|ap_j\|} Ep(v_k)), where v_k ∈ vuls(ap_j) ∀ap_j ∈ AP_i. The exploitability of each path is "the cumulative product of all the vulnerabilities required", and paths are combined "using the disjoint set theory". Ep is the CVSS v2 exploitability. | attacker-side | attacker effort/cost | per network state (analytic) | §5.1.4, Eq. (7), p. 40 |
| hong2018 | attack cost of exploitation ("Capability: knowledge") | ACE | Eq. (8): ACE = 1 − Σ_{i=0}^{\|S\|} AC_i / \|S\|. "computes the exploitability for the attacker to reach the target". "If vulnerabilities have high exploitability value (e.g., 1), the ACE value tends toward zero." Worked example = 0.9831. Note: the sum runs i = 0..\|S\|, but the worked example sums 4 terms over \|S\| = 4. | attacker-side (Resource → Capability) | attacker effort/cost | analytic, [0, 1] | §5.1.4, Eq. (8), p. 40; worked Eq. (21), §5.3.4, p. 43 |
| hong2018 | "Time: duration" (acronym never expanded) | ACD | Eq. (9): ACD = Σ_{i=0}^{\|S\|} [min(t(ap_j)) / max(t(ap_j))] / \|S\|, ∀ap_j ∈ AP_i. "the minimum time taken by the attacker to compromise the target in each network state … normalized by the maximum amount of time to compromise the target". §5.3.5 calls it "the ratio of the shortest and longest times taken for the attacker to exploit the target in each network state", and says "lower ACD value represents that a significant proportion of the network states can be exploited in a shorter time than the expected maximum". Worked example = 0.5848. | attacker-side (Resource → Time) | attacker time | analytic, [0, 1] | §5.1.5, Eq. (9), p. 40; worked Eq. (22), §5.3.5, p. 43 |
| hong2018 | variant assignment cost | VC_i | Eq. (10): VC_i = 1 − Σ_{j=1}^{\|H_i\|} vc(var_k, h_j) \| vh(h_j, i) ≠ vh(h_j, i−1), ∀h_j ∈ H_i, ∀var_k ∈ VAR. This is the cost of hosts whose variant changed between states. | defender-side | defence cost/overhead | per network state | §5.2.1, Eq. (10), p. 41 |
| hong2018 | normalized variant assignment cost | V̄C_i | Eq. (11): V̄C_i = 1 − Σ_{j=1}^{\|H_i\|} [vc(var_j) \| vh(h_j, i) ≠ vh(h_j, i−1)] / (\|H_i\| × max(vc(var_k))). The paper says it divides vc_i "by the maximum variant assignment cost allowed for that particular network state". | defender-side | defence cost/overhead | per network state, [0, 1] | §5.2.1, Eq. (11), p. 41 |
| hong2018 | "Resource: monetary" (acronym not expanded; §5.3.10 calls it "the cost of variant assignment cost (i.e., NVC)") | NVC | Eq. (12): NVC = 1 − Σ_{i=1}^{\|S\|} V̄C_i / (\|S\| − 1). "The total cost associated with different diversity when MTD techniques deployed for all network states". "If the NVC value is low, then the network state transitions are reassigning variants to the hosts in the network frequently". Worked example = 0.9048. | defender-side (Node → Resource) | defence cost/overhead | analytic, [0, 1] | §5.2.1, Eq. (12), p. 41; worked Eq. (23), §5.3.6, p. 43 |
| hong2018 | downtime (per state) | DT_i | Eq. (13): DT_i = 1 − max(dt(var_k, h_j) \| vh(h_j, i) ≠ vh(j_j, i−1)), ∀h_j ∈ H_i. The "j_j" typo is in the original. | defender-side | availability/QoS | per network state | §5.2.2, Eq. (13), p. 41 |
| hong2018 | "Time: downtime" (acronym not expanded; §5.3.10 calls it "the cost of variant downtime (i.e., NVDT)") | NVDT | Eq. (14): NVDT = 1 − Σ_{i=1}^{\|S\|} max(dt(var_k, h_j) \| vh(h_j, i) ≠ vh(j_j, i−1)) / ((\|S\| − 1) × max(dt(var_k, h_j))), ∀h_j ∈ H_i, ∀var_k ∈ VAR. "The downtime has been normalized by the maximum downtime experienced." A higher value means less downtime. Worked example = 0.7917. | defender-side (Node → Time) | availability/QoS | analytic, [0, 1] | §5.2.2, Eq. (14), p. 41; worked Eq. (24), §5.3.7, p. 43 |
| hong2018 | edge variation cost ("Overhead: service") | EVC | Eq. (15): EVC = 1 − Σ_{i=1}^{\|S\|} [\|ES(s_i) ⊖ ES(s_{i−1})\| / \|ES(s_i) ∪ ES(s_{i−1})\|] / (\|S\| − 1). "we define the difference between the edge set as the edge variation cost. We assume the cost of changing an edge is the same." A higher value means fewer edge changes. Worked example = 0.7949. | defender-side (Communication → Overhead) | defence cost/overhead (from configuration change) | analytic, [0, 1] | §5.2.3, Eq. (15), p. 41; worked Eq. (25), §5.3.8, p. 43 |
| hong2018 | time duration of the edge pair changes in s_i | et(s_i) | Eq. (16): et(s_i) = max(et(h_j)), ∀h_j ∈ H_i | defender-side | availability/QoS (delay) | per network state | §5.2.4, Eq. (16), p. 41 |
| hong2018 | edge variation time ("Delay: medium"; §5.3.10 calls it "edge variation downtime (i.e., EVT)") | EVT | Eq. (17): EVT = 1 − Σ_{i=1}^{\|S\|} et(s_i) / (max(et(s_i)) × (\|S\| − 1)), ∀s_i ∈ S. "normalized by the maximum amount of time taken for edge set changes". Tends to 0 when "the maximum delay for changing the edge set is observed for all network states". Worked example = 0.3333. | defender-side (Communication → Delay) | availability/QoS | analytic, [0, 1] | §5.2.4, Eq. (17), p. 41; worked Eq. (26), §5.3.9, p. 43 |
| hong2018 | compound security metrics | output_{M,W} | Eq. (27): output_{M,W} = Σ_{i=1}^{\|M\|} w_i × m_i, ∀m_i ∈ M, w_i ∈ W, with \|M\| = \|W\| and Σw_i = 1. Worked: {ACE, NVC, EVC} at 1/3 each = 0.8943 (Eq. 28); {APV, NVDT, EVT} at 1/3 each = 0.5972 (Eq. 29). Weight choice is out of scope (hospital vs. media-firm templates, p. 44). | mixed (composite) | other (weighted composite) | analytic | §5.3.10, Eq. (27), p. 43; Eqs. (28)–(29), p. 44 |
| hong2018 | "Measuring the Reconnaissance Attack Efforts subcategory using a compound security metric with APV, APN and APE" | — | Eq. (27) over {APV, APN, APE} with equal weights ("the weight distribution among selected metrics is equal", §6.2.1) | attacker-side | attack paths | analytic, swept over hosts / variants / states | Fig. 4a p. 46; Fig. 5a p. 47; Fig. 6a p. 49 |
| hong2018 | "Measuring the Resource Attack Efforts subcategory using a compound security metric with ACE and ACD" | — | Eq. (27) over {ACE, ACD}, equal weights | attacker-side | attacker effort/cost + attacker time | analytic | Fig. 4b p. 46; Fig. 5b p. 47; Fig. 6b p. 49 |
| hong2018 | "Measuring the Node Defense Efforts subcategory using a compound security metric with NVC and NVDT" | — | Eq. (27) over {NVC, NVDT}, equal weights | defender-side | defence cost/overhead + availability | analytic | Fig. 4c p. 46; Fig. 5c p. 47; Fig. 6c p. 49 |
| hong2018 | "Measuring the Communication Defense Efforts subcategory using a compound security metric with EVC and EVT" | — | Eq. (27) over {EVC, EVT}, equal weights | defender-side | defence cost/overhead + availability | analytic | Fig. 4d p. 46; Fig. 5d p. 47; Fig. 6d p. 49 |
| hong2018 | "Overall Effectiveness of MTDs taking into account both Attack and Defense Efforts" | — | Compound over attack and defence modules. The exact module set is not stated beyond the caption; weights are equal. "For the overall combination of attack and defense efforts, a metric value towards one is beneficial to the defender (i.e., attack efforts increased while defense efforts decreased)." | mixed | other (composite effectiveness) | analytic | Fig. 4e p. 46; Fig. 5e p. 47; Fig. 6e p. 49; direction §6.1.1 p. 45 (module set unverified) |
| hong2018 | "effort to security gain ratio" | — | **Named only, never defined:** "This is also apparent when we compute the effort to security gain ratio." | mixed | defence cost/overhead vs. gain | — (undefined) | §6.2.1, p. 47 |
| hong2018 | "mean attack path length" | — | **Used only to explain a result, never defined:** shuffling can "increase the ACD value, as well as the ACE by increasing the mean attack path length" | network-state | attack paths | — (undefined) | §6.2.3, p. 48 |

### 1B. hong2018 primitives and inputs (defined quantities that feed the metrics)

| paper | name as written | acronym / symbol | definition | perspective | measures | unit | locator |
|---|---|---|---|---|---|---|---|
| hong2018 | set of network states / hosts / vulnerabilities / attack paths / variants | S, H, V, AP, VAR (cardinality \|·\|) | Table 1; "\|S\| represents the cardinality of the set of network states" | network-state | attack paths (AP); configuration (S, H, V, VAR) | count | Table 1, p. 39; §5, p. 39 |
| hong2018 | "The time duration of an ith network state" | t(s_i) | Table 2 | network-state | configuration change (state dwell) | per state (time) | Table 2, p. 39 |
| hong2018 | "The time duration of an attack exploiting the attack path ap_i" | t(ap_i) | Table 2. Also used for exposure in APE and for time-to-compromise in ACD. The paper says it "can approximate the minimum time to exploit … through empirical studies (McQueen et al., 2009; Zhang et al., 2014)" (p. 40). | attacker-side | attacker time | per path | Table 2, p. 39; §5.1.5, p. 40 |
| hong2018 | "The time taken to exploit a vulnerability v_k" | t(v_k) | Table 2; Table 4 "Timetaken to exploit (h)": Linux 2, Windows 1, FreeBSD 4 | attacker-side | attacker time | per vulnerability (hours) | Table 2, p. 39; Table 4, p. 42 |
| hong2018 | "The exploitability of a vulnerability v_k using the CVSS" | Ep(v_k) | CVSS v2 exploitability sub-score. Table 4: Linux 0.15, Windows 0.2, FreeBSD 0.1. The simulation draws U[0.1, 1]. | network-state | risk/vulnerability | per vulnerability | Table 2, p. 39; §5.1.4, p. 40; Table 4, p. 42; §6.1.1, p. 45 |
| hong2018 | "The cost of assigning a variant var_k to a host h_j" | vc(var_k, h_j) | Table 2; Table 4 "Var assign. cost" = 1 per OS; the simulation uses "one unit" | defender-side | defence cost/overhead | per host-variant | Table 2, p. 39; Table 4, p. 42; §6.1.1, p. 45 |
| hong2018 | "The downtime assigning the variant var_k to the host h_j" | dt(var_k, h_j) | Table 2; Table 4 "Var assign. downtime (h)": 0.5 / 0.2 / 0.8 | defender-side | availability/QoS | per host-variant (hours) | Table 2, p. 39; Table 4, p. 42 |
| hong2018 | "The time taken to update the edge pairs of a host h_j" | et(h_j) | Table 2; "assumed to be the number of updated edges" | defender-side | availability/QoS | per host | Table 2, p. 39; §5.3.9, p. 43 |
| hong2018 | "The variant of the host h_j in the ith network state" | vh(h_j, i) | Table 2; used to detect variant change | network-state | configuration change | per host per state | Table 2, p. 39 |
| hong2018 | "The set of edges in the ith network state" | ES(s_i) | Table 2 | network-state | configuration change | per state | Table 2, p. 39 |
| hong2018 | "The set of vulnerabilities associated with an attack path ap_i" / "The set of AP at the ith network state" | vuls(ap_i) / path(s_i) | Table 2 | network-state | attack paths | per path / per state | Table 2, p. 39 |
| hong2018 | measurement units proposed for defence efforts | — | "overhead traffic load (in bytes, also in percentage)", "downtime (in seconds)", "cost (in dollars) of purchasing the OS, cost (in dollars) of required hardware" | defender-side | defence cost/overhead; availability | raw units | §5.4.2, p. 44 |

### 1C. hong2018 effort categories named but NOT turned into metrics

| category (as written) | parent | metricised? | locator |
|---|---|---|---|
| Path Variation | Attack → Reconnaissance → Scanning | yes, APV | Fig. 1, p. 36 |
| Path Number | Attack → Reconnaissance → Scanning | yes, APN | Fig. 1, p. 36 |
| Exposure | Attack → Reconnaissance → **Frequency** ("*Frequency* specifies the amount of scanning", §3.1) | yes, APE (but APE measures path-exposure duration, **not** an amount of scanning) | Fig. 1, p. 36; §3.1, pp. 35–36 |
| Cost | Attack → Reconnaissance → **Frequency** (as drawn in Fig. 1) | not as drawn: the attack cost ACE sits under "Capability: knowledge" in §5.1.4 | Fig. 1, p. 36 |
| Knowledge | Attack → Resource → Capability | yes, ACE | Fig. 1, p. 36 |
| Tools | Attack → Resource → Capability | **no** | Fig. 1, p. 36 |
| Duration | Attack → Resource → Time | yes, ACD | Fig. 1, p. 36 |
| "the probing rate" | named as an attack effort an evolving attacker raises ("if an attacker increases the number of port scanning … the attacker is increasing the attack efforts (here, the probing rate)") | **no** | §4.1, p. 36 |
| Monetary / Hardware / Software | Defence → Node → Resource | Monetary yes (NVC); Hardware and Software **no** | Fig. 2, p. 37 |
| Update / Downtime | Defence → Node → Time | Downtime yes (NVDT); Update **no** | Fig. 2, p. 37 |
| Patch / Reconfigure | Defence → Service → Maintenance | **no** | Fig. 2, p. 37 |
| Deploy / Compatibility | Defence → Service → New Service | **no** | Fig. 2, p. 37 |
| Service / Data | Defence → Communication → Overhead | Service yes (EVC); Data **no** | Fig. 2, p. 37 |
| Protocol / Medium | Defence → Communication → Delay | Medium yes (EVT); Protocol **no** | Fig. 2, p. 37 |

### 1D. Metrics hong2018 only mentions or cites (not hong2018's own; listed so nothing is cross-attributed)

| cited source (per hong2018) | metric as hong2018 writes it | locator in hong2018 |
|---|---|---|
| Evans et al. 2011 | "the probability of an attack success" | §2, p. 34 |
| Evans et al. 2011 | "the attack lifetime" (given as the rationale for APE) | §5.1.3, p. 40 |
| Zhuang et al. 2012 | "the rate of attack success" | §2, pp. 34–35 |
| Zaffarano et al. 2015 | mission metrics: "*productivity, success, confidentiality* and *integrity*" | §2, p. 35 |
| Maleki et al. 2016 | "security capacity"; "the probability of a successful attack … in relation to the attackers time and cost spent" | §2, p. 35 |
| Zhu & Başar 2013 | "qualitative damage metric" | §2, p. 35 |
| Kreidl & Frazier 2004 | "the failure cost and the maintenance cost" | §2, p. 34 |
| Pendleton et al. 2016 | "the security gained and/or the attack efforts" | §2, p. 35 |
| (generic) | "system risk", cited as an example of a boundary-less metric that cannot be normalised | §7.3, p. 50 |

---

## Paper 2: brown2023

brown2023 gives **no formula** for any metric. Both reported metrics are defined only by name, figure axis and prose. The number of trials and the aggregation across trials are not stated ("keeping the frequency of the MTD operation similar between trials", §IV, p. 5). "Per run" below is an inference from the simulation design, not a statement in the paper.

### 2A. Metrics brown2023 reports

| paper | metric name as written | acronym | definition / formula | perspective | measures | unit | locator |
|---|---|---|---|---|---|---|---|
| brown2023 | "total actions blocked". Also §IV-A heading "Attack Actions Blocked", Fig. 4 axis "No. of Actions Blocked", §V-D "the number of attack actions blocked" | — | para.: a count of the attacker actions that an MTD operation interrupted. The three blocking cases are defined in §III-D: "Connection to Host is Lost" (IP / host-topology shuffle), "Connection to Service is Lost" (service / OS diversity, port shuffle) and "User Access Has Changed" (user shuffle). No formula. | attacker-side by the paper's framing ("we measured the attack efforts", §V-D); in substance, a count of defence–attacker interdiction events | attacker effort/cost (paper's framing); equally, defence success events | per run and scenario (inferred; aggregation unstated) | §IV ¶1, p. 5; §IV-A, p. 5; Fig. 4, p. 6; §V-D, p. 7; block cases §III-D, pp. 4–5 |
| brown2023 | "average attempts required to compromise". Also §IV-B heading "Average Attempts Required to Compromise", Fig. 5 axis "No. of Attack Attempts per Compromise", §V-D "the number of attack attempts per compromise" | — | para.: the mean number of attack attempts per host compromise. No formula. Reading of results: "when the attacker is blocked, the attacker simply needs to reconnect and then exploit the same vulnerabilities" (p. 6) | attacker-side | attacker effort/cost | per compromise (averaged; run aggregation unstated) | §IV ¶1, p. 5; §IV-B, pp. 5–6; Fig. 5, p. 6; §V-D, p. 7 |

The paper's rationale for choosing only these two: "We look at these two metrics as the simplest form of metrics when considering multiple attack scenarios, as other metrics such as cost, RoA, probability of attack success, etc. depend on other external factors." (§IV, p. 5)

### 2B. brown2023 in-model quantities (defined or used, but not reported as evaluation outputs)

| paper | name as written | acronym | definition | perspective | measures | unit | locator |
|---|---|---|---|---|---|---|---|
| brown2023 | return on attack | RoA | Used as the attacker's exploit ordering: "The vulnerabilities from all the services scanned will be put into a priority stack based on their return on attack (RoA) [13]". No formula in brown2023; the definition is deferred to Alavizadeh et al. 2018 [13]. | attacker-side (decision quantity) | risk/vulnerability (value to the attacker) | per vulnerability | §III-C-2, p. 4 |
| brown2023 | attack complexity | — | "decide the difficulty of exploiting the vulnerability, randomly generated between [0.4, 1]", "derived from the CVSS" | network-state | risk/vulnerability | per vulnerability | §III-A "Vulnerability Layer", p. 3; Table I, p. 5 |
| brown2023 | impact | — | "decides the reward for compromising the vulnerability, randomly generated between [0, 1]" | network-state | risk/vulnerability | per vulnerability | §III-A, p. 3; Table I, p. 5 |
| brown2023 | "No. of atack attempts before giving up" (sic) | — | parameter = 10. "the attacker agent will move on after trying to exploit for 10 times"; in Scenario 2 the attacker never gives up on the target | attacker-side (behavioural cap, not a metric) | attacker effort/cost | per host | Table I, p. 5; §V-C, p. 7 |
| brown2023 | "time penalty" | — | "giving a time penalty whenever the attacker is blocked due to an MTD and forces them to re-scan"; magnitude not given | attacker-side (mechanism, not a metric) | attacker time | per block | §V-A, p. 7 |
| brown2023 | "Defense trigger time" | E(T) | Uniform(1000, 5000) ms, E(T) = 3000 ms (MTD interval) | defender-side (configuration, not a metric) | configuration change | per MTD event | Table I, p. 5; §IV ¶1, p. 5 |
| brown2023 | "the total number of hosts compromised" | — | **Explanatory only, not plotted:** "more attack actions are blocked against scenario 1 … because the total number of hosts compromised in scenario 2 is much smaller" | attacker-side | reach/breadth | per run (unreported) | §IV-A, p. 5 |
| brown2023 | "the number of hosts the attacker needs to compromise to reach the target node" / "the number of hosts the attacker attempts before reaching the target host" | — | **Explanatory only, not plotted** | attacker-side | reach/breadth (path to target) | per run (unreported) | §IV-B, p. 6 |

### 2C. Metrics brown2023 only mentions, cites or defers

| cited source / context | metric as written | locator |
|---|---|---|
| Alavizadeh et al. [6], [14] (Hong co-author) | "Return on Attack (RoA), Attack Cost (AC) and Risk" | §II-A, p. 1 |
| Alavizadeh et al. [13] (Hong co-author) | "RoA, AC, risk, and availability" | §II-A, p. 2 |
| Yoon et al. [15] | "a reasonable amount of overhead" | §II-A, p. 2 |
| Maleki et al. [7] | MTD "increasing the AC"; "the system considered exploited when the attacker reaches a winning state" | §II-B, p. 2 |
| game theory (generic) | "minimize risk or damage" | §II-C, p. 2 |
| deferred by the authors | "cost, RoA, probability of attack success" | §IV, p. 5 |
| discussion | "ROI"; "cost-value" analysis | §V-D, p. 7 |
| discussion (qualitative) | host shuffle is "computationally expensive" | §IV-B, p. 6 |

---

## Paper 3+: other Hong-authored papers

None are held (see Scope). alavizadeh2022 is **not Hong-authored**. zhang2023, ho2024 and tay2024 are **Hong-supervised, not Hong-authored**. hongkim2016 is **NOT HELD**, and so is hongkim2012harm.

---

## (a) Every attacker-side metric

**hong2018.** These are attacker-side by the paper's "attack efforts" framing, but all are analytic properties of a sequence of T-HARM network states. **No simulated attacker behaviour is measured.**
- ΔAP_{i,i−1} and **APV** (Eqs. 1–2)
- Δ\|AP\|_{i,i−1} (Eqs. 3–4) and **APN** (Eq. 5)
- **APE** (Eq. 6)
- AC_i (Eq. 7) and **ACE** (Eq. 8)
- **ACD** (Eq. 9)
- The Reconnaissance compound (APV + APN + APE) and the Resource compound (ACE + ACD) (Figs. 4–6 a/b)
- Attacker-side primitives: t(ap_i), t(v_k); Ep(v_k) is a network-state input used for attacker cost
- Named but unmetricised: Tools, Cost-under-Frequency, "the probing rate" (§4.1)

**brown2023.** These are the only attacker-side quantities in either paper that are measured on a running simulated attacker.
- **total actions blocked** (framed as attack effort)
- **average attempts required to compromise**
- RoA (decision quantity, not reported)
- Explanatory, unreported: total number of hosts compromised; number of hosts attempted before reaching the target

## (b) Detectability, stealth, noise, tempo, rate, intensity, dwell, or probes/scans

**Neither paper defines a metric for any of these.** The nearest items:
- **hong2018, "Frequency" category.** "*Frequency* specifies the amount of scanning" (§3.1, pp. 35–36, Fig. 1). This is the only named slot for scan volume. The one metric filed under it, APE, measures attack-path exposure duration, not scanning.
- **hong2018, "the probing rate".** Named as the attack effort an evolving attacker raises against IP shuffling (§4.1, p. 36). It is a rate in the tempo/intensity sense, and it is not metricised.
- **hong2018, ACD's rationale is detection.** "the longer the attack takes, the more likely it will be detected. Hence, increasing the amount of time to attack can negatively affect the attacker" (§5.1.5, p. 40). The metric itself is a min/max time ratio with no detection model.
- **hong2018, APE as an exposure window.** It is tempo-adjacent (how long a path stays open) and draws on Evans's "attack lifetime" (§5.1.3, p. 40).
- **hong2018, t(s_i).** A network-state dwell time, the time a configuration persists (Table 2, p. 39). It is an input, not a metric.
- **brown2023.** Scans exist as procedure steps (host discovery, port scans, re-scans forced after a block, §III-C-2, §III-D, §V-A), but nothing counts them. The block time penalty (§V-A, p. 7) and the MTD trigger interval (Table I) are mechanisms or configuration, not metrics. Stealth is absent: `extractions/brown2023.md` scores the attacker "Stealth: NONE".

## (c) Actions, attempts or effort per compromise

- **brown2023, "average attempts required to compromise" / "No. of Attack Attempts per Compromise".** This is the one direct hit (§IV-B, Fig. 5, p. 6).
- **brown2023, "total actions blocked".** A count of actions, but only blocked ones and not normalised per compromise (§IV-A, Fig. 4).
- **brown2023, give-up cap.** 10 attempts per host (Table I; §V-C). This is a parameter, not a metric.
- **hong2018, ACE / AC_i.** Effort as the difficulty of exploitation (products of CVSS exploitability along paths). It is analytic and is not a count of actions or attempts.
- **hong2018, ACD.** Effort as time, not as actions.
- **hong2018, "Tools" and "Knowledge" categories** (Fig. 1). Only Knowledge is metricised, via ACE.

## (d) How far the attacker gets (hosts, paths, proportion compromised)

- **hong2018.** Nothing measures attacker progress or hosts compromised. The path-set metrics APV and APN (and AP, \|AP\|) measure the attack paths **available** in each network state, which is reach potential, not reach achieved. The threat model states that a broken privilege chain returns the attacker "to the last reachable host in the chain" (§6.1.2, p. 45), but no metric counts it. "Mean attack path length" is used explanatorily only (§6.2.3, p. 48).
- **brown2023.** "The total number of hosts compromised" (§IV-A, p. 5) and "the number of hosts the attacker attempts before reaching the target host" (§IV-B, p. 6) appear **only in explanatory prose, not as plotted or reported metrics**. There is no proportion-compromised metric.
- **Cited only.** Success-event metrics from others: Evans's "probability of an attack success" and Zhuang's "rate of attack success" (hong2018 p. 34); "probability of attack success", deferred in brown2023 (p. 5).

## (e) Hong-authored papers NOT HELD that look metric-rich (download list)

Where the local corpus says what metrics a paper uses, I name the citing file. Otherwise the metric-richness judgement rests on the title alone.

1. **Hong & Kim 2016**, "Assessing the effectiveness of moving target defenses using security models", IEEE TDSC 13(2):163–177. hong2018 calls it the prior work whose "existing security metrics used cannot capture and represent changes in the network" (p. 35), and it is the source of the Shuffle/Diversity/Redundancy (SDR) taxonomy (§4.3, p. 38). **Highest priority.**
2. **Alavizadeh, Hong, Jang-Jaccard, Kim 2018**, "Comprehensive security assessment of combined MTD techniques for the cloud", ACM MTD Workshop, pp. 11–20. brown2023 says it uses "RoA, AC, risk, and availability" (p. 2). It is also **the RoA source MTDSim's attacker cites** ([13], p. 4). High priority.
3. **Enoch (Yusuf), Hong, Ge, Kim**, "Composite metrics for network security analysis", arXiv:2007.03486 (2020). Cited by `herranz2023` [48] and `alavizadeh2022` [44]. Metric-rich by title.
4. **Hong & Kim 2014**, "Scalable security models for assessing effectiveness of moving target defenses", IEEE/IFIP DSN, pp. 515–526 (cited in `cho2020` [74]).
5. **Yusuf, Ge, Hong, Kim, Kim, Kim 2016**, "Security modelling and analysis of dynamic enterprise networks", IEEE CIT, pp. 249–256. This is the T-HARM origin: hong2018's Definitions 1–4 are quoted from it.
6. **Alavizadeh, Kim, Hong, Jang-Jaccard 2017**, "Effective security analysis for combinations of MTD techniques on cloud computing", ISPEC, pp. 539–548. brown2023 says it uses RoA, AC and Risk (p. 1).
7. **Alavizadeh, Hong, Jang-Jaccard, Kim 2018**, "Evaluation for combination of shuffle and diversity on MTD strategy for cloud computing", TrustCom, pp. 573–578. brown2023 says it uses RoA, AC and Risk (p. 1).
8. **Alavizadeh, Hong, Kim, Jang-Jaccard 2021**, "Evaluating the effectiveness of shuffle and redundancy MTD techniques in the cloud", *Computers & Security* 102:102091. Already on `tactic_profiles/step_d/download_list.md` l.131.
9. **Nhlabatsi, Hong, Kim, et al.**, "Threat-specific security risk evaluation in the cloud", IEEE TCC 9(2):793–806. Cited in `masud2025`. Risk metrics.
10. **Enoch, Mendonça, Hong, Ge, Kim 2022**, "An integrated security hardening optimization for dynamic networks using security and availability modeling …", *Computer Networks* 208:108864. Cited in `masud2025`.
11. **Hong & Kim 2012**, "HARMs: Hierarchical attack representation models for network security analysis", AISM/SECAU (**hongkim2012harm, NOT HELD**). Primarily a model paper; it may carry HARM-level static metrics (unverified).
12. **Hong & Kim 2013**, "Scalable security analysis in HARM using centrality measures", DSN-W (cited in `cho2020` [73] and `herranz2023` [18]); and "Performance analysis of scalable attack representation models", SEC 2013 (cited in `masud2025`).
13. **Hong, Yoon, Lim, Kim 2017**, "Optimal network reconfiguration for SDN using shuffle-based online MTD", SRDS, pp. 234–243 (cited in hong2018 and brown2023).
14. **Ge, Hong, Guttmann, Kim 2017**, "A framework for automating security analysis of the IoT", JNCA 83:12–27; and **Ge, Hong, Yusuf, Kim 2018**, "Proactive defense mechanisms for the software-defined IoT with non-patchable vulnerabilities", FGCS 78:568–582.
15. Hong & Kim, "Towards scalable security analysis using multi-layered security models" (`alavizadeh2022` [21]); Hong & Kim, "Scalable security model generation and analysis using k-importance measures" (`alavizadeh2022` [46]); Hong, Kim, Chung, Huang, "A survey on the usability and practical applications of graphical security models" (`alavizadeh2022` [47]). All three reference entries are truncated in the extracted text; venues unverified.
16. **Not cited anywhere in the local corpus; from general knowledge, so verify before chasing:** Enoch, Ge, Hong, Alzaid, Kim, "A systematic evaluation of cybersecurity metrics for dynamic networks", *Computer Networks* 144 (2018). If it exists as recalled, it is probably the single most metric-dense Hong paper for this census.
