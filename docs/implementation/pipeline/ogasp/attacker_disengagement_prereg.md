---
status: durable
created: 2026-08-02
topic: "The attacker-disengagement measure's pre-registration — five conclusions with criteria fixed, a kill criterion on attributability, one degeneracy predicted in advance rather than discovered, and the reporting shape (a frontier over patience) fixed before any output existed"
---

# Attacker disengagement — conclusions committed before the numbers

**Status:** durable pre-registration. **Written and committed before the measure
produced a single reported row**; the git history is the audit trail. The
analysis computes a held/moved verdict per conclusion from the rows rather than
asserting one, every aggregate goes through `interval_report` with
`ordering_supported` as the gate, and censored runs are reported separately from
observed ones throughout.

**What this measures, and why it exists.** Every attacker-side metric in this
lineage is conditioned on the attacker *continuing*: attack success rate, mean
time to compromise and host compromise ratio each ask how well an attack that
persists to the horizon performed. Abandonment is the outcome MTD's economic
argument is actually about — raise the attacker's cost until this network is no
longer worth the effort — and the suite could represent none of it. This is the
measurement that replaces axis 6's mechanism work, which closed as DESIGNED
([`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 6, final
disposition).

**It is a reader and it stays one.** It reports when a run *would have*
disengaged; it never stops one. An attacker that actually stopped would make
"MTD causes disengagement" definitional — cost rises, the threshold trips, the
run ends — and no null arm could falsify it. The per-run reporting unit is a
snapshot (*the attacker would have given up at X*) and the run continues.

## 1. The quantity

At each attempted action `t`:

```
    T(t) = t + (W − h(t)) / r(t) ,     r(t) = (h(t) + α) / (t + α / r₀)
```

`t` is effort in **attempted actions**; `h(t)` is progress in **distinct hosts
compromised**, read from `MovementRecord.n_compromised`; `W` is the total work
the objective requires. Abandonment at budget `B` is the **first** `t` where
`T(t) > B`; a run whose projection never crosses is **censored** at that budget,
not "did not abandon".

**Effort is denominated in actions, never seconds, and that is forced rather than
preferred.** Under S3-R the movement layer prices all of its own time while the
baseline runs on substrate pricing, so `EventWiseComparable` carries no time
field by construction. A time-denominated abandonment would be arm-local and
could not be compared to the inherited attacker.

## 2. The values — one derived, two declared, one swept

| | value | status | tier | band |
|---|---|---|---|---|
| `W` work total | **40.0** = `terminate_compromise_ratio` 0.8 × `total_nodes` 50 | **derived** from the substrate's own termination condition | — | — |
| `r₀` prior rate | **0.02778** = 39.2 hosts ÷ 1 411 actions | **measured within-substrate**: the unimpeded inherited attacker's realised rate | attested-pattern (behaviour) / declared-magnitude (number) | ×½ and ×2 |
| `α` prior strength | **1.0** (one pseudo-host) | declared | declared-judgement | [0.5, 5.0] |
| `B` budget | **not declared** | swept as the reporting axis | — | `k × U`, `k ∈ [1, 10]` |

`U` is **derived, not declared**: `U = W / r₀ = 1 440` attempted actions, the
effort an unimpeded attacker at its measured rate would need to reach the
objective. The budget is expressed as a multiple `k` of it so the reporting axis
is in units of *unimpeded campaigns*.

**The prior is anchored within-substrate and never to real-world figures.** The
duration catalogue is explicitly shape-not-scale, so simulated units carry no
calibrated mapping to real campaign durations, and anchoring patience to
breach-report hours would import exactly the cross-scale comparison the project
forbids.

### 2.1 One degeneracy is predicted here rather than discovered later

At `t = 1` with `h = 0`, the rate is `α / (1 + α/r₀)` and the projection is
`T(1) = 1 + W·(1 + α/r₀)/α = 1 + U + α/r₀·…` — arithmetically `T(1) = 1 + U`
to within a rounding of the prior. **So `k = 1` must abandon at action 1 in every
run of every arm, by construction**, because the budget is `U` and the projection
starts one action above it.

This is stated in advance so it reads as a property of the parameterisation
rather than as a finding. The informative band therefore begins just above
`k = 1`, and the swept points are `k ∈ {1, 1.25, 1.5, 2, 3, 5, 7.5, 10}` — `k = 1`
retained deliberately as the degenerate anchor that shows the prediction holds.

## 3. The matrix

Re-read over recorded runs wherever possible: `T(t)` is a trajectory and every
budget is a threshold read off it, so **one run yields the entire budget family**
and a frontier over patience costs no additional simulation. Fresh runs only for
cells the recorded corpus cannot cover.

Five profiles × both MTD conditions × the defence family at the 200 s operating
interval × 10 seeds on `v2_partial`, plus the inherited baseline arm. The
baseline is where the measure must demonstrate **validity** rather than answer
the research question: that arm actually progresses, and MTD cuts it from 39.2 to
13.1 distinct hosts, a threefold rate reduction abandonment effort ought to
register. **If it does not register there, the measure is broken, not the
finding.**

## 4. The conclusions

| | Conclusion | Criterion |
|---|---|---|
| **C1** | The measure is non-degenerate | mean abandonment effort varies across the `k` band by more than its own 95 % interval width, on ≥ 3 of 5 profiles. A flat curve means the budget axis carries no information and the measure is useless whatever else holds |
| **C2** | **THE KILL CRITERION — the defence is attributable** | at ≥ 1 budget level, mean abandonment effort under ≥ 1 MTD mechanism is CI-disjoint from the no-MTD arm, on ≥ 3 of 5 profiles. **If C2 moves, stop and report** |
| **C3** | Mechanisms differ from one another | the ranking of mechanisms by mean abandonment effort is not uniform — ≥ 1 adjacent pair separates at the operating interval. Otherwise the measure only reads MTD on/off, which host-compromise count already does |
| **C4** | **The payoff — it discriminates where ASR cannot** | at the 200 s operating interval, inside the degenerate region where ASR is pinned at 0.00 for every arm, abandonment effort separates ≥ 1 adjacent pair of conditions |
| **C5** | **Committed in the direction that would embarrass it** — the measure is not a restatement of breadth | Spearman correlation between mean abandonment effort and mean distinct hosts, across all cells, is **below 0.9**. At or above 0.9 the measure is a monotone re-expression of a quantity already reported, and adds nothing — say so plainly rather than shipping it |

**C2 moving is a result, not a failed study.** If disengagement on this substrate
is driven by procedural friction rather than by the defence, that is the same
family of finding as the axis-6 negative and the learning study's credit-signal
result. **Do not** respond to a moved C2 by re-specifying the measure until it
separates — that is the scoring-driven design the criterion's standing constraint
forbids.

**C5 is the one to watch.** The measure's progress term is distinct hosts, and
breadth is distinct hosts at the horizon. That the two are related is not a
defect; that the measure might be a monotone re-expression of breadth *is*, and
C5 is set to catch it. Note the correlation is expected to be substantial and
negative in sign (more breadth, later abandonment); the criterion is on
magnitude.

## 5. Reporting shape — a frontier over patience, never a chosen threshold

Zhang never stated a threshold value, so none can be declared honestly. For each
defence condition, report **mean abandonment effort as a function of `k`**, with
its 95 % interval and its censoring fraction at every point. The reader picks
their own reservation and reads off the answer; no declared value is
load-bearing.

**Censoring is data, not a nuisance.** At low `k` almost every run abandons; at
high `k` most censor. Observed and censored are reported separately, never pooled
into one mean — a pooled mean understates every censored run, and the censoring
fraction itself varies along the curve.

## 6. Gates, discharged before any reported output

1. **Unit gate** — hand-built record streams with hand-worked expected values:
   steady progress lowers the projection, a stall raises it monotonically, no
   progress rises from the prior alone, a run that crosses and recovers reports
   the **first** crossing, a run that never crosses returns `None` rather than a
   sentinel. In `tests/l3_simulation/test_movement_measures.py`.
2. **Instrumentation gate** — settled and **failed as originally specified**,
   which is why the record schema moved. Cumulative compromise events over-count
   distinct hosts by a measured **5.40×**, and the over-count is MTD-dependent
   (5.4–8.8 without MTD against 1.8–3.5 with it), so events would have biased the
   very comparison C2 tests. `MovementRecord.n_compromised` replaces the proxy
   with the substrate's own count, asserted monotone, duplicate-free and equal to
   `compromised_count` at the horizon.
3. **Reader gate** — the full suite passes and **no golden moves**: the
   observation field is popped from the golden serialisation exactly as `retrace`
   is, on the builder's own principle that only behaviour may move a digest.
4. **Determinism** — the measure draws from no stream; re-derivation from
   re-created runs is exact.

## 7. What this study will not license

- **No badge move.** This is a measurement. Axis 6 is closed as DESIGNED and this
  reader scores an *outcome*, where that axis asks whether the attacker
  *conditions on* cost. Say so plainly in the record.
- **No attacker that stops.** The decision rule that consumes this measure is a
  separate build, gated on this one discriminating.
- **No composite score** trading attacker disengagement against defender
  disruption. The frontier is the deliverable.
- **No cross-arm time comparison.** Effort-denominated primary; any
  time-denominated view is arm-local and labelled as such.
