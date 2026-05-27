# Attack Flow (CTID) — extraction notes

> MITRE Engenuity Center for Threat-Informed Defense (CTID). *Attack Flow* — language specification + analyst-curated corpus. v3.2.0 (some sub-pages still v3.0.0 at extraction time). 2022–2025. Licensed under Apache 2.0. Document numbers CT0040, CT0122, 25-2036.
> Source file: `docs/sources/2_1_attackflowdoc.md` (gitignored).
> Relevance to this thesis: the STIX 2.1 extension language that supplies the precondition/sequencing semantics missing from ATT&CK-in-STIX (lit review §III-A); supplies the analyst-curated corpus that is the **data substrate** for the adversarial profiles this dissertation builds.

## Bibliographic anchor

- **Citation key**: `ctid-attackflow`
- **DOI / URL**: https://center-for-threat-informed-defense.github.io/attack-flow/
- **Source-document version**: Attack Flow **v3.2.0** as declared in the frontmatter of [`../sources/2_1_attackflowdoc.md`](../sources/2_1_attackflowdoc.md) (some sub-pages still served v3.0.0 content at extraction time — noted inline in the source).
- **Schema version the thesis pins**: *pending architecture decision* — [`../specs/architecture.md`](../specs/architecture.md) §(c) records the Attack Flow schema version as an open build-time decision (v3.2.0 vs in-tree v2.x under `notebooks/attack-flow/`), and §(l) lists it under open architectural questions. Until that lands, this anchor cites the source document version (v3.2.0) and will be re-pinned once the architecture decision resolves. [`../specs/project_context.md`](../specs/project_context.md) does not currently carry an Attack Flow schema entry.
- **Pages cited from**: language specification (§3), usage-guide (§§4–5)

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### TODO — Pass 2

(awaiting Pass-2 deep extraction)

Sections to lift in Pass 2:
- *Effect* edges and their precondition semantics.
- AND / OR operators and condition nodes.
- The analyst-curated example corpus — coverage, structure, fair-use considerations for reuse.
- The 2018 Tesla cryptojacking flow used as Figure 2 in the lit review.
- Cross-link to architecture spec L0 (raw CTI) → L1 (GAP — nodes = ATT&CK techniques).

---

## Open questions / things to verify

- **For Marc — schema version pinning depends on an architecture decision that has not yet landed.** [`../specs/architecture.md`](../specs/architecture.md) §(c) and §(l) flag the choice between Attack Flow v3.2.0 (the current CTID release, matching the extracted source) and the v2.x corpus that may live in-tree under `notebooks/attack-flow/` as an open build-time decision: the GAP construction depends on which `.afb` generation's fields (actions / conditions / operators / effect-edges) are parsed. Once §(c) pins a version, update the Bibliographic-anchor block above to cite that pinned version explicitly (and the matching schema URL under the CTID GitHub Pages site). Until then, this extraction inherits v3.2.0 from the source document only.
- Apache-2.0 implications for redistributing snippets of the analyst-curated corpus in the dissertation appendix.

## Out of scope for this thesis

- Builder UI / authoring-tool details — interactive walkthroughs already culled from the extracted source.
