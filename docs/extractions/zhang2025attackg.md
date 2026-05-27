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

### Relevance class

**S — Supporting-argument.** AttacKG+ anchors the lit review's third automated-extraction strand (LLM-based) in §III-D alongside the NLP exemplar [[rahman2025]] (ChronoCTI), establishing what prompted-LLM pipelines bring to CTI structuring without driving a specific L0→L1 methodology choice in the architecture. The pipeline output (technique-tagged behaviour triplets, stage summaries) is adjacent to — not the same as — the dependency / sequencing / precondition structure L1 GAP construction consumes from Attack Flow `.afb` per [`../specs/architecture.md`](../specs/architecture.md) §(c)–(d), so the paper bounds rather than supplies L1 inputs.

### Used in lit review

- [`../sources/LIT_REVIEW.md:141`](../sources/LIT_REVIEW.md#L141) — cited as `[17]` to name AttacKG+ as the LLM-based exemplar of the three automated-extraction strands, with the appeal of "generalisation to unseen knowledge types without per-task training"; this is then qualified against the [[buechel2025sok]] SoK plateau finding (best generative / embedder systems near *F*1 = 0.70 on the 50 most common TTPs).
- [`../sources/LIT_REVIEW.md:283`](../sources/LIT_REVIEW.md#L283) — full reference entry for `[17]`.

### Four-module LLM pipeline (rewriter → parser → identifier → summariser)

**Source locator:** §1 (Introduction) and §4 (Approach), specifically §4.1–§4.4; framework overview Fig. 3. Source markdown is HTML-extracted with no page numbers; locators are by section heading.

**Paraphrase:** AttacKG+ is a fully automatic LLM-driven framework for constructing attack graphs from CTI reports, composed of four sequential modules each implemented through instruction prompting and in-context learning rather than supervised training. The *rewriter* (§4.2.1) ingests a raw CTI report and reorganises it by MITRE tactical phase, filtering redundant prose so downstream extraction works against pre-segmented, temporally ordered text. The *parser* (§4.2.2) extracts threat behaviour as ordered atomic-event triplets (subject, action, object) plus non-action entity–entity relations, with temporal edges between actions implied by their order in the rewritten text. The *identifier* (§4.3) matches the extracted behaviour against the MITRE TTP matrix to attach technique labels, exploiting the rewriter's tactical segmentation to bound the candidate technique set per stage. The *summariser* (§4.4) emits a per-stage state summary across four facets — permission state, file collection, sensitive information, tool set — capturing how the environment changes across tactical phases. The output is what the paper calls a three-layer attack-graph schema (behaviour graph, TTP labels, state summary) temporally aligned across stages.

**Quote (if essential):**
> "Leveraging LLMs for the attack graph construction, we propose a fully automatic framework with four modules: rewriter, parser, identifier, and summarize, each of which is implemented with dedicated prompt engineering and in-context learning based on LLMs." (§1)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 → L1 boundary (parser contract) · §(d) L1 GAP construction. The closest analogue to L1's input requirement is the *parser*'s triplet stream, but the paper's triplets are descriptive event tuples carrying temporal order; they do not encode the precondition / dependency structure (`AND`/`OR` operators, `effect` / `on_true` / `on_false` edges) that Attack Flow `.afb` exposes and that L1 GAP aggregation consumes. The state summary is orthogonal to GAP's edge-aggregation step.

**Disposition for this thesis:** *contrasted-against* the automated-extraction path. AttacKG+ exemplifies what the lit review's §III-D names as the LLM strand of automated profiling; this thesis instead takes the manual-curation path via the Attack Flow corpus (per §(c)), because the procedural-semantic gap identified at [`../sources/LIT_REVIEW.md:131`](../sources/LIT_REVIEW.md#L131) — the *sequencing, preconditions, dependencies* — is not what AttacKG+'s pipeline reconstructs. The pipeline architecture is recorded here so that any future move toward automated L0 → L1 extraction can be calibrated against the closest peer-reviewed exemplar rather than re-derived.

---

### Generalisation-to-unseen-knowledge-types claim and its evidence base

**Source locator:** §1 (Limitation 1 framing); §5.2.1 (RQ1 — threat behaviour graph extraction) and Table 2; §5.2.2 (RQ2 — technique identification).

**Paraphrase:** The paper frames its central appeal as overcoming the "limited generalisation capability to diverse knowledge types" of prior NLP / graph-matching extractors, on the argument that LLMs internalise broad open-domain knowledge during pre-training and can perform zero-shot extraction over unseen entity types and emerging threat vocabulary without per-task labelled data (§1, Limitation 1 + the LLM rebuttal that follows). Evidence is delivered as a head-to-head comparison on 15 manually-labelled APT CTI reports against EXTRACTOR (entity / relation extraction) and AttacKG (technique identification): on entities AttacKG+ reports overall F1 0.732 vs EXTRACTOR's 0.668; on relations 0.647 vs 0.601; on techniques 0.588 vs 0.545 against AttacKG (Table 2, "Overall" rows). The paper attributes the gain to LLMs' tolerance of noisy raw report text and ability to handle "emerging threat entities" that regular-expression-based or trained-graph-matching pipelines miss (§5.2.1 discussion of EXTRACTOR's false-negative drivers). The evaluation uses GLM-4 as the backbone LLM (§5.1) on 15 manually-annotated reports drawn from a 500-report corpus.

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 corpus boundary and §(k) validation strategy; calibrates against [[buechel2025sok]]'s open-set evaluation finding cited at [`../sources/LIT_REVIEW.md:141`](../sources/LIT_REVIEW.md#L141).

**Disposition for this thesis:** *contrasted-against*. The lit review at [`../sources/LIT_REVIEW.md:141-143`](../sources/LIT_REVIEW.md#L141) explicitly pairs this paper's claim with the [[buechel2025sok]] SoK's finding that, under realistic open-set evaluation, generative and embedder-based methods do not yet beat traditional NLP classifiers and plateau near *F*1 = 0.70 on the 50 most common TTPs. AttacKG+'s reported gains are on a 15-report manually-labelled sample comparing against two specific baselines (EXTRACTOR, AttacKG); the SoK evaluates more broadly. The two are not in direct conflict — the SoK is the wider statement — and the bound it implies on L1 automation is what the lit review uses both papers together to anchor. Per guardrail, this is recorded as a scope contrast (open-set TTP-level fidelity ceiling), not a claim that AttacKG+'s results are wrong on its own protocol.

---

## Open questions / things to verify

- Whether AttacKG+'s "emerging threat entity" handling extends to recovering the procedural-semantic structure (precondition / sequencing / dependency) identified as the open gap at [`../sources/LIT_REVIEW.md:131`](../sources/LIT_REVIEW.md#L131), or whether it only improves entity / relation recognition over text it already segments by tactic. The §4.2.2 parser description suggests the latter — temporal relation is "implied by a directed edge" inferred from order in the rewritten text — but the paper does not measure precondition / dependency recovery directly.
- Filename clash: this is `zhang2025attackg.md`, distinct from `zhang2023.md` (the MTDSimTime lineage paper). Different authors, different work.

## Out of scope for this thesis

- LLM-prompting engineering details beyond what's needed to assess transferability.
