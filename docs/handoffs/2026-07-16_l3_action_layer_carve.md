---
status: open
created: 2026-07-16
---

# Carve the six action-layer verbs into standalone-callable actions — separate each verb's executable core from its hard-coded successor tail-call, so a controller can invoke actions individually and own the succession, while the inherited FSM still runs unchanged as the baseline

> **Build-phase follow-on to the action-layer anatomy** (read-only; now recorded in
> [`../implementation/pipeline/ogasp/action_layer_anatomy.md`](../implementation/pipeline/ogasp/action_layer_anatomy.md)).
> This handoff carries the forward-looking, code-writing component the anatomy
> deliberately deferred — the anatomy *specified* the carve (§3.3) but did not perform
> it. Gated on Marc's review of the anatomy record. Motivation (Marc, 2026-07-16): the
> six verbs are welded in order *and* meaning — each `_execute_*` core tail-calls its
> own successor and communicates only through shared adversary state — so a controller
> cannot drive them in a net-imposed order without either synthesising state at each
> entry (near-zero reordering freedom) or carving the cores free of their tails. This
> handoff builds the carve, if the entry-plus-synthesis route is judged insufficient.

## State of play

- **The anatomy is done and is the sole input.** The record's
  [§2.2](../implementation/pipeline/ogasp/action_layer_anatomy.md) (per-verb
  reads/mutations/tail-calls/preconditions), [§3.2](../implementation/pipeline/ogasp/action_layer_anatomy.md)
  (callability classification: `SCAN_HOST` callable-as-is, `ENUM_HOST`
  callable-with-context, the other four chain-bound), and
  [§3.3](../implementation/pipeline/ogasp/action_layer_anatomy.md) (the carve,
  specified) are the design inputs. Do not re-derive them.
- **The decisive constraint is baseline preservation.** The inherited FSM is the
  procedural baseline every golden was captured against
  ([`project_context.md`](../workflows/project_context.md); the substrate seam in
  [`architecture.md`](../implementation/architecture.md) §(f)). The carve **must not
  change baseline behaviour** — the seeded goldens must reproduce bit-for-bit
  (SIM-05 determinism). So this is not "delete the tail-calls"; it is "expose the cores
  *without* disturbing the path the baseline drives".
- **The two-lever finding frames the build.** Without a carve, a controller has only:
  choose the entry phase, and pre-populate the state a verb assumes (record §3.1). The
  carve adds the third lever — controller-owned succession — and is the minimal change
  that turns the machine into a callable surface.
- **This is where the read-only constraint lifts.** The anatomy was read-only; this
  handoff writes code in `mtdnetwork/operation/attack_operation.py` (and possibly
  `adversary.py`). It stays inside the attacker-only boundary (D5).

## Recommended approach

Carve by **extracting each verb's executable core into a pure action that returns its
branch outcome, and demoting the tail-call to a caller's decision** — done additively so
the baseline path is untouched. Three implementation shapes were considered; pick from
this shortlist:

1. **Core-extraction with a thin FSM wrapper (recommended).** Split each `_execute_*`
   into (a) a pure `_do_*` that performs the action, mutates state, and *returns* the
   branch condition (compromised? / reuse-hit? / stack-empty?), and (b) the existing
   `_execute_*`, rewritten to call `_do_*` and then tail-call the native successor
   exactly as today. The baseline calls `_execute_*` and is bit-identical; a controller
   calls `_do_*` and reads the returned outcome to choose the next verb itself. *Why
   this one:* the native path is preserved by construction (the wrapper is the old body),
   and the callable surface is the clean `_do_*` set — no mode flag threading through the
   FSM.
2. **Controller-mode flag.** A single `controller_driven` boolean that each core checks
   before its tail-call, suppressing it when a controller is in charge. *Rejected as
   primary:* it litters every core with a branch and risks a missed site silently
   re-entering the native chain (the anti-goal via a bug); the extraction makes the two
   paths structurally separate instead.
3. **Full state-machine rewrite (event-returning stepper).** Replace the tail-call chain
   with a `step()` that returns the next event to the caller. *Rejected for now:* largest
   diff, hardest to prove baseline-identical, and unnecessary if the extraction gives the
   controller what it needs. Hold as a later option if the controller needs finer
   stepping than `_do_*` provides.

Whichever shape: **land it behind a determinism check first** (capture goldens, carve,
re-run, diff) so baseline preservation is proven, not assumed.

## Validation gate

Done when:
1. The inherited FSM still reproduces the seeded goldens **bit-for-bit** (SIM-05) — the
   carve is provably baseline-neutral.
2. Each of the six cores is invocable in isolation given its documented precondition
   context (record §2.2) — the four chain-bound verbs run when handed a synthesised
   `curr_host` / `curr_ports`, and fail loudly (not silently degenerate) when not.
3. A controller can drive at least one **non-native** verb order end-to-end (the order
   the tail-calls would not produce), demonstrating the third lever exists.
4. No new dependency; determinism preserved; the change is inside `mtdnetwork/operation/`
   (+ `adversary.py` if needed), nothing substrate-behavioural.
5. Marc has reviewed the carve design before it lands.

## Hard constraints

- **Baseline is sacrosanct.** The goldens must not move. If they do, the carve is wrong —
  do not re-baseline to accommodate it (that would destroy the comparison). See
  [`metrics_semantics.md`](../implementation/metrics_semantics.md) on within-substrate
  comparability.
- **Attacker-only boundary (D5).** No substrate/defender/HARM edits; the give-up and
  vuln-ranking mechanics stay as inherited.
- **Determinism / SIM-05** across the carve.
- **Don't "fix" the half-wired give-up** (record §4.2, `verify`) as a side effect — it is
  an open inherited-vs-editorial disposition for Marc, not carve scope.
- Branch hygiene; **never push without an explicit ask**; Australian English.

## Reading list

- [`../implementation/pipeline/ogasp/action_layer_anatomy.md`](../implementation/pipeline/ogasp/action_layer_anatomy.md)
  §2.2 / §3.2 / §3.3 — the per-verb ledger, the callability classes, and the carve spec.
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  — the cores to split; the tail-calls to demote.
- [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  — the shared state the cores read/write.
- [`../../baseline/run_baseline.py`](../../baseline/run_baseline.py) and
  [`../../baseline/BASELINE.md`](../../baseline/BASELINE.md) — how the goldens are
  captured, for the determinism gate.
- [`./2026-07-15_l3_tactic_action_influence_map.md`](./2026-07-15_l3_tactic_action_influence_map.md)
  — the consumer: per-pair verdicts need the carved, callable surface to be real.

## Out of scope (explicitly)

- The tactic→action influence map itself (separate handoff — this carve is its
  enabler, not its content).
- The feedback-net / movement-layer design that *drives* the carved actions
  ([`./2026-07-15_l3_feedback_net_design.md`](./2026-07-15_l3_feedback_net_design.md)) —
  this handoff makes the actions drivable; it does not build the driver.
- The two-way net↔substrate coupling (the deferred C3 extension in
  [`../implementation/pipeline/ogasp/binding_design_space.md`](../implementation/pipeline/ogasp/binding_design_space.md)).
- Any substrate/defender/HARM change; the give-up disposition; metrics work.
