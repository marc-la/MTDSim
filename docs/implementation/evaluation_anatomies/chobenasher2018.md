# chobenasher2018 — evaluation-section anatomy

Source read: `docs/sources/lit_review/chobenasher2018.md` (1267 lines) — Cho & Ben-Asher, "Cyber defense in breadth: Modeling and analysis of integrated defense systems", *Journal of Defense Modeling and Simulation* 15(2), 2018, pp. 147–160. **No PDF is held in the repo for this paper** (`docs/sources/lit_review/` has no `chobenasher2018.pdf`, and `original/` has no equivalent), so figure artwork could not be inspected — everything below about figures comes from their captions and the prose that reads them.

**Conversion quality — partial garbling.** The md is a text conversion of a two-column layout and is *readable but out of order in the results section*: at md:709–730 the metric-definition list is interrupted mid-item by equation (3) and the PAS bullet, which physically belong ~20 lines later; and in §5.3 the paragraphs are shuffled — "Figure 3(a) shows MTTSF …" (md:909) appears *before* the "Defense performance:" paragraph that introduces Figure 3 (md:916), and "In Figure 2(c) …" (md:924) appears before "In Figure 2(b) …" (md:940). Table 2 (md:862–905) and Table 3 (md:937–1015) are split into a column of labels followed by a column of values, and Table 3's rate column is interleaved with body text. Equations survive as broken inline fragments (`MTTSF= P i∈S R∞ t=0 ri Pi(t)dt`). Reading order was reconstructed by following the "Figure N(x)" references; where I reconstructed, I say so. Line numbers below are `chobenasher2018.md:<line>`.

Paper's own research question / purpose (one sentence): "we develop a probability model using Stochastic Petri Nets that describes an integrated defense system with the defense techniques of both intrusion detection (i.e., IDS) and intrusion prevention (i.e., honeypots and platform migration) and analyze its performance compared to single defense or partially integrated defense approaches" (md:14–19, abstract) — the object evaluated is the *degree of integration* of a defence portfolio; the attacker is a modelled behaviour set, not a treatment.

---

## A. Skeleton of the evaluation portion

Section numbering is Arabic (1–7). Setup and results **are two separate sections** (4 = model + metrics, 5 = results), and §5 opens with its own three-part scaffold — comparing schemes, experimental setup, results — before any number is shown. There is **no separate discussion section**: interpretation is folded into §5.3 and summarised in §6.

- **3. System model** (md:381) — [setup]
  - (untitled opening, md:437–441) — the node population and Pv
  - 3.1. Attack model (md:442) — five bulleted attacker behaviours
  - Figure 1 (md:483) — "Stochastic Petri Nets modeling the system integrated with intrusion detection system (IDS), moving target defense (MTD), and honeypots."
  - 3.2. Defense model (md:493) — three bulleted mechanisms (IDS, Deception, MTD) + the cost-weighting decision
- **4. Performance model** (md:557) — [setup]
  - 4.1. Stochastic Petri Nets (md:558) — a tutorial paragraph on SPN notation, then a transition-by-transition walkthrough of Figure 1 under seven bold run-in headings: "Access by an attacker", "Reconnaissance", "Defense by deception", "Attack failure due to deception", "Attacker's deception detectability", "Defense by MTD", "Defense by IDS", "Attack success" (md:583–708)
  - 4.2. Metrics (md:709) — four metrics, each a bullet with a reward-function equation, plus two derived unit-cost metrics
- **5. Numerical results and analyses** (md:774) — [setup + results]
  - 5.1. Comparing schemes (md:781) — the four conditions, each defined by *which SPN parameter is zeroed*
  - 5.2. Experimental setup (md:806) — network size, fixed probabilities, Table 2, Table 3
  - 5.3. Comparative performance analyses (md:834) — Figure 2 (attack side), Figure 3 (defence side), read panel by panel
- **6. Conclusion and future work** (md:1074) — findings recap + three numbered future-work items
- **7. References** (md:1131)

Tables and figures in the evaluation portion: Table 2 "Key design parameters, their meanings, and their default values" (md:862), Table 3 "Transition names, meanings, rates, and enabling conditions" (md:937), Figure 2 (md:1017), Figure 3 (md:1019).

---

## B. Setup — what is declared before any result

### Network configuration(s)
**One configuration, one size, no topology.** "For the experiment, we consider a computer networked system consisting of N nodes set to 200, representing a network of a mid-sized organization. Each node is either a VN or a NVN based on a given vulnerability probability, Pv, implying the number of NVNs is (1−Pv)N while the number of VNs is PvN." (md:807–812). There is **no graph, no topology, no adjacency, no layering, and no attack path** — the network is a *population of 200 nodes* characterised only by the vulnerable fraction. Nodes are typed once, up front: "We assume that a certain percentage of the computers exhibits security vulnerabilities while others do not. We shortly name a vulnerable node as a VN while calling a non-vulnerable node as a NVN. We model these nodes based on the probability that a given node is vulnerable or not vulnerable, denoted by Pv and 1−Pv" (md:437–441). The size 200 also does duty as the run-termination bound (see *Replications*, below).

### Attacker model / scenarios
**One attacker, defined by a five-bullet behaviour list, not by a name or a scenario.** §3.1 opens "In this work, an attacker is assumed to exhibit the following behaviors" (md:443) and gives (md:445–476, condensed with the operative clauses verbatim):
1. Exploit-matching drives Pv: "The attacker has a finite set of exploits and Pv is a function of the match between the attacker's exploits and the software stack on the target nodes."
2. Perfect vulnerability oracle: "An attacker can detect whether a given node in a system of interest has vulnerability or not with **perfect knowledge**. That is, when the attacker accesses a certain node in the system, it knows whether the accessed node is exploitable."
3. Deception detectability as a single parameter: "An attacker is characterized by the probability of detecting the deception deployed in a given node, denoted by Pad."
4. Learning from failure: "An attacker can learn from its past experiences including failure experiences where it was detected by IDS, deceived by a honeypot (i.e., a deception technique), or confused by MTD. The attacker becomes smarter based on this learning (i.e., previous attack failure experiences), leading to expediting the attack success (i.e., shortening the time to reach the system failure)."
5. MTD-induced delay: "An attacker may take more time to investigate system configurations if a defender deploys MTD in a given VN … Extending the reconnaissance period not only drains the attacker's resources, but also allows IDS to earn additional time to detect the attacker before the attack can progress."

Only two of the five are *parameters*; the rest are structural, and the paper says so: "The above attack behaviors are modeled using the probability of detecting deception by an attacker, denoted Pad in the SPN illustrated in Figure 1" (md:476–478). Behaviours 4 and 5 are actually realised inside **transition rate expressions**, which is the paper's distinctive move — the attacker's learning and the MTD penalty are algebra in a rate, not code in an agent:
- Attack success rate: `TATKS = (mark(AF)+1)/(Ts(1+mark(MTD)))` — "The formulation of TATKS implies that the attacker learns based on the past failure experiences (i.e., mark(AF)) but its additional effort is required upon the execution of MTD." (md:700–708). Accumulated failures speed the attacker up linearly; MTD being on halves the rate.
- Detection rate: `TDET = (mark(AF)+mark(MTD)+1)(1−Pfn)/Td` (md:673–677) — the *same* failure counter also speeds up the defender, and an active MTD adds one to the IDS's numerator.

**Failure condition (the whole security model in one assumption):** "we assume that if a single VN is compromised and exploited by an attacker, then the entire system fails … when a single node is compromised and its group key is captured by the attacker (i.e., exploited), the entire system will be compromised. Thus, we use this hard security condition to evaluate the proposed integrated defense system" (md:478–492). There is therefore **no lateral movement and no multi-step attack path** — the attacker's whole campaign is: access a node → it is VN or NVN → reconnaissance → success/failure.

### Defence conditions
Three mechanisms (§3.2, md:493–556), each a bullet with a rationale rather than an algorithm:
- **IDS** — host-based, adaptive: "IDS will be triggered with a certain interval but adaptively in proportion to detected attacks, reflecting IDS's learning towards attacks exhibited in the past. IDS can take advantage of MTD by earning extra time to detect attackers before a successful attack is attained." Errors are modelled one-sided: "we consider the true negative based on 1−Pfn to represent the true negatives in IDS of the SPN model" (md:496–520). Only Pfn (false negatives) is parameterised; false positives are named but not given a parameter.
- **Deception (honeypot)** — "a 'honeypot' technique is used by a defender with the goal of misleading an attacker to believe that an isolated and highly monitored node is a high quality target that is worth attacking"; its ceiling is set by the attacker: "the effectiveness of this deception technique is significantly affected by the attacker's ability to detect the deception … denoted by Pad" (md:521–536).
- **MTD (platform migration)** — "Platform migration, one of the diversity techniques in MTD, is used to conduct MTD. This is costly compared to light-weighted manipulation of environmental settings such as Shuffling (e.g., changing an IP address) … However, since this platform migration introduces a lot more new configurations the attackers need to investigate or figure out, it is more effective than a deception technique which may be detected by the attacker over time" (md:537–548).

**How the mechanisms combine:** by *placement probability in one shared SPN*, not by a scheduler. A honeypot enters via transition `THP` at rate `Ph/Th`, MTD via `TMTD` at rate `Pm/Tm`, and both are cleared for the next node by a single reset transition: "when a new scan by an attacker arrives by enabling the transition TACCESS, a token in place MTD is taken out by the transition TNEXT" (md:660–663, and identically for HP at md:626–630). The *interplay* is explicitly modelled in two places rather than assumed additive: MTD lengthens the attacker's reconnaissance, which raises IDS's detection chance ("If MTD is executed, IDS can have more time to detect attackers based on their suspicious activities during their prolonged reconnaissance period, leading to higher attack detection rates. At the same time, the attack success can be delayed by MTD", md:648–658), and this is realised by `mark(MTD)` appearing in *both* TDET's numerator and TATKS's denominator.

**Cost weighting is a declared modelling decision, stated before results:** "In terms of the cost of a defense technique, MTD is the most expensive defense technique among three techniques … We model IDS and deception as an equal cost while MTD costs twice of IDS or deception, to reflect the high cost paid to deploy MTD." (md:549–556), realised in the CD reward function as `mark(HP) + 2×mark(MTD) + mark(DCVDCGT)` (md:747).

**Conditions are defined by parameter ablation** (§5.1, md:781–805) — four schemes, each specified as which SPN parameter is zeroed:
| Scheme | Definition given |
|---|---|
| IDS only | "the probabilities that MTD or a honeypot is placed on a node accessed by an attacker will be set to zero (i.e., Pm = 0 and Ph = 0), disabling the transitions THP and TMTD" |
| IDS + HP | "We set Pm = 0, disabling the transition TMTD while Ph > 0 in the SPN." |
| IDS + MTD | "We set Ph = 0, disabling the transition THP in the SPN." |
| IDS + MTD + HP | "This is realized with Pm > 0 and Ph > 0 in the SPN." |

**No-defence baseline: NO.** The floor condition is "IDS only", not "no defence" — IDS is present in all four schemes and is never ablated. The paper's own framing makes this deliberate: "For the purpose of this work, any defense system with more than one security mechanism is considered as an integrated defense system" (md:139–141), so the design is *degree of integration* (1, 2, 2, 3 mechanisms) rather than *presence vs absence of defence*.

### Metric definitions
Four metrics + two derived unit costs, all as SPN reward functions (§4.2, md:709–773). The framing: "We use four performance metrics in which two metrics measure the attack performance while the other two metrics estimate the defense performance" — i.e. **the metric set is symmetric by construction, two per side.**

- **MTTSF (mean time to security failure)** — "refers to the system life time indicating how long the system will prolong until the security failure occurs (i.e., when mark(AS) = 1, the security failure occurs)": `MTTSF = Σ_{i∈S} r_i ∫_{t=0}^{∞} P_i(t) dt` (Eq. 1, md:723–731), "where r_i (reward) is 1 for the absorbing states having mark(AS) = 0 and 0 for mark(AS) = 1". Claimed as novel in the contribution list: "MTTSF is a new metric derived from the traditional reliability metric but considers the security failure as the system failure condition in terms of an attacker's success" (md:130–134).
- **CD (accumulated defense cost)** — "measures how much defense cost is given to achieve MTTSF under a given defense system": `CD = Σ_{i∈S} D_i ∫ P_i(t) dt` (Eq. 2, md:732–748), with `D_i = mark(HP) + 2×mark(MTD) + mark(DCVDCGT)`.
- **PAS (attack success probability)** — "Assuming that the system will fail when any one of VNs is compromised by an attacker": `PAS = Σ_{i∈S} SF_i ∫ P_i(t) dt / MTTSF` (Eq. 3, md:711–719), "where SF_i (reward) is set to 1 for mark(AS) = 1 or 0 for mark(AS) = 0". **Note it is normalised by MTTSF** — PAS is a rate-like quantity, not a plain probability.
- **CA (accumulated attack cost)** — "measures the accumulated time an attacker invested until it succeeds its attack by having mark(AS) = 1": `CA = Σ_{i∈S} C_i ∫ P_i(t) dt` (Eq. 4, md:749–761), with `C_i = mark(RECON) + mark(DCVDCGT)`. **Attack cost is literally time-in-state** — time spent doing reconnaissance plus time spent inside a honeypot.
- **Two derived unit costs, with the direction of goodness stated:** "we will also demonstrate attack or defense cost per performance, the so-called attack unit cost or defense unit cost. They represent how much cost is paid to achieve given performance. That is, attack cost per attack success probability, CA/PAS, and defense cost per MTTSF, CD/MTTSF, are considered to show a unit cost for attack or defense performance, respectively. Note that **a lower unit cost is more desirable in terms of the perspective of each party**, an attacker, or a defender." (md:762–773)

### Parameter table
**YES — Table 2, "Key design parameters, their meanings, and their default values" (md:862–905), three columns (Param. | Meaning | Value), 14 rows.** Reassembled from the split-column text:

| Param. | Meaning | Value |
|---|---|---|
| N | The number of nodes (i.e., components of a system) | 200 |
| Pv | The probability that a given node is vulnerable | **[0.3, 0.7]** |
| Ph | The probability that a given vulnerable node (VN) has a honeypot | 0.5 |
| Pm | The probability MTD is in execution | 0.5 |
| Pad | The probability that the attacker detects deception by a defender | 0.5 |
| Pfn | The probability that IDS falsely detect an attacker's malign behavior as benign | 0.05 |
| Th | The inter-arrival time that a honeypot is placed in a given node | 5 hrs. |
| Tm | The inter-arrival time that MTD is triggered | 5 hrs. |
| Tr | The inter-arrival time that an attacker performs 'reconnaissance' | 1 hr. |
| Ta | The inter-arrival time that an attacker accesses a given node | 5 hrs. |
| Ts | The inter-arrival time that an attacker attains its success | 3 hrs. |
| Tc | The inter-arrival time that an attacker is deceived by a defender's deception | 1 hr. |
| Tf | The inter-arrival time that an attacker fails its attack goal | 3 hrs. |
| Td | The inter-arrival time that IDS is triggered | 3 hrs. |

Note the **column-embedded sweep**: every parameter has a scalar default except Pv, whose "value" is the interval [0.3, 0.7] — the swept axis is declared inside the default-values table rather than in a separate sensitivity section.

**A second table carries the model itself: Table 3, "Transition names, meanings, rates, and enabling conditions" (md:937–1015)** — 4 columns (Transition name | Meaning | Transition rate | Enabling conditions), 8 rows. Reassembled:

| Transition | Meaning | Rate | Enabling condition |
|---|---|---|---|
| TACCESS | attacker accesses a given node | `(1−Pv)/Ta` for place NVN; `Pv/Ta` for place VN | `mark(NVN)+mark(VN)==0 ∧ mark(AS)+mark(AF)<200` |
| TRECON | attacker reconnaissances a given node | `Pad/Tr` | `mark(RECON)==0 ∧ mark(AS)+mark(AF)<200` |
| TDCVD | attacker is deceived | `(1−Pad)/Tc` | `mark(DCVDCGT)==0 ∧ mark(AS)+mark(AF)<200` |
| TATKS | attacker succeeds | `(mark(AF)+1)/(Ts(1+mark(MTD)))` | `mark(AS)+mark(AF)<200` |
| TATKF | attacker fails | `1/Tf` | `mark(AS)+mark(AF)<200` |
| TDET | IDS detects an attack | `(mark(AF)+mark(MTD)+1)(1−Pfn)/Td` | `mark(DCVDCGT)==0 ∧ mark(AS)+mark(AF)<200` |
| TMTD | MTD is triggered in a given node | `Pm/Tm` | `mark(MTD)==0 ∧ mark(AS)+mark(AF)<200` |
| THP | honeypot is placed in a given node | `Ph/Th` | `mark(HP)==0 ∧ mark(AS)+mark(AF)<200` |
| TNEXT | MTD or honeypot is reset for a next node | `1/Ta` | `mark(MTD)+mark(HP)>0 ∧ mark(AS)+mark(AF)<200` |

This table is the paper's **reproducibility artefact**: with Table 2 and Table 3 together, the model is fully specified, and the enabling conditions double as the termination rule.

**Distributions declared?** Only structurally: the SPN is exponential/semi-Markov by construction — "we use a SPN model in which the underlying mode is Markov or semi-Markov" (md:560–562) — so every "inter-arrival time" T is the mean of an exponential clock. No distribution is named per parameter, and no distribution is fitted to data.

### Replications
**Not stated as such — and by design there are none to state.** The evaluation is an *analytic* solve of the underlying Markov chain, not a Monte-Carlo simulation: every metric is a stationary integral `∫_{t=0}^{∞} P_i(t) dt` over state probabilities (Eqs. 1–4, md:723–761), computed by a solver — "We use SPN Package version 6 which is developed by Duke University and available in Trivedi" (md:562–564; SPNP, ref. 31 at md:1236). Consequently: no run count, no seeds, no error bars, no confidence intervals, no significance tests anywhere. **Termination is declared, but only inside Table 3's enabling conditions**: every transition carries `mark(AS)+mark(AF) < 200`, i.e. the model stops once 200 attack outcomes (successes + failures) have accumulated — the same 200 as the node count, though the paper never remarks on the coincidence. The time horizon is `∞` in the reward integrals.

### Statistics
None reported. Results are single deterministic curves per scheme per Pv value. No dispersion measure appears anywhere in the paper.

### Anything else declared
Tool and version: SPNP v6 from Duke (md:562–564). **No hardware, no runtime, no code link, no solver settings, no state-space size.** Funding/acknowledgement of ARL sponsorship at md:1121–1130.

---

## C. Results — how the numbers are shown

### Order of results
**Perspective-major: attacker side first, defender side second**, each as one three-panel figure, each panel read in order (raw performance → cost → cost-per-unit-performance). "Attack performance: In Figure 2, we show the attack performance under the four defense systems in terms of attack success probability (Figure 2(a)), attack cost (Figure 2(b)), and attack unit cost (Figure 2(c))." (md:841–845); "Defense performance: In Figure 3, we show the performance of the four defense systems when system vulnerability varies in terms of the system lifetime based on the security failure, MTTSF (Figure 3(a)), defense cost (Figure 3(b)), and defense unit cost (Figure 3(c))." (md:916–923). The attacker-first ordering matters: the defender panels are then read *against* the attacker panels ("This is a reverse order of Figure 2(a)", md:914).

### Every figure in the evaluation portion
- **Figure 1** (md:483–486) — "Stochastic Petri Nets modeling the system integrated with intrusion detection system (IDS), moving target defense (MTD), and honeypots." The model diagram; places (VN, NVN, RECON, DCVDCGT, HP, MTD, AS, AF) and transitions. Setup, not results. Walked through transition-by-transition in §4.1 (md:583–708).
- **Figure 2** (caption at md:1017–1018) — "Attack performance comparison under the four defense schemes with respect to varying system vulnerability: (a) attack success probability (PAS); (b) accumulated attack cost (CA); (c) attack cost per attack success (CA/PAS)." Three panels; x = system vulnerability Pv over [0.3, 0.7] (from Table 2); y = the named metric; four series = the four schemes. Chart type not recoverable without the PDF; the prose ("higher increase … between Pv = 0.3 and Pv = 0.4", md:855) implies line/curve plots over a continuous Pv.
- **Figure 3** (caption at md:1019–1021) — "Defense performance comparison under the four defense schemes with respect to varying system vulnerability: (a) MTTSF; (b) accumulated defense cost (CD); (c) defense cost per MTTSF (CD/MTTSF)." Same layout, same x-axis, same four series.

**Every result in the paper is one figure family × one swept parameter.** There is no table of results and no per-scheme numeric summary.

### Every table
- Table 1 "Categorization of deception techniques" (md:278) — sits in §2 related work; a literature taxonomy, not a result.
- Table 2 (md:862) and Table 3 (md:937) — parameters and model, §B above.
- **No results table exists.**

### How the baseline appears
"IDS only" is the fourth series in all six panels, and it is used as the *worst* reference point in prose ("introducing HP provides quite high performance compared to IDS Only but incurs much less cost than MTD", md:1021–1023; "introducing a deception technique (i.e., a honeypot) costs significantly more than using IDS only while it significantly increases MTTSF (i.e., more than 25%) in IDS+HP than in IDS only", md:1038–1043). It is never labelled a control group, and there is no zero-defence condition to anchor against.

### How comparisons are stated in prose
Predominantly **full four-way orderings written as a chain of inequalities** — a distinctive habit, and the paper writes them in both directions to make the perspective explicit:
- Attacker side: "we can observe that the attacker's performance is in the order of IDS+MTD+HP < IDS+MTD < IDS+HP < IDS only" (md:895–898).
- Defender side: "The performance of the four schemes is ordered as follows: IDS+MTD+HP > IDS+MTD > IDS+HP > IDS only. **This is a reverse order of Figure 2(a) and is true for a defender's perspective.**" (md:912–915).
Magnitudes appear only as **percentage lower bounds on MTTSF gains**, and only twice: "it significantly increases MTTSF (i.e., more than 25%) in IDS+HP than in IDS only. However, integrating a deception technique on top of IDS+MTD (i.e., IDS+MTD+HP) adds a little more cost compared to the cost in IDS+MTD and accordingly **increases MTTSF at least more than 5%**." (md:1040–1047). No absolute values are quoted anywhere for any metric.
Recommendation form is deferred rather than issued: "In terms of a defender's perspective, it is critical to identify an optimal setting, including optimal use of deception and MTD techniques that minimizes defense cost but maximizes MTTSF. **We leave this sensitivity analysis to the future work.**" (md:1057–1062).

---

## D. Narrative — the claims, in order

1. Monotone effect of the swept parameter, with a named knee: "Overall, all schemes allow higher attack success as Pv becomes higher. Noticeably, a higher increase of attack success is observed between Pv = 0.3 and Pv = 0.4 than when Pv > 0.4." (md:853–857), explained mechanically ("When there are more VNs compared to NVNs, it is more likely for the attacker to perform a successful attack", md:857–860).
2. Full ordering on attack success, with the integrated scheme best: "the integrated defense mechanism (i.e., IDS + MTD + HP) shows the minimum attack success probability, showing the highest security among the four schemes" (md:898–901).
3. **A deliberately-flagged non-alignment between two metrics:** "Although the performance is quite similar to Figure 2(a), we notice that **the highest attack success does not necessarily require the highest attack cost**. For example, the cost of IDS+MTD is the highest while the cost of IDS+MTD+HP is the second highest. This is because IDS+MTD+HP balances defense workload among three techniques where MTD costs higher than IDS or HP." (md:940–954).
4. Unit cost confirms the ordering and adds a *sensitivity* observation: "Due to the lowest attack success under IDS+MTD+HP, the attack unit cost is highest under IDS+MTD+HP among all, implying that the attacker is required to make the highest effort. The second highest attack unit cost is incurred when the defender is using MTD … It is also interesting to see that **the attacker's cost per success is less sensitive to the system vulnerability when the defender is using IDS only and IDS+HP** compared to IDS+MTD and IDS+MTD+HP." (md:924–936).
5. MTTSF mirrors attack success, including the knee: "As attack success probability has a high increase between Pv = 0.3 and Pv = 0.4, we can notice its impact on MTTSF, showing its high decrease in the same setting. In addition, we observe the expected trend that MTTSF decreases as Pv increases." (md:909–912).
6. Cost ordering is the expected one: "As expected, the highest cost is incurred under IDS+MTD+HP among all. In addition, we can notify that MTD is costly compared to HP … However, MTD achieves a much higher level of security than HP, showing lower attack success in MTD than HP" (md:1024–1032).
7. **The paper's headline finding, stated as non-linearity of marginal returns:** "introducing a deception technique (i.e., a honeypot) costs significantly more than using IDS only while it significantly increases MTTSF (i.e., more than 25%) in IDS+HP than in IDS only. However, integrating a deception technique on top of IDS+MTD (i.e., IDS+MTD+HP) adds a little more cost compared to the cost in IDS+MTD and accordingly increases MTTSF at least more than 5%. This reveals that **the integrated defense system can add different defense techniques to enhance security without introducing a significant cost**, leading to more effectively dealing with sophisticated attacks." (md:1038–1052). Restated in the conclusion as: "we observe that the contribution of adding an additional defense technique to security and performance is **not linear**. This implies that a defense system can maximize its performance and security while reducing the defense cost depending on how to integrate defense techniques." (md:1100–1105).
8. **A face-validity argument made from a cross-metric comparison** — the one claim in the paper that appeals to the outside world rather than the model: "Interestingly as observed in Figure 2(b) and Figure 3(b), our SPN model captures the higher defense cost than the attack cost. The clear gap in the cost associated with launching malicious activities by an attacker and defending against the attacker **looks realistic based on the overall trends of most cyber attack–defense situations**. That is, the technical knowledge and amount of resources required to initiate a cyber attack decrease continuously while the defender's costs to deal with the attacks increase steadily by deploying additional defense based on multiple defense techniques." (md:1063–1073).

### Does the paper make claims about the ATTACKER's properties from the data?
**Yes — half the reported results are attacker-side, and the paper says so structurally.** Two of the four metrics (PAS, CA) and one of the two unit costs (CA/PAS) are the attacker's; Figure 2 is entirely the attacker's; and the framing is explicit: "While taking the perspectives of both the attacker and defender, we analyze the effectiveness and efficiency of the techniques" (md:116–119), and "the developed SPN model allowed us to evaluate the performance of different combinations of defense techniques from the perspectives of both a defender and an attacker" (md:1078–1082). Specific attacker claims read off the data: "the attacker is required to make the highest effort" (md:929); "the attacker's cost per success is less sensitive to the system vulnerability when the defender is using IDS only and IDS+HP" (md:933–936); "attack performance (e.g., attack success and attack cost) is significantly affected by the defense techniques used by a system" (md:1094–1097).
But these are still *defender-side model outputs*: the attacker has no strategy, no target selection, and no lateral movement — its "cost" is `mark(RECON)+mark(DCVDCGT)` (time in two places), and its "learning" is the linear factor `(mark(AF)+1)` in one rate expression. The paper concedes the reward functions are the weak point: future work item (1) is to "enhance reward functions used to measure performance metrics considering cost details of attack and defense actions such as communication or computational overhead" (md:1108–1112).

---

## E. Sensitivity / parameter analysis

**This is the most instructive thing about the paper for the present purpose: there is no sensitivity section, one parameter is swept, and the paper explicitly names what it did *not* sweep and defers it.**

- **What is varied:** exactly one parameter — system vulnerability **Pv over [0.3, 0.7]** (Table 2, md:868/885), and it is the x-axis of all six result panels. Every figure caption says "with respect to varying system vulnerability" (md:1017, md:1019).
- **One-at-a-time or grid:** neither, strictly — it is a *single* swept axis crossed with the four defence schemes, i.e. a 4 × (Pv grid) design. No second parameter is ever varied while another is held.
- **Range justification:** **not stated.** Neither the floor 0.3 nor the ceiling 0.7 is argued for anywhere; N = 200 gets a one-clause justification ("representing a network of a mid-sized organization", md:809) but Pv's interval gets none.
- **What is explicitly held fixed, and named as such:** "We fix the Pad = 0.5 as an attacker's ability to detect a deception. We also set the probabilities that a honeypot or MTD is placed, respectively." (md:812–815), and again at the end of §5.3: "In this experiment, we fixed Pad = 0.5 (an attacker's ability to detect a deception), Ph = 0.5 (the probability of using a honeypot), and Pm = 0.5 (the probability of using MTD)." (md:1053–1057). The three most decision-relevant knobs — how much deception, how much MTD, and how good the attacker is at seeing through deception — are all pinned at 0.5 and never moved.
- **Where the sensitivity claim is made instead:** in a *prose assertion of insensitivity*, offered in §5.2 in place of an experiment, and this is the paper's single most distinctive move —
  > "The design parameter values used in this experiment reflect a particular system condition where attackers exhibit a series of behaviors following the given set of event triggering time, which is modeled by the transition rates. A different set of design parameter values can reflect a different system condition and performance requirement to maintain. **When varying the event transition times and probabilities to adjust the behaviors of attackers and defenders, we observe that the overall behavior across times remain the same while the evolution of system behavior changes to some extent with respect to time. Therefore, the presented results provide sufficient insights for the overall behaviors of the proposed defense system** and its impact on defense performance against attack behaviors." (md:817–834)

  No figure, table, range, or number accompanies this — the robustness of every result rests on an unreported exploration.
- **What the deferral says, verbatim:** "In terms of a defender's perspective, it is critical to identify an optimal setting, including optimal use of deception and MTD techniques that minimizes defense cost but maximizes MTTSF. **We leave this sensitivity analysis to the future work.**" (md:1057–1062), repeated as future-work item (3): "validate the proposed model based on various scenarios through **comprehensive sensitivity analysis**" (md:1112–1115).
- **What the one sweep is used to support:** (a) that the scheme ordering is *stable across the whole Pv range* (the orderings at md:895 and md:912 are asserted without qualification, implying no crossings); (b) that there is a **knee at Pv ≈ 0.3–0.4** where the marginal effect of vulnerability is largest (md:853–857, md:909–912); and (c) that the *slope* itself discriminates the schemes — "the attacker's cost per success is less sensitive to the system vulnerability when the defender is using IDS only and IDS+HP compared to IDS+MTD and IDS+MTD+HP" (md:933–936), which is a sensitivity claim read straight off the sweep rather than off any point value.

---

## F. Discussion / limitations

**Folded into results — there is no discussion section and no limitations section.** §5.3 does the interpretive work inline (the mechanism explanations at md:947–954 and md:1044–1052, the face-validity argument at md:1063–1073), and §6 "Conclusion and future work" (md:1074) restates findings and then lists three future-work items. There are **no threats to validity, no attacker-realism concession, and no comparability caveat**; no comparison to any other paper's numbers is attempted anywhere.

The nearest things to limitation statements, verbatim:
- The unreported-robustness clause quoted in §E: "When varying the event transition times and probabilities to adjust the behaviors of attackers and defenders, we observe that the overall behavior across times remain the same while the evolution of system behavior changes to some extent with respect to time. Therefore, the presented results provide sufficient insights for the overall behaviors of the proposed defense system" (md:823–832).
- The deferral: "We leave this sensitivity analysis to the future work." (md:1061–1062).
- The three future-work items, which are limitations in disguise: "(1) enhance reward functions used to measure performance metrics considering cost details of attack and defense actions such as communication or computational overhead; (2) identify an optimal setting in terms of an optimal deception or MTD placement that meets both minimum defense cost (or maximum attack cost) and maximum MTTSF (or minimum attack success); and (3) validate the proposed model based on various scenarios through comprehensive sensitivity analysis." (md:1106–1115). Note (3) uses the word **"validate"** — the model is nowhere validated against data, real traces, or another model, and the paper does not say so in its own voice.
- A *generic* limitation list does appear, but it is about MTD in the literature (§3 opening, md:406–430: "There is a need to choose the appropriate MTD technique to mitigate a specific attack type … Some MTD techniques are better at disrupting the attacker compared to others, depending on the attacker's goal which is often unknown … The use of MTD incurs cost associated with system performance affecting service availability or computational performance and/or network connectivity"), not about this study. It is used to motivate the design, not to qualify the results.

The conclusion's strongest claims: "the integrated defense system with the three defense techniques, including IDS, MTD, and deception, performs the best in terms of prolonging the system lifetime (i.e., MTTSF) while minimizing the attack success" and "we conclude that the integrated defense system can maximize the system performance and security based on the interplay of defense mechanisms and cost-effective defense techniques" (md:1088–1100) — stated without qualification by Pv range, by parameter setting, or by the pinned Ph = Pm = Pad = 0.5.

---

## G. Transferable vs purpose-specific

### Transfers to an honours dissertation evaluating existing MTD mechanisms against a new attacker model on a simulator

- **The symmetric metric set, declared as symmetric:** "four performance metrics in which two metrics measure the attack performance while the other two metrics estimate the defense performance" (md:709–712). Two attacker metrics and two defender metrics, then a derived unit-cost for each side, with the direction of goodness spelled out ("a lower unit cost is more desirable in terms of the perspective of each party", md:771–773). This is the cleanest attacker/defender metric symmetry in the four papers surveyed.
- **Defining each condition by which parameter is zeroed** (§5.1, md:781–805) rather than by prose description — the ablation is unambiguous and re-runnable, and it makes the "degree of integration" factor visible as a design.
- **A parameter table whose Value column carries the sweep** (Pv = [0.3, 0.7] alongside 13 scalars, md:862–905): one table declares both the fixed configuration and the varied axis.
- **A second table that specifies the model itself** — Table 3's Transition | Meaning | Rate | Enabling condition (md:937–1015). The analogue for a simulator dissertation is a table of the mechanisms with their trigger rule and precondition, and it is what makes this paper reproducible without code.
- **Putting the attacker's adaptivity in an explicit formula and then explaining it in one sentence:** `TATKS = (mark(AF)+1)/(Ts(1+mark(MTD)))`, glossed as "the attacker learns based on the past failure experiences (i.e., mark(AF)) but its additional effort is required upon the execution of MTD" (md:700–708). The pattern — write the coupling, then say in words what it means for the attacker — is directly reusable.
- **Modelling the interplay rather than assuming additivity:** `mark(MTD)` appears in *both* the detection rate and the success rate (md:648–677), so "MTD helps IDS" is in the model, not just in the discussion. A dissertation combining MTD mechanisms should say where the cross-terms are.
- **Reporting a cross-metric non-alignment as a finding** ("the highest attack success does not necessarily require the highest attack cost", md:942–944) instead of smoothing it away.
- **The marginal-return framing** — reporting the *increment* from adding a third mechanism separately from the increment of adding a second (md:1038–1052), which is what converts a "more is better" result into a decision-relevant one.
- **Naming the fixed parameters twice** — once in setup (md:812–815) and again at the point where the results depend on them (md:1053–1057) — so the reader meets the caveat where it bites.

### Purpose-specific artefacts (JDMS special-issue article; analytic SPN, defence-portfolio question)

- **The "we observed robustness but do not show it" sentence** (md:823–832). It substitutes for a sensitivity analysis and would not survive examination in a dissertation; the correct move is to run the sweep and put it in an appendix.
- **No sensitivity analysis, and it is explicitly deferred twice** (md:1061, md:1112) while the three most consequential parameters are pinned at 0.5. Fine for a first model paper; disqualifying where the parameter values are themselves the contested object.
- **No no-defence baseline** — IDS is in every arm. Coherent for the "defense in breadth" question (the paper is about *integration*, not about *whether defence helps*), but it means no result in the paper is anchored to an undefended system.
- **Network as a scalar population, not a graph**: 200 nodes with a vulnerable fraction, one-node-compromise-fails-everything (md:478–492). This collapses lateral movement out of existence and is the direct opposite of what a movement-attacker dissertation needs.
- **Everything read off one swept axis** (Pv) crossed with four schemes: six panels, no tables, no absolute numbers. Compact for a 14-page article; too thin as an evaluation chapter.
- **Analytic Markov solve rather than simulation** (SPNP, md:562–564), which is why replications, seeds and CIs are absent. Borrowing the *presentation* without the analytic solve would leave a stochastic study with no error reporting.
- **No hardware, runtime, state-space size, or code link** — and no validation of the model against anything external, with "validate" appearing only as future work (md:1112–1115).
- **The face-validity paragraph** (md:1063–1073) argues a result "looks realistic based on the overall trends of most cyber attack–defense situations" with no citation. The instinct (check the model against the world) transfers; the execution (an uncited appeal to general knowledge) does not.
