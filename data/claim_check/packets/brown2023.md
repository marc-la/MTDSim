# Packet: brown2023

27 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0029 (prose, L441) tier H
*Introduction*

> We execute each attack profile in MTDSim, an existing MTD simulator [brown2023], as the APT attacker model.

Context before: [U0027] We aggregate the 38 attack flows into one graph, then split it into attack profiles by objective, such as stealing data. [U0028] Each attack profile records the steps drawn in the attack flows with that objective, and how often each step led to the next.

Context after: [U0030] MTDSim's original scripted attacker, the baseline attacker, follows a fixed procedure of six attack actions, such as scanning a host's ports and exploiting its vulnerabilities. [U0031] The APT attacker model takes the same six attack actions, but its attack profile decides which comes next, and values we declared decide when and what to do after one fails.

### U0061 (prose, L731) tier H
*Background > MTDSim*

> MTDSim simulates an attacker and MTD on one network, to evaluate MTD mechanisms singly and in combination [brown2023].

Context before: [U0059 cites cho2020] A proactive MTD moves on a schedule; a reactive MTD moves in response to an event, such as an intrusion alert; a hybrid MTD adapts its schedule to such events while bounding the time between moves [cho2020].

Context after: [U0062 cites zhang2023] Every attack action and every deployment takes simulated time, counted in seconds [zhang2023]. [U0063] Figure <fig:mtdsim-model> draws the simulator's three modules: the attacker, the network and MTD. MTD deploys its mechanisms at intervals, and each deployment reconfigures part of the network and disrupts the attacker.

### U0072 (prose, L778) tier H
*Background > MTDSim > Network model*

> Each deeper level is a set of subnets, small groups of densely linked hosts, joined to the level before it, so reaching a level requires a compromised host in the level before it [brown2023].

Context before: [U0070] The hosts sit in levels of depth. [U0071] The first level is the exposed endpoints, the hosts reachable from outside the network.

Context after: [U0073] By default the network has 50 hosts in four levels of depth and eight subnets, with five exposed endpoints. [U0074] Five database hosts at the deepest level are the target hosts of the targeted attack scenario (Section <subsec:attacker-model>).

### U0078 (prose, L790) tier H
*Background > MTDSim > Network model*

> Each vulnerability has an attack complexity from the Common Vulnerability Scoring System (CVSS), which sets the probability that an exploit succeeds, and an impact, the damage a successful exploit does [brown2023].

Context before: [U0076] Each host has an IP address, user accounts, one operating system and a few services, each running on a port. [U0077] The exposed endpoints keep their address, software and accounts throughout: no MTD mechanism changes them, although a topology shuffle can change their links.

Context after: [U0079] A service is compromised when the impact of its exploited vulnerabilities passes a threshold, and a compromised service can compromise its host. [U0080] MTDSim deploys seven MTD mechanisms: five shuffles, two diversities, and no redundancy (Table <tab:defence-mechanisms>).

### U0083 (caption, L821, tab:defence-mechanisms) tier H
*Background > MTDSim > MTD mechanisms and deployment strategies*

> The seven MTD mechanisms, from the pool of Brown [brown2023], added to by Zhang [zhang2023], by the part of the network each reconfigures.

### U0107 (prose, L919) tier H
*Background > MTDSim > Baseline attacker*

> The baseline attacker is the attacker MTDSim was built with [brown2023].

Context before: 

Context after: [U0108 cites brown2023,hutchins2011] It follows a fixed procedure of six attack actions, modelled on the Cyber Kill Chain [brown2023, hutchins2011]: it scans for hosts, enumerates one, scans its ports, exploits its vulnerabilities, brute-forces its accounts, and scans the neighbours of each host it compromises (Figure <fig:attacker-model>). [U0109] The attacker follows one of two attack scenarios (Table <tab:attacker-objectives>).

### U0108 (prose, L921) tier H
*Background > MTDSim > Baseline attacker*

> It follows a fixed procedure of six attack actions, modelled on the Cyber Kill Chain [brown2023, hutchins2011]: it scans for hosts, enumerates one, scans its ports, exploits its vulnerabilities, brute-forces its accounts, and scans the neighbours of each host it compromises (Figure <fig:attacker-model>).

Context before: [U0107 cites brown2023] The baseline attacker is the attacker MTDSim was built with [brown2023].

Context after: [U0109] The attacker follows one of two attack scenarios (Table <tab:attacker-objectives>). [U0110 cites zhang2023] A run ends when the attacker compromises more than 80 % of the hosts [zhang2023], compromises a target host in the targeted scenario, or can discover no new host.

### U0111 (caption, L941, tab:attacker-objectives) tier H
*Background > MTDSim > Baseline attacker*

> The two attack scenarios of the baseline attacker [brown2023], by the attacker's goal.

### U0116 (prose, L958) tier H
*Background > MTDSim > Baseline attacker*

> On each host it tries stolen credentials first, then exploits the vulnerabilities in order of return on attack, an exploit's probability of success times its impact, divided by the time it takes [brown2023], and brute force last.

Context before: [U0115] The attacker knows only its visible subgraph: the exposed endpoints, the hosts it has compromised and their neighbours.

Context after: [U0117] If all three fail, it moves to the next host on its list. [U0118] When the list runs out, it scans for hosts again, and the new list holds every host it can reach, including those it has already tried.

### U0119 (prose, L972) tier H
*Background > MTDSim > Baseline attacker*

> It gives up on a host after ten attempts, but never on a target host [brown2023].

Context before: [U0117] If all three fail, it moves to the next host on its list. [U0118] When the list runs out, it scans for hosts again, and the new list holds every host it can reach, including those it has already tried.

Context after: [U0120 cites tay2024code] Scanning for hosts, enumerating a host and scanning a host's neighbours each take 5 s, scanning its ports 25 s and brute force 20 s [tay2024code]. [U0121 cites brown2023] An exploit takes 15 s times one minus the vulnerability's attack complexity, which lies between 0.4 and 1 [brown2023], so from 0 to 9 s.

### U0121 (prose, L982) tier H
*Background > MTDSim > Baseline attacker*

> An exploit takes 15 s times one minus the vulnerability's attack complexity, which lies between 0.4 and 1 [brown2023], so from 0 to 9 s.

Context before: [U0119 cites brown2023] It gives up on a host after ten attempts, but never on a target host [brown2023]. [U0120 cites tay2024code] Scanning for hosts, enumerating a host and scanning a host's neighbours each take 5 s, scanning its ports 25 s and brute force 20 s [tay2024code].

Context after: [U0122 cites zhang2023] An exploit of a vulnerability it has exploited before takes half the time [zhang2023]. [U0123] A host-layer deployment disrupts the attacker during any attack action and sends it back to scanning hosts, because the host it was on may have moved.

### U0124 (prose, L990) tier H
*Background > MTDSim > Baseline attacker*

> A service-layer deployment disrupts it only while it scans ports, exploits or brute-forces, and sends it back to scanning the same host's ports [brown2023].

Context before: [U0122 cites zhang2023] An exploit of a vulnerability it has exploited before takes half the time [zhang2023]. [U0123] A host-layer deployment disrupts the attacker during any attack action and sends it back to scanning hosts, because the host it was on may have moved.

Context after: [U0125] A user shuffle disrupts only brute force, and sends it to exploit instead. [U0126 cites zhang2023] Each disruption costs the attacker a confusion penalty of about 20 s [zhang2023].

### U0130 (table-row, tables/tab_2-2b_lineage_configurations:34, tab:lineage-configurations) tier H
*Background > MTDSim > Baseline attacker*

> Parameter | Brown [brown2023] | Zhang [zhang2023] | Ho [ho2024]

Context before: 

Context after: [U0131] Hosts | 200 | 25; 50; 75; 100 | 150 [U0132] Levels of depth | 5 | 4 | ---

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

### U0264 (prose, L3388) tier H
*Literature review > MTD attacker models > Recent MTD attacker models* · drafting trail: session-drafted, redrafted

> \paragraphBaseline attacker. The baseline attacker has campaign persistence: it repeats its six attack actions host by host until it reaches its goal, and carries on through every disruption [brown2023].

Context before: 

Context after: [U0265] It has choice of attack strategy in part: it can enter a host with stolen credentials, an exploit or brute force, but a fixed rule sets the order in which it tries them. [U0266 cites brown2023] It has adaptivity in part: a fixed rule sets its response to each kind of disruption, such as always re-scanning after a host-layer disruption [brown2023].

### U0266 (prose, L3391) tier H
*Literature review > MTD attacker models > Recent MTD attacker models* · drafting trail: session-drafted, redrafted

> It has adaptivity in part: a fixed rule sets its response to each kind of disruption, such as always re-scanning after a host-layer disruption [brown2023].

Context before: [U0264 cites brown2023] \paragraphBaseline attacker. The baseline attacker has campaign persistence: it repeats its six attack actions host by host until it reaches its goal, and carries on through every disruption [brown2023]. [U0265] It has choice of attack strategy in part: it can enter a host with stolen credentials, an exploit or brute force, but a fixed rule sets the order in which it tries them.

Context after: [U0267] It has no cost--benefit reasoning: it orders the exploits on a host by return on attack (RoA), but that chooses which vulnerability to exploit, not which technique. [U0268] It has no objective-specific behaviour: after a foothold it takes the same six attack actions in either attack scenario, which changes only the host it attacks next and whether it gives up on it, and none of them exfiltrates or impedes.

### U0429 (prose, L4885) tier H
*APT attacker model > Integration with MTDSim > Tactic-to-action mapping* · drafting trail: redrafted

> Enumerate host moves the attacker to its next host, which is the goal of Lateral Movement, and Brown describes scan neighbours as Command and Control revealing connected hosts [brown2023].

Context before: [U0427] Initial Access, Execution and Privilege Escalation each include a technique that exploits a vulnerability, so all three map to exploit, and Reconnaissance and Discovery each include a scanning technique, so Reconnaissance maps to scan host and Discovery to scan port. [U0428] For the remaining two, Lateral Movement and Command and Control, we chose the attack action that serves the tactic's goal.

Context after: [U0431] Seven tactics are unmapped, because no attack action in MTDSim carries them out.

### U0520 (table-row, tables/tab_4-5a_metrics:247, tab:metrics) tier H
*APT attacker model > Evaluation metrics*

> Attack actions blocked per MTD deployment | [brown2023]

Context before: [U0518] lMTD effectiveness (Section <subsec:metrics-effectiveness>) [U0519 cites alavizadeh2022] NCR reduction | [alavizadeh2022]

Context after: [U0521 cites royston2013] Time lost per MTD deployment | this dissertation, after [royston2013]

### U0566 (prose, L5605) tier H
*APT attacker model > Evaluation metrics > MTD effectiveness* · drafting trail: session-drafted, redrafted

> \paragraphAttack actions blocked per MTD deployment. Attack actions blocked per MTD deployment is the number of attack actions MTD disrupts, divided by the number of MTD deployments before the run ends, counting over every run [brown2023]:

Context before: [U0565 cites alavizadeh2022] It is 0 when MTD has no effect, 1 when no host is compromised under MTD, and negative when MTD raises NCR. It takes the form of the mitigation factor of Alavizadeh et al. [Eq. 13 alavizadeh2022], with NCR in place of annual loss expectancy and no floor at 0.

Context after: [U0568] A deployment disrupts at most the attack action in progress, so the metric runs from 0, when no deployment disrupts one, to 1, when every deployment does.

### U0588 (table-row, tables/tab_5-1a_experiment:75, tab:experiment) tier H
*Evaluation > Experimental setup*

> Attacker | the baseline attacker [brown2023]; the APT attacker model on $c_1$ to $c_4$

Context before: [U0587] Setting | Value

Context after: [U0589 cites brown2023,zhang2023,tay2024] MTD | no MTD; the single deployment strategy, once for each of the seven MTD mechanisms [brown2023, zhang2023]; the random and alternative deployment strategies [zhang2023]; MTDShield, as released [tay2024] [U0590 cites zhang2023,ho2024,tay2024code] Deployment interval | 50, 100 and 200 s [zhang2023, ho2024]; 500, 1 000 and 2 000 s; near-periodic (Section <subsec:defence-mechanisms>) [tay2024code]

### U0589 (table-row, tables/tab_5-1a_experiment:76, tab:experiment) tier H
*Evaluation > Experimental setup*

> MTD | no MTD; the single deployment strategy, once for each of the seven MTD mechanisms [brown2023, zhang2023]; the random and alternative deployment strategies [zhang2023]; MTDShield, as released [tay2024]

Context before: [U0587] Setting | Value [U0588 cites brown2023] Attacker | the baseline attacker [brown2023]; the APT attacker model on $c_1$ to $c_4$

Context after: [U0590 cites zhang2023,ho2024,tay2024code] Deployment interval | 50, 100 and 200 s [zhang2023, ho2024]; 500, 1 000 and 2 000 s; near-periodic (Section <subsec:defence-mechanisms>) [tay2024code] [U0591 cites tay2024code] Network | 50 hosts, 4 levels of depth, 8 subnets, 5 exposed endpoints [tay2024code]

### U0594 (table-row, tables/tab_5-1a_experiment:83, tab:experiment) tier H
*Evaluation > Experimental setup*

> Attack scenario | targeted [brown2023]

Context before: [U0592 cites tay2024code] Target hosts | 2, at the deepest level [tay2024code] [U0593 cites tay2024code] Diversity pool | 20 services per operating system [tay2024code]

Context after: [U0595 cites brown2023,ho2024] End of run | a target host compromised [brown2023], or 15 000 s [ho2024] [U0596 cites arcuri2014hitchhiker] Runs per configuration | 1 000 [arcuri2014hitchhiker], on seeds 0 to 999

### U0595 (table-row, tables/tab_5-1a_experiment:84, tab:experiment) tier H
*Evaluation > Experimental setup*

> End of run | a target host compromised [brown2023], or 15 000 s [ho2024]

Context before: [U0593 cites tay2024code] Diversity pool | 20 services per operating system [tay2024code] [U0594 cites brown2023] Attack scenario | targeted [brown2023]

Context after: [U0596 cites arcuri2014hitchhiker] Runs per configuration | 1 000 [arcuri2014hitchhiker], on seeds 0 to 999 [U0597] Attack profiles | replaced by the attack graph (Section <sec:technique-graph>): every MTD and deployment interval; by 10 random partitions of the attack flows: no MTD, and IP shuffle and OS diversity at 200 and 2 000 s

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
