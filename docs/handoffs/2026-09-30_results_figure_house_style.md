---
status: open
created: 2026-09-30
---

# Finish the results-figure house layout: file keys, the owed figures, the headline ruling

## State of play

The supervisor's read of §5.2–§5.3 found the figures inconsistent: keys in a
different place in every figure, titles on some panels and not others, series
re-encoded between figures. The standard is now
[`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md)
§o. It is applied to Figures 5.1–5.7 through two helpers in
`tools/_ch5_style.py` (`panel_title`, `key_row`), and all seven chapter 5
figure environments are `[tp]`. Every panel has a `(a) Title`. Every key sits
directly above what it decodes. The baseline attacker is a grey square on a
dashed line everywhere. The pooled APT attacker model is black in 5.4 and 5.7.
The build is clean at 103 pages. Values, chart types, scales and captions
were not touched.

**The "two Figure 5.2 headings".** The 2026-09-29 build has no duplicate
Figure 5.2 caption, no duplicate label and no duplicate include. The likely
cause was Figure 5.3, whose file is still keyed `fig_5-2-2a_…`: it printed
"MTD deployment" as a heading above both panels (a) and (b). That label is
now one key entry (§o rule 4). A second candidate is Table 5.2 and Figure 5.2
sitting a page apart. They are separate counters, which is standard LaTeX. If
Marc meant something else, ask for the page.

## What is owed

1. **Re-key the chapter 5 files (§j).** The 2026-09-23 restructure moved the
   floats without renaming their files. Every chapter 5 figure file name is
   now stale:

   | Now | Should be | Generator STEM |
   |---|---|---|
   | `fig_5-2-1a_campaign_openings` | `fig_5-2a_…` | `ch5_unopposed_figures.STEM_A` |
   | `fig_5-2-1b_attack_confidentiality` | `fig_5-2b_…` | `…STEM_C` |
   | `fig_5-2-2a_disruption_response` | `fig_5-3-1a_…` | `ch5_disruption_figure.STEM` |
   | `fig_5-3-2b_interval_headline` | `fig_5-3-2a_…` | `ch5_sweep_figures.STEM_HEAD` |
   | `fig_5-3-3b_interval_mechanisms` | `fig_5-3-3a_…` | `…STEM_MECH` |
   | `fig_5-3-3c_interval_schemes` | `fig_5-3-3b_…` | `…STEM_SCH` |
   | `fig_5-4a_ablation` | `fig_5-4-1a_…` | `ch5_ablation_figure.STEM` |

   Four retired figures block three of the targets: `fig_5-3-1a_suppression_profiles`,
   `fig_5-3-2a_cross_arm`, `fig_5-4a_frontier` and `fig_5-4b_time_split`.
   Their floats were retired on 2026-09-23. Rename them `fig_unplaced_…`
   (with their generators' STEMs) or delete them. Recommend delete: git
   history keeps them, and FLOATS.md already strikes them through. The table
   fragments have the same drift (`tab_5-2-1a`, `tab_5-3-1a`, …). Do figures
   and tables in one commit with `FLOATS.md`, because it touches
   `dissertation.tex`. Check first that no parallel session has the tex dirty.
2. **Figure 5.3's pooled APT attacker model is still blue** (§o rule 5 says
   black). It was left because the two shaded dips in (a) and (b) would both
   turn grey and stop being told apart. `chore/disruption-mechanism` proposes
   replacing this figure's metric, so apply rule 5 in that rebuild, not
   before.
3. **Figure C.1** (`tools/ch5_sensitivity_figure.py`, appendix) is a results
   chart and is not yet on §o. It is also included at `0.78\textwidth`
   rather than bare (§h).
4. **Headline emphasis, Marc to rule** (§o rule 9): bold only the value the
   text cites as the headline, at most one per column, decoded in the
   caption. The figure half needs no change (Figure 5.4 already does it).
5. **Content flags, not formatting (Marc's call, left untouched):**
   - Figure 5.1(b) still draws attack path variation ("APV (%)"), which
     `1785cf99`/`529a67f7` replaced with distinct attack paths in §4.5.
   - Figure 5.3(c) draws time lost per MTD deployment, which `1785cf99`
     retired.
   - NCR reduction is on a 0–1 scale in Figures 5.4–5.6, but every other
     share in chapter 5 is a percentage. The prose matches each figure, so
     this is a units choice, not a defect.
   - With panel titles on the figures, the captions can lose their
     per-panel "(a) … (b) …" naming where the title now says it. That is
     Marc's prose.
6. **Generator drift on two table fragments.** `ch5_sweep_figures.py` emits
   `\begin{table}[H]` for `tab_5-3-2c_attacker_values` and
   `tab_5-3-2d_attacker_ranking`, but the committed fragments say `[htbp]`,
   so they were hand-edited after generation. The next regeneration will
   silently revert them. Fix the generator (or the fragments) to match §k
   rule 8.

## Validation gate

- `grep -n "panel_letter\|anchor=south east.*LONG" tools/ch5_*.py` finds no
  hand-placed titles, and every chapter 5 figure's `.tex` has a key and
  titles drawn by the helpers.
- `ls docs/thesis/figures/fig_5-*` shows only placed files, keyed to their
  headings. `FLOATS.md` matches.
- The PDF build is clean, with no new overfull box in chapter 5. A contact
  sheet of the chapter 5 pages shows every key in the §o slot and every
  figure at the top of its page.

## Hard constraints

- Layout only. No value, scale, chart type or caption changes without Marc
  ("do not look at the correctness or accuracy of the values themselves").
- Values flow from the tracked JSON (`data/results/ch5_*`). Never hand-edit
  a generated fragment.
- Parallel sessions: `feat/ablation-narrative` (merged) and
  `chore/disruption-mechanism` (Figure 5.3's replacement) touch the same
  figures. Re-check `git status` before editing the tex.

## Reading list

- `docs/workflows/figure_table_conventions.md` §o, §j, §h
- `tools/_ch5_style.py` (the helpers and the series contract)
- `docs/thesis/FLOATS.md`
- `tools/ch5_sweep_figures.py` (the fullest use of the helpers)
