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

### §5.1 Statistics unit (was *MTD ranking*; Q7 ruled yes, 2026-10-06), ≈ 150 words

Marc's condition: each statistic is said in plain words, so that a reader who
has never met it can read it off a float.

| Slot | Job | Facts | Ceiling |
|---|---|---|---|
| St-1 | the interval rule | each value carries its 95 % interval; an effect is *told apart from zero* when its interval excludes zero (M4) | define "told apart" here, once |
| St-2 | the profiles as one | where the APT attacker model is one line or column, it is averaged over $c_1$ to $c_4$ (M5, in Q12's wording) | — |
| St-3 | Scott–Knott, in plain words | it sorts the MTD mechanisms and deployment strategies into ranks; two in one rank are not told apart; rank 1 compromises the fewest hosts (cited) | no test mechanics |
| St-4 | ρ, in plain words (M7) | Spearman's ρ compares the two attackers' rankings: 1 when they rank the MTD in the same order, 0 when the orders are unrelated, −1 when one is the reverse of the other | it is not a p-value; the reader should never need to ask |
| St-5 | Cohen's $d$, in plain words (M6) | the difference between two means, in units of their standard deviation over seeds; below 0.2 the component moves the result by less than a fifth of its ordinary seed-to-seed variation, which counts as negligible (Cohen's small effect) | the threshold is Cohen's convention, and is attributed to him as that |

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

## 7. Marc's rulings and his read of the floats (2026-10-06, second turn, dictated)

**Ruled:**
- A4, B2 and B3 accepted (Q14 yes).
- L1: Table 5.3 to Appendix E.
- L4 accepted.
- The move list (§3) accepted.
- Q7 yes, with a condition. The statistics go to §5.1 **and are explained
  there in plain words**: "what's the Spearman's ρ, the Cohen's d, it's not
  really explained to me".

**Not yet ruled:** Q3, Q5, Q11, Q12, Q13. On Q3 Marc notes that his "complete
bonkers" read of ASP was made on the 100-seed run. At 1 000 seeds he reads the
ASP rows as "it just mirrors the same story but with different looking
graphs", which still argues for the appendix.

**His walk-through, the content for the prose** (each reading checked against
the floats; the slips are corrected after the list):
1. Fig. 5.1(a): the baseline attacker has a gap, the unmapped tactics. Fig.
   5.1(b): the baseline attacker is procedural, the same opening every time,
   while the profiles vary across 1 000 runs.
2. Table 5.2: ASP and NCR are far lower than the baseline attacker's. MTTC is
   comparable, slightly longer. The attack rate is lower, about half. Attack
   confidentiality is lower for the baseline attacker, so it is the more likely
   to be detected.
3. Fig. 5.2(a): the baseline attacker is blocked by nearly every deployment,
   because it always has an action running. The APT attacker model is blocked
   a third of the time on the host layer, less on the service layer, almost
   never by user shuffle. Fig. 5.2(b): **"I would expect there to be time lost
   … at least 20 seconds … if there's a confusion penalty … I don't expect it
   to speed up"; the negatives are "scaring me".** See §8.
4. Fig. 5.3: the host layer, random and alternative thwart the APT attacker
   model best. The service layer thwarts the baseline attacker, through
   service diversity. ASP tells the same story. The gap is widest at short
   intervals and narrows at long ones. **The NCR-reduction axis reads from the
   defender's side, and the supervisor, reading from the attacker's side,
   struggled with it.** The caption and the prose must say which way is
   better.
5. Fig. 5.4: all the profiles move together, so "the model itself is more
   important than the profile". IP shuffle has a smaller attacker gap than the
   topology shuffles. Port shuffle and OS diversity work to about 500 s, then
   join the rest. Service diversity is the baseline attacker's most effective
   mechanism. User shuffle reduces almost nothing beyond the shortest interval.
6. Table 5.4: the rankings are "not particularly useful". MTTC "is not really
   doing much" (supports L3).
7. Table 5.5: only the attack profiles move the result. The failure matrix and
   the vulnerability memory are negligible.
8. **The headline:** the attacker model changes the results an MTD evaluation
   gives. A deployment strategy built on one attacker model risks overfitting to
   its assumptions; MTDShield is the case.

**Slips corrected against the floats** (for the prose, not for Marc to redo):
- NCR is the share of the network's hosts compromised. The proportion of runs
  that reach the target is ASP.
- Attack confidentiality is the share of attack actions the scan detector does
  not flag. It is not a count of actions per 60 s; the detector flags an
  action that is the fifth within 60 s. The reading Marc drew from it stands.
- ASP is 5 to 16 times lower than the baseline attacker's, and NCR 2.4 to 3.3
  times lower. "Four times" fits neither.
- On the service layer the APT attacker model is blocked by about one
  deployment in seven, not one in eight.
- "Only one is negligible" in the partition ablation is one combination of
  Table 5.5's five (OS diversity at 2 000 s), not one profile.

**To chapter 6 as content points, not chapter 5 prose:**
- MTDShield overfitting to the baseline attacker (§6.2(4), §6.4).
- Random and alternative drawing three of the seven mechanisms from the host
  layer (§6.2(4)).
- "the model itself is more important than the profile" (§6.1(3)).
- The failure matrix as something the simulator already enforces (§6.3; the
  placeholder has it).
- The memory, if a host takes about two exploits (§6.3; a hypothesis, to check
  before it is written).
- Rankings tied to one simulator (§6.4).

**Marc's idea for the numbers phase:** compare the attackers at a fixed NCR
reduction, for example the interval at which each line falls to 0.5.
Recommendation: use it only as the way slot 32-a2 reads Fig. 5.3 in words
("the APT attacker model's host layer stays above 0.5 to about X s; the
baseline attacker's service layer falls below it by Y s"). It is not a new
metric (the 2026-09-22 rule: no invented metrics).

## 8. Why time lost is negative for the baseline attacker (Marc's question, 2026-10-06)

**Marc:** "I would expect … at least 20 seconds … if there's a confusion
penalty … I don't expect it to speed up."

**Checked on the 1 000-seed corpus** (2 000 s interval). The checker is
`data/results/ch5_defended/time_lost_first_deployment.py`, and its output is
`time_lost_first_deployment_numbers.json`. Each deployment that `time_lost.py`
keeps is split three ways:
- the run's first deployment against the later ones;
- whether the defended run and its no-MTD twin had compromised the same hosts
  at the same times up to the deployment;
- whether the deployment blocked an attack action.

**1. The penalty is charged.** The baseline attacker pays the confusion
penalty, an exponential draw about 20 s, on every interrupt
(`mtdnetwork/operation/attack_operation.py:212`). After a host-layer interrupt
it then restarts at SCAN_HOST, and after a service-layer one at SCAN_PORT.
Marc's expectation is right for every deployment but the first. After the
first, time lost is positive under the host layer: +21 to +33 s against the
baseline attacker, about the penalty plus the rescan.

**2. The first deployment is the exception, and it carries every negative.** At
every interval the first deployment completes one deployment duration into
the run, about 110 s. At that moment the baseline attacker is exploiting its
first host. The forced rescan puts that host back at the head of its queue, so
the attacker gets a second attempt it would not otherwise have had.

| Baseline attacker, 1 000 runs | median time to first compromise | runs whose first compromise is host 0 |
|---|---|---|
| no MTD | 689 s | 456 |
| complete topology shuffle, 2 000 s | 370 s | 766 |
| service diversity, 2 000 s | 332 s | 760 |
| user shuffle, 2 000 s (blocks almost nothing) | 698 s | 453 |

Time lost at the first deployment is −204 to −232 s for every mechanism that
blocks the baseline attacker. That includes service diversity, whose
deployments after the first cost +648 s. Averaged over about five deployments
per run, the first deployment pulls the host-layer means below zero.

**3. It is inherited intent, not a bug.** The intent spec classes the forced
rescan after a block as documented intent: IS-INT-01, IS-INT-05 ("restart from
Phase 1 regardless of prior progress") and IS-INT-07 (Brown §III-D, §V-A;
Zhang §4.4.2). The second attempt is a consequence of that rule. Classified
`conforms`; it is not a bug candidate. The APT attacker model does not get the
second attempt. Its first deployment costs +73 to +106 s under the host layer.

**4. B2's direction survives both subsets.** Host layer against service layer:
- the APT attacker model: +73 to +106 against −2 to +10 s at the first
  deployment; +257 to +361 against +34 to +76 s at the later ones;
- the baseline attacker: about −220 s for every blocking mechanism at the first
  deployment; at the later ones, service diversity +648 s against the host
  layer's +21 to +33 s.

**5. A measurement caveat that stays.** After the first deployment, the
defended run and its no-MTD twin are compared at the same clock time, not at
the same point in their campaigns. The 2026-09-24 record named this (8g-5,
decision 3). The two runs' states differ at 80 % or more of the later deployments (bounded from the checker's marginal counts). The
direction of B2 does not depend on it; the magnitudes might.

**Ruling T1, how to report it** (recommendation first):
- **(a)** Keep the metric as §4.5.3 defines it, and add one by-construction
  sentence to §5.3.1: the first deployment lands while the baseline attacker
  exploits its first host, and the forced rescan gives it a second attempt
  there, which brings its next compromise forward. The appendix table (Table
  5.3 after L1) gains two columns, first deployment and later deployments, so
  the sentence has a float. The caveat in point 5 becomes one sentence in §6.5.
  No new metric, and no post hoc change of definition.
- (b) Exclude the first deployment from time lost. Rejected: it would change
  the definition after seeing the data.
- (c) Report the split in the body figure. Rejected: it doubles Figure 5.2 to
  explain one exception.

**Marc's precision question.** Time lost's intervals are 10–60 s wide, so the
rule (results presentation standard P1) prints it to the 10 s at most. Table
5.3 already rounds each column to its widest interval; the figure needs
nothing finer.

## 9. Third turn (2026-10-06): rulings, and the no-number draft landed

**Ruled by Marc:**
- **T1 (a):** keep the metric. Plus **an appendix item on the negative result**:
  "the attacker goes from this attack action to this one … its information state
  looks like this, the network looks like this … plainly and succinctly …
  my supervisor would like to see that". The discussion takes it up as well.
- **Q5** yes; **L3** yes ("you can remove the MTTC").
- **Q11** yes.
- **Q12:** *averaged over*, "fix that everywhere". Done (commit "One form for
  the four attack profiles taken together"): two generators, four tables and
  three tex captions; no "combined" remains.
- **Q13** yes. §5.2 compares the models with the baseline attacker, not the
  profiles with each other.
- **Q3** still open. The draft keeps one pointer sentence to the ASP rows.

**Marc's framing for §5.2, adopted in the draft:** "we have a wide range of
models … they model a range of behaviours … see if the baseline attacker fits
into that range or it's above the range below the range". Every §5.2
paragraph now reads where the baseline attacker falls against the range of
$c_1$–$c_4$. The comparison between profiles is cut to one clause (the
property relative tactic occurrence records).

**Marc's question answered, from the code and the runs:** "is it because
there's only one host … in its queue?" No. The queue holds all five exposed
endpoints. The baseline attacker gives a host one round of exploits and then
moves to the next, never coming back unless it rescans. The interrupt at about
110 s forces that rescan, and the rescan puts the same host first again. Seed 0
with no MTD: host 0 fails at 151 s, the next endpoint fails, and host 2 falls at
369 s. With complete topology shuffle: host 0 falls at 293 s, in its second
round. It is not always a gain: in seed 2 the no-MTD run takes host 0 at
133 s, and the interrupted run takes it at 274 s.

**Statistics, Marc's misreading kept in view:** he read Spearman's ρ as a
p-value ("0 to 1 … below 0.05 is significant"). The §5.1 Statistics unit now
says what ρ reads (1 same order, 0 unrelated, −1 reversed). It never mentions a
p-value: the definition alone leaves nothing to confuse.

**Landed (DRAFT STATE):**
- the §5.1 Statistics unit (St-1 to St-5);
- all twenty §5.2–§5.4 prose blocks, rebuilt from §4 with every number
  `\prelim{?}`;
- each block's NUMBERS comment, naming each `?` and its JSON;
- the moved content points, as comments under chapter 6's §6.1, §6.2 and §6.5
  placeholders.

The build is clean (0 errors, no undefined references). Chapter 5 is one page
shorter. Its printed prose is about 1 600 words: §5.3.1 is over its slot,
because of T1's first-deployment explanation, and the exponential `\owed`
block (Q8) is untouched.

**Gate run on the draft (§5):**
- Openers: four that put a phrase before the subject were fixed.
- Clauses: no sentence the draft wrote exceeds three.
- Terms: the registry breaches listed in §5 item 4 are gone from the rewritten
  blocks.
- Antecedents: one gap. Chapter 2 never says the baseline attacker moves to the
  next host when every attack on one fails, and §5.3.1 now leans on it. It is
  carried as an `\owed` mark.
- Duplication: B1's "a deployment's layer decides" is in Figure 5.2's caption
  and Table 5.3's as well as the text. It goes in the caption pass.

**Next, in order:**
1. Marc reads the draft.
2. Q3 and Q8.
3. The numbers phase: L5 first (the memory re-read), then fill every `?` from
   the NUMBERS lines.
4. L1–L4 in the generators, plus Table 5.1's random-partition row.
5. The appendix item on the first deployment (a worked trace with the tracer,
   plus the split columns).
6. The chapter 2 clause.
7. The caption pass.

## 10. Fourth turn (2026-10-06): the bug question, L5 done, the chapter 2 clause, Q3 and Q8

**"That just sounds like a bug" (Marc): classified `conforms`, with evidence.**
His disposition is still owed. With no MTD the baseline attacker also comes
back to a host it left:
- when its queue holds no reachable host, ENUM_HOST hands over to SCAN_HOST
  (`attack_operation.py` `_enum_host`);
- the new scan lists every reachable host it has not given up on, exposed
  endpoints included;
- it gives up on a host only after ten attempts (`constants.py`
  ATTACKER_THRESHOLD = 10; IS-SCN-04, Brown §V-C and Table I).

So retrying a host is Brown's design. The first deployment's forced rescan
(IS-INT-01, IS-INT-05) moves that retry earlier, before the attacker has
tried the other endpoints. A rescan that put a partly tried host at the back
of the queue is documented nowhere. Treating that ordering as a bug, and
changing the inherited simulator, is Marc's call. **Recommendation:** leave
it. Explain it in the appendix item, and let chapter 6 §6.2(2) read it.

**L5 done: the memory floats re-read at 1 000 seeds, and the cause fixed.**
`memory_ablation.py` intersected the on and off arms with the 100-seed
perfect-exploit diagnostic arm. That cut every reported comparison to 100
seeds, under captions saying 1 000. It now compares on against off over the
1 000 seeds those two arms share; the perfect arm keeps its own 100.
Regenerated: `memory_ablation_numbers.json`, Table E.6, Figure E.1, and Table
5.5's memory block. That block's no-MTD row (0.171) now equals the partition
block's, which closes the 2026-10-02 flag (0.167 against 0.171).

Every on-minus-off interval of $d$ now lies wholly inside ±0.2; the widest
reaches +0.15. With one service per operating system, the share of exploits
that succeed rises from 0.69 to 0.92. The §5.4.3 verdict ("holds for the share
of exploits that succeed, and not for NCR") is now defended. Its `\owed`
mark is removed.

**Chapter 2 clause added** (§2.2.3, after the per-host order): if all three
attacks fail, the attacker moves to the next host on its list. When the list
runs out it scans again, and the new list holds every reachable host,
including those already tried. It gives up on a host after ten attempts, but
never on a target host. The clause is DRAFT STATE, with its code and intent
pins in the comment.

**Q3 ruled yes (Marc):** "all the ASP reduction rows … basically the same thing
as the NCR reduction … NCR reduction is more of a fine grained tool". The
ruling extends to moving the ASP reduction definition to the appendix "if
needed". The full extent, for the float phase:
- Fig. 5.3 rows (g)–(l) go to Appendix E as their own figure, with the
  §4.5.3 definition of ASP reduction beside them;
- Table 5.4 drops its ASP-reduction column with its MTTC columns (L3);
- Table 4.3's row moves, and the metric count drops from eleven to ten
  (§5.1 Metrics, Table 5.1's Metrics row);
- the §5.3.2 pointer sentence to the ASP rows becomes an appendix pointer or
  goes.

**Q8 ruled (Marc):** varying the timing distribution "might be a threat to
validity … second-rate". Applied:
- the exponential level is cut from Table 5.1, with its caption clause;
- §5.1's "the timing distribution is varied separately" is cut;
- §5.3.3's `\owed` paragraph is cut;
- §6.5 gains a content point.

**Blank cells (Marc dislikes them):** the open ruling is B, in the chat.
S1 (ratified 2026-10-02) follows APA 7 §7.12: blank means not applicable, and
a dash means not reported (S2). A dash in the no-MTD row would give the dash
two meanings. **Recommendation:** write *reference* in the no-MTD row's
reduction cells (S5: words over symbols). Marc rules.

**Table 5.1 (Marc: "what do we need in there … who's using this … what's the
convention"):** the proposal is in the chat, ruling A. Its layout comes from
§k: a factor-and-level table of what is varied, at which levels, and what is
held, each value with its source. Definitions stay where they are defined.

## 11. Fifth turn (2026-10-06): A, the citation and the symbols, the numbers, L1–L4, Q3

**Ruled:**
- **B:** blank cells stay ("don't worry about having the word reference").
- **Spearman citation:** added (`spearman1904proof`).
- **A:** Table 5.1 rebuilt as proposed, with near-periodic timing made clear.
- **Symbols:** "let's make it clear".

**Applied:**
- **Table 5.1:**
  - three groups of rows: varied in every combination, varied in one ablation
    each, held;
  - the Metrics row, the deployment durations and the memory-on row are gone,
    and "Arm" is now "Attacker";
  - the random partitions are declared;
  - placed `[t]`, so it opens at the top of a page with text below.
- **Chapter 2, §2.2.2:** a sentence says what near-periodic means (each
  interval is the set value plus a random delay of 0.5 s on average; code
  `exponential_variates(loc, 0.5)`). Table 5.1's timing row says the same.
- **§5.1 Statistics:** "Spearman's rank correlation, $\rho$ (rho)" with its
  citation, and "the effect size Cohen's $d$".
- **Numbers filled:** every `\prelim{?}` in §5.2–§5.4, from the 1 000-seed
  JSON named in each NUMBERS comment. The fill corrected four ratified
  findings against the data:
  - **D2:** IP shuffle, as well as service diversity, keeps a reduction against
    the baseline attacker at every interval (0.19 [0.16, 0.22] at 2 000 s).
  - **D3:** $c_3$'s larger host-layer reduction holds at 500 and 1 000 s, not
    at 2 000 s under the topology shuffles.
  - **E3:** "the random partitions compromise less than both" holds with no
    MTD only. Under IP shuffle at 200 s all three sit near 0.007.
  - **C4:** user shuffle against the APT attacker model is below zero at every
    interval, its interval excluding zero; "at or below" became "below".
- **L1:** Table 5.3 moved to Appendix E, where it is now Table E.1.
- **Q3:** Figure 5.3 now draws NCR reduction only, as a half page (the caption
  overflow is fixed). The ASP rows became Figure E.1
  (`fig_F-0b_interval_asp`, generator `--only asp`). ASP reduction's definition
  moved to Appendix E beside it, with the reason the chapter ranks on NCR.
  §4.5.3's NCR paragraph inherited the 0/1/negative reading and the Alavizadeh
  form. Table 4.3 lost its ASP-reduction row, and §5.1 now says "ten metrics".
- **L3:** Table 5.3 (the ranking) shows rank and NCR reduction only, with
  Spearman's ρ and its interval as the foot row. The blank no-MTD row is cut,
  and the reference NCR is in the caption.
- **L4:** Table 5.5 (now 5.4) has a "random" column under NCR and under NCR
  reduction: the mean over the ten partitions, attack-profiles block only.
  §5.4.1 reads the mean (0.33 against 0.35) from it.

**Build:** clean, with no undefined references. Overfull boxes are down to
12, none of them in this turn's floats; Table C.1 (`tab_C-0a`) is the widest
existing one. Chapter 5 is printed pp. 30–41, down from 30–43. The PDF is
copied to `docs/thesis/dissertation.pdf`.

**Still open:**
1. Marc's read of the numbered draft.
2. The appendix item on the first deployment (a worked trace, plus the split
   columns): the `\owed` in §5.3.1.
3. The caption pass. For example, Figure 5.2's and Table E.1's captions still
   state B1's "a deployment's layer decides", which the text now carries.
4. FLOATS.md is not updated; another session holds it (B13).

## 12. Sixth turn (2026-10-06): the high-level critique of §5.1, before any paragraph is touched

Marc's ask: is the title right, is the split right, do the table and the prose
work together, what does the reader need, what does the examiner expect. He
reads paragraph by paragraph only after this. Nothing in §5.1 has moved.

**Build fix:** the PDF handed over in §11 printed Spearman's citation as
"[?]" (it was copied before the last pass). Rebuilt; it is now [53].

**C1. Titles: keep both.** "Evaluation" and "Experimental setup" are
conventional. The field's dominant form puts the setup at the head of the
results (evaluation_conventions §a: Brown, Zhang, Hong, Kim), so the move out
of the method was right. "Results" would misname a chapter that also holds the
setup and the ablations. The preamble's "Section 5.1 sets out the experimental
setup: the network, attacker, ..." names the title twice and lists the run-in
heads, so it follows whatever split is ruled.

**C2. The fault is the axis.** The units are the simulation's parts (network,
attacker, MTD: chapter 2's own split) plus three analysis notes. That was the
2026-09-18 ruling, made when §5.1 was a run plan. Since then the frame has
become SQ3, a comparison. An examiner arriving at a setup asks five questions:

| Examiner's question | Where §5.1 answers it now |
|---|---|
| E1. What is compared with what, and against what reference? | Split over Attacker, MTD (the interval is buried inside it), the table caption, and the last sentence of MTD (the no-MTD reference). The three ablations, a third of the table, have no prose. |
| E2. Is it fair: does only the attacker change? | Never stated. Half is in Network's last sentence and half in Runs ("the same seeds"). The sentence that answers it is parked as a comment from the 4.4 preamble ("Both attackers run on the same MTDSim ... so a difference between the two attackers' runs is a difference in the attacker"). |
| E3. What is held, and is it the field's configuration? | The table, and Network repeats it. Chapter 2 §2.2.1 already gives 50 hosts, four levels, eight subnets and five endpoints as the defaults, so the only setup fact is "two target hosts instead of five". |
| E4. How many runs, and why is that enough? | Runs: sound. |
| E5. How does a difference become a claim? | Statistics: five jobs in one paragraph (below). |

**C3. Accretion.** Each pass answered one question that had been asked once, in
a clause: Zhang's second network of four; the 25–200 host range; three
intervals to a decade; three reasons for tabling 200 s; MTTC's NCHS rule; why
NCR ranks; the gloss on Cohen's d. Each clause is true. Together they make
622 words of provenance that the table already carries as citations. The
caption drives this: "an uncited value is argued in the text" pulls a clause
into the prose for every uncited value.

**C4. The table and the prose do not divide the labour.** The table should
hold the values and their sources. The prose should hold what a table cannot:
the design logic and the analysis.

- **In both:** the network values, the MTD list, the intervals, the seeds and
  the sources.
- **Only in the prose:** the reference, the choice of 200 s, the MTTC rule and
  all the statistics.
- **Only in the table:** the three ablations, the random partitions, the time
  limit with its 80 % stop, and the timing distribution.
- **Where the two disagree:**
  - The heading "Varied in every combination" is false for no MTD. It is run
    once per attacker, with no interval (`run_corpus.py` docstring, l.22).
  - The attack graph runs the full grid but sits under the ablations.

**C5. Table form.**

- **Group rows:**
  - The group rows carry no indent. Table 2.2, the same form, indents with
    `\quad`, so the house style has two versions.
  - The stripes run through the italic group rows, so a group row looks like a
    data row.
- **Value cells:**
  - The value cells are semicolon lists with citations inside them, and the
    ablation cells are whole sentences.
  - A Source column would keep the values short and line the citations up.
    This is the per-row data-source form in STRESS-DES (§k1).
- **Groups:** Compared / Reference / Held / Ablations would match the design.

**C6. The Statistics paragraph.**

- **"Told apart" is an invented term.** It is used twice. The field says
  "differs from zero".
- **Its five jobs are out of reading order:**
  1. the interval rule;
  2. averaging over $c_1$ to $c_4$, which is a reporting convention;
  3. Scott–Knott ranking and why NCR is used;
  4. $\rho$;
  5. $d$, its threshold and its gloss.

  Reading order follows use: the interval (every float), the averaging, the
  ranking and $\rho$ (§5.3.2), then $d$ (§5.4).
- **How the interval is computed is never declared.** "Percentile bootstrap
  over runs" appears in about 13 captions but never in the setup, so method
  sits in captions (evaluation_conventions §j8 item 6).
- **Metrics is one pointer plus the MTTC rule.** It folds into the same unit.

**C7. Form.**

- **The run-ins:** six run-in heads, each with vertical space above, holding
  one to eight sentences.
- **The table:** a page-high float splits the MTD paragraph mid-sentence ("the
  one | MTDShield was trained at").
- **The result:** it reads as notes. With the table as the part to scan, the
  prose's job is to read.

**Proposal (shape only, for Marc's ruling).** The units follow the examiner's
questions, and the table is regrouped to match:

| Unit | Answers | Holds |
|---|---|---|
| Design | E1, E2 | Both attackers under each MTD at six intervals. No MTD is the reference. The simulator, network and seeds are the same, so a difference is the attacker's. One clause gives the interval range. |
| Held settings | E3 | The default network of §2.2.1 with two target hosts, and the time limit. The values are in the table. |
| Ablations | — | One sentence, or none, leaving everything to §5.4. |
| Analysis | E5 | The metrics of §4.5. 95 % percentile bootstrap intervals. Averaging over $c_1$ to $c_4$. The MTTC rule. The ranking and $\rho$. Then $d$. |
| Runs | E4 | As now. |

The target is about 300 words. This overturns the 2026-09-18 rulings ("the
units are the simulation's moving parts"; "open on the first object") on merit:
the frame they served was a run plan, and SQ3 is now a comparison.

**Rulings asked:**

- **R1:** split by the examiner's questions (recommended).
- **R2:** the ablation settings stay in Table 5.1 (recommended: one experiment,
  one table) or move to §5.4.
- **R3:** keep the run-in heads, matched to the table groups (recommended), or
  use plain paragraphs.

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

## 13. Seventh turn (2026-10-06): §5.1 and Table 5.1 redrafted to the §12 shape

Marc's rulings:
- **R1:** split by the examiner's questions, implicitly ("it will answer the
  examiner's internal benchmark").
- **R2:** keep the ablations in Table 5.1, last ("it's the last bit").
- **R3:** keep the run-in heads.
- **Terms:** every noun is from chapters 2–4 or from the MTD evaluation field
  ("told apart is terrible").
- **Stripes:** "present it as you see fit". He may rule them out house-wide
  later.

**Units, in order, each with its reason:**

| Unit | What it holds | Why |
|---|---|---|
| Comparison | The attackers, every MTD, the six deployment intervals and why, the no-MTD runs (no interval), and MTDShield as released (Appendix D). Then the fairness sentence: "same networks, same MTD, same six attack actions … a difference is a difference in the attacker". | It answers E1 and E2. The fairness sentence is the parked 4.4-preamble candidate. |
| Held settings | The default network of §2.2.1 with two target hosts, the released code as the basis, and the targeted attack scenario, with a pointer to the table. | It answers E3. Chapter 2 is not restated. |
| Runs | Kept. | It comes before Analysis because Analysis refers to seeds and runs. |
| Analysis, paragraph 1 | How a value is reported: the confidence intervals, the differs-from-zero rule, averaging over $c_1$ to $c_4$, and the MTTC rule. | It answers E5. |
| Analysis, paragraph 2 | How MTD is compared: Cohen's $d$, then Scott–Knott, then $\rho$. | $d$ comes first because the Scott–Knott merge uses it. |
| Ablation studies | Their settings in the table, and the rule for a negligible component, the interval of $d$ inside ±0.2. | Last, per R2. §5.4 already gives the purpose and the seeds. |

**Cut, each because something else already carries it:**
- **Network values:** chapter 2 and the table.
- **Zhang's second network and the 25–200 host range:** Table 2.4.
- **"Where one interval is tabled it is 200 s":** this is now false, because
  Figure 5.2 is at 2 000 s. Each caption names its own interval.
- **MTDShield's training interval:** Appendix D.
- **"Both attackers are measured on the ten metrics":** the preamble says it.
- **The gloss on $d$ ("a fifth of its variation"):** it repeated the
  definition.

**Interval facts verified in code:**
- **Means** (`measures.mean_ci`) use the normal approximation, 1.96 SD/√n.
- **These use a seeded percentile bootstrap over runs:**
  - reductions (`analyse.suppression`, unpaired);
  - time lost (`time_lost.py`, 2 000 resamples);
  - ratios;
  - $\rho$.

  This is declared once, so the caption pass can shorten "95 % percentile
  bootstrap intervals over runs" to "95 % intervals".
- **The differs-from-zero rule holds where the text uses it:**
  - user shuffle's NCR reduction against the APT attacker model excludes zero
    at all six intervals;
  - the baseline attacker's negative time lost under OS diversity at 2 000 s
    is [−69, −42] s.

**Table 5.1:**
- The columns are Setting | Value | Source, with sources in their own column.
- The groups are Compared / Held / Ablation studies, with the rows indented as
  in Table 2.2.
- The caption states the no-MTD exception. "Varied in every combination" was
  false.
- The row names are ratified terms: "Interval distribution", and "End of run"
  as in Table 2.4.
- The stripes are kept under the house rule.

**Preamble:** "the network, attacker, MTD, metrics, statistics and runs" now
reads "the comparison, held settings, runs, analysis and ablation studies".

**Noun check:**
- **From chapters 2–4:** default network, goal, attack graph, attack profile,
  attack action, deployed alone, factor.
- **From the field, each cited:** normal approximation; percentile bootstrap
  (Efron); Scott–Knott effect size difference test; Cohen's $d$; Spearman's
  $\rho$; significantly.
- **Defined in their own cell:** the random partitions.

**Length:** about 540 words, down from 622. Half of it is Analysis, which holds
the plain definitions of $\rho$ and $d$ that Marc asked for.

**Build:** 0 errors, 0 undefined references, and 12 overfull boxes, all
pre-existing. §5.1 runs from printed p.30 to p.32.

**Still open:**
1. The chapter 6 conclusion-validity placeholder says "Spearman's $\rho$
   without an interval". This is stale: $\rho$ now has one.
2. The old §5.1 ruling comments after the Runs unit, before
   `\section{APT attacker model versus baseline attacker}`, are kept as trail.
   They describe text that no longer stands.
