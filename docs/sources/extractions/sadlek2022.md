# Sadlek 2022 — extraction notes

> L. Sadlek, P. Čeleda, D. Tovarňák. "Current Challenges of Cyber Threat and Vulnerability Identification Using Public Enumerations." *The 17th International Conference on Availability, Reliability and Security* (ARES 2022), Vienna, Austria, August 23–26, 2022. ACM, 8 pp. doi:10.1145/3538969.3544458.
> Source file: `docs/sources/2_2_sadlek2022current.md` (gitignored).
> Relevance to this thesis: peer-reviewed corroboration of the Pyramid of Pain's ordering (lit review §III-B) — TTPs as "the most mature indicators used for the security defense"; IP-address validity decays within a day; behavioural patterns persist with operational habits.

## Bibliographic anchor

- **Citation key**: `sadlek2022`
- **DOI / URL**: `https://doi.org/10.1145/3538969.3544458`
- **Venue**: *The 17th International Conference on Availability, Reliability and Security* (ARES 2022), August 23–26, 2022, Vienna, Austria. ACM, New York, NY, USA, 8 pages.
- **Author order**: Lukáš Sadlek, Pavel Čeleda, Daniel Tovarňák — per the ACM Reference Format on source p. 1 and the "L. Sadlek et al." running header on p. 2. (The byline block at the top of the source PDF text renders Čeleda first; that is affiliation-block layout, not citation order.) The lit review's "Sadlek et al. [15]" at `docs/sources/LIT_REVIEW.md:116` matches the publisher's canonical short form.
- **Pages cited from**: p. 3 (TTP-maturity claim — quoted at lit review line 116). IP-decay locator within the paper still TODO for Pass 2.

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**S — Supporting-argument.** Sadlek 2022 anchors lit review §III-B's claim that the Pyramid of Pain's ordering — practitioner heuristic by origin — is corroborated in the peer-reviewed literature. It establishes a categorical distinction between disposable atomic indicators (low rungs) and behavioural TTPs (apex) but does not drive a methodology decision in the L0→L4 pipeline ([`../specs/architecture.md`](../specs/architecture.md) §(c)–(g)); the PoP ordering itself is load-bearing via [[bianco2013]], not via sadlek. Sadlek's role here is rhetorical: a peer-reviewed citation supporting the framing introduced via Bianco's blog post.

### Used in lit review

- [`../sources/LIT_REVIEW.md:116`](../sources/LIT_REVIEW.md) — §III-B (Pyramid of Pain), single paragraph. Two distinct citations: (a) `[15, p. 3]` carrying the direct quote "the most mature indicators used for the security defense"; (b) bare `[15]` carrying the IP-address-validity-decay claim ("decays within a day"). Both anchor the same paragraph's categorical-distinction argument — atomic indicators are short-lived, behavioural patterns at TTP rung persist.

### TTPs as the most mature defence indicators

**Source locator:** §2.2 "Position of Enumerations in Cyber Threat Intelligence" (running header p. 3; source markdown line 108). No native page numbers in the markdown-extracted PDF — locator is by §-heading.

**Paraphrase:** Sadlek et al. position CTI enumeration entries on a maturity axis, comparing two existing models — the Pyramid of Pain (PoP) [Bianco 2013] and the Detection Maturity Level (DML) model [Stillions 2014]. Both express the same idea: detection that operates on more abstract indicator classes is more mature, and harder for an adversary to evade. The PoP collapses DML's three apex tiers (procedures / techniques / tactics) into a single "TTPs" rung; otherwise the orderings agree (paper's Table 2). The paper concludes that TTPs sourced from frameworks such as MITRE ATT&CK represent the apex of this ordering.

**Quote (essential — this is the exact phrasing cited at lit review line 116):**
> "Tactics, techniques, and procedures (TTPs) that can be obtained, e.g., from MITRE ATT&CK, express the most mature indicators used for the security defense." — §2.2

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(j) (methodological positioning — PoP framing) · corroborates [[bianco2013]] PoP ordering.

**Disposition for this thesis:** **adopted-as-baseline** for the lit review's §III-B framing. The paper supplies a peer-reviewed citation point for what would otherwise rest on a single blog post (Bianco). No methodology consequence beyond reinforcing the choice of TTP-level adversary modelling — which the L1 Attack-Flow → L2 GASP build pipeline already commits to ([`../specs/architecture.md`](../specs/architecture.md) §(d)–(e)).

---

### IP-address validity decays quickly

**Source locator:** §4.2 "Maturity of Methods" (source markdown line 218). No native page numbers; § / heading only.

**Paraphrase:** In motivating why threat-identification research has moved away from low-level IOC correlation, Sadlek et al. observe that naive IOC matching is brittle because an attacker can change atomic indicators trivially — specifically, the validity of an IP address "quickly decreases after one day". The paper cites this empirical claim to Tounsi and Rais (the paper's ref [48], *Computers & Security* 2018), i.e., Sadlek is the channel, not the primary source. The lit review's `[15]` citation for "within a day" therefore inherits sadlek's framing of the underlying Tounsi-Rais measurement.

**Quote (kept short; exact phrasing matters because lit review echoes "within a day"):**
> "the validity of IP addresses quickly decreases after one day" — §4.2 (Sadlek's paraphrase of [48] Tounsi and Rais 2018)

**Maps to:** [`../sources/LIT_REVIEW.md:116`](../sources/LIT_REVIEW.md) §III-B, second sentence (IP-decay anchor).

**Disposition for this thesis:** **verified** for citation use — sadlek does make the claim in the form the lit review uses. Flagged for the open-questions block: the lit review attributes a measurement to sadlek that sadlek itself attributes to Tounsi-Rais. Acceptable as secondary citation; would be cleaner to cite Tounsi-Rais directly if the empirical magnitude becomes load-bearing anywhere downstream.

---

## Open questions / things to verify

- Sadlek's IP-decay claim is sourced from Tounsi and Rais 2018 (sadlek's ref [48], `Computers & Security` 72, pp. 212–233). The lit review currently cites sadlek as a channel rather than the primary measurement. Decide whether to (a) leave the secondary citation, (b) add a parenthetical "as reported by sadlek, drawing on Tounsi-Rais 2018", or (c) cite Tounsi-Rais directly. Low priority unless the magnitude ("within a day") gets used in a methodology-load-bearing way elsewhere — at present it functions rhetorically in §III-B and that is fine.
- Sadlek's Table 2 (DML ↔ PoP correspondence, source line 116–124) is potentially useful if the architecture spec ever needs to reference the DML model alongside the PoP. Not currently used; recording for findability.

## Out of scope for this thesis

- The broader CVE / CWE enumeration challenges discussed in the paper.
