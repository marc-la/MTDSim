# `l3_simulation` — L3 OGASP

L3 OGASP has **two substrates** (architecture §(f)), and they live in different
places:

| substrate | artefact | architecture § | status | code home |
|---|---|---|---|---|
| DES substrate seam | graph-driven attacker alongside the 6-phase baseline | [§(f)](../../../docs/implementation/architecture.md) · [§(i)](../../../docs/implementation/architecture.md) | **stub** | **substrate seam in `mtdnetwork/`** (below) |
| analytical Petri net | weighted structural tactic-place nets per GASP class | [§(f)](../../../docs/implementation/architecture.md) | **L3a shipped** | [`petri/`](petri/) |
| standalone timeline runner | seeded single-token walks → timed attacker-state sequences (D2 v1) | [§(f)](../../../docs/implementation/architecture.md) | **L3b shipped** | [`timeline/`](timeline/) |

## `petri/` — L3a structural Petri-net MVP

Four un-weighted **structural** tactic-place Petri nets (one per GASP class),
built in SNAKES with a single moving black token — the *shape* only (no rates,
timing, weights, rewards, MTD or CTMC; those are later stages). Build brief:
`handoffs/2026-06-18_l3a_petri_mvp.md` (shipped & deleted per handoff lifecycle; see git log);
rationale: [`docs/implementation/pipeline/ogasp/petri_feasibility.md`](../../../docs/implementation/pipeline/ogasp/petri_feasibility.md).
Outputs land under [`data/ogasp/petri/`](../../../data/ogasp/petri/); the
timeline runner ([`timeline/`](timeline/)) writes its artefacts to
[`data/ogasp/timeline/`](../../../data/ogasp/timeline/) (see the
[`data/ogasp/` index](../../../data/ogasp/README.md)). Run:

```sh
pip install snakes                                     # not in environment.yml; diagrams need graphviz `dot`
PYTHONPATH=src python -m mtdsim.l3_simulation.petri    # build + analyse + render
PYTHONPATH=src python -m mtdsim.l3_simulation.timeline # seeded library + report + figures
PYTHONPATH=src python -m pytest tests/l3_simulation/   # validation gate
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
