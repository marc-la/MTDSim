# Packet: mitre2026attackkb

6 units cite it; 1 more name its first author without citing it.

## Units that cite it

### U0162 (prose, L1402) tier V2
*Literature review > APT attacker behaviour > MITRE ATT | CK* · drafting trail: session-drafted, redrafted

> It holds the attack matrix alongside catalogues of named attacker groups and their campaigns, each group characterised by the techniques observed across its operations [mitre2026attackkb, alsada2024].

Context before: [U0160 cites cisaaa24038a] Volt Typhoon, for example, held footholds in US critical infrastructure networks for at least five years, to disrupt their operational technology in a future crisis [cisaaa24038a]. [U0161 cites strom2018mitre,ferraz2026,buchel2025] MITRE ATT | CK is a knowledge base of attacker behaviour derived from real-world observations, developed by the MITRE Corporation in 2013 [strom2018mitre], and the common language for attacker behaviour [ferraz2026, buchel2025].

Context after: [U0163 cites strom2018mitre] ATT | CK organises behaviour into a hierarchy of tactics, techniques, sub-techniques and procedures [strom2018mitre]. [U0164 cites rodriguez2024] A tactic is what an attacker does to achieve a goal, a technique is how it does it, and a procedure is one recorded instance of a technique [rodriguez2024].

### U0166 (prose, L1449) tier V2
*Literature review > APT attacker behaviour > MITRE ATT | CK* · drafting trail: session-drafted, redrafted

> The Initial Access tactic (\attackidTA0001), for example, is realised through Valid Accounts (\attackidT1078), whose Domain Accounts sub-technique (\attackidT1078.002) carries a procedure recording Volt Typhoon's use of compromised domain accounts to authenticate to devices on compromised networks [mitre2026attackkb].

Context before: [U0164 cites rodriguez2024] A tactic is what an attacker does to achieve a goal, a technique is how it does it, and a procedure is one recorded instance of a technique [rodriguez2024]. [U0165] The matrix lays out the top two levels: the 15 tactics as columns, each tactic's techniques beneath it (Figure <fig:attack-matrix>).

Context after: [U0168 cites rodriguez2024] Attack profiling reads CTI to recover the order in which an attacker used ATT | CK techniques to reach its objective [rodriguez2024].

### U0167 (caption, L1532, fig:attack-matrix) tier V2
*Literature review > APT attacker behaviour > MITRE ATT | CK* · drafting trail: session-drafted, redrafted

> The MITRE ATT | CK Enterprise matrix (v19.1), with the Initial Access tactic opened down to a Volt Typhoon procedure [mitre2026attackkb].

### U0182 (prose, L1921) tier H
*Literature review > APT attacker behaviour > Attack profiling* · drafting trail: session-drafted, redrafted

> Attack Flow can record when each technique started and ended, but the attack flows in the corpus almost never do, and ATT | CK dates each campaign only to the month [ctid2025attackflow, mitre2026attackkb].

Context before: [U0181] Attack profiling recovers the order of an attack's techniques, but not their timing.

Context after: [U0183] MTD must therefore decide when to move (Section <sec:mtd-concept>) without the attacker's timing. [U0184 cites cho2020] Deploying too often costs service availability, and deploying too rarely gives the attacker time [cho2020].

### U0331 (prose, L4082) tier V2
*APT attacker model > Attack graph from attack flows*

> Reconnaissance and Resource Development happen largely outside the scope of the defender's controls [mitre2026attackkb], so the investigations that CTI reports rarely see them, and any CTI corpus shares the gap.

Context before: [U0329] Tactics also make the tactic-to-action mapping smaller: it maps 15 tactics, rather than the 124 techniques the attack flows use, to MTDSim's six attack actions (Section <sec:execution>). [U0330] The attack graph is sparsest before Initial Access: Reconnaissance appears in 10 of the 38 attack flows.

Context after: [U0332] An MTD evaluation cannot ignore it, because shuffling works by making the attacker's reconnaissance out of date. [U0333] Section <sec:petri-formalism> adds the missing edges as the pre-intrusion overlay.

### U0461 (prose, L5005) tier H
*APT attacker model > Integration with MTDSim > Tactic durations*

> Persistence, Stealth and Command and Control keep a foothold, stay hidden and stay in contact throughout an attack [mitre2026attackkb], so we set them longest, at 45 s.

Context before: [U0459] Chapter <ch:experiments> compares the APT attacker model with the baseline attacker under the same MTD deployments, so we kept the nine on the scale of the baseline attacker's attack actions (Section <subsec:attacker-model>). [U0460] We also kept each under the 200 s default deployment interval (Section <subsec:defence-mechanisms>), or a deployment would disrupt most runs of the tactic.

Context after: [U0462] Collection, Exfiltration and Impact move or destroy data, which we judged to take a little longer than surveying a network, so we set them at 36 s. [U0463] Execution and Defense Impairment are single acts, so we set them at half the 45 s, 22.5 s, still longer than an exploit because the attacker slows them to stay hidden.

## Units that name the author without citing

### U0161 (prose, L1398) cites strom2018mitre, ferraz2026, buchel2025

> MITRE ATT | CK is a knowledge base of attacker behaviour derived from real-world observations, developed by the MITRE Corporation in 2013 [strom2018mitre], and the common language for attacker behaviour [ferraz2026, buchel2025].
