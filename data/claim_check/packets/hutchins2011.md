# Packet: hutchins2011

3 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0108 (prose, L921) tier H
*Background > MTDSim > Baseline attacker*

> It follows a fixed procedure of six attack actions, modelled on the Cyber Kill Chain [brown2023, hutchins2011]: it scans for hosts, enumerates one, scans its ports, exploits its vulnerabilities, brute-forces its accounts, and scans the neighbours of each host it compromises (Figure <fig:attacker-model>).

Context before: [U0107 cites brown2023] The baseline attacker is the attacker MTDSim was built with [brown2023].

Context after: [U0109] The attacker follows one of two attack scenarios (Table <tab:attacker-objectives>). [U0110 cites zhang2023] A run ends when the attacker compromises more than 80 % of the hosts [zhang2023], compromises a target host in the targeted scenario, or can discover no new host.

### U0155 (prose, L1264) tier V2
*Literature review > APT attacker behaviour > Advanced persistent threat* · drafting trail: session-drafted

> This dissertation groups the stages of published lifecycle models of an attack [hutchins2011, mandiant2013, alshamrani2019] into four: preparation, intrusion, post-intrusion operations and actions on objectives.

Context before: [U0153 cites alshamrani2019,mtrends2026] It moves low and slow, trading speed for staying undetected [alshamrani2019]: espionage intrusions go undetected for a median of 122 days, against 14 days across all intrusions [mtrends2026]. [U0154 cites alshamrani2019,nist2011sp80039] And it is a threat defined by its objective: data exfiltration, impediment of mission-critical components, or positioning for future operations [alshamrani2019, nist2011sp80039].

Context after: [U0156 cites chemat2024] The models differ in the names and number of their stages but follow a comparable cycle [chemat2024]. [U0157] In preparation, the attacker researches its target and builds its tools; in intrusion, it gains a foothold on a host in the target's network and runs its code there; in post-intrusion operations, it moves through the network undetected; in actions on objectives, it steals data or impedes the victim's systems.

### U0476 (prose, L5160) tier V2
*APT attacker model > Integration with MTDSim > Failure matrix* · drafting trail: redrafted

> Hutchins et al. describe an APT campaign that tried again the next day, with new recipients, after its intrusion attempt was detected and mitigated [hutchins2011].

Context before: [U0474] We set the failure matrix from three assumptions about what an attacker does after a failure. [U0475] First, an attacker without a foothold (Section <subsec:apt>) is unlikely to go on to a tactic that needs one, so after a failed Initial Access it is likely to go back to preparation to try again.

Context after: [U0477] Second, an attacker that fails after it has a foothold keeps the foothold, so we judged it more likely to try another tactic of the same lifecycle stage than to move to another stage. [U0478] Third, an attacker seldom skips a lifecycle stage, as in the lifecycle models of Section <subsec:apt>, which run their stages in sequence.
