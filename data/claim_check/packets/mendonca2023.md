# Packet: mendonca2023

3 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0216 (table-row, L2524, tab:mtd-metrics) tier V2
*Literature review > MTD evaluation > Metrics* · drafting trail: session-drafted, redrafted

> Efficiency | Attack cost [cho2020, alavizadeh2022]; return on attack (RoA) [cremonini2005, alavizadeh2022] | Defence cost and system performance overhead [cho2020, mendonca2023]; quality of service [cho2020, mendonca2023]

Context before: [U0214] | Attacker-side | Defender-side [U0215 cites evans2011,cho2020,kim2026,masud2025,mcqueen2006,zhang2023,ho2024,hong2018,manadhatawing2011tse,brown2023,alavizadeh2022,tay2024] Effectiveness | Attack success probability (ASP) [evans2011, cho2020, kim2026, masud2025]; mean time to compromise (MTTC) [mcqueen2006, cho2020, zhang2023, ho2024]; attack path variation, number and exposure [hong2018]; attack surface [manadhatawing2011tse]; attack utility [cho2020] | Defence success probability [cho2020]; attack actions blocked [brown2023]; network compromise ratio (NCR) [zhang2023]; risk [alavizadeh2022, ho2024]; mitigation factor [alavizadeh2022]; time since last MTD [ho2024, tay2024]

Context after: 

### U0365 (prose, L4333) tier V2
*APT attacker model > Petri-net formalism* · drafting trail: redrafted

> Stochastic Petri nets are an established formalism in MTD evaluation [chobenasher2018, mendonca2023].

Context before: [U0363] Two attack profiles that reach the same tactics can therefore move between them differently (Appendix <app:profile-edges>). [U0364] Section <subsec:ablation-attack-profiles> ablates the split: it runs the APT attacker model on the whole attack graph of Section <sec:technique-graph> and compares the results with those of the four attack profiles.

Context after: [U0366 cites cai2016] Cai et al. compare MTD mechanisms with one variant in particular, the generalised stochastic Petri net (GSPN) [cai2016]. [U0367] We follow this convention and formalise each attack profile as a GSPN. An attack profile gives only the edges between tactics and their weights.

### U0458 (prose, L4996) tier V2
*APT attacker model > Integration with MTDSim > Tactic durations*

> We set their mean durations by judgement, from what each tactic does in an attack, as other models that time attack steps do where data are missing [mcqueen2006, bland2020, mendonca2023].

Context before: [U0456] Reconnaissance and Discovery survey a network, as MTDSim's scans for hosts, ports and neighbours do together, so each takes the total time of the three scans, 35 s. [U0457] No source times the other nine tactics, since threat reports time whole intrusions.

Context after: [U0459] Chapter <ch:experiments> compares the APT attacker model with the baseline attacker under the same MTD deployments, so we kept the nine on the scale of the baseline attacker's attack actions (Section <subsec:attacker-model>). [U0460] We also kept each under the 200 s default deployment interval (Section <subsec:defence-mechanisms>), or a deployment would disrupt most runs of the tactic.
