# Ferraz 2025 — extraction notes

> Á. L. R. Ferraz, S. Barbieri, M. E. de Souza, L. A. Pereira Júnior. "The Procedural Semantics Gap in Structured CTI: A Measurement-Driven STIX Analysis for APT Emulation." Preprint, arXiv:2512.12078, December 2025 (current v3, May 2026). Aeronautics Institute of Technology / Carnegie Mellon University. (The source PDF in `docs/sources/` is an earlier draft titled "The Procedural Semantics Gap in ATT&CK-in-STIX: Measuring Procedural Sufficiency for APT Emulation" — same paper, retitled on arXiv between source extraction and v1 submission.)
> Source file: `docs/sources/2_4_ferraz2024procedural.md` (gitignored).
> Relevance to this thesis: directly names the **procedural-semantics gap** in ATT&CK-in-STIX that the lit review §III-D centres on (CTI describes *what* but not *how*); provides empirical measurement of the gap (43.0% of techniques appear in at least one campaign; intrusion sets lack ordering/preconditions/environmental assumptions); presents a three-stage methodology that mirrors this dissertation's L0→L1→L2 reconstruction.

## Bibliographic anchor

- **Citation key**: `ferraz2025` (renamed from the earlier `ferraz2024` per Marc's confirmation — first arXiv post 12 December 2025, so the publication-year key is 2025, not the filename year).
- **DOI / URL**: arXiv:2512.12078 (preprint, no DOI; arXiv handle `https://doi.org/10.48550/arXiv.2512.12078`). The source PDF in `docs/sources/` is an earlier draft with the original "ATT&CK-in-STIX" title and a 43.0% campaign-coverage figure, whereas arXiv v1+ uses the "Structured CTI" title and reports 35.6%. Pass 2 will need to anchor on a specific arXiv version (current v3, 6 May 2026) and reconcile any quoted figures against the source PDF's earlier draft.
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**L — Load-bearing on methodology.** Ferraz supplies the *procedural-semantics gap* framing and the *procedural-sufficiency boundary* terminology that LIT_REVIEW.md §III-A and §III-D depend on (lines 101, 103, 131), and the paper's three-stage pipeline (structural modelling → technique translation → emulation integration) is the closest published analogue to this dissertation's L0→L1→L2→L3 staging — directly informing how the architecture §(c)–(f) seam is positioned. The C-class boundary against this paper sits at one point only (Caldera vs MTDSim as execution substrate); the framing layer above the substrate is load-bearing.

### Procedural-semantics gap — the *what* vs *how* asymmetry in ATT&CK-in-STIX

**Source locator:** §1 Introduction (Abstract + Contributions); §2 Background, paras 2–5; §6 Behavioural Analysis (synthesis bullets); §11 Conclusion.

**Paraphrase:** Public ATT&CK-in-STIX bundles are constructed as a descriptive knowledge base of adversary behaviour: campaign and intrusion-set objects record *which* techniques an adversary used, but the STIX object model has no dedicated procedure type and the existing object types (`attack-pattern`, `campaign`, `intrusion-set`, `relationship`, etc.) do not encode temporal ordering, prerequisites, environmental constraints, branching logic, or parameter flows. Where any of those live, they live in natural-language description fields, not in machine-readable structure. Ferraz names this the *procedural-semantics gap*: structured CTI tells you *what* an adversary does but not enough of *how* to automate it. The gap is presented as a structural property of the standard, not a quality complaint about any particular feed.

**Quote (if essential):**
> "public Cyber Threat Intelligence (CTI) describes _what_ adversaries do, but not enough of _how_ to automate those behaviors" (§1 Abstract)

**Maps to:** [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §III-A (line 103) and §III-D (line 131) — both passages cite [13] for this exact construction; [`../specs/architecture.md`](../specs/architecture.md) §(c) L0 framing, where Attack Flow is brought in precisely to supply the dependency/ordering structure that Ferraz documents as absent from raw STIX.

**Disposition for this thesis:** *adopted-as-baseline.* The procedural-semantics gap is the rhetorical foundation under §III-D's "two forms (manual / automated) of bridging the gap" structure. The dissertation's L0→L1→L2 pipeline is one such bridge, executed at simulation level rather than emulation level.

---

### The "procedural sufficiency boundary" — a measurement boundary, not an absence claim

**Source locator:** §1 Introduction (RQ framing + Figure 1 caption); §9 Discussion, opening; §11 Conclusion.

**Paraphrase:** Ferraz reframes the gap as a *boundary* rather than a defect. The contribution is to draw, by measurement, a reproducible line between (i) the behavioural information that public ATT&CK-in-STIX *does* encode and serves as grounding, and (ii) the procedural elements — ordering, parameters, preconditions, SUT bindings — that an analyst or model must still supply before any technique can execute. Public CTI's role is recast as a bounded input to intelligence-driven emulation, "rather than as a coverage label." Figure 1's "translation boundary" is the diagrammatic instance of this idea: descriptive CTI plus a declared SUT crosses the boundary via explicit translation and binding into an executable workflow.

**Quote (if essential):**
> "These results establish a reproducible boundary between the behavioral information encoded in public CTI and the procedures that must still be provided prior to execution." (§1 Abstract)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(j) methodological positioning — the boundary framing is the cleanest way to characterise what the L0→L2 build pipeline *does not* claim to supply (and where analyst curation enters); also relevant to [`../specs/architecture.md`](../specs/architecture.md) §(g) L4 validation framing.

**Disposition for this thesis:** *adopted-as-baseline.* The "procedural sufficiency boundary" terminology is directly inheritable; the dissertation operates on the same boundary, with the curated Attack Flow corpus (§III-A of the lit review) sitting on the grounding side and the L1/L2 motivation-subgraph construction sitting on the curation side. Mark this term for adoption in the Methodology chapter.

---

### Three-stage methodology — structural modelling → translation → execution

**Source locator:** §5 Methodology (§5.1 Stage 1, §5.2 Stage 2, §5.3 Stage 3); Figure 2 caption; §9 Discussion (Stage-1 vs Stage-2 automatability audit).

**Paraphrase:** Ferraz's pipeline is format-agnostic in design and instantiated with STIX + Caldera. Stage 1 is *automated structural modelling*: typed objects (techniques, campaigns, intrusion sets, malware, tools) are normalised into a behavioural graph; each campaign becomes a binary vector over techniques; a conservative tactic-ordered list is derived per campaign by aligning each technique with the canonical ATT&CK kill-chain progression (Reconnaissance → Impact), with deterministic tie-breaking by external identifier. This ordering is explicitly called an organisational behaviour, not a recovered temporal sequence. Stage 2 is *analyst-curated technique translation*: each technique in the ordered list is bound to an executable step (a concrete command), with parameters, preconditions, privilege assumptions, and validation logic supplied by the analyst — optionally drafted from Atomic Red Team templates or LLM suggestions, but validated against platform constraints. Missing bindings are documented explicitly. Stage 3 is *workflow integration*: translated steps become Caldera abilities, grouped into adversary profiles, orchestrated through Caldera operations.

A structured-field audit in §9 finds Stage 1 *fully automatable* against the v18.1 Enterprise bundle: `kill_chain_phases` and `x_mitre_platforms` are populated for all 691 active techniques (Appendix C, Table 3). Stage 2 is *not* rule-automatable from the current bundle: candidate fields (`x_mitre_system_requirements`, `x_mitre_data_sources`, `x_mitre_permissions_required`) are absent, and `x_mitre_detection` carries no machine-actionable content. Hence Stage 2 must be supplied by an expert analyst, LLM, or other strategy.

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(c)–(f): Ferraz's Stage 1 ≈ this thesis's L0→L1 (structural modelling and aggregation of CTI into a behavioural graph); Stage 2 ≈ this thesis's L1→L2 (motivation-subgraph construction is the closest analogue — though the dissertation's analyst-curation effort lives upstream at the Attack Flow corpus authorship layer rather than at per-technique command binding); Stage 3 ≈ this thesis's L3 (graph traversal inside the substrate). Note the substrate-level divergence is documented separately below.

**Disposition for this thesis:** *adopted-as-baseline* on the staging concept itself. The dissertation's L0→L1→L2 build pipeline is the closest published parallel to Ferraz's Stage 1 + Stage 2; Ferraz's Stage 2 being non-rule-automatable is a useful corroboration of why the dissertation depends on the analyst-curated Attack Flow corpus rather than attempting an end-to-end automated extraction from raw STIX.

---

### Empirical findings — campaign sparsity, no reusable backbone (43.0% coverage)

**Source locator:** §6 Behavioural Analysis (paras 9–13 and the synthesis bullets at the end of §6); Figure 5; Appendix D Table 4.

**Paraphrase:** Across the 51 active Enterprise campaigns and 691 active attack-pattern objects in v18.1, Ferraz reports four mutually reinforcing negative results about behavioural reusability:

1. *Coverage is sparse.* Only 43.0% of techniques (297 of 691) appear in at least one campaign; 57.0% appear in no campaign. The most-used technique (T1105, Ingress Tool Transfer) appears in 55% of campaigns; no technique is universal across campaigns.
2. *No stable clusters.* k-means with k=7 on campaign-technique vectors yields a mean silhouette of 0.05; a sparsity-preserving random baseline yields −0.01 ± 0.01; Jaccard agglomerative clustering across k ∈ [2, 10] yields silhouettes in 0.03–0.05. PCA on the 172 intrusion sets (Figure 3) shows a dense near-origin cloud with no distinct families.
3. *No shared subsequences.* Longest Common Subsequence over the 1,275 campaign pairs (tactic-ordered) gives mean length 2.8 (median 2.0, max 29); 200 randomised tactic-orderings keep the mean in 2.728–2.754. Appendix D's order-free probe shows the maximum support of any 5-itemset is 6 campaigns (11.8%).
4. *Intrusion sets are broader but still not procedures.* Intrusion sets cover 70.6% of techniques (488 of 691) and are less fragmented than campaigns, but the median Jaccard overlap between a campaign and its attributed intrusion set is only 10.0% (across 22 active attribution pairs).

The synthesis is that public CTI carries small recurring behavioural fragments but not a dominant reusable backbone — confirming the procedural-semantics gap quantitatively rather than rhetorically.

**Quote (if essential):**
> "only 43.0% of techniques appear in at least one campaign, and neither clustering nor Longest Common Subsequence (LCS) analysis reveals reusable procedural structure" (§1 Abstract)

**Maps to:** [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §III-A (line 101, "richest campaign-level structure" claim) and §III-D (line 131, the procedural-semantic-gap claim) both lean on this measurement; the result also underwrites this dissertation's choice in [`../specs/architecture.md`](../specs/architecture.md) §(c) to use the analyst-curated Attack Flow corpus as L0 input rather than attempting to derive structure from raw STIX campaign objects.

**Disposition for this thesis:** *verified* as the empirical anchor for §III-D's framing — but the dissertation does *not* attempt to replicate or extend the measurement itself. Used as a finding to cite, not as a result to reproduce.

---

### Caldera substrate vs MTDSim substrate — the C-class boundary inside an L-class paper

**Source locator:** §5.3 Stage 3 (Emulation Integration); §7 Emulation Setup; §10 Threats to Validity (Execution validity para); §B Open Science.

**Paraphrase:** Ferraz instantiates Stage 3 in MITRE Caldera 5.3.0 — an adversary emulation framework that executes concrete commands against a real (containerised) target environment. The laboratory is four Docker containers across three private networks (Caldera server, Kali agent, NGINX service, internal database), with each translated technique implemented as a Caldera ability carrying a single shell command and optional cleanup logic. Workflows execute in an isolated, reproducible testbed; success is measured by successful-link counts, end-of-workflow markers (T1529), and absence of residual non-zero links at plateau. Execution validity is bounded by the laboratory substrate — outcomes are evidence of *procedural progress* within Ferraz's shared Docker substrate, not of *historical replay* on victim infrastructures. The Docker testbed is "intentionally simplified and designed to test procedural coherence rather than to reproduce historical victim infrastructures."

The dissertation makes a different substrate choice: the equivalent of Stage 3 lives inside MTDSim (a discrete-event simulator, not an emulator), and the operationalisation is graph-traversal inside the simulator rather than command execution against containers. This is documented as an explicit architectural decision in [`../specs/architecture.md`](../specs/architecture.md) §(a) ("Decision — no MITRE Caldera adversary emulation"; rationale: emulation overhead misaligned with simulation-based scope). The two substrates target different fidelity rungs: Caldera operates at executable-procedure fidelity (concrete commands against concrete hosts), MTDSim at simulated-traversal fidelity (technique-level events with timing). The framing layers above the substrate (procedural-semantics gap, sufficiency boundary, three-stage staging) carry across; the substrate layer does not.

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(a) "Decision — no MITRE Caldera adversary emulation"; §(f) L3 (the OGASP operationalisation layer); §(j) methodological positioning.

**Disposition for this thesis:** *contrasted-against* at the substrate layer only. Ferraz is load-bearing on framing (the four artefact sections above) and contrasted on execution venue: this dissertation deliberately does *not* execute against a real or containerised target environment, by the architecture §(a) decision. The contrast is methodological scope, not a disagreement — Ferraz's Caldera measurements answer a different question ("does the workflow execute?") from the dissertation's MTDSim runs ("how do MTD mechanisms perform against behaviourally-grounded traversal?").

---

### Used in lit review

Cited as `[13]` in [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) (References list at line 261). In-text locators:

- **Line 101** (§III-A, MITRE ATT&CK) — "among public STIX exports, the Enterprise bundle preserves the richest campaign-level structure [13]" and "ATT&CK has become the *lingua franca* for adversary behaviour [13], [14]." Anchors the choice of Enterprise bundle as the empirical centre and corroborates ATT&CK's status as the de-facto standard.
- **Line 103** (§III-A) — "the ATT&CK-in-STIX export — records *which* techniques an adversary used without recording *how* they fit together: it encodes no temporal order, explicit prerequisites, environmental constraints, or branching logic between techniques [13]." Anchors the structural-property statement that motivates Attack Flow's introduction in the next paragraph.
- **Line 131** (§III-D, Attack Profiling) — two citations: "CTI ... in its unstructured form ... requires manual normalisation before systematic use [13]" and the procedural-semantic-gap definition itself: "CTI describes *what* attackers do but routinely omits the sequencing, preconditions, and dependencies — the *how* — required to operationalise behaviour as an executable or simulable process [13]." This is the load-bearing citation — §III-D's two-paths structure (manual curation vs automated extraction) hangs off this framing.

## Open questions / things to verify

- **arXiv-version reconciliation.** The source PDF (earlier draft, "ATT&CK-in-STIX" title) reports the 43.0% campaign-coverage figure used above. arXiv v1+ (current v3, May 2026) is retitled "Structured CTI" and reportedly carries a 35.6% figure (per the bibliographic-anchor block at the top of this file). Before any quotation from this extraction lands in the dissertation prose, Marc should pin which arXiv version is being cited and reconcile the headline number — the LIT_REVIEW.md entry already cites the 2026 arXiv handle, so the 35.6% figure may be the one to use in the manuscript even though the structural argument is identical in either draft.
- **"Procedural" rung naming in §IV-B Table II.** LIT_REVIEW.md §IV-B (line 195) uses "procedural" as one rung in the fidelity descriptor; the same word names Ferraz's gap. The lit review's procedural rung is defined narrowly as "rule-based decision-making within an attack progression at runtime" (line 174). Ferraz's "procedural semantics" is broader (ordering, parameters, preconditions, environment). The two are consistent — runtime rule-based decision-making is a strict subset of what Ferraz means — but the manuscript should be explicit that the two usages are coherent and not borrowed names for different things. Marc to verify in Methodology chapter.
- **Stage-2 analyst burden vs the dissertation's analyst burden.** Ferraz's Stage 2 analyst effort goes into per-technique command binding (endpoints, ports, credentials, validation logic). The dissertation's analyst effort goes into the Attack Flow corpus authorship (CTID flow construction) and motivation attribution at L2. These are *different* kinds of analyst-curation work and Marc should be explicit about this when adopting the three-stage framing — the dissertation is not "automating Ferraz's Stage 2", it is *moving the analyst-curation upstream* to the corpus-authorship layer.

## Out of scope for this thesis

- Caldera-specific implementation details.
