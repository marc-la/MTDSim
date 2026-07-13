---
status: open
created: 2026-07-09
---

# Characterise the four operational objectives from the literature and pre-register per-class timeline acceptance criteria — the behavioural validation set the calibrated runner must pass, sequenced *before* the catalogue v1 freeze

> **This is a validation-set build, not a fitting loop.** The timeline runner
> has ~two global free parameters (the stealth and objective-execution dwell
> anchors); the per-class behaviour is carried by the *frozen* W-A weights and
> objective sets. So the deliverable is a **falsification/acceptance test** the
> calibrated timelines either pass or fail — never a target the weights get
> bent toward. A class that misses its signature is a **finding** (corpus
> thinness, prefix gap, tactic-aggregation loss), not a knob left un-turned.
> Read the degrees-of-freedom argument in full before starting — it is the
> reason this handoff is shaped the way it is.

## State of play

- **The four operational objectives** are the GASP L2 classes — `pure_steal`,
  `pure_impediment`, `double_extortion`, `infrastructure_setup` — plus the
  `aggregate` null profile. Defined in
  [`../specs/02_gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md); the class
  semantics and objective sets are fixed in the committed nets
  ([`../../data/ogasp/README.md`](../../data/ogasp/README.md)).
- **The runner has shipped** (2026-07-09): the seeded timeline library +
  behavioural report exist, and the report already shows the four envelopes
  *differ* from each other and from the null on median net time-to-objective,
  occupancy and outcome mix. It does **not** yet show they match any external
  per-class behavioural signature — that gap is this handoff.
  Contract: [`../../data/ogasp/timeline/timeline_schema.md`](../../data/ogasp/timeline/timeline_schema.md).
- **The structural discrimination test came back negative:** the divergence
  report found *no* class exceeds the shuffled-label null p95 at n≈29
  ([`../../data/ogasp/petri/divergence_report.md`](../../data/ogasp/petri/divergence_report.md)).
  So the structural weight layer alone does not separate the classes from the
  null. This handoff's behavioural signature match is the positive result that
  negative leaves open — and the test that could confirm or sink the thesis's
  "the profiles are meaningfully distinct" claim. High stakes, both directions.
- **The per-tactic profiles already exist** — the 15
  [`../tactic_profiles/`](../notes/ch3_design/tactic_profiles/) §5 blocks are the single source
  of truth for dwell/behaviour (catalogue consistency constraint). No
  *class-level* characterisation exists yet; that is the new artefact.
- **Some objective-timing extractions already exist** and were the catalogue's
  Tier-2 calibration targets: `docs/sources/extractions/breach_reports_macro_timing.md`
  (Sophos access→exfil ~73–79 h — the held-out milestone),
  `collection_exfil_timing.md` (Bromiley ~64% collect+exfil ≤ 5 h),
  `ransomware_timing.md` (encryption ~6 min–2 h). These are *pooled/generic*
  breach milestones, not per-objective — the point of this handoff is the
  per-class refinement.
- **Calibration is not yet frozen.** The catalogue is v0-uncalibrated; the
  per-tactic provenance rows await Marc's approval and v1 must not freeze
  before that ([`../specs/provenance.md`](../implementation/provenance.md) § L3
  state-duration catalogue). This handoff runs *ahead of* that freeze so the
  criteria can inform what "plausible dwells" means.

## Why a validation set and not a fitting target — the degrees-of-freedom argument

Read this before deciding the shape of the work; it is the load-bearing point.

- The tunable surface is **two global scalars**: the `stealth-low-and-slow`
  anchor (v0 = 45 s) and the `objective-execution` anchor (v0 = 36 s). Tier-1
  tactics are substrate-pinned; every other tactic is a *fixed multiplier* off
  one anchor. Moving the stealth anchor shifts all six stealth-group tactics
  **together, across all four classes** — there is no per-class dwell knob.
- The per-class *behavioural* differences therefore come almost entirely from
  the **W-A weights** (routing) and the **objective set** (termination) — both
  **frozen and grounded**. Bending them to hit a target is exactly the
  circularity [`../specs/metrics_semantics.md`](../implementation/metrics_semantics.md)
  §(f) prohibits.
- Consequence: a model with two global knobs **cannot overfit** four rich
  per-class narratives — which is a strength — but it also **cannot be steered
  per class** to fix a miss. So the criteria are an acceptance gate on the
  frozen structure, and a class-level miss is a documented limitation, not a
  tuning defect. If you find yourself wanting to move a weight to pass a
  criterion, stop: that is the anti-pattern this handoff exists to prevent.

## What a timeline can and cannot express (project criteria onto this before writing them)

A single-token, dwell-summed, tactic-level timeline **can** express:
- tactic **ordering** (which tactics precede which);
- relative **occupancy** (mean dwell share per tactic);
- **net time-to-objective ratios** (cross-class and cross-tactic — never
  absolute hours: shape-not-scale);
- **outcome mix** (objective / stalled / cap rates);
- **which objective(s)** are reached, and the visited-set completion condition.

It **cannot** express (by deliberate modelling choice — do not write criteria
that need these):
- absolute wall-clock (shape-not-scale forbids it);
- concurrency / parallel actions (single token; AND-gates aggregated away at
  structural build — recorded tradeoff);
- data volumes, tooling specifics, actor attribution;
- detection interplay / dwell-before-detection (detection is culled from the
  substrate).

Every literature characteristic must be projected onto the five expressible
axes *before* it becomes a criterion, or it is not testable.

## Recommended approach

**1 — Roll the per-tactic profiles up to the class level first (cheap, keeps
consistency).** Before any new digging, aggregate the existing 15
`tactic_profiles/` §5 blocks into a per-objective sketch: for each class, which
tactics are in its net, which dominate its flows, what the §5 dwell/behaviour
notes already imply about ordering and occupancy. The profiles stay the single
source of truth, so a roll-up is consistent by construction and far cheaper
than a parallel characterisation. Only dig new literature where the *class*
level needs something the *tactic* level cannot supply (e.g. the
double-extortion sequencing of exfil-before-impact, which is a class property,
not a tactic property).

**2 — Characterise each operational objective from the literature (targeted,
per-class).** One extraction per class under
[`../extractions/`](../sources/extractions/) (or extend the three existing
objective-timing extracts). Match the source *to the class*: espionage /
data-theft IR for `pure_steal`; ransomware / wiper timing for
`pure_impediment`; double-extortion playbooks for `double_extortion`;
access-broker / infrastructure-staging reporting for `infrastructure_setup`.
**Anti-circularity:** do not draw on the same case material that defined the
class in GASP L2 — if a source *is* a backing flow, it validates nothing.
Follow the paper-acquisition split (OA/arXiv/blogs → Claude fetches; paywalled
→ Marc's download list). Consider the `dissect-paper` skill for the valuable
ones.

**3 — Pre-register the per-class criteria (the circularity insurance).** For
each class, **before looking at the timeline stats**, commit to expected values
on the five expressible axes: dominant-tactic occupancy ordering; tactics that
must be present / absent; the cross-class net time-to-objective ordering;
expected outcome-mix shape; the correct objective set. Write these into a
committed criteria doc with the source behind each. Pre-registration is what
turns "it kind of matches" into a passed test — the commit that records the
criteria must land *before* the commit that scores them.

**4 — Score the calibrated runner against the criteria (the acceptance gate).**
After the two-anchor calibration produces its candidate v1 dwells, run the
library and check each class's timeline statistics against its pre-registered
criteria. Report pass / partial / fail per class per axis. Fold the **null**
in: each class should match its own signature; the aggregate should read as a
blur of all four (the sharper class-vs-null story the structural test could not
give). Carry the **small-class asymmetry** explicitly — `double_extortion` /
`infrastructure_setup` have 4 dedup flows each, the widest sampling noise and
the thinnest external evidence, so their verdicts are the weakest and must say
so.

**5 — Feed the result into the v1 freeze decision, forward-only.** If the
criteria reveal that "plausible dwells" should differ from the v0 priors,
that feeds the two-anchor calibration *before* freeze. **Freeze L2**: if the
dig suggests a class is mis-defined, record it as a documented limitation, not
a v1 L2 rework (reopening L2 cascades through weights → nets → timelines; out
of scope here — see below).

*Alternatives considered:* (a) keep validating only against the pooled generic
milestones — rejected: they average espionage and ransomware together, so they
cannot test *per-class* fidelity, which is the actual thesis claim. (b) Add
per-class dwell multipliers or unfreeze weights to gain fitting handles —
rejected: buys fit at the cost of the grounding claim and re-introduces the
§(f) circularity. (c) Let the literature dig reopen the L2 class definitions —
deferred: forward-only for v1; the cascade is a separate, larger piece of work.

## Validation gate

Done when:
1. A per-objective characterisation exists for all four classes, sourced,
   with each characteristic **projected onto the five expressible axes** (and
   the un-expressible ones explicitly set aside).
2. A **pre-registered** per-class criteria doc is committed, with the criteria
   fixed in a commit that predates any scoring commit (the anti-circularity
   audit trail).
3. Each class is scored pass / partial / fail per axis against the calibrated
   timeline library, with the null-profile blur check included.
4. Every class-level **miss is written as a characterised limitation** (which
   frozen input — weights / objective set / prefix gap / aggregation — causes
   it), never actioned as a weight edit.
5. The small-class validation-power asymmetry is stated in every verdict that
   touches `double_extortion` / `infrastructure_setup`.
6. The result is connected to the v1-freeze decision (does it move the two
   anchors within their sweep bands, or not?), forward-only, with L2 frozen.

## Hard constraints

- **Never bend the weights or objective sets to pass a criterion**
  ([`../specs/metrics_semantics.md`](../implementation/metrics_semantics.md) §(f)). The
  weights are the grounded input you defend; the two dwell anchors are the only
  tunable surface, and even they tune against the held-out milestone, not
  against these per-class criteria directly.
- **Shape-not-scale throughout** — criteria are orderings/ratios/occupancy,
  never absolute hours
  ([`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/ch3_design/operational_validation.md)).
- **Pre-register before scoring** — the criteria commit predates the scoring
  commit, or the exercise is circular.
- **Anti-circularity on sources** — do not validate a class against material
  that is one of its own backing flows.
- **Envelope-not-actor phrasing** — a class signature is an *envelope*
  characterisation, never "what APT-X does"; the statistic is the **net
  time-to-objective**, never the DES MTTC.
- **Freeze L2 for v1** — the dig is forward-only validation; a mis-defined
  class is a limitation, not a v1 rework.
- **Consistency constraint** — the `tactic_profiles/` §5 blocks stay the single
  source of truth; the class roll-up must agree with them and any
  dissertation.tex §3.1 changes land in the same commit.
- Branch hygiene, **never push without an explicit ask**, Australian English.

## Reading list

- [`../../data/ogasp/timeline/timeline_report.md`](../../data/ogasp/timeline/timeline_report.md)
  — the current behavioural stats the criteria will be scored against (occupancy,
  time-to-objective, outcome mix per class).
- [`../../data/ogasp/petri/divergence_report.md`](../../data/ogasp/petri/divergence_report.md)
  — the negative structural result this behavioural test is meant to answer;
  read the verdict and the small-class null-band note.
- [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/ch3_design/operational_validation.md)
  — shape-not-scale, tiers, held-out milestone, anti-circularity rules — the
  discipline this handoff extends to the class level.
- [`../specs/02_gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md) — the four
  operational-objective class definitions and their objective sets (what you
  are characterising).
- The three existing objective-timing extractions
  (`docs/sources/extractions/breach_reports_macro_timing.md`,
  `collection_exfil_timing.md`, `ransomware_timing.md`) — the pooled milestones
  to refine per-class; and one or two `tactic_profiles/*.md` §5 blocks for the
  roll-up conventions.

## Out of scope (explicitly)

- **Actioning any criterion by editing weights, objective sets, or multipliers**
  — misses are findings, not fixes.
- **Reopening the L2 class definitions** — forward-only validation for v1; the
  class-definition cascade is separate work.
- **The two-anchor duration calibration itself** — that is the v0→v1 freeze
  step (approval-gated on the provenance rows); this handoff *feeds* it and
  *gates* its output, it does not perform it.
- **Absolute-time realism** — shape-not-scale; no criterion targets wall-clock.
- **Feeding timelines into MTDSim** (the replay attacker) and the tactic→action
  binding — separate handoffs.
- **Corpus expansion / the prefix bridge / multi-token concurrency** — the
  standing v1 deferrals.
