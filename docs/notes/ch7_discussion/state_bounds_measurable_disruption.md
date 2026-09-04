---
status: durable
chapter: ch7_discussion
created: 2026-08-05
updated: 2026-08-05
---

# A moving-target defence can only destroy the kind of state the attacker model carries, so the attacker's state representation bounds what an evaluation can measure

## Position in the dissertation

The discussion chapter's account of what substituting a campaign-structured
attacker buys the evaluation, argued at the level of the defence rather than the
attacker. It converts a measurement taken on one simulator into a constraint on
how any moving-target defence should be evaluated, and it is the note that
explains why the attacker-model contribution is a contribution to *evaluation*
and not only to adversary modelling.

## The idea

Moving-target defence is justified by what it takes away from an attacker. The
survey literature states the mechanism plainly: rearranging the attack surface
renders the exploratory knowledge the attacker has accumulated useless
(Alshamrani et al. 2019). That is a claim about *knowledge*, and it is the claim
the field's evaluations are meant to test. What follows is that a simulator can
only register the claim to the extent that its attacker has accumulated
knowledge in the first place — and the incumbent attacker of this lineage has
almost none.

The inherited attacker carries exactly two pieces of state: which host it is
currently working on, and which step of a fixed six-step procedure it is
executing. When a mutation interrupts it, both are duly taken. It pays a time
penalty, a network-layer mutation clears its host, and it is then returned to an
earlier step of the same procedure, chosen by the mutating layer — a
network-layer change sends it back to host discovery, an application-layer
change to port scanning. The disruption is faithful to what the source paper
specifies, a time penalty and a forced re-scan (Brown et al. 2023), and it is
complete: there is no third thing the attacker holds for the defence to reach.
An evaluation built on it can therefore measure moving-target defence as a
position tax and a procedure restart, and it cannot measure anything else, not
because the defence is weak but because the adversary has nothing further to
lose.

The campaign-structured attacker changes what is available to be destroyed. It
does not execute a fixed procedure; it walks a campaign whose stages are drawn
from analyst-curated intrusion reports, choosing its next stage probabilistically
from where it currently stands. Its state is therefore a *position in a
campaign*, and that is a kind of state the incumbent does not possess. The
disruption reaches it through the same shared cost — the identical time penalty,
the identical loss of host on a network-layer mutation, and this was verified
mechanism by mechanism rather than assumed — but the succession differs. Instead
of a forced return to a fixed step, the interruption is read as a failed action,
and the failure re-weights the attacker's choice of next stage. The weighting is
asymmetric by design: a step backwards through the campaign is roughly two and a
half times more likely after a failure than a step forwards, where after a
success the preference is reversed. The behaviour the disruption produces is
regression through the campaign, which is the behaviour the literature's claim
describes.

**This is the sense in which behavioural fidelity is a contribution to the
evaluation and not only to the adversary.** The campaign-structured attacker is
the first attacker on this simulator that has a campaign to be set back in, so it
is the first against which the defence's stated mechanism is expressible at all.
The comparison between the two attackers is not a comparison of two adversaries
of differing realism; it is a comparison between an instrument that can register
the defence's claim and one that structurally cannot.

Three concessions travel with that, and together they fix where the claim stops.

The first is that the regression is a **declared policy rather than an emergent
consequence**. The asymmetry between falling back and pressing on is a value
fixed by the modeller before any run took place, on stated grounds and with its
alternatives ranked, but fixed nonetheless. Nothing in the simulator derives it.
So the defensible statement is that the model *gives the defence a state to
attack*, not that the defence has been *shown to destroy campaign progress* — the
strength and the limitation are the same fact, since a state representation rich
enough to express the claim is also rich enough to have been specified to
express it.

The second is measured, and it is the more deflating of the two. Between roughly
half and three-quarters of all interruptions arrive while the attacker is between
actions — occupying a stage that consumes time but dispatches nothing — and the
model deliberately raises no outcome there. Such an interruption costs the
attacker its time penalty and re-routes it not at all. For the two surface-churning
mechanisms the share is around seven in ten. So the dominant *realised* effect,
even against the attacker that has a campaign to lose, remains a time tax; the
regression the previous paragraphs describe applies to the minority of
interruptions that catch the attacker mid-action. An evaluation that reported
the mechanism without this proportion would overstate it considerably.

The third is that there is one channel where destruction is unambiguous, and it
is not the campaign position at all. When the attacker is given the capacity to
learn which of its stages tend to pay — the capability the field's surveys most
often ask for and most rarely build (Cho et al. 2020) — that learned estimate is
degraded on every single mutation, irrespective of the mutating layer, of which
action was running, and of whether any outcome was raised. This is the one place
where the defence reaches something the attacker genuinely accumulated, and the
measured result is that it is severely effective: most of the learner's advantage
is gone once a modest fraction of the estimate is lost per mutation. It is also
a defence effect that none of the conventional security metrics registers, since
what has been destroyed is an estimate rather than a foothold — which is the
argument of this note restated at one further remove.

## What this does not claim

It does not claim that the campaign-structured attacker is more realistic, and
nothing here rests on it being so; the argument is about what the evaluation can
see, not about whose adversary is truer. It does not claim that the defence is
more effective against it — on one axis the measurement runs the other way, with
application-layer mechanisms delivering materially less disruption to the
campaign-structured attacker than to the incumbent, because that attacker spends
much of its time in reconnaissance-shaped stages the interruption rule has always
exempted. And it does not claim that the incumbent attacker is defective. It is
faithful to its specification. The point is narrower and, if anything, more
uncomfortable: fidelity to a specification is not the same property as adequacy
as a measuring instrument, and an evaluation inherits whichever one its attacker
happens to have.

## The generalisable form

When a defence's claim is about destroying what an attacker knows, the attacker
model's state representation is part of the measuring apparatus, and its
omissions become the evaluation's blind spots rather than the defence's
limitations. The practical consequence for reporting is a single sentence that
the field's evaluations do not currently carry: **state what state the attacker
had.** A result that a defence "disrupted the attacker by X" is uninterpretable
without it, because the same defence acting identically will produce a different
X against an adversary holding a different amount.

## Evidence and repo anchors

- Per-mechanism verification of the disruption channels across both attackers —
  the executed interrupt table, the realised traffic, the share of interruptions
  landing between actions, and the class-versus-arm asymmetry:
  [`../../implementation/disruption_wiring.md`](../../implementation/disruption_wiring.md).
- The six disruption channels and their class-level pricing:
  [`../../implementation/boundary_attacker_defender_channels.md`](../../implementation/boundary_attacker_defender_channels.md).
- The declared success/failure routing policy, its rule tiers and the rationale
  for the backward/forward asymmetry:
  `data/ogasp/controller/outcome_rules.json` and
  [`../../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../../implementation/pipeline/ogasp/success_failure_overlay_design.md).
- The learning capability, its decay on mutation, and the sweep behind "severely
  effective":
  [`../../implementation/pipeline/ogasp/learning_capability.md`](../../implementation/pipeline/ogasp/learning_capability.md).
- Source extractions: [`../../sources/extractions/alshamrani2019.md`](../../sources/extractions/alshamrani2019.md)
  (§IV-C-2-B, the knowledge-destruction statement),
  [`../../sources/extractions/cho2020.md`](../../sources/extractions/cho2020.md)
  (§V-D, the attacker-learning asymmetry). The Brown time-penalty-and-forced-re-scan
  clause is a *citation anchor to reconcile* against the primary source before
  this note is drafted into the chapter.
- Sibling notes: [`learning_without_context.md`](learning_without_context.md)
  (why the learning capability reduced friction without improving progress) and
  [`procedural_mismatch_artefact.md`](procedural_mismatch_artefact.md) (the
  complementary case, where the simulator's encoded procedure manufactures
  attacker failure).

## Revisit conditions

Three things would reframe this note. If the proportion of interruptions arriving
between actions were changed — by re-mapping which campaign stages dispatch an
action, which is a chosen input rather than a finding — the second concession's
magnitude moves and could move a long way, since that proportion is a property of
the mapping and not of the defence. If the declared routing policy's
backward-versus-forward asymmetry were derived from evidence rather than declared,
the first concession weakens and the claim strengthens correspondingly. And if a
learning capability were built whose credit signal carried progress rather than
mere permission to act, the third paragraph of concessions becomes the note's
lead rather than its coda, because the channel where the defence demonstrably
destroys something would then also be the channel that matters to the attacker's
success.
