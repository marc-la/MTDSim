---
status: open
created: 2026-08-09
---

# Ablate the objective partition — establish whether axis 2's DEMONSTRATED badge measures objective conditioning, or five nets built from different flow subsets

> **Progress, 2026-08-09 — the behavioural half is instrumented and has run;
> the control arm (§ Recommended approach, arm 3) is what remains.**
> `profile_divergence` now carries the execution-level null band §3 below asked
> for (`split_half_divergence_null` / `divergence_report`, `measures.py` §2),
> and the first corpus run is on record
> ([`../implementation/pipeline/ogasp/profile_divergence_findings.md`](../implementation/pipeline/ogasp/profile_divergence_findings.md);
> workspace `data/results/profile_divergence/`, pre-registered before output).
> Three things a session picking this up must know. **A1 is discharged** — every
> between-class pair clears the null by 40–110× on the visit stream. **The
> size confound this handoff predicted is now measured, and it is total**: the
> pre-registered kill criterion fired at Spearman ρ = −1.0 between a class's
> JSD-to-`aggregate` and its flow count, so the class-versus-`aggregate`
> comparison is established as uninterpretable on its own and the label-blind
> size-matched arm is not merely recommended but forced. **The outcome half is
> unseparated at 50 seeds** (`ordering_supported` False on distinct hosts in
> both MTD conditions), so A2 needs either more seeds or a sharper outcome
> measure. The analysis re-slices by re-invocation; run the control arm's runs
> through the same `analyse.py` beside this corpus.

## State of play

**Axis 2 is the only DEMONSTRATED badge on the criterion whose ablation has never
run.** It has been demonstrated twice — profile identity determines failure mode
independent of seed ([`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
§(f)), and profile identity determines which defence suppresses the attacker best,
in four of five cells at the operating interval (§(f2)). Both are *between-profile*
differences. A between-profile difference is consistent with two explanations, and
no run on record separates them:

1. the objective partition conditions behaviour — the claim the badge makes;
2. the five nets are unions of different flow subsets, and any five such nets
   would differ.

Axes 4, 6 and 7 all carry ablation arms and all held at DESIGNED **because of
them**. Axis 2 has never been asked the question.

**The ablation arm already exists, and has already run.** `aggregate` is not a
fifth objective class — it is the union of every classified flow, built as the
partition-off null. The builder says so in its own docstring
([`weights.py:116-125`](../../src/mtdsim/l3_simulation/petri/weights.py#L116-L125)):
*"the four classes plus `aggregate` = the union of all classified flows (the full
corpus — built from the flow union, not an average of the class nets, **so the null
is corpus-grounded**)"*. It has run in experiment 1, experiment 2, both learning
sweeps, the progress-credit sweep and the stealth corpus. Every findings table
lists it as a fifth profile beside the four classes. **Nothing has ever analysed it
as the null it was built to be.**

**The measure exists too, and has never been run on a corpus.**
`profile_divergence` ([`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py)
§2) computes pairwise Jensen–Shannon divergence between profiles' pooled visit
distributions and terminal-tactic distributions, in the L2 convention, so the
method is already defended one layer up
([`../implementation/pipeline/gasp/gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md)
§(g)). It appears nowhere outside
[`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
and the validation harness. That record names its open blind spot: **no null band**
— "the L2 check calibrates one; an execution-level null is future work". §3 below
supplies one.

**The class flow counts, which are the whole reason a second control is needed**
(`data/gasp/classification.csv`, 38 flows):

| class | flows |
|---|--:|
| `objective_exfiltration` | 19 |
| `objective_impact` | 8 |
| `objective_exfiltration_impact` | 6 |
| `objective_none_c2` | 5 |
| `aggregate` | **38** (the union) |

`aggregate` carries between two and nearly eight times any single class's flows, so
a class-versus-`aggregate` separation is confounded with corpus size from the
outset. That is what the size-matched arm in §2 exists to break.

**A free pre-check before committing to any run.** The progress-credit sweep's
`v2_partial` no-MTD ablation column already holds all five profiles under identical
conditions ([`../implementation/pipeline/ogasp/progress_credit_findings.md`](../implementation/pipeline/ogasp/progress_credit_findings.md)
§4): `aggregate` **6.14** distinct hosts, `objective_impact` 4.74,
`objective_exfiltration` 4.30, `objective_none_c2` 3.40,
`objective_exfiltration_impact` 1.96. The unpartitioned attacker compromises more
than every conditioned one. One cell of one sweep settles nothing, but it points at
objective conditioning **costing** breadth rather than buying it, and it costs
nothing to look at first.

**Two adjacent corrections, flagged and deliberately not actioned here.**

- [`2026-08-05_apt_axis_measurement_metrics.md`](2026-08-05_apt_axis_measurement_metrics.md)
  §2 records axes 2 and 4 as "not built". Both are built —
  `profile_divergence` is `measures.py` §2 and the axis-4 readers are §3. That
  handoff's work list needs correcting or retiring; it is not this handoff's job,
  but a session picking this up will read it and should not be misled.
- The criterion's axis 7 is stale: it states a progress-carrying credit signal is
  "the sole remaining item", and that signal was built and swept on 2026-08-02
  over 7 000 runs with all five conclusions not confirmed
  ([`../implementation/pipeline/ogasp/progress_credit_findings.md`](../implementation/pipeline/ogasp/progress_credit_findings.md)).
  `progress_credit` appears nowhere in the criterion. Separate job.

## Recommended approach

**Three arms, because two cannot separate the two explanations.**

| arm | what it is | status |
|---|---|---|
| the four classes | the shipped objective-conditioned nets | on disk, already run |
| `aggregate` | the partition removed, corpus held whole | on disk, already run |
| **size-matched, label-blind** | nets built from random flow subsets at each class's flow count, drawn ignoring the objective labels | **the only new work** |

The third arm is the one that decides the study. If the classes separate from
`aggregate` but **not** from label-blind subsets of the same size, then what the
badge has been reading is corpus size and net shape, not objective conditioning.

**This is the precedent that makes the design non-negotiable.** Axis 7's sweep ran
two controls — `control_asymptotic` and `control_matched`, the latter a declared
static bias matched to the learner's own observed aggression. The learner separated
cleanly from the first (JSD 0.2804) and **not at all** from the second (0.1196),
and U3 is the sharpest finding in that record precisely because the second control
existed ([`../implementation/pipeline/ogasp/progress_credit_findings.md`](../implementation/pipeline/ogasp/progress_credit_findings.md)
§2). One control here would reproduce the same near-miss with nothing to catch it.

### Building the control arm without touching source

`load_routing_net` already takes a `petri_dir`
([`net.py:215`](../../src/mtdsim/l3_simulation/movement/net.py#L215)), so the
control nets can live in a scratch directory and no shipped artefact moves. It also
validates `profile in PROFILES`, so **name the drawn subsets with the five existing
profile names** rather than widening that tuple — that keeps the change to zero
lines of source.

The path:

1. Write a scratch `classification.csv` assigning the drawn flow subsets to the
   five existing class names. Seed the draw and record the drawn flow IDs.
2. Run `PYTHONPATH=src python -m mtdsim.l3_simulation.petri` against it, writing
   into the scratch directory.
3. Run the movement layer with `petri_dir` pointed at that directory.
4. Repeat over **R independent draws** (recommend R = 10) so the control is a
   distribution rather than a point. A single draw is a sample, and the classes
   would be compared against an arbitrary one.

**The synthetic overlay must be regenerated with the nets, never inherited — this
is the trap in the design.** `synthetic_overlay.json` is profile-keyed, and the
overlays genuinely differ: `objective_exfiltration_impact` and `objective_none_c2`
each receive a synthetic recon → initial-access transition because their observed
corpus does not bridge that edge, while the other three receive none because theirs
already does. The guard rule fires **conditionally on the flow set**, so a drawn
subset named `objective_none_c2` that happens to bridge the edge would inherit a
synthetic transition it does not need. Step 2 regenerates the overlay and the
structural nets together, which is the reason to build through the existing builder
rather than hand-writing nets.

### What to measure

**Behavioural half** — `profile_divergence`, both halves (pooled visit
distribution and terminal-tactic distribution).

**The null band the measure lacks.** Compute it from the same runs rather than
declaring one: split each profile's seeds into two halves and take the JSD between
halves. That is the divergence attributable to seed noise alone at this sample
size, and every between-arm figure must clear it to mean anything. It is cheap,
it is derived from the corpus rather than declared, and it closes the blind spot
`measurement_suite.md` §(b) records.

**Outcome half** — distinct hosts, blocked fraction, terminal mode. These are what
the badge's existing evidence is actually stated in (failure mode), so the ablation
must speak to them or it does not address the badge.

**The defence-ranking half, budget permitting.** The badge's stronger form is that
the mechanism ranking differs by profile. If the defence family is affordable at
this seed count, the same question applies to it: does the ranking differ between
classes by more than it differs between label-blind draws?

**Re-read before you re-run.** The class and `aggregate` arms should come from a
recorded corpus wherever one matches the conditions; only the control arm strictly
needs new simulation.

### Alternatives considered

- **`aggregate` alone as the control.** Rejected — confounded with corpus size
  from the outset (the table above), and this is exactly the near-miss axis 7's
  second control caught.
- **A parameter-null ablation, matching axis 4's empty value table or axis 6's
  λ = 0.** Not available. The objective partition *is* structure; there is no knob
  to zero, so the ablation is necessarily structural. Say so in the record rather
  than apologising for it — a structural ablation is the correct instrument when
  the thing ablated is structure.
- **Re-partitioning the corpus on a different objective taxonomy.** A much larger
  study, and it answers a different question (is *this* partition the right one)
  than the badge makes (does partitioning by objective do anything).

## Pre-register before running

House discipline, and this study needs it more than most, because **it can lower a
badge**. Commit the conclusions, their criteria and their directions before any
output exists, in a `*_prereg.md` beside the findings record, in its own commit —
the commit order is the audit trail. Suggested conclusions, to be refined by the
session that owns them:

- **A1 — the divergence measure clears its own null.** Between-class JSD exceeds
  the within-profile cross-seed JSD null.
- **A2 — the partition does something.** The four classes separate from
  `aggregate` on at least one outcome measure, 95 % CIs disjoint.
- **A3 — the badge gate, and the one that matters.** The four classes separate
  from the size-matched label-blind draws. *If A2 holds and A3 fails, the badge's
  evidence is corpus size and net shape, not objective conditioning, and the
  record must say so.*
- **A4 — kill criterion.** The measure is not a re-expression of flow-set size:
  Spearman |ρ| between a profile's JSD-to-`aggregate` and its flow count is below
  0.90. This mirrors the non-redundancy bar the disengagement and exposure studies
  both imposed on themselves; use the same threshold so verdicts stay comparable.

Commit the unflattering direction explicitly. A measure re-specified after it
fails to discriminate is the failure mode the whole discipline exists to prevent.

## Validation gate

1. **Readers-plus-a-control only.** Full `tests/l3_simulation` and the
   substrate/carve/golden suites pass **unchanged**. A moved golden means a
   mechanism was built, and none is authorised here.
2. **Shipped artefacts byte-identical.** `data/ogasp/petri/*_structural.json` and
   `synthetic_overlay.json` are untouched; the scratch directory is the only thing
   written. Verify with `git status` before committing.
3. **The draw is reproducible.** Seeded, with the drawn flow IDs recorded per draw
   in the results workspace, so the control arm can be rebuilt exactly.
4. **Determinism (SIM-05).** Re-derivation from re-created runs is exact.
5. **Every aggregate through `interval_report`**; `ordering_supported` is the gate,
   never the sorted means.
6. **Censoring reported separately**, never pooled.

## Hard constraints

- **No attacker capability, no new declared magnitude, no new declared family.**
  The control arm is a re-draw of an existing corpus through an existing builder.
- **Scores move on evidence only.** Never change the model, weights, mapping or
  metrics to protect a row (S6; [`../workflows/guardrails.md`](../workflows/guardrails.md)).
  That binds a badge moving **down** exactly as it binds one moving up.
- **No badge move without a pre-registered criterion met on the evidence** — in
  either direction.
- **Degenerate region.** At the 200 s operating interval no arm completes the
  objective, so every measure must be breadth- or time-shaped; success-rate-shaped
  measures are pinned at zero and evidence nothing.
- **Envelope, not actor.** A run is one instantiation of a behavioural envelope
  under a declared policy; the study scores what the partition does to the
  envelope, never the realism of any class.
- Determinism; within-substrate comparability only; Australian English; branch per
  session; commit locally; **never push**.

## Reading list

- [`../../src/mtdsim/l3_simulation/petri/weights.py`](../../src/mtdsim/l3_simulation/petri/weights.py)
  §`profile_flow_sets` (lines 116–125) — `aggregate` is the corpus-grounded null,
  in the builder's own words. The premise of this whole handoff.
- [`../../src/mtdsim/l3_simulation/movement/measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py)
  §2 — `profile_divergence`, `jsd`, `visit_distribution`,
  `terminal_place_distribution`. Read the signatures before designing the analysis.
- [`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  §(b) — the `profile_divergence` row and its recorded blind spot; §(f) for what
  every consumer must respect.
- [`../implementation/pipeline/ogasp/progress_credit_findings.md`](../implementation/pipeline/ogasp/progress_credit_findings.md)
  §2 (U3) — the two-control precedent, and what running only one would have cost.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(d) axis 2 and §(f)/§(f2) — the badge, and the two qualifications its evidence
  already carries.

## Out of scope (explicitly)

- **Any mechanism.** No attacker capability, no routing change, no declared family.
- **Re-partitioning the corpus** or revisiting the objective taxonomy — a
  different question, and a much larger one.
- **Regenerating the shipped nets.** The scratch directory exists so that they are
  not touched.
- **The other axes.** Their instruments are built; axes 2 and 4 are the two never
  run, and axis 4's readers (`interrupt_action_mix`, `recovery_times`) are the
  companion job, not this one.
- **Correcting the stale 2026-08-05 handoff or the criterion's axis 7** — both
  flagged in State of play, neither actioned here.
- **Dissertation prose.**
