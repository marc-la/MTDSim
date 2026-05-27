# `l3_simulation` — L3 OGASP (substrate seam)

| level | artefact | architecture § | status | code home |
|---|---|---|---|---|
| L3 | OGASP (operationalised GASP) | [§(f)](../../../docs/specs/architecture.md) · [§(i)](../../../docs/specs/architecture.md) | **stub** | **substrate seam in `mtdnetwork/`** |

**This stage holds no code here.** L3 is the load-bearing *substrate seam*: the
graph-driven attacker is added *alongside* the inherited 6-phase attacker in the
MTDSim substrate, not in this `src/mtdsim/` pipeline tree.

**Where the code attaches** (architecture §(f) "Code location"):

- [`mtdnetwork/component/adversary.py`](../../../mtdnetwork/component/adversary.py)
  — the `Adversary` class (6-phase baseline; the graph-driven attacker is
  intended to live alongside it, selected per-run, not by inheritance).
- [`mtdnetwork/operation/attack_operation.py`](../../../mtdnetwork/operation/attack_operation.py)
  — the SimPy process driver.

The substrate (`mtdnetwork/`) is inherited, golden-bearing, and out of scope for
the pipeline-layout work; this directory is a navigational pointer only.
