---
status: open                  # standing context for the §4.1 drafting passes; retire when the section is drafted and scrutinised
created: 2026-08-21
---

# Standing context for drafting "What an APT attack model must capture" (methodology §4.1) — the frame, the per-unit framework, and the boundaries

> **Mode note, first.** Marc drafts the prose; sessions scaffold and scrutinise.
> [`../workflows/draft_scrutiny.md`](../workflows/draft_scrutiny.md) governs — a
> session that returns finished dissertation paragraphs has failed, however good
> they are. What a session may return: content-point scaffolds, scrutiny findings
> with grounding documents, and skeleton/figure/citation mechanics. Every unit
> travels the drafting pipeline
> ([`../workflows/drafting_pipeline.md`](../workflows/drafting_pipeline.md)):
> Marc dictates, passes 2–3a repair, his marker walk, scrutiny, his compression,
> pass 6 at section level.

## What the section is, in one line

**Criteria before the thing judged.** §4.1 converts ch3's demonstrated need into
(1) a precisely-defined technical problem and the commitments taken against it
(§4.1.1), and (2) a pre-committed, literature-derived yardstick — the eight axes
— that §4.2 builds toward and ch6's fidelity verdict is later scored against
(§4.1.2). The section *poses*; it never scores this project's model.

## State of play

- The skeleton in [`../thesis/dissertation.tex`](../thesis/dissertation.tex)
  (`sec:requirements`, lines ~264–283) is the authority; its comment blocks are
  the ratified per-unit contract (structure per the 11-Aug V-trail, skeleton
  2026-08-12). Two subsections, one unit (~250 words) each:
  `subsec:apt-omission` ("The threat model MTD evaluation omits") and
  `subsec:criterion` ("A fidelity criterion from the APT literature").
- The **chapter opening is a separate, unnumbered block** (~half a unit, shared
  with `sec:requirements`): the live `fig:pipeline` ladder figure plus the
  capture → model → evaluate spine declared once, with the sub-question map in a
  sentence. It is *not* §4.1.1 — Marc's 2026-08-21 dictation recalled §4.1.1 as
  "the chapter preamble", and the skeleton allocates it differently: §4.1.1 is
  the compressed problem definition, a full unit with its own disclosures. If
  Marc wants the preamble/problem-definition fold, that is the structural
  CONFIRM below, not a drift to apply silently.
- **§4.1's output is already load-bearing.** The ratified §4.2 preamble ships
  prose that leans on it: "it aims to tick off the axes from
  Section~\ref{sec:requirements}" and "Now that we have outlined the eight axes
  that we are going to be measuring our model against". §4.1.2 therefore owes a
  numbered, referenceable presentation of the eight axes — and an in-file note
  (line ~332) already flags the \ref choice (`sec:requirements` renders "4.1";
  the axes' exact home is `subsec:criterion`).
- The instrument itself is finished and stable:
  [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  (loaded every session by supervisor direction, S6). Nothing in §4.1 requires
  new analysis — the section is compression and selection, not research.

## The per-unit framework

| Unit | Question it answers | Must-carry content | Disclosures (sentences, never headings) | Grounding |
|---|---|---|---|---|
| Chapter opening (unnumbered, ~½ unit) | how the chapter is organised | spine declared once; sub-question map auditable against V5 (sec:requirements poses; §4.2's first two subsections answer capture, last two model; experimental setup answers evaluate); figure owns the ladder — no prose re-narration | — | dissertation.tex comments (lines ~203–262); [`../notes/_writing_guide.md`](../notes/_writing_guide.md) spine matrix |
| §4.1.1 The threat model MTD evaluation omits | what, precisely, is the technical problem | the ontology gap (intelligence-derived structure vs the simulator's vocabulary); unobservable APT dwell times; the proof-of-concept commitment; the attacker-only substrate scope (network, HARM, mechanisms untouched — *a commitment for comparability, not a caveat*) | ruled exclusions in one sentence (reasons ride ch:futurework); the observability argument's literature half stays in `sec:apt-survey` | [`../notes/ch4_methods/README.md`](../notes/ch4_methods/README.md) (the chapter's two-job statement names all three gaps); [`../implementation/architecture.md`](../implementation/architecture.md) §(a) decisions, §(f) ruled exclusions, §(j) modest claim; [`../notes/ch4_methods/host_simulator_contract.md`](../notes/ch4_methods/host_simulator_contract.md); [`../notes/ch4_methods/structure_to_behaviour_binding.md`](../notes/ch4_methods/structure_to_behaviour_binding.md); [`../notes/ch3_lit_review/tactic_duration_precedent_survey.md`](../notes/ch3_lit_review/tactic_duration_precedent_survey.md) |
| §4.1.2 A fidelity criterion from the APT literature | what an APT attack model must capture, and how we will know | the eight literature-derived axes, by number and name; the epistemic badge vocabulary (demonstrated / designed / conjectured / not addressed); how prior MTD work scores (the cross-section's near-empty column; the inherited attacker is a compromise-loop FSM); the anti-reverse-fitting provenance (axes fixed from the literature *before* the model was scored) | evidential provenance (Row A) and evaluative consequence (Row B), one sentence each, flagged as this project's additions | [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md) §(a) derivation, §(b) badges, §(c) scorecard, §(d2) lettered rows, §(e) fidelity placement; extractions [`cho2020.md`](../sources/extractions/cho2020.md), [`alshamrani2019.md`](../sources/extractions/alshamrani2019.md), [`jalowski2026.md`](../sources/extractions/jalowski2026.md); lit review §IV-B Table II (gitignored source; the parametric → scripted → procedural → behavioural descriptor is **Marc's own instrument** — flag as this project's synthesis, never as a paper's claim) |

## What of the instrument reaches the chapter — selection discipline

The criterion file is ~1,500 lines; the unit is ~250 words. What the chapter
gets: the axes (number + name + one-clause meaning), the badge vocabulary, the
axis provenance (three named sources; the synthesis flagged as editorial), the
prior-work absence, and the rows-A/B sentences. What it does **not** get:

- **Per-axis evidence trails, amendments, dispositions, M8b fields** — ch6
  fidelity-verdict material and repo record. §4.1.2 poses the yardstick blind
  to the answer; even the scorecard's "This model today" column is arguably
  ch6's, not §4.1.2's (see CONFIRM 3).
- **The census-not-scale caveat and the measured axis-3/6/7 tensions** — ride
  wherever the scores are presented, not the posing.
- **The degenerate-region constraint** — ch5's sensitivity preamble owns it.
- **Envelope-not-actor discipline and the modest-claim ceiling** — declared
  where claims are made (§4.2, ch6), not where criteria are posed.

## Boundaries — questions this section must NOT answer

- **What APTs are / how the literature characterises them** — ch3
  `sec:apt-survey` owns the survey, including the observability argument's
  literature half. §4.1 compresses to the axes; it cites, never re-surveys.
- **Why the gap exists** — ch3's gap sentence and strand endings earned it.
- **What the simulator or the baseline attacker is** — ch2 (V7 ruling).
- **Whether this model satisfies the axes** — ch6's fidelity verdict; §4.2 must
  not pre-claim against the yardstick either (badge ceiling:
  `apt_model_criterion.md` rules; *designed* stays designed).
- **What the parameters do to outcomes** — ch5 (V6 regime).
- **Why each exclusion was ruled** — ch:futurework carries reasons; §4.1.1
  carries the one-sentence disclosure only.

## Term and heading rulings

- Sentence case; no acronyms in headings **except** the ratified visible set —
  APT stays visible (Marc's standing heading conventions; both §4.1 headings
  are already ratified as written).
- **"Eight axes", kept simple** — Marc's ruling on the §4.2 preamble: no
  criterion/criteria wordform discussion in prose. The heading's "fidelity
  criterion" is ratified; in running prose "the eight axes" carries.
- **Threat model = genre term, never our model's name** (registry, ratified
  2026-08-20). Its census is pinned at two uses: the §4.1.1 heading and the
  §4.2 preamble opener. §4.1 must not add drifting uses.
- **The naming move belongs to §4.2's preamble**, not §4.1: *movement attacker*
  / *baseline attacker* are introduced there. §4.1 speaks of "an attack model"
  / "attacker models" generically — the registry explicitly licenses generic
  *attacker model* in criterion contexts.
- Full registry: [`../workflows/terminology.md`](../workflows/terminology.md).

## Citation mechanics

- `alshamrani2019` is live in `references.bib`; **`cho2020` and `jalowski2026`
  are drafted but commented out** — uncomment at first cite (Jalowski author
  list already corrected in the comment: Rekosz, Paulina).
- Locators come from the tracked extractions, never invented (guardrails). The
  key anchors: Cho §V-A (four characteristics) and §V-D (three under-developed
  dimensions); Alshamrani §II-A/§II-C (NIST clauses, objective triad, five-phase
  lifecycle); Jalowski §4.3 ("most glaring flaw") and §4.1 (three primitives).
- Lit review Table II lives in `docs/sources/lit_review/LIT_REVIEW.md`
  (gitignored — source markdown is the citable artefact; do not chase URLs).

## Open CONFIRMs for Marc

1. **Subsection split.** His 2026-08-21 dictation queried whether §4.1 needs
   the §4.1.1/§4.1.2 split at all. The skeleton ratifies two units with
   distinct jobs (problem definition vs yardstick), and the §4.2 preamble's
   \ref note already anticipates `subsec:criterion` as the axes' deep anchor.
   Folding them saves a heading, not a unit — the ledger still owes both jobs.
   Recommendation: keep the split; but it is his structure to rule.
2. **The \ref target for the axes** in the §4.2 preamble (`sec:requirements`
   vs `subsec:criterion`) — the line-332 note; falls out of CONFIRM 1.
3. **Does the scorecard (any "this model today" column) appear in §4.1.2 at
   all**, or does §4.1.2 present axes-plus-badges only, with every score
   deferred to ch6? The skeleton comment says "how the inherited attacker
   scores" — the prior-work column — which is posable without self-scoring.
   Where the summary table lands (here, ch6, or both views) is unruled, and it
   is the section's only figure/table candidate: the §4.2 figures programme
   never covered §4.1.

## Validation gate

A unit is done when: ~250 words (one to two paragraphs) drafted by Marc through
the dictation pipeline; its must-carry disclosures present as sentences; then a
scrutiny pass under [`../workflows/draft_scrutiny.md`](../workflows/draft_scrutiny.md)
§(b) with the ch4 pack row, returning at most three prioritised moves. Voice is
Marc's own gate ([`../workflows/voice.md`](../workflows/voice.md)); pass 6 runs
at section level once both units stand.

## Hard constraints

- No prose generation by sessions (draft_scrutiny §a).
- **Never renumber the axes.** Axes 1–8 are cited by number across the
  implementation records and experiment findings; the lettered rows exist
  precisely so numbering never moves.
- **Badge ceiling.** No §4.1 sentence may imply a score the criterion does not
  hold; two of eight axes are NOT ADDRESSED and that visibility is part of the
  instrument, not a tone choice.
- Every axis content-claim carries its paper and locator; the synthesis (axis
  selection, names, the NIST-onto-Cho merge, rows A/B, the fidelity descriptor)
  is flagged as this project's editorial work.
- Ledger conservation: §4.1 holds 2 units plus the shared half-unit opening;
  growth names what it displaces.
- Branch/commit rules per [`../workflows/guardrails.md`](../workflows/guardrails.md).

## Reading list (cold-start order)

1. `dissertation.tex` lines ~200–348 — the chapter opening + §4.1 skeleton
   comments and the ratified §4.2 preamble that leans on §4.1.
2. [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
   — §(a), §(b), §(c), §(d2), §(e) minimum (loaded every session anyway).
3. [`../notes/ch4_methods/README.md`](../notes/ch4_methods/README.md) — the
   chapter's two-job statement (§4.1.1's content in one paragraph).
4. The three extractions (cho2020, alshamrani2019, jalowski2026).
5. [`../workflows/terminology.md`](../workflows/terminology.md) +
   [`../workflows/drafting_pipeline.md`](../workflows/drafting_pipeline.md).
