---
status: durable — the study it pre-registered ran and its direction is closed (see iterated_cost_model.md §0)
created: 2026-08-02
updated: 2026-08-02
topic: "The iterated cost model's pre-registration — the five conclusions, their criteria, and the sweep matrix, all fixed before a single row existed. The repair is motivated by a defect, which makes the temptation to show it working the sharpest this project has faced; this record is the guard against it"
---

# The iterated cost model — conclusions committed before the numbers

**Status:** durable pre-registration. **Written and committed before the sweep
ran**; the git history is the audit trail, and the runner
(`data/results/iterated_cost/run_sweep.py`) carries the same conclusions and
criteria in its docstring. The analysis computes a held/moved verdict per
conclusion from the rows rather than asserting one, and every aggregate goes
through `interval_report` with `ordering_supported` as the gate.

**Why the discipline matters more here than anywhere else it has been applied.**
Every prior pre-registration in this project guarded against a *flattering*
result. This one guards against something sharper: the change is motivated by a
**defect that has already been recorded and published in three documents**
([`cost_model_plain.md`](cost_model_plain.md) §2.2a,
[`incentive_rationality.md`](incentive_rationality.md) §6.2 and §8,
[`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 6), and a
repair that fails to repair it would embarrass the diagnosis as well as the
build. That is precisely the circumstance in which criteria drift after the fact.
So the criteria are fixed here, two of the five are committed in the direction
that would embarrass the repair, and **U2's failure is a stopping condition
rather than a licence to re-specify**.

## 1. What is being tested

The mechanism is
[`utility_iterated.py`](../../../../src/mtdsim/l3_simulation/movement/utility_iterated.py),
registered as factor 7 in
[`modulator_composition.md`](modulator_composition.md). Two changes, each
computed from artefacts already on disk, neither adding a declared family:

- **Change A — expected cost.** `cost*(b | s) = duration(b) + enabling_cost(verb(b), s)`,
  where `enabling_cost` is the cheapest ordered verb sequence taking the
  attacker's held capabilities to a set satisfying `verb(b)`'s requirement,
  priced from the declared duration catalogue through the run's controller
  mapping. A shortest-path search over the declared precondition relation's
  eight-state capability closure — a search rather than a sum, because
  `ENUM_HOST` *clears* `curr_ports` while producing `curr_host`, so the relation
  has ordering effects an unordered set of missing prerequisites cannot express.
- **Change B — enabling value.** The benefit numerator's stage-gap distance is
  measured through the profile's own routing net instead of the lifecycle-stage
  ordering: `1.0` at an objective, `rho^(1 + hops)` elsewhere, and the shipped
  stage-gap value where the net affords no directed path.

**The declared parameters are untouched.** ρ, `cost_floor_s` and λ keep their
values and their swept bands; what changes is what they are applied to. That is
the brief's central claim and it is enforced as a test, not an intention (§4).

## 2. The four arms, and why three of them exist

The change is two changes, so a two-arm study could not attribute an effect to
either. Four arms:

| arm | cost term | benefit term | stateful |
|---|---|---|---|
| `declared` | declared duration | stage gap | no |
| `A` | **expected cost** | stage gap | yes |
| `B` | declared duration | **net hops** | no |
| `AB` | **expected cost** | **net hops** | yes |

`declared` reproduces the shipped modulator's factors exactly — asserted in the
test suite over every place of every profile's net under both mappings — so the
comparison baseline is the model every recorded figure in this project was
produced by, not a re-implementation of it.

## 3. The matrix

**Main sweep.** λ ∈ {0, 0.5, 1, 2, 4} × 4 arms × 5 profiles × 2 mappings
(`v1_ckc_total`, `v2_partial`) × 2 MTD conditions (none, `random` multi) × 10
seeds, at the 15 000 s horizon and the 200 s operating mutation interval. λ = 0
returns no non-unit factor under **any** arm, so it is run once as a shared
ablation arm rather than four times; the per-arm λ = 0 identity is asserted
exhaustively as a *test* over the full configuration grid instead (U1), which is
a stronger check than a sampled run would be. **3 400 runs.**

**The layer sub-study (U3b).** λ ∈ {0, 1} × {`declared`, `A`, `AB`} × 4
single-mechanism conditions × 5 profiles × 10 seeds on `v2_partial`, the mapping
experiment 2's defence-family study used. The four mechanisms are the two
**position-destroying** (Complete Topology Shuffle, IP Shuffle) and the two
**diversity** (OS Diversity, Service Diversity) members of the active pool.
**800 runs.**

Total **4 200 runs**, on the current substrate. Freshness checked before
running: no commit has touched the substrate since `816b300`, so these rows and
the 2026-08-01 re-verification describe the same simulator.

**Two limits stated in advance.** The study is **not powered** for any ranking of
MTD mechanisms under a cost-sensitive attacker — that is experiment 2's, and the
sub-study's four conditions exist to separate two *families*, never to order four
mechanisms. And **no conclusion rests on ASR**, which discriminates nothing at
the 200 s operating interval per the rate feasibility study's degenerate-region
finding.

## 4. The conclusions

| | Conclusion | Criterion |
|---|---|---|
| **U1** | The ablation is still exact | at λ = 0 the record stream is field-for-field identical to a run with no modulator, across profiles × seeds × mappings × MTD conditions, **for every arm**; zero differing runs. **A hard constraint, not a finding** |
| **U2** | The repair reaches the wall | blocked fraction at the declared λ is **lower** under the iterated model than under the `declared` arm, with disjoint 95 % intervals, on ≥ 3 of 5 profiles. This is the defect's own signature and the minimum the change must show |
| **U3** | **The payoff — MTD's measured effect now changes with cost-sensitivity** | the action-mix JSD between λ = 0 and λ = 1 is larger under MTD than without it, on ≥ 3 of 5 profiles — C4's criterion verbatim, so the verdicts are comparable. If U3 holds, axis 6's DEMONSTRATED condition is met by mechanism rather than by operating point |
| **U3b** | The response is layer-specific, as the mechanism predicts | U3's quantity is **larger under the position-destroying family than under the diversity family**, on ≥ 3 of 5 profiles. `mtd_clears` says the cost term can only see network-layer mutations, so a uniform response across families would mean the effect is not coming from the mechanism claimed. **Reported whichever way it falls** |
| **U4** | **Committed in the direction that would embarrass it** — the repair is not bought with plurality | pooled path entropy at the declared λ under the iterated model is **not lower** than under the `declared` arm. A repair that buys progress by collapsing traversal further has traded against axis 3 and must say so |
| **U5** | **Committed in the direction that would embarrass it** — the attacker is not simply better | distinct hosts at the declared λ are reported against **both** the `declared` arm and the λ = 0 arm. A rise over λ = 0 is **not required and must not be sought**: the honest outcome may be that the repaired attacker is merely less self-defeating, and C5's original spirit — no performance gain the mechanism is not entitled to — carries over unchanged |

**U2, U3 and U3b are each evaluated per arm** (`A`, `B`, `AB`) against the
`declared` arm, which is what the three-arm design is for. A conclusion that
holds only for `AB` is a different finding from one that holds for `A` alone, and
the analysis reports it that way rather than collapsing to a single verdict.

### The two directions that are deliberately uncomfortable

**U4 and U5 are committed against the repair.** The easy story is that a repaired
cost model makes the attacker both better and more diverse. U4 says the entropy
must not fall; U5 refuses to require a breadth gain at all. If the repaired
attacker turns out merely *less self-defeating* than the shipped one — same
breadth, fewer blocked attempts — that is the honest result and it is what these
two are written to let the record say without softening.

**U3b can only embarrass the mechanism, never flatter it.** If the repair
produces a uniform response across both mechanism families, U3 might still hold
while the *explanation* offered for it is wrong, because `mtd_clears` says the
cost term is blind to application-layer mutation. A held U3 with a moved U3b is
therefore a weaker result than a held U3 alone would appear to be, and the record
must report it as such. Note that the split U3b tests is the same mechanism split
the project's headline ranking-inversion result turns on
([`experiment_02_findings.md`](experiment_02_findings.md) §9), which is why the
prediction is worth making rather than merely worth checking.

## 5. The stopping rule

**If U2 moves, stop and report.** A repair that does not reach the defect it was
built for is a finding about the *diagnosis*, not a licence to re-specify until
it lands — the same rule the disengagement brief puts on its own C2. No arm may
be added, no λ chosen, and no criterion relaxed after a moved U2. The record
would then say that the double-penalty diagnosis was correct as an account of the
model and wrong as an account of the attacker's collapse, which is itself a
result worth having.

**No declared value may be chosen because it improves an outcome.** The three
declared parameters are unchanged by construction, and gate 2 (§6) asserts it.

## 6. Validation gates — all discharged before the sweep

1. **Exactness (U1).** The λ = 0 identity asserted over the full configuration
   grid, per arm, as a test rather than a run.
2. **No new declared value.** A test asserting the iterated model reads only
   `tactic_durations.json`, `precondition_relation.json`, the profile nets and
   the existing ρ / `cost_floor_s` / λ — with a structural companion asserting
   the module names no data path of its own, so there is no second home a value
   could enter through.
3. **Determinism (SIM-05).** Re-verified because the modulator is now stateful: a
   conditioned run reproduces exactly under both MTD conditions.
4. **The laundering check.** Change B measures distance in the same graph the
   base transition weights live on, so benefit\* is asserted **not monotone** in
   the base out-weight over every edge of every profile's net. Without it the
   term would be laundering corpus frequency as value, and the separation the
   shipped family earned would be lost.
5. **Reader gates unchanged.** The full `tests/l3_simulation` suite and the
   substrate / carve / golden suites pass; no golden moves, since this is a
   movement-layer modulator and the substrate is untouched.

## 7. What this study will not license

- **No operating λ recommendation.** λ = 1 is the declared value because it is
  the only point in the band with a non-arbitrary reading, not because a sweep
  preferred it.
- **No ranking of profiles, and no ranking of MTD mechanisms.** The sub-study
  separates two families; it is not powered to order four mechanisms.
- **No composition with the axis-7 readiness learner.** Change A and the learner
  condition on the same readiness signal against the same artefact, so composing
  them would double-count it. The bar and the reason the existing joint check
  does not transfer are recorded in
  [`modulator_composition.md`](modulator_composition.md).
- **No re-running of any recorded experiment** under the iterated model. The
  frontier, experiment 2 and the axis sweeps stand as records of the model they
  ran under.

## 8. Where the results land

Verdicts and the full record go to
[`iterated_cost_model.md`](iterated_cost_model.md), added by the commit that runs
the sweep. The axis-6 badge moves **only if U3 holds**, and the round is logged
as R3 in `attacker_utility.json`.
