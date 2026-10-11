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
