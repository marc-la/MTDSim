---
status: open
created: 2026-09-29
---

# §4.5 Evaluation metrics: equations a reader can follow, and every number with a basis

## Update, 2026-09-29 (second session): Marc's read, the round 3 rewrite and rulings E–G

Marc's read of §4.5, his words condensed:

- The terms are vague ("the defence", "a sophisticated attacker", "the field defines").
- Nuance is stated aloud ("with no defence running", "adapted from", "used as defined").
- Table 4.3's Measures column cannot be specific in one line.
- His supervisor could not answer "why is APV a percentage", "how is relative tactic occurrence computed" or "why 1 minus".
- Attack confidentiality drew "did you make this up".
- The NCR growth rate is "completely lost" (NCR is per run end, averaged over the cell; a growth rate within one run confuses the two), and time lost per MTD deployment carries no confidence.

His writing rule is now durable in [`voice.md` §(0)](../workflows/voice.md) and in CLAUDE.md: purpose, context, audience, clarity, relevance.

### Done in this session (round 3, number-preserving except the attack-rate unit)

- **Table 4.3** has two columns, metric and source. Each group is a heading row naming its section, and the dagger is gone.
- **Preamble:** one paragraph. It gives SQ3, defines a cell in words, and states the three ways a run ends. The metric count, "used as defined" and $\mathcal{R}$ are gone.
- **Lead-ins:** the behaviour lead-in is one sentence mapping each metric to its APT property. The outcome lead-in carries Marc's content: simulation studies repeat over many randomised runs and report established metrics.
- **Equations:** in named quantities ("steps in tactic $p$ / all steps"; "mean over runs"). There are no per-metric symbols, and the τ_p, q, a_j and λ clash is gone.
- **Relative tactic occurrence and APV** are defined as the percentages Figure 5.1 draws. Rodríguez tabulate "Occur. (rel.)" as a percentage (Table 3: 45.01 %), so the figure was always faithful to the source; the definition was not. APV's "1 −" is now the definition itself: "the percentage of runs whose opening differs from the most common one". The change from Hong's Eq. 2 is one sentence. Ruling D is closed as recommended.
- **Attack rate per minute:** Marc's ruling, which closes B. `analyse.py _rate` was changed at source and `numbers.json` regenerated. Only the 22 attack-rate values moved, each by exactly ×0.06 (checked). Table 5.2 was regenerated: APT 0.70–1.24 against baseline 1.71 per minute. The honeypot sentence is cut.
- **Statistical analysis:** cut to what the examiner needs.
- **Term:** *defence mechanism* is the ratified row (terminology.md, 2026-09-07; *MTD mechanism* deprecated). §4.5 uses it and Table 5.1's condition names.

**Owed from the round 3 rewrite:** the §5.2 prose still says "\prelim{11.7} to \prelim{20.7} actions per 1\,000\,s against \prelim{28.4}" (l.~7464). That is Marc's dictated prose, so it is left for him: per minute it is 0.70 to 1.24 against 1.71.

### Ruling E — attack confidentiality: a standard scan-detector rule replaces the declared EWMA detector. Supersedes C.

The detector is what made the metric unreadable:
- an exponential kernel;
- a memory κ with no source;
- an alarm tuned to the median of a quantity with no unit;
- 1 500 s bins.

The thesis also concedes that "the detector counts actions, so the two are one observation" (with attack rate).

What the literature fixes:
- Jung, Paxson, Berger and Balakrishnan 2004 (IEEE S&P; open access; `docs/sources/s45_fetched/trw.pdf`, §2, PDF p. 3): "Historically most scan detection has been in the simple form of detecting N events within a time interval of T seconds". They add: "once the window size is known it is easy for attackers to evade detection by simply increasing their scanning interval".
- The same paper states Snort's default (§6, PDF p. 11): "it flags a source IP address that has sent connections to 5 different IP addresses within 60 seconds".

**Recommended definition:** an action is flagged when it is at least the fifth of the attacker's actions within the 60 s up to and including it. Attack confidentiality is the share of actions not flagged, over every run of the cell.
- Both numbers are the field's.
- Nothing is tuned on the baseline attacker.
- One stated adaptation: actions stand in for connections to distinct addresses.

**Dry run** (no-defence corpus, 100 seeds; `data/results/s45_metric_redesign/stealth_count.py`). Percentage of actions not flagged:

| rule | $c_1$ | $c_2$ | $c_3$ | $c_4$ | baseline |
|---|---|---|---|---|---|
| **5 in 60 s (Snort default, recommended)** | **92** | **96** | **98** | **89** | **83** |
| 3 in 60 s | 63 | 73 | 79 | 57 | 36 |
| 4 in 60 s | 82 | 90 | 93 | 78 | 58 |
| 5 in 90 s (Snort medium window) | 84 | 91 | 95 | 79 | 68 |
| 5 in 600 s (Snort high window) | 3 | 5 | 11 | 2 | 1 |
| 10 in 60 s | 100 | 100 | 100 | 100 | 100 |

- The order $c_3 > c_2 > c_1 > c_4 >$ baseline holds under every rule that flags anything and does not flag almost everything.
- At the default, 2–11 % of the APT attacker model's actions are flagged, against 17 % of the baseline attacker's.
- The margin is smaller than under the retired detector (50 % flagged by construction), because that detector was tuned to the baseline.

**Presentation:**
- **Recommend** one whole-run value per attacker, as a Table 5.2 column beside attack rate, with the N × T sweep as Appendix C.4 (`app:detector-memory`, now a real sweep).
- **Retire Figure 5.2** (confidentiality over the run in 1 500 s bins). That removes the last unsourced constant.
- **Alternative:** keep Figure 5.2 with bins of one tenth of the time limit.

**Proposed tex:**

```latex
\paragraph{Attack confidentiality.}
Attack confidentiality is ``how much attacker activity may be visible by
detection mechanisms'' \citep[Table~4]{zaffarano2015}, computed as the share of
the attacker's actions not exposed. MTDSim has no detection mechanism, so an
action here is exposed when a standard scan detector would flag it. Scan
detectors flag ``N events within a time interval of T seconds''
\citep{jung2004}, and Snort's default flags a source that contacts five
addresses within 60\,s. An action is flagged when it is at least the fifth of
the attacker's actions in the 60\,s up to and including it:
\begin{equation}
  \text{attack confidentiality} =
  \frac{\text{actions not flagged}}{\text{actions}},
\end{equation}
counting over every run of the cell. Appendix~\ref{app:detector-memory} varies
the count and the window.
```

**Alternatives:**
- (E2) Keep the old detector. Rejected: it is the formula Marc and his supervisor could not read.
- (E3) Drop attack confidentiality and report Zhan's own secondary statistic, the inter-arrival time between actions. Median gap: $c_1$ 31 s, $c_2$ 42 s, $c_3$ 53 s, $c_4$ 26 s, baseline 20 s. It is zero-parameter and cited, but it is attack rate restated, and it loses the only stealth metric the MTD literature names (Zaffarano).

**Blast radius:**
- `analyse.py`: replace `_detector_levels`, `confidentiality_over_run` and the θ median with the count rule.
- `tools/ch5_unopposed_figures.py`: add a Table 5.2 column; `emit_fig_c` retired or re-binned.
- The §5.2 prose (the \prelim 69–93 % and 43 %).
- Appendix C.4 (a real sweep).
- The bib: `jung2004` (Marc's call on placing the PDF in `docs/sources/`).

### Ruling F — the deployment response: one ratio, named for what it counts, and time lost from it. Folds in A.

Why the NCR growth rate fails:
- Its name says NCR, a cell-level end-of-run ratio.
- Its equation takes a derivative of one run's step function.
- The code actually pools counts over live seconds (found in round 2).

**Recommended:** rename it and define it as what the code computes, with the window $I/2$ each side (ruling A):

- **Compromise rate after an MTD deployment:** the attacker's hosts compromised per second in the $I/2$ after a deployment completes, as a percentage of its rate in the $I/2$ before. It is pooled over every deployment of every run in the cell, and a run that has ended adds no seconds. It is 100 when the attacker's pace is unchanged and 0 when it is stopped. It is read beside the same ratio at the same moments on the same seed's run with no defence (pace drifts within a run). Figure 5.3(a, b) draws it in slices of time since the deployment: the drop and the bounce-back Marc described.
- **Time lost per MTD deployment** $= \tfrac{I}{2} \times$ (the ratio with no defence − the ratio under the defence mechanism) / 100. In seconds. The name is the supervisor's form, kept. **This is exactly Bruneau's area**: the integral of $(1 - \text{relative pace})$ over a window is the window times $(1 - \text{its mean})$. The integral, the derivative and the bins leave the definition. Worked example: at 60 % of its earlier rate for the 1 000 s after, where it would be at 100 % with no defence, the attacker loses 400 s.

**Dry run** (2 000 s interval, $I/2$ = 1 000 s each side; `data/results/s45_metric_redesign/rate_ratio.py`). It reproduces the "$I/2$, one slice" column of ruling A exactly:

| cell | rate before (hosts/h) | ratio under defence | ratio, no defence | time lost (s) |
|---|---|---|---|---|
| APT, IP shuffle | 1.77 | 0.53 | 1.01 | 475 |
| APT, host topology | 2.15 | 0.57 | 1.01 | 434 |
| APT, complete topology | 2.16 | 0.58 | 1.00 | 423 |
| APT, service diversity | 2.14 | 0.84 | 1.00 | 161 |
| APT, OS diversity | 2.13 | 0.97 | 1.00 | 38 |
| APT, port shuffle | 2.07 | 0.97 | 1.01 | 38 |
| APT, user shuffle | 2.12 | 1.02 | 1.00 | −25 |
| baseline, service diversity | 5.32 | 0.49 | 0.95 | 461 |
| baseline, complete topology | 7.35 | 0.83 | 0.95 | 112 |
| baseline, host topology | 6.86 | 0.86 | 0.94 | 82 |
| baseline, user shuffle | 6.85 | 0.91 | 0.98 | 63 |
| baseline, IP shuffle | 5.11 | 0.92 | 0.94 | 24 |
| baseline, OS diversity | 6.21 | 0.95 | 0.96 | 18 |
| baseline, port shuffle | 5.82 | 0.96 | 0.95 | −4 |

A side benefit: an $I/2$ window is defined at 200 s too, where the fixed 750/1 250 s window was not. That lifts §5.3.1's "read at 2 000 s only".

**Alternative tried and rejected: time to the next compromise after a deployment** (Marc's "time to the next viable tactic"). The dry run is `data/results/s45_metric_redesign/next_compromise.py`.
- With **no defence**, the APT attacker model compromises no host in the 2 000 s after 42 % of deployment moments. Its median wait is therefore about 1 450 s, set by its own slow pace, and under IP shuffle the median is censored beyond the interval.
- The baseline's topology shuffles come out *faster* than no defence (443 s against 510 s). This is the same phase confound that retired the estimator on 2026-09-24 (`disruption.py` docstring).
- The before/after ratio holds each attacker to its own pace, and that is why it survives.

**Proposed tex:**

```latex
\paragraph{Compromise rate after an MTD deployment.}
The compromise rate after an MTD deployment is the attacker's rate of
compromising hosts in the half interval after a deployment completes, as a
percentage of its rate in the half interval before:
\begin{equation}
  \text{compromise rate after an MTD deployment} = 100 \times
  \frac{\text{hosts compromised after} \,/\, \text{seconds after}}
       {\text{hosts compromised before} \,/\, \text{seconds before}},
\end{equation}
counting over every deployment of every run in the cell; a run that has ended
adds no seconds. It is 100 when a deployment leaves the attacker's pace
unchanged and 0 when it stops the attacker. An attacker's pace drifts within a
run with no defence, so the same ratio is read at the same moments on the same
seed's run with no defence.

\paragraph{Time lost per MTD deployment.}
Time lost per MTD deployment is the attack progress one deployment costs the
attacker, in seconds at its own pace:
\begin{equation}
  \text{time lost per MTD deployment} = \frac{I}{2} \times
  \frac{\text{rate after, no defence} - \text{rate after, under the condition}}{100},
\end{equation}
where $I$ is the deployment interval and each rate is the compromise rate after
an MTD deployment. If an attacker compromises hosts at 60\,\% of its earlier
rate for the 1\,000\,s after a deployment, where with no defence it would keep
its rate, the deployment costs it 400\,s. This is the loss of resilience of
Bruneau et al.\ \citep{bruneau2003}, the area between a system's quality after
a disruption and its level before, with the attacker's pace as the quality.
```

**Blast radius:**
- `disruption.py`: `EDGES` becomes interval-relative, and `_time_lost` takes the one-slice form (identical to the ratio).
- `ablation.py` imports it.
- Figure 5.3 (y-axis label; slices kept for the curve only).
- Table C.5, re-based on the split.
- The §5.3.1 numbers (l.~8027–8050) and §5.4's "494 s".
- Table 4.3 and Table 5.1 rows (the name).
- The effectiveness lead-in.

### Ruling G — smaller items, one line each

- **G1. The null condition's name.** Table 5.1 says *no defence*, and §4.5 now uses it only as that condition's name. Marc's "what defence? we're talking about MTD" could re-key it to *no MTD* dissertation-wide (ch5 captions, Table 5.1, generators). **Recommend:** keep *no defence* as the condition name, since it pairs with the ratified *defence mechanism*, and cut every other generic "defence" (done in §4.5).
- **G2. Table 3.2's caption** says "properties of a sophisticated attacker". Marc: "why do we say sophisticated? standardise". **Recommend:** "an APT attacker", the ratified ch3 class term. This is out of this session's scope (ch3), so it is flagged, not changed.
- **G3. Table 5.2 omits the MTTC coverage share** that §4.5 promises. Add a column, "runs with a compromise", or a caption clause. This was carried from the state of play below.
- **G4. A list of symbols:** not recommended. With the equations in named quantities, §4.5 has two symbols ($p$, $k$), each defined where it is used. Knuth's rule of words over shorthand makes a symbol list unnecessary, and Table 4.2 already lists the Petri-net notation.

## State of play (round 2 session, before Marc's second read)

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
