---
status: open
created: 2026-05-28
---

# Step back from L2 and write down what it actually means — observation-grounded synthesis, not spec or design

L2 is built. The spec ([`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md))
records *what GASP is*; the investigation notes record *how the decision
was reached*; the audit outcome
([`../notes/2026-05-28_l2_assembly_audit.md`](../notes/2026-05-28_l2_assembly_audit.md))
records *whether the pieces hang together*. **What hasn't been written
down is the reflective pass** — a high-level read of what L2 has actually
*achieved*, what it *means*, what its strengths and limitations are, and
what it *implies* for L3/L4 design. That's this handoff.

This is **not a do-stuff session** in the usual sense. The output is a
note. The work is thinking + observing + synthesising, anchored in
specific artefacts. Marc is the audience and needs this for methodology
narrative (chapter 3 / 4 of the thesis), not as code.

## State of play

Everything load-bearing has landed:

- **Spec** at [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md)
  (canonical; 9 sections; five decisions).
- **Build** at [`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph)
  (`schema.py`, `selector.py`, `build.py`, `__main__.py`); test gate at
  [`../../tests/l2_subgraph/test_gasp.py`](../../tests/l2_subgraph/test_gasp.py).
- **Artefacts** at [`../../data/gasp/`](../../data/gasp/) (4× `SubgraphView`
  JSONs + `classification.csv` + `_viz/`).
- **Investigation notes** under [`../notes/`](../notes/): partition
  reasoning (why operational objective, not motivation),
  partition decision (the P6 verdict + rubric + JSD), per-flow
  justifications (the audit-traced classification of all 38 flows),
  operator-aggregation concern (the load-bearing caveat), and the audit
  outcome.
- **Architecture integration** — `architecture.md` §(e), §(j), §(l)
  reflect the operational-objective axis and the audit-trace mechanism.

What's **not** written down:
- A reflective pass on what L2's 19:8:6:5 class split means *as a
  finding*, not just a result.
- A clear-eyed limitations section that names what L2 *can't* defend, and
  what that means for what the thesis can claim.
- A synthesis of why the structural-vs-narrative pivot was load-bearing
  — and what that says about the broader CTI-data-as-evidence question.
- A forward-looking sketch of what L3 inherits from this state (without
  designing L3).

## Recommended approach

A **reading-then-writing session**, weighted heavily toward reading. The
goal is not to recapitulate the spec; it is to look at the spec, the
notes, the code, the subgraphs, the visualisations, and the corpus
itself, and write down what a clear-eyed reader *sees* across them.

The pattern to apply is **observation → synthesis**:

> *Observation:* the four class subgraphs range 39–98 surface nodes —
> `pure_steal` is 2.5× the size of `infrastructure_setup`. *Observation:*
> the L1 GAP has 124 nodes; `pure_steal` already touches 79 % of them.
> *Observation:* the JSD signal across class pairs is in the
> 0.284–0.351 range — modest, not stark. *Synthesis:* L2 has *not* found
> four crisply-separated attacker behaviours; it has found *operational-
> objective-conditioned weightings over a shared technique pool*. The
> classes share most of the GAP and diverge in *frequencies*, not in
> *what they use*. **Implication for L3**: an attacker agent
> parameterised by class would not differ in *which techniques are
> available* — it would differ in *which transitions are weighted high*.
> That is a different design problem than "four disjoint attack graphs".

The note should do this *many* times, across different observation
domains: code, data, viz, narrative.

### What domains to observe (suggestions, not a checklist)

- **The class subgraphs themselves.** Open the 4 JSONs. Look at node
  counts, edge counts, overlap. The class node sets are not disjoint by
  design (spec §(d)) — what does the actual overlap *look like*? Which
  techniques appear in all four classes (the "behavioural backbone")?
  Which appear in only one? What does that tell you about *where* the
  classes actually differ?
- **The visualisations** at
  [`../../data/gasp/_viz/`](../../data/gasp/_viz/). The 2×2 technique
  grid (`gasp_grid_technique.png`) and tactic-FSM grid
  (`gasp_grid_tactic_fsm.png`) are the cleanest cross-class read. The
  per-class technique panels at `obs ≥ 2` filter out the long tail —
  what remains is the *recurring* per-class workflow. The
  `double_extortion` panel losing its `impact` tactic at `obs ≥ 2` (per
  the partition-decision note's *Notable finding from the eyeball pass*)
  is a *finding* worth synthesising on. The comparison chart
  (`gasp_comparison.png`) shows tactic-share deltas — what stands out
  visually?
- **The 38 flows themselves.** Look at the audit CSV
  ([`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv))
  and the per-flow note. Patterns: half of `double_extortion` is Conti.
  Half of `pure_impediment` is wipers (Sandworm × 2 + Shamoon + Sony).
  All of `infrastructure_setup` is "evicted-before-mission" or CISA-403.
  The *audit-traced* mechanism is doing work the structural mechanism
  couldn't — and that gap is itself a finding about CTI data quality.
- **The structural-vs-narrative pivot.** P1 (structural-terminal) agrees
  with the audit on 23/38 flows (61 %). The 40 % disagreement is
  *truncated breach reports* (analyst stops drawing before exfil). This
  is not just a methodological choice — it is a *commentary on what
  Attack Flow corpora actually contain* relative to what the attacks
  *did*. Synthesise on that.
- **The corpus's thinness.** Per the GAP construction note
  ([`./2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)),
  88 % of GAP edges are single-observation. L2 inherits this. What
  generalisation can L2 plausibly claim, given that?
- **The two `low`-confidence non-CISA flows**
  (`mac_malware_steals_crypto`, `searchawesome_adware`) sit at the edges
  of the 4-class scheme. They are *honest* — the audit downgraded
  confidence rather than force a clean fit. Is this kind of edge case
  a *limit of the partition* or a *limit of the scheme*? What's the
  difference?
- **The operator-aggregation problem.** Per the dedicated note, three
  Conti flows dominate `double_extortion` (50 %). The operator-dedup
  JSD re-check survives null (audit-confirmed; deterministic now at
  null p95 = 0.1849), but the margin is thin. What does that tell you
  about whether the per-class behavioural claim is *operator-robust* or
  *operator-fragile*?
- **The "double_extortion" naming**. CrowdStrike / Mandiant / CISA
  vocabulary, not NIST. STIX's `attack-motivation-ov` spreads too thin;
  Alshamrani's 3-goal spreads too coarse. L2 ended up at *operational
  CTI vocabulary*, which is a stance worth stating explicitly.

### What synthesis to attempt

Pull these into 4–6 high-level findings. Examples of the *shape* of
finding (not the content — derive yours from the reading):

- *"L2 has surfaced a class structure the corpus *contains*, not a
  taxonomy the literature *imposes*."* — why this matters; what it
  costs (no standards-grounded names); what it buys (corpus-empirical
  legitimacy).
- *"The L2 partition is doing two jobs simultaneously: slicing the GAP
  for downstream traversal *and* exposing the CTI corpus's observational
  bias."* — and the latter may be more thesis-valuable than the former.
- *"The class subgraphs are not disjoint attacker variants; they are
  *weighted overlays* over a shared substrate."* — what this means for
  L3's attacker action-selection design.

### Forward-looking to L3 (informational context, not L3 design)

A sentence or two on what L2's state implies for L3, without
designing L3:
- L3 inherits a *graph plus an edge-frequency profile*, not four crisply
  disjoint graphs. Attacker traversal must consume both.
- The Jalowski primitives at `architecture.md` §(f) — state-collision
  recognition, defender-behaviour conditioning, side-channel /
  metadata invariance — encode *how* an attacker decides; L2 encodes
  *which* techniques are available + weighted. These are independent
  axes the L3 design will need to compose.
- Petri-net formalism at L4 (per `architecture.md` §(f)) would be a
  *parallel-not-primary* analytical substrate. L2's per-class node
  counts (39–98) exceed the primer's 10–20 tractability bound; if
  Petri-net promotes from parallel to primary, per-class slices (e.g. a
  hand-picked T1486 cone of 6 nodes inside `double_extortion`) would
  be the substrate, not the full class subgraph. Surface this as
  context, do not design it.
- The operator-aggregation question will resurface at L3/L4 — Mitigations
  2–4 in the operator-aggregation note (operator-weighted JSD,
  operator-stratified holdout, corpus expansion) are not L2 work but
  will need explicit positioning in the evaluation matrix.

### Alternatives considered

- *Skip the reflective pass; let the spec speak for itself.* Rejected —
  the spec is *what GASP is*, not *what it means*. A defence reader
  ("OK, so the four classes are operational objectives — *so what?*")
  needs the so-what spelled out somewhere. The thesis methodology
  chapter (chapter 3) will lean on this synthesis.
- *Defer to chapter-3 writing time.* Rejected — chapter 3 is months
  out; the L2 state is fresh now, observations have higher fidelity
  while the construction context is loaded. Reflective notes written
  cold lose precision.
- *Bundle into the audit outcome note.* Rejected — the audit is a
  PASS/FIX/DEFER checklist; reflection is qualitatively different
  output. Mixing them dilutes both.

## Validation gate

The session lands a reflective note at
`docs/notes/<YYYY-MM-DD>_l2_synthesis.md` (or similar) that:

1. **Reads as observation-grounded synthesis, not as a spec restatement.**
   The note should be readable by someone who has *not* read
   `02_gasp_schema.md`, but it should not *replace* it. The shape is
   "what does this all *mean*", not "what is GASP".
2. **References specific artefacts by path / line / number.** Each
   high-level finding traces back to concrete observations
   (`gasp_pure_steal.json` has 98 nodes; `gasp_grid_technique.png`
   shows X; `2026-05-28_l2_partition_decision.md` records Y). No
   ungrounded claims.
3. **Has 4–6 high-level synthesised findings**, not a long list of
   observations. The work is in the *synthesis* layer; observations are
   raw material.
4. **Names strengths and limitations explicitly.** What L2 *can*
   defend; what it *can't*. Honest about thinness, operator-aggregation,
   the two low-confidence honest-edge flows, the JSD margin.
5. **Forward-thinking to L3 is contextual, not design.** A few sentences
   on what L3 inherits, framed as *implications of L2's state*. No
   L3 architecture, no Petri-net specifics beyond noting the
   tractability bound and where the discussion lives.
6. **No new code, no spec edits, no refactors.** The single deliverable
   is the note.

Length target: substantive but contained. ~1500–2500 words is the right
shape. Less and the synthesis is thin; more and it has drifted into
spec or design.

## Hard constraints

- **Branch hygiene.** Dedicated session branch (e.g.
  `chore/l2-reflective-synthesis`). Never on `main`. No push without
  ask. Per [`../specs/session_workflow.md`](../specs/session_workflow.md).
- **Read-only against L2.** No edits to
  [`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph),
  [`../../data/gasp/`](../../data/gasp/), or
  [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md). If the
  reflection surfaces a spec gap, *flag it* — open a follow-up
  handoff, don't fix in this session.
- **No L3 design.** Forward-looking text is *informational context
  for the methodology chapter*, not architecture or code. If L3 design
  ideas surface, capture them as a side-list at the bottom of the note
  for a future L3-design handoff to consume — do not engineer them here.
- **No new literature claims.** The note can *reference* what's already
  in [`../extractions/`](../extractions/) (Alshamrani, Cho, Jalowski,
  Bianco, Ferraz) and [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md)
  — but do not add new lit findings. The reflection is on *L2's own
  state* read against *already-extracted lit*; reading new papers
  here is scope creep.
- **Single deliverable.** One note file. Not a multi-file restructure,
  not a notebook, not a spec amendment.

## Reading list

In order — read the *artefacts*, not just skim. The synthesis lives in
having looked carefully.

1. **The four class subgraphs themselves** —
   [`../../data/gasp/gasp_pure_steal.json`](../../data/gasp/gasp_pure_steal.json),
   [`gasp_pure_impediment.json`](../../data/gasp/gasp_pure_impediment.json),
   [`gasp_double_extortion.json`](../../data/gasp/gasp_double_extortion.json),
   [`gasp_infrastructure_setup.json`](../../data/gasp/gasp_infrastructure_setup.json).
   Skim sizes, look at overlap, pick a handful of techniques and check
   which classes they appear in.
2. **The visualisations** —
   [`../../data/gasp/_viz/gasp_grid_technique.png`](../../data/gasp/_viz/),
   `gasp_grid_tactic_fsm.png`, `gasp_comparison.png`, and the
   per-class `_obs1` diagnostic vs filtered panels. The grids are the
   cleanest cross-class read.
3. **The canonical spec** —
   [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md). Read
   for what L2 *is*, then close it. The synthesis is about what *that*
   means.
4. **The investigation notes** — in this order:
   - [`../notes/2026-05-28_l2_partition_reasoning.md`](../notes/2026-05-28_l2_partition_reasoning.md)
     for the framing (why L2 at all; why this axis).
   - [`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md)
     for the verdict (rubric + JSD + the *Notable finding from the
     eyeball pass*).
   - [`../notes/2026-05-28_l2_per_flow_justifications.md`](../notes/2026-05-28_l2_per_flow_justifications.md)
     for the audit-trace per-flow defence.
   - [`../notes/2026-05-28_l2_operator_aggregation_concern.md`](../notes/2026-05-28_l2_operator_aggregation_concern.md)
     for the load-bearing caveat.
   - [`../notes/2026-05-28_l2_assembly_audit.md`](../notes/2026-05-28_l2_assembly_audit.md)
     for what's resolved and what's deferred.
5. **Architecture context** —
   [`../specs/architecture.md`](../specs/architecture.md) §(a), §(e),
   §(f) (Jalowski primitives), §(j) (methodology), §(l) (open
   questions). §(e) was edited during the audit to include the
   operational-objective axis decision; that's the integration
   point to read carefully.
6. **L1 context (just enough)** —
   [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) §(a)–(d)
   (the lossless graph L2 sits on) and the *thin generalisation*
   finding in [`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)
   (88 % single-observation edges).
7. **The build code** —
   [`../../src/mtdsim/l2_subgraph/build.py`](../../src/mtdsim/l2_subgraph/build.py)
   and [`schema.py`](../../src/mtdsim/l2_subgraph/schema.py). Quick
   read for what the L2 builder actually does — the contract is small
   (`(gap, audit_csv, class_name) → SubgraphView`) and the implementation
   reflects that. Useful to ground the synthesis in code reality.
8. **Already-extracted lit anchors** (only if the synthesis needs to
   cite them):
   [`../extractions/alshamrani2019.md`](../extractions/alshamrani2019.md)
   (phases 3–5 objective conditioning),
   [`../extractions/jalowski2026.md`](../extractions/jalowski2026.md)
   (the three primitives — context for the L3 forward-look),
   [`../extractions/cho2020.md`](../extractions/cho2020.md) (SDR
   taxonomy — context for what L4 will compare across),
   [`../extractions/bianco2013.md`](../extractions/bianco2013.md)
   (Pyramid of Pain — context for *behaviourally-grounded*).

## Out of scope (explicitly)

- **Redoing any L2 analysis.** No re-classifications, no re-fetching CTI
  sources, no re-running JSD. The artefacts are stable; this session
  reads them.
- **Designing L3.** The L3 design will be its own multi-step process
  (per Marc's note above — Petri-net formalism, attacker traversal,
  the Jalowski-primitives encoding decisions). This handoff *contextualises*
  what L3 inherits from L2; it does not produce L3 design.
- **Editing the spec, code, data, or existing notes.** If the synthesis
  surfaces a spec gap or a stale phrase, *flag it* — open a follow-up
  handoff, don't fix in this session.
- **New literature.** Only artefacts already in
  [`../extractions/`](../extractions/) or
  [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md). Adding new
  citations is scope creep.
- **L4 evaluation matrix design.** The synthesis can *note* that L2's
  shape constrains what L4 can claim (thinness, JSD margin,
  operator-aggregation); it should not propose a matrix.
- **Chapter-3 prose.** The note is for Marc-writing-the-thesis, not
  *as* thesis prose. Plain English, well-organised, citation-grounded
  — but a working document, not a chapter draft.

## Critique

Four traps to avoid:

- **Restating the spec.** The biggest failure mode. If a paragraph
  could be replaced by "see `02_gasp_schema.md` §(b)", cut it. The
  reflection's value is the *synthesis layer above the spec*, not a
  re-explanation of what's already canonical.
- **Speculation without grounding.** Every high-level finding traces
  back to a specific artefact — a number, a graph, a passage, a
  visualisation. If a claim can't be grounded, either ground it or
  cut it. "GASP probably generalises well" is speculation; "GASP's
  6/38 `low`-confidence rate (15.8 %) sits under the investigation's
  stated 20 % gate, but two of those six are honest edges within the
  scheme, not data-source gaps" is grounded.
- **Drift into L3 design.** Forward-looking implications are valuable;
  prescribing L3 architecture is the next handoff's job. The boundary
  is: *what does L2's state mean for the *shape* of what L3 has to
  do?* — not *what should L3 look like?*. If you find yourself
  designing the L3 attacker's action-selection logic, you have
  drifted.
- **The "everything is fine" reading.** L2 has real limitations —
  thinness, operator-aggregation, the two honest-edge low-confidence
  flows, the modest JSD margin, the CISA-403 cluster, the Petri-net
  tractability gap. A synthesis that does not name these is a
  marketing brochure, not a methodology document. *Honest* — not
  pessimistic — is the tone.
