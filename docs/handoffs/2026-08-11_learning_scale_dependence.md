---
status: open
created: 2026-08-11
related: 2026-08-11_fsm_hosted_learning_control_arm.md
---

# Test the first-principles prediction that attacker-learning advantage is scale-dependent — and if it is absent, diagnose whether the cause is the mechanism or the implementation

> **Sibling shipped; a third handoff is open (updated 2026-08-11).** This handoff
> sweeps the **existing** L3 routing-belief learner (axis 7) across *host-count*
> scale, and **as of 2026-08-11 it has not been executed** — no scale sweep
> exists on `dev`. The sibling it originally pointed at
> (`2026-08-11_probability_shaped_exploit_learning.md`) has since been executed
> and deleted: it landed as the compound-exploit-learning mechanism
> ([`../implementation/pipeline/ogasp/exploit_learning.md`](../implementation/pipeline/ogasp/exploit_learning.md))
> and returned a **measured negative** — the mechanism operates on the movement
> attacker but moves no outcome, diagnosed to out-of-order-FSM churn, axis 7
> holding at DESIGNED
> ([`../implementation/pipeline/ogasp/exploit_learning_findings.md`](../implementation/pipeline/ogasp/exploit_learning_findings.md)).
> A third handoff,
> [`2026-08-11_fsm_hosted_learning_control_arm.md`](2026-08-11_fsm_hosted_learning_control_arm.md),
> now hosts that mechanism on the native FSM attacker as a positive-control arm,
> to discriminate the structural from the mechanism-limited reading of that null.
> Three distinct instruments — routing learner × scale (this), exploit learner ×
> pool (shipped), exploit learner × host attacker (open) — a session picking up
> any of them should read all three records to avoid conflation.

## State of play

The within-run learning capability (axis 7,
[`../implementation/pipeline/ogasp/learning_capability.md`](../implementation/pipeline/ogasp/learning_capability.md))
has only ever been swept at a **single network scale** — the 150-node /
`v2_partial` configuration inherited from experiment 1. On that one scale the
capability demonstrably operates (blocked fraction falls within runs) and
demonstrably does **not** help (compromise breadth *falls* as κ rises: 6.50 →
0.80 hosts on `aggregate` at κ = 4; §7.6). The recorded cause is a credit-signal
defect — the learner updates on the binary routing verdict, scanning succeeds
more often than exploiting, so a confident learner concludes reconnaissance pays
and abandons the objective. Axis 7 sits at DESIGNED for exactly this reason.

**What has never been tested is whether that verdict holds across scale.** Marc's
first-principles intuition, and the premise of this handoff: learning advantage
should *surface at smaller service/host counts*, because the objective is fewer
hops away, belief over a smaller tactic-place set saturates faster relative to
the horizon, and fewer MTD mutations intervene to decay it before it could pay.
On this reasoning the single-scale null is under-powered, not conclusive: it may
have measured the mechanism at precisely the scale where it *cannot* show, and
generalised a scale-specific artefact into a mechanism verdict.

This handoff is **predicated on producing that result** — a scale at which the
learner's accumulated belief converts to breadth or stage advance against its own
ablation arm. If the sweep produces it, axis 7's evidence changes materially. If
it does not, the null is itself informative *only once the alternative
explanation is excluded*: that the effect is absent not because the mechanism is
scale-invariant but because **something in the implementation prevents belief
from being exercised before it decays** — a technical defect, not a law.

## Recommended approach

Pre-register before running (house discipline; commit order is the audit trail).

1. **Add network scale as the swept factor**, holding the learning family, κ band,
   forgetting fraction ρ and seeds fixed. Sweep at least three scales spanning
   well below the inherited 150 (candidate: ~25 / ~50 / ~150 host counts, matched
   to Zhang's network sizes so the axis is shared with the evaluation chapter).
   Report against **both** the no-learning ablation arm and the destination-only
   learner, exactly as the readiness study did — the ablation arm is the control
   that matters, because the substrate's own state accumulation improves it too.
2. **Score on breadth and stage advance, never on friction.** The
   [`learning_readiness_findings.md`](../implementation/pipeline/ogasp/learning_readiness_findings.md)
   warning binds here: the representations are indistinguishable to three decimals
   on every friction-shaped measure. Blocked-fraction decline is *not* evidence
   for this hypothesis and must not be read as such.
3. **Commit the confirmatory prediction and the two null branches before the
   run.** Prediction: breadth-over-ablation-arm rises as scale falls, monotone in
   the swept scales. Null branch A (mechanism): the learner still fails to exceed
   its ablation arm at every scale — the credit-signal defect is scale-invariant,
   and small scale does not rescue it, which sharpens the axis-7 finding rather
   than overturning it. Null branch B (implementation): breadth over the ablation
   arm is *flat in scale* in a way inconsistent with belief accumulating at all —
   which points at a defect, not a mechanism limit, and triggers step 4.
4. **Diagnostic, only on null branch B.** Instrument, do not tune. Candidate
   technical causes to check *before* concluding anything:
   - **decay outrunning accumulation** — does the interrupt count (hence
     forgetting count) fail to fall with scale, so belief is wiped as fast as it
     forms regardless of network size? (learning_capability §7 records ~42
     interrupts/run at 150 nodes; confirm whether that scales down.)
   - **belief never consulted before the objective** — at small scale the token
     may reach its objective place in fewer decision points than it takes the
     Laplace estimate to depart from its uniform prior, so the learner is
     *structurally* mute on short paths. Measure decision-points-to-objective
     against estimate-departure, per scale.
   - **the credit-signal defect dominating** — the abandonment pathology (§7.6)
     may simply swamp any scale effect; if so, a minimal progress-carrying credit
     signal is the only thing that would let scale matter, and that is the axis-7
     credit-assignment redesign, out of scope here but named as the blocker.

   The distinction between "small scale does not help because the mechanism is
   sound and the verdict says so" (branch A) and "small scale does not help
   because belief never gets exercised" (branch B) is the whole diagnostic value
   of this handoff, and it is exactly the distinction the single-scale sweep could
   not draw.

## Validation gate

The work is done when there is, on record and pre-registered: (i) a scale sweep
of the learner against its ablation arm scored on breadth and stage advance;
(ii) a committed verdict on which of the three branches the evidence supports;
and (iii) if branch B, a named technical cause with an instrument reading behind
it — not a fix, a diagnosis. A result that reads "learning helps at small scale"
is only admissible if it beats the ablation arm on a progress measure; beating
the destination-only learner on friction is not the gate.

## Hard constraints

- **No value chosen because it improves an outcome.** The κ band, ρ, and the
  scale levels are fixed before the run; the confirmatory prediction and both null
  branches are committed before any output exists. This is a hypothesis test, not
  a search for a scale that flatters the mechanism.
- **The degenerate region** — no success-rate-shaped claim at the 200 s operating
  interval. Score breadth and stage advance, which discriminate throughout.
- **No time-denominated cross-arm comparison** (S3-R pricing asymmetry).
- **S2 action-set freeze** — the credit-signal redesign named in step 4 is a
  substrate/movement-layer change and is *out of scope*; this handoff sweeps and
  diagnoses the existing mechanism only.
- Branch / commit / push rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.
- Australian English.

## Reading list

- [`../implementation/pipeline/ogasp/learning_capability.md`](../implementation/pipeline/ogasp/learning_capability.md)
  §7.6 — the breadth-collapse table and the credit-signal defect; this handoff's
  entire premise is that §7.6 was measured at one scale.
- [`../implementation/pipeline/ogasp/learning_readiness_findings.md`](../implementation/pipeline/ogasp/learning_readiness_findings.md)
  — the friction-vs-breadth measurement warning; why step 2 forbids friction scoring.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(d) axis 7 — the badge this could move, and the credit-signal requirement it fixes.
- [`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
  — the scale/defence factor design this sweep should share an axis with.

## Out of scope (explicitly)

- The credit-assignment redesign (progress-carrying reward). Named as the likely
  blocker on null branch A; not built here.
- Any tuning of κ, ρ, or the learning representation to produce a positive result.
- MTD-crossed cells — run this no-MTD first to isolate the scale × learning
  interaction before adding the mutation regime as a third factor.

## Return format

Report framed in terms of the thesis, succinctly: whether the learning-advantage
prediction holds at small scale, which of the three branches the evidence takes,
whether axis 7's badge or evidence moves, and — if branch B — the named technical
cause. Point at the committed sweep record for the detail.
