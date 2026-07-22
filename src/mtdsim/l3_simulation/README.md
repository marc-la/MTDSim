# `l3_simulation` — L3 OGASP

L3 OGASP has **two substrates** (architecture §(f)), and they live in different
places:

| substrate | artefact | architecture § | status | code home |
|---|---|---|---|---|
| DES substrate seam | graph-driven attacker alongside the 6-phase baseline | [§(f)](../../../docs/implementation/architecture.md) · [§(i)](../../../docs/implementation/architecture.md) | **movement layer built** (consumes the carved substrate + controller) | [`movement/`](movement/) (drives the carve in `mtdnetwork/`) |
| controller sublayer | tactic → MTDSim-verb dispatch + success/failure outcome overlay | [§(f)](../../../docs/implementation/architecture.md) | **dispatch shipped; overlay composition finalising** | [`controller/`](controller/) |
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

## `movement/` — the DES substrate seam (the graph-driven attacker)

The graph-driven attacker that walks a class net's single token **live inside a
running MTDSim simulation**, *alongside* the inherited 6-phase attacker (per-run
selection, no inheritance — both keep working). Build brief:
`handoffs/2026-07-22_l3_attacker_petri_to_mtdsim.md`. Per-place lifecycle, all
through the controller library:

```
enter place → dwell (D4) → controller.phase_for(tactic) → attack_op.step(verb)
  → verdict adapter → overlay.compose(place, verdict) → sample the next transition
```

The net supplies *movement*; the carved substrate (`step(verb)`, anatomy §3)
supplies *outcome* (M4). Pieces:

- [`movement/net.py`](movement/net.py) — the routing net (base out-weights per
  place: observed D3 weights composed with the M6 synthetic overlay; schema-pinned).
- [`movement/attacker.py`](movement/attacker.py) — `MovementAttacker`, the live
  SimPy net-walker, and the per-event `MovementRecord`.
- [`movement/statistics.py`](movement/statistics.py) — a *reader* over the records
  (MTTC / ASR per profile); the inherited attack-stats maths is untouched.
- [`movement/run.py`](movement/run.py) — run wiring (attacker selected alongside
  the native one; D8 arms; the controller library injected).

**Attacker-only (D5).** The movement layer lives entirely here; it *drives* the
inherited substrate through the carved action surface but changes no behaviour
under [`mtdnetwork/component/`](../../../mtdnetwork/component/) or
[`mtdnetwork/mtdai/`](../../../mtdnetwork/mtdai/) — so the goldens reproduce
byte-for-byte and the boundary audit is clean (`tests/l3_simulation/test_movement_smoke.py`).

**Consumes, never forks.** Dispatch (`controller.phase_for`), outcome composition
(`overlay.compose`) and the success/failure verdict adapter are the controller
sublayer's surface — the movement layer calls them (injected collaborators). The
composition + verdict adapter are finalised by the controller handoff
(`handoffs/2026-07-22_l3_controller_success_failure.md`); `run.py` wires the real
controller by default and works unmodified once they land.
