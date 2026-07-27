---
status: open
created: 2026-07-27
---

# Build the APT-attacker-model criterion — a structured, literature-derived rubric of what an APT attacker model should capture, this model scored against it honestly, and the artefact wired into every session's context

**Chain position: wave 1 — run first, independently.** Nothing blocks it, and
everything after it benefits: this is the yardstick the later work is scored
against, and the supervisor asked for it to be loaded into every future session.
Executes **S6**.

## State of play

**The ruling.** The supervisor's question is the project's headline: *what does
this model capture about APT attackers that prior models do not?* The direction
is to return to the reviewed APT literature and build a **structured criterion /
rubric** from it, score this model against it, and use it to benchmark the work
over the coming weeks. Two constraints ride with it: the artefact must be
**loaded into the context of every future session**, and it must **not promise
the world** — this model will not satisfy every axis, and the claim is that it
captures the *missing essence* the literature names, not that it closes the gap.

**The three named sources are already extracted, and each supplies a different
part of the instrument.** Do not re-read the papers from scratch; start from the
extractions, which carry locators.

- **Cho 2020** ([`../sources/extractions/cho2020.md`](../sources/extractions/cho2020.md))
  supplies two things: §V-A's four sophisticated-attacker characteristics
  (persistent, adaptive, stealthy, incentive-driven) and §V-D's three
  under-developed dimensions of the attacker model (the smart/learning attacker
  is seldom modelled; multi-strategy scenarios are scarce; the rational-actor
  framing is applied to defenders but not attackers). The four characteristics
  are the natural **axes**; the three dimensions are the **gap** the axes are
  meant to expose.
- **Jalowski 2026** ([`../sources/extractions/jalowski2026.md`](../sources/extractions/jalowski2026.md))
  names the attacker model "the most glaring flaw in the MTD literature", rejects
  Nmap-style active-scanning baselines as too naive for APT, and prescribes an
  attacker that reasons about the MTD scheme itself. Its §4.1 supplies three
  concrete primitives (state-collision recognition, MTD-event-as-beacon,
  metadata-shadow invariance) which
  [`../implementation/architecture.md`](../implementation/architecture.md) §(f)
  already carries as *pending encoding* — those are ready-made rows in the
  honest-negatives column.
- **Alshamrani 2019** ([`../sources/extractions/alshamrani2019.md`](../sources/extractions/alshamrani2019.md))
  supplies the enumeration: the three-property definition, the NIST behavioural
  clauses (pursues objectives repeatedly over an extended period; adapts to
  defender resistance; maintains the interaction needed), the five-phase
  lifecycle with its invariant prefix and objective-conditioned suffix, and
  §II-B's "what is NOT an APT" boundary.

**Marc's own instrument already exists in draft.** The lit review's §IV-B builds
a cross-section scoring the surveyed threat models against Cho's four
characteristics *plus a constructed fidelity descriptor* (parametric / scripted /
procedural / behavioural). That table is the spine this criterion should extend,
not replace — it is Marc's own contribution and the examiner will recognise it.
The lit review is at `docs/sources/lit_review/` (gitignored, readable).

**What the model can honestly claim today** — the inputs to the scoring column:
the first coupled experiment's result and its two failure modes
([`../implementation/pipeline/ogasp/experiment_01_findings.md`](../implementation/pipeline/ogasp/experiment_01_findings.md)),
the CTI-derived movement structure, the objective-conditioned profiles, and the
declared-policy routing. What it cannot claim: any of the three Jalowski
primitives, attacker learning, MTD-scheme awareness, and — on the evidence of
experiment 1 — sustained multi-stage progress on this substrate.

## Recommended approach

1. **Derive the axes from the literature, not from the model.** Build the axis
   set before looking at what this model does, so the rubric cannot be
   reverse-fitted to flatter it. Cho's four characteristics and Alshamrani's NIST
   clauses are the obvious spine; Jalowski's primitives and the fidelity
   descriptor are the depth dimension. Aim for a small number of axes that each
   discriminate — a rubric with twenty rows nobody reads is worse than one with
   six that an examiner can argue with.
2. **Give every axis the same five fields:** what it is (with its source and
   locator), why it matters for *MTD* evaluation specifically, how prior MTD work
   scores on it (from the lit review's cross-section), how this model scores
   today, and — the fold-in below — what measurement would evidence a claim on
   that axis.
3. **Fold in the deferred metrics-gap review (M8b).** The retired first-numbers
   handoff left one item open: identify the supplementary measurements that would
   show where APT-shaped behaviour matters, given that the current suite cannot
   see it. That belongs here rather than in a separate document, because the
   criterion is exactly the place where "we claim axis X" meets "here is what
   would demonstrate axis X". Recommend, do not build.
4. **Score honestly, and make the negatives as visible as the positives.** Every
   axis carries one of *demonstrated* / *designed* / *conjectured* / *not
   addressed*, and the not-addressed rows are not buried. The supervisor's
   "isn't promising the world" is a hard requirement of the artefact, not a tone
   preference.
5. **Place it and wire it.** Recommended placement is
   `docs/implementation/apt_model_criterion.md`, promoted to the *read-first*
   list in [`../../CLAUDE.md`](../../CLAUDE.md) and registered in
   [`../workflows/docs_map.md`](../workflows/docs_map.md) in the same commit.
   *Alternatives considered:* `docs/workflows/` — rejected, that subtree is
   session working rules, and this is a claim about the model; `docs/notes/` —
   rejected for the primary artefact, because the scored rows cite repo
   artefacts and would fail the notes rubric's supervisor test. A distilled,
   rubric-clearing note for the background or discussion chapter is the natural
   *second* artefact, and is explicitly deferred until the criterion exists.

## Validation gate

Done when:

1. The criterion exists as a single self-contained document with every axis
   carrying the five fields above, and every literature claim traceable to an
   extraction with a locator (no uncited axis, no locator invented).
2. This model is scored against every axis with an explicit epistemic badge, and
   the axes it does not address are present and unhidden — including the three
   Jalowski primitives and attacker learning.
3. Each axis this model *claims* names the measurement that would evidence it —
   the M8b metrics-gap recommendation, delivered in criterion form rather than as
   built metrics.
4. Experiment 1's result is scored against the criterion, so the rubric is
   demonstrated to discriminate rather than merely asserted to.
5. `CLAUDE.md` and `docs_map.md` are updated in the same commit, so the next
   cold session loads it without being told to.

## Hard constraints

- **Cite or flag, never assert.** Guardrails: never claim a paper says something
  it does not; never invent a locator; one paper per pass when working across
  several. Where an axis is Marc's synthesis rather than a paper's claim, label
  it as such — the fidelity descriptor already is.
- **The modest-claim ceiling.** The defensible claim remains *behavioural
  fidelity changes the answer*, not *the attacker model is true*
  ([`../implementation/architecture.md`](../implementation/architecture.md) §(j)).
  The criterion must not quietly upgrade it.
- **Envelope, not actor** phrasing throughout.
- No new metrics code, no experiments, no changes to the model to improve a
  score. Australian English; branch hygiene; never push without an explicit ask.

## Reading list

- [`../sources/extractions/cho2020.md`](../sources/extractions/cho2020.md),
  [`../sources/extractions/jalowski2026.md`](../sources/extractions/jalowski2026.md),
  [`../sources/extractions/alshamrani2019.md`](../sources/extractions/alshamrani2019.md)
  — the three sources, with locators.
- `docs/sources/lit_review/LIT_REVIEW.md` §IV-A/§IV-B — the gap statement and the
  existing cross-section table this criterion extends.
- [`../implementation/architecture.md`](../implementation/architecture.md) §(f)
  (the pending Jalowski primitives), §(j) (the positioning the criterion gives a
  yardstick to), §(l) (the open question this closes).
- [`../implementation/pipeline/ogasp/experiment_01_findings.md`](../implementation/pipeline/ogasp/experiment_01_findings.md)
  — what the model has actually been shown to do.
- [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
  §S6 and §M8.

## Out of scope (explicitly)

- Dissertation chapter prose. The distilled note is a follow-up, written only
  once the criterion exists and only if it clears the notes rubric.
- Building any supplementary measurement. Recommend them; do not implement.
- Changing the model, the weights, the mapping, or the metrics to score better.
- Expanding the literature survey. Use the reviewed corpus; if an obviously
  load-bearing APT-model source is missing, note it for a separate extraction
  pass rather than chasing it here.
