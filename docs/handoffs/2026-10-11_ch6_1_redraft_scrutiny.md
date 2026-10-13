---
status: open — §6.1 redrafted 2026-10-11 on Marc's rulings (§8); awaiting his line-by-line read. §9 carries the lessons to §6.2–§6.5: keep this file until ch6 is redrafted
created: 2026-10-11
topic: "§6.1 (APT attacker model versus baseline attacker): why the overdraft does not read, what the section is for, the structure that purpose sets, and a line-by-line verdict"
reads: dissertation.tex 8486–8662 (§6.1, four paragraphs, ~1 120 words); §5.2 6493–7206; Table 3.2 (tab:attacker-properties); §4.5.1; Table 6.1 and §6.3 8862–9076; §6.5 9240–
---

# §6.1 redraft: scrutiny

**Goal.** Give §6.1 one purpose, a structure set by that purpose, and a sentence-level verdict on the overdraft. Marc then dictates against the slots in §5, as for chapter 5.

## 1. Diagnosis: why the overdraft does not read

Marc read it word by word and came away with three points: "the model is a bit stealthier, they run a bit differently, the attack profiles do something a bit different". The causes, in order of damage:

1. **No section-level message was set before drafting.** The point set was built bottom-up: heading points, then sub-points, then answers to examiner questions, then each point expanded into sentences and the sentences concatenated. Nobody tested the structure against a purpose, so the paragraphs are an inventory, not an argument.
2. **The reader's scaffold was ignored.** §5.2 already walks the comparison property by property ("On objective-specific behaviour … On choice of attack strategy … On attack outcome … On detection avoidance"), and Table 6.1 scores those properties. §6.1's paragraphs are organised by the session's own labels instead (quieter, outcome, openings, attack profiles), so the reader has to infer which property each paragraph serves. Marc's question was "what property number is that?", and the text never answers it.
3. **The per-point cycle (restate, why, compare, bound, so what) was applied mechanically.** It produced "Three bounds hold. First … Second … Third …" twice. Most of those bounds are already in §4.5 or §6.5, so they break the explain-once rule from the other side: a bound is stated once, in §6.5.
4. **"Say more with less" was pushed past the top of the inverted U.** Without defined words to compress into, the draft coined its own: *quieter*, *spaced out*, *costs it outcome*, *the plurality has a price*, *stealth is itself an unmapped tactic*, *the spacing sets both*, *the scan detector flags bursts*. None of them is a chapter 2–5 term, so each reads as a riddle. The fix is the defined term, even when it is longer: *attack rate*, *attack confidentiality*, *detection avoidance*, *choice of attack strategy*, *refused for a missing precondition*.
5. **Bare float references.** A "(Table 5.2)" after a paraphrase does not tell the reader which column or which number the claim rests on, so they cannot check it and stop trusting the sentence. Name the metric in the sentence; give the one number the claim turns on.
6. **Hedges in the wrong place.** Mechanism claims are stated flatly ("Two causes compound") and then followed by a run of bound sentences. The discussion convention is one calibrated hedge inside the inferred claim ("most likely", "likely"), with no hedge on what is measured or true by construction. Hyland's hedging work is the usual reference. A comparison of ChatGPT essays with human essays found the model leans on a narrow hedge ("may") and uses no boosters (Shalevska 2024). The pattern matches: here, flat assertion plus appended caveats.
7. **Numbers without a job.** Examples: "42 to 139 of the APT attacker model's 1 000 against 656"; "three openings over eight steps" written in words beside 179 in digits. APA 7 sets numerals for numbers compared with numbers of 10 or more.

Marc's sorting test is the right one for every sentence: **does the discussion need it here, does it live elsewhere already, or does it live nowhere?**

## 2. The heading: keep the mirror

Keep the heading as it is: it mirrors §5.2 (ruled 2026-09-28). The mirror earns its place only if the inside mirrors too. A reader who has just read §5.2's four "On …" paragraphs should meet the same four properties, in the same words, with the *why* added. The current draft keeps the heading and breaks the inside mirror. That is the defect, not the heading.

A heading that states the job ("Why the APT attacker model behaves differently with no MTD") would fail the heading rule: headings say what a section is on, nothing more.

## 3. Purpose, and the structure it sets

**Purpose of §6.1 (one sentence).** §5.2 showed how the two attackers differ with no MTD, one property at a time. §6.1 explains each difference, and ties it to the property it bears on and to that property's mark in Table 6.1.

**The section's message (its first sentence, in substance).** Two things the APT attacker model adds on top of MTDSim's attack actions explain every difference in §5.2:
- **its tactics take time**, including the unmapped tactics, which dispatch no attack action;
- **the order of its tactics is drawn** by the Petri net from the attack flows, where the baseline attacker's procedure fixes its order.

Name the two causes once and repeat them verbatim (term: Q3).

**Inbound contracts §6.1 must meet.** These are the places where §6.3, §6.5 and the ch6 preamble say "(Section 6.1)":
- §6.3: "in MTDSim an objective shows only in how an attack profile spends its steps (§6.1)". **The current draft never says this.** Paragraph 4 is about ASP ranges instead.
- §6.3: "the pace is assumed to hide the attacker and is measured by proxy (§6.1)".
- §6.3: "the choice stays within what the reports document (§6.1)".
- §6.3: "the reversal rests on the tactic durations and order (§6.1)".
- §6.3: "the baseline attacker, which runs the same attack actions in a fixed order (§6.1)".
- §6.5: "the attack flows record campaigns that were detected and reported (§6.1)". Re-point this one if §6.1 stops carrying it (§4, P4-row 10).
- Preamble: §6.1 "explains why, with no MTD, the APT attacker model is quieter … and succeeds less often". The word *quieter* is in the preamble too, so re-word it with the section.

**Structure.** An opening claim sentence, then one paragraph per §5.2 lead. Each opens on its property's name, then gives the mechanism, then the mark. Outcome goes last because it is the cost of both causes.

| ¶ | Opens on | Job | Hands to |
|---|---|---|---|
| 0 (one or two sentences, may merge into ¶1) | — | the two causes | — |
| 1 | objective-specific behaviour | the attack profiles divide their steps differently; the objectives' tactics are unmapped, so the objective shows only in how steps are spent (why both attackers are in part) | §6.3 |
| 2 | choice of attack strategy | the order is drawn, not fixed: hundreds of openings against one to three; the baseline's single branch is its fixed rule at work (ch3's in-part mark) | §6.2 ("tested against one opening") |
| 3 | detection avoidance | tactic time lowers attack rate; attack confidentiality orders the five attackers the same way; low and slow (the property's own words, §3.3.1) by declared tactic durations, not a choice against a detector, so in part | §6.3, §6.5 |
| 4 | attack outcome | the same two causes cost outcome by the time limit: fewer attack actions, slower spread (45 s against 5 s scan neighbours), attack actions refused for a missing precondition (24 %); the rival explanation is a longer run (one hedged clause); the so-what is a property in MTDSim, not an estimate of APT success; the baseline is the reference, not a rival | §6.2 |

This order is §5.2's with attack outcome moved from third to last. **Q1:** move §5.2's outcome paragraph last too, a one-paragraph move with the prose unchanged, so the mirror is exact?

Budget: about 600 words (ch6 target ~3 300 over five sections; ch6 now measures ~6 700). **A guide, not a target to compress to (Marc 2026-10-11):** the length comes from strong arguments prevailing and weak or irrelevant points being discarded, over several redrafts.

## 4. Line-by-line verdicts on the overdraft

K keep (as is or re-worded into defined terms) · R rewrite · M move (where to) · C cut (where it already lives).

### Paragraph 1 (now: "quieter"; becomes ¶3, detection avoidance)

| # | Sentence (abridged) | V | Why |
|---|---|---|---|
| 1 | "…is quieter …: fewer attack actions per minute, and the scan detector flags fewer of them (Table 5.2)" | R | *Quieter* is undefined. Open on *detection avoidance*, with *attack rate* and *attack confidentiality* by name. |
| 2 | "An unmapped tactic takes time and dispatches no attack action, so … arrive spaced out" | R | The mechanism is right; *spaced out* is wrong. Say that it lowers the attack rate. |
| 3 | "The share of steps in unmapped tactics orders the attack profiles" | K/R | Verified: c3 47.0 %, c2 37.1, c1 36.5, c4 26.0 against attack rate ascending in the same order. Lead with the attack rate, not the share. **Q4:** Figure 5.1(a) does not print the unmapped total, so the reader cannot check 47 %. |
| 4 | c3/c4 sentence with "the reverse" and "c1 and c2 lie between" | R | Too many clauses. One sentence: the most steps in unmapped tactics, the lowest attack rate; the fewest, the highest. |
| 5 | "c3 sits at the far end of this mechanism" | C | Repeats sentence 4. |
| 6 | "Stealth is itself an unmapped tactic, because nothing in MTDSim watches the attacker, so … quiet only because …, and its attack actions refused … never reach the network" | R | Three ideas in one sentence. Keep two: (a) the model does not choose attack actions against a detector, because MTDSim has none; (b) refused attack actions are not counted (§4.5.1), a second, smaller contributor to the lower attack rate. *Stealth* as the bare ATT&CK tactic name reads as the plain word; drop it. |
| 7 | "For the same reason, detection is read by proxy, through the scan detector" | C | §4.5.1 says it ("measure it by proxy"), and §6.5 says it again. |
| 8 | "The scan detector flags bursts, which attack rate, a mean, does not show; … the spacing sets both" | R | Keep only the result: attack confidentiality orders the five attackers as attack rate does (verified), so one cause explains both. The burst argument is §4.5.1's. |
| 9 | six of nine detector settings; the other three under 2 % | C | Appendix C.4, and §6.5 points at it. |
| 10 | low and slow (§3.1.1), "the same trade … through declared tactic durations … in part" | R | This is the paragraph's verdict and should land plainly. §3.3.1 defines detection avoidance as moving low and slow. The model moves low and slow by its declared tactic durations, not by choosing against a detector, so Table 6.1 marks it in part. Note: Table 3.2's definition reads "chooses attack actions a detector does not flag"; the *chooses* is what it lacks. |

### Paragraph 2 (now: "costs it outcome"; becomes ¶4, attack outcome)

| # | Sentence | V | Why |
|---|---|---|---|
| 1 | "The time that makes the APT attacker model quiet also costs it outcome" | R | A riddle. Open on attack outcome: lower ASP and NCR by the time limit, for the same two causes. |
| 2–3 | "compromises less … reach it only just later"; "ASP and NCR well below; MTTC only just longer, c3 overlaps" | C | A replay of §5.2. The c3 overlap is true (9 700 ± 900 s against 9 100 ± 200 s) but nothing turns on it. Marc's "C3 diverges most" is under MTD, at 500–1 000 s, not here. |
| 4 | each attack profile succeeds almost only where the baseline attacker does (App F.1) | K? | It is evidence that the gap is pace and order, not a different capability. One plain sentence, or cut (**Q5**). |
| 5–8 | the two causes: tactics take time (45 s against 5 s for scan neighbours); order puts an exploit before its port scan, and it is refused | K/R | This is the paragraph's core. Use the defined terms: *refused for a missing precondition* (§4.5.1). Bring "about a quarter" (24 %, Table B.7, verified) here from paragraph 3. |
| 9 | "Three bounds hold. First, MTTC is over the runs …" | C | §4.5.2 defines MTTC "over the runs in which it does" (eq. mttc). Marc asked whether this belongs in §4.5: it is there already. |
| 10 | "Second, whether the gap narrows over a longer campaign was not run" | R | Keep, as the rival explanation: one hedged clause ("the gap may narrow over a longer run; this was not tested"). It is not in §6.5. |
| 11 | "Third, ASP scores reaching a target …; objectives unmapped, so not scored" | C | ¶1 (objective-specific behaviour) carries the unmapped objectives, and §6.3 the mark. |
| 12 | CTI records detected, reported, mostly successful campaigns; "nothing in the world can check that measure" | M → §6.5 external | §6.5 already says "detected and reported" and points back to §6.1 for it. Move the "mostly successful" half there and re-point §6.5's reference to §4.4.3 (failure matrix). |
| 13 | "A lower ASP is therefore a property of the APT attacker model in MTDSim, not an estimate of how often APTs succeed" | K | This is the so-what Marc wanted ("less successful, but not necessarily a bad thing"). |
| 14 | "An APT is defined by persistence toward an objective …; not competing with the baseline attacker, which is the reference" | K/R | The closing sentence. Plain: an APT is defined by persistence, not speed, and the baseline attacker is the reference, not a rival. |

### Paragraph 3 (now: openings; becomes ¶2, choice of attack strategy)

| # | Sentence | V | Why |
|---|---|---|---|
| 1 | "opens almost every run the same way … hundreds of ways (Fig 5.1(b))" | R | Open on choice of attack strategy, then the cause: the order is drawn, not fixed. |
| 2 | "share one opening over their first four steps … then branch once … three openings over eight steps" | C | A replay of §5.2. Marc's doubt was right to raise: the curve is 1, 1, 1, 1, 2, 2, 2, 3. The third opening, at step 8, is two runs (§5.2: "all but two … branch once"). So "branch once" beside "three openings" reads as a contradiction. Replace with "one to three openings". |
| 3 | decision places weighted by how often the attack flows took each edge; 5–19 attack flows give 179–947 openings | K | The mechanism. Numerals throughout (APA 7). |
| 4–5 | ch3 credited the baseline with choice in part, a fixed rule sets the order; "its single branch is that rule at work" | K/R | The comparison move. One sentence. |
| 6–10 | "The plurality has a price …" to the ceiling | M → ¶4 | This is the second cause of lower success, not choice. *Plurality* is a coined word; drop it. Keep the ceiling sentence ("only as good as the attack actions it adopts"), cited to §4.4.1, in ¶4. |
| 11 | "With every tactic mapped …, most are refused" | C | §6.5 construct validity carries it. |
| 12 | Bound 1: the units differ (a tactic against an attack action) | Q2 | A real examiner question, but stated without its answer it plants doubt and leaves it. Either resolve it with the attack-action count (190–844 against 3; registry A3, not in ch5), which needs a ch5 footnote or an App F line, or cut it. |
| 13 | Bound 2: capped by 1 000 runs, c1 nearly reaches it | C | Figure 5.1(b)'s caption decodes 1 000. |
| 14 | Bound 3: chooses as documented attackers did; would need cost–benefit reasoning | C | §6.5 has "whether it chooses well is not measured", and §6.3 has cost–benefit. |
| 15 | "An MTD evaluated against the baseline attacker is tested against one opening; §6.2 reads …" | K | The so-what and the hand-on. |

### Paragraph 4 (now: attack profiles differ; becomes ¶1, objective-specific behaviour)

| # | Sentence | V | Why |
|---|---|---|---|
| 1 | "differ from one another, but less than from the baseline attacker" | R | True, but this is not the property. Open on objective-specific behaviour: the attack profiles divide their steps among the tactics differently (relative tactic occurrence, Fig 5.1(a)). |
| 2 | the ranges of ASP, NCR, attack confidentiality and distinct openings | C | A replay. |
| 3 | "because each attack profile divides its steps over the tactics its own attack flows reach" | K | The mechanism. |
| — | **missing** | add | Collection, exfiltration and impact are unmapped, so in MTDSim an objective shows only in how an attack profile divides its steps, not in what it does to a host. Hence in part, the same mark as the baseline attacker. §6.3 cites §6.1 for this. |
| 4–8 | ASP does not follow attack rate; c4 order hypothesis; c3 breadth hypothesis | C | Two "likely"s on a secondary question, and §6.3 / App F.5 own the objective-versus-size question. If anything is kept, one clause pointing to §6.3. |
| 9 | "Which … the objective causes, and which the size … (§6.3)" | K? | One clause, only if the paragraph needs a hand-on. |

## 5. Slots for dictation (job, facts, ceiling; no prose)

**¶0, opener (1–2 sentences).**
- *Job:* state the two causes that explain §5.2.
- *Facts:* unmapped tactics dispatch no attack action but take their tactic duration (§4.4.1–4.4.2); the order is drawn at the Petri net's decision places (§4.3), where the baseline attacker's procedure fixes it (Fig 2.3).
- *Ceiling:* "explain" is licensed by construction for detection avoidance and choice, and by the ablations and the total mapping for outcome.

**¶1, objective-specific behaviour (3–4 sentences).**
- S1 *job:* the profiles divide their steps differently. *Facts:* Fig 5.1(a).
- S2 *job:* why. *Facts:* each profile's attack flows reach different tactics.
- S3 *job:* the limit. *Facts:* the objectives' tactics are unmapped, so the objective shows only in how steps are divided.
- S4 *job:* the mark. *Facts:* in part, as for the baseline attacker (Table 6.1).

**¶2, choice of attack strategy (4 sentences).**
- S1 *job:* the claim and the cause. *Facts:* 179–947 openings against 1–3 (Fig 5.1(b)).
- S2 *job:* the mechanism. *Facts:* decision places weighted by how often 5–19 attack flows took each edge.
- S3 *job:* compare with ch3. *Facts:* the baseline attacker's one branch is its fixed rule (§3.3.2 in-part mark).
- S4 *job:* so what, hand-on. *Facts:* an MTD tested against the baseline attacker meets one opening; §6.2.

**¶3, detection avoidance (4–5 sentences).**
- S1 *job:* the claim. *Facts:* lower attack rate (Table 5.2).
- S2 *job:* the mechanism. *Facts:* unmapped tactics take time and dispatch nothing; refused attack actions are not counted.
- S3 *job:* evidence. *Facts:* more steps in unmapped tactics, lower attack rate, across the attack profiles (c3 47 %, c4 26 %; Q4).
- S4 *job:* the second metric. *Facts:* attack confidentiality orders all five the same way.
- S5 *job:* the mark. *Facts:* low and slow by declared durations, not chosen against a detector; in part.

**¶4, attack outcome (5–6 sentences).**
- S1 *job:* the claim. *Facts:* lower ASP and NCR by the time limit, from the same two causes.
- S2 *job:* time. *Facts:* 45 s against 5 s for scan neighbours, the only attack action that finds new hosts.
- S3 *job:* order. *Facts:* 24 % refused for a missing precondition; the ceiling of §4.4.1.
- S4 *job:* the rival explanation. *Facts:* a longer run may narrow the gap; not tested (one hedge).
- S5 *job:* so what. *Facts:* a property of the model in MTDSim, not an estimate of APT success.
- S6 *job:* close. *Facts:* persistence, not speed, defines an APT; the baseline attacker is the reference.

## 6. Questions for Marc (recommendation first)

- **Q1. Exact mirror.** Move §5.2's attack-outcome paragraph to last, so §5.2 and §6.1 share one order? *Recommend yes.* It is one paragraph move with no prose change, and it puts the outcome after the behaviour that explains it in both chapters.
- **Q2. The unit bound on distinct openings.** Resolve it with the attack-action count (190–844 against 3), or cut it? *Recommend resolve.* It is the question an examiner asks of Figure 5.1(b). It needs one line in ch5 or App F, since ch6 brings no new numbers.
- **Q3. The term for the second cause.** "the order of its tactics", "tactic order", or "its order"? §6.3 already says "order, the substance of choice of attack strategy". *Recommend "the order of its tactics"* at first use, then "order".
- **Q4. The 47 % / 26 %.** Add an "unmapped" total row to Figure 5.1(a), or state the ordering without the numbers? *Recommend the row.* The reader can then check the number, which is Marc's trust point.
- **Q5. App F.1, success on the same networks.** Keep one sentence in ¶4, or leave F.1 to §6.5 / §6.3? *Recommend keep.* It is the cleanest evidence that the gap is pace and order, not a different capability.

## 7. Validation gate

- Each paragraph opens on a §5.2 property name, or "attack outcome".
- No word outside the ch2–5 vocabulary.
- Every float reference sits next to the metric it shows.
- No bound that §4.5 or §6.5 already states.
- §6.3's five back-references are each answered.
- §6.1 is about 600 words.
- The voice.md §(f) gate passes.
- Build clean.

## Sources consulted for §1

- UBC Writing Library, *Discussion sections in research articles* (Hopkins & Dudley-Evans moves): https://writing-library.sites.olt.ubc.ca/files/2024/05/Discussion-Sections-in-Research-Articles.pdf
- Shalevska 2024, *Hedges and boosters in AI and human writing*: https://eprints.uklo.edu.mk/id/eprint/10825/
- The ch6 handoff D_examiner_benchmarks (UWA marking guide, "interpret, never replay").

## 8. Rulings and what was applied (2026-10-11)

Marc on §1–§3: the diagnosis is "spot on"; the purpose, message and structure stand.

- **Q1 yes.** §5.2's attack-outcome paragraph moved to last; prose unchanged, with a comment. §5.2 describes, §6.1 explains: the mirror is the order, not the register.
- **Q2.** Marc: "comparing openings across different units is a bit of a bummer … whichever is fair". His 2026-10-09 ruling declined the attack-action recount (190–844 against 3) as supplementing the evaluation. Applied: the concession is stated once, in §6.5 beside "distinct openings counts any variety": an attack profile's steps are tactics and the baseline attacker's are attack actions (§4.5.1), so the two counts are not in the same unit. §6.1 carries no unit sentence (explain once). *Open option:* the recount is a pure read of the stored runs and could be Appendix F.6, which would let §6.5 say the gap survives it. Not done; Marc's call.
- **Q3** ("whatever is the most clear"). "The order of its tactics" at first use, then "order", as §6.3 already says ("order, the substance of choice of attack strategy"). Not "sequence", because §4.5.1 uses *opening* for a sequence of steps.
- **Q4 yes, "as long as it's very clear in the figure".** Figure 5.1(a) gains an *All unmapped* row: the column sums (36, 37, 47, 26), plain numbers with no heat fill (a sum is off the cells' colour scale), and the baseline attacker's cell blank. Generator `tools/ch5_unopposed_figures.py`; the tables regenerate byte-identical.
- **Q5 keep.** Marc's reading: network topology; both attackers compromise through identical attack actions, so easy networks are easy for both. Written as "likely because both attackers compromise hosts through the same attack actions".

Applied to the tex:
- §6.1 replaced: an opener and four paragraphs (objective-specific behaviour, choice of attack strategy, detection avoidance, attack outcome), about 760 words.
- The ch6 preamble's §6.1 sentence now names the two causes; *quieter* is gone.
- §6.5: "detected and reported" re-pointed from §6.1 to §4.4.3 (which says the reports "describe incidents that succeeded and were worth writing about"); the unit clause added.
- The objective-specific mark now gives chapter 3's own reason for the baseline attacker ("after a foothold … no attack action for exfiltration or impediment"), the same reason that holds for the APT attacker model.
- Build clean, 115 pages, 0 undefined.

## 9. Lessons for §6.2–§6.5 (Marc: "the lessons … translated for the other sections")

Every ch6 section was drafted the same way §6.1 was, bottom-up from point sets, so expect the same defects. Run this before redrafting each one:

1. **Purpose first.** Which ch5 section or float does it read, and what must it hand on? List the inbound "(Section 6.x)" references from the other sections: each is a contract the section must meet. (§6.1 failed §6.3's.)
2. **One message**, in the first sentence, naming the causes once in terms that are then repeated verbatim.
3. **Mirror the reader's scaffold inside the paragraphs.** Each paragraph opens on the term the reader already holds: the ch5 lead, the metric, or the property.
4. **Sort every sentence**: needed here, already elsewhere (§4.5 definitions, §6.5 bounds, appendices), or nowhere.
5. **Bounds live once, in §6.5.** A section keeps only the rival explanation for its own finding, as one hedged clause.
6. **No coined compressions.** If a short phrase is not a ch2–5 term, use the defined term, even when it is longer.
7. **Hedge inside the inferred claim** ("likely"); no hedge on what is measured or true by construction.
8. **Floats sit next to the metric they show.** Every number has a job, and the reader can find it in the float cited; if they cannot, fix the float (as Figure 5.1(a)'s unmapped row did) or drop the number.
9. **Length comes from cutting weak points across redrafts**, never from compressing sentences toward a word target.
10. **Cold examiner read** on the redraft (PDF only), then verify and triage, before handing to Marc.

## 10. Cold examiner round (2026-10-11; PDF only, no repo), verified and triaged

**Fixed in §6.1** (each checked against its source first):
- "the five attackers" became "the four attack profiles and the baseline attacker", §5.2's own words.
- "order gives" and "Order costs it" no longer make order the actor.
- "spread" (undefined) became "how fast it finds new hosts".
- "an attack profile's objective" became "the objectives". c4's attack flows "did neither" (§4.2).
- "5 to 19 attack flows give it 179 to 947 openings" was cut. It implied that more attack flows give more openings, and c4 has 5 flows and 662 openings.
- "the same opening in most runs" became "over the first four steps of every run". Figure 5.1(b) shows counts, not shares, so only that version can be checked.
- Command and control's cause is now hedged "most likely", as §4.4.2 hedges it. The 5 s is cited to §2.2.3, where it is stated.
- The rival is named in the opener: removing the failure matrix or the vulnerability memory moves NCR negligibly (§5.4).
- MTTC is now read: it is over the runs that reach a target, and those runs fall on the same networks for both attackers. Hedged "likely".
- The outcome paragraph is split in two: its causes, and what the lower ASP means.
- The ceiling sentence was cut from §6.1. §6.3's close and §6.5 carry it.

**Consequential edits:**
- Appendix F.1's "so it is not part of the main argument" is cut, since §6.1 now uses F.1 under Q5.
- The ch6 opener's "held back most" became "reduces each attacker's NCR most". Marc dislikes "held back", and NCR reduction is what §6.2 measures.

**For §6.3's redraft. These are viva risks the examiner ranked highest, outside §6.1:**
1. "How is a weighted random draw *choosing* among attack strategies? Would a uniform random walk also earn the full mark? How many openings are there counted in attack actions?" This strengthens the case for the Appendix F.6 recount (§8, Q2).
2. "Why do judgement-set durations earn detection avoidance in part, when the baseline attacker's fixed pace earns none?"
3. "Objective-specific behaviour is near-tautological: the attack profiles were built to differ (§4.5.1)."

**Set aside:**
- Moving the so-what and the longer-run clause to §6.5: Marc ruled them in, and the longer run is the rival explanation for this finding.
- "Table 6.1 marks …" pre-empting §6.3: tying each difference to its mark is §6.1's purpose (§3).

**Flagged only:**
- Table B.4 says *Refused*, where §4.5.1 and §6.1 say *fails because its preconditions are missing*.
- Table 3.3's legend never says "in full", which §6.1 and §6.3 use.

## 11. Round 2: Marc's read of the redraft (2026-10-11), critiqued both ways

Marc's verdict: "definitely on the right track … I could read this a lot better and faster", but the structure still leaves loose ends, and several sentences are rhetorical rather than plain. He asked for his own critique to be critiqued as hard as the draft.

### 11.1 Evidence checked before ruling (pure reads, no runs)

Scripts in the session scratchpad (`rate_decomp.py`, `verb_share.py`), reading `data/results/ch5_s531_unopposed/runs_reported.jsonl`. Not in the thesis: a number here enters chapter 6 only through an Appendix F section (Q10).

**Where the APT attacker model's run time goes, and its attack rate if that time were removed** (attack actions per minute; baseline attacker 1.71):

| Attack profile | Unmapped tactics, % of run time | Blocked attack actions, % of time / % of those dispatched | Attack rate | …unmapped tactics took no time | …blocked counted | …counted actions at the baseline's times |
|---|---|---|---|---|---|---|
| c1 | 49.6 | 4.7 / 14.5 | 1.09 | 2.16 | 1.27 | 1.47 |
| c2 | 51.1 | 8.1 / 27.0 | 0.89 | 1.82 | 1.22 | 1.17 |
| c3 | 57.4 | 9.5 / 30.4 | 0.68 | 1.60 | 0.98 | 0.84 |
| c4 | 33.6 | 13.0 / 28.4 | 1.23 | 1.85 | 1.71 | 1.80 |

Reading: unmapped tactics take a third to over half of the run. Removing that time alone brings every attack profile's attack rate to about the baseline attacker's (1.6 to 2.2 against 1.7). Timing the mapped tactics as the baseline attacker's attack actions moves it less. **The unmapped tactics are the main cause of the lower attack rate.** Marc's instinct is borne out.

**Attack actions after the foothold** (% of counted attack actions after the first exploit or brute force that succeeds):

| | scan host | enum host | scan port | exploit | brute force | scan neighbours |
|---|---|---|---|---|---|---|
| c1 | 8.1 | 15.8 | 14.5 | 11.3 | 19.2 | 31.1 |
| c2 | 2.6 | 15.5 | 24.9 | 20.3 | 6.6 | 30.2 |
| c3 | 0.0 | 9.8 | 35.1 | 22.9 | 2.3 | 29.9 |
| c4 | 2.5 | 18.1 | 14.1 | 11.9 | 16.6 | 36.8 |
| baseline | 1.8 | 33.2 | 22.5 | 20.0 | 13.7 | 8.9 |

Reading: after the foothold, the attack profiles do take different attack actions, the definition's own unit. Brute force ranges from 2 % to 19 %. This is already visible in Figure 5.1(a), because credential access is the only tactic that dispatches brute force: its row reads 10, 3, 1, 10 %. But c4, which has no objective, differs as much as the others, so the difference comes from each attack profile's attack flows, not from the objective as such (the examiner's tautology risk, §10).

**The attack scenario, in code** (`mtdnetwork/operation/attack_operation.py`, the targeted-objective seams):
- The targeted scenario changes three things: the order of the host list (Brown's priority-then-distance sorter), the give-up rule (never on a target host), and termination.
- It never changes which attack actions are taken.
- The same seam serves both attackers. For the APT attacker model, the scenario changes which host comes next and when the run ends, never the order of its tactics.
- Chapter 5 runs only the targeted scenario (§5.1, Held settings), so the dissertation never compares general against targeted.

**Blocked attack actions.** §4.5.1 already says that an attack action failing because its preconditions are missing "never reaches the network" and is not counted. The reason holds for a detection proxy: a detector can flag only what reaches the network. But it has a size. Counted, c4's attack rate would equal the baseline attacker's (1.71).

**The tactic durations** (§4.4.2).
- Six tactics take MTDSim's own times: exploit 4.5 s; reconnaissance and discovery 35 s, the three scans together.
- The other nine are judgement, including all seven unmapped tactics. Two mapped tactics run longer than the attack action they dispatch: command and control (45 s, scan neighbours 5 s) and execution (22.5 s, exploit).
- The 45 s value that Appendix B finds moves NCR most also times persistence and stealth, both unmapped. So Appendix B cannot separate command and control from them, and §6.1's "most likely through command and control" rests on §4.4.2's own hedge.

### 11.2 Marc's points: agreed, taken further, or pushed back

**Agreed:**
1. *Opener: the first and last sentences carry it; the middle is sandwich.* "Every tactic takes its tactic duration" says nothing, and "drawn from the attack flows by the Petri net" is a riddle.
2. *"Draws/drawing" is rhetorical.* §4.3 has the terms. At each *decision place* one *immediate transition* fires, with probability proportional to its *base weight*, the share of the attack profile's attack flows that took that edge. Use them in words, with no symbols. Symbols never appear in ch6 prose, and that should stay.
3. *"Its one branch … is that rule at work"* gives the reader nothing. Cut it.
4. *"One to three" is vague.* Say what Figure 5.1(b) shows: one opening over the first four steps, three over eight.
5. *Lead with the unmapped tactics, not "tactic durations".* The data say so (§11.1).
6. *No secondary definitions.* "Which take time and dispatch no attack action" re-defines a ch4 term. One gap: *unmapped* is not \emph'd at §4.4.1, so give it its \emph there, then never gloss it.
7. *The c3/c4 percentages are decoration.* They make the reader decode profile names to check an ordering. If Q10 is yes, replace them with the one number that carries the claim (about half the run time); otherwise give the ordering without numbers.
8. *"Not what they do to a host" and "not to stay undetected"* are not-X-but-Y. The second also reads as an accident when the pace is designed: §4.4.2 sets execution and defense impairment at 22.5 s because "the attacker paces [them] to stay hidden".
9. *Attack outcome is a metric family, not a property.* Placing it as a fourth "On …" paragraph is a false parallel. The opener must say that the three attacker behaviour metrics show how the attackers differ, and attack outcome shows what the difference costs.
10. *The last paragraph is loose ends, a sign of a sort failure.* It mixes outcome causes (F.1, MTTC), a rival (longer run), a bound (CTI records successes, already in §6.5) and a framing (persistence not speed; reference not rival). Sort: causes and rival into the outcome paragraph; the bound cut (§6.5 has it); the framing kept as one so-what sentence.
11. *"Takes only the tactics its own attack flows reach" is janky.* §4.2 builds each attack profile from the attack flows of one objective; say that.

**Taken further:**
- **Stealth and defense impairment, the ATT&CK tactics of detection avoidance, are themselves unmapped tactics.** In MTDSim, hiding is time spent without attack actions, and that time is what lowers the attack rate. This is the sharpest true sentence the detection-avoidance paragraph can carry. It is honest: hiding is modelled as time by design (§4.4.1, §4.4.2), and nothing chooses against a detector.
- **The same fact explains attack outcome.** The outcome paragraph leads with command and control's 45 s on a hedged sensitivity reading. The stronger cause is that the APT attacker model spends a third to over half its run in tactics that dispatch nothing, and a seventh to almost a third of its dispatched attack actions are blocked. Both are steps with no effect in MTDSim. Each comes from where the model meets MTDSim's attack actions, which §6.3 already names as what the reversal rests on.
- **Two senses of "objective".** The attack scenario's goal (which host) and the attack profile's objective (exfiltration, impact) are different things. The baseline attacker's in-part mark rests on the first, while property 2's definition speaks of the second. An examiner can split these.

**Pushed back:**
- *"A rational actor would lower edge 3's weight after it kept failing", so choice of attack strategy is not in full.* Updating a choice on what was observed is adaptivity (4) and learning (7), both already marked in part. Marking choice down for it scores the same gap twice.
- *"Chooses" implies deliberation.* Chapter 3 fixed the meaning when it scored Masud et al. in part because their model "has every attack path … but chooses none". There, choosing is a selection among several sequences, not a deliberation, and §4.3 calls the immediate transition the attacker's "choice of the next tactic". Redefining it now breaks §6.3's claim that the properties were fixed before any model was scored, and the blind scorer gave the full mark on the definition as written. **Marc is right on two narrower points:**
  - the definition's unit is attack actions, while distinct openings counts tactics (the F.6 recount closes this);
  - the weights are constants, set from the reports, and the choice ignores the attacker's state. It can choose an exploit before a scan, which is half of why attack actions are blocked. That limit belongs in §6.3's reason for the full mark ("a full mark meets the definition, not the ceiling") and in Future work: weights that change with what the attacker observes (the supervisor's dynamic weighting), beside the uniform-weights Petri net already listed.
- *"If everything goes to in part, the two rows look the same."* That is the honest output of the rule, and §6.3 already says the marks do not show upgrades made within an in-part mark. It is not a reason to keep a full mark. The definition is.
- *"The durations are honest extrapolations of the baseline attacker's, so they cannot explain the difference."* Only six of 15 are borrowed. The nine set by judgement include every unmapped tactic, command and control and execution. The conclusion still holds (lead with the unmapped tactics), but for the data's reason, not this one.
- *"A failed attack action should count."* For attack rate as a detection proxy, an action that sends nothing cannot be flagged, so excluding it is right. What the draft lacks is the reason in the sentence: "which never reaches the network, so no detector could flag it".
- *Component-by-component structure* ("we added X, it was negligible"). Organising by component breaks the §5.2 mirror Marc ratified and makes the reader map components onto properties. The component accounting fits in the opener: the two causes, plus one sentence naming what the ablations rule out.
- *Capital letters for ATT&CK tactics.* The thesis is lowercase throughout. The only two capitalised uses are sentence starts. Changing it is dissertation-wide and a figure change. Where a bare noun reads ambiguously, write "the impact tactic" or "the tactics collection, exfiltration and impact".
- *Property numbers in the prose* ("property 2"). That would give each property a second name, against one term per thing. Table 6.1 already heads each column with its number and abbreviation. Point to Table 3.2 once in the opener, and use names only.

### 11.3 What is still wrong at the structural level

1. **The message names a vague cause.** "Tactic durations" covers six borrowed values and nine judged ones. The cause the data support is the **unmapped tactics**: time with no attack action. Paired with the order of tactics, they become two ch4 terms, with no coinage.
2. **The marks duplicate §6.3.** §6.3 ¶2 already gives each mark's reason. Ending each §6.1 paragraph on its mark pulls the scoring debates (choice in full? the baseline attacker's in-part reason?) into the section that should only explain. **This overturns §3's structure and §10's set-aside, on merit.** §6.3 says the runs "could lower one of its marks … never raise one", so the runs' job in §6.1 is to say whether each property shows. Each paragraph ends on what the runs show about the property; §6.3 gives the mark.
3. **The false parallel.** Three properties plus a metric family are written as four equals.
4. **No sort pass on the last paragraph** (11.2, point 10).

### 11.4 Structure v3 (subject to Q6–Q10)

| ¶ | Opens on | Job | Evidence the reader can find |
|---|---|---|---|
| 0 | the two causes | The unmapped tactics take much of the APT attacker model's run and dispatch nothing. The order of its tactics follows the attack flows' base weights, not the attack actions' preconditions. Together they explain each difference in §5.2. What they do not: the ablations (failure matrix, vulnerability memory). The three behaviour metrics show how the attackers differ; attack outcome shows what that costs. | §4.4.1, §4.3, §5.4 |
| 1 | objective-specific behaviour | Each attack profile is built from one objective's attack flows (§4.2), so the profiles divide their steps differently, including mapped tactics, and so take different attack actions after the foothold (credential access, the only tactic that dispatches brute force: 1 % to 10 %). The objectives' own tactics are unmapped, so the runs show the property only through the mapped tactics. | Figure 5.1(a) |
| 2 | choice of attack strategy | At each decision place, one immediate transition fires in proportion to its base weight. Runs therefore follow different sequences: hundreds of distinct openings over eight steps, against the baseline attacker's one over four and three over eight, fixed by its procedure. Every opening uses edges the attack flows took (§6.3's contract). The weights ignore the attack actions' preconditions, which leads to ¶4. Hand to §6.2. | Figure 5.1(b) |
| 3 | detection avoidance | The unmapped tactics, among them stealth and defense impairment, take time and dispatch nothing. The larger their share, the lower the attack rate. Blocked attack actions never reach the network, so they are not counted. Attack confidentiality agrees. The model moves low and slow by design (§4.4.2), but chooses nothing against a detector: MTDSim has none (proxy, §4.5.1). | Table 5.2, Figure 5.1(a) All unmapped row |
| 4 | attack outcome (introduced as the cost) | Lower ASP and NCR by the time limit, likely because it takes fewer attack actions (unmapped time; blocked attack actions; command and control's 45 s, hedged as §4.4.2 does). Not the network: it succeeds on the networks the baseline attacker does (F.1), so MTTC is close. Rival: a longer run, untested. So-what: the baseline attacker is the reference, and §6.2 reads MTD as NCR reduction against each attacker's own NCR with no MTD. | Table 5.2, Table 5.3, App F.1 |

Cut from §6.1: the CTI-records-successes bound (§6.5 has it); "persistence, not speed" (§6.3's property 1). The Table 6.1 marks go to §6.3 (Q7).

Blast radius if Q6 is yes:
- the ch6 preamble's §6.1 sentence;
- §6.3 ¶3 ("rests on the tactic durations and order");
- §6.3 ¶4 ("the tactic durations, which set the pace behind detection avoidance");
- §4.4.1, giving *unmapped* its \emph.

### 11.5 Questions for Marc (recommendation first)

- **Q6. Message.** Name the two causes as *the unmapped tactics* and *the order of its tactics*, replacing *tactic durations*. Recommended: the data put the unmapped tactics first; command and control's 45 s stays as one hedged cause of outcome.
- **Q7. Marks.** Move the marks out of §6.1, so each paragraph ends on what the runs show about its property and §6.3 gives every mark. Recommended (explain-once; §6.3's "runs could lower, never raise").
- **Q8. Choice of attack strategy.** Keep the full mark on the definition as fixed in chapter 3. Do the F.6 recount in attack actions. State the limit (constant weights, blind to the attacker's state) in §6.3. Add dynamic weighting to Future work. Recommended. The alternative is in part, which changes Table 6.1, §6.3 ¶1, ¶2 and ¶4, ch7 Contributions, the abstract and ch1's claim, and leaves detection avoidance in part as the only gain over the baseline attacker.
- **Q9. The baseline attacker's in-part mark on objective-specific behaviour.** Keep it, because chapter 3 scores from the paper, and the scenario does change which host it attacks (verified in code). Name the two senses of "objective" in §6.5 as a threat. The alternative re-scores Table 3.3 and Table 6.1 to a cross; it is a defensible reading, but a ch3 change that touches the chapter's finding.
- **Q10. Appendix F.** Two more pure reads:
  - F.6: openings counted in attack actions (190 to 844 against 3);
  - F.7: where the run time goes (§11.1's first table).
  Recommended: both. F.7 is what lets §6.1 say "about half its run" instead of decoding profile shares. The after-foothold table stays out, since Figure 5.1(a)'s credential-access row already shows it.

## 12. Round 3: Marc's rulings on §11, applied; the Table 3.2 audit (2026-10-11)

### 12.1 Rulings
- **Q6 yes.** The causes are the unmapped tactics and the order of its tactics. Marc: "that chalks down most of the difference". Applied as "most of": the outcome paragraph keeps command and control's 45 s as a third, hedged cause, so "each difference" would overclaim.
  - Marc's caution for §6.2: if these two explain the no-MTD gap, §6.2 must argue with care which of them drives each MTD result. NCR reduction is relative: "coming from a low base and then going to a lower".
  - §6.3 ¶3 still says "the reversal rests on the tactic durations and order (Section 6.1)". The reversal is §6.2's claim, so it is left for the §6.2/§6.3 redrafts.
- **Q7 yes.** The marks are out of §6.1. Each paragraph opens on its Table 3.2 definition and tests the clauses in order; §6.3 scores.
- **Q8 yes.** Choice of attack strategy keeps its full mark. Owed: dynamic weighting in Future work, and the limit (constant weights, blind to the attacker's state) in §6.3.
- **Q10, "just do what you need to do".** But Marc warns against over-reliance on the appendix: "if it's critical … put it into 5.2". Done as Appendix F.2 and F.3, because the main claims stand on the ch5 floats (Figure 5.1(a)'s All unmapped and credential access rows; Figure 5.1(b)) and the appendix checks them.
  - **F.2**, the attacker behaviour metrics counted in attack actions: openings 190–844 against 3; each attack action's share after the foothold.
  - **F.3**, where the run time goes: unmapped tactics 34–57 % of the run; attack rate with no time in them 1.60–2.16 against 1.71.
  - Script `further_analyses.py` f6 and f7. The attack rates reproduce Table 5.2 exactly. The five existing F tables regenerate byte-identical.
- §6.5's unit clause now says the gap holds when recounted (F.2), and the preamble names the two causes.
- **Marc's question, "why only three in 5.2 and 6.1? Where do the other five live?"**, is answered in the §6.1 opener:
  - 2, 3 and 5 have attacker behaviour metrics (§4.5) and are read in §5.2 and §6.1;
  - 4 needs MTD and is read in §5.3.1 and §6.2;
  - §6.3 scores all eight: 1, 6 and 7 from Chapter 4 by construction, 8 absent.

### 12.2 Capitals for ATT&CK tactic names
There is a recorded convention: `docs/workflows/literature_conventions.md` §a4 (2026-08-20, from al-sada2024 and rodriguez2024). Tactic names are proper names, capitalised in tables and figures, and common nouns in running prose when the text describes activity ("the attacker moves laterally").

The thesis drifted from it:
- figures use sentence case ("Credential access", Figure 5.1(a));
- prose that *names* a tactic is lowercase ("Credential access, the only tactic that dispatches brute force").

By §a4 that is a proper name. Capitals would also separate the tactics from plain words and from property names: *persistence* (and campaign persistence), *impact* (and RoA's impact), *execution*, *collection*, *discovery*.

**Recommendation:** Title Case wherever the text names an ATT&CK tactic, in prose, tables and figures, and lowercase only for activity. The change runs across the whole dissertation, through the figure generators and a terminology row. Marc's call.

### 12.3 Table 3.2 audit: source intent, testable clauses, effect on marks (proposal; Marc rules)
Sources were read by a sub-agent from `docs/sources/lit_review/{2_3_alshamrani2019survey,1_1_cho2020toward,3_1_jalowski2026rethinking}.md`. **NIST SP 800-39 is not in the repo.** Rows 1 and 4 cite it only through Alshamrani's restatement (§II-A, :53). Check the PDF before submission.

**Integrity rule for any re-wording.** Table 6.1 claims the properties were fixed before any model was scored. A re-wording made now must:
- come from the source's intent,
- apply to all four rows,
- be re-scored blind (as on 2026-10-08),
- be declared.

A re-wording that raises the APT attacker model's mark is the one an examiner will suspect. None proposed here does.

| # | Now | Source intent (locator) | Problem | Proposed | Testable clauses | Marks (B / Masud / Kim / APT) |
|---|---|---|---|---|---|---|
| 1 | runs one multi-stage campaign toward its objective over an extended period | NIST via Alshamrani :53 "pursues its objectives repeatedly over an extended period"; :51 "do not give up" | "one" narrows "repeatedly"; "extended period" has no reference length | pursues its objective through many stages over an extended period, and does not give up | many stages? toward the objective? carries on through resistance? | unchanged ✓ / P / P / ✓ |
| 2 | after the foothold, takes different attack actions for different objectives, such as exfiltration or impediment | Alshamrani §II-C :103: the first two stages are common; "the other 3 stages are applicable based on the attackers' goal", e.g. exfiltration for data theft | "such as …" is an example, not a clause. The source is goal-directed: the goal decides what follows. "Different" alone is met by any variation. Drops "position for the future" | after the foothold, takes the attack actions its objective needs, so that different objectives, such as stealing data, impeding systems or positioning for the future, give different attack actions | after the foothold? the attack actions the objective needs? different objectives give different attack actions? | B P (same attack actions, different host) / Masud P / Kim P / **APT P, now for a clause it visibly fails**: no attack action steals data or impedes |
| 3 | chooses among several attack strategies (sequences of attack actions) toward the same objective | Cho §V-D :460: "multiple strategies … decide which system vulnerability it needs to target" | The parenthesis and "same objective" are our separators. Defensible, and keep. A random choice meets 3 but not 6 (that is the 3/6 split) | unchanged | several sequences toward one objective? chooses among them, rather than a fixed order? | unchanged P / P / ✗ / ✓ |
| 4 | chooses its next attack action in response to an MTD disruption | NIST via Alshamrani :53 "adapts to defenders efforts to resist it"; Cho §V-A :381 | As worded, a one-step reaction also meets 7. The 2026-09-07 boundary clause ("reacts as they occur") was lost in rounds 42–43 | chooses its next attack action in response to the MTD disruption it has just met | observes the disruption? next attack action depends on it? chosen, not a forced reset? | unchanged P / P / ✗ / P |
| 5 | chooses attack actions a detector does not flag, for example passive reconnaissance | Alshamrani :51 "evasive techniques to elude detection"; :107 passive reconnaissance; Jalowski :197 | Narrows to choosing actions; evasive execution and pace are dropped. "for example …" is an example | **unchanged**. Adding pace ("low and slow") would raise only the APT attacker model's evidence, the suspect direction. Note in §6.5 that the definition leaves pace out | a detector (or proxy)? the attacker's choice depends on what it flags? | unchanged ✗ / ✗ / P / P |
| 6 | chooses each attack action by weighing its cost against its benefit | Cho §V-A :398 "rational actor … sensitive to incentives" | "each" is stricter than Cho's "the attack" | unchanged | cost? benefit? weighed in the choice? at every choice? | unchanged |
| 7 | keeps what it observes of past MTD deployments, and uses it to choose later attack actions | Cho §V-D :458 "detect defense patterns by using learning … what types of MTD … what the patterns are"; Jalowski :197 "learn mutation patterns over time" | Overlaps 4. The source's object is the MTD's patterns | keeps what it observes across MTD deployments, and uses it to choose its attack actions after later ones | keeps observations across deployments? of the MTD? they change later choices? | **at risk** for B and APT. Both "learn" vulnerabilities, not MTD deployments, and the memory makes an exploit faster, not a choice. Strictly, part of the definition is unmet in both clauses, so P could fall to ✗. Marc's call; ch3 and Table 6.1 move together |
| 8 | predicts which mechanism the deployment strategy deploys next, and when | Jalowski :169 "predict future movements"; Cho §V-D :464 "leverage how MTD works" | A prediction that drives nothing leaves no trace | predicts which mechanism the deployment strategy deploys next, and when, and uses the prediction to choose its attack actions | predicts what? when? uses it? | unchanged ✗ / ✗ / P / ✗ |

**Marc's reading of row 2** ("we literally do that … every clause"): under the current wording, he is right. The APT attacker model meets "after the foothold", "different attack actions" (F.2: brute force 2 % to 19 %) and "different objectives". The P was set on 2026-10-08 for a reason the current wording does not state (exfiltration and impact unmapped). So the reason and the definition disagree. Either:
- (a) re-word row 2 to the source's goal-directed intent (recommended). The P then rests on a stated clause, and the same clause explains the baseline attacker's and Kim's P; or
- (b) keep the wording and raise the APT attacker model to ✓. That changes Table 6.1, §6.3 (three in full), ch7 and the abstract, and an examiner will ask how a model with no exfiltration has objective-specific behaviour in full.

§6.1 v3 already tests the clauses in a way that serves either: it states what differs, and that no attack action steals data or impedes.

**Questions:**
- **Q11.** Capitals for tactic names (12.2)?
- **Q12.** Row 2: (a) or (b)?
- **Q13.** Rows 1, 4, 7 and 8 re-worded as proposed? Row 7's strict reading (P to ✗ for the baseline attacker and the APT attacker model): apply it, or keep P?
- **Q14.** After any re-wording, re-run the blind scorer and declare the change beside Table 3.2?

## 13. Round 4: Marc's rulings on §12; Table 3.2 proposals, word by word (2026-10-11)

### 13.1 Rulings and what was applied
- **Q11 yes** ("Title Case … 100 % agree"). Applied dissertation-wide in commit 1754681a:
  - prose, tables and figures;
  - `literature_conventions.md` §a4 updated, and a pointer added to `terminology.md`.
- **§6.1 openers.** Marc asked "why don't we just cite objective-specific behaviour, Table 3.2". Applied: each paragraph names its property and cites Table 3.2. Restating the definition was a re-gloss, and a definition under audit should not be copied into §6.1.
- **The opener's "where the other five live".** Marc reads it as right: 2, 3 and 5 compare without MTD; 4 needs MTD; 1, 6 and 7 are implicit, by construction. He wants the relation to MTD clear. Kept as drafted.
- **Q12.** Re-word row 2 to the source's intent, yes, "but propose it to me, and tell me why" each operative word and hedge.
- **Q14 yes.** After the re-wording, re-run the blind scorer on all four rows: the baseline attacker, Masud et al., Kim et al. and the APT attacker model.
- **NIST SP 800-39** is fetched, and the extract is at `docs/sources/nist2011sp80039.md` (gitignored). Its glossary (App. B, p. B-1) is where row 2's examples come from: objectives "typically include establishing and extending footholds … for purposes of exfiltrating information, undermining or impeding critical aspects of a mission … or positioning itself to carry out these objectives in the future"; (i) "pursues its objectives repeatedly over an extended period of time"; (ii) "adapts to defenders' efforts to resist it"; (iii) "is determined to maintain the level of interaction needed to execute its objectives".

### 13.2 Proposals (none applied; Marc rules each)

The rules each word answers to:
- **specific** (a defined term, or a word with one reading);
- **testable** (each clause is a yes/no question about an attacker model);
- **faithful** (the source's intent, cited).

"Such as" marks an example, never a clause. Marks are *predicted* here; the blind scorer decides them.

**Row 2, objective-specific behaviour.**
- Now: *after the foothold, takes different attack actions for different objectives, such as exfiltration or impediment*
- Proposed: *after the foothold, takes the attack actions that carry out its objective, such as exfiltrating data, impeding a system or positioning for a later attack, so that different objectives lead to different attack actions*
- Word by word:
  - *after the foothold.* Alshamrani §II-C: "for any of the 3 APT goals, the first 2 stages are necessary"; NIST: footholds are established "for purposes of" the objectives. Behaviour before the foothold is shared by every objective, so it neither earns nor costs the property. Clause 1.
  - *takes the attack actions.* The unit rows 3 to 6 use, and the one a run records.
  - *that carry out its objective.* The operative change. Alshamrani: the later stages are "applicable based on the attackers' goal", and a data thief "involve[s] in data exfiltration activities". The objective decides the actions, and the actions do the objective. "Carry out" is chosen over "serve": every action an attacker takes arguably serves its objective, so "serve" tests nothing. Clause 2.
  - *such as exfiltrating data, impeding a system or positioning for a later attack.* NIST's three objectives, all of them (the current row drops the third, which Alshamrani says "take[s] a different path"). "Such as" makes them examples, not clauses, so a model with another objective is not excluded. The gerunds name what the attacker does, matching "takes the attack actions".
  - *so that different objectives lead to different attack actions.* The comparison the property's name promises ("objective-specific"), kept as its own clause, so a model with only one objective can meet clause 2 without clause 3. "Attack actions", not "behaviour": behaviour would let a change of target host count. Clause 3.
- Predicted marks:

  | Model | Clause 1 | Clause 2 | Clause 3 | Mark |
  |---|---|---|---|---|
  | Baseline attacker | ✓ | ✗ (its goal is the compromise itself, NIST's foothold) | ✗ (the scenario changes the host, not the attack actions) | **✗** (now P) |
  | Masud et al. | n/a (nothing follows the database) | ✗ | ✗ | **✗** (now P) |
  | Kim et al. | ✓ | ✓ for positioning (a kept reverse shell, tools installed) | ✗ (one objective) | P |
  | APT attacker model | ✓ | ✗ (the objectives' tactics are unmapped) | ✓ (F.2: brute force 2 % to 19 %) | P |

- **The cost.** Two comparators would fall, and ch3's Finding paragraph would change. Objective-specific behaviour would become a property one model has (Kim in part) plus ours in part. An examiner may read lowering the comparators as convenient. The defence is that the wording is NIST's and Alshamrani's, applied to all four, and re-scored blind.

**Row 4, adaptivity.**
- Now: *chooses its next attack action in response to an MTD disruption*
- Proposed: *chooses its next attack action in response to the MTD disruption it has just met*
- Word by word:
  - *chooses.* Kept. NIST (ii) "adapts"; a fixed response is ch3's in-part clause ("a fixed rule sets the behaviour").
  - *next attack action.* Kept. It sets the horizon at the immediate response.
  - *in response to.* The disruption must be an input to the choice.
  - *the MTD disruption it has just met.* The present disruption only. That is what separates 4 from 7: adaptivity reacts to what is happening now, learning carries the past forward (Cho §V-A :381 "adaptive to dynamically changing … conditions" against §V-D :458 "learn"). "MTD" narrows NIST's "defenders' efforts" on purpose, because MTD is the only defender in the dissertation's scope.
- Predicted marks: unchanged (baseline P, Masud P, Kim ✗, APT P).

**Row 7, learning.**
- Now: *keeps what it observes of past MTD deployments, and uses it to choose later attack actions*
- Proposed: *keeps what it observes of each MTD deployment, and uses it to choose its attack actions after later deployments*
- Word by word:
  - *keeps.* Memory across time (Jalowski "over time").
  - *what it observes of each MTD deployment.* The object is the MTD (Cho: "what types of MTD techniques are used and what the patterns are to trigger an MTD operation"). That is why a memory of vulnerabilities is not learning in this sense.
  - *to choose.* The kept observation must change a choice, not only a speed or an odds.
  - *after later deployments.* The use comes after a later deployment. That is the time horizon that separates 7 from 4.
- Predicted marks:
  - **Baseline attacker and APT attacker model at risk, P to ✗.** Both keep vulnerabilities, not MTD observations, and the memory changes an exploit's time or odds, not a choice. Only the "keeps … uses later" shape is met.
  - Masud ✗ and Kim ✗, unchanged.

**Row 1, campaign persistence** (agent's finding; smaller).
- Now: *runs one multi-stage campaign toward its objective over an extended period*
- Proposed: *pursues its objective through many stages over an extended period, and does not give up*
- Word by word:
  - *pursues … over an extended period.* NIST (i) verbatim.
  - *through many stages.* Alshamrani :55 "multiple stages".
  - *does not give up.* Alshamrani :51; NIST (iii) "determined to maintain the level of interaction". It replaces the untestable weight "extended" with a testable clause: does it carry on through every disruption until the run ends?
  - "one" is dropped, because NIST says "repeatedly".
- Predicted marks: unchanged.

**Row 8, deployment-strategy awareness** (agent's finding).
- Proposed: append *and uses the prediction to choose its attack actions* (Cho §V-D :464 "leverage how MTD works"). A prediction that drives nothing leaves no trace in a run.
- Predicted marks: **Kim at risk, P to ✗.** Its success probability depends on the time to the next deployment, but that is the evaluators' model, not a prediction the attacker makes or uses. The others are unchanged.

**Rows 3, 5 and 6: no change.**
- Row 5 stays, so as not to widen in our favour; the omission of pace is noted for §6.5.
- Row 3's parenthesis is a gloss on "strategy", not a clause.

### 13.3 Questions
- **Q15.** Row 2 as proposed, accepting that the baseline attacker and Masud are likely to fall to ✗? Or a softer clause 3 ("lead to different behaviour"), which would keep the baseline attacker's P through its choice of host but is vaguer?
- **Q16.** Rows 4 and 7 as proposed, accepting that row 7 is likely to fall to ✗ for both the baseline attacker and the APT attacker model?
- **Q17.** Rows 1 and 8 as proposed (Kim's row 8 at risk)?

After the rulings: re-word Table 3.2; re-run the blind scorer on all four rows; re-copy Table 3.3 into Table 6.1; update ch3's per-model paragraphs and Finding, §6.3, ch7 and the abstract; declare the re-wording beside Table 3.2.

## 14. Table 3.2 final wording; blind re-score of all four rows (2026-10-11)

### 14.1 Applied (Marc's rulings)
- Row 1: *pursues*.
- Rows 2–7: *technique* (ATT&CK, §3.1.2).
- Row 3: *sequences of techniques*, with no bracket.
- Row 5: *an intrusion detection system (IDS) … such as*.
- Row 7: *the patterns it observes in*.
- *Attack action* is now used only for MTDSim's six. *IDS* replaces *detector* and *scan detector* dissertation-wide.
- Commits 81d583d4 and 7ccac64b; terminology register rows added.

### 14.2 Blind re-score
**Method.** Four independent scorers, run in parallel. Each received:
- the same rule file: the mark meanings, neutral glosses of *technique*, *IDS*, *MTD disruption*, *MTD mechanism* and *deployment strategy*, and the eight definitions as they now stand;
- only its own model's sources:
  - baseline attacker: Brown 2023, Zhang 2023, and the §2.2 MTDSim text;
  - Masud et al.: their paper;
  - Kim et al.: their paper;
  - APT attacker model: §2.2 and chapter 4, comments stripped, with chapter 4's opener claim, the §4.4.3 claim (adaptivity) and the §4.4.4 claim (learning) redacted.

No scorer saw Table 3.3, Table 6.1 or our scoring paragraphs. The packets are in the session scratchpad (`blind2/`).

| Model | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Baseline attacker, now | ✓ | P | P | P | ✗ | P | P | ✗ |
| Baseline attacker, blind | **P** | **✗** | P | P | ✗ | P | **✗** | ✗ |
| Masud et al., now | P | P | P | P | ✗ | P | ✗ | ✗ |
| Masud et al., blind | P | **✗** | P | P | ✗ | P | ✗ | ✗ |
| Kim et al., now | P | P | ✗ | ✗ | P | ✗ | ✗ | P |
| Kim et al., blind | P | **✗** | ✗ | ✗ | P | ✗ | ✗ | **✗** |
| APT attacker model, now | ✓ | P | ✓ | P | P | P | P | ✗ |
| APT attacker model, blind | ✓ | P | ✓ | P | P | P | **✗** | ✗ |

**Reasons given:**
- **Row 2 (baseline, Masud, Kim):** each has one objective, or two goals that differ only in the target host, so no model uses different techniques for different objectives.
- **Row 7 (baseline, APT):** the memory is of vulnerabilities, not MTD patterns, and it changes time or odds, not a choice.
- **Row 8 (Kim):** the time-to-deployment term is the evaluators' model, not a prediction the attacker makes or uses.
- **Row 1 (baseline):** "the papers never call that duration extended", and "never give up" was read as a set rule. The scorer's own close call would give full credit if pursuing the target across many 50–200 s deployment intervals counts as extended.

**Column consistency, row 1 (the scorers disagree).** The APT attacker model keeps the baseline attacker's loop, and both run the same horizon with the same never-give-up rule on target hosts. The APT scorer gave full credit for exactly the evidence the baseline scorer marked in part. One mark must hold for both.

**Recommendation: full for both.**
- Campaign persistence is not a choice property: "pursues" has no "chooses".
- The rule's fixed-rule clause is about a rule that replaces a decision, so it does not apply.
- The definition's "extended period" is met by a campaign that spans the whole run and many deployments.

**Close calls the scorers named for the APT attacker model:**
- Row 5 is the closest: the pace is assumed, and no technique is chosen against an IDS.
- Row 3: is a weighted random draw a choice, and are six attack actions too coarse?
- Row 2: a different order and frequency of the same six could be read as full or as none.

### 14.3 What follows if the blind marks stand (row 1 reconciled to full)
- **Counts.**
  - APT attacker model: 2 full, 4 in part, 2 none (was 2/5/1).
  - Gains over the baseline attacker: choice of attack strategy (full against in part), detection avoidance (in part against none) and objective-specific behaviour (in part against none).
- **Chapter 3 Finding.**
  - "Only the baseline attacker has one in full, campaign persistence" holds.
  - "Detection avoidance, learning and deployment-strategy awareness are the rarest" becomes: none of the three has objective-specific behaviour, learning or deployment-strategy awareness, and one has detection avoidance in part.
- **Edits needed:**
  - Table 3.3 and Table 6.1 (synced);
  - chapter 3's per-model paragraphs (baseline rows 2 and 7; Masud row 2; Kim rows 2 and 8) and the Finding;
  - §4 opener ("in part, learning") and §4.4.4 ("gives … learning … in part");
  - §6.3 ¶1, ¶2 and ¶4 (the counts; the gains; learning now "none" with the same reason);
  - chapter 7 Contributions, the abstract and chapter 1;
  - the AI Use Declaration, which must name this blind re-score.

**Q18.** Accept the blind marks, with row 1 reconciled to full for both the baseline attacker and the APT attacker model?

## 15. Clause-by-clause tests, and the in-part rule (2026-10-11)

Marc on §14: "are we testing each of the clauses of the definition"; the ch3 paragraphs should "mirror exactly how it's already laid out, but using the language and clausing … we tick this, this and this, but the model doesn't do this, because of this mechanism or the lack of it". He also asks whether *in part* should mean "ticks most of the clauses", with "does a little bit" dropping to none.

### 15.1 The clauses, split once and used for every model
1. **Campaign persistence:** (a) one campaign, (b) multi-stage, (c) toward its objective, (d) over an extended period.
2. **Objective-specific behaviour:** (a) after the foothold, (b) uses different techniques, (c) for different objectives. *Exfiltration or impediment* illustrates (c).
3. **Choice of attack strategy:** (a) chooses, (b) among several sequences of techniques, (c) toward the same objective.
4. **Adaptivity:** (a) chooses its next technique, (b) in response to an MTD disruption.
5. **Detection avoidance:** (a) chooses techniques, (b) that an IDS does not flag. *Passive reconnaissance* illustrates (b).
6. **Cost–benefit reasoning:** (a) chooses each technique, (b) by weighing its cost against its benefit.
7. **Learning:** (a) keeps the patterns it observes in past MTD deployments, (b) uses them to choose later techniques.
8. **Deployment-strategy awareness:** (a) predicts which mechanism deploys next, (b) and when.

### 15.2 Matrix

Key:
- ✓ met;
- ~ met by a fixed rule or an assumption standing in;
- ½ partly met;
- ✗ not met.

The reasons are from the four blind scorers, reconciled.

| Clause | Baseline attacker | Masud et al. | Kim et al. | APT attacker model |
|---|---|---|---|---|
| 1a one campaign | ✓ host by host | ✗ recomputed each interval | ½ each attack starts afresh | ✓ one token |
| 1b multi-stage | ✓ kill-chain procedure | ✓ chains of exploits | ✓ four CKC stages | ✓ 15 tactics in stages |
| 1c toward its objective | ✓ never gives up on a target host | ✓ the database | ✓ the shell | ✓ same loop |
| 1d extended period | ✓ the run, many deployments | ½ static per time point | ✗ one short attempt | ✓ the run, many deployments |
| **1 mark** | **✓** | **P** | **P** | **✓** |
| 2a after the foothold | ✓ C2, scan neighbours | ½ hops after entry | ✓ keeps shell, installs tools | ✓ |
| 2b different techniques | ✗ same six in both scenarios | ✗ | ✗ | ½ same six at different rates; Exfiltration, Impact unmapped |
| 2c different objectives | ✗ two goals, both compromise; scenario changes host only | ✗ one objective | ✗ one objective | ✓ four profiles by objective |
| **2 mark** | **✗** | **✗** | **✗** | **P** |
| 3a chooses | ~ fixed order: credentials, exploit, brute force | ✗ "chooses none" (easiest path assumed) | ✗ | ✓ immediate transition by base weight |
| 3b several sequences | ½ vary only by outcome | ✓ every attack path | ✗ one scenario | ✓ 190–844 openings in attack actions (F.2) |
| 3c same objective | ✓ | ✓ | n/a | ✓ within one profile |
| **3 mark** | **P** | **P** | **✗** | **✓** |
| 4a chooses next technique | ~ fixed response per disruption type | ✗ no next technique chosen | ✗ | ✓ failure matrix reweights the next tactic |
| 4b in response to an MTD disruption | ✓ | ~ assumed ("forces rescanning") | ✗ does not observe the MTD | ½ responds to the failure, cannot tell MTD; none during unmapped tactics |
| **4 mark** | **P** | **P** | **✗** | **P** |
| 5a chooses techniques | ✗ scans actively | ✗ | ~ reverse shell assumed chosen "to evade" | ✗ nothing chosen against an IDS |
| 5b an IDS does not flag | ✗ no IDS | ✗ | ✗ testbed runs no IDS | ~ pace assumed to hide; no IDS, proxy only |
| **5 mark** | **✗** | **✗** | **P** | **P** |
| 6a chooses each technique | ✗ only the exploit's vulnerability | ✗ no choice depends on it | ✗ | ✗ next tactic by CTI weights |
| 6b weighs cost against benefit | ✓ RoA | ✓ cost, RoA computed | ✗ | ✓ RoA inside exploit, inherited |
| **6 mark** | **P** | **P** | **✗** | **P** |
| 7a keeps MTD patterns | ✗ keeps vulnerabilities | ✗ | ✗ | ✗ keeps vulnerabilities |
| 7b uses them to choose | ✗ exploit time halves, no choice | ✗ | ✗ | ✗ success odds rise, no choice |
| **7 mark** | **✗** | **✗** | **✗** | **✗** |
| 8a predicts which mechanism | ✗ | ✗ | ✗ | ✗ cannot see the schedule |
| 8b and when | ✗ | ✗ | ✗ (the time term is the authors' model) | ✗ |
| **8 mark** | **✗** | **✗** | **✗** | **✗** |

### 15.3 The in-part rule
Now (§3.3.2): *P* = "does part of what the definition says, or its authors set the behaviour by a fixed rule … or assume it".

Proposed: **✓ meets every clause; P meets at least half its clauses, or a fixed rule or an assumption stands in for the clauses it misses; ✗ otherwise.**

Applied to 15.2 it reproduces every blind mark (row 1 reconciled):
- baseline row 2: 1 of 3 met → ✗;
- Kim row 2: 1 of 3 → ✗;
- Masud rows 4 and 6: half met → P.

"Does a little bit" (one clause in three) becomes none, as Marc asks. "Half" is used rather than "most" because six of the eight definitions have two clauses, and "most of two" is both, which is full.

**The live question is the assumption branch.** Kim's row 5 and the APT attacker model's row 5 meet no clause outright. Each is P only because an assumption stands in: Kim's assumed evasion, and our pace, assumed to hide the attacker. If assumptions count for nothing, both fall to ✗, and the APT attacker model loses detection avoidance as a gain over the baseline attacker. Keeping the branch is consistent with chapter 3's rule as ratified and with scoring Kim the same way.

### 15.4 The examples and the hedge
- **The examples are illustrations, not clauses, and both are used.** *Exfiltration or impediment* shows what the objectives are; §6.1 tests it: Exfiltration and Impact are unmapped, so no technique carries them out. *Passive reconnaissance* shows a technique an IDS cannot see; the APT attacker model's Reconnaissance maps to scan host, which is active.
- **"Does not flag", not "is unlikely to flag".** The property is the choice. A probability ("unlikely to flag") would admit pace alone (low and slow) and widen the row toward our model, the direction already declined for row 5. Passive reconnaissance is a technique an IDS cannot flag at all.

**Q19.** The in-part rule as proposed, with the assumption branch kept?

**Q20.** Then: redraft chapter 3's four model paragraphs clause by clause in their current layout ("It has X in part: it does a and b, but not c, because …"), apply the marks (Tables 3.3 and 6.1), and carry every consequence (§14.3).

## 16. Q18–Q20 applied (2026-10-11)

**Marc's rulings:**
- The clause-by-clause test goes in an appendix, for transparency; §3.3.2 keeps the plain rule.
- An assumption can earn at most *in part* ("you have to model an assumption properly").
- "Does not flag" stays.
- The blind marks are accepted, with row 1 reconciled to full for both the baseline attacker and the APT attacker model.

**Applied:**
- **§3.3.2 rule.** Clause by clause, with three marks: ✓ every clause; P at least half, met outright or by a fixed rule or an assumption; ✗ neither. It points to the new appendix.
- **Tables 3.3 and 6.1, synced:**
  - baseline attacker: ✓ ✗ P P ✗ P ✗ ✗;
  - Masud et al.: P ✗ P P ✗ P ✗ ✗;
  - Kim et al.: P ✗ ✗ ✗ P ✗ ✗ ✗;
  - APT attacker model: ✓ P ✓ P P P ✗ ✗.
- **Chapter 3 model paragraphs** (current layout, one sentence per property, clause language):
  - baseline attacker: objective-specific behaviour and learning are now crosses, with mechanism reasons;
  - Masud et al.: objective-specific behaviour is a cross;
  - Kim et al.: objective-specific behaviour and deployment-strategy awareness are crosses.
- **Chapter 3 Finding.** None of the three has objective-specific behaviour, learning or deployment-strategy awareness; only Kim et al. has detection avoidance, in part.
- **Counts:**
  - Chapter 1: two in full, four in part.
  - Chapter 4 opener: built for three properties; two in full, four in part.
  - §4.4.4: the vulnerability memory "is not learning … keeps vulnerabilities, not the patterns of MTD deployments, and changes the odds of an exploit, not which technique comes next".
- **§6.3:**
  - ¶1: counts; three gains; the rewording declared ("lowered marks and raised none"); the blind sentence now covers four scorers, one mark reconciled, pointing to the appendix.
  - ¶2: the objective-specific reason (the same six attack actions at different rates); cost–benefit reasoning separated; learning and deployment-strategy awareness "lacks".
  - ¶4: three gains.
- **Chapter 7 Evidence:** four in part; three gains.
- **New Appendix B, "The attacker models tested clause by clause"** (label `app:clause-tests`):
  - the rule;
  - the declaration of the rewording (six marks lowered, none raised) and of the blind re-score, with the row 1 reconciliation and its reason;
  - Table B.1, every clause against the four models: yes, rule, assumed or no, and the resulting mark.
  - The cells are typed, not generated (judgement, no data artefact).
  - One clause label is shortened for width ("keeps the patterns of past MTD deployments").
- **Appendix letters shift:** the old B–F are now C–G. Handoffs written before today use the old letters; `\ref` labels are unchanged.

Build clean: 118 pages, 0 undefined, overfull count unchanged at 14.

**Owed:**
- The AI Use Declaration is still empty. §6.3 and Appendix B cite it for both blind re-scores (2026-10-08 and today); the packets are in the session scratchpad (`blind2/`).
- The abstract states no counts (checked), so it needs no change.
- Future work: dynamic weighting (Q8).

## 17. Predicates replace clauses (2026-10-12)

**Trigger.** A role-played critical supervisor read Table 3.2, the §3.3.2 rule, Appendix B and §6.3 cold. Points raised:
1. the rewording moved the comparison our way: it lowered five marks of the other models and one of ours, and objective-specific behaviour became our gain only after it;
2. most in-part marks were "setting without behaviour": the clause split cut the verb from its modifiers, and "at least half" counted them equally;
3. "chooses" for a weighted draw had no stated reason;
4. "low and slow" had no test;
5. the rule was worded three ways (§3.3.2, Appendix B, the Table 6.1 caption).

Marc's ruling: point 1 was warranted, since the old marks could not be argued in discussion. The root cause of 2 is that the clauses were not predicates, so none could be true or false on its own. Table 3.2 stays as it is. Make the derivation apparent in Appendix B so that the mark follows from the cells alone, and change no more than necessary.

**Applied.**
- **Rule**, word for word in §3.3.2 and Appendix B:
  - a *behaviour predicate* is the verb, with every condition it carries; a *qualifier predicate* is a condition that can be checked apart;
  - cells are yes / rule / assumed / no;
  - ✓ = every cell yes; P = a behaviour predicate is yes, rule or assumed, but some cell is not yes; ✗ = every behaviour predicate is no.
- **Predicates.** Each is Table 3.2 word for word, except that rows 1 and 6 each split off one qualifier ("over an extended period, across MTD deployments"; "for each technique") and row 5 splits at its "and". Row 5's first predicate carries its test: "slower than the baseline attacker" (Marc).
- **Marks.** Masud rows 3, 4 and 6 go from P to ✗ (every attack path but no choice; recomputation but no next technique; RoA computed but no choice depends on it). No other mark changes. The APT attacker model stays ✓ P ✓ P P P ✗ ✗, with the same three gains.
- **APT row 2** is P by an *assumed* cell. The attack profiles enter different tactics after the foothold by objective; Collection, Exfiltration and Impact are unmapped, so their techniques are assumed. This is the same footing as Kim's assumed evasion. Alshamrani's life cycle is the cited observation behind the definition, not the assumption.
- **Appendix B** gains a paragraph giving the reasons for the APT attacker model's four non-obvious cells (row 2 assumed, row 3 yes against the baseline attacker's fixed order, row 4 rule for the failure matrix on any failure, row 5 rule for the declared durations). The history paragraph declares the clause-counting rule the blind scorers used and the predicate change. Against the first scoring, nine marks were lowered and none raised: one ours (learning) and eight of the others', including objective-specific behaviour for all three, which leaves the APT attacker model the only one with it in part.
- **Knock-ons:**
  - the Table 6.1 caption now uses Table 3.3's gloss (the stale "a fixed rule or assumption takes the place" is gone);
  - in §6.3, the blind scorers gave every mark but four (one reconciled, three Masud marks lowered by the predicates), and "every clause" became "every predicate";
  - the Masud paragraph in §3.3.2 and the Masud rows of Tables 3.3 and 6.1 are updated.
- **Checks.** Build clean: 119 pages, 0 undefined, 14 overfull (unchanged).

**Next (Marc).** Marc will supply the three papers. Their attacker models are to be extracted near word for word and diagram for diagram, and only the contentious marks argued against the predicates; the strong ones are left alone.

## 18. Comparators tested against the predicates; counterpoint table (2026-10-12)

- **Kim et al.** (extraction in `docs/sources/extractions/kim2026.md`):
  - P ✗ ✗ ✗ P ✗ ✗ ✗ confirmed.
  - The row 1 qualifier was reworded to "until it reaches its objective, however many MTD deployments that takes", because one Kim attack outlasts a deployment.
  - The §3.3.2 row 8 sentence now reads: predicts ("can determine", p. 10), but no technique leverages the prediction.
- **Masud et al.** (`masud2025.md`):
  - P ✗ ✗ ✗ ✗ ✗ ✗ ✗ confirmed under the strict reading. Behaviour the paper only describes (RoA prioritisation, "fresh scans and adaptation", p. 7) is no.
  - Marc's ruling: strict, but acknowledge every elephant.
  - Appendix B now carries the boundary: an assumption counts only where the model takes the behaviour's step and its authors assume what the model cannot show.
  - The §3.3.2 Masud paragraph gains one sentence quoting the described behaviour.
- **Why strict** (recorded for the viva):
  - Deleting Masud's described sentences changes no number in the paper.
  - The description contradicts Algorithm 2: every path is aggregated, none prioritised.
  - A generous rule, applied evenly, would make Kim's row 2 assumed ("based on the objectives of the attacks", p. 7) and end the claim that only the APT attacker model has objective-specific behaviour.
- **Table B.2 (tab:counterpoints)** quotes, for each contested cell, the strongest counterpoint from the source and why the cell stands. It covers Masud et al. (2, 4, 6), Kim et al. (1 qualifier, 2, 8) and the APT attacker model (2, 3, 4, 5); the APT attacker model's former reasons paragraph moved into it.
- **Owed:** the baseline attacker's rows, after Brown 2023 and Zhang 2023 are extracted the same way.
- **Checks:** build clean, 119 pages.

## 19. The APT attacker model scored blind from its own chapter (2026-10-12)

**Packet** (session scratchpad `blind_apt/`):
- Chapter 4 §§4.1–4.4 as rendered text, with the authors' property claims redacted;
- §2.2 (MTDSim and the baseline attacker);
- the Appendix B rule and predicates.

The scorer was a general-purpose agent, told to use those files only.

**Blind marks:** ✓ P ✓ P P **✗** ✗ ✗. Ours are ✓ P ✓ P P **P** ✗ ✗. Every other cell agrees: row 2 assumed, row 3 yes, row 4 rule, row 5 rule/no.

**Row 6, cost–benefit reasoning: the one disagreement.**
- *Finding 1, verified in code:* the APT attacker model drives the shared exploit core (`attack_operation._do_exploit_vuln`, `driven=True`). That core takes each service's vulnerabilities sorted by RoA (`mtdnetwork/component/services.py:257`, `:278-287`). So our P is true of the model, but **Chapter 4 never says so**; only §2.2.3 states it, for the baseline attacker.
- *Finding 2, on merit:* the RoA order chooses *which vulnerability* the exploit attack action tries, which is a choice within one ATT&CK technique, not among techniques. Under the strict reading (technique = ATT&CK technique, as ruled), row 6's behaviour predicate is no for **both** the baseline attacker and the APT attacker model. That gives P → ✗ for both and leaves the gains over the baseline unchanged. The counts would become: APT attacker model 2 full, 3 in part, 3 none; baseline attacker 1 full, 2 in part. **Proposed to Marc; not applied.**

**Other contested cells, with counterpoints to add to Table B.2:**
- APT row 1Q: Chapter 4 never states when a run ends. The run ends by the simulator's rule (objective at NCR > 0.8, or the time horizon, `movement/run.py:528`), the same for both attackers; nothing in the model ends its campaign.
- APT row 4: a deployment during an unmapped tactic "never changes which tactic comes next" (§4.4.1).
- APT row 5 B1: it is faster than the baseline attacker on brute force (4.5 s against 20 s) and enumerate host. It is slower overall through the declared durations, mostly time in unmapped tactics.

**Applied the same day:** the §3.3.2 baseline sentence now reads "which changes only the host it attacks next and whether it gives up on it".

## 20. Row 6 ruled strict (Marc 2026-10-12)

**Ruling.** Cost–benefit reasoning is none for the baseline attacker and the APT attacker model alike. The RoA order chooses a vulnerability within one technique, not among techniques. Marc's standing instruction: discussion and appendix entries may be updated automatically; ch1–ch5 (and ch7) changes go past him first.

**Applied:**
- Table 6.1: baseline attacker and APT attacker model, column 6 → ✗.
- §6.3 ¶1: "two in full, three in part, and lacks three". The blind-scorer sentence now gives six differences, which Appendix B accounts for.
- §6.3 ¶2: "Three it lacks", with the RoA reason; "Campaign persistence shows by construction".
- Appendix B, Table B.1: row 6 all no.
- Appendix B, history: the fifth scorer (Chapter 4 alone) is declared; eleven marks lowered against the first scoring, none raised.
- Appendix B, Table B.2:
  - baseline row 6 now argues the behaviour predicate;
  - APT rows added for 1Q and 6;
  - APT rows 4 and 5 strengthened with the blind scorer's points.
- `apt_model_criterion.md`: axis 6 ruling note.
- Build clean, 120 pages.

**Proposed, then approved and applied the same day** (ch1, ch3, ch4, ch7):
- ch1 contributions: "four in part" → "three in part".
- ch3, Table 3.3: baseline attacker column 6 → ✗. Until this lands, Table 3.3 and Table 6.1 differ.
- ch3 baseline paragraph: the cost–benefit sentence becomes none.
- ch3 Finding: add cost–benefit reasoning to the list of properties none of the three has.
- ch4 opener: drop "and, in part, its cost–benefit reasoning"; "four in part" → "three in part".
- ch7 Evidence: "four in part" → "three in part".


## 21. Critique of §6.1 v3 after the mark changes (2026-10-12; no redraft, Marc's read to follow)

Marc: v3 reads better, but it still reads as a list ("number, number, point, point"), with rhetoric, re-explanation and a vestigial last paragraph; and has the re-scoring made it stale? Read against the current tex (§6.1 untouched since 7ccac64b, checked), Table 3.2's current wording, Appendix B, §6.3, and the ch5 redraft pipeline (`2026-10-06_ch5_results_prose_redraft.md` §0, §1, §4, §5).

### 21.1 Stale or not

- **Marks: not stale.** No §6.1 sentence states a mark, and no marking commit touched it.
- **What changed for the APT attacker model:** learning and cost–benefit reasoning fell to none (✓ P ✓ P P ✗ ✗ ✗). Against the baseline attacker (✓ ✗ P P ✗ ✗ ✗ ✗) it now differs on exactly three properties: objective-specific behaviour (new, since the baseline fell to none), choice of attack strategy and detection avoidance. **These are the three §6.1 discusses.** The opener can use that (21.3, point 4).
- **Stale from the wording changes, not the marks:**
  1. Table 3.2 rows 2–7 now say *technique*. §6.1 tests rows 2 and 5 in *attack actions* and never says once how the two relate (¶3's close: "chooses no attack action against an IDS"; the definition: "chooses techniques an IDS does not flag"). One bridge, once, or the clause tests read off-unit.
  2. Row 5 now opens on *moves low and slow*, the definition's own first predicate (test: slower than the baseline attacker). ¶3 still cites §3.1.1 for it. Point at the definition.
  3. The IDS sweep: ¶3 says "MTDSim has no IDS", then "The IDS flags the APT attacker model less", then "MTDSim has none to choose against". §4.5.1's stand-in needs naming as the stand-in here.
- **Downstream, not §6.1's text:** §6.3 cites §6.1 for "the pace is assumed to hide the attacker", while Appendix B types row 5's first predicate *rule*, not *assumed*. §6.3 still names the causes "the tactic durations and order" (twice), §6.1 "the unmapped tactics and the order of its tactics" (known, §12.1).

### 21.2 Measured

About 1 000 words against the ~600 guide; 39 cross-references (20 to sections), one per 25 words. *Take* 8 times in three senses (takes time, takes 26–47 % of steps, takes openings / attack actions); *differ* 11; *so* 9; *therefore* 3.

### 21.3 Structure: why it reads as a list

1. **The opener names two causes; the paragraphs never hand them back.** ¶1 explains through each attack profile's own base weights (the order of its tactics, unnamed) and the unmapped objective tactics (unnamed); ¶2 names neither term; ¶3 names *unmapped tactics*; ¶4 uses both plus a third cause (Command and Control's 45 s) and a fourth fact (same networks, F.1). The reader holds two labels and never meets them again verbatim. The throughline is the one-term rule applied to the causes: each paragraph's claim sentence names its cause in the opener's words.
2. **The opener states causes of "each difference" without stating the differences.** A discussion opens on its principal finding (Hopkins and Dudley-Evans; Docherty and Smith). The ch5 spine (§1, A4) made outcome §5.2's **headline** and "the reference for every effect in §5.3"; §6.1 demotes it to "what these differences cost". One opening sentence carrying the whole finding (more distinct openings, lower attack rate, lower ASP and NCR) makes the last paragraph the payoff of that sentence, not a pivot.
3. **The last paragraph has nine jobs in 278 words:** finding and cause; F.3 evidence; why attack actions fail (duplicates ¶2's last sentence); a third cause (C2 45 s); same networks (F.1); the MTTC bound; the longer-run rival; "the baseline attacker is the reference …" (says nothing); the §6.2 pointer. Its earned so-what is the *reason* for the pointer: the APT attacker model compromises less with no MTD, so raw NCR under MTD would credit MTD with the attacker's weakness; §6.2 therefore compares NCR reduction against each attacker's own NCR. The text writes "therefore" after a sentence that does not supply that reason.
4. **The opener's middle (S5–S7) is a roadmap.** "Adaptivity needs MTD and is read in §6.2, and §6.3 scores all eight" is chapter allocation (the preamble does it). "Each paragraph below tests …" is meta. Overturns §13.1's "kept as drafted" on merit: Marc's own question ("where do the other five live?") is answered by the preamble. Candidate replacement, one sentence with argument in it: these are the three properties Chapter 5 measures with no MTD, and the three on which Table 6.1 marks the two attackers differently. Tension with Q7 (no marks in §6.1): it points at Table 6.1 without scoring. Marc's call.
5. **Paragraph leads.** ¶1 opens on construction (§4.2 restated); its claim is in S2 and its baseline contrast is the last sentence, an afterthought in a "versus baseline" section. ¶2 opens on the finding (good). ¶3 opens on a limitation ("MTDSim has no IDS"); its best sentence (lower attack rate, mostly the unmapped tactics) is second. ¶4 opens on a rhetorical line.
6. **Implications are signposts.** Three "Section 6.x reads …" pointers stand where each paragraph's so-what should be. The so-whats already earned: ¶1, in MTDSim an objective shows only in how often each of the six attack actions runs (§6.3's contract); ¶2, an MTD tested against the baseline attacker meets one opening (v1 had it; v3 lost it); ¶3, in MTDSim hiding is time without an attack action (present, mid-paragraph); ¶4, the NCR-reduction reason above.

### 21.4 The sort test, sentence by sentence (cut = lives elsewhere or nowhere)

| Where | Sentence (abridged) | Verdict | Why |
|---|---|---|---|
| Opener S1 | "Two things … adds to MTDSim explain most of each difference …: [the two]" | R | Subject is a count ("two things"); the content is after the colon. Name the two as subject. "Most of each difference" → "most of the differences". |
| Opener S2 | unmapped tactics "take time but dispatch no attack action (§4.4.1), and they take 26 to 47 % of … steps" | C/R | Re-defines a ch4 term (ruled against, §11.2 point 6); 26–47 % replays §5.2. The fact the argument turns on is run time (a third to over half, F.3), and ¶3/¶4 carry it. |
| Opener S3 | order follows the base weights …, "where the baseline attacker's procedure fixes the order" | C here | Said again in ¶2 (S3, S5). One home: ¶2. Cite Figure 2.x once, not §2.2.3. |
| Opener S4 | failure matrix, vulnerability memory move NCR negligibly | K | The rival ruled out; licenses "most". Move up, next to S1. Note §6.3 says it twice already. |
| Opener S5–S7 | roadmap | C | 21.3 point 4. |
| ¶1 S1 | profiles built from one objective's flows (§4.2), own edges and base weights, divide steps differently | R | Construction first, finding last. Lead with the finding and its cause in the opener's words. |
| ¶1 S2 | Credential Access, 10 % of c1, 1 % of c3, holds after the foothold (F.2) | K | The best evidence, and the definition's "after the foothold". Say what it tests. c1 and c3 are codes; c4 is glossed in S6, these are not. |
| ¶1 S3 | same six attack actions, at different rates | K/merge | Merge with S2: different/same/different is a U-turn over three sentences. |
| ¶1 S4 | Collection, Exfiltration and Impact … unmapped, so no attack action steals data … | R | §5.2 says the first half verbatim. Keep the consequence, in the definition's terms (the techniques of those tactics are assumed for their duration, Appendix B's word). |
| ¶1 S5 | "built to differ, so the runs show that the difference survives in MTDSim" | R | "Survives" is a riddle. Plainly: the runs show the built difference reaches MTDSim's attack actions. |
| ¶1 S6 | "They do not show that the objective causes it: c4 … differs too" | K | Honest bound. Pronouns: they = the runs, it = the difference. |
| ¶1 S7 | baseline follows one procedure in either scenario … | M → lead | The contrast the section is named for. |
| ¶2 S1 | hundreds of openings over eight steps against one over four and three over eight | K | Finding first. The "and so of one objective" interjection breaks subject from verb. |
| ¶2 S2 | counted in attack actions, 190–844 against 3 (F.2) | C | §6.5 carries the unit concession and the recount (§8 Q2, explain once). |
| ¶2 S3 | decision place, immediate transition, probability proportional, share of flows (§4.3) | R | 40 words of §4.3. The discussion needs the cause only: the next tactic is picked at random in proportion to how often the attack flows took each edge. |
| ¶2 S4 | every opening made of edges the flows took | K | §6.3's contract. |
| ¶2 S5 | baseline's procedure fixes the order of credentials, exploits, brute force | K (one home) | Keep here, cut from opener. |
| ¶2 S6 | weights change only after a failure, so blind to the network; exploit before its scan | M → ¶4 | ¶4 S4 says the exploit-before-scan again. One home: ¶4, where it causes failures. |
| ¶2 S7 | "Section 6.2 reads what MTD does against the many openings" | R | Signpost → the so-what (one opening against the baseline attacker). |
| ¶3 S1 | MTDSim has no IDS, so §4.5 measures it by proxy | C | §4.5.1 and §6.5 say it. Limitation-first lead. |
| ¶3 S2–S4 | attack rate lower, mostly the unmapped tactics; more steps in them, lower rate; with no time in them, about the baseline's (F.3) | K, lead | The paragraph's claim and its two pieces of evidence. "They" in S4. |
| ¶3 S5 | Stealth is one of them, so it hides by spending time without an attack action | K | The sharpest sentence; it is the so-what. Move to the close. |
| ¶3 S6 | failed attack actions not counted, never reach the network | C or R | §4.5.1's rule, with no stated job here. Either one clause as a second, smaller contributor, or cut. |
| ¶3 S7 | the IDS flags it less: attack confidentiality orders the five as attack rate | K/R | Name the stand-in IDS (21.1). |
| ¶3 S8 | moves low and slow, "as §3.1.1 describes …", "pace set on purpose", §4.4.2 times Stealth | R | Now the definition's first predicate: say it meets it, by its declared tactic durations (Appendix B: *rule*). "On purpose" is colloquial. Two section refs → one. |
| ¶3 S9 | chooses no attack action against an IDS; MTDSim has none | K/R | The second predicate. *Technique*, the definition's noun (21.1). |
| ¶4 S1 | "Attack outcome shows what these differences cost" | C | Rhetorical; S2 is the finding. |
| ¶4 S2 | fewer runs reach a target, fewer hosts by 15 000 s, likely fewer attack actions | K, lead | Finding + hedged cause. Name the two causes here verbatim. |
| ¶4 S3 | unmapped a third to over half the run; 15–30 % fail for missing preconditions (F.3) | K | The two causes' evidence. |
| ¶4 S4 | attack actions written for the procedure …; "the order of its tactics can put an exploit before the scan" | K (one home) | "its" is ambiguous after "MTDSim's attack actions … the baseline attacker's procedure". |
| ¶4 S5 | Command and Control 45 s against 5 s, likely slows finding hosts | C (recommend) | A third cause in a two-cause frame, on the weakest evidence (Appendix C's 45 s also times Persistence and Stealth, §11.1), and F.3 shows unmapped time alone restores the rate. |
| ¶4 S6 | success depends mostly on the network: profiles succeed almost only where baseline does (F.1) | R | Leads on a sub-claim about the network. The point for this section: same attack actions, same networks, fewer runs. |
| ¶4 S7 | MTTC over different runs (42–139 against 656); 600–2 200 s longer | R | Bound before finding. §6.4 cites §6.1 for "MTTC compares different runs", so it stays, finding first. |
| ¶4 S8 | longer run may narrow the gap; not tested | K | The rival, one clause. |
| ¶4 S9 | "The baseline attacker is the reference …, and the lower ASP shows how the two differ" | C | Says nothing (21.3 point 3). |
| ¶4 S10 | "§6.2 therefore reads MTD by NCR reduction" | R | Supply the reason; this is the section's close. |

### 21.5 The takeaway each paragraph owes the reader (one line each; job, not prose)

- **Opener:** with no MTD, the APT attacker model varies its openings more, attacks at a lower rate and succeeds less than the baseline attacker; its unmapped tactics and the order of its tactics explain most of this; removing the failure matrix or the vulnerability memory changes NCR negligibly.
- **¶1 objective-specific behaviour:** after the foothold the attack profiles use the six attack actions at different rates, through the order of their tactics, where the baseline attacker's are the same in either attack scenario; the objectives' own tactics are unmapped, so in MTDSim an objective shows only in those rates, and c4, with no objective, differs too.
- **¶2 choice of attack strategy:** the order of its tactics is picked from the attack flows at each decision place, so its runs have hundreds of openings, all made of edges the attack flows took, where the baseline attacker's procedure gives one to three; an MTD evaluated against the baseline attacker meets one opening.
- **¶3 detection avoidance:** the unmapped tactics lower its attack rate (without their time it would match the baseline attacker's), and attack confidentiality agrees; it moves low and slow by its declared tactic durations and chooses no technique against an IDS; in MTDSim, hiding is time without an attack action.
- **¶4 attack outcome:** the same two causes leave it fewer attack actions that succeed, so it reaches a target host in fewer runs and compromises fewer hosts, on the same networks as the baseline attacker; a longer run might narrow the gap; because its NCR with no MTD is lower, §6.2 compares NCR reduction.

### 21.6 Applying the ch5 pipeline (§0, §1, §4, §5 of the ch5 redraft)

- ch5's fix was **one chosen finding per paragraph** before any sentence. §6.1 needs the same: one chosen explanation per paragraph (21.5), then sentences.
- ch5's gate item 8, inverted for a discussion: **could the sentence be true without any explanation, read straight off a ch5 float?** Then it is a replay; cut it or reduce it to the back-reference. Fails: opener S2, ¶1 S4, ¶2 S1's second half, ¶4 S7's counts.
- ch5's gate items 1, 2, 5, 7 apply unchanged: at most three clauses; the subject leads; every noun has an antecedent in ch2–5; no fact in two sentences (here: the procedure fixes the order ×2, base weights ×2, exploit before scan ×2, proxy ×2 with §4.5.1/§6.5).
- Words, by sense: *take* → unmapped tactics *last*; runs *have* openings (§5.2's verb); attack profiles *use* attack actions.

## 22. From critique to redraft: the plan (2026-10-12; proposal, nothing applied to the tex)

Marc accepted §21 ("beautiful test … I agree on your sentence-level stuff") and asked how it becomes a redraft that is methodical and does not go backwards on purpose, context and audience. His proposed shape: the opener as a mini-introduction (what differs, on which three properties; the two causes; everything else negligible), one paragraph per property (the takeaway, this model against that, the cause, hedged), then outcome. His question: is outcome a vestigial fourth paragraph, or does it support each property?

### 22.1 The frame every sentence is checked against (written once, before any slot)

- **Purpose.** Explain why, with no MTD, the APT attacker model differs from the baseline attacker on the three properties where Table 6.1 marks them differently, and what those differences change in the attack outcome.
- **Context.** §5.2's results, explained by Chapter 4's mechanisms. No marks (§6.3 scores); no bounds that §4.5 or §6.5 state; no new numbers beyond the Appendix G (formerly F) reads already ratified.
- **Audience.** A fourth-year CS student who has read Chapters 1–5 and holds only their terms, and an examiner who checks each claim against a float.
- **Nouns the section may use** (all defined in ch2–5): attack action, tactic, technique, unmapped tactic, tactic duration, Petri net, decision place, base weight, attack flow, attack profile, objective, foothold, attack scenario, the baseline attacker's procedure, step, opening, relative tactic occurrence, distinct openings, attack rate, attack confidentiality, IDS (the stand-in of §4.5.1), ASP, NCR, MTTC, time limit, failure matrix, vulnerability memory, precondition. **Not:** stealthier, quieter, spread, survive, draw, cost (as a metaphor), "two things".

### 22.2 Marc's shape, tested

**Agreed:** the opener is a mini-introduction that says what differs before saying why; one paragraph per property, in §5.2's order; each paragraph = takeaway, this model against the baseline attacker, the cause (hedged where inferred).

**Two corrections on merit:**
1. **"We ablated everything else and it was negligible" overclaims.** §5.4 ablated three components. The failure matrix and the vulnerability memory are negligible. The attack profiles are not: with no MTD, NCR is 0.171 with them and 0.189 on the attack graph ($d = -0.28$), and they beat every random partition of the same sizes ($d$ 0.25 to 1.47). The two causes themselves have no ablation (§6.3: "the Petri net's choice has no ablation of its own"). What supports them is Appendix G.3 for the unmapped tactics (attack rate with no time in them, 1.60–2.16 against 1.71) and the baseline attacker for the order. The opener may say only: removing the failure matrix or the vulnerability memory changes NCR negligibly.
2. **Attack outcome does not show a property emerging.** A lower ASP is no evidence of being more APT-like: §6.3 says "an attacker that compromises more is stronger, not closer to an APT attacker". What outcome does show is that the mechanisms behind the three properties change what MTDSim measures. That is its motivation, and it is why §6.2 cannot compare raw NCR.

### 22.3 Structure: outcome split by cause, plus a short close (recommended)

Each mechanism's effect on outcome goes into its own property paragraph as one sentence, where the evidence exists:
- **¶1:** grouping the attack flows by objective changes NCR against random groups of the same sizes (§5.4). This also answers ¶1's own bound (is it the objective, or the group size?).
- **¶2:** the order ignores preconditions, so 15–30 % of the attack actions it dispatches fail (G.3).
- **¶3:** the time in unmapped tactics leaves it fewer attack actions by the time limit.

The close then **sums, it does not add**. It introduces no new cause:
- the two causes together: fewer runs reach a target host, fewer hosts compromised;
- on the same networks as the baseline attacker (G.1), so MTTC is over different runs;
- a longer run might narrow the gap (untested);
- the implication: a lower NCR with no MTD is how the APT attacker model behaves in MTDSim, so §6.2 compares each attacker's NCR reduction against its own NCR with no MTD.

This keeps the homes that §6.4 cites in §6.1 ("ASP and NCR call a quiet attacker weak"; "MTTC compares different runs"). Command and Control's 45 s is cut (§21.4).

Alternative: no close, with the implication moved to the opening of §6.2. Rejected: §6.4's two back-references would lose their home, and the headline that §5.2 founds would never be summed.

### 22.4 The chosen explanation per paragraph (the spine)

| ¶ | Takeaway (the one thing the reader leaves with) | Cause, in the opener's words | Against the baseline attacker | Outcome sentence | Hedge / bound (one) | Float |
|---|---|---|---|---|---|---|
| 0 | With no MTD, the APT attacker model differs from the baseline attacker on objective-specific behaviour, choice of attack strategy and detection avoidance (the three that Chapter 5 measures and on which Table 6.1 marks them differently), and it compromises less | the unmapped tactics; the order of its tactics | — | stated in the finding | failure matrix and vulnerability memory negligible | Table 5.2, §5.4 |
| 1 | After the foothold, the attack profiles use the six attack actions at different rates, but no attack action carries out an objective: the property shows in the order, not in the acts | order (each attack profile's own base weights); unmapped (Collection, Exfiltration, Impact) | the same attack actions in either attack scenario | the attack profiles compromise more than random groups of the same sizes | c4, with no objective, differs too | Fig. 5.1(a), G.2 |
| 2 | Its runs open in hundreds of ways because the order of its tactics is picked from the attack flows; the baseline attacker's procedure gives one to three | order | its procedure fixes the order | the pick ignores preconditions: 15–30 % of dispatched attack actions fail | every opening is made of edges the attack flows took (§6.3's contract) | Fig. 5.1(b), G.3 |
| 3 | It moves low and slow because its unmapped tactics hold it a third to over half its run with no attack action; it chooses no technique against an IDS | unmapped (Stealth and Defense Impairment among them) | higher attack rate, lower attack confidentiality | fewer attack actions by the time limit | with no time in unmapped tactics, its attack rate would be about the baseline attacker's | Table 5.2, Fig. 5.1(a) All unmapped, G.3 |
| 4 | The two causes leave it fewer attack actions that succeed, so it compromises less, on the same networks; MTD is therefore compared by NCR reduction | both, named again | lower ASP and NCR | — (this *is* outcome) | a longer run might narrow the gap | Table 5.2, G.1 |

### 22.5 Slot sheets (job · facts · ceiling); about 570 words in all

**¶0, ~90 words, 3–4 sentences.**
- O1 *finding.* The three properties by name; the two attackers differ on them with no MTD; the APT attacker model compromises less (Table 5.2). *Ceiling:* no metric values (§5.2 has them); a pointer to Table 6.1 only for "where they are marked differently" (Q22).
- O2 *causes.* The unmapped tactics; the order of its tactics. Name them as the subject. *Ceiling:* "most of", not "each".
- O3 *rival.* Removing the failure matrix or the vulnerability memory changes NCR negligibly (§5.4). *Ceiling:* not "everything else" (22.2).
- O4 *bridge (once, for ¶1 and ¶3).* Table 3.2 defines the properties in techniques; in MTDSim an attack action carries out one of a tactic's techniques (§4.4.1's words), so the runs test them through attack actions. *Ceiling:* no "proxy" or "operationalisation" (new words for an existing sentence).

**¶1, ~130 words.**
- 1a *claim + baseline.* After the foothold the attack profiles use the attack actions at different rates; the baseline attacker uses the same ones in either attack scenario. Facts: Credential Access, the only tactic that dispatches brute force, 10 % against 1 % (Fig. 5.1(a)), holding after the foothold (G.2). *Ceiling:* name what c1 and c3 are, or say "between attack profiles".
- 1b *cause.* Each attack profile has its own base weights, so the order of its tactics differs.
- 1c *limit.* Collection, Exfiltration and Impact are unmapped tactics, so no attack action carries out an objective. *Ceiling:* no re-gloss of "actions on objectives"; no not-X-but-Y.
- 1d *outcome (Q23).* The attack profiles compromise more than random groups of the same sizes (§5.4).
- 1e *bound.* c4, whose attack flows reached no objective, differs as much, so the difference comes from the attack flows grouped together more than from the objective itself. Hedged.

**¶2, ~120 words.**
- 2a *claim + baseline.* Hundreds of distinct openings against one over four steps and three over eight (Fig. 5.1(b)).
- 2b *cause.* At each decision place the next tactic is picked in proportion to how often the attack flows took each edge (§4.3); the baseline attacker's procedure fixes its order (Figure 2.x). *Ceiling:* one sentence, plain words, no symbols.
- 2c *contract.* Every opening is made of edges the attack flows took.
- 2d *outcome.* The pick ignores the preconditions of MTDSim's attack actions, so it can exploit before the scan the exploit needs; 15–30 % of dispatched attack actions fail (G.3).
- 2e *so-what.* An MTD evaluated against the baseline attacker meets one opening.

**¶3, ~130 words.**
- 3a *claim + baseline.* A lower attack rate and a higher attack confidentiality than the baseline attacker (Table 5.2).
- 3b *cause.* Its unmapped tactics hold it a third to over half its run with no attack action (G.3); the more steps an attack profile spends in them, the lower its attack rate (Fig. 5.1(a), All unmapped).
- 3c *evidence.* With no time in unmapped tactics, its attack rate would be about the baseline attacker's (G.3).
- 3d *the definition's first predicate.* It moves low and slow (Table 3.2) by its declared tactic durations (§4.4.2). *Ceiling:* no "on purpose"; no §3.1.1.
- 3e *the second predicate.* It chooses no technique against an IDS: the IDS of §4.5.1 only counts. *Ceiling:* never "MTDSim has no IDS" next to "the IDS flags".
- 3f *so-what.* Stealth and Defense Impairment are themselves unmapped, so in MTDSim, hiding is time without an attack action. The fewer attack actions by the time limit feed ¶4. *Ceiling:* the outcome sentence may merge here.

**¶4, ~100 words, 4 sentences.**
- 4a *finding + causes.* Fewer runs reach a target host, and it compromises fewer hosts by the time limit (Table 5.2), likely because the unmapped tactics and the order of its tactics leave it fewer attack actions that succeed (¶2, ¶3; no new numbers).
- 4b *same networks.* It succeeds almost only where the baseline attacker does (G.1), likely because both compromise through the same attack actions; so its MTTC is over fewer, different runs.
- 4c *rival.* A longer run might narrow the gap; not tested.
- 4d *implication.* A lower NCR with no MTD is how the APT attacker model behaves in MTDSim, so §6.2 compares each attacker's NCR reduction against its own NCR with no MTD.

### 22.6 Process (the ch5 pipeline, adapted)

1. **Rule** Q21–Q25 below, and ratify the spine (22.4). Nothing is drafted before the spine is agreed: ch5's lesson.
2. **Draft one paragraph at a time against its slots**, in the mode Marc picks (Q25). Each paragraph passes the gate before Marc sees it.
3. **Gate** on every sentence:
   - ch5 §5 items 1, 2, 5 and 7 (at most three clauses; the subject leads; nouns from 22.1 only; no fact twice);
   - the replay test (if a sentence reads straight off a ch5 float with no explanation, cut it to the back-reference);
   - the reference rule (a float reference where a number is read; a section reference only for a term the reader may not hold; never one after a re-explanation, so cut the re-explanation);
   - voice.md §(f).
4. **Cold readers on the PDF**, run together: a CS student (could they say each paragraph's takeaway in one line?) and an examiner (does each claim stand on a float?). Verify the findings, triage them, and hand them to Marc.
5. **Knock-ons** in the same commit as the redraft:
   - §6.3's two "tactic durations" causes become the unmapped tactics;
   - §6.3's "assumed" for pace is checked against Appendix B's *rule*;
   - §6.3's random-partition sentence points back to §6.1, if Q23 is yes;
   - the preamble's §6.1 sentence;
   - §6.4's two back-references are re-checked.
   - Build clean.

### 22.7 Questions (recommendation first)

- **Q21.** Structure 22.3: outcome split into ¶1–¶3 by cause, with a four-sentence close that sums and implies. *Recommend yes.*
- **Q22.** The opener names the three properties as those on which Table 6.1 marks the two attackers differently. It points at the table and scores nothing, so Q7 holds. *Recommend yes:* it is the section's reason to exist, stated once.
- **Q23.** The random-partition result (§5.4) goes into ¶1 as its outcome sentence and answers ¶1's bound; §6.3 points back. This crosses the "ablations are §6.3's evidence" rule. *Recommend yes,* because the job differs: §6.1 uses it to explain a §5.2 difference, while §6.3 uses it to answer the sub-questions.
- **Q24.** IDS is first expanded inside Table 3.2. Expand it at the first prose use instead: the §3.3.1 Jalowski sentence ("… to stay hidden from an intrusion detection system (IDS)"). This is a ch3 change. *Recommend yes.*
- **Q25.** Drafting mode. (a) Marc dictates each slot, as in ch5; or (b) the session drafts one paragraph against its slots, gated, and Marc edits only the flagged sentences. *Recommend (b) for the opener and the close,* where connective prose is green-lit, *and (a) for ¶1–¶3,* where the argument is his.

## 23. §6.1 v4 drafted, cold-read, revised (2026-10-12)

Marc ruled Q21, Q22 and Q24 yes and Q23 yes. On Q25: "you draft, I want to see it … put in the hard work … get it very close", then he gives feedback paragraph by paragraph. v4 was drafted against the §22 slots and gated. Two cold readers then read the rendered PDF text only: a fourth-year CS student and an examiner. Their findings were verified against the tex and the floats and triaged. v4 is in the tex, about 830 words (v3 was about 1 000).

### 23.1 What the cold reads changed (verified; each overturns part of the §22 plan on merit)

1. **Openings "made of edges the attack flows took" was false** for c3 and c4. Their token leaves Reconnaissance only through the pre-intrusion overlay (§4.3, "three immediate transitions that none of their attack flows draws"). Now "follows edges the attack flows drew, apart from the pre-intrusion overlay". The failure matrix's reweighting is named in the mechanism sentence.
2. **The first cause is "its tactic durations" again, not "its unmapped tactics"** (partly reverses Q6's term).
   - §6.5 names the causes "the tactic durations and order, which no run separates".
   - §4.4.2 and §6.5 say NCR rests most on the 45 s mean duration, most likely through Command and Control, a mapped tactic.
   - Naming only the unmapped tactics misattributed outcome.
   - The opener now says that most of the time goes to the unmapped tactics, which keeps Q6's point, and hedges with "likely … although no run separates the two (§6.5)".
   - §6.3 and the preamble are kept on "tactic durations"; the first-pass edits to "unmapped tactics" were reverted.
3. **Runs end at the first target host compromised** (§6.5, Table 5.1). The baseline attacker's NCR stops short in 656 runs. "By the 15 000 s time limit" and "fewer attack actions in that time" are gone.
4. **Q23 reversed: the random-partition result is out of ¶1.** Three reasons:
   - it holds averaged over c1–c4, and c1 lies below all ten of its random groups (Table G.8);
   - it works through the small groups (G.7, "a hypothesis … not part of the main argument");
   - the attack profiles compromise *fewer* hosts than the attack graph.
   §6.3 keeps it with its hypothesis.
5. **Objective-specific behaviour is now tested against Table 3.2's *techniques* and Appendix B's *assumed* cell.**
   - The attack profiles enter different tactics after the foothold.
   - Their mapped tactics show as the six attack actions in different shares.
   - The techniques that steal data or impede a system are represented only by the time each tactic takes.
   - The Credential Access example is now the range across all four profiles (1 to 10 %). c1 against c3 was a cherry-pick, since c4 is also 10 %.
6. **"Rates" is used only for attack rate**; the share of steps is "shares". "The order of its tactics" is now defined once, in the opener (picked in each run from the attack profile's base weights, §4.3).
7. **"Hides" is gone.** §4.4.1 says "Stealth has nothing to hide from". The close of ¶3 is now "its detection avoidance is time spent without an attack action". "Low and slow" is scoped: "in the only sense MTDSim can test: more slowly than the baseline attacker (Appendix B)".
8. **The attack-rate counterfactual is attributed as G.3 words it:** recomputed from the recorded runs; "about the baseline attacker's" (1.60–2.16 against 1.71). Attack confidentiality is reported as ordering the attackers the same way, with no cause attached, since excluding failed attack actions also raises it.
9. **The close's so-what was a post-hoc reason for NCR reduction**, which §4.5.3 fixes and §6.5 already bounds (each ranking over the attacker's own NCR). It is replaced by the sum: the parts that give the three properties also lower ASP and NCR, so ASP and NCR read alone would rate it the weaker attacker (§6.4's contract).
10. **MTTC is now "close to the baseline attacker's but over different runs".** c3 overlaps (9 700 ± 900 s against 9 100 ± 200 s).
11. **Smaller fixes:** base weights cited to §4.3; "whereas" for "where"; "the state that the attack action before it leaves behind" (it was a garden path); "three over eight" dropped, since the student could not read it off the log axis; the second-half sentence restructured.

**Kept against a reader:**
- *G.1's "likely because both compromise hosts through the same attack actions"*: Marc's Q5 reading, and compatible with G.1's network reading.
- *The forward reference to Table 6.1*: Q22.
- *The baseline-attacker sentence in ¶1*: it is the contrast the section is named for.

**Left for §6.3's redraft (the examiner's viva question):** neither the tactic durations nor the order was removed in a run. "Is the APT attacker model the baseline attacker made slower, plus a precondition penalty?" §6.5 owns the bound and names the future-work run (the baseline attacker given the APT attacker model's tactic durations). §6.3 should answer it directly. The weighted-draw-as-choice question is already §6.3's (stochastic FSM).

### 23.2 Other edits applied
- §3.3.2 (Q24): IDS expanded at its first prose use ("an intrusion detection system (IDS)"). It was first expanded only inside Table 3.2. Jalowski's sentence was not used, because his words are "remain in the shadows", not IDS.
- §6.3: "The pace is assumed … as Kim et al.'s evasion is assumed" became "set by its declared tactic durations … a rule, and measured by proxy (§4.5.1)". Appendix B types APT row 5 as *rule*, Kim's as *assumed*.
- Preamble: §6.1's sentence names the three properties and the two causes.
- Appendix G.2: Table 3.2 defines the properties "in techniques, which MTDSim carries out as its attack actions"; "hold in the unit of the definitions" became "hold when counted in attack actions".

Build clean: 120 pages, 0 undefined, 14 overfull (unchanged).

### 23.3 Flagged, not touched
- §6.2 says "holds an attacker back" (Marc dislikes "held back").
- §6.4 says "a quiet attacker" ("quiet" is not a ch2–5 term).

## 24. Paragraph-by-paragraph rounds on v4 (Marc 2026-10-12)

Marc rules each paragraph in turn. This section logs each round: what he flagged, what was checked, the edit, and any standing advice for the rest of Chapter 6. Edit only the flagged sentences ([[feedback_redraft_edit_dont_rewrite]]).

### 24.1 Opener, round 1

**What Marc flagged:**
1. "the three properties on which Table 6.1 marks the two attackers differently". This points forward to the marks. It reads as though the mark came first and the evidence was joined to it afterwards.
2. The outcome sentence should say plainly that this is attack outcome.
3. "no run separates the two" is vague. Say what can and cannot be said.
4. "Most of the time its tactic durations take falls in its unmapped tactics …" repeats what the opener already said. "take" and "falls" are the wrong verbs, since the unmapped tactics *consume* the time.
5. "so neither explains them". Explains what?

**Checked:**
- Table 6.1 sits in §6.3, which marks the properties from §6.1's evidence. A pointer from §6.1 to the marks therefore turns the argument around. Q22 is reversed.
- §4.5.2 is headed "Attack outcome", so the term is ch4's.
- §6.5 says the comparison "does not show which of the model's parts causes the change". So the true statement is that no run removes either cause.
- Marc's 26–47 % is the step share of unmapped tactics (Figure 5.1(a), the All unmapped row: 36/37/47/26). The time share is 34–57 % (Appendix G.3). ¶3 already carries the time share ("a third to over half of its run"), so cutting the definition sentence loses nothing.
- §5.4 measured NCR only (Table 5.4). It also shows that the failure matrix changes where the attacker goes after a failed Initial Access (back to Reconnaissance 0.76–0.83 with the failure matrix, 0.08–0.10 without). That is part of choice of attack strategy. "Neither explains them", read as all the differences, was therefore **false**. The claim is now limited to NCR.

**Edit (applied):**
> The APT attacker model differs from the baseline attacker with no MTD on objective-specific behaviour, choice of attack strategy and detection avoidance (Section 5.2). In attack outcome, it also reaches a target host in fewer runs and compromises fewer hosts (Table 5.2). Its tactic durations and the order of its tactics likely explain most of these differences, but no run removes either to test this (Section 6.5). Removing the failure matrix or the vulnerability memory changes its NCR negligibly (Section 5.4), so neither explains its lower NCR.

**Advice for the rest of Chapter 6:**
- (a) §6.1–§6.2 are evidence and §6.3 scores it. Never point from the evidence to the marks.
- (b) A pronoun at the end of a paragraph ("them") must name its referent when two plural nouns precede it.
- (c) Scope a negative claim to what was measured.
- (d) A hedge says what was not done ("no run removes either"), not an abstraction ("separates").
- (e) An opener names each cause once. The definition and the evidence go in the paragraph that uses them.

### 24.2 The tactic-durations ablation, run (Marc 2026-10-12)

**Why.** The opener said the tactic durations and the order of its tactics "likely explain most of these differences, but no run removes either". Marc: "why do we not run these?" The order of its tactics is the Petri net, so removing it leaves the baseline attacker, which is already run. The tactic durations can be removed through the `dwell_catalogue` override, with no new code. Marc approved both arms. This is registry F13, the control all six cold examiners asked for, run the other way round and with no MTD only.

**Design.** `data/results/ch6_further_analyses/run_duration_ablation.py` and `analyse_duration_ablation.py` → `duration_ablation_numbers.json`.
- **Pins** are the reported corpus's: v2_partial, v4_failure_only, retrace on, targeted, 15 000 s, no MTD, vulnerability memory rate 2, seeds 0–999, c1–c4.
- **Arm A:** the seven unmapped tactics take no time (mean 0, an immediate transition).
- **Arm B:** Arm A, plus each mapped tactic's mean set to the baseline attacker's mean time for the attack action it dispatches. Each mapped tactic dispatches exactly one attack action under v2_partial. The times, taken from f7 of the baseline's own records:
  - SCAN_HOST, ENUM_HOST and SCAN_NEIGHBOR: 5 s;
  - SCAN_PORT: 25 s;
  - EXPLOIT_VULN: 7.47 s;
  - BRUTE_FORCE: 20 s (the APT attacker model's Credential Access is 4.5 s, so this one is slower).
- **Checked:**
  - On the movement arm, the tactic's draw *is* the attack action's time. The attacker.py docstring (S3-R) says so, and every reported action-bearing record has end − start − dwell = 0.
  - The centre (the declared catalogue, passed explicitly) is bit-identical to runs_reported.jsonl on 80 runs.
  - 8 000 runs, 0 errors, 0 event-cap hits, 932 s.
- The baseline attacker is not re-run, because it consumes no tactic duration.

**Results.** Means; intervals are 95 % paired bootstrap over seeds. "Gap closed" = (arm − reported) / (baseline − reported). The baseline attacker: ASP 0.656, NCR 0.497, attack rate 1.71, attack confidentiality 0.822, MTTC 9 098 s (656 runs).

| | ASP reported / A / B | ASP gap closed A; B | NCR reported / A / B | NCR gap closed A; B | attack rate reported / A / B | blocked share reported / A / B |
|---|---|---|---|---|---|---|
| c1 | 0.124 / 0.403 / 0.630 | 0.52 [0.48, 0.57]; 0.95 [0.90, 1.01] | 0.149 / 0.261 / 0.348 | 0.32; 0.57 | 1.09 / 2.15 / 4.59 | 0.14 / 0.15 / 0.19 |
| c2 | 0.139 / 0.440 / 0.706 | 0.58 [0.53, 0.63]; 1.10 [1.05, 1.14] | 0.209 / 0.354 / 0.447 | 0.50; 0.83 | 0.89 / 1.81 / 4.05 | 0.27 / 0.27 / 0.28 |
| c3 | 0.056 / 0.078 / 0.078 | 0.04 [0.02, 0.05]; 0.04 [0.02, 0.05] | 0.172 / 0.202 / 0.202 | 0.09; 0.09 | 0.68 / 1.26 / 2.18 | 0.30 / 0.45 / 0.53 |
| c4 | 0.042 / 0.100 / 0.374 | 0.09 [0.07, 0.12]; 0.54 [0.50, 0.58] | 0.154 / 0.220 / 0.384 | 0.19; 0.67 | 1.23 / 1.83 / 4.06 | 0.28 / 0.29 / 0.31 |

- MTTC at B: 5 910 (c1), 6 185 (c2), 2 476 (c3), 8 992 (c4), against the baseline attacker's 9 098.
- Attack confidentiality at B: 0.32–0.56, against the baseline attacker's 0.82.
- Distinct openings over eight steps are unchanged in every arm. A zero-time draw consumes no random number, and the routing stream is separate.

**What it shows.**
1. **c1 and c2 (26 of 38 attack flows).** The tactic durations explain the whole gap in ASP. At the baseline attacker's pace they reach a target host as often as it does (c1) or more often (c2). The time in unmapped tactics alone closes about half.
2. **c4.** Pace closes about half of the gap in ASP. The other half comes from something else.
3. **c3.** Pace closes almost none of the gap, and its runs stall rather than run out of time:
   - the same 78 seeds succeed in A and B, and they include all 56 reported successes;
   - at B, the last successful exploit falls at a median of 2 069 s, and the run goes on to 15 000 s;
   - the second half of a run at B is mostly unmapped tactics, attack actions blocked for missing preconditions (Discovery, Lateral Movement, Privilege Escalation, Execution), and scans of neighbours that find none fresh;
   - its blocked share rises with pace (0.30, then 0.45, then 0.53).

   The order of its tactics stalls c3.
4. **NCR closes less than ASP** in every arm. A faster run reaches a target host sooner and stops there, so NCR stops short. The baseline attacker's NCR also stops short in its 656 runs. NCR's gap closed is therefore a lower bound on what pace explains.
5. **At the baseline attacker's pace, the APT attacker model acts faster than it** (attack rate 4.1–4.6 against 1.71), and is flagged more (attack confidentiality 0.32–0.38 against 0.82). The baseline attacker's EXPLOIT_VULN rows on one host count as one action, and its procedure spends time between actions. So per-action times alone do not set its attack rate.
6. **Appendix G.3's recomputation is now a run.** G.3 recomputed attack rate with no time in unmapped tactics as 1.60–2.16. Arm A measures 1.26–2.15. c3 comes out lower than its recomputation, because its blocked share rises once its unmapped tactics take no time.

**Consequences for the prose (proposals; nothing applied yet, Marc to see the numbers first):**
- **Opener:** "likely explain most …, but no run removes either" becomes the measured statement. Removing the tactic durations brings c1 and c2 to the baseline attacker's ASP, c4 halfway, and c3 not at all, because the order of its tactics stalls it.
- **¶3:** the sentence recomputing attack rate from the records becomes the run.
- **Close (¶4):** the attribution becomes the measurement, and the "most likely through Command and Control (45 s)" sentence may be superseded.
- **§6.3:** the examiner's question ("the baseline attacker made slower plus a precondition penalty?"), answered for no MTD. For c1 and c2, its lower ASP is pace. For c3 and c4, the order of its tactics adds a stall.
- **§6.5:** the comparison with MTD still does not separate the parts. This run is no MTD only.
- **Appendix:** a new further-analyses section beside G.3 (one table), or G.3 extended.
- **Registry F13:** marked partly run in the tex comment block.

### 24.3 The run integrated; "pace" retired (Marc 2026-10-12)

**What Marc said:**
- Keep the per-profile nuance out of the body: "that's not the focus of this. This is the APT attacker model versus the baseline". The appendix entry carries it, and the body cites it.
- "I hate the word pace … reads as rhetorical … be more specific". The term is *tactic durations*.
- Once "pace" was gone, the body was inconsistent. It said one cause was tested and the other untested, but named the tested one differently. Say plainly which cause was removed in a run and which was not.

**Applied (ch6 and the appendix, under the standing permission):**
- **Opener.** It names both causes, then says which was run.
  - "Appendix G.3 runs the APT attacker model with the baseline attacker's times: its unmapped tactics take no time, and each mapped tactic takes the baseline attacker's mean time for the attack action it dispatches. It then closes about two thirds of its gap in ASP to the baseline attacker. No run removes the order of its tactics, which most likely accounts for the rest."
  - "The baseline attacker's times" is defined there once and repeated verbatim in ¶3, §6.5 and G.3.
- **Two thirds:** the four attack profiles pooled, each weighted equally and paired by seed. ASP goes from 0.090 to 0.447 against the baseline attacker's 0.656, which is 0.63 [0.61, 0.65] of the gap. The JSON stores it as `pooled.baseline_pace`.
- **¶3.**
  - "Its pace is set by its tactic durations" became "Its tactic durations make it slower".
  - The records-recomputation sentence became the run: "With the baseline attacker's times, its attack rate rises above the baseline attacker's, and its attack confidentiality falls below it". It now comes after the ordering sentence.
- **Close.** The first two sentences ("most likely also explain … lower its attack rate … makes some fail") became one sentence: "The APT attacker model's tactic durations lower its ASP and NCR by lowering its attack rate, and the order of its tactics most likely lowers them by making some of its attack actions fail (Appendix G.3)." The 45 s sentence and the rest are kept, since Marc has not yet read this paragraph.
- **§6.3.**
  - "The pace is set by its declared tactic durations" became "Its declared tactic durations make it slower".
  - "which set the pace behind detection avoidance in part" became "which give it the part of detection avoidance it has".
- **§6.4:** "differ in pace and success" became "differ in attack rate and ASP".
- **§6.5.**
  - "through pace and a declared IDS rule" became "through how often an attacker acts and a declared IDS rule".
  - "which no run separates" became "which no run with MTD separates".
  - The future-work sentence now reports the run with no MTD and leaves the run with MTD as future work.
- **Appendix G.3.**
  - Heading: "The APT attacker model's tactic durations".
  - Paragraph 1: the record shares, with the failed attack actions counted.
  - Paragraphs 2 and 3: the runs, pooled first and then per attack profile, with c3's stall and NCR stopping short.
  - Table G.5 lost the two recomputed columns that the runs replace.
  - Table G.6 is new and generated (tools/further_analyses_tables.py, `t_durations`). Its rows with the tactic durations as declared reproduce Table 5.2 exactly.
- **Reader:** the successful seeds nest in every attack profile (as declared ⊂ unmapped tactics take no time ⊂ the baseline attacker's times). The appendix says so.

**Proposed, not applied (ch3, ch4, ch7 need Marc):**
- ch4 opener (l.3895): "Detection avoidance rests on a pace assumed to hide the attacker" becomes "Detection avoidance rests on tactic durations that make it slower than the baseline attacker". This also drops "hide", which contradicts §4.4.1.
- §4.4.2 (l.4903): "They set the APT attacker model's pace, and the longer a tactic runs …" becomes "They set how long the APT attacker model takes between attack actions, and the longer a tactic runs …".
- §4.5.1 (l.5422): "measure it by proxy, through the attacker's pace" becomes "measure it by proxy, through how often the attacker acts".
- §7.2 (l.9840): "The baseline attacker given the APT attacker model's tactic durations, and a Petri net with uniform weights, to separate pace, order and the weights from CTI" becomes "The APT attacker model with the baseline attacker's times under MTD (Appendix G.3 runs it with no MTD), and a Petri net with uniform weights, to separate the tactic durations, the order of its tactics and the weights from CTI".

**Advice for the rest of Chapter 6:**
- (f) No word stands in for a defined term. "Pace" was a session coinage for the tactic durations, and it made one cause read as two.
- (g) When one cause is tested and another is not, name both in the same terms and say which was run.

**Applied after Marc's "all good" (2026-10-12):** the four ch4 and ch7 proposals above. One differs from the proposal. In §4.4.2, "how long the APT attacker model takes between attack actions" became "how often the APT attacker model acts". A mapped tactic's duration is its attack action's own time, not time between attack actions, so the proposed wording was inaccurate. The new wording also matches §4.5.1's "how often the attacker acts". "Pace" no longer appears anywhere in the thesis prose.

### 24.4 Opener, round 2: the run's setup moved to G.3 (Marc 2026-10-12)

**What Marc said:**
- The run's detail dominated the opener. Is it argument, or can it live in the appendix?
- "which no run removes" is redundant with "most likely". You cannot remove the order: the APT attacker model with its Petri net disconnected is no model at all, and the baseline attacker is already the run without it.
- Marc's framing: the timeline the APT attacker model produces at runtime answers three questions. *What*: the tactics, in their order. *How*: the tactic-to-action mapping to the attack actions. *When*: the tactic durations. The two causes are the *what* and the *when*. The *how* is shared with the baseline attacker.

**Applied:**
> Its tactic durations and the order of its tactics explain these differences. With the baseline attacker's times in place of its tactic durations, it closes about two thirds of its gap in ASP (Appendix G.3), and the order of its tactics most likely accounts for the rest.

- The definition of the baseline attacker's times now lives only in G.3, which already carried it. The name describes itself.
- "most likely" covers the order of its tactics, which can only be read by subtraction. It also covers the failure matrix and the vulnerability memory, which §5.4 measured on NCR only, and which the next sentence handles.

**Advice for the rest of Chapter 6:**
- (h) In the body, give an analysis's result and its share. The setup goes in the appendix entry the body cites.
- (i) One hedge per claim. A "which no run removes" clause beside "most likely" says the same thing twice.

### 24.5 ¶1 (objective-specific behaviour), rounds 1–3 (Marc 2026-10-12)

**Round 1, the critique of v4 on disk.** The paragraph never said what the APT attacker model does against the definition:
- S1 restated §5.2 with the hedge first.
- The lead evidence (Figure 5.1(a), Credential Access 1–10 %) was whole-run tactic steps, while the definition reads after the foothold, in techniques.
- S3 re-explained §4.4.1 in five clauses.
- "represented only by the time" was roundabout.
- The baseline sentence carried §3.3.2 detail.

**Round 2.** Marc's flags:
- the property was de-emphasised;
- "foothold", "shares" and "objective" were never made concrete;
- *why* no attack action carries out an objective was missing;
- why was the headline evidence (G.2) in the appendix?
- "sets these shares" was opaque;
- "the definition's own examples" was vacuous;
- the separate baseline sentence was vacuous.

The fix: name the property first; give the reason (MTDSim's six attack actions only find and compromise hosts, §2.2.3); lead with Figure 5.1(a)'s rows.

**Round 3.** Marc asked why it still read as muddled.
- **It rebuilt a frame the reader already has.** §4.5.1 already bridges the definition to the runs: "the attack profiles … should divide their steps among the tactics differently, most of all in actions on objectives … the metric tests whether their runs still differ in MTDSim". The paragraph now answers that question.
- **Percentages read as hand-picked** without that frame. With it, the Exfiltration and Impact rows *are* the prediction, so the paragraph names the pattern (which attack profiles enter which tactic), not numbers.
- **"Its runs reach the tactics of that objective" got the split wrong.** §4.2 split the attack flows by what the attacker did. The tactics follow from the attack flows.
- **The tactic-step evidence and the after-foothold attack-action evidence read as one claim twice.** G.2 left the body, and Appendix B's row 2 now cites G.2 directly.

**Applied** (Marc: "a lot stronger … 90 % of the way there … polishing around the edges"):
> On objective-specific behaviour, the attack profiles' runs still differ in MTDSim, most of all in actions on objectives (Figure 5.1(a)): Exfiltration occurs only in c1 and c3, Impact almost only in c2 and c3, and neither in c4. Each attack profile follows the order of tactics of its own attack flows (Section 4.2), and the failure matrix's reweighting does not erase it. Actions on objectives are unmapped tactics, because MTDSim's six attack actions, the baseline attacker's procedure, only find and compromise hosts (Section 2.2.3), so the APT attacker model steals no data and impedes no system. Outside actions on objectives, c4, whose attack flows share no objective, also divides its steps differently from the others, so there the differences are not shown to come from the objective.

- **Figure 5.1(a)'s rows:** Exfiltration c1 6, c2 –, c3 4, c4 –; Impact c1 <1, c2 8, c3 12, c4 –.
- **Marc on "does not erase it":** right. The failure matrix reroutes after a failure, and the order of its tactics survives.
- **Inbound references checked:**
  - §6.3's "same six attack actions at different rates" cites Figure 5.1(a) and still holds.
  - Appendix B row 2 cited §6.1 for that claim, which §6.1 no longer makes. It now cites Appendix G.2.

**Advice for the rest of Chapter 6:**
- (j) A discussion paragraph answers the question its metric's paragraph in §4.5 posed, in that paragraph's words. Do not rebuild the bridge from Table 3.2.
- (k) Numbers without the frame that makes them the test read as hand-picked. Name the pattern the figure shows instead.
- (l) Tight is not clear. Each abstract noun ("shares", "objective", "sets") must have its referent in the paragraph or in the reader's scaffold.
- (m) Give the reason behind a negative claim in one clause, here what MTDSim's attack actions do.

### 24.6 ¶1's c4 bound tested against the random partitions (Marc 2026-10-12)

**Ruled and applied:** "and the failure matrix's reweighting does not erase it" cut (Marc: "cut the clause … beautiful"). The ablations already show the failure matrix changes NCR negligibly (§5.4).

**Marc's reading of the c4 sentence:** the differences outside actions on objectives "may not come from the objective, might just be the partitioning", and ten random partitions were run. Until now the random partitions had been read on ASP and NCR only.

**Test** (`data/results/ch6_further_analyses/partition_step_divergence.py` → `partition_step_divergence_numbers.json`). It reads the partition-control runs: no MTD, 1 000 seeds, the same pins as the reported corpus (v2_partial, failure-only overlay, retrace on, targeted, 15 000 s, memory rate 2). The five partitions replaced on 2026-10-07 come from the redraw stream: 20 000 + 20 000 runs. For each group, relative tactic occurrence (§4.5.1) is pooled over its runs. Between two groups the measure is the share of steps lying in different tactics (total variation distance). It covers the six pairs of each partition's four groups, against the attack profiles' six pairs from `runs_reported.jsonl`.

| | Attack profiles, mean of 6 pairs | Ten random partitions, mean per partition | At or above the attack profiles |
|---|---|---|---|
| Outside actions on objectives | 0.25 | 0.25 to 0.42 | 9 of 10 |
| All tactics | 0.30 | 0.27 to 0.45 | 8 of 10 |

- **Marc's reading holds.** Outside actions on objectives, any grouping of the 38 attack flows into groups of 19, 7, 7 and 5 differs as much as the attack profiles do. c4 is not the evidence; the random partitions are.
- **Over all tactics the magnitude is not objective-specific either.** What follows the objective is *which* actions on objectives occur:
  - The attack profiles lack Exfiltration (c2, c4) or Impact (c1 0.17 %, c4) exactly as their objectives say: three of four groups.
  - Random groups also lack one by chance (Exfiltration below 0.5 % in 8 of 40, Impact in 11 of 40, both in 3), one or two groups per partition, with no pattern.
  - The pattern holds by construction (§4.2 split the attack flows by what the attacker did). The run test is that MTDSim keeps it, which is §4.5.1's question.
- **How it fits §5.4 / Table F.4 / G.7 (outcome; not overstated).** With no MTD the attack profiles compromise more than all ten random partitions (NCR 0.171 against 0.097–0.157; d 0.25 to 1.47, all not negligible). That claim is about outcome and stands.
  - Combined with today's result: the attack profiles differ from each other *less* than most random groups yet compromise *more*.
  - This fits G.7's mechanism: small random groups lose chains of tactics to a target host, while grouping by objective keeps them. The structure shows as kept chains, not as distinct attack profiles. It remains a hypothesis.
- **A step division has no negligible band.** Total variation distance is descriptive, not an effect size, so don't say "negligible" for it (Marc asked whether it "lives within a negligible range"). Say "within the range random grouping produces".

**Proposed, awaiting Marc:**
1. ¶1 last sentence (replaces the c4 argument): "Random groups of the same sizes divide their steps as differently (Appendix G.7), so only which actions on objectives each attack profile takes is shown to follow its objective."
2. G.7: one paragraph with the two rows above and the absence counts.
3. §6.5 (when reached): "likely because attack flows with one objective share more of their moves than a random group does" reads as a behaviour claim that today's measure bears on. Bound it to G.7's mechanism (keeping the chains that lead to a compromise).

**Marc's takeaway, checked** ("objective-filtered behaviour … shares the same chains … less variance across profiles than random partitioning").
- *Supported:* grouping by objective compromises more than random grouping (outcome).
- *Not supported:* "less variance". The attack profiles are second-lowest of 11 groupings, which chance gives about one time in five. Nor "share the same chains": a share of steps does not see order, and attack flows that were more alike would make the groups *more* distinct than random ones, not less.
- *The two-part takeaway:* outcome, grouping by objective compromises more; behaviour, outside actions on objectives grouping by objective divides steps like random grouping.

**New gate rule** (Marc 2026-10-12): text downstream of the paragraph being redrafted changes automatically; text upstream, and the paragraph itself, is presented first.

**Applied downstream:**
- §6.2 fidelity paragraph: "likely because attack flows with one objective share more of their moves than a random group does" → "likely because a small random group can lose the chains of tactics that lead to a compromise (Appendix G.7)".
- §6.2 SQ1/SQ2 answer: "They differ most in actions on objectives, which are unmapped, so in MTDSim an objective shows only in how an attack profile spends its steps" → "In behaviour they differ only in which actions on objectives they take, which are unmapped".
- G.7: a second paragraph with the step-division result, the absence counts, and the bound (the chains are an order of tactics, which a share of steps does not measure).
- Build clean, 121 pages.

**¶1, presented:** only the last sentence changes; see the reply of 2026-10-12. Outcome stays out of ¶1.

**Advice:**
- (n) Before a sentence explains a difference by a grouping, check the difference against random groupings of the same sizes. A single odd group (c4) is not a control.
- (o) Keep outcome claims (NCR, with effect sizes and a negligible band) apart from behaviour-divergence claims (descriptive, compared to a chance range). One does not license the other.

### 24.7 ¶1, round 4: the bound against random groups, and a clarity pass (Marc 2026-10-12, "approved")

- **S2 stays as it was.** Marc: a proposed rewording ("the pattern is the one their attack flows show, because…") made the same point twice. "By construction" is already in the scaffold: §4.5.1 says "The attack profiles were built to differ, so the metric tests whether their runs still differ in MTDSim".
- **S4 is the bound against random groups.** It names the measure in §4.5.1's words and gives "the objective" its referent: "an attack profile's objective".
- **S3 is fixed and moved last.**
  - Actions on objectives is a stage, not tactics, so the sentence names Collection, Exfiltration and Impact (§5.3's phrase).
  - "The baseline attacker's procedure" is cut.
  - The paragraph now ends on what the objective-specific tactics do in MTDSim: nothing.

**Applied:**
> On objective-specific behaviour, the attack profiles' runs still differ in MTDSim, most of all in actions on objectives (Figure 5.1(a)): Exfiltration occurs only in c1 and c3, Impact almost only in c2 and c3, and neither in c4. Each attack profile follows the order of tactics of its own attack flows (Section 4.2). Before actions on objectives, the attack profiles divide their steps among the tactics no more differently than groups of the same sizes drawn at random from the attack flows (Appendix G.7), so an attack profile's objective shows only in actions on objectives. Collection, Exfiltration and Impact, the tactics of actions on objectives, are unmapped, because MTDSim's six attack actions only find and compromise hosts (Section 2.2.3), so the APT attacker model steals no data and impedes no system.

**Advice:**
- (p) Before proposing a sentence that states a cause or a construction, check whether the scaffold (§4.5's paragraph for the metric) already says it. If it does, the sentence repeats it.
- (q) Name the measure in a comparison whose appendix holds more than one measure. "Differ" alone lets outcome and behaviour blur.
- (r) A stage (actions on objectives) is not a set of tactics. Name the tactics when the claim is about tactics.

### 24.8 ¶2 (choice of attack strategy), round 1 (Marc 2026-10-12)

**Critique of the on-disk ¶2 (8 sentences):**
- It opened on the mechanism, not on §4.5.1's answer.
- It rebuilt §4.4: decision places, base weights, the failure matrix. §6.2 credits choice to the Petri net drawing from the attack flows, and the failure matrix belongs to adaptivity.
- It compared unlike lengths ("hundreds over eight" against "one over its first four").
- The overlay exception and the implication sentence repeated or over-qualified.

**My first redraft; Marc's response:**
- "does not take the same first steps in every run" restated a defined term. Use distinct openings itself.
- The G.2 attack-action recount is a nuance the discussion does not need, and it hid the baseline attacker's 3.
- "Draws", "ignores" and "leaves behind" are rhetorical or unclear.
- The catch was said twice.
- "Boil it down to what the discussion needs", then Marc left the call to me.

**Applied** (4 → 3 sentences; the overlay, G.2, the mechanics and the implication cut):
> On choice of attack strategy, the attack profiles' 1 000 runs have 179 to 947 distinct openings over eight steps, and the baseline attacker's 3 (Figure 5.1(b)). In each run, the Petri net picks the next tactic at random, in proportion to how often the attack profile's attack flows took that step, whereas the baseline attacker's procedure fixes the order of its attack actions (Figure 4.1). The order of its tactics can dispatch an attack action whose preconditions are missing (Section 4.3.x, runtime mechanics; ch4 gives the example, an exploit of a vulnerability not yet scanned for), and 15 to 30 % of the attack profiles' attack actions fail this way (Appendix G.3).

- **Numbers:** `numbers_reported.json` core.table distinct_openings "8": c1 947, c2 748, c3 179, c4 662; baseline 3.
- **Precondition example:** ch4 gives it already, so ¶2 cites ch4 rather than repeating it.

**Advice:**
- (s) Never paraphrase a defined metric ("does not take the same first steps"). Say the metric's name and its number.
- (t) Plain verbs for a mechanism: "picks at random, in proportion to", not "draws". A verb that personifies a weight ("ignores") or a state ("leaves behind") is rhetoric.
- (u) A catch is said once. Give its reason by pointing to where ch4 defined it.

### 24.9 ¶2, round 2 (Marc 2026-10-12, "a lot clearer … 90 % of the way")

- **"Step" was the wrong word.** Marc asked whether it should be the Petri net's term. "Step" is §4.5.1's unit of a *run* (an opening is a run's first k steps), so using it for the attack flows overloaded it. The Petri net's terms are now used: the edge's base weight (Equation base-weight, ch4 §4.3: "the share of the attack profile's attack flows leaving p that go to q"). Marc: "that's the equation".
- **Scope.** The base weights alone hold only after a success. After a failure the failure matrix rescales them (Equation routing), so one clause says so (advice c). Cut it only if Marc rules the nuance off.
- **The catch names the mapping.** The order of tactics fails attack actions only through the tactic-to-action mapping (Marc: "because of the fact … of this mapping"). "Its" is resolved to "the APT attacker model's" (advice b), since the sentence before has two subjects. The 15–30 % stays: Marc says it "hits harder".

**Applied:**
> On choice of attack strategy, the attack profiles' 1 000 runs have 179 to 947 distinct openings over eight steps, and the baseline attacker's 3 (Figure 5.1(b)). In each run, the Petri net picks the next tactic at random, in proportion to its edge's base weight (Equation 4.x), which the failure matrix rescales after a failure (Equation 4.y), whereas the baseline attacker's procedure fixes the order of its attack actions (Figure 4.1). Through the tactic-to-action mapping, the order of the APT attacker model's tactics can dispatch an attack action whose preconditions are missing (Section 4.3.x), and 15 to 30 % of the attack profiles' attack actions fail this way (Appendix G.3).

**Advice:**
- (v) Describe a component in the terms that formalise it (Petri net: edge, base weight, transition, and its equation). Never borrow a word that is already a metric's unit elsewhere ("step").

### 24.10 ¶2, round 3, and its clarity check (Marc 2026-10-12)

- **The failure-matrix clause moves into the citation.** Marc: it "breaks up the clarity", so "hide it in the hedging". "In proportion to its edge's base weight (Eq. 4.2), which the failure matrix rescales after a failure (Eq. 4.4)" becomes "in proportion to the weight of the edge to it (Equations 4.2 and 4.4)". "Weight", not "base weight", is true before and after a failure, and the two equations carry the difference. "The edge to it" also gives "its" a referent.

**Clarity check (terms, noun clusters, nuance, hedging, relevance):**
- **S1, result.** Every term is defined: choice of attack strategy (Table 6.1), distinct openings (§4.5.1), a step (a run's unit), the attack profiles, the baseline attacker. One comparison, on one length. Nothing missing, nothing extra.
- **S2, cause.** In ch4's terms: the Petri net, edge, weight, and the equations; the baseline attacker's procedure (ch2/ch4). The contrast says what differs: picked at random against fixed. Hedging: none needed, because it describes the model.
- **S3, catch.**
  - The defined term from the opener: "the order of its tactics", here naming the APT attacker model. It names the mapping, which is the route of the failure.
  - "Can" scopes it.
  - "This way" points to "preconditions are missing".
  - The number is Appendix G.3's.
  - One open point: "the order … can dispatch" gives a dispatching verb to an order. Proposed: "can put an attack action before its preconditions are met" (the verb of an order). Awaiting Marc.
- **Cut, and staying cut:** the decision-place mechanics, the failure matrix by name, the overlay, the G.2 recount, the implication sentence.
- **Relevance:** S3 is the mechanism the opener names for "the order of its tactics most likely lowers [ASP and NCR] by making some of its attack actions fail".

**Advice:**
- (w) A nuance that qualifies a term can live in the term's choice ("weight" rather than "base weight") and its citation, not in a clause.

### 24.11 ¶2, round 4 (Marc 2026-10-12)

- "in proportion to the weight of the edge to it" → "in proportion to the edge weights". Marc: too many filler words.
- "can dispatch an attack action whose preconditions are missing" → "can run an attack action before its preconditions are met". Marc: "I don't like the word dispatch … remove it", so ¶2 now uses an order's verb.
- **"Dispatch" elsewhere.** It is ch4's verb for what a tactic does with its attack action (ll. 4397, 4877, 5374), and ch6 uses it at 8634, 9269 and 9333 plus in Appendix G. It was not touched beyond ¶2; asked Marc whether to retire it wider (ch4 would be a proposal).

**¶2 as applied:**
> On choice of attack strategy, the attack profiles' 1 000 runs have 179 to 947 distinct openings over eight steps, and the baseline attacker's 3 (Figure 5.1(b)). In each run, the Petri net picks the next tactic at random, in proportion to the edge weights (Equations 4.2 and 4.4), whereas the baseline attacker's procedure fixes the order of its attack actions (Figure 4.1). Through the tactic-to-action mapping, the order of the APT attacker model's tactics can run an attack action before its preconditions are met (Section 4.3), and 15 to 30 % of the attack profiles' attack actions fail this way (Appendix G.3).

### 24.12 "Dispatch" retired dissertation-wide (Marc 2026-10-12, "please fix ch4 verb thanks")

"Dispatch" (a tactic dispatches its attack action) → "run". The change covers:
- ch4 (ll. 4397, 4877);
- §4.5.1 (5374);
- Figure 5.1's caption;
- §5.3;
- ch6 (8637, 9272, 9336);
- Appendix B and the Appendix G entries (G.3 twice, Figure G.x's caption).

The generator `tools/further_analyses_tables.py` is fixed and regenerated:
- Table G.4's column "Dispatched" → "All";
- Table G.5's caption.

Only the intended lines changed. Data keys (`dispatched|4`) are left alone. No "dispatch" is left in the prose.

### 24.13 ¶3 (detection avoidance), rounds 1–3 (Marc 2026-10-12, v3 "yes")

**Critique of the on-disk ¶3 (8 sentences):**
- It rebuilt §4.5.1's proxy bridge and pointed to the marking appendix (a, j).
- The result had no numbers and came late.
- A four-profile correlation was superseded by the run.
- The confidentiality ordering was implied by the scaffold.
- The close was too narrow: "time spent without an attack action" leaves out the mapped tactics. Their durations slow it too, and c3 stays below the baseline attacker's attack rate at arm A.

**Marc on v1:**
- "Their tactic durations make them slower": whose? Now the APT attacker model, the opener's owner.
- "With the baseline attacker's times, their attack rate rises above the baseline attacker's" read as the baseline against the baseline. Now "in place of its tactic durations", with numbers on both sides.
- Marc was unsure which way confidentiality moves. Acting faster puts more attack actions five or more within 60 s, so more are flagged and confidentiality falls. The numbers now carry the direction.
- The IDS rule is tautological: a slower attacker passes it. §4.5.1 already says both metrics measure "how often the attacker acts", so ¶3 does not repeat it.

**Marc on v2:**
- The IDS sentence was clause on clause. Now one clause in a CS student's terms: "MTDSim has no IDS, so the APT attacker model cannot choose techniques an IDS does not flag."
- Order kept: result → cause → test → the half not met → summary.

**Final clarity pass:**
- **Numbers checked** against Table 5.2 and `duration_ablation_numbers.json`: 0.680–1.228 / 1.709; 89.4–98.1 / 82.2; 2.18–4.59; 32.1–56.0.
- **Every term is defined:**
  - detection avoidance (Table 6.1);
  - attack rate and its unit, and attack confidentiality (§4.5.1);
  - tactic durations, and "the baseline attacker's times" (opener, G.3);
  - unmapped (§4.4.1);
  - Stealth and Defense Impairment (ch4 spelling).
- **Pronouns:** "it" and "its" all point to the APT attacker model.
- **One fix:** "the tactics *of* avoiding detection" → "*for* avoiding detection".
- **No rhetorical words.** "Slower" is the definition's own word.

**Applied:**
> On detection avoidance, the attack profiles have a lower attack rate than the baseline attacker, 0.68 to 1.23 attack actions per minute against 1.71, and a higher attack confidentiality, 89 to 98 % against 82 % (Table 5.2). The APT attacker model's tactic durations make it slower. With the baseline attacker's times in place of its tactic durations, it takes 2.18 to 4.59 attack actions per minute, more than the baseline attacker, and its attack confidentiality falls to 32 to 56 %, below the baseline attacker's (Appendix G.3). MTDSim has no IDS, so the APT attacker model cannot choose techniques an IDS does not flag. Stealth and Defense Impairment, the tactics for avoiding detection, are unmapped, so in MTDSim its detection avoidance comes only from its tactic durations.

**Advice:**
- (x) In a comparison against a run that borrows the comparator's values, name what was replaced ("in place of its tactic durations") and give both sides' numbers. Otherwise it reads as the comparator against itself.
- (y) Use the reader's plainest fact ("MTDSim has no IDS") rather than the procedure that follows from it ("applied to its runs after they end").
- (z) A close that names a mechanism must cover all of it. Use the defined term for the cause, not one part of it.

### 24.14 The §6.1 close, rounds 1–3 (Marc 2026-10-12, "keep it as drafted")

**Critique of the on-disk close (7 sentences, ~170 words):**
- C1 repeated the opener.
- C2 (45 s via Command and Control's scan neighbours) duplicated §6.5.
- C3 (succeeds on the same networks, G.1) is a separate finding, about networks.
- C4 (MTTC over different runs) is shown by Table 5.2's run counts.
- C5 (a longer run untested) is in ch7.
- Only C6 (the parts that give its properties also lower ASP and NCR, so they would rate it weaker) said something new.

**Rounds:**
- **v1** ("the parts … give these three properties … read alone, would rate it the weaker attacker"). Marc: rhetorical, "the parts" vague.
- **v2** (one plain sentence, the reading consequence left to §6.2). Marc: oversteered. It lost the takeaway, so it failed purpose, context, audience and relevance.
- **v3, first form** ("With no MTD … reaches a target host in fewer runs … the same causes that give it detection avoidance and choice … although its behaviour is closer to an APT's"). Marc:
  - "With no MTD" is the opener's scope already.
  - Use the metrics' names.
  - The property list is a cliché and names only two of the three.
  - "Closer to an APT" is true by construction, so it is no news.
- **Diagnosis:**
  - The news is that the same causes produce both results, so the outcome metrics alone penalise the behaviour being modelled.
  - The order of tactics also gives objective-specific behaviour (¶1: each attack profile follows its own attack flows' order), so "three properties" is right and needs no list.

**Applied:**
> The APT attacker model's three properties and its lower ASP and NCR have the same two causes: its tactic durations and the order of its tactics. ASP and NCR alone therefore rate it the weaker attacker for behaving more like an APT.

- **Hedge.** The order's "most likely" is the opener's. The close gathers it up and does not repeat it, because inline it would also hedge the order's certain role in the properties.
- **Scope (Marc: "putting ASP and NCR on notice?").** No, not as metrics for MTD evaluation:
  - they measure what an MTD reduces;
  - the MTD section uses NCR reduction, which is relative to each attacker's own NCR with no MTD.

  They are not a yardstick of fidelity, which §6.2 already says ("an attacker that compromises more is stronger, not closer to an APT attacker"). Nor do they show that real APTs are weaker: part of the gap is where the model meets MTDSim's attack actions (§6.5).

**Logged for §6.3 (Implications), new claim, needs Marc's ruling when reached:**
- An evaluator who picks the attacker that compromises most, as a worst case, would pick the less APT-like one.
- The choice changes conclusions, not just levels: ρ between the two attackers' MTD rankings lies between −0.24 and 0.25.

**Advice:**
- (aa) A close says the one thing the paragraphs do not say together. Find the joint (here: same causes, both results), not a summary.
- (bb) A contrast true by construction ("although it is closer to an APT") is no news. Look for the dependence instead ("for behaving more like an APT").
- (cc) A close in a section that has fixed its scope does not restate it ("with no MTD"), and uses the metrics' names.


## 25. §6.2 (APT attacker model versus MTD): critique of the overdraft, and the plan (2026-10-12; nothing applied to the tex)

Marc: §6.2 reads as "dot points concatenated", with no opener, a closer almost as big as the opener, rhetorical flourish throughout, and "a page of words" after the first sentence. He asked whether §6.1's lessons carry over. He also noted that §6.1 went through two redrafts: first a logical rearrangement with minimal cuts, then the cut-down rounds. He asked whether §6.1 is missing its tie to the sub-questions.

### 25.1 Measured

- §6.2: **1 426 words** in five paragraphs (425 / 367 / 141 / 344 / 148). §6.1 is 521.
- Chapter 6: 6 321 words against the ~3 300 target (preamble 141, §6.3 1 290, §6.4 1 147, §6.5 1 796).
- §6.2 holds the main result, so it can be longer than §6.1. **Budget: ~700–750 words.**

### 25.2 Marc's critique, checked: it holds on every count

1. **No opener.** P1 is the opener, the mechanism, the attack profiles, a literature comparison and a bound, fused into 425 words. Its finding (S2–S3) is right but buried.
2. **The close repeats the opener.** "To SQ3, then" restates P1 S2–S3 with Table E.1's numbers. Only the Chapter 1 tie (the advantage of time) is new. That fails (aa): a close says the one thing the paragraphs do not say together.
3. **One mechanism, said twice.** "The baseline attacker restarts … the APT attacker model waits for Lateral Movement" is in P1 (S9–S10) and again in P2 (S4–S6). The "why" (P1) also comes before its evidence (P2, disruption per deployment).
4. **The order breaks the preamble's promise.** The preamble says §6.1 and §6.2 "follow Chapter 5's order". §5.3 runs disruption per MTD deployment → MTD ranking → by attack profile. §6.2 runs ranking + mechanism + attack profiles → disruption → interval → MTDShield.
5. **The cause is never named, so it is never handed back.** §6.1's lesson (21.3 point 1) applies directly, and here it is the missing throughline. Each mechanism §6.2 gives is one of §6.1's two causes meeting MTDSim's deployment rules, which are written for the baseline attacker's procedure (§2.2.3: what a deployment disrupts, and where it sends the attacker):
   - "blocked less, because an unmapped tactic runs no attack action" = **its tactic durations**;
   - "the service layer catches it less: it runs scans, exploits and brute force between unmapped tactics" = **its tactic durations**;
   - "regains its place only when its Petri net next reaches Lateral Movement" = **the order of its tactics**.

   §6.2 can name the two causes verbatim, as §6.1 does. That is the chapter's coherence.
6. **Rhetorical and stand-in words** ((f), (l), (t)):
   - "holds an attacker back" ×6 (Marc's ruling: *disrupts*);
   - "currency", "they part", "catches", "move together", "separates", "the far end of the same mechanism", "the split runs by layer", "the direction runs the other way";
   - "takes a different state from each attacker", "pulls the mean below zero", "hand the attacker easier vulnerabilities", "pure loss", "its line … sits below it".
7. **Replays of Chapter 5** (the 21.6 replay test). Much of P2 is §5.3.1 sentence for sentence: every host-layer deployment blocks it; 204 to 232 s forward. P4 restates §5.3.2's numbers and Appendix D's shares.
8. **Bounds that belong to §6.5** (memory: bounds once, in §6.5):
   - P3: "MTDSim charges a deployment nothing" (also in §6.4 l.9225 and §6.5 l.9276);
   - P4: "run as released, outside its training conditions" (§6.5 l.9450), the no-cost point again, and "a strategy learned against the APT attacker model … not built" (ch7 future work);
   - P1: "MTDSim's implementation of it, on its default network".
9. **Hedges stack** ((i)). There are five session hypotheses, each with its own hedge:
   - "most likely" (failed attack actions);
   - "likely" (c3 at the far end);
   - "possibly" (OS diversity);
   - "likely" (recovery time);
   - "suggests" (MTDShield fitted).

   Two are untraced: c3 and OS diversity.
10. **Side topics that are not SQ3:**
    - port shuffle sharing rank 1 ("does not rank shuffling against diversity");
    - c3 from 500 s (a per-profile nuance; Marc ruled per-profile nuance out of the §6.1 body);
    - OS diversity's negative time lost;
    - the Cho comparison, which is a literature tie and fits §6.4, where §6.4 l.9110–9114 already generalises "optimal for one attacker model".

### 25.3 Marc's side question: is §6.1 missing its tie to the sub-questions?

**No. By design, §6.1 answers no sub-question.**
- The preamble allocates the answers: §6.1 explains the no-MTD differences, §6.2 answers SQ3, §6.3 answers SQ1 and SQ2. Chapter 7 draws them into the research question.
- §6.1 is evidence. Pointing from it to an answer reverses the argument, the same fault as pointing to the marks ((a)).

**What does need tying is §6.1 → §6.2, through the causes:**
- §6.1's close ("ASP and NCR alone rate it the weaker attacker") is why §6.2 reads NCR reduction, which is relative to each attacker's own NCR with no MTD. The §6.2 opener can rest on that rather than re-explain it.
- §6.2 hands back §6.1's two causes verbatim (25.2 point 5).

The current close's Chapter 1 tie (the advantage of time, \citep{ghosh2009nitrd}) is the ch1–ch6–ch7 link for SQ3. Keep it.

### 25.4 The spine (one takeaway per paragraph, in §5.3's order)

| ¶ | Takeaway | Cause (§6.1's words) | Evidence | Words |
|---|---|---|---|---|
| Opener | In MTDSim, the host layer disrupts the APT attacker model most and the service layer the baseline attacker most. No MTD mechanism or deployment strategy ranks first against both. MTDSim writes what a deployment disrupts, and where it sends the attacker, for the baseline attacker's procedure. The APT attacker model meets those rules through its tactic durations and the order of its tactics | both, named once | §5.3.2, §2.2.3 | ~100 |
| 1 Disruption per MTD deployment (attack actions blocked; time lost, adaptivity) | A deployment blocks the baseline attacker more often under every layer. The APT attacker model loses time to the host layer, the baseline attacker to service diversity | tactic durations: an unmapped tactic runs no attack action, so a deployment then blocks none (by construction, one clause). Order of its tactics: after a host-layer deployment the baseline attacker's procedure restarts by scanning for hosts, while the APT attacker model regains its place only when its Petri net next reaches Lateral Movement | Fig. aio-adaptivity, App. fa-foothold, fa-traced-run | ~170 |
| 2 MTD ranking (NCR reduction, deployment interval) | The layers rank in opposite order for the two attackers at every deployment interval; ρ −0.24 to 0.25. The host layer keeps half or more of the APT attacker model's NCR off up to 1 000 s; the service layer never does | ¶1 carried to hosts compromised (one sentence); the interval, hedged once (recovery time); user shuffle's rule, one sentence (§6.4 l.9179 cites §6.2 for it) | Fig./Tab. eff-cross-arm, eff-interval-values | ~150 |
| 3 Deployment strategies (MTDShield) | MTDShield, trained against the baseline attacker, chooses service diversity at 70 % or more against either attacker, and beats random over the same four MTD mechanisms against the baseline attacker alone. Its zero inputs mean this run cannot tell a fitted policy from a fixed preference | the attacker model it was trained against | Fig. eff-cross-arm(e), App. mtdshield-observed, mtdshield-limitations | ~120 |
| 4 By attack profile | At 50–200 s the four attack profiles' NCR reductions lie close together and apart from the baseline attacker's, so the attacker model matters more than the attack profile. This is consistent with §6.1: an objective shows only in actions on objectives, which are unmapped | — | Fig. eff-suppression-profiles | ~70 |
| Close (SQ3) | The answer: MTD performs differently against the APT attacker model, by MTD layer, because of how its two causes meet MTDSim's deployment rules. Chapter 1's advantage of time: against the slower APT attacker model, the host layer keeps its effect at deployment intervals ten times longer | — | — | ~90 |

**Inbound contracts to keep** (later text that cites §6.2):
- §6.4 l.9114: what each deployment takes is written against the baseline attacker's procedure.
- §6.4 l.9145: MTDShield chooses service diversity at 70 % or more, and beats random against the baseline attacker alone.
- §6.4 l.9182: user shuffle, the rule MTDSim gives it.
- §6.4 l.9205: the baseline attacker's mean time lost to the host layer is below zero.
- §6.4 l.9228: the service layer never halves the APT attacker model's NCR.
- §6.5 l.9276: Lateral Movement.
- §6.5 l.9395: the first deployment is where the baseline attacker's time lost falls below zero.
- §6.5 l.9453: MTDShield runs outside its training conditions.
- Appendices fa-foothold, fa-accounts, fa-traced-run.

**Cut, and where each lives:**
- the port-shuffle rank aside (nowhere, or §6.5);
- the Cho comparison (to §6.4);
- c3 from 500 s (cut; untraced);
- the OS-diversity hypothesis (cut; untraced);
- the two MTDShield bounds and no-cost (§6.5);
- "a strategy learned against the APT attacker model" (ch7 future work);
- the SQ answer's Table E.1 numbers (Table E.1).

**One fact to check before drafting:** why service diversity costs the APT attacker model little (60 s against 493 s). "Vulnerabilities are the baseline attacker's currency" is a metaphor with no measurement behind it. Either trace it (lower attack rate, so a redraw rarely lands on an exploit in progress?) or state only the result.

### 25.5 Process: §6.1's two stages, kept

1. **Stage 1, logical redraft.** Rearrange to the spine with minimal rewording. Cut only the items above that live elsewhere. Apply the mechanical voice fixes ("holds back" → "disrupts"). Expected ~850–950 words.
2. **Stage 2, paragraph rounds.** Marc rules each paragraph in turn: critique, propose, clarity pass, apply, build, log, commit.

**Advice carried from §6.1:**
- (a) no pointer to the marks;
- (e) the opener names each cause once;
- (f)/(l) no stand-in words;
- (i) one hedge per claim;
- (j) answer the question §4.5 posed (here SQ3, as §4.5's opener poses it);
- (k) give numbers with their frame;
- (aa) the close says the joint;
- the replay test;
- one fact, one home.


## 26. §6.2 stage 1: the logical redraft, applied (Marc 2026-10-12, "happy with that … put in the hard work")

**Applied to the tex** (spine 25.4, cuts 25.4, mechanical fixes 25.2 point 6). 1 426 → ~900 words:

| Paragraph | Words |
|---|---|
| opener | 95 |
| disruption per MTD deployment | 258 |
| MTD ranking | 178 |
| deployment strategies (MTDShield) | 183 |
| by attack profile | 80 |
| SQ3 answer | 109 |

The overdraft is in git at 7fd1b08f.

**The throughline.** The opener names §6.1's two causes verbatim, and ¶1 hands each back:
- **tactic durations:** an unmapped tactic runs no attack action, so a deployment then blocks none;
- **the order of its tactics:** it decides when the Petri net next reaches Lateral Movement.

The close answers SQ3 through the same two causes.

**Checks made while drafting:**
- **"Disrupts most" was false for the baseline attacker** if read as attack actions blocked: the host layer blocks it 1.0 per deployment, against 0.95 for the service layer. The opener and close therefore say NCR reduction, the ranking's metric. "Disrupts" keeps ch2's sense (interrupting an attack action).
- **Time lost under the host layer is not attributed to the order alone.** The order decides *when* the Petri net reaches Lateral Movement, and the 242–324 s is stated as a result. The time between is tactic durations too (memory: measurement vs attribution).
- **Service diversity ranks 4th against the APT attacker model at 200 s** (Table 5.3), so the Cho sentence moved to §6.4 says "at 200 s".
- **Inbound contracts** (25.4) all still hold in the new text, apart from §6.5 l.9453 (below).

**Downstream (auto):**
- **§6.4 P1:** the Cho comparison, one sentence, after the dwell-robustness sentence: "At 200 s, service diversity ranks first against the faster baseline attacker and fourth against the APT attacker model, the reverse of the case Section 3.2.1 cited …".
- **§6.5:** "MTDShield runs as released, outside its training conditions" now cites Appendix D.4, which lists the training conditions, instead of §6.2, which no longer states them.

**Small cuts beyond 25.4** (listed in the tex comment):
- the within-layer match of the blocked bars (MTDSim's rule, §2.2.3);
- MTDShield's "does nothing at most of the rest" and its line below service diversity's (Figure 5.3 detail);
- "under MTDShield all four attack profiles sit below the baseline attacker".

**Flags for Marc's weeding:**
1. The SQ3 sentence opens the section, as §6.3's does. Keep it, or open on the finding.
2. The layer ranking is in the opener and again as ¶2's first sentence, and the interval facts are in ¶2 and again as a ratio in the close.
3. ¶4's "which fits Section 6.1" is the session's inference.
4. Service diversity's 60 s against 493 s is stated, not explained (no traced cause).
5. ¶1 is the longest paragraph (258 words), with blocks, host layer, restart and service diversity. It is the candidate to split or weed first.

Build clean, 120 pages.


## 27. §6.2 opener: scrutiny (Marc 2026-10-12, "don't redraft yet"; nothing applied to the tex)

Marc's read: the opener leads with the SQ3 question, not the finding; "the host layers … the service layers the baseline" is unclear; "MTDSim writes … where it sends the attacker against the baseline procedure" is rhetorical flourish; the last line quotes §6.1. He asked what the opener is for, which nuance it needs, which the reader already holds, and whether §6.1's opener lessons (§9, §24.1, §24.4) carry over.

### 27.1 What the opener is for (one line)

**Answer SQ3 with the section's finding (the host layer reduces the APT attacker model's NCR more than the service layer, and the service layer the baseline attacker's, at every deployment interval), and name §6.1's two causes as its likely explanation.** Everything else is a paragraph's job or lives elsewhere.

### 27.2 What the reader already holds when they reach it

| Fact | Already given |
|---|---|
| SQ3's question | Ch1 (l.374); §4.5's opener, **word for word the same sentence** (l.5290); ch5's opener; the ch6 preamble ("§6.2 … answers SQ3") |
| Every claim is about MTDSim | ch6 preamble ("Every claim is about MTDSim") |
| §6.2 explains why a different MTD layer reduces each attacker's NCR most | ch6 preamble |
| What a deployment disrupts and where it sends the attacker; "loses only its place" | §2.2.3, Figure 2.2's dashed arrows |
| The APT attacker model shares the attack actions; the Petri net picks the next tactic | ch4 opener; §6.1 ¶2 ("whereas the baseline attacker's procedure fixes the order of its attack actions") |
| A deployment during an unmapped tactic cuts its duration short and costs the penalty, but blocks no attack action and never changes the next tactic | §4.4.1 (l.4877); §4.4.2 ("the longer a tactic runs, the more likely an MTD deployment disrupts it") |
| The two causes, by name | §6.1's opener and its close, the paragraph just read |
| No MTD mechanism or deployment strategy ranks first against both; ρ | §5.3.2's lead; and again in §6.4's opener (l.9050), with ρ |

So the opener needs none of S1, S3 or the first half of S4. The only new things it can give are the finding at the level of the MTD layer and the claim that the two causes explain it.

### 27.3 Sentence by sentence

- **S1, "SQ3 asks how MTD performs …".** Not needed in this form. It is the fourth telling of the question and a verbatim repeat of §4.5's opening sentence. It puts the question before the finding (important point first fails). The section must still tie to SQ3 (Marc), but by *answering* it, not by asking it again (27.5 Q1).
- **S2, "In MTDSim, the host-layer mechanisms reduce … most, and the service-layer mechanisms the baseline attacker's; no MTD mechanism or deployment strategy ranks first against both (Section 5.3.2)."** This is the finding, and it should lead, but:
  - "In MTDSim": the preamble covers it, and §6.1's opener does not say it.
  - "the host-layer mechanisms … the service-layer mechanisms": true only as **layer means** (the line Figure 5.3 plots). Per mechanism it fails for the baseline attacker: OS diversity ties IP shuffle at rank 2 at 200 s (0.68 each), and from 500 s IP shuffle beats it (0.39 against 0.04, Table F.0a). Use "the host layer" and "the service layer", Figure 5.3's terms.
  - "most" has no frame (at what interval, against what?). The data support "more than the service layer, at every deployment interval" for the APT attacker model, and the reverse for the baseline attacker (Table F.0a, layer means at all six intervals).
  - Gapping ("and the service-layer mechanisms the baseline attacker's") leaves the reader to supply the verb and the noun. This is the "not clear" Marc heard.
  - "no MTD mechanism or deployment strategy ranks first against both": for mechanisms, it follows from the layer clause; it is §5.3.2's lead, and §6.4 opens on it with ρ as the point that transfers. One fact, one home: §6.4. (Inbound: Chapter 7's draftnotes cite §6.2 for it; repoint to §6.4 when Chapter 7 is reached, gated.)
  - The pointer is a Section, not the float that shows the layer lines (lesson 8): Figure 5.3.
- **S3, "MTDSim writes what a deployment disrupts, and where it sends the attacker, against the baseline attacker's procedure (Section 2.2.3)."** Not needed here.
  - "writes … against" is a stand-in verb (flourish), and the key phrase comes last after two embedded clauses (sentence weights 2 and 3).
  - Content: the rules are §2.2.3's. ¶1 shows how each cause meets them and cites §2.2.3. The point that the answer rests on those rules is a bound, already in §6.4 (l.9060, "the ranking moves because MTDSim writes what each deployment takes against the baseline attacker's procedure", same flourish), in §6.5, and in §6.2's own close. Four homes.
- **S4, "The APT attacker model runs the same attack actions without that procedure, so these rules act on it through its tactic durations and the order of its tactics (Section 6.1)."**
  - First half: already given (ch4, §6.1 ¶2).
  - "act on it through": abstract verb chain; it says the causes matter without saying how (¶1's job).
  - **No hedge on an inferred claim.** The Appendix G.3 run has no MTD (the baseline attacker's times were tested only with no MTD), so no run under MTD removes either cause. That the causes explain the ranking is inference and takes one "likely" (lesson 7; Chapter 7's draftnotes already say "which no run separates").
  - The handback is right (the throughline Marc approved); the gloss around it is what quotes §6.1. Name the two causes verbatim, as §6.1's opener does, and stop.

### 27.4 §6.1's lessons, checked against this opener

| Lesson | Here |
|---|---|
| §9.2 one message in the first sentence | **fails**: S1 is the question |
| §9.3 open on the reader's term | partly: "host-layer mechanisms" for Figure 5.3's "host layer" |
| §9.4 sort every sentence | S1, S3 and half of S4 live elsewhere (27.2) |
| §9.5 bounds once, in §6.5 | **fails**: S3 is the rules bound, also in §6.4, §6.5 and the close |
| §9.6 no stand-in words | **fails**: "writes … against", "act on it through" |
| §9.7 hedge inside the inferred claim | **fails**: S4 |
| §9.8 floats next to the claim | **fails**: points to a Section, not Figure 5.3 |
| (e) opener names each cause once; mechanism goes in the paragraph that uses it | **fails**: S3–S4 carry mechanism that ¶1 repeats |
| §24.4 the run's setup in the appendix; result and share in the body | n/a (no run under MTD) |
| (aa) the close says the joint | **fails, as a knock-on**: the close opens "To SQ3, then: … MTD performs differently … the difference follows the MTD layer, because … tactic durations and the order of its tactics": S2 and S4 again. Marc's overdraft critique ("a closer almost as big as the opener") still holds after stage 1 |

§6.1's opener worked because it was finding (with its float) → causes named → evidence share. §6.2's has the question first, then the finding, then two sentences of mechanism that ¶1 gives again.

### 27.5 The fix, as structure (no prose yet)

Two slots, about 45 words in place of 95:

1. **Answer (SQ3, tagged once).** Job: answer SQ3 with the finding. Facts: the host layer reduces the APT attacker model's NCR more than the service layer, and the service layer the baseline attacker's more than the host layer, at every deployment interval. Float: Figure 5.3. Ceiling: one sentence, no numbers (¶2 has them), no gapping, no "In MTDSim".
2. **Cause.** Job: hand §6.1's two causes back. Facts: its tactic durations and the order of its tactics, verbatim, with one "likely". Ceiling: one short sentence; no rules, no procedure, no pointer back to §6.1.

**Questions (recommendation first):**
- **Q1, the SQ3 tie.** (Recommended) **Answer first, tagged.** The first sentence is the answer and names SQ3 as what it answers. Then the close drops its restatement and keeps only what the paragraphs do not say together: Chapter 1's advantage of time and the interval ratio. Otherwise, (b) keep the question as S1 (the fourth telling, and §4.5's sentence verbatim), or (c) no tag in the opener, leaving the close as the answer (the opener–close repeat stays). Whatever is ruled applies to §6.3's opener too, which also opens on the question (gate: downstream, so it changes after this ruling).
- **Q2, "no MTD mechanism or deployment strategy ranks first against both".** (Recommended) Cut from the opener. It lives in §5.3.2, and §6.4 opens on it as the point that transfers.
- **Q3, the rules nuance.** (Recommended) It lives in ¶1 (per cause, citing §2.2.3) and §6.5 (bound). The close's last sentence and §6.4's "writes … against" are reviewed when those are reached.

**Knock-ons once ruled (downstream, automatic):**
- ¶2's first sentence restates the layer claim; ¶2 opens on its numbers instead.
- Appendix F (fa-foothold) says "§6.2 explains why the host layer disrupts the APT attacker model most"; keep, or align with the opener's NCR wording.
- §6.3's opener, under Q1.

### 27.6 Rulings and what was applied (Marc 2026-10-12, "the fixed structure … let's get that done")

**Rulings:**
- **Q1, answer first.** Answer the question in its own terms. SQ3 was phrased so its clauses can be answered directly, and the answer is specific.
- **Q2, cut** the no-rank-first phrase. Marc: vague language, needs to be specific.
- **Q3, accepted.** Downstream changes are automatic.

**Opener (95 → 52 words):**
> In answer to SQ3, the host layer reduces the APT attacker model's NCR more than the service layer does at every deployment interval, and the service layer reduces the baseline attacker's NCR more than the host layer does (Figure 5.3). The APT attacker model's tactic durations and the order of its tactics likely explain the difference.

- The cause sentence names the APT attacker model rather than "its". The sentence before ends on the baseline attacker, so "its" would point at the wrong attacker (advice (b)).
- "Explain the difference" means the contrast S1 states.

**Downstream (automatic):**
- **¶2 S1** no longer restates the layer claim. It now opens on ρ ("at every deployment interval", Table 5.3).
- **The close** loses its first sentence ("To SQ3, then: … the difference follows the MTD layer, because …"). It now opens on Chapter 1's advantage of time. Its last sentence, "Each part of this answer rests on MTDSim's rules …", is left for the close's round (Q3).
- **§6.3's opener**, under Q1. Before: "SQ1 and SQ2 ask how … ; the eight properties score the answer. Scored by the rule of Chapter 3, …". Now: "In answer to SQ1 and SQ2, scored by the rule of Chapter 3, the APT attacker model has …". Only the tag was swapped. The specific answer in the question's terms is §6.3's own round.

**Proposed, gated (Chapter 7):** the draftnotes cite §6.2 for "no MTD mechanism ranks first against both". Repoint them to §5.3.2 or §6.4.

**Advice for the rest of Chapter 6:**
- (ab) A section that answers a sub-question opens on the answer, in the question's own terms and with the specific measure, and tags the sub-question once. Never re-ask the question: §4.5 and Chapter 5 already did.
- (ac) A layer claim uses the figure's layer term ("the host layer", the mean the figure plots). Check per-mechanism truth before writing "the host-layer mechanisms".

Build clean, 120 pages, 0 undefined.

### 27.7 Opener round 2, the clarity pass (Marc 2026-10-12, "apply that")

**Applied:**
- "at every deployment interval" moved to the front of the sentence, so it covers both clauses.
- "the difference" became "the difference between the two attackers". S1 holds two gaps, the host layer against the service layer within each attacker, and the layer order between the two attackers. The causes explain the second.

**Checked:**
- "Host layer" and "service layer" are defined in emphasis in §2.2.1.
- "Deployment interval" is defined in emphasis in §2.2.2.
- Figure 5.3's caption calls each layer line the mean over its mechanisms.

**Advice:**
- (ad) When a cause sentence follows a sentence holding two comparisons, name which one the cause explains.

## 28. §6.2 ¶2 (disruption per MTD deployment): scrutiny (Marc 2026-10-12, "look at paragraph two"; nothing applied)

Paragraph two counts the opener as paragraph one: "On disruption per MTD deployment …", 258 words, 13 sentences.

### 28.1 What it is for (one line)

**Show how each of the two causes meets MTDSim's deployment rules, at the level of one deployment.**
- **Tactic durations** lower attack actions blocked per MTD deployment.
- **The order of its tactics** makes the APT attacker model lose time to the host layer, where the baseline attacker loses none.

The ranking in ¶3 then follows. Two further facts are kept only because they are needed:
- the baseline attacker's time lost below zero (§6.5 cites §6.2 for it);
- service diversity, where the baseline attacker loses most.

### 28.2 What the reader already holds (§5.3.1 states most of this paragraph, nearly verbatim)

| ¶2 says | Already given |
|---|---|
| A deployment blocks the baseline attacker more often | §5.3.1's first sentence |
| "The APT attacker model runs no attack action while in an unmapped tactic, so a deployment then blocks none" | §5.3.1, **word for word** (with a §4.3.x pointer); §4.4.1 ("cuts its duration short … never changes which tactic comes next") |
| The two attackers lose time to different MTD mechanisms | §5.3.1's adaptivity lead |
| 242 to 324 s; 493 against 60 s; below zero under every mechanism but service diversity; 204 to 232 s forward | §5.3.1, every number |
| A deployment costs the attacker only its place | §2.2.3 |
| Host layer: back to scanning hosts; service layer: back to scanning ports | §2.2.3, Figure 2.2's dashed arrows |
| Lateral Movement runs enumerate host, the attack action that moves the attacker to its next host | §4.3.x (tactic-to-action mapping, l.4843) |
| A failure caused by MTD routes like any other | §4.4.2 (failure matrix) |

What is **new** in ¶2:
- the attribution of blocks to tactic durations;
- the host-layer recovery contrast (the baseline attacker is sent back to scanning hosts, while the APT attacker model waits for Lateral Movement);
- why the baseline attacker's time lost is below zero (the second attempt);
- why service diversity costs the baseline attacker (erased exploit progress).

The rest is replay.

### 28.3 Sentence by sentence

1. **"On disruption per MTD deployment, a deployment blocks … more often … and the two attackers lose time to different MTD mechanisms (Figure 5.2)."** The scaffold lead is right (§5.3.1's heading). It restates with a back-reference and no numbers, which the rules allow. "Blocks … more often" paraphrases the metric; the defined name is *attack actions blocked per MTD deployment*. **Keep, in the metric's name.**
2. **"The APT attacker model runs no attack action while in an unmapped tactic, so a deployment then blocks none: its tactic durations lower how often MTD blocks it."** The first two clauses are §5.3.1 verbatim. Only the attribution after the colon is new. "Lower how often MTD blocks it" paraphrases the metric again, and "MTD" stands in for "a deployment". **Keep the attribution only, in the metric's name; the mechanism is a pointer.**
3. **"A block ends the attack action as a failure, so what a deployment costs an attacker is what it does next."** The "so" clause is abstract (a flourish). The first half is §4.4.2 (a failure routes like any other); the second restates §4.5's definition of time lost. **Cut.**
4. **"A host-layer deployment costs either attacker its place (Section 2.2.3)."** This is §2.2.3, but it is the premise for the contrast that follows. **Keep as a clause** that opens the contrast.
5. **"The baseline attacker restarts its procedure after a block, whatever its progress \citep{brown2023}, so it scans for hosts again and finds its place at once."**
   - "Restarts its procedure after a block" is **false for the service layer**: there it is sent back to scanning the same host's ports (§2.2.3). The 204–232 s finding below covers both layers, so the wrong verb carries into the second attempt.
   - "whatever its progress" is a clause no later sentence uses.
   - "at once" is vague. §5.3.1 has the number: each later host-layer or port-shuffle deployment costs it 19 to 32 s, the contrast pair to 242–324 s.
   - **Fix:** use §2.2.3's verbs ("sent back to scanning hosts") and give the measured cost.
6. **"The APT attacker model regains its place only when its Petri net next reaches Lateral Movement, which the order of its tactics decides, and until then its attack actions most likely fail for missing preconditions (Appendices F.x, F.y)."** This is the core, and it is new. Two gaps:
   - **why Lateral Movement**: it is the one tactic mapped to enumerate host, the attack action that moves the attacker to a host. The reader holds this from §4.3, but not here, so a pointer to Section 4.3.x is needed, not a sentence;
   - the hedge is right (one traced run, 255 of 363 refused; no aggregate under MTD).

   The strongest measured support is in Appendix F.2, not in the text: under the host layer at 50 to 200 s, 70–89 % of the APT attacker model's runs compromise no host, against 3–20 % of the baseline attacker's. Whether that number belongs in the body is Q3.
7. **"It loses 242 to 324 s per host-layer deployment."** This is a §5.3.1 number. It is the payoff of S6 and the pair to S5's 19–32 s. **Keep only if S5 gets its number.** Otherwise it is a one-sided replay.
8. **"The restart can also help the baseline attacker."** A transition with no content of its own. **Fold into S9.**
9. **"The first deployment lands while it exploits its first host, so the restart gives it a second attempt there and brings its first compromise 204 to 232 s forward (§5.3.1); its time lost is therefore below zero under every MTD mechanism but service diversity."**
   - The mechanism is new, and §6.5 (l.9395) cites §6.2 for it.
   - **"therefore" overclaims for user shuffle.** The 204–232 s is for the host-layer and service-layer mechanisms (§5.3.1). User shuffle disrupts only brute force, so it cannot block the first exploit, yet the baseline attacker's time lost under it is also below zero (−23 s, Table 5.x). **Fix:** scope it to the host and service layers.
   - **A check on the inherited claim:** under complete topology shuffle (−14 s, [−29, 2]) and host topology shuffle (−15 s, [−30, 0]), the confidence interval reaches zero. "Below zero under every MTD mechanism but service diversity" is §5.3.1's sentence (ch5, gated). Flagged, not ours to fix here.
10. **"The APT attacker model gets no second attempt."** A compressed phrase. The reason is ch4's: a block is a failure that its Petri net routes like any other (§4.4.2). **Keep, with the reason in ch4's words or as a pointer.**
11. **"Service diversity costs the baseline attacker 493 s per deployment and the APT attacker model 60 s: it redraws every service, so the baseline attacker loses the vulnerabilities it was exploiting."**
    - The baseline attacker's side is supported by disruption_mechanism.md §1: its exploit progress on the host is erased, and its next compromise comes 2.6× later.
    - The APT attacker model's 60 s is **not explained**. The same audit says the service layer leaves it its position, "it pays only through later exploit outcomes". The cause is untraced (flag 4 from §26).

### 28.4 §6.1's lessons, checked against ¶2

| Lesson | Here |
|---|---|
| Replay test (§21.6) | **fails**: S1, S2 (first half), S7 and S9's numbers are §5.3.1's sentences |
| §9.3 open on the reader's term, metric names verbatim | **partly**: lead ✓; "blocks … more often", "how often MTD blocks it" paraphrase the metric |
| §9.6 no stand-in words | **fails**: "restarts its procedure" (wrong for the service layer), "finds its place at once", "gets no second attempt", "what a deployment costs is what it does next" |
| §9.7 one hedge per inferred claim | ✓ (one "most likely") |
| (c) scope a claim to what was measured | **fails**: "therefore … every MTD mechanism but service diversity" covers user shuffle, which the mechanism does not |
| (k) numbers with their frame | **partly**: 242–324 s has no contrast number for the baseline attacker |
| (e) mechanism in the paragraph that uses it | ✓ (this is that paragraph) |
| §9.4 sort every sentence | S3 nowhere; S8 folds into S9 |

### 28.5 The structure (slots; no prose yet)

Four moves, about 150–170 words:

1. **Lead.** Attack actions blocked per MTD deployment is higher for the baseline attacker under every MTD mechanism, and the two attackers lose time to different MTD mechanisms (Figure 5.2). No numbers.
2. **Tactic durations, blocks.** The attribution only: tactic durations lower the APT attacker model's attack actions blocked per MTD deployment. The mechanism is a pointer to §4.3.x or §5.3.1, not re-said.
3. **The order of its tactics, host-layer time lost.**
   - A host-layer deployment costs either attacker its place (§2.2.3).
   - The baseline attacker is sent back to scanning hosts, and a later deployment costs it 19–32 s.
   - The APT attacker model regains its place only when its Petri net next reaches Lateral Movement, the tactic mapped to enumerate host (§4.3.x), which the order of its tactics decides. Until then its attack actions most likely fail for missing preconditions, and it loses 242–324 s (Appendices F.2, F.4).
4. **Two consequences for the baseline attacker.**
   - The first deployment gives it a second attempt at its first host: 204–232 s forward, so its time lost under the host and service layers is below zero. A block costs the APT attacker model no attempt; its Petri net routes it like any failure (§4.4.2).
   - Service diversity erases its exploit progress: 493 s against 60 s.

**Questions (recommendation first):**
- **Q1, the replay.** (Recommended) Keep only one contrast pair of numbers (19–32 s against 242–324 s). The rest of §5.3.1's numbers (204–232 s, 493/60 s) stay only where a mechanism sentence needs them as its frame. Otherwise, keep every number as now.
- **Q2, split or not.** (Recommended) **Do not split.** After the cuts the paragraph has one job, the two causes at one deployment, at about 160 words. A split would give the blocks a two-sentence paragraph.
- **Q3, the no-foothold share.** (Recommended) **Leave it in Appendix F.2.** The hedge and the appendix pointer carry it; the body has 242–324 s. Otherwise, bring "70–89 % of its runs compromise no host, against 3–20 %" into the body as the measured support for "most likely".
- **Q4, service diversity's 60 s.** (Recommended) **State the baseline attacker's cause only, and keep the APT attacker model's 60 s as the contrast.** Tracing the 60 s is cheap with the movement tracer if Marc wants it explained; the explanation would be a hypothesis until traced. Otherwise, run the trace first, or cut the 60 s.

**Gated (ch5), proposed:** §5.3.1's "below zero under every MTD mechanism but service diversity". The complete topology shuffle and host topology shuffle intervals reach zero, so "at or below zero" is the reading the table licenses.

### 28.6 Rulings, and the ¶2 draft proposed (Marc 2026-10-12, "proposed draft of paragraph two … put in the hard work")

**Rulings:**
- **Bare bones.** No rehash of the evaluation. Repeat a number only if it is a headline number or it advances the point.
- **No split.**
- **The 60 s explained and qualified.** No new runs.
- **"At or below zero" approved for ch5.** Applied to §5.3.1. The same claim in §6.4 ("whose mean time lost to it is at or below zero") was changed downstream, automatically.

**Marc's question: is this adaptivity?** Yes. Time lost per MTD deployment is the adaptivity metric (§4.5), and §5.3.1's second lead reads "On adaptivity". The paragraph's story is adaptivity:
- the APT attacker model loses more time to the host layer (the order of its tactics);
- it loses less to service diversity (its tactic durations, through the blocks).

Attack actions blocked per MTD deployment is the evidence for the second point, not a topic of its own. The lead therefore mirrors §6.1's leads, which open on the property.

**The contrast pair is corrected on merit.** This overturns my own Q1 recommendation:
- 242–324 s is the mean over **all** deployments.
- 19–32 s is the baseline attacker's cost for deployments **after the first** only. As a pair, the two are not like for like.
- The like-for-like contrast is §5.3.1's own: 242–324 s against at or below zero. So 19–32 s is dropped, and the second attempt explains why the baseline attacker's figure is at or below zero.

**Sources for the facts:**
- **Later host-layer deployments, 19–32 s:** the B20 note gives 18.5–32.4 s.
- **The first user-shuffle deployment:** +6.5 s (B20). This confirms that "therefore … every MTD mechanism but service diversity" overclaimed.
- **Every host-layer deployment catches the APT attacker model in something** ("nothing caught" is 0 %). The place is cleared as it is for the baseline attacker, and only Lateral Movement (enumerate host) restores it (disruption_mechanism.md §C (iv)).

**Draft (197 words, from 258; not applied):**

> On adaptivity, the APT attacker model loses more time per MTD deployment than the baseline attacker under the host layer, and less under service diversity (Figure 5.2(b)). A host-layer deployment costs either attacker its place (Section 2.2.3). The baseline attacker is sent back to scanning hosts, and the first deployment even gives it a second attempt at its first host, so its time lost is at or below zero. The APT attacker model regains its place only when its Petri net next reaches Lateral Movement, the tactic mapped to enumerate host (Section 4.3.2); the order of its tactics decides when. Until then its attack actions most likely fail for missing preconditions (Appendices F.2 and F.4), and it loses 242 to 324 s per host-layer deployment. An unmapped tactic runs no attack action, so its tactic durations lower its attack actions blocked per MTD deployment under every MTD mechanism (Figure 5.2(a)): under the service layer, 0.15 against the baseline attacker's 0.95. Service diversity redraws every service, so a block costs an attacker the vulnerabilities it was exploiting: the baseline attacker loses 493 s per deployment, and the APT attacker model, blocked less often, likely loses less, 60 s.

**Cut candidate:** the second-attempt clause (about 25 words). If it goes, §6.5's "that first deployment is where the baseline attacker's time lost falls below zero (Section 6.2)" is repointed to §5.3.1, and the figure's negative bars go unexplained here.

### 28.7 ¶2 v3 critiqued (Marc 2026-10-12), and v4 (proposed, not applied)

**What Marc flagged in v3, checked:**
1. **"More time under the host layer, and less under service diversity" sets a layer against one mechanism.** That holds: across the rest of the service layer the APT attacker model loses *more* than the baseline attacker (port shuffle 26 against −24 s, OS diversity −8 against −58 s). The specific, true lead is §5.3.1's own: the APT attacker model loses time mainly to the host layer (242–324 s), and the baseline attacker only to service diversity (493 s; every other mechanism is at or below zero). With both headline numbers in the lead, nothing is conflated.
2. **"Sent back to scanning hosts" is §2.2.3's own wording.** ✓
3. **The second attempt: on purpose or a bug?** On purpose. Brown's rule restarts the attacker from scanning hosts "regardless of prior progress" (IS-INT-01, -05, -07), and the second attempt follows from that rule. It is classified as conforming (disruption_mechanism.md §F.3), and the APT attacker model does not get it. **Home:** §6.5, which already says the first deployment is where the baseline attacker's time lost falls below zero. That sentence gains the reason in one clause and repoints from §6.2 to §5.3.1 when ¶2 is applied (downstream, automatic). With the new lead ("only to service diversity"), ¶2 makes no claim about the sign, so it needs no second attempt.
4. **The blocks sentence restates by-construction facts.** Kept only as the cause of the 60 s, and limited to the service layer. "Under every MTD mechanism" is cut (§5.3.1 states it).
5. **"A block costs an attacker the vulnerabilities it was exploiting" is a flourish.** Replaced by what happens: the baseline attacker is sent back to scanning the host's ports and starts its exploits on that host again (disruption_mechanism.md §1: its exploit progress on the host is erased).

**Kept or dropped:**

| Detail | Verdict |
|---|---|
| Headline numbers 242–324 s and 493 s | kept, in the lead (they make it specific) |
| Either attacker loses its place | kept (the joint for the host-layer contrast; §2.2.3) |
| Why Lateral Movement (enumerate host) | kept, as a clause with a pointer |
| Missing preconditions, one hedge | kept |
| The second attempt, and the sign of the baseline attacker's time lost | moved to §6.5 |
| 19–32 s, 204–232 s, "under every MTD mechanism" | dropped (§5.3.1) |
| The 60 s cause, one hedge | kept, with 0.15 against 0.95 as its frame |

**v4 (170 words, from 258):**

> On adaptivity, the APT attacker model loses time mainly to the host layer, 242 to 324 s per deployment, and the baseline attacker only to service diversity, 493 s (Figure 5.2(b)). A host-layer deployment costs either attacker its place (Section 2.2.3). The baseline attacker is sent back to scanning hosts and continues its procedure from there. The APT attacker model regains its place only when its Petri net next reaches Lateral Movement, the tactic mapped to enumerate host (Section 4.3.2), and the order of its tactics decides when. Until then its attack actions most likely fail for missing preconditions (Appendices F.2 and F.4). Service diversity redraws every service, so the baseline attacker, sent back to scanning a host's ports, starts its exploits on that host again. The APT attacker model's tactic durations keep it in unmapped tactics, which run no attack action, so its attack actions blocked per service-layer deployment are 0.15, against the baseline attacker's 0.95 (Figure 5.2(a)). Service diversity therefore likely costs it only 60 s.

### 28.8 ¶2 v4 critiqued (Marc 2026-10-12, "the narrative isn't as honest as it can be"), and v5 (proposed, not applied)

**What Marc flagged, checked:**
1. **"Its place" clashes with a Petri net term.** §4.2 defines places ("Tokens sit on places"), and §6.2 used "its place" in the same sentence as "its Petri net". What "place" meant is **the host it was working on**. The code clears that host on a host-layer deployment and keeps it on a service-layer one (disruption_mechanism.md §C (iv)). The source of the clash is ch2 l.957 ("the attacker loses only its place"); §6.4 (l.9221–9223, "its place until its Petri net next reaches Lateral Movement"; "might keep its place") inherits it.
2. **"Sent back to scanning hosts and continues its procedure from there" depends on the layer.** True. The rule sends the baseline attacker back to a different attack action per layer (§2.2.3): scanning hosts, scanning that host's ports, or exploiting. v4 read as though every deployment did the same thing.
3. **"The order of its tactics decides when" + "until then … fail" say one thing in two clauses.** Merged. The cause is now inside the clause ("only when the order of its tactics next brings it to Lateral Movement").
4. **The narrative was not honest about the service layer.** It was not. v4 put the 60 s down to tactic durations alone. The code shows a second cause, as large or larger:
   - the service-layer rule sends the baseline attacker back to scanning that host's ports, where it starts the host's exploits again;
   - the APT attacker model is sent back nowhere, because its Petri net routes the failure like any other (§4.4.2). It keeps the host and the ports it had found, and nothing later fails (disruption_mechanism.md §C (iv)–(v)).

   So the same difference cuts both ways:
   - **Under the host layer**, a fixed return point helps the baseline attacker, and the APT attacker model's lack of one costs it.
   - **Under service diversity**, the fixed return point costs the baseline attacker, and the APT attacker model's carrying on spares it.

   v4's tidy split (host layer = the order of its tactics, service layer = tactic durations) was too neat. Both causes act on the service layer.

**Structure of v5:**
- the lead with both headline numbers;
- the joint (a fixed return point against the Petri net routing a failure like any other);
- then each layer, in parallel: what the deployment takes, then each attacker's response.

**v5 (about 205 words; v4 was 168, and the parallel per-layer structure costs about 35):**

> On adaptivity, the APT attacker model loses time mainly to the host layer, 242 to 324 s per deployment, and the baseline attacker only to service diversity, 493 s (Figure 5.2(b)). MTDSim sends a disrupted baseline attacker back to a fixed attack action of its procedure (Section 2.2.3), whereas the APT attacker model's Petri net routes a failure that a deployment causes like any other (Section 4.4.2). A host-layer deployment costs either attacker the host it was working on. The baseline attacker is sent back to scanning hosts and enumerates one next. The APT attacker model gets a host back only when the order of its tactics next brings it to Lateral Movement, the tactic mapped to enumerate host (Section 4.3.2); until then its attack actions most likely fail for missing preconditions (Appendices F.2 and F.4). A service-layer deployment leaves either attacker its host. The baseline attacker is sent back to scanning that host's ports, and under service diversity, which redraws every service, starts its exploits on that host again. The APT attacker model carries on, and because its tactic durations keep it in unmapped tactics, which run no attack action, its attack actions blocked per service-layer deployment are 0.15 against 0.95 (Figure 5.2(a)); service diversity likely costs it only 60 s.

**Proposed, gated (ch2 l.957):** "the attacker loses only its place" → "the attacker loses only the attack action in progress and, under the host layer, the host it was working on". This takes "place" out of ch2, where it would clash with §4.2's Petri net places. §6.4 l.9221–9223 change downstream, automatically, when §6.4 is reached.

### 28.9 ¶2 v5 critiqued (Marc 2026-10-12), and v6 (proposed, not applied)

**What Marc flagged:**
1. **"Routes a failure like any other" misses the point: it is a forced reroute.** A failed attack action sends the APT attacker model through the failure matrix to another tactic. After a host-layer deployment, each failure moves it again rather than towards Lateral Movement. disruption_mechanism.md §C (iii) supports this: a failure at a post-intrusion tactic keeps the token in its stage, and does not send it towards the tactics that restore its host.
2. **"Leaves either attacker its host" is unclear.** It now reads "changes services, not hosts, so neither attacker loses its host".
3. **Short sentences, per layer:** how it is modelled, what the baseline attacker does, what the APT attacker model does, the result.
4. **Only three of the four numbers were given, and unevenly.** All four are now there, one per attacker per layer:
   - host layer: at or below zero against 242–324 s;
   - service diversity: 493 s against 60 s.
5. **Why is Lateral Movement a big deal and the port scan not?** The honest answer is that it is the same mechanism, a precondition lost until the tactic mapped to the restoring attack action comes up. The difference is *what each layer takes*:
   - the host layer takes the host, which only Lateral Movement (enumerate host) restores;
   - the service layer takes no precondition, because the APT attacker model keeps its host and the ports it found (disruption_mechanism.md §C (iv)). The baseline attacker is not short of a precondition either. MTDSim's rule *forces* it back to scanning ports, and under service diversity its exploits on that host restart.

   So both attackers are force-rerouted: the baseline attacker by MTDSim's rule, the APT attacker model by the failure matrix.

**Accuracy fixes in v6:**
- "So its time lost is at or below zero" lost its "so". The value comes from the first deployment (§6.5), not from the quick return alone.
- The 60 s hedge covers both reasons: no precondition lost, and caught less often.

**v6 (254 words; longer than v5, because all four numbers and both reroutes are now stated):**

> On adaptivity, the two attackers lose time to different MTD mechanisms (Figure 5.2(b)). After a disruption, MTDSim sends the baseline attacker back to a fixed attack action of its procedure (Section 2.2.3). The APT attacker model is not sent back: its Petri net picks its next tactic, and a failed attack action reroutes it through the failure matrix (Section 4.4.2). A host-layer deployment takes the host either attacker was working on. The baseline attacker is sent back to scanning hosts and enumerates one next; its time lost is at or below zero. The APT attacker model enumerates a host only in Lateral Movement (Section 4.3.2). Until its Petri net next reaches it, the attack actions of its other tactics most likely fail for a missing host, and each failure reroutes it again (Appendices F.2 and F.4). It loses 242 to 324 s per deployment. A service-layer deployment changes services, not hosts, so neither attacker loses its host. The baseline attacker is sent back to scanning that host's ports, and under service diversity, which redraws every service, it starts its exploits on that host again. It loses 493 s per deployment. The APT attacker model keeps the ports it found, so nothing it runs next fails for a missing precondition, and a deployment catches it less often: its tactic durations keep it in unmapped tactics, which run no attack action, so its attack actions blocked per service-layer deployment are 0.15, against 0.95 (Figure 5.2(a)). It loses 60 s per service-diversity deployment, likely for both reasons.

### 28.10 Fresh scrutiny of v5 and v6: why the drafts circle, and the lean argument (Marc 2026-10-12, "why are we circling … what is a discussion point, keep it; what is not, get rid of it"; no drafting)

**Two facts checked first:**
- **The failure matrix does not explain the host-layer cost.** §5.4 (Table 5.4) removed it under IP shuffle: NCR 0.007 against 0.006 at 200 s, 0.114 against 0.109 at 2 000 s, both negligible. v6's "a failed attack action reroutes it through the failure matrix" is therefore contradicted by our own ablation. Marc's suspicion was right.
- **Lateral Movement is not rare.** With no MTD it is 9 % of the APT attacker model's steps (5.6–13.8 % by attack profile; Figure 5.1(a)), and 1.4 % of its time (numbers_reported.json, step_share/time_share). After a host-layer deployment, the APT attacker model visits 8–10 tactics before Lateral Movement gives it a host back, 216–304 s (disruption_mechanism.md §C (iv)). That is about one step in eleven, at its tactic durations per step. **The wait is the order of its tactics (how often Lateral Movement comes up) times its tactic durations (how long each step in between takes)**, the opener's two causes. The rerouting is the Petri net moving on, as it always does, not the failure matrix.

**Why the drafts circle:**
1. **The mechanism was never settled before drafting.** Five drafts gave four explanations:
   - the procedure restarts;
   - the attacker loses its place;
   - a fixed return point;
   - the failure matrix reroutes it.

   Prose cannot converge on a claim that keeps changing.
2. **One explanation contradicted our own result** (the failure matrix, §5.4). A cold examiner would catch it.
3. **Accretion.** Each critique was answered by adding a clause, never by removing an idea. v6 carries two metrics × two layers × two attackers, plus the first deployment, preconditions, the failure matrix and the blocks.
4. **The throughline was imposed top-down.** "Host layer = the order of its tactics, service layer = tactic durations" does not match the data:
   - the host-layer wait is *both* causes;
   - the service-diversity cost is the *baseline attacker's* rule.

   Forcing the split is what made v4 dishonest.
5. **Bookkeeping drove the prose.** v6 was rearranged to place numbers, and the argument got harder to follow (memory: bookkeeping never drives prose).

**The sort:**

| Point | Verdict | Why |
|---|---|---|
| D1. The 2×2: the host layer costs the APT attacker model 242–324 s and the baseline attacker none (at or below zero); service diversity costs the baseline attacker 493 s and the APT attacker model 60 s | **keep**, as the lead | the finding, specific; all four cells (Marc) |
| D2. Host layer: the deployment takes the host each attacker was working on. The baseline attacker is sent back to scanning hosts and enumerates one next. The APT attacker model enumerates a host only in Lateral Movement, about one step in eleven, so it waits through its other tactics, and their attack actions most likely fail for a missing host | **keep** | the discussion point; it is the opener's two causes, verified |
| D3. Service diversity: MTDSim sends the baseline attacker back to scanning that host's ports, and with every service redrawn it starts that host's exploits again. The APT attacker model is not sent back; it keeps its host and the ports it found | **keep**, one hedge | the discussion point; MTDSim's rule acts through the baseline attacker's procedure |
| "The two attackers lose time to different MTD mechanisms" | cut | vague; D1 states it with numbers |
| "After a disruption, MTDSim sends the baseline attacker back to a fixed attack action of its procedure" | cut | abstract; D2 and D3 each name the attack action |
| The failure matrix, rerouting | cut | contradicted by §5.4 |
| "The APT attacker model is not sent back" as its own sentence | fold into D3 | it matters only for the service layer |
| Attack actions blocked, 0.15 against 0.95, tactic durations | cut | §5.3.1 states it, and it is a secondary cause of the 60 s next to D3 |
| The first deployment's second attempt; why the value is at or below zero | §6.5 | a property of the metric (counterfactual exact only to the first deployment) |
| "Neither attacker loses its host" | fold into D3 | "that host's ports" and "keeps its host" carry it |
| After Lateral Movement it also needs Discovery before it can exploit | off | implicit nuance; the wait to a host already carries the point |

**Split into two paragraphs?** No. D1–D3 come to about 120–150 words in one paragraph: a lead, three sentences on the host layer, two on service diversity. Split by layer only if D2 or D3 cannot be said in that.

**Tie to the opener:**
- **D2** is both causes, so it matches "its tactic durations and the order of its tactics".
- **D3** is the baseline attacker's procedure against the APT attacker model's Petri net, which picks its next tactic, so it is the order of its tactics in the broad sense.

Nothing in the opener needs changing.

**Advice for the rest of Chapter 6:**
- (ae) Settle each mechanism in one line, verified against the code and the ablations (§5.4), *before* drafting. If a critique changes the mechanism, re-settle it; do not redraft around it.
- (af) When a critique says "unclear", cut an idea before adding a clause.
- (ag) A throughline is checked against the data per claim. Where the data do not split as the throughline does, the throughline gives way.

### 28.11 v7, from the sort (Marc 2026-10-12, "translate this … abide by your own scrutiny"; proposed, not applied)

**Mechanisms settled first (one line each, verified):**
- **Host layer.**
  - The deployment costs each attacker the host it was working on (§2.2.3; code: the cursor is cleared).
  - The baseline attacker is sent back to scanning hosts and enumerates one next (§2.2.3, its procedure).
  - The APT attacker model enumerates a host only in Lateral Movement (§4.3.2): 6–14 % of its steps with no MTD (Figure 5.1(a); numbers_reported.json step_share 0.056–0.138). After a deployment, it visits 8–10 tactics before Lateral Movement, 216–304 s (disruption_mechanism.md §C (iv)). How often Lateral Movement comes up is the order of its tactics; how long each step in between takes is its tactic durations.
  - Not the failure matrix (§5.4).
- **Service diversity.**
  - MTDSim sends the baseline attacker back to scanning the same host's ports (§2.2.3), and with every service redrawn it starts that host's exploits again (disruption_mechanism.md §1: its exploit progress is erased).
  - The APT attacker model is not sent back. It keeps its host and the ports it found (§C (iv)), which likely explains 60 s. One hedge, since the cause of 60 s is untraced.

**v7 (173 words):**

> On adaptivity, the APT attacker model's time lost per host-layer deployment is 242 to 324 s, against at or below zero for the baseline attacker; per service-diversity deployment, the baseline attacker's is 493 s, against 60 s (Figure 5.2(b)). A host-layer deployment costs each attacker the host it was working on (Section 2.2.3). The baseline attacker is sent back to scanning hosts and enumerates one next. The APT attacker model enumerates a host only in Lateral Movement (Section 4.3.2), which the order of its tactics reaches in 6 to 14 % of its steps with no MTD (Figure 5.1(a)). Until then, the attack actions of its other tactics most likely fail for a missing host, and its tactic durations set how long that lasts (Appendices F.2 and F.4). Service diversity redraws every service, and MTDSim sends the baseline attacker back to scanning the same host's ports, so it starts that host's exploits again. The APT attacker model is not sent back and keeps the ports it found, which likely explains its 60 s.

**Checked against the scrutiny:**
- **D1–D3 only.** Every cut item from §28.10 is absent.
- **All four numbers,** given once in the lead under the metric's name.
- **Both causes handed back in D2,** verbatim.
- **One hedge per inferred claim** ("most likely" on the missing-host failures, "likely" on the 60 s). The facts that hold by construction carry no hedge.
- **Every term is a ch2 or ch4 term:**
  - "sent back to scanning hosts", "the same host's ports" (§2.2.3);
  - "enumerates", "Lateral Movement" (§4.3.2);
  - "tactic durations", "the order of its tactics" (§6.1).
- **"Place" is gone.**
- **No pronoun has two candidate referents.** Each "it" in the last two sentences has one possible antecedent.

**On apply (downstream, automatic):**
- §6.5's first-deployment sentence repoints from §6.2 to §5.3.1 and takes the reason in one clause.
- §6.4 l.9221–9223 ("its place … Lateral Movement") is aligned when §6.4 is reached.
- The §5.3.1 sentence "The APT attacker model runs no attack action while in an unmapped tactic, so an MTD deployment then blocks none" stays: v7 no longer repeats it, so the ch5 cut proposed in §28.6 is withdrawn.

### 28.12 v7's terms audited against what the reader is given; v8 (Marc 2026-10-12, "careful with the language … standard terms and specific terms"; proposed, not applied)

| v7 phrase | What the reader has been given | v8 |
|---|---|---|
| "per host-layer deployment … per service-diversity deployment" (a layer against one mechanism, with no reason given) | ch5's "loses … s per host-layer deployment"; Figure 5.2(b) is per mechanism | say why these two cells: the APT attacker model loses time *mainly* to the host layer (no other mechanism costs it more than 60 s); the baseline attacker *only* to service diversity (every other mechanism is at or below zero) |
| "costs each attacker the host it was working on" | §2.2.3: "because the host it was on may have moved" | "neither attacker has a host to act on, because the host it was on may have moved" |
| "sent back to scanning hosts" | §2.2.3 verb phrase; the attack action's name is *scan host* (§4.3.2) | "MTDSim sends the baseline attacker back to scan host" |
| "enumerates one next" | *enumerate host*; the baseline attacker's procedure (§2.2.3, §6.1) | "its procedure runs enumerate host next" |
| "enumerates a host only in Lateral Movement" | §4.3.2: Lateral Movement maps to enumerate host; "a tactic runs its attack action" (ratified verb) | "only Lateral Movement runs enumerate host" |
| "6 to 14 % of its steps" | §4.5.1's metric, *relative tactic occurrence*; Figure 5.1(a) | "a relative tactic occurrence of 6 to 14 % with no MTD" |
| "fail for a missing host" | §4.4: "An attack action fails if its preconditions were missing" | "fail because their preconditions are missing" |
| "sends … back to scanning the same host's ports" | §2.2.3; attack action *scan port* | "back to scan port on the same host" |
| "starts that host's exploits again" | §2.2.3: it exploits vulnerabilities in order of return on attack | "exploits the host's new vulnerabilities from the start" |
| "is not sent back" (no mechanism given) | §6.1 ¶2: the Petri net picks the next tactic | "its Petri net picks its next tactic" |
| "keeps the ports it found" | scan port finds them (§2.2.3) | kept |

**v8 (222 words; v7 was 173). Spelling out the terms costs about 50 words:**

> On adaptivity, the APT attacker model loses time mainly to the host layer, 242 to 324 s per deployment, where the baseline attacker's time lost is at or below zero; the baseline attacker loses time only to service diversity, 493 s per deployment, where the APT attacker model loses 60 s (Figure 5.2(b)). After a host-layer deployment, neither attacker has a host to act on, because the host it was on may have moved (Section 2.2.3). MTDSim sends the baseline attacker back to scan host, and its procedure runs enumerate host next. For the APT attacker model, only Lateral Movement runs enumerate host (Section 4.3.2), and the order of its tactics gives Lateral Movement a relative tactic occurrence of 6 to 14 % with no MTD (Figure 5.1(a)). Until it next runs, the attack actions of its other tactics most likely fail because their preconditions are missing, and its tactic durations set how long that lasts (Appendices F.2 and F.4). A service-diversity deployment redraws every service on every host, and MTDSim sends the baseline attacker back to scan port on the same host, so it exploits the host's new vulnerabilities from the start. The APT attacker model is not sent back: its Petri net picks its next tactic, and it keeps the ports it had found, which likely explains its 60 s.

**Still flagged:** "the ports it had found" and its effect on the 60 s come from the code audit (disruption_mechanism.md §C (iv)–(v)), not from a thesis section. They carry the paragraph's one "likely".

### 28.13 v8 nuance pass; v9 (Marc 2026-10-12, "95 % of the way … what nuance is needed, what can live in the hedge"; proposed, not applied)

| v8 detail | Verdict | Why |
|---|---|---|
| The four numbers, "mainly", "only" | keep | the finding, and why these two cells |
| "because the host it was on may have moved" | cut | §2.2.3 gives the reason, and the pointer stays |
| "sends … back to scan host … runs enumerate host next" | keep | the contrast the paragraph turns on |
| "only Lateral Movement runs enumerate host" | keep | the mechanism |
| "the order of its tactics gives Lateral Movement a relative tactic occurrence of 6 to 14 % with no MTD (Figure 5.1(a))" | cut the share; keep the order as the clause "until the order of its tactics next brings it there" | 242–324 s already measures the wait, so the share is a second number for the same point |
| "and its tactic durations set how long that lasts" | cut (Marc's example) | the length of the wait is implicit in "until"; the measured result is 242–324 s |
| "(Appendices F.2 and F.4)" | F.4 only | F.4 (the traced run, 255 of 363 attack actions refused for missing preconditions) is the evidence for "most likely fail"; F.2 (no foothold) supports no sentence here, and F.2 already points to §6.2 |
| "redraws every service on every host" | "redraws every service" | Table 2.3 gives "on every internal host" |
| "so it exploits the host's new vulnerabilities from the start" | keep | the cost to the baseline attacker |
| "is not sent back:" | cut (a rhetorical lead) | replaced by what it does: "keeps the ports it had found and goes on to the tactic its Petri net picks" |
| Two hedges ("most likely", "likely") | keep | one per inferred claim; everything else is by construction or measured |

**Note:** with "its tactic durations" cut, ¶2 hands back only the order of its tactics by name. If the throughline should name both causes here, the smallest fold is "until the order of its tactics, at its tactic durations, next brings it there" (four words).

**v9 (185 words):**

> On adaptivity, the APT attacker model loses time mainly to the host layer, 242 to 324 s per deployment, where the baseline attacker's time lost is at or below zero; the baseline attacker loses time only to service diversity, 493 s per deployment, where the APT attacker model loses 60 s (Figure 5.2(b)). After a host-layer deployment, neither attacker has a host to act on (Section 2.2.3). MTDSim sends the baseline attacker back to scan host, and its procedure runs enumerate host next. For the APT attacker model, only Lateral Movement runs enumerate host (Section 4.3.2), so it has no host until the order of its tactics next brings it there, and meanwhile the attack actions of its other tactics most likely fail because their preconditions are missing (Appendix F.4). Service diversity redraws every service, and MTDSim sends the baseline attacker back to scan port on the same host, so it exploits the host's new vulnerabilities from the start. The APT attacker model keeps the ports it had found and goes on to the tactic its Petri net picks, which likely explains its 60 s.

### 28.14 v9 applied after a final clarity pass (Marc 2026-10-12, "happy with that")

**Clarity pass:** one fix. "Until the order of its tactics next brings it *there*" could be read as "to a host", so it now reads "brings it to Lateral Movement" (a repeated name is clearer than a vague pointer). Everything else held: the terms are from ch2, ch4 and §4.5, and there is one hedge per inferred claim.

**Applied:** v9 in place of the stage-1 paragraph, at 186 words (from 258).

**Downstream (automatic):**
- **§6.5, the bound on time lost:** the first-deployment sentence now gives the reason and repoints to §5.3.1: "falls below zero: sent back to scan host, it gets a second attempt at its first host, as MTDSim's rule intends \citep{brown2023} (Section 5.3.1)".
- **§6.5, threats:** "costs the APT attacker model its place … might keep its place" became "has no host to act on until its Petri net next reaches Lateral Movement … might keep one".
- **Appendix F.2:** "costs either attacker its place … regains it" became "neither attacker has a host to act on … gets one back".
- **Appendix F.4:** "has lost its place" became "has no host to act on".

**Remaining "its place":** only ch2 l.957 ("the attacker loses only its place"). The proposal in §28.8 is still open (gated).

Build clean, 120 pages, 0 undefined.


## 29. §6.2 ¶3 (MTD ranking against each attacker): scrutiny (Marc 2026-10-12; nothing applied)

Current ¶3: 178 words, 6 sentences. ρ; "NCR reduction falls as the deployment interval grows"; the half-or-more intervals; the recovery-time rule; user shuffle's rule.

### 29.1 Marc's questions

- **"On MTD ranking" is not a property.** True. §6.1's "On X" leads name properties, and ¶2's "On adaptivity" does too. "MTD ranking against each attacker" is §5.3.2's heading, not a property. The reader's term for this paragraph is the **metric and its axis: NCR reduction against the deployment interval** (§4.5.3, §2.2.2, Figure 5.3). Recommend dropping the "On X" formula here and opening on the claim in those terms.
- **"Rankings are only useful in context; they carry the model's assumptions."** That is an *implication*, and §6.4's first paragraph already owns it: "An optimal MTD mechanism is therefore optimal for one attacker model in one simulator, and an evaluation should report its ranking with the attacker model behind it and the assumptions that model and the simulator make. Neither of the two attacker models is the better one: each ranking is right for its own." §6.5 bounds it (MTDSim's rules). One fact, one home: not in §6.2.
- **"The point is no correlation between these ten numbers."** That is ρ, −0.24 to 0.25. It is §5.3.2's result, and §6.4 opens on it as the point that transfers. The opener already answers SQ3 with the layer reversal, the specific form of "no correlation". So ρ in ¶3 is a third telling.

### 29.2 What ¶3 can say that nothing else says (the takeaway, one line)

**Against the APT attacker model, the host layer keeps halving NCR at deployment intervals ten times longer than against the baseline attacker (1 000 s against 100 s), and the service layer never halves it. This fits what ¶2 found: each host-layer deployment costs it 242–324 s, about a quarter to a third of a 1 000 s interval.**

This is the deployment-interval half of SQ3's answer. It is also the fact behind the close's Chapter 1 tie (MTD's aim of shifting the advantage of time to the defender), so ¶3 and the close currently say it twice (stage-1 flag 2).

### 29.3 Sentence by sentence

| Sentence | Verdict | Why |
|---|---|---|
| S1 "On MTD ranking …, ρ … −0.24 and 0.25 at every deployment interval (Table 5.3)" | cut | §5.3.2 and §6.4's opener; the opener gives the specific form. Also, Table 5.3 is 200 s only, so it cannot show "every deployment interval" |
| S2 "NCR reduction falls as the deployment interval grows" | cut | §5.3.2 replay; "up to 1 000 s" already implies it |
| S3 the half-or-more intervals (host: 1 000 s against 100 s; service: 200 s, never) | **keep**, as the lead | the new fact for SQ3; §6.4 l.9228 cites §6.2 for "never" |
| S4 "MTD likely reduces an attacker's NCR only while the deployment interval is shorter than the time the attacker needs to recover …" | cut as a general rule; keep a narrow, hedged link for the APT attacker model's host layer only | **not verified, with counterexamples** (lesson (ae)): port shuffle still reduces the baseline attacker's NCR by 0.91 at 200 s, though a later deployment costs it about 21 s. The host layer halves the baseline attacker's NCR to 100 s at 19–32 s per later deployment, while the service layer, at +34 to +76 s per later deployment of the APT attacker model, never halves its NCR. As a threshold it also fails for the APT attacker model itself: the host layer still halves its NCR at 1 000 s, beyond its 242–324 s. What holds is narrower: the longer each host-layer deployment costs the APT attacker model, the larger the share of each interval it loses |
| S5 user shuffle raises the APT attacker model's NCR (redrawn accounts, held accounts stay valid) | move: Appendix F.3 (fa-accounts) explains it in full; §6.4 l.9125 repoints there | an artefact of MTDSim's rule (the appendix says so: "follows from MTDSim's rule for user shuffle, not from user shuffle as an MTD mechanism"); not SQ3's answer |

### 29.4 §6.1's lessons, checked against ¶3

| Lesson | Here |
|---|---|
| Replay test | **fails**: S1, S2 |
| One fact, one home | **fails**: ρ in three places; the interval facts in ¶3 and the close; user shuffle's rule in ¶3, §6.4 and Appendix F.3 |
| (ae) settle the mechanism, verified, before drafting | **fails**: S4 is a general rule with counterexamples |
| §9.3 open on the reader's term | **fails**: a §5.3.2 heading, not a property or a metric |
| §9.8 float next to the claim | **fails**: S1 cites Table 5.3 (200 s) for a claim at every interval; the interval claims belong to Figure 5.3 or Table F.1 |
| (k) numbers with their frame | ✓ for S3 |
| Hedge inside the inferred claim | ✓ (one "likely"), but on the wrong claim |

### 29.5 Slots (no prose)

1. **Lead, the fact.** Job: the interval half of the answer. Facts: the host layer halves the APT attacker model's NCR up to 1 000 s, the baseline attacker's only up to 100 s; the service layer halves the baseline attacker's up to 200 s and never the APT attacker model's. Float: Figure 5.3, Table F.1. Ceiling: one sentence, the metric and the deployment interval named, no "On X".
2. **Why, APT attacker model only, one hedge.** Job: tie to ¶2. Facts: each host-layer deployment costs it 242–324 s, a quarter to a third of a 1 000 s interval. Ceiling: one sentence.
3. **(Optional) the Chapter 1 tie.** MTD's aim of shifting the advantage of time to the defender: against the APT attacker model, the host layer holds it at intervals ten times longer. If it lives here, the close keeps only its last sentence or goes (Q3).

Estimated 50–70 words, from 178.

### 29.6 Questions (recommendation first)

- **Q1, the takeaway.** (Recommended) ¶3 is the deployment interval: the host layer halves the APT attacker model's NCR to intervals ten times longer, and fits ¶2. ρ and "rankings carry their model's assumptions" stay in §6.4, which owns them. Otherwise, ¶3 restates ρ as its lead (a third telling).
- **Q2, user shuffle.** (Recommended) Move it to Appendix F.3, and repoint §6.4 l.9125 there (downstream, automatic). Otherwise keep one sentence here.
- **Q3, where the Chapter 1 tie lives.** (Recommended) **In ¶3, as its last sentence**, which leaves the close with only the bound sentence. That sentence is also §6.5's, so the close then goes, and the section ends on the attack profiles. Settle at the close round. Otherwise the tie stays in the close and ¶3 stops at slot 2.

### 29.7 Marc: "what explanation does the reader take from ¶3? Does it live elsewhere, or is it in the wrong spot?"

**Answer: in the wrong spot. ¶3 has no explanation of its own.**
- Once the other sections' points leave (ρ and "rankings carry their model's assumptions" to §6.4; user shuffle to Appendix F.3) and the unverified recovery-time rule goes, one explanation is left. It is ¶2's mechanism carried from one deployment to NCR across deployment intervals: **because each host-layer deployment costs the APT attacker model 242–324 s, the host layer still halves its NCR when it is deployed only every 1 000 s, ten times the interval at which it still halves the baseline attacker's.**
- That is the fact behind the close's Chapter 1 tie (MTD's aim of shifting the advantage of time to the defender), and the close already states it ("up to ten times longer"). ¶3 and the close are therefore one point told twice.

**Recommendation: dissolve ¶3; its explanation becomes the close.** The close is the joint (lesson (aa)): it ties the opener's answer and ¶2's mechanism to Chapter 1's aim, which the paragraphs do not say together.
- **Close, slot 1:** the interval fact, with ¶2's 242–324 s as its likely reason (one hedge).
- **Close, slot 2:** what it means against Chapter 1's aim (advantage of time).
- **Close, cut:** its last sentence ("Each part of this answer rests on MTDSim's rules …"), which is §6.5's bound.

About 60 words in place of ¶3's 178 and the close's 75.

**The section then runs:**
1. opener (the layer answer, both causes);
2. ¶2, adaptivity (the mechanism at one deployment);
3. deployment strategies (MTDShield);
4. by attack profile;
5. close (the deployment interval and Chapter 1's advantage of time).

The mirror of §5.3 holds: §5.3.2's ranking is the opener (mechanisms) and the MTDShield paragraph (deployment strategies).

**Alternative:** the interval sentence as ¶2's last sentence (mechanism, then its consequence), with the close keeping only the Chapter 1 tie. It reads in the order of the logic, but makes ¶2, already the densest paragraph, longer.

### 29.8 Applied (Marc 2026-10-12, "easy done … downstream automatic")

**¶3 dissolved; the close rewritten:**
> The host layer reduces the APT attacker model's NCR by half or more at deployment intervals up to 1 000 s, and the baseline attacker's only up to 100 s, likely because each host-layer deployment costs the APT attacker model 242 to 324 s; the service layer never halves the APT attacker model's NCR (Table F.1). Chapter 1 set MTD the aim of shifting the advantage of time to the defender \citep{ghosh2009nitrd}: against the APT attacker model, the host layer holds it at deployment intervals ten times longer.

The bound sentence ("Each part of this answer rests on MTDSim's rules …") is cut; §6.5 holds it.

**Downstream (automatic):**
- **§6.4:** user shuffle's rule now cites Appendix F.3 (fa-accounts), not §6.2.
- **Appendix F.3:** the lead stands alone ("User shuffle raises … because it redraws …"), no longer "Section 6.2 explains why".
- **§6.4, the deployment-interval paragraph:** the last two "hold … back" phrases are replaced:
  - "where both MTD layers reduce the baseline attacker's NCR" (not "halve": the host layer gives 0.49 at 200 s);
  - "where MTD stops reducing an attacker's NCR".
- **§6.4's "a service layer that never halves the APT attacker model's NCR (§6.2)":** the close still states it.

**§6.2 now:** opener, adaptivity, deployment strategies (MTDShield), by attack profile, close. About 560 words, from 1 426.

Build clean, 120 pages, 0 undefined.

## 30. §6.2 deployment strategies (MTDShield) paragraph: scrutiny (Marc 2026-10-12; nothing applied)

Marc: "what is the explanation we're trying to give here … why does this read like a collection of facts rather than an argument … boil it down to the discussion … what's the structure … are the scrutiny's lessons applicable?"

### 30.1 Facts verified before any drafting (lesson (ae))
- **Random and alternative draw from all seven MTD mechanisms.** `run_corpus._strategies` passes the full pool; `random.choice` / a fixed rotation. So three of every seven deployments are host layer.
- **MTDShield's four:** complete topology shuffle, IP shuffle, OS diversity, service diversity, or none (§2.2.2).
- **MTDShield at 200 s (Appendix D.5):**
  - service diversity at 76 % of decisions (baseline attacker) and 70 % (APT attacker model);
  - nothing at 23 % and 29 %;
  - the other three under 1 % together.
- **Table F.1 at 200 s:**

  | | APT attacker model | Baseline attacker |
  |---|---|---|
  | Random | 0.75 | 0.33 |
  | Alternative | 0.72 | 0.38 |
  | MTDShield | 0.28 | 0.68 |
  | Random over MTDShield's four | 0.80 | 0.56 |
  | Service diversity alone | 0.36 | 0.92 |

- **MTDShield sits just below service diversity alone against both attackers.** That fits "service diversity, deployed less often" (nothing at about a quarter of decisions).
- **Not additive (nuance, keep off the page).**
  - At 200 s, random gives 0.75 against the APT attacker model, where the mean of the seven mechanisms is 0.48. Against the baseline attacker it gives 0.33, where the mean is 0.56.
  - Random over MTDShield's four behaves the same way: 0.80 against a mean of 0.59, and 0.56 against 0.68.
  - So a deployment strategy follows its mechanisms in **direction**, not in size. Never write "the sum" or "the mean". The likely reason (a host-layer deployment costs the APT attacker model longer than the interval) is untraced.

### 30.2 Why it reads as a collection of facts
It has no claim of its own. Sentence by sentence:
1. **S1** (random and alternative more against the APT attacker model; MTDShield more against the baseline attacker up to 1 000 s) is §5.3.2 ¶2 almost word for word. It is a ch5 rehash in the place where the paragraph's claim should be.
2. **S2** (0.68 vs 0.56; 0.28 vs 0.80) is a number with no reason given for it.
3. **S3** (76 % / 70 %; the other three under 1 %) is a second fact. It never says what the choice does to NCR reduction, which is the explanation.
4. **S4** (rank 1, so "consistent with a policy fitted to the baseline attacker") answers *was MTDShield fitted to the baseline attacker?* That is §6.4 ¶2's question, and §6.4 already asks and bounds it.
5. **S5** ("cannot tell a fitted policy from a fixed preference") is §6.4's "whether MTDShield was fitted to one, this run cannot tell", told twice.

So the paragraph's only explanation is implied between S1 and S3, and never stated: **a deployment strategy reduces an attacker's NCR as the MTD mechanisms it deploys do.** That is ¶2's adaptivity result carried to the deployment strategies. It is the "components → what is measured" reading Marc gave, in direction and not in size.

### 30.3 Lessons checked
- **(ab) Answer first, in the question's terms.** The answer is the explanation. The ch5 fact follows as evidence and is no longer the lead.
- **(ac) Layer terms, checked per mechanism.** "Host layer" for random and alternative's three of seven holds (all three host-layer mechanisms halve the APT attacker model's NCR at 200 s). For MTDShield, name service diversity, not "the service layer": it picks one mechanism.
- **(ad) Name which comparison a cause explains.** The mix explains the *between-attacker* direction for each deployment strategy, and MTDShield against random over the same four. It does not explain MTDShield against service diversity alone, beyond "deployed less often".
- **(ae) Verified before drafting.** Done (30.1).
- **(af) Cut an idea before adding a clause.** "Trained against the baseline attacker", "fitted policy" and the four zero inputs are all §6.4's.
- **(ag) A throughline gives way to the data.** The non-additivity stays off the page, so no size claim.
- **¶3's lesson: is the argument owned elsewhere?** Partly. §6.4 owns *why MTDShield chose service diversity* (fitted or not) and the test recommendation. §6.2 owns only *what the choice does to each attacker's NCR*.
- **Property parallel.** Not "On deployment-strategy awareness": neither attacker has it, and the result is adaptivity's (time lost per MTD deployment), carried through the deployment strategy. The deployment strategies are the subject.

### 30.4 Slots (no prose)
- **S1, the answer.** Each deployment strategy reduces an attacker's NCR as the MTD mechanisms it deploys do (Figure 5.3(d)–(f)). This is directional; one "likely" if Marc reads it as inferred.
- **S2, random and alternative.**
  - Job: they draw from all seven, so three of every seven deployments are host layer, and they reduce the APT attacker model's NCR more at every deployment interval.
  - Numbers: 0.75 and 0.72 against 0.33 and 0.38 at 200 s.
- **S3, MTDShield.**
  - Job: it deploys service diversity at 70 % or more of its decisions, nothing at most of the rest, and the host layer at under 1 %, so it reduces the baseline attacker's NCR more, a little below service diversity alone.
  - Numbers: 0.68 against 0.92; 0.28 against 0.36 (Appendix D.5).
- **S4, the matched control** (§6.4 points here).
  - Job: random over the same four deploys IP shuffle or complete topology shuffle at half its deployments. It beats MTDShield against the APT attacker model and loses to it against the baseline attacker.
  - Numbers: 0.80 against 0.28; 0.56 against 0.68 (Table F.1).
- **Cut:**
  - current S1 (§5.3.2);
  - S4 (rank 1 → "fitted": §6.4);
  - S5 ("cannot tell": §6.4, Appendix D.4);
  - the 76/70 split (one form, "70 % or more", as §5.3.2 and §6.4 give it).

About 90–110 words, from 183.

### 30.5 Questions (recommendation first)
- **Q1. Do the matched-control numbers stay here?** Recommend yes. They are the sharpest evidence for S1, and §6.4 ¶2 cites §6.2 for "beats random over the same four … against the baseline attacker alone". Alternative: move them to §6.4 and repoint to Table F.1. §6.2 is then three sentences, and §6.4 grows.
- **Q2. Does "trained against the baseline attacker" stay off this paragraph?** Recommend yes. It is the reason the reader cares *why* MTDShield chose service diversity, which is §6.4's question ("The dependence reaches deployment strategies").
- **Q3. S3's "nothing at most of the rest" needs the 23 % / 29 % to be specific.** Recommend giving them in the parenthesis cite only to Appendix D.5 and keeping "nothing at most of the rest" in the prose. Alternative: one number pair in the prose.

### 30.6 Marc: "is this a paragraph worth keeping, or do the points live elsewhere?" Cut (Marc 2026-10-12, "easy done … let's cut that")

**Takeaway proposed:** the deployment strategy that reduces the baseline attacker's NCR most, MTDShield, reduces the APT attacker model's least, likely because it deploys almost only service diversity. Checked at every deployment interval in Table F.1: top against the baseline attacker and bottom against the APT attacker model.

**Verdict: cut, like ¶3.**
- Random and alternative need no explanation: they draw from all seven, so they deploy both layers, and the opener covers them.
- MTDShield's point is §6.4's argument. §6.4 ¶1 has chapter 3's "the attacker model decides which deployment strategy is optimal" and no deployment strategy first against both. §6.4 ¶2 has "The dependence reaches deployment strategies".
- The preamble promises §6.2 only the layer explanation.

**Applied:**
- **§6.2:** the paragraph is replaced by a comment block.
- **§6.4 ¶2:** "MTDShield was trained against the baseline attacker and chooses service diversity at 70 % or more of its decisions (Appendix D.5), the only MTD mechanism the baseline attacker loses time to (Section 6.2). At 200 s it beats random over the same four MTD mechanisms against the baseline attacker, 0.68 against 0.56, and loses to it against the APT attacker model, 0.28 against 0.80 (Table F.1)."
- **No other inbound reference** depended on the paragraph. Ch7's draftnotes cite §6.2 for "no rank first"; that repoint is already gated.

**§6.2 now:** opener, adaptivity, by attack profile, close. The §5.3 mirror holds at the mechanism level; the deployment strategies sit in §6.4.

Build clean, 119 pages, 0 undefined.

## 31. §6.2's last two paragraphs (by attack profile; the close): scrutiny (Marc 2026-10-12; nothing applied)

Marc: "what are their purposes, their one-liners, are they cuttable … what explanation do we need to deliver? Interval goes up, disruption goes down, as expected, almost tautological."

### 31.1 By attack profile (≈75 words)
- **One-liner it tries:** MTD's effect depends more on the attacker model than on the attack profile, because an attack profile's objective shows only in unmapped tactics.
- **S1** is §5.3.3 ¶1 almost word for word: a ch5 rehash.
- **S2's explanation is already given twice.**
  - §6.1's objective-specific paragraph: "an attack profile's objective shows only in actions on objectives … unmapped".
  - §6.3: "Exfiltration and Impact are unmapped, so the attack profiles take the same six attack actions at different rates".
- **S2's "therefore depends more on the attacker model" is §6.3's** ("the reversal therefore rests on … not on the failure matrix, the vulnerability memory or the attack profiles", from the ablation).
- **SQ3 relevance:** none. It compares the attack profiles with each other, not the two attackers. Its only job is a scope check (the average over c1–c4 hides no split), and Figure 5.4 and §5.3.3 already show that.
- **Verdict: cut.** Nothing is lost. The flagged "which fits Section 6.1" (the session's inference) goes with it.

### 31.2 The close (≈75 words, two sentences, two jobs)
- **Sentence 1** (the host layer halves the APT attacker model's NCR up to 1 000 s and the baseline attacker's only up to 100 s, likely because of 242–324 s per deployment; the service layer never halves the APT attacker model's):
  - **The downward trend is not an explanation.** NCR reduction falls as the interval grows for every mechanism and both attackers, as expected. Ch5 reports it.
  - **The only part that isn't tautological** is the gap between the attackers (1 000 s against 100 s). That is a Table F.1 fact. Its reason is ¶2's per-deployment mechanism seen across intervals.
  - **The reason is only half true.** It holds on the APT attacker model's side. On the baseline attacker's side, time lost does not set the result: the host layer reduces its NCR by 0.72 at 50 s with time lost at or below zero, so blocks do the work. This is the recovery-time rule that §29 rejected, back in hedged form.
  - **§6.4 already owns what the interval means:** the earlier studies' 50–200 s, "judge the host layer spent far sooner", "a service layer that never halves". It cites §6.2 only for the numbers.
- **Sentence 2** (Chapter 1's "shifting the advantage of time to the defender" (Ghosh): "the host layer holds it at deployment intervals ten times longer"):
  - This is an answer-level "so what". It ties to chapter 1's aim, not an explanation of a result.
  - "holds it" is figurative.
  - Its home is ch7, where the answers meet the research question. Ch7's Contribution 2 draftnote already names this number as its candidate ("the host layer keeps half of the APT attacker model's NCR off up to 1 000 s, against 100 s").
- **Verdict: cut from §6.2.**
  - **§6.4 (downstream, auto after ruling):** "(Section 6.2)" repoints to Table F.1, and "far sooner" becomes specific: spent beyond 100 s, though it halves the APT attacker model's NCR up to 1 000 s.
  - **Ch7 (gated, proposed):** add the advantage-of-time tie to the Contribution 2 draftnote beside its candidate number.

### 31.3 What §6.2 is then
The opener (the answer to SQ3, both causes) and ¶2 (adaptivity: why, per deployment), about 250 words.
- It ends on ¶2's service-diversity sentence ("which likely explains its 60 s"). That is a weak last line, but it stops at the peak and adds nothing.
- **Alternative:** keep one closing sentence that gives the interval gap and its ¶2 reason for the APT attacker model only, with no ch1 tie. That costs about 35 words and re-states a Table F.1 fact. Not recommended.

### 31.4 Marc: "is the lean §6.2 satisfactory? What does the close look like? Draft it" (proposed, not applied)

**Marc is happy with the cuts in 31.1 and 31.2.** They will be applied together with the close.

**What the close must do.** The opener names two causes. ¶2 cashes only the order of its tactics (time lost under the host layer). It leaves two things open:
- why the host layer reduces the baseline attacker's NCR at all, when its time lost is at or below zero;
- where the tactic durations come in.

Both are answered by attack actions blocked per MTD deployment:
- **Baseline attacker:** 0.95 to 1 under every host-layer and service-layer mechanism (§5.3.1).
- **APT attacker model:** 0.15 to 0.39.
- **The tactic durations put 34 to 57 % of an attack profile's run in unmapped tactics** (Appendix G.3, fa-run-time). Ch4 §4.3.2 and §5.3.1 say an MTD deployment there blocks no attack action.

This is the parallel of §6.1's close: both causes joined, each to the comparison it explains (lesson (ad)).

**Not the dishonest throughline.** Durations explain blocks under *every* mechanism, not "the service layer". The 60 s stays ¶2's (ports kept).

**A separate paragraph, not the end of ¶2.** ¶2 is time lost (adaptivity) and already 186 words; this is blocks, the other half of Figure 5.2.

**Draft (≈110 words):**
> Attack actions blocked per MTD deployment is 0.95 to 1 for the baseline attacker under every host-layer and service-layer mechanism (Figure 5.2(a)), which likely explains why the host layer reduces its NCR although its time lost is at or below zero. For the APT attacker model it is 0.15 to 0.39, likely because its tactic durations put 34 to 57 % of its run in unmapped tactics, where an MTD deployment blocks no attack action (Appendix G.3). Against the APT attacker model, the service layer therefore blocks few attack actions and costs it 60 s or less per deployment, and the host layer likely reduces its NCR through the time it costs.

**Checks:**
- **Facts:**
  - 60 s or less: port shuffle 26, OS diversity −8, service diversity 60.
  - Blocks are from §5.3.1.
  - 34–57 % is from Appendix G.3.
- **The mapped-time share (43–66 %) exceeds 0.35–0.39.** Durations are not the whole cause, hence "likely".
- **Three hedges for three inferred claims.**
- **Terms:**
  - "attack actions blocked per MTD deployment" (§4.5);
  - "unmapped tactics" (§4.3.2);
  - "tactic durations" (§4.4);
  - "time lost".

### 31.5 Marc: "this is a separate, substantive point; what's its purpose, its one-liner? Scrutinise the draft: what's missing, what nuance in or out" (no drafting)

**Purpose.** Figure 5.2 has two panels: attack actions blocked per MTD deployment, and time lost per MTD deployment (§4.5). ¶2 explains only the time lost. The reader is left with two questions:
- the baseline attacker loses no time to the host layer, so why does the host layer reduce its NCR at all;
- where do the tactic durations, the opener's first cause, come in?

**One-liner:**
> An MTD deployment disrupts an attacker in two ways, by blocking its attack action in progress and by the time it then costs: the baseline attacker loses mostly attack actions, and the APT attacker model mostly time, because its tactic durations keep it between attack actions at most deployments.

**Scrutiny of the 31.4 draft:**
1. **The lead is a number, not the point.** "Attack actions blocked per MTD deployment is 0.95 to 1 …" is §5.3.1's sentence form. That is the MTDShield paragraph's fault again: a ch5 rehash where the claim belongs.
2. **No frame.** The draft never says there are two ways to disrupt, or that ¶2 covered one of them, so the paragraph reads as a second list of numbers.
3. **The one-liner is buried in the last clause** ("the host layer likely reduces its NCR through the time it costs"), after a "therefore" chain.
4. **S3 repeats ¶2's 60 s and the opener's layer ordering.**
5. **Three "likely" in 112 words.** Stacked hedges read weak. Restructured, there is one inferred claim (the one-liner) with one hedge; the rest are facts or rules by construction.

**Missing (or nearly overclaimed):**
- **Port shuffle.** Blocks and time lost do not explain why port shuffle (0.91 at 200 s) beats the host layer (0.38–0.68) against the baseline attacker. Blocks are 0.95 against 1, and time lost is −24 s against −14 to −27 s. The paragraph must not claim blocks explain the baseline attacker's service-over-host ordering. The draft did not; v2 must not either.
- **The intervals differ.** Blocks and time lost are measured at 2 000 s (§5.3.1), but the opener's NCR ordering is at every interval. The link is the "likely". This is an examiner risk, but the reader was told 2 000 s in §5.3.1, so it stays off the page.

**Nuance off the page:**
- A deployment during an unmapped tactic still cuts its duration short and costs the confusion penalty (§4.3.2). That is in the time lost.
- The mapped-time share (43–66 %) exceeds the blocks (0.35–0.39), so the tactic durations are not the whole cause. The hedge covers this.
- Service diversity's 493 s for the baseline attacker is in "mostly".

**Nuance on the page:** the 34–57 % (unmapped share of run time). "Most of its run" would be false at 34 %. It is the one fact that ties the tactic durations to the blocks.

**Slots (no prose):**
- **S1, the one-liner (one hedge),** with Figure 5.2.
- **S2, the baseline attacker.**
  - Facts: 0.95 to 1 attack action blocked per deployment under both layers; time lost at or below zero under every mechanism but service diversity.
  - Job: the host layer reduces its NCR through blocks alone.
- **S3, the APT attacker model.**
  - Facts: 0.15 to 0.39 blocked.
  - Job: its tactic durations put 34–57 % of its run in unmapped tactics, where a deployment blocks none (§4.3.2, Appendix G.3).
- **No S4.** The consequence for the service layer is the opener's and ¶2's.

About 90 words.

### 31.6 Marc: "blocks says nothing on which attack actions get blocked: the critical ones, the longest? Knock-on for 6.2's structure?" (no drafting)

**Which attack actions are blocked.** Whichever one is in progress when the deployment completes (disruption_mechanism.md §1). So the longer an attack action runs, the likelier it is blocked; ch4 §4.4 says this ("the longer a tactic runs, the more likely an MTD deployment disrupts it").
- The count says nothing about which attack action or what the block costs.
- No per-attack-action breakdown is in the thesis. It could be computed from the run records, but the argument does not need it.
- Marc's interval reasoning holds: the sweep runs 50–2 000 s, so no lucky alignment explains a result. Blocks and time lost are both measured at 2 000 s.

**What this overturns in 31.5.** Blocks are a count, not a cost. What a block costs (the block, the 20 s penalty and the lost position) is already in time lost. The baseline attacker resumes a blocked attack action in 45–55 s, sooner than its usual gap of 93 s (disruption_mechanism.md table). So:
- **31.5's one-liner is withdrawn:** "the baseline attacker loses mostly attack actions, the APT attacker model mostly time" is a category error. The two metrics are not parallel ways to disrupt; time lost is the cost, and a block is one of its causes.
- **31.5's S2 is withdrawn:** "the host layer reduces the baseline attacker's NCR through blocks alone" has no support. A candidate is §5.3.1's 19–32 s per later deployment (the mean at or below zero is pulled down by the first deployment's second attempt), but it is untested. Keep it off the page; §6.5 holds the first deployment.

**What survives, and the one-liner it gives:**
- The host layer takes the attacker's host at every deployment, whether or not an attack action is in progress (disruption_mechanism.md §1, item 3; ¶2).
- The service layer interrupts an attacker through the attack action in progress (the block), plus, under service diversity, the redrawn vulnerabilities (¶2).
- The baseline attacker always has an attack action in progress (0.95–1). The APT attacker model's tactic durations put 34–57 % of its run in unmapped tactics, so a service-layer deployment blocks one of its attack actions at 15–16 % of deployments.

> **One-liner:** An MTD deployment blocks an attack action only if one is in progress; the baseline attacker always has one, but the APT attacker model's tactic durations keep it out of one at most deployments, so the service layer rarely blocks it, while the host layer takes its host either way.

- **Which comparison it explains (lesson (ad)):** the service layer's weakness against the APT attacker model is now the tactic durations (exposure) plus ¶2's kept ports (60 s). The host layer's strength does not depend on exposure.
- **Not the dishonest throughline.** The service layer gets both causes.

**Structure.** No knock-on.
- The opener names both causes.
- ¶2 is the order of its tactics (what each layer takes and how each attacker gets it back: time lost, adaptivity).
- ¶3 is the tactic durations (whether a deployment catches an attack action in progress: blocks).
- ¶3 does not open "On adaptivity": §4.5 makes time lost adaptivity's metric, and blocks carry no property. The subject (the block) leads.
- Marc: "the structure looks about right".

### 31.7 The package proposed (Marc 2026-10-12, "get that in … propose the changes for ¶1, ¶2 and a draft of ¶3"; not applied)

**The argument in one line (Marc):** the APT attacker model sits in unmapped tactics between attack actions.

- **¶1 (opener): no change.**
  - It names both causes, verbatim from §6.1.
  - Its "likely" is the section's answer-level hedge.
  - ¶2 is the order of its tactics and ¶3 the tactic durations. The order in which the opener names them is §6.1's fixed phrase, so it is kept.
- **¶2: no change.**
  - It ends on service diversity's 60 s, and ¶3 opens on the service layer, so they join.
  - It cites Figure 5.2(b) and ¶3 cites (a), which splits the figure cleanly.
  - ¶2's "fail because their preconditions are missing" is not a block. §4.5 counts only the attack action in progress, at most 1 per deployment, so the two paragraphs do not collide.
- **¶3, draft v1 (≈60 words):**
  > The APT attacker model's tactic durations likely mean that at most MTD deployments it has no attack action in progress, so the service layer rarely blocks one: 0.15 attack actions per service-layer deployment, against 0.95 for the baseline attacker (Figure 5.2(a)). Its unmapped tactics, which run no attack action, take 34 to 57 % of its run (Appendix G.3).
  - **Checks:**
    - "most": 0.15–0.39 blocked under every mechanism, so 61–85 % of deployments catch none;
    - one hedge;
    - the host layer's 0.35–0.39 is left out (¶2 explains the host layer without blocks).
  - **Terms:**
    - "attack action in progress" (§4.5);
    - "unmapped tactics … run no attack action" (§4.3.2);
    - "host-layer deployment" (¶2's form, here "service-layer deployment").
- **Cuts (31.1, 31.2):** the attack-profile paragraph; the old close.
- **§6.4 (downstream):** "would judge the host layer spent far sooner than it is against the APT attacker model, and rely on a service layer that never halves the APT attacker model's NCR (Section 6.2)" becomes "would judge the host layer spent beyond 100 s, though it halves the APT attacker model's NCR up to 1 000 s, and rely on a service layer that never halves the APT attacker model's NCR (Table F.1)".
- **Ch7 Contribution 2 draftnote (gated):** add beside the candidate number: "Tie: Chapter 1's aim of shifting the advantage of time to the defender \citep{ghosh2009nitrd}; against the APT attacker model, the host layer keeps half its NCR off at deployment intervals ten times longer."
- **§6.2 after the change:** the opener, ¶2 and ¶3, about 310 words.

### 31.8 Applied: cuts, §6.4, ch7 (Marc 2026-10-12, "Chapter 7 is fine … downstream is fine"); ¶3 v1 rejected, v2 proposed

**Applied:**
- **§6.2:** the attack-profile paragraph and the old close are cut, replaced by a comment block.
- **§6.4:** "spent beyond 100 s, though it halves the APT attacker model's NCR up to 1 000 s … (Table F.1)".
- **Ch7 Contribution 2 draftnote:** gains the advantage-of-time tie.
- §6.2 is now the opener and ¶2, 238 words. Build clean, 119 pages, 0 undefined.

**Marc on v1:** "vague … not specific … non-standard terms … what does 'at most' mean … 'has no attack action in progress', why say it like that … why the service layer specifically, when the host layer blocks fewer too … so what?"

**Facts checked in the code for v2:**
- **A service-layer ('application') deployment blocks the attack action in progress unless it is scan host, enumerate host or scan neighbours** (`mtd_operation._interrupt_adversary`). The baseline attacker is then sent back to scan port (`attack_operation._handle_interrupt`).
- **A deployment during the APT attacker model's unmapped tactic is felt.** It cuts the tactic duration short and pays the confusion penalty (`attacker._serve_time` → `_pay_interrupt_cost` → `apply_mtd_interrupt_cost`). Under the host layer, that same call clears the host. **So a host-layer deployment takes the APT attacker model's host whether or not it is running an attack action.** That is why the block matters under the service layer and not under the host layer: it answers Marc's "why the service layer specifically".
- **Gap found (ch4, gated):** l.4877, "an MTD deployment during [an unmapped tactic] cuts its duration short and costs the attacker the confusion penalty, but never changes which tactic comes next", omits that under the host layer it also takes the host. Proposed clause: "and, under the host layer, the host it was working on".

**¶3 v2 (≈75 words):**
> The APT attacker model's tactic durations likely explain why the service layer reduces its NCR less than the host layer. Its unmapped tactics, which run no attack action, take 34 to 57 % of its run (Appendix G.3), and an MTD deployment blocks only an attack action in progress (Section 4.5). Attack actions blocked per service-layer deployment is 0.15 for the APT attacker model, against 0.95 for the baseline attacker (Figure 5.2(a)). A host-layer deployment takes its host whether or not it is running an attack action.

**The so-what is S1:** ¶3 explains half of the opener's ordering for the APT attacker model; ¶2 explains the host layer's time lost. The last sentence answers "why the service layer". "At most", "has no … in progress" and "dwell" are gone; the subject is specific (its unmapped tactics). There is one hedge, and "therefore" is avoided because 34–57 % does not account for all of 85 % (the service layer also cannot block the three host-discovery attack actions; that nuance stays off the page).

### 31.9 ¶3 v2 critiqued; v3 from the reader's terms (Marc 2026-10-12, "check all the language … every noun class given in ch1–5 … do we need the appendix, or can 5.2/5.3 supply it?"; proposed, not applied)

**Marc's reading of the argument:**
- the service layer disrupts only an attack action in progress;
- the host layer disrupts indiscriminately;
- the slower APT attacker model, between attack actions in unmapped tactics, is not disrupted by the service layer, while the baseline attacker, always mid-action, is.

**The appendix.** Ch5 cannot supply the time share.
- §5.2 gives the **step** share in unmapped tactics (26–47 %), which is the wrong measure for a deployment that lands at a moment in time.
- Only Appendix G.3 gives the **time** share (34–57 %).
- **Recommendation: drop the number.** The size is carried by Figure 5.2(a)'s 0.95 against 0.15. The rule is the reader's (§2.2.3, §5.3.1). The attribution to tactic durations is the one hedge.

**Term audit (lesson 6: each noun is the reader's own):**

| v2 | Reader's term | Where given |
|---|---|---|
| "an MTD deployment blocks only an attack action in progress" | "A service-layer deployment disrupts it only while it scans ports, exploits or brute-forces" | §2.2.3, near verbatim |
| "takes its host" | "has no host to act on" | ¶2, Appendix F.2 |
| "Its unmapped tactics … take 34 to 57 % of its run" | "runs no attack action while in an unmapped tactic" | §5.3.1 |
| "attack actions blocked per service-layer deployment" | "Under every service-layer mechanism, attack actions blocked per MTD deployment is …" | §4.5 metric name, §5.3.1's form |

**v3 (≈95 words):**
> The APT attacker model's tactic durations likely explain why the service layer reduces its NCR less than the host layer does. A service-layer deployment disrupts an attacker only while it scans ports, exploits or brute-forces (Section 2.2.3). The baseline attacker runs its attack actions back to back, and the APT attacker model's tactic durations keep it in unmapped tactics between them, where it runs no attack action (Section 5.3.1): under every service-layer mechanism, attack actions blocked per MTD deployment is 0.95 for the baseline attacker and 0.15 for the APT attacker model (Figure 5.2(a)). A host-layer deployment leaves the APT attacker model no host to act on whether or not it is running an attack action.

**Checks:**
- **"Back to back":** verified (disruption_mechanism.md, "the baseline is always running an action"); it is plain language, not a coined term.
- **The 0.15 has a second cause:** the APT attacker model's own scan neighbours and enumerate host, which the service layer cannot disrupt. It stays off the page, inside the hedge.
- **The last sentence rests on code** (`_serve_time` → `apply_mtd_interrupt_cost` clears the host). Ch4 l.4877 omits it; the clause proposed in 31.8 is still gated.
- **Hedges:** one "likely" (S1); the rest are measured or true by construction.
- **Not used:** "dwell", "in flight", "hides" and "indiscriminate" (Marc's own words, kept off the page as stand-ins or figurative).

### 31.10 ¶3 v4 (Marc 2026-10-12: "why end on the host layer? reads vestigial … clarity, argument, importance, important part first, plain language, what goes in the hedge, what the reader is given"; proposed, not applied)

**Cut: v3's last sentence** ("A host-layer deployment leaves the APT attacker model no host to act on …").
- The host layer's side of the comparison is ¶2's, so a closing "whereas" re-tells it and reads as vestigial.
- That a host-layer deployment also takes the host during an unmapped tactic stays off the page (code fact). Ch4 l.4877's clause stays gated.

**v3's long third sentence split** into the cause (S3) and the measure (S4). Each sentence leads with its subject:
- the cause;
- the rule;
- the two attackers;
- the measure, the APT attacker model first.

**v4 (≈85 words):**
> The APT attacker model's tactic durations likely explain why the service layer reduces its NCR less than the host layer does. A service-layer deployment disrupts an attacker only while it scans ports, exploits or brute-forces (Section 2.2.3). The baseline attacker runs its attack actions back to back, but the APT attacker model's tactic durations keep it in unmapped tactics between them, where it runs no attack action (Section 5.3.1). Under every service-layer mechanism, attack actions blocked per MTD deployment is 0.15 for the APT attacker model, against 0.95 for the baseline attacker (Figure 5.2(a)).

**Given to the reader:**
- the cause and the comparison (the opener's);
- §2.2.3's rule, near verbatim;
- §5.3.1's unmapped-tactic rule;
- the metric by its §4.5 name, with both numbers.

**Inside the hedge ("likely"), off the page:**
- the APT attacker model's own scan neighbours and enumerate host, which the service layer cannot disrupt (a second cause of the 0.15);
- the 34–57 % time share (Appendix G.3);
- blocks are measured at 2 000 s;
- the host layer takes the host even during an unmapped tactic.

**Checks:**
- "Less than the host layer does" holds per mechanism at every interval: each host-layer mechanism exceeds each service-layer mechanism against the APT attacker model (Table F.1), so it is not only a layer mean (lesson (ac)).
- There is no "therefore" before the numbers, because the second cause exists.

### 31.11 ¶3 applied after a final clarity pass; full §6.2 pass (Marc 2026-10-12, "put it in … has 6.2 done its job: answer SQ3, engage with 5.3 constructively?")

**Clarity pass on v4.** One fix: "keep it in unmapped tactics between them, where it runs no attack action". "Them" pointed at the baseline attacker's attack actions, and "attack action" came twice.
> … but the APT attacker model's tactic durations keep it between attack actions, in unmapped tactics that run none (Section 5.3.1).

The contrast with "back to back" now comes first. Applied. §6.2 is 327 words. Build clean, 119 pages, 0 undefined.

**Does §6.2 answer SQ3?** Yes, in the first sentence, in the question's terms (both attackers, the MTD layers, every deployment interval), with both causes named. Each later paragraph says which cause it carries:
- ¶2 is the order of its tactics: host-layer time lost, Figure 5.2(b).
- ¶3 is the tactic durations: the service layer's blocks, Figure 5.2(a).

**Does it engage §5.3 constructively?** Each of §5.3's results is either explained here or sent once to its owner:

| §5.3 result | Where it is handled |
|---|---|
| §5.3.1, Figure 5.2(a) blocks | ¶3, why |
| §5.3.1, Figure 5.2(b) time lost | ¶2, why |
| §5.3.1, the first deployment's second attempt | §6.5 |
| §5.3.2, the layer ordering across intervals (Figure 5.3) | the opener |
| §5.3.2, what the interval means | §6.4 |
| §5.3.2, the ranking and ρ | §6.4 |
| §5.3.2, deployment strategies and MTDShield | §6.4 ¶2 |
| §5.3.2, user shuffle | Appendix F.3, via §6.4 |
| §5.3.3, attack profiles | §6.1 and §6.3 |

**Inbound references still met:**
- §6.4: time lost at or below zero; service diversity, the only mechanism the baseline attacker loses time to.
- §6.5: Lateral Movement.
- Appendices F.2 and F.4: the host-layer mechanism.
- The ch7 draftnote's "no MTD mechanism ranks first against both (Section 6.2)" is not met here. Its repoint to §5.3.2/§6.4 is still gated.

**The one gap: the baseline attacker's half of the opener.**
- The section explains the APT attacker model's ordering fully. For the baseline attacker it explains only service diversity (493 s).
- Port shuffle and OS diversity beat the host layer against the baseline attacker at 200 s (0.91 and 0.68 against 0.38–0.68), yet cost it no time (−24, −58 s), and blocks are alike (0.95 against 1).
- **Candidate cause (untraced):** a block sends the baseline attacker back to scan port and erases its exploit progress on the host, which at short intervals it cannot rebuild between deployments. disruption_mechanism.md §1 gives "exploit progress erased" for the service layer.
- **Recommendation:** no edit.
  - The opener's causes explain "the difference between the two attackers", and the baseline attacker's own ordering is MTDSim's rules (§2.2.3) measured in ch5.
  - Log it as a cold-examiner question; if it is asked, the answer is §2.2.3's rule plus the trace.
  - Alternative: one hedged clause in ¶3 ("and sends it back to scan port"). But ¶2 already gives that rule for service diversity, and the size claim is untraced.

**Still gated (ch1–5):**
- ch4 l.4877: add "and, under the host layer, the host it was working on";
- ch2 l.957: "its place" → "the attack action in progress and, under the host layer, the host it was working on";
- the ch3/ch4 "pace" fixes.

### 31.12 The gated ch2/ch4/ch5/ch7 edits, reworked in context (Marc 2026-10-12, "put in the hard work … in the context of the actual paragraphs"; proposed, not applied)

**ch2 l.957 (§2.2.3, the disruption paragraph).**
- **Problem:** "its place" is a Petri net term. The sentences before it already say where each deployment sends the attacker, so the loss is the work it must redo. That is Marc's word, progress.
- **Proposed:** "A deployment never takes back a compromised host or a stolen credential \citep{zhang2023}; the attacker loses only the progress it must repeat, and a topology shuffle also rebuilds its visible subgraph."
- The host-layer sentence ("sends it back to scanning hosts, because the host it was on may have moved") already gives the host loss that ¶2 cites. No change there.

**ch4 l.4877 (§4.3.2, after the unmapped-tactic gaps).**
- **Problem:** the paragraph omits that a host-layer deployment during an unmapped tactic costs the APT attacker model the host it was on (code: `_serve_time` → `apply_mtd_interrupt_cost`). ¶2's "neither attacker has a host to act on" and ¶3's reasoning rest on it.
- **Proposed:** split into the rule, then what a deployment does, in ch2's words ("the host it was on"):
  > An unmapped tactic runs no attack action, so it cannot fail. An MTD deployment during it still cuts its duration short and costs the attacker the confusion penalty, and a host-layer deployment also costs it the host it was on (Section 2.2.3), but no deployment changes which tactic comes next.
- "No deployment changes which tactic comes next" stays true: no verdict, base weights.

**ch4 l.4969 (§4.4, the judgement-set durations).**
- **Problem:** "single acts that the attacker paces to stay hidden, so we set them at 22.5 s, half the 45 s and longer than an exploit". "Pace" is banned, and the two reasons are joined to the two bounds without saying which is which.
- **Proposed:** one reason per bound:
  > Execution and Defense Impairment are single acts, so we set them at half the 45 s, 22.5 s, still longer than an exploit because the attacker slows them to stay hidden.

**ch5 l.6198 (§5.1, ablation studies).**
- **Problem:** "what takes each component's place" uses "place" outside the Petri net sense.
- **Proposed:** "Table 5.1 gives what replaces each component and the configurations each ablation study runs."
- The idiom "in place of" (ll. 556, 5547, 6109; §6.1 ll. 8553, 8627; ch7 9745) is "instead of", not a position. Recommend keeping it; it is not the noun.

**ch7 draftnote l.9718 (Preamble, "The answer in MTDSim").**
- **Problems:**
  - "No MTD mechanism ranks first against both … (Section 6.2)" points at text that was cut.
  - Its first sentence ("the host layer disrupts the APT attacker model more, and the service layer less") is not §6.2's answer: it is in "disrupts", not NCR reduction, and it omits the baseline attacker's half.
- **Proposed:**
  > MTD performs differently against the APT attacker model than against the baseline attacker, and the difference runs by MTD layer: the host layer reduces the APT attacker model's NCR more than the service layer does, and the service layer the baseline attacker's (Section 6.2). No MTD mechanism ranks first against both attackers at any deployment interval (Section 5.3.2).

## 32. §6.3 (Properties of the APT attacker model): heavy scrutiny of the overdraft (Marc 2026-10-12; nothing applied)

Marc: "no rhyme or reason … reads like a concatenation of dot points … what is 6.3 doing that 6.1, 6.2 and chapter 3's marks can't? What is relevant for discussion, what floats to the appendix? Is the title right? Is Table 6.1 presented properly?" No redraft.

### 32.1 Measured

§6.3 is 1 235 words in four paragraphs (271 / 350 / 322 / 292) plus Table 6.1, against §6.1 492 and §6.2 327. Unchanged since the overdraft.

### 32.2 Diagnosis: why it reads as a list

1. **No question owns it.** It names SQ1 and SQ2 twice (¶1 "In answer to", ¶4 "To … then") and answers neither in its own terms. SQ1 and SQ2 ask *how*; Chapter 4 is the how. The discussion's job is how well: what recovering from threat reports carried and lost (SQ1), and what executing in an existing simulator capped (SQ2). ¶1 answers "how many marks", and ¶4 re-describes Chapter 4's pipeline.
2. **Four paragraphs, four jobs, none building on the last:**
   - ¶1 is the scoring procedure (method and validity);
   - ¶2 is a ch3-style per-mark walk (Chapter 4's claims, in Table 3.3's paragraph format);
   - ¶3 attributes the SQ3 result to components (§6.2's and §6.5's job);
   - ¶4 recaps all three and gives a CTI verdict.
3. **Most sentences live elsewhere already** (§32.3). What is left that only §6.3 can say is about four sentences.

### 32.3 Sort test (cut = lives elsewhere or nowhere)

| Content | Already in | Verdict |
|---|---|---|
| ¶1 S1: 2 full, 3 in part, field ≤1 full | only here | **Keep**: Table 6.1's headline, the SQ1/SQ2 evidence |
| ¶1 S2: gains over the baseline attacker (3, 2, 5) | §6.1 opener (the same three properties); ¶4 repeats it; ch7 draftnote | Keep once (it is said twice in §6.3) |
| ¶1 S3–S8: rule fixed first, tightened, each model from its source, runs lower never raise, "we first marked what it implements", four LMs plus a fifth | ch3 §3.x; App clause-tests; §6.5 construct (l.9356); AI Use Declaration | **Cut**: method and validity, not discussion. "We first marked…" is process history. |
| ¶2 S1: every mark short of full stops at the attack actions or a decision no part makes | only here | **Keep**: the SQ2 answer |
| ¶2 persistence keeps the baseline attacker's loop | ch4 opener l.3891 | Cut |
| ¶2 choice: the Petri net draws, the run joins flows | §6.1 ¶2 | Cut |
| ¶2 emulation vs simulation | ch3 §evaluation-methods | Cut |
| ¶2 one token = the same draw as a stochastic finite state machine; the source, not the formalism | only here | **Keep**: an SQ2 point, honest about what the Petri net buys |
| ¶2 objective-specific: AoO unmapped, same six attack actions | §6.1 ¶1 | Cut |
| ¶2 the baseline attacker has none | ch3 baseline paragraph | Cut |
| ¶2 failure matrix reads only the verdict | ch4 l.5150 | Cut |
| ¶2 detection avoidance: durations, proxy, no IDS | §6.1 ¶3, near verbatim | Cut |
| ¶2 three it lacks: RoA, memory keeps vulnerabilities, no schedule | ch3 baseline paragraph word for word; ch4 l.5233 | Cut |
| ¶2 last: persistence by construction; adaptivity's metric does not resolve the component | measurement validity | §6.5 construct, or cut |
| ¶3 §5.4 results: failure matrix and time lost, same three mechanisms, d −0.76 vs −0.28 | §5.4 verbatim | Cut (rehash of ch5) |
| ¶3 "reversal rests on durations and order, not FM / memory / profiles" | §6.1 opener, §6.3 ¶4, §6.4 ¶3, §6.5 ¶1 and ¶2: **six statements in ch6** | One home (Q3) |
| ¶3 "NCR reduction, not NCR … stronger, not closer" | nowhere | Cut (not-X-but-Y twice); the idea is §6.4's if anywhere |
| ¶3 "a negative only a model with the mechanism can report" | nowhere | Cut (rhetorical) |
| ¶3 attack graph pools objectives; profiles beat random partitions | §6.1 ¶1, §5.4, ¶4: three times in ch6 | Keep once, in the SQ1 answer |
| ¶3 the Petri net has no ablation | §6.5 ("Order has no test of its own") | Cut |
| ¶4 S1 "To SQ1 and SQ2, then." | n/a | Cut (rhetorical) |
| ¶4 the pipeline recap | ch4 opener; ch7 Contribution 1 | One clause at most |
| ¶4 "differ only in which AoO they take" | §6.1 ¶1 says "no more differently than random groups" | **Stale and an overclaim**: they do differ before AoO (TV 0.17–0.37), only not more than random groups |
| ¶4 "three of four rest on 5 to 7 flows" | §6.5 | Cut (bounds once, in §6.5) |
| ¶4 "a mark in full means every predicate … upgrades within in part don't show" | only here | Keep, one clause: the honest reading of Table 6.1 |
| ¶4 "what reorders the MTD mechanisms is order … and the tactic durations" | §6.2 opener, which hedges it "likely" | Unhedged here: inconsistent |
| ¶4 "Grounding in CTI therefore changes what an MTD evaluation finds" | §6.4 says the results do *not* show "that the grounding in CTI caused the reversal"; §6.5 says order has no test with MTD | **Contradiction** (§32.4) |

### 32.4 Substantive problems (beyond length)

1. **The CTI verdict contradicts §6.4 and §6.5, and its own logic.** Of the two causes it names:
   - the tactic durations are our judgement, not CTI (§6.5);
   - the order of its tactics, the CTI part, has no run with MTD that separates it (§6.5).

   So "therefore changes what an MTD evaluation finds" does not follow. At most: likely, through the order of its tactics, which is untested under MTD. Ch7's Contribution 1 "Bound" draftnote carries the same claim (gated).
2. **Inconsistent scorer account.** ¶1 says four language models scored, plus a fifth. §6.5 l.9356 says "one scorer … with a language model's blind re-score as the check". One of them is stale.
3. **Not-X-but-Y count: about 7.** "not the patterns", "not from the formalism", "not which technique", "NCR reduction, not NCR", "stronger, not closer", "not which component pays it", "not from the reweighting".
4. **The ablation-negligible claim** is stated six times across ch6 (§32.3). §6.4 ¶3's "(Section 6.3)" pointer depends on where it lands.

### 32.5 Title

"Properties of the APT attacker model" names the yardstick, not a comparison. It reads as a ch4 heading, and it breaks the §6.1 / §6.2 pattern ("X versus Y"). The one thing only this section has is Table 6.1: the APT attacker model against the field of Chapter 3.

- **Recommend:** "APT attacker model versus MTD attacker models". It mirrors §6.1 and §6.2, uses ch3's term, and names the float.
- **Alternative:** keep it, if the section's spine becomes SQ1/SQ2 rather than the table.

### 32.6 Table 6.1

- Its placement (head of section) and its sync with Table 3.3 are right.
- **Problems:**
  - The abbreviated column heads ("Pers.", "Strat.", …) are decoded nowhere in the caption. Table 3.3 has the same issue (results presentation standard: the caption must decode).
  - "from Chapter 4" in the caption is ambiguous: it means scored from Chapter 4's description.
  - The prose never tells the reader where to look in the table (the APT row against the column maxima, rows 1 and 4).
- **Option:** ¶2's 350 words exist mainly to annotate cells. A one-line note under the table could carry "stopped by: the attack actions (2, 4, 5) / no decision (6, 7, 8)" and free the prose. This is a presentation choice for Marc.

### 32.7 What only §6.3 can do (the motivated structure)

- **6.1** explains the three measured properties against the baseline attacker.
- **6.2** explains SQ3.
- **Ch3** owns the rule; **ch4** owns why each component gives its property.
- **Only 6.3** can (a) set the model against the field, (b) say what recovery from threat reports carried and lost (SQ1), (c) say what execution in an existing simulator capped (SQ2), and (d) say which marks reach SQ3's result.

Proposed (no prose; job and takeaway; about 350–450 words in all):

- **Opener: the answer, from Table 6.1.**
  - Job: answer SQ1 and SQ2 in their own terms with the table as evidence: recovered as attack flows → attack graph → attack profiles; executed as a Petri net over MTDSim's six attack actions; 2 full, 3 in part, the field ≤1 full.
  - Takeaway: *the recovered behaviour runs, and it closes more of the gap than the field.*
- **¶2, SQ1: what threat reports carry, and what they don't.**
  - They carry the order of tactics (choice of attack strategy, the full mark), and grouping by objective carries structure (beats random partitions; said once).
  - They carry no tactic durations, failure response or memory (judgement).
  - They record actions on objectives that MTDSim cannot run.
  - Takeaway: *threat reports give the order of an APT's tactics, not their timing.*
- **¶3, SQ2: what an existing simulator caps.**
  - Every mark short of full stops at the attack actions or at a decision no part makes.
  - With one token, the Petri net draws what a stochastic finite state machine would: the source, not the formalism, gives the choice.
  - Takeaway: *executed in an existing simulator, the model is capped by its attack actions.*
- **Close: which marks reach the result.**
  - The components that bought in-part marks (failure matrix, vulnerability memory, attack profiles) leave the ranking unchanged. What reaches SQ3 is the order of its tactics (CTI, choice of attack strategy) and the tactic durations (judgement, detection avoidance in part).
  - Hedged to agree with §6.4/§6.5: likely, through the order of its tactics, untested under MTD.
  - Takeaway: *of what CTI adds, likely only the order of its tactics reaches the result.*

**Moves out:**
- scoring procedure → App clause-tests, §6.5 construct (reconciled), AI Use Declaration;
- per-mark justifications → already in ch4;
- §5.4 numbers → §5.4;
- the bounds (5–7 flows, judgement values) → §6.5.

### 32.8 Questions (recommendation first)

1. **Title:** "APT attacker model versus MTD attacker models" (recommended), or keep it.
2. **The scoring procedure leaves §6.3** for the appendix and §6.5, keeping only "by Chapter 3's rule" (recommended). Also: which scorer account is current, ¶1's or §6.5 l.9356's?
3. **One home for "the failure matrix and vulnerability memory move NCR negligibly":**
   - recommended: §6.5 internal validity owns the attribution;
   - §6.3 says it once in mark terms;
   - §6.1's opener (no MTD) stays;
   - §6.4 ¶3's pointer is repointed to §6.5.
4. **The CTI verdict is softened** to agree with §6.4 and §6.5 (recommended). The ch7 Contribution 1 "Bound" follows; ch7 is gated.
5. **Table 6.1:** decode the column abbreviations in the caption (and Table 3.3's, which is gated). Optionally add a "stopped by" note in place of ¶2.

## 33. §6.3 rulings applied; SQ1 losses checked against the corpus; slot sheet (Marc 2026-10-12)

### 33.1 Rulings ("100 % agree"; Q1–Q5 yes)

- **Q1 title:** "APT attacker model versus MTD attacker models". **Applied.**
  - Marc asked whether §3.3.1 should mirror it. Recommended no: §3.3 is already titled "MTD attacker models", so §6.3's title mirrors ch3 through that term.
  - Chapter 3 has no APT attacker model to set "versus" against, and it is gated.
- **Q2:** the scoring procedure leaves §6.3; only "by Chapter 3's rule" stays.
  - The appendix (l.9913–9926) gives four language models plus a fifth, as §6.3 ¶1 does, so §6.5 was the stale one.
  - **Applied:** §6.5 now reads "with language models scoring blind as the check (Appendix clause-tests)", pointing at the appendix in place of §6.3.
- **Q3:** one home for "the failure matrix and vulnerability memory move NCR negligibly". **Applied as repoints:**
  - §6.4 ¶3 → Section ablation;
  - §6.5 internal validity → Section ablation;
  - §6.5 limits ("the reversal rests on the tactic durations and order") → §6.2.
  - §6.3 will say it once, in mark terms, in its close.
  - Flag: that §6.5 limits sentence is unhedged against §6.2's "likely". Not touched.
- **Q4:** the CTI verdict is softened to agree with §6.4 and §6.5. The ch7 Contribution 1 "Bound" follows (approved); it is applied when §6.3's close is drafted.
- **Q5:** Table 6.1's caption decodes the eight column numbers, and "from Chapter 4" is now "as Chapter 4 describes it". **Applied.** Table 3.3 is unchanged (Marc: clear beside Table 3.2).
- Build clean, 119 pages, 0 undefined. Other pointers to §6.3 stay valid after the redraft:
  - ch7 future-work (attack actions);
  - Appendix clause-tests (the stochastic finite state machine);
  - Appendix fa-group-size (random partitions).

### 33.2 Marc's SQ1 content, checked (the 38 STIX bundles, data/gap/_corpus_stix; code src/mtdsim/l3_simulation/petri/build.py)

**What the attack flows carry, and the model keeps:**
- the order of steps (tactic to tactic);
- through the attack profiles, which order goes with which objective.

Marc's gain: plausible objective-driven sequences of attack behaviour, reusable, plugged into MTDSim.

**What they carry and the model drops:**

| Lost | In the corpus | Where the reader has it |
|---|---|---|
| Techniques → tactics | 124 techniques → 15 tactics | ch4 §4.2 |
| Procedures (the tools and malware used) | tool 119 in 24 flows, malware 91 in 22 | nowhere (new; plain words suffice) |
| Vulnerabilities | 24 in 16 flows; MTDSim's synthetic vulnerabilities used | nowhere |
| How steps combine | operators 78 in 30 flows (AND 64, OR 14); conditions 143 in 27 flows | Figure 2.x shows an OR and a condition; no prose anywhere. The GAP keeps the joins as edge metadata, but the attack graph counts each step as its own edge, and build.py reads no operator. ch4's single-token sentence covers parallel branches only |
| Actions on objectives | recorded; unmapped | §6.1 ¶1 |

**What they almost never carry** (judgement fills it):
- timing (ch2: "almost never");
- the response to a failure (attack flows record what happened).

**Correction:** mitigations are not a loss. There is one course-of-action object in one flow, because attack flows record the attack, not the defence.

**Antecedent:** AND/OR and conditions need a home before §6.3 can name them. Either plain words in §6.3, or a gated ch4 §4.2 clause. Proposed, not applied:

> Where an attack flow joins steps with AND or OR, or records the condition a step leaves (Figure 2.x), the attack graph keeps each step as its own edge and drops the join and the condition.

### 33.3 Slot sheet (job · facts · ceiling); about 420 words against 1 235

**Opener (about 70)**
- **S1, the SQ1 and SQ2 answer in their "how":** recovered from 38 attack flows as an attack graph, split by objective into four attack profiles; executed in MTDSim as a Petri net over its six attack actions. *Ceiling:* nouns only, no ch4 recap.
- **S2, Table 6.1's evidence:** 2 in full, 3 in part, lacks 3, against at most 1 in full for the three MTD attacker models; over the baseline attacker it gains 3 in full, and 2 and 5 in part. *Ceiling:* "by Chapter 3's rule", no procedure.

**¶2, SQ1: what the threat reports carry and lose (about 150)**
- **S1, the claim:** the attack flows give the order of an APT's tactics, and grouping them by objective carries structure (beats random partitions with no MTD). *Ceiling:* one hedge on "plausible"; no §6.1 numbers.
- **S2, what is lost to make it run, in three groups:**
  - what the attacker used: procedures, vulnerabilities, techniques → tactics;
  - how steps combine: AND/OR joins, conditions;
  - what it achieved: actions on objectives.
  
  *Ceiling:* one sentence; counts only if Marc wants one.
- **S3, what the reports never had:** timing and the response to a failure, so tactic durations and the failure matrix are our judgement. *Ceiling:* point to §6.5, no bound restated.
- **S4 (optional HYP), the so-what:** the attack actions' own preconditions stand in for the conditions the flows record. Likely why 15–30 % of attack actions fail (§6.1 ¶2); keeping the conditions is future work. *Ceiling:* one "likely".

**¶3, SQ2: what an existing simulator caps (about 110)**
- **S1, the claim:** every mark short of full stops at MTDSim's attack actions (2, 4, 5) or at a decision no part of the model makes (6, 7, 8). *Ceiling:* name, don't explain (ch4, §6.1).
- **S2, the formalism:** with one token, a stochastic finite state machine built from the same attack flows would make the same draw; the choice comes from the attack flows. *Ceiling:* no not-X-but-Y.
- **S3 (optional):** a mark in full needs every predicate, so improvements inside a mark in part (the failure matrix, the vulnerability memory) do not show in Table 6.1.

**Close: which marks reach the result (about 90)**
- **S1:** the components behind the in-part marks leave the result unchanged: the failure matrix and the vulnerability memory move NCR negligibly; without the attack profiles the same three MTD mechanisms reduce NCR the most (§5.4). *Ceiling:* no d values.
- **S2:** what likely reaches SQ3's result is the order of its tactics (from the attack flows; choice of attack strategy) and the tactic durations (our judgement; detection avoidance in part), as §6.2.
- **S3, the CTI verdict:** grounding in CTI likely reaches the result only through the order of its tactics, which no run with MTD tests alone (§6.5). This agrees with §6.4's "nor that the grounding in CTI caused the reversal".

## 34. §6.3 first redraft on the board (Marc 2026-10-12, "first draft on the board … then I can work through each paragraph")

- **Applied** from the §33.3 slot sheet. The overdraft is at 2b6ddfc1.
- **Size:** 1 235 → 520 words (−58 %). Paragraphs: opener 104, SQ1 170, SQ2 147, close 99.
- **Rulings used:**
  - ¶2 keeps the preconditions point, hedged once.
  - Plain words, no ch4 clause: "steps an attack flow requires together"; "conditions" is given in ch2's attack-flow definition.
  - Chapter 3 is left alone.
- **New in ¶3, from ch4 §4.3:** "a transition is enabled only when each of its input places holds a token", which is an AND. So the Petri net could carry the AND joins and the conditions. Built with one token and a place per tactic, it uses neither, so the choice comes from the attack flows. This replaces the stochastic finite state machine sentence, which had no antecedent in ch1–5. Appendix clause-tests still says it, pointing here.
- **ch7 Contribution 1 "Bound"** is in step with the close (Q4, approved).
- **Flagged for Marc's paragraph rounds:**
  - Is adaptivity really stopped "at MTDSim's attack actions"? (The failure matrix reads the attack action's verdict, which cannot tell an MTD-caused failure.)
  - "Three of the components … barely move the result": the vulnerability memory adds no mark.
  - The close's two hedges, one claim leaning on the other.
  - Marc: some of the discussion he gave earlier may not have reached §6.3; to be found after this read.
- Build clean, 118 pages, 0 undefined.

## 35. §6.3 structure, second look: the table's job and one question per paragraph (Marc 2026-10-12; nothing applied)

Marc, on the first draft: the opener has no clear purpose (it recaps ch4, then counts marks); it answers two sub-questions at once; nothing says how the APT attacker model got its marks; Table 6.1 is "answered in 6.1 and 6.2, we don't really use it here". Should the row go into ch3's Table 3.3 instead?

**35.1 Where Table 6.1 lives: keep it in §6.3.**
- ch3 scores the field to motivate the gap; a row for a model ch4 has not yet defined is a forward reference and a claim before the method. Marc ruled ch3 left alone (§33 Q1).
- The marks are scored from ch4 (appendix clause-tests), but the counterpoints that make 2, 4 and 5 "in part" cite §6.1's evidence (Appendix fa-run-time, fa-behaviour-actions). The verdict needs the discussion.
- Fairness: the same predicates, applied to our model from ch4 by its builder. That bias is §6.5's construct threat (blind language-model check), not a reason to move the table.
- Repeating three rows from Table 3.3 is the cost of setting the columns side by side.

**35.2 The table's job in §6.3: say where each mark comes from.** §6.1 and §6.2 explain the *measured* differences on properties 2, 3, 4 and 5; nothing in ch6 says why each mark is full, in part or none. The appendix predicate cells already give it:

| Property | Mark | Cell | Source of the mark | Why not full |
|---|---|---|---|---|
| 1 campaign persistence | full | yes | MTDSim's loop, kept | — |
| 2 objective-specific | in part | assumed | attack flows: different tactics after the foothold per objective | MTDSim has no attack action for Collection, Exfiltration or Impact |
| 3 choice of strategy | full | yes | attack flows + Petri net draw at runtime | — |
| 4 adaptivity | in part | rule | failure matrix, our judgement | the reports never record a response to failure; the attack action's verdict does not say MTD caused it |
| 5 detection avoidance | in part | rule, no | tactic durations, our judgement | the reports almost never record timing; MTDSim has no IDS |
| 6, 7, 8 | none | no | no part of the model | left out of scope |

So: the threat reports give the full mark (3) and the behaviour of 2 (SQ1); every in-part mark is in part because our judgement or the simulator fills what the reports do not record (SQ1) or cannot execute (SQ2). This uses the table and answers "how do we get those markings" without rehashing §6.1/§6.2.

**35.3 One question per paragraph.**
- **Opener (the title's comparison, about 60 words):** the APT attacker model against the field: two in full and three in part against at most one in full, by the same predicates; the only one with objective-specific behaviour; gains over the baseline attacker. Drop the ch4 recap ("recovered… aggregated… executed"), which ch4's opener already claims as its answer to SQ1 and SQ2.
- **¶2, "In answer to SQ1" (about 130):** threat reports yield the order of an APT attacker's tactics by objective. That gives 3 in full and the behaviour of 2. What else they record is dropped to run (procedures, vulnerabilities, AND joins, conditions). What they almost never record (timing, response to failure) is our judgement, which is why 4 and 5 are in part.
- **¶3, "In answer to SQ2" (about 110):** an existing simulator keeps campaign persistence and caps 2 (no attack action for actions on objectives) and 5 (no IDS). The Petri net could carry AND joins and conditions but, built with one token, uses neither. 6, 7 and 8: no part of the model.
- **Close (about 80):** which marks reach SQ3. Keep, but fix "three of the components" (the vulnerability memory backs no mark) and the leaning hedge.
- Estimated about 380 words, from 520.

**35.4 Cuts and fixes found.**
- ¶2's "likely explains why 15 to 30 % … fail" duplicates §6.1 ¶3, which states it as measured (Appendix fa-run-time l.~10810). Cut from §6.3; the hedge was wrong too.
- ¶2's "the attack profiles compromise more than random partitions" pulls against §6.1 ¶2 (steps divided no more differently than random groups). It answers neither sub-question; cut, or Marc places it in §6.1.
- ¶3's "a mark in full needs every predicate … within a mark in part" becomes redundant once 35.2 names why each mark is in part.
- **Stale pointer:** the appendix counterpoints row "APT attacker model, 3: yes" cites "a stochastic finite state machine … (Section 6.3)", which §6.3 no longer says. Repoint or reword with the redraft (appendix: auto).
- Adaptivity flag (§34) resolved by the cell: the mark is "rule" because the failure matrix is our judgement, with the simulator's verdict a second reason. ¶3's "stops at MTDSim's attack actions, for … adaptivity" is wrong as written.

## 36. §6.3: where the source of each mark goes (Marc 2026-10-12; nothing applied)

- **Marc's sort, as given:**
  - campaign persistence: inherited from MTDSim;
  - objective-specific behaviour: the attack flows split by objective into attack profiles;
  - choice of attack strategy: the attack flows;
  - adaptivity: the failure matrix, set by our judgement;
  - detection avoidance: the tactic durations;
  - 6, 7 and 8: not modelled.
  This agrees with the appendix cells (§35.2).
- **Prose, no new table.**
  - Table 6.1 must keep Table 3.3's layout (round 50).
  - The appendix already scores the APT attacker model predicate by predicate (Table clause-tests, its column, and the counterpoints rows).
  - A second table would be a third copy of the marks.
- **The sort falls along the sub-questions:**
  - ¶2 (SQ1): what the reports give (3 in full, 2's behaviour) and what our judgement fills (4, 5);
  - ¶3 (SQ2): what the simulator gives (1) and caps (2, 5), and what is not modelled (6–8).
  - One clause per source, never a sentence per property.
- **Why the overdraft's ¶2 was cut (§32.3):** it walked property by property, and each justification already lived in ch4, §6.1 or ch3 (rows "Cut: lives elsewhere"). Space was not the reason. The walk never sorted marks by source, which is what is missing; the sort adds no new evidence.
- **Order:** §6.2 (SQ3) comes before §6.3 (SQ1, SQ2) because §6.3's marks rest on §6.1's evidence and its close reads which marks reach SQ3's answer. Keep it; the ch6 opener already states the order. Within §6.3, SQ1 comes before SQ2.
- **§6.1/§6.2:** no update needed; their sources (tactic durations, attack profiles) agree.

## 37. §6.3 second redraft on the board (Marc 2026-10-12, "I approve this, let's do this")

- **Applied:** the plan of §35–§36. Each mark is sorted by its source, along the sub-questions.
  - **Opener:** the comparison with the field. The Chapter 4 recap is gone. The opener now carries 6, 7 and 8 ("no part of it chooses a technique by its cost, keeps the patterns of MTD deployments or predicts the deployment strategy"). This is a field-level point (none of the four has them), so it sits in the opener, not in the SQ2 paragraph.
  - **¶2 (SQ1):** the order of tactics by objective gives 3 in full and 2. The losses are listed. Timing and the response to failure are set by judgement, so 4 and 5 are in part.
  - **¶3 (SQ2):** the simulator gives 1 and caps 2 (actions on objectives unmapped) and 5 (no IDS). The Petri net could carry the AND joins and the conditions but uses neither.
  - **Close:** two marks likely reach SQ3. Each ablation is now tied to its mark: the failure matrix behind adaptivity, the attack profiles behind objective-specific behaviour. The vulnerability memory is dropped (it backs no mark), and the last sentence carries its own "likely".
- **Cut:**
  - the 15–30 % sentence (§6.1 ¶3 has it as measured);
  - the random-partition sentence;
  - "a mark in full needs every predicate…".
- **Appendix counterpoints, row "APT attacker model, 3":** the stochastic-finite-state-machine pointer to §6.3 now reads "fixed weights, set before the run from the attack flows (Section petri-formalism)". One comment-only mention is left at l.~9549.
- **Size:** 520 → 512 words (opener 99, SQ1 176, SQ2 148, close 89). The ~380 estimate of §35.3 did not hold: the source sentences replaced the cuts word for word.
- Build clean, 118 pages, 0 undefined.

## §38. §6.3 opener: clarity pass (Marc 2026-10-12)

**One-liner.** The APT attacker model has more of the eight properties than any MTD attacker model; all four lack 6–8.

**Split of work, caption against opener.**
- The caption carries the column decode, the mark legend and "by the same rule". It now also carries the appendix pointer: "Appendix A tests each mark predicate by predicate." (Applied.)
- The opener carries only the comparison with the field.
- Neither carries: the predicates; the gain over the baseline attacker (the rows sit side by side, and ¶2–¶3 say what is kept and what is added; Marc: "easy", cut); the gloss of 6–8 (it restates Chapter 3).
- No hedge: we scored the marks ourselves, so the opener states them with authority. Scorer bias is covered once, in §6.5.

**Marc's critique of the first proposal** ("two in full, where none of them has more than one, and objective-specific behaviour, which none of them has. Like them, …"):
- the clauses stack;
- the argument oscillates between the APT attacker model and the three;
- "them" is hard to resolve.

**Fix.** One claim per sentence, with the subject named first. The APT attacker model's claims come together, then the claim about all four, with no pronoun pointing back at the three.

**Proposed (not applied; the paragraph being drafted is proposed first):**
> The APT attacker model has more of the eight properties than any of the three MTD attacker models (Table 6.1). It alone has two in full, and it alone has objective-specific behaviour. All four attacker models lack cost–benefit reasoning, learning and deployment-strategy awareness.

Build clean, 118 pages, 0 undefined.

## §39. §6.3 opener applied (Marc 2026-10-12)

**Marc on the §38 proposal:**
- "which three": name the section the three come from;
- "it alone… it alone" is a rhetorical mirror;
- objective-specific behaviour is only in part;
- in sentence two, the reader has to infer which two properties are "in full".

**Fix.** Sentence two now names the two marks no other attacker model has:
- choice of attack strategy in full (the baseline attacker has it in part);
- any objective-specific behaviour.

Campaign persistence in full is shared with the baseline attacker, so counting "two in full" did not mark a difference. A third sentence giving the shared marks (persistence, adaptivity, detection avoidance) was proposed. Marc cut it, because the table shows those marks and the opener points only to what matters.

**Applied (46 words, from 99):**
> The APT attacker model has more of the eight properties than any of the three MTD attacker models of Section 3.x (Table 6.1). It is the only attacker model with choice of attack strategy in full or with any objective-specific behaviour, which it has in part. All four attacker models lack cost–benefit reasoning, learning and deployment-strategy awareness.

§6.3 now totals about 459 words. Build clean, 118 pages.

## §40. Table 6.1 caption trimmed (Marc 2026-10-12, approved)

**Cut:**
- "as Chapter 4 describes it": by §6.3 the reader knows where the model comes from;
- "scored … by the same rule": Table 3.3's caption names no rule, so the phrase pointed at nothing.

**Pointer made plain:** "Appendix B gives the reasoning behind each mark". This replaces "tests each mark predicate by predicate"; the predicates are Appendix B's business.

**Kept:**
- the rows (copied from Table 3.3);
- the properties of Table 3.2, with the 1–8 decode (the length that cannot be cut);
- the mark legend.

**Note:** the clause-tests appendix is Appendix B. Appendix A is the original proposal. §38–§39 and chat said "Appendix A"; the LaTeX uses `\ref` throughout and was always right.

Build clean, 118 pages, 0 undefined.

## §41. §6.3 ¶2 (SQ1): scrutiny of the text on disk (Marc 2026-10-12; nothing applied)

Marc: "does it directly answer the question, engage all the clauses … threat reports give the model … but there are still limitations … criticise what's on disk, no redraft." ¶2 is 176 words, eight sentences.

**One-liner it should carry:** the attack flows drawn from threat reports give the model which tactic follows which, and which actions on objectives go with each objective; we set the timing and the response to failure ourselves.
**Purpose:** the source of marks 3, 2, 4 and 5 along SQ1 (§36): what recovery from threat reports carried, dropped and never had.

### 41.1 SQ1's clauses ("How can the behaviour of APT attackers be recovered from published threat reports?")

| Clause | Engaged? | Note |
|---|---|---|
| "How can … be recovered" | **No** | ¶2 says what the reports give, not how. One clause would answer it: through hand-drawn attack flows, the only source tried that records which step came first (ch4 §4.1: automatic mining recovered 10 % and 14 % of tactic edges, the attack flows 50 %). That is the evidence that recovery works at all. |
| "the behaviour of APT attackers" | **Overclaimed** | "the order of an APT attacker's tactics": ch4 l.~4027 and §6.5 say the attack graph records attackers reported in CTI, not APT attackers alone. Fix in the wording, no hedge; the bound stays in §6.5. |
| "recovered" | Yes, its strongest part | Kept / dropped / never recorded. "Order" is per edge (a run chains edges from different attack flows, §6.5 "a campaign no attacker ran"); the ch6 term stays, flag only. |
| "from published threat reports" | Yes, rightly partial | The source's own limits (detected, succeeded, stop short of the objective) are §6.5's. Only the two absences that set marks (timing, response to failure) belong here. |

### 41.2 Structure

Marc's reading (gives / drops / never records → judgement) is the right spine. Problems:
1. **Said twice:** S1 "our judgement fills what they do not record" and S6 "we set … by judgement". The topic sentence pre-states the end.
2. **The drops change no mark.** S4–S5 (66 words, 38 %) end on nothing; every other sentence ends on a mark, so these read as a list. Their real job is ¶3's antecedent ("the AND joins and the conditions the model drops"), and ¶2 never says "AND join".
3. **"To run" gives the wrong reason.** ch4 §4.1 drops these when building the attack graph (tactics as nodes, for edges that recur and a smaller mapping): recovery (SQ1), not execution (SQ2). "Most of what else" is unquantified.
4. **Objective-specific behaviour overclaims.** "Enter different tactics after the foothold" contradicts ch4 §4.2 (same common tactics before actions on objectives; they differ in actions on objectives) and §6.1 ¶2 (no more differently than random groups before actions on objectives; 755f5534, 9 of 10 random partitions at or above). It also reads as a full mark; "in part" arrives only in ¶3.
5. **Last sentence:** "them" (pronoun); "a fixed rule of ours" fits the failure matrix only (the tactic durations are values); the order flips against S6; "so each is in part" leaps (why does judgement make it in part? Appendix B's cell: our fixed rule, not the attacker's choice).
6. **Detection avoidance "in part" twice** (¶2 judgement, ¶3 no IDS). §6.1 ¶3 already gives both causes together.

### 41.3 Terms

- The source is named two ways: "threat reports" (S1) and "the attack flows" (S2, S4, S6). Both are right (ch1: attack flows drawn from CTI reports), but the subject shifts unannounced. Name the chain once, then "attack flows".
- "Procedures" collides with "the baseline attacker's procedure" (ch2; §6.1 ¶2, two paragraphs earlier). Use §33.2's plain words: the tools and malware used.
- "How often the attack flows take each edge": Eq. base-weight is the share of the attack profile's attack flows leaving a tactic that draw the edge. "How often" suggests occurrences; use ch4's words or point to the equation, as §6.1 does.
- "Steps an attack flow requires together become separate edges, each enough on its own": hard to parse. "AND join" has no antecedent in ch1–5 prose (Figure 2.x only), yet ¶3 uses it.
- "Conditions between steps": ch2 defines only the condition a flow starts and ends in.

### 41.4 Verified

- Edge weights: Eq. base-weight, l.~4343.
- Techniques → tactics: ch4 §4.1.
- Timing almost never recorded: ch2 l.~1883.
- Only completed steps drawn: ch4 l.~5060.
- Actions on objectives as the only objective signal: ch4 §4.2, §6.1 ¶2, App fa-group-size, 755f5534.
- The §6.5 overlap (CTI records no tactic durations or failure-matrix values, l.~9148) is acceptable: ¶2 needs it for the mark.

### 41.5 Questions (recommendation first)

1. Add the "how" in one clause (hand-drawn attack flows record the order), with no numbers. **Recommended: yes.**
2. Drop "APT attacker's" from the order claim. **Recommended: yes.**
3. The drops: one sentence, its reason fixed to building the attack graph, naming the AND joins and conditions that ¶3 picks up. Procedures and vulnerabilities go in as plain words, or are cut. **Recommended:** keep all, one sentence.
4. Objective-specific: "the attack profiles differ in actions on objectives". **Recommended: yes**, with the mark left to ¶3.
5. Detection avoidance's mark: given in ¶2 by its source, with ¶3 "a second reason". Alternatively, ¶2 names the source only. **Recommended:** the first.

## §42. SQ1's wording, the two vocabularies, and the SQ1/SQ2 split of the marks (Marc 2026-10-12; nothing applied)

Marc's questions:
- Is "recovered" right, if behaviour only emerges when the model runs?
- Why "published" threat reports?
- How do the CTI terms and the MTD terms reconcile?
- Which marks belong to SQ1 and which to SQ2?
- What is the structure?

### 42.1 SQ1's wording: keep (ch1 gated; it also touches the abstract, the ch4 opener and ch7)

- **"Recovered":** the attack flows record what attackers did, and the attack profiles are a recovered description of it (the order of tactics, by objective). Behaviour appears when the description runs, which is SQ2's "executed". The two sub-questions already split it this way. A "how can" question admits a partial answer, and ¶2 gives it: the order, by objective, and not the timing or the response to failure.
- **"Published":** it binds the source to public CTI (ch1 defines CTI as the reports firms and agencies publish). Unpublished incident reports exist, but they are not available and would make the corpus impossible to reproduce. Keep it.
- **"APT attackers":** keep it as the aim. ¶2 states what the attack flows record in their own terms. The gap (18 of 38 attributed) is a bound for §6.5.

### 42.2 The two vocabularies: relations, not equalities

| The question's term | The instance | Relation | Defined |
|---|---|---|---|
| threat reports (SQ1) | the 38 attack flows | drawn from | ch1 approach, ch2 |
| behaviour | the order of tactics, by objective (attack profiles) | what is recovered | ch4 §4.1–4.2 |
| an existing MTD simulator (SQ2) | MTDSim | the instance | ch1 approach |
| techniques | tactics | each technique stands for its tactic | ch4 §4.1 |
| tactics | MTDSim's six attack actions | tactic-to-action mapping | ch4 §4.4.1 |
| APT attackers | attackers reported in CTI | the corpus bound | ch4 §4.1, §6.5 |

**Rule:**
- Each "In answer to SQx" sentence uses its question's words once and names the bridge in one phrase ("threat reports, through the attack flows drawn from them"; "an existing simulator, MTDSim").
- After that, only the instance term is used, never alternating.
- ¶3 already does this; ¶2 does not.

### 42.3 The split follows ch4's own allocation (ch4 opener l.~3899–3902)

- §4.1–4.2 (the attack graph and the attack profiles) answer SQ1.
- §4.3–4.4 (the Petri net and the integration with MTDSim) answer SQ2.
- The tactic durations (§4.4.2) and the failure matrix (§4.4.3) sit in §4.4, so they are SQ2: running needs them, and the reports lack them.

| Mark | Paragraph | Its source |
|---|---|---|
| 3 choice of strategy, full | ¶2 | the order, from the attack flows |
| 2 objective-specific, in part | ¶2 gain, ¶3 cap | the attack profiles differ in actions on objectives; MTDSim cannot run them |
| 1 campaign persistence, full | ¶3 | MTDSim's loop, kept |
| 4 adaptivity, in part | ¶3 | the failure matrix, set by our judgement |
| 5 detection avoidance, in part | ¶3 only | the tactic durations, set by our judgement, and MTDSim has no IDS |
| 6, 7, 8 | neither | no part of the model; the opener says all four lack them |

- ¶2 ends on the absence (the reports almost never record timing or the response to failure), which is a fact about SQ1.
- ¶3 opens on the fill (running needs both, so we set them).
- This also settles §41.5 Q5: detection avoidance is marked once, with both reasons.

### 42.4 Structure (slots only)

**¶2, SQ1 (about 110 words)**
1. The answer, with the how: threat reports, through hand-drawn attack flows, give the model the order of tactics, by objective.
2. Mark 3: the order, drawn at run time (Eq. base-weight).
3. Mark 2's gain: the attack profiles differ in actions on objectives.
4. Lost in building the attack graph: the tools and malware, the vulnerabilities, the AND joins and the conditions.
5. Never recorded: how long a step took, and what the attacker did after a failure.

**¶3, SQ2 (about 150 words)**
1. The answer: an existing simulator, MTDSim, gives campaign persistence. Running also needs what the reports lack, and MTDSim caps marks 2 and 5.
2. Mark 1: the kept loop.
3. Marks 4 and 5: we set the failure matrix and the tactic durations by judgement, a fixed rule rather than the attacker's choice.
4. The caps: actions on objectives are unmapped (mark 2 in part); there is no IDS (mark 5, a second reason).
5. The Petri net could carry the AND joins and the conditions; built with one token, it uses neither.

**Close:** unchanged.

## §43. §6.3 ¶2 (SQ1) redraft proposed (Marc 2026-10-12, "translate all of this scrutiny into paragraph two"; not applied)

From the §42.4 slots and the §41 fixes. 176 → 156 words.

```latex
In answer to \ref{sq:capture}, the attack flows that analysts drew step by
step from threat reports give the APT attacker model the order of its
tactics, by objective. The order gives it choice of attack strategy in full,
because its Petri net draws each next tactic during the run, among the edges
out of the tactic it is on (Equation~\ref{eq:base-weight}). Its objective-specific
behaviour comes from the attack profiles, which differ in actions on
objectives (Section~\ref{sec:attack-profiles}). Building the attack graph
keeps which tactic follows which and drops the rest of each step: its
technique, and the tools, malware and vulnerabilities it used
(Section~\ref{sec:technique-graph}). It also drops how the steps combine: the
AND joins, which require several steps done before the next, and the
conditions between steps. The attack flows almost never record how long a
step took. They never record what the attacker did after a failure, because
each draws only the steps its attacker completed
(Section~\ref{subsec:failure-matrix}).
```

**What each §41 point became:**
- The "how": "drew step by step" (manual attack profiling records the order).
- "APT attacker's" is dropped; the bound stays in §6.5.
- The drops are given the reason "building the attack graph", not "to run".
- "Procedures" became the tools and malware.
- The AND join is glossed for ¶3.
- Objective-specific: "differ in actions on objectives"; the mark is left to ¶3.
- Judgement, marks 4 and 5, and "them" all moved to ¶3.
- "Threat reports" appears once, then "attack flows" throughout.
- Edge weights: "among the edges out of the tactic it is on" (Appendix B row 3's reason, run time and current state).

**Knock-ons:**
- ¶2 and ¶3 must land together. Otherwise adaptivity and detection avoidance lose the sentence that gave their marks.
- Appendix B row "APT attacker model, 2" still says "enter different tactics after the foothold for different objectives". It changes to "differ in actions on objectives" when ¶2 lands (auto, downstream).

## §44. §6.3 ¶2 draft (§43) rejected as a list: "so what? where's the punch?" Sort test and the punch (Marc 2026-10-12; nothing applied)

Marc: the §43 draft answers the question with the right structure, but it reads as precise sentences without an argument. It tries to answer SQ1, describe the model and justify the marks all at once. He asked whether its points already live elsewhere.

### 44.1 Sort test of the §43 draft

| Sentence | Already in | Verdict |
|---|---|---|
| Attack flows drawn step by step | ch2 (manual attack profiling), ch4 §4.1 | Clause at most |
| The order → choice in full; the Petri net draws at run time | §6.1 ¶2 (the draw), Appendix B row 3 | Cut the reasoning; cite the mark as evidence |
| Objective-specific from the attack profiles' actions on objectives | §6.1 ¶2, ch4 §4.2 | Same |
| Drops: the technique, tools, malware, vulnerabilities | nowhere | No consequence anywhere: cut |
| Drops: AND joins, conditions | nowhere | Their only consequence is ¶3's "the Petri net could carry them": move to ¶3 |
| No timing; no response to failure | ch2 l.~1883; ch4 §4.4.2–4.4.3; §6.5 (bound) | Keep: the premise of the punch |

**Diagnosis:** the only sentences new to the thesis (the drops) have no consequence. Everything else repeats evidence that lives elsewhere. The paragraph never says what the answer means.

### 44.2 The punch (new; nowhere in ch6)

- **Premise:** in MTDSim a deployment meets the attacker at two points (ch2 l.~843; ch4 l.~4400):
  - it disrupts an attack action in flight, which depends on how long the action takes;
  - the failed verdict sends the attacker to its response to failure.
- **The match:** those are the two things threat reports do not record. They describe attacks that succeeded, step by step.
- **So:** what the model recovers from CTI is the route (which tactic follows which, by objective). Where MTD meets the attacker, it rests on our judgement.
- **Answer to SQ1:** threat reports can recover the route of an APT attacker, but not its encounter with MTD.
- **Sets up the close:** of what CTI gives, the route (order) likely reaches SQ3's answer.
- §6.4 (the interface paragraph) and §6.5 (the judgement bound) state the parts; neither draws the conclusion.

### 44.3 Spine proposed for ¶2 (about 90–110 words)

1. **The answer:** threat reports, through attack flows, recover the route an attacker takes: which tactic follows which, for each objective. Marks 3 and 2 are cited as evidence in one clause (Table 6.1).
2. **The limit, with its cause:** they record attacks that succeeded, so they almost never record how long a step took and never what an attacker did when a step failed.
3. **The punch:** in MTDSim those are where a deployment meets the attacker (it disrupts an attack action in flight, and the attacker must respond to the failure). So the model is grounded in CTI along its route and rests on our judgement where MTD acts on it.
4. **(Optional, one hedge):** any attacker model recovered from threat reports likely shares this gap.

**¶3 then opens:** to run, we set the tactic durations and the failure matrix by judgement (marks 4 and 5). It also takes over the AND joins and the conditions.

## §45. §6.3 ¶2 second draft, on the §44 spine (Marc 2026-10-12, "let's have a look at this"; proposed, not applied)

**Rulings asked, with recommendations taken:**
- The tools, malware and vulnerabilities are cut outright. They are not a threat to validity: no result rests on them, and MTDSim uses its own vulnerabilities.
- The AND joins and the conditions go to ¶3.
- Sentence 4 (other attacker models likely share the gap) is left out of ¶2. The punch already rests on a general fact (reports time only whole intrusions and describe successes). It can be offered to §6.4 if wanted.
- "Route" is not used. The thesis term is "the order of its tactics" (§6.1, §6.2, the close); one term per thing.

**Draft: 145 words** (176 on disk).

```latex
In answer to \ref{sq:capture}, the attack flows drawn from threat reports
give the APT attacker model the order of its tactics for each objective. That
order gives it choice of attack strategy in full and objective-specific
behaviour in part (Table~\ref{tab:fidelity-verdict}). Threat reports time only
whole intrusions, so the attack flows almost never record how long a step took
(Section~\ref{subsec:dwell-times}). Drawn from attacks that succeeded, they
never record what the attacker did after a step failed
(Section~\ref{subsec:failure-matrix}). In MTDSim, timing and the response to
failure are where MTD disrupts the attacker: the tactic durations set how
likely a deployment is to land during an attack action and fail it, and the
response to failure sets where the attacker goes next
(Section~\ref{subsec:runtime-mechanics}). The APT attacker model is therefore
grounded in threat reports for the order of its tactics, and rests on our
judgement where MTD disrupts it.
```

**Facts:**
- "Threat reports time only whole intrusions": ch4 l.~4954.
- "Attacks that succeeded … only completed steps": ch4 l.~5060.
- "A deployment that lands during an attack action fails it": ch4 l.~4400 and ch2.
- "MTD disrupts": ch2's verb.

**Knock-on for ¶3:** it opens on the fill (the tactic durations: six from MTDSim's times, nine by judgement; the failure matrix), which gives marks 4 and 5. It takes over the AND joins and the conditions.

## §46. §6.3 ¶2 clarity pass (Marc 2026-10-12, "beautiful … clarity pass please"; proposed, not applied)

**Marc approved the §45 draft and the cut.**

**Term-by-term clarity pass:**
- **"Step":** kept. It is the attack flow's unit (ch1 "graphs of an attack's steps"; ch4 "draws only the steps its attacker completed"). The model's unit is the tactic. "Place" is a Petri-net term, so it is wrong here.
- **"Attacks that succeeded" → "incidents that succeeded":** ch4 l.~5060 verbatim, and ch2 defines an attack flow as one incident.
- **"Timing and the response to failure" → "these two points":** a third name for each thing is gone. The model's components are now named (its tactic durations, its failure matrix), which bridges step → tactic duration and failure → failure matrix. They are the antecedents of "our judgement".
- **"Land during an attack action and fail it" → "cut an attack action short and fail it":** ch4 l.~4400 says "cut … short".
- **"Where the attacker goes next" → "which tactic it takes after an attack action fails":** specific. The flows' "step failed" and the model's "attack action fails" are kept apart.
- **"Disrupts the attacker" → "disrupts the APT attacker model":** names it.

**Draft: 146 words.**

```latex
In answer to \ref{sq:capture}, the attack flows drawn from threat reports
give the APT attacker model the order of its tactics for each objective. That
order gives it choice of attack strategy in full and objective-specific
behaviour in part (Table~\ref{tab:fidelity-verdict}). Threat reports time only
whole intrusions, so the attack flows almost never record how long a step took
(Section~\ref{subsec:dwell-times}). Drawn from incidents that succeeded, they
never record what the attacker did after a step failed
(Section~\ref{subsec:failure-matrix}). In MTDSim, MTD disrupts the APT
attacker model at these two points: its tactic durations set how likely a
deployment is to cut an attack action short and fail it, and its failure
matrix sets which tactic it takes after an attack action fails
(Section~\ref{subsec:runtime-mechanics}). The APT attacker model is therefore
grounded in threat reports for the order of its tactics, and rests on our
judgement where MTD disrupts it.
```

## §47. §6.3 ¶2 applied (Marc 2026-10-12, "very clear as is, I'm happy with it")

- **Applied:** the §46 text, 146 words, replacing 176.
- **Pointer:** S2 keeps Table 6.1 alone; no stacked §6.1/§6.2 pointers.
  - Table 6.1's caption points to Appendix B, which carries each mark's reasoning.
  - §6.1 explains the measured differences, not the marks.
  - §6.2 does not touch marks 2 and 3.
- **Appendix B row "APT attacker model, 2" (auto, downstream):** "enter different tactics after the foothold for different objectives" → "differ in actions on objectives".
- **Owed by ¶3's redraft (next):**
  - marks 4 and 5 (the tactic durations: six from MTDSim's times and nine by judgement; the failure matrix), which have lost their sentence until then;
  - the AND joins and the conditions: ¶3's "the AND joins and the conditions the model drops" has lost its antecedent in ¶2;
  - detection avoidance marked once, with both reasons.
- Build clean, 118 pages, 0 undefined.

## §48. §6.3 ¶3 (SQ2): scrutiny of the text on disk, with ¶2's lessons (Marc 2026-10-12; nothing applied)

¶3 is 148 words in six sentences. ¶2's lessons, applied here:
- answer plainly, with a so-what;
- sort test: does the sentence live elsewhere?;
- translate the question's terms;
- the structure follows from all three.

### 48.1 SQ2's clauses ("How can the recovered behaviour be executed as an APT attacker model inside an existing MTD simulator?")

| Clause | Engaged? | Note |
|---|---|---|
| "How can … be executed" | **No** | One clause: the tactic its token reaches runs as one of MTDSim's six attack actions, through the tactic-to-action mapping (ch4 §4.4, the loop). |
| "the recovered behaviour" | **No** | ¶3 never names what is executed. The bridge from ¶2 is the order of its tactics. |
| "as an APT attacker model" | Yes | The marks; cite them, don't re-argue. |
| "inside an existing MTD simulator" | Half | It gives what MTDSim gives (persistence) and caps (2, 5). It misses why "existing" matters: the model runs the baseline attacker's six attack actions under the same deployments, which is the comparison SQ3 asks for. |

### 48.2 Sort test

| Sentence | Already in | Verdict |
|---|---|---|
| S1: gives persistence, caps two marks | ch4 opener l.~3888 ("keeps the baseline attacker's campaign persistence; they also cap what it gains") | Rehash of ch4's own answer to SQ2 |
| S2: keeps the baseline attacker's loop → persistence | ch4 opener; App B l.~9809 | Clause. **Term clash:** ch4 §4.4's "loop" is the APT attacker model's own Petri net–MTDSim loop. "It" is ambiguous (simulator or model). |
| S3: AoO unmapped → 2 in part | ch4 §4.4.1 ("nothing to act on"); §6.1 ¶2 near verbatim | Clause. "The techniques that differ by objective are assumed" is Appendix B jargon; unclear. |
| S4: no IDS → 5 in part | ch4 §4.4.1 ("nothing in MTDSim watches the attacker"); §6.1 ¶3 near verbatim | Clause. It misses the judgement half (owed from ¶2). |
| S5–S6: the Petri net could carry the AND joins and conditions; with one token it uses neither | nowhere; ch7 future work has "more than one token" | Antecedent lost with ¶2. Same test as the tools cut (nothing follows): **cut**. |
| Owed from ¶2: the fill (tactic durations: six from MTDSim, nine by judgement; failure matrix) → 4, 5 | ch4 §4.4 ("the attack flows cannot supply three inputs of the loop … we declare each") | Clause, pointing to ¶2's "our judgement" |

**Diagnosis:** the same as ¶2's first draft. Every sentence re-argues a mark that ch4 or §6.1 already argues, and the one new point (the AND joins) leads nowhere. There is no so-what.

### 48.3 The punch: what "existing" buys and costs

- **Buys:** the APT attacker model runs MTDSim's six attack actions, the baseline attacker's own, under the same MTD deployments. So the two attackers differ only in what the model adds (the order of its tactics, the tactic durations, the failure matrix, the vulnerability memory). That is the comparison SQ3 asks for ("compared with the simulator's baseline attacker"), and §6.1/§6.2's explanations rest on it.
- **Costs:** the same attack actions set the ceiling (ch4: "only as good as the attack actions it adopts"). Seven tactics are unmapped. The two marks MTDSim caps are both caps through unmapped tactics:
  - actions on objectives have nothing to act on (2);
  - Stealth has nothing to hide from (5).
- **One causal chain for 5,** which settles the double reason: nothing watches the attacker, so its detection avoidance comes only from the tactic durations, which we set (§6.1 ¶3's own conclusion).
- **Not yet in ch6 as SQ2's answer:**
  - ch4 states the ceiling;
  - ch4 §4.4.2 uses "the same MTD deployments" only to justify the scale of the durations;
  - no paragraph puts the two together as the trade.

### 48.4 Terms

| Question's term | Instance | Note |
|---|---|---|
| the recovered behaviour | the order of its tactics | ¶2's term, verbatim |
| executed | the tactic its token reaches runs as an attack action | ch4 §4.4 |
| an existing MTD simulator | MTDSim | bridge once, as ¶2 does |
| (what it runs) | MTDSim's six attack actions, via the tactic-to-action mapping | seven tactics unmapped (ch4 §4.4.1) |
| persistence source | ch4 opener's "keeps … with those attack actions" | not "loop" (ch4's loop is the model's) |
| detection | "nothing in MTDSim watches the attacker" (ch4) / "no IDS" (§6.1) | pick one; §6.1 uses IDS |
| "caps" | ch4 opener's own verb | keep |

### 48.5 Structure that follows (slots, about 110–130 words)

1. **The answer, with the how:** the order of its tactics runs inside MTDSim, the tactic its token reaches becoming one of MTDSim's six attack actions.
2. **What running needs that the reports lack:** the tactic durations and the failure matrix, set by us (¶2's "our judgement"), which leave adaptivity and detection avoidance in part. Clause-level; cite Table 6.1.
3. **What "existing" buys:** the baseline attacker's attack actions and loop of play under the same deployments, so persistence is kept, and the two attackers differ only in what the model adds.
4. **What it costs:** seven tactics are unmapped. Actions on objectives have nothing to act on (2 in part), and nothing watches the attacker, so its detection avoidance is only its tactic durations (5, one chain).
5. **The punch:** executing in an existing simulator makes the comparison with its baseline attacker fair and sets the ceiling of the model at that attacker's attack actions.
   - S3 and S5 may merge.
   - No hedge needed: by construction.

### 48.6 Questions (recommendation first)

1. **The punch** is the trade (comparison bought, ceiling set). **Recommended.** Alternative: only the ceiling, which is ch4's.
2. **Cut the AND-joins/conditions sentences.** **Recommended:** the same test as the tools cut; ch7 future work already carries the one-token point.
3. **One chain for detection avoidance:** nothing watches → only tactic durations → ours. **Recommended.**
4. **Persistence wording:** use ch4's ("keeps it with those attack actions") and drop "loop". **Recommended.**

## §49. §6.3 ¶3 (SQ2) redraft proposed, on the §48 slots (Marc 2026-10-12, "translate … into a clear, concise argument"; not applied)

All four §48.6 recommendations are taken as approved with the structure:
- the punch is the trade;
- the AND joins are cut;
- detection avoidance gets one chain;
- persistence is worded as ch4 does, and "loop" is dropped.

148 → 169 words. It now carries marks 4 and 5, owed from ¶2. §6.3 is about 450 words in all.

```latex
In answer to \ref{sq:model}, the APT attacker model executes the order of its
tactics inside an existing simulator, MTDSim, by mapping eight of the 15
tactics onto MTDSim's six attack actions
(Section~\ref{subsec:tactic-verb-mapping}). It shares the baseline attacker's
attack actions and MTD deployments, so it keeps the baseline attacker's
campaign persistence. Any difference between the two attackers comes from what
the APT attacker model adds. We set two of those additions by judgement: the
tactic durations and the failure matrix. The failure matrix makes its response
to failure a fixed rule of ours, so adaptivity is in part
(Table~\ref{tab:fidelity-verdict}). The same attack actions cap the APT attacker
model, because
the other seven tactics have none to run. Collection, Exfiltration and Impact
have nothing to act on, which leaves objective-specific behaviour in part.
Nothing in MTDSim watches the attacker, so its detection avoidance comes only
from the tactic durations we set, and is in part. The attack actions that make
the two attackers comparable therefore also set the APT attacker model's
ceiling.
```

**Facts:**
- 8 of 15 tactics mapped (7 unmapped, ch4 §4.4.1).
- The same MTD deployments (ch4 §4.4.2; ch5).
- Persistence kept with the attack actions (ch4 opener).
- The failure matrix is a fixed rule (App B row 4).
- "Nothing in MTDSim watches the attacker" and "nothing to act on" (ch4 §4.4.1).
- Detection avoidance only from the tactic durations (§6.1 ¶3).
- The ceiling (ch4 §4.4.1).

## §50. §6.3 ¶3 clarity pass, on Marc's review (Marc 2026-10-12, "80% there … tidy round the edges"; proposed, not applied)

**Marc's points, and what each became:**
- **"What it adds" is vague.** It now names them: the order of its tactics and four declared parts (the tactic-to-action mapping, the tactic durations, the failure matrix, the vulnerability memory). The "two by judgement" of §49 undercounted.
- **Judgement or assumption?** "Declared" is ch4's verb (§4.4: "we declare each, from MTDSim's constants where they exist and otherwise from the literature or our judgement"). §6.4 says "declared assumption". The durations are six from MTDSim's times and nine by judgement, so "declared" is exact. ¶2's "our judgement" stays: it names the gaps the reports leave, consistent with §6.5's "declared them by judgement".
- **Is adaptivity's mark the failure matrix's, given the ablation?** Yes.
  - Without it, the model routes after a failure by the base weights, as after a success (§5.4 failure-matrix paragraph). Nothing then depends on the verdict.
  - With it, the model goes back to Reconnaissance after a failed Initial Access in 0.76–0.83 of cases, against 0.08–0.10 without.
  - The mark scores what the model implements. The ablation measures its effect on NCR (negligible), which the close already ties to the mark.
- **"Nothing to act on" → "unmapped":** ch4's defined term (emph).
- **"Nothing in MTDSim watches the attacker" → "MTDSim detects no attacker":** ch4 l.~5424. Detection avoidance "only by proxy, through its tactic durations" uses ch4's "by proxy". The mark is stated first.
- **The punch was a cliché ("the same thing is the limitation").** It is now concrete: MTDSim's attack actions make the two attackers comparable and limit the model to finding and compromising hosts (§6.1 ¶2's words).
- **Persistence:** "It runs the baseline attacker's attack actions, so it keeps the baseline attacker's campaign persistence". "Facing the same MTD deployments" moved to the difference sentence, where it belongs.

**Draft: 182 words** (148 on disk).

```latex
In answer to \ref{sq:model}, the APT attacker model executes the order of its
tactics inside an existing simulator, MTDSim, by mapping eight of the 15
tactics onto MTDSim's six attack actions
(Section~\ref{subsec:tactic-verb-mapping}). It runs the baseline attacker's
attack actions, so it keeps the baseline attacker's campaign persistence.
Facing the same MTD deployments, the two attackers differ only in what the APT
attacker model adds: the order of its tactics and four declared parts, the
tactic-to-action mapping, the tactic durations, the failure matrix and the
vulnerability memory (Section~\ref{sec:execution}). The failure matrix
reweights the next tactic after a failed attack action by a rule we declared,
so adaptivity is in part (Table~\ref{tab:fidelity-verdict}). The same attack
actions cap the APT attacker model, because the other seven tactics are
unmapped. Among them are Collection, Exfiltration and Impact, so
objective-specific behaviour is in part. MTDSim detects no attacker, so detection
avoidance is in part: the APT attacker model avoids detection only by proxy,
through its tactic durations. MTDSim's
attack actions thus make the two attackers comparable, and limit the APT
attacker model to finding and compromising hosts.
```

## §51. §6.3 ¶3 second clarity pass (Marc 2026-10-12: "what details does the discussion need … important part first … what is redundant, what is decoration"; proposed, not applied)

**Changes:**
- **The claim moves to S2** (important part first): running the baseline attacker's own attack actions under the same deployments makes the two attackers comparable and caps what the model can do. The closing "punch" sentence is cut; it restated this claim, and Marc heard it as a cliché.
- **The list of four declared parts is cut** (detail). The difference is "the order of its tactics and the parts we declared to run it (Section 4.4)". Only the two parts that set marks are named, where they set them: the failure matrix (adaptivity) and the tactic durations (detection avoidance). The mapping and the vulnerability memory set no mark.
- **Objective-specific:** back to Marc's preferred original causal chain (the attack actions only find and compromise hosts → Collection, Exfiltration and Impact unmapped → in part). "Seven tactics" and "among them" are cut.
- **Detection avoidance:** it leads with the behaviour (only by proxy, through its tactic durations), then the reason (MTDSim has no IDS to evade). "MTDSim detects no attacker, so detection avoidance is in part" read as a contradiction.
- **"Eight of the 15" cut** (detail no longer used).
- No hedge needed: every claim holds by construction.

**Draft:** about 158 words (148 on disk).

```latex
In answer to \ref{sq:model}, the APT attacker model executes the order of its
tactics inside an existing simulator, MTDSim, by mapping tactics onto
MTDSim's six attack actions (Section~\ref{subsec:tactic-verb-mapping}).
Running the baseline attacker's own attack actions under the same MTD
deployments makes the two attackers comparable and caps what the APT attacker
model can do. The APT attacker model keeps the baseline attacker's campaign
persistence, and differs from the baseline attacker only in the order of its
tactics and the parts we declared to run it (Section~\ref{sec:execution}). Of
the declared parts, the failure matrix sets its response to a failed attack action by a
fixed rule, so adaptivity is in part (Table~\ref{tab:fidelity-verdict}).
MTDSim's attack actions only find and compromise hosts, so Collection,
Exfiltration and Impact are unmapped and objective-specific
behaviour is in part. The APT attacker model avoids detection only by proxy,
through its tactic durations, because MTDSim has no IDS to evade. Detection
avoidance is therefore in part.
```

## §52. Why ¶3 got worse over three drafts: a critique, no redraft (Marc 2026-10-12)

**Marc:** §49 "was probably the strongest and it just gets progressively worse … am I giving the wrong prompts? Don't redraft, critique." His new flags:
- "mapping tactics" bare is vaguer than "eight of the 15". The 15 is anchored to ATT&CK v19.1 in ch4 §4.1, so it is not stale inside the thesis.
- "Caps what the APT attacker model can do" reads fake and vague.

### 52.1 Trace: each §49 sentence, Marc's flag, and what §50/§51 did

| §49 sentence | Marc on it | §50 / §51 | Right move |
|---|---|---|---|
| 1. executes the order … mapping eight of the 15 tactics | no flag | §51 cut "eight of the 15" | keep |
| 2. shares attack actions and deployments → persistence | "Yep" | §50 reordered; §51 folded into a new claim sentence | keep |
| 3. any difference comes from what it adds | "a bit vague, what does it add?" | §50 listed all four; §51 back to "the parts we declared" | name what the paragraph uses |
| 4. we set two … by judgement | question: two or four? judgement or assumption? | §50 term swap → "declared"; §51 removed | answer in chat; fix the count/term only |
| 5. failure matrix → fixed rule → adaptivity in part | question: is the mark the failure matrix's, given the ablation? | §50 reworded; §51 reworded again | answer in chat (yes; the ablation is the close's); no edit |
| 6. the same attack actions cap it: the other seven have none to run | "that's true" | §50 → "unmapped"; §51 cut | keep, with "unmapped" |
| 7. C/E/I have nothing to act on → 2 in part | "act on, or unmapped?" | §50 "among them"; §51 back to an older chain | "are unmapped" |
| 8. nothing watches the attacker → durations → 5 in part | "MTDSim models no IDS; by proxy" | §50 "detects no attacker" (contradiction); §51 reordered | wording only: no IDS, by proxy |
| 9. punch: comparable and the ceiling | "a bit of a cliché" | §50 made it concrete; §51 cut it and moved the claim to S2 | rephrase, keep the slot |

**Result:**
- Of nine sentences, five needed an edit and two needed only a chat answer.
- §50 and §51 changed all nine.
- §51 changed the structure Marc had called "100 % right".

### 52.2 Diagnosis

1. **Rewrote instead of editing.** This breaks the standing rule ([[feedback-redraft-edit-dont-rewrite]], ch3 round 44 of 2026-10-02, the same failure). §49 was the base, and only the flagged sentences should have moved.
2. **Questions turned into edits.** "Do we need all four?" and "is it judgement or assumption?" were questions. Answering them in prose first added a list (§50), then removed it (§51), and so oscillated around Marc's original complaint.
3. **A general lens applied globally.** "Clarity pass … important first … what's redundant, for everything" was read as licence to restructure. It is a lens for the flagged sentences.
4. **Term churn.** Each pass swapped a term: judgement → declared; watches → detects no attacker → no IDS to evade. Each swap fixed one thing and broke register or added a contradiction.
5. **Past the peak** (clarity is an inverted U). §49 was near it. §50 added nuance (the list); §51 cut the specifics that made it concrete ("eight of the 15", "the other seven", the punch).

### 52.3 Marc's prompts?

Mostly not the cause. His voice reviews mix agreement ("yep"), questions and fixes in one stream, and separating them is the session's job. What would help, on either side:
- name the base round;
- a "yep" locks a sentence;
- questions are answered in chat;
- each change comes back traced to a flag (the table above).

### 52.4 The way back (no redraft yet)

- **Base:** §49.
- **Edits on rows 3, 4, 6, 7, 8 and 9 only:**
  - name what it adds (the order of its tactics; the tactic durations and failure matrix that it declares);
  - fix the count/term;
  - "unmapped";
  - no IDS, by proxy;
  - rephrase the punch.
- **Kept:** rows 1, 2 and 5.

## §53. §6.3 ¶3: §49 plus the flagged edits only (Marc 2026-10-12, "start from 49"; proposed, not applied)

| §49 sentence | Flag | Edit |
|---|---|---|
| 1, 2 | none / yep | unchanged |
| 3. what it adds | vague | "the order of its tactics and four parts we declared (Section 4.4)" |
| 4. two by judgement | count, term | "Two of those parts, the tactic durations and the failure matrix, fill what the threat reports do not record" (ch4's "declare"; it links to ¶2) |
| 5. failure matrix → adaptivity | question (answered) | unchanged except "its" → "the APT attacker model's": after row 4, "its" read as the failure matrix's (pronoun rule) |
| 6. the other seven have none to run | true | "are unmapped" |
| 7. nothing to act on | unmapped? | "Three of them are Collection, Exfiltration and Impact, the tactics of actions on objectives" (§6.1 ¶2 verbatim) |
| 8. nothing watches | no IDS, by proxy | "MTDSim has no IDS, so the APT attacker model avoids detection only by proxy, through its tactic durations" |
| 9. punch | cliché | "The APT attacker model is therefore comparable with the baseline attacker, and limited to what MTDSim's attack actions do: find and compromise hosts" |

**Draft: 196 words** (148 on disk; §49 was 170).

```latex
In answer to \ref{sq:model}, the APT attacker model executes the order of its
tactics inside an existing simulator, MTDSim, by mapping eight of the 15
tactics onto MTDSim's six attack actions
(Section~\ref{subsec:tactic-verb-mapping}). It shares the baseline attacker's
attack actions and MTD deployments, so it keeps the baseline attacker's
campaign persistence. Any difference between the two attackers comes from
what the APT attacker model adds: the order of its tactics and four parts we
declared (Section~\ref{sec:execution}). Two of those parts, the tactic
durations and the failure matrix, fill what the threat reports do not record.
The failure matrix makes the APT attacker model's response to failure a fixed rule of ours, so
adaptivity is in part (Table~\ref{tab:fidelity-verdict}). The same attack
actions cap the APT attacker model, because the other seven tactics are
unmapped. Three of them are Collection, Exfiltration and Impact, the tactics
of actions on objectives, so objective-specific behaviour is in part. MTDSim
has no IDS, so the APT attacker model avoids detection only by proxy, through
its tactic durations, and detection avoidance is in part. The APT attacker model is therefore comparable with the baseline
attacker, and limited to what MTDSim's attack actions do: find and compromise
hosts.
```

## §54. §6.3 ¶3 applied; final clarity pass (Marc 2026-10-12, "apply that … final clarity pass over the full draft")

- **Applied:** §53's text. The last sentence is §53's, plus "with no actions on objectives" (Marc's missing nugget, in ch4's stage term). It took four rounds on that sentence:
  - "steals no data", "says nothing about", "only for" and "only as" were each heard as rhetorical or off-term;
  - the base sentence with the nugget added was the tightest.
- About 199 words, from 148. §6.3 is about 480 words.
- Build clean, 118 pages, 0 undefined.

**Final clarity pass (flags only; the lesson of §52):**

| Sentence | Verdict |
|---|---|
| S1 the how | clear; "eight of the 15" sets up S6's "the other seven" |
| S2 shares attack actions and MTD deployments → persistence | **one flag:** persistence follows from the attack actions alone; "and MTD deployments" rides along under "so". Optional fix: "It shares the baseline attacker's attack actions, so it keeps the baseline attacker's campaign persistence, and faces the same MTD deployments." |
| S3 what it adds | clear; "declared" is ch4's verb |
| S4 two of those parts | clear; picks up ¶2 |
| S5 failure matrix → adaptivity | clear |
| S6 the same attack actions cap it | clear; "the same" resolves to S2 |
| S7 C/E/I, the tactics of actions on objectives | clear; §6.1 verbatim |
| S8 no IDS → by proxy | clear; two consequences under one "so", acceptable at this length |
| S9 punch | clear; "actions on objectives" repeats S7's term (one term, deliberate) |

**Close (¶4) checked against ¶3:** it ties the failure matrix to adaptivity and the attack profiles to objective-specific behaviour, the same sources ¶3 gives. No knock-on.

## §55. §6.3 close: does it earn its place, and what is its one-liner? (Marc 2026-10-12; nothing applied)

Marc kept ¶3's S2 as it is. On the close he asked: what must it carry, is it needed, what is the one-liner? The close is 89 words in three sentences.

### 55.1 Sort test

| Sentence | Already in | Verdict |
|---|---|---|
| S1: two marks likely reach SQ3 (choice of attack strategy via the order; detection avoidance via the tactic durations) | §6.2 opener ("tactic durations and the order of its tactics likely explain the difference"); §6.1 close | the same claim in mark terms; the only new part is the translation into marks |
| S2: the failure matrix (adaptivity) moves NCR negligibly; without the attack profiles (objective-specific) the same three MTD mechanisms lead | §5.4; §6.1 opener; §6.5 internal validity | rehash (the claim counted six times in §32.3) |
| S3: of what the threat reports give, only the order likely reaches the answer; no run with MTD tests the order alone | §6.5 ("order and durations, which no run with MTD separates … Order has no test of its own"); §6.4 ("nor that the grounding in CTI caused the reversal") | the bound is §6.5's (bounds once); the CTI verdict is half-said by ¶2's ending |

### 55.2 What only the close can do

- ¶2 ends: grounded in threat reports for the order; rests on our judgement where MTD disrupts it.
- ¶3 ends: comparable, and limited to finding and compromising hosts.
- §6.2 says the order and the tactic durations likely explain SQ3's answer.
- **Nobody joins them.** The two marks that likely reach SQ3 come one from each source of ¶2: choice of attack strategy from the threat reports, detection avoidance from our judgement.
- That is the payoff of §6.3 for the research question: what the answers to SQ1/SQ2 mean for SQ3.

**One-liner:** *SQ3's answer likely rests on one mark from the threat reports and one from our judgement.*

### 55.3 Recommendation

- **Keep the close as one sentence:** the join, hedged once ("likely"), pointing to §6.2.
- **Cut S2:** a rehash, with its homes in §5.4, §6.1 and §6.5.
- **Cut S3's bound to §6.5,** where bounds live once.
- **Alternative:** cut the close. §6.3 then ends on ¶3, and the reader joins ¶2 to §6.2 alone. The cost: §6.3 never says why its marks matter for the result.
- **Gated knock-on:** ch7 Contribution 1 "Bound" is written "in step with §6.3's close" (the CTI verdict, untested alone, the negligible ablations). If the close drops them, the Bound points to §6.5 and §5.4 instead. That is a ch7 edit, to be proposed.

## §56. §6.3 close cut (Marc 2026-10-12, "cut it")

- **Why:** the one-sentence close drafted from §55 relabelled §6.2's causes as marks (order → choice of attack strategy, tactic durations → detection avoidance). That added nothing, and it conflated a mark (a score of a property) with a cause.
- **The only new idea** (one cause from the threat reports, one from judgement) needs a claim no run supports: no run with MTD separates the order from the durations (§6.5).
- **Where everything now lives:**
  - ¶2's ending carries the source split;
  - ¶3's ending carries the scope;
  - §6.2 carries what explains SQ3;
  - §5.4, §6.1 and §6.5 carry the ablations and the bound.
- **§6.3:** opener, ¶2, ¶3. About 390 words, down from 1 235 at the overdraft.
- Nothing in ch6 refers to the close.
- **Owed, gated (ch7):** Contribution 1's "Bound" draftnote is "in step with §6.3's close". Proposed:
  - first clause → "SQ3's answer likely rests on the order of its tactics, from CTI, and the tactic durations, set by judgement (Section 6.2)";
  - "no run with MTD tests the order alone" → Section 6.5;
  - the negligible ablations → Section 5.4.
- Build clean, 118 pages, 0 undefined.

## §57. §6.3 as a whole: does it do its jobs? (Marc 2026-10-12; nothing applied)

§6.3 is now the opener, ¶2 and ¶3 (about 406 words) plus Table 6.1.

| Job | Done? | Where / gap |
|---|---|---|
| Set the model against the field | yes | the opener: more properties than any; the only one with 3 in full and any 2; all four lack 6–8 |
| Answer SQ1 | yes | ¶2: the order of tactics for each objective is recovered; timing and the response to failure are not; the model rests on our judgement where MTD disrupts it. The "how" is thin ("drawn from"), but it is enough with ch4 behind it. |
| Answer SQ2 | **mostly** | ¶3: mapped onto six attack actions; comparable and capped. **Gap: the Petri net is gone from §6.3.** Ch1 and ch4 answer SQ2 as "execute each attack profile as a Petri net inside MTDSim", and ¶3's how names only the mapping. |
| Explain Table 6.1's marks (the source of each) | **all but one reason** | 1 ¶3; 2 ¶2 + ¶3; 4 ¶3; 5 ¶3. **Mark 3's "in full" lacks its reason:** "that order gives it choice of attack strategy in full", but the baseline attacker has an order too. The full mark is for drawing the next tactic during the run (Appendix B row 3), which the Petri net does. The §43 draft had it; the §45 rewrite dropped it. 6–8: the opener states the gap for the field; the model's own reason (not modelled) is in ch4 and Appendix B, which is enough. |
| Agree with §6.1 | yes | the objective shows only in actions on objectives; detection avoidance only through the tactic durations. Same sources, no contradiction. |
| Link to SQ3 | cut by ruling (§56) | §6.2 owns it |

**One fix closes both gaps:** name the Petri net and its run-time draw in ¶3's S1, the SQ2 how. For example:

> "… executes the order of its tactics inside an existing simulator, MTDSim, as a Petri net that draws its next tactic during the run, mapping eight of the 15 tactics onto MTDSim's six attack actions."

- ¶2's "That order gives it choice of attack strategy in full" then has its reason one paragraph later.
- Alternatively, ¶2's S2 gets the clause ("…in full, drawn by its Petri net during the run").
- **Recommended: ¶3**, because the draw is execution (SQ2), and ¶2 stays as approved.
- Proposed, not applied (paragraph gate).

## §58. §6.3 ¶3: the Petri net clause applied (Marc 2026-10-12, "yes that's fine")

- **S1 now reads:** "…executes the order of its tactics inside an existing simulator, MTDSim, as a Petri net that draws its next tactic during the run, mapping eight of the 15 tactics onto MTDSim's six attack actions".
- **What it closes (both from §57):**
  - SQ2's how now names the Petri net, as ch1 and ch4 answer it;
  - mark 3's "in full" has its reason (the draw during the run, Appendix B row 3).
- **Word counts (prose, by label range):** §6.1 492, §6.2 327, §6.3 about 415.
- Build clean, 118 pages, 0 undefined.

## §59. §6.3 ¶3: "draws … during the run" → "chooses … at runtime" (Marc 2026-10-12)

- Ch4 opener verbatim ("the Petri net of its attack profile chooses its next tactic at runtime"); §4.4 also says "chooses".
- "Draws" is Appendix B's word; "during the run" appears only in an Appendix B cell.
- "Chooses" also matches the property name, choice of attack strategy.
- Build clean, 118 pages.

## §60. §6.4 scrutiny (Marc 2026-10-12: "heavily scrutinised … no redraft yet"; nothing applied)

**Rating.** Evidence strong (specific, verified); structure weak; fit with the ch6 rules weak. The material for the section is on the page. It needs a re-sort, not new content.

**Why it reads as a concatenation**
1. No spine. The opener spends three sentences on the section's job and a bound before its claim ("what transfers is that a ranking can depend on the attacker model", S3). The 2026-10-09 plan (dependence → where it travels → what to report → what the numbers cannot decide) mixes axes: P1 is a finding, P2 a case, P3 a reporting duty, P4 the metric plus the deployment interval.
2. Twelve "should"s to four readers: anyone who evaluates MTD, a simulator builder, "a builder", designers of learned deployment strategies. Each gets one sentence of evidence before the next starts.
3. Several implications per paragraph. P1 has three: the ranking belongs to the attacker model; comparability needs shared attacker models; the lowest NCR reduction across attacker models gives a lower bound. It also carries a mechanism, CTI and the bounds. P4 (~380 words) has two: the metric; the interval and its price.
4. About 200 words restate §6.5 or §6.2:
   - the dwell robustness;
   - "the ranking moves because MTDSim writes … against the baseline attacker's procedure" (§6.5's second design choice);
   - the closing bounds of P1;
   - "the attack actions carry an order" (§6.1, §6.5);
   - "MTDSim charges a deployment nothing" (§6.5's third design choice).

**Argument faults**
- a. "Neither of the two attacker models is the better one: each ranking is right for its own." This gives away the contribution. §6.3 scores the APT attacker model with more of the eight properties, and §6.1 closes on it behaving more like an APT. Defensible version: each ranking is correct for its attacker model, and the one to use depends on the attacker the evaluation expects.
- b. The reversal gets two causes on adjacent pages: §6.2 gives the tactic durations and the order of its tactics; P1 gives MTDSim's rules. They read as rival explanations. §6.5 owns the rules bound.
- c. The lowest NCR reduction across the attacker models run is a lower bound over those models only, not against the unknown attacker. Its payoff sits in P4 ("Even the lower bound turns on the metric"), so one argument is split across two paragraphs.
- d. "CTI is one way to cut what an attacker model must assume" overreaches. §6.3 has just said the tactic durations and failure matrix rest on judgement. It is true for the order of its tactics only.
- e. The recommendations generalise from one simulator with no hedge. One scoping sentence in the opener would let every "should" inherit it.
- f. P3 "write attack actions without a fixed order" is an unhedged design prescription, and "without a fixed order" is vague. The meaning is preconditions that do not presume the baseline attacker's procedure.
- g. P3's last sentence (ablate the failure matrix before refining it) is a method lesson for a different reader, tacked on. It belongs in ch7 or is cut.
- h. P2 is the strongest paragraph, and its bound is honest. Two problems:
  - "sits beneath its inputs" is figurative, and the detection-input point is Appendix D detail;
  - S5 and S6 say the same thing (trained-in assumptions; a same-simulator test shares them).

**Terms and back-references**
- "\ref{sq:evaluate} was answered": past tense and passive, read two minutes earlier.
- "the concern of the research question": vague.
- "a quiet attacker" (carried flag): not a ch2–5 term. §6.1 now says "ASP and NCR alone … rate it the weaker attacker".
- **Broken pointer.** P4 cites §6.1 for "MTTC … compares different runs", but §6.1 no longer mentions MTTC.
- "refused" (P3 ×2; also §6.5): not a ch1–5 term. Ch4 l.4606 says an attack action "fails if its preconditions were missing".
- "three choices join the APT attacker model to MTDSim" against §6.3's "four parts we declared". §4.3 has four subsections: the mapping, the tactic durations, the failure matrix and the vulnerability memory.
- "integration work": not a term. Ch4's verb is "integrates" (the loop).
- "has refused what arrives out of it": tense.
- "spent beyond 100 s": undefined. The baseline attacker's host layer is at 0.52 at 100 s, 0.50 at 200 s and 0.17 at 500 s.
- "builder" (P3 end): which builder?
- "says more about the simulator than about user shuffle": rhetorical.
- The Cho sentence nests "the reverse of the case … cited, in which …". It is the section's only disagreement with prior work, it is buried mid-paragraph, and it needs its hedge (a different MTD mechanism and simulator).

**Verified (data/results/ch5_defended/numbers_reported.json)**
- MTDShield against random over its four, at 200 s: 0.68 against 0.56 (baseline attacker); 0.28 against 0.80 (APT attacker model).
- IP shuffle on the baseline attacker at 500 s: NCR reduction 0.39, ASP reduction −0.09. ASP reduction stays negative to 2 000 s.
- User shuffle raises the APT attacker model's NCR at all six deployment intervals (−0.04 to −0.13).
- The host layer halves the APT attacker model's NCR up to 1 000 s (0.52).
- The service layer's peak against the APT attacker model is 0.35. Service diversity alone reaches 0.50 at 50 and 100 s, so "never halves" holds for the layer, not for every MTD mechanism in it.
- ASP reduction of IP shuffle against the APT attacker model at 200 s is 1.0.

**Structure (proposed, not ruled)**
- Conventional shapes are by audience (research or practice) or by finding.
  - By audience does not fit: the audience is one, people who evaluate MTD in simulation.
  - By finding re-walks §6.1–§6.2.
- Proposed: by the decision an evaluator makes. In MTDSim, three decisions each change which MTD mechanism ranks first: the attacker model, the metric and the deployment interval.
- Skeleton (~850 words, against 1 192):
  - opener: the claim and the three decisions, with the one scoping hedge;
  - ¶ the attacker model: ρ and rank-first; ch2 argued it and we measure it; Cho; comparability (Jalowski); report the attacker model with its four declared parts;
  - ¶ learned deployment strategies inherit it (MTDShield);
  - ¶ the metric: blocked against time lost; NCR reduction against ASP reduction; MTTC;
  - ¶ the deployment interval and its price;
  - close, when the attacker is unknown: the lowest reduction across attacker models, which turns on the metric, plus what each deployment takes (the simulator's rules, user shuffle).
- Prose rather than bullets. Optionally, one closing table of what to report, each row tied to its evidence.

**Open for Marc**
- the spine;
- simulator-side recommendations: in the close, or a paragraph of their own;
- a closing table, or prose;
- the rewording of "neither is the better one".

## §61. §6.4 spine, second proposal (Marc 2026-10-12; nothing applied)

**Marc's reply to §60**
- The "three decisions" structure is "OK" but he is not enthused by it. It sorts the content without arguing anything.
- "Neither is the better one" was meant as: with two attacker models, does an evaluator trust the better one or take the minimum of both? That points to a range of models.
- His ramblings need judging on merit, with the overreach stripped.

**Proposed purpose.** §6.4 turns SQ3's answer into what the next person evaluating MTD should do differently. Marc's question is the through-line.

**Proposed chain**
1. **Problem.** A ranking belongs to its attacker model: ρ, no shared first; Hong; Cho; Jalowski.
2. **Consequence.** A deployment strategy learned against one attacker model inherits its ranking (MTDShield).
3. **Answer.** Rank across several attacker models and report each MTD mechanism's lowest reduction.
   - Hinge: §6.3 ¶2. The APT attacker model has more of the eight properties but rests on judgement where MTD disrupts it, so trusting the better one is not safe.
   - Hedge: the minimum is a bound over the attacker models run only.
4. **The minimum turns on the metric and the deployment interval.**
5. **What a range needs.** The four declared parts and the simulator's rules for what each deployment takes.

**Verified: the minimum over the two attackers (numbers_reported.json)**
- **NCR reduction.** IP shuffle is first at all six deployment intervals: 0.88, 0.70, 0.68, 0.39, 0.30, 0.19. That is the APT attacker model's first choice at every interval. Random over MTDShield's four is second at 50 to 200 s.
- **ASP reduction.** Service diversity is first from 100 s: 0.93, 0.83, 0.62, 0.38, 0.25. That is the baseline attacker's first choice (it ties with port shuffle at 100 s). IP shuffle is first at 50 s (0.97).

**Dropped on merit**
- CTI cuts what an attacker model must assume.
- Write attack actions without a fixed order. At most a hedged line in ¶5, or ch7.
- Ablate before refining (ch7).
- The detection-input detail (Appendix D).
- "Neither is the better one" as worded. Its intent becomes ¶3's hinge.

## §62. §6.4 structure from first principles (Marc 2026-10-13: "not sold … vague … what are all the takeaways … what is conventional"; nothing applied)

**Sources read**
- the assembly handoff, §4 (6.4-I1–I6), §14 (six examiners) and §14a (Marc's twelve answers);
- harvest C, M01–M96, held outside the repo;
- harvest D (the UWA rubric, B1–B14, the implications skeleton);
- ch1 (the gap, contribution 2) and ch3 §3.2;
- Table 5.1.

**Where the structure comes from.** Ch3 §3.2 opens: "This section surveys the three parts of an MTD evaluation that use the attacker model \citep{cho2020}": the MTD modelling approaches, the metrics and the evaluation methods. Each subsection ends on a claim about the attacker model that ch5 now tests:
- **Modelling approaches:** "The attacker model therefore decides which deployment strategy is optimal", with Cho's diversity example.
- **Metrics:** ASP, MTTC and NCR depend on how the attacker is implemented (Hong); MTD mechanisms cannot be compared across evaluations (Jalowski).
- **Evaluation methods:** simulation dominates because it models attack behaviours flexibly; simulation results do not transfer.

§6.4 is named after §3.2, so it answers §3.2 part by part. This meets B1 (tie back to ch3) and B6 (engage the literature critically).

**Alternatives set aside**
- **Table 5.1 (varied and held settings).** It is shaped like the experiment, so it replays ch5. It has no home for the metrics. Its held settings (network, target hosts, diversity pool, scenario) are §6.5's external validity.
- **By audience.** There is one audience.
- **"Three decisions" (§60).** Our own sort.
- **Problem → consequence → answer (§61).** Its paragraph jobs were vague.

**Proposed, about 840 words against 1 192**
- **Opener (~60).** The three parts of §3.2 that use the attacker model, and that the results bear on each in MTDSim. One scoping hedge. No "\ref{sq:evaluate} was answered".
- **¶ MTD modelling approaches (~280).** A deployment strategy is optimal only for the attacker model it was found against.
  - ρ −0.24 to 0.25; no shared first rank at any deployment interval. Ch3 argued it; ch5 measures it.
  - Cho's example runs the other way in MTDSim: service diversity ranks first against the baseline attacker and fourth against the APT attacker model at 200 s (Scott–Knott, checked). Hedged: a different MTD mechanism and simulator.
  - MTDShield (machine learning, trained against the baseline attacker): 0.68 against 0.56 and 0.28 against 0.80, beside random over its four.
  - So: test against an attacker model the strategy was not found against.
  - Where the attacker is unknown, rank by the worst case over several attacker models (Marc's "trust the better one or take the minimum"). On NCR reduction that is IP shuffle at every deployment interval. It is a bound over the attacker models run only.
- **¶ Metrics (~250).** A shared metric is not enough to compare MTD mechanisms: the attacker model alone reorders them, so comparison also needs shared attacker models (extending Jalowski). The metrics also read the two attackers differently:
  - ASP and NCR alone rate the APT attacker model weaker (§6.1);
  - attack actions blocked flatter the host layer against the baseline attacker, whose time lost is at or below zero;
  - ASP reduction reaches 1, and splits sign from 500 s;
  - MTTC covers only the runs that reach a target host.

  So: report behaviour beside outcome and time lost beside blocks, and lead with NCR reduction. The worst case turns on the metric (service diversity on ASP reduction from 100 s).
- **¶ Evaluation methods (~250).**
  - Simulation's flexibility makes the attacker model a variable that can be swapped with the networks, MTD mechanisms and seeds held.
  - But the simulator's rules were written for its own attacker: what each deployment takes, the preconditions, and user shuffle. So: report the interface on both sides, the four declared parts and the rules they meet.
  - MTDSim charges nothing for a deployment, so a sweep cannot choose a deployment interval. A defender who sets a threshold of acceptable disruption and a cost could (Marc, M74).
    - Illustration, layer NCR reduction ≥ 0.5: against the baseline attacker, host layer to 100 s and service layer to 200 s; against the APT attacker model, host layer to 1 000 s and service layer at no interval.
  - Transfer to a real network is §6.5's.

**Marc's ideas, triaged on merit**
- **Kept, as above:**
  - M01, M03–M07, M11, M12;
  - M31 and M74, as the threshold illustration;
  - §14a Q2 (optimal is like a model on its training set), Q4, Q6 and Q8 (take the bottom of each).
- **To §6.5:** M08 (no transfer); the held settings; "nothing watches the attacker"; the time limit.
- **To §7.2:**
  - IDS-paired risk-based MTD (Q8);
  - post-intrusion MTD (Q9);
  - technique-level graph ablation (Q1);
  - learned strategies recommending a fixed set (Q6);
  - retraining MTDShield (M72);
  - extending the attack actions (M73);
  - MTD cost and QoS (Q7).
- **Dropped:**
  - "neither attacker model is better" as worded (its intent is the worst case);
  - "CTI cuts the assumptions" (§6.3 owns what CTI gives);
  - "write attack actions without a fixed order" (as a prescription; future work at most);
  - "ablate before refining" (§5.4 and ch7);
  - random as not its members' mean;
  - the detection-input detail (Appendix D);
  - "the rankings invalidate the field" (M07, overreach).

## §63. §6.4 first draft from the §62 structure, applied (Marc 2026-10-13: "structure to first draft ... report the mechanical cuts ... recompile")

**Applied.** §6.4 is now an opener plus three paragraphs, one for each part of ch3 §3.2 that uses the attacker model: MTD modelling approaches, metrics and evaluation methods. The build is clean: 0 undefined references, 118 pages.

**Words** (prose only, comments and macros stripped; this counter reads slightly higher than the label-range count): **1 217 → 945, −272 (−22 %).** Chapter 6 falls by the same amount.

**Mechanical cuts** (low value, low risk; each traced to §60 or §62)
1. Dwell-duration robustness sentence. §6.5 owns it.
2. "The ranking moves because MTDSim writes …": a rival cause to §6.2's. §6.5 owns MTDSim's rules.
3. "Neither of the two attacker models is the better one …" Its intent is now the hinge "an evaluation cannot tell which ranking to trust", with the worst case as the answer.
4. "CTI is one way to cut what an attacker model must assume". It overreached; §6.3 owns what CTI gives.
5. P1's closing bounds: no real network, not the CTI grounding, no recommendation. Now one scope sentence in the opener, with a pointer to §6.5.
6. "The attacker model also sits beneath its inputs …": the detection input. Appendix D owns it.
7. P2's S6, a duplicate of S5 (same simulator, same assumptions). Merged into the test-set analogy.
8. P3's opener, "Joining … is integration work".
9. "The attack actions also carry an order … A simulator builder should write attack actions without a fixed order." §6.1 and §6.5 own the order; the prescription was dropped.
10. "… which says more about the simulator than about user shuffle" (rhetorical).
11. "Without the interface, a reader cannot trace a ranking to its assumptions" (merged).
12. "The failure matrix moves NCR negligibly, so a builder should ablate …". §5.4 and ch7.
13. "Even the lower bound turns on the metric …": merged into one sentence at the end of the metrics paragraph.
14. The lineage-interval sentence ("judge the host layer spent beyond 100 s …"). Replaced by the threshold reading.

**Fixes carried in**
- "a quiet attacker" is replaced by §6.1's wording ("ASP and NCR alone rate the APT attacker model the weaker attacker for behaving more like an APT").
- The MTTC pointer now cites Equation 4.x (eq:mttc) in place of §6.1.
- "Three choices" is now the four parts named (Section 4.3).
- "Refused" is gone.

**Added** (all from §62)
- one topic sentence per §3.2 part;
- the Cho example's hedge (the two MTD mechanisms differ);
- the trust-or-worst-case hinge, which cites Table 6.1 and §6.3;
- Hong's "computed from what the attacker does";
- the deployment-interval threshold reading. At an NCR reduction ≥ 0.5 (Table E.1 layer means):
  - host layer: to 1 000 s against the APT attacker model and to 100 s against the baseline attacker;
  - service layer: to 200 s against the baseline attacker, and at no deployment interval against the APT attacker model.

**Next.** Marc reads it in the PDF. Then a scrutiny round paragraph by paragraph, then a clarity pass on the flagged sentences only.

**Retired overdraft (2026-10-09 prose, verbatim, for recovery):**

```latex
\ref{sq:evaluate} was answered for the APT attacker model in MTDSim. This
section states what the answer means for anyone who evaluates MTD against APT
attackers, the concern of the research question. One simulator on its default
network cannot transfer its numbers or its rankings; what transfers is that a
ranking can depend on the attacker model. Chapter~\ref{ch:litreview} argued
that the attacker model decides which deployment strategy is optimal
(Section~\ref{subsec:defence-modelling-approaches}), and that ASP, MTTC and
NCR depend on how the attacker is implemented \citep{hong2018}; we measure
it. On the same simulator, networks, MTD mechanisms and seeds, no MTD
mechanism or deployment strategy ranks first against both attackers at any
deployment interval, and $\rho$ between the two rankings lies between $-0.24$
and $0.25$ (Section~\ref{subsec:eff-cross-arm}). At 200\,s, this holds with
the 45\,s mean duration at both ends of its band
(Appendix~\ref{app:dwell-robustness}). At 200\,s, service diversity ranks first
against the faster baseline attacker and fourth against the APT attacker
model, the reverse of the case Section~\ref{subsec:defence-modelling-approaches}
cited, in which migrating a service across diverse platforms defends against
persistent attacks but can weaken the defence against fast ones
\citep{cho2020}. The ranking moves because MTDSim
writes what each deployment takes against the baseline attacker's
procedure, which the APT attacker model does not follow
(Section~\ref{sec:disc-mtd-performance}). An optimal MTD mechanism is
therefore optimal for one attacker model in one simulator, and an evaluation
should report its ranking with the attacker model behind it and the
assumptions that model and the simulator make. Neither of the two attacker
models is the better one: each ranking is right for its own.
Chapter~\ref{ch:litreview} also found that MTD mechanisms cannot be compared
across evaluations, because each evaluation chooses its own metrics
\citep{jalowski2026}. Here the metric is shared and the attacker model alone
reorders the MTD mechanisms, so comparability also needs shared attacker
models. Where the attacker is unknown, an evaluation can run several
attacker models and take each MTD mechanism's lowest NCR reduction across
them as its lower bound. No one attacker model sets that bound throughout:
at 200\,s the APT attacker model sets it for the service layer, and the
baseline attacker for the host layer (Table~\ref{tab:eff-interval-values}).
CTI is one way to cut what an attacker model must assume, because it records
what attackers did. The results do not say which ranking holds on a real
network, nor that the grounding in CTI caused the reversal
(Section~\ref{sec:threats}), and they recommend no MTD mechanism.

The dependence reaches deployment strategies. MTDShield was trained against
the baseline attacker and chooses service diversity at 70\,\% or more of its
decisions (Appendix~\ref{app:mtdshield-observed}), the only MTD mechanism the
baseline attacker loses time to (Section~\ref{sec:disc-mtd-performance}). At
200\,s it beats random over the same four MTD mechanisms against the baseline
attacker, 0.68 against 0.56, and loses to it against the APT attacker model,
0.28 against 0.80 (Table~\ref{tab:eff-interval-values}). The
attacker model also sits beneath its inputs: the detection input codes the
attacker's current attack action, so an unmapped tactic of the APT attacker
model reads as nothing detected (Appendix~\ref{app:mtdshield-limitations}).
A learned deployment strategy is only as faithful as the attacker model,
network and MTD cost it is trained in, so it should be tested beside random
over the same MTD mechanisms, against an attacker model it was not trained
on. A test in the same simulator against the same attacker model shares the
assumptions the agent was trained on, so it cannot show that the agent
generalises. The evidence is one agent, Tay's as released and not retrained,
with four of its inputs at zero at every decision
(Appendix~\ref{app:mtdshield-limitations}). It shows the risk of fitting one
attacker model; whether MTDShield was fitted to one, this run cannot tell.

Joining a new attacker model to a simulator is integration work, so an
evaluation should report the interface on both sides. On the attacker's side,
three choices join the APT attacker model to MTDSim: the mapping from tactics
to attack actions (Section~\ref{subsec:tactic-verb-mapping}), the tactic
durations anchored on MTDSim's times (Section~\ref{subsec:dwell-times}), and
the failure matrix that reweights the next tactic after a failed attack action
(Section~\ref{subsec:failure-matrix}). Each is a declared assumption, and an
evaluation should report them with the tactics left unmapped and the attack
actions refused. The attack actions also carry an order: each of MTDSim's
relies on the state the one before it leaves, so every attacker model that
adopts them inherits the order, and has refused what arrives out of it
(Section~\ref{sec:disc-behaviour}). A simulator builder should write attack
actions without a fixed order. On the defender's side, an evaluation should
report what each deployment takes from the attacker. User shuffle raises the
APT attacker model's NCR at every deployment interval
(Table~\ref{tab:eff-interval-values}) because of the rule MTDSim gives it
(Appendix~\ref{app:fa-accounts}), which says more about the simulator
than about user shuffle. Without the interface, a reader cannot trace a
ranking to its assumptions. The failure matrix moves NCR negligibly
(Section~\ref{sec:ablation}), so a builder should ablate a component
like it before refining its values.

The metric an evaluation reports decides part of its answer. Read alone, ASP
and NCR call a quiet attacker weak (Section~\ref{sec:disc-behaviour}), so an
evaluation should report what the attacker does
(Section~\ref{subsec:metrics-behaviour}) beside what it achieves. Counting the
attack actions MTD blocks would rank the host layer the most disruptive
against the baseline attacker, whose mean time lost to it is at or below zero
(Section~\ref{sec:disc-mtd-performance}), so an evaluation should report the
time lost per MTD deployment beside it. Of the outcome metrics, NCR reduction
counts hosts in every run, while ASP reduction rests on the few runs that
reach a target host and reaches its ceiling of 1 against the APT attacker
model (Table~\ref{tab:eff-interval-values-asp}). An evaluation of an attacker
that rarely reaches its target should therefore lead with NCR reduction and
report ASP reduction beside it. MTTC covers only the runs that reach a
target, so between attackers that differ in attack rate and ASP it compares
different runs (Section~\ref{sec:disc-behaviour}); it should be reported with
the share of runs it covers. NCR reduction and ASP reduction agree on the
reversal, but not always in sign: from 500\,s, IP shuffle reduces the
baseline attacker's NCR by 0.39 and raises its ASP, an ASP reduction of
$-0.09$ (Tables~\ref{tab:eff-interval-values}
and~\ref{tab:eff-interval-values-asp}), so under it the baseline attacker
compromises fewer hosts but reaches a target host more often. Even the lower
bound turns on the metric. Taking each MTD mechanism's worse value over the
two attackers, IP shuffle is highest on NCR reduction at every deployment
interval, and service diversity on ASP reduction from 100\,s. The deployment
interval depends on the attacker model too. The earlier MTDSim studies ran
50 to 200\,s (Table~\ref{tab:lineage-configurations}), where both MTD layers
reduce the baseline attacker's NCR; an interval chosen against the baseline
attacker would judge the host layer spent beyond 100\,s, though it halves the
APT attacker model's NCR up to 1\,000\,s, and rely on a service layer that
never halves the APT attacker model's NCR (Table~\ref{tab:eff-interval-values}).
An interval
also needs a price. MTDSim charges a deployment nothing, so a sweep shows
where MTD stops reducing an attacker's NCR but cannot choose an interval; an
evaluation that sets one should model the overhead and loss of service each
deployment costs.
```

## §64. §6.4: pointers from each paragraph to its §3.2 subsection (Marc 2026-10-13, "fine with the proposed")

- Each paragraph's second sentence, the one that says what ch3 claimed, now points to its subsection, not to "Chapter 3":
  - §3.2.1 (subsec:defence-modelling-approaches);
  - §3.2.2 (subsec:mtd-metrics);
  - §3.2.3 (subsec:evaluation-methods).
- The opener still cites §3.2 for the three parts. That covers the bare "On X," openers, which follow the convention of §6.1 and §6.2: a term is defined once and repeated word for word, with no citation on each use.
- Bold run-in headings were considered and set aside. They would make §6.4 the only ch6 section with them, and the examiner benchmarks call for no headings below the section.
- Build clean, 118 pages.

## §65 — §6.4 opener: placeholder (Marc 2026-10-13)

Scrutiny of the first-draft opener: it opened on what Chapter 3 did (a roadmap, no claim); "the results bear on each" names nothing; the bound sentence repeats the chapter preamble and §6.5; its "so" did not follow. A first redraft ("the attacker model alone changes which MTD layer reduces NCR most … this section states what that means") was rejected as a flourish plus a signpost.

Placed as a **placeholder** (Marc: "just put that in ... a placeholder for now"):

> In MTDSim, the service layer reduces the baseline attacker's NCR most and the host layer the APT attacker model's (Section 6.2), so an MTD evaluation run against the baseline attacker alone picks the MTD layer that reduces the APT attacker model's NCR less. For each of the three parts of an MTD evaluation that use the attacker model (Section 3.2), an evaluation should therefore change one thing: test a deployment strategy against more than one attacker model, report the attacker's behaviour beside the metrics, and report the rules that join its attacker model to the simulator.

Open (Marc): the three recommendations read as "we already do that". Settle them in the paragraph redrafts, then rewrite the opener's list to match. Build clean, 118 pages, 0 undefined.

## §66 — §6.4 ¶1 (MTD modelling approaches): scrutiny, no redraft (Marc 2026-10-13)

**Job.** Answer §3.2.1: "the attacker model decides which deployment strategy is optimal … a deployment strategy found against another attacker may not be optimal against [an APT attacker]".

**What §3.2.1 set up, and what the results can test.**

| §3.2.1 point | Tested here? |
|---|---|
| Game theory assumes a rational attacker | No: no game-theoretic deployment strategy was run |
| Genetic algorithms: the attacker is only the fitness function | No |
| Machine learning: the attacker is the training environment's; MTDShield's is the baseline attacker | Yes: MTDShield, the only deployment strategy here found by an MTD modelling approach |
| The attacker model decides which deployment strategy is optimal | Yes, but on the proactive schedules (random, alternative, single; ch2, near tab:deployment-strategies: "follow a schedule, so they are proactive"), which no MTD modelling approach found |
| Cho's migration example | Not directly: no MTD mechanism migrates a service |
| An APT attacker is persistent, so a strategy found against another may not be optimal | Yes: MTDShield |

**Reading.** ~400 words, five ideas, two "should"s, ordered as discovered, not by weight: (1) claim + ρ; (2) Cho inverts (hedged to nothing); (3) MTDShield + the test-set recommendation + its bound; (4) which ranking to trust; (5) rank by the lowest NCR reduction. The strongest evidence, MTDShield, comes third; the weakest, Cho, second. Ideas 4–5 answer a different question (what to do when the attacker is unknown).

**Facts.**
- X1 "chooses service diversity at 70 % or more of its decisions": true at 200 s (76 %, 70 %), false at 2 000 s (46 %, 65 %) (app:mtdshield-observed). Scope it to 200 s.
- X2 "0.68 against 0.56", "0.28 against 0.80": the metric is unnamed (NCR reduction).
- X3 "no MTD mechanism or deployment strategy ranks first against both attackers at any deployment interval": holds (mean rank 1: IP shuffle against the APT attacker model, service diversity against the baseline attacker, at all six; ch5_defended/numbers_reported.json sweep.by_interval.*.ranks), but §5.3.2's prose states 200 s only.
- X4 "the faster baseline attacker": "faster" is not a ch5/ch6 term, and equating it with Cho's "fast" attacks is a stretch.
- X5 IP shuffle first on the lowest NCR reduction across the two attackers: no float shows it; the reader must compute it from Table E.1.

**Sentences.** "the results measure it" (unresolved "it"); "runs the other way", "inherits", "beats" (figurative); "found against" (vague for schedules); the test-set sentence stacks three clauses; "four of its inputs at zero" duplicates §6.5's "MTDShield runs as released" (keep the one hedge "cannot tell whether MTDShield is fitted to the baseline attacker"); "rests on our judgement where MTD disrupts it" (which judgement?); "a bound over those attacker models only" ("bound" is §6.5's word for limits).

**Direction (no text yet).** One claim: a deployment strategy found by an MTD modelling approach is optimal for its attacker model, and MTDShield shows it. Order: §3.2.1's claim → the choices a modelling approach optimises over rank differently (ρ, one sentence) → MTDShield → so what (test a learned deployment strategy against an attacker model other than its training one, beside random over the same MTD mechanisms) → one hedge. Cho: cut, or one clause. Ideas 4–5: Marc to rule (own short paragraph, §7.2, or cut). Target ~200 words.

## §67 — §6.4 ¶1 redraft applied (Marc 2026-10-13: "90% the way there")

Two rounds after §66. Round 1 (critique): the opener abstracted ("one attacker / another") where the evidence is named; one vocabulary per job (MTD terms for the subject, MTDSim for the evidence, RL only for learning; no CTI); "trained against the baseline attacker" folded into the §3.2.1 sentence (ch3 says it); "of the four MTD mechanisms" and first/third ranks cut (no scale; the reader met service diversity via §6.2: the only MTD mechanism the baseline attacker loses time to); comparator = the plain random deployment strategy (Figure 5.x(d) vs (e)), which holds at every deployment interval both ways (Table E.1: baseline 0.84/0.67 ... 0.05/-0.01; APT 0.42/0.95 ... 0.04/0.08); the same-four comparator gives the same direction (0.56, 0.80 at 200 s) and stays only in the should; NCR reduction read as a percentage of NCR (eq:ncr-reduction); 76/70 % -> "most of its decisions" (ch5 states the shares); the simile names the training environment; "disrupts" not "reduces NCR most" (the reward is not NCR). Round 2 (clarity, three sentences): "but" in the opener (random is the bar); "reduces ... by 68 %" (the flip 68->28 vs 33->75); "generalises to other attackers" vs "fitted to its training attacker".

218 words (was 353). Build clean, 118 pages, 0 undefined.

## §68 — §6.4 ¶2 (metrics): scrutiny, no redraft (Marc 2026-10-13: "same process ... efficiency ... we don't model")

**Job.** Answer §3.2.2.

| §3.2.2 point | What ¶2 does now |
|---|---|
| Cho's taxonomy: effectiveness or efficiency, attacker-side or defender-side (tab:mtd-metrics) | Silent. Every metric here is an effectiveness metric (ASP, MTTC attacker-side; NCR, attack actions blocked defender-side; time lost per MTD deployment, which §4.5 groups with NCR reduction). No efficiency metric: MTDSim prices nothing (§6.5). |
| ASP is the dominant effectiveness metric | Not used, though it is the hook for ASP reduction's ceiling and sign flip. |
| No standard set, so MTD mechanisms cannot be compared across evaluations (Jalowski) | Extended: shared attacker models are needed too. Its evidence, ρ, left with ¶1's redraft (§67), so the claim now has none in ¶2. |
| ASP, MTTC, NCR depend on how the attacker is implemented (Hong) | Confirmed ("read the two attackers differently"). |

**Reading.** 271 words, 10 sentences, five recommendations: report behaviour beside outcome; report blocks with time lost; lead with NCR reduction; ASP reduction and MTTC beside it, MTTC with its share of runs; the worst case moves with the metric. Same shape as the old ¶1: a list of caveats, each with its own "so". Rehash: "ASP and NCR alone rate the APT attacker model the weaker attacker for behaving more like an APT" is §6.1's close word for word; blocks against time lost is §6.2's; MTTC's coverage is eq:mttc's definition. The worst-case tail is orphaned now ideas 4–5 are parked (§66).

**Marc's efficiency point (the gap).** MTDSim charges a deployment nothing, so effectiveness is all it measures. In Table E.1, no MTD mechanism or deployment strategy that reduces NCR reduces it more at a longer deployment interval (beyond 0.01: OS diversity 0.18 -> 0.19, 0.92 -> 0.93), so on effectiveness alone the shortest deployment interval always ranks first, and an interval sweep cannot choose one. The attacker model moves the interval a defender would need: §5.3.2 already states that the host layer's NCR reduction stays above 0.5 up to 1 000 s against the APT attacker model, and the service layer's only up to 200 s against the baseline attacker. This is now in ¶3 (evaluation methods) with the threshold illustration; it belongs to metrics (Cho's efficiency half). §6.5 keeps the bound ("MTDSim prices nothing").

**Points ranked by strength.**
1. Efficiency: not measured; without it the shortest interval always wins; the attacker model moves the interval needed (Marc; ties to Cho's taxonomy; misfiled in ¶3).
2. Comparability needs a shared attacker model (Jalowski extended; ρ as evidence).
3. ASP, the field's dominant metric, reaches its ceiling of 1 (APT attacker model, host layer, to 200 s) and disagrees in sign with NCR reduction (IP shuffle, baseline attacker, 500 s: 0.39 vs −0.09), so lead with NCR reduction.
4. Behaviour metrics beside outcome (Cho's taxonomy has no behaviour metric; M12) — worded as §6.1's sentence now.
5. Blocks against time lost (§6.2 made it).
6. MTTC covers only the runs that reach a target host (definition; MTTC is thin in ch5).
7. The worst case moves with the metric (orphaned; parked with §66's ideas 4–5).

**Direction (no text).** One claim across both halves of Cho's taxonomy: what the metrics say depends on the attacker model. Effectiveness (measured): the two attackers order the MTD mechanisms differently (ρ) and ASP disagrees with NCR reduction. Efficiency (inferred, one hedge): not measured, so the shortest deployment interval always wins, and the attacker model sets how often MTD must be deployed. Cut 4–7 or leave each to its home. Move the efficiency material out of ¶3. Marc to rule on the spine and on keeping 3 and 4.

## §69 — §6.4 ¶2 (metrics): the thread and a spine (Marc 2026-10-13: "really think this one through"; no text)

**Method.** §3.2.2 dissected sentence by sentence against the results and Marc's points (ASP is blunt, success is not impact; no behaviour metrics because evaluations run one attacker model; efficiency unmodelled; metrics are ad hoc and so are ours).

**The thread.** Ch4, subsec:tactic-verb-mapping: "MTDSim's attacker stops at compromising hosts, so Collection, Exfiltration and Impact have nothing to act on." Every metric reported stops there too: ASP (the share of runs that reach the goal, a target host compromised; eq:asp), MTTC (time to it), NCR (share of hosts compromised; eq:ncr), attack actions blocked and time lost per MTD deployment (attack actions toward it). So the metrics measure progress toward compromising hosts: the baseline attacker's whole goal, and only part of the APT attacker model's (its attack profiles' objectives, exfiltration and impact, lie past it). Cho's classification has cells for the rest — attack utility (attacker-side effectiveness), attack and defence cost, QoS (efficiency) — and MTDSim fills none.

**Section-wide thread (for the opener, later).** Each part of an MTD evaluation that uses the attacker model was built around the baseline attacker in MTDSim: MTDShield was trained against it (¶1), the metrics stop where it stops (¶2), and MTDSim's rules for what each deployment takes follow its procedure (¶3). Candidate one-liner for the placeholder opener (§65).

**Spine (slots, no text; ~230 words).**
1. Claim: every metric here counts progress toward compromising hosts, where MTDSim's attacker stops (§4.3 mapping, eq:asp, eq:ncr).
2. §3.2.2: ASP is the dominant metric; values depend on the attacker (Hong); Cho's classification also has what the attacker gains and what MTD costs (tab:mtd-metrics).
3. Attacker side: ASP counts a run once it reaches a target host, whatever the attacker does next; it reaches its ceiling of 1 (APT attacker model, host layer, to 200 s) and disagrees in sign with NCR reduction (IP shuffle, baseline attacker, 500 s: 0.39 vs −0.09). Why ch5 leads with NCR reduction. ASP and NCR rate the APT attacker model weaker (pointer to §6.1, no restatement); the behaviour metrics (§4.5.1), a kind the classification lacks, show what the outcome misses.
4. Defender side: no efficiency metric (MTDSim prices nothing, §6.5); on effectiveness alone the shortest deployment interval always ranks first (Table E.1), and the attacker model moves the interval needed (§5.3.2: host layer above 0.5 to 1 000 s against the APT attacker model; service layer to 200 s against the baseline attacker). Hedge here (the cost side is inferred).
5. So (ad hoc): §3.2.2 found metrics chosen per evaluation (Jalowski); this dissertation chose its own too; with the metrics shared, the attacker model still reorders the MTD mechanisms (ρ −0.24 to 0.25). One should: comparing MTD across evaluations needs a shared attacker model as well as shared metrics.

**Out.** Blocks against time lost (§6.2); MTTC coverage (definition); the worst case by metric (parked, §66); the threshold illustration's service-layer-never clause (§5.3.2 carries the numbers).

**To verify before drafting.** "Evaluations run one attacker model" (Marc): check §3.3's surveyed evaluations (Table 3.3 rows) before any sentence claims it; otherwise scope it to the evaluations surveyed or drop it.

## §70 — §6.4 ¶3: cost and threshold sentences cut (Marc 2026-10-13, "apply those cuts to paragraph three")

99 words removed ("MTDSim also charges an MTD deployment nothing ... (Table E.1)"); the efficiency point moves to ¶2 (draft pending, §69). Until ¶2 is applied the PDF carries no efficiency point. Build clean.

## §71 — §6.4 ¶2 redraft applied as ¶2a and ¶2b (Marc 2026-10-13: "the structure is right ... a 2a and 2b might make sense")

Critique of the 320-word draft (Marc: "not as hard hitting ... clause, clause ... collection of facts"): S1 abstract ("every metric ... progress") -> names ASP and NCR and what each counts; the four-clause S2 split, thread first ("They stop where MTDSim's attacker stops"), then the attack profiles (c1-c3 pursue exfiltration or impact; Collection, Exfiltration, Impact run no attack action); ch3 facts placed beside the result each sets up; "the bluntest" cut; IP shuffle told as the story (fewer hosts compromised, more runs that compromise a target host) with both numbers in the tables' format; behaviour = "Cho et al.'s classification has no metric of attacker behaviour; §4.5.1 adds four"; efficiency in §6.5's words (no overhead or loss of service); "priced each deployment" -> the threshold: every 1 000 s vs every 200 s, five times as often; the so-what before the should ("A ranking of MTD mechanisms holds for the attacker model it was measured against").

Applied: ¶2a (250 words; one should: report against an existing attacker model) and ¶2b (119 words; efficiency; one hedge: "would therefore likely change what MTD costs"); plus "so a sweep of deployment intervals cannot choose one" (from the cut ¶3 sentence). Old ¶2 271 + ¶3's cut 99 = 370 -> 369. Build clean, 118 pages, 0 undefined.

## §72 — §6.4 ¶2a v2 (238 words, not applied): critique before the last sentence (Marc 2026-10-13)

**Checks.** ASP reduction and NCR reduction across Tables E.1/E.2 (11 rows x 12 cells): Spearman 0.92 (APT attacker model 0.98, baseline attacker 0.91); same sign in 128 of 144 cells. The IP shuffle 500 s example (§68-§71) was one of the 16 disagreements: selective, rightly dropped. Appendix E (app, eq:asp-reduction) already gives the ranking reason: "At 200 s, ASP reduction shows the order of NCR reduction, and reaches its ceiling of 1 against the APT attacker model, whose ASP with no MTD is low, so Chapter 5 ranks on NCR reduction." §4.5 (sec:evaluation-metrics) already says "None of them measures how an attacker behaves, so none shows whether an attacker model has the properties it needs to model an APT attacker. We add attacker behaviour metrics ..." Ch4's three families: attack outcome, MTD effectiveness, attacker behaviour. Ch4's objectives: steal data, impede systems (Table 4.x columns "Stole data", "Impeded systems"); the tactics Collection, Exfiltration, Impact have "no attack action in MTDSim".

**Discussion point on ASP (de-risked).** Not "ASP is wrong": the two agree on direction; ASP reduction loses resolution against an attacker that seldom reaches a target host (APT attacker model, host layer: 1.00 to 200 s), which is how an APT-like attacker scores (§6.1). The field's dominant metric is weakest exactly against the attacker this dissertation models. Point to Appendix E for the ranking choice.

**Per sentence and noun audit:** see the chat return of 2026-10-13 (sentence table, noun table); direction: S1 keep; S2 cut the scenario clause, NCR in ch4's words ("hosts in the network"); S3-S5 merge to one sentence in ch4's objective words ("steal data or impede systems ... no attack action"), "measures" not "counts"; S6-S7 replace "one outcome per run" with the ceiling point (agree on direction, ceiling against an attacker with low ASP; Appendix E); S8-S9 plain: a shared set of metrics would not make MTD evaluations comparable, since on NCR reduction alone service diversity scores 92 % vs 36 %; S10 keep (attack outcome metrics lower, more of the eight properties); S11 cut "rank attackers by what they compromise" (S10 says it); the behaviour-metric gap points to §4.5 (said there), the results confirm it. Last sentence parked by Marc.

## §73 — §6.4 ¶2a v5 (264 words, not applied; Marc: "a lot tighter ... a good draft"): point critiques

1. **Last sentence** ("report the attacker's behaviour ... resembles an APT"): not actionable, invites optimism (Marc). His alternative: define the attacker model in its own right (what it does, its assumptions). Grounding: Jalowski §4.3 p. 8, full quote "the ill-defined attacker models, which are often too simplistic or based on completely unrealistic assumptions" (ch3 quotes only "the most glaring flaw"); tay2024 extraction l.149: the executed attacker is specified in one sentence. Instrument the dissertation already provides: the eight properties (Table 3.3, Table 6.1). Candidate: state the attacker model and its assumptions in their own right, and score it on the eight properties as Table 6.1 does.
2. **"under the host layer it reaches its ceiling of 1"**: the reader cannot tell what 1 is. Plain: under the host layer, no run of the APT attacker model compromises a target host up to 200 s.
3. **Weight of the ASP block** (~95 of 264 words) for a side branch. Option: two sentences (~55 words), dropping "rests on those 42 to 139 runs" and leaving "same order" to Appendix E. Marc to rule.
4. **"Section 4.5 added attacker behaviour metrics for this reason"** reverses time: §4.5 predicted it, the result confirms it.

## §74 — §6.4 ¶2a applied (Marc 2026-10-13: "apply it")

Rulings on §73: (2) "under the host layer in no run up to 200 s"; (3) the ASP block in two sentences (resolution: few runs, then none, so rank on NCR reduction, which counts hosts in every run); (4) "Section 4.5 expected this when it added attacker behaviour metrics" (own sentence). Last sentence: no Jalowski "ill-defined" lean, no eight-property standard (Marc: "everyone should use my standard ... cliche"); "set out its attacker model and that model's assumptions in a section of their own, where a reader can examine them, as it sets out its MTD mechanisms." Clarity pass: attack profiles' owner named; ch4 objective names (data exfiltration, impediment); "ranks the MTD mechanisms"; fronted modifiers moved; "it rests on" ambiguity removed; dangling "where" fixed. 241 words (was 250). No hedge. Build clean, 118 pages, 0 undefined.


## §75 — §6.4 ¶2a last sentence and ¶2b: scrutiny, no drafting (Marc 2026-10-13)

**¶2a last sentence (Marc: "a disjoint recommendation ... how does the conclusion come from the substance?").** Not a softening problem: the sentence overclaims nothing; a step is missing. The paragraph shows that the attacker model sets what the effectiveness metrics can show (no attack action for the objectives; ASP's few runs; weaker attacker on outcome metrics; 92 % vs 36 % on one metric) but never says so, and "therefore" attaches only to the sentence before it. "A section of their own" is a reporting-format claim with no premise in the paragraph. One-liner: *in MTDSim the attacker model sets what the effectiveness metrics can show, so a reader needs the attacker model to read them.* Fix: lead with that claim (opener names Cho's effectiveness family, so 2a/2b mirror Cho's two families from §3.2.2); end with what the section must hold, taken from the paragraph's own evidence (the tactics the attacker model has attack actions for; its results with no MTD), so the should is derived, not inserted. Side flag: the 92/36 pair is the third use (abstract l.210, ch1 l.463); a pointer to §6.2 is an option.

**¶2b one-liner:** *MTDSim has no efficiency metrics, yet the attacker model still sets how often MTD must deploy for a given NCR reduction, and so what it would cost.* Split justified by Cho's classification (2a effectiveness, 2b efficiency).

**Checks (numbers_reported.json, sweep layer means, intervals 50/100/200/500/1000/2000):** APT host 0.98 0.96 0.96 0.79 0.52 0.24; baseline service 0.97 0.97 0.84 0.27 0.19 0.11; baseline host 0.72 0.52 0.49 (CI 0.48-0.51) 0.16; credentials (user shuffle) vs APT -0.13 -0.11 -0.10 -0.06 -0.06 -0.04, rising toward zero. Deployments executed per run: 131.6, 99.5, 75, 30, 15, 8 (same for both attackers).

**Per sentence.**
- S1: leads with Cho, not the point; restates ch3's efficiency definition; "charges ... no overhead" is §6.5's third bound almost word for word ("MTDSim prices nothing. A deployment costs no overhead or loss of service"); "quality of service" then "loss of service" (two terms). Point to §6.5.
- S2: three clauses; "always better" is a verdict word and false for user shuffle against the APT attacker model; "a sweep ... cannot choose one" is said in §6.5 and in ch7 future work F11. Bound, so §6.5's.
- S3: the only new claim. "Five times as often" is a grid artefact: the crossings lie between tested intervals (baseline service 200-500 s, APT host 1,000-2,000 s), so the true ratio is 2 to 10; "must deploy every 200 s" overstates (200 s is the longest tested interval). Compares different layers, whose per-deployment cost differs, so deployment frequency is not cost. Same-layer alternative (host layer: 1,000 s vs 100 s) is fragile: baseline host at 200 s, 0.495 (CI 0.48-0.51), straddles 0.5. The two numbers stand; drop the ratio. Ch5 §5.3.2 already gives both numbers.
- S4: double hedge ("would ... likely"); "costs as well as achieves" pairing; no should, so no so-what (¶1 and ¶2a end in one).
- Candidate should (actionable now, distinct from ch7 F11): with no cost model, report per MTD mechanism the longest deployment interval that reaches a stated NCR reduction against each attacker model, with the deployments per run, so a reader can price them at their own cost per deployment. One hedge on the cost inference.

**Gated flag (ch7):** the Contribution 2 draft note's "1,000 s against 100 s ... ten times longer" (host layer, same-layer) rests on baseline host 0.52 at 100 s and 0.495 at 200 s with the CI straddling 0.5; the same grid-artefact caution applies.

## §76 — §6.4 ¶2a opener and close, ¶2b redraft applied for Marc's evaluation (2026-10-13: "push both and I will evaluate")

¶2a: new opener "On metrics, the attacker model decides what the effectiveness metrics can show." (claim first; Cho's effectiveness family, mirrored by 2b's efficiency); close "set out its attacker model in a section of its own, as it sets out its MTD mechanisms. A reader needs three things from that section to read the metrics: the tactics the attacker model has attack actions for, its ASP and NCR with no MTD, and its assumptions." ("where a reader can examine them" cut). ~265 words, no hedge.

¶2b redraft (~110 words, was 119): claim first ("the attacker model still decides how often MTD must deploy for a given NCR reduction"); §6.5's no-cost bound as a pointer; host layer vs APT attacker model > half up to 1,000 s, service layer vs baseline attacker only up to 200 s (§5.3.2's phrasing); "five times" and "must" dropped; one hedge ("likely changes what MTD costs"); should: report the longest deployment interval at which each MTD mechanism reaches a stated NCR reduction, against each attacker model, so a reader can apply their own cost per deployment. Deployments per run (15 at 1,000 s, 75 at 200 s in numbers_reported.json) kept out: printed in no float, and counts fall below schedule at 50 and 100 s. Open: "its most effective layer" left implicit (Marc to rule).

Build clean, 118 pages, 0 undefined. Pending Marc's evaluation.


## §77 — §6.4 ¶2a structure critique, no drafting (Marc 2026-10-13: "a step back ... run the wringer through paragraph one ... the structure or the narrative has been lost")

**Verdict.** The wording is not the problem. Since §72 the paragraph has drifted from §69's spine ("with the metrics shared, the attacker model still reorders the MTD mechanisms (ρ); comparing MTD across evaluations needs a shared attacker model as well as shared metrics"). ρ left ¶2a when ¶1 was redrafted (§67). ASP-floor and actions-on-objectives material filled the gap, so ¶2a now carries two threads: (A) which metric fits the attacker model (S2-S7) and (B) comparability across evaluations (S8-S9). The should comes from B and the three-item list from A, which is why the close reads disjoint.

**Structural faults.**
1. The order is inverted against ¶1's pattern (result, then what ch3 said, then numbers, then mechanism, then should). The ch3 anchor arrives at S8 of 11 and the strongest evidence (92 % vs 36 %) at S9. The paragraph leads with its weakest material: definitions and a simulator bound.
2. It is missing ch3's own prediction. §3.2.2 P2 (Hong: metric values depend on how the attacker is implemented; "MTD that is effective against one attacker may therefore not be effective against an APT attacker") is the claim the results confirm, and the paragraph never closes that loop.
3. It is missing the strongest evidence. Switching the metric keeps the order: at 200 s, ASP reduction shows the order of NCR reduction (Appendix E; §72: Spearman 0.92, 128/144 same sign, unprinted). Switching the attacker loses it: ρ between the attackers' NCR reductions is 0.01 [−0.19, 0.05] at 200 s and lies between −0.24 and 0.25 at every interval (§5.3.2). So the attacker model moves the conclusion more than the metric choice does. §6.5 (l.~9282) already points to §6.4 for "a ranking carries the assumptions of its attacker model", so §6.4 owes this claim.
4. The should does not follow from the evidence. A section describing the attacker model makes 92 % vs 36 % explainable, not comparable. The three-item list (tactics with attack actions, ASP and NCR with no MTD, assumptions) is tied to MTDSim's metrics: a game-theoretic evaluation reads payoffs and needs none of it (Marc). "Assumptions" is vague.

**Per sentence.**
- S1 "decides what the effectiveness metrics can show": names no result; two vague verbs.
- S2 (what ASP and NCR count): restates §4.5. It is needed only for S3.
- S3 (actions on objectives): a simulator bound. §6.3 says it (l.~8582, l.~8894), and bounds live in §6.5. If MTDSim cannot run the objectives, no metric could measure them, so this is not a metrics finding.
- S4 (ASP 4-14 %, none under the host layer to 200 s): a true and sharp point, but it is Appendix E's and §6.5's ("so the ranking uses NCR reduction").
- S5 (Chapter 5 ranks on NCR reduction): a method justification, the third statement (Appendix E, §6.5).
- S6-S7 (the APT attacker model scores weaker; §4.5 expected this): a third thread (behaviour metrics), §6.1's close per §68. S7 is self-reference.
- S8-S9: the paragraph's real claim and evidence, at the end.
- S10-S11: see fault 4.
- About 265 words, the longest paragraph in §6.4.

**Spine proposed (slots, no text; ~150 words).**
1. Claim: on the same networks, the attacker model changes which MTD mechanisms rank first, and the choice of metric does not (ρ, §5.3.2; ASP reduction's order, Appendix E).
2. §3.2.2: no standard set, so no comparison (Jalowski); values depend on the attacker (Hong). The results show the second is the larger cause.
3. One concrete case: service diversity, 92 % vs 36 % at 200 s (Table eff-cross-arm). The layer flip itself is §6.2's (pointer).
4. So what: a standard set of metrics alone would not make MTD mechanisms comparable across evaluations. One hedge, on generalising from two attackers in one simulator.
5. Should (metric-agnostic, so it holds for game theory too): a standard for comparing MTD evaluations should fix the attacker model beside the metrics. Candidate form: report the metrics against at least one attacker model that other evaluations also use. Distinct from ¶1's should, which is within one evaluation (does a learned strategy generalise); this one is across evaluations (comparability).

**Out.** S2, S3 (to §6.3/§6.5, already said), S4-S5 (Appendix E, §6.5), S6-S7 (§6.1; or Marc keeps one clause), the section-of-its-own close and its list.

**Open for Marc.**
- (a) Jalowski's four metric guidelines (§5; source l.209-219) name no attacker model, though the same passage says ASP "can only describe effectiveness against one, often very specific, attack". This would give slot 5 a direct target. It is not in ch3, so citing it in ch6 brings new literature into the discussion; the option is to cite it there or leave it out.
- (b) Keep the ASP floor as one clause in slot 3, or leave it to Appendix E and §6.5. Recommendation: leave it.
- (c) The opener's list goes stale again (item 2 becomes the shared attacker model); fix it with the opener rewrite.


## §78 — §6.4 ¶2a v6 drafted from §77's spine, proposed, not applied (Marc 2026-10-13: "give it a try do this redrafting")

Draft in the session scratchpad (p2a_v6.tex), quoted in the chat return. 150 words (was ~265), seven sentences, one hedge ("likely"). Order: claim, then what §3.2.2 said (Jalowski, Hong), then the metric switch and the attacker switch, the one concrete case (service diversity 92 % vs 36 %), so what, should. Open calls: (a) Jalowski's guidelines left out (no new literature in ch6); (b) ASP's few runs left to Appendix E and §6.5.

**Checks (numbers_reported.json, ranking.by_interval, 10 options).** The within-attacker Spearman between ASP reduction and NCR reduction (computed, unprinted) is 0.94-0.99 for the APT attacker model at every interval. For the baseline attacker it is 0.94, 0.98 and 0.92 at 50-200 s, then 0.50, 0.48 and 0.29 at 500-2,000 s. So "the choice of metric does not change the ranking" holds at 200 s only, and the claim is scoped to 200 s; Appendix E's printed sentence is also scoped to 200 s. Between-attacker ρ at 200 s is 0.006 [−0.19, 0.05] (spearman_ncr_reduction; §5.3.2 prints 0.01). Service diversity NCR reduction at 200 s: baseline attacker 0.918, APT attacker model 0.364. ρ covers ten options (seven MTD mechanisms and three deployment strategies), so S1 names both.


## §79 — §6.4 ¶2a v6: what the cuts lose (Marc 2026-10-13: "can you rest assured that cutting these ideas is OK?"; "the redraft is OK")

Each idea cut from ¶2a, checked against the tex for a home:
- What ASP and NCR count: §4.5 (subsec:metrics-outcome).
- No attack action for actions on objectives: §6.1 (l.~8575-8583) and §6.3 (l.~8894-8899, "find and compromise hosts, with no actions on objectives").
- The run ends at the first target host compromised: §6.5 (l.~9141, with the 656-of-1,000 consequence).
- The APT attacker model scores weaker on ASP and NCR: §6.1's close (l.~8648, "rate it the weaker attacker for behaving more like an APT").
- ASP's few runs, so rank on NCR reduction: Appendix E and §6.5 (l.~9292, 42 to 139 of 1,000).
- **Not placed:** "ASP is the dominant effectiveness metric" is stated only in ch3. Ch6 gives ASP's few runs as a method choice, never as an implication for evaluations. Offer: three words in §6.5's sentence at l.~9292, "ASP, the dominant effectiveness metric (Section 3.2.2)". A clause in ¶2a would cut against its claim (ASP reduction ranks as NCR reduction does, with ties at the ceiling).

¶2a/¶2b pairing: Cho's two families, effectiveness (the attacker model changes the ranking) and efficiency (it changes how often MTD must deploy). v6 no longer says "effectiveness"; ¶2b says "efficiency metrics" only in its should.


## §80 — §6.5 dominant-metric pointer applied; §6.4 ¶2a v7 clarity pass, proposed (Marc 2026-10-13: "push forward to 6.5"; "this is on effectiveness"; "a final clarity pass")

**§6.5 applied.** "... with no MTD (§6.1), too few to rank on ASP, the dominant effectiveness metric (Section 3.2.2). The ranking uses NCR reduction, with ASP reduction as the check." ("therefore" dropped: the sentence before already has one.) Build clean, 118 pages, 0 undefined.

**¶2a v7 (scratchpad p2a_v7.tex, 150 words), changes from v6:**
- S1: "On metrics" becomes "On effectiveness metrics" (the signpost, mirroring Cho's classification in §3.2.2 and Table 3.1). "The choice of metric" becomes "ranking on ASP reduction instead of NCR reduction" (two metrics were tested, so name them). The Appendix E pointer moves up from S3, so S3 no longer repeats S1.
- S3: now leads with its subject, "the rank correlation ρ" (ch4's term), and ends on what ρ means. The ASP clause is cut (now in S1).
- S5: "would therefore likely not make ... comparable" becomes "likely still cannot be compared", which is ch3's own phrase. That removes the modal, connective, hedge and negation stack. "Whose attacker models differ" scopes the claim and sets up the should.
- S6: "should also" becomes "should therefore" (the connective moved from S5). "Also" now marks the shared attacker model ("that other evaluations also use").

**¶2b signpost (proposed, not applied).** S1 claim first: "On efficiency metrics, the attacker model decides how often MTD must deploy for a given NCR reduction, although in MTDSim a deployment costs no overhead or loss of service (Section threats)."


## §81 — §6.4 ¶2a v8 sentence pass, proposed (Marc 2026-10-13: "do we need ... at 200 seconds?"; S1 "compress[es] two [claims] into one"; "do not agree" reads rhetorical, say uncorrelated; "clear for the reader")

Scratchpad p2a_v8.tex, about 150 words.
- S1 is split. The claim holds at every deployment interval (ρ between −0.24 and 0.25, §5.3.2), so "at 200 s" leaves it; "at every deployment interval" mirrors ¶1's S1. The metric switch becomes its own sentence (S5).
- "200 s" is stated once, as the frame for the numbers (ρ = 0.01, 92 % vs 36 %, ASP order), in ¶1's words ("the default deployment interval of 200 s"). The ASP agreement needs it: for the baseline attacker the ASP-NCR Spearman falls to 0.50, 0.48 and 0.29 at 500-2,000 s (§78).
- "so their rankings do not agree" becomes "the two attackers' rankings on NCR reduction are uncorrelated (ρ = 0.01; §5.3.2)": the subject leads, and ρ moves into the parenthesis.
- The 92/36 sentence gets "for example" to tie it to the ρ sentence.
- S5 "Ranking on ASP reduction instead gives the same order against either attacker": subject first; "instead" refers back to NCR reduction in S3. It sits right before the so-what it supports.
- S6 subject first ("A shared set of metrics is likely not enough"), with no fronted "With ... alone"; one hedge. S7 keeps the only "therefore".


## §82 — §6.4 ¶2a v8 applied; ¶2b efficiency signpost applied (Marc 2026-10-13: "very clear ... I'm happy with it")

One change from v8. Marc: "beside its own" is a pointer to nowhere. The close now reads "report its metrics against its own attacker model and against one that other evaluations also use". ¶2b opener: "On efficiency metrics, the attacker model decides how often MTD must deploy for a given NCR reduction, although in MTDSim a deployment costs no overhead or loss of service (Section threats)." This is a downstream ch6 edit mirroring ¶2a's signpost; it was proposed in §80 and Marc raised no objection. The stale ¶2 and ¶2a comment blocks are replaced by one current comment. Build clean, 118 pages, 0 undefined.

Next: §6.4 opener (placeholder). Its list is stale: item 2 should now be the shared attacker model (¶2a), and the longest deployment interval per attacker model (¶2b) is missing. Then ¶3 scrutiny.


## §83 — §6.4 ¶2b (efficiency): structure scrutiny, no drafting (Marc 2026-10-13: "fundamentally ... a bit flawed ... we don't do any of that ... what is the one-liner, and the structure?")

**Verdict.** The topic stands: §3.2.2 gives Cho's efficiency half, and §6.4 must answer it. The paragraph as written does not hold up.
1. **The evidence cannot carry a cost claim.** It compares different layers across the attackers (host layer vs the APT attacker model, service layer vs the baseline attacker). Each layer has its own cost per deployment, so "deploy less often" does not mean "costs less". The comparison is also §5.3.2's sentence restated.
2. **The should prescribes a method we never ran** (Marc). "The longest deployment interval that reaches a stated NCR reduction, such as half" asks others to apply a threshold that ch5 uses only as an illustration in one sentence, and the threshold level is arbitrary. It also edges into ch7 F11 (price each deployment so a sweep can choose an interval).
3. **S4 restates S1.** "On a real network each deployment costs ... so the attacker model likely changes what MTD costs" is S1 again, by way of §6.5's bound.

**The stronger evidence: the same mechanism against both attackers**, read at intervals that were run (Table eff-interval-values, so nothing is interpolated):
- host layer mean: about half against the baseline attacker at 200 s (0.49) and against the APT attacker model at 1,000 s (0.52);
- service diversity: about half against the APT attacker model at 100 s (0.50, also 0.50 at 50 s) and against the baseline attacker at 1,000 s (0.54).

A mechanism's overhead and loss of service per deployment are properties of the mechanism, not of the attacker. So for the same mechanism, how often it must deploy for the same NCR reduction stands in for what that reduction costs. This needs one assumption and no cost model. The shift runs both ways: the host layer needs fewer deployments against the APT attacker model, and service diversity needs more. So neither attacker model gives the conservative cost. No ratios are stated, because they depend on the tested intervals. "About half" is a reference level for comparing like with like, not a recommended threshold.

**One-liner.** *For the same MTD mechanism, the attacker model changes how often it must deploy for the same NCR reduction, in either direction, so an efficiency metric measured against one attacker model likely misstates the cost against another.*

**Spine (slots, no text; ~110 words).**
1. Claim: on efficiency metrics, the attacker model changes how often the same MTD mechanism must deploy for the same NCR reduction.
2. Context: efficiency metrics measure the cost of MTD (§3.2.2, Cho); MTDSim measures none (§6.5, pointer only).
3. Evidence: the host layer and service diversity at about half, at the intervals above (Table eff-interval-values).
4. Inference, one hedge: cost per deployment is the mechanism's, so the attacker model likely changes what the same NCR reduction costs, and in opposite directions for the two layers.
5. Should: an evaluation that measures efficiency should measure it against more than one attacker model, because no one attacker model gives the conservative cost. This is distinct from ¶2a (comparability across evaluations) and from F11 (pricing deployments).

**Cut.** The longest-interval recommendation; the cross-layer comparison (§5.3.2 has it); S4's restatement.

**Open for Marc.** (a) Keep slot 5, or end on slot 4 and let ¶2a's should ("report its metrics against ...") cover efficiency too. Recommendation: keep slot 5; "more than one" follows from "both directions", which is ¶2b's own evidence. (b) Use the host-layer mean, or a single mechanism for both cases (IP shuffle: 0.68 vs baseline at 200 s, 0.58 vs the APT attacker model at 1,000 s, which does not sit at half). Recommendation: the layer mean for the host layer, as Figure 5.3 plots it.


## §84 — §6.4 ¶2b: what to present (Marc 2026-10-13: "the one-liner is too confused ... efficiency metrics are not the silver lining ... they will still be implicit to the attacker model ... we can only hypothesise")

**Marc's argument, restated.** Efficiency metrics (defence cost, system performance overhead, quality of service; Table 3.1) let an evaluation weigh the cost of moving against the risk of not moving. That weighing takes its effectiveness side from the attacker model, so efficiency metrics do not escape the attacker model; they inherit it. MTDSim measures none, so this is a hypothesis (one hedge). Service diversity looks efficient against the baseline attacker and would likely not be against the APT attacker model.

**One-liner (replaces §83's).** *An efficiency metric weighs the cost of MTD against its effectiveness, so it inherits the attacker model through the effectiveness.*

**Terms check (Table 3.1).** Defender-side efficiency: defence cost and system performance overhead; quality of service. Risk is listed as a defender-side *effectiveness* metric (Alavizadeh, Ho). So "the risk of not moving against the cost of moving" pairs an effectiveness metric with an efficiency metric. That pairing is the mechanism: the effectiveness side carries the attacker model.

**What it presents.** A hypothesis, with ¶2a as its premise. Effectiveness depends on the attacker model (¶2a, measured). Efficiency is cost weighed against effectiveness, so it likely does too (inferred, one hedge). The same-mechanism rows (§83) show how: cost per deployment belongs to the mechanism, and the deployments a given NCR reduction needs belong to the attacker model. Service diversity continues ¶2a's example: about half at 1,000 s against the baseline attacker and at 100 s against the APT attacker model. The host layer runs the other way (200 s vs 1,000 s).

**Spine A (standalone ¶2b, ~100 words, no new should).**
1. Claim, hedged: on efficiency metrics, which MTDSim does not measure (§6.5 pointer), the attacker model likely matters as it does for effectiveness, because an efficiency metric weighs the cost of MTD against its effectiveness.
2. Ch3's terms: defence cost, system performance overhead, quality of service (Table 3.1). These are paid per deployment.
3. Evidence: the deployments a given NCR reduction needs depend on the attacker model. Service diversity reaches about half at 1,000 s vs the baseline attacker and at 100 s vs the APT attacker model; the host layer is the reverse (Table eff-interval-values).
4. So what: adding efficiency metrics would not free an evaluation from its attacker model. Service diversity, efficient against the baseline attacker, would likely not be against the APT attacker model. ¶2a's should covers it ("its metrics").

**Spine B (fold into ¶2a).** Slots 1 and 3 as two sentences before ¶2a's should, which then reads "its effectiveness and efficiency metrics". ¶2a's opener would go back to "On metrics". Saves about 50 words. The cost is that it undoes the Cho split and the paragraph just applied.

**Recommendation.** A. It keeps Cho's split visible, and its so-what (efficiency metrics are no way out of the attacker model) is its own point, not a second should. Dropped from §83: slot 5's "more than one attacker model" should, which repeated ¶2a.


## §85 — §6.4 ¶2b v3 drafted from spine A, proposed, not applied (Marc 2026-10-13: "a hypothesis ... risk of not moving is the mechanism ... no should, because we don't have any leg to stand on")

Scratchpad p2b_v3.tex, about 120 words, six sentences, one hedge ("likely", S1). The claim leads with Marc's point: adding efficiency metrics (the other half of Cho's classification) would not free an evaluation from its attacker model. S2 uses Table 3.1's terms (system performance overhead, quality of service) and states the weighing (Marc's mechanism). S3 is the route: cost grows with how often MTD deploys, and the deployments needed depend on the attacker model. S4-S5 give the evidence at tested intervals. S6 is the so-what, with no should.

**Precision note.** An efficiency metric itself (overhead per deployment) does not depend on the attacker. What depends on the attacker is the choice it informs, through the deployments a given NCR reduction needs. S2-S3 say this, so S1 claims dependence for the evaluation, not for the metric.

**Checks (numbers_reported.json, service diversity NCR reduction).** APT attacker model: 0.502 [0.49, 0.51] at 50 s, 0.503 at 100 s, 0.364 at 200 s; never above about half, hence "only at 100 s or shorter". Baseline attacker: 0.536 [0.52, 0.55] at 1,000 s. Host layer mean (printed): baseline 0.49 at 200 s, APT 0.52 at 1,000 s.


## §86 — §6.4 ¶2b v4 clarity pass, proposed (Marc 2026-10-13: "very well thought through ... I'm happy with it"; four refinements)

Scratchpad p2b_v4.tex.
- S2: "Efficiency metrics measure the cost of MTD" restated ch3's definition. Now "An evaluation weighs the cost of MTD, such as system performance overhead and quality of service (Table 3.1), against the effectiveness of MTD": the terms are used, not redefined.
- S3: "For a given MTD mechanism, the cost grows with how often it deploys" (Marc: cost also depends on the mechanism and how it is modelled). This also sets up the same-mechanism evidence.
- S4-S5 reframed so that deploying less often reads as the good outcome (Marc: the numbers read as "bigger is bad"). "Reduces NCR by about half when it deploys every 1,000 s against the baseline attacker, but only when it deploys every 100 s or more often against the APT attacker model"; the host layer is parallel (200 s, 1,000 s).
- S6: "worth its cost" (rhetorically inflated) becomes "can therefore be efficient against one attacker model and not against another".


## §87 — §6.4 ¶2b v5, proposed (Marc 2026-10-13: "very, very close"; "two examples, is that needed?"; specific terms)

Scratchpad p2b_v5.tex. S2 becomes "An MTD evaluation weighs" (specific term). S4 gets "for example". The host-layer sentence is cut. It showed the shift runs both ways, which mattered for §83's "more than one attacker model" should. That should is gone, and ¶2a already shows the two attackers' rankings are uncorrelated (and §6.2 the layer reversal), so the reader will not take "the APT attacker model is harder" from one example. S6 holds on service diversity alone. About 25 words saved. Echo: ¶2a also has "Service diversity, for example,"; it is the same example carried on, so the echo is left in.


## §88 — §6.4 ¶2b v5 applied (Marc 2026-10-13: "I'm happy with that ... put that in")

Text as in §87. The stale ¶2b comment is replaced by one current comment. Build clean, 117 pages (was 118), 0 undefined.

Next: the §6.4 opener (placeholder). Its list is stale: ¶2a now asks for its own attacker model and a shared one; ¶2b has no should. Then ¶3 (evaluation methods) scrutiny.

## §89 — §6.4 ¶3 (evaluation methods) thread and scrutiny, proposed, no draft (Marc 2026-10-13: "what is the one liner that threads this together ... scrutiny only")

**One-liner (recommended).** "On evaluation methods, MTDSim's rules for MTD deployments follow the baseline attacker's procedure, whichever attacker model runs." This is the only claim ¶3's own evidence shows that no other paragraph makes. It continues §6.4's thread: each part of MTDSim's evaluation was built around the baseline attacker (¶1 the deployment strategy's training attacker, ¶2 the metrics, ¶3 the simulator's rules). It also answers ch3 §3.2.3 directly. Ch3 credits simulation with modelling attack behaviour flexibly; the results show where that flexibility stops.
Rejected: (B) "simulation lets an evaluation change the attacker model and hold everything else" is what was done, not an implication, and §6.5 already says it ("Both attackers share the attack actions, the networks, the MTD mechanisms and the seeds..."). (C) "results transfer only as far as the simulator's rules" is external validity, which belongs to §6.5.

**Spine (five slots, the ¶1/¶2a pattern).**
1. The claim, in MTDSim.
2. Ch3: simulation is dominant because it models specific attack behaviours flexibly (Cho); this dissertation used that to run the APT attacker model through MTDSim's attack actions.
3. Shown: user shuffle raises the APT attacker model's NCR at every deployment interval because MTDSim's rule redraws every host's accounts but leaves valid the ones the attacker holds (App fa-accounts).
4. Stakes: the host layer's rank against the APT attacker model rests on the same kind of rule (each deployment sends the attacker back to an attack action of the baseline attacker; Figure 2.x, §6.5). Pointer only; the bound stays in §6.5.
5. Hedge plus should: a simulator's rules likely follow the attacker it was built with. An MTD evaluation that runs a new attacker model in a simulator should report the simulator's rule for each MTD deployment beside its results, so that an effect of the rule can be told from an effect of the MTD mechanism (App fa-accounts draws exactly this line).

**Current ¶3, sentence by sentence.**
- S1 "simulation lets an evaluation change the attacker model and hold everything else": opens on the method's strength, not the finding; restates §6.5; "an evaluation" should be "an MTD evaluation". Cut, or keep as a clause in slot 2.
- S2, ch3 pointer: accurate to ch3 l.2571. Keep.
- S3 "same networks, MTD mechanisms and seeds ... comes from the attackers": §6.5 almost word for word. Cut and point.
- S4 "The simulator's rules, though, were written for its own attacker": the real claim, buried fourth and arriving as a U-turn ("though"); "its own attacker" should name the baseline attacker. Promote it to S1.
- S5 "rules for what each MTD deployment takes": "takes" is vague. Ch2's Figure 2.x caption has the specific term, "the attack action each kind of deployment sends the attacker back to".
- S6 user shuffle "because of the rule MTDSim gives it": vague (the appendix states the rule), and joined to S5 by "and", so two claims sit in one sentence.
- S7 should: "interface" is defined nowhere in ch1–5 (an invented term); "both sides" is vague. The list of four declared parts (tactic-to-action mapping, tactic durations, failure matrix, vulnerability memory) has no evidence in this paragraph. Ch4 already reports them, and §6.3 finds the failure matrix and vulnerability memory move NCR negligibly. Narrow the should to the deployment rules. The sentence also stacks clauses (colon, list, "and the rules").

**Cut, and where each idea lives.** Controlled comparison: §6.5. The four declared parts: ch4 sec:execution, and §6.3 for their effect. Transfer to real networks: §6.5. The attacker that analytical models import: ch3 §3.2.1, untested here.

**Dependencies.** (a) The §6.4 opener's list: ¶3's item becomes "report the simulator's rule for each MTD deployment". (b) Gated ch7: Contribution 1's Impact points to §6.4 for "the interface: tactic-to-action mapping, tactic durations, failure handling", which goes stale if the list is cut; propose a repoint. (c) App fa-accounts points to §6.4 for "follows from MTDSim's rule", so ¶3 must keep user shuffle, or that pointer needs a new home.

## §90 — §6.4 ¶3 thread revised, proposed, no draft (Marc 2026-10-13: "the thread hasn't really sold me yet because it's a bit vague ... the attack actions are the drivers ... you can only do six things ... further back on the timeline")

**Why §89 was vague.** "MTDSim's rules for MTD deployments" names nothing a reader can picture. It could mean MTDShield, the random deployment strategy, the deployment intervals or the network, but all of those are inputs the evaluation chose, and none of them assumes an attacker. What §89 meant is narrower: where each deployment sends the attacker back to (Figure 2.x's dashed arrows). That is itself defined over the attack actions. So the attack actions are the thread, and the deployment rule is one of them.

**One-liner (revised).** "On evaluation methods, a simulator's attack actions limit how far a new attacker model can differ from the simulator's own attacker." Ch3 credits simulation with modelling specific attack behaviours flexibly (Cho) and closes on "This dissertation uses MTDSim's flexibility to run an APT attacker model through its existing attack actions". ¶3 says what that bought.

**Distinct from ¶1.** ¶1 is the MTD modelling approach: the deployment strategy carries an attacker (MTDShield learned the baseline attacker). ¶3 is the evaluation method: the simulator carries an attacker (its six attack actions, their order and where each deployment sends the attacker back to). ¶1 is about the defence; ¶3 is about the test bench. Nothing needs to come out of ¶1.

**Evidence (all printed).**
- (a) Timing: with the baseline attacker's times in place of its tactic durations, the APT attacker model closes about two thirds of its gap in ASP (§6.1, App run-time). Its outcomes differ mostly in when, not in what.
- (b) Order: 15 to 30 % of the attack profiles' attack actions fail on preconditions, because the six attack actions encode the baseline attacker's order (§6.1; §6.5 "the six encode one order").
- (c) Deployment rule: the host layer's lead against the APT attacker model turns on where MTDSim sends each attacker after a host-layer deployment (§6.2).
- (d) Cap: 8 of 15 tactics mapped; no actions on objectives (§6.3).

**Spine.** S1 the claim. S2 ch3 (Cho's flexibility; the dissertation's use of it). S3 in MTDSim, the APT attacker model differs from the baseline attacker in the order and timing of the same six attack actions: (a) and (b). S4 against MTD, its results turn on the simulator's rule for each deployment: (c), as a pointer to §6.2. S5 one hedge on the general claim. S6 the should, or none.

**Should, two options.** (i) "An MTD evaluation that runs a new attacker model in a simulator should therefore report which of its tactics the simulator's attack actions cannot run." The leg: the seven unmapped tactics, including actions on objectives, are why ASP and NCR rate the APT attacker model weaker (§6.1 close). (ii) No should, ¶2b style: the so-what is that changing the attacker model in a simulator changes the order and timing of its attack actions, and an attacker that differs in what it can do needs new attack actions. Lean: (i), because it is actionable and has a leg.

**Knock-on.** If user shuffle leaves ¶3, App fa-accounts' pointer ("follows from MTDSim's rule ... Section evaluation-implications") needs a new home (§6.5 or §6.2). Ch7 Contribution 1's "interface" pointer still needs repointing (gated).

## §91 — §6.4 ¶3 v1 drafted from §90's spine, proposed, not applied (Marc 2026-10-13: "that one liner is spot on ... the common ground, it is the only ground ... beautiful structure ... I think this is good")

Marc's "blessing and a curse" line is §6.3's close ("comparable with the baseline attacker, and limited to what MTDSim's attack actions do"). S3 points to it in plain terms, with no idiom. About 190 words, nine sentences, one hedge (S8 "likely").

```
On evaluation methods, a simulator's attack actions limit how far a new
attacker model can differ from the simulator's own attacker.
Section~\ref{subsec:evaluation-methods} found simulation the dominant evaluation
method because it models specific attack behaviours flexibly \citep{cho2020}.
The APT attacker model runs through MTDSim's six attack actions, which makes it
comparable with the baseline attacker and limits it to what those attack
actions do: find and compromise hosts (Section~\ref{sec:fidelity-verdict}). The
two attackers therefore differ in the order and timing of the same attack
actions. With the baseline attacker's times in place of its tactic durations,
the APT attacker model closes about two thirds of its gap in ASP
(Appendix~\ref{app:fa-run-time}). The attack actions' preconditions follow the
baseline attacker's procedure, so 15 to 30\,\% of the APT attacker model's
attack actions fail because the order of its tactics runs them too early
(Section~\ref{sec:disc-behaviour}). Against MTD, the host layer's rank against
the APT attacker model rests on where MTDSim sends each attacker after a
host-layer deployment (Section~\ref{sec:disc-mtd-performance}). An attacker
model that differs in what it can do, such as one that exfiltrates data, would
likely need new attack actions. An MTD evaluation that runs a new attacker model
in a simulator should therefore report which of its tactics the simulator's
attack actions cannot run.
```

**Correction to §90.** §90 gave should (i)'s support as "the unmapped tactics are why ASP and NCR rate it weaker". That is wrong: §6.1's close puts the lower ASP and NCR down to tactic durations and order. Should (i)'s support is S3's limit instead: find and compromise hosts only, with no actions on objectives (§6.3).

**Checks.** "About two thirds": App run-time, 0.63 [0.61, 0.65] of the ASP gap (§6.1 prints "about two thirds"). 15 to 30 %: App run-time and §6.1. "Rests on where MTDSim sends each attacker": §6.5's wording; mechanism in §6.2. User shuffle is out of ¶3, so App fa-accounts' pointer needs a new home.

**Open for Marc.** (1) S8 (hedge) and S9 (should) are two endings; one could go. (2) Length: about 190 words against the old ¶3's 140 and ¶2a's 150.

## §92 — §6.4 ¶3 v1: does it engage ch3 §3.2.3 or only borrow its label? (Marc 2026-10-13: "a comparator but also a limiter ... we cannot take it to the real world")

**What ¶3 v1 engages.** Ch3 §3.2.3 P1 opens "An MTD evaluation method runs MTD against an attacker model"; ¶3 S1 says what that attacker model runs through in a simulator. P2's "simulation is dominant because it models specific attack behaviours more flexibly" is ¶3 S2, and ¶3 S3–S7 answer it: that flexibility stops at the attack actions. P2's last sentence (the APT attacker model "through its existing attack actions") is S3's comparator-and-limiter.

**What it misses.** P2's middle sentence: "Simulation results do not transfer directly to a real network". That is ch3's (Cho's) cost of simulation, and Marc's "cannot take it to the real world". Without it, ¶3 answers half of ch3's trade-off. With it, ¶3 adds a second cost to the one ch3 names: Cho's sits between the simulator and a real network, and ¶3's sits inside the simulator, where a new attacker model keeps the simulator's own attacker.

**Proposed S2 edit (only).** "Section 3.2.3 found that simulation, the dominant evaluation method, models specific attack behaviours flexibly but does not transfer directly to a real network \citep{cho2020}." The transfer bound itself stays in §6.5. Here it is only ch3's claim being answered.

**Not added.** Emulation and real testbeds (ch3 P1) would run real attack tools rather than a simulator's attack actions, but nothing was run on either, so there is no leg. Analytical models: the same.

## §93 — §6.4 ¶3 v2 clarity pass, proposed, not applied (Marc 2026-10-13: "strong ... but the language ... specific terms ... already said somewhere else ... so many examples ... more concisely ... language we settled on")

About 150 words (v1: about 190), six sentences, no hedge.

```
On evaluation methods, a simulator's attack actions limit how far a new
attacker model can differ from the attacker the simulator was built with.
Section~\ref{subsec:evaluation-methods} found that simulation, the dominant
evaluation method, models specific attack behaviours flexibly but that its
results do not transfer directly to a real network \citep{cho2020}. The APT
attacker model shares the baseline attacker's six attack actions, so it is
comparable with the baseline attacker and limited to what those attack actions
do: find and compromise hosts, with no actions on objectives
(Section~\ref{sec:fidelity-verdict}). The two attackers therefore differ mostly
in the APT attacker model's tactic durations and the order of its tactics
(Section~\ref{sec:disc-behaviour}). With MTD, the host layer's rank against the
APT attacker model rests on MTDSim's rule for a host-layer deployment, written
for the baseline attacker's procedure (Section~\ref{sec:disc-mtd-performance}).
An MTD evaluation that runs a new attacker model in a simulator should therefore
report which of its tactics the simulator's attack actions cannot run.
```

| v1 | v2 | Why |
|---|---|---|
| S1 "the simulator's own attacker" | "the attacker the simulator was built with" | Ch2's definition of the baseline attacker, word for word; "own" pointed nowhere, like "beside its own" (§82). |
| S2 the flexibility clause only | adds "but that its results do not transfer directly to a real network" | §92: answers both halves of ch3's claim. |
| S3 "runs through ... which makes it" | "shares the baseline attacker's six attack actions, so it is comparable ... and limited to ... with no actions on objectives" | §6.3's settled wording; "which" had no clear antecedent; Marc asked for "no actions on objectives". |
| S4 "order and timing of the same attack actions" | "mostly in the APT attacker model's tactic durations and the order of its tactics" | The ch6 opener's terms, word for word; "timing" was a second term for tactic durations. "Mostly", as the opener says, because §6.3 also names the declared parts. |
| S5 two thirds of the ASP gap | cut | §6.1 and App run-time; S4 points there. Evidence for the difference, not for the limit. |
| S6 15-30 % fail on preconditions | cut | §6.1 and App run-time. Second example (Marc: "so many examples"). |
| S7 host layer "rests on where MTDSim sends each attacker" | "rests on MTDSim's rule for a host-layer deployment, written for the baseline attacker's procedure" | §6.5's wording; names which rule, and ties the rule back to S1's limit. The one example kept, because it is the one that reaches an MTD result. "Against MTD, ... against" becomes "With MTD". |
| S8 hedge, "would likely need new attack actions" | cut | Two endings (§91). S1 is structural (an attacker model in a simulator can run only the simulator's attack actions), not inferred, so it needs no hedge. |
| S9 should | unchanged | Its support is S3's limit (§91 correction). |

## §94 — §6.4 ¶3 v3, proposed, not applied (Marc 2026-10-13: "very, very good"; host-layer sentence unclear, "rests on the assumption ... the baseline attacker was going all in all the time"; "you only need the one example"; the should "is specific but not generalisable"; "allow for comparison, but also a limiting factor ... nuanced, balanced")

S1-S4 as v2. About 170 words.

```
On evaluation methods, a simulator's attack actions limit how far a new
attacker model can differ from the attacker the simulator was built with.
Section~\ref{subsec:evaluation-methods} found that simulation, the dominant
evaluation method, models specific attack behaviours flexibly but that its
results do not transfer directly to a real network \citep{cho2020}. The APT
attacker model shares the baseline attacker's six attack actions, so it is
comparable with the baseline attacker and limited to what those attack actions
do: find and compromise hosts, with no actions on objectives
(Section~\ref{sec:fidelity-verdict}). The two attackers therefore differ mostly
in the APT attacker model's tactic durations and the order of its tactics
(Section~\ref{sec:disc-behaviour}). With MTD, a service-layer deployment
disrupts an attacker only while it runs an attack action, which the baseline
attacker does back to back (Section~\ref{sec:disc-mtd-performance}). The APT
attacker model's tactic durations keep it in unmapped tactics, which run none,
so attack actions blocked per MTD deployment is 0.15 for it, against 0.95 for
the baseline attacker. An MTD evaluation should therefore report the attack
actions its evaluation method gives the attacker, since the same attack actions
that let two attacker models be compared also limit how far they can differ.
```

| v2 | v3 | Why |
|---|---|---|
| Host layer "rests on MTDSim's rule for a host-layer deployment, written for the baseline attacker's procedure" | Service layer: "disrupts an attacker only while it runs an attack action, which the baseline attacker does back to back", then 0.15 against 0.95 attack actions blocked per MTD deployment | "Rule" left the reader to guess the assumption. The service layer states it in one clause (Marc's "going all in all the time"), with §6.2's wording. It ties directly to S3's limit: the unmapped tactics run no attack action, so a service-layer deployment cannot disrupt them. One example only. The host-layer rule stays in §6.2 and §6.5. |
| Should "a new attacker model in a simulator ... which of its tactics the simulator's attack actions cannot run" | "An MTD evaluation should therefore report the attack actions its evaluation method gives the attacker, since the same attack actions that let two attacker models be compared also limit how far they can differ" | Generalises across ch3's four evaluation methods (an analytical model, emulation and real testbed also give the attacker a set of actions), and to evaluations without a new attacker model or tactics. Comparison and limit are stated as a balanced pair. |

Checks: 0.15 and 0.95 printed in §6.2 (Figure aio-adaptivity(a)); "back to back" and "keep it ... in unmapped tactics that run none" are §6.2's wording; the metric name is ch4 l.1569's.
Note: the should's balance echoes S3 (comparable and limited). The repeat is deliberate (Marc: balanced). If it reads as a repeat, the short form is "report the attack actions its evaluation method gives the attacker".

## §95 — §6.4 ¶3 example settled first, should held (Marc 2026-10-13: "you don't need to say [unmapped tactics which run none] ... attack actions blocked is much lower and as a result the service layer deployments are less effective ... the assumptions of the model emerge this result ... I just want to settle the example")

Example only (S5-S7); S1-S4 as v2/v3; the should is next.

```
With MTD, a service-layer deployment disrupts an attacker only while it runs an
attack action, which the baseline attacker does back to back
(Section~\ref{sec:disc-mtd-performance}). Attack actions blocked per MTD
deployment is 0.15 for the APT attacker model, against 0.95 for the baseline
attacker. This difference likely explains why the service layer reduces the APT
attacker model's NCR less than the host layer does, at every deployment interval.
```

- S5: unchanged from v3. It states the assumption (disruption only while an attack action runs) and who it suits.
- S6: "The APT attacker model's tactic durations keep it in unmapped tactics, which run none" is cut (Marc). The number stays as the measured difference.
- S7 is new: the result the assumption produces (Marc's "emerge"). It uses §6.2's printed claim ("the service layer reduces its NCR less than the host layer does", at every deployment interval, the sq:evaluate answer) and §6.2's hedge ("likely explain"). One hedge in ¶3. "This difference" names its referent; it is not a bare "this".
- Checked and rejected: "less than the baseline attacker's" does not hold at every interval. Port shuffle at 1,000 s is 0.050 vs 0.041, and OS diversity at 1,000 s is -0.012 vs -0.004, both near zero (numbers_reported ranking.by_interval).

## §96 — §6.4 ¶3 example moves to §6.2; ¶3 points to it (Marc 2026-10-13: "isn't this something that we already present in 6.2 ... why do we present it here instead of in 6.2"; "your example is actually cleaner than currently in 6.2")

**Diagnosis.** §95's S5-S7 restate §6.2 ¶3 (service layer) almost word for word: the same assumption, the same 0.15 against 0.95, the same result. That is a rehash in ¶3. What made §95 cleaner: "back to back" is attached to the assumption it suits, and there is no "but" U-turn.

**Proposed §6.2 ¶3 edit (upstream, proposed only).** Two flagged sentences; the claim-first opener and the numbers are kept.

```
The APT attacker model's tactic durations likely explain why the service layer
reduces its NCR less than the host layer does. A service-layer deployment
disrupts an attacker only while it scans ports, exploits or brute-forces
(Section~\ref{subsec:attacker-model}), which the baseline attacker does back to
back. The APT attacker model's tactic durations keep it between attack actions,
in unmapped tactics that run none (Section~\ref{subsec:aio-disruption}). Under
every service-layer mechanism, attack actions blocked per MTD deployment is
therefore 0.15 for the APT attacker model, against 0.95 for the baseline
attacker (Figure~\ref{fig:aio-adaptivity}(a)).
```

- S2: "which the baseline attacker does back to back" moves onto the assumption.
- S3: the U-turn "The baseline attacker runs its attack actions back to back, but ..." becomes a plain sentence on the APT attacker model. The unmapped-tactics clause stays here: in §6.2 it is the mechanism (Marc cut it from ¶3 only).
- S4: "therefore" ties the number to S2-S3.

**¶3 S5-S7 become one pointer (proposed).**

```
With MTD, these two differences likely decide which MTD layer reduces each
attacker's NCR most (Section~\ref{sec:disc-mtd-performance}).
```

"These two differences" names S4's tactic durations and order of its tactics. This is §6.2's own opener claim, with its hedge ("likely explain"). It shows the limit reaching an MTD result without re-explaining it. The should is next.

**Not taken from Marc's musing (answered in chat).** (a) "Service-layer disruption scales with attack rate": the attack rate ratio is 0.68-1.23 vs 1.71 per minute (about 0.4-0.7), but the blocked ratio is 0.15/0.95 (about 0.16), so the two are not proportional. Time in unmapped tactics, not attack rate, carries it. (b) The host layer: §6.2 puts it on the order of its tactics (no host until Lateral Movement runs enumerate host), not on the APT attacker model being slower.

## §97 — §6.4 ¶3 v4 in full, plus a ch6 duplication map (Marc 2026-10-13: "Yep, that's good" on §96; "what does the full thing look like ... some duplication with chapter 6 sections ... how to consolidate")

About 130 words, six sentences, one hedge (S5).

```
On evaluation methods, a simulator's attack actions limit how far a new
attacker model can differ from the attacker the simulator was built with.
Section~\ref{subsec:evaluation-methods} found that simulation, the dominant
evaluation method, models specific attack behaviours flexibly but that its
results do not transfer directly to a real network \citep{cho2020}. The APT
attacker model shares the baseline attacker's six attack actions, so it is
comparable with the baseline attacker and limited to what those attack actions
do: find and compromise hosts, with no actions on objectives
(Section~\ref{sec:fidelity-verdict}). The two attackers therefore differ mostly
in the APT attacker model's tactic durations and the order of its tactics
(Section~\ref{sec:disc-behaviour}). With MTD, these two differences likely
decide which MTD layer reduces each attacker's NCR most
(Section~\ref{sec:disc-mtd-performance}). An MTD evaluation should therefore
report the attack actions its evaluation method gives the attacker.
```

**Duplication map.**

| ¶3 | Also in | Verdict |
|---|---|---|
| S1 claim | none | ¶3's own |
| S2 ch3 | none in ch6 | ¶3's own (answers ch3) |
| S3 comparable and limited, with no actions on objectives | §6.3 close, word for word; §6.5 design choice 1 ("act through the same attack actions"; "Seven tactics have no attack action to run") and its "Both attackers share the attack actions ... comes from the attackers" | premise, pointed |
| S4 tactic durations and order | ch6 opener; §6.1 opener and close | premise, pointed |
| S5 decides the MTD layer | §6.2 opener | premise, pointed |
| S6 should | none | ¶3's own |

**Reading.** S3-S5 are a chain of premises that each owning section needs for its own question: §6.1 explains, §6.2 answers SQ2, §6.3 answers SQ3, and §6.5 bounds. ¶3 states each premise once, with a pointer, and adds S1, S2 and S6. This is the ¶2a pattern (premises pointed, implication its own), so no section needs to give anything up for ¶3.

**The one real duplication is outside ¶3.** The comparator-and-limit point is made in full twice, in §6.3's close and in §6.5's design choice 1 plus its "Both attackers share ..." sentence. That is for the ch6 cut pass (word band about 3,300), not this round: §6.5 keeps the bound, and §6.3 keeps the SQ3 answer. Parked.

**Consolidated in ¶3 this round.** The should's reason clause ("since the same attack actions that let two attacker models be compared also limit how far they can differ", v3) repeated S3, so it is cut to the short should. The balance Marc asked for (comparator and limiter) now lives in S3 alone.

## §98 — §6.2 service-layer paragraph edit applied (Marc 2026-10-13: "happy with the 6.2 change as well")

Text as proposed in §96: "which the baseline attacker does back to back" moved onto the assumption, the "but" U-turn removed, and "therefore" added on the number. Build clean, 117 pages, 0 undefined. ¶3 v4 (§97) is still proposed.

## §99 — §6.4 ¶3 v5: the should is dropped, ¶3 ends on its so-what (Marc 2026-10-13: "the should doesn't land ... you're just arguing for more transparency ... a bit cliche ... we already do that ... it's not going to fix anything")

Also asked: "is there a point on host-layer disruption being emergent from slower tactic durations?" Answered in chat: no. §6.2 puts the host layer on the order of its tactics (no host until Lateral Movement) and the service layer on tactic durations. Durations plausibly also lengthen the time without a host, but no run with MTD isolates them (App run-time's baseline-times run is no-MTD only; ch7's bound says so). They stay off the page. Candidate further analysis: the host layer with the baseline attacker's times (registry, if wanted). Marc: "a bit implicit", left out.

**Why the should goes.** "Report the attack actions its evaluation method gives the attacker" asks for transparency evaluations already give and fixes nothing. The one should that would fix the limit ("add attack actions to the simulator") prescribes something not run: the ¶2b threshold case (no leg, §84-§85). So ¶3 ends like ¶2b, on a hedged so-what that says what such an evaluation actually tests. It is the general form of S4-S5, as ¶2a's "A shared set of metrics is likely not enough ..." is the general form of its evidence.

```
On evaluation methods, a simulator's attack actions limit how far a new
attacker model can differ from the attacker the simulator was built with.
Section~\ref{subsec:evaluation-methods} found that simulation, the dominant
evaluation method, models specific attack behaviours flexibly but that its
results do not transfer directly to a real network \citep{cho2020}. The APT
attacker model shares the baseline attacker's six attack actions, so it is
comparable with the baseline attacker and limited to what those attack actions
do: find and compromise hosts, with no actions on objectives
(Section~\ref{sec:fidelity-verdict}). The two attackers therefore differ mostly
in the APT attacker model's tactic durations and the order of its tactics
(Section~\ref{sec:disc-behaviour}). With MTD, these two differences likely
decide which MTD layer reduces each attacker's NCR most
(Section~\ref{sec:disc-mtd-performance}). An MTD evaluation that changes only
the attacker model therefore likely tests MTD against a new order and timing of
the same attack actions.
```

About 135 words, two hedges on two inferred claims (S5 cause, S6 generalisation). Rejected alternative ending: "An attacker model that differs in what it can do, such as one with actions on objectives, would likely need new attack actions" (v1 S8). It points the way forward rather than saying what an MTD evaluation shows, and it edges toward the unrun prescription.

## §100 — §6.4 ¶3 v5 final ending, ready to apply (Marc 2026-10-13: "this is MTDSim context specific ... how do you generalise that to a full audience"; then "that's correct ... no punch, but it doesn't have to be a punch anymore ... this is very specific ... you're basically constrained to this")

The ending names the reader it reaches: someone who runs a new attacker model in an existing simulator, as MTDSim's own extensions did (Zhang, Ho, Tay). S1 is general by construction. S3-S5 are MTDSim's evidence, scoped by naming the two attackers. "Likely" covers the step from one simulator to others.

```
On evaluation methods, a simulator's attack actions limit how far a new
attacker model can differ from the attacker the simulator was built with.
Section~\ref{subsec:evaluation-methods} found that simulation, the dominant
evaluation method, models specific attack behaviours flexibly but that its
results do not transfer directly to a real network \citep{cho2020}. The APT
attacker model shares the baseline attacker's six attack actions, so it is
comparable with the baseline attacker and limited to what those attack actions
do: find and compromise hosts, with no actions on objectives
(Section~\ref{sec:fidelity-verdict}). The two attackers therefore differ mostly
in the APT attacker model's tactic durations and the order of its tactics
(Section~\ref{sec:disc-behaviour}). With MTD, these two differences likely
decide which MTD layer reduces each attacker's NCR most
(Section~\ref{sec:disc-mtd-performance}). An MTD evaluation that runs a new
attacker model in an existing simulator therefore likely tests MTD against a new
order and timing of that simulator's attack actions.
```

Not taken: Marc's "the only two things you can change are the order and the timing" as "likely changes only ...". "Only" would contradict S4's "mostly" (the tactic-to-action mapping and the failure matrix also differ; §6.3). The specific ending carries the weight: S1 says the limit, and S6 says what is left inside it.

## §101 — §6.4 ¶3 v6 ending, proposed (Marc 2026-10-13: "it almost reads like a fact ... you spend a year and you figure out you can only change the order and the timing. Oh you suck")

v5's ending stated only what is left inside the limit, so it read as a confession. The result is the other half: the APT attacker model changes little more than order and timing, and that still likely decides which MTD layer reduces each attacker's NCR most (S5). v6 ends on that, so "only two things" becomes "two things were enough". This is the comparator-and-limiter balance (Marc, §94), now aimed at the field rather than at the author.

```
On evaluation methods, a simulator's attack actions limit how far a new
attacker model can differ from the attacker the simulator was built with.
Section~\ref{subsec:evaluation-methods} found that simulation, the dominant
evaluation method, models specific attack behaviours flexibly but that its
results do not transfer directly to a real network \citep{cho2020}. The APT
attacker model shares the baseline attacker's six attack actions, so it is
comparable with the baseline attacker and limited to what those attack actions
do: find and compromise hosts, with no actions on objectives
(Section~\ref{sec:fidelity-verdict}). The two attackers therefore differ mostly
in the APT attacker model's tactic durations and the order of its tactics
(Section~\ref{sec:disc-behaviour}). With MTD, these two differences likely
decide which MTD layer reduces each attacker's NCR most
(Section~\ref{sec:disc-mtd-performance}). A new attacker model in an existing
simulator can therefore likely change which MTD layer reduces NCR most, even when
it changes little more than the order and timing of the simulator's attack
actions.
```

- "Little more than" agrees with S4's "mostly"; "only" would not (§100).
- One hedge ("likely") for the step from one simulator to others; S5 keeps its own "likely" on the cause.
- "Which MTD layer reduces NCR most" is the SQ2 answer's wording (§6.2) and the result an MTD evaluation reports.
- The implicit so-what is that varying the attacker model is worth doing even inside one simulator. It is not stated as a should: ¶1 and ¶2a already carry the shoulds to test against more than one attacker model.

## §102 — Where the three findings live; the "within the limit" framing parked for ch7 (Marc 2026-10-13: "I really liked that ... is that my contribution or an introduction point")

Marc likes v6's ending. The three findings named in chat (the MTD layer flips with the attacker; MTDShield reduces the APT attacker model's NCR less than random does; rankings on NCR reduction uncorrelated) are Contribution 2 (SQ2), already claimed in the abstract (most effective MTD mechanism differs at every interval; 92 vs 36 %), ch1's second contribution bullet, and ch7 Contribution 2 (claim; MTDShield under Impact). The correlation is in §5.3.2 and §6.4 ¶2a. Not new contributions, and not intro points beyond ch1's bullet.

**New, and parked for the ch7 pass (gated, propose first).** The framing that strengthens Contribution 2: the two attackers share MTDSim's attack actions, networks, MTD mechanisms and seeds, yet the most effective MTD layer differs. Candidate for ch7 Contribution 2's Claim or Not claimed: "even though the two attackers share MTDSim's attack actions". Frankness bound: that they share the attack actions is measured design; that order and timing caused the flip is hedged ("likely"; no run separates them, ch7 Not claimed; future work F13).

## §103 — §6.4 ¶3 v7 clarity pass, proposed (Marc 2026-10-13: "happy with your drafting ... v6 is pretty good, just do a clarity check ... can therefore change how MTD is measured to perform")

Only S6 changes; S1-S5 pass.

```
On evaluation methods, a simulator's attack actions limit how far a new
attacker model can differ from the attacker the simulator was built with.
Section~\ref{subsec:evaluation-methods} found that simulation, the dominant
evaluation method, models specific attack behaviours flexibly but that its
results do not transfer directly to a real network \citep{cho2020}. The APT
attacker model shares the baseline attacker's six attack actions, so it is
comparable with the baseline attacker and limited to what those attack actions
do: find and compromise hosts, with no actions on objectives
(Section~\ref{sec:fidelity-verdict}). The two attackers therefore differ mostly
in the APT attacker model's tactic durations and the order of its tactics
(Section~\ref{sec:disc-behaviour}). With MTD, these two differences likely
decide which MTD layer reduces each attacker's NCR most
(Section~\ref{sec:disc-mtd-performance}). A new attacker model in an existing
simulator can therefore likely change how MTD is measured to perform, even when
it differs in little more than when and in what order it runs the simulator's
attack actions.
```

| v6 S6 | v7 | Why |
|---|---|---|
| "change which MTD layer reduces NCR most" | "change how MTD is measured to perform" | Marc. "Perform" is the RQ's and SQ2's word ("How does MTD perform against ..."), so the term is not vague. "Measured" keeps it to the evaluation's result, not MTD itself (ch3's point). It also reaches evaluations that do not use NCR or MTD layers. |
| "can change ... even when it changes little more than" | "even when it differs in little more than" | "Change ... changes" echoed; "differs" echoes S1's "differ from", so the paragraph closes on its claim. |
| "the order and timing of the simulator's attack actions" | "when and in what order it runs the simulator's attack actions" | "Timing" was a second term beside S4's "tactic durations" (§93). A general attacker model may have no tactic durations, so the plain words replace both terms. |

Checked, unchanged: S2's appositive (one clause, ch3's own pair); S3 "baseline attacker" twice (repetition beats "it", which would be ambiguous); "therefore" in S4 and S6 (not adjacent; each marks a step that follows); one hedge per inferred claim (S5 cause, S6 generalisation).

## §104 — §6.4 ¶3 v7 applied (Marc 2026-10-13: "it's uplifting ... it took honesty and maturity to land a sentence like that ... I'm actually happy with this chapter. So you can push it in")

Text as §103. The old ¶3 (the controlled comparison, the "rules" thread, user shuffle, the interface list) is replaced, and one current comment goes above it.

**Downstream, applied automatically.** App fa-accounts' "follows from MTDSim's rule for user shuffle ... (Section evaluation-implications)" now points to sec:threats, where §6.5's second design choice is MTDSim's rules for what each deployment takes.

**Other pointers to §6.4, checked.** §6.5's two pointers (a ranking carries its attacker model's assumptions; rankings never a verdict) rest on ¶2a and still hold. The ch6 opener's pointer is generic.

Build clean, 117 pages, 0 undefined.

**Still open in §6.4.** (1) The opener placeholder: its three-should list is stale (¶1 and ¶2a end on a should; ¶2b and ¶3 do not); re-frame on the thread that each part of MTDSim's evaluation was built around the baseline attacker. This is the paragraph's own text, so propose first. (2) Gated ch7: Contribution 1's Impact, "Another simulator needs the interface: ... (Section evaluation-implications)", is stale ("interface" is gone from §6.4); Contribution 2's "within the limit" framing (§102); its Impact list (the lowest-NCR-reduction lower bound is not in §6.4).

## §105 — Endings review, §6.4 (and §6.1-§6.3 closes): honesty, teeth, maturity (Marc 2026-10-13: "trying to land a punchy line is losing us marks ... are we being honest ... do they read as tacky ... have a look through those in 6.4"). Review only; nothing applied.

| Ending | Verdict | Why |
|---|---|---|
| §6.4 opener (placeholder) "an MTD evaluation run against the baseline attacker alone picks the MTD layer that reduces the APT attacker model's NCR less" | Overreaches; rewrite (already pending) | It treats the APT attacker model as the yardstick. Ch7 Contribution 2's Not claimed says neither attacker model is the better one. The honest frame: run against one attacker model alone, an evaluation picks the MTD layer that suits that attacker model. Its three-should list is also stale. |
| ¶1 should (learned deployment strategy vs another attacker model, beside random) | Earns it | The leg is measured: MTDShield is below random against the APT attacker model at every interval. The mechanism is hedged ("most likely"). "Like a test on training data" is the CS reader's own concept, not a flourish. Tay is described, not judged. Optional: the trailing "which shows what the learning adds" stacks a clause. |
| ¶2a "A shared set of metrics is likely not enough ..." plus should | Earns it | It answers Jalowski with a hedge and one number (rho = 0.01). The should names no attacker model of ours ("one that other evaluations also use"), so it is not self-serving. |
| ¶2b "can therefore be efficient against one attacker model and not against another" | Right weight | A hypothesis ends on "can", with no should, because there is no leg. |
| ¶3 "can still change how MTD is measured to perform, even when it differs in little more than ..." | Strongest | It says the limit and the result together. "Likely" and "little more than" keep it to what was measured. |

**§6.1 close: the one punch with less teeth than it shows (upstream, propose).** "ASP and NCR alone therefore rate it the weaker attacker for behaving more like an APT." About two thirds of the ASP gap comes from tactic durations (App run-time), and ch4 sets nine of the 15 mean durations by "our judgement" (subsec:dwell-times). §6.3's own close says the model "rests on our judgement where MTD disrupts it". So "behaving more like an APT" credits our judgement as APT behaviour, and §6.3 contradicts it. Candidate: "ASP and NCR alone therefore rate it the weaker attacker for the same tactic durations and order that give it these properties." The irony stays; the claim drops to what §6.1 shows.

**§6.2 and §6.3 closes.** §6.2 ends on numbers, with no punch. §6.3's "grounded in threat reports for the order of its tactics, and rests on our judgement where MTD disrupts it" and "comparable ... and limited ..." are the frankest lines in ch6, and they set the bar the §6.1 close misses.

## §106 — §6.1 close fixed (Marc 2026-10-13: "'these properties' seems a bit vague ... you can fix that up")

"ASP and NCR alone therefore rate it the weaker attacker for behaving more like an APT" becomes "... for what gives it objective-specific behaviour, choice of attack strategy and detection avoidance". The three properties are named in §6.1's own order. "What gives it" points back to the two causes the previous sentence names, without repeating them. The irony is kept; the claim no longer credits the judgement-set tactic durations as APT behaviour (§105). Comment added above the paragraph. The phrase appears nowhere else (grep). Build clean, 117 pages, 0 undefined.

## §107 — §6.4 opener v1, proposed, not applied (Marc 2026-10-13: "what do we say in the opener ... frank and honest ... present our results clearly ... keeping it lean, short, sharp ... intentional")

**Job.** (1) The result that makes §6.4 necessary, scoped once ("In MTDSim"). (2) What it means in general, hedged once ("can"). (3) Why the three parts: ch3 §3.2's own frame ("the three parts of an MTD evaluation that use the attacker model"), named in ch3's words and order. About 70 words.

```
In MTDSim, at every deployment interval, the most effective MTD mechanism
differs between the two attackers (Section~\ref{subsec:eff-cross-arm}). Which
MTD mechanism an MTD evaluation finds most effective can therefore depend on its
attacker model. This section says what that means for each of the three parts of
an MTD evaluation that use the attacker model
(Section~\ref{sec:mtd-evaluation-survey}): MTD modelling approaches, metrics and
evaluation methods.
```

- S1 is the abstract's sentence (SQ2's answer), word for word, with the ch5 pointer. It presents the result plainly: we ran this, and found this.
- S2 is ch7's hedge ("can depend"). It does not name the APT attacker model as the right one, which fixes §105's overreach.
- S3 uses ch3 §3.2's frame word for word; each paragraph's "On ..." opener then does the signposting.
- No list of shoulds: ¶1 and ¶2a end on one, ¶2b and ¶3 do not, so a list would misstate two paragraphs.
- No "even with the same attack actions" (Marc's "in the face of adversity"). That is ¶3's ending, and the opener would spend it before ¶3 lands. It also goes to ch7 Contribution 2 (§102).

## §108 — §6.4 opener v1 applied; §6.4 redraft complete (Marc 2026-10-13: "yeah, that's fine. beautiful")

Text as §107. It replaces the placeholder and the stale DRAFT STATE / PLACEHOLDER comments with one current comment. Build clean, 117 pages, 0 undefined.

§6.4 is now: opener, ¶1 (MTD modelling approaches), ¶2a (effectiveness metrics), ¶2b (efficiency metrics), ¶3 (evaluation methods), each redrafted and applied this session.

**Carried forward.** Gated ch7 (propose first): Contribution 1's Impact "interface" pointer is stale; Contribution 2 gets the "shared attack actions, yet the layer differs" framing (§102), and its Impact list's lowest-NCR-reduction lower bound is not in §6.4. Also: the ch6 cut pass toward about 3,300 words (the §6.3-close vs §6.5 duplication, §97); a cold-examiner pass on §6.2; and the earlier carried items (dev push and remote branches; gated "pace" lines; "refused" in §6.5).


## §109 — §6.5 scrutiny and structure guidance, no redraft (Marc 2026-10-13: "scrutiny only, forward guidance only, no redraft yet")

**Convention (sources checked 2026-10-13).**
- Verdecchia and Bogner 2025 (arXiv 2506.11002, §3.10): one paragraph per threat category, using a categorisation that fits the study (Wohlin et al.). It covers the most important or most likely threats only. Each threat gives its mitigation, or why none was possible, plus the residual and how likely it is to affect the results, with evidence where possible (Wyrich and Apel 2024). Separate limitations, which are conscious scope decisions and may sit in the study design, from threats, which are not chosen. Length about 1 to 1.5 columns in a 10-page paper.
- ACM SIGSOFT Empirical Standards, General: disclose all major limitations; describe attempts to mitigate; discuss sensitivity of the results to assumptions. Antipatterns: "acknowledging limitations but then writing implications and conclusions as though the limitations don't exist"; applying a validity type the study has no use for.
- Verdecchia, Engström, Lago, Runeson and Song 2023 (IST 164:107329), and the ESEM 2024 follow-up: threats are mostly an afterthought and seldom discussed in depth, and categorisations are ignored. Abstracts only; full text not read.
- de França and Travassos 2015 (CLEI EJ 18(1)): 28 threats for simulation studies, by Cook and Campbell's types. This is the closest fit for MTDSim. Not read.
- In references.bib, only sargent2011 of these is present. Wohlin et al. is still missing.

**Current state.** About 1,770 words in five paragraphs (371/420/398/304/278), about 45 % of ch6. It is a collection of points: about 25 threats, unranked, at one weight each.

**Structural findings.**
1. ¶1 mixes limitations by design, a causal claim and a mitigation, and threats. By the convention, the scope limits (one token, the default network, 15 000 s, simulation only, existing MTD mechanisms) are limitations, so they get one sentence with a pointer. Several are external-validity threats and also appear in ¶4.
2. ¶1 rehashes ch6. Root 1 (shared attack actions as comparator and limit) is now §6.4 ¶3 and §6.3's close. Root 2 (no host until Lateral Movement) is §6.2 ¶2. Only root 3 (no cost of deployment, no detection) is unique to §6.5.
3. **"The reversal" contradicts ¶5.** ¶1 and ¶2 say "the reversal" three times. ¶5 says rho near zero "is weaker than one inverting the other". The settled terms are §6.2's layer claim and §6.4's "the most effective MTD mechanism differs".
4. **¶5 bounds a claim ch6 no longer makes alone.** ¶5 says the statistics support "the two attackers' rank 1, and little beyond it". §6.2's answer to SQ2 is a layer claim ("at every deployment interval the host layer reduces the APT attacker model's NCR more than the service layer does ..."), and §6.4 ¶3 leans on it. ¶5 must bound the layer claim, or the claim needs its test. OPEN: what the layer claim rests on (point values per interval on fig:eff-cross-arm, CIs, or Scott-Knott groups). This is the Empirical Standards antipattern in reverse: the bounds and the claims have drifted apart.
5. Tactic durations are split across ¶2 (six from MTDSim, nine by judgement; B19 band test) and ¶3 (declared by judgement; untested multipliers). It is one threat with one mitigation (B19), and it is the main residual on SQ2.
6. No ranking. The threat with the most leverage on the answer (cause not isolated: durations and order; the with-MTD run is not done) sits mid-¶2 at the same weight as "distinct openings counts tactics, not attack actions".
7. Several threats bound SQ1 (the yardstick, behaviour metrics by proxy, one coder), while the opener frames the section around SQ2. They are fair to keep, but they belong in their own construct block, tagged to SQ1.
8. Endings: ¶1 "Each is future work"; ¶2 "Defects ... repaired"; ¶5 a bootstrap fact with no direction or so-what. None says the residual on the answer.

**Sentence flags (lessons from §6.1–§6.4).**
- Banned: "refused" twice (¶1, ¶3).
- Figurative: "prices nothing", "earn it nothing and cost it outcome", "cut short by the attack actions' own", "gain at no cost".
- Unsourced: "On a real network, speed raises alarms".
- Vague: "MTDSim's rules for what each deployment takes" (the phrase from the §89 round); "The metrics measure their properties in part".
- Overclaim: "the different starting points cannot cause the reversal".
- Stacked opener: "bounds the answers to the three sub-questions, and how far the answer to SQ2 reaches APT attackers".
- Rehash: ¶2's "two thirds" is §6.1's sentence.
- The verification sentence is a mitigation with no threat stated.

**Forward guidance (proposed, for Marc's ruling).**
- S0 opener (about 40 words): what §6.5 bounds; limitations versus threats; cite Wohlin et al.
- S1 limitations by design (about 80 words, one paragraph): one sentence each on the one token, the default network, 15 000 s, simulation only, existing MTD mechanisms on a schedule, and no cost or detection. Each points to ch4/ch5 and §7.2.
- S2 threats, numbered T1–Tn and ranked by how far each could change the answer to SQ2. Grouped by type in the order internal, construct, conclusion, external. Each threat gets one shape: the claim at risk, the threat, the mitigation done (with pointer), the residual. The numbers let ch7 and §7.2 cite a threat ("T1").
  - Candidate rank: T1 cause not isolated (durations and order; B19; with-MTD run is future work); T2 judgement values (one threat; band test); T3 the mapping (input; total mapping 0.15 vs 8.13); T4 unequal conditions and the end of a run; T5 statistics for the layer claim and rank 1; T6 metrics by proxy and time lost; T7 the corpus; T8 no observed APT campaign against MTD (Sargent).
- Target about 1,000–1,100 words, which saves about 700 and puts ch6 near 3,300.
- Not recommended: a threat table in place of prose. It could read as a way round the word band, and as boilerplate (French's examiner feedback).


## §110 — §6.5 v1 drafted, not applied (Marc 2026-10-13: "ranked T1-Tn ... don't move anything above 6.5 yet ... check whatever you need ... first draft mechanical structure ... float vestigial points")

**Evidence checked before drafting (numbers_reported.json, ch5_defended).**
- Layer means (Figure 5.3): the 95 % CIs of host and service layer separate at all six intervals, for both attackers. They also separate on ASP reduction (sweep_asp).
- Per mechanism: against the APT attacker model, every host-layer mechanism is above every service-layer mechanism at every interval. Against the baseline attacker this holds only at 50 and 100 s. At 200 s IP shuffle = OS diversity (0.68). From 500 s IP shuffle is above port shuffle and OS diversity, so the service layer's lead is service diversity's alone.
- Scott-Knott rank 1 (sk_esd groups) shares no mechanism at any interval: all host layer (APT attacker model) against all service layer (baseline attacker). But only 200 s is PRINTED (Table 5.3; Table C.1b at 200 s only).
- B19 band test: 200 s only. Host layer above service layer at both ends (Table C.1b).
- Re-verified against floats: 42-139, 656, 0.15-0.21 vs 0.50 (Table 5.2); 0.15 vs 8.13 (App B); 24 of 60 (sec:ablation); 18 of 38; one token (sec:petri-formalism).

**Structure.** Opener (45 words); limitations, one paragraph (105); T1-T11 as an enumitem series (label T\arabic*, \label{thr:*}, as ch1's SQ list), under four run-in heads: internal T1-T4, construct T5-T8, conclusion T9, external T10-T11. Each item: the threat on a named claim, mitigation with pointer, residual. Compiled in a scratch copy: T1-T11 resolve; only wohlin2012 is undefined (not in bib); 118 pages.

**Words:** about 1,470 against about 1,770 (the target is about 1,000-1,100; cut pass owed).

**Vestigial / floated to Marc (nothing applied):**
- Cut: the "prices nothing" causal paragraph and "speed raises alarms" (unsourced); §6.4 ¶2b and the limitations sentence carry it.
- Cut: "refused" and the one-order sentence (§6.1/§6.3 carry it); "ten options, three deploy the other seven"; "near zero, small spread, large d"; random partitions "one time in eleven" (ch6 does not lean on it; it bounds §5.4).
- Corrected: "a difference ... comes from the attackers, not ..." becomes T2, where part can come from MTDSim's rules.
- Downstream (auto after ruling): App F.3 pointer to \ref{thr:rules}; ch4 l.4027 could point to \ref{thr:corpus} (ch4, propose); "refused" in App experiment-one.
- Upstream (propose): print Scott-Knott rank 1 at every interval (§6.4 opener says "at every deployment interval"; T9's "200 s only" sentence then goes); wohlin2012 bib entry; ch7 §7.2 notes say "in that section's order" (order now limitations, then T1-T11); ch7 l.9572 "one clause per root" refers to the retired two-roots spine.
- Limitations stay in §6.5: each is already declared upstream (one token sec:petri-formalism; network and run length Table 5.1; simulation only §3.2.3; nothing watches the attacker §4.4 mapping), so the paragraph names them as limits with pointers. §6.4 ¶2b and §7.2 point here.

```
\section{Threats to validity}
\label{sec:threats}

This section bounds the answers to the three sub-questions. Limitations are
scope we chose; threats to validity are risks we did not choose. The threats
are grouped by type \citep{wohlin2012} and ranked within each type by how far
each could change the answer to \ref{sq:evaluate}.

Every result is a result in MTDSim, within six limitations. The APT attacker
model runs MTDSim's six attack actions, which carry out eight of its 15
tactics and stop at compromising hosts (Section~\ref{subsec:tactic-verb-mapping}).
One token pursues one line of a campaign at a time
(Section~\ref{sec:petri-formalism}). MTDSim measures no efficiency metric, and
nothing in MTDSim watches the attacker. Each run uses MTDSim's default network
of 50 hosts and lasts at most 15\,000\,s, about four hours, against campaigns of
months (Table~\ref{tab:experiment}). The evaluation is simulation only
(Section~\ref{subsec:evaluation-methods}), with existing MTD mechanisms, each
deployed at a deployment interval (Section~\ref{subsec:defence-mechanisms}).
Each limitation is a direction of future work (Section~\ref{sec:future-work}).

\paragraph{Internal validity.}
\begin{enumerate}[label=T\arabic*, ref=T\arabic*, series=threats, align=left]
\item\label{thr:cause} Which part of the APT attacker model makes the most
effective MTD mechanism differ is not isolated. The APT attacker model differs
from the baseline attacker in its tactic durations, the order of its tactics and
its response to failure at once. Removing the failure matrix or the
vulnerability memory changes NCR negligibly where each was run, and without the
attack profiles the same three MTD mechanisms reduce NCR the most
(Section~\ref{sec:ablation}). That leaves the tactic durations and the order of
its tactics, which no run with MTD separates. The causes
Section~\ref{sec:disc-mtd-performance} gives for each MTD layer are therefore
likely, not shown. The APT attacker model with the baseline attacker's times
was run with no MTD only (Appendix~\ref{app:fa-run-time}).

\item\label{thr:rules} Part of the difference between the two attackers can
come from MTDSim's MTD mechanisms, which were written against the baseline
attacker's procedure (Section~\ref{subsec:attacker-model}). After a host-layer
deployment, the APT attacker model has no host until the order of its tactics
reaches Lateral Movement (Section~\ref{sec:disc-mtd-performance}). An APT that
holds hosts through Command and Control might keep one, so the host layer's
rank against the APT attacker model rests on MTDSim's rule. User shuffle leaves
valid the accounts the attacker holds, so each deployment gives both attackers
a fresh chance to log in (Appendix~\ref{app:fa-accounts}). Both attackers face
the same MTD mechanisms, networks and seeds, and no MTD mechanism was changed
for the APT attacker model, so the rules are shared but untested.

\item\label{thr:conditions} The two attackers do not run under identical
conditions. An attack action takes the mean duration of the tactic that runs
it, not MTDSim's time (Table~\ref{tab:attack-action-times}), and the
vulnerability memory acts on an exploit's chance of success, where the baseline
attacker's acts on its time. With no MTD, the APT attacker model's NCR is 0.15
to 0.21 against the baseline attacker's 0.50 (Table~\ref{tab:unopposed-summary}).
Each ranking compares MTD mechanisms against one attacker, over that attacker's
own NCR with no MTD, so the different starting points likely do not decide
which MTD mechanism ranks first. A run also ends at the first target host
compromised or at 15\,000\,s, so the baseline attacker's NCR stops short in 656
of its 1\,000 runs with no MTD. The layer order also holds on ASP reduction,
which does not depend on when a run ends
(Table~\ref{tab:eff-interval-values-asp}).

\item\label{thr:code} The code may not do what this dissertation says it does.
It was checked by an event tracer that replays a run step by step, an audit of
MTDSim's code against what its papers describe, unit tests of the Petri net and
the simulator, and fixed seeds that reproduce every run exactly. Defects found
in MTDSim were repaired before the evaluation, so the results are not compared
numerically with earlier MTDSim studies.
\end{enumerate}

\paragraph{Construct validity.}
\begin{enumerate}[resume*=threats]
\item\label{thr:values} CTI records no tactic durations, failure-matrix values
or factor for the vulnerability memory, so we declared them by judgement
rather than fitting them (Table~\ref{tab:value-bases}). Each was varied,
substituted or removed one at a time, which leaves their interactions untested,
and three were not tested: the per-tactic duration multipliers, the share of
weight given to the pre-intrusion overlay and the choice of one attack flow per
APT group. Only the 45\,s mean duration changes NCR much
(Table~\ref{tab:anchor-sensitivity}). At a quarter and at four times its value,
the APT attacker model's rank~1 still shares no MTD mechanism with the baseline
attacker's, and the host layer still ranks above the service layer
(Table~\ref{tab:duration-ranking}). That test ran at 200\,s only.

\item\label{thr:mapping} The tactic-to-action mapping is our input
(Section~\ref{subsec:tactic-verb-mapping}). Command and Control is the only
tactic that maps to scan neighbours, the attack action that finds new hosts, so
it sets how fast the APT attacker model spreads. A total mapping gives every
tactic an attack action, and most then fail on their preconditions: the APT
attacker model compromises 0.15 hosts with no MTD, against 8.13 under the
partial mapping (Table~\ref{tab:experiment-one}). No other partial mapping was
tested.

\item\label{thr:metrics} Three metrics measure their property only in part.
Time lost per MTD deployment compares the wait under MTD with the wait from the
same moment in the run with no MTD, and the two runs are identical only up to
the first MTD deployment. At that deployment the baseline attacker's time lost
falls below zero: sent back to scan host, it gets a second attempt at its first
host, as MTDSim intends \citep{brown2023} (Section~\ref{subsec:aio-disruption}).
Attack rate and attack confidentiality measure detection avoidance by proxy,
through how often an attacker acts and a declared IDS rule
(Appendix~\ref{app:detector-memory}). Distinct openings counts any variety, so
it shows that the APT attacker model chooses among attack strategies, not that
it chooses well. It counts an attack profile's steps as tactics and the
baseline attacker's as attack actions; recounted in attack actions, the gap
holds (Appendix~\ref{app:fa-behaviour-actions}).

\item\label{thr:yardstick} The eight properties are this dissertation's reading
of the APT definition and two surveys. They are not a complete standard, they
are weighed equally though not equally important, and one scorer marked the APT
attacker model and three MTD attacker models on them, with language models
scoring blind as the check (Appendix~\ref{app:clause-tests}). The attack
profiles rest on two yes-or-no questions asked of each attack flow, answered by
one coder from the CTID descriptions and their sources, three of them by our
own decision (Appendix~\ref{app:classification-audit}).
\end{enumerate}

\paragraph{Conclusion validity.}
\begin{enumerate}[resume*=threats]
\item\label{thr:statistics} The statistics support the layer order and the
comparison of the two attackers' rank~1, and little beyond them. Against the
APT attacker model, every host-layer mechanism reduces NCR more than every
service-layer mechanism at every deployment interval. Against the baseline
attacker, this holds up to 100\,s; from 500\,s, IP shuffle reduces NCR more
than port shuffle and OS diversity, and the service layer's lead rests on
service diversity alone (Table~\ref{tab:eff-interval-values}). The Scott--Knott
ESD test ranks the MTD mechanisms at 200\,s only (Table~\ref{tab:eff-cross-arm});
at the other deployment intervals, rank~1 is read from the values and their
confidence intervals. $\rho$ between $-0.24$ and $0.25$ means that the two
attackers' orders do not agree, which is weaker than one inverting the other.
The APT attacker model reaches a target host in only 42 to 139 of each attack
profile's 1\,000 runs with no MTD (Table~\ref{tab:unopposed-summary}), too few
to rank on ASP, the dominant effectiveness metric
(Section~\ref{subsec:mtd-metrics}), so the rankings use NCR reduction. A
negligible effect is Cohen's default of $\pm 0.2$, not a bound set for hosts
compromised. The ablations leave 24 of 60 cells inconclusive for the attack
profiles, with no correction for the number of cells compared
(Section~\ref{sec:ablation}). The confidence intervals resample runs, not
seeds, so they treat the four attack profiles' runs on one seed's network as
independent.
\end{enumerate}

\paragraph{External validity.}
\begin{enumerate}[resume*=threats]
\item\label{thr:corpus} The results reach APT attackers only as far as the 38
attack flows do. The attack flows record campaigns that were detected and
reported (Section~\ref{subsec:failure-matrix}), and each draws only the steps
its threat report describes, which can stop short of the objective
(Section~\ref{sec:attack-profiles}). Only 18 of the 38 are attributed to a
group in ATT\&CK, criminal groups among them, so the attack graph records
attackers reported in CTI, not APT attackers alone
(Section~\ref{sec:technique-graph}). We chose attack flows because CTI and
ATT\&CK rarely record the order of an attack's techniques
(Section~\ref{subsec:profiling}), at the cost of volume: three of the four
attack profiles rest on 5 to 7 attack flows (Table~\ref{tab:attack-profiles}).
The APT attacker model is therefore the behaviour a handful of reported
incidents document, not an optimal adversary. A run is a draw from an attack
profile, not a replay, and may join parts of several attack flows into a
campaign no attacker ran.

\item\label{thr:observation} No APT campaign against MTD can be observed, so
the APT attacker model cannot be checked against one. For a system that cannot
be observed, Sargent advises exploring the model's behaviour as thoroughly as
possible and comparing it with other models \citep{sargent2011}.
Appendix~\ref{app:sensitivity} and the ablations explore it, and the baseline
attacker is the other model. MTDShield also runs as released, outside its
training conditions (Appendix~\ref{app:mtdshield-limitations}), so its results
bound MTDShield as released, not MTDShield retrained against the APT attacker
model.
\end{enumerate}
```


## §111 — §6.5 opener merged; follow-through applied; completeness audit (Marc 2026-10-13: "merged opener, that's fine ... the Wohlin entry you can do ... we can fix all those downstream ... do you think this is pretty complete")

**Applied.**
- Opener merged into the limitations paragraph. "This section bounds the answers to the three sub-questions" is cut, and the wrong count ("six limitations"; the paragraph lists eight) is gone. A two-sentence threats lead-in, citing Wohlin et al. and stating the ranking rule, sits before T1.
- wohlin2012 is in references.bib (Crossref-checked).
- §7.2 notes reordered to §6.5's order; "prices nothing" and "reversal" retired; the promises list updated.
- §7.1 bound note now points to T1 and T2.
- App F.3 pointer now goes to T2.
- App B "refused" becomes "fail on their preconditions".
- Build clean, 118 pages, 0 undefined. Commits da05137b and this one.

**Completeness audit against the six cold examiners' fifteen (assembly handoff §13) and Cook and Campbell's types.**
Covered:
- 1 → T1; 2 → T5; 4 → T10 and the limitations; 5 → T7; 6 and 9 → T3; 12 → T11; 14 → T6.
- 3 and 15 are not threats.
- 10 → T9, partly: the mixtures were cut.
- 11 → T9, partly: d near the floor and the random partitions' one-in-eleven were cut.
- 13 → T5, T8 and T10, partly.

Gaps, in proposed order of weight:
- (a) **Post-hoc analyses.** Appendix F was run after the results were seen, and ch6 leans on it (§6.1's two thirds; T1). App F's opener says "none enters the main argument", yet §6.1 uses App F run-time as evidence for its causal claim. This is a conclusion-validity threat that is not stated, and the inconsistency needs a ruling.
- (b) **Values declared before any result.** This mitigation was in the old ¶2 and was dropped in v1. Restore it in T5. Marc's 13a #9 supports it; ch4 does not state it.
- (c) **Time lost.** It is measured at 2,000 s only, where the next deployment caps the wait (examiners 4/6). One clause in T7.
- (d) **Random partitions, p ≥ 1/11** (examiners 3/6). Restore one clause in T9, or leave it out: ch6 does not lean on it.
- (e) **Comparators.** The three MTD attacker models were chosen by us, and there is no game-theoretic attacker (examiners 2/6). One clause in T8.
- Not added: "c4 a residual bin" and "corpus weights never varied". No text supports either.


## §112 — Rank 1 at every interval printed (Marc 2026-10-13: "5.3.2 yeah you can do that ... the appendix entry, I don't care")

- tools/ch5_sweep_figures.py gains `--only rankone`, which emits tables/tab_F-0c_rank_one.tex (tab:rank-one-intervals): Table 5.3's Scott-Knott rank 1 at each of the six intervals. Checked: the rank field equals sk_esd group 0 everywhere. Rank 1 shares nothing at any interval: 50-200 s, three host-layer shuffles against service diversity + port shuffle; 500-2,000 s, IP shuffle against service diversity.
- Appendix E (app:sup-mtd-effect): one lead-in sentence and the table, after Table E.x.
- §5.3.2 (ch5, approved): "At every deployment interval, rank 1 against the APT attacker model holds only host-layer mechanisms, and rank 1 against the baseline attacker only service-layer mechanisms (Table~\ref{tab:rank-one-intervals})."
- ch6 (auto): §6.4 opener points to the table; T9's "Scott-Knott at 200 s only" sentence is cut.
- Build 118 pages, 0 undefined; no new overfull box.


## §113 — §6.5: the five gaps added (Marc 2026-10-13: "yes you can add all of them")

- **Gap 1, post-hoc analyses.** New item thr:posthoc (now T10, conclusion validity). Appendix F was chosen after ch5's results were seen; ch6 uses it, most of all fa-run-time; each analysis answers a ch5 float's question and changes no ch5 result, but explores rather than tests. External threats renumber to T11-T12 (labels by name; nothing breaks).
- **App F opener (appendix, auto).** Two false claims fixed. "None enters the main argument" (§6.1 and T1 use fa-run-time) becomes "none changes a result of Chapter 5, and Section 6.5 bounds their use (T10)". "Each reads runs already recorded, so none needed a new run" now adds "except fa-run-time, which runs the APT attacker model again with no MTD".
- **Gap 2.** T5: "declared them by judgement before any result, rather than fitting them".
- **Gap 3.** T7: time lost AND attack actions blocked are measured at 2,000 s only (Table 5.x caption; the cap), so §6.2 explains the service layer at every interval from measures at one. This is new on checking: §6.2's 0.15 vs 0.95 is from the 2,000 s figure.
- **Gap 4.** T9: beating all ten random partitions is what chance alone gives one time in eleven, so the comparison describes rather than tests.
- **Gap 5.** T8: the three MTD attacker models are our choice (subsec:recent-threat-models), and none is the attacker of a game-theoretic model, the dominant MTD modelling approach (cho2020).
- §6.5 is now about 1,590 words. Build 118 pages, 0 undefined.


## §114 — §6.5 v1 structure scrutiny, no redraft (Marc 2026-10-13: "why do we have two paragraphs ... what does the reader expect ... what is the one-liner ... what can live in the hedging ... criticise, don't redraft")

**Why two openers.** ¶1 (limitations) is a body block dressed as an opener; ¶2 (threats lead-in) is the real opener. ¶1's first sentence repeats the ch6 opener ("Every claim is about MTDSim"). Each limitation is declared upstream, and two are §6.3 ¶3 nearly verbatim (eight of 15 tactics, stops at compromising hosts; no IDS).

**What the reader expects (Verdecchia and Bogner; Empirical Standards).** (1) Up front: which claims are bounded and what survives. (2) The scheme. (3) The threats that could change an answer, first and frankly. (4) Each with mitigation and residual, specific to this study. (5) Residuals that ch7 can carry. v1 gives (2) and part of (3)-(4). It has no (1), and several items end without a residual (T2 "shared but untested", T4, T9, T12).

**One-liner (proposed).** The layer claim is measured, and it holds under every check run (ASP reduction, the band test, separated CIs). What stays open is why it holds (T1, T2, T5) and how far it reaches APT attackers (T11, T12).

**Sort (keep here / elsewhere / cut).**
- Limitations ¶: one sentence in the opener, with a pointer to §7.2. The rest is upstream.
- T1 cause: keep, top. The ablation recap shortens to a clause.
- T2 MTDSim's rules: keep. The Lateral Movement recap is §6.2; keep the pointer. User shuffle becomes a pointer (App F.3 needs the label).
- T3 conditions: dissolve. "Not identical conditions" is the treatment itself, not a threat. Different starting points becomes a clause in conclusion. End of run (656) with the ASP mitigation moves to construct (NCR truncated).
- T4 code: keep, last in internal; the verification home (show-verification memory).
- T5 values: keep, top construct; trim the untested list.
- T6 mapping: keep, short.
- T7 metrics: split. Time lost (first deployment; 2,000 s) bounds §6.2. Distinct openings bounds §6.1. The proxy sentence is §6.3 ¶3: cut.
- T8 yardstick: keep the yardstick and comparators. One coder for the attack profiles moves next to the corpus.
- T9 statistics: split. (a) The layer claim: per-mechanism scope for the baseline attacker, bootstrap over runs, NCR because ASP is thin. (b) Ablations and partitions: Cohen, 24 of 60, one in eleven. The rho sentence is vestigial (it was written to retire "reversal"; §6.4 ¶2a already says uncorrelated): cut.
- T10 post-hoc: keep, short.
- T11 corpus: the 18 of 38 and the reason for attack flows are ch4 l.4018-4027 verbatim; "incidents that succeeded" is §6.3 ¶2. Keep: detected and reported, few flows per profile, not an optimal adversary, a run joins flows.
- T12: Sargent, keep. MTDShield as released becomes its own short residual on §6.4 ¶1.

**Shape.** Each item opens on the claim at risk (subject first), then threat, mitigation and residual. The ranking rule says "the answers" (or tags the SQ), since construct threats bound SQ1/SQ2 and §6.1, not SQ3.

**Sentence flags.** Not-X-but-Y / "rather than" run through it: "rather than fitting", "likely, not shown", "describes rather than tests", "explores rather than testing", "not an optimal adversary", "not a replay", "not MTDShield retrained". T1's first sentence buries its subject. "Three metrics measure their property only in part" and "the rules are shared but untested" are vague.

**Size.** The sort removes about 450-500 words, so about 1,100. Nothing applied.


## §115 — §6.5 opener: the §114 one-liner withdrawn (Marc 2026-10-13: "reads like a riddle ... what is the point of the opener to threats to validity ... why this structure ... do we need to say what the biggest threats are")

**Why the one-liner failed.** It put a verdict into a section that, by convention, is a catalogue. It also compressed twelve items into labels the reader has not met yet ("the layer claim", "every check", "why it holds"). Pulling the residuals together is ch7's job (the §7.1 bound note), not the opener's.

**The opener's job.** Orient the reader: what is bounded, the difference between limitations and threats, and what the four types ask, said as plain questions for a reader who does not know the terms. It gives no verdict, and it does not list the biggest threats: the ranking shows them, so naming them would repeat T1, T5 and T11.

**Why Wohlin's four types.** Examiners recognise them, and they force coverage (the §111 audit ran against them). Each type is one question about an answer:
- internal: is the cause the one we claim?
- construct: do the metrics and values measure what we say?
- conclusion: do the statistics support the claim?
- external: does it reach APT attackers beyond MTDSim and the 38 attack flows?

**Slots (no prose; one paragraph, about 70-90 words).**
- S1: the section sets out the threats to the answers of §6.1-§6.4, the risks we did not choose.
- S2: the limitations are the scope we chose, named in one sentence (one token, the default network, 15 000 s, simulation only, existing MTD mechanisms, no efficiency metric, no IDS), each a direction of §7.2.
- S3: the four types as the four questions, citing Wohlin et al.
- S4: the ranking rule. Within each type, by how far the threat could change an answer, so the first item of each type is its largest.
