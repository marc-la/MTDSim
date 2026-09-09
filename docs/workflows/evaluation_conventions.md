---
status: durable
created: 2026-09-09
updated: 2026-09-09
---

# Evaluation conventions — how the field builds and reports an MTD experiment

**Status:** durable. The experiments-chapter counterpart to
[`literature_conventions.md`](literature_conventions.md) (prose and methods
norms) and [`figure_table_conventions.md`](figure_table_conventions.md) (the
visual contract). This file carries the **structural** conventions: where setup
lives, what a results section is organised by, what a sensitivity analysis
looks like in this literature, how many runs get reported, and the grammar of a
comparison sentence. Load it before designing or drafting the experiments
chapter, and before deciding where an experimental fact belongs.

**Evidence base.** A section-level anatomy of the evaluation portion of each
paper, built one paper per pass with page or line locators on every claim
(2026-09-09 survey). Twenty-five papers: this project's own lineage (Brown,
Zhang, Ho, Tay); the MTD evaluations the review cites (Hong, Masud, He, Kim,
Alavizadeh, Cho–Ben-Asher, Zaffarano); the formal-model cousins (Bland, Outkin,
Anderson, Torquato, Maleki, Venkatesan, and a partial pass over the
timed-attack-model family); the network-layer MTD papers (Carroll, Crouse,
Jafarian, Wang, Reti); the metric-definition genre (Manadhata and Wing); and the
two critiques that say what an evaluation *should* do (Cho's survey, Jalowski's
gap analysis). The per-paper files are
[`../implementation/evaluation_anatomies/`](../implementation/evaluation_anatomies/),
whose README records what the survey did not reach. Method prescriptions the MTD
corpus does not carry — how many replications, what validation licenses — come
from the simulation-methodology sources under `docs/sources/methodology/`. Every
rule below is an observed convention, not an invention of this repo.

**Division of labour.** This file states the conventions. What they apply to
lives elsewhere: metric semantics and the comparability boundary in
[`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md);
the hypothesis structure and the statistical instrument in
[`../implementation/pipeline/ogasp/hypothesis_tree.md`](../implementation/pipeline/ogasp/hypothesis_tree.md)
and [`../implementation/pipeline/ogasp/evaluation_predesign.md`](../implementation/pipeline/ogasp/evaluation_predesign.md);
the badge ceiling in [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md).

---

## a) Setup and results are usually one movement, not two chapters

The corpus census, on where the experimental declaration physically sits:

| Form | Papers |
|---|---|
| Setup as an untitled head of the results section | Brown (run configuration opens §IV); Zhang (the factors, the two parameter tables and the 100-run statement open ch. 5) |
| Setup and results as sibling subsections of one section | Hong (6.1 setup / 6.2 results); Kim (6.1 setup / 6.2–6.3 results) |
| Setup in the model section; results stand alone | Anderson (parameters in §III MODEL); Bland (§4 nets, §5 learner, §6 results); Carroll |
| A titled setup section of its own | Reti (§5 EXPERIMENTAL SETUP); He (§V EXPERIMENT SETUP, holding only dataset and metrics) |
| Setup interleaved, one parameterisation before each result | Outkin (§5.1.1 → §5.1.2; §5.2.1 → §5.2.2) |

**A separate experimental-setup chapter is not the field's form.** The
dominant pattern is one movement: declare, then report. Where a paper does
title a setup section, it is small and holds only what the model section did
not already carry. This ratifies the merged Experiments chapter rather than
merely permitting it.

**Consequence for placement:** a parameter is declared where it is first used,
not collected into a front-loaded chapter. A parameter used by every experiment
is declared once, in a table, before the first result.

## b) Results are organised by one axis, named in a roadmap sentence

Three organising axes are attested, and papers pick exactly one:

- **By metric family** — Brown (blocked actions, then attempts); Kim
  (§6.2 performance, §6.3 security); He (attack effectiveness, defence
  performance, diversity, adaptive adversary, efficiency).
- **By swept variable** — Hong (hosts, then variants, then network states);
  Zhang (effectiveness, then interval, then network size).
- **By mechanism** — Masud (IP shuffle, shuffle, diversity, redundancy, scale).

**The metric-family axis is the one to imitate when the contribution is the
attacker rather than a mechanism**, because it lets the same runs answer more
than one question (§f). Kim's performance/security split is the field's plain
form of the effectiveness/efficiency purpose axis that Cho's survey defines.

The results section opens with a **roadmap paragraph naming each subsection's
question and the reason for the order** (He L249–257; Hong's §6 preamble; Kim's
§6 opener). This is cheap and universal; write it.

## c) Sensitivity analysis is rarely a section — it is usually the results

**Almost nobody in this corpus has a section called "Sensitivity analysis."**
Outkin's §5.1.2 is the only titled one in the surveyed set. Everywhere else the
parameter sweep *is* the results section (Hong's entire §6.2; Anderson's entire
§IV; Carroll's entire §IV), or it is an unlabelled axis inside results (He,
Kim, Masud, Zhang).

Two designs are attested, and both are acceptable:

1. **One-at-a-time (OAT)** — universal. Hong (three one-factor sweeps);
   Anderson (four sweeps, each x = the defender's knob against a second
   parameter at three levels, then the whole set repeated in the second model);
   Carroll (four); He (two); Kim (one); Masud (two); Bland (one, four levels);
   Outkin (by attack stage). Madan's is the canonical justification: parameters
   were guessed, so the sweep is offered as the substitute for estimation.
2. **Full factorial** — Reti (the whole Table 1 grid, 100 runs per cell); Zhang
   (4 × 4 interval × network size); Outkin's §5.2 (3 × 2, but with empirically
   given levels).

**Range justification is almost never given.** Hong, Anderson, Carroll, Zhang
and Reti state no rationale for any range. Bland states the opposite outright —
the rates are "notional and currently have no relation to a real computing
system". A dissertation that derives its bands from the model's own structure
therefore exceeds the corpus, and should say so once rather than assume the
reader knows it is unusual.

**What the good papers do instead of justifying ranges is name what they did
not sweep.** This is the discipline worth importing, and it is well attested:
Hong defers the metric weights with a reason and asserts the direction of their
effect; Bland writes "Identifying realistic rates is a future effort"; Kim
fixes the MTD interval at 300 s and defends the value by citation, repeating it
in every caption; He states that a parameter was "empirically set"; Reti flags
its step limit as a threat in the conclusion; Zhang says a sensitivity analysis
"can" determine two of its constants and never runs one. Outkin names the time
step's known monotone effect and fixes it anyway.

**The rule that follows:** every declared parameter is listed; each row says
either the band it was swept over and what moved, or that it was held and why.
One register, both kinds of row. A parameter that appears in neither list is
the failure the corpus keeps committing.

**Presentation.** The standard figure is a line chart: x = the swept parameter,
y = the metric, series = a second factor at two to four levels, one figure per
swept parameter (Anderson is the purest form; Hong, Carroll, Kim, Masud all
follow it). Zhang's alternative is a small-multiple grid over the two crossed
factors with two zoom panels. A sensitivity **table** is rare; where the
outcome is "nothing moved", a table of band-ends against centre is the honest
compression and saves the figures for what did move.

## d) Replication is under-reported, and reporting it is an upgrade

| Paper | What it declares |
|---|---|
| Brown | nothing — no run count, no seeds, no horizon; the word "trials" appears once |
| Zhang | 100 runs |
| Reti | "Each combination of parameters was run 100 times" |
| Bland | 500 000 episodes per case, figures truncated to 100 000 |
| Hong, Anderson, Carroll, Madan | analytical; no replication, by construction |
| He | no runs at all — a fixed captured dataset, so replication is not the unit |

**No paper in the lineage reports a confidence interval.** Means over repeated
runs is the local ceiling. Reporting effect sizes with intervals therefore
*exceeds* lineage practice and should be stated as a deliberate improvement,
not slipped in. The seed scheme, the run count per cell and the horizon are
declared once, in the dimensions table.

Where the simulator is cheap enough that any difference can be made
significant by adding runs, the field offers no protection — so a minimum
effect size of interest is declared with each claim. That discipline comes from
this project's own predesign, not from the corpus, and is worth one sentence of
ownership.

**The model declaration**, and the fullest in the whole source tree, is Barach's
2026 ransomware-MTD paper: "Each experimental configuration was repeated 100
times under randomized user behavior and threat injections. For each metric
(Accuracy, MTTC, Encryption Success Rate), we report the mean and standard
deviation. In addition, 95% confidence intervals were calculated to assess the
statistical reliability of the results. Where applicable, paired t-tests were
conducted between the proposed framework and baseline models." Four sentences
carrying repetitions, dispersion, intervals and the test. Copy the *form*; the
choice of test is a per-study matter, and a paired test is wrong wherever the
arms do not actually share randomness.

**A vocabulary warning.** A census of every term of art in formal
sensitivity analysis — Sobol, Saltelli, Morris, one-at-a-time, OAT, factorial
screening — across the whole source tree returns **zero hits** outside this
repo's own records. The MTD literature practises one-at-a-time analysis
universally and names it never. So naming the design puts a dissertation ahead
of its field, and importing the wider apparatus of global sensitivity analysis
would read as foreign. Name the design in the field's plain words, cite the
method once if a method paper is cited at all, and do not build the chapter's
vocabulary out of a literature this one does not read.

**One inherited debt worth knowing about.** The substrate's own paper states
that it "set[s] the time duration of each MTD technique within a reasonable
range based on existing empirical data and conducts sensitivity analysis to
determine the appropriate value", and states of a second constant that it "can
be determined via empirical study and sensitivity analysis". Neither analysis
appears in that document. Constants inherited from it therefore carry a stated
justification that cannot be read, which is a fact about provenance rather than
a fault to fix.

## d2) How many runs, and what "validation" licenses

The MTD corpus answers neither question, so both come from the
simulation-methodology literature now held under `docs/sources/methodology/`.

**Choosing the number of replications.** Hoad, Robinson and Davies set out the
three methods in use: a *rule of thumb* (Law and McComas: at least three to five
replications — "useful for telling users that relying upon the results of only
one run is unwise", but it "makes no allowance for the characteristics of a
model's output"); a *graphical method* (plot the cumulative mean of the chosen
output against the replication count and read off where the line flattens —
simple, and "subjective with no measured precision level"); and the *confidence
interval with specified precision* method, which "asks the user to make a
judgment as to how large an error they can tolerate in their model's estimate of
the true mean", then runs replications until the interval around the cumulative
mean is inside that precision. The third is the one they automate, and it is the
one to cite: it makes the run count a consequence of a declared tolerance rather
than a round number.

**What validation means.** Sargent's taxonomy is the standard reference and has
four parts: *conceptual model validation* — the theories and assumptions
underlying the model are correct and its representation is "reasonable for the
intended purpose"; *computerised model verification* — the programming and
implementation of the conceptual model are correct; *operational validation* —
"the model's output behavior has sufficient accuracy for the model's intended
purpose over the domain of the model's intended applicability"; and *data
validity*.

Two consequences matter for a model of an unobservable system:

- **Parameter-variability sensitivity analysis is named as an operational
  validation technique**, not merely as a robustness check. A sensitivity
  section is therefore doing validation work and can say so, with a citation.
- **The ceiling is explicit and citable.** "If a system is not observable, which
  is often the case, it is usually not possible to obtain a high degree of
  confidence in the model. In this situation the model output behavior(s) should
  be explored as thoroughly as possible and comparisons made to other valid
  models whenever possible." A modest claim about an unobservable adversary is
  the discipline's own prescription, not a hedge.

## e) The grammar of a results sentence

Four moves, in this order, attested across the corpus:

1. **The observation**, as ordering or trend far more often than magnitude.
   Hong: "the shuffle-based approach is slightly better than the
   diversity-based approach"; Brown: "the host shuffle performed the best,
   followed by port shuffling". Where magnitude is given it is a relative
   percentage (Kim: "reduced by about 46%"; "about 65 % smaller") or an
   approximate fraction (Outkin: "about 2% of the time ... as compared to about
   5%").
2. **The mechanism**, in the next sentence, as the reason. Hong: "This is
   because a large proportion of the attack paths is changed." Brown: "This is
   because all these techniques work at a host level." He labels these
   explicitly — "We hypothesize that ..." — which is the more honest form when
   the mechanism was not measured.
3. **The exception or the surprise**, marked as such. He separates
   "Surprisingly, WBLM attacks demonstrate better RI ... despite their poorer
   ADR" from its expected findings and attaches a hypothesis to each.
4. **The conditional recommendation**, closing the subsection. Hong: "the
   diversity-based MTD technique would be most suitable when the network has
   the same number of software variants and network states, but the number of
   hosts increases." Brown: "Hence, to mitigate attacks such as scenario 1,
   host-based and/or port-based shuffling is effective compared to other
   types."

Two refinements worth adopting:

- **Declare the success criterion at the metric, before the result.** He
  defines what counts as a successful attack and a successful defence, each
  with a justification paragraph, then draws the thresholds on the figures.
  This is where a grading vocabulary belongs when there is no separate
  burden-of-proof section — at the definition site, one sentence, not a unit of
  its own.
- **Defer materiality to the reader when the evidence cannot settle it.**
  Outkin: "Whether the difference between 5% versus 2% in 'Ready' state is
  material would be determined by the defender preferences, cost difference
  ... and the nature of the system the defender is protecting." This is the
  clean way to report a real but small separation without inflating it.

## f) One run set, two questions — the funnel

The structural problem of a thesis whose contribution is an *attacker* is that
the same experiments must characterise the attacker and evaluate the defence.
The corpus solves it with a **funnel**, and He is the clearest instance:

> §VI.A characterises the attacks on the **undefended** target — which
> knowledge level is actually more dangerous, which generator is viable, how an
> attack parameter trades evasiveness against intensity — and *prunes* the
> attack set to the one configuration that matters. §VI.B then evaluates the
> defence against that configuration only, with the pruning rule stated.

Two properties make this work and both are worth copying. The attacker
characterisation runs **against no defence**, so it is a statement about the
attacker rather than about the interaction. And its output is a **selection
step** that the defence evaluation then depends on, so the characterisation
earns its place in the chapter instead of reading as a detour.

Bland does the smaller version: an attacker-capability claim read off the
reward curve ("The positive trend implies that the machine learning algorithm
is finding or improving the attacker's strategy"). Outkin reads attacker
residence times off the same chain that scores the defender.

**The convention:** attacker-property claims are legitimate results, they are
taken from the no-defence arm, and they are reported in the results chapter as
observations. The *verdict* they add up to belongs in the discussion.

## f2) "Baseline" names two different things — keep them apart

The corpus uses the word for two objects, and an evaluation needs both.

- **The no-defence condition**, which is the reference every effectiveness
  number is a difference from. Zaffarano's framework makes this definitional and
  says it three times: "Metrics are derived from the statistical differences
  between these interactions during runs when an MTD is not deployed (the
  baseline) and when it is deployed"; "Runs with no MTD deployed represent a
  baseline run, which can be contrasted to effects measured during identically
  configured runs with a deployed MTD technology. This contrast drives our
  metrics." Brown plots it as a "None" bar in every panel and calls it "the No
  MTD control group"; Tay makes it the *unit* of the y-axis by normalising every
  metric against it.
- **The comparison arm** — the prior model, agent, or scheme the contribution is
  set against.

A chapter that says "the baseline" without saying which will be read as
confusing a control with a competitor. Name them separately at first use and
never let one word carry both.

Two further moves from the same framework, both cheap and both worth taking:

- **Measure the defence's cost on the same instrument as its benefit.** Every
  metric is instantiated twice, once over a mission activity model and once over
  an attacker activity model, with identical formulae; the two are distinguished
  only by the sign of the weight at aggregation. The design point is that an MTD
  "ha[s] as much potential to interfere with a network's ability to support the
  mission as [it does] to defend the network", so an evaluation that measures
  only the attacker side cannot inform a deployment decision.
- **A phase-resolved effectiveness locator is an established measure, not a
  bespoke one.** The same paper defines the kill-chain phase against which an
  MTD is most effective as the argmax over phases of the mean per-task change in
  success, with and without the MTD. Any tactic-resolved MTD-effect measure has
  this as its published antecedent and should cite it rather than introduce
  itself as novel.

## g) Threat model, limitations, and what the critiques demand

- **The threat model is its own titled subsection** and is written in the same
  template as the defence model. He's *Goal / Knowledge / Capability* triple,
  applied to attacker and defender symmetrically, is the tightest form in the
  corpus; Hong (§6.1.2), Brown (§III.C) and Masud (§3.1) all carry the section.
- **Limitations are owned in the authors' own voice, before a reviewer finds
  them.** Brown's §V names its attacker's unrealism directly. Zhang puts the
  concessions in a chapter titled future work. He pairs each limitation with
  the future work that would lift it — the form to prefer.
- **Position the evaluation on the method ladder and own the rung's cost.**
  Cho's four classes are analytical, simulation, emulation, real testbed, and
  simulation's stated cost is that "all possible variables may not be captured
  ... the lessons obtained from the simulation studies may not be realized in
  real testbed-based experiments". Its stated affordance is exactly the
  sensitivity analysis: "easy parameterization for sensitivity analysis".
- **The critiques' standing demands**, which an APT-attacker evaluation is
  read against. Cho §V-D: attackers in MTD studies are pattern-following rather
  than learning, single-strategy, and confined to reconnaissance, while
  defenders are granted adaptivity. Jalowski, harder: "The most glaring flaw in
  the MTD literature is the ill-defined attacker models, which are often too
  simplistic or based on completely unrealistic assumptions", and "testing
  against active scanning (Nmap) is too naive. Advanced Persistent Threats
  utilize Passive Reconnaissance to remain in the shadows and learn mutation
  patterns over time. To move forward, research must shift toward defending
  against smart, adaptive attackers who understand the MTD scheme." A study
  that answers these must show it, not assert it — and must say which half it
  answers.

**The field's only enumerated prescription for an evaluation metric** is
Jalowski's four guidelines, verbatim: a metric should be "possibly easy to
establish, using data that can be obtained both during simulations and from the
normal runtime of the network"; "generic enough so that possibly many, or all,
schemes can be evaluated using it"; "as a baseline, it should compare the MTD
scheme to a state-of-the-art system, protected using the best available
methods"; and it should use "common security mechanisms and terminology ...
making it understandable even to people who are not experts in the MTD field."
Any bespoke measure a dissertation introduces will be read against this list,
and the third guideline in particular is one most MTD evaluations — including
those that compare mechanisms only against each other and against no defence —
do not meet. Owning that is cheaper than being caught by it.

## h) The local genre — what a thesis in this lineage actually does

Two UWA theses in this project's own supervision lineage, read for structure.
They matter more than any single journal paper, because they are the form the
examiner has seen before.

**Tay** splits the experimental portion into **three chapters by function**:
§5 *Evaluation* carries the design-of-experiment and the numbers; §6
*Discussion* carries the interpretation, **mirroring §5 subsection for
subsection in the same order**; §7 *Future Works* carries the limitations,
framed forward. Every result gets a mechanism paragraph by construction, and no
interpretation leaks into the results narration. **This is the ruled shape of
this dissertation's ch5/ch6/ch7**, so the local precedent is exact.

**Ho** takes the other option: one *Results and Discussion* chapter whose
per-factor blocks each close with a titled discussion subsection, with the
limitations in a combined future-work-and-conclusion chapter. Its setup is
split into an *Experiment Setup* section (fixed-parameter tables, features,
conditions) and a separate *Evaluation Method* section (collection pipeline,
metric calculation).

Three conventions from Tay worth importing wholesale:

- **A roadmap paragraph opens every numbered chapter**, naming each subsection
  in order. It appears at three chapter heads in that document — a house
  pattern, cheap, and it is what a reader uses to navigate.
- **Every swept range is justified against the literature's default, and the
  deviation argued.** The model case declares the common range, states that the
  experiment will instead use a wider one, and says what the extra region is
  for. This is the single most reusable move in the document, and it is exactly
  what the journal corpus almost never does (§c).
- **A repeating internal shape per experiment subsection:** define the
  parameter and what it trades off; declare the range *and its justification*;
  the figure; the numeric readout, with the "why" deferred to the discussion
  chapter.

And one measurement of the local floor, recorded as a floor rather than a
target: that thesis declares no network configuration, no attacker model, no
run count, no seeds, no dispersion, and contains no tables at all. Reporting a
factor table, a seed scheme and intervals clears the local bar comfortably; the
bar to actually aim at is the journal corpus's.

## i) The corpus's own failures, named so they are not repeated

- **No run count at all** (Brown) — the most-cited paper in the lineage does
  not say how many times anything was run.
- **A sensitivity analysis promised and not delivered** (Zhang, twice; Outkin's
  conclusion claims a parameter-ranking capability it never reports).
- **A swept parameter whose results are not shown** (Bland's exploration rate:
  four levels declared, one number reported).
- **Held-fixed defaults never stated**, so a sweep cannot be reproduced
  (Anderson: the three parameters held fixed in each figure appear nowhere).
- **A stale roadmap** that names section numbers the paper does not have
  (Reti).
- **Ranges with no rationale**, near-universally.
