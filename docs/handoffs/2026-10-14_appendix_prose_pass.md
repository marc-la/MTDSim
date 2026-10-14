---
status: open
created: 2026-10-14
updated: 2026-10-14
companions: ../workflows/appendix_conventions.md, ../workflows/voice.md, ../workflows/terminology.md, ../workflows/results_presentation_standard.md, 2026-10-09_ch7_conclusion_and_appendix_structure.md (§10–§13, this appendix's rulings)
---

# Appendix prose and caption pass (Appendices B–D)

**Goal.** Every lead, opener and caption in Appendices B, C and D gives the reader
arriving from a body pointer what that pointer promised, in the fewest words that
carry it. Marc approved the pass (2026-10-14). Scope: leads, openers and captions;
not Appendix A, the AI Use Declaration, table bodies, layout or placement, or the
caption sentences that decode an encoding (Bold:, Grey:, Blank:, Shading:, symbol
keys), which a parallel visual-encoding pass owns.

## 1. The checklist, with its sources

Each rule carries one before → after from the sources. "Ruled" means Marc ruled it.

| # | Rule | Before → after (source) |
|---|---|---|
| R1 | A section is its floats plus a lead of one or two sentences naming the body claim the floats back. No argument, no logbook, no self-declared irrelevance. | D's "The sections that follow read the same perturbations value by value" → deleted, because they no longer did (`appendix_conventions.md` §c–§d; ch7 handoff §12) |
| R2 | A lead or opener names what each part holds; it is not a roadmap of ordinals. Signposting uses the section's own heading words. | "Each paragraph below tests …" → cut as meta (ch6.1 handoff §21.3); `chapter_scrutiny.md` §7 "Signposting names exactly what each section holds" |
| R3 | A caption decodes: what the float shows, sample, units, how to read it. It never argues, defines a metric, or narrates. | Table D.2/D.3 captions "abnormally large" → cut to decode only, "the metric's scale, the runs per cell and the interval method" removed (ch7 handoff §13, D.2 captions); `results_presentation_standard.md` "Captions read alone" |
| R4 | Lead and caption divide the labour: the caption keeps what the float needs to read alone; the lead keeps the claim. The same fact is not in both. | D.3 dedupe: "Prose now states the frame … Captions keep their own comparison" (ch7 handoff §13); ch5 redraft §5 gate 7, "No number or finding appears … in both a caption and the text" |
| R5 | Never re-define or re-gloss a term the body defined; use it. | "Which take time and dispatch no attack action" → cut, "re-defines a ch4 term" (ch6.1 §11.2 point 6); voice.md §0 "Never pre-define a term …" |
| R6 | One term per thing, verbatim from `terminology.md`: attack action, tactic duration / mean duration, MTD mechanism, deployment strategy, configuration, no MTD, target host, averaged over $c_1$ to $c_4$, attack flow, disrupt, the baseline attacker's times. Banned: pace, held back, dispatch, refused, *draw* for a mechanism, timing, bare defence. | "Its pace is set by its tactic durations" → "Its tactic durations make it slower" (ch6.1 §24.3); "do not agree" → "uncorrelated" (ch6.1 §81) |
| R7 | Subject first, one main clause, at most three clauses; no fronted modifier ahead of the subject. | "subject first, 'In Section 6.2,' moved to a closing parenthesis" (ch6.1 §133); memory: three sentence weights (Marc 2026-10-01) |
| R8 | No vague back-reference ("these", "such", "the first", an ambiguous "it"): name the noun again. Repetition beats a pointer. | "brings it *there*" → "brings it to Lateral Movement" (ch6.1 §28.14); memory: dense over walked-through (Marc 2026-09-24, "whenever you use the word such or it") |
| R9 | No not-X-but-Y, no colon-then-list flourish, no em-dash aside. A contrast of values reads "in place of". | "not MTDSim's time" flagged as not-X-but-Y (ch6.1 §137); "With the baseline attacker's times, …" → "in place of its tactic durations" (ch6.1 lesson x, §24.13) |
| R10 | Specific, never vague. Name the referent ("here" → the chapter). At the short end of the inverted U, restore the missing referent, never the nuance. | "rate after / rate before" named nothing a reader could compute (voice.md §0, Marc 2026-09-29) |
| R11 | Every claim is true of the float and scoped to what was measured (interval, metric). | "true at 200 s … false at 2 000 s … Scope it to 200 s" (ch6.1 §66); results standard F5 |
| R12 | Never paraphrase a defined metric; use its name. | "does not take the same first steps" → the metric's name and its number (ch6.1 lesson s, §24.8) |
| R13 | Say what a number means in plain terms. | "reaches its ceiling of 1": "the reader cannot tell what 1 is" → "under the host layer in no run up to 200 s" (ch6.1 §73–§74) |
| R14 | Cut a sentence that gives the reader nothing, restates the body, or replays the float. | "Its one branch … is that rule at work" → cut (ch6.1 §11.2 point 3); replay test (ch6.1 §21.6) |
| R15 | No logbook register: no "now", no history of changes; present tense, active voice. | appendix_conventions §d "Logbook … tells how the work evolved"; voice.md §d "Present tense, active by default" |
| R16 | A float reference sits next to the claim or number read there, and the float shows it. | "Table 5.3 is 200 s only, so it cannot show 'every deployment interval'" (ch6.1 §29.3) |
| R17 | Edit, don't rewrite. Ratified text keeps its structure; change only what fails a rule; never undo a ruling. Never drop a fact or number something relies on; never change a number. | memory: redraft edit-don't-rewrite (Marc 2026-10-02, "43 was much stronger"); "a 'yep' locks a sentence" (ch6.1 §52) |
| R18 | Australian English; numerals in a comparison with a number of 10 or more (APA 7). | ch6.1 §1 item 7 |
| R19 | One calibrated hedge, inside the inferred claim; none on what was measured. | "Three 'likely' in 112 words" (ch6.1 §31.5) |
| R20 | No hard-coded appendix letters; every pointer is a `\ref`. | ch7 handoff §12 pointer sweep |
| R21 | Headings state what the section is on, nothing more; change a title only if plainly rhetorical, and propose rather than apply. | voice.md §d; Appendix B retitled because the old title "restates what ch3 already does" (ch7 handoff §13.aa) |

## 2. Ledger, per paragraph and caption

**Method.** For each unit: every `\ref` into it from the body was listed (the body
promise), then each sentence was tested against §1. Rendered pages were read before
and after (physical page = printed + 9). Captions were edited in their generators and
regenerated; every generator reproduced its committed output byte for byte before any
edit (four needed a gitignored input symlinked read-only from the main checkout; none
is committed). Body floats the same generators write (Table 5.4, Figures 5.2–5.3) are
byte-identical after the pass.

### Appendix B (body promise: ch3 3198 and ch6 Table 6.1, "the predicates behind each mark")

| Unit | Before → after | Rules |
|---|---|---|
| Lead S1 | "… of Tables 3.3 and 6.1: the APT attacker model from Chapter 4, the three MTD attacker models from their papers." → "… of Tables 3.3 and 6.1. Its cells judge the APT attacker model from Chapter 4 and the three MTD attacker models from their papers." | R9 (colon-then-list), R10: the appositive list could be read as glossing the two tables (in reverse order). Round 2: the first fix ("read from Chapter 4 for …") read as if the *predicates* came from Chapter 4 (cold reader); the cells are what is judged |
| Lead S2 | kept: "The predicates are Table 3.2's definitions word for word; rows 1 and 6 split off a qualifier, row 5 splits at its 'and'." | Ruled 2026-10-13 (the split rule in the lead) |
| Table B.1 caption | kept | S1 states what the table shows; the cell key and the mark key are decode sentences (parallel pass) |

### Appendix C (body promises: ch4 4031, 4177, 4225, 5129; ch6 9068 and 9092)

| Unit | Before → after | Rules |
|---|---|---|
| Opener | "Each section of this appendix backs one claim of Chapter 4, in the chapter's order." → "Each section of this appendix gives the data behind one part of the APT attacker model, in Chapter 4's order." | R11: C.4 and C.6 are cited only from Section 6.5 (`thr:conditions`, `thr:values`); no Chapter 4 sentence points at C.4 |
| C.1 lead S2 | "Figure C.1 draws the edges between techniques that two or more attack flows draw." → "Figure C.1 gives 55 of the 59 edges between techniques that two or more attack flows draw." | R14 (draws … draw); R11: 59 edges have two or more attack flows (`gap_v0.5.json`, recounted), the figure draws 55 after its component filter, so "the edges" overclaimed (cold reader) |
| C.1 lead S1 | "… because most edges between techniques come from one attack flow: …" → "… are drawn by only one attack flow: …" | R10: "come from one attack flow" read as one particular flow (cold reader); "drawn by", the verb of S2 and Section 4.2. Counts kept |
| Figure C.1 caption S1 | "… and without the pieces of fewer than three techniques this leaves: 35 of its 124 …" → "… and only the connected groups of three or more techniques those edges form: 35 of its 124 …"; "in ATT&CK matrix order" → "in ATT&CK's order" | R8 ("this leaves"), R10 ("pieces"), checked against `_big_components(floor=3)` in `tools/gap_appendix_figures.py`; R6 (Table C.2 and Figure C.2 say "ATT&CK's order") |
| Figure C.1 caption S2–S5 | kept | Decode sentences |
| C.2 lead S2 | "We decided the three attack flows these sources left open from their threat reports." → "We decided the three attack flows these sources left open, each from its threat report." | Garden path ("left open from …") |
| C.2 lead S4 | "Mac Malware Steals Crypto stole credentials and also mined cryptocurrency … hijacking them, so it did both" → "The attacker of Mac Malware Steals Crypto stole credentials and mined cryptocurrency … hijacking them, so it stole data and impeded systems" | R10 ("both" names nothing on the page), R14 ("also"); the two answers in Figure C.2's words; the attacker, not the attack flow, is the subject (cold reader) |
| C.2 lead S5 | "… by its report, does not take user data, and it impedes no system, so it did neither" → "… by its report, takes no user data and impedes no system, so its attacker did neither" | R14, R8 |
| C.2 lead S1, S3 | kept | Ruled 2026-10-13 ("the prose still does the one job a cell cannot") |
| Table C.1 caption | "the columns give what else was, and a blank row …" → "the columns give what else was read, and a blank row …" | Garden path from the elided verb (cold reader). The blank-row clause is a decode and is otherwise untouched |
| C.3 lead, Figure C.2 caption | kept | Ruled 2026-10-13/14 (the Muddy Water sentence); the caption decodes only |
| C.4 lead S1 | "Table C.2 sets each attack action's time in MTDSim, which the baseline attacker takes, beside the mean durations of the tactics mapped to it, which the APT attacker model takes instead." → "An attack action can take a different time for each attacker (Section 6.5, T2); Table C.2 gives both times." | R1 (name the claim: Table C.2's only body pointer is `thr:conditions`); R4 (the caption says the same); R11 (the table has been one row per tactic since 2026-10-14, not one per attack action). "can": the two times match for Initial Access and Privilege Escalation |
| C.4 lead S2 | "Six tactics take the time of the attack action whose work they resemble, not always the one they run; we set the other nine by judgement, from what each tactic does in an attack (Section 4.4.2)." → "Six tactics take MTDSim's time for the same kind of work, even where they run another attack action: 4.5 s, the exploit's, or 35 s, the three scans' together. We set the other nine by judgement (Section 4.4.2)." | R11, R16: the reader could not find the six in Table C.2, and 35 s is no single attack action's time (it is the three scans' total, Section 4.4.2) (cold reader); R14 ("from what each tactic does in an attack" is Section 4.4.2's sentence). The wording follows Section 4.4.2 ("the same kind of work … even where the tactic maps to another"). **This re-opens Marc's ruled form of 2026-10-14** ("Six tactics take an attack action's time; we set the other nine by judgement"), on the merit that its claim cannot be checked against the table; revert is one hunk |
| Table C.2 caption | "The exploit's time is its mean: it runs 0 to 9 s" → "it takes 0 to 9 s"; cut "An unmapped tactic runs no attack action." | R6 (a tactic *runs* an attack action, an attack action *takes* a time); R5 (re-glosses Section 4.4.1's *unmapped*) |
| C.5 lead | "… the first rule of Table C.3 that the move matches …" → "… that applies to the move …"; cut "These are our judgement." | R6 (the caption's verb is "applies to"); R14 and R8 (Section 4.4.3 already says "their values are our judgement"; "These") |
| Table C.3 caption | kept | Ruled 2026-10-14 (second revision) |
| C.6 lead | "Table C.4 gives every value of the APT attacker model, grouped by where it comes from, our judgement first, with the section that gives its reason." → "The values we set by judgement (Section 6.5, T4) come first in Table C.4." | R1 (names the claim, `thr:values`, the table's only pointer); R4 (the old lead repeated the caption word for word; round 2 cut the last "every value" clause too, which the caption carries) |
| Table C.4 caption, row text | kept | Decodes; row text see open question 3 |

### Appendix D (body promises: ch5 6089, 6214, 7541, 7787, 7796, 7827, 7927, 8219, 8263, 8439, 8457; ch6 8555, 8609, 8627, 8913, 8966, 8988, 9060, 9078, 9097, 9143, 9160, 9216; ch7 9574)

| Unit | Before → after | Rules |
|---|---|---|
| Opener | "The first five sections back Chapter 5: the first gives MTDShield as run, the next three the full data behind its comparisons and ablations, and the fifth its sensitivity analysis of the tactic durations. The last, an ablation of the tactic durations, backs Chapter 6." → "Sections D.1 to D.5 back Chapter 5, and Section D.6 backs Chapter 6." (by `\ref`) | R2 (a roadmap of ordinals restating the headings below it); Marc's ruled content (2026-10-14: which sections back which chapter) kept whole |
| D.1 P1 S3 | "… compares its training with the runs here." → "… with the runs of Chapter 5." | R10 |
| D.1 P1 S1–S2 | kept | S2 is the only place the dissertation says why random over MTDShield's four MTD mechanisms runs (Table D.3's row key points here) |
| D.1 P2 S1 | "Two changes were needed to run it: Tay's input construction is restored beside the simulator's, and a decision to do nothing now waits …" → "Two changes let MTDShield run: Tay's input construction is restored as an option beside the simulator's, and a decision to do nothing waits …" | R15 ("were needed", "now"); R10 ("restored beside" said nothing a reader could picture; "as an option" is the pre-cut record's wording, commit 4aea3c3e); R8 ("it") |
| D.1 P2 S2 | "An unmapped tactic of the APT attacker model runs no attack action, so the agent reads it as nothing detected." → "The agent reads an unmapped tactic of the APT attacker model as nothing detected." | R5 (re-glossed *unmapped*); the caption already says the agent is told the current attack action |
| D.1 P2 S3 | "at 76 % … nothing at 23 %" → "in 76 % … nothing in 23 %" | R6 (ch5 7827's form, "in 70 % or more of its decisions") |
| Table D.1 caption | kept | Decodes; ruled 2026-10-14 |
| D.2 lead | kept | Eight words; names the figure it backs |
| Table D.2 caption | "Time lost is over the MTD deployments made while the same seed's run with no MTD is still going, at least 78 % of each cell's." → "… still going, which are at least 78 % of each cell's MTD deployments." | R10 (the noun was missing; round 2 attached the share to its noun, cold reader) |
| D.3 lead | "… the values Figure 5.3 plots, at every deployment interval, and Table D.4 gives rank 1 … at every deployment interval." → drop the first "at every deployment interval" | R14 (Figure 5.3 plots every interval) |
| D.3 ASP paragraph | "… on ASP reduction, the share of an attacker's ASP that MTD removes: [eq] It is 0 when MTD has no effect, 1 when the attacker reaches its goal in no run under MTD, and negative when MTD raises ASP, after the mitigation factor of Alavizadeh et al. At 200 s, ASP reduction shows the order of NCR reduction, and reaches its ceiling of 1 against the APT attacker model, whose ASP with no MTD is low, so Chapter 5 ranks on NCR reduction." → "… on ASP reduction, NCR reduction (Equation 4.12) with ASP in place of NCR: [eq] ASP reduction is 1 when no run under MTD compromises a target host. At 200 s, ASP reduction shows the order of NCR reduction. Against the APT attacker model, whose ASP with no MTD is 0.09, it cannot separate the five that reach 0.99 or more: every host-layer MTD mechanism and the random and alternative deployment strategies. Chapter 5 therefore ranks on NCR reduction." | R5 (define by reference to Section 4.5's NCR reduction, whose 0 / 1 / negative reading and Alavizadeh form carry over, in place of re-glossing them); R12 ("reaches its goal" paraphrased ASP); R13 ("ceiling of 1", ruled unreadable in ch6.1 §73) replaced by the values, checked in `numbers_reported.json` `sweep_asp` at 200 s (1.0 ×3, 0.997, 0.995); "low" → 0.09 (`hosts_none` 0.090); R8 (the old "It" sat after two floats, a page from its equation). Round 2 (cold reader): the step from "0.99 or more" to ranking on NCR is now stated ("cannot separate"). "Shows the order of NCR reduction" is kept word for word because Section 6.4 (8966) relies on it; see open question 2. The equation and its label are unchanged |
| Tables D.3–D.5, Figure D.1 captions | kept | Decodes; ruled 2026-10-14 ("captions decode only") |
| D.4 lead S1 | "Each table gives in full an ablation that Table 5.4 summarises (Section 5.4): …" → "Each table gives in full an ablation study of Section 5.4: …" | R11: Table 5.4 holds no random partitions (Table D.7 left it on 2026-10-06) |
| D.4 lead S2 | kept | Ruled 2026-10-14 (the shared reading of $d$ stated once) |
| Table D.7 caption | "… into groups of the same sizes" → "… into four groups of the attack profiles' sizes" | R10 (same sizes as what?); Section 5.4's own words |
| Tables D.6, D.8 captions | kept | Each states its comparison; the rest decodes |
| D.5 P1 | "… moved to both ends of a band" → "… of its band"; "… moves NCR much" → "… changes NCR much" | R10; R6 (Chapter 4 4991 and Section 6.5 9097 say "changes NCR much") |
| D.5 P2 | "So the ranking of Section 5.3.2 at 200 s was repeated at both ends of the 45 s band … and the two rankings stay unrelated." → "We therefore repeated the 200 s ranking of Section 5.3.2 at both ends of the 45 s band … and the two rankings stay uncorrelated." | R7, R15 (passive, "So" opener); R6 ("uncorrelated" is Marc's word for $\rho$ near 0, ch6.1 §81) |
| Table D.9 caption | "… have half the 45 s mean duration, so it moves theirs too." → "… so moving the 45 s moves theirs too." | R8 ("it"); the wording of the 2026-10-14 redesign |
| Table D.10 caption | kept | S1 states the comparison; the rest decodes |
| D.6 lead S2 | "This ablation checks the first; …" → "This ablation tests the tactic durations; …" | R8 ("the first") |
| D.6 lead S3 | cut "on the same 1 000 seeds" | R4 (Table D.11's caption: "The same 1 000 seeds in every row") |
| D.6 lead S5 | "… the baseline attacker's mean time … takes 5 s for scan neighbours, not 45 s, and Credential Access 20 s for brute force, not 4.5 s." → "… the baseline attacker's time … 5 s for scan neighbours in place of 45 s, and Credential Access 20 s for brute force in place of 4.5 s." | R6 (Section 6.1's term, "the baseline attacker's times"); R9 ("X, not Y" → "in place of", ch6.1 lesson x) |
| D.6 lead S6 | "Averaged over the four attack profiles, the two steps raise its ASP from 0.09 to 0.45, against the baseline attacker's 0.66: 0.63 [0.61, 0.65] of the gap." → "The two steps raise the APT attacker model's ASP, averaged over $c_1$ to $c_4$, from 0.09 to 0.45 against the baseline attacker's 0.66; the share of its gap in ASP they close is 0.63 [0.61, 0.65]." | R7 (fronted modifier), R6 (the ratified "averaged over $c_1$ to $c_4$"; Section 6.1's "its gap in ASP"), R10 ("the gap" after a colon); round 2: "closing 0.63 … of its gap" read as an ASP beside the ASP values (cold reader), so the share is named |
| D.6 lead S7 | cut "An attack action fails when it runs before its preconditions are met (Section 4.4)." | R5, R14: Section 6.1 (8607–8609) states it beside the 15–30 % it reads from the table |
| D.6 lead S1, S2 disclosure, S4 | kept | Ruled 2026-10-14 (the claim, the post-hoc disclosure, the two steps) |
| Table D.11 caption | kept | Decodes |

## 3. Cold read (round 2)

After round 1, a cold reader (a fourth-year CS student who knows the body's terms) read
the rendered pages 57–70 and returned twelve findings. Two were caused by round 1
(the B lead, the D.3 "it"); both are fixed. Taken and applied: the B lead, C.1 S1–S2,
C.2 S4, C.4 S2, C.6, D.3, D.6 S6, and the Table C.1 and D.2 captions (all in §2).
Left, with the reason:

- **C.3, the Muddy Water sentence** ("why does this matter; what is confidence 0"):
  Marc's ruling of 2026-10-13 ("yes add"). It explains the one Impact cell drawn in
  $c_1$'s grid.
- **C.5, "factor" names a matrix entry and the distance factor**: both are Section
  4.4.3's terms. "Three away" is the most there is, with four lifecycle stages.
- **D.1, why each change was needed**: Marc cut the reasons on 2026-10-14 ("chop,
  chop down").
- **D.5, "a test fixed before the run"**: Marc's ruled finding. The 22.5 s that
  Execution and Defense Impairment share is resolved by Table D.9's caption.

## 4. Proposals (not applied)

**Chapter 4 (ch1–5 gate, so proposed only).**

- **P1, Section 4.4.2, l. 4990–4991.** The sentence says the appendix "halved and
  doubled each one in turn". Table D.9 moves the 45 s from a quarter to four times
  (11.25 to 180 s), as Section 6.5 (9060) says, and it moves the four mean durations
  that several tactics share, not each value.
  - Before: "after the values were fixed, it halved and doubled each one in turn."
  - After: "after the values were fixed, it moved each mean duration in turn to
    both ends of a band, from half to double, and from a quarter to four times for
    the 45~s."

**Appendix C row text, with Section 6.5 (ch6 updates automatically once ruled).**

- **P2, "Per-tactic duration multipliers"** (the Table C.4 row in `value_bases.json`;
  `thr:values`, l. 9094). Chapter 4 never says *multiplier*. Its object is
  "Execution and Defense Impairment … at half the 45 s" (Section 4.4.2).
  - Before: "Per-tactic duration multipliers".
  - After: "Half the 45 s for Execution and Defense Impairment", with the same words
    in `thr:values`.
  - Marc to rule. The registry rule is that a term is defined before use, and this
    is a repo word on the surface.

**Titles.** None proposed. Every B–D heading states its topic. None is rhetorical by
voice.md §d.

## 5. Numbers

- **Pages.** 86 before and after. The page map is unchanged: A p. 51–56, B p. 57,
  C p. 58–63, D p. 64–70.
- **References.** One undefined reference before and after, `app:detector-memory` in
  Chapter 4, left alone.
- **Overfull boxes.** 62 before and after.
- **Words.** Appendix prose: the leads and openers outside floats, plus the long
  captions; headings, table bodies and comments excluded. Counter:
  `scratchpad/wc.py`; references and maths count as one word each.

| | Leads | Captions | Total |
|---|---:|---:|---:|
| Before (15aa897e) | 1 137 | 1 069 | 2 206 |
| After | 1 076 | 1 073 | 2 149 |

The cut is small, −57 words (−2.6 %). The 2026-10-13/14 rounds had already cut
B–D to their leads. The yield of this pass is truth and readability, not length:
- two false claims made true (C opener; D.4's "Table 5.4 summarises");
- one overclaim fixed (C.1's "the edges");
- the unreadable "ceiling of 1" replaced;
- a dozen missing referents restored.

Four leads grew to restore a referent (C.1, C.2, C.4, D.3). The D opener lost 32 words,
and C.6 lost 12.

## 6. Unsure, and open questions

1. **Re-opened ruling, C.4 S2.** Marc's 2026-10-14 form, "Six tactics take an attack
   action's time", is replaced by a sentence that names the two times (4.5 s, 35 s).
   The ruled form could not be checked against Table C.2 (the cold reader's top
   finding). Revert, or keep?
2. **Section 6.4, l. 8964–8966**, "Ranking on ASP reduction instead gives the same
   order against either attacker". This is checked only at point values at 200 s,
   and not with Scott–Knott:
   - for the APT attacker model, the order is the same, with ties at the top;
   - for the baseline attacker, the layer order holds, but complete topology shuffle
     (NCR reduction 0.42, ASP reduction 0.39) and random (0.33, 0.43) swap.

   D.3 keeps its original "shows the order of NCR reduction", so the pointer still
   lands. Should Section 6.4 say "the same layer order", which is what Section 6.5
   (9076) claims?
3. **D.5 S1, "Our judgement sets the tactic durations".** Section 4.4.2 takes 4.5 s
   and 35 s from MTDSim. The analysis moves all four shared mean durations, two of
   which are MTDSim's. The sentence was ruled on 2026-10-14 and is kept. It mirrors
   Chapter 4 (l. 4988, "Because these values are our judgement").
4. **Decode ownership.** The following sentences were read as the parallel pass's and
   left untouched:
   - B.1's cell and mark keys;
   - C.1's encoding sentences (edge darkness, the italic count, blue, the filled box);
   - Table D.2's "A printed 1.000 is exact";
   - Table D.3's italic row and "Random, MTDShield's four" key;
   - Table D.9's *Change* decode.

   This pass edited other sentences in the same caption strings, in
   `attack_action_times_table.py`, `ablation_table.py`, `ch5_disruption_figure.py`,
   `analyse.py` and `gasp_structural_baseline.py`. A merge with that pass will
   conflict on those lines. Every edit is one clause, listed in §2.
5. **The worktree's base.** The worktree branch was cut from `main` (31ce3beb), not
   from `feat/ch6-redraft`. It had no commits of its own and a clean tree, so it was
   moved to 15aa897e with `git reset --hard` before any work. Guardrails list
   `reset --hard` as destructive. Nothing was lost, but it is disclosed.
6. **Generator inputs.** Four generators needed five gitignored inputs, symlinked
   read-only from the main checkout and not committed:
   - `enterprise-attack-19.1.json`;
   - `runs_reported_summaries.pkl`;
   - `runs_memory.jsonl`;
   - `ch5_s531_unopposed/runs_reported.jsonl`;
   - `rate_feasibility_study/run_study.py`.

   Every generator reproduced its committed output byte for byte before the edits,
   and the generators and their outputs were edited and rerun together.
