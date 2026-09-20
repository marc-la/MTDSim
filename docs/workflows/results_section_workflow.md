# Results-section workflow — from a placeholder float to a populated one

**Status:** durable, session-facing. The process that produced §5.3.1 (Figures
5.2–5.3, Table 5.4) on 2026-09-15, written down so the next results subsection
(§5.3.2, §5.4.x, §5.5) follows the same path instead of re-deriving it. Rules
here are mechanisms, not exceptions: where §5.3.1 hit a trap, the rule below is
the general form.

The path has seven stages. Marc rules twice: once on the run plan (stage 2),
once on the preliminary read (stage 4). Nothing reaches the tex before both.

## 1. Orient — read what the section already owes

Before any run, read in this order and take notes against each:

1. **The section's floats in the tex** — the `\placeholderbox` text and the long
   caption of every float, plus the comment blocks above them. The captions fix
   *what is measured*; the comment blocks carry the rulings (which measures were
   killed, which are ruled exhibits, which columns wait on a ruling).
2. **Tables 5.2 and 5.3** (`docs/thesis/tables/tab_5-2*.tex`) — the levels are
   the run plan and the held rows are the pins. A level not in Table 5.2 is not
   run; a pin not in Table 5.3 is not a configuration.
3. **The discussion affinity board** (`docs/handoffs/*ch6_discussion_affinity_board.md`
   §5–§6) — which discussion points this section's measurements feed, and which
   foundation risks rest on it. The preliminary read reports which way each moved.
4. **The records the floats were shaped on** (`docs/implementation/pipeline/ogasp/*_findings.md`,
   `plurality_reporting.md`, etc.) — and, critically, *the configuration they ran
   at*. Every §5.3.1 record predated the chapter's pins (general objective, v1
   overlay, ten seeds), so the picture was expected to move.
5. **The seam** (`src/mtdsim/l3_simulation/movement/run.py` `run_movement`,
   `_install_objective`; `measures.py` for every instrument) and the nearest
   prior recorder (`data/results/profile_divergence/run_study.py`,
   `data/results/targeted_attacker_build/run_gate0.py` for the baseline arm).

**Time one run per arm and horizon** at the exact configuration before writing
the plan. It gives the plan a real budget (movement 0.13–0.34 s, baseline
0.05 s at 50 hosts) and it surfaces configuration surprises early — the seed-0
probe showed a profile reaching the target unopposed, which became the section's
main finding.

## 2. Design — a handoff for acceptance, then ask once

Write `docs/handoffs/YYYY-MM-DD_ch5_<section>_runs.md` with:

- **The cell set as a table keyed to Table 5.2's factors**: one row per factor,
  the level(s) run here, and why. Say explicitly which factors collapse for this
  section (under no defence the interval and the timing regime are not read).
- **The pins translated to seam keyword arguments**, one row each, with the
  literal value passed. **Name the overlay and the mapping by version string**;
  the registries' defaults are experiment 1's (`v1_band_relationship`,
  `v1_ckc_total`), not the chapter's, and a run at a default is a different
  configuration.
- **The measure read per float**, naming the `measures.py` function, the
  aggregation (`interval_report`, `divergence_report`), and how the baseline row
  is filled (structural cells stated as such, never measured).
- **Extension and diagnostic arms** the section can afford: the one-at-a-time
  factor levels that are cheap here (the 60 000 s horizon under no defence has no
  dose confound), and a diagnostic arm that attributes any moved number to one
  switch (the general-objective arm). Diagnostic arms are read in the analysis,
  never drawn.
- **Rulings owed**, each with a recommendation, so Marc can accept in one word.

Commit the handoff, return the cell set in the chat, and stop. Do not launch.

## 3. Record — `data/results/ch5_<section>/run_corpus.py`

- One JSONL row per run; the job dict spread into the row (`arm`, `profile`,
  `objective`, `horizon`, `seed`), then the run-level fields, then the stream.
- **Movement rows carry the full per-visit stream** in the
  `profile_divergence` shape (`place, verb, outcome, verdict, blocked,
  interrupted, dwell, start, end, place_class` plus `last_next_place`), so every
  suite measure can be rebuilt without re-simulating.
- **Baseline rows carry the native attack record** (`name, start, finish,
  compromise_host, compromise_host_uuid`), wired through the same
  `_install_objective` seam as the Gate 0 harness so both arms face the same
  objective.
- Errors are written as rows, never dropped; `ProcessPoolExecutor` at six
  workers; seeds 0–99 shared across arms; 100 seeds even for a preliminary,
  because the cost is minutes and a re-run later costs more than the seeds.
- `data/results/` is gitignored. Force-add the recorder, the analyser and
  `numbers.json` (the Gate 0 precedent) so the figures regenerate from a
  versioned artefact; never the JSONL.

## 4. Read — `analyse.py`, previews, the findings record, the chat return

- `analyse.py` is a **pure reader** over `runs.jsonl`: rebuild `MovementRunResult`s
  exactly as `profile_divergence/analyse.py` does, call the suite's measures,
  never re-derive maths. The only RNG is the seeded split-half null.
- **Sanity block first**: error rows, runs per cell, the baseline's structural
  zeros present, `max_events` terminations. The generator refuses a corpus whose
  sanity block fails.
- Every number any float could quote goes into `numbers.json`; the extension and
  diagnostic arms go in beside the core, keyed apart.
- **Check what a "reached objective" means per arm.** The baseline's
  `end_event` fires on the target *or* on the inherited 80 % compromise ratio;
  read time-to-target from the attack record, not `termination_time`, and split
  the ending column. The movement arm's run ends at the target.
- **Previews are matplotlib, for direction only**; look at them (the Read tool
  renders PNGs) before writing a word. They are never the route into the tex.
- Write `docs/implementation/pipeline/ogasp/ch5_<section>_findings.md`:
  configuration and sanity; one section per float with the numbers; the
  extension and diagnostic reads; **"what the floats need changed"** as a
  numbered list with a recommendation each; **"against the record"** as a table
  of record value, new value, and what moved it.
- The chat return is thesis-framed (session_workflow.md): what each float now
  says, what changed premise, the rulings needed. Send the previews.

**Expect saturated columns.** Under the partial mapping every depth-shaped
measure reads the same on every profile (deepest successful stage 2.00 ± 0.00;
advance-after-first-success 1.00). Check spread before proposing a column, and
substitute the measure the record names for the same axis (successes per
distinct host for persistence), not a near-synonym.

## 5. Rule — Marc reads §6 of the findings

"Do the necessary updates" means the recommendations as written; a substitution
forced by the data (a proposed replacement column that is also saturated) is
made and reported, not re-asked.

## 6. Draw — `tools/ch5_<section>_figures.py`, then the tex

The generator reads `numbers.json` and emits the figures **and** the table
fragment, prints every caption fact, and compiles.

Figures (figure_table_conventions.md §f, §h, §l; thesis-figure-pipeline memory):

- TikZ standalone, 12 pt, `helvet` 0.92, `\footnotesize` labels; pack to the
  page box — **15.7 cm natural for a full-width figure** (the 2 pt standalone
  border and rounding put 16.0 cm over `\textwidth` by 5.7 pt) — and include
  bare. Print the `gs -sDEVICE=bbox` size and a fits / TOO WIDE verdict.
- Series encoding is the chapter's contract: one hue and one marker per profile,
  identical in every figure from §5.3 on; the baseline attacker a dashed grey
  line; a key panel shown once per multi-panel figure. The five hues are in the
  generator's `COLOUR` map and passed the dataviz validator; reuse them, do not
  re-pick.
- Time courses that saturate early get an overview panel and a zoom panel
  sharing the y axis, lettered, with the zoom window marked on the overview.
- Printed-value matrices: grey ramp on the off-diagonal, diagonal unfilled,
  every cell printed; the caption decodes both.
- Render the PDF to PNG and **look at it** before touching the tex.

Tables (figure_table_conventions.md §k):

- `\tablestyle` fragment under `docs/thesis/tables/`, GENERATED header comment,
  the caption inside the fragment. Try `\footnotesize` first; a table with seven
  numeric columns and intervals does not fit, so drop to `\scriptsize` with
  `\tabcolsep` 3 pt **together**, centred fixed-width `p{1.5cm}` numeric columns
  so two-line headers wrap inside the column, and a `P{3.0cm}` label column so
  the longest profile name does not wrap.
- Intervals as `$m \pm c$` to one decimal; shares to two.
- No `\rowgroup` on a one-row group — the rotated label collides with the
  group above; the `\midrule` carries the structure.
- Structural baseline cells carry a mark decoded in the footnote row; the
  footnote row spans exactly the column count.

Tex:

- Replace each `\placeholderbox` float with the include or `\input`, keep the
  label, and put a `% POPULATED YYYY-MM-DD (tool; corpus; record)` comment above
  it saying what changed against the placeholder. Captions edited from the
  placeholder's carry a DRAFT STATE line; the voice pass is Marc's.
- `docs/thesis/FLOATS.md`: a row in the figures list, a row in the tables list,
  and the planned-floats row flipped to **LANDED**.
- Build with `pdflatex` twice (plus `bibtex` once); `latexmk` is not installed.
  Grep the log for `^!` and for `Overfull` at the new float's line numbers, then
  render the built pages (printed page number + the front-matter offset, 10 at
  the time of writing) and look at them. Iterate until the table sits inside the
  margins and the header row aligns with the body.

## 7. Commit — and the two things that are not the session's

- Stage by file. If Marc has an uncommitted hunk elsewhere in
  `dissertation.tex`, stage only the section's region: write HEAD's file with
  the section swapped for the working copy's, `git add`, then restore the
  working copy. His hunk stays unstaged and untouched.
- Update the handoff status to what is still owed (typically the caption
  ratification and any unruled column) and the findings status to "applied".
- **Overleaf is Marc's**. There is no git remote for it; the only credentials on
  the machine are the literature-review project's, and it has no git access. A
  push needs the dissertation project's ID and token. Until then, list the paste
  set: the section's tex block, the figure PDFs, the table fragment.

## Traps met on §5.3.1, so they are not met twice

| Trap | Rule |
|---|---|
| Registry defaults are experiment 1's, not the chapter's | pass `overlay_version` and `mapping_version` by name, always |
| Baseline `end_event` also fires on the 80 % compromise ratio | split target / ratio / horizon; time to target from the record |
| Depth measures saturate under the partial mapping | check spread before a column; substitute the record's own measure |
| A `%` in a TikZ label inside a `%`-formatted string | write `\%%`; run the generator before trusting it |
| `sed` on TeX backslashes silently matches nothing | edit generators with a Python replace and assert the count |
| A standalone at 16.0 cm overflows by the border | pack to 15.7 cm; the generator prints the verdict |
| `\multicolumn` span left at the old column count | the span equals `len(columns)`; compile and look |
| `\rowgroup` on a one-row group | drop it; the rule separates |
| `latexmk` absent | `pdflatex` × 2 with `bibtex` between |
| PDF page ≠ printed page | printed + front-matter offset; verify with the aux label |

## After the float lands — scrutinise it

A populated float is not a settled one. Before it is ratified, run the
[`scrutinise-figure`](../../.claude/skills/scrutinise-figure/SKILL.md) skill
(first run: Figure 5.1, 2026-09-20): the subsection's takeaways are defined
first, then a cold reader (figure, caption and one introducing sentence only)
and a context critic test the float against them, and it is reworked until
neither reports a blocking defect.
