---
status: open                  # the brief for WRITING §4.5 — every metric defined in the method; Marc's plan (2026-09-24): results first, then fit the definitions to the settled list. Work in progress: add entries as metrics are ruled
created: 2026-09-24
updated: 2026-09-24
parent: the metrics design handoff (2026-09-22_metrics_provenance_and_instrumentation.md, RETIRED 2026-09-24 into this brief; implementation commits 23624188, e081a49c, 7f8cb105, 8d04fe12; full text in git history)
evidence: ../sources/extractions/mtd_metric_catalogue.md (the verdict and the source behind every entry)
---

# Define every metric in §4.5 *Evaluation metrics* — in the formalism's symbols, with its source, and why where it is ours

## Goal

§4.5 holds one definition per metric the evaluation reads — all ten of Table 4.3, the cited ones included — so that the table only has to name them and a reader can place every one in the field. This is the convention the field follows and this thesis has adopted (`docs/workflows/literature_conventions.md` §d, anchored in hong2018, which defines its whole metric family in its method with equations, pp. 40–41). Marc, 2026-09-24: "we can define every single metric in the method and then that will make Table 5.2's job easier"; "results first, and then I'll backwards fit once I've got the complete list of metrics down"; "strictly defensible … so anyone reading the paper can be like, oh yeah, that's what they're doing."

**Not this brief's job:** changing any metric, number or float (they landed 2026-09-24); the prose voice (Marc dictates; this brief supplies content points only).

## State of play

- **§4.5 is *Evaluation metrics*** (`\label{sec:evaluation-metrics}`, renamed 2026-09-24 from *Instrumenting MTDSim*), with a placeholder, the metrics table, and **three subsections, one per class** — *Attacker behaviour* (`subsec:metrics-behaviour`), *Attack outcome* (`subsec:metrics-outcome`), *MTD effectiveness* (`subsec:metrics-effectiveness`) — each holding a "definitions owed" placeholder. The older comment block with the 2026-09-23 content points sits below; this brief supersedes it.
- **The metrics table moved into §4.5** (Table 5.2 → **Table 4.3**, `tables/tab_4-5a_metrics.tex`, label `tab:metrics` kept): Class · Metric · Source, the class a level first column, no definition column — the definitions are this brief's job. §5.1 now only points to it.
- **§5.2's floats and §5.3's labels** carry these metrics (Figure 5.1's three panels, Table 5.3; NCR reduction, attack actions blocked, recovery time in §5.3). Numbers are 100 seeds until the 1 000-seed run.
- **Appendix C** has the owed sweep's section, `app:detector-memory`, as a placeholder.
- **Bib:** `zhan2013`, `pendleton2016`, `ward2018`, `jafarian2015` added (names as the sources print them; `pendleton2016`'s wording to confirm in the published version). Every other source below is already in the bib.

## What each definition must carry

1. The field's name, and its acronym where the field has one (ASP, NCR, MTTC, APV). No invented acronym: attack rate and attack confidentiality have none; *AC* is taken by attack cost.
2. **A numbered display equation in the formalism's symbols** — the run, its records, the places $p$, the verbs $\varphi(p)$ — so the metric reads as part of the model, not beside it.
3. Its direction (which way is more, or better for the defender).
4. Its source, cited.
5. For an **adapted** metric: the one difference from the source that matters, stated at the definition (convention §d2 — a field name is never reused with a changed meaning silently).
6. For an **introduced** metric: what it captures and why no cited metric does (E3).
7. **Reader level.** The census's finer distinctions (Ho's per-attempt ASR, the five MTTCs of the lineage, Brown's in-flight blocks) stay in the catalogue; the thesis states our definition, its source and the one difference that matters.

### Symbols (proposal; ruling owed, Open 1)

Taken in chapter 4 (`tab:gspn-notation`): $c$, $\mathcal{N}_c$, $p$, $\hat{p}$, **$\tau_p$**, $t_{pq}$, $\mu_p$, $w_c$, $s$, $M_0$, $v$, $F_v$, $\varphi$, $R$, $d$, **$\gamma$, $\delta$**, $z$. So the detector's memory **cannot be $\tau$** as in the records and the analyser (`TAU`); proposed:
- $\kappa$ — the detector's memory, in seconds (60 s);
- $\theta$ — the alarm level;
- $k$ — the opening length (already printed in Table 5.2);
- $A_r = (a_1, a_2, \dots)$ — the start times of run $r$'s actions; $T_r$ — its active time;
- $H_r$ — the hosts run $r$ compromises; $N = 50$ the network's hosts.
Checked free in the tex: $\theta$, $\kappa$, $\lambda$, $\eta$, $\omega$, $h$, $k$.

## The ten entries

### Attacker behaviour — read in §5.2, Figure 5.1

**1. Relative tactic occurrence — cited** (ruled 2026-09-24, third pass).
- *Definition:* the share of an attacker's steps that fall in each tactic, pooled over its runs; a step is a tactic entered (the firing of its timed transition $\tau_p$), or, for the baseline attacker, a verb entered with consecutive repeats collapsed.
- *Source:* Rodriguez et al. 2024 (`rodriguez2024`, already in the literature review): Table 3 reports, per ATT&CK tactic, "Occur. (rel.)" — the share of the attackers' events in each tactic, from process mining of attack logs. The same quantity, so cited, not adapted. (Supersedes the marsan1984 anchor proposed the same morning.)
- *Why steps, not time:* the model's time at a tactic is its declared dwell, which replaces the verb's native cost; time shares would compare two clocks. Steps are counts on both.
- *Numbers now:* dwell-only tactics hold 36/37/47/26 % of $c_1$–$c_4$'s steps; the baseline's six verbs: `ENUM_HOST` 25, `SCAN_PORT` 25, `EXPLOIT_VULN` 23, `BRUTE_FORCE` 16, `SCAN_NEIGHBOR` 9, `SCAN_HOST` 2.

**2. Attack path variation (APV) — adapted** (ruled 2026-09-24).
- *Definition:* for an opening of $k$ tactics, the share of the attacker's runs whose first $k$ tactics differ from its most common first $k$ (for the baseline attacker, activities entered, repeats collapsed). 0: every run opens alike.
- *Source:* Hong et al. 2018 (`hong2018`), APV, Eq. 2, p. 39: "lower APV value means the set of attack paths tends to be more static".
- *Differs:* Hong measures how the attack paths *available* change between network states; this measures how the paths an attacker *takes* vary between its runs.
- *Why:* strategic plurality is claimed; the baseline attacker is one script.

**3. Attack rate — cited name, adapted unit.**
- *Definition:* $1000\,|A_r| / T_r$, averaged over runs: the attacker's actions per 1 000 s of its active time.
- *Source:* Zhan et al. 2013 ("the number of attacks that arrive at unit time"); surveyed by Pendleton et al. 2016 as a measure of an attack's aggressiveness.
- *Differs:* one attacker's own actions, not attacks arriving at a sensor.
- *The action rule, stated once for both stealth metrics:* an action is a verb that **runs** on the network (end-of-run markers, which carry no verb, are not actions either). A tactic that invokes no verb adds time and no action; a verb whose precondition is unmet is checked before it runs and never touches the network (`movement/attacker.py:896`), so it is not an action; the baseline attacker's per-vulnerability exploit rows are one action. **Say that the rule matters:** counting the unmet verbs would put $c_4$ level with the baseline attacker (20.7 against 28.4 per 1 000 s, or 28.7 if counted; `numbers.json`, `attack_rate_counting_blocked`).
- *Why active time:* in the targeted attack scenario a run ends when the target falls; the baseline attacker takes it early (its active time averages 0.70 of the limit), so a rate over the whole limit would hide the difference.
- *Why the metric:* it is the footprint a detector sees, measured with no assumption (entry 4).

**4. Attack confidentiality — adapted.** *The by-proxy stealth metric — the paragraph E10(i) depends on.* **Read over the run (Figure 5.1(c), third pass):** in each 1 500 s bin, the share of actions below the alarm, with the alarm set by one rule — it flags half of the baseline attacker's actions (the median of $D$ over them, $\theta_b$ = 2.95) — a detector tuned on the attacker the defences were built against. So no alarm level is chosen, and the baseline sits near 50 % by construction; the result is the profiles' 70–93 %, flat across the run. §4.5 states the rule and that the baseline's level is set by it. The across-levels curve (the earlier panel) stays in `numbers.json` as a robustness reading.
- *Definition:* the share of the attacker's actions taken while $D < \theta$, where $D(t) = \sum_{a_i \le t} e^{-(t - a_i)/\kappa}$ counts the attacker's recent actions, each fading over about a minute ($\kappa$ = 60 s: an action counts fully when it happens, about a third a minute later, a seventh two minutes later). An action is exposed when $D$, counting it, reaches $\theta$; Figure 5.1(c) shows every $\theta$, so none is chosen.
- *Source:* Zaffarano et al. 2015, attack confidentiality, "how much attacker activity may be visible by detection mechanisms"; relayed in Cho et al. 2020 as "the degree of attack behaviors detected by a defender". Already in Table 3.1.
- *Differs:* Zaffarano's exposure was information visible in network traffic; here it is a declared detector that counts recent actions.
- *Why, and why by proxy:* an APT attacker trades speed for evasion (Alshamrani et al. 2019); slowing the rate of an attack avoids triggering a defence (Ward et al. 2018, §5.18); fast scanning is easy to detect (Jafarian et al. 2015). The three outcome metrics read only the speed side. MTDSim has no detector, so detection cannot be measured; what can be measured is what the attacker gives a detector to see, and this says what a stated detector would make of it.
- *Must also say, once:* a detector that counts time spent on the network would read the slower attacker the other way (Hong et al. 2018, rationale for ACD: "the longer the attack takes, the more likely it will be detected"); the claim is bounded to a detector that counts actions. $\kappa$ is swept in Appendix `app:detector-memory`.

### Attack outcome — read in §5.2 (Table 5.3) and §5.3

**5. Attack success probability (ASP) — cited.** The share of runs in which the attacker compromises a target host of the targeted attack scenario. Lower is better for the defender. Cho et al. 2020 (the dominant effectiveness metric, "the probability that attacks are successfully performed"); Zaffarano et al. 2015 (*attack success*).

**6. Network compromise ratio (NCR) — cited.** $|H_r| / N$ at the end of the run, averaged over runs. Zhang 2023; Ho et al. 2024 (Eq. 10). *One sentence §4.5 owes* (Marc 2026-09-24): the lineage reads NCR with the general attack scenario, where taking the network is the goal; under the targeted attack scenario it reads how much of the network the attacker holds when its run ends — because the target fell or time ran out — and ASP beside it says which. Under a defence the APT attacker model rarely takes the target, so its runs reach the time limit and NCR compares like with like; that is why NCR, not ASP, carries §5.3.

**7. Mean time to compromise (MTTC) — cited, checkpoint stated.** The mean, over the runs that compromise a host, of the time from the start of the run to its first compromise; the share that compromise none is given beside it. McQueen et al. 2006; Zhang 2023. *One sentence:* Zhang reads it when 80 % of the hosts have fallen; the APT attacker model never reaches that (14–20 % by the limit), so here it is the first host.

### MTD effectiveness — read in §5.3

**8. NCR reduction — cited form.** $1 - \overline{\mathrm{NCR}}_{\text{defence}} / \overline{\mathrm{NCR}}_{\text{no defence}}$, a ratio of means with a bootstrap interval: 0 for no effect, 1 for no host compromised, negative if the defence helps the attacker. The form is Alavizadeh et al. 2022's mitigation factor, $1 - \mathrm{ALE}^m / \mathrm{ALE}$, "the ability of the defensive MTD techniques to impair the attack" (Eq. 13). *Why NCR and not ASP:* under a defence the APT attacker model's ASP is zero on most conditions and cannot order them.

**9. Attack actions blocked — adapted.** The share of the attacker's actions that fail because something they need is no longer there. Brown et al. 2023, §IV-A "Attack Actions Blocked" (a count of the actions an MTD technique blocked; §III-D: connection to the host or service lost, or the user's access changed). *Differs:* a share, so attackers acting at different rates compare; and it counts such failures with no defence running too (0.24), so §5.3.1 reads its change around a disruption.

**10. Time lost per MTD deployment — introduced (was recovery time; renamed 2026-09-24 with the Figure 5.3 rebuild, results context §8g-5; the full name RULED by Marc the same day: "the name should explicitly describe what it's doing"; notes also sit under §4.5's holder in the tex).** The progress one MTD deployment costs the attacker, as seconds at its own pace: the hosts it would have compromised in the 1 250 s after the deployment completes at its rate in the 750 s before, less those it did, over that rate — less the same quantity read at the same moments on the same seed's no-defence run (the placebo; the attacker's pace drifts within a run). Zero: the deployment cost nothing; it can be negative (a catch-up above its level cancels a dip). It is the dip at the deployment, not the net over the run (NCR reduction is the net); only deployments with a full 750 s before them count; at a 2 000 s interval the window stops at 1 250 s because the next deployment's before-window begins there. Must also define **NCR growth rate** (new Table 4.3 row): hosts compromised per unit of the attacker's live time, read around a deployment as a percentage of its rate before; the curve time lost is the area of. *Why:* adaptivity — responding to a defence — is the one APT property readable only when a defence acts; the field's recovery metric (MTTR) is the defender's; that the attacker must recover at all is Jafarian et al. 2015's point. Three per-event estimators (the wait to the next compromise, against a clock-matched or a progress-matched reference) were tried and rejected on censoring and reference grounds; record in §8g-5. **The equations (Marc 2026-09-24: "can this be expressed in calculus? ... we're measuring the rate of change"): yes, and this is their display form.** With $H(t)$ the hosts compromised by time $t$ ($\mathrm{NCR}(t) = H(t)/50$) and a deployment completing at $t_d$: the NCR growth rate is $r(t) = \mathrm{d}\,\mathrm{NCR}/\mathrm{d}t$, estimated in 125 s bins of live time; relative to the rate before, $\tilde r(t) = r(t_d + t) / \bar r_{-}$ with $\bar r_{-}$ the mean rate over $[t_d - 750, t_d)$; time lost $= \int_0^{1250} (1 - \tilde r(t))\,\mathrm{d}t$, less the same integral on the same seed's no-defence run at the same $t_d$ (pooled over deployments before the ratio is taken, so it is a ratio of sums, not a mean of ratios). The 1 250 s upper limit and the 750 s window are declared constants; say why (the next deployment's window at a 2 000 s interval).

## The "why did you do that" items for §5.1 (Marc, 2026-09-24)

Not §4.5, but the same defensibility pass, and the setup is where a reader asks:
- **The targeted attack scenario.** Brown's general attack scenario is a takeover (compromise as much of the network as possible); his target attack scenario is the one he calls "APT-style" — so the thesis switches it on for both attackers, and it exists in the lineage. One clause at the Attacker unit (currently "Both pursue the targeted attack scenario (Table 2.3)").
- **The metrics sentence.** §5.1's Metrics unit still says "grouped by effectiveness and efficiency, as Table 3.x groups the field's": it becomes the three classes, each named for what it measures, defined in §4.5.

## Open (add as they come)

**Moved out of the §5.2 captions and axes into §4.5 (Marc, 2026-09-24: "define them once ... the figures are self-explanatory"; the floats now name each metric and say how to read it).** §4.5 must therefore carry: what a *step* is (a tactic entered; a verb entered by the baseline attacker, repeats collapsed); what an *opening* of length $k$ is; APV's direction (higher: runs start more differently); what an *action* is (a verb that runs: not dwell-only, not blocked, not end-of-run markers; one exploit activity, not each vulnerability); the detector (recent actions, each fading over about a minute) and the alarm's tuning rule, with the consequence that the baseline attacker's share over the whole run is 50 % and its later bins sit below it because its actions fall early; *active time* (to the last action; a run ends on taking a target) as the attack rate's denominator; MTTC to the first host; and — in §4.3's words, not §4.5's — that $c_{\mathrm{agg}}$ is its own profile (the attack graph before partition), not an average.

**Framing ruled (Marc, 2026-09-24):** chapter 5/6 say the model takes fewer actions above a rate alarm tuned on the baseline attacker, because much of its campaign is in tactics the simulator gives no network action — not "much harder to detect". The four-variant action-rule sensitivity (results context §8i-5) goes to Appendix C.4 as a later item.


0. *Action* has two senses in Table 4.3 and §4.5 must name both: a verb **invoked** (attack actions blocked counts the invoked verbs whose precondition fails) and a verb that **runs** (attack rate, attack confidentiality). Also define *opening*, *alarm level* and *detector* — Figure 5.1's caption points here.

1. The symbols (above), especially $\kappa$ for the detector's memory in place of $\tau$.
2. Table 3.1: add the anchors it lacks — attack rate (Zhan), Outkin's time share, the mitigation factor (Alavizadeh) — so every §4.5 source is on the literature review's map. Attack confidentiality, APV, ASP, NCR, MTTC and attack actions blocked are there already.
3. The sweep for `app:detector-memory` — **the alarm quantile and $\kappa$ together** (round 3: at the 60th percentile $c_4$ drops below the baseline in the first bin; $\theta_b$ depends on $\kappa$); §4.5 must also say **why the median** (a detector tuned to flag half of the known attacker's activity). Was: the $\kappa$ sweep (no-defence corpus, both attackers; the ordering across $\theta$ at each $\kappa$). The 2026-08 sweep was for the older tier-weighted detector and does not carry over.
4. A hand trace for each adapted and introduced metric (V1) — a four-host run, recorded.
5. The ablation sentence for §5.2 (the no-action tactics removed from the record) re-run on this detector: at the minute scale it erased the margin; say it only where it holds.
6. The comment block under §4.5's holders (the 2026-09-23 content points) — replace with a pointer here when the definitions are written.

## Validation gate

Each of the ten has its equation, direction and source in §4.5; every adapted metric states its one difference; every introduced metric states why; the symbols collide with nothing in `tab:gspn-notation`; Table 5.2's Source column and §4.5 agree; the two §5.1 clauses are in; build clean.

## Reading list

- `docs/workflows/literature_conventions.md` §d — the convention.
- `docs/thesis/dissertation.tex` — §4.5's holders; `tab:gspn-notation` (l.~4427); Table 3.1 (l.~2120).
- `docs/sources/extractions/mtd_metric_catalogue.md` — each source, with its locator.
- `data/results/ch5_s531_unopposed/analyse.py` — the implementation each equation must match (the metrics-design block).

## Carried from the retired metrics design (2026-09-24)

**The split, and why it is ours.** Three classes, one per question the results ask of the attacker: *attacker behaviour* (what it does; §5.2), *attack outcome* (what it achieves; §5.2's reference and what §5.3's defences change), *MTD effectiveness* (what a defence does to it; §5.3). Not the phases (the outcome metrics are read in both); not Cho's effectiveness/efficiency (the thesis does not model defence cost). "MTD effectiveness" keeps Cho's word because that class *is* the field's effectiveness question. Labels ruled 2026-09-24.

**Wording ceiling for the stealth pair.** Observations of the no-defence runs: "acts at a lower rate", "takes more of its actions below the alarm"; never "less detectable" in chapter 5; the stealth property stays NOT ADDRESSED (a declared detector, not a detection model in the simulator). Framing ruled 2026-09-24: fewer actions above a rate alarm tuned on the baseline attacker, because much of its campaign is in tactics the simulator gives no network action.

**The supervisor's questions, and where the page answers them.**

| Question | Answer |
|---|---|
| Where is this metric from? | Table 4.3's Source column; §4.5 for every adapted or introduced one |
| What is NCR reduction — is that yours? | NCR is Zhang's and Ho's; the with-and-without form is Alavizadeh's mitigation factor; it is the old *suppression*, renamed |
| Your ASR isn't Ho's. | It is ASP (Cho), estimated over runs; Ho's ASR is hosts compromised per attempted action |
| MTTC to what? | the first host (the lineage's 80 % checkpoint is never reached by the APT attacker model) |
| How can you measure stealth with no detector? | the footprint (attack rate) and what a declared detector makes of it (attack confidentiality); the claim is bounded to that |
| Isn't a slow attacker *more* detectable? | to a detector that counts time on the network, yes (Hong 2018's rationale for ACD); ours counts recent actions |
| Your model is worse. | slower and quieter for the same reason — Table 5.2 beside Figure 5.2 |
| What is time lost per MTD deployment, and why not recovery time? | the area of the dip in NCR growth rate after a deployment, as seconds at the attacker's own pace; the per-event wait to the next compromise failed on censoring and on its reference (results context §8g-5) |

**Cut from §5.2, with the reason** (for the examiner who asks): profile divergence (the heat map shows it; its noise floor could not be failed); effective behavioural breadth (Cho and Jalowski use *unpredictability* for the defender's configuration); the detectability level as a metric of its own (it survives as the detector inside attack confidentiality); disengagement and learning (inert in the reported configuration); path entropy, coverage curves, deepest stage (killed or saturated).

**The internal-MTTC finding** now lives in `docs/implementation/metrics_semantics.md` §(a).
