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

*Everything above this line was committed before the sweep existed (`8bbc530`).
Everything below reports against those criteria without amending them.*

**The run.** 2 080 runs, zero errored cells, `data/results/fsm_succession/`.

**B5 HELD.** ρ(α = 0) = **−0.821** against experiment 2's −0.893 and a criterion of
−0.5, with the contemporaneous baseline reproducing that run's no-MTD figure
exactly (38.40 hosts). The sweep is measuring the phenomenon it set out to
decompose.

## B1 — MOVED, and it moved in the direction opposite to the criterion

| α | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|--:|--:|--:|--:|--:|
| ρ vs the inherited attacker | −0.821 | −0.929 | −0.893 | −0.857 | **−1.000** |

ρ(1) − ρ(0) = **−0.179** against a bar of +0.50. The inversion does not weaken as
the attacker is aligned to the inherited FSM's own procedural order. **It
strengthens**, and at the limiting end it becomes a *perfect* reversal — the
profiled attacker's defence ranking is the exact inverse of the inherited
attacker's.

**Every non-degenerate band point sits at or below the null.** α = 1 is flagged
degenerate by the guard (§4 below) and its ρ may not be reported as a statement
about the inversion, exactly as pre-registered — but 0.25, 0.5 and 0.75 are all
clean and all sit below −0.821. The claim the sweep licenses is therefore the
strong form of the negative: **across the whole usable band, buying off the
inherited FSM's procedural rigidity does not make the two attackers agree about
the defence.**

## B2 — MOVED, and the sign is the finding

| α | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|--:|--:|--:|--:|--:|
| hosts, no MTD | 5.60 | 5.20 | 4.86 | 4.26 | **2.18** |
| 95 % CI half-width | ±0.59 | ±0.72 | ±0.63 | ±0.52 | ±0.48 |
| gap to baseline closed | 0.0 % | −1.2 % | −2.3 % | −4.1 % | **−10.4 %** |

Monotone, and monotone **downward**. Aligning the CTI attacker to the inherited
FSM does not narrow its disadvantage; it **widens** it, by about a tenth of the
gap at the limit and measurably at every step before it.

**Read beside factor 8, this is the sweep's most valuable output.** Two
independent instruments, with different targets and different failure modes, now
answer the same question:

| instrument | target | answer |
|---|---|---|
| factor 8 | distance to a productive action | **≤ 7.4 %** of the breadth gap is procedural rigidity |
| factor 9 | the inherited FSM's own succession | the gap **widens** by 10.4 %; the inversion strengthens |

The standing alternative explanation for the project's headline — *the profiled
attacker under-performs because it walks the wrong order for this simulator, so
the inversion is a mismatch artefact* — is now refuted twice over, and the second
refutation is the sharper one. Factor 8 could be read as "the dial was too weak to
close the gap". Factor 9 cannot: it aligns the attacker to the incumbent's own
procedure, the procedure the incumbent thrives on, and the attacker gets **worse**.
The two attackers depend on different substrate properties, and forcing one to
walk the other's order does not transfer the dependency — it only costs the
follower the structure it had.

## B3 — MOVED, and it locates itself precisely

| α | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|--:|--:|--:|--:|--:|
| pooled blocked fraction | 51.5 % | 51.6 % | 51.4 % | 52.7 % | 49.7 % |
| attempted actions per run | 363 | 334 | 303 | 254 | **165** |
| dwell-only share of visits | 34.1 % | 37.8 % | 42.6 % | 50.4 % | **67.6 %** |

Friction is **flat** — it neither falls (the criterion) nor explodes (factor 8's
failure, +21 points). The criterion is not met, so B3 is recorded MOVED and B1 and
B2 may not be attributed to alignment on this evidence.

But the row that fails is not the row that matters, and the anatomy says why. What
the dial actually does is not reduce friction, it **removes action**:

| α | 0 | 1.0 |
|---|--:|--:|
| `ENUM_HOST` share of actions | 16.6 % | **57.8 %** |
| `EXPLOIT_VULN` | 28.2 % | 9.4 % |
| `BRUTE_FORCE` | 11.1 % | 2.1 % |

**The two design choices interact badly at high α, and this is the honest
mechanism.** Dwell-only places are transparent — they keep full weight because
they fire nothing and so cannot violate the succession. But when the licensed verb
set is narrow, the *seven* dwell-only tactics of `v2_partial` dominate the
renormalised distribution against the *one* tactic that dispatches the licensed
verb. Tightening the verb constraint therefore shifts mass onto **dwell**, not
onto the licensed verb. The attacker ends up pivoting (`ENUM_HOST` is licensed
from three states, so it is the most frequently permitted verb) and otherwise
waiting.

That is a property of transparency composed with a narrow relation, not a defect
in either alone, and it is the thing a successor would have to design around.

## B4 — HELD

| α | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|--:|--:|--:|--:|--:|
| pooled path entropy (bits) | 2.714 | 2.712 | 2.694 | 2.610 | 1.682 |
| distinct places per run | 13.41 | 13.40 | 13.34 | 13.32 | 11.39 |

Monotone non-increasing, as committed. **The prediction that this factor would be
gentler on plurality than factor 8 is confirmed**: 1.682 bits against factor 8's
1.112 at the same band point, and distinct places 11.39 against 9.16. Any arm
quoting a non-zero α quotes its own figure from this table.

## §4 — the rewritten guard fired, and it fired on the clauses factor 8's lacked

| α | hosts (modal) | succ/act | actions | places | entropy | assists | verdict |
|---|--:|--:|--:|--:|--:|--:|---|
| 0 | 5.60 (6) | 0.358 | 363 | 13.41 | 2.714 | 0/7 | ok |
| 0.25 | 5.20 (5) | 0.357 | 334 | 13.40 | 2.712 | 0/7 | ok |
| 0.5 | 4.86 (4) | 0.360 | 303 | 13.34 | 2.694 | 0/7 | ok |
| 0.75 | 4.26 (4) | 0.346 | 254 | 13.32 | 2.610 | 0/7 | ok |
| **1.0** | **2.18 (0)** | 0.303 | **165** | 11.39 | 1.682 | 0/7 | **DEGENERATE** |

**The prediction was wrong — one band point is degenerate — and the guard is
vindicated anyway, which is the more useful outcome.** Three clauses fired at
α = 1: hosts below half the null's, **modal hosts = 0** (the modal run compromises
nothing at all), and actions outside the two-sided band. Two of those three are
clauses that did **not exist** in factor 8's pre-registration, and the third is the
lower half of a bound factor 8 wrote one-sided.

Put plainly: **factor 8's guard, applied to this sweep, would have passed α = 1**
— places 11.39 > 3, entropy 1.682 > 0.1, actions not more than halved on the
one-sided reading. The rewrite was not bookkeeping.

One clause is worth recording for *not* firing. **`assists` is 0/7 at every band
point**: no MTD condition ever produces more breadth than no-MTD. Factor 8's
limiting end had the defence acting as the attacker's pivot generator, and that
pathology is genuinely absent here — the FSM target fixed the thing it was chosen
to fix. What it did not fix is a different failure, which is why it is reported as
a second measured negative rather than as a repair.

## Abstention and fallback — the bound on what the dial could do

| α | decisions | abstained | capability fallback | candidates suppressed |
|---|--:|--:|--:|--:|
| 0.25 | 217 388 | 8.9 % | 15.7 % | 579 969 |
| 0.5 | 213 493 | 9.1 % | 14.6 % | 572 516 |
| 0.75 | 205 915 | 9.6 % | 13.4 % | 554 877 |
| 1.0 | 204 175 | 9.5 % | 8.2 % | 512 299 |

Roughly one decision in eleven offered no FSM-legal move and the factor did
nothing; roughly one in seven had to fall back to the capability closure because
the licensed successor could not run. Neither rate is large enough for the
measured effects to be an artefact of a rarely-acting dial — over half a million
candidates were suppressed at every band point.

## What this leaves

1. **The alignment programme has now returned two measured negatives, and
   together they are a result rather than two failures.** Neither instrument closes
   the gap; the second widens it. The procedural-confound explanation for the
   inversion is refuted from two directions, and the dissertation can state the
   inversion as behavioural with a quantity attached rather than an argument.
2. **No third factor is licensed by this.** The stopping rule was written for
   exactly this outcome: *if the limiting end is degenerate again, that is recorded
   as a second measured negative for the alignment programme, not repaired into a
   third factor.* The transparency-versus-narrow-relation interaction in B3 is
   recorded as the thing a successor would design around, not as a brief.
3. **The reported configuration is untouched.** The headline arm still runs
   modulators null; α is declared 0.0; no badge moved and none was eligible to.
