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

**C — contrast / adjacent.** Masud anchors the §IV-B Table II cross-section at the *scripted* rung of the fidelity descriptor and is one of the two papers that drive the "rhetoric-versus-execution gap" pattern that section diagnoses (the other being [[kim2026]]). It is contrasted-against, not adopted: the contribution this thesis takes from it is a *placement* on the fidelity ladder ([`../specs/architecture.md`](../specs/architecture.md) §(j), [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) L195) — not an orchestration primitive, metric definition, or substrate choice. (Note: Masud is also the *specified pole* exemplar in §II-C of the orchestration spectrum, but that placement is rhetorical scene-setting; the load-bearing use is the §IV-B Table II row.)

### Threat-model placement on the Table II fidelity descriptor

**Source locator:** §3.1 "Threat model" (lines 186–188); §3.3 experimental-validation paragraph (line 299); coexistence rules at §3.2 (line 192) and §3.3 (line 246). Locator format is §/heading plus markdown line number — the Elsevier-extracted markdown does not preserve PDF page numbers as inline anchors (the running header "Computers & Security 153 (2025) 104380" appears between sections without numbering).

**Paraphrase:** The threat model is specified in §3.1 as an external adversary attempting to reach the database on host8 by exploiting OS-level vulnerabilities in IoT devices, with hypervisor isolation between VMs assumed. The adversary's behavioural realisation is left to the experimental-validation paragraph (§3.3, L299), which states the attackers were "modeled after techniques in the cyber kill chain and MITRE ATT&CK" and that vulnerabilities were "prioritized by return on attack". In execution, however, the attacker is the path enumeration the security-metrics algorithm runs — `all_simple_paths(G, Ss, Tr)` over the 3-layer THARM (Algorithm 2, L414), producing ASP / AR / AC / RoA values aggregated across every simple path between source and target. There is no per-step decision agent, no runtime adaptation, and no technique-level behaviour beyond the CVE/CVSS-parameterised graph the algorithm traverses; the kill-chain framing names a vocabulary but does not enter the executed model. This is *scripted* fidelity in the §IV-B sense — a pre-coded traversal against specific CVEs — sitting one rung above the *parametric* placement of [[brown2023]] / [[tay2024]] / [[he2025]] and on the same rung as [[kim2026]].

**Quote (if essential):**
> "Attackers were modeled after techniques in the cyber kill chain and MITRE ATT&CK, mirroring real threats. ... Vulnerabilities were prioritized by return on attack, emphasizing those with greatest impact." (§3.3, L299)

**Maps to:** [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §IV-B "_3) Masud et al., 2025_" (L185) and Table II row (L205) · [`../specs/architecture.md`](../specs/architecture.md) §(j) "behavioural fidelity changes the answer" framing (L460–462)

**Disposition for this thesis:** **contrasted-against.** Masud occupies the row on the fidelity descriptor that this thesis's L2/L3 GASP→OGASP attacker design is built *up from*. The placement is *not* a deficiency — Masud's contribution is on the orchestration side (coexistence rules between IP-shuffle, OS-diversity, redundancy via a priority queue + suspension list, §3.2 L192 and Algorithm 1 L361–393), where the threat model functions as evaluation backdrop rather than the focus. Used in the lit review to ground the §IV-B claim that *across the cross-section* the threat model sits markedly below the rung the defence claims to operate at — the rhetoric-versus-execution gap that opens the space for this thesis. The §II-C "specified pole" use of Masud (orchestration as explicit conflict-resolution rules) is rhetorical scene-setting, not a primitive this work adopts — the lineage substrate inherits no orchestration logic from Masud.

---

### Used in lit review

- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) L85 — §II-C "specified pole" of the orchestration spectrum: priority queue + suspension list as the conflict-resolution mechanism; evaluation across attack risk, attack cost, and RoA. *Rhetorical scene-setting for the orchestration spectrum's specified end.*
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) L177 — §IV-B introduction: Masud listed as the "recent IoT-cloud orchestration" point of the five-paper cross-section.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) L185 — §IV-B per-paper justification: scripted-fidelity placement; the "modeled after techniques in the cyber kill chain and MITRE ATT&CK" quote ([11, p. 7]) carries the rhetoric-versus-execution gap.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) L205 — Table II row: Persistent ✗ · Adaptive ✗ · Stealthy ✗ · Incentive-aware ✗ · Fidelity scripted.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) L195 — §IV-B general observations: Masud cited alongside [[kim2026]] as clustering at *scripted* on the ladder; collectively anchors the "located asymmetry" framing this thesis takes up.

---

## Open questions / things to verify

- The lit review cites the kill-chain framing as `[11, p. 7]`. The source markdown does not expose page numbers inline; the quoted text sits at L299 immediately following Table 4. Verify against the PDF that the "p. 7" anchor in the lit review is correct, since the bibliographic anchor was settled but PDF-page-to-markdown-line is not.
- Whether the "vulnerabilities prioritized by return on attack" mention (§3.3, L299) corresponds to a single design-time ordering or to a per-step RoA evaluation. The Algorithm 2 / Eq. 4 formulation computes RoA as a static ratio of accumulated risk to accumulated cost over an attack path; there is no evidence of a runtime per-step prioritisation. Worth verifying against §4 results to be sure the *evaluation* doesn't enact a per-step RoA decision the algorithmic description omits.

## Out of scope for this thesis

- IoT-specific architecture details unless they bear on the orchestration logic.
