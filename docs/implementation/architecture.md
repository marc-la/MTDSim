---
status: durable
created: 2026-05-27
updated: 2026-08-06
---

# Architecture — L0→L4 pipeline and methodological positioning

**Status:** Pass 1 scaffold (drafted 2026-05-27 from the pre-lit-review *Current
State* doc and the *Methodology Carry-Forward* note, both pasted-only). The
skeleton, decisions log, and substrate seam are in place; methodological
positioning will be fleshed against [`../sources/LIT_REVIEW.md`](../sources/lit_review/LIT_REVIEW.md) in Pass 2.
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
Generalised APT Profile), operational-objective-subgraphing (L2, **GASP** —
operational-objective-subgraphed APT Profile, per
[`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md)), and operationalisation inside MTDSim
(L3, **OGASP** — Operationalised GASP), to comparative effectiveness
measurement (L4). The §(h) glossary carries full definitions.

The substrate is the inherited MTDSimTime fork ([`mtdsim_spec.md`](mtdsim_spec.md));
the load-bearing seam is the **attacker module**, where graph-driven traversal
is added *alongside* — not replacing — the inherited 6-phase scripted attacker
(per [`project_context.md`](../workflows/project_context.md) L17). The defender side is
deliberately frozen: SDR-family mechanisms + Tay's AI selection, no novel
defender innovation and no novel RL training.

The single research question is *"how do existing MTD mechanisms perform against
behaviourally-grounded adversarial profiles derived from CTI?"* — a comparative
question over (MTD family × attacker profile) on a single canonical substrate.

**Decision — single RQ, no sub-problems.**
**Why:** All previously-considered sub-questions resolved to either methodology
positioning (chapter 3 material) or empirical splits of the same comparative
claim; neither warrants RQ-level promotion. Aligns with
[`project_context.md`](../workflows/project_context.md) L9.
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
[`project_context.md`](../workflows/project_context.md) L10 and [`docs_map.md`](../workflows/docs_map.md)).
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
 Campaigns                              operational           in MTDSim          across attacker profiles
 Attack Flow         techniques        objective              graph-driven       MTTC | ASR
 corpus              + edges           (audit-traced;         attacker traversal | attack-path exposure
 ATT&CK group        (consensus,        surface subgraph)     + inherited 6-phase| RoA
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
[`01_gap_schema.md`](pipeline/gap/gap_schema.md). That spec **supersedes the aggregation
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

## (e) L2 — GASP (operational-objective-subgraphed APT Profile)

**Status:** built. The data model and the five construction decisions live
in [`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md); the L2 builder is at
[`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph); this section
is the architecture-level summary.

- **Inputs.** L1 GAP; an **operational-objective specifier** drawn from the
  canonical set `{objective_exfiltration, objective_impact,
  objective_exfiltration_impact, objective_none_c2}`. The class set is
  empirically derived from a 38-flow audit-traced corpus
  ([`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(b) Decision 2) — a refinement
  of Alshamrani's 3-goal NIST taxonomy that names double extortion
  explicitly and declines Alshamrani's *position_for_future* because the
  corpus contains zero surveillance flows. The set is closed
  for v0.5; corpus growth may promote it. The labels name each class's
  **declared objective tactic** (`OBJECTIVE_TACTICS`), never a selection
  filter — membership is analyst-stated, per the §(a) central invariant; the
  three-vocabulary crosswalk is in
  [`gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(c).
- **Outputs.** An operational-objective-conditioned subgraph of GAP — the
  techniques (surface) and edges drawn by analysts in flows assigned to the
  specified class. Boundary object: `SubgraphView` (`class_name`,
  `node_set`, `edge_set`, `provenance`).
- **Transformation.** Take the **surface subgraph** — techniques actually
  present in the class's flows, GAP edges where both endpoints are in the
  union. Class membership is sourced from the audit-traced CSV at
  [`../notes/2026-05-28_l2_metadata_audit.csv`](../../data/gasp/metadata_audit.csv),
  *not* from graph-structural terminal-node detection. The CSV is the
  load-bearing input; the no-synthesis invariant
  ([`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(a)) refuses synthesised class
  memberships in exactly the way the L1 GAP refuses synthesised edges.
- **Validation.** Subgraphs differ across operational-objectives at the
  technique-frequency level (mean pairwise JSD 0.317 vs null p95 0.148, all
  six class pairs in 0.284–0.351). The operator-deduplicated re-check
  ([`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(g)) runs as a test gate over
  the L2 build and the signal survives null p95 on the n=29 deduplicated
  corpus — the per-class behaviour is operator-robust at the corpus level.
  Simulator-level discrimination is L3/L4-scoped, not L2.
- **Code location.** Built on this branch at
  [`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph); outputs
  at [`../../data/gasp/`](../../data/gasp/) (classification CSV +
  per-class `SubgraphView` JSONs). The v0.4 terminal-node-ancestor proxy
  on `feat/attacker-profiling` / `feat/replay-viz` is not ported.

**Decision — the L2 slice axis is operational objective, not motivation.**
**Why:** Motivation (espionage / financial / disruption) is rarely written
down in structured CTI; STIX `primary_motivation` is empty across all 187
ATT&CK groups and all 52 ATT&CK campaigns (verified 2026-04-16). Operational
objective — what the operation *did* by the analyst-stated narrative — is
observable directly from CTI text, sidestepping inference. Alshamrani 2019
([`../extractions/alshamrani2019.md`](../sources/extractions/alshamrani2019.md))
locates objective-conditioned behavioural divergence at APT phases 3–5,
which is where it matters for an MTD evaluation. Detail in
[`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(b) Decision 1.
**If revisited:** If a corpus emerges with structured motivation attribution
(STIX `primary_motivation` populated), motivation re-enters as a comparable
axis; the GASP would then carry both.

**Decision — class membership is sourced from analyst-stated narrative
(audit-traced metadata attestation), not from GAP graph structure.**
**Why:** Graph-structural terminal-node detection (the dropped P1 candidate)
agrees with the audit on only 23 of 38 flows (61 %). The 40 % disagreement
is systematic: *truncated breach reports* (Equifax, JP Morgan, Marriott,
etc.) where the analyst stopped drawing before the exfiltration step
appeared as a structural terminal. Sourcing membership from CTI narrative
resolves the truncation pattern correctly. Per-flow defence in
[`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(b) Decision 3 and
[`../notes/2026-05-28_l2_per_flow_justifications.md`](pipeline/gasp/per_flow_justifications.md).
**If revisited:** If a corpus expansion or simulator-driven discrimination
step reveals operator-aggregation is dominating per-class discrimination
(e.g. the `objective_exfiltration_impact` class's signal is *the Conti signature* rather
than a *double-extortion signature*), re-open the spec against the four
mitigations in
[`../notes/2026-05-28_l2_operator_aggregation_concern.md`](../notes/ch4_methods/operator_concentration.md)
(operator-deduplicated re-check / operator-weighted JSD / stratified holdout
/ corpus expansion).

---

## (f) L3 — OGASP (operationalised GASP)

**Status:** built end-to-end (first result on record). The structural nets,
weights, durations and the standalone timeline runner are shipped; the
**feedback-coupled profiled attacker is built and green** (commit `48471b8`),
verified against the runtime model before use
([`pipeline/ogasp/runtime_verification.md`](pipeline/ogasp/runtime_verification.md)),
and **experiment 1 has run** — the profiled attacker reaches the substrate
objective in 0/100 runs against a 0.90–1.00 baseline, failing through
substrate-precondition friction and non-spreading churn
([`pipeline/ogasp/experiment_01_findings.md`](pipeline/ogasp/experiment_01_findings.md)).
*The baseline magnitude is stale as a comparison target:* the seven-defect
repair (`dd8c5ec`) and the deliberate re-baseline that followed it (`06ed8d9`)
landed after experiment 1's numbers were taken, and on the current substrate
the baseline reaches the objective 0/10 under random MTD at 200 s where
experiment 1 recorded 10/10
([`pipeline/ogasp/rate_feasibility_study.md`](pipeline/ogasp/rate_feasibility_study.md)
§6). The findings stand; any new comparison re-measures the baseline in the
same run.
The post-experiment-1 rulings **S1–S6** allocate the response and are the live
work; refinement, not construction, is what remains.

### The runtime stack — movement / controller / action / substrate

The L0–L4 numbering above is a **build-time data-flow** view: how the
attacker's behavioural artefacts are *constructed*. The vocabulary the
supervisor update ratified (2026-07-21) is a **runtime execution** view: how
the profiled attacker *runs*. They are two views of one system, not competing
numberings — GAP and GASP are the movement layer's provenance, not separate
runtime components, and the substrate is deliberately **not** renumbered "L5"
(evaluation at L4 consumes runs *on* the substrate; placing a runtime component
downstream of evaluation muddles the data-flow reading).

| Runtime layer | What it owns | Built from |
|---|---|---|
| **Movement layer** | which moves are legal and their base proportions — everything from the CTI (Attack Flow) through to the attack profiles (the Petri nets), plus the synthetic pre-intrusion structure composed in at net-build | L0 → L3a |
| **Controller layer** | the mapping/join between the movement layer and the simulator: which verb a tactic dispatches, and how a returned verdict re-weights the next move. **The application layer the experiments vary** | M5 → the controller reframe (2026-07-22), S4 |
| **Action layer** | the outcome oracle — the predefined attack behaviour inherited from MTDSim: the six verbs, their native time costs, their own dice, no succession | inherited; anatomised in [`pipeline/ogasp/action_layer_anatomy.md`](pipeline/ogasp/action_layer_anatomy.md) |
| **Substrate** | network / host / service / vulnerability terrain, MTD mechanisms, statistics — unchanged (D5) | inherited; [`mtdsim_spec.md`](mtdsim_spec.md) |

**Decision — overlay the runtime vocabulary, do not renumber the pipeline.**
**Why:** the two views answer different questions and both are load-bearing;
renumbering to make one subsume the other would touch data directories
(`data/gap|gasp|ogasp`), code paths (`l3_simulation`) and every chapter note
that says "L3", for a nominal gain.
**Cost:** two vocabularies coexist, so any document using either must say which
view it is in.
**If revisited:** a renumber is separate, sequenced work — the rename, not the
decision, is the expensive part.

**Working-layer ledger** (the terms the 2026-07-03 handoff chain uses):
- **L3a** — the structural nets *plus their parameterisation*: flow-proportion
  transition weights (D3; disposition in
  [`metrics_semantics.md`](metrics_semantics.md) §(f)) and the per-tactic
  duration catalogue (D4; regime row in [`provenance.md`](provenance.md)).
- **Timeline generation** — standalone net execution: seeded single-token
  walks over the weighted nets emitting timed attacker-state sequences.
  Post-M1 this is the **analytical track only** (D1's standalone half), not
  the MTDSim input.
- **Coupling** — the MTDSim join: the net runs live inside the simulation
  (M1); a tactic→action influence map dispatches existing substrate actions
  (M5); the substrate's binary attack outcome feeds back as conditional
  transition-weight sets (M2), with direction from a kill-chain mapping (M3).
  *(Formerly "binding / replay" — the one-way timeline-replay framing died
  with D2→M1.)*

- **Inputs.** L2 GASP; the MTDSim substrate (network, MTD scheduler, the
  inherited 6-phase attacker module).
- **Outputs.** Per-run attack records suitable for L4 evaluation —
  technique-level events along the GASP traversal, timed within the simulator.
- **Transformation.** Under the v1 coupling model (M1 decision block below):
  the weighted class net runs **live inside the simulation** — a single token
  occupies one tactic-place at a time; at each place the profiled attacker
  fires the mapped substrate action(s) (M5) against its current network
  position; the binary outcome selects the success or failure conditional
  weight set (M2) that governs the next transition, with forward/backward
  direction read off the kill-chain mapping (M3).
  The net-driven attacker runs *alongside* the
  inherited 6-phase attacker, which is retained as the procedural baseline
  (per [`project_context.md`](../workflows/project_context.md) L17). Both must work; both must
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
  (the SimPy process driver). The replay attacker is **unbuilt**; the
  design intent is that it lives alongside `Adversary` in the same module —
  selection is per-run, not via inheritance. The L3a Petri build code lives at
  [`../../src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri);
  outputs at [`../../data/ogasp/`](../../data/ogasp/).

**Decision — graph-driven attacker is added alongside the 6-phase attacker,
not replacing it.**
**Why:** The 6-phase attacker is the substrate Tay's RL trained against and the
basis of every golden; ripping it out forfeits the procedural baseline against
which behavioural-fidelity is compared. The comparative claim of the thesis
*requires* both to coexist on the same substrate.
**If revisited:** Removing the 6-phase attacker would force a re-baseline of
every Tay-comparison run and is not justified by any current finding.

**Decision — Jalowski et al.'s three attacker-model primitives
(*Methodology Carry-Forward* §1) are promoted from *pending* to *out of
scope* (Marc, 2026-07-28), superseding the earlier pending-encoding wording
of this block.** The three primitives are:

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
**Why out of scope:** encoding any of the three requires an inference
capability — machine learning or reinforcement learning over observed defender
behaviour — that the remaining timeframe cannot support building and
validating. The exclusion is capability-shaped, not substrate-shaped: the
observation channel primitive (2) would consume already exists and is unwired
(`Adversary.observed_changes`,
[`adversary.py:23`](../../mtdnetwork/component/adversary.py), is an empty
dictionary nothing in the repository reads or writes, and the substrate
already exposes per-event MTD records with resource layer and timing, a
computed mutation-execution frequency, the running and suspended mutations,
and cumulative interrupt counts from the adversary's live network handle —
[`mtd_statistics.py`](../../mtdnetwork/statistic/mtd_statistics.py)). Per-host
mutation counts are the one genuinely absent input: no MTD strategy keeps
per-target bookkeeping, so a beacon primitive would have to derive or
instrument them.
**Cost:** the encoded subset — which bounds the contribution by this block's
own argument — stays empty on this axis for the life of the project;
[`apt_model_criterion.md`](apt_model_criterion.md) §(d) axis 8 remains the
criterion's bluntest honest negative, now as a ruled exclusion rather than
unstarted work.
**Amended 2026-08-09 — the exclusion is no longer only a timeframe one.**
Jalowski's §4.3 metric-manipulation route (distinct from the three §4.1
primitives this block rules on) was designed, wired and closed on evidence:
triggering is clocked in every arm of the defence pool, so attacker behaviour
cannot influence *when* the defender deliberates; and the one defence that reads
attacker-derived metrics converges to constant-action policies that do not read
their state, with the static-degrade timer supplying almost every mutation in
the low-movement regime. Full reasoning and the caution against overclaiming
this as "the substrate is time-based MTD" are in
[`apt_model_criterion.md`](apt_model_criterion.md) axis 8, amendment 2026-08-09.
Building an event-triggered defender to make the axis assessable was declined
against the two decisions above (defence side is existing mechanisms only; IDS
is not a research thread).
**If revisited:** promotion to *encoded* changes the L3 contract and the
attacker state space, not L1/L2 graph construction — and it re-opens the S2
freeze's capability candidates, so it carries a fresh comparability argument
against the retained baseline.

**Decision — the Petri net is the primary behaviour source for the
executable attacker (supervisor D1, July 2026), superseding its earlier
positioning as a "candidate alternative analytical substrate".**
**Why:** The supervisor settled both tracks: "incorporate the petri net into
MTDSim so the attack behaviour is dictated by this", *and* examine the attack
behaviour the net generates on its own. The net-driven behaviour is the
substantive operationalisation move; the standalone examination (Monte-Carlo
over the timeline runner) delivers the analytical track without a second L4
substrate. The closed-form CTMC solve of the earlier analytical framing moves
to the deferred register. Decision register:
[`../notes/2026-07-03_supervisor_meeting_l3_decisions.md`](pipeline/ogasp/supervisor_decision_register.md).
**If revisited:** If a closed-form analytical evaluation is resurrected, L4
acquires a second substrate column and the comparability boundary at §(j) is
extended.

**Decision — v1 coupling is a live feedback-coupled net (supervisor M1/M2,
14 July 2026), superseding the one-way timeline replay (D2).**
**Why:** A pre-generated timeline cannot capture substrate feedback — an MTD
mutation that severs the attacker's foothold must throw the attacker's *state*
back, and a fixed sequence marches on regardless (the dead end Marc raised and
Jin confirmed). Instead the net is a live object inside the simulation: the
substrate's existing attack machinery is the **outcome oracle** ("fetch the
success outcome from the bottom"), and the binary outcome selects between
predefined success/failure transition-weight sets at the current place (M2),
directional per the kill-chain mapping (M3). This is the *minimal* two-way
form — conditional weights, not a capability precondition/effect contract —
and it keeps the substrate change attacker-only (D5): the new movement layer
calls the existing action machinery as an API (M7). The original D2 wording
is preserved in the decision register, annotated; the timeline library it
produced survives as the standalone analytical track (D1).
**Deferred (D10 register, as at 2026-07-27):** the full capability
precondition/effect contract, evasion/detection-rate modelling, aggregated
cross-profile variation analysis, the closed-form CTMC solve, richer-than-
binary outcome classes (M2), an attacker that studies the MTD (M8d), and
attacker-state-conditioned *dynamic* transition weights (S1's eventual
direction). **Lifted since:** two-way integration (M1, built); **sensitivity
analysis on the weights** (S1); **timed-net firing semantics** (S3 — per-tactic
exponential firing on the movement layer, with dwell-only tactics consuming
time and the MTD confusion penalty replicated as a net place).
**If revisited:** Reverting to one-way replay resurrects the shipped timeline
contract (`ogasp-timeline/v1`) as the coupling input; the feedback loop is
strictly additive on top of it, so the fallback is cheap.

**Decision — the attacker action set is frozen short-term (supervisor S2,
21 July 2026).** No attacker action, ability, or attacker state is added,
removed, or altered; only refinement of existing code and bug fixes are
licensed.
**Why:** experiment 1's failure modes are attributable to two things that are
separable — the inherited phases' tight integration (a substrate property) and
the deliberately coarse tactic→verb collapse (a controller parameter). Changing
the action set while both are in play would confound which one the numbers are
measuring.
**Cost:** the tactics with no substrate capability stay uncovered, so the
controller cannot be made *complete* — only *sensible* (S4 turns that from a
defect into a modelling stance: dwell-only tactics).
**If revisited:** lifting the freeze re-opens the update's capability
candidates (an evasion action, a tooling endowment, a privilege level, a
durability parameter) as design work, and requires a fresh comparability
argument against the retained baseline.

**Note on the Tay-IDS ↔ Jalowski-beacon inverse** (*Methodology Carry-Forward*
§2). Tay's IDS-sensitivity experiment varies what the *defender* observes
about the attacker; Jalowski's beacon-conditioning primitive is what the
*attacker* infers from the defender's behaviour. With primitive (2) now ruled
out of scope, this positioning move is future work rather than a live option;
recorded because it is the natural framing if the ruling is ever revisited.
Not load-bearing for the scaffold; explicit in case Pass 2 picks it up.

---

## (g) L4 — Evaluation

**Status:** partially built (substrate runs and produces metrics; the
behavioural attacker runs and has produced a first result — see §(f) — but the
matrix has covered only no-MTD vs one MTD scheme, so the mechanism-ranking
question the RQ turns on is not yet answered).

- **Inputs.** Per-run attack records from L3 (across MTD mechanism × attacker
  profile × MTD interval); the post-2c golden as the behavioural oracle.
- **Outputs.** Comparative effectiveness measures across attacker profiles,
  MTD mechanisms, and MTD intervals. Primary metric: **internal MTTC** per
  [`metrics_semantics.md`](metrics_semantics.md). Secondary: ASR, attack-path
  exposure, RoA (per [`project_context.md`](../workflows/project_context.md) L19).
- **Transformation.** Run MTDSim across the experiment matrix; aggregate per
  (mechanism, profile, interval); report deltas against the 6-phase procedural
  baseline.
- **Validation.** Within-substrate comparison is valid; cross-paper numeric
  comparison to Zhang/Tay is *not* valid
  ([`project_context.md`](../workflows/project_context.md) L20;
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
maintenance cost. Recorded in [`project_context.md`](../workflows/project_context.md) L20 and
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
- **GASP** — *Operational-objective-subgraphed APT Profile*. The L2
  operational-objective-conditioned subgraphs of GAP — four `SubgraphView`s,
  one per class `{objective_exfiltration, objective_impact, objective_exfiltration_impact,
  objective_none_c2}`, per [`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md). (The
  earlier "motivation-subgraphed" expansion is investigation-time
  terminology; the live axis is operational objective.)
- **OGASP** — *Operationalised GASP*. The L3 attacker-agent traversal of GASP
  within MTDSim.
- **Operational-objective profile** — a categorical specifier from
  `{objective_exfiltration, objective_impact, objective_exfiltration_impact, objective_none_c2}`
  parameterising the L1→L2 subgraphing step. (Supersedes the early
  "motivation profile" framing — see
  [`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(b) Decision 1.)
- **Behaviourally-grounded attacker** — an attacker whose behaviour is shaped
  by CTI-derived structure (the GASP traversal), as opposed to a *procedural*
  attacker whose phase order and parameters are fixed in code.
- **Procedural attacker / 6-phase attacker** — the inherited substrate
  attacker; six scripted phases per [`mtdsim_spec.md`](mtdsim_spec.md). Retained
  as the comparison baseline against the behaviourally-grounded attacker.
- **MTD mechanism family — SDR** — shuffle / diversity / redundancy, the
  canonical MTD taxonomy (Cho 2020 §III-B / Hong 2018; see
  [`../extractions/cho2020.md`](../sources/extractions/cho2020.md)). The three
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

## (j) Methodological positioning *(Pass 1 — two paragraphs; flesh in Pass 2 against [`../sources/LIT_REVIEW.md`](../sources/lit_review/LIT_REVIEW.md))*

Prior literature independently provides (a) CTI-grounded attack profiling,
(b) attack-graph operationalisation in simulation, and (c) MTD evaluation
methodologies. The dominant MTD evaluation pattern — characterised across the
lineage Brown 2023 → Zhang 2023 → Ho 2024 → Tay 2024 ([`project_context.md`](../workflows/project_context.md)
L27) — is *single-mechanism, single-network optimisation against procedurally-
scripted attackers*. Attacker fidelity sits at the bottom of the Pyramid of
Pain (hashes, IPs, artefacts) even though MTD's claimed defensive value extends
upward to TTPs. This work sits at the intersection of (a), (b), (c): a
behaviourally-grounded evaluation of *multiple* MTD mechanisms (SDR family +
AI-driven selection) against CTI-derived APT profiles, on a generic network
substrate. It varies the defence pool *and* the attacker behavioural model
while holding the substrate generic — directly addressing the two limitations
of the dominant pattern. *"Behaviourally-grounded" has a concrete mechanism
here:* each L2 class partition is audit-traced to analyst-stated operational
objective in the CTI narrative (CTID `example_flows/` blurb + ATT&CK
Group/Campaign page + vendor URL), with per-flow citations in
[`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(c) and
[`../notes/2026-05-28_l2_per_flow_justifications.md`](pipeline/gasp/per_flow_justifications.md) —
the mechanism is documented, not assumed.

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

**Envelope, not actor.** Each class net is a **behavioural envelope /
generative grammar for an operational objective** — the union of 5–19
analyst-drawn flows, over-generating by construction (a token can stitch
technique-A-from-one-campaign onto technique-B-from-another and produce a
chain no real actor ever ran; rationale in
[`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/ch4_methods/structure_to_behaviour_binding.md)
§1). *Commits to:* a run is *one instantiation* of the envelope under a
declared policy; the defensible claim is **fidelity-changes-the-answer over a
CTI-grounded envelope**. *Rules out:* claiming a traversal *is* a named
actor; reading the envelope MTTC as a real campaign's dwell time; reading
weighted paths as actor-likelihood. Every downstream claim is phrased
envelope-relative ("under the `objective_exfiltration` envelope…") — the one-liners in
[`metrics_semantics.md`](metrics_semantics.md) §(f) and
[`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(a) enforce the same reading at
their layers.

---

## (k) Validation strategy

The system is validated end-to-end when:

1. **L1 reproducibility.** GAP construction reruns from the pinned Attack Flow
   schema generation and yields the same graph (modulo aggregation thresholds,
   which are tunable). Threshold sensitivity is itself a methodology question
   — scoped to a single later section, not a validation gate.
2. **L2 non-triviality.** Different operational-objective specifiers yield
   meaningfully different subgraphs (different technique populations,
   different ancestral structure). An operational-objective specifier that
   produces a near-empty or near-full subgraph is a construction failure,
   not a finding. (Confirmed at corpus level by the JSD discrimination check
   in [`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(g); simulator-level
   confirmation is L3/L4-scoped.)
3. **L3 substrate consistency.** Both attackers (6-phase, graph-driven)
   produce attack records that respect every row in
   [`mtdsim_spec.md`](mtdsim_spec.md). The 6-phase attacker reproduces the
   post-2c golden bit-for-bit (SIM-05 determinism;
   [`../../baseline/golden/`](../../baseline/golden/)). The graph-driven attacker
   produces non-degenerate, terminating runs against a non-empty GASP.
4. **L4 within-substrate comparability.** All comparisons are within this
   substrate. Cross-paper numeric comparison to Zhang/Tay is **invalid**
   (per [`metrics_semantics.md`](metrics_semantics.md) §d and
   [`project_context.md`](../workflows/project_context.md) L20). The primary discriminator is
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
  → [`01_gap_schema.md`](pipeline/gap/gap_schema.md) §(f)/§(h) pins the parser on the STIX
  export (sidestepping the `.afb` version delta); the version pin itself stays open.
- **Which Jalowski primitives does the attacker model encode** (state
  collision / beacon conditioning / metadata invariance)? Each is independent.
- **L1 aggregation parameter choice** (`min_support`, `min_confidence`,
  consensus / backward / forward edge modes). Architecture commits only to the
  *form*; the values are tunable. → **Resolved for the GAP stage** by
  [`01_gap_schema.md`](pipeline/gap/gap_schema.md): Attack-Flow-only edges (co-occurrence
  dropped), lossless artefact, thresholds / acyclicity as downstream views.
- **Motivation-attribution method — RESOLVED** → see
  [`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md). Class membership is sourced from
  audit-traced metadata attestation (analyst-stated operational objective in
  the CTI narrative); the structural-terminal proxy is documented as the
  dropped P1 candidate. NLP/group-mediated inference remains parked but is
  no longer the parked *alternative to the structural proxy* — it would be
  an alternative to the audit-traced mechanism, with the operator-
  aggregation re-check ([`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(g)) as
  the natural decision point.
- **Network substrate generality.** Held generic by intent — but does the RQ
  require parametric variation across topologies, or is one canonical
  network sufficient? §(a) and §(i) currently say *one*, generic; revisit
  if findings depend on topology.
- **L4 evaluation matrix shape.** MTD mechanism × attacker profile × MTD
  interval — what is the exact factorial? Pass 2 should pin this against the
  lit review's gap framing. Experiment 1 ran a deliberate corner of it (no-MTD
  vs one scheme, ten seeds); the full SDR sweep is carried by the experiment-2
  handoff.
- **What this model captures that prior attacker models do not (S6).** The
  project's headline claim is currently argued in §(j) as positioning. The
  supervisor's direction is to convert it into a **structured criterion** built
  from the reviewed APT literature (Cho 2020's axes, Jalowski 2026's gap
  statement, Alshamrani 2019's enumeration) and to score this model against it
  honestly — including the axes it does not satisfy.
  → **Resolved 2026-07-27:** the criterion exists at
  [`apt_model_criterion.md`](apt_model_criterion.md) (eight axes, per-axis
  epistemic badges, experiment-1 scoring, M8b measurement recommendations) and
  sits on the every-session read-first list in [`CLAUDE.md`](../../CLAUDE.md).
  §(j)'s positioning now has its yardstick; re-score triggers live in that
  file's §(h).

---

## (m) Related specs

- [`project_context.md`](../workflows/project_context.md) — thesis-level direction; the
  one-line L0→L4 pipeline this file expands.
- [`01_gap_schema.md`](pipeline/gap/gap_schema.md) — L1 GAP data model and the six
  construction decisions; the detail under §(d).
- [`02_gasp_schema.md`](pipeline/gasp/gasp_schema.md) — L2 GASP data model and the
  five construction decisions; the detail under §(e).
- [`mtdsim_spec.md`](mtdsim_spec.md) — substrate row-level dispositions.
- [`metrics_semantics.md`](metrics_semantics.md) — internal MTTC and the
  comparability boundary.
- [`provenance.md`](provenance.md) — load-bearing constants and rules
  cross-linked to source / code / disposition.
- [`guardrails.md`](../workflows/guardrails.md) — non-negotiables (branch, scope,
  fair-use).
- [`session_workflow.md`](../workflows/session_workflow.md) — stage-commit / handoff
  lifecycle.
- [`docs_map.md`](../workflows/docs_map.md) — docs tree layout.
- [`../extractions/`](../sources/extractions/) — per-paper extracts. Lineage four
  (Brown, Zhang, Ho, Tay) are locked; the adjacent-paper extractions
  cited from this spec — including the §IV-B fidelity-descriptor anchors
  ([`../extractions/cho2020.md`](../sources/extractions/cho2020.md),
  [`../extractions/bianco2013.md`](../sources/extractions/bianco2013.md)),
  the L3 primitives source
  ([`../extractions/jalowski2026.md`](../sources/extractions/jalowski2026.md)),
  the L0 substrate spec
  ([`../extractions/attackflow.md`](../sources/extractions/attackflow.md)),
  and the framing-closest paper
  ([`../extractions/ferraz2024.md`](../sources/extractions/ferraz2024.md)) —
  are deep-fleshed and citable from §(j) Pass 2.
- [`../sources/LIT_REVIEW.md`](../sources/lit_review/LIT_REVIEW.md) — Marc's lit review,
  gitignored; primary input to Pass 2's §(j) flesh-out.
