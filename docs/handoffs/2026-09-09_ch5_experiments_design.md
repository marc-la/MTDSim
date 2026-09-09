---
status: open — design ratified and scaffolded; restructured 2026-09-09 second pass (§9); C1–C10 owed as drafting rulings
created: 2026-09-09
topic: "The Experiments chapter designed against the field's conventions rather than invented: a section-level survey of how MTD evaluations are built and reported (now docs/workflows/evaluation_conventions.md), the ch5 design that follows from it, the funnel that lets one run set both characterise the attacker and evaluate the defence, the property-to-measurement map the discussion's fidelity table depends on, and the five things the chapter cannot yet say."
---

# The Experiments chapter — design against the corpus

## What this is

Marc's ask (2026-09-09): get the experiments setup right the first time, and
get it right by looking at how the field does it rather than by inventing a
shape. Two outputs. The evidence layer is
[`../workflows/evaluation_conventions.md`](../workflows/evaluation_conventions.md)
— a durable conventions file distilled from a section-level anatomy of the
evaluation portion of every MTD-evaluation paper in the corpus, one paper per
pass, with page or line locators on every claim. This file is the design that
follows from it.

**Status, 2026-09-09.** Marc ratified the design in full and asked for it in the
tex. The scaffolding has landed: ch5 now carries its section and subsection tree
with a per-section comment block saying what the section does, what it should
look like against the named corpus convention, what it must carry from the
records, and which discussion section it feeds; ch6's three sections carry the
matching "fed by" wiring, including the property-by-property map for the
fidelity table's walk. Build clean, no undefined references. **No prose was
written** — comments and headings only, per the drafting pipeline, and the
headings are scaffolding for Marc to rename.

What remains open is C1–C8 below, which are now *drafting* rulings rather than
design ones, plus the blockers in §5.

## 1. The frame, already ruled — do not re-open

Recorded so a cold session does not re-litigate settled ground.

- **The chapter is one chapter.** Experimental setup and results merged into
  "Experiments", 12 units, on Marc's 2026-09-08 ruling. Discussion, future work
  and conclusion renumbered.
- **The model is a hypothesis, not a claim to justify.** No burden-of-proof
  unit, no grading unit, no fidelity-defence unit in this chapter. The fidelity
  verdict emerges from the results and is read in the discussion.
- **The movement attacker is the new baseline.** No separate prior-model
  comparison section; the inherited attacker is compared *inside* the strands.
- **Strands are clustered by instrumented metric family**, not by experiment
  family: effectiveness, efficiency, supplementary measures.
- **Facts and figures only.** Interpretation is the discussion's.

**The corpus ratifies all five.** A separate experimental-setup chapter is not
the field's form — the dominant pattern is one movement, declare then report
(conventions §a). Organising results by metric family is well attested and is
the right axis when the contribution is the attacker rather than a mechanism
(§b). Both were the right calls independent of the reasoning that produced them.

## 2. What the survey changes about the design

Four findings from the conventions file bear directly on ch5.

**(1) A titled sensitivity-analysis section is rare; the sweep is usually the
results.** Only one paper in the surveyed corpus has a section called
"Sensitivity analysis". Elsewhere the parameter sweep *is* the results section
(Hong's entire §6.2, Anderson's entire §IV, Carroll's entire §IV) or an
unlabelled axis inside it. §5.1 as a titled section is therefore an unusual
move — defensible, because V6 ruled the results preamble and because this
chapter's sweeps interrogate *ch4's* declared inputs rather than the
experiment's factors, but it is not free. It should read as *the model's inputs,
priced* rather than as a detached methods section, and one sentence should say
so.

**(2) Ranges are almost never justified; unswept parameters sometimes are.**
Hong, Anderson, Carroll, Zhang and Reti state no rationale for any range. Bland
says outright that its rates are "notional and currently have no relation to a
real computing system". What the better papers do instead is *name what they did
not sweep* and why. So bounds derived from the formalism's own structure put
this chapter ahead of the corpus, and that is worth one sentence — while the
genuinely load-bearing discipline is the register in §3 below.

**(3) Nobody in the lineage reports a confidence interval.** Brown states no run
count at all. Zhang and Reti report 100 runs. Means over repeated runs is the
local ceiling, so reporting effect sizes with intervals *exceeds* lineage
practice and should be claimed as a deliberate improvement rather than slipped
in.

**(4) The field already solves the double game, with a funnel.** See §4.

**(5) "How many runs" has a real answer, and it is not a round number.** The MTD
corpus does not address it — a hundred is simply what two papers happened to do.
The simulation-methodology literature gives three methods: a rule of thumb (three
to five, which exists only to say that one run is unwise), a graphical method
(plot the cumulative mean against the run count and read off where it flattens —
simple, subjective, no stated precision), and the **confidence interval with
specified precision** method, which asks what error you can tolerate in the
estimate and then runs until the interval is inside it. The third is the one to
use and to cite, and it is already what this project's own power arithmetic
does — it just has no citation attached. Declaring the tolerance turns the run
count from an assertion into a consequence.

The same literature settles what §5.1 *is*. Sargent's taxonomy names
parameter-variability sensitivity analysis as an **operational validation**
technique — determining that "the model's output behavior has sufficient
accuracy for the model's intended purpose over the domain of the model's
intended applicability". So the sensitivity section is not a robustness
appendix that happens to come first; it is the validation of a model whose
system is unobservable, and the same source states the ceiling that follows:
where the system is not observable "it is usually not possible to obtain a high
degree of confidence in the model", and the behaviour "should be explored as
thoroughly as possible". The modest claim this project already makes is the
discipline's own prescription, and can now be cited as such rather than argued
from first principles.

## 3. The design

Unit budget against the ruled 12. Tables and figures are outside the word
count, which is what makes the register affordable.

| § | Units | What it carries |
|---|---|---|
| opening (unnumbered) | ~0.5 from slack | what the chapter does with the attacker model |
| 5.1 preamble + register | 1 | the parameter register (table), the sweep frame, the swept/held rule |
| 5.1.1 dwell times | 0.75 | four anchors over their bands; the distribution family |
| 5.1.2 tactic-to-verb mapping | 0.5 | a swap, not a band — the one input with no interval |
| 5.1.3 failure matrix | 0.75 | the two decay parameters and the floor; the nine rules argued, not swept |
| 5.2 experimental dimensions | 2 | the factor table; metrics named as instrumentation; the comparability boundary; the discrimination gate; seeds, horizon, statistics |
| 5.3 effectiveness | 3 | unopposed → under defence → cross-arm |
| 5.4 efficiency | 1 | attacker cost and return on attack; the defender-side reconfiguration ledger; the frozen-defender concession |
| 5.5 supplementary measures | 2 | what the inherited suite cannot express; the ablation contrasts |

### 3.1 One register, not two — the recommendation that saves a unit

The formalism inventory carries a parameter register and, separately, a
twelve-item assumption register, and asks (its ruling R6) whether the second is
a ch5 unit or a ch4 closing paragraph. **Neither. Merge them.**

Every declared quantity gets one row, and each row says either *the band it was
swept over and what moved*, or *that it was held, and why*. An assumption is
simply a row whose sweep column reads "held", with the reason in a clause. One
table, both kinds of row, and no separate assumption list anywhere.

Three reasons this is the right shape:

- It is the discipline the corpus's better papers actually practise, stated as a
  rule instead of scattered (conventions §c). A parameter appearing in neither
  list is the omission the corpus keeps committing.
- It answers R6 without spending a unit the ledger does not have. Twelve
  assumption sentences is roughly one unit; as table rows it is nearly free.
- It makes the chapter's honesty structural rather than rhetorical. A reader can
  see the unswept rows without hunting for a concession paragraph.

The register belongs in §5.1's preamble, where V6 put the results-preamble
table.

### 3.1b Make §5.1 select something, not merely survive

The strongest sensitivity analyses in the corpus feed forward. Manadhata and
Wing's produces guidelines for choosing parameters, and their later values are
assigned on its recommendation; Torquato's first study locates an optimal
migration trigger, and a later study truncates its axis there with the reason
stated, so the dropped region is dominated rather than unexamined.

§5.1 can do the same at no extra cost, and it turns its most awkward result into
an asset. Three of the four dwell anchors are inert and one — the low-and-slow
anchor — is the only one that moves an outcome; the floor in the failure kernel
is inert on this corpus; the profile ordering moves while the headline verdicts
hold. Reported flatly that is a page of things that did not happen. Reported as a
selection, it says which single parameter the evaluation's conclusions are
actually exposed to, and therefore which one §5.2's design has to hold or vary
deliberately.

Recommend closing §5.1 with one sentence naming what the sweep selected, and
having §5.2 open by picking it up. That also earns the section its unusual
position ahead of the dimensions rather than merely defending it.

### 3.2 The sweeps on record do not share the main experiments' configuration

This is the sharpest problem in §5.1 and it is not a drafting problem.

Both existing sweeps ran at **ten seeds**, on the **pre-restoration** substrate,
with the `random` multi-mechanism scheme as the only MTD condition. The failure
matrix sweep additionally ran under the **superseded fixed-dwell timing
regime** — the record itself says a re-sweep under the settled regime is owed.
The main experiments will run at a hundred seeds on the restored substrate over
a seven-mechanism pool.

So §5.1's numbers and §5.3–5.5's numbers come from different configurations,
inside one chapter. Three honest dispositions, in order of preference:

1. **Re-run the sweeps at the reported configuration.** Cheapest in credibility,
   costs compute the record says is trivial (the whole failure-matrix sweep is
   2 600 runs; the dwell sweep about 1 560). Recommended.
2. **Report them as taken and state the configuration difference in the register
   caption**, with the argument that a stability verdict taken at a *lower* seed
   count and a *narrower* defence set is conservative. Defensible for the dwell
   anchors, weaker for the failure matrix, whose regime actually changed.
3. Say nothing. Not available — it would put two configurations on one page
   undeclared, which is the failure the conventions file names in §i.

### 3.3 Where the ablation arms live

The model's optional capabilities — the verdict-blind arm, uniform weights, the
learning exponent and decay, the incentive exponent — are factor *levels*, not
metric families, so a metric-family organisation gives them no section. They are
**declared once in §5.2's factor table** as capabilities with a null value at
which the run is bit-identical, and their **results are reported in whichever
strand instruments them**. That keeps the ruled organisation intact and needs no
new section.

**But two of them currently have no antecedent in ch4 at all** — the tex's own
flag on the fidelity table. The chapter as drafted carries the dwell times, the
mapping and the failure matrix, and neither the incentive rule nor the learner.
The fix already exists as a recommendation in the formalism inventory: show the
history-term slot in the formal definition (its ruling R3), one symbol, with
each ablation arm named as a factor in that slot.

**That ruling is therefore load-bearing for the discussion's fidelity table, not
a formalism nicety.** Without it, two of the six ticked properties are ticked on
mechanisms the dissertation never defines. Recommend taking R3 as *show the
slot* explicitly on that ground.

## 4. The funnel — one run set, two questions

Marc's double game: the same results must evaluate the defence *and* evidence
what the attacker model captures. The corpus solves this and the clearest
instance is He 2025.

> Its results section characterises the attacks against the **undefended**
> target first — which attacker knowledge level is actually more dangerous,
> which generator is viable, how an attack parameter trades evasiveness against
> intensity — and *prunes* the attack set to the configurations that matter. The
> defence evaluation then runs against those only, with the pruning rule stated.

Two properties make it work, and both transfer. The characterisation runs
**against no defence**, so it is a statement about the attacker rather than
about the interaction. And its output is a **selection step** the defence
evaluation depends on, so it earns its place instead of reading as a detour.

Applied here, §5.3 opens on the no-defence arm: what each profile does
unopposed, beside the inherited attacker. That single block is simultaneously
the attacker characterisation, the denominator for every suppression number that
follows, and the selection step that explains why breadth rather than objective
achievement is the denominator at all — because the profiled attacker reaches
the mass-compromise objective in none of its unopposed runs. Then the defence
comparison, then the cross-arm contrast.

**Attacker-property claims are legitimate results and belong here as
observations.** The verdict they add up to stays in the discussion. That
division is exactly the ruled one.

### A word that must not carry two jobs

"Baseline" is used in this project for two different objects, and the chapter
needs both. The **no-defence condition** is the reference every effectiveness
number is a difference from — that is what the field means by a baseline run,
and Zaffarano's framework makes it definitional ("Metrics are derived from the
statistical differences between these interactions during runs when an MTD is
not deployed (the baseline) and when it is deployed"). The **inherited scripted
attacker** is the comparison arm for the threat-model-dependence claim. The
ruling that the movement attacker is the new baseline speaks to the second and
does not remove the need for the first.

Recommend naming them separately at first use — the no-defence condition, and
the inherited attacker — and never letting one word carry both. A chapter that
blurs them reads as confusing a control with a competitor.

Two related gains from the same source, both cheap. Reporting a defender-side
cost on the same instrument as the attacker-side benefit is that framework's
core design move, which supports the reconfiguration-occupancy ledger in §5.4
being there at all rather than looking like an extra. And a **phase-resolved
effectiveness locator is an established measure**: the same paper defines the
kill-chain phase against which an MTD is most effective as the argmax over
phases of the mean per-task change in success, with and without the defence. The
supplementary strand's tactic-resolved MTD effect therefore has a published
antecedent and should cite it rather than introduce itself as novel.

### The property-to-measurement map

The discussion's fidelity table needs, for each ticked property, a pointer to
either a ch4 mechanism or a ch5 measurement. This is what ch5 must actually
produce, and it is the check that the strands are sized right.

| Property | Measurement on record | Strand | Arm it is read from |
|---|---|---|---|
| 1 persistence | distinct-tactic coverage over time; deepest successfully-actioned stage; foothold retention across mutations | 5.5 | no-defence, then under defence |
| 2 objective conditioning | profile divergence against its own split-half null | 5.5 | no-defence |
| 3 strategic plurality | path entropy and distinct prefixes; the per-profile defence response | 5.5 + 5.3 | both |
| 4 adaptivity | the verdict-blind ablation; action mix before against after an interrupt; recovery time | 5.5 | under defence |
| 5 stealth | none — blank, ruled | — | — |
| 6 incentive | the utility-exponent arm against the cost ledger | 5.4 | under defence |
| 7 learning | the learning-exponent and decay arms; breadth against exponent | 5.5 | both |
| 8 scheme awareness | none — blank, ruled out of scope | — | — |

**Budget risk, stated rather than solved:** §5.5 at two units carries four of the
six ticked properties plus the APT-specific measures. Either it takes a half
unit from §5.3, or the ablation contrasts compress into the register-and-table
form the conventions file says the field accepts when the finding is "nothing
moved". Marc's call at drafting time; do not silently overrun.

## 5. What the chapter cannot say yet

Five blockers, all already on record, listed here because they bound the prose
rather than the code.

1. **The headline inversion does not reproduce on the restored substrate.** The
   rank correlation between the two attackers' defence orderings was −0.893 at
   ten seeds; a re-run at fifty seeds on the restored substrate returned −0.071,
   because the *inherited* attacker's defence response moved and nothing
   re-measured it. The re-establishment experiment is unrun. **Until it runs, no
   sentence in this chapter may state the inversion as a fact of the current
   substrate**, and the chapter's headline is unsettled.
2. **Three of the seven single mechanisms have never been run against the
   movement attacker.** They entered the pool after the published matrix.
3. **The overlay version is split across the document.** A ch4 caption already
   names the failure-only overlay while the published numbers are the superseded
   one. Either re-key the experiments or write the reconciling sentence.
4. **Internal mean time to compromise ranks the mechanisms perversely** and is
   named the project's primary metric. Its brief is owed before the
   effectiveness strand names it.
5. **Cross-arm event counts are inflated about fourfold** by per-vulnerability
   row writing. The corrected counter exists; the restatement is the cost.

## 5a. What Marc's "ours is the new baseline" framing does to blocker 1

Ruled 2026-09-09: the work is not trying to beat the inherited model, because the
movement attacker *is* the new baseline. That is right, and it lowers the bar the
re-established measurement has to clear — but it lowers it rather than removing
it, and the distinction is worth keeping straight.

What the framing removes: any need for the profiled attacker to out-perform the
inherited one. Weaker headline performance is the condition of the study, not its
verdict, and that argument is already staged in the discussion notes.

What it does not remove: the cross-arm number is not a performance comparison. It
is the claim that the two attackers *reward different defences* — the thesis's
"so what", and the thing the results note in `ch6_results/` is built on. That
still needs a measurement.

**The useful consequence is that the bar drops.** The re-run no longer has to
reproduce a rank correlation of −0.893; it has to establish whatever stable
cross-arm difference exists, at the grade the evidence carries. The grading
vocabulary already covers exactly this — magnitude if the same defences win by
different margins, ordering if the ranking moves, recommendation if the top-ranked
mechanism changes — and under the merge ruling that vocabulary survives as a
sentence at the metric's definition site rather than as a unit of its own. A
result at the magnitude grade is a real result; it is a weaker sentence than the
one on record, not the absence of one.

## 5b. One concession the chapter should volunteer

The field's only enumerated prescription for an evaluation metric is Jalowski's
four guidelines, and the third is that a metric "should compare the MTD scheme
to a state-of-the-art system, protected using the best available methods". This
evaluation compares mechanisms against each other and against no defence, on one
simulator, with the defender frozen. It does not meet that guideline, and
neither does most of the corpus.

Volunteering it costs one sentence in §5.2's comparability disclosure and buys
the chapter its own critique's terms. The same paragraph is the right place to
say which half of the attacker-realism demand the work answers — a CTI-grounded,
objective-conditioned, adaptively-routed attacker, and *not* a scheme-aware one,
which is ruled out of scope and already sits in future work.

## 6. Rulings owed

| # | Question | Recommendation |
|---|---|---|
| C1 | Merge the parameter and assumption registers into one table? | Yes — §3.1. Answers the formalism inventory's R6 and saves a unit |
| C2 | Re-run the two sweeps at the reported configuration, or disclose the difference? | Re-run — §3.2. The compute is trivial; the credibility is not |
| C3 | Take the formalism's R3 as *show the history slot*? | Yes, and on the fidelity-table ground in §3.3, which is a stronger reason than the formalism one |
| C4 | Does §5.3 open on the no-defence arm as a distinct block? | Yes — §4. It is the funnel, and it is what makes the attacker characterisation a result rather than a detour |
| C5 | Where does the half unit for §5.5 come from? | §5.3, or compress the ablation contrasts to a table |
| C6 | Is the effectiveness strand's denominator breadth, target reach, or both? | Both, reported separately — breadth is degeneracy-proof at every tempo, target reach discriminates only where it is non-degenerate. Depends on the targeted-objective ruling, still open |
| C7 | Minimum effect sizes per channel | Still owed from the hypothesis tree; a cheap-run simulator makes any difference significant, so this is not optional |
| C7b | Does §5.1 close by naming what it selected, with §5.2 picking it up? | Yes — §3.1b. It costs one sentence, earns §5.1 its position, and converts a page of inert parameters into a design input |
| C9 | Does the disruption frontier expand §5.4 beyond one unit? | Probably yes — §8. Its defender-side measure is arm-invariant where attacker-side time is not, so it is the more robust of the two cross-arm claims and is currently the thinnest-funded |
| C10 | Return on attack: report the inherited per-vulnerability score, or the cost ledger's realised ratios? | The ledger's ratios, with one sentence saying why — the inherited quantity is an exploit-ordering input, not a realised return, and two lineage papers report it as an outcome |
| C8 | Declare the run count as a tolerated-error consequence rather than a round number? | Yes — §2(5). It costs one sentence, cites a method the corpus lacks, and makes the hundred-seed budget a result instead of a habit |

## 7. Papers — what arrived, and the short list left for Marc

A fetch pass ran during this session and **thirteen open-access methodology and
survey sources are now in the repo** under `docs/sources/methodology/`, each
verified against its title page, each with a plain-text conversion carrying page
markers, and each logged with the route used in that directory's acquisition
log. That covers most of what I would otherwise have asked for: the two
sensitivity-analysis reviews, the global-sensitivity review, the agent-based
sensitivity guide, Sargent on verification and validation, Hoad and Robinson on
choosing a replication count and on warm-up length, the two experimental-rigour
critiques, the simulation-based MTD study, and two MTD surveys including the
333-page Lincoln Laboratory one.

**What is actually left, in priority order:**

1. **Cai, Wang, Luo & Hu (2016), "A Model for Evaluating and Comparing Moving
   Target Defense Techniques Based on Generalized Stochastic Petri Net"**,
   Advanced Computer Architecture, Springer, doi
   `10.1007/978-981-10-2209-8_16`. The closest possible structural precedent — a
   generalised stochastic Petri net used to *evaluate and compare* MTD
   techniques — cited in ch4 as the MTD Petri precedent, with no copy in the
   repo. Springer chapter; institutional access.
2. **Ajmone Marsan et al.** — the formalism citation, already owed for §4.3.
   Either the 1984 ACM TOCS paper or the 1995 book.
3. **Ben-Asher, Morris-King, Thompson & Glodek (2016), "Attacker skill, defender
   strategies and the effectiveness of migration-based MTD"**, ICCWS 2016. Found
   by a census of the existing sources: cited by Cho, Tay and Kim, extracted
   nowhere. An attacker-skill × defender-strategy study is the closest published
   relative of this dissertation's threat-model-dependence claim.
4. **Lei et al. (2018), "Moving Target Defense Techniques: A Survey"**,
   Security and Communication Networks, doi `10.1155/2018/3759626`. It is CC-BY
   and therefore free, but the publisher's endpoint refuses non-browser clients.
   Opening the DOI in a browser and pressing the PDF button is the whole task.
5. **Hoad, Robinson & Davies (2010)**, the journal version of the
   replication-count paper. Only if the journal wording is specifically wanted —
   the 2007 conference paper carrying the same method is already in the repo and
   is the citable substitute.

**One bibliography action that follows.** The methodology chapter's
operational-validation argument invokes Sargent's taxonomy, and the entry for it
in the bibliography is commented out because no source was held. The source is
now in the repo, so the entry can be activated and the argument cited rather
than attributed from memory. The same is true of the replication-count rule,
which the chapter currently has no citation for at all.

## 8. Drafting cards — the shape of each section

Added 2026-09-09 on Marc's ask: for each heading, what goes under it, the shape
the literature would give it, how it ties to the formalism and to what is already
built, and what must change before numbers are written. These are cards to write
*against*, not prose to adopt.

### The chapter's one-sentence logic

The attacker model of chapter 4 has three declared inputs and a set of optional
capabilities. §5.1 prices the inputs. §5.2 declares the experiment. §5.3–5.5
run it, on three metric families: what the defence achieves, what it costs, and
what the inherited suite cannot see. The discussion then reads a verdict off
them. Nothing in this chapter argues; it declares, measures and reports.

---

### §5.1 Sensitivity analysis

**Why these three and not others.** They are not a list of worries — they are
*the* free parameter families of the formal definition, one each:

| §4.3 element | What it is in the net | §5.1 subsection |
|---|---|---|
| `W(τ_p) = 1/μ_p` | the rate of every timed transition | 5.1.1 dwell times |
| `φ: P → A ∪ {⊥}` | the coupling between the net and the environment | 5.1.2 mapping |
| `F_failure = R · d` | the conditioning factor on the immediate weights | 5.1.3 failure matrix |

That is the tie-in Marc asked for, and it is what makes the section legible: the
formalism has three places where a number had to be chosen, and this section
prices all three. Say it once in the preamble and the section stops looking like
a detached methods block.

**Shape, per subsection** — Tay's repeating form, which is the local genre and
also the clearest in the corpus:

1. Name the parameter and what it trades off.
2. Declare the range **and its justification**. Ours come from the formalism and
   the derivation records, which is more than the corpus gives.
3. The figure (or, where nothing moved, the table).
4. The numeric readout. The "why" is deferred to chapter 6.

**Presentation.** Line chart, x = the swept parameter, y = the metric, series = a
second factor at two to four levels, one figure per parameter (Anderson's form,
also Hong's and Carroll's). Where the answer is "nothing moved", a band-ends
against-centre table is the honest compression — `app:sensitivity`'s anchor table
already is one.

**Close by naming what the sweep selected.** Three anchors inert, one not; the
floor inert; profile ordering unstable for a power reason. As a list that is a
page of non-events. As a selection it says: the conclusions are exposed to one
declared parameter, and here is the operating region that follows. §5.2 then
opens by picking it up. Manadhata and Wing assign their later parameters on their
sensitivity analysis's recommendation; Torquato truncates a later axis at the
optimum a first study found, with the reason stated.

**What must change before numbers are written here:**

- **Re-run both sweeps at the reported configuration.** They ran at ten seeds on
  the pre-restoration substrate with one MTD condition, and the failure-matrix
  sweep under the superseded fixed-dwell regime. About 2 600 + 1 560 runs;
  minutes of compute. Without this the chapter carries two configurations on one
  page.
- **Settle the overlay version.** A chapter-4 caption already names the
  failure-only overlay; the published sweep numbers are the superseded one.
- **Rule the register merge** (C1), because it decides whether the twelve
  assumptions are table rows here or a paragraph in chapter 4.

---

### §5.2 Experimental dimensions

**Shape.** The corpus's cleanest form is Reti's **two tables**: one of the
factors that vary with their levels, one of everything held fixed with its value.
That is the same swept-or-held logic as §5.1's register, applied to the
experiment instead of the model, and it makes the design auditable at a glance.
Ho does the same thing across two sections; Zhang folds it into an untitled head
before the first result.

**What goes in the varying table:** attacker arm (inherited baseline; four
objective profiles; the aggregate envelope), defence condition (none; seven
single mechanisms; three deployment schemes), mutation tempo, network scale and
density. **What goes in the fixed table:** horizon, geometry, seed set, the
timing regime, the mapping version, the overlay version, the modulator nulls.

**Also here, and nowhere else:**

- The metrics, **named as instrumentation** and grouped by family, with the
  comparability boundary stated as a disclosure: within-simulator comparison is
  valid, cross-paper numeric comparison is not.
- The **run count as a consequence** — declare the tolerable error in the
  estimate, then the count follows. No lineage paper does this; Brown states no
  count at all.
- The **operating-point fact**: at the default tempo the success metric cannot
  discriminate, because neither attacker completes the objective. Stated once,
  as a design fact. Its interpretation is chapter 6's.
- The **ablation arms declared**, each with the null at which the run is
  bit-identical. This is where they live; their results ride the strands.
- The **volunteered concession**: Jalowski's third metric guideline asks for
  comparison against a state-of-the-art protected system. We compare mechanisms
  against each other and against no defence, with the defender frozen.

---

### §5.3–§5.4 Effectiveness and efficiency — what the split actually means

Marc asked what separates them and whether we really have efficiency. Both
answers are firmer than expected.

**The axis is Cho's, and Table 3.1 already implements it.** Effectiveness asks
*did the defence achieve the security goal* — measured on what happens to the
attack: success events, attacker time, attack paths, system state. Efficiency
asks *what did that cost* — resource spent, on either side. Goal attainment
against the price of attainment. Both are crossed with the attacker/defender
perspective, which is why each has an attacker-side and a defender-side half.

**We do have efficiency, on both sides, and it is instrumented today:**

- *Attacker side* — the cost ledger, which decomposes a run into attempts by
  verb (split blocked and dwell-only), time into behavioural dwell plus the
  mutation penalty plus residual, the re-work a mutation forced, distinct hosts
  and yield per unit time; plus the effort-to-breadth ratios (actions and
  successes per distinct host).
- *Defender side* — the reconfiguration ledger: what fraction of the run at
  least one layer was being reconfigured, decomposed by layer and mechanism,
  plus churn tempo and the suspended-mutation tally. It is derived entirely from
  the simulator's own per-mutation records, so it introduces no new declared
  value.

**One caution on return on attack.** The inherited quantity is a
*per-vulnerability attractiveness score* the attacker uses to order exploits,
not a realised return over a run — while two papers in the lineage report it as
an outcome. If the chapter reports it, it must say which sense it means, or use
the cost ledger's ratios instead and say why.

**What we genuinely do not have:** quality of service to users and system
performance overhead — the half of the field's efficiency axis that needs a
workload model. Not instrumentable on this substrate; state it once as scope,
in the same sentence as the frozen defender.

**The finding that may be underweighted at one unit.** Pairing attacker-side
suppression against defender-side occupancy gives a cost–benefit frontier per
mechanism, per attacker — and the result on record is that the *shape of the
trade* inverts with the attacker. Two properties make this attractive. It is the
same claim family as the ranking result but on a different instrument, and its
defender-side measure is **arm-invariant** — reconfiguration time is priced by
the simulator on both arms, unlike attacker-side time. So it is the more robust
of the two cross-arm claims, and it is the one currently allocated a single unit.
Worth a ruling: does the frontier ride §5.4 with more budget, or stay a
supporting result?

---

### §5.3 Effectiveness — the three subsections

**5.3.1 Without defence.** The funnel's first step, and the reason the section is
subsectioned at all. He 2025 characterises its attacks on the undefended target,
prunes to what matters, then evaluates the defence against that, with the pruning
rule stated. Here the block does three jobs at once: it is a claim about the
attacker rather than about the interaction, because nothing is defending; it is
the denominator every later suppression number is a difference from; and it is
the selection step that explains why breadth is the denominator, since the
profiled attacker reaches the mass-compromise objective in none of its unopposed
runs. State the pruning rule explicitly — that is what stops it reading as a
detour.

**5.3.2 Under defence.** The conditions against both attackers. Report the
no-defence condition as the origin of a relative-change plot, not as its own
series (He's form; Tay normalises by it; Brown plots it as a bar). Note the
condition set is not the published matrix's: three of the seven single mechanisms
entered the pool afterwards and have never run against the movement attacker.

**5.3.3 Across the two attackers.** The cross-arm contrast plus the lineage
headlines re-run under both attackers, which belong inside the strand they
instrument rather than in a section of their own. Blocked on the re-established
measurement; the bar is whatever stable difference exists, at the grade it earns.

---

### §5.5 Supplementary measures — what it does that the other two cannot

**The argument for the strand existing.** Effectiveness and efficiency are the
inherited suite's axes, and that suite was built for an attacker whose behaviour
is scan, exploit, propagate. It has no vocabulary for a tactic, a phase, or a
behavioural distribution. So it can say what an attacker achieved and what that
cost, and it cannot say:

- how much of a campaign lifecycle was traversed, or in what order;
- whether behaviour varies across runs and differs between profiles;
- whether the attacker changed what it does after being disrupted;
- whether accumulated knowledge changed anything.

Those are precisely the properties the fidelity criterion scores. **The
supplementary strand is the measurement side of the attacker model's own claim** —
which is also why it is the strand that would not exist if the contribution were
a mechanism rather than an attacker.

**Where the two subsections came from.** They split by *how the evidence is
obtained*, not by topic:

- **5.5.1 Campaign structure and plurality** — read directly off the walk, mostly
  from the no-defence arm: distinct-tactic coverage over time, deepest
  successfully-actioned stage, foothold retention (property 1); profile
  divergence against its own split-half null (property 2, the one property shown
  to change an outcome); path entropy and distinct prefixes (property 3).
- **5.5.2 The declared capabilities, ablated** — cannot be read off a single arm
  at all; each needs a contrast against its null: the verdict-blind arm
  (property 4) and the learning arms (property 7). Both return measured
  negatives, and those negatives are among the most credible things the work
  owns.

The literature tie is direct: Tay's evaluation chapter has an explicit ablation
subsection, so the second card has a local precedent in this supervisor's own
lineage, and He devotes a results subsection to a structural property of its
defence rather than to an outcome.

Also here: the tactic-resolved MTD effect, which should be **cited, not claimed
as novel** — Zaffarano defines the kill-chain phase against which a defence is
most effective as the argmax over phases of the mean per-task change in success
with and without the defence.

---

### The full change list before numbers are written

1. Re-run the two sweeps at the reported configuration (§5.1).
2. Settle the overlay version, or write the reconciling sentence.
3. Rule the history slot in the formalism, so the ablation arms have a chapter-4
   antecedent and two fidelity marks stop resting on undefined mechanisms.
4. Resolve the internal mean-time-to-compromise question before §5.3 names it.
5. Correct the cross-arm event count before any cross-arm event number.
6. Run the headline re-establishment before §5.3.3 is drafted.
7. Rule whether the disruption frontier expands §5.4 beyond one unit.

## 9. Second pass (2026-09-09) — the restructure, and three answers

Marc's objection: the supplementary strand is weak, and the instruments used to
evidence the attacker model "were proprietary and ad hoc and maybe not in the
metric family we defined for MTD evaluation — they're more for attacker
evaluation on the simulator". That is correct, and it is a structural fault
rather than a drafting one.

### 9.1 The fault, and the fix

A chapter organised by instrumented metric family has **two** families,
effectiveness and efficiency. The eight-property evidence is measured on
instruments in neither: coverage curves, profile divergence against a split-half
null, path entropy, interrupt action mix, the disengagement frontier. Calling
them a third family is a category error, and it is exactly what made the old
supplementary section read as a grab-bag.

The fix gives that evidence its own section, named for what it is, placed before
the evaluation — which is also the funnel:

| | Old (2026-09-08) | New |
|---|---|---|
| 5.3 | Effectiveness: unopposed, under defence, cross-arm | **The attacker model in operation**: unopposed, response to disruption, the declared capabilities |
| 5.4 | Efficiency | **Effectiveness**: under defence, across the attackers, the prior models re-run |
| 5.5 | Supplementary measures: structure, ablations | **Efficiency** |

Units unchanged at twelve. Nothing is lost — every measure from the old 5.3.1 and
5.5 is in the new 5.3, and the no-defence arm still serves double duty as the
reference the effectiveness section reports against. Four gains: the
attacker-model instruments are labelled as what they are instead of disguised as
a metric family; all eight properties are read in one place, so the discussion's
fidelity walk points at one section rather than three; the funnel becomes the
chapter's spine rather than a subsection of it; and the two evaluation sections
become purely about the defence, which is what the merge ruling wanted.

Reverting is one edit: split 5.3 back across effectiveness and a supplementary
section. The comment blocks travel with their subsections.

### 9.2 Does the hypothesis tree carry?

**As a planning artefact, yes. As chapter structure, no.** The tree was built
when the chapter was going to be setup plus burden-of-proof plus grading — the
two-limb shape the merge ruling superseded — and its AND/OR gating with
alpha-spending is the wrong register for a chapter ruled facts and figures only.
What survives and is still load-bearing: it is the inventory of which runs must
happen, and it fixes the failure dispositions in advance, which is what stops a
result being reframed after it is seen. Keep it in the record; do not surface it.

### 9.3 Where a meaningful difference can come from, given one action set

Marc's hardest question: both attackers share the same six verbs, so how can
they possibly produce different defence responses?

**The answer is mechanistic, not statistical, and it is already on record.** The
two attackers cannot differ in *what* they can do. They differ in **which
substrate property they depend on**, and the defence family splits on exactly
that line:

- The movement attacker is **position-driven**. Network-layer defence clears the
  host cursor, so it severs position: blocked fraction rises from 0.15 to 0.72.
  This is not address tracking — the attacker has no addressing model at all — so
  the two network-layer mechanisms are *one* attacker-facing effect, 0.721
  against 0.725.
- The inherited attacker is **exploit-driven**. Application-layer defence
  re-rolls the vulnerability set on uncompromised hosts, which is the thing it
  leans on. It barely reaches the movement attacker, whose blocked fraction stays
  at the no-defence level of about 0.16, because exploitation is uninterruptible
  on that arm.

So the family is a two-by-two — severance against surface re-roll — and the
difference between the attackers is which half of it matters. Same alphabet,
different order, mixture and targeting. That is the sentence §5.4.2 exists to
earn, and it is why "same action set" does not imply "same defence response".

### 9.4 The figure and table budget

Corpus norm for an evaluation of this length: Brown two results figures and one
parameter table; Zhang about seven figures; Tay five figures and no tables at
all; Ho about eight figures and eight tables; Reti six figures and two tables.
The chapter targets **nine figures and four tables**, itemised in the tex per
subsection with each one's purpose stated. The load-bearing ones are the
register table, the coverage curve (the clearest single picture of what the model
added), the suppression bars by attacker arm (the whole claim in one figure), and
the cost-benefit frontier.

## Validation gate

The design half is discharged: ratified and scaffolded. What remains is that
Marc rules C1–C8 and that the §5.1 register exists as a generated table whose
numbers come from artefacts rather than transcription. Section prose waits on
the blockers in §5 — §5.1's on the sweep configuration, §5.3.3's on the
re-established measurement.

## Hard constraints

- Numbers in the tex come from tracked artefacts, never typed.
- The badge ceiling is untouched by anything here: this file plans where evidence
  is reported, never what it licenses.
- The drafting pipeline holds — no session-written prose in the tex.
- Within-substrate comparison only; the comparability boundary is a disclosure in
  §5.2, not a footnote.

## Reading list

- [`../workflows/evaluation_conventions.md`](../workflows/evaluation_conventions.md)
  — the evidence layer this design rests on.
- [`../implementation/pipeline/ogasp/hypothesis_tree.md`](../implementation/pipeline/ogasp/hypothesis_tree.md)
  §§7, 8c, 8f — the leaves, the two limbs, and what went stale on the restored
  substrate.
- [`../implementation/pipeline/ogasp/evaluation_predesign.md`](../implementation/pipeline/ogasp/evaluation_predesign.md)
  §§4–5 — the statistical instrument and the run budgets.
- [`2026-09-08_ch4_s43_gspn_formalism.md`](2026-09-08_ch4_s43_gspn_formalism.md)
  §7 — the two registers this file proposes merging, and rulings R3 and R6.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(c), §(d) — the properties the map in §4 must feed.

## Out of scope

Running any experiment; changing the tex; re-opening the merge ruling or the
metric-family organisation; the notes-directory rename that the merge implies.

## Note on a superseded sibling

An untracked handoff dated 2026-09-08 proposes a two-limb split across a
separate setup chapter and a results chapter. Marc's merge ruling overtakes it
and the tex comment records that. It is another session's file and is left for
its owner; nothing in this design depends on it.
