---
status: open
created: 2026-08-20
updated: 2026-08-20
---

> **SHIPPED 2026-08-20 (this session).** The entry is drafted, generated, wired
> and building: `tab:preliminary-extraction` in Appendix~D, from
> `tools/preliminary_extraction_table.py`. **What remains is Marc's:** the
> framing paragraph (specified in the `app:cooccurrence` comment block, not
> drafted anywhere), the caption's voice pass, and the four open calls in §(f).
> The sections below are the reasoning behind what shipped; read §(g) first for
> what is actually on the page.

# The preliminary-extraction appendix entry — `app:cooccurrence`

**Goal:** fill the existing `app:cooccurrence` appendix chapter with the
evidence behind the two abandonment claims §4.2.1 already cites — the
co-occurrence mining runs and the keyword/ontology-regex tests.
**(Ruled 2026-08-20: keep — the entry is load-bearing; the abandonment claim
cites `\ref{app:cooccurrence}`.)**

**Status change (2026-08-20, this session): the recovery step is DONE and the
re-run contingency is void.** Every number the entry needs exists in tracked
history. Step 2 of the old approach ("if the numbers cannot be recovered,
re-run minimally") is struck. What remains is a table design, a generator, and
Marc's framing prose.

---

## (a) Recovered evidence — provenance

### Which artefact can carry this entry — settled, and it is not v0.5

Checked on Marc's steer to use the latest archive artefact (2026-08-20):

- `archive/replay-viz` and `archive/attacker-profiling` carry the **identical**
  `data/gap/gap_v0.4_latest.json` (same md5). There is no newer GAP on either
  branch; v0.4 is the highest either holds.
- **`data/gap/gap_v0.5.json` on `dev` is the shipped L1 and contains no
  evidence-type field at all** — 124 nodes, 478 edges, 38 flows,
  `attack-flow@v3.1.1`, ATT&CK Enterprise 19.1, built 2026-05-28.

That absence is structural, not an oversight: **v0.5 is the artefact that
resulted from the abandonment.** Decision 1 removed both routes, so v0.5 has one
source and nothing to distinguish. The two dead routes exist in exactly one
built artefact — v0.4 — and always will. So the entry reads v0.4 for the
abandoned routes and v0.5 for the comparator, and says so.

Two artefacts on `archive/attacker-profiling` (pinned at
`b8060c630ad6ac60520dc6be9cac1c8ea7321b70`):

1. **`data/gap/gap_v0.4_latest.json`** — the built v0.4 GAP, `build_date`
   2026-04-19. Carries every edge with its `evidence[].source_type`, so the
   per-route yields and the cross-route corroboration are computable from the
   artefact itself.
2. **`notebooks/2026-04-08_MTDSim_AttackGraphBuild.ipynb`** — the build
   notebook **with its cell outputs stored**. This is the run log: usage-matrix
   shape, rule counts, the median cut, the intra-tactic drop, the top-10 rules
   with support/confidence/lift, and sample ontology extractions.

Source code for both routes, same branch:
`src/mtdsim/attacker/gap/cooccurrence_miner.py` (FP-Growth) and
`extract_ontology_edges` in `src/mtdsim/attacker/gap/edge_importer.py` (regex).

The abandonment itself is already a shipped ruling —
[`../implementation/pipeline/gap/gap_schema.md`](../implementation/pipeline/gap/gap_schema.md)
**Decision 1** ("the canonical GAP is Attack-Flow-only") — so the appendix
reports evidence for a decision the implementation record already owns; it does
not make the decision.

---

## (b) The numbers, pinned

**Co-occurrence mining (FP-Growth over the ATT&CK group + software `uses`
matrix, after Rahman et al. 2022):**

| Quantity | Value | Source |
|---|---|---|
| Usage matrix | 952 entities × 216 parent techniques | notebook cell 7 |
| Corpus behind it | 172 intrusion sets, 784 software, 17 270 `uses` relationships | cell 4 |
| Parameters | `min_support` 0.10, `min_confidence` 0.60 | `cooccurrence_miner.py` defaults, artefact fields |
| Simple (1→1) rules generated | 115 | cell 8 |
| Median-confidence cut | **0.690** | cell 8 / artefact `confidence_threshold` |
| Rules surviving the cut | 58 | cell 8 |
| Directed edges produced | **42** | cell 8, artefact |
| Rules dropped as intra-tactic (undirectable) | **15** | cell 8, artefact `intra_tactic_unresolved` |
| Lift: median / range | **1.37** / 1.17–4.34 | artefact |
| Edges at lift < 1.5 | **33 of 42** | artefact |
| Edges sourced at T1059 alone | **24 of 42 (57 %)** | artefact |
| Backward edges produced | **0 of 42** | artefact |
| Corroborated by an analyst-drawn edge | **16 of 42 (38 %)** | artefact |

**Keyword / ontology-regex extraction (DeepOP-style, over ATT&CK technique
descriptions):**

| Quantity | Value | Source |
|---|---|---|
| Input | 216 technique descriptions | cell 4 |
| Method | 10 precondition phrases (`requires`, `after`, `following`, `depends on`, `once`, `leveraging`, …) × `\bT\d{4}\b` | `edge_importer.py` |
| Confidence threshold | **none — every edge stamped `confidence = 0.8` as a constant** | `edge_importer.py` l.211 |
| Edges extracted | **60** | cell 11 |
| Edges surviving into the built artefact | 53 | artefact |
| Running against tactic order (`is_backward`) | **27 of 53 (51 %)** | artefact |
| Corroborated by an analyst-drawn edge | **3 of 53 (5.7 %)** | artefact |

### The tactic-level collapse — the finding that carries the entry

**Ruled by Marc (2026-08-20): the coverage claim is *relative to Attack Flow*.**
Collapsing each route's technique edges onto their techniques' primary tactics —
the resolution the dissertation actually ships at — gives the comparison in the
terms the claim is made in. Of the **210** possible ordered cross-tactic
transitions (15 tactics), the same v0.4 build recovers:

| Route | Technique edges | Cross-tactic transitions recovered | Share of 210 |
|---|---|---|---|
| Co-occurrence mining | 42 | **19** | 9 % |
| Keyword extraction | 53 | **25** | 12 % |
| Attack Flow (same v0.4 build) | 307 | **91** | 43 % |
| **Attack Flow, shipped L1 (v0.5)** | 478 | **122** | **58 %** |

Two things fall out, and both are threshold-independent — they survive whatever
the exploratory thresholds were, which is exactly what makes them safe to print:

1. **"Low coverage relative to Attack Flow" is vindicated, with a number.**
   Co-occurrence recovers under a quarter of the tactic structure the analyst
   corpus gives, off a vastly larger input (952 entities against 38 flows).
2. **Marc's memory of the keyword run reconciles with the code.** He recalls
   running it over the MITRE descriptions and finding "very very few connections
   between the tactics themselves". The artefact agrees: 60 technique edges
   collapse to just **25** cross-tactic transitions, 12 % of the space. The
   technique-level count (60) and the tactic-level memory (very few) are the
   same run seen at two resolutions.

**Wording note:** the committed extractor parses technique descriptions from the
STIX bundle; Marc recalls running it against the ATT&CK website. Same text, two
fetches — "ATT&CK technique descriptions" covers both and no discrepancy needs
airing.

**The Attack Flow route, same build (the comparator):** 436 edges imported
pre-merge; 307 present in the built artefact. The shipped L1 is a different
build — 124 techniques, 478 edges, 38 flows, Attack Flow corpus v3.1.1,
ATT&CK Enterprise v19.1.

**Merged v0.4 artefact:** 383 edges over 216 techniques, of which **94 (25 %)
carried a machine-inferred signal** and **76 (20 %) rested on an inferred
signal alone**, with no analyst-drawn edge behind them. Only **18 edges (4.7 %)
carried two or more independent evidence types.**

### The 80 % CONFIRM — searched exhaustively, not found in committed history

**Marc's ruling context (2026-08-20): the April material is stale, and the
thresholds were moved around a lot during exploration.** What committed history
shows, searched end to end:

- the design schema at **v0.1, v0.2 and v0.3** (`notebooks/2026-04-08_MTDSim_AttackGraphDesignSchema.md`,
  four commits) specifies `min_support` 0.1, `min_confidence` 0.6, and a
  median-confidence filter — no 80 % anywhere;
- `cooccurrence_miner.py` was committed **once** (94c4abb) and never amended;
- **all nine** versions of the build notebook pass `min_support=0.1,
  min_confidence=0.6`;
- the only 0.8 in the codebase is the constant the *keyword* extractor stamps on
  every edge it emits (`edge_importer.py` l.211), and the only "80 %" in the
  schema docs is a v0.2 remark that the top 50 techniques by campaign count
  likely cover >80 % of observed behaviour — a coverage estimate, not a filter.

**Disposition: the 80 % co-occurrence threshold Marc remembers is real but was
run in uncommitted working state; it cannot be sourced.** Per the annal's rule,
this is flagged, not argued down. **Consequence for the entry: cite no
threshold.** The abandonment does not rest on one, the thresholds moved, and a
number that cannot be traced must not reach the page. Both dissertation
comments (l.359, l.1652) should have the "80 % — CONFIRM" struck rather than
resolved.

### Two counting subtleties the entry must not blur

1. **Yields are pre-merge; corroboration is post-merge.** The built artefact
   ran `_break_cycles` after merging, which destroyed edges across all three
   signals (Attack Flow 436 → 307 is mostly this). So the yield row reports the
   route's own output (42 / 60 / 436) and the corroboration row reports the
   built artefact (16 of 42, 3 of 53). The caption states which is which.
2. **The v0.4 Attack Flow column is not the shipped L1.** Its importer used the
   `_parse_afb` pixel-proximity latch hack that v0.5 replaced. It is a
   same-build comparator, not the artefact the dissertation ships — footnote it.

---

## (c) What §4.2.1's prose currently claims, and the gap

Live prose (l.380-392): *"Co-occurrence mining gave low coverage and keyword
mining poor fidelity"*, then NLP ruled out as a class
`\citep{rahman2025, buchel2025}`, then *"a human analyst drew every dependency"*.

**Marc's rulings, 2026-08-20, which govern what follows:** the coverage claim is
relative to Attack Flow; **NLP was never run** — it was ruled out systematically
from the literature, and the prose is already correct on that; the keyword run
was over the MITRE descriptions and found very few tactic connections.

Content points for Marc. **The prose is Marc's; nothing here is drafted for
insertion.**

1. **The existing verdict stands and now has evidence.** "Low coverage" is
   correct once read as relative to Attack Flow, which is how Marc means it: 19
   cross-tactic transitions against Attack Flow's 91 in the same build, off 952
   entities against 38 flows. No verdict change needed — the appendix supplies
   the scale the sentence currently asserts. *(An earlier session position that
   "low coverage" was the wrong verdict was argued at technique resolution and
   is withdrawn; at tactic resolution — the shipped resolution — coverage is
   exactly the story.)*
2. **The one genuinely new argument: imposed direction makes cycles impossible
   by construction.** Co-occurrence yields symmetric association, so v0.4 had to
   impose direction from canonical tactic ordering — and because that ordering
   forbids backward edges, **none of the 42 mined edges could be a loop**, while
   15 rules whose endpoints shared a tactic could not be directed at all and
   were discarded. The shipped L1 preserves cycles deliberately (real attackers
   loop: move laterally, discover, move again), and the L3 unit now owns
   introducing loop preservation (l.360 item (d)). So the method is not merely
   lower-coverage than Attack Flow — it is structurally incapable of
   representing the behaviour the movement attacker runs on. This is unstated
   anywhere in the chapter and is threshold-independent. **Recommended as the
   one sentence worth adding**, if the ledger can carry it.
3. **Keep the NLP boundary visible.** The paragraph runs the two attempted runs
   straight into the class-level NLP ruling-out, so `\citep{rahman2025,
   buchel2025}` can read as covering our own runs. It must stay legible that two
   things were *built and run* and one class was *ruled out on the literature*,
   never tried. This also constrains the appendix: it reports two routes and
   must not imply NLP or process mining was tested. (Process-mining ingestion
   was likewise considered and dropped, 23-Jun, in
   [`../implementation/research_record/threads/objective_pivot.md`](../implementation/research_record/threads/objective_pivot.md).)

**Budget reality.** The unit is already at ~1.6 ledger units (l.356-358). The
recommendation is therefore **at most one added sentence** — item 2 — paid for
by a named overdraft or a cut at the ledger pass. Item 1 costs nothing.

## (d) Proposed shape of the appendix entry

**What the reader needs.** A reader arrives from §4.2.1 with exactly one
question: *were these approaches given a fair run, and is the abandonment
evidenced or asserted?* The entry must show, per route: what was run (so it
reads as a fair trial, not a strawman), what came out, and the structural
reason the output was unusable. Nothing else. Not a survey of extraction
methods; not a re-litigation of Decision 1 (`gap_schema.md` owns that).

**One table, not two.** The two runs share reporting axes, so two floats would
duplicate headers over four rows each; and the argument is *comparative* — it
lands when 38 % and 5.7 % are read side by side. Genre: the
approach-comparison table (`figure_table_conventions.md` §e2, cho2020
TABLES IV/VI), **transposed** — approaches as columns, axes as rows, because
the axes are heterogeneous (counts, fractions, prose) and there are only three
columns. The third column, Attack Flow at the same build, is what makes the
table argue rather than report: without it "42 edges" has no scale.

**Proposed axes — split into two registers, on Marc's abstraction steer
(2026-08-20).** The entry's argument is carried by rows that **cannot move with
any parameter**; the measured row is one dated illustration, stamped as such.
Everything threshold-sensitive is cut.

*Stable rows — definitional, parameter-free, the load-bearing three:*

| Row | Co-occurrence mining | Keyword extraction | Attack Flow (adopted) |
|---|---|---|---|
| What an edge rests on | two techniques used by the same actor or tool | precondition wording in a technique's description | a dependency an analyst drew in one incident |
| Where direction comes from | not in the evidence — imposed from tactic ordering | not in the evidence — inferred from tactic ordering | drawn by the analyst |
| Can a loop be represented? | no — a total order admits no backward edge | no | yes, and the shipped graph preserves them |

*Dated row — one measured comparison, version-stamped in the caption:*

| Row | Co-occurrence | Keyword | Attack Flow |
|---|---|---|---|
| Tactic transitions recovered, of 210 | 19 (9 %) | 25 (12 %) | 122 (58 %) in the shipped L1; 91 (43 %) in the same v0.4 build |

**Cut entirely, as threshold-sensitive:** technique edge counts (42 / 60 / 436),
support and confidence parameters, the median cut, lift, and the corroboration
counts. All of these move with settings that moved during exploration, and none
is needed — the stable rows carry the argument and the coverage row carries the
scale. This is the direct answer to the staleness objection: **an appendix built
on definitional facts cannot be falsified by a threshold nobody can source.**

The prose cells in the stable rows are the load-bearing ones; keep them short
enough that the widest cell does not set an illegible width
(§h's cap-the-column rule).

**What goes in the caption, not the body** (§b2 decode, §b5 version stamp):

- the build stamp — v0.4 GAP, built 2026-04-19, ATT&CK Enterprise as parsed
  then (216 parent techniques);
- the decode of "agreement with a drawn edge" — the same directed pair also
  drawn by an analyst in the same build;
- the pre-merge / post-merge split from §(b) above;
- the footnote that this v0.4 Attack Flow column used a superseded importer and
  is a same-build comparator, not the shipped L1 (124 techniques, 478 edges,
  corpus v3.1.1, ATT&CK v19.1);
- that both abandoned routes were **built, merged and used** before being
  removed wholesale by Decision 1 — this is what makes the entry evidence
  rather than a thought experiment, and it belongs in the caption because it is
  the reader's fairness check.

**One worked failure per route, in the flagged paragraph — not the caption
and not a second float.** Captions decode; they do not narrate. Both are
concrete images of the kind Tim French's feedback rewards:

- *Keyword:* T1110 (Brute Force)'s ATT&CK description contains "adversaries may
  attempt to brute force access to [Valid Accounts]" — a cross-reference, which
  the extractor read as a precondition and emitted as four separate edges
  (T1078, T1003, T1087, T1201 → T1110) off one sentence, with the direction
  inverted.
- *Co-occurrence:* T1059 sources 24 of the 42 mined edges at lift 1.37–1.41 —
  the rules record that T1059 is common, not that anything depends on it.

**Structure: one table + one flagged paragraph.** This is also what makes the
entry migration-safe. If it later moves into Results (Marc's flag), what moves
is the float and the chapter collapses to nothing.

---

## (e) Mechanism — how the numbers reach the page

No re-run. The provenance chain, respecting the no-value-typed rule:

```
archive/attacker-profiling@b8060c6:data/gap/gap_v0.4_latest.json
  + the build notebook's stored cell outputs
      → tools/preliminary_extraction_evidence.py   (one-shot, committed)
      → data/gap/archive/v0.4_extraction_run.json  (small, tracked, marked superseded)
      → tools/preliminary_extraction_table.py
      → docs/thesis/tables/preliminary_extraction.tex
```

Recommended over committing the whole 1.1 MB superseded artefact onto `dev`;
the extraction script pins the source SHA in its header so the chain is
auditable either way. **Flag:** if Marc would rather have the full artefact on
the branch for auditability, that is the alternative — say so and it changes.

---

## (f) Open questions for Marc

1. **Rename the label?** `app:cooccurrence` is named after one of two routes,
   which is already wrong for a two-route entry and worse if it migrates to
   Results. The chapter title already reads "Preliminary corpus extraction
   runs". Recommend `app:preliminary-extraction` / `tab:preliminary-extraction`
   — a one-line change in two places now, annoying later.
2. ~~**Does process mining get a column, a row, or nothing?**~~ **Settled
   (Marc, 2026-08-20):** neither process mining nor NLP was ever run — both were
   ruled out systematically. The table carries **two attempted routes plus the
   Attack Flow comparator, and nothing else**; the appendix must not imply
   anything untried was tested.
3. **Chapter or section?** A single-table chapter is thin; it could fold as a
   section into `app:supplementary`. The 2026-08-20 wiring comment (l.1174)
   ruled it stays its own chapter — recommend holding that unless the Results
   migration happens.
4. **The prose supplement's budget** — §(c) items 1 and 2 are a verdict change
   plus one sentence into a unit already at ~1.6 units. Overdraft or cut?

---

## Validation gate

Table generated (not hand-typed) from a tracked evidence file; every number
traceable to the pinned v0.4 artefact or the build notebook's stored outputs;
the 80 % CONFIRM corrected in **both** dissertation comments; the §4.2.1
citation reads correctly against the finished entry; caption carries the build
stamp, the corroboration decode and the pre/post-merge split; `\caption[short]`
present; pdflatex clean.

## Reading list

1. `docs/thesis/dissertation.tex` §4.2.1 (l.377–392) + the `app:cooccurrence` stub (l.1650–1658)
2. [`../implementation/pipeline/gap/gap_schema.md`](../implementation/pipeline/gap/gap_schema.md) — Decision 1, the shipped ruling this entry evidences
3. [`../implementation/research_record/threads/objective_pivot.md`](../implementation/research_record/threads/objective_pivot.md) — the process-mining/ontology-regex drop
4. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §b, §e2, §h
5. [`../notes/_writing_guide.md`](../notes/_writing_guide.md) — the ledger, and the "appendix is not a fourth chapter" rule


---

## (g) What shipped, and what is still owed

**Shipped.**

- `tools/preliminary_extraction_table.py` — computes every number from the
  artefacts (the v0.4 GAP read out of `archive/attacker-profiling` by sha; the
  shipped `data/gap/gap_v0.5.json`), takes every word from
  `data/gap/archive/preliminary_extraction_labels.json`, and emits both a
  record file and the float. No value and no corpus fact is typed into the tool.
  `--check` recomputes and prints without writing.
- `data/gap/archive/preliminary_extraction_labels.json` — the editorial text and
  the presentation pins. This is the file a voice pass edits.
- `data/gap/archive/v0_4_extraction_run.json` — the emitted record: counts, the
  pinned v0.4 commit, both builds' provenance.
- `docs/thesis/tables/preliminary_extraction.tex` — `tab:preliminary-extraction`.
- `dissertation.tex` — the appendix chapter carries the float and a comment block
  specifying the paragraph Marc owes; the two stale `CONFIRM` comments in
  §4.2.1 are replaced with what the record actually licenses.

**The table as built.** Rows are the three modes; columns are *a dependency
rests on* / *direction from* / *tactic transitions* / *why it was not used*. Of
the 182 transitions 14 tactics admit: co-occurrence 19 (10 %), keyword 25
(14 %), Attack Flow 91 (50 %) on the same build, and 113 (62 %) in the shipped
graph, quoted in the caption.

**One thing found while building that the design did not anticipate.** The two
artefacts resolve on **different tactic axes** — v0.4 on stock ATT&CK's 14, the
shipped v0.5 on this project's 15, which splits defence evasion into stealth and
defence impairment. Quoting both against one denominator would have been
apples-to-oranges. The generator folds the split back and *asserts* the axes then
match, failing loudly if a later artefact breaks it; the caption names the fold.
This is why the denominator is 182 and not the 210 an earlier draft of this
handoff quoted.

**Build state.** `pdflatex` clean; zero overfull and zero underfull boxes from
this float (the four remaining underfulls in the log are pre-existing, in another
appendix table); `app:cooccurrence` resolves to Appendix~D and
`tab:preliminary-extraction` to Table~D.1; the §4.2.1 `\ref` reads correctly.
Rendered and read at print size.

**Owed, and deliberately not done.**

1. **Marc's framing paragraph.** Specified in the chapter comment; never drafted.
   Until it lands the float sits under a bare chapter heading and its placement
   will settle when the prose arrives.
2. **The caption's voice pass.** SESSION-DRAFTED and flagged. It is long — it
   runs to about a page-third above a compact table. That is per Marc's "push
   what is necessary to the caption", and conventions §b2, but it is the first
   thing to look at with fresh eyes. The `not_attempted` sentence is the most
   plausible cut, if that guard moves into Marc's paragraph instead.
3. **The four open calls in §(f)** — chief among them the `app:cooccurrence`
   rename, left undone because it edits a live sentence of Marc's.
4. **The prose supplement** in §(c) item 2 (the loop argument), which is now
   recorded as AVAILABLE in the §4.2.1 comment rather than taken.
