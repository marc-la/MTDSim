---
status: durable
created: 2026-07-29
updated: 2026-08-01
topic: "Findings ledger (F1–F8) from the axis-6 session, re-read under the thesis framing: what greater attack fidelity implies for current MTD evaluation methods. Preserves 1 800 runs' worth of results that read as mechanism failures and are findings about the evaluation apparatus."
---

# What greater attack fidelity implies for current MTD evaluation methods — a findings ledger

> **Retired class labels.** This record is investigation history and is left as
> written: it reports the pre-2026-08-06 labels `pure_steal` / `pure_impediment` /
> `double_extortion` / `infrastructure_setup`, which the objective-tactic rename
> replaced with `objective_exfiltration` / `objective_impact` /
> `objective_exfiltration_impact` / `objective_none_c2`. Rewriting them would
> re-attribute evidence to labels that did not exist when it was taken. Crosswalk:
> [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

> **Relocated from `docs/handoffs/` on 2026-08-01, unchanged in substance.** It
> was filed as a handoff and is not one: it commissions no work, sets no
> validation gate, and will never be "shipped and deleted". By the placement
> criterion in [`../../../workflows/docs_map.md`](../../../workflows/docs_map.md)
> it is an investigation record, and the handoffs directory is meant to be an
> inventory of *open work*. Its findings stand as the record of the runs that
> produced them; the body below is preserved as written.
>
> **One decision remains open for Marc** — see §"What this asks of Marc" at the
> end. It is pointed at from `docs/handoffs/README.md` so it stays visible now
> that this file no longer sits in that directory.
>
> **Re-confirmed 2026-08-01.** F2 (MTD's cost effect is uniform in *relative*
> terms and therefore invisible to a normalised utility ratio) and F5 (a more
> rational attacker performs worse) were independently re-measured on the
> post-disposition substrate during the cost-model simplification work, and both
> reproduce — [`cost_model_plain.md`](cost_model_plain.md) §2.1. F4's successor
> question is now carried by the attacker-disengagement measure, since built and
> run — [`attacker_disengagement.md`](attacker_disengagement.md).

**This record deliberately has no goal.** It is a preservation record: a
session's worth of measurements that were produced while chasing criterion
axis 6 and which turned out to answer the project's actual thesis question
better than they answered the axis. It carries no recommended approach and no
validation gate, because nothing here is a commission. A future session should
read it to know **what has already been measured** before designing anything —
and to avoid re-deriving results that cost 1 800 runs to get.

The framing is Marc's, stated 2026-07-29 and clearer than the framing the
session started with:

> **The thesis of this project is "what does greater attack fidelity imply on
> current evaluation methods of MTD".**

Everything below is re-read under that question. Several results that were
logged as *failures of the axis-6 build* are, under this framing, **findings
about the evaluation method** — which is why they are worth preserving rather
than discarding with the mechanism that produced them.

## Why this session hit a wall

It was pursuing the wrong contrast. The axis-6 work, the targeted-attacker
feasibility study, and the give-up proposal were all built on **empirical
comparison of the baseline attacker against the movement attacker** — "does the
profiled attacker do something different". That is not the thesis. The thesis
asks what a *more faithful attacker reveals about the evaluation instrument*,
which is a question about the **method**, not a contest between two attackers.
Read that way, several results stop looking like dead ends.

Recording the wrong turn explicitly so the next session does not repeat it: a
finding of the form "attacker A beats attacker B" is not thesis material unless
it says something about what the measurement could or could not see.

## The findings, re-read under the thesis question

Ordered by how much they bear on the evaluation method, not by when they were
found. Every number is regenerable from `data/results/axis6_rationality/`
(untracked by design; the scripts are the record).

### F1 — Aggregate MTD metrics hide a 13-fold variation in MTD's actual effect

MTD's suppression of per-tactic success rate, measured on the unconditioned
attacker over five profiles × seven seeds under `v2_partial`, spans **0.08× to
1.02×**. `lateral-movement` is essentially untouched (0.98×); `initial-access`
(0.08×) and `execution` (0.10×) are nearly erased.

**Implication for evaluation.** Current practice reports MTD's effect as an
aggregate over one collapsed attacker — an ASR, an MTTC, a compromise ratio. A
tactic-resolved attacker shows that single number is an average over an order of
magnitude of variation. A defence that looks moderately effective in aggregate
may be *useless* against the tactic an actual campaign depends on. This is the
strongest evaluation-methods claim the session produced and it needs **no new
mechanism** — it is a measurement over the existing attacker.

### F2 — MTD's cost effect is near-uniform in relative terms, so cost-based MTD metrics overstate its effect against a rational attacker

MTD's confusion penalty per tactic spans an 18-fold range in absolute terms, and
correlates with the tactic's declared dwell at Spearman 0.87 — longer dwells
straddle mutations more often. Expressed **relatively**, the tax is nearly flat:
penalty ÷ declared cost ranges 0.032–0.113 about a mean of **0.086**, a roughly
uniform ~9 % surcharge.

**Implication for evaluation.** A rational agent responds to *relative* cost, not
absolute. So an evaluation reporting "MTD raises attacker cost by X %" is
reporting something real that a cost-rational attacker is **behaviourally
indifferent to** — a uniform proportional inflation cancels in any normalised
utility. The metric measures a quantity that does not change the modelled
adversary's decisions. That is a methodological finding about cost-denominated
MTD metrics, independent of whether anyone builds a cost-rational attacker.

### F3 — MTD cannot reach the TTP layer at all; it reaches execution, not planning

Failures accumulated **before the token first reaches its objective tactic**,
no-MTD → MTD, per profile: 7.4→7.9, 6.1→6.3, 7.4→8.3, 9.7→10.7, 0.7→0.7 —
ratios **1.00 to 1.12**. MTD does not delay the attacker's *arrival at its
objective tactic* by any measurable amount.

Meanwhile total failures absorbed over the run rise **2.6×** on the two profiles
that engage most (78→201, 80→204).

**Implication for evaluation.** This is Marc's pyramid-of-pain observation
confirmed empirically: the MTD schemes in this lineage operate on network and
host artifacts (IP, port, OS, service, topology), which sit *below* TTPs. An
attacker modelled at the ATT&CK-tactic layer is **structurally insulated** from
them in its planning, and is affected only in its execution. So an evaluation
that credits MTD with "disrupting attacker behaviour" is crediting it with
something it demonstrably does not do at that layer — it disrupts whether
actions succeed, never which actions are chosen. Any future attacker-fidelity
work that adds *planning* sophistication should expect it to be invisible to MTD
for this reason, and should say so in advance rather than discovering it.

### F4 — The evaluation's own success criterion is degenerate, and attacker fidelity supplies a better one

The only live objective in the simulator, for **both** arms, is Zhang's NCR
0.8 — compromise 80 % of the network. The movement attacker's
`reached_objective` is exactly that flag. **A profile's operational objective has
no connection to what the simulator counts as success.** At the 200 s operating
interval nobody reaches NCR 0.8, so ASR is pinned at zero and discriminates
nothing (the degenerate region the rate feasibility study recorded).

Two alternative criteria were measured, and both discriminate where NCR cannot:

- **A located objective.** Scoring "did the attacker reach a database host"
  takes the baseline from 1.43 of 2 database hosts without MTD to **0.00** under
  it — total separation, at the interval where ASR separates nothing.
- **A fidelity-derived objective, requiring no substrate change.** Scoring "the
  token visited its profile's objective place *while holding a live foothold*"
  gives, no-MTD → MTD: `pure_impediment` **7/7 → 2/7**, `aggregate` 7/7 → 4/7,
  `infrastructure_setup` 7/7 → 4/7. Reaching `exfiltration` with nothing
  compromised is not exfiltration, and MTD's actual mechanism is severing the
  position that would make it real.

**Implication for evaluation.** The success criterion inherited from the lineage
is attacker-agnostic — it describes a quantity of network owned, not an
objective any modelled adversary holds. Greater attacker fidelity does not just
change the answer; it exposes that the question was being asked in a form the
instrument could not answer at its own operating point.

### F5 — A more rational attacker performs *worse*, so fidelity and adversary strength are not the same axis

Registering a cost/benefit decision rule and sharpening it drives blocked
attempts from **49 % to 99 %** of attempted actions and drops distinct hosts
compromised toward zero. The cheapest tactics on this substrate are the
exploit-shaped ones, which are also the most tightly precondition-coupled; an
attacker optimising declared cost optimises its way into a wall. This is
experiment 1's H-coupling finding restated in economic terms.

**Implication for evaluation.** An evaluation that assumes "higher-fidelity
attacker ⇒ stronger adversary ⇒ lower bound on MTD's effectiveness" is unsound.
On this substrate the relationship is non-monotone, and a fidelity increase can
*flatter* the defence. Any claim of the form "we evaluated against a more
realistic attacker, therefore our defence result is conservative" needs this
checked, not assumed.

> **Amended 2026-08-01 (R2 on the benefit family) — the implication survives,
> the stated mechanism does not, and the amendment makes the finding
> stronger.** The paragraph above locates the cause in the *terrain*: cheap
> tactics happen to be precondition-coupled here. That is not established. The
> decision rule's two terms — declared duration as cost, objective proximity as
> benefit — penalise *instrumental* tactics twice over and in the same
> direction, so reconnaissance is discounted both for being the slowest
> declared tier and for sitting furthest from any objective, and neither term
> can represent that a tactic is worth its price because of what it unlocks
> ([`cost_model_plain.md`](cost_model_plain.md) §2.2a). So "a more rational
> attacker performs worse" is more honestly "**an attacker optimising a
> mis-specified cost performs worse**", and the mis-specification is in the
> model, not the map.
>
> **F5's implication for evaluation holds either way, and gains a sharper
> form.** It never depended on *why* the fidelity increase hurt — only on the
> fact that it did, which is measured. What the amendment adds is the reason a
> practitioner should care: the failure mode is not exotic. Pricing attacker
> actions by their declared duration and valuing them by proximity to the goal
> are both the obvious first choices, and together they systematically starve
> the enabling steps that make the goal reachable. An evaluation that gives its
> attacker a cost model without asking whether that model can express
> instrumental value will measure the attacker defeating itself and may report
> it as the defence working. That is a transferable warning of the same family
> as the axis-7 credit-signal result, and it belongs beside it.

### F6 — Not all attacker fidelity is evaluation-relevant, and there is a test for which is

The axis-6 utility modulator is a pure function of declared data and the current
place, so its factor table is precomputable. Proven by spike: the table was
computed with no simulation running, folded into a plain overlay, and reproduced
the stateful run **30 of 30 bit-identical**
(`data/results/axis6_rationality/collapse_test.py`). It is structurally a third
static overlay — an overlay on an overlay, in Marc's phrase — and the MTD
condition is not among its inputs, so no parameter choice could have made it
respond to the defence.

**Implication for evaluation, and the generalisable test.** A fidelity increase
is evaluation-relevant only if the defence's actions are among its **inputs**. A
mechanism that reads only declared data and current position adds descriptive
realism and **cannot** change what an evaluation measures, however sophisticated
it looks. The collapse test generalises: precompute the mechanism's contribution
with no simulation running; if the run is bit-identical, the mechanism is
static and cannot interact with the defence. This is cheap and should be run on
any future attacker-fidelity mechanism *before* it is swept.

> **Amended 2026-08-02 — the verdict above describes the *superseded* model, and
> the property it rests on has since been surrendered on purpose.** The iterated
> cost model ([`iterated_cost_model.md`](iterated_cost_model.md)) replaces the
> declared-duration denominator with a cost conditioned on the capabilities the
> attacker currently holds, and the defence's actions are therefore among its
> inputs: the declared precondition relation's `mtd_clears` field says a
> network-layer mutation destroys the position an enabling chain was walked
> from, so the chain must be re-walked and the cost rises. **The collapse test
> would now fail by construction**, which is exactly the intent — a factor that
> cannot see attacker state cannot see MTD either, and the shipped model's
> inability to respond to the defence (F2, C4) and its inability to express
> instrumental value (F5, R2) turned out to have one remedy between them.
>
> **What survives the amendment is the part that matters, and it survives
> strengthened.** F6's generalisable test is not about the utility modulator; it
> is about *any* attacker-fidelity mechanism, and it now has both outcomes on
> record rather than one. The shipped model precomputed to 30/30 bit-identical
> and was correctly diagnosed as evaluation-irrelevant; the iterated model was
> designed to fail the same test, and the axis-6 sweep is the check on whether
> failing it is sufficient as well as necessary. That pairing is a better
> instrument than the original finding was: the test tells a designer whether a
> mechanism *can* interact with the defence, and says nothing about whether it
> *will*. Read F6 as a screening test with a known negative and a known
> positive, not as a verdict on one mechanism.

### F7 — The lineage's own higher-fidelity attacker has rotted to unreachable

Brown's Scenario 2 (targeted attacker) is fully specified in the literature
layer, was descoped by Zhang for time-domain reasons, and has since decayed:
forcing `network_type = 0` **crashes graph generation** on the phase-0 geometry,
the shipped `target_layer = 4` exceeds the layer loop's maximum index of 3, and
across the layers that can fire, construction succeeds only on a seed-dependent
subset (3/3 at layer 2, 1/3 at layer 3). Brown's targeted *strategy* has no live
code path at all. Full detail:
[`targeted_attacker_feasibility.md`](targeted_attacker_feasibility.md) §4.

**Implication for evaluation.** The field's evaluation infrastructure has
atrophied around the low-fidelity attacker. The higher-fidelity option was
present, documented, dropped for expedience, and is now not merely unexercised
but non-functional — with no lineage paper documenting its time-domain
semantics. That is a concrete instance of the thesis's premise: evaluation
methods have consolidated around an attacker chosen for tractability, and the
alternative decayed unnoticed.

### F8 — A named MTD evaluation metric returns a constant, and nobody noticed

Because `target_node` is `None` in every run this project has ever done,
`get_path_from_exposed` falls into a bare `except: pass` and
`attack_path_exposure()` returns a degenerate **1.0**. Given a real target node
it returns a meaningful value (0.963 for target 49 on seed 0). Attack-path
exposure is one of the four metrics the project names as mattering.

**Not currently corrupting any published number** — nothing in `src/mtdsim/` or
the results workspaces consumes APE or SAPV; only the substrate's scorer
computes them. It is a trap for whoever turns targeting on, not a live error.

**Implication for evaluation.** A metric that presupposes attacker fidelity the
simulator does not provide degrades silently to a constant rather than failing.
This is the sharpest small instance of the thesis available: the *metric*
assumed a targeted attacker, the *attacker* was descoped, and the metric kept
reporting.

## What was built, and its status

Shipped and committed on `feat/axis6-incentive-rationality`:

- `src/mtdsim/l3_simulation/movement/utility.py` + `data/ogasp/attacker_utility.json`
  and its generated 75-cell view — the axis-6 utility modulator and its declared
  benefit family. Null-equivalent at λ = 0 (bit-identical, tested). **Registered
  nowhere by default**; it changes nothing unless an experiment constructs it.
- `tests/l3_simulation/test_movement_utility.py` — 27 tests.
- [`incentive_rationality.md`](incentive_rationality.md)
  — design record, pre-registered conclusions, sweep results, and (corrected
  2026-07-29) the §6.3 explanation of why C4 moved.
- [`targeted_attacker_feasibility.md`](targeted_attacker_feasibility.md)
  — the targeted-attacker study. **Its §7 recommendation is superseded** by F4:
  it recommends a substrate repair, and the foothold-conjoined objective
  measured afterwards achieves the same discrimination entirely in the movement
  layer. Read §7 with that caveat.
- Criterion axis 6 moved NOT ADDRESSED → **DESIGNED** with DEMONSTRATED
  explicitly withheld.

Nothing here needs unwinding. The modulator is inert unless constructed, and the
records are honest about what did and did not reproduce.

## Open questions, recorded without prescribing answers

Not a task list. These are the things the session could not settle, phrased so a
future session knows they are open rather than decided.

1. **Which of F1–F8 are thesis chapters and which are footnotes?** F1, F3 and F4
   look like the load-bearing ones; F8 is the sharpest anecdote. That is Marc's
   editorial call, not a session's.
2. **Does the evaluation-method critique need a *more faithful attacker* at all,
   or only a *tactic-resolved measurement*?** F1 and F2 were obtained from the
   unconditioned attacker. If the thesis's claims can be made without any new
   attacker mechanism, that is a considerably stronger and cheaper position —
   and it inverts the assumption the wave-5 handoffs were built on.
3. **Whether a give-up / abandonment condition belongs in the model.** It was
   proposed as a baseline-vs-movement discriminator, which the thesis framing
   rules out as a goal. As an *evaluation* observation it may survive: current
   MTD evaluation has no attacker-abandonment concept, so MTD's deterrence
   effect is unmeasurable in the current method. Note the scale obstacle if
   revisited: profiles accumulate 15–293 failures, so **no single global
   threshold separates all five**.
4. **The S2 governance question is still unanswered** and now has a second half.
   The seam record's §7 asks Jin whether a within-run movement-layer state is M7
   refinement. F4's located objective would additionally change *what the
   simulator counts as success*, which is a larger question than the seam's.
5. **The axis-6 / axis-7 boundary.** A utility conditioned on realised success
   and a learner conditioned on realised success read the same signal. Whether
   "rational about cost/benefit" is distinguishable from "learns what works"
   once both exist is unsettled, and both handoffs assumed it was.

## Hard constraints that still hold

- Branch / commit / push rules from
  [`../../../workflows/session_workflow.md`](../../../workflows/session_workflow.md); never
  push.
- **S2 action-set freeze** — no substrate change without a ruling. Every
  mechanism in F4's cheaper route lives in the movement layer; the F7 route does
  not.
- **The degenerate region** — no success-rate-shaped claim at the 200 s
  operating interval.
- **No time-denominated cross-arm comparison** (S3-R pricing asymmetry).
- **No value chosen because it improves an outcome.** The declared-value
  guardrails apply in full to anything that comes out of this.
- Australian English.

## Reading list

- [`../../apt_model_criterion.md`](../../apt_model_criterion.md)
  §(d) axes 2 and 6 — the scored instrument, and where Brown's scenarios are
  filed.
- [`incentive_rationality.md`](incentive_rationality.md)
  §6 — the sweep and its corrected explanation.
- [`targeted_attacker_feasibility.md`](targeted_attacker_feasibility.md)
  §§2–5 — the collapse test, the two channels, the construction blockers, and
  the discrimination probe.
- [`measurement_suite.md`](measurement_suite.md)
  — what is already measurable without building anything.
- `data/results/axis6_rationality/README.md` — the workspace, and the one thing
  in it not to misread.

## Out of scope (explicitly)

- Any commissioning of work. This handoff records; it does not ask.
- Re-running the axis-6 sweep. It is done, and the verdicts are recorded.
- Re-deriving F1–F8. The scripts exist; run them rather than rebuilding them.
