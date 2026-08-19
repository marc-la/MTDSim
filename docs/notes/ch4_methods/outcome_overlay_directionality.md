---
status: durable
chapter: ch4_methods
created: 2026-08-14
updated: 2026-08-19
---

# Directionality without a stage machine — why the attacker's progress is a failure-conditioned overlay, not an imposed ordering

## Position in the dissertation

The methodology chapter's account of how the executable attacker acquires
*direction*: why a campaign that advances on success and falls back on failure
is built as one declared weight set multiplied onto the intelligence-derived
structure when the simulator reports a failure, with the intelligence-derived
structure routing unchanged on a success, rather than as an imposed kill-chain
ordering. It sits beside the structure-to-behaviour binding argument — that
note explains how the attacker's structure is executed at all; this one
explains where its sense of forward comes from — and it carries a validity
defence the examiner will press on, because the failure weights are declared
rather than measured.

## The idea

An attacker traversing a graph of adversary tactics needs some notion of which way
is forward, or it wanders: a token walking the technique structure with no outcome
feedback is as likely to retreat to reconnaissance after a successful exfiltration
as to press its advantage. The obvious fix is to impose an ordering — stamp the
tactics with kill-chain stages and forbid backward steps — and it was the first
design considered here. It was rejected, for a reason that is also a positioning
argument: a fixed stage machine contradicts the very framework the structure is
drawn from. The MITRE ATT&CK taxonomy is explicit that its tactics carry no
prescribed sequence; a campaign may return to discovery after gaining a foothold,
or re-establish command-and-control mid-operation. An attacker whose legal moves
are frozen into kill-chain order would be less faithful to the intelligence than
the graph it was built from, not more.

The design keeps direction without imposing sequence, and it does so with one
declared object. The intelligence-derived transition weights are proportions
taken from reports of campaigns that succeeded, so at each tactic they already
answer the question "given that this step worked, where did the campaign go
next". On a success verdict the token therefore routes on those weights
unchanged: the corpus is the success policy. On a failure verdict — the case the
corpus is silent on — a declared weight set multiplies the intelligence-derived
weights at the moment of the routing decision, shifting mass toward recovery and
retry. The ordering the kill-chain would have stamped in is instead *emergent*:
it lives in the measured proportions on the success branch and in one
inspectable, tunable overlay on the failure branch, rather than in a hard
constraint on the graph. Direction becomes a property of how the attacker
responds to its world, which is what an adaptive adversary's direction actually
is, rather than a rule the modeller wrote down in advance.

### The overlay is one-sided, and the one-sidedness is the honest part

The natural design is a matched pair — a success set and a failure set — and an
earlier version of this model carried one. It was retired once the asymmetry in
the evidence was stated plainly, because the pair rests on evidence of very
different strength and conflating the two halves hides the design's weakest
point. Threat intelligence is a record of what worked: incident reports and
curated attack flows document the techniques a campaign successfully chained,
because those are the steps that left forensic traces and reached an objective
worth reporting. A declared success set therefore re-answers a question the
corpus has already answered, at a weaker evidential tier, and wherever it
differs from the measured proportions it overrules evidence with judgement; its
removal was measured before it was made, and it moved no conclusion the
evaluation rests on. The intelligence says almost nothing about what an
attacker does when a step *fails* — the abandoned attempts, the retooling, the
lateral reconsideration — because failed branches rarely make it into a
published report. The failure overlay is therefore the one layer no corpus could
supply, and it is a declared model of plausible recovery behaviour rather than
an evidenced one. This is a survivorship gap in the source material, not a
defect of the encoding, and the design names it rather than papering over it:
the failure weights are a Tier-3 declared-and-swept quantity in the same sense
the unobservable tactic durations are, and they are defended the same way —
face-valid structure, a declared range, and a conclusion shown robust across
it.

### The rule that keeps the overlay from being a fitting knob

There is a tempting shortcut the design forbids explicitly: solving for the
weight set that makes the intelligence-derived nets traverse "correctly" —
advancing when they should, retreating when they should — would produce a
mathematically tidy attacker and destroy the argument. Reverse-engineering the
overlay to optimise the nets' behaviour would collapse two things that must stay
separate: the campaign structure, which comes from the intelligence, and the
outcome-response policy, which is declared knowledge about how attackers react
to failure. If the second were fitted to make the first work, the model would be
measuring its own tuning. The overlay is therefore built as a deliberately
*separate* layer from the nets, populated from general knowledge of adversary
behaviour and a distance principle — a persistent attacker does not fall from
exfiltration all the way back to reconnaissance, and a jump between distant
tactics that skips every step between them is weighted toward zero, consistent
with the sequencing that published APT lifecycle models describe (the Cyber Kill
Chain; Alshamrani et al. 2019). The literature here supplies a *consensus
constraint* on declared values, not a stage machine — the same relationship to
the evidence that the timing layer's operational validation has. The same rule
governed the decision to retire the success set: it was retired on the evidence
argument above, not because removing it made any net traverse better, and the
measured effect of its removal is reported as an outcome, not used as a reason.

### How the declared weights were defended in the absence of ground truth

No empirical source can populate these weights, so they were subjected to
adversarial scrutiny instead of empirical fitting. The candidate weight set was
stress-tested by a panel of independent reviewers instructed to red-team each
value — to argue, at each tactic pair, whether the declared recovery tendency is
what a real campaign would do after a failed step — including one reviewer
whose sole charge was to detect any drift toward reverse-engineering the nets.
This substitutes procedural rigour for measurement: it cannot make declared
weights correct, but it can make them defensible, and it converts "the modeller
picked these numbers" into "these numbers survived structured challenge from
reviewers who did not share the modeller's stake in them". The claim the
overlay licenses is exactly this modest one — a plausible,
literature-constrained, sweep-robust recovery policy — never a validated model
of attacker recovery.

## Evidence and repo anchors

- The overlay's design and the sensitivity study that swept it:
  [`../../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../../implementation/pipeline/ogasp/success_failure_overlay_design.md),
  [`../../implementation/pipeline/ogasp/weight_sensitivity_study.md`](../../implementation/pipeline/ogasp/weight_sensitivity_study.md).
- The retirement of the success set — the evidence argument, the static and
  behavioural pricing of the retired column, and the ruling:
  [`../../implementation/pipeline/ogasp/success_null_overlay_feasibility.md`](../../implementation/pipeline/ogasp/success_null_overlay_feasibility.md);
  the failure set decomposed on the page:
  [`../../implementation/pipeline/ogasp/failure_weight_decomposition.md`](../../implementation/pipeline/ogasp/failure_weight_decomposition.md).
- The intent arc and the abandoned kill-chain alternative:
  [`../../implementation/research_record/threads/outcome_overlay.md`](../../implementation/research_record/threads/outcome_overlay.md).
- The consensus-constraint sources: [`alshamrani2019`](../../sources/extractions/alshamrani2019.md) (APT lifecycle), [`hutchins2011`](../../sources/extractions/hutchins2011.md) (Cyber Kill Chain).
- Sibling notes: [`structure_to_behaviour_binding.md`](structure_to_behaviour_binding.md) (how the structure is executed at all), [`operational_validation.md`](operational_validation.md) (the Tier-3 declare-and-sweep discipline the failure overlay inherits).

## Revisit conditions

- If the sensitivity sweep shows a conclusion changes under a different failure
  overlay, the survivorship gap becomes load-bearing and this note is rewritten
  around the shape-dependence rather than around the licence.
- If a corpus of failed-attempt intelligence surfaces (red-team logs, honeypot
  traces), the failure overlay could move from declared toward evidenced, and the
  one-sidedness argument weakens.
- If the emergent-ordering claim is challenged — that a stage machine would be more
  faithful — the ATT&CK-no-ordering positioning is the load-bearing defence and
  must be stated first.
- If the success pass-through is challenged — that the corpus proportions are
  not a success policy because the corpus also records steps that preceded a
  failure — the answer is the survivorship argument itself: the flows are
  curated from campaigns reported *because* they reached an objective, so
  their transitions are the successful ones by selection; the residual is a
  limit of the source, to be disclosed, not a reason to reinstate a declared
  set over it.
