# Packet: mitre2026attackv19

2 units cite it; 1 more name its first author without citing it.

## Units that cite it

### U0314 (prose, L4012) tier H
*APT attacker model > Attack graph from attack flows* · drafting trail: session-drafted, redrafted

> The attack graph aggregates the 38 attack flows into one weighted directed graph whose nodes are the 15 tactics of ATT | CK v19.1 [mitre2026attackv19].

Context before: [U0312] Sections <sec:petri-formalism> and <sec:execution> answer <sq:model>: they execute each attack profile as a Petri net inside MTDSim. [U0313] Section <sec:evaluation-metrics> defines the metrics with which Chapter <ch:experiments> answers <sq:evaluate>.

Context after: [U0315] Each technique in an attack flow stands for its tactic, and a technique listed under several tactics stands for the leftmost of them in the ATT | CK matrix. [U0316] An edge runs from tactic $p$ to tactic $q$ wherever an attack flow steps from a technique of $p$ to a technique of $q$, and its weight is the number of attack flows that draw it (Figure <fig:attack-graph-construction>).

### U0948 (caption, tables/tab_B-2a_objective_classification_audit:12, tab:profile-sources) tier V2
*Supplementary material for the APT attacker model > The sources behind each attack flow's attack profile*

> The sources that answered the two questions of Section <sec:attack-profiles> for each attack flow, grouped by attack profile (Table <tab:attack-profiles>). The CTID description of every attack flow was read [ctid2025attackflow], with the analyst's notes on its steps where needed; the columns give what else was read, and a blank row needed nothing else. ATT | CK group is the group page read [mitre2026attackv19], and Threat report the report the attack flow cites.

## Units that name the author without citing

### U0161 (prose, L1398) cites strom2018mitre, ferraz2026, buchel2025

> MITRE ATT | CK is a knowledge base of attacker behaviour derived from real-world observations, developed by the MITRE Corporation in 2013 [strom2018mitre], and the common language for attacker behaviour [ferraz2026, buchel2025].
