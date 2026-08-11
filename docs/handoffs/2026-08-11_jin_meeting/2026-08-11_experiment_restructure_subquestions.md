---
status: open
created: 2026-08-11
---

# Execute V5–V7 — restructure the experimental setup and chapter skeleton onto the sub-question spine

## State of play

The morning of the 11-Aug meeting, `c909421` landed the evaluation's grading
instrument ([`../../notes/ch5_evaluation/evaluation_grading.md`](../../notes/ch5_evaluation/evaluation_grading.md))
and a two-dimension `sec:experimental-setup` scaffold in
[`../../thesis/dissertation.tex`](../../thesis/dissertation.tex). The meeting then
replaced the organising frame
([`../../implementation/pipeline/ogasp/supervisor_decision_register.md`](../../implementation/pipeline/ogasp/supervisor_decision_register.md)
§V5–V7): the research question is reworded APT-explicit — **"How does MTD
perform against APT attackers?"** — stated in the *introduction* (with a
compact methodology and key highlights), and decomposed into three
sub-questions that become the methodology's spine: **capture** (data
collection, corpus → profiles), **implementation** (Petri-net mapping,
weights, state semantics, configuration justifications), **evaluation**
(benchmark = the inherited baseline attacker; standard metrics plus the
APT-specific supplementary ones). The experiment dimensions become means
*inside* the sub-question they answer — not the top-level structure, and not
all of them need appear. V6 adds the sensitivity-analysis regime (results
preamble: a table of arbitrarily-set parameters, ranges swept, effects; most
impactful first — timing and durations named; the ~200-value overlay matrix
to an appendix). V7 moves the inherited-simulator description (the revised
boilerplate's §3.2: network / defence / procedural attacker) out of the
methodology into a **Background** chapter after the introduction.

What survives untouched: the grading instrument's answer vocabulary
(magnitude / ordering / recommendation) was not challenged — it becomes
sub-question 3's scoring, not a casualty. The two dimensions (prior-model
comparison; fresh evaluation) survive as the internal split of sub-question 3.
The learning-vs-scale hypothesis
([`2026-08-11_learning_scale_dependence.md`](../2026-08-11_learning_scale_dependence.md))
becomes a candidate dimension within sub-question 3, not a parallel structure.

## Recommended approach

1. **`dissertation.tex` skeleton**: introduction gains the RQ, the three
   sub-questions, and the compact-methodology slot; a Background chapter is
   added (network model / defence model / procedural attacker) between the
   introduction and the literature review; the methodology reorders per the
   revised boilerplate minus its §3.2; `sec:experimental-setup` reorganises
   by sub-question with the factor table embedded under sub-question 3 and a
   sensitivity-analysis preamble slot per V6.
2. **`evaluation_grading.md`**: re-aim the note at sub-question 3 and
   re-clear it against the notes rubric.
3. **Annotate register §V5–V7 executed** in the same commit.

Alternative considered: keeping the two-dimension frame and mapping
sub-questions onto it in prose. Rejected — the ruling is explicitly that the
sub-questions organise and the dimensions serve, and a frame that says
otherwise will be re-derived wrongly by every future session.

## Validation gate

`latexmk -pdf dissertation.tex` compiles; the skeleton shows the
introduction-RQ block, the Background chapter, and the sub-question-organised
setup; the grading note re-clears the rubric checklist; register §V5–V7
annotated. Marc can draft the methodology into the new skeleton without
moving structure.

## Hard constraints

- [`../../workflows/voice.md`](../../workflows/voice.md) is the **hard gate** for
  any `thesis/` prose and the default for `notes/`; load it before writing
  either. Load [`../../workflows/notes_rubric.md`](../../workflows/notes_rubric.md)
  in full before editing the note.
- Thesis heading conventions: sentence case, no acronyms in headings; keep
  the L0–L4 prefixes, "movement attacker" and "APT" visible in the text.
- The single-RQ decision (architecture §(a)) is intact — the sub-questions
  are methodological decomposition, per the register's §V5 consistency note.
  Do not introduce sub-problem framing.
- Structure only: no experiments run, no results prose.
- Branch / commit / never-push rules per
  [`../../workflows/session_workflow.md`](../../workflows/session_workflow.md).

## Reading list

- [`../../implementation/pipeline/ogasp/supervisor_decision_register.md`](../../implementation/pipeline/ogasp/supervisor_decision_register.md) — §V5–V7 (the operative rulings)
- [`../../notes/ch5_evaluation/evaluation_grading.md`](../../notes/ch5_evaluation/evaluation_grading.md) — the note being re-aimed
- [`../../thesis/dissertation.tex`](../../thesis/dissertation.tex) — `sec:experimental-setup` as landed at `c909421`
- [`../../workflows/voice.md`](../../workflows/voice.md) + [`../../workflows/notes_rubric.md`](../../workflows/notes_rubric.md) — the gates
- [`../../notes/_writing_guide.md`](../../notes/_writing_guide.md) — chapter-job map for the Background/introduction moves

## Out of scope (explicitly)

Drafting methodology or background *prose* (Marc drafts this week — the
deliverable is the structure he drafts into); running any experiment cell;
the sensitivity sweeps themselves (V6 says run as time permits — they get
their own brief when commissioned).
