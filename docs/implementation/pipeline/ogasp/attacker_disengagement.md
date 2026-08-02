---
status: durable
created: 2026-08-02
topic: "The attacker-disengagement measure — built as a reader, validated against the inherited attacker where it separates every MTD condition from none, and unable to attribute the profiled attacker's disengagement to the defence. The kill criterion moved; the contrast between the two arms is the finding"
---

# Attacker disengagement — the measure works, and it says the profiled attacker's collapse is not MTD's doing

**Status:** durable results record. It discharges the attacker-disengagement
handoff. Conclusions and criteria were fixed in
[`attacker_disengagement_prereg.md`](attacker_disengagement_prereg.md) and
committed before a single reported row existed.

**The headline. C2 — the pre-registered kill criterion — MOVED, so the stopping
rule fired and nothing was re-specified.** But the study is not a failure, and
the reason is the arm that was included precisely to tell the two apart: **on the
inherited attacker the measure separates every MTD condition from no-MTD
completely**, and on the profiled attacker it separates almost nothing. A measure
that registers the defence against one attacker and not the other is a statement
about **what each attacker's failure is made of**, and that is the result this
record reports.

## 1. What was built

A reader over the record stream, in `measures.py` §8. At each attempted action:

```
    T(t) = t + (W − h(t)) / r(t) ,     r(t) = (h(t) + α) / (t + α / r₀)
```

Effort `t` is attempted actions; progress `h(t)` is distinct hosts compromised;
`W = 40` is derived from the substrate's own termination condition
(0.8 × 50 nodes). Abandonment at budget `B` is the **first** `t` where `T(t) > B`;
a run whose projection never crosses is **censored**, not "did not abandon". The
budget is never declared — it is swept as `k × U` where `U = W / r₀ = 1 440`
actions, the effort an unimpeded attacker at its measured rate would need.

**It reports; it never stops a run.** The reporting unit is a snapshot — *the
attacker would have given up at action X* — and the run continues. An attacker
that actually stopped would make "MTD causes disengagement" definitional, with no
null arm able to falsify it.

**One declared value survives** (α = 1.0, the Laplace pseudo-count). `W` is
derived, `r₀` is measured from the unimpeded inherited attacker, and `B` is a
reporting axis.

### 1.1 The instrumentation gate failed as designed, and that is why the schema moved

The design assumed cumulative compromise *events* could proxy the distinct-host
trajectory. Measured over 50 runs before anything was built: **837 events against
155 distinct hosts, a ratio of 5.40** — and worse without MTD (5.4–8.8) than with
it (1.8–3.5). Using events would have biased precisely the MTD-versus-no-MTD
comparison C2 tests. `MovementRecord` therefore gained one integer,
`n_compromised`, sampled from the substrate's own list and asserted monotone,
duplicate-free and equal to `compromised_count` at the horizon. The suite's
standing preference is to extend the reader rather than widen the record; that
measurement is the burden of proof discharged, and no golden moved (the field is
popped from the golden serialisation exactly as `retrace` is, on the builder's
own principle that only behaviour may move a digest).

## 2. Verdicts

400 movement runs (5 profiles × 8 defence conditions × 10 seeds, `v2_partial`,
200 s interval, 15 000 s horizon) and 80 baseline runs.

| | Conclusion | Verdict |
|---|---|---|
| **C1** | the measure is non-degenerate across the patience band | **held (5/5)** |
| **C2** | **KILL CRITERION** — abandonment effort is CI-disjoint from no-MTD | **MOVED (2/5)** |
| **C3** | mechanisms differ from one another | **MOVED** — no adjacent pair separates |
| **C4** | it discriminates where ASR cannot | **MOVED** — same evidence as C3 |
| **C5** | **committed to embarrass it** — not a restatement of breadth | **held** (Spearman +0.521) |

**C1 held decisively.** Mean abandonment effort varies across the band by 62 to
308 actions against typical interval widths of 0 to 10 actions. The patience axis
carries information, which is the precondition for everything else.

**C5 held, and it is the conclusion most at risk of failing.** The measure's
progress term is distinct hosts and breadth is distinct hosts at the horizon, so
a monotone re-expression was a live possibility. At Spearman **+0.521** over 40
cells it is related to breadth without being a restatement of it — the projection
carries rate and remaining work, not only the level.

## 3. The validity arm — the measure is not broken

The inherited attacker was included so that a null result on the profiled arm
could be read correctly. That arm actually progresses (38.4 distinct hosts
unimpeded), and the measure registers the defence on it **unambiguously**:

| condition | mean abandonment at k = 2 | censoring | distinct hosts |
|---|--:|--:|--:|
| **none** | — | **1.00** | 38.4 |
| complete_topology | 178.0 | 0.30 | 31.4 |
| ip_shuffle | 178.0 | 0.70 | 29.9 |
| os_diversity | 241.9 | 0.00 | 4.3 |
| service_diversity | 256.1 | 0.00 | 3.7 |
| random_multi | 256.1 | 0.00 | 10.9 |
| simultaneous_multi | 355.8 | 0.00 | 13.0 |
| alternative_multi | 256.1 | 0.00 | 12.1 |

**The unimpeded inherited attacker never crosses at any patience level** —
censoring 1.00 — while **every** MTD condition produces abandonment. That is a
complete separation, and it is the strongest evidence available that the
instrument measures what it claims: where there is real progress for a defence to
suppress, suppression shows up as disengagement.

## 4. Why C2 moved — the profiled attacker's collapse is not the defence's doing

On the profiled arm, abandonment effort is CI-disjoint from the no-MTD arm on
**2 of 5 profiles**, and the separating cells are isolated rather than systematic
(`pure_steal` at one budget, `infrastructure_setup` at two). C3 and C4 move for
the same reason: at k = 2 the eight conditions span 39 to 76 actions with **no
adjacent pair separating**, and at k = 5 they span 141 to 189 with none
separating either.

**The mechanism is legible and it is the same one this project has met before.**
The profiled attacker compromises 0.5 to 5 hosts against a target of 40, under
every condition including none. Its projected campaign effort is therefore
dominated by its own low progress rate rather than by anything the defence does
— the projection is enormous from the first action and stays enormous, so the
budget it crosses is set by its own rate, not by MTD's contribution to it. The
defence cannot be attributed a disengagement that would have happened anyway.

**This is the contrast the design predicted, and it mirrors the headline result.**
Experiment 2 found the defence *ranking* inverts between the two attackers; this
finds that the defence's *attributability* does too. A measure that registers MTD
against the inherited attacker and not against the profiled one is a statement
about what each attacker's failure is made of: the inherited attacker fails
because the defence stops it, and the profiled attacker fails because CTI-ordered
traversal fights the substrate's procedural order — the coupling finding, arrived
at through a third independent instrument.

**Per the stopping rule, nothing was re-specified.** No criterion was relaxed, no
budget chosen, no arm added after the fact.

## 5. Two honest corrections to the pre-registration

**The predicted degeneracy held on one arm and failed on the other, for a reason
worth recording.** §2.1 of the pre-registration predicted that every run must
abandon at action 1 when k = 1, because `T(1) = 1 + U` against a budget of `U`.
That holds exactly on the movement arm — every one of the 400 runs abandons at
action 1, censoring 0.00 in every condition. It **fails on the baseline arm**,
because that attacker begins with exposed endpoints already compromised, so
`h(1) ≥ 1` and its first projection is far below `U`. The prediction was correct
about the arithmetic and incomplete about the initial condition; the arm-specific
version is the one a successor should carry.

**A post-hoc observation, flagged as post-hoc and deliberately not acted on.**
C2's criterion tests the *mean abandonment effort among runs that abandon*, which
conditions on abandoning. The censoring fractions were not part of any criterion,
and they carry a signal the means do not: at k = 2 the no-MTD arm censors at
**0.40** while the MTD conditions censor at 0.08 to 0.20 — that is, MTD roughly
doubles or triples the *fraction* of runs that would disengage, without moving
*when* the survivors do. Whether that is the measure's real discriminating half is
a question for a fresh pre-registration, not a re-reading of this one. It is
recorded here because suppressing it would be worse, and acted on nowhere.

## 6. The frontier

Mean abandonment effort in actions, with the censoring fraction beside it —
never pooled, because a pooled mean understates every censored run.

| condition | k=1.25 | k=1.5 | k=2 | k=3 | k=5 | k=7.5 | k=10 |
|---|---|---|---|---|---|---|---|
| none | 9 / .02 | 37 / .06 | 67 / .40 | 104 / .74 | 141 / .86 | 229 / .94 | 317 / .98 |
| complete_topology | 9 / .00 | 19 / .02 | 39 / .10 | 82 / .24 | 171 / .30 | 249 / .46 | 317 / .66 |
| ip_shuffle | 9 / .00 | 19 / .02 | 39 / .12 | 88 / .24 | 173 / .34 | 249 / .46 | 317 / .66 |
| os_diversity | 12 / .00 | 30 / .02 | 76 / .14 | 95 / .46 | 162 / .66 | 317 / .82 | 317 / .96 |
| service_diversity | 9 / .02 | 22 / .04 | 64 / .20 | 105 / .44 | 163 / .68 | 295 / .84 | 317 / .94 |
| random_multi | 9 / .00 | 26 / .02 | 61 / .14 | 126 / .30 | 180 / .64 | 277 / .78 | 317 / .88 |
| simultaneous_multi | 9 / .00 | 19 / .02 | 44 / .08 | 92 / .18 | 172 / .32 | 257 / .44 | 317 / .62 |
| alternative_multi | 9 / .00 | 21 / .02 | 51 / .12 | 107 / .24 | 189 / .56 | 249 / .74 | 317 / .86 |

The reader picks their own reservation and reads off the answer; no declared
value is load-bearing anywhere in this table.

## 7. What this licenses, and what it does not

**Licensed.** The measure exists, is validated against an arm where the defence
demonstrably acts, is non-degenerate over its reporting axis, and is not a
re-expression of breadth. The finding that MTD's attributability differs between
the two attackers is licensed, and it is the third independent instrument to
locate the profiled attacker's failure in procedural coupling rather than in the
defence.

**Not licensed.** **No badge move** — axis 6 is closed as DESIGNED and this reader
scores an *outcome*, where that axis asks whether the attacker *conditions on*
cost. No ranking of mechanisms by disengagement (C3 moved; nothing separates). No
claim that MTD fails to induce disengagement *in general* — it plainly does, on
the inherited attacker. No attacker that actually stops: that build was gated on
this measure discriminating on the profiled arm, and it did not.

## 8. What a successor should do

**Not** re-specify C2 and re-run — the stopping rule exists because a measure
motivated by a defence's own economic claim is exactly where criteria drift.

The live question is §5's post-hoc observation: the censoring fraction moves
sharply with the defence where the conditional mean does not, which suggests the
measure's discriminating half is *whether* a run would disengage rather than
*when*. That is a different conclusion needing its own pre-registration, its own
criterion and its own null arm — and it should be written before it is looked at
again.

## Evidence

- [`attacker_disengagement_prereg.md`](attacker_disengagement_prereg.md) — the
  five conclusions and their criteria, committed before any reported row.
- `data/results/attacker_disengagement/` (untracked/regenerable) —
  `run_study.py`, `analyse.py` computing every verdict from the trajectories,
  `verdict.txt`, `verdicts.json`.
- `measures.py` §8 and its unit gate in
  `tests/l3_simulation/test_movement_measures.py` — hand-worked streams pinning
  the arithmetic, including first-crossing and censoring semantics.
- [`experiment_02_findings.md`](experiment_02_findings.md) §9 — the ranking
  inversion this record's arm contrast mirrors.
