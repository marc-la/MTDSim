---
status: open (for Marc's review)
created: 2026-10-14
branch: worktree-agent-a113d8ce74ff65816 (from feat/ch6-redraft at 15aa897e)
---

# Appendix float design pass (2026-10-14)

**Brief (Marc):** each appendix table and figure should show the reader, at a glance, the numbers it exists for, using conventional devices only. D.7 had "a lot of bolding going on"; D.11 is the model (reference row first, group labels that say what changed, bold with one meaning tied to the claim, a caption that decodes only).

**Method, per float:** the body claim(s) it backs, from every `\ref` to it and to its section; the cells those claims need; what the eye lands on now; then a redesign or a reason to leave it. Every change is made in the generator and regenerated; the build was rendered and read after each change. Rules applied: `results_presentation_standard.md` S3/S4, `figure_table_conventions.md` §k, `appendix_conventions.md`.

**Outcome:** three tables changed (D.7, D.6, C.4) and one appendix lead sentence. Sixteen floats were reviewed and left as they are, each for the reason given below. Body generated floats are byte-identical: `tab_5-4a_ablation.tex` comes from the same generator as D.7, and `git diff 15aa897e` lists only the files named here.

Page numbers below are printed pages.

---

## Appendix B

### B.1 `tab:clause-tests` (inline), p. 57: **left**
- **Job:** it gives the predicates behind each mark of Tables 3.3 and 6.1 (ch3 3198; Table 6.1's caption). The reader looks up a mark and finds the predicate cell that set it.
- **Why left:** the marks sit on each property's row, the predicate cells sit under them, and shading is by property. Marc ruled all three on 2026-10-13 (handoff §13). The cells hold words (yes, rule, assumed, no), so no bold or grey meaning would make the look-up easier.

## Appendix C

### C.1 `fig:app-technique-core` (`gap_appendix_figures.py`), p. 59: **left**
- **Job:** it backs ch4 4031: most technique edges come from one attack flow (419 of 478) and only 47 of 122 tactic edges do. The figure draws the 55 edges that two or more flows share.
- **Why left:** the sparsity shows at a glance. The end-mark option was weighed and rejected on 2026-10-13.

### C.1 `tab:profile-sources` (`gasp_structural_baseline.py --tex`), p. 60: **left**
- **Job:** it backs ch4 4177 and ch6 9132: the sources behind each answer. The three attack flows we decided ourselves are named in the prose, by ruling.
- **Why left:** it is a look-up table with no claim cells. Five long flow names wrap. Widening the name columns into the 0.75 cm that is left would fix only the two Turla rows, and the two-up layout was ruled on 2026-10-13.

### C.2 `fig:profile-edges` (`ch4_attack_profiles_figure.py`), p. 61: **left**
- **Job:** it backs ch4 4225 (profiles that reach the same tactics move between them differently) and the lead's Muddy Water edge.
- **Why left:** the grids, the diagonal (2026-10-13) and the outlined Exfiltration and Impact columns carry the claim. Lifecycle separators were already declined. The generator also writes body Figure 4.2, so it was not run.

### C.2 `tab:attack-action-times` (`attack_action_times_table.py`), p. 62: **left**
- **Job:** it backs ch6 9068 (an attack action takes the tactic's mean duration, not MTDSim's time) and the lead's "six tactics take an attack action's time".
- **Why left:** the two times sit in adjacent columns, one row per tactic. Marc ruled this flat design on 2026-10-14 ("looks tacky"). Bolding the differing rows would mark six of the eight mapped rows.

### C.3 `tab:overlay-failure-rules` (`failure_weight_decomposition_figure.py`), p. 63: **left**
- **Job:** it backs ch4 5129: the rules and the distance factor set all 210 factors.
- **Why left:** it is a decision table, revised twice with Marc on 2026-10-14. The Value column is the answer and is already right-aligned beside the conditions.

### C.4 `tab:value-bases` (`value_bases_table.py`), p. 63: **changed**
- **Job:** it backs ch6 `thr:values` 9092: which values are our judgement. That group comes first, by ruling.
- **Change:** the columns are widened to the text width (3.0 / 10.0 / 1.95 cm, from 3.0 / 8.0 / 2.6). "Mean durations from MTDSim's scan and exploit attack actions" no longer wraps (standard T4), and the table is one line shorter. There is no overfull box; an intermediate 1.75 cm Reason column caused one, which was fixed.

## Appendix D

### D.1 `tab:mtdshield-configuration` (inline), p. 64: **left**
- **Job:** it backs ch6 9216: MTDShield runs outside its training conditions.
- **Why left:** every row is a setting that differs between training and Chapter 5. The table was cut to exactly those rows on 2026-10-14.

### D.2 `tab:disruption` (`ch5_disruption_figure.py`), p. 65: **left; one precision flag**
- **Job:** it holds Figure 5.2's values with their intervals (ch5 §5.3.1).
- **Why left:** it is the look-up table behind a body figure. Every cell is a value the body prose reads, so no subset needs marking.
- **Flag (open question 1):** the baseline attacker's time lost under host topology shuffle prints [−30, 0]. Its true upper bound is −0.23, so the interval excludes zero, but the printed interval reads as if it includes it. The generator goes one place finer only once (P1), and here a bound still rounds to 0 after that step. Not changed.

### D.3 `tab:eff-interval-values`, D.4 `tab:rank-one-intervals`, Figure D.1 `fig:eff-cross-arm-asp`, D.5 `tab:eff-interval-values-asp` (`ch5_sweep_figures.py`), pp. 65–67: **left**
- **Jobs:**
  - D.3 backs ch6 8988 (service diversity: 0.50 at 50 and 100 s against the APT attacker model, 0.54 at 1 000 s against the baseline attacker) and ch6 9137–9143 (the layer order per attacker per interval).
  - D.4 backs ch5 7787 and ch6 8913 (rank 1 holds only host-layer mechanisms against the APT attacker model, and only service-layer ones against the baseline attacker).
  - Figure D.1 and D.5 back ch6 9078 (the layer order holds on ASP reduction).
- **Why left:** the rows are grouped by layer, with italic layer-mean rows, so the layer order reads down each column. Grey carries S3 (the interval includes zero). Marc ruled grey kept, and the NCR and ASP tables not combined, on 2026-10-14.
- **Bold considered and declined.** Marking rank 1 in D.3 would duplicate D.4, the float Marc kept for rank 1 (appendix conventions, "one float per fact"). The generator also writes body floats, so it was not run.

### D.6 `tab:ablation-attack-profiles` (`partition_ablation.py`, `TABLE_ONLY=1`), p. 67: **changed**
- **Job:** it backs ch5 8219: under MTD, the effect of the attack profiles is not negligible in 29 of 60 configurations, negligible in 7 and inconclusive in 24.
- **Diagnosis:** bold (29 cells) is the count the body cites. The rows ran in a different order from every other Appendix D table: user shuffle sat between port shuffle and OS diversity, and there were no group labels. The bold therefore read as scattered cells, not as the pattern it is.
- **Change:** the rows are grouped and ordered as in Table D.3, under italic group rows: host layer, service layer, credentials, deployment strategies. The bold now reads as one block, the host layer plus the random and alternative strategies.
- **Unchanged:** the values, the marks and the caption ("Bold: not negligible").
- **See open question 2:** the table cannot show which plain cells are negligible (7) and which are inconclusive (24).

### D.7 `tab:ablation-random-partitions` (`ablation_table.py`, `control_table`), p. 68: **changed (named by Marc)**
- **Job:** it backs ch5 8263:
  1. With no MTD, the attack profiles beat every random partition by a not-negligible *d* of 0.25 to 1.47.
  2. Under IP shuffle and OS diversity, the effect is not negligible against six to ten of the ten partitions in each configuration, in the attack profiles' favour except against two partitions under IP shuffle at 200 s.
- **Diagnosis:** 45 of the 50 cells were bold, so bold drew the eye to nothing. The rows ran in arbitrary partition order. The count the body cites ("six to ten") had to be found by counting bold.
- **Changes:**
  - **Row order:** falling *d* with no MTD, so the 1.47 and the 0.25 are the first and last rows. Partitions keep their numbers.
  - **Count row:** "Not negligible (of 10)", set off by a rule, giving 10, 6, 10, 9 and 10. This is the body's "six to ten".
  - **Bold:** marks only the two cells the body names as exceptions, partitions 6 and 5 under IP shuffle at 200 s (−1.03 and −0.48), decoded as "Bold: not negligible, in the random partition's favour".
  - **Caption:** it now names the cells that are not "not negligible", generated from the verdicts: "Negligible: partitions 3, 8, 9 and 10 under IP shuffle at 200 s; inconclusive: partition 9 under OS diversity at 200 s; every other *d* is not negligible (Section 5.1)". Every cell's verdict stays decoded. The caption also gains "in falling order of *d* with no MTD".
- **Appendix lead edited.** D.4's lead (dissertation.tex, about line 10055) said "bold marks a *d* that is not negligible" for all three tables, which is no longer true of D.7. It now reads "Every *d* is on NCR (Section 5.1), on the same 1 000 seeds, with the APT attacker model averaged over *c*₁ to *c*₄". Each caption decodes its own bold (S4); D.8 has none.
- **Body Table 5.4** (`tab_5-4a_ablation.tex`, same generator) is byte-identical.

### D.8 `tab:ablation-memory` (`memory_ablation.py`), p. 68: **left**
- **Job:** it backs ch5 8439 and 8457.
  - With no MTD at 20 services per OS, exploits succeed 0.73 with the memory and 0.69 without.
  - At one service per OS, they succeed 0.92 with it and 0.69 without, and the effect on NCR is still negligible.
- **Why left:** the two cited rows are the last and first of the no-MTD block. The with and without columns sit side by side, and the *d* intervals are printed; all of them lie inside ±0.2. Nothing is marked, so nothing needs decoding. The MTD blocks back the generality of "still negligible", so none was cut.

### D.9 `tab:anchor-sensitivity` (`ch5_s51_sensitivity/analyse.py`), p. 69: **left**
- **Job:** it backs ch6 9097 and D.5's prose: only the 45 s mean duration moves NCR much.
- **Why left:** bold falls on the largest change in each column group (−0.208 and −0.144), which is exactly the claim. The rows are in rising order of duration. Ruled on 2026-10-14.

### D.10 `tab:duration-ranking` (`duration_ranking_table.py`), p. 69: **left**
- **Job:** it backs ch6 9060 and D.5's prose. At both ends of the band, the host layer stays above the service layer, rank 1 shares no mechanism with the baseline attacker's, and ρ stays near 0.
- **Why left:** the rows are in declared rank order with a Group column, bold marks rank 1, and the ρ row is set off by a rule. At 110 dpi the bold "1"s look like plain type, but a 200 dpi render confirms they are bold.

### D.11 `tab:fa-tactic-durations` (`further_analyses_tables.py`), p. 70: **left (the model)**
- **Job:** it backs ch6 8555 to 8627 and 9574, the two-step ablation.
- **Why left:** it is Marc's reference design.

---

## Final state

- **Pages:** 86, unchanged. The page map is unchanged: A p51–56, B p57, C p58–63, D p64–70. No float moved off its section's pages.
- **Undefined references:** 1, `app:detector-memory` in ch4, which is pending and was left alone.
- **Overfull boxes:** 62, as at the start; the changes added none.

## Proposals for chapters 1–5 and 7

None. No body sentence describes an appendix float's bold or ordering. Every body number the changed tables carry (0.25 to 1.47; six to ten; the two exceptions; 29 of 60) still reads off the table.

## Open questions for Marc

1. **D.2 precision (P1).** The baseline attacker's time lost under host topology shuffle prints [−30, 0], but its upper bound is −0.23, so the interval excludes zero.
   - **Proposed fix:** loop the "one place finer" step until no bound rounds to 0. The baseline time-lost column would then print to tenths, for example −14.7 [−29.9, −0.2], and service diversity would print 492.5 [468.6, 515.6] where the body has 493.
   - Not applied, because it changes how a ratified rule is read and how a body-cited number is printed.
2. **D.6 verdicts.** The body cites "negligible in seven and inconclusive in 24 (Table D.6)", but plain cells do not tell the two apart.
   - **Option:** name the seven negligible cells in the caption, as D.7 now does: MTDShield at every deployment interval but 200 s, and service diversity at 1 000 and 2 000 s.
   - Not applied, given the 2026-10-14 ruling that cut the counts from this caption.
3. **Bold in two adjacent tables.** In D.6, bold means "not negligible". In D.7 it means "not negligible, in the random partition's favour", which is a subset of that. Each caption decodes its own (S3 is per float). Confirm that the difference reads clearly on the facing pages.
4. **Stripe overhang, document-wide.** `\rowcolors` paints `\tabcolsep` past `@{}` table edges, so stripes stick out beyond the rules on both sides of most striped tables, body ones included. D.10 uses a per-table workaround. A preamble fix would change the body tables, so it is out of this pass's scope.
5. **C.1 wraps.** Five long attack-flow names wrap in the two-up layout. A fix would need a different layout, not wider columns.
