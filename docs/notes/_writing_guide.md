---
status: durable
created: 2026-07-13
updated: 2026-09-22   # the retired name swapped for the APT attacker model at its three mentions (register E2)
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

| | Lit review | Attacker model | Experiments | Discussion |
|---|---|---|---|---|
| **Capture** | what exists | how it was done | — | what the capture licenses |
| **Model** | attacker models in MTD | the APT attacker model | sensitivity of its parameters | fidelity verdict |
| **Evaluate** | how MTD is evaluated | — | experimental design / the numbers | what changes for MTD evaluation |

The introduction states the RQ and the three sub-questions (the grey box); the conclusion closes each thread. The capture row's empty results cell is deliberate — the capture produces artefacts, not measurements; its downstream test rides the model row's sensitivity analysis. This matrix is the whole-document coherence check: a proposed unit (see the ledger below) should be able to name its cell, and a unit that cannot is a cut candidate.

## The one-line job of each part

| Part | What it does |
|---|---|
| **Title** | Highlights the main *technical* contribution (and the application where the application is the novelty). Written **last**. A workshopped candidate shortlist is staged in [`_title_workshop.md`](_title_workshop.md). |
| **Abstract** | States the technical gap and places the contribution against it, for an expert reader, as briefly as possible; ends with the single headline outcome. |
| **Introduction (ch1)** | A compressed literature review that hops landmark-to-landmark straight to the technical gap, then the contributions, then one highlight result. Sells the whole dissertation — a reader should be able to judge the work's value from it alone. States the RQ and the three sub-questions. |
| **Background (ch2)** | The two existing things this thesis builds on, before the literature review: the moving-target-defence vocabulary the document speaks (2.1) and the inherited simulator it runs on (2.2, with the network model, defence mechanisms and baseline attacker nested beneath it). Existing things, not methodology (V-series ruling, 2026-08-11); scope widened 2026-08-21 when the MTD concept material was re-homed from the literature review. Structure, the lineage table's placement, and the two placement tests that keep ch2 and ch3 apart: [`ch2_background/README.md`](ch2_background/README.md). |
| **Literature review (ch3)** | Tells each category of prior work as a chronological story — method, its limitation, why the next method came — and *narrows down onto the gap this work fills*, ending on the demonstrated need. Survey of APT attackers; attacker models in MTD; how MTD is evaluated. |
| **APT attacker model (ch4)** | Defines the attacker model and explains it *as simply as possible*: the chapter preamble states the commitments (it names nothing — the model is the *APT attacker model*, its title; the name *movement attacker* was retired on the supervisor's 2026-09-22 ruling, register E2, and the layer trichotomy with it), then L0–L1 → L2 → L3 → L4. The precise problem statement and the fidelity criterion it is built toward are ch3's (§3.3, the research gap and the criterion) — restructured 2026-09-04, Marc's ruling: the former §4.1 duplicated them. Realisation arguments live here too — the ratified structure has no separate implementation chapter. |
| **Experiments (ch5)** | Experimental setup and results MERGED (Marc's ruling, 2026-09-08): the sensitivity analysis on the three declared inputs of ch4 §4.4 (dwell times, tactic-to-verb mapping, failure matrix), swept within the bounds the formalism sets; the experimental dimensions, with the instrumented metrics named as instrumentation and the comparability boundary as a disclosure; then the strands, one per instrumented metric family (effectiveness, efficiency, the supplementary measures), each running every profile and the baseline. Facts and figures only. No burden / grading / fidelity-defence unit: the model is a hypothesis; the fidelity verdict emerges from the results and is read in the discussion. |
| **Discussion (ch6)** | Interprets outcomes against the field — what the APT attacker model captured, the fidelity verdict, what changes for MTD evaluation — and owns the limitations. |
| **Future work (ch7)** | Names the successor programme this work's own closures point at, with the conditions that would reopen each ruled exclusion. |
| **Conclusion (ch8)** | *Not* the abstract in past tense. Emphasises the impact of the specific technical move, and names the next step in the line of research. |

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
| APT attacker model | 1 500 | 6 |
| Experiments | 3 000 | 12 |
| Discussion | 2 250 | 9 |
| Future work | 750 | 3 |
| Conclusion | 500 | 2 |
| **Total** | **≈14 050** | **56, +4 float** |

Reallocation record: 2026-08-12 — methodology 9→11 for the ratified 11-unit methodology skeleton (the capture/model/evaluate workshop), funded by background 6→5 and discussion 10→9. 2026-08-21 — **no change**, recorded because it looks like one should have happened: ch2's scope widened to carry the MTD vocabulary re-homed from the literature review, and the five units absorbed it internally (the *Prior work* section dissolved into a lineage table, which sits outside the word budget). Both float units remain unspent. 2026-09-04 — **methodology 11 → attacker model 6 + experimental setup 3, float 2 → 4** (Marc's structural ruling): §4.1's two units (problem definition; criterion adoption) are cut as duplicates of ch3 §3.3 and returned to the float; the former §4.2 becomes the chapter (its four subsections are now §4.1–§4.4, plus one unit of in-chapter slack); the former §4.3 is its own three-unit chapter. Words follow units; nothing else moves. 2026-09-08 — **§4.4 claims one unit of overdraft** (Marc's ruling at the §4.4 pass 5): the section holds four subsections (the runtime mechanics; the dwell times; the tactic-to-verb mapping; the failure matrix) on its two units plus the chapter's slack unit; both pass-5 streams measured ≈ 850–900 words as the floor at that shape once the ruled sentences, citations and must-carries stand, and the front-loaded draft lands near 1 000. The unit is claimed against the float (4 → 3) rather than displaced from another chapter; the cut to the ledger, if any, is the assembled-section reconciliation (the 2026-08-18 first-completion ruling). 2026-09-08 — **experimental setup 3 + results 9 → experiments 12** (Marc's structural ruling, same day): the two chapters merge into one, "Experiments" (sensitivity analysis → dimensions → strands by instrumented metric family); the discussion, future work and conclusion renumber to ch6–ch8. Words follow units; the total is unchanged.

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

Notes are staged per chapter (see [`../workflows/docs_map.md`](../workflows/docs_map.md)); each chapter README opens with its purpose. The introduction and conclusion have no notes dirs because both are compressions of material staged elsewhere — the introduction compresses ch3's gap narrowing (and ch2's platform framing) and ch4–ch6's contributions; the conclusion compresses impact and next steps already carried in notes' *Position* and *Revisit conditions* sections and in `ch8_future_work/`. When drafting begins, this file is the order-of-operations checklist.
