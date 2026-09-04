---
status: durable
chapter: ch7_future_work
created: 2026-08-21
updated: 2026-08-21
---

# The emulation rung — what carries up the evaluation ladder, and what must be re-derived

## Position in the dissertation

The future-work chapter's third programme, beside the two substrate upgrades:
moving the evaluation from simulation to an emulated environment. It is where
the methodology's portability claim — that the attack model is joined to its
environment through declared inputs rather than embedded in it — is cashed
out as a concrete successor project, and where the questions a simulation
cannot answer by construction are named as that project's motivation.

## The idea

Two questions a practitioner will put to this evaluation cannot be answered
at the rung it runs on, and no amount of further simulation would change
that. The first is deployment overhead in its operational form: what does
moving the target actually cost in latency, processor time, and
reconfiguration traffic? A discrete-event simulator prices a mutation as a
timed event that occupies a resource layer while it deploys; it contains no
processor, no packets and no links, so there is nothing in it on which a
latency or bandwidth figure could be measured. The second is whether the
disruption measured here — the denial, delay and containment the defence
imposes on the modelled attacker — appears in the same shape when the
mutations are real reconfigurations and the attack actions are real tooling.
Both are properties of the rung, not defects of the implementation: the
published evaluations this work descends from sit at the same rung and are
silent on the same questions.

What this work does instead is price the defence in the simulator's own
currency, and that result is the one the successor inherits rather than
repeats. Every executed mutation leaves a record of the window during which
its resource layer was under active reconfiguration, and from those records
alone — no declared value anywhere in the measure — the evaluation reports
suppression against occupancy as a frontier. Its finding is the sharpest
reason to believe the rung change is worth making: against the inherited
attacker the best-suppressing mechanism is also the cheapest, so the defence
looks like a free lunch; against the behaviourally-grounded attacker
suppression rises near-monotonically with occupancy, and almost the whole
family is efficient — every further increment of protection is bought with
further disruption to the defender's own system. An evaluation that cannot
see cost would have recommended the free lunch. Whether that trade keeps its
shape when the costs are measured rather than modelled — when occupancy
becomes reconvergence latency and controller load — is exactly what only the
next rung can say. One boundary is owned here: the execution windows behind
occupancy are the simulator's inherited per-mechanism durations, so the
frontier's currency is availability under declared prices, not a measured
resource bill.

The portability claim is what makes this a programme rather than a rebuild,
and it can be stated precisely. What carries is the model's knowledge and
its semantics: the campaign structure aggregated from analyst-drawn incident
reports, the objective-conditioned attack profiles, the stochastic Petri-net
execution semantics, and the controller pattern that joins them to an
environment — a dwell time per tactic, a tactic-to-action mapping, and a
failure re-weighting. None of these references the simulator; the join is
two declared inputs, and swapping the environment means authoring those two
inputs against the new action vocabulary, not touching the model above them.
A natural vehicle already exists: an adversary-emulation platform that
operationalises the same tactic vocabulary (MITRE Caldera, considered for
this work and set aside on overhead grounds) would make the mapping a
tactic-to-ability table, while an SDN or container testbed would make each
mutation an actual reconfiguration whose latency, packet loss and controller
load are measurements rather than modelling choices. This programme composes
with the tactic-level action layer named beside it: a successor building a
richer action vocabulary could build it directly at the emulated rung rather
than inside the simulator.

What does not carry is as important to state, and it is a design fact rather
than a loss. The declared magnitudes — the per-tactic dwell times anchored
to this simulator's own action costs, and the failure weights argued against
its vocabulary — are parameters of the model in this environment, not
invariants of the attacker, and the methodology says so where they are
introduced. A successor re-derives them against the new environment by the
same discipline: declare, justify against what evidence exists, and sweep.
The negative scope is equally explicit: emulation narrows the abstraction
gap, it does not close it. No rung of this ladder yields a claim about a
real adversary; what the next rung yields is the same envelope of modelled
behaviour evaluated against real mechanisms at real cost, which is the form
of the overhead question a reviewer actually asks.

## Evidence and repo anchors

- The defender-cost frontier this note treats as the carried result:
  [`../../implementation/pipeline/ogasp/mtd_disruption_frontier.md`](../../implementation/pipeline/ogasp/mtd_disruption_frontier.md);
  the derived measure itself (`DisruptionLedger`, occupancy) in
  [`../../../src/mtdsim/l3_simulation/movement/measures.py`](../../../src/mtdsim/l3_simulation/movement/measures.py)
  and its per-run snapshot in
  [`../../../src/mtdsim/l3_simulation/movement/statistics.py`](../../../src/mtdsim/l3_simulation/movement/statistics.py).
- The inherited per-mechanism execution durations occupancy rests on:
  [`../../implementation/provenance.md`](../../implementation/provenance.md)
  (MTD-14, Zhang 2023 Table 3).
- The controller layer as the declared join (mapping, dwell catalogue,
  failure matrix): [`../../implementation/pipeline/ogasp/controller.md`](../../implementation/pipeline/ogasp/controller.md);
  the dissertation's own portability and Caldera sentences in §4.2.4
  ([`../../thesis/dissertation.tex`](../../thesis/dissertation.tex),
  `subsec:execution`; Caldera: `applebaum2016` in `references.bib`).
- The sibling programmes this one sits beside and composes with:
  [`successor_programme.md`](successor_programme.md).
- The rung analysis and its commissioning context (the tiered overhead
  options, the rejected declared-price middle tier):
  [`../../implementation/pipeline/ogasp/evaluation_predesign.md`](../../implementation/pipeline/ogasp/evaluation_predesign.md)
  §1b.

## Revisit conditions

- If an emulation study is actually run, this note graduates from future
  work: the frontier's shape becomes a tested prediction, and the note is
  superseded by whatever the comparison finds.
- If the tactic-level action layer is built inside the simulator first, the
  mapping half of the portability argument is exercised early and this
  note's claim narrows to the environment half (real reconfiguration costs).
- If the inherited execution durations are shown unfaithful to the lineage
  they are badged against, the frontier's occupancy currency weakens and
  the carried-result framing must be restated.
