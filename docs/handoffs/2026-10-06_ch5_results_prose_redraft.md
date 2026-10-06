---
status: open — awaiting Marc's ruling on §1 (the spine), §2 (floats and layout) and §3 (what moves); no tex edited
created: 2026-10-06
supersedes: Part C and Part D of 2026-09-25_ch5_setup_defence_and_prose_slots.md (the slot plan the current agent drafts were written to). Its Parts A, B, E and G stay as the record of §5.1.
---

# Chapter 5 results prose (§5.2–§5.4): rebuilt from the findings, without numbers first

**Goal.** §5.2–§5.4 read as a short walk through the floats, each paragraph
opening on the one finding its float carries. The headline findings found
chapter 6. The draft has no numbers until Marc approves it. Then the numbers go
in, read from the 1 000-seed floats.

**Marc's brief (2026-10-06).** The current text is "vague, not specific, no
narrative, and is stale as I updated the figures"; "quite a lot of it
detracting from the clarity". The fix he wants:
- a tight conventional structure, kept to;
- the headline points first, shown against the figures, for his comment
  before any redraft;
- after drafting, plain language: no sentence over three clauses, and the
  subject leading every sentence;
- after drafting, every noun checked against what chapters 2–4 give the reader;
- the floats refitted at the macro level, so the layout is clean and
  conventional;
- purpose, context, audience, clarity, relevance and specificity throughout.

Approved method: "no fluff, no duplication, no repetition"; "you write without
the numbers first, once I approve, we will add the numbers"; "let me know what
you are planning to move".

---

## 0. What went wrong (the diagnosis Marc accepted, 2026-10-06)

1. **The text copies the floats instead of reading them.** §5.2–§5.4 run to
   about 3 270 words. Most sentences restate a number the float beside them
   prints. The 2026-09-26 ruling asks for "the numbers that carry the
   observation". The draft gave all of the numbers, because no observation was
   chosen first.
2. **The headline is buried.** The answer to SQ3 is that the two attackers rank
   MTD differently. It sits in the last paragraph of §5.3.2. MTDShield's choice
   of service diversity is a subordinate clause.
3. **Method and discussion leak in.** Examples are the dispatch-failure reason,
   the deployment-mix reweighting check, and each ablation re-stating its own
   design. §3 below lists every case.
4. **The numbers are stale because the prose types them in.** 65 `\prelim`
   values still date from the 100-seed run. Sentences such as "over the 5 to 13
   runs in 100" and ρ = −0.03 are wrong at 1 000 seeds (ρ is 0.006 there).

**How the draft got here.** The 2026-09-25 agent drafts were argument-shaped.
Marc called them "rhetorically inflated" on 2026-09-26. The rewrite then turned
his spoken walk through the floats into a catalogue. This rebuild keeps the
plain description and the "Figure X shows" opener, and adds the step both
drafts skipped: **one chosen finding per paragraph.**

---

## 1. The spine — the findings, how each sits in its float, and what it founds

**The chapter's answer to SQ3, in one sentence:** which MTD works best depends
on the attacker it is evaluated against. Marc's own words:
- 2026-09-30: "on NCR the best value depends on the attacker … that's basically
  the headline";
- 2026-09-26: "the fidelity of your model will determine … the outcomes of your
  rankings".

**Sources for each finding.**
- The ratified takeaways: T1–T4 (2026-09-20), R1–R3 (2026-09-24), H1–H4 and
  D1–D4 (2026-09-25), and the 2026-10-02 audit's B3 and B8. The retired brief
  holds them:
  `git show 7435c315^:docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md`,
  §8a, §8g-5, §8j-2 and §8j-3.
- Takeaways 1–11, ratified in session 5470d00b (2026-09-30, at 100 seeds),
  which supersede R1–R3 for Figure 5.2.
- The ablation rulings of 2026-09-26 to 2026-10-03.

Each finding below was **re-read against the 1 000-seed float as built
today**. Where the float moved the takeaway, the change is said.

**Headline** marks the findings chapter 6 stands on. Every other finding
supports one of them.

### §5.2 APT attacker model versus baseline attacker → chapter 6 §6.1

| # | Finding (no numbers) | Where the reader sees it | Founds | Was |
|---|---|---|---|---|
| A1 | Part of the APT attacker model's steps fall on unmapped tactics, which dispatch no attack action. The baseline attacker's steps fall only on its six attack actions. | Fig. 5.1(a): the unmapped block of rows, filled for $c_1$–$c_4$ and empty for the baseline attacker's column | §6.1(1), the mechanism of "less, more slowly" | T1 |
| A2 | The four attack profiles divide their steps among the tactics differently. Impact is the contrast that needs no legend hunt. | Fig. 5.1(a): the impact row read across | §6.1(3); property 2 | T2 |
| A3 | The APT attacker model's runs part ways within a few steps; the baseline attacker's runs open alike. Of the four profiles, $c_3$ has the fewest openings. | Fig. 5.1(b): four rising lines against a flat grey line | §6.1(3); property 3 | T3. At 1 000 seeds the order is $c_1$ > $c_2$ > $c_4$ > $c_3$. The metric is now a count out of 1 000 runs, and "nearly one per run" no longer holds. The current text's counts "of 100" are stale. **Marc, 2026-09-30:** "I don't know why you're separating C3 … it's just so sparse." Option: drop the $c_3$ clause and let the line speak (Q13). |
| **A4 Headline** | With no MTD, the APT attacker model takes a target host in far fewer runs and compromises less of the network than the baseline attacker. | Table 5.2: the ASP and NCR columns, with the baseline attacker's row under the four profiles | §6.1(1); **the reference for every effect in §5.3** | T4. "Later" is dropped: at 1 000 seeds $c_3$'s MTTC interval overlaps the baseline attacker's. |
| A5 | The APT attacker model also has the lower attack rate and the higher attack confidentiality. The two are one observation, since the detector counts attack actions. | Table 5.2: the last two columns | §6.1(2); property 5 stays blank | S2-c1 (2026-09-25) |

### §5.3.1 Response to disruption → chapter 6 §6.2(2)

| # | Finding | Where the reader sees it | Founds | Was |
|---|---|---|---|---|
| B1 | A deployment's layer decides how often it blocks an attack action. Nearly every deployment blocks one of the baseline attacker's. Far fewer block one of the APT attacker model's: about a third under the host layer, a sixth under the service layer. | Fig. 5.2(a): grey bars at the ceiling, black bars low and equal within a layer | §6.2(2) | B3 (2026-10-02) |
| **B2 Headline** | The MTD mechanism that costs one attacker time costs the other none. The host layer costs the APT attacker model time. Service diversity costs the baseline attacker time. Against the baseline attacker, the other mechanisms cost no time, and several shorten its wait for the next compromise. | Fig. 5.2(b): black bars on the left, one tall grey bar on the right, the grey bars elsewhere at or below zero | §6.2(1)–(2); the mechanism behind C1 | Takeaway 6 (2026-09-30), which replaces R3 on the 2026-09-30 metric. **Falsified at 1 000 seeds:** R3's "the baseline attacker's other mechanisms include zero". IP shuffle, port shuffle, OS diversity and user shuffle are below zero (Table 5.3). |
| B3 (headline candidate) | A blocked attack action need not cost time. Every host-layer deployment blocks one of the baseline attacker's attack actions, and none costs it time. | Fig. 5.2(a) against (b), read down one column | §6.2(2), "simply needs to reconnect" | The session proposed it on 2026-10-02 as one of three discussion findings ("interruption is not disruption"). **Marc moved on without ruling.** Today it sits in Figure 5.2's caption, where a finding does not belong. |

### §5.3.2 Effect of the attacker model → chapter 6 §6.2(1), (3), (4) and its close

| # | Finding | Where the reader sees it | Founds | Was |
|---|---|---|---|---|
| **C1 Headline** | The two attackers order the MTD layers in reverse. Against the APT attacker model the host layer reduces NCR most. Against the baseline attacker the service layer does. | Fig. 5.3(a) and (b): the black line above the grey in (a), the grey above the black in (b) | §6.2(1), the layer reversal | H1 |
| C2 | Every reduction falls as the deployment interval grows, except user shuffle's against the APT attacker model. | Fig. 5.3(a)–(f), read left to right | the interval as a defender's setting | H2 |
| C3 | The deployment strategies follow their mechanisms. Random and alternative, which draw on all seven, reduce the APT attacker model's NCR more. MTDShield, which chooses service diversity at most decisions, reduces the baseline attacker's more. | Fig. 5.3(d)–(f); Appendix D.5 for MTDShield's choices | §6.2(4), MTDShield trained against the baseline attacker | H3, reframed as a consequence of C1 |
| C4 | The exception, marked and not explained: user shuffle is at or below zero against the APT attacker model, so the model compromises more hosts than with no MTD. | Fig. 5.3(c) | §6.2(3) | H4 |
| **C5 Headline** | No MTD mechanism or deployment strategy ranks first against both attackers. The two rankings are unrelated: Spearman's ρ is near zero. | Table 5.4: the two rank columns (the host layer rank 1 on the left, service diversity and port shuffle rank 1 on the right) | §6.2 close; §6.4, implications for MTD evaluation | R1 recast. At 1 000 seeds ρ at 200 s is 0.006 [−0.19, 0.05], and it lies between −0.24 and +0.25 at every interval (`numbers_reported.json` `ranking.by_interval`). See ruling Q5. |
| ~~C6~~ | **Not a finding.** ASP reduction is drawn in Fig. 5.3(g)–(l), but its takeaway was never ratified. Marc, 2026-09-30: "don't really understand that … the ASP … is complete bonkers", and "the ASP is just ridiculous" when he reversed the 2026-09-29 ASP headline. | Fig. 5.3(g)–(l) | nothing in chapter 6 | Takeaway 8, unratified; B8 (2026-10-02). Hence L2: the rows go to the appendix, and the text gives them at most one pointer. |

### §5.3.3 MTD mechanisms and deployment strategies → chapter 6 §6.2 (depth) and property 2

| # | Finding | Where the reader sees it | Founds | Was |
|---|---|---|---|---|
| D1 | A layer's line hides mechanisms that agree for one attacker and not the other. Against the APT attacker model the three host-layer mechanisms act alike up to 200 s. Against the baseline attacker IP shuffle does more than either topology shuffle. | Fig. 5.4(a)–(c): the profile lines bunched, the grey line separate | §6.2(1), depth | D1 |
| D2 | Service diversity is the only MTD mechanism that keeps a reduction against the baseline attacker at every interval. | Fig. 5.4(f), the grey line | §6.2(1) | D3 |
| D3 | The four attack profiles follow one line per mechanism. The exception, marked: $c_3$ keeps a larger host-layer reduction from 500 s. | Fig. 5.4(a)–(c), the $c_3$ line | property 2; §6.1(3) | D2 |
| D4 | Against every attack profile, MTDShield does less than against the baseline attacker, and random and alternative do more. | Fig. 5.4(h)–(j): the grey line above every profile in (i), below in (h) and (j) | §6.2(4) | Takeaway 11 (2026-09-30), amended at 1 000 seeds: MTDShield's gap is separated up to 1 000 s (it was 500 s), and random and alternative stay ahead at every interval. Marc's reading, "it's because it's overfitting to the baseline", is §6.2(4)'s, not chapter 5's. |

### §5.4 Ablation studies → chapter 6 §6.3 (properties 2, 4, 7)

| # | Finding | Where the reader sees it | Founds | Was |
|---|---|---|---|---|
| **E1 Headline** | Of the three judgement calls, only the partition into attack profiles changes a result. | Table 5.5: bold rows in the first block only | §6.3: the model's additions operate, and only the partition changes the outcome | Marc's §6.3 placeholders |
| E2 | Without the partition the attacker has more distinct openings and compromises more, by a small-to-medium effect. Its NCR reduction under the host layer changes. | Table 5.5, first block; Table E.5 at every combination | property 2 | the 2026-10-02 ablation design. **Two counts are in circulation for the combinations beyond the threshold:** 48 of 61 by the point $d$ (the session record), and 30 of 61 by the interval (the text; Table E.5 says 29 of 60 without no MTD). §5.4's decision rule is the interval, so the numbers phase uses the interval count only. |
| E3 | Random partitions of the same group sizes compromise less than either, and give the same change in NCR reduction. Sorting by objective accounts for the extra compromise; group size accounts for the change in NCR reduction. | **No float today.** These numbers live only in the prose (Q6). | property 2, bounded | as E2 |
| E4 | Removing the failure matrix changes where the attacker goes after a failure, not what it achieves. Where there is any difference, it runs opposite to the prediction. | Table 5.5, second block: no bold | §6.3, adaptivity told frankly | the 2026-09-26 ablation |
| E5 | The vulnerability memory raises the share of exploits that succeed, not NCR. This holds even with one service per operating system, where its effect on exploits is largest. | Table 5.5, third block; Fig. E.1 and Table E.6 | §6.3, property 7 | the 2026-09-30 §5.4.2 design |

**Marc's call:** amend any wording, promote or demote any finding, or strike
one. The slots in §4 are built on this table, and nothing is drafted until it
is ratified.

---

## 2. The floats — fresh read against the findings, and the macro layout

Every chapter 5 float was rendered from today's build (`pdflatex` ×2 +
`bibtex`, 0 errors) and read against the findings it carries.

| Float | Carries | Verdict | Proposal |
|---|---|---|---|
| Table 5.1 | the setup | holds | Add the random-partition control to the Ablation row (it is run and reported, but not declared). |
| Figure 5.1 | A1–A3 | holds; each finding is visible without the text | none |
| Table 5.2 | A4–A5 | holds | none |
| Figure 5.2 | B1–B3 | holds. B3 is legible as (a) against (b). | Move the caption's finding ("a mechanism can block every attack action in (a) and still not delay the next compromise in (b)") into the text as B3. The caption keeps the decode. |
| **Table 5.3** | B1–B2 again | **It prints the same values as Figure 5.2**, and its caption repeats Figure 5.2's nearly word for word. With the text, each number appears three times. | **L1:** move it to Appendix E beside Tables E.1–E.4, which already hold the values behind Figures 5.3 and 5.4. §5.3.1 then has one float, and its caption points to the appendix table. |
| **Figure 5.3** | C1–C4, C6 | Twelve panels on a full page. **The caption runs into the page number** (printed p. 38). Rows (g)–(l) draw ASP reduction, which saturates against the APT attacker model (B8), while the ranking is on NCR. | **L2:** keep rows (a)–(f), NCR, as the headline: a half-page, 2 × 3 figure. Move rows (g)–(l) to Appendix E as a figure of their own, with C6 as one sentence. This fixes the overflow, and Figure 5.3 and Table 5.4 can share a page. |
| **Table 5.4** | C5 | Holds the ranks. ρ, the headline number, is in no float. Five of the ten APT MTTC cells are dashes, and MTTC carries no finding. | **L3:** add a foot row giving Spearman's ρ with its interval. Drop the two MTTC columns, which Tables E.3–E.4 already hold. Print the no-MTD NCR and ASP in the no-MTD row and cut that sentence from the caption. |
| Figure 5.4 | D1–D4 | holds; the depth reads cleanly | none |
| **Table 5.5** | E1, E2, E4, E5 | Holds. The random-partition control (E3) has no float. | **L4:** add a column (or a block) with the random partitions' mean NCR and range, so E3 can be stated without numbers in the prose. |
| Table E.5 | depth for E2 | holds. Its caption counts 29 of 60 combinations; §5.4.1 counts 30 of 61, because it includes no MTD. | Use one count, read off the table. |
| **Fig. E.1, Table E.6, and Table 5.5's memory block** | E5 | **They print 100-seed data under captions that say 1 000 seeds.** `memory_ablation_numbers.json` (2026-10-01) reads 100 seeds per pool. `runs_memory.jsonl` has held all 1 000 seeds since 2026-10-02 16:40, and the reader was never re-run. | **L5 (blocking for the numbers phase):** re-run `memory_ablation.py`, then `ablation_table.py`, then rebuild. It is a reader-only re-run, with no new simulation. |

**The macro layout after L1–L4:** §5.1 has Table 5.1 (one page). §5.2 has
Figure 5.1 and Table 5.2. §5.3.1 has Figure 5.2 only. §5.3.2 has the half-page
Figure 5.3 and Table 5.4, which can share a page. §5.3.3 has Figure 5.4 (one
page). §5.4 has Table 5.5. The body goes from nine floats to eight, and the
chapter should lose about one page. Captions get one pass after the prose, so
that each decodes its float and states no finding (figure conventions §b2).

---

## 3. What moves out of the §5.2–§5.4 prose, and where it goes

Marc asked to see this before anything moves. **Cut** means the content is
already carried elsewhere, which is named.

| # | Now in | The content | Goes to | Why |
|---|---|---|---|---|
| M1 | §5.2 ¶3 | "the model dispatches the simulator's attack actions in the order its tactics call them, so 14 to 28 % … fail before they run … a design choice of Chapter 4" | §6.1(1). Marc's placeholder already lists it there as "the mechanism". | It is a reason, not an observation. The 2026-09-26 ruling allowed it as a by-construction reason. This overturns that on merit: chapter 6 owns the mechanism, and here it splits A4 from its float. |
| M2 | §5.2 ¶3 | "40 % of the baseline attacker's runs last to the time limit, against 87 to 95 %" | **Cut** | ASP already carries it, and the 100-seed values contradict Table 5.2 (64 % plus 40 % exceeds every run). |
| M3 | §5.2 ¶4 | `\owed`: counting unmapped steps as attack actions lowers attack confidentiality to the baseline attacker's level | §6.5 threats to validity (ruling F13 of 2026-09-25, its other option) | It is a concession about the detector, and it stands on an untracked dry run. |
| M4 | §5.3 head | the zero-exclusion rule; "not told apart" for a shared Scott–Knott rank | §5.1, the MTD ranking unit | It is statistics. §5.1 already defines Scott–Knott and ρ there. |
| M5 | §5.3 head | the APT attacker model as one line is averaged over $c_1$–$c_4$ | §5.1, the Attacker unit, in the ratified wording ("averaged over $c_1$ to $c_4$"; "pools … with equal weight" breaches the registry) | It is a declaration of the setup. Every caption already repeats it. |
| M6 | §5.4 head ¶2 | Cohen's $d$, its interval and the 0.2 threshold | §5.1, the same unit (Q7: rename it *Statistics*) | It is statistics. One home with the other tests. |
| M7 | new in §5.1 | what Spearman's ρ reads: +1 the same order, 0 unrelated, −1 the reverse | §5.1, beside ρ | Marc read −0.03 as a p-value (2026-10-06). The reader will too. |
| M8 | §5.3.1 ¶3 | "The penalty is paid only by the deployments that disrupt … small beside the wait for the next compromise" | §6.2(2) | It is interpretation. Bare "penalty" also has no chapter 5 antecedent. |
| M9 | §5.3.1 ¶3 | the deployment-mix check ("lands before the first compromise in 23 % … moves no time lost by more than 33 s") | Appendix C, with the other robustness checks, or cut | It is a robustness check, not a result. |
| M10 | §5.3.1 head | "Section 5.4 tests whether the failure matrix contributes to this response" | **Cut** | Chapter 6 §6.3 joins the two. |
| M11 | each §5.4.x ¶1 | "is our judgement, so this section tests whether any result … depends on it" ×3 | **Cut** to the §5.4 head, which already says it once | repetition |
| M12 | each §5.4.x ¶1 | the run design (arms, seeds, mechanisms, intervals) | **Cut**: Table 5.1's Ablation row carries it (with L-item: add the random partitions) | duplication of Table 5.1 |
| M13 | §5.4.1 ¶4 | the design of the random-partition control | stays, as one clause; its scope goes to Table 5.1 | The reader needs to know what the control is in order to read E3. |
| M14 | §5.4.x | "Chapter 6 discusses why" ×3 | **Cut** | The chapter preamble says chapter 6 interprets. |
| M15 | §5.3.3 last ¶ | `\owed`: the exponential timing distribution | Q8 | It is declared in Table 5.1 and reported nowhere. |

**Stays, by construction (one clause each):** the APT attacker model's pace is
the tactic durations chapter 4 declared (A4; T4 ratified). Disruption is read
at 2 000 s because at 200 s the next deployment caps time lost (§5.3.1 head,
first use). Each ablation keeps its prediction as one clause, because E4's
"opposite to the prediction" needs it.

---

## 4. The slot sheets

**The paragraph form**, one rule for every results paragraph:
1. **Opener:** "Figure X shows that [finding]." The float is the subject, and
   the finding is in the first sentence. This keeps the 2026-09-26 "Figure X
   shows" form and puts the finding first.
2. **Evidence:** one or two sentences. Each names the compared quantity, and its
   numbers are added after approval.
3. **Exception**, if any: marked, not explained.
4. **By-construction clause**, only where §3 keeps one.

A section opens on its question in one sentence. It closes on its last
finding, with no summary and no hand-off unless the next section's question
needs one.

**Numbers.** The draft carries none. Each slot's facts are named quantities. In
the tex draft a number's place is held by `\prelim{?}` with a comment naming
the quantity and its JSON path, so the swap is mechanical.

**Budget:** about 1 400 words for §5.2–§5.4, against 3 270 now.

### §5.2 (≈ 250 words, 4 paragraphs)

| Slot | Job | Facts (named, no numbers) | Float | Ceiling |
|---|---|---|---|---|
| 2-h | the question | how each attacker acts, and what it achieves, with no MTD running | — | one sentence; define nothing (§4.5 has) |
| 2-a1 | A1 | the share of steps on unmapped tactics (APT); six attack actions only (baseline) | Fig. 5.1(a) | no reason |
| 2-a2 | A2 + the property | impact's share across $c_1$–$c_4$; relative tactic occurrence records objective-specific behaviour | Fig. 5.1(a) | one contrast only |
| 2-b1 | A3 + the property | distinct openings at a short opening length: the profiles against the baseline attacker; the metric records choice of attack strategy; $c_3$ only if Q13 keeps it | Fig. 5.1(b) | never "unpredictable" |
| 2-c1 | A4 | ASP and NCR, each attack profile against the baseline attacker | Table 5.2 | MTTC stays in the table |
| 2-c2 | by construction | the pace is the declared tactic durations (§4.4.2) | — | one clause, possibly merged into 2-c1 |
| 2-c3 | A5 + the property | attack rate lower, attack confidentiality higher; one observation, because the detector counts attack actions; together they record detection avoidance | Table 5.2 | never "stealthy" or "evades" |

### §5.3 head (≈ 50 words)

| Slot | Job | Facts | Ceiling |
|---|---|---|---|
| 3-h1 | the question | how much each MTD mechanism and deployment strategy reduces what each attacker achieves, against the same attacker's no-MTD runs (§5.2) | M4 and M5 have moved to §5.1 |
| 3-h2 | the order | one deployment (§5.3.1), then the interval sweep (§5.3.2), then by mechanism and attack profile (§5.3.3) | one sentence, or merge into 3-h1 |

### §5.3.1 Response to disruption (≈ 150 words, 2 paragraphs)

| Slot | Job | Facts | Float | Ceiling |
|---|---|---|---|---|
| 31-h | why here, at which interval | adaptivity needs MTD to be seen; read at 2 000 s, because at 200 s the next deployment caps time lost | — | one sentence, plus the clause |
| 31-a | B1 | attack actions blocked per MTD deployment: the baseline attacker against the APT attacker model, host layer and service layer; equal within a layer, by construction (§2.2.3) | Fig. 5.2(a) | the construction is a clause, not a paragraph |
| 31-b | B2 | time lost per MTD deployment: host layer (APT attacker model), service diversity (baseline attacker); against the baseline attacker the rest at or below zero; user shuffle below zero for the APT attacker model; below zero decoded once (the next compromise came sooner) | Fig. 5.2(b) | no recovery story; no "resilient" |
| 31-c | B3 | the host layer blocks every baseline attack action and costs it no time | Fig. 5.2(a), (b) | an observation; the reason ("reconnects") is §6.2(2) |

### §5.3.2 Effect of the attacker model, the headline (≈ 230 words, 3 paragraphs)

| Slot | Job | Facts | Float | Ceiling |
|---|---|---|---|---|
| 32-a1 | **C1, stated first** | NCR reduction, host layer against service layer, for each attacker, up to 200 s and at 2 000 s | Fig. 5.3(a), (b) | this sentence *is* the section |
| 32-a2 | C2 | every line falls with the interval; where the APT attacker model's host layer and the baseline attacker's service layer end | Fig. 5.3 | name two lines, not all |
| 32-a3 | C4, the exception | user shuffle at or below zero against the APT attacker model | Fig. 5.3(c) | not explained |
| 32-b1 | C3 | random and alternative against MTDShield, for each attacker; MTDShield's share of decisions on service diversity, and its closeness to service diversity against the APT attacker model | Fig. 5.3(d)–(f); App. D.5 | a consequence of C1, not a second finding; "trained against the baseline attacker" is §6.2(4) |
| 32-c1 | **C5** | the rank-1 sets for each attacker at 200 s; ρ with its interval; and, if Q5 is ratified, the range of ρ over every interval | Table 5.4 | "unrelated", not "misleads" (that is §6.4) |
| 32-c2 | C6 (only if Q3 keeps or moves the ASP rows) | ASP reduction at its ceiling against the APT attacker model under the host layer | Fig. 5.3(g)–(l) or App. E | one sentence |

### §5.3.3 MTD mechanisms and deployment strategies, the depth (≈ 170 words, 2 paragraphs)

| Slot | Job | Facts | Float | Ceiling |
|---|---|---|---|---|
| 33-a1 | D1 | the three host-layer mechanisms: alike against the APT attacker model up to 200 s; IP shuffle above the topology shuffles against the baseline attacker | Fig. 5.4(a)–(c) | — |
| 33-a2 | D2 | service diversity, the baseline attacker's line at 2 000 s | Fig. 5.4(f) | — |
| 33-a3 | D3 + the exception | the profiles follow one line; $c_3$ from 500 s on the host layer | Fig. 5.4 | marked, not explained (the reason is §6.1(3)) |
| 33-b1 | D4 | the baseline attacker's line above every profile under MTDShield, and below them under random and alternative | Fig. 5.4(h)–(j) | — |
| 33-b2 | Q8, conditional | whether the exponential timing distribution changes any order at 200 s | App. table, if built | one sentence or nothing |

### §5.4 Ablation studies (≈ 480 words)

**Against Marc's 2026-09-30 ruling** ("about 250 words each … each paragraph
probably could be one sentence"; the six moves as six sentences). The six moves
are purpose, variant, prediction, float, decision rule and scope. Two of them
are the same for all three ablations: purpose (each component is our judgement)
and the decision rule (Cohen's $d$ against 0.2). Written three times, they
are the repetition Marc asked to cut. This sheet states them once, in the §5.4
head. Each subsection keeps variant, prediction, result and scope, about four
sentences. The amendment is named here so Marc can overturn it (Q11).

| Slot | Job | Facts | Float | Ceiling |
|---|---|---|---|---|
| 4-h1 | the question | three components are our judgement, and each gives one property: the partition (objective-specific behaviour), the failure matrix (adaptivity), the vulnerability memory (learning); does removing one change any result? | — | Cohen's $d$ has moved to §5.1 (M6) |
| 4-h2 | **E1** | only the partition changes a result | Table 5.5 | this is the section's first finding |
| 41-a | E2, what it does | distinct openings without and with the partition | — (Fig. 5.1(b) form; prose only) | — |
| 41-b | E2, what it achieves | NCR and $d$ with no MTD; NCR reduction under IP shuffle at 2 000 s; the count of combinations beyond the negligible band | Table 5.5; Table E.5 | — |
| 41-c | the control, one clause | the partition also builds each Petri net from fewer attack flows; ten random partitions of the same sizes separate the two | Table 5.1 (L-item) | design, one clause |
| 41-d | E3 | random partitions: NCR below both; NCR reduction among theirs | Table 5.5 (after L4) | the reading in one sentence; the why is §6.3 |
| 42-a | E4, the route | after a failed initial access, the share sent back to reconnaissance with and without the failure matrix; $c_2$ has no such move | — | — |
| 42-b | E4, the outcome | $d$ inside the negligible band everywhere; the direction runs opposite to the prediction | Table 5.5 | the scope as one clause: two mechanisms, two intervals |
| 43-a | E5 | the share of exploits that succeed, with and without the memory; $d$ negligible | Table 5.5; Table E.6 | the scope as one clause |
| 43-b | E5, the pool hypothesis (§4.4.4) | with one service per operating system, the exploit share rises most and NCR's $d$ stays below the threshold | Fig. E.1; Table E.6 | the hypothesis holds for exploits, not for NCR, stated as measured |

---

## 5. The post-draft gate, run on every sentence before Marc sees it

1. **At most three clauses.** A sentence over three is split.
2. **The subject leads.** The first noun phrase is what the sentence is about
   (a float, an attacker, a mechanism). No "With …", "Against …" or "Under …"
   opener ahead of the subject.
3. **Plain words.** No metaphor, no inversion opener, no summary claim
   (2026-09-26 ruling); no not-X-but-Y.
4. **One term per thing**, checked against `docs/workflows/terminology.md`.
   Breaches already in the current text, for the redraft to avoid:
   - *defence mechanisms* in §5.1 → **MTD mechanisms**
   - *pools … with equal weight* in §5.3 → **averaged over $c_1$ to $c_4$**
   - *settings* (§5.4.1 "61 settings") → **combinations**
   - bare *the model* (§5.2, §5.4.2) → **the APT attacker model**
   - *routes* (§5.4.2) → chapter 4's own verb for the failure matrix
   - bare *penalty* (§5.3.1) → moved (M8)
   - *arm* (§5.4.1 "every arm"; also Table 5.1's row name) → flag to Marc
   - *its attack profiles $c_1$ to $c_4$ combined* (captions of Figs. 5.2–5.3
     and Tables 5.3–5.4) against *averaged over $c_1$ to $c_4$* (Table 5.5,
     E.5, E.6, and the registry's ratified row of 2026-09-30) → one form (Q12)
5. **Antecedents.** Every noun is one chapters 2–4 or §5.1 gave the reader.
   The check is a census of chapter 5's nouns against the tex up to §5.1. Any
   noun with no antecedent is listed for a chapter 4 insertion, never defined
   mid-result.
6. **Every float is referenced** from the text, and every sentence cites the
   float its finding is read from.
7. **No duplication.** No number or finding appears in two sentences, or in
   both a caption and the text.
8. **The interpretation test:** could the sentence be false while every number
   in the floats stayed the same? If so, it moves to chapter 6.

---

## 6. Rulings owed — ask once, each with a recommendation

| # | Ruling | Recommendation |
|---|---|---|
| Q1 | §1, the spine: ratify, amend or strike each finding | — |
| Q2 | L1: Table 5.3 to Appendix E | yes |
| Q3 | L2: Figure 5.3 keeps the NCR rows; the ASP rows move to Appendix E | yes. Marc called the ASP reading "complete bonkers" (2026-09-30), and its takeaway was never ratified. The move also fixes the caption overflow. |
| Q4 | L3: Table 5.4 gains a ρ row and loses its MTTC columns | yes |
| Q5 | ρ at every interval: the range in the text, the values in a row of Table E.1 | yes. "Unrelated at every interval" is a stronger and more honest claim than one interval chosen. |
| Q6 | L4: the random-partition control into Table 5.5; Table 5.1's Ablation row declares it | yes |
| Q7 | §5.1's "MTD ranking" unit renamed *Statistics*, taking M4–M7 | yes |
| Q8 | the exponential timing distribution: build the owed appendix table plus one sentence (generator work), or move it to §6.5 as declared and not reported | the table, if time allows; otherwise §6.5 |
| Q9 | M1 overturns the 2026-09-26 allowance for the dispatch-failure reason | move it to §6.1(1) |
| Q10 | the paragraph form in §4 ("Figure X shows that [finding]") | yes |
| Q11 | the ablations: purpose and decision rule once in the §5.4 head, not in each subsection (amends the 2026-09-30 "six moves as six sentences") | yes |
| Q12 | one form for the four profiles taken together: *averaged over $c_1$ to $c_4$* (registry, ratified 2026-09-30) or *its attack profiles $c_1$ to $c_4$ combined* (the supervisor's flag, 2026-10-02) | *averaged over* (it is exact for every metric the floats draw), then sweep the captions in the generators |
| Q13 | A3: drop the $c_3$ clause ("I don't know why you're separating C3", 2026-09-30), or keep it as the marked exception | drop it from §5.2; $c_3$'s host-layer exception stays in §5.3.3 (D3), where it is a result |
| Q14 | B3 ("a blocked attack action need not cost time") as a headline for §6.2 | yes. Fig. 5.2 already shows it, and it explains B2. |
| L5 | the memory floats re-read at 1 000 seeds | no ruling needed; it is a correction, done in the numbers phase |

## Validation gate

- Marc rules Q1–Q14.
- The no-number draft passes §5's gate and is ratified by Marc.
- Numbers are filled from `numbers_reported.json` and its siblings, and no
  `\prelim` remains in §5.2–§5.4.
- L1–L4 are applied in the generators, never in the `.tex`.
- The build is clean, with no float overflowing its page.
- §5.2–§5.4 are about 1 400 words.
- This handoff and Parts C–D of the 2026-09-25 handoff are retired in the
  commit that lands it.

## Reading list

1. This file, §1 and §4.
2. The retired brief, §3 (paragraph shape) and §5 (frame):
   `git show 7435c315^:docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md`.
3. `docs/workflows/terminology.md`, the ratified rows.
4. `dissertation.tex` chapter 6 placeholders (l.~8540–8700): what each finding
   must found.
5. `docs/handoffs/2026-10-02_ch5_float_presentation_audit.md`: the float
   standard L1–L4 must keep.

## Out of scope

- §5.1's values (settled 2026-09-25), beyond receiving M4–M7.
- Chapter 6 prose. The moved items go in as content points under its
  placeholders, not as drafted text.
- New runs, except the exponential table if Q8 asks for it.
