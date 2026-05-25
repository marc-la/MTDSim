# Attack Flow `.afb` schema audit

**Phase:** 2 (recon).  **Date:** 2026-05-25.
**Scope:** Marc's `src/mtdsim/attacker/gap/edge_importer.py::_parse_afb` parser
(on `feat/replay-viz`) vs. the **current** MITRE CTID Attack Flow corpus file
format, as a reproducibility check for the GAP v0.4 artifact in
`data/gap/gap_v0.4_latest.json`.

> Stream A scope — included here only because the parser is the brittle hinge
> between Marc's local GAP build and the upstream corpus, and the brief asked
> to confirm reproducibility before relying on the v0.4 graph downstream.

---

## TL;DR — recommend **document, don't migrate**

- **Application versions:** Attack Flow project has tagged releases
  v3.0.0 (2023-07-07) and v3.1.x (2024-04 – 05). These bump the **builder
  UI/library** version, *not* the save-file schema.
- **Save-file schema:** every current corpus `.afb` file under
  `https://github.com/center-for-threat-informed-defense/attack-flow/tree/main/corpus`
  is **still tagged `"schema": "attack_flow_v2"`** (verified 2026-05-25 against
  `Black Basta Ransomware.afb`).
- **Local checkout:** `notebooks/attack-flow/attack-flow-main/` is a vendored
  skeleton — every meaningful subdirectory (`corpus/`, `data/`,
  `src/attack_flow_builder/`) is `.gitignore`d to `*.json` / `*` and contains
  only a stub `.gitignore`. There are **no local `.afb` files to audit
  directly**; the audit was done against a freshly-downloaded corpus file
  (`/tmp/bb.afb`) and a static read of [edge_importer.py](https://github.com/marc-la/MTDSim/blob/feat/replay-viz/src/mtdsim/attacker/gap/edge_importer.py)
  on `feat/replay-viz`.
- **Compatibility verdict:** Marc's parser **still parses** current-day
  corpus files. On `Black Basta Ransomware.afb` (downloaded fresh today)
  it returns 41 (parent-collapsed, deduped) technique→technique edges
  from 38 `action` objects and 146 resolved `generic_latch`s — semantically
  consistent with the v0.4 build that reported "attack_flow: 307" across
  the full corpus.
- **Recommendation:** **Document the schema dependency in the GAP-build
  notebook; do not migrate.** The author-side `attack_flow_v2` tag is
  stable; the v3.x app reads/writes the same format. A v3.x→v3.x corpus
  redesign is **not** announced. Two small parser hardenings (§4) would
  make the dependency robust to drift if it ever does happen.

---

## 1. What the parser expects

[src/mtdsim/attacker/gap/edge_importer.py:30-103](https://github.com/marc-la/MTDSim/blob/feat/replay-viz/src/mtdsim/attacker/gap/edge_importer.py#L30-L103)
(on `feat/replay-viz`, not present on `main` / `chore/baseline-spec`).

It treats an `.afb` as a JSON document with:

| Key path | Type | What it must contain |
|---|---|---|
| `objects` | list[dict] | All flow elements. |
| `layout` | dict[str, [x, y]] | Position of each `instance` UUID for spatial latch resolution. |
| `objects[*].id == "action"` | dict | Technique nodes. Must carry `instance` and a `properties` list. |
| `objects[*].properties` | list[[key, value]] | Property pairs as `[name, value]`. Parser looks for `["technique_id", "T#####"]` (sub-techniques collapse to parent). |
| `objects[*].id == "generic_latch"` | dict | Anchor proxy. Parser resolves each latch → owning action by **nearest-neighbour Euclidean distance in `layout`**, capped at 400 px. |
| `objects[*].id == "dynamic_line"` | dict | Edge object. Must have `source` and `target` referencing latch instances. |

Anything not matching these `id` values is ignored.

## 2. What today's published corpus actually looks like

Inspected file: `corpus/Black Basta Ransomware.afb`, downloaded via raw GitHub
on 2026-05-25.

```json
{
  "schema": "attack_flow_v2",
  "theme": "dark_theme",
  "objects": [ ... ],
  "layout": { ... },
  "camera": { ... }
}
```

Object-type histogram for that one flow:

| `id` | Count | Marc's parser | Note |
|---|---|---|---|
| `vertical_anchor` | 390 | ignored | **NEW** in v2 schema (or always present, parser didn't need it). Holds a `latches` list pointing back at the latches it owns — **direct edges without the spatial-proximity hack**. |
| `horizontal_anchor` | 390 | ignored | as above |
| `generic_latch` | 146 | handled (via spatial layout) | as documented. |
| `dynamic_line` | 73 | handled | now also carries an optional `handles` list (intermediate waypoints). Parser ignores; harmless. |
| `generic_handle` | 73 | ignored | new waypoint object; not significant. |
| `action` | 38 | handled | `properties` still a `[[key, value], …]` list of pairs; `technique_id` field present, exact match. |
| `process`, `tool`, `file` | 4 – 7 each | ignored | STIX-SCO observables attached to actions for context. **Carry no `technique_id`** and don't form edges, so no impact. |
| `AND_operator` | 3 | ignored | **NEW** logical combinator. Has its own `anchors` dict and routes `dynamic_line`s through itself. Since it has no `technique_id`, any `action → AND → action` chain is silently dropped — see §3.B. |
| `flow` | 1 | ignored | flow-level metadata only. |

Key-shape comparison for the three object types the parser cares about:

```
action:        keys=['id', 'instance', 'properties', 'anchors']
                ^^ NEW: anchors dict mapping {position: latch_uuid}
                       → makes the spatial hack obsolete but not wrong
generic_latch: keys=['id', 'instance']           (unchanged)
dynamic_line:  keys=['id', 'instance', 'source', 'target', 'handles']
                                                              ^^ NEW: ignored, harmless
```

## 3. Deltas Marc's parser would benefit from accounting for

### A. `action.anchors` makes spatial resolution unnecessary

Current `action` objects ship with an explicit
`anchors: {"0": latch_uuid, "30": latch_uuid, …, "330": latch_uuid}` map
(12 directional anchor slots). Inverting that map gives `latch → action`
**deterministically**, without a 400 px Euclidean radius and without
mis-attribution risk if a latch sits within the radius of two actions.

- Risk on current parser: low. The spatial-fallback works (verified on Black
  Basta: 146/146 latches resolved). It can mis-resolve if two actions are
  unusually close — Marc's `latch_max_distance=400.0` is a deliberate cap
  precisely because of that.
- Fix: prefer the explicit `action.anchors` map; fall back to spatial. ~10
  lines.

### B. `AND_operator` (and `OR_operator`, where present) drops transitive edges

When an attack flow expresses *"techniques A and B together precede C"*, the
flow author wires both `A → AND_op → C` and `B → AND_op → C` rather than two
direct `A → C` / `B → C` edges. Marc's parser doesn't recognise `AND_operator`
as an action, so the latch resolution against `AND_operator.anchors` *would*
work (`AND_operator` has its own `anchors` dict), but `action_to_tid` has no
entry for it → both edges fail the `src_tid and tgt_tid` guard and are
discarded silently.

- Risk on current parser: medium. The published corpus uses 3 `AND_operator`s
  in this one flow. Across the full ~40-flow corpus this is plausibly tens of
  edges; some will be recovered as `co_occurrence` evidence (where both pre-
  conditions appear in the same campaign anyway), but the `attack_flow`
  evidence count is undercounted.
- Fix: treat `AND_operator` as a pass-through — when resolving an edge, if
  either endpoint resolves to an operator, fan out across the operator's
  other connected latches. Larger change (~30 lines, plus a graph walk).

### C. The `"schema"` top-level tag is not checked

If MITRE CTID *ever* tags a corpus file `"attack_flow_v3"` (no such file
exists yet), Marc's parser would happily try to parse it under v2
assumptions and would silently produce 0 or wrong edges depending on what
moved. The 5-line hardening is to assert `data.get("schema") == "attack_flow_v2"`
at the top of `_parse_afb` and log/skip otherwise.

- Risk today: zero (no v3 files exist).
- Risk for future reproducibility: non-trivial. Adding the guard is essentially
  free.

## 4. Reproducibility recommendation

**Migrate? No. Document? Yes.** Concretely:

1. Add a paragraph to [notebooks/2026-04-08_MTDSim_AttackGraphBuild.ipynb](https://github.com/marc-la/MTDSim/blob/feat/replay-viz/notebooks/2026-04-08_MTDSim_AttackGraphBuild.ipynb)
   (Phase 3 setup cell) documenting:
   - The build pins to corpus files tagged `"schema": "attack_flow_v2"`.
   - As of `data/gap/gap_v0.4_latest.json` (`build_date: 2026-04-19`), the
     corpus snapshot used had 40 `.afb` files contributing 307 edges.
   - Re-running against a future corpus that adds `"attack_flow_v3"` files
     requires either a parser update or a `git checkout` of the corpus repo
     at a v2-only commit.
2. **Optionally** apply the three §3 hardenings above. (§3.A and §3.C are
   trivial; §3.B is a small graph walk and only worth doing if Stream A
   work later starts caring about edge-count fidelity to the corpus.)
3. Capture the corpus commit hash in
   [src/mtdsim/attacker/gap/gap_builder.py::build_gap](https://github.com/marc-la/MTDSim/blob/feat/replay-viz/src/mtdsim/attacker/gap/gap_builder.py)'s
   output metadata so future re-runs can diff against a known-good corpus.

None of these are needed before the lit-review deadline; they're Stream A
hygiene. The simulator's substrate fixes ([crash_6000s.md](crash_6000s.md))
are the only Phase-2 outputs that gate the dissertation timeline.

## 5. What this finding does *not* answer

- Whether the **STIX 2.1 publication** version of Attack Flow (the official
  exchange format, separate from `.afb` save files) diverges from `.afb` v2 in
  ways that matter to the GAP pipeline. Marc's importer reads `.afb` only, not
  the STIX publication.
- Whether the `process` / `tool` / `file` STIX-SCO observables in newer flows
  could carry sequencing constraints the parser should consider (likely no —
  they're attached *to* actions, not to other actions).
- Whether the corpus has changed campaign-set composition since
  `build_date: 2026-04-19`. Out of scope here; trivial to check via
  `git log corpus/` on the attack-flow repo.
