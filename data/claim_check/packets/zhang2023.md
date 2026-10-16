# Packet: zhang2023

23 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0062 (prose, L733) tier H
*Background > MTDSim*

> Every attack action and every deployment takes simulated time, counted in seconds [zhang2023].

Context before: [U0061 cites brown2023] MTDSim simulates an attacker and MTD on one network, to evaluate MTD mechanisms singly and in combination [brown2023].

Context after: [U0063] Figure <fig:mtdsim-model> draws the simulator's three modules: the attacker, the network and MTD. MTD deploys its mechanisms at intervals, and each deployment reconfigures part of the network and disrupts the attacker. [U0064] The attacker observes part of the network and compromises hosts in it.

### U0082 (prose, L816) tier H
*Background > MTDSim > MTD mechanisms and deployment strategies*

> A deployment is one run of one mechanism, and takes from 20 s to 110 s to complete, depending on the mechanism [zhang2023].

Context before: [U0080] MTDSim deploys seven MTD mechanisms: five shuffles, two diversities, and no redundancy (Table <tab:defence-mechanisms>). [U0081] Each reconfigures one part of the network: the host layer, the service layer or the users' credentials.

Context after: 

### U0083 (caption, L821, tab:defence-mechanisms) tier H
*Background > MTDSim > MTD mechanisms and deployment strategies*

> The seven MTD mechanisms, from the pool of Brown [brown2023], added to by Zhang [zhang2023], by the part of the network each reconfigures.

### U0093 (prose, L852) tier H
*Background > MTDSim > MTD mechanisms and deployment strategies*

> The random, alternative and single deployment strategies follow a schedule, so they are proactive [zhang2023].

Context before: [U0092] A deployment strategy decides which mechanism is deployed, and when (Table <tab:deployment-strategies>).

Context after: [U0094 cites tay2024] MTDShield is a reinforcement-learning agent [tay2024]. [U0095] At each interval it reads the network's security metrics and the attacker's current attack action, and deploys one of four mechanisms (complete topology shuffle, IP shuffle, OS diversity or service diversity) or none; if 2 000 s pass without a deployment, one is forced.

### U0100 (caption, L870, tab:deployment-strategies) tier H
*Background > MTDSim > MTD mechanisms and deployment strategies*

> The four deployment strategies: three from Zhang [zhang2023] and MTDShield, the reinforcement-learning agent of Tay [tay2024].

### U0110 (prose, L935) tier H
*Background > MTDSim > Baseline attacker* · drafting trail: session-drafted

> A run ends when the attacker compromises more than 80 % of the hosts [zhang2023], compromises a target host in the targeted scenario, or can discover no new host.

Context before: [U0108 cites brown2023,hutchins2011] It follows a fixed procedure of six attack actions, modelled on the Cyber Kill Chain [brown2023, hutchins2011]: it scans for hosts, enumerates one, scans its ports, exploits its vulnerabilities, brute-forces its accounts, and scans the neighbours of each host it compromises (Figure <fig:attacker-model>). [U0109] The attacker follows one of two attack scenarios (Table <tab:attacker-objectives>).

Context after: 

### U0122 (prose, L984) tier H
*Background > MTDSim > Baseline attacker*

> An exploit of a vulnerability it has exploited before takes half the time [zhang2023].

Context before: [U0120 cites tay2024code] Scanning for hosts, enumerating a host and scanning a host's neighbours each take 5 s, scanning its ports 25 s and brute force 20 s [tay2024code]. [U0121 cites brown2023] An exploit takes 15 s times one minus the vulnerability's attack complexity, which lies between 0.4 and 1 [brown2023], so from 0 to 9 s.

Context after: [U0123] A host-layer deployment disrupts the attacker during any attack action and sends it back to scanning hosts, because the host it was on may have moved. [U0124 cites brown2023] A service-layer deployment disrupts it only while it scans ports, exploits or brute-forces, and sends it back to scanning the same host's ports [brown2023].

### U0126 (prose, L993) tier H
*Background > MTDSim > Baseline attacker*

> Each disruption costs the attacker a confusion penalty of about 20 s [zhang2023].

Context before: [U0124 cites brown2023] A service-layer deployment disrupts it only while it scans ports, exploits or brute-forces, and sends it back to scanning the same host's ports [brown2023]. [U0125] A user shuffle disrupts only brute force, and sends it to exploit instead.

Context after: [U0127 cites zhang2023] A deployment never takes back a compromised host or a stolen credential [zhang2023]; the attacker loses only the progress it must repeat, and a topology shuffle also rebuilds its visible subgraph. [U0128] The earlier MTDSim studies ran these three modules in the configurations of Table <tab:lineage-configurations>.

### U0127 (prose, L994) tier H
*Background > MTDSim > Baseline attacker*

> A deployment never takes back a compromised host or a stolen credential [zhang2023]; the attacker loses only the progress it must repeat, and a topology shuffle also rebuilds its visible subgraph.

Context before: [U0125] A user shuffle disrupts only brute force, and sends it to exploit instead. [U0126 cites zhang2023] Each disruption costs the attacker a confusion penalty of about 20 s [zhang2023].

Context after: [U0128] The earlier MTDSim studies ran these three modules in the configurations of Table <tab:lineage-configurations>.

### U0130 (table-row, tables/tab_2-2b_lineage_configurations:34, tab:lineage-configurations) tier H
*Background > MTDSim > Baseline attacker*

> Parameter | Brown [brown2023] | Zhang [zhang2023] | Ho [ho2024]

Context before: 

Context after: [U0131] Hosts | 200 | 25; 50; 75; 100 | 150 [U0132] Levels of depth | 5 | 4 | ---

### U0207 (prose, L2249) tier H
*Literature review > MTD evaluation > Metrics* · drafting trail: session-drafted, redrafted

> Defender-side effectiveness metrics measure the network's security, such as network compromise ratio (NCR) [zhang2023].

Context before: [U0205 cites cho2020] Attacker-side effectiveness metrics measure the attacker's progress, such as attack success probability (ASP) and mean time to compromise (MTTC) [cho2020]. [U0206 cites cho2020] ASP is the dominant effectiveness metric [cho2020].

Context after: [U0208 cites cho2020] Efficiency metrics measure the cost of an attack or of MTD [cho2020]. [U0209 cites cho2020] No standard set of metrics exists [cho2020].

### U0215 (table-row, L2520, tab:mtd-metrics) tier H
*Literature review > MTD evaluation > Metrics* · drafting trail: session-drafted, redrafted

> Effectiveness | Attack success probability (ASP) [evans2011, cho2020, kim2026, masud2025]; mean time to compromise (MTTC) [mcqueen2006, cho2020, zhang2023, ho2024]; attack path variation, number and exposure [hong2018]; attack surface [manadhatawing2011tse]; attack utility [cho2020] | Defence success probability [cho2020]; attack actions blocked [brown2023]; network compromise ratio (NCR) [zhang2023]; risk [alavizadeh2022, ho2024]; mitigation factor [alavizadeh2022]; time since last MTD [ho2024, tay2024]

Context before: [U0214] | Attacker-side | Defender-side

Context after: [U0216 cites cho2020,alavizadeh2022,cremonini2005,mendonca2023] Efficiency | Attack cost [cho2020, alavizadeh2022]; return on attack (RoA) [cremonini2005, alavizadeh2022] | Defence cost and system performance overhead [cho2020, mendonca2023]; quality of service [cho2020, mendonca2023]

### U0251 (prose, L3226) tier H
*Literature review > MTD attacker models > Recent MTD attacker models* · drafting trail: session-drafted, from-memory, redrafted

> The first is MTDSim's baseline attacker, described in Section <subsec:attacker-model> [brown2023, zhang2023].

Context before: [U0250] This section scores three MTD attacker models, published from 2023 to 2026, on the eight properties an MTD attacker model needs to model an APT attacker (Table <tab:attacker-properties>).

Context after: [U0252 cites masud2025,kim2026] The other two are the attacker models of two recent MTD evaluations that describe their attacker by the Cyber Kill Chain or ATT | CK, by Masud et al. [masud2025] and Kim et al. [kim2026]. [U0253] This dissertation chose them because it expects an attacker model described this way to be the most likely to have the

### U0261 (table-row, L3369, tab:attacker-cross-section) tier H
*Literature review > MTD attacker models > Recent MTD attacker models* · drafting trail: session-drafted, redrafted

> Baseline attacker [brown2023, zhang2023] | 2023 | \propmet | \propnone | \propstandin | \propstandin | \propnone | \propnone | \propnone | \propnone

Context before: [U0260] Attacker model | Year | 1\newline Pers. | 2\newline Obj. | 3\newline Strat. | 4\newline Adapt. | 5\newline Detect. | 6\newline Cost | 7\newline Learn. | 8\newline Deploy.

Context after: [U0262 cites masud2025] Masud et al. [masud2025] | 2025 | \propstandin | \propnone | \propnone | \propnone | \propnone | \propnone | \propnone | \propnone [U0263 cites kim2026] Kim et al. [kim2026] | 2026 | \propstandin | \propnone | \propnone | \propnone | \propstandin | \propnone | \propnone | \propnone

### U0269 (prose, L3396) tier H
*Literature review > MTD attacker models > Recent MTD attacker models* · drafting trail: session-drafted, redrafted

> It has no learning: an exploit of a vulnerability it has exploited before takes half the time [zhang2023], but it keeps vulnerabilities, not the patterns of MTD deployments, and the memory changes no choice.

Context before: [U0267] It has no cost--benefit reasoning: it orders the exploits on a host by return on attack (RoA), but that chooses which vulnerability to exploit, not which technique. [U0268] It has no objective-specific behaviour: after a foothold it takes the same six attack actions in either attack scenario, which changes only the host it attacks next and whether it gives up on it, and none of them exfiltrates or impedes.

Context after: [U0270] It has no detection avoidance: it scans actively and does nothing to avoid an intrusion detection system (IDS). [U0271] It has no deployment-strategy awareness: nothing in it uses which mechanism deploys next or when it deploys.

### U0516 (table-row, tables/tab_4-5a_metrics:243, tab:metrics) tier H
*APT attacker model > Evaluation metrics*

> Network compromise ratio (NCR) | [zhang2023]

Context before: [U0514] lAttack outcome (Section <subsec:metrics-outcome>) [U0515 cites cho2020] Attack success probability (ASP) | [cho2020]

Context after: [U0517 cites mcqueen2006,zhang2023] Mean time to compromise (MTTC) | [mcqueen2006, zhang2023] [U0518] lMTD effectiveness (Section <subsec:metrics-effectiveness>)

### U0517 (table-row, tables/tab_4-5a_metrics:244, tab:metrics) tier H
*APT attacker model > Evaluation metrics*

> Mean time to compromise (MTTC) | [mcqueen2006, zhang2023]

Context before: [U0515 cites cho2020] Attack success probability (ASP) | [cho2020] [U0516 cites zhang2023] Network compromise ratio (NCR) | [zhang2023]

Context after: [U0518] lMTD effectiveness (Section <subsec:metrics-effectiveness>) [U0519 cites alavizadeh2022] NCR reduction | [alavizadeh2022]

### U0557 (prose, L5534) tier H
*APT attacker model > Evaluation metrics > Attack outcome*

> \paragraphNetwork compromise ratio (NCR). NCR is the share of the hosts in the network that the attacker has compromised when a run ends [zhang2023], averaged over runs:

Context before: [U0555 cites cho2020] \paragraphAttack success probability (ASP). ASP is the share of runs in which the attacker reaches its goal [cho2020]:

Context after: [U0559] \paragraphMean time to compromise (MTTC).

### U0560 (prose, L5549) tier H
*APT attacker model > Evaluation metrics > Attack outcome*

> MTTC is the mean time from the start of a run to the attacker reaching its goal, over the runs in which it does [mcqueen2006, zhang2023]:

Context before: [U0559] \paragraphMean time to compromise (MTTC).

Context after: [U0562] NCR reduction and time lost per MTD deployment compare an attacker's runs under MTD with its runs on the same seeds with no MTD, so each pair of runs starts from the same network.

### U0589 (table-row, tables/tab_5-1a_experiment:76, tab:experiment) tier H
*Evaluation > Experimental setup*

> MTD | no MTD; the single deployment strategy, once for each of the seven MTD mechanisms [brown2023, zhang2023]; the random and alternative deployment strategies [zhang2023]; MTDShield, as released [tay2024]

Context before: [U0587] Setting | Value [U0588 cites brown2023] Attacker | the baseline attacker [brown2023]; the APT attacker model on $c_1$ to $c_4$

Context after: [U0590 cites zhang2023,ho2024,tay2024code] Deployment interval | 50, 100 and 200 s [zhang2023, ho2024]; 500, 1 000 and 2 000 s; near-periodic (Section <subsec:defence-mechanisms>) [tay2024code] [U0591 cites tay2024code] Network | 50 hosts, 4 levels of depth, 8 subnets, 5 exposed endpoints [tay2024code]

### U0590 (table-row, tables/tab_5-1a_experiment:77, tab:experiment) tier H
*Evaluation > Experimental setup*

> Deployment interval | 50, 100 and 200 s [zhang2023, ho2024]; 500, 1 000 and 2 000 s; near-periodic (Section <subsec:defence-mechanisms>) [tay2024code]

Context before: [U0588 cites brown2023] Attacker | the baseline attacker [brown2023]; the APT attacker model on $c_1$ to $c_4$ [U0589 cites brown2023,zhang2023,tay2024] MTD | no MTD; the single deployment strategy, once for each of the seven MTD mechanisms [brown2023, zhang2023]; the random and alternative deployment strategies [zhang2023]; MTDShield, as released [tay2024]

Context after: [U0591 cites tay2024code] Network | 50 hosts, 4 levels of depth, 8 subnets, 5 exposed endpoints [tay2024code] [U0592 cites tay2024code] Target hosts | 2, at the deepest level [tay2024code]

### U0757 (table-row, L8868, tab:fidelity-verdict) tier H
*Discussion > APT attacker model versus MTD attacker models* · drafting trail: session-drafted, redrafted

> Baseline attacker [brown2023, zhang2023] | 2023 | \propmet | \propnone | \propstandin | \propstandin | \propnone | \propnone | \propnone | \propnone

Context before: [U0756] Attacker model | Year | 1\newline Pers. | 2\newline Obj. | 3\newline Strat. | 4\newline Adapt. | 5\newline Detect. | 6\newline Cost | 7\newline Learn. | 8\newline Deploy.

Context after: [U0758 cites masud2025] Masud et al. [masud2025] | 2025 | \propstandin | \propnone | \propnone | \propnone | \propnone | \propnone | \propnone | \propnone [U0759 cites kim2026] Kim et al. [kim2026] | 2026 | \propstandin | \propnone | \propnone | \propnone | \propstandin | \propnone | \propnone | \propnone

### U0813 (prose, L9137) tier H
*Discussion > Threats to validity*

> MTDSim's code was inherited from prior studies [brown2023,zhang2023,ho2024,tay2024], and all of ours was written with AI assistance (\hyperref[ch:ai-declaration]AI Use Declaration).

Context before: [U0811 cites wohlin2012] We group the threats into four types of validity [wohlin2012]: internal, construct, conclusion and external. [U0812] A defect in the code is a plausible alternative explanation for the results in this chapter.

Context after: [U0814] To mitigate this threat, we checked the code by its behaviour, with an event tracer, unit tests and fixed seeds that reproduce every run exactly. [U0815] We repaired the defects we found in MTDSim, calling a behaviour a defect only where it departs from what the prior studies describe, so that its design choices are implemented as intended.
