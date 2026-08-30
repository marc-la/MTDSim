---
status: open — results landed 2026-08-25; awaiting Marc's fork ruling (§7.3)
created: 2026-08-25
updated: 2026-08-30
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

> **Annotation, 2026-08-30 — the sentence is confirmed on the fixed attacker,
> with a rider.** The fresh-host contract (Marc's loop-fix ruling; the
> re-compromise churn was 45 % of the movement attacker's compromise verbs,
> measured at 5 × 350 seeds) is now the reported configuration, and
> [`fsm_token_hold_findings.md`](fsm_token_hold_findings.md) H5 re-measures
> reach on it: **1.4 %** on `aggregate` at 15 000 s against this record's 20 %
> Gate 0 bar — still degenerate, so *structural, not tunable* stands, and B-i
> is still the binding barrier (footprint at reach 17.9 hosts: frontier
> collisions, not pursuit). The rider is the 30 000 s point: the fixed attacker
> reaches **14.6 %** (this table's 4.0 % on the churning one), because the fix
> removed enough of B-iii's breadth cap (10.6 → 18.5 hosts) that horizon alone
> now moves reach materially. Jin's token-hold rule, the other candidate, does
> not: 0.3 % at either horizon, degenerate (H3 there).

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

## 10. Re-verification on the current code, and Marc's host-priority question (2026-08-30)

Marc asked, cold, whether the targeted objective (dissertation §2.2.3,
Table 2.3 "Targeted") is *properly implemented and geared toward the target* —
recalling that Brown codes the targeted attacker's **host priority differently**
from the general attacker's. Everything below was re-run or re-read against the
tree at `042afc5f` (after the MTD-pool restore `d127f443` and the fresh-host
contract `ce8739ad`, both of which touched the substrate since §1 was written).

**Verdict: the targeted objective is not implemented as a live attacker in this
repository, in either arm.** What exists is (a) a correct **read-only reach
measurement** over the database set (§1), and (b) Brown's targeted machinery,
**present but vestigial and unconstructable** on the shipped geometry. Marc's
recollection is right, and it is the sharpest form of the finding: Brown *does*
specify a distinct host-priority rule for the targeted attacker (IS-SCN-03 /
B-ATK-02: the target itself if found → hosts on the target's layer → hosts on
other layers, moving toward the target's layer), and the code **carries that
rule verbatim** as `assign_tag_priority` / `get_host_id_priority`
(`network.py:764–816`) — but **no line of the attack chain ever calls it**. Host
selection in both scenarios, and on both arms, is
`sort_by_distance_from_exposed_and_pivot_host` (`attack_operation.py:397`):
nearest-from-foothold, the *general* attacker's rule (IS-SCN-02, Brown Fig 3
box 2). So the two objectives in Table 2.3 share one host-selection policy in
the code; only the objective *label* differs, and even that label is dead
(`network_type = 1` hardcoded, `network.py:71`).

### 10.1 What was re-verified, item by item

| Claim | Status at `042afc5f` | Evidence |
|---|---|---|
| `network_type` hardcoded to 1 (general) in every constructible network | **holds** | `network.py:71`; `TimeNetwork` never overrides; `tests/test_action_layer_dispositions.py:95` pins it |
| `target_node` is `None` in every run to date | **holds** | spike: `target_node None` on the phase-0 geometry, seed 0 |
| B1/B2 — `network_type = 0` + `target_layer = 4` crashes (`colour_map[None]`) | **holds, all seeds tried** | spike: `TypeError` at seeds 0, 1, 2 |
| B3 — construction is seed-dependent at other target layers | **holds, bit-identical to the feasibility table** | `target_layer = 3`: 1/3 (node 40); `target_layer = 2`: 3/3 (nodes 37, 26, 33) |
| B4 — targeted termination commented out; `is_target_compromised` uncalled | **holds** | `attack_operation.py:732–737` still commented; `is_target_compromised` has no caller in `mtdnetwork/`, `src/`, `tools/`, `tests/`; on the shipped network it *raises* (`AttributeError` on `get_host(None)`) |
| B5 — Brown's priority rule never reaches host selection | **holds** | `get_host_id_priority` / `tag_priority` have no caller outside `network.py`; `_do_enum_host` sorts by distance only |
| **B6 (new)** — `TargetNetwork.copy_network`, Brown's original targeted entry point, cannot run against `TimeNetwork` | **fails** | reads `network.total_layers`, which `Network` never sets (it stores `self.layers`, `network.py:51`): `AttributeError` on call; nothing in the tree constructs `TargetNetwork` |
| The priority rule itself is Brown-correct when it *is* evaluated | **holds** | spike at `target_layer = 2`: `tag_priority = [application, db, file, web]` → same layer first, then adjacent layers, then the far layer; target scores 0, same-layer 1 — exactly B-ATK-02 |
| The read-only reach measurement is correct | **holds** | `run.py:489–493` and `attacker.py:677–688` intersect `get_compromised_hosts()` with `get_database()` ({48, 49}, both at layer 3 = deepest); the baseline arm reads `compromise_host` / `finish_time` off the attack-statistics dataframe (`run_probe.py:172–182`) — same target set, both arms |
| Give-up protection for the target (IS-SCN-04) | live code, dead branch | `attack_operation.py:421` gates on `network_type == 0`, so it never fires |

One labelling quirk worth carrying, *to verify against Brown, not a bug claim*:
`HOST_TAGS` assigns the tag `db` to **layer 1** and `file` to layer 3, while the
`_database` (crown-jewel) set sits at **layer 3**. Brown's default geometry is
five layers with `target_layer = 2` (`target_network.py:6`); the tag order was
presumably written for that geometry and never re-keyed for the four-layer
time-domain network. It has no effect today (nothing reads the tags), but a
targeted build that priorities "the same layer as the database" would need to
key on `get_layers()` and `get_database()`, not on the `db` tag.

### 10.2 What this means for §2.2.3 of the dissertation

Table 2.3 describes **Brown's design** — two objectives on identical
capabilities — and as background on Brown's MTDSim that is accurate. It is
*not* true of the simulator this dissertation runs: Zhang refactored only
Scenario 1 into the time domain (IS-SCN-06, IS-CFL-04), and the repository
inherits that narrowing with the targeted remnants unreachable. The prose
"the attacker holds an objective, of which two exist" therefore reads as a
claim about the live simulator that the code does not support. This is the M2
item already flagged in the tex comment (ruled 2026-08-27: Marc's to fix, not a
session's); the evidence above is what that fix has to reconcile with. The
honest framing is Brown's two objectives as *design*, and the general objective
as the one the time-domain lineage — and every experiment in this dissertation
— actually runs, with the located objective reached in this project only as the
§1 measurement.

### 10.3 What "properly implemented and geared toward the target" would take

Unchanged from §7.4, now with the seam pinned: not a substrate repair of
B1–B6 (which would restore Brown's *targeted network*, not a targeted
*attacker*), but the `movement_targeted` host-selection variant on the movement
seam — re-key the frontier sort toward `get_database()` (or call Brown's own
`get_host_id_priority` keyed to the database layer), plus the exclude-owned
half of [`movement_objectives_design.md`](movement_objectives_design.md) §3 —
and, only if target-reach becomes the win condition, a termination on
`database_held` in place of the ratio. All of it re-opens the inversion
headline (§7.4), so it stays Marc's ruling.

## 11. Proposal — what it takes to run Brown's targeted attacker (2026-08-30)

Marc's ask: wire `attack_objective ∈ {general, targeted}` as a top-level input
on the attack model **vacuously** now (done — see §11.1), and propose the changes
that would make the targeted value do Brown's work. The proposal is ranked as a
build order; every step is default-preserving (the `general` arm and every
golden stay byte-identical), and the steps that cross a governance line say so.
Nothing below is built except §11.1.

### 11.1 Done — the vacuous input

`run_movement(attack_objective="general")` → `MovementAttacker.attack_objective`
→ `MovementRunResult.attack_objective`; validated against
`movement/attacker.py::ATTACK_OBJECTIVES = ("general", "targeted")`; read by no
control flow. `tests/l3_simulation/test_movement_attack_objective.py` pins the
default, the echo, the refusal of any third value, and — deliberately, to be
retired the day the policy lands — that `"targeted"` is bit-identical to
`"general"`. The input sits on the movement seam because that is where Marc's
integration lands; §11.3 argues the *behaviour* belongs one layer down.

### 11.2 What Brown's targeted attacker is (the spec to build against)

Four rules, all `[behav]`, none with a time-domain spec (IS-SCN-06 — so this is
recorded as an **extension**, not a restoration):

| # | Rule | Source | Status in code |
|---|---|---|---|
| T-a | The target is a **single host at a chosen depth** `TX` (target in the X-th layer), swept as an experimental variable | Brown §III-C(1), §V; B-ATK-02 | `target_node` / `target_layer`, unconstructable (B1–B3, B6) |
| T-b | **Host priority**: the target itself if it is visible → hosts on the target's layer → hosts on other layers, nearer the target's layer first | IS-SCN-03 / B-ATK-02 | `get_host_id_priority` — correct, never called (B5) |
| T-c | **Never give up on the target**; give up on any other host after 10 failed attempts | IS-SCN-04 / B-ATK-06 | `attack_operation.py:421`, gated on `network_type == 0`, never fires |
| T-d | **Terminate on target compromise**, not on the 80 % ratio | Brown §III-C(1) | commented out, `attack_operation.py:732–737` (B4) |

Everything else (the six verbs, RoA exploit ordering, credential stuffing, C2
pivoting) is identical across the two scenarios by design (IS-SCN-01) and needs
no change.

### 11.3 The changes, in build order

**Step 1 — the target, chosen without repairing `gen_graph`.** Do not resurrect
`target_node` (B1–B3, B6 are four separate construction defects, and fixing
them changes the generation RNG sequence for every seed, which re-baselines
every golden on both arms). Instead choose the target **after** the network is
built, on the seam, from the seeded RNG: `target_hosts = {one host drawn from
[h for h, layer in network.get_layers().items() if layer == target_layer]}`,
or, for the geometry-fixed crown-jewel reading used by this probe,
`set(network.get_database())`. Both realise Brown's `TX` sweep
(`target_layer ∈ {1, 2, 3}` on the four-layer geometry), both are identical for
the two arms, and neither touches a substrate line. Carry the choice as
`target_hosts: frozenset[int]` beside `attack_objective`; `general` runs carry
the empty set. Re-key on `get_layers()`, never on the `db` tag (§10.1 quirk).

**Step 2 — host priority (T-b), the one change that makes the attacker
targeted.** The pop happens in the shared core `_do_enum_host`
(`attack_operation.py:396–402`): D-28 filter → `sort_by_distance_from_exposed_and_pivot_host`
→ `pop(0)`. The movement arm reaches the same lines through
`_reselect_fresh_host` (`attacker.py`), so **one hook serves both arms**. Give
`AttackOperation` the objective and the target set at construction
(`AttackOperation(..., attack_objective="general", target_hosts=frozenset())`),
and in `_do_enum_host` branch once:

- `general` → today's sort, untouched (byte-identical; the branch is the whole
  default-preservation argument).
- `targeted` → sort the visible stack by
  `(priority(host), distance_from_exposed_or_pivot(host), tiebreak)` where
  `priority` is Brown's own `get_host_id_priority` re-keyed to the target set
  (0 if `host in target_hosts`; else `|layer(host) − target_layer| + 1`), and the
  distance sort is kept as the **within-class** order so the attacker still moves
  toward the nearest host of the preferred class. Rule T-b's first clause
  ("attack only the target if found") falls out of priority 0 sorting first.

The tiebreak draws `random.random()` per queued host from the global stream
today; keep exactly that draw count in the targeted branch so the two arms'
stream discipline (D-29) is unchanged. Fresh-host contract composes unchanged —
the loop still pops through the same core; it just pops in a different order.

**Step 3 — never give up on the target (T-c).** Replace the dead guard
`network.network_type == 0 and curr_host_id == network.get_target_node()` at
`attack_operation.py:421` with `curr_host_id in self.target_hosts`. Empty set
under `general` → identical behaviour.

**Step 4 — termination (T-d).** Two arms, two lines. Movement: in
`run_movement`, after `attacker.start()`, a watcher (or a check in the record
writer where `_database_held` is already computed) fires `end_event.succeed()`
when `held & target_hosts` is non-empty **and** `attack_objective == "targeted"`;
`reached_objective` then means target reached. Baseline: re-enable the commented
block at `attack_operation.py:732` keyed to `target_hosts`, not `network_type`.
Keep `TimeNetwork.is_compromised` (the ratio) as the `general` criterion — it is
the comparability bridge to Zhang/Ho/Brown and must not be replaced.

**Step 5 — tests and goldens.** (i) The §11.1 bit-identity test is retired and
replaced by a **general-arm** bit-identity test (targeted machinery present, the
general run unchanged — the gate that avoids a re-baseline). (ii) Unit tests
on the sort: target visible → popped first; target not visible → same-layer
hosts before adjacent layers before far layers; within a class, nearest first.
(iii) T-c: attempt counter on the target passes 10 and the target is never
appended to `stop_attack`. (iv) T-d: `end_event` fires on target compromise
with fewer than 40 hosts held. (v) A trace-tool row for the objective and the
target set (`mtdsim.l3_simulation.trace`), so a run can be shown to be targeted.

**Step 6 — the experiment (pre-registered, per §3).** Brown's design: sweep
`target_layer ∈ {1, 2, 3}` (his `TX`), both arms, five profiles + baseline,
unopposed then the four-mechanism family, 350 / 100 seeds; report reach rate,
time-to-target (censored, Kaplan–Meier) and footprint-at-reach. The Gate 0
question re-asked with navigation present: does the movement attacker now
reach a **shallow** target in ≥ 20 % of unopposed runs (§3.3)? This is the
direct test of Marc's directedness hypothesis the probe could not run.

### 11.4 What each step costs, and who rules it

| Step | Layer | Governance | Cost |
|---|---|---|---|
| 1 target choice | seam (`run.py`) + `AttackOperation` ctor | none — additive, default empty | small |
| 2 host priority | **substrate core** `_do_enum_host`, branched, default untouched | crosses the S2 freeze and the host-selection gate of [`movement_objectives_design.md`](movement_objectives_design.md) §6; **Marc's ruling** — it is the same seam the fresh-host contract just opened, so the precedent exists | medium; the one real design |
| 3 give-up | substrate, one guard | same ruling as 2 | trivial |
| 4 termination | seam + one substrate block | same ruling | small |
| 5 tests | tests | none | small |
| 6 experiment | `data/results/` harness | pre-register first | ~15 min compute |

Two risks ride with step 2, both already on record: the **breadth cap** (B-iii) —
a directed attacker that still churns on owned hosts may stop short of a deep
target, which is why the fresh-host contract (now on by default) is its
prerequisite; and the **Row-B confound** — re-ordering host selection can shift
the inversion headline, so H2 is re-established on the targeted objective, never
carried (§3.4). And one modelling caveat for the write-up: Brown's T-b assumes
the attacker "can identify target characteristics" — that it knows the target's
*layer* before it can see the target. That is a knowledge assumption the
general attacker does not make; the dissertation states it as Brown's, not
argued fresh.

**In one sentence:** the targeted attacker is one branch in `_do_enum_host`
(priority-then-distance instead of distance), a one-line give-up guard and a
termination on the target set — with the target drawn on the seam rather than
in `gen_graph`, so no golden moves — and the only thing standing between the
vacuous flag and Brown's work is the host-selection ruling.
