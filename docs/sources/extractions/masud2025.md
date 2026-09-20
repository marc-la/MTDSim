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
