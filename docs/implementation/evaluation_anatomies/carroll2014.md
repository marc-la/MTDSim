# carroll2014 — evaluation-section anatomy

Source read: /home/marc/GitHub/MTDSim/docs/sources/tactic_profiles/step_d/1_recon/Analysis_of_network_address_shuffling_as_a_moving_target_defense.md (240 lines; clean md; equations dropped by the converter — equation bodies (1)–(6) are absent, only their prose lead-ins survive; figures present as picture-text with captions). Locators cited as `Analysis_of_network_address_shuffling_as_a_moving_target_defense.md:<line>` (abbreviated `carroll.md:<line>` below).

Paper's own research question / purpose: "This paper introduces probabilistic models that can provide insight into the performance of address shuffling. These models quantify the probability of attacker success in terms of network size, quantity of addresses scanned, quantity of vulnerable systems, and the frequency of shuffling." (carroll.md:15); it asks "if and when address shuffling is advantageous" (carroll.md:63). Primarily an analytical paper; simulation is a supporting empirical check.

## A. Skeleton of the evaluation portion

Verbatim headings:
- `III. MODELS FOR NETWORK SHUFFLING DEFENSES` (:61) — setup (assumptions list :65–77; two statistics of interest :79). `A. Urn-Based Models` (:81), `B. Modeling Static Addresses` (:89), `C. Modeling Perfect Address Shuffling` (:99).
- `IV. ANALYSIS OF SHUFFLING DEFENSES` (:119) — results. `A. Network Address Space (one vulnerable computer)` (:123), `B. Percentage of Address Space Probed` (:131), `C. Number of Vulnerable Computers` (:149), `D. Expected Number of Probes` (:168), `E. Address Shuffle Frequency` (:174) — the last is the only simulation subsection, and it contains its own setup paragraph (:182–184) before its results (:186).
- `V. CONCLUSIONS` (:199) — discussion and limitations folded here.

Setup and results are two sections for the analytical part (§III models, §IV analysis); for the simulation part, setup and results are one subsection (§IV-E). No section titled Discussion, Limitations, Experimental Setup, or Evaluation.

## B. Setup — what is declared before any result

**Network configuration(s).**
- Analytical: abstract address space of n addresses with v ≤ n vulnerable computers (:65). Concrete values appear per-figure: "a class-C network (255 addresses)" (:135), "a class-C network" (:166).
- Simulation (§IV-E): "a class-C IP network defended using address shuffling" (:182); "one of 10 vulnerable systems within the network" (:182). Single configuration. How chosen: not stated beyond class-C.
- Topology: not stated (flat address space).

**Attacker model / scenarios.**
- Defined as an assumption list (:65–77), not bold-named: "The attacker is aware of the address space (n addresses) and will serially attempt k connections (probes)." (:75); "The goal of the attacker is to contact at least one of the v vulnerable computers in k attempts." (:77).
- Under static addresses, "the attacker's strategy for finding a vulnerable system is to sequentially iterate through the address space" (:91); "The optimal strategy of the attacker is to explore the entire address space, never contacting the same host twice." (:29).
- Simulation: "The attacker is allowed to make 255 probes, in an attempt to find one of 10 vulnerable systems within the network. The probes occur serially, each lasting 32 milliseconds, which is commensurate with the model developed in the previous section." (:182). One attacker scenario only. The 32 ms figure is not justified beyond "commensurate with the model".

**Defence conditions.**
- Two analytical extremes: "static addressing (no shuffling) and perfect shuffling (shuffle after each probe)" (:87); shuffle "randomly and uniformly remaps all n addresses" (:73).
- Simulation: "The shuffling rate varied from never occurring (static addresses) to shuffling after every probe (perfect shuffling)... normalized value, where zero represents no shuffling (static addresses) and one is perfect shuffling. Therefore a shuffle rate of 0.5 indicates that a shuffle event occurred after half of the probes were attempted" (:184).
- No-defence baseline: yes — static addressing is the zero of the shuffle-rate axis (:184) and the comparator in every analytical subsection (:125, :133, :151).
- Schedulers/strategies: single periodic-by-probe-count scheme.

**Parameter table.** No. Parameters are declared in prose: n, v, k (:65–77), 255 addresses, 10 vulnerable, 255 probes, 32 ms per probe (:182). Distributions declared: yes for the models — hypergeometric (:93), negative hypergeometric (:97), binomial (:105), geometric (:109); shuffle is "randomly and uniformly" (:73); simulation connection destinations "randomly associated ... with an address within the class-C address space" (:182).

**Replications.** "For each possible shuffle rate 100,000 experiments were performed." (:184). Horizon: 255 probes (:182). Termination rule: implicit — probe budget exhausted or a vulnerable system contacted (:77, :182); not stated as a list. Seeds: not stated.

**Statistics.** "The average connection loss, attacker success probabilities, and expected number of vulnerable computers contacted were recorded." (:184). Means only; no std, CI, or tests stated. Analytical results are exact probabilities.

**Other declarations.** Trace data: "Network traces were collected from the Dartmouth University CRAWDAD project ... For each trace, the TCP connection start times and durations were identified." (:182). Simulator: "A network simulation program was then developed" (:182) — unnamed, no language/version, no availability. Hardware: not stated. "Note, a more detailed model description can be found in [8]" (:79) — a master's thesis.

## C. Results — how the numbers are shown

**Order.** One parameter per subsection, in the order the model's variables were introduced: network size n (§IV-A), probes k (§IV-B), vulnerable count v (§IV-C), expected probes (§IV-D, no figure), then shuffle frequency (§IV-E, simulation). The section preamble announces this as an impact-of-variables analysis: "This section will analyze the impact of these variables on the benefit and cost of static addressing and perfect shuffling under certain conditions. Although not exhaustive, the examples will provide guidance in the use of shuffling." (:121). The analytical results precede the empirical one, and the empirical one is positioned as verifying the model ("which is predicted by the theoretical models", :186).

**Figures.**
- Fig. 1 (:140): line; x = size of network address space (log scale, 10^0–10^4); y = attacker success probability; one series (perfect shuffling, k = n). Caption: "The attacker success probability for finding the vulnerable computer as the network size increases. The attacker can make n probes... Note, the the x-axis is in log scale."
- Fig. 2 (:145): line; x = percentage of the address space probed (0–100); y = attacker success probability; series = Static addresses, Perfect Shuffle. Caption: "... Only one vulnerable computer exists in the class-C network space."
- Fig. 3 (:162): line; x = percentage of the address space vulnerable (log scale 10^0–10^2); y = attacker success probability; one series (perfect shuffling, k = n). 
- Fig. 4 (:197): line; x = shuffle rate (0–1 normalised); y = probability; series = Attacker success, Connection loss. Caption: "The average percentage of vulnerable computers contacted as the normalized shuffle rate increases... Network contained 10 vulnerable computers in a class-C address space." (Caption says "percentage of vulnerable computers contacted", axis label says "probability", prose says "attacker success probability" — recorded as-is.)

**Tables.** None.

**Baseline appearance.** Static addressing is a series in Fig. 2 (:143), the x = 0 point in Fig. 4 (:186), and stated in prose as providing "no defense" in Figs 1 and 3 (:125, :151–165) rather than plotted.

**Comparison phrasing.**
- Magnitude: "perfect shuffling reduces the probability of attacker success by 37% as compared to using static addresses" (:129); converges "to e^{-1} ≈ 0.63" (:127).
- Ordering: "Comparing perfect shuffling to static addressing, perfect shuffling provides an improved defense." (:147); "perfect shuffling always requires more probes; however, this advantage decreases as the percentage of systems that are vulnerable increases" (:172).
- Conditional/recommendation: "perfect shuffling is only beneficial if there is a relatively small number, less than 1% in this example, of vulnerable computers in the network" (:166); "a lower shuffling rate can provide a comparable defense to perfect shuffling but with a lower loss probability" (:186).
- Verification language: "which is predicted by the theoretical models in the previous sections" (:186); "again predicted by the theoretical models" (:186).

## D. Narrative — the claims, in order

1. With one vulnerable computer and k = n, static addresses "provide no defense" while perfect shuffling depends on network size (:125).
2. Success under perfect shuffling falls with network size and "converges to e^{-1} ≈ 0.63" (:127); "perfect shuffling reduces the probability of attacker success by 37%" (:129).
3. Static success grows linearly in k/n; perfect-shuffle success "slowly increases" to ≈ 0.63 at full probing (:133–135; Fig. 2).
4. "perfect shuffling provides an improved defense" (:147).
5. As v grows, perfect-shuffle success "approaches one"; benefit only when < 1% of addresses are vulnerable (:166; Fig. 3).
6. Perfect shuffling always needs more probes, advantage shrinking with vulnerable fraction (:172).
7. Simulation: static → no loss, attacker 100%; success drops with shuffle rate "as predicted"; perfect shuffling ≈ "0.63 percent" [sic] (:186); connection loss rises slowly until ≈ 0.85 shuffle rate (every 38 probes); lower rate gives comparable defence at lower loss (:186).

**Claims about the attacker from the data.** The analytical results are stated as attacker success probability, but the attacker's strategy is an assumption, not something inferred. The conclusion makes an attacker-adaptation claim without data: "an attacker who has gained a user level perspective... Once this occurs—and no doubt it will occur as the adversaries evolve their tactics in response to moving target defenses—the size of the pool doesn't matter." (:207). No claim about attacker properties is derived from the simulation.

## E. Sensitivity / parameter analysis

Present, and it constitutes the whole results section: one-at-a-time sweeps of n (Fig. 1, 10^0–10^4), k as a fraction of n (Fig. 2, 0–100%), v as a fraction of n (Fig. 3, 10^0–10^2 %), and shuffle rate (Fig. 4, 0–1). Not grid/factorial; each sweep holds the others at a stated value (one vulnerable computer :125, :133; k = n :151; class-C :135, :166, :182). Range justification: not stated beyond class-C being a concrete example. Reported as figures only. Sits inside §IV as the results themselves (no separate sensitivity section). Claims supported: the "small population of vulnerable systems within a large network address space" condition (:15, :166, :203) and the shuffle-rate/connection-loss trade-off (:186).

## F. Discussion / limitations

No separate discussion section; interpretation is in §V Conclusions (:199–209). Contents: restatement of the dependence on n, v, k (:203); the conditional verdict ("shuffling provides some protection for networks that have very few vulnerable systems; otherwise shuffling provides limited benefit", :203); a cost verdict ("the expense of shuffling (impact on legitimate connections) might be considered too high for realistic use", :203); an attacker-realism concession that the model ignores a user-level attacker (:205–207); and future work (:209).

Verbatim limitation sentences:
- "Although not exhaustive, the examples will provide guidance in the use of shuffling." (:121)
- "Studying this shuffling cost, referred to as the drop probability, is problematic since it relies on assumptions about network connection arrival patterns. Here, as in [3], the performance and cost of shuffling are studied empirically in this section." (:180)
- "the models and attack scenarios presented in this paper indicate shuffling has defense benefit that is likely less than originally perceived" (:205)
- "This paper analyzes the extreme cases of shuffling (zero shuffling to perfect shuffling). The development of a theoretical model for infrequent shuffling would be beneficial and is currently under consideration. Beyond infrequent shuffling, the model can be employed to study parallel probes, in which the attacker performs multiple probes between shuffle events." (:209)
- Comparability caveat aimed at prior empirical work: "the findings of these studies are typically limited to very specific scenarios (e.g. certain network address space size)" (:27) — used to motivate the model, not to caveat the paper's own simulation.
Replication statement: none (simulator unnamed, not released; trace source cited :182, :235).

## G. Transferable vs purpose-specific

**Transfers:**
- Declaring the attacker as a short numbered/bulleted assumption list before any model or result (:65–77), and naming the two statistics of interest up front (:79).
- One-parameter-per-subsection results structure with the section preamble naming the variables to be swept (:121) — a clean way to organise a sensitivity analysis when it is the main result.
- Static/no-defence as the zero of the defence-intensity axis (:184) and "no defense" stated in prose when it would be a flat line (:125).
- Pairing the security metric with a cost metric on the same axes (Fig. 4: attacker success vs connection loss) to argue a trade-off.
- Using an analytical limit (e^{-1}) as a sanity check on simulation output ("predicted by the theoretical models", :186).
- Stating the replication count in one sentence next to the swept parameter (:184).
- Conceding the attacker-adaptation gap explicitly in the conclusion (:207).

**Purpose-specific:**
- The urn-model framing and closed-form distributions (:93–109) — the paper's contribution is the model; the simulation exists to verify it.
- "Perfect shuffling" as a theoretical extreme (:87, :103) rather than an implementable scheduler.
- Real-trace replay (CRAWDAD) to drive the cost metric (:182) — needed because connection loss is the cost of interest here.
- Single attacker scenario (serial probes, find one of v) and single class-C network; no parameter table, no seeds — a 6-page ICC paper.
- 100,000 replications (:184) is cheap for a probe-counting simulator; not a norm to import.
