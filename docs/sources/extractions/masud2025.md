# Masud 2025 — extraction notes

> M. T. Masud, M. Keshk, N. Moustafa, B. Turnbull, W. Susilo. "Vulnerability defence using hybrid moving target defence in Internet of Things systems." *Computers & Security*, vol. 153, art. 104380, 2025.
> Source file: `docs/sources/1_3_masud2025vulnerability.md` (gitignored).
> Relevance to this thesis: the *specified pole* of the orchestration spectrum in lit review §II-C — three-layer Temporal HARM (T-HARM) with explicit MTD-coexistence conflict-resolution rules (priority queue + suspension list); evaluated across attack risk, attack cost, RoA.

## Bibliographic anchor

- **Citation key**: `masud2025`
- **DOI / URL**: 10.1016/j.cose.2025.104380
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**C — contrast / adjacent.** Masud anchors the §IV-B Table II cross-section at the *scripted* rung of the fidelity descriptor and is one of the two papers that drive the "rhetoric-versus-execution gap" pattern that section diagnoses (the other being [[kim2026]]). It is contrasted-against, not adopted: the contribution this thesis takes from it is a *placement* on the fidelity ladder ([`../specs/architecture.md`](../../implementation/architecture.md) §(j), [`../sources/LIT_REVIEW.md`](../lit_review/LIT_REVIEW.md) L195) — not an orchestration primitive, metric definition, or substrate choice. (Note: Masud is also the *specified pole* exemplar in §II-C of the orchestration spectrum, but that placement is rhetorical scene-setting; the load-bearing use is the §IV-B Table II row.)

### Threat-model placement on the Table II fidelity descriptor

**Source locator:** §3.1 "Threat model" (lines 186–188); §3.3 experimental-validation paragraph (line 299); coexistence rules at §3.2 (line 192) and §3.3 (line 246). Locator format is §/heading plus markdown line number — the Elsevier-extracted markdown does not preserve PDF page numbers as inline anchors (the running header "Computers & Security 153 (2025) 104380" appears between sections without numbering).

**Paraphrase:** The threat model is specified in §3.1 as an external adversary attempting to reach the database on host8 by exploiting OS-level vulnerabilities in IoT devices, with hypervisor isolation between VMs assumed. The adversary's behavioural realisation is left to the experimental-validation paragraph (§3.3, L299), which states the attackers were "modeled after techniques in the cyber kill chain and MITRE ATT&CK" and that vulnerabilities were "prioritized by return on attack". In execution, however, the attacker is the path enumeration the security-metrics algorithm runs — `all_simple_paths(G, Ss, Tr)` over the 3-layer THARM (Algorithm 2, L414), producing ASP / AR / AC / RoA values aggregated across every simple path between source and target. There is no per-step decision agent, no runtime adaptation, and no technique-level behaviour beyond the CVE/CVSS-parameterised graph the algorithm traverses; the kill-chain framing names a vocabulary but does not enter the executed model. This is *scripted* fidelity in the §IV-B sense — a pre-coded traversal against specific CVEs — sitting one rung above the *parametric* placement of [[brown2023]] / [[tay2024]] / [[he2025]] and on the same rung as [[kim2026]].

**Quote (if essential):**
> "Attackers were modeled after techniques in the cyber kill chain and MITRE ATT&CK, mirroring real threats. ... Vulnerabilities were prioritized by return on attack, emphasizing those with greatest impact." (§3.3, L299)

**Maps to:** [`../sources/LIT_REVIEW.md`](../lit_review/LIT_REVIEW.md) §IV-B "_3) Masud et al., 2025_" (L185) and Table II row (L205) · [`../specs/architecture.md`](../../implementation/architecture.md) §(j) "behavioural fidelity changes the answer" framing (L460–462)

**Disposition for this thesis:** **contrasted-against.** Masud occupies the row on the fidelity descriptor that this thesis's L2/L3 GASP→OGASP attacker design is built *up from*. The placement is *not* a deficiency — Masud's contribution is on the orchestration side (coexistence rules between IP-shuffle, OS-diversity, redundancy via a priority queue + suspension list, §3.2 L192 and Algorithm 1 L361–393), where the threat model functions as evaluation backdrop rather than the focus. Used in the lit review to ground the §IV-B claim that *across the cross-section* the threat model sits markedly below the rung the defence claims to operate at — the rhetoric-versus-execution gap that opens the space for this thesis. The §II-C "specified pole" use of Masud (orchestration as explicit conflict-resolution rules) is rhetorical scene-setting, not a primitive this work adopts — the lineage substrate inherits no orchestration logic from Masud.

---

### Used in lit review

- [`../sources/LIT_REVIEW.md`](../lit_review/LIT_REVIEW.md) L85 — §II-C "specified pole" of the orchestration spectrum: priority queue + suspension list as the conflict-resolution mechanism; evaluation across attack risk, attack cost, and RoA. *Rhetorical scene-setting for the orchestration spectrum's specified end.*
- [`../sources/LIT_REVIEW.md`](../lit_review/LIT_REVIEW.md) L177 — §IV-B introduction: Masud listed as the "recent IoT-cloud orchestration" point of the five-paper cross-section.
- [`../sources/LIT_REVIEW.md`](../lit_review/LIT_REVIEW.md) L185 — §IV-B per-paper justification: scripted-fidelity placement; the "modeled after techniques in the cyber kill chain and MITRE ATT&CK" quote ([11, p. 7]) carries the rhetoric-versus-execution gap.
- [`../sources/LIT_REVIEW.md`](../lit_review/LIT_REVIEW.md) L205 — Table II row: Persistent ✗ · Adaptive ✗ · Stealthy ✗ · Incentive-aware ✗ · Fidelity scripted.
- [`../sources/LIT_REVIEW.md`](../lit_review/LIT_REVIEW.md) L195 — §IV-B general observations: Masud cited alongside [[kim2026]] as clustering at *scripted* on the ladder; collectively anchors the "located asymmetry" framing this thesis takes up.

---

## Open questions / things to verify

- The lit review cites the kill-chain framing as `[11, p. 7]`. The source markdown does not expose page numbers inline; the quoted text sits at L299 immediately following Table 4. Verify against the PDF that the "p. 7" anchor in the lit review is correct, since the bibliographic anchor was settled but PDF-page-to-markdown-line is not.
- Whether the "vulnerabilities prioritized by return on attack" mention (§3.3, L299) corresponds to a single design-time ordering or to a per-step RoA evaluation. The Algorithm 2 / Eq. 4 formulation computes RoA as a static ratio of accumulated risk to accumulated cost over an attack path; there is no evidence of a runtime per-step prioritisation. Worth verifying against §4 results to be sure the *evaluation* doesn't enact a per-step RoA decision the algorithmic description omits.

## Out of scope for this thesis

- IoT-specific architecture details unless they bear on the orchestration logic.

---

## Eight-property verification (2026-09-07, independent pass for Table 3.3)

Source read in full (`lit_review/1_3_masud2025vulnerability.md`); threat model §3.1 (l.186–188), the attacker-behaviour paragraph §3.3 (l.299 — the converter displaced it; it continues l.327), definitions §3.4 (l.339–357), Algorithm 2 §3.5 (l.394–446), results §4.2–4.5 (l.580–628). Marks as in the Table 3.3 decode.

Executed attack: **no attacker agent runs.** The "attacker" is a graph node (V_hS, S_hS, Def. 1–4) with edges to the entry VMs; the evaluation enumerates every simple path from it to the target — `AP = all_simple_paths(G, Ss, Tr)` (l.414, Algorithm 2) — on the THARM graph at each interval and recomputes CVSS-derived ASP / risk / attack cost / RoC per VM, per path and network-wide before and after each MTD deployment.

| # | Property | Mark (strict / generous) | Evidence | Reason |
|---|---|---|---|---|
| 1 | Persistence | NONE / HALF | attack path "a sequence of consecutive VMs… from the entry node… to the target node" (l.270–273, Table 3); metrics "across time internals" (l.628) | multi-hop paths exist as structure, re-evaluated on the defender's 10 min trigger (Table 4, l.318); nothing pursues them |
| 2 | Objective conditioning | NONE / HALF | "The attacker's objective is to breach the database (DB) on host8" (l.188, §3.1); Tr fixes the enumeration (l.414) | the objective fixes the target node of an exhaustive enumeration; no post-foothold behaviour exists to be conditioned; "widespread and focused attacks" (l.299) has no algorithm, parameter or result |
| 3 | Strategic plurality | NONE / HALF | "for ap in AP do… for Vi in ap" (l.414); "ASP across eight different paths" (l.596); OR-gate attack trees per VM (l.357, Def. 4) | plural paths enumerated exhaustively and aggregated; no attacker chooses among them |
| 4 | Adaptivity | NONE | "The edge set can be modified for different MTD strategies… at different times (tn)" (l.400); framing "forcing fresh scans and adaptation to new flaws" (l.299), "continuously adapt" (l.651) | re-enumeration on the post-MTD graph is the analyst's; the adaptation claims (l.299, 536, 651, 657) have no mechanism |
| 5 | Stealth | NONE | "the IP-shuffling method renders 40% of reconnaissance attempts ineffective" (l.572); IPV = IP-set difference between time points (l.496–500); "attackers will be none the wiser" (l.242) | no scanning, evasion or detection executed; IPV is a defender-side address-churn metric glossed as reconnaissance defeated |
| 6 | Incentive-driven rationality | NONE / HALF | "RoCvi = Rvi / ACvi" (l.420, Alg. 2 Eq. 4); "A higher RoA number means that attackers are more likely to take advantage of weaknesses" (l.446, §3.5.4); "Vulnerabilities were prioritized by return on attack" (l.299, §3.3, p.7) | **RoA is computed over enumerated paths as a metric and reported as an outcome** (RoCap1 = 0.259, RoCs = 1.01, l.584–586; Fig. 8/9); it is an input to the defender's Algorithm 3, whose selection is `rank(argmax(Cvi, Dvi, Bvi))` over centralities (Eq. 8, l.468), not RoA; no equation, algorithm or figure has the attacker selecting anything by RoA. The l.299 sentence is the only support for a per-step reading and nothing instantiates it. → the Table 3.3 dash stands on the strict rule |
| 7 | Learning | NONE | silent; "more likely to attempt the same attack again, given it was previously successful" (l.586) is interpretive | no attacker state across intervals or deployments |
| 8 | Scheme awareness | NONE | "attackers will be none the wiser about the hosts they previously discovered being invalid" (l.242); "creating a scheme to breach the system" (l.570) is the ordinary sense | attacker explicitly unaware of the shuffle |

Framing vs execution (all without mechanism): l.96 "defense-adversary interaction model… force rescanning, credential reuse"; l.299 kill chain / ATT&CK / widespread-vs-focused / RoA prioritisation / command channels / fresh scans (ATT&CK is not in the reference list; Hutchins 2011 is the only kill-chain source); l.430 ASP "accounting for the attacker's available resources" (Eq. 1 uses CVSS exploitability only); l.657 "attackers will have to change their strategies"; l.693 future work names "assessment against sophisticated attacks". Terminology: the quantity is written RoA (l.62, l.446), RoC / "Return of attack" (Table 3, Alg. 2–3, §4.2–4.4) and "Return on Cost (RoC)" (l.628) — recorded, not asserted as inconsistency. Two scales (8-VM and 400-VM), one attacker node. Per-CVE costs C_v, C_s (Tables 1–2) are graph parameters, not a budget spent.

Locator verified: "modeled after techniques in the cyber kill chain and MITRE ATT&CK" — PDF page 7 of 17, footer "Computers & Security 153 (2025) 104380 7" → **p. 7 correct** (the earlier open question is closed); same page carries "prioritized by return on attack". Algorithm 2 / §3.5.4 p.9; l.586 p.13; l.657 p.15.

## Fair re-score as an analytical attacker model (2026-10-02, blind pass, PROPOSED — Marc rules)

**Why.** Marc (2026-10-02) asked whether Masud's model had been scored fairly. The
2026-09-07 rule ("a half needs something the executed attacker does… a paper that
runs no attacker earns nothing") scores every analytical model zero by construction.
That contradicts ch3 §3.2, which names analytical models as a legitimate MTD
evaluation method.

**The pass.** An independent reader scored the whole text (l.1–831) blind to this
file, the dissertation and the handoffs. Rule: an analytical attacker model is the
set of assumptions its computation makes about the attacker; credit what enters the
computation, and report framing separately.

| # | Blind mark | Evidence (line) | Session adjustment |
|---|---|---|---|
| 1 | partial | a multi-hop path from an entry VM to the target, re-evaluated per time instance (l.512, l.345, l.628); no campaign state carried between snapshots | keep |
| 2 | partial | one fixed objective bounds the path set: the database on host 8 (l.188, l.414) | **none**. Column consistency: Kim's single fixed objective scores none, and the lineage's partial rests on two scenarios |
| 3 | partial | every simple path enumerated and aggregated, none chosen (l.414, l.287) | keep |
| 4 | partial, borderline none | graph edited and the path set recomputed after each MTD change (l.400, l.299, l.584); the attacker holds no state | keep, flagged borderline |
| 5 | none | detection only as framing (l.21, l.454) | — |
| 6 | partial | per-vulnerability cost (Tables 1–2, l.206–232); RoA = risk/cost per VM and path (l.420, l.446), driving no attacker-side choice; Algorithm 3 ranks by centrality (l.468) | keep, flagged borderline (a computed metric) |
| 7 | none | memory only as framing (l.68, l.536, l.586) | — |
| 8 | none | scheme logic on the defender's side only (l.192, l.318) | — |

**Framing versus computation.** The framing (the kill chain and ATT&CK, RoA
prioritisation, "forcing fresh scans and adaptation" at l.299; the
defence–adversary interaction model at l.96; continuous adaptation at l.651 and
l.657; a Bayesian attack graph at l.92) does not enter Algorithm 2 (l.408–426) or
Algorithm 3 (l.464–486).

**Fair credit.** The attacker is modelled at two layers: reachable VMs, and
exploitable OS and service vulnerabilities, each with a cost. Its full path set,
success probability, cost and return are recomputed after every MTD change, so each
shuffle, OS swap or replica measurably changes what it can reach and what reaching
it costs.

**If ruled, the blast radius:**

- Table 3.3;
- tab:fidelity-verdict (the ch6 twin);
- apt_model_criterion.md §(c), the prior-work column;
- the §3.3.2 Masud paragraph and close;
- the "strict but generous" rule text in the Table 3.3 comment block.

## Attacker model, extracted for the predicate tests (2026-10-12)

Source: the published PDF (Computers & Security 153, 104380; CC BY). Pages are as printed. The **attacker model as computed** (A–D) is listed apart from the **attacker as described** (E). E is prose about the attacker that no definition, algorithm, symbol or result carries; the earlier passes call it "framing".

### A. What the attacker is
- A1 "we assume that a potential attacker is external to the private cloud and could exploit vulnerabilities present in IoT device operating systems to gain unauthorized access … The attacker's objective is to breach the database (DB) on host8, which stores critical IoT data." (§3.1, p. 5)
- A2 "Given its limited access solely to the database, V8 becomes a prime target for attackers and remains ineligible for migration". (§3, p. 5)
- A3 The attacker is a node in the graphs: V_hS = (attacker, V1, …, V8) and S_hS = (attacker, S1, …, S14), with edges (attacker, V1) and (attacker, V2). (Defs. 1–3, pp. 7–8)
- A4 An attack path ap is "a sequence of consecutive VMs in the cloud that extends from the entry node within the edge sets to the target node", and AP is "All possible cloud attack paths leading to the target node". (Table 3, p. 7)
- A5 The attacker's capability is a set of CVEs per OS (Table 1) and per service (Table 2), each with a CVSS base score, impact, exploitability and attack cost. (p. 6)
- A6 Large cloud: 400 VMs; "Attackers can exploit weaknesses in each VM, map out attack routes, and ultimately get access to the target node." (§4.5, p. 14)

### B. What is computed (Algorithm 2, p. 9)
- B1 Input: "All possible Edge sets G, considering time t_i edge-sets G_ti".
- B2 ASP_Vi = 1 − (∏(1 − E_v) + ∏(1 − E_s)), from CVSS exploitability. (Eq. 1)
- B3 "AP = all_simple_paths (G, S_s, T_r)"; for each ap and each V_i on it: R_vi (Eq. 2), AC_vi (Eq. 3), RoC_vi = R_vi / AC_vi (Eq. 4), and the centralities C, D, B (Eqs. 5–7).
- B4 RoA: "the ratio between how much an attack costs and the benefit it provides. A higher RoA number means that attackers are more likely to take advantage of weaknesses, which means they are more likely to launch attacks." (§3.5.4, p. 9)
- B5 "Key metrics like attack success probability, attack cost, and attack risk were automatically calculated at intervals". (§3.3, p. 7) Defense trigger interval: 10 min. (Table 4)
- B6 Table 3 (p. 7) defines no symbol for an attacker decision, state or memory.

### C. What the MTD does to it (the defender's side)
- C1 Algorithm 3 selects the VM to move: "V*_i = rank(arg max(C_vi, D_vi, B_vi))" (Eq. 8, p. 10). It ranks by centrality, not by RoA.
- C2 Shuffle removes and adds edges in U; diversity swaps the attack tree's OS; redundancy adds a VM with new vulnerabilities and edges. (Algorithm 3; §§3.6.2–3.6.5, pp. 10–11)
- C3 Algorithm 1 ends with "Interrupt adversary if necessary" (line 28, p. 8); Fig. 2 has an "Interrupt Adversary" box. These are the only steps that act on the adversary, and both are the defender's.
- C4 The defender lengthens "the easiest attack path for attackers looking to compromise the database … V2 → V7 → V8". (§3.6.2, p. 10)
- C5 Results are recomputed metrics: e.g. R_ap1 = 43.15, AC_ap1 = 166.5, RoC_ap1 = 0.259 after V5 migrates (§4.2, p. 13); Figs. 6–9 show metrics per VM, per path and over time.

### D. Time
- D1 "Periodic triggers initiate MTD processes, exclusively designed to be proactive without reactive considerations." (§3.2, p. 5)
- D2 THARM is indexed by network state at time t_i (Defs. 1–4). Each t_i's paths are recomputed from the attacker node. (Algorithm 2)

### E. The attacker as described, carried by no definition, algorithm or result
- E1 "A defense-adversary interaction model that evaluates how MTD strategies dynamically disrupt attacker workflows and force rescanning, credential reuse, and other adversarial efforts". (§1, p. 3)
- E2 "Attackers were modeled after techniques in the cyber kill chain and MITRE ATT&CK, mirroring real threats … Tests included widespread and focused attacks aiming to breach many or specific high-value hosts. Vulnerabilities were prioritized by return on attack, emphasizing those with greatest impact. Successful exploitation let adversaries control internals through command channels to connected devices … Service and operating system diversification modified configurations, forcing fresh scans and adaptation to new flaws." (§3.3, p. 7)
- E3 "attackers will be none the wiser about the hosts they previously discovered being invalid" (§3.2, p. 6); MTD nullifies "any information or progress obtained by an attacker in the current state" (§1, p. 2)
- E4 "the attacker has fewer incentives to target that particular IoT cloud configuration when RoC_s is low … a higher RoC_s means that the attacker is more likely to attempt the same attack again, given it was previously successful." (§4.2, p. 13)
- E5 "each of the subsequent MTD changes means that attackers will have to change their strategies" (§4.6, p. 15); "compelling them to continuously adapt" (§5, p. 15)
- E6 Threats "avoid or neutralize standard security defensive mechanisms, including firewalls and intrusion detection systems (IDSs)" (§1, p. 1); "A cyber resilience system supported by an intrusion defence system (IDS) is made more secure with MTD." (§3.6, p. 9) Neither puts an IDS in the model.
- E7 Future work names "assessment against sophisticated attacks". (§6, p. 16)

### Predicate tests (Appendix B rule)

| # | Predicate | Cell | Evidence | Strongest counter, answered | Call |
|---|---|---|---|---|---|
| 1 | B: pursues one multi-stage campaign toward its objective | yes | A1, A4: a multi-hop path from the entry VM to the database | — | strong |
| 1 | Q: over an extended period, until it reaches its objective, however many MTD deployments that takes | no | D2, B6: each t_i's paths are recomputed from the attacker node, and nothing carries over | E3 implies an attacker that keeps discovered hosts across a shuffle, but no symbol or step holds them | strong |
| 2 | B: after the foothold, uses different techniques for different objectives | no | A1, B3: one target T_r | E2 "widespread and focused attacks": two objectives at most, with no technique that differs and no parameter or result. Description only | strong |
| 3 | B: chooses among several sequences of techniques toward the same objective | no | B3: every simple path is enumerated and aggregated; C4: the "easiest" path is the defender's target | — | strong |
| 4 | B: chooses its next technique in response to an MTD disruption | no, if E counts as description; assumed, if it counts as assumption | B3, D2: paths are recomputed, nothing chooses; C3: the defender interrupts | **E1, E2, E5: "forcing fresh scans and adaptation to new flaws"** | **contentious** |
| 5 | B1: moves low and slow | no | No timing in the model | — | strong |
| 5 | B2: chooses techniques an IDS does not flag | no | No IDS in the model | E6 is general framing and the defender's IDS | strong |
| 6 | B: chooses techniques by weighing their cost against their benefit | no, if E counts as description; assumed, if it counts as assumption | B3, B4: RoA is computed as a metric; C1: the only selection ranks by centrality | **E2: "Vulnerabilities were prioritized by return on attack"; E4** | **contentious** |
| 6 | Q: for each technique | no | — | — | strong |
| 7 | B: keeps the patterns of past MTD deployments and uses them | no | B6, D2 | E3, E4 are about hosts found and past success, not MTD patterns | strong |
| 8 | B: predicts and leverages which mechanism deploys next, and when | no | C1–C3 are the defender's side | E3: the attacker is "none the wiser" | strong |

Mark: P ✗ ✗ ✗ ✗ ✗ ✗ ✗ if E counts as description. If E counts as assumption, rows 4 and 6 become P: P ✗ ✗ P ✗ P ✗ ✗, the marks before the predicate change.

### Findings for the thesis

Ruled 2026-10-12: Marc chose the **strict** reading, provided every elephant is acknowledged. Findings 1 and 2 are applied, and each contested cell's strongest counterpoint is quoted in Appendix B, Table B.2, with the test that decides it.
1. **The "assumed" cell needs a boundary** (Appendix B). Kim's assumed cell and the APT attacker model's each have a step the model takes:
   - Kim: the script opens the reverse shell, and its evasion is assumed.
   - APT attacker model: its attack profiles enter different tactics by objective, and the techniques inside the unmapped tactics are assumed.

   Masud's E has no step in the model at all. Proposed sentence for Appendix B, after the cell definitions: "An assumption counts only where the attacker model takes the behaviour's step and its authors assume what the model cannot show; a behaviour its authors describe, but no step of the model takes, is no." It moves no mark (Kim and the APT attacker model keep theirs).
2. **The Masud paragraph** should show that E was read. Proposed sentence after "no cost–benefit reasoning": "The paper also says its attackers prioritise vulnerabilities by RoA and adapt to new flaws \citep[p.~7]{masud2025}, but no step of the analytical model does either."
3. **Either reading leaves the APT attacker model's claims intact.** None of the three comparators has more than one property in full, and the gains over the baseline attacker do not involve Masud et al.
4. **The rest of the §3.3.2 Masud paragraph checks out** against A–D: the analytical model, the set of attack paths from the Internet to a target database, the metrics recomputed per interval before and after the MTD deploys, and every cross. One wording risk: the paper calls its evaluation "Experimental validation conducted in a simulated IoT environment" (p. 3). The thesis calls it an analytical model, which matches §3.2's definition (Algorithm 2 computes metrics; nothing is simulated), and B3 is the evidence if challenged.
