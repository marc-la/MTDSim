# manadhatawing2011tse — evaluation-section anatomy (template applied loosely; §H is the substance)

Source read: `docs/sources/lit_review/manadhatawing2011tse.md` (1,059 lines; Ghostscript two-column extraction, header note at L1 flags imperfect spacing and says the PDF is authoritative) **and** `docs/sources/lit_review/manadhatawing2011tse.pdf` in full — 16 pages, journal pages 371–386, IEEE TSE 37(3), May/June 2011. The .md extraction **silently drops the body of every table**; Tables 1, 4, 5, 6, 7, 8 and 11 were recovered by rendering the PDF pages at 200–220 dpi and are transcribed below. Locators are `md L<n>` with the journal page in parentheses. Journal page N = PDF page N−370.

Paper's own research question / purpose (one sentence): "we propose using a software system's attack surface measurement as an indicator of the system's security. We formalize the notion of a system's attack surface and introduce an attack surface metric to measure the attack surface in a systematic manner" (abstract, md L8–10, p.371).

Why it is worth reading here: it is a **security-metric introduction paper** — the thing this dissertation is doing when it defines its own measure. It is also the source of two ideas the MTD literature reuses constantly (attack surface; damage-potential-effort ratio), and it contains an explicit critique of Time-To-Compromise-style metrics (§G).

## A. Skeleton

Sixteen pages; the paper spends **9 pages defining** and **6 pages measuring and validating**. Setup, results and validation are three separate sections, and validation gets its own top-level section — which is the structural point to steal.

- **1 INTRODUCTION** (md L19, p.371) — 1.1 Motivation (md L40, p.371); 1.2 Attack Surface Metric (md L52, p.371) [the informal definition, before any formalism]
- **2 BACKGROUND** (md L70, p.372) — Howard's Relative Attack Surface Quotient; the two shortcomings that motivate the work
- **3 FORMAL MODEL FOR A SYSTEM'S ATTACK SURFACE** (md L145, p.373) — 3.1 I/O Automata Model (md L154) with 3.1.1 Model, 3.1.2 Entry Points, 3.1.3 Exit Points, 3.1.4 Channels, 3.1.5 Untrusted Data Items, 3.1.6 Attack Surface Definition (md L329, p.375); 3.2 Damage Potential and Effort (md L343, p.376) with 3.2.1, 3.2.2; 3.3 A Quantitative Metric (md L453, p.377) with 3.3.1 Damage Potential-Effort Ratio, 3.3.2 Quantitative Attack Surface Measurement Method. **Definitions 1–12 and Theorems 1–2 all live here.**
- **4 EMPIRICAL ATTACK SURFACE MEASUREMENTS** (md L508, p.378) — 4.1 Identification of Entry Points and Exit Points, Channels, and Untrusted Data Items; 4.2 Estimation of Damage Potential-Effort Ratio; 4.3 Attack Surface Measurements and Their Usage [the worked C measurement: two IMAP daemons]
- **5 EMPIRICAL STUDIES FOR VALIDATION** (md L585, p.379) — 5.1 Statistical Analysis of Microsoft Security Bulletins (5.1.1 MSBs, 5.1.2 Hypothesis 1, 5.1.3 Hypothesis 2, 5.1.4 Hypothesis 3); 5.2 Expert User Survey (5.2.1 Subjects and Questionnaire, 5.2.2 Results); 5.3 Open Source Patch Analysis (5.3.1 Identification of Relevant Patches, 5.3.2 Results and Discussion); 5.4 Anecdotal Evidence
- **6 MEASUREMENT METHOD FOR SAP SOFTWARE SYSTEMS** (md L778, p.382) — 6.1 Implementation of a Measurement Tool; 6.2 Estimation of the Damage Potential-Effort Ratio; 6.3 Results and Discussion; 6.4 Lessons Learned [the scale-up case study, Java]
- **7 RELATED WORK** (md L855, p.384)
- **8 CONCLUSION AND FUTURE WORK** (md L944, p.385)

## B. Setup — what is declared before any measurement

- **Systems measured**: two open-source IMAP daemons, **Courier-IMAP 4.0.1** and **Cyrus 2.2.10** (md L528–529, p.378), chosen "due to their popularity" and measured in both codebases "to obtain a fair comparison" (md L532–534, p.378). Two FTP daemons (ProFTPD 1.2.10, Wu-FTPD 2.6.2) were also measured but "we omit the results due to space limitations [10]" (md L529–531, p.378). Plus, in §6, three versions (S1, S2, S3) of "a core building block of NetWeaver … used by most SAP customers" (md L823–825, p.383).
- **Scope restriction, declared up front**: "The empirical application of our method focuses only on direct entry and exit points since, unlike for indirect ones, we can automatically identify direct ones using source code analysis tools. Developing automated tools to identify indirect entry and exit points whose use would then afford a more complete attack surface measurement is left for future work." (md L520–526, p.378).
- **Method, as a figure**: Fig. 8 "Steps of our attack surface measurement method for C" (md L494, p.378), with an explicit legend for what is automated and what is not — "The dotted box shows the step done manually and the solid boxes show the steps done programmatically. The two dotted arrows represent manual inputs required for measuring the attack surface. We automated as many steps as possible in our measurement method and minimized the number of manual inputs required by the method." (md L512–519, p.378).
- **Instrumentation**: call graphs from `cflow` for C (md L516–517, p.378); for Java, two interchangeable call-graph generators offering "a precision-scalability tradeoff" — the TACLE Eclipse plugin (precise, does not scale) and an Eclipse API (less precise, scales) (md L828–838, p.383); the tool itself shipped as an Eclipse plugin (Fig. 9, md L797, p.383).
- **Counting rule, declared**: "If a method ran with multiple privileges or was accessible with multiple access rights levels during different executions, then we counted the method multiple times." (md L517–519, p.378).
- **Parameter table**: YES — **TABLE 4, "Numeric Values Assigned to the Attributes"** (p.379), a 3-block table pairing each damage-potential attribute with its effort counterpart:

| Method Privilege | Value | Access Rights | Value |
|---|---|---|---|
| root | 5 | admin | 4 |
| cyrus | 4 | authenticated | 3 |
| authenticated | 3 | anonymous | 1 |
| | | unauthenticated | 1 |

| Channel Type | Value | Access Rights | Value |
|---|---|---|---|
| TCP | 1 | local auth | 4 |
| SSL | 1 | remote unauth | 1 |
| UNIX socket | 1 | | |

| Data Item Type | Value | Access Rights | Value |
|---|---|---|---|
| file | 1 | root | 5 |
| | | cyrus | 4 |
| | | authenticated | 3 |
| | | world | 1 |

- **The parameter values are conceded to be subjective, and a sensitivity analysis is offered in mitigation** — see §E. Also declared: "We also assumed that each channel has the same damage potential" (md L585–586, p.379), and two system-specific orderings justified in prose (cyrus > authenticated because "a method running with cyrus privilege in the Cyrus daemon has access to every user's email files"; admin and cyrus cost more effort than authenticated, md L577–585, p.379).
- **Counts declared before the numbers** — **TABLE 1, "IMAP Daemons' Entry Points and Exit Points"** (p.378), DEP = direct entry points, DExP = direct exit points:

| Privilege | Access Rights | DEP | DExP |
|---|---|---|---|
| *Courier* | | | |
| root | unauthenticated | 28 | 17 |
| root | authenticated | 21 | 10 |
| authenticated | authenticated | 113 | 28 |
| *Cyrus* | | | |
| cyrus | unauthenticated | 16 | 17 |
| cyrus | authenticated | 12 | 21 |
| cyrus | admin | 13 | 22 |
| cyrus | anonymous | 12 | 21 |

- **Replications / statistics**: not applicable to the measurement itself (a static analysis is deterministic given the same code and the same numeric assignment). Statistics appear only in §5, where they are stated precisely: ordered logistic regression with z-tests, p < 0.05, on 202 observations (§H.4); t-tests on Likert responses, p < 0.05, n = 20; binomial results at "confidence level = 95%, p < 0.05" for the patch analysis.

## C. Results — how the numbers are shown

- **Order**: definitions → worked measurement on a real pair of systems → validation → scale-up case study. Results are shown *twice*: once as a demonstration that the method runs (§4), and once as evidence that the metric means something (§5).
- **The headline result is a pair of triples, not a scalar**: "Courier's attack surface measurement is ⟨417.67, 2.25, 72.13⟩ and Cyrus's attack surface measurement is ⟨343.00, 3.25, 66.50⟩" (md L555–560, p.379), with the arithmetic shown in-line for one cell: "from Table 1 and Table 4, Courier's methods contribute (45 × (5/1) + 31 × (5/3) + 141 × (3/3)) = 417.67" (md L555–558, p.379).
- **The comparison is stated per dimension, and deliberately not aggregated**: "The attack surface metric tells us that the Cyrus daemon presents less security risk along the methods and data dimensions, whereas the Courier daemon presents less security risk along the channels dimension. Keeping the measurement separated along three different dimensions offers a design choice to our users, e.g., system administrators can choose a dimension appropriate for their need." (md L560–568, p.379).
- **Recommendation form is conditional on the reader's threat concern**, stated three times in a row: "if we were concerned about privilege elevation on the host running the IMAP daemon, then the methods dimension presents more risk and the attack surface metric suggests that we would choose the Cyrus daemon over the Courier daemon. Similarly, if we were concerned about the number of open channels … we would choose the Courier daemon. If we were concerned about the safety of email files, then the data dimension presents more risk and we would choose the Cyrus daemon." (md L568–584, p.379). **Note the convention: the metric does not choose; it makes the choice legible once the reader declares what they care about.**
- **SAP results** — **TABLE 11, "Attack Surface Measurements"** (p.384): S3 = 5298.44, S2 = 4687.00, S1 = 4649.00, with Table 10 giving the entry/exit point counts. Read as an ordering test, not a level: "The relative ordering among the service's three measurements conforms to the expected ordering" (md L829–831, p.383), then explained by the release history (S2 backward-compatible with S1 plus new features; S3 converted a public interface to internal *and* added features) — "If no new features had been added, S3's measurement would have been less than S2; the increase in S3's measurement is due to new features." (md L852–857, p.383–384).

## D. Narrative — the claims, in order

1. Security measurement is an open problem and industry needs it (md L20–33, p.371).
2. Code-quality effort and attack-surface reduction are complementary risk-mitigation strategies (Fig. 1; md L42–48, p.371).
3. Attackers use methods, channels and data items; so define the attack surface over those three resource kinds (md L66–76, p.372).
4. Not all resources are in the surface (→ entry/exit point framework) and not all contribute equally (→ damage potential-effort ratio) (md L77–87, p.372).
5. Howard's RASQ had the right idea but was informal and needed a security expert; ours is formal and does not (md L119–141, p.372–373).
6. Formal payoff: **more surface ⟹ more potential attacks** (Theorems 1 and 2).
7. The method runs on real C code and separates two real IMAP servers per dimension (§4.3).
8. The metric survives three empirical validation studies and one theoretical one (§5).
9. It scales to enterprise Java and is usable inside a developer's IDE (§6).
10. It differs from prior work in being vulnerability-independent, system-centric (not attacker-centric), and actually applied (§7).

**Claims about the attacker from the data**: **none, by design** — and this is stated as a positive property, not a limitation. See §G.

## E. Sensitivity / parameter analysis

**Present, and it is the paper's answer to the "your numbers are arbitrary" objection.** It sits inside §4.2, not in its own section, and its detail is deferred to the thesis [10]:

> "The exact choice of the numeric values is subjective and depends on a system and its environment. Hence we cannot automate the process of numeric value assignment. We, however, provide guidelines to our users for numeric value assignment using parameter sensitivity analysis. In our parameter sensitivity analysis, we studied the effects of changing the difference in the numeric values assigned to the attributes on our measurements. Numeric values should be chosen such that both the privilege values and the access rights values affect the attack surface measurements comparison's outcome. Our analysis shows that if both systems have comparable numbers of entry points and exit points, then the access rights values do not affect the measurements if the privilege difference is low or high. Similarly, if one system has a significantly larger number of entry points and exit points than the other, then no choice of the privilege difference or the access rights difference affects the measurement. Please see Section 4.5 of [10] for further details on the parameter sensitivity analysis." (md L553–574, p.379)

Two things to note about the convention. First, the sensitivity analysis is framed as producing **guidelines for choosing parameters**, not merely as a robustness check — it tells the user which region of the parameter space makes the comparison informative. Second, it is **used later as a design input**: the SAP numeric assignments are made "based on our parameter sensitivity analysis' recommendation: `public = 1` and `internal = 18`" (md L810–812, p.383) and "in proportion to the average severity ratings and based on the recommendation of our prior parameter sensitivity analysis (Table 9)" (md L800–803, p.383). A sensitivity analysis that feeds forward into later parameter choices is a stronger use than one that only defends a single result.

## F. Discussion / limitations

No "Limitations" or "Threats to Validity" heading. Concessions are distributed and each is paired with what would fix it. The strongest, verbatim:

- **Scope of the empirical method**: "The empirical application of our method focuses only on direct entry and exit points since, unlike for indirect ones, we can automatically identify direct ones using source code analysis tools." (md L520–523, p.378)
- **Human error in the data**: "We collected data from 110 bulletins, published over a period of two years, by manually interpreting the bulletins' descriptions; hence the process is subject to human error." (md L649–652, p.380). And again for the patch study: "The missing type inference process is subject to human error. Hence, we repeated our experiment by analyzing only those patches that have a type assigned in the NVD." (md L732–735, p.382) — **a limitation answered by re-running the study on the cleaner subset, and reporting both numbers.**
- **Incompleteness of the dimensions**: "We, however, cannot rule out other dimensions, even though we did not find any other resource types mentioned in the bulletins." (md L616–618, p.380)
- **Two validation findings that did not come out**: "the findings with respect to channel protocol and data item type are not statistically significant and hence not conclusive (Table 8)" (md L689–691, p.381); and "The bulletins did not have any data relevant to a resource's likelihood of being used in attacks. Henc, we could not use the MSBs to validate Hypothesis 3." (md L680–683, p.381, "Henc" sic) — **a negative result reported plainly, and then routed to a different study.**
- **A negative finding turned into a method simplification**: "The subjects who disagreed with our choice were of the opinion that a channel's (data item's) damage potential depends on the methods that process the data received from the channel (data item); hence they concluded that a TCP socket and an RPC endpoint are equally attractive to an attacker, irrespective of their protocol. These findings suggest that we should assign the same damage potential, i.e., 1, to all channels and data items. In that case, we do not have to perform the difficult step of assigning total orderings among the channel protocols and the data item types." (md L692–702, p.381)
- **Known gaps in the model**: "our I/O automata model is not expressive enough to include attacks such as side channel attacks, covert channel attacks, and attacks where one user of a software system can affect other users (e.g., fork bombs)" (md L969–974, p.385); "our attack surface measurement method requires a system's source code. It may not, however, always be feasible to obtain the source code" (md L959–963, p.385).
- **What the tool cannot tell you**: "our tool guides the developers to focus on a system's relevant parts to reduce the attack surface; the tool, however, does not help in deciding when to stop the reduction process." (md L876–880, p.383)
- **The framing sentence for the whole enterprise**: "We view our work as a first step in the grander challenge of security metrics. We believe that no single security metric or measurement will be able to fulfill our requirements. We certainly need multiple metrics and measurements to quantify different aspects of security." (md L913–918, p.385)

## G. Transferable vs purpose-specific

**Transfers:**
- **The whole §5 move**: a top-level section named for validation, opening with the admission that validation is hard, then converging on the claim from several independent directions. See §H.4.
- **Informal definition in §1.2 → formal definition in §3 → instantiated definition in §4 → validated definition in §5.** The reader is never asked to hold an unexplained formalism.
- **Declaring what the metric is *not*** before anyone can misread it (md L94–99, p.371 — quoted in §H.3). A dissertation defining an attacker-side measure should copy this sentence pattern verbatim in shape.
- **Reporting a metric as a tuple of per-dimension values and refusing to aggregate**, then showing how a reader with a declared concern picks a dimension (md L560–584, p.379).
- **Pairing every "damage" attribute with an "effort" attribute** and combining them as a ratio, because "damage potential is the benefit to the attacker … and the effort is the cost to the attacker" (md L481–484, p.377).
- **Stating an explicit conservative assumption where estimation is infeasible**, with the reason: p(m) = p(c) = p(d) = 1, i.e., "every method has an exploitable vulnerability; even if a method does not have a known vulnerability now, it might have a future vulnerability not discovered so far" (md L497–503, p.378).
- **Sensitivity analysis used as a parameter-choice guideline that then feeds later work** (§E).
- **Reporting the study that failed** (Hypothesis 3 unvalidatable from MSBs; channel protocol and data item type inconclusive) and saying which other study covers the gap.
- **The related-work critique of Time-To-Compromise metrics**, which is directly relevant to this repo's MTTC comparability boundary: "McQueen et al. use an estimate of a system's expected Time-To-Compromise (TTC) as an indicator of the system's security risk [46]. TTC is the expected time needed by an attacker to gain a privilege level in a system; TTC, however, depends on the system's vulnerabilities and the attacker's skill level." (md L934–941, p.385); and on Voas's MTTI: "The MTTI value, however, depends on the threat classes simulated and the intrusion classes observed. In contrast, the attack surface metric does not depend on any threat class." (md L908–912, p.385). **Both are stated as criticisms — dependence on attacker skill and on simulated threat class is precisely what a simulator-based attacker-model dissertation must own rather than deny.**

**Purpose-specific / positioned against this dissertation:**
- **The system-centric stance is the direct antithesis of an attacker-model dissertation**, and the paper says so: "prior research on security measurement has taken an *attacker-centric* approach [44], [45], [46], [47]. In contrast, we take a *system-centric* approach. The attacker-centric approach makes assumptions about attacker capabilities and resources, whereas the system-centric approach assesses security without reference to or assumptions about attacker capabilities [48]. Our attack surface measurement is based on a system's design and is independent of the attacker's capabilities and behavior; hence our metric can be used as a tool in the software design and development process." (md L870–881, p.383). This is the strongest available statement of the position a new attacker model has to argue against — cite it as the counter-position, not as support.
- The metric is **static and per-codebase**: it needs source code, a call graph and a per-system total ordering. Nothing about it varies with a run, a defence schedule or an attacker's trajectory, so it cannot serve as an outcome measure for an MTD simulation.
- **Software-engineering venue conventions**: SDLC-phase framing (§6.4), an IDE plugin, an industrial partner, and a "lessons learned" subsection — all TSE-shaped.
- The heavy I/O-automata formalism (12 definitions, 2 theorems, proofs deferred to the thesis) is a TSE-scale investment. The *sequence* transfers; the volume does not.

## H. How a security metric is introduced and validated

### H.1 The definition-before-use sequence

The paper introduces its metric in **five escalating passes**, and never uses a term before it has been given at that level of precision. This ordering is the transferable artefact.

1. **Pass 0 — the one-sentence intuition, in the introduction, before any machinery.** "Intuitively, a system's attack surface is the set of ways in which an adversary can enter the system and potentially cause damage. Hence, the 'smaller' the attack surface, the more secure the system." (md L36–39, p.371). Two sentences: what it is, and which way it points. Note "Intuitively" is doing declared work — it flags that this is not yet the definition.
2. **Pass 1 — the informal decomposition, §1.2, still before any formalism.** The attacker's means are enumerated from attack experience ("many attacks on a system take place either by sending data from the system's operating environment into the system (e.g., buffer overflow exploitation) or by receiving data from the system (e.g., symlink attacks)", md L54–58, p.371), which yields the three resource kinds: "an attacker uses a system's methods, channels, and data items present in the environment to attack the system. We collectively refer to the methods, channels, and data items as the resources and thus define a system's attack surface in terms of the system's resources (Fig. 2)." (md L71–76, p.372). Then the two refinements are named and each is bound to the machinery that will deliver it: "A resource is part of the attack surface if an attacker can use the resource to attack the system; we introduce an *entry point and exit point framework* to identify these relevant resources. A resource's contribution to the attack surface reflects the resource's likelihood of being used in attacks. … We introduce the notion of a *damage potential-effort ratio* to estimate a resource's contribution." (md L79–87, p.372).
3. **Pass 2 — the negative definition, immediately after, so the metric cannot be misread.** Quoted in H.3.
4. **Pass 3 — the formal definitions, §3**, twelve of them, each introducing exactly one notion, in dependency order: direct entry point (Def. 1) → indirect entry point (Def. 2) → direct exit point (Def. 3) → indirect exit point (Def. 4) → untrusted data item (Def. 5) → **attack surface** (Def. 6) → larger attack surface, qualitative (Def. 7) → potential attack (Def. 8) → resource contribution ordering (Defs. 9, 10) → larger attack surface measurement, qualitative (Def. 11) → **quantitative attack surface measurement** (Def. 12). Two theorems connect the definitions to the thing anyone actually cares about (number of possible attacks). *Nothing is measured until all twelve exist.*
5. **Pass 4 — the instantiation, §4**, which is where language-specific and system-specific choices enter, explicitly labelled as such: "In this section, we **instantiate** the previous section's abstract measurement method for systems implemented in the C programming language" (md L510–512, p.378). The generic definition and the C-specific realisation are kept in separate sections, so a reader can reject the instantiation without rejecting the metric — and §6 exploits exactly that by re-instantiating for Java.

### H.2 The formal definition

**The qualitative object (Definition 6, md L260–266, p.375):**
> "Given a system, s, and its environment, E_s, s's attack surface is the triple, ⟨M^{E_s}, C^{E_s}, I^{E_s}⟩, where M^{E_s} is s's set of entry points and exit points, C^{E_s} is s's set of channels, and I^{E_s} is s's set of untrusted data items."

with the relativisation made explicit in the following sentence: "Notice that we define s's entry points and exit points, channels, and data items with respect to the given environment E_s. Hence s's attack surface, ⟨M^{E_s}, C^{E_s}, I^{E_s}⟩, is with respect to the environment E_s." (md L267–272, p.375). And the comparability precondition, stated before any comparison is attempted: "We compare the attack surfaces of two similar systems (i.e., different versions of the same software or different software that provide similar functionality) along the methods, channels, and data dimensions **with respect to the same environment** to determine if one has a larger attack surface than another." (md L272–275, p.375).

**The contribution weight (§3.3.1, md L479–484, p.377):**
> "Hence we consider damage potential and effort in tandem and quantify a resource's contribution as a damage potential-effort ratio. The ratio is similar to a cost-benefit ratio; the damage potential is the benefit to the attacker in using a resource in an attack and the effort is the cost to the attacker in using the resource."

Formally, functions `der_m : method → ℚ`, `der_c : channel → ℚ`, `der_d : data item → ℚ` (md L437–445, p.377). In practice, "we compute a resource's damage potential-effort ratio by assigning numeric values to the resource's attributes" (md L445–450, p.377) — the six attributes being method privilege and access rights, channel protocol and access rights, data item type and access rights (md L640–643, p.380).

**The quantitative metric (Definition 12, md L454–458, p.377):**
> "Given a system, s's, attack surface, ⟨M^{E_s}, C^{E_s}, I^{E_s}⟩, s's attack surface measurement is the triple ⟨ Σ_{m∈M^{E_s}} der_m(m), Σ_{c∈C^{E_s}} der_c(c), Σ_{d∈I^{E_s}} der_d(d) ⟩."

**Grounded in an existing formalism, explicitly.** "Our attack surface measurement method is analogous to the risk estimation method used in risk modeling [11]. … In risk modeling, the risk associated with a set E of events is Σ_{e∈E} p(e) C(e), where an event, e's, occurrence probability is p(e) and consequence is C(e). The events in risk modeling are analogous to the resources in our measurement method. An event's occurrence probability is analogous to the probability of a successful attack using a resource. … An event's consequence is analogous to a resource's damage potential-effort ratio." (md L460–487, p.377). The full risk form is therefore ⟨Σ p(m)der_m(m), Σ p(c)der_c(c), Σ p(d)der_d(d)⟩, and Definition 12 is that form under a stated conservative assumption: "In practice, however, predicting defects in software [12] and estimating the likelihood of vulnerabilities in software are difficult tasks [13]. Hence we take a conservative approach in our measurement method and assume that p(m) = 1 for all methods, i.e., every method has an exploitable vulnerability; even if a method does not have a known vulnerability now, it might have a future vulnerability not discovered so far. We similarly assume that p(c) = 1 for all channels and p(d) = 1 for all data items." (md L495–504, p.378). **Convention worth stealing: define the general form first, then set the unmeasurable factor to a stated constant and say why — rather than defining the simplified form and never mentioning what was dropped.**

**The two theorems that license the metric's use** (proofs omitted, deferred to [10]):
- *Theorem 1* (md L321–328, p.375): "Given an environment, E = ⟨U, D, T⟩, and systems, A and B, if A's attack surface, ⟨M^E_A, C^E_A, I^E_A⟩, is larger than B's attack surface, ⟨M^E_B, C^E_B, I^E_B⟩, and the rest of the resources of A and B are equal, then attacks(A) ⊇ attacks(B)."
- *Theorem 2* (md L436–443, p.377): the same conclusion from a larger attack surface *measurement* rather than a larger attack *surface*.
- With the comparability assumption made explicit beforehand: "Since A and B are similar systems … we assume that both A and B have the same set of state variables and the same set of resources except the ones appearing in the attack surfaces." (md L313–320, p.375).
- And each theorem is immediately given a practical reading: "Theorem 1 has practical significance in the software development process. The theorem shows that if we create a newer version of a software system by only adding more resources to an older version, then assuming all resources are counted equally (see Section 3.2), the newer version has a larger attack surface, and hence, a larger number of potential attacks." (md L328–337, p.375–376).

### H.3 The direction statement

Stated **positively, negatively and comparatively, all within one page**, before any formalism:

- **Positive direction** (md L38–39, p.371): "Hence, the 'smaller' the attack surface, the more secure the system." *(the scare quotes around "smaller" are the authors' — the ordering is not yet defined at that point.)*
- **The negative statement — what a measurement does NOT mean** (md L94–99, p.371):
  > "A large measurement does not imply that the system has many vulnerabilities, and having few vulnerabilities does not imply a small measurement. Instead, a larger measurement indicates that an attacker is likely to exploit the vulnerabilities present in the system with less effort and cause more damage to the system."
- **The comparative frame — the metric is ordinal and per-dimension, not absolute** (md L99–102, p.371):
  > "Given two systems, we compare their attack surface measurements to indicate, along each of the three dimensions, whether one is more secure than the other with respect to the attack surface metric."
  Note the closing qualifier "with respect to the attack surface metric": the claim is scoped to the metric, not to security in general.
- **Direction of each component** (md L350–358, p.376): "A resource's contribution to a system's attack surface depends on the resource's damage potential, i.e., the level of harm the attacker can cause to the system in using the resource in an attack and the effort the attacker spends to acquire the necessary access rights in order to be able to use the resource in an attack. **The higher the damage potential or the lower the effort, the higher the resource's contribution to the attack surface.**"
- **The prescription that follows from the direction** (md L336–341, p.376): "Software developers should ideally strive toward reducing the attack surface of their software from one version to another, or if adding resources to the software (e.g., adding methods to an API), then do so knowing that they are increasing the attack surface."
- **And the honest scope of the whole claim** (md L913–918, p.385): "We believe that no single security metric or measurement will be able to fulfill our requirements. We certainly need multiple metrics and measurements to quantify different aspects of security."

### H.4 How the paper validates that the metric measures what it claims

**All four validation modes are used: an empirical statistical study, an expert survey, an empirical case-controlled study, and anecdotal industry evidence — plus a fifth, external theoretical validation by other authors.** This is the section to model on.

**The framing (md L585–593, p.379):**
> "A key challenge in security metrics research is the validation of a metric. Validating a software attribute's measure is hard [17], [18], [19]; security is an attribute that is hard to measure and hence even harder to validate. To validate our metric, we conducted three exploratory empirical studies inspired by the research community's software metrics validation approaches [20], [21]."

**The validation theory it borrows, stated explicitly before the studies (md L594–607, p.379–380):**
> "In practice, validation approaches distinguish measures from prediction systems; measures numerically characterize software attributes whereas prediction systems predict software attributes' values. For example, lines of code (LOC) is a measure of software 'length'; LOC becomes a prediction system if we use LOC to predict software 'complexity.' We validate a measure by showing its correctness in numerically characterizing an attribute and a prediction system by showing its accuracy. Our attack surface metric plays a dual role: It measures a software attribute, i.e., the attack surface, and is also a prediction system to indicate software's security risk. Hence we took a two-fold validation approach."

**The convergence argument, stated as a method, not an excuse (md L607–616, p.380):**
> "First, we validated the measure by validating our measurement method using two empirical studies: a statistical analysis of data collected from Microsoft Security Bulletins (Section 5.1) and an expert user survey for Linux (Section 5.2). Our approach is motivated by the notion of *convergent evidence* in Psychology [22]; since each study has its own strengths and weaknesses, the convergence in the studies' findings enhances our belief that the findings are valid and not methodological artifacts."
>
> "Second, we validated our metric's prediction system by validating attack surface measurements. In Section 3, we formally showed that a larger attack surface leads to a larger number of potential attacks on software. We established a relationship between attack surface measurements and security risk by analyzing vulnerability patches in open source software (Section 5.3). We also gathered anecdotal evidence from software industry to show that attack surface reduction mitigates security risk (Section 5.4)." (md L617–625, p.380)

**External theoretical validation, credited to third parties (md L626–630, p.380):**
> "Liu and Traore introduce a theoretical validation framework, based on established security design principles, to validate security metrics [23]. They demonstrate that our metric is valid in their framework; their theoretical validation complements our empirical studies."

**The method is decomposed into falsifiable hypotheses before it is tested (md L634–646, p.380)** — this is the pivot of the whole section:
> "Our measurement method is based on the following three key hypotheses; hence we validated the hypotheses to validate the method.
> 1. Methods, channels, and data are the attack surface's dimensions.
> 2. The six resource attributes (method privilege and access rights, channel protocol and access rights, and data item type and access rights) are indicators of damage potential and effort.
> 3. A resource's damage potential-effort ratio is an indicator of the resource's likelihood of being used in attacks."

**Study 1 — statistical analysis of Microsoft Security Bulletins (§5.1).**
- Data: "We collected data from 110 bulletins, published over a period of two years, by manually interpreting the bulletins' descriptions; hence the process is subject to human error. We identified the resources (methods, channels, and data items) that the attacker has to use to exploit the vulnerabilities described in the bulletins, the resources' attributes that are indicators of damage potential and effort, and the bulletins' severity ratings. Many bulletins contained multiple vulnerabilities; hence the 110 bulletins resulted in **202 observations**." (md L649–658, p.380)
- **Hypothesis 1, by frequency count**: "Out of the 202 observations, 202 mention methods, 170 mention channels, and 108 mention data items as the resources used in exploiting the vulnerabilities. These findings suggest that methods, channels, and data items are used in attacks on software and hence are the attack surface's dimensions. We, however, cannot rule out other dimensions, even though we did not find any other resource types mentioned in the bulletins." (md L660–663 + L614–618, p.380)
- **Hypothesis 2, by regression against an external ground truth.** The external variable is Microsoft's own severity rating, and the analogy to the metric's two halves is argued first: "A bulletin's severity rating depends on Microsoft's assessment of the impact of exploiting the vulnerability described in the bulletin and the exploitation's difficulty. The higher the impact and the lower the difficulty, the higher the rating. The exploitation's impact and difficulty are equivalent to damage potential and attacker effort in our measurement method, respectively. Hence we expect the severity rating to depend on the six attributes … we also expect the severity rating to increase with an increase in the value of an attribute that is an indicator of damage potential, e.g., method privilege, and to decrease with an increase in the value of an attribute that is an indicator of attacker effort, e.g., method access rights. In other words, we expect an indicator of damage potential (effort) to be a significant predictor of the severity rating and to be positively (negatively) correlated with the severity rating." (md L621–637 + L644–647, p.380) — i.e. **the sign of the coefficient is predicted in advance, so the test can fail.**
  Test: "We used ordered logistic regression to test for the attributes' significance as logistic regression uses maximum likelihood estimates to compute the regression coefficients. A positive coefficient indicates a positive correlation between an attribute and the severity rating, and a negative coefficient indicates a negative correlation. We used z-tests to determine the coefficients' statistical significance (p-value < 0.05); our null hypothesis was that the coefficients are zero and hence the attributes are not significant predictors of the severity rating." (md L637–647, p.380). Scale handling is declared: total orderings and ordinal values for privileges, access rights and severity; nominal values for channel protocols and file formats, "Since nominal values are not ordered, we could not determine a positive or negative correlation with severity rating." (md L650–659, p.380).
  Results — **TABLE 5, "Significance of Method and Channel Attributes"** (p.380):

  | Attribute | Coefficient | Standard Error | p-value |
  |---|---|---|---|
  | *Methods* | | | |
  | Privilege | 0.948 | 0.236 | p < 0.001 |
  | Access Rights | −0.584 | 0.110 | p < 0.001 |
  | *Channels* | | | |
  | SMTP | 2.535 | 0.504 | p < 0.001 |
  | TCP | 0.957 | 0.466 | p = 0.040 |
  | Pipe | 0.948 | 0.574 | p = 0.099 |
  | Access Rights | −0.312 | 0.109 | p = 0.004 |

  **TABLE 6, "Significance of Data Item Attributes"** (p.381):

  | Attribute | Coefficient | Standard Error | p-value |
  |---|---|---|---|
  | HTML | −0.651 | 0.263 | p = 0.013 |
  | DHTML | −0.589 | 0.437 | p = 0.177 |
  | ActiveX | 1.522 | 0.480 | p = 0.002 |
  | WMF | 46.314 | 2.58e+09 | p = 1.000 |
  | Doc | −1.123 | 0.462 | p = 0.015 |
  | Access Rights | −0.310 | 0.078 | p < 0.001 |

  Read as: "A method's privilege (Table 5, row 3), a method's access rights (Table 5, row 4), a channel's access rights (Table 5, row 9), and a data item's access rights (Table 6, row 8) are significant predictors of the severity rating and exhibit expected correlation with the severity rating. Table 5 shows that SMTP and TCP are significant and pipe is insignificant in explaining the severity rating. Since two of the three protocols are significant, the finding suggests that channel protocol is a significant predictor of the severity rating." (md L669–677, p.381). **Note the signs match the predicted directions: damage-potential attributes positive, effort (access-rights) attributes negative in all three rows.**
- **Hypothesis 3 could not be tested here, and the paper says so and reroutes it**: "The bulletins did not have any data relevant to a resource's likelihood of being used in attacks. Henc, we could not use the MSBs to validate Hypothesis 3. We used an expert survey described in Section 5.2 to validate Hypothesis 3." (md L680–683, p.381)

**Study 2 — expert user survey (§5.2).** Two stated reasons, one of which is an explicit generalisation check: "First, we wanted to find out potential users' perception of our metric. Second, our MSB analysis was with respect to Windows; we conducted the survey with respect to Linux." (md L688–691, p.381).
- Subjects: "We identified **20 experienced system administrators** working in universities, corporations, and government agencies as our survey's subjects." (md L700–703, p.381), chosen because "Software developers and software consumers are our metric's two potential user groups … System administrators are examples of software consumers" (md L694–698, p.381).
- Instrument, with bias controls named: "The survey questionnaire consisted of six explanatory questions designed to measure the subjects' attitude about our measurement method's steps. The first five questions asked the subjects to indicate their degree of agreement or disagreement with the steps. We used the last question to collect information about the subjects to avoid **self-selection bias**, i.e., the subjects incorrectly consider themselves expert system administrators without relevant experience or expertise. The subjects indicated their attitude on a five-point Likert scale … We conducted six rounds of pretesting and post-test interviews to identify and remove leading questions, ambiguous terms, and overall confusing questions from the questionnaire." (md L704–719, p.381)
- Analysis, with a second bias control named: "We combined the 'strongly agree' and the 'agree' responses … and the 'strongly disagree' and the 'disagree' responses … to avoid **central tendency bias** … We performed t-tests to determine the survey responses' statistical significance (p-value < 0.05); we used the null hypothesis that the mean of a survey question's Likert scale responses is 'neutral.'" (md L669–683, p.381)
- Results — **TABLE 7, "The Subjects' Perception about the Dimensions and the Damage Potential-Effort Ratio"** (p.381):

  | | Agree | Disagree | Neutral | p-value |
  |---|---|---|---|---|
  | *Dimensions* | | | | |
  | Methods | 95% | 0% | 5% | p < 0.0001 |
  | Channels | 95% | 0% | 5% | p < 0.0001 |
  | Data | 85% | 0% | 15% | p < 0.0001 |
  | *Damage Potential-Effort Ratio (der)* | | | | |
  | der | 70% | 20% | 10% | p = 0.0141 |

  **TABLE 8, "The Subjects' Perception about the Attributes"** (p.381):

  | Attribute | Agree | Disagree | Neutral | p-value |
  |---|---|---|---|---|
  | Method Privilege | 90% | 0% | 10% | p < 0.0001 |
  | Access rights | 70% | 5% | 25% | p = 0.0001 |
  | Channel Protocol | 45% | 25% | 30% | p = 0.2967 |
  | Access Rights | 75% | 5% | 20% | p < 0.0001 |
  | Data Item Type | 45% | 5% | 50% | p = 0.8252 |
  | Access Rights | 85% | 10% | 5% | p < 0.0001 |

  Reported honestly, including the two that failed: "the findings with respect to channel protocol and data item type are not statistically significant and hence not conclusive (Table 8)" (md L689–691, p.381) — and then the disagreeing minority's *reason* is elicited and converted into a proposed simplification of the method (quoted in §F).

**Study 3 — open-source patch analysis (§5.3), validating the prediction system.** The logic: "A vulnerability patch reduces a system's security risk by removing an exploitable vulnerability from the system; hence we expect the patch to reduce the system's attack surface measurement. We demonstrated that a majority of patches in open source software reduce the attack surface measurement." (md L706–724, p.381–382)
- **Relevance is defined before the data is touched, and the exclusion is principled**: "Not all patches are relevant to the measurement. A patch is relevant if we expect the patch to remove a vulnerability by modifying the number of resources that are part of the attack surface or by modifying such resources' damage potential-effort ratios. For example, we expect a patch that resolves authentication issues to affect the resources' access rights; hence the patch is relevant. We, however, do not always expect the patches for buffer overruns to affect the attack surface measurement." (md L727–735, p.382). Relevance is decided by an **external, independent classification** — the NVD's CWE vulnerability type (md L736–747, p.382) — and the seven admissible types are listed: "Authentication Issues; Permissions, Privileges, and Access Control; Cross-Site Scripting (XSS); Format String Vulnerability; SQL Injection; OS Command Injection; and Information Disclosure." (md L748–752, p.382). The paper further predicts *which* of those should always reduce the measurement and which need not: "If a vulnerability has one of the first two types, we always expect the vulnerability's patch to reduce the measurement. The vulnerabilities belonging to the last five types can be patched in different ways; hence the patches may not always reduce the measurement." (md L753–758, p.382)
- **Headline result**: "Our results indicate that **67 percent and 70 percent of the relevant patches reduced the attack surfaces of Firefox and the ProFTP server, respectively (confidence level = 95%, p < 0.05)**." (md L761–766, p.382)
- Full accounting, with the non-reducing cases named and explained: Firefox 2.0.0.1–2.0.0.8, 48 C/C++ vulnerabilities with public patch source, 12 relevant, "eight of these patches reduced the measurement and four did not change the measurement. Three out of the four patches that did not reduce the measurement are patches of three XSS vulnerabilities. We do not expect XSS vulnerability patches to always reduce the attack surface measurement." (md L767–782, p.382). ProFTP: 21 vulnerabilities from NVD, 10 relevant, "seven of these patches reduced the measurement and three format string vulnerability patches did not change the measurement." (md L722–732, p.382)
- **The robustness re-run**, on the subset that needed no human type inference: "The missing type inference process is subject to human error. Hence, we repeated our experiment by analyzing only those patches that have a type assigned in the NVD. Our results show that **76.9 percent of the relevant patches reduced the attack surface measurement (confidence level = 95%, p < 0.05)**." (md L732–735, p.382)
- **The sampling funnel is reported in full**, including everything lost: "The NVD contains 25,000 bulletins; only 363 bulletins, however, have a vulnerability type and contain one or more hyperlinks to their patches. We identified 73 C/C++ vulnerability bulletins out of the 363 to be relevant to the attack surface measurement based on their type. We could, however, obtain source code of only 13 patches; in the case of the remaining 60 bulletins, the hyperlinks labeled as patch information point to downloadable patches in binary format (e.g., patches of commercial software). Ten out of these 13 patches reduced the attack surface measurement. One was a format string vulnerability patch and two patches used cryptographic techniques to remove vulnerabilities; hence the three patches did not reduce the measurement." (md L736–758, p.382)

**Study 4 — anecdotal evidence (§5.4), labelled as anecdotal in the heading and the first sentence.** "Anecdotal evidence from industry demonstrates that reducing the attack surface mitigates software security risk." (md L750–752, p.382). Three worked cases, each a natural experiment where an attack surface reduction coincided with immunity: the Sasser worm against Windows 2000/XP but not Windows Server 2003, where the vulnerable RPC interface "was made to be accessible by only local administrators … because of the entry point's higher access rights" (md L754–762, p.382); Microsoft's Kill-Bits reducing browser attack surface (md L765–770, p.382); and SSL 2 turned off by default in Firefox 2.0 so that "Firefox 2.0's default configuration was immune to attacks that exploit the vulnerability, whereas Firefox 1.5 was not" (md L771–777, p.382).

**Study 5 — the industrial case study (§6)** is not labelled validation but functions as a feasibility-and-usefulness check: "The measurement results show that our measurement approach is feasible for SAP's complex systems. We also received positive feedback from SAP's developers on the usefulness of the measurement process." (md L864–867, p.383), and the ordering test against known release history quoted in §C. Adoption is offered as a final external signal: "Howard's measurement method is already used on a regular basis as part of Microsoft's Security Development Lifecycle. Mu Security's Mu-4000 Security Analyzer uses our measurement framework for security analysis [53]. SAP is also planning to use attack surface measurements in their software quality improvement process." (md L951–957, p.385).

### H.5 The validation move, distilled

Decompose the method into three falsifiable hypotheses; test each against **external ground truth the authors did not produce** (Microsoft's severity ratings, expert practitioners' judgements, the NVD's CWE types, patch histories) using a **named statistical test with a stated null and a pre-declared direction**; run **more than one study on different populations** (Windows bulletins, Linux administrators, open-source patches) and argue *convergent evidence* explicitly; **report the hypotheses that could not be tested and the attributes that came out insignificant**; **re-run the study on the cleaner subset** when a step was subject to human error, and report both numbers; and separate the validation of the *measure* from the validation of the *prediction system*, because they require different evidence (correctness vs accuracy).
