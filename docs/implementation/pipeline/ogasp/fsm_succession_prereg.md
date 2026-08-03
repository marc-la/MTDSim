---
status: open
created: 2026-08-03
updated: 2026-08-03
topic: "Pre-registration of the FSM-succession sweep — the design, five conclusions with criteria fixed in advance, the direction committed, the kill criterion inherited from the factor-8 sweep, and the two degeneracies its guard was blind to, now guarded explicitly"
---

# The FSM-succession sweep, pre-registered

**Everything in this file is committed before the sweep produces a single row.**
The verdicts land below the fold in a separate commit, scored against these
criteria without amending them.

**This sweep moves no badge and can move none.** Factor 9 scores no axis
([`fsm_succession_overlay.md`](fsm_succession_overlay.md)), and nothing below is
written so that a verdict could raise a row.

## 1. The question, and what changed since the last attempt

Factor 8's sweep asked whether the defence-ranking inversion is procedural or
behavioural, and returned a usable answer — **at most ~7 % of the profiled
attacker's breadth disadvantage is procedural rigidity of the kind a
capability-distance dial removes** — but its limiting end was uninterpretable: the
attacker reached permanent readiness on a single host and MTD became its pivot
generator ([`fsm_alignment_prereg.md`](fsm_alignment_prereg.md) §3).

Factor 9 changes the *target*, not the question. It conditions on the inherited
FSM's own succession, which pivots after a compromise by construction, so the
failure mode that made factor 8's endpoint unreadable should not recur. The sweep
therefore re-asks factor 8's question with an instrument whose limiting end is
expected to be interpretable — and **that expectation is itself a conclusion
below, so it can fail.**

**The direction is committed here, in advance, and it is committed toward the
result that superficially reads as damage.** If the inversion weakens as α rises,
that is a quantified statement that the inversion is procedural rather than
behavioural — the *less* flattering reading for the project's headline. Factor 8
found it did not weaken; the honest expectation is that factor 9 finds the same,
with a cleaner instrument.

## 2. The design

| input | value | why |
|---|---|---|
| controller mapping | `v2_partial` | experiment 2's, so the null arm is comparable to the run this is aimed at |
| outcome overlay | `v3_persistent_backward` | experiment 2's; named deliberately, the registry default is experiment 1's |
| sink policy | retrace | experiment 2's main matrix |
| mutation interval | **200 s only** | the inversion is a property of the high-pressure regime (ρ = +0.286 at 2 000 s), so the phenomenon does not exist at the relaxed interval |
| horizon / geometry / timing | 15 000 s / standard 50-host / S3-R | unchanged, so the substrate is not a variable |
| seeds | 0–9 | ten. See §5 |
| α band | 0, 0.25, 0.5, 0.75, 1.0 | the declared band |
| modulators 3, 4, 8 | **off** | the factor-4 composition bar, and factor 8 is the thing being superseded |

Arms: `baseline` (the inherited FSM, re-run inside this sweep so both arms come
off the same substrate) and `movement@α` for each band point. Eight defence
conditions, unchanged from experiment 2. **2 080 runs.**

## 3. The conclusions, each with its criterion fixed in advance

**B1 — the inversion's response to α.** The statistic is experiment 2's E5
verbatim: Spearman ρ between the baseline's and the movement arm's orderings of
the seven non-`none` defence conditions, by pooled breadth suppression. HELD if
ρ(α) is **non-decreasing across all five band points** *and* **ρ(1) − ρ(0) ≥ 0.5**.
The full curve is reported whichever way it falls. *Expectation: MOVED, matching
factor 8 — the inversion is behavioural.*

**B2 — the breadth gap.** Pooled distinct-host count under `none` is
**non-decreasing across the band**, and at α = 1 has closed **at least half** the
gap between α = 0 and the contemporaneous baseline. The *fraction closed* is
reported whichever way it falls, and is directly comparable with factor 8's
7.4 %. *This is the number the instrument exists to produce.*

**B3 — the dial does what it says.** Pooled blocked fraction is **non-increasing
across the band**. Unlike factor 8's criterion this carries **no magnitude
requirement**, because the FSM target is not expected to reduce friction so much
as to stop manufacturing it — factor 8's failure was a *rise* of 21 points. If B3
MOVES, B1 and B2 may not be attributed to alignment.

**B4 — the plurality cost, committed in the unflattering direction.** Pooled path
entropy is **non-increasing across the band**. Reported per band point so any arm
quoting a non-zero α quotes its own figure. *Expectation: HELD, but far less
steeply than factor 8's 2.712 → 1.112, because dwell-only places are transparent.*

**B5 — the kill criterion, inherited unchanged.** ρ(α = 0) ≤ −0.5 against this
sweep's own contemporaneous baseline. If it fires, no ρ(α) curve may be reported
as a statement about the inversion.

## 4. The degeneracy guard, rewritten because the last one was blind

Factor 8's pre-registration wrote three guards and **all three passed at a band
point where the attacker owned one host forever**. Every one was
activity-denominated — distinct places, entropy, action count — and the failure
that occurred was the mirror image of the one predicted: the attacker acted four
times as much and achieved less. The lesson was recorded; here it is applied.

A band point is **degenerate**, and its ρ may not be reported as a statement about
the inversion, if **any** of the following holds:

1. **Progress-denominated (the guard factor 8 lacked).** Pooled distinct hosts
   under `none` falls below **half** the α = 0 arm's, *or* pooled successes per
   attempted action falls below half the α = 0 arm's.
2. **Immobility.** The modal number of distinct hosts compromised under `none` is
   ≤ 1 across seeds — the exact signature factor 8's α = 1 arm showed (38 of 50
   runs at one host) and that no factor-8 guard could see.
3. **Defence-assists-attacker.** Pooled breadth under any MTD condition *exceeds*
   pooled breadth under `none` — which is what actually flipped factor 8's ρ, and
   is reported as its own finding rather than folded into the curve.
4. **Activity (retained from factor 8, both directions).** Distinct places below
   3, entropy below 0.1 bits, or mean attempted actions outside
   [0.5×, 2×] the α = 0 arm's. The upper bound is new: factor 8's action count
   *quadrupled*, and a one-sided guard could not see it.

**Predicted:** none of the four fires. That is the point of changing the target,
and committing the prediction is what makes it falsifiable.

**Also reported, not a guard:** the **abstention rate** — the share of routing
decisions at which the net offered no FSM-legal move and the factor did nothing.
It bounds what the dial can do at all, and a large α effect alongside a large
abstention rate would mean the effect came from few decisions.

## 5. What this run is not powered for

Ten seeds supports a **rank comparison, not a significance test** — established
four times over in this project's record. No per-profile ρ is claimed. B2's gap is
measured on distinct hosts, an event-wise quantity, because the two attackers are
not comparable on time.

## 6. The stopping rule

Nothing above is re-specified after a row exists. No arm added, no criterion
relaxed, no band point dropped for reading badly. In particular: **if the limiting
end is degenerate again, that is recorded as a second measured negative for the
alignment programme, not repaired into a third factor.**

## 7. Reproduce

```
PYTHONPATH=src python data/results/fsm_succession/run_sweep.py --workers 7
PYTHONPATH=src python data/results/fsm_succession/analyse.py
```

---

# The verdict, as found

*Everything above this line was committed before the sweep existed. Everything
below reports against those criteria without amending them.*

**Not yet run.**
