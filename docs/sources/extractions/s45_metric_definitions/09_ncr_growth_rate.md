# 4.5.3 NCR growth rate (`eq:ncr-growth`) — drafting agent 09

## LaTeX

```latex
\paragraph{NCR growth rate.}
We define the NCR growth rate to measure how fast the attacker compromises
hosts around a deployment. It is the derivative of NCR over the run, read
relative to the attacker's rate before a deployment that completes at $t_d$:
\begin{equation}
  g(t) = \frac{\mathrm{d}\,\mathrm{NCR}_r(t)}{\mathrm{d}t},
  \qquad
  \tilde{g}(t) = \frac{g(t_d + t)}{\bar{g}_{-}},
  \label{eq:ncr-growth}
\end{equation}
where $\mathrm{NCR}_r(t) = |H_r(t)|/N$, with $H_r(t)$ the hosts run $r$ has
compromised by time~$t$; in $\tilde{g}$, $t$ is the time since the deployment
completed, and $\bar{g}_{-}$ is the rate over the 750\,s before it.
$\mathrm{NCR}_r$ rises in steps of $1/N$, one per compromise, so $g$ is
estimated in 125\,s bins $[t, t + 125)$, pooled over every deployment of every
run in $\mathcal{R}$:
\begin{equation}
  \hat{g}(t) =
  \frac{\sum_{(r,\,t_d)} \bigl[\mathrm{NCR}_r(t_d + t + 125) - \mathrm{NCR}_r(t_d + t)\bigr]}
       {\sum_{(r,\,t_d)} \ell_r(t_d + t)},
  \label{eq:ncr-growth-est}
\end{equation}
where $t$ steps from $-750$ to $1\,125$\,s, $\ell_r(t_d + t)$ is the part of
the bin, in seconds, before run $r$ ends, and $\bar{g}_{-}$ is the same ratio
over $[t_d - 750, t_d)$. A run that has ended because its target fell therefore
adds no time, and does not read as a stalled one. $\tilde{g}$ is 1 at the
attacker's pace before the deployment, below 1 while the deployment slows it
and above 1 if it catches up; Chapter~\ref{ch:experiments} reads it as a
percentage. Only deployments that complete at least 750\,s into a run count,
since an earlier one has no full window before it; that window includes the
time the deployment itself runs. NCR and NCR reduction read how much of the
network the attacker holds when its run ends; the growth rate reads its pace in
the minutes around one deployment, where a response to the defence can be read
(Section~\ref{subsec:aio-disruption}). Normalising by the attacker's own rate
keeps a slower attacker from reading as a damaged one. The form is the
resilience curve of \citet{bruneau2003}, a system's performance after a
disruption as a percentage of its level before, which \citet{kott2021} carry to
cyber resilience; here the performance is the attacker's. The window assumes
deployments at least 2\,000\,s apart: at a shorter interval it spans several
deployments, and the rate before is itself disturbed.
```

Prose: 330 words by `wc` with the display equations removed (inline maths and LaTeX commands counted), so about 290 words of prose; 11 sentences.

## Structure

- **S1+S2 merged** into the opening sentence ("We define … to measure …"), the corpus's introduced form (Sharma: "We propose a … metric for measuring …").
- **S3** is carried twice, because Marc asked for calculus and the code computes a discrete estimate:
  - Eq. `eq:ncr-growth` gives the definition, the derivative and its normalised form;
  - Eq. `eq:ncr-growth-est` (a new label) gives the estimator the code computes.
  - The estimator is a finite difference of NCR over live time. It is the discrete analogue of the derivative, and it is written only in shared symbols plus $\ell_r$.
- **S4.** The range and direction of $\tilde g$ (1 is the pace before the deployment; values run from 0 upward). The percentage reading licenses Figure 5.3's axis.
- **S5.** Two edge cases:
  - a run that ended adds no time;
  - a deployment needs a full 750 s before it.
- **S6, introduced:**
  - what no cited metric captures (end-of-run NCR, against the pace around one deployment);
  - the rationale for normalising (the tex slot's own clause);
  - the source of the form (the resilience curve; Bruneau, Kott & Linkov);
  - one limitation (the window's assumption about the deployment interval).
- **Length.** 11 sentences, inside the introduced budget of 8–15.
- **Possible cuts if Marc wants it tighter:**
  - the "run that has ended" sentence could move to 4.5.4;
  - the "keeps a slower attacker" sentence could merge into the S4 sentence.
- **Not included:**
  - the placebo (time lost owns it);
  - the 750/1 250 s rationale beyond one clause (time lost owns the 1 250 s end);
  - statistics;
  - results.

## Verification

| Claim | Source and locator | Verbatim quote | Verdict |
|---|---|---|---|
| The form (performance over time after a disruption, as a percentage where 100 % is no degradation) is a resilience curve. | Bruneau & Reinhorn 2006, *Overview of the Resilience Concept*, Proc. 8th U.S. NCEE, Paper 2040, p. 1 (open access, eng.buffalo.edu; read in full from the PDF). It relays Bruneau et al. 2003. | "a measure, Q(t), which varies with time, can be defined to represent the quality of the infrastructure … performance can range from 0% to 100%, where 100% means no degradation in quality and 0% means total loss." | holds, through the 2006 relay. The 2003 original is paywalled (SAGE): **to download**. |
| The dip-and-recover shape is Bruneau's (this anchors time lost more than this metric). | same, p. 2, Eq. 1 | "community earthquake loss of resilience, R … can be measured by the size of the expected degradation in quality … over time (that is, time to recovery). Mathematically, it is defined by: R = ∫_{t0}^{t1} [100 − Q(t)] dt"; Fig. 1 is captioned "(Bruneau et al. 2003)" | holds. Time lost, Eq. `eq:time-lost` $= \int (1-\tilde g)\,dt$, is this integral on the ratio scale. **Tell the time-lost agent.** |
| Cyber resilience uses a functionality curve normalised by its level before the event. | Kott & Linkov 2021, *To Improve Cyber Resilience, Measure It*, IEEE Computer 54(2) 80–85; arXiv:2102.09455 preprint, p. 2 | "a more resilient system would exhibit a greater area under the curve (AUC) – the integral of retained system functionality F(t) over the total mission time Tm. If so, we might try to define the resilience quantity as R = (AUC)/(F(0)*Tm)" | holds (preprint wording; confirm against the published version) |
| Resilience applies to the attacker's side too. | Kott & Linkov, arXiv p. 2 | "Ironically, impressive examples of cyber resilience may come from malware operations. For instance, the notorious TrickBot … has demonstrated an agile and effective recovery after competent malware-fighting organizations attempted to dismantle the botnet" | holds. It licenses "here the performance is the attacker's". |
| No field metric exists for the attacker's pace or recovery around a disruption, so "introduced" is honest. | `docs/sources/extractions/mtd_metric_catalogue.md` l.37 and l.59 | "Time from a disruption to the attacker's next compromise (*recovery time*) \| **Does not exist attacker-side** … mean time to recovery (**MTTR**) is defender-side"; "No field metric for attacker behavioural variety, disengagement or recovery." | holds |
| NCR is the base quantity. | Table 4.3; the NCR entry | (NCR's agent carries the Zhang / Ho quotes) | not re-verified here |

**Code check** (`data/results/ch5_defended/disruption.py`; the figure is drawn by `tools/ch5_disruption_figure.py`):

| Term | Code | Verdict |
|---|---|---|
| $\mathrm{NCR}_r(t)$ steps once per host compromised | l.87–90: the movement arm's compromise records (`COMPROMISE` set, time `x[8]`) and the baseline's records with a host (`x[3]`). A read-only check over 3 001 runs: the event count equals `compromised` in every run (2 393 / 2 393 and 608 / 608), so there is one step per host. | matches |
| $t_d$ = completion | l.96, `e[2]` = `finish_time` (`run_corpus.py:157`, `analyse.py:155`) | matches |
| 125 s bins, $t = -750 \dots 1\,125$ | l.67, `EDGES = np.arange(-750, 1251, 125)`: 16 bins | matches |
| Numerator: the rise in NCR in the bin | l.118–120: compromises in `[lo, hi)`; one at the run's last instant is counted in the bin ending there. The $1/N$ is omitted, and it cancels in $\tilde g$. | matches up to the $1/N$ constant |
| $\ell_r$ = the seconds of the bin before run $r$ ends | l.111–113: `lo, hi` clipped to `[0, T]`, and `den += hi - lo`. `T` = `termination_time` | matches. **Not $T_r$** (see Symbols). |
| Sums over every deployment and every run of the cell | l.108 loops over the landings; l.148 sums over the runs. This is a ratio of sums. | matches |
| Which deployments: completion ≥ 750 s and < end | l.96, `-EDGES[0] <= e[2] < T` | matches ("at least 750 s into a run") |
| $\bar g_-$ = the same ratio over $[t_d-750, t_d)$ | l.134 and l.149: `num[PRE].sum()/den[PRE].sum()` | matches. It is the pooled ratio over the whole window, **not** a mean of the six bin rates, which the tex slot's "mean rate over" could suggest. |
| $\tilde g$ as a percentage | l.135: `100 * (num/den) / pre` | matches (×100) |
| The cell $\mathcal{R}$ | l.183–184: one arm and one interval, over one mechanism (per-mechanism reads, which Figure 5.3 (a)/(b) draws) **or** over a layer or all seven (the pooled reads, which feed body sentences) | matches for the figure. A per-layer read pools three cells (see For elsewhere). |

**Status check.**
- "Introduced" is honest for the quantity. No MTD source reads the attacker's compromise rate around a deployment (the catalogue confirms it).
- The form is conventional: a performance curve normalised to its level before the disruption (Bruneau 2003, through the 2006 relay; Kott & Linkov 2021).
- So the defensible wording is the one NCR reduction uses: the quantity is ours, "in the form of" a cited one.
- The name keeps NCR's meaning (Zhang, Ho): hosts compromised over $N$. "Growth rate" is the plain absolute rate $d/dt$. It is **not** the per-capita (logarithmic) growth rate of population biology or epidemiology. The equation fixes the reading.

## Symbols

- **Used from the shared set:**
  - $r$ and $\mathcal{R}$;
  - $N$;
  - $H_r$, extended to $H_r(t)$, the hosts compromised by time $t$; $H_r$ is $H_r(t)$ at the run's end, and the NCR agent should confirm this reading;
  - $t_d$.
- **New:**
  - $g$, $\tilde g$, $\hat g$, $\bar g_-$: the growth rate, its relative form, its estimate, and the rate before;
  - $\ell_r(\cdot)$: live seconds in a bin.
- **Why $g$ and not $r$ (the draft's letter):**
  - $r$ is the run in the shared notation, and Eq. `eq:ncr-growth-est` needs both the run and the rate in one line;
  - $g$ is the conventional letter for a growth rate in economics (the ecological $r$ is the per-capita rate, which this is not);
  - the alternative, Newton's $\dot{\mathrm{NCR}}$, introduces no letter but makes $\tilde{\dot{\mathrm{NCR}}}$ and $\bar{\dot{\mathrm{NCR}}}_-$ unreadable.
- **Collision check.** A grep of the uncommented `dissertation.tex` finds 0 hits each for `\$g`, `g(t`, `\hat{g}`, `\ell`, `\mathcal{D}`, `\$u`, `H(t`, `H_r`, `r(t`. `tab:gspn-notation` has no $g$ or $\ell$.
- **Avoided on purpose:**
  - $b$ for a bin: App. B.6 uses $b$ for a tactic (l.8435–8441, $\Delta = s(b)-s(a)$);
  - $n_r$ for a count: relative tactic occurrence's draft uses $n_r(p)$ (tex l.5443);
  - $\Delta t$: $\Delta$ is App. B.6's phase offset. (NCR reduction's draft $\Delta_{\mathrm{NCR}}$ meets the same clash; tell its agent.)
- **$t$ is used as an offset in $\tilde g(t)$ and $\hat g(t)$, and as absolute time in $g(t)$.** The where-clause says so. The alternative is a new offset letter $u$, which is free.
- **Units:**
  - $g$ is a share of the network per second;
  - $\tilde g$ has no unit, since $N$ and the unit cancel;
  - `disruption_numbers.json` reports `pre_rate_per_ksec` in **hosts per 1 000 s**, which is $1000\,N\,\bar g_-$, not $\bar g_-$.
- **$T_r$ must not be used for the run's end here.**
  - $T_r$ (attack rate's active time) runs to the last record's end (`ch5_s531_unopposed/analyse.py:351`).
  - The live time here runs to `termination_time`.
  - For the baseline attacker these differ by a median of 2 041 s: 563 of 608 runs sampled (92.6 %) differ by more than 1 s. For the model they are equal.
  - So "before run $r$ ends" is stated in words.

## For elsewhere

- **Time-lost agent:**
  - rename $r$, $\tilde r$ and $\bar r_-$ in `eq:time-lost` to $g$, $\tilde g$ and $\bar g_-$;
  - $\int_0^{1250}(1-\tilde g)\,dt$ is evaluated on the same bins ($\sum_{t\ge0} 125\,(1-\tilde g(t))$, `disruption.py:138–142`);
  - Bruneau's $R=\int[100-Q(t)]\,dt$ (quoted above) is a direct precedent for its area. That may make time lost "in the form of Bruneau et al. 2003", not purely introduced.
- **§4.5 opener and 4.5.4:**
  - the opener's "each is read per run" is false for this metric, which is pooled over deployments and runs as a ratio of sums (and it is equally false for relative tactic occurrence, APV and time lost);
  - 4.5.4's table already tags it "pooled over deployments";
  - the opener should say "read per run, or pooled where stated".
- **Table 4.3 Source cell.** "introduced here" is honest. More defensible: "introduced here, in the form of \citep{bruneau2003}", parallel to NCR reduction's row.
- **Chapter 5 §5.3.1:**
  - the per-layer and pooled reads (`host`, `service`, `all` in `disruption.py:183`) pool deployments across several conditions, which is more than one cell $\mathcal{R}$; a body sentence that quotes a per-layer curve must say it pools the layer's mechanisms;
  - the 200 s interval: per the limitation sentence, the curve there has a disturbed rate before, so a 200 s reading should be framed as such (or not quoted as a growth-rate curve);
  - any "rate before … per 1 000 s" in the body is hosts, not NCR.
- **Tex comment correction.** The holder comment says the deployment runs "70–100 s". `disruption_numbers.json` medians at 2 000 s are 20 s (user shuffle) to 110 s (complete topology). The draft says "the time the deployment itself runs" with no number.
- **The tex slot says "the mean rate over [t_d − 750, t_d)".** The code takes the pooled ratio over the window, not a mean of bin rates. The draft's "the same ratio over" is exact.
- **Bib:** add `bruneau2003` and `kott2021`; see Open.

## Open for Marc

1. **Rate symbol $g$** in place of $r$, which collides with the run. Recommend $g$. The alternative is $\dot{\mathrm{NCR}}$.
2. **Status wording:** "introduced here", or "introduced, in the form of Bruneau et al. 2003". Recommend the latter, in both Table 4.3 and the prose (the draft already cites the form).
3. **Bruneau et al. 2003** (*Earthquake Spectra* 19(4) 733–752, doi 10.1193/1.1623497) is paywalled: **to download**, then confirm Fig. 1 and the $R$ integral in the original. Alternatively cite the open-access Bruneau & Reinhorn 2006 relay, which was read. Recommend downloading and citing 2003.
4. **Bib entries:**
   - `bruneau2003`: Bruneau, Chang, Eguchi, Lee, O'Rourke, Reinhorn, Shinozuka, Tierney, Wallace, von Winterfeldt, "A Framework to Quantitatively Assess and Enhance the Seismic Resilience of Communities", *Earthquake Spectra* 19(4):733–752, 2003;
   - `kott2021`: Kott & Linkov, "To Improve Cyber Resilience, Measure It", *IEEE Computer* 54(2):80–85, 2021 (arXiv:2102.09455).
   - Recommend adding both, and confirming Kott's quoted wording in the published version.
5. **Second display** `eq:ncr-growth-est` for the estimator. Recommend keeping it, since the code computes the estimate and Marc asked for how it is estimated. The alternative is to fold it into words.
6. **Which limitation to print:** the window's 2 000 s assumption (drafted), or the pooled curve being diluted by deployments that never reach the attacker (every completion counts, by design). Recommend the drafted one, because chapter 5 reads 200 s.
