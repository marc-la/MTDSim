---
status: durable
created: 2026-09-09
updated: 2026-09-25   # §j prose around a results float, §k defending the setup (genre + reporting-standard searches); §e scope note for a mirrored discussion
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

**"Held and why" has a preferred answer: a study that ran the value, cited
against it** (supervisor ruling E5, 2026-09-22: "every hard-coded number,
somebody will ask why that number"). Kim's cited 300 s interval is the corpus
form. In this thesis the lineage's configurations are one generated table in
chapter 2 (`tab:lineage-configurations`, from
`data/misc/lineage_configurations.yaml`), Table 5.1 carries a citation after
every value a prior study ran, and its caption covers the rest: an uncited
value is the simulator's default or is argued in §5.1's prose. A value with
none of the three — citation, default, stated reason — is the gap an examiner
finds first. The citation goes after the **value** it sources, not on the
parameter's label, because one row can mix sourced and unsourced levels
(200 s is cited; 2 000 s is argued).

**A sensitivity analysis can do more than defend a result, and the strongest
instances do.** Manadhata and Wing frame theirs as producing *guidelines for
choosing parameters* — "we provide guidelines to our users for numeric value
assignment using parameter sensitivity analysis ... Numeric values should be
chosen such that both the privilege values and the access rights values affect
the ... measurements comparison's outcome" — and then actually assign their
later parameters "based on our parameter sensitivity analysis' recommendation".
Torquato does the operational version: a first study finds the
availability-aware migration trigger, and a later study truncates its axis at
that value with the reason stated — "we adopt this approach because longer VM
migration trigger intervals provide worse results for both availability and
security", so the dropped region is dominated rather than unexamined.

The convention worth taking: **a sweep that selects the operating region for
the experiments that follow is stronger than one that only shows a verdict did
not move**, and it costs nothing extra once the sweep has been run. It also
converts a null result — most parameters inert, one influential — from a
non-finding into a design input.

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

**Scope of the four moves (2026-09-25).** The papers these moves come from
mostly have no separate discussion, so the reason has to sit in the results.
In a thesis whose discussion chapter mirrors the results (§h, Tay, the ruled
ch5/ch6 split), moves 2 and 4 **move to the discussion**. The results keep:
- move 1;
- a reason only where it is true by construction;
- move 3, stated and not explained;
- a hand-off.

The genre literature supports the same line (§j3), and it is the rule in
the retired results-context brief (§3).

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

## j) The prose around a results float

Added 2026-09-25 from a genre-literature search (Marc: "seek guidance on how
you structure evaluation prose"). The sources are writing-centre guidance and
move analyses of results sections, read open-access on the date above, plus
re-reads of the anatomies in `../implementation/evaluation_anatomies/`. §b
and §e above still stand. This section covers the *text* that sits between
floats, which neither of them does.

**j1. The unit is data commentary: locate, highlight, then qualify.** Swales
and Feak's three elements, in order, are the location element and summary,
then the highlighting statement, then the implications, problems or
exceptions: "do NOT simply repeat all the details in words, attempt to cover
all the information, or claim more than is reasonable" (via HSLU's
academic-writing text, ch. 4.5). Move analyses of results sections agree on
what is obligatory:
- Yang and Allison's dominant moves are preparatory information, reporting
  results and summarising results.
- Kanoksilapatham finds reporting results to be the only obligatory move.
- Moskovitz (2023) finds that a results section always *announces*, usually
  *orients* and *observes*, and only sometimes *explains*.

So around each float the text owes one move that points the reader at it and
one that selects the finding. It does not owe more than that.

**j2. Point to the float before the observation, and let the finding hold
the sentence.** Moskovitz: observing first and pointing afterwards "encourages
them to try to understand details as they read without the aid of the
visual"; "only novices believe that 'see Figure 1' is sufficient". UNC's
four acceptable forms are:
- "As shown in Table 1, …"
- "Results are shown in Table 1."
- "Table 1 shows that …"
- "… (Table 1)."

No source forbids "Figure X shows", but the working rule is this: **the
finding is the subject of the sentence, or it sits in the *that*-clause, and
it falls at the end of the sentence**. Gopen and Swan call that end position
the stress position; the start of the sentence (the topic position) carries
the link back to what came before. This thesis prefers the parenthesis form
("… (Figure 5.4)"), Kim's "As shown in Fig. 8, …" is the corpus exemplar, and
Hong's panel-by-panel narration ("Fig. 4a shows … Fig. 4b shows …") is the
named anti-pattern.

**j3. Where results end.** Three sources set the line:
- UNC: "Nothing your readers can dispute should appear in the Results
  section". Trends are allowed, because "no one can deny that these trends
  do exist".
- USC: "It is appropriate to highlight this finding in the results section.
  However, speculating as to why this correlation exists … belongs in the
  discussion section."
- UNSW allows an honours thesis "a brief comment on the significance of key
  results".

So a results sentence may compare, and may give a reason that is true by
construction. It may not give an unmeasured mechanism, a verdict or a
recommendation (see §e's scope note). The test for a sentence: *could it be
false while every number in the floats stayed the same?* If it could, the
sentence is interpretation, and it moves to the discussion.

**j4. The paragraph is context, then content, then the answer.** Mensh and
Kording (2017), Rule 7: each results paragraph "starts with a sentence or two
that set up the question that the paragraph answers … and the paragraph ends
with a sentence that answers the question". Rule 4: "each subject should be
covered in only one place"; "parallel messages should be communicated with
parallel form". Their Rule 7 suggestion that subsection *headers* be
declarative claims is **rejected**, because it conflicts with the ruled
noun-phrase heading convention.

**j5. Preambles.** Thomson (2023): the reader "may need to be told what the
big point is. And context. And only a little about how the sections are
organised". About a paragraph is enough. SJSU: open the results "with an
introduction to connect the results with the research question(s)". Hong
(§6.2.1) states at the head of each subsection what is held fixed in it,
which is the local form of §i's held-defaults failure. The corpus fails in
three ways:
- **Previewing the payoff.** Masud §4: "The outcomes demonstrate that…".
- **A stale roadmap.** Reti; Tay §4 promises a §4.3 that never comes.
- **No preamble at all.** Ho §4.

**j6. Closing and connecting.** SJSU and USC both recommend closing on a
"narrative bridge" to the discussion. He §VI.B ends by pointing to the next
section, and §VI.C opens by pointing back to it. Bunton (1999) found that
metatext operating across chapters holds a long text together more than
local signposts do. Two conventions follow:
- Each section's last sentence hands the next section its question.
- A back-reference names the exact subsection, not the chapter.

**j7. Captions: decode, and let the text select.** The house rule stands:
"a caption decodes, it does not narrate" (figure conventions §b2, §m), and
chapter 5's captions say how to read the float, not what it shows (the
2026-09-09 sweep). The literature allows it:
- Rougier's Rule 4 says the caption "explains how to read the figure".
- Nature's legend guidance: a brief title, then each panel and symbol; "All
  error bars and statistics must be defined"; "no details of methods".

The alternative is also attested:
- Mensh and Kording: "the title of the figure should communicate the
  conclusion".
- Caltech lets the opening sentence be "a summary statement that highlights
  the key finding".
- Kim Table 5 is the corpus's only message caption.

A message caption is a ruling Marc would have to make. It should never be
made on a float whose numbers are still preliminary (the 2026-09-09 test:
would the caption survive the result coming out the other way?).

**j8. Pitfalls, each named in the sources above:**
1. The float holds the topic position instead of the finding, or the text narrates the float panel by panel (Hong).
2. The text observes before it points to the float, or points with a bare "see Figure 1" (Moskovitz).
3. Data dumping: every number restated, none selected. UNC: "your readers appreciate discrimination more than your ability to recite facts". Tay's best/worst/percentage template is the corpus instance.
4. A float the text never refers to (UNC: "you'll need to refer to each table or figure directly").
5. A number in the text that disagrees with the float. This repo prevents it by generating numbers from tracked artefacts (`results_section_workflow.md`).
6. An undefined interval, n or abbreviation in a caption; an acronym glossed three ways (Masud); methods detail in a caption (Nature).
7. A claim beyond the evidence (HSLU; USC: "the results of a study do not prove anything").
8. Over-hedging and vague modifiers ("appeared to be greater", "promising trends"; UNC, USC).
9. A mechanism or verdict leaking into the results when a mirrored discussion exists (§e scope note).
10. The same claim made in several subsections (Tay makes one claim three times).
11. A preamble that previews the findings, or a roadmap gone stale.
12. A reference to the wrong float (Ho, p. 32: "Figure 11" for Figure 10).
13. A factor or control declared in the setup whose result appears in no float (Bland, §i). It belongs in this list because the absence shows up in the prose, not in the table.

## k) Defending the setup — what a reporting standard asks of each value

Added 2026-09-25. The MTD corpus barely justifies its values (§c), so the
standard comes from simulation-reporting and security-evaluation
methodology. Copies are under `docs/sources/methodology/`:
- STRESS-DES (Monks et al. 2019, *J. Simulation*; checklist v1.1);
- ODD (Grimm 2020);
- Law 2015 (WSC);
- Currie and Cheng 2016 (WSC);
- Kleijnen 2005 and 2008;
- Arcuri and Briand's technical report;
- Rossow et al. 2012;
- van der Kouwe et al. 2018.

**k1. Every value has a basis, and the basis has a kind.** ODD §3.2: "provide
the basis for all parameter values (e.g., taken from which literature, and
why …)". STRESS-DES 3.3: list every input with its base-case value, "state
the range of values that parameters can take", and, for any theoretical
distribution, "state how these were selected and prioritised above other
candidate distributions". STRESS 3.4 treats a value with no source as an
*assumption*, to be declared as one. The paper's Table 5 gives each row a
*Data source*, and those sources mix a citation, an observation and "expert
opinion". **So a per-row source is the standard's own form.** E5's citation
after the value, with the caption naming the other kinds of source, is the
same thing in less space (§c).

**k2. "Default" alone is not a basis.** It becomes one when it is traced to
where it came from and pinned to a version (Rossow B.4: "presumptions about
the 'standard' OS change with time"; van der Kouwe F2). The strongest form
cites the released code. The one place where "default" is the justification
by itself is the no-defence reference: "the proper baseline is usually the
original system using default settings with no defenses enabled" (van der
Kouwe D1).

**k3. The run type, the stopping condition and the run length.** STRESS 4.1:
"Report if the system modelled is terminating or non-terminating … For
terminating systems state the stopping condition". Kurkowski et al. found
that 58 % of network discrete-event-simulation studies did not say which
(STRESS p. 57). Law 2015 §3: a terminating run's ending event "is specified
before any runs are made", and no warm-up period is needed (Currie and Cheng
§4). Rossow C.4: "describe why the analysis duration they chose suffices".
The cheap evidence for that last point is the share of runs that reach the
time limit.

**k4. The run count and the seeds.**
- **Run count.** Arcuri and Briand (TR 2011-13, §11, pp. 21–22): "run each
  randomized algorithm at least n = 1,000 times", *on each artefact*, and
  where artefacts are plentiful, "less runs per artifact (though at least
  n = 10)". Report the count *and* its justification (STRESS 4.3).
- **Seeds.** Common random numbers must be declared along with how the
  streams are split (STRESS 5.2). They license paired differences, but they
  violate the independence that a classic test assumes (Kleijnen 2008,
  p. 479). Currie and Cheng §5.3: the same stream for every configuration is
  not enough; the same draws must drive the same variables.

**k5. Swept levels.** Spacing levels geometrically across orders of
magnitude is the design-of-experiments convention for a factor whose effect
is relative (Kleijnen 2005, p. 3, on a logarithmic transformation). The 1–2–5
series is the usual rounding, but it is **not** an ISO series, so do not cite
ISO 3 for it. The range should reach the region where the effect ends (van
der Kouwe A3: "fail to test performance over an appropriate range of
settings"; ten Broeke 2016 ¶4.3: choose a wide range so as not to "ignore
interesting model behaviour").

**k6. Subsets and comparators.** Van der Kouwe A2 names "subsetting without
proper justification"; Rossow B.3 says authors should "describe how they
selected the … subsets". Any scheme, mechanism or scenario the simulator
offers and the experiment leaves out needs its reason in one clause. Van der
Kouwe D3 adds that a comparator run away from its published configuration is
an unfair benchmark, so each comparator runs at its own settings or the
change is stated.

**k7. What an examiner checks first**, drawn from the standards above:
1. A value with no basis.
2. A run count with no justification, or a misquoted recommendation.
3. No terminating or steady-state statement, and no reason the run is long enough.
4. A seed claim with no description of how the streams are split, or a paired claim beside a test that assumes independence.
5. A sweep that stops before the effect ends, or levels with no spacing logic.
6. An unexplained subset, or a comparator run away from its own settings.
7. No version pin behind "default".
8. Relative numbers only, with no absolute values and no variance (van der Kouwe F4, B4).
