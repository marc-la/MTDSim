---
status: open
created: 2026-05-28
---

# Decide and justify the L2 (GASP) partition key — operational-objective taxonomy, evaluated against the v0.5 GAP

The investigation answers **two coupled questions**:

1. **Is L2 warranted at all?** I.e., does conditioning the GAP on an operational
   objective yield distinguishable downstream behaviour, or can L3 traverse the
   un-partitioned GAP directly?
2. **If yes, by what taxonomy?** Comparing at least three candidate partition
   schemes against the v0.4 rubric (canonicity / coverage / distinctiveness /
   MTD relevance / validation), and confirming the choice survives the
   downstream Petri-net encoding constraint.

The deliverable is a **notebook + a notes/-file write-up** that picks (or
refuses) a partition method with cited evidence. **No final code lands** in
`src/mtdsim/l2_subgraph/` from this handoff — that is a separate, post-decision
session.

## State of play

### Why L2 is on the docket now

Pipeline status: L1 (GAP v0.5) is built and lossless on this branch; L2
(`src/mtdsim/l2_subgraph/`) is a stub (README + `__init__` only,
[`src/mtdsim/l2_subgraph/README.md`](../../src/mtdsim/l2_subgraph/README.md));
L3/L4 are seam pointers. The pipeline can't be exercised end-to-end until L2
exists, and the **shape** of L2 is a design choice that bounds what L3 can do
and what L4 can claim.

### What's already known (so the next session doesn't re-derive)

**Three independent arguments converge on "L2 is warranted":**

1. *Lit-review framing.* The RQ is explicitly two-axis — SDR-family × *"profiles
   differentiated by operational objective (Section III-C) — the dimension
   along which APT campaigns vary, and which parametric models collapse"*
   ([`docs/sources/LIT_REVIEW.md:233`](../sources/LIT_REVIEW.md#L233)). Without
   L2, the profile axis collapses to a single cell and the RQ is no longer
   comparative.

2. *Fidelity-ladder definition.* The lit review's behavioural rung is defined
   as *"campaign-level intent, motivation conditioning, and learning
   capability"* ([`LIT_REVIEW.md:175`](../sources/LIT_REVIEW.md#L175)).
   Motivation conditioning **is** L2. No L2 → the work sits at Procedural,
   weakening §IV-B's claim to operate at the rung MTD targets.

3. *Empirical structure in the v0.5 corpus.* The GAP construction note already
   records the structural finding: *"of 40 flows, 13 reach exfiltration, 13
   reach impact, but only 3 reach both — campaigns commit to one terminal
   objective, exactly the 'stages 4–5 split by objective' structure"*
   ([`docs/notes/2026-05-27_gap_construction.md`:110-115](../notes/2026-05-27_gap_construction.md#L110)).
   Re-computed at terminal-action granularity (i.e. action with zero
   out-degree in its per-flow extract) on the canonical v0.5 GAP:

   | Bucket (Alshamrani 3-way, structural mapping) | n / 40 | % |
   |---|---:|---:|
   | `steal_data` — terminal in `exfiltration` | 11 | 28% |
   | `impediment` — terminal in `impact` only | 7 | 18% |
   | `position_for_future` (or unobserved suffix) | 22 | 55% |
   | (overlap: exfil ∩ impact) | 3 | 8% |

   Lopsided toward "position_for_future" — but that bucket is **conflated with
   observability bias** (incident reports that stop at the documented intrusion
   without reaching the published terminal). The 11:7 split on the
   observably-completed flows is the cleaner signal and is the empirical
   warrant for splitting at the terminal tactic.

**Two arguments converge on "Alshamrani-NIST 3-goal is the candidate to beat":**

- *Standards-grounded.* Alshamrani §II-C derives stages 3–5 conditioning from
  NIST SP 800-39's three APT goals — *Steal Organization Data* / *Undermine
  Organization's Critical Aspects* / *Position for Future*
  ([`docs/extractions/alshamrani2019.md:54`](../extractions/alshamrani2019.md#L54);
  source verbatim at [`docs/sources/2_3_alshamrani2019survey.md:85`](../sources/2_3_alshamrani2019survey.md#L85)).
- *Operationalisable structurally.* The terminal-tactic of each per-flow
  extract maps cleanly to a NIST goal class without analyst inference —
  `exfiltration` → steal_data, `impact` → impediment, otherwise →
  position_for_future. This sidesteps the "motivation as inferred attribute"
  problem the user raised.

**Three taxonomies are demonstrably dead-ends for L2 partitioning** (do not
re-run these — the evidence is recorded):

- *STIX `primary_motivation` field as the key.* 0 / 187 groups and 0 / 52
  campaigns populate it (2026-04-16 motivation notebook on
  `origin/feat/replay-viz:notebooks/2026-04-16_MTDSim_ATTACKMotivationExploration.ipynb`,
  Part 1 — read via `git show`). Adopting it commits to per-campaign manual
  labelling against an unpopulated field.
- *STIX `attack-motivation-ov` (10-cat vocab) as the key.* Spreads thin: 47
  campaigns labelled by hand from external CTI collapse onto 3 of the 10
  categories with a 31:9:7 (organizational-gain : personal-financial-gain :
  dominance) split — the 7 unused categories add nothing, and the 3 used ones
  are already the answer below.
- *Entry-node anchoring.* T1566 (spear-phishing) alone reaches ~49% of v0.4
  GAP nodes → lopsided 1-to-many partition with one dominant bucket
  (2026-04-17 GAPSubgraphExploration notebook, Candidate C). Same property
  expected to hold on v0.5.

**Selector prior art** lives on `feat/attacker-profiling` /
`feat/replay-viz` (same blob hashes for the selector modules; the latter
has 9 extra commits adding notebooks). The four implemented selectors are:

| Module (v0.4) | Strategy | Rubric (in 2026-04-17 nb) | Status against current question |
|---|---|---:|---|
| `selectors/terminal.py` | Terminal-objective ancestor cone | 21–22/30 | Closest existing analogue — needs **re-labelling** to NIST 3-goal classes |
| `selectors/platform.py` | Platform bucket | 23/30 | **Orthogonal axis** — defender-posture partition, not motivation |
| `selectors/terminal_constrained.py` | Group-witnessed terminal | 22/30 | Tightens A by requiring group co-occurrence — keep as candidate |
| `selectors/base.py` | `ancestor_subgraph()` helper | — | Reuse pattern, not literal port (per zero-trust stance) |

**Demonstrated discrimination** (v0.4): two terminal-cone GASPs (T1486
ransomware vs T1567 cloud-exfil) on identical network + scalar params
produced measurably different technique-level and tactic-level traces under
the simulator (2026-04-22 GAPSubgraphAttackerDemo notebook). So L2 → L3
discrimination is **already empirically supported at proof-of-concept scale**;
this investigation is about choosing the *right* partition axis, not about
showing partitions matter at all.

**Petri-net constraint downstream**
(`origin/feat/replay-viz:notebooks/2026-05-02_MTDSim_PetriNetPrimer.ipynb` —
read via `git show`). The SNAKES-formalisation primer uses
`TerminalObjectiveSelector(technique='T1486')` as its exemplar GASP and
articulates: bounded reachability is **why** the partition matters — a
GASP-shaped subgraph yields a tractable CTMC state space for analytical
MTTC / ASR computation; the un-partitioned GAP does not. Any L2 design must
keep per-partition node count bounded enough for petri-net encoding (the
primer worked at ~14 places, 5–7 transitions on the T1486 cone).

### What's not yet known (this investigation is to settle)

- Whether the v0.5 GAP's per-bucket sizes (under Alshamrani 3-way or
  alternatives) are usable, or whether `position_for_future` is so dominated
  by observability bias that the partition is effectively binary on what
  remains.
- Whether the v0.4 demo's behavioural-discrimination finding (T1486 vs T1567
  produce different traces) survives the re-labelling to NIST 3-goal classes
  on the v0.5 GAP — i.e. does coarsening 30 terminals into 3 classes preserve
  the discrimination?
- Whether any partition produces tractable Petri-net encodings across **all**
  buckets, or whether one bucket (e.g. impediment) is too sparse / fragmented
  to encode usefully.
- Whether the v0.4 rubric's MTD-relevance and validation criteria are still
  the right adjudicators against the v0.5 substrate, or whether new criteria
  (e.g. Petri-net tractability bound) need to be added.

## Recommended approach

A single **investigation notebook** under `notebooks/`, dated
`YYYY-MM-DD_MTDSim_L2PartitionInvestigation.ipynb`, that runs the comparison
end-to-end against the v0.5 GAP and writes a notes file with the verdict.
**Do not modify `src/mtdsim/l2_subgraph/`** — the package stays a stub until
this investigation lands a recommendation Marc signs off on.

### Notebook structure (suggested — adjust as findings dictate)

1. **Load** `data/gap/gap_v0.5.json` and the 40 per-flow YAML extracts under
   `data/gap/flows/`.

2. **Implement four candidate partitions** — fresh, in-notebook, not ported.
   Each yields a dict `{bucket_name: set[flow_ids]}` from the per-flow
   extracts, plus a derived `{bucket_name: SubgraphView-like object}` from
   the aggregate GAP (induced subgraph of bucket's ancestor cone).

   | # | Candidate | Mechanic |
   |---|---|---|
   | P1 | **Alshamrani-NIST 3-goal** (recommended primary) | Bucket each flow by its terminal action's tactic: `exfiltration → steal_data`; `impact → impediment`; otherwise → `position_for_future`. Subgraph = ancestor cone of the bucket's terminal techniques in the aggregate GAP. |
   | P2 | **Terminal-technique** (v0.4 baseline) | One bucket per objective technique (`gap.objective_nodes`, 15 buckets in v0.5). Subgraph = single-objective ancestor cone. The "fragmentation control" against which P1's coarsening earns its keep. |
   | P3 | **Group-witnessed terminal** (v0.4 best) | P2 restricted to ancestors that co-occur in ≥1 ATT&CK group with the terminal. Requires loading ATT&CK group→technique mappings (already available in the build via `attack_stix.py`). |
   | P4 | **Reduced STIX-motivation 3-cat** | Bucket each *flow* (not technique) by Marc's 47-campaign hand-labels onto `{organizational-gain, personal-financial-gain, dominance}`. Requires crosswalking Attack Flow corpus flows to ATT&CK campaigns/groups (some flows have no ATT&CK Campaign ID — those are an explicit "unknown" bucket, not silent drop). The labelling file lives in the 2026-04-16 motivation notebook (Part 4) on `feat/replay-viz`. |

   *Don't* re-run motivation, entry-node, Louvain, or tactic-clustering
   experiments — they have documented negative findings (see *Out of scope*).

3. **Score each partition on the rubric** (carry the 5 criteria from the
   2026-04-17 notebook + **add a sixth, Petri-net tractability**):

   - *Canonicity* (0–5) — is the partition key MITRE-/standards-canonical?
   - *Coverage* (0–5) — fraction of GAP nodes/edges represented across buckets
     (no bucket dropping techniques the lit review claims to model).
   - *Distinctiveness* (0–5) — mean / median pairwise Jaccard overlap on the
     per-bucket technique sets; lower is more distinct. Report distribution
     not just mean.
   - *Balance* (0–5) — coefficient of variation of bucket sizes; a partition
     with one bucket holding 80% of techniques scores low. Use IQR / CV.
   - *Validation path* (0–5) — can the bucket assignment be defended without
     analyst inference? (P1 = high: structural; P4 = low: hand-labelled.)
   - **NEW** *Petri-net tractability* (0–5) — per-bucket node count + edge
     count vs the primer's stated tractability bounds (~14 places, low-tens
     of transitions). Buckets that exceed need to demonstrate analytical
     encoding remains feasible.

4. **Pick the top two partitions on the rubric** and run the **discrimination
   check** the 2026-04-22 demo established:
   - For each top candidate's buckets, build a `SubgraphAttackerProfile`-style
     wrapper *in the notebook* (do not port the v0.4 wrapper).
   - Run the simulator across (bucket × at-least-2-MTD-schemes × 3 seeds),
     report MTTC / ASR / technique-frequency per bucket.
   - **Discrimination is the load-bearing finding**: if buckets within a
     partition don't produce distinguishably different simulator traces, that
     partition has failed regardless of rubric score.

5. **Sketch Petri-net encoding** for one bucket from the winner:
   - Reuse the primer's place=tactic / transition=GAP-edge mapping.
   - Report per-bucket reachability set size and confirm CTMC construction
     remains feasible.
   - **Not** a full SNAKES implementation — a sketch that confirms or
     falsifies the tractability claim.

6. **Write the verdict** as
   `docs/notes/YYYY-MM-DD_l2_partition_decision.md`:
   - Which partition (or none).
   - Rubric scores, discrimination evidence, Petri-net tractability check.
   - The `If revisited:` line stating what would change the decision.
   - A pointer for the *next* session to take the verdict into
     `src/mtdsim/l2_subgraph/` as the implementation step.

### Alternatives considered (don't take them — recorded so the next session disagrees from a shortlist, not from scratch)

- *Skip the investigation; port the v0.4 `TerminalObjectiveSelector`
  directly.* Rejected: re-runs the same partition the 2026-04-17 notebook
  already scored 21–22/30 on v0.4, with no re-evaluation against the v0.5
  (Enterprise-only, lossless) GAP and no coarsening to a NIST-defensible
  3-way. Skips the standards-grounding move that turns the partition from
  "structural surrogate" into "Alshamrani-anchored category".
- *Try a richer motivation-attribution method (NLP / LLM on group
  descriptions).* Rejected for now: the 2026-04-16 notebook already showed
  keyword extraction has F1 0.47; an NLP/LLM pipeline is doable but the
  payoff (labelling 47 campaigns against an unpopulated STIX field) is
  bounded — and even if it succeeded, the labels collapse onto 3 categories.
  Defer to a separate workstream if P4 (reduced STIX 3-cat) turns out to be
  the winner *and* the manual labels are the limiting factor.
- *Take the corpus partition Marc has already started (the 2026-04-16
  motivation notebook's external CTI labels) as a fifth candidate without
  re-deriving.* Worth doing — that's P4 above. Don't *add* a sixth; the
  notebook already covers it.
- *Decide a partition by inspection of the v0.5 GAP visualisation, skip the
  experiment.* Rejected: looking at the graph cannot establish behavioural
  discrimination, which is the load-bearing finding. The rubric is necessary
  but not sufficient.

## Validation gate

The investigation is **done** when:

1. The notebook executes end-to-end against `data/gap/gap_v0.5.json` and
   produces, for each of the 4 candidate partitions:
   - A complete bucket assignment (every flow in exactly one bucket).
   - Numerical scores against the 6-criterion rubric (the 5 from 2026-04-17
     plus Petri-net tractability).
   - A bucket-by-bucket size table (n flows, n techniques, n edges, % of GAP).
2. For the top-2 partitions on the rubric, simulator runs across
   (bucket × ≥2 MTD schemes × ≥3 seeds) report MTTC and ASR per bucket, with
   a clear *discriminates / does not discriminate* verdict per partition.
3. For the winning partition, one bucket's reachability-set size is computed
   and confirmed to fit the primer's tractability bounds (or shown to exceed
   them, with a documented mitigation).
4. `docs/notes/YYYY-MM-DD_l2_partition_decision.md` exists with: the verdict,
   the rubric table, the discrimination evidence, the Petri-net tractability
   check, the `If revisited:` line.
5. This handoff (`2026-05-28_l2_partition_investigation.md`) is **deleted
   in the same commit** that ships the notebook + notes file (per
   [`session_workflow.md`:32-35](../specs/session_workflow.md#L32) handoff
   lifecycle).

A *negative* result is also a valid gate-pass: if no partition discriminates,
the notes file records that and recommends the alternative (`L2 collapses to
the un-partitioned GAP — the contribution lives at L1; revisit if a richer
corpus changes the discrimination signal`).

## Hard constraints

- **Branch hygiene.** Work on a new session branch, not on `feat/gap-schema`
  (it's holding the v0.5 GAP work for review). Suggested name:
  `feat/l2-partition-investigation`. Per
  [`guardrails.md`](../specs/guardrails.md): never on `main`, never push.
- **Zero-trust against prior code.** The v0.4 selector implementations on
  `feat/attacker-profiling` / `feat/replay-viz` are *inspiration only* — do
  not import or copy them into the notebook. The notebook implements the four
  partition mechanisms fresh, justified against the v0.5 spec.
- **Source markdown is authoritative.** When citing literature, cite the
  [`docs/extractions/*.md`](../extractions/) files (Alshamrani, Ferraz,
  Rodríguez) — do not chase external URLs for non-peer-reviewed material when
  the extraction is the source of record.
- **No final code in `src/mtdsim/l2_subgraph/`.** The package stays a stub
  until this investigation lands a recommendation. The notebook is the
  decision artefact; implementation is the *next* handoff after Marc reviews.
- **GAP is the only data input.** Do not re-run L1 (`gap_v0.5.json` is the
  pinned artefact for this investigation). If the GAP changes mid-session,
  flag and pause.
- **Determinism.** Notebook seeds for the simulator runs are fixed and
  reported; re-running the notebook reproduces the same bucket assignments
  and the same simulator traces.
- **Don't action out-of-scope findings.** If the investigation surfaces
  observations about L1 (the GAP) or L3 (the substrate seam), record them as
  a follow-up handoff or a notes file — do not modify either.

## Reading list

In order, before touching the notebook:

1. **[`docs/specs/architecture.md`](../specs/architecture.md) §(e)** — the
   L2 GASP spec block (motivation specifier, terminal-node-ancestor proxy,
   the *"if comparative pass shows motivation-by-attribution matters more
   than motivation-by-terminal-node, swap in the NLP path"* revisit clause).
2. **[`docs/specs/01_gap_schema.md`](../specs/01_gap_schema.md)** — the v0.5
   GAP data model (so the notebook reads `TechniqueNode` / `DependencyEdge` /
   `Occurrence` correctly) + the §(e) views section (the existing
   `support_filter` / `acyclic_projection` views are the API L2 consumes from).
3. **[`docs/notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)
   §"What the assembled graph looks like" + §"The observability boundary"** —
   the empirical structure of the v0.5 GAP and *why* the position-for-future
   bucket is conflated with observability bias.
4. **[`docs/extractions/alshamrani2019.md`](../extractions/alshamrani2019.md)
   §"Five-phase APT lifecycle"** — the load-bearing claim that stages 3–5
   are objective-conditioned; the NIST 3-goal source for P1.
5. **`docs/sources/LIT_REVIEW.md` §III-C, §III-D, §IV-B, §V-B**
   ([line 120 onwards](../sources/LIT_REVIEW.md#L120)) — the RQ framing, the
   behavioural rung definition, the two-axis (SDR × operational-objective)
   structure.

Optional but useful (skim if unfamiliar):

- **The v0.4 partition exploration**, viewable via
  `git show origin/feat/replay-viz:notebooks/2026-04-17_MTDSim_GAPSubgraphExploration.ipynb`
  (the 5-criterion rubric design + the 6 candidate evaluations).
- **The v0.4 demo**, viewable via
  `git show origin/feat/replay-viz:notebooks/2026-04-22_MTDSim_GAPSubgraphAttackerDemo.ipynb`
  (the discrimination check pattern this investigation reuses).
- **The Petri-net primer**, viewable via
  `git show origin/feat/replay-viz:notebooks/2026-05-02_MTDSim_PetriNetPrimer.ipynb`
  (the tractability bounds the 6th rubric criterion uses).

## Out of scope (explicitly)

The investigation is *not* asking for:

- **A motivation NLP/LLM pipeline.** The 2026-04-16 notebook already showed
  keyword extraction is poor (F1 0.47); an NLP/LLM pass is a separate
  workstream if P4 wins *and* hand-labels are the limiting factor. Don't run
  it pre-emptively.
- **Re-evaluating Candidates C (entry-node) / D (tactic-clustering) /
  E (Louvain) / F (raw STIX `primary_motivation`)** from the 2026-04-17
  notebook. All four have recorded negative findings; re-running them is
  re-deriving rejected hypotheses.
- **A full SNAKES Petri-net implementation.** A reachability-size sketch
  confirms (or falsifies) tractability — that's the criterion. Full
  implementation is a separate workstream after the partition decision.
- **Modifying the GAP** (`src/mtdsim/l1_construction/`,
  `data/gap/gap_v0.5.json`, the per-flow extracts) to "fix" anything the
  investigation surfaces. Record findings as a follow-up handoff.
- **Modifying `mtdnetwork/` substrate** to plug the chosen partition into L3.
  That is the *next* handoff after this one's verdict lands.
- **Touching `feat/attacker-profiling` / `feat/replay-viz`.** Those branches
  hold the v0.4 prior art; do not commit to them.
- **Cross-flow AND/OR reconciliation** ([`01_gap_schema.md`](../specs/01_gap_schema.md)
  §(h) Q1). The aggregate edge metadata preserves the operator data; how it
  reconciles at the Petri-net step is itself a separate question.
- **A partition that produces > 5 buckets.** Hard cap derived from (a) the
  L4 factorial budget (SDR-family × buckets × MTD-interval), and (b) the
  primer's per-bucket Petri-net tractability bound. P2 (15-bucket
  terminal-technique) is included as the *control* showing why coarsening
  matters, not as a candidate winner.

---

*Author's note (current session). The "Alshamrani-NIST 3-goal terminal-tactic"
candidate (P1) is the partition I'd back going in: standards-grounded,
operationalisable structurally (no analyst inference per flow), 3 buckets
sized 11/7/22 on the v0.5 corpus. The 22-bucket "position_for_future" is the
main risk — half of those flows are likely incident reports truncated at
intrusion, not genuine surveillance campaigns. The investigation needs to
report which it is, and whether the bucket is usable or needs sub-splitting
(e.g. "ongoing-lateral-movement" vs "documentation-truncated"). The primary
falsification path is the discrimination check: if P1's three buckets produce
indistinguishable simulator traces, the standards-grounded framing buys
nothing and we fall back to the v0.4 finer-grained terminal-technique
selectors. The Petri-net tractability check is the secondary
falsification path: if the position-for-future bucket's reachability set is
too large to encode, partition needs sub-splitting or the bucket needs
dropping (with the L4 claim narrowed accordingly).*
