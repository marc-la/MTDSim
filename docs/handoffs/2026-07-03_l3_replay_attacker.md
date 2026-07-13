---
status: open
created: 2026-07-03
---

# Build the replay attacker — feed the net-generated timelines into MTDSim alongside the 6-phase baseline, run the v1 experiment matrix, and send Dr Hong the pre-semester progress update

> **The capstone of the v1 chain — run last.** The timeline runner has
> **SHIPPED** (2026-07-09; its handoff is deleted): the input contract is
> [`../../data/ogasp/timeline/timeline_schema.md`](../../data/ogasp/timeline/timeline_schema.md)
> (`ogasp-timeline/v1`, with committed example + behavioural report; the bulk
> library regenerates via `python -m mtdsim.l3_simulation.timeline`). Still
> depends on
> [`./2026-07-03_l3_binding_scoping.md`](./2026-07-03_l3_binding_scoping.md)
> (the tactic→action map, cost-only dispositions, success-model and
> MTD-interruption recommendations). This executes supervisor decisions
> D1/D2/D5 end-to-end: the attack behaviour inside MTDSim is dictated by the
> Petri net, via one-way timeline replay, with attacker-only substrate change.

## State of play

- **Upstream half landed (2026-07-09):** the timeline library — seeded, timed
  attacker-state sequences over the full run matrix (72 cells; entries per
  D8; weighted/uniform policies; central + sweep-extreme dwells) — exists
  under the gitignored `data/ogasp/timeline/_timelines/`, with the committed contract
  at [`../../data/ogasp/timeline/timeline_schema.md`](../../data/ogasp/timeline/timeline_schema.md).
  Still pending: the scoping note that fixes what each tactic-state does
  against the substrate.
- **The seam is already named in the architecture**
  ([`../specs/architecture.md`](../implementation/architecture.md) §(f)): the
  graph-driven attacker lives **alongside** the inherited 6-phase
  [`Adversary`](../../mtdnetwork/component/adversary.py) /
  [`AttackOperation`](../../mtdnetwork/operation/attack_operation.py) — the
  procedural baseline Tay's RL trained against and the basis of every golden.
  **Selection per-run, not inheritance. Both must keep working.**
- The inherited attacker is already a hand-rolled timed token-game
  (`_curr_process` = state; `_execute_attack_action` = fire with
  `env.timeout`; MTD = SimPy interrupt) — the replay attacker reuses that
  execution machinery and swaps the *sequencing source* (timeline instead of
  the hardcoded 6-phase loop).
- The post-2c goldens at [`../../baseline/golden/`](../../baseline/golden/)
  are the behavioural oracle for "the baseline still works".
- Nothing replay-shaped exists in the codebase.

## Recommended approach

**1 — The replay driver.** A new attacker class alongside `Adversary` (per
architecture §(f): same module family, per-run selection flag in the run
entry-points, no inheritance from the 6-phase loop). It consumes one timeline
record (pinned schema version) and walks it: at each state's window
`[t_enter, t_exit)`, execute the bound action(s) from
`tactic_action_map.csv` against the live network; `COST_ONLY` states consume
their dwell and emit a record without touching network state. Timing comes
from the timeline (schedule-authoritative); substrate action durations run
*inside* the window; the scoping note's recommendation governs what happens
when an action doesn't fit or an MTD interrupt fires mid-state
(implement exactly the recommended policy — e.g. state-fails-and-timeline-
advances — and log the per-state outcome `achieved | failed | interrupted`).

**2 — Output contract (architecture §(f)):** non-degenerate, timed,
technique/tactic-level attack records per run, distinct per class — the same
statistics pipeline ([`../../mtdnetwork/statistic/`](../../mtdnetwork/statistic))
must be able to compute MTTC/ASR from them, with the success semantics the
scoping note recommended (state-gated / objective-read), and the DES MTTC
clearly named as such (never conflated with the runner's net
time-to-objective).

**3 — The v1 experiment matrix (the result that goes to Hong).**
`MTD mechanism (SDR family + Tay AI selection, existing only) ×
{procedural 6-phase baseline, 4 class profiles, aggregate profile} ×
N seeds`, MTD intervals per the existing run conventions. Report per-cell
MTTC/ASR distributions with CIs and two headline statements: (a) do the class
profiles separate behaviourally *under MTD* (beyond the aggregate null)?
(b) does any MTD mechanism's **ranking** change between the procedural
baseline and a CTI profile? — the fidelity-changes-the-answer claim, phrased
envelope-relative. (E1 discipline: MTTC/attacker-effort discriminate;
end-of-sim compromise fraction does not at long horizons.)

**4 — The progress update.** Draft the pre-semester update to Dr Hong (the
minuted TODO): what shipped (weighted nets, durations catalogue, timeline
library, replay attacker), the matrix result headline, and the confirmed-vs-
pending decision list (aggregate profile, CVE-binding confirmation, corpus
expansion). Marc sends it — draft only.

*Alternatives considered:* event-authoritative replay (substrate timing
governs dwell; timeline gives sequence only) — closer to the two-way end
state but more divergence handling; rejected for v1 unless the scoping note
recommended it. Driving the net inside SimPy step-by-step — that *is* the
deferred two-way integration; not v1. Replacing the 6-phase attacker —
forbidden (architecture §(f) decision block; the comparative claim needs
both).

## Validation gate

Done when:
1. **The goldens still pass:** the 6-phase baseline reproduces
   [`../../baseline/golden/`](../../baseline/golden/) byte-for-byte under the
   documented seeds — the replay attacker is added *alongside*, and no shared
   code path changed behaviour.
2. A replay run on a given timeline is **deterministic** (SIM-05): same
   timeline + seed → same attack records.
3. **Schema pinning:** the driver refuses a timeline whose schema version it
   doesn't know (mechanical test).
4. **State-gating is real:** a mechanical test shows a substrate event that
   the inherited attacker would take being refused/absent when the timeline
   state doesn't license it (the D7 override, per the scoping note's model);
   `COST_ONLY` states demonstrably touch no network state.
5. The full matrix has run, seeded, with CIs; the two headline statements are
   recorded with numbers.
6. The progress-update draft exists for Marc's review.
7. No file under `mtdnetwork/component/` (network/host/service/MTD) or
   `mtdnetwork/mtdai/` is behaviourally changed — attacker-side additions
   only (D5); `git diff` audit against that boundary.

## Hard constraints

- **Never delete or modify the 6-phase attacker's behaviour** — alongside,
  per-run selection ([`../specs/architecture.md`](../implementation/architecture.md)
  §(f) decision block).
- **Attacker-only change (D5)**; HARM / MTD mechanisms / orchestrator /
  statistics semantics untouched (the stats pipeline may gain a reader for
  the new records, not altered maths for the old ones).
- **Within-substrate comparability only** — report the DES MTTC; no
  cross-paper magnitude claims
  ([`../specs/metrics_semantics.md`](../implementation/metrics_semantics.md) §(d));
  the MTTC event definition of §(a) holds for the baseline unchanged.
- **Envelope-not-actor** phrasing in every reported claim.
- **No IDS/detection**; adaptive/MTD-conditioned behaviour deferred (D10).
- Tay's RL is a benchmark to *run*, never to extend/retrain.
- Determinism (SIM-05); branch hygiene; **never push without an explicit
  ask**; Australian English.

## Reading list

- [`./2026-07-03_l3_binding_scoping.md`](./2026-07-03_l3_binding_scoping.md)
  + its output note and `tactic_action_map.csv` — the contract being
  implemented (read the note in full first).
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  — the SimPy driver machinery to reuse (`_execute_attack_action`, the
  interrupt pattern).
- [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  — the state the driver mutates; what "alongside" has to coexist with.
- [`../../data/ogasp/timeline/timeline_schema.md`](../../data/ogasp/timeline/timeline_schema.md)
  + [`timeline_example.jsonl`](../../data/ogasp/timeline/timeline_example.jsonl) — the
  input contract (`ogasp-timeline/v1`; the driver pins to it).
- [`../../baseline/BASELINE.md`](../../baseline/BASELINE.md) +
  [`../specs/mtdsim_spec.md`](../implementation/mtdsim_spec.md) — the oracle and the
  row-level invariants the new attacker must not violate.

## Out of scope (explicitly)

- Two-way integration (simulator ↔ net each event), capability
  precondition/effect contract, MTD-capability-reset modelling — all deferred
  (D10); documented as the upgrade path in the scoping note.
- Sensitivity analysis over weights/durations beyond the extremes already in
  the timeline library.
- New MTD mechanisms, IDS, detection-rate tuning, RL retraining.
- Sending the progress update (Marc sends; this drafts).
- The L4 write-up/evaluation chapter — this delivers the matrix numbers, not
  the dissertation analysis.
