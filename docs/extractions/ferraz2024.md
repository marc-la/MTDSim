# Ferraz 2024 — extraction notes

> Á. L. R. Ferraz, S. Barbieri, M. E. de Souza, L. A. Pereira Júnior. "The Procedural Semantics Gap in ATT&CK-in-STIX: Measuring Procedural Sufficiency for APT Emulation." Preprint (Aeronautics Institute of Technology / Carnegie Mellon University), 2025. Subsequently revised on arXiv as "The Procedural Semantics Gap in Structured CTI: A Measurement-Driven STIX Analysis for APT Emulation" (arXiv:2512.12078).
> Source file: `docs/sources/2_4_ferraz2024procedural.md` (gitignored).
> Relevance to this thesis: directly names the **procedural-semantics gap** in ATT&CK-in-STIX that the lit review §III-D centres on (CTI describes *what* but not *how*); provides empirical measurement of the gap (43.0% of techniques appear in at least one campaign; intrusion sets lack ordering/preconditions/environmental assumptions); presents a three-stage methodology that mirrors this dissertation's L0→L1→L2 reconstruction.

## Bibliographic anchor

- **Citation key**: `ferraz2024`
- **DOI / URL**: arXiv:2512.12078 (preprint, no DOI; arXiv handle `https://doi.org/10.48550/arXiv.2512.12078`). First arXiv post 12 December 2025; the source PDF in `docs/sources/` is an earlier draft with the original "ATT&CK-in-STIX" title and a 43.0% campaign-coverage figure, whereas arXiv v1+ uses the "Structured CTI" title and reports 35.6%. Flag for Marc: the citation key `ferraz2024` may need to become `ferraz2025` once Pass 2 settles which version is being cited.
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### TODO — Pass 2

(awaiting Pass-2 deep extraction)

Sections to lift in Pass 2:
- The procedural-semantics-gap definition — directly load-bearing for the lit review's §III-D framing.
- The 43.0% campaign-coverage finding and the LCS / clustering analysis.
- The three-stage methodology (structural CTI modelling → analyst-curated technique translation → workflow integration in Caldera). Compare against this dissertation's L0→L1→L2 pipeline.
- The ShadowRay / Soft Cell case studies as worked examples.
- The "procedural sufficiency boundary" framing — likely a key term to inherit.

---

## Open questions / things to verify

- This paper appears closer to the dissertation's own framing than any other in the corpus. Pass 2 should pay particular attention — there may be terminology to adopt directly.
- Whether the "procedural" rung in the lit review's fidelity descriptor (Table II construction) was named after this paper or independently.
- Caldera vs. MTDSim as the execution substrate — the dissertation chose MTDSim; Ferraz uses Caldera. Note the contrast.

## Out of scope for this thesis

- Caldera-specific implementation details.
