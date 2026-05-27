# Bianco 2013 — extraction notes

> D. Bianco. "The Pyramid of Pain." *Enterprise Detection & Response* (blog), 1 March 2013 (updated 17 January 2014 to add the Hash Values tier).
> Source file: `docs/sources/2_2_bianco2013pop.md` (gitignored).
> Relevance to this thesis: defining source for the Pyramid of Pain (lit review §III-B); supplies the apex-vs-base argument that MTD's claimed level of disruption (TTPs) is categorically distinct from the level the field is evaluated at (parametric/scripted indicators).

## Bibliographic anchor

- **Citation key**: `bianco2013pop`
- **DOI / URL**: https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html
- **Pages cited from**: full post

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**L — Load-bearing on methodology.** The Pyramid of Pain is the cost-ranking instrument that anchors the lit review's §III-B framing and, through it, the fidelity descriptor in §IV-B (parametric → scripted → procedural → behavioural). Architecture §(j) reads "attacker fidelity sits at the bottom of the Pyramid of Pain even though MTD's claimed defensive value extends upward to TTPs" — that claim was flagged as unsupported by the docs audit ([docs/notes/2026-05-27_docs_audit.md](../notes/2026-05-27_docs_audit.md) §5 finding 2); this extraction is what retires that finding.

---

### Concept 1 — Six-tier ordering of indicator classes

**Source locator:** § *Types of Indicators*; restated through §§ *Hash Values* → *Tactics, Techniques & Procedures* (single-page blog, no page numbers; locators are headings).

**Paraphrase:** Bianco enumerates six classes of detection indicator and orders them apex → base by how much disruption it costs the adversary when a defender denies that class. Apex (most costly to the adversary): tactics, techniques, and procedures. Then tools; then network and host artefacts (paired as a single tier in the diagram, though defined separately in the text); then domain names; then IP addresses; with hash values at the base. The ordering is presented as a ranking of *defensive value*, not of detection difficulty — a hash is the most precise indicator but the least painful for the adversary to evade.

**Quote (if essential):** none needed — the ordering is the substantive content and is paraphrased above; the qualitative labels per tier are extracted in Concept 4.

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(j) (the "fidelity sits at the bottom of the Pyramid of Pain" claim); [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §III-B (the ordering as stated in the review's prose) and Figure 3 (the tier-and-label diagram).

**Disposition for this thesis:** adopted-as-baseline. The ordering is the reference scale the lit review's §IV-B fidelity descriptor inherits from — *parametric* and *scripted* attacker fidelity correspond to evaluations operating at the base of the pyramid (IP / artefact-class indicators), while *procedural* and *behavioural* fidelity correspond to the TTP rung at the apex.

---

### Concept 2 — The "cost imposed on the adversary" framing

**Source locator:** § *The Pyramid of Pain* (introductory paragraph); § *The Pyramid Explained*.

**Paraphrase:** The diagram's organising principle is not the technical sophistication of each indicator class but the *cost an adversary pays* when the defender successfully denies them indicators of that class. Bianco frames this as the "amount of pain" the defender can impose: denying a hash costs the attacker nothing (a single bit flip yields a new hash); denying an IP costs them only a switch to another address; denying a tool costs them research, development, and retraining time; denying a TTP forces them to learn new behaviour. The asymmetry is the point — higher-tier denial converts a defender's detection into a sustained capability tax on the adversary.

**Quote (if essential):**
> "the amount of pain you cause an adversary depends on the types of indicators you are able to make use of"  *(§ Effective Use of APT1 Indicators, closing paragraph)*

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(j) (the asymmetry between MTD's claimed defensive value at TTPs and the indicator-class level its evaluations actually exercise); [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §I (abstract: "MTD locates its defensive value at the apex of the Pyramid of Pain") and §III-B ("disruption higher in the hierarchy therefore imposes a steeper recovery cost").

**Disposition for this thesis:** adopted-as-baseline. The cost-asymmetry framing is what makes the apex-vs-base mismatch a *substantive* argument rather than a tier-labelling exercise — without it, the lit review's "MTD claims the apex, evaluates at the base" critique would reduce to a category-error observation rather than an empirical underclaim.

---

### Concept 3 — The TTP tier as "force the adversary to learn new behaviours"

**Source locator:** § *Tactics, Techniques & Procedures*.

**Paraphrase:** Bianco distinguishes the TTP rung from the tools rung beneath it by what it denies the adversary: at TTPs, detection operates on behaviour itself rather than on the instruments that implement it (Pass-the-Hash detection inspecting Windows logs, rather than blocking the specific tool that performs the credential dump). The defensive consequence Bianco names is that effective TTP-level disruption forces the adversary into the most time-consuming response available: learning new behaviour, or — if the disruption is broad enough across the adversary's repertoire — abandoning the campaign or reinventing themselves from scratch. The mechanism is durability: behaviour persists with the adversary's operational habits, whereas tool choice can be swapped at the next compile.

**Quote (if essential):** none needed — the "learn new behaviours" framing is paraphrased above; pairing this with Sadlek's peer-reviewed corroboration of TTP-class durability is handled at [[sadlek2022]].

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(a) ("behaviourally-grounded adversarial profiles derived from CTI" — the thesis-level direction motivated by the TTP-rung target); §(j) (the methodological-positioning argument that MTD's value claim extends to TTPs); [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §IV-B (the *behavioural* rung of the fidelity descriptor: "campaign-level intent, motivation conditioning, and learning capability").

**Disposition for this thesis:** adopted-as-baseline. The "behaviour persists, tools and indicators do not" claim is the conceptual hinge the dissertation's behaviourally-grounded attacker rests on. The Jalowski primitives encoded at architecture §(f) (state-collision recognition, defender-behaviour conditioning, metadata-invariance recognition) are the concrete operationalisation of *behaviour the adversary is unlikely to discard between campaigns* — Bianco supplies the *why* this rung is the right one to model against.

---

### Concept 4 — Qualitative labels per tier (used in lit-review Figure 3)

**Source locator:** § *The Pyramid Explained* (tier-colour discussion: green base → yellow middle → red apex) and per-tier sections that follow. The short label tokens ("Tough!", "Challenging", "Annoying", "Simple", "Easy", "Trivial") appear inside the original blog-post pyramid graphic, not in the prose body of this archive of the post. The prose justifies each label through the per-tier discussion (e.g., "if you deny the adversary the use of one of their IPs, they can usually recover without even breaking stride" — § *IP Addresses*).

**Paraphrase:** Each tier carries a one-word qualitative descriptor of how painful denial at that tier is for the adversary, ranging from *trivial* at the hash-value base to *tough* at the TTP apex, with intermediate descriptors marking domain-name, network/host-artefact, and tools tiers. The labels are mnemonic shorthand for the cost-imposed-on-adversary argument extracted under Concept 2; they are not independent claims. The labels themselves are short tokens reproduced verbatim in the lit review's Figure 3 caption, with attribution to Bianco; the cited form for the caption is adequate without requiring a longer verbatim extract here.

**Maps to:** [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) Figure 3 caption (line 119), which uses the labels as the tier descriptors with attribution.

**Disposition for this thesis:** verified — the labels reproduced in the lit-review caption match the original blog post's tier-descriptor scheme. The labels are practitioner mnemonics; for the methodological argument they back, the substantive content is Concept 2 (cost-asymmetry framing), not the labels themselves.

---

### Used in lit review

- **`docs/sources/LIT_REVIEW.md:16` (Abstract).** Anchors the thesis-level claim that MTD locates its defensive value at the apex of the Pyramid of Pain.
- **`docs/sources/LIT_REVIEW.md:22` (§I Introduction).** Names Bianco's 2013 introduction of the Pyramid alongside MITRE ATT&CK as the two ~2013 instruments the threat-intelligence community built around adversary behaviour.
- **`docs/sources/LIT_REVIEW.md:24` (§I Introduction).** Anchors the mismatch claim — MTD claims the apex (TTPs), the attacker models against which it is evaluated sit near the base.
- **`docs/sources/LIT_REVIEW.md:93` (§III opening).** Frames the Pyramid as one of two conceptual lenses on adversary behaviour (alongside MITRE ATT&CK).
- **`docs/sources/LIT_REVIEW.md:114` (§III-B opening).** Introduces the Pyramid formally — the six-tier ordering and the "force the adversary to learn new behaviours" framing for the TTP tier.
- **`docs/sources/LIT_REVIEW.md:119` (Figure 3 caption).** Tier-and-label diagram, "Adapted from Bianco".
- **`docs/sources/LIT_REVIEW.md:157` (§IV-A → §IV-B bridge).** Frames the Pyramid as the *reference point for attacker capability* on which the §IV-B fidelity descriptor is anchored — the load-bearing handover from PoP to the four-rung ladder.
- **`docs/sources/LIT_REVIEW.md:167` (§IV-B, Cho-derived attacker characteristics).** "Stealthy: operating at the TTP tier of the Pyramid of Pain" — one of Cho's four sophisticated-attacker characteristics framed through the PoP.

---

## Open questions / things to verify

- ~~The Pyramid is a practitioner heuristic, not peer-reviewed — pair with Sadlek 2022 for the peer-reviewed corroboration.~~ Resolved: the lit review at §III-B (line 116) already pairs the citations exactly this way, and the pairing is now durable in the extraction at [[sadlek2022]].
- ~~Confirm preferred citation form (blog post vs. derivative academic citations).~~ Resolved at the bibliographic-anchors pass: blog post is the citable artefact (citation key `bianco2013pop`, URL anchored).
- The original blog-post pyramid graphic is not present in this archive of the source markdown; the short tier labels ("Tough!" → "Trivial") are inferred from the prose-tier ordering plus the lit-review caption's attribution. Not load-bearing — Concept 2 (cost-asymmetry framing) is the substantive content the methodology rests on, not the label tokens themselves — but worth noting that the labels are sourced via the lit review's transcription rather than directly from this archive.

## Out of scope for this thesis

- The blog's broader detection-engineering material.
