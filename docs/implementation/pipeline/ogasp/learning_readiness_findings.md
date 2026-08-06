---
status: durable
created: 2026-08-01
updated: 2026-08-01
topic: "The readiness-keyed learner sweep — per-conclusion verdicts against the pre-registration, the badge decision, and the joint-composition check that falsified the freeze's precautionary inference"
---

# The readiness-keyed learner — what the generalisation bought, and what it did not

> **Retired class labels.** This record is investigation history and is left as
> written: it reports the pre-2026-08-06 labels `pure_steal` / `pure_impediment` /
> `double_extortion` / `infrastructure_setup`, which the objective-tactic rename
> replaced with `objective_exfiltration` / `objective_impact` /
> `objective_exfiltration_impact` / `objective_none_c2`. Rewriting them would
> re-attribute evidence to labels that did not exist when it was taken. Crosswalk:
> [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

**Status:** durable findings record. It reports the 4 600-run sweep and the
800-run joint-composition check against the criteria fixed in
[`learning_readiness_prereg.md`](learning_readiness_prereg.md) **before any output
existed** (commit `97c54a5`). The criteria are transcribed, not adjusted; the one
ambiguity the pre-registration left is resolved in the open (§2.1).

**Reproduce.** Workspace `data/results/learning_readiness/` (gitignored by design
— regenerable), run against commit `cefabef`:

```
PYTHONPATH=src python data/results/learning_readiness/run_sweep.py --workers 6
PYTHONPATH=src python data/results/learning_readiness/analyse.py
PYTHONPATH=src python data/results/learning_readiness/run_composition.py --workers 2
PYTHONPATH=src python data/results/learning_readiness/analyse_composition.py
```

## 1. The verdict in one paragraph

**The representation fix does exactly what a representation fix can do, and it
does not make the attacker better.** Re-keying the learner from the destination
tactic to `(destination, precondition-satisfied?)` **undoes the damage** the
destination-only learner did — compromise breadth at the declared capability
recovers from 3.38 hosts to 4.52, exploitation's share of successes recovers from
6.0 % to 9.5 %, and the collapse at high capability is arrested (1.02 → 2.40 hosts
at κ = 4). What it does not do is **exceed the no-learning ablation arm**, which
sits at 4.60 hosts. The generalised learner climbs back to roughly where an
attacker with no learning at all already was, and stops there. The badge gate
turned on beating that arm, so **axis 7 holds at DESIGNED** (§4).

That result is the one the discussion note
[`../../../notes/ch6_discussion/learning_without_context.md`](../../../notes/ch6_discussion/learning_without_context.md)
predicted in advance: it argued that the credit **signal** and the **representation**
must move together, and only the representation moved here. The learner still
updates on the binary routing verdict; keying that verdict by readiness stops it
from drawing the *wrong* conclusion about exploitation, but a verdict that does not
carry progress still cannot steer toward progress. The two halves of the diagnosis
are now separated by measurement rather than by argument, which is what this sweep
adds.

## 2. Per-conclusion verdicts

| | conclusion | verdict |
|---|---|---|
| **R1** | the readiness key raises breadth against its own ablation arm | **MOVED** (no-MTD); would be HELD on the MTD arm, and neither reading is CI-separated |
| **R2** | the collapse at high capability is arrested | **HELD**, both MTD conditions |
| **R3** | exploitation survives confidence | **HELD**, at every capability |
| **R4** | the learner still reduces its own blocked fraction within a run | **HELD**, and indistinguishable from the destination-only key |
| **R5** | learning still costs strategic plurality | **HELD** — and the readiness key costs *less* of it at every step |
| **R6** | the H-coupling finding survives the ablation | **HELD** |
| **R7** | attack success rate stays zero | **HELD** — 0 of 4 600 |
| **J1** | composition compounds the narrowing | **MOVED**, in all four cells — the narrowing is *sub-additive* |
| **J2** | the null cell reproduces the reported configuration | **HELD** |

### 2.1 The ambiguity the pre-registration left, resolved in the open

§2's R1 named the mapping (`v2_partial`) and the parameter point but **not the MTD
condition**, exactly as the destination-only sweep's L1 failed to. It is read in
the **no-MTD arm**, for the same reason that sweep resolved the same ambiguity the
same way: that is the condition experiment 1's own table reports, and adopting the
other reading after seeing that it flatters the mechanism is precisely what
pre-registration exists to prevent. Both readings are printed by the analysis and
both are recorded here:

| arm | ablation | destination-only | readiness | R1 |
|---|--:|--:|--:|---|
| no MTD | 4.60 ± 0.73 | 3.38 ± 0.66 | 4.52 ± 0.70 | **MOVED** |
| random MTD @ 200 s | 1.42 ± 0.36 | 1.16 ± 0.37 | 1.70 ± 0.48 | would be HELD |

**Neither reading is CI-separated**, and that matters more than which arm is
chosen. On the MTD arm the readiness key's 1.70 against the ablation's 1.42 is
well inside overlapping intervals at ten seeds, so even the favourable reading
would not support the claim. A fourth independent sweep has now failed to separate
adjacent arms at ten seeds; the constraint is a property of the sample size, not of
this mechanism.

### 2.2 R1 and R2 — the ladder is the clearest form of the result

Mean distinct hosts, `v2_partial`, no MTD, ρ = 0.5:

| κ | destination-only | readiness |
|--:|--:|--:|
| 0 (ablation) | 4.60 | 4.60 |
| 0.5 | 4.00 | 4.40 |
| 1.0 | 3.38 | **4.52** |
| 2.0 | 2.02 | 3.66 |
| 4.0 | 1.02 | **2.40** |

The destination-only learner degrades monotonically from the moment it is switched
on. The readiness-keyed learner **tracks the ablation arm** through the declared
point and degrades far more slowly above it. Read as a statement about the
representation this is unambiguous: the collapse recorded as the destination-only
learner's headline failure was **a representational artefact**, and the key fixes
it. Read as a statement about the attacker it is equally unambiguous in the other
direction: at no capability does the readiness learner exceed 4.60.

Effort-to-breadth at the declared point tells the same story from the cost side —
the readiness learner converts 273 actions into 4.52 hosts (60.5 actions per host)
against the ablation's 63.4 and the destination-only learner's 80.1. It is the
*most efficient* of the three and still not the broadest.

### 2.3 R3 — exploitation survives, which is R2's mechanism measured directly

Share of successes that are `EXPLOIT_VULN` (`v2_partial`, no MTD):

| arm | successes | of which `EXPLOIT_VULN` | hosts |
|---|--:|--:|--:|
| ablation (κ = 0) | 9 659 | 1 106 (11.5 %) | 4.60 |
| destination-only, κ = 1 | 11 123 | 668 (6.0 %) | 3.38 |
| **readiness, κ = 1** | 11 555 | 1 102 (**9.5 %**) | 4.52 |
| destination-only, κ = 4 | 17 031 | 320 (1.9 %) | 1.02 |
| **readiness, κ = 4** | 17 841 | 667 (**3.7 %**) | 2.40 |

This is the diagnosis confirmed at its mechanism. The destination-only learner
concluded that exploitation does not pay, because its marginal averaged the
0.61-when-ready regime together with the 0.00-when-unready one
([`learning_representation.md`](learning_representation.md) §1). The readiness key
lets it hold both beliefs separately, and exploitation's share at the declared
capability returns to within two points of the no-learning arm. At κ = 4 it is
still nearly double the destination-only key's — the attacker stays willing to
attack — but it is well below the ablation's 11.5 %, which is why R2's arrest is
partial rather than complete.

### 2.4 R4 — friction reduction is real and the generalisation adds nothing to it

Blocked fraction over the first against the last quarter of each run's attempted
actions, at the declared point, `v1_ckc_total` friction profiles:

| profile | ablation | destination-only | readiness |
|---|---|---|---|
| `aggregate` | 0.969 → 0.880 (−0.089) | 0.918 → 0.442 (−0.476) | 0.919 → 0.445 (**−0.474**) |
| `pure_impediment` | 0.833 → 0.415 (−0.418) | 0.851 → 0.000 (−0.851) | 0.845 → 0.003 (**−0.842**) |
| `pure_steal` | 0.964 → 0.983 (+0.019) | 0.931 → 0.940 (+0.009) | 0.931 → 0.940 (+0.009) |

R4 **HELD**, and the interesting part is that the two keys are
**indistinguishable** on it (−0.474 against −0.476; −0.842 against −0.851). That is
not a null result, it is the study's sharpest internal evidence for what the key
does and does not change: *avoiding what fails* needs only the marginal, so both
keys do it equally well, while *knowing when the thing that failed would have
worked* needs the context, and only one key has it. The blocked-fraction measure
cannot see the difference between the two mechanisms, and breadth can. An
evaluation that scored this axis on friction alone would have called the two
learners equivalent.

`pure_steal` remains the counter-case it was in the destination-only sweep, for the
same structural reason: at 97.6 % blocked there is almost no success anywhere in
its net for a belief to steer toward, and a belief-based learner needs at least one
destination that pays. The readiness key does not change that — a context split of
a nearly-empty evidence base is still nearly empty.

### 2.5 R5 — the plurality trade is real, and the readiness key pays less of it

Pooled path entropy (bits), no MTD, ρ = 0.5:

| κ | `v2_partial` destination-only | `v2_partial` readiness | `v1_ckc_total` destination-only | `v1_ckc_total` readiness |
|--:|--:|--:|--:|--:|
| 0 | 2.621 (ablation) | 2.621 | 2.679 (ablation) | 2.679 |
| 0.5 | 2.474 | 2.509 | 2.607 | 2.605 |
| 1.0 | 2.272 | **2.405** | 2.514 | 2.530 |
| 2.0 | 1.881 | **2.030** | 2.346 | 2.424 |
| 4.0 | 1.232 | **1.300** | 2.281 | 2.307 |

R5 **HELD** — entropy falls with capability on both keys, so the axis-3 trade
stands and any claim on either axis must still name the capability it was measured
at. But the readiness key retains more plurality at every step above κ = 0.5. The
reason follows from the key: a learner that can believe "exploitation pays *when
ready*" keeps exploitation in its out-sets and keeps visiting the places that make
it ready, where a marginal learner prunes the whole branch. Less collapse is a
by-product of the representation, not a separate mechanism.

### 2.6 R6 — the coupling finding survives at full strength

Ablation-arm blocked fraction, no MTD, against experiment 1's 30 % friction
threshold:

| profile | `v1_ckc_total` | side | `v2_partial` | side |
|---|--:|---|--:|---|
| `aggregate` | 0.914 | friction | 0.147 | churn |
| `pure_impediment` | 0.601 | friction | 0.172 | churn |
| `pure_steal` | 0.976 | friction | 0.132 | churn |
| `double_extortion` | 0.000 | churn | 0.363 | friction |
| `infrastructure_setup` | 0.000 | churn | 0.227 | churn |

On `v1_ckc_total` — the mapping experiment 1 ran — the same three profiles sit on
the friction side and the same two on the churn side, as in experiment 1 and the
three prior sweeps. **HELD.** The hard constraint the handoff set is therefore met:
the coupling finding remains reportable at null strength, so every change at κ > 0
is attributable to the mechanism rather than to the problem having been defined
away.

## 3. The badge's other half, reported rather than quietly used

The axis-7 criterion's gate is a **disjunction** — *raise breadth **or** stage
advance against its own ablation arm* — while R1 as pre-registered names breadth
alone. The other half is therefore reported here in full, so the narrower R1 cannot
be read as having dodged it.

Fraction of runs advancing past the stage they first succeeded at, declared point,
no MTD:

| mapping | ablation | destination-only | readiness |
|---|---|---|---|
| `v1_ckc_total` | 0.540 ± 0.140 | 0.720 ± 0.126 | 0.720 ± 0.126 |
| `v2_partial` | 0.960 ± 0.055 | 0.980 ± 0.039 | 0.980 ± 0.039 |

The disjunction does not rescue the gate, on two independent grounds. The
readiness key's stage advance is **identical to the destination-only key's** to
three decimals on both mappings, so R1's second half — higher than the
destination-only learner at the same point — fails on this measure exactly as it
does on breadth; whatever is raising stage advance over the ablation arm is
*learning*, not the generalisation. And the intervals overlap the ablation arm's on
both mappings, so the rise is not separated at ten seeds in any case.

## 4. The badge, decided against the pre-registered criterion

**Axis 7 holds at DESIGNED.** Not DEMONSTRATED, and the reasoning is the
pre-registration's rather than a reading of the numbers.

§3 of the pre-registration fixed the gate: DEMONSTRATED only if R1 holds. R1 moved
on the resolved reading, is unseparated on the other, and the disjunction's other
half fails for the same reason. The pre-registration also anticipated this exact
shape and named it in advance — *if the generalised learner merely lowers the
blocked fraction again (R4 holds, R1 moves), that is the same result as before and
the badge does not move.* R4 held, R1 moved, and the badge does not move.

It would have been easy to argue the other way, and the temptation is worth
recording because it is stronger here than in the destination-only study. That
sweep produced a mechanism that plainly hurt the attacker; this one produced a
mechanism that plainly *repaired* that harm — a 34 % breadth recovery at the
declared point and a 135 % recovery at κ = 4, with exploitation restored and
plurality partly preserved. Every one of those is a real, measured improvement, and
none of them is the criterion. The criterion asks whether the attacker's
accumulated knowledge makes it a **better adversary than an attacker with no
knowledge at all**, and on this substrate the answer is still no.

**What would move it, restated with the new evidence.** The remaining gap is now
isolated to the credit signal, and the isolation is this study's contribution. The
representation is no longer the blocker — it was, it was fixed, and fixing it
recovered exactly the ground the misrepresentation had lost and no more. A learner
whose credit signal carries **progress** (host compromise, stage advance, breadth)
rather than the routing verdict remains the outstanding requirement, and it is now
the *only* outstanding requirement on this axis. That is the item the freeze record
already lists as future work item 1
([`model_scope_freeze.md`](model_scope_freeze.md) §3).

**On the standing category-error question**, which this study does not resolve and
does not attempt to. The axis-7 findings ledger argues that scoring a *property*
axis with a *performance* test is a category error, and that the correct response
would be a fresh pre-registration under a property framing
([`learning_axis_evaluation_findings.md`](learning_axis_evaluation_findings.md)
§5). This sweep was
pre-registered under the **performance** framing, because the handoff directed the
criterion the axis-7 record already fixed. It therefore inherits the same open
question rather than settling it, and the disposition remains Marc's. What this
study adds to that question is a cleaner test case: under a property framing, a
mechanism that demonstrably changes *what the attacker believes and attempts* — R2,
R3 and R5 all measure exactly that — would read very differently from how the
performance gate scores it here.

## 5. What the sweep exposed that nobody pre-registered

**The two keys are separated by breadth and by nothing else in the friction
family.** §2.4 is the finding: on every friction-shaped measure the two learners
are indistinguishable to three decimals, and on breadth they differ by 34 %. The
measure that made axis 7 look successful in the destination-only study — within-run
blocked-fraction reduction — is precisely the measure that **cannot** tell the two
representations apart. This is the axis's own recurring lesson arriving a second
time and from a new direction: an attacker's friction is not its progress, and a
capability scored on friction can be scored identically whether or not it can
represent the thing that causes the friction.

## 6. The joint-composition check — the freeze's inference was wrong

J1 asked whether composing the two built modulators compounds the narrowing each
does alone. **It does not. J1 MOVED in all four cells**, and the direction is
consistent enough to be a finding rather than noise.

Pooled path entropy (bits) and mean distinct hosts:

| cell | v1 no-MTD | v2 no-MTD | v2 no-MTD hosts |
|---|--:|--:|--:|
| null (reported config) | 2.679 | 2.621 | 4.60 ± 0.73 |
| learner only | 2.530 | 2.405 | 4.52 ± 0.70 |
| utility only | **1.934** | **1.993** | 2.22 ± 0.54 |
| both active | 1.979 | 2.233 | 4.22 ± 0.94 |

In every cell the both-active configuration sits **above** the utility-only
configuration on entropy — the composition is **sub-additive**, and on `v2_partial`
markedly so (2.233 against 1.993). Breadth tells the same story more strongly: the
utility modulator alone costs 2.38 hosts (4.60 → 2.22), and adding the learner to
it **recovers almost all of them** (→ 4.22).

The mechanism is legible from what each factor does. The utility modulator applies
a *static declared* preference for cheap tactics, which on this substrate are the
most precondition-coupled ones — experiment 1's coupling finding in economic terms.
The readiness learner applies a *learned, state-conditioned* preference that
discovers those cheap tactics are failing when attempted unready. The two therefore
pull in opposite directions on the same edges, and the learner partially corrects
the utility model's declared mistake. They are not two narrowings that stack; they
are a declared bias and an empirical correction to it.

**What this changes and what it does not.** It falsifies the freeze's precautionary
inference that "composing them compounds the narrowing" — that was reasoned, never
measured, and it is now measured and wrong. It does **not** change the pin on the
reported configuration: every single-modulator cell still narrows traversal against
the null cell, so axis 3's plurality evidence still belongs to the modulators-null
arm and any modulator-active arm still reports its own plurality figure
([`modulator_composition.md`](modulator_composition.md) §4). The pin was right; the
reason given for it was not the whole story.

J2 **HELD**: the null cell's pooled entropy (2.679 on v1, 2.621 on v2) sits inside
the 1.45–2.71 bit range experiment 2 recorded for the reported configuration, so
the configuration described is the configuration measured.

## 7. Where this connects, and when to update

- **Reports against:** [`learning_readiness_prereg.md`](learning_readiness_prereg.md)
  (not updated — a pre-registration is not revised after its sweep).
- **Generalises:** [`learning_capability.md`](learning_capability.md) (the
  destination-only learner and its sweep, which this reproduces as a control arm).
- **Rests on:** [`learning_representation.md`](learning_representation.md) (the
  key ruling and its measured sparsity budget).
- **Supplies verdicts to:** [`modulator_composition.md`](modulator_composition.md)
  §5 (J1/J2).
- **Qualifies:** [`../../../notes/ch6_discussion/learning_without_context.md`](../../../notes/ch6_discussion/learning_without_context.md)
  — its revisit condition is engaged and its diagnosis survives (§1); the note is
  updated with the separating evidence rather than retracted.
- **When to update:** if a progress-carrying credit signal is built and swept, at
  which point this record becomes the control arm for that study exactly as the
  destination-only sweep is the control arm for this one; and if the category-error
  disposition (§4) is resolved in favour of a property framing, which would call
  for a fresh pre-registration rather than a re-reading of these numbers.
