---
status: open
created: 2026-07-27
---

# Replace sink-death with edge retracing, think the consequences through before building it, then run experiment 2 across the full defence family — the comparative run the refinements exist to make meaningful

**Chain position: wave 4 — last.** The procedural change can be designed and
built as soon as the controller rebuild lands, but the *run* should consume the
re-derived weights and the timing regime, or it will need repeating. Executes
**S5**, and carries the two items the retired first-numbers handoff left open.

## State of play

**The ruling.** A run that reaches a sink should not die. The token **retraces the
edge it travelled**; the meeting also floated routing to some other node as an
alternative. This supersedes the current behaviour — a walk that reaches a place
with no outgoing edge simply stops and the run is censored — which was ruled as
the deliberate low-risk default for experiment 1 and is retained as that
experiment's arm.

**Why it matters, with numbers.** Two of the five profiles died at a sink in
almost every run: one at the impact place in nine runs of ten, another at
credential-access in ten of ten. Those walks observed a truncated window — 74 to
210 actions per run against roughly 500 for the profiles that ran to the horizon —
so their per-profile timing denominator is shorter than everyone else's, and any
per-profile comparison has to carry that caveat. Retracing removes the censoring
rather than documenting it.

**Sinks will not disappear on their own.** They are a property of the nets: a
place has no outgoing edge because the corpus drew none leaving it. Neither the
partial mapping nor the distance-weighted transitions add edges, so the sink set
is essentially unchanged by the other handoffs — retracing is still needed after
they land. The sink enumeration per profile is already recorded and is the
starting inventory. Two confirmations from the S1 study, which walked all five
nets under both mappings: the distance term does introduce exactly-zero pair
values, so a *stall* (a verdict suppressing a whole out-set) is now
representable — but no place loses its out-set at any point in the declared sweep
space, so retracing still only has sinks to handle, not stalls. And on
`v2_partial` the sink terminations do not go away: `double_extortion` still ends
at a sink in 8 of 10 seeds and `pure_steal` in 3 of 10.

**Three things this run inherits from the S1 study**
([`../implementation/pipeline/ogasp/weight_sensitivity_study.md`](../implementation/pipeline/ogasp/weight_sensitivity_study.md)),
each of which changes the design rather than merely informing it:

1. **A defence effect to confirm or withdraw.** Under `v2_partial` the profiled
   attacker compromises 2.6–4.5 hosts without MTD and roughly 0.3 with it — a
   ~90% suppression, invisible under experiment 1's mapping because the attacker
   never got far enough to be suppressed. It is stable across the whole weight
   sweep, so it is not an artefact of the declared values; whether it is an MTD
   *result* is this run's question, and it is the most promising thing on the
   table. Design the matrix so this is measurable per mechanism, not just per
   condition.
2. **A seed count.** The S1 sweep could not separate the profiles by progress at
   ten seeds — adjacent confidence intervals overlap almost everywhere — so the
   ordering half of the evaluation's burden cannot be discharged at that sample
   size whatever the weights do. Ten seeds is enough for the ASR and MTD-invariance
   claims and is *not* enough for any per-profile ordering. Budget accordingly, and
   if the budget will not stretch, say which claims the run is not powered for
   before it runs.
3. **A progression metric to replace.** Deepest lifecycle stage reached is
   saturated — all five profiles traverse to the objective stage and then fail
   against the substrate — so it cannot carry "how far did it get". This is the
   axis-1 M8b measurement gap made concrete; pick a finer measure (distinct-tactic
   coverage over time, foothold-retention duration, effort-to-breadth conversion)
   rather than reporting a metric that cannot discriminate.

**What the run still owes from the first experiment.** Two gate items were left
open when the first-numbers handoff was retired: the matrix covered only the
no-defence case against a single mechanism, so the question of whether a defence
*ranking* shifts under a profiled attacker is unanswered; and the supplementary
measurements review was folded into the criterion handoff rather than delivered
separately. The first is this handoff's to discharge. The second should be
consumed here, not re-derived: score the run against the criterion.

## Recommended approach

**Part A — design the retrace, and take its implications seriously.** The change
is three lines of code and a week of consequences; the meeting asked for the
thinking, so do that first and write it down.

1. **Define retrace precisely.** Moving the token back to the place it came from
   is the obvious reading, and it immediately raises the next question: from
   there, what stops it walking straight back into the same sink? Without an
   answer the walk oscillates between two places for the rest of the run,
   producing a great many events and no information. Candidate answers worth
   ranking: suppress the edge that led to the sink for the next selection;
   treat arrival at a sink as a failure verdict and let the failure-side
   weighting route the token away; or retrace more than one step. Recommend the
   verdict route if it works, because it reuses a mechanism that already exists
   rather than adding a special case.
2. **Decide whether retracing costs time.** It must. A zero-time retrace is an
   infinite loop in zero simulated time, which is a hang rather than a result.
   Say what it costs and why.
3. **Decide what it records.** A retrace that emits no event is invisible to
   every analysis, and the action-budget decomposition was what made the first
   experiment legible. A retrace that emits an ordinary event inflates the action
   count and quietly changes every per-action metric. Pick, and state the
   consequence for the metrics.
4. **State the comparability break.** Profiles that previously ended early will
   now run to the horizon, so their event counts and timing windows change for a
   reason that has nothing to do with the attacker being better. Experiment 2's
   numbers therefore cannot be pooled with experiment 1's, and the write-up must
   say so rather than presenting a before-and-after as an improvement.
5. **Evaluate the alternative the meeting raised.** Routing to "some other node"
   needs a rule for choosing that node, and any rule that invents a transition
   the corpus did not draw runs into the no-synthesis discipline the structural
   layer is built on. If it is taken up, it should reuse the declared
   pre-intrusion structure rather than inventing fresh edges. Record it as the
   considered alternative either way.

**Part B — run experiment 2.** Reuse the first experiment's runner shape: it
already produces seeded numbers with intervals, the action-budget decomposition,
and the figures, and its output directory is untracked and regenerable by design.

6. **Widen the matrix to the defence family**, which is the question the first
   run could not answer, and keep both attacker arms.
7. **Report the two headline statements** the evaluation needs: whether the
   profiles separate behaviourally under defence beyond the aggregate null, and
   whether any mechanism's *ranking* changes between the baseline attacker and a
   profiled one.
8. **Score the run against the criterion** from the criterion handoff, so the
   result is measured against a yardstick that existed before it.
9. **Promote the findings into a tracked record**, as experiment 1's were — the
   run workspace is gitignored, so a result that only lives there does not exist
   for the next session.

## Validation gate

Done when:

1. The retrace policy is written up with its alternatives, its time cost, its
   record semantics, and the oscillation answer — before it is built.
2. It is implemented and tested: no walk loops without consuming time, a seeded
   run is reproducible, and a profile that previously died at a sink now
   continues.
3. The comparability break against experiment 1 is stated in the record, not
   discovered by a reader comparing tables.
4. Experiment 2 has run across the defence family, seeded, with intervals,
   holding both attacker arms.
5. The two headline statements exist with numbers, phrased envelope-relative.
6. The result is scored against the criterion, and the findings are promoted into
   a tracked implementation record.

## Hard constraints

- **No tuning in reaction to the numbers.** Weight and parameter adjustments are
  reviewed work with their own handoff, never a same-session response to a
  disappointing result. This rule survived experiment 1 and matters more here.
- **Within-substrate comparability only** — internal timing measures, no
  cross-paper magnitude claims, envelope-not-actor phrasing throughout.
- **Existing defence mechanisms only.** The defender side is frozen by scope.
- **The action-set freeze (S2) holds**, and the H-coupling stays visible: a
  retrace policy that quietly routes around every unmet precondition would hide
  the finding.
- Determinism (SIM-05); Australian English; branch hygiene; never push without an
  explicit ask.

## Reading list

- [`../implementation/pipeline/ogasp/runtime_verification.md`](../implementation/pipeline/ogasp/runtime_verification.md)
  §P7 — the five ways a walk ends, the per-profile sink enumeration, and the
  superseded ruling.
- [`../implementation/pipeline/ogasp/experiment_01_findings.md`](../implementation/pipeline/ogasp/experiment_01_findings.md)
  — the setup to mirror, the numbers to be comparable against, and Finding 3.
- [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  §6.1 — the stepping lifecycle and the existing bounded-retry treatment of a
  degenerate out-distribution, which is the closest precedent for a retrace; and
  §2.7 for what S1 changed about the values this run consumes.
- [`../implementation/pipeline/ogasp/weight_sensitivity_study.md`](../implementation/pipeline/ogasp/weight_sensitivity_study.md)
  — §4 for the sweep-reporting shape to reuse, §5 for the three inheritances in the
  state-of-play above, and §1.4 for how to name an overlay version at this run's
  seam (`v2_lifecycle_distance`, alongside `v2_partial` for the mapping — the
  registry default is deliberately still experiment 1's, so an unqualified run
  silently reproduces the old arm).
- [`../implementation/pipeline/ogasp/synthetic_overlay.md`](../implementation/pipeline/ogasp/synthetic_overlay.md)
  — the declared structural layer any "route elsewhere" alternative should reuse
  rather than bypass.
- [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md)
  — metric definitions and the comparability boundary the write-up must respect.

## Out of scope (explicitly)

- Adding transitions to the nets to remove sinks. Sinks are corpus structure; the
  policy handles them at runtime.
- Building supplementary measurements — the criterion recommends them; this
  handoff does not implement them.
- Changing the mapping, the weights, or the timing in response to what experiment
  2 shows. That is the next cycle's work, reviewed.
- Dissertation chapter prose. This delivers numbers, a record, and a score
  against the criterion.
