---
status: open — results landed 2026-08-25; awaiting Marc's fork ruling (§7.3)
created: 2026-08-25
updated: 2026-08-25
handoff: 2026-08-21_targeted_objective_diagnosis.md
topic: "The targeted-objective (crown-jewel reach) probe — does the movement attacker reach a located deep target better than the inherited baseline, and what does it lack? Records the working operationalisation (the database set, not the broken target_node), the pre-registered reach/efficiency/survivability criteria and the 'better' threshold (committed before any number was seen), the Gate 0 unopposed result, the reach-under-MTD result, the ranked barrier diagnosis, and the fork Marc rules."
---

# The targeted-objective probe — does the movement attacker reach a located target, and what does it lack?

**Status: results landed; the fork is Marc's to rule (§7.3).** This record executes
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

## 5. Gate 0 — unopposed reach (350 seeds/arm, 2 100 runs)

**The Gate precondition fails, decisively and in the predicted direction.** No
movement profile reaches the crown jewels in anything near a healthy fraction of
unopposed runs; the inherited baseline reaches them in three runs of four.

| Arm / profile | reach rate | 95 % CI | runs reached | footprint at reach | median time-to-target | mean hosts total |
|---|--:|--|--:|--:|--:|--:|
| **baseline** | **0.751** | [0.706, 0.797] | 263 / 350 | 29.4 | 9 744 s | 39.7 |
| aggregate | 0.006 | [0.000, 0.014] | 2 / 350 | 7.5 | 13 749 s | 6.3 |
| objective_exfiltration | 0.003 | [0.000, 0.009] | 1 / 350 | 5.0 | 10 413 s | 4.1 |
| objective_impact | 0.003 | [0.000, 0.009] | 1 / 350 | 4.0 | 4 274 s | 3.5 |
| objective_exfiltration_impact | 0.003 | [0.000, 0.009] | 1 / 350 | 8.0 | 9 409 s | 1.9 |
| objective_none_c2 | 0.000 | [0.000, 0.000] | 0 / 350 | — | — | 0.1 |

Five movement runs of 1 750 reached a database host (0.29 % pooled). In **every
one**, the footprint at reach equals the run's total footprint (4–8 hosts) — the
crown jewel was the *last* host owned, reached at the frontier of a small spread,
not pursued. The baseline reaches by flooding: mean footprint at reach 29.4
hosts, total spread 39.7 of 50 (min 7, max 41). The movement profiles cap out at
1.9–6.3 hosts (p95 ≤ 10), and nodes 48–49 at the deepest layer are essentially
never inside that footprint.

### 5.1 The "better" threshold, ruled against the numbers

Marc's claim — the movement attacker reaches a located target *better* than the
baseline — is **falsified on the evidence**, against the criteria committed
before the numbers were seen (§3.2):

- **Better more often? No.** Baseline 0.751 vs movement ≤ 0.006; the CIs do not
  come within 70 percentage points of overlapping. The baseline wins the reach
  race overwhelmingly, exactly as the scrutiny prediction warned — it owns a
  deep host as *collateral* of mass compromise, a route the low-breadth movement
  attacker structurally lacks.
- **Better more efficiently? Unmeasurable, with a hint that does not clear the
  bar.** The five movement reaches carry footprint 4–8 against the baseline's
  29.4 — a directedness-shaped signal in the pre-registered direction. But at
  `n_reached` ≤ 2 per profile it cannot clear the non-overlapping-CI /
  ≥ 3-host requirement, and the reaches are incidental (frontier collisions, not
  navigation), so this is a hint that host-level targeting *could* pay, not
  evidence that the current attacker reaches efficiently.
- **Better more survivably? No** (§6): unopposed movement reach is ~0, so
  reach-under-MTD is ~0 by construction — there is no reach for MTD to preserve.

The Gate precondition (§3.3, ≥ 20 %) is not met by any profile (max 0.6 %). The
located objective is **degenerate on the movement arm** — the ASR-pinned-at-zero
pathology re-instantiated on a new objective. The fork (§3.4) therefore falls to
**Option B/C**: the named gaps are the barrier, and the breadth-based tree
stands.

## 6. Reach under MTD (100 seeds/cell, 4 single mechanisms, 2 400 runs)

**On the movement arm there is nothing for MTD to deny — target reach is 0.000
under every mechanism, because it was already ~0 unopposed.** The material MTD
effect on the movement arm lives on *breadth*, not target reach (§6.2). On the
**baseline** arm, MTD denies the target strongly and mechanism-dependently — and
the dependence is the inversion, visible on the located objective.

### 6.1 Baseline target reach — MTD denies it, and *which* mechanism differs

| Condition | baseline reach | retention (vs 0.751) | baseline mean hosts |
|---|--:|--:|--:|
| unopposed | 0.751 | 1.000 | 39.7 |
| ip_shuffle | 0.510 | 0.679 | 30.8 |
| complete_topology | 0.220 | 0.293 | 31.3 |
| os_diversity | **0.000** | **0.000** | **4.4** |
| service_diversity | **0.000** | **0.000** | **4.4** |

The **diversity family annihilates the baseline** — target reach to zero, total
spread from 39.7 to 4.4 hosts — while the **severance family only dents it**
(reach retained 0.29–0.68, spread ~31). This is the H2 inversion on the located
objective: the flooding baseline leans on the vulnerability re-roll that OS/
Service Diversity destroys, so diversity is *strong* against it, exactly opposite
to the movement arm, where diversity is the weak family and severance the strong
one (§8d of [`hypothesis_tree.md`](hypothesis_tree.md)). The target objective
makes the inversion visible **as objective denial for the baseline**, which the
mass objective could not.

### 6.2 Movement breadth under MTD — where the movement disruption actually is

| Condition | movement `aggregate` mean hosts | vs unopposed 6.3 |
|---|--:|--:|
| ip_shuffle | 0.6 | crushed (severance) |
| complete_topology | 0.9 | crushed (severance) |
| os_diversity | 4.4 | mild (surface re-roll) |
| service_diversity | 4.5 | mild (surface re-roll) |

The movement arm's inversion is on breadth: severance (IP/topology) crushes it,
diversity barely touches it — the mirror image of the baseline's target-reach
pattern. So the H2 inversion is real on *both* arms; it simply reads out on
different quantities because the two attackers have different objectives-in-fact
(the baseline reaches a deep host, the movement attacker does not).

### 6.3 Tuning — no threat-model parameter moves the movement attacker's reach

Marc's question: do threat-model parameters change the result? **No.** A
confirmatory sweep of the most reach-favourable knobs for the best-reaching
profile (`aggregate`, unopposed, 150 seeds each) leaves reach on the floor:

| Config | reach rate | mean hosts |
|---|--:|--:|
| v2_partial (shipped) | 0.007 | 6.3 |
| uniform weights (strip corpus preference) | 0.000 | 6.6 |
| no synthetic overlay | 0.013 | 5.9 |
| retrace sinks on | 0.007 | 6.3 |
| exponential timing regime | 0.007 | 6.3 |
| **horizon doubled to 30 000 s** | **0.040** | **12.4** |
| v1_ckc mapping | 0.000 | 0.3 |

The only knob that moves reach at all is **more time**, and it does so by leaking
more *incidental* breadth (12.4 hosts, 4 % reach at double the horizon), not by
directing the attacker. This confirms the barrier is **structural, not tunable**:
no dwell/timing/weight/overlay parameter adds navigation toward the target or
lifts the breadth cap. It also aligns with the prior finding that every declared
modulator (utility λ, learning, forgetting) *narrows* traversal
([`apt_model_criterion.md`](../../apt_model_criterion.md) axes 3/6/7), so those
knobs make reach the same or worse, never better. The lever that would work is
not a parameter but a **capability** — host-level targeting (§7.1 B-i).

## 7. Diagnosis — the ranked barriers, and the fork

**Headline finding.** Under an APT-authentic *located* objective (reach the
crown jewels), the profiled movement attacker essentially never succeeds even
unopposed (≤ 0.6 %), while the inherited mass-compromise baseline reaches the
target 75 % of the time as a by-product of flooding. **The movement attacker
models APT tactical *behaviour* without APT *target-seeking*** — a named gap, and
the sharp form of the "so what" objection stated as a measured fact rather than a
worry. This confirms the tree §8b prediction verbatim: the target is not
reachable unopposed, so *the six verbs and the traversal, not the objective
definition, are the true bind* — Option A (wire the located objective as-is) buys
nothing, because it would replace one degenerate objective (mass compromise,
0/400) with another (target reach, 5/1750).

### 7.1 The barriers, ranked by evaluation impact

The reach/footprint split adjudicates the candidates directly:

1. **B-i — no host-level targeting (primary).** The attacker's conditioning is
   tactical, never navigational: it cannot prefer a path toward the target. Its
   five reaches are frontier collisions (the database host was the last owned),
   not pursuit. **This is the binding barrier for the located objective.**
   Minimal lift: the `movement_targeted` host-selection variant — re-key the
   distance sort toward the database set via `get_path_from_exposed`
   ([`movement_objectives_design.md`](movement_objectives_design.md) §7.3). It is
   a **movement-layer** change (the objective lives on the host-selection seam,
   §1 of that record), *not* substrate work, so it is honours-feasible — but it
   re-opens scoped work and interacts with the Row-B inversion headline (removing
   churn may shift the ranking; that record §5–§6), so it is **Marc's ruling**,
   not a session action.
2. **B-iii — breadth-capped traversal (compounding cause).** The movement
   attacker spreads to ~2–6 hosts and stops (the structural churn of
   [`movement_objectives_design.md`](movement_objectives_design.md) §2); the
   deepest-layer target is almost never inside that footprint. B-iii is *why* the
   target is out of reach and B-i is *why* the small footprint is never pointed
   at it — they are entangled, and the same `movement_targeted` policy
   (exclude-owned-and-re-select) is the minimal change that addresses both,
   because it converts re-compromise churn into forward progress. Predicted
   effect: reach becomes non-incidental and footprint-to-target stays low (the
   directedness the five lucky reaches hint at) — **the direct test of Marc's
   actual hypothesis**, and the measurement that would flip the fork if it pays.
3. **B-ii — no terminal-objective action (downstream, moot until B-i lifts).**
   The objective tactics dispatch nothing under `v2_partial` (dwell-only); "reach
   the target" is a compromise proxy, not the objective itself. But this cannot
   bind until the attacker can reach the target host at all, so it ranks last.
   Minimal lift: the tactic-level action layer — the successor programme
   ([`../../../notes/ch7_future_work/successor_programme.md`](../../../notes/ch7_future_work/successor_programme.md)),
   heavy, resets the mapping, future work.

### 7.2 Reconciliation with the axis-6 final disposition

The axis-6 final disposition (Marc, 2026-08-02;
[`apt_model_criterion.md`](../../apt_model_criterion.md) axis 6) recorded that a
located objective is *substrate work* outside the honours timeframe. This probe
refines that on evidence: the located objective **as a measurement** needs no
substrate work (it is read-only over the always-present database set — B1–B3
avoided), and now exists. What that disposition correctly identified as heavy is
split by this probe into two pieces of different weight: **host-level
target-seeking** (`movement_targeted`) is *movement-layer* and honours-feasible
(the B-i lift), while the **terminal-objective action** (B-ii) is the substrate/
successor work the disposition named. The disposition's substance — "something to
be rational about but nothing to be rational *toward*" — is exactly what the
probe measures: the attacker has no pull toward the payoff, and its reaches are
accidental.

### 7.3 The fork Marc rules

- **Option A — wire located objective as-is: declined by evidence.** It
  re-denominates on an objective the attacker reaches 0.3 % of the time; it
  strengthens nothing.
- **Option B′ — build host-level targeting (`movement_targeted`):** the honours-
  feasible middle the tree's binary A-vs-B missed. It is the minimal change that
  could make the located objective non-degenerate and directly tests Marc's
  directedness claim. Re-opens scoped work; interacts with the inversion
  headline; **needs Marc's ruling** before any build. Recommended *as the next
  measurement* only if Marc wants to pursue the located-objective spine.
- **Option C — do nothing:** the tree passes on the breadth denominator; the
  headline is the inversion plus tempo-bound containment of host spread; the
  located objective and its target-seeking are future work with a measurement
  behind the call. The record's standing recommendation, and honest as it stands.

**The inversion (H2) is untouched** by all of this — it is measured on host-
compromise breadth on the current mapping, and this probe changes no mapping and
runs no defence against the movement arm's routing.

### 7.4 How it would be implemented — the metric change is empty, the mechanism change is the point

Marc's own framing separates two layers, and the probe shows only the second
matters:

- **Layer 1 — the success metric ("did I reach the target host" vs "did I own
  80 %").** This is the easy change and it is **already done** as a read-only
  measurement (§1); making it the *termination* condition is a few lines. But on
  its own it is **empty**: the attacker reaches the target host 0.3 % of the time,
  so re-denominating success on it just swaps one degenerate objective for
  another. Changing the metric without changing behaviour buys nothing — the
  probe is the proof.
- **Layer 2 — the host-selection mechanism (Marc's "order them by distance
  *toward the objective*").** This is the real lever, and Marc has it exactly
  right. The six phases need no new verbs: the objective lives on
  **host-selection**, not tactic order
  ([`movement_objectives_design.md`](movement_objectives_design.md) §1). Today,
  after a scan the attacker sorts the frontier by
  `sort_by_distance_from_exposed_and_pivot_host` — nearest-from-exposed/pivot,
  plus a random tiebreak (`network.py:873`). The targeted variant re-keys that
  sort by **distance toward the target** (the database set) via
  `get_path_from_exposed` — "this host is in the direction of my objective, go
  there." Brown's own targeted strategy already encodes this
  (`get_host_id_priority` / `tag_priority` toward the target layer,
  `network.py:764`), but it is vestigial — never called from the attack chain
  (feasibility B5). So the change is: **make the frontier sort objective-directed
  instead of exposure-directed**, on the host-selection seam, in the movement
  layer — no substrate repair, no new verb.
- **Layer 3 — the six phases *toward* the objective (Marc's second question).**
  Even with targeting, the six verbs are all host-compromise verbs; none is a
  *terminal objective action* (exfiltrate/impact/collect at the target). So
  "reach the target host" stays a compromise proxy for the objective, not the
  objective itself. Making the phases actually serve the objective is the heavier
  successor work (B-ii), and it is a later question — targeting (Layer 2) is the
  honours-feasible first step and the direct test of the directedness hypothesis.

**Will Layer 2 change anything? — the open empirical question, and why it is not a
session action.** The five lucky reaches at footprint 4–8 (§5) show a deep host
*can* fall inside a small spread when the path happens to run there, so directing
the path is a live hypothesis, not a lost cause. Two risks ride with it, both on
record: the breadth cap (B-iii) means a directed attacker may still churn short
of the target unless the same change carries the exclude-owned-and-re-select half
([`movement_objectives_design.md`](movement_objectives_design.md) §3); and the
**Row-B confound** — removing churn may weaken or shift the inversion headline
(that record §5) — which is why a host-selection change **re-opens scoped work and
is the single open supervisor question** (§6 of that record). It is therefore
Marc's ruling, not a session action. **In one sentence, the bottleneck: the
movement attacker has no navigation toward a host, and adding it (the `movement_targeted`
sort) is the one change that could make the located objective non-degenerate — but
it re-opens the inversion headline, so it needs a ruling before it is built.**

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
