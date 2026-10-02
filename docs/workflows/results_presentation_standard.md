---
status: durable
created: 2026-10-02
updated: 2026-10-02
---

# Results presentation standard — what every results table and figure must meet

**Status:** durable. The yardstick for auditing a chapter 5 or appendix results
float before it is ratified. Load it with
[`figure_table_conventions.md`](figure_table_conventions.md) (the house look)
and [`evaluation_conventions.md`](evaluation_conventions.md) §d2, §k (run counts,
the reporting standards for the setup). This file covers what neither does: how a
**number** is printed, what an **empty cell** means, when a summary is **too thin to
report**, and what a **caption must decode**, so that no cell invites a question
about the result's validity.

**Why (Marc, 2026-10-02).** "Those little integration issues and those little
clarity issues ... the examiner will question the validity of your results." A
table that prints 1.00 beside a mean time taken over one run reads as an error,
and the reader then distrusts the cells that are right.

**Evidence.** Every rule cites the standard or guide it rests on. The quotes, URLs,
locators and confidence tags are in
[`../sources/extractions/results_presentation_conventions.md`](../sources/extractions/results_presentation_conventions.md)
(rule numbers R1.1–R8.6 there). A rule marked **declared** is a choice between
sources that disagree (that file's Part C); it binds because it is applied
everywhere, not because a source forces it.

**Status of each rule.** *Ratified* = Marc has ruled. *Proposed* = this file's
recommendation, applied only once Marc rules (the audit ledger lists each one).
Marc accepted every float and caption fix of the §5.1–§5.3 audit on 2026-10-02
("I accept all the changes that are required and the captions").

**Captions read alone (Marc, 2026-10-02).** "If somebody just read the captions
... they could figure out what's happening." A caption opens with what the float
shows, gives n, decodes every encoding and the reading direction of each metric
(what 1, 0 and below zero mean), and points to Section 4.5 for definitions; it
does not define a metric (the supervisor's 2026-09-22 rule). Test it with a cold
reader who sees only the rendered float and its caption.

---

## P — Precision and bounds

**P1. A value is rounded to its interval's precision.** Round the 95 % half-width
to one significant figure (two when that figure is a 1) and the value to the same
place; within a column, use the place of the column's widest interval, so the
column aligns. A half-width that rounds to zero at the column's place prints as
`<0.001` (at that place), never `± 0.000`; where an interval bound would round to
0 without being 0, the column goes one place finer, so the reader can see whether
the interval includes zero (Table 5.3's time lost). *Ratified 2026-09-30* (the house
precision rule, figure_table_conventions.md, "Precision and table size"). Sources:
Cole 2015 (R1.1–R1.3); SI Brochure, one format per column (R1.11).

**P2. Never print a bound of the scale that the value does not reach.** A
reduction of 0.997 prints `>0.99`, not 1.00; an ASP of 0.0003 prints `<0.01`, not
0.00. Exactly 1 and exactly 0 print as 1.00 and 0.00. The caption decodes the
symbol whenever the float uses it. In a figure, where a point at 0.997 and a point
at 1 cannot be told apart, the caption says so and names the table that does.
*Ratified 2026-10-02.* Sources: APA 7, "p < .001" (R1.8); Cole 2015, "never 0.000";
UK Government Analysis Function, `[low]`/`[high]` and "'0' only for a true zero"
(R1.8, R2.4).

**P3. One number format per column.** The same decimals (or the same place) down
a column; a true minus (`$-$`), never a hyphen; a thin space from 1 000. Sources:
SI Brochure §5.4.4 (R1.10, R1.11); APA 7 (R1.11).

**P4. Leading zero, thousands separator and the space before %: declared.** The
thesis writes `0.25` (SI and the Australian Style Manual; APA would write `.25`),
`1\,000` (SI; APA and the Style Manual use a comma) and `95\,\%` (SI; the Style
Manual uses no space). *Declared*; already the thesis's practice. Sources: R1.9,
R1.10, R6.8.

## S — Empty cells and symbols

**S1. A cell that cannot hold a value because none applies is blank.** The no-MTD
reference has no rank and no reduction: those cells are blank, and the caption says
why once ("no MTD is the reference ..., so its rank and reductions are blank").
*Ratified 2026-10-02.* Source: APA 7 §7.12, "if a cell cannot be filled because
data are not applicable, leave the cell blank" (R2.1).

**S2. A dash marks a value not reported, and the caption gives the reason.** The
reason is specific (for MTTC: "fewer than 10 runs compromise a target host").
*Ratified 2026-10-02.* Sources: APA 7, a dash "explain[ed] in the general note"
(R2.1); NCHS, every suppressed estimate footnoted with its reason (R2.5, R8.6).

**S3. One symbol, one meaning, across the dissertation.** A dash never also means
"not applicable" or "nil"; bold never means two things in one float; grey text
means "interval includes zero" wherever it is used. *Ratified 2026-10-02* ("two
different meanings ... through one symbol"). Sources: UK Analysis Function, "NA"
is ambiguous (R2.2); figure_table_conventions.md "dash is a binary channel and gets
one meaning".

**S4. Every encoding is decoded in its float's caption.** Bold, grey text, a dash,
a blank, `>`/`<`, hatching, a dashed line, a colour scale. Sources: APA 7 general
note (R2.3); Rougier et al. 2014 rule 4 (R8.1); figure_table_conventions.md §b2.

**S5. Prefer words or a defined mark to asterisks and daggers.** *Declared.* The
UK Analysis Function advises against `*` and `†` for accessibility (R2.2); the
thesis uses bold, grey text and `>`/`<`, each decoded.

## N — Small numbers and conditional summaries

**N1. A summary taken over too few runs is not reported.** MTTC is reported only
when at least **10** runs compromise a target host **and** its 95 % interval is no
wider than **160 %** of its value; otherwise a dash (S2). *Ratified 2026-10-02*
("don't report MTTC over too few runs"); the threshold is the NCHS standard for
rates from 2023 data (Kochanek et al. 2024, s. 3, p. 18; Parker et al. 2023,
Vital Health Stat 2(200), Table A), **borrowed by declared analogy**, because MTTC
is a conditional mean, not a rate. The older NCHS rule of 20 events applied to
data up to 2022 and is not cited. The rule lives once in code
(`tools/_ch5_style.py`, `mttc_unreported`) and every generator imports it. Sources:
R3.2; Dudley et al. 2016, halt estimates when fewer than 10 remain (R3.4).

**N2. A conditional summary names its denominator and sits beside it.** MTTC is a
mean over the runs that reach a target, which are right-censored at the time limit
(Arcuri and Briand 2014 §6). So every float that prints MTTC states that it is
conditional, and prints, or points to, the share of runs it is taken over (ASP).
Sources: R3.4; SAMPL, numerators and denominators (R3.1).

**N3. A mean over a subset of events states the share left out.** Time lost per
MTD deployment leaves out deployments with no no-MTD comparison; the share left out
is reported wherever it could change the reading (Table 5.3's caption gives the smallest share kept). *Ratified 2026-10-02.* Source: SAMPL,
"report numerators and denominators" (R3.1); CONSORT item 16.

**N4. A proportion's interval is not a Wald interval near 0 or 1.** Use
Clopper–Pearson (or Wilson) for ASP, and flag a proportion of exactly 0 or 1 as such
rather than printing a zero-width interval as if it were measured. *Ratified 2026-10-02* (Tables 5.2, F.3, F.4; `clopper_pearson` in `tools/_ch5_style.py`).
Source: NCHS proportions standard, Vital Health Stat 2(175) (R3.3, R4.8).

## I — Intervals and effect sizes

**I1. Every interval says what it is: its level and its method.** "95 % percentile
bootstrap interval over runs", "95 % interval on the mean (normal approximation)".
A float with two kinds names both. Sources: Wilke ch. 16; Cumming, Fidler and Vaux
2007 rule 1 (R7.4); Nature reporting summary (R8.2).

**I2. One name per interval method across the dissertation.** The same method is
called the same thing in every caption (terminology.md's one-term rule): "95 %
percentile bootstrap interval over runs", "95 % interval on the mean (normal
approximation)", "95 % Clopper--Pearson interval" (the constants `IV_BOOT`,
`IV_MEAN`, `IV_PROP` in `tools/_ch5_style.py`). *Ratified 2026-10-02.*

**I3. The number of runs behind every cell is stated or derivable.** The caption
or Table 5.1 gives it; where two series differ (4 000 runs for the APT attacker
model pooled, 1 000 for the baseline attacker), the caption says so. Sources:
Cumming et al. 2007 rule 2 (R3.5); Arcuri and Briand 2014 §11 (R3.6).

**I4. An effect size comes with its interval, its formula in words, and the raw
values it is built from.** Sources: Arcuri and Briand 2014 §11 (R4.3, R4.5);
Lakens 2013 (R4.4). Applies to §5.4's Cohen's d; not yet audited.

## R — Relative measures

**R1. Every reduction can be read beside the absolute values it compares.** A
reduction table prints, or points to, the reference value and the value under MTD.
Sources: CONSORT 2010 17b, "both absolute and relative effect sizes" (R5.1);
Hoefler and Belli rule 1, "never report ratios without absolute values" (R5.2).

**R2. Where the reference is small, say that the reduction saturates.** A
reduction from a small reference reaches its ceiling of 1 for any MTD that stops
nearly every success, so it stops separating MTDs. The text says so where a
float shows it (ASP reduction against the APT attacker model, whose ASP with no MTD
is 0.09). *Ratified 2026-10-02*; Table 5.4's caption prints the reference values, the sentence is Marc's. Sources: Cochrane Handbook §15.4.1 (R5.3); NCHS on relative
measures of small proportions (R5.5, an inference).

**R3. Aggregate the quantities, then take the ratio.** A layer's reduction is the
reduction of the pooled mean, not a mean of per-run ratios. Source: Hoefler and
Belli rule 4 (R5.4). Met: the layer means pool hosts compromised before the ratio.

## T — Tables

**T1. A table is readable without the text.** Every metric named verbatim as
Table 4.3 names it, every unit in its column header, every symbol decoded. Sources:
Australian Style Manual (R6.1); SI Brochure §5.4.1, quantity/unit headers (R6.7).

**T2. The sign of a signed measure is decoded.** A negative time lost, a negative
reduction: the caption says what below zero means. Source: S4; R6.1.

**T3. One term per thing, matching the text and the other floats.** A metric, a
mechanism class or a layer is named the same in the table, the figure, the caption
and the prose (terminology.md).

**T4. Cells never wrap.** A wrapped cell reads as two values. Widen the column or
drop the type size by the house rule (figure_table_conventions.md "Table size").

## F — Figures

**F1. Bars start at zero; a truncated axis uses points, and the caption says
where the axis starts.** Source: Wilke ch. 6.3, ch. 17 (R7.1).

**F2. Panels to be compared share axis ranges; where they cannot, the caption
says so.** Source: Wilke ch. 21 (R7.2, R8.4).

**F3. Lines join points only over an ordered factor.** Source: Hoefler and Belli
rule 12 (R7.5).

**F4. The same thing looks the same in every figure.** Series encoding, layer
names and panel titles match across figures. Source: Wilke ch. 21 (R7.3).

**F5. A caption's claim about the plot holds for every point.** "1 with no
whisker means no run" must be true of every point drawn at 1 (P2). Source: Rougier
et al. 2014 rule 7, "do not mislead" (R7.6).

**F6. Error bars too small to draw are stated in the caption.** Source: Hoefler
and Belli rule 12 (R8.5).

---

## Audit procedure (per float)

1. Render the float from the built PDF (`gs -sDEVICE=png16m`), and read it cold.
2. Check every cell against P1–P3 and S1–S5; check every summary against N1–N4.
3. Check the caption against S4, I1–I3, T1–T2 and F5.
4. Recompute three cells from the numbers file the generator names, including
   any cell at a bound, a dash, or a small n.
5. Record each finding in the audit ledger (`docs/handoffs/`) with its rule ID,
   the cell, the fix, and whether the fix is ratified or proposed. Apply ratified
   fixes in the **generator**, never in the `.tex`.
