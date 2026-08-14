---
status: durable
chapter: ch4_methods
created: 2026-07-28
updated: 2026-07-28
---

# An exponential dwell is a tractability choice, not a fidelity claim

## Position in the dissertation

The methodology chapter's validity defence for the *shape* of the timing
distribution, sitting beside the defence of its *values* in
[`operational_validation.md`](operational_validation.md). It is the answer to the
examiner's question "real attacker dwell is not memoryless, so why is your model
exponential?", and it states the one condition under which that answer holds.

## The idea

Assigning each attacker tactic a duration drawn from a distribution, rather than a
fixed dwell, forces a declaration that a fixed dwell never had to make: not only
how long a tactic takes on average, but the shape of the variation around it. The
values themselves are defended elsewhere, through output-oriented validation and a
declared sweep. The shape is a separate choice and it arrives undefended. This note
argues that the exponential is defensible here, that its defence is tractability
and precedent rather than realism, and that the defence rests on a specific
property of the metric which must be checked rather than assumed.

### What the exponential assumes, and where it is plainly wrong

An exponential dwell carries three properties. It is memoryless, so the expected
remaining time in a tactic is unchanged by how long the attacker has already spent
there; its single most probable value is zero; and its variability is fixed, with a
standard deviation equal to its mean.

For the fast, opportunistic tactics this is tolerable, and a retry-until-success
reading even makes memorylessness natural. For the slow, deliberate tactics it is
wrong in a way worth stating plainly. Persistence, concealment and
command-and-control are characterised in the incident literature by *paced*
behaviour, which means probability mass gathered around a typical duration. An
exponential says the opposite: the most likely thing a concealment dwell does is
end almost immediately. A distribution with the same mean but a heavier shoulder —
a gamma, or the Erlang that arises from summing several exponentials — would
represent that pacing far better. The mismatch is not marginal, and it is
acknowledged rather than argued away.

### What the field actually does about firing rates

A survey of timed adversary models settles what the alternative to this position
would be, and the answer is that no better-defended position exists in the
literature. Three findings carry it.

First, rates are declared rather than measured, and the strongest work says so
outright. Bland et al. (2020), the closest executed stochastic-Petri-net attacker
model, state that their rates "were notional and randomly selected between one and
ten" and that identifying realistic ones is future work — in a peer-reviewed
venue, and with the net's *structure* validated by a panel of practitioners while
its rates were uniform random draws. Mendonça et al. (2023) mark un-sourceable
parameters with a question mark inside the parameter table itself, recording that
they "were reasonably estimated, as they were not found in the literature or
product specifications". McQueen et al. (2006), at the root of the
time-to-compromise lineage, set one process mean "somewhat arbitrarily" at eight
hours and concede that some of the model's assumptions were never validated.

Second, and more pointedly for this note, what these papers justify is the
*formalism*, never the distribution. Mendonça et al. defend their choice of net on
the grounds that it "allows the analysis of systems through numerical solution and
simulation methods", which is an argument about solvability. No surveyed work
defends memorylessness as faithful to attacker behaviour. The simulator this thesis
extends already made the same move without comment: Zhang (2023) replaced the
inherited uniform mutation interval with an exponential one and recorded no
justification for the distribution at all. Adopting an exponential here is
therefore not a new liberty taken; it is the inherited convention, now at least
declared as a choice.

Third, the gap this thesis fills is real but narrow, and should be worded at that
granularity. No surveyed source grounds a *per-tactic* attacker firing rate in
measured data. Where attacker-side timing is empirically grounded, it is at the
granularity of exploit development, vulnerability discovery, or whole-campaign
compromise — never the tactic. Even the flagship attack-simulation language for
this domain ships without timing: Xiong et al. (2021) note that their attack steps
are of equal width "owing to the lack of probability distributions that can be
assigned to attack steps", and name assigning them as future work.

### The licence, and the condition it depends on

The defence that makes an admittedly wrong shape acceptable comes from the
lineage's own landmark, and it is a claim about which quantity the metric
consumes. Madan et al. (2004) modelled intrusion and response as a semi-Markov
process, choosing that formalism precisely because "some of the sojourn time
distribution functions may be non-exponential" — and then showed that the analysis
"depends only on the mean sojourn time and is independent of the actual sojourn
time distributions". McQueen et al. arrive at the same place by a different route:
having hypothesised beta, gamma and exponential shapes for their three processes,
they report that "for now, the analysis only uses the expected value of the
time-to-compromise", and the shapes are never exercised.

The mechanism behind Madan's result is worth stating, because it is also what
bounds it. The mean time for a process to reach an absorbing state decomposes into
the expected number of visits to each state multiplied by the mean dwell in that
state. The visit counts are a property of the routing probabilities alone. So when
routing is independent of how long each state takes, the aggregate depends on the
declared means and not on the distributions around them, and an exponential costs
nothing.

That independence is the condition, and in a moving-target setting it does not
hold exactly. A defensive mutation fires on its own schedule and races the
attacker's dwell, so a long dwell is more likely to be interrupted than a short
one, and an interruption changes where the attacker goes next. Distribution shape
therefore re-enters through the interrupt channel, even though it leaves through
the arithmetic. This matters most in exactly the regime the thesis is about, since
the central contest is the ratio between mutation interval and tactic dwell. The
honest position is that the mean is expected to be the load-bearing quantity, that
the residual shape-sensitivity runs through interruption, and that this is a
prediction to be tested by sweeping a same-mean heavier-tailed family rather than a
property to be assumed. Naming the leak is what keeps the defence from being
circular: the distribution was fixed on precedent grounds before any result was
examined, and the check that could falsify the reasoning is specified in advance.

### The counter-evidence, and the asymmetry that softens it

One large empirical study contradicts the exponential directly and should be cited
rather than omitted. Holm (2014), across 203,025 intrusions on 261,757 systems,
finds that a Pareto distribution best fits time-to-first-compromise and that the
exponential is a poor choice for time-between-compromises and overall
time-to-compromise, failing to reproduce the heavy tail beyond roughly eighty days.
Two qualifications travel with it: the population is opportunistic malware activity
rather than targeted campaigns, and it measures campaign-level compromise timing
rather than the per-tactic dwell modelled here. The finding still stands as the
best available evidence on the shape question, and its direction is clear. Real
compromise timing is heavier-tailed than exponential.

There is a compensating asymmetry. Where the modelling literature does reject the
exponential, it rejects it for the *defender's* move rather than the attacker's
dwell, because a scheduled defence is genuinely periodic rather than random.
Mendonça et al. model a time-based mutation as a deterministic transition for this
reason, and the FlipIt analysis shows a periodic strategy with a random phase
strongly dominating all renewal strategies of the same rate. The defensive
mechanisms evaluated here keep their own inherited timing and are not
re-parameterised by this work, so the literature's sharpest objection to
exponential firing lands on machinery this thesis does not touch.

### What this argument does not claim

It does not claim that attacker dwell is exponentially distributed; the evidence
points the other way, and the low-and-slow tactics are the clearest mismatch. It
does not claim that the declared means are correct, which is the separate question
the validity defence handles. It claims something narrower and defensible: that
under a declared, mean-anchored, swept regime the exponential is the tractable
member of a family the aggregate metric is largely insensitive to, that the one
route by which shape can still matter has been named, and that a conclusion which
survives the sweep is a result while a conclusion which does not is a finding to
report. The formalism is a tractable veneer over quantities that are inherently
arbitrary, because a true per-tactic duration is not a measurable property of the
world. Saying so is stronger than pretending otherwise.

## Evidence and repo anchors

- Extractions behind each named source: [`bland2020`](../../sources/extractions/bland2020.md) (§2.1, notional rates); [`mendonca2023`](../../sources/extractions/mendonca2023.md) (§2.3 solvability rationale; §4.1 the `?`-badged parameter table); [`mcqueen2006`](../../sources/extractions/mcqueen2006.md) (§1 unvalidated assumptions; §3.4 expected values only); [`timed_attack_models`](../../sources/extractions/timed_attack_models.md) (Madan 2004: §1 semi-Markov rationale, §"mean sojourn time" — the extraction records the mean-sufficiency result for the steady-state analysis); [`initial_access_timing`](../../sources/extractions/initial_access_timing.md) (Holm 2014, §5.2.1–§5.2.2); [`persistence_reset_models`](../../sources/extractions/persistence_reset_models.md) (FlipIt, §4.3 renewal-game Theorem 4); [`xiong2021`](../../sources/extractions/xiong2021.md) (§6.1, §8); [`zhang2023`](../../sources/extractions/zhang2023.md) (§4.3.4, §4.5).
- The design record carrying the technical form of this argument, the formalism ruling, and the per-tactic parameterisation: [`../../implementation/pipeline/ogasp/stochastic_timing_design.md`](../../implementation/pipeline/ogasp/stochastic_timing_design.md) §1, §3.
- The catalogue of declared durations this regime turns into distribution means: [`../../../data/ogasp/tactic_durations.json`](../../../data/ogasp/tactic_durations.json).
- Sibling notes: [`operational_validation.md`](operational_validation.md) (the defence of the *values*, and the shape-not-scale discipline this note inherits); [`../ch2_background/tactic_duration_precedent_survey.md`](../ch2_background/tactic_duration_precedent_survey.md) (the declare-and-sweep precedent and the gap statement); [`../ch4_methods/evaluation_burden.md`](../ch4_methods/evaluation_burden.md) (the commitment to report a negative sensitivity result).
- The sweep that tests this note's central prediction: [`../../handoffs/2026-07-28_tactic_rate_feasibility_study.md`](../../handoffs/2026-07-28_tactic_rate_feasibility_study.md).

## Revisit conditions

- If the sensitivity sweep shows a conclusion changes under a same-mean
  heavier-tailed family, the mean-sufficiency defence fails for this model and the
  note is rewritten around the shape-dependence rather than around the licence.
- If the interrupt channel proves to be the dominant route by which shape matters,
  the argument narrows further and the distribution family becomes a first-class
  parameter rather than a tractability convenience.
- If a study grounding per-tactic attacker dwell in measured data appears, the
  narrow gap statement weakens and this note reframes as a comparison against that
  precedent.
- If the defensive mechanisms are ever re-parameterised by this work, the asymmetry
  argument no longer holds and the periodic-versus-exponential objection becomes
  live for machinery the thesis does own.
