---
status: open
created: 2026-08-20
---

# The L2 classification appendix — audit table (Appendix [Y]) + rejected partitions (Appendix [X])

**Goal:** build the two appendix entries §4.2.2 already cites as placeholders:
the per-flow classification audit table (`Appendix~[Y]`, l.444) and the
rejected-partition comparison (`Appendix~[X]`, l.450 — note this is a
**different** `[X]` from §4.2.4.1's; labels assigned by the wiring handoff).

## The audit table (Appendix [Y])

- **Sources:** `data/gasp/classification.csv` + `data/gasp/metadata_audit.csv`
  (the load-bearing classification input), emitted not typed.
- **Columns (Marc's 2026-08-20 dictation, transcript-repaired):** one row per
  attack flow — flow, citation, CTID reference *(dictation had "the CGI" —
  read as the CTID blurb/ID; CONFIRM)*, terminal tactic, assigned objective
  class.
- **PROPOSAL — the override column replaces the confidence grade.** Marc mused
  "do away with the subjectivity"; recommendation: no subjective confidence
  column — carry instead *terminal-tactic read vs assigned class, and which
  cross-check source decided* (CTID blurb / ATT&CK page / vendor report). This
  discharges the recorded consistency obligation in the same stroke: **19 of
  38 land off the terminal read**, and the appendix must state the override
  rule or an examiner sees the inversion undefended. The repo record's own
  inversion history (narrative-primary; structural terminal the rejected P1)
  stays repo-side, unchanged.
- **Caption pins the Attack Flow corpus version** (read the pin from the
  tracked corpus metadata under `data/gap/`; §b5) and the 38-flow census.
- **Freshness check before emitting** (standing concurrent-sessions rule):
  the emitted classes must reproduce the validated post-ruling set —
  19 / 7 / 7 / 5, 38 / 38 high, terminal read 8 / 12 / 1 with 19 on neither
  ([`../implementation/pipeline/gasp/structural_baseline.md`](../implementation/pipeline/gasp/structural_baseline.md)).
  A mismatch is a stop-and-report, not a silent regeneration.

## The rejected partitions (Appendix [X] — §4.2.2's) — SPECIFIED 2026-08-20

Ruled scope (2026-08-17): six alternative schemes, **one row each, why
dismissed — no rubric**. The rubric totals, the per-criterion scores and the
JSD discrimination table stay repo-side in
[`../implementation/pipeline/gasp/partition_decision.md`](../implementation/pipeline/gasp/partition_decision.md).
Genre: approach-comparison table (§e2), prose cells, booktabs, portrait.

### What the reader needs from it

§4.2.2 makes one argument — *not motivation, not attribution, not graph
structure; the analyst's stated objective, in four disjoint classes* — and this
table is the standing answer to the examiner question "why this taxonomy and not
another?". Three things have to be legible from the float alone:

1. **What evidence each scheme would have read.** This is the axis. It is what
   turns a list of discarded ideas into the argument the chapter makes, and it
   is the column that has to scan.
2. **What each scheme would actually have produced on this corpus.** The
   defence is empirical, not aesthetic: each scheme was computed, and the
   numbers are what dismissed it. A reason without a number reads as taste.
3. **Which dismissals are about this corpus and which are about the scheme.**
   Two schemes cannot be built here at all (the metadata does not exist); three
   can be built and are wrong; one is a near-miss on shape alone. That
   distinction is what the sensitivity hook hangs off.

### The axes (five columns)

| Column | Content | Width |
|---|---|--:|
| **Scheme** | descriptive name, no `P`-numbers (`gasp_schema.md` §(b) deprecates the P-framing for spec text; the ledger keeps them repo-side) | 0.17 |
| **Slices on** | the evidence read: *Inferred motivation* / *Actor attribution* / *Graph: terminal tactic* / *Graph: objective reach* / *Graph: terminal technique* / *Stated objective*. Citations inline as `\citep`, no separate Ref(s). column — six columns does not fit portrait | 0.15 |
| **On this corpus** | what it yields: class count, split, and the disagreement against the attested objective. Every number generated | 0.24 |
| **Why dismissed** | the verdict clause, prose | 0.34 |
| **Buildable** | `\checkmark` where the scheme's membership can be derived from artefacts the pipeline already holds; **empty cell** where it cannot (§e1: never `✗`) | 0.06 |

**Row order runs the chapter's argument**, furthest evidence first, near-miss
last, adopted row after a `\midrule`:

| # | Scheme (row label) | Slices on | On this corpus (live, recomputed 2026-08-20) | Dismissal, in one clause | Build |
|--:|---|---|---|---|:--:|
| 1 | Motivation categories, reduced to three | Inferred motivation (STIX `attack-motivation-ov`) | ten categories; a 47-campaign hand-label sample used three of them; **0 of 38** flows carry an ATT&CK Campaign identifier to join the labels to | slices on inference rather than observation, and the labels do not join to this corpus at all | |
| 2 | Group-witnessed objective | Actor attribution (ATT&CK Groups) | **18 of 38** flows carry a Group identifier; none carries a Campaign identifier; **20** are unattributed | half the corpus would be unclassifiable, and the classes would name actors, not objectives | |
| 3 | Terminal tactic in the dependency graph | Graph: terminal tactic (Def A) | **7 / 11 / 1 / 19** (exfil / impact / both / neither); disagrees with the attested objective on **19 of 38** | the disagreement is systematic, not noise: 14 of the 19 are reports that stop before the objective, so the graph is silent where the analyst attests one | ✓ |
| 4 | Objective tactic reached anywhere | Graph: objective reach | **10 / 10 / 3 / 15**; disagrees on **14 of 38** | more forgiving than the terminal read and still structural: 15 flows remain unclassifiable, and a tactic occurring anywhere is weaker evidence than the analyst's statement | ✓ |
| 5 | Terminal technique | Graph: terminal technique | **36** distinct terminal-technique sets over 38 flows, **34** of them unique to one flow; **2** flows are cyclic with no terminal at all | fragments to roughly one class per incident; a class of one is a single account, not a behavioural envelope | |
| 6 | Stated objective, three classes with multi-membership | Stated objective | **26 / 14 / 5** memberships over 38 flows; the **7** double-objective flows sit in two classes at once | the profiles stop being alternatives — a flow in two of them is counted twice in the comparison — and the compound objective the corpus repeatedly documents gets no name | ✓ |
| — | **Stated objective, four disjoint classes (adopted)** | Stated objective | **19 / 7 / 7 / 5**; every flow in exactly one class | — (cell states what the others cost: disjoint, attested, and the compound objective named) | — |

**The adopted scheme is a row.** Recommended, and a genuine choice: an
approach-comparison table whose winner is absent makes every "on this corpus"
cell a comparison against something the reader has to hold in memory from four
pages earlier. Marked by a `\midrule` and decoded in the caption. *Marc's
ruling owed — the section title says "considered and dismissed", so if the row
stays the title should read "Partition schemes considered".*

### The sensitivity hook (Marc's 2026-08-20 dictation)

The `Buildable` column is the flag. Framing matters and this is the ruling to
take: it marks **what can be constructed from artefacts already held**, which is
a fact about the data today, **not** a commitment that the sweep will run. A
column that promises a sweep is a cheque the appendix writes and ch5 has to
cash.

Three rows tick: the two structural schemes (rows 3, 4 — both already computed
by `tools/gasp_structural_baseline.py`, membership is a vector swap over the
same disjoint machinery) and the multi-member scheme (row 6 — membership is a
collapse of the audit CSV). **The cost is not equal and the table should not
imply it is:** rows 3 and 4 are cheap sensitivity variants; row 6 breaks the
disjointness the L3 envelope assumes, so running it is a code change, not a
config flag. That distinction stays here, not on the page.

If V6 takes this up, the ch5 parameter table gains one row — *objective
partition scheme*, swept over {adopted, terminal-tactic, reach} — and this
appendix's caption is what earns the pointer. **Not commissioned by this brief;
Marc's call, and it is a real run cost.**

### Execution

**Tracked ledger, not a typed table.** New `data/gasp/partition_candidates.csv`,
one row per scheme (seven, including the adopted): `scheme_id` (`p1`–`p7`, repo
provenance, never printed), `order`, `status` (`dismissed` | `adopted`), `name`,
`slices_on`, `outcome_template`, `dismissal`, `buildable`, `provenance`. The
prose lives in the ledger so it is edited in one place; every **number** in
`outcome_template` is a named placeholder the generator substitutes from the
artefacts.

**Generator:** `tools/gasp_partition_candidates.py`, emitting
`docs/thesis/tables/rejected_partitions.tex`. It **imports** Def A, the reach
read and the two concordance rules from `tools/gasp_structural_baseline.py`
rather than re-implementing them — that tool already emits the sibling audit
table, and the 19-of-38 count appears in both floats *and* in the chapter's own
sentence at l.482. One home for the definition, or they drift.

**Freshness gate (stop-and-report, not silent regeneration):** refuse to emit
unless the audit CSV reads 38 rows, 19 / 7 / 7 / 5, 38 / 38 high confidence, and
the dismissed-row count is exactly **six** — §4.2.2 l.488 says "Six other
partitions", so the word and the table are coupled.

**Fact sheet on stdout**, as the other generators do: every substituted number,
the corpus pins, the column-width sum, and an explicit **TYPED** marker on the
one figure that cannot be computed (the 47-campaign hand-label sample has no
tracked artefact — same flagged deviation as `tab:experiment-one`).

**Caption** — `\caption[short]{long}` per §c; short form *"Partition schemes
considered and dismissed"*. The long form carries, per Marc's "push all the
information into the caption": what a row is; that *Slices on* names the
evidence the scheme would have read; the Def A terminal definition in one clause
(rows 3 and 4 depend on it); the `\checkmark`/empty-cell decode; that the final
row is the adopted scheme; and the pins — Attack Flow corpus v3.1.1, ATT&CK
Enterprise v19.1, 38 usable flows (read from the tracked corpus metadata under
`data/gap/`, as `gap_appendix_figures.py` does; §b5). **No mention of the
rubric** — naming an instrument the table does not reproduce invites "show me",
and the 2026-08-17 ruling took it off the face. SESSION-DRAFTED, flagged for
Marc's voice pass.

**Preamble:** `\checkmark` needs `amssymb`, which is not loaded. One line in a
file concurrent sessions read — add it in the same commit as the `\input`, or
fall back to `$\bullet$` and change nothing.

**Wiring:** `\input{tables/rejected_partitions}` under
`\label{app:rejected-partitions}` plus the `% [prose slot --- Marc]` comment for
the framing sentence or two (appendix-prose rule).

### Freshness findings — the record cannot be transcribed as written

Recomputed 2026-08-20 from `data/gasp/metadata_audit.csv`. The live numbers
above reproduce the pinned baseline exactly (7 / 11 / 1 / 19 terminal,
10 / 10 / 3 / 15 reach, 19 / 7 / 7 / 5 adopted). Four things in
`partition_decision.md` do **not** survive:

- **P2's cardinality.** The record says "15-class"; `gasp_schema.md` §(b) says
  the v0.4 scheme was "30-bucket". Neither reproduces: under the pinned Def A
  there are **36** distinct terminal-technique sets over 38 flows (34
  singletons, two pairs), 88 distinct terminal techniques, and 2 flows with no
  terminal technique at all. Use the recomputed figure; both recorded numbers
  are pre-Def-A.
- **The double-extortion count.** The record says six throughout; the
  2026-08-17 rulings moved the split to 19 / 7 / 7 / 5, so it is **seven**, and
  the P5 multi-membership arithmetic (26 / 14 / 5 over 45 memberships) has to be
  re-derived, not copied.
- **Confidence.** The record's "6 of 38 low" is stale — the CSV is **38 / 38
  high**.
- **The JSD table is internally inconsistent** (P6's technique JSD is given as
  0.317 in the table's note and 0.302 in the reading paragraph) and is
  pre-ruling. A further reason discrimination numbers stay off this float:
  putting them on the page would mean materialising all five schemes to
  recompute, which is not a table job.

## Considerations

1. **Connective prose is Marc's.** Each appendix entry needs a sentence or two
   framing the table; sessions emit the floats and flag the prose slots.
2. 38 rows × a citation column is wide — expect landscape or a two-part
   layout; citations as `\citep` keys resolving in the bibliography, not URLs.
3. The per-profile subgraph renders (Marc's 2026-08-20 "maybe") would live in
   this appendix neighbourhood **if** ruled in — gated on his ruling and on a
   prose citation existing; not part of this brief's gate.

## Validation gate

Both tables emitted from tracked artefacts under real labels; §4.2.2's two
placeholders resolve; corpus pin in both captions; freshness check recorded.

Three proposals need Marc's ruling before the floats are final:

1. the audit table's **override column** replacing the confidence grade
   (accept / amend);
2. whether the **adopted scheme appears as a row** in the rejected-partitions
   table — and, if it does, the section title loses "and dismissed";
3. the **`Buildable` column's framing** — recommended as *what can be
   constructed today*, not *what will be swept*; ticking it as a sweep
   commitment obliges ch5 to run the variants.

## Reading list

1. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md)
2. `data/gasp/classification.csv`, `data/gasp/metadata_audit.csv`
3. [`../implementation/pipeline/gasp/structural_baseline.md`](../implementation/pipeline/gasp/structural_baseline.md) — the validated numbers
4. [`../implementation/pipeline/gasp/gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md) §(a), §(c)
5. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §b4, §b5, §e2
