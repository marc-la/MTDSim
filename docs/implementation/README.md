# Design records

The working records behind the code: what was decided, why, and how it was
checked. They use the repository's internal names (L0–L4, GAP for the attack
graph, GASP for the attack profiles, "substrate" for the inherited simulator);
`src/mtdsim/README.md` maps those names to the dissertation's.

**Start here**

| Record | What it settles |
|---|---|
| [`architecture.md`](architecture.md) | how the stages fit together, from threat intelligence to runs in MTDSim |
| [`substrate_primer.md`](substrate_primer.md) | the inherited simulator, read from the attacker's side |
| [`trace_tool.md`](trace_tool.md) | the two event-log tracers and how to read them |
| [`apt_model_criterion.md`](apt_model_criterion.md) | the eight properties an APT attacker model is scored against (Chapter 3) |

**Checking the inherited simulator (§6.5, threat to validity from code defects)**

| Record | What it settles |
|---|---|
| [`mtdsim_intent_spec.md`](mtdsim_intent_spec.md) | what the prior studies say MTDSim does, from their papers alone |
| [`intent_conformance_audit.md`](intent_conformance_audit.md) | the code checked against that spec, row by row: conforms, design choice, or defect |
| [`mtdsim_spec.md`](mtdsim_spec.md) | the code's behaviour and each disposition |
| [`attacker_read_surface.md`](attacker_read_surface.md), [`boundary_attacker_defender_channels.md`](boundary_attacker_defender_channels.md), [`mtd_write_surfaces.md`](mtd_write_surfaces.md), [`disruption_wiring.md`](disruption_wiring.md) | what the attacker reads, what each MTD mechanism changes, and how the two meet, each verified by running it |

**Values and metrics**

| Record | What it settles |
|---|---|
| [`provenance.md`](provenance.md), [`declared_value_provenance.md`](declared_value_provenance.md) | every load-bearing constant, its source and where the code uses it |
| [`metrics_semantics.md`](metrics_semantics.md), [`disruption_mechanism.md`](disruption_mechanism.md) | what each metric measures and how far it compares with the prior studies |
| [`mtd_mechanism_costs.md`](mtd_mechanism_costs.md) | the measured run-time cost of each MTD mechanism |
| [`figure_table_conventions.md`](figure_table_conventions.md), [`results_presentation_standard.md`](results_presentation_standard.md) | how the floats print numbers and intervals |

**Per stage:** [`pipeline/gap/`](pipeline/gap/) (attack graph schema),
[`pipeline/gasp/`](pipeline/gasp/) (attack profiles schema and partition),
[`pipeline/ogasp/`](pipeline/ogasp/) (every Chapter 4 design choice as a
pre-registration and its findings, and the Chapter 5 findings records).
[`evidence/`](evidence/) holds the per-tactic literature evidence behind the
tactic durations; [`run_plans/`](run_plans/) the run plans the experiment
scripts cite.
