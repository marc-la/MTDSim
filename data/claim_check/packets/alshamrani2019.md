# Packet: alshamrani2019

13 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0013 (prose, L270) tier V2
*Introduction* · drafting trail: session-drafted

> Volt Typhoon is an advanced persistent threat (APT), a well-resourced attacker that pursues a specific objective against a specific target over months or years [alshamrani2019].

Context before: [U0011 cites cisaaa24038a] In February 2024, US and Australian cyber agencies reported that the Chinese state-sponsored group Volt Typhoon had held footholds in American critical infrastructure networks for at least five years [cisaaa24038a]. [U0012 cites cisaaa24038a] The group stayed hidden by signing in with stolen but valid credentials and running the administration tools already installed on each network [cisaaa24038a].

Context after: [U0014 cites cisaaa24038a] Before breaking in, Volt Typhoon conducted reconnaissance of its victims' networks [cisaaa24038a]. [U0015 cites ghosh2009nitrd] A static network keeps such reconnaissance valid and lets an attacker plan at its leisure [ghosh2009nitrd].

### U0018 (prose, L310) tier V2
*Introduction*

> MTD has been proposed as a defence against APTs [alshamrani2019], yet it is rarely tested against one.

Context before: [U0016 cites cho2020] Moving target defence (MTD) changes a network's addresses, layout, software and credentials on a schedule, so that stolen credentials and reconnaissance go out of date even if the attacker is never detected [cho2020]. [U0017 cites ghosh2009nitrd,zhuang2012] MTD aims to shift the advantage of time from the attacker to the defender [ghosh2009nitrd, zhuang2012].

Context after: [U0019 cites cho2020,jalowski2026,hong2018] Most tests run in simulation, against attacker models far simpler than an APT [cho2020, jalowski2026], and how MTD is measured to perform depends on how the attacker is implemented [hong2018]. [U0020] This gap motivates the research question of this dissertation:

### U0149 (prose, L1211) tier H
*Literature review > APT attacker behaviour > Advanced persistent threat* · drafting trail: session-drafted, redrafted

> An APT attacker is a well-resourced attacker, typically sponsored by a nation-state or organisation, that pursues a specific objective against a specific target [alshamrani2019].

Context before: [U0147] Section <subsec:attack> describes MITRE ATT | CK, the knowledge base that records attacker behaviour as techniques. [U0148] Section <subsec:profiling> describes attack profiling, which recovers the order of an attack's techniques from CTI.

Context after: [U0150] Each word of the name stands for one property. [U0151 cites alshamrani2019] It is advanced in its tooling and tradecraft [alshamrani2019].

### U0151 (prose, L1215) tier V2
*Literature review > APT attacker behaviour > Advanced persistent threat* · drafting trail: session-drafted, redrafted

> It is advanced in its tooling and tradecraft [alshamrani2019].

Context before: [U0149 cites alshamrani2019] An APT attacker is a well-resourced attacker, typically sponsored by a nation-state or organisation, that pursues a specific objective against a specific target [alshamrani2019]. [U0150] Each word of the name stands for one property.

Context after: [U0152 cites nist2011sp80039] It is persistent: in the definition of the US National Institute of Standards and Technology (NIST), it pursues its objective repeatedly over an extended period and adapts to the defender's resistance [nist2011sp80039]. [U0153 cites alshamrani2019,mtrends2026] It moves low and slow, trading speed for staying undetected [alshamrani2019]: espionage intrusions go undetected for a median of 122 days, against 14 days across all intrusions [mtrends2026].

### U0153 (prose, L1219) tier H
*Literature review > APT attacker behaviour > Advanced persistent threat* · drafting trail: session-drafted, redrafted

> It moves low and slow, trading speed for staying undetected [alshamrani2019]: espionage intrusions go undetected for a median of 122 days, against 14 days across all intrusions [mtrends2026].

Context before: [U0151 cites alshamrani2019] It is advanced in its tooling and tradecraft [alshamrani2019]. [U0152 cites nist2011sp80039] It is persistent: in the definition of the US National Institute of Standards and Technology (NIST), it pursues its objective repeatedly over an extended period and adapts to the defender's resistance [nist2011sp80039].

Context after: [U0154 cites alshamrani2019,nist2011sp80039] And it is a threat defined by its objective: data exfiltration, impediment of mission-critical components, or positioning for future operations [alshamrani2019, nist2011sp80039]. [U0155 cites hutchins2011,mandiant2013,alshamrani2019] This dissertation groups the stages of published lifecycle models of an attack [hutchins2011, mandiant2013, alshamrani2019] into four: preparation, intrusion, post-intrusion operations and actions on objectives.

### U0154 (prose, L1221) tier V2
*Literature review > APT attacker behaviour > Advanced persistent threat* · drafting trail: session-drafted, redrafted

> And it is a threat defined by its objective: data exfiltration, impediment of mission-critical components, or positioning for future operations [alshamrani2019, nist2011sp80039].

Context before: [U0152 cites nist2011sp80039] It is persistent: in the definition of the US National Institute of Standards and Technology (NIST), it pursues its objective repeatedly over an extended period and adapts to the defender's resistance [nist2011sp80039]. [U0153 cites alshamrani2019,mtrends2026] It moves low and slow, trading speed for staying undetected [alshamrani2019]: espionage intrusions go undetected for a median of 122 days, against 14 days across all intrusions [mtrends2026].

Context after: [U0155 cites hutchins2011,mandiant2013,alshamrani2019] This dissertation groups the stages of published lifecycle models of an attack [hutchins2011, mandiant2013, alshamrani2019] into four: preparation, intrusion, post-intrusion operations and actions on objectives. [U0156 cites chemat2024] The models differ in the names and number of their stages but follow a comparable cycle [chemat2024].

### U0155 (prose, L1264) tier V2
*Literature review > APT attacker behaviour > Advanced persistent threat* · drafting trail: session-drafted

> This dissertation groups the stages of published lifecycle models of an attack [hutchins2011, mandiant2013, alshamrani2019] into four: preparation, intrusion, post-intrusion operations and actions on objectives.

Context before: [U0153 cites alshamrani2019,mtrends2026] It moves low and slow, trading speed for staying undetected [alshamrani2019]: espionage intrusions go undetected for a median of 122 days, against 14 days across all intrusions [mtrends2026]. [U0154 cites alshamrani2019,nist2011sp80039] And it is a threat defined by its objective: data exfiltration, impediment of mission-critical components, or positioning for future operations [alshamrani2019, nist2011sp80039].

Context after: [U0156 cites chemat2024] The models differ in the names and number of their stages but follow a comparable cycle [chemat2024]. [U0157] In preparation, the attacker researches its target and builds its tools; in intrusion, it gains a foothold on a host in the target's network and runs its code there; in post-intrusion operations, it moves through the network undetected; in actions on objectives, it steals data or impedes the victim's systems.

### U0158 (prose, L1273) tier V2
*Literature review > APT attacker behaviour > Advanced persistent threat* · drafting trail: session-drafted

> Preparation and intrusion are the same for every APT attacker; post-intrusion operations and actions on objectives depend on its objective [alshamrani2019].

Context before: [U0156 cites chemat2024] The models differ in the names and number of their stages but follow a comparable cycle [chemat2024]. [U0157] In preparation, the attacker researches its target and builds its tools; in intrusion, it gains a foothold on a host in the target's network and runs its code there; in post-intrusion operations, it moves through the network undetected; in actions on objectives, it steals data or impedes the victim's systems.

Context after: [U0159 cites alshamrani2019] An attacker positioning for future operations stays in post-intrusion operations [alshamrani2019]. [U0160 cites cisaaa24038a] Volt Typhoon, for example, held footholds in US critical infrastructure networks for at least five years, to disrupt their operational technology in a future crisis [cisaaa24038a].

### U0159 (prose, L1275) tier V2
*Literature review > APT attacker behaviour > Advanced persistent threat* · drafting trail: session-drafted

> An attacker positioning for future operations stays in post-intrusion operations [alshamrani2019].

Context before: [U0157] In preparation, the attacker researches its target and builds its tools; in intrusion, it gains a foothold on a host in the target's network and runs its code there; in post-intrusion operations, it moves through the network undetected; in actions on objectives, it steals data or impedes the victim's systems. [U0158 cites alshamrani2019] Preparation and intrusion are the same for every APT attacker; post-intrusion operations and actions on objectives depend on its objective [alshamrani2019].

Context after: [U0160 cites cisaaa24038a] Volt Typhoon, for example, held footholds in US critical infrastructure networks for at least five years, to disrupt their operational technology in a future crisis [cisaaa24038a]. [U0161 cites strom2018mitre,ferraz2026,buchel2025] MITRE ATT | CK is a knowledge base of attacker behaviour derived from real-world observations, developed by the MITRE Corporation in 2013 [strom2018mitre], and the common language for attacker behaviour [ferraz2026, buchel2025].

### U0230 (prose, L2949) tier V2
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: session-drafted, redrafted

> The APT definition of Section <subsec:apt> gives four: the APT attacker pursues its objective over an extended period (campaign persistence), uses different techniques after the foothold for different objectives (objective-specific behaviour), adapts to the defender's resistance (adaptivity) and moves low and slow to avoid detection (detection avoidance) [nist2011sp80039, alshamrani2019].

Context before: [U0228] sets out eight properties an MTD attacker model needs to model an APT attacker, and Section <subsec:recent-threat-models> scores three recent MTD attacker models on them. [U0229] An MTD attacker model needs eight properties to model an APT attacker.

Context after: [U0231 cites cho2020,jalowski2026] The two surveys add the other four: choice of attack strategy, cost--benefit reasoning, learning and deployment-strategy awareness [cho2020, jalowski2026]. [U0232] This dissertation synthesises the eight properties in Table <tab:attacker-properties>.

### U0242 (table-row, L3073, tab:attacker-properties) tier V2
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: session-drafted, redrafted

> 1 | Campaign persistence | pursues one multi-stage campaign toward its objective over an extended period | [alshamrani2019, nist2011sp80039]

Context before: [U0241] | Property | Definition | Source

Context after: [U0243 cites alshamrani2019] 2 | Objective-specific behaviour | after the foothold, uses different techniques for different objectives, such as exfiltration or impediment | [alshamrani2019] [U0244 cites cho2020] 3 | Choice of attack strategy | chooses among several sequences of techniques toward the same objective | [cho2020]

### U0243 (table-row, L3075, tab:attacker-properties) tier V2
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: session-drafted, redrafted

> 2 | Objective-specific behaviour | after the foothold, uses different techniques for different objectives, such as exfiltration or impediment | [alshamrani2019]

Context before: [U0241] | Property | Definition | Source [U0242 cites alshamrani2019,nist2011sp80039] 1 | Campaign persistence | pursues one multi-stage campaign toward its objective over an extended period | [alshamrani2019, nist2011sp80039]

Context after: [U0244 cites cho2020] 3 | Choice of attack strategy | chooses among several sequences of techniques toward the same objective | [cho2020] [U0245 cites cho2020,nist2011sp80039] 4 | Adaptivity | chooses its next technique in response to an MTD disruption | [cho2020, nist2011sp80039]

### U0246 (table-row, L3078, tab:attacker-properties) tier V2
*Literature review > MTD attacker models > Properties an MTD attacker model needs to model an APT attacker* · drafting trail: session-drafted, redrafted

> 5 | Detection avoidance | moves low and slow and chooses techniques an intrusion detection system (IDS) does not flag, such as passive reconnaissance | [alshamrani2019, jalowski2026]

Context before: [U0244 cites cho2020] 3 | Choice of attack strategy | chooses among several sequences of techniques toward the same objective | [cho2020] [U0245 cites cho2020,nist2011sp80039] 4 | Adaptivity | chooses its next technique in response to an MTD disruption | [cho2020, nist2011sp80039]

Context after: [U0247 cites cho2020] 6 | Cost--benefit reasoning | chooses each technique by weighing its cost against its benefit | [cho2020] [U0248 cites cho2020,jalowski2026] 7 | Learning | keeps the patterns it observes in past MTD deployments, and uses them to choose later techniques | [cho2020, jalowski2026]
