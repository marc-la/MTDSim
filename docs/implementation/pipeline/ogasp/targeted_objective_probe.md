---
status: open — pre-registration committed 2026-08-25; results appended after the run
created: 2026-08-25
updated: 2026-08-25
handoff: 2026-08-21_targeted_objective_diagnosis.md
topic: "The targeted-objective (crown-jewel reach) probe — does the movement attacker reach a located deep target better than the inherited baseline, and what does it lack? Records the working operationalisation (the database set, not the broken target_node), the pre-registered reach/efficiency/survivability criteria and the 'better' threshold (committed before any number was seen), the Gate 0 unopposed result, the reach-under-MTD result, the ranked barrier diagnosis, and the fork Marc rules."
---

# The targeted-objective probe — does the movement attacker reach a located target, and what does it lack?

**Status: pre-registration committed, results pending.** This record executes
the [`2026-08-21_targeted_objective_diagnosis.md`](../../../handoffs/2026-08-21_targeted_objective_diagnosis.md)
handoff and the Option-A probe the tree names as the decisive next action
([`hypothesis_tree.md`](hypothesis_tree.md) §8b, §8e). Everything in §§1–4 was
committed **before the probe produced a single reach number**, so "reaches
better" cannot be decided after the fact (handoff hard constraint;
[`../../../workflows/guardrails.md`](../../../workflows/guardrails.md)). §§5–7
are appended after the run.

## 1. The operationalisation — the database set, not the broken `target_node`

The handoff and the tree §8b Option A both name `is_target_compromised()` over
`target_node` at `target_layer = 4` as the machinery to wire. **On the shipped
geometry that machinery cannot be made to fire, and it does not need to be.**
Two facts, both verified in code this session:

- **`target_node` is unconstructable on the phase-0 geometry.** Target
  selection fires only at `i == target_layer and j == 1 and network_type == 0`
  in `Network.gen_graph` (`network.py:215`), but the layer loop reaches only
  `layers - 1 = 3` while `target_layer = 4`, so `i == 4` never occurs; and
  `network_type` is hardcoded to `1` in `Network.__init__` (`network.py:71`).
  Forcing `network_type = 0` then crashes, because `gen_graph` unconditionally
  writes `colour_map[target_node]` with `target_node` still `None`
  (`network.py:277`). This is the five-blocker finding of
  [`targeted_attacker_feasibility.md`](targeted_attacker_feasibility.md) §4
  (B1–B3), re-verified.
- **The database set is defined in every run, regardless of `network_type`.**
  `Network.__init__` sets `_database = range(total_nodes - total_database,
  total_nodes)` (`network.py:55`); for the movement geometry (`total_nodes =
  50`, `total_database = 2`) that is **nodes 48 and 49, both at the deepest
  layer (layer 3)** — the crown jewels. `get_database()` exposes them and no
  construction blocker touches them.

**Decision: the located objective is operationalised as reaching a database
(crown-jewel) host** — `set(compromised) & set(get_database())` non-empty. This
is chosen over the `target_node` machinery for four reasons, each of which the
guardrails' evidence standard requires be stated:

1. **No substrate repair.** It requires no change to `mtdnetwork/`, so the S2
   freeze, every golden and every lineage-comparison run are untouched — the
   handoff's "additive only" hard constraint is met by construction.
2. **Measurement precedent.** [`targeted_attacker_feasibility.md`](targeted_attacker_feasibility.md)
   §5 already measured "database hosts reached (of 2)" — the one measured result
   that justified this whole direction used the database set, not `target_node`.
3. **It is the same target for both arms.** The baseline and the movement
   attacker are scored against an identical, geometry-fixed deep-host set, so
   the cross-arm contrast is well-defined.
4. **It is faithful to Brown's design.** Brown's targeted attacker pursues a
   deep target and sweeps target depth as an experimental variable
   ([`targeted_attacker_feasibility.md`](targeted_attacker_feasibility.md) §5,
   IS-SCN-03); a deepest-layer host is that concept realised on the working
   geometry.

**Realised as a read-only measurement, not a termination toggle.** The handoff
proposed wiring the objective as a default-off termination toggle. The probe
instead measures reach **without changing termination**: a new read-only field
`MovementRecord.database_held` (substrate ground truth, one set-intersection per
record, exactly the `n_compromised` precedent) records whether a crown-jewel
host was held at each event, and `MovementRunResult.database_hosts_reached` /
`first_database_reach_time` derive reach and time-to-target after the run. This
is **strictly safer than a toggle** — it changes no control flow, so every run
is byte-identical to before and SIM-05 determinism is preserved by construction
(verified: seed-matched records identical, full L3 suite 769 passed / 248
skipped). A real termination toggle is only needed if target-reach later becomes
the *win condition* of the fresh evaluation (the post-fork Option-A build), not
for this diagnostic. The baseline arm reads the same reach off its own
attack-statistics dataframe (host id + `finish_time`), so no substrate change
touches it either.

## 2. The hypothesis under test — and it is allowed to fail

**Marc's claim:** the movement attacker should reach a located target *better*
than the baseline — "antithetical if not the case, but most likely the case."
This is the thing to test, not to assume (guardrails: a verdict, not a first
impression). The scrutiny prediction pulls the other way: the baseline floods
the network (~38/50 hosts) and so may own a deep host as *collateral*, while the
movement attacker owns ~6 and has **no host-level targeting** — its objective
conditioning is over *tactics*, not *navigation toward a host*.

## 3. Pre-registered criteria — reach, efficiency, survivability

All arms: the inherited **baseline** plus the five movement profiles
(`aggregate`, `objective_exfiltration`, `objective_impact`,
`objective_exfiltration_impact`, `objective_none_c2`). Determinism: SIM-05; per
D-29 seed-matched arms are **independent, not paired**, so all cross-arm
comparisons are **unpaired**. Horizon 15 000 s, mapping `v2_partial`, overlay
`v3_persistent_backward` (experiment-2 configuration, modulators null per the
axis-3 §4 pin). Seed budget **350 seeds** per cell unopposed (≈ 2 100 runs
unopposed ≈ 7 min at ~0.2 s/run), matching the C6 power budget
([`evaluation_predesign.md`](evaluation_predesign.md) §5).

### 3.1 The three operationalisations of "reaches the target"

- **Reach rate** — fraction of runs (per arm) in which ≥ 1 database host is
  compromised. Reported per arm with a seed-level bootstrap 95 % CI
  (BCa, 2 000 resamples). Cross-arm: two-proportion comparison, unpaired.
- **Reach efficiency** — among *reached* runs only: **hosts-compromised-en-route
  to the target** (footprint at `first_database_reach_time`, from the
  `n_compromised` trajectory) and **time-to-target** (`first_database_reach_time`,
  right-censored at the horizon for non-reaching runs; Kaplan–Meier).
- **Reach survivability** — reach rate *under MTD pressure*, per defence
  mechanism, and the **reach-rate retention** = reach-rate(MTD) /
  reach-rate(no-MTD) per arm.

### 3.2 The "better" threshold — committed before the numbers

Marc's claim is decided against three pre-registered disjuncts; the movement
attacker "reaches better" if it wins **any** of them (an APT's directedness can
show as any one):

- **Better more often:** movement reach rate > baseline reach rate, for ≥ 1
  profile, with non-overlapping 95 % CIs (minimum effect of interest: **10
  percentage points** — a smaller gap is a tie).
- **Better more efficiently:** among reached runs, movement
  hosts-en-route < baseline hosts-en-route, for ≥ 1 profile, non-overlapping
  CIs (minimum effect: **3 hosts** — fewer hosts owned to reach the same target
  is the directedness signal).
- **Better more survivably:** movement reach-rate retention under any single
  defence > baseline retention, for ≥ 1 profile, non-overlapping CIs.

### 3.3 The Gate precondition (tree §8e) — committed before the numbers

The located objective is **non-degenerate** — worth denominating an evaluation
on — only if some movement profile reaches the database in a **healthy fraction
of unopposed runs**, pre-registered as **≥ 20 %**. Below that, target-reach is a
degenerate-region statistic on the movement arm (the ASR-pinned-at-zero
pathology, re-instantiated on a new objective) and cannot discriminate MTD.

### 3.4 The fork this decides (stated, not pre-judged)

- **Movement reaches usefully** (wins any 3.2 disjunct, and the 3.3 Gate holds)
  → the located objective becomes the spine of the fresh evaluation; H1
  re-denominates on target-reach; the inversion (H2) is **re-established on the
  new objective, not carried** (V-map caution). Option A.
- **It does not** → the named gaps (§4) are the barrier, documented with
  evidence; the breadth-based tree stands (headline = inversion +
  tempo-bound containment of host spread), and the missing capability is future
  work ([`../../../notes/ch7_future_work/successor_programme.md`](../../../notes/ch7_future_work/successor_programme.md)).
  Option B/C.

## 4. The candidate barriers, to rank by evaluation impact (pre-registered list)

The handoff names three; the run ranks them by how much each blocks a meaningful
MTD evaluation, and names the minimal change that would lift each:

- **B-i — No host-level targeting.** Conditioning is tactical (which tactic),
  not navigational (which host); the attacker cannot prefer a path toward the
  target. Minimal lift: the `movement_targeted` host-selection variant that
  re-keys the distance sort toward the database set
  ([`movement_objectives_design.md`](movement_objectives_design.md) §7.3).
- **B-ii — No terminal-objective action.** The objective tactics (exfiltration,
  impact, collection) dispatch nothing under `v2_partial` (dwell-only); "reach
  the target" is a *compromise proxy* for the objective, not the objective
  itself. Minimal lift: the tactic-level action layer (successor programme —
  heavy, resets the mapping).
- **B-iii — Breadth-capped traversal.** ~6 hosts unopposed; is the target out
  of reach at that footprint, or reachable and just not sought? The reach/
  footprint split (§3.1) adjudicates B-i vs B-iii directly.

## 5. Gate 0 — unopposed reach

*(appended after the run)*

## 6. Reach under MTD

*(appended after the run)*

## 7. Diagnosis and the fork

*(appended after the run)*

## 8. Evidence and anchors

- The wiring: `MovementRecord.database_held` and `MovementRunResult.database_hosts_reached`
  / `first_database_reach_time` (read-only ground truth); `MovementAttacker._database_held`;
  `run_movement` post-run derivation. Baseline reach off the attack-statistics
  dataframe.
- The probe harness: `data/results/targeted_objective_probe/run_probe.py`.
- The construction blockers re-verified: `mtdnetwork/component/network.py`
  (`network_type`, `gen_graph` target selection, `_database`),
  [`targeted_attacker_feasibility.md`](targeted_attacker_feasibility.md) §4–§5.
- The design groundwork: [`movement_objectives_design.md`](movement_objectives_design.md);
  the cascade this feeds: [`hypothesis_tree.md`](hypothesis_tree.md) §8b, §8e.
- Statistical instrument and seed budget: [`evaluation_predesign.md`](evaluation_predesign.md)
  §4, §5.

## 9. Revisit conditions

- Marc rules the fork (§7); this record's status moves to `durable` and the
  handoff retires in that commit.
- If the geometry's `total_database` or `target_layer` changes, the located
  target set changes and the reach numbers re-derive.
