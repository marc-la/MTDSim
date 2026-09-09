---
status: open — design proposal; Marc's rulings owed before any tex change
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

Nothing here changes the tex. Everything below is a proposal or a flagged
blocker.

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

## Validation gate

The design is discharged when Marc has ruled C1–C7 and the §5.1 register exists
as a generated table whose numbers come from artefacts rather than transcription.
The chapter is not drafted against this file until blocker 1 is resolved, because
the headline it would be written around is currently unreproduced.

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
