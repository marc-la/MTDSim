# `data/ogasp/` — L3 OGASP artefacts

The L3 OGASP data tree, split by workstream. This index is hand-maintained;
the sub-directory READMEs/contracts are the authoritative detail.

| Path | Workstream | What |
|---|---|---|
| [`petri/`](petri/) | **L3a — weighted tactic-place Petri nets** | the five committed structural + weighted nets (four GASP classes + the aggregate null profile), the divergence-from-aggregate report, and the gitignored `_viz/` net diagrams. Generated README: [`petri/README.md`](petri/README.md). Build code: [`src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri). |
| [`timeline/`](timeline/) | **L3b — standalone timeline runner** | the `ogasp-timeline/v1` contract ([`timeline/timeline_schema.md`](timeline/timeline_schema.md)), committed example + behavioural verification report, and the gitignored `_timelines/` seeded library and `_viz/` awareness figures. Runner code: [`src/mtdsim/l3_simulation/timeline/`](../../src/mtdsim/l3_simulation/timeline). |
| [`tactic_durations.json`](tactic_durations.json) | **state-duration catalogue (v0, uncalibrated)** | per-tactic dwell consumed by the timeline runner; shared input, owned by neither sub-directory. Source of truth: the 15 [`docs/notes/ch3_design/tactic_profiles/`](../../docs/notes/ch3_design/tactic_profiles/) §5 blocks; provenance dispositions in [`docs/implementation/provenance.md`](../../docs/implementation/provenance.md). |

## Rebuild

```sh
pip install snakes                 # not in environment.yml; needs graphviz `dot` for diagrams
PYTHONPATH=src python -m mtdsim.l3_simulation.petri    # petri/: nets x5 + divergence report + _viz/
PYTHONPATH=src python -m mtdsim.l3_simulation.timeline # timeline/: seeded library + report + _viz/ figures
PYTHONPATH=src python -m pytest tests/l3_simulation/   # validation gate
```

All underscore-prefixed directories (`petri/_viz/`, `timeline/_timelines/`,
`timeline/_viz/`) are gitignored and regenerable — the same pattern as
`data/gap/_*` and `data/gasp/_*`.
