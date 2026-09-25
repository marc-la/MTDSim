# 10 · Time lost per MTD deployment (§4.5.3, `eq:time-lost`)

## LaTeX

```latex
\paragraph{Time lost per MTD deployment.}
We define time lost per MTD deployment to measure the progress one deployment
costs the attacker, in seconds at the attacker's own pace. Its form is the loss
of resilience of \citet{bruneau2003}: the area between a system's quality after
a shock and its full level, over the time the system takes to recover. Here the
quality is $\tilde{r}$, the attacker's NCR growth rate relative to its rate
before the deployment (Equation~\ref{eq:ncr-growth}), read over the 1\,250\,s
after the deployment completes at $t_d$:
\begin{equation}
  L = \int_{0}^{1250} \bigl(1 - \tilde{r}(t)\bigr)\,\mathrm{d}t \;-\; L_{\text{none}},
  \label{eq:time-lost}
\end{equation}
where $t$ is the time in seconds since $t_d$, and $L_{\text{none}}$ is the same
integral read at the same moments on the attacker's no-defence run of the same
seed. The integral is evaluated as a sum over the ten 125\,s bins in which
$\tilde{r}$ is estimated, with every deployment of a cell pooled before the
ratio is taken. $L_{\text{none}}$ is subtracted because an attacker's pace
drifts within a run with no defence acting on it. A deployment that stops the
attacker for 300\,s and then lets it resume at its former pace costs 300\,s;
zero is no cost, and a negative value means the attacker ran above its former
pace afterwards and more than made up the dip. Every deployment that completes
at least 750\,s into a run counts, whether or not it interrupts the attacker, so
that the rate before it has a full window. The 1\,250\,s limit follows from the
2\,000\,s deployment interval, the only interval at which time lost is read
(Section~\ref{subsec:aio-disruption}): the next deployment's 750\,s window
begins there, and beyond it the curve would re-read that window, which returns
it to 1 by construction.
NCR reduction reads the net effect of a defence over the run, and MTTC the time
to the first host; neither says what one deployment does to the attacker's
progress. The field's recovery metric, mean time to recovery, is the defender's
time to restore a system \citep{enoch2018}; the attacker has to recover too,
because an address mutation forces it to rediscover the network it had mapped
\citep{jafarian2015}. Time lost is the dip at a deployment, measured against the
attacker's pace between deployments, so it can differ in sign from NCR
reduction when a defence raises that pace. A dip that has not recovered by
1\,250\,s is cut off at the window's end, so its time lost is a lower bound.
```

**Word count:** about 385 words of prose (equation excluded), 13 sentences. That is long for 13 sentences, because sentences 3, 9 and 11 each carry two clauses; see Structure for the cut candidates.

## Structure

| Slot | Used | Sentence(s) |
|---|---|---|
| S1 name, status, citation | yes: "We define … to measure …" (introduced), with the form anchored at once to Bruneau et al. 2003 | 1–2 |
| S2 what it measures | merged into S1 (the corpus's "We propose a … metric for measuring …" does both in one sentence) | 1 |
| S3 operation in words → equation → "where" | yes; the words ride sentence 3, the "where" clause defines $t$ and $L_{\text{none}}$; $\tilde r$ and $t_d$ are pointed back to `eq:ncr-growth` and the shared symbols | 3–4 |
| (evaluation) | one sentence: the discrete sum the integral stands for, and the pooling (the pitfalls table's "pooled before the ratio is taken") | 5 |
| S4 range and direction | seconds; zero, positive, negative; with the one worked value (300 s), licensed because "seconds at its own pace" is not an intuitive reading | 6–7 |
| S5 when read, edge cases | which deployments count (≥ 750 s, interrupting or not); why 1 250 s; read at 2 000 s only | 8–9 |
| S6 introduced: why no cited metric | NCR reduction (net) and MTTC (first host); MTTR is the defender's; Jafarian for why the attacker must recover | 10–11 |
| S6 limitation | the dip, not the net (sign can differ from NCR reduction); truncation → lower bound | 12–13 |

**Merged/dropped.** S2 merged into S1. Two limitations kept, not one: the dip/net distinction licenses §5.3.1 content point 3 and pre-empts the sign-disagreement an examiner will find in Figure 5.3(c) against Table 5.3; the truncation licenses content point 4 ("lower bounds"). Marc's S6 note on *adaptivity* is left to §5.3.1's head, which already says it (l.7417–7418): putting it here would attribute (measurement is not attribution). **Length:** 13 sentences against 8–15 (upper half). The cut candidates, if Marc wants ~10: the MTTR/Jafarian sentence (the examiner's "isn't this MTTR?" question then goes unanswered), or sentence 12 (then §5.3.1 must carry the dip/net distinction alone).

## Verification

### Sources

| Claim | Source, locator | Verbatim quote | Verdict |
|---|---|---|---|
| The form (area between quality and its full level after a shock, integrated over recovery time) is Bruneau et al.'s *loss of resilience* | Bruneau et al. 2003, *Earthquake Spectra* 19(4):733–752, p. 736–737, the one equation of §"Resilience"; open access at the first author's page (`https://www.eng.buffalo.edu/~bruneau/EERI%202003%20Bruneau%20et%20al.pdf`, read in full text) | p. 736: "a measure, Q(t), which varies with time, has been deﬁned for the quality of the infrastructure … 100% means no degradation in service and 0% means no service is available." p. 737: "community earthquake loss of resilience, R, … can be measured by the size of the expected degradation in quality (probability of failure), over time (that is, time to recovery). Mathematically, it is deﬁned by R = ∫_{t0}^{t1} [100 − Q(t)] dt" | **holds** for the form. Differences, all ours: the quality is the attacker's relative growth rate, not a service level; the upper limit is a fixed 1 250 s, not full recovery $t_1$; $\tilde r$ may exceed 1 (Bruneau caps quality at 100 %); the placebo subtraction has no counterpart. The name "resilience triangle" is **not** in this paper (grep: no hit); it is later literature, so the draft does not use it. |
| The area-under-the-functionality-curve construct is current in cyber resilience | Kott & Linkov 2021, *IEEE Computer* 54(2):80–85, arXiv 2102.09455 preprint p. 2 | "a more resilient system would exhibit a greater area under the curve (AUC) – the integral of retained system functionality F(t) over the total mission time Tm"; and, on attackers: "impressive examples of cyber resilience may come from malware operations … TrickBot … has demonstrated an agile and effective recovery" | holds; **not cited in the draft** (origin rule, literature conventions §f: cite Bruneau). Offered in Open as a bridge if the examiner wants a security-field instance. |
| The field's recovery metric (MTTR) is defender-side | Enoch, Hong, Ge & Kim 2018, *Software Networking* 2018(1):137–160, arXiv 2007.03486, p. 5, Table 1 | "Mean-Time-to-Recovery (MTTR) [16] is used to assess the eﬀectiveness of a network to recovery from an attack incidents. It is deﬁned as the average amount of time required to restore a system out of attack state." | holds. Census F (`metric_census/F_web_open_access.md:94`): "I found no attacker-side recovery metric under an established name." Enoch cites Jaquith 2007 (a book, unread); cite Enoch for what Enoch says. |
| An (address) mutation forces the attacker to redo reconnaissance | Jafarian, Al-Shaer & Duan 2015, IEEE TIFS 10(12), §VII-E (`docs/sources/tactic_profiles/step_d/10_disc/An_Effective_Address_Mutation_Approach_for_Disrupting_Reconnaissance_Attacks.md:373`); also §VII (l.279) | l.373: "Changing the addresses of network hosts invalidates existing mappings of network hosts, thus forcing potential attackers to squander their resources on re-discovery of these mappings." l.279: "after each mutation interval, the attacker is forced to restart his scan." | holds, bounded to *address* mutation (the draft says "an address mutation"). |
| No cited metric reads one deployment's cost: NCR reduction is the net over the run; MTTC the first host | this thesis's own definitions (entries 7, 8; §4.5 holders l.5516–5552) | — | holds by construction of those definitions. |

### Code check (`data/results/ch5_defended/disruption.py`)

| Term of Eq. `eq:time-lost` / claim in prose | Code | Verdict |
|---|---|---|
| Anchor $t_d$ = the deployment's completion | l.96 `e[2]` of `mtd_executions`; `analyse.py:155` names `e[2]` `finish_time` | matches |
| Deployments counted: completes ≥ 750 s in, before the run ends; every one, interrupting or not | l.96 `-EDGES[0] <= e[2] < T` (no interrupt filter anywhere) | matches |
| Window 0 to 1 250 s after $t_d$ | l.67 `EDGES = np.arange(-750, 1251, 125)`; post bins `~PRE` (l.140) | matches |
| Integral as a sum over ten 125 s bins | l.142 `np.nansum((1 - rate / pre) * np.diff(EDGES)[post])`, ten post bins of 125 s | matches. Edge: a bin with no live time is dropped (`nansum`), i.e. contributes 0. It never binds in the reported cells: every cell's minimum pooled live seconds per bin is ≥ 74 125 s (`disruption_numbers.json`). |
| $\tilde r$ = pooled rate over pooled before-rate (ratio of sums) | l.148 sums over runs and deployments first; l.139 `pre = num[PRE].sum() / den[PRE].sum()`; l.141 `rate = num[post] / den[post]` | matches (pooled before the ratio) |
| $L_{\text{none}}$ = same integral, same moments, same seed's no-defence run | l.128 `none[(arm, profile, seed)]` supplies the counts and live time; `r["landings"]` (the defended run's $t_d$) are the moments (l.108); l.156 `_time_lost(pn, pd)`: the placebo's own before-rate normalises it | matches ("the same integral") |
| $L = $ raw − placebo | l.160 `"seconds": raw - plac` | matches |
| Run end (censoring) | l.111–113 bins clipped to $T$, so live time stops at the run's end; l.118–120 the run-ending compromise counted once | matches; this belongs to the growth-rate definition (live time), cited through $\tilde r$ |
| Read at 2 000 s only | l.181 `per_deployment = iv >= EDGES[-1] - EDGES[0]` (2 000); time lost computed only then and only per single mechanism (l.185) | matches |
| 1 250 s = where the next deployment's before-window starts | measured on the corpus: completion-to-completion gaps at the 2 000 s interval run 1 997–2 004 s (1 405 gaps, 201 runs; percentiles 0/50/100 = 1 997.0 / 2 000.5 / 2 003.6 s) | holds to ±4 s |
| Negative values occur | `disruption_numbers.json`: APT attacker model, user shuffle −13 s; relative rate reaches 113–138 % in post bins | holds |
| Worked value (300 s dead stop, full resumption → 300 s) | ∫(1 − 0) over 300 s + ∫(1 − 1) after = 300 | holds (also the code's docstring, l.35–36) |

**No mismatch** between equation and code.

### Status check

"Introduced" is honest for the quantity: no attacker-side recovery metric exists under an established name (census F, `F_web_open_access.md:94`), and the catalogue row (`mtd_metric_catalogue.md:37`) records "Does not exist attacker-side". The **form** is Bruneau's loss of resilience, so the status is "introduced, in the form of Bruneau et al." (the same move as NCR reduction "in the form of" Alavizadeh). The name reuses no field name; "time lost" is not a lineage metric, and "resilience" is not used as the metric's name (that would claim the defender's concept for the attacker).

## Symbols

| Symbol | Use | Status | Collision check |
|---|---|---|---|
| $L$ | time lost per MTD deployment | **new**; "L" for loss (Bruneau's own letter is $R$, which is chapter 4's rule kernel, so it cannot be reused) | `grep` of live (uncommented) lines of `dissertation.tex` and `tables/*.tex` for `$L`, `L_{`, `\mathcal{L}`, `\ell`: no hit. Free. |
| $L_{\text{none}}$ | the placebo term | new, subscript as NCR reduction's draft $\overline{\mathrm{NCR}}_{\text{none}}$ | free |
| $t$ | seconds since $t_d$ (integration variable) | as the growth-rate draft uses it | chapter 4's $t_{pq}$ is subscripted; bare $t$ is conventional for time. Low risk. |
| $t_d$ | the moment a deployment completes | shared (brief) | free (only hit: a figure filename) |
| $\tilde r$ | relative NCR growth rate | **defined by the NCR growth rate agent**; `eq:ncr-growth` | **Collision flagged:** the shared notation reserves $r$ for *a run* (and $\mathcal{R}$ its set), while the boilerplate draft writes the growth rate as $r(t)$, $\tilde r$, $\bar r_{-}$. One of them must move. This draft uses $\tilde r$ as the boilerplate does; a rename is a find-and-replace here. |

## For elsewhere

- **NCR growth rate (dependency).** This draft assumes it defines: $\tilde r(t) = r(t_d+t)/\bar r_{-}$ with $t$ in seconds since $t_d$; estimation in 125 s bins of live time; pooling over every deployment of a cell (and the APT attacker model's four profiles) *before* the ratio; the 750 s before-window; live time stopping at the run's end with the run-ending compromise counted. If it does not state the pooling, sentence 5 here must carry it in full. It must also resolve the $r$ collision above.
- **4.5.4.** (i) Time lost's interval is a seeded percentile bootstrap, 2 000 resamples, **over runs** (profile × seed for the APT attacker model), each resampled with its placebo pair (`disruption.py:157–161`). That conflicts with 4.5.4's "the unit is the seed, profiles averaged per seed". Either 4.5.4 names the exception, or the bootstrap resamples seeds (with all four profiles' runs together). (ii) Its row in the "reported as" table: "pooled over deployments, with a run bootstrap" is accurate.
- **§4.5 opener / shared symbols.** "Cell" must be defined there. For §5.3.1's reads, the APT attacker model's cell pools its four profiles, weighted by live time; the brief's $\mathcal{R}$ ("one attacker, one condition, one interval") should say so.
- **Table 4.3 source cell.** Recommend "introduced here, in the form of \citep{bruneau2003}" (parallel to NCR reduction's "in the form of").
- **References.bib.** Three keys missing: `bruneau2003`, `enoch2018` (below, Open). `jafarian2015` is present.
- **Chapter 5.** Figure 5.3's caption ("read as seconds at the attacker's pre-deployment rate and net of the same area with no defence, with 95 % bootstrap intervals over runs") agrees with the equation and the code. No live body prose reads time lost yet. §5.3.1 owes (from §8g-5): the dip/net sign disagreement (baseline, topology shuffles), the lower bounds, and the 200 s sentence. This definition licenses all three. §5.3.1's head says "the 200 s interval is reported in the text where it differs": for time lost it cannot be (the metric is undefined at 200 s), so any 200 s sentence must use the growth rate, not time lost.
- **Table 5.1** now lists six intervals (50–2 000 s): time lost exists only at 2 000 s. The definition says so. The §5.3.3 interval-sweep floats must not carry it.

## Open for Marc

1. **Anchor the form to Bruneau et al. 2003 (status "introduced, in the form of").** Recommend yes: it is the origin of the area-of-the-dip construct and is open access. Bib entry: `@article{bruneau2003, author = {Bruneau, Michel and Chang, Stephanie E. and Eguchi, Ronald T. and Lee, George C. and O'Rourke, Thomas D. and Reinhorn, Andrei M. and Shinozuka, Masanobu and Tierney, Kathleen and Wallace, William A. and von Winterfeldt, Detlof}, title = {A Framework to Quantitatively Assess and Enhance the Seismic Resilience of Communities}, journal = {Earthquake Spectra}, volume = {19}, number = {4}, pages = {733--752}, year = {2003}, doi = {10.1193/1.1623497}}`.
2. **Cite Enoch et al. for MTTR.** Recommend yes (the examiner's "isn't this MTTR?"). Bib: `@article{enoch2018, author = {Enoch, Simon Yusuf and Hong, Jin B. and Ge, Mengmeng and Kim, Dong Seong}, title = {Composite Metrics for Network Security Analysis}, journal = {Software Networking}, volume = {2018}, number = {1}, pages = {137--160}, year = {2018}, note = {arXiv:2007.03486}}`. Confirm the page range on the published version.
3. **Kott & Linkov 2021 as a security-field bridge to Bruneau.** Recommend no (the origin rule). Keep it in reserve if the examiner asks for a cyber-security instance.
4. **Rename the growth rate or the run** (the $r$ collision). Recommend the run keeps $r$ (it is used by every other definition), and the growth rate takes $g(t)$, $\tilde g$, $\bar g_{-}$. $g$ is free in the live tex (grep for `$g`, `\tilde{g}`, `\bar{g}`: no hit).
5. **Two limitations, or one.** Recommend both (each licenses a §5.3.1 content point); cut sentence 12 only if §5.3.1 carries the dip/net distinction itself.
6. **Bootstrap unit for time lost** (runs, not seeds). Recommend resampling by seed before the 1 000-seed run, for consistency with 4.5.4.
