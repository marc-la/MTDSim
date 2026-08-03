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

*Everything above this line was committed before the sweep existed (`eb83d90`).
Everything below reports against those criteria without amending them.*

**The run.** 2 080 runs, zero errored cells, `data/results/fsm_alignment/`.

**A5 HELD, and the substrate-drift worry §2.2 hedged against is retired by
measurement rather than by argument.** The contemporaneous baseline arm reproduces
experiment 2's recorded figures *exactly* — 38.40 hosts with no MTD, and all four
single-mechanism suppressions to within 0.1 of a percentage point (90.4 %, 88.8 %,
22.1 %, 18.2 %). The α = 0 movement arm reproduces its no-MTD figure exactly
(5.88 hosts) and its suppressions to within 1.8 points. The null arm's rank
correlation against the baseline is **ρ = −0.857**, against experiment 2's −0.893
and a criterion of −0.5. This sweep is measuring the phenomenon it set out to
decompose.

## A1 — MOVED, and the shape it moved on is the finding

| α | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|--:|--:|--:|--:|--:|
| ρ vs the inherited attacker | −0.857 | −0.821 | −0.786 | −0.857 | **+0.607** |

The magnitude criterion is met — ρ(1) − ρ(0) = **+1.464** against a bar of 0.50 —
and monotonicity fails, so the conclusion is recorded **MOVED** on the reading
fixed in advance. What fails is more informative than a pass would have been:
**the inversion is not dose-responsive. It is threshold-shaped, and
three-quarters of the dial buys nothing at all.** Between α = 0 and α = 0.75 the
correlation moves by 0.000 net — it drifts to −0.786 and returns to where it
started — while over the same span the attacker's compromise breadth rises by
41 %. Procedural alignment, in any partial measure this band can express, changes
what the attacker *achieves* without changing which defence an evaluator would
choose.

**The α = 1 endpoint may not be read as the inversion vanishing by alignment.**
That is A3's disqualifier firing exactly as pre-registered, and §3 shows what the
endpoint actually is.

## A3 — MOVED, and it locates itself

| α | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|--:|--:|--:|--:|--:|
| pooled blocked fraction | 47.0 % | 45.0 % | 42.5 % | 40.6 % | **61.4 %** |
| attempted actions per run | 363 | 385 | 418 | 510 | **1 250** |
| dwell-only visits per run | 188 | 183 | 176 | 153 | **38** |

Over four-fifths of the band the dial does exactly what it says: friction falls
monotonically, the attacker stops spending visits in places that dispatch nothing,
and it acts more. At the limiting end friction jumps 21 points while activity more
than doubles.

The rise is **entirely located in the position-destroying conditions**, which is
what makes it diagnosable rather than mysterious:

| blocked fraction | α = 0 | α = 0.75 | α = 1 |
|---|--:|--:|--:|
| `none` | 0.153 | 0.097 | 0.112 |
| OS / Service Diversity | 0.163 | 0.108 | 0.112 |
| IP Shuffle | 0.726 | 0.695 | **0.931** |
| Complete Topology Shuffle | 0.722 | 0.660 | **0.922** |

Under no defence, and under the defences the capability vocabulary cannot see,
friction keeps falling all the way to the limit. Under the defences that sever
position it explodes. **The declared relation's own recorded optimisms are the
cause** — it models `SCAN_HOST` as producing `host_stack` where the substrate can
produce an *empty* stack, and `SCAN_PORT` as producing `curr_ports` where a host
with no open ports yields nothing. Those over-predictions are harmless when
diluted across a plural walk, because the attacker tries other things. At α = 1
the dial removes the dilution: the attacker retries the over-predicted verb
exclusively, because the model keeps rating it minimal. **A declared predictive
model's known optimisms are a rounding error under a plural policy and become the
whole behaviour under a hard one** — which generalises past this factor to any
declared relation used as a *constraint* rather than as a *prior*.

## 3. What α = 1 actually is — the anatomy, recorded rather than explained away

Under **no MTD** at α = 1, across fifty runs, the attacker compromises **exactly
one host in 38 runs and none in the other 12**. It does so over 1 296 attempted
actions, at a blocked fraction of 0.112 and a success rate per action of 0.396 —
the *lowest* friction and among the *highest* per-action success rates anywhere in
the sweep. It is maximally able to act and completely immobile.

The reason is the distance model's own arithmetic. Once `curr_host` is held,
`SCAN_PORT`, `BRUTE_FORCE` and `EXPLOIT_VULN` all sit at distance 0, while
`ENUM_HOST` — the verb that moves the cursor to a **fresh** host — sits at 1. The
limiting end therefore zeroes the only move that creates new opportunity. The verb
mix says it plainly: `SCAN_NEIGHBOR` falls from 22.6 % of actions to **0.7 %** and
`SCAN_HOST` from 4.4 % to **0.3 %**, while `BRUTE_FORCE` triples to 33.7 %.

### 3.1 The consequence — MTD becomes the attacker's pivot generator

Because a network-layer mutation clears `curr_host`, it is the **only event that
returns `ENUM_HOST` to the minimal set**. At α = 1 the defence therefore does the
attacker's pivoting for it, and breadth under attack *exceeds* breadth under no
attack at all:

| condition (α = 1) | hosts | interrupts | `ENUM_HOST` share | distinct places |
|---|--:|--:|--:|--:|
| `none` | 0.76 | 0.0 | 25.5 % | 7.28 |
| OS Diversity | 0.76 | 66.9 | 24.6 % | 7.28 |
| Service Diversity | 0.76 | 66.8 | 24.6 % | 7.28 |
| IP Shuffle | **2.56** | 75.0 | 31.8 % | 10.36 |
| Complete Topology Shuffle | **3.22** | 75.0 | 31.7 % | 10.40 |

Suppression goes **negative** across the whole position-destroying family, and
that — not any convergence toward the inherited attacker — is what flips ρ.
Ranking the conditions by suppression puts the diversity family first because it
suppresses *nothing*, and the position family last because it *helps*. The
resulting order happens to resemble the baseline's. **The resemblance is an
artefact of a defence that assists a stuck attacker, and reporting ρ(1) = +0.607
as "the inversion vanished" would be reporting a coincidence of orderings as a
mechanism.**

### 3.2 An independent confirmation of the boundary, unlooked for

The two diversity rows above are identical to the no-MTD row to three significant
figures — 0.76 hosts, 7.28 distinct places, `ENUM_HOST` at 24.6 % — while
interrupting the attacker 67 times per run. The declared capability vocabulary is
**measurably** blind to what OS and Service Diversity destroy, which the design
record's §4 boundary and the indistinguishability handoff had argued rather than
measured. The confinement of every MTD claim from this factor to the
position-destroying family is now evidenced rather than assumed.

## A2 — MOVED, and it yields the number the instrument was built to produce

| α | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|--:|--:|--:|--:|--:|
| hosts, no MTD | 5.88 | 6.32 | 7.40 | 8.28 | **0.76** |
| 95 % CI half-width | ±0.63 | ±0.79 | ±0.89 | ±1.23 | ±0.12 |
| gap to baseline closed | 0.0 % | 1.4 % | 4.7 % | **7.4 %** | −15.7 % |

Monotone and rising across the usable band, then collapsing. The criterion asked
for half the gap and the sweep delivers a fourteenth of it, so the conclusion is
**MOVED** — and the fraction is reported as the pre-registration required, because
it is the answer this instrument exists to give:

> **At most about 7 % of the profiled attacker's compromise-breadth disadvantage
> is procedural rigidity of the kind a declared alignment bias can remove.** The
> other ~93 % is not attributable to CTI order fighting the substrate's procedural
> order.

That is a small number and it is load-bearing. The standing alternative
explanation for this project's headline result — that the profiled attacker
under-performs because it walks the wrong *order*, rather than because it is a
behaviourally different adversary — is now **quantified and largely refuted** on
this substrate. The measurement is confined to what it measured: compromise
breadth, at the operating interval, on the `v2_partial` mapping, against the one
alignment mechanism built. It does not license a claim about *why* the remaining
93 % sits where it does.

## A4 — HELD

| α | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|--:|--:|--:|--:|--:|
| pooled path entropy (bits) | 2.712 | 2.705 | 2.677 | 2.552 | 1.112 |
| distinct places per run | 13.42 | 13.40 | 13.39 | 13.24 | 9.16 |

Monotone non-increasing, as committed in the unflattering direction. The dial is
cheap in plurality until it is not: three-quarters of the band costs 0.16 bits and
the last quarter costs 1.44. Any future arm quoting a non-zero α quotes its own
figure from this table, per the pin — which is untouched, since the reported
headline configuration still runs modulators null.

## 4. The degeneracy guard did not fire, and it was blind rather than satisfied

This is the sharpest methodological lesson of the sweep, and it is recorded
against the pre-registration that got it wrong.

§6 predicted partial degeneracy at α = 1 and wrote three guards for it: distinct
places below 3, entropy below 0.1 bits, or mean actions less than half the null
arm's. **None fired** — places 9.16, entropy 1.112, and actions not halved but
*quadrupled*. On the guard's own reading, α = 1 is a healthy band point.

It is not. The attacker at α = 1 owns one host, forever, and the guard cannot see
it. All three were specified for a single imagined failure — *the attacker stops
acting* — and what happened is that failure's mirror image: **the attacker acts
far more and achieves far less.** The prediction reasoned about the *routing
structure* (a narrow minimal set early in a run, widening once a foothold is held)
and never about *what the routing is for*, so the guard it produced was
activity-denominated when the thing at risk was progress.

The guard that would have caught it is one line — successes per attempted action,
or breadth against the null arm — and both quantities were already in the record
before the sweep ran. This is the fourth time in this project's history that a
pre-registered measure has failed by counting the wrong denominator, and it
belongs beside the others: the saturated depth measure, the retention measure that
counted footholds severed rather than kept, and the criterion a negative control
passed.

**A1 and A2 are scored on the full band regardless**, because their criteria are
what they are and the stopping rule forbids re-specification. What §3 supplies is
the *attribution*, which is a separate thing from the verdict — and A3's
disqualifier, written in advance, is what makes that separation binding rather
than editorial.

## 5. The transferable claim, and where it converges

**"Distance to a productive action" is not "distance to progress".** The distance
model rewards an attacker for being *able* to attack, and being able to attack is
not the same as getting anywhere: at the limiting end the attacker optimises
itself into a state of permanent readiness on a single host it has already taken.

That is the **axis-7 credit-signal finding reappearing in a mechanism with no
learning in it at all**. The learner under its `acceptance` rule was measured to
track whether an action was *permitted* at rank correlation +0.921 and whether it
*advanced the attacker* at −0.027, and it optimised away from the objective for
exactly that reason ([`progress_credit.md`](progress_credit.md) §2). This factor
accumulates nothing, believes nothing, and updates from nothing — it is a static
lookup over a declared relation — and it fails the same way. Two mechanisms, one
built on accumulation and one on a table, share a failure mode because they share
a **target**, not a method.

The claim that generalises past both: **an evaluation that rewards an attacker for
permitted or enabled actions, by any mechanism, will measure the attacker
optimising into the state where the most actions are permitted — which on this
substrate is a single owned host.** It is a statement about the choice of target
rather than about the choice of algorithm, and it is one this project can now make
from two independent directions.

**This moves no badge and is not offered as evidence for one.** Axis 6 is closed,
axis 7's mechanism scope is ruled, and this factor scores nothing. What it earns
is a citation in the discussion chapter beside the credit-signal warning, as its
second and independent instance.

## 6. What is now open

Three items, none actioned here, each recorded so it is not re-derived:

1. **The objective-verb set's home.** The design record §3 flags it as a seam
   impurity — substrate-specific knowledge living in movement-layer code because
   the brief consumed the precondition relation unchanged and unbumped. The sweep
   gives no reason to move it and none to leave it; it remains Marc's ruling.
2. **A progress-denominated distance would be a different factor, not a fix.**
   Distance to *compromise of a host not already owned* is expressible over the
   same closure — `ENUM_HOST` clears `foothold`, so the relation already carries
   the pivot. It would be a new declared model with its own pre-registration, and
   it is explicitly **not** licensed by this sweep: redesigning a mechanism because
   its measured result read badly is the scoring-driven design the criterion's
   standing constraint forbids. What the sweep licenses is the *observation*.
3. **The composition bar with factor 4 stays in force and is now better argued.**
   Nothing here ran the two together, and §3.1's mechanism supplies a concrete
   reason to expect them to compound rather than cancel: both now demonstrably
   prefer permitted actions, which is precisely the agreement the retired factor
   7's lesson says invalidates an inherited sub-additivity result.
