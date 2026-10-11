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
