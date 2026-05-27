---
status: durable
created: 2026-05-27
topic: GAP construction (L1)
---

# How the GAP is built, and what it assumes

## Why this is worth recording

The GAP (Generalised APT Profile) is the first transformation that turns
published threat intelligence into something the simulator can drive an attacker
with. Several choices in how it is built are **load-bearing methodological
commitments**, not implementation trivia, and an examiner will reasonably ask
"why this and not that?". This note states those choices in plain English and —
the part most easily lost in the code — names the **assumptions** that bound what
the GAP can claim to represent. The headline one (the graph is labelled against
MITRE ATT&CK *Enterprise* only) is invisible in the code yet shapes what the
downstream evaluation actually means.

## The substance

**What it is.** The GAP aggregates many analyst-drawn, per-incident *Attack
Flow* diagrams into one directed graph: nodes are ATT&CK techniques, edges are
dependencies between them ("to do B, the adversary first needed A"). One
incident shows one path; the GAP generalises across ~40 incidents so the
attacker model reflects *recurring* behaviour, not a single campaign.

**The non-negotiable rule.** Every edge corresponds to a dependency a human
analyst actually drew in some flow. Nothing is inferred statistically or by a
language model. (The superseded v0.4 approach mixed in technique co-occurrence
and keyword heuristics — edges no analyst drew.) This is what makes the GAP a
*behavioural* profile rather than a generic "these techniques co-occur" graph,
and it is what licenses the claim that the simulated attacker is doing things
real adversaries were *observed* doing.

**What's preserved.** Real attacks aren't linear. Analysts express this with
AND/OR operators (several things must all happen before the next) and
conditional branches (if X succeeds do Y, else Z). The GAP keeps this: where v0.4
flattened a three-way AND-join into three unrelated edges, the GAP tags each edge
with the operator and the *join-group* it belonged to, so "these three are
jointly required" is recoverable. The worked example is the 2018 Tesla
cryptojacking incident — Deploy Container (T1610), Proxy (T1090) and Non-Standard
Port (T1571) are all required before Resource Hijacking (T1496) — which is the
lit review's Figure 2, and is now a passing test.

**Lossless, with reduction as a lens.** The committed GAP keeps every observed
edge, with a count of how many incidents showed it, and preserves cycles (real
attackers loop: move laterally, discover more, move again). Thresholding ("only
edges seen in ≥ k incidents"), projecting to an acyclic graph, and tactic
layering are computed on demand as *views* — never baked into the stored
artefact. A later decision to filter more aggressively changes only the view, not
the data, and stays reproducible.

**Two committed layers.** Each incident becomes a small, human-readable per-flow
file (the lossless intermediate); these aggregate into the single GAP. The
per-flow files are deliberately hand-editable — the seam for adding a
hand-curated incident later, which then aggregates identically to a
corpus-derived one.

## Assumptions that bound the claims

The "future-you must defend this" points:

- **ATT&CK Enterprise only.** Technique names, tactics and platforms come from
  MITRE ATT&CK *Enterprise* (pinned at v19.1). The corpus is not purely
  Enterprise: a few incidents reference ATLAS (adversarial-ML) or ICS
  techniques, and some use technique IDs that recent ATT&CK has since revoked.
  These still appear as GAP nodes — they are real observations — but carry no
  label. They are kept **as the analyst drew them**, never remapped to a
  "nearest" current technique (that would be us inventing intelligence). The
  consequence: the GAP is an Enterprise-centric reading of a slightly broader
  corpus, and a minority of nodes are unlabelled. An "Enterprise-only" filtered
  *view* is the natural way to set them aside when that matters. **This is an
  assumption, not a result.**
- **Latest-ATT&CK pin.** Pinning the newest ATT&CK is a deliberate
  "current taxonomy" choice; it is why some older corpus IDs read as revoked. The
  alternative — pinning a version contemporaneous with each incident — chases a
  moving target across a decade of incidents, so a single recent pin is the
  defensible simplification.
- **Tactic order is layout only.** The kill-chain ordering is used for drawing
  and for describing an edge as forward/backward — it never sets or reverses an
  edge's direction. Direction comes only from the flow. (v0.4 used tactic order
  to *impose* direction on inferred edges; that is exactly the synthesis this
  design rejects.)
- **Sub-techniques collapse to their parent.** T1078.004 is counted as T1078 —
  denser, more general graph at the cost of sub-technique precision; revisitable
  if a finding needs the finer resolution.
- **Conditions are mostly end-state annotations in this corpus.** The schema
  supports true/false branches and the build handles them, but the public corpus
  rarely populates them — so branch-conditioned edges are a *tested capability*,
  not yet a corpus-exercised feature.

## How it connects

- To the spec: [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) is the
  formal data model + the four decisions; this note is its plain-English
  companion. Build code: [`../../src/mtdsim/l1_construction/`](../../src/mtdsim/l1_construction);
  artefacts: [`../../data/gap/`](../../data/gap).
- To the architecture: [`architecture.md`](../specs/architecture.md) §(c)–(d)
  place the GAP as L1 of the L0→L4 pipeline.
- To the lit review: the Attack Flow grammar and the Tesla Figure-2 example are
  extracted in [`../extractions/attackflow.md`](../extractions/attackflow.md).

## When this would need updating

- If the ATT&CK pin changes — re-examine the revoked-ID and unlabelled-node
  counts.
- If hand-curated incidents are added (the per-flow seam) — the "corpus-derived
  only" framing weakens.
- If the Enterprise-only assumption is revisited (e.g. ATLAS/ICS techniques
  brought in with their own matrices).
- If cross-flow AND/OR reconciliation is resolved — the GAP currently records
  disagreeing joins without adjudicating them; likely settled at the eventual
  Petri-net step.
