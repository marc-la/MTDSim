# §4.5.3, entry 8: NCR reduction (the first MTD effectiveness metric)

## LaTeX

```latex
\paragraph{NCR reduction.}
\citet{alavizadeh2022} measure ``the ability of the defensive MTD techniques to
impair the attack'' by a mitigation factor, one minus the ratio of the annual loss
expectancy with a defence to that without it. NCR reduction adapts it to NCR
(Equation~\ref{eq:ncr}):
\begin{equation}
  \text{NCR reduction} = 1 - \frac{\mathrm{NCR}(\mathcal{R}_m)}{\mathrm{NCR}(\mathcal{R}_0)},
  \label{eq:ncr-reduction}
\end{equation}
where $\mathcal{R}_m$ is one attacker's runs under defence $m$ at one deployment
interval, and $\mathcal{R}_0$, the \emph{no-defence reference}, is the same
attacker's runs on the same seeds with no defence, one set serving every interval.
It takes values in $(-\infty, 1]$: 0 is no effect, 1 is no host compromised, and
higher is better for the defender. Unlike the mitigation factor, it is not floored
at zero, so a defence that helps the attacker reads negative. Every attacker
compromises hosts with no defence (Table~\ref{tab:unopposed-summary}), so the
denominator is never zero. Section~\ref{subsec:metrics-statistics} gives its
interval and ranks the defences by it.
```

Word count: about 125 words of prose (the equation excluded).

## Structure

| Slot | Used | Where |
|---|---|---|
| S1 name, cited, status | yes, merged with the source's meaning | sentence 1 cites the source and quotes its purpose; sentence 2 gives the status: "adapts it to NCR" |
| S2 what it measures | merged into S1 | the quoted purpose ("the ability ... to impair the attack") does S2's job. A second sentence would repeat it |
| S3 operation and equation | yes | the equation, with a "where" clause that also defines the **no-defence reference** (this entry owns that term) |
| S4 range and direction | yes | one sentence: $(-\infty, 1]$, with 0, 1 and the direction |
| S5 edge case | yes | the denominator is never zero, bound to Table 5.2's no-defence NCRs, with no number quoted |
| S6 adapted difference | yes, one sentence | the floor at zero is dropped. The other difference (NCR in place of the loss) is already in sentence 2 |
| Rationale (why NCR, not ASP) | **dropped** | 4.5.2's NCR definition already owes the sentence "that is why NCR, not ASP, carries §5.3" (handoff entry 6). Repeating it here would say it twice. If the NCR drafter drops it, restore one clause here: "on NCR because the APT attacker model's ASP is zero under most defences and cannot order them" |
| Last sentence | yes | points to 4.5.4 for the interval and the ranking. Scott–Knott ESD is not named here |

**Length.** The budget is 40–80 words for an adapted metric, plus one clause for the difference, so about 95. This draft is about 125. Three things this entry must carry push it over: the owned term, the edge case the pitfalls table requires ("say so"), and the 4.5.4 pointer. If the no-defence reference moves to the 4.5.3 opener, cut the where clause's second half and "one set serving every interval". That brings the draft to about 100 words.

## Verification

| Claim | Source and locator | Verbatim quote | Verdict |
|---|---|---|---|
| Alavizadeh et al. define a mitigation factor, and this is its purpose | alavizadeh2022, §V-D "Benefits of security", p. 1782 (`docs/sources/lit_review/alavizadeh2022.md` l.596–601; also checked in the PDF text layer, pypdf, p. 11 of the file) | "Another evaluation measurement that uses the ALE values of the cloud before and after deploying the MTD techniques is the mitigation factor. The mitigation factor, denoted by MF^m, shows the ability of the defensive MTD techniques to impair the attack." | holds (the draft quotes "the ability ... to impair the attack" exactly) |
| Its form is one minus the ratio of ALE with a defence to ALE without | same, Eq. 13 (pypdf text) | "MFm = 1 − ALEm c / ALEc ; if ALEm c < ALEc ; 0; otherwise" | **partly**: the form holds on the first branch only. **The factor is piecewise and floored at 0.** The handoff (entry 8), the tex holder and `mtd_metric_catalogue.md` l.35 all quote it as a bare $1 - \mathrm{ALE}^m/\mathrm{ALE}$ and leave the floor out |
| Its range and direction | same, l.599–601 | "MFm takes values within the range [0,1] as in Equation 13. Note that, a larger value of MFm is more desirable." | holds. Our range differs ($(-\infty,1]$), and the draft says so |
| ALE is the annual loss expectancy | same, §V-C, l.548–551 | "Annual loss expectancy (ALE) can be defined as the expected financial loss due to an attack event" | holds |
| "Reduction" as a 1 − ratio in MTD evaluation (supports the name; not cited in the draft) | sharma2025, Eq. 17 (`docs/sources/lit_review/sharma2025.md` l.383–386) | "Security Risk Reduction Percentage (SRRP) ... = (1 − TTC_no−mtd(hi) / TTC_mtd(hi)) × 100%" | holds as corroboration only. It is the same 1 − ratio shape on a quantity where higher is better (hence the inverted ratio). It is **not** needed in the definition |
| NCR is Zhang 2023 / Ho 2024's metric | entry 6's drafter verifies this | — | not re-verified here. The draft cites it only through Equation~\ref{eq:ncr} |
| Every attacker's NCR is positive with no defence | `docs/thesis/tables/tab_5-2-1a_unopposed_summary.tex` | NCR $0.15, 0.20, 0.16, 0.14, 0.17$ ($c_1$–$c_4$, $c_{\mathrm{agg}}$); $0.49$ (baseline) | holds. numbers.json `sweep.by_interval.*.attacker.*.hosts_none`: APT attacker model (c1–c4 pooled) 8.13 hosts (n = 400), i.e. NCR 0.16; baseline attacker 24.34 hosts, i.e. 0.49. The smallest per-profile value is 7.21 hosts ($c_4$) |
| Negative values occur, so the range must include them | numbers.json `sweep` | min point −0.144 (APT attacker model, user shuffle, 50 s; bootstrap interval −0.229 to −0.061); −0.131 (baseline attacker, complete topology, 2 000 s) | holds. This is why the floor must go (not quoted in the draft: no results in a definition) |

**Status ruling: "adapted from", not "in the form of".**
- "In the form of" is not a conventional attribution formula. The template's three formulas are "as defined by", "adapted from" and "we define".
- The phrase is also inaccurate. Alavizadeh's factor has a floor, and ours does not. Keeping the negative values is a real change: chapter 5's captions and Table 5.3.2c read "a negative value is more hosts compromised than with no defence", and the user shuffle is negative against the APT attacker model.
- So the metric is **adapted** on two counts: the base quantity (NCR for ALE) and the floor (dropped). The draft names both.
- No field name is reused. "Mitigation factor" is named only as the source, and "NCR reduction" is a descriptive name built from NCR, in line with Sharma's "risk reduction".

**Code check** (`data/results/ch5_defended/analyse.py`). The table comment's `analyse.py:304` is stale: `suppression()` is now at l.334.

| Equation term | Code | Verdict |
|---|---|---|
| $1 - \mathrm{NCR}(\mathcal{R}_m)/\mathrm{NCR}(\mathcal{R}_0)$ | l.337 `point = 1.0 - cond_hosts.mean() / none_hosts.mean()` | **matches**. It is a ratio of means over runs, not a mean of per-run ratios. The code uses host counts, and $N = 50$ cancels (NCR $= |H_r|/N$, averaged) |
| $|H_r|$ | movement l.179 `run.compromised_count` (= `len(adversary.get_compromised_hosts())`, `movement/run.py:533`); baseline l.256 `row["compromised_uuid"]` (distinct hosts, `run_corpus.py:294`) | matches: hosts compromised at the end of the run |
| $\mathcal{R}_m$, one attacker | `arm_cells` l.755–767 (APT attacker model = the runs of `FOUR` = $c_1$–$c_4$ pooled, **not** $c_{\mathrm{agg}}$; baseline = its own cell); per profile `section_sweep` l.1016 against that profile's own no-defence cell (l.1003) | matches, if "one attacker" covers "the four profiles pooled" and "one profile". The pooling itself belongs to 4.5.4 (see For elsewhere) |
| at one deployment interval | `section_sweep` l.1004–1010, `section_ranking` l.1068–1073: numerator per interval | matches |
| $\mathcal{R}_0$ the same seeds, no defence, one set for every interval | `_cell` l.316–320 forces `interval = 0` for `condition == "none"`; `run_corpus.py:338–340` runs "none" once per seed at interval 0 from the same `SEEDS`; numbers.json shows the same denominator (8.13 / 24.34) at all six intervals | matches |
| Range $(-\infty, 1]$ | point = 1 iff `cond_hosts.mean() == 0`; unbounded below | matches |
| (Not in the definition) interval | l.338–343: percentile bootstrap, 2 000 resamples, the two cells **resampled independently** ("unpaired") | 4.5.4's; the handoff already flags it as open |

**Name check.** "NCR" is used as Zhang and Ho use it (hosts compromised over hosts, read at the end of the run; entry 6 owns the checkpoint caveat). "Mitigation factor" is used only as Alavizadeh's name for Alavizadeh's quantity.

## Symbols

| Symbol | Status | Reason |
|---|---|---|
| $\mathcal{R}$ | shared (§4.5 set) | the runs of one cell |
| $m$ | **new** | a defence condition (a mechanism, a scheme or MTDShield). Taken from the source: Alavizadeh's superscript $m$ is "a set of MTD used as defensive techniques" (l.590–591), so this is the field's own symbol |
| $\mathcal{R}_0$ | **new subscript** | the no-defence reference. A subscript 0 for the control is conventional, and the code stores that cell at interval 0 |
| $\mathrm{NCR}(\mathcal{R})$ | depends on entry 6 | Equation~\ref{eq:ncr} evaluated over a set of runs. It needs eq:ncr written as a mean over $\mathcal{R}$, as the tex holder drafts it |
| LHS "NCR reduction" spelled out | **proposed in place of $\Delta_{\mathrm{NCR}}$** | $\Delta$ conventionally denotes a difference, and this is a relative reduction. The code also computes a true difference (`absolute_reduction`), which $\Delta$ would invite a reader to confuse with this one. $\Delta$ is also already live in the appendix (l.8441, "signed phase offset $\Delta$"). An acronym (e.g. "NCRR") is ruled out (no invented acronyms). A worded left-hand side is defensible: Sharma's Eq. 17 names its LHS by the metric's name (SRRP). Alavizadeh's own symbol is $\mathrm{MF}^m$; borrowing it would misname our unfloored quantity |

Collision check (live, uncommented tex):
- `grep -nP '\$[^$]*(?<![a-zA-Z\\])m(?![a-zA-Z])[^$]*\$'` over `dissertation.tex` and `tables/*.tex` found no hits, so $m$ is free.
- `tab:gspn-notation` (l.4664ff.) has no $m$ and no $\mathcal{R}$. $M_0$ is a different letter from $\mathcal{R}_0$.
- `\Delta` has one live hit at l.8441, which is why $\Delta_{\mathrm{NCR}}$ is avoided.
- There is no live `\mathrm{NCR}` math yet.

## For elsewhere

- **Table 4.3 (`tab_4-5a_metrics.tex` l.179).** The Source cell reads "\citep{zhang2023, ho2024}, in the form of \citep{alavizadeh2022}". Change it to "adapted from \citep{alavizadeh2022}", which matches the other adapted rows; NCR's own citations sit on the NCR row. Also fix the comment's `analyse.py:304` to l.334.
- **§4.5 holder (l.5539–5552).** It says "adopted form" and "cited form". Both should now read adapted.
- **`mtd_metric_catalogue.md` l.35 and the handoff entry 8.** Both misquote Eq. 13 without its floor ("otherwise 0") and its [0,1] range. Correct the record.
- **Entry 6 (NCR).** Write eq:ncr as $\mathrm{NCR}(\mathcal{R}) = \frac{1}{|\mathcal{R}|}\sum_{r\in\mathcal{R}} |H_r|/N$, so that this entry can call it on $\mathcal{R}_m$ and $\mathcal{R}_0$. Keep the "why NCR, not ASP, carries §5.3" sentence there, because this entry relies on it.
- **4.5.4.** It must say three things:
  - the APT attacker model's cell pools $c_1$–$c_4$ in both numerator and denominator ($c_{\mathrm{agg}}$ is read on its own);
  - the bootstrap is unpaired (resamples the two cells independently), an open point already flagged;
  - the Scott–Knott ESD ranks per-seed mean hosts, which within one attacker orders the defences as NCR reduction does, since the denominator is shared. This is what licenses "ranks the defences by it" here.
- **The 4.5.3 opener.** If it defines the no-defence reference ("every MTD effectiveness metric is read against ..."), trim this entry's where clause to "$\mathcal{R}_0$ the no-defence reference".
- **Chapter 5.** The usage is licensed:
  - Figure 5.4/5.5/5.6 captions, Tables 5.3.2a–c and F-1 ("zero is as many as with no defence, below zero is more", "the no-defence reference", "pooled over $c_1$ to $c_4$") all agree with the definition.
  - Figure eff-cross-arm's "a layer's line being the mean over its mechanisms" holds, because the code's pooled-runs ratio equals the mean of the mechanisms' NCR reductions when the run counts are equal (they are, 400 each).
  - **Mismatch:** `tab_5-3-3a_lineage.tex` l.18 still says "mean suppression" (the deprecated word). Replace it with "NCR reduction".

## Open for Marc

1. **Status: "adapted from", not "in the form of".** Recommend adapted. The source floors the factor at zero and ours goes negative, so "in the form of" overstates the match and is not a conventional formula.
2. **The equation's left-hand side.** Recommend spelling out "NCR reduction", over $\Delta_{\mathrm{NCR}}$ ($\Delta$ reads as a difference and is live at l.8441) and over $\mathrm{MF}$ (it would misname an unfloored quantity).
3. **Where "the no-defence reference" is defined.** Recommend keeping it here, where it is first needed. Move it to the 4.5.3 opener only if time lost's definition also leans on it; it does, through $L_{\text{none}}$.
