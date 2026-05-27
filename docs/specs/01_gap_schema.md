---
status: draft — malleable design schema (v0.5 target). Supersedes the v0.4
        GAP implementation on `feat/attacker-profiling`.
created: 2026-05-27
scope: L1 (GAP construction) only. L2/L3/L4 are consumers, not in scope here.
---

# 01 — GAP schema (Generalised APT Profile, technique-level)

The data model and construction method for **L1 — GAP**: the aggregate
technique-level graph built from the MITRE CTID Attack Flow corpus. This file
is the *what it is* (data model + invariants + decisions). The phased *how to
build it* lives in the companion handoff
[`../handoffs/2026-05-27_gap_rebuild.md`](../handoffs/2026-05-27_gap_rebuild.md).

This sits under [`architecture.md`](architecture.md) §(c)–(d) (L0 parser-contract
+ L1 GAP) and resolves several of its §(l) open questions for the GAP stage. It
does **not** restate ATT&CK / Attack Flow schema basics — those are extracted in
[`../extractions/attackflow.md`](../extractions/attackflow.md) (load that first).

---

## (a) Purpose and the central invariant

The GAP aggregates many analyst-curated per-incident/per-campaign Attack Flows
into one technique-level directed graph, so downstream stages (L2 motivation
subgraphing, L3 attacker traversal, and the eventual Petri-net encoding) read
*generalised* attacker behaviour rather than one campaign at a time.

**Central invariant — every GAP edge corresponds to a dependency a human
analyst actually drew in a flow.** No edge is synthesised by statistical
inference, NLP heuristics, or generative interpretation. This is what "complete
and non-genai-interpretive" means operationally, and it is the property that
distinguishes the GAP from a generic technique co-occurrence graph. An edge that
cannot be traced to at least one `effect_refs` / `on_true_refs` / `on_false_refs`
link in a source flow does not belong in the GAP.

Two corollaries:
- **Tactic ordering is a layout/ordering proxy only.** It never imposes,
  reverses, or invents edge direction — direction comes from the flow. (Contrast
  v0.4, which *imposed* direction on mined edges via tactic order.)
- **Reduction is never destructive at build time.** Thresholds, acyclicity, and
  layering are *views* over a lossless artefact, not bakes into it (§e).

---

## (b) The four design decisions (this session, with Marc)

**Decision 1 — the canonical GAP is Attack-Flow-only.**
The v0.4 GAP merged three edge signals: curated Attack Flow, FP-Growth
co-occurrence over the all-ATT&CK group+software `uses` matrix (Rahman 2022),
and ontology regex over technique descriptions. Drop the latter two from the
canonical GAP.
**Why:** Co-occurrence is *statistical association* across the whole ATT&CK
group population — not observed sequencing — and ontology regex *synthesises*
edges no analyst drew; both violate the §(a) invariant and dilute the curated
signal under one shared `confidence`. (In the built v0.4 artefact, 92/383 edges
were inferred, not curated.)
**If revisited:** Co-occurrence/ontology can return as a **separate, labelled
"associative prior" graph** that is never merged into the curated GAP — useful
as a comparison baseline or for gap-filling, but kept provenance-distinct.

**Decision 2 — AND/OR + condition branches are preserved as edge metadata
(join-groups) on a technique-only aggregate; the per-flow extract stays fully
lossless.**
The aggregate GAP has technique nodes only. Each aggregate edge carries the
operator (`AND`/`OR`), the **join-group id** it belonged to, and the condition
`branch` (`true`/`false`) for every flow occurrence (§d). The per-flow extract
(§c) retains operator and condition objects as first-class nodes, so nothing is
destroyed.
**Why:** Keeps the aggregate a clean technique graph for visualisation and
traversal, while preserving the branching/join semantics v0.4 dropped. The
lossless per-flow layer is the natural input to the eventual Petri-net encoding
(actions→transitions, conditions→places, operators→join/split).
**If revisited:** If a consumer needs the logic *in* the aggregate topology,
promote operators/conditions to first-class aggregate nodes (bipartite graph).
The per-flow layer already holds everything required to do so.
**Open:** *cross-flow* AND/OR reconciliation — one flow AND-joins a precondition
that another OR-joins into the same technique — is **not** resolved into a single
aggregate verdict. The GAP records all occurrences; the reconciliation policy is
§(g) open question 1.

**Decision 3 — the canonical GAP is lossless; reduction is a view.**
Store every observed edge with its `observation_count` and contributing
`flow_ids`; **preserve cycles**. Thresholding (minimum observation count),
DAG-ification, and tactic-layering are computed downstream on demand (§e).
**Why:** v0.4 baked `min_support`/`min_confidence` and broke cycles at build
time — lossy, tied to one threshold choice, and discarding real attacker loops
(lateral-movement ↔ discovery) that matter for fidelity and for the Petri net.
A lossless artefact is reproducible across threshold choices and re-derivable.
**If revisited:** If artefact size becomes a problem, persist a lossless edge
list plus a cached default view, never a reduced-only artefact.

**Decision 4 — data home: gitignore the upstream clone; commit distilled
per-flow extracts + the aggregated GAP.**
The CTID corpus is consumed from a gitignored local clone. The committed,
durable artefacts are (i) one distilled per-flow extract per flow (§c) and
(ii) the aggregated GAP (§d).
**Why:** The per-flow extracts are small, human-reviewable, and the **seam for
adding hand-curated incidents** later — author a new per-flow file by hand and
it aggregates identically to a corpus-derived one. Mirrors the repo's
`extractions/` philosophy (curated, durable) vs `sources/` (gitignored upstream).
**If revisited:** If hand-curation never materialises, the per-flow layer can
become a build cache rather than a committed artefact — but that forfeits the
extension seam, so keep it committed until that's certain.

---

## (c) Per-flow extract — the lossless intermediate (committed)

One file per Attack Flow, generated from the flow's **STIX 2.1 bundle** (not the
`.afb`; see §f) or hand-authored for a new incident. This is a *faithful*
technique-level rendering of the flow: action / operator / condition objects as
typed nodes, `effect_refs` / `on_true_refs` / `on_false_refs` as typed edges.
Format: **YAML** (human-reviewable and hand-editable per Decision 4; JSON is an
acceptable alternative — §g open question 2).

```yaml
flow_id: tesla                       # corpus filename stem, or hand-assigned slug
flow_name: Tesla Kubernetes Cryptojacking
scope: incident                      # attack-flow.scope: incident|campaign|threat-actor|...
source: attack_flow_corpus           # attack_flow_corpus | hand_curated
schema_version: "3.2.0"              # Attack Flow schema generation parsed
references:                          # external_references from the flow (provenance)
  - source_name: "..."
    url: "..."
start_refs: [n1, n3]                 # nodes that start the flow (entry points)
nodes:
  - id: n1                           # stable local id within this flow
    kind: action                     # action | operator | condition
    technique_id: T1610              # actions only — parent-collapsed (§ Decision: sub-techniques)
    sub_technique_id: T1610          # original id as drawn (may equal parent)
    name: Deploy Container
    tactic: execution                # primary tactic (kill-chain phase) of the action
    confidence: 70                   # STIX per-action confidence 0–100, if present
  - id: op1
    kind: operator
    operator: AND                    # AND | OR
  - id: c1
    kind: condition
    description: "elevated privileges obtained"
edges:
  - {source: n1,  target: op1, type: effect}
  - {source: op1, target: n5,  type: effect}
  - {source: c1,  target: n6,  type: on_true}
  - {source: c1,  target: n7,  type: on_false}
```

**Invariants for the per-flow extract:**
- Round-trip faithful: the action/operator/condition nodes and typed edges
  reproduce the flow's logic graph (verified by the §f validation).
- Sub-techniques collapse to parent in `technique_id`; the original is retained
  in `sub_technique_id`. (Decision carried over from v0.4 / Marc's prior
  assumptions.)
- Assets, command refs, and other enrichment STIX objects are **out of scope**
  for L1 (they do not carry sequencing) — recorded only if cheap; never required.

---

## (d) Aggregate GAP — the canonical artefact (committed)

Built by **contracting** operator/condition nodes out of each per-flow graph to
yield technique→technique edges, then **unioning** across all flows. Contraction
tags each resulting edge with the logic it passed through, so AND/OR and
true/false survive as edge metadata (Decision 2).

*Example contraction (Tesla AND-join):* `T1610 → op1(AND) → T1496`,
`T1090 → op1(AND) → T1496`, `T1571 → op1(AND) → T1496` contract to three
technique edges, each tagged `join: {group_id: "tesla:op1", operator: AND}`.
The shared `group_id` is what makes the three recoverable as one AND-set.

### Node — `TechniqueNode`

| Field | Type | Notes |
|---|---|---|
| `technique_id` | str | parent technique, e.g. `T1496` |
| `name`, `tactics`, `primary_tactic`, `tactic_layer` | — | from the ATT&CK STIX bundle |
| `platforms`, `sub_technique_ids` | list | observed sub-techniques collapsed here |
| `flow_count` | int | **node multiplicity** — number of flows containing this technique |
| `flow_ids` | list[str] | provenance |
| `is_entry` | bool | appears in any flow's `start_refs`, or has zero in-edges |
| `is_objective` | bool | terminal in some flow (zero out-edges), typically an Impact tactic |

### Edge — `DependencyEdge`

| Field | Type | Notes |
|---|---|---|
| `source_id`, `target_id` | str | parent technique ids; direction **as drawn in the flow** |
| `observation_count` | int | **edge multiplicity** — number of distinct flows with this contracted edge |
| `flow_ids` | list[str] | provenance — which flows contributed |
| `occurrences` | list[obj] | one per (flow, occurrence); see below — preserves join/branch context |
| `tactic_delta` | enum | `forward` \| `backward` \| `intra` — descriptive only (from `tactic_layer`); never alters direction |
| `confidence_samples` | list[int] | per-occurrence STIX action confidence, if present (for view-time weighting) |

Each `occurrences[i]`:

```yaml
- flow_id: tesla
  edge_type: effect            # effect | on_true | on_false
  join:                        # null when the edge was action→action with no operator
    group_id: "tesla:op1"      # operator instance, namespaced by flow → AND-set recoverable
    operator: AND              # AND | OR
  branch: null                 # true|false when the edge passed through a condition; else null
```

### GAP-level metadata

`version`, `build_date`, `attack_flow_schema_version`, `corpus_ref` (clone
commit/release tag — reproducibility), `attack_source` (ATT&CK STIX version for
node attributes), `source_flow_count`, `node_count`, `edge_count`,
`entry_nodes`, `objective_nodes`, `layers` (tactic_layer → [technique_ids], for
layout).

**Dropped from v0.4 GAP metadata:** `min_support`, `min_confidence`,
`confidence_threshold`, `consensus_edge_count`, `intra_tactic_unresolved`,
`backward_edge_count` — these are properties of a *view* (§e), not of the
lossless artefact, and the support/confidence pair belonged to the
co-occurrence miner that Decision 1 removes.

---

## (e) Views — reduction without loss

Consumers read the lossless GAP through view functions. None mutate the artefact.

| View | Parameter | Use |
|---|---|---|
| **Support filter** | `min_observation_count` | drop edges seen in fewer than *k* flows (the honest replacement for `min_support`) |
| **Acyclic projection** | cycle-break policy | a DAG when a consumer needs topological order; the policy (which edge to cut) is explicit and recorded, not silent |
| **Tactic layering** | — | group nodes by `tactic_layer` for visualisation; `tactic_delta` colours forward/back edges |
| **Motivation subgraph (L2/GASP)** | motivation specifier | the existing terminal-ancestor selectors operate unchanged on the lossless node/edge sets |

This keeps L2 selectors ([`selectors/`] on `feat/attacker-profiling`) and the
HTML visualiser usable: they consume `nodes` + `edges`, which still exist —
they just read richer, lossless edges.

---

## (f) Build pipeline (summary; full plan in the handoff)

1. **Acquire corpus.** Gitignored clone of `center-for-threat-informed-defense/attack-flow`
   (already covered by `.gitignore: attack-flow/`). Pin the release tag.
2. **Resolve to STIX.** Use the flows' **STIX 2.1 JSON bundles**, not `.afb`. The
   corpus ships exported bundles; if only `.afb` are present, convert with the
   Attack Flow CLI (`export-stix`). *(Exact in-repo corpus path: verify at
   implementation — do not hardcode a guess.)*
3. **Parse per flow.** STIX bundle → per-flow extract (§c): read `attack-action`
   (`technique_id`, `tactic`, `confidence`), `attack-operator` (`operator`,
   `effect_refs`), `attack-condition` (`on_true_refs`, `on_false_refs`),
   `attack-flow` (`scope`, `start_refs`). Collapse sub-techniques to parent.
4. **Contract + aggregate.** Contract operator/condition nodes to technique
   edges tagged with join-group/operator/branch (§d); union across flows,
   accumulating `observation_count`, `flow_ids`, `occurrences`.
5. **Attach node attributes.** Join technique nodes to ATT&CK STIX for name /
   tactics / platforms (reuse [`stix_parser.py`]'s ATT&CK reader; **discard** its
   campaign-set path and the whole co-occurrence/ontology path).
6. **Persist.** Commit per-flow extracts + the aggregated GAP. No baked
   reductions.

**Reuse vs replace from v0.4** (`feat/attacker-profiling`): *reuse* the ATT&CK
STIX node reader, the dataclass skeleton in `schema.py` (extended per §c–d), the
L2 selectors, and the HTML viz. *Replace* `cooccurrence_miner.py` (delete from
the canonical path — Decision 1), `edge_importer.py`'s `_parse_afb`
pixel-proximity hack and `extract_ontology_edges` (Decision 1), and
`gap_builder.py`'s threshold + `_break_cycles` bakes (Decision 3).

---

## (g) Validation

- **Tesla golden (operators survive).** The Tesla cryptojacking flow's
  three-input AND join (`T1610`, `T1090`, `T1571` → `T1496`) must appear in the
  per-flow extract as an `AND` operator and in the GAP as three edges sharing one
  `join.group_id` with `operator: AND`. This is the unit test the v0.4 parser
  would have failed (it flattened the join). Source: lit-review Figure 2 /
  [`../extractions/attackflow.md`](../extractions/attackflow.md) Concept 4.
- **Round-trip.** Re-deriving a flow's technique set + directed edges from its
  per-flow extract matches the source STIX bundle's action/effect topology.
- **Aggregate sanity.** Node count tracks corpus technique coverage;
  `observation_count` distribution is non-degenerate (not all 1s);
  entry/objective nodes are plausible (Initial-Access entries, Impact objectives).
- **No-synthesis check.** Every GAP edge has ≥1 `occurrences` entry tracing to a
  real flow link — the §(a) invariant, mechanically assertable.

---

## (h) Open questions (deliberately unresolved)

1. **Cross-flow AND/OR reconciliation.** When flows disagree on whether a
   precondition into a technique is AND- or OR-joined, the GAP records both; it
   does not yet emit a single aggregate verdict. Resolution likely belongs at the
   Petri-net step, where join semantics become explicit transition structure.
   (Also flagged in [`architecture.md`](architecture.md) §(l) / §(d) and
   [`../extractions/attackflow.md`](../extractions/attackflow.md) Concept 2.)
2. **Per-flow format: YAML vs JSON.** YAML chosen for hand-editability; revisit
   if round-trip tooling makes JSON cleaner.
3. **Attack Flow schema version pin.** Inherits [`architecture.md`](architecture.md)
   §(c) open decision (v3.2.0 vs in-tree v2.x). The four-node grammar is stable
   across versions; parsing the STIX export sidesteps the `.afb` format delta.
4. **Corpus ↔ ATT&CK-Campaign overlap.** The CTID corpus flows (named e.g.
   "OceanLotus") are a *different* CTI input from the ATT&CK Campaign
   technique-sets in `data/attacker_profiles/*.yaml` (which are flat, edge-less,
   and feed L3 capability parameters). Whether and how the two are cross-walked
   is out of scope here and noted for L2/L3.

---

## (i) Relationship to other specs

- [`architecture.md`](architecture.md) — §(c) L0 parser-contract and §(d) L1 GAP;
  this file is the GAP data-model detail those sections defer. (Follow-up: add a
  cross-link from §(d)/§(l) once this lands — not done here to keep architecture's
  Pass-2 work Marc-driven.)
- [`../extractions/attackflow.md`](../extractions/attackflow.md) — the Attack Flow
  schema extraction (load-bearing prerequisite reading).
- [`project_context.md`](project_context.md) — the L0→L4 one-liner GAP sits in.
- Prior art being superseded: the v0.4 GAP implementation under
  `src/mtdsim/attacker/gap/` on `feat/attacker-profiling`.
