---
status: durable
created: 2026-08-02
updated: 2026-08-02
topic: "Pre-registration of the FSM-alignment sweep — the design, the five conclusions with their criteria, the direction committed in advance, the kill criterion on attributability, and one degeneracy predicted rather than discovered"
---

# The FSM-alignment sweep, pre-registered

**Everything in this file is committed before the sweep produces a single row.**
The verdicts land below the fold in a separate commit, scored against these
criteria without amending them. The commit order is the audit trail, exactly as it
was for the rationality-exponent sweep, the learning sweeps, the iterated cost
model and the progress-credit sweep.

**This sweep moves no badge and can move none.** The factor it exercises scores
no axis ([`fsm_alignment_overlay.md`](fsm_alignment_overlay.md)), and nothing
below is written so that a verdict could raise a row. What it measures is a
**confound** in this project's headline result, on this project's own substrate.

## 1. The question, and why a falling effect is the valuable answer

Experiment 2 found that the ranking of MTD mechanisms very nearly reverses between
the inherited attacker and the profiled one — rank correlation **ρ = −0.893** at
the operating interval ([`experiment_02_findings.md`](experiment_02_findings.md)
§9). That is the project's strongest result and it is currently a **categorical**
one: two attackers, two orderings, and an argument about why.

The standing alternative explanation is procedural. The profiled attacker walks
CTI order on a substrate whose action layer enforces a different order, and it
compromises roughly a seventh of what the inherited attacker does. Some of that
gap is behaviour and some is rigidity, and nothing on record separates them.

The dial separates them by construction. **If the inversion weakens monotonically
as α rises and has substantially vanished by α = 1, that is a strong, quantified
statement that the inversion is caused by the attacker's behavioural shape rather
than by noise or by an artefact of the mapping** — because α = 1 is precisely the
arm in which the behavioural shape has been replaced by the substrate's own
procedural order. It converts a categorical contrast into a dose-response curve.

**The direction is committed here, in advance, and it is committed toward the
result that superficially reads as damage.** A vanishing inversion at α = 1 is the
*expected* and *confirmatory* outcome. An inversion that survives α = 1 unchanged
would be the surprising one, and would mean something other than procedural
alignment drives it.

## 2. The design

| input | value | why |
|---|---|---|
| controller mapping | `v2_partial` | experiment 2's, so the α = 0 arm is comparable to the run this sweep is aimed at |
| outcome overlay | `v3_persistent_backward` | experiment 2's; the registry default is still experiment 1's, so it is named deliberately |
| sink policy | retrace | experiment 2's main matrix |
| timing regime | S3-R stochastic | unchanged |
| horizon | 15 000 s | unchanged |
| geometry | the standard 50-host network | unchanged, so the substrate is not a variable |
| mutation interval | **200 s only** | see §2.1 |
| seeds | 0–9 | ten. See §5 |
| α band | 0, 0.25, 0.5, 0.75, 1.0 | the declared band |
| modulators 3, 4 | **off** | the factor-4 composition bar ([`modulator_composition.md`](modulator_composition.md) §2.1) |

### 2.1 One interval, and the reason it is one

Experiment 2 carried the mutation interval as a dimension because a defence
ranking taken inside the degenerate region means nothing on its own. This sweep
runs at **200 s only**, and that is a scope decision rather than an oversight:
**the inversion is a property of the high-pressure regime** — at 2 000 s the same
correlation is ρ = +0.286 — so the phenomenon this study exists to decompose does
not exist at the relaxed interval. Halving the matrix to measure a thing where it
is absent would buy nothing.

The cost of that decision is stated rather than hidden: **no claim from this sweep
extends above the operating interval**, and any success-rate-shaped reading of it
is pinned at zero by the degenerate region and is not reported.

### 2.2 The arms

| arm | what it is | what it is for |
|---|---|---|
| `baseline` | the inherited 6-phase FSM, untouched | the reference ordering the inversion is measured against |
| `movement@α` | the profiled attacker with factor 8 at α | five arms, one per band point |

The baseline arm is **re-run inside this sweep** rather than read from experiment
2's stored rows. Both arms must come off the same substrate at the same time, and
the movement runner's API has moved since that experiment; reusing its numbers
would put an unquantified substrate difference inside the one comparison the study
turns on.

## 3. The matrix

| block | runs |
|---|---|
| 5 α × 5 profiles × 8 defence conditions × 10 seeds | 2 000 |
| baseline × 8 defence conditions × 10 seeds | 80 |
| **total** | **2 080** |

The eight defence conditions are experiment 2's, unchanged: `none`, the four
single mechanisms, and the three multi-mechanism schemes, with the trigger
interval set explicitly on every condition so the scheme dimension means
something.

## 4. The conclusions, each with its criterion fixed in advance

**A1 — the inversion weakens monotonically in α.** *The headline.* The statistic
is experiment 2's E5 verbatim so the verdicts are comparable: Spearman ρ between
the baseline's and the movement arm's orderings of the **seven non-`none` defence
conditions**, ranked by pooled breadth suppression against each arm's own `none`
condition. HELD if ρ(α) is **non-decreasing across all five band points** *and*
**ρ(1) − ρ(0) ≥ 0.5**. The full curve is reported whichever way it falls, and the
five ρ values are reported as a table beside the verdict, because a
dose-response claim that reports only its endpoints is not a dose-response claim.

**A2 — the breadth gap closes.** The instrument's other half: how much of the
profiled attacker's disadvantage is rigidity. Criterion: pooled distinct-host
count under the `none` condition is **non-decreasing across the band**, and at
α = 1 has closed **at least half** the gap between the α = 0 arm and the
contemporaneous baseline arm's no-MTD figure. Reported as *the fraction of the gap
closed* whichever way it falls — that fraction is the number this whole
instrument exists to produce, and it is reportable even if the threshold is
missed.

**A3 — the dial does what it says.** A mechanism check, not a result. Criterion:
pooled blocked fraction is **non-increasing across the band**, and falls by at
least 20 percentage points from α = 0 to α = 1. If this MOVES, the distance model
is not biasing the attacker toward actions the substrate will accept, and **A1 and
A2 may not be attributed to alignment at all** whatever they show.

**A4 — the plurality is paid for, and the amount is reported.** Committed in the
unflattering direction, because the standing generalisation is that every
modulator narrows traversal and this one narrows it by construction. Criterion:
pooled path entropy is **non-increasing across the band**. Expected to HELD; the
figure is reported per band point so that any future arm quoting a non-zero α
quotes its own plurality figure, as the §4 pin requires.

**A5 — the kill criterion, on attributability.** The null arm must reproduce the
phenomenon this sweep decomposes, against **this sweep's own** contemporaneous
baseline. Criterion: **ρ(α = 0) ≤ −0.5**. If it is not, this sweep is not
measuring the inversion, and **no ρ(α) curve may be reported as a statement about
it** — the result would then be a finding about substrate drift since experiment
2, which is worth recording and is not this study.

## 5. What this run is not powered for, stated before it runs

Ten seeds supports a **rank comparison and not a significance test**. That
constraint is established four times over in this project's record, and A1 is a
rank statistic for exactly that reason. Three further limits:

- **A1's ρ is a statistic over seven points.** Its sampling behaviour is coarse:
  single adjacent swaps move it in visible steps. Monotonicity in α is therefore a
  weak-ish criterion by construction, and the criterion pairs it with a magnitude
  requirement rather than resting on the shape alone.
- **No per-profile ρ is claimed.** Pooling across profiles is what experiment 2's
  E5 does, and a per-profile ranking at ten seeds is the thing four previous
  sweeps failed to separate.
- **A2's "gap" is between two attackers that are not comparable on time.** It is
  measured on distinct hosts, an event-wise quantity, and no time-denominated
  cross-arm comparison is made.

## 6. One degeneracy predicted rather than discovered

The failure mode that would make A1 read as confirmation when it is not: **the
inversion could vanish at α = 1 because the attacker stops being an attacker**
rather than because it has aligned. A dial that limits transitions to shortest
paths could collapse the walk into a short cycle, and an attacker that does almost
nothing has no defence ordering to invert.

The prediction, committed now: **partial degeneracy at α = 1, in traversal
diversity but not in activity.** The minimal set is narrow early in a run (with
nothing held, exactly one tactic advances) and *widens* once the host cursor is
held (five tactics sit at distance 0 under `v2_partial`), so the walk should
concentrate without stopping.

**The guard.** If, at any band point, the pooled distinct-place count falls below
3, or pooled path entropy falls below 0.1 bits, or the mean attempted actions per
run falls by more than half against α = 0, then that band point is **degenerate**
and its ρ may not be reported as "the inversion weakened". It is reported as "the
attacker stopped acting", and A1 is scored on the non-degenerate band points with
the truncation stated.

## 7. The stopping rule

Nothing below is re-specified after a row exists. No arm is added, no criterion
relaxed, no band point dropped for reading badly. If A1 MOVES, it is recorded
moved and the curve is reported. If A5 fires, the sweep is reported as a
substrate-drift finding and A1–A4 are reported as descriptive only.

## 8. Reproduce

```
PYTHONPATH=src python data/results/fsm_alignment/run_sweep.py --workers 7
PYTHONPATH=src python data/results/fsm_alignment/analyse.py
```

---

# The verdict, as found

*Everything above this line was committed before the sweep existed. Everything
below reports against those criteria without amending them.*
