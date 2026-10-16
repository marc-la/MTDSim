# Packet: ctid2025attackflow

6 units cite it; 7 more name its first author without citing it.

## Units that cite it

### U0026 (prose, L429) tier H
*Introduction* · drafting trail: session-drafted

> Our source is 38 attack flows, graphs of an attack's steps that analysts drew by hand from CTI reports [ctid2025attackflow].

Context before: [U0024] How does MTD perform against the APT attacker model compared with the simulator's baseline attacker? [U0025] We recover the order of APT attackers' steps from cyber threat intelligence (CTI), the threat reports that security firms and government agencies publish on attacks they have investigated.

Context after: [U0027] We aggregate the 38 attack flows into one graph, then split it into attack profiles by objective, such as stealing data. [U0028] Each attack profile records the steps drawn in the attack flows with that objective, and how often each step led to the next.

### U0176 (prose, L1688) tier V2
*Literature review > APT attacker behaviour > Attack profiling*

> This dissertation uses manual attack profiling, with Attack Flow, a language from MITRE's Center for Threat-Informed Defense (CTID) for recording the order of an incident's techniques [ctid2025attackflow].

Context before: [U0174] In manual attack profiling, analysts read a report and draw the order by hand. [U0175] It is reliable, but covers only the incidents analysts have drawn.

Context after: [U0177 cites ctid2025attackflow] An attack flow is one incident recorded in Attack Flow, from the condition it starts in to the condition it ends in [ctid2025attackflow]. [U0178 cites ctid2025attackflow] CTID publishes a corpus of attack flows that analysts drew from publicly reported incidents [ctid2025attackflow].

### U0177 (prose, L1691) tier V2
*Literature review > APT attacker behaviour > Attack profiling*

> An attack flow is one incident recorded in Attack Flow, from the condition it starts in to the condition it ends in [ctid2025attackflow].

Context before: [U0175] It is reliable, but covers only the incidents analysts have drawn. [U0176 cites ctid2025attackflow] This dissertation uses manual attack profiling, with Attack Flow, a language from MITRE's Center for Threat-Informed Defense (CTID) for recording the order of an incident's techniques [ctid2025attackflow].

Context after: [U0178 cites ctid2025attackflow] CTID publishes a corpus of attack flows that analysts drew from publicly reported incidents [ctid2025attackflow]. [U0179 cites cisaaa24038a] Figure <fig:attack-flow-volt-typhoon> shows an attack flow drawn for this dissertation from the Volt Typhoon advisory [cisaaa24038a].

### U0178 (prose, L1693) tier V2
*Literature review > APT attacker behaviour > Attack profiling*

> CTID publishes a corpus of attack flows that analysts drew from publicly reported incidents [ctid2025attackflow].

Context before: [U0176 cites ctid2025attackflow] This dissertation uses manual attack profiling, with Attack Flow, a language from MITRE's Center for Threat-Informed Defense (CTID) for recording the order of an incident's techniques [ctid2025attackflow]. [U0177 cites ctid2025attackflow] An attack flow is one incident recorded in Attack Flow, from the condition it starts in to the condition it ends in [ctid2025attackflow].

Context after: [U0179 cites cisaaa24038a] Figure <fig:attack-flow-volt-typhoon> shows an attack flow drawn for this dissertation from the Volt Typhoon advisory [cisaaa24038a].

### U0182 (prose, L1921) tier H
*Literature review > APT attacker behaviour > Attack profiling* · drafting trail: session-drafted, redrafted

> Attack Flow can record when each technique started and ended, but the attack flows in the corpus almost never do, and ATT | CK dates each campaign only to the month [ctid2025attackflow, mitre2026attackkb].

Context before: [U0181] Attack profiling recovers the order of an attack's techniques, but not their timing.

Context after: [U0183] MTD must therefore decide when to move (Section <sec:mtd-concept>) without the attacker's timing. [U0184 cites cho2020] Deploying too often costs service availability, and deploying too rarely gives the attacker time [cho2020].

### U0948 (caption, tables/tab_B-2a_objective_classification_audit:12, tab:profile-sources) tier V2
*Supplementary material for the APT attacker model > The sources behind each attack flow's attack profile*

> The sources that answered the two questions of Section <sec:attack-profiles> for each attack flow, grouped by attack profile (Table <tab:attack-profiles>). The CTID description of every attack flow was read [ctid2025attackflow], with the analyst's notes on its steps where needed; the columns give what else was read, and a blank row needed nothing else. ATT | CK group is the group page read [mitre2026attackv19], and Threat report the report the attack flow cites.

## Units that name the author without citing

### U0434 (prose, L4907) cites nothing

> The attacker can neither see nor change the MTD schedule, so Defense Impairment has nothing to impair.

### U0451 (table-row, tables/tab_4-4a_dwell_catalogue:18) cites nothing

> Execution, Defense Impairment | Judgement | 22.5

### U0463 (prose, L5011) cites nothing

> Execution and Defense Impairment are single acts, so we set them at half the 45 s, 22.5 s, still longer than an exploit because the attacker slows them to stay hidden.

### U0740 (prose, L8673) cites nothing

> Stealth and Defense Impairment, the tactics for avoiding detection, are unmapped, so in MTDSim its detection avoidance comes only from its tactic durations.

### U0987 (table-row, tables/tab_B-4b_attack_action_times:22) cites nothing

> Defense Impairment | unmapped | | 22.5

### U1154 (caption, tables/tab_C-1a_family_sensitivity:8) cites nothing

> NCR at the low end, the declared value and the high end of each mean duration's band (Table <tab:dwell-catalogue>); the APT attacker model averaged over $c_1$ to $c_4$, 400 runs per cell. Execution and Defense Impairment have half the 45 s mean duration, so moving the 45 s moves theirs too. Change: high end minus low end; bold, the largest. Every NCR's 95 % interval is within $\pm 0.014$.

### U1210 (figure-text, figures/fig_3-1-2a_attack_matrix.tex:19) cites nothing

> Defense Impairment\\\fontsize7.5pt8.85pt\selectfont\mdseries\colorblack!6018 techniques
