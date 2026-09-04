---
status: durable
chapter: ch6_results
created: 2026-08-01
updated: 2026-08-01
---

# An MTD evaluation's recommendation is a function of its threat model

## Position in the dissertation

The evaluation chapter's headline result: the finding the chapter is organised
to deliver, and the discharge of the divergence half of the pre-declared burden
of proof. The chapters before it argue that behavioural fidelity in the attacker
model *should* change an evaluation's answer; this is the experiment in which it
did.

## The idea

A simulated evaluation of moving target defence must choose an attacker to
evaluate against, and the choice is usually treated as a formality — a scripted intruder that walks
the simulator's own procedure, standing in for "the attacker" in general. The
result reported here is that the choice is not a formality. Two attackers run
against the same defences, on the same simulated network, under identical
conditions, produce defence rankings that are very nearly opposite: an evaluator
using one attacker would deploy close to the reverse of what an evaluator using
the other would deploy. **The ranking of defences is a function of the threat
model**, and an evaluation that fixes its attacker by default has silently fixed
its recommendation the same way.

The two attackers are these. The first is the simulator's inherited attacker: a
scripted six-phase intruder, native to the platform this work extends, that
walks the simulator's own precondition order — scan, enumerate, exploit,
propagate — as fast as the environment permits. It is the attacker against which
this simulator lineage's published results were produced. The second is the
attacker built by this project: a campaign envelope derived from analyst-curated
cyber-threat-intelligence corpora, which traverses adversary tactics in the
orders and proportions observed campaigns exhibit, conditioned on an operational
objective, spending much of its time in activity that touches nothing the
simulator scores. The two were run against a family of seven moving-target
defence conditions — four single mechanisms (address shuffling, topology
shuffling, operating-system diversification, service diversification) and three
composition schemes — with the defence's mutation interval normalised across
conditions so that tempo could not confound the comparison, ten seeds per cell.

The criterion was fixed before the run existed: the experiment pre-registered,
among its conclusions, whether the rank order of defence conditions by
suppression of compromise breadth differs between the two attackers, to be
reported as a rank comparison whichever way it fell. It fell about as far as it
could. At the evaluation's operating mutation interval, the rank correlation
between the two attackers' defence orderings is **−0.893** — not merely
different orderings, but nearly reversed ones. Service diversification, the
strongest defence against the inherited attacker, suppresses its compromise
breadth by roughly ninety per cent while suppressing the profiled attacker's by
thirty-seven; topology shuffling does almost exactly the reverse, suppressing
the inherited attacker by eighteen per cent and the profiled attacker by
eighty-nine.

The mechanism is legible, which matters more than the coefficient. The inherited
attacker is a *vulnerability-exploiting* actor: it converts scanned services
into compromised hosts, so a defence that re-rolls services and their versions
destroys precisely the resource it depends on, while moving hosts around barely
inconveniences a procedure that re-scans on every step. The profiled attacker is
a *position-driven* actor: it advances by accumulating and holding position
across a long campaign, spending over a third of its visits in tactics that
dispatch no scoreable action at all, so a defence that shuffles topology and
addresses destroys precisely the resource *it* depends on — while re-rolling a
service it was never going to exploit costs it comparatively little. Each
attacker is best countered by the defence that attacks its dependency; the two
attackers depend on different properties of the environment; therefore the
rankings cross. Nothing in that argument is statistical, and the crossing would
be expected to survive re-runs even where individual magnitudes move.

What this result is not must be stated as plainly as what it is. The profiled
attacker is not a stronger attacker — it is dramatically weaker on every
headline security metric, compromising roughly a seventh of the hosts the
inherited attacker does and reaching the simulator's objective zero times in
twelve hundred runs. The claim has never been that greater behavioural fidelity
produces a more dangerous adversary, and this experiment reinforces the
opposite. The claim is about the evaluation, not the attacker: fidelity changed
*which defence the evaluation recommends*, and it did so while losing on every
measure by which attackers are conventionally compared. An attacker model is an
instrument for measuring defences, and this result is what it means for the
instrument to matter.

Three boundaries travel with the finding, disclosed as design facts rather than
discovered later. First, ten seeds per cell supports a rank comparison and not a
significance test; two prior sensitivity studies on this model established that
sample size cannot separate quantities this close, so the inversion is reported
as directional. Second, the inversion is a property of the high-pressure regime:
at a mutation interval ten times longer — chosen deliberately, because the
operating interval sits in a region where success-rate metrics cannot
discriminate — the rank correlation rises to +0.286, still far from agreement
but no longer an inversion, because at that tempo the defences barely suppress
the profiled attacker at all. Whatever moving-target defence buys against a
position-driven attacker, it buys at tempo. Third, and most consequentially: the
profiled attacker's behaviour reaches the simulator through a declared mapping
from adversary tactics onto the simulator's six executable actions, and that
mapping is a chosen input parameter, not a recovered truth. How much of the
inversion is carried by the intelligence-derived behaviour and how much by the
mapping cannot be separated from within this run; a mapping-sensitivity study is
the natural next instrument. A further reading discipline: in this simulator
compromise is never revoked, so "suppression" throughout means slower
acquisition of hosts within the horizon, not hosts taken back.

The comparison is also strictly within this simulator: no magnitude here is
comparable to the published results of the lineage this platform descends from,
and no profile's behaviour is claimed to reproduce any real campaign — each is
one instantiation of a behavioural envelope under a declared policy. What
survives all of these boundaries is the form of the conclusion, and it is the
form that generalises: two attackers that depend on different properties of the
protected system are protected by different defences, so an MTD evaluation's
recommendation inherits its threat model's dependencies. An evaluation that
wants its recommendation to transfer must either argue that its attacker's
dependencies match those of the adversary it fears, or vary the attacker and
report the ranking's sensitivity — exactly as it already varies and reports the
parameters it considers uncertain.

## Evidence and repo anchors

- The comparative run, its pre-registered criteria (E5), the ranking tables, the
  interval dependence and the mechanism reading:
  [`../../implementation/pipeline/ogasp/experiment_02_findings.md`](../../implementation/pipeline/ogasp/experiment_02_findings.md)
  §2, §9–§10 — note its reconciliation banner: the sink-policy cells of three
  profiles ran under a superseded implementation variant (divergence bounded
  small; re-take is an open ruling).
- The burden this discharges, and the stability half that precedes it:
  [`evaluation_burden.md`](../ch5_experimental_setup/evaluation_burden.md).
- The degenerate-region constraint that forced the second interval:
  [`../../implementation/pipeline/ogasp/rate_feasibility_study.md`](../../implementation/pipeline/ogasp/rate_feasibility_study.md)
  §7 (C5); the standalone argument is
  [`operating_point_discrimination.md`](../ch5_experimental_setup/operating_point_discrimination.md).
- The attacker model's honest scorecard, and where this result sits in it (it
  scores on no axis, deliberately):
  [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md)
  §(f2), §(g); the model boundary:
  [`../../implementation/pipeline/ogasp/model_scope_freeze.md`](../../implementation/pipeline/ogasp/model_scope_freeze.md) §1.
- The mapping caveat's record:
  [`../../implementation/pipeline/ogasp/controller.md`](../../implementation/pipeline/ogasp/controller.md)
  and [`../../implementation/pipeline/ogasp/controller_mapping_v2.md`](../../implementation/pipeline/ogasp/controller_mapping_v2.md).
- The measurement-failure companion (why several inherited instruments could not
  see this result): [`../ch7_discussion/instruments_fail_silently.md`](../ch7_discussion/instruments_fail_silently.md).

## Revisit conditions

- If the mapping-sensitivity study runs and the inversion does not survive
  plausible alternative mappings, the claim narrows from "fidelity changes the
  recommendation" to "the mapping changes the recommendation", and the note is
  rewritten around that weaker and different result.
- If the sink-policy cells are re-taken under the landed implementation and any
  ranking position moves, the tables here are re-read against the new record.
- If a re-run at a seed count that supports significance testing overturns the
  rank comparison, the directional claim falls with it.
- If the defence family is extended (in particular by the reactive,
  attacker-sensing defender the project defers), the ranking must be recomputed
  before this note's tables are quoted for the extended family.
