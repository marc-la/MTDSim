# Clausing check: the ruling file

This file gives every proposal from the final register pass, in five clusters. It was generated on 2026-10-18 from `data/clausing_check/clusters/`, under the standard in `docs/workflows/clausing_check.md`.

**How to rule.**
1. Read each cluster's **Rule** and its **cluster-wide move**, and rule the move once.
2. Then mark each item **ok**, **alt**, **keep** or **look**. An unmarked item takes the cluster-wide ruling.
3. The kept rows are listed with their warrants, so you can overrule a keep as well.

**Before you start.** Your 19 calibration items are in `docs/handoffs/2026-10-18_final_register_pass.md` and are not repeated here.

| Cluster | Name | Kept | Proposed |
|---|---|---|---|
| F | Captions and headings | 57 | 37 |
| C | Colons | 82 | 48 |
| A1 | Comma jobs, chapters 1–4 | 41 | 24 |
| A2 | Comma jobs, chapters 5–7 and appendices | 49 | 20 |
| D | Words | 44 | 7 (D.7 merged into C.28) |

**Three items need you, not a style rule** (now §0 below).
- **A2.14 (L9845, chapter 7), a factual overclaim.** "maps each tactic onto one of the baseline attacker's six attack actions" is wrong, because the unmapped tactics run no attack action (§4.4.1, L4938). The fix is folded into the comma edit. It is the one item here that changes a claim.
- **F.7 overturns a ratified ruling:** round 3's "the caption says what to look at". The item names it.
- ***Step* has three senses in chapter 4:** a step drawn in an attack flow, a numbered step of the loop in Figure 4.4, and the step of the behaviour metrics. Renaming one touches a figure and chapter 5, so it is left as a question, not a proposal: should the senses be split?

## 0. First: the factual fix and the three senses of *step*

**F.7. Ruled ok (Marc, 2026-10-18).** The figure should show it visually. Where it cannot, the caption says it clearly.

### 0.1 · A2.14 · L9845 · §7.1. Restoring the fact

> In MTDSim, the APT attacker model uses a Petri net to choose its next tactic at runtime, and maps each tactic onto one of the baseline attacker's six attack actions, none of which models actions on objectives.

| | After | Δ |
|---|---|---|
| (a) fact only | …at runtime, and maps eight of the 15 tactics onto the baseline attacker's six attack actions, none of which models actions on objectives. | +3 |
| (b) fact plus split | …at runtime. It maps eight of the 15 tactics onto the baseline attacker's six attack actions, none of which models actions on objectives. | +2 |

- "Eight of the 15 tactics" is §6.4's wording verbatim (L8979), so chapters 6 and 7 then agree.
- (a) changes only the false words. (b) also splits a two-idea sentence.
- **Recommended: (a).** It is the minimal fix, and A2's comma concern is secondary here.

**Mark:** a / b / look —

### 0.2 *Step*: three senses, split two ways

The three senses are:
1. **a step drawn in an attack flow** (one technique after another, L438–445, L4038–4078, L9397–9516). **Keep *step*.**
2. **a numbered part of the loop in Figure 4.4** (caption L4635, L4643, and the refs at L4893, L4965, L5118, L5292);
3. **the unit the behaviour metrics count** (definition L5434–5437, the relative tactic occurrence equation (`eq:rto`), L5446–5494, chapter 5 at L6807–6831 and L8680, and the axis label "First *k* steps" in `tools/ch5_unopposed_figures.py:300`).

The figure prints only numbered badges with one-word labels. It never prints "step", so sense 2 is prose-only.

**Sense 2, the loop.**

| Option | Form | Pros | Cons |
|---|---|---|---|
| **(a) no noun; cite the number** | "(2 in Figure 4.4)" | no term at all; the figure's numbers are the labels; −1 word per reference; removes a K2 tail at L4965 and L5118 | an unusual reference form at first sight |
| (b) *part* | "at part 2 of Figure 4.4" | one plain noun | vague, and a new word to carry |
| (c) *stage* | — | — | **collides** with the failure matrix's lifecycle stages (L5184, L10302) and Kim's four stages |

**Recommended: (a).** The edits:
- **L4635 caption:** "…numbered by step." becomes "…numbered in order." (0)
- **L4643:** "One iteration of the loop runs in six steps, numbered as in Figure 4.4:" becomes "One iteration of the loop runs as follows, numbered as in Figure 4.4:" (−1). The list itself shows the six.
- **L4893:** "…attack actions at step 2 of Figure 4.4." becomes "…attack actions (2 in Figure 4.4)." (−2)
- **L4965:** "…how long each tactic takes, at step 3 of Figure 4.4." becomes "…how long each tactic takes (3 in Figure 4.4)." (−2)
- **L5118:** "…after an attack action fails, at step 5 of Figure 4.4." becomes "…after an attack action fails (5 in Figure 4.4)." (−2)
- **L5292:** "(step 3 of Figure 4.4)" becomes "(3 in Figure 4.4)." (−1)

**Sense 3, the metrics' unit.**

| Option | Pros | Cons |
|---|---|---|
| **(a) *turn*** ("A *turn* is one tactic the token enters…"; "first *k* turns"; "947 distinct openings over eight turns") | plain English; no collision as a noun; sits with *opening*, which is already a game term; clearly not a drawn step | about 16 prose edits plus one axis label and a figure re-render; "turns" is a verb at L4893 ("turns the token's tactic into") |
| (b) keep *step* for the metrics; call sense 1 a *drawn step* | no edit to chapter 5 or the figure | you keep a word you found rhetorical; senses 1 and 3 differ in resolution (technique against tactic), which is the risk |
| (c) no unit noun ("the tactics the token enters") | no term | "openings over eight tactics" reads as eight *different* tactics, which is wrong |

**Recommended: (a) *turn*.** It is the only option that separates the senses without ambiguity, and it costs 0 words: each edit swaps one word for one word. The L4893 verb becomes "maps the token's tactic onto" (0), so *turn* is never both a noun and a verb.
- *Move* was considered and rejected. It collides with MTD's "when to move" and with the failure matrix's "a move to another tactic".

**Mark:** sense 2 a / b / look — sense 3 a / b / c / look —

---

**Calibration item 5 correction.** Cluster F found that Table D.2 also holds attack actions blocked, so the proposed D.2 title "Values of time lost per MTD deployment" undersells the table. See F's note.

**What a full accept does.** About 44 colons go, which brings the rate from 7.9 to about 5.3 per 1 000 words against the field's 5.0. Every cluster is net zero or negative in words except C, at +2.

---

## F. Captions and headings

**Rule.** Captions "should be informative" and "fully describe the figure's major elements" (Zobel pp. 176–177; Rougier et al. 2014 rule 4; *Nature*: a brief title, then each panel). The first sentence names what the float shows in the body's terms, and the later sentences decode and nothing else (figure_table_conventions §b2). Headings are "concise and informative, have specific rather than general terms", and siblings are parallel (Zobel pp. 95–96, p. 196).

**The cluster-wide move.** Ten chapter 5 and Appendix D captions end their first sentence on "; the APT attacker model averaged over c1 to c4", which is a semicolon hinge carrying an appended absolute phrase (K1 and K2).
- (a) Make it its own sentence in every caption: "The APT attacker model is averaged over c1 to c4." Pro: plain, identical everywhere, and the stress falls back on the float's subject. Con: +1 word per caption, about +10 in all.
- (b) State it once in §5.1 *Runs* and cut it from the captions. Pro: about −70 words. Con: a caption no longer reads alone (§b2), and the appendix floats sit 30 pages from §5.1.
- (c) Keep it. Pro: zero cost, and a formula the reader learns once. Con: the hinge repeats ten times in the unit where the census puts the colon and K2 rates highest.

**Recommended:** (a). It keeps every caption readable alone for one word each. Items F.11–F.13, F.26–F.29, F.31 and F.37 apply it.

**Sibling sets checked.** Chapters 1–7 and Appendices A–D are parallel noun phrases. §2.2.1–3 name MTDSim's three modules. §3.1.1–3 hold. §3.2.1–3 do not (F.2). §3.3.1–2 are parallel once ledger item 1 is applied. §4.1–4.5, §4.4.1–4, §4.5.1–3, §5.2–5.3 and §6.1–6.3 are parallel, with ledger item 2 applied. §5.3.1–3 are parallel in form, but §5.3.1 names no metric (F.10). In the §5.4 run-ins, one of three is not a component name (F.16). The run-in labels of §3.3.2, §4.5, §5.1 and §6.5 hold under the voice §d carve-out. The ledger's C and D sets give the form used here: one noun phrase naming the object, with no leading article.

**Kept as warranted (57: 55 worklist rows, plus L7709 and L8182).**

- `L1873`: Figure 3.2. The node labels decode, and one clause names the float.
- `L3718`: Figure 4.1. Names the float and decodes blue.
- `L4222`: Table 4.1. The column headers decode.
- `L4268`: Figure 4.3. In the body's terms, with the legend in the figure.
- `L4633`: Figure 4.5. "Numbered by step" decodes the numbers, and a fix gains nothing.
- `tables/tab_4-4a_dwell_catalogue:8`: Table 4.2. The phrase after the comma is the second column, not a nuance.
- `tables/tab_4-5a_metrics:229`: Table 4.3. One noun phrase.
- `tables/tab_5-1a_experiment:67`: Table 5.1. Ratified in round 12, and the wording is plain.
- `tables/tab_5-2-1a_unopposed_summary:11`: Table 5.2. A key colon, and the cells read "(124 runs)".
- `L160`: Owed before submission. A front-matter list, gone before submission.
- `L258, L676, L1045, L3626, L5655, L8538, L9779`: chapter titles. One noun phrase each, parallel.
- `L709, L741`: §2.1–2.2. The body's terms.
- `L776, L831, L928`: §2.2.1–3. Name Figure 2.1's three modules.
- `L1187, L1979, L2847, L3514`: §3.1–3.4. Noun phrases naming the topic.
- `L1228, L1564`: §3.1.1, §3.1.3. Defined terms.
- `L1415`: §3.1.2. A proper name, so the acronym rule does not apply.
- `L2066`: §3.2.1. The body's term "MTD modelling approach".
- `L3168`: §3.3.2. The ledger's reference term.
- `L3973, L4119, L4305, L4540, L5318`: §4.1–4.5. Parallel noun phrases in the body's terms.
- `L4862, L4944, L5063, L5240`: §4.4.1–4. The component names.
- `L5371, L5517, L5578`: §4.5.1–3. The metric-group names.
- `L6115, L6581, L7294`: §5.1–5.3. Parallel with §6.1–6.2.
- `L7709`: §5.3.2 (not on the worklist). "Rankings" is the body's word, as in ledger D.3.
- `L7963`: §5.3.3. "MTD effectiveness" is §4.5.3's term.
- `L8182`: §5.4 (not on the worklist). The body's term.
- `L8589, L8731, L9002, L9126`: §6.1, 6.2, 6.4, 6.5. Noun phrases, parallel.
- `L9817, L9885`: §7.1–7.2. Conventional.
- `L10176, L10348`: Appendices C and D. A parallel pair, each naming the chapter it supports.

**Proposals (37).** The worklist missed Table 3.2 (L3075), Table 3.3 (L3381) and Figure C.1 (L10205), because the census drops a caption whose short form spans lines. They are read and included here. Short captions no longer print, so short-caption ripples are noted inside items at no cost.

### F.1 · L934 · §2.2.3 Figure 2.3 · K5
> The six attack actions of the baseline attacker and the moves between them. A dashed arrow marks the attack action each kind of deployment sends the attacker back to.

**After:** The six attack actions of the baseline attacker and the moves between them. A dashed arrow marks the attack action a deployment sends the attacker to.
Δ −3 · "Each kind of" compresses what the arrow labels already name. "Back" is wrong for a user shuffle, which sends the attacker on to exploit (§2.2.3).
**Mark:** ok / alt / keep / look —

### F.2 · L2238, L2562 · §3.2.2–3.2.3 headings · K5
> MTD modelling approaches / Metrics / Evaluation methods

**After:** MTD modelling approaches / MTD metrics / MTD evaluation methods
Δ +2 · A bare "Metrics" is the unqualified head noun of ledger item 2. The body defines "An MTD metric" and "An MTD evaluation method". It also separates §3.2.2 from §4.5's "Evaluation metrics". Alt: change only "MTD metrics" (+1).
**Mark:** ok / alt / keep / look —

### F.3 · L2534 · §3.2.2 Table 3.1 · K2
> MTD metrics as Cho et al. classify them [cho2020], with examples from the works surveyed.

**After:** MTD metrics from the works surveyed and their class in Cho et al. [cho2020].
Δ −1 · The phrase appended after the comma was the table's content, so it becomes the head. This is the shape of ledger item 9. Short-caption ripple: `MTD metrics from the works surveyed`.
**Mark:** ok / alt / keep / look —

### F.4 · L3075 · §3.3.1 Table 3.2 · K5, K2 (ripple of ledger item 1)
> The eight properties an MTD attacker model needs to model an APT attacker, and their sources.

**After:** The eight properties of an APT attacker and their sources.
Δ −6 · Mirrors ledger item 1's heading. The ledger changed only the short caption. Apply only if item 1 is ruled ok.
**Mark:** ok / alt / keep / look —

### F.5 · L3381 · §3.3.2 Table 3.3 · K1
> Three MTD attacker models from 2023 to 2026, scored by this dissertation on the eight properties of Table 3.2: ● has the property, ◐ has it in part, ○ does not have it.

**After:** Three MTD attacker models from 2023 to 2026, scored by this dissertation on the eight properties of Table 3.2. ● has the property, ◐ has it in part, ○ does not have it.
Δ 0 · The colon becomes a full stop, so the key is a sentence of its own, as in Table 6.1.
**Mark:** ok / alt / keep / look —

### F.6 · L4072 · §4.1 Figure 4.2 · K5
> Part of two attack flows aggregated into the attack graph.

**After:** Part of two attack flows aggregated into the attack graph. A number on an edge counts the attack flows that draw it.
Δ +11 · The edge numbers 2 and 1 are not decoded (§b2). The wording is Figure C.1's and §4.1's. Short-caption ripple: "How attack flows are aggregated…" is not a noun phrase, so `Part of two attack flows aggregated into the attack graph`. Alt: keep, because the sentence above the float defines the weight.
**Mark:** ok / alt / keep / look —

### F.7 · L4481 · §4.3 Figure 4.4 · K8, K1, K3
> One tactic of a Petri net. (a) The construction for one tactic p, with the legend for every mark. (b) Initial Access in c1: each successor q with its base weight W(t_pq) and, in blue, its weight after a failure, W(t_pq | failure) (Equations 4.2 and 4.4). After a failure, most of the weight moves to Reconnaissance.

**After:** One tactic of a Petri net. (a) The construction for one tactic p. (b) Each successor q of Initial Access in c1 with its base weight W(t_pq) and, in blue, its weight after a failure W(t_pq | failure) (Equations 4.2 and 4.4).
Δ −14 · "With the legend for every mark" tells the reader the legend exists. The colon and the comma before the symbol go. The last sentence is a finding, which §4.4.3 l.5197 states. This overturns round 3 ("the caption says what to look at"), because a caption only decodes. Alt: keep the last sentence (−5).
**Mark:** ok / alt / keep / look —

### F.8 · L4918 · §4.4.1 Figure 4.6 · K2
> The tactic-to-action mapping, with the tactics grouped by the four lifecycle stages of Section 3.1.1.

**After:** The tactic-to-action mapping. The tactics are grouped by the four lifecycle stages of Section 3.1.1.
Δ 0 · Splits the appended phrase into its own sentence. Alt: `The tactic-to-action mapping.` (−12), since the figure's column is labelled "lifecycle stage".
**Mark:** ok / alt / keep / look —

### F.9 · L6653 · §5.2 Figure 5.1 · K5
> How each attacker acts with no MTD running (Section 4.5.1). (a) Left: the attack action each tactic runs (Section 4.4.1); the baseline attacker's column is by attack action. Blank: a tactic the attack profile's attack flows do not reach (Figure 4.3); 0: a tactic they reach that no run takes. (b) 1: every run takes the same opening; 1 000: every run takes its own.

**After:** Relative tactic occurrence and distinct openings with no MTD running (Section 4.5.1). (a) Left: the attack action each tactic runs (Section 4.4.1). The baseline attacker's column counts attack actions. Blank: a tactic the attack profile's attack flows do not reach (Figure 4.3); 0: a tactic they reach that no run takes. (b) 1: every run has the same opening; 1 000: every run has its own.
Δ +1 · "How each attacker acts" names nothing a reader could point to. The metric names do, and they make the caption parallel with Table 5.2's. "Is by" is compressed. "Has the same opening" is §4.5.1's wording. Short-caption ripple: the same noun phrase.
**Mark:** ok / alt / keep / look —

### F.10 · L7405 · §5.3.1 heading · K5, K6 (not on the worklist)
> Disruption per MTD deployment

**After:** Attack actions blocked and time lost per MTD deployment
Δ +5 · Ledger D.2 calls "disruption" K6 drift, and no metric is named that. This is Figure 5.2's short caption, verbatim. **Flag on ledger D.2:** its *after*, "Values of time lost per MTD deployment", drops attack actions blocked, which Table D.2 also holds. Alt: keep both titles as they are.
**Mark:** ok / alt / keep / look —

### F.11 · L7612 · §5.3.1 Figure 5.2 · K1, K2 (cluster move)
> Attack actions blocked and time lost per MTD deployment for each MTD mechanism, at a deployment interval of 2 000 s; the APT attacker model averaged over c1 to c4. Table D.2 gives each bar's value with its confidence interval.

**After:** Attack actions blocked and time lost per MTD deployment for each MTD mechanism, at a deployment interval of 2 000 s. The APT attacker model is averaged over c1 to c4. Table D.2 gives each bar's value with its confidence interval.
Δ +1 · Cluster move (a).
**Mark:** ok / alt / keep / look —

### F.12 · L7875 · §5.3.2 Figure 5.3 · K1, K2 (cluster move)
> NCR reduction against the deployment interval; the APT attacker model averaged over c1 to c4. Host layer and service layer: …

**After:** NCR reduction against the deployment interval. The APT attacker model is averaged over c1 to c4. Host layer and service layer: …
Δ +1 · Cluster move (a). The rest stays.
**Mark:** ok / alt / keep / look —

### F.13 · tables/tab_5-3-2d_attacker_ranking:15 · §5.3.2 Table 5.3 · K1, K2 (cluster move)
> The MTD mechanisms and deployment strategies ranked by NCR reduction against each attacker, at a deployment interval of 200 s; the APT attacker model averaged over c1 to c4. Bold: rank 1.

**After:** The MTD mechanisms and deployment strategies ranked by NCR reduction against each attacker, at a deployment interval of 200 s. The APT attacker model is averaged over c1 to c4. Bold: rank 1.
Δ +1 · Cluster move (a). Generator: `tools/ch5_sweep_figures.py`.
**Mark:** ok / alt / keep / look —

### F.14 · L8006 · §5.3.3 Figure 5.4 · K2
> NCR reduction against the deployment interval, for each attack profile and the baseline attacker. Where no whisker shows, the confidence interval is narrower than the marker. Table D.3 gives each point's value for the baseline attacker, and averaged over c1 to c4 for the APT attacker model.

**After:** NCR reduction against the deployment interval for each attack profile and the baseline attacker. Where no whisker shows, the confidence interval is narrower than the marker. Table D.3 gives each point's value for the baseline attacker and the mean over c1 to c4 for the APT attacker model.
Δ 0 · Two commas go. The appended ", and averaged over…" made the reader supply "each point's value" a second time.
**Mark:** ok / alt / keep / look —

### F.15 · tables/tab_5-4a_ablation:7 · §5.4 Table 5.4 · K5
> The APT attacker model with and without each component, averaged over c1 to c4. Bold: not negligible (Section 5.1).

**After:** The APT attacker model with and without each component, averaged over c1 to c4. d on NCR is with minus without. Parentheses give its 95 % interval. Bold: not negligible (Section 5.1).
Δ +11 · The sign of d and the bracketed interval are not decoded (§b2), and the reader cannot read "−0.28" without them. The wording is Table D.10's. Generator: `data/results/ch5_defended/ablation_table.py`.
**Mark:** ok / alt / keep / look —

### F.16 · L8231 · §5.4 run-in label · K5 (not on the worklist)
> Attack profiles by objective.

**After:** Attack profiles.
Δ −2 · Its siblings, "Failure matrix." and "Vulnerability memory.", name components, as §5.4's lead does ("the attack profiles, the failure matrix and the vulnerability memory"). Ripple: Table 5.4's group row in the generator.
**Mark:** ok / alt / keep / look —

### F.17 · L8904 · §6.3 Table 6.1 · K4
> … Appendix B gives the predicates behind each mark.

**After:** … Appendix B derives each mark from its predicates.
Δ 0 · "Behind" is the vague preposition of ledger C.2. Appendix B's own rule is that the mark follows from the cells. The rest of the caption is kept, because the numbered list decodes the abbreviated column heads. Ripple: Appendix B's lead uses the same phrase (prose cluster).
**Mark:** ok / alt / keep / look —

### F.18 · L10118 · Appendix B Table B.1 · K5 (ripple of ledger item 3)
> Each attacker model tested on each predicate of Table 3.2. …

**After:** Each MTD attacker model tested on each predicate of Table 3.2. …
Δ +1 · Matches ledger item 3's title. Apply only if item 3 is ruled ok. The rest is a decode list and is kept.
**Mark:** ok / alt / keep / look —

### F.19 · L10205 · Appendix C.1 Figure C.1 · K1, K2 (not on the worklist)
> The attack graph with techniques as nodes, with only the edges drawn by two or more of the 38 attack flows, and only the connected groups of three or more techniques those edges form: 35 of its 124 techniques and 55 of its 478 edges. Techniques are grouped by tactic, in ATT&CK's order, and labelled by identifier; each group gives its tactic and, in italic, how many of its techniques are drawn. Darker, thicker edges are drawn by more attack flows, and a number on an edge counts them where more than two did; blue edges run back to an earlier tactic. A filled box is a technique some attack flow starts at.

**After:** The attack graph with techniques as nodes, limited to the edges drawn by two or more of the 38 attack flows and the connected groups of three or more techniques those edges form. The figure keeps 35 of its 124 techniques and 55 of its 478 edges. Techniques are grouped by tactic, in ATT&CK's order, and labelled by identifier. Each group gives its tactic and, in italic, how many of its techniques are drawn. Darker, thicker edges are drawn by more attack flows, and a number on an edge counts them where more than two did. Blue edges run back to an earlier tactic. A filled box is a technique some attack flow starts at.
Δ 0 · The colon and two semicolons become full stops, and one comma goes. Short-caption ripple: ledger C.1's title.
**Mark:** ok / alt / keep / look —

### F.20 · tables/tab_B-2a_objective_classification_audit:12 · Appendix C.2 Table C.1 · K2
> … The CTID description of every attack flow was read [ctid2025attackflow], with the analyst's notes on its steps where needed; the columns give what else was read, and a blank row needed nothing else. …

**After:** … We read the CTID description of every attack flow [ctid2025attackflow] and the analyst's notes on its steps where needed. The columns give what else we read, and a blank row needed nothing else. …
Δ 0 · The appended "with…" phrase and the semicolon go. "We" is licensed (chapter 4's appendix) and is §4.2's wording ("We answered both questions…"). Short-caption ripple: ledger C.2's title. Generator: `tools/gasp_structural_baseline.py`.
**Mark:** ok / alt / keep / look —

### F.21 · L10258 · Appendix C.3 Figure C.2 · K1, K2
> Edges of the four attack profiles: each cell is an edge from the tactic of its row to the tactic of its column, darker where more of the attack profile's attack flows draw it. …

**After:** Edges of the four attack profiles. Each cell is an edge from the tactic of its row to the tactic of its column. Darker cells are drawn by more of the attack profile's attack flows. …
Δ +1 · The colon hinge and the appended decode each become a sentence. The rest is kept.
**Mark:** ok / alt / keep / look —

### F.22 · tables/tab_B-4b_attack_action_times:8 · Appendix C.4 Table C.2 · K2, K1
> Each tactic, in ATT&CK's order, with the attack action it runs (Figure 4.6), that attack action's time in MTDSim [tay2024code], which the baseline attacker takes, and the tactic's mean duration, which the APT attacker model takes instead. The exploit's time is its mean: it takes 0 to 9 s, by the vulnerability.

**After:** Each tactic in ATT&CK's order with the attack action it runs (Figure 4.6), that attack action's time in MTDSim [tay2024code] and the tactic's mean duration. The baseline attacker takes MTDSim's time, and the APT attacker model takes the mean duration instead. An exploit takes 0 to 9 s by the vulnerability. The exploit's time is its mean.
Δ +3 · Seven commas and two "which" clauses go down to two commas. The colon and the tail ", by the vulnerability" (ledger item 12's shape) go. Generator: `tools/attack_action_times_table.py`.
**Mark:** ok / alt / keep / look —

### F.23 · tables/tab_B-6a_outcome_overlay_weights:8 · Appendix C.5 Table C.3 · K3
> … After a tactic's attack action fails, the first rule that applies to a candidate next tactic, from A down, gives its value. …

**After:** … After a tactic's attack action fails, the first rule from A down that applies to a candidate next tactic gives its value. …
Δ 0 · The interrupting phrase moves next to its noun, and two commas go. Generator: `tools/failure_weight_decomposition_figure.py`.
**Mark:** ok / alt / keep / look —

### F.24 · tables/tab_C-0b_value_bases:5 · Appendix C.6 Table C.4 · K4, K2
> Every value the APT attacker model needs, grouped by where it comes from, with the section that gives its reason.

**After:** The source of every value the APT attacker model needs and the section that gives its reason.
Δ −3 · "Where it comes from" is the narrative form of "source" (ledger C.6), and the first column shows the grouping. Ripple: the column header `Comes from` becomes `Source` (−1). Generator: `tools/value_bases_table.py`.
**Mark:** ok / alt / keep / look —

### F.25 · L10374 · Appendix D.1 Table D.1 · K2
> MTDShield's settings in training, from the release's training script [tay2024code], and as run in Chapter 5 (Table 5.1). In both, it chooses among complete topology shuffle, IP shuffle, OS diversity and service diversity, or nothing; it is told the attacker's current attack action at every decision; and a deployment is forced after 2 000 s without one.

**After:** MTDShield's settings in the release's training script [tay2024code] and as run in Chapter 5 (Table 5.1). In both, it chooses among complete topology shuffle, IP shuffle, OS diversity and service diversity, or nothing. It is told the attacker's current attack action at every decision. A deployment is forced after 2 000 s without one.
Δ −3 · The interrupting source phrase folds into the head. Two semicolons become full stops. Short-caption ripple: the colon in "MTDShield's settings: trained and run here" goes, giving `MTDShield's settings in training and in Chapter 5`.
**Mark:** ok / alt / keep / look —

### F.26 · tables/tab_5-3-1b_disruption:7 · Appendix D.2 Table D.2 · K1, K2
> The values of Figure 5.2, each with its 95 % confidence interval: attack actions blocked and time lost per MTD deployment at a deployment interval of 2 000 s, the APT attacker model averaged over c1 to c4. Time lost is over the MTD deployments made while the same seed's run with no MTD is still going, which are at least 78 % of each cell's MTD deployments. A printed 1.000 is exact.

**After:** Attack actions blocked and time lost per MTD deployment at a deployment interval of 2 000 s, each with its 95 % confidence interval (Figure 5.2). The APT attacker model is averaged over c1 to c4. Time lost is over the MTD deployments made while the same seed's run with no MTD is still going. These are at least 78 % of each cell's MTD deployments. A printed 1.000 is exact.
Δ −3 · The first sentence now names the metrics. The colon hinge, the cluster move and the "which" split are applied. Generator: `tools/ch5_disruption_figure.py`.
**Mark:** ok / alt / keep / look —

### F.27 · tables/tab_F-0a_interval_values:9 · Appendix D.3 Table D.3 · K1, K3
> NCR reduction for each MTD mechanism and deployment strategy against each attacker, at every deployment interval: the values of Figure 5.3, the APT attacker model averaged over c1 to c4. An italic row is a layer's mean, the line the figure plots. …

**After:** NCR reduction for each MTD mechanism and deployment strategy against each attacker at every deployment interval (Figure 5.3). The APT attacker model is averaged over c1 to c4. An italic row is the layer's mean the figure plots. …
Δ −4 · The colon hinge and the appositive go, and the cluster move is applied. The "Grey:" and "Random, MTDShield's four:" keys are kept. Generator: `tools/ch5_sweep_figures.py`.
**Mark:** ok / alt / keep / look —

### F.28 · tables/tab_F-0c_rank_one:5 · Appendix D.3 Table D.4 · K1, K8
> Rank 1 of Table 5.3 at every deployment interval: the MTD mechanisms and deployment strategies ranked first by NCR reduction against each attacker; the APT attacker model averaged over c1 to c4.

**After:** Rank 1 by NCR reduction (Table 5.3) against each attacker at every deployment interval. The APT attacker model is averaged over c1 to c4.
Δ −8 · The gloss after the colon restates "rank 1", which Table 5.3 defines. The cluster move is applied. Generator: `tools/ch5_sweep_figures.py`.
**Mark:** ok / alt / keep / look —

### F.29 · L10471 · Appendix D.3 Figure D.1 · K4, K2
> ASP reduction against the deployment interval, drawn as Figure 5.3 draws NCR reduction; the APT attacker model averaged over c1 to c4. A point at 1 may be a reduction above 0.99, which Table D.5 tells apart.

**After:** ASP reduction against the deployment interval, drawn as Figure 5.3 draws NCR reduction. The APT attacker model is averaged over c1 to c4. A point at 1 may be a reduction above 0.99. Table D.5 prints it as >0.99.
Δ +2 · "Tells apart" is an idiom. The appended "which" clause becomes a sentence in Table D.5's own wording. The cluster move is applied.
**Mark:** ok / alt / keep / look —

### F.30 · tables/tab_F-0d_interval_values_asp:4 · Appendix D.3 Table D.5 · K1
> ASP reduction, laid out as Table D.3: the values of Figure D.1. …

**After:** ASP reduction (Figure D.1), laid out as Table D.3. …
Δ −3 · The colon hinge goes. The paired semicolon in the last sentence is kept (voice §d). Generator: `tools/ch5_sweep_figures.py`.
**Mark:** ok / alt / keep / look —

### F.31 · tables/tab_C-1a_family_sensitivity:8 · Appendix D.4 Table D.6 · K1, K2
> NCR at the low end, the declared value and the high end of each mean duration's band (Table 4.2); the APT attacker model averaged over c1 to c4, 400 runs per cell. … Change: high end minus low end; bold, the largest. …

**After:** NCR at the low end, the declared value and the high end of each mean duration's band (Table 4.2). The APT attacker model is averaged over c1 to c4 with 400 runs per cell. … Change: high end minus low end. Bold: the largest. …
Δ +2 · Cluster move. The mixed semicolon and comma key becomes the house "Bold:" form. Generator: `data/results/ch5_s51_sensitivity/analyse.py`.
**Mark:** ok / alt / keep / look —

### F.32 · tables/tab_C-1b_duration_ranking:7 · Appendix D.4 Table D.7 · K1, K2
> The rank of each MTD mechanism … at the low and high ends of its band; the baseline attacker's ranks are Table 5.3's, and the APT attacker model is averaged over c1 to c4. Bold: rank 1, by Scott–Knott ESD. ρ: Spearman's rank correlation with the baseline attacker's NCR reductions; every 95 % interval lies within −0.27 and 0.05.

**After:** The rank of each MTD mechanism … at the low and high ends of its band. The baseline attacker's ranks are Table 5.3's, and the APT attacker model is averaged over c1 to c4. Bold: rank 1. ρ: Spearman's rank correlation with the baseline attacker's NCR reductions. Every 95 % interval of ρ lies between −0.27 and 0.05.
Δ −1 · Two semicolons become full stops. ", by Scott–Knott ESD" is an appended tail that §5.1 already states for every rank, and Table 5.3 omits it. "Within … and" becomes "between … and". Alt: keep the method (+2). Generator: `tools/duration_ranking_table.py`.
**Mark:** ok / alt / keep / look —

### F.33 · tables/tab_F-3_ablation_attack_profiles:5 · Appendix D.5 Table D.8 · K3
> d on NCR, the attack profiles minus the attack graph. Bold: not negligible. Negligible: service diversity at 1 000 and 2 000 s; MTDShield at every interval but 200 s; every other plain d is inconclusive.

**After:** d on NCR of the attack profiles minus the attack graph. Bold: not negligible. Negligible: service diversity at 1 000 and 2 000 s and MTDShield at every interval but 200 s. Every other plain d is inconclusive.
Δ +2 · The appositive goes. The last clause was not a "Negligible:" item, so it stands as its own sentence. Generator: `data/results/ch5_defended/partition_ablation.py`.
**Mark:** ok / alt / keep / look —

### F.34 · tables/tab_F-4_ablation_random_partitions:6 · Appendix D.5 Table D.9 · K3, K2
> d on NCR, the attack profiles minus each of 10 random partitions of the attack flows into four groups of the attack profiles' sizes, in falling order of d with no MTD. Bold: not negligible, in the random partition's favour. Negligible: partitions 3, 8, 9 and 10 under IP shuffle at 200 s; inconclusive: partition 9 under OS diversity at 200 s; every other d is not negligible (Section 5.1).

**After:** d on NCR of the attack profiles minus each of 10 random partitions of the attack flows into four groups of the attack profiles' sizes. Rows are in falling order of d with no MTD. Bold: not negligible, in the random partition's favour. Negligible: partitions 3, 8, 9 and 10 under IP shuffle at 200 s. Inconclusive: partition 9 under OS diversity at 200 s. Every other d is not negligible (Section 5.1).
Δ +3 · The appositive and the appended row-order tail go. Three keys joined by semicolons become sentences. Generator: `data/results/ch5_defended/ablation_table.py`.
**Mark:** ok / alt / keep / look —

### F.35 · tables/tab_F-2_ablation_memory:5 · Appendix D.5 Table D.10 · K1, K8
> The APT attacker model with and without the vulnerability memory, at every number of services per operating system: the share of exploits that succeed, NCR, and d on NCR, with minus without, with its 95 % interval. An exploit the host's operating system rules out is not counted.

**After:** The APT attacker model with and without the vulnerability memory at every number of services per operating system. d on NCR is with minus without. Parentheses give its 95 % interval. An exploit the host's operating system rules out is not counted.
Δ −6 · The list after the colon repeated the column headers ("Exploits that succeed", "NCR"). What stays decodes d and the brackets, in the same form as F.15. Generator: `data/results/ch5_defended/memory_ablation.py`.
**Mark:** ok / alt / keep / look —

### F.36 · tables/tab_FA-8_tactic_durations:7 · Appendix D.5.1 Table D.11 · K2
> … Bold: past the baseline attacker's value, the 95 % intervals apart (a higher ASP, NCR or attack rate, a lower attack confidentiality). …

**After:** … Bold: past the baseline attacker's value with the 95 % intervals apart (a higher ASP, NCR or attack rate, or a lower attack confidentiality). …
Δ +2 · The absolute phrase is attached to its condition. The "or" stops the two cases reading as one list. Generator: `tools/further_analyses_tables.py`.
**Mark:** ok / alt / keep / look —

### F.37 · tables/tab_FA-9_unmapped_mtd:7 · Appendix D.5.1 Table D.12 · K2 (cluster move)
> … The same 1 000 seeds in every row; the APT attacker model averaged over c1 to c4; ± the 95 % interval.

**After:** … The same 1 000 seeds in every row. The APT attacker model is averaged over c1 to c4. ±: the 95 % interval.
Δ +1 · Cluster move. The semicolon chain of fragments becomes sentences, with the house key form "±:". Generator: `tools/further_analyses_tables.py`.
**Mark:** ok / alt / keep / look —

**Cluster total.** About −7 words if every recommendation is taken (F.6 and F.15 add 22 words, all of it decoding).

---

## C. Colons

**Rule.** A colon's one major use is that what follows explains or elaborates what precedes it (Trask). Chicago 18th §6.65 limits it to "illustrating or amplifying", and Zobel p. 126 says colons "should not be overused" (field 5.0 per 1 000 words, dissertation 7.9). Stricter test applied here: a colon is warranted only when the clause before it *announces* what follows, by a count, by "the following", or by ending on a noun the colon unpacks (item 19). Evidence, a reason, an instance, a consequence or what a term means after a colon is a K1 hinge (item 18).

**The cluster-wide move.**
- (a) Split every hinge into two sentences. Pro: Δ ≈ 0, no new words or terms. Con: many short claim sentences; a few lose the explicit link (C.7, C.11 use *because* instead).
- (b) Rewrite the clause before the colon so it announces what follows. Pro: keeps one sentence. Con: adds words at the word-band ceiling, and only a few hinges have a natural count.
- (c) Keep hinges whose evidence is numeric. Pro: no edits. Con: that is most of the surplus.

**Recommended:** (a), with (b) or *because* only where a split leaves a fragment or loses the link.

**The §3.3.2 property walk** (L3409–L3488, 24 rows: one sentence per property, the mark and then its evidence).
- (a) Keep the colon run-ins as a declarative walk. Pro: voice §d licenses run-in labels in declarative passages; round 51 ruled "one sentence per property, its name first", so the reader meets each mark in Table 3.3's order. Con: about 23 colons stay, the main reason chapter 3 is above the field rate.
- (b) Recast each as one sentence with the evidence first and the mark last. Pro: removes about 23 colons at Δ ≈ 0, and the mark lands in the stress position. Con: it overturns round 51, and 23 sentences ending "so it has …" form a same-skeleton run (voice §d). Two examples:
  - L3409: "The baseline attacker has campaign persistence: it repeats its six attack actions host by host until it reaches its goal, and carries on through every disruption [brown2023]." → "The baseline attacker repeats its six attack actions host by host until it reaches its goal and carries on through every disruption, so it has campaign persistence [brown2023]." (Δ 0)
  - L3419: "It has no detection avoidance: it scans actively and does nothing to avoid an intrusion detection system (IDS)." → "It scans actively and does nothing to avoid an intrusion detection system (IDS), so it has no detection avoidance." (Δ 0)
- **Recommended:** (a). The walk is declarative scoring, and the name-first order is a ruling that (b) would have to overturn on merit. If the colon rate must fall further, (b) is the one lever that moves chapter 3.

**Kept as warranted (82).**

- `L336` — introduces the displayed research question
- `L398` — announced list or count
- `L594` — announced by "the following"
- `L696` — announced list or count
- `L698` — announced list or count
- `L714` — announced list or count of quoted questions
- `L755` — announced list or count
- `L834` — announced list or count
- `L836` — "one part" unpacked into the three parts
- `L942` — announced list or count
- `L977` — "visible subgraph" unpacked into its three parts
- `L1242` — "its objective" unpacked into the three objectives
- `L1285` — announced list or count
- `L1468` — announced list or count
- `L2198` — already calibration item 18; not repeated
- `L2673` — announced list or count
- `L2970` — announced list or count
- `L2973` — announced list or count
- `L3583` — calibration item 19, the reference case
- `L4205` — "each have an action" unpacked into the two actions
- `L4209` — count, then a quoted question
- `L4215` — "five attack flows" broken down by count
- `L4278` — "most common tactics" unpacked by name
- `L4384` — run-in label in a definition list
- `L4389` — run-in label in a definition list
- `L4401` — introduces an equation
- `L4411` — run-in label in a definition list
- `L4419` — announced list or count
- `L4451` — introduces an equation
- `L4578` — "the two in one loop" unpacked into both halves
- `L4694` — announced list or count
- `L4979` — announced list or count
- `L5360` — announced list or count
- `L5448` — introduces an equation
- `L5473` — introduces an equation
- `L5487` — introduces an equation
- `L5547` — introduces an equation
- `L5555` — introduces an equation
- `L5570` — introduces an equation
- `L5602` — introduces an equation
- `L5626` — introduces an equation
- `L5643` — introduces an equation
- `L5766` — announced list or count
- `L5775` — announced list or count
- `L6156` — announced list or count
- `L6236` — "95 % confidence interval" unpacked into its three methods
- `L8221` — announced list or count
- `L8308` — announced list or count
- `L8725` — announced list or count
- `L8965` — announced list or count
- `L8984` — "what the model adds" unpacked into its parts
- `L8996` — "what the attack actions do" unpacked
- `L9023` — announced list or count
- `L9112` — "what those attack actions do" unpacked
- `L9175` — announced list or count
- `L9193` — no prose colon; false flag from \hyperref
- `L10394` — announced list or count
- `L10448` — introduces an equation
- `L10459` — announced list or count ("the six")
- `L3409`–`L3488` (23 rows, all but L3481) — §3.3.2 property walk, kept as one unit; see the walk option block

**Proposals (48).**

### C.1 · L790 · 2.2.1 Network model · K1
> The network in MTDSim is a three-layer hierarchical attack representation model (HARM) [hongkim2012harm, brown2023]: a graph of hosts, in which each host runs services and each service carries vulnerabilities (Figure 2.2).

**After:** The network in MTDSim is a three-layer hierarchical attack representation model (HARM) [hongkim2012harm, brown2023]. It is a graph of hosts, in which each host runs services and each service carries vulnerabilities (Figure 2.2).
Δ +2 · K1: the colon says what the term means; a copula sentence carries it. Alt: keep, since the colon unpacks the noun it ends on.
**Mark:** ok / alt / keep / look —

### C.2 · L794 · 2.2.1 Network model · K1
> The host layer is the topology: the hosts are nodes, and an edge joins two hosts that can reach each other.

**After:** The host layer is the topology. Its hosts are nodes, and an edge joins two hosts that can reach each other.
Δ 0 · K1: what a term means; split.
**Mark:** ok / alt / keep / look —

### C.3 · L809 · 2.2.1 Network model · K1
> The exposed endpoints keep their address, software and accounts throughout: no MTD mechanism changes them, although a topology shuffle can change their links.

**After:** No MTD mechanism changes the address, software or accounts of the exposed endpoints, although a topology shuffle can change their links.
Δ −2 · K1: the colon joins a claim to its restatement; one clause says it. Alt: split (Δ 0).
**Mark:** ok / alt / keep / look —

### C.4 · L882 · 2.2.2 MTD mechanisms and deployment strategies · K1
> The deployment interval is the time between deployments: 200 s by default.

**After:** The deployment interval is the time between deployments and is 200 s by default.
Δ +2 · K1: the colon hinges a second fact onto the definition. A split would open on a second "It is" beside C.5's.
**Mark:** ok / alt / keep / look —

### C.5 · L884 · 2.2.2 MTD mechanisms and deployment strategies · K1
> It is near-periodic: each interval is the set value plus a random delay of 0.5 s on average.

**After:** It is near-periodic. Each interval is the set value plus a random delay of 0.5 s on average.
Δ 0 · K1: what a term means; split.
**Mark:** ok / alt / keep / look —

### C.6 · L1237 · 3.1.1 Advanced persistent threat · K1
> It is persistent: in the definition of the US National Institute of Standards and Technology (NIST), it pursues its objective repeatedly over an extended period and adapts to the defender's resistance [nist2011sp80039].

**After:** It is persistent. In the definition of the US National Institute of Standards and Technology (NIST), it pursues its objective repeatedly over an extended period and adapts to the defender's resistance [nist2011sp80039].
Δ 0 · K1: what a term means; split. A short sentence lands before the long one.
**Mark:** ok / alt / keep / look —

### C.7 · L1240 · 3.1.1 Advanced persistent threat · K1, K2
> It moves low and slow, trading speed for staying undetected [alshamrani2019]: espionage intrusions go undetected for a median of 122 days, against 14 days across all intrusions [mtrends2026].

**After:** It moves low and slow to avoid detection [alshamrani2019]. Espionage intrusions go undetected for a median of 122 days, against 14 days across all intrusions [mtrends2026].
Δ −2 · K1: evidence from a second source; split. K2: the participial tail becomes §3.3.1's own wording (L2970, "moves low and slow to avoid detection"). Alt: split only (Δ 0).
**Mark:** ok / alt / keep / look —

### C.8 · L1703 · 3.1.3 Attack profiling · K1
> It scales to many reports, but even identifying which techniques a report describes is not yet reliable: on the 50 most common techniques, the best systems reach 80 % precision at 66 % recall [buchel2025].

**After:** It scales to many reports, but even identifying which techniques a report describes is not yet reliable. On the 50 most common techniques, the best systems reach 80 % precision at 66 % recall [buchel2025].
Δ 0 · K1: evidence in numbers; split.
**Mark:** ok / alt / keep / look —

### C.9 · L2185 · 3.2.1 MTD modelling approaches · K2
> Cho et al. identify three: game theory, genetic algorithms and machine learning, with game theory dominating by volume [cho2020].

**After:** Cho et al. identify three: game theory, genetic algorithms and machine learning. Game theory dominates by volume [cho2020].
Δ −1 · Colon kept (announced count). K2: the "with … dominating" tail becomes its own sentence; the first names Cho et al., so the cite still covers both.
**Mark:** ok / alt / keep / look —

### C.10 · L2190 · 3.2.1 MTD modelling approaches · K1
> Attackers are not necessarily rational: many aim only to exhaust a system's resources, and a strategy found against a rational attacker may not work against them [cho2020].

**After:** Attackers are not necessarily rational. Many aim only to exhaust a system's resources, and a strategy found against a rational attacker may not work against them [cho2020].
Δ 0 · K1: a reason and a consequence; split. The cite stays on the sentence that carries both.
**Mark:** ok / alt / keep / look —

### C.11 · L2979 · 3.3.1 Properties an MTD attacker model needs · K1
> First, they lack adaptivity and learning: the attacker follows fixed attack patterns while the defender adapts and learns, although in practice the attacker is often the smarter of the two.

**After:** First, they lack adaptivity and learning. The attacker follows fixed attack patterns while the defender adapts and learns, although in practice the attacker is often the smarter of the two.
Δ 0 · K1: what the limitation means; split. The paragraph's count ("three limitations") still announces C.11–C.13.
**Mark:** ok / alt / keep / look —

### C.12 · L2982 · 3.3.1 Properties an MTD attacker model needs · K1
> Second, they lack choice of attack strategy: few evaluations let the attacker choose among several attack strategies.

**After:** Second, they lack choice of attack strategy. Few evaluations let the attacker choose among several attack strategies.
Δ 0 · K1: evidence; split, as C.11.
**Mark:** ok / alt / keep / look —

### C.13 · L2983 · 3.3.1 Properties an MTD attacker model needs · K1
> Third, they lack cost–benefit reasoning and deployment-strategy awareness: the attacker is seldom modelled as a rational actor, or as one that exploits how the MTD works.

**After:** Third, they lack cost–benefit reasoning and deployment-strategy awareness. The attacker is seldom modelled as a rational actor, or as one that exploits how the MTD works.
Δ 0 · K1: what the limitation means; split, as C.11.
**Mark:** ok / alt / keep / look —

### C.14 · L2987 · 3.3.1 Properties an MTD attacker model needs · K1
> They find the same lack of learning and deployment-strategy awareness: an APT attacker learns the MTD's deployment patterns over time and looks for the logic of the deployment strategy [jalowski2026].

**After:** They find the same lack of learning and deployment-strategy awareness. An APT attacker learns the MTD's deployment patterns over time and looks for the logic of the deployment strategy [jalowski2026].
Δ 0 · K1: a reason; split.
**Mark:** ok / alt / keep / look —

### C.15 · L2989 · 3.3.1 Properties an MTD attacker model needs · K1
> They add detection avoidance: MTD is typically tested against active scanning, such as Nmap, while an APT attacker uses passive reconnaissance to stay hidden [jalowski2026].

**After:** They add detection avoidance. MTD is typically tested against active scanning, such as Nmap, while an APT attacker uses passive reconnaissance to stay hidden [jalowski2026].
Δ 0 · K1: a reason; split.
**Mark:** ok / alt / keep / look —

### C.16 · L3263 · 3.3.2 Recent MTD attacker models · K1, K2
> A P means a behaviour predicate is true, but not every predicate is true of its own behaviour: a predicate is false, or true only because its authors set the behaviour by a fixed rule, such as always re-scanning after a host-layer disruption, or assume it.

**After:** A P means a behaviour predicate is true, but not every predicate is true of its own behaviour. At least one predicate is false, or true only because its authors assume the behaviour or set it by a fixed rule, such as always re-scanning after a host-layer disruption.
Δ +2 · K1: what the mark means; split, with "At least one" so the new sentence does not read as a generic claim. K2: "or assume it" was stranded after the example; reordered from the sentence's own words. (P is how \propstandin prints.)
**Mark:** ok / alt / keep / look —

### C.17 · L3469 · 3.3.2 Recent MTD attacker models · K3
> Their attacker model is an automated attack script that runs four stages in a fixed order: it scans for web servers, collects the version of each web service it finds, exploits one known vulnerability of the Apache web server, and keeps a reverse shell, an outbound connection from the compromised server back to the attacker.

**After:** Their attacker model is an automated attack script that runs four stages in a fixed order: it scans for web servers, collects the version of each web service it finds, exploits one known vulnerability of the Apache web server, and keeps a reverse shell. A reverse shell is an outbound connection from the compromised server back to the attacker.
Δ +4 · Colon kept (announced count). K3: the reader needs *reverse shell* again (L3476, L3479), so it gets a copula sentence, as item 17. Alt: keep (Δ 0).
**Mark:** ok / alt / keep / look —

### C.18 · L3481 · 3.3.2 Recent MTD attacker models · K2
> It has no deployment-strategy awareness: the attacker "can determine the remaining available time" before the next MTD deployment [kim2026, p. 10], when every mechanism deploys at once, so it predicts which mechanism deploys next and when, but no technique leverages the prediction.

**After:** It has no deployment-strategy awareness: the attacker "can determine the remaining available time" before the next MTD deployment [kim2026, p. 10]. Every mechanism deploys at once, so the attacker predicts which mechanism deploys next and when, but no technique leverages the prediction.
Δ 0 · Colon per the walk block. K2: the "when …" phrase after the quote starts a five-clause chain; split there, and "it" becomes "the attacker" so the referent survives.
**Mark:** ok / alt / keep / look —

### C.19 · L3495 · 3.3.2 Recent MTD attacker models · K1
> Finding. The three MTD attacker models still lack the properties of an APT attacker: only the baseline attacker has one in full, campaign persistence.

**After:** Finding. The three MTD attacker models still lack the properties of an APT attacker. Only the baseline attacker has one in full, campaign persistence.
Δ 0 · K1: evidence; split. The property stays at the end, in the stress position.
**Mark:** ok / alt / keep / look —

### C.20 · L3953 · 4 APT attacker model (chapter opening) · K1
> It is a proof of concept: it tests whether an attacker with more of an APT's properties changes what an MTD evaluation measures.

**After:** It is a proof of concept that tests whether an attacker with more of an APT's properties changes what an MTD evaluation measures.
Δ −1 · K1: what the term means; the sentence's own words rebuilt around "that".
**Mark:** ok / alt / keep / look —

### C.21 · L4041 · 4.1 Attack graph from attack flows · K1
> A step between two techniques of the same tactic is not an edge: the time an attacker spends within a tactic is its tactic duration (Section 4.4.2).

**After:** A step between two techniques of the same tactic is not an edge because the time an attacker spends within a tactic is its tactic duration (Section 4.4.2).
Δ +1 · K1: a reason; *because* states it. Alt: split (Δ 0), which leaves the link implicit.
**Mark:** ok / alt / keep / look —

### C.22 · L4077 · 4.1 Attack graph from attack flows · K1
> We built the attack graph from attack flows because they come from manual attack profiling: an analyst drew the order of every step.

**After:** We built the attack graph from attack flows because they come from manual attack profiling. An analyst drew the order of every step.
Δ 0 · K1: what the term means; split.
**Mark:** ok / alt / keep / look —

### C.23 · L4085 · 4.1 Attack graph from attack flows · K1
> The corpus is not limited to APT attackers: 18 of the 38 attack flows are attributed to a group in ATT&CK, criminal groups among them, and the other 20 name no group; one is an adware campaign.

**After:** The corpus is not limited to APT attackers. Only 18 of the 38 attack flows are attributed to a group in ATT&CK, criminal groups among them, and the other 20 name no group. One is an adware campaign.
Δ +1 · K1: evidence; split, with "Only" so the sentence does not open on a numeral. The semicolon joins a second sentence, not a paired opposition (voice §d), so a full stop, as items 6 and 8.
**Mark:** ok / alt / keep / look —

### C.24 · L4093 · 4.1 Attack graph from attack flows · K1
> Most edges between techniques come from one attack flow alone: 88 %, against 39 % of the edges between tactics (Appendix C.1).

**After:** Most edges between techniques (88 %) come from one attack flow alone, against 39 % of the edges between tactics (Appendix C.1).
Δ 0 · K1: evidence in numbers; a split would leave a fragment, so the figure moves into a parenthesis beside the noun it counts.
**Mark:** ok / alt / keep / look —

### C.25 · L4098 · 4.1 Attack graph from attack flows · K1
> Tactics also make the tactic-to-action mapping smaller: it maps 15 tactics, rather than the 124 techniques the attack flows use, to MTDSim's six attack actions (Section 4.4).

**After:** Tactics also make the tactic-to-action mapping smaller. It maps 15 tactics, rather than the 124 techniques the attack flows use, to MTDSim's six attack actions (Section 4.4).
Δ 0 · K1: evidence in numbers; split.
**Mark:** ok / alt / keep / look —

### C.26 · L4101 · 4.1 Attack graph from attack flows · K1
> The attack graph is sparsest before Initial Access: Reconnaissance appears in 10 of the 38 attack flows.

**After:** The attack graph is sparsest before Initial Access. Reconnaissance appears in 10 of the 38 attack flows.
Δ 0 · K1: evidence; split.
**Mark:** ok / alt / keep / look —

### C.27 · L4289 · 4.2 Attack profiles by objective · K1
> Section 5.4 ablates the split: it runs the APT attacker model on the whole attack graph of Section 4.1 and compares the results with those of the four attack profiles.

**After:** Section 5.4 ablates the split. It runs the APT attacker model on the whole attack graph of Section 4.1 and compares the results with those of the four attack profiles.
Δ 0 · K1: what the term means; split.
**Mark:** ok / alt / keep / look —

### C.28 · L4394 · 4.3 Petri-net formalism · K1
> No transition leads from a tactic back to itself: the time spent in a tactic is the delay of $\tau_p$.

**After:** No transition leads from a tactic back to itself because the tactic duration is the delay of $\tau_p$.
Δ −2 · K1: a reason, as C.21. Merged with D.7 (K6): the registered term *tactic duration* replaces the paraphrase. Alt: split (Δ −3).
**Mark:** ok / alt / keep / look —

### C.29 · L4412 · 4.3 Petri-net formalism · K1
> The single token means the attacker pursues one line of the campaign at a time: where an attack flow draws parallel branches, the token follows one of them.

**After:** The single token means the attacker pursues one line of the campaign at a time. Where an attack flow draws parallel branches, the token follows one of them.
Δ 0 · K1: a consequence; split.
**Mark:** ok / alt / keep / look —

### C.30 · L4440 · 4.3 Petri-net formalism · K1
> A GSPN cannot route on the verdict: its weights are constants, or functions of the marking, and the verdict comes from MTDSim, outside the Petri net.

**After:** A GSPN cannot route on the verdict. Its weights are constants, or functions of the marking, and the verdict comes from MTDSim, outside the Petri net.
Δ 0 · K1: a reason; split. Alt: *because* (Δ +1).
**Mark:** ok / alt / keep / look —

### C.31 · L4443 · 4.3 Petri-net formalism · K1
> We therefore extend the GSPN with one element, the failure matrix $F$: a declared factor between zero and one for each pair of tactics (Section 4.4.3).

**After:** We therefore extend the GSPN with one element, the failure matrix $F$. It holds a declared factor between zero and one for each pair of tactics (Section 4.4.3).
Δ +2 · K1: what the term means; a copula-style sentence of its own.
**Mark:** ok / alt / keep / look —

### C.32 · L4700 · 4.4 Integration with MTDSim · K1
> The vulnerability memory (Section 4.4.4) extends MTDSim's exploit attack action: each earlier success on a vulnerability raises the attacker's odds of exploiting it again.

**After:** The vulnerability memory (Section 4.4.4) extends MTDSim's exploit attack action. Each earlier success on a vulnerability raises the attacker's odds of exploiting it again.
Δ 0 · K1: what the extension means; split.
**Mark:** ok / alt / keep / look —

### C.33 · L4932 · 4.4.1 Tactic-to-action mapping · K1
> These gaps set the ceiling of this dissertation: the APT attacker model can only be as good as the attack actions it adopts.

**After:** These gaps set the ceiling of this dissertation. The APT attacker model can only be as good as the attack actions it adopts.
Δ 0 · K1: what the term means; split. The second sentence is the quotable one and now stands alone.
**Mark:** ok / alt / keep / look —

### C.34 · L5051 · 4.4.2 Tactic durations · K1
> Because these values are our judgement, Appendix D.4 tests whether NCR (Section 4.5) depends on them: after the values were fixed, it moved each mean duration in turn to both ends of a band, from half to double, and from a quarter to four times for the 45 s.

**After:** Because these values are our judgement, Appendix D.4 tests whether NCR (Section 4.5) depends on them. After the values were fixed, it moved each mean duration in turn to both ends of a band, from half to double, and from a quarter to four times for the 45 s.
Δ 0 · K1: the procedure is a second sentence; the split halves a 48-word sentence.
**Mark:** ok / alt / keep / look —

### C.35 · L5290 · 4.4.4 Vulnerability memory · K1
> The baseline attacker already remembers the vulnerabilities it has exploited: exploiting one again takes it half the time (Section 2.2.3).

**After:** The baseline attacker already remembers the vulnerabilities it has exploited. Exploiting one again takes it half the time (Section 2.2.3).
Δ 0 · K1: what remembering means; split.
**Mark:** ok / alt / keep / look —

### C.36 · L5361 · 4.5 Evaluation metrics · K3
> We also add one MTD effectiveness metric for a fourth property, adaptivity: time lost per MTD deployment, how much each deployment delays the attacker.

**After:** We also add one MTD effectiveness metric for a fourth property, adaptivity: time lost per MTD deployment.
Δ −7 · Colon kept ("one metric" announces it). K3: the gloss repeats the name and its definition (L5640); round 8 of this paragraph cut the metric glosses.
**Mark:** ok / alt / keep / look —

### C.37 · L8412 · 5.4 Ablation studies · K1
> The failure matrix leaves time lost per MTD deployment unchanged: under IP shuffle and OS diversity at 2 000 s, the 95 % interval of the difference with and without it includes zero.

**After:** The failure matrix leaves time lost per MTD deployment unchanged. Under IP shuffle and OS diversity at 2 000 s, the 95 % interval of the difference with and without it includes zero.
Δ 0 · K1: evidence in numbers; split.
**Mark:** ok / alt / keep / look —

### C.38 · L8653 · 6.1 APT attacker model versus baseline attacker · K1
> On objective-specific behaviour, the attack profiles' runs still differ in MTDSim, most of all in actions on objectives (Figure 5.1(a)): Exfiltration occurs only in $c_1$ and $c_3$, Impact almost only in $c_2$ and $c_3$, and neither in $c_4$.

**After:** On objective-specific behaviour, the attack profiles' runs still differ in MTDSim, most of all in actions on objectives (Figure 5.1(a)). Exfiltration occurs only in $c_1$ and $c_3$, Impact almost only in $c_2$ and $c_3$, and neither in $c_4$.
Δ 0 · K1: evidence; split.
**Mark:** ok / alt / keep / look —

### C.39 · L9344 · 6.5 Threats to validity · K1
> NCR reduction, our main metric, only partially measures how MTD performs: it counts the hosts an attacker compromises, whether or not it reaches a target host in the targeted attack scenario.

**After:** NCR reduction, our main metric, only partially measures how MTD performs. It counts the hosts an attacker compromises, whether or not it reaches a target host in the targeted attack scenario.
Δ 0 · K1: a reason; split. The threat sentence keeps its conventional wording.
**Mark:** ok / alt / keep / look —

### C.40 · L9400 · 6.5 Threats to validity · K1
> To mitigate this threat, we declared these values before any result and tested them one at a time: timing changes NCR most, but the rankings hold across its band (Table D.7), and without the failure matrix, which sets the response to failure, NCR changes negligibly (Section 5.4).

**After:** To mitigate this threat, we declared these values before any result and tested them one at a time. Timing changes NCR most, but the rankings hold across its band (Table D.7). Without the failure matrix, which sets the response to failure, NCR changes negligibly (Section 5.4).
Δ −1 · K1: the colon hinges two results onto the mitigation; three sentences. The gloss stays, because it maps the failure matrix to the threat's own "response to failure".
**Mark:** ok / alt / keep / look —

### C.41 · L9424 · 6.5 Threats to validity · K1
> Section 6.3's comparison only partially measures how closely an attacker model represents an APT attacker: we synthesised the eight properties from the APT definition and two surveys, and scored each attacker model from a face-value reading of its papers.

**After:** Section 6.3's comparison only partially measures how closely an attacker model represents an APT attacker. We synthesised the eight properties from the APT definition and two surveys, and scored each attacker model from a face-value reading of its papers.
Δ 0 · K1: a reason; split, as C.39.
**Mark:** ok / alt / keep / look —

### C.42 · L9434 · 6.5 Threats to validity · K1
> The comparison covers only four attacker models: the three MTD attacker models we chose (Section 3.3.2) include none from game theory, the dominant MTD modelling approach [cho2020].

**After:** The comparison covers only four attacker models. The three MTD attacker models we chose (Section 3.3.2) include none from game theory, the dominant MTD modelling approach [cho2020].
Δ 0 · K1: a reason; split. The closing gloss stays, because it says why the gap matters.
**Mark:** ok / alt / keep / look —

### C.43 · L9916 · 7.2 Future work · K1
> The attack actions are the highest priority: we kept them unchanged by design, and they limit every result.

**After:** The attack actions are the highest priority. We kept them unchanged by design, and they limit every result.
Δ 0 · K1: reasons the claim does not announce; split.
**Mark:** ok / alt / keep / look —

### C.44 · L10110 · Appendix B Predicate tests of the attacker models · K1
> Distinct openings (Equation 4.6) backs the APT attacker model's mark for choice of attack strategy (Section 6.1): counted in attack actions, as for the baseline attacker, the attack profiles have 190 to 844 distinct openings against its 3.

**After:** Distinct openings (Equation 4.6) backs the APT attacker model's mark for choice of attack strategy (Section 6.1). Counted in attack actions, as for the baseline attacker, the attack profiles have 190 to 844 distinct openings against its 3.
Δ 0 · K1: evidence in numbers; split. "its" still finds the baseline attacker in its own sentence.
**Mark:** ok / alt / keep / look —

### C.45 · L10192 · C.1 The attack graph with techniques as nodes · K1
> Section 4.1 chose tactics as the nodes of the attack graph because most edges between techniques are drawn by only one attack flow: 419 of the 478 (88 %), against 47 of the 122 edges between tactics (39 %).

**After:** Section 4.1 chose tactics as the nodes of the attack graph because 419 of the 478 edges between techniques (88 %) are drawn by only one attack flow, against 47 of the 122 edges between tactics (39 %).
Δ −1 · K1: evidence in numbers after a colon left a fragment; the count becomes the subject, so "most" goes.
**Mark:** ok / alt / keep / look —

### C.46 · L10282 · C.4 Tactic durations against the baseline attacker's times · K1, K3
> Six tactics take MTDSim's time for the same kind of work, even where they run another attack action: 4.5 s, the exploit's, or 35 s, the three scans' together.

**After:** Six tactics take MTDSim's time for the same kind of work, even where they run another attack action. Each takes the exploit's 4.5 s or the three scans' 35 s together.
Δ +2 · K1: the values are an instance, and the clause before does not announce them; split. K3: two appositive glosses fold into possessives, and three commas become none.
**Mark:** ok / alt / keep / look —

### C.47 · L10555 · D.4 Sensitivity analysis of the tactic durations · K1
> The comparison holds at both ends: the host layer still ranks above the service layer, the APT attacker model's rank 1 still shares no MTD mechanism with the baseline attacker's, and the two rankings stay uncorrelated.

**After:** The comparison holds at both ends. The host layer still ranks above the service layer, the APT attacker model's rank 1 still shares no MTD mechanism with the baseline attacker's, and the two rankings stay uncorrelated.
Δ 0 · K1: evidence; split. Alt (b): "holds at both ends in three ways:" announces the list (Δ +3).
**Mark:** ok / alt / keep / look —

### C.48 · L10619 · D.5.1 Ablation of the tactic durations · K1
> Then each mapped tactic also takes the baseline attacker's time for the attack action it runs: Command and Control takes 5 s for scan neighbours in place of 45 s, and Credential Access 20 s for brute force in place of 4.5 s.

**After:** Then each mapped tactic also takes the baseline attacker's time for the attack action it runs. Command and Control takes 5 s for scan neighbours in place of 45 s, and Credential Access 20 s for brute force in place of 4.5 s.
Δ 0 · K1: the instances that change; split.
**Mark:** ok / alt / keep / look —

**Total if all taken:** Δ +2 (about −6 with the alternatives for C.1, C.17, C.21 and C.28). 44 proposals remove a colon; with walk option (b), about 67.

---

## A1. Comma jobs, chapters 1–4

**Rule.** Readers stress what arrives at the end of a sentence, so a qualifier appended after the last comma puts a minor detail where the point belongs (Gopen & Swan, "The Stress Position"). Many-comma sentences "often have strangulated syntax … consider breaking the sentence into shorter ones" (Zobel p. 125), and information "embedded within a sentence that is not part of its main statement" should be avoided (Zobel p. 102).

**The cluster-wide move.**
- (a) **Split.** A two-idea sentence becomes two, and a needed gloss becomes a copula sentence. Pro: removes the hinge and lands short verdicts. Con: a few items add words.
- (b) **Rearrange in place.** Move the tail or the gloss inside the sentence, or drop a comma, a dead gloss or an unused abbreviation. Pro: Δ ≤ 0, and the edit does not show. Con: some long sentences stay long.
- (c) **Keep all.** The prose already runs below the field's comma rate. Con: it leaves the K2 (×3.5) and K3 (×2) surplus that §3 measured.
- **Recommended:** (b) first, and (a) only where the sentence holds two ideas or a term the reader needs. 19 of the 24 items are Δ ≤ 0, and the net is −20 words.

**Kept as warranted (41).**
- `L246`: acknowledgements, personal register, a parallel list of thanks.
- `L443`: "such as stealing data" grounds *objective* for the chapter 1 reader.
- `L464`: a conditional clause, not an appositive.
- `L466`: a conditional clause, not an appositive.
- `L618`: scoping commas, and verbatim with §6.4 and chapter 7.
- `L694`: chapter opener. *Inherits* is the honest-claim fact.
- `L717`: an example list after *such as*.
- `L759`: a gapped roadmap list, parallel by design.
- `L798`: the gloss defines the emphasised term in its own sentence.
- `L811`: covered by calibration item 10. The *which* clause carries a needed fact.
- `L873`: the consequence (*proactive*) is the point, in the stress position.
- `L956`: a list of three end conditions.
- `L991`: the tail carries the point, that tried hosts return.
- `L1000`: a gapped list of times.
- `L1003`: the chain ends on its result, the range.
- `L1213`: a roadmap gloss that sets up *techniques* for the next sentence.
- `L1290`: semicolons separate four named stages that contain commas.
- `L1464`: a list of the hierarchy's levels.
- `L1466`: parallel definitions of the hierarchy's levels.
- `L1696`: covered by calibration item 16.
- `L3438`: the tail (before and after) is the comparison, the point.
- `L3466`: the gloss names the specific testbed. Ratified round 63, parallel with Masud.
- `L4091`: the trade-off is the justification, in the stress position.
- `L4200`: names the symbols $c_1$–$c_4$ that later text reuses.
- `L4376`: a *where* list decoding an equation.
- `L4459`: fronted conditions in given-new order.
- `L4655`: an enumerated item. The gloss is *tactic duration*'s first definition.
- `L4668`: two conditions, with a bracketed example on the first.
- `L4971`: two short appositives that name the parameter and the defined term.
- `L5009`: a parallel derivation walk, with the value in the stress position.
- `L5012`: a parallel derivation walk, with the value in the stress position.
- `L5026`: a parallel derivation walk, with the value in the stress position.
- `L5030`: a parallel derivation walk. The *which* clause carries the judgement.
- `L5060`: the consequence lands on the point.
- `L5299`: "on any host" carries the across-host fact.
- `L5314`: the nuance answers the expectation, and the *but* clause is the verdict.
- `L5486`: the tail names the proxy, which is the sentence's point.
- `L5497`: the *which* clause carries the needed fact (an IDS flags bursts).
- `L5635`: the glosses decode the two ends of the range.
- `L5638`: the property link is needed, and a split costs +2.
- `L5650`: a worked example, with the givens before the result.

**Proposals (24).**

### A1.1 · L453 · Chapter 1 · K3
> We execute each attack profile in MTDSim, an existing MTD simulator [brown2023], as the APT attacker model.

**After:** We execute each attack profile as the APT attacker model in MTDSim, an existing MTD simulator [brown2023].
Δ 0 · K3: the gloss and the cite split the verb from its complement. Rearranged, the new term lands in the stress position, and the next sentence opens on *MTDSim*. Alt: a copula sentence first, "MTDSim is an existing MTD simulator [brown2023]." (+2).
**Mark:** ok / alt / keep / look —

### A1.2 · L455 · Chapter 1 · K3
> MTDSim's original scripted attacker, the baseline attacker, follows a fixed procedure of six attack actions, such as scanning a host's ports and exploiting its vulnerabilities.

**After:** MTDSim's original scripted attacker is the baseline attacker. It follows a fixed procedure of six attack actions, such as scanning a host's ports and exploiting its vulnerabilities.
Δ +2 · K3: the reader needs this term for the whole dissertation, so it gets a copula sentence, the move of calibration item 16. The term lands in the stress position. The +2 is the copula.
**Mark:** ok / alt / keep / look —

### A1.3 · L461 · Chapter 1 · K3
> We run both first with no MTD, then under each of MTDSim's seven MTD mechanisms at six deployment intervals, how often MTD changes the network.

**After:** We run both first with no MTD, then under each of MTDSim's seven MTD mechanisms at six deployment intervals.
Δ −6 · K3: §2.2.2 defines *deployment interval* as "the time between deployments". This gloss pre-defines it in other words (voice §0.5) and hangs off the stress position. Alt: a copula sentence in §2.2.2's words, "A deployment interval is the time between MTD deployments." (+3 net).
**Mark:** ok / alt / keep / look —

### A1.4 · L663 · Chapter 1 · K2
> It answers SQ1 and SQ2 by scoring the APT attacker model on the eight properties, and SQ3 by finding which MTD mechanisms are most effective against each attacker, and proposing why.

**After:** It answers SQ1 and SQ2 by scoring the APT attacker model on the eight properties, and SQ3 by finding which MTD mechanisms are most effective against each attacker and proposing why.
Δ 0 · K2: the last comma sets "proposing why" loose, like a third item. Without it, the phrase reads as the second half of SQ3's answer.
**Mark:** ok / alt / keep / look —

### A1.5 · L720 · §2.1 · K3
> How to move is one of three operations, the shuffle–diversity–redundancy (SDR) taxonomy [hongkim2016].

**After:** How to move is one of the three operations of the shuffle–diversity–redundancy taxonomy [hongkim2016].
Δ +1 · K3: the appositive equates three operations with a taxonomy. *SDR* is used nowhere else, so it goes (K7, Zobel p. 120).
**Mark:** ok / alt / keep / look —

### A1.6 · L876 · §2.2.2 · K2
> At each interval it reads the network's security metrics and the attacker's current attack action, and deploys one of four mechanisms (complete topology shuffle, IP shuffle, OS diversity or service diversity) or none; if 2 000 s pass without a deployment, one is forced [tay2024code].

**After:** At each interval it reads the network's security metrics and the attacker's current attack action, and deploys one of four mechanisms (complete topology shuffle, IP shuffle, OS diversity or service diversity) or none. If 2 000 s pass without a deployment, one is forced [tay2024code].
Δ 0 · K2: the forced deployment is a second idea appended after a semicolon. Split rather than connect (§4 rule 4).
**Mark:** ok / alt / keep / look —

### A1.7 · L979 · §2.2.3 · K3
> On each host it tries stolen credentials first, then exploits the vulnerabilities in order of return on attack [brown2023], an exploit's probability of success times its impact, divided by the time it takes [tay2024code], and brute force last.

**After:** On each host it tries stolen credentials first, then exploits the vulnerabilities in order of *return on attack* [brown2023], and brute force last. Return on attack is an exploit's probability of success times its impact, divided by the time it takes [tay2024code].
Δ +4 · K3: a definition nested inside a three-step sequence buries "brute force last". §3.3.2 reuses the term (as RoA), so the reader needs a copula sentence. Each cite stays on its claim. Alt: put the gloss in a parenthesis in place (Δ 0). That nests a cite inside the bracket.
**Mark:** ok / alt / keep / look —

### A1.8 · L1040 · §2.2.3, chapter close · K3
> Chapter 3 compares the baseline attacker, and the attacker models of recent MTD evaluations, with an APT attacker.

**After:** Chapter 3 compares the baseline attacker and the attacker models of recent MTD evaluations with an APT attacker.
Δ 0 · K3 (paired commas): the comma pair demotes an equal object to an aside. Chapter 3 scores all three models alike.
**Mark:** ok / alt / keep / look —

### A1.9 · L1419 · §3.1.2 · K2
> MITRE ATT&CK is a knowledge base of attacker behaviour derived from real-world observations, developed by the MITRE Corporation in 2013 [strom2018mitre], and the common language for attacker behaviour [ferraz2026, buchel2025].

**After:** MITRE ATT&CK is a knowledge base of attacker behaviour derived from real-world observations, developed by the MITRE Corporation in 2013 [strom2018mitre]. It is the common language for attacker behaviour [ferraz2026, buchel2025].
Δ +1 · K2: the appended "and the common language" is a second claim with its own cites. After the participle, it garden-paths as "developed by the MITRE Corporation … and the common language". Split.
**Mark:** ok / alt / keep / look —

### A1.10 · L3257 · §3.3.2 · K2
> This dissertation scores each attacker model on each property from its paper, by predicates taken from each definition in Table 3.2 (Appendix B), with one of three marks.

**After:** This dissertation scores each attacker model on each property from its paper with one of three marks, by predicates taken from each definition in Table 3.2 (Appendix B).
Δ 0 · K2: two tails were stacked. Rearranged, *predicates* ends the sentence, and the next sentence ("A behaviour predicate states…") opens on it. One comma fewer.
**Mark:** ok / alt / keep / look —

### A1.11 · L3497 · §3.3.2 Finding · K2
> None of the three has objective-specific behaviour, cost–benefit reasoning, learning or deployment-strategy awareness, and only Kim et al.'s has detection avoidance, in part.

**After:** None of the three has objective-specific behaviour, cost–benefit reasoning, learning or deployment-strategy awareness. Only Kim et al.'s has detection avoidance in part.
Δ −1 · K2: these are two verdicts, so split them. "In part" stops trailing behind a comma and reads as the score's own wording ("has it in part").
**Mark:** ok / alt / keep / look —

### A1.12 · L3499 · §3.3.2 Finding · K3
> The attacker models of Masud et al. and Kim et al., which this dissertation expected to be the most likely to have the properties, have none in full.

**After:** This dissertation expected the attacker models of Masud et al. and Kim et al. to be the most likely to have the properties. They have none in full.
Δ 0 · K3: the interposed clause split the subject from its verdict. Split, the expectation (set at §3.3.2's opening) becomes the head, and the verdict lands as a short sentence (voice §d).
**Mark:** ok / alt / keep / look —

### A1.13 · L4088 · §4.1 · K2
> We keep all 38, because dropping the 20 would halve an already sparse corpus, so the attack graph records attackers reported in CTI, not APT attackers alone (Section 6.5).

**After:** We keep all 38, because dropping the 20 would halve an already sparse corpus. The attack graph therefore records attackers reported in CTI, not APT attackers alone (Section 6.5).
Δ 0 · K2: in the *because …, so …* chain, *so* can attach to the halving or to the keeping. Split, so the consequence is its own sentence. "Therefore" replaces "so".
**Mark:** ok / alt / keep / look —

### A1.14 · L4103 · §4.1 · K2
> Reconnaissance and Resource Development happen largely outside the scope of the defender's controls [mitre2026attackkb], so the investigations that CTI reports rarely see them, and any CTI corpus shares the gap.

**After:** Reconnaissance and Resource Development happen largely outside the scope of the defender's controls [mitre2026attackkb], so the investigations that CTI reports rarely see them. Any CTI corpus shares the gap.
Δ −1 · K2: the generalisation beyond this corpus is the point, but it was appended as a third clause. Its own sentence gives it the stress position.
**Mark:** ok / alt / keep / look —

### A1.15 · L4356 · §4.3 · K3
> Cai et al. compare MTD mechanisms with one variant in particular, the generalised stochastic Petri net (GSPN) [cai2016].

**After:** Cai et al. compare MTD mechanisms with the generalised stochastic Petri net (GSPN) [cai2016].
Δ −4 · K3: "one variant in particular" is a lead-in that the name repeats. *Generalised stochastic Petri net* already says it is a variant of the previous sentence's stochastic Petri nets.
**Mark:** ok / alt / keep / look —

### A1.16 · L4371 · §4.3 · K2
> Of several enabled immediate transitions, one fires, with probability proportional to its weight.

**After:** Of several enabled immediate transitions, one fires with probability proportional to its weight.
Δ 0 · K2: the firing rule is the sentence's substance, but the comma made it an afterthought.
**Mark:** ok / alt / keep / look —

### A1.17 · L4901 · §4.4.1 · K2
> Initial Access, Execution and Privilege Escalation each include a technique that exploits a vulnerability, so all three map to exploit, and Reconnaissance and Discovery each include a scanning technique, so Reconnaissance maps to scan host and Discovery to scan port.

**After:** Initial Access, Execution and Privilege Escalation each include a technique that exploits a vulnerability, so all three map to exploit. Reconnaissance and Discovery each include a scanning technique, so Reconnaissance maps to scan host and Discovery to scan port.
Δ −1 · K2: two parallel mappings were joined by ", and" (Zobel p. 125). Split, each one reads as a single *because–so* step.
**Mark:** ok / alt / keep / look —

### A1.18 · L4966 · §4.4.2 · K2
> They set how often the APT attacker model acts, and the longer a tactic runs, the more likely an MTD deployment disrupts it.

**After:** They set how often the APT attacker model acts. The longer a tactic runs, the more likely an MTD deployment disrupts it.
Δ −1 · K2: two ideas. The disruption claim, the one chapter 5 tests, gets its own sentence.
**Mark:** ok / alt / keep / look —

### A1.19 · L5056 · §4.4.2 · K3
> Only the 45 s changes NCR much, most likely through Command and Control, one of the three tactics it times.

**After:** Only the 45 s changes NCR much, most likely through Command and Control.
Δ −7 · K3: the reader already has the gloss, since the 45 s timing Persistence, Stealth and Command and Control was set about 30 lines above. Cutting it ends the sentence on the tactic that the next sentence picks up.
**Mark:** ok / alt / keep / look —

### A1.20 · L5185 · §4.4.3 · K2
> Third, an attacker seldom skips a lifecycle stage, as in the lifecycle models of Section 3.1.1, which run their stages in sequence.

**After:** Third, an attacker seldom skips a lifecycle stage, as in the lifecycle models of Section 3.1.1.
Δ −5 · K2: the trailing *which* clause restates what "seldom skips a lifecycle stage" and §3.1.1 already give, and the cut ends the sentence on the source. Alt: keep, if the sequential order is felt to be the warrant.
**Mark:** ok / alt / keep / look —

### A1.21 · L5219 · §4.4.3 · K3
> Where the attack flows give a tactic no next tactic, a dead end, there is nothing to reweight, and the token retraces the edge it travelled.

**After:** Where the attack flows give a tactic no next tactic, there is nothing to reweight, and the token retraces the edge it travelled.
Δ −3 · K3/K7: "dead end" names the condition once and is never used again, so the name does no work.
**Mark:** ok / alt / keep / look —

### A1.22 · L5295 · §4.4.4 · K3
> It is not learning, property 7 of Table 3.2: it keeps vulnerabilities, not the patterns of MTD deployments, and it changes the odds of an exploit, not which technique comes next.

**After:** It is not learning (property 7 of Table 3.2): it keeps vulnerabilities, not the patterns of MTD deployments, and it changes the odds of an exploit, not which technique comes next.
Δ 0 · K3: after "not learning," the comma reads as the start of a list. A parenthesis marks the pointer as a pointer, which voice §d calls the authored device. The colon introduces the reasons (warranted, §1 K1).
**Mark:** ok / alt / keep / look —

### A1.23 · L5303 · §4.4.4 · K3
> Hosts that run the same service carry the same vulnerabilities, so we expect the memory to matter more when the diversity pool, the services each operating system can run, is small.

**After:** The *diversity pool* is the services each operating system can run. Hosts that run the same service carry the same vulnerabilities, so we expect the memory to matter more when the diversity pool is small.
Δ +4 · K3: the definition interrupts "when the diversity pool … is small". Chapter 5 uses the term three times, so it needs a copula sentence. Alt: keep. The gloss sits at first use, and the split costs four words.
**Mark:** ok / alt / keep / look —

### A1.24 · L5501 · §4.5.1 · K3
> MTDSim has no IDS, so one stands in with a single rule, the default port-scan rule of the Snort IDS, which flagged a source that connected to five different addresses within 60 s [Sect. 5.2, jung2004].

**After:** MTDSim has no IDS, so the default port-scan rule of the Snort IDS stands in for one. It flagged a source that connected to five different addresses within 60 s [Sect. 5.2, jung2004].
Δ −3 · K3: in the chain *so …, appositive, which …*, the rule is named only after "a single rule". The rule becomes the subject, and its threshold gets its own sentence. Alt, to keep *single*: "…so a single rule stands in for one. It is the default port-scan rule of the Snort IDS, which flagged…" (+1).
**Mark:** ok / alt / keep / look —

---

## A2. Comma jobs, chapters 5–7 and appendices

**Rule.** The end of a sentence is its stress position, so an appended qualifier there buries the point (Gopen & Swan, "The Stress Position"; Zobel p. 106). A sentence with many commas should be broken into shorter ones (Zobel p. 125), and information nested in a sentence that is not part of its main statement should be avoided (Zobel p. 102).

**The cluster-wide move.**
- (a) **Split** at the tail, so that the nuance heads its own sentence. Pro: it removes participial tails (Reinhart: 5.3× the human rate) and stacked tails. Con: more sentences, sometimes +1 word.
- (b) **Reorder** inside the sentence by fronting the scope phrase. Pro: Δ 0. Con: in results prose it pushes the comparison back from the opening.
- (c) **Keep.** Pro: no rework. Con: leaves the participial and stacked tails in place.
- **Recommended:** (a) for participial tails, stacked tails, and glosses repeated after first use. (c) everywhere else, because most tails in chapters 5–7 carry a number, a scope or a cited rationale the reader needs.

**Kept as warranted (49).**
- `L6171` — tail carries the source of the two-target change
- `L6193` — appositive carries the cited rationale for 1 000 seeds
- `L6201` — equipment list, ratified today (851dfed6, rubric 4.2)
- `L6204` — mid-sentence aside; the stress lands on the scripts
- `L6278` — appositive states the sign convention used in §5.4
- `L6279` — the three verdict conditions, defined in parallel
- `L6809` — first place the body ties these tactics to actions on objectives
- `L6827` — "into" phrase names the branch; tail bounds it
- `L7049` — paired numeric comparison
- `L7063` — numeric appositives
- `L7621` — paired numeric comparison
- `L7632` — flag spurious; one clause
- `L7864` — parallel paired result; the commas sit inside the interval notation
- `L8120` — tail announces the two cases the next sentences walk
- `L8125` — paired clauses, no gloss
- `L8295` — d appositive is the number; the count list sums to 60
- `L8340` — the ablation house formula (also L8293); d carries the number
- `L8404` — paired numeric contrast
- `L8581` — roadmap; "answers" parallels the sibling sentence
- `L8679` — paired numeric gapping; "3" is a numeral for comparison (APA)
- `L8682` — "whereas" pairs an opposition; the proportion is spec
- `L8700` — numeric appositives on a paired comparison
- `L8705` — comparator tails carry the reversal at each stress position
- `L8709` — first place the body ties these tactics to detection
- `L8789` — semicolon paired opposition with numbers (§d)
- `L8829` — parallel which-clauses carry the mechanism facts
- `L8831` — paired numeric comparison
- `L8950` — flag spurious; a list of three named properties
- `L8986` — appositive names the two parts the next sentence uses
- `L9033` — scope tail is the claim's strength; "On X" house opener
- `L9048` — the comma pair marks the training-attacker aside
- `L9063` — the scope tail is the claim's strength
- `L9071` — the tail states the control that licenses the contrast
- `L9090` — "such as" names Table 3.1's cost metrics
- `L9109` — "dominant" is the finding the implication rests on
- `L9245` — the which-tail is the mitigation's result, at the stress position
- `L9351` — the tail carries the mechanism's result
- `L9395` — the because-clause is the threat's cause
- `L9432` — threats-terminology closing formula
- `L9487` — paired opposition; deliberate "In MTDSim" anaphora
- `L9510` — three corpus biases, each with its section reference
- `L9812` — parallel paired result
- `L9871` — flag spurious; one clause
- `L9933` — parallel future-work closer that ties to the verdict
- `L9968` — parallel future-work closer that ties to the verdict
- `L10235` — attribution aside; the sibling sentences' "so its attacker" formula
- `L10399` — semicolon pairs an opposition; "live" contrasts "before the run starts"
- `L10407` — paired percentages in respective order
- `L10435` — short causal chain of 13 words

**Proposals (20).**

### A2.1 · L6825 · §5.2 APT attacker model versus baseline attacker · K3
> The baseline attacker's runs share one opening over their first four steps, the order of its fixed procedure (Section 2.2.3).

**After:** The baseline attacker's fixed procedure gives all its runs one opening over their first four steps (Section 2.2.3).
Δ −2 · The appositive attaches to "four steps" but means "one opening". The procedure becomes the head (the K3 move).
**Mark:** ok / alt / keep / look —

### A2.2 · L7642 · §5.3.1 Disruption per MTD deployment · K2
> The first deployment disrupts the baseline attacker while it exploits its first exposed endpoint, and its procedure sends it straight back to that endpoint, keeping the progress it made there (Section 2.2.3).

**After:** The first deployment disrupts the baseline attacker while it exploits its first exposed endpoint. Its procedure sends it straight back to that endpoint with the progress it made there (Section 2.2.3).
Δ −1 · A participial tail on a two-idea sentence, so split. Round 3 (2026-10-06) split this passage; this takes the split one step further. Alt: "…endpoint, and it keeps the progress it made there" (+1), if "with" reads weaker than "keeping".
**Mark:** ok / alt / keep / look —

### A2.3 · L8097 · §5.3.3 MTD effectiveness by attack profile · K3, K2
> At 50 to 200 s, the deployment intervals the earlier MTDSim studies ran, the four attack profiles' NCR reductions differ from one another less than the baseline attacker's NCR reduction differs from the nearest attack profile's, under every MTD mechanism and deployment strategy (Figure 5.4).

**After:** Under every MTD mechanism and deployment strategy at 50 to 200 s, the four attack profiles' NCR reductions differ from one another less than the baseline attacker's NCR reduction differs from the nearest attack profile's (Figure 5.4). The earlier MTDSim studies ran these deployment intervals.
Δ +1 · A 42-word sentence with an opening appositive and an appended scope (Zobel p. 125). The paragraph now opens on its comparison, and the context gets its own sentence. Alt: drop the context sentence (−7 in all).
**Mark:** ok / alt / keep / look —

### A2.4 · L8658 · §6.1 APT attacker model versus baseline attacker · K2
> Collection, Exfiltration and Impact, the tactics of actions on objectives, are unmapped, because MTDSim's six attack actions only find and compromise hosts (Section 2.2.3), so the APT attacker model steals no data and impedes no system.

**After:** Collection, Exfiltration and Impact, the tactics of actions on objectives, are unmapped because MTDSim's six attack actions only find and compromise hosts (Section 2.2.3). The APT attacker model therefore steals no data and impedes no system.
Δ 0 · Five commas chain *because* and *so*. The consequence gets its own sentence. Alt: also drop the gloss (−6), since the previous sentence already ties Exfiltration and Impact to actions on objectives.
**Mark:** ok / alt / keep / look —

### A2.5 · L8977 · §6.3 APT attacker model versus MTD attacker models · K2
> In answer to SQ2, the APT attacker model executes the order of its tactics inside an existing simulator, MTDSim, as a Petri net that chooses its next tactic at runtime, mapping eight of the 15 tactics onto MTDSim's six attack actions (Section 4.4.1).

**After:** In answer to SQ2, the APT attacker model executes the order of its tactics inside an existing simulator, MTDSim, as a Petri net that chooses its next tactic at runtime. It maps eight of the 15 tactics onto MTDSim's six attack actions (Section 4.4.1).
Δ +1 · The participial tail adds a second idea, so split. "An existing simulator, MTDSim" stays because it echoes SQ2's wording.
**Mark:** ok / alt / keep / look —

### A2.6 · L8993 · §6.3 APT attacker model versus MTD attacker models · K3
> Three of them are Collection, Exfiltration and Impact, the tactics of actions on objectives, so objective-specific behaviour is in part.

**After:** Three of them are the tactics of actions on objectives, so objective-specific behaviour is in part.
Δ −4 · Third use of the same appositive (§5.2, §6.1). The reader has the names, and the verdict needs only the stage. This is the K3 move for a term the reader already has.
**Mark:** ok / alt / keep / look —

### A2.7 · L8994 · §6.3 APT attacker model versus MTD attacker models · K2
> MTDSim has no IDS, so the APT attacker model avoids detection only by proxy, through its tactic durations, and detection avoidance is in part.

**After:** MTDSim has no IDS, so the APT attacker model avoids detection only through its tactic durations. Detection avoidance is therefore in part.
Δ −2 · The verdict was appended after a stacked tail, so split. "Only through" carries "by proxy". Alt: keep "by proxy", as "…only by proxy, through its tactic durations. Detection avoidance is therefore in part." (Δ 0).
**Mark:** ok / alt / keep / look —

### A2.8 · L9052 · §6.4 Implications for MTD evaluation · K2
> An MTD evaluation should therefore test a learned deployment strategy against an attacker model other than the one it was trained against, beside the random deployment strategy over the same MTD mechanisms, which shows what the learning adds.

**After:** An MTD evaluation should therefore test a learned deployment strategy against an attacker model other than the one it was trained against. The random deployment strategy over the same MTD mechanisms shows what the learning adds.
Δ −2 · Two recommendations were stacked as tails. The second now heads its own sentence. Alt: "It should also run the random deployment strategy over the same MTD mechanisms to show what the learning adds." (+3), if the second sentence must keep "should".
**Mark:** ok / alt / keep / look —

### A2.9 · L9298 · §6.5 T3 · K2
> Only the APT attacker model has unmapped tactics, and at 200 s MTDShield chose to deploy nothing in 29 % of its decisions against it and 23 % against the baseline attacker, in 100 runs (Appendix D.1).

**After:** Only the APT attacker model has unmapped tactics. At 200 s MTDShield chose to deploy nothing in 29 % of its decisions against it and 23 % against the baseline attacker, in 100 runs (Appendix D.1).
Δ −1 · A premise and an observation were joined by ", and", so split (§4 rule 4). The sentence stays because it is the threat's evidence.
**Mark:** ok / alt / keep / look —

### A2.10 · L9361 · §6.5 T4 · K2
> To mitigate this threat, we also computed ASP reduction, and it orders the two layers as NCR reduction does, for both attackers, at every deployment interval (Table D.5).

**After:** To mitigate this threat, we also computed ASP reduction. For both attackers at every deployment interval, it orders the two layers as NCR reduction does (Table D.5).
Δ −1 · Two scope tails were stacked after the result. The scope moves to the head, and the agreement takes the stress. The mitigation formula is kept.
**Mark:** ok / alt / keep / look —

### A2.11 · L9458 · §6.5 T7 · K2
> The ablations are weaker evidence, as they compare many cells without correction, so some may cross Cohen's threshold for a negligible effect, ±0.2, by chance.

**After:** The ablations are weaker evidence. They compare many cells without correction, so some may cross Cohen's threshold for a negligible effect (±0.2) by chance.
Δ −1 · An as-clause, a so-clause and an appositive (four commas) become the claim, then its reason. The value moves into Marc's parenthesis.
**Mark:** ok / alt / keep / look —

### A2.12 · L9838 · §7.1 Contributions · K2
> The first contribution is an APT attacker model that any study using MTDSim can run in place of the baseline attacker, answering SQ1 and SQ2.

**After:** The first contribution answers SQ1 and SQ2. It is an APT attacker model that any study using MTDSim can run in place of the baseline attacker.
Δ +1 · A participial tail. The sentence now parallels L9870's "The second contribution answers SQ3.", and "baseline attacker" now meets the next sentence's.
**Mark:** ok / alt / keep / look —

### A2.13 · L9842 · §7.1 Contributions · K2
> Threat reports record the order of an attack's tactics, but not how long each took or what followed a failure, so the APT attacker model's timing and response to failure, where MTD disrupts it, rest on our judgement.

**After:** Threat reports record the order of an attack's tactics, but not how long each took or what followed a failure. The APT attacker model's timing and response to failure, where MTD disrupts it, therefore rest on our judgement.
Δ 0 · Four commas carried both cause and consequence, so split.
**Mark:** ok / alt / keep / look —

### A2.14 · L9845 · §7.1 Contributions · K2, K7
> In MTDSim, the APT attacker model uses a Petri net to choose its next tactic at runtime, and maps each tactic onto one of the baseline attacker's six attack actions, none of which models actions on objectives.

**After:** In MTDSim, the APT attacker model uses a Petri net to choose its next tactic at runtime. It maps eight of the 15 tactics onto the baseline attacker's six attack actions, none of which models actions on objectives.
Δ +1 · "Maps each tactic" overclaims, because seven tactics are unmapped (L8977, L8991). Split at ", and". The tail stays because the next sentence's "any objective-specific behaviour" rests on it.
**Mark:** ok / alt / keep / look —

### A2.15 · L10232 · C.2 The sources behind each attack flow's attack profile · K2
> The attacker of Mac Malware Steals Crypto stole credentials and mined cryptocurrency on the victims' machines, hijacking them, so it stole data and impeded systems [unit42maccookies2019].

**After:** The attacker of Mac Malware Steals Crypto stole credentials and hijacked the victims' machines to mine cryptocurrency, so it stole data and impeded systems [unit42maccookies2019].
Δ −1 · The participial "hijacking them" carried the evidence for "impeded". It becomes the verb.
**Mark:** ok / alt / keep / look —

### A2.16 · L10364 · D.1 MTDShield as run · K2
> MTDShield in Chapter 5 is the agent Tay scored highest in his hyperparameter evaluation [tay2024, Sect. 5.2], run as released, with his weights and input code [tay2024code].

**After:** MTDShield in Chapter 5 is the agent Tay scored highest in his hyperparameter evaluation [tay2024, Sect. 5.2]. It runs as released, with his weights and input code [tay2024code].
Δ +1 · The participial tail adds a second claim with its own citation. Now each sentence has one claim and one citation.
**Mark:** ok / alt / keep / look —

### A2.17 · L10397 · D.1 MTDShield as run · K2 kept, numeral
> As released, its evaluation code reads four of its eleven inputs before the run starts, so they are zero at every decision, as in Tay's own evaluations.

**After:** As released, its evaluation code reads four of its 11 inputs before the run starts, so they are zero at every decision, as in Tay's own evaluations.
Δ 0 · The tail is warranted because it is the fidelity fact. "Eleven" breaks the house rule of numerals above ten (an overlap fix).
**Mark:** ok / alt / keep / look —

### A2.18 · L10437 · D.3 MTD ranking against each attacker · K2
> Resampling seeds instead, with the APT attacker model's four attack profiles averaged at each seed, the host layer and the service layer remain apart at every deployment interval against both attackers; they are closest for the baseline attacker at 500 s, where the service layer leads by 0.11 (0.09, 0.12).

**After:** Resampling seeds instead, with the APT attacker model's four attack profiles averaged at each seed, keeps the host layer and the service layer apart at every deployment interval against both attackers. They are closest for the baseline attacker at 500 s, where the service layer leads by 0.11 (0.09, 0.12).
Δ 0 · "Resampling" dangled, because the layers do not resample. The gerund becomes the subject, with T7's verb ("keep … apart", L9455). The semicolon joined no opposition, so it becomes a full stop.
**Mark:** ok / alt / keep / look —

### A2.19 · L10616 · D.5.1 Ablation of the tactic durations · K2
> The APT attacker model runs again with no MTD, with only its tactic durations changed, in two steps (Table D.11).

**After:** With no MTD and only its tactic durations changed, the APT attacker model runs again in two steps (Table D.11).
Δ 0 · Three stacked tails. The conditions move to the head, and "two steps" takes the stress before "First… Then…" walks them.
**Mark:** ok / alt / keep / look —

### A2.20 · L10628 · D.5.1 Ablation of the tactic durations · K2, K3
> Under service diversity, the APT attacker model then spends 45 % of its time in scan neighbours, the attack action of Command and Control, and under IP shuffle, 79 % of its attack actions fail for missing preconditions.

**After:** Under service diversity, the APT attacker model then spends 45 % of its time in scan neighbours, the attack action of Command and Control. Under IP shuffle, 79 % of its attack actions fail for missing preconditions.
Δ −1 · Two results were joined across an appositive, so split. Alt: also drop the gloss (−8 in all), since §6.2 already says Command and Control runs scan neighbours.
**Mark:** ok / alt / keep / look —

---

## D. Words: figurative wording, term overload, needless definitions, unneeded content

**Rule.** Technical prose avoids metaphor and idiom (Zobel pp. 77, 115) and describes a concept "always … in the same way … not by a series of synonyms" (Zobel p. 117; ISO 704 §7.2). A term defined but barely used, and content the reader does not need, are cut (Zobel pp. 120, 174, 177, 196).

**The cluster-wide move.**
- (a) Swap a word only where a defined or registered term exists, at Δ ≤ 0. Pro: seamless, and each swap is checkable against terminology.md. Con: leaves plain idioms ("behind", "sit") in place.
- (b) Purge every flagged cue word. Pro: uniform. Con: most cues are literal ("answers the research question"), so it churns ratified prose for nothing.
- (c) Keep all. Pro: no risk. Con: leaves real term collisions (*stage*, *method*, *outcome*, *procedure*) that the registry already rules out.
- **Recommended:** (a). It fixes only what the registry or a defined term licenses, and the flags proved mostly false positives.

**Kept as warranted (44).**
- `L667` — "answers the research question" is literal.
- `L721` — SDR triad of parallel definitions. *Shuffle* is used throughout.
- `L729` — owned by calibration item 6. Table 2.2 reuses all three terms.
- `L797` — plain verb. The registry row itself says "sit in".
- `L799` — "deeper" is literal, given *levels of depth*.
- `L803` — *target host* is used about 10 times (the census undercounted).
- `L805` — *internal host* is used six times in Table 2.1.
- `L1235` — owned by calibration item 14 (delete).
- `L1236` — emphasis marks the name's words, kept after item 14.
- `L3961` — sections answer sub-questions: literal.
- `L3964` — literal, as for L3961.
- `L3965` — literal, as for L3961.
- `L4095` — plain idiom. No defined term replaces it.
- `L4211` — yes-or-no answers to the two questions: literal.
- `L4241` — "the answers" to those questions: literal.
- `L4281` — the evidence for "differ in actions on objectives".
- `L4418` — forward-referenced at L4108. Used three more times.
- `L4575` — "carry out" is literal. The next sentence echoes it.
- `L4926` — the reason one tactic is unmapped. The reader asks why.
- `L4927` — the reason, as for L4926.
- `L4928` — the reason, as for L4926.
- `L5123` — "behind" means "the source of". Plain idiom.
- `L5124` — motivates the failure matrix.
- `L5190` — "tell apart" is plain. No term exists.
- `L5357` — motivates the attacker behaviour metrics.
- `L5762` — literal.
- `L7623` — explains the low count of attack actions blocked.
- `L7628` — the result itself.
- `L8534` — *diversity pool* is a defined term (§4.4.4).
- `L8569` — literal.
- `L8579` — literal.
- `L8585` — literal.
- `L8633` — the attribution sentence. It carries the ablation result.
- `L8775` — literal.
- `L8957` — literal.
- `L9160` — the scope statement. It carries the design bounds.
- `L9293` — the threat's own content.
- `L9870` — a contribution answers a sub-question. Standard.
- `L9926` — `\emph` run-in item label. Not a definition.
- `L9939` — run-in item label, as for L9926.
- `L9961` — run-in item label, as for L9926.
- `L10100` — plain idiom. "Predicates behind each mark" is clear.
- `L10179` — plain idiom, as for L10100.
- `L10405` — disclosure ruled "that's fine" (2026-10-15).

**Proposals (8).**

### D.1 · L941 · Baseline attacker · K6
> It follows a fixed procedure of six *attack actions*, modelled on the Cyber Kill Chain [brown2023, hutchins2011]: it scans for hosts, …

**After:** It follows a fixed sequence of six *attack actions*, modelled on the Cyber Kill Chain [brown2023, hutchins2011]: it scans for hosts, …
Δ 0 · *Procedure* is ATT&CK's defined term ("one recorded instance of a technique", §3.1.2), and the registry lists it as a watched variant. Here it means only a fixed order.
**Mark:** ok / alt / keep / look —

### D.2 · L2183 · MTD modelling approaches · K6
> An MTD modelling approach is a method for finding an optimal deployment strategy.

**After:** An MTD modelling approach finds an optimal deployment strategy.
Δ −4 · The registry rules that an approach is not a *method*, which is reserved for §3.2.3's *evaluation method*. Alt: "searches for" (Δ −3) if "finds" claims too much.
**Mark:** ok / alt / keep / look —

### D.3 · L3469, L3474, L3485 · Recent MTD attacker models · K6
> Their attacker model is an automated attack script that runs four stages in a fixed order: …
> … each attack runs all four stages, but in one short attempt, …
> … every attack follows one attack scenario, in the same four stages.

**After:** *stages* → *steps* at all three sites ("runs four steps in a fixed order", "runs all four steps", "in the same four steps").
Δ 0 · *The four stages* is the registered name for §3.1.1's lifecycle (preparation to actions on objectives), and Figure 4.2 groups the tactics by it. Kim's four script steps are a different object.
**Mark:** ok / alt / keep / look —

### D.4 · L4036 · Attack graph from attack flows · K4
> Each technique in an attack flow stands for its tactic, and a technique listed under several tactics stands for the leftmost of them in the ATT&CK matrix.

**After:** Each technique in an attack flow counts as its tactic, and a technique listed under several tactics counts as the leftmost of them in the ATT&CK matrix.
Δ 0 · "Stands for" is figurative, the same instance as calibration item 14. The aggregation literally counts each technique as its tactic.
**Mark:** ok / alt / keep / look —

### D.5 · L4360 · Petri-net formalism · K6
> A timed transition models the time the attacker spends on a tactic, and an immediate transition models its choice of the next tactic.

**After:** A timed transition models the tactic duration, and an immediate transition models the attacker's choice of the next tactic.
Δ −5 · Chapter 4 phrases one concept three ways: time spent "within" (L4042), "on" (here) and "in" (L4394) a tactic. *Tactic duration* is the registered term, already used at L4042.
**Mark:** ok / alt / keep / look —

### D.6 · L4365 · Petri-net formalism · K4
> Tokens sit on places.

**After:** Places hold tokens.
Δ −1 · The next sentence says "each of its input places holds a token". One verb now serves both sentences.
**Mark:** ok / alt / keep / look —

### D.7 · L4394 · merged into C.28

### D.8 · L4436 · Petri-net formalism · K6
> Each attack action the APT attacker model runs in MTDSim succeeds or fails; this outcome is the attack action's *verdict* (Section 4.4).

**After:** The *verdict* of each attack action the APT attacker model runs in MTDSim is success or failure (Section 4.4).
Δ −3 · *Outcome* collides with *attack outcome*, §4.5.2's metric group. The term now opens its own copula definition, and the semicolon goes.
**Mark:** ok / alt / keep / look —
