---
status: open
created: 2026-08-20
updated: 2026-08-20
---

# The dwell-time catalogue — chapter table, appendix derivation, exponential entry

**Goal:** three artefacts from one declared family **(ruled 2026-08-20)**: the
in-prose dwell parameter table (§4.2.4.1), the appendix dwell-derivation table
(debt dictated 2026-08-19 — the prose already points: "You can see the appendix
for this"), and the exponential-shape justification entry in `app:sensitivity`.

> **BUILT 2026-08-20.** All three artefacts landed and the document compiles
> clean (no undefined reference; zero overfull or underfull box attributable to
> these floats). `tab:dwell-catalogue` is Table~4.1 in §4.2.4.1;
> `tab:dwell-derivation` is Table~B.1 at `app:dwell-derivation`;
> `tab:anchor-sensitivity` and `tab:shape-substitution` are C.1--C.2 in
> `app:sensitivity`. Generator: `tools/dwell_catalogue_tables.py`.
> `tests/l3_simulation/test_durations.py` passes at 12.
>
> **Still owed, and all of it Marc's:** the caveat sentence beside Table~4.1
> (slot flagged in the tex); the framing prose in both `app:sensitivity`
> sections (slots carry the numbers); and the proofread of the 15
> `short_justification` strings, which are PROVISIONAL. Corrections go to
> `data/ogasp/tactic_durations.json` and are regenerated --- never typed into
> the emitted `.tex`.
>
> **Deviations from the spec above, with reasons:**
> 1. **The appendix table dropped its `Mult.` column.** At six columns the float
>    ran 14.8 pt too wide and 67 pt too tall for the page. The multiplier is
>    already in the chapter's panel~(b), which is where must-carry item 4
>    (same-verb-different-dwell) is discharged, so the appendix repeating it was
>    the cheapest thing to lose. Its caption now points at
>    `tab:dwell-catalogue` for the multipliers.
> 2. **The short justifications were tightened twice** --- the first cut ran
>    ~150 characters and wrapped to five lines a row, which is what pushed the
>    float off the page. Two were then reworded to clear loose lines
>    (`collection`, `lateral-movement`). All still PROVISIONAL.
> 3. **Artefact 3 landed as two sections, not one.** Table~4.1's caption claims
>    band robustness is reported in `app:sensitivity`, so that pointer had to be
>    earned: C.1 reports the anchor sweep, C.2 the shape substitution.
> 4. **Values are typed in `app:sensitivity`**, flagged in the tex --- the
>    sweep's `numbers/` workspace is untracked by design, so the docs record is
>    the only source. Same declared deviation as `tab:experiment-one`.

Specified at the 2026-08-20 planning pass; every ruling below marked
**(ruled 2026-08-20)** is Marc's from that dictation. Items marked **CONFLICT**
are where a ruling supersedes or strains an earlier one — his to close.

## The governing split — the what and the why **(ruled 2026-08-20)**

> The chapter table carries the **what**: the settled micro-parameters, one
> value per tactic. The **why** — how each number was arrived at — goes to the
> appendix, where it is allowed to get messy; anything that will not sit even
> there goes to `app:sensitivity`.

This is the principle the whole build answers to. The main argument stays tight:
§4.2.4.1 gains a table reference and Marc's caveat sentence, and nothing else.

The corollary, ruled the same day: the reader does not know what a badge means,
so the badge stays a one-word label in the table and its **decode and pointers
live in the caption**. That is conventions §b2 exactly (the caption decodes every
encoding; a reader seeing only the float can read it completely) — the corpus
precedents are he2025's shading footnote and brown2023's abbreviation keys.

## Sources

`data/ogasp/tactic_durations.json` (the declared catalogue). Derivation
rationale from the record: the anchor-verb / multiplier / shape reasoning per
tactic ([`../implementation/pipeline/ogasp/`](../implementation/pipeline/ogasp/)
timing records; the §4.2.4.1 prose narrates the tiering — verb constants where
sufficient, multipliers where not, judged shape otherwise; e.g. 45.0 s = 10×
the exploit shape; resource-development 0 s as off-network).

The sweep evidence is [`../implementation/pipeline/ogasp/rate_feasibility_study.md`](../implementation/pipeline/ogasp/rate_feasibility_study.md):
pre-registered, 1 740 runs under the settled S3-R regime (1 728 under the
superseded hybrid), sweeping **all four group anchors** across their
catalogue-derived bands plus a same-mean Erlang-*k* shape check. Headline: no
anchor band inverts any conclusion, and the sensitivity is concentrated in the
low-and-slow anchor — the two MTDSim-priced anchors are inert.

## What the table carries that the prose cannot **(ratified 2026-08-20)**

The acceptance test for any layout. The prose at l.695–737 already argues the
case in Marc's voice; the table must not re-argue it, only enumerate.

1. **All fifteen tactics with a value.** The prose gives two worked examples.
2. **Four anchors, not fifteen free parameters** — the identifiability argument
   (anti-circularity rule 2). Fifteen tactics resolve to **six distinct values**
   (0, 4.5, 22.5, 35.0, 36.0, 45.0) off four families. Shown, not claimed.
3. **The evidence grade per family** — the badge *is* the validity claim.
4. **Same-verb-different-dwell**, the quiet argument: live under the v2 mapping,
   where `initial-access` and `execution` both dispatch `EXPLOIT_VULN` but dwell
   4.5 s and 22.5 s. The multiplier column is what shows it — do not collapse.
5. **The ordering/ratio structure the thesis turns on**: the 45 s low-and-slow
   dwell sits an order above the priced verbs but below the 200 s MTD trigger
   interval, so the interval-vs-dwell contest stays live rather than degenerate.

## The chapter table (§4.2.4.1) — `tab:dwell-catalogue`

Parameter-table genre (conventions §e3), booktabs, no vertical rules, emitted
from the JSON — **no value typed** (§h). Floated **after** the exponential
paragraph (~l.737), not after the derivation paragraph: the `Exp(μ)` semantics
in the column header must already be declared in prose. Referenced from the
derivation paragraph at l.715 alongside the existing appendix pointer.

**Two blocks in one float (ruled 2026-08-20)**, superseding the original
"keep it minimal (tactic | dwell | note-at-most)" line — see CONFLICT 1.

**(a) Anchor families** — five rows: family | priced from | value (s) | badge.
This is the four-anchor argument made structural, and it is where the badges
live (the badge is constant within a family, so it never repeats down block b).

**(b) Per tactic** — fifteen rows in the **shared tactic-axis order**
(conventions §b6 is a hard rule; grouping by family would show the structure
more loudly but break the axis contract with `fig:l1-graph` and the weight
matrix): tactic | family | multiplier | mean dwell (s). Value column
right-aligned, units bracketed in the header.

### The badges **(ruled 2026-08-20)**

Three, not four. Tier 2 and Tier 3 collapse into one chapter badge because
**under `v0-uncalibrated` their validity claims are genuinely identical** — both
declared, both swept, neither calibrated. The objective anchor's status is
"literature-calibratable … once the runner lands": the macro targets are *named*
(Sophos access→exfil median ~73–79 h; Bromiley ~64 % collect+exfil ≤ 5 h;
ransomware encryption ~6 min–2 h) but **no check has been run**, so no badge may
say "checked". The tier number and the named target go to the appendix row,
where the distinction is honestly prospective. If v1 calibration lands, the
badge splits back out.

| Family | Badge | Caption points it to |
|---|---|---|
| Scan-shaped, exploit-shaped | **Priced by MTDSim** | the simulator's own action costs (ch2; §4.2.4.1 prose) |
| Low-and-slow, objective execution | **Declared and swept** | `app:sensitivity` — the anchor sweep |
| Off-network prep | **Declared, off-clock** | §4.2.3 — the GSPN immediate transition, already introduced at l.548 |

**"Substrate" is repo vocabulary and does not enter the thesis (ruled
2026-08-20.)** In the tex it is the **simulator**, or **MTDSim**. Ten of its
eleven tex occurrences are in comments; the eleventh is the `tab:experiment-one`
caption (three uses), drafted at the appendix-wiring pass and never voice-passed
— recorded here as a terminology-registry item for Marc, **not** rewritten by
this brief.

### The caption contract

Long caption decodes, short caption mandatory (§c — `\caption[short]{long}`).
The long form must carry, and nothing here may be left to the reader:

1. each badge decoded in a clause, with its pointer (table above);
2. the distribution semantics — mean dwell, `Exp(μ)`; and that resource
   development is a **GSPN immediate transition, not `Exp(0)`**, which is
   degenerate;
3. **hazard (a), closed precisely**: under S3-R the movement layer supplies
   every unit of the attacker's time — the dwell *replaces* the dispatched
   verb's native cost, it is not charged on top of it. Without this sentence a
   careful examiner reads "priced by MTDSim" as double charging;
4. the catalogue version pin (`v0`) and the ATT&CK version (§b5).

The **caveat sentence stays in prose beside the float and is Marc's** (standing
must-carry): model parameters anchored to this simulator, not real-world
measurements. Flag the slot — see CONFLICT 3.

**No ATT&CK id column, and no bracketed ids after the tactic names (ruled
2026-08-20)** — names only; the version pin in the caption is what conventions
§b5 actually asks for.

**Exponential folded in lightly (ruled 2026-08-20):** column header + footnote,
no rate column — for an exponential the mean *is* the whole parameterisation, so
a λ column would be fifteen numbers that are a deterministic function of the
column beside them. If the float still reads heavy once drawn, the first thing
to cut is the multiplier column, not the badges — but see CONFLICT 2 first.

## The appendix derivation table — `app:dwell-derivation` (B.4, reserved)

The **why**, and it is allowed to be dense. Columns: tactic | shape source |
multiplier | declared value (s) | sweep band | why (short justification). Same
tactic-axis order. Footnote row for provenance (§b4) carrying the catalogue
version and the corpus pin.

- **Sweep bands live here, not in the chapter**: they are **per-tactic and vary
  within a family** (`initial-access` and `lateral-movement` are both
  exploit-shaped at 4.5 s but carry [0.5, 2.0] and [0.25, 4.0]), so they cannot
  collapse into block (a), and fifteen band cells would swamp the chapter table.
  The distinction to hold: the appendix declares the **bands**; `app:sensitivity`
  reports what happened when they were **swept**. Bands are parameters; the
  sweep is a result.
- **Column heading is "shape source", never "anchor verb" — hazard (b).** The
  derivation input is not the runtime mapping and the two genuinely differ:
  `persistence` takes the low-and-slow shape but is **dwell-only** under v2;
  `reconnaissance` is priced off three scan verbs (5+5+25) but dispatches only
  `SCAN_HOST`. Headed "anchor verb", a reader finds it contradicting
  `fig:controller-mapping`. The footnote says so explicitly.
- The vocabulary discipline is load-bearing: values are **declared and justified
  against the literature — never "calibrated", never "from the literature"**
  (standing ruling; the operational_validation "calibrated" vocabulary is
  aspirational and stays out).

### The short-justification field **(ruled 2026-08-20)**

The JSON's `justification` strings are multi-sentence — too long for a cell. Add
a **`short_justification`** field per tactic to `data/ogasp/tactic_durations.json`
and emit the column from it. Keeps the tool dumb (hard-coding the strings in
`tools/` is out under mechanism-not-exception). Two obligations ride with it:

- add it to `REQUIRED_ENTRY_FIELDS` in `tests/l3_simulation/test_durations.py`
  so a missing one fails rather than emits an empty cell;
- the strings are **PROVISIONAL pending Marc's proofread** (his ruling: "we can
  put them in for now"). Mark them so in the commit message.

`data/` is mutated by concurrent sessions — re-read before writing (standing rule).

## The exponential entry (`app:sensitivity`)

**(Ruled 2026-08-20:** how the exponential was settled is additional
sensitivity analysis, not chapter prose.**)** The chapter keeps its live
declaration + stochastic-evidence citations (`holm2014, madan2004, bland2020` —
the VERIFY-the-subset flag on those is Marc's, still open). The 2026-08-19
ruling already routes the sweep pointer to the appendix; the standing V6
tension (results preamble vs appendix for swept parameters) is recorded as
Marc's to reconcile — **do not re-open**. A sweep-wiring handoff remains a
MAYBE (his 2026-08-19 "leave that as a handoff as well") — owed when this
appendix is actually built.

Structure and numbers are already written and need distilling, not deriving —
[`stochastic_timing_design.md`](../implementation/pipeline/ogasp/stochastic_timing_design.md)
§3.1–3.3 and [`exponential_as_tractability_choice.md`](../notes/ch4_methods/exponential_as_tractability_choice.md).
The spine: what the exponential assumes (memoryless, mode at zero, CV fixed at
1); where it is defensible (scan/exploit, retry-until-success) and where it is
wrong (the low-and-slow group, whose paced character is the opposite of a
mode-at-zero draw); the mean-is-load-bearing argument from madan2004 **and its
stated leak** — routing here is not dwell-independent, because a long dwell is
likelier to be interrupted, so shape re-enters through the interrupt channel in
exactly the regime the thesis is about; holm2014 as counter-evidence,
acknowledged rather than buried. Framing prose is Marc's.

## CONFLICTS — flagged for Marc, not resolved by this brief

1. **Two-block table vs "keep it minimal".** The original brief said tactic |
   dwell | note-at-most. The two-block layout supersedes it — recorded as a
   supersession, since the flat version cannot carry item 2 of the must-carry
   list (the four-anchor argument). Ratified twice in dictation; noted here so
   the earlier line is not read as still live.
2. **Is the multiplier column *what* or *why*?** Under a strict what/why split
   it looks like *why*. **Recommendation: it stays.** A tactic's parameter *is*
   anchor × multiplier — that is the parameterisation itself, not its
   justification; and it is the only cell that carries must-carry item 4
   (same-verb-different-dwell), which Marc ratified. The *why this multiplier*
   is what goes to the appendix. Needs one word from Marc, since it also decides
   the trim-first order if the float reads heavy.
3. **Caveat sentence: prose or caption?** Ruled earlier as prose beside the
   float; the caption is now carrying four decode obligations. **Recommendation:
   caveat stays in prose** — it is a claim about the model, not a decode of the
   float, and moving it would put a Marc-voice sentence inside a generated
   caption. Cheap to flip if he prefers the float self-contained.
4. **Downstream:** collapsing tiers 2–3 for the chapter means the three-tier
   scheme in [`operational_validation.md`](../notes/ch4_methods/operational_validation.md)
   no longer matches its chapter face. That note wants one line recording that
   under v0 the chapter shows three badges, and why. Not this brief's edit.

## Considerations

1. Zero-dwell rows (resource-development 0 s) need a formatting decision that
   doesn't read as missing data — "0" with the off-network footnote, not a dash.
   Its multiplier cell takes an em dash, not "0.0" (there is no anchor to scale).
2. Same-verb-different-dwell is the table's quiet argument — the multiplier
   column is what shows it; don't collapse those rows.
3. Artefact freshness: emit at build time from the tracked JSON; concurrent
   sessions mutate `data/` (standing rule).
4. One generator, `tools/dwell_catalogue_tables.py`, emitting both bodies into
   `docs/thesis/tables/` (`dwell_catalogue.tex`, `dwell_derivation.tex`),
   `\input` from the tex. Regenerate, never hand-edit.
5. **Use `tools/_tactic_axis.py`** — landed by a concurrent session after this
   brief was first drafted, and it is "the single source for anything built
   after it". It supplies the row order, the sentence-case display names read
   from the pinned bundle (so no label map is typed, and the Australianisation
   ruling is honoured by lookup), and `version` for the §b5 caption pin — which
   discharges caption-contract item 4 by generation rather than by hand. Both
   tables take **`matrix_order`**, not `stage_grouped_order`: the dwell
   catalogue draws no stage bands, and matrix order is what `fig:l1-graph`
   takes. Declare the choice in the generator docstring, as the module asks.

## Validation gate

Chapter table wired in §4.2.4.1 with the caveat slot flagged for Marc and a
caption discharging all four contract items; appendix derivation table placed
with a real label the prose's "see the appendix" resolves to; exponential entry
drafted as structure + numbers (prose Marc's); every value traceable to the JSON
or the record; `pdflatex` clean, zero overfull, both floats in the List of
Tables as one line each.

## Reading list

1. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md)
2. `data/ogasp/tactic_durations.json`
3. [`../implementation/pipeline/ogasp/`](../implementation/pipeline/ogasp/) — `stochastic_timing_design.md`, `rate_feasibility_study.md`, `operational_validation.md` (vocabulary boundary)
4. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §b2, §b5, §b6, §c, §e3, §h
