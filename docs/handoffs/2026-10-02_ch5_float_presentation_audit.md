---
status: open
created: 2026-10-02
updated: 2026-10-02
---

# Chapter 5 floats against the results presentation standard — audit ledger (§5.1–§5.3 and Appendix F.1–F.4)

**Goal.** Every table and figure that §5.1–§5.3 report from is strictly conventional
and defensible: no cell, symbol or caption claim an examiner can use to doubt the
result. The yardstick is
[`../workflows/results_presentation_standard.md`](../workflows/results_presentation_standard.md)
(rule IDs below); its evidence is
[`../sources/extractions/results_presentation_conventions.md`](../sources/extractions/results_presentation_conventions.md).
§5.4 and Appendix F.5 are **out of scope** until Marc opens them (Marc, 2026-10-02:
"don't do 5.4 yet").

**Scope audited.** Table 5.1 (`tab:experiment`), Figure 5.1 (`fig:aio-coverage`),
Table 5.2 (`tab:unopposed-summary`), Figure 5.2 (`fig:aio-adaptivity`), Table 5.3
(`tab:disruption`), Table 5.4 (`tab:eff-cross-arm`), Figure 5.3
(`fig:eff-cross-arm`), Figure 5.4 (`fig:eff-suppression-profiles`), Tables F.1–F.2
(`tab:eff-interval-values[-asp]`), Tables F.3–F.4 (`tab:full-movement`,
`tab:full-baseline`). Each was rendered from the built PDF, read cold, and its
bound, dash and small-n cells recomputed from `numbers_reported.json` /
`time_lost_numbers_reported.json` (1 000 seeds).

---

## A. Applied (ratified rules; generators changed, floats regenerated, build clean)

Marc ruled 2026-10-02: no rounded bound (P2), no MTTC over too few runs (N1),
two meanings need two symbols (S1–S3), no bold for it. Applied in the generators,
never in the `.tex`: `tools/_ch5_style.py` (the shared `bounded`,
`mttc_unreported`, `mttc_dash_decode`), `tools/ch5_sweep_figures.py`,
`tools/ch5_unopposed_figures.py`, `tools/ch5_disruption_figure.py`.

| # | Float | Rule | Was | Now |
|---|---|---|---|---|
| A1 | Table 5.4; F.2; F.3; F.4 | P2 | ASP reduction 1.00 where one or two runs still reach a target: random 200 s (1 of 4 000), host topology shuffle 500 s (1 of 4 000), host layer mean 500 s, the baseline attacker's service diversity 200 s (2 of 1 000); ASP 0.00 for random and alternative, and the baseline's service diversity | `>0.99`; ASP `<0.01`; each caption decodes it. 1.00 and 0.00 now mean exactly that |
| A2 | Table 5.4; F.3; F.4 | N1 | MTTC "3 000" for random (over **1** run) and alternative (**2** runs), shown as three times faster than no MTD; the baseline's service diversity "10 000" over 2 runs; F.3 printed "3 279 ± 0" and "3 473 ± 4 314" | a dash: "fewer than 10 runs compromise a target host" |
| A3 | Table 5.4; F.3; F.4 | S1–S3 | one dash meant both "no MTD has no rank or reduction" and "MTTC undefined" | the reference's rank and reductions are blank (not applicable); the dash means only "MTTC not reported", with its reason |
| A4 | F.3; F.4 | P1 | NCR "0.17 ± 0.00" (a zero half-width printed); MTTC unrounded "10 692 ± 304" | NCR "0.171 ± 0.003", "0.007 ± <0.001"; MTTC "10 700 ± 300" |
| A5 | Table 5.4 | P1 | MTTC column rounded to thousands because its widest interval was alternative's 2-run ±4 314 | hundreds (the widest *reported* interval, ±1 100): no MTD 10 700 s, IP shuffle (baseline) 7 500 s |
| A6 | Figure 5.3 caption | F5, P2 | "an ASP reduction of 1 with no whisker is an MTD under which no run compromises a target host": false for random at 200 s and host topology shuffle at 500 s, whose whiskers are too short to see | "a point at 1 is an ASP reduction of 1, no run compromising a target host, or one above 0.99, which Table F.2 tells apart" (session-worded; DRAFT STATE) |
| A7 | Figure 5.3 panel titles | T3, F4 | "by the layer they **rewrite**"; captions and Table 2.4 say "reconfigures" | "by the layer they reconfigure" |
| A8 | Table 5.2 caption | I1 | "a 95 % interval" (method unnamed) | "a 95 % interval on the mean (normal approximation)" |
| A9 | four generators' headers | provenance | "GENERATED ... from numbers.json" while reading `numbers_reported.json` | the path read from the generator's own `NUMBERS` |
| A10 | F.3; F.4 | T4 | negative brackets and `>0.99 [0.99, 1.00]` wrapped onto two lines | columns widened; `{>}`/`{<}` set without relation spacing; no cell wraps |

Build (pdflatex ×2 + bibtex, scratch output dir): 0 errors, 0 undefined
references, overfull boxes 13 (15 before).

**Commit state.** `tools/_ch5_style.py`, this session's hunks of the three
generators and the Figure 5.3 caption clause are committed (staged hunk by hunk;
a parallel session's uncommitted edits in the same files were left unstaged). The
regenerated `.tex`/`.pdf` floats sit uncommitted in the working tree, because
they also carry that session's uncommitted table style (`\grouprow`, stripes);
they go in with that work (the same arrangement as commit 1882c08f). Rerunning
the three generators reproduces them.

---

## B. Proposed (each needs Marc's ruling; nothing applied)

Ordered by examiner risk. "Content point" items are prose: Marc dictates them.

**B1. A §5.3.2 sentence is false at 1 000 seeds, and has no `\prelim` mark** (so
the 1 000-seed swap will not catch it). *Rule: data, not presentation.*
> "Against the APT attacker model no run compromises a target host up to 500 s
> under the host layer and the random deployment strategy, and up to 200 s under
> the alternative deployment strategy."

At 1 000 seeds (runs reaching a target, of 4 000): host layer none up to 200 s
(IP shuffle 2 at 500 s, host topology shuffle 1, complete topology shuffle 0);
random none up to 100 s (1 at 200 s, 32 at 500 s); alternative none up to 100 s
(2 at 200 s). The same paragraph's "−0.22" (baseline host layer at 500 s) is now
−0.12, and is typed with a hyphen (B2). **Recommend:** Marc re-dictates the
sentence from these facts; "no run" only where the table prints 1.00.

**B2. Hyphens for minus signs in §5.3 prose** ("-0.22", "-0.03", "-0.19 to 0.05").
*P3.* **Recommend:** `$-0.22$` in each; a mechanical swap, offered for approval.

**B3. Attack actions blocked is the same for every mechanism of a layer, by
construction: the reader is not told.** *T1, F5; Marc's own reading, 2026-10-02*
("it just reads like all of the mechanisms have the same effectiveness").
Table 5.3 and Figure 5.2(a): 0.35–0.39 for every host-layer mechanism, 0.15 for
every service-layer one, 1.00 / 0.95 for the baseline attacker. The simulator
decides a disruption by the deployment's **layer** and the attacker's current
action, never by the mechanism (`mtdnetwork/operation/mtd_operation.py`
`_interrupt_adversary`; Section 2.2 already states the rule, Brown 2023). So
panel (a) measures *how often the attacker is mid-action on that layer*, not how
effective a mechanism is. **Recommend:** one caption clause on Figure 5.2 and
Table 5.3, "a deployment's layer, not its mechanism, decides which attack actions
it disrupts (Section 2.2), so the mechanisms of one layer block the same share",
and the same point as a content point for the §5.3.1 prose.

**B4. Negative time lost is not decoded.** *T2.* Table 5.3 and Figure 5.2(b) print
−60 to −10 s; neither caption says what below zero means. **Recommend:** caption
clause "below zero: the next compromise came sooner than on the same seed with no
MTD" (Section 4.5.3 already allows it).

**B5. Time lost leaves out some deployments, and the share is not reported.**
*N3.* A deployment that completes after the no-MTD run has ended is dropped
(Section 4.5.3 declares the rule); the share dropped is 1–3 % for the APT attacker
model but up to 28 % for the baseline attacker (service diversity 1 548 of 5 572;
complete and host topology shuffle 21–22 %). **Recommend:** the caption gives the
range ("over the deployments with a no-MTD comparison: at least 72 % of each
cell's"), or an Appendix F column.

**B6. One interval method, three names.** *I2.* "95 % bootstrap intervals over
runs" (Table 5.3, Figures 5.1–5.2), "95 % percentile bootstrap interval" (Tables
5.4, F.1–F.4, Figure 5.3), "a 95 % interval on the mean (normal approximation)"
(Tables 5.2, F.3–F.4). **Recommend:** two names only, "95 % percentile bootstrap
interval over runs" and "95 % interval on the mean (normal approximation)",
generated from one constant in `_ch5_style.py`.

**B7. ASP has a Wald interval (Table 5.2) or none (Tables F.3–F.4).** *N4, I1.* At
ASP 0.04 over 1 000 runs the Wald interval is adequate, but the NCHS proportions
standard rejects it near 0 and 1, and F.3–F.4 give every other column an interval.
**Recommend:** Clopper–Pearson 95 % intervals for ASP in all three tables; an
analysis change in the readers, then regenerate.

**B8. ASP reduction saturates against the APT attacker model, and the text does
not say so.** *R2; Marc's question, 2026-10-02.* Its ASP with no MTD is 0.09, so
five MTDs reach ≥ 0.99 at 200 s and the column stops separating them; NCR
reduction (0.75–0.96) still does, which is why Table 5.4 ranks on it. **Content
point for §5.3.2:** "ASP reduction reaches its ceiling of 1 for five MTDs against
the APT attacker model, whose ASP with no MTD is 0.09; NCR reduction separates
them."

**B9. Figure 5.1(a): the dash means "not applicable", and the colour scale is not
decoded.** *S1, S3, S4.* "A dash marks a tactic the attacker does not have" is
the not-applicable case, which S1 gives a blank cell; and the fill darkens with
the share, which the caption does not say (the printed values carry the reading,
so the risk is low). **Recommend:** a blank, unfilled cell, decoded "a blank cell:
a tactic the attacker does not have", and "darker is a larger share".

**B10. Table 5.1's Metrics row says "attack actions blocked".** *T3.* Table 4.3
and every chapter 5 float say "attack actions blocked per MTD deployment".
**Recommend:** the full name (Table 5.1 is hand-set).

**B11. Chapter 4 does not declare the MTTC reporting threshold.** *N1, S2.* Every
caption now says "fewer than 10 runs", but §4.5.2 says only that MTTC is undefined
where no run compromises a target host. **Content point for §4.5.2 (Marc
dictates):** MTTC is not reported where fewer than 10 runs compromise a target host
or its 95 % interval is wider than 160 % of its value, after the NCHS standard for
rates (Kochanek et al. 2024). Needs a bib entry (NCHS 2024 report; URL in the
extraction).

**B12. Figure 5.3's NCR and ASP rows use different y ranges (−0.4 to 1, −1 to 1)
without saying so.** *F2.* Low risk (different metrics). **Recommend:** a caption
clause "the ASP rows' axis runs to −1".

**B13. FLOATS.md describes Figure 5.2 as its 2026-09-24 form** (NCR growth-rate
panels from `disruption_numbers.json`) and Table 5.2 as reading `numbers.json`.
*Provenance.* FLOATS.md is dirty in a parallel session; flag only.

**Out of scope, flagged for the §5.4 pass.** Table 5.5 (`tab:ablation`) prints
"---" for the no-MTD row's NCR reduction (S1: blank); Cohen's d is "below 0.2" with
the threshold attributed to Cohen, which Lakens 2013 calls a benchmark of last
resort (I4; the 2026-09-30 comment already avoids putting "negligible" in Cohen's
mouth); the no-MTD rows' NCR differs between the two blocks (0.169 / 0.167).

---

## Validation gate

- Every B item ruled (taken, amended or declined), and each taken one applied in
  its generator or dictated into the prose.
- Rebuild clean; every in-scope float rendered and re-read against the standard's
  audit procedure.
- `grep -n '\$1\.00\$' docs/thesis/tables/tab_5-*.tex tab_F-[0-4]*.tex` hits only
  cells whose value is exactly 1.
- Then this ledger is deleted, and §5.4 is audited against the same standard.

## Reading list

1. `docs/workflows/results_presentation_standard.md`
2. `docs/sources/extractions/results_presentation_conventions.md` (Parts A, C)
3. `tools/_ch5_style.py` (the shared reporting rules, end of file)
4. `docs/workflows/figure_table_conventions.md` §b, §k, "Precision and table size"
