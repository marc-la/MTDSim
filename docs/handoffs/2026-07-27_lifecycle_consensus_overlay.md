---
status: open
created: 2026-07-27
---

# Build the APT-lifecycle consensus overlay — overlay the published attack-lifecycle models onto the ATT&CK tactics, extract their consensus ordering, and express it as a declared tactic-to-tactic distance model ready to ground the transition weights

**Chain position: wave 1 — run first, independently.** A literature pass with no
code and no dependency on the other handoffs. Its output is the input to the
weight re-derivation
([`./2026-07-27_tactic_weight_sensitivity_study.md`](./2026-07-27_tactic_weight_sensitivity_study.md)),
which should not start until this lands. Executes the literature half of **S1**.

## State of play

**The defect this is answering.** The tactic-pair routing weights grade a
transition by *direction* — forward, lateral, backward, read off a five-band
kill-chain prior — and by whether the source tactic *enables* the destination.
Neither term is sensitive to **how far** a transition travels. So
`reconnaissance → impact` and `reconnaissance → initial-access` are both simply
"forward", and a jump across the entire campaign lifecycle carries mass
comparable to a step to the adjacent phase. The supervisor named this directly:
the current numbers are not realistic, *large jumps in tactics* being the
example. The directed fix is a **literature-based dependency** — close jumps
weighted higher, far jumps weighted close to or exactly zero.

**Why the grounding is a separate handoff.** The values must not be reasoned
into existence by this project and then presented as literature-based. The
supervisor's instruction is specific about the method: **overlay the lifecycle
models, see what the consensus is, and only then fold that consensus into the
weights.** Keeping the consensus artefact separate from the weight edit is what
makes that auditable — and it is the same discipline the declared-value ledger
already sets out
([`../implementation/declared_value_provenance.md`](../implementation/declared_value_provenance.md)).

**What already exists in the repo, and must be reconciled rather than
duplicated:**

- The **ATT&CK → CKC crosswalk** is already drawn and used — the seven Lockheed
  phases mapped to the fifteen tactics, in
  [`../implementation/pipeline/ogasp/controller.md`](../implementation/pipeline/ogasp/controller.md)
  §1 and `data/misc/_viz/ckc_layer_viz.py`. This is the primary overlay the
  supervisor named; it is not new work, it is work to *cite and check*.
- The **five-band prior** (0 prep, 1 intrusion, 2 consolidate, 3 expand,
  4 objective) in
  [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  §2.1 is already a coarse consensus ordering — declared, not sourced. Part of
  this handoff's value is deciding whether the bands survive the overlay, get
  re-cut, or are replaced by a finer ordering.
- **Alshamrani 2019** ([`../sources/extractions/alshamrani2019.md`](../sources/extractions/alshamrani2019.md))
  supplies the five-phase lifecycle *and* records that it consolidates
  Mandiant's seven-stage and Ussath's three-stage models — so one extraction
  already carries three lifecycles, with the load-bearing structural claim that
  phases 1–2 are invariant while 3–5 are objective-conditioned.
- **ATT&CK itself imposes no ordering.** That is why the direction has to be
  imported at all (recorded as **M3**), and it must stay stated as an assumption
  of this work rather than a property of ATT&CK.

**Candidate additional lifecycles — verify before citing.** The supervisor
invited "many other APT lifecycles in the literature". Check the existing
extraction set first, since several adjacent papers may already carry lifecycle
material: `al-sada2024`, `sadlek2022`, `buechel2025`, `bianco2013`,
`adversary_emulation_frameworks`. Anything beyond those is a fresh extraction —
one paper per pass, per the guardrails, and flagged `unverified` until read
rather than cited from memory.

## Recommended approach

1. **Fix the target representation first.** Decide what the artefact must
   produce before reading: a **distance** `d(a, b)` over ordered tactic pairs, or
   an **ordering** (a rank per tactic) from which distance is derived. Recommend
   the ordering — it is what lifecycle models actually publish, it degrades
   gracefully when two models disagree, and distance falls out of it. Distances
   over a directed pair also need a sign convention: forward distance and
   backward distance are not the same quantity and should not collapse.
2. **One model per pass, into a common frame.** For each lifecycle, record its
   phases verbatim with a locator, then map each phase onto the fifteen ATT&CK
   tactics as a separate, explicit step. The mapping is where the interpretive
   work lives — do it once per model, visibly, rather than smuggling it into an
   aggregate.
3. **Take the consensus without erasing the disagreement.** Where models agree
   on relative order, that is the consensus and it is strong evidence. Where they
   disagree — the usual candidates being where persistence sits relative to
   lateral movement, and whether command-and-control is a phase or a continuous
   activity — **record the disagreement and resolve it by a stated rule**, not by
   averaging. A rubric that hides its disagreements cannot be defended when an
   examiner names one.
4. **Derive the distance model, and demonstrate it on worked pairs.** State the
   functional form and its declared parameters, then show it on the pairs that
   motivated the work: `reconnaissance → impact` must fall to near zero,
   `reconnaissance → initial-access` must stay high, and a plausible backward
   move must not be indistinguishable from an implausible one.
5. **Write the record, and stop.** Deliverable is the consensus artefact plus its
   provenance row — *no weight values change in this handoff*. The fold-in is the
   next handoff's job, and keeping the seam clean is what lets the sensitivity
   study vary the distance model independently.

*Alternatives considered:* folding grounding and re-derivation into one pass —
rejected, it makes the literature step unfalsifiable, because any awkward
consensus could be quietly softened while editing the values. Deriving distance
from the corpus's observed transitions — rejected on principle: that is the
CTI-independence boundary, and it would make the weights a function of the very
nets they route.

## Validation gate

Done when:

1. Every lifecycle used is cited to an extraction with a section-level locator,
   and any newly-read paper has its own extraction record.
2. Each model's phases are mapped onto the fifteen tactics explicitly, with a
   per-cell justification or an explicit `verify` flag — no silent cells.
3. The consensus ordering exists, with the disagreements listed and each
   resolved by a stated rule.
4. A distance model exists with a declared functional form, named parameters,
   and worked examples demonstrating the near/far behaviour the ruling asks for.
5. The record states plainly what is *sourced* and what is *declared* — the two
   must be separable by a reader, since the sensitivity study will sweep only the
   declared part.
6. A provenance row exists in
   [`../implementation/provenance.md`](../implementation/provenance.md), and no
   weight artefact has been edited.

## Hard constraints

- **The distance model is declared knowledge, not a fit.** It must not be tuned
  so that any profile's net traverses well; the CTI-independence boundary in
  [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  §1 is the operative rule.
- **Never assert a paper wrong, and never resolve a disagreement by declaring one
  model authoritative without saying so.** Flag, record, choose with a rule.
- **ATT&CK's lack of ordering stays an assumption of this work** (M3), stated
  wherever the ordering is used.
- Docs and data only — no simulator or net-build code. Australian English;
  branch hygiene; never push without an explicit ask.

## Reading list

- [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  §2 and §2.6 — the value model the distance term enters, and what S1 changes.
- [`../implementation/pipeline/ogasp/controller.md`](../implementation/pipeline/ogasp/controller.md)
  §1 — the ATT&CK → CKC crosswalk already in use.
- [`../sources/extractions/alshamrani2019.md`](../sources/extractions/alshamrani2019.md)
  — the five-phase lifecycle and the models it consolidates.
- [`../implementation/declared_value_provenance.md`](../implementation/declared_value_provenance.md)
  — the ledger format a declared model has to meet.
- [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
  §S1 and §M3.

## Out of scope (explicitly)

- Editing any weight value or regenerating the pair tables — the next handoff.
- The sensitivity sweep.
- Dynamic, attacker-state-conditioned weights: named in S1 as the eventual
  direction and explicitly deferred.
- Re-opening the base flow-proportion weights (D3). This work touches the
  *policy* layer only; the corpus-derived structure is not in play.
