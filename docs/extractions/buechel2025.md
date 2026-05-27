# Büchel 2025 — extraction notes

> M. Büchel, T. Paladini, S. Longari, M. Carminati, S. Zanero, H. Binyamini, G. Engelberg, D. Klein, G. Guizzardi, M. Caselli, A. Continella, M. van Steen, A. Peter, T. van Ede. "SoK: Automated TTP Extraction from CTI Reports – Are We There Yet?" *USENIX Security 2025*.
> Source file: `docs/sources/2_4_buechel2025sok.md` (gitignored).
> Relevance to this thesis: the Systematization of Knowledge whose finding — that generative and embedder-based methods do not yet beat traditional NLP classifiers in realistic open-set evaluation, plateauing near *F*1 = 0.70 even on the 50 most common TTPs — motivates this dissertation's *manual-curation* choice over automated extraction (lit review §III-D).

## Bibliographic anchor

- **Citation key**: `buechel2025sok`
- **DOI / URL**: https://www.usenix.org/conference/usenixsecurity25/presentation/buechel
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
- The open-set evaluation protocol — what counts as "realistic" in their framing.
- The *F*1 = 0.70 plateau on the top-50 TTPs.
- The categorisation of methods (traditional NLP / embedder-based / generative).
- The implications-for-practice section — which directly feeds the manual-vs-automated-curation argument.

---

## Open questions / things to verify

- Whether the SoK distinguishes single-TTP from multi-TTP / sequence-level extraction — the latter is what this dissertation actually needs.
- Whether any system in the SoK comes close to operational fidelity for sequence extraction (vs. flat technique-label classification).

## Out of scope for this thesis

- Detection-engineering downstream uses of extracted TTPs.
