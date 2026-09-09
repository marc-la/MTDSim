# crouse2015 — evaluation-section anatomy

Source read: /home/marc/GitHub/MTDSim/docs/sources/tactic_profiles/step_d/1_recon/2808475.2808480.md (313 lines; clean md, read in full. Equation bodies (1)–(9) were dropped by the converter — only the prose lead-ins survive, e.g. ":88" ends "the probability of drawing at least one green marble is," with nothing after it. Figures survive as garbled "picture text" blocks whose axis labels and legend entries are recoverable, with intact bold captions.) Locators are md line numbers, cited as `2808475.2808480.md:<line>` (abbreviated `crouse.md:<line>`).

Paper's own research question / purpose: "This paper introduces probabilistic models for reconnaissance defenses to provide deeper understanding of the theoretical effect these strategies and their parameters have for cyber defense. The models quantify the success of attackers under various conditions, such as network size, deployment of size [sic], and number of vulnerable computers." (crouse.md:13). The framing question is economic: "given the benefit and cost associated with reconnaissance defenses, understanding under what circumstances they are most effective is important" (:23). This is a modelling paper (MTD'15 workshop, 9 pages incl. refs); the simulation in §5 exists to cover the cases the closed-form model cannot reach.

## A. Skeleton of the evaluation portion

Verbatim headings (md line):

- `3. RECONNAISSANCE PERFORMANCE MODELS` (:49) — setup. Urn framing (:51), five-bullet network/attacker assumption list (:55–63), marble colouring (:74–76). `3.1 Undefended Model` (:78), `3.2 Honeypot Defense Model` (:92) with `3.2.1 Allowable Losses` (:104), `3.3 Shuffling Defense Model` (:110) — the shuffling model is not derived here, it is imported from Carroll et al. [4] (:112).
- `4. ANALYSIS OF HONEYPOT DEFENSES` (:124) — results (analytical). Preamble defines the two attack goals (:126–128). `4.1 Foothold Scenario` (:130) with `4.1.1 Number of Scans` (:134), `4.1.2 Number of Honeypots` (:147), `4.1.3 Honeypot Deception` (:158), `4.1.4 Allowable Losses` (:171). `4.2 Minimum to Win Scenario` (:177) with `4.2.1 Number of Scans` (:190), `4.2.2 Number of Honeypots` (:196), `4.2.3 Number of Vulnerable Computers` (:219).
- `5. COMPARING AND COMBINING RECONNAISSANCE DEFENSES` (:223) — setup **and** results in one section. The whole simulation setup is two unnumbered paragraphs (:229 simulator/traces/network; :231 attack scenario/termination/replications) before any subsection. `5.1 Foothold Scenario` (:233), `5.2 Minimum to Win Scenario` (:239), `5.3 Shuffling Drop Probability` (:257).
- `6. CONCLUSIONS` (:272) — three paragraphs; all discussion is here.

Setup and results are **two sections for the analytical half** (§3 models, §4 analysis) and **one section for the empirical half** (§5 carries its own setup inline). There is no section titled Experimental Setup, Evaluation, Discussion, Limitations, Related Work, or Threats to Validity. The intro roadmap (:31) matches the actual numbering.

Structural note: §4.2.3 (:219–221) has a title and a paragraph but **no figure and no completed result** — it sets up the vulnerable-computer sweep ("consider a class-C network and the attacker seeks to contact at least 16 computers in 64 scans (25% of the addresses)"), states only the trivial no-honeypot case, and then §5 begins. Recorded as-is; the subsection appears truncated.

## B. Setup — what is declared before any result

**Network configuration(s).**
- Analytical: abstract address space, "There are _n_ total addresses available to the administrator (address space) and _v ≤ n_ vulnerable computers." (:55); "There are _h_ honeypots within the network." (:57). "Note _n_ is equal to the number of addresses, not the number of computers within the network." (:74).
- Every analytical example instantiates the same single network size — "a class-C network (255 addresses)" (:136) — with the vulnerable fraction varying **between** subsections without justification: 25% vulnerable in §4.1.1 (:136), 10% in §4.1.2 (:156), 10% in §4.1.3 (:160), 10% in §4.1.4 (:175), 25% in §4.2.1 (:192), 10% in §4.2.2 (:217).
- Simulation: "a class-C network, 255 addresses" (:229). Address set is resampled per run: "The traffic consists of over 1,000 unique destination IP addresses, of which 255 were randomly chosen for each simulation" (:229). "For the simulations 10% of the addresses contained vulnerable computers, while 4% of the addresses were designated as honeypots." (:229) — the 4% honeypot level matches none of the analytical levels (1/5/10%); no statement reconciles them.
- Topology: not stated anywhere; flat address space in both halves. How the class-C size was chosen: not stated.

**Attacker model / scenarios.**
- Declared as a five-bullet assumption list before any model (:55–63), not bold-named: "The attacker is aware of the address space (_n_ addresses) and will serially attempt _k_ connections, _k < n_." (:61); "Given _k_ attempts, the attacker wins if they are able to locate _m_ vulnerable computers within the network **without** contacting and being deceived by a honeypot." (:63); "The attacker has probability _d_ of being deceived by a honeypot." (:59).
- Serial/parallel equivalence stated as a property of the model, not a scenario: "These reconnaissance actions are modeled as either _k_ individual draws (serial) or a single draw of _k_ marbles from the urn (parallel)." (:76); the "without replacement" condition is what licenses it (:82, :96).
- **Two scenarios, italic-defined once each** in the §4 preamble: "the establishment of a _foothold_ in the targeted network" (:126) and "to compromise a minimum number of computers (_minimum to win_) within the targeted network" (:128). Each gets a motivating story — foothold: a target behind a firewall, "This strategy is a lower risk for the attacker as their actions can be more direct and precise, attracting less attention with this less pronounced behavior." (:126); minimum-to-win: "if the attacker's goal is to gain information that is distributed across multiple computers or if the goal is to acquire as many resources as possible, for example for botnet recruitment [12]" (:128). The same two names structure §5 (:233, :239), so the analytical and empirical halves share one scenario taxonomy.
- A third, sub-scenario axis: the "_well-resourced_ and determined attacker" willing to sustain L losses (:106, :173).
- Explicit attacker-behaviour assumption with a realism justification: "If they contact a honeypot before reaching the _k_^th scan, the attacker will continue to scan. This assumption is made to simplify the probability model. It also models reality in the case where the attacker's reconnaissance is automated, without carefully observing the result after each scan event. Therefore, contacting a honeypot would not cause the attacker, or script, to stop scanning." (:149).
- Simulation-only two-phase attacker: "an attack is divided into a reconnaissance phase followed by an attack phase. The attacker is allowed to attempt _k_ scans during the reconnaissance phase. The attacker will then attempt to compromise any vulnerable computers discovered during the first phase after waiting 10 minutes, termed the _attack wait time_." (:231). The 10-minute value is not justified at the point of use; a citation for attacker patience appears later, in §5.3 (:270).
- Uncited attacker-effort claim in the background: "it has been found that well-resourced adversary can spend approximately 45 percent of his time performing reconnaissance" (:35) — no reference attached.

**Defence conditions.**
- Analytical: honeypots (§3.2) and shuffling (§3.3, imported from [4] as "_perfect shuffling_, where the administrator shuffles after every reconnaissance attempt … Although perfect shuffling is difficult to implement in practice, the model provides an upper bound on the defense performance [4]", :112).
- Simulation: **four conditions**, named in the figure legends — "No defense", "Shuffle", "Honeypot", "Shuffle and honeypot" (:244, :249). The combined condition is the paper's headline contribution.
- Failure semantics per defence stated once, in the setup paragraph: "An attack is deemed successful if a vulnerable computer is contacted during both phases. When honeypots are used as a defense, the attacker fails if a honeypot is contacted in either phase. When address shuffling is used as a defense, the attacker fails if reconnaissance reveals a vulnerable computer that cannot be subsequently contacted during the attack phase due to a shuffle event." (:231).
- No-defence baseline: yes, in both halves — "No defense" is a plotted series in Figures 2, 4, 5, 6, 9, 10, and is stated in prose where it would be trivial (:80, :156, :221).
- Scheduler: shuffling is expressed only as an **inter-shuffle time relative to the attack wait time** — "Results reference the ratio of inter-shuffle time to attack wait time; therefore, a ratio of 2 indicates the inter-shuffle time is twice as long as the attacker wait time." (:235). §5.2 fixes it: "the inter-shuffle time was 20 minutes." (:253). No alternative shuffling strategies.

**Parameter table.** **None.** All parameters are declared in prose or in the §3 bullet list: n, v, h, d, k, m, L (:55–63, :106). Concrete values appear in the sentence introducing each figure ("consider a class-C network where 10% of the addresses are vulnerable computers and the attacker is able to scan 10% of the address space", :160). Distributions declared: yes, and each is named and defined — hypergeometric, quoted as "number of successes in a sequence of _k_ draws from a finite population without replacement" [11] (:82); multivariate hypergeometric (:96); binomial, quoted as "number of successes in a sequence of k draws from a finite population with replacement" (:114); geometric (:118). For the simulation, the only stochastic element declared is the random draw of 255 addresses from the trace (:229) and the random assignment of address types (:229).

**Replications.** "Each experiment was simulated 1000 times to provide a stable sample of the attacker success rates under each defense mechanism." (:231). One sentence, in the setup paragraph, with a stated purpose ("a stable sample") but no variance evidence. Horizon: the two phases (k scans, then 10-minute wait, then the attack), with the run ending on success or failure per :231 — the termination rule is embedded in the success/failure sentences, not listed. Seeds: not stated. Total cell count: not stated.

**Statistics.** Every figure caption reads "Average attacker success probability …" (:143, :154, :169, :186, :205, :210, :215, :246, :251) — means only. No std, no CI, no min/max, no significance test, no error bars mentioned anywhere. The analytical figures are exact probabilities but carry the same word "Average" in their captions.

**Other declarations.** Simulator: "A discrete event simulator was created to collect empirical data." (:229) — unnamed, no language, no version, no availability statement. Traces: "we utilize the 2008 SIGCOMM conference packet traces, using the flow start and end times for both normal and attacker connections for a class-C network, 255 addresses [15]. These traces are primarily web-oriented, with the majority of the flows consisting of DNS or HTTP." (:229); reference [15] is a bare URL (:308). Hardware: not stated. Runtime: not stated.

## C. Results — how the numbers are shown

**Order.** Two-level. Across the paper: **model first, simulation second** — §4 exhausts the analytical honeypot results, §5 then runs the simulation for what the model cannot cover, with the reason stated up front: "Theoretical performance models do exist for the use of network address shuffling in isolation under certain assumptions about the shuffling epoch [4]; however, modeling shuffling under more realistic attacker scenarios where the attacker needs to both locate and reliably compromise a set of machines is more challenging." (:225). Within §4: **scenario × parameter grid** — the two scenarios are the subsections, and inside each, one parameter per sub-subsection, with the parameter order repeated across scenarios (scans, honeypots, then a scenario-specific extra: deception + allowable losses for foothold; vulnerable count for minimum-to-win). Within §5: the same two scenarios, then the cost metric last (§5.3).

**Figures (evaluation portion) — 10 in total, all line charts, all with y = attacker success probability except Fig. 11.**

Analytical (§4):
- Figure 2 (:143): x = percentage of address space scanned (0–100); series = No defense, 1% honeypots, 5% honeypots, 10% honeypots. Caption: "Average attacker success probability for gaining a foothold in a class-C network as the number of attacker scans increases. Different lines represent different percentages of honeypots deployed." Network: 25% vulnerable (:136).
- Figure 3 (:154): x = percentage of honeypots within the address space (0–80); series = 5% scan, 10% scan, 20% scan, 50% scan. Caption: "… as the number of honeypots deployed increases. Different lines represent different attacker scan rates." Network: 10% vulnerable (:156).
- Figure 4 (:169): x = honeypot deception probability (0–1); series = No defense, 1%, 5%, 10% honeypots. Caption: "… as the honeypot deception probability increases."
- Figure 5 (:186): x = number of allowable losses (0–8); series = No defense, 1%, 5%, 10% honeypots. Caption: "… as the number of allowable losses increases."
- Figure 6 (:205): x = percentage of address space scanned (0–100); series = No defense, 1%, 5%, 10% honeypots. Caption: "Average attacker success probability of obtaining at least 16 of the 64 vulnerable computers (minimum to win) in a class-C network as the number of attacker scans increases."
- Figure 7 (:210): x = percentage of address space scanned (0–100); series = "Min is 5% of vulnerable", "Min is 10% …", "Min is 25% …"; y range 0–0.4. Caption fixes the held-constant values: "The network had a class-C address space and the 5% of the addresses were honeypots." **No "No defense" series in this one.**
- Figure 8 (:215): x = percentage of honeypots within the address space (0–16); series = 5%, 10%, 20%, 50% scan; y range 0–0.5. Caption: "Average attacker success probability of obtaining at least 6 of the 25 vulnerable computers (minimum to win) …". **No "No defense" series.**

Simulation (§5):
- Figure 9 (:246): x = ratio of shuffle time to attack time (0–3); series = No defense, Shuffle, Honeypot, Shuffle and honeypot. Caption: "Average attacker success probability for gaining a foothold in a **simulated** class-C network as the ratio of shuffle time to attack increases. Different lines represent different defenses." (emphasis added — "simulated" is the only word distinguishing the empirical captions from the analytical ones).
- Figure 10 (:251): x = percentage of vulnerable computers necessary for the attacker (0–40); same four series. Caption: "… in a simulated class-C network."
- Figure 11 (:266): x = ratio of shuffle time to attack time (0–3); y = **connection drop probability** (0–0.12); one series, no legend. Caption (truncated in the original): "Connection drop probability as the shuftime increases."

**Tables.** None, anywhere in the paper.

**Baseline appearance.** "No defense" is a plotted line in Figures 2, 4, 5, 6, 9, 10; absent from Figures 3, 7, 8 (where its value is instead given in prose — "the probability of attacker success when there are no honeypots within the space is proportional to the scan rate, which is equivalent to no defense discussed in Section 3.1", :156; "The probability of success when there are no honeypots is the same as the no defense case.", :221); and irrelevant to Figure 11 (a cost-only plot). In the simulation figures the baseline is one of four defence conditions, not a separate reference line.

**Comparison phrasing.**
- Point-value magnitude, read off the figure: "the attacker has a maximum success rate of 62% percent with a 2% scan rate" (:145); "With 10% honeypots the maximum success rate for the attacker falls below 50%." (:145); "If no defense is provided, the attacker success probability is 93%. With 5% honeypots deployed, the attacker is success rate drops to 50% if the detection rate is 50%. In contrast, with 10% honeypots the success rate drops to 25% …" (:160); "the drop probability for legitimate connections is approximately 0.04 when the inter-shuffle time equals the wait time" (:270).
- Ordering, always conditional on a crossover point: "Once the shuffle time was greater than the attack wait time, the honeypot-only defense performed better than the shuffle-only defense." (:237); "once more than one vulnerable computer was required for the attacker to win (8% of the vulnerable), shuffling performed slightly better than the honeypot-only defense" (:255).
- Best-of ordering: "The combination of shuffling and honeypots provided the best defense, since both are capable of defending against an attack." (:237).
- Shape claims rather than numbers: "The reduction is increasingly sub-linear with larger populations of honeypots." (:160); "The probability of success decreases dramatically at a scan rate of 50% as the number of honeypots increases only slightly." (:217).
- Recommendation, with an external citation supplying the operational constant: "According to Rowe and Goh, attackers can wait up to a day before acting on reconnaissance information [16]. Then it would be reasonable to have network shuffles only a few times a day, limiting the overhead of shuffling while interrupting a very small percentage of daily network traffic." (:270); "The addition of a few honeypots can further reduce the shuffling frequency (thus increasing inter-shuffle period) necessary for a desired attacker success rate." (:270).
- Expectation-confirmation language used repeatedly as the interpretive move: "As expected, the probability of attacker success when there are no honeypots … is proportional to the scan rate" (:156); "This is expected since the population of undetectable honeypots is increasing" (:160); "This is expected since the shuffle time is twice the attack wait time." (:255); "As the intershuffle time increases, the drop probability continues to decrease as expected." (:270).

## D. Narrative — the claims, in order

Analytical (§4):
1. Scanning more is not monotonically good for the attacker once honeypots exist — with 1% honeypots "the probability of success increases until the scan rate reaches 5% of the address space. After this scan rate, the attacker is more likely find a honeypot" (:145). This inverted-U is the paper's first substantive result.
2. Honeypot density has a large, scan-rate-independent effect: "increasing the number of honeypots does cause the probability of success to quickly decrease. This trend is also independent of the number of scans performed" (:156).
3. Attacker ability to detect honeypots degrades the defence smoothly and sub-linearly (:160).
4. Allowable losses restore the attacker: "The maximum success rate is achieved once the number of allowable losses is equal to pre greater than [sic] the number of deployed honeypots." (:175).
5. Minimum-to-win has a hard floor: "The case of no defense is similar to Figure 2, except there is a zero probability of success until the attacker is able to make at least 16 scans." (:192); "Even deploying 1% honeypots has a dramatic effect." (:192).
6. Raising the required minimum lowers success monotonically (:194).
7. (§4.2.3 states no result — see §A.)

Simulation (§5):
8. Shuffling's benefit is a function of the shuffle:wait ratio — "As the shuffle time increased … the attacker success rate also increased since the likelihood of a shuffle event occurring between reconnaissance and attack was less likely." (:237).
9. Crossover: honeypot-only beats shuffle-only once shuffle time exceeds wait time (:237).
10. Layering wins, and degrades gracefully to its stronger component: "as the shuffle time increased the defensive effect of shuffling decreased and as expected, and the performance of the combined defense approached a honeypot-only defense." (:237).
11. In minimum-to-win the shuffle/honeypot ordering **flips** relative to foothold once >1 machine is required (:255).
12. Cost: drop probability ≈0.04 at ratio 1 and falls with longer inter-shuffle times, i.e. the cost and the benefit move together (:268–270).

**Claims about the ATTACKER's properties from the data.** Two kinds, and the paper does not distinguish them.
- Derived-from-model claims about attacker *capability under assumptions*: "The figure demonstrates that well-resourced and determined attacker has a high success rate given an allowable number of losses." (:175); "This shows the difficulty of locating an increasing minimum number of vulnerable computers." (:194). These are re-descriptions of the swept parameter, not inferences about a real attacker.
- Attacker *timing* as an input, not an output: the 10-minute attack wait time is a stipulated parameter (:231), and the one real-world attacker-behaviour figure — "attackers can wait up to a day before acting on reconnaissance information [16]" (:270) — is imported from the literature and used to convert the ratio axis into an operational recommendation. Nothing about the attacker is inferred from the simulation output.
- The attacker's honeypot-detection ability (d) is likewise a swept input justified by citation, not measurement: "techniques do exist for determining if a device is a honeypot [13, 14]" (:160).

## E. How the analytical model and the simulation are reconciled

This is the paper's distinguishing feature, so recorded separately from the sensitivity analysis.

- **Division of labour, stated once.** The simulation is justified by a gap in the model's reach, not by a need to validate it: "modeling shuffling under more realistic attacker scenarios where the attacker needs to both locate and reliably compromise a set of machines is more challenging" (:225). The model gives honeypots (derived here) and shuffling in isolation (imported from [4], :112); the simulation gives the *combination*, the two-phase attack, and the connection-drop cost.
- **Shared scenario taxonomy.** §4.1/§4.2 and §5.1/§5.2 carry the same two subsection titles (Foothold Scenario, Minimum to Win Scenario), so a reader can line the two halves up by scenario. §5.1 opens by pointing back: "As described in section 4, the foothold attack scenario requires the attacker contact at least one vulnerable computer." (:235).
- **One explicit cross-check, in prose, on one series only.** "The attacker success rate with the honeypot-only defense remains constant as predicted by Equation 4." (:237). That single sentence is the whole of the model↔simulation agreement claim: the honeypot arm of the simulation is flat across the shuffle-ratio axis, which is what the closed-form model requires (the model has no time dimension). No numeric agreement is quoted, no error is computed, and the other three simulated conditions are never compared to a model prediction.
- **No overlay.** No figure plots analytical and simulated curves on the same axes; no table compares predicted vs observed. Figures 9–11 are captioned "simulated" (:246, :251) and Figures 2–8 are not — that adjective is the only in-figure marker of which half a result belongs to.
- **Parameters are not held common across the two halves.** Analytical honeypot levels are 1%, 5%, 10% (:143) and vulnerable fractions are 10% or 25%; the simulation fixes 4% honeypots and 10% vulnerable (:229). No sentence reconciles the 4% choice with the analytical levels, so the two halves are not numerically comparable point-for-point.
- **The imported model does double duty.** §3.3's shuffling model is Carroll et al. [4] restated (:112), and §5.3 closes by referring the inter-shuffle-time trade-off back to that same source: "Therefore as discussed in [4], finding the correct inter-shuffle time required some knowledge of the attack wait and average legitimate connection time." (:270). The empirical drop-probability curve (Fig. 11) is thus positioned as the empirical counterpart of a prior paper's analytical claim, not of this paper's.
- **Replication count is asserted as sufficient without evidence:** 1000 runs "to provide a stable sample" (:231); no convergence check, no variance reported, so the reader cannot verify that simulated and analytical values agree to within noise.

## F. Sensitivity / parameter analysis

Present, and — as in carroll2014 — it *is* the results section rather than a separate part.

- **Structure:** strictly one-at-a-time, one parameter per sub-subsection, with the sub-subsection title being the parameter name ("Number of Scans", "Number of Honeypots", "Honeypot Deception", "Allowable Losses", "Number of Vulnerable Computers"). Not grid/factorial: each figure sweeps one x-variable, uses a second variable as the series, and pins the rest in the introducing sentence.
- **Parameters and ranges:** scan rate 0–100% of address space (Figs 2, 6, 7); honeypot density 0–80% (Fig. 3) and 0–16% (Fig. 8); honeypot deception probability d, 0–1 (Fig. 4); allowable losses L, 0–8 (Fig. 5); minimum-to-win requirement 5/10/25% of vulnerable (Fig. 7) and 0–40% (Fig. 10); shuffle-to-attack-time ratio 0–3 (Figs 9, 11). Network size n is **not** swept (unlike carroll2014, which sweeps it) — it is fixed at class-C throughout.
- **Range justification:** not stated for any range. The one range that is implicitly bounded by the model is Fig. 3's honeypot axis: "To analyze the impact of different honeypots, the number of scans within the network must be _k < n − hd_. If not, the probability of attacker success is zero following the same logic." (:149).
- **Reporting:** figures only, no tables, no tornado/one-factor summary.
- **Placement:** inside §4 and §5 as the results themselves; no appendix, no separate sensitivity section.
- **Claim supported:** the deployment-guidance headline — "a relatively small number of deployed honeypots can provide an effective defense strategy, often better than movement alone" (:13) — plus the layering claim (:13, :274).

## G. Discussion / limitations

**No separate discussion section.** Interpretation is distributed: (i) inline after each figure in §4/§5, (ii) the operational-recommendation paragraph at the end of §5.3 (:270), and (iii) §6 Conclusions (:272–276). There is no threats-to-validity paragraph, no comparability caveat about the trace source, and no statement of what the model's assumptions exclude.

Verbatim sentences that carry limitation content (they are scattered, and mostly framed as assumptions or as future work rather than as limitations):
- "Although perfect shuffling is difficult to implement in practice, the model provides an upper bound on the defense performance [4]." (:112)
- "This assumption is made to simplify the probability model. It also models reality in the case where the attacker's reconnaissance is automated, without carefully observing the result after each scan event." (:149)
- "Performance analysis thus far has assumed the attacker is unable to distinguish a real device from a honeypot; however, techniques do exist for determining if a device is a honeypot [13, 14]." (:160) — a limitation named and then immediately dissolved by adding the parameter d.
- "modeling shuffling under more realistic attacker scenarios where the attacker needs to both locate and reliably compromise a set of machines is more challenging" (:225)
- "Determining the best time for a shuffle is important as well (i.e., shuffling during business hours may be too disruptive)." (:270)
- "The models introduced can help provide direction for honeypot deployment, and can serve as a framework to address additional questions. For example, reconnaissance defenses can have a high administrative cost. The defense performance models described in this paper can be combined with cost models to provide better deployment guidance." (:276) — future work standing in for the cost limitation the introduction raised (:23).

**Replication statement:** none. The simulator is unnamed and unreleased (:229); the trace source is cited as a bare URL (:308); no seeds, no code, no parameter table. The honest statement of what a reader could reproduce is: the analytical figures (from the named distributions and the stated class-C/percentage values), but not the simulation.

**Attacker-realism concessions:** two, both partial — the automated-scanner assumption (:149) and the honeypot-detectability parameter (:160). The paper does **not** concede that its attacker never adapts its scan rate, never re-scans after a shuffle, and has no knowledge of the defence — carroll2014, its own reference [4], does make the analogous concession in its conclusion.

## H. Transferable vs purpose-specific

**Transfers to an honours dissertation evaluating existing MTD mechanisms against a new attacker model on a simulator:**
- Declaring the attacker as a short bulleted assumption list before any model or result (:55–63), each bullet one sentence, with the win condition stated as a bullet (:63).
- Italic-defining each attacker scenario exactly once, at the head of the results section, with a one-paragraph motivating story (:126, :128) — then reusing those same scenario names as subsection titles in *both* the analytical and the empirical half, so the two can be read against each other.
- Naming an assumption, justifying it on realism grounds, and saying what it buys — the honeypot-continue-scanning passage (:149) is a compact template.
- Turning a defence's timing parameter into a **dimensionless ratio against an attacker timescale** (inter-shuffle time ÷ attack wait time, :235) rather than plotting seconds. It makes the crossover claim (:237) parameter-free and portable across networks.
- Pairing the security metric with a cost metric measured on the *same* x-axis (Fig. 9 vs Fig. 11 both on the shuffle:wait ratio) and then stating the trade-off in one paragraph (:270).
- Stating the replication count in the setup paragraph with its purpose attached — "1000 times to provide a stable sample" (:231).
- Marking simulated results in the figure caption ("in a simulated class-C network", :246) so caption text alone distinguishes model from measurement.
- Reporting *shape* claims (inverted-U, :145; sub-linear, :160; crossover point, :237) rather than only endpoint numbers — these survive parameter disagreement better than point values do.
- Using an external literature constant to convert a swept axis into an operational recommendation (:270).

**Purpose-specific / artefacts of this paper's venue and aim:**
- The urn framing and the four named distributions (:82–118) — the contribution is the model; a simulator-based dissertation inherits none of this machinery, though the *habit* of naming the distribution behind each stochastic choice does transfer.
- Importing the shuffling model wholesale from a prior paper (:112) and letting §5.3 defer its interpretation to that paper (:270) — a workshop-paper economy, not a standard.
- No parameter table and no seeds — acceptable at 9 pages with an analytical core; not acceptable for a simulation-first dissertation.
- Means-only reporting with no dispersion on 1000 stochastic runs (:231, captions) — the analytical half needs no error bars, and the empirical half inherits the convention. Do not import this.
- Varying the held-constant vulnerable fraction between subsections (25% in §4.1.1, 10% in §4.1.2–4, :136 vs :156) without comment — a defect, not a convention.
- The 4% simulated honeypot level matching none of the analytical levels (:229 vs :143) — the two halves cannot be lined up numerically, which is the cost of reconciling model and simulation only in prose.
- A single fixed network size (class-C, 255) across every result — the paper's parameter of interest is density, not scale.
- Real-trace replay (SIGCOMM 2008) purely to supply legitimate-connection start/end times for the drop-probability metric (:229) — needed only because connection loss is the cost of interest.
