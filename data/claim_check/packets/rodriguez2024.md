# Packet: rodriguez2024

4 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0164 (prose, L1445) tier V2
*Literature review > APT attacker behaviour > MITRE ATT | CK* · drafting trail: session-drafted, redrafted

> A tactic is what an attacker does to achieve a goal, a technique is how it does it, and a procedure is one recorded instance of a technique [rodriguez2024].

Context before: [U0162 cites mitre2026attackkb,alsada2024] It holds the attack matrix alongside catalogues of named attacker groups and their campaigns, each group characterised by the techniques observed across its operations [mitre2026attackkb, alsada2024]. [U0163 cites strom2018mitre] ATT | CK organises behaviour into a hierarchy of tactics, techniques, sub-techniques and procedures [strom2018mitre].

Context after: [U0165] The matrix lays out the top two levels: the 15 tactics as columns, each tactic's techniques beneath it (Figure <fig:attack-matrix>). [U0166 cites mitre2026attackkb] The Initial Access tactic (\attackidTA0001), for example, is realised through Valid Accounts (\attackidT1078), whose Domain Accounts sub-technique (\attackidT1078.002) carries a procedure recording Volt Typhoon's use of compromised domain accounts to authenticate to devices on compromised networks [mitre2026attackkb].

### U0168 (prose, L1670) tier V2
*Literature review > APT attacker behaviour > Attack profiling* · drafting trail: session-drafted, redrafted

> Attack profiling reads CTI to recover the order in which an attacker used ATT | CK techniques to reach its objective [rodriguez2024].

Context before: [U0166 cites mitre2026attackkb] The Initial Access tactic (\attackidTA0001), for example, is realised through Valid Accounts (\attackidT1078), whose Domain Accounts sub-technique (\attackidT1078.002) carries a procedure recording Volt Typhoon's use of compromised domain accounts to authenticate to devices on compromised networks [mitre2026attackkb].

Context after: [U0169 cites ferraz2026] CTI records which techniques an attack used, but rarely their order, and ATT | CK does not record the order either [ferraz2026]. [U0170] The product of attack profiling, an attack profile, can be executed as an attacker in a simulation; Chapter <ch:attacker-model> builds its APT attacker model on attack profiles.

### U0510 (table-row, tables/tab_4-5a_metrics:237, tab:metrics) tier V2
*APT attacker model > Evaluation metrics*

> Relative tactic occurrence | [rodriguez2024]

Context before: [U0508] Metric | Source [U0509] lAttacker behaviour (Section <subsec:metrics-behaviour>)

Context after: [U0511 cites hong2018] Distinct openings | this dissertation, after [hong2018] [U0512 cites zhan2013] Attack rate | [zhan2013]

### U0532 (prose, L5434) tier H
*APT attacker model > Evaluation metrics > Attacker behaviour*

> Rodr\'\iguez et al. tabulate the same percentage over the events of an attack log, in which one tactic can log many events [Table 3 rodriguez2024].

Context before: [U0530] Relative tactic occurrence is the percentage of an attacker's steps taken in each tactic, counting over every run:

Context after: [U0533] The attack profiles were built to differ, so the metric tests whether their runs still differ in MTDSim, where a failed attack action reweights the attacker's next tactics (Section <subsec:failure-matrix>). [U0534] \paragraphDistinct openings. An attacker with choice of attack strategy chooses among several sequences of techniques toward the same objective.
