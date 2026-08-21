---
status: open           # retire when Gate 0 is run and Marc rules the fork
created: 2026-08-21
---

# Forward brief — the located-objective probe (Gate 0), and the campaign fork it decides

> **One-line goal.** Decide whether the movement attacker's win condition
> becomes a **located APT target** (reach the crown jewels) or stays
> **mass host compromise** — by measuring, in one cheap run, whether the
> low-and-slow attacker reaches a layer-4 target *unopposed*. Everything in
> the final experimental campaign forks on this one number.

## Why this exists (the finding that produced it)

The hypothesis tree ([`../implementation/pipeline/ogasp/hypothesis_tree.md`](../implementation/pipeline/ogasp/hypothesis_tree.md)
§8b) predicted that the evaluation tree *passes*, but that its objective-half
is under-powered as a story, because the substrate's goal
(`terminate_compromise_ratio = 0.8` — own 40 of 50 hosts) is a **mass-compromise
goal, not an APT goal**. The profiled attacker reaches it 0/400 even with no
MTD, so there is no goal-achievement for MTD to deny; H1 reduces to "MTD
reduces host spread" and the sharp "MTD denies the APT its objective" is
unclaimable. The located-target machinery to fix this **already exists as dead
code** (`is_target_compromised()` over `target_node` at `target_layer = 4`,
`total_database = 5` — the Brown lineage's "targeted" strategy, IS-SCN-03, no
live path). The novel result (H2, the ρ = −0.893 defence-ranking inversion) is
**not** affected by this and stands either way.

## The one unmeasured fact everything hinges on

Reaching a layer-4 target is still done through the six host-compromise verbs;
the attacker paths 0→1→2→3→4 by compromising a host at each hop. The profiled
attacker compromises ≈ 6 hosts unopposed. **Whether 6 hosts is enough to reach
a layer-4 target is unknown** — every prior run measured breadth (host *count*),
none measured depth-to-target. The probe measures exactly this.

## Gate 0 — the probe

1. **Wire `is_target_compromised` as an additive objective option** on the
   movement runner — a per-run toggle (precedent: the timing-regime toggle),
   default off, so no golden and no lineage-comparison run changes. Do **not**
   replace the ratio objective.
2. **Run:** movement attacker, **no MTD**, located-target objective, all five
   profiles, ~350 seeds (predesign §5 budget; minutes on six workers).
3. **Measure:** per profile, the fraction of runs that reach the target, and
   the time-to-reach where they do (censored otherwise).

## The fork the probe decides

- **Reachable unopposed (healthy fraction)** → the located goal is viable.
  - Wire it as the **fresh-evaluation** objective; **keep the ratio objective
    for the prior-model comparison (E5)** — it is the comparability bridge to
    Zhang/Ho/Brown.
  - Re-denominate the tree's H1 leaves on **objective-reach** (deny/delay/
    contain the target) — the stronger headline.
  - **Re-establish the inversion (H2) on the new objective** — it is a new
    measurement, not carried automatically (V-map caution).
  - Proceed to the standing gates + E3.
- **Not reachable even unopposed** → the six verbs are the true bind, proven by
  measurement. The breadth-based tree stands as-is (headline = inversion +
  tempo-bound containment); the tactic-level action layer (Option B) is future
  work ([`../notes/ch7_future_work/successor_programme.md`](../notes/ch7_future_work/successor_programme.md))
  with evidence behind the decision.

## Standing gates (run regardless of the fork; precede E3)

From the pre-design ([`../implementation/pipeline/ogasp/evaluation_predesign.md`](../implementation/pipeline/ogasp/evaluation_predesign.md)
§7): overlay re-key to `v4_failure_only`; D-33 (SCAN_NEIGHBOR from
uncompromised hosts); the retrace re-take; the per-vulnerability event-count
correction (`baseline_action_rows`); per-channel minimum effect sizes;
mapping-study (V-map / E6) scope call; internal-MTTC brief.

## Validation gate (how the next session knows Gate 0 is done)

The probe's per-profile reach fraction and reach-time table exist, committed as
a record under `docs/implementation/pipeline/ogasp/`, and Marc has ruled the
fork. This handoff retires in that commit.

## Hard constraints

- The located objective is **additive** — the ratio objective and every golden
  and lineage-comparison run are untouched (freeze on the lineage side holds).
- Determinism (SIM-05): the toggle is a pure function of (config, seed).
- The inversion (H2) is the anchor result on the current mapping; it is
  preserved and reported whichever way the fork goes — never silently replaced.
- Analysis records are pre-registered where they gate a claim (commit-order
  discipline).

## Reading list (cold-start order)

1. [`../implementation/pipeline/ogasp/hypothesis_tree.md`](../implementation/pipeline/ogasp/hypothesis_tree.md)
   §8b (the prediction and the action-layer decision) and §1–§7 (the tree).
2. [`../implementation/pipeline/ogasp/evaluation_predesign.md`](../implementation/pipeline/ogasp/evaluation_predesign.md)
   §7 (the standing gates), §5 (seed budgets).
3. `mtdnetwork/component/network.py` (`is_target_compromised`, `target_node`)
   and `component/time_network.py` (`terminate_compromise_ratio`); the movement
   objective wiring in `src/mtdsim/l3_simulation/movement/run.py`.
4. [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
   axis 6 final disposition (the located-objective / IS-SCN-03 note).
