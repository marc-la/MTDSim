---
status: durable
created: 2026-08-14
updated: 2026-08-14
---

# Draft scrutiny — checking a dissertation draft against the record of what the research actually decided

**Status:** durable. The contract for any session asked to **scrutinise** Marc's
draft dissertation content — or to produce **content points** for a section he will
draft himself — against this repo's corpus. Load this file, then the corpus pack the
map below selects, then the draft. It is the content/intent layer; two sibling
contracts sit below it and are loaded with it when the task reaches prose:
[`critique_protocol.md`](critique_protocol.md) (is the draft well-argued and
well-written in the abstract) and [`voice.md`](voice.md) (how the sentences sound).
This file answers a different question from either: **is this the right content for
*this* research** — the arguments Marc decided to make, the concessions the work
owns, the claims its evidence earns — measured against the record, not against
generic writing principles.

## (a) The one rule that defines the mode — scrutinise, never generate

The corpus is a **yardstick and an evidence base for feedback. It is never a source
of draft prose.** A session that reads the research record or a note and writes
Marc's dissertation section *from* it has violated the mode, however good the prose.
The reason is Marc's, stated when this workflow was commissioned (2026-08-14): the
corpus exists to check whether a draft hit the right argument, the right framing,
and whether an argument is missing — not to generate the dissertation, whose value
is that it is in his voice. Two consequences hold without exception:

1. **Scrutiny returns content points, not text.** A gap is named, its grounding
   document cited, and the drafting is left to Marc — the same T3 rule
   `critique_protocol.md` §(b) enforces for arguments and citations, applied to
   content: *"this section is missing the shape-not-scale defence — see the timing
   note"* is a complete review comment; supplying the paragraph is not.
2. **A cold-draft request is answered with a scaffold, not a section.** When Marc
   asks a session to "cold-draft" a section, the deliverable is the *argument
   skeleton* — which claims the section should make, in what order, each with the
   record document that grounds it and the badge ceiling it must respect — from
   which Marc writes the prose. A session that returns finished paragraphs has
   pre-empted the voice the exercise exists to protect. If in doubt, return points
   and offer to expand any into a scaffold, never into prose.

## (b) The scrutiny question set — run against the pack, in this order

Generic argument quality is `critique_protocol.md` §(d)'s job. This set is what that
one cannot do without the corpus: measure the draft against the *specific* record of
this research. Every finding names the corpus document that grounds it (that is the
"supporting document" a scrutineer attaches), and stops at naming — never drafting.

1. **Intent fidelity.** Does the draft's claim match what the record shows Marc
   decided? The research record's threads and the decision registers are the
   authority on intent. A draft that argues a position the record shows was *reached
   and then abandoned* fails here — flag it, cite the thread, name both dates.
2. **Reversal hygiene.** Is the draft presenting a superseded position, an abandoned
   path, or a killed axis as if it were live? The prompts are dated evidence, never
   current truth ([`../implementation/research_record/`](../implementation/research_record/)),
   and the criterion's dispositions are the current word. Cite the disposition that
   settled it.
3. **Argument completeness.** Is a known argument — one already worked out in a note
   or thread — missing from the draft? This is the highest-value check and the one
   only the corpus enables: the notes are the inventory of arguments the research has
   *earned the right to make*, so a section that omits one is under-claiming its own
   work. Name the missing argument and its note.
4. **Concession coverage.** Does the draft own the concessions the record owns — the
   census framing over a performance race, the survivorship gap in the failure
   overlay, the weakest-link limitation, the declared-parameter honesty? An
   examiner reaches first for a limitation the text could have named
   (`voice.md` §c-5); the discussion notes and the criterion carry the ones this
   work has already conceded. A draft that hides one the record discloses fails.
5. **Badge ceiling.** Does the draft claim more than the evidence earns —
   *demonstrated* where the criterion holds *designed*, *true* where it holds
   *envelope*? The APT criterion
   ([`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md))
   is the authority on what each axis may claim today; the draft may not outrank it.
6. **Evidence grounding.** Is each empirical or technical claim traceable to an
   implementation record, a data artefact, or an extraction — or is it asserted?
   Name the grounding document where one exists (attach it), and flag the claim as a
   citation anchor where none does. Never invent one.

Close with a **priority summary of at most three moves**, as `critique_protocol.md`
§(c) requires — a scrutineer prioritises; forty co-equal content notes is a failure
mode, not thoroughness.

## (c) The corpus map — which documents scrutinise which draft

This is the "add supporting documents to any scrutineer" mechanism: given the draft's
chapter or topic, the pack is the row below. Load the **whole row** — the notes carry
the earned arguments, the research-record threads carry the intent and the abandoned
alternatives, the implementation records carry the technical ground truth, and the
extractions carry the literature a claim must cite. Widen a pack when a draft reaches
across rows; never narrow it below the notes column.

| Draft chapter / topic | Notes (earned arguments) | Research-record threads (intent, reversals) | Implementation / evidence |
|---|---|---|---|
| **ch2 background** — inherited platform | `ch2_background/` | `additive_integration`, `bug_vs_design`, `fairness_boundaries` | `substrate_primer`, `mtdsim_spec`, `metrics_semantics`, the boundary records; extractions `brown2023`, `zhang2023`, `ho2024`, `tay2024` |
| **ch3 literature review** — gap, precedent | `ch3_lit_review/` | `objective_pivot`, `rq_and_structure` | extractions `cho2020`, `alshamrani2019`, `jalowski2026`, `evans2011_mtd_effectiveness`, the timing-precedent extractions |
| **ch4 methods — capture** (corpus → graph → profiles) | `ch4_methods/technique_graph_construction`, `objective_partition_rationale`, `objective_partition_findings`, `cti_corpus_as_snapshot`, `operator_concentration` | `objective_pivot` | `pipeline/gap/`, `pipeline/gasp/` |
| **ch4 methods — model** (movement attacker, binding, timing, overlay) | `structure_to_behaviour_binding`, `operational_validation`, `exponential_as_tractability_choice`, `outcome_overlay_directionality`, `inherited_attacker_flowchart_vs_machine`, `host_simulator_contract`, `bug_or_design_verification`, `uniform_filtering_for_comparison` | `three_layer_seam`, `timing_regime`, `outcome_overlay`, `bug_vs_design`, `fairness_boundaries` | `pipeline/ogasp/` (controller, stochastic timing, overlay design), `architecture`, `apt_model_criterion` |
| **ch4 methods — fidelity extensions** (incentive, learning, stealth, axis 4/8) | (criterion is the spine) | `incentive_rationality`, `learning_capability`, `axis8_rise_and_fall`, `criterion_lifecycle` | `apt_model_criterion`, `pipeline/ogasp/` (incentive, learning, stealth, disengagement records) |
| **ch4 methods — evaluation design / criterion** | `evaluation_burden`, `evaluation_grading`, `operating_point_discrimination` | `comparability_and_census`, `criterion_lifecycle`, `rq_and_structure` | `apt_model_criterion`, `metrics_semantics` |
| **ch5 results** — sensitivity, MTD evaluation | `ch5_results/defence_ranking_inversion` | `comparability_and_census` | `pipeline/ogasp/` experiment findings, the sweep records, `data/ogasp/` |
| **ch6 discussion** — interpretation, limitations | `ch6_discussion/` (all) | `movement_objectives`, `comparability_and_census`, `axis8_rise_and_fall` | `apt_model_criterion`, the measured-negative records |
| **ch7 future work** | `ch7_future_work/successor_programme` | `axis8_rise_and_fall`, `movement_objectives`, `learning_capability`, `incentive_rationality` | `apt_model_criterion` (reopening conditions) |
| **RQ / structure / whole-document** | `_writing_guide` | `rq_and_structure` | `pipeline/ogasp/supervisor_decision_register` (V-series) |

Repo-relative homes: notes under [`../notes/`](../notes/); threads under
[`../implementation/research_record/threads/`](../implementation/research_record/threads/);
implementation under [`../implementation/`](../implementation/); extractions under
[`../sources/extractions/`](../sources/extractions/). When a needed argument is not
in any pack, that is itself a finding — the draft may be making a point the research
has not yet earned, or a note is owed before the section can be written.

## (d) Fanning to scrutineer subagents

For a long draft, or for breadth, the scrutiny may be fanned: each subagent gets
**this file, the relevant pack row, and the draft**, and returns content points
under §(b) only. Two rules keep the fan honest:

- **Each subagent is a scrutineer, not a co-author.** The §(a) no-generation rule
  binds every one of them; a subagent that returns drafted prose is discarded, not
  merged.
- **The pack travels with the draft, always.** A scrutineer without the corpus row
  gives generic feedback — exactly the broad, ungrounded review this workflow exists
  to replace. Grounding is the point: the feedback a scrutineer gives is only as
  relevant as the supporting documents it holds.

## (e) What this is not

- **Not generation.** Restated because it is the whole point (§a).
- **Not prose review.** Sentence rhythm, tells, and voice are `voice.md` and
  `critique_protocol.md`; a scrutiny pass may note a §(b) content gap inside a
  paragraph but leaves the wording to those contracts.
- **Not a re-decision.** Where a draft contradicts the record, the finding is a
  *flag* for Marc, never a correction — the same rule the research record runs on:
  the record is dated evidence, a draft is Marc's current intent, and where they
  disagree he rules. A scrutineer that "fixes" the draft to match an old thread has
  inverted the hierarchy.
