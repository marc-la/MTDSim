# `l4_evaluation` — L4 evaluation (substrate seam)

| level | artefact | architecture § | status | code home |
|---|---|---|---|---|
| L4 | — | [§(g)](../../../docs/specs/architecture.md) · [§(i)](../../../docs/specs/architecture.md) | **stub** | **substrate seam — `mtdnetwork/` metrics** |

**This stage holds no code here.** L4 evaluation runs on the inherited MTDSim
substrate and its metrics pipeline, reported per
[`docs/specs/metrics_semantics.md`](../../../docs/specs/metrics_semantics.md):
**internal MTTC** primary; ASR, attack-path exposure, RoA secondary.
Within-substrate comparison is valid; cross-paper numeric comparison is **not**.

**Where the code attaches.** The statistics / metrics pipeline under
[`mtdnetwork/statistic/`](../../../mtdnetwork/statistic/) (architecture §(i)
"Metrics pipeline" row; see [`docs/specs/mtdsim_spec.md`](../../../docs/specs/mtdsim_spec.md)
for the authoritative description). The substrate is inherited and out of scope
for the pipeline-layout work; this directory is a navigational pointer only.
