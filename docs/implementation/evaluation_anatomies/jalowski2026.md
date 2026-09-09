# jalowski2026 — what the critique says about MTD evaluation

Source read: `docs/sources/lit_review/3_1_jalowski2026rethinking.md` (md; line locators "L<n>") and `docs/sources/lit_review/original/3.1_jalowski2026rethinking.pdf` (13-page PDF; PDF page = journal page, given as "p<n>" using the md's "n of 13" markers and confirmed for Figures 2–3 by rendering p7–p8). Full citation: Jalowski, Zmuda, Rawski, Rekosz, "Rethinking the Security Assurances of MTD: A Gap Analysis for Network Defense", *Future Internet* 2026, 18, 89 (L3–L5, L25).

Paper type: CRITIQUE / POSITION / GAP ANALYSIS. **No experimental portion of its own** — "Data Availability Statement: No new data were created or analyzed in this study." (L235; p10). Template sections A–F therefore do not apply; nothing is recorded under them.

Paper's own purpose (L39; p2): "we organize the analysis into three dimensions: (i) security of core design principles (what/when/how to move) under realistic attacker models, (ii) implementation-level risks such as metadata leakage, forward/backward secrecy, and vulnerabilities introduced by MTD code, and (iii) operational challenges across the network life cycle". And (L45; p3): "The presented paper moves from 'survey and taxonomy' found in the prior literature to gap analysis and actionable research directions. In particular, it emphasizes security assurance, deployment practicality, and attacker realism".

---

## 1. Criticisms of how MTD evaluations are conducted

### 1a. Comparability / standards (the "isolated worlds" charge)
- "As recent surveys in this field have pointed out [5–7], there are no reliable and agreedupon methods for comparing two different techniques against one another. Surprisingly, there is also no consensus regarding how to measure the security of newly proposed strategies. Instead, many authors propose their own idea on how to test the effectiveness of MTD strategies, using their own metrics and frameworks ... These, however, fall short and fail to reach a broader audience. This all contributes to the overall information chaos surrounding MTD." (L35; p2)
- "Many existing articles on this security paradigm focus too narrowly on a single, often very specific topic, thereby overlooking the wider context" (L35; p2).
- Sec. 3.1 "The Standardization and Comparison Gap" (L121–L125; p5): "MTD strategies effectively exist in 'isolated worlds,' evaluated predominantly through ad hoc methods provided by their own creators. This lack of prevailing standards or metrics has led to significant confusion in the field." (L123) Framework proposals "often remain siloed within specific technologies" — [13] topology shuffle + software diversity, [14] SDN, [15] entropy, [16]–[20] SDR in cloud — "While these individual approaches are not necessarily incorrect, the lack of a universal metric prevents any objective cross-technique comparison, leaving a critical gap in the holistic evaluation of MTD efficacy." (L125)
- "it is currently impossible to compare different techniques meaningfully" (L119; p5).
- "to the best of our knowledge, no common framework for measuring MTD security currently exists ... The absence of such a standard framework is one of the main gaps preventing the creation of standardized solutions." (L115; p5)

### 1b. Metrics
- On ASP specifically (L209; p9): "existing metrics are far from perfect. They are commonly very hard, if not impossible, to properly measure outside of a controlled lab environment. A perfect example of this is ASP, which may be too naive, as it can only describe effectiveness against one, often very specific, attack, but it does not consider any other possibilities. To make matters worse, it is commonly calculated using simple Nmap scans [52] as a baseline, an issue that has already been discussed in this article. Furthermore, many authors introduce their own metrics, which adds to the overall confusion. Although this problem has already been raised in existing surveys [5–7], very little has been done to date to remediate this problem."
- Metric catalogues it re-states from the surveys (Sec. 2.3, L75–L113; p4–p5): Sengupta [5] grouping — Qualitative (security of individual defenses / of the ensemble; "very few works ... take a holistic approach") vs Quantitative (CIA metrics, Risk metrics, Attack graph/tree, Policy conflict analysis); Cho [6] grouping — attacker/defender pairs: ASP/DSP, Attack/Defense utility, MTTC/MTTF, Learning, Attack surface and system security ("degree of vulnerability"), Attack/defense cost.
- Sec. 3.2 (L137; p6): "the majority of the literature, including surveys on intelligent algorithms for optimization [25], tends to focus on defense costs and performance rather than rigorous, adversarial security modeling."
- Conclusions (L223; p9): "Existing approaches are fragmented and often context-specific, which prevents meaningful comparisons across techniques and hinders the establishment of best practices."

### 1c. Attacker models / threat modelling
- Sec. 3.2 "The Threat Modeling and Comprehensive Analysis Gap" (L127–L137; p5–p6): "As pointed out in [7], many papers entirely lack threat models or provide incomplete ones at best. This indicates a widespread failure to conduct a comprehensive analysis of an MTD approach's impact on the overall system security." (L129) "Research often focuses on the mechanism itself rather than the attacker's counterresponse." (L131) Exceptions named: [21] "IP-shuffling against sophisticated, network-aware attackers", [22] "models to abstract attacker behavior during different phases", [23] multidimensional attack graphs, [24] attack-surface impact (L131–L137). "This absence of a standardized threat-centric approach directly necessitates the gap analysis provided in Section 4." (L137)
- Sec. 4.3 "Threat Modeling: Deconstructing Attacker Assumptions" (L189–L197; p8): "The most glaring flaw in the MTD literature is the ill-defined attacker models [7], which are often too simplistic or based on completely unrealistic assumptions. By applying Shostack's four-step framework [50], we can expose the limitations of existing schemes." (L191)
- Location dependence / insider gap (L193; p8): "MTD effectiveness is highly location-dependent. While it may defeat an external eavesdropper (Attacker A), it has no effect on an attacker who has gained privilege escalation on an endpoint (Attacker C). Given that phishing and stolen credentials remain primary vectors [51], this 'Insider Threat Gap' is a critical shortcoming."
- Active scanning as test adversary (L197; p8): "testing against active scanning (Nmap [52]) is too naive. Advanced Persistent Threats (APTs) [53,54] utilize Passive Reconnaissance [55] to remain in the shadows and learn mutation patterns over time. To move forward, research must shift toward defending against smart, adaptive attackers [6] who understand the MTD scheme and look for the mathematical logic behind the movement."
- Sec. 4.1 attacker-side observations that bear on what an evaluation should test: state-collision in finite parameter spaces — "as the number of protected nodes increases, a small parameter space guarantees state repetition ... If an attacker compromises one state, the probability that another node resides in that same state is high. Consequently, low-entropy MTD schemes do not truly 'move' the target; they merely rotate it within a predictable set of vulnerabilities." (L153; p6); mutation-frequency as a beacon — "assigning higher mutation frequencies to critical 'Red Zones' inadvertently signals asset value to an observer. An intelligent attacker can utilize traffic analysis to identify which segments are mutating fastest" (L163; p7, Figure 2 L165); metadata shadow — "If an attacker is intelligent and attentive, unusual protocol properties or timing patterns may emerge as side-channels that remain invariant across mutations. Without addressing this 'metadata shadow,' address mutation provides only a facade of security." (L167; p7); forward/backward secrecy — "If any mathematical correlation exists between MTD states, a skilled attacker can predict future movements or decipher past communications." (L169; p7); MTD code as attack surface — "MTD components must be factored into the attack surface, as the controller itself becomes a structural single point of failure" (L169; p7).

### 1d. Experiments / testing practice
- Discussion (L201; p8): "more work needs to be done in rethinking approaches to testing it in realistic ways, simulating how actual attackers might approach breaching the network."
- Sec. 4.2 Configuration and Tuning (L175; p7): "There is a significant lack of empirical guidelines for setting parameters like mutation intervals, leading to ad hoc, sub-optimal deployments."
- Sec. 4.2 (L173; p7): "For MTD to achieve widespread adoption, it must coexist with the entire network life cycle—a requirement currently missing from most design-focused papers."

### 1e. Claims
- "Relying on 'security by obscurity' [10] is a fatal error" (L169; p7).
- "Although security metrics are not directly tied to the security of any MTD scheme, they remain an important topic worth exploring" (L209; p9).
- No explicit criticism of over-claiming from data beyond the ASP-against-one-attack point at L209.

---

## 2. Prescriptions — what a sound evaluation should include

### 2a. The four metric guidelines (the paper's only enumerated prescription list), verbatim (L209–L217; p9)
"The following guidelines should be fulfilled by any useful security metrics:
- Possibly easy to establish, using data that can be obtained both during simulations and from the normal runtime of the network;
- Should be generic enough so that possibly many, or all, schemes can be evaluated using it;
- As a baseline, it should compare the MTD scheme to a state-of-the-art system, protected using the best available methods;
- Using common security mechanisms and terminology to evaluate the workings of the scheme, making it understandable even to people who are not experts in the MTD field."

### 2b. Threat modelling
- "robust threat modeling is indispensable for evaluating the true security benefits of MTD. Effective models must account for attacker capabilities, realistic attack vectors, and adaptive strategies, moving beyond the simplistic assumptions that currently dominate the literature." (L223; p9)
- Use "Shostack's four-step framework [50]" (L191; p8) — the four steps are not enumerated in the paper (not stated).
- "the paper emphasizes the need for more sophisticated attacker models and comprehensive threat modeling to ensure that MTD schemes meet their intended security objectives." (L45; p3)
- Test against "smart, adaptive attackers [6] who understand the MTD scheme" and against passive reconnaissance rather than Nmap scans (L197; p8).
- Consider attacker location: the evaluation should cover positions where MTD "has no effect" (Attacker C) not only the external eavesdropper (L193; p8).

### 2c. Testing realism
- "simulating how actual attackers might approach breaching the network" (L201; p8); "employ the services of pentesters, or so-called 'ethical hackers' ... probing it with a different mindset than the defenders" (L207; p9).

### 2d. Design-parameter reporting
- Distinguish "infinite and finite parameter spaces" for the moving element (L153; p6); provide "empirical guidelines for setting parameters like mutation intervals" (L175; p7).
- The three design questions (what / when / how to move, L53–L59; p3) are the paper's organising axis for security trade-offs: "Each decision introduces unique security trade-offs that influence both resilience and operational performance." (L223; p9)

### 2e. Metrics for comparison
- "Properly defined evaluation methods are essential to correctly measure, rank, and identify promising MTD schemes." (L209; p9)
- "the development of standardized, comprehensive security metrics is urgently needed." (L223; p9)
- Baseline choice: the comparison baseline should be "a state-of-the-art system, protected using the best available methods" (L215; p9) — i.e. not an undefended system. (Recorded; not evaluated.)

---

## 3. The three attacker primitives (Figure 3, p8; caption L195)
The paper names three attackers by network position, not by capability class:
- **Attacker A** — "in point A, an attacker can read outbound traffic" (positioned on the link outward from the router; figure p8). Text: "an external eavesdropper (Attacker A)" that MTD "may defeat" (L193).
- **Attacker B** — "in B, an attacker can read traffic between endpoints and router" (positioned on the LAN side of the router; figure p8). No separate claim is made about B in the text (not stated beyond the caption).
- **Attacker C** — "in C is an attacker who gained privilege escalation on one of the endpoints" (positioned at an endpoint; figure p8). Text: MTD "has no effect on" C; this is the "Insider Threat Gap" (L193).
Figure caption verbatim (L195): "Simplified fragment of network. Letters signify different attackers—in point A, an attacker can read outbound traffic, in B, an attacker can read traffic between endpoints and router, and in C is an attacker who gained privilege escalation on one of the endpoints."

Related attacker-behaviour primitives the paper names elsewhere (not labelled as a triple by the paper): active scanning (Nmap) vs Passive Reconnaissance vs "learn mutation patterns over time" (L197; p8); traffic analysis of mutation frequency (L163); metadata/timing side-channels (L167); state prediction via inter-state correlation (L169).

---

## 4. What the paper does NOT contain (recorded so it is not assumed)
- No experiment, simulation, dataset, network size, replication count, or statistical procedure (L235).
- No definition of the Shostack four steps.
- No worked example of applying its four metric guidelines.
- No numbers on how many surveyed papers lack threat models (it cites [7] for the claim, L129).
- Its own summary of the three MTD surveys' metric taxonomies is a re-statement of [5] and [6] (L77–L113), not new material.

---

## 5. Summary of the prescriptive content (record, not evaluation)
1. A metric must be computable from simulation data *and* runtime data, be scheme-generic, be benchmarked against a best-available-defence baseline, and be expressed in common security terminology (L211–L217; p9).
2. The threat model must be explicit, must state attacker location (A/B/C), attacker capability (passive reconnaissance, learning of mutation patterns), and attacker adaptivity, and must not reduce to Nmap scanning (L191–L197; p8; L223; p9).
3. ASP against a single specific attack is named as the exemplar of a naive metric (L209; p9).
4. Comparability across schemes is the field's central deficit (L35, L119, L123–L125, L223).
