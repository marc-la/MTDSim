---
status: durable
created: 2026-08-02
updated: 2026-08-02
topic: "L3 criterion axis 7 — the progress-credit sweep: 7 000 runs, all five pre-registered conclusions not confirmed, two refuted in the opposite direction, and the one large separated effect sitting outside the gated cell as a lead"
---

# The progress-credit sweep — five conclusions, none confirmed, and where the result actually is

**Status:** durable findings record. Criteria fixed in
[`progress_credit_prereg.md`](progress_credit_prereg.md) §3 before a single row
existed; the mechanism is [`progress_credit.md`](progress_credit.md). 7 000 runs,
seven arms, 50 seeds, both mappings, both MTD conditions, five profiles.

**Headline: the badge does not move, and four of the five conclusions failed in
ways worth more than a pass would have been.** Two were refuted in the direction
opposite to their prediction, one of them with CI separation. The stopping rule
was honoured — nothing re-specified, no arm added, no criterion relaxed, no cell
re-chosen.

## 0. A terminology correction, stated first so nothing below is misread

The pre-registration used **MOVED** to mean *the conclusion was confirmed*. That is
the **opposite** of this project's established idiom, where "U2 is recorded moved"
([`iterated_cost_model.md`](iterated_cost_model.md)) means the conclusion was *not*
confirmed. The criteria themselves are unchanged and were never touched; only the
labels were wrong. This record and `analyse.py` therefore use **CONFIRMED / NOT
CONFIRMED** throughout, which cannot be read backwards.

## 1. The table

Distinct hosts compromised, mean ± 1.96·SEM, n = 250 per cell (50 seeds × 5
profiles).

### `v2_partial` — the decision cell, named in advance

| arm | no MTD | random MTD @200 s |
|---|--:|--:|
| ablation | 4.11 ± 0.31 | 1.21 ± 0.16 |
| control_asymptotic | 3.67 ± 0.34 | 1.57 ± 0.21 |
| control_matched | 4.24 ± 0.30 | 1.51 ± 0.18 |
| acceptance_r50 | 4.19 ± 0.34 | 1.32 ± 0.18 |
| **progress_r50** | **4.54 ± 0.39** | **1.49 ± 0.19** |
| acceptance_r00 | 4.19 ± 0.34 | 1.22 ± 0.21 |
| progress_r00 | 4.54 ± 0.39 | 1.06 ± 0.18 |

### `v1_ckc_total` — generality check, carries no gate

| arm | no MTD | random MTD @200 s |
|---|--:|--:|
| ablation | 0.44 ± 0.08 | 0.41 ± 0.11 |
| control_asymptotic | 0.72 ± 0.08 | 2.98 ± 0.48 |
| control_matched | 0.68 ± 0.08 | 1.60 ± 0.33 |
| acceptance_r50 | 0.47 ± 0.07 | 0.61 ± 0.16 |
| **progress_r50** | **1.70 ± 0.29** | 0.54 ± 0.14 |
| acceptance_r00 | 0.47 ± 0.07 | 1.40 ± 0.30 |
| progress_r00 | 1.70 ± 0.29 | 1.31 ± 0.24 |

A sanity check the design predicts and the data honours: with no MTD the ρ arms
are **identical** (4.19/4.19 and 4.54/4.54), because the forgetting rule never
fires without an interrupt.

## 2. The five verdicts

**U1 — the badge gate. NOT CONFIRMED, as predicted.** `progress_r50` 4.54 ± 0.39
against ablation 4.11 ± 0.31: the direction favours the mechanism at both MTD
conditions and the intervals overlap at both. **The badge stays DESIGNED.** This
was the conclusion committed against the repair, and it landed where it was
predicted to.

**U2 — the credit repair, like for like. NOT CONFIRMED.** `progress_r50` 4.54
against `acceptance_r50` 4.19 (no MTD), 1.49 against 1.32 (MTD). Direction favours
progress in **8 of 10** profile × MTD cells, and neither pooled comparison
separates. This was the conclusion the build was aimed at. **It missed its own
bar, and that is the result.** A consistent 8-of-10 direction at an effect size
this small is a power statement, not a mechanism statement, and the honest reading
is that the repair does something on this mapping too small to establish at 50
seeds.

**U3 — non-degeneracy. NOT CONFIRMED, and this is the uncomfortable one.** The
mechanism separates cleanly from `control_asymptotic` (4.54 vs 3.67, JSD 0.2804)
and **does not separate from `control_matched`** (4.54 vs 4.24, JSD 0.1196). Both
halves were required. Running two controls rather than one is what produced the
finding: against a declared static bias *matched to the learner's own observed
aggression*, the accumulated evidence buys no distinguishable behaviour on this
mapping. **On the criterion an examiner asks first — is this learning, or a lookup
with extra steps — the answer here is not yet established.**

**U4 — the instrument quantity. Sign opposite to prediction.**
`I = +0.15` for `progress_r50` (predicted `I < 0`). MTD's measured *absolute*
effect is marginally **larger** against the learner, not smaller. Note the two
readings differ and both are reported: on retained fraction the learner holds
32.8 % against the ablation's 29.4 %, which is the direction predicted, while on
absolute host loss it is 3.05 against 2.90, which is not. The point estimates are
close together and none of this is separated. **The prediction is recorded as
wrong on its own stated measure.**

**U5 — type-disciplined forgetting. REFUTED, with separation, in the opposite
direction.** Predicted ρ = 0 better on the argument that the belief is tradecraft
and MTD cannot destroy tradecraft. Measured on the decision cell under MTD:
`progress_r00` **1.06 ± 0.18** against `progress_r50` **1.49 ± 0.19** —
**CI-disjoint, and forgetting is better**. The acceptance rule shows the same sign
unseparated (1.22 vs 1.32).

This kills the C2 recommendation of
[`learning_mechanism_feasibility.md`](learning_mechanism_feasibility.md) as
stated, and the mechanism is legible: a learner that never forgets becomes
confidently committed to a policy the defence has already invalidated, and the ρ
decay is what restores exploration after a mutation. The literature argument —
that tradecraft is durable — is about what an *operator* retains; it does not
follow that a within-run frequency estimate keyed on tactic-places is the right
object to make durable. **The argument was good and the object it was applied to
was wrong.** Had the ρ ruling been taken on the earlier reasoning it would have
been taken incorrectly.

## 3. The two leads — labelled as leads, not verdicts

**Lead 1 — the effect is large and separated on the mapping the gate does not
cover.** On `v1_ckc_total` with no MTD, `progress_r50` reaches **1.70 ± 0.29**
against ablation **0.44 ± 0.08** and acceptance **0.47 ± 0.07** — CI-disjoint
against both, a ~3.6× improvement, and the *only* separated positive result in the
sweep. `v1_ckc_total` is the mapping that runs at 60–98 % blocked, i.e. the one
where the CTI-derived order and the substrate's procedural order disagree most.

The coherent reading — **and it is a hypothesis, not a finding** — is that
progress credit pays in proportion to how badly the two orders mismatch: where the
substrate barely obstructs the attacker there is little for a corrected credit
signal to recover, and where it obstructs heavily there is a great deal. That is
directly a claim about porting behaviourally-grounded attackers onto procedurally
rigid substrates, which is the thesis's own subject. **It carries no gate by
pre-registration and must not be reported as a badge argument.** It needs its own
pre-registration with `v1_ckc_total` named as the decision cell in advance.

**Lead 2 — the ρ lead from the readiness sweep was mapping-specific, and
pre-registration caught it.** [Study §5](learning_mechanism_feasibility.md)
identified ρ = 0 as the only cell where a learner beat the ablation with
separation, on `v1_ckc_total` under MTD. That replicates here (acceptance 1.40 vs
0.61; progress 1.31 vs 0.54) **and reverses on the decision cell** (progress 1.06
vs 1.49). Naming `v2_partial` in advance is precisely what prevented a
mapping-specific artefact from being adopted as a declared-value change. This is
the strongest available argument for the pre-registration discipline itself.

## 4. Profile heterogeneity, and a watch item that fired

`v2_partial`, no MTD, per profile:

| profile | ablation | acceptance | progress |
|---|--:|--:|--:|
| aggregate | 6.14 | 6.16 | 7.00 |
| pure_impediment | 4.74 | 5.06 | **6.84** (disjoint vs ablation) |
| pure_steal | 4.30 | 4.40 | 4.96 |
| double_extortion | 1.96 | 1.46 | 1.90 |
| **infrastructure_setup** | 3.40 | 3.88 | **2.02** |

Progress credit helps four profiles and **hurts `infrastructure_setup` badly**.
That is watch item 2 of [`progress_credit.md`](progress_credit.md) §3 firing
exactly where it was flagged before the sweep ran: the pivot (`lateral-movement` /
`ENUM_HOST`) held a belief of 0.138 in the pre-sweep demonstration on this very
profile, and suppressing the pivot closes the campaign early. The watch item was
recorded in advance, which is why this is diagnosable rather than mysterious.

The pooled `v2_partial` result is therefore an average over a mechanism that
helps most profiles and harms one; the pooled figure conceals a real interaction.

## 5. What this licenses, and what it does not

**Licensed.** That the badge stays DESIGNED on U1. That the credit repair's
direction favours it in 8 of 10 cells without separating on the decision cell.
That the mechanism is not distinguishable from an aggression-matched declared bias
on `v2_partial` (U3). That ρ = 0 is *worse* than ρ = 0.5 on the decision cell under
MTD, with separation, for the progress rule — and that the C2 type-discipline
recommendation is therefore withdrawn as stated. That the pre-sweep watch item on
the pivot was correct.

**Not licensed.** **No badge move.** No claim from the `v1_ckc_total` result — it
carries no gate and is a lead requiring its own pre-registration. No
reported-configuration change: the headline arm still runs modulators null and
`ACCEPTANCE` remains the modulator's default. No ρ re-declaration — U5 is evidence
for a ruling, and the ruling is Marc's. No re-specification of U2 and re-run: the
stopping rule fired, and a repair motivated by a published defect is exactly the
circumstance in which criteria drift. No composition with axis 6's factor 7A/AB;
that bar is untouched.

## 6. What a successor should do, in priority order

1. **Pre-register the `v1_ckc_total` cell and re-run.** It holds the only
   separated positive effect in 7 000 runs, and the mismatch-proportional
   hypothesis in §3 is directly testable — the prediction is that the effect
   scales with the mapping's blocked fraction.
2. **Fix the pivot, then re-test U2.** `infrastructure_setup` is the one profile
   the mechanism harms, and the cause was identified before the sweep. Crediting
   the pivot properly is a mechanism question, not a tuning one.
3. **Do not adopt ρ = 0.** U5 refuted it with separation on the decision cell.
4. **Treat U3 as the open question it is.** Whether the accumulated belief buys
   anything a matched static bias does not is now the axis's live problem, and it
   is a better-posed problem than "does the attacker win".

## 7. Evidence

- [`progress_credit_prereg.md`](progress_credit_prereg.md) — the criteria,
  committed before any row existed.
- [`progress_credit.md`](progress_credit.md) — the mechanism, and §3's watch items,
  one of which fired.
- `data/results/progress_credit/` (untracked/regenerable) — `run_sweep.py`
  carrying the criteria in its docstring, `analyse.py` computing every verdict
  from the rows, `runs.jsonl` (7 000), `verdict.txt`.

## 8. Addendum (2026-08-02) — which of these negatives are real, and which are the instrument

Added after the verdicts above were recorded. **Nothing in §2 is re-graded.** The
pre-registered criterion was non-overlapping 95 % CIs on arm means, that criterion
was applied, and those verdicts stand as this sweep's record. What follows asks a
different and legitimate question — *are these negatives measuring the mechanism or
the measurement?* — and its answers are **leads for a fresh pre-registration**, never
substitutes for §2.

### 8.1 The arms share seeds, and the convention discards it

Every arm runs the same 50 seeds against the same profiles, differing only in the
modulator. The difference between two arms on a given (profile, seed) is therefore
a **paired** observation, and comparing arm means with independent CIs throws that
pairing away. On this sweep it costs a factor of **2.0 in variance**
(unpaired SDs 3.14 and 2.47; paired SD of the difference 2.86).

Pooling over profiles compounds it: the ablation's within-profile SDs are
1.44–2.50 while its pooled SD is 2.47, because profile means span 1.96 to 6.14
hosts. The pooled comparison is being asked to detect a ~0.4-host effect through
variance that is mostly *between-profile* and cancels exactly under pairing.

### 8.2 Paired differences (same seed, same profile), reported as leads

Positive favours the first arm; **separated** means the 95 % CI on the difference
excludes zero.

| mapping | MTD | comparison | paired difference | |
|---|---|---|--:|---|
| `v2_partial` | none | progress vs **ablation** | **+0.436 ± 0.354** | **separated** |
| | none | progress vs acceptance | +0.352 ± 0.377 | — |
| | none | progress vs control_matched | +0.304 ± 0.357 | — |
| | random | progress vs **ablation** | **+0.284 ± 0.207** | **separated** |
| | random | progress vs control_matched | −0.016 ± 0.232 | — |
| `v1_ckc_total` | none | progress vs **ablation** | **+1.260 ± 0.245** | **separated** |
| | none | progress vs **acceptance** | **+1.236 ± 0.272** | **separated** |
| | none | progress vs **control_matched** | **+1.024 ± 0.251** | **separated** |
| | random | progress vs control_matched | **−1.064 ± 0.246** | **separated (control better)** |

### 8.3 So which negatives were false?

- **U1 is a probable false negative.** Paired, the mechanism beats its ablation on
  the decision cell at **both** MTD conditions. The unpaired verdict is not wrong —
  it is the criterion that was set — but the criterion could not see an effect the
  data contains. **This does not move the badge**: a badge cannot be taken on an
  analysis chosen after the rows existed. It is the single strongest argument for
  re-running with paired analysis pre-registered.
- **U2 is genuinely borderline.** +0.352 ± 0.377 paired — still not separated, still
  8 of 10 in direction. Underpowered rather than absent.
- **U3 is a true negative on `v2_partial` and passes on `v1_ckc_total`.** Against the
  aggression-matched control the mechanism is indistinguishable on `v2` (+0.304 ±
  0.357; −0.016 under MTD) and clearly separated on `v1` (+1.024 ± 0.251). **The
  "is it learning?" question has a mapping-dependent answer**: the accumulated
  belief buys nothing a static declared bias does not where the substrate barely
  obstructs, and buys a great deal where it obstructs heavily. That is the §3
  mismatch-proportional hypothesis arriving independently on the criterion that was
  designed to be failable.
- **U4 is a measure-definition problem, not a detection one.** The absolute and
  retained-fraction readings disagree in sign; the pre-registration named only one.
- **U5 is a true negative and stands unchanged.** It separated *against* its
  prediction on the pre-registered criterion, and pairing does not rescue a
  refutation. Do not adopt ρ = 0.

### 8.4 The implication reaches past this sweep

**Four successive sweeps on this project have failed to separate adjacent arms at
ten seeds, and all of them compared arm means with independent CIs while running
shared seeds.** Some part of that history may be instrument rather than mechanism.
This is a lead about the project's measurement convention, not a re-reading of any
recorded experiment — every prior verdict stands as the record of the criterion it
was taken under. What it earns is a **pre-registered paired analysis in the next
sweep**, and a note in the criterion doc that a pooled unpaired comparison over
heterogeneous profiles is a weak instrument for a small effect.
