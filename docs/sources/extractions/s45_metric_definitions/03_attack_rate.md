# 4.5.1 Attack rate (label eq:attack-rate)

## LaTeX

```latex
\paragraph{Attack rate.}
Zhan et al.\ define the attack rate as the number of attacks that arrive at a
honeypot per unit time \citep{zhan2013}. We adapt it to one attacker's own
actions, per 1\,000\,s of its active time:
\begin{equation}
  \lambda = \frac{1}{|\mathcal{R}|} \sum_{r \in \mathcal{R}} \frac{1000\,|A_r|}{T_r},
  \label{eq:attack-rate}
\end{equation}
where $A_r = (a_1, a_2, \dots)$ holds the start times of run $r$'s actions and
$T_r$ is its active time, from the start of the run to the end of the
attacker's last step. An action counts when it runs on the network: a
dwell-only tactic dispatches none, an action whose precondition is unmet fails
before it runs (Section~\ref{subsec:runtime-mechanics}), and the baseline
attacker's exploit counts once, however many vulnerabilities it tries. Only the
APT attacker model dispatches actions outside the baseline attacker's phase
order, so leaving out unmet preconditions lowers its rate alone. Active time is the
denominator because an attacker can stop before the time limit, as it does on
compromising a target, and the time after would read as a slower attacker. A
higher rate is a more aggressive attack \citep{pendleton2016}.
```

**Word count:** about 150 words of prose (168 by `wc`, which counts the inline maths as words); equation excluded. The metric alone (source sentence, adaptation, equation lead-in, where clause, direction) is about 75 words. The definition of *action*, which both stealth metrics use, and its concession take about 55. The active-time rationale takes about 30.

## Structure

| Slot | Used | Where |
|---|---|---|
| S1 name, cited, status | yes | Sentence 1 gives the source's definition, with the cited author as subject (terminology.md l.73). Sentence 2 says "We adapt it", so the status is in the second sentence and each opener stays a single main clause (Marc's opener rule). |
| S2 what it measures | merged into S6 | "one attacker's own actions, per 1 000 s of its active time" says what it measures and how it differs from Zhan in one clause. |
| S3 operation and equation | yes | Eq. `eq:attack-rate` with a where clause. It defines $A_r$ and $T_r$ for the first time in §4.5, and attack confidentiality reuses both. |
| Action rule (owned term) | yes, 2 sentences | One colon sentence covering the three exclusions a reader could ask about, then a one-sentence concession (voice.md §c5: the rule favours the APT attacker model, so the text says so). End-of-run markers are left out of the prose because they are a recording artefact with no action and no counterpart in ch4. The code excludes them (see below). |
| S4 range and direction | yes, last sentence | Direction, cited to Pendleton's "aggressiveness" reading. The range ($\lambda \ge 0$, unbounded) goes unstated because it is obvious for a count per time. |
| S5 when read, edge case | when read: rationale sentence; edge case: dropped | $T_r = 0$ cannot occur (below), so no edge-case sentence. When it is read (no defence) is the class opener's job. |
| S6 what differs | merged into sentence 2 | Differences from Zhan: whose events (one attacker's own actions, not arrivals at a honeypot from many attackers) and the window (active time, not a calendar unit). |
| Rationale | one sentence, on active time | A reader asks why the denominator is not the time limit. Per 1 000 s needs no rationale: Zhan leaves the unit free ("e.g., minute or hour or day"). |

**Length against budget.** Adapted: 40–80 words plus one clause, plus 1–2 sentences for *action*. That gives about 120. This draft is about 150, the same as the two sibling drafts (RTO about 165, APV about 150). **Cut candidates in order**, if Marc wants it tighter:
1. The Pendleton sentence (9 words). Direction is obvious for a rate, and Pendleton can move to Table 4.3's source cell.
2. The concession sentence (24 words). It could move to the §5.2 body that reads the rate. I do not recommend this (voice.md §c5).

## Verification

### Sources

| Claim | Source and locator | Verbatim quote | Verdict |
|---|---|---|---|
| Zhan et al. define attack rate as attacks arriving per unit time | Zhan, Xu & Xu, arXiv 1603.07433v1 (the authors' copy of IEEE TIFS 8(11), 2013), p. 3, §III-B "Step 2: Basic statistical analysis". Fetched this session: `scratchpad/s45/zhan2013.txt` l.313–320 | "For stochastic cyber attack processes, the primary statistic is the attack rate, which describes the number of attacks that arrive at unit time (e.g., minute or hour or day). Note that attack rate can be instantiated at various resolutions of attack processes, such as: network-level attack rate, victim-level attack rate and port-level attack rate." | holds |
| The attacks are honeypot-captured events | same, p. 3, §III-B Step 1 | "It is now a common practice to treat honeypot-captured data as attacks because there are no legitimate services and the honeypot computers passively wait for incoming events." Also: "we advocate using flows, rather than IP packets, to represent attacks" | holds ("arrive at a honeypot") |
| The unit is free, so per 1 000 s is within the source | same quote | "(e.g., minute or hour or day)"; the case study uses "the per-hour attack rate" (p. 5, `zhan2013.txt` l.493) | holds |
| Pendleton et al. survey attack rate and read it as aggressiveness | `docs/sources/methodology/pendleton2016_security_metrics_survey.md`, arXiv 1601.05792v1, p. 15, §5.1 "Measuring the threat landscape" (l.766–772) | "Another related attack rate metric measures the number of attacks that arrive at a system of interest per unit time [Zhan et al. 2013; Zhan et al. 2015]. These metrics reflect the aggressiveness of cyber attacks." | **partly**: read in arXiv v1 only. The bib entry is the ACM CSUR version with Cho as an author. The bib's own VERIFY comment asks for the published wording |
| Catalogue relay (census F S1) matches the primary | `docs/sources/extractions/metric_census/F_web_open_access.md` l.15 | its quote matches the arXiv text word for word | holds |
| Chapter 4 calls the six operations *actions*, dispatched by a tactic | dissertation.tex l.5159–5166; terminology.md l.52 (RULED 2026-09-25: *action* over *verb*, "verb DEPRECATED") | "Where there is no mapping, the tactic is dwell-only: it consumes time in the simulator and dispatches nothing." | holds. The brief's "a verb that runs" is written as "an action … runs" |
| Chapter 4 has an action failing on an unmet precondition | dissertation.tex l.4910–4911 (§4.4.1 `subsec:runtime-mechanics`) | "An action fails if the preconditions of the action itself were missing --- for example, trying to exploit a vulnerability without having scanned for it." | holds. The draft adds that such an action "fails before it runs", which the code confirms (below) |
| The join dispatches outside the baseline attacker's phase order | dissertation.tex l.4843–4844 | "The join calls each MTDSim action on its own, outside the baseline attacker's phase order" | holds |
| *Time limit* is the canonical term; a run ends early on a target | terminology.md l.93 (RULED 2026-09-20); tables/tab_5-1a_experiment.tex l.114 | "Time limit & 15\,000\,s \citep{ho2024}; a run ends earlier if the attacker compromises a target" | holds |

### Code check

The attack rate is computed in `data/results/ch5_s531_unopposed/analyse.py`, **not** in the `ch5_defended` files the brief lists. Numbers are in `data/results/ch5_s531_unopposed/numbers.json` → `core.metrics.<profile>.attack_rate`.

| Equation term | Code (file:line) | Verdict |
|---|---|---|
| Mean over runs of per-run rates, $\frac{1}{\lvert\mathcal{R}\rvert}\sum_r$ | `analyse.py:423` (APT attacker model) and `:433` (baseline attacker) apply `_iv` → `M.mean_ci` to the per-run `_rate` values. This is a mean of ratios, not a ratio of sums | matches. A ratio of sums would give c4 20.65 against 20.68, and baseline 28.17 against 28.43 |
| $1000\,\lvert A_r\rvert / T_r$ | `analyse.py:365–366` `_rate`: `1000.0 * len(starts) / end` | matches |
| $A_r$ for the APT attacker model: actions that run | `analyse.py:343–352`: a record counts if `place_class == "action-bearing"`, `rec.verb` is non-empty, and it is `not rec.blocked` | matches |
| Dwell-only tactics dispatch none | `movement/attacker.py:603–625` records `verb=""`, `place_class=DWELL_ONLY` | matches (excluded) |
| Unmet precondition fails before it runs | `movement/attacker.py:894–902`: `assert_action_context(verb)` raises `ActionContextError` **before** `attack_op.step()` (l.906). The record is `_PRECONDITION_UNMET` with `blocked=True`, and the tactic's time is still served. The checks are in `mtdnetwork/operation/attack_operation.py:771–801` (e.g. exploit needs `curr_host` and non-empty `curr_ports`). A second blocked path, `attacker.py:865–876`, covers the case where the fresh-host contract finds no fresh host: the action is not run, and it is also `blocked=True` | matches |
| End-of-run markers excluded | `attacker.py:1258–1291` `_emit_terminal`. In the data all 53 markers have `verb=""` and zero length, sit at the previous record's end, and occur only on target capture | matches (excluded by `rec.verb`) |
| Interrupted actions | `attacker.py:979–999`: `_read_interrupt` returns `was_blocked=False`, so an action cut short by a deployment counts (it ran) | consistent; not in play in the no-defence corpus |
| Baseline exploit counts once | `analyse.py:355–362` collapses consecutive `EXPLOIT_VULN` rows. `attack_operation.py:536–565` writes one row per vulnerability tried (90 860 of 97 080 exploit rows are repeats) | matches |
| $T_r$: start of run to the end of the last step | `analyse.py:351` is `max(rec.end_time for rec in run.records)` over **all** records (actions, dwell-only tactics, blocked). The baseline uses the max row finish (`:361`). `movement/run.py:515–516`: `termination_time = records[-1].end_time`. A step still running at the time limit is never recorded | matches the draft ("the end of the attacker's last step"). **Mismatches the tex slot S5 and the handoff Open list**, which say "to the last action". For the APT attacker model the two differ by 0–1 369 s (median 0) |
| Why active time | Baseline: `run_corpus.py:103` runs to `horizon` regardless. The attacker stops on target capture (58 of 100 runs end on a target row) **or when host discovery finds nothing** (`attack_operation.py:353`, "If the scan returns nothing, the attacker stops"). The second case is 17 of the 40 runs that miss the target, stopping 943–9 457 s early | holds. The handoff's rationale names only the target, so the draft says "can stop before the time limit, as it does on compromising a target" to cover both |
| Reproduction | read-only import of `analyse.py`: c4 20.677, $c_{\mathrm{agg}}$ 16.913, baseline 28.430 | equal to numbers.json and Table 5.3 |

**Edge case $T_r = 0$.** `_rate` returns `None` and that run is left out of the mean. It cannot occur: every run's first step takes positive time, and the minimum observed $T_r$ is 4 686 s (APT attacker model) and 3 043 s (baseline). No prose is owed. The run count behind every value is $\lvert\mathcal{R}\rvert$ (n = 100 in numbers.json).

**Findings for Marc** (not changes):
1. **Baseline repeated ENUM_HOST rows each count as an action.** The native loop re-dispatches ENUM_HOST (5 s each) for every already-owned host it pops (`attack_operation.py:462–471`). That is 2 305 rows, 7.8 % of the baseline's 29 416 actions. The APT attacker model's equivalent re-pops happen inside one action at no time cost (`attacker.py:865–870`, `_reselect_fresh_host`). Each baseline re-dispatch really runs, so the rule is applied consistently. The asymmetry inflates the baseline's rate: collapsing those rows gives 26.36 against 28.43, and c4 at 20.7 is still below it. RTO (draft 01) collapses these rows into one *step*, so for the baseline an action is not a step.
2. **The baseline does not strictly always meet preconditions.** 37 of its 29 416 actions (0.13 %) are zero-length exploits with no vulnerability to try (`attack_operation.py:595–611`). They run and so count, which is consistent with the rule. The draft's concession ("Only the APT attacker model dispatches actions outside the baseline attacker's phase order") is worded on the phase order, not on "never fails", and holds.
3. **The action rule matters.** Counting unmet preconditions would put c4 at 28.65 against the baseline's 28.43 (`numbers.json` `attack_rate_counting_blocked`). The draft states the direction of the bias but gives no number (no results in a definition).

### Status check

"Adapted" is honest. Zhan's quantity is the same operation, a count of attack events per unit time, and the source leaves both the unit and the resolution open ("network-level … victim-level … port-level"). Two things differ: the events are one attacker's own actions rather than every attacker's flows arriving at a honeypot, and the window is the attacker's active time rather than a fixed calendar unit, averaged over runs. The name is used as Zhan and Pendleton use it: a count per time, not a probability or an intensity. The reading of a *lower* rate as stealth is not in either source. It belongs to attack confidentiality's rationale (Ward, Jafarian, Alshamrani) and is not claimed here. The draft cites Pendleton only for the source's own reading (aggressiveness).

## Symbols

| Symbol | Meaning | Status |
|---|---|---|
| $\lambda$ | the attack rate, actions per 1 000 s | **new to the tex** (grep: `\lambda` appears only in the commented draft at l.5468; not in `tab:gspn-notation`, and absent from the tables). It is the conventional symbol for an arrival rate, and the corpus uses it for exactly this quantity: Kim et al. 2026 (`kim2026`, in the bib) print "ATK_λ | Attack rate per 1 min." (`docs/sources/lit_review/3_2_kim2026mtdid.md` l.363). Zhan writes $X_t$ for the rate at time $t$, but $X$ says nothing and is time-indexed. The risk is that a GSPN reader expects $\lambda$ as a transition firing rate. Chapter 4 uses $\mu_p$ (mean dwell) and never $\lambda$, so no collision |
| $r$, $\mathcal{R}$ | a run; the runs of one cell | shared (brief) |
| $A_r = (a_1, a_2, \dots)$ | start times of run $r$'s actions | shared. **First defined here**; attack confidentiality reuses $a_i$ |
| $T_r$ | active time | shared. **Owned here** |

Collision check: `grep -n "\\lambda\|A_r\|T_r\|\\mathcal{R}" dissertation.tex` finds live-text hits in none of them, only in the §4.5 comment block (l.5424–5425, 5468–5469). Chapter 4 reserves $\tau$, $t_{pq}$, $\mu_p$ and the rest; none of those appears here. One watch item for another agent: the NCR growth rate draft uses $r(t)$, which collides with $r$ for a run.

## For elsewhere

- **§4.5.1 class opener.** It should say the class is read with no defence running. The attack rate draft relies on this and does not repeat it.
- **Step (RTO, draft 01).** $T_r$ is defined as "to the end of the attacker's last step", so *step* must be defined before attack rate. Draft 01 does this. For the baseline attacker, steps collapse repeated ENUM_HOST rows and actions do not; see finding 1.
- **Attack confidentiality.** Reuse $A_r$, $a_i$ and *action* exactly as defined here, and do not redefine them.
- **Tex slot S5 and handoff Open list**: "active time: to the last action" is wrong against the code. It is to the end of the last step (any record). Correct the comment when this block is uncommented.
- **Handoff entry 3**: "a verb that runs" becomes "an action that runs" (*verb* deprecated 2026-09-25). The "why active time" rationale should also name the baseline's other stopping case, finding nothing left to scan.
- **Chapter 5 §5.2 body** (not yet drafted): the one number behind the concession, c4 28.7 if unmet preconditions counted against the baseline's 28.4, belongs where the rate is read or in an Appendix C robustness item. No such appendix section exists yet; the handoff's "Appendix C.4" is not in the tex.
- **Table 5.3** (`tab_5-2-1a_unopposed_summary.tex`): the header "Attack rate (per 1 000 s)" and the caption's "Means with a 95 % interval" are both licensed by Eq. `eq:attack-rate`. The numbers match the code. No mismatch.
- **Table 4.3 source cell**: "adapted from \citep{zhan2013}" is consistent. Optionally add `pendleton2016` if the Pendleton sentence is cut from §4.5.
- **Table 3.1** (handoff Open 2): add Zhan as an anchor so the source is on the literature review's map.
- **Brief's code list**: the attack rate lives in `data/results/ch5_s531_unopposed/`, not `ch5_defended/`.

## Open for Marc

1. **Keep the concession sentence** (the rule lowers the APT attacker model's rate alone). Recommend keeping it: voice.md §c5, and it answers the examiner before they ask.
2. **Keep the Pendleton direction sentence, or move it to Table 4.3.** Recommend keeping it, pending confirmation of "aggressiveness" in the published CSUR version (the bib's VERIFY). If it cannot be confirmed, cut it.
3. **Baseline ENUM_HOST repeats (finding 1)**: keep them counted as actions (each is a dispatched 5 s action in MTDSim). Recommend keeping them, and adding one sentence where the §5.2 body reads the rate, or in an appendix, giving 26.4 if they are collapsed.
4. **Symbol $\lambda$**: recommend adopting it (conventional arrival-rate symbol; Kim 2026's ATK_λ).
5. **To download (low priority)**: the published Zhan 2013 (IEEE TIFS 8(11):1775–1789) for page numbers. The arXiv copy read here carries the definition, so the thesis can cite it by section (§III-B) now. The published Pendleton 2016 is already on the list.
