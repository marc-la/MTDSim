# Packet: masud2025

6 units cite it; 1 more name its first author without citing it.

## Units that cite it

### U0215 (table-row, L2520, tab:mtd-metrics) tier H
*Literature review > MTD evaluation > Metrics* · drafting trail: session-drafted, redrafted

> Effectiveness | Attack success probability (ASP) [evans2011, cho2020, kim2026, masud2025]; mean time to compromise (MTTC) [mcqueen2006, cho2020, zhang2023, ho2024]; attack path variation, number and exposure [hong2018]; attack surface [manadhatawing2011tse]; attack utility [cho2020] | Defence success probability [cho2020]; attack actions blocked [brown2023]; network compromise ratio (NCR) [zhang2023]; risk [alavizadeh2022, ho2024]; mitigation factor [alavizadeh2022]; time since last MTD [ho2024, tay2024]

Context before: [U0214] | Attacker-side | Defender-side

Context after: [U0216 cites cho2020,alavizadeh2022,cremonini2005,mendonca2023] Efficiency | Attack cost [cho2020, alavizadeh2022]; return on attack (RoA) [cremonini2005, alavizadeh2022] | Defence cost and system performance overhead [cho2020, mendonca2023]; quality of service [cho2020, mendonca2023]

### U0252 (prose, L3228) tier V2
*Literature review > MTD attacker models > Recent MTD attacker models* · drafting trail: session-drafted, from-memory, redrafted

> The other two are the attacker models of two recent MTD evaluations that describe their attacker by the Cyber Kill Chain or ATT | CK, by Masud et al. [masud2025] and Kim et al. [kim2026].

Context before: [U0250] This section scores three MTD attacker models, published from 2023 to 2026, on the eight properties an MTD attacker model needs to model an APT attacker (Table <tab:attacker-properties>). [U0251 cites brown2023,zhang2023] The first is MTDSim's baseline attacker, described in Section <subsec:attacker-model> [brown2023, zhang2023].

Context after: [U0253] This dissertation chose them because it expects an attacker model described this way to be the most likely to have the [U0254] This dissertation scores each attacker model on each property from its paper, by predicates taken from each definition in Table <tab:attacker-properties> (Appendix <app:clause-tests>), with one of three marks.

### U0262 (table-row, L3371, tab:attacker-cross-section) tier H
*Literature review > MTD attacker models > Recent MTD attacker models* · drafting trail: session-drafted, redrafted

> Masud et al. [masud2025] | 2025 | \propstandin | \propnone | \propnone | \propnone | \propnone | \propnone | \propnone | \propnone

Context before: [U0260] Attacker model | Year | 1\newline Pers. | 2\newline Obj. | 3\newline Strat. | 4\newline Adapt. | 5\newline Detect. | 6\newline Cost | 7\newline Learn. | 8\newline Deploy. [U0261 cites brown2023,zhang2023] Baseline attacker [brown2023, zhang2023] | 2023 | \propmet | \propnone | \propstandin | \propstandin | \propnone | \propnone | \propnone | \propnone

Context after: [U0263 cites kim2026] Kim et al. [kim2026] | 2026 | \propstandin | \propnone | \propnone | \propnone | \propstandin | \propnone | \propnone | \propnone

### U0272 (prose, L3412) tier V2
*Literature review > MTD attacker models > Recent MTD attacker models* · drafting trail: session-drafted, redrafted

> \paragraphMasud et al. Masud et al. use an analytical model to evaluate an MTD that combines shuffle, diversity and redundancy on an Internet-of-Things cloud network [masud2025].

Context before: [U0270] It has no detection avoidance: it scans actively and does nothing to avoid an intrusion detection system (IDS). [U0271] It has no deployment-strategy awareness: nothing in it uses which mechanism deploys next or when it deploys.

Context after: [U0273] Their attacker model is the set of attack paths through a graph model of that network, from the Internet to a target database. [U0274] At each deployment interval, the analytical model computes each attack path's success probability, cost and RoA, before and after the MTD deploys.

### U0279 (prose, L3423) tier H
*Literature review > MTD attacker models > Recent MTD attacker models* · drafting trail: session-drafted, redrafted

> The paper also says its attackers prioritise vulnerabilities by RoA and adapt to new flaws [p. 7 masud2025], but no step of the analytical model does either.

Context before: [U0277] It has no adaptivity: its attack paths are recomputed after each MTD deployment, but no next technique is chosen from them. [U0278] It has no cost--benefit reasoning: it computes each attack path's cost and RoA, but no choice depends on them.

Context after: [U0280] It has no objective-specific behaviour: every attack path leads to one objective, the database, and nothing follows once it reaches it. [U0281] It has no detection avoidance: the analytical model has no IDS for an attack path to avoid.

### U0758 (table-row, L8870, tab:fidelity-verdict) tier H
*Discussion > APT attacker model versus MTD attacker models* · drafting trail: session-drafted, redrafted

> Masud et al. [masud2025] | 2025 | \propstandin | \propnone | \propnone | \propnone | \propnone | \propnone | \propnone | \propnone

Context before: [U0756] Attacker model | Year | 1\newline Pers. | 2\newline Obj. | 3\newline Strat. | 4\newline Adapt. | 5\newline Detect. | 6\newline Cost | 7\newline Learn. | 8\newline Deploy. [U0757 cites brown2023,zhang2023] Baseline attacker [brown2023, zhang2023] | 2023 | \propmet | \propnone | \propstandin | \propstandin | \propnone | \propnone | \propnone | \propnone

Context after: [U0759 cites kim2026] Kim et al. [kim2026] | 2026 | \propstandin | \propnone | \propnone | \propnone | \propstandin | \propnone | \propnone | \propnone

## Units that name the author without citing

### U0297 (prose, L3478) cites nothing

> The attacker models of Masud et al. and Kim et al., which this dissertation expected to be the most likely to have the properties, have none in full.
