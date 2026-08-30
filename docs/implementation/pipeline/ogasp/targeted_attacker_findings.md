---
status: open — built and verified (rungs 1–6); Gate 0 re-ask pre-registered in §2, results to follow in §4
created: 2026-08-30
updated: 2026-08-30
handoff: 2026-08-30_targeted_attacker_build.md
topic: "The targeted attacker (Brown Scenario 2) built on the movement attacker's host-selection seam under decision A — what was built, how each verification rung was passed, the pre-registered Gate 0 re-ask (committed before any number), and its result."
---

# The targeted attacker — build, verification, and the Gate 0 re-ask

Executes [`2026-08-30_targeted_attacker_build.md`](../../../handoffs/2026-08-30_targeted_attacker_build.md)
under Marc's ruling of 2026-08-30: **decision A** (the sort hook on the shared
core; policy in the movement layer) and the **database set as the default
target** with Brown's `TX` layers for the sweep. §§1–3 were committed before
the Gate 0 harness produced a row; §4 is appended after.

## 1. What was built

| Piece | Where | What |
|---|---|---|
| The policy | `src/mtdsim/l3_simulation/movement/targeting.py` | `choose_target_hosts` (database set, or one host drawn on layer `k` from a seed-derived stream that never touches the substrate's global RNG) and `TargetedSorter` (the inherited distance sort first, then a stable sort by Brown's class: 0 the target, 1 its layer, `d+1` a layer `d` away) |
| The seam | `mtdnetwork/operation/attack_operation.py` | `host_sorter` (None → the old line) and `target_hosts` (empty → old behaviour) on `AttackOperation`; `_do_enum_host` sorts through the hook; the give-up guard spares `target_hosts` (replacing the never-firing `network_type == 0` form); the commented-out targeted termination re-enabled keyed on `target_hosts` |
| The wiring | `movement/run.py::_install_objective` | resolves the target on the seam and installs both hooks; shared by the trace tool so a traced run wires identically; `target_hosts` / `target_layer` on `MovementRunResult` |
| Observability | `MovementRecord.target_class`; `mtdsim.l3_simulation.trace` | the class of the host each selecting row chose (ENUM pop **or** fresh-host re-select — the re-select loop pops through the same core); `--attack-objective targeted [--target-layer k]` on the trace CLI, a header line naming the target, per-row `[popped/re-selected host h (class c, layer l)]`, and a verdict section with pops-by-class and whether the run ended on the target |
| Tests | `tests/l3_simulation/test_movement_attack_objective.py` | 16 tests, rungs 1–5 |

Both arms run the targeted objective through the **same** hooks: the Gate 0
harness installs `_install_objective` on the inherited attacker's
`AttackOperation` exactly as `run_movement` does, so the cross-arm contrast
is one policy on two drivers.

### 1.1 Rungs 1–6, as passed

1. **General arm unchanged.** With the machinery present and uninstalled, an
   explicit `general` run equals an unqualified run field for field; the full
   L3 + action-layer + trace + regression suites pass with every movement and
   baseline golden unchanged (§1.2).
2. **Sorter.** Target first, then its layer, then nearer layers (classes
   non-decreasing); within a class the general order (compared element-wise
   against the inherited sort on the same stack and RNG state); the global
   stream is in the same state after the targeted sort as after the general
   sort (equal draw count).
3. **Give-up.** The core's guard keys on `self.target_hosts` and nothing else
   (source-inspected, comments stripped); the target is never appended to
   `stop_attack`, a non-target is at the threshold.
4. **Termination.** A targeted run at `target_layer=1` ends with
   `reached_objective=True`, fewer than 40 hosts, a terminal `SIM_END` record
   immediately after the reach, and the target's own selection on record as
   class 0.
5. **Determinism.** Same `(profile, seed, target_layer)` twice → identical
   records and target; `targeted` and `general` at one seed first diverge at
   or after the first ENUM pop.
6. **Hand trace** (`aggregate`, seed 1, `v2_partial`, `--target-layer 1`;
   target = host 9): the first five pops are the exposed endpoints (class 2 —
   nothing else is visible yet); at t = 2 005.8 the first internal host to
   become visible on the target's layer (host 13, class 1) is popped ahead of
   everything else; at t = 4 034.2 the fresh-host guard re-selects host 9 —
   the target, class 0 — and `EXPLOIT_VULN` compromises it (`HOST OWNED host 9
   … owns 3/50`), and the very next token event is `END SIM_END`. Pops by
   class `{0: 1, 1: 2, 2: 7}`; the general arm on the same seed runs to the
   horizon owning 18 hosts. The full log is reproducible from the command
   line; nothing in it was edited.

### 1.2 Suite

See §4 for the run that carried this record's commit.

## 2. Pre-registration — the Gate 0 re-ask (committed before any row)

Harness: `data/results/targeted_attacker_build/run_gate0.py`. Unopposed,
**350 seeds**, five movement profiles + the inherited baseline, each arm under
the targeted objective through the same seam, four targets: one host drawn on
**layer 1, 2, 3** (Brown's `TX`) and the **database set** (layer 3, two
hosts). Horizon 15 000 s, mapping `v2_partial`, fresh-host contract on (the
reported configuration), token hold off. 8 400 runs.

**Measures** (the probe's §3.1 verbatim, re-denominated on the drawn target):
reach rate with a seed-level BCa 95 % CI; time-to-target (right-censored at
the horizon); footprint at reach (hosts held when the run ended on the
target); hosts total. Cross-arm: unpaired (D-29).

**Criteria, fixed now:**

- **Gate (probe §3.3).** The targeted objective is non-degenerate on the
  movement arm iff some profile reaches the **layer-1** target in ≥ 20 % of
  unopposed runs. The database/layer-3 target is reported but is not the
  Gate: the probe already established that the deep target is out of the
  breadth cap's reach, and this build changes navigation, not breadth.
- **Directedness (probe §3.2, "better more efficiently").** Among reached
  runs, movement footprint-at-reach < baseline footprint-at-reach for ≥ 1
  profile at ≥ 1 target, non-overlapping CIs, minimum effect 3 hosts.
- **"Better more often"** is reported but expected to fail (the baseline
  floods); it is not required for the Gate.
- **Priors, stated.** From the twelve-seed scan during the build (`aggregate`,
  layer 1): 4/12 reached. Prior for the layer-1 Gate on `aggregate`: reach in
  the 20–40 % band — **near the Gate, either side plausible**. Layer 2: below
  the Gate. Layer 3 / database: ≤ 5 %, consistent with H5's 1.4 %.

**What each outcome means.** Gate holds at layer 1 → the located objective is
usable as an evaluation spine **for a shallow target**, and the under-MTD
matrix (100 seeds, four mechanisms) is the next pre-registered step; H2 is
re-established on it, never carried. Gate fails everywhere → navigation alone
does not lift reach past the breadth cap; B-iii is the binding barrier and
the record says so.

## 3. Scope

Additive; the general arm byte-identical; no golden re-baselined; no
`gen_graph` repair (B1–B3/B6 stand). The inversion headline is spun out
([`2026-08-30_headline_on_restored_substrate.md`](../../../handoffs/2026-08-30_headline_on_restored_substrate.md))
and this record does not touch it. Brown's knowledge assumption — the
attacker knows the target's layer before it can see the target — is his, not
argued fresh (IS-SCN-03: "the attacker can identify target characteristics").
No time-domain spec for Scenario 2 exists (IS-SCN-06): extension, not
restoration.
