---
status: durable
created: 2026-07-23
updated: 2026-07-27
topic: "OGASP runtime verification — cross-examination of the layer model (structure / policy / execution) against the landed loop (commit 48471b8) before the first-numbers run; per-proposition verdicts, the P4 H-coupling quantification, the P7 sink enumeration + termination disposition, and the four seam invariants"
lineage: closes docs/handoffs/2026-07-23_l3_ogasp_runtime_verification.md; preceded the first-numbers run, recorded at experiment_01_findings.md (both handoffs shipped and deleted)
---

# OGASP runtime verification — the model reconciled against the code

**Status:** durable. This is the verification gate the first-numbers run
([`experiment_01_findings.md`](experiment_01_findings.md))
depends on. The attacker Petri → MTDSim loop is built and green (commit `48471b8`;
full suite **242 passed**). Before pulling numbers, the runtime model — three
sublayers plus a driver — was cross-examined against the landed code: each claim in
Marc's 2026-07-23 runtime description became a proposition with a locus, a method,
and a recorded verdict. Nothing here changed behaviour; it audits, quantifies the
one open finding (P4), enumerates the one open decision (P7), and states the four
seams as first-class invariants. The overlay *values* stay provisional (Marc's
separate greenlight); this pass certifies the *mechanism*, independent of blessing
the numbers.

## The layer model (what was verified)

OGASP at runtime is three sublayers plus a driver that threads them. The telling
merges a couple of seams the code deliberately keeps apart; the code keeps them
apart, and the merge is only in the telling.

| Sublayer | What it owns | Where it lives |
|---|---|---|
| **Movement / structure** (GASP) | which moves are legal, and their base proportions — the net's legal-move grammar, with the pre-attack synthetic overlay already composed in at net-build | [`net.py`](../../../../src/mtdsim/l3_simulation/movement/net.py) (`RoutingNet`, `load_routing_net`, `_compose_out`) |
| **Controller / policy** | which verb a tactic fires, and how a verdict re-weights the next move | [`controller/`](../../../../src/mtdsim/l3_simulation/controller/) (`controller.py` = map, `outcome.py` = compose, `verdict.py` = verdict adapter) |
| **Action** (MTDSim substrate) | the outcome oracle (M4) — one verb, native time cost, its own dice, no succession | [`attack_operation.py`](../../../../mtdnetwork/operation/attack_operation.py) (`step`, `_do_*`, `assert_action_context`) |
| **Driver** (execution) | one seeded walk: enter → dwell → dispatch → step → verdict → compose → sample | [`attacker.py`](../../../../src/mtdsim/l3_simulation/movement/attacker.py) (`MovementAttacker._walk`) |

The trichotomy is the one in
[`success_failure_overlay_design.md`](success_failure_overlay_design.md):
**structure** = the net's legal-move grammar; **policy** = which enabled move fires
on which verdict; **execution** = one seeded walk. Verifying the seams *is*
verifying the separation.

## Per-proposition verdicts

Status key: **✓ confirmed** · **✓ clarified** (true, but a seam was described
loosely and the code draws it more finely) · **◆ decision** (ruling required).

### P1 — "OGASP = GASP (movement) + controller (weights + mapping) + MTDSim action." — ✓ clarified
The driver holds exactly three injected collaborators (`routing_net`;
`controller` + `overlay`; `attack_op` + `verdict_of`) and forks none of their logic
— it only calls `phase_for`, `step`, `verdict_of`, `compose`, and its own
`_sample`. **Clarification:** "controller = weights **and** mapping" is right, but
the *weights split in two*. The **base** weights are **structure** (GASP + synthetic
overlay, in `net.py`); only the **success/failure** weights are the **controller's
policy** (`outcome.py`). The base proportions are *conditioned*, never re-derived
([`../../metrics_semantics.md`](../../metrics_semantics.md) §(f)). Verified: `net.py`
imports nothing from `controller/` (seam 1 below).

### P2 — "The attacker overlays the pre-attack tactics onto itself, then begins at the first tactic (one token)." — ✓ clarified
**Load-bearing clarification:** the pre-attack (synthetic) overlay is **not**
applied by the attacker at runtime. It is composed at **net-build**, in
[`net.py::_compose_out`](../../../../src/mtdsim/l3_simulation/movement/net.py) when
`load_routing_net(with_synthetic_overlay=True)`. The attacker receives an
already-composed, immutable `RoutingNet` (a frozen dataclass; `base_out_weights`
returns a *copy*) and never mutates its own structure — this is the separation that
keeps *structure* fixed before *execution* begins. "Begins at the first tactic" is
the D8 entry arm: `_choose_entry` seeds at `reconnaissance` (overlay-on) or
`initial-access` (observed-only). The token is the single `place` variable in
`_walk` — one token, confirmed.

### P3 — "The tactic corresponds to an action via the controller mapping." — ✓ confirmed
`controller.phase_for(place)` → verb, 15 tactics → 6 verbs, complete coverage,
test-enforced ([`test_controller.py`](../../../../tests/l3_simulation/test_controller.py)).
**Coarseness is intended and is the experiment-1 input parameter** (swappable by
editing `controller.csv`; [`controller.md`](controller.md) §2): the map is
many-to-one — `initial-access` → `SCAN_PORT` (not exploit), the Actions-on-Objectives
band → `SCAN_NEIGHBOR`. To be *recorded in the write-up* so a reader knows the
tactic→verb collapse is a chosen parameter, not a fidelity claim.

### P4 — "The simulator returns success/failure; minimal MTDSim changes; calling phases out of order gives more failures." — ✓ confirmed + quantified
**Minimal changes: confirmed.** The carve is `step(verb)` + `assert_action_context`
+ the `driven=True` kwarg on `_do_exploit_vuln`; the native FSM path is
byte-identical (the golden headline **692 records / 41 hosts** reproduces —
[`test_movement_integration.py::test_native_baseline_reproduces_its_golden_headline`](../../../../tests/l3_simulation/test_movement_integration.py)),
and the carve is confined to `mtdnetwork/operation/` (D5, seam 4).
**Out-of-order → more failures: confirmed, and by design.** The verbs share state
(`curr_host`, `curr_ports`) the native call-order guarantees; a net walking tactics
in a different order routinely reaches a verb whose precondition is unmet. The
driver records this as `PRECONDITION_UNMET` (tag `blocked`, verdict `failure`) and
lets the overlay route it — it does **not** re-impose native order, because that
would manufacture the very coupling the evaluation is meant to expose
([`action_layer_anatomy.md`](action_layer_anatomy.md) §6, H-coupling). No substrate
time is consumed on a block (the verb never ran).

**The H-coupling as a number** (horizon 15 000, no MTD, seeds 0–7/42/1234 = 10 runs
per cell; the blocked-fraction is the H-coupling finding, a *result to report*, not
a defect to hide):

| arm | profile | ev/run | blocked% | compromise events | distinct hosts (Σ over 10) |
|---|---|--:|--:|--:|--:|
| overlay | aggregate | 479 | 78% | 134 | 4 |
| overlay | pure_steal | 209 | 96% | 0 | 0 |
| overlay | pure_impediment | 426 | 38% | 734 | 12 |
| overlay | double_extortion | 74 | 0% | 102 | 7 |
| overlay | infrastructure_setup | 502 | 0% | 931 | 22 |
| observed | aggregate | 480 | 78% | 136 | 4 |
| observed | pure_steal | 210 | 97% | 0 | 0 |
| observed | pure_impediment | 483 | 88% | 152 | 4 |
| observed | double_extortion | 67 | 100% | 0 | 0 |
| observed | infrastructure_setup | 124 | 99% | 0 | 0 |

The blocked-fraction spans **0 %–100 %** across profile × arm — precisely the
H-coupling signal: a profile whose net ordering happens to route through
preconditions in a satisfiable order blocks little and compromises hosts; one that
does not is almost entirely blocked. Compromises are sparse and seed-dependent by
design (the coarse experiment-1 controller + precondition gating). **Reproduces the
build-session observation exactly:** aggregate/overlay seed 42 → 2 hosts, seeds
7/1234 → 0. (Full per-cell rows regenerable from the matrix runner; see the
first-numbers run for the reported aggregation with CIs.)

### P5 — "The signal goes back to the petri net during the tactic; the net calculates the next tactic from the signal and the weights." — ✓ clarified
**Second load-bearing clarification:** the **petri net does not calculate the next
tactic**. It supplies `base_out_weights(place)` only. The **controller** transforms
those (`OutcomeOverlay.compose(place, verdict, base)` — the M2
multiply-then-renormalise); the **driver** samples (`_sample`); the **verdict** is
read by `verdict_for` from the substrate outcome. The accurate telling: *substrate
returns an outcome → controller reads a verdict and composes a verdict-conditioned
distribution → driver samples the next place from it.* **Timing:** the verdict is
read **after** `step()` returns (after the verb's time cost and the D4 dwell) and
routes the **next** transition — not "during" the tactic; MTTC reads off these
timestamps. **Directionality confirmed with the live numbers:** at `initial-access`
(aggregate, overlay-on), failure swings `→ reconnaissance` from **0.004** (success)
to **0.643** (failure) — "back to the drawing board", live.

### P6 — "The existing weights are transformed by the signal, then the next transition is randomly selected." — ✓ confirmed
`compose` (multiply-renormalise; absent-pair = 1.0 passthrough; present-`0` =
hard-suppress) → `_sample` (destinations sorted before the cumulative draw, over a
dedicated `random.Random(seed)`). **RNG isolation verified:** the sampler uses its
own `Random(seed)`, so token sampling neither reads nor perturbs the substrate's
global `random` / `numpy` draws — the baseline and movement arms stay independently
seedable. SIM-05 determinism is test-pinned
([`test_movement_integration.py::test_determinism_same_inputs_identical_records`](../../../../tests/l3_simulation/test_movement_integration.py)).

### P7 — "This continues until the simulation ends; the attacker loops in the petri net until sim end." — ◆ decision
`_walk` loops until one of five conditions: (a) `end_event` (objective met) →
`SIM_END`; (b) the horizon censor (`env.run(until=horizon)`); (c) `max_events`
backstop → `MAX_EVENTS`; (d) a **stall** (compose returns `{}`) — walk ends; (e) a
**sink** (a place with no base out-edges) — walk ends. "Loops until sim end" is the
*intended primary* path, but (d) and (e) can end a walk early.

- **(d) stall is unreachable** — both overlay files carry **zero** zero-valued cells
  (`failure.json` / `success.json`: 0 zero-pairs each), so no verdict zeroes an
  out-set. No stall termination was observed across the matrix. Ignore unless the
  numbers change.
- **(e) sink is real and profile-dependent.** Sink enumeration (a place with no
  flow-backed observed out-edge *and* no synthetic out-edge):

  | profile | overlay-on sinks | observed-only sinks |
  |---|---|---|
  | aggregate | — | — |
  | pure_steal | `impact` | `impact` |
  | pure_impediment | — | — |
  | double_extortion | `credential-access` | `credential-access`, `reconnaissance`, `resource-development` |
  | infrastructure_setup | `defense-impairment` | `defense-impairment`, `reconnaissance`, `resource-development` |

  Over the matrix, **pure_steal** terminates early at the `impact` sink (9/10 runs,
  both arms) and **double_extortion** at the `credential-access` sink (10/10, both
  arms); infrastructure_setup/observed terminates at the `reconnaissance` sink
  (10/10). These walks are **censored short**, which changes the MTTC denominator
  and the per-profile event counts.

> **Superseded for experiment 2 by S5 (2026-07-21).** The ruling below stands as
> the **experiment-1** behaviour and is retained as the comparison arm, but the
> supervisor has since directed the opposite treatment going forward: a token
> reaching a sink **retraces the edge it travelled** rather than the run being
> discarded (an alternative raised in the meeting: route to some other node).
> The consequences of accept-and-censor recorded below — truncated observation
> windows, a shortened MTTC denominator for `pure_steal`, `double_extortion` and
> `infrastructure_setup`/observed — are exactly what the change is meant to
> remove, and they materialised in experiment 1 as predicted
> ([`experiment_01_findings.md`](experiment_01_findings.md) Finding 3). The
> replacement policy and its implications are worked through in
> [`../../../handoffs/2026-07-27_sink_retrace_experiment2.md`](../../../handoffs/2026-07-27_sink_retrace_experiment2.md).

**The decision — ruled by Marc (2026-07-23): accept-and-censor.** A walk that reaches
a sink **stops and is censored**, recorded as a sink termination (tag on the last
record's `next_place is None` with `is_sink(place)` true). This is the current code
behaviour — **no change** — and the low-risk default for experiment-1 "behaviour,
not numbers". The consequence is on record: profiles that sink early (pure_steal at
`impact`, double_extortion at `credential-access`, infrastructure_setup/observed at
`reconnaissance`) contribute **truncated observation windows**, which shortens their
MTTC denominator relative to profiles that run the full horizon — this must be
stated when the per-profile MTTC is reported. Re-seed / bounce was considered and
declined for this pass: it adds a routing policy not in the code and belongs to a
reviewed follow-up, not a verification gate.

### P8 — "This is compared to the baseline attacker originally in MTDSim." — ✓ confirmed (path) + comparability re-affirmed
Baseline = `proceed_attack` (untouched 6-phase FSM; 692/41 golden); movement =
`MovementAttacker`; both run in the same `GEOMETRY`
([`run.py`](../../../../src/mtdsim/l3_simulation/movement/run.py)); the reader
([`statistics.py`](../../../../src/mtdsim/l3_simulation/movement/statistics.py))
yields MTTC/ASR without touching the inherited `AttackStatistics` maths.
**Comparability re-affirmed — MTTC means the same on both arms.** The three
compromise events the reader keys on —
`(EXPLOIT_VULN, EXPLOIT_COMPROMISED)`, `(BRUTE_FORCE, TRUE)`, `(SCAN_PORT, TRUE)` —
are **exactly** the three `_do_*` branches that call
`update_compromise_progress` in the substrate (`_do_exploit_vuln` on compromise,
`_do_brute_force` on `True`, `_do_scan_port` on a reuse hit). That is the single
substrate procedure that appends to `compromised_hosts` and fires the `end_event` —
identical on both arms. `ENUM_HOST`'s re-control call to the same procedure is a
no-op on the distinct-host set (guarded by `not in get_compromised_hosts()`) and is
correctly **not** counted as a compromise event. Cross-check over the matrix: in
**0** runs did the reader's compromise-event count fall below the substrate's
distinct-host count (`compromised_count`); where they differ, events ≥ hosts (extra
events are re-compromise records on an already-owned host), so
`first_compromise_time` is never inflated. The comparison stays
**within-substrate only** — internal MTTC, no cross-paper magnitude claim
([`../../metrics_semantics.md`](../../metrics_semantics.md) §(d)).

## The four seams, as first-class invariants

Each seam now has a check that fails loudly if a future edit blurs it:

1. **Movement ⊥ Controller.** `net.py` carries no verdict/compose logic; `compose`
   never calls back into the net (`base_out_weights` reaches it as a *parameter*).
   *Check:* [`test_seam_invariants.py::test_seam1_movement_net_imports_no_controller_and_no_simpy`](../../../../tests/l3_simulation/test_seam_invariants.py)
   — `net.py` imports nothing from `controller/` and no SimPy.
2. **Controller ⊥ Action.** The controller is pure and SimPy-free; it never calls
   `step()`. *Check:*
   [`test_seam_invariants.py::test_seam2_controller_is_simpy_free_and_does_not_import_movement`](../../../../tests/l3_simulation/test_seam_invariants.py)
   (`verdict.py` may import the substrate outcome *constants* — plain strings — but
   no SimPy and no movement); the totality of `verdict_for` / `compose` is
   unit-tested in [`test_controller_outcome.py`](../../../../tests/l3_simulation/test_controller_outcome.py).
3. **Driver consumes, never forks.** `attacker.py` holds no dispatch/compose/verdict
   semantics of its own. *Check:*
   [`test_movement_attacker.py::test_driver_delegates_verdict_and_composition`](../../../../tests/l3_simulation/test_movement_attacker.py).
4. **Attacker-only (D5).** No behavioural change under `mtdnetwork/component` or
   `mtdnetwork/mtdai`; the carve is confined to `mtdnetwork/operation`. *Check:*
   [`test_movement_smoke.py::test_g6_no_behavioural_change_under_substrate_boundary`](../../../../tests/l3_simulation/test_movement_smoke.py).

## What this unblocks, and what it does not

- **Unblocks** the first-numbers run
  ([`experiment_01_findings.md`](experiment_01_findings.md)):
  the model and the code agree in the telling, not just the behaviour; the P4
  H-coupling table is a result to report; P8 is comparably measured.
- **Two things to carry into the write-up:** (P3) state that the tactic→verb
  collapse is a chosen input parameter; (P4) report the blocked-fraction table as
  the H-coupling finding.
- **Does not** pull numbers, tune weights, edit the map, or add substrate
  behaviour. The one open item is P7's sink-termination ruling.
