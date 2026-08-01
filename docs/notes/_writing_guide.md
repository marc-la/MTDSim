---
status: durable
created: 2026-07-13
updated: 2026-08-01
provenance: distilled from a UWA research-writing seminar (April 2026) supplied by Marc; adapted from paper-writing to dissertation shape
---

# Writing guide — what each part of the dissertation does

> **Process scaffolding** (underscore-prefixed, exempt from the notes register).
> Broad-brushstroke purpose statements for the dissertation's parts, so notes are
> written *toward* the job their chapter performs. Per-chapter purposes are
> restated in each chapter dir's README; this file holds the whole-document
> guidance and the parts that have no notes dir (title, abstract, introduction,
> conclusion).

## The one-line job of each part

| Part | What it does |
|---|---|
| **Title** | Highlights the main *technical* contribution (and the application where the application is the novelty). Written **last**. A workshopped candidate shortlist is staged in [`_title_workshop.md`](_title_workshop.md). |
| **Abstract** | States the technical gap and places the contribution against it, for an expert reader, as briefly as possible; ends with the single headline outcome. |
| **Introduction (ch1)** | A compressed literature review that hops landmark-to-landmark straight to the technical gap, then the contributions, then one highlight result. Sells the whole dissertation — a reader should be able to judge the work's value from it alone. |
| **Background / lit review (ch2)** | Tells each category of prior work as a chronological story — method, its limitation, why the next method came — and *narrows down onto the gap this work fills*, ending on the demonstrated need. |
| **Design / methodology (ch3)** | Defines the technical problem precisely (a precisely-defined problem is more than half solved) and explains the solution *as simply as possible*, with inherited preliminaries separated from own contribution. |
| **Implementation (ch4)** | Carries the realisation detail the method chapter deliberately excludes; implementation challenges are themselves contribution. |
| **Evaluation (ch5)** | Empirical validation on shared benchmarks with shared metrics, comparison against prior methods (adapted nearest-neighbours if the problem is new), plus ablation — which component of the method contributes what. |
| **Discussion (ch6)** | Interprets outcomes against the field — what changes because this exists — and owns the limitations. |
| **Conclusion (ch7)** | *Not* the abstract in past tense. Emphasises the impact of the specific technical move, and names the next step in the line of research. |

## Writing order (when drafting a chapter or the whole document)

Work from the concrete to the framing — the framing is the hardest part and is written against finished material:

1. **Figures, then tables** — no text yet.
2. **Captions, written long** — self-contained, as if there were no body text.
3. **Method text** (you built it; you can write it), then **experiments** (you designed them) — squeezing the captions down as the body absorbs their content (captions stay self-contained, never "Architecture diagram").
4. **Literature review** — the chronological narrowing onto the gap.
5. **Introduction** — the compressed retelling; expect it to be many refinement passes from acceptable.
6. **Abstract**, and only then the **title**.

## Time allocation and the refine cycle

- Roughly **half the writing time goes to title + abstract + introduction**. They are the shortest parts and the hardest; the reader (and examiner) has largely judged the work by the end of the introduction. The first three parts should carry the full story without the details.
- **Refine–forget–refine.** A first draft is a draft zero. Rereading it ten times in one day finds nothing; refine, *put it away* (a day, then three, then a week as the deadline allows), and refine again — each pass finds a different class of improvement. Never hand a draft zero to the supervisor; the supervisor's pass should lift the draft from your ceiling, not do your early iterations.
- **Selection discipline for the introduction:** what sells the contribution goes in; what doesn't, comes out; no application-example padding when writing for an expert audience.
- **Citation selection for the review:** from each category, the *first* method (sets the direction), the *most established* method (survived the test of time), and the *latest* (the current year where possible — a stale newest-reference dates the whole review).

## How this maps onto the notes system

Notes are staged per chapter (see [`../workflows/docs_map.md`](../workflows/docs_map.md)); each chapter README opens with its purpose. The introduction and conclusion have no notes dirs because both are compressions of material staged elsewhere — the introduction compresses ch2's gap narrowing and ch3–ch5's contributions; the conclusion compresses impact and next steps already carried in notes' *Position* and *Revisit conditions* sections. When drafting begins, this file is the order-of-operations checklist.
