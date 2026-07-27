---
status: open
created: 2026-07-27
---

# Refine the action layer under the change freeze — audit the six inherited verbs and the movement carve for genuine defects, fix only what is a bug, and disposition everything else as inherited-by-design, so that experiment 2's failures are attributable to the model rather than to broken plumbing

**Chain position: wave 1 — run first, independently.** No design dependency on
the other handoffs, and it makes the substrate trustworthy before the controller
and weight work changes what is asked of it. Executes **S2**.

## State of play

**The ruling, and its exact boundary.** The supervisor has frozen the attacker
action set short-term: no action, ability, or attacker state is added, removed,
or altered — *"do not change the MTDSim code yet"*. What remains licensed is
**refinement of existing code and bug fixes**. This handoff is that licensed
work, and its hardest task is holding the line between the two.

**The distinction that governs every call here is already in the guardrails.** An
**inherited divergence** is the code's reality — to parameterise or document, not
to correct. A **bug** is unintended: it violates an invariant, or entered through
an unexplained change with no basis in the source papers. Fix bugs; do not
"fix" inherited reality. Applied to this audit, that means one thing above all:

**The precondition blocking observed in experiment 1 is not a bug.** The verbs
share state (`curr_host`, `curr_ports`) that the native call order guarantees; a
net walking tactics in a different order routinely reaches a verb whose
precondition is unmet, and the driver records `PRECONDITION_UNMET` and lets the
routing policy handle it. That was verified deliberate (P4), spans 0–100 % of
actions across profile and arm, and is a **result to report**. Re-imposing the
native order to make it go away would manufacture the very coupling the
evaluation exists to expose. Anything that looks like a fix for the blocked
fraction is out of scope by construction.

**Known items to disposition — the audit's starting list, not its limit:**

- **The global attack-attempt cap is inert** — the counter increments but the
  guard is commented out. Recorded as `diverged (inert)`. Decide: inherited
  reality to leave, or a defect to restore? It has a paper-free heuristic origin,
  so leaving it is defensible; either way it should stop being ambiguous.
- **The give-up rule fires only on the targeted network type.** The anatomy
  record flags this `verify`: on the general network no host is ever given up by
  that path, so an attacker can retry a host without bound. Determine which
  network type the experiments actually run, because if it is the general one,
  the give-up rule Brown specifies is inactive in every run to date.
- **The movement driver charges the per-tactic dwell *and* the verb's native
  cost.** Grep-level observation, to confirm: the driver applies the catalogue
  dwell, then dispatches a verb that charges its own `ATTACK_DURATION`. Whether
  that is double-charging or two distinct costs is a *design* question owned by
  the timing handoffs — record it here, do not resolve it here.
- **The movement attacker appears not to pay the MTD confusion penalty.** Also
  grep-level, and more consequential: on interrupt the native path applies an
  exponential penalty draw, while the driven path re-raises to the driver, which
  records the interrupt and routes. If the movement arm pays no penalty and the
  baseline arm does, the two arms are not paying the same price for the same
  defensive event — a comparability question that must at minimum be *stated*.
  Confirm it with a test before believing it, and note that S3 makes the penalty
  a movement-layer object anyway.
- **The interrupt-to-verdict wiring is already landed** (verified 2026-07-27):
  the verdict adapter reads an interrupt as failure for all six verbs. The
  "named build prerequisite" in the outcome-overlay design record is discharged;
  no work needed beyond confirming the test coverage.

## Recommended approach

1. **Audit before you touch anything.** Walk the six verbs and the carve, and
   produce a table: observed behaviour, whether it matches Brown's stated intent,
   whether it matches the paper lineage, and a disposition of **bug** /
   **inherited divergence** / **by design**. The two anatomy records already did
   most of the reading — this pass is looking for defects, which they were not.
2. **Fix only the bug rows, one commit each, each with a regression test.** A
   defect with no test is not fixed, it is moved.
3. **Treat the goldens as the tripwire.** The native baseline reproduces a
   692-record / 41-host headline, and that is the contract with every prior
   result. If a fix changes it, stop: either the fix is out of scope, or a
   deliberate re-baseline is needed, and a re-baseline is Marc's call and its own
   changelog entry — never a side effect.
4. **Record the non-bugs where the next reader will find them.** Anything
   dispositioned inherited-or-by-design goes into the anatomy record's register
   with its reasoning, so the next session does not re-litigate it.
5. **Report what you decline to fix.** The freeze means some real limitations
   stay in place; naming them is the deliverable, because they become either
   dwell-only tactics under the controller work or entries in the criterion's
   honest-negatives column.

*Alternatives considered:* fixing the friction by making verbs tolerant of
missing preconditions — rejected, that is an action-set change under a freeze
*and* it would erase the H-coupling finding. Deferring the audit until the freeze
lifts — rejected: the freeze exists precisely so that the next experiment
measures the model rather than the plumbing, which requires the plumbing to be
known-good now.

## Validation gate

Done when:

1. Every verb and the carve have a disposition row; no observed anomaly is left
   unclassified.
2. Every row classified **bug** is fixed with a regression test; every row
   classified otherwise carries its reasoning in the anatomy record.
3. The native baseline golden still reproduces (692 records / 41 hosts) and the
   full test suite is green.
4. The action set is unchanged: same six verbs, no new attacker state, no altered
   ability — demonstrable by diff.
5. The confusion-penalty asymmetry between the two arms is settled as fact
   (test-confirmed either way) and written down, whether or not it is acted on.
6. The seam invariants still hold — the movement net imports no controller, the
   controller stays free of the simulation library, the driver forks no
   semantics, and the carve stays inside the operation module.

## Hard constraints

- **No action added, removed, split, or altered; no new attacker state.** This is
  the freeze, and it is the whole point of the handoff.
- **Do not fix the precondition blocking.** It is the finding.
- **Determinism (SIM-05)** holds after every change; seeded runs stay
  reproducible and the two arms stay independently seedable.
- **Attacker-only (D5)** — no behavioural change to the network, host, service,
  MTD, or statistics layers.
- Never bypass a failing pre-commit hook; never re-baseline a golden without
  Marc's explicit call. Australian English; branch hygiene; never push without an
  explicit ask.

## Reading list

- [`../implementation/pipeline/ogasp/action_layer_anatomy.md`](../implementation/pipeline/ogasp/action_layer_anatomy.md)
  §1 (intent vs realisation), §2 (coupling graph), §4 (affordance and
  limitations register — where the dispositions land).
- [`../implementation/pipeline/ogasp/attacker_phase_catalogue.md`](../implementation/pipeline/ogasp/attacker_phase_catalogue.md)
  — per-verb preconditions and outcomes, at a glance.
- [`../implementation/pipeline/ogasp/runtime_verification.md`](../implementation/pipeline/ogasp/runtime_verification.md)
  §P4 (why blocking is deliberate), §P8 (what comparability rests on), and the
  four seam invariants.
- [`../implementation/mtdsim_spec.md`](../implementation/mtdsim_spec.md) — the
  row-level dispositions any "is this a bug" call must be checked against; and
  [`../implementation/provenance.md`](../implementation/provenance.md) for the
  inert-cap and give-up rows.
- [`../workflows/guardrails.md`](../workflows/guardrails.md) — the
  inherited-divergence-versus-bug rule this handoff turns on.

## Out of scope (explicitly)

- Any new capability: an evasion action, a tooling endowment, a privilege level,
  a durability parameter. All are named in the supervisor update and all are
  frozen.
- Changing the tactic-to-verb mapping — that is the controller handoff.
- Changing timing semantics — that is the timing pair, which this handoff feeds
  observations to and takes no decisions for.
- Re-running the experiment matrix.
