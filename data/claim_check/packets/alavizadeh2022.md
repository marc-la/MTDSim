# Packet: alavizadeh2022

4 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0215 (table-row, L2520, tab:mtd-metrics) tier H
*Literature review > MTD evaluation > Metrics* · drafting trail: session-drafted, redrafted

> Effectiveness | Attack success probability (ASP) [evans2011, cho2020, kim2026, masud2025]; mean time to compromise (MTTC) [mcqueen2006, cho2020, zhang2023, ho2024]; attack path variation, number and exposure [hong2018]; attack surface [manadhatawing2011tse]; attack utility [cho2020] | Defence success probability [cho2020]; attack actions blocked [brown2023]; network compromise ratio (NCR) [zhang2023]; risk [alavizadeh2022, ho2024]; mitigation factor [alavizadeh2022]; time since last MTD [ho2024, tay2024]

Context before: [U0214] | Attacker-side | Defender-side

Context after: [U0216 cites cho2020,alavizadeh2022,cremonini2005,mendonca2023] Efficiency | Attack cost [cho2020, alavizadeh2022]; return on attack (RoA) [cremonini2005, alavizadeh2022] | Defence cost and system performance overhead [cho2020, mendonca2023]; quality of service [cho2020, mendonca2023]

### U0216 (table-row, L2524, tab:mtd-metrics) tier V2
*Literature review > MTD evaluation > Metrics* · drafting trail: session-drafted, redrafted

> Efficiency | Attack cost [cho2020, alavizadeh2022]; return on attack (RoA) [cremonini2005, alavizadeh2022] | Defence cost and system performance overhead [cho2020, mendonca2023]; quality of service [cho2020, mendonca2023]

Context before: [U0214] | Attacker-side | Defender-side [U0215 cites evans2011,cho2020,kim2026,masud2025,mcqueen2006,zhang2023,ho2024,hong2018,manadhatawing2011tse,brown2023,alavizadeh2022,tay2024] Effectiveness | Attack success probability (ASP) [evans2011, cho2020, kim2026, masud2025]; mean time to compromise (MTTC) [mcqueen2006, cho2020, zhang2023, ho2024]; attack path variation, number and exposure [hong2018]; attack surface [manadhatawing2011tse]; attack utility [cho2020] | Defence success probability [cho2020]; attack actions blocked [brown2023]; network compromise ratio (NCR) [zhang2023]; risk [alavizadeh2022, ho2024]; mitigation factor [alavizadeh2022]; time since last MTD [ho2024, tay2024]

Context after: 

### U0519 (table-row, tables/tab_4-5a_metrics:246, tab:metrics) tier V2
*APT attacker model > Evaluation metrics*

> NCR reduction | [alavizadeh2022]

Context before: [U0517 cites mcqueen2006,zhang2023] Mean time to compromise (MTTC) | [mcqueen2006, zhang2023] [U0518] lMTD effectiveness (Section <subsec:metrics-effectiveness>)

Context after: [U0520 cites brown2023] Attack actions blocked per MTD deployment | [brown2023] [U0521 cites royston2013] Time lost per MTD deployment | this dissertation, after [royston2013]

### U0565 (prose, L5588) tier H
*APT attacker model > Evaluation metrics > MTD effectiveness*

> It is 0 when MTD has no effect, 1 when no host is compromised under MTD, and negative when MTD raises NCR. It takes the form of the mitigation factor of Alavizadeh et al. [Eq. 13 alavizadeh2022], with NCR in place of annual loss expectancy and no floor at 0.

Context before: [U0563] \paragraphNCR reduction. NCR reduction is the share of an attacker's NCR that MTD removes:

Context after: [U0566 cites brown2023] \paragraphAttack actions blocked per MTD deployment. Attack actions blocked per MTD deployment is the number of attack actions MTD disrupts, divided by the number of MTD deployments before the run ends, counting over every run [brown2023]:
