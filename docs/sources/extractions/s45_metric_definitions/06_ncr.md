# §4.5.2 Network compromise ratio (NCR): drafting agent 06

## LaTeX

```latex
\paragraph{Network compromise ratio (NCR).}
NCR, as defined by \citet[p.~32]{zhang2023}, is the share of the network's hosts
the attacker has compromised; \citet[Eq.~10]{ho2024} calls it the host
compromise ratio.
Over the runs of a cell,
\begin{equation}
  \mathrm{NCR} = \frac{1}{|\mathcal{R}|} \sum_{r \in \mathcal{R}} \frac{|H_r|}{N},
  \label{eq:ncr}
\end{equation}
where $H_r$ is the set of hosts run $r$ has compromised by its end and $N = 50$
is the number of hosts.
NCR lies in $[0, 1]$; lower is better for the defender.
A run ends when a target falls, when $|H_r|/N$ exceeds 0.8, or at the time limit
(Table~\ref{tab:experiment}).
The 0.8 checkpoint is Zhang's, for the general attack scenario, where taking the
network is the goal; under the targeted attack scenario NCR reads how much of the
network the attacker has taken when its runs end, and ASP gives the share of runs
that ended on a target.
```

Word count: about 130 words of prose (the display equation excluded; citations counted as one word). The adopted core (name, status, equation, range and direction) is about 65 words. The rest is the two sentences the brief requires: the checkpoint, and Marc's owed sentence on the general and targeted attack scenarios.

## Structure

- **S1 + S2 merged.** The name, the status ("as defined by") and the citation sit in the sentence that says what NCR measures. The corpus's shortest adopted definitions do the same (Ho gives the name and the ratio in one sentence). The Ho clause names the same ratio under Ho's name. It is there because Table 4.3 cites Ho for NCR, and Ho never uses that name (see Verification).
- **S3.** The operation is a mean over runs of $|H_r|/N$, with a "where" clause defining the two symbols this definition owns. $\mathcal{R}$ ("the runs of a cell") is assumed defined in the opener or symbols table.
- **S4.** The range and direction go in one sentence.
- **S5.** There are two sentences. The first states the checkpoint precisely, as the three ways a run ends. The second is Marc's owed sentence: the lineage's scenario against ours, and what ASP adds. No edge case is needed. $N$ is constant and never zero, and a run with no compromise counts as 0, which the equation already says.
- **S6.** Not applicable (adopted). The one thing a lineage reader could misread is that Zhang uses NCR as a stopping rule, not as a reported value. S5's last sentence carries that disclosure (convention §d2).
- **Length.** Over the adopted budget of 40–80 words by the two required sentences. The core is within it. To tighten further, dropping the Ho clause saves about 10 words (Open 2).

## Verification

### Sources

| Claim | Source and locator | Verbatim quote | Verdict |
|---|---|---|---|
| Zhang defines NCR as the ratio of compromised hosts to all hosts | Zhang 2023, §5 *Evaluation*, printed p. 32 (PDF p. 33); `docs/sources/lit_review/zhang2023.md` l.420; confirmed against `original/GENG5512Report_Zhang_22792191.pdf` | "we use Network Compromise Ratio (NCR) as the simulation checkpoint to evaluate MTD techniques and their combinations. NCR is the ratio of compromised hosts to the total number of hosts in the network." | holds |
| Zhang uses NCR as the checkpoint that ends a run, at 0.8 | same passage | "we set the terminating condition for the simulation as the NCR reaching 0.8 and run the simulation 100 times for each variable set" | holds |
| Zhang reports the time to that checkpoint, not NCR itself | Zhang 2023, Fig. 8 caption, printed p. 34; Fig. 10, p. 36 | "Figure 8: Single MTD Evaluation - Mean Time to Compromise on 0.8 NCR" | holds. NCR is never a reported outcome in Zhang, only a stopping rule (the catalogue agrees: `mtd_metric_catalogue.md` (b)3, "in the lineage NCR is a stopping rule") |
| Zhang gives no equation for NCR | whole of `zhang2023.md` and the PDF text; NCR appears only in prose at p. 32 and in two figure captions | (absence) | holds. Equation 4.x is ours in Zhang's words; Ho's Eq. 10 gives the form |
| Ho's Eq. 10 is the same ratio | Ho 2024, §3.3.2 *Features*, item 4, Eq. (10), printed p. 19 (PDF p. 20); md l.350; confirmed against `original/GENG5512Report_Ho_22701889.pdf` | "4) Host Compromised Ratio (HCR): The ratio of hosts that are compromised in the system. The ratio is calculated by: HCR = Ct / Thost (10) where Ct is the number of compromised hosts at time t and Thost is the total number of hosts in the network." | holds for the quantity |
| Ho calls it NCR | full text of Ho's PDF, searched for "NCR" and "network compromise" | 0 hits | **fails**. Ho's name is HCR, spelt "Host Compromised Ratio" at Eq. 10 and "Host Compromise Ratio" in Table 5 (printed p. 22). The draft says so, using the Table 3.1 / Table 5 spelling |
| Ho's HCR is a selector feature, not an evaluation metric | Ho 2024, §3.4.2, printed p. 23 | "The four evaluation metrics are Attack Success Rate (ASR), Return on Attack (ROA), Attack Path Exposure (APE), Risk (R)." | holds. So Ho is cited for the ratio's definition only, never as a precedent for reporting it |
| Ho reads HCR at an arbitrary time $t$ | Eq. 10's "where" clause, above | "Ct is the number of compromised hosts at time t" | holds. Reading the ratio at the run's end is choosing $t$, which the definition licenses |
| The general attack scenario's end is Zhang's 80 % | `dissertation.tex` l.986–995, Table 2.5 (`tab:attacker-objectives`) | "the general scenario's termination ratio is Zhang's"; "General & compromise the network: 80\,\% of the hosts" | holds (thesis-internal, already cited) |
| The name is used outside the MTDSim lineage | `extractions/metric_census/F_web_open_access.md` l.68, l.137 | "I found no source for the exact name 'network compromise ratio / NCR'" | partly. The name belongs to the lineage only (Zhang's master's thesis). Nearest outside it: Cheng 2014's *compromised host percentage* (census F, not held) |

### Code: each term of Eq. `eq:ncr`

| Term | Where computed | Verdict |
|---|---|---|
| $\lvert H_r\rvert$, APT attacker model | `src/mtdsim/l3_simulation/movement/run.py:533` (`compromised_count=len(adversary.get_compromised_hosts())`) → `data/results/ch5_defended/run_corpus.py:197` (`"compromised"`) → `analyse.py:177` (`"hosts"`); §5.2 corpus the same (`ch5_s531_unopposed/analyse.py`, `r.compromised_count`) | matches |
| $\lvert H_r\rvert$, baseline attacker | `run_corpus.py:290–294`: distinct `compromise_host_uuid` over the attack records (`"compromised_uuid"`) → `analyse.py:256`. It is identical to the positional list in every run (`numbers.json` sanity `baseline_uuid_vs_positional_hosts_differ: 0`) | matches |
| Distinct, never lost | `mtdnetwork/operation/attack_operation.py:728–729` appends a host only if it is absent. Nothing removes from the list (grep: the only mutation is the id remap in `adversary.py:106–137`, for host topology shuffle, which keeps the foothold, D-02). `movement/attacker.py:240–242` asserts the count is monotone and ends equal to `compromised_count`. Compromise events equal distinct hosts on the current no-defence corpus (3 252 = 3 252 for the model, 2 434 = 2 434 for the baseline; checked read-only). So "ever compromised" and "held at the end" are one quantity | matches ("has compromised by its end") |
| Entry host | The attacker starts outside the network: its pivot is −1 (`attack_operation.py:311, 720`) and it first attacks the exposed endpoints. No foothold is pre-counted, and $\lvert H_r\rvert = 0$ occurs (4 % of the APT attacker model's no-defence runs; MTTC's share) | matches |
| $N = 50$ | `run.py:62` `GEOMETRY total_nodes=50`, shared by the baseline (`run_corpus.py:245`). None of the seven mechanisms adds or removes hosts. The readers divide by 50: `ch5_s531_unopposed/analyse.py:340, 489` (`NET_HOSTS`) and `tools/ch5_effectiveness_figures.py:231` | matches |
| $\frac{1}{\lvert\mathcal{R}\rvert}\sum$ | `analyse.py:331` (`hosts_of`) → `_iv` mean; printed as mean/50. The mean of $\lvert H_r\rvert$ over 50 equals the mean of $\lvert H_r\rvert/N$ exactly | matches |
| The checkpoint | `mtdnetwork/component/time_network.py:55` (`len(compromised)/total_nodes > 0.8`), checked at `attack_operation.py:742–747` **before** the target check at :754–757, in **both** scenarios. The attacker stops on `end_event` (`attack_operation.py:110, 241`). Time limit `HORIZON = 15_000` (`run_corpus.py:53`). How runs ended in the §5.2 corpus (`ch5_s531_unopposed/numbers.json`, `core/table/*/ended`): the APT attacker model only on a target or the time limit (its maximum is 28 hosts across the defended core corpus); the baseline attacker on a target 0.58, **the 0.8 checkpoint 0.02**, the time limit 0.40. In the defended core corpus, 117 of 6 900 baseline runs exceed 40 hosts | matches the drafted sentence. **Mismatch with Table 5.1**, which lists only the target and the time limit |

**Status check.** Adopted is honest. The quantity (compromised hosts over all hosts) is Zhang's in words and Ho's Eq. 10 in symbols, unchanged. What is ours is the reading moment, the end of the run (Ho's "at time $t$" licenses any $t$), and the role: a reported value, where Zhang's is a stopping rule. That is a stated checkpoint, as with MTTC, and not a changed quantity, so "adapted" would over-claim a change. The name is used as Zhang uses it. Citing Ho **for the name** is not accurate, which is why the draft names Ho's HCR. Tay's HCR is a different quantity ("compromised or at high risk", census B l.126) and is correctly not cited.

## Symbols

- **Used:** $\mathcal{R}$ and $r$ (shared; assumed defined earlier). $H_r$ and $N$ are **defined here**, as the brief assigns.
- **New:** none.
- **Collision check.** A Python scan of every non-comment `$…$` in `dissertation.tex` finds no live $H$, $H_r$, $N$ or $\mathcal{R}$. The only hits are $\mathcal{N}_c$ (l.4509, 4544, 4671, 4788), a distinct glyph, and $N$ is not in `tab:gspn-notation`. There is a visual neighbour ($N$ against $\mathcal{N}_c$) but no clash.
- **Consistency with 09.** Agent 09 (NCR growth rate) writes $\mathrm{NCR}_r(t) = |H_r(t)|/N$, with $H_r(t)$ the hosts compromised by time $t$. That is consistent: $H_r$ here is $H_r(t)$ at the run's end. The handoff's older $H(t)$ (a count, not a set) should not be used.

## For elsewhere

- **Table 5.1 (`tab_5-1a_experiment.tex` l.114).** The time-limit cell says "a run ends earlier if the attacker compromises a target". It omits the inherited 0.8 checkpoint, which ends 2 % of the baseline attacker's no-defence runs in the §5.2 corpus. Add "or compromises more than 80 % of the hosts". Also, §4.4 l.4855 ("the run ends when a target is compromised") is about the APT attacker model only, so it is true as written.
- **ASP: a code mismatch, for agent 05 and Marc.** `ch5_defended/analyse.py:1032` and `:1078` compute ASP as the mean of `r["reached"]`, which is `end_event.triggered` (`run_corpus.py:295`). For the baseline attacker that includes runs ended on the 0.8 checkpoint with no target taken. The §5.2 reader excludes them (`ch5_s531_unopposed/analyse.py:255–258, 282`, `target_reach`). Effect: the no-defence baseline reads 60/100 in the defended corpus against 58 target hits, and 92 baseline core runs across conditions count as reached with no target. The defended tables (5.3, F-1, the §5.3.2 ranking table) therefore overstate the baseline's ASP slightly. The fix is the §5.2 rule (`reached_target`, already computed at `analyse.py:259`).
- **NCR reduction (agent 08).** Its "why NCR, not ASP" clause is the brief's like-with-like point: under a defence the APT attacker model's runs mostly reach the time limit, so NCR compares like with like. It belongs there, not in this definition.
- **Table 4.3 source cell.** `\citep{zhang2023, ho2024}` is acceptable only because §4.5 now names Ho's HCR. If Marc drops the Ho clause (Open 2), drop `ho2024` from this row and from NCR reduction's row too.
- **Placeholder and brief wording.** The `\paragraph` placeholder (l.5511) says "Zhang et al.~2023 and Ho et al.~2024". Both are single-author theses (the bib entries: Zhang, Wenxiao; Ho, Wai Him). Never write "et al." for either.
- **Page locator.** `tab_2-2b_lineage_configurations.tex` l.26 cites Zhang's checkpoint at "p.33", which is the PDF page. The printed page is 32. Use one convention thesis-wide; this draft uses printed pages (Zhang p. 32; Ho p. 19).
- **Chapter 5's uses are licensed.** Table 5.2 (NCR per profile, mean ± interval), Table 5.3 and F-1 (NCR per condition), and the lineage table (§5.3.3, general attack scenario: the definition's end rules cover that scenario too).

## Open for Marc

1. **Declare the inherited 0.8 checkpoint under the targeted attack scenario.** Recommend: declare it, as drafted and in Table 5.1. It is in the simulator, it ends 2 % of the baseline attacker's no-defence runs, and it caps that attacker's NCR at 0.82. Removing it would need a re-run.
2. **Keep Ho's citation for NCR?** Recommend: keep, with the naming clause as drafted. Ho supplies the only equation for the ratio, and the clause makes the name difference explicit. The alternative, citing Zhang alone, saves about 10 words.
3. **ASP counts checkpoint-ended runs as successes in the defended reader.** Recommend: switch `_metrics` to `reached_target` before the 1 000-seed run (this belongs to the ASP owner, and the ruling is yours).
4. **Page convention (printed or PDF) for the lineage theses.** Recommend: printed pages.
