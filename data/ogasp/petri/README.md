# `data/ogasp/petri/` — L3a OGASP weighted tactic-place Petri nets

Five **weighted** structural tactic-place Petri nets — one per GASP
class plus the **aggregate (null) profile** over the union of all
flows — built in SNAKES with a single moving black token. Shape +
W-A flow-proportion weights; no timing, rewards, MTD or CTMC (those
are later stages). Stages 1–2 (L3a) of the OGASP Petri-net
workstream. The timeline runner's artefacts live beside this
directory under [`../timeline/`](../timeline/); the shared duration
catalogue and the index are at the [`data/ogasp/` root](../README.md).

- **Build code:** [`src/mtdsim/l3_simulation/petri/`](../../../src/mtdsim/l3_simulation/petri).
- **Design / rationale:** [`docs/implementation/pipeline/ogasp/petri_feasibility.md`](../../../docs/implementation/pipeline/ogasp/petri_feasibility.md)
  (the base structural net is GO-unconditional, sec.8).
- **Locked P/T/F/M mapping:** places = ATT&CK tactics; transitions =
  inter-tactic tactic-pairs (each tracing to >=1 GASP technique-edge — the
  no-synthesis invariant); flow = `place[a] -> T -> place[b]`; marking =
  one black token in `reconnaissance` (else `initial-access`).
- **Weight regime (D3, dispositioned in
  [`docs/implementation/metrics_semantics.md`](../../../docs/implementation/metrics_semantics.md) §(f)):**
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
| `synthetic_overlay.json` | **computed** | the **synthetic overlay** (declared pre-intrusion structure) — the bidirectional pre-intrusion connective tissue (forward chain `reconnaissance → resource-development → initial-access`, share 1.0 each; backward regression bridge `initial-access → reconnaissance`, declared share) for exactly the profiles whose observed corpus leaves the pre-intrusion band detached; flagged synthetic, no flow backing; composed at net construction, never folded into the observed nets |
| `outcome_overlay.json` | **authored (declared)** | the **outcome (policy) overlay** — the success/failure conditional-likelihood weighting over the whole directed tactic-pair set, composed multiplicatively with the base weights and the substrate's binary verdict at runtime; a policy layer distinct from the structural synthetic overlay (design: `docs/implementation/pipeline/ogasp/success_failure_overlay_design.md`) |
| `_viz/<profile>.png` / `.svg` | gitignored | **tactic-state diagram** — kill-chain L→R; token in its seed; entry green, objective orange, sinks double-outlined; edge width/opacity = W-A weight (uniform absolute scale across the five nets); unreachable-from-token places dashed |
| `_viz/<profile>_snakes.png` | gitignored | the **formal SNAKES net** (bipartite places + transition bars) — faithful but dense; kept as a provenance artefact |
| `_viz/_reachability.png` | gitignored | **headline chart** — tactics reachable from the recon token vs from any entry, per profile |

The timeline-runner artefacts (schema contract, example, behavioural
report, seeded library, timeline figures) live under
[`../timeline/`](../timeline/).

All `_viz/` figures are gitignored (regenerable; mirrors the `data/gasp/_*`
pattern). The diagrams need graphviz `dot` + the `graphviz` Python package;
the headline chart needs `matplotlib` (both house dependencies of
`data/gasp/_viz/gasp_viz.py`).

## Structural summary

| Profile | Flows (raw → dedup) | Places | Transitions | Inter-tactic edges | Self-loops dropped | Objective reachable from recon | recon→initial-access |
|---|---|--:|--:|--:|--:|---|---|
| `objective_exfiltration` | 19 → 14 | 15 | 109 | 358 | 50 | yes | bridged |
| `objective_impact` | 7 → 6 | 13 | 76 | 217 | 29 | yes | bridged |
| `objective_exfiltration_impact` | 7 → 5 | 14 | 72 | 205 | 24 | **no** | **disconnected** |
| `objective_none_c2` | 5 → 4 | 13 | 57 | 130 | 11 | **no** | **disconnected** |
| `aggregate` | 38 → 29 | 15 | 122 | 422 | 56 | yes | bridged |

The aggregate's declared objective set is the union of the four
class-semantic objectives (command-and-control, exfiltration, impact)
— a recorded choice; the null envelope has no single operational
objective. Note the operator clusters span classes (e.g. the CISA
AA22-138B trio splits across `objective_exfiltration` and `objective_none_c2`),
so deduplication can remove flows from several classes at once —
dedup class sizes are 14 / 7 / 4 / 4 (Σ = 29).

## Divergence from the aggregate (headline)

- **objective_exfiltration** — mean per-place JSD 0.1876 vs aggregate; does NOT exceed the shuffled-label null p95 (0.2248).
- **objective_impact** — mean per-place JSD 0.3330 vs aggregate; does NOT exceed the shuffled-label null p95 (0.4466).
- **objective_exfiltration_impact** — mean per-place JSD 0.2894 vs aggregate; does NOT exceed the shuffled-label null p95 (0.4781).
- **objective_none_c2** — mean per-place JSD 0.3348 vs aggregate; does NOT exceed the shuffled-label null p95 (0.5101).

Full tables, discriminators and the verdict paragraph:
[`divergence_report.md`](divergence_report.md).

## The prefix gap (inspect-the-base finding)

The marking seeds the token in `reconnaissance`. On the observed-only
base the corpus starts at the point of detection, so the
`reconnaissance → initial-access` link is near-absent — and it shows up
directly in the single-token reachability:

- **objective_exfiltration** — BRIDGED by 1 direct recon->initial-access edge(s) [('T1593', 'T1195')] -- a thin, fragile prefix link
- **objective_impact** — BRIDGED by 1 direct recon->initial-access edge(s) [('T1593', 'T1195')] -- a thin, fragile prefix link
- **objective_exfiltration_impact** — DISCONNECTED -- reconnaissance cannot reach initial-access; the recon place is an island (the observed-only prefix gap)
- **objective_none_c2** — DISCONNECTED -- reconnaissance cannot reach initial-access; the recon place is an island (the observed-only prefix gap)
- **aggregate** — BRIDGED by 1 direct recon->initial-access edge(s) [('T1593', 'T1195')] -- a thin, fragile prefix link

Consequence: in the classes where recon is an island, a recon-seeded
token cannot reach the objective over the observed structure alone.
The **synthetic overlay** resolves this:
[`synthetic_overlay.json`](synthetic_overlay.json) declares the
bidirectional pre-intrusion connective tissue for exactly those
profiles — the forward chain `reconnaissance → resource-development →
initial-access` (share 1.0 each; resource-development is a forward
pass-through) plus the backward regression bridge `initial-access →
reconnaissance` (declared share) so a failed attacker can fall back
into the pre-intrusion band — all flagged synthetic, no flow backing,
composed into the net at construction time (`build_all_profiles` /
`synthetic_overlay.apply_synthetic_overlay`; on by default, observed-only via
`with_synthetic_overlay=False`). The observed nets in the
`*_structural.json` artefacts stay observed-only — the no-synthesis
invariant on `transitions` is untouched. Overlay off + an
`initial-access` seed remains the comparison arm. See the feasibility
study sec.4 / sec.9 for the observed-only reading.

In-tactic dwell is the duration catalogue's job
([`../tactic_durations.json`](../tactic_durations.json), the
state-durations workstream), **not** a
self-loop weight — intra-tactic edges were dropped at structural
build time and carry no weight.

