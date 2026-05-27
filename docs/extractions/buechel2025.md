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

### Relevance class

**S — Supporting-argument.** Büchel 2025 anchors the lit review's evidentiary basis for choosing manually-curated CTI (Attack Flow) over automated TTP extraction as the L0 input to the L1 GAP pipeline ([`../specs/architecture.md`](../specs/architecture.md) §(c)). It does not drive an architectural choice — the manual-curation direction is already fixed by the Attack Flow substrate decision — but it *justifies* that choice empirically: the SoK is the citable demonstration that automation is not yet a viable alternative at the fidelity this thesis needs.

### Open-set plateau on the top-50 TTPs

**Source locator:** §1 Key insights (item 1); §7 Overall Comparison; §9 Conclusion and Takeaways

**Paraphrase:** Across three method families (NER, embedder-based classification, generative LLMs) evaluated on a unified protocol over the two best public datasets (TRAM2, AnnoCTR), no approach surpasses an *F*1-score of roughly 0.70 by more than a small margin — and that ceiling is reached only on the 50 most common ATT&CK techniques. When the label space expands toward the full ATT&CK Enterprise matrix (637 techniques) in their open-set scenario, precision collapses well below 40% (§1). The SoK frames this as a *performance limit existing approaches seemingly cannot overcome as of yet*, attributing it not to NLP innovation deficits but to dataset scarcity, class imbalance, ontology ambiguity (e.g., 31% inter-annotator agreement on AnnoCTR, §9 "Label confusion"), and the closed-set bias of the literature.

**Quote (essential — the headline plateau number):**
> "the most recent NLP models, such as generative LLMs, are unable to surpass the F1-Score bar set at 70% by less recent models (e.g., BERT-based text classifiers), by more than a small degree." (§9 Conclusion and Takeaways)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 corpus boundary — the rationale for pinning the L0 input to manually-curated Attack Flow rather than an automated extraction pipeline. Also relates to §(j) methodological positioning, where the manual-curation choice is part of the "behavioural fidelity changes the answer" stance.

**Disposition for this thesis:** *adopted-as-baseline* (the SoK's empirical finding is the citable warrant for the lit review's manual-vs-automated framing at [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 141; we adopt its conclusion, we do not replicate its experiments).

---

### Closed-set vs open-set evaluation protocol — the realism distinction

**Source locator:** §3 Empirical Analysis: Setup; §7 Overall Comparison (Table 12, Figure 4)

**Paraphrase:** The SoK distinguishes two evaluation regimes: a *closed-set scenario* in which the label space and dataset characteristics are known a priori and approaches can be tuned to them (the dominant pattern in prior work), versus an *open-set scenario* in which no prior information about the data is available and no per-approach adjustment is performed. The closed-set numbers — where generation reaches *F*1 ≈ 0.72 on TRAM2 (Table 12) — flatter the field; the open-set numbers, scanned across the top-{10,25,50,118,637} label subsets (Figure 4), are the SoK's pointed contribution and the basis for its "are we there yet?" answer of *not yet*. The framing matters because automated CTI extraction in a production threat-intelligence pipeline is structurally an open-set problem: the analyst does not get to pre-restrict the ontology to fifty techniques.

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) — argues that any future "swap in automated extraction at L0" branch would inherit open-set performance, not the closed-set headline numbers. Backs the §(j) note that the working methodology direction is calibrated against the dominant pattern's limitations.

**Disposition for this thesis:** *adopted-as-baseline* — the open-set framing is exactly the realism criterion the lit review §III-D appeals to when it says automated extraction "still falls short of reliable technique recovery in realistic settings" ([`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 221). Used rhetorically, not replicated.

---

### Used in lit review

Citations of `[14]` in [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md):

- **Line 135** — "Automated extraction dominates the literature [14] and spans three families: natural language processing (NLP), process mining (PM), and large language models (LLMs)." Gloss: the SoK is cited as the authoritative survey establishing that automated extraction is the dominant strand and decomposing it into the three method families the review then walks through.
- **Line 141** — "a recent Systematization of Knowledge (SoK) on TTP extraction finds that generative and embedder-based methods do not yet beat traditional NLP classifiers in realistic open-set evaluation: even on the 50 most common TTPs, the best systems plateau near *F*1 = 0.70 [14]." Gloss: the headline empirical finding — the *F*1 = 0.70 plateau and the counterintuitive ordering of traditional NLP over modern methods — is loaded directly from this paper.
- **Line 143** — "automated extraction holds the coverage advantage, but on the SoK's evidence it does not yet recover technique-level behaviour reliably enough to ground an adversary on" (implicit `[14]` reference via "the SoK"). Gloss: the SoK's evidence is the warrant for the comparative trade-off conclusion that motivates the manual-curation choice.
- **Line 221** (§IV-A Approach) — "automated extraction dominates the literature but still falls short of reliable technique recovery in realistic settings [14]". Gloss: the SoK is the citation that justifies the deliberate L0-input choice when the methodology is announced.

---

## Open questions / things to verify

- The SoK evaluates *sentence-level* (and one document-level) classification of TTP labels; it does not directly evaluate *sequence-level* / multi-TTP graph extraction (the equivalent of producing an Attack-Flow-style graph from a CTR). §6.2 "Document-Level" shows recall collapsing further at document granularity, which suggests sequence extraction would fare worse still, but this is not the SoK's framed claim. Worth verifying against AttacKG+ [[zhang2025attackg]] — the closest LLM-pipeline-to-graph exemplar — before quoting the SoK as evidence about *sequence* extraction quality rather than *label* classification quality.
- The SoK's "label confusion" finding (§9, e.g., T1547.001 vs T1112) hints that the ATT&CK ontology itself may be under-specified for unambiguous machine extraction. Whether this also affects manually-curated artefacts (Attack Flow analysts working from the same ontology) is not addressed by the SoK and is a question for the Attack Flow extraction stub, not this one.

## Out of scope for this thesis

- Detection-engineering downstream uses of extracted TTPs.
