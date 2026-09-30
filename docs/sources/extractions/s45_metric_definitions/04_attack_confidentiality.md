> **Superseded in part 2026-09-29:** the detector this record verifies (an exponentially fading count, κ = 60 s, alarm at half the baseline) was replaced by a count of actions in a 60 s window, alarm at the baseline's median count (ruling C, handoff 2026-09-29_s45_equation_clarity.md; evidence record 14).

## LaTeX

```latex
\paragraph{Attack confidentiality.}
Attack confidentiality, adapted from \citet{zaffarano2015}, measures ``how much
attacker activity may be visible by detection mechanisms'' as the share of the
attacker's actions a detector does not expose. Zaffarano et al.\ mark a task
exposed when its information is visible in plaintext in network traffic; MTDSim
encodes no detection (Section~\ref{subsec:defence-mechanisms}), so exposure
here is judged by a declared \emph{detector}, a rate alarm of the kind an
attacker evades by slowing \citep{jafarian2015, ward2018}. At each of the
attacker's actions the detector counts that action and those before it, each
fading with the detector's memory $\kappa$:
\begin{equation}
  D_r(j) = \sum_{i=1}^{j} e^{-(a_j - a_i)/\kappa},
  \label{eq:detector}
\end{equation}
where $a_1, a_2, \dots$ are the start times $A_r$ of run $r$'s actions and
$\kappa = 60$\,s, so an action counts one when taken and about a third a minute
later. $D_r(j)/\kappa$ is the action rate as an exponentially weighted moving
average, the statistic intrusion detectors hold against a threshold
\citep{cisar2010ewma}. Action $j$ is exposed when $D_r(j)$ reaches the
\emph{alarm level}~$\theta$, and attack confidentiality is the share not
exposed:
\begin{equation}
  \text{attack confidentiality}(b) =
  \frac{\sum_{r \in \mathcal{R}} \lvert \{\, j : a_j \in b,\ D_r(j) < \theta \,\} \rvert}
       {\sum_{r \in \mathcal{R}} \lvert \{\, j : a_j \in b \,\} \rvert},
  \label{eq:confidentiality}
\end{equation}
where $b$ is a 1\,500\,s bin of the run and the actions are pooled over the
runs $\mathcal{R}$. The alarm level is tuned on the baseline attacker: $\theta$
is the median of $D_r(j)$ over all its actions with no defence running
($\theta \approx 2.95$, about three actions a minute), so the alarm flags half
of them by construction. Attack confidentiality takes values in $[0, 1]$, and
lower is better for the defender. The reading is bounded to a detector that
counts actions; one that counts time on the network would read a slower
attacker the other way, since ``the longer the attack takes, the more likely it
will be detected'' \citep[p.~40]{hong2018}. Appendix~\ref{app:detector-memory}
moves $\kappa$ and the share of the baseline attacker's actions the alarm flags.
```

**Words:** about 280 of prose (equations and citations excluded), in ten sentences with two "where" clauses. That is over the adapted budget. The brief allowed 6–9 sentences for this metric because the detector has to be declared. About 110 words are the metric itself (sentences 1–2, the exposure sentence, the range sentence). The rest declares the detector, the alarm rule and the bound. Syntax checked in a scratch compile (0 errors); the full thesis was not built.

**Cuttable, in order, if Marc wants it shorter:** the Hong quote (keep the citation: −13 words); the gloss "so an action counts one … a minute later" (−13); the EWMA sentence (−22, but it is the only thing that makes the detector conventional; see Open 2).

## Structure

| Slot | Used | Where |
|---|---|---|
| S1 name, status, cite | yes | sentence 1: "adapted from \citet{zaffarano2015}", with Zaffarano's own definition quoted |
| S2 what it measures | merged into S1 | "as the share of the attacker's actions a detector does not expose" |
| S6 what differs, and why | moved up to sentence 2 | the difference (Zaffarano's plaintext-exposure rule against no detection in MTDSim) is also the reason a detector must be declared, so it comes before the detector |
| rationale for a *rate* detector | tail of sentence 2 | one clause with two held citations (brief (e)) |
| S3 operation, equations | sentences 3–5 | `eq:detector` (the detector), then the EWMA identity that makes it conventional, then the exposure rule and `eq:confidentiality` |
| S5 when read, and the alarm rule | the "where b" clause and sentence 6 | 1 500 s bins, pooled over runs; θ is the median over the baseline attacker's actions, with its consequence (one half by construction) stated |
| S4 range and direction | sentence 7 | [0, 1], lower better for the defender |
| limitation (brief (d)) | sentences 8–9 | bounded to a detector that counts actions; Hong's time-at-risk rationale runs the other way; the appendix sweep |

I dropped nothing from the template. I merged S2 into S1 and moved S6 forward because it motivates the detector. Following voice §c5, the concession (the Hong bound) comes in the same paragraph as the claim it limits. No results appear in the paragraph. θ ≈ 2.95 is included as a worked value: $D$'s scale is not intuitive, and "about three actions a minute" is what makes θ readable. It is a calibration constant, not a result, and it moves with the 1 000-seed run (Open 4).

## Verification

| # | Claim | Source, locator | Verbatim quote | Verdict |
|---|---|---|---|---|
| 1 | Zaffarano's attack confidentiality is "how much attacker activity may be visible by detection mechanisms" | `docs/sources/lit_review/zaffarano2015.md` l.344–345; PDF p. 9 (printed), Table 4 | "Attack Confidentiality is a measure of how much attacker activity may be visible by detection mechanisms" | holds |
| 2 | Zaffarano compute it as the share of tasks left unexposed | same, §4.3, p. 10 (formula) and §3.2, p. 7 (attribute) | "Confidentiality(M,ν) = 1/\|T\| Σ_{τ∈T} ν(τ, unexposed)"; "unexposed: whether task information was exposed, values are 0 (information was exposed) and 1 (information was not exposed)" | holds. The formula is written "for a mission model M"; the attacker case is "computed similarly … with the same type of costs and benefits". Zaffarano's attacker tasks are "the types of actions an attacker would perform" (§3.2), so task ↔ action is a fair mapping |
| 3 | Zaffarano's exposure rule is plaintext visibility in network traffic | same, §4.3, p. 10 | "in these initial experiments, we simply refer to whether information is visible in plaintext in network traffic" | holds |
| 4 | Cho 2020 relays it (brief's status line) | `lit_review/1_1_cho2020toward.md` l.603–605; §VII-A, p. 728 | "attack confidentiality means the degree of attack behaviors detected by a defender" | holds as a relay, but with the **direction inverted** ("detected", where Zaffarano's formula counts the *unexposed*). Cho files it under the defender's system-security metrics. It is not cited in the paragraph (see For elsewhere) |
| 5 | MTDSim encodes no detection | `dissertation.tex` l.886–888 (§2, `subsec:defence-mechanisms`) | "no detection channel is encoded, so a detection-triggered strategy, such as an IDS-based scheme, is not possible" | holds |
| 6 | A rate threshold is evaded by slowing | `docs/sources/methodology/ward2018_mit_survey.md` l.11893–11894, §5.18 Düppel, p. 236; the threshold is at p. 234 | "An attacker could avoid triggering Düppel to switch from sentinel to battle mode by slowing the rate of attack."; "If the number of preemptions exceeds 10 per millisecond, Düppel assumes a side-channel attack … is in progress" | holds. Düppel is a rate-threshold detector in the MTD survey itself (a host side channel, not network actions); the thesis sentence claims only "a rate alarm … evaded by slowing" |
| 7 | Fast scanning is easy to detect | Jafarian 2015, `tactic_profiles/step_d/10_disc/An_Effective_Address_Mutation_Approach_for_Disrupting_Reconnaissance_Attacks.pdf`, PDF p. 10 = p. 2571, §VII | "we focus on scanners/worms with low scanning rates, since fast scanning is easy to detect [4]" | holds. ~~The sentence is missing from the `.md` conversion~~ (corrected 2026-09-29, record 14: it is in the markdown at l.289); it is read from the PDF (the census quoted it correctly) |
| 8 | APT "low and slow" (brief (e); not used in the paragraph, available) | `lit_review/2_3_alshamrani2019survey.md` l.51; §II-A, p. 1852 | "They plan for the use of several evasive techniques to elude detection by their target's intrusion detection systems. They follow "low and slow" approach to increase the rate of their success." | holds for "low and slow". **"Trades speed for evasion" is not Alshamrani's wording**: it is ch2's paraphrase (l.1221) and must not be quoted |
| 9 | $D/\kappa$ is an EWMA of the action rate, the statistic intrusion detection thresholds | Čisar, Bošnjak & Maravić Čisar 2010, IJCCC 5(2):160–170, abstract and Eq. 1, p. 160 (open access, read: univagora.ro …/ijccc/article/download/2471/938) | "Many intrusions manifest in changes in the intensity of events occuring in computer networks. Because of the ability of exponentially weighted moving average (EWMA) control charts to monitor the rate of occurrences of events based on their intensity, this technique is appropriate for implementation in control limits based algorithms."; "EWMA_t = λY_t + (1 − λ)EWMA_{t−1} … 0 < λ ≤ 1 is a constant that determines the depth of memory of the EWMA" | holds, with one step of mine. The identity is my derivation: bin the actions at width Δ, set λ = 1 − e^{−Δ/κ}, and as Δ → 0 the EWMA of per-bin counts is (Δ/κ)·D. Checked numerically: D = 4.6583 against the limit 4.6582. So D/κ is the EWMA *rate*. The primary source for EWMA in intrusion detection is Ye, Borror & Zhang 2002 (paywalled; Open 2) |
| 10 | A detector counting time on the network reads a slower attacker the other way | `lit_review/1_2_hong2018dynamic.md` l.305–307; §5.1.5 "Time: duration", p. 40 (PDF-confirmed) | "The amount of time taken for the attacker to compromise each stepping stone in an attack path is another significant factor, as the longer the attack takes, the more likely it will be detected." | holds (the rationale for Hong's ACD, Eq. 9) |
| 11 | Appendix `app:detector-memory` exists and moves both κ and the alarm | `dissertation.tex` l.8731–8738 | "rests on two choices: how long the detector remembers an action, 60 s, and where its alarm is set … This section moves both" | holds (the section is still a placeholder; the sweep is owed, handoff Open 3) |

**Is there a conventional name for the detector? (brief (b))** Yes, in family. $D_r/\kappa$ is exactly the continuous-time exponentially weighted moving average of the action rate, and a threshold on an EWMA of event intensity is an established intrusion-detection technique (row 9). The exact form, a sum of exponential kernels over event times, appears in no security source I read. It is the event-time limit of the discrete EWMA, which I derived and checked numerically, so it is not quoted from a source. Other names for this family (leaky integrator, Hawkes-type exponential kernel, exponentially time-decayed count as in Cormode et al. 2009) are real but outside intrusion detection, so none is cited. I invented no name. The prose says "a rate alarm" and "exponentially weighted moving average" and adds no acronym.

**Code check** (`data/results/ch5_s531_unopposed/analyse.py`. The metric is computed there, **not** in `ch5_defended/analyse.py` as the brief lists. The `ExposureCurve` in `measures.py` §9, l.1498ff., is the older tier-weighted detector and is not used.)

| Term | Code | Verdict |
|---|---|---|
| actions $A_r$: start times, action-bearing records with an action and not blocked; the baseline attacker's consecutive exploit rows collapsed | `_actions_movement` l.349–358; `_actions_baseline` l.361–368 | matches (the attack rate draft owns the rule) |
| $\kappa = 60$ s | `TAU = 60.0` l.338 | matches |
| $D_r(j) = \sum_{i \le j} e^{-(a_j - a_i)/\kappa}$, the action counting itself | `_detector_levels` l.394–401: `d = d·exp(−(t − last)/TAU) + 1.0`, level recorded after the +1 | **matches exactly in the index form.** The brief's time form $D(t) = \sum_{a_i \le t}$ **mismatches on ties**: 37 of the baseline attacker's 29 416 actions share a start time with the previous one. The code counts them in record order (the first does not count the second); the time form counts both at both. The APT attacker model has no ties. So I wrote the equation in the index form. Hand trace: actions at 0, 30, 60, 200 s give D = 1, 1.607, 1.974, 1.191, identical from the code and the formula |
| exposed iff $D_r(j) \ge \theta$; the share uses $D < \theta$ | l.413 `d < theta` | matches |
| $b$: 1 500 s bins $[t_0, t_0 + 1500)$ from 0 to 15 000 s (10 bins) | `BIN = 1500.0` l.391; `edges = np.arange(0, CORE + BIN, BIN)`, `lo <= t < hi` l.409–413; `CORE = 15_000` l.63 | matches |
| pooled over runs (a ratio of sums) | l.413–414: one list across every run, then `np.mean` | matches `eq:confidentiality`. (The full-run curve `confidentiality`, from `_confidentiality_curve` / `_curve_summary` l.369–388, is a *mean of per-run shares* over θ ∈ {1.0, …, 6.0}. It is a different estimator and is not what the figure draws.) |
| θ = median of D over all the baseline attacker's actions, no defence, pooled | l.784–785: `np.median` over every action of `baseline[CORE]` | matches. θ_b = 2.9488 over 100 runs and 29 416 actions. The share below it is exactly 0.500 (no ties at the median), so "one half by construction" holds |
| the same θ applied to every APT profile | l.786–788 | matches |

Read-only checks: `scratchpad/s45/chk_conf.py` and `chk_ties.py`. The pooled whole-run shares at θ_b are $c_1$ 0.765, $c_2$ 0.866, $c_3$ 0.913, $c_4$ 0.702, $c_{\mathrm{agg}}$ 0.798 and baseline 0.500. These are for chapter 5, not the definition.

**Status check.** "Adapted" is honest, not "introduced under Zaffarano's name". The quantity is Zaffarano's formula, (1/|T|)·Σ ν(τ, unexposed): a share of attacker tasks unexposed. It is used with Zaffarano's name and direction (higher means more hidden). Only the exposure valuation ν is replaced, and Zaffarano's framework leaves that valuation to the experimenter ("In principle, there are many ways in which information could be exposed"). This is the smallest adaptation in §4.5. Two further differences are reading choices, not changes to the quantity, so the paragraph leaves them out. First, Zaffarano read the with-minus-without-MTD difference; this thesis compares two attackers with no defence. Second, the reading is taken in time bins.

## Symbols

| Symbol | Status | Note |
|---|---|---|
| $r$, $\mathcal{R}$, $A_r = (a_1, a_2, \dots)$ | shared (brief) | $A_r$ is the attack rate draft's; I restate "the start times" in the "where" clause so the index form reads |
| $j$, $i$ | new, running indices | action indices within a run. $i$ is unused as a named symbol in ch4 |
| $D_r(j)$ | new (the brief's $D$, with run subscript and index argument) | `\$D` has no live use in the tex (grep: 0 live lines; ch4 uses $d$ for the distance kernel, which is distinct in case). The index form is forced by the tie finding |
| $\kappa$ | owned (brief) | 0 live uses of `\kappa` in the tex or tables |
| $\theta$ | owned (brief) | 0 live uses of `\theta`. Jafarian uses θ for mutation rate, but that is only in the source and never printed in the thesis |
| $b$ | new | a time bin. It is free as a bare symbol (ch4 has none); the NCR growth draft uses bins too, so align the letter if it names one |
| $\text{attack confidentiality}(b)$ | the metric's name in the equation, following Zaffarano's own word-as-function notation ("Confidentiality(M,ν)") and the NCR reduction draft's `\text{NCR reduction}` | no letter invented (C is taken in spirit by attack cost, AC) |

Collision grep: the `tab:gspn-notation` reserved set ($c, \mathcal{N}_c, p, \hat p, \tau_p, t_{pq}, \mu_p, w_c, \sigma, M_0, v, F_v, \varphi, R, d, \gamma, \delta, z$) is untouched. `\theta`, `\kappa`, `\mathbb{1}` and `A_r` have 0 live occurrences in `dissertation.tex` or `tables/*.tex`. $e$ is Euler's number here, and ch4 prints no $e$ as a symbol.

## For elsewhere

- **§4.5.1 opener / attack rate:** must define *action* (the ruled term; *verb* is DEPRECATED 2026-09-25, `terminology.md` row "six inherited operations") and $A_r$ as start times, **in record order**. This paragraph relies on both.
- **§4.5.4:** say that attack confidentiality is reported as a **pooled share per bin with no interval**, and that the whole-run reading is a ratio of sums. If the body quotes the $c_4$ first-bin margin (4.6 pp, bootstrap 1.1–8.3, appendix comment l.8741), 4.5.4 must declare that bootstrap.
- **Table 4.3 source cell:** "adapted from \citep{zaffarano2015}" is correct as it stands. Do not add Cho: his relay inverts the direction.
- **Table 3.1:** it already carries attack confidentiality with Zaffarano (l.2691); nothing is owed.
- **Chapter 5 / stale references:** the float is `fig:aio-stealth`, a separate figure (Figure 5.2 by the generator's docstring), no longer "Figure 5.1(c)". Stale: the brief; handoff entry 4 ("Figure 5.1(c) shows every θ, so none is chosen", superseded by the one-rule θ); `tools/ch5_unopposed_figures.py` `emit_table` docstring ("Figure 5.1(c)'s"). The caption's "alarm tuned so that it flags half of the baseline attacker's actions" matches the definition. **The caption could add** that the baseline attacker's bins sit either side of one half (0.675 in the first bin, 0.41–0.45 later), because one half holds over the whole run. Its runs thin out, from 100 to 30 active runs in the last bin.
- **Chapter 5 body, measurement against attribution (voice §c10):** $D$ is time-denominated, and the APT attacker model's time is its declared dwell $\mu_p$ (§4.4, "a drawn dwell replaces the dispatched action's native cost"). This is the "two clocks" caveat carried in `measures.py` §9 and `stealth_exposure_prereg.md`. So its higher attack confidentiality is a consequence of the declared dwells and of the no-action tactics. The ruled framing ("fewer actions above a rate alarm tuned on the baseline attacker, because much of its campaign is in tactics the simulator gives no network action") carries this; keep it in ch5, not §4.5.
- **Appendix `app:detector-memory`:** sweep κ and the alarm quantile together (θ_b depends on κ). The handoff's Open 5 ablation ("erased the margin" at the minute scale) goes there only if it holds on this detector.
- **Bib:** `cisar2010ewma` is missing (Open 2).

## Open for Marc

1. **Index form of the detector** ($D_r(j) = \sum_{i \le j}$, in place of the brief's $D(t) = \sum_{a_i \le t}$). The time form mismatches the code on 37 tied baseline actions. **Recommend:** accept the index form. It is exact, and it shows the counting-itself convention (the $i = j$ term) in the equation.
2. **Conventional anchor for the detector:** add the bib key `cisar2010ewma`, which I read and verified: Čisar, P., Bošnjak, S. and Maravić Čisar, S. (2010), "EWMA Algorithm in Network Practice", *International Journal of Computers, Communications & Control* 5(2):160–170, doi:10.15837/ijccc.2010.2.2471 (DOI resolves). **To download** (paywalled): Ye, N., Borror, C. and Zhang, Y. (2002), "EWMA techniques for computer intrusion detection through anomalous changes in event intensity", *Quality and Reliability Engineering International* 18(6):443–451, doi:10.1002/qre.493, the primary source. **Recommend:** cite Ye once it has been read and confirmed, keeping Čisar as the held one. If neither is accepted, cut the EWMA sentence, and the detector stands as declared without a precedent.
3. **θ ≈ 2.95 in the text:** it is a corpus-derived constant and moves at 1 000 seeds. **Recommend:** keep it with "about three actions a minute" (it makes $D$ readable), regenerated from `numbers.json` `core.detector.alarm_tuned_to_baseline` at the reported run.
4. **Length (about 280 words against the adapted budget):** **Recommend:** keep for now, since this is the one definition that declares a model component. At pass 5, cut first the Hong quote (keeping the citation), then the κ gloss.
5. **Alshamrani:** dropped from the paragraph (the rate-alarm clause is carried by Jafarian and Ward, which are closer). **Recommend:** leave it to ch2's low-and-slow sentence, and never quote "trades speed for evasion" as Alshamrani's words.
