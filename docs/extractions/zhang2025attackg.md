# Zhang 2025 (AttacKG+) — extraction notes

> Y. Zhang, T. Du, Y. Ma, X. Wang, Y. Xie, G. Yang, Y. Lu, E.-C. Chang. "AttacKG+: Boosting attack graph construction with Large Language Models." *Computers & Security*, vol. 150, art. 104220, 2025.
> Source file: `docs/sources/2_4_zhang2025attackg_.md` (gitignored).
> Relevance to this thesis: the LLM-based extraction exemplar in lit review §III-D (the [17] citation) — prompted-LLM stages replacing trained classifiers, with the appeal of generalisation to unseen knowledge types without per-task training; foil for the Büchel SoK plateau finding.

## Bibliographic anchor

- **Citation key**: `zhang2025attackg`
- **DOI / URL**: 10.1016/j.cose.2024.104220
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
- The LLM-stage pipeline architecture.
- The generalisation-to-unseen-knowledge-types claim and the evidence behind it.
- The model-design-/-tuning-cost reduction argument over traditional NLP pipelines.

---

## Open questions / things to verify

- How AttacKG+'s evaluation protocol compares against the open-set framing in Büchel 2025 [[buechel2025]] — is its reported performance comparable, or measured under a more favourable protocol?
- Filename clash: this is `zhang2025attackg.md`, distinct from `zhang2023.md` (the MTDSimTime lineage paper). Different authors, different work.

## Out of scope for this thesis

- LLM-prompting engineering details beyond what's needed to assess transferability.
