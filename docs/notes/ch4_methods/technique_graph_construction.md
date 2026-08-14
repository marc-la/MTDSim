---
status: durable
chapter: ch4_methods
created: 2026-05-27
updated: 2026-07-13
lineage: 2026-05-27_gap_construction.md
---

# Constructing the technique graph from threat intelligence — what is built, and what it assumes

## Position in the dissertation

The methodology chapter's account of the pipeline's first transformation: how published incident intelligence becomes a single aggregated graph of adversary technique dependencies, which design choices in that construction are load-bearing methodological commitments, and which assumptions bound what the graph can claim to represent.

## The idea

The attacker model in this work is grounded in *Attack Flow* diagrams — analyst-drawn, per-incident graphs published by MITRE's Center for Threat-Informed Defense, in which each node is a MITRE ATT&CK technique and each edge is a dependency the analyst observed ("to do B, the adversary first needed A"). One incident shows one path; the construction aggregates roughly thirty-nine incidents into a single directed graph — internally called the *Generalised APT Profile* (GAP) — so that the simulated attacker reflects *recurring* behaviour rather than a single campaign. Several choices in how that aggregation is done deserve defence, and an examiner will reasonably ask "why this and not that?".

**The non-negotiable rule.** Every edge in the graph corresponds to a dependency a human analyst actually drew in some incident. Nothing is inferred statistically or by a language model. (A superseded earlier approach mixed in technique co-occurrence and keyword heuristics — edges no analyst drew.) This rule is what makes the graph a *behavioural* profile rather than a generic co-occurrence graph, and it is what licenses the claim that the simulated attacker does things real adversaries were *observed* doing.

**What is preserved.** Real intrusions are not linear. Analysts express this with AND/OR operators (several preconditions jointly required) and conditional branches. The construction keeps this structure: each edge is tagged with its operator and the join-group it belonged to, so "these three steps are jointly required" remains recoverable. The worked example is the 2018 Tesla cryptojacking incident, where deploying a container, establishing a proxy, and opening a non-standard port are all required before resource hijacking; the case is preserved end-to-end and enforced by a test.

**Lossless within scope, with reduction as a lens.** The committed graph keeps every observed edge between ATT&CK Enterprise techniques, with a count of how many incidents exhibited it, and preserves cycles (real attackers loop: move laterally, discover more, move again). Thresholding ("edges seen in ≥ k incidents"), acyclic projection, and tactic-level layering are computed on demand as *views*, never baked into the stored artefact — a later decision to filter differently changes the view, not the data. Two committed layers realise this: each incident becomes a small, human-readable per-incident file (the lossless intermediate, deliberately hand-editable — the seam for adding a hand-curated incident later), and these aggregate into the single graph.

### What the assembled graph looks like

The built artefact (124 technique nodes, 478 edges, 38 incidents at the current version) has properties that shape how it can be read:

- **The tactic-level view is nearly a complete graph.** Collapsing techniques onto their fifteen ATT&CK tactics, roughly six in ten of all possible directed transitions are present. At tactic level, *which* stages connect is almost uninformative; the signal is entirely in *how often* — the edge weights. This is the empirical case for carrying an observation count on every edge.
- **The technique-level graph is dense, and its generalisation is thin.** 88% of edges (419 of 478) were drawn in exactly one incident; only 59 recur, and just 7 appear in three or more. The "recurring adversary behaviour" the graph claims therefore lives in a small high-weight core — a command-and-control ↔ discovery loop, execution → concealment, and a few self-loops — while the long tail is campaign-specific detail. Any downstream use that ignores the weights is mostly reading single-incident detail. The single-observation share is the honest gauge of whether "generalised" in the artefact's name is yet earned, and it is the number to watch as the corpus grows.
- **The kill chain is a layout, not the shape.** The graph is genuinely cyclic: about 37% of edges run backward against kill-chain order, and two-thirds of tactics carry self-loops. Tactic ordering is used only for drawing and for labelling an edge forward/backward; direction always comes from the incident flows.

### The observability boundary — a threat-model input, not just a limitation

Incident-derived intelligence starts at the point of *detection* and works forward. Pre-intrusion reconnaissance happens on attacker infrastructure and leaves little defender telemetry, so analysts rarely draw it — and the corpus bears this out: reconnaissance appears in only 10 of 38 incidents while initial access appears in 30, and the reconnaissance → initial-access edge is essentially absent (observed once). This under-run repeats at the back end: post-objective cleanup and anti-forensics erase, by design, the telemetry reports are built from.

This thinness reads as a limitation only if the goal were a complete, attacker's-eye account of adversary behaviour. It is not. The graph feeds a *defender-side* evaluation: MTD is a control a defender deploys, and the question is how it perturbs the attacker behaviour a defender *can know about*. Threat intelligence is exactly the codification of that knowledge, so an attacker model built from it is bounded by defender observability *by construction* — the right bound for the object being modelled. The simulated attacker being blind to pre-intrusion reconnaissance is faithful to the defender's actual epistemic position, not a sampling defect to apologise for. Where the intelligence goes dark maps the limits of defensible knowledge, and naming precisely where observation stops and inference must begin is a property of the threat model, not a weakness of the corpus. The corpus's selection bias is acknowledged as global rather than a prefix quirk: it is built from incidents that were detected, investigated deeply enough to reconstruct, and published — so even the dense middle describes campaigns that were caught.

Notably, the corpus *confirms* the structural claims of the APT survey literature where it can see: the densely-observed foothold stage is consistent with Alshamrani et al.'s (2019) invariant recon-to-foothold prefix, and of the 38 incidents, 13 reach exfiltration, 13 reach impact, but only 3 reach both — campaigns commit to one terminal objective, exactly the objective-conditioned back half that survey predicts, observed directly in the data. That observation is what makes slicing the graph by operational objective defensible against this corpus (see the partition rationale note).

### Assumptions that bound the claims

- **ATT&CK Enterprise only, baked in.** A node is kept only if it resolves to a current Enterprise technique under the pinned ATT&CK version (v19.1). The corpus is slightly broader — a few incidents reference adversarial-ML or industrial-control-system techniques, or revoked IDs — and those nodes are *dropped, not remapped or bridged*: dependencies are never reconnected across a dropped node (that would invent intelligence no analyst drew). The per-incident layer stays fully lossless; the scope is applied only at aggregation. At the current version, 22 of 146 candidate nodes were non-Enterprise and dropped.
- **Latest-version pin.** Pinning the newest ATT&CK is a deliberate "current taxonomy" choice; the alternative — pinning a version contemporaneous with each incident — chases a moving target across a decade of incidents.
- **Tactic order is layout only** (above); it never sets or reverses an edge's direction.
- **Sub-techniques collapse to their parent** (T1078.004 counts as T1078): a denser, more general graph at the cost of sub-technique precision; revisitable if a finding needs finer resolution.
- **Conditional branches are a tested capability, not a corpus-exercised feature.** The schema and build handle analyst-drawn true/false branches, but the public corpus rarely populates them.
- **The pre-intrusion prefix is never silently filled.** If reconnaissance structure is ever supplied, it enters as a separately-provenanced, opt-in *inferred* overlay — and even that overlay stays within threat intelligence's epistemic envelope: it imports well-grounded technique vocabulary glued by someone's inference, not ground truth. The contribution is not "we filled the gap" but "we are explicit about which edges are observation and which are inference".

## Evidence and repo anchors

- The formal data model + numbered construction decisions: [`../../implementation/pipeline/gap/gap_schema.md`](../../implementation/pipeline/gap/gap_schema.md) (this note is its methodological companion). Build code under `src/mtdsim/l1_construction/`; artefacts under `data/gap/`.
- Edge-weight semantics (recurrence, never efficacy or transition probability) and the comparability boundary: [`../../implementation/metrics_semantics.md`](../../implementation/metrics_semantics.md) §(f).
- Pipeline position: [`../../implementation/architecture.md`](../../implementation/architecture.md) §(c)–(d).
- The Attack Flow grammar and the Tesla worked example: [`attackflow`](../../sources/extractions/attackflow.md); the APT-phase structural claims: [`alshamrani2019`](../../sources/extractions/alshamrani2019.md).
- Downstream dependants: [`objective_partition_rationale.md`](objective_partition_rationale.md), [`objective_partition_findings.md`](objective_partition_findings.md).

## Revisit conditions

- If the ATT&CK pin changes — re-examine revoked-ID and unlabelled-node counts.
- If hand-curated incidents are added through the per-incident seam — the "corpus-derived only" framing weakens and must be requalified.
- If the inferred reconnaissance overlay is ever authored — the observed-only framing of the canonical graph is unchanged, but the corpus+inferred view becomes available and must be labelled.
- As the corpus grows — re-check the 88% single-observation share; it measures how much of the graph is genuinely recurring behaviour.
