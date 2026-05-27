---
status: open
created: 2026-05-27
---

# Rebuild the GAP (L1) as a lossless, Attack-Flow-only technique graph

Implement the data model + pipeline specified in
[`../specs/01_gap_schema.md`](../specs/01_gap_schema.md), superseding the v0.4
GAP on `feat/attacker-profiling`. This handoff is the *how*; the spec is the
*what*. Read the spec first — it carries the four design decisions and is the
source of truth for the schema.

## State of play

- A full v0.4 GAP pipeline exists on `feat/attacker-profiling` under
  `src/mtdsim/attacker/gap/` (parser, co-occurrence miner, edge importer,
  builder, dataclasses, motivation enrichment, L2 selectors, HTML viz) plus a
  built `data/gap/gap_v0.4_latest.json` (216 nodes, 383 edges).
- **It does not meet the brief** ("complete, non-genai-interpretive, preserve
  sequencing + dependencies"). Confirmed losses, with evidence, are in the
  critique that produced the spec. The headline ones:
  - AND/OR operators and condition true/false branches are dropped
    (`edge_importer._parse_afb` reads only `action`→`action`).
  - Attack Flow is parsed from the proprietary `.afb` by **pixel-proximity**
    (≤400px) instead of the lossless STIX export.
  - Edge multiplicity is a text string; `source_count` counts evidence *types*,
    not flows — there is no numeric edge weight.
  - 92/383 edges are *inferred* (co-occurrence + ontology), not curated.
  - Build-time threshold + `_break_cycles` bakes discard cycles and tie the
    artefact to one threshold choice.
- `.gitignore` already anticipates the corpus clone (`attack-flow/`,
  `enterprise-attack.json`, `attack-stix-data/`).
- The per-campaign YAMLs in `data/attacker_profiles/*.yaml` are a **separate**
  artefact (flat ATT&CK *Campaign* technique-sets → L3 capability params) — not
  part of this rebuild.

## Recommended approach

Phased, per [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) §(f). Land
each phase behind its own validation before moving on.

1. **Corpus acquisition.** Clone CTID attack-flow into the gitignored location;
   pin the release tag in GAP metadata (`corpus_ref`). Locate the STIX 2.1 JSON
   bundles; if only `.afb` are present, convert via the Attack Flow CLI
   (`export-stix`). **Verify the in-repo corpus path — do not hardcode a guess.**
2. **STIX → per-flow extract.** New parser producing the §(c) YAML: action /
   operator / condition nodes + typed edges (`effect` / `on_true` / `on_false`).
   Validate against the **Tesla golden** (§g): the three-input AND must survive.
3. **Contract + aggregate.** Operator/condition contraction → technique edges
   tagged with join-group/operator/branch; union across flows with
   `observation_count`, `flow_ids`, `occurrences` (§d).
4. **Node attributes + persist.** Reuse the ATT&CK STIX reader for node
   metadata; commit per-flow extracts + the aggregated GAP. No baked reductions.
5. **Views.** Reimplement support-filter / acyclic-projection / layering as
   non-mutating views (§e); confirm the L2 selectors and HTML viz still consume
   the richer edges.

**Reuse, don't rewrite:** the ATT&CK STIX node reader in `stix_parser.py`, the
`schema.py` dataclass skeleton (extended per spec §c–d), the L2 selectors, and
the viz. **Delete from the canonical path:** `cooccurrence_miner.py`, the
`_parse_afb` + `extract_ontology_edges` functions, and `gap_builder.py`'s
threshold/`_break_cycles` bakes.

**Alternative considered:** keep v0.4 and add a thin "preserve operators" patch.
Rejected — the lossy `.afb` parser, imposed tactic direction, baked thresholds,
and the merged inferred edges are structural, not patchable without the schema
change.

## Validation gate

- **Tesla golden** passes: AND-join (`T1610`/`T1090`/`T1571` → `T1496`) present
  as one `AND` operator in the per-flow extract and three edges sharing a
  `join.group_id` in the GAP.
- **No-synthesis assertion** passes: every GAP edge traces to ≥1 real flow link.
- **Round-trip:** per-flow extract reproduces the source STIX action/effect
  topology.
- **Multiplicity is numeric:** `observation_count` is a populated integer with a
  non-degenerate distribution (not all 1s).
- **Lossless:** rebuilding with a different support threshold changes only the
  *view*, not the committed artefact.

## Hard constraints

- **Branch / commit / never push** per [`../specs/session_workflow.md`](../specs/session_workflow.md).
  Do **not** commit the gitignored corpus clone or `enterprise-attack.json`.
- **§(a) central invariant is non-negotiable:** no synthesised edges; tactic is
  layout-only and never sets direction.
- **Australian English** in docs/comments ([`../specs/guardrails.md`](../specs/guardrails.md)).
- Keep the GAP consumable by L2/L3 — `nodes` + `edges` must still exist; don't
  break the selector/viz contract.
- Apache-2.0 corpus: preserve CTID notice if any flow content is reproduced.

## Reading list

- [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) — the schema + the four decisions (read in full).
- [`../extractions/attackflow.md`](../extractions/attackflow.md) — Attack Flow SDO grammar (Concepts 1–4; Tesla in 4).
- [`architecture.md`](architecture.md) §(c)–(d), §(l) — where GAP sits + open questions this resolves.
- `src/mtdsim/attacker/gap/{schema,stix_parser,edge_importer,cooccurrence_miner,gap_builder}.py` on `feat/attacker-profiling` — the v0.4 prior art (reuse/replace map in spec §f).
- `docs/sources/2_1_attackflowdoc.md` §3 — the STIX field names (gitignored; read in-session).

## Out of scope (explicitly)

- L2 (GASP) motivation attribution, L3 (OGASP) traversal, L4 evaluation — GAP is
  the deliverable; downstream stays as-is.
- The Petri-net encoding (the per-flow lossless layer is built *for* it, but
  encoding it is later work).
- The `data/attacker_profiles/*.yaml` ATT&CK-Campaign sets and their substrate
  capability mapping.
- Resurrecting co-occurrence/ontology as a labelled prior (spec §b Decision 1
  "If revisited") — only if Marc asks.
- Editing `mtdsim_spec.md` / `metrics_semantics.md` / `provenance.md`.
