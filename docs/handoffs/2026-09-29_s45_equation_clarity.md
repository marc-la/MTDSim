---
status: open
created: 2026-09-29
---

# §4.5 Evaluation metrics: equations a reader can follow, and every number with a basis

## State of play

Marc's read of §4.5 (2026-09-29): the prose is tight, but the equations read as
decoration. The causes are:

- undefined symbols ($q$, $a_j$, $b$, $\mathbf{1}[\cdot]$);
- notation borrowed from §4.3 that does no work here ($\tau_p$);
- set-builder notation for simple ideas (APV);
- one-off Greek letters ($\lambda$, $\theta$, $\kappa$), one of which clashes: $\lambda$ is already the vulnerability-memory factor in §4.4.5;
- seven different time constants across the metrics (1 000, 60, 1 500, 750, 1 250, 125 and 2 000 s), most without a stated basis.

His further points:

- One template was applied to ten metrics that differ. Some are the field's, some are adapted, and some we introduced.
- A metric whose equation is borrowed should quote its source's equation and then show the adaptation ("don't take my word for it, take theirs").
- A metric name should stand on the left of the equation instead of a Greek letter.
- The hard-coded numbers make the metrics hard for a practitioner to port.

This session **verified every equation against the code that produced the
chapter 5 numbers**. Nine hold. The NCR growth rate equation is **wrong as
written**. It takes the derivative of one run's NCR over that run's own mean
before the deployment. Per run that is zero almost everywhere and divides by
zero whenever no host fell in the window before. The code (`disruption.py`,
`_sums`/`_relative`) computes a **pooled ratio of counts to live seconds**,
which the sentence after the equation describes in words. The prose and the
maths disagree.

**Evidence, all 2026-09-29, in `docs/sources/extractions/s45_metric_definitions/`:**

- `12_equation_conventions.md`: 26 conventions and pitfalls from open sources. The main ones:
  - Knuth et al. *Mathematical Writing*: rule 13, the "blah" test; rule 3, words over shorthand; rule 14, one notation per thing.
  - Halmos: "the best notation is no notation".
  - Mermin: refer back by phrase as well as number.
  - ISO/IEC/IEEE 15939: define base measures once, then each derived measure as a function of them.
  - The ODD protocol and the ACM SIGSOFT Empirical Standards: a basis for every parameter value, and a sensitivity check.
  - Hong 2018 §5.3: one worked example through every metric.
- `13_source_equations.md`: what each source actually writes, verbatim, one paper per pass.
  - Zaffarano, Hong, Alavizadeh, Bruneau, Čisar and Ho have equations. Rodríguez, Zhan, Cho and Zhang do not.
  - No source licenses any of our time constants.
- `14_detector_conventions.md`: production intrusion detectors (Snort 2/3, Suricata, Zeek) and academic ones (Williamson, Jung TRW, Čisar).
  - The conventional rate alarm is "at least N events in the last W seconds".
  - **60 s is the most common default window**: Snort sfPortscan low; the Snort and Suricata `detection_filter` examples. Longer defaults are 90 s, 300 s, 600 s and 900 s.
  - No source sets an alarm "to flag half a known attacker".
- The three open-access texts that were missing (zhan2013, cisar2010, bruneau2003) and the detector sources are kept in `docs/sources/s45_fetched/` (gitignored).

**Corrections to earlier records, found by these passes (not yet applied):**

- `10_time_lost.md`: Bruneau does *not* cap quality at 100 %. He mentions recovery to "more than 100% pre-earthquake levels". The phrase "resilience triangle" is not in the paper.
- `04_attack_confidentiality.md`, row 7: Jafarian's "fast scanning is easy to detect [4]" *is* in the markdown, at l.289.
- The tex drops "plaintext" from Zaffarano's exposure rule ("visible in plaintext in network traffic").
- APV is presented as "adapted from Hong Eq. 2", but it is a **different formula**:
  - Hong average the change in the set of attack paths between successive network states.
  - Ours is 1 minus the share of the most common opening.
  - The change of form is not stated.

## Recommended approach: the template

The conventions agree on one structure, which replaces the current identical template of six slots:

1. **A shared opening, once.** It defines the cell $\mathcal{R}$ and a run $r$, and what the simulator records per run:
   - the run's steps;
   - its actions and their start times;
   - its compromised hosts and their times;
   - whether a target fell;
   - the run's length.

   It also names the three experiment settings every window derives from, each pointed *backwards* where it can be:
   - the network's $N = 50$ hosts, §2.2.1 (`subsec:network-model`);
   - the time limit $T$ and the deployment interval $I$, Table 5.1, the one forward pointer. They are experiment settings, so this is unavoidable, and saying so is enough.
2. **Per metric:**
   - **Name on the left of the equation.** No per-metric Greek letter.
   - One sentence that defines it and still reads if the equation is skipped. This is the "blah" test.
   - The property it records.
   - The equation in plain operators, as a function of the shared measures.
   - A *where* clause for anything the opening did not define.
   - Unit, range and direction.
   - The empty case.
   - Each parameter named, with its basis.
3. **Differentiated by provenance.** One template does not fit ten metrics:
   - **The field's, used as defined** (ASP, NCR): the source's words, then our estimator. Short.
   - **Adapted, where the source has an equation** (attack confidentiality, NCR reduction, APV): **quote the source's equation in its own notation**, then state each substitution. This is Marc's "take theirs".
   - **Adapted, where the source has no equation** (relative tactic occurrence, attack rate, MTTC): quote the source's words, then give our equation.
   - **Introduced** (NCR growth rate, time lost): the source of the *form* (Bruneau's loss of resilience, quoted), a worked example with round numbers, and every constant derived or swept.
4. **Worked examples use invented round numbers**, like the existing 300 s one. They never use chapter 5 results, per the ch5-antecedent rule in reverse: method before results.

## Per-metric proposals

$\mathcal{R}$, $r$, $N$, $p$ (a tactic, §4.3), $I$ and $T$ are defined once in the opening.

**1. Relative tactic occurrence.** Number-preserving.

The source is the relative occurrence column of Rodríguez et al. (Table 3), "Occur. (rel.)", which has no equation.

$$\text{relative tactic occurrence}(p) = \frac{\sum_{r} n_r(p)}{\sum_{r} n_r},$$

where $n_r(p)$ is the number of steps run $r$ takes in tactic $p$ and $n_r$ is all its steps.

- $\tau_p$ and $q$ are gone.
- One added sentence: the baseline attacker has actions, not tactics. Each of its steps is placed on the tactic that maps to its action (§4.4.3), so both attackers are read on the tactics' axis. This is what Figure 5.1(a) already does. Marc asked for this.

**2. APV.** Number-preserving if the modal form is kept.

$$\mathrm{APV}_k = 1 - \frac{m_k}{|\mathcal{R}|},$$

where $m_k$ is the number of runs that follow the most common opening of $k$ steps.

- Say what $k$ is: the *length* of the opening. It is not a tactic. Marc read $k$ and $p$ as doing the same work.
- Say which $k$ is reported: 1 to 8, drawn in Figure 5.1(b).
- **Quote Hong's Eq. 2 as printed**, then name the change of form. Their states form a sequence and our runs do not, so each run is compared with the most common opening instead of with its predecessor.
- *Alternative (flagged, not recommended):* the Gini–Simpson index, $1 - \sum_\pi s_\pi^2$, "the chance two runs picked at random open differently". It is the order-free form of Hong's pairwise change, and so the closer transposition. It would change Figure 5.1(b)'s numbers.

**3. Attack rate.** The unit is Ruling B.

The source is Zhan's "number of attacks that arrive at unit time", which has no equation. Zhan picked per hour as "natural" for his time scale, which is a precedent for fitting the unit to the scale.

$$\text{attack rate} = \frac{1}{|\mathcal{R}|}\sum_{r}\frac{\text{actions}_r}{\text{active time}_r},$$

The symbol $\lambda$ is dropped. That also removes the clash with §4.4.5.

**4. Attack confidentiality.** The detector is Ruling C.

**Quote Zaffarano's equation:**
$$\mathrm{Confidentiality}(M,\nu) = \frac{1}{|T|}\sum_{\tau\in T}\nu(\tau,\mathit{unexposed}).$$

Then state the substitutions:

- Their tasks $T$ become the attacker's actions, pooled over the cell.
- Their exposure rule, "visible in plaintext in network traffic", becomes "not flagged by the detector". MTDSim has no traffic.

**The detector, recommended form:** an action is flagged when the attacker has taken at least $\theta$ actions in the 60 s up to and including it. This is the count-in-a-window alarm of Snort and Suricata, and 60 s is their common default.

- $\theta$ is the baseline attacker's median count, 3.
- The alarm then flags 64 % of the baseline attacker's actions. With whole counts, "half" cannot be hit exactly.
- The exponential kernel, the EWMA derivation and $\kappa$ all go.
- Read over the run in ten equal slices of the time limit, $T/10$. That is *where the 1 500 s comes from*. Marc's "a run is not always 1 500" was the missing derivation.
- A run that ends early adds only to the slices it reaches.

**5. ASP.** Number-preserving.

$$\mathrm{ASP} = \frac{\text{runs that compromise a target host}}{|\mathcal{R}|}.$$

This is written in words, so the indicator function goes. Cho's page is p. 727 per `13_source_equations.md`. The draft cites Sec. VII-A, which stands.

**6. NCR.** Number-preserving.

Show Ho's Eq. 10 as the form, $\mathrm{HCR} = C_t / T_{host}$, read at the run's end. Point $N$ back to §2.2.1.

**7. MTTC.** Number-preserving.

This one is clear already. **Separate gap:** Table 5.2 reports MTTC without the covered share $|\mathcal{R}_1|/|\mathcal{R}|$ that §4.5 promises. Add a column or a caption clause.

**8. NCR reduction.** Number-preserving.

Quote Alavizadeh's Eq. 13 whole. It is piecewise, with a floor of 0 when the defence does not lower the loss. Then state the two changes: ALE → NCR, and the floor dropped.

**9. NCR growth rate.** A correction. The window is Ruling A.

$$\text{NCR growth rate}(s) = \frac{C(s)/S(s)}{C_{-}/S_{-}},$$

where:

- $C(s)$ is the hosts compromised in slice $s$ after a deployment, summed over every deployment of every run in the cell;
- $S(s)$ is the seconds of that slice in which the run is still going;
- $C_-$ and $S_-$ are the same over the window before the deployment.

Its value is 1 at the attacker's earlier pace and 0 when the attacker has stalled. A sentence keeps the derivative: NCR rises in steps of $1/N$, so compromises per second estimate its slope. This is exactly what the code computes, and the pooled ratio is what makes it defined. Figure 5.3(a,b) draws it in 125 s slices; the slice width is a resolution of the figure, and Table C.5 shows it changes no value.

**10. Time lost per MTD deployment.** The window is Ruling A.

**Quote Bruneau:** $R=\int_{t_0}^{t_1}[100-Q(t)]\,dt$, where $t_0$ is the event and $t_1$ is full repair.

Ours:
$$\text{time lost} = W_{+}\bigl(1 - \text{NCR growth rate over } W_{+}\bigr) \;-\; \text{the same on the no-defence run}.$$

- In words: the window after the deployment, times the fraction of pace lost in it.
- **This is Bruneau's area.** The integral of $(1 - \text{relative pace})$ over a window equals the window's length times $(1 - \text{its mean})$.
- **Verified on the corpus:** the one-slice form matches the current 125 s-bin area to within 13 s on all 14 cells (below).
- The integral and the bins leave the definition.
- Worked example, round numbers: the attacker runs at 60 % of its pace for the 1 000 s after a deployment, so it loses 400 s.

## Rulings needed (ask once; recommendation first)

**A. The window around a deployment. Recommend: half the interval each side, $I/2$ before and $I/2$ after (1 000 s + 1 000 s at $I$ = 2 000 s).**

- It removes the only window number with no basis, 750 s. 1 250 s is just what is left of 2 000 s.
- It makes the window portable to any interval.
- Cost: the after-window shortens by 250 s, so a dip that has not recovered is cut earlier and read as a lower bound.
- The alternative is to keep 750/1 250 and give 750 a basis. None was found.

Dry-run: time lost, s, at 2 000 s. Placebo-corrected; pooled; no bootstrap yet.

| cell | now: 750/1 250, 125 s bins | 750/1 250, one slice | $I/2$ each side, one slice |
|---|---|---|---|
| APT, IP shuffle | 511 | 524 | 475 |
| APT, host topology | 483 | 494 | 434 |
| APT, complete topology | 429 | 442 | 423 |
| APT, service diversity | 194 | 198 | 161 |
| APT, OS diversity | 55 | 54 | 38 |
| APT, port shuffle | 47 | 48 | 38 |
| APT, user shuffle | −13 | −14 | −25 |
| baseline, service diversity | 593 | 599 | 461 |
| baseline, complete topology | 103 | 109 | 112 |
| baseline, host topology | 97 | 101 | 82 |
| baseline, IP shuffle | 86 | 88 | 24 |
| baseline, user shuffle | 53 | 55 | 63 |
| baseline, OS diversity | 8 | 12 | 18 |
| baseline, port shuffle | 3 | 3 | −4 |

- The APT model's order is unchanged.
- The baseline's largest value, service diversity, keeps its place but drops by 22 %. Its dip is still 72 % below its earlier pace at 1 250 s (§5.3.1), so a shorter window cuts more of it.
- Every other baseline value is below 115 s, where Appendix C.5 already says a value is "not read as different from zero".
- The APT model's four largest values move by 3 to 10 %.

**B. The attack-rate unit. Recommend: per minute.**

- A minute is a standard unit, while 1 000 s is a scale.
- It shares its unit with the detector's 60 s window: "about one action a minute; the alarm sounds at three in a minute".
- Table 5.2 would read 1.0 (APT aggregate) against 1.7 (baseline), instead of 16.9 against 28.4.
- Per hour, Zhan's own "natural" choice, is the alternative: 61 against 102. No run is re-done either way; only the numbers are rescaled.

**C. The detector. Recommend: the 60 s count window with $\theta$ = 3, the baseline's median count.**

The finding holds under every form tried. Every APT profile stays above the baseline in every slice, in the order $c_3 > c_2 > c_1 > c_4 >$ baseline, with one exception: under the count ≥ 3 detector, $c_2$ and $c_3$ are level in the first slice (75.8 % each).

| detector | baseline flagged | whole-run confidentiality: $c_1$ / $c_2$ / $c_3$ / $c_4$ / baseline |
|---|---|---|
| now: exponential, $\kappa$ = 60 s, $\theta$ = 2.95 | 50 % | 76 / 87 / 91 / 70 / 50 % |
| count ≥ 3 in 60 s (recommended) | 64 % | 63 / 73 / 79 / 57 / 36 % |
| count ≥ 4 in 60 s | 42 % | 82 / 90 / 93 / 78 / 58 % |

- The recommended form is the field's own alarm, with a cited window and a threshold stated as a count.
- The empty appendix `app:detector-memory` becomes a sweep with a cited range:
  - windows 60, 90, 300 and 600 s, the Snort low/medium, Zeek and Snort high defaults;
  - counts 2 to 6.
- Alternative: keep the exponential and cite 60 s by the same equivalence (at a steady rate, a memory of $\kappa$ averages the same count as a window of $\kappa$). This keeps every number but also keeps the formula Marc found hardest.
- Changes: Figure 5.2(b), the §5.2 prose numbers (the `\prelim` 69–93 % and 43 %), and `analyse.py` (`_detector_levels`, the median rule).

**D. APV's form. Recommend: keep the modal form, and state the change from Hong.** Gini–Simpson is closer to Hong but changes Figure 5.1(b) for no gain in clarity.

## Blast radius, by ruling

- **A:**
  - `data/results/ch5_defended/disruption.py`: `EDGES`, and `_time_lost` if the one-slice form is adopted in code;
  - `ablation.py`, which imports it;
  - `tools/ch5_disruption_figure.py`: Figure 5.3;
  - `tools/ch5_timelost_window_table.py`: Table C.5. Re-base its sweep on the split, e.g. before/after at 750/1 250, $I/2$ and 1 250/750;
  - the numbers in §5.3.1 (l.~7984–8010), in §5.4 ("494 s", l.~8562), and in chapter 6 if any are quoted.
- **B:** Table 5.2's header and column, Table 4.3's row, the §5.2 prose ("11.7 to 20.7 actions per 1 000 s"), and the §6 mentions.
- **C:** `data/results/ch5_s531_unopposed/analyse.py`, Figure 5.2(b), the §5.2 prose, Appendix `app:detector-memory` (a new sweep and table), and Table 4.3's description.
- **Number-preserving rewrites (1, 2, 5–8, and the corrected equations for 9 and 10):** §4.5 and Table 4.3 only.

## Validation gate

- §4.5 passes Knuth's "blah" test: every definition still reads with its equation replaced by "blah".
- No symbol in §4.5 is used before it is defined, and none clashes with Table 4.2 or §4.4.5.
- Every number in §4.5 is cited, derived from $N$, $T$ or $I$, or declared and swept in an appendix. Grep the section for digits and account for each.
- Every equation is re-traced against the code line that computes the reported number, as the 04 record's hand trace did.
- The tex builds; Figure 5.2(b), Figure 5.3, Table 5.2 and Table C.5 are regenerated under the rulings; and the voice gate (voice.md §f) is run on §4.5.

## Hard constraints

- Rulings A–C change reported numbers. **None is applied without Marc's ruling.** The rewrites that preserve numbers can go first.
- Open-access sources only. The paywalled items in records 12 and 14 go on Marc's list.
- Chapter 5 prose uses only chapter 4 vocabulary. Worked examples in §4.5 use invented numbers, never results.

## Reading list

- `docs/thesis/dissertation.tex` §4.5 (l.5588–5870) and `tables/tab_4-5a_metrics.tex`.
- `docs/sources/extractions/s45_metric_definitions/12_equation_conventions.md`, the template section at the end.
- `13_source_equations.md`, the summary table at the end.
- `14_detector_conventions.md`, its conclusions.
- `data/results/ch5_defended/disruption.py`, the docstring and `_sums`/`_time_lost`.

## Out of scope

- The metric set itself: which ten, their names, and the three groups. The headings were reviewed on 2026-09-29 and stand.
- §4.5.4, Statistical analysis.
