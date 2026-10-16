# Packet: arcuri2014hitchhiker

2 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0596 (table-row, tables/tab_5-1a_experiment:85, tab:experiment) tier H
*Evaluation > Experimental setup*

> Runs per configuration | 1 000 [arcuri2014hitchhiker], on seeds 0 to 999

Context before: [U0594 cites brown2023] Attack scenario | targeted [brown2023] [U0595 cites brown2023,ho2024] End of run | a target host compromised [brown2023], or 15 000 s [ho2024]

Context after: [U0597] Attack profiles | replaced by the attack graph (Section <sec:technique-graph>): every MTD and deployment interval; by 10 random partitions of the attack flows: no MTD, and IP shuffle and OS diversity at 200 and 2 000 s [U0598] Failure matrix | removed: no MTD, and IP shuffle and OS diversity at 200 and 2 000 s

### U0602 (prose, L6172) tier H
*Evaluation > Experimental setup* · drafting trail: redrafted

> \paragraphRuns. Each configuration of attacker, MTD and deployment interval in Table <tab:experiment> is run on the same 1 000 seeds, the number recommended for randomised algorithms [arcuri2014hitchhiker].

Context before: [U0600] \paragraphHeld settings. Table <tab:experiment> gives every held setting and its source. [U0601 cites tay2024code] Both attackers follow the targeted attack scenario (Table <tab:attacker-objectives>), on the default network of Section <subsec:network-model> with two target hosts in place of five, as in the simulator's released experiment code [tay2024code].

Context after: [U0603] Each seed generates one network, so the 1 000 runs of every configuration start from the same 1 000 networks. [U0604] Every metric at every configuration, with its interval, is published with the experiment scripts.
