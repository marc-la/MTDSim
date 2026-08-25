---
status: open           # retire when the diagnostic record lands and Marc rules the fork
created: 2026-08-21
---

# The targeted-objective line — does the movement attacker reach a located APT target, and what does it lack?

> **One-line goal.** Give the threat model an APT-aligned win condition — reach
> a located high-value target — and use it to diagnose, on evidence, **what the
> movement attacker is missing as an instrument for meaningful MTD evaluation**.
> The output is a recommendations record, not just a number.
>
> **Run this in a fresh session, cold from this brief.**

## Why this exists

The RQ's evaluation sub-question (SQ3) is answerable today, but on a **non-APT
objective**: the substrate's goal is `terminate_compromise_ratio = 0.8` — own
40 of 50 hosts, a mass-compromise goal no APT pursues. The profiled attacker
reaches it 0/400 even unopposed, so *MTD denies the APT its objective* — the
strongest, most authentic form of the thesis headline — is unclaimable. The
novel result (the ρ = −0.893 defence-ranking inversion, H2 of the hypothesis
tree) is unaffected and stands regardless. The located-target machinery to fix
the objective mismatch **already exists as dead code**: `is_target_compromised()`
over `target_node` at `target_layer = 4` (the Brown lineage's "targeted"
strategy, IS-SCN-03, no live path). Full context:
[`../implementation/pipeline/ogasp/hypothesis_tree.md`](../implementation/pipeline/ogasp/hypothesis_tree.md)
§8b.

## The hypothesis under test — and it must be allowed to fail

**Marc's claim:** the movement attacker should reach a located target *better*
than the baseline — "antithetical if not the case, but most likely the case."

**This is the thing to test, not to assume** (guardrails: a verdict, not a
first impression; zero-trust). Two operationalisations pull in opposite
directions, and separating them is the point:

- **Reach rate** (fraction of runs reaching the target). The scrutiny
  prediction is that the **baseline may win this**, not lose it: it floods the
  network (~38/50 hosts) and so owns a single target host as *collateral*,
  while the movement attacker owns ~6 and has **no host-level targeting** — its
  objective-conditioning is over *tactics*, not *navigation toward a host*. If
  the baseline reaches the target more often, that is not a failure of the
  thesis; it is the diagnosis.
- **Reach efficiency and survivability** — hosts compromised en route (footprint),
  time-to-target, and reach rate *under MTD pressure*. This is where an APT's
  directedness should show, if the model captures it. The honest question is
  whether the movement attacker reaches the target *deliberately* or not at all.

If the movement attacker reaches the target neither more often *nor* more
efficiently *nor* more survivably, the finding is that it models APT tactical
*behaviour* without APT *target-seeking* — a named gap, not a null result.

## The experiment (both arms — the comparison is the point)

1. **Wire `is_target_compromised` as an additive objective toggle** on the
   movement runner (default off; precedent = the timing-regime toggle), so no
   golden and no lineage-comparison run changes. Do **not** replace the ratio
   objective — it is the comparability bridge to Zhang/Ho/Brown.
2. **Unopposed reach (the Gate 0 fork):** both arms, no MTD, located-target
   objective, five profiles + baseline, ~350 seeds. Report per arm/profile:
   reach fraction, time-to-target (censored), and **hosts-compromised-en-route**.
3. **Reach under MTD:** the same, across the defence family at the operating
   interval and one relaxed interval — does MTD deny/delay the target, and does
   *which* mechanism differ by arm (the inversion, re-denominated on the
   target)?

## The deliverable Marc asked for — a diagnosis, ranked

A tracked record under `docs/implementation/pipeline/ogasp/` that answers, on
evidence: **what does the movement attacker lack as a barrier to meaningful MTD
evaluation, and what is the minimal change to remove each barrier?** Candidate
barriers to test and rank by evaluation impact (add any the data surfaces):

- **No host-level targeting** — conditioning is tactical, not navigational; the
  attacker cannot prefer a path toward the target. Likely the primary gap.
- **No terminal-objective action** — the objective tactics (exfiltration,
  impact, collection) dispatch nothing; "reach the target" is a compromise
  proxy for the objective, not the objective itself (the six-verb ceiling).
- **Breadth-capped traversal** — ~6 hosts unopposed; is the target simply out
  of reach at that footprint, or reachable and just not sought?
- Whichever of these the reach/efficiency split implicates, with the minimal
  change that would lift it (config-scale target wiring vs a targeting
  behaviour vs the tactic-level action layer) and the predicted effect on the
  evaluation's meaningfulness.

## The fork this decides (state it, do not pre-judge it)

- **Movement attacker reaches the target usefully** (more efficiently /
  survivably, even if not more often) → the located objective becomes the spine
  of the fresh evaluation; H1 re-denominates on objective-reach; **re-establish
  the inversion on the new objective** (a new measurement, not carried — the
  V-map caution). Keep the ratio objective for E5.
- **It does not** → the named gaps are the barrier, documented with evidence;
  the breadth-based tree stands (headline = inversion + tempo-bound
  containment), and the missing capability is future work
  ([`../notes/ch7_future_work/successor_programme.md`](../notes/ch7_future_work/successor_programme.md))
  with a measurement behind the call.

## Second diagnostic — where the disruption actually comes from (explicit vs implicit)

Marc's hunch: disruption should come mostly from the **implicit** channel (the
mutation changes the attack surface, so the attacker's actions fail) rather than
the **explicit** channel (the hard-coded 20 s confusion penalty charged on every
interrupt, an invariant since the lineage began). He expected ~80 % implicit /
20 % explicit and suspected it was the other way round. A teaser measurement over
experiment 2's recorded runs (movement arm, 200 s) says it is **mechanism-
dependent, and the split *is* the inversion**:

- **Position-destroying (topology / IP):** blocked fraction rockets from 0.15
  (no MTD) to **0.72** — the surface change is doing the work; plus a 10.3 %
  time penalty. **Implicit-dominant.** Strip the penalty and these still crush
  breadth, because 72 % of actions already fail.
- **Diversity (OS / service):** blocked fraction stays at **0.16 ≈ the no-MTD
  level** — the surface change does almost nothing to the movement attacker
  (it does not depend on those preconditions); the only disruption is the 7.2 %
  penalty plus the token throw-back. **Explicit-dominant.** Strip the penalty
  and these suppress almost nothing — which is why they barely touch the
  movement attacker (the inversion's losing arm).

**The reassuring headline this gives Marc:** the ~88 % suppression that carries
the thesis (position-destroying family) is **real attack-surface disruption, not
the hard-coded penalty**. The penalty only dominates for the mechanisms that
barely work anyway. This defuses the "it's all just a 20 s hack" worry for the
result that matters.

**The clean experiment to nail it (recommended):** ablate the penalty — run the
matrix with the confusion penalty set to 0 vs its inherited 20 s, and report
which mechanisms' suppression survives. That isolates explicit from implicit per
mechanism with a bit-identical control (the penalty is a run input on the
substrate side). Pre-register that penalty-0 leaves position-destroying
suppression roughly intact and collapses diversity suppression toward zero.
Feeds the tree's D-tax vs D-contain channels directly and answers whether the
disruption "makes sense" as more than a hard-coded assumption.

## Visualisation deliverable (Marc's ask — "how do we visualise this")

The diagnostic record carries figures, not just tables:

- **Target-reach:** per-arm survival curves to target (Kaplan–Meier, reach
  probability over time), and a footprint scatter (hosts-en-route vs reached?).
- **Explicit/implicit split:** a stacked or grouped bar per mechanism — blocked-
  fraction rise (implicit) beside penalty-time share (explicit) — so the two
  sources are read at a glance, with the penalty-ablation overlay.
- Conventions: [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md);
  no accentuation on diagnostic viz (let the bars/curves speak); generated by a
  tracked `tools/` script, never hand-drawn.

## Hard constraints

- **Additive only** — the ratio objective, every golden, and every
  lineage-comparison run are untouched; the freeze on the inherited side holds.
- **Determinism (SIM-05)** — the toggle is a pure function of (config, seed);
  the two arms share RNG streams, so seed-matched arms are **independent, not
  paired** (D-29) — cross-arm tests are unpaired.
- **The inversion (H2) is the anchor** on the current mapping — preserved and
  reported whichever way the fork falls, never silently replaced.
- **Pre-register** the reach/efficiency criteria and the "better" threshold
  before running (commit-order discipline), so "reaches better" cannot be
  decided after the numbers are seen.
- Test the hypothesis; do not confirm it. A baseline that reaches the target
  more often is data, not an embarrassment.

## Validation gate (how the fresh session knows it is done)

The diagnostic record exists: per-arm/profile reach rate, efficiency and
under-MTD tables; the ranked barrier list with minimal-change recommendations
and their predicted evaluation impact; and the fork stated with its evidence.
Marc then rules the fork. This handoff retires in that commit.

## Reading list (cold-start order)

1. This brief, then
   [`../implementation/pipeline/ogasp/hypothesis_tree.md`](../implementation/pipeline/ogasp/hypothesis_tree.md)
   §8b (the prediction, the action-layer bind) and §1–§7 (the tree).
2. [`../implementation/pipeline/ogasp/evaluation_predesign.md`](../implementation/pipeline/ogasp/evaluation_predesign.md)
   §5 (seed budgets), §7 (standing gates), §4 (the statistical instrument —
   unpaired tests, effect floors).
3. `mtdnetwork/component/network.py` (`is_target_compromised`, `target_node`),
   `component/time_network.py` (`terminate_compromise_ratio`), and the movement
   objective wiring + arm construction in
   `src/mtdsim/l3_simulation/movement/run.py`.
4. [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
   axis 6 final disposition (located objective / IS-SCN-03) and axis 1
   (persistence — the target-reach measure bears on it).
5. [`../notes/ch7_future_work/successor_programme.md`](../notes/ch7_future_work/successor_programme.md)
   (the action-layer programme the "not reachable" fork feeds).
