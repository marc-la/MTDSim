---
status: open
created: 2026-08-09
---

# Axis 1, persistence — context only: what the badge rests on, and why every progression measure built for it is saturated or measuring the wrong object

## What this document is

**Context only.** The approach arrives in the session prompt; Marc brings the
ideas. No recommended approach, no validation gate, nothing commissioned. What it
supplies is what is built, what has been measured, and the bounds already
established — so a proposal lands against the real bar rather than re-deriving a
wall someone already hit.

Siblings, same date and same purpose, one per axis:
[axis 4](2026-08-09_axis4_adaptivity_context.md),
[axis 6](2026-08-09_axis6_incentive_rationality_context.md),
[axis 7](2026-08-09_axis7_learning_context.md).

## 1. This axis is the odd one of the four, and the difference matters

Axes 1, 4, 6 and 7 all sit at DESIGNED, and the criterion records that the badge
vocabulary cannot encode why they differ
([`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
§(b)). **Axis 1 records an *absence*** — a structure that runs, with no outcome ever
shown. Axes 4, 6 and 7 record *measured negatives*: built, swept, ablatable
mechanisms shown to operate without conferring advantage.

The consequence for this axis specifically: **nothing here has been swept and found
wanting.** No mechanism has failed. A positive result may therefore be available
from measurement alone, which is not true of the other three. What has failed is
the measurement — repeatedly, and in two distinct ways worth keeping apart (§3).

## 2. What the badge rests on, and what is built

**The claim.** A 15-tactic-place Petri campaign structure derived from the
analyst-curated Attack Flow corpus, with pre-intrusion structure composed in
synthetically ([`synthetic_overlay.md`](../implementation/pipeline/ogasp/synthetic_overlay.md),
M6). One hundred coupled runs traversed it end-to-end.

**What is not on record** is persistence in **outcome** terms: 0/100 objective
reaches in experiment 1, and effort does not convert to breadth (finding 2). The
structure is real and runs; sustained staged advance is not evidenced, which is why
the badge holds. §(f) of the criterion is explicit that a rubric scoring persistence
"captured" on structural grounds alone would be reverse-fitted.

**Built, in [`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py)
§1.** `distinct_place_curve` / `distinct_place_count`, `deepest_successful_stage`,
`deepest_visited_stage` (kept only as the saturated comparator),
`foothold_retentions`, `successes_per_distinct_host`, `actions_per_distinct_host`,
`first_success_stage`, `advanced_after_first_success`, `blocked_fraction_trend`.

**The M8b field** asks for distinct-tactic coverage over time (the lead
recommendation), foothold-retention duration across MTD mutations, and the
effort-to-breadth conversion ratio.

## 3. The bounds already established — read before proposing a measure

**Two depth measures, both saturated, for two different reasons.**

- **Kill-chain depth is withdrawn as saturated.** Every profile traverses to the
  objective stage of its own campaign structure. `deepest_visited_stage` reads
  **3.0 ± 0.0 for all five profiles under both mappings**, with zero adjacent pairs
  separating — the criterion's §(h) finding, reproduced by the suite itself.
- **Its replacement is also saturated under the go-forward mapping, and the cause
  is structural rather than power.** `deepest_successful_stage` returns the same
  value for **all 800** movement runs of experiment 2. Seven tactics are dwell-only
  under `v2_partial`, including the objective band, so a stage-3 place can dispatch
  no verb and hold no success verdict: the measure's ceiling drops to 2, four
  profiles sit at exactly 2.0 ± 0.0
  ([`measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  §(c)). Under `v1_ckc_total` it *does* discriminate — one adjacent pair CI-disjoint
  — so the saturation is mapping-induced, not intrinsic.

**Foothold retention counts the wrong thing, twice over.**

- It counts footholds **severed** rather than retained.
- The two application-layer mechanisms interrupt often and **sever position never**,
  so retention under them is total by the absence of any threat to it. Against the
  defences that actually contest position, per-foothold retention at the operating
  interval is **0.0–1.6 %**.

**Records carry no host identity.** `foothold_retentions` therefore measures
retention of *position*, not of a named host. `n_compromised` — the one integer
`MovementRecord` gained for the disengagement measure, asserted monotone and
duplicate-free — **does not close this**: a monotone count gives a trajectory and
cannot name a foothold. The suite's standing rule is that a schema widening carries
the burden of proof and is discharged by measurement, as `n_compromised` was (837
compromise events against 155 distinct hosts, and the over-count itself
MTD-dependent at 5.4–8.8 without against 1.8–3.5 with).

**Experiment 2 reported this axis moving to DEMONSTRATED and the move was
withdrawn** on cross-examination, on the first two grounds above. The criterion
records the near-miss deliberately, as the pre-registration discipline doing the
only job it exists to do.

## 4. What survives, and what leads by default

`distinct_place_curve` is the one measure the suite says still discriminates in
exactly the band the depth measure cannot see, and the criterion has it leading the
M8b field. **It leads by default rather than by demonstration** — it has not been
shown to separate profiles or defence conditions on a pre-registered bar.

`actions_per_distinct_host` formalises experiment 1's finding 2 and does
discriminate: cell totals put the baseline at ~36 attempted actions per distinct
host against `objective_none_c2` at ~314 attempted (~277 successful), an
order-of-magnitude gap that survived the re-baseline. Its per-run form is undefined
at zero hosts, and the infinite ratio is itself the finding for
`objective_exfiltration`, which converts its whole budget into zero hosts.

## 5. Constraints that bind any proposal here

- **The degenerate region.** At 200 s neither attacker completes the objective, so
  success-rate-shaped measures are pinned at zero. Evidence must be breadth- or
  time-shaped, or come from outside the region and say so.
- **Mapping-induced censoring is now a known failure mode on this axis
  specifically.** Any progression measure must be checked under both mappings
  before adoption; adopting a second saturated measure unchecked is exactly what
  §(h) records happening once already.
- **Ten seeds separate almost nothing.** `interval_report`; `ordering_supported`
  is the gate, never the sorted means.
- **Reader versus mechanism.** A reader changes nothing and moves no badge — axis 5
  declined the move three times on that ground. Prefer extending the reader over
  widening the record; the confusion-penalty derivation shows a gap can close
  without a schema change.
- **Scores move on evidence only** — never change the model, weights, mapping or
  metrics to improve a row (S6;
  [`../workflows/guardrails.md`](../workflows/guardrails.md)).
- Determinism (SIM-05); envelope-not-actor; Australian English; branch per session;
  commit locally; **never push** without an explicit ask.

## Reading list

- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(d) axis 1, §(f) (held at DESIGNED by experiment 1), §(f2) (the withdrawn move),
  §(h) (the saturation finding).
- [`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  §(b) rows for the axis-1 measures, §(c) gate 3's split verdict, §(f) what
  consumers must respect.
- [`../implementation/pipeline/ogasp/experiment_01_findings.md`](../implementation/pipeline/ogasp/experiment_01_findings.md)
  finding 2 — effort does not convert to breadth.
- [`../implementation/pipeline/ogasp/attacker_disengagement.md`](../implementation/pipeline/ogasp/attacker_disengagement.md)
  §1.1 — `n_compromised`, and the measured case that justified the one widening.

## Out of scope for this document

It commissions nothing, sets no gate, recommends no build and expresses no
preference. The approach arrives in the prompt.

## Return format

Default ([`../workflows/session_workflow.md`](../workflows/session_workflow.md#handoff-workflow)):
framed in terms of the thesis and succinct — which claim moves, which criterion row
is affected, what is now sayable. A null or inverted result reports the same way.
