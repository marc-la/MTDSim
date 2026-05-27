# Rahman 2024 — extraction notes

> M. R. Rahman, B. Wroblewski, Q. Matthews, B. Morgan, T. Menzies, L. A. Williams. "Mining temporal attack patterns from cyberthreat intelligence reports." *Knowledge and Information Systems*, vol. 67, no. 10, pp. 8941–8981, 2025. (The source PDF in `docs/sources/` carries an arXiv-era "TRANSACTION OF SOFTWARE ENGINEERING" running header from when the manuscript was under submission; the artefact was ultimately published in Springer KAIS.)
> Source file: `docs/sources/2_4_rahman2024mining.md` (gitignored).
> Relevance to this thesis: the NLP-based extraction exemplar in lit review §III-D — **ChronoCTI** pipeline, applied to 713 CTI reports, mines 124 recurring temporal attack patterns; the [16] citation, surfacing chains such as phishing-then-macro that individual reports describe in isolation.

## Bibliographic anchor

- **Citation key**: `rahman2024`
- **DOI / URL**: 10.1007/s10115-025-02491-6 (Springer *Knowledge and Information Systems*, vol. 67 no. 10, pp. 8941–8981, 2025; arXiv preprint `arXiv:2401.01883`, January 2024). Flag for Marc: the citation key `rahman2024` reflects the arXiv-preprint year; if the dissertation prefers publication-year keys this should become `rahman2025`. The source-PDF "TRANSACTION OF SOFTWARE ENGINEERING" header reflects the manuscript's earlier submission target, not the final venue.
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
- The ChronoCTI pipeline architecture (domain-fine-tuned LM + supervised classifier).
- The 713-report corpus and the 124 patterns / 9 categories result.
- The temporal-pattern definition — what "temporal" actually means in their framing (vs. flat technique co-occurrence).
- The phishing→macro pattern as a worked example.

---

## Open questions / things to verify

- Whether ChronoCTI's "temporal patterns" rise to the level of operationalisable sequences for simulation, or remain co-occurrence-with-direction.
- Open-set vs. closed-set evaluation framing — relate to Büchel 2025 SoK [[buechel2025]] findings.

## Out of scope for this thesis

- The dataset curation methodology beyond what's needed to assess transferability.
