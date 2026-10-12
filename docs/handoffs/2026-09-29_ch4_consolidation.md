---
status: open
created: 2026-09-29
supersedes: 2026-09-29_s45_equation_clarity.md (its rulings A–F are applied; its evidence is in git at dc1d4c7f)
---

# Chapter 4 consolidation: open rulings, the §4.3 review, and what chapter 5 now owes

**Goal:** consolidate chapter 4 before chapter 5 is regenerated. Chapter 5 is **stale by Marc's ruling** (2026-09-29: "the evaluation will go stale for the purposes of rewriting and consolidating"). This is the one running document for the session. Add to it; don't fork it.

The writing rule for everything below is `voice.md` §(0): the five checks and "say more with less".

## 1. Applied in this session

- **§4.5 round 4** (DRAFT STATE):
  - the targeted scenario stated in the preamble;
  - the cell defined once, in §4.5.4;
  - APV replaced by **distinct attack paths**: the number of different first-$k$-step sequences among the runs, the count Marc asked for;
  - **attack rate** stated as one rate per run, then the mean;
  - **attack confidentiality** on Snort's default scan rule, five actions within a minute (Jung et al. 2004, §2 and §6);
  - **compromise rate after an MTD deployment** and **time lost per MTD deployment** on the half interval, with a worked example before the equation;
  - statistics under bold run-in labels (Runs, Intervals, Ranking, Ablations);
  - Table 4.3 renamed and unstriped, and placed under the heading;
  - three equations shortened so their numbers fit.
- **Table 4.1** (`tab:gspn-notation`): the Meaning column now names each symbol and no longer re-defines it.
- **"no defence" → "no MTD"**, effective immediately (registry row added):
  - 18 prose lines;
  - 16 generated tables and the 7 generators that write them;
  - 2 figures recompiled.
  - Census after: 0 in live text. Comments keep the history.
- **"sophisticated attacker" → "APT attacker"** at 7 own-voice sites, the §3.3.1 heading and the Table 3.2 caption included. Cho's cited phrase (l.~3533) stays.
- **Bib:** `jung2004` added. The venue was verified by the detector record; **the pages and DOI are unverified**, so add them on read.
- **§4.4.5 vulnerability memory:** the odds equation is now in named quantities ("odds of success after $n$ successes = $k^n$ × odds of success with none"), with $p_0$ and $p_n$ retired and a worked example at an **illustrative $k = 2$** (1 in 2 → 2 in 3 → 4 in 5). **Owed:** $k$ is still undeclared in Appendix B (`adversary.py` l.100, `_exploit_learning_rate = 0.0`, where $k = 1 + \lambda$). Once it is declared, either keep $k = 2$ as a labelled illustration or swap in the declared value.
- **`voice.md` §(0)** gains the mantra, the worked case and "symbols only where they work". The same is in CLAUDE.md and memory.

## 2. Open rulings (recommendation first)

### H. The targeted scenario, and what it does to the metrics

**Facts:**
- Every run in chapter 5 is Brown's targeted scenario. Its success is a compromised target host, and the run ends there (`attack_operation.py` l.748–757).
- The same code also keeps **the general scenario's stop, NCR > 0.8** (l.741–746). Both fire `end_event`.
- **ASP is unaffected:** the analysers count a target only when a database host was reached (`analyse.py` l.254–259, `ch5_defended/analyse.py` l.184). The ratio stop is tallied apart.
- **No-MTD corpus, 100 seeds:** the ratio stop ends 2 of 100 baseline runs and no APT run. The APT model reaches its target in 5–17 % of runs (median time to target 10 500–13 600 s); the baseline in 58 % (9 360 s).
- **Defended corpus at 2 000 s**, APT pooled over $c_1$–$c_4$, 400 runs a cell: ASP is 0.00 (host topology) to 0.09 (no MTD, OS diversity, user shuffle). The baseline's is 0.20–0.72.

**A correction first.** The repo's *internal MTTC* is **not** the reading Marc described. It is Ho's mean duration of one attack event (`metrics_semantics.md` §(a)), which the thesis already dropped. What Marc described is Zhang's: "the time it takes for an attacker to compromise a target host" (§3.4, p. 16), read at 80 % of hosts in Zhang's general-scenario runs (§5.1, p. 33).

**H1 RULED 2026-09-30 (Marc): target host, over the runs that take one; applied on
chore/s5-results-asp (see 2026-09-30_disruption_metrics.md).**

**H1. MTTC. Recommend: read MTTC at a target host**, the targeted scenario's objective in Zhang's own words, printed beside ASP (which is its coverage), with "—" where no run succeeds.
- Cost: under MTD it rests on few APT runs. At 2 000 s that is 0–36 of 400 today, and ten times that at 1 000 seeds.
- For host topology it is undefined.
- Alternative: keep the first host. It has full resolution, but it needs a justifying sentence and is not what a reader expects MTTC to mean in a targeted scenario.
- **Overturns** the 2026-09-24 first-host ruling on merit (the scenario).

**H2. The 80 % stop inside targeted runs. Recommend: remove it from targeted runs at the next corpus run**, so each scenario has one stop.
- First classify it against `mtdsim_intent_spec.md` (Brown's targeted termination): the comment at l.748 re-enabled the target stop on 2026-08-30 and left the ratio stop running beside it.
- Effect: at most the few baseline runs that reach 41 hosts before their target.
- Then the preamble's sentence "The simulator also keeps the general scenario's stop" is cut.

**H3. NCR in the targeted scenario. Recommend: keep NCR reduction as the ranking metric, and read it as hosts compromised on the way to a target.** §4.5 now says this in one clause.
- ASP cannot rank the MTD mechanisms for the APT model: it sits at 0.00–0.09 under every condition.
- ASP and NCR can disagree in sign. For the baseline under IP shuffle at 2 000 s, ASP rises from 0.60 to 0.65 while NCR falls from 0.49 to 0.41. So they measure different things, and ch5 must not read one as the other.

### I. Generic "defence" and the ratified "defence mechanism"

Marc: "every instance of defence could be MTD, unless we're talking about defence as a concept".

Census, live text:

| Term | Prose | Generated tables | Generators |
|---|---|---|---|
| *defence mechanism* | 24 | 1 | 2 |
| *the/a/each defence* | about 32 | — | — |

The ch2 heading "Defence mechanisms" and the ch5 heading "Defence mechanisms and execution schemes" are also affected.

**Recommend:**
- ***MTD mechanism*** for *defence mechanism* everywhere, including the two headings. This **overturns** the 2026-09-07 registry row on merit: Marc's specificity rule.
- Generic *the/a/each defence* goes case by case, to *MTD*, *the MTD mechanism* or *the condition*.

One sweep; ask once. Not applied, because the headings and the registry row are ruled surfaces.

### J. Attack confidentiality: how the sweep is shown (Appendix C.4, now a placeholder)

**Recommend** one small table: one row per rule, one column per attacker, the Snort default row first. The rules are the count $N$ = 3, 4, 5, 6 within 60 s ("per minute", matching the attack rate) and Snort's medium window, 5 within 90 s.

100-seed numbers, % of actions not flagged, from `data/results/s45_metric_redesign/stealth_count.py`:

| Rule | $c_1$ | $c_2$ | $c_3$ | $c_4$ | baseline |
|---|---|---|---|---|---|
| **5 in 60 s** | 92 | 96 | 98 | 89 | 83 |
| 3 in 60 s | 63 | 73 | 79 | 57 | 36 |
| 4 in 60 s | 82 | 90 | 93 | 78 | 58 |
| 5 in 90 s | 84 | 91 | 95 | 79 | 68 |

The order holds in every row.
- Name: keep **attack confidentiality** (Zaffarano, cited). *Detectability* is Jafarian's ratio of scans with and without MTD, a different quantity.

### K. The name *attack rate*

**Recommend: keep it.** It is Zhan's term, cited. *Attack action rate* would be an invented variant.

It is not time-resolved: one rate per run (actions over run length), then the mean over runs. §4.5 now says so.

## 2b. Marc's third read (2026-09-29): new rulings F′, L, J′

**Applied:**
- §4.4.5 now says why the odds form never caps: "the odds have no upper limit, and the chance is the odds over one plus the odds".
- Distinct attack paths counts the paths the runs **realise**, "not the paths the attack graph allows".
- Snort is named as an intrusion detection system, and its port-scan rule is the detector (the overlap is deliberate).
- Attack confidentiality states its direction: "a higher attack confidentiality is a stealthier attacker".
- `voice.md` §(0) has the **inverted U**: too short is as vague as too long; restore the referent, not the nuance.

### F′. Replace the compromise rate after an MTD deployment and time lost per MTD deployment. Supersedes F.

Marc: "structurally lost … what rate? … I don't think anyone can replicate that". His model of the cost is the time between successful tactics. After a deployment the action fails, and the Petri net retraces until a tactic dispatches the equivalent action again.

The census (`mtd_metric_catalogue.md` §(a), §(b)4) has **no attacker-side recovery metric in the field**. It does have **Brown 2023's attack actions blocked** (§IV-A p.5, Fig. 4, "total actions blocked"; §III-D defines a block as the MTD cutting off something the action needed). In MTDSim a block is the interrupt: an action a deployment cuts off while it runs.

**Recommended pair, both event-based and replicable:**

1. **Attack actions blocked** (Brown's, cited): the attacker's actions an MTD deployment interrupts, per run.
2. **Time to resume a blocked action** (introduced; the name says what it does): the time from the end of a blocked action to the start of the attacker's next run of the same action. The median is taken over the cell's blocked actions, beside the attacker's usual gap between two runs of the same action with no MTD. A blocked action never run again counts as longer than every resumed one.

**Dry run** (2 000 s, 100 seeds; `data/results/s45_metric_redesign/blocked_resume.py`):

| cell | blocked per run | deployments that block an action | resume median | resumed before run end |
|---|---|---|---|---|
| APT, IP shuffle | 2.81 | 35 % | 444 s | 92 % |
| APT, complete topology | 3.07 | 38 % | 373 s | 94 % |
| APT, host topology | 3.10 | 39 % | 367 s | 96 % |
| APT, port shuffle | 1.24 | 15 % | 147 s | 99 % |
| APT, OS diversity | 1.18 | 15 % | 141 s | 98 % |
| APT, service diversity | 1.21 | 15 % | 136 s | 98 % |
| APT, user shuffle | 0.09 | 1 % | 149 s | 97 % |
| baseline, IP / complete / host topology | 5.3–6.4 | 67–81 % | 55 s | 98–99 % |
| baseline, port / OS / service | 5.4–6.9 | 68–87 % | 45 s | 100 % |
| baseline, user shuffle | 0.41 | 5 % | 93 s | 100 % |

The usual gap between two runs of the same action with no MTD is 136 s for the APT model and 93 s for the baseline.

**How the table reads:**
- A deployment catches the APT model in flight far less often: it is in dwell-only tactics much of the time.
- When a host-layer deployment does catch it, the APT model takes about three times its usual gap to run the action again (the retrace).
- The baseline restarts at once, sooner than its usual gap.

**Known limit, to state:** resume time records the interruption, not its downstream consequence. The baseline's service-diversity cost (time lost 461 s under the old metric) comes from exploits failing *after* it resumes, so NCR reduction carries it.

**Draft tex, for ruling:**

```latex
\paragraph{Attack actions blocked.}
Attack actions blocked is Brown's count of the attacker's actions that MTD
blocks \citep[Sec.~IV-A]{brown2023}: here, the actions an MTD deployment
interrupts while they run (Section~\ref{subsec:runtime-mechanics}), per run:
\begin{equation}
  \text{attack actions blocked} = \operatorname*{mean}_{\text{runs}}
  \left( \text{actions interrupted by an MTD deployment} \right).
\end{equation}

\paragraph{Time to resume a blocked action.}
Time to resume a blocked action is the time from the end of a blocked action
to the start of the attacker's next run of the same action. After a block the
APT attacker model's Petri net routes on a failure
(Section~\ref{subsec:failure-matrix}) until a tactic dispatches that action
again; the baseline attacker restarts its procedure. It is the median over the
blocked actions of every run, reported beside the attacker's usual gap between
two runs of the same action with no MTD:
\begin{equation}
  \text{time to resume} = \operatorname*{median}_{\text{blocked actions}}
  \left( \text{start of the next run of the action} -
         \text{end of the blocked action} \right).
\end{equation}
A blocked action the attacker does not run again before its run ends counts as
longer than every resumed one.
```

**Blast radius (chapter 5, stale anyway):**
- `disruption.py` retires; the dry-run script becomes the reader.
- Figure 5.3 is redrawn: bars of resume time per mechanism per attacker, the usual gap as a reference line, and blocked per run as a panel or table column.
- Table C.5 (the window sweep) is deleted, since the new metrics have no window.
- The prose at §5.3.1 (l.~7868, 7967ff.) and §5.4's "494 s" change.
- The Table 4.3 and Table 5.1 rows are renamed.
- `ablation.py` imports.

### L. ASP reduction or NCR reduction?

Marc: ASP is the targeted scenario's own outcome, so should effectiveness be ASP reduction? 100-seed dry run, 2 000 s:

| mechanism | APT: ASP reduction | APT: NCR reduction | baseline: ASP reduction | baseline: NCR reduction |
|---|---|---|---|---|
| host topology | +1.00 | +0.17 | −0.08 | −0.07 |
| complete topology | +0.89 | +0.16 | −0.15 | −0.13 |
| IP shuffle | +0.56 | +0.33 | −0.08 | +0.16 |
| port shuffle | +0.22 | +0.01 | +0.02 | +0.03 |
| service diversity | +0.22 | +0.04 | +0.67 | +0.30 |
| OS diversity | 0.00 | −0.01 | −0.12 | −0.02 |
| user shuffle | 0.00 | −0.03 | −0.20 | −0.08 |

**It does change the calculus in places:**
- For the APT model the same three host-layer mechanisms lead under both, but the order inside that group flips: ASP puts host topology first, NCR puts IP shuffle first.
- For the baseline, ASP says only service diversity stops it reaching a target. IP shuffle cuts the hosts it takes (+0.16) but not its success (−0.08).

**Resolution:** APT successes are few, e.g. 0 of 400 under host topology, so a reduction of exactly 1.00 has no interval. At 1 000 seeds, no MTD gives about 360 successes of 4 000.

The Scott–Knott ESD ranking assumes a continuous measure (hosts per seed). A binary success would need a proportions test instead.

**Recommend:** define **ASP reduction** in §4.5.3 as the scenario's effectiveness metric (same Alavizadeh form, ASP in place of NCR). Keep **NCR reduction** beside it as the ranking basis, read as "how much of the network MTD keeps the attacker from on the way". Chapter 5 then reports whether MTD stops the target (ASP reduction) and how much of the network it saves (NCR reduction).

The alternative is to rank on ASP reduction with a proportions test. It is more aligned, but its resolution is poor for the APT model and it changes the statistics section.

On *define both scenarios' ASP?* No: define the one run (targeted). NCR already reads in targeted terms.

### J′. Appendix C.4: drop it. Supersedes J.

Snort's default has precedent (Jung 2004 §6), so no sweep appendix is needed. One sentence in §5.2 can say the ordering holds from 3 to 6 actions per minute; the evidence is in `stealth_count.py`. Then delete `app:detector-memory` and §4.5's pointer to it.

## 2c. Marc's fourth read (2026-09-29): round 5 applied

**Applied to chapter 4** (DRAFT STATE):
- **§4.4.5 odds, for a CS reader:** "the odds are the number of successes expected for each failure". The example does the arithmetic: odds 1 → 2 → 4 is 1 in 2 → 2 in 3 → 4 in 5. The "no upper limit / odds over one plus the odds" wording is cut.
  - **Alternative, not applied:** replace the odds rule with "each earlier success divides the chance of *failure* by $k$" (1 − p₀ becomes (1 − p₀)/kⁿ). It parallels Zhang's halving of exploitation time, needs no odds, and also never passes certainty.
  - It changes `adversary.py`'s learning rule. No reported number moves, since the memory is off in every run so far.
  - **Marc's call.**
- **ASP reduction is the headline and the ranking basis.** Marc: "we're running the targeted scenario … NCR is a backup metric". This rules L in its "all the way" form.
  - The ranking is Scott–Knott ESD on each run's success (1 or 0), with Cohen's $h$ (his effect size for two proportions, same book) in place of $d$.
  - NCR reduction is kept as "the same comparison on NCR".
  - The attack-outcome lead-in now says ASP is the targeted scenario's outcome, with NCR and MTTC beside it.
- **Time lost per MTD deployment retired.** Its content is the depth of the same curve, and Marc could not follow it. This supersedes F and F′.
- **One metric backs Figure 5.3:** the compromise rate after an MTD deployment, re-defined with every referent:
  - the compromise rate is "hosts compromised per hour";
  - $I$ is the deployment interval (Table 5.1), and the time between two deployments is split in half;
  - why the counts are totalled: compromises are rare, and one deployment's window seldom holds one;
  - direction: 100 means unchanged, falling towards 0 the more the deployment slows the attacker;
  - the no-MTD reference;
  - eight equal slices of $I/2$ trace the drop and the recovery (125 s at 2 000 s, derived rather than chosen).
  - Marc's calculus question: a count of compromised hosts is a step function, so its derivative is zero except at the jumps. A rate therefore has to be counted over a window. This is why the "before" and "after" exist.
- **Attack actions blocked** (Brown 2023) added. Marc: "that's fine".
- **Run count and seeds moved** from §4.5.4 to §5.1 Runs (Marc: they duplicated each other). §4.5.4 keeps Intervals, Ranking and Ablations; the cell is defined in the §4.5 preamble.
- **Table 4.3 and Table 5.1** list ASP reduction, NCR reduction, attack actions blocked, and the compromise rate after an MTD deployment.

**Chapter 5 owed, added by round 5:**
- Analysers:
  - ASP reduction with bootstrap intervals;
  - Scott–Knott on per-run success with Cohen's $h$ (`sk_esd.py`), then re-derive Table 5.3's rank grid;
  - attack actions blocked per run (`blocked_resume.py` has the counting rule).
- `disruption.py`: the before window becomes $I/2$ (was 750 s), after-slices $I/16$, and `_time_lost` is retired.
- Figure 5.3:
  - (a, b) keep the curve;
  - (c) becomes the compromise rate after an MTD deployment over the whole $I/2$, per mechanism per attacker, beside its no-MTD value. Dry run: APT 53 % under IP shuffle against 101 % with no MTD; baseline 49 % under service diversity against 95 %.
- Delete Appendix C.5 (`app:timelost-window`), whose window sweep no longer applies.
- The prose at §5.3.1, §5.4's "494 s" and chapter 6 mentions of time lost.
- **H1 is now narrower:** MTTC is a secondary metric beside ASP. Whether it reads at the first host or the target is still open.
- **J′ is still open:** "Appendix C.4 varies the count and the window" stays in §4.5 until it is ruled.

## 3. §4.3 formalism review (from paragraph two): proposals, none applied

**What a formalism section needs:**
1. the standard definition, cited (the GSPN tuple, Ajmone Marsan);
2. how an attack profile compiles to it, one line per element;
3. the one extension (verdict conditioning), with its equation;
4. where the token starts.

Implementation equivalences, forward-compatibility clauses and construction details of other sections are not formalism.

| # | Proposal | Why | Cost |
|---|---|---|---|
| F1 | **Collapse the verdict family.** $F=\{F_v : v\in V\}$ with $F_{\text{success}}=F_{\text{none}}=1$ becomes one failure matrix $F_{\text{failure}}$: on a failure verdict $W(t_{pq})=w_c F_{\text{failure}} / \sum w_c F_{\text{failure}}$, otherwise the base weights stand. | Three of four symbols do no work (the "blah" test). | 3 uses of $V$, 6 of $F_v$, 1 each of $F_{\text{success}}$ and $F_{\text{none}}$; two Table 4.1 rows go |
| F2 | Cut *tangible* / *vanishing* (2 uses each); keep "decision place, left in zero time". | Terms defined for one use. | none |
| F3 | Cut "$T_I$ is the set of pairs with $w_c>0$. The implementation carries every pair … the two nets are the same object in execution." | An implementation equivalence, not the formalism. | none |
| F4 | Reduce the token/AND/concurrency sentences to one: "The net carries one token: the attacker pursues one line of the campaign at a time." | Nuance the reader does not need. | none |
| F5 | Fold item 4 ($I$ and $O$) into item 2's line: "arcs $p\to\tau_p\to\hat p\to t_{pq}\to q$, each of weight one". | One line where there are two. | none |
| F6 | Move "An operator with several attack flows counts once … 29 of the 38 attack flows carry weight" to §4.2 (attack profiles). | Corpus construction, not the net. | one sentence moves |
| F7 | Move "A timed transition may also be cut short by an MTD deployment …" to §4.4.1; cut "Any further declared factor multiplies … none does in the runs this dissertation reports". | Runtime, and forward-compatibility. | none |
| F8 | Redraft the overlay paragraph ("We can assume that they perform these because we know they do that … nothing detects pre-intrusion activity anyway"). | Spoken register. It is Marc's dictation, so it is his to re-dictate; the content points are: what the overlay adds, $\sigma$ = 0.1 declared, and why (§3.1). | Marc |
| F9 | Keep the tuple Eq. 4.1 and Eqs. 4.2–4.3. | This is the formalism the examiner expects. | — |

## 4. Chapter 5 owed (stale by ruling; do after chapter 4 is settled)

- **Attack rate per minute in the §5.2 prose** (l.~7430: "11.7 to 20.7 actions per 1 000 s against 28.4"): 0.70–1.24 against 1.71. Table 5.2 is already regenerated.
- **Distinct attack paths:**
  - Figure 5.1(b) and its caption ("Attack path variation by opening length");
  - the prose at l.~7191 (the 22 %, 70 % and 32 % reading).
  - The analyser already records `distinct_openings`. At 100 seeds: baseline 1, 1, 1, 1, 2, 2, 2, 2 for $k$ = 1–8; $c_1$ reaches 76 at $k$ = 5 and 100 (every run) at $k$ = 8. The count saturates at the run count.
- **Attack confidentiality:**
  - `analyse.py`: the count rule replaces `_detector_levels`, `confidentiality_over_run` and the θ median;
  - a Table 5.2 column;
  - retire or re-bin Figure 5.2 (l.~7453) and its caption ("alarm tuned so that it flags half");
  - the §5.2 prose (l.~7429: 69–93 %, 43 %);
  - Appendix C.4 (l.~9851) is now ruling J's table.
- **Deployment response:**
  - `disruption.py`: `EDGES` to the half interval, and time lost in the one-slice form (identical to the ratio; the dry run is `data/results/s45_metric_redesign/rate_ratio.py`);
  - `ablation.py` imports it;
  - Figure 5.3: y-axis and caption "NCR growth rate" → "compromise rate after an MTD deployment" (l.~7954);
  - the §5.3.1 prose (l.~7868, 7967ff.);
  - §5.4's "494 s" (l.~8545);
  - Table C.5, re-based on the split.
  - A half-interval window is defined at 200 s too.
- **MTTC:** follows ruling H1. It needs the Table 5.2 coverage (ASP beside it, or a runs-with-a-compromise column).
- **The run-end sentence** in the §4.5 preamble follows ruling H2.
- **The "defence" sweep** in ch5 floats and generators follows ruling I.
- **The 1 000-seed overnight run** regenerates every `\prelim` number.

## Validation gate

- Rulings H–K recorded.
- §4.3 proposals ruled and applied.
- The chapter 5 owed list emptied.
- The build is clean.
- The voice gate (§0 first) passes on chapter 4.

## Reading list

- `docs/workflows/voice.md` §(0).
- `dissertation.tex` §4.3 (l.~4635–4960) and §4.5 (l.~5637–5850).
- `data/results/s45_metric_redesign/README.md`.
- `docs/sources/extractions/s45_metric_definitions/13_source_equations.md` and `14_detector_conventions.md`.
