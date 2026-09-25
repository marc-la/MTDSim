# §4.5.1 Relative tactic occurrence (`eq:rto`), with the term *step*

## LaTeX

```latex
\paragraph{Relative tactic occurrence.}
Relative tactic occurrence, adapted from Rodriguez et al.\ \citep{rodriguez2024},
is the share of an attacker's steps that fall in each tactic, pooled over its runs.
A \emph{step} of the APT attacker model is one firing of $\tau_p$, its execution
of tactic $p$. The baseline attacker has no tactics, and its step is one of its
actions entered. Its record logs a row for each host enumerated and each
vulnerability tried, so consecutive rows of the same action count as one step,
matching the Petri net, which has no self-loops
(Section~\ref{sec:petri-formalism}). Relative tactic occurrence is
\begin{equation}
  o(p) = \frac{\sum_{r \in \mathcal{R}} n_r(p)}
              {\sum_{r \in \mathcal{R}} \sum_{q} n_r(q)},
  \label{eq:rto}
\end{equation}
where $\mathcal{R}$ is the runs of one attacker, on one attack profile for the
APT attacker model, $n_r(p)$ is the number of steps run $r$ takes in tactic $p$,
and $q$ ranges over the profile's tactics. The baseline attacker's shares are
taken in the same way over its actions. Each share lies in $[0, 1]$, and an
attacker's shares sum to one. Rodriguez et al.\ count every event in their logs,
consecutive events of one tactic included; here a tactic counts once each time it
is executed, because one firing of $\tau_p$ is the finest unit the APT attacker
model records.
```

Word count (prose, equation excluded): about 170 words (198 tokens with the LaTeX commands). The metric itself (sentence 1, the equation's lead-in and where clause, the range sentence and the adapted clause) is about 95; the definition of *step*, which §4.5 has to carry once anyway, is about 70.

## Structure

| Slot | Used | Where |
|---|---|---|
| S1 name, cited at the name, with its status | yes | sentence 1: "adapted from Rodriguez et al." (see the status ruling under Verification) |
| S2 what it measures | merged into S1 | "is the share of an attacker's steps that fall in each tactic, pooled over its runs". Keeping it in one sentence saves one sentence and puts the pooling up front |
| S3 the operation in words, then the equation | yes | the two *step* sentences (the operation's unit), then Eq. `eq:rto` with a "where" clause. The baseline attacker is covered by one sentence, "taken in the same way over its actions", so $p$ is not overloaded with a second meaning |
| S4 range and direction | range only | the shares lie in [0, 1] and sum to one. There is no direction, because the metric describes behaviour and neither end is better for the defender. It needs no reading of 0 and 1 either |
| S5 when it is read, and the edge case | dropped | the 4.5.1 opener already says the class is read with no defence. There is no edge case: every run takes at least one step, so the denominator is positive |
| S6 what differs from the source | yes, one clause plus its reason | the last sentence: a tactic counts once per execution, where Rodriguez et al. count every logged event |
| "Why steps, not time" (the rationale in the handoff) | dropped | the source counts, so counting needs no motivation. A time share is not the conventional alternative, and a reader of Rodriguez would not ask for it. The rationale stays in the analyser's docstring (`ch5_s531_unopposed/analyse.py:463–469`) for an examiner who asks |

**Length against the budget.** The adapted budget is 2–4 sentences plus one clause, about 40–80 words. The metric part is about 95 words, a little over, because the where clause has to scope $\mathcal{R}$ to one attack profile (see For elsewhere). The *step* definition adds about 70 words, which the brief allows.

## Verification

| Claim | Source and locator | Verbatim quote | Verdict |
|---|---|---|---|
| Rodriguez et al. tabulate a relative occurrence for each ATT&CK tactic | `docs/sources/lit_review/2_4_rodriguez2024process.md` l.358–384; §4.4.1, Table 3 "Log Summary (ProM)" (PDF p. 8 of 20) | "\|**class**\|**Occur. (abs.)**\|**Occur. (rel.)**\| … \|execution\|3270\|45.01%\|" | holds |
| The relative occurrence is a tactic's events over all events, pooled over the process instances (a ratio of sums) | same table, header rows | "Total number of process\|instances: 21" … "Total number of events:\|7265"; 3270 / 7265 = 45.01 %, and the absolute counts sum to 7 265 (checked) | holds. They pool over 21 red-team cases, as Eq. `eq:rto` pools over runs |
| An event is one labelled row of a host log | §3.1.3 (l.169) and §4.3 (l.321) | "The log is exported as a CSV file, each row representing an event with columns containing event attributes, including the case ID, activity name, and timestamp." / "…mapped to MITRE ATT&CK … the behavior of these 21 attackers is represented by the tactics expressed in the Class column" | holds |
| Their events include consecutive repeats of one tactic, counted separately | §3.2 Discovery (l.181, PDF p. 5) | "In our domain, cases may include repeated activities in sequence or duplicate tasks with the same taxonomy signature." | holds. Their method has no merging step; each row counts |
| Their denominator includes ProM's artificial Start and End classes; ours has none | Table 3 | "\|Start\|21\|0.29%\|" "\|End\|21\|0.29%\|" | holds. Immaterial (0.58 % of their events), so it is not stated in the thesis |
| Rodriguez et al. give no symbol or equation | Table 3 is the quantity's only appearance (grep "Occur" returns only Tables 3 and 5) | — | holds. Eq. `eq:rto` is written here, as the boilerplate's S1 note already said |
| A step of the APT attacker model is one firing of $\tau_p$ | tex §4.3, item 2 of the net's where-list (l.~4516) | "$T_T = \{\tau_p\}$: one timed transition per tactic, from $p$ to $\hat{p}$, whose firing is the attacker's execution of that tactic" | holds |
| The Petri net has no self-loops | tex §4.3, item 3 | "there are no self-loops, because time spent within a tactic is carried by $\tau_p$" | holds. It is also verified in the data: 0 consecutive repeats in 198 524 records (c1–c4, 400 runs) |
| The baseline attacker logs a row per vulnerability tried and per host enumerated | `mtdnetwork/operation/attack_operation.py:462–467` (ENUM_HOST loops back on an already-compromised host); runs.jsonl rows (one EXPLOIT_VULN row per vulnerability) | "An already-compromised host loops back to ENUM_HOST; a fresh host triggers…" | holds. In the data, consecutive repeats are EXPLOIT_VULN 90 860 and ENUM_HOST 2 305; no other action ever repeats |

**Status ruling: adapted, not adopted.** The operation (count per tactic, divided by the total, pooled over cases) is Rodriguez's exactly. The unit counted is not. Their event is a sensor detection, and one tactic executed can emit many of them in a row. Their execution share of 45 % is weighted by how many events the tactic emits. Ours is a tactic entry, and it never repeats. Under literature_conventions §d2, reusing the name with "as defined by" would silently carry that change. With "adapted", the difference costs one clause.

This overturns, on merit, the 2026-09-24 third-pass ruling ("The same quantity, so cited, not adapted"), which rested on the catalogue row's "the share of an attacker's events (here, steps)". That parenthesis is exactly the difference. The collapse on the baseline side is a second transformation that the source does not make.

**The name.** "Relative tactic occurrence" is Rodriguez's column label, "Occur. (rel.)", with the class ("tactic") written in. It is not a field acronym, and none is invented.

### Code check

The figure's analyser is `data/results/ch5_s531_unopposed/analyse.py` (the no-defence corpus), not `ch5_defended/analyse.py`. The defended analyser's `whole_run_tactic_share` (l.562) is a disruption-block quantity that no §4.5 metric names. The check was recomputed from `runs.jsonl` by the script `scratchpad/s45/rto_check.py`.

| Equation term | Code | Verdict |
|---|---|---|
| $n_r(p)$ summed over $r \in \mathcal{R}$ (numerator) | `analyse.py:204`, `Counter(rec.place for r in runs for rec in r.records)` | matches, with the terminal-marker exception below |
| $\sum_r \sum_q n_r(q)$ (denominator) | `analyse.py:205`, `total = sum(visits.values())` | matches. A **ratio of sums**: the recomputation equals numbers.json exactly (maximum difference 0). A mean of per-run shares would differ by up to 0.0005 |
| $\mathcal{R}$ = one attacker, one profile | `analyse.py:778`, `"step_share": rows[p]["tactic_visit_share"]` with `rows[p]` built from `movement[("targeted", CORE, p)]` per profile (l.764) | matches. The data is per profile, never pooled over c1–c4 |
| $q$ ranges over the profile's tactics; a held tactic never entered reads 0, one not held is absent (the figure's dash) | `analyse.py:206–207` (`held = load_routing_net(profile, …).places`) | matches |
| the baseline attacker: its actions, consecutive repeats collapsed, pooled | `analyse.py:463–475` (`step_share_baseline`) | matches. The recomputation equals numbers.json exactly |
| one record per firing of $\tau_p$ | `movement/attacker.py:603`, `:669`: the record is appended after the dwell and routing. A tactic in flight at the time limit is not recorded. A zero-dwell tactic (resource development: $\tau_p$ immediate, §4.3 item 2) is recorded and counted (0.0–3.3 % of steps) | matches |
| **exception** | `attacker.py:567`: when a target falls, a terminal marker is recorded at the tactic the token has just entered (zero dwell, no firing). `analyse.py:204` counts it; `measures.py:123` `visit_records` would drop it | **mismatch, negligible**: 36 markers among 198 524 records (0.02 %). Dropping them changes no share by more than 0.00005, below the figure's 0.1-point precision |

## Symbols

| Symbol | Status | Note |
|---|---|---|
| $\tau_p$, $p$, $q$ | chapter 4 (`tab:gspn-notation`, $t_{pq}$) | $q$ as a second tactic is chapter 4's own use |
| $r$, $\mathcal{R}$ | §4.5 shared | the where clause scopes $\mathcal{R}$ to one attack profile for the APT attacker model |
| $o(p)$ | **new** | "o" for occurrence. Rodriguez et al. give no symbol. Collision check: `grep '\$o(\|\$o_'` finds nothing in live tex. The one risk is visual: $O$ is the output arcs in Eq. `eq:gspn`. If Marc wants no letter near $O$, the alternative is $f(p)$, the conventional relative-frequency symbol (grep `f(` and `f_` in math: free) |
| $n_r(p)$ | **new** | the conventional count notation. grep `n_r` and `n(p` finds nothing in live tex |

APV needs *step* as defined here. Its opening of $k$ steps and the Figure 5.1(b) axis label "opening length $k$ (steps)" both read it.

## For elsewhere

- **Table 4.3, source cell:** change `\citep{rodriguez2024}` to `adapted from \citep{rodriguez2024}` (if Marc accepts the status ruling). Also update the table's comment (round 3, "so not 'adapted'") and the catalogue row (`mtd_metric_catalogue.md` l.40, "the same quantity").
- **§4.5 opener or symbols table:** $\mathcal{R}$ as "the runs of one cell (one attacker, one condition, one interval)" needs to say that the APT attacker model's cells are per attack profile. Otherwise this where clause carries it alone, as drafted.
- **4.5.1 opener:** the boilerplate plans to define *step* in the subsection opener. This draft defines it inside the relative tactic occurrence paragraph, its first use, and APV reuses it. If the opener takes the definition instead, lift sentences 2–4 verbatim and start the paragraph at sentence 1.
- **4.5.4:** relative tactic occurrence is "shares pooled over runs" (the handoff's table). The paragraph says "pooled", so 4.5.4 needs no interval for it, and no ranking.
- **Chapter 5, Figure 5.1(a):** consistent. The caption's "the tactics grouped by the action each dispatches" puts each baseline action's share against the tactics $\varphi$ maps to it. The caption's "a dash marks a tactic the attacker does not have" matches `analyse.py:206–207`. The caption title, "Where each attacker's steps fall", uses *step* in exactly this sense.
- **Terminology:** the handoff and boilerplate say "verb entered". The 2026-09-25 registry row deprecates *verb* for *action*, so the draft says "one of its actions entered".
- **Code (APV's drafter, and Marc):** `measures.place_sequence` (`measures.py:390`) also keeps the terminal marker. APV's openings count it too, as a step with no firing. The effect is again negligible, since a marker is always last and openings are the first 2–8 steps.

## Open for Marc

1. **Status: adapted or adopted?** Recommend **adapted**. Rodriguez counts every logged event, repeats in sequence included; a step counts a tactic once per execution. This overturns the 2026-09-24 third pass.
2. **Terminal marker in the count** (36 of 198 524 records). Recommend filtering it in `tactic_visit_share` (use `measures.visit_records`, or filter on the outcome tag) at the 1 000-seed run, so that the code matches "one firing of $\tau_p$" exactly. Note that `visit_records` also drops zero-dwell dwell-only visits (resource development), so filter on the `SIM_END` tag, not on `dwell > 0`.
3. **Symbol $o(p)$ or $f(p)$.** Recommend $o(p)$ (mnemonic; no collision in the tex).
4. **The *step* definition in this paragraph or in the 4.5.1 opener.** Recommend this paragraph, at its first use; APV then points back to it.
