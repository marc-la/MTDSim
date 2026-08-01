---
status: durable
created: 2026-08-01
updated: 2026-08-01
topic: "Pre-registration for the readiness-keyed learner sweep — the conclusions, their criteria and the badge gate, committed before a single sweep run exists; plus the joint-composition check the three modulator families have never had"
---

# Pre-registration — the readiness-keyed learner sweep, and the joint-composition check

**Status:** pre-registration. Every conclusion below, with its criterion, is
written and committed **before any sweep output exists**. This is the discipline
the three prior sweeps established
([`weight_sensitivity_study.md`](weight_sensitivity_study.md),
[`incentive_rationality.md`](incentive_rationality.md),
[`learning_capability.md`](learning_capability.md) §6) and the only thing that
makes a verdict falsifiable rather than a reading of the numbers. The findings
record reports against these criteria **as written**, whichever way they fall.

The mechanism being swept is Part B of the procedural-rigidity handoff: the
axis-7 learner re-keyed from `(destination tactic)` to
`(destination tactic, precondition-satisfied?)`, argued in
[`learning_representation.md`](learning_representation.md). Nothing else changes —
same estimator, same declared (κ, ρ) family and bands, same composition, same
forgetting rule.

## 1. The sweep

| | |
|---|---|
| **swept** | κ over its declared band {0, 0.5, 1, 2, 4}, ρ over its declared band {0, 0.25, 0.5, 1} — the *same* bands as the destination-only sweep, deliberately, so the two studies are comparable arm for arm. No new value family is declared (§4) |
| **sampling** | the destination-only sweep's 12 points exactly: the declared point (1, 0.5); κ ∈ {0, 0.5, 2, 4} at ρ = 0.5; ρ ∈ {0, 0.25, 1} at κ = 1; corners (0.5, 0), (0.5, 1), (4, 0), (4, 1). κ = 0 makes ρ inoperative, so the ablation arm runs once |
| **arms** | **three**, and this is the design's one addition: the readiness-keyed learner, the destination-only learner at the same point, and the shared κ = 0 ablation. The middle arm is what makes "the generalisation did something" separable from "learning did something" |
| **mappings** | both registered controller mappings — `v1_ckc_total` (experiment 1's, where the friction failure mode lives and where the declared readiness bit is exact) and `v2_partial` (experiment 2's, where the attacker compromises hosts and where the bit runs at 92–94 %) |
| **overlay** | `v3_persistent_backward`, as the destination-only sweep used |
| **matrix** | 12 points × 2 keys × 2 mappings × 5 profiles × {no MTD, random-multi @ 200 s} × 10 seeds, minus the shared ablation — the same shape and horizon (15 000 s) as every prior sweep, so the arms are comparable |
| **not powered for** | any ordering of profiles by progress. Three independent sweeps have now failed that conclusion at ten seeds; it is not attempted |

## 2. The conclusions, each with its criterion fixed in advance

- **R1 — the readiness key raises compromise breadth against its own ablation
  arm.** *This is the axis's substantive claim and the badge gate.* Criterion: on
  `v2_partial` (the mapping where the attacker compromises hosts at all), the mean
  distinct hosts at the declared (κ = 1, ρ = 0.5) is **higher** than at κ = 0, and
  higher than the destination-only learner's at the same point. HELD if both;
  MOVED otherwise. *The destination-only learner's breadth fell 6.5 → 5.6 at this
  point and 6.5 → 0.8 at κ = 4; if the generalisation does not reverse that, it
  has not fixed what it was built to fix, and that verdict is reported rather than
  explained away.*
- **R2 — the collapse at high capability is arrested.** Criterion: on
  `v2_partial`, mean distinct hosts at κ = 4 is **higher** for the readiness key
  than for the destination-only key. The destination-only learner collapsed to
  0.80 hosts there because a confident marginal learner stops exploiting; a
  readiness-keyed learner should not, because it can believe exploitation pays
  *when ready* while still believing it fails when not. HELD if higher; MOVED
  otherwise. A MOVED verdict here says the collapse was never about the key.
- **R3 — exploitation survives confidence.** Criterion: on `v2_partial` at κ = 4,
  the share of successes that are `EXPLOIT_VULN` is **higher** for the readiness
  key than for the destination-only key (which fell to 1 %). This is R2's
  mechanism, measured directly rather than inferred, and it is reported whichever
  way it falls.
- **R4 — the learner still reduces its own blocked fraction within a run.** *The
  destination-only sweep's L1, re-run on the new key.* Criterion: on the profiles
  whose ablation-arm blocked fraction is at or above 30 % in the **no-MTD** arm
  (experiment 1's threshold, in the condition its own table reports — the reading
  the prior sweep resolved in the open), the mean last-quartile blocked fraction at
  the declared point is lower than the first-quartile, and that within-run
  reduction is larger than at κ = 0. HELD if both. *Note this conclusion is
  necessary but nowhere near sufficient: the destination-only learner passed it
  emphatically while making the attacker worse, which is the whole reason R1 and
  not R4 is the badge gate.*
- **R5 — learning still costs strategic plurality.** Criterion: pooled path
  entropy at the declared κ is **lower** than at κ = 0, and lower again at κ = 4.
  Reported at every κ point whichever way it falls. The destination-only learner
  lost entropy in all ten profile × mapping cells; if the readiness key restores
  some, that is an honest and interesting result, and if it does not, the axis-3
  trade stands and any claim on either axis must name the capability it was
  measured at.
- **R6 — the H-coupling finding survives the ablation.** Criterion: at κ = 0 the
  friction/churn split experiment 1 recorded is reproduced, so the coupling finding
  remains reportable at full strength and any change at κ > 0 is attributable to
  the mechanism rather than to the problem having gone away. HELD if the ablation
  arm's per-profile blocked fractions place the same profiles on the same side of
  the 30 % threshold as experiment 1 and the three prior sweeps did. *This is a
  hard constraint of the handoff, not merely a conclusion: a mechanism that quietly
  routed around every unmet precondition would hide the project's own finding.*
- **R7 — attack success rate stays zero.** Criterion: no run at any point reaches
  the substrate objective. A check that nothing broke, not a claim — the operating
  mutation interval sits inside the degenerate region where ASR cannot discriminate
  anything ([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(b)).

## 3. The badge criterion, fixed before the numbers

Axis 7 is re-scored to **DEMONSTRATED** only if **R1 holds** — the criterion the
axis-7 record already fixed, transcribed here unchanged: *a learner whose credit
signal carries progress, shown to raise breadth or stage advance against its own
ablation arm* ([`learning_capability.md`](learning_capability.md) §8;
[`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d) axis 7).

If R1 moves, the honest badge stays **DESIGNED**, and specifically: if the
generalised learner merely lowers the blocked fraction again (R4 holds, R1 moves),
**that is the same result as before and the badge does not move.** The handoff
names this explicitly as the most tempting place in the project to claim a move
that the evidence does not support.

One clarification fixed in advance, because it will otherwise be arguable
afterwards: R1's second half compares against the *destination-only learner at the
same point*. A readiness key that beat the ablation arm but not the marginal
learner would show that learning helps and the generalisation does not, which is a
different claim from the one this work exists to make, and it would not move the
badge.

## 4. The declared-value statement

**No value in this family was selected to improve any outcome, and no new value
was declared at all.** The readiness generalisation reuses the destination-only
learner's rules artefact (`learning_rules.json`) unchanged — same declared κ = 1
and ρ = 0.5, same bands, same tiers, same Laplace prior α = β = 1. This is
deliberate and is itself the guard: a representation change swept over the
*existing* declared band cannot have had its band chosen to flatter it, because
the band was committed before this representation existed.

The one genuinely new declared artefact is the precondition relation
(`data/ogasp/controller/precondition_relation.json`), and it declares no
magnitude — it transcribes the substrate's own precondition guard, its accuracy
against that guard is measured and reported (exact on v1, 92–94 % on v2), and its
known optimisms are named in the artefact rather than discovered later.

## 5. The joint-composition check

Carried from the superseded composition handoff, and run in the same session
because it gates what the reported configuration may claim.

**The problem.** The three declared modulator families — the outcome overlay's
verdict conditioning, the axis-6 utility modulator, and the axis-7 learner — have
only ever been swept **one at a time**. Two of them independently narrow traversal,
so composing them should compound the narrowing, and **axis 3's demonstrated badge
was earned with all of them null**
([`model_scope_freeze.md`](model_scope_freeze.md) §4). If the model's reported
configuration ships with any modulator active, the plurality evidence was measured
on a different model than the one being described.

**The check.** A small crossed arm — {learner off, learner declared} ×
{utility off, utility declared} — at the declared values, on both mappings, all
five profiles, ten seeds, both MTD conditions, reporting **pooled path entropy**
and distinct hosts.

- **J1 — composition compounds the narrowing.** Criterion: pooled path entropy in
  the both-active cell is **lower** than in either single-active cell. HELD if
  lower than both. This is the expected result and the reason the freeze pinned the
  reported configuration; reporting it makes the pin evidence-backed rather than
  precautionary.
- **J2 — the reported configuration is still the measured one.** Criterion: the
  modulators-null cell reproduces the path entropy on record for the reported
  configuration. This is a consistency check on the claim-integrity rule, not a new
  finding.

Whatever J1 finds, **no combined configuration is claimed**: the headline arm runs
with modulators null, and any modulator-active arm is reported as its own labelled
arm with its own plurality figure. That rule is the freeze's and is not up for
revision here.

## 6. Where this connects

- **Pre-registers the sweep for:** [`learning_representation.md`](learning_representation.md)
  (the representation ruling this tests) and the findings record that follows.
- **Transcribes its badge gate from:** [`learning_capability.md`](learning_capability.md)
  §8 and [`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d) axis 7.
- **Owes its composition check to:** [`model_scope_freeze.md`](model_scope_freeze.md)
  §4 (the pinned reported configuration) and
  [`attacker_state_seam.md`](attacker_state_seam.md) §2 (the composition rule).
- **When to update:** it is a pre-registration and is **not** updated after the
  sweep runs. The findings record reports against it as written; if a criterion
  turns out to be ambiguous, the ambiguity and its resolution are recorded there,
  in the open, exactly as the prior sweep resolved its own.
