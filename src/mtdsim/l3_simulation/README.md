# `l3_simulation` — L3 OGASP

L3 OGASP has **two substrates** (architecture §(f)), and they live in different
places:

| substrate | artefact | architecture § | status | code home |
|---|---|---|---|---|
| DES substrate seam | graph-driven attacker alongside the 6-phase baseline | [§(f)](../../../docs/specs/architecture.md) · [§(i)](../../../docs/specs/architecture.md) | **stub** | **substrate seam in `mtdnetwork/`** (below) |
| analytical Petri net | structural tactic-place nets per GASP class | [§(f)](../../../docs/specs/architecture.md) | **L3a MVP built** | [`petri/`](petri/) |

## `petri/` — L3a structural Petri-net MVP

Four un-weighted **structural** tactic-place Petri nets (one per GASP class),
built in SNAKES with a single moving black token — the *shape* only (no rates,
timing, weights, rewards, MTD or CTMC; those are later stages). Build brief:
[`docs/handoffs/2026-06-18_l3a_petri_mvp.md`](../../../docs/handoffs/2026-06-18_l3a_petri_mvp.md);
rationale: [`docs/notes/2026-06-18_l3_petri_feasibility.md`](../../../docs/notes/2026-06-18_l3_petri_feasibility.md).
Outputs land under [`data/ogasp/`](../../../data/ogasp/). Run:

```sh
pip install snakes                                    # not in environment.yml; diagrams need graphviz `dot`
PYTHONPATH=src python -m mtdsim.l3_simulation.petri   # build + analyse + render
PYTHONPATH=src python -m pytest tests/l3_simulation/  # validation gate
```

## DES substrate seam (the other L3 substrate)

**This part holds no code here.** The DES substrate seam adds the graph-driven
attacker *alongside* the inherited 6-phase attacker in the MTDSim substrate, not
in this `src/mtdsim/` pipeline tree.

**Where that code attaches** (architecture §(f) "Code location"):

- [`mtdnetwork/component/adversary.py`](../../../mtdnetwork/component/adversary.py)
  — the `Adversary` class (6-phase baseline; the graph-driven attacker is
  intended to live alongside it, selected per-run, not by inheritance).
- [`mtdnetwork/operation/attack_operation.py`](../../../mtdnetwork/operation/attack_operation.py)
  — the SimPy process driver.

The substrate (`mtdnetwork/`) is inherited, golden-bearing, and out of scope for
the pipeline-layout work; this directory is a navigational pointer only.
