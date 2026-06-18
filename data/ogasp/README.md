# `data/ogasp/` — L3a OGASP structural Petri nets

Four un-weighted **structural** tactic-place Petri nets (one per GASP
class), built in SNAKES with a single moving black token. The shape
only — no rates, timing, weights, rewards, MTD or CTMC (those are later
stages). This is Stage 1 (L3a) of the OGASP Petri-net workstream.

- **Build code:** [`src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri).
- **Design / rationale:** [`docs/notes/2026-06-18_l3_petri_feasibility.md`](../../docs/notes/2026-06-18_l3_petri_feasibility.md)
  (the base structural net is GO-unconditional, sec.8).
- **Locked P/T/F/M mapping:** places = ATT&CK tactics; transitions =
  inter-tactic tactic-pairs (each tracing to >=1 GASP technique-edge — the
  no-synthesis invariant); flow = `place[a] -> T -> place[b]`; marking =
  one black token in `reconnaissance` (else `initial-access`).

## Rebuild

```sh
pip install snakes                 # not in environment.yml; needs graphviz `dot` for diagrams
PYTHONPATH=src python -m mtdsim.l3_simulation.petri   # write <class>_structural.json x4 + _viz/<class>.png x4
PYTHONPATH=src python -m pytest tests/l3_simulation/  # validation gate
```

## Contents

| Path | Tracked? | What |
|---|---|---|
| `<class>_structural.json` | **computed** | net shape (places, transitions + per-transition GASP provenance) + structural report |
| `_viz/<class>.png` | gitignored | rendered diagram (regenerable; mirrors the `data/gasp/_*` pattern) |

## Structural summary

| Class | Places | Transitions | Inter-tactic edges | Self-loops dropped | Objective reachable from recon | recon→initial-access |
|---|--:|--:|--:|--:|---|---|
| `pure_steal` | 15 | 109 | 363 | 50 | yes | bridged |
| `pure_impediment` | 14 | 83 | 225 | 29 | yes | bridged |
| `double_extortion` | 14 | 72 | 201 | 24 | **no** | **disconnected** |
| `infrastructure_setup` | 13 | 57 | 136 | 12 | **no** | **disconnected** |

## The prefix gap (inspect-the-base finding)

The marking seeds the token in `reconnaissance`. On the observed-only
base the corpus starts at the point of detection, so the
`reconnaissance → initial-access` link is near-absent — and it shows up
directly in the single-token reachability:

- **pure_steal** — BRIDGED by 1 direct recon->initial-access edge(s) [('T1593', 'T1195')] -- a thin, fragile prefix link
- **pure_impediment** — BRIDGED by 1 direct recon->initial-access edge(s) [('T1593', 'T1195')] -- a thin, fragile prefix link
- **double_extortion** — DISCONNECTED -- reconnaissance cannot reach initial-access; the recon place is an island (the observed-only prefix gap)
- **infrastructure_setup** — DISCONNECTED -- reconnaissance cannot reach initial-access; the recon place is an island (the observed-only prefix gap)

Consequence: in the classes where recon is an island, a recon-seeded
token cannot reach the objective; seeding at `initial-access` (the
corpus's dominant real entry) is required. Whether to add the
literature-grounded `recon → initial-access` inferred prefix bridge
(GAP Decision 6 Option B) is the next decision — **deferred by intent**:
inspect this base first. See the feasibility study sec.4 / sec.9.

