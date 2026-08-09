---
status: open
created: 2026-08-09
---

# What the reactive defender spends its budget on — the mechanism-selection finding, and the blocker in front of it

**Split out of `2026-08-07_axis8_defender_metric_reasoning.md`
on 2026-08-09, which is deleted.** That brief's own question — an attacker that
manoeuvres the defender's metrics into suppressing mutation — is **closed on
evidence** and recorded in
[`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
axis 8, amendment 2026-08-09. What survives it is not an attacker mechanism. It
is a defender-side observation the λ ladder produced in passing, and one
substrate defect standing in front of any study of it.

**Nothing here needs a new attacker capability, and nothing here is axis 8.**

---

## 1. The finding, and why it is worth a study

From [`../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md`](../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md)
§3, recorded there as *"the one worth carrying into the discussion"*:

The **λ = 0 agent — the one whose reward is Tay's, unmodified** — deploys at the
maximum available rate and fires **IPShuffle on 100 % of 367 mutations across all
three seeds**. IPShuffle is the single mechanism this project has separately
verified changes *nothing in the attacker's readable projection*
([`../implementation/attacker_read_surface.md`](../implementation/attacker_read_surface.md)
§(f) finding 1: *"DEAD to the attacker — and that is documented behaviour"*). It
compromises 9.27 hosts. The λ = 400 agent barely deploys at all and compromises
9.67.

Stated as the claim it *might* support: **maximal movement into the attacker's
blind spot buys approximately what not moving buys.** If that survives a powered
test it speaks directly to the RQ — it is a statement about how an existing MTD
mechanism performs, which is what the thesis asks — and it bears on what
"minimising unnecessary MTD deployments" could ever have meant in the source
work.

⚠ **It is currently a shape, not a result, and must not be written as one.**
C5 was pre-registered as a negative control and **does not separate**: three
seeds, per-episode standard deviation of 2.3–3.8 hosts, and per-seed means at
fixed λ swinging further than the ladder does (9.6 / 3.4 / 8.2 at λ = 25). The
calibration record says so in terms and the wording should not drift.

**The distinction the study must hold.** IPShuffle is dead to the attacker's
*readable* projection; it is **not** inert. It still interrupts, and an interrupt
costs the attacker time and its host cursor. So the claim is about *information*
— the mutation invalidates nothing the attacker knows — and never about
disruption. Conflating the two would be the easiest way to get this wrong.

---

## 2. ⚠ The blocker — measured, unrepaired, and needing Marc's disposition

**Any study pairing the movement attacker with `mtd_ai` is blocked until this is
dispositioned.** Two profiles in three crash the run outright with
`ZeroDivisionError` on `attack_success_rate = compromised_num / attack_event_num`
(`mtdnetwork/operation/mtd_ai_operation.py` ~line 448).

Measured trigger, at the **first decision** (t = 200.1 s):

| | value at crash |
|---|---|
| record rows | 1 |
| `compromised_num` (60 s window) | 0 |
| `attempt_hosts` | **0** |
| verbs in record | `{SCAN_HOST: 1}` |

**The cause is not a tactic mix light on `SCAN_PORT`**, which is what was
originally predicted. It is `attempt_hosts == 0`: the walk has run only
*host-independent* recon (`SCAN_HOST` writes `current_host_uuid = -1`), so the
denominator never accumulates. Any profile whose opening stretch is
host-independent trips it. The inherited attacker escapes only because its phase
order reaches a host-scoped verb before the first decision epoch.

**This is flaky rather than categorical — which is the worse failure mode.** One
profile in three survived, so a sweep could be run and reported without anyone
noticing which arms never completed a run.

**Not repaired**, per the originating brief's constraint: it is a substrate
change and needs its own disposition against
[`../implementation/mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md)
before anyone calls it a bug. Note it is reachable on the *inherited* arm too in
principle — the guard is absent, not merely unlucky.

---

## 3. What already exists, and does not need rebuilding

Committed on `feat/mtd-ai-cost-calibrated`:

- `run_movement(..., mtd_scheme="mtd_ai", mtd_ai=MTDAIConfig(main_network=...))`
  — the movement attacker against the reactive defender, defaulting to a
  strictly greedy policy.
- `mtd_action_space()` / `CANONICAL_FEATURES` in `mtdnetwork/mtdai/mtd_ai.py` —
  one owner for the action space and the state head, so no run can re-point an
  action index at a mechanism the agent was not trained to deploy.
- `MovementRunResult.mtd_decisions` and `decision_summary()` — the per-decision
  ledger with the **greedy share separated from the pooled one**, which matters
  because a pooled no-op share is floored by the exploration rate and would
  report the schedule rather than the policy.
- `tests/l3_simulation/test_movement_mtd_ai_wiring.py` — 8 tests, no TensorFlow.

---

## 4. Recommended approach

1. **Disposition the §2 divide-by-zero.** Nothing below is runnable at profile
   coverage until then.
2. **Power the comparison properly.** C5's spread says three seeds cannot carry
   it. Size the seed budget off the measured per-episode standard deviation
   (2.3–3.8 hosts) before running, not after.
3. **Report mechanism mix as the primary outcome**, with the **forced share
   separated** — at the top of the ladder the guard draws uniformly over the four
   mechanisms by construction, so a pooled mix there is the timer's coin and not
   a preference. This is the same trap C3 fell into and was recorded as *not
   interpretable* because of.
4. **Pair it with the two instruments the scaled-training brief already owes** —
   greedy-policy entropy (MTDAI-16) and the static-degrade sweep (MTDAI-17)
   ([`2026-08-08_mtd_ai_scaled_training_proposal.md`](2026-08-08_mtd_ai_scaled_training_proposal.md)
   gates 6 and 7). A constant-action policy pinning one mechanism *is* the
   entropy finding seen from the other side; measuring both together costs
   almost nothing extra and each corroborates the other.

---

## 5. Validation gate

- The divide-by-zero carries a written disposition before any run.
- The seed budget is derived from the measured spread and stated before the run.
- Mechanism mix is reported with the forced share separated out, never pooled.
- Any "movement buys nothing" claim is stated against the **information** channel
  (readable projection) and explicitly not against disruption.
- If the comparison still does not separate, that is a reportable null and is
  written up as one — it bounds what the reactive arm can evidence.

---

## 6. Hard constraints

- **`replicate, never extend`.** No new defender, no new mechanism, no retuning
  of `MTD_DURATION` (provenance-badged faithful against Zhang 2023 Table 3).
- **No published Tay figure as a comparator** — those characterise a uniform
  random selector; the project's own random-scheme arm is the comparator.
- **Bounded to the reactive case.** Time-triggered MTD is unaffected by attacker
  tempo and nothing here generalises to the rest of the pool.
- Determinism (SIM-05); arms at a common seed are **independent, not paired**
  (D-29, and the calibration record's §2 gate); within-substrate comparability
  only; Australian English; branch per session; never push without asking.

---

## 7. Out of scope

- **Any axis-8 attacker mechanism.** Closed — see the criterion amendment.
- Building an event-triggered defender. Declined against two recorded decisions
  in [`../implementation/architecture.md`](../implementation/architecture.md)
  (defence side is existing mechanisms only, Jin 19 Mar 2026; IDS is not a
  research thread), and circular by construction besides.
- Repairing any other `get_state_and_time_series` quirk.
- Running the scaled training — that is its own brief.
- Dissertation prose.

---

## 8. Reading list

- [`../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md`](../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md)
  §3 — the ladder, C3's and C5's non-interpretability, and the finding in §1.
- [`../implementation/attacker_read_surface.md`](../implementation/attacker_read_surface.md)
  §(f) finding 1 — the IPShuffle claim this rests on, and its exact scope.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  axis 8, amendment 2026-08-09 — why the attacker half is closed, and the
  overclaim to avoid.
- [`2026-08-08_mtd_ai_scaled_training_proposal.md`](2026-08-08_mtd_ai_scaled_training_proposal.md)
  gates 6–7 — the two instruments this shares.
