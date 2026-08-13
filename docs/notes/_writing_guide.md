---
status: durable
created: 2026-07-13
updated: 2026-08-13
provenance: distilled from a UWA research-writing seminar (April 2026) supplied by Marc; adapted from paper-writing to dissertation shape; unit ledger added 2026-08-12 from Marc's base-unit framing plus an independent chapter-weighting suggestion he supplied
---

# Writing guide — what each part of the dissertation does

> **Process scaffolding** (underscore-prefixed, exempt from the notes register).
> Broad-brushstroke purpose statements for the dissertation's parts, so notes are
> written *toward* the job their chapter performs. Per-chapter purposes are
> restated in each chapter dir's README; this file holds the whole-document
> guidance and the parts that have no notes dir (title, abstract, introduction,
> conclusion).

## The narrative spine — capture / model / evaluate

The single research question decomposes into three methodological sub-questions (supervisor register §V5, 2026-08-11; the skeleton in [`../thesis/dissertation.tex`](../thesis/dissertation.tex) executes it): **capture** — how APT attacker behaviour is captured from published CTI; **model** — how the captured behaviour is made executable as an attacker traversing that structure in the simulator; **evaluate** — how MTD performance against the APT attack model differs from its performance against the inherited scripted attacker. These are *threads, not chapters*: each runs the length of the document, and the argument-carrying chapters are where the threads surface —

| | Lit review | Methodology | Results | Discussion |
|---|---|---|---|---|
| **Capture** | what exists | how it was done | — | what the capture licenses |
| **Model** | attacker models in MTD | the movement attacker | sensitivity of its parameters | fidelity verdict |
| **Evaluate** | how MTD is evaluated | experimental design | the numbers | what changes for MTD evaluation |

The introduction states the RQ and the three sub-questions (the grey box); the conclusion closes each thread. The capture row's empty results cell is deliberate — the capture produces artefacts, not measurements; its downstream test rides the model row's sensitivity analysis. This matrix is the whole-document coherence check: a proposed unit (see the ledger below) should be able to name its cell, and a unit that cannot is a cut candidate.

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

## The unit ledger — budgeting the 15 000 words

The dissertation is measured in **units of work**: one unit = one subsection = 1–2 concise paragraphs ≈ 250 words. The branching rule cuts both ways — content that needs more than two paragraphs branches into another subsection *and pays for it from the ledger*, or compresses; a subsection that cannot fill one paragraph is not a unit and folds into its neighbour.

Working allocation (word targets exclude tables and figures; appendices are unbudgeted but sanctioned-use only — see below):

| Chapter | Words | Units |
|---|---|---|
| Abstract | 300 | 1 |
| Introduction | 1 500 | 6 |
| Background | 1 250 | 5 |
| Literature review | 3 000 | 12 |
| Methodology | 2 750 | 11 |
| Results | 2 250 | 9 |
| Discussion | 2 250 | 9 |
| Future work | 750 | 3 |
| Conclusion | 500 | 2 |
| **Total** | **≈14 550** | **58, +2 float** |

Reallocation record: 2026-08-12 — methodology 9→11 for the ratified 11-unit methodology skeleton (the capture/model/evaluate workshop), funded by background 6→5 and discussion 10→9.

Three rules keep the ledger honest:

1. **Conservation.** The total is fixed. A unit added to any chapter names the unit it displaces — no silent growth. The two-unit float is spent by naming it, once; it is not borrowed against repeatedly. Reallocations between chapters are Marc's ruling, recorded here.
2. **Skeleton discipline.** The headings in `dissertation.tex` *are* the ledger's units: every subsection heading is a claim on ~250 words, so a session proposing structure proposes its unit count in the same breath, and no heading is added without a budget line. (The failure mode this rule exists against: the 2026-08-11 methodology skeleton carried ~44 subsections — a coverage map of every defensible decision, ~11 000 words if drafted, five times the chapter's budget.)
3. **Cut material has three sinks**, in order of preference: compression to a sentence-level disclosure inside a surviving unit; relocation to the chapter that owns it; the appendix, only for its sanctioned uses (register V6/V7: completed sensitivity sweeps that outgrow the results preamble, the overlay-matrix declaration, the original proposal). The appendix is not a fourth chapter.

Pacing: at ~2 units per day the document is roughly 4–5 weeks of drafting (from 2026-08-12).

## Time allocation and the refine cycle

- Roughly **half the writing time goes to title + abstract + introduction**. They are the shortest parts and the hardest; the reader (and examiner) has largely judged the work by the end of the introduction. The first three parts should carry the full story without the details.
- **Refine–forget–refine.** A first draft is a draft zero. Rereading it ten times in one day finds nothing; refine, *put it away* (a day, then three, then a week as the deadline allows), and refine again — each pass finds a different class of improvement. Never hand a draft zero to the supervisor; the supervisor's pass should lift the draft from your ceiling, not do your early iterations.
- **Selection discipline for the introduction:** what sells the contribution goes in; what doesn't, comes out; no application-example padding when writing for an expert audience.
- **Citation selection for the review:** from each category, the *first* method (sets the direction), the *most established* method (survived the test of time), and the *latest* (the current year where possible — a stale newest-reference dates the whole review).

## How this maps onto the notes system

Notes are staged per chapter (see [`../workflows/docs_map.md`](../workflows/docs_map.md)); each chapter README opens with its purpose. The introduction and conclusion have no notes dirs because both are compressions of material staged elsewhere — the introduction compresses ch2's gap narrowing and ch3–ch5's contributions; the conclusion compresses impact and next steps already carried in notes' *Position* and *Revisit conditions* sections. When drafting begins, this file is the order-of-operations checklist.
