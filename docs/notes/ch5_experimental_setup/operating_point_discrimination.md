---
status: durable
chapter: ch4_methods
created: 2026-08-01
updated: 2026-08-01
---

# An evaluation must show its operating point can discriminate its metric before reporting it

## Position in the dissertation

An experimental-design argument for the evaluation chapter: the rule the
comparative experiment's design obeys and every earlier run of this project
unknowingly violated. It is the cheapest and most transferable methodological
finding the project produced.

## The idea

Every run this project published before its comparative experiment was taken at
a defensive mutation interval of two hundred seconds — the default the
simulation platform ships with, adopted by every earlier run of this project
without examination. At that interval, it turns out, the evaluation's headline success
metric could not have produced a result. Sweeping the defender's tempo alongside
the attacker's revealed that at two hundred seconds *neither* attacker — not the
intelligence-derived attacker this project built, and not the platform's own
scripted attacker — ever completes the objective the success metric is defined
on. The metric sits at zero on both sides of every comparison, and the objective
only becomes reachable when mutations are spaced roughly eight times further
apart. Until the sweep ran, nobody knew.

The analytic literature on this contest names the regime precisely: when the
defence's churn outpaces the attacker's completion, an attack that must restart
after each mutation can never succeed — Anderson et al. (2016) derive exactly
this in closed form. What the literature supplies is the existence of the
region; what an evaluation must supply for itself is which side of the boundary
its chosen operating point sits on, because a success metric measured inside the
region is pinned at its floor and can no longer distinguish anything — one
defence from another, a strong attacker from a weak one, or the things the
evaluation exists to distinguish from each other. A zero measured there reports
a property of the region, not of the attacker. The later comparative experiment
confirmed this reading directly: relaxing the interval by a factor of ten lifted
the scripted attacker's success rate off the floor, from eight to thirty-three
runs in eighty, while the profiled attacker's zero survived the relaxation —
which is how the evaluation learned that one zero was regime-induced and the
other was real. Inside the region the two zeros are indistinguishable.

The degeneracy is metric-specific, which is what makes the check actionable
rather than fatal. Compromise breadth and elapsed time continued to respond to
both the attacker and the defence throughout the degenerate region — the
project's tempo conclusions survive because they lean on those measures — so the
consequence of the check is not that the operating point is unusable but that
each reported metric must be paired with an operating point at which it has room
to move. The comparative experiment's design absorbed the rule directly: it
carried the mutation interval as an experimental dimension, keeping the
inherited interval because it is the only point comparable with earlier runs and
adding a second interval beyond the feasibility boundary at which success-rate
measures discriminate, with every claim stating which interval it was measured
at.

The transferable rule is almost embarrassing to state: **before reporting a
metric, establish that the operating point permits the metric to vary.** The
check is cheap — sweep the one parameter that sets the contest's tempo and watch
whether the metric comes off its floor — and it is not made redundant by
experience, because this region was found by a project that had already run
hundreds of simulations at the operating point without suspecting it. A floor is
silent: a metric pinned at zero looks identical to a metric honestly reporting
failure, and only moving the operating point tells them apart. Nothing about the
rule is specific to moving-target defence; any evaluation whose metric is gated
on completing a multi-step contest — a race between an attacker's progress and a
defender's disruption — has a degenerate region somewhere on its tempo axis, and
either knows where it is or is possibly inside it.

The negative scope: this note does not claim the inherited interval was a wrong
choice for the studies that inherited it — their questions may not have run
through the gated metric, and no published result is here asserted to be an
artefact. The claim is about this project's own runs, where the region is
demonstrated, and about the design rule that follows.

## Evidence and repo anchors

- The sweep that found the region, its pre-registered criteria, and the interval
  table: [`../../implementation/pipeline/ogasp/rate_feasibility_study.md`](../../implementation/pipeline/ogasp/rate_feasibility_study.md)
  §7 (C4, C5).
- The confirmation that the region is a property of the regime, and the
  profiled attacker's zero is not:
  [`../../implementation/pipeline/ogasp/experiment_02_findings.md`](../../implementation/pipeline/ogasp/experiment_02_findings.md)
  §2.1, §17.
- The standing constraint the finding placed on the model's scorecard:
  [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md)
  §(b).
- The churn-versus-completion analysis: Anderson, Mitchell, Chen 2016, via the
  extraction [`../../sources/extractions/mtd_scan_disruption.md`](../../sources/extractions/mtd_scan_disruption.md)
  (§III locator).
- The burden-of-proof note this rule now rides inside:
  [`evaluation_burden.md`](evaluation_burden.md) (second instalment); the
  headline result whose design obeys it:
  [`defence_ranking_inversion.md`](defence_ranking_inversion.md).

## Revisit conditions

- If a survey of the surrounding evaluation literature is undertaken and finds
  the discriminability check *is* standard practice, the novelty framing
  softens to a restatement; the rule itself is unaffected.
- If a future substrate change moves the feasibility boundary, the specific
  intervals here are re-measured, though the rule survives any boundary.
- If a metric is introduced that is not gated on contest completion, the rule
  applies to it vacuously and this note does not constrain its operating point.
