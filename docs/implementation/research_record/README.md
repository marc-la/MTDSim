---
status: living
created: 2026-08-14
updated: 2026-08-14
---

# Research record — the annal mined from Marc's own prompts

**What this is.** The durable record of the research *process* — intent, reversals,
and abandoned paths — mined from the session-transcript corpus under
[`../../handoffs/2026-08-06_research_record_from_prompt_corpus.md`](../../handoffs/2026-08-06_research_record_from_prompt_corpus.md).
The premise, Marc's own: **the prompts are the record of human intent; the
assistant's output is an execution layer.** Where the two disagree about what the
research was, the prompts win. Shipped records describe what *is*; this subtree
owns what was tried, dropped, reversed, and why — the negative space no other
document holds.

**What it is not.** Not a diary (`git log` is the chronological record), not a
substitute for the decision registers, and never an authority over a shipped
record: where an old prompt and a current record disagree, the disagreement is
*flagged* in [`dispositions.md`](dispositions.md) and ruled on by Marc, exactly as
a candidate bug is.

## Contents

- [`dispositions.md`](dispositions.md) — every prompt in the ≥ 150-word band
  (107, chronological), each with band, disposition, thread, and a paraphrase
  summary. The audit trail for the claim "the corpus has been read", and the key
  (by `uuid`) for re-running the mining against only the prompts added since.
- [`threads/`](threads/) — one file per decision that moved. A thread states what
  was asked and when, what was decided, **what was abandoned and why**, and where
  it landed. Threads fully covered by shipped records collapse to pointers.

## Provenance and mechanics

- Extractor: [`tools/prompt_corpus.py`](../../../tools/prompt_corpus.py)
  (committed, gated). This pass read the uuid-deduplicated **union of the
  2026-08-08 and 2026-08-14 snapshots** at `~/mtdsim-corpus-snapshot/` —
  107 prompts / 79 698 words (7 Apr / 47 Jul / 53 Aug).
- **The live store loses transcripts silently** (nine on 2026-08-08; a further
  July shrinkage of 14 ≥ 150-word prompts by 2026-08-14). Fourteen prompts in the
  table survive only in the 2026-08-08 snapshot. **Snapshot before every mining
  session**; never trust the live store as an archive.
- **May–June 2026 blackout:** zero transcripts against 92 `dev` commits. That
  window was introduction and literature-review work, out of this record's scope
  by Marc's direction — a boundary with an explanation, not data loss. Do not
  reconstruct it.
- **Third-party content** (supervisor emails, meeting transcripts, pasted AI
  chats) is paraphrased and attributed as dated direction, never quoted into this
  tracked tree. Verbatim text lives only in the untracked snapshots.
- **Prompts are dated evidence, never current truth.** Every claim here carries
  its prompt's date; a reversed position is recorded *as* reversed, with both
  dates.

## The threads, in one line each

| File | The decision that moved |
|---|---|
| [`threads/additive_integration.md`](threads/additive_integration.md) | Wrap, never modify: bit-identity of the inherited path, from April's demo plan to the golden oracle and the dev/main split |
| [`threads/abandoned_visualisers.md`](threads/abandoned_visualisers.md) | The interactive GAP/replay visualiser programme — built through April, dropped whole in June |
| [`threads/objective_pivot.md`](threads/objective_pivot.md) | APT-group/motivation profiling → operational-objective classes; process-mining ingestion dropped; the classification-verification worry |
| [`threads/timing_regime.md`](threads/timing_regime.md) | Dwell times: calibration refused, declaration adopted, exponential veneer owned, S3-R hands all time to the movement layer |
| [`threads/outcome_overlay.md`](threads/outcome_overlay.md) | The success/failure weight overlay: directionality without a kill-chain, survivorship-aware, adversarially scrutinised |
| [`threads/three_layer_seam.md`](threads/three_layer_seam.md) | Movement / controller / action coined; controller as owned concession; the alignment dial |
| [`threads/comparability_and_census.md`](threads/comparability_and_census.md) | Two framing reversals: cross-paper comparability abandoned; performance race reframed as capability census |
| [`threads/bug_vs_design.md`](threads/bug_vs_design.md) | "Is what you are fixing actually a bug?" — the literature-only intent spec as arbiter |
| [`threads/incentive_rationality.md`](threads/incentive_rationality.md) | Incentive: mechanism sought, nothing to be rational toward, resolved as a measurement (disengagement) |
| [`threads/learning_capability.md`](threads/learning_capability.md) | Learning: MVP → recon-bias failure → representation → credit signal; the in-flight exploit-learning mechanism |
| [`threads/axis8_rise_and_fall.md`](threads/axis8_rise_and_fall.md) | The smart-APT/side-channel vision, the Tay retrain ambition, and the kill on calibration circularity |
| [`threads/movement_objectives.md`](threads/movement_objectives.md) | The churn diagnosis, the weakest-link concession, and the refusal to optimise toward the baseline |
| [`threads/fairness_boundaries.md`](threads/fairness_boundaries.md) | "A fair contest": the three-seam boundary programme (pointer-collapsed — the records are shipped) |
| [`threads/criterion_lifecycle.md`](threads/criterion_lifecycle.md) | The APT criterion as instrument: genesis, Marc's own axis vocabulary, the badge pushes, the kills |
| [`threads/rq_and_structure.md`](threads/rq_and_structure.md) | The research question and the document: single RQ → capture/model/evaluate; the background-chapter ruling; the unit ledger |

## Re-running the mining

A second pass is owed once the axis-7/8/stealth metrics and the results land (see
the handoff's § *Why this stays open past Stage 3*). Snapshot, `gate`, `stats`,
then triage **only** prompts whose `uuid` is not in `dispositions.md`.
