# `data/ogasp/` — L3a OGASP weighted tactic-place Petri nets

Five **weighted** structural tactic-place Petri nets — one per GASP
class plus the **aggregate (null) profile** over the union of all
flows — built in SNAKES with a single moving black token. Shape +
W-A flow-proportion weights; no timing, rewards, MTD or CTMC (those
are later stages). Stages 1–2 (L3a) of the OGASP Petri-net
workstream.

- **Build code:** [`src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri).
- **Design / rationale:** [`docs/notes/2026-06-18_l3_petri_feasibility.md`](../../docs/notes/2026-06-18_l3_petri_feasibility.md)
  (the base structural net is GO-unconditional, sec.8).
- **Locked P/T/F/M mapping:** places = ATT&CK tactics; transitions =
  inter-tactic tactic-pairs (each tracing to >=1 GASP technique-edge — the
  no-synthesis invariant); flow = `place[a] -> T -> place[b]`; marking =
  one black token in `reconnaissance` (else `initial-access`).
- **Weight regime (D3, dispositioned in
  [`docs/specs/metrics_semantics.md`](../../docs/specs/metrics_semantics.md) §(f)):**
  per transition and corpus variant, `weight = numerator / denominator`
  where the numerator counts **distinct attack flows** contributing >=1
  technique-edge under the tactic-pair and the denominator sums the
  numerators over the source place's out-transitions — the
  out-edge-normalised flow proportion; per-place out-weights sum to 1.
  The literal minuted per-flow proportion (`flow_proportion` =
  numerator / `flows_leaving_source`) is stored beside it; where flows
  branch it sums to >1 across a place, which is why the normalised
  form is the routing weight. Raw numerators/denominators and backing
  flow IDs stay inline so the thinness is visible (D9). Two variants
  per net: `operator_dedup` (primary, n = 29 — the §(g) Mitigation-1
  rule, one representative per operator cluster) and `raw` (n = 38,
  robustness). `observation_count` is never normalised or consumed.
  No smoothing. **Weights are workflow-recurrence, never efficacy or
  actor-likelihood** — each net is a class **envelope**, and
  tactic-level aggregation deliberately trades away AND-gate/join
  structure for groundable weights (recorded tradeoff).

## Rebuild

```sh
pip install snakes                 # not in environment.yml; needs graphviz `dot` for diagrams
PYTHONPATH=src python -m mtdsim.l3_simulation.petri   # write <profile>_structural.json x5 + divergence report + _viz/
PYTHONPATH=src python -m mtdsim.l3_simulation.timeline # seeded timeline library + example + behavioural report
PYTHONPATH=src python -m pytest tests/l3_simulation/  # validation gate
```

## Contents

| Path | Tracked? | What |
|---|---|---|
| `<class>_structural.json` × 4 | **computed** | net shape (places, transitions + per-transition GASP provenance) + W-A weight layer (both corpus variants, backing flow IDs) + structural report |
| `aggregate_structural.json` | **computed** | the fifth (null) net over the union of all flows — same shape and weight layer |
| `divergence_report.md` / `.json` | **computed** | class-vs-aggregate per-place JSD, weighted discriminators, shuffled-label null, verdict |
| `_viz/<profile>.png` / `.svg` | gitignored | **tactic-state diagram** — kill-chain L→R; token in its seed; entry green, objective orange, sinks double-outlined; edge width/opacity = W-A weight (uniform absolute scale across the five nets); unreachable-from-token places dashed |
| `_viz/<profile>_snakes.png` | gitignored | the **formal SNAKES net** (bipartite places + transition bars) — faithful but dense; kept as a provenance artefact |
| `_viz/_reachability.png` | gitignored | **headline chart** — tactics reachable from the recon token vs from any entry, per profile |
| `timeline_schema.md` | **committed** | the timeline-runner artefact contract (`ogasp-timeline/v1`): record schema, declared walk semantics, run matrix |
| `timeline_example.jsonl` | **committed** | the shortest committed timeline of each outcome kind (objective / stalled / cap) — the contract's living companion |
| `timeline_report.md` / `.json` | **computed** | behavioural verification report — per-cell summary stats, class-vs-aggregate comparison, verdict (the behavioural half of the divergence question) |
| `_timelines/<cell>.jsonl` + `manifest.json` | gitignored | the seeded timeline library over the full run matrix — regenerable via `python -m mtdsim.l3_simulation.timeline` |

All `_viz/` figures are gitignored (regenerable; mirrors the `data/gasp/_*`
pattern). The diagrams need graphviz `dot` + the `graphviz` Python package;
the headline chart needs `matplotlib` (both house dependencies of
`data/gasp/_viz/gasp_viz.py`).

## Structural summary

| Profile | Flows (raw → dedup) | Places | Transitions | Inter-tactic edges | Self-loops dropped | Objective reachable from recon | recon→initial-access |
|---|---|--:|--:|--:|--:|---|---|
| `pure_steal` | 19 → 14 | 15 | 109 | 363 | 50 | yes | bridged |
| `pure_impediment` | 8 → 7 | 14 | 83 | 225 | 29 | yes | bridged |
| `double_extortion` | 6 → 4 | 14 | 72 | 201 | 24 | **no** | **disconnected** |
| `infrastructure_setup` | 5 → 4 | 13 | 57 | 136 | 12 | **no** | **disconnected** |
| `aggregate` | 38 → 29 | 15 | 122 | 422 | 56 | yes | bridged |

The aggregate's declared objective set is the union of the four
class-semantic objectives (command-and-control, exfiltration, impact)
— a recorded choice; the null envelope has no single operational
objective. Note the operator clusters span classes (e.g. the CISA
AA22-138B trio splits across `pure_steal` and `infrastructure_setup`),
so deduplication can remove flows from several classes at once —
dedup class sizes are 14 / 7 / 4 / 4 (Σ = 29).

## Divergence from the aggregate (headline)

- **pure_steal** — mean per-place JSD 0.1919 vs aggregate; does NOT exceed the shuffled-label null p95 (0.2248).
- **pure_impediment** — mean per-place JSD 0.3330 vs aggregate; does NOT exceed the shuffled-label null p95 (0.4158).
- **double_extortion** — mean per-place JSD 0.3000 vs aggregate; does NOT exceed the shuffled-label null p95 (0.5281).
- **infrastructure_setup** — mean per-place JSD 0.3813 vs aggregate; does NOT exceed the shuffled-label null p95 (0.5101).

Full tables, discriminators and the verdict paragraph:
[`divergence_report.md`](divergence_report.md).

## The prefix gap (inspect-the-base finding)

The marking seeds the token in `reconnaissance`. On the observed-only
base the corpus starts at the point of detection, so the
`reconnaissance → initial-access` link is near-absent — and it shows up
directly in the single-token reachability:

- **pure_steal** — BRIDGED by 1 direct recon->initial-access edge(s) [('T1593', 'T1195')] -- a thin, fragile prefix link
- **pure_impediment** — BRIDGED by 1 direct recon->initial-access edge(s) [('T1593', 'T1195')] -- a thin, fragile prefix link
- **double_extortion** — DISCONNECTED -- reconnaissance cannot reach initial-access; the recon place is an island (the observed-only prefix gap)
- **infrastructure_setup** — DISCONNECTED -- reconnaissance cannot reach initial-access; the recon place is an island (the observed-only prefix gap)
- **aggregate** — BRIDGED by 1 direct recon->initial-access edge(s) [('T1593', 'T1195')] -- a thin, fragile prefix link

Consequence: in the classes where recon is an island, a recon-seeded
token cannot reach the objective; seeding at `initial-access` (the
corpus's dominant real entry) is required. Whether to add the
literature-grounded `recon → initial-access` inferred prefix bridge
(GAP Decision 6 Option B) is a deferred decision — the weighted nets
stay observed-only. See the feasibility study sec.4 / sec.9.

In-tactic dwell is the duration catalogue's job
(`tactic_durations.json`, the state-durations handoff), **not** a
self-loop weight — intra-tactic edges were dropped at structural
build time and carry no weight.

