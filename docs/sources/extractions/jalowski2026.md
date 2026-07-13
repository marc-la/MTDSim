# Jalowski 2026 — extraction notes

> Ł. Jalowski, M. Zmuda, M. Rawski, P. Rekosz. "Rethinking the Security Assurances of MTD: A Gap Analysis for Network Defense." *Future Internet*, vol. 18, no. 2, art. 89, 2026.
> Source file: `docs/sources/3_1_jalowski2026rethinking.md` (gitignored).
> Relevance to this thesis: second of the two surveys naming the attacker-modelling gap (lit review §IV-A) — names the attacker model "the most glaring flaw in the MTD literature"; critiques Nmap-style active-scanning baselines as too naive for APT; prescribes an attacker that reasons about the MTD scheme itself.

## Bibliographic anchor

- **Citation key**: `jalowski2026`
- **DOI / URL**: `10.3390/fi18020089` (MDPI, open access CC-BY; published 7 February 2026)
- **Pages cited from**: full text (esp. p. 8 — the "most glaring flaw" quote)

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**L — load-bearing on methodology.** Three artefacts here (state-collision recognition, mutation-frequency-as-beacon, metadata-shadow invariance) are the source primitives that [`../specs/architecture.md`](../specs/architecture.md) §(f) labels "Jalowski et al.'s three attacker-model primitives" and treats as the operationalisation of *behaviourally-grounded* at L3 OGASP. A fourth artefact (the §4.3 attacker-model gap and the active-vs-passive recon corrective) anchors the lit review's §IV-A diagnostic frame. The paper's primitives are inputs the L3 attacker module is being designed to encode (or explicitly defer); the disposition of each primitive feeds §(l) open question #2 ("which Jalowski primitives does the attacker model encode").

### State-collision vulnerability — finite parameter spaces guarantee post-shuffle state repetition

**Source locator:** §4.1 *Key MTD Design Principles: The Entropy and Complexity Paradoxes*, p. 6 (labelled "6 of 13").

**Paraphrase:** Jalowski et al. argue that *what to move* is not a tactical choice but a strategic determination of the system's available randomness. They distinguish *infinite* parameter spaces (e.g., IPv6 address pool) from *finite* "exotic" mutations (e.g., OS versions, software stacks). The latter operate within an inherently narrow space, so as the number of protected nodes grows a small parameter space guarantees state repetition. The consequence they name is not a performance issue but a security flaw: if an attacker compromises one state, the probability another node sits in the same state is high. Low-entropy MTD therefore does not "move" the target, it rotates it within a predictable set of vulnerabilities.

**Quote (essential):**
> "This leads to the state collision vulnerability: as the number of protected nodes increases, a small parameter space guarantees state repetition. ... If an attacker compromises one state, the probability that another node resides in that same state is high. Consequently, low-entropy MTD schemes do not truly 'move' the target; they merely rotate it within a predictable set of vulnerabilities." (§4.1, p. 6)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(f) decision-block primitive 1 (*state-collision recognition / cross-target memory*); [`../specs/architecture.md`](../specs/architecture.md) §(l) open question #2.

**Disposition for this thesis:** *pending encoding.* §(f) records primitive 1 as a candidate attacker capability — does the L3 attacker maintain a memory of compromised configurations across the target population and recognise post-shuffle state collisions? Jalowski et al. supply the threat justification (low-entropy spaces *will* collide on cross-target observation); this work has not yet committed to whether OGASP encodes that recognition. Promotion from *pending* to *encoded* would change the L3 attacker state space (cross-target memory becomes part of the attacker observation) but not the L1/L2 graph construction.

---

### MTD-event-as-beacon — host-specific mutation frequency signals asset value

**Source locator:** §4.1, p. 7 (labelled "7 of 13"), Figure 2.

**Paraphrase:** Examining *when to move*, Jalowski et al. note that the hybrid scheme — combining timer-based and event-based mutation, with mutation frequency tuned per host — is likely the strongest. But they identify a critical predictability risk: assigning higher mutation frequencies to critical "Red Zones" inadvertently signals asset value to an observer. An intelligent attacker performing traffic analysis can identify which segments are mutating fastest and thereby identify the most valuable data, turning the defence mechanism itself into a beacon for high-value targets.

**Quote (essential):**
> "As illustrated in Figure 2, assigning higher mutation frequencies to critical 'Red Zones' inadvertently signals asset value to an observer. An intelligent attacker can utilize traffic analysis to identify which segments are mutating fastest, thereby identifying the organization's most valuable data. This creates a side-channel where the defense mechanism itself acts as a beacon for high-value targets..." (§4.1, p. 7)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(f) decision-block primitive 2 (*defender-behaviour conditioning / MTD-event-as-beacon*); the inverse positioning against Tay's IDS-sensitivity sweep noted at §(f) end-of-section ("Tay-IDS ↔ Jalowski-beacon inverse").

**Disposition for this thesis:** *pending encoding.* §(f) records primitive 2 as a candidate capability — does the attacker condition action selection on observed defender frequency, treating MTD events as a target-criticality signal? Jalowski et al. supply the justification by side-channel argument (defender-rate observability is sufficient to localise high-value zones). If encoded, this is the natural inverse-positioning move against Tay's IDS-sensitivity experiment — where Tay varies what the *defender* observes about the attacker, primitive 2 varies what the *attacker* infers from the *defender*'s behaviour.

---

### Metadata shadow — side-channel invariants that survive mutation

**Source locator:** §4.1, p. 7.

**Paraphrase:** Network metadata is a persistent and (Jalowski et al. argue) insufficiently recognised gap in MTD design. They observe that metadata can yield information ranging from population estimation to detection of cryptomining. Despite the existence of metadata-preserving algorithms and traffic-analysis resistance research, many MTD schemes carry wrongful assumptions about state isolation: an attentive attacker may observe unusual protocol properties or timing patterns as side-channels that remain *invariant* across mutations. Without addressing this "metadata shadow", address mutation provides only a facade of security. The argument is extended by reference to Forward Secrecy and Backwards Secrecy: any mathematical correlation between MTD states lets a skilled attacker predict future movements or decipher past communications.

**Quote (essential):**
> "If an attacker is intelligent and attentive, unusual protocol properties or timing patterns may emerge as side-channels that remain invariant across mutations. Without addressing this 'metadata shadow,' address mutation provides only a facade of security." (§4.1, p. 7)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(f) decision-block primitive 3 (*side-channel / metadata-invariance recognition*).

**Disposition for this thesis:** *pending encoding, likely out-of-scope for the encoded subset.* §(f) records primitive 3 as the third candidate — does the attacker's observation include invariant-feature extraction from network metadata (what does *not* change when the attack surface does), or is observation CVE/CVSS-only? Jalowski et al.'s framing is general (any timing or protocol-level invariant counts). The substrate's observation model is CVE/CVSS-driven (per [`../specs/mtdsim_spec.md`](../specs/mtdsim_spec.md)); encoding metadata invariance would require extending the substrate's attacker-observation surface, which is a larger seam-change than primitives 1–2. Flagging as `unimplemented` is the likely disposition; the §(l) open question pins which subset is finally encoded.

---

### The attacker-model gap — "most glaring flaw" and the passive-reconnaissance corrective

**Source locator:** §4.3 *Threat Modeling: Deconstructing Attacker Assumptions*, p. 8 (labelled "8 of 13"); also §5 *Discussion*, p. 8–9.

**Paraphrase:** Jalowski et al. open §4.3 by naming the attacker model "the most glaring flaw in the MTD literature": existing models are too simplistic or based on unrealistic assumptions. Two specific critiques follow. First, MTD effectiveness is location-dependent (Figure 3): three attacker positions are distinguished — Attacker A (external eavesdropper reading outbound traffic), Attacker B (between endpoints and router), and Attacker C (privilege escalation on an endpoint). MTD may defeat A but has no effect on C, and given that phishing and stolen credentials remain primary vectors, this "Insider Threat Gap" is a critical shortcoming. Second, testing against active scanning (Nmap) is too naive: Advanced Persistent Threats utilise passive reconnaissance to remain hidden and learn mutation patterns over time. The prescribed corrective is to shift research toward defending against *smart, adaptive attackers who understand the MTD scheme and look for the mathematical logic behind the movement*. §5 sharpens this against the Attack Success Probability (ASP) metric: ASP is commonly calculated using simple Nmap scans as a baseline, an issue the paper has already flagged.

**Quote (essential):**
> "The most glaring flaw in the MTD literature is the ill-defined attacker models, which are often too simplistic or based on completely unrealistic assumptions." (§4.3, p. 8)

> "Furthermore, testing against active scanning (Nmap) is too naive. Advanced Persistent Threats (APTs) utilize Passive Reconnaissance to remain in the shadows and learn mutation patterns over time. To move forward, research must shift toward defending against smart, adaptive attackers who understand the MTD scheme and look for the mathematical logic behind the movement." (§4.3, p. 8)

**Maps to:** [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §IV-A (line 155 — the "most glaring flaw" citation and the passive-recon / MTD-scheme-aware corrective); [`../specs/architecture.md`](../specs/architecture.md) §(a) RQ framing (the *behaviourally-grounded* qualifier inherits the "understands the MTD scheme" framing); §(j) methodological positioning (the dominant-pattern critique aligns with the Pyramid-of-Pain mismatch noted in [`../specs/architecture.md`](../specs/architecture.md) §(j) Pass-1 paragraph 1).

**Disposition for this thesis:** *adopted-as-baseline (diagnostic frame), with one explicit divergence.* The diagnostic frame — attacker model is the most glaring gap, Nmap-style scanning is too naive, the corrective is an attacker that reasons about the MTD scheme — is adopted as the lit-review's §IV-A anchor and aligns directly with this work's RQ. The location-dependent Insider Threat Gap (Attacker A/B/C) is `contrasted-against` rather than adopted: this work's behaviourally-grounded attacker corresponds approximately to a network-positioned (post-recon) adversary on the substrate, not to an endpoint-privileged insider; Jalowski et al.'s point that an insider defeats MTD outright is acknowledged but is out-of-scope per [`../specs/architecture.md`](../specs/architecture.md) §(a) (existing-MTD evaluation, not insider-threat defence).

### Used in lit review

- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) **§IV-A, line 151** — "Two MTD surveys, six years apart, identify attacker-model under-development as a primary limitation of the field. Cho et al. document it in 2020; Jalowski et al. document it again in 2026." Anchors the structural-not-incidental framing of the attacker-modelling gap.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) **§IV-A, line 155** — the "most glaring flaw" citation, the Nmap-too-naive critique, and the passive-recon + MTD-scheme-aware corrective. This sentence is the paper's load-bearing contribution to the lit review's diagnostic frame.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) **References §, line 247** — entry [6] (bibliographic anchor only; not a content citation).

---

## Open questions / things to verify

- **Encoded subset of the three §4.1 primitives** (state-collision recognition, MTD-event-as-beacon, metadata-shadow invariance). This is the open question recorded at [`../specs/architecture.md`](../specs/architecture.md) §(l) item #2 and the §(f) decision block. This extraction narrows the question by stating each primitive's source justification and disposition; promotion of any one primitive from *pending* to *encoded* or *out of scope* belongs to the architecture handoff, not here.
- **Jalowski et al.'s Attacker C (endpoint-privileged insider) and the substrate.** §4.3 treats privilege-escalation-on-endpoint as defeating MTD outright. This work's behaviourally-grounded attacker sits at the network-positioned (post-recon, pre-domain-compromise) level on the substrate — verify in Pass 2 of [`../specs/architecture.md`](../specs/architecture.md) §(j) whether the position is stated explicitly enough to forestall a reviewer reading the contribution as ignoring Attacker C.
- **Section 5 ASP critique.** §5 frames ASP-with-Nmap-baseline as a measurement problem distinct from the attacker-model problem (though related). This work uses internal MTTC, not ASP, as the primary discriminator ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md); [`../specs/architecture.md`](../specs/architecture.md) §(g) Decision). Worth confirming in §(j) Pass-2 that the Nmap-baseline critique transfers cleanly from "ASP is naive" to "the attacker-fidelity ladder needs to sit above scripted CVE traversal".

## Out of scope for this thesis

- §2.1 MTD taxonomy (*what / when / how to move*) — restated background, already established elsewhere in the lit review.
- §2.2 Attack Surface — definition restatement.
- §2.3 Security metrics taxonomy — Sengupta et al. and Cho et al. grouping summaries; this work uses metrics defined in [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md), not the survey's reported grouping.
- §3.1 Standardisation-and-comparison gap — relevant context but not load-bearing on this work's RQ (which is comparative within a single substrate, not cross-technique standardisation).
- §3.3 Architectural-and-domain-specific gap (Cloud / SDN / CDN imbalance) — out of scope; the substrate is generic-network, not cloud or SDN-specific.
- §4.1 Forward Secrecy / Backwards Secrecy / Security-by-obscurity sub-points and §4.1 controller-as-single-point-of-failure observation — design-principle critiques unrelated to attacker modelling.
- §4.2 Deployment / Operational Friction (configuration, reconfiguration, retirement, protocol coexistence, QoS) — operational concerns; out of scope for this thesis's simulation-based evaluation.
- §5 pentesters / ethical-hackers research-direction recommendation — methodological suggestion not adopted here.
- §5 attackers-using-MTD direction (DDoS / C&C address mutation) — out of scope; this work studies MTD as a defence, not as an attacker tool.
