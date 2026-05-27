# `l1_construction` — L1 GAP construction

| level | artefact | architecture § | status | code home |
|---|---|---|---|---|
| L1 | GAP (Generalised APT Profile) | [§(d)](../../../docs/specs/architecture.md) | **built** | here |

Builds the **GAP**: a lossless, Attack-Flow-only technique-dependency graph
aggregated from the L0 corpus. Data model + the four construction decisions:
[`01_gap_schema.md`](../../../docs/specs/01_gap_schema.md); plain-English
companion:
[`2026-05-27_gap_construction.md`](../../../docs/notes/2026-05-27_gap_construction.md).

```sh
PYTHONPATH=src python -m mtdsim.l1_construction   # -> data/gap/flows/, gap_v0.5.json
PYTHONPATH=src python -m pytest tests/gap/         # 13-test validation gate
```

- `schema.py` — dataclasses (per-flow extract + GAP).
- `attack_flow_parser.py` — STIX bundle → per-flow extract.
- `attack_stix.py` — ATT&CK node metadata + tactic taxonomy.
- `aggregate.py` — contract operators/conditions → technique edges; union across flows.
- `views.py` — non-mutating reductions (support filter, acyclic projection, tactic layering).
- `build.py` — top-level `build_gap()` + persistence.
- `__main__.py` — the CLI runner.

Artefacts under [`data/gap/`](../../../data/gap/); gate at
[`tests/gap/`](../../../tests/gap/).
