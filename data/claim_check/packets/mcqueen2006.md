# Packet: mcqueen2006

4 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0215 (table-row, L2520, tab:mtd-metrics) tier H
*Literature review > MTD evaluation > Metrics* · drafting trail: session-drafted, redrafted

> Effectiveness | Attack success probability (ASP) [evans2011, cho2020, kim2026, masud2025]; mean time to compromise (MTTC) [mcqueen2006, cho2020, zhang2023, ho2024]; attack path variation, number and exposure [hong2018]; attack surface [manadhatawing2011tse]; attack utility [cho2020] | Defence success probability [cho2020]; attack actions blocked [brown2023]; network compromise ratio (NCR) [zhang2023]; risk [alavizadeh2022, ho2024]; mitigation factor [alavizadeh2022]; time since last MTD [ho2024, tay2024]

Context before: [U0214] | Attacker-side | Defender-side

Context after: [U0216 cites cho2020,alavizadeh2022,cremonini2005,mendonca2023] Efficiency | Attack cost [cho2020, alavizadeh2022]; return on attack (RoA) [cremonini2005, alavizadeh2022] | Defence cost and system performance overhead [cho2020, mendonca2023]; quality of service [cho2020, mendonca2023]

### U0458 (prose, L4996) tier V2
*APT attacker model > Integration with MTDSim > Tactic durations*

> We set their mean durations by judgement, from what each tactic does in an attack, as other models that time attack steps do where data are missing [mcqueen2006, bland2020, mendonca2023].

Context before: [U0456] Reconnaissance and Discovery survey a network, as MTDSim's scans for hosts, ports and neighbours do together, so each takes the total time of the three scans, 35 s. [U0457] No source times the other nine tactics, since threat reports time whole intrusions.

Context after: [U0459] Chapter <ch:experiments> compares the APT attacker model with the baseline attacker under the same MTD deployments, so we kept the nine on the scale of the baseline attacker's attack actions (Section <subsec:attacker-model>). [U0460] We also kept each under the 200 s default deployment interval (Section <subsec:defence-mechanisms>), or a deployment would disrupt most runs of the tactic.

### U0517 (table-row, tables/tab_4-5a_metrics:244, tab:metrics) tier H
*APT attacker model > Evaluation metrics*

> Mean time to compromise (MTTC) | [mcqueen2006, zhang2023]

Context before: [U0515 cites cho2020] Attack success probability (ASP) | [cho2020] [U0516 cites zhang2023] Network compromise ratio (NCR) | [zhang2023]

Context after: [U0518] lMTD effectiveness (Section <subsec:metrics-effectiveness>) [U0519 cites alavizadeh2022] NCR reduction | [alavizadeh2022]

### U0560 (prose, L5549) tier H
*APT attacker model > Evaluation metrics > Attack outcome*

> MTTC is the mean time from the start of a run to the attacker reaching its goal, over the runs in which it does [mcqueen2006, zhang2023]:

Context before: [U0559] \paragraphMean time to compromise (MTTC).

Context after: [U0562] NCR reduction and time lost per MTD deployment compare an attacker's runs under MTD with its runs on the same seeds with no MTD, so each pair of runs starts from the same network.
