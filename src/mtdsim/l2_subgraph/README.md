# `l2_subgraph` — L2 GASP construction

| level | artefact | architecture § | status | code home |
|---|---|---|---|---|
| L2 | GASP (operational-objective-subgraphed APT Profile) | [§(e)](../../../docs/specs/architecture.md) | **implemented** | here |

Given the L1 GAP ([`mtdsim.l1_construction`](../l1_construction/)) and an
operational-objective specifier
(`{pure_steal, pure_impediment, double_extortion, infrastructure_setup}`),
produce the **surface** class subgraph — techniques actually present in the
class's flows, with GAP edges where both endpoints land in that node set.
No ancestor closure. Canonical reference:
[`docs/specs/02_gasp_schema.md`](../../../docs/specs/02_gasp_schema.md).

Class membership is sourced from the audit-traced CSV at
[`../../../docs/notes/2026-05-28_l2_metadata_audit.csv`](../../../docs/notes/2026-05-28_l2_metadata_audit.csv) —
not re-derived from per-flow structure. The CSV is the load-bearing input.

## Run

```sh
PYTHONPATH=src python -m mtdsim.l2_subgraph        # writes data/gasp/classification.csv + 4 × gasp_<class>.json
PYTHONPATH=src python -m pytest tests/l2_subgraph/ # validation gate (incl. operator-dedup JSD re-check)
```

## Module layout

| File | Purpose |
|---|---|
| `schema.py` | `SubgraphView` (frozen dataclass) + JSON round-trip |
| `selector.py` | `load_classification` (audit CSV → `flow_id → class`) + `OperationalObjectiveSelector` |
| `build.py` | orchestration: GAP + audit CSV → 4 × `SubgraphView` + `classification.csv` |
| `__main__.py` | CLI entrypoint |

## Validation

`tests/l2_subgraph/test_gasp.py` covers: schema round-trip, the 19:8:6:5
class-count invariant, subgraph-subset-of-GAP sanity, and the operator-
deduplicated JSD re-check (spec §g; Mitigation 1 from
[`../../../docs/notes/2026-05-28_l2_operator_aggregation_concern.md`](../../../docs/notes/2026-05-28_l2_operator_aggregation_concern.md)).
The JSD numbers land in [`../../../data/gasp/README.md`](../../../data/gasp/README.md).
