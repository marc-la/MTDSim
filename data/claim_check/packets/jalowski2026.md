# Packet: jalowski2026

13 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0019 (prose, L312) tier H
*Introduction*

> Most tests run in simulation, against attacker models far simpler than an APT [cho2020, jalowski2026], and how MTD is measured to perform depends on how the attacker is implemented [hong2018].

Context before: [U0017 cites ghosh2009nitrd,zhuang2012] MTD aims to shift the advantage of time from the attacker to the defender [ghosh2009nitrd, zhuang2012]. [U0018 cites alshamrani2019] MTD has been proposed as a defence against APTs [alshamrani2019], yet it is rarely tested against one.

Context after: [U0020] This gap motivates the research question of this dissertation: [U0021] partopsep=0pt] \itshape How does MTD perform against APT attackers?

### U0210 (prose, L2253) tier V2
*Literature review > MTD evaluation > Metrics* · drafting trail: session-drafted, redrafted

> Each evaluation chooses its own, so MTD mechanisms cannot be compared across evaluations [jalowski2026].

Context before: [U0208 cites cho2020] Efficiency metrics measure the cost of an attack or of MTD [cho2020]. [U0209 cites cho2020] No standard set of metrics exists [cho2020].

Context after: [U0211 cites hong2018] ASP, MTTC and NCR are all computed from what the attacker does, so their values depend on how the attacker is implemented [hong2018]. [U0212] MTD that is effective against one attacker may therefore not be effective against an APT attacker.

### U0226 (prose, L2866) tier V2
*Literature review > MTD attacker models* · drafting trail: session-drafted, redrafted

> Two surveys of MTD find that MTD attacker models lack properties of an APT attacker [cho2020, jalowski2026].

Context before: [U0224 cites cho2020] Simulation results do not transfer directly to a real network, which no simulation fully captures [cho2020]. [U0225] This dissertation uses MTDSim's flexibility to run an APT attacker model through its existing attack actions (Chapter <ch:attacker-model>).

Context after: [U0227] This section checks whether recent MTD attacker models still lack them. [U0228] sets out eight properties an MTD attacker model needs to model an APT attacker, and Section <subsec:recent-threat-models> scores three recent MTD attacker models on them.

### U0231 (prose, L2952) tier V2
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: session-drafted, redrafted

> The two surveys add the other four: choice of attack strategy, cost--benefit reasoning, learning and deployment-strategy awareness [cho2020, jalowski2026].

Context before: [U0229] An MTD attacker model needs eight properties to model an APT attacker. [U0230 cites nist2011sp80039,alshamrani2019] The APT definition of Section <subsec:apt> gives four: the APT attacker pursues its objective over an extended period (campaign persistence), uses different techniques after the foothold for different objectives (objective-specific behaviour), adapts to the defender's resistance (adaptivity) and moves low and slow to avoid detection (detection avoidance) [nist2011sp80039, alshamrani2019].

Context after: [U0232] This dissertation synthesises the eight properties in Table <tab:attacker-properties>. [U0233 cites cho2020] Cho et al. name three limitations of MTD attacker models [cho2020].

### U0237 (prose, L2963) tier H
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker*

> Jalowski et al. call the attacker model ``the most glaring flaw in the MTD literature'' [p. 8 jalowski2026].

Context before: [U0235] Second, they lack choice of attack strategy: few evaluations let the attacker choose among several attack strategies. [U0236] Third, they lack cost--benefit reasoning and deployment-strategy awareness: the attacker is seldom modelled as a rational actor, or as one that exploits how the MTD works.

Context after: [U0238] They find the same lack of learning and deployment-strategy [U0239 cites jalowski2026] awareness: an APT attacker learns the MTD's deployment patterns over time and looks for the logic of the deployment strategy [jalowski2026].

### U0239 (prose, L2966) tier V2
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: session-drafted, redrafted

> awareness: an APT attacker learns the MTD's deployment patterns over time and looks for the logic of the deployment strategy [jalowski2026].

Context before: [U0237 cites jalowski2026] Jalowski et al. call the attacker model ``the most glaring flaw in the MTD literature'' [p. 8 jalowski2026]. [U0238] They find the same lack of learning and deployment-strategy

Context after: [U0240 cites jalowski2026] They add detection avoidance: MTD is typically tested against active scanning, such as Nmap, while an APT attacker uses passive reconnaissance to stay hidden [jalowski2026].

### U0240 (prose, L2968) tier H
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: session-drafted, redrafted

> They add detection avoidance: MTD is typically tested against active scanning, such as Nmap, while an APT attacker uses passive reconnaissance to stay hidden [jalowski2026].

Context before: [U0238] They find the same lack of learning and deployment-strategy [U0239 cites jalowski2026] awareness: an APT attacker learns the MTD's deployment patterns over time and looks for the logic of the deployment strategy [jalowski2026].

Context after: 

### U0246 (table-row, L3078, tab:attacker-properties) tier V2
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: session-drafted, redrafted

> 5 | Detection avoidance | moves low and slow and chooses techniques an intrusion detection system (IDS) does not flag, such as passive reconnaissance | [alshamrani2019, jalowski2026]

Context before: [U0244 cites cho2020] 3 | Choice of attack strategy | chooses among several sequences of techniques toward the same objective | [cho2020] [U0245 cites cho2020,nist2011sp80039] 4 | Adaptivity | chooses its next technique in response to an MTD disruption | [cho2020, nist2011sp80039]

Context after: [U0247 cites cho2020] 6 | Cost--benefit reasoning | chooses each technique by weighing its cost against its benefit | [cho2020] [U0248 cites cho2020,jalowski2026] 7 | Learning | keeps the patterns it observes in past MTD deployments, and uses them to choose later techniques | [cho2020, jalowski2026]

### U0248 (table-row, L3081, tab:attacker-properties) tier V2
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: redrafted

> 7 | Learning | keeps the patterns it observes in past MTD deployments, and uses them to choose later techniques | [cho2020, jalowski2026]

Context before: [U0246 cites alshamrani2019,jalowski2026] 5 | Detection avoidance | moves low and slow and chooses techniques an intrusion detection system (IDS) does not flag, such as passive reconnaissance | [alshamrani2019, jalowski2026] [U0247 cites cho2020] 6 | Cost--benefit reasoning | chooses each technique by weighing its cost against its benefit | [cho2020]

Context after: [U0249 cites cho2020,jalowski2026] 8 | Deployment-strategy awareness | predicts and leverages which mechanism the deployment strategy deploys next, and when | [cho2020, jalowski2026]

### U0249 (table-row, L3082, tab:attacker-properties) tier V2
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: redrafted

> 8 | Deployment-strategy awareness | predicts and leverages which mechanism the deployment strategy deploys next, and when | [cho2020, jalowski2026]

Context before: [U0247 cites cho2020] 6 | Cost--benefit reasoning | chooses each technique by weighing its cost against its benefit | [cho2020] [U0248 cites cho2020,jalowski2026] 7 | Learning | keeps the patterns it observes in past MTD deployments, and uses them to choose later techniques | [cho2020, jalowski2026]

Context after: 

### U0299 (prose, L3566) tier V2
*Literature review > Research gap* · drafting trail: session-drafted, from-memory, redrafted

> Two surveys find that MTD attacker models lack properties of an APT attacker [cho2020, jalowski2026], and the three recent MTD attacker models scored in Section <subsec:recent-threat-models> still lack them.

Context before: [U0297] The attacker models of Masud et al. and Kim et al., which this dissertation expected to be the most likely to have the properties, have none in full. [U0298] An MTD evaluation's result depends on its attacker model: the attacker model decides which deployment strategy is optimal (Section <subsec:defence-modelling-approaches>) and how effective MTD is (Section <subsec:mtd-metrics>).

Context after: [U0300] How MTD performs against APT attackers therefore remains unmeasured. [U0301] This dissertation recovers the behaviour of APT attackers from CTI by attack profiling (Section <subsec:profiling>) and executes it as an APT attacker model inside MTDSim (Chapter <ch:attacker-model>).

### U0791 (prose, L9009) tier H
*Discussion > Implications for MTD evaluation*

> Section <subsec:mtd-metrics> found that MTD mechanisms cannot be compared across evaluations because each evaluation chooses its own metrics [jalowski2026], and that metric values depend on how the attacker is implemented [hong2018].

Context before: [U0789] An MTD evaluation should therefore test a learned deployment strategy against an attacker model other than the one it was trained against, beside the random deployment strategy over the same MTD mechanisms, which shows what the learning adds. [U0790] On effectiveness metrics, the two attackers rank the MTD mechanisms and deployment strategies differently, at every deployment interval.

Context after: [U0792] At the default deployment interval of 200 s, the two attackers' rankings on NCR reduction are uncorrelated ($\rho = 0.01$; Section <subsec:eff-cross-arm>). [U0793] Service diversity, for example, reduces the baseline attacker's NCR by 92 % and the APT attacker model's by 36 %, on the same networks (Table <tab:eff-cross-arm>).

### U0841 (prose, L9365) tier H
*Discussion > Threats to validity* · drafting trail: redrafted

> That MTD attacker models in general lack the properties of an APT attacker is the finding of the two surveys [cho2020, jalowski2026].

Context before: [U0839] Nor did we read the attacker models' code, which may behave differently from their papers, so the threat remains. [U0840 cites cho2020] The comparison covers only four attacker models: the three MTD attacker models we chose (Section <subsec:recent-threat-models>) include none from game theory, the dominant MTD modelling approach [cho2020].

Context after: [U0842] The confidence intervals of NCR reduction treat each run as independent. [U0843] Our design violates this assumption, because at each seed the four attack profiles run on the same network.
