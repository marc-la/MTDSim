---
status: in-progress
created: 2026-07-22
updated: 2026-07-22
lineage: reframed from 2026-07-15_l3_profiled_attacker_build.md (M7); re-pointed onto the controller sublayer
---

> **Progress (2026-07-22).** The movement layer is **built and tested**, in
> [`src/mtdsim/l3_simulation/movement/`](../../src/mtdsim/l3_simulation/movement/)
> — `net.py` (schema-pinned routing net: observed D3 weights composed with the M6
> synthetic overlay), `attacker.py` (`MovementAttacker`, the live SimPy net-walker
> + `MovementRecord`), `statistics.py` (a *reader* → MTTC/ASR per profile),
> `run.py` (run wiring, D8 arms, controller injection). Tests:
> [`tests/l3_simulation/test_movement_{net,attacker,smoke}.py`](../../tests/l3_simulation/)
> (27 new; full suite 167 green). **What is proven now** (against injected,
> controlled controller collaborators, since the overlay `compose` + verdict
> adapter are the parallel controller handoff's surface): the per-place lifecycle
> runs end-to-end; determinism (SIM-05); the feedback loop is real (a forced
> failure vs a forced success at the same place select different transitions; an
> MTD interrupt reads as failure and routes); schema pinning refuses an unknown
> net; the smoke matrix runs all five profiles emitting readable records; the
> native no-MTD golden headline (692/41) is unperturbed and the boundary audit is
> clean (zero diff under `mtdnetwork/component` · `mtdnetwork/mtdai`). **What
> remains (scope expanded 2026-07-22 — Marc folded the blocking controller pieces
> into this handoff):** implement the real `verdict_for` + `OutcomeOverlay.compose`
> + the `EXPLOIT_VULN`-interrupt carve tweak, then validate the whole thing
> end-to-end plug-and-play (both the baseline and the movement attacker). The
> five-step execution plan — concrete mappings, files, and the plug-and-play test
> matrix — is in **§ Execution plan** below; `run.py` already wires the real library
> by default, so no run-side change is needed. Behaviour is the bar, not the numbers
> (those stay provisional, pending Marc's greenlight). Delete this handoff in the
> commit that lands the plan and re-runs the gates against the real controller.

# Build the attacker Petri → MTDSim — a new movement-layer attacker class that steps the class net live inside MTDSim, dispatches verbs and composes the outcome overlay through the controller sublayer, feeds the binary outcome back to route the token, alongside the untouched 6-phase baseline

> **Second of the two forward build handoffs — blocked on the controller
> finalisation** ([`./2026-07-22_l3_controller_success_failure.md`](./2026-07-22_l3_controller_success_failure.md)).
> That handoff delivers the controller as a SimPy-free library: dispatch
> (`phase_for`), overlay composition (`compose`), and the verdict adapter
> (including MTD-interrupt-as-failure). **This handoff is the full two-way build**:
> wire that library into a live SimPy attacker that walks the Petri net inside
> MTDSim. Per the July meeting, once this runs the implementation phase is
> essentially done — what remains is pulling numbers and writing
> ([`./2026-07-15_l3_first_numbers.md`](./2026-07-15_l3_first_numbers.md)).

## State of play

- **The seam is settled** (architecture §(f)): the movement-layer attacker lives
  **alongside** the inherited 6-phase
  [`Adversary`](../../mtdnetwork/component/adversary.py) /
  [`AttackOperation`](../../mtdnetwork/operation/attack_operation.py) — per-run
  selection, no inheritance, both keep working. M7: a new movement layer on top
  that calls the existing action machinery as an API.
- **The controller is (will be) a ready library.** After the finalise handoff:
  `controller.phase_for(tactic)` → the verb; `controller.compose(place, verdict)`
  → the renormalised out-weights; the verdict adapter → the binary verdict from a
  verb's outcome + interrupt. This build **consumes** those; it does not re-derive
  dispatch, composition, or verdict semantics.
- **The nets, durations, and overlays exist.** Five weighted structural nets
  ([`../../data/ogasp/petri/`](../../data/ogasp/petri/)), the dwell catalogue
  ([`../../data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json)),
  the synthetic (structural) overlay
  ([`../implementation/pipeline/ogasp/synthetic_overlay.md`](../implementation/pipeline/ogasp/synthetic_overlay.md)),
  and the outcome (policy) overlay (finalised in the controller handoff).
- **The goldens are the oracle.** The post-2c goldens
  ([`../../baseline/golden/`](../../baseline/golden/)) prove "the baseline still
  works"; the attacker-only boundary (D5) is auditable via `git diff` against
  `mtdnetwork/component/` and `mtdnetwork/mtdai/`.
- **Nothing coupled exists yet.** The standalone timeline runner stays the D1
  analytical track and is not consumed here.

## Recommended approach

1. **The movement layer.** A new attacker class in the same module family as
   `Adversary`, selected per-run. It owns the loaded class net (schema-pinned), the
   token position, and the seeded RNG. Per-place lifecycle, all through the
   controller library:
   `enter place → dwell (D4 duration) → controller.phase_for(tactic) → step(verb) →
   verdict adapter → controller.compose(place, verdict) → sample next transition`.
2. **Entry point (D8), two declared arms.** Load the net with the synthetic overlay
   and seed at `reconnaissance` (kill-chain head), or observed-only and seed at
   `initial-access` (comparison arm) — a `with_synthetic_overlay` toggle at
   net-build, not a second code path.
3. **Records.** Emit the per-event record (place, verb, verdict, overlay branch,
   transition taken, sim time); extend the statistics layer with a *reader* for the
   new records (MTTC/ASR per class) — a reader only; do not alter the maths for the
   old records.
4. **Tests.** Mechanical gates below, plus a smoke matrix cell (one class × one MTD
   × a few seeds) to prove the loop end-to-end before the numbers handoff.

*Alternatives considered:* adapting the 6-phase loop in place — forbidden
(alongside-not-replacing, architecture §(f)). Re-implementing dispatch/composition
here instead of consuming the controller library — rejected (the finalise handoff
owns that surface; this build calls it).

## Validation gate

Done when:
1. **Goldens pass:** the 6-phase baseline reproduces
   [`../../baseline/golden/`](../../baseline/golden/) byte-for-byte — no shared
   code path changed behaviour.
2. **Determinism (SIM-05):** same net + overlay + seed → identical event records.
3. **The feedback loop is real:** a forced failure verdict (incl. an MTD interrupt
   mid-action) produces a backward/retry transition a forced success does not — net
   state demonstrably moves with substrate outcomes (the two-way demonstration).
4. **Schema pinning:** the class refuses a net artefact version it does not know.
5. All five profiles (4 classes + aggregate) run to termination or horizon on the
   smoke cell, emitting non-degenerate records the statistics reader turns into
   MTTC/ASR.
6. **Boundary audit:** `git diff` shows no behavioural change under
   `mtdnetwork/component/` or `mtdnetwork/mtdai/` — attacker-side additions and a
   statistics *reader* only.

## Hard constraints

- **Never modify the 6-phase attacker's behaviour** — alongside, per-run selection.
- **Attacker-only (D5):** HARM / MTD mechanisms / orchestrator / statistics maths
  untouched.
- **Consume the controller library** — do not fork dispatch, composition, or
  verdict semantics into the attacker.
- **Within-substrate comparability only** — internal MTTC; no cross-paper magnitude
  claims ([`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md) §(d)).
- No IDS/detection; Tay's RL run, never extended. Determinism (SIM-05); branch
  hygiene; **never push without an explicit ask**; Australian English.

## Reading list

- [`./2026-07-22_l3_controller_success_failure.md`](./2026-07-22_l3_controller_success_failure.md)
  + the [`controller`](../../src/mtdsim/l3_simulation/controller/) sublayer — the
  API this build consumes.
- [`../implementation/pipeline/ogasp/controller.md`](../implementation/pipeline/ogasp/controller.md)
  §3 (the end-to-end loop) + §4 (verdict).
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  (the carved machinery / interrupt pattern) and
  [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  (what "alongside" coexists with).
- [`../../baseline/BASELINE.md`](../../baseline/BASELINE.md) +
  [`../implementation/mtdsim_spec.md`](../implementation/mtdsim_spec.md) — the
  oracle and row-level invariants.

## Execution plan to close end-to-end (expanded scope — Marc's 2026-07-22 direction)

Marc widened this handoff's scope on 2026-07-22: **make the whole thing work
end-to-end, plug-and-play** across controller layers, movement layers (the five
Petri profiles), and sim settings, with **both** the native baseline and the
movement attacker behaving as expected — *behaviour*, not results (the overlay
numbers stay provisional / pending Marc's greenlight; see gate 5 of the controller
handoff). That folds the three still-missing pieces (previously deferred to the
controller handoff) into this one. None is SimPy work — the SimPy spine already
runs; these are the pure functions the loop calls plus one carve tweak. Planned,
**not yet done** (session ended on credits):

1. **Verdict adapter — `controller/verdict.py`, exported as `verdict_for`.** A pure
   `verdict_for(verb, outcome, interrupted=False) -> "success"|"failure"` per
   `controller.md` §4. Concrete mapping (the outcome is a carved `_do_*` return
   value):
   - `interrupted` **or** `outcome == EXPLOIT_HALTED` (non-sim-end) → **failure**.
   - `SCAN_HOST`: `bool` — `True` (hosts found) success, `False` (empty) failure.
   - `EXPLOIT_VULN`: `EXPLOIT_COMPROMISED` success, `EXPLOIT_UNCOMPROMISED` failure.
   - `BRUTE_FORCE`: `bool` — `True` (compromised) success, `False` failure.
   - `ENUM_HOST` / `SCAN_PORT` / `SCAN_NEIGHBOR`: **success** unless interrupted —
     documented simplification. Their §4 "failure" conditions (`ENUM_HOST` is a
     dispatcher; `SCAN_PORT` "empty" ports; `SCAN_NEIGHBOR` "no new neighbours")
     are not visible in the bare `_do_*` return (`_do_scan_neighbors` returns
     `None`; `_do_scan_port`'s bool is reuse-only). Empty-ports surfaces one step
     later as an `EXPLOIT_VULN` `PRECONDITION_UNMET` failure, so no signal is lost.
     A richer version would pass the adversary in to read `host_stack`/`curr_ports`
     deltas — deferred; the bool mapping is enough for "sim behaving as expected".
   `run.py::_default_verdict_adapter` already imports this exact name — it wires
   automatically once the file exists.

2. **`OutcomeOverlay.compose` — `controller/outcome.py` (replace the stub).** The
   M2 rule `w'(a→b) = base(a→b)·overlay_v(a→b) / Σ`. Per destination `b` in the
   passed `base_out_weights`, factor = the overlay value **if the `(a,b)` pair is
   present** in that verdict's `by_source[a]`, **else 1.0** (absent = unconditioned
   passthrough; a *present* `0` hard-suppresses — this distinction makes it robust
   to any net/overlay pairing, i.e. plug-and-play). Renormalise; if the sum is `0`
   (the verdict suppressed every out-edge) return `{}` — the **stall** (design §3),
   which `MovementAttacker._route` already reads as walk-termination. Consumes the
   provisional `data/ogasp/controller/{success,failure}.json` as-is; never edits the
   numbers.

3. **Carve extension for the `EXPLOIT_VULN` interrupt — `attack_operation.py`.** Add
   a `driven=False` kwarg to `_do_exploit_vuln`; on `simpy.Interrupt`, when
   `driven` **re-raise** (let the driver own succession) instead of spawning the
   native `_handle_interrupt` recovery. `step('EXPLOIT_VULN')` passes `driven=True`;
   the native `_execute_exploit_vuln` keeps the default, so its path — and the nine
   `baseline/golden` scenarios — stay **byte-identical** (the goldens are the proof).
   This edit is to `mtdnetwork/operation/`, the sanctioned attacker-side carve — it
   does **not** touch `mtdnetwork/component` or `mtdnetwork/mtdai`, so the D5
   boundary audit in `test_movement_smoke.py` still holds.

4. **Attacker cleanup — `movement/attacker.py`.** Once (3) lands, an `EXPLOIT_VULN`
   interrupt re-raises like the other five verbs, so `_dispatch` handles it through
   the single `except simpy.Interrupt` path; drop the `outcome == EXPLOIT_HALTED`
   special-case (keep the sim-end `EXPLOIT_HALTED → _SIM_END` handling).

5. **Plug-and-play integration test — `tests/l3_simulation/test_movement_integration.py`.**
   Drive the **real** controller (`load_controller`, `load_outcome_overlay`,
   `verdict_for` — no injected fakes) across the matrix: 5 profiles × {overlay-on
   seed-recon, observed-only seed-initial-access} × {no-MTD, one MTD scheme} × a
   couple of seeds. Assert each cell runs to horizon, emits records, the statistics
   reader yields MTTC/ASR, and the run is deterministic (SIM-05). Add one cell that
   runs the **native baseline** (`proceed_attack`) and the movement attacker in the
   same geometry and checks both behave (baseline compromises hosts and reproduces
   its golden headline; movement attacker walks and the two D8 arms differ). This is
   the "both working as one would expect" gate.

**After all five:** the validation gate closes against the real controller (not
fakes); `run.py` needs no change (it already defaults to the real library). Then
delete this handoff in that commit. The only thing outside code is Marc's greenlight
on the overlay numbers — behaviour is validated regardless of the numbers.

**Collision note:** items 1–2 touch files the parallel controller handoff also
claimed (`controller/outcome.py`, the verdict adapter). Marc folded them here
knowingly; reconcile with any concurrent controller-session edits before committing
(re-read those files first — they were being edited 2026-07-22 evening).

## Out of scope (explicitly)

- The full experiment matrix and numbers review
  ([`./2026-07-15_l3_first_numbers.md`](./2026-07-15_l3_first_numbers.md)).
- The full experiment matrix and numbers review
  ([`./2026-07-15_l3_first_numbers.md`](./2026-07-15_l3_first_numbers.md)).
- R2 success-rate tuning, R3 styles, richer outcome classes, duration calibration,
  the C2 capability layer — post-first-numbers.
