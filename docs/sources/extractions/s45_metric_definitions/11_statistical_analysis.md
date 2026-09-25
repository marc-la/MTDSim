# 4.5.4 Statistical analysis — drafting agent 11 (2026-09-25)

## LaTeX

Variant A, which describes what the code computes today. Variant B, the one I recommend, follows it and needs a code change first. Keys marked † are not in `references.bib` yet (see Open).

```latex
\subsection{Statistical analysis}
\label{subsec:metrics-statistics}

The metrics above are read from runs; this subsection states how the runs are
counted, combined and compared. Every combination in Table~\ref{tab:experiment}
runs on the same 1\,000 seeds, the number of runs \citet{arcuri2014hitchhiker}
recommend for evaluating a randomised algorithm, and a seed fixes the network. A
mean carries a 95\,\% interval from the normal approximation over runs,
$\bar{x} \pm 1.96\,s/\sqrt{n}$. NCR reduction, a ratio of two means, carries a
95\,\% percentile bootstrap interval from 2\,000 resamples
\citep{efron1994introduction}, with the defended and no-defence runs resampled
independently; time lost per MTD deployment resamples each run with the
no-defence run on its seed.

Defences are ranked, per attacker and deployment interval, by the Scott--Knott
effect size difference (ESD) test \citep{tantithamthavorn2017empirical}. Within
one attacker every NCR reduction divides by the same no-defence mean, so the test
ranks mean hosts compromised per seed, the APT attacker model's four attack
profiles averaged at each seed. The test sorts the defences' means and splits
them where the between-groups sum of squares is largest, if the likelihood-ratio
test of \citet{scott1974cluster} is significant at $\alpha = 0.05$, and repeats
on each part. It then merges adjacent groups whose standardised difference in
means, Cohen's effect size \citep{cohen1988statistical}, is below 0.2. Defences
in one group share a rank, numbered densely from~1 for the fewest hosts
compromised; no defence, the reference, is not ranked. The groups cannot overlap,
so no chain of pairwise tests is needed, and the merge does not depend on the
number of runs.

We keep the significance step of \citet{tantithamthavorn2017empirical}, which
version~2.0 of the test drops \citep{tantithamthavorn2019impact}, and omit their
log transform, because the ranked quantity is the mean the metric is built on.
The test pools the defences' unequal variances, so each grouping is checked
against all-pairs Welch $t$-tests with Holm's correction
\citep{welch1947generalization, holm1979simple}; ignoring the seeds the defences
share is conservative. No MTD evaluation in the lineage tests a ranking;
\citet{alavizadeh2022} mark the best value per metric. The two attackers'
rankings are compared at each deployment interval by Spearman's $\rho$ between
their NCR reductions.
```

† `efron1994introduction`, `tantithamthavorn2019impact`, `welch1947generalization`, `holm1979simple`.

**Variant B (recommended once the code resamples by seed).** Replace paragraph 1's last three sentences, and paragraph 2's per-seed clause, with the text below:

```latex
... and a seed fixes the network, so the seed is the unit of analysis: where the
APT attacker model's four attack profiles are pooled, their runs at one seed are
averaged into one value. A mean carries a 95\,\% interval from the normal
approximation over seeds, $\bar{x} \pm 1.96\,s/\sqrt{n}$. NCR reduction, a ratio
of two means, carries a 95\,\% percentile bootstrap interval from 2\,000
resamples of the seeds \citep{efron1994introduction}, so each seed's defended and
no-defence runs stay together; time lost per MTD deployment is resampled the
same way.
% paragraph 2, sentence 2 becomes:
Within one attacker every NCR reduction divides by the same no-defence mean, so
the test ranks mean hosts compromised per seed.
```

**Word count:** Variant A is about 336 words of prose (99 / 144 / 93 by paragraph). Variant B is about 345.

## Structure

**Slots used.** The S1–S6 template is for a single metric, so it does not apply here. The subsection follows the handoff's content points in this order:
1. opener, saying why the subsection stands apart;
2. the run count and the unit;
3. the intervals, per statistic;
4. the ranking: its quantity, its two steps, the rank convention, and why this test;
5. deviations and assumptions;
6. beyond the lineage;
7. ρ.

**Merged or dropped.**
- **The per-metric tagging table** ("which statistic applies to which metric") is folded into the sentences on means, NCR reduction and time lost. The shares (relative tactic occurrence, APV, attack confidentiality) carry no interval and have no float that shows one, so they get no sentence.
- **Dropped: "middle ranks are indicative (d near 0.2)".** It does not reproduce on the per-seed data (see Verification, F4).
- **Dropped: "clean groups forced on a continuum".** It is a concession for ch6 threats, and cutting it keeps the subsection in budget.
- **Arcuri's "at least" softened to "the number of runs … recommend".** The thesis declares 1 000, so "at least" adds nothing.

**Length.** The budget is 200–320 words. Variant A is about 336, about 5 % over. The next cut, if needed, is the lineage sentence (14 words); it could move to §5.3.2's text.

**Marc's question: what "Statistical analysis" means, and why it is apart from the three classes.**
- **A metric is a quantity defined on a run.** Examples: hosts compromised at the end, time to the first compromise, the share of actions below the alarm. The three classes sort metrics by the question they answer about the attacker.
- **Statistical analysis is how the per-run values of many runs become the numbers chapter 5 prints, and how conditions are compared.** It covers how many runs there are, what the independent unit is, what uncertainty each number carries, and the test that decides which defences differ.
- **It answers no question about the attacker.** It answers "how sure are we, and which differences are real". It applies across all three classes, so it cannot sit inside any one of them.
- **Tantithamthavorn et al. 2017 draw the same line.** They put §5.6 *Performance Measurement* (the metrics) apart from §5.8 *Ranking and Clustering* (Scott–Knott ESD). Ho 2024 splits §3.4.1 *Results collection pipeline* (how trials are aggregated: "The mean of the checkpoints … overall results … taken by the median of the trials") from §3.4.2 *Evaluation metrics calculation*.

**Heading.**
- **The corpus has no dedicated heading for this.**
  - Ho uses *Results collection pipeline* under *Evaluation Method*.
  - Barach puts the paragraph at the end of §4 *Experiment Setup* (p. 12), with no subhead.
  - Zhang puts it in §5 *Evaluation*'s opening paragraph.
  - Tantithamthavorn uses *Ranking and Clustering* for the ranking only.
- **Options:**
  - (a) *Statistical analysis*: plain, states the topic, and the usual name in empirical-software-engineering and clinical reporting (I have not verified that last point against a source);
  - (b) *Statistical methods*: the same meaning, slightly more formal;
  - (c) *Aggregation and comparison of runs*: descriptive, but invented;
  - (d) no subsection, with the run count and intervals moved into §5.1 as Barach and Zhang do.
- **Recommendation: keep (a).** It follows voice.md's heading rule (it states what the section is on), and Marc ruled that the method is accountable for the ranking (§8j-4), which rules out (d).

## Verification

| # | Claim | Source, locator | Verbatim quote | Verdict |
|---|---|---|---|---|
| 1 | 1 000 runs is the recommended count | Arcuri & Briand, Simula Tech. Report 2011-13 (preprint of STVR 2014), p. 22, §11 Practical Guidelines (read: `web-backend.simula.no/.../Simula.simula.670.pdf`) | "On each artifact in the case study, run each randomized algorithm at least n = 1, 000 times." | **partly.** (i) Read in the TR, not in the STVR version (the ORBilu author copy timed out twice), so the STVR page and wording still need checking. (ii) Their count is per artifact. Here each seed is a new network, so one run per network, and their next bullet trades runs per artifact for more artifacts ("at least n = 10"). The draft's wording, "recommend for evaluating a randomised algorithm", is within this. (iii) The same guideline recommends Mann–Whitney U and Vargha–Delaney Â12, which this analysis does not use; an examiner may note this. |
| 2 | Tantithamthavorn 2017 pairs Scott–Knott ESD with 1 000 repetitions, citing Arcuri | Tantithamthavorn et al. 2017 author copy (`rebels.cs.uwaterloo.ca/papers/tse2017_tantithamthavorn.pdf`), §9.1 | "To ensure that the results are robust, we repeat the experiment 1,000 times, as suggested by Arcuri et al. [3]." | holds (precedent, not cited in the draft) |
| 3 | Step 1: Scott–Knott splits sorted means into distinct groups at α = 0.05 | Tantithamthavorn 2017, §5.8.1 | "The Scott-Knott test [90] uses hierarchical cluster analysis to partition the set of treatment means into statistically distinct groups (α = 0.05)." ([90] = Scott & Knott 1974, Biometrics 30(3) 507–512) | holds (secondary). The primary (JSTOR) has not been read. |
| 4 | Step 2: adjacent groups with negligible effect are merged | Tantithamthavorn 2017, §5.8.1 | "merge any two statistically distinct groups that have a negligible effect size into one group." | holds |
| 5 | The threshold is \|d\| < 0.2, and d is the difference in means over the SD | Tantithamthavorn 2017, §5.8.1, Eq. 5 | "Cohen's delta (d) [16], which is the difference between two means divided by the standard deviation of the data … thresholds provided in Cohen [17], i.e. \|d\|< 0.2 "negligible"" | holds. Note that [16] is Cohen 1988 (d) and [17] is Cohen 1992 *A power primer* (the thresholds). The bib has only 1988. |
| 6 | The 2017 test includes a log transform, which this analysis omits | Tantithamthavorn 2017, §5.8.1 "Normality correction" | "we mitigate the skewness by log-transforming each treatment (ln(x+1))" | holds. The draft names the omission. |
| 7 | Version 2.0 drops the significance test | Tantithamthavorn et al. 2019, TSE 45(7) 683–711 (arXiv 1801.10270), §5.5.3 | "Instead of using a likelihood ratio test and a χ2 distribution as a splitting and merging criterion … we analyze the magnitude of the difference"; "Unlike the earlier version of the Scott-Knott ESD test [141] that post-processes the groups that are produced by the Scott-Knott test" ([141] = the 2017 paper) | holds. The source says "v2.0"; the handoff says "2.0.3" (the CRAN release). The draft says "version 2.0". |
| 8 | Several treatments may share one rank | Tantithamthavorn 2019, §5.5.2 | "The Scott-Knott ESD test ranks each variable exactly once, but several variables may appear within one rank." | holds (supports shared ranks; the dense numbering is ours) |
| 9 | No MTD evaluation in the lineage tests a ranking | `docs/sources/lit_review/alavizadeh2022.md` l.637, 651–652 (Tables 4–5); `zhang2023.md` l.493 (Fig. 14); grep of all 43 `lit_review/*.md` files for Scott-Knott / ANOVA / t-test / Wilcoxon / Mann-Whitney / Kruskal / Friedman / Nemenyi | Alavizadeh: a "Best" row naming the best VM per metric. Zhang: "a Max Count value of 5 indicates that there are five MTD combinations achieving the best results". The grep's only hit is Manadhata & Wing's "performed t-tests to determine the survey responses'" (l.679), which is not a ranking of defences. | holds, narrowly. Barach 2026 (outside lit_review, `tactic_profiles/.../TSP_CMC_71705.md` l.213, p. 12) runs "paired t-tests … between the proposed framework and baseline models": a test, but not a ranking. So the sentence must say "tests a ranking", not "tests a difference". |
| 10 | Heading precedent | Ho 2024 `ho2024.md` l.475–481; Barach l.179–213; Zhang `zhang2023.md` l.416–420; Tantithamthavorn 2017 §5.6, §5.8 | Ho: "## 3.4.1 Results collection pipeline … the overall results for each models will be taken by the median of the trials" | holds |
| 11 | Percentile bootstrap citation | Efron & Tibshirani, *An Introduction to the Bootstrap* (Crossref DOI 10.1201/9780429246593, Chapman & Hall/CRC) | not read (book) | to download: Marc |
| 12 | Welch 1947; Holm 1979 | Crossref: Welch, Biometrika 34(1/2), p. 28, DOI 10.2307/2332510. Holm is not on Crossref. | not read | metadata only; see Open |

**Code check** (every method term against the code; I did not re-run `analyse.py`; the checks read `summaries.pkl` only, with scripts in the scratchpad at `check11*.py`):

| Term | Code | Verdict |
|---|---|---|
| same seeds on every combination and arm | `run_corpus.py:48` `SEEDS = tuple(range(100))` shared by every job (l.338–362) | matches (1 000 at the reported run, which is the thesis's declaration) |
| a seed fixes the network | `run_corpus.py:239–243` seeds `random` and `np.random` and then builds `TimeNetwork(**GEOMETRY)`; `movement/run.py:99–103` does the same for the APT attacker model | matches (both attackers, same seed, same network) |
| normal-approximation interval, mean ± 1.96 s/√n | `measures.py:1165–1178` `mean_ci`; called through `analyse.py:311` `_iv` on `hosts_of(runs)`, i.e. per **run** | matches Variant A. **Mismatch with "the seed is the unit" (F1).** |
| percentile bootstrap, 2 000, seeded | `analyse.py:99–100` `N_BOOT = 2_000`, `RNG_SEED = 0`; `suppression` l.334–353, 2.5 %/97.5 % quantiles | matches |
| resampled independently | `analyse.py:340–341`: two separate `rng.integers` draws, per run | matches Variant A (the OPEN issue, F2) |
| time lost resampled with its no-defence pair | `disruption.py:145–161` resamples run indices and carries each run's placebo row; `N_BOOT = 2_000`, `SEED = 20260924` (l.69–70) | matches ("over runs", paired by seed) |
| ranked quantity = hosts per seed; four profiles averaged | `analyse.py:1039–1048` `per_seed_hosts`; l.1073 `sk_esd({c: per_seed_hosts(...)}, best="low")` | matches |
| rank by hosts = rank by NCR reduction | `suppression` point `1 - cond.mean()/none.mean()` (l.336), with `none` fixed per attacker (l.1062–1063, interval 0) | matches (monotone; N cancels) |
| sort; split at max between-groups SS; LR test at α = 0.05; recurse | `sk_esd.py:52–72` (`ss`, `lam = π/(2(π−2))·B0/σ̂0²`, `chi2.ppf(1−α, g/(π−2))`), a port of R ScottKnott `MaxValue` | matches (40 synthetic cases cross-checked per §8j-4, not re-checked by me) |
| merge adjacent groups with \|d\| < 0.2 | `sk_esd.py:35, 98–106` (merges the smallest first; stops at `d >= 0.2`); `cohen_d` l.38–46 uses the pooled SD | matches |
| dense ranks, 1 = fewest hosts | `sk_esd.py:108`; `best == "low"` negates (l.82–87) | matches |
| no defence not ranked | `analyse.py:76` `RANKED` = the ten defences (seven mechanisms, two schemes, MTDShield) | matches |
| one-way ANOVA pooled MSE | `sk_esd.py:93–95` | matches ("pools the defences' variances") |
| Spearman ρ between NCR reductions per interval | `analyse.py:1085–1088` `spearman_points` over the ten points; no interval here | matches. The ρ interval exists only in `rank_block` (l.779–801, 200 and 2 000 s, resampled independently). |
| Welch/Holm check | **absent from the code.** It was an examiner agent's ad hoc run. | **mismatch: not reproducible from the repo (F3)** |

**Findings from the read-only checks (100 seeds, all six intervals):**
- **F1: intervals on means ignore the clustering.** For the APT attacker model's pooled cells, the interval over 400 runs is 25–35 % narrower than over 100 per-seed means. Example: hosts under OS diversity at 200 s, ±0.38 over runs against ±0.51 over seeds. For the baseline attacker, runs and seeds coincide. So Variant A's intervals are **anti-conservative** for the pooled model, which contradicts declaring the seed as the unit.
- **F2: the independent bootstrap is mostly conservative, but not harmlessly so.** Width of the NCR reduction interval at 200 s, independent against by seed:
  - APT user shuffle: 0.169 against 0.091;
  - baseline user shuffle: [−0.187, 0.042] against [−0.132, −0.009];
  - APT IP shuffle: about equal (0.015 against 0.016).

  On baseline user shuffle, the by-seed interval excludes zero where the independent one includes it. The method choice changes a reading.
- **F3: the Welch–Holm check reproduces the groups at 200 s only in part.**
  - At 200 s, no two defences that share a rank differ, for either attacker. But 2 of 41 APT pairs in different groups are not separated (port shuffle and service diversity, each against MTDShield; Holm-adjusted p = 0.24 and 0.22).
  - At 50 s it fails the other way. 8 of 10 APT pairs and 3 of 7 baseline pairs that share a rank differ under Welch–Holm, because the pooled variance (per-seed variances up to 370:1) makes Scott–Knott under-split.
  - At 1 000 and 2 000 s many between-group pairs are not Welch–Holm-significant (up to 13 of 29). All-pairs Holm is less powerful than a hierarchical split, so part of this is expected.
  - So the handoff's line, "Welch/Holm reproduce the groups", holds at 200 s in one direction only.
- **F4: the ESD merge barely acts, and the "d near 0.2" claim fails.** The merge fires once in 12 rankings (APT at 1 000 s). The smallest standardised difference between adjacent final groups is 0.21–1.04, so "middle neighbours at 0.19–0.20" (§8j-4) does not reproduce on per-seed data. I dropped it.
- **F5: ignoring the blocking is conservative (holds).** The mean pairwise correlation of per-seed hosts across the ten defences at 200 s is 0.47 (APT) and 0.20 (baseline).
- **F6: the stored ranks reproduce exactly** for 50, 200 and 2 000 s, both attackers.

**Status check.** Every method here is adopted and cited, with two named departures (the log transform omitted, the significance step kept against v2.0). "Scott–Knott ESD" and "Cohen's effect size" are used as their sources use them. Spearman's ρ and the percentile bootstrap are standard and uncited except Efron. "No defence is not ranked" and dense ranking are our choices, both stated.

## Symbols

- **Used:** $\bar{x}$, $s$, $n$ (the sample mean, SD and count, inside the interval formula only), $\alpha$, $\rho$.
- **Collision check:**
  - `tab:gspn-notation` (dissertation.tex l.4664 block) reserves $c, \mathcal{N}_c, p, \hat p, \tau_p, t_{pq}, \mu_p, w_c, \sigma, M_0, v, F_v, \varphi, R, d, \gamma, \delta, z$.
  - An awk/grep over the live (uncommented) tex for `$s$`, `$n$`, `\bar{x}` and `\alpha` returns 0 hits. `\rho` returns 1 hit, the §4.5.4 placeholder itself.
  - **Cohen's $d$ collides with chapter 4's $d$ (the lifecycle-distance kernel).** The draft therefore writes "standardised difference in means, Cohen's effect size" and uses no symbol. $\sigma$ is taken, which is why the SD is $s$.
- **No new §4.5 shared symbols** ($r$, $\mathcal{R}$, $H_r$ are not needed here).

## For elsewhere

- **§4.5 opener:** "each is read per run, and Section 4.5.4 says how runs are combined" is consistent with this draft.
- **NCR reduction's last sentence** ("defences are ranked by it, Section 4.5.4"): consistent.
- **§5.1 Runs paragraph (tex l.6478–6481)** says "Differences are reported as effect sizes with 95 % confidence intervals". That is **not what is reported**: chapter 5 reports means with intervals, NCR reduction with a bootstrap interval, and ranks. Cliff's δ lives only in numbers.json. Replace it with a pointer to Section 4.5.4.
- **The Zhang and Arcuri clauses would duplicate.** §5.1 compares 1 000 against Zhang's 100 while §4.5.4 cites Arcuri. Keep Zhang's comparison in §5.1 and Arcuri's justification in §4.5.4, or move both to one place.
- **Table 5.3 caption** (`tab_5-3-2d_attacker_ranking.tex`) points to `sec:evaluation-metrics` for the ranking. Point it to `subsec:metrics-statistics`. The caption's "mean hosts compromised per seed" matches the draft.
- **Appendix F tables** (`tab_F-1_*`): "± a 95 % interval on the mean (normal approximation)" matches Variant A. If Variant B is adopted, add "over seeds".
- **Table 5.2 (`tab_5-2-1a`)** gives ASP as mean ± normal approximation, a Wald interval on a proportion. Near 0 it is poor ($c_3$ 0.05 ± 0.04). The draft's "a mean" covers it, but a Wilson interval would be more defensible.
- **Figure 5.3(c) caption** ("bootstrap intervals over runs") matches the time-lost sentence.
- **Figure 5.4 caption** ("95 % percentile bootstrap intervals") matches.
- **Pitfalls table in the handoff** ("every value with a 95 % interval"): shares such as relative tactic occurrence, APV and attack confidentiality carry none. Either soften the pitfall row or accept it; this draft does not claim it.
- **§8j-4 content point** "middle neighbours at 0.19–0.20": does not reproduce (F4). Retire it.

## Open for Marc

1. **Bootstrap by seed (the OPEN issue).** Recommend **Variant B**: resample seeds jointly for the defended and no-defence cells, and take the intervals on means over per-seed values, before the 1 000-seed run. F1 and F2 show both current choices are wrong in opposite directions, and one of them changes a reading.
2. **The Welch–Holm check.** It is not in the code and holds only at 200 s. Recommend adding it to `analyse.py`, reporting agreement per interval in Appendix F, and keeping the sentence. If you would rather not, cut the sentence and say instead that the pooled variance is a stated assumption.
3. **Four bib keys to add**, or cut the sentences that need them:
   - `efron1994introduction`: Efron, B. & Tibshirani, R. J., *An Introduction to the Bootstrap*, Chapman & Hall/CRC, 1993/1994, DOI 10.1201/9780429246593 (to download);
   - `tantithamthavorn2019impact`: Tantithamthavorn, McIntosh, Hassan & Matsumoto, "The Impact of Automated Parameter Optimization on Defect Prediction Models", *IEEE TSE* 45(7), 683–711, 2019, DOI 10.1109/TSE.2018.2794977 (arXiv 1801.10270, read);
   - `welch1947generalization`: Welch, B. L., "The Generalization of 'Student's' Problem when Several Different Population Variances are Involved", *Biometrika* 34(1/2), 28–35, 1947, DOI 10.2307/2332510;
   - `holm1979simple`: Holm, S., "A Simple Sequentially Rejective Multiple Test Procedure", *Scandinavian Journal of Statistics* 6(2), 65–70, 1979 (not on Crossref; confirm on JSTOR).

   Recommend adding all four.
4. **To download:**
   - Scott & Knott 1974 (JSTOR), to confirm the likelihood-ratio test and α;
   - Cohen 1988, to confirm d = 0.2 as "small";
   - the STVR version of Arcuri & Briand, to confirm the page and whether "at least n = 1,000" survived from the TR.
5. **Cohen 1992 for the threshold.** Tantithamthavorn cites *A power primer* (Psych. Bull. 112(1), 155–159) for the 0.2 cut. Recommend keeping only Cohen 1988, whose "small" effect is the same 0.2, unless your copy disagrees.
6. **Heading.** Recommend keeping *Statistical analysis* (Structure section).
7. **Arcuri recommends Mann–Whitney and Â12 in the same guideline.** Recommend owning this in one clause of ch6 threats rather than here, because Scott–Knott ESD follows Tantithamthavorn's practice, which itself cites Arcuri for the run count.
8. **Morris, White & Crowther 2019** (Monte Carlo uncertainty, *Stat Med* 38(11) 2074–2102, DOI 10.1002/sim.8086) is not cited. Recommend leaving it out; Arcuri already carries the point in the budget.
