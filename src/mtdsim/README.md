# `src/mtdsim/` — the APT attacker model

The code behind Chapter 4. The package names predate the dissertation's terms
(`l1`–`l3`, GAP / GASP); the table maps each part to the section that describes it.
`src/mtdnetwork/` is the simulator inherited from Brown, Zhang, Ho and Tay.

| Dissertation | Code | Data it reads or writes |
|---|---|---|
| Threat intelligence inputs (§3.1) | [`l0_cti/`](l0_cti/) — `python -m mtdsim.l0_cti` | `data/gap/_corpus_stix/` (committed snapshot), `data/gap/_attack/` (fetched, SHA-256 checked) |
| §4.1 Attack graph from attack flows | [`l1_construction/`](l1_construction/) — `python -m mtdsim.l1_construction` | `data/gap/flows/*.yaml`, `data/gap/gap_v0.5.json` |
| §4.2 Attack profiles by objective | [`l2_subgraph/`](l2_subgraph/) — `python -m mtdsim.l2_subgraph` | `data/gasp/` |
| §4.3 Petri-net formalism | [`l3_simulation/petri/`](l3_simulation/petri/) — `python -m mtdsim.l3_simulation.petri` | `data/ogasp/petri/` |
| §4.4 Integration with MTDSim | [`l3_simulation/movement/`](l3_simulation/movement/) (`run.py: run_movement`) | — |
| §4.4.1 Tactic-to-action mapping | [`l3_simulation/controller/`](l3_simulation/controller/) | `data/ogasp/controller/mappings/v2_partial.csv` |
| §4.4.2 Tactic durations | `l3_simulation/movement/timing.py` | `data/ogasp/tactic_durations.json` |
| §4.4.3 Failure matrix | `l3_simulation/controller/outcome.py`, `l3_simulation/petri/synthetic_overlay.py` | `data/ogasp/controller/overlays/v4_failure_only/` |
| §4.4.4 Vulnerability memory | `src/mtdnetwork/component/adversary.py` (`enable_exploit_learning`), switched on by `run_movement(exploit_learning_rate=2.0)` | — |
| §4.5 Evaluation metrics | `experiments/*/analyse.py` | `experiments/*/numbers*.json` |
| Event-log tracer (§6.5) | [`l3_simulation/trace.py`](l3_simulation/trace.py) — `python -m mtdsim.l3_simulation.trace` | — |

`l3_simulation/timeline/` is an earlier stand-alone walk of the same Petri nets,
kept because its tests pin the nets' structure. Design records for each part are
in [`docs/implementation/`](../../docs/implementation/): the attack-graph and
attack-profile schemas under `pipeline/gap/` and `pipeline/gasp/`, and the
pre-registrations and findings for every Chapter 4 design choice under
`pipeline/ogasp/`.
