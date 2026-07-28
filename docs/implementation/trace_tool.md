---
status: living
created: 2026-07-28
updated: 2026-07-28
---

# The trace tool — an event-by-event log of the substrate contest

**What it is.** [`mtdnetwork/trace.py`](../../mtdnetwork/trace.py) renders one substrate run as a colour-coded, chronologically ordered event log — attacker phases, MTD deployments, network mutations, interrupts and their confusion penalties — followed by a verdict that scores the contest and flags the two common misconfigurations (every mutation missing; more mutations queued than the network can absorb). It answers what the summary statistics cannot: *how* a run went, not just who won. Both machine-greppable (`--no-colour`, one event per line, stable `time · actor · message` shape) and human-readable.

```
python -m mtdnetwork.trace --scheme none            # the attacker, unopposed (control)
python -m mtdnetwork.trace --scheme simultaneous    # the same seed, defended
python -m mtdnetwork.trace --only attacker,compromise --no-colour > run.log
python -m mtdnetwork.trace --quiet                  # verdict only
```

**Provenance.** Ported 2026-07-28 from `main` (commit `31ce3be`, where it lives as `mtdsim/trace.py` against the rebuilt standalone simulator), with imports retargeted at dev's inherited substrate (`mtdnetwork.*`). The `main` and dev substrates have diverged; the port re-verified every hooked seam against dev's code and the full test file passes unchanged.

## What sessions should use it for

- **Verifying a substrate change.** Trace the same seed before and after; diff the event streams. A change that should be behaviour-neutral must produce identical logs; a change that should matter shows up as a legible narrative difference, not a bare metric delta.
- **Pinpointing a bug.** The log localises *where in the contest* a number went wrong — e.g. a hit rate of 0% distinguishes a scheduling problem from a strength problem; a foothold that never happens distinguishes a stalled attacker from a winning defence.
- **Demonstrating the simulator.** An undefended run and a defended run at one seed make the point of MTD directly visible.

## Design invariants (the only fixed part)

Instrumentation is **read-only** and **draws no randomness**: every wrapper delegates to the original seam unchanged and only records. A traced run is therefore identical to the same seed untraced. [`tests/test_trace.py`](../../tests/test_trace.py) pins this (state and full attack-record equality), plus chronological ordering, all-actors coverage, tally/stream consistency, and that a defence measurably delays the foothold.

## This is a living tool — extend it

Deliberately **dynamic, not frozen**. Sessions that need a seam the tracer doesn't narrate (L3 movement-driver decisions, controller outcomes, new MTD strategies, new tallies for a new question) should add hooks rather than write one-off print debugging — the instrumentation accumulates value that ad-hoc logging throws away. The contract for any extension:

1. wrappers delegate unchanged and write no simulator state;
2. no randomness drawn inside instrumentation;
3. `tests/test_trace.py` still passes — the non-perturbation test is the gate that makes every extension trustworthy.

Extensions that survive use become part of the tool; the long-run intent is a battle-tested demo instrument, hardened by sessions using it in anger. Record substantive extensions by bumping `updated` here and noting the new seam.
