---
status: durable
created: 2026-08-02
updated: 2026-08-02
topic: "L3 criterion axis 7 — the pre-registration for the progress-credit sweep: seven arms, the decision cell named in advance, five conclusions with their predicted signs (two committed against the repair), the seed count from an explicit power calculation, and the stopping rule"
---

# Pre-registration — the progress-credit sweep

**Committed before a single row exists.** Nothing below may be re-specified once
output is on disk. The mechanism it tests is
[`progress_credit.md`](progress_credit.md); the rubric it scores against is
[`learning_mechanism_feasibility.md`](learning_mechanism_feasibility.md) §6.

The discipline is the one the iterated cost model set and honoured: conclusions
and criteria fixed in advance, every one reported whatever it does, and a
stopping rule that forbids adding an arm or relaxing a bar after the fact. This
axis has a specific reason to need it — a post-hoc lead already exists in the
readiness sweep (§5 of the study), and pre-registering the arm that would test it
is the only legitimate way to use it.

## 1. Why the seed count changed, and why that is not scoring-driven design

Every prior sweep ran **ten** seeds. From `4.60 ± 0.73` at n = 10, σ ≈ 1.18, so
detecting a 0.7-host difference (~15 %) at 80 % power needs roughly **45 seeds
per arm**. Four successive sweeps have failed to separate adjacent arms, which is
a power failure rather than four findings about mechanisms.

**This sweep runs n = 50.** Raising *n* on an unchanged metric does not change
what is measured — it gives an unchanged measure the power to discriminate — and
under S6 it is arguably obligatory rather than merely permitted. The grid is
*concentrated*, not widened: no new parameter values are explored, and the κ
sweep of the prior study is deliberately not repeated.

## 2. Arms — seven, fixed

All at κ = 1.0 (the declared capability) except the ablation. Overlay
`v3_persistent_backward`, horizon 15 000, MTD interval 200 s.

| # | label | what it is | why it is here |
|---|---|---|---|
| 1 | `ablation` | κ = 0 | the badge's comparator; key- and credit-independent by construction |
| 2 | `control_asymptotic` | declared bias, `q_ready` = 0.85, `q_unready` = 0.001 | C3: the pooled measured regime rates, not-ready at its Laplace-positive limit |
| 3 | `control_matched` | declared bias, `q_ready` = 0.85, `q_unready` = 0.06 | C3 at the learner's *observed* aggression, so the comparison is about learning and not about how hard the arm suppresses |
| 4 | `acceptance_r50` | shipped rule, ρ = 0.5 | the historical control — this is the mechanism on record |
| 5 | `progress_r50` | new rule, ρ = 0.5 | **the arm under test** |
| 6 | `acceptance_r00` | shipped rule, ρ = 0 | the C2 contrast, held constant across credit rules |
| 7 | `progress_r00` | new rule, ρ = 0 | the C2 contrast under the new rule |

Two declared-bias controls rather than one, because a single one confounds the
question. `control_asymptotic` is what the declared inputs actually imply;
`control_matched` holds suppression strength near the learner's own measured
not-ready belief (0.069–0.333, audit §8b) so that a difference cannot be
attributed to the control simply being more aggressive. Their two constants are
**arguments owned by this pre-registration**, not declared values of the model.

**Cells.** Both mappings (`v1_ckc_total`, `v2_partial`) × both MTD conditions
(none, random @200 s) × all five profiles × 50 seeds = **7 000 runs**.

**The decision cell is named in advance: `v2_partial`.** It is the mapping under
which the attacker compromises hosts at all, and it is the cell the prior
pre-registration used. `v1_ckc_total` is reported as a generality check and
carries no gate. The MTD-condition ambiguity has bitten this axis twice; every
conclusion below states its condition explicitly.

## 3. Conclusions, with predicted signs

Primary measure throughout is **distinct hosts compromised** (breadth).
`advanced_after_first_success` is **prospectively excluded from every gate** — it
is a boolean per run, saturates at 0.960–0.980 on `v2_partial`, and returns
identical values for mechanisms differing 34 % on breadth. It is reported, never
gated on, on the axis-6 precedent that a statistic which cannot discriminate
cannot move a badge. Separation means non-overlapping 95 % CIs (mean ± 1.96·SEM,
the project's convention), pooled over profiles unless stated.

**U1 — the badge gate.** `progress_r50` beats `ablation` on breadth, `v2_partial`,
**reported at both MTD conditions**.
*Predicted: HELD under no-MTD, and I expect no separation.* The credit rule fixes
what the attacker optimises; it does not widen the six-verb action vocabulary it
optimises within. **This is committed against the repair.**

**U2 — the credit repair, like for like.** `progress_r50` beats `acceptance_r50`
on breadth, `v2_partial`, both MTD conditions. This is the comparison that
isolates the credit rule with everything else held identical.
*Predicted: MOVED — progress > acceptance.* This is the conclusion the build was
aimed at; if it fails, the repair does not work and that is the finding.

**U3 — C3, non-degeneracy.** `progress_r50` differs from **both** controls, on
breadth **and** on the realised transition distribution (Jensen–Shannon
divergence over the pooled `transitions` tally). Both halves must hold; agreeing
with either control on both measures fails the criterion.
*Predicted: differs.* **This is the conclusion most likely to fail, and it is the
one an examiner asks first.**

**U4 — C1, the instrument quantity.** `I = [P(no-MTD) − P(MTD)]_mech −
[P(no-MTD) − P(MTD)]_abl` on breadth, `v2_partial`, for `progress_r50`.
*Predicted sign: I < 0 — MTD's measured effect is **smaller** against the
learning attacker than against the memoryless one*, continuing the direction of
the unseparated point estimate already on record (30.9 % → 37.6 % breadth
retained). Reported whether it separates or not, and **never substituted for U1**.
A robust negative I is the thesis result in its strongest form: greater attacker
fidelity implies current MTD evaluations overstate MTD's benefit.

**U5 — C2, type-disciplined forgetting.** ρ = 0 beats ρ = 0.5 under the **same**
credit rule, `v2_partial`, under **MTD only** (with no MTD the rule never fires,
so the arms are identical by construction and the comparison is vacuous).
*Predicted: MOVED for both credit rules — ρ = 0 better.* The belief is a
tradecraft object and the literature holds that MTD cannot destroy tradecraft.
**This is the pre-registration of the post-hoc lead in study §5, which is the only
legitimate way to use it. A ρ ruling is Marc's and this conclusion does not
pre-empt it — it supplies the evidence the ruling would rest on.**

## 4. Stopping rule

- Every conclusion above is reported with its verdict (MOVED / HELD), whatever it
  is, in a findings record that cites this file.
- **No arm is added, no criterion relaxed, no cell re-chosen, and no measure
  substituted after rows exist.** If U2 fails, the repair failed; the response is
  to record that, not to find a cell where it did not.
- Post-hoc observations are permitted **only** when labelled as leads for a fresh
  pre-registration, never as verdicts — the treatment study §5 gave the readiness
  lead.
- The badge decision is taken in the findings record, on U1, and nowhere else.
- No composition with axis 6's factor 7A/AB: the joint-composition bar in
  [`modulator_composition.md`](modulator_composition.md) §2 is untouched by this
  sweep and no arm here crosses it.

## 5. What a result cannot license, whatever it says

- **No reported-configuration change.** The headline arm runs modulators null and
  `ACCEPTANCE` stays the modulator's default regardless of outcome; a
  modulator-active arm is reported as its own labelled arm with its own plurality
  figure ([`model_scope_freeze.md`](model_scope_freeze.md) §4).
- **No re-reading of any recorded experiment.** The readiness sweep, the frontier
  and experiment 2 stand as records of the model they ran under.
- **No claim about the attacker being a better adversary in general.** The
  substrate, mapping, defence family and horizon are all fixed here.
- **No axis-4 claim.** Responding to the substrate's procedural order is not
  adaptivity to the defender, and conflating them is the embellishment the freeze
  exists to prevent.

## 6. Evidence layout

`data/results/progress_credit/` (untracked/regenerable): `run_sweep.py` carrying
these criteria in its docstring, `analyse.py` computing every verdict from the
rows, `runs.jsonl`, `verdict.txt`. The findings record that cites this file is
`progress_credit_findings.md`.
