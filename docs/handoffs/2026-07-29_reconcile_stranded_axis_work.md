---
status: open
priority: do this before anything else on the chain
created: 2026-07-29
---

# Reconcile the stranded axis-6, axis-7 and experiment-2 work into `dev` — three completed studies and three badge moves currently exist on branches `dev` cannot see

**Chain position: blocking.** Every other open handoff, and every statement in
[`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md),
assumes work that is not on `dev`. Until this lands, `dev` misrepresents the
state of the project — in the specific direction of **understating** it.

## State of play — what is where

`dev` (currently `c99b5d9`, shared with `perf/mtd-mechanism-cost-audit`) carries
the attacker-state seam, both axis mechanisms **as built**, and the intent-audit
substrate dispositions. What it does **not** carry is everything those mechanisms
produced.

| artefact | on `dev` | where it actually lives |
|---|---|---|
| axis-6 utility modulator (code) | yes | — |
| axis-7 learner (code) | yes | — |
| `incentive_rationality.md` | **319 lines, pre-run** | 502 lines on `feat/axis134-demonstration-arms` |
| `learning_capability.md` | **382 lines, §7 is a stub** | 657 lines on `feat/axis134-demonstration-arms` |
| axis-6 λ sweep (1 800 runs) | **absent** | recorded only on `feat/axis134-demonstration-arms` |
| axis-7 κ/ρ sweep (2 400 runs) | **absent** | recorded only on `feat/axis134-demonstration-arms` |
| criterion axes 6 and 7 | **NOT ADDRESSED** | **DESIGNED** on `feat/axis134-demonstration-arms` |
| sink-retrace design | absent | two competing versions (below) |
| experiment 2 (2 760 runs) | absent | `feat/exp02-ashen-lynx` |
| criterion axis 3 | **DESIGNED** | **DEMONSTRATED** on `feat/exp02-ashen-lynx` |

The stub is the sharpest symptom. On `dev`, `learning_capability.md` §7 reads
*"(To be completed by the run. Nothing is written here until the runs exist.)"* —
and the runs exist. 4 200 swept runs and roughly 460 lines of analysis are
reachable from one feature branch and nowhere else.

**The two axis handoffs are therefore still open on `dev` and must not be deleted
yet.** Their work has shipped, but not to `dev`; deleting them here would leave
the branch with neither the brief nor the result. They are retired by *this*
handoff's merge, not before it.

## The one genuine conflict

Two independent sink-retrace implementations exist, built in parallel by
concurrent sessions. They agree on the diagnosis and differ on one clause.

- `feat/axis134-demonstration-arms` — `sink_retrace_design.md` plus an
  implementation. Repairs the handoff's failure-verdict rule by moving it to the
  **predecessor**, and adds a **one-shot suppression** of the edge that led into
  the sink.
- `feat/exp02-ashen-lynx` — `sink_policy.md` plus an implementation and 33 tests.
  Drops the verdict clause entirely on the grounds that the nets make it
  unnecessary: no sink's in-neighbour has out-degree below 6, and the heaviest
  edge into any sink carries weight 0.111, so the expectation is ~1.1 retraces
  per encounter.

Both reached the same non-obvious finding — the handoff's recommended rule cannot
fire at a sink, because a sink has no out-set to condition. **Recommendation:
keep the `feat/axis134-demonstration-arms` version.** It is the one the axis-1/3/4
work builds on, and the one-shot suppression is a strictly stronger guarantee that
costs one declared rule. The other implementation's contribution is its §3
out-degree inventory, which should be lifted into the surviving record as the
empirical argument that the suppression is a belt-and-braces measure rather than a
load-bearing one.

## Recommended approach

1. **Reconcile in dependency order**, not chronological order: the axis-6/7
   records and their criterion badge moves first (they are additive and conflict
   with nothing), then the sink policy (pick one, per above), then experiment 2
   (which depends on both).
2. **Re-run experiment 2's analysis after the merge, do not re-run the matrix.**
   The 2 760 runs were taken on the substrate *after* the intent-audit
   dispositions, which `dev` has. If the surviving sink implementation differs
   behaviourally from the one those runs used, re-run only the sink sub-study —
   the policy fires on three profiles and the rest of the matrix is untouched by
   it.
3. **Reconcile `apt_model_criterion.md` by hand, not by merge tool.** Three badge
   moves land on it from two branches (6 and 7 from one, 3 from the other) plus a
   §(f2) section and lifecycle-trigger edits. A textual merge will succeed and
   produce a scorecard whose summary paragraphs contradict its table.
4. **Verify the badge count after reconciliation** against
   [`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)
   §2, which states the intended end state: two DEMONSTRATED, four DESIGNED, two
   NOT ADDRESSED. If the merged file says anything else, something was lost.
5. **Delete the three shipped handoffs in the merge commit** —
   `2026-07-28_axis6_incentive_rationality.md`,
   `2026-07-28_axis7_learning_capability.md`,
   `2026-07-28_axis134_demonstration_arms.md` — and
   `2026-07-27_sink_retrace_experiment2.md`. All four have shipped; they are open
   on `dev` only because their work is.

## Validation gate

Done when `dev` carries: both filled-in axis records with their sweep verdicts;
one sink-retrace implementation with its tests green; the experiment-2 findings
record; a criterion whose table reads 2 / 4 / 2 and whose prose agrees with it;
and four fewer handoffs.

## Hard constraints

- **Nothing is re-run to make it merge.** These are recorded results; a merge is
  bookkeeping, not an experiment.
- **No badge is re-decided during reconciliation.** Each was decided against a
  pre-registered criterion on its own branch; a merge does not re-open it.
- Branch and commit rules from [`../workflows/session_workflow.md`](../workflows/session_workflow.md);
  never push; never force.

## Reading list

- `git log --oneline --graph dev feat/axis134-demonstration-arms feat/exp02-ashen-lynx` — the divergence, first.
- `docs/implementation/pipeline/ogasp/model_scope_freeze.md` — the intended end state, and why it matters that the badges are right.
