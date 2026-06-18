---
status: open
created: 2026-06-18
---

# Build the L3a Petri-net MVP — four un-weighted structural tactic-place nets in SNAKES, from the GASP profiles

> **This is the concrete first build (Stage 1) of the broader plan in
> [`./2026-06-18_l3_ogasp_petri_implementation.md`](./2026-06-18_l3_ogasp_petri_implementation.md);
> the *why* is the feasibility study at
> [`../notes/2026-06-18_l3_petri_feasibility.md`](../notes/2026-06-18_l3_petri_feasibility.md).**
> Read those for rationale; this handoff is code-ready and self-contained for the
> build itself. **Scope: the un-weighted *structural* net only — just the shape.**
> No rates, no timing, no rewards, no MTD, no CTMC. Those are later stages.
>
> **This is THE direct next step.** It is **GO-unconditional** — it needs *none*
> of the feasibility study's four go-conditions and *none* of the roadmap's
> Stage 0 governance (those gate the *analytical numbers*, Stage 2 onward, not
> this structural net).

## State of play

- **What exists:** the four L2 GASP class subgraphs are committed and canonical
  at [`../../data/gasp/`](../../data/gasp/) (`gasp_<class>.json`, each a
  `SubgraphView` = `{class_name, node_set, edge_set, provenance}`), derived from
  [`../../data/gap/gap_v0.5.json`](../../data/gap/gap_v0.5.json). The component
  mapping below is **locked** (this session).
- **What this MVP is:** four *separate* ordinary Petri nets (one per class), built
  in **SNAKES**, with **tactic places**, **inter-tactic GASP edges as
  transitions**, and a **single moving black token**. Plus the structural
  analyses you get for free with no weighting, and a rendered diagram per class.
- **What this MVP is NOT** (all deferred to later stages): firing rates / timing,
  the CTMC solve (MTTC/ASR), SRN rewards, the MTD competing transition, the
  one-shared-net (D4) optimisation, the technique-level faithful net (D2), the
  per-class slices (D3), and the recon→initial-access inferred prefix bridge
  (GAP Decision 6 — inspect the base first, *then* decide).
- **Code/outputs land** under `src/mtdsim/l3_simulation/` (the pipeline pointer
  that currently holds no code), tests under `tests/l3_simulation/`, diagrams
  under `data/ogasp/_viz/` (new, gitignored like the other `_viz/`).

## The locked component mapping (P, T, F, M)

| Component | What it is | Source (already in the artefacts) |
|---|---|---|
| **Places (P)** | one place per **ATT&CK tactic** present in the class | distinct `gap_v0.5.json` `nodes[t].primary_tactic` over the class `node_set`. Counts: **pure_steal 15, pure_impediment 14, double_extortion 14, infrastructure_setup 13** (infra has no `impact`/`exfiltration`). |
| **Transitions (T)** | one per **inter-tactic GASP edge** `u→v` where `tactic(u) ≠ tactic(v)` — the technique-effected move between tactics | `gasp_<class>.json` `edge_set` joined to `primary_tactic`. Inter-tactic edge counts: **363 / 225 / 201 / 136**; intra-tactic (same-tactic) edges → **self-loops, dropped** (50 / 29 / 24 / 12). |
| **Flow relation (F)** | **bipartite**: `place[tactic(u)] →(input arc)→ T →(output arc)→ place[tactic(v)]`. A GASP edge becomes a *transition + two arcs*, never a place→place arc. | the `edge_set` routing above |
| **Marking (M)** | **one black token = "where the attack is now"** (single moving token, pure path traversal). Initial: token in `reconnaissance` (else `initial-access`). | `is_entry` / `start_refs`; reachable-set ≤ #places (≤15) so it is trivially tractable |

**Transition granularity — one decision to make.** Two valid options; pick one
and record it:
- **(recommended, legible) one transition per inter-tactic *tactic-pair*** — the
  net is then the tactic-FSM (matches the existing
  [`../../data/gasp/_viz/gasp_<class>_tactic_fsm.png`](../../data/gasp/_viz/)
  diagrams). Record the contributing technique-edges as a transition attribute so
  the no-synthesis check still traces every transition to GASP edges. Pair counts:
  **109 / 83 / 72 / 57**.
- **(alternative, finest) one transition per inter-tactic *technique-edge*** — 1:1
  with GASP edges (trivial provenance) but a busier diagram (225 transitions for
  pure_impediment).

Both preserve the no-synthesis invariant; the tactic-pair view is the cleaner MVP
"shape." The token semantics and reachability are identical either way.

## Recommended approach

**Step 0 — Env.** SNAKES is not in [`../../environment.yml`](../../environment.yml).
`pip install snakes`; rendering needs graphviz `dot` on PATH for `net.draw(...)`.
Note the addition in the PR description (the env-reconciliation item is already
open per [`../specs/repo_conventions.md`](../specs/repo_conventions.md)).

**Step 1 — Load + index.** Read `gap_v0.5.json` → build `technique → primary_tactic`
(and `is_entry` / `is_objective`). Read each `gasp_<class>.json` → `node_set`,
`edge_set`.

**Step 2 — Build one net per class.** Places = distinct tactics over `node_set`.
For each inter-tactic edge (or tactic-pair), add a transition + input arc from the
source-tactic place + output arc to the target-tactic place. Drop intra-tactic
self-loops. Put one token in the entry place.

**Step 3 — SNAKES skeleton** (single black token; sketch, not gospel):

```python
import snakes.plugins
snakes.plugins.load('gv', 'snakes.nets', 'nets_gv')
from nets_gv import PetriNet, Place, Transition, Value

def build_structural_net(class_name, node_set, edge_set, tactic_of, entry_tactic):
    net = PetriNet(class_name)
    tactics = sorted({tactic_of[t] for t in node_set})
    for tac in tactics:
        net.add_place(Place(tac, [1] if tac == entry_tactic else []))  # 1 = the moving token
    pairs = {}  # (src_tac, tgt_tac) -> [technique-edges] for provenance
    for u, v in edge_set:
        a, b = tactic_of[u], tactic_of[v]
        if a == b:
            continue                       # intra-tactic -> self-loop, dropped
        pairs.setdefault((a, b), []).append((u, v))
    for (a, b), prov in pairs.items():
        t = f'{a}__to__{b}'
        net.add_transition(Transition(t))  # provenance: prov (record alongside)
        net.add_input(a, t, Value(1))      # consume the token from place a
        net.add_output(b, t, Value(1))     # produce it into place b
    return net
```

With one token, when it sits in place `a`, *every* transition `a→*` is enabled;
firing one moves the token (the attacker picks a next tactic). Cycles (e.g.
`execution ↔ stealth`) are fine — the single-token reachability set is just the
tactics reachable from the entry (≤15 markings).

**Step 4 — Structural analyses (the MVP's actual payoff, no weights needed).**
Emit per class: reachable tactic-set from entry; **is the objective tactic
reachable?** (`impact`/`exfiltration` for the three objective classes;
`command-and-control` for infrastructure_setup); deadlock/sink tactics;
shortest & longest entry→objective tactic path; and **the prefix-gap probe — is
`reconnaissance` connected to `initial-access`?** (expected: *no* — ~1 recon→IA
edge in the whole GAP; surface this, it is the deduction the next decision rests
on). Reachability over a single black token can be a plain BFS over the place
graph, or SNAKES `StateGraph` — either is fine at ≤15 states.

**Step 5 — Render + persist.** `net.draw('data/ogasp/_viz/<class>.png')` per class;
write a small `data/ogasp/README.md` and a structural-summary JSON
(places, transitions, reachable-set, objective-reachable, prefix-connected) per
class.

*Alternatives considered:* one shared 15-place net with class-tagged transitions
(the D4 design) — deferred; four separate nets is the simpler MVP and matches
"from the profiles." Technique-level places (D2) — deferred; richer shape but not
"as basic as it gets."

## Validation gate

The MVP is done when:
1. Four nets build in SNAKES with place counts **15 / 14 / 14 / 13** and the
   inter-tactic transition counts above (self-loops excluded).
2. **No-synthesis test passes:** every transition traces to ≥1 GASP edge in the
   class `edge_set` (mechanical); no place/transition is invented.
3. A **reachability + objective-reachability report** is emitted per class, and
   the **recon→initial-access prefix gap is surfaced** (connected: yes/no).
4. A **diagram per class** renders to `data/ogasp/_viz/`.
5. The build is **deterministic** (sorted iteration; same inputs → same net) and
   runnable via a documented entry point (mirror the L2 pattern:
   `PYTHONPATH=src python -m mtdsim.l3_simulation.petri`).

## Hard constraints

- **Structural only** — no rates, timing, rewards, MTD, or CTMC in this MVP.
- **Single moving token** — not multi-token (that is the state-space explosion the
  analytical design avoids; feasibility study §6.1).
- **No-synthesis invariant** ([`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)
  §(a)): every transition traces to a GASP edge; class memberships consumed
  unchanged. The recon→IA prefix bridge is **out of scope** (inspect first).
- **v0.5 data only** ([`../../data/gap/gap_v0.5.json`](../../data/gap/gap_v0.5.json)
  + the four [`../../data/gasp/`](../../data/gasp/) JSONs). Do **not** import the
  primer's stale `mtdsim.attacker.gap` layout or `gap_v0.4_latest.json`.
- Determinism, branch hygiene (work on `feat/l3-ogasp-petri` or a child; never
  push), Australian English — per
  [`../specs/session_workflow.md`](../specs/session_workflow.md).

## Reading list

- [`../notes/2026-06-18_l3_petri_feasibility.md`](../notes/2026-06-18_l3_petri_feasibility.md)
  §4 (what L2 hands forward, incl. the prefix gap) and §6.2 (why no weights yet).
- This handoff's **component mapping** table (the locked P/T/F/M).
- [`./2026-06-18_l3_ogasp_petri_implementation.md`](./2026-06-18_l3_ogasp_petri_implementation.md)
  — the broader staged plan this MVP is Stage 1 of.
- The 2026-05-02 SNAKES primer notebook on `feat/replay-viz`
  (`notebooks/2026-05-02_MTDSim_PetriNetPrimer.ipynb`) — **SNAKES API only**
  (`PetriNet`/`Place`/`Transition`/`add_input`/`add_output`/`draw`); its GAP-v0.4
  data and rate code are **stale**, do not copy.
- [`../../data/gasp/`](../../data/gasp/) `gasp_<class>.json` + `README.md`, and
  the existing `_viz/gasp_<class>_tactic_fsm.png` (the shape the MVP net mirrors).

## Out of scope (explicitly)

Rates / timing / weights (Stage 2); the CTMC solve and MTTC/ASR; SRN rewards; the
MTD transition; the one-shared-net (D4) and technique-level (D2) encodings; the
recon→initial-access inferred prefix bridge (deferred — base first); editing the
canonical specs.
