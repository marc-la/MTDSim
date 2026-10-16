# Packet: bland2020

2 units cite it; 0 more name its first author without citing it.

## Units that cite it

### U0442 (prose, L4947) tier V2
*APT attacker model > Integration with MTDSim > Tactic durations* · drafting trail: redrafted

> A tactic's duration is random each time it runs, an exponential delay, because the timed transitions of a GSPN fire after exponential delays (Section <sec:petri-formalism>) and attack behaviour is stochastic [holm2014, madan2004, bland2020].

Context before: [U0440] The tactic durations set how long each tactic takes, at step 3 of Figure <fig:runtime-loop>. [U0441] They set how often the APT attacker model acts, and the longer a tactic runs, the more likely an MTD deployment disrupts it.

Context after: [U0443] An exponential delay has one parameter, its mean, so each tactic needs one value, its mean duration $\mu_p$. [U0444] MTDSim times only its attack actions, and seven tactics are unmapped (Section <subsec:tactic-verb-mapping>), so each tactic has a mean duration of its own.

### U0458 (prose, L4996) tier V2
*APT attacker model > Integration with MTDSim > Tactic durations*

> We set their mean durations by judgement, from what each tactic does in an attack, as other models that time attack steps do where data are missing [mcqueen2006, bland2020, mendonca2023].

Context before: [U0456] Reconnaissance and Discovery survey a network, as MTDSim's scans for hosts, ports and neighbours do together, so each takes the total time of the three scans, 35 s. [U0457] No source times the other nine tactics, since threat reports time whole intrusions.

Context after: [U0459] Chapter <ch:experiments> compares the APT attacker model with the baseline attacker under the same MTD deployments, so we kept the nine on the scale of the baseline attacker's attack actions (Section <subsec:attacker-model>). [U0460] We also kept each under the 200 s default deployment interval (Section <subsec:defence-mechanisms>), or a deployment would disrupt most runs of the tactic.
