---
status: durable
chapter: ch7_discussion
created: 2026-07-29
updated: 2026-08-01
---

# An attacker that learns from outcomes alone will route around a procedural constraint rather than satisfy it

## Position in the dissertation

The discussion chapter's account of why the attacker's learning capability
reduced its own friction without improving its progress. It generalises a result
about one simulator into a design constraint on attacker learning, and it is the
argument that motivates the remaining work on that capability.

## The idea

Attacker learning is the capability the moving-target literature most often asks
for and least often builds. Surveys of the field note that attackers are modelled
as following fixed patterns while defenders are routinely granted the ability to
learn, and call the asymmetry contrary to practice. The obvious way to answer it
is the cheap one: let the attacker keep a record of which actions have succeeded
and bias its later choices toward them. That is what was built here, and it
exposes a limitation that is worth more than the capability itself.

The mechanism is deliberately myopic. For each tactic the attacker maintains
counts of the successful and unsuccessful outcomes it has observed there, and
estimates a success probability from them under a uniform prior, so that a tactic
it has never tried sits at an even chance and is never ruled out. That estimate
then scales the probability of moving to the tactic, raised to a declared exponent
that fixes how strongly the attacker acts on what it believes. Nothing about the
arrangement is exotic, and its zero setting reproduces an attacker with no memory
at all, which makes the capability separable from everything else the model does.

It works, in the narrow sense that it does what it was built to do. Across the
declared range of the exponent the attacker drives down the proportion of its
actions that the environment refuses, and it does so *within* a run rather than
across runs — the falsifiable form of the claim, and the one that distinguishes
learning from an environment that simply becomes more permissive as the attacker
accumulates position. Against a control arm with the capability switched off, the
reduction is several times larger.

**And the attacker gets worse.** Over the same range, the number of distinct hosts
it compromises falls by roughly an order of magnitude, the proportion of its
successes that are acts of exploitation rather than reconnaissance falls from
around one in eight to one in a hundred, and its conversion of effort into breadth
deteriorates throughout. It performs more actions, succeeds at more of them, and
achieves less.

The explanation is not that the learner is badly tuned, and this is the point the
note exists to make. Whether an action succeeds in an environment of this kind
depends on **state**: an attempt to exploit a service fails not because
exploitation is a poor tactic but because this particular host has not yet been
examined closely enough for the attempt to be actionable. The quantity that would
have to be learned is therefore the success probability of a tactic *conditioned
on the attacker's current position in the procedure*. A learner keyed on the
tactic alone cannot hold that quantity. It can only hold the average taken over
every situation it has been in, and averaging over the situation discards exactly
the variable the constraint depends on. No quantity of additional experience
repairs this; it is a property of what the model can represent, not of how much it
has seen.

Denied the ability to express *this tactic pays here*, the learner does the only
thing left open to it: it learns *this tactic often fails*, and shifts its effort
onto the actions that succeed unconditionally. In this environment those are
reconnaissance and discovery, which require almost nothing to have happened first.
The attacker becomes a highly successful scanner. There is also a feedback loop
that explains why the effect grows steadily rather than saturating — as the
attacker attempts fewer intrusive actions, it spends less time in the situations
where those actions would have been actionable, which further depresses its
estimate of their worth.

The transferable claim is this. **An attacker given a learning capability whose
reward is the immediate acceptance of an action, rather than progress toward its
objective, will optimise the reward it was given.** The two come apart wherever the
environment distinguishes an action that is permitted from an action that
advances, which is to say almost everywhere. An evaluation that grants an attacker
learning on those terms will measure it optimising away from the objective and may
reasonably conclude that attacker learning is unimportant, when what it has
measured is a misspecified reward.

Two consequences follow for anyone building the learning attacker this literature
keeps requesting. The first concerns the signal: a credit signal must carry
progress — a host taken, a stage advanced, breadth gained — and not merely the
environment's acknowledgement that an action ran. The second concerns the
representation, and it is the less obvious of the two: the signal is not sufficient
on its own, because a learner keyed on the action alone cannot express a
conditional constraint however good its reward. Both must move together, and the
smallest change that does so is a key carrying some notion of the situation the
action was taken in — which need be no richer than whether the action's
preconditions were satisfied at the time.

The scope of the claim should be stated plainly. The gap between an accepted
action and an advancing one is a property of how this environment's action
vocabulary was carved, and whether it is as wide elsewhere is untested. What
generalises is not the magnitude but the failure mode, and the reason to record it
is that the failure is silent: the capability produces a metric that improves
monotonically, and only a measure of progress reveals that the attacker has been
optimising away from its objective the whole time.

## The two halves, since separated by experiment

The argument above rests on two claims that were made together and could not, when
it was written, be told apart: that the reward was misspecified, and that the
representation could not express the constraint. A learner keyed on the situation —
specifically on whether the action's preconditions were satisfied, the minimum this
note proposed — has since been built and swept against the original as a control.
The two halves come apart cleanly.

**The representation half is confirmed and is now quantified.** Given the ability to
hold "this tactic pays when I am ready for it" separately from "it fails when I am
not", the attacker stops abandoning intrusive action: the proportion of its
successes that are acts of exploitation recovers from around one in sixteen to
roughly one in ten, against one in nine for an attacker with no learning at all, and
the order-of-magnitude collapse in hosts compromised is arrested. The collapse was
therefore an artefact of what the learner could represent, exactly as argued, and
not an inevitable consequence of giving an attacker something to optimise.

**The reward half is confirmed by what did not happen.** The repaired learner
climbs back to approximately where an attacker with no memory already stood and
stops there — it recovers the ground the misrepresentation lost and gains none
beyond it. Fixing what the attacker can represent removes a defect; it does not
supply a direction. A verdict that reports only whether an action was permitted
still cannot indicate progress, however finely the situations in which it was
obtained are distinguished.

The sharper form of the original claim is therefore this: the representation and
the reward are not two candidate explanations for the same failure but two
independent requirements, and satisfying one of them buys exactly the part of the
failure it owns. There is also a methodological warning in how the two were told
apart. On every friction-shaped measure — including the within-run reduction in
refused actions that made the original capability look successful — the two
learners are indistinguishable to three decimal places. Only a measure of breadth
separates them. A study scoring this capability on the attacker's own friction
would have concluded that the representation makes no difference, which is the
opposite of what it does.

## Evidence and repo anchors

- `docs/implementation/pipeline/ogasp/learning_capability.md` — the mechanism, the
  rejected alternatives to a tactic-keyed estimator, the swept parameter bands and
  the conclusions committed before the runs existed (§3.1, §7.6, §8).
- `docs/implementation/pipeline/ogasp/model_scope_freeze.md` §5 — the
  representational argument, and why an alignment factor conditioned on the
  attacker's phase is the complement rather than the competitor of this mechanism.
- `docs/implementation/pipeline/ogasp/experiment_01_findings.md` §3 — the coupling
  between an externally-derived tactic order and the environment's own precondition
  order, which is the constraint being routed around.
- `docs/implementation/pipeline/ogasp/learning_representation.md` — the ranked
  candidate keys, the measured per-cell observation budgets, and the measurement
  showing an unmet precondition to be a deterministic failure (§1, §3, §4).
- `docs/implementation/pipeline/ogasp/learning_readiness_findings.md` — the
  4 600-run sweep separating the two halves above, its pre-registered verdicts and
  the badge decision (§1, §2.2–2.4, §4).
- Survey framing of the defender-learning/attacker-fixed asymmetry: Cho et al.
  2020 §V-D; the claim that a capable adversary learns the defence's patterns over
  time: Jalowski et al. 2026 §4.3. *(Citation anchors to reconcile against the
  tracked extractions.)*

## Revisit conditions

~~If a learner keyed on a richer context is built and *still* fails to convert
reduced friction into progress, the diagnosis here is wrong and the limitation lies
elsewhere — most likely in the action vocabulary rather than the learner.~~
**Engaged, and the diagnosis survives with a correction to this condition as
written.** The richer-keyed learner was built and does not convert reduced friction
into progress *beyond the no-learning baseline* — but the condition above was too
blunt, because it treated the two requirements as alternatives when the note's own
argument had already said they must move together. The richer key recovers
precisely the ground the poorer one lost, which is what a representational defect
predicts and what an action-vocabulary limitation would not. The outstanding
requirement is the reward, and it is now the only one.

The remaining condition stands unchanged: if the environment's action layer is ever
widened so that acceptance and progress coincide, the failure mode described here
becomes unreachable and the note narrows to a historical account of this substrate.
Should a progress-carrying reward then be built on the richer key and the attacker
*still* fail to advance, the limitation does lie in the action vocabulary, and that
is the form the original condition should have taken.
