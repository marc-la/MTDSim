---
status: open — design ratified and scaffolded; §5.2 DESIGNED 2026-09-14 (§20; C34, C36, C37 ruled; C32–C33, C35, C38–C41 owed; §20.8 the ch3 trace); restructured 2026-09-09 second pass (§9); reviewed third to fifth passes 2026-09-09 (§10–§12); four-reviewer scrutiny pass (§13); Marc's rulings + the horizon answer (§14, §15); register re-cut and assumptions moved to ch4 (§16); headings (§17) and the float audit (§18) APPLIED 2026-09-13; C1 reversed; C29–C30 done, C31 confirmation owed
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
6. **The learning negative is a pre-restoration result with a named reopening
   condition** (added by the third pass — §10.4). Every exploit-learning number
   predates `d127f443`, which reinstated the OS-gated exploit-success channel and
   may have dropped the perfect-exploit ceiling the null rests on. One no-MTD
   cell decides whether a ≈ 370-run re-test is owed; until it runs, §5.3.3 states
   a negative measured on a substrate that no longer exists.

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

---

## 10. Third pass (2026-09-09) — the review, and what it found

Marc's ask, in his words: *verify and critique the current setup* — go through
the implementation records and see what late-pipeline work can be pulled to the
fore; go through the notes and ask how they tie in **in the experimental sense**;
check the MTD-evaluation survey is faithfully represented; and answer a list of
specific objections to the chapter as scaffolded. This section is that review.
Everything actionable is also written into the tex as a comment block at the
section it governs, so a cold drafting session finds it in place rather than
here.

### 10.1 The defect Marc named, fixed

**Every ch5 float rendered before the heading it belongs to.** Figures 5.1–5.4
landed on pp. 28–29 against subsections on p. 30; §5.4.1–5.4.3 all sat on p. 37
with their figures on pp. 34–36. Cause: with no prose between them, the float
queue flushes ahead of the headings. Fixed by loading `float` and pinning ch5's
22 placeholder floats with `[H]`, and by reordering §5.1, §5.2 and §5.5 so the
placeholder paragraph leads its floats. Every float now sits on or after its own
subsection's page. **Revert each `[H]` to `[htbp]` as that subsection's prose
lands** — this is a placeholder-phase measure, recorded in `FLOATS.md`.

### 10.2 Marc's questions, answered

**Q. What is Table 5.1 for, and is it every assumption? Here or the appendix?**
It is the answer to a question a reader of an MTD evaluation cannot otherwise
ask — *how much of this result is a choice?* Yes, it is every assumption: a held
row **is** an assumption, which is why no separate assumption list exists in the
document (C1). The recommendation is **both homes, split by function**: the body
table carries one row per declared *family* (the four dwell anchors as one row,
the nine failure rules as one row) at 10–14 rows and half a page; `app:sensitivity`
carries the per-value expansion, which is the form `tab:anchor-sensitivity`
already has. A 40-row body table stops being read, and an unread honesty table is
worth less than a short one.

**Q. Is §5.1 what a sensitivity analysis looks like?** Yes on shape — one factor
at a time over a declared band, one figure per parameter, band ends against
centre, readout separated from interpretation. Two qualifications and one gap.
(i) OAT is the *weak* form and the methodology sources say so: it explores a
cross through the space, never its interior, so it cannot see an interaction. The
failure matrix already half-answers that by also running the corners of the
influential pair; one sentence naming OAT and the corner check pre-empts the
obvious question. Do not claim a global sensitivity analysis. (ii) §5.1.2 is not
a sensitivity analysis in the same sense — the mapping is a discrete swap, so it
reports a robustness check, and the section is stronger for saying so. (iii)
Three of the four figures are figures of non-events; the fix is C7b, already
planned — close on the one parameter the conclusions are exposed to and demote
the inert results to register rows.

**Q. What axes of disruption does §5.3.2 run — which mechanisms?** The chapter
never said, and it must. The spanning set is not the SDR taxonomy and it is not
all seven mechanisms: it is a **2 × 2 on attacker-facing effect**, which is the
resource layer the mechanism rewrites — network layer → **severance** (clears the
host cursor; blocked fraction 0.15 → 0.72; the two network-layer mechanisms are
*one* attacker-facing effect at 0.721 against 0.725), application layer →
**surface re-roll** (barely reaches this attacker; blocked fraction stays at the
no-defence ≈ 0.16, because exploitation is uninterruptible on that arm). One
mechanism from each layer spans the effect space for this subsection; the full
condition set belongs to §5.4. **And the SDR classes do not span it — which is a
finding, not a convenience:** shuffle spreads across both layers while diversity
sits in one, so the taxonomy the literature reads by and the taxonomy the
attacker feels are different partitions. The third axis is **tempo**, not a
mechanism: a response visible at one mutation interval is a property of the
interval, so show it at two. Free extra: the **pure-interrupt pair** (IP shuffle
and port shuffle reach the attacker through the interrupt alone) prices what an
interrupt by itself is worth at each layer, and costs no new runs.

**Q. "Declared capabilities" — I don't understand that section.** Repo
vocabulary. It means the two things the attacker was *given* that it need not
have had, each with a setting at which it switches off and the run is
bit-identical. Those two things are a sense of cost and a memory, so the heading
now says that: **§5.3.3 "A cost model and a memory"**. Alternatives left in the
tex; Marc's to overrule.

**Q. "Action mix" — I don't understand that.** Jargon leaked from the measurement
suite. What it is: *what the attacker is doing changes after it is hit*. Take the
handful of steps immediately before each mutation and the handful immediately
after and compare which activities fill them; more reconnaissance and less
exploitation after a mutation is the attacker re-orienting. Paired within run so
run-to-run variation cancels; the verdict-blind arm is the control that separates
response from drift. The figure's placeholder text now says that; the prose
should never say "action mix".

**Q. Effectiveness is basically just pure runs — the profiles unopposed?** No —
that is §5.3, which now sits immediately above it and takes the unopposed arm.
§5.4 runs the **defences**; every number in it is a difference from the
no-defence reference §5.3 fixes. The one-line separation, worth putting in the
roadmap sentence: §5.3 asks what the attacker does, §5.4 asks what the defences
do to it, §5.5 asks what that costs on both sides.

**Q. We can dial the attacker's predictability down and find a nice baseline.**
The dial exists, and it is already in §5.3.3 under another name: **λ, the
rationality exponent**. It exponentiates each transition's utility ratio against
the out-set mean, so at λ = 0 every factor is 1.0 and the run is bit-identical to
no modulator, and as λ rises the routing concentrates on high-payoff moves —
concentrating the routing *is* making the attacker more predictable. So **one
sweep carries two readings**, and the second is free: report effective
behavioural breadth beside the outcome measure at each λ. The uniform-weight arm
is the other end of the same axis. That also gives the "nice baseline" a
criterion instead of a feel — **the operating point is the largest λ at which
behavioural breadth is still plural**, which converts λ from a declared value
into a selected one, the same move §5.1 makes. **It is not an equilibrium:** the
defender is frozen on a schedule, so there is no second player optimising against
this attacker, and the word must not appear.

**Q. Are we budgeting 3 000 words?** Yes — 12 units × ~250 words is the ledger's
own allocation, and the arithmetic is exactly right. Three things make it behave
differently here. (i) **Floats are outside the word count** — the ledger's targets
exclude tables and figures, and every caption is written long on purpose, so the
chapter's argument is mostly not in its word budget. That is what makes 3 000
words affordable for a results chapter. (ii) **The binding constraint is pages,
not words**: 15 figures + 7 tables is about twelve pages of floats against roughly
seven of prose, above the corpus norm; `FLOATS.md` marks 9 + 4 core and the rest
is the cut list. (iii) **The heading count already exceeds the unit count** — 5
sections + 9 subsections = 14 headings on 12 units. It balances only if §5.3 and
§5.4 spend nothing at section level beyond a roadmap sentence and §5.1's
subsections average two-thirds of a unit. So Marc's instinct is right: **most
sections here are half-units by nature**, and a subsection that grows to a full
250 words has taken the budget from a sibling. §5.3.1 and §5.4.2 are the two that
want to overrun.

### 10.3 Sweep 1 — the implementation records: three instruments that exist and are not placed

Marc's framing: *we instrumented it so we could show our model is less
detectable, less predictable; we produced these metrics but they weren't really
the right metrics — they're attacker-side*. The answer is sharper than the design
pass gave. Two of the three are the **right** metrics and are stronger than what
the chapter currently draws; the third is right on its own terms and is fenced by
a badge ruling, not by a measurement problem.

**(a) Opening variety is the ruled primary plurality exhibit, and it is not in
the chapter.** `plurality_reporting.md` closed on Marc's own second-pass ruling:
the axis-3 fidelity exhibit is **distinct k-place opening sequences** per profile
against the inherited FSM's structural single ordering — every profile opens on
the same entry tactic and fans out with depth at a profile-specific rate, where
the baseline holds one at every k, structurally. The same record **killed the
alternative**: the entropy fan was ruled not drawn because its pre-registered
kill criterion fired at Spearman −0.967 between pooled path entropy and maximum
single-place visit share, so an entropy chart is a hub-occupancy chart wearing an
entropy axis. As scaffolded, §5.3.1 has entropy in `tab:unopposed-summary` and no
opening variety at all — which inverts the ruling. Recommendation: add opening
variety as the plurality figure, or make Fig. 5.6 two panels (divergence |
opening fan). No new unit either way.

**(b) Effective behavioural breadth is the cleanest cross-arm statement the
project owns, and it is nowhere in the chapter.** `predictability.md` (V2 rework,
ratified after the 2026-08-11 challenge) established the inherited attacker
*against its own code* as a **deterministic policy** — every (phase, branch) cell
carries exactly one successor, so it exercises **one** effective behaviour, while
the movement attacker runs **2.7–5.9**. That is a calibrated instrument with a
self-test, computed on both arms, and it says in one number what §5.3.1 currently
says in three. Two disciplines travel with it, both already ruled: the term
*predictability* is **retired in this venue** (Cho and Jalowski own it for
defender-terrain foreseeability), and the honest phrasing is a deterministic
policy against a stochastic one.

**(c) The detectability contrast is measured, survives its own ablation, and is
fenced by a badge ruling — Marc's call, and it is a real one.**
`stealth_spacing_diagnostic.md`: four of five profiles space their verb
invocations **1.5–1.8× further apart** than the inherited attacker with seed
intervals disjoint; the same four are **45 % quieter on the level** (mean 0.40
against 0.72), holding on the time-average and the median; and an ablation
attributes the **whole** margin to the non-action tactics — delete them and every
profile falls under the baseline. The fifth profile inverts, and its composition
says why (fewest non-action tactics), which is the mechanism working rather than
an exception. Axis 5 stays **NOT ADDRESSED** because there is no detection model
for a spacing choice to matter against — the axis's own argument, held three
times. **The fence is on the badge, not on the measurement.**

> **Ruling owed (C11).** May ch5 report the spacing contrast as an *observation*
> about what the two attackers do, with `tab:fidelity-verdict`'s axis-5 cell
> still blank? **Recommended yes**, one sentence plus a `tab:unopposed-summary`
> column, on three grounds: it is the only cross-arm behavioural contrast the
> work owns that is not about outcome; it is what makes §4.4.2's dwell catalogue
> visible in behaviour rather than only in declaration; and reporting a
> measurement while withholding the badge is exactly the discipline the criterion
> exists to enforce. Two caveats travel with it verbatim — the granularity
> confound is *not* resolved (state it at invocation granularity with the
> per-vulnerability reading beside it), and most of the contrast is present
> before any decay is applied, so what the decay adds is the shape of the quiet,
> not the separation. If the ruling is no, it goes to ch7 as a named condition,
> not silently.

### 10.4 Sweep 1b — a new blocker the chapter's list does not carry

**The learning negative is a pre-restoration result with a named reopening
condition, and Fig. 5.9's caption states it as settled fact.** Every
exploit-learning number predates `d127f443`, and that commit changed exactly the
channel the capability probes: D-19 reinstated the **OS-gated exploit-success
channel**, so OS-dependent vulnerabilities now fail on a mismatched host. The
2026-08-11 null rests on a **perfect-exploit ceiling** — when a roll always
succeeds, no exploit-phase capability has headroom, so of course the learner buys
nothing. If the OS gate now refuses a material fraction of this attacker's
exploits, that ceiling has dropped and the learner has headroom it did not have
when it was measured. The original sweep also moved only `services_per_os` and
never the OS pool, which D-19 has made a live lever.

**The cheap pre-check decides it:** measure the movement arm's exploit-success
rate on **one** no-MTD cell on the restored substrate. Little refusal → the null
stands as written and the caption is safe. Material refusal → re-test (≈ 370
runs) with the OS pool as a second lever before any sentence claims the negative.
This joins the five blockers in §5 as **blocker 6**, and it is the cheapest of
them to clear.

### 10.5 Sweep 2 — the notes, read in the experimental sense

Every rubric-passed note in `ch7_discussion/` and `ch5_experimental_setup/` is now
paired with the ch5 measurement it needs, as a parked-discussion-points block in
the tex under `sec:evaluation-implications`. The point of the pairing is the
**reverse direction**: a discussion point with no ch5 measurement behind it is
either a cut or an experiment nobody designed. Reading the list that way returns
two things:

- **One note is currently unevidenced.** `pure_interrupt_pair.md` needs IP shuffle
  and port shuffle run as a *named contrast*. They are two conditions already
  inside the seven, so the cost is a sentence and a column, not a run — but as
  scaffolded the chapter does not pick the pair out, so the note has nothing
  behind it and would have to be cut rather than asserted.
- **One note's foundation may move.** `learning_without_context.md` rests on the
  evidence §10.4 puts a pre-check under.

**Two notes the merge ruling orphaned**, flagged for a docs pass rather than
actioned: `ch5_experimental_setup/evaluation_burden.md` and `evaluation_grading.md`
were written for units this chapter no longer has. The grading vocabulary
survives as a sentence at the metric's definition site; the burden of proof is not
a unit at all. Both need a status line saying so, or a cold session will draft a
section from them.

### 10.6 Sweep 3 — is the survey faithfully represented? Two gaps, both cheap

The conventions file's own prescriptions were checked against the scaffold. Most
are carried. Two are not, and a third is a coverage question Marc asked directly.

**(1) The defender's half of the model is undeclared anywhere in the document.**
The corpus convention (§g) is a threat model written as Goal / Knowledge /
Capability applied **symmetrically**; He's is the tightest form. ch4 is an entire
chapter of the attacker's half, so that side is discharged — but the defender's
half exists nowhere. It is three clauses and it belongs in §5.2 beside the
frozen-defender concession: goal (disrupt, not detect), knowledge (none of the
attacker — there is no detection channel), capability (seven mechanisms on a
fixed schedule, never reacting). Cheapest possible way to answer the frozen-
defender objection before it is raised.

**(2) The adaptive defender is in ch2 and nowhere here.** Table 2.5 puts
MTDShield in the roster as one of five deployment strategies and this chapter
runs none of it. Defensible — the agent needed rebuilding before it could trade
cost against risk at all, and `mtd_ai_cost_calibration.md`'s verdict is *GO for a
scaled training proposal*, not a trained model, while Tay's published figures
characterise a uniform random selector — but it must be **declared, not silently
absent**, or a reader compares our roster against ch2's and finds one missing.
One held row in Table 5.3, pointing at future work.

**(3) The coverage map — what we have on the field's own taxonomy, and what we do
not.** Table 3.1's ten metric families against what this simulator can produce.
We report on six.

| Family | Standing |
|---|---|
| success events | Attacker-side ASR **degenerate** at the operating tempo (neither attacker completes the objective) — the suite computes none. Defender-side reported as **blocked fraction** (Brown's "attack actions blocked"), 0.15 → 0.72. Detection rate: **no** — no detection channel exists |
| attacker time | Internal MTTC exists with three riders (it is the *substrate's* quantity; cross-arm comparability withdrawn under S3-R; it ranks the mechanisms perversely). The usable channel is **delay to first compromise**, censored |
| game payoff | **No.** There is no game model. The utility modulator is an attacker *decision input*, never a payoff metric, and must not be reported in this cell |
| attack paths | **No**, as the family defines it. APV/APN/APE/SAPV are graph-theoretic over a graphical security model; we measure path variety over the attacker's own walk. Different object, similar name — state the difference, do not claim the family |
| configuration space | **No.** Attack surface not computed. **Name collision, already ruled:** Cho's *unpredictability* is a defender-terrain property of the configuration space; our behavioural-variety measure is not that, which is why the name was retired. Do not let our measure be read into this cell |
| system state | Host-compromise breadth (the HCR-shaped quantity). Risk, confidentiality/integrity: no |
| network-state change (effectiveness) | Churn tempo (an MEF analogue) and time-since-last-mutation, from the disruption ledger. Host IP variability: no |
| resource spent | **Both sides — the strongest coverage in the chapter.** Attacker-side: the cost ledger (attempts by verb, time split into dwell / mutation penalty / residual, re-work, effort-to-breadth ratios), which includes Brown's "attempts required" directly. Defender-side: reconfiguration occupancy plus `downtime_ratio`, the node-replacement-downtime analogue Tay reports |
| service to users | **No.** QoS and system performance overhead need a workload model the substrate does not have. Say it once, in the same sentence as the frozen defender |
| network-state change (efficiency) | Deployment-window time by layer and by mechanism — the raw material for the variant-cost family |

**The honest headline, and it is worth more than the table:** on the field's own
taxonomy this evaluation is **strong on cost (both sides), adequate on
containment and delay, and silent on surface, payoff and service** — and the
silence is a property of the simulator, not an oversight.

### 10.7 The largest omission: the objective denominator is not a factor

`hypothesis_tree.md` §8e makes the objective a first-class experimental
dimension, and the scaffold's factor table has no row for it. Under the **mass**
objective the attacker reaches the goal 0/400 even unopposed, so "MTD denies the
objective" is vacuous — which is precisely why the claim is denominated on host
breadth. The **targeted** objective is what fills that vacuum, and the Gate 0
probe has run (`targeted_attacker_findings.md` §4, 8 400 runs): non-degenerate at
**layer 1 on `aggregate` only** (38.3 % [33.1, 43.1] against a 20 % bar), marginal
at layer 2, failed at layer 3 and on the database set — and **the four
objective-conditioned profiles fail the Gate at every depth**. Consequence: a
targeted headline is a headline about the aggregate envelope, so `aggregate`
would have to become a *branch* of the claim rather than characterisation. E7
(four single mechanisms × both arms × 100 seeds at the layer-1 target) is
designed and awaits Marc's ruling.

Recommendation (C6, restated with the Gate result in hand): keep **breadth** as
the backbone — it is degeneracy-proof at every tempo — and report **target
reach** beside it wherever it is non-degenerate. Either way the objective must be
a row in Table 5.2 or Table 5.3. What is not available is leaving the reader to
infer which goal a suppression number is a suppression *of*.

### 10.8 One consequence of the run-count arithmetic, stated before it is met

`evaluation_predesign.md` §5 already carries measured per-cell variance and the
seed requirement per adjacent pair (≈ 18, 22, 190 and 329 seeds — the two tight
pairs drive the budget). The honest consequence: **at 100 seeds the adjacent
within-family ranks are not separable**, so the reportable object is the 2 × 2
family contrast and not a total order. Say that in §5.2 rather than discovering
it in the results — it is the same discipline as the operating-point fact, and it
protects §5.4.2 from a strained ranking.

### 10.9 Rulings owed from this pass

| # | Question | Recommendation |
|---|---|---|
| C11 | May ch5 report the spacing / detectability contrast as an observation with axis 5 still blank? | Yes — §10.3(c); one sentence and a column, with both caveats verbatim |
| C12 | Does opening variety replace or join the plurality evidence in §5.3.1? | Join, as a panel of Fig. 5.6 — it is the ruled primary exhibit and entropy is a hub-occupancy proxy |
| C13 | Does effective behavioural breadth enter §5.3.1 as the cross-arm plurality statement? | Yes — deterministic policy (1) against stochastic (2.7–5.9); never call it predictability |
| C14 | Objective denominator as a factor row: breadth only, or breadth + target reach? | Both, breadth as backbone — §10.7; and rule E7 in or out in the same breath |
| C15 | Is the λ sweep read twice (incentive **and** behavioural breadth), with the operating point selected as the largest plural λ? | Yes — one sweep, two readings, and it converts a declared value into a selected one |
| C16 | Declare the defender's Goal / Knowledge / Capability and MTDShield's absence in §5.2? | Yes to both — three clauses and one held row |
| C17 | Run the exploit-success pre-check before Fig. 5.9's caption is drafted? | Yes — one no-MTD cell decides whether a ≈ 370-run re-test is owed |
| C18 | Is the pure-interrupt pair picked out as a named contrast in §5.4.1? | Yes if the note is kept; otherwise cut the note. No new runs either way |

### 10.10 What changed in the tex on this pass

Comments and headings only; no prose, per the drafting pipeline.

- `float` loaded; ch5's 22 placeholder floats pinned `[H]`; §5.1, §5.2, §5.5
  reordered so the placeholder paragraph leads. Build clean, 82 pages.
- Chapter head: the word-and-page budget arithmetic, including the 14-headings-
  on-12-units fact.
- §5.1: what Table 5.1 is for and the body/appendix split; the "is this what a
  sensitivity analysis looks like" answer (OAT, the mapping's different status,
  the non-events gap).
- §5.2: the four missing factor-table obligations (objective denominator, the
  adaptive defender declared absent, the defender's half of the model, the run
  count as arithmetic with its ranking consequence); the full coverage map.
- §5.3: the three unplaced instruments and the C11 ruling; the disruption-axis
  answer and the plain-English replacement for "action mix"; §5.3.3 renamed
  **"A cost model and a memory"**, with the λ dial and the operating-point
  criterion, and blocker 6.
- §5.4: what the section is, against the reading it invites.
- ch6: the parked discussion points, each paired with its ch5 measurement, and
  the two orphaned notes flagged.
- ch7: what ch5 hands future work, each as a measured exclusion rather than a
  wish.
- `FLOATS.md`: the `[H]` placement convention and its revert condition.

---

## 11. Fourth pass (2026-09-09) — the ablation ladder, the results-fitting audit, and the register prefilled

Three asks from Marc, in the same exchange.

### 11.1 The ablation study — how the field does it, and where it folds in

**Convention.** A titled ablation subsection has a *local* precedent, which is
the strongest signal available: **Tay's evaluation chapter carries one**, in this
supervisor's own lineage, so the examiner has seen the form. He 2025 does the
same for a structural property of its defence. The journal corpus mostly does not
ablate at all, so there is no competing convention.

**The answer: no new section — §5.3.3 already *was* the ablation subsection, and
is now named and widened to be one.** It held two arms against their nulls; it
now holds all five, which is its natural content and costs no unit. Renamed
**"What each part of the model contributes"**. This also removed a duplication:
`tab:parameter-register` now carries the five optional capabilities as *one*
swept row pointing at §5.3.3, rather than five rows the ladder repeats.

**Why it earns a subsection on merit** (not on what it returns): §5.4 and §5.5
ask what the *defence* does; an ablation asks what a *component of the attacker*
contributes — a different question, with a different comparison (against a null,
not against no defence). Scattered across the strands, the ladder is never seen
as a ladder. In practice the five share one apparatus, so reporting them together
is cheaper in words than reporting them five times.

**The ladder**, most capable first, each rung switching one thing off at a
setting where the run is bit-identical: full model → less cost sensitivity → less
within-run learning → less outcome-conditioned routing (the verdict-blind arm,
which *does its work* as the control in §5.3.2 and is *reported* here as a rung,
cross-referenced, not measured twice) → less corpus-derived preference (uniform
weights) → **less objective conditioning (the aggregate envelope)**.

**The aggregate is the rung Marc was asking about, and placing it here fixes a
mis-filing.** `aggregate` is the **flow union** — the same corpus with the
objective partition switched off; the divergence record's own figure legend calls
it *unsegregated*. That makes it the null for the model's **central** claim, in
exactly the way the exponent at zero is the null for cost sensitivity. It
currently rides the hypothesis tree as characterisation (C-agg) rather than as an
ablation arm, and the tree's open ruling 5 — is the claim over four profiles or
five — is the same question from the other end. Reading it as a rung answers both.

> **Caveat, pre-registered rather than discovered:** the **divergence-to-
> aggregate** column may not be read as objective conditioning — its kill
> criterion fired at Spearman −1.0 against flow count, because `aggregate` is the
> union and a large class is close to the union by arithmetic. The *arm* is fine;
> that one *statistic* is not. Read the rung on breadth, coverage and blocked
> fraction.

**And one sentence that protects §5.4.2: the inherited attacker is not a rung.**
It is not this model with everything switched off — it is a different machine (a
deterministic policy over six verbs, with no net, no objective, and no routing
decision to condition), and no setting of any parameter reaches it. So a
cross-arm difference is **not attributable to any one component**, and the
chapter must not let the ladder and the cross-arm comparison read as one
instrument. Saying that once is what earns the cross-arm claim its correct and
narrower form — the two attackers depend on different substrate properties, which
is structural, not component-wise.

A placeholder `tab:ablation-ladder` is now in §5.3.3: the two rungs with a
continuous dial keep their figures, the three discrete rungs are rows.

### 11.2 The results-fitting audit — Marc's discipline, applied to this chapter

Marc's rule: *"you don't know what the results are… don't put things in knowing
the results, knowing that's going to be the strongest thing. Put things in that
are strong on merit, strong in practice and strong in convention."* Written into
the chapter head as a **standing test**:

> **Would this heading still be here if the result came out the other way?**

with the distinction that makes it workable rather than paralysing: **structure
is settled by convention and merit, content is left to the result.** §5.1 closing
by naming what its sweep selected is a *convention* (the corpus's strongest
sensitivity analyses feed forward); *which* parameter it names is the result, and
the chapter does not know it yet.

**Audit result — the skeleton passes.** Every section and subsection is justified
by a declared input of the model (§5.1.1–3), by the factor space (§5.2), by the
contribution being an attacker (§5.3), by the two metric families the field's own
taxonomy names (§5.4, §5.5), or by the comparison the thesis claims (§5.4.2).
None depends on which way a number falls.

**One justification failed, and is repaired.** §5.3.3 was argued on *"the measured
negatives are among the most credible things the work owns"* — precisely a
heading defended by a known outcome. It is now argued as the ablation subsection,
on convention and merit, and that survives whichever way every arm falls. The
same correction applies to §10.3's framing in the third pass: the ground for
reporting a declared capability is that **a declared capability that is never
measured is an assertion**, which holds flat, positive or negative.

**And a caption sweep followed, which is where the rule bit hardest.** Six ch5
captions stated a direction the chapter cannot yet state — and **four of them
came from sweeps this same handoff (§3.2) says must be re-run before they may be
reported at all**, so they were asserting results from a configuration the
chapter does not describe. Figures 5.1, 5.2, 5.4, 5.6, 5.9, 5.14 and Table 5.4
now say what the float is *for* and what would *count* as a finding, not what the
finding is. Apply the same test to any caption added later.

### 11.3 The floats ruling

Marc: *"I don't care how many floats exist — I just need as many as relevant and
reasonable and comprehensive enough."* So the corpus float **count** is not a
constraint on this chapter and nothing is cut to hit a norm. `FLOATS.md`'s list
is re-read as a **relevance ranking, not a cut quota**: a float that carries a
claim stays however many that makes; a float that only decorates a claim another
float already carries goes however few remain. This retires the page-budget half
of §10.2's word-budget answer; the unit arithmetic (14 headings on 12 units)
stands, because that is about prose.

### 11.4 The register, prefilled

**The twelve is real and enumerated** — A1–A12 in the §4.3 formalism brief §7.2 —
and the three Marc knows are the three declared *inputs* that are §5.1's
subsections, which is a different list. **Four of the twelve are already parameter
rows and are not repeated:** A1 exponential firing is the dwell-shape row, A4
success passthrough the success-treatment row, A9 synthetic pre-intrusion
structure the share row, A11 substrate invariants the mutation-cost and geometry
rows. The remaining eight have no number and form the third group. That is the
merge (C1) working: an assumption is a held row, and nothing is listed twice.

`tab:parameter-register` is now a real table, not a grey box — three row groups
(**Swept** 9, **Held** 7, **Assumed** 8), rows taken from the tracked registers
(§7.1 parameters, §7.2 assumptions) rather than typed from memory.

**The effect column is deliberately empty**, and this is the point rather than an
omission: it cannot be filled from the sweeps on record, because those ran at ten
seeds on the pre-restoration substrate with `random` as the only MTD condition,
and the failure-matrix sweep under the superseded timing regime. Any effect
number typed today would come from a configuration this chapter does not report.
It is filled by the re-run, by a generator.

**The per-value expansion stays in the appendix** — the four dwell anchors
individually and the nine failure-rule values are `app:sensitivity`'s, and
`tab:anchor-sensitivity` is already in that form. The body table is one row per
declared *family*, which is what keeps it to a page. It floats (`[htbp]`) rather
than being pinned, because a full-page table cannot be pinned; it lands on its own
page immediately after §5.1 opens.

---

## 12. Fifth pass (2026-09-09) — ratifications, and the register grounded in the formalism

Three short things, all of them Marc's rulings rather than findings.

### 12.1 The ablation folds in — ratified

No separate ablation section. §5.3.3 carries it, renamed, with `tab:ablation-ladder`
as a placeholder. Nothing further owed; §11.1 is the record.

### 12.2 The stale-numbers rule — a companion to the results-fitting test

Marc: *"you might think you know what's gonna happen but it might not actually
happen… I know you've got lots of numbers but they could be stale. So just do it
with the intent in mind that we're hypothesising and expanding the hypothesis."*

The standing test in §11.2 governs **structure**. This governs **numbers**, and
it is now at the chapter head beside it:

> **Every number appearing in a comment in this chapter is provenance, not a
> value.** It records what a record said when it was written, under a
> configuration this chapter may not report — ten seeds, the pre-restoration
> substrate, one MTD condition, a superseded timing regime, a mapping version
> since changed. It is there so a drafting session can find the study, never so
> it can be transcribed. **No number reaches the prose except from a tracked
> artefact via a generator**, re-derived at the configuration the chapter
> reports. The same applies to the *direction* of an effect: a comment saying a
> sweep was inert or a capability bought nothing records what was measured then,
> and the chapter states it only once it has been measured again.

This is the rule the §11.2 caption sweep was an instance of, generalised so it
does not have to be rediscovered each pass. It also settles how the third pass's
findings (§10.3, §10.4) should be read: the *instruments* named there are real
and placed on merit; the *magnitudes* quoted beside them are provenance.

**The posture it puts the chapter in, and it is the right one:** we have a model,
we know what it declares and what it was given, and these are the experiments
that interrogate it. What they return is a hypothesis, not a memory.

### 12.3 The register grounded in the formalism's terminology

Marc: *"the sensitivity analysis has to be grounded in at least the terminology
of the formalism."* Done, and it turned out to be the thing that makes §5.1 read
as one section rather than three unrelated worries.

`tab:parameter-register` gains a **symbol column carrying only symbols
`tab:gspn-notation` actually declares** — $\mu_p$, $\tau_p$, $\gamma$, $\delta$,
$z$, $F_v$, $\varphi$, $w_c$, $c$, $R$, $F_{\text{success}}$, $s$, $M_0$, $d$,
$v$ — so every swept quantity traces to its place in the formal definition, and
the notation table becomes the key this one reads from, which is what §8.4 of the
formalism brief always intended it for. The §5.1 comment's own symbols are
re-aligned to the tex (it had `phi` where the document has $\varphi$, and
`W(\tau_p)` where the declared quantity is $\mu_p$).

Rows are re-cut on the formalism's joints rather than on plain-English names, and
two of them changed meaning as a result: outcome-conditioned routing is $F_v$
against the identity (which is what the verdict-blind arm *is*), and objective
conditioning is $c$ — one class in place of four — which is the aggregate rung of
§11.1 stated in the formalism's own terms.

**Two rows carry no symbol, and the reason matters in each case:**

- **The optional modulators.** The history term has *no symbol in the document*,
  because §4.3 ruling **R3** (show the history-term slot in the formal
  definition) is still open. Using one here would reference a symbol the
  dissertation never defines — the same flag already standing against two marks
  in `tab:fidelity-verdict`. When R3 lands, this row gets its symbol and the flag
  clears. **This is now the third independent place R3 binds**, which is the
  argument for taking it.
- **The environment rows** (mutation cost, interval, geometry, horizon, run
  count). These are the simulator's and the experiment's, not the model's, so the
  formalism has no symbol for them by construction. That is the right answer, not
  a gap.

**Two honesty corrections made in the same pass.** The comment claimed the rows
were "from tracked registers, not typed"; they are *transcribed* from tracked
registers, which is not the same thing, and the declared values still owe a
generator pass against `data/ogasp/*.json`. And a **record inconsistency** is
flagged rather than resolved: the formalism brief's §7.1 writes the dwell anchors
as `μ_g` where its own notation table §8.4 and the tex both use `μ_p`. The tex is
taken as authoritative here; the brief wants correcting.

---

## 13. Supervisor scrutiny pass (2026-09-09) — four independent expert reviews

Marc asked for a supervisor-style review of the scaffold: *"what would an expert
in the field of MTD say to the structure we have cooked up?"* Four reviewers were
run in parallel, each on one dimension, each forming its own view **before**
reading §§10–12, and each marking its points as already known or new.

**The verdict in one line: the structure survives, the inference does not, and
three findings threaten claims rather than presentation.** The reviewers
converged on almost nothing the earlier passes had found — which is the useful
result. §§10–12 are strong on coverage, honesty and staleness; they were close to
silent on inference, on control adequacy, and on whether the instruments can
separate the effect from the apparatus.

### 13.1 The three findings that threaten a claim

Each is **verified against the code or the records in this session**, not taken
on the reviewer's word.

**(A) The central property's null was retired one layer down, and the deciding
arm is unrun.** `fig:aio-divergence` tests objective conditioning against a
**split-half** null, and the chapter's comments call this "the ONE property shown
to change an outcome". But `gasp_schema.md` §(g) records Marc's 2026-08-17 ruling
that the half-split null is **lenient and no longer the load-bearing check**; and
under the **size-matched label-shuffle** null at tactic-to-tactic resolution the
classes **do not separate beyond chance** (*p* = 0.49, *p* = 0.71, class sizes
19:7:7:5). L2 then hands the discrimination claim forward in terms — "the
load-bearing test for the L3/L4 evaluation phase". At L3,
`profile_divergence_findings.md` states that arm 3, the size-matched label-blind
control, **has not run** and is "the deciding arm". So the chapter discharges its
central property with the comparator L2 retired, while the arm that would settle
it is outstanding. The chapter already fences the divergence-to-`aggregate`
column for size confounding and leaves the between-profile figure unfenced.
**This is the chapter's largest exposure.** Either arm 3 runs, or Fig. 5.6 claims
only "profiles differ by more than seed noise" and states L2's strict-null
verdict beside it.

**(B) The headline mechanism may be an artefact of the disruption wiring.**
§5.4.2's mechanism — network layer severs position, application layer barely
reaches this attacker — is measured by `disruption_wiring.md` §(d) *as an
instrumentation asymmetry*: per firing, network-class delivers 0.92–1.00 of its
native yield to the movement arm, application-class 0.67–0.83; the diversity
family loses **89–97 %** of its exploit-blocking windows there because
exploitation is uninterruptible on that arm (D-35, a declared **mapping policy**,
not a defence property). The counterfactual in the same record is the sharp part:
make dwell-only places application-immune and the diversity pair retains
**0.17–0.18** of its yield — so roughly four-fifths of "what application-layer
MTD does to this attacker" arrives through the `DWELL` sentinel, which exists
because of how the movement layer presents its clock. Nothing in the scaffold
lets a reader separate the mechanism from the apparatus. **Owed:** per-firing
yield ratios and the DWELL-channel share reported beside the suppression figures;
D-35 and D-36 as declared rows in `tab:factors-fixed`; a robustness arm
(dwell-immune or per-firing-normalised).

**(C) The defence is near-periodic, so the property MTD is named for is not
instantiated — and ch2 says otherwise.** The default regime draws
`expon.rvs(loc=200, scale=0.5)`. Measured this session over 200 000 draws:
**mean 200.5 s, sd 0.50, CV ≈ 0.0025**, against CV ≈ 1.0 for a true exponential.
Mutations arrive on a clock. Ch2 tells the reader "the interval between
deployments is drawn exponentially", which is misleading under the default
regime, and the register's assumed row *nothing is known of the defence's
schedule* is carrying a schedule that is trivially learnable — which is
precisely Jalowski's "learn mutation patterns over time". `--timing-regime
exponential` already exists. **Owed:** one sensitivity arm at true Exp(μ), the
quasi-periodic regime declared in `tab:factors-fixed`, and the ch2 sentence
corrected.

### 13.2 Inference — the gap §§10–12 missed entirely

- **No multiplicity control anywhere in the chapter.** Ruling the hypothesis tree
  "a planning artefact, do not surface it" removed the α-spending, the
  pre-registration and the failure dispositions along with the AND/OR gating. The
  chapter reports roughly 160 leaf comparisons with no stated family-wise error
  rate, and its only decision rule is `tab:eff-conditions`'s "overlapping
  intervals are indistinguishable" — which is not a test. **Owed:** four
  sentences in §5.2 (estimation-first, unpaired per D-29, Holm within each
  declared family, effect floors declared before the run), and the tree's leaf
  table as an appendix. Multiplicity control can be surfaced without surfacing
  the gating.
- **The cross-arm rank statistic is structurally unstable, not merely
  underpowered.** ρ is computed over cells the project's own power arithmetic
  says cannot be ranked, which is a mechanical explanation for −0.893 → −0.071
  that owes nothing to the substrate restoration — and would not be repaired by
  E2-R. Two reviewers reached this independently. **Owed:** make the family-level
  contrast (severance vs surface re-roll, per arm) the object with Cliff's δ and
  intervals; keep ρ as a companion only.
- **Seed budget derived from the wrong cells.** The 18/22/190/329 arithmetic was
  computed by normal approximation on *unopposed* breadth and is being spent on
  *defended* cells the same document calls floor-pinned and non-normal.
- **The adaptivity figure has an uncontrolled time confound.** Steps after a
  mutation are also later in the campaign, and stage advances monotonically, so
  drift and response are collinear. The verdict-blind arm is a different
  trajectory from step one, so it is a between-arm comparison, not a matched
  control. The correct null is free: placebo mutation timestamps drawn from the
  same interval distribution in the no-defence arm.
- **Capability sweeps read in the degenerate region.** Under network-layer
  defence breadth sits near 0.6 hosts, so the λ and learning sweeps are read
  where the outcome has no headroom — the same ceiling logic as blocker 6,
  generalised.

### 13.3 Structure — the shape holds, three placements do not

- **The funnel breaks.** The reader crosses the undefended/defended boundary
  three times before the evaluation proper: §5.3.2 runs a defence set, §5.3.3
  runs conditions again, §5.4 runs defences a third time. And §5.3.2 as edited in
  §10 now delivers the severance/re-roll mechanism that §5.4.2's own comment says
  is "the sentence this subsection exists to earn" — whichever lands first makes
  the other a restatement.
- **The ablation is placed against the precedent cited for it.** §11.1 justified
  §5.3.3 on Tay's evaluation chapter carrying an ablation subsection — but Tay's
  is the **final** results subsection, after the headline, and He's structural
  analysis likewise follows its evaluation. The convention argues for placing it
  after §5.4, not before. Either move it or justify the position on other
  grounds.
- **Three tables of "what was held", with overlapping and contradicting rows.**
  `tab:parameter-register` says geometry is held so every condition runs on one
  terrain; `tab:factors-varied` lists network scale and density as varied; and no
  section reports a scale or density axis (V-gen/E4 unrun). Two reviewers found
  this independently. The environment rows should leave the register — the
  comment already concedes they are the simulator's, not the model's.
- Smaller: no chapter-opening placeholder exists while the roadmap is assigned to
  §5.2, so §5.1 runs before the reader is told what the chapter does; §5.1.2 is a
  half-unit heading the ledger's own fold rule forbids; `subsec:eff-lineage` is
  the only §5.4 subsection not measured against the no-defence reference and
  belongs in the discussion; fifteen-plus bespoke instruments have no structural
  home for their definitions.

### 13.4 Measurement — five corrections

- **The comparability boundary as planned is two-valued and therefore wrong.** It
  is three-valued: cross-paper invalid; cross-arm valid **only** for counts,
  fractions and per-host ratios (test-enforced to carry no time field);
  within-arm cross-configuration valid. As drafted the chapter then violates it
  twice — `fig:eff-delay` puts a time axis across arms, and the spacing
  observation recommended in §10.3(c) is time-denominated across arms with the
  cross-clock caveat missing.
- **The coverage map counts one instrument twice.** Reconfiguration occupancy is
  claimed for both defender-side *resource spent* and *network-state change
  (efficiency)*; there is no system-performance-overhead measure at all. Honest
  is **five of ten**, not six, and occupancy is a **floor** (three named
  undercounts) which Fig. 5.14's axis does not say.
- **The disengagement frontier plots the half that does not move** — the
  conditional mean, while the censoring fraction is what moves with the defence,
  over an axis whose right half is pinned at the horizon.
- **Jalowski: the wrong concession is volunteered.** Conceding guideline 3 is
  cheap and most of the corpus fails it too. The bespoke attacker-side suite
  fails 1, 2 and 4 — computable only from the model's own token trace, evaluating
  no other scheme, and not in common terminology. The defence is the one §5.3's
  restructure already built: those are **model-validation instruments, not MTD
  evaluation metrics**, and only §5.4–5.5 are offered against the guidelines.
- **A factual error in a caption.** `fig:aio-coverage` says the inherited
  attacker runs "a fixed loop over three activities". It has **six** verbs
  (`predictability.md` R1 derives the transition table from the code). Also,
  structural zeros should be a table row with the reason, not a reference line
  drawn beside measured values.

### 13.5 What the reviewers agreed was right

Merging setup and results (corpus-ratified); the metric-family axis as the
organiser for an attacker contribution; effectiveness before efficiency;
deferring every verdict to ch6; the coverage map as the chapter's best defence;
the pruning rule that makes breadth the denominator; effective behavioural
breadth as the best-built instrument in the project; blocked fraction sitting
correctly in Brown's cell.

### 13.6 Rulings owed from this pass

| # | Question | Recommendation |
|---|---|---|
| C19 | Run divergence arm 3 (size-matched label-blind), or narrow Fig. 5.6's claim? | Run it — it is the deciding arm for the chapter's central property and L2 handed the claim here explicitly |
| C20 | Report per-firing yields and the DWELL-channel share beside the suppression figures? | Yes, and declare D-35/D-36 — otherwise the headline mechanism is indistinguishable from the apparatus |
| C21 | Add a true-exponential timing arm, and correct ch2's sentence? | Yes to both; the regime flag already exists and the ch2 claim is currently wrong |
| C22 | State the inferential model and multiplicity control in §5.2? | Yes — four sentences, plus effect floors (this finally forces C7) |
| C23 | Make the family contrast the cross-arm object, demoting ρ to a companion? | Yes — ρ over non-separable cells is a statistic over noise |
| C24 | Move the ablation after §5.4, or re-justify its position? | Re-justify or move; the precedent cited in §11.1 points the other way |
| C25 | Evict the environment rows from `tab:parameter-register`, and fix the geometry contradiction? | Yes — two reviewers found it independently, and it is a self-contradiction on the page |
| C26 | Placebo-mutation control for the adaptivity figure? | Yes — it is free, and without it property 4 is unevidenced |
| C27 | State the comparability boundary three-valued, and re-cut `fig:eff-delay`? | Yes — as drafted the chapter breaks its own rule twice |
| C28 | Concede Jalowski 1, 2, 4 for the attacker-side suite on the model-validation ground? | Yes — the restructure already earned this defence; the prose should collect it |

### 13.7 Method note

Four reviewers, one dimension each (chapter shape; experimental validity; metrics
and measurement; the defence side and threat model), each read the scaffold and
its supporting records cold and only then checked itself against §§10–12. Three
of the four reported that essentially every point was new. The exercise's value
was not in re-finding known gaps but in the dimension the earlier passes had no
reviewer for: **whether the instruments can separate the effect from the
apparatus.** Findings A, B and C all live there.

---

## 14. Marc's rulings on the scrutiny pass (2026-09-09), and one correction owed to him

### 14.1 CORRECTION — §13.1(A) was over-compressed, and Marc caught it

Marc: *"I'm pretty sure it does produce meaningful behaviour at runtime, because
if you look at the runs, the runs are a little different."* **He is right, and
§13.1(A) as written conflated two different measurements at two different
layers.** The record, checked:

- **At runtime (L3), the profiles separate decisively.** P1 in
  `profile_divergence_findings.md` held "by 40–110×": between-class visit-stream
  JSDs of 0.081–0.237 against null ceilings ≤ 0.0022. In that record's own words,
  "profile identity conditions the runtime visit distribution far above seed
  noise". There is no question that the runs differ.
- **The unsettled question is attribution, not existence.** What has not run is
  the size-matched label-blind control (arm 3), which is "the only instrument
  that can separate conditioning from corpus size" — the profiles carry 19, 8, 6
  and 5 flows. And the *corpus-level* (L2) check is what failed the size-matched
  null at *p* = 0.49 / 0.71; that is a statement about the partition's structure,
  not about runtime behaviour.

**So the honest form of the exposure is much narrower:** the runtime effect is
large and real; what is unproven is that it is *objective conditioning* rather
than *corpus size*. That is still worth closing — it is the same confound that
fired the kill criterion on the divergence-to-`aggregate` column, and the same
one that makes the aggregate a comparison rather than a clean ablation null
(§13.2, reviewer 1's point 4) — but it is one arm, not a threatened claim.
**C19 is re-graded from claim-threatening to attribution-closing.**

### 14.2 The wiring (§13.1(B)) — Marc's ruling, and the question inside it

**Ruled: the finding does not stand as an objection.** Marc: disruption has to be
implemented *somehow*; this substrate models it directly and indirectly through
component interaction; the model is inherited and has been embraced by five or so
papers. Modelling disruption in a particular way is not an error, and the chapter
will not present it as one.

**Also ruled — a register constraint that applies chapter-wide.** Marc:
*"you're going into technical details which somebody reading this is not going to
understand… we're just trying to model something using a simulator."* **No
chapter-5 prose descends into codebase internals** — no `DWELL` sentinel, no
`curr_process`, no disposition numbers, no `charge_time`. Where a boundary must
be stated it is stated in modelling language ("application-layer defence reaches
the two attackers unequally, because…"), and the mechanism detail stays in the
implementation record. This supersedes the phrasing recommended in §13.1(B).

**The live question Marc raised, answered from the record.** *"EXPLOIT_VULN
uninterruptible — that's a big one, I think it should be interruptible if there's
an MTD interrupt. But it was designed that way because if you're running exploit
you're in flight. Was that a design choice?"*

Run against the intent spec, per the bug-vs-design procedure:

- **It is a design choice, and it is ours, not the lineage's.** It is already
  classified in `intent_conformance_audit.md` as **D-35, mapping policy — not
  documented-nowhere**, so it is not a candidate bug. It is the direct declared
  consequence of **S3-R** (the movement layer supplies every unit of the
  attacker's time, so the substrate's per-vulnerability timing loop and its
  yields are declined). S3-R was ruled deliberately.
- **But it diverges from documented lineage intent, and that is worth knowing.**
  IS-INT-05 has application-layer MTD *interrupting* attack actions with the
  adversary restarting from phase 1; IS-INT-06 gives each action a limited number
  of attempts with an interruption threshold. So the lineage's intent is that
  exploitation *is* interruptible. No lineage paper specifies *how many* interrupt
  windows an attempt offers, which is why this is a divergence rather than a
  conformance failure. **Marc's instinct matches the documented intent; the
  current behaviour is a consequence of our own timing ruling.**
- **Three dispositions are on record, and this is Marc's call.** (a) record it as
  a comparability boundary — zero code, zero goldens (the record's own
  recommendation); (b) divide the supplied duration across the vulnerability loop
  so the attempt offers the same number of windows on both arms — restores
  cross-arm parity on exactly the channel that is the diversity family's *entire*
  effect, but it is a substrate timing change that moves every movement golden and
  partly re-opens S3-R; (c) keep and say nothing — not recommended.

### 14.3 Timing stochasticity (§13.1(C)) — ruled INTO the experiment

Marc: *"we are moving roughly every 200 seconds. We can add more stochasticity.
That's fine. It can be part of the experimentation."* **So this is not a
limitation to declare but a factor to vary** — the timing regime joins
`tab:factors-varied` with two levels (the quasi-periodic default and true
Exp(μ)), and `--timing-regime exponential` already exists to run it. The ch2
sentence still needs correcting either way, since it currently describes the
regime the default does not use. **C21 upgraded: a factor, not a disclosure.**

### 14.4 The `simultaneous` scheme — Marc's realism objection

Marc: *"how do you run many attack-surface changes at the same time without
collisions? If you're changing all the hosts' IP addresses at once, when does the
state become stable? You'd have competing writes on the same resources, so you'd
need some lock or you'd gridlock. It's a bit of 'let's do everything at once' and
it's not really realistic."*

**Partly answered by the substrate, and partly not.** Contention *is* modelled:
two mechanisms rewriting the same resource layer cannot operate concurrently
(Zhang), and the disruption ledger carries a suspended-mutation tally — so the
lock exists and the queue is counted. What is *not* answered is his realism point
about a defender that reconfigures everything at once, nor the measurement
problem reviewer 4 raised: `simultaneous` fires roughly **150 mutations per run
against 75** at the same nominal interval, with 38 suspensions, so putting it on
one axis beside single mechanisms ranks **dose, not strategy**.

**Recommendation:** either drop `simultaneous` from the reported conditions on
the realism ground Marc states — which is a defensible modelling judgement and
costs nothing — or keep it and report it per firing. What is not available is
ranking it against single mechanisms on total effect.

### 14.5 Marc's other rulings, briefly

- **Three unrun mechanisms:** run them. *"We'll pull the numbers and we'll find
  out."*
- **Efficiency metric:** a better one than reconfiguration occupancy is wanted;
  deferred to when the section is drafted.
- **Defender threat model:** declare it (C16 confirmed).
- **The headline:** *"we'll find out what the headline is in due course — you can
  put a note in saying this is what we're hypothesising."* So §5.4.2 carries a
  stated hypothesis, not an asserted mechanism.
- **The 0.721/0.725 equivalence** (reviewer 4's point 4), restated plainly since
  the original was opaque: the claim that the two network-layer mechanisms are
  one effect rests on their numbers being close at six seeds on one profile. Two
  numbers being close is not evidence that they are the same; showing sameness
  needs a stated margin ("within X of each other counts as equivalent") declared
  before looking. Cheap to fix, and the source record already says it does not
  support a significance claim.

## 15. Marc's horizon question — the answer he asked for

*"We might have to run the simulator a bit longer for the movement attacker,
because it runs about four times slower than the original attacker… maybe 60 000
seconds on the clock. We measure MTTC, ASR, network compromise ratio of 0.8
depending on the objective. Food for thought — get back to me."*

**The instinct is right, and there is a stronger version of it already built into
the substrate.**

### 15.1 Why this dissolves several problems at once

The degenerate operating region is not a property of the attacker; it is an
artefact of **pairing an inherited 15 000 s horizon with an attacker that takes
roughly four times as long per unit of progress.** Everything downstream of that
pairing is a workaround: breadth as the denominator instead of objective
achievement, the "no ASR at the operating interval" rule, the pruning-rule
paragraph, and the capability sweeps being read where the outcome has no
headroom. Fix the horizon and those are choices again rather than necessities —
and the three field-standard metrics the coverage map currently concedes
(**MTTC, ASR, network compromise ratio**) come back.

### 15.2 The stronger version: report at a compromise checkpoint

Marc's "network compromise ratio of 0.8" is not an aside — **it is the inherited
idiom, and the substrate already implements it.**
`evaluation.py::evaluation_result_by_compromise_checkpoint` reports the metric
suite at compromise checkpoints `[0.1 … 0.9]` of the host fleet, and the
lineage's own golden headline is taken at **0.25**. So the canonical question in
this simulator is not *what did the attacker achieve by time T*, it is *how long
did it take to reach X % of the fleet* — which is **non-degenerate by
construction wherever X is reached, and censored where it is not**, and censoring
is data rather than a missing result.

**Recommendation: checkpoint-denominated reporting as the primary, horizon
extension as the enabler.** Extend the horizon far enough that a meaningful
checkpoint is reached in a healthy fraction of runs, then report at the
checkpoint rather than at the horizon.

### 15.3 What it costs, and the one trap

- **Compute is not the constraint.** A movement run is ≈ 0.2 s at 15 000 s and
  the full matrix at 100 seeds is ≈ 1.5–2 h on six workers; at 60 000 s that is
  roughly 6–8 h if cost scales linearly. Overnight, once.
- **THE TRAP, and it is the reason not to just quadruple the horizon and move
  on:** at a fixed mutation interval, a 4× longer run is also **4× more
  mutations** — so "longer horizon" is silently "more defence". Horizon and
  defence dose are confounded unless mutations-per-run is held or effects are
  reported per firing. This is the same defect as the `simultaneous` dose problem
  in §14.4, arriving from a different direction.
- **E5 must stay at the lineage's configuration.** The prior-models re-run is the
  comparability bridge; if its horizon moves, the comparison breaks. So horizon
  becomes a **factor with two levels**, not a global change.
- **It may move the Gate 0 result.** The targeted objective was non-degenerate at
  layer 1 on the aggregate envelope only, measured at 15 000 s. At a longer
  horizon more profiles may reach it, which would re-open C14 favourably.

**Owed before this is taken:** a cost curve at 2–3 horizons (the "no silent caps"
convention), and a decision on which checkpoint is the headline — 0.25 keeps the
lineage bridge, 0.8 is a much stronger claim and will be censored far more often.

---

## 16. The register re-cut, and where each class of thing lives (2026-09-13)

Marc walked `tab:parameter-register` row by row and found what the table's own
reviewers half-found in §13.3: it carries **four different kinds of thing** under
one honesty banner, and "held" reads as *inherited* when half the group is
model-side. **C1 is reversed** on separation of concerns — Marc's ruling, his
words: *"separation of concerns should be considered."* The four classes, the
convention each has in the literature now held under `docs/sources/methodology/`,
and the ruled home of each:

| Class | Rows it covers today | Convention | Ruled home |
|---|---|---|---|
| **Free inputs of the formal definition** | $\mu_p$, $\tau_p$ shape, $\gamma$, $\delta$, $z$, $\varphi$; $R$ named as unswept | ten Broeke's input table (nominal, range, origin) + extended OFAT; Pianosi/Saltelli purposes **screening** and **ranking**; Sargent operational validation + ceiling | `tab:parameter-register`, ~7 rows. **This is what the sensitivity analysis is.** Not three chosen of twelve: all the definition's free parameters, as ten Broeke prescribes |
| **Ablation arms** | $F_v$ identity, uniform $w_c$, unsegregated $c$, cost/learning modulators | Journal MTD corpus does not ablate; Tay's subsection served an RL agent | **§5.3.3 dropped** (Marc: "persuaded by the convention in these journals"). Aggregate envelope stays as a fifth attacker arm / summary-table row in §5.3.1; verdict-blind arm stays as the §5.3.2 control; modulators held at defaults as `tab:factors-fixed` rows. **Consequence flagged, not yet confirmed by Marc:** fidelity-verdict properties 6 and 7 become *implemented, not evidenced*; the R3 dependency leaves ch5 |
| **Environment / experimental factors** | mutation cost, interval, timing regime, network, horizon, run count | Reti's two tables; Anderson's failure (held defaults unstated); Kim (fix by citation, repeat in captions) | `tab:factors-varied` / `tab:factors-fixed` in §5.2 only (C25). Horizon (§15) and timing regime (§14.3) are **varied** factors. `retrace_sinks` runs on every reported configuration (an assumption, A10, per Marc 2026-09-13); one `tab:factors-fixed` row declares it |
| **Modelling assumptions** | the twelve of the §4.3 brief §7.2 | ODD: assumptions live in the model description at the submodel; Sargent conceptual-model validation; corpus §g limitations paired with future work | **ch4 prose at the symbol each constrains — APPLIED 2026-09-13.** A1, A2, A3, A9 were already stated; A4, A5, A6, A7, A8, A10, A11, A12 inserted on Marc's ratification of a fourteen-item proposal (dated trails at each anchor). "Three assumptions" → "three inputs" at the §4.4 opening |

**Marc's sharpening of what §5.1 is.** The three inputs were *derived and argued*,
not fitted: the sweep is Madan's substitute for estimation, a check that the
conclusions survive the declared values being wrong, never a calibration. The
placement criterion that follows is the only one needed: an assumption *with a
number attached* can be moved and is a §5.1 row; one *without* is a ch4 sentence.

**§5.1 collapses to one section, ~1 unit, no subsections** (was 3 units, three
subsections, four figures — three of them of non-events). Preamble: purpose
(screening + ranking), method (OFAT over formalism-derived bands, corner check on
the influential pair, no global claim), ceiling (Sargent). Then the ~7-row table,
**one** figure (the parameter that moved), and a closing paragraph naming the
selection for §5.2 to pick up (C7b). Shape-swap and mapping-swap are rows with
appendix pointers, not subsections. With §5.3.3 gone the chapter has **10 headings
on 12 units** — under budget for the first time.

**What the chapter is, in one sentence (the roadmap).** Chapter 4 declares the
model. Chapter 5 checks the declared numbers do not carry the conclusions, declares
the experiment, and runs it: what the attacker does unopposed, what the defences do
to it, and what that costs.

**Record correction attempted and withdrawn in the same pass.** The §4.3 brief's
A6 ("a mutation during a dwell-only place is felt in cost, not routing") was first
read as contradicting `boundary_attacker_defender_channels.md` D-21 ("mid-dwell
interrupts are read as a failure verdict"). Marc's framing and the code say the
brief was right: a dwell-only place exercises no capability, the interrupt costs
time, and `movement/attacker.py` routes the dwell-only branch on `VERDICT_NONE`
whether or not the dwell was interrupted. D-21's wording is the interrupt gate's
exposure accounting, not a routing claim. Brief and ch4 sentence both carry the
cost-only framing. Lesson for the record: a "read as failure" in a trace is not
the same object as the verdict the token routes on.

**Retrace, ruled (Marc, 2026-09-13).** `retrace_sinks` was meant as an input but
is run on every reported configuration; it is therefore an *assumption the work
runs with* (A10, now in ch4 §4.4.1), not a factor. The driver default stays off for
golden reproducibility. One row in `tab:factors-fixed` declares it; nothing to
sweep.

**Owed (next session, tex):** (i) re-cut `tab:parameter-register` to the free
inputs and move its environment rows to §5.2; (ii) collapse §5.1 to one section
and retire `subsec:sens-dwell-times`, `subsec:sens-mapping`, `subsec:sens-failure`
(re-point ch4's forward refs to `sec:sensitivity`); (iii) drop §5.3.3 once Marc
confirms the fidelity-table consequence, moving the aggregate row to
`tab:unopposed-summary` and the modulator defaults to `tab:factors-fixed`;
(iv) add the retrace row to `tab:factors-fixed`. Ruling numbers: **C29** (C1
reversed), **C30** (§5.1 collapse), **C31** (§5.3.3 drop + fidelity consequence —
*confirmation owed*).

---

## 17. Headings — the convention, and the set Marc accepted (2026-09-13)

Marc: some subsection headings read *"second rate, over-descriptive, not
standardised"* ("What each part of the model contributes" as the example). The
corpus's form is consistent: **a results heading is a noun phrase naming the
quantity measured, the factor varied, or the object evaluated — two to five words,
no verb, no claim.** Brown names the metric (*Attack actions blocked*); He names
property-of-object (*Effectiveness of adversarial attacks*, *Efficiency of
generating MTD-AD models*); Ho and Hong name the factor (*Impact of MTD interval*,
*Varying the number of hosts*); Zhang and Tay name the object (*Single MTD
evaluation*, *Baseline evaluation*, *Ablation studies*). Setup sections are
*Experiment(al) setup* wherever titled (He, Reti, Ho); *Simulation setup* (Hong).
The claim goes in the section's first sentence — Marc's own heading rule.

Accepted set (applied to the tex the same day; labels unchanged so refs stand):

| Was | Now | Form |
|---|---|---|
| Experiments | **Evaluation** | Tay, Zhang; the third sub-question's word |
| 5.1 Sensitivity analysis | Sensitivity analysis | Outkin |
| 5.2 Experimental dimensions | **Experimental setup** | He, Reti, Ho |
| 5.3 The attacker model in operation | **APT attacker behaviour** | He's property-of-object; APT visible |
| 5.3.1 Unopposed behaviour | **Without defence** | Brown's "None" condition as label |
| 5.3.2 Response to disruption | **Under defence** | the paired condition |
| 5.3.3 What each part of the model contributes | *removed* (C31) | — |
| 5.4 Effectiveness | **Defence effectiveness** | Cho's axis, object named |
| 5.4.1 Under defence | **Mechanisms and schemes** | Zhang's single/multiple, factor named |
| 5.4.2 Across the two attackers | **Attacker comparison** | object of the claim, no claim in it |
| 5.4.3 The prior models re-run | **Prior evaluations** | Masud's comparison form; not "replication" |
| 5.5 Efficiency | **Defence efficiency** | pairs with 5.4 |

Audit against Marc's traps: sentence case; APT the only acronym; every heading
two or three words; no frame repeated beyond a pair. Chapter 4 is **not** retitled
— a one-sentence signpost in its opening roadmap is Marc's (slot comment at
`ch:attacker-model`). Stage 2 — the float-by-float audit, convention first — follows
as §18.

---

## 18. The placeholder audit — convention first, then reconciled (2026-09-13, APPLIED)

**Read this section, §16 and §17 first if you are working on chapter 5.** With
the FLOAT CONTRACT comment at the chapter head of the tex and `FLOATS.md`, they
are the retrievable context for the chapter's structure and every float in it.

### 18.1 The baseline the corpus sets (figure_table_conventions.md §b, §e, §f, §g; evaluation_conventions.md §c)

Setup is two parameter-genre tables (symbol, description, value; levels as sets,
ranges as intervals; inherited values and version pins in a footnote, once). A
sweep is a marker-per-series line chart — x the parameter, y the metric with its
interval, series a second factor at 2–4 levels — **one figure per parameter that
moved**, and a band-ends-against-centre table for those that did not. A
comparison across conditions is grouped bars with no defence as the origin. A
two-metric outcome space is a scatter. Stacked bars only with values printed.
Multi-panel figures: lettered panels, one caption, one legend. Results tables:
booktabs, grouped headers, right-aligned fixed decimals, intervals, best marked.
One colour per condition holds across the chapter. The named anti-pattern is
Brown's: mechanism-combination labels rendered illegibly small.

### 18.2 Section by section — convention → had → reconciled (all applied to the tex)

| § | Convention wants | Had | Now |
|---|---|---|---|
| 5.1 | input table + one figure per mover; inert → appendix band-ends table | 26-row register; 4 figures, 3 of non-events / swaps | 7-row `tab:parameter-register`; `fig:sens-dwell-anchor` as the mover's slot; three figures removed; **App. C.3 `tab:decay-sensitivity` added** |
| 5.2 | Reti's two parameter tables | two tables, rows partly stale | rows re-cut (varied: arm, condition, tempo, timing regime, horizon, objective; fixed: geometry, tolerance-set runs, versions in footnote, penalty, retrace, modulators, adaptive selector, schedule); scale/density leave unless E4 is run; capability arms gone |
| 5.3.1 | progression figure + summary table | coverage line; divergence points vs shaded band; table | `fig:aio-coverage` two panels (coverage; **opening variety**, the ruled exhibit); `fig:aio-divergence` a printed-value 4 × 4 matrix (no aggregate row — size-confounded); table + aggregate and inherited rows, entropy footnoted |
| 5.3.2 | grouped bars, control beside, lettered panels | under-specified two-panel | 2 × 2 mechanism × tempo, control beside, legend once |
| 5.4.1 | grouped bars from the no-defence origin + numbers table | one figure, table marked cut | two lettered panels (singles / schemes); table kept, + delay column with censoring |
| 5.4.2 | grouped bars, series = arm; results table | figure; survival curves; orderings table | figure with panel split and hatch; **`fig:eff-delay` removed** (delay is a table column; Zhang-form bars if checkpoint time becomes primary); orderings table unchanged |
| 5.4.3 | comparison table (Masud §4.6) | small-multiple claim panels | **`fig:eff-lineage` → `tab:eff-lineage`** |
| 5.5 | scatter; stacked bars with values printed; ledger table | all three, one marked cut | all three kept; frontier markers labelled; decomposition captioned as attacker-model-only (D-37) |

Totals: **8 figures + 8 tables** in the body (from 15 + 8), plus one appendix
table. Placeholder box text is renumbered to the new sequence (Fig. 5.1–5.8,
Tab. 5.1–5.8, Tab. C.3) and matches the build.

### 18.3 What rides on Marc's rulings, still open

- **C31** — the ablation removal's consequence: the fidelity verdict's marks for
  cost sensitivity and learning drop to *implemented, not evidenced*. Removal
  applied; consequence not yet confirmed.
- **Stealth (axis-5) column** in `tab:unopposed-summary` — the spacing contrast
  as an observation with the badge blank (handoff §10.3(c)). Not added.
- **Horizon / checkpoint** (§15) — decides whether a Zhang-form time-to-checkpoint
  bar chart re-enters §5.4.2, and fixes the configuration the §5.1 re-run must
  share.

### 18.4 Owed before numbers

Generator pass for `tab:parameter-register` against `data/ogasp/*.json`; the two
sweeps re-run at the reported configuration (fills the effect column and
`tab:decay-sensitivity`); the prose slots (§5.1 preamble, chapter opening, ch4
signpost sentence, App. C.3 framing paragraph) — all Marc's dictation.

---

## 19. Marc's cold read of §5.1 (2026-09-13) — what the section owes the reader before it owes numbers

Marc read the collapsed §5.1 as drafted (§16, C30 applied) and found it "cut and
dry" but vague: *where did the decay come from, what is the rule kernel, what is
forward/backward, the symbols feel made up, what is Figure 5.1 for, what goes in
the effect column, what are the appendix items for.* Every one of those is
answered in the record; none is answered on the page. The cause is locatable:
the 2026-09-08 front-loading ruling cut the kernel-value, floor and example
sentences from §4.4.3, so a reader now meets $\gamma$, $\delta$, $z$ and $R$ for
the first time in `tab:gspn-notation` and then in Table 5.1 with only a
two-word name each. The symbols are the formalism's (§4.3 binds $\mu_p$, $\tau_p$,
$\varphi$, $F_{\text{failure}} = R \cdot d$; App. B.6 binds $\gamma$, $\delta$, $z$),
so the order — ch4 declares, §5.1 prices — is right and is ten Broeke's input
table. What is missing is one clause of *meaning* per row, and it belongs in the
table's Quantity column, not in prose the ledger cannot afford.

**The seven rows in plain words** (for the Quantity column and the preamble; every
value below is the record's, not a new derivation):

| Row | What it is, in one clause | Where it came from | What the record already says |
|---|---|---|---|
| $\mu_p$ | the four dwell anchors the 15 tactic times resolve onto: scan 35 s and exploit 4.5 s priced from MTDSim's own action costs; low-and-slow 45 s (10× exploit) and objective 36 s (8× exploit) declared | `tab:dwell-anchors`, App. B.4 | only the low-and-slow anchor moves an outcome (7.82 → 4.56 → 1.78 hosts across ×0.25..×4, MTD off); the other three inert at both band ends (`rate_feasibility_study.md` §10) |
| $\tau_p$ | the shape of the draw around each mean: exponential, on the supervisor's direction, against a same-mean Erlang-4 | `stochastic_timing_design.md` §3 | inert everywhere except the long-dwell corner under mutation (stealth ×4, 200 s), where the faithful shape is *worse* for the attacker (App. C.2 table) |
| $\gamma$ | how much a failure-routed jump *forward* across two lifecycle stages is suppressed (the factor is $\gamma^{\Delta-1}$: adjacent = 1, two stages = 0.25, three = 0.0625) | `lifecycle_consensus.json`; the encoding of Marc's "far jumps close to or exactly zero" | 36 % largest shift, on the forced-total mapping only (`weight_sensitivity_study.md` §6.2, fixed-dwell regime) |
| $\delta$ | the same suppression for a *fallback backward* after a failure (two stages back = 0.25) — the persistence ruling: a deep attacker does not return to external reconnaissance | same; re-cut 0.5 → 0.25 on 2026-07-28 | the most influential of the three (101 % on actions-per-host, forced-total mapping); band re-cut 0.25–0.75 → 0.1–0.5 *after* the study, so 0.1 is unswept until the re-run |
| $z$ | the floor: a distance factor below it reads as exactly zero, which is what makes "exactly zero" representable for the three-stage corners | same | zero sensitivity **by structure**: no profile net carries a three-stage edge, so nothing for the floor to act on (§6.1); report it as such, not as "tested and small" |
| $\varphi$ | which tactic dispatches which simulator verb; partial (seven dwell-only) against the forced-total alternative | `controller_mapping_v2.md`, App. B.5/B.7 | a swap, not a band: the forced-total mapping ran a tightly ordered machine in an unordered way and under-performed (App. B.7) |
| $R$ | the nine failure rules A–I — the gates and dampers (initial access failed → foothold-dependent 0.02; recon failed → deep 0.05 …) and the forward / lateral / backward ladder (0.3–0.35 / 0.7 / 0.9) | `outcome_rules.json`; adversarially reviewed R0–R4 | **not swept**: each is a single argued magnitude, and the declared-value precedent's rule is *argument for single magnitudes, sweep for parameterised terms*. Listed so no declared quantity is absent (conventions §c) |

Marc's own intuition for $\gamma$/$\delta$ was the right one, one direction
flipped: *small* decay suppresses far jumps hard (the things meant to be near
impossible stay so), *large* decay lets them happen; the floor is what does the
"exactly zero" for the corners. The band is bracketed either side of the declared
0.25 for that reason.

**Figure 5.1 is the corpus's standard sensitivity figure, and nothing more**
(conventions §c: x = the swept input across its band, y = the outcome, series =
a second factor at two to four levels, one figure per input that moved —
Anderson, Hong, Carroll). Its job is to show the *form* of the one relationship
that exists (ten Broeke: OFAT reveals whether the response is linear or has a
tipping point), which a band-ends row cannot. It reads as nonsense today because
its caption is written as a **slot** ("the one declared input whose band ends
separate from its centre") rather than naming the input. On the record it is the
low-and-slow anchor; once the re-run confirms that, the caption says so and the
figure is legible. Inert rows get no figure — that is the whole point of
collapsing §5.1: three figures of non-events were removed on 2026-09-13.

**The effect column** is the band-ends-against-centre readout for each row, with
intervals: for a mover, three numbers (low / declared / high) or a pointer to the
figure; for an inert row, the word *inert* with the band-end deviation inside the
interval at centre; for $z$, *zero by structure*; for the two swaps, the
alternative's value against the declared one. It is empty because the sweeps on
record ran at ten seeds, one MTD scheme, pre-restoration substrate, and the
failure-matrix sweep under the superseded fixed-dwell regime (§3.2). **Nothing in
the column or the figure can be written until the re-run at the reported
configuration**; the dwell sweep's S3-R re-run (1 740 runs) is the closest thing
to a usable number and still differs in seed count and mechanism pool.

**What each appendix item is for, and what it still owes:**

| Item | Purpose | State | Owed |
|---|---|---|---|
| B.4 dwell derivation | the *why* of each dwell value: anchor families, evidence tiers, multipliers | tables generated | proofread of the justification strings |
| B.5 mapping reasons | why each tactic maps as it does, incl. what the simulator lacks for a dwell-only row | table generated | caption voice pass |
| B.6 weight sets | the failure matrix decomposed: rule kernel (a) × distance kernel (b) = set (c); the A–I ledger; the declared point in its bands | figures + tables landed | the 2–3 sentence lead; the sweep-results paragraph (blocked on the re-run) |
| B.7 forced-total | the experiment that rejected the total mapping | table landed | the framing paragraph |
| C.1 dwell robustness | per-anchor band ends against centre; the identifiability result; the degenerate operating region; the power limit | table landed (ten seeds, S3-R) | framing paragraph; numbers refreshed by the re-run |
| C.2 exponential family | the shape defence, the Madan leak, the holm2014 counter-evidence, the measured scope | table landed | the framing prose (spine in the comment) |
| C.3 decay robustness | $\gamma$, $\delta$, $z$ band ends against centre, then the corners of the influential pair | **placeholder — no data at any regime the chapter reports** | the re-run, then the framing paragraph |

The body/appendix split is by resolution, not by importance: Table 5.1 is one
row per input *family* and says inert-or-moved; the appendix is the per-value
expansion a reader goes to when they doubt a row. Nothing was "pushed to the
appendix" to hide it.

**Order of work that follows.** (1) Re-run both sweeps at the reported
configuration — the standing blocker (§3.2), now also blocking §5.1's prose,
since the preamble's *selection* sentence names the mover and the re-run decides
it. (2) Put the plain-words clause in Table 5.1's Quantity column (a table edit,
no ledger cost). (3) Then §5.1 is one dictated unit: purpose, method, ceiling,
the table, the figure, the selection sentence.

---

## 20. §5.2 Experimental setup — the design, ratify before drafting (2026-09-14)

Marc's ask: string the settled material into §5.2 — structure, organisation,
the points that must be prioritised, the two tables — as the precursor to the
runs that start today, and for the supervisor discussion tomorrow. Design only;
no tex touched. Everything below is assembled from §§1–19, the conventions
files and the records; nothing here is a new finding.

### 20.1 The boilerplate as it sits — what holds and what would mislead

**Placement holds.** §5.2 sits after §5.1, which now closes by naming its
selection, and before §5.3, which is the funnel's first movement. That is the
corpus's one-movement form (conventions §a: declare, then report) and nothing
moves.

**The placeholder paragraph holds** — two tables, the measures named as
instrumentation, the comparability boundary as a disclosure — and is the right
brief. Four things in the comment blocks under it would mislead a drafting
session and should be retired when the section is drafted:

1. The section-head comment still puts *network scale and density* and *the
   declared-capability arms and their nulls* in Table 5.2. Both left on
   2026-09-13 (§16, §18): scale and density are unswept and say so in Table 5.3;
   the capability arms are gone and the modulators are held rows.
2. The comment assigns the **roadmap sentence** to §5.2. The chapter opener now
   carries the roadmap (Marc's dictation placeholder, Tay's house pattern), so
   §5.2 must not repeat it. What §5.2 owes instead is the *closing* sentence in
   §20.3 — where each results section reads in the factor space.
3. **A terminology consequence nobody has drawn.** The registry ratifies
   **baseline attacker** for the inherited scripted attacker. Conventions §f2
   says never let "baseline" carry the no-defence condition as well. So the
   no-defence condition is **no defence** everywhere in ch5 — the table level,
   the figure origin, the prose — and never "the baseline". The §5.4.2 caption
   and several placeholders still say *inherited scripted attacker* / *inherited
   attacker*, which the registry deprecates; a voice-pass item, not a §5.2 one,
   but §5.2 is where the two references are fixed by name, so it sets the term.
4. **One duplication to resolve at the voice pass, not now.** §5.1's drafted
   outcome-measure sentence already says that at the inherited interval neither
   attacker completes the objective. §5.2 owns that as the *design fact* (ch7
   point A needs it stated once in `sec:dimensions`); §5.1's clause is its local
   justification and can become a forward reference once §5.2 exists.

Both tables are `[H]` placeholder boxes. They become real `\tablestyle` tables
in the drafting pass; §20.6 recommends generating them.

### 20.2 The shape — two movements, one section, no subsections

The corpus's titled setup sections split the same way: Ho's *Experiment Setup*
(conditions, fixed parameters) against *Evaluation Method* (collection,
metric calculation); He's V.A (dataset) against V.B (metrics). Reti's single
untitled §5 carries both in one run of prose around two tables. On two units
the recommendation is **Reti's form** — one section, two movements, the tables
carrying the internal structure — because the chapter's heading count is
under budget for the first time (10 on 12) and a setup section reads best as
one declaration. *Alternative*, if navigation is wanted: 5.2.1 *Factors* and
5.2.2 *Measures* (He's split), two headings on the two units, both noun
phrases; costs nothing on the ledger, adds two rows to the contents.

| Movement | Unit | Carries | Floats |
|---|---|---|---|
| 1 — the factor space | 1 (~250 w) | opens on §5.1's selection; fixes the two references by name; the design facts that set the levels; the defender's three clauses | Tab. 5.2 varied, Tab. 5.3 held |
| 2 — the measurement | 1 (~250 w) | the measures by family and the coverage headline; the run count as a consequence; the four inference sentences; the comparability boundary and the two concessions; the closing where-each-section-reads sentence | Tab. 5.4 measures (recommended, §20.5) |

### 20.3 Movement 1 — content points, in order (cue card, not prose)

1. **Pick up the selection** (C7b, §5.1's last paragraph): the low-and-slow
   anchor held at its declared value and named in every claim that could turn
   on it; the exponential draw live only at long dwell under mutation pressure;
   the mutation interval a varied factor because the inherited tempo sits in a
   degenerate region. One sentence, three clauses.
2. **Fix the two references by name** (conventions §f2): the **no-defence
   condition**, which every effectiveness number is a difference from; the
   **baseline attacker**, which is the comparison arm. Never one word for both.
3. **Introduce the two tables in one sentence each.** Table 5.2: what varies,
   and that the design is a crossed core with three one-at-a-time extensions —
   the same discipline as §5.1, applied to the experiment. Table 5.3: what is
   held, with its reason, so the reader can judge how far a result generalises;
   Reti's paired tables are the precedent (conventions §a).
4. **The three design facts that set the levels**, each one sentence:
   - *tempo*: before a metric is reported the operating point must let it
     vary; the second interval sits above the boundary at which the objective
     becomes reachable, so success-shaped measures can move there and every
     claim states its interval (operating_point_discrimination.md; Kim's
     repeat-in-every-caption discipline).
   - *horizon*: a longer run at a fixed interval is also more defence, so the
     extended horizon holds deployments per run (or reports per firing) —
     horizon and dose are never confounded (§15.3). Checkpoint-denominated
     reporting rides here if Marc takes §15.2.
   - *objective*: breadth is the backbone denominator because it is
     degeneracy-proof at every tempo; target reach is reported beside it
     wherever it is non-degenerate, which on record is the level-1 target on
     the aggregate only (C14).
5. **The defender's half of the model** (C16; He's Goal / Knowledge /
   Capability, applied symmetrically — ch4 is the attacker's half): its goal is
   to disrupt, not detect; it knows nothing of the attacker, there being no
   detection channel; its capability is the seven mechanisms on a time-triggered
   schedule it never departs from. The adaptive selector is declared not
   exercised in Table 5.3 with its reason, so the roster matches ch2's.
6. **Negative scope, one clause**: the network is one terrain; scale and density
   are not varied (named as unswept, future work) — the corpus's discipline of
   naming what was not swept (conventions §c).

### 20.4 The two tables — rows and columns

House style throughout (`\tablestyle`, `P{}`, `\rowgroup`, booktabs, short
caption, footnote row for marks and pins — conventions §e3 parameter genre).

**Table 5.2 — the factors varied.** Columns *Factor · Levels · What the levels
are for*. Two row groups, and the grouping is the design statement: the crossed
core is a full factorial; the three extensions are run one at a time from the
core at its reference settings, so the run count has an arithmetic.

| Group | Factor | Levels | What the levels are for |
|---|---|---|---|
| Crossed | Attacker arm | the baseline attacker; the movement attacker under each of the four attack profiles (exfiltration; impact; double extortion; no realised objective); the aggregate, the corpus unpartitioned | the comparison arm; the five instantiations of the model, the aggregate being the objective-conditioning contrast |
| Crossed | Defence condition | no defence; each of the seven mechanisms alone (Table 2.2); random and alternative over the seven (Table 2.3) | no defence is the reference; singles and schemes are reported in separate panels. *Simultaneous dropped, Marc 2026-09-14 (C34): it ranks dose, not strategy, and a defender that rewrites everything at once is not a realistic posture (§14.4)* |
| Crossed | Mutation interval | 200 s (inherited); 2 000 s | the second is above the boundary at which the objective becomes reachable |
| One at a time | Timing regime | quasi-periodic (inherited: the mean plus a small exponential term, in effect a clock); exponential with the same mean | whether the schedule is learnable |
| One at a time | Horizon | 15 000 s (lineage); 60 000 s with deployments per run held (*placeholder, Marc 2026-09-14 — the cost curve sets the value, C36*) | the lineage bridge; headroom for a campaign the lineage's horizon was never sized for |
| One at a time | Objective | **targeted, the default on every cell** (target reach the headline denominator where non-degenerate, host breadth the backbone beside it); opportunistic on the prior evaluations' configurations only (§5.4.3, the lineage bridge) | *Marc 2026-09-14 (C37)*: an APT pursues a specific objective against a specific target (ch3 §3.1.1), so the targeted objective is the APT's and the opportunistic one is the lineage's (Brown's Scenario 1) |

Ruled 2026-09-14: `simultaneous` is dropped (C34); the horizon's second level
is a 60 000 s placeholder until the cost curve runs (C36); the targeted
objective is the default (C37), which also puts the **target placement** on the
table — see C41. Still open: whether the tempo row gains the E3 frontier at
reduced seeds (C35). A level that is not run does not appear — the table is the
run plan.

**Table 5.3 — the factors held.** Columns *Held · Value · Reason*. Four row
groups so a reader sees which side each constant belongs to; inherited values
marked in the footnote once, with the three version pins.

| Group | Held | Value | Reason |
|---|---|---|---|
| Environment | Network | 50 hosts, 5 endpoints, 8 subnets, 4 levels; one generated topology | one terrain, so every difference is the attacker's or the defence's; scale and density are not varied |
| Environment | Confusion penalty † | 20 s per interrupted action | substrate invariant |
| Environment | Deployment durations † | Zhang's per-mechanism means | substrate invariant |
| Replication | Runs per cell | 100, set by the declared tolerance (value: Marc's) | the interval around the cell mean sits inside the tolerance (Hoad, Robinson and Davies) |
| Replication | Seeds | the same seed set on every arm; arms independent | shared seeds do not give matched randomness across arms, so every cross-arm test is unpaired |
| Attacker model | Declared inputs | Table 5.1's values | the low-and-slow anchor is the one the conclusions are exposed to |
| Attacker model | Sink retrace | on | an assumption the work runs with (ch4 §4.4.1) |
| Attacker model | Cost and learning modulators | off | implemented, not exercised: the model is run without its optional capabilities |
| Defender | Schedule | time-triggered; never reacts; no knowledge of the attacker | the defender's model (§20.3 point 5) |
| Defender | Adaptive selector | not exercised | needed retraining before it could trade cost against risk; future work |

Footnote row: † inherited from the simulator (Brown; Zhang). Pins: tactic-to-verb
mapping v2 (partial); failure set v4 (failure-only); ATT&CK Enterprise v19.1.
Stated here once and nowhere else in the chapter (the no-internals rule).

### 20.5 Movement 2 — content points, and the recommended third table

1. **The measures, named as instrumentation and grouped by the section that
   reads them** — which is also the family split of Table 3.1: §5.3's are
   model-validation instruments (not MTD metrics, and offered against no
   metric guideline — C28); §5.4's are effectiveness; §5.5's efficiency.
   **Recommended: a third table, Table 5.4**, columns *Measure · What it is ·
   Read from · Comparable across*. Grounds: He's V.B and Ho's *Evaluation
   Method* are titled setup homes for metrics; the reviewers found fifteen-plus
   bespoke instruments with no definition site (§13.3); the *Comparable across*
   column turns the three-valued comparability boundary (C27) from a paragraph
   into a property of each row, so a time-denominated measure is visibly
   within-arm only. *Alternative*: one prose paragraph grouped by family. Rows,
   from the records (definitions one clause each; equations, where a measure
   needs one, go to an appendix):

   | Section | Measure | Read from | Comparable across |
   |---|---|---|---|
   | §5.3 | distinct-tactic coverage over time; deepest stage reached; foothold retention | no defence, then under defence | within arm |
   | §5.3 | opening variety (distinct k-place openings) | no defence | cross-arm (counts) |
   | §5.3 | profile divergence against a split-half null (size-matched control pending, C19) | no defence | within arm |
   | §5.3 | effective behavioural breadth | no defence | cross-arm (a count) |
   | §5.3 | invocation spacing — an observation, axis-5 badge blank (C11, if ruled) | no defence | within arm (time) |
   | §5.3 | activity before against after a mutation, placebo-timestamp control (C26) | under defence | within arm |
   | §5.4 | host breadth and its suppression against no defence | all | cross-arm (counts) |
   | §5.4 | target reach, where non-degenerate | targeted level | cross-arm (a fraction) |
   | §5.4 | delay to first compromise, censored at the horizon | all | within arm (time) |
   | §5.4 | blocked fraction (Brown's actions blocked) | under defence | cross-arm (a fraction) |
   | §5.4 | time to a compromise checkpoint (only if §15 is taken) | extended horizon | within arm (time) |
   | §5.5 | attacker cost: attempts by verb; time split into activity, imposed delay, remainder (movement arm only, D-37); effort per host reached | all | counts cross-arm; time within arm |
   | §5.5 | defender reconfiguration occupancy (a floor) and deployments per unit time | all | cross-arm (arm-invariant) |

   Internal MTTC enters no row until its brief is ruled (blocker 4); return on
   attack is reported as the ledger's realised ratios, never the inherited
   per-vulnerability score (C10).
2. **The coverage headline, one sentence** (§10.6, corrected §13.4): on the
   field's own families this evaluation is strong on cost on both sides,
   adequate on containment and delay, silent on surface, payoff and service —
   five of ten — and the silence is the simulator's, not an oversight. Plus
   one clause on which instruments were re-validated against the new attacker
   (ch7 point B): the progression measures that saturated and their
   replacements.
3. **The run count as a consequence** (C8): declare the tolerance, cite the
   method, then the count follows; then the honest rider (§10.8): adjacent
   within-family ranks are not separable at that count, so the reportable
   cross-arm object is the two-by-two family contrast, not a total order (C23).
4. **The inferential model in four sentences** (C22): estimation first, effect
   sizes with intervals — which exceeds lineage practice and is claimed as such
   (conventions §d); arms independent, so unpaired throughout; Holm within each
   declared family; a minimum effect of interest declared per claim before the
   run (C7 — Marc's numbers). Barach's four-sentence form is the model.
5. **The comparability boundary, three-valued** (C27): cross-paper numbers are
   not comparable; across the two attackers only counts, fractions and per-host
   ratios are, never time; within an attacker every configuration is. One
   sentence, and Table 5.4's last column is where it lives.
6. **The two concessions, volunteered** (5b, C28): Jalowski's third guideline —
   no state-of-the-art protected system is compared, only mechanisms against
   each other and against no defence, with the defender frozen; and guidelines
   one, two and four for the attacker-side suite, conceded on the ground that
   those are model-validation instruments. In the same breath: which half of
   the attacker-realism demand the work answers (CTI-grounded, objective-
   conditioned, adaptively routed) and which it does not (scheme-aware; future
   work).
7. **The evaluation method on the ladder, one clause**: simulation over a
   graphical security model, with its stated cost owned (Cho) — if ch3 §3.2.3
   has not already discharged it for the document.
8. **Close on where each section reads**: §5.3 reads the no-defence column at
   both intervals and, for the response measure, one mechanism per layer;
   §5.4 reads every condition against no defence, both arms; §5.5 reads the
   two cost ledgers over the same cells. That sentence is what makes "any result
   can be located in this space" true on the page.

### 20.6 What today's runs need from this — the table is the run plan

**Recommendation: generate Tables 5.2–5.3 from the run matrix, not type them.**
A `tools/ch5_setup_tables.py` that reads the matrix definition the runs are
launched from and emits `tables/tab_5-2a_factors_varied.tex` and
`tab_5-2b_factors_fixed.tex` makes the declaration and the executed plan one
object, exactly as the ch2 defence-module figure fails the build on pool drift.
It also discharges the standing rule that no value reaches the tex except from
a tracked artefact. The prose is dictated; the tables are emitted.

The crossed core, from Table 5.2's rows: 6 arms × 11 conditions × 2 intervals
× 100 seeds = **13 200 runs**, ≈ 0.2 s each — under an hour on six workers (the
arithmetic is the design's; the wall cost is the record's, predesign §5). Each
one-at-a-time extension adds one level over the core at the reference interval.
The §5.1 re-run (2 600 + ~1 560 runs) shares this configuration and should be
launched in the same batch, since its effect column and Table 5.2's tempo row
must describe the same substrate.

### 20.7 Rulings owed before §5.2 is drafted

| # | Question | Recommendation |
|---|---|---|
| C32 | One section (Reti) or two subsections *Factors* / *Measures* (He)? | One section; the tables carry the structure |
| C33 | Table 5.4, the measures, as a third setup table? | Yes — the definition site the reviewers found missing, and the comparability column |
| C34 | `simultaneous`: drop on the realism ground, or keep and report per firing? | **RULED 2026-09-14: dropped.** Schemes are random and alternative |
| C35 | Tempo: two levels, or two plus the E3 frontier at reduced seeds? | Two in the crossed core; the frontier as a third entry only if it is run for §5.4 |
| C36 | Horizon second level 60 000 s with deployments held, and checkpoint reporting (§15)? | **RULED 2026-09-14: 60 000 s as a placeholder; the numbers decide.** Checkpoint reporting still recommended |
| C37 | Objective row: does E7 run (the level-1 target on the aggregate)? | **RULED 2026-09-14: the targeted objective is the default** on every cell; opportunistic only for the prior evaluations. Breadth stays reported beside target reach (degeneracy-proof) |
| C38 | The tolerance and the per-claim effect floors (C7, C8) | Marc's numbers; the sentences are ready for them |
| C39 | Generate the setup tables from the run matrix (§20.6)? | Yes |
| C40 | *no defence* as the fixed term for the reference condition, never *baseline*? | Yes — forced by the ratified *baseline attacker* row |
| C41 | Target placement, now that targeted is the default: the database set (Marc's 2026-08-30 default; Brown's "credential database", Masud's database host) or one host at a declared level (Brown's TX)? | The database set as the declared target — it is the field's own form and the ch3 form — with the Gate re-run at the extended horizon deciding whether it is reachable; a level-1 target as the fallback, since it is the only placement non-degenerate on record at 15 000 s. Whichever is taken is one row of Table 5.3, not a factor |

Assumed carried unless overruled, each already recommended above: C11, C16,
C22, C23, C26, C27, C28.

### 20.8 Marc's tempo question, and the literature review's motivation for every row (2026-09-14)

**The tempo row is the defender's, not the attacker's.** The word *tempo* in
the chat return named the mutation interval — the factor the corpus varies
most (Zhang's four intervals, Ho's and Hong's *Impact of MTD interval*, Reti's
movement time, Kim's interval fixed at 300 s and repeated in every caption) and
Cho's *periodicity* row of Table 3.1. The attacker's tempo is a different object
and it is already in the chapter three times, none of them as a factor: it is
**declared** in §5.1 as the dwell anchors (the "persistent low-and-slow tempo
that trades speed for evasion", ch3 §3.1.1); it is **observed** in §5.3 as the
invocation-spacing contrast (C11); and it is the denominator of the
interval-to-dwell ratio the rate study found decides the regime. Varying it in
§5.2 would re-sweep a §5.1 input under another name.

**Detectability is not a Cho metric family, and the chapter should say so
once.** Table 3.1 carries *detection rate* (He) as a defender-side success
event, and property 5 is stealth; neither is instrumentable here because the
simulator encodes no detection channel (ch2 §2.2.2, ch3 §3.2.3's own
trade-off sentence). What the work owns is the spacing and level contrast as
an observation about what the two attackers do, reported with the axis-5 badge
blank. So the answer to "is attacker tempo part of detectability, and is that in
Cho" is: it would be, under a detection model; there is none; the observation is
reported and the badge withheld. That is the same sentence as the coverage
headline's "silent on … service", and it belongs beside it.

**The unified-piece trace.** Marc's rule: whatever the review set up motivates
the setup. Read that way, every row of Tables 5.2–5.3 and every section of
Table 5.4 already has its sentence in ch3, and movement 1's prose should give
each factor that clause rather than a repo reason:

| Row / block | Motivated by | The sentence in ch3 |
|---|---|---|
| Attacker arm: the four profiles | §3.1.1 | an APT is "a *threat* defined by its objective: data exfiltration, impediment …, or positioning for future operations" — the four profiles are that partition, on the corpus |
| Attacker arm: the baseline attacker | §3.3.2–3.3.3 | the lineage's attacker, "carried unchanged", partial on six of eight; the comparison the gap statement asks for |
| Objective: targeted by default | §3.1.1, §3.3.2 | "pursues a specific objective against a specific target"; Brown's Scenario 2 is "like APT-style attacks"; Masud's target is the database host — the targeted objective is the field's APT form, the opportunistic one is the lineage's flooder |
| Defence condition: singles and schemes | §3.2.3 closing | "MTD evaluation is mostly one defence against a single or small set of attacks; evaluating multiple defence mechanisms together is where the recent work sits" |
| Mutation interval | §3.3.2 (Kim), Table 3.1 | the corpus's most-varied factor; Kim sizes the attacker's scan range to the interval, which is the interval-to-dwell contest stated from the other side |
| Timing regime | §3.3.1 (Jalowski) | an APT "learns the defender's mutation patterns over time" — a near-periodic schedule is learnable, so the regime is a factor rather than a footnote |
| Horizon | §3.1.1 | median dwell 14 days, espionage 122 days, Volt Typhoon five years: the lineage's 15 000 s horizon was sized for a flooder, and a campaign attacker needs headroom — with deployments held so the horizon is not silently more defence |
| Held: the defender's model (goal / knowledge / capability), no detection, no reaction | §3.2.1, §2.2.2 | the defender here is the "SDR operation alone" class, not game-theoretic, genetic or learning; "no purely reactive deployment strategies … no detection channel is encoded" |
| Held: one network | §3.2.3 | simulation's stated cost — "parameters that are not captured in a simulator are not accounted for"; scale and density named as unswept |
| Table 5.4, §5.3 block | §3.3.1 | the eight properties, one measure each — the instruments are the properties' own measurements, which is why they are model-validation instruments and not metrics (C28) |
| Table 5.4, §5.4–5.5 blocks | §3.2.2, Table 3.1 | perspective × purpose; and Hong's sentence — "the effectiveness metrics are dependent on how the attacker was implemented" — is the sentence the cross-arm comparison tests |
| The concessions and the boundary | §3.2.2 | "cannot be benchmarked … no common benchmark" (Jalowski): the comparability boundary and the third-guideline concession are ch3's diagnosis owned in ch5 |
| The funnel (§5.3 before §5.4) | §3.3.3 | "the performance of MTD against an attacker with a foothold remains unmeasured" — the no-defence arm is the foothold attacker characterised before the defence is scored |

One consequence for the drafting cue card (§20.3 point 4): each design fact
opens on its ch3 clause and closes on its level, so a reader meets the factor
as a claim the review already made. That is the unification Marc asked for, and
it costs no words the section does not already spend.
