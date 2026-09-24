---
status: open                  # WORK IN PROGRESS by Marc's ruling (2026-09-24): "it's not complete ... keep that somewhere ... we can increment to it"; add entries as metrics are ruled
created: 2026-09-24
parent: 2026-09-22_metrics_provenance_and_instrumentation.md (the metrics design; this file is its §3, grown into the running list for §4.5)
evidence: ../sources/extractions/mtd_metric_catalogue.md
---

# §4.5 *Instrumenting MTDSim* — what the section must define, one entry per metric

## The convention the section follows

`docs/workflows/literature_conventions.md` §d, anchored in Jin's own paper:
1. **Every metric is defined before it is used** — name, the field's acronym where it has one, a numbered display equation, and its direction (which way is better, or which way is *more*) — as hong2018 defines its whole family in its method (pp. 40–41). This applies to the **cited** metrics too, not only the new ones: §4.5 defines all ten, and Table 5.2 is the lookup that points back to it.
2. **A field name is never reused with a different meaning silently** — where we adapt one, the difference is said at the definition.
3. What §4.5 adds for an **adapted** or **introduced** metric: what it captures, what differs from the source, and why the cited metrics do not already capture it (E3: "it should explain something new").

**The reader's level.** The section is written for a computer-science reader, not for the census: it states our definition, its source and, where adapted, the one difference that matters. The finer distinctions the census found (Ho's per-attempt ASR, the five meanings of MTTC in the lineage, Brown's in-flight blocks) stay in the catalogue and are not argued in the thesis — we do not use those meanings, so rule 2 does not require them. (Marc, 2026-09-24: "we need to be on a higher abstraction level ... make it clear for the reader.")

**Where each thing lives.** Table 3.1 (literature review) places a metric in the field; §4.5 defines it; Table 5.2 (§5.1) lists what the chapter reads, with its source. Survey, definition, lookup — the three-place pattern of the field's methods sections. Proposed (ruling owed, §Open 3): Table 3.1 gains the anchors it lacks, so that every §4.5 source is already on the reader's map.

## The entries

Status: **cited** (the field defines it; §4.5 gives the equation and direction); **adapted** (the field's name, one difference stated); **introduced** (no field metric exists; definition and why).

### Attacker behaviour — read in §5.2, Figure 5.1

**1. Time share per tactic — adapted** (was *share of steps per tactic*; recommended change, ruling owed).
- *Definition:* the share of an attacker's time spent in each tactic, pooled over its runs (for the baseline attacker, in each of its six activities, placed on the tactic that maps to it, §4.4.3).
- *Source:* Outkin et al. 2022 (bib `outkin2022`) use "the steady state distribution of the Markov chain to represent the fraction of the time an attacker spends at a particular step" — the same quantity, which they compute from a Markov chain and we measure from runs.
- *Why it is needed:* objective conditioning is claimed, and it shows only in where the attacker spends its campaign; no metric in the field measures the make-up of an attacker's own behaviour.
- *Why time rather than steps:* it avoids defining a "step", it is Outkin's quantity, and it states the stealth mechanism directly — on today's corpus the tactics that take no action hold 49–57 % of the profiles' time ($c_4$ 34 %) against 36–47 % of their steps; the baseline holds none.

**2. Attack path variation across runs — adapted** (was *runs leaving the commonest opening*; recommended name, ruling owed).
- *Definition:* for an opening of *k* tactics, the share of an attacker's runs whose first *k* tactics differ from its most common first *k*. Zero means every run opens the same way.
- *Source:* Hong et al. 2018's attack path variation (APV, Eq. 2, p. 39) — "lower APV value means the set of attack paths tends to be more static".
- *Differs:* Hong measures how the attack paths *available* change between network states; this measures how the paths an attacker *takes* vary between its runs. Stated at the definition (rule 2).
- *Why it is needed:* strategic plurality is claimed — the APT attacker can go more than one way — and the baseline attacker is one script.
- *Alternative if the adaptation is judged too far:* keep the plain name and cite APV as the nearest idea.

**3. Attack rate — adapted.**
- *Definition:* the attacker's actions per 1 000 s of its active time. An action is one verb the attacker invokes; a tactic that invokes none adds time and no action. Active time runs from the start to its last action.
- *Source:* Zhan et al. 2013 ("the number of attacks that arrive at unit time"), surveyed by Pendleton et al. 2016 as a measure of the aggressiveness of attacks. No acronym in either; none is invented.
- *Differs:* one attacker's own actions, not attacks arriving at a sensor.
- *Why active time:* in the targeted attack scenario a run ends when the target falls, and the baseline attacker takes it early (0.70 of the limit on average), so a rate over the whole limit would hide the difference.
- *Why it is needed:* it is the footprint a detector would see, measured with no assumption; it reads the side of the APT trade the outcome metrics cannot (entry 4).

**4. Attack confidentiality — adapted.** *The by-proxy stealth metric; the most important paragraph in §4.5 (E10(i)).*
- *Definition:* the share of the attacker's actions taken while a detector is below its alarm level. The detector: $D(t) = \sum_i e^{-(t - t_i)/\tau}$ over the attacker's past actions, each counting one, with $\tau$ = 60 s — **in plain words, an action counts fully when it happens and fades over about a minute** (a minute later it counts about a third, two minutes later about a seventh). An action is exposed when $D$, counting it, reaches the alarm level; the alarm level is not chosen — Figure 5.1(c) shows every level.
- *Source:* Zaffarano et al. 2015 — "how much attacker activity may be visible by detection mechanisms"; relayed in Cho et al. 2020 as "the degree of attack behaviors detected by a defender". Already in Table 3.1. No acronym (the letters AC are taken by attack cost).
- *Differs:* Zaffarano's exposure was information visible in network traffic; ours is a declared detector that counts recent actions.
- *Why it is needed, and why by proxy:* an APT attacker trades speed for evasion (Alshamrani et al. 2019); slowing the rate of an attack avoids triggering a defence (Ward et al. 2018, §5.18); fast scanning is easy to detect (Jafarian et al. 2015). The three outcome metrics read only the speed side. MTDSim has no detector, so detection cannot be measured; what can be measured is what the attacker gives a detector to see, and this metric says what a stated detector would make of it.
- *Must also say, once:* a detector that counts time spent on the network would read the slower attacker the other way (Hong et al. 2018, rationale for ACD: "the longer the attack takes, the more likely it will be detected"); the claim is bounded to a detector that counts actions.
- *$\tau$:* the one declared constant, swept in the appendix (the 2026-08 sweep exists for the older form; re-run on this one).

### Attack outcome — read in §5.2 (Table 5.3) and §5.3

**5. Attack success probability (ASP) — cited.**
- *Definition:* the share of runs in which the attacker compromises a database host (the targeted attack scenario). Direction: lower is better for the defender.
- *Source:* Cho et al. 2020 (the dominant effectiveness metric, "the probability that attacks are successfully performed"); Zaffarano et al. 2015 (*attack success*).

**6. Network compromise ratio (NCR) — cited, one sentence on the scenario.**
- *Definition:* the hosts compromised by the end of a run, over the network's 50.
- *Source:* Zhang 2023; Ho 2024 (Eq. 10).
- *The sentence §4.5 owes (flag, Marc 2026-09-24: "NCR is dependent on the attack scenario"):* the lineage uses NCR with the general attack scenario, where compromising the network is the goal. This thesis runs the targeted attack scenario — Brown's "APT-style" scenario, the reason it was chosen — so NCR here reads *how much of the network the attacker holds when the run ends*, whether because the target fell or time ran out; ASP, printed beside it, says which. Under a defence the APT attacker model rarely takes the target, so its runs reach the time limit and NCR compares like with like; that is also why NCR, not ASP, carries §5.3 (entry 8).

**7. Mean time to compromise (MTTC) — cited, checkpoint stated.**
- *Definition:* the mean time from the start of a run to its first compromised host, over the runs that compromise one; the share of runs that compromise none is given beside it.
- *Source:* McQueen et al. 2006; Zhang 2023.
- *Differs (rule 2, one sentence):* Zhang reads it when 80 % of the hosts have fallen; the APT attacker model never reaches that, so the checkpoint here is the first host.

### MTD effectiveness — read in §5.3

**8. NCR reduction — cited form.**
- *Definition:* $1 - \mathrm{NCR}_{\text{defence}}/\mathrm{NCR}_{\text{no defence}}$: 0 for no effect, 1 for no host reached, negative if a defence helps the attacker.
- *Source:* NCR (entry 6), in the form of Alavizadeh et al. 2022's mitigation factor, $1 - \mathrm{ALE}^m/\mathrm{ALE}$, "the ability of the defensive MTD techniques to impair the attack" (Eq. 13).
- *Why NCR and not ASP:* with a defence running, the APT attacker model's ASP is zero under most conditions, so it cannot order the defences.

**9. Attack actions blocked — adapted.**
- *Name, verbatim:* Brown et al. 2023, §IV-A heading "Attack Actions Blocked"; Fig. 4 "total actions blocked" — a count of the actions an MTD technique blocked (§III-D: the connection to the host or service is lost, or the user's access has changed).
- *Definition here:* the share of the attacker's actions that fail because something they need is no longer there.
- *Differs:* a share rather than a count, so attackers that act at different rates compare; and it counts such failures with no defence running too, so §5.3.1 reads its change around a disruption.

**10. Recovery time — introduced.**
- *Definition:* the time from a disruption to the attacker's next compromise, as a multiple of its own mean time between compromises with no defence (1 = back at its own pace).
- *Source:* none attacker-side; the field's recovery metric (mean time to recovery) is the defender's.
- *Why it is needed:* adaptivity — responding to a defence — is the one APT property readable only when a defence acts; that the attacker must recover at all is Jafarian et al. 2015's point (a mutation forces the attacker to restart its reconnaissance).

## Open (add as they come)

1. Entries 1 and 2: the recommended changes (time share after Outkin; attack path variation after Hong) — Marc's ruling. If taken, Figure 5.1(a) and (b) and Table 5.2 follow.
2. Stealth pair: whether Table 5.3 carries attack rate only (recommended) or also one attack-confidentiality reading.
3. Table 3.1: add the anchors it lacks — attack rate (Zhan), Outkin's time share, the mitigation factor (Alavizadeh) — so every §4.5 source is on the literature review's map. Attack confidentiality, APV, ASP, NCR, MTTC and attack actions blocked are already there.
4. $\tau$'s sweep, re-run on the current detector (appendix).
5. Hand trace for each adapted and introduced metric (V1) — a four-host run, recorded.

## Done
- Bib entries `zhan2013`, `pendleton2016`, `ward2018`, `jafarian2015` added 2026-09-24 (initials as the sources print them; `pendleton2016`'s wording to confirm in the published version).
