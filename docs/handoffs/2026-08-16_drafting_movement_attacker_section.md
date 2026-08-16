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
- Open micro-flag left to Marc: "attack graphs" (plural) in the L0–L1 heading vs
  the single aggregated technique graph L1 actually produces.

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

## Loose thread

One-line heads-up owed to Jin in the next update: the dissertation's L3/L4 tokens
now mean formalism/traversal, while the register trail he has been ruling on uses
L3 = execution model.
