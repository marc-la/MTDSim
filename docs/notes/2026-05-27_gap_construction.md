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
incident shows one path; the GAP generalises across ~39 incidents so the
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

**Lossless within scope, with reduction as a lens.** The committed GAP keeps
every observed edge *between Enterprise techniques* (see the Enterprise-only
assumption below), with a count of how many incidents showed it, and preserves
cycles (real attackers loop: move laterally, discover more, move again).
Thresholding ("only edges seen in ≥ k incidents"), projecting to an acyclic
graph, and tactic layering are computed on demand as *views* — never baked into
the stored artefact. A later decision to filter more aggressively changes only
the view, not the data, and stays reproducible. (Enterprise scope is the one
thing baked in, not a view — it defines *which taxonomy* the GAP is, rather than
reducing it; the per-flow layer below stays fully lossless regardless.)

**Two committed layers.** Each incident becomes a small, human-readable per-flow
file (the lossless intermediate); these aggregate into the single GAP. The
per-flow files are deliberately hand-editable — the seam for adding a
hand-curated incident later, which then aggregates identically to a
corpus-derived one.

## What the assembled graph looks like

A few properties of the built artefact (observed on the current Enterprise-only
build: 124 technique nodes, 478 edges, 39 flows) are worth recording — they
shape how the GAP can be read, and they bear out the design choices above.

**The tactic-level view is nearly a complete graph.** Collapse the techniques
onto their 15 ATT&CK tactics — an FSM whose states are tactics — and roughly 6
in 10 of all possible directed transitions are already present (132 of 225,
self-loops included), approaching complete connectivity among the handful of hub
tactics. So at the tactic level *which* stages connect is almost uninformative;
the signal is entirely in *how often* — the edge weights. This is the empirical
case for carrying an observation count on every edge and treating thresholding as
a view: strip the weights and the tactic graph is a near-clique that says little.

**The technique-level graph is dense, and its generalisation is thin.** 478
edges over 124 nodes is a hairball unfiltered, but the sharper point is that
**88% of those edges (419) were drawn in exactly one incident**; only 59 recur,
and just 7 appear in three or more. The "recurring adversary behaviour" the GAP
claims therefore lives in a small high-weight core — command-and-control ↔
discovery (the beacon-and-recon loop), execution → stealth, and a few self-loops
— while the long tail is campaign-specific. Any downstream use that ignores the
weights is mostly reading single-incident detail, not generalised behaviour.

**The kill chain is a loose layout, not the shape.** The graph is genuinely
cyclic: ~37% of edges run *backward* against kill-chain order and two-thirds of
the tactics carry a self-loop (several discovery steps in a row; lateral-move →
discover → lateral-move again). The tactic ordering earns its keep only for
drawing and for labelling an edge forward/backward — it does not describe a
linear progression, which is exactly why direction is taken from the flows and
never from the layering.

**The early kill chain is barely observed — and that confirms the literature
where it can see.** Incident-derived intelligence starts at the point of
*detection* (the intrusion) and works forward; pre-intrusion reconnaissance
happens on attacker infrastructure and via OSINT, leaves little defender
telemetry, and so analysts rarely draw it. The corpus bears this out:
**reconnaissance appears in only 10 of 39 flows while initial-access appears in
30 of 39**, and there is essentially no `reconnaissance → initial-access` edge
(1, observed once). This is not a modelling error but a **survivorship-/
observability bias** of the source — the GAP is densest in the observable middle
of the kill chain and blind to the pre-intrusion prefix. It does **not**
contradict Alshamrani 2019's claim that the recon→foothold prefix is *invariant*
across APT operations; it *confirms it at the half the corpus can see* (foothold,
30/39, is densely observed) while being structurally unable to observe the
invariant prefix itself. The same lens corroborates the back half of Alshamrani's
claim: of the 39 flows, **13 reach exfiltration, 13 reach impact, but only 3 reach
both** — campaigns commit to *one* terminal objective, exactly the "stages 4–5
split by objective" structure, observed directly in the data (and what makes the
L2 motivation-subgraphing design defensible against this corpus). The decision not
to paper over the prefix gap in the canonical GAP — supplying it, if at all, only
through a separately-provenanced `inferred` overlay, never the observed graph — is
Decision 6 in [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) §(b)/§(h).

**Both levels need a lens to be legible.** Neither view reads unfiltered — the
technique graph swamped by edge count, the tactic FSM by near-completeness.
Weighting (emphasis) and thresholding (the "≥ k incidents" view) are not
cosmetic; they are how either level becomes interpretable, and the two trade
resolution against legibility. The right view depends on the question being
asked — which is the whole reason reduction is kept as a lens rather than baked
in.

## The observability boundary is a defender's-eye property — a threat-model input, not just a limitation

The thinness above (88% single-observation) and the recon blindness read as
*limitations* only if the goal were a complete, attacker's-eye account of APT
behaviour. It is not. The GAP feeds a **defender-side** evaluation: MTD is a
control a defender deploys, and the question is how it perturbs the attacker
behaviour a defender *can know about*. CTI is exactly the codification of that
knowledge — so an attacker model built from CTI is bounded by what defenders
observe *by construction*, and that bound is the right shape for the object being
modelled. The simulated attacker being blind to pre-intrusion reconnaissance is
**faithful to the defender's actual epistemic position**, not a sampling defect to
apologise for.

That reframes the bias as a finding. Where CTI goes dark maps the **limits of
defensible knowledge**, and those limits are themselves an input to the APT threat
model ([`architecture.md`](../specs/architecture.md) §(e)–(f)): the front end
(passive recon, resource development) and the symmetric back end (post-objective
cleanup / anti-forensics — Alshamrani's phase 5, which *by design* erases the
telemetry the report is built from) are the two regions where a defender must
*infer* an adversary's behaviour rather than *observe* it. Naming precisely where
the observed account stops and inference must begin is an astute property of the
threat model, not a weakness of the corpus — and it is sharpest on the
*dependency*, not the technique: even when a reconnaissance node appears it is
mostly in-network discovery wired *backward* from the observable middle (8 of its
in-edges come from execution / persistence / lateral-movement / C2), while the
pre-intrusion `reconnaissance → initial-access` *edge* is essentially absent.

Supplementing that prefix (Decision 6's `inferred` overlay) does **not escape the
boundary — it is still CTI**. Group-behaviour reports, ATT&CK group profiles, and
survey structural claims document recon *vocabulary* and *generalised sequencing*,
but the incident-wired recon→foothold *edge* remains an inference — often someone
else's (a vendor analyst's read, or non-public collection re-badged). So the
overlay imports well-grounded nodes glued by inferred edges; it extends the model
*within* CTI's epistemic envelope rather than reaching ground truth. That is
exactly why it is a declared, separately-provenanced, opt-in layer: cheap to
author through the per-flow seam, deferred for now, and labelled so the threat
model can state which of its edges are observed and which are inferred. The
contribution is not "we filled the gap" but "we model the attacker the defender
must reason about, and we are explicit about where that reasoning is observation
versus inference." And the survivorship/selection framing is what makes this
global rather than a prefix quirk: the corpus is built from incidents that were
detected, investigated deeply enough to reconstruct, *and* published — so even the
dense middle is the behaviour of campaigns that were *caught*. Recon and cleanup
are the extremes of a bias that tilts the whole graph toward observable,
documented, largely-successful-but-detected operations.

## Assumptions that bound the claims

The "future-you must defend this" points:

- **ATT&CK Enterprise only — baked into the GAP.** The GAP is scoped to MITRE
  ATT&CK *Enterprise* (pinned at v19.1): a node is kept only if it resolves to a
  current Enterprise technique. The corpus is not purely Enterprise — a few
  incidents reference ATLAS (adversarial-ML, `AML.*`) or ICS (`T0###`)
  techniques, and some use IDs that v19.1 has revoked — and those nodes are
  **dropped from the aggregated GAP**, together with their edges. Crucially the
  drop is *removal, not remapping or bridging*: we never reconnect a dependency
  across a dropped node (that would invent intelligence no analyst drew), and we
  never relabel a technique to a "nearest" current one. The *per-flow extracts
  stay lossless* — they record every technique as the analyst drew it, ATLAS and
  ICS included — so the corpus record and the hand-curation seam are intact; the
  Enterprise scope is applied only when aggregating the per-flow extracts into
  the GAP. The consequence: the GAP is a clean Enterprise-technique graph (every
  node labelled), built from a slightly broader corpus whose non-Enterprise parts
  live on in the per-flow layer. **This is an assumption, not a result** — at
  v0.5, 22 of 146 candidate nodes were non-Enterprise (15 ATLAS, 2 ICS, 5
  revoked/absent), and were dropped.
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
  formal data model + the six decisions; this note is its plain-English
  companion. Build code: [`../../src/mtdsim/l1_construction/`](../../src/mtdsim/l1_construction);
  artefacts: [`../../data/gap/`](../../data/gap).
- On what the edge weights mean (recurrence, **not** efficacy or transition
  probability) and the "MTD perturbs typical observed workflow" comparability
  boundary for L3/L4: [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f).
- To the architecture: [`architecture.md`](../specs/architecture.md) §(c)–(d)
  place the GAP as L1 of the L0→L4 pipeline.
- To the lit review: the Attack Flow grammar and the Tesla Figure-2 example are
  extracted in [`../extractions/attackflow.md`](../extractions/attackflow.md).

## When this would need updating

- If the ATT&CK pin changes — re-examine the revoked-ID and unlabelled-node
  counts.
- If hand-curated incidents are added (the per-flow seam) — the "corpus-derived
  only" framing weakens.
- If the `inferred` overlay (Decision 6 — Option B) is ever authored — the
  pre-intrusion prefix becomes modellable, but only in the corpus+inferred view;
  the observed-only framing of the canonical GAP above is unchanged.
- If the Enterprise-only assumption is revisited (e.g. ATLAS/ICS techniques
  brought in with their own matrices).
- If cross-flow AND/OR reconciliation is resolved — the GAP currently records
  disagreeing joins without adjudicating them; likely settled at the eventual
  Petri-net step.
- As the corpus grows — the single-observation share (88% at v0.5) is the number
  to watch: it measures how much of the GAP is genuinely *recurring* behaviour
  versus one-off campaign detail, and is the honest gauge of whether "generalised"
  in the name is yet earned.
