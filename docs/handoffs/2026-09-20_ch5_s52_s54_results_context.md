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

> **Superseded in shape, 2026-09-22.** The supervisor ruled the chapter into
> two phases read from the APT attacker's perspective — the APT attacker model
> against the baseline attacker without defence; the defences against the APT
> attacker model, effectiveness and efficiency merged, the baseline as a
> reference line (register E1) — and ruled the model's name, the layer
> trichotomy and *suppression* out of the dissertation's surface (E2, E3). §2
> (why the three-way split is right), §4 (the five headings) and §6 (the opening
> slots) are therefore superseded by the two-phase restructure (landed
> 2026-09-23: §5.2 *APT attacker model versus baseline attacker*; §5.3 *APT
> attacker model versus MTD* = 5.3.1 Response to disruption, 5.3.2 Effect of the
> attacker model, the headline, 5.3.3 Defence mechanisms and execution schemes,
> the depth; §5.3.3 Comparison with prior evaluations and §5.4 retired). Owed here
> when drafting starts: re-cut §6's opening slots for that set, and reverse T14's
> hand-off (the headline now comes first and the depth breaks it down);
> §1 (the reader), §3 (the paragraph shape), §5 (the frame, with its vocabulary
> re-keyed by the terminology brief) and §8 (every figure's record) stand.

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
| attack profile (the four), by code from chapter 4: $c_1$ exfiltration, $c_2$ impact, $c_3$ double extortion, $c_4$ no realised objective; the aggregate, $c_{\mathrm{agg}}$ (ruled 2026-09-22, §8f) | the nets, class, GASP; C1, "profile 1" |
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
| T2 | The campaign depends on the objective: the four profiles are differently weighted campaigns (amended 2026-09-21, §8d) | Fig. 5.1(a); two body sentences on the pairwise divergence (was Fig. 5.2, demoted) |
| T3 | A profile does not run its campaign the same way twice | Fig. 5.1(b) |
| T4 | The no-defence reference the defence sections are read against: at the time limit the movement attacker has reached less than the baseline attacker because it is slower, and the pace is set by chapter 4's declared dwell times (reworded 2026-09-21 on Marc's ruling, §8e; the old clause "a fuller campaign does not mean a better outcome" reversed when the limit moved) | Table 5.3; one framing paragraph owed |

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

### 8c. Second rework, applied 2026-09-20 — this supersedes the panel definitions in 8b

8b's panel (a) (share of runs ENTERING each tactic) was a wall of 100s: profile
membership, a construction fact, the same failure as the coverage curves. Its
panel (b) fell where the claim rises and compared unlike steps. Two reviewers
(a cold reader given only figure, caption and one body sentence; a critic
reading against this file) rejected it; the third design passed both with no
blocking defect. Scope ruling (Marc): Figure 5.1 only; Figure 5.2 and the table
are not restructured in this pass.

- **Panel (a), T1 and T2:** share of each profile's steps that fall in each
  named tactic, pooled over runs (`tactic_visit_share`; the distribution the
  divergence matrix is computed over). Dash = not in the profile; 0 = in the
  profile, never entered (resource development, on exfiltration and impact);
  <1 = below one per cent. Profiles only.
- **Panel (b), T3:** share of runs that have LEFT the attacker's most common
  opening, rising, lengths 1 to 8, baseline an ordinary measured series.
- **One unit, the step:** a tactic entered (profile) or a phase entered
  (baseline). The baseline's consecutive repeats of one phase are collapsed
  (77 % of its records); uncollapsed, its first six steps were four phases and
  the comparison was not like for like. Measured so: 0 % to length 4, 22 % from
  length 5 (the exploit outcome branches to brute force or to scanning
  neighbours). Three profiles reach 98-99 % by length 8; double extortion 32 %.
- **Fairness, no normalisation:** departure needs branching, not vocabulary (a
  fixed attacker of any vocabulary stays at zero), and the figure holds its own
  control: exfiltration (15 tactics) and double extortion (14) sit at opposite
  ends. Body text states this as an observation.
- **Motivating sentence the body text owes (content, not prose):** a defence
  that works by overturning what the attacker has learned is only tested by an
  attacker whose next move is not fixed. The text must not say the baseline is
  fixed outright: 22 % of its runs branch at step five.
- **Exception to mark, not explain:** double extortion sits beside the
  baseline. Chapter 6 owns why.
- **Tactics held, with the synthetic overlay: 15, 13, 14, 13** (8b's 14, 14,
  12, 13 were tactics ever entered). Reconcile before the text cites a count.
- The method for settling a figure, kept: blind reader plus context critic,
  repeated until neither reports a blocking defect.

### 8d. Figure 5.2 demoted, 2026-09-21 (scrutinise-figure pass; Marc: "put it into the comment, remove the figure")

Three reviewers together (cold reader on the PNG and caption only; context
critic against this file; sceptical examiner on the claim) and none was told
the other's verdict. All three: the 4 × 4 divergence matrix re-expressed
Figure 5.1(a) as one number per pair, its split-half null was a floor that
could not be failed (sampling noise of a distribution pooled over ~50 000 steps;
pairs clear it by sixty times and more, and the ratio only grows at a thousand
seeds), the caption gave no scale (the measure runs 0 to 1), and half the cells
were repeats. Under §3's test "every pair clears its null" is a construction
fact. Verified beyond the reviewers' word: the two floats used different
denominators (the suite's divergence dropped zero-dwell resource-development
records; reconciled to every record, Marc's ruling by acceptance); tactics
held by only one profile of a pair carry 9–51 % of each cell; the size-matched
label-blind control has never run at L3. Rejected: the critic's flow counts of
19, 8, 6, 5 (the audit and chapter 4 say 19, 7, 7, 5).

- **Outcome:** the figure environment, its generator panel and its files are
  gone; the tex comment at the former site carries the content points for two
  T2 body sentences and the ceilings for chapter 6. FLOATS.md and the findings
  record are updated.
- **8a amended:** T2 is *differently weighted campaigns*, carried by Figure
  5.1(a) plus two sentences (the 0–1 scale, the range 0.08–0.21, closest and
  farthest pair, noise below 0.002); "the one property shown to change an
  outcome" may not be read from this measure, and the outcome non-separation
  (target reached and hosts reached intervals overlap) is a T4 fact.
- **Chapter 6 ceilings:** mean divergence to the others rises as flow count
  falls (the aggregate column's confound inside the pairwise cells); the
  label-blind arm is unrun, so T2 carries the caveat.
- **Terminal-tactic half:** 3 of 6 pairs clear at 100 seeds; T4's paragraph,
  one clause, only if it still fails at a thousand.
- **The one rework that would have earned a figure**, declined as a second
  chart about the same matrix: six bars, one per pair, on a 0–1 axis, each
  split into the part from tactics only one profile holds and the part from
  reweighting the shared ones.

### 8e. Table 5.3 cut to the no-defence reference, 2026-09-21 (scrutinise-figure pass; Marc: "let's get this down")

- **Takeaway under test:** T4 only. T1 to T3 are Figure 5.1's.
- **Marc's read, upheld column by column:** distinct tactics and the commonest
  opening repeat Figure 5.1; path entropy's own footnote said not to read it;
  successes per host printed no baseline value; ended at time limit is one minus
  target reached on an arbitrary limit; no footnote earned its place; several
  terms were defined nowhere.
- **Applied:** four Table 5.2 columns (hosts reached, target reached, delay to
  first compromise, runs with no compromise); rows grouped under *movement
  attacker* with the profiles indented, then *baseline attacker*; the aggregate
  kept (Marc: it is a profile); no footnotes; caption says how to read only and
  points at Tables 5.1 and 5.2.
- **Fairness check (Marc's instruction):** both attackers stop acting at the
  target, so the comparison is under one stopping rule; the rows reproduce
  Table 5.4's pooled no-defence row. Detail in the findings addendum.
- **Cold reader (never given T4):** its message was T4 (three times the hosts,
  target in 0.58 against 0.05 to 0.17, first compromise three times sooner;
  profiles alike). Two blocking reports: (i) nothing frames the gap, so the
  reader concludes the model is "simply worse" — that is the T4 paragraph's
  job, content points 1 and 2 in the tex comment, and is OWED in body text;
  (ii) no network size or run length — answered by the caption's pointer to
  Table 5.1. Declined: shares as per cent (Tables 5.4 and 5.5 print decimals),
  intervals on shares, Table 5.2's column order (hosts reached leads because it
  is the suppression denominator).
- **Profile codes (C1 to C4, C_aggregate):** considered on Marc's suggestion,
  not applied. Chapter 4 uses $c$ as an unenumerated index, so codes need a
  chapter 4 insertion first (antecedent rule), then Figure 5.1 and Table 5.3
  change together. Open for his ruling.
- **Correction carried:** the §8d ceiling said hosts reached overlaps between
  profiles; adjacent pairs do, the ends do not (impact against exfiltration and
  no realised objective). Tex comment amended.

#### 8e, second pass the same day — the full scrutinise-figure run on the reworked table

Four reviewers, launched together: a fresh cold reader, the context critic, a
numbers auditor, a sceptical examiner. Every accepted finding was checked
against `numbers.json` or the raw runs first.

- **Numbers auditor:** all 24 cells reproduce from `runs.jsonl` without the
  analyser; both attackers stop acting when a target falls (53 of 53 movement
  runs, 58 of 58 baseline runs); one compromise event per host on both; the
  pooled 400 profile runs give Table 5.4's no-defence row exactly.
- **Context critic:** passes, T4 delivered, not a duplicate of Table 5.4 (the
  baseline row, the per-profile rows and the aggregate appear nowhere else).
  One blocking fix, applied: the caption said "run length", a word §5 lists
  under Never; it now says "time limit", Table 5.1's row. One estimator fix,
  applied: target reached on the movement row now requires a target host held,
  as the baseline row does. Nothing moves at 15 000 s; at 60 000 s impact goes
  0.64 to 0.62 and the aggregate 0.60 to 0.58.
- **Cold reader (never given T4):** message matched T4. Blocking: no run count
  (the thesis declares it in Table 5.1, and the caption now points there), and
  nothing says the gap is expected (body text, below).
- **Sceptical examiner, upheld from the data: T4's second clause does not
  survive the §3 test.** At 60 000 s the same corpus reads target reached 0.58,
  0.62, 0.58 and 0.36 (exfiltration, impact, aggregate, no realised objective)
  against the baseline attacker's 0.67, and 17 to 21 hosts against 25. The gap
  at 15 000 s is pace under a time limit, and chapter 4 declares the dwell
  times as inputs. **RULING OWED:** T4 reworded to "at this time limit the
  movement attacker has reached less, because it is slower", and whether the
  60 000 s reading enters the table, the body text or neither (Table 5.1 does
  not declare it).
- **Also upheld:** double extortion stalls and is not merely slow (9.2 hosts,
  0.05, 0.08 with no compromise at 60 000 s; steps per run 454 to 1 742), an
  exception to mark and hand to chapter 6; "three times sooner" is about 2.6
  times on medians; the delay's ordering among profiles is not read because it
  is conditioned on compromise. All are content points 6 to 11 in the tex
  comment.
- **Declined, with reasons:** intervals on the share columns (the examiner
  wanted them at 100 runs; the thesis reports 1 000, where he agrees it is
  pedantry, so the body text says the profiles are not separated instead);
  "of 50" in the header (Table 5.1); per cent for shares (Tables 5.4 and 5.5).
- **Open check, the examiner's third attack:** hosts reached is cut short by
  the stop at the target in 0.60 of baseline runs against 0.05 to 0.17 of the
  movement attacker's, and under defence that share falls, which pushes the
  baseline attacker's suppression toward zero. The movement attacker without
  the stop moves 7.44 to 7.51; no baseline run without the stop exists. This is
  §5.3.2's fairness question, not this table's, and needs a baseline arm on the
  opportunistic objective before it can be sized.

#### 8e, rulings after the pass (Marc, 2026-09-21)

- **T4 reworded** to the pace form (table above). "Slower is a fact; the dwell
  times are inputs."
- **Hosts reached carries its anchor:** the header reads "Hosts reached (of
  50)". This overturns the session's decline of the cold reader's "of 50".
- **Double extortion** is an exception marked in chapter 5 and discussed in
  chapter 6 (the sparse profile).
- **Marc's question, does the baseline attacker give up? Yes, measured on the
  60 000 s runs:** its mean hosts reached reads 4.6, 10.9, 19.9, 24.3, 25.2 at
  2 500, 5 000, 10 000, 15 000 and 20 000 s and is flat at 25.2 from there. It
  holds a target in 67 runs; in the other 33 its last compromise falls no
  later than 19 346 s (median 12 478 s) at a median of 27 hosts. The movement
  attacker is still climbing at 60 000 s (exfiltration 7.4, 12.8, 17.2 at
  15 000, 30 000, 60 000 s; impact 10.0, 16.6, 21.3; no realised objective 7.2,
  12.6, 20.1; aggregate 8.7, 15.3, 20.1), double extortion flat at 9.2 from
  30 000 s. So 15 000 s (Table 5.1, after Ho) reads the baseline attacker
  almost finished and the movement attacker about a third of the way.
- **RULED 2026-09-22 (Marc): the 60 000 s reading is a body sentence, not a
  figure.** The session's figure recommendation is overturned. The sentence's
  content: the baseline attacker adds no host after about 20 000 s; the
  movement attacker is still adding them at 60 000 s; double extortion is the
  exception. Prerequisite: 60 000 s has no antecedent (Table 5.1 declares
  15 000 s only, C36), so the sentence declares the extension in passing or
  Table 5.1 gains a row. Marc's call when the T4 paragraph is dictated.
- **Marc's read of T1 and T2 on Figure 5.1 (2026-09-22):** the figure alone
  does not make it clear that the baseline attacker has no campaign, and the
  profiles "look mostly the same, differing slightly". Both are what §8a
  already assigns to body sentences (T1: one sentence for the baseline; T2: the
  two divergence sentences from the content points at the former Figure 5.2
  site). No figure change; the sentences carry the load. Marc reads T4 as the
  concession that a fuller campaign does not translate to results; the honest
  form of that concession carries "at this time limit", per the 60 000 s
  numbers above.

### 8f. Formalism in §5.2.1's floats, profile codes, and the label-blind control (2026-09-22)

Marc, 2026-09-22: body sentences come once every float is settled, the
thousand-seed run is done and the size-matched label-blind control has run.
Three questions were put; two are answered here, one is open for his ruling.

**The size-matched label-blind control: what it is and what it shows.** The
four profiles differ in size (19, 7, 7, 5 flows) as well as in objective, so
a divergence between two profiles could be corpus size alone. The control
draws four groups of the same sizes from the 38 flows with the objective
labels shuffled, compiles each draw to a net by chapter 4's construction, runs
it, and measures the same divergence. If the labelled profiles diverge by more
than the shuffled draws do, the objective label carries the difference; if
not, size does. It is a fair comparison because everything but the label is
held: the corpus, the construction, the dwell times, the runs. It answers
"does the objective condition the campaign" (T2's attribution), which is what
the size confound leaves open. It does NOT show that the profiles "run
differently": that is already shown (every pair is sixty times its seed
noise) and is not in question. Marc's "they will run differently" is T2's
existence half, carried by Figure 5.1(a) and the divergence sentences; the
control is the attribution half. Design: `2026-09-09_ch5_experiments_design.md`
C19; `profile_divergence_findings.md` §7.

**Formalism in Figure 5.1 and Table 5.3 (context critic, verified against the
registry): keep the names, attach no symbol.** Reasons, each checked:
- "step is one tactic entered" is the chapter 5 rendering of $t_{pq}$ firing
  into $q$; *place* and *token* sit under Never in §5, and the unit has to be
  shared with the baseline attacker's "phase entered", which no net symbol can
  do.
- "share of the profile's steps" has no chapter 4 symbol. It is not $w_c$
  (a declared proportion); attaching it would be wrong, not decorative.
- "profile" against $c$ / $\mathcal{N}_c$: the registry (terminology.md row
  47) ratifies *attack profiles* and flags bare *the nets* as a conflation, and
  §5 lists *the nets* under Never. "They are the attack nets" is that
  conflation.
- Table 5.3's headers are Table 5.2 names by ruling; nothing to attach.
- No contradiction between the caption and chapter 4; row order agrees
  everywhere (exfiltration, impact, double extortion, no realised objective).

**Profile codes: RULED 2026-09-22 (Marc) and APPLIED.** "Trying to remember
four names is hard for the reader"; enumerate in chapter 4, use the codes from
there on. The session's names recommendation is overturned. Applied: §4.3
indexes the four ($c_1$ to $c_4$, in its listing order) and names the
aggregate $c_{\mathrm{agg}}$; §4.4 compiles the aggregate by the same
construction; the notation table row for $c$ carries the mapping; Figure 4.1's
L2 rows carry code and name (the figure precedes the declaration); Figure 4.3's
caption says "$c_1$, the exfiltration profile"; §5.1 and Table 5.1 declare the
attacker on $c_1$ to $c_4$ and $c_{\mathrm{agg}}$; every chapter 5 float keys
by code only, through the one map in `tools/_ch5_style.py` (and
`ch5_unopposed_figures.py`'s copy). Appendix tables keep the names (records
that predate the codes, said so in their captions). Facts the ruling was made
on:
- Chapter 4 never enumerates $c$; the notation table defines it as "one of
  the four objective classes" with no order. The smallest antecedent is one
  clause in that row: "$c \in \{1,\dots,4\}$ in the order of §4.3".
- The aggregate is outside the formalism: §4.3 compiles "each attack profile
  $c$"; no chapter 4 sentence compiles the aggregate. Codes would need a
  second insertion ("the aggregate compiles by the same construction").
- Blast radius: one map (`tools/_ch5_style.py` LABEL, plus
  `ch5_unopposed_figures.py`'s own), every chapter 5 float, §5.1's sentence,
  every body sentence.
- Session recommendation: names. A code forces a lookup on every float; the
  name carries the objective, which is T2's takeaway. If Marc rules codes, the
  form is $c_1$ to $c_4$ in prose and keys (the symbol the reader met), never
  "C1"; the aggregate stays "the aggregate".

### 8g. §5.2.2 Response to disruption — takeaways, the mechanism fact, and the redesign (2026-09-22; takeaways and design RATIFIED by Marc the same day, "design, run, execute")

**Marc's read of the landed figure (`fig_5-2-2a_adaptivity`), checked against
the findings record and upheld.** Four panels that look the same; no visible
response; the differences unhighlighted. The record already called it a null
(largest shift 2.5 points of share; the control inside the model's interval
in 26 of 28 cells). Two further defects Marc named and the session confirms:
(i) the reader cannot tell what the panels are (he read the 2 × 2 of mechanism
× interval as the four profiles); (ii) "five visits before", "outcome-blind
control" and "share of visits" over the six verbs are all undeclared at the
point of use. The deeper defect is **resolution**: the verb is downstream of
the tactic-to-verb mapping, and the distance term keeps the campaign near its
lifecycle order, so a verb-level mix inherits the baseline attacker's shape by
construction. The response has to be read where the model lives, on the
tactic and its lifecycle stage. The verb-level null becomes one body sentence
here and a limitation in chapter 6 (the campaign is ported onto the
simulator's six verbs).

**The mechanism fact, verified from code (the ruling Marc asked for: does the
mechanism or the state decide where the attacker is thrown back to?)**

| attacker | what decides the landing | source |
|---|---|---|
| baseline attacker | **the mechanism's layer**, whatever state it was in: a host-layer mechanism restarts it at scan host from any phase; a service-layer mechanism restarts it at scan port and bites only in scan port / exploit / brute force; the credential-layer mechanism bites only in brute force and sends it to look for vulnerabilities. The state decides *whether* the disruption lands; the layer decides *where* | `mtdnetwork/operation/mtd_operation.py` `_interrupt_adversary`; `attack_operation.py` `_handle_interrupt` |
| movement attacker | **nothing moves the token.** Every mechanism charges the same substrate price (the confusion penalty; on a host-layer mechanism the host cursor is cleared). The interrupt is read as a failure verdict *at the place the token is on*, and that place's failure-matrix row decides the next place. So the fall-back depends on where it was, not on which mechanism hit it. A dwell-only tactic feels the disruption as time only and routes on its base proportions (chapter 4's sentence). The layer shows underneath: after a host-layer mechanism every verb that acts on the current host is refused (`PRECONDITION_UNMET`) until an enumerate or scan host succeeds | `src/mtdsim/l3_simulation/movement/attacker.py` `_read_interrupt`, `_pay_interrupt_cost`; `apply_mtd_interrupt_cost` (shared by both arms) |

Chapter 3 already carries the baseline's rule as prose (l.~811: network layer
→ scanning hosts, application layer → scanning ports); §8g adds that it is
measured in the defended corpus (landing shares in `numbers.json` §s522).

**The story in the reader's terms, two steps.** (1) What a disruption does to
the attacker: it loses its foothold, and the time to win one back is
measurable. (2) What the attacker does about it: the baseline restarts a
script; the movement attacker keeps walking the same campaign, falls back at
most a stage, and re-finds a host. It never gives up: the cost capability sits
at its inert setting (chapter 4 / §5.1 fact, one body sentence).

**Takeaways (RATIFIED 2026-09-22).**

| # | Takeaway | Carried by |
|---|---|---|
| T5 | A disruption costs the attacker its foothold, and it wins one back within a measurable time that depends on the layer hit | figure, recovery panel |
| T6 | The movement attacker is not thrown back to a state. It stays in its campaign, its actions are refused, and it re-finds a host. The baseline attacker restarts its script from scanning hosts | figure, position panel, plus one body sentence for the baseline (its rule is chapter 3's; its landing share is the measured clause) |
| T7 | The response does not depend on whether the attacker reads its outcomes | the control, in the figure only if the tactic-level read shows a signature; otherwise one sentence |
| T8 | Hand-off: the defence's effect lands on position and pace, not on route, so §5.3 reads it on hosts reached | one closing sentence |

Property 4's honest form after this read is stronger than the fidelity
table's "built and run, not shown to change an outcome": on the tactic-level
instrument too, whatever the numbers say, the register stays *observation*.

**Figure design (`fig_5-2-2a_disruption_response`, replaces the adaptivity
figure; label `fig:aio-adaptivity` kept so every `\ref` stands).** Movement
attacker only, pooled over the four profiles, at 200 s (the interval with
the clean placebo; the 2 000 s read in the record and one sentence).

- **Panel (a), the position (T6).** Where the token sits by lifecycle stage
  (chapter 4's four: preparation, intrusion, post-intrusion, objective) at
  each visit from five before to five after each disruption. One series set,
  because the layer does not decide the fall-back; the per-layer read is in
  the record and, if the shapes agree, one sentence. The refused-action share
  by the same offsets is the second reading of the same panel (the "actions
  bounce" signal), drawn if the preview shows it and otherwise a sentence.
- **Panel (b), the recovery (T5).** Time from a disruption to the next host
  compromise, per layer hit (host / service / credentials), both attackers on
  the one measure, the censored share printed beside each value (Table 5.3's
  form: a conditional mean with its no-event share stated).
- **Leaves the figure:** the interval axis (one sentence); the verb-level mix
  (one sentence + chapter 6); the control unless it shows a signature.
- **The control's name at the head of the subsection** (owed, §3): an
  attacker whose routing stays on the base proportions whatever its actions
  return. "Outcome-blind" and "verdict-blind" do not reach the page.

**Instrument facts a drafter needs.** The records carry no host identity, so
position is measured as the stage the token sits on and recovery as the time
to the next compromise, never as a return to a named host. The defended
corpus records do not carry the interrupting mechanism per record; the layer
is the run's condition (single-mechanism conditions only; the two schemes are
mixed and are not pooled by layer). Every read is on the existing 100-seed
corpus; the thousand-seed rerun is owed with the rest of the chapter.

**Analyser and generator.** `data/results/ch5_defended/analyse.py` §s522
(stage and tactic by offset, refused share by offset, recovery to next
success and to next compromise with censoring, whole-run tactic distribution
against no defence, the placebo at stage level, the control at stage level,
the baseline's landing shares and phase mix); `tools/ch5_disruption_figure.py`
draws from it. Findings: `ch5_s532_adaptivity_findings.md` gains the §5.2.2
read as a dated addendum (the §s532 numbers stand as the verb-level record).

**Method.** Scrutinise-figure: takeaways first (this section), then a fresh
cold reader and the context critic on the redraw, until neither reports a
blocking defect.

#### 8g, the run and the pass (2026-09-22, same day; figure APPLIED as `fig_5-2-2a_disruption_response`)

**The preliminary read amended the panel definitions above**, on the data
(record: `ch5_s522_disruption_findings.md`):

- *Position by stage is flat* under every layer and both intervals (JSD ≤
  0.004; the token never falls back a stage; what moves at 2 000 s moves
  forward and is drift). So the stage panel is a sentence, and **panel (a) is
  the response as the share of steps whose action fails its precondition**,
  five steps either side of a disruption, per layer. Under a host-layer
  mechanism it rises from about 0.2 to 0.57 at the next step and decays to
  0.46 by the fifth; under a service-layer mechanism it does not move (the
  host is kept). The first failure is construction; the jump's size and its
  decay are measured, and the control decays identically.
- *Drawn at 2 000 s, not 200 s.* At 200 s the median spacing between
  disruptions is 7 steps, inside the ±5 window, so the share sits at about
  one half throughout (the same shape on a raised floor). The design text
  above said "200 s with the clean placebo"; that placebo was the stage read's,
  and the failure-share read needs none against a 30-point jump. Overturned
  on the data.
- *Panel (b)* as designed (time to the next compromise per layer, both
  attackers, censored share printed) **plus the pace anchor**: each
  attacker's mean gap between compromises with no defence as a dashed line in
  its colour (1 291 s movement, 394 s baseline). Without it the panel invites
  "simply worse" (both cold readers said so); with it the ordering inverts
  between attackers (host hits the movement attacker hardest, 1.6× its gap;
  service hits the baseline hardest, 1.5×). The anchor is a pace reference,
  not a null; the body quotes ratios as ordering, never bar minus line.
- *Not drawn:* the interval axis; the control (within 0.025 at every step on
  both spanning mechanisms, inside the recovery intervals; T7 is a sentence);
  the credential mechanism (0.1 disruptions per run at 2 000 s); the
  verb-level mix (a sentence here, a chapter 6 limitation).

**Reviewers.** Round one: a cold reader (PNG, caption, one body sentence) and
the context critic. The cold reader's one-sentence message was T5 and T6
without being told them. Named fixes, all applied: "visits" → "steps" (no
antecedent; Figure 5.1's unit); the key's "attacker model" → "movement
attacker" (registry row 1; the shared map in `tools/_ch5_style.py` is left
for Marc's ruling, its blast radius being Figures 5.4, 5.6 and the efficiency
table); a dashed swatch in each attacker's colour; the printed percentages
named in the key; one caption clause on why only 2 000 s is drawn;
"credentials" per Table 2.1; the two y-labels set on two lines. Round two: a
fresh cold reader and the critic re-verifying from the render, the built
figure tex and `numbers.json`. Both panels pass; the caption phrase "the
conditions that deploy one mechanism of the layer alone" ruled close enough
to Table 5.1's "alone". Panel (a) then redrawn in greys so the accent means
the movement attacker only (the second cold reader read blue in (a) as the
attacker). Rejected: plotting the ratio to the anchor (T5 promises a time; a
ratio hides censoring); intervals on panel (a) (pooled over 9 564
disruptions; a content point instead).

**Content points for the body text** are §7 of the findings record (16
items: the instrument and its construction half, the flat service line and
why the panels do not disagree, the before-level difference between layers,
the stage sentence, the baseline's landing shares bridged to chapter 3's
layer names, the control, the 200 s sentence, credentials, the ratios, the
inversion as an observation, censoring as the stopping rule's, the recovery
spanning a further disruption, the verb-level null, the pooling range, the
hand-off).

#### 8g, third round (2026-09-22, Marc's `/scrutinise-figure figure 5.2` on the merged figure)

**Marc's read, checked.** (i) "Service-layer mechanisms don't do much, host-layer
mechanisms disrupt a lot": upheld for the movement attacker on every measure
(failure share flat under the service layer; hosts reached 8.05 against 8.13
with no defence, host layer 6.36). (ii) "Make the disruption clearer in (a)":
the disruption's own step is now a shaded slot between the two windows
(`--band`); the critic rules it a decode, not accentuation. (iii) "Panel (b) is
dominated by the movement attacker being slower; not a fair comparison; the
service layer disrupts the baseline more, the host layer the movement
attacker more": the first half upheld (three cold readers took "slower" from
the absolute form). The second half is **one condition, not the layer**,
verified per condition at 2 000 s: the baseline's service-layer recovery is
service diversity alone (952 s, 2.42× its no-defence gap, 18 % censored),
while port shuffle and OS diversity leave it at pace (370 and 378 s, 0.94×
and 0.96×, against 394 s). Its host-layer conditions sit at 398–442 s
(1.01–1.12×). The movement attacker's half holds in every condition: host
1 970–2 221 s (1.53–1.72×) above service 1 490–1 611 s (1.15–1.25×), IP
shuffle the harshest. So "the service layer disrupts the baseline more" may
not be said as a layer statement; "service diversity does" may.

**Reviewers, and where they disagree.** A fresh cold reader on the ratio
candidate took the inversion in one sentence (the form communicates T5's
layer dependence). The sceptical examiner (numbers from the run cache): the
movement-side inversion survives means, medians and a censoring-aware
(Kaplan–Meier) estimator (KM medians 1 790 against 1 377 s); the baseline
side survives the mean only and is service diversity; the censored shares are
the time limit's on the movement side (every censored host-layer recovery is
in a run cut at 15 000 s) and the stopping rule's on the baseline side (0.66
and 0.49 of its defended runs reach the target, not the 0.6 quoted in the
findings); the pace anchor is defensible (a random-time null moves the ratios
by at most 0.2 and the inversion stands); a movement recovery after a
host-layer disruption spans a further disruption in about a third of cases,
which raises its mean but not its KM median. **Examiner's ruling: absolute
form plus a mark at each mechanism's own mean on every bar; no ratio.**
Reason: the ratio turns an ordering into a magnitude that moves under the
estimator (1.59× on means, 2.01× on KM). **Context critic's ruling, reversed
from round one: take the ratio.** Reason: the absolute form delivered T4
again to three readers; §3 rule 1 asks for magnitude as a relative figure;
censoring is still printed; the four absolute times fit one body sentence.
One named fix on the ratio: the interval must be a bootstrap on the ratio
(Figure 5.4's house form), not the recovery's interval divided by the anchor.

**Candidates rendered** (`data/results/ch5_defended/candidate_fig522_A_relative_marks.png`,
`candidate_fig522_B_split_absolute.png`), both with the shaded disruption
slot and the per-mechanism marks:
- **A** ratio to the attacker's own no-defence gap, one panel, dashed line at
  one; the marks show the baseline's service bar as 0.94 / 0.96 / 2.42.
- **B** absolute seconds, one panel per attacker on its own scale, each with
  its own pace line; the cross-attacker height is removed by layout.

**Session recommendation: A**, with the bootstrap interval on the ratio, the
estimator sentence and the four absolute times in the body, and the
service-diversity narrowing stated as the observation. B keeps the seconds
but hides the SQ3 contrast behind two scales and crowds the figure.
**RULED 2026-09-22 (Marc): A.** "A is definitely more clear"; the black
per-mechanism bars "are not particularly clear, I am not getting much out of
those", so they are redrawn as small hollow circles at each mechanism's ratio
(dropped if the fourth round finds them still mute); the rest of A stands.
Marc also confirmed the register: the results describe the shape of the data,
observations included; the reason is chapter 6's. Applied: the generator's
default is the ratio form with the shaded disruption step and the circles
(`--absolute` restores the first form); the analyser gains the bootstrap on
the ratio (both pools resampled by run, seeded); caption rewritten (DRAFT
STATE); a fourth review round on the applied figure is recorded below.

#### 8g, fourth round (2026-09-22, on the applied ratio form; no blocking defect)

- **Cold reader (fresh; PNG, caption, one body sentence):** message in one
  sentence was T5, T6 and the inversion *with* its single-mechanism
  narrowing ("slowed by service ones, though mostly by a single mechanism"),
  read off the circles unprompted. So the circles do the job the black bars
  did not. Non-blocking, folded into the findings' content points (§7 item
  19): the circles are anonymous (the body names them); the pooled bar is not
  the mean of its circles (caption now says "pooled the same way"); the
  bootstrap interval is the pooled mean's, the circles carry the spread; one
  is "at its own pace", not "no effect"; the movement attacker's censored
  shares are mostly the time limit's floor on a slow attacker.
- **Context critic (fourth pass, from the built figure tex and §s522):**
  every whisker back-converts to the bootstrap bounds to three places; the
  caption says what it must and states no result; the circles decode, breach
  nothing, and are what stop the figure asserting a layer fact for the
  baseline (0.94 / 0.96 / 2.42); the y-label passes ("÷" is a taste call for
  Marc; Figure 5.4 says "relative to" in words). One named fix, applied: the
  circles sat on the neighbouring bar's edge; each set is now on its own bar,
  the bars slightly widened. Body obligation restated: for the baseline
  attacker say "service diversity", never "the service layer"; the movement
  attacker's host-layer result is uniform across its three mechanisms, IP
  shuffle largest.
- **Applied state:** `fig_5-2-2a_disruption_response` in the ratio form,
  `tools/ch5_disruption_figure.py` default (`--absolute`, `--no-band`,
  `--no-marks`, `--split` restore the other forms for the record); caption
  DRAFT STATE; build clean at 88 pages. Candidates A and B remain as PNGs in
  `data/results/ch5_defended/`.

**Rulings 2026-09-22 (Marc), after the fourth round.** (0) "÷" stays. (1) The
shared key map is fixed: `_ch5_style.py` LABEL["movement"] = "movement
attacker"; Figures 5.4 (`fig_5-3-2a_cross_arm`) and 5.6 (`fig_5-4a_frontier`)
and Table 5.8 (`tab_5-4a_cost`) regenerated. Found on the way, fixed as a
mechanism: the grouped-panel key in `ch5_effectiveness_figures.py` spaced
entries at 0.115 cm per character and overlapped "baseline attacker" with the
next swatch in the committed figure too; now 0.165. Found, not fixed, not
this session's: `fig_5-4a_frontier` was 16.1 cm wide before and after (the
panel (b) label column), over the 15.7 cm pack. (2) The control's declaration
is drafted at the head of §5.2.2 with the two other head slots (why the
property needs defence; the layers and the interval read), DRAFT STATE,
ratify on read. (3) The 200 s and 60 000 s reads: Marc will settle later.
Marc's closing read of the figure: it conveys that a disruption occurs and
that the response to it differs by model.

**Still open for Marc:**
against the registry (three other floats); (2) the control's declaration at
the head of §5.2.2 (owed, §3); (3) whether the 60 000 s and 200 s reads enter
as sentences (Table 5.1 declares 15 000 s and the two intervals only).

### 8h. §5.3.1 Defence mechanisms and execution schemes — takeaways (2026-09-22; RATIFIED by Marc the same day, then the full scrutinise-figure pass: three rounds, no blocking defect; record in 8h-2 below)

Marc's ask: scope to §5.3.1, define what the reader must leave with before
the floats (`fig:eff-suppression-profiles`, `tab:eff-conditions`) are tested,
check his read against the corpus, formalise the whisker, and say why Table
5.4's footnote is so long. Numbers below are the 100-seed corpus
(`numbers.json` §s541); every value is provenance, never a chapter value.

**What the reader holds when §5.3.1 opens** (chapters 2 to 4, §5.1, §5.2, and
nothing else): seven defence mechanisms, grouped by what each rewrites — three
the host layer (IP shuffle, complete topology shuffle, host topology shuffle),
three the service layer (port shuffle, OS diversity, service diversity), one
the credentials (user shuffle) (Table 2.4, Figure 2.3); four execution
schemes of which two are run, random (one mechanism drawn from the pool per
interval) and alternative (the pool in a fixed rotation, one per interval)
(Table 2.5); two deployment intervals and the time limit (Table 5.1); suppression
as $1 - \bar H_{\mathrm{defence}} / \bar H_{\mathrm{no\ defence}}$ on hosts
reached (Table 5.2); the no-defence reference, 8.1 hosts pooled (Table 5.3);
and §5.2.2's hand-off (T8): a disruption lands on position and pace, not on
route, so the defence is read on hosts reached. The §5.3 head still owes
(§3): the pooling of the four profiles, and what counts as a separation.

**The subsection's question** (§3): which defence conditions reduce what the
movement attacker reaches, and does the answer depend on the profile. Not
yet: whether the baseline attacker agrees (§5.3.2).

**Takeaways (PROPOSED; the pass criterion once Marc agrees).**

| # | Takeaway | Carried by | Could it have come out otherwise? |
|---|---|---|---|
| T9 | Which defences reach the movement attacker is decided by the layer the mechanism rewrites. At 200 s the three host-layer mechanisms remove nearly all of its hosts reached and are one effect; the three service-layer mechanisms remove little; the credentials mechanism removes none | Fig. 5.3(a); Table 5.4's suppression column and dagger for the tier boundaries | Yes: the ordering is measured, and the baseline attacker returns a different one (§5.3.2) |
| T9′ | Where the host-layer effect shows in the other metrics: the attacker is denied its first host in most runs, its first compromise comes later where it comes at all, and most of its actions are refused; under the service layer all three stay at the no-defence level | Table 5.4, the four columns the figure does not carry | Yes |
| T10 | The tiers are the same on every profile at 200 s (Marc: "they all move very similarly, with some variation"). Inside a tier the magnitude differs by profile, and on the schemes and the host layer the difference is separated (amended 2026-09-22 on the examiner's check, 8h-2) | Fig. 5.3, the five bars per condition (the reason the figure is drawn per profile); one body sentence with the spread, conditioned on 200 s | Yes: §5.2 showed the profiles walk different campaigns |
| T11 | A scheme over the pool does less than the best mechanism in it: random and alternative sit between the host-layer tier and the service-layer tier | Fig. 5.3(b); Table 5.4 | Yes. By-construction sentence allowed (§3 rule 2): a scheme fires one mechanism per interval and three of the seven are host-layer (Table 2.5) |
| T12 | At the longer interval every effect attenuates; the host layer and, narrowly, the random scheme stay separated from zero (amended 2026-09-22: random 0.09 [0.02, 0.15]); the 200 s ordering is a property of the deployment interval | Table 5.4 lower block (the carrier: per profile only IP shuffle is separated on every series); Fig. 5.3(c), (d) | Yes. By-construction sentence allowed: eight deployments against seventy-five inside the time limit (Table 5.1) |
| T13 | Exception, marked and not explained (§3 rule 3): user shuffle is negative at 200 s on the pooled cell | Table 5.4 (the pooled row is the separated one; the figure shows direction only, see below) | Attribution open; trace owed (findings §1 item 2) |
| T14 | Hand-off: this pooled ordering is what §5.3.2 reads the baseline attacker against | one closing sentence | — |

Not a takeaway: "the defence is really strong". Strength belongs to one tier
at one interval; the figure's message is *which layer*, not *how much*.

**Marc's read, checked against the corpus.**

| Marc's point | Checked | Verdict |
|---|---|---|
| At 200 s IP, topology and host are very strong | 0.96, 0.96, 0.96 pooled; per profile 0.93–0.98; intervals overlap each other and nothing else; 75 of 75 deployments interrupt in every profile | Upheld. One effect, the host-layer tier |
| Port, user, OS and service not as strong | service 0.36 [0.31, 0.41], port 0.20 [0.13, 0.26], OS 0.07 [0.00, 0.14], user −0.14 | Upheld, with a tier inside it: service and port are separated from zero, OS touches it |
| User shuffle is negative, helping the attacker | pooled −0.14 [−0.22, −0.05], 9.23 hosts against 8.13. Per profile: $c_1$ −0.13 [−0.27, −0.01] excludes zero; $c_2$, $c_3$, $c_4$, $c_{\mathrm{agg}}$ include it | Upheld on the pooled cell only. The figure, drawn per profile, does not show a separated negative on four of its five series; the table does. "Helping" is chapter 6's word until the trace lands |
| The schemes are just an average of the pool | The seven singles average 4.22 hosts, suppression 0.48; random is 0.75 and alternative 0.72 at 200 s. At 2 000 s the average is 0.09; random 0.09, alternative 0.03 | Not upheld at 200 s: a scheme does more than the pool's mean and less than its best member. Upheld at 2 000 s. The prose may say only the by-construction fact (T11) |
| Confusion is not modelled, so a scheme cannot compound | §4.4.1 declares one confusion penalty per disruption, charged whatever mechanism fired (§8g mechanism fact) | Half upheld: the penalty exists and is flat; what does not exist is any interaction between mechanisms in a scheme, so a scheme is a mixture of single effects by construction. Chapter 7's sentence, not §5.3.1's |
| At 2 000 s everything is less because the attacker has more room | only IP shuffle (0.33) and the topology shuffles (0.16–0.17) separated from zero; every other interval includes zero; eight conditions overlap a neighbour | Attenuation upheld (T12). "Room to breathe" is interpretation; the admissible sentence is the deployment count |
| Table 5.4 presents the values from above | the figure is per profile, the table pooled: the pooled suppression appears nowhere in the figure, and four of the table's columns are in no figure | Partly: the table is where the pooled number, its interval and the other channels live (T9′, T13) |

Found beyond Marc's list, from the float and the generator:

- **The figure caption misdescribes the schemes**: "the schemes that deploy
  several together" is *simultaneous* (Table 2.5), which was not run. Random
  and alternative deploy one mechanism per interval from the pool.
- **The x-axis short names** "topology" and "host" stand for complete topology
  shuffle and host topology shuffle; a cold reader can read "host" as a host
  shuffle. Candidate fix: "compl. top." / "host top.", or the layer as a
  bracket over the three.
- **Layer vocabulary is split.** Chapter 2 and the §5.2.2 design say host
  layer / service layer / credentials; the findings record and Table 5.5's
  footnote say network layer / application layer. The antecedent rule wants
  chapter 2's words in §5.3.1; Table 5.5 is out of this pass's scope and is
  flagged.
- **Both captions carry an "intention" sentence**, which §8b moved to the body
  text.
- **Table 5.4's caption says "three channels"** and the table has six metric
  columns; the frame is interpretive and is chapter 6's.
- **Profile dependence at 2 000 s**: the spread widens (IP shuffle 0.20–0.47,
  alternative −0.11 to 0.16) with the intervals; no separated pair inverts. T10
  holds at both intervals but the sentence must say "at this seed count".

**Why Table 5.4's footnote is long, and what it may lose.** It defines target
reached, suppression, the delay's censoring and the blocked fraction — all
four are Table 5.2's definitions — plus the ordering rule and the dagger. The
ruling on Table 5.3 (§8e: no footnotes, the caption says how to read and
points at Tables 5.1 and 5.2) applies unchanged. Recommendation: the caption
points at Table 5.2 for the metrics and keeps two facts Table 5.2 cannot
carry, the ordering (by suppression within each interval; the no-defence
reference one cell read against both) and the dagger's decode. The delay's
conditioning ("over the runs that compromise one") is already Table 5.2's
definition. Footnote goes from six clauses to the dagger, or to nothing if the
dagger moves into the caption.

**The whisker, formalised (from `analyse.py` `suppression`).** Let
$H_{0,1},\dots,H_{0,n_0}$ be hosts reached in the $n_0$ no-defence runs and
$H_{d,1},\dots,H_{d,n_d}$ in the $n_d$ runs under condition $d$; pooled over
the four profiles $n_0 = n_d = 4 \times$ the seed count. The point estimate is
$\hat S_d = 1 - \bar H_d / \bar H_0$. For $b = 1,\dots,B$ with $B = 2\,000$,
draw $n_0$ runs with replacement from the no-defence cell and $n_d$ from the
defended cell, independently, and compute $\hat S_d^{(b)}$ on the two
resampled means. The whisker is the percentile interval
$[\,Q_{0.025}(\hat S_d^{(1..B)}),\ Q_{0.975}(\hat S_d^{(1..B)})\,]$, seeded so it
reproduces. Two properties the prose may state: it is an interval on a ratio
of means, so it is asymmetric and can cross zero (user shuffle); and it is
unpaired although the cells share seeds (§5.1 "the same seeds"), so it is the
wider of the two intervals the design permits. A paired form (resample seeds,
compute both means on the same draw) is a session choice, not a bug; it would
narrow every whisker and change no ordering unless Marc asks for it. Table
5.4's $\pm$ on hosts reached, delay and blocked fraction is the suite's mean
interval (`_iv`: $1.96\,s/\sqrt{n}$, the normal approximation on the sample standard deviation), a different estimator; the caption should not call both
"intervals" without saying so.

**Rulings taken (Marc, 2026-09-22, second turn):** T9–T14 ratified as the
pass criterion; "really strong" was a reading of the diagram, not a claim;
the average-of-pool correction accepted ("the three big ones and the four
small ones come out to a medium value"); the confusion note accepted
(simultaneous is not run); the footnote: "move it into the caption or remove
it"; the whisker: asked for the convention, not "a bar and then a bunch of
text". The layer words and the paired bootstrap were left to the pass
(8h-2).

### 8h-2. The pass (2026-09-22): three rounds, what was accepted, what was rejected, what was applied, what is still Marc's

**Round one, five reviewers launched together** (cold reader on the two
renders only; context critic against this file; numbers auditor from
`summaries.pkl` and `runs.jsonl`; convention reader against
`figure_table_conventions.md` and the anatomies; sceptical examiner on T9).
Every finding below was checked against `numbers.json` before it was
accepted; the numeric additions are in the findings record §5.

| Finding | Source | Checked | Verdict |
|---|---|---|---|
| Caption says the schemes "deploy several together" | critic | Table 2.5: random draws one per interval, alternative rotates one per interval; "several together" is simultaneous, not run | Accepted, fixed |
| Ticks "topology" / "host" ambiguous between the two topology shuffles | cold reader, critic, conventions | the cold reader guessed and said so; corpus form is a decoded key (Brown) | Accepted: two-line full short names on the ticks |
| $c_{\mathrm{agg}}$ read as the pooled row | cold reader (rounds 1 and 2) | aggregate IP shuffle 0.95 against pooled 0.96 at 200 s, 0.20 against 0.33 at 2 000 s; the aggregate has its own 100-run cell and is not in the 400 | Accepted: figure caption declares it a fifth series outside the pooled cell; table caption pools by code |
| T12 "only the host layer" false | critic, examiner | random 0.09 [0.02, 0.15] at 2 000 s | Accepted, T12 amended |
| T10 magnitudes differ by profile, separated | examiner | IP shuffle $c_1$ 0.93 [0.90, 0.95] vs $c_4$ 0.98 [0.97, 0.99]; random $c_3$ 0.81 [0.76, 0.86] vs $c_1$ 0.69 [0.64, 0.74] | Accepted, T10 amended (tiers same, magnitude varies) |
| "Removes nearly all" is the dose, not the layer | examiner | 85–89 % of host-layer compromises land 100–200 s after the last interrupt; the order holds at both intervals, the size does not | Accepted as a ceiling: T9 stays conditioned on 200 s; the mechanism reading is chapter 6's |
| Bare "schemes" in the (b)/(d) titles | critic (round 2) | §5 Never list | Accepted: "execution schemes"; the interval is the row's, carried by (a)/(c) |
| Footnote restates four Table 5.2 definitions | Marc, critic, conventions | corpus footnotes carry provenance or a mark decode only | Accepted: footnote removed; ordering rule, one-cell reference and dagger decode in the caption |
| Two estimators in one row, undeclared | critic, conventions | brackets are the percentile bootstrap, $\pm$ is $1.96\,s/\sqrt n$ | Accepted: one caption clause decodes both |
| Dagger does not say which neighbour | cold reader | generator flagged both members of each pair | Accepted: the mark sits on the upper row, "overlaps the row below's" |
| Chart-text formula line under the panels | Marc, conventions | no antecedent in ten anatomies; Table 5.2 holds the formula | Accepted: line removed |
| "Intention" sentences in both captions | critic, conventions §l | §8b ruling; a caption decodes | Accepted: removed; the content goes to the body slots |
| Table at scriptsize with 3 pt colsep; two wrapped cells | conventions | §k1: 8 pt only with 4 pt together | Accepted: 4 pt, widths 3.5 / 2.8 / 5 × 1.48 cm = 452.5 pt of 455.2; no wrap |
| Hyphen for minus inside the bracket bounds | critic (round 3) | text-mode bounds | Accepted: math mode |
| Layer words: chapter 2's host / service / credentials, not network / application | critic | Table 2.4's column is what T9 is about; §2.2.3's network/application is the attacker's landing rule | Accepted for §5.3.1's body; neither float uses a layer word. Table 5.5's footnote flagged, its own pass |
| Grey the 2 000 s rows | cold reader | §k3: shading is a reading aid, never an encoding | Rejected |
| y floor to −0.5 | cold reader | nothing clipped: lo min −0.381 (auditor) | Rejected |
| Intervals on the share columns | cold reader | Table 5.3 precedent (§8e) | Rejected, same reason |
| "Target reached" undefined for pooled profiles | cold reader (round 1) | every profile pursues the one targeted objective (Table 5.1); the confusion came from the prompt's context sentence | Rejected |
| Five bars per condition are clutter | author's doubt | the five carry T10 and the separated $c_3$ scheme bump | Rejected by the critic; kept per profile |
| Pool composition has no antecedent | examiner | §5.1 says the schemes "draw on the whole pool"; Table 2.5 | Rejected as a breach; T11's clause cites both |

**Rounds two and three.** Fresh cold reader and critic each time. Round two:
both one-sentence messages matched T9, T11 and T12; two blocking items (the
aggregate; bare "schemes"), fixed. Round three: nothing blocking from either;
the cold reader's message was T9 + T11 + T12 and it read the aggregate, the
panels and every dagger pair correctly.

**Final float definitions.**
- *Figure 5.3* (`tools/ch5_effectiveness_figures.py --only fig55`): 2 × 2,
  (a)/(c) the seven mechanisms in Table 2.4's row order at 200 s / 2 000 s,
  (b)/(d) random and alternative; series the four profiles by code and the
  aggregate; bars suppression of hosts reached, whiskers the percentile
  bootstrap; two-line tick names; key of the five series only; 15.1 × 9.5 cm.
  Caption decode-only; DRAFT STATE.
- *Table 5.4* (`--only tab55`): the pooled cell ($c_1$ to $c_4$, 400 runs at
  100 seeds), six Table 5.2 effectiveness columns, ordered by suppression
  within each interval, the no-defence reference once; dagger on the upper
  row of an unseparated adjacent pair; no footnote; scriptsize with 4 pt
  colsep. Caption decode-only; DRAFT STATE.
- `grouped_panels` is shared with Figure 5.6: the two-line ticks and the
  (b)/(d) titles reach it on its next regeneration (its own pass).

**Units and fairness, as argued.** Pooled 400 against a pooled 400 no-defence
cell; per profile 100 against 100; every cell on seeds 0–99 and the same
network per seed; the no-defence cell reads no interval or timing draw and
is one cell read against both intervals (fair to both: examiner). The stop at
the target moves suppression ≤ 0.02 at 200 s. Schemes over the seven against
singles: same reference, same axis; the pool composition (three of seven
firings on the host layer, measured) is the by-construction clause T11 owes.

**The whisker, settled.** The formal statement stands in 8h. The convention
question Marc asked: the corpus reports no confidence interval at all (every
anatomy records the absence), so there is no figure-level convention to copy;
the one model the conventions file nominates is a setup-paragraph declaration
(§d). Recommendation: §5.1's Runs unit names both estimators once ("percentile
bootstrap intervals, resampling runs within each cell, for ratios; a normal
interval on the mean elsewhere"), after which the captions say "95 %
intervals (Section 5.1)". Until Marc dictates that sentence the captions
carry the one-clause decode. Unpaired kept: the seed pairing holds only until
the first deployment (every mechanism draws from the one global RNG; seed
correlation 0.19–0.24 under the host layer, 0.59–0.81 under the service
layer), pairing narrows the weak-defence whiskers by 25–45 % and moves no
ordering (findings §5).

**Content points the body text owes** (content, not prose; §3's shape):
1. §5.3 head slots (§6): the four profiles pooled, the aggregate its own
   series outside the pool; a separation is two 95 % intervals that do not
   overlap, read on adjacent conditions only; the layer word is Table 2.4's
   (host layer, service layer, credentials).
2. T9, conditioned on the interval: at 200 s the host layer, one effect
   (three intervals overlapping each other and nothing else; the "one
   effect" floor is open, below); the service layer separated from zero on
   service diversity and port shuffle, OS diversity touching it; user shuffle
   below zero.
3. T9′ from the table: denied its first host in 71–76 % of runs, first
   compromise three times later where it comes, blocked fraction 0.24 →
   0.80–0.83; the service layer at the no-defence level on all three.
4. T10 at 200 s: the tiers on every profile; the spread inside a tier
   (≤ 0.06 on the singles but service diversity 0.10; schemes 0.13–0.18,
   $c_3$ highest); at 2 000 s the spread widens with the intervals and no
   separated pair inverts the condition order.
5. T11 with its by-construction clause: a scheme fires one mechanism per
   interval from the whole pool (§5.1, Table 2.5), three of the seven
   host-layer.
6. T12 with its clause: eight deployments against seventy-five inside the
   time limit; the host layer and random separated from zero; every other
   interval includes zero and the chain of daggers runs to the last row.
7. T13 marked, not explained; the attribution waits on the trace
   (findings §5 names what it must show).
8. T14: this pooled ordering is what §5.3.2 reads the baseline attacker
   against.
9. The owed Appendix C sentence (tex comment at the §5.1 site, l. 5372:
   the 200 s suppression's exposure to the low-and-slow dwell band) lands
   beside point 2.

**Chapter 6 ceilings** (not for chapter 5): the 200 s magnitude is the dose
and the layer is the ordering (findings §5, saturation); magnitudes are not
converged at 15 000 s; profile independence on the service layer is absence
of evidence at this seed count; the schemes are a mixture of single effects
by construction (no interaction is modelled: one flat confusion penalty per
disruption); user shuffle's two read paths.

**Rulings still Marc's:**
1. **Layer group labels under the ticks** (one grey label per Table 2.4
   group beneath (c)'s ticks: host layer, service layer, credentials). A
   decode, not an accentuation; it would let the figure carry T9's word.
   Recommendation: yes.
2. **Paired bootstrap:** recommendation no, for the reason above.
3. **The §5.1 Runs sentence** naming the two estimators: his dictation;
   slot content above.
4. **An effect floor for "one effect"** before the thousand-seed run: the
   host-layer trio differs by 0.004–0.006 and will likely separate at 1 000
   seeds on the overlap test alone. Recommendation: declare 0.05 suppression
   as the smallest difference the chapter reads, in the §5.3 head with the
   separation rule.
5. **The profile-hue contract** is unrecorded in conventions §i (five hues
   against "greys + one accent"); Figure 5.1 already uses it by acceptance.
   One line in §i closes it.
6. **Table 5.5's network / application words** → Table 2.4's, in its pass.
7. **The (b)/(d) titles carry no interval** (width); the round-three cold
   reader inferred it from the row and called it minor.
8. **"at this seed count"** in the dagger decode: kept for consistency with
   Table 5.5; cut if he hears it as a hedge.

**Validation.** Build clean, 88 pages, 0 errors; no overfull box at either
float (the log's nearest are Appendix B tables and Figure 5.5); auditor 243
of 243 table values and 90 of 90 bars reproduced. Numbers are the 100-seed
corpus throughout; the thousand-seed rerun is owed with the chapter.


### 8h-3. Rulings on 8h-2 and the one-page fit (Marc, 2026-09-22, third turn; APPLIED)

- **Layer brackets under the ticks: yes** ("brackets: host, host, host,
  credentials, the what-it-moves from the table"). Applied: the singles
  panel's x order is now grouped by the layer each mechanism rewrites (host
  layer: IP, complete topology, host topology; service layer: port, OS,
  service; credentials: user), Table 2.4's column rather than its row order,
  with one grey bracket and label per group; the caption says "grouped by the
  layer each rewrites". `grouped_panels` is shared, so Figure 5.6 was
  regenerated with the same ticks, titles and brackets (its caption is not
  yet scrutinised; FLOATS.md says so).
- **Profile hues kept** ("the colour is good in terms of separating the
  meaning of each profile"). The contract is now recorded in
  `figure_table_conventions.md` §i as a scoped exception to one-accent.
- **Table 5.5's words standardised** to Table 2.4's: host-layer against
  service-layer mechanisms in caption and footnote, user shuffle named the
  credentials mechanism. Regenerated.
- **Figure 5.3 and Table 5.4 on one page, as §5.2.1's floats are.** Measured
  against the 24.7 cm text height: the pair needed 1.5 cm less. Taken from
  the figure's internal spacing (panel height 3.4 → 2.4 cm, row gap 0.8 →
  0.6, key offset) and from the two captions (the figure's shortened by half
  a line; the table's dagger clause deleted on Marc's word: "cut out the
  clauses that don't matter, the footnote one you can just delete"). The
  daggers went with the clause, since an undecoded mark is a §b2 breach and
  the printed intervals carry the overlap; the body text names the separated
  pairs from `numbers.json` `overlapping_adjacent`. Result: heading, figure
  and table on page 44, content ending 1.7 mm above the text-area floor;
  the thesis is 87 pages. The margin is thin: a caption that grows by a line
  pushes the table to the next page.
- **Still open from 8h-2:** the §5.1 Runs sentence naming the estimators
  (his dictation); the "one effect" floor before the thousand-seed run
  (recommend 0.05); the (b)/(d) titles carry no interval; "at this seed
  count" is gone from Table 5.4 with the dagger clause and stays in Table 5.5
  for its own pass. The paired bootstrap stays unpaired (8h-2's reason).

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
