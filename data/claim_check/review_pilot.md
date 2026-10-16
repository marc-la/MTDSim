# Pilot review sheet: statistics and metric sources (wave 1)

2026-10-16. Nine sources, 15 units, 16 unit–source pairs. Verifier A and adversarial verifier B worked independently, one source per pass. All 56 quotes were found verbatim in their own source by `tools/claim_quote_check.py`, and the reported PDF pages match each agent's own locator. The session re-read the three passages behind rows 1–3 against the source text before writing this sheet. Verdict files are in `verdicts/pilot/`.

Mark each row `ok`, `fix` (as proposed), `fix-other`, or `look`.

## On the sheet

| # | Unit (tex) | Sentence (short) | What the source says | A / B | Proposed fix | Mark |
|---|---|---|---|---|---|---|
| 1 | U0613 (l. 6251) | "negligible when its interval lies wholly inside ±0.2 … inconclusive when it crosses ±0.2 [Lakens]" | The interval rules are Lakens's equivalence and minimal-effects tests (pp. 260–261). But Lakens gives no ±0.2 bound and warns against benchmark bounds: "Relying on a benchmark is the weakest possible justification" (p. 262, printed). His "inconclusive" means neither different from zero nor equivalent, and he uses a 90 % interval for the equivalence test | A: placement, minor. B: contradicted, **major** | Move the citation onto the interval rule only, and say plainly that ±0.2 is our choice, on the basis the dissertation already gives (a minimal edit). Optional: one clause owning the 95 % interval | |
| 2 | U0606 (l. 6212) | "Effect size is Cohen's d with the pooled standard deviation, negligible within ±0.2 [Cohen]" | Cohen has no saved text. Tantithamthavorn, cited one sentence later, writes the label as "provided in Cohen [17], i.e., \|d\| < 0.2 'negligible'" (p. 9). So the word "negligible" may be Tantithamthavorn's reading of Cohen; from memory, Cohen calls 0.2 "small", which Marc should confirm | not checkable | **Marc to look in Cohen.** If "negligible" is not Cohen's word, cite both: `[cohen1988statistical, tantithamthavorn2017empirical]` | |
| 3 | U0602 + method | 1 000 runs "the number recommended for randomised algorithms [Arcuri]" | Arcuri says "at least n = 1000" (p. 244, printed), as a rule of thumb. Separately, the same paper explains why the d family "should not be used when analysing randomized algorithms" and recommends Vargha–Delaney Â12 (p. 234 ff.). The dissertation cites Arcuri in the section that adopts Cohen's d | A and B: partial, minor; the d point is from B | "the minimum recommended". The d-versus-Arcuri point is a **method exposure, not a citation defect**: rule on whether §6.5 owns it in one line | |
| 4 | U0571 (l. 5622) | "a difference of restricted means [Royston, Eq. 1]" | Eq. 1 defines one restricted mean; the difference is the unnumbered display after it (p. 3) | both: fix locator | `[royston2013, p. 3]` or keep Eq. 1 and say "after" | |
| 5 | U0519, U0513 (Table 4.3) | NCR reduction `[alavizadeh2022]`; attack confidentiality `[zaffarano2015]` | Both metrics are adapted: NCR in place of annual loss expectancy, and an IDS in place of plaintext exposure. The table's own convention elsewhere is "this dissertation, after […]" | A: one. B: both | "after [x]" on both cells, matching the table | |
| 6 | U0548 (l. 5479) | attack confidentiality as an IDS-flag share [Zaffarano] | Zaffarano counts tasks "exposed" (visible in plaintext traffic) to unspecified "detection mechanisms", and uses the metric as an MTD-effectiveness measure | both: partial, minor | `keep` if the adaptation is said once (row 5 does it); otherwise one clause | |
| 7 | U0607 + `sk_esd.py` | Scott–Knott ESD [Tantithamthavorn] | The cited test log-transforms with ln(x+1) before ranking (Sect. 5.8.1). The implementation omits that step, because NCR reduction can be negative | both noted | Say once that the log-transform step is omitted and why, or check that no ranking changes with it | |

## Skim list (one verifier, minor)

- **U0605, Clopper–Pearson.** The limits assume one binomial p. Check that an ASP averaged over c1 to c4 is computed as one pooled proportion (B).
- **U0549, Jung.** Snort counts distinct addresses, and the implemented rule counts attack actions. The next sentence, U0550, already says "the attacker's fifth attack action … on any target" (B). Likely `keep`.
- **U0215 and U0216, Table 3.1.** Alavizadeh files the mitigation factor under economic metrics and attack cost under effectiveness. The table's Efficiency row is Cho's frame, not Alavizadeh's. Likely `keep` (B).
- **U0609, Spearman.** The paper's own coefficient is R, not ρ. Citing Spearman 1904 for ρ is the convention, so `keep` (B).

## Cleared (A and B both SUPPORTED, quotes found)

U0596 (Arcuri, Table 5.1), U0565 (Alavizadeh Eq. 13), U0521 (Royston, "after"), and U1163 (the caption's Spearman, covered by U0609).
