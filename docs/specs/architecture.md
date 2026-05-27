# Architecture — L0→L4 pipeline and methodological positioning

**Status:** Pass 1 scaffold (drafted 2026-05-27 from the pre-lit-review *Current
State* doc and the *Methodology Carry-Forward* note, both pasted-only). The
skeleton, decisions log, and substrate seam are in place; methodological
positioning will be fleshed against [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) in Pass 2.
Each subsection carries an explicit `Status:` marker
(*designed* / *partially built* / *unbuilt*) — the architecture describes the
*system by design*, not progress.

This file describes Marc's system *on top of* the inherited substrate. For the
substrate itself see [`mtdsim_spec.md`](mtdsim_spec.md); for the metrics those
runs produce see [`metrics_semantics.md`](metrics_semantics.md); for the
codebase-↔-source provenance, see [`provenance.md`](provenance.md). This file
does not restate any of them.

---

## (a) Goal and scope

This work evaluates *existing* Moving Target Defence (MTD) mechanisms against
**behaviourally-grounded adversarial profiles derived from CTI**. The contribution
sits at the intersection of three independently-mature literatures: CTI-grounded
attack profiling, attack-graph operationalisation in simulation, and MTD
evaluation. The pipeline takes raw CTI (L0) through aggregation (L1, **GAP** —
Generalised APT Profile), motivation-subgraphing (L2, **GASP** —
motivation-subgraphed APT Profile), and operationalisation inside MTDSim
(L3, **OGASP** — Operationalised GASP), to comparative effectiveness
measurement (L4). The §(h) glossary carries full definitions.

The substrate is the inherited MTDSimTime fork ([`mtdsim_spec.md`](mtdsim_spec.md));
the load-bearing seam is the **attacker module**, where graph-driven traversal
is added *alongside* — not replacing — the inherited 6-phase scripted attacker
(per [`project_context.md`](project_context.md) L17). The defender side is
deliberately frozen: SDR-family mechanisms + Tay's AI selection, no novel
defender innovation and no novel RL training.

The single research question is *"how do existing MTD mechanisms perform against
behaviourally-grounded adversarial profiles derived from CTI?"* — a comparative
question over (MTD family × attacker profile) on a single canonical substrate.

**Decision — single RQ, no sub-problems.**
**Why:** All previously-considered sub-questions resolved to either methodology
positioning (chapter 3 material) or empirical splits of the same comparative
claim; neither warrants RQ-level promotion. Aligns with
[`project_context.md`](project_context.md) L9.
**If revisited:** If Jin asks for sub-questions, frame them as empirical splits
(per-MTD-family, per-motivation-profile) of the umbrella, not methodology
choices.

**Decision — defence side is existing mechanisms only.**
**Why:** Defender-mechanism innovation is a "large can of worms" (Jin, 19 Mar
2026) and not the focus of the thesis. The contribution lives on the attacker
side.
**Cost:** L4 comparative claims are bounded to the existing-MTD pool
(SDR-family + Tay's AI selection); a "novel defender X outperforms Y" claim
is out of reach within this evaluation.
**If revisited:** Any defender-mechanism extension promotes this to a two-arm
contribution and rebudgets the evaluation matrix.

**Decision — IDS is not a research thread.**
**Why:** Folded into the lit review only, as one example of observation-driven
adaptive MTD. Detection/sensitivity machinery in Tay's RL agent is retained as
inherited substrate, not extended.
**If revisited:** Would require restoring IDS as L4 evaluation axis and
defining detection-quality semantics — a separate workstream.

**Decision — no MITRE Caldera adversary emulation.**
**Why:** Emulation overhead misaligned with simulation-based scope; the
contribution is a methodological one over a simulator, not over an emulation
platform.
**If revisited:** Caldera would shift the substrate from DES to emulation —
effectively a different thesis.

**Decision — Tay's RL agent is reused as benchmark defence, not retrained.**
**Why:** Retraining would consume time without a research payoff; the goal is
*comparison against* a known AI-driven MTD mechanism, not RL methodology
contribution. Deferred to the evaluation/ablation phase (per
[`project_context.md`](project_context.md) L10 and [`repo_conventions.md`](repo_conventions.md)).
**Role clarification:** Tay's policy is *both* (i) an inherited benchmark we
do not extend and (ii) one of the L4 comparison points alongside the
time-scheduled SDR schemes — these are the same code object in two roles, not
two competing framings.
**Cost:** Reuse runs against a known feature-shape mismatch — the model
expects 8 static + 3 time-series features but the pipeline returns 7 + 3
(missing `exposed_endpoints`, `attack_type`); chasing this belongs to the
eval/ablation phase. The methodological consequence is that L4 cannot
disentangle "MTD-AI's per-substrate optimisation" from "Tay's published
policy on this substrate" — Tay's column at L4 is an inherited-policy
result, not an optimised-policy result.
**If revisited:** If Tay's pretrained weights prove unusable end-to-end,
fall back to a documented "reference RL benchmark unavailable" disposition
rather than retraining.

---

## (b) ASCII pipeline diagram

```
   L0                     L1                    L2                    L3                       L4
 (raw CTI)              (GAP)                 (GASP)               (OGASP)                (evaluation)

 ATT&CK         ──►  aggregate  ──►   subgraph by    ──►  operationalise  ──►   compare MTD mechanisms
 Campaigns                              motivation             in MTDSim          across attacker profiles
 Attack Flow         techniques        terminal-node           graph-driven       MTTC | ASR
 corpus              + edges           ancestor proxy          attacker traversal | attack-path exposure
 ATT&CK group        (consensus,                               + inherited 6-phase| RoA
 descriptions        backward;                                 baseline retained
                     thresholds)
                                                                       ▲
                                                               attacker module seam
                                                              (load-bearing; see
                                                               project_context L17)
```

L0–L2 are pre-substrate (build-time artefacts). L3 is the seam where Marc's
work plugs into the inherited MTDSim substrate. L4 measures inside the
substrate using the metrics defined in [`metrics_semantics.md`](metrics_semantics.md).
**L4 metric values are within-substrate-only**: comparison across configurations
inside this substrate is valid; cross-paper numeric comparison against
Zhang/Tay published values is **not** (see
[`metrics_semantics.md`](metrics_semantics.md) §d for the comparability boundary).

---

## (c) L0 — Raw CTI

**Status:** designed (inputs are external).

- **Inputs.** MITRE ATT&CK Campaigns (techniques attributed to named campaigns);
  MITRE Attack Flow corpus (per-campaign `.afb` graphs of action / condition /
  operator / effect nodes); ATT&CK group descriptions (free-text motivation
  attribution).
- **Outputs.** The same artefacts, materialised under `docs/sources/` (gitignored;
  read-only verification target). No transformation at this stage.
- **Transformation.** None. L0 is the corpus boundary.
- **Validation.** The corpus is reproducible from MITRE/CTID releases by
  version; the architecture states the version pinned so the build is
  reproducible.

**Parser contract (`.afb` → L1-ready tuples).** The L0→L1 step needs a
parser that reads `.afb` files (Attack Flow's STIX-2.1-style JSON
serialisation) and yields, per file: action nodes (with `technique_id`),
condition nodes, operator nodes (`AND`/`OR`), and the directed edges between
them (`effect`, `on_true`, `on_false`). L1 aggregation consumes that tuple
stream, not the raw `.afb`. **In-tree status:** corpus location and parser
implementation are **unverified** as of 2026-05-27 — no `notebooks/attack-flow/`
directory exists on the current branch. The schema-version decision below
(and §(l) open question #1) remain open until the parser and corpus land
somewhere reachable.

**Decision — Attack Flow schema version is pinned and documented explicitly.**
**Why:** Attack Flow v3.2.0 is the current MITRE/CTID release (8 Jul 2025),
but the codebase forked earlier may carry a v2.x corpus under
`notebooks/attack-flow/`. The GAP construction depends on which `.afb`
generation's fields are parsed (actions / conditions / operators / effect-edges
shifted between v2 and v3). Until verified in-tree, this is an open
build-time decision recorded here (see *Methodology Carry-Forward* §3).
**If revisited:** Migrating to v3.2.0 mid-thesis means rerunning GAP
construction; if the field deltas don't touch the parsed subset, document the
delta and stay on v2.x.

---

## (d) L1 — GAP (Generalised APT Profile)

**Status:** partially built (v0.4 implementation exists; design intent fixed,
parameterisation tunable).

**GAP schema detail.** The data model, the four construction decisions (made
2026-05-27 with Marc), and the build method live in
[`01_gap_schema.md`](01_gap_schema.md). That spec **supersedes the aggregation
sketch in this section**: GAP edges are Attack-Flow-only (FP-Growth
co-occurrence and ontology-regex dropped), the artefact is lossless, and
support / confidence / consensus / acyclicity become *views* rather than
build-time bakes. Reconciling this section's prose to that spec is Pass-2 work.

- **Inputs.** L0 corpus.
- **Outputs.** A single aggregated directed graph: nodes = ATT&CK techniques;
  edges = inter-technique dependencies inferred from the Attack Flow corpus.
  Edge metadata records support / confidence per the aggregation method
  (consensus, backward, etc.). Persisted as a serialised graph object plus
  an HTML visualisation artefact.
- **Transformation.** Edge extraction from per-campaign Attack Flow graphs,
  followed by aggregation across campaigns with minimum-support and
  minimum-confidence thresholds. Specific parameters (`min_support`,
  `min_confidence`, which aggregation modes are enabled) are
  implementation-tunable; the design does not commit to specific values.
- **Validation.** The graph is sane if (i) it contains the techniques expected
  from the corpus, (ii) edge counts roughly track campaign coverage, and
  (iii) the resulting subgraphs at L2 are non-trivially navigable. Threshold
  sensitivity is itself a methodology question — *not* a validation step.
- **Code location.** Built on this branch at
  [`../../src/mtdsim/l1_construction/`](../../src/mtdsim/l1_construction) (GAP
  v0.5; pipeline cross-walk in
  [`../../src/mtdsim/README.md`](../../src/mtdsim/README.md)). Self-contained —
  imports nothing from `mtdnetwork/`; the substrate integration (L3) is unpinned.
  The superseded v0.4 implementation is on `feat/attacker-profiling`.

**Decision — graph-driven traversal replaces the early-proposal "per-tactic
linear amplification" of the base attacker.**
**Why:** Linear amplification was a PoC scaffold that did not capture
behavioural dependency between techniques. Graph traversal of GASP is the
substantive operationalisation move.
**Cost:** No linear-amplification comparator survives at L4 — the procedural
6-phase baseline carries the only comparator role against the graph-driven
attacker.
**If revisited:** Reverting to amplification would collapse this work to a
parameter sweep over the inherited substrate — not a thesis-level
contribution.

**Decision — weighted GAP edges and per-technique parameter weights are
parked.**
**Why:** The unweighted graph is sufficient for the first comparative pass; the
weighted variant (with per-technique stealth / privilege / etc. weights
producing motivation-archetype adversaries) is an obvious extension that
clutters the MVP.
**If revisited:** Required if the comparative pass does not discriminate
across motivation profiles.

---

## (e) L2 — GASP (motivation-subgraphed APT Profile)

**Status:** partially built (terminal-node-ancestor proxy implemented; the
"true" motivation-attribution method is unfinalised).

- **Inputs.** L1 GAP; a **motivation specifier** drawn from the canonical
  set `{espionage, disruption, financial}` — three by default, matching the
  primary motivation categories surfaced across ATT&CK group descriptions.
  The set is **open**: an evaluation matrix may add a fourth (e.g.
  *hacktivism*) if a finding depends on it, but the L4 baseline factorial
  is currently scoped to these three. Pinning the L4 factorial shape is
  §(l) open question #6.
- **Outputs.** A motivation-conditioned subgraph of GAP: the techniques and
  edges relevant to the specified motivation.
- **Transformation.** Currently: identify terminal nodes (no outgoing edges)
  attributable to the motivation, then take the ancestor closure of those
  nodes in GAP. The design intent — *motivation-subgraphed* — is broader than
  this proxy.
- **Validation.** Subgraphs should differ across motivations in non-trivial
  ways (different technique populations, different ancestral structure). The
  subgraph must remain traversable end-to-end (a connected reachable region).
- **Code location.** Stub on this branch at
  [`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph) (scaffold +
  README; no implementation yet). The v0.4 terminal-node-ancestor proxy is prior
  art on `feat/attacker-profiling`, not ported.

**Decision — motivation attribution is implemented today as terminal-node
ancestor expansion; richer attribution (NLP over group descriptions,
group-mediated inference) is parked.**
**Why:** ATT&CK does not expose a clean "motivation" field. The terminal-node
proxy is honest about what it is — a structural surrogate for motivation —
and is sufficient to differentiate subgraphs in a comparative experiment.
**If revisited:** If the comparative pass shows motivation-by-attribution
matters more than motivation-by-terminal-node, swap in the NLP path; the L2
contract (graph in → subgraph out, motivation-parameterised) does not change.

---

## (f) L3 — OGASP (operationalised GASP)

**Status:** unbuilt (the substrate runs; the graph-driven attacker on top of it
does not yet exist).

- **Inputs.** L2 GASP; the MTDSim substrate (network, MTD scheduler, the
  inherited 6-phase attacker module).
- **Outputs.** Per-run attack records suitable for L4 evaluation —
  technique-level events along the GASP traversal, timed within the simulator.
- **Transformation.** The attacker agent traverses GASP within MTDSim, bridging
  technique → tactic → attacker action against the substrate's network and
  reacting to MTD events. The graph-driven attacker runs *alongside* the
  inherited 6-phase attacker, which is retained as the procedural baseline
  (per [`project_context.md`](project_context.md) L17). Both must work; both must
  be internally consistent against the substrate's invariants.
- **Validation.** Internal consistency against the substrate's invariants
  ([`mtdsim_spec.md`](mtdsim_spec.md) row-level dispositions); 6-phase baseline
  reproduces the post-2c golden ([`../../baseline/golden/`](../../baseline/golden/));
  graph-driven traversal produces non-degenerate attack records on a GASP it
  is given.
- **Code location.** Inherited 6-phase attacker is at
  [`mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  (the `Adversary` class) and
  [`mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  (the SimPy process driver). The graph-driven attacker is **unbuilt**; the
  design intent is that it lives alongside `Adversary` in the same module —
  selection is per-run, not via inheritance. The pipeline tree marks this seam
  at [`../../src/mtdsim/l3_simulation/`](../../src/mtdsim/l3_simulation) (a
  pointer only; holds no code).

**Decision — graph-driven attacker is added alongside the 6-phase attacker,
not replacing it.**
**Why:** The 6-phase attacker is the substrate Tay's RL trained against and the
basis of every golden; ripping it out forfeits the procedural baseline against
which behavioural-fidelity is compared. The comparative claim of the thesis
*requires* both to coexist on the same substrate.
**If revisited:** Removing the 6-phase attacker would force a re-baseline of
every Tay-comparison run and is not justified by any current finding.

**Decision — encoding of Jalowski et al.'s three attacker-model primitives
(*Methodology Carry-Forward* §1) is pending and documented as such.**
The three primitives are:

1. **State-collision recognition (cross-target memory).** Does the attacker
   maintain a memory of compromised configurations across the target
   population and recognise post-shuffle state collisions?
2. **Defender-behaviour conditioning (MTD-event-as-beacon).** Does the
   attacker condition action selection on observed defender frequency,
   treating MTD events as a target-criticality signal?
3. **Side-channel / metadata-invariance recognition.** Does the attacker's
   observation include invariant-feature extraction from network metadata
   (what does *not* change when the attack surface does), or is observation
   CVE/CVSS-only?

**Why this is the explicit list:** these primitives operationalise what
"behaviourally-grounded" *means* concretely — without one or more of them, the
phrase is hand-wavy. The encoded subset bounds the contribution. The validation
claim is *"behavioural fidelity changes the answer"*, not *"the attacker
model is true"* (see §(j)).
**If revisited:** Each primitive can be promoted from *pending* to *encoded*
or *out of scope* independently; promotion changes the L3 contract and the
attacker state space, not L1/L2 graph construction.

**Decision — Petri-net (SNAKES) formalisation is positioned as a candidate
alternative analytical substrate, not as a step inside L1/L2.**
**Why:** The pre-lit-review *Current State* listed it under Stream A
(profile construction); the *Methodology Carry-Forward* clarified it is a
*separate* workstream. Architecturally, a Petri-net encoding of GASP would
sit *parallel* to MTDSim/DES execution as an alternative substrate for L4
analytical evaluation — not inside L1/L2.
**If revisited:** If Petri-net evaluation matures, L4 acquires a second
substrate column and the comparability boundary at §(j) is extended.

**Note on the Tay-IDS ↔ Jalowski-beacon inverse** (*Methodology Carry-Forward*
§2). Tay's IDS-sensitivity experiment varies what the *defender* observes
about the attacker; Jalowski's beacon-conditioning primitive is what the
*attacker* infers from the defender's behaviour. If primitive (2) above is
encoded, this is the natural positioning move against Tay's substrate. Not
load-bearing for the scaffold; explicit in case Pass 2 picks it up.

---

## (g) L4 — Evaluation

**Status:** partially built (substrate runs and produces metrics; behavioural-
attacker runs not yet possible because L3 is unbuilt).

- **Inputs.** Per-run attack records from L3 (across MTD mechanism × attacker
  profile × MTD interval); the post-2c golden as the behavioural oracle.
- **Outputs.** Comparative effectiveness measures across attacker profiles,
  MTD mechanisms, and MTD intervals. Primary metric: **internal MTTC** per
  [`metrics_semantics.md`](metrics_semantics.md). Secondary: ASR, attack-path
  exposure, RoA (per [`project_context.md`](project_context.md) L19).
- **Transformation.** Run MTDSim across the experiment matrix; aggregate per
  (mechanism, profile, interval); report deltas against the 6-phase procedural
  baseline.
- **Validation.** Within-substrate comparison is valid; cross-paper numeric
  comparison to Zhang/Tay is *not* valid
  ([`project_context.md`](project_context.md) L20;
  [`metrics_semantics.md`](metrics_semantics.md) §d). The E1 finding from Phase 3
  applies: end-of-sim compromise fraction is a poor discriminator at long
  horizons — MTTC / attacker-effort discriminate.
- **Code location.** The metrics pipeline is inherited substrate
  ([`mtdnetwork/statistic/`](../../mtdnetwork/statistic)); the pipeline tree
  marks this seam at
  [`../../src/mtdsim/l4_evaluation/`](../../src/mtdsim/l4_evaluation) (a pointer
  only; holds no code).

**Decision — one canonical substrate; the `internal`/`lineage` preset was
evaluated and dropped.**
**Why:** Post-C6→0.8, the preset split would have distinguished only MTD
durations plus two unimplemented behaviours — not enough to justify the
maintenance cost. Recorded in [`project_context.md`](project_context.md) L20 and
[`metrics_semantics.md`](metrics_semantics.md).
**If revisited:** Resurrecting the preset would mean re-introducing
maintained divergence-flags in the substrate — large reverse-step.

**Decision — primary discriminator is internal MTTC, not end-of-sim compromise
fraction.**
**Why:** Phase 3 E1 finding: at long horizons, every MTD eventually loses on
ASR/compromise; MTTC and attacker-effort separate mechanisms.
**If revisited:** Only if a shorter-horizon evaluation produces stable
ASR signal across the experiment matrix.

---

## (h) Glossary

- **CTI** — cyber threat intelligence. The raw input class at L0.
- **ATT&CK** — MITRE ATT&CK technique knowledge base. Node namespace at L1+.
- **Attack Flow** — MITRE CTID corpus of per-campaign action-condition-operator
  graphs. Edge-source at L1.
- **GAP** — *Generalised APT Profile*. The L1 aggregated graph.
- **GASP** — *Motivation-subgraphed APT Profile*. The L2 motivation-conditioned
  subgraph of GAP.
- **OGASP** — *Operationalised GASP*. The L3 attacker-agent traversal of GASP
  within MTDSim.
- **Motivation profile** — a categorical specifier (*espionage* / *disruption*
  / *financial*, …) parameterising the L1→L2 subgraphing step.
- **Behaviourally-grounded attacker** — an attacker whose behaviour is shaped
  by CTI-derived structure (the GASP traversal), as opposed to a *procedural*
  attacker whose phase order and parameters are fixed in code.
- **Procedural attacker / 6-phase attacker** — the inherited substrate
  attacker; six scripted phases per [`mtdsim_spec.md`](mtdsim_spec.md). Retained
  as the comparison baseline against the behaviourally-grounded attacker.
- **MTD mechanism family — SDR** — shuffle / diversity / redundancy, the
  canonical MTD taxonomy (Cho 2020 §III-B / Hong 2018; see
  [`../extractions/cho2020.md`](../extractions/cho2020.md)). The three
  primitives are complementary rather than partitioned:
  - **Shuffling** — rearranges or randomises existing components (IP
    mutation, port hopping, topology reconfiguration), invalidating
    reconnaissance the attacker has already done.
  - **Diversity** — deploys different implementations of the same function,
    so that an exploit against one variant is unlikely to apply to others.
  - **Redundancy** — replicates components to preserve service while
    shuffling/diversity operate.
  The defence pool evaluated in this work draws from the SDR-family classes
  in [`mtdsim_spec.md`](mtdsim_spec.md) MTD-01–MTD-09, alongside Tay's
  AI-driven selection.
- **DES** — discrete-event simulation. The MTDSim execution paradigm.
- **GSM** — graph-structural model (e.g. HARM, T-HARM). The structural model
  on top of which DES executes in this lineage.
- **Internal MTTC, ASR, attack-path exposure, RoA** — primary L4 metrics. See
  [`metrics_semantics.md`](metrics_semantics.md) for internal MTTC's exact
  definition; the others' definitions live alongside it in the substrate spec.

---

## (i) Substrate seam map

The architecture plugs into MTDSim at one load-bearing seam — **the attacker
module**.

| Substrate region | What happens here | Position in this work |
|---|---|---|
| Network model | Topology, hosts, services, vulnerabilities | **Left alone.** Generic by design (no thesis-specific topology). The substrate's current defaults (`50/5/4/8`) **diverge** from Brown's headline `200/20/5/20` — see [`mtdsim_spec.md`](mtdsim_spec.md) NET-04 / NET-05. "Generic" here means "not thesis-tuned", not "Brown-faithful". |
| MTD scheduler | When MTD events fire, on which targets | **Left alone.** Existing schemes are the comparison axis at L4. |
| MTD mechanism pool | SDR family + Tay's AI selection | **Left alone.** Existing mechanisms only; this is the defender side and is frozen by scope. |
| **Attacker module** | Phase progression, action selection, state | **The seam.** Graph-driven (GASP) traversal added *alongside* the inherited 6-phase attacker. Both coexist; selection is per-run. |
| Metrics pipeline | MTTC, ASR, etc. per run | **Left alone.** Per [`metrics_semantics.md`](metrics_semantics.md). |
| RL benchmark (Tay) | Detection + RL-based MTD selection | **Left alone — deferred to eval phase.** Reused as benchmark defence, not extended. |

The "left alone" rows are the inherited substrate; the row description here is
a placeholder, not a re-spec — read [`mtdsim_spec.md`](mtdsim_spec.md) for the
authoritative description.

**Decision — the inherited HARM-structural + DES-execution composition is
treated as a deliberate choice, not a default.**
**Why:** Cho's four MTD evaluation methods (analytical / simulation /
emulation / real testbed) name *components* the current GSM-MTD literature
composes (graph-structural model executed via DES), not mutually exclusive
alternatives (*Methodology Carry-Forward* §4). This work inherits that
composition deliberately; alternatives (analytical Petri-net at L4,
emulation via Caldera) are scoped out as discussed in §(a) and §(f).
**If revisited:** A move to analytical Petri-net at L4 would alter the
substrate column at L4, not the seam at L3.

---

## (j) Methodological positioning *(Pass 1 — two paragraphs; flesh in Pass 2 against [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md))*

Prior literature independently provides (a) CTI-grounded attack profiling,
(b) attack-graph operationalisation in simulation, and (c) MTD evaluation
methodologies. The dominant MTD evaluation pattern — characterised across the
lineage Brown 2023 → Zhang 2023 → Ho 2024 → Tay 2024 ([`project_context.md`](project_context.md)
L27) — is *single-mechanism, single-network optimisation against procedurally-
scripted attackers*. Attacker fidelity sits at the bottom of the Pyramid of
Pain (hashes, IPs, artefacts) even though MTD's claimed defensive value extends
upward to TTPs. This work sits at the intersection of (a), (b), (c): a
behaviourally-grounded evaluation of *multiple* MTD mechanisms (SDR family +
AI-driven selection) against CTI-derived APT profiles, on a generic network
substrate. It varies the defence pool *and* the attacker behavioural model
while holding the substrate generic — directly addressing the two limitations
of the dominant pattern.

The defensible validation claim is **"behavioural fidelity changes the
answer"**, not **"the attacker model is true"** (*Methodology Carry-Forward*
§1, scoping note). MITRE ATT&CK Evaluations gives EDR-style ground truth, not
MTD-specific ground truth; without that, the contribution is a sensitivity
analysis bounded by the encoded Jalowski primitives (§(f)), not a fidelity
claim. The closest *published* methodological precedent is Rodríguez et al.
2024 (process mining over runtime telemetry → ATT&CK labels → process model);
this work differs along four axes — *input class* (curated CTI corpus vs
runtime telemetry), *temporal stance* (a-priori profile construction vs
post-hoc forensic discovery), *output use* (sampling-ready behavioural profile
driving MTD evaluation vs process model for forensic interpretation), and
*validation* (MTD sensitivity analysis in MTDSim vs PWNJUTSU/WannaCry case
studies). Stating these axes explicitly forestalls a "this is just process
mining" reading.

---

## (k) Validation strategy

The system is validated end-to-end when:

1. **L1 reproducibility.** GAP construction reruns from the pinned Attack Flow
   schema generation and yields the same graph (modulo aggregation thresholds,
   which are tunable). Threshold sensitivity is itself a methodology question
   — scoped to a single later section, not a validation gate.
2. **L2 non-triviality.** Different motivation specifiers yield meaningfully
   different subgraphs (different technique populations, different ancestral
   structure). A motivation specifier that produces a near-empty or near-full
   subgraph is a construction failure, not a finding.
3. **L3 substrate consistency.** Both attackers (6-phase, graph-driven)
   produce attack records that respect every row in
   [`mtdsim_spec.md`](mtdsim_spec.md). The 6-phase attacker reproduces the
   post-2c golden bit-for-bit (SIM-05 determinism;
   [`../../baseline/golden/`](../../baseline/golden/)). The graph-driven attacker
   produces non-degenerate, terminating runs against a non-empty GASP.
4. **L4 within-substrate comparability.** All comparisons are within this
   substrate. Cross-paper numeric comparison to Zhang/Tay is **invalid**
   (per [`metrics_semantics.md`](metrics_semantics.md) §d and
   [`project_context.md`](project_context.md) L20). The primary discriminator is
   internal MTTC; ASR/RoA/path-exposure are reported but secondary.
5. **Scoped contribution claim.** The thesis-level claim is bounded to
   sensitivity analysis — *the answer changes when the attacker is
   behaviourally grounded* — over the encoded subset of Jalowski primitives
   (§(f)). Anything stronger requires MTD-specific ground truth, which is
   not available in any current corpus.

---

## (l) Open architectural questions

These are decisions the scaffold flags but does not close. They are *pending*
in the same sense as the §(f) Jalowski-primitives block — surfaced here for
Pass 2 / Marc to drive, not assumed-resolved.

- **Attack Flow schema version + parser entrypoint in-tree.** Pinning is
  blocked until the corpus and parser materialise somewhere reachable;
  see §(c) Decision-block + Parser-contract for the current open state.
  → [`01_gap_schema.md`](01_gap_schema.md) §(f)/§(h) pins the parser on the STIX
  export (sidestepping the `.afb` version delta); the version pin itself stays open.
- **Which Jalowski primitives does the attacker model encode** (state
  collision / beacon conditioning / metadata invariance)? Each is independent.
- **L1 aggregation parameter choice** (`min_support`, `min_confidence`,
  consensus / backward / forward edge modes). Architecture commits only to the
  *form*; the values are tunable. → **Resolved for the GAP stage** by
  [`01_gap_schema.md`](01_gap_schema.md): Attack-Flow-only edges (co-occurrence
  dropped), lossless artefact, thresholds / acyclicity as downstream views.
- **Motivation-attribution method.** Terminal-node-ancestor proxy today;
  NLP/group-mediated inference parked. Which lands in the final evaluation?
- **Network substrate generality.** Held generic by intent — but does the RQ
  require parametric variation across topologies, or is one canonical
  network sufficient? §(a) and §(i) currently say *one*, generic; revisit
  if findings depend on topology.
- **L4 evaluation matrix shape.** MTD mechanism × attacker profile × MTD
  interval — what is the exact factorial? Pass 2 should pin this against the
  lit review's gap framing.

---

## (m) Related specs

- [`project_context.md`](project_context.md) — thesis-level direction; the
  one-line L0→L4 pipeline this file expands.
- [`mtdsim_spec.md`](mtdsim_spec.md) — substrate row-level dispositions.
- [`metrics_semantics.md`](metrics_semantics.md) — internal MTTC and the
  comparability boundary.
- [`provenance.md`](provenance.md) — load-bearing constants and rules
  cross-linked to source / code / disposition.
- [`guardrails.md`](guardrails.md) — non-negotiables (branch, scope,
  fair-use).
- [`session_workflow.md`](session_workflow.md) — stage-commit / handoff
  lifecycle.
- [`repo_conventions.md`](repo_conventions.md) — docs tree layout.
- [`../extractions/`](../extractions/) — per-paper extracts. Lineage four
  (Brown, Zhang, Ho, Tay) are locked; the adjacent-paper extractions
  cited from this spec — including the §IV-B fidelity-descriptor anchors
  ([`../extractions/cho2020.md`](../extractions/cho2020.md),
  [`../extractions/bianco2013.md`](../extractions/bianco2013.md)),
  the L3 primitives source
  ([`../extractions/jalowski2026.md`](../extractions/jalowski2026.md)),
  the L0 substrate spec
  ([`../extractions/attackflow.md`](../extractions/attackflow.md)),
  and the framing-closest paper
  ([`../extractions/ferraz2024.md`](../extractions/ferraz2024.md)) —
  are deep-fleshed and citable from §(j) Pass 2.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) — Marc's lit review,
  gitignored; primary input to Pass 2's §(j) flesh-out.
