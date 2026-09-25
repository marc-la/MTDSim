# 02 — Attack path variation (APV), §4.5.1, `eq:apv`

## LaTeX

```latex
\paragraph{Attack path variation (APV).}
Attack path variation (APV) is adapted from \citet[Eq.~2]{hong2018} and
measures how often an attacker's runs begin differently. The
\emph{opening of length~$k$} of a run $r$, written $\pi_k(r)$, is its first
$k$ steps (all of its steps, in a run of fewer than $k$). APV at length $k$
is the share of the runs whose opening differs from the most common one:
\begin{equation}
  \mathrm{APV}_k = 1 - \max_{\pi}\,
  \frac{\lvert\{\, r \in \mathcal{R} : \pi_k(r) = \pi \,\}\rvert}{\lvert\mathcal{R}\rvert},
  \label{eq:apv}
\end{equation}
where $\pi$ ranges over the openings of length $k$ that the runs take.
It is 0 when every run opens alike and at most $1 - 1/\lvert\mathcal{R}\rvert$,
when no two runs do, and it cannot fall as $k$ grows. Hong et al.\ compare
the attack paths available in the network between consecutive network
states, where a lower value means a more static set of paths; here the
paths are the sequences of steps one attacker takes, compared across its
runs, which reads whether the attacker has more than one way to begin.
```

**Words:** about 150 in prose (equation excluded). Five sentences plus the "where" clause: opener (name, status, what it measures), the opening definition (a term this paragraph owns), the operation, range and direction, and the difference clause.

## Structure

| Slot | Used | Where |
|---|---|---|
| S1 name, acronym, status, cited at the name | yes | sentence 1, "adapted from \citet[Eq.~2]{hong2018}" |
| S2 what it measures | yes, merged into S1 | "measures how often an attacker's runs begin differently"; one main clause, authority first |
| Owed term: *opening of length k* | yes | sentence 2; *step* is taken as defined by the relative tactic occurrence paragraph just above |
| S3 operation in words, then equation, "where" clause | yes | sentence 3, Eq. `eq:apv`, "where" clause for the bound $\pi$ |
| S4 range and direction | yes | sentence 4. No defender-good direction is given, on purpose: this is an attacker-behaviour metric read with no defence (see Verification, direction row) |
| S5 edge case | yes, folded into the opening's definition | a run shorter than $k$ opens with all its steps, which is exactly what the code does. Mode ties need no clause because the $\max$ form is the same whichever tied opening is chosen |
| S6 the one difference, and why | yes | last sentence. Three changes are packed into one clause: available paths become taken paths; consecutive network states become runs; host paths become step sequences. The "why" is the clause's tail |
| Worked value | dropped | 0 and the maximum explain the reading; Figure 5.1(b) gives the values |

**Budget:** adapted, 2–4 sentences plus one difference clause, plus the opening definition. That is 4 + 1 sentences, about 150 words. It sits over the ~80-word guide because the opening is defined here. Without sentence 2 it would be about 120 words. The "cannot fall as $k$ grows" clause (8 words) is the first cut if Marc wants it tighter. I kept it because Figure 5.1(b) plots APV against $k$ and every bar rises: the clause tells the reader that rise is a property of the metric, not a finding.

## Verification

### Source claims

| Claim | Source and locator | Verbatim quote | Verdict |
|---|---|---|---|
| Hong names the metric *attack path variation (APV)* | `docs/sources/lit_review/1_2_hong2018dynamic.md` l.231; §5.1.1 "Scanning: path variation", p. 39 (PDF p. 7, checked by text search of `original/1.2_hong2018dynamic.pdf`) | "Hence, the attack path variation (APV) measures the shift in attack paths as the network changes when MTD techniques are deployed." | holds |
| Hong's object is the set of attack paths the network offers in each network state, and the comparison is between network states | same, l.231 and l.235 | "APV captures the change in the set of attack paths between the network states." / "Here, $AP_i$ represents the set of attack paths found in the $i^{th}$ network state." | holds |
| Eq. 1, the per-pair term, is the share of the current state's paths that are new | same, l.237–239, Eq. (1), p. 39 | $\Delta AP_{i,i-1} = \frac{\lvert AP_i - AP_{i-1}\rvert}{\lvert AP_i\rvert}$; "The set of difference from the previous network state to the current one reveals the new attack paths which were not in the previous network state." | holds (equation restored by hand from the PDF, per the file header) |
| Eq. 2 is the mean over consecutive state pairs | same, l.240–243, Eq. (2), p. 39 | $APV = \frac{\sum_{i=1}^{\lvert S\rvert} \Delta AP_{i,i-1}}{\lvert S\rvert - 1}$; "The metric has been normalized by the number of consecutive network state pairs." | holds. Note: the printed index runs $i=1..\lvert S\rvert$ over $\lvert S\rvert-1$ pairs; the worked Eq. 18 sums three terms over four states, so the numerator has $\lvert S\rvert - 1$ terms. Not our concern, but do not re-typeset Hong's Eq. 2 in the thesis without checking the glyph |
| Hong's paths are host sequences | same, l.406, §5.3.1, p. 42 | "$AP_0$ = {(A, h1, h4, h7), (A, h1, h5, h6, h7), …} is the set of attack paths in $s_0$" | holds; this is a third difference (host paths, not step sequences) |
| The reading "lower APV value means the set of attack paths tends to be more static" | same, l.408, **§5.3.1, p. 42** (PDF p. 10) | "Lower APV value means the set of attack paths tends to be more static." | holds, **but the locator is wrong in the handoff and the boilerplate**: the quote is on p. 42 (the worked example), not p. 39. Eq. 2 is on p. 39 |
| Hong's direction for attack-effort metrics is "toward one makes the attack harder" | `metric_census/A_hong.md` l.20, citing §6.1.1, p. 45 (PDF p. 13, found by text search) | "For attack efforts, a metric value toward one is making the attack more difficult" | holds. **This direction does not carry over.** Our APV describes the attacker, with no defence running, so the draft gives no better-for-defender direction |
| Hong's APV is computed analytically from network states, not from a running attacker | `mtd_metric_catalogue.md` l.52 | "attacker-side by framing, but computed analytically from a sequence of network states, not from a running attacker." | holds |
| The evidence catalogue records no field metric for this quantity | `mtd_metric_catalogue.md` l.41 | "Share of runs leaving the commonest opening (Figure 5.1(b)) \| **Does not exist**" | holds. The catalogue predates the 2026-09-24 "adapted" ruling and was not updated; see Open |
| Freeman's *variation ratio* is $1 - f_m/N$, the proportion of cases outside the modal category, a dispersion statistic for nominal data | secondary only: Wikipedia "Variation ratio" (web search 2026-09-25) | "the proportion of cases which are not in the mode category: $1 - f_m/N$" | **partly: primary not read** (Freeman 1965, *Elementary Applied Statistics*, Wiley; to download). Not cited in the draft |

### Code check

The code is `data/results/ch5_s531_unopposed/analyse.py`, **not** `ch5_defended/analyse.py`. APV is read only on the no-defence corpus; `ch5_defended/` and `measures.py` compute no APV. Figure 5.1(b) is drawn by `tools/ch5_unopposed_figures.py` from `ch5_s531_unopposed/numbers.json`.

| Equation term | Code | Verdict |
|---|---|---|
| $\mathrm{APV}_k = 1 - (\cdot)$ | `analyse.py:478–482`, `apv()`: `{k: 1.0 - v for k, v in opening_share.items()}` | matches |
| $\max_\pi \lvert\{r : \pi_k(r) = \pi\}\rvert / \lvert\mathcal{R}\rvert$ | `analyse.py:186–189`, `commonest_opening_share`: `Counter(s[:k] for s in seqs).most_common(1)[0][1] / len(seqs)` | matches. `most_common(1)` returns *a* modal opening; its count is the max, so ties do not change the value. Ties occur (e.g. $c_1$ at $k$=7, 8; $c_{\mathrm{agg}}$ at 7, 8; read-only check) and are harmless |
| $\mathcal{R}$ = the runs of one cell | `analyse.py:234–237` (per profile, `movement[("targeted", CORE, p)]`), `:302–305` (baseline, `baseline[CORE]`); `:776`, `:791` | matches: per attacker and profile, never pooled. Targeted scenario, 15 000 s limit, 100 runs per cell (preliminary) |
| $\pi_k(r)$, first $k$ steps, profiles: a tactic entered | `measures.py:390–393`, `place_sequence` (one entry per record); `analyse.py:236` slices `[:k]` | matches. Read-only check: no profile sequence repeats its predecessor (0 consecutive repeats in all five profiles), so a record is a tactic entered |
| $\pi_k(r)$, baseline: a verb entered, repeats collapsed | `analyse.py:289–292`: `tuple(n for i, n in enumerate(names) if i == 0 or n != names[i - 1])` | matches |
| Run shorter than $k$: opens with all its steps | Python slicing `s[:k]` returns the whole tuple when `len(s) < k` | matches the draft's bracket. Never triggered on this corpus: the shortest run has 76 steps (baseline) or ≥ 160 (profiles), and $k \le 8$ |
| $k$ | `analyse.py:66`, `K_MAX = 8`, computed for $k$ = 1..8; the figure draws 2..8 (`ch5_unopposed_figures.py:194`, "length 1 is zero for every attacker by construction") | matches; $k$ is the metric's argument, no single value is chosen |
| Range $[0, 1 - 1/\lvert\mathcal{R}\rvert]$, non-decreasing in $k$ | follows from the equation: an opening of length $k{+}1$ is shared by no more runs than its own length-$k$ prefix, so the modal count cannot rise with $k$ | holds, and matches `numbers.json` (every series is non-decreasing in $k$; maximum observed 0.99 at $\lvert\mathcal{R}\rvert$ = 100) |

Values reproduced from `runs.jsonl` (read-only) match `numbers.json` `core.metrics.*.apv` exactly.

### Status check: is "adapted" honest, and is the name used as Hong uses it?

**What Hong measures:** how much the set of attack paths *available* in the network (host sequences, from the T-HARM) changes between *consecutive network states* under an MTD. It is the mean share of each state's paths that are new. It is an attack-effort metric of MTD effectiveness: a higher value means the attack is harder.

**What this measures:** how much the step sequences *one attacker takes* differ across its *runs*, over the first $k$ steps, with no defence running. It is a descriptor of attacker behaviour, with no better-for-defender direction.

**What is kept:**
- the plain meaning of the name (variation in attack paths);
- the range in $[0, 1]$;
- Hong's reading, transposed ("lower means more static").

**What changes, in four respects:**
1. Available paths become taken paths.
2. Host paths become tactic or verb sequences.
3. Consecutive states become an unordered set of runs.
4. The metric's role: MTD effectiveness becomes attacker behaviour.

The form changes too: see below.

**Defensible under `literature_conventions.md` §d2?** Only as a *named* divergence. The rule forbids reuse "with divergent semantics silently", and the draft's last sentence names the divergence at the definition site. So it passes the letter of §d2.

The adaptation is at the far edge of "adapted", though. It keeps Hong's name and his idea (a static set of paths is bad, variation is good), and changes almost everything else. The catalogue's own verdict for this quantity is "Does not exist" (l.41). **The supervisor, Dr Jin B. Hong, is the first author of `hong2018`**, so the reader best placed to object is the one who will read it. See Open 1.

**Can the adapted equation keep Hong's form?** Not literally. Hong's form needs an ordering of states and a set of paths per state; runs are unordered and each takes one path.

- **The nearest faithful transposition:** treat each run as a state holding the single path $\{\pi_k(r)\}$. Hong's per-pair term becomes $\mathbb{1}[\pi_k(r) \ne \pi_k(r')]$, and averaging over all pairs (runs have no "consecutive") gives the share of run pairs whose openings differ, $1 - \sum_j n_j(n_j-1)/(\lvert\mathcal{R}\rvert(\lvert\mathcal{R}\rvert-1))$ (the Gini–Simpson index).
- **The modal form is the code's:** $1 - \max/\lvert\mathcal{R}\rvert$, Freeman's variation ratio.
- **Where they agree and differ:** both are 0 when every run opens alike. The pairwise form saturates faster (≥ 0.96 for $c_1$, $c_2$, $c_4$, $c_{\mathrm{agg}}$ at $k \ge 5$), so it loses resolution across $k$.
- **They order $c_3$ against the baseline attacker differently at $k$ = 5 and 6.** Modal: 0.20 against 0.22. Pairwise: 0.36 against 0.35. Both margins are negligible (read-only check on the 100-run corpus). No other ordering changes.

**Recommendation:** keep the modal form (what the code and figure compute). Say "adapted", naming the difference. Optionally cite Freeman for the form once the primary text is held.

## Symbols

| Symbol | Status | Note |
|---|---|---|
| $r$, $\mathcal{R}$, $k$ | shared (brief) | used as defined |
| $\pi_k(r)$ | **new**, proposed in the boilerplate | run $r$'s opening of length $k$. $\pi$ is the conventional letter for a path. Collision check: `grep '\\pi' dissertation.tex` finds only the commented boilerplate (l.5455–5456); `tab:gspn-notation` has no $\pi$. One caution: GSPN texts conventionally use $\pi$ for the steady-state distribution. The thesis never computes one (`grep -i 'steady.state\|stationary'`: no live hits), so there is no clash inside the document. Alternative: Hong's own path symbol $ap$ (his $ap_j$), e.g. $ap_k(r)$, which would tie the notation to the source but is a two-letter italic |
| $\pi$ (bound, under $\max$) | new | ranges over the openings the runs take; stated in the "where" clause |
| $\mathrm{APV}_k$ | new | the subscript makes $k$ an argument; the figure's axis already reads "opening length $k$" |

The boilerplate's $\pi_k^{*}$ ("the commonest") is dropped: the $\max$ form avoids defining a modal opening that is not unique under ties.

## For elsewhere

- **§4.5.1 opener / relative tactic occurrence:** the draft assumes *step* is defined in the paragraph before it (a tactic entered; for the baseline attacker a verb entered, consecutive repeats collapsed). If the step definition moves into the 4.5.1 opener, nothing here changes.
- **4.5.4:** APV is a share over the runs of a cell, reported without an interval in Figure 5.1(b). 4.5.4's "which statistic applies" table lists it as "shares pooled over runs". *Pooled* here means over runs within one attacker and profile, never across profiles. Check 4.5.4 says "per cell".
- **Table 4.3:** the Source cell "adapted from \citep{hong2018}" is consistent with the draft.
- **Figure 5.1 caption / §5.2:**
  - the figure starts at $k$ = 2 because $\mathrm{APV}_1 = 0$ for every attacker (every run's first step is the same: reconnaissance for the profiles, `SCAN_HOST` for the baseline attacker). This is a construction fact the body text or caption may want in one clause, so no reader hunts for the missing $k$ = 1;
  - $c_{\mathrm{agg}}$ has APV values in `numbers.json` but is not drawn; that is fine, but the body text should not quote it without a figure behind it.
- **Handoff and boilerplate locator:** "APV, Eq. 2, p. 39: 'lower APV value means…'" conflates two pages. Eq. 2 is p. 39; the quote is §5.3.1, p. 42.
- **Handoff and brief code pointer:** APV lives in `data/results/ch5_s531_unopposed/analyse.py:186, 478`, not in `ch5_defended/analyse.py` or `measures.py`.
- **`mtd_metric_catalogue.md` l.41** still says "Does not exist … defined in §4.5". It contradicts the 2026-09-24 "adapted from Hong" ruling. One of the two should be updated to match Marc's ruling on Open 1.

## Open for Marc

1. **Keep Hong's name for a quantity Hong would not recognise as his APV?** The draft is §d2-compliant (the difference is named), but it changes object, axis, form and role, and Hong is the supervisor. *Recommendation:* keep "attack path variation (APV), adapted from Hong", with the difference sentence as drafted. Raise it with Dr Hong in the next meeting rather than let him find it; the fallback is a descriptive name (no acronym) citing Hong as the nearest metric.
2. **Modal form or Hong's pairwise form?** *Recommendation:* modal (the code and figure). It keeps resolution across $k$; the pairwise form saturates by $k$ = 5 and flips the negligible $c_3$/baseline order at $k$ = 5–6.
3. **Cite Freeman (1965) for the $1 - $ modal-share form?** *Recommendation:* yes, if you want the form itself anchored. To download: L. C. Freeman, *Elementary Applied Statistics: For Students in Behavioral Science*, Wiley, 1965 (the variation ratio). Not in `references.bib`; read only through a secondary source.
4. **Symbol $\pi_k(r)$ or Hong's $ap_k(r)$?** *Recommendation:* $\pi_k(r)$ (conventional for a path, free in the thesis).
5. **The "cannot fall as $k$ grows" clause:** *Recommendation:* keep. It stops the reader from reading Figure 5.1(b)'s rise with $k$ as a result, and is the first 8 words to cut if the paragraph must shrink.
