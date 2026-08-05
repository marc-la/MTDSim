---
status: open
created: 2026-08-05
---

# A metric per axis — make the eight APT characteristics measurable, so the criterion is scored by evidence rather than by argument

**The gap this closes, stated once.** The APT criterion
([`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md))
scores this attacker model on eight literature-derived axes, and every axis
carries an **M8b field** naming the measurement that would move its badge. Those
fields were written as recommendations and most were never built. The criterion's
own §(f) says it plainly: *"the measurement suite can currently score axes it
holds no claim on, and cannot score the axes the model claims."*

So the model's headline — *what this attacker captures about APT behaviour that
prior models do not* — currently rests on argument at four of eight axes. This
brief builds the instruments that let it rest on measurement.

**Scope discipline: readers, not mechanisms.** Every item below is a pure
function over records that already exist, in the shape
[`measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
established — no attacker capability is added, no golden moves, no S2 freeze
question arises, and existing recorded runs can be re-read without re-simulating.
Where an axis *cannot* be scored without a mechanism, this brief says so and
stops rather than smuggling one in.

## 1. What already exists, so nothing is rebuilt

Check these before writing a line — three of the eight axes are partly served:

- [`measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  — the reader module, the baseline-arm row adapter, `interval_report`, the
  cost ledger, the disruption ledger, the coverage curve and
  deepest-successfully-actioned-stage (axis 1's partial).
- [`2026-08-01_attacker_disengagement_measure.md`](2026-08-01_attacker_disengagement_measure.md)
  — **axis 6's metric**, designed in full. Do not duplicate it here; this brief
  consumes it.
- [`2026-08-04_stealth_exposure_metric_reader.md`](2026-08-04_stealth_exposure_metric_reader.md)
  — **axis 5's metric**, designed in full. Same: consume, do not duplicate.

This brief therefore owns axes **1, 2, 3, 4, 7, 8** and the two lettered rows,
and its first job is to state for each whether the M8b recommendation still
stands as written.

## 2. The per-axis work list

Each row: what the criterion's M8b field asks for, what state it is in, and the
smallest reader that would discharge it.

| Axis | Badge | What M8b asks for | State | The reader |
|---|---|---|---|---|
| **1** Persistence | DESIGNED | distinct-tactic coverage over time; foothold-retention duration across mutations; effort-to-breadth conversion | **partly built** — coverage curve and effort-to-breadth exist; the originally-recommended kill-chain depth is **withdrawn as saturated**; foothold retention is blocked on a known blind spot | `foothold_retention` — needs `MovementRecord` to carry **host identity**, which it does not (the same blind spot the disengagement brief's §2.3 must settle). Settle it once, here, for both |
| **2** Objective conditioning | DEMONSTRATED | per-profile behavioural divergence: JSD between profiles' action streams and terminal-tactic distributions at L3 | **not built** — the L2 corpus-level JSD check exists; its execution-level mirror does not | `action_stream_jsd(profile_a, profile_b)` over the recorded action streams. Mirrors `gasp_schema.md` §(g)'s method one layer down, so the method is already defended |
| **3** Strategic plurality | DEMONSTRATED | plurality that is *chosen* rather than drawn | **built** — pooled path entropy and distinct opening sequences are reported | None needed. **Record that the badge's evidence is the modulators-null arm**, and that any modulator-active arm must report its own entropy figure |
| **4** Adaptivity | DESIGNED | action-mix change before vs after an MTD trigger; recovery time from an MTD-induced throw-back; weight-set switch frequency vs progress | **not built** — and this is the largest genuine gap on the list | `pre_post_mtd_action_mix` (JSD across the trigger boundary), `recovery_time_to_first_success`, `weight_set_switch_rate`. All three are windowed reads over the existing record stream plus the MTD execution log |
| **7** Learning | DESIGNED | a credit signal carrying **progress** rather than the routing verdict, shown to raise breadth or stage advance against its own ablation arm | **requirement isolated, not dischargeable by a reader** — the representation half is discharged; what remains is a *mechanism* redesign | **Stop here.** State plainly that axis 7 cannot be moved by measurement, and that the credit-assignment redesign is out of this brief's scope. A reader that re-reports the existing friction measures would be measurement theatre — and the readiness study already warns that friction-shaped measures **cannot discriminate between representations** |
| **8** Scheme awareness | NOT ADDRESSED → under review | per primitive: repeat-compromise rate on previously-seen configurations vs unseen; correlation between target selection and mutation frequency; any invariant-feature channel | **now live** — the exclusion is under reversal for a proof of concept ([`2026-08-04_vulnerability_memory_and_swift_mode.md`](2026-08-04_vulnerability_memory_and_swift_mode.md)) | `repeat_configuration_compromise_rate` — the primitive-(i) measure, and the natural acceptance test for that PoC. **Build the reader first**, before the mechanism: it is what tells you whether configurations *ever* repeat on this substrate, which decides whether the PoC has anything to find |
| **Row A** provenance | scored | aggregation over tier badges | **built** (by aggregation, §(d2)) | None — re-run the aggregation if a declared family is added |
| **Row B** consequence | RECOMMENDATION | comparative run, both attackers, same substrate | **built** | None. Note the standing caveats: ten seeds supports a rank comparison and not a significance test, and — new — seed-matched arms are **independent, not paired** (D-29), so that caveat is understated |

## 3. Two cross-cutting constraints that shape every reader

**The degenerate region.** At the 200 s operating interval neither attacker
completes the objective, so any success-rate-shaped measure is pinned at zero and
cannot discriminate
([`rate_feasibility_study.md`](../implementation/pipeline/ogasp/rate_feasibility_study.md)
§7, C5). Every reader here must be **breadth- or time-shaped**, or state that its
evidence comes from outside the region. This is why axis 4's three measures are
windowed rather than outcome-based.

**Cross-arm comparability.** Under S3-R the movement layer prices its own time
while the baseline runs on substrate pricing, so `EventWiseComparable` carries no
time field by construction. Any measure intended to compare the profiled attacker
against the inherited one must be **effort-denominated (actions)**, not
time-denominated; time views are arm-local and labelled as such.

## 4. The one instrumentation decision to settle first

**`MovementRecord` carries no host identity.** Axis 1's foothold-retention
measure needs it, the disengagement measure's progress trajectory needs it
(§2.3 there), and the axis-8 repeat-configuration reader needs something like it.
Three consumers is the justification a schema widening requires, and the suite's
standing rule is to prefer extending the reader over widening the record — so
this needs deciding once, deliberately, rather than three times by three
sessions.

Settle it **before** building any reader that depends on it. The cheap check
first: over existing recorded runs, compare compromise *events* against
`compromised_count`; report the ratio either way. Then put the widening to Marc
with its three consumers named.

*(Note the adjacent widening the disruption brief also needs — the interrupting
mechanism's name. If both are taken, take them in one schema change and one
re-capture.)*

## 5. Pre-registered conclusions — per reader, committed before any output

House discipline, and it applies to readers as much as to sweeps. Every aggregate
goes through `interval_report`; `ordering_supported` is the gate. For each reader
built, commit before running:

- **Non-degeneracy** — the measure varies across profiles (or across the defence
  family) by more than its own dispersion. A flat measure carries no information
  and should be reported as such, not tuned until it moves.
- **Non-redundancy** — Spearman correlation against the quantity it is meant to
  add to (usually distinct hosts) is **below 0.9**. At or above, it is a monotone
  re-expression of something already reported. This is the criterion the
  disengagement brief's C5 already imposes on itself; use it verbatim so verdicts
  are comparable.
- **Direction committed in advance**, including where the expected direction would
  embarrass the model.

**A measure that fails its own non-degeneracy or non-redundancy bar is a result,
not a failed build.** Report it and move on — the criterion's value depends on
its measures discriminating, and one that does not is worth knowing about.

## 6. Build order

1. Settle §4's `MovementRecord` question (cheap check, then Marc's ruling).
2. Axis 2's JSD reader — smallest, self-contained, mirrors an already-defended
   method, and moves a DEMONSTRATED badge from argument to measurement.
3. Axis 4's three windowed readers — the largest genuine gap, and the axis where
   "reacts" versus "adapts usefully" is currently unfalsifiable.
4. Axis 1's foothold retention, once §4 is settled.
5. Axis 8's repeat-configuration reader — **before** the PoC mechanism it serves.
6. Record as `docs/implementation/pipeline/ogasp/axis_metrics.md`; bump
   `measurement_suite.md` §(g); update each axis's M8b field to say *built* and
   what it returned; move a badge **only** where a pre-registered criterion was
   met.

## 7. Validation gates

1. Unit gate: hand-built record streams with hand-worked expected values, beside
   the existing readers in `tests/l3_simulation/test_movement_measures.py`.
2. Reader gate: full `tests/l3_simulation` + substrate/carve/golden suites pass
   **unchanged**. A moved golden means a mechanism was built.
3. Cross-arm gate: computes field-for-field on one seeded run of each arm, with
   no time-denominated field in the comparable subset.
4. Determinism: re-derivation from re-created runs is exact.

## 8. Hard constraints

- **Readers only.** No attacker capability, no mechanism, no declared magnitude
  that changes behaviour. Axis 7 is the test of this rule: it cannot be moved by
  measurement, and the brief must say so rather than building a proxy.
- **No badge moves without a pre-registered criterion** met on the evidence.
- **No measure re-specified after it fails to discriminate.**
- Breadth-/time-shaped inside the degenerate region; effort-denominated
  cross-arm; censoring reported separately, never pooled.
- Determinism (SIM-05); envelope-not-actor; within-substrate comparability only;
  Australian English; branch per session; never push.

## 9. Reading list

- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  — the eight axes, their badges, and every M8b field this brief discharges.
  §(b)'s degenerate-region constraint and its non-additive-census warning.
- [`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  — the reader contract, the blind-spot discipline, the cross-arm enforcement.
- [`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)
  — the per-axis mechanism/measurement/governance split this brief works the
  *measurement* column of.
- [`../implementation/pipeline/gasp/gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md)
  §(g) — the corpus-level JSD check axis 2's reader mirrors.
- [`../implementation/pipeline/ogasp/learning_readiness_findings.md`](../implementation/pipeline/ogasp/learning_readiness_findings.md)
  — why axis 7 resists measurement, and the warning that friction-shaped
  measures cannot discriminate between representations.

## 10. Out of scope

- **Any mechanism.** Axis 7's credit-signal redesign, axis 8's PoC, axis 5's
  dwell-scaling state and axis 6's decision rule are all mechanisms and all
  tracked elsewhere.
- Axis 5 and axis 6's readers — designed in their own handoffs; consumed here,
  not duplicated.
- Re-running recorded experiments. Re-read them.
- Dissertation prose.
