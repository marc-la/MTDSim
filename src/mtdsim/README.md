# `src/mtdsim/` — the contribution pipeline (L0→L4)

This package is the project's **contribution pipeline**, organised by the
architecture's own **L0–L4 levels**
([`architecture.md`](../../docs/specs/architecture.md)). Each stage is a
directory named `lN_<function>`. This table is the one canonical map of where
each pipeline stage's code lives.

## Cross-walk

| dir | level | artefact | architecture § | status | code home |
|---|---|---|---|---|---|
| [`l0_cti`](l0_cti/) | L0 | raw CTI | [§(c)](../../docs/specs/architecture.md) | **built** | here |
| [`l1_construction`](l1_construction/) | L1 | GAP | [§(d)](../../docs/specs/architecture.md) | **built** | here |
| [`l2_subgraph`](l2_subgraph/) | L2 | GASP | [§(e)](../../docs/specs/architecture.md) | stub | here (prior art: v0.4 selectors on `feat/attacker-profiling`) |
| [`l3_simulation`](l3_simulation/) | L3 | OGASP | [§(f)](../../docs/specs/architecture.md) · [§(i)](../../docs/specs/architecture.md) | stub | **seam in `mtdnetwork/`** (not greenfield) |
| [`l4_evaluation`](l4_evaluation/) | L4 | — | [§(g)](../../docs/specs/architecture.md) | stub | **`mtdnetwork/` metrics** |

## Two axes: pipeline vs substrate

- **Pipeline (stage-organised, here).** L0–L2 are the project's own
  transformations, from raw CTI to a motivation-subgraph. They live in this tree.
- **Substrate (role-organised, `mtdnetwork/`).** L3–L4 *operationalise and
  evaluate* inside the inherited MTDSim simulator. Their `lN_` directories here
  are **seam pointers only** — the code lives in `mtdnetwork/` (inherited,
  golden-bearing). See each stub's `README.md`.

## Naming

Directories are `lN_` + a generic function label: import-safe (a leading
letter, not a digit), self-ordering, and acronym-free. The artefact acronyms
(**GAP / GASP / OGASP**) are kept as *artefact* names in the docs, not in import
paths.

## Running the built stages

```sh
PYTHONPATH=src python -m mtdsim.l0_cti           # L0: acquire gitignored CTI inputs
PYTHONPATH=src python -m mtdsim.l1_construction  # L1: build data/gap/ artefacts
PYTHONPATH=src python -m pytest tests/gap/       # L1 validation gate
```

Artefacts land under [`data/gap/`](../../data/gap/); the L1 data model + the
four construction decisions are in
[`01_gap_schema.md`](../../docs/specs/01_gap_schema.md).
