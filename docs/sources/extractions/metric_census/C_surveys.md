# Census C — metrics in survey / framework papers

Read-only census, 2026-09-23. Sources: the source markdown under `docs/sources/` (authoritative) plus the tracked extractions where they exist. No repo file edited.

**Conventions.** One row per metric. "Primary source cited" is copied as the survey writes it (bracket numbers resolved to author/year in parentheses where I checked the survey's own reference list; unresolved numbers left bare). Perspective: A = attacker-side, D = defender-side, N = network-state. Locator: section + source-markdown line (`L123`). Pages are pinned where the markdown carries page markers (Jalowski "N of 13"; Sengupta arXiv-layout pages; Ward PDF pages; Zhuang; Zaffarano printed pp. 3–10); Cho and NITRD markdown carry no page numbers, so their pages are unverified. Where a survey only *mentions* a quantity in passing (e.g. an evaluation of a single primary paper), it is still recorded, marked "(passing)".

---

## 1. cho2020 — Cho et al., "Toward Proactive, Adaptive Defense: A Survey on MTD", IEEE COMST 22(1) 2020

Source: `docs/sources/lit_review/1_1_cho2020toward.md`. The §VII taxonomy is two-by-two: effectiveness (§VII-A) vs efficiency (§VII-B) × attacker's metrics vs defender's metrics. Figs. 6–8 (counts) and Fig. 16 are image-omitted. Pages unverified (article spans pp. 709–745; Table VI is p. 732 per the extraction).

### 1a. §VII-A Effectiveness — attacker's metrics (L574–586)

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| cho2020 | Attack success probability | ASP | "the probability that attacks are successfully performed. For example, it refers to the probability that a system component (or defender) is compromised or a target is successfully discovered or accessed by an attacker." | [3] (Al-Shaer 2012), [11] (Anderson 2016), [22] (Ben-Asher 2016), [25] (Carroll 2014), [26] (Carter 2014 arXiv), [28] (Casola 2013), [32] (Cho & Ben-Asher 2018), [45] (DeLoach 2014), [49] (Evans 2011), [136] (Rahman 2014), [147] (Sharma 2018 FRVM), [173] (Zaffarano 2015) | A | success events | §VII-A, L578; noted as dominant metric (L636) |
| cho2020 | Attackability | — | "the probability that an attacker can access system states (or components) to the attack … combines the degree of system vulnerability plus the feasibility of an attacker accesses and performs an attack based on its own resource level"; Cho folds it into ASP | Rahman et al. [136] | A | success events | §VII-A, L578 |
| cho2020 | Attack utility | — | "the payoff (or utility) of an attacker is used to measure the gain or loss by deploying a proposed MTD" (game-theoretic) | [5], [6] (Alavizadeh 2018 ×2), [22], [119] (Neti 2012), [134] (Prakash & Wellman 2015), [181] (Zhu & Başar 2013), [182] (Zhu 2012) | A | game payoff | §VII-A, L580 |
| cho2020 | Learning by attackers | — | "the degree of an attacker's learning toward the payoff obtained by a defender upon the performed attack" | [181] (Zhu & Başar 2013) | A | other (adaptation/learning) | §VII-A, L582 |
| cho2020 | Mean time to compromise a system | MTTC | "how long an attacker takes to compromise an entire system"; defender-side counterpart is MTTF | [4] (Alavizadeh 2017), [26], [27] (Carter 2014 ×2), [32] (Cho & Ben-Asher 2018), [186] (Zhuang 2014) | A | attacker time | §VII-A, L584–585 |
| cho2020 | Unpredictability | — | "how much confusion or uncertainty a given MTD has introduced to attackers" | [66] (Green 2015), [110] (MacFarland & Shue 2015), [145] (Shan 2015) | A (effect on attacker) | other (uncertainty) | §VII-A, L587 |
| cho2020 | Attack surface | — | "the amount of system resources that can be used by attackers to attack the system, such as channels, data items, or methods" | [112], [114] (Manadhata & Wing 2011 ×2) | A (listed under attacker's metrics) / N | risk/vulnerability | §VII-A, L589 |

### 1b. §VII-A Effectiveness — defender's metrics (L591–629)

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| cho2020 | Defense success probability | DSP | umbrella: "metrics measuring the success of an MTD technique"; includes Zaffarano's rate of successful defences/attacks, Colbaugh & Glass's detection accuracy, Clark's decoy-detected portion, Al-Shaer's IP-mutation success probability | [3], [35] (Clark 2013), [38] (Colbaugh & Glass 2012), [173] (Zaffarano 2015) | D | success events | §VII-A, L593 |
| cho2020 | rate of executing successful defenses / attacks (inside DSP) | — | "for a defender, the rate at which tasks are executed and completed … for an attacker, the rate at which attacks are performed and successfully completed" | Zaffarano et al. [173] | D and A | success events (rate) | §VII-A, L593 |
| cho2020 | detection accuracy of anomaly behaviors (inside DSP) | — | used "to determine whether to trigger an MTD operation" | Colbaugh and Glass [38] | D | stealth/detection | §VII-A, L593 |
| cho2020 | portion of decoy nodes detected by attackers (inside DSP) | — | measures success of IP-shuffling MTD | Clark et al. [35] | D (measured on attacker action) | success events / other (deception) | §VII-A, L593 |
| cho2020 | IP-mutation success probability (inside DSP) | — | "the probability that a mutated IP is not hit by scanning attacks" | Al-Shaer et al. [3] | D | success events | §VII-A, L593 |
| cho2020 | Mean time to failure | MTTF | "a system reliability metric capturing the system's up-time in the presence of attacks …"; "the same as MTTC" | [26], [27], [32], [186] | D | attacker time (mirror) / availability | §VII-A, L595 |
| cho2020 | Defense utility | — | payoff (utility) of the defender | [22], [119], [134], [181], [182] | D | game payoff | §VII-A, L597 |
| cho2020 | Learning by defenders | — | "the degree of a defender's learning toward the payoff an attacker has obtained upon a defense action" | [181] | D | other (learning) | §VII-A, L599 |
| cho2020 | System security → Confidentiality | — | "how many system components are compromised [134]"; also degree of preserving confidential info | [134] (Prakash & Wellman 2015), [173], [177] (Zhang 2012) | D / N | reach/breadth (component count) | §VII-A, L603 |
| cho2020 | Mission confidentiality | — | "the degree of exposing confidential information to unauthorized parties" | [173] (Zaffarano 2015) | D | risk/vulnerability | §VII-A, L603–605 |
| cho2020 | Attack confidentiality | — | "the degree of attack behaviors detected by a defender" | [173] (Zaffarano 2015) | A | stealth/detection | §VII-A, L605 |
| cho2020 | Integrity → Mission integrity | — | "how much information related to executing a given mission is communicated without being modified or forged" | [173] | D | other (mission info) | §VII-A, L607 |
| cho2020 | Attack integrity | — | "how much accurate information the attacker's view" | [173] | A | other (attacker knowledge) | §VII-A, L607 |
| cho2020 | Availability | — | "the portion of system assets that are not compromised to provide a normal service" | [66], [134] | N | availability/QoS (inverse reach) | §VII-A, L609 |
| cho2020 | Degree of vulnerability | — | "the probability that a given platform to be selected is vulnerable during a particular time period or a given system component is vulnerable because it is controlled by an attacker" | [4], [5], [6], [22], [25], [26], [27], [181] | N | risk/vulnerability | §VII-A, L611 |
| cho2020 | Controllability | — | "the portion of critical system assets that expose a high vulnerability to an attacker if compromised" | [134] | N | risk/vulnerability | §VII-A "Other metrics", L615 |
| cho2020 | Worm propagation speed | — | "how much a deployed MTD can slow down actions by an attacker"; "indirectly increases the detection of attackers by earning more time to monitor" | [3], [86], [87] (Jafarian 2015, 2012) | A | attacker time / tempo | §VII-A, L617 |
| cho2020 | Vastness | — | "the size of spaces that a given defense mechanism can cover, such as IP spaces an attacker needs to scan through"; number of target hosts consumes attacker resource | [66], [110], [114], [177] | D (config) / A effort | configuration change / attacker effort | §VII-A, L619 |
| cho2020 | Periodicity | — | "how often system configurations change in order to provide a level of confusion to attackers" | [66], [110] | D | configuration change | §VII-A, L621 |
| cho2020 | Uniqueness | — | "how uniquely an individual entity (e.g., a host) is authorized to a system without being accessed by other entities" | [66], [110] | D | configuration change | §VII-A, L623 |
| cho2020 | Revocability | — | "the degree of frequency to terminate or expire a prior system configuration" | [66], [110] | D | configuration change | §VII-A, L625 |
| cho2020 | Distinguishability | — | "how well a given defense distinguishes trustworthy entities from non-trustworthy entities" | [66], [110] | D | stealth/detection | §VII-A, L627 |
| cho2020 | Loss in rewards between an optimal deployment and an executed deployment | — | "how much loss occurred for the actual execution of an MTD operation over the optimal deployment" | [141] (Sengupta 2017) | D | game payoff | §VII-A, L629 |

### 1c. §VII-B Efficiency (L638–677)

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| cho2020 | Penalty in attack payoff | — | "attack cost at an abstract level (e.g., cost is 1 for attacking; 0 otherwise)" | [52] (Feng 2017), [91] (Jia 2013 MOTAG), [168] (Wright 2016), [177] | A | attacker effort/cost (game payoff) | §VII-B, L642 |
| cho2020 | Attack cost | — | "how much overhead or impact is introduced to attackers to perform their attacks"; Nmap scanning overhead [93] | [5], [6], [93] (Kampanakis 2014), [113] (Manadhata 2013), [147] | A | attacker effort/cost | §VII-B, L644 |
| cho2020 | scanning overhead (inside Attack cost) | — | captured with Nmap | [93] | A | attacker effort/cost (probes) | §VII-B, L644 |
| cho2020 | Quality-of-Service (QoS) to users | QoS | "degree of service quality provided to users while implementing a given MTD" | [35], [68] (Han 2014), [168] | D | availability/QoS | §VII-B, L650 |
| cho2020 | number of connections interrupted (inside QoS) | — | "upon deploying IP mutation techniques" | [35] | D | availability/QoS | §VII-B, L650 |
| cho2020 | System performance | — | "how much overhead is introduced to deploy a given MTD" | [9], [33], [36], [48], [54], [68], [85], [105], [118], [132], [163], [164], [176] | D | defence cost/overhead | §VII-B, L656 |
| cho2020 | message overhead (delay, packet loss, control packet overhead) | — | sub-item of system performance | [48], [176] | D | defence cost/overhead | §VII-B, L656 |
| cho2020 | operational delay / cost to deploy an MTD | — | sub-item | [118], [176] / [54], [68], [163], [164], [176] | D | defence cost/overhead | §VII-B, L656 |
| cho2020 | number of dropped connections | — | sub-item | [36] | D | availability/QoS | §VII-B, L656 |
| cho2020 | performance overhead (file sizes, degradation to distribute software) | — | sub-item | [85] | D | defence cost/overhead | §VII-B, L656 |
| cho2020 | system throughput (network throughput; server throughput) | — | "how many messages are correctly delivered" / "how many queries are properly provided" | [9], [176] / [132] | D | availability/QoS | §VII-B, L656 |
| cho2020 | Defense cost (abstract: migration / maintenance cost of VMs) | — | "abstract level of defense cost … mostly used in game theoretic MTD" | [32], [52], [91], [168], [177] | D | defence cost/overhead | §VII-B, L658 |
| cho2020 | level of infrastructure (number of proxy or decoy nodes) | — | required to ensure service availability | [91], [168] | D | defence cost/overhead | §VII-B, L658 |
| cho2020 | Address space overhead | — | "the required address space based on mutation speed (e.g., … LFM, … HFM)" | [3] | D | defence cost/overhead | §VII-B, L660 |
| cho2020 | Flow table size | — | size of OpenFlow flow table under OF-RHM | [86], [87], [176] | D | defence cost/overhead | §VII-B, L662 |
| cho2020 | Integrated performance cost | — | integrates performance and security cost; Ge: bandwidth cost + risk at servers; Clark: number of active sessions + fraction of decoy nodes scanned | [36], [54] | D | defence cost/overhead | §VII-B, L664–670 |
| cho2020 | fraction of decoy nodes scanned by attackers (inside integrated cost) | — | component of Clark's cost function | Clark et al. [36] | A | other (deception) / probes | §VII-B, L664 |
| cho2020 | Strategy switching cost | — | "switching cost (e.g., migration cost)"; web-stack configuration switching | [141] | D | defence cost/overhead | §VII-B, L671 |
| cho2020 | Power consumption | — | energy consumption vs benefit in WSN/IoT | [175] (Zeitz 2018) | D | defence cost/overhead | §VII-B, L673 |

### 1d. Metrics named elsewhere in Cho (outside §VII)

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| cho2020 | Mean time to security failure | MTTSF | "the security failure is defined by the system state being compromised by an attacker" (Okhravi); "(i.e., system lifetime)" (Cho & Ben-Asher) | Okhravi et al. [124]; Cho and Ben-Asher [32]; also Ge et al. [57] | D | attacker time (mirror) | §VIII-A-1, L687, L691; §VI-B L523 |
| cho2020 | System Risk | Risk | named only | Alavizadeh et al. [4], [5], [6] | N | risk/vulnerability | §IV-D, L346, L348, L351 |
| cho2020 | Reliability | R | named only | Alavizadeh et al. [4] | D | availability/QoS | §IV-D-2, L346 |
| cho2020 | Attack Cost | AC | "an appropriate MTD technique should decrease Risk and RoA while increasing AC" | Alavizadeh et al. [6], [5] | A | attacker effort/cost | §IV-D-3, L348; L351 |
| cho2020 | Return on Attack | RoA | should be decreased by MTD | Alavizadeh et al. [6], [5] | A | game payoff / risk | §IV-D-3, L348; L351 |
| cho2020 | system availability | SA | named only | Alavizadeh et al. [5] | D | availability/QoS | §IV-D-4, L351 |
| cho2020 | "eight security metrics … based on different perspectives, such as attackers and defenders" | — | not enumerated by Cho | Alavizadeh et al. [8] | A+D | other | §IV-D-3, L348 |
| cho2020 | number of attack paths towards the decoy targets | — | GA fitness metric | Ge et al. [57] | N | attack paths | §VI-B, L523 |
| cho2020 | defense cost (GA fitness) | — | — | Ge et al. [57] | D | defence cost/overhead | §VI-B, L523 |
| cho2020 | attackers' overhead | — | "evaluating the performance in terms of the attackers' overhead increased by the MTD" | Kampanakis et al. [93] | A | attacker effort/cost | §IV-A-1, L288 |
| cho2020 | resistance toward brute-force attacks; proxy-based and communication-based overhead | — | (passing) | Jia et al. [91] | A / D | success events / defence cost | §IV-A-5, L299 |
| cho2020 | time it takes to switch VMs | — | (passing) | Penner and Guirguis [130] | D | defence cost/overhead | §IV-A-5, L299 |
| cho2020 | rotation window | — | "the duration of an OS being exposed and vulnerable to an attack" | Thompson et al. [157] | N | attacker time / configuration change | §IV-A-8, L307 |
| cho2020 | system dependability: availability, reliability, service response time | — | (passing) | Gorbenko et al. [65] | D | availability/QoS | §IV-D-1, L344 |
| cho2020 | attack resilience (GA ranking of configurations) | — | (passing) | Crouse and Fulp [40] | N | risk/vulnerability | §VI-B, L518 |
| cho2020 | probability of attack success / accuracy / utility (NetHide) | — | "mitigate the probability of attack success by 1% while it provides 90% and 72% accuracy and utility" | Meier et al. [115] | A / D | success events / availability | §V-C, L431 |
| cho2020 | fingerprinter attack success probability | — | (passing) | Rahman et al. [135] | A | success events | §II-C-1, L191 |
| cho2020 | attacker's workload | — | the effectiveness criterion of Farris & Cybenko's expert survey ("limited to the attacker's workload") | Farris and Cybenko [51] | A | attacker effort/cost | §I-B, L73 |
| cho2020 | success rate; overhead (storage cost, end-to-end (ETE) delay) | ETE | (passing, emulation) | Aydeger et al. [16] | A / D | success events / defence cost | §VIII-C, L710 |
| cho2020 | time-to-first-byte; total download time | — | (passing) | Skowyra et al. [152] | D | availability/QoS | §VIII-C, L710 |
| cho2020 | system downtime | — | (passing) | Alavizadeh et al. [7] | D | availability/QoS | §VIII-D-2, L727 |
| cho2020 | migration downtime; network traffic | — | (passing) | Penner and Guirguis [130] | D | defence cost/overhead | §VIII-D-2, L727 |
| cho2020 | page loading time overhead | — | (passing) | Vikram et al. [163] | D | defence cost/overhead | §VI-C, L529 |
| cho2020 | attack effort and complexity | — | "MTD systems … increase attack effort and complexity" | Bardas et al. [20] | A | attacker effort/cost | §IX-E, L827 |
| cho2020 | success rates in reduction of Trojan attacks; power consumption rates | — | (passing) | Zhang et al. [178] | A / D | success events / defence cost | §IX-C, L796 |
| cho2020 | detection capabilities vs associated costs | — | trade-off via OPF | Lakshminarayana and Yau [100] | D | stealth/detection | §IX-C, L796 |
| cho2020 | throughput and delay | — | (passing) | Ulrich et al. [159] | D | availability/QoS | §IX-C, L789 |
| cho2020 | packet-loss ratio (during hand-off delay) | — | "zero packet-loss ratio" | Heydari [71] | D | availability/QoS | §IX-C, L789 |
| cho2020 | packet loss and latency | — | (passing) | Groat et al. [67] | D | availability/QoS | §IX-C, L789 |
| cho2020 | accessibility, knowledge and existing security | — | performance axes of power-grid MTD | Rahman et al. [136] | A / N | other | §IX-C, L789 |
| cho2020 | information entropy (of CAN IDs) | — | (passing) | Wu et al. [169] | D | configuration change (unpredictability) | §IX-F, L858, L865 |
| cho2020 | service availability of ECU nodes | — | (passing) | Yoon et al. [170] | D | availability/QoS | §IX-F, L865 |
| cho2020 | channel security; confusion factor; intercept probability | — | (passing) | Ghourab et al. [63] | D / A | other / success events | §IX-F, L865 |
| cho2020 | mean time to compromise (cloud platform migration) | MTTC | (passing) | Carter et al. [26], [27] | A | attacker time | §IX-E, L835/L844 |
| cho2020 | Security / performability / economical cost metrics | — | three-metric family proposal: security = effectiveness; performability = efficiency; economical (operational, capital) cost | Cho et al. (own proposal, Fig. 16) | D | other (framework) | §IX lim. L873; §XI-B L928 |

**Parameters (not metrics) Cho names that bear on the priority list:** number of addresses scanned by attackers (Carroll [25], L288, L691); number of probes (Luo [108], L290); number of attacker bots (Wright [168], L481); frequency of shuffling (several). These are *inputs* against which ASP is plotted, not outputs.

---

## 2. jalowski2026 — Jalowski et al., "Rethinking the Security Assurances of MTD: A Gap Analysis for Network Defense", Future Internet 18(2):89, 2026

Source: `docs/sources/lit_review/3_1_jalowski2026rethinking.md` (page markers "N of 13" present, so pages are pinned). Jalowski defines no new metric; §2.3 relays two survey groupings (Sengupta [5], Cho [6]); §3.1 names further primary metric sets; §5 critiques ASP and states four criteria for a useful metric.

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| jalowski2026 | Qualitative Metrics — Security of individual defenses | — | "model security of each individual component of the system" | Survey [5] (Sengupta et al. 2020) | D | other (qualitative) | §2.3, p. 4, L81 |
| jalowski2026 | Qualitative Metrics — Security of the ensemble | — | "looks at a system as a whole" | [5] | D | other (qualitative) | §2.3, p. 4, L83 |
| jalowski2026 | Confidentiality, Integrity, Availability (CIA) Metrics | CIA | "used to measure the impact on the system during an attack" | [5] | N | availability/QoS / risk | §2.3, p. 4, L89 |
| jalowski2026 | Risk Metrics | — | "consider risk associated with deploying the MTD technique" | [5] | N | risk/vulnerability | §2.3, p. 4, L91 |
| jalowski2026 | Attack graph/tree | — | "represents possible attack paths in a system" | [5] | N | attack paths | §2.3, p. 4, L93 |
| jalowski2026 | Policy Conflict Analysis | — | "shows how different MTD countermeasures can cause security policy violations" | [5] | D | defence cost/overhead (policy) | §2.3, p. 4, L95 |
| jalowski2026 | Attack Success Probability / Defense Success Probability | ASP | "the chance for an attack to succeed and for a defense to protect against it" | Survey [6] (Cho et al. 2020) | A / D | success events | §2.3, p. 4, L99; abbreviation list L243 |
| jalowski2026 | Attack Utility / Defense Utility | — | "measure the gain or loss for each side by applying the MTD technique" | [6] | A / D | game payoff | §2.3, p. 4, L101 |
| jalowski2026 | Mean time to compromise a system, or mean time to failure | — (no acronym given) | "how long it takes to compromise the system or indicates its up time in the presence of attacks" | [6] | A / D | attacker time | §2.3, p. 5, L107 |
| jalowski2026 | Learning by attackers/defenders | — | "the degree of learning by each side after each undertaken action" | [6] | A / D | other (learning) | §2.3, p. 5, L109 |
| jalowski2026 | Attack surface | — | "the amount of system resources that an attacker can use"; defined also at §2.2 as "the set of resources in a system that can be targeted for attack" | [6]; §2.2 cites [12] (Manadhata & Wing 2011) | N | risk/vulnerability | §2.2 p. 3 L63; §2.3 p. 5 L111 |
| jalowski2026 | System security (CIA, degree of vulnerability) | — | "security properties enhanced by MTD, in terms of CIA and 'degree of vulnerability,' which is the probability that a platform selected by the attacker is vulnerable" | [6] | N | risk/vulnerability | §2.3, p. 5, L111 |
| jalowski2026 | Attack/defense cost | — | "efficiency of the MTD scheme in either causing overhead for an attacker or increasing costs for the defender in terms of network parameters like flow table size, address space overhead, increased power consumption, or others" | [6] | A / D | attacker effort/cost; defence cost/overhead | §2.3, p. 5, L113 |
| jalowski2026 | new set of metrics for network topology shuffle and software diversity (not enumerated) | — | "a new set of metrics for evaluating MTD security" | [13] (Hong et al. 2018, "Dynamic Security Metrics …") | N | other | §3.1, p. 5, L125 |
| jalowski2026 | security metrics for SDN (not enumerated) | — | — | [14] (Sharma et al. 2020, "Dynamic Security Metrics for SDN-based MTD") | N | other | §3.1, p. 5, L125 |
| jalowski2026 | entropy parameters: vulnerability, attack, attenuation | — | "quantify MTD techniques using entropy parameters such as vulnerability, attack, and attenuation" | [15] (Ma et al. 2017) | N | configuration change / risk | §3.1, p. 5, L125 |
| jalowski2026 | risk and attack costs (SDR-based cloud model) | — | "analyze risk and attack costs" | [16] (Hong & Kim 2015); [17]–[20] (Alavizadeh 2018, 2019, 2020, 2022) | N / A | risk/vulnerability; attacker effort/cost | §3.1, p. 5, L125 |
| jalowski2026 | availability, reliability, and security trade-offs (cloud) | — | (passing) | [28] (Torquato & Vieira 2019), [29] (Alavizadeh 2020) | D | availability/QoS | §3.3, p. 6, L143 |
| jalowski2026 | Quality of Service | QoS | MTD "may exacerbate … QoS challenges for delay-sensitive protocols like VoIP" | [49] (Karakus & Durresi 2017) | D | availability/QoS | §4.2, p. 8, L187; abbreviation list L243 |
| jalowski2026 | mutation frequency (per zone) as an attacker-observable signal | — | "assigning higher mutation frequencies to critical 'Red Zones' inadvertently signals asset value"; attacker uses "traffic analysis to identify which segments are mutating fastest" | own analysis; hybrid host-specific timing from [34] (Gudla & Sung 2020) | D (config) observed by A | configuration change / stealth/detection (defender leakage) | §4.1, p. 7, L163; Fig. 2 |
| jalowski2026 | probability that another node resides in the same (compromised) state — "state collision" | — | "If an attacker compromises one state, the probability that another node resides in that same state is high" | own analysis | A / N | reach/breadth | §4.1, p. 6, L153 |
| jalowski2026 | ASP (critique) | ASP | "may be too naive, as it can only describe effectiveness against one, often very specific, attack … commonly calculated using simple Nmap scans [52] as a baseline" | [52] (Nmap) as the criticised baseline | A | success events | §5, p. 9, L209 |
| jalowski2026 | Criteria for a useful metric (meta, not a metric) | — | (i) easy to establish from simulation and normal runtime data; (ii) generic across schemes; (iii) baseline = "a state-of-the-art system, protected using the best available methods"; (iv) common security mechanisms and terminology | own proposal | — | other (meta) | §5, p. 9, L211–217 |

Notes: Jalowski's §2.3 renders Cho's list *without* acronyms other than ASP (MTTC/MTTF spelled out). Passive reconnaissance vs active Nmap scanning (§4.3, p. 8, L197) is a threat-model claim, not a metric. No detection/stealth metric is proposed, but the "Red Zones" beacon (L163) is the one place detectability runs defender→attacker.

---

## 3. sengupta2020 — Sengupta, Chowdhary, Sabur, Alshamrani, Huang, Kambhampati, "A Survey of Moving Target Defenses for Network Security", IEEE COMST 22(3) 2020 (arXiv 1905.00964 layout)

Source: `docs/sources/methodology/sengupta2020_survey.md` (PDF-text extraction with `=== page N ===` markers, so pages are pinned to the arXiv layout, not the journal pagination). §V's structure: **A. Qualitative** (security vs performance × individual defence vs ensemble; Fig. 12) and **B. Quantitative** (Fig. 13: *Security Metrics* = CIA, Risk, Attack Graph/Tree, Policy Conflict Analysis; *Usability Metrics* = QoS, Cost). Bracket numbers resolved from Sengupta's own reference list.

### 3a. §V-A Qualitative metrics (pp. 21–24)

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| sengupta2020 | Security of Individual Defenses | — | security of each constituent configuration, mostly via defender utility built from CVSS | [60] Lei 2017, [77] Sengupta 2017 IDS, [58] Jajodia 2018, [92], [65] Carter 2014, [151] Rass 2017, [79] (+ Fig. 12 list: [63], [73], [67], [133], [105], [68], [56], [150], [74], [64], [69], [76]) | D | risk/vulnerability | §V-A-1a, p. 21, L2581–2627; Fig. 12 p. 22 |
| sengupta2020 | security of a configuration ∝ 1 / probability the adversary can come up with a new attack given earlier attacks | — | "inversely proportional to the probability with which an adversary can come up with a new attack given the attacks it performed in the earlier time steps" | [65] Carter et al. 2014 | A | success events | §V-A-1a, p. 21, L2594–2598 |
| sengupta2020 | expert-annotated effectiveness vs zero-day | — | experts annotate how effective a countermeasure is against zero-days | [151] Rass et al. 2017 | D | other | §V-A-1a, p. 21, L2598–2604 |
| sengupta2020 | penalty imposed on an attacker (DDoS, repeated game) | — | each defence action "weighed based on the penalty it imposes on an attacker" | [73] Chowdhary et al. (dynamic game SDN cloud) | A | attacker effort/cost | §V-A-1a, p. 21, L2611–2614 |
| sengupta2020 | security risk of the present vulnerable state | — | reasoning to migrate VM or not | [67] El Mir et al. | N | risk/vulnerability | §V-A-1a, p. 21, L2614–2616 |
| sengupta2020 | reputation of the current state | — | "looks at the type and number of attacks that were done in previous time steps" | [68] Debroy et al. 2016 | N | risk/vulnerability | §V-A-1a, p. 21, L2616–2620 |
| sengupta2020 | fingerprint of the overall network | — | epistemic effect of a defence action | [56] Zhao et al. 2017 | A (knowledge) | other (attacker knowledge) | §V-A-1a, p. 22, L2669 |
| sengupta2020 | topology information a defence action leaks to an attacker | — | — | [150] Meier et al. 2018 (NetHide) | A (knowledge) | other (attacker knowledge) | §V-A-1a, p. 22, L2670–2672 |
| sengupta2020 | security risk ∝ 1 / attacker cost to compromise | — | "inversely proportional to the cost (it believes) an attacker would spend to compromising it" | [133] Kampanakis et al. 2014 | A | attacker effort/cost | §V-A-1a, p. 22, L2672–2675 |
| sengupta2020 | Security of the Ensemble (vs static configuration as control) | — | compares MTD ensemble with a static configuration; warns the static control is not guaranteed to be the most secure constituent | [86] Shi 2017 CHAOS, [54] Jafarian 2012, [55] Aydeger 2016, [66] Thompson 2014, [145] Zhuang 2013 | D | other (baseline) | §V-A-1b, p. 22, L2676–2685 |
| sengupta2020 | entropy / diversity of the ensemble | — | "metrics that are similar to entropy or diversity of the ensemble" | [137] Dunlop 2011 MT6D; [124] Ahmed & Bhargava 2016 Mayflies | D | configuration change (unpredictability) | §V-A-1b, p. 22, L2686–2697 |
| sengupta2020 | topological distance measure | — | "the symmetric difference between the edge sets of the current and the consecutive defense configuration" | [110] Hong et al. 2017 | D | configuration change | §V-A-1b, p. 22, L2697–2703 |
| sengupta2020 | diversity metric (software / configuration pool) | — | compiler-level diversity; GA pool maximising diversity | [114] Homescu et al.; [71] Crouse et al. 2012 | D | configuration change | §V-A-1b, p. 22, L2704–2720 |
| sengupta2020 | differential immunity | — | an MTD whose constituent configurations "are all vulnerable to the same attack, can never be secure" | own heuristic; DNN ensemble [80] | D | configuration change / risk | §V-A intro, p. 21, L2555–2558; L1112 |
| sengupta2020 | attack surface features / attack surface measurements; utility for attack surface shifting | — | individual vs ensemble utility | [62] Manadhata 2013 | N / D | risk/vulnerability; game payoff | §V-A-1c, p. 22, L2723–2729 |
| sengupta2020 | number of interruptions for an attacker to reach a goal node from a start point | — | "increase the number of interruptions for an attacker to start from one point in the network and reach a goal node" | [147] Bardas et al. 2017 (MTD CBITS) | A | attack paths / attacker effort | §V-A-1c, p. 23, L2733–2737 |
| sengupta2020 | coverage of attacker-goal leaves by the defence set | — | "covering each of the leaves that an attacker might want to reach" | [95] Miehling et al. | D | attack paths | §V-A-1c, p. 23, L2738–2742 |
| sengupta2020 | overlapping vulnerabilities between configurations | — | diverse ensemble = configurations with few overlapping vulnerabilities | [70] Neti et al. 2012 | N | risk/vulnerability | §V-A-1c, p. 23, L2745–2748 |
| sengupta2020 | lines of code differing between two OSs (diversity) | — | — | [65] Carter et al. 2014 | D | configuration change | §V-A-1c, p. 23, L2748–2750 |
| sengupta2020 | Performance of Individual Defenses | — | performance cost of each constituent configuration, mostly in defender utility | [60], [76], [77], [79], [96] | D | defence cost/overhead | §V-A-2a, p. 23, L2776–2790 |
| sengupta2020 | Performance of the Ensemble — shuffling costs: (1) downtime, (2) legitimate in-flight requests, (3) keeping ≥2 configurations running | — | "All these costs can be termed as shuffling costs" | own categorisation | D | defence cost/overhead | §V-A-2, p. 23, L2760–2768 |
| sengupta2020 | latency impact of NIDS placement (centrality-based heuristics) | — | — | [76], [77] | D | availability/QoS | §V-A-2a, p. 23, L2787–2790 |
| sengupta2020 | average time for packet transfer | — | increases under random path selection | [55] Aydeger 2016 | D | availability/QoS | §V-A-2a, p. 23, L2821–2825 |
| sengupta2020 | performance cost of defend action on legitimate traffic | — | — | [56] | D | availability/QoS | §V-A-2a, p. 23, L2825–2827 |
| sengupta2020 | number and quality of resources ("honey") for a credible honeynet | — | — | [58] Jajodia 2018 | D | defence cost/overhead | §V-A-2a, p. 23, L2833–2837 |
| sengupta2020 | one-step cost of switching between defence actions | — | — | [63] Zhu & Başar 2013; [64] Sengupta 2017 | D | defence cost/overhead | §V-A-2b, p. 23, L2846–2848 |
| sengupta2020 | IPv6 header overhead (40 bytes); latency during address change (12 ms vs 3 ms) | — | — | [137] Dunlop 2011 | D | defence cost/overhead | §V-A-2b, p. 23–24, L2852–2858 |
| sengupta2020 | file-system replica creation time (+2 min) | — | — | [124] Mayflies | D | defence cost/overhead | §V-A-2b, p. 24, L2859–2862 |
| sengupta2020 | number of HTTP error packets on the wire | — | — | [147] Bardas 2017 | D | availability/QoS | §V-A-2b, p. 24, L2862–2867 |
| sengupta2020 | end-to-end (ETE) packet delivery time; number of collisions | ETE | — | [59] Algin et al. | D | availability/QoS | §V-A-2b, p. 24, L2872–2878 |
| sengupta2020 | number of servers controlled by the defender (FlipIt state) | — | "an indirect way of measuring system performance" | [69] Prakash & Wellman 2015 | D / N | reach/breadth (inverse) | §V-A-2c, p. 24, L2886–2891 |
| sengupta2020 | availability over a bounded horizon; downtime / unavailability during migration | — | — | [67] El Mir | D | availability/QoS | §V-A-2c, p. 24, L2891–2895 |
| sengupta2020 | host capacity and network bandwidth per configuration | — | — | [68] Debroy 2016 | D | defence cost/overhead | §V-A-2c, p. 24, L2895–2899 |
| sengupta2020 | cost of ensuring same performance across configurations; cost of an ensemble-capable system | — | — | [112]; [74] Clark 2015 | D | defence cost/overhead | §V-A-2c, p. 24, L2899–2908 |

### 3b. §V-B Quantitative metrics (pp. 24–26)

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| sengupta2020 | (framing) "shuffling x % number of hosts leads to y % reduction in attack success probability, and z % increase in overhead/quality of service (QoS)" | — | illustrates a quantitative claim | — | A / D | success events; availability/QoS | §V-B, p. 24, L2940–2943 |
| sengupta2020 | CIA Metrics | CIA | "used as quantitative metrics for measurement of impact on system under attack" | Fig. 13: [131] Zaffarano 2015, [51] Chowdhary 2016, [118] Connell 2017, [89] MASON, [66] MORE, [71] Crouse | N | risk/vulnerability | §V-B-1, p. 24–25, L2970–2974; Fig. 13 L2793 |
| sengupta2020 | mission confidentiality valuation | Conf(M, v) | "Conf(M, v) = 1/\|T\| Σ_{t∈T} (t, unexposed)" | Zaffarano et al. [131] | D | other (mission info) | §V-B-1, p. 25, L2974–2980 |
| sengupta2020 | mission integrity valuation | Int(M, v) | "Int(M, v) = 1/\|T\| Σ_{t∈T} (t, intact)" | Zaffarano et al. [131] | D | other (mission info) | §V-B-1, p. 25, L2981–2986 |
| sengupta2020 | availability (with system reconfiguration rate α, CTMC) | α | "system reconfiguration rate α is modeled as a function of system resources" | Connell et al. [118] | D | availability/QoS; configuration change | §V-B-1, p. 25, L2990–2994 |
| sengupta2020 | threat score (PageRank-based, IDS alerts + CVSS) | — | port hopping 40–50 % of services reduces overall threats by 97 % | MASON [89] Chowdhary 2018 | N | risk/vulnerability | §V-B-1, p. 25, L2995–3004 |
| sengupta2020 | reduction in reconnaissance attempts and exploits; rotation window (60 s makes nmap fingerprinting ineffective) | — | — | MORE [66] Thompson 2014 | A | success events / configuration change | §V-B-1, p. 25, L3005–3009 |
| sengupta2020 | average vulnerability of configurations; decaying vulnerability rates | — | — | Crouse et al. [71] | N | risk/vulnerability | §V-B-1, p. 25, L3010–3014 |
| sengupta2020 | Attack Graph / Attack Tree (ARMs) | ARM, AG, AT | answer "(a) What are the possible attack paths … (b) What attack paths can be taken … to reach a specific target node" | Attack Graph [45]; Attack Tree [35]; SDN scalable MTD [51]; Bayesian AG [95] Miehling; Fig. 13 adds [88], [96], [161], [162] | N | attack paths | §V-B-1, p. 25, L3015–3034; defs §II-E Def. 1–2, p. 6 |
| sengupta2020 | Risk Metrics | — | risk associated with deploying the MTD | Fig. 13: [163] Hong & Kim 2016, [46] Hong & Kim 2013, [164], [63], [79], [89], [88] | N | risk/vulnerability | §V-B-1, p. 25, L3042–3072 |
| sengupta2020 | risk via HARM; instance measure | IM | "computing the instance measure (IM) which uses vulnerability's base score, impact score, etc" | Hong & Kim [163]; IM from [46] | N | risk/vulnerability | §V-B-1, p. 25, L3062–3072 |
| sengupta2020 | damage / cost caused by an attacker at different stages (bounded cost function); peak of risk | — | zero-sum matrix game, SPE | Zhu et al. [63] (Zhu & Başar 2013) | A / N | risk/vulnerability; game payoff | §V-B-1, p. 25, L3073–3083 |
| sengupta2020 | statistical risk metrics for "how the attacker can quickly conduct and succeed in adversarial attacks"; APT overhead "that can be measured and detected"; CPU utilisation | — | validated by simulated APT scenario | [126] Taylor et al. 2016 | A | attacker time / stealth/detection | §V-B-1, p. 25, L3084–3094 |
| sengupta2020 | revenue for defensive and offensive approaches (Markov game) | — | theorem under probabilistic constraints | Cheng et al. [60] (ref list: Lei, Ma, Zhang 2017) | A / D | game payoff | §V-B-1, p. 25–26, L3095–3104 |
| sengupta2020 | minimum effort required to detect stealthy botnets | — | "determine the minimum effort required a system to detect stealthy botnets" | [76] Venkatesan et al. 2016 | D | stealth/detection | §V-B-1, p. 26, L3105–3108 |
| sengupta2020 | entropy (distance of adversary from detection point) | — | "entropy was measured to determine how close an adversary is to the detection point, where high entropy indicates the attacker is far in distance from the detector" | [76] Venkatesan et al. 2016 | A | stealth/detection | §V-B-1, p. 26, L3109–3111 |
| sengupta2020 | Return of Investment | ROI | countermeasure selection over attack paths; "Countermeasure option that produces the smallest ROI is considered the optimal one" | Chung et al. [88] NICE | D | defence cost/overhead | §V-B-1, p. 26, L3117–3123 |
| sengupta2020 | network delay, CPU utilization, traffic load | — | NICE system performance | [88] | D | defence cost/overhead | §V-B-1, p. 26, L3124–3125 |
| sengupta2020 | threat score vs number of intrusions and vulnerabilities; service risk value | — | PageRank-like threat scoring | Chowdhary et al. [51] | N | risk/vulnerability | §V-B-1, p. 26, L3126–3141 |
| sengupta2020 | Policy Conflict Analysis | — | "how different MTD countermeasures … can cause security policy violations" (loops, blackholes) | Pisharody [157], [158]; [159]; Khurshid [160]; Fig. 13 adds [51], [79] | D | other (policy) | §V-B-1, p. 26, L3142–3156 |
| sengupta2020 | QoS Metrics (network bandwidth, delay) | QoS | "QoS (network bandwidth, delay), impact on existing mission metrics and the cost of deploying MTD" | Fig. 13: [54], [153], [65], [67], [59], [76], [77], [86], [110] | D | availability/QoS | §V-B-2, p. 26, L3157–3160 |
| sengupta2020 | vIP collisions / unpredictability constraints | — | minimise QoS impact of vIP collisions while maintaining unpredictability | Jafarian et al. [54] | D | configuration change | §V-B-2, p. 26, L3162–3167 |
| sengupta2020 | reconnaissance, deception performance, attack success probability vs connection drop probability, attacker's success probability (vs network size, number of vulnerable computers) | — | — | Crouse et al. [153] | A / D | success events; availability/QoS | §V-B-2, p. 26, L3167–3173 |
| sengupta2020 | Mission Success | — | "the rate at which mission tasks are completed" | Taylor et al. [126] | D | availability/QoS (mission) | §V-B-2, p. 26, L3174–3183 |
| sengupta2020 | Mission Productivity | — | "how often are mission tasks successful" | Taylor et al. [126] | D | availability/QoS (mission) | §V-B-2, p. 26, L3180–3183 |
| sengupta2020 | performance vs adaptability (static vs dynamic attacks; slow vs fast-evolving adversary) | — | — | Carter et al. [65] | A / D | other | §V-B-2, p. 26, L3184–3191 |
| sengupta2020 | availability, downtime, downtime cost (CTMC); normalised CVSS score as migration trigger | — | — | El-Mir [67] | D | availability/QoS | §V-B-2, p. 26, L3192–3198 |
| sengupta2020 | network throughput vs number of detection agents | — | 16 Gbps (1 agent) → ~6 Gbps (15 agents) | Sengupta et al. [77] | D | defence cost/overhead | §V-B-2, p. 26, L3199–3207 |
| sengupta2020 | packet count / packet delay; percentage of information disclosure (90 % → 10 %) | — | — | CHAOS [86] Shi 2017 | D / A | availability/QoS; other (attacker knowledge) | §V-B-2, p. 26, L3208–3215 |
| sengupta2020 | Cost Metrics — adaptation cost; cost to defender if attacker exploits a vulnerability | — | "what is the adaptation cost? … what is the cost incurred by a defender if an attacker succeeds" | Wang et al. [154] 2016; Fig. 13: [155], [126], [77], [38], [156], [116] | D | defence cost/overhead | §V-B-2, p. 26–27, L3216–3263 |
| sengupta2020 | mission productivity (ΔM) and attack success productivity (ΔA) | ΔM, ΔA | change-point analysis of cost-benefit on DNAT | Lei et al. [155] 2016 | D / A | success events (rate) | §V-B-2, p. 27, L3263–3269 |
| sengupta2020 | Measurement of Effectiveness | MOE | umbrella for Taylor's cost/effectiveness evaluation | Taylor et al. [126] | A / D | other | §V-B-2, p. 27, L3273–3275 |
| sengupta2020 | hop-delay (for different attack success rates) | — | — | [126] | D | defence cost/overhead | §V-B-2, p. 27, L3276–3277 |
| sengupta2020 | attacker's productivity | — | "how quickly attacker can perform adversarial tasks"; increases against static defence | Taylor et al. [126] | A | attacker time / tempo | §V-B-2, p. 27, L3277–3280 |
| sengupta2020 | attacker's confidentiality | — | "ability to remain undetected"; "same for both the static and the dynamic defense case" | Taylor et al. [126] | A | stealth/detection | §V-B-2, p. 27, L3280–3282 |

### 3c. Metrics and metric-like quantities elsewhere in Sengupta

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| sengupta2020 | success rate of cyberattacks | — | what MTD reduces (abstract) | — | A | success events | Abstract, p. 1, L53 |
| sengupta2020 | Cost of Attack | COA | QoS segmentation: "malicious traffic can be slowed down in order to increase the Cost of Attack (COA)" | — | A | attacker effort/cost | §II-D-9, p. 5, L598–602 |
| sengupta2020 | (Tarpit rationale) attacker gives up if goal takes too long | — | "adversaries will give up on a target if it takes too long to achieve the defined goal" | — | A | other (disengagement) | §II-D-8, p. 5, L594–597 |
| sengupta2020 | Access Complexity; Exploitability Score; Impact Score (CVSS v2) | AC, ES, IS | AC categorical {EASY, MEDIUM, HIGH}; CIA in [0,10] | CVSS [34], [12] | N | risk/vulnerability | §II-E-2, p. 5, L675–686 |
| sengupta2020 | time to construct attack representation methods | — | "grows exponentially with … number of hosts or … vulnerabilities" | [46] | D | defence cost/overhead | §II-E, p. 6, L755–758; Table III p. 7 |
| sengupta2020 | attack traffic volume → chance of getting caught (crossfire obfuscation) | — | "attackers are forced to use a lot of attack traffic … Such behavior increases their chances of getting caught" | [55] Aydeger 2016 | A | stealth/detection (noise) | §III-A-1, p. 8, L955–960 |
| sengupta2020 | noisy-rich (NR) cyber-attackers | NR | "adversaries who try to exploit all the vulnerabilities present in order to compromise the target network" (an attacker type, not a metric) | Jajodia et al. [58] | A | behavioural variety (attacker type) | §III-A-1, p. 8, L979–982 |
| sengupta2020 | rewards R^D, R^A weighting change in features ΔF, attack surface ΔAS, attack surface measurement ΔASM | ASM | "R^D = B1(ΔF) + B2(ΔAS) − D1(ΔASM); R^A = B3(ΔASM) − D2(ΔAS)"; D1 = cost of defence action, D2 = cost of attack action | Manadhata [62] | D / A | game payoff; attacker effort/cost | §III-C-1, p. 13–14, L1521–1537 |
| sengupta2020 | cyber attack inter-arrival rate | CAIA | "knowledge obtained from historical attack data to obtain a cyber attack inter-arrival (CAIA) rate"; switching period constrained below CAIA | Debroy et al. [68] | A | attacker time / tempo | §III-B-1, p. 12, L1346–1350 |
| sengupta2020 | (OS rotation evaluation) likelihood of thwarting a successful exploit; magnitude of impact of an exploit; availability of applications | — | evaluated over 60–300 s periods | Thompson et al. [66] | A / D | success events; availability/QoS | §III-B-1, p. 12, L1324–1336 |
| sengupta2020 | switching time period (15 s jamming, 60 s Nmap) | — | empirically chosen periods | [59]; [90] | D | configuration change | §VI-B, p. 27–28, L3333–3337 |
| sengupta2020 | mutation rate (HFM / LFM) | HFM, LFM | sensitive hosts have a higher mutation rate | [52] Al-Shaer; OF-RHM [54] | D | configuration change | §III-B-1 p. 12 L1356–1361; §IV-B, p. 18, L2251–2253 |
| sengupta2020 | proportion of information-gathering and external scanning attempts thwarted (~99 %) | — | OF-RHM result | Jafarian et al. [54] | A | success events (recon) | §IV-B, p. 18, L2255–2257 |
| sengupta2020 | exploits probability; VM reputation (history of attacks against the VM); exposure period during migration | — | frequency-minimal MTD factors | Debroy et al. [68] | A / N | success events; risk | §IV case study, p. 18, L2291–2324 |
| sengupta2020 | attack success rate; network bandwidth; VM performance (GENI) | — | — | GENI FM-MTD testbed | A / D | success events; availability | §IV-D, p. 19, L2378–2383 |
| sengupta2020 | attack efficiency (reduced by proxy replacement) | — | "renders the exploration effort of the attacker useless and at the same time, reduced the attack efficiency of the attacker" | [76] (as cited in text) | A | attacker effort/cost | §III-A-5, p. 10, L1197–1205 |
| sengupta2020 | attacker uncertainty whether attack was detected or is being monitored | — | effect of prevention-surface shifting (qualitative) | — | A | stealth/detection | §III-A-4, p. 10, L1167–1175 |

Sengupta also states (§V-A, Fig. 12 caption, p. 22) that *no* surveyed work considers all four qualitative metric kinds, and (§VI-D, p. 28) that "the lack of testing against real-world attackers also makes it difficult to prioritize which metrics a defender needs to care about".

---

## 4. ward2018 — Ward, Gomez, Skowyra, Bigelow, Martin, Landry, Okhravi, "Survey of Cyber Moving Targets, Second Edition", MIT LL Technical Report 1228, 17 Jan 2018

Source: `docs/sources/methodology/ward2018_mit_survey.md` (pdfminer extraction, 333 PDF pages; `=== page N ===` markers are **PDF** pages; the report's printed page = PDF page − 12, e.g. §6.1 DYNAT is printed p. 237 = PDF p. 249). Locators below give PDF page + source line.

**Shape of the metric content.** Ward is a technique catalogue, not a metrics survey. It defines **no named security metric**. What it does define is a fixed *per-technique evaluation template* (§1.7, PDF p. 17–18), applied to all ~110 entries; those template fields are Ward's evaluation dimensions and are recorded as rows 4a. The per-entry numbers (e.g. "13% throughput overhead") are measurements of the template's cost dimensions, attributed to the entry's primary paper; 4b records each *distinct* quantity type with representative locators rather than every numeric instance. 4c records every attacker-side, detection, effort and tempo quantity found (searched across all entries; ch. 5 Dynamic Platforms and ch. 6 Dynamic Networks read in full).

### 4a. The per-technique evaluation template (Ward's own dimensions)

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| ward2018 | Execution Overhead | — | per-entry bullet list (e.g. % over SPEC benchmark, added µs) | per-technique primary paper | D | defence cost/overhead | §1.7 p. 17; every entry (e.g. §2.1 PDF p. 19) |
| ward2018 | Memory Overhead | — | per-entry | per-technique | D | defence cost/overhead | §1.7; every entry |
| ward2018 | Network Overhead | — | per-entry (bytes per header, latency, dropped connections, redundant packets) | per-technique | D | defence cost/overhead; availability/QoS | §1.7; every entry |
| ward2018 | Hardware Cost | — | per-entry | per-technique | D | defence cost/overhead | §1.7; every entry |
| ward2018 | Modification Costs | — | checklist: Data / Source Code / Compiler-Linker / Operating System / Hardware / Infrastructure | own | D | defence cost/overhead | every entry (e.g. §2.1 PDF p. 20) |
| ward2018 | Expertise Required to Implement | — | ordinal: Simple Configuration/Installer; Complex Configuration (System Admin); Custom Programmer (General); Custom Programmer (Experiment/Low-Level/Kernel) | own | D | defence cost/overhead | every entry (PDF p. 20) |
| ward2018 | Expertise Required to Operate | — | ordinal: Seamless; Simple Configuration; Complex Configuration (System Admin); Expert Operator | own | D | defence cost/overhead | every entry (PDF p. 20) |
| ward2018 | Kill-Chain Phases | — | checklist over Ward's 5-phase kill chain: Reconnaissance, Access, Exploit Development, Attack Launch, Persistence | own (adapted; §1.4) | A (phase disrupted) | other (coverage) | §1.4 PDF p. 15–16; every entry |
| ward2018 | Attack Techniques Mitigated | — | categorical over Ward's CAPEC-derived taxonomy (Data Leakage, Resource, Code/Control Injection, Spoofing, Exploitation of Authentication, Exploitation of Privilege/Trust, Scanning, Supply Chain/Physical) | CAPEC [3] | A | other (coverage) | §1.2 PDF p. 13–15; every entry |
| ward2018 | Entities Protected | — | categorical: Applications, OS, Machine, Network, Traffic, Session, Data | own | N | other (coverage) | §1.3 PDF p. 15 |
| ward2018 | Types of Weaknesses | — | checklist: Overcome Movement; Predict Movement; Limit Movement; Disable Movement | own | A (attacker counter-capability) | other (defeat mode) | §1.5 PDF p. 16–17; every entry |
| ward2018 | Impact on Attackers | — | free-text assessment per entry | own | A | other (qualitative) | §1.7 p. 17; every entry |
| ward2018 | Availability (of the technique) | — | prototyped / public / commercial | own | — | other | every entry |

### 4b. Distinct measured quantities appearing inside entries (representative locators)

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| ward2018 | throughput overhead; latency overhead (%) | — | e.g. Apache 2-variant UID: 13 %/14 % unsaturated, 58 %/135 % saturated | §2.2 primary [7] | D | availability/QoS | §2.2 PDF p. 23 |
| ward2018 | average execution / memory overhead (%) on benchmarks | — | e.g. 11 % exec, 1 % memory (data randomization); ISR 17 %, CSD 54 % (Genesis); monitor 17/30/37 % for 2/3/4 variants (multivariant) | [8]; §5.2; §5.3 primaries | D | defence cost/overhead | §2.3 PDF p. 26; §5.2 PDF p. 189 L9080; §5.3 PDF p. 192 L9245 |
| ward2018 | downtime during migration | — | "A few seconds of downtime during migration" (TALENT) | §5.6 primary | D | availability/QoS | §5.6 PDF p. 204, L9791 |
| ward2018 | added request-processing time | — | "Up to an additional 50% time may be needed to process a request" | §5.7 primary | D | availability/QoS | §5.7 PDF p. 207, L9956 |
| ward2018 | header bytes; protocol latency | — | "IPSec adds an additional 24 bytes … average 30% latency" (RITAS) | [132] | D | defence cost/overhead | §6.3 PDF p. 258 |
| ward2018 | dropped connections due to IP address changes | — | NASR network overhead | [133] | D | availability/QoS | §6.4 PDF p. 261 |
| ward2018 | address-space overhead; routing-update overhead | — | "The faster the mutation rate, the higher the overhead"; routing overhead ∝ routing-table size | RHM [138] | D | defence cost/overhead | §6.8 PDF p. 276 |
| ward2018 | flow-table size overhead (number of rules) | — | related to address-mutation rate, number of hosts, flow-termination rate | OF-RHM [139] | D | defence cost/overhead | §6.9 PDF p. 279 |
| ward2018 | DNS traffic overhead; controller execution overhead | — | spatio-temporal mutation | [141] | D | defence cost/overhead | §6.10 PDF p. 283 |
| ward2018 | per-flow trigger latency (0.322 µs reporting, 1.697 µs rule activation) | — | AVANT-GUARD | [142] | D | defence cost/overhead | §6.11 PDF p. 286 |
| ward2018 | packet loss vs frequency of node ID updates | — | "Packet loss increases with the frequency of node ID updates" | [143] | D | availability/QoS | §6.12 PDF p. 291 |
| ward2018 | proportion of redundant packets (51.84 %) | — | CPSMorph | [144] | D | defence cost/overhead | §6.13 PDF p. 294 |
| ward2018 | client reassignment time (60 clients < 5 s); greedy O(N·M) | — | cloud DDoS shuffling | [145] | D | defence cost/overhead | §6.14 PDF p. 298 |
| ward2018 | expected number of benign clients saved per shuffling round; number of shuffling rounds to save 95 % vs 80 % of benign clients (+40 %) | — | objective of the greedy algorithm and its cost curve | [145] | D | availability/QoS | §6.14 PDF p. 297, 300 |
| ward2018 | response-time increase per packet flow (0.2 ms); time to generate a virtual-network view (seconds) | — | RDS | [147] | D | availability/QoS | §6.15 PDF p. 302 |
| ward2018 | delay overhead of virtual paths (+15 ms two-peer) | — | EPRM | [150] | D | availability/QoS | §6.17 PDF p. 310 |
| ward2018 | QoS constraints: bandwidth; number of hops / end-to-end delay | — | quoted constraints | [150] | D | availability/QoS | §6.17 PDF p. 309 |
| ward2018 | resilience constraint: minimum link overlap between successive virtual paths | — | "a sequence of virtual paths should have minimum overlap in the links used in order to increase unpredictability" | [150] | D | configuration change | §6.17 PDF p. 309 |
| ward2018 | latency per new flow (DFI); rule TTL trade-off | — | overhead at most once per flow | [153] | D | availability/QoS | §6.19 PDF p. 318, 320 |
| ward2018 | mutation rate / rotation rate / validity interval / MRT | — | movement-frequency parameters recurring across entries (RHM, OF-RHM, MORE, DARE, MANET IDs, Minimum Run Time) | various | D | configuration change | §6.8–6.12; §5.15–5.17 |

### 4c. Attacker-side, detection, effort and tempo quantities (exhaustive search)

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| ward2018 | probability of detection (raised by brute-force failures) | — | brute-forcing keys "could result in a large number of program failures that would increase the probability of detection" | §2.3 primary [8] | A | stealth/detection | §2.3 PDF p. 28, L1274–1277 |
| ward2018 | amount of work an attacker has to do (workload) | — | recurrent Impact-on-Attackers phrase ("increases the workload for an attacker", "amount of work … to discover the targets if he is using IP scans") | various (e.g. DYNAT [129,130]; RITAS [132]; ARCSYNE [136]) | A | attacker effort/cost | §2.4 PDF p. 31; §6.1 PDF p. 251; §6.3 PDF p. 260; §6.7 PDF p. 273; §5.4, §5.8 PDF p. 198, 214 |
| ward2018 | number of attack attempts needed / whether attempts succeeded (decoys) | — | "Makes it difficult for attackers to determine if their attack attempts have succeeded" | RedHerring §3.8 primary | A | other (attacker knowledge) | §3.8 PDF p. 68 |
| ward2018 | time before being detected (depends on mutation rate) | — | "Depending on the mutation rate, attacks may succeed for a lengthy period of time before being detected, if at all" | §3.11 primary | A | stealth/detection; attacker time (dwell) | §3.11 PDF p. 77, L3651 |
| ward2018 | number of leaked key bits (≈100 → 16 of 128) | — | side-channel leakage | §3.12 primary | A | success events (information) | §3.12 PDF p. 80, L3805 |
| ward2018 | bits of entropy (29 heap, 28 stack, 20 mmap, 20 data/code) | — | randomisation entropy bounded by machine width | ASLP §4.1.1 primary; [41, 42] | D | configuration change (unpredictability) | §4.1.1 PDF p. 87, L4114–4117 |
| ward2018 | number of guesses to brute-force ASLR ("at most 1024 guesses" on 64-bit clone-probing) | — | each failed guess crashes the child | RASLR [69] | A | attacker effort/cost (attempts) | §4.1.14 PDF p. 127, L6066–6071 |
| ward2018 | false-negative / false-positive rate of pointer tracking | — | RASLR taint tracking | [69] | D | other | §4.1.14 PDF p. 127, L6083 |
| ward2018 | booby-trap trigger probability (crash + warning on attack) | — | "triggered with high probability. A booby trap crashes the program and displays a warning that an attack was attempted" | Readactor++ §4.1.17 primary | A | stealth/detection | §4.1.17 PDF p. 137, L6564 |
| ward2018 | probability of successful attack diminishing exponentially with gadget-chain length | — | Isomeron | §4.1.20 primary | A | success events | §4.1.20 PDF p. 146, L7028 |
| ward2018 | stealthy attacker avoids detection (detection-dependent MTDs) | — | "A stealthy attacker could avoid detection and carry out their attack without extra hindrance" | Security Agility Toolkit §5.1 | A | stealth/detection | §5.1 PDF p. 187, L8976 |
| ward2018 | security score of a configuration | — | "the number and severity of security incidents reported while that configuration was active"; weakness: "based on detected attacks … A stealthy attacker could still carry out their attack"; attacker may manipulate it "by causing detections" | GA configurations §5.10 primary | N (driven by detections) | risk/vulnerability; stealth/detection | §5.10 PDF p. 218–220, L10439–10566 |
| ward2018 | exposure time (of a server before cleaning) | — | "minimal exposure time before cleaning a system would require a fast-acting exploit"; "decreases the amount of time an attacker has to accomplish their goal" | SCIT [115–117] | A / N | attacker time | §5.9 PDF p. 215 |
| ward2018 | information leakage rate between co-resident VMs; co-residency time | — | Nomad minimises global leakage "by trying to minimize the time they are co-resident"; benefit quantifiable only "if the provider is aware of the leakage rate" | Nomad §5.14 primary | A | success events (information) / attacker time | §5.14 PDF p. 233–236 |
| ward2018 | time window during which attackers can scan and attack (periodic rotation) | — | "rotation is periodic provides a time window during which attackers can scan and attack the system as normal"; attacker "can simply wait for a scanned VM to come back into rotation" | MORE [125]; DARE [126] | A | attacker time / behavioural variety (waiting) | §5.15 PDF p. 239; §5.16 PDF p. 242 |
| ward2018 | time it takes an attacker to identify and exploit an OS / web service | — | Impact on Attackers | MORE [125]; DARE [126] | A | attacker time | §5.15 PDF p. 239, L11434; §5.16 PDF p. 242 |
| ward2018 | variety of targets available to the attacker | — | rotation "may actually help the attacker by increasing the variety of targets" | MORE; DARE | A | reach/breadth | §5.15 PDF p. 239; §5.16 PDF p. 242 |
| ward2018 | minimum run time vs sensitive-computation time (2 ms vs 5 ms) | MRT | MRT longer than the sensitive computation "completely removes the ability of an attacker to measure intermediate computation states" | §5.17 primary | D / A | configuration change | §5.17 PDF p. 243–245 |
| ward2018 | rate of attack (slowed to avoid triggering the defence) | — | "An attacker could avoid triggering Düppel to switch from sentinel to battle mode by slowing the rate of attack. This causes loss of precision, but is likely preferable to triggering the defense." | Düppel §5.18 primary | A | stealth/detection; tempo | §5.18 PDF p. 248, L11894 |
| ward2018 | classifier accuracy on leaked instructions (90 % → 38 %) | — | information leaked under Düppel | §5.18 primary | A | success events (information) | §5.18 PDF p. 248 |
| ward2018 | likelihood of detecting anomalies (flooded obfuscated fields) | — | "This same property would also increase the likelihood of detecting anomalies" | DYNAT [129, 130] | D | stealth/detection | §6.1 PDF p. 249, L11947 |
| ward2018 | pool size of addresses (predictability of next address) | — | small pool lets attacker "predict which addresses will be next with better accuracy" | ARCSYNE [136]; NASR [133] | D | configuration change | §6.7 PDF p. 273; §6.4 PDF p. 263 |
| ward2018 | chance of being detected (rises with scanning frequency) | — | "A persistent adversary might try scanning frequently and from each host she is able to target and reach, but that increases her chance of being detected" | Spatio-temporal address mutation [141] | A | stealth/detection; tempo | §6.10 PDF p. 285, L13686 |
| ward2018 | deception and detectability metrics (defined by the primary authors) | — | "deception and detectability metrics defined by the authors are evaluated as other configurable variables" (not reproduced by Ward) | [141] | A | stealth/detection | §6.10 PDF p. 285, L13697 |
| ward2018 | scan-detection indicator: abnormal increase in size of connected components of the communication graph in an interval | — | triggers deceptive mutation | [141] | D | stealth/detection | §6.10 PDF p. 282–283 |
| ward2018 | traffic-rate trigger (packets per second, bits per second, raw count) | PPS, BPS | attacker "could infer some conditions … then operate in a way that does not trigger the rule activation"; payload "in a flow that stays below the traffic-rate trigger" | AVANT-GUARD [142] | A (evasion) / D (trigger) | stealth/detection; tempo | §6.11 PDF p. 286–288 |
| ward2018 | inter-packet delay distribution (IPD) | IPD | traffic-analysis feature CPSMorph makes indistinguishable | [144] | A (observable) | stealth/detection | §6.13 PDF p. 293 |
| ward2018 | naive vs persistent bots (attacker types) | — | persistent bots follow moving replicas | [145] | A | behavioural variety (attacker type) | §6.14 PDF p. 297 |
| ward2018 | scan delay factor ("delayed malicious network scans up to a factor of 115") | — | slow-down of reconnaissance | RDS [147] | A | attacker time | §6.15 PDF p. 301 |
| ward2018 | "address distance" of vulnerable hosts from the scanning source | — | placement objective once a scanner is identified | RDS [147] | A | reach/breadth | §6.15 PDF p. 301 |
| ward2018 | detection of malicious flows (honeypot contacts) before the attack is finished | — | "Malicious flows from scanning … might be detected and the source mitigated before the attack is finished" | RDS [147] | D | stealth/detection | §6.15 PDF p. 304 |
| ward2018 | staying under the radar of detection tools (false negatives) | — | "attackers can overcome movement by staying under the radar"; time gap between IDS trigger and response | Bro NetControl [148]; PSI [152] | A | stealth/detection | §6.16 PDF p. 307–308; §6.18 PDF p. 315 |
| ward2018 | time the attacker has to finish the attack or evade the response | — | "an attacker has significantly less time (or none) to finish the attack or evade the response" | [148]; PSI [152] | A | attacker time | §6.16 PDF p. 308; §6.18 PDF p. 316 |
| ward2018 | reconnaissance needed for an attack to succeed | — | DFI "could greatly increase the reconnaissance needed" | DFI [153] | A | attacker effort/cost | §6.19 PDF p. 320 |

Ward's kill chain (§1.4, PDF p. 15–16) is five phases: Reconnaissance, Access, Exploit Development, Attack Launch, Persistence (the "MIT Lincoln lab shorter version" that Cho §V-B also reports).

---

## 5. zhuang2012 — Zhuang, Zhang, DeLoach, Ou, Singhal, "Simulation-based Approaches to Studying Effectiveness of Moving-Target Network Defense", National Symposium on Moving Target Research, 2012

Source: `docs/sources/methodology/zhuang2012_simulation_mtd.md` (12 pages, `=== page N ===` markers). **Not a survey**: a design-schema + NeSSi2 simulation paper (it is Cho's [183] and is cited by Ward). Its related-work §5 reports metrics from four primary works, which are recorded with Zhuang's citation. The paper states the analytical model "only captures the attacker's perspective" (§1, p. 2).

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| zhuang2012 | (required metric property 1) the area an attacker must search to determine the configuration | — | metrics "must capture (1) the area that an attacker must search to determine the configuration of the system" | own | A | attacker effort/cost (search space) | §1, p. 1, L77 |
| zhuang2012 | (required metric property 2) the modifiable aspects of the system | — | — | own | D | configuration change | §1, p. 1 |
| zhuang2012 | (required metric property 3) what is changing and how fast | — | "what is changing in the system configuration and how fast the configuration is changing"; must be "relatable to the effort required by an attacker" | own | D → A | configuration change; attacker effort | §1, p. 1–2, L77–88 |
| zhuang2012 | adversary's chance for success / attacker's success likelihood | — | what the MTD is hypothesised to decrease | own | A | success events | Abstract p. 1 L30; §1 p. 2; §6 p. 11 |
| zhuang2012 | time canvassing the network | — | "the attacker needs to spend more time canvassing the network in order to identify topological information" | own | A | attacker time (recon) | §2, p. 3, L247 |
| zhuang2012 | privilege retention / frequency of regaining privileges | — | "the attacker cannot keep privileges gained for long and will have to frequently regain privileges" | own | A | attacker effort/cost; attacker time | §2, p. 3, L250 |
| zhuang2012 | accumulate knowledge and privileges "as long as he is not detected" | — | undetected accumulation as the limit on MTD | own | A | stealth/detection | §2, p. 3, L182 |
| zhuang2012 | attacker effort and likelihood of revealing themselves (guessing service locations) | — | "repeatedly conduct extensive reconnaissance to re-identify service locations, thus increasing the attackers' effort and the likelihood of revealing themselves"; following the RMS pattern "significantly simplifies intrusion detection" | own | A | stealth/detection; attacker effort/cost | §2.1.1, p. 5, L342 |
| zhuang2012 | probability of correctly guessing IP and port of next target | — | "a low-probability event"; wrong guess "will fall into a decoy that can issue alerts and track the attacker's activities" | own | A | success events; stealth/detection | §2.2, p. 6, L482–494 |
| zhuang2012 | how far an attacker can move forward (vs MTD frequency) | — | "The frequency of such MTD mechanisms will affect how far an attacker can move forward in a system" | own | A | reach/breadth (path progress) | §2.2, p. 6, L444 |
| zhuang2012 | effort of activities on a conservative-attack-graph edge | — | "The effort involved in the activities can be measured in various ways" | own | A | attacker effort/cost | §2.2, p. 6 |
| zhuang2012 | success-likelihood to time diagram | — | "how much time it will take the attacker to reach a certain success likelihood for a specific action" (Fig. 5 axis: probability of success vs t) | own | A | attacker time; success events | §2.2, p. 7, L512 |
| zhuang2012 | probability of being forced to "move back" to a prior state | — | "a probability for the attacker to be forced to 'move back' to one of the prior state along the path, due to the MTD mechanisms" | own | A | reach/breadth (regression) | §2.2, p. 7, L516 |
| zhuang2012 | CAG edge value = attacker's probability of success node-to-node (static) | — | e.g. 0.4 Planner→TargetDB; "computed based on combining the probability of unknown and known vulnerabilities" | own | A | success events | §3.2, p. 8, L658 |
| zhuang2012 | success ratio of each (individual) attack | — | ≈50 % static → 16.2 % at adaptation interval 20 (Fig. 8) | own | A | success events | §4, p. 9, L710 |
| zhuang2012 | number of completed attacks (out of 1000) against the TargetDB | — | 245 static; 50 at interval 100; 5 at interval 20 (Fig. 9) | own | A | success events | §4, p. 9, L723 |
| zhuang2012 | adaptation interval (20, 50, 100, 200, ∞) | — | time between Configuration Manager adaptations (independent variable) | own | D | configuration change | §4, p. 9, L693ff |
| zhuang2012 | Δt (time to launch an attack; 50 set, 102 actual) | — | "simulates the time required to launch an attack" | own | A | attacker time (tempo parameter) | §3.2/§4, p. 8–9 |
| zhuang2012 | length of the CAG path to the node of interest | — | "the longer the path in the CAG to a node of interest, the more protection an MTD system provides" | own | N | attack paths | §4.1, p. 10, L765 |
| zhuang2012 | attacker's effort (network mapping) / ability to map the network | — | DYNAT "made it almost impossible to map the network while significantly increasing the attacker's effort" | [11] Kewley & Bouchard (DARPA dynamic defense experiment) | A | attacker effort/cost | §5, p. 10, L797 |
| zhuang2012 | attacker actions as obvious anomalies (ease of spotting attacks) | — | "DYNAT highlighted typical attacker actions as obvious anomalies that made spotting the attacks much easier" | [11] | A | stealth/detection | §5, p. 10, L802 |
| zhuang2012 | worms easier to detect | — | NASR "beneficial in making the worms easier to detect" | [3] Antonatos et al. 2007 | A | stealth/detection | §5, p. 10, L849 |
| zhuang2012 | soft / hard change timer | — | minimal interval between address changes with no activity / maximum time a host keeps an address | [3] | D | configuration change | §5, p. 10 |
| zhuang2012 | metric for topological network change | — | "captures the difference in the required bandwidth between two nodes"; links active 33 % of the time | [6] (Compton / Hopkinson et al.) | D | configuration change | §5, p. 10–11, L858 |
| zhuang2012 | runtime of obfuscation heuristic; deviation from optimal | — | NOH vs MILP | [9] Greve 2010 | D | defence cost/overhead | §5, p. 11 |
| zhuang2012 | entropy in the executables | — | "with sufficient entropy in the executables, the approach was effective at thwarting known attacks" | [17] (proactive obfuscation) | D | configuration change | §5, p. 11 |
| zhuang2012 | cost and overhead of deploying the MTD on the mission | — | deferred ("A more comprehensive analysis will also take into account…") | own | D | defence cost/overhead | §1, p. 2 |

---

## 6. zaffarano2015 — Zaffarano, Taylor, Hamilton, "A Quantitative Framework for Moving Target Defense Effectiveness Evaluation", MTD'15 (ACM), pp. 3–10

Source: `docs/sources/lit_review/zaffarano2015.md` (Ghostscript two-column text; printed page numbers 3–10 appear as bare lines, so pages are pinned: p. 3 ≤ L61, p. 4 ≤ L111, p. 5 ≤ L143, p. 6 ≤ L208, p. 7 ≤ L277, p. 8 ≤ L330, p. 9 ≤ L389, p. 10 ≤ L460). **Not a survey**: a framework paper and the *primary* source that Cho [173] and Sengupta [131] relay. It defines four task attributes, and four metrics × two activity models (mission, attacker) = **eight metrics** (Fig. 2, Table 4). Each metric's MTD effect is the **difference between a run with the MTD and the baseline run without it** (Table 3).

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| zaffarano2015 | task attribute: duration | — | "length of time to complete the task execution, values are non-negative real numbers" | own | A / D | attacker time (per task) | §3.2, p. 7, L212–213 |
| zaffarano2015 | task attribute: success | — | "whether the task was successfully completed, values are 0 … and 1" | own | A / D | success events | §3.2, p. 7, L214–215 |
| zaffarano2015 | task attribute: unexposed | — | "whether task information was exposed, values are 0 (information was exposed) and 1 (information was not exposed)" | own | A / D | stealth/detection (attacker) | §3.2, p. 7, L217–219 |
| zaffarano2015 | task attribute: intact | — | "whether task information was corrupted" | own | A / D | other (information integrity) | §3.2, p. 7, L221–223 |
| zaffarano2015 | Productivity | — | "Productivity(M, ν) = 1/\|T\| Σ_{τ∈T} ν(τ, duration)" — "a measure of how quickly tasks in an activity model can be completed", defined as "the average of the duration attribute over the tasks" | own | A / D | attacker time / tempo | §4.1, p. 8–9, L310–318 |
| zaffarano2015 | Mission Productivity | — | "the rate at which mission tasks are completed"; difference with vs without MTD "is the cost of deploying the MTD" (may be negative) | own | D | availability/QoS (mission) | §4.1 p. 8 L321–329; Table 4 p. 9 L332–333 |
| zaffarano2015 | Attack(er) Productivity | — | "the rate at which attacker tasks are completed" (Table 4: "how quickly an attacker can perform and complete adversarial tasks"); with − without MTD = "the effectiveness of the MTD with regard to attacker productivity"; "increased duration of attacker tasks is typically a good result from a defensive standpoint" | own | A | attacker time / tempo | §4.1 p. 9 L349–362; Table 4 L334–335 |
| zaffarano2015 | Success | — | "Success(M, ν) = 1/\|T\| Σ_{τ∈T} ν(τ, success)", real in [0,1] | own | A / D | success events | §4.2, p. 9, L378–386 |
| zaffarano2015 | Mission Success | — | "the number of attempted mission tasks that are successfully completed"; with − without MTD = cost | own | D | availability/QoS (mission) | Table 4 p. 9 L336–337; §4.2 L387–388 + L349–352 (column-interleaved) |
| zaffarano2015 | Attack Success | — | "how successful an attacker may be while attempting to attack a network"; difference = "a benefit of deploying the MTD" | own | A | success events | Table 4 p. 9 L338–339; §4.2 L352–355 |
| zaffarano2015 | Confidentiality | — | "Confidentiality(M, ν) = 1/\|T\| Σ_{τ∈T} ν(τ, unexposed)"; operationalised as "whether information is visible in plaintext in network traffic" | own | A / D | stealth/detection; other | §4.3, p. 9–10, L382–397 |
| zaffarano2015 | Mission Confidentiality | — | "how much mission information is exposed to eavesdroppers, whether information could be intercepted" | own | D | other (mission info) | Table 4 p. 9 L340–342 |
| zaffarano2015 | Attack Confidentiality | — | "a measure of how much attacker activity may be visible by detection mechanisms"; "an attacker being exposed is desirable" | own | A | stealth/detection | Table 4 p. 9 L343–344; §4.3 L385–386 |
| zaffarano2015 | Integrity | — | "Integrity(M, ν) = 1/\|T\| Σ_{τ∈T} ν(τ, intact)" | own | A / D | other (information integrity) | §4.4, p. 10, L407–419 |
| zaffarano2015 | Mission Integrity | — | "how much mission information is transmitted without modification or corruption" | own | D | other (mission info) | Table 4 p. 9 L345–346 |
| zaffarano2015 | Attack Integrity | — | "the accuracy of the information viewed by an attacker"; "an attacker's transmissions being corrupted is beneficial" | own | A | other (attacker knowledge) | Table 4 p. 9 L347–348; §4.4 L413–415 |
| zaffarano2015 | kill-chain phase against which the MTD is most effective | — | "argmax_{φ∈Φ} 1/\|T_φ\| Σ_{τ∈T_φ} ν′(τ, success) − ν(τ, success)" (ν′ with MTD, ν without); alternative: proportional change in success | own | A | success events (per phase) | §4.2, p. 9, L360–380 |
| zaffarano2015 | Overall metric (weighted average) | — | "a simple weighted average of each metric, where the network mission is positively weighted, and the attacker mission is negatively weighted" | own | A + D | other (composite) | §4.5, p. 10, L437–449 |
| zaffarano2015 | cost to mission / effectiveness (experimental matrix) | — | Table 3: mission model without MTD = mission baseline, with MTD = cost to mission; attacker model without = attacker baseline, with = effectiveness | own | A / D | other (baseline contrast) | Table 3, p. 8, L279–282; §4 L289–297 |
| zaffarano2015 | network visibility (nmap output) | — | Discovery stage: "assesses network visibility"; difference with/without MTD "indicate[s] whether an MTD is making it more difficult for an attacker to (accurately) view the network" | own; nmap | A | reach/breadth (visibility) | Table 2 p. 8 L279–282; L298–304 |
| zaffarano2015 | dictionary attack success or failure (ncrack) | — | Delivery stage | own; ncrack | A | success events | Table 2, p. 8 |
| zaffarano2015 | ability to successfully establish a backdoor (ncat) | — | C2 / Exfiltration stage | own; ncat | A | success events | Table 2, p. 8 |
| zaffarano2015 | ability to run, modify, delete, create (read/write/execute) incl. privilege escalation | — | Action stage; D5 effects (Deceive, Deny, Disrupt, Degrade, Destroy) | own | A | success events | Table 2 p. 8; L319–326 |
| zaffarano2015 | ability to maneuver within the network | — | Propagation stage (Discovery + Delivery combination) | own | A | reach/breadth | Table 2 p. 8; L327–328, L284–287 |
| zaffarano2015 | (non-metric benefit) finer-grained logging of attack operations for attribution | — | "conditions under which an MTD might fail to stop an attack, but is still able to monitor and log much more fine grained detail … not well represented in traditional information assurance metrics" | own | D | stealth/detection | §2, p. 4, L67–72 |

Discrepancy to flag: Sengupta §V-B-2 (p. 26, L3179–3183) attributes to **Taylor et al. [126]** (the 2016 companion paper, same authors) "Mission Success, i.e., the rate at which mission tasks are completed, and Mission Productivity, i.e., how often are mission tasks successful" — the reverse of Zaffarano 2015's Table 4 (Productivity = rate/duration; Success = number successful). Cho §VII-A (L593) paraphrases Zaffarano's DSP-like quantity as "the rate at which tasks are executed and completed", which also merges the two. Whether Taylor 2016 itself swaps them is unverified (not in the corpus read).

---

## 7. ghosh2009 — NITRD CSIA-IWG, *Cybersecurity Game-Change R&D Recommendations*, §1 "Moving Target Defense" (2009; repo key now `nitrd2009` per the extraction)

Source: `docs/sources/lit_review/1_1_ghosh2009NITRD.md` (+ `docs/sources/extractions/ghosh2009.md`). A research-agenda document of eleven "ideas" (§1.1–1.11). It **defines no metric and cites no primary metric source**; the quantities below are the evaluation targets and effect claims it names. No page numbers in the markdown; locators are section + line. Primary source column is "—" throughout because NITRD gives no citations.

| paper | metric (as written) | acronym | definition / formula | primary source cited | persp. | family | locator |
|---|---|---|---|---|---|---|---|
| ghosh2009 | amortization of development costs (attacker) | — | "we force him to do reconnaissance and launch exploits anew for every desired penetration; the attacker enjoys no amortization of development costs" | — | A | attacker effort/cost | §1 "What is the new game?", L9 |
| ghosh2009 | randomness / predictability of the defender's systems | — | "we win by increasing the randomness or decreasing the predictability of our systems" | — | D | configuration change (unpredictability) | §1, L9 |
| ghosh2009 | attacker persistence expectation | — | adversaries "can afford to invest significant resources in their attacks because they expect to persist in our systems for a long time" | — | A | attacker time (dwell) | §1, L9 |
| ghosh2009 | exposure time of rotated VMs | — | "VMs … rotated and exposed to the attacker only for a limited time" | — | N | attacker time / configuration change | §1.1 bullets, L13 |
| ghosh2009 | total cost of ownership; usability impact; virtualization performance | — | listed concerns | — | D | defence cost/overhead; availability/QoS | §1.1 concerns, L17–30 |
| ghosh2009 | change frequency relative to automated scanner and worm propagation | — | change "On a high frequency basis to outperform automated scanner and worm propagation" | — | D vs A | configuration change; tempo | §1.1.1, L63 |
| ghosh2009 | service disruption and delays | — | change "Quickly to minimize service disruption and delays" | — | D | availability/QoS | §1.1.1, L65 |
| ghosh2009 | entropy of the address/key distribution | — | "Unpredictable to ensure that future IP addresses and keys are undiscoverable and irreversible (i.e., high entropy distribution)" | — | D | configuration change (unpredictability) | §1.1.1, L67 |
| ghosh2009 | worm propagation slow-down (uncertainty in scanning phase) | — | evaluation target: "significantly slow down worm propagation by increasing uncertainty in scanning phase" against random-scanning and divide-and-conquer worms; tested with Nmap/Nessus and real scan traces | — | A | attacker time / tempo | §1.1.5.2, L151–153; §1.1.5.4, L173–175 |
| ghosh2009 | fraction of systems on which an attack succeeds; number of different attacks required; cost to the attacker | — | "any specific attack will succeed only on a small fraction of systems … An attacker would require a large number of different attacks … which radically increases the cost to the attacker" | — | A | reach/breadth; attacker effort/cost | §1.2.1, L183 |
| ghosh2009 | real-time detection by divergence of parallel variants | — | "attacks could be detected in real-time when the behaviors of the versions diverge" | — | D | stealth/detection | §1.2.1, L183 |
| ghosh2009 | performance overhead of diversity (5 %–10 %) | — | "paying a small performance overhead such as 5%-10% … may be worth the cost" | — | D | defence cost/overhead | §1.2.3, L201 |
| ghosh2009 | attackers slowed / confused / discouraged by decoys | — | "attackers will be slowed down (probably confused or discouraged) by interacting with fake targets" | — | A | attacker time; other (disengagement) | §1.6 intro, L615 |
| ghosh2009 | detection of new attack activity (decoy access) | — | "since decoys are not usually accessed, any such access points to ongoing attacker activity" | — | D | stealth/detection | §1.6 intro L615–617; §1.6.1 L637 |
| ghosh2009 | probability of a successful attack on the real target | — | decoys "increase the attack surface while decreasing the probability of a successful attack on the real target" | — | A | success events | §1.6.1, L639 |
| ghosh2009 | attack Return on Investment | ROI | "and hence reduce the attack Return on Investment (ROI)" | — | A | game payoff / attacker effort | §1.6.1, L639 |
| ghosh2009 | ratio of real : decoy targets (e.g. 1:10000) | — | "must be very low … creates a large additional attack surface that an attacker needs to cover" | — | D | configuration change / attacker effort | §1.6.1, L641 |
| ghosh2009 | red-team difficulty in violating security or functionality requirements; performance impact | — | "Quantitatively evaluate increase in read-team's [sic] difficulty in successfully violating security or functionality requirements. Also, assess performance impact"; "mid-term and final 'exams' … administered by red teams" | — | A / D | attacker effort/cost; defence cost | §1.7.4, L747; §1.7.5, L763 |
| ghosh2009 | additional work effort needed by attackers to reach the data | — | NSA red team to identify moving data | — | A | attacker effort/cost | §1.8.4, L847 |
| ghosh2009 | exposure duration (application online for a short duration) | — | "short exposure for adversary" | — | N | attacker time | §1.9 Benefits, L917 |
| ghosh2009 | decision cycle time vs attacker | — | "Decision cycle time: need to move faster than the attacker" (derailer) | — | D vs A | tempo | §1.11.2, L1097 |
| ghosh2009 | false positives | — | listed inertia of smart motion management | — | D | stealth/detection | §1.11 inertia, L1051 |
| ghosh2009 | optimal security–performance trade-off | — | benefit of smart motion adaptation | — | D | other (trade-off) | §1.11.1, L1075 |

---

# Cross-paper synthesis

Row references use `paper §locator`; full definitions are in the tables above.

## (a) Every attacker-side metric

**cho2020.** ASP (+ attackability [136], fingerprinter ASP [135], NetHide probability of attack success [115]); attack utility; learning by attackers [181]; MTTC (§VII-A and cloud [26],[27]); unpredictability (effect on attacker); attack surface; rate of successful attacks (inside DSP, [173]); attack confidentiality [173]; attack integrity [173]; worm propagation speed; vastness (as attacker search cost); penalty in attack payoff; attack cost + Nmap scanning overhead [93]; fraction of decoy nodes scanned [36]; portion of decoy nodes detected by attackers [35]; AC and RoA (Alavizadeh [5],[6]); attackers' overhead [93]; attacker's workload (Farris & Cybenko [51]); attack effort and complexity [20]; resistance to brute force [91]; success rate [16]; Trojan-attack success reduction [178]; intercept probability [63]; accessibility / knowledge [136].

**jalowski2026.** ASP (relayed from Cho, and critiqued §5); attack utility; MTTC/MTTF (spelled out); learning by attackers; attack cost; attack surface; state-collision probability (own analysis, §4.1).

**sengupta2020.** 1/probability of a new attack [65]; penalty imposed on attacker [73]; network fingerprint / leaked topology information [56], [150]; 1/attacker cost [133]; number of interruptions to reach a goal node [147]; attack success probability vs connection-drop probability [153]; attacker's productivity and attacker's confidentiality (Taylor [126]); attack success productivity ΔA [155]; statistical "how quickly the attacker can … succeed" and detectable APT overhead [126]; entropy distance to the detector [76]; damage/cost at stages [63]; offensive revenue [60]; reduction in reconnaissance attempts [66]; information disclosure % [86]; COA; attack efficiency [76]; R^A with D2 cost of attack action [62]; CAIA rate [68]; exploits probability [68]; attack success rate (GENI); success rate of cyberattacks (abstract); ~99 % scanning attempts thwarted [54]; likelihood of thwarting an exploit / magnitude of impact [66].

**ward2018.** Kill-Chain Phases / Attack Techniques Mitigated / Types of Weaknesses / Impact on Attackers (template); probability of detection from brute-force failures (§2.3); workload / amount of work (many entries); attack-attempt success uncertainty (§3.8); time before being detected (§3.11); leaked key bits (§3.12); number of guesses ≤ 1024 (§4.1.14); booby-trap trigger (§4.1.17); success probability vs gadget-chain length (§4.1.20); exposure time (§5.9); leakage rate / co-residency time (§5.14); attack/scan time window, time to identify and exploit, target variety (§5.15–5.16); rate of attack slowed to evade (§5.18); classifier accuracy on leaked data (§5.18); chance of being detected vs scanning frequency, detectability metrics (§6.10); staying below PPS/BPS triggers (§6.11); IPD features (§6.13); naive vs persistent bots (§6.14); scan delay factor ×115, address distance (§6.15); staying under the radar, time to finish/evade (§6.16, §6.18); reconnaissance needed (§6.19).

**zhuang2012.** Area to search; success likelihood / chance for success; time canvassing; privilege retention / regain frequency; undetected accumulation; effort and likelihood of revealing themselves; probability of guessing IP+port; how far the attacker moves forward; per-edge effort; success-likelihood-to-time diagram; move-back probability; CAG edge success probability; per-attack success ratio; completed attacks /1000; Δt; attacker's effort to map (DYNAT [11]); anomaly conspicuousness [11]; worm detectability [3].

**zaffarano2015.** Attack(er) Productivity (mean attacker-task duration); Attack Success (mean success over attempted attacker tasks); Attack Confidentiality (unexposed); Attack Integrity (accuracy of attacker's view); most-effective kill-chain phase (argmax of Δsuccess); network visibility (nmap); dictionary-attack success (ncrack); backdoor establishment (ncat); read/write/execute ability; ability to manoeuvre.

**ghosh2009.** Attacker amortisation of development cost; persistence expectation; fraction of systems an attack succeeds on / number of distinct attacks needed / cost to the attacker; slowed/confused/discouraged at decoys; probability of success on real target; attack ROI; red-team difficulty; additional work effort; worm-propagation slow-down.

## (b) Detection, detectability, stealth, evasion, noise, tempo, rate, intensity, dwell, probe/scan counts (priority)

**Named metrics that measure attacker detectability or stealth (the only three that are formally defined):**
1. **Attack Confidentiality** — Zaffarano 2015 Table 4 (p. 9, L343–344): "a measure of how much attacker activity may be visible by detection mechanisms"; formula Confidentiality(M,ν) = 1/|T| Σ ν(τ, unexposed) over attacker tasks (§4.3, L382–397), operationalised in 2015 only as "whether information is visible in plaintext in network traffic". Relayed as "attack confidentiality … the degree of attack behaviors detected by a defender" by Cho §VII-A (L605, cite [173]) and as **attacker's confidentiality, "ability to remain undetected"** by Sengupta §V-B-2 (p. 27, L3280–3282, cite Taylor et al. [126] 2016), with the finding that it is "same for both the static and the dynamic defense case".
2. **Entropy as distance from the detection point** — Sengupta §V-B-1 (p. 26, L3109–3111), cite Venkatesan et al. [76] 2016: "high entropy indicates the attacker is far in distance from the detector"; paired with "minimum effort required … to detect stealthy botnets".
3. **Deception and detectability metrics** — Ward §6.10 (PDF p. 285, L13697), cite spatio-temporal address mutation [141]: Ward says they are "defined by the authors" but does not reproduce them (primary paper needed; Cho's reference list has this as [88] Jafarian et al., "Spatio-temporal address mutation for proactive cyber …", L1119).

**Defender-side detection accuracy/quality metrics:** detection accuracy of anomaly behaviours (Cho, Colbaugh & Glass [38]); distinguishability (Cho, [66], [110]); detection capabilities vs cost (Cho, Lakshminarayana & Yau [100]); minimum effort to detect stealthy botnets (Sengupta [76]); threat score from IDS alerts + CVSS (Sengupta MASON [89]; [51]); scan-detection indicator = abnormal growth of connected components in the communication graph (Ward §6.10, [141]); malicious-flow detection via honeypot contacts (Ward §6.15, RDS [147]); false-positive/false-negative detections (Ward §2.2, §6.16; NITRD §1.11); decoy access as detection (NITRD §1.6); variant-divergence detection (NITRD §1.2.1; Ward §2.2, §5.3, §5.5); the GA "security score" built from detected incidents, which a stealthy attacker defeats and can manipulate "by causing detections" (Ward §5.10).

**Stated (unmeasured) links between attacker behaviour and detection:**
- *Brute force → crashes → detection*: "a large number of program failures that would increase the probability of detection" (Ward §2.3, PDF p. 28); booby traps (Ward §4.1.17); RASLR 1024 crash-guesses (Ward §4.1.14).
- *Scanning frequency / volume → detection*: "scanning frequently and from each host … increases her chance of being detected" (Ward §6.10, PDF p. 285, [141]); crossfire obfuscation forces "a lot of attack traffic … increases their chances of getting caught" (Sengupta §III-A-1, p. 8, L955–960, [55]); repeated reconnaissance increases "the attackers' effort and the likelihood of revealing themselves" (Zhuang §2.1.1, p. 5, L342); wrong guesses land in alerting decoys (Zhuang §2.2, p. 6, L482); DYNAT makes "typical attacker actions … obvious anomalies" (Zhuang §5, L802, [11]; Ward §6.1 "increase the likelihood of detecting anomalies"); NASR makes worms "easier to detect" (Zhuang §5, L849, [3]).
- *Slowing down to evade (tempo/rate)*: "An attacker could avoid triggering Düppel … by slowing the rate of attack. This causes loss of precision, but is likely preferable to triggering the defense" (Ward §5.18, PDF p. 248, L11894) — the only explicit speed-for-evasion trade in the seven; AVANT-GUARD traffic-rate triggers in PPS/BPS that an attacker can stay beneath (Ward §6.11, PDF p. 286–288, [142]); "staying under the radar" of IDS-driven movement (Ward §6.16, §6.18).
- *Detection-dependent MTDs are defeated by stealth*: Ward §5.1 (PDF p. 187), §5.10, §6.16; Cho §V-B "stealthy, undetected inside attackers are more serious threats" (L423); Cho §V-A "Stealthy attackers" as an attacker characteristic [3], [87] (not a metric).
- *Detection latency / dwell*: "attacks may succeed for a lengthy period of time before being detected, if at all" depending on mutation rate (Ward §3.11, PDF p. 77); the time gap between IDS trigger and network response (Ward §6.16, §6.18); privileges "maintained for a long time without being detected" (Zhuang §1, L43); APT expectation "to persist in our systems for a long time" (NITRD §1, L9); "worm propagation speed … indirectly increases the detection of attackers by earning more time to monitor" (Cho §VII-A, L617).
- *Passive vs active reconnaissance*: Jalowski §4.3 (p. 8, L197) — APTs "utilize Passive Reconnaissance to remain in the shadows"; Nmap-baseline ASP is "too naive" (§5, p. 9, L209). Jalowski's "Red Zones" (§4.1, p. 7, L163): defender mutation *frequency* is itself detectable by the attacker via traffic analysis.

**Tempo / rate / time quantities:** Attack(er) Productivity = mean attacker-task duration (Zaffarano §4.1; "how quickly an attacker can perform adversarial tasks" per Sengupta citing Taylor [126]); attack success productivity ΔA (Sengupta, Lei et al. [155]); CAIA cyber-attack inter-arrival rate (Sengupta §III-B-1, Debroy [68]); worm propagation speed (Cho); scan delay factor ×115 (Ward §6.15); Δt time to launch an attack (Zhuang); MTTC / MTTF / MTTSF (Cho); exposure time / time window (Ward §5.9, §5.15–5.16; NITRD §1.9); decision cycle time vs attacker (NITRD §1.11.2); change frequency vs scanner/worm propagation (NITRD §1.1.1).

**Probe / scan counts:** no survey defines a probe or scan *count as an output metric*. The nearest: Nmap-measured scanning overhead as a form of attack cost (Cho §VII-B, Kampanakis [93]); fraction of decoy nodes scanned (Cho §VII-B, Clark [36]); reduction in reconnaissance attempts (Sengupta §V-B-1, MORE [66]); ~99 % of scanning attempts thwarted (Sengupta §IV-B, OF-RHM [54]). "Number of probes" (Luo [108]) and "number of addresses scanned" (Carroll [25]) appear in Cho only as **input parameters** against which ASP is computed (Cho §IV-A, L288–290; §VIII-A, L691).

**Noise:** "noisy-rich (NR) cyber-attackers … who try to exploit all the vulnerabilities" (Sengupta §III-A-1, p. 8, L979–982, Jajodia et al. [58]) — an attacker *type*, not a metric. Elsewhere "noise" means defender-injected side-channel noise (Ward §3.12, §5.17–5.18) or a noisy attacker *view* (Sengupta Fig. 4 caption: exploration-surface shifting makes "sensing actions noisy or erroneous").

**Absent in all seven:** no metric named *attack intensity*, *dwell time* (as a measured quantity), *mean time to detect*, or *probes per unit time*. The words "intensity" and "dwell" do not occur in any of the seven sources (grep-verified).

## (c) Attempts / effort per compromise

- **Per-attempt success ratios**: Zaffarano Success = 1/|T| Σ ν(τ, success) over *attempted* tasks (Mission Success is "the number of attempted mission tasks that are successfully completed", Table 4); Zhuang's "success ratio of each attack" (≈50 % static → 16.2 % at interval 20, §4 p. 9) and CAG edge success probabilities (§3.2); Sengupta's 1/probability of the adversary's next new attack ([65]).
- **Attempt counts**: at most 1024 guesses to brute-force ASLR by clone-probing (Ward §4.1.14, RASLR [69]); brute-force failure counts driving detection (Ward §2.3); ncrack dictionary-attack success/failure (Zaffarano Table 2).
- **Effort / cost to the attacker**: attack cost and Nmap scanning overhead (Cho [5], [6], [93], [113], [147]); penalty in attack payoff (Cho [52], [91], [168], [177]; Sengupta [73]); AC and RoA (Cho, Alavizadeh [5], [6]); attackers' overhead (Cho [93]); attacker's workload (Cho, Farris & Cybenko [51]; Ward passim); attack effort and complexity (Cho [20]); COA (Sengupta §II-D-9); security ∝ 1/attacker cost (Sengupta [133]); D2 cost of attack action in R^A (Sengupta [62]); number of interruptions to reach the goal (Sengupta [147]); attack efficiency (Sengupta [76]); reconnaissance needed (Ward §6.19); area to search, per-edge effort, frequency of regaining privileges (Zhuang); attacker's effort to map the network (Zhuang [11]); no amortisation of development cost, number of distinct attacks needed, red-team difficulty, additional work effort (NITRD).
- No survey defines a ratio of *attempts per successful compromise*; it has to be composed from the per-attempt success rates above.

## (d) Reach / breadth

Confidentiality as "how many system components are compromised" (Cho [134]); Availability as "portion of system assets that are not compromised" (Cho [66], [134]); Controllability (Cho [134]); MTTC "to compromise an entire system" (Cho); attack surface (Cho, Jalowski, Sengupta); number of servers the defender controls in FlipIt (Sengupta [69]); number of interruptions from start to goal node (Sengupta [147]); coverage of attacker goal leaves (Sengupta [95]); number of attack paths toward decoy targets (Cho, Ge [57]); variety of targets available (Ward §5.15–5.16); "address distance" of vulnerable hosts from the scanner (Ward §6.15); how far the attacker moves forward, move-back probability, completed attacks reaching TargetDB, CAG path length (Zhuang); network visibility via nmap and "ability to maneuver within the network" (Zaffarano Table 2); fraction of systems on which an attack succeeds (NITRD §1.2.1); state-collision probability across nodes (Jalowski §4.1). No survey names a *network compromise ratio* as such; Cho's [134]-based Confidentiality/Availability pair is the nearest (count and complement of compromised components).

## (e) Attacker behavioural variety or unpredictability

No survey defines a metric of **attacker** behavioural variety. Every "unpredictability" / entropy / periodicity / diversity metric in the seven measures the **defender's** configuration (Cho unpredictability [66], [110], [145]; Sengupta ensemble entropy [137], [124]; Ward entropy bits; NITRD high-entropy distribution). Attacker-variety content is typological or qualitative:
- Learning by attackers (Cho [181]; Jalowski §2.3) — the only attacker-adaptation *metric*.
- Attacker types: script kiddies / experienced hackers / organized criminals / nation states (Cho §VI-A-3, Manadhata [113]); noisy-rich attackers (Sengupta [58]); slow vs fast-evolving adversary (Sengupta [65]); irrational attacker modelled from historical traces (Sengupta [63]); naive vs persistent bots (Ward §6.14, [145]); attacker profiles in Cho §V-A (persistent, adaptive, stealthy, incentive-driven).
- Strategy multiplicity as a gap: "few scenarios have considered multiple strategies" (Cho §V-D); "smart, adaptive attackers who understand the MTD scheme" (Jalowski §4.3); an attacker who "can simply wait for a scanned VM to come back into rotation" (Ward §5.15–5.16).
- Zaffarano's attacker model deliberately runs kill-chain-stage tasks "not necessarily in order" (p. 7–8) — a design choice, not a measure.

## (f) Attacker giving up / disengagement

Mentioned only as mechanism rationale; **no metric** in any of the seven:
- Sengupta §II-D-8 (p. 5, L594–597), Tarpit: "adversaries will give up on a target if it takes too long to achieve the defined goal".
- NITRD §1.6 (L615): attackers "slowed down (probably confused or discouraged)" by decoys; §1.6.1 (L641) "significantly slow down and frustrate the attackers".
- Ward §3.8 (PDF p. 68), RedHerring: decoy disinformation "may frustrate further attempts to move beyond"; Ward §6.15 (PDF p. 304), RDS "could slow down an insider reconnaissance attack enough that it halts further attacks" (halting there is by defender isolation, per the threat model at PDF p. 301).
- Cho §VI-A (L508–510): game theory's rationality assumption fails for attackers "not stimulated by the incentives" — about irrationality, not disengagement.

## (g) Acronyms recurring in ≥ 2 of the seven papers

| acronym | expansion (as written) | papers | note |
|---|---|---|---|
| ASP | Attack Success Probability | cho2020, jalowski2026 | Sengupta and Zhuang use the phrase without the acronym |
| QoS | Quality of Service / Quality-of-Service | cho2020, jalowski2026, sengupta2020, ward2018, ghosh2009 | a metric family in Cho, Jalowski, Sengupta, Ward (§6.17 constraints); in NITRD only as a commercial service / provisioning term (§1.5, L555, L579; §1.9, L909) |
| CIA | Confidentiality, Integrity, Availability | jalowski2026, sengupta2020, ghosh2009 | Cho and Zaffarano spell the three out without the acronym |
| ROI | Return on Investment / "Return of Investment" | sengupta2020 (NICE [88], defender countermeasure ROI), ghosh2009 (attack ROI) | different sides of the ledger |
| RoA / ROI-like | Return on Attack | cho2020 only (Alavizadeh) | listed for contrast with ROI |
| AC | Attack Cost (cho2020, Alavizadeh) vs Access Complexity (sengupta2020, CVSS) | cho2020, sengupta2020 | **collision**: same letters, different quantities |
| ETE | end-to-end (delay / packet delivery time) | cho2020, sengupta2020 | |
| HFM / LFM | High / Low Frequency Mutation | cho2020, sengupta2020 | Al-Shaer et al. RHM |
| RHM / OF-RHM | (OpenFlow) Random Host Mutation | cho2020, sengupta2020, ward2018 | technique names that recur with their overhead metrics (address space, flow table) |
| HARM | Hierarchical Attack Representation Model / Method | cho2020, sengupta2020 | Sengupta writes "Method" |
| CKC | Cyber Kill Chain | cho2020, sengupta2020 | Ward uses a five-phase variant without the acronym; Zaffarano spells it out (seven stages) |
| APT | Advanced Persistent Threat | cho2020, jalowski2026, sengupta2020, zaffarano2015 | not a metric; Ward (APTs spelled out in §6.15 only) and NITRD do not use the acronym |
| IDS | Intrusion Detection System | all but zaffarano2015 | not a metric |
| MTTC, MTTF, MTTSF, DSP | — | cho2020 only | Jalowski spells MTTC/MTTF out; no other paper uses them |
| IPD, PPS, BPS | inter-packet delay; packets / bits per second | ward2018 only | |
| COA, CAIA, MOE, IM, ARM, NR, ΔM, ΔA | — | sengupta2020 only | |

Two terminology hazards worth recording: (1) **AC** means Attack Cost in Cho and Access Complexity in Sengupta; (2) **Productivity vs Success**: Zaffarano 2015 defines Productivity as mean task duration ("how quickly") and Success as the fraction of attempted tasks completed, but Sengupta's relay of Taylor et al. [126] swaps them ("Mission Success, i.e., the rate at which mission tasks are completed, and Mission Productivity, i.e., how often are mission tasks successful"), and Cho's DSP paraphrase of [173] ("the rate at which tasks are executed and completed") merges them. Cite Zaffarano 2015 Table 4 directly.
