# Packet: tay2024code

9 units cite it; 5 more name its first author without citing it.

## Units that cite it

### U0099 (prose, L863) tier H
*Background > MTDSim > MTD mechanisms and deployment strategies*

> It is near-periodic: each interval is the set value plus a random delay of 0.5 s on average [tay2024code].

Context before: [U0097] No deployment strategy is reactive. [U0098] The deployment interval is the time between deployments: 200 s by default.

Context after: 

### U0120 (prose, L979) tier H
*Background > MTDSim > Baseline attacker*

> Scanning for hosts, enumerating a host and scanning a host's neighbours each take 5 s, scanning its ports 25 s and brute force 20 s [tay2024code].

Context before: [U0118] When the list runs out, it scans for hosts again, and the new list holds every host it can reach, including those it has already tried. [U0119 cites brown2023] It gives up on a host after ten attempts, but never on a target host [brown2023].

Context after: [U0121 cites brown2023] An exploit takes 15 s times one minus the vulnerability's attack complexity, which lies between 0.4 and 1 [brown2023], so from 0 to 9 s. [U0122 cites zhang2023] An exploit of a vulnerability it has exploited before takes half the time [zhang2023].

### U0590 (table-row, tables/tab_5-1a_experiment:77, tab:experiment) tier H
*Evaluation > Experimental setup*

> Deployment interval | 50, 100 and 200 s [zhang2023, ho2024]; 500, 1 000 and 2 000 s; near-periodic (Section <subsec:defence-mechanisms>) [tay2024code]

Context before: [U0588 cites brown2023] Attacker | the baseline attacker [brown2023]; the APT attacker model on $c_1$ to $c_4$ [U0589 cites brown2023,zhang2023,tay2024] MTD | no MTD; the single deployment strategy, once for each of the seven MTD mechanisms [brown2023, zhang2023]; the random and alternative deployment strategies [zhang2023]; MTDShield, as released [tay2024]

Context after: [U0591 cites tay2024code] Network | 50 hosts, 4 levels of depth, 8 subnets, 5 exposed endpoints [tay2024code] [U0592 cites tay2024code] Target hosts | 2, at the deepest level [tay2024code]

### U0591 (table-row, tables/tab_5-1a_experiment:80, tab:experiment) tier H
*Evaluation > Experimental setup*

> Network | 50 hosts, 4 levels of depth, 8 subnets, 5 exposed endpoints [tay2024code]

Context before: [U0589 cites brown2023,zhang2023,tay2024] MTD | no MTD; the single deployment strategy, once for each of the seven MTD mechanisms [brown2023, zhang2023]; the random and alternative deployment strategies [zhang2023]; MTDShield, as released [tay2024] [U0590 cites zhang2023,ho2024,tay2024code] Deployment interval | 50, 100 and 200 s [zhang2023, ho2024]; 500, 1 000 and 2 000 s; near-periodic (Section <subsec:defence-mechanisms>) [tay2024code]

Context after: [U0592 cites tay2024code] Target hosts | 2, at the deepest level [tay2024code] [U0593 cites tay2024code] Diversity pool | 20 services per operating system [tay2024code]

### U0592 (table-row, tables/tab_5-1a_experiment:81, tab:experiment) tier H
*Evaluation > Experimental setup*

> Target hosts | 2, at the deepest level [tay2024code]

Context before: [U0590 cites zhang2023,ho2024,tay2024code] Deployment interval | 50, 100 and 200 s [zhang2023, ho2024]; 500, 1 000 and 2 000 s; near-periodic (Section <subsec:defence-mechanisms>) [tay2024code] [U0591 cites tay2024code] Network | 50 hosts, 4 levels of depth, 8 subnets, 5 exposed endpoints [tay2024code]

Context after: [U0593 cites tay2024code] Diversity pool | 20 services per operating system [tay2024code] [U0594 cites brown2023] Attack scenario | targeted [brown2023]

### U0593 (table-row, tables/tab_5-1a_experiment:82, tab:experiment) tier H
*Evaluation > Experimental setup*

> Diversity pool | 20 services per operating system [tay2024code]

Context before: [U0591 cites tay2024code] Network | 50 hosts, 4 levels of depth, 8 subnets, 5 exposed endpoints [tay2024code] [U0592 cites tay2024code] Target hosts | 2, at the deepest level [tay2024code]

Context after: [U0594 cites brown2023] Attack scenario | targeted [brown2023] [U0595 cites brown2023,ho2024] End of run | a target host compromised [brown2023], or 15 000 s [ho2024]

### U0601 (prose, L6150) tier H
*Evaluation > Experimental setup* · drafting trail: redrafted

> Both attackers follow the targeted attack scenario (Table <tab:attacker-objectives>), on the default network of Section <subsec:network-model> with two target hosts in place of five, as in the simulator's released experiment code [tay2024code].

Context before: [U0600] \paragraphHeld settings. Table <tab:experiment> gives every held setting and its source.

Context after: [U0602 cites arcuri2014hitchhiker] \paragraphRuns. Each configuration of attacker, MTD and deployment interval in Table <tab:experiment> is run on the same 1 000 seeds, the number recommended for randomised algorithms [arcuri2014hitchhiker]. [U0603] Each seed generates one network, so the 1 000 runs of every configuration start from the same 1 000 networks.

### U1024 (prose, L10285) tier H
*Supplementary material for the MTD evaluation > MTDShield as run*

> MTDShield in Chapter <ch:experiments> is the agent Tay scored highest of the 38 he trained [Sec. 5.2.2 tay2024], run as released, with his weights and input code [tay2024code].

Context before: [U1023] Sections <app:mtdshield> to <app:sensitivity> back Chapter <ch:experiments>, and Section <app:further-analyses> backs Chapter <ch:discussion>.

Context after: [U1025] Chapter <ch:experiments> runs the random deployment strategy over the same four MTD mechanisms beside it, so the difference between the two is what the agent's policy adds. [U1026] Table <tab:mtdshield-configuration> compares its training with the runs of Chapter <ch:experiments>.

### U1027 (caption, L10295, tab:mtdshield-configuration) tier H
*Supplementary material for the MTD evaluation > MTDShield as run*

> MTDShield's settings in training, from the release's training script [tay2024code], and as run in Chapter <ch:experiments> (Table <tab:experiment>). In both, it chooses among complete topology shuffle, IP shuffle, OS diversity and service diversity, or nothing; it is told the attacker's current attack action at every decision; and a deployment is forced after 2 000 s without one.

## Units that name the author without citing

### U0100 (caption, L870) cites zhang2023, tay2024

> The four deployment strategies: three from Zhang [zhang2023] and MTDShield, the reinforcement-learning agent of Tay [tay2024].

### U0129 (caption, tables/tab_2-2b_lineage_configurations:30) cites tay2024

> The configurations the earlier MTDSim studies ran. Times are in seconds; a dash marks a value the study does not state. Tay [tay2024] states none.

### U0787 (prose, L8992) cites tay2024

> Tay et al. tested MTDShield in its training environment, against the baseline attacker, and compared it with no MTD [tay2024].

### U1033 (prose, L10315) cites nothing

> Two changes let MTDShield run: Tay's input construction is restored as an option beside the simulator's, and a decision to do nothing waits for the next deployment interval instead of stopping the clock.

### U1034 (prose, L10318) cites nothing

> As released, its evaluation code reads four of its eight inputs before the run starts, so they are zero at every decision, as in Tay's own evaluations.
