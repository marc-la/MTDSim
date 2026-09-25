# §4.5.2 — Mean time to compromise (MTTC) — drafting agent 07

## LaTeX

```latex
\paragraph{Mean time to compromise (MTTC).}
MTTC is adapted from \citet{zhang2023}, after the time to compromise of
\citet{mcqueen2006}. It is the mean time to a run's first compromised host,
over the runs that compromise one:
\begin{equation}
  \mathrm{MTTC} = \frac{1}{|\mathcal{R}_1|} \sum_{r \in \mathcal{R}_1} t_r ,
  \qquad
  \mathcal{R}_1 = \{\, r \in \mathcal{R} : H_r \neq \emptyset \,\},
  \label{eq:mttc}
\end{equation}
where $t_r$ is the end of the action that compromises run $r$'s first host,
in seconds from the start of the run; larger is better for the defender.
\citet{zhang2023} read it at 80\,\% of the hosts, where the general attack
scenario ends (Table~\ref{tab:attacker-objectives}); a run of the targeted
attack scenario ends when a target is compromised, so the checkpoint here is
the first host. Runs with no compromise are left out, so MTTC is reported
with $|\mathcal{R}_1|/|\mathcal{R}|$, the share of runs it is taken over, and
is undefined when $\mathcal{R}_1$ is empty.
```

Word count (prose, equation excluded; LaTeX commands count as one word): 121. Of these, the adapted clause (the Zhang/checkpoint sentence) is about 40 and the edge-case sentence about 30.

## Structure

| Slot | Used | Where |
|---|---|---|
| S1 name, citation, status | yes | sentence 1: "adapted from" Zhang, "after" McQueen's time to compromise (McQueen's own definition is kept in Verification row 1, not glossed in the prose, at reader level) |
| S2 what it measures | yes | sentence 2, which also leads into the equation |
| S3 operation and equation | yes | Eq. `eq:mttc`, with an inline "where" clause for $t_r$; $\mathcal{R}_1$ is defined inside the display. $H_r$ is NCR's. |
| S4 range and direction | yes | folded into the "where" clause: "in seconds from the start of the run; larger is better for the defender" |
| S5 checkpoint and edge case | yes | the checkpoint is merged into S6, because it *is* the adaptation; the edge case is the last sentence |
| S6 what differs and why | yes | the Zhang-80 % sentence. Its reason uses no results (Verification row 7). |

Length: 121 words against the adapted budget of about 40–80 plus one clause. The base (S1–S4) is about 50 words. The overrun is the checkpoint sentence, which the handoff owes, and the edge case, whose reporting rule chapter 5's tables rely on. Two trims are possible:
- "(Table~\ref{tab:attacker-objectives})" and "where the general attack scenario ends" could go, saving about 9 words. The cost is that 80 % loses its tie to the reader's own Table 2.x.
- "the share of runs it is taken over" could go, saving 8 words. The cost is that the reader must decode $|\mathcal{R}_1|/|\mathcal{R}|$ unaided.

Recommendation: neither.

## Verification

| # | Claim | Source and locator | Verbatim quote | Verdict |
|---|---|---|---|---|
| 1 | McQueen defines time to compromise as the time an attacker needs to gain privilege on a component | McQueen et al. 2006, INL preprint `docs/sources/tactic_profiles/step_c/mcqueen2006_time_to_compromise.md`, §3, PDF p. 4 (l.149) | "The time-to-compromise ( Tpi) is defined as the time needed for an attacker to gain some level of privilege p on some system component i." | holds |
| 2 | McQueen's quantity is an analytical expected value, per component and skill level, and not a mean over simulated runs | same, §3.4, PDF pp. 11–12 (l.556, Eq. 6, l.594) | "For now, the analysis only uses the expected value of the time-to-compromise." / "T is the expected value of time-to-compromise" | holds. So McQueen is cited for the **concept** (the prose says "after", not "as defined by"). The estimator, an empirical mean over runs, is not his. |
| 3 | McQueen does not name the metric "mean time to compromise" | same, full text; the only "mean time-to-compromise" is Process 1's sub-estimate (PDF p. 6, l.235) | "Thus, the mean time-to-compromise for Process 1 is not modified based on skill" | holds. The "M" comes later in the lineage (Leversage & Byres 2008; census B, Pass 4). This is why MTTC is attributed to Zhang, not to McQueen. |
| 4 | Zhang defines MTTC per target host | Zhang 2023 `docs/sources/lit_review/zhang2023.md`, §3.4, p. 16 (l.250) | "Mean Time to Compromise (MTTC), which measures the time it takes for an attacker to compromise a target host on the network [4]" | holds. Note that Zhang's [4] is Cho et al. 2020, not McQueen. |
| 5 | Zhang reads MTTC when 80 % of the hosts are compromised, averaged over runs | same, §5, p. 32 (l.420); §5.1, p. 33 (l.443); Fig. 8 caption, p. 34 (l.449) | "we set the terminating condition for the simulation as the NCR reaching 0.8 and run the simulation 100 times for each variable set" / "the average time for the adversary to compromise 80% nodes of the target network" / "Mean Time to Compromise on 0.8 NCR" | holds |
| 6 | Zhang's 0.8 is where the general attack scenario ends | dissertation l.984–995, Table `tab:attacker-objectives` and its caption | "General & compromise the network: 80\,\% of the hosts" / "the general scenario's termination ratio is Zhang's \citep{zhang2023}" | holds (the thesis's own table) |
| 7 | A run of the targeted attack scenario ends when a target is compromised (the result-free reason for the checkpoint) | dissertation §4.4.1 (`subsec:runtime-mechanics`), l.4852–4855; code `attack_operation.py:749-757` per the tex comment | "the run ends when a target is compromised." | holds. It replaces the handoff's "14–20 % by the limit", which is a result (Table 5.2's NCR) and so is not allowed in a definition. |
| 8 | The name carries several meanings in the lineage, so the checkpoint must be stated | Cho et al. 2020, `1_1_cho2020toward.md` l.584, §VII-A; Ho 2024 §3.3.2 item 8 (census B l.73) | Cho: "Mean time to compromise a system (MTTC) … how long an attacker takes to compromise an entire system". Ho: "It average of the durations of attack events of SCAN_PORT, EXPLOIT_VULN, and BRUTE_FORCE" | holds. The meanings are an entire system (Cho), 80 % of the hosts (Zhang), the mean duration of one attack event (Ho), and one analytical expectation per component (McQueen). The draft states its checkpoint at the name. |
| 9 | The attacker starts holding no host, so the "first compromise" is its first foothold; no entry host is pre-compromised and excluded | `mtdnetwork/component/adversary.py:77,83` | `self._compromised_hosts = []` … `self._curr_host_id = -1` | holds. Nothing is excluded, and $t_r$ counts the initial-access compromise. |

**The code check, term by term:**

| Term | Code | Verdict |
|---|---|---|
| $t_r$ for the APT attacker model: the end of the first compromising action | `src/mtdsim/l3_simulation/movement/statistics.py:142-148`, `first_compromise_time()`, which returns `rec.end_time` of the first record whose (verb, outcome) is in `_COMPROMISE_EVENTS` (l.33–39: an exploit that compromised, a brute force that succeeded, a credential-reuse port scan). It is read at `data/results/ch5_defended/analyse.py:179`. | matches |
| $t_r$ for the baseline attacker | `analyse.py:260`, `min(r[2] for r in comps)`, where `r[2]` is the record's `finish_time` (`run_corpus.py:299-306`) and `comps` are the records with a compromised host | matches ("the end of the action") |
| "from the start of the run" | both attackers start at simulated time 0: `proceed_time=0` (`run_corpus.py:247`, `movement/run.py:106`). The minimum $t_r$ over 59 755 runs is 40.4 s, and no run has $t_r = 0$ (summaries.pkl check). | matches. The start of the run and the attacker's first action coincide. |
| $\mathcal{R}_1$ and $H_r \neq \emptyset$ | `analyse.py:356`, `obs = [... if r["first_compromise"] is not None]`. Across 59 755 runs, "first compromise is None" and "hosts = 0" never disagree (0 mismatches). | matches |
| the mean over $\mathcal{R}_1$ | `analyse.py:358` → `_iv(obs)` → `M.mean_ci` (the arithmetic mean). The same estimator is at `ch5_s531_unopposed/analyse.py:174-183`. | matches |
| $|\mathcal{R}_1|/|\mathcal{R}|$ is reported | `analyse.py:361` computes `censored_share = 1 - len(obs)/len(runs)`, and `tools/ch5_effectiveness_figures.py:279` prints `1 - censored_share` as the percentage | matches Table 5.3 |
| empty $\mathcal{R}_1$ | `analyse.py:358`: `"observed": _iv(obs) if obs else None` | matches ("undefined"). No cell in the current corpus has an empty $\mathcal{R}_1$. The smallest share is 0.05 ($c_3$, IP shuffle, interval 50). |
| runs left out | every run with no compromise ends at the time limit: all 9 686 of them end within 343 s of 15 000 s, with terminal mode `horizon` for the model and not reached for the baseline. No run ends early at a sink. | consistent. The runs left out are right-censored at the time limit. |

**The code does not compute the inherited MTTC.** The thesis's MTTC is not `mtdnetwork/statistic/evaluation.py`'s quantity. That one is Ho's mean event duration (`metrics_semantics.md` §a), and it is not used by the chapter's analysers.

**The status check: "adopted" is not honest. Ruling: adapted.**
- Zhang's *reported* MTTC is read at a checkpoint of NCR 0.8. This one is read at the first host, which is the one difference that matters, and it is stated.
- McQueen's time to compromise is a per-component analytical expectation that he never calls MTTC.
- Table 4.3's own convention (`tab_4-5a_metrics.tex` comment (2)) is that a bare citation means "the field defines it" and "adapted from" means "the field's name, one difference stated in §4.5". MTTC falls under the second.
- The name is used as the field uses it (time to compromise), and the checkpoint is stated at the definition, as `literature_conventions.md` §d2 requires.

## Symbols

- **Used, shared (not redefined here):**
  - $\mathcal{R}$ (the runs of one cell);
  - $r$;
  - $H_r$ (defined under NCR, which precedes MTTC).
- **New:**
  - $\mathcal{R}_1$: the runs that compromise at least one host. It keeps the draft's own symbol in the tex (l.5525). The subscript reads "at least one host". The alternative is $\mathcal{R}^{+}$.
  - $t_r$: run $r$'s time to its first compromise. It is lower-case $t$ with a time meaning, as in the shared $t_d$. McQueen's own letter $T$ is not free, because $T_r$ is active time.
- **Collision check** (`grep` on `docs/thesis/dissertation.tex`, uncommented lines):
  - `t_r`: 0 live hits (one commented hit, the draft at l.5526);
  - `\mathcal{R}`: 0 live hits;
  - `H_r`: 0 live hits.
  - Chapter 4 has $t_{pq}$ (an immediate transition, two place subscripts) and $R$ (the rule kernel, upright capital). $t_r$ with a run subscript and calligraphic $\mathcal{R}$ are distinct in form. The residual risk of reading $t_r$ as a transition is low, but it is Marc's to judge (Open 3).

## For elsewhere

- **Table 4.3, the Source cell:** change `\citep{mcqueen2006, zhang2023}` to "adapted from \citep{zhang2023}, after \citep{mcqueen2006}" (or "adapted from \citep{mcqueen2006, zhang2023}"). This follows the table's own rule that a stated difference means "adapted from".
- **Table 5.2 (`tab_5-2-1a_unopposed_summary.tex`) prints MTTC without $|\mathcal{R}_1|/|\mathcal{R}|$.** The definition says MTTC is reported with that share. Table 5.2 has to carry it, as a parenthesis the way Table 5.3 does, or as a caption clause. The shares with no defence are 1.00 / 0.99 / 0.92 / 0.95 for $c_1$–$c_4$, 0.99 for $c_{\mathrm{agg}}$, and 1.00 for the baseline (100-seed corpus). This is a licensing gap and not a number change.
- **Table 5.3 (`tab:eff-conditions`)** agrees: its caption says "MTTC is over the runs that compromise a host, and its parenthesis is their share of all runs". That is exactly $|\mathcal{R}_1|/|\mathcal{R}|$. The handoff (entry 7) and the tex S5 comment speak of "the share that compromise none", which is the complement. The definition follows the tables. Align the handoff's wording to it.
- **Chapter 5's reading of MTTC under strong defences:** e.g. IP shuffle, 6 423 s over 24 % of runs. That is a mean conditional on compromise. A condition that stops most runs from compromising anything leaves MTTC over the few that did. The definition says "conditional", so any sentence in chapter 5 comparing MTTC across conditions must read it with the share, and never alone.
- **Appendix `tab:experiment-one`** (l.8550) heads a column "MTTC (s)" with a parenthesised *count* of runs, not a share. It is a pre-§4.5 record. Either key it to Eq. `eq:mttc` with the count explained (as its caption already does), or rename the header.
- **4.5.4:** MTTC is a mean with a normal-approximation 95 % interval, over $\mathcal{R}_1$ only. Say there that the interval is conditional on $\mathcal{R}_1$.
- **Table 3.1 (l.2679)** cites MTTC to `mcqueen2006, zhang2023, ho2024, tay2024, sharma2025` as one family cell. That is fine for the map. §4.5 is where the checkpoint is fixed.

## Open for Marc

1. **The status is adapted, not adopted.** The checkpoint differs from Zhang's reported one, and McQueen's is an analytical expectation. *Recommendation:* adapted, with the Table 4.3 cell changed to match.
2. **The citation order.** Should Zhang (the name and the lineage) lead, with McQueen as the root of the concept, or should McQueen lead? *Recommendation:* Zhang first. McQueen never uses the name, and Zhang's own MTTC source is Cho 2020 [4], not McQueen.
3. **The symbols $t_r$ and $\mathcal{R}_1$.** $t_r$ sits beside chapter 4's $t_{pq}$. *Recommendation:* keep both, since they are distinct in subscript and defined inline. Switch to $\mathcal{R}^{+}$ only if the "1" reads as an index.
4. **Why the first host and not the time to the target.** The draft gives only the design reason: the lineage's checkpoint is the general attack scenario's goal, which is not run here. A clause such as ", which every run that compromises a host reaches" (8 words) would argue the first host over the target without results. The stronger reason (time to target would be defined only in the few runs that reach it) is a result. *Recommendation:* keep it result-free, add the 8-word clause if Marc wants the step walked (voice §c4), and let ASP carry the target.
5. **The length is 121 words against about 100.** *Recommendation:* accept it. If it must be cut, take the two trims under Structure.
6. **Survival-analysis alternative.** A restricted mean or Kaplan–Meier would use the censored runs instead of dropping them. That is a statistics choice for 4.5.4 and not this definition. *Recommendation:* no change for this thesis. If an examiner asks, the share printed beside MTTC is the disclosure.
