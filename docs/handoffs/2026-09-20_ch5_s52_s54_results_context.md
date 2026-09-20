---
status: open                  # standing context for §5.2–§5.4; retire in the commit that takes the last of the three sections through pass 6
created: 2026-09-20
companions: 2026-09-09_ch5_experiments_design.md (the design record, §8–§9, §17–§18), 2026-09-17_ch5_s532_s55_defended_runs.md (the run plan), ../workflows/evaluation_conventions.md (the corpus conventions this file applies)
---

# §5.2–§5.4 — what the three results sections are for, who they are for, how they are titled, and the frame they must stay inside

> **Mode note.** Written 2026-09-20 at Marc's ask, top-down, **structure only**:
> the floats and any drafted captions are treated as a black box and no result
> is read or quoted here. This is orientation for the sessions that draft the
> three sections, not a draft. Nothing in it is a sentence for the chapter;
> every heading change it proposes is Marc's to rule (§4). Where it overturns
> an earlier ruling it names the ruling.
>
> **Numbering.** The sensitivity section was cut today, so the chapter is
> §5.1 Experimental setup, **§5.2** attacker behaviour, **§5.3** defence
> effectiveness, **§5.4** defence efficiency. Every record and tex comment
> written before 2026-09-20 calls these §5.3, §5.4, §5.5. This file uses the new
> numbers throughout.

---

## 1. The reader, and what they are owed

**Who.** A computer science student or examiner: fluent in systems and
security at a general level, not an MTD specialist, and not a reader of this
repository. They have read chapters 2 to 4 once and §5.1 a page ago.

**What they hold when §5.2 opens** (all of it from §5.1 and nothing more): one
fifty-host network that never changes; two attackers, the baseline attacker and
the movement attacker on its four attack profiles and the aggregate, both
pursuing the targeted objective; ten defence conditions, no defence among them,
at two deployment intervals; the metrics of Table 5.2, filed under Table 3.1's
purposes and measures; a thousand runs per cell.

**What they are asking.** §5.1 told them *how the experiment is built*. The
question they carry into the results is the plain one: **did changing the
attacker change the answer?** That is SQ3 word for word, and it is the only
question the chapter exists to settle.

**Why a general CS reader should care, stated once and early.** The thesis's
result is an instance of something every CS reader already believes in another
setting: *an evaluation's conclusion is a function of the workload it was run
under.* A benchmark ranks systems differently under a different workload; a
classifier scores differently on a different test distribution. In MTD
evaluation the attacker model is the workload, and chapter 3 closed on exactly
this (every effectiveness metric is computed over the attacker model, so a
weak attacker model is the weakest link). The three results sections are what
it looks like to take that seriously: show the new workload, score the system
under it and under the old one, then price the score. This analogy is
orientation for the drafter; whether any of it reaches the page is Marc's
call, and if it does it belongs in the chapter opening, once.

**The value the reader takes from each section**, in the order they need it:

| § | The reader's question | What they leave with |
|---|---|---|
| 5.2 | Before I trust a defence number computed over this attacker: what does the attacker actually do when it is run? | The campaign it walks with nothing opposing it, how it differs across profiles and from the baseline attacker, how it responds when disrupted, and the no-defence reference every later number is a difference from |
| 5.3 | What do the defences achieve against it, and is that the same answer the baseline attacker gives? | Which defence conditions reduce what the attacker reaches, whether that depends on the profile, whether it depends on the attacker model (SQ3), and whether prior evaluations' claims keep their direction |
| 5.4 | What did that cost, on each side? | What each condition forces the attacker to spend, what it costs the defender to run, and the two read together |

If a paragraph in these sections does not serve one of those three questions it
is in the wrong chapter (§5).

---

## 2. Is the three-way split right? Yes, and here is what it rests on

**The split is two conventions composed, and both are attested.**

1. **The funnel** (evaluation conventions §f; He 2025 is the clearest
   instance). When the contribution is an *attacker*, the same run set must
   characterise the attacker and evaluate the defence. The corpus's answer is
   to characterise the attacker on the undefended target first, then evaluate
   the defence against it. That is §5.2 before §5.3, and it is why §5.2 is a
   step in the argument and not a detour.
2. **The purpose axis** (Cho's effectiveness / efficiency, which Table 3.1
   already implements and Table 5.2 already files the metrics under; Kim's
   performance / security split is the field's plain form). That is §5.3 and
   §5.4.

So the chapter is organised **object first, then purpose**: the attacker, then
the defence read for what it achieves, then the defence read for what it costs.
He's results section has exactly this shape (attack effectiveness, then defence
performance, then efficiency). Conventions §b says a paper picks one organising
axis and names it in a roadmap sentence; a composed axis is fine provided the
roadmap names the composition. **That sentence is owed by the chapter opening**
(still a placeholder), along with the reason two attackers are run at all,
which §5.1 deliberately no longer says.

**The results-fitting test passes** (Marc, 2026-09-09: would this heading still
be here if the result came out the other way?). §5.2 exists because the
contribution is an attacker; §5.3 and §5.4 exist because the field's taxonomy
names two purposes; the attacker-model subsection exists because SQ3 asks it.
None depends on the direction of a number.

**The imbalance is convention, not neglect.** §5.3 has three subsections and
§5.4 none. Efficiency is the thin half in the corpus too, and here it is thin
for a stated reason: the half of the field's efficiency axis that needs a
workload model (quality of service, performance overhead) cannot be
instrumented on this simulator. §5.4 says that once, as scope.

**One placement question, settled on merit.** §5.2.2 reads defended runs, so
why is it not in §5.3? Because the *object read* is the attacker (property 4,
adaptivity, is definitionally about what changes under disruption and cannot be
read from the no-defence runs). §5.3 reads the defence. The distinction is the
object, not the condition, and the current §5.2.2 heading hides it (§4).

---

## 3. What each section motivates, and what it hands on

Stated as jobs and hand-offs. No findings: the direction of every result is
left to the findings records and the generators.

### §5.2 — the attacker, run

- **Answers:** does the attacker model, executed, show the properties chapter 4
  built it to have? It reads the properties the model implements, by number
  (Table 3.2): 1 to 3 without defence, 4 under defence. Properties 5 and 8 are
  absent by ruling and 6 and 7 sit at their inert settings; none of the four is
  read here.
- **Register:** *observations about the model*, never a verdict and never
  "validation" (Marc's ruling, 2026-09-18: a self-chosen instrument set cannot
  carry a claim of proof). The verdict is §6.2's.
- **Owes at its head:** the declaration of the four things it reads (campaign
  coverage, opening variety, profile divergence, response to disruption) and
  the condition each is read under. They left Table 5.2 on the ruling above and
  are declared where first used (conventions §a).
- **Owes at the head of §5.2.2:** the control in which the attacker's routing
  is made blind to the outcome its actions return. It is run and declared
  nowhere yet.
- **Hands §5.3:** the no-defence reference, and the reason hosts reached is the
  quantity suppression is computed on. State it as a rule, because it is what
  makes §5.2 the funnel's first movement.
- **Hands chapter 6:** the evidence for §6.1 (what the movement attacker has
  captured) and the rows of the fidelity table in §6.2.

### §5.3 — what the defences achieve

- **Answers:** SQ3. Three questions in order of dependence: which defence
  conditions reduce what the movement attacker reaches, and does it depend on
  the profile (§5.3.1); is that the answer the baseline attacker gives
  (§5.3.2, the thesis's own claim); do prior evaluations' headline claims keep
  their direction on one simulator under both attackers (§5.3.3).
- **Every number is a difference from the no-defence reference.** "Baseline"
  never names that reference: *baseline attacker* is the comparison attacker,
  *no defence* is the control (conventions §f2).
- **Owes at its head:** that "the movement attacker" in the pooled floats is
  the four profiles pooled, and the success criterion at the metric
  (suppression is already defined in Table 5.2; say what counts as a separation
  before the first result, He's form).
- **The comparability boundary is restated in §5.3.3 and nowhere else:**
  configurations are re-run; published numbers are not comparable.
- **Hands chapter 6:** §6.3, what changes for MTD evaluation.

### §5.4 — what it costs

- **Answers:** the price of §5.3's effect, on both sides, on Table 5.2's four
  efficiency metrics, then the two read together.
- **Owes:** the one-sentence scope statement (no service-to-users or overhead
  metric), and, if return on attack is named at all, which sense is meant.
- **Hands chapter 6:** §6.3 again; the defender-side metric is priced
  identically under both attackers, which is what lets the two be compared
  directly.

### The shape of a results paragraph — settled by convention (2026-09-20)

Marc: results state the facts, and what is in the section against what is not
is decided by the convention. The survey
([`../implementation/evaluation_anatomies/`](../implementation/evaluation_anatomies/))
answers it, and the answer turns on the *form of the document*, not on taste:

| Document has | Where the reason for a result goes | Papers |
|---|---|---|
| no discussion, or a discussion that is limitations only | folded into the results, a "this is because" or "we hypothesise" sentence after each observation | Zhang, Reti, He, Kim, Ho's §4.3 |
| a discussion chapter that mirrors the results subsection for subsection | the results carry the numeric readout and **no** reason; every result gets its reason in the mirror | Tay (this supervisor's lineage, and the ruled shape of ch5/ch6) |
| a separate discussion section, not mirrored | a one-sentence structural reason stays beside the observation; interpretation and recommendations go to the discussion | Brown, Hong, Masud |

This thesis has a discussion chapter built to mirror chapter 5, so it sits in
the second row. Conventions §e's four moves were distilled mostly from
documents in the first row, which have nowhere else to put a reason; they do
not transfer whole. **The rule for §5.2–§5.4:**

1. **The observation**, as ordering or trend, magnitude as a relative figure.
2. **A reason only where it is true by construction**: a fact the setup or
   chapters 2 to 4 already declared (the baseline attacker's coverage line is
   flat because it has six activities; a metric is zero on one attacker because
   it is not defined there). That is a fact, so it is a result-section
   sentence. Brown and Hong keep exactly this much.
3. **The exception**, marked as one, stated and not explained.
4. **The hand-off**: what the subsection gives the next.

A reason that was not measured, what a result means, and any recommendation
are chapter 6's, in the section that mirrors this one. The test for a sentence:
*could it be false while every number in the floats stayed the same?* If yes,
it is interpretation and it moves.

---

## 4. The headings — audit and proposals

**The convention** (design handoff §17, from the corpus): a results heading is
a noun phrase of two to five words naming the *quantity measured*, the *factor
varied* or the *object evaluated*; no verb, no claim; the claim is the
section's first sentence. Plus Marc's rules: sentence case, no acronym but APT,
"movement attacker" is a name for the prose and not for headings.

**How the corpus balances sibling titles**, which is the part §17 did not
record: siblings at one level name the *same kind of thing*. Hong's subsections
are all factors; Brown's are all metrics; Kim's two are both purposes. A
factor-level heading ("Without defence") works when the quantity is constant
across the siblings and only the factor moves. Where the quantity changes
between siblings, the heading has to name the quantity or the reader cannot
tell the siblings apart from the table of contents. Two of the current
headings fail on that test, and one fails on the claim ceiling.

| § | Now | Verdict | Proposed | Why |
|---|---|---|---|---|
| 5.2 | APT attacker behaviour | **change** | **Behaviour of the APT attacker model** (or the stacked form, *APT attacker model behaviour*) | As written it reads as a claim about how real APT attackers behave, which the claim ceiling bars (a run is one instantiation of a behavioural envelope, not an actor). The section reports the *model's* behaviour. Adding "model" also pairs it with chapter 4's title, so the table of contents reads: the model built (ch4), the model run (§5.2). He's property-of-object form. |
| 5.2.1 | Without defence | keep | — | Names the reference condition the whole of §5.3 reports against, which a reader will look for by that name. Brown's "None". |
| 5.2.2 | Under defence | **change** | **Response to disruption** | Collides with §5.3, all of which is under defence; and the quantity changes between §5.2.1 and §5.2.2, so a condition pair hides what differs. This names the quantity, in the ratified word (*disruption*, 2026-09-08). Overturns the 2026-09-13 pairing on merit; it is that day's own "was" column. |
| 5.3 | Defence effectiveness | keep | — | Cho's purpose with the object named; pairs with §5.4; is Table 3.1's and Table 5.2's row-group word, so the reader has met it twice. The vagueness Marc feels is cured by the first sentence (what an effect is measured as, against what), not by the title. |
| 5.3.1 | Mechanisms and schemes | **tighten** | **Defence mechanisms and execution schemes** | Bare "schemes" is unregistered; *defence mechanism* and *execution scheme* are chapter 2's ratified nouns, and the reader can look both up. Names the factor varied. |
| 5.3.2 | Attacker comparison | **change** | **Effect of the attacker model** | "Comparison" of what, on what? The factor varied is the attacker model, and the corpus's factor form is Ho's *Impact of MTD interval*. It echoes SQ3 and chapter 3's closing argument, and it carries no claim: the subsection stands whether or not there is an effect. |
| 5.3.3 | Prior evaluations | **change** | **Comparison with prior evaluations** (alternative: *Prior evaluations re-run*) | As written it reads as related work. Masud's attested form. The comparability boundary goes in its first sentence, because "comparison" invites the numeric reading the boundary forbids. |
| 5.4 | Defence efficiency | keep | — | Pairs with §5.3. No subsections at one unit; the attacker side, the defender side and the two together are paragraphs. |

**Audit of the proposed set against Marc's traps:** sentence case; APT the only
acronym; "movement attacker" in no heading; two to six words; no verb; every
heading survives the result coming out the other way.

**RULED AND APPLIED 2026-09-20 (Marc: "all the headings I approve").** The five
changes are in the tex and in `FLOATS.md`, with the of-form for §5.2; build
clean at 90 pages.

**Labels do not change** (`sec:attacker-in-operation`, `subsec:aio-unopposed`,
`subsec:aio-disruption`, `sec:effectiveness`, `subsec:eff-under-defence`,
`subsec:eff-cross-arm`, `subsec:eff-lineage`, `sec:efficiency`), so every
`\ref` stands.

---

## 5. The frame — what these sections may say, and in which words

**The abstraction level.** The reader is being shown *a model of a network
under defence*, not this repository (the register constraint ruled 2026-09-09,
which binds the whole chapter). Every boundary is stated in modelling language:
a defence "destroys the attacker's position" or "re-rolls the surface it
exploits"; it never "clears the host cursor". The implementation record holds
the mechanism.

**The antecedent rule.** Chapter 5 prose uses only objects chapters 2 to 4 and
§5.1 have already named. A needed object with no antecedent becomes a chapter 4
insertion or a declaration at the head of the section that first uses it
(§3 lists the two owed), never a first use mid-result.

**The vocabulary these sections run on** (the living registry is
[`../workflows/terminology.md`](../workflows/terminology.md); this is the
subset in play):

| Say | Never |
|---|---|
| movement attacker; baseline attacker | inherited / original attacker; arm; "the model" bare, where it could mean either |
| attack profile (the four), the aggregate | the nets, class, GASP |
| no defence, the no-defence reference | "baseline" for the control |
| defence mechanism; execution scheme; deployment strategy (the covering term) | MTD mechanism / technique; bare "scheme" |
| deployment; deployment interval; timing distribution; time limit | mutation; mutation interval / tempo; timing regime; horizon; run length |
| disruption | block (Brown's word, only as his metric's name) |
| tactic; verb; dwell time; failure matrix; stage (lifecycle) against phase (the baseline attacker's six) | action mix; place; token; overlay; sentinel |
| property (the eight, by number, Table 3.2); partial | axis; badge; DEMONSTRATED / DESIGNED |
| metric, by its Table 5.2 name to the letter (target reached; runs with no compromise; blocked fraction; delay to first compromise; hosts reached; suppression; actions per host reached; successes per host reached; time lost to MTD; share of run under reconfiguration) | a second name for any of these; internal MTTC (unruled); "measure" as the noun |
| observation (of the §5.2 quantities) | validation; ablation; "less predictable" (the field owns *predictability* for something else); "less detectable" |
| targeted objective; opportunistic objective (only in §5.3.3) | scenario; general |
| this thesis; the simulator / MTDSim | substrate; any disposition number, function name, version pin, hypothesis label, "kill criterion", "pre-registered" |

**What these sections do not talk about**, so a drafter can refuse it on sight:

- the fidelity verdict, or any scoring of the eight properties (§6.2);
- what a result *means* for MTD evaluation practice (§6.3);
- properties 5 to 8, and the cost and learning capabilities (held at their
  inert settings in §5.1; chapter 7 where they are future work);
- the declared parameters' robustness (Appendix C; one owed sentence of Marc's
  where the 200 s suppression figure is reported, and no more);
- how real APT attackers behave (the claim ceiling: behavioural fidelity
  changes the answer, never the attacker model is true);
- published numbers from prior evaluations as comparands;
- deployment strategies that were not run;
- evaluate as a layer (it carries no layer number).

**Numbers.** No number reaches the prose except from a tracked artefact through
a generator, at the configuration the chapter reports (a thousand seeds; the
word "preliminary" appears nowhere). Every number in a tex comment is
provenance, not a value; several are known stale.

---

## 6. Opening slots, per section

Slots in Marc's sense (job, facts, ceiling; no content). One sentence each
unless marked.

**Chapter opening (roadmap, owed).** (a) what chapter 4 left and this chapter
does with it; (b) why two attackers are run, which is SQ3; (c) the order and
its reason: the attacker first, then the defence for what it achieves, then for
what it costs; (d) where interpretation lives (chapter 6). Ceiling: no result,
no layer number.

**§5.2 head.** (a) the section's question; (b) the four quantities read and the
condition each is read under; (c) the register: observations, the verdict is
chapter 6's. Ceiling: not "validation".

**§5.2.1.** Opens on its claim. Closes on the hand-off: the no-defence
reference and the rule for the quantity suppression is computed on.

**§5.2.2 head.** (a) why this property cannot be read without defence; (b) the
two mechanisms that span how a defence reaches the attacker, in chapter 2's
layer words, and the two deployment intervals; (c) the control, declared.

**§5.3 head.** (a) the object has changed: the defence is now what is
evaluated; (b) every number is a difference from §5.2.1's reference; (c) the
pooling of the four profiles; (d) what counts as a separation.

**§5.3.2.** Opens on SQ3 as the subsection's claim slot. Ceiling: states the
grade the evidence carries and nothing about what it means.

**§5.3.3.** First sentence carries the comparability boundary.

**§5.4 head.** (a) the question (the price of §5.3's effect); (b) both sides,
by Table 5.2's names; (c) the scope sentence.

---

## 7. Rulings

1. **The five headings: approved and applied** (2026-09-20).
2. **The results-paragraph shape: settled by convention** (§3), on Marc's
   direction that results state the facts.
3. **The frame of §5: agreed** (2026-09-20).
4. **The workload analogy of §1: not ruled, and nothing depends on it.** It is
   drafter orientation only and reaches the page only if Marc later wants it.
   Plainly: a benchmark's ranking of systems depends on the test load it is run
   with; here the attacker model plays the part of the test load.

## 8. Figure 5.1 critique (2026-09-20; critique upheld, design 8b RULED YES AND APPLIED the same day)

Marc's read of `fig:aio-coverage`, cross-examined against the corpus
(`data/results/ch5_s531_unopposed/`). Nothing applied to the figure yet.

| Marc's point | Checked | Verdict |
|---|---|---|
| Panel (b) is a subset of (a) and adds nothing | Coverage saturates inside 2 000 s of a 15 000 s run; (a) is 85 % flat line | Upheld. One coverage panel, on the window where the curve moves |
| No visible shaded band | The 95 % half-width is 0.15–0.5 tactics on a 0–15 axis | Upheld. The band is drawn and is sub-pixel; the caption promises what the reader cannot see |
| Tactics against the baseline is not a fair comparison | The baseline line counts its six *activities*; the profiles count *tactics*. Two units on one axis | Upheld. The 6-against-14 gap is two vocabulary sizes, a construction fact, not a result |
| The baseline succeeds and fails, so it has distinct openings | `analyse.py` hard-codes the baseline's openings to 1 ("structural"). Measured from the recorded runs: 1 up to length 6, then 2 at length 7 and 4 at length 8 | Upheld. "One ordering at every length by construction" is false as drawn; the baseline series must be measured like the others |
| What are the tactics? | The figure counts tactics and never names one | Upheld. The reader cannot tell what campaign was traversed |
| The flat line at six is a construction limit, not research | Same for each profile's plateau if it equals the profile's own tactic count (to check) | Upheld. By the §3 test these are by-construction facts: one sentence, not a figure's headline |

Found beyond Marc's list:
- The opening count is capped by the run count (exfiltration hits 100 of 100 at
  length 8) and the corpus here is 100 seeds where the thesis declares 1 000.
  A count that depends on sample size needs a normalised form (share of runs
  that are unique, or number of runs sharing the commonest opening).
- "Opening sequence" and "places" are not chapter 4 vocabulary at the axis.
- The only non-construction facts in the figure: every campaign is opened
  within about 2 000 s; the profiles differ in how fast; double extortion has
  the widest coverage and the *fewest* openings (30 against 96–100).

### 8a. What the reader takes from §5.2.1 (agreed 2026-09-20)

| # | Takeaway | Carried by |
|---|---|---|
| T1 | The attacker runs a named, multi-stage campaign, where the baseline attacker has six activities and no campaign | Fig. 5.1(a); one body sentence for the baseline |
| T2 | The campaign depends on the objective: the four profiles are different campaigns | Fig. 5.1(a) in detail; Fig. 5.2 in one number per pair |
| T3 | A profile does not run its campaign the same way twice | Fig. 5.1(b) |
| T4 | The no-defence reference the defence sections are read against, including that a fuller campaign does not mean a better outcome (target reached sits below the baseline's) | Table 5.3 |

Pace is not a takeaway. It is one hand-off sentence (every campaign is opened
within about 2 000 s, the order of the deployment intervals) into §5.2.2.

### 8b. Figure 5.1 design — applied 2026-09-20 as `fig_5-2-1a_campaign_openings`; body-text reading and the thousand-seed rerun still owed (supersedes the tactic-by-time proposal, withdrawn: time is not the question)

Rulings taken: small-seed corpus while the structure settles, the full
thousand once it has (Marc, 2026-09-20). Old panels (a) and (b) go: each
profile's plateau is its own tactic count (14, 14, 12, 13 held; 13.6, 14.0,
11.8, 12.8 reached), so the curve is a construction fact on both attackers.

**Panel (a) — tactics entered, by profile (T1, T2).** Printed-value matrix,
the genre of Fig. 5.2. Rows: the named tactics in the order chapter 4 lists
them. Columns: the four profiles (no aggregate, no baseline). Cell: share of
runs that enter the tactic, printed; grey fill by value; a tactic the profile
does not hold is left empty and decoded in the caption. No time, no order of
entry. What it shows on the current corpus: most cells are 100 %; the profiles
differ in which rows are empty (resource development, exfiltration, impact,
defence impairment) and in three partial cells (impact 60 % on the
exfiltration profile; initial access 81 % and collection 81 %).

**Panel (b) — repeatability of the opening (T3).** Line chart, x = length of
the opening in steps (1 to 8), y = share of runs that follow the profile's
most common opening of that length. Replaces the count of distinct openings,
which is capped by the run count. Does not depend on the number of seeds.
Baseline MEASURED from its recorded runs, steps being its activities (the
caption says so). Current corpus: baseline 100 % to length 6, 98, 94; the
exfiltration, impact and no-realised-objective profiles fall to 1-2 % by
length 8; double extortion holds 68 %. "Step" = a tactic entered; "places"
leaves the axis.

**Caption** says what the panels are and how to read them; the "intention"
sentences move to the body text.

**Generator work:** `analyse.py` gains the entry-share matrix and the
commonest-opening share, and measures the baseline (the hard-coded 1 and the
structural 0.0 entropy go); `tools/ch5_unopposed_figures.py` redraws. Table
5.3's openings column follows the same measure.

**Open check, not blocking:** by order of first entry the exfiltration profile
reaches command and control second and initial access tenth. Panel (a) does
not show order, so the figure is safe, but whether that order is the source
reports' or a recording artefact should be known before chapter 6 reads it.

## Validation gate

This file has done its job when each of §5.2–§5.4 opens on the slots in §6,
uses only the left-hand column of §5's table, and the headings carry Marc's
rulings on §4. Retire it in the commit that takes the last of the three
sections through pass 6.

## Reading list

- [`../workflows/evaluation_conventions.md`](../workflows/evaluation_conventions.md) §b, §e, §f, §f2, §h
- [`2026-09-09_ch5_experiments_design.md`](2026-09-09_ch5_experiments_design.md) §8–§9 (the split and the funnel), §17 (the heading convention)
- [`../workflows/terminology.md`](../workflows/terminology.md)
- `docs/thesis/dissertation.tex`, the chapter 5 comment blocks above each heading (old section numbers)
- [`../workflows/results_section_workflow.md`](../workflows/results_section_workflow.md), before any float is touched
