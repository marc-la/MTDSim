# Rahman 2024 — extraction notes

> M. R. Rahman, B. Wroblewski, Q. Matthews, B. Morgan, T. Menzies, L. Williams. "Mining Temporal Attack Patterns from Cyberthreat Intelligence Reports." *Transactions on Software Engineering*, 2024.
> Source file: `docs/sources/2_4_rahman2024mining.md` (gitignored).
> Relevance to this thesis: the NLP-based extraction exemplar in lit review §III-D — **ChronoCTI** pipeline, applied to 713 CTI reports, mines 124 recurring temporal attack patterns; the [16] citation, surfacing chains such as phishing-then-macro that individual reports describe in isolation.

## Bibliographic anchor

- **Citation key**: `rahman2024`
- **DOI / URL**: TODO — confirm exact TSE volume/issue and DOI
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
