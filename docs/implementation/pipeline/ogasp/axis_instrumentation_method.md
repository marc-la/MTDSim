---
status: durable
created: 2026-08-09
updated: 2026-08-13
topic: "The method the axis-instrumentation programme arrived at, extracted from eight axes and roughly 30 000 runs — the diagnostic that decides whether an axis wants a mechanism, an instrument or nothing; the six design rules that separated the results that held from the ones that did not; and the failure modes that cost this project the most time"
---

# How to instrument an axis — the method, extracted from the axes that worked and the ones that did not

**Status:** durable method record, for sessions and for the methodology chapter's
evidence. It generalises the practice that produced
[`apt_model_criterion.md`](../../apt_model_criterion.md)'s scored rows; the per-axis
*content* lives in that criterion and in the study records, and is not restated here.

**Why it exists.** Eight axes were instrumented over roughly six weeks and thirty
thousand runs. The results that held and the results that collapsed are separated by
a small number of practices, most of which were discovered by their absence — a
measure adopted unchecked, a control not run, a null never established. Writing them
down once is cheaper than rediscovering them on axis nine.

**What it is not.** Not a checklist to satisfy, and not a substitute for the per-axis
context. It is the shape of the reasoning that worked.

## 1. The diagnostic that comes first — where is the binding constraint?

Before proposing anything for an axis, establish which of three things is actually
blocking it. **Getting this wrong is the most expensive error available**, because
each answer licenses a different kind of work and the wrong kind can absorb
thousands of runs before returning nothing.

| the constraint is a… | symptom | what moves it |
|---|---|---|
| **mechanism** | the capability does not exist; nothing has been swept | build it, declared and ablatable |
| **instrument** | the mechanism exists, operates, and the measure cannot tell whether it helped | build the measure, or find that no measure can |
| **substrate** | the mechanism and the measure both exist, and the terrain cannot express the property | stop, and record why |

**Axis 6 walked all three, in order, and that is the worked example.** It began
missing a mechanism; a declared-duration utility modulator was built and swept (1 800
runs) and operated without changing MTD's measured effect. The constraint became an
instrument problem: a second, better mechanism was built and swept (4 200 runs), and
its badge criterion was **passed by a negative control** — an arm proved by spike to
be unable to see MTD at all. A criterion a negative control can pass is not measuring
the property it tests, so no mechanism could have moved the row. The constraint then
became substrate: on this terrain the attacker has *something to be rational about
but nothing to be rational toward*, because it banks no payoff. The row closed.

The diagnostic value is retrospective and cheap: **had the instrument question been
asked before the second mechanism, 4 200 runs would have been spent differently.**

**A corollary worth stating separately.** When the constraint is an instrument, the
honest deliverable may be *"no measure can move this row"*. Axis 7's context says so
outright, and refusing to build a proxy is a result. A reader that re-reports existing
friction measures under a new name is measurement theatre.

## 2. Instrument design — four rules, each bought with a failure

### 2.1 The null is measured, not declared

A divergence, an entropy or an exposure figure means nothing until the reader knows
what the same thing compared with *itself* returns. This project shipped
`profile_divergence` and left it unrun for months precisely because it had no null;
the corpus run built `split_half_divergence_null` — within-profile JSD between random
half-splits, 200 seeded draws — and only then did the numbers acquire meaning. The
reporting form that resulted is the one to copy: **null-relative**, so the headline
sentence is *every pair diverges by at least 53× the seed-noise ceiling* rather than
an uninterpretable 0.1.

The same defect in a different guise: six modulator sweeps each report a path-entropy
null, at three different poolings, and one value appears at two of them. Nulls that
were never established on common ground cannot be superimposed later.

### 2.2 The kill criterion must be able to fire, and must be committed first

Every measure carries a plausible degenerate reading — that it is a decayed event
counter, a hub-occupancy proxy, a re-expression of corpus size. **Name that reading,
commit a threshold against it before the measure runs, and report the verdict either
way.** The project's convention is Spearman |ρ| against 0.90, used verbatim across
studies so verdicts stay comparable.

Both outcomes have now occurred and both were valuable. Axis 5's exposure measure
**held** at −0.529, and the sign was the interesting part: the attacker that acts most
reads quietest, which a decayed counter could not produce. Axis 2's size criterion
**fired at exactly −1.0**, killing the divergence-to-`aggregate` column as arithmetic
rather than behaviour — a column that would otherwise have been read as evidence of
objective conditioning.

**The governing principle: a measure that has not been shown capable of returning the
unflattering answer has not been shown to measure anything.**

### 2.3 Check the measure under every mapping and condition before adopting it

Axis 1 adopted a replacement for a saturated depth measure and the replacement was
**itself saturated** under the go-forward mapping — the objective band is dwell-only
there, so no verdict can exist in it and the ceiling silently drops. It returned the
same value for all 800 runs of the comparative experiment. No inspection of the
measure's *definition* would have revealed this; the fault lives in the interaction
between the measure and the mapping.

The suite's gate 3 is the shape to reuse: require a candidate to separate at least one
adjacent pair that the measure it replaces cannot, run it under both mappings, and
record a split verdict as a split verdict.

### 2.4 Port the shape of a metric that already worked

The cheapest way to instrument a new axis is to reuse the *shape* of one that
succeeded, not to design from scratch. The axis-5 detectability measure established a
shape — **one scalar, computed over both attack models, with a declared family whose
order is corpus-grounded and whose magnitudes are swept, each with a null in its
band** — and that shape ported directly onto axis 3 as the **effective behavioural
breadth** measure ([`predictability.md`](predictability.md) — the record's filename
predates the 2026-08-13 rename from "predictability", §Resolution R6–R7 there): the
effective number of distinct next-moves per decision state (the exponential of the
policy's conditional entropy).

Two things travelled with the shape and are the reusable part:

- **A calibration arm that the instrument must return a known value for.** The
  scripted baseline is a **deterministic policy**, so it carries **one effective
  behaviour by construction**, and the reader has a self-test: if it does not
  return 1 there, the reader is wrong, not the attacker. Building a cell whose
  answer is known in advance is the cheapest validity check available, and it is
  independent of every result.
- **A census that gates everything.** Before any headline number, establish that each
  cell is estimable at the available sample size. It costs one pass and prevents a
  reported figure that the data could never have supported.

The general rule: **when a new axis needs an instrument, ask first which shipped
measure it most resembles.** A ported shape inherits its predecessor's validation
argument, its reporting conventions and its reviewer objections already answered.

### 2.5 Reader or mechanism — decide, and let the answer bind

A **reader** is a pure function over records that already exist. It changes nothing,
raises no freeze question, needs no re-simulation, and **moves no badge**. A
**mechanism** changes behaviour, raises the S2 question and needs a comparability
argument.

Axis 5 declined a badge move three times on this ground while its measurement field
was being discharged, and the discipline is what keeps the criterion honest: the
measurement field and the row are different objects, and discharging one is not
scoring the other. Prefer extending a reader over widening a record — the
confusion-penalty derivation closed an instrumentation gap with no schema change at
all — and when a widening is genuinely needed, discharge its burden by measurement
rather than by argument, as `n_compromised` was (837 compromise events against 155
distinct hosts, with the over-count itself MTD-dependent).

## 3. Comparison design — the part that decides whether a result survives

### 3.1 Run the second, matched control

**This is the highest-yield practice in the whole programme.** A mechanism compared
against a single weak control will separate from it and prove nothing.

Axis 7's progress-credit sweep ran two: `control_asymptotic` and `control_matched` —
the latter a declared static bias **matched to the learner's own observed
aggression**. The mechanism separated cleanly from the first (JSD 0.2804) and not at
all from the second (0.1196). That single contrast produced the axis's live question,
stated in the record as *is this learning, or a lookup with extra steps?* — and one
control would have returned a clean, wrong pass.

The pattern recurs by shape rather than by name: axis 4's **verdict-blind ablation**
(an empty value table, so composition passes everything through at 1.0) and axis 2's
**size-matched label-blind draws** are the same instrument. Build the control that is
matched on the thing you are *not* claiming credit for.

### 3.2 Make the null arm bit-identical

Every declared family in this project ablates to bit-identity at its null — λ = 0,
κ = 0, an empty value table. The arms then differ **by a parameter rather than by
wiring**, which removes an entire class of objection and makes the ablation exact
instead of approximate. Design for this before building, because it is nearly free
then and expensive afterwards.

### 3.3 Name the decision cell in advance

Sweeps here run over profiles × mappings × MTD conditions, and effects are routinely
cell-specific. Axis 7 named `v2_partial` as its decision cell before the sweep: the
ρ = 0 lead from the previous study replicated on `v1_ckc_total` and **reversed** on
the decision cell, so pre-naming is exactly what prevented a mapping-specific artefact
from being adopted as a declared-value change.

The discipline cuts both ways and must. The same sweep's **only separated positive
result in 7 000 runs** sits on the un-named mapping, and is therefore recorded as a
lead requiring its own pre-registration — not claimed. A rule that only bites when
convenient is not a rule.

## 4. Verdict discipline

- **The stopping rule.** Nothing re-specified after a criterion fails to discriminate;
  no arm added, no band re-centred, no cell re-chosen. The circumstance in which
  criteria drift is precisely a repair motivated by a known defect, which is when the
  rule matters most.
- **A failed criterion is a result, not a failed build.** Report it and move on. Two
  of this project's most transferable claims — that a normalised utility ratio cannot
  see a proportional surcharge, and that representation and reward are independent
  requirements — exist only because a criterion was allowed to fail.
- **Say which way "moved" points.** The house idiom is that a conclusion *recorded
  moved* was **not** confirmed; one pre-registration used the word in the opposite
  sense and needed a correction note at the top of its findings record. Prefer
  **CONFIRMED / NOT CONFIRMED**, which cannot be read backwards.
- **Ten seeds separate almost nothing**, and fifty did not separate an 8-of-10
  direction. Every aggregate goes through `interval_report`; `ordering_supported` is
  the gate, never the sorted means. A consistent direction at an effect size this
  small is a power statement, not a mechanism statement — say so.
- **Badges move on evidence only**, in either direction, and never by changing the
  model, weights, mapping or metrics to improve a row.

## 5. Reporting is part of the instrument

Two lessons, both bought at the cost of rework.

**A figure must let the eye compute the comparison it claims.** The axis-5 level
figure took three passes, and the failure was the same each time — a chart of a
*mean-level* result drawn so the eye tracked *peaks*, which read as a contradiction of
the table above it. What worked was binned means (so the comparison is a vertical
distance rather than an integral the reader estimates) plus an exceedance curve (which
states the claim with no summary statistic at all). **If a figure needs a sentence
explaining why it does not contradict its own table, it is the wrong figure.**

**Prefer the redundancy-free form.** A symmetric divergence matrix states every figure
twice and spends its diagonal restating the null five times; the ranked-dot form on a
log axis against a shaded seed-noise band says the same thing once, and the matrix
survives as a lookup companion rather than as the argument.

And the standing convention: on diagnostic and evidence figures, **no accentuation** —
no arrows, circles, callouts or highlight colours. Let the lines and cells carry it.
Uniform treatment across instances; a per-instance adjustment is stated and justified.

## 6. The failure modes that cost the most, and how to spot them early

- **Record staleness in a load-bearing document.** The criterion is loaded every
  session and its axis 7 has never recorded a 7 000-run sweep, so it still names as
  outstanding a thing that was built and swept. A metrics handoff listed two built
  readers as unbuilt. **Both would have caused a session to re-commission finished
  work.** Read the code against the record before trusting either; that check is what
  opened this programme's most useful findings.
- **An accounting unit that is not what it looks like.** The substrate writes one
  attack-record row per *vulnerability tried*, inflating the baseline arm's event
  count **3.75×**. A whole study's premise rested on the resulting apparent tempo
  contrast, and inverted when the unit was corrected. Establish the unit before the
  comparison.
- **Free pre-checks orient, they do not decide.** The recorded-data pre-check on
  breadth pointed one way and did not reproduce under the study's own conditions.
  Worth running — it is free — and never worth concluding from.
- **The rows are a census, not a scale.** Improving one axis provably degrades
  another: every declared modulator narrows traversal, so raising incentive or
  learning lowers plurality. Any claim names the configuration it was measured at. A
  proposal that would raise one row must say which one it lowers.

## 7. What the progression actually looked like

Recorded because the arc is itself the lesson, and it was not the arc anyone planned.

The axes began as **argued** — a rubric with a badge per row and a
*what-would-evidence-a-claim* field that was, in the criterion's own words, a set of
recommendations most of which were never built. The programme's first real finding was
that *the measurement suite could score axes the model held no claim on, and could not
score the axes it claimed.*

What followed was not a march from designed to demonstrated. **Most axes were
instrumented and returned negatives**, and the negatives turned out to be the
transferable results: that the substrate's success verdict — the atom every metric in
this lineage is built on — is not a progress signal; that MTD's tax is levied in
near-proportion to declared dwell, which a normalised ratio cannot see; that
representation and reward are independent requirements; that a criterion can be passed
by a mechanism provably blind to the thing it tests.

Two badges moved in the entire programme. Three axes hold at DESIGNED on **measured**
negatives rather than on absences, which is a stronger position than silence and is
only reachable by a model that carries the capability. And the project's largest
result — that the defence *ranking* inverts between attackers — scores on no numbered
axis at all, which is why the lettered rows exist.

**The practical shape of a productive session, distilled:** audit what exists against
what the records claim; find the gap is usually reporting rather than building; find
the control or null that was never run; pre-register before producing an output; and
let the criterion fail if it is going to.

**And the arc has a recent, cleaner instance worth naming.** Axis 3's reporting
question — chart, table, or nothing — was resolved not by choosing among them but by
**porting axis 5's metric shape** onto the axis (§2.4): one scalar over both attack
models, pre-registered before any trace was read, with an honesty ceiling fixed before
any number existed, a census gating the headline, a calibration arm pinned by
construction, and kill criteria each declared a reportable finding rather than a
failure. That is every rule in this record applied at once, on an axis whose evidence
had previously been carried by prose. It is the strongest available demonstration that
the method transfers, and it took a fraction of the effort the axes that discovered
these rules required.

## 8. Evidence

Every claim above is a generalisation of a recorded study. The per-axis specifics live
in [`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d) and in:
[`measurement_suite.md`](measurement_suite.md) (the reader contract, gate 3, the blind
spots), [`profile_divergence_findings.md`](profile_divergence_findings.md) (the
measured null, the size kill criterion firing),
[`progress_credit_findings.md`](progress_credit_findings.md) (two controls, the
decision cell, the moved/confirmed correction),
[`iterated_cost_model.md`](iterated_cost_model.md) (the criterion passed by a negative
control), [`incentive_rationality.md`](incentive_rationality.md) (the MTD-tax anatomy),
[`stealth_exposure_metric.md`](stealth_exposure_metric.md) and
[`stealth_spacing_diagnostic.md`](stealth_spacing_diagnostic.md) §7a (the kill
criterion holding; the three-pass figure),
[`experiment_02_findings.md`](experiment_02_findings.md) §11 (the verdict-blind
ablation), [`learning_readiness_findings.md`](learning_readiness_findings.md)
(representation versus reward).

The dissertation-side companion is
[`../../../notes/ch6_discussion/instruments_fail_silently.md`](../../../notes/ch6_discussion/instruments_fail_silently.md),
which argues the **instrument-failure taxonomy** for a chapter audience. This record is
its methodological other half and is deliberately session-facing: the note asks what
the failures mean, this asks what to do next time.
