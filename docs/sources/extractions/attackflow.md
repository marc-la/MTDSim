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

### Relevance class

**L — Load-bearing on methodology.** Attack Flow defines the L0 raw-CTI schema (action / condition / operator / effect nodes and edges) that the L1 GAP construction parses, and its analyst-curated corpus is the data substrate for the GAP. The architecture spec carries an explicit open decision (schema version pinning) on this source. [`../specs/architecture.md`](../specs/architecture.md) §(c) parser-contract block + §(d) GAP transformation; lit-review §III-A para 3–4 and §III-C, §III-D.

### Concept 1 — Action chaining via `effect_refs`: precondition semantics on directed edges

**Source locator:** §2 "Core Concepts — Action Objects"; §3 "Language Specification — Attack Action"; §3 "Effects".

**Paraphrase:** An `attack-action` represents one adversary technique execution (typically named by an ATT&CK `technique_id`). Actions point at downstream objects through an `effect_refs` list — the directed edge that joins one action to the next. The schema is explicit that this edge does not merely mean "happened before": the downstream object cannot execute until the upstream action completes successfully, because the upstream action produces the effect (state change, knowledge gained, code execution achieved) that the downstream action depends on. While an action is executing its effect is *indeterminate*; once concluded, effects evaluate as succeeded or failed. This is the precondition semantics that an ATT&CK-in-STIX export lacks, and the structural property the L1 GAP build pipeline consumes when it interprets `.afb` graphs as technique-to-technique dependencies rather than flat technique sets.

**Quote (if essential):**

> "An action connected to another action represents a **dependency**: the second action cannot execute until the first completes successfully. This is *not* merely 'one happened before another' — it models how an adversary uses one behavior to create the preconditions needed for the next." (§2 Action Objects)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) parser-contract (action nodes + `effect` edges); §(d) L1 GAP — edges = inter-technique dependencies inferred from the Attack Flow corpus.

**Disposition for this thesis:** adopted-as-baseline. The precondition semantics on `effect` edges is the property that makes Attack Flow load-bearing: it is what licenses the L1 step ("aggregate per-campaign Attack Flow graphs into a generalised technique-dependency graph") rather than merely reading flat technique sets out of ATT&CK-in-STIX.

---

### Concept 2 — Branching semantics: AND/OR operators, condition true/false branches

**Source locator:** §2 "Core Concepts — Operator Objects", "Success and Failure"; §3 "Attack Condition", "Attack Operator".

**Paraphrase:** Two SDO types encode logic over multiple paths. An `attack-operator` carries `operator: AND | OR` and an `effect_refs` list: under AND every incoming path must succeed for the operator to evaluate true; under OR a single succeeding incoming path is enough. An `attack-condition` carries a `description` of the state being evaluated plus separate `on_true_refs` and `on_false_refs` lists — exactly one branch fires, depending on the outcome. The condition's false-branch is what lets a flow model adversary recovery from a failed technique (the spec's example: spear-phishing fails, so the adversary falls back to password spraying), rather than collapsing to a happy-path tree. Operators and conditions can be chained directly to actions, to each other, or back to actions, and conditions can also be used as a flow-start placeholder when initial-access is unknown.

**Quote (if essential):**

> "**OR** — only one incoming path needs to succeed for the flow to continue. **AND** — all incoming paths must succeed for the flow to continue." (§2 Operator Objects)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) parser-contract (condition nodes; operator nodes `AND`/`OR`; `on_true` / `on_false` edges). §(d) L1 transformation acknowledges these as part of the input grammar that the GAP aggregation must collapse across campaigns.

**Disposition for this thesis:** unimplemented at the L1 stage as of 2026-05-27 — §(d) describes the GAP as nodes = ATT&CK techniques, edges = inter-technique dependencies, but does not commit on how AND/OR branching and condition true/false splits are aggregated across per-campaign graphs (one campaign's AND-joined preconditions versus another's OR-fallback). This is a known open consequence of the §(l) "L1 aggregation parameter choice" question rather than a divergence from the source. Recorded here so the GAP build pipeline, when it lands, can be checked against the four-node grammar (action / condition / operator / asset) rather than only the action-and-effect subset.

---

### Concept 3 — Analyst-curated example corpus: scope, quality bar, and data-substrate role

**Source locator:** §1 "Getting Started" ("corpus of example flows"); §4 "Quality Standards for Public Flows"; §5 "Mapping CTI Reports to ATT&CK Techniques"; §8 developer-CLI workflow (`corpus/*.json`, `corpus/*.afb`).

**Paraphrase:** CTID maintains a corpus of public flows reconstructed by analysts from CTI reports. The source establishes a minimum quality bar for submissions — at least ten actions with proper structure, and at least one credible source cited in metadata — and prescribes the mapping workflow: assess source quality (factors include first-hand access, currency, ability to separate facts from analytical assessments), order behaviours chronologically from Reconnaissance / Initial Access through to Impact, assign an ATT&CK technique per event, set the per-action `confidence` field to reflect source uncertainty. The §5 worked example walks through the MuddyWater flow at tactic resolution (Initial Access → Execution → C2 → Persistence → Impact), explicitly noting that multiple paths can be joined by OR/AND operators when the underlying CTI is ambiguous about which path was taken. The corpus is the substantive artefact the L1 pipeline consumes; the §3 language specification is the schema that artefact conforms to.

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 inputs ("MITRE Attack Flow corpus (per-campaign `.afb` graphs of action / condition / operator / effect nodes)"); §(d) L1 transformation inputs ("L0 corpus").

**Disposition for this thesis:** adopted-as-baseline as the L0 data substrate. The corpus's deliberate trade — analyst review for fidelity, at a coverage cost — is the position the lit review takes in §III-D (manual curation vs automated extraction families) and is what motivates GAP construction *across* campaigns rather than per-campaign replay. Fair-use note on dissertation reuse: the corpus is Apache-2.0; per-flow content is structured data, so reuse of structure (technique IDs and graph topology) is well-clear of the quote-budget issue that affects narrative source material. The §(l) open question of *which* corpus generation is parsed (v2.x in-tree under `notebooks/attack-flow/` vs v3.2.0 CTID release) is the gating decision for treating this artefact as fixed.

---

### Concept 4 — The Tesla 2018 cryptojacking flow as the corpus exemplar (lit-review Figure 2)

**Source locator:** §8 Developers — Library & Builder, CLI walkthroughs reference `corpus/tesla.json` across the GraphViz / Mermaid / Navigator-overlay rendering paths. The source markdown carries no node-level walkthrough of the Tesla flow itself — the flow is corpus content, not specification content.

**Paraphrase:** The CTID corpus ships a Tesla flow file (`tesla.json` / `.afb`) that the source markdown treats as a standard demonstration target for the CLI tools (validate / GraphViz / Mermaid / matrix overlay). The lit review (§III-A para 4) uses an excerpt of this flow as Figure 2 — the 2018 Tesla Kubernetes cryptojacking incident — to make concrete the abstract "actions joined by effect edges with AND/OR operators" claim from para 3: specifically, a three-input AND operator joining Deploy Container (T1610), Proxy (T1090), and Non-Standard Port (T1571) into Resource Hijacking (T1496). The schema mechanics that licence reading the figure (AND operator semantics; action nodes named by `technique_id`) are exactly Concepts 1 and 2 above; no fresh schema property is introduced. Fair-use boundary: per the lit review's Figure 2 caption, the figure is *adapted* from the example corpus and reproduces only the subset needed to demonstrate the AND-join; the full corpus flow contains additional supporting STIX objects (e.g., the shared Infrastructure node) joined by generic `related-to` rather than effect edges.

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 inputs (the corpus) → §(d) L1 GAP construction. The Tesla flow is the per-campaign `.afb` graph the parser-contract consumes in miniature.

**Disposition for this thesis:** verified — the lit review's Figure 2 framing of Attack Flow's discriminating structural property (preconditioned multi-input joins via AND operators) is consistent with the §2–§3 schema description in this source. Recorded here as the canonical illustration; no separate methodological commitment beyond Concepts 1–3.

---

### Used in lit review

- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 103 — anchors the claim that Attack Flow is the STIX 2.1 extension supplying the precondition / sequencing semantics that ATT&CK-in-STIX lacks (CTID, 2022).
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 105 — anchors the AND/OR operators + condition state + effect-edge precondition framing; provides the Tesla 2018 cryptojacking example (Figure 2) — three-input AND joining T1610, T1090, T1571 into T1496.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 107 — anchors the analyst-curated corpus as the data substrate for adversarial profiles, with the coverage / fidelity trade taken up in §III-D.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 110 — Figure 2 caption (Tesla Kubernetes cryptojacking flow, adapted from CTID corpus; legend covers edge conventions and the *†* speculation marker).
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 127 — anchors the claim that the Attack Flow project curates APT campaigns into structured records and that group toolchains / sequencing recur across operations, which is what makes the APT a tractable modelling target.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 135 — anchors the manual-curation exemplar in the §III-D coverage-vs-fidelity framing (analyst review for fidelity, at a pace and effort cost that limits coverage).
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 223 — anchors the synthesis claim in §V that the analyst-validated corpus trades coverage for the fidelity an adversarial profile requires.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) line 245 — Reference [5] (CTID, *Attack Flow*, v3.2.0, 2025).

---

## Open questions / things to verify

- **For Marc — schema version pinning depends on an architecture decision that has not yet landed.** [`../specs/architecture.md`](../specs/architecture.md) §(c) and §(l) flag the choice between Attack Flow v3.2.0 (the current CTID release, matching the extracted source) and the v2.x corpus that may live in-tree under `notebooks/attack-flow/` as an open build-time decision: the GAP construction depends on which `.afb` generation's fields (actions / conditions / operators / effect-edges) are parsed. Once §(c) pins a version, update the Bibliographic-anchor block above to cite that pinned version explicitly (and the matching schema URL under the CTID GitHub Pages site). Until then, this extraction inherits v3.2.0 from the source document only. **Refinement from Pass 2:** the four-node grammar (action / condition / operator / asset) appears stable across v2.x → v3.x; the load-bearing schema delta is more likely in the surrounding STIX extension-definition wrapper, the `.afb` builder file format, and any v2→v3 publisher CLI upgrade path (§8 documents `upgrade-v2` as a Builder CLI subcommand renaming originals to `.afb-v2`). The §(l) decision therefore turns less on "do action/effect/operator/condition exist" — they do in both — and more on which `.afb` format the parser reads, since the JSON-export end-state is the same.
- **In-tree corpus + parser entrypoint.** §(c) records `find . -type d -name 'attack-flow*'` empty as of 2026-05-27, meaning neither the corpus checkout nor the `.afb` parser is materialised on this branch. This extraction cannot verify which version of the corpus the prior GAP code (referenced in §(d) "v0.4 implementation lives in an off-substrate workstream") actually consumed. Resolving the §(l) "Attack Flow schema version + parser entrypoint" question requires either locating the off-substrate workstream's parser or rebuilding it against the CTID public corpus.
- Apache-2.0 implications for redistributing snippets of the analyst-curated corpus in the dissertation appendix. **Partial answer from Pass 2:** Apache-2.0 permits reuse including derivatives provided notice is preserved; the source explicitly carries the licence + CTID document numbers (CT0040, CT0122, 25-2036). Lit review's Figure 2 ("adapted from the MITRE/CTID example corpus") sits within this allowance. Remaining open item: whether the dissertation appendix should reproduce a complete flow (the full Tesla node list) or stick to excerpts — a stylistic / editorial choice rather than a licence one.

## Out of scope for this thesis

- Builder UI / authoring-tool details — interactive walkthroughs already culled from the extracted source.
