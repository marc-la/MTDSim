---
status: durable
created: 2026-08-06
topic: "The duty-cycle study — the kill criterion fired. Which attacker looks stealthier flips entirely on how the baseline's exploit attempts are counted, so the tempo comparison cannot be made on this substrate until the S3-R pricing asymmetry is resolved. The one thing that did settle: the result is timing, not the tactic ranking"
---

# Detectability as a duty cycle — the comparison is not robust, and the kill criterion says so

**Status:** durable results record. It discharges the duty-cycle study.
Conclusions and criteria were fixed in
[`stealth_dutycycle_prereg.md`](stealth_dutycycle_prereg.md) and committed
(`59f4e28`) before the ruled configuration was computed, with a full disclosure
(§0 there) of which numbers were already visible.

**The headline. D4 — the kill criterion — FIRED, and it fired cleanly.** The
whole arm-versus-arm verdict **reverses** depending on whether the inherited
attacker's exploit attempts are counted as one invocation or as the 15–18
per-vulnerability events the substrate actually spreads across simulated time.
Counted as invocations, the baseline is the arm that returns to the floor and the
profiles are the ones that stay elevated. Counted as the substrate prices them,
the reverse: all five profiles sit above the baseline. **Both readings are
defensible and they disagree completely**, so the finding is a property of the
granularity choice, not of the two attackers.

That is exactly the confound the criterion was written to isolate, and it is the
S3-R pricing asymmetry: the baseline charges each vulnerability its own exploit
time while the movement arm, running the identical loop with `charge_time=False`,
lands all of its attempts at a single instant.

**One thing did settle, and it is the study's real gain.** Under D5 the verdict is
**unchanged at `ρ = 1`**, where every invocation scores identically. Whatever the
answer turns out to be, it is a **timing** result and not an artefact of the
tactic ranking — which is precisely what could not be said of the first study,
whose entire outcome was carried by the increment term.

## 1. What changed since the first study

Two rulings (Marc, 2026-08-06), both now in the declared family:

- **R1 — the increment fires on a tactic's invocation of a verb.** A dwell-only
  visit contributes elapsed time and no increment. The first study scored every
  visit, which put 56–62 % of four profiles' exposure on tactics the simulator
  never executes. Under R1 those tactics become what the low-and-slow argument
  always wanted them to be: **silence, during which the level decays**.
- **R2 — verb-level tiers across arms, tactic-level within.** Every arm-versus-arm
  figure below is scored with both sides on one identical verb-level rule, so a
  cross-arm difference **can only be *when*, never *what***.

And the two statistics the first study reported were retired for this question,
because both are provably blind to spacing: `mean_exposure` samples `D` only at
the top of every spike, and `time_average_exposure` satisfies `∫D dt = τ·Σd`
exactly (verified at ratios 0.9933–1.0000), making it a rate wearing a decay
costume.

**R1 also makes the arms genuinely comparable in size**, which the first study's
configuration did not:

| | visits in stream | **invoking** (scored) |
|---|--:|--:|
| double_extortion | 463.3 | 262.2 |
| pure_impediment | 464.8 | 280.5 |
| aggregate | 490.2 | 293.8 |
| pure_steal | 508.4 | 318.6 |
| **baseline** | **371.3** | **371.3** |
| infrastructure_setup | 674.2 | 571.5 |

The baseline now sits mid-pack rather than at one end.

## 2. Verdicts

50 movement runs (5 profiles × 10 seeds, `v2_partial`, retrace on, **no MTD**)
and 10 baseline runs — the same recorded corpus the first study used. No
re-simulation: both rulings and every declared parameter are read off the stream.

| | Conclusion | Verdict |
|---|---|---|
| **D1** | the duty-cycle statistic is non-degenerate across profiles | **held** — 3 of 4 adjacent pairs CI-disjoint, max/min 2.73 |
| **D2** | the prediction — the profiles return to the floor and the baseline does not | **MOVED** — 0 of 5 profiles above the baseline, in every τ cell |
| **D3** | the level claim — a typical moment is quieter under the profiles | **MOVED** |
| **D4** | **KILL CRITERION** — not an artefact of the S3-R granularity | **FIRED** — the verdict flips with the granularity |
| **D5** | the ranking is not doing the work | **held** — same verdict at `ρ = 1` |

## 3. D2 and D4 — the flip

`p90/p50` of `D` over time, cross-arm at verb-level tiers. Higher means the level
comes back to the floor between actions.

**Baseline counted as invocations (the primary unit):**

| τ | baseline | pure_steal | pure_imped | double_ext | infra_setup | aggregate | profiles above? |
|--:|--:|--:|--:|--:|--:|--:|:--|
| 60 | **4.03** | 2.45 | 2.57 | 2.96 | 2.27 | 2.59 | 0 of 5 |
| 240 | **1.84** | 1.60 | 1.60 | 1.77 | 1.53 | 1.64 | 0 of 5 |
| 960 | **1.44** | 1.26 | 1.25 | 1.33 | 1.23 | 1.30 | 0 of 5 |

**Baseline counted as the substrate prices it (per-vulnerability):**

| τ | baseline | profiles above? |
|--:|--:|:--|
| 3.75 | 10.92 | **5 of 5** |
| 15 | 2.32 | **5 of 5** |
| 60 | 1.58 | **5 of 5** |
| 240 | 1.25 | **5 of 5** |
| 960 | 1.17 | 3 of 5 |

The direction reverses completely. Under the first counting the inherited
attacker is the bursty one — long exploit invocations with real silence between
them; under the second it is the steady one — a near-continuous drumbeat of
individual attempts that never lets the level fall.

**Neither counting is wrong, and that is the problem.** One invocation is the
like-for-like unit, because the movement arm's dispatch runs the same
vulnerability loop internally. Per-vulnerability is what the substrate actually
puts on the clock. The movement arm **cannot** express the second, because S3-R
took the per-vulnerability pricing off that arm — so the comparison is not
between two attackers, it is between two pricing regimes.

## 4. A defect in the pre-registered primary, reported rather than swapped out

`p90/p50` is **numerically degenerate wherever the attacker is silent for most of
the run**, which at a short decay constant is the normal case: it divides by a
quantile going to zero and returns 627 at τ = 15 and 4 × 10¹³ at τ = 3.75. Only
the τ ∈ {60, 240, 960} cells are meaningful, and §3 reports those.

**It was not replaced.** The stopping rule forbids re-specifying after the fact,
and swapping in a better-behaved statistic once the pre-registered one had
embarrassed itself is exactly the drift it exists to prevent. What §5 reports
instead is the **quiet-fraction frontier, which was pre-registered alongside it**
as the reporting axis and is bounded by construction. The degeneracy is now
pinned by a unit test so a successor meets it as a documented property rather
than as a surprise.

The verdicts are unaffected: D2's and D4's directions are identical in the
well-behaved cells and in the degenerate ones.

## 5. The quiet-fraction frontier — and it crosses

Fraction of the run with `D` below θ × that run's own peak. The threshold is a
reporting axis, never a declared value.

| | θ=0.01 | θ=0.02 | θ=0.05 | θ=0.10 | θ=0.25 |
|---|--:|--:|--:|--:|--:|
| **baseline** | **0.524** | **0.558** | 0.610 | 0.671 | 0.816 |
| pure_steal | 0.391 | 0.474 | 0.611 | 0.739 | 0.917 |
| pure_impediment | 0.436 | 0.509 | 0.626 | 0.735 | 0.898 |
| double_extortion | 0.485 | 0.562 | 0.682 | 0.787 | 0.929 |
| infrastructure_setup | 0.304 | 0.381 | 0.512 | 0.642 | 0.865 |
| aggregate | 0.435 | 0.513 | 0.639 | 0.754 | 0.919 |

**The ordering inverts across the frontier, at about θ = 0.05.** At a tight
threshold the inherited attacker is quiet for more of the run than any profile;
at a loose one every profile but `infrastructure_setup` is quieter than it. The
two arms differ in the *shape* of their quiet, not in its amount: the baseline has
more **deep** silence, the profiles more **shallow** quiet. A single declared
threshold would have picked whichever answer it happened to sit on — which is why
the frontier was pre-registered instead of a value.

## 6. D1 and D5

**D1 held.** Between profiles, at tactic-level tiers, `p90/p50` runs 6.82
(`infrastructure_setup`) to 18.62 (`double_extortion`) — max/min 2.73, with three
of four adjacent pairs CI-disjoint. The statistic discriminates *within* the
movement arm, where there is no cross-arm pricing asymmetry to confound it. This
is the one comparison in the study that is not bracketed by §3's flip.

**D5 held, and it is the study's real gain.** At `ρ = 1` every invocation scores
identically, so the curve is pure event timing — and D2's verdict is unchanged.
Whatever this comparison eventually says, it is a timing statement. The first
study could not claim that: its entire result came from the increment term, and
its arms did not separate on tempo at all.

## 7. What this licenses, and what it does not

**Licensed.** The rulings are implemented and gated. `D1` supports a between-
profile duty-cycle comparison. And the strongest claim here is a **methodological
negative**: on this substrate, a tempo or stealth comparison **between the
inherited and profiled attackers cannot be made** without first resolving the
per-vulnerability pricing asymmetry, because the answer flips on it. That is a
finding about the evaluation, not about either attacker, and it is the kind this
project's Row B already trades in.

**Not licensed.** No badge move — axis 5 stays **NOT ADDRESSED**; this is still a
reader. No claim that the profiled attacker is stealthier, and none that it is
not. No claim over the ranking's full range: R1 narrows the movement arm's
realised tiers to **1–3**, so tier 0 and tier 4 are unreachable and nothing here
evidences the ranking's extremes. Nothing about the first study's E1–E5, which
were scored against a different instrument.

## 8. What a successor should do

**Not** re-specify D2 and re-run. The stopping rule fired and was honoured: no
criterion relaxed, no band re-centred, no statistic swapped after it failed.

**The one thing that would settle it** is not another statistic — it is removing
the confound. Either price the movement arm's exploit attempts per vulnerability
as the substrate does (an S3-R change, and a large one: it would move every
movement-arm timing figure on record), or accept that the two arms' event streams
are not comparable at sub-invocation granularity and confine tempo claims to
**within-arm** comparisons, where D1 shows the instrument works. **Recommend the
second**, and recommend it be ruled rather than inherited.

**Two dispositions carried forward from the first study are now sharper.** The
dwell-only convention is settled by R1 and needs no further ruling. The
per-vulnerability row count is no longer only a bookkeeping question about
`baseline_ledger` — it is the axis this study's verdict turns on, which raises its
priority.

## 9. Evidence

- [`stealth_dutycycle_prereg.md`](stealth_dutycycle_prereg.md) — the five
  conclusions, their criteria, and the disclosure of what was already visible.
- [`stealth_exposure_metric.md`](stealth_exposure_metric.md) — the first study,
  now carrying a superseding banner for its scoring convention.
- `data/ogasp/movement/exposure_rules.json` — R1 and R2 in the declared family.
- `data/results/stealth_exposure/` (untracked/regenerable) —
  `analyse_dutycycle.py` computing every verdict, `verdict_dutycycle.txt`,
  `verdicts_dutycycle.json`; `duty_cycle.py` and `why_inverted.py` the
  post-hoc diagnostics that prompted the study.
- `measures.py` §9b and `tests/l3_simulation/test_movement_measures.py` — the
  duty-cycle summaries, the proof that the time-average is a rate, and the pinned
  degeneracy of `p90/p50`.
