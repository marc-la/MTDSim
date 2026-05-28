---
status: open
created: 2026-05-28
---

# Implement GASP construction in `src/mtdsim/l2_subgraph/`, against the accepted spec

An earlier handoff (`2026-05-28_l2_simulator_verification.md`, deleted in
the same commit as this handoff was opened) framed L2 implementation as
conditional on a simulator-driven discrimination check. **Marc has now
greenlit P6** without that condition; the implementation proceeds
against the accepted GASP construction (to be cemented as a spec by
handoff
[`./2026-05-28_l2_spec_consolidation.md`](./2026-05-28_l2_spec_consolidation.md)).
The cheaper operator-deduplicated JSD re-check (Mitigation 1 from the
operator-aggregation concern note) is retained here as the validation
gate.

The L2 package at [`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph/)
is currently a stub (`README.md` + `__init__.py`). This handoff promotes
it to a real package implementing the `(gap, operational_objective) →
SubgraphView` contract, with the four operational-objective classes
sourced from the audit-traced CSV at
[`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv).

## State of play

**Settled (don't re-derive — the spec consolidation handoff captures
all of this in canonical form, but if it hasn't landed yet, these are
the load-bearing facts):**

- Four classes: `pure_steal` (19), `pure_impediment` (8),
  `double_extortion` (6), `infrastructure_setup` (5) on 38 active
  flows.
- Class membership is sourced from the audit CSV's `stated_objective`
  column, mapped:
  ```
  steal_data          → pure_steal
  impediment          → pure_impediment
  double_extortion    → double_extortion
  position_for_future → infrastructure_setup
  ```
- Class subgraph definition is **surface**: union of techniques present
  in the class's flows, with GAP edges where both endpoints are in the
  union. No ancestor closure.
- The L2 boundary object is `SubgraphView` (`node_set: frozenset[str]`,
  `edge_set: frozenset[tuple[str, str]]`, `provenance: dict`). L3
  consumes this; never sees per-flow detail.
- The v0.4 prior art (`SubgraphAttackerProfile` on `feat/replay-viz`) is
  *inspiration only* — fresh implementation.

**Unsettled (this handoff resolves):**

- The schema, classification table, selector, and tests under
  `src/mtdsim/l2_subgraph/`.
- The build entrypoint (`PYTHONPATH=src python -m mtdsim.l2_subgraph`
  should emit the GASP artefacts under `data/gasp/`).
- The validation gate via operator-deduplicated JSD re-check (Mitigation 1
  from [`../notes/2026-05-28_l2_operator_aggregation_concern.md`](../notes/2026-05-28_l2_operator_aggregation_concern.md)).

## Recommended approach

A single implementation session. Code is small (~200 lines across 3–4
modules); the load-bearing work is testing + the validation re-check.

### Package layout

```
src/mtdsim/l2_subgraph/
├── README.md            (existing — update for the implementation)
├── __init__.py          (existing — export the public API)
├── __main__.py          (new — entrypoint for `python -m mtdsim.l2_subgraph`)
├── schema.py            (new — SubgraphView dataclass)
├── classification.py    (new — flow_id → class table, audit-CSV-sourced)
├── selector.py          (new — OperationalObjectiveSelector)
└── build.py             (new — orchestrates classification + selection → artefacts)
```

Tests under `tests/l2_subgraph/`:

```
tests/l2_subgraph/
├── __init__.py
├── test_schema.py
├── test_classification.py
├── test_selector.py
└── test_subgraph_sizes.py   (golden — surface technique counts per class)
```

Data outputs under `data/gasp/` (peer of `data/gap/`):

```
data/gasp/
├── README.md            (new — what's here)
├── classification.csv   (computed — flow_id → class)
├── gasp_pure_steal.json (computed — SubgraphView serialised)
├── gasp_pure_impediment.json
├── gasp_double_extortion.json
└── gasp_infrastructure_setup.json
```

(`data/gasp/_viz/` may be created in parallel by handoff
[`./2026-05-28_l2_viz_iteration.md`](./2026-05-28_l2_viz_iteration.md)
— if it exists when this handoff runs, leave it alone.)

### Tasks

1. **`schema.py` — `SubgraphView` dataclass.**
   - `frozen=True` immutable dataclass with `node_set`, `edge_set`,
     `provenance` fields.
   - `provenance` carries `{operational_objective, class_label,
     selector_name, source_audit_csv, build_date, source_flow_count,
     source_flow_ids}`. Audit-traceable forever after.
   - Serialisation: `to_json()` / `from_json()` round-trips losslessly.

2. **`classification.py` — `flow_id → class` table.**
   - Read the audit CSV at
     `docs/notes/2026-05-28_l2_metadata_audit.csv` and produce a
     `dict[str, str]` mapping `flow_id → class_label`.
   - Read each `flow_id`'s `metadata_confidence` column too — surface
     it in the SubgraphView's provenance.
   - Apply the audit-objective → class mapping (the 4-class
     materialisation).
   - Unit test: every flow in the CSV resolves to exactly one of the
     4 classes; 38 flows total; the per-class counts match
     19 / 8 / 6 / 5.

3. **`selector.py` — `OperationalObjectiveSelector`.**
   - Constructor: `OperationalObjectiveSelector(operational_objective:
     str)` where the value is one of
     `{pure_steal, pure_impediment, double_extortion, infrastructure_setup}`.
     ValueError on anything else (don't fall back silently).
   - `select(gap: dict, flow_classifications: dict[str, str]) ->
     SubgraphView`.
   - Surface subgraph computation: iterate the YAMLs at
     `data/gap/flows/*.yaml`, gather techniques per flow,
     union for flows in the class, then filter GAP edges where both
     endpoints are in the union.
   - **The selector reads per-flow YAMLs *directly*, not via the GAP**
     — the GAP's `flow_count` / `flow_ids` per-node metadata isn't a
     class-membership index (it's an L1 metadata field). Keep these
     concerns separate.

4. **`build.py` — orchestration.**
   - Loads GAP + audit CSV.
   - Instantiates the four selectors.
   - Writes class-CSV + per-class JSON artefacts under `data/gasp/`.
   - Mirrors `l1_construction/build.py`'s structure — keep the
     symmetry visible.

5. **`__main__.py` — CLI.**
   - `PYTHONPATH=src python -m mtdsim.l2_subgraph` runs `build.py`.
   - Optional flags: `--out-dir`, `--gap-path`, `--audit-path` (each
     defaulting to the convention path; explicit override only for
     re-running on a non-default location).

6. **Tests** — golden + invariant checks:
   - `test_schema.py` — round-trip serialisation; frozen-dataclass
     immutability.
   - `test_classification.py` — 38 flows / 4 classes / 19:8:6:5 counts.
   - `test_selector.py` — for each of the 4 selectors,
     `SubgraphView.node_set` is a subset of `gap['nodes']`;
     `edge_set ⊆ {(e['source_id'], e['target_id']) for e in gap['edges']}`;
     every node in `node_set` belongs to at least one flow in the
     class (no synthesis).
   - `test_subgraph_sizes.py` — golden sizes per class (subject to
     small drift if the audit CSV is edited):
     ```
     pure_steal:           98 techniques, 413 edges   (16 flows pre-verification → 19 post; sizes ± a few)
     pure_impediment:      62 techniques, 254 edges
     double_extortion:     57 techniques, 225 edges
     infrastructure_setup: 39 techniques, 148 edges
     ```
     **Update these numbers on first run** — they're approximate from
     the viz-iteration's output.

7. **Validation gate: operator-deduplicated JSD re-check.** Per
   [`../notes/2026-05-28_l2_operator_aggregation_concern.md`](../notes/2026-05-28_l2_operator_aggregation_concern.md)
   Mitigation 1: re-run the corpus-level technique-JSD discrimination
   on an **operator-deduplicated** corpus. Concretely, for each
   operator-cluster (Conti, Turla, FIN13, CISA AA22-138B, Sandworm,
   OceanLotus, Lazarus), pick the flow with the highest `n_actions`
   and drop the rest. The resulting ~28-flow corpus is the
   "operator-uniform" view. Compute mean pairwise technique-JSD on
   surface subgraphs.

   - If mean JSD remains above the null p95 (~0.15): verdict stands
     and is **operator-robust**. Record the operator-deduplicated JSD
     in `data/gasp/README.md` as a one-line validation note.
   - If mean JSD collapses to the null: the per-class discrimination
     signal is operator-dominated; **flag back to Marc** before
     proceeding with downstream L3 work. The implementation can still
     land (it's a structural decision) but the L4 evaluation claim
     would need re-scoping.

   Implementation: a small `tests/l2_subgraph/test_operator_deduplication.py`
   that asserts the operator-deduplicated mean JSD is above the null
   p95. The test failing is a real finding, not a bug — Marc decides
   what to do.

8. **Update [`../../src/mtdsim/l2_subgraph/README.md`](../../src/mtdsim/l2_subgraph/README.md)**
   to reflect that the package is now built (not stub). Point to the
   new spec at `docs/specs/02_gasp_schema.md` as the canonical
   reference.

### Alternatives considered

- *Read class memberships from the GAP json's per-node metadata
  rather than the audit CSV.* Rejected. The GAP's per-node
  `flow_count` / `flow_ids` are *technique-presence* records, not
  *class-membership* records. Going via flows → class is the correct
  separation of concerns.
- *Compute class subgraphs via ancestor closure (matching the original
  architecture §(e) proxy).* Rejected — see the partition-decision
  note for the empirical reason (every class's ancestor cone covers
  87–97 % of the GAP, so cones are non-distinct).
- *Run the simulator-driven discrimination check as a hard gate.*
  Demoted — Marc greenlit P6 without it. Keep operator-deduplicated
  JSD as the validation gate (Mitigation 1; cheap, decisive enough);
  full simulator discrimination is L3 / L4 territory and lives in a
  separate workstream.
- *Implement L2 selectors as functions rather than classes.* Defensible
  but rejected for consistency — the GAP's L1 build uses classes
  (`SubgraphView` is a class), and the v0.4 prior art used a selector
  *class*. Match the convention.

## Validation gate

Done when:

1. `src/mtdsim/l2_subgraph/` is a real package: schema, classification,
   selector, build, `__main__` all present and import cleanly.
2. `PYTHONPATH=src python -m mtdsim.l2_subgraph` runs end-to-end and
   produces `data/gasp/classification.csv` + 4 × `data/gasp/gasp_<class>.json`.
3. `PYTHONPATH=src python -m pytest tests/l2_subgraph/ -q` passes.
4. Class counts in the produced classification.csv match
   19 / 8 / 6 / 5 = 38.
5. Operator-deduplicated JSD re-check runs and produces a
   one-line validation note in `data/gasp/README.md`.
6. The L2 README points to the new spec
   (`docs/specs/02_gasp_schema.md`) as canonical.
7. This handoff is deleted in the same commit that ships the
   implementation.

## Critique

Four pitfalls:

- **Reading prior code via `git show`.** Reading it is fine (zero-trust
  is *don't port*, not *don't read*). But the temptation to
  copy-with-modifications is real. Implement fresh, justifying choices
  against the spec; the v0.4 module structure was good but its tactic-
  to-phase mapping and `sample_technique` weighting are scoped to a
  different problem (the simulator's attacker).
- **Coupling L2 to the simulator.** The L2 boundary object
  (`SubgraphView`) should be simulator-agnostic. The simulator's
  attacker wraps `SubgraphView`, not the other way around. If the
  implementation grows a `sample_technique` method on the selector,
  that's coupling — move it out.
- **Test brittleness on subgraph sizes.** The class sizes I gave
  (98/62/57/39 techniques) come from the viz iteration's surface
  computation. If the audit CSV is edited later (e.g. ToolShell
  flow-split, which is in the open-questions list), the sizes shift.
  Tests should assert *ranges* (e.g. `90 <= len(pure_steal.node_set)
  <= 110`) and the *count of flows per class* exactly; the exact
  technique count is a golden, not an invariant.
- **The operator-deduplication test could fail "in production".**
  This is by design — see the verdict note's "if revisited" clause.
  But the failure mode should be loud (a failing pytest with a clear
  message) rather than silent (a quietly-changed JSON). Make it a
  pytest, not a logged warning.

## Hard constraints

- **Branch hygiene.** Dedicated branch
  (`feat/l2-subgraph-implementation` or similar). Never on `main`. No
  push without ask.
- **Zero-trust against the v0.4 wrapper.** Read for inspiration; don't
  copy.
- **Determinism.** Building L2 from the same audit CSV + GAP must be
  byte-stable (sorted iteration; explicit ordering on serialisation).
- **No edits to the audit CSV.** If the implementation surfaces an
  audit error, record as a follow-up handoff. The CSV is the source of
  truth for membership.
- **No edits to L1 / the GAP.** L2 reads them; doesn't change them.

## Reading list

In order:

1. **`docs/specs/02_gasp_schema.md`** (if it exists when this handoff
   runs — written by the spec-consolidation handoff). The canonical
   reference. If it doesn't exist, fall back to the partition-decision
   note.
2. **[`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md)** —
   the verdict the implementation realises.
3. **[`../notes/2026-05-28_l2_operator_aggregation_concern.md`](../notes/2026-05-28_l2_operator_aggregation_concern.md)** —
   the validation gate (Mitigation 1).
4. **[`../../src/mtdsim/l1_construction/`](../../src/mtdsim/l1_construction/)** —
   the structural prior art. The L2 module structure should mirror L1's
   (`schema.py`, `build.py`, `__main__.py`, etc.).
5. **`git show origin/feat/replay-viz:src/mtdsim/attacker/subgraph_profile.py`** —
   the v0.4 wrapper's API surface. *Read, don't copy.*

## Out of scope

- Visualisation — handoff
  [`./2026-05-28_l2_viz_iteration.md`](./2026-05-28_l2_viz_iteration.md).
- Spec consolidation — handoff
  [`./2026-05-28_l2_spec_consolidation.md`](./2026-05-28_l2_spec_consolidation.md).
- L3 / L4 work — the simulator's attacker wrapper (`SubgraphAttackerProfile`-
  equivalent) lives in `mtdnetwork/`, not in `l2_subgraph/`. Wrapping
  is a separate handoff (likely `feat/l3-graph-driven-attacker` or
  similar).
- Cross-flow AND/OR reconciliation
  ([`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) §(h) Q1) —
  not an L2 problem.
- The full Petri-net L4 substrate — informational per architecture
  §(f) and the partition-decision note's Branch-point C.
- Modifying the audit CSV.
