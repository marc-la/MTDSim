---
status: open
created: 2026-07-15
---

# Build the profiled attacker (M7) — a new movement-layer attacker class that steps the class net live inside MTDSim, dispatches the mapped substrate actions, and feeds the binary outcome back as conditional weights, alongside the untouched 6-phase baseline

> **Third in the post-meeting chain — blocked on the two records before it.**
> Implements the contract from the success/failure outcome-overlay design
> ([`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md);
> supersedes the feedback-net design handoff)
> using the map from
> [`./2026-07-15_l3_tactic_action_influence_map.md`](./2026-07-15_l3_tactic_action_influence_map.md).
> Do not start before both are Marc-reviewed. This replaces the retired
> replay-attacker handoff (2026-07-03): the one-way timeline replay it would
> have built died with D2→M1; the validation discipline it carried (goldens,
> determinism, attacker-only boundary) survives here unchanged. Per the
> meeting: once this runs, the implementation phase is essentially done —
> what remains is pulling numbers and writing.

## State of play

- **The seam is named and settled** (architecture §(f)): the profiled
  attacker lives **alongside** the inherited 6-phase
  [`Adversary`](../../mtdnetwork/component/adversary.py) /
  [`AttackOperation`](../../mtdnetwork/operation/attack_operation.py) —
  selection per-run, no inheritance, both must keep working. Jin's M7
  wording: a new layer/class for movement on top of the existing simulator,
  which is called as an API; deep edits to the well-integrated existing
  model are to be avoided.
- **The inherited machinery is reused, not rebuilt:** the SimPy
  interrupt/penalty pattern, exploit pricing, attempt limits, and compromise
  bookkeeping stay authoritative — the movement layer calls them and reads
  their outcomes (the oracle contract).
- **The post-2c goldens**
  ([`../../baseline/golden/`](../../baseline/golden/)) are the behavioural
  oracle for "the baseline still works"; the attacker-only boundary (D5) is
  auditable via `git diff` against `mtdnetwork/component/` (network/host/
  service/MTD) and `mtdnetwork/mtdai/`.
- **Nothing coupled exists yet.** The L3a net build code
  ([`../../src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri))
  and the standalone timeline runner exist; the runner stays as the
  analytical track and is not consumed here.

## Recommended approach

1. **The movement layer.** A new attacker class in the same module family as
   `Adversary`, selected per-run via the existing entry points. It owns: the
   loaded class net (schema-pinned), the token position, the conditional
   weight logic, and the seeded RNG stream. Per the design record's
   lifecycle: enter place → dwell → dispatch mapped action(s) through the
   existing operation machinery → read the binary verdict → select weight
   set → transition.
2. **The oracle adapter.** A thin read-only interface over the existing
   action outcomes (exploit landed / attempt limit / interrupt), returning
   the binary verdict per the map's definitions. No changes to the actions
   themselves.
3. **Records.** Emit the per-event record from the design contract; extend
   the statistics layer with a *reader* for the new records (MTTC/ASR per
   class) without altering the maths for the old ones.
4. **Tests.** Mechanical gates below, plus a smoke matrix cell (one class ×
   one MTD × a few seeds) to prove the loop end-to-end before the full
   matrix handoff.

*Alternatives considered:* adapting the 6-phase loop in place — forbidden
(alongside-not-replacing, architecture §(f)). Consuming pre-generated
timelines with post-hoc correction — the dead end M1 closed.

## Validation gate

Done when:
1. **Goldens pass:** the 6-phase baseline reproduces
   [`../../baseline/golden/`](../../baseline/golden/) byte-for-byte under
   documented seeds — no shared code path changed behaviour.
2. **Determinism (SIM-05):** same net + seed → identical event records,
   mechanically tested.
3. **The feedback loop is real:** a mechanical test shows a forced failure
   verdict (e.g. an MTD interrupt mid-action) producing a backward/retry
   transition that a forced success does not — net state demonstrably moves
   with substrate outcomes.
4. **Schema pinning:** the class refuses a net artefact version it doesn't
   know.
5. All five profiles (4 classes + aggregate) run to termination or horizon
   on the smoke cell, emitting non-degenerate records the statistics reader
   turns into MTTC/ASR.
6. **Boundary audit:** `git diff` shows no behavioural change under
   `mtdnetwork/component/` (network/host/service/MTD) or `mtdnetwork/mtdai/`
   — attacker-side additions and a statistics *reader* only.

## Hard constraints

- **Never modify the 6-phase attacker's behaviour** — alongside, per-run
  selection (architecture §(f) decision block).
- **Attacker-only (D5):** HARM / MTD mechanisms / orchestrator / statistics
  maths untouched.
- **Implement the design record exactly** — deviations go back to the
  record first (contract-first discipline).
- **Within-substrate comparability only** — internal MTTC; no cross-paper
  magnitude claims
  ([`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md) §(d)).
- No IDS/detection; Tay's RL is run, never extended; R2/R3 hooks preserved,
  not built.
- Determinism (SIM-05); branch hygiene; **never push without an explicit
  ask**; Australian English.

## Reading list

- [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  → the contract, in full, first (the M2 policy overlay; supersedes the
  feedback-net design handoff). Its artefact:
  [`../../data/ogasp/petri/outcome_overlay.json`](../../data/ogasp/petri/outcome_overlay.json).
- [`./2026-07-15_l3_tactic_action_influence_map.md`](./2026-07-15_l3_tactic_action_influence_map.md)
  → its record + ledger — the dispatch and verdict definitions.
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  — the machinery being called (interrupt pattern especially).
- [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  — what "alongside" coexists with.
- [`../../baseline/BASELINE.md`](../../baseline/BASELINE.md) +
  [`../implementation/mtdsim_spec.md`](../implementation/mtdsim_spec.md) —
  the oracle and row-level invariants.

## Out of scope (explicitly)

- The full experiment matrix and numbers review (the first-numbers handoff).
- R2 success-rate tuning, R3 styles, evasion/persistence action enrichment,
  richer outcome classes, the C2 capability layer — post-first-numbers.
- Duration calibration (R1), corpus expansion, two-way upgrades beyond the
  M2 conditional-weight form.
