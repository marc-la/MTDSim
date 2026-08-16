---
status: open                  # standing context for the §4.2 drafting passes; retire when the section is drafted and scrutinised
created: 2026-08-16
---

# Standing context for drafting "The movement attacker" (methodology §4.2) — the ratified frame, the per-unit speaking framework, and the boundaries

> **Mode note, first.** Marc drafts the prose; sessions scaffold and scrutinise.
> [`../workflows/draft_scrutiny.md`](../workflows/draft_scrutiny.md) governs — a
> session that returns finished dissertation paragraphs has failed, however good
> they are. What a session may return: content-point scaffolds, scrutiny findings
> with grounding documents, and skeleton/figure/citation mechanics.

## State of play

The section's frame was workshopped and **ratified 2026-08-16** (merged to `dev`
at `b4d3ea4`). The skeleton in
[`../thesis/dissertation.tex`](../thesis/dissertation.tex) (`sec:movement-attacker`)
is the authority — its comment blocks carry the full per-unit contract and are
deliberately written as the drafting brief. What was settled:

- **The thesis ladder (Marc's ruling).** The dissertation presents the model's
  *logical* ladder: L0–L1 intelligence→graph, L2 profiles, **L3 = the GSPN
  formalism**, **L4 = the attacker-agent traversal in MTDSim**. Evaluation carries
  **no layer number** — it is the manipulation of the L4 object. This deviates
  from the repo's numbering (repo-L3 = OGASP traversal, repo-L4 = evaluation);
  the divergence is recorded once in
  [`../implementation/architecture.md`](../implementation/architecture.md) §(b).
  **Do not "correct" either document family to the other.** The chapter-opening
  pipeline figure is the definition of the thesis ladder.
- **Four subsections, five units:** L0–L1 (1 unit), L2 (1), L3 (1), L4 (2 — the
  fold of the former Parameterisation + Traversal-and-the-controller units). Any
  subsubsection heading added at drafting is a new unit claim on the writing-guide
  ledger; the L4 fold holds exactly two.
- **Section preamble:** unnumbered, a few sentences, no unit claim. It owes two
  things only — the naming move (*movement attacker* for the proposed model,
  *baseline attacker* for the inherited scripted attacker; V5-consistent) and the
  one-sentence end-to-end orientation (structure → parameters → execution). No
  ladder re-narration: the chapter-opening figure owns the ladder.
- **Placeholder figure** `fig:pipeline` (controller-action PNG) sits at the
  chapter opening until the box-and-flow pipeline figure is drawn to the thesis
  ladder. Caption to be rewritten long and self-contained at the figures pass.

## The purpose of the section, and the framework per unit

**One line: the build told end-to-end, structure → parameters → execution** — how
published CTI became an executable attacker, as simply as the material allows.
Selection discipline: relevant-and-interesting only; the full implementation
record stays in the repo. The problem definition is NOT this section's job
(`sec:requirements` already did it).

| Unit | Question it answers | Must-carry disclosures | Grounding |
|---|---|---|---|
| L0–L1 technique graph | how campaigns become structure | consensus thresholds; what the graph cannot represent | `notes/ch4_methods/technique_graph_construction.md`, `cti_corpus_as_snapshot.md` |
| L2 attack profiles | how structure becomes objective-conditioned | objective over motivation; the four classes; operator concentration | `objective_partition_rationale.md`, `objective_partition_findings.md`, `operator_concentration.md` |
| L3 GSPN formalism | why this formalism | alternatives ranked one sentence each (feasibility study behind it); synthetic pre-intrusion structure; entry-point selection (D8) | `implementation/pipeline/ogasp/petri_feasibility.md`, `stochastic_timing_design.md` |
| L4 traversal (2 units) | where the numbers come from + how the net drives the simulator | corpus sparsity; dwell standard-of-evidence; sweep pointer at ch5 (never restated); mapping-as-chosen-input-parameter; routing ablatability | `structure_to_behaviour_binding.md`, `operational_validation.md`, `exponential_as_tractability_choice.md`, `pipeline/ogasp/controller.md` |

The two commitments the L4 fold must not lose (from the 2026-08-12 merge, carried
through the 2026-08-16 fold): **the tactic-to-verb mapping as a chosen input
parameter** (the standing caveat bounding every results-chapter claim) and
**routing ablatability** (null modulator bit-identical to no-modulator).

## Boundaries — questions this section must NOT answer

- **What the simulator is** — ch2 Background (supervisor ruling V7). The preamble
  names the baseline attacker in a sentence; it never re-describes it. The section
  reads as a *backwards join onto the ch2 substrate*.
- **Whether the model is faithful** — ch6's fidelity verdict. The criterion
  subsection before §4.2 poses the yardstick; §4.2 must not pre-claim against it
  (badge ceiling: *designed* stays designed — `apt_model_criterion.md` rules).
- **What the parameters do to outcomes** — the ch5 sensitivity preamble (V6:
  declare, sweep, show movement). §4.2 declares and points.
- **Why the gap exists** — ch3 and `sec:requirements` already earned it.

## Term and heading rulings (from the 2026-08-09 + 2026-08-16 workshopping)

- Sentence case; **no acronyms in headings** (spelled-out forms ratified:
  *cyber threat intelligence*, *generalised stochastic Petri-net*). L-prefixes
  are wanted signage.
- **"Generalised"**, never "general", stochastic Petri net — GSPN semantics
  *executed, not solved* (`stochastic_timing_design.md` §1).
- *Movement attacker* / *baseline attacker* is the ratified naming pair.
- ~~Open micro-flag~~ **Ruled (Marc, 2026-08-16): "attack graph" singular** in the
  L0–L1 heading — applied in the skeleton ("…to an attack graph").

## The drafting pipeline (ratified in practice, 2026-08-16, on L0–L1)

**Promoted to durable:** [`../workflows/drafting_pipeline.md`](../workflows/drafting_pipeline.md)
is now the authority (Marc adopted the pipeline for all future drafting; this
handoff retires with §4.2, the pipeline does not). Summary kept below for
this section's sessions; on any divergence the workflows file wins.

Five drafts per unit; **no pass after draft 1 writes prose** — that is what keeps
the voice Marc's. Sequencing ruling: pilot one unit through all five (L0–L1,
done), then batch drafts 1–2 for the remaining units while warm, then convert
in a run.

1. **Speak** the argument long (aim ~2–3× budget), transcribe raw.
2. **Transcription repair + register 3a** (session task, bundled 2026-08-16 as
   the `repair-dictation` skill — invoke it on any raw transcript): STT errors
   fixed with technical vocabulary watched hardest, disfluencies and pads
   dropped, run-ons split, meta-narration beheaded, hedges flagged as `[3b]`
   markers never resolved; verify watchlist + change log returned. Scrutiny
   rounds run interleaved as `[comments]` (see the scrutinise-draft skill's
   inline-annotated format).
3. **Register pass** (Marc, ~15 min/unit): four Ctrl+F sweeps — pads deleted,
   run-ons split, hedges resolved to confidence or scope, meta-narration
   beheaded. One-touch rule: delete/split/word-repair only, never rewrite a
   sentence; if it needs rewriting, mark `% P5?` and leave. Read-aloud check:
   sounds like Marc being careful, not a journal.
   **Ratified split (2026-08-16):** *3a* (session): detection + pure
   deletion/splits only — pads deleted, run-ons split at conjunctions with
   clause order untouched, meta-narration beheaded where the next sentence
   stands; every hedge flagged as a `[3b]` marker, never resolved; zero
   synonyms, zero reordering. *3b* (Marc): walk the `[3b]` markers (each is a
   binary or a word choice), rule the globals (contractions, second person),
   read aloud. Rationale: deleting Marc's words can't inject a session's; the
   AI-flatten risk lives in repairs-that-choose-words, so those all route to 3b.
4. **Content scrutiny** (session task): `/scrutinise-draft` on the unit, ≤3
   moves. Runs after register, before compression; re-run cheaply if
   compression cuts >half.
5. **Compression** (Marc): per sentence, one binary — "does the unit still
   answer its question without this?" Cut order: duplicates → re-explanations →
   second examples → covered qualifiers. Never cut: must-carry disclosure
   sentences, numbers, citations. Sentence fusion allowed only once cuts stall.

## Validation gate

A unit is done when: (~250 words, 1–2 paragraphs) drafted by Marc; its must-carry
disclosures present as sentences (never new headings); then a scrutiny pass run
under `draft_scrutiny.md` §(b) with the ch4-methods-model pack row, returning at
most three prioritised moves. Voice is Marc's own gate
([`../workflows/voice.md`](../workflows/voice.md)).

## Hard constraints

- No prose generation by sessions (draft_scrutiny §a).
- No renumbering of repo docs/code/data to the thesis ladder (architecture §(b):
  ruled disproportionate).
- Ledger conservation: the section holds 5 units; growth names what it displaces.
- Branch/commit rules per [`../workflows/guardrails.md`](../workflows/guardrails.md).

## Loose threads

- One-line heads-up owed to Jin in the next update: the dissertation's L3/L4 tokens
  now mean formalism/traversal, while the register trail he has been ruling on uses
  L3 = execution model.
- **From the 2026-08-16 L0–L1 drafting passes:**
  - Marc owes a **brief appendix entry** on the co-occurrence preliminary runs
    (single-digit edge counts above a confidence threshold) — it anchors the
    abandonment claim in §4.2.1, which cites it as "Appendix [X]".
  - The **ATT&CK v19.1 pin lost its in-section home** when Marc cut the
    staleness/taxonomy passage from §4.2.1; the pin must surface elsewhere
    (experimental setup is the natural spot) — it is a reproducibility datum.
  - ~~Consensus-thresholds must-carry~~ **Resolved by evidence (2026-08-16):**
    Marc signed the unit off without it, confirming the earlier "not that
    interesting" ruling; the skeleton comment is amended (disclosure list now
    "what the graph cannot represent" only). The lossless/views record stays in
    the repo (`gap_schema.md` Decision 3).
  - **L0–L1 pilot complete through pass 5 (2026-08-16), signed off at ~400
    words.** Open on the unit: the ~1.6-unit ledger overdraft (further cut or
    an explicit named overdraft at the ledger pass); the 80% confidence
    threshold CONFIRM; both appendix entries. **Flag for the L3 drafting:** the
    cycles-preserved sentence was cut from L0–L1 at pass 5, so L3 must
    introduce loop preservation itself — readers default to assuming attack
    graphs are acyclic.
  - Ruled out of §4.2.1 at drafting, on the record: the Tesla worked example
    (word count), the staleness/map-not-milk passage, the L2 bridge sentence
    (bridges live at the start of each subsection), and — **ruled twice, do
    not re-flag** — the defender-validity argument and the "observability
    boundary" naming (Marc, 2026-08-16: the limitation's "so what" is the
    synthetic pre-intrusion structure, which is the L3 unit's disclosure;
    stating the defence in L0–L1 is premature elaboration. The unit ends on
    the forward pointer; if the term is wanted, L3 or ch6 coins it. This
    supersedes the technique_graph_construction note's ch4 placement of the
    threat-model-input reframe for this unit).
