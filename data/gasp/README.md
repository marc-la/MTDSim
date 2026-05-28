# `data/gasp/` — L2 GASP artefacts

The Generalised APT Subgraph Profile (L2): four operational-objective-
conditioned surface subgraphs over the L1 GAP. Data model and design
decisions: [`docs/specs/02_gasp_schema.md`](../../docs/specs/02_gasp_schema.md).
Build code: [`src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph).

## Contents

| Path | Tracked? | What |
|---|---|---|
| `classification.csv` | **computed** | flow_id → class_name + audit metadata carried through |
| `gasp_pure_steal.json` | **computed** | `SubgraphView` for `pure_steal` (19 flows) |
| `gasp_pure_impediment.json` | **computed** | `SubgraphView` for `pure_impediment` (8 flows) |
| `gasp_double_extortion.json` | **computed** | `SubgraphView` for `double_extortion` (6 flows) |
| `gasp_infrastructure_setup.json` | **computed** | `SubgraphView` for `infrastructure_setup` (5 flows) |
| `_viz/` | gitignored | diagnostic visualisations (regenerable via `_viz/gasp_viz.py`) |

The class subgraphs are a deterministic function of `data/gap/gap_v0.5.json`
and `docs/notes/2026-05-28_l2_metadata_audit.csv`; both inputs are the load-
bearing sources. Re-running the build is cheap.

## Rebuild

```sh
PYTHONPATH=src python -m mtdsim.l2_subgraph         # write classification.csv + 4 × gasp_<class>.json
PYTHONPATH=src python -m pytest tests/l2_subgraph/  # validation gate (incl. operator-dedup JSD re-check)
```

## Validation

The operator-deduplicated JSD re-check (Mitigation 1 from
[`docs/notes/2026-05-28_l2_operator_aggregation_concern.md`](../../docs/notes/2026-05-28_l2_operator_aggregation_concern.md))
re-runs the per-class technique-JSD discrimination after collapsing each
multi-flow operator cluster (Conti, Turla, FIN13, CISA AA22-138B,
OceanLotus, Sandworm, Lazarus) to one representative — the flow with the
highest `n_actions`. If the JSD signal survives the deduplication, the
per-class discrimination is operator-robust.

**Operator-dedup JSD re-check:** mean JSD = 0.3149, null p95 = 0.1826, n_kept = 29 flows. See [`docs/notes/2026-05-28_l2_operator_aggregation_concern.md`](../../docs/notes/2026-05-28_l2_operator_aggregation_concern.md) for the mitigation rationale.
