# Rahman 2025 — extraction notes

> M. R. Rahman, B. Wroblewski, Q. Matthews, B. Morgan, T. Menzies, L. A. Williams. "Mining temporal attack patterns from cyberthreat intelligence reports." *Knowledge and Information Systems*, vol. 67, no. 10, pp. 8941–8981, 2025. doi:10.1007/s10115-025-02491-6. (The source PDF in `docs/sources/` carries a "TRANSACTION OF SOFTWARE ENGINEERING" running header from when the manuscript was under submission to IEEE TSE; the artefact was ultimately published in Springer KAIS — verified via CrossRef.)
> Source file: `docs/sources/2_4_rahman2024mining.md` (gitignored).
> Relevance to this thesis: the NLP-based extraction exemplar in lit review §III-D — **ChronoCTI** pipeline, applied to 713 CTI reports, mines 124 recurring temporal attack patterns; the [16] citation, surfacing chains such as phishing-then-macro that individual reports describe in isolation.

## Bibliographic anchor

- **Citation key**: `rahman2025` (renamed from the earlier `rahman2024` per Marc's confirmation — publication-year keys; the arXiv preprint year was 2024, but the Springer KAIS publication is 2025).
- **DOI / URL**: 10.1007/s10115-025-02491-6 (Springer *Knowledge and Information Systems*, vol. 67 no. 10, pp. 8941–8981, 2025; arXiv preprint `arXiv:2401.01883`, January 2024).
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**S — Supporting-argument.** Rahman is cited once in [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) (§III-D, line 139) as the NLP-based extraction *exemplar* in the automated-extraction taxonomy (NLP / process-mining / LLM). The citation anchors a coverage claim ("applied to 713 reports, mines 124 recurring temporal patterns") that feeds into the §III-D coverage-versus-fidelity contrast on which the thesis bases its choice of manual Attack Flow curation over automated extraction — it does not drive any architectural decision in [`../specs/architecture.md`](../specs/architecture.md) §(c)–(g).

### ChronoCTI pipeline and corpus-scale result

**Source locator:** §1 (Introduction, contributions list); §3 (Methodology, steps S1A–S2C); §4 (Findings on RQ1, S1B + S1D); §5 (Findings on RQ2). Source markdown is paginated by `TRANSACTION OF SOFTWARE ENGINEERING` running headers rather than numbered pages — locators are by §/step.

**Paraphrase:** ChronoCTI is a two-stage supervised pipeline. Stage S1 (technique classification) fine-tunes a RoBERTa language model on roughly three thousand cybersecurity web articles drawn from MITRE ATT&CK citations (the *CTI-Roberta* variant), then trains a multi-class multi-label text classifier on ATT&CK procedure examples — restricted to the 120 techniques with at least 20 training sentences out of ATT&CK v12.1's 193 techniques, evaluated at a 0.95 prediction threshold (highest F1 = 0.69 against held-out reports). Stage S2 (temporal-relation classification) trains a gradient-boosting classifier over 309 hand-engineered features per pair — temporal markers, TimeML annotations, sentence adjacency / similarity / coreference, discourse relations, and apriori association-rule features mined from ATT&CK's malware / group / campaign repositories. Applied to a curated corpus of 713 CTI reports (filtered from 1,301 ATT&CK citation URLs by inclusion / exclusion criteria), the pipeline identifies 124 unique temporal patterns across nine categories, with 718 instances; the most prevalent pattern (P1, "phishing BEFORE user execution") appears in 201 reports. Stage-S2 macro-F1 is 0.71 on cross-validation but 0.54 on the held-out evaluation set, with precision-favoured trade-off ("higher precision and lower recall" — §6, threats to validity).

**Quote (if essential):**
> "We apply **ChronoCTI** on a set of 713 CTI reports, where we identify 124 temporal attack patterns - which we categorize into nine pattern categories." (§Abstract)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 — Raw CTI (manual Attack Flow curation as the chosen alternative to NLP extraction) · [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §III-D ll. 135, 139, 141–143 (the NLP / PM / LLM trichotomy and the coverage-versus-fidelity disposition).

**Disposition for this thesis:** *contrasted-against* — adopted as a corroborating exemplar of what NLP-based extraction can deliver *at scale* (713 reports, 124 patterns), the coverage advantage [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §III-D credits automated extraction with. The thesis sits on the *other* side of the same trade-off: Attack Flow's analyst-curated structured graphs are taken as the L0 substrate precisely to inherit the fidelity that an extraction pipeline at this F1 ceiling does not yet guarantee (cf. [[buechel2025]] on the open-set-evaluation plateau near F1 = 0.70). ChronoCTI does not feed the L0 → L1 build; it bounds the counterfactual.

---

### Temporal-pattern definition — directed pairs, not sequences

**Source locator:** §2 (Key Concepts, "Temporal Relation between Attack Action" and "Temporal Attack Pattern"); Table 1 (relation definitions); §5 (RQ2 findings, opening paragraph).

**Paraphrase:** Rahman et al. specify a temporal *pattern* as a tuple `(Tx, Ty, τ)` — two ATT&CK techniques and one temporal relation drawn from `{BEFORE, SIMULTANEOUS-OVERLAP, CONCURRENT, NULL}`, derived from a five-relation reduction of TimeML v1.2.1's fourteen `TLINK` relations. The pattern threshold `n` is set to 2 reports in §5 (a pair counts as a pattern if it recurs across at least two of the 713 reports). The unit is a *directed pair* with an ordering relation, not a sequence — chains of three or more techniques are not explicitly mined; the 124-pattern result is 124 directed pairs categorised post-hoc into nine thematic groups (Tables 9–17). The worked example throughout the paper is `T1566: Phishing` BEFORE `T1204: User Execution` (Example 1; P1 in Table 9), recurring in 201 of the 713 reports.

**Quote (if essential):**
> "We refer to the pattern as a temporal attack pattern - the frequent occurrence of two techniques with a temporal relation." (§2, "Temporal Attack Pattern")

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 (the "what extracted CTI looks like" comparator) · [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §III-D l. 139 (the "phishing followed by macro execution" gloss the lit review uses for ChronoCTI's output).

**Disposition for this thesis:** *contrasted-against* — Attack Flow's `.afb` action / condition / operator / effect graphs ([`../specs/architecture.md`](../specs/architecture.md) §(c)) carry richer sequencing structure (multi-node chains, branching conditions, AND/OR operators) than a directed-pair pattern with one of four relation labels. Rahman's framing demonstrates that *temporal ordering is recoverable from CTI text*, validating the L0 corpus class as a viable source for behavioural structure; but the recovered structure is shallower than what the thesis's L1 GAP construction inherits from analyst-curated graphs. This is the §III-D coverage-versus-fidelity contrast made concrete at the artefact level.

---

### Used in lit review

- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §III-D, l. 139 — anchors the *NLP-based automated extraction* exemplar in the PM / NLP / LLM trichotomy; supplies the "713 reports → 124 patterns" coverage figure and the phishing-then-macro worked example that grounds the abstract claim in a concrete pattern.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) References, l. 281 — citation [16].

## Open questions / things to verify

- *Resolved inline:* whether ChronoCTI's "temporal patterns" rise to the level of operationalisable sequences for simulation — they do not. The unit is a directed pair `(Tx, Ty, τ)` with one of four relation labels, not a multi-step chain; the nine pattern *categories* in §5 are post-hoc thematic groupings of these pairs, not composed sequences. See the temporal-pattern definition artefact above.
- *Carried forward:* open-set vs. closed-set evaluation framing — ChronoCTI's S1 classifier discards 73 of ATT&CK v12.1's 193 techniques (those with fewer than 20 procedure examples) and reports F1 on the retained 120, which is a closed-set regime over a restricted vocabulary. Whether ChronoCTI's S1 numbers (F1 = 0.69 at the 0.95 threshold on held-out reports) sit above or below the SoK's ~0.70 plateau for the top-50 techniques is for the [[buechel2025]] extraction to settle — not this paper's source.
- *Carried forward, low priority:* κ inter-rater agreement on the temporal-relation ground truth is moderate (0.47–0.49 for BEFORE / CONCURRENT / SIMULTANEOUS-OVERLAP — §S2A); §6 (threats to validity) acknowledges the subjectivity of identifying temporal order in unstructured prose. If Attack Flow turns out to be too narrow at L0, the *upper bound* on what an NLP fallback could supply is bounded by this annotation reliability — not classifier F1 alone.

## Out of scope for this thesis

- The dataset curation methodology beyond what's needed to assess transferability.
