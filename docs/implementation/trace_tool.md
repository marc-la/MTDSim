---
status: living
created: 2026-07-28
updated: 2026-07-28
---

# The trace tool — an event-by-event log of a run, across every layer

**What it is.** A family of two entry points over one shared core, rendering a run as a colour-coded, chronologically ordered event log followed by a verdict that scores the contest. Both are machine-greppable (`--no-colour`, one event per line, stable `time · actor · message` shape) and human-readable. It answers what the summary statistics cannot: *how* a run went, not just who won.

- [`mtdnetwork/trace.py`](../../mtdnetwork/trace.py) — the **substrate tracer**: the native 6-phase attacker vs the MTD defence (attacker phases, deployments, mutations, interrupts and their confusion penalties).
- [`src/mtdsim/l3_simulation/trace.py`](../../src/mtdsim/l3_simulation/trace.py) — the **unified L3 tracer**: a movement-layer run narrated across all three layers on the one shared clock — the token walking the class net, the controller's dispatch/verdict/routing decisions, and the substrate events underneath. It imports the substrate tracer's core (`Event`, `Tracer`, the hook installer, the palette); the dependency direction stays `mtdsim → mtdnetwork`.

```
python -m mtdnetwork.trace --scheme none            # native attacker, unopposed (control)
python -m mtdnetwork.trace --scheme simultaneous    # the same seed, defended
python -m mtdnetwork.trace --only attacker,compromise --no-colour > run.log

PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate                       # movement run, unopposed
PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate --scheme simultaneous # defended
PYTHONPATH=src python -m mtdsim.l3_simulation.trace pure_steal --mapping v2_partial # select the controller mapping
PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate --only token,controller --quiet
```

**Provenance.** The substrate tracer was ported 2026-07-28 from `main` (commit `31ce3be`, where it lives as `mtdsim/trace.py` against the rebuilt standalone simulator), with imports retargeted at dev's inherited substrate (`mtdnetwork.*`). The `main` and dev substrates have diverged; the port re-verified every hooked seam against dev's code and the full test file passes unchanged (one adaptation: dev's `MTDScheme.suspend_mtd` takes `mtd_strategy` by keyword). The unified L3 tracer was added the same day — the tool's first extension under its own charter.

## What sessions should use it for

- **Verifying a change** (substrate or L3). Trace the same seed before and after; diff the event streams. A change that should be behaviour-neutral must produce identical logs; a change that should matter shows up as a legible narrative difference, not a bare metric delta.
- **Pinpointing a bug.** The log localises *where in the contest* a number went wrong — e.g. a hit rate of 0% distinguishes a scheduling problem from a strength problem; a foothold that never happens distinguishes a stalled attacker from a winning defence; a 1%-success walk under `v1_ckc_total` shows *which* dispatches blocked on which preconditions.
- **Demonstrating the simulator.** An undefended run and a defended run at one seed make the point of MTD directly visible; a `v1_ckc_total` run next to a `v2_partial` run makes the mapping's effect visible.

## What the unified L3 trace captures (the design elements)

The substrate actors (ATTACKER, COMPROMISE, DEFENDER, MUTATION, INTERRUPT, NETWORK) carry over unchanged — the same hooks fire, so cross-layer events interleave. Two actors join them:

| Actor | Events | The design element it makes visible |
|---|---|---|
| **TOKEN** | `ENTER` (place + visit count) · `DWELL` (the sampled draw **vs the catalogue mean**) · `STEP` (place → verb → verdict → next place, with what the tactic's time **bought** and whether the substrate added anything) · `END` (terminal tag) | The S3 stochastic-timing regime per event; the walk's shape; the per-step time decomposition; the terminal reason (objective / stall / sink / horizon / `MAX_EVENTS`) — never an unexplained stop |
| **CONTROLLER** | `DISPATCH` (tactic → verb, or dwell-only, naming the mapping version) · `VERDICT` (substrate outcome → success/failure, incl. interrupt-as-failure) · `ROUTE` (candidates, suppressed edges, the conditioned next-place distribution) · `STALL` (every out-edge suppressed) | The selected mapping actually deciding; the verdict adapter's reading of each outcome; the M2 composition conditioning the routing; the stall as an explicit event |

Blocked dispatches (`PRECONDITION_UNMET`) deliberately emit **no** `VERDICT` event — the controller never judged; the failure is a movement-layer routing policy — and the `STEP` line says `blocked — precondition unmet` instead. The verdict section then reports: the run's identity (profile / mapping / overlay / timing regime / scheme / seed), how the token moved (steps, distinct places, top places by time, terminal reason), the controller's decisions (dispatches by verb, success rate, blocked count — the coupling surface as data, interrupts split mid-verb vs mid-dwell), **where the time went** (dwelling vs running verbs vs interrupt penalties — the action-budget decomposition), the defence's tallies, and the substrate ground truth (foothold, hosts owned).

**How it instruments.** The driver takes its collaborators by injection, so `phase_for` / `compose` / `verdict_of` / `timing.draw` are wrapped in recording proxies — no monkeypatching. Only two substrate seams are class-patched (with undo), because the driven arm bypasses the seams the substrate tracer hooks: `AttackOperation.step` (verbs run through the carve, not `_execute_*`) and `apply_mtd_interrupt_cost` (the driven arm's penalty path — it never calls `_handle_interrupt`). The per-step TOKEN summary is derived from the driver's own `MovementRecord` stream as appended, the one instrumentation point that cannot disagree with what the run records.

## Design invariants (the only fixed part)

Instrumentation is **read-only** and **draws no randomness**: every wrapper delegates to the original seam unchanged and only records. A traced run is therefore identical to the same seed untraced. [`tests/test_trace.py`](../../tests/test_trace.py) pins this for the substrate tracer (state and full attack-record equality); [`tests/l3_simulation/test_movement_trace.py`](../../tests/l3_simulation/test_movement_trace.py) pins it for the unified tracer (**record-for-record equality against `run_movement`**, undefended and defended), plus chronological ordering, all-layers coverage, dwell-only narration under `v2_partial`, and tally/record-stream consistency.

## This is a living tool — extend it

Deliberately **dynamic, not frozen**. Sessions that need a seam the tracer doesn't narrate (new MTD strategies, distinguishing dwell-cut from verb-cut interrupts at the event level, a machine-readable JSON emitter, new tallies for a new question) should add hooks rather than write one-off print debugging — the instrumentation accumulates value that ad-hoc logging throws away. The contract for any extension:

1. wrappers delegate unchanged and write no simulator state;
2. no randomness drawn inside instrumentation;
3. the non-perturbation tests still pass — [`tests/test_trace.py`](../../tests/test_trace.py) and [`tests/l3_simulation/test_movement_trace.py`](../../tests/l3_simulation/test_movement_trace.py) are the gate that makes every extension trustworthy.

Extensions that survive use become part of the tool; the long-run intent is a battle-tested demo instrument, hardened by sessions using it in anger. Record substantive extensions by bumping `updated` here and noting the new seam.

**Extension log.**

- 2026-07-28: the unified L3 tracer (`mtdsim/l3_simulation/trace.py`) — TOKEN and CONTROLLER actors over the movement layer, collaborator-proxy instrumentation, the `run_movement` parity gate.
- 2026-07-28: **narration re-cut for S3-R**, where the movement layer supplies every unit of the attacker's time. The per-step split was `dwell + verb`, which became degenerate the moment the substrate's action costs were retired — every line read `+ verb 0.0`. It now reports what the tactic's time *bought* (the action ran / the substrate could not action it / the place dispatches nothing) and states the substrate's residual, so the regression the ruling forbids — a substrate cost creeping back on top — is visible in the log rather than only in a test. The verdict section gained the matching decomposition and an explicit `!!` line if that residual is ever non-zero. Also fixed: the catalogue mean printed with `:.0f`, which rendered the exploit-shaped anchor of 4.5 as "4" through round-half-even — the one figure a reader checks the regime against.
