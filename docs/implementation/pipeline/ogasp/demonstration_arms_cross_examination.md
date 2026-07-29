---
status: durable
created: 2026-07-29
topic: "Cross-examination of the experiment-2 / demonstration-arms result (branch feat/exp02-ashen-lynx) by an independent parallel derivation of the same handoff: two agreements that count as replication, one power objection against the axis-3 promotion, one reasoning conflation in the sink policy, and the merge surface between the two branches."
updated: 2026-07-29
---

# Cross-examination — a second, independent derivation of the same handoff

**Status:** durable review record. Two sessions ran
[`../../../handoffs/2026-07-28_axis134_demonstration_arms.md`](../../../handoffs/2026-07-28_axis134_demonstration_arms.md)
in parallel without knowledge of each other, from the same commit (`a683e36`).
The other session's work is on **`feat/exp02-ashen-lynx`** and is the fuller
deliverable: it carries the run, [`sink_policy.md`](sink_policy.md),
[`experiment_02_findings.md`](experiment_02_findings.md) and the criterion
update. This session's run was **stopped as a duplicate** on Marc's ruling.

What survives from the duplication is worth more than a second copy of the
numbers: an independent pre-registration
([`demonstration_arms_prereg.md`](demonstration_arms_prereg.md)) and an
independent design record ([`sink_retrace_design.md`](sink_retrace_design.md)),
written before either session saw the other's, against which the shipped result
can be cross-examined. Two of the findings below are **agreements**, which is
replication; two are **objections**, flagged for Marc to resolve rather than
actioned.

## 1. Agreement — the saturated depth measure, predicted independently

Both derivations concluded, separately, that `deepest_successful_stage` cannot
carry axis 1 under `v2_partial`. The other session found it returns **2 for all
800 movement runs**. This session found the same before running anything — every
run first succeeds at stage 0 and reaches stage 2 — and pre-registered the
consequence as a reason for *not* using it as axis 4's primary measure
([`demonstration_arms_prereg.md`](demonstration_arms_prereg.md) §5).

Two independent derivations retiring the same measure for the same structural
reason is the strongest form this finding could take. It is the third progression
measure retired for saturation, and the second time it has happened to a
*replacement* for a saturated measure — which is itself the durable lesson.

## 2. Agreement — the per-mechanism split of the ~90 % suppression

The shipped result attributes the suppression to one family. This session's
partial run (207 rows, `pure_steal`, conditioned arm, 30 seeds, stopped before
completion) reproduces it on a different runner and a different seed budget:

| mechanism | this session (partial) | shipped result (profiled arm) |
|---|--:|--:|
| Complete Topology Shuffle | 89 % | 89.1 % |
| IP Shuffle | 82 % | 87.8 % |
| Host Topology Shuffle | 85 % | *(not in the shipped table)* |
| OS Diversity | 40 % | 41.2 % |
| Service Diversity | 40 % | 37.1 % |
| Port Shuffle | 19 % | *(not in the shipped table)* |

The agreement is close enough to treat as replication, and it is the substantive
half of E1: the ~90 % figure belongs to the **topology-and-address** mechanisms
against the profiled attacker, not to MTD in general.

## 3. Objection — axis 3's promotion rests on a statistic the same document declares unpowered

**This is the one finding here that could change a badge, and it is flagged for
Marc rather than actioned.**

`experiment_02_findings.md` §5 states, in the not-powered list: *"Any significance
claim on the defence ranking (E5). Ten seeds gives a directional rank comparison,
not a test."* E5 is then reported with exactly that discipline — a rank
correlation, captioned as directional.

E3(b), however, is operationalised as *"the mechanism ranking by breadth
suppression is not identical for every profile"*, and is reported as met on *"4 of
5 distinct at 200 s, 5 of 5 at 2 000 s"*. That is the **same class of statistic** —
a per-profile ranking of mechanisms by breadth suppression at ten seeds — and it
is used to move a badge from DESIGNED to DEMONSTRATED.

The concern is specific, and the analysis code states it more sharply than the prose
does. `analyse.py` computes half (b) as:

```python
    ok_b = len(set(rankings.values())) > 1
```

— where `rankings[profile]` is that profile's conditions sorted by mean breadth
suppression at ten seeds, with **no interval test anywhere in the comparison**. The
criterion is therefore satisfied when *any two of the five profiles* produce a
different permutation. With five profiles independently ordering seven noisy means,
the probability that all five produce the *identical* permutation is negligible, so
`ok_b` evaluates true with probability close to 1 **under the null of no interaction
at all**. A test that cannot fail on noise cannot distinguish signal from it.

The contrast is internal to the same file. Twenty lines further down, E5 computes
`shifted = ranks["baseline"] != ranks["movement"]` — structurally the same
comparison — and captions it *"DIRECTIONAL at ten seeds — a rank comparison, never a
significance claim."* That discipline is right, and it is the discipline E3(b) needs
before it carries a badge.

Establishing an interaction needs the difference-of-differences to separate, not the
winners to differ.

This session pre-registered the stricter form independently and before seeing the
other: a **crossover** — two conditions *i, j* and two profiles *P, Q* such that the
paired difference (*i* − *j*) is CI-separated **positive in P and negative in Q**
([`demonstration_arms_prereg.md`](demonstration_arms_prereg.md) §5). A sign reversal
is testable at this sample size in a way an argmax comparison is not, and it is the
form an examiner is likeliest to ask for.

**What this does and does not say.** It does *not* say axis 3 should not be
DEMONSTRATED. Half (a) — traversal diversity, path entropy 1.451–2.714 bits, 2–10
distinct openings — is solid and is not in question. And the arm-to-arm inversion
(ρ = −0.893) is a genuinely strong observation, though it compares *attackers*, not
profiles, so it evidences the thesis's divergence claim rather than axis 3's
interaction. What is in question is whether half (b), as operationalised, carries
the weight of a badge move. Two ways forward, both cheap:

1. Re-score E3(b) on the crossover form against the existing runs — no re-run
   needed, the paired per-seed data is already on disk.
2. Raise the seed count for this contrast alone. Thirty seeds was this session's
   pre-registered budget for exactly this reason; the run cost is ~40 min.

## 4. Objection — the sink policy declines edge suppression on an argument that does not reach it

[`sink_policy.md`](sink_policy.md) §2 removes the oscillation guard, reasoning that
routing out of the retraced-to place under an imposed verdict *"means the token
passes through it rather than re-occupying it, so it never pays that place's dwell
and the retrace becomes a zero-time teleport"*. §5 then declines **two** mechanisms
together on that basis: imposing a failure verdict, and suppressing the edge that
led to the sink.

The argument defeats the first and does not reach the second. Under **edge
suppression** the token re-occupies the predecessor as an ordinary visit — it draws
that tactic's dwell, dispatches its verb and produces its own real verdict, exactly
as §2 clause 2 requires. The suppression applies only to the *routing draw that
follows* that visit, removing one destination from the composed distribution before
it is sampled. Nothing is imposed, nothing is skipped, and no time is saved: this
session built it that way and its gates pass, including the one asserting every
retraced visit consumes positive time
([`sink_retrace_design.md`](sink_retrace_design.md) §3, `test_movement_retrace.py`).

**The conclusion is unaffected — the guard genuinely is unnecessary.** §3's
structural argument is stronger than this session's (it computes the geometric
expectation, ~1.1 retraces per encounter, where this session only checked that
positive mass remains), and this session's own measurements agree: 4 retraces per
479-step run, under 1 % of steps. Suppression is redundant on this corpus.

What matters is that §3's closing sentence nominates edge suppression as *"the
fallback to adopt if a future corpus revision breaks the §3 check"*. A future
session picking up that fallback will read §5's stated reason, find "arithmetically
incompatible with charging the retrace any time", and conclude the fallback cannot
be built. It can; it is built on this branch. **The recorded reason should be
narrowed to the verdict-imposition variant**, leaving suppression declined on
redundancy alone — which is the honest and sufficient ground.

## 5. A limitation this cross-examination exposes in *this session's* criterion

The shipped analysis's axis-1 correction is the best piece of reasoning in either
derivation, and it lands partly on this session's own work. Two artefacts were
caught there: `foothold_retentions` measures duration *until loss* rather than
retention, and application-layer mechanisms (OS/Service Diversity) sever position
**never**, so every foothold under them is retained trivially — persistence
evidenced by the absence of a challenge to it.

This session's `refoothold_rate` is immune to the second artefact **by
construction**: it returns `None` when position was never severed, so
application-layer-only cells are excluded rather than counted as successes, and
the docstring records that encoding it as 0.0 would be the mirror error. That is a
genuine advantage of the formulation and a reason to keep the measure.

It is **not** immune to the deeper critique. The shipped finding is that retention
rises as mutation pressure falls, so a badge would move on evidence that *"the
attacker keeps position exactly when the defence stops taking it"*. A re-foothold
*rate* inherits that: with fewer severances and more time after each, the rate
rises at the slower tempo for the same reason. This session's criterion carries a
sinkless-profile guard (A1.3) against the retrace confound but **no tempo guard**,
and it should have. Recorded as a defect in
[`demonstration_arms_prereg.md`](demonstration_arms_prereg.md) §5 A1.1, not
retro-fixed: the pre-registration stands as written, and the correction belongs to
whoever next scores axis 1.

## 6. The merge surface

Four source files are touched by both branches and will conflict:
`movement/attacker.py`, `movement/run.py`, `movement/measures.py`,
`l3_simulation/trace.py`. Everything else is disjoint.

The two sink implementations are **not** compatible line-for-line and should not be
hand-merged: they differ in what a retrace records (the other session emits a
separate zero-dwell `RETRACE` record; this session flags the re-visit), and every
downstream count follows from that choice. **Recommendation: take the shipped
branch's implementation whole** — it is the one the published numbers were produced
on, and a record schema that disagrees with the run that used it would be worse
than either choice.

Additive from this branch, and not present on the other:

| artefact | why it is worth keeping |
|---|---|
| `controller/outcome.py::verdict_blind_overlay` + `test_verdict_blind_arm.py` (45 tests) | the ablation as a named, exported helper with the null **test-pinned** at every place of every net under every verdict, and end to end against an independently-constructed no-overlay object. The shipped branch builds the arm inside its runner, so the null identity is used but not asserted. |
| `measures.refoothold_times` / `refoothold_rate` | §5 — the position-contest measure that excludes application-layer-only cells by construction |
| `measures.first_success_stage` / `advanced_after_first_success` | advance-past-first-success, invariant to where the ceiling sits; the one stage-shaped quantity the saturation argument does not kill |
| `MovementRunResult.retrace_count` | makes the no-budget argument falsifiable from the run result rather than from the records |
| [`demonstration_arms_prereg.md`](demonstration_arms_prereg.md) | the independent criteria §3 and §5 rest on |

**An operational hazard, found the hard way.** The other session's worktree reaches
`data/results/` through a **symlink to the main clone's copy**, so two sessions on
two branches were writing experiment workspaces into one directory. Nothing
collided — the workspaces are named `axis134_demonstration/` and
`expo02_ashen_lynx/` — but only by luck of naming, and a session that reused a
directory name would have overwritten another's numbers with no warning and no
trace in git (the whole tree is gitignored). Two mitigations, either sufficient:
name the workspace after the branch rather than after the handoff, or give a
worktree its own `data/results/` rather than a symlink.

One further datum for whoever next sizes a matrix: **`OSDiversityAssignment` at a
200 s interval takes over four minutes per run** — it solves an LP per mutation, so
that one mechanism is roughly four hours of a full grid. It is one of the four
already commented out of the inherited `MTDScheme` default pool, and any grid
naming all eight mechanisms should budget for it or exclude it deliberately.

## 7. What Marc has to rule on

1. **Axis 3's badge** — re-score E3(b) on the crossover form (§3), or accept the
   ranking form with its power caveat stated in the criterion entry. The badge is
   currently DEMONSTRATED on the branch.
2. **Which sink implementation lands** (§6), and whether the additive artefacts are
   grafted on.
3. **Whether `sink_policy.md` §5's stated reason is narrowed** (§4). This is
   editorial and changes no result.
