---
status: open — built, verified (rungs 1–7); Gate 0 result landed 2026-08-30 (§4); the next pre-registered step (under-MTD matrix) awaits Marc
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

885 passed / 248 skipped across `tests/l3_simulation`, the action-layer
disposition and carve suites, the trace and crash-fix regression suites, with
the build present (`7bbce690`); every movement and baseline golden unchanged.

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

## 4. Gate 0 result (8 400 runs, 2026-08-30)

Rows: `data/results/targeted_attacker_build/gate0_rows.csv` (untracked, regenerable
from the harness); the summary table as printed by `analyse_gate0.py` is
tracked beside it as `gate0_summary.md`. BCa 95 % CIs, 2 000 resamples.

| target | arm / profile | reach | 95 % CI | reached | footprint at reach [CI] | median TTT (s) | mean hosts |
|---|---|--:|--|--:|--:|--:|--:|
| **L1** | **baseline** | **0.777** | [0.731, 0.820] | 272 / 350 | 13.1 [12.1, 14.2] | 4 586 | 16.8 |
| L1 | **aggregate** | **0.383** | [0.331, 0.431] | 134 / 350 | **5.8** [5.3, 6.4] | 7 311 | 7.2 |
| L1 | objective_exfiltration | 0.126 | [0.094, 0.163] | 44 / 350 | 4.3 [3.8, 5.1] | 5 012 | 2.4 |
| L1 | objective_impact | 0.063 | [0.043, 0.094] | 22 / 350 | 3.8 [3.1, 5.2] | 3 519 | 1.6 |
| L1 | objective_exfiltration_impact | 0.054 | [0.034, 0.083] | 19 / 350 | 4.7 [4.0, 5.9] | 3 897 | 1.9 |
| L1 | objective_none_c2 | 0.000 | — | 0 / 350 | — | — | 0.1 |
| L2 | baseline | 0.671 | [0.623, 0.720] | 235 / 350 | 18.9 [17.9, 20.0] | 7 273 | 21.4 |
| L2 | aggregate | 0.211 | [0.171, 0.254] | 74 / 350 | 8.3 [7.6, 9.0] | 10 414 | 8.6 |
| L2 | objective_exfiltration | 0.054 | [0.034, 0.083] | 19 / 350 | 6.5 [5.5, 7.8] | 8 410 | 2.6 |
| L2 | objective_impact | 0.014 | [0.006, 0.031] | 5 / 350 | 7.2 | 4 778 | 1.7 |
| L2 | objective_exfiltration_impact | 0.011 | [0.003, 0.026] | 4 / 350 | 8.2 | 5 079 | 2.1 |
| L3 | baseline | 0.580 | [0.531, 0.632] | 203 / 350 | 23.3 [22.3, 24.6] | 8 884 | 25.3 |
| L3 | aggregate | 0.094 | [0.066, 0.126] | 33 / 350 | 10.5 [9.5, 11.5] | 11 681 | 9.1 |
| L3 | objective_exfiltration | 0.026 | [0.011, 0.046] | 9 / 350 | 8.1 | 8 819 | 2.7 |
| L3 | other three profiles | 0.000 | — | 0 / 350 | — | — | 0.1–2.1 |
| db | baseline | 0.646 | [0.594, 0.694] | 226 / 350 | 23.5 [22.3, 24.6] | 9 145 | 24.3 |
| db | aggregate | 0.097 | [0.071, 0.134] | 34 / 350 | 9.9 [9.0, 10.8] | 11 426 | 9.1 |
| db | objective_exfiltration | 0.023 | [0.011, 0.043] | 8 / 350 | 8.2 | 7 797 | 2.7 |
| db | other three profiles | ≤ 0.009 | — | ≤ 3 / 350 | — | — | 0.1–2.1 |

### 4.1 The pre-registered criteria, ruled

- **The Gate holds — at layer 1, on `aggregate`.** 38.3 % [33.1, 43.1] against
  the 20 % bar, the whole CI above it. Layer 2 is on the bar (21.1 %
  [17.1, 25.4] — point above, CI straddling: *not* ruled as holding). Layer 3
  and the database set fail it (9.4 %, 9.7 %). The prior (20–40 % band at layer
  1) was right. The objective-conditioned profiles fail the Gate at every
  depth: `objective_exfiltration` reaches 12.6 % at layer 1, the two impact
  profiles ≤ 6.3 %, `objective_none_c2` never — the profiles that dispatch
  fewer compromise verbs cannot convert navigation into reach.
- **Directedness — won, at every target.** Among reached runs the movement
  attacker's footprint at reach is **5.8 vs 13.1** at layer 1, 8.3 vs 18.9 at
  layer 2, 10.5 vs 23.3 at layer 3, 9.9 vs 23.5 on the database set — CIs
  non-overlapping everywhere, effects of 7–14 hosts against the 3-host
  minimum. Every reaching profile shows it (`objective_exfiltration` 4.3 at
  layer 1). This is the signal the probe's five lucky reaches only hinted at,
  now measured: **given navigation, the movement attacker reaches a located
  target with less than half the collateral the inherited attacker needs.**
- **More often — lost, as predicted.** The baseline reaches every target more
  often (0.58–0.78) because it floods; under the targeted objective it stops
  on the target, so its mean footprint falls from 39.7 (probe §5) to
  16.8–25.3 — it too is now directed, and still needs twice the hosts.
- **Time-to-target:** the baseline is faster at every depth (4 586 vs 7 311 s
  at layer 1) — the movement attacker's per-tactic dwell is the declared
  APT tempo, so this is consistent with the model, not a finding against it.

### 4.2 What navigation bought, against the probe

On the deep (database) target the same attacker went from **1.4 %** reach
(H5, fresh-host contract, general objective) to **9.7 %** under the targeted
objective — a seven-fold lift from host selection alone, with no change to
breadth (9.1 hosts total, against H5's 7.9) — and still short of the Gate.
So the probe's ranking is confirmed with a sharper edge: **B-i (no
navigation) was the binding barrier for a shallow target and is lifted; B-iii
(the breadth cap) is the binding barrier for a deep one and is not.** A
directed attacker that owns ~9 hosts at the horizon cannot reliably reach a
layer-3 host through a four-layer network whatever order it prefers.

### 4.3 What this means for the fork (probe §3.4, §7.3)

The Option-B′ measurement Marc asked for has been made, and it flips the
probe's fork **for a shallow target**: the located objective is non-degenerate
on `aggregate` at layer 1 (and marginal at layer 2), and the movement attacker
reaches it *more efficiently* than the inherited attacker — the pre-registered
"better" threshold is met on the efficiency disjunct. Per the pre-registration
the next step is the **under-MTD matrix** on the layer-1 target (100 seeds,
four single mechanisms, both arms): does MTD deny the target, does *which*
mechanism differ by arm, and does the retention read out on the target the
way the probe's §6 did for the baseline. H2 is re-established on that
objective, never carried. It is a new pre-registration and Marc's call to
run.

Two honest bounds. The result is one profile's: the objective-conditioned
profiles do not clear the Gate anywhere, so a headline denominated on the
located objective is a headline about `aggregate` unless their reach can be
lifted (their bind is verb dispatch, not navigation — B-ii territory). And
the baseline comparison is against Brown's targeted baseline *as built on the
same seam* (priority-then-distance, stop on target); there is no lineage
number for it, because the lineage never ran Scenario 2 in the time domain
(IS-SCN-06).

## 5. Revisit conditions

- Marc rules on the under-MTD matrix; this record's status moves to
  `durable` in that commit.
- Any change to `TargetedSorter`'s key, the geometry, or the fresh-host
  contract re-derives §4.
