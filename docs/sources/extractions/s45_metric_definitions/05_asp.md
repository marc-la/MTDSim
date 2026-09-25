# §4.5.2 Attack success probability (ASP): drafting agent 05

## LaTeX

```latex
\paragraph{Attack success probability (ASP).}
\citet[Sec.~VII-A]{cho2020} define attack success probability as ``the
probability that attacks are successfully performed''. Here an attack succeeds
when the attacker compromises any target host of the targeted attack scenario
(Table~\ref{tab:attacker-objectives}) before the time limit. ASP is estimated as
the share of runs in $\mathcal{R}$ that succeed,
\begin{equation}
  \mathrm{ASP} = \frac{1}{|\mathcal{R}|} \sum_{r \in \mathcal{R}}
  \mathbf{1}\bigl[\, r \text{ compromises a target host} \,\bigr],
  \label{eq:asp}
\end{equation}
where $\mathbf{1}[\cdot]$ is 1 when its condition holds and 0 otherwise, so any
other ending counts as 0. ASP takes values in $[0, 1]$; lower is better for the
defender.
```

Word count (prose, head and equation excluded): **about 76 words**, 4 sentences. That is within the adopted budget of 40 to 80 words.

## Structure

| Slot | Used | Sentence |
|---|---|---|
| S1 name, cited, with status | yes | S1. It opens with the authority (brief: authority first, one main clause, no brackets). The acronym is already in the `\paragraph` head. "Adopted" is carried by quoting Cho's definition unchanged and by Table 4.3's plain `\citep{cho2020}` with no "adapted". |
| S2 what it measures | merged into S2 | The success event in this evaluation. This is where the term **target** is defined: any target host of the targeted attack scenario, before the time limit ("any" answers the two-target question: one suffices). |
| S3 operation, equation, "where" clause | yes | S3 and Eq. `eq:asp`. It says "estimated as the share", because Cho's quantity is a probability and the runs give its relative-frequency estimate. |
| S4 range and direction | yes | S4 |
| S5 when read, edge case | merged into S3's "where" clause | "so any other ending counts as 0". This covers the time limit, a Petri-net sink and the simulator's 80 % stop (see For elsewhere) without naming a mechanism §4.4 has not declared. |
| S6 adapted or introduced | dropped | The metric is adopted. |

The draft's S4 clause ("not Ho's ASR") was dropped: ASR appears nowhere in chapter 5, so it would add reader overhead (brief, "reader level"). See Open 2.

## Verification

| Claim | Source and locator | Verbatim quote | Verdict |
|---|---|---|---|
| Cho's definition of ASP | `docs/sources/lit_review/1_1_cho2020toward.md` l.578, §VII-A "Metrics for Measuring MTD Effectiveness" (published pp. 709–745; page not in the markdown) | "**Attack success probability (ASP)** [3], [11], … : This metric refers to the probability that attacks are successfully performed." | holds. The quote in S1 is exact. |
| Our success event (a target host compromised) is one of Cho's own instances, so the status is adopted and not adapted | same, l.578 | "For example, it refers to the probability that a system component (or defender) is compromised or a target is successfully discovered or accessed by an attacker." | holds |
| Cho frames ASP as a campaign-level goal outcome | same, l.636 | "the attack success probability (e.g., whether an attacker achieved its goal of a launched attack such as finding a vulnerable target) is a dominant metric used for the effectiveness of MTD aiming to minimize this metric" | holds. This also supports the direction (lower is better for the defender). |
| Cho gives no estimator. The share of runs is ours, and it is the standard relative-frequency estimate | Cho is a survey; §VII-A has no equation for ASP. The formal precedent for a mean of a Boolean is Zaffarano 2015 §4.2, `docs/sources/lit_review/zaffarano2015.md` l.379–386 (p. 9) | "The success attribute is Boolean valued, taking on just 0 and 1, but the average over a number of tasks makes mission success and attacker success real-valued numbers in the range [0,1]. Formally, … Success(M,ν) = 1/\|T\| Σ_{τ∈T} ν(τ,success)" | partly. Zaffarano gives the same form (mean of an indicator, range [0,1]) but over **tasks**, where ours is over runs. The form is precedented and the unit is ours, so Zaffarano is not cited in the definition (Open 3). |
| Zaffarano names "attack success" | `zaffarano2015.md` l.339–340, Table 4 (p. 8) | "Attack Success is a measurement of how successful an attacker may be while attempting to attack a network" | holds. It is already in Table 3.1 (tex l.2676). |
| With several targets, success is any one (field precedent) | `docs/sources/lit_review/chobenasher2018.md` l.751–752, §4 (the P_AS definition) | "Attack success probability (PAS): Assuming that the system will fail when any one of VNs is compromised by an attacker, PAS is defined by:" | holds. This is supporting evidence only and is not cited. |
| Ho's ASR is a different quantity (per attempt, not per run) | `docs/sources/lit_review/ho2024.md` l.358–364, §3.3.2(6) | "It is calculated by the percentage of attacks by adversaries that successfully compromised hosts compared to the overall attempted attacks. … If no compromised hosts are recorded, the attack success rate is zero." | holds. Confirmed not ASP; kept out of the prose. |
| "Target" as the thesis already names it | tex l.996 (Table 2.3, `tab:attacker-objectives`); l.4852–4855 (§4.4, `subsec:runtime-mechanics`); l.6160–6163 (§5.1 Network) | "Targeted & compromise a target host, deep-embedded, such as a database"; "It attacks a target host if one is visible, … the run ends when a target is compromised."; "the two database hosts at the deepest level as the target" | holds. The draft reuses "target host" and "targeted attack scenario" exactly, and leaves the count (two) to §5.1. |

**Code check (Eq. `eq:asp` against the code).**

| Term | Code | Verdict |
|---|---|---|
| $\mathcal{R}$: the runs of one cell | `data/results/ch5_defended/analyse.py:316` `_cell`, and `_pool` for the APT attacker model's four profiles; `ch5_s531_unopposed/analyse.py` per profile | matches |
| $\frac{1}{\lvert\mathcal{R}\rvert}\sum$: a mean over runs | `ch5_defended/analyse.py:1032` `"asp": float(np.mean([r["reached"] for r in runs]))`; `:1078` (no-defence row). `ch5_s531_unopposed/analyse.py:257–259`, `:318`, `:488` | matches |
| $\mathbf{1}[r$ compromises a target host$]$ in **Table 5.3** (`tab:unopposed-summary`) | `ch5_s531_unopposed/analyse.py:254–259` (APT attacker model: `reached_objective and database_hosts_reached > 0`); `:269–282` (baseline attacker: a target host in the record's compromises; "a run that ended on the inherited compromise-ratio stop is not a target reached") | matches |
| $\mathbf{1}[\cdot]$ in **§5.3's tables** (`tab:eff-cross-arm`, `tab_F-1_conditions_baseline`) | `ch5_defended/analyse.py:178` and `:258`: `reached` is `reached_objective`, which is `end_event.triggered` (`run_corpus.py:198`, `:295`). The event fires on a target compromise **or** on more than 80 % of hosts compromised: `mtdnetwork/operation/attack_operation.py:743–747` (the ratio stop) and `:754–757` (the target stop); `mtd_operation.py:79–81` (the ratio stop again); `time_network.py:55` (the 0.8 threshold) | **MISMATCH, baseline attacker only.** A run that ends at the 80 % stop without a target counts as a success. Checked on `runs.jsonl` (core, targeted): the baseline's no-defence ASP is **0.60 here against 0.58 in Table 5.3** (2 of 100 runs ended at the ratio stop). Under a defence the gap is up to **+0.10** (user shuffle at 500 s: 0.76 against 0.66 target-only). The printed `tab:eff-cross-arm` shows user shuffle at 200 s as 0.74; target-only it is 0.69. The APT attacker model never exceeds 80 % of hosts, so its `reached` is exactly "target compromised" (0 of 48 355 targeted runs) and its ASP is unaffected. |
| Range $[0,1]$ and direction | a mean of Booleans | matches |

A second trap, for whoever fixes the mismatch: `database_hosts_reached` (compromised ∩ database, read **at the end of the run**) is not a valid success read under a host-topology shuffle. `HostTopologyShuffle` swaps host instances within a level and remaps the compromised IDs with them (`mtdnetwork/mtd/hosttopologyshuffle.py:44–56`). For the baseline attacker the defence keeps shuffling after the target falls, until the time limit. As a result, 144 baseline host-topology runs reached a target but show no database host at the end, and 86 show one at the end without having reached a target. The valid read is the record's compromise of a target ID at the time it happened, as `ch5_s531_unopposed/analyse.py:276–278` does for the baseline attacker, or `reached_objective` once the ratio stop is excluded.

**Status check.** "Adopted" is honest. The quantity is Cho's probability of a successful attack, and the success event is one Cho names ("a system component … is compromised or a target is … accessed"). The share of runs is its estimate, which does not change its meaning, and S3 says "estimated". The name and the acronym are used as Cho uses them. The draft does not use Ho's ASR.

## Symbols

- **Used (shared, not redefined here):** $r$ and $\mathcal{R}$, both from the brief's shared table. They need the opener or the symbols table to define them before §4.5.2.
- **New:** $\mathbf{1}[\cdot]$, the indicator function. It is conventional and defined inline in the "where" clause. It is written `\mathbf{1}` because amssymb's `\mathbb` has no digits: `\mathbb{1}` would need `bbm` or `dsfont`, which are not loaded (only `amsmath` and `amssymb`, tex l.28–29).
- **Collision check:** `grep -n 'mathcal{R}\|mathbb{1}\|mathbf{1}'` over live (non-comment) tex lines returns no hits, so both are free. `tab:gspn-notation` (tex l.4664–4684) uses $R$ (the rule kernel), which is distinct from $\mathcal{R}$ by typeface. That is conventional, but whoever owns the symbols table should say so if it is ever read as a clash.
- The target set gets no symbol, deliberately. A set form ($H_r \cap G \neq \varnothing$) would need a new $G$ and would use $H_r$ before NCR defines it.

## For elsewhere

1. **§4.5 opener or symbols table:** $\mathcal{R}$ and $r$ must be defined before §4.5.2. The same applies to the **time limit**, which live chapter 4 text never uses (it is ruled in terminology.md and first used in chapter 5 and the appendices). If the opener does not define it, "before the time limit" reads as plain English.
2. **4.5.4:** ASP's interval in Table 5.3 is the Wald (normal-approximation) binomial interval, $1.96\sqrt{p(1-p)/n}$ (`tools/ch5_unopposed_figures.py:398`). It has zero width at 0.00, which is the APT attacker model's value under five of the ten defences in `tab:eff-cross-arm`. 4.5.4 should declare the interval rule for proportions, and preferably use Wilson for ASP.
3. **Chapter 5, the mismatch:** `tab:unopposed-summary` (0.58) and `tab:eff-cross-arm` (0.60) print different no-defence ASPs for the same baseline attacker. Fix `ch5_defended/analyse.py` `_metrics` (l.1032) and the no-defence row (l.1078) to the target rule (the record-based target compromise, never `database_hosts_reached` at the end of the run), then regenerate `tab_5-3-2d` and `tab_F-1_conditions_baseline`. Baseline ASP values shift down by up to 0.10. The rankings are unaffected because they rest on hosts compromised.
4. **§4.4 and §5.1, an undeclared stop:** under the targeted attack scenario the simulator still ends a run at more than 80 % of hosts compromised, for both attackers (`attack_operation.py:743–747`, `mtd_operation.py:79–81`). §4.4 (l.4854–4855) says only "the run ends when a target is compromised". `targeted_objective_probe.md:575` records Brown's intent (T-d) as "Terminate on target compromise, not on the 80 % ratio". Only the baseline attacker reaches the stop. This is a behaviour to classify against the intent spec before anyone calls it a bug (Open 1).
5. **Appendix, a name clash:** `tab:experiment-one` (tex l.8534, l.8550) labels a column **ASR**, "the fraction of runs reaching the simulator's objective". That is ASP's quantity under Ho's name for a different quantity, and it collides with §4.5 and Table 3.1. Rename it to ASP, or to "objective reached", in the appendix.
6. **NCR-reduction drafter:** the rationale "the APT attacker model's ASP is zero under most defences" holds for 5 of 10 defences at 200 s in `tab:eff-cross-arm` (the other five read 0.02–0.10). That is half of them, not most. Check the claim across the six intervals before writing "most".
7. **NCR drafter:** "ASP beside it says which [ended the run]" is consistent with this definition, provided item 4 is resolved: a baseline run can also end at the ratio stop.

## Open for Marc

1. **The 80 % stop under the targeted attack scenario:** is it declared, or disabled? *Recommendation:* declare it in one clause at §5.1's Attacker unit, keep ASP target-only as drafted, and fix the defended analyser (For elsewhere 3). Disabling it would re-run the corpus for a 2 % effect.
2. **A clause saying ASP is not Ho's ASR?** *Recommendation:* omit it. ASR never appears in chapter 5, and Table 3.1 already lists the two apart. Rename the appendix's ASR column instead (For elsewhere 5).
3. **Cite Zaffarano 2015 at the definition?** *Recommendation:* no. His Success is a mean over tasks, not runs, and Table 4.3's source cell stays `\citep{cho2020}` alone.
4. **The page for the verbatim quote from Cho:** the held markdown has no page numbers, so the draft cites `[Sec.~VII-A]`, which matches the thesis's `Sec.~` pinpoint style. *Recommendation:* keep the section pinpoint. If you want a page, it needs the published PDF (IEEE COMST 22(1), pp. 709–745; to download).
