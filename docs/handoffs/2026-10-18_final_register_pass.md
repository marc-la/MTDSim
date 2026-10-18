---
status: open
created: 2026-10-18
---

# Final register pass: clausing, flourish and float text, ruled line by line

**Goal.** Remove the AI-redraft shapes Marc found in pages i–15 from the whole dissertation by minimal, seamless edits. Each edit is proposed side by side and ruled by Marc before it touches the tex.

## State of play

- **The standard exists.** [`../workflows/clausing_check.md`](../workflows/clausing_check.md) sorts the defects into eight classes, K1–K8, each grounded in style authority and, where it exists, in measured LLM-text evidence. It also sets the seamless-edit rules (§4).
- **The census exists.** [`../../tools/clause_census.py`](../../tools/clause_census.py) `rates` measures the dissertation against 20 pre-2023 field papers, and `flags` lists the units to read. Its findings are in the standard's §3. The defect is real but concentrated: chapters 2 and 3, the captions, and the appendix headings.
- **Calibration ledger (below), not yet ruled.** It holds Marc's 19 items from pages iv–15, each with a proposal. Ruling it first tests the standard on the cases that produced it, before the session extrapolates.
- **Extrapolation done (2026-10-18), not ruled.** [`../../data/clausing_check/ruling_file.md`](../../data/clausing_check/ruling_file.md) has 136 proposals in five clusters: F captions and headings, C colons, A1 and A2 comma jobs, D words. Each cluster has its rule, a cluster-wide move with options, its kept rows and their warrants, and per-item marks.
  - Every unit of the dissertation was assigned to exactly one cluster by the census thresholds (`clause_census.py worklist`, standard §5), and one agent judged each cluster.
  - Cluster C was re-judged under a stricter amplification test after a spot check found the "amplification" warrant over-used.
- **Known tool gaps,** to fix before any re-run:
  - the worklist misses captions whose short form wraps a line;
  - the calibration heading pattern also drops §5.3.1–5.3.2 and §5.4, because they share their wording with Appendix D.

  Cluster F covered both by reading.

## Order of work

1. **Marc rules the calibration ledger, then the ruling file cluster by cluster.** Where a ruling disagrees with the standard, the standard changes first (rule on merit).
2. **Headings and captions, all chapters.** Read every one in full, whatever the flags say: they are where an examiner forms a judgement first, and where Marc's worst finds sat. Then:
   - chapters 2–3 (colon rate two to three times the field);
   - chapter 4 and the appendices;
   - chapters 1 and 5–7, which are near the field on colons, so the work there is mostly K2 and K3.
3. **One ledger per tranche,** in the calibration ledger's format, appended to this handoff or written beside it as `2026-10-18_final_register_pass_<tranche>.md`.
4. **Apply the ruled items, rebuild, re-run `rates`, count words.** Report the delta against the 15 000 ±10 % band.

## Hard constraints

- **Every item is proposed.** Marc rules each one, in every chapter. This overrides the ch6/appendix auto-apply rule for this pass only, at Marc's request (2026-10-18).
- **Seamless editing** (standard §4). Rearrange the sentence's own words first. The word delta is zero or negative where possible. No new terms, and no added commas.
- **A float label changes in its generator** (`tools/`), never in the PDF.
- **Concurrent sessions** are committing to this branch: re-read each passage at HEAD before applying.

## Reading list

1. [`../workflows/clausing_check.md`](../workflows/clausing_check.md): the standard.
2. [`../workflows/voice.md`](../workflows/voice.md) §0, §d and §h: what must survive (paired opposition, the parenthesis).
3. [`../workflows/academic_register.md`](../workflows/academic_register.md) §i: the term screen (K5–K7 overlap it).
4. [`../workflows/terminology.md`](../workflows/terminology.md): the one-term registry that every *after* must use.
5. This ledger's rulings, once made: the calibration set for every later tranche.

---

## Calibration ledger: Marc's pages iv–15

Each item gives the location, the class (standard §1), the text before and after, the word delta, and why. Marks: **ok** (apply), **alt** (apply the named alternative), **keep** (leave as is), **look** (discuss).

### 1. §3.3.1 heading (p. iv), K5 long heading

> Properties an MTD attacker model needs to model an APT attacker

**After:** `Properties of an APT attacker` (−6)

- The section's first sentence already says the properties are what an MTD attacker model needs, so the heading only has to name the topic. It keeps "APT" visible, as the heading conventions require.
- Alt (a): `Properties an MTD attacker model needs` (−5). It keeps the requirement framing but drops APT.
- Table 3.2's short caption repeats the long form ("The eight properties an MTD attacker model needs to model an APT attacker"). Mirror the change there: `The eight properties of an APT attacker`.

**Mark:** ok / alt / keep / look —

### 2. §6.3 heading (p. v), K5 unqualified head noun

> APT attacker model versus MTD attacker models

**After:** `APT attacker model versus recent MTD attacker models` (+1)

- The APT attacker model is itself an MTD attacker model, so the bare plural does not name the comparison.
- "Recent MTD attacker models" is §3.3.2's heading and Table 3.3's subject, the set §6.3 compares against, verbatim.

**Mark:** ok / alt / keep / look —

### 3. Appendix B title (p. v), K5 unqualified head noun

> Predicate tests of the attacker models

**After:** `Predicate tests of the MTD attacker models` (+1)

- The table tests four MTD attacker models: the baseline attacker, Masud et al., Kim et al. and the APT attacker model.
- Bare "attacker models" invites the reader to ask which ones.

**Mark:** ok / alt / keep / look —

### 4. Appendix C section titles (p. v), K4 narrative wording and K5 a non-parallel set

| | Before | After | Δ |
|---|---|---|---|
| C.1 | The attack graph with techniques as nodes | Attack graph with techniques as nodes | −1 |
| C.2 | The sources behind each attack flow's attack profile | Sources for each attack flow's objective | −3 |
| C.3 | Edges of the attack profiles | *(keep)* | 0 |
| C.4 | Tactic durations against the baseline attacker's times | Tactic durations and attack action times | −2 |
| C.5 | The rules and the distance factor of the failure matrix | Failure matrix rules and distance factor | −4 |
| C.6 | Where each value of the APT attacker model comes from | Sources of the APT attacker model's values | −3 |

- **The set's form.** Each title is one noun phrase naming the object the section gives, with no leading article. C.3 already has that form.
- **C.2.** The table answers §4.2's two questions (stole data? impeded systems?) for each attack flow, which is the attack flow's objective. "Behind each attack flow's attack profile" stacks two of our terms on a vague preposition.
- **C.4.** "Against" read as a contest, but the table sets two times side by side.
- **C.6.** "Where … comes from" is the narrative form of "sources".

**Mark:** ok / alt / keep / look —

### 5. Appendix D section titles (p. v), K5 vague purpose

| | Before | After | Δ |
|---|---|---|---|
| D.1 | MTDShield as run | MTDShield's settings | 0 |
| D.2 | Disruption per MTD deployment | Values of time lost per MTD deployment | +3 |
| D.3 | MTD ranking against each attacker | Values of the MTD ranking | −1 |
| D.4 | Sensitivity analysis of the tactic durations | *(keep)* | 0 |
| D.5 | Ablation studies | Ablation study tables | +1 |
| D.5.1 | Ablation of the tactic durations | *(keep)* | 0 |

- **D.1.** The section's table is "MTDShield's settings", so the title names what the table holds.
- **D.2, D.3 and D.5.** These titles repeat chapter 5's section names, so they do not say that the appendix holds the *values* behind chapter 5's figures. "Time lost per MTD deployment" is the metric's defined name. "Disruption" was a looser synonym, a K6 drift.
- **What the set does.** Each title names the object the appendix gives, as Appendix C's do once they are fixed.

**Mark:** ok / alt / keep / look —

### 6. §2.1 ¶1, l.723–726 (p. 3), K6 term overload

> When to move is set by the trigger. A *proactive* MTD moves on a schedule; a *reactive* MTD moves in response to an event, such as an intrusion alert; a *hybrid* MTD adapts its schedule to such events while bounding the time between moves [cho2020].

**After:**

> When to move makes an MTD *proactive*, *reactive* or *hybrid* [cho2020]. A proactive MTD moves on a schedule, and a reactive MTD moves on an intrusion alert. A hybrid MTD adapts its schedule to such alerts, up to a maximum time between moves [cho2020].

Δ −4.

- **What changes.**
  - "Trigger" goes: it is used once in the prose and once as Table 2.2's column header, and never defined.
  - "Event" and "alert" become one term.
  - The two semicolons become full stops.
- **Accuracy.** Cho's hybrid definition holds: an interval "adaptive upon certain events or security alerts while the interval is also bounded" (Cho et al. 2020, §II-B). §2.2.2's "within a bound, so it is hybrid" still reads against it.
- **Ripple:** Table 2.2's column header `Trigger` becomes `When to move`.

**Mark:** ok / alt / keep / look —

### 7. Figure 2.1 caption (p. 3), K5 compressed caption

> The three modules of MTDSim and how each acts on the others.

**After:**

> The three modules of MTDSim. MTD reconfigures the network and disrupts the attacker. The attacker observes the network and compromises its hosts.

Δ +9.

- The caption now says, in the figure's own arrow labels, what "how each acts on the others" compressed.
- **Alternative (a):** cut to `The three modules of MTDSim.` (−7). The arrows are already labelled, so nothing is left undecoded.
- (a) is cheaper. The recommendation reads alone without the body text.

**Mark:** ok / alt / keep / look —

### 8. Figure 2.2 caption and one label (p. 4), K4 narrative wording and K2 appended clauses

> The network, and one host in it. (a) The attacker enters at the exposed endpoints and works deeper, level by level, towards the target hosts; red marks its route and the hosts it has compromised. (b) What a host holds, and the MTD mechanism that reconfigures each part.

**After:**

> The host layer and one host. (a) The hosts in four levels of depth, from the exposed endpoints to the target hosts. Red marks the attacker's route and the hosts it has compromised. (b) The parts of one host, each beside the MTD mechanism that reconfigures it.

Δ −3.

- **What changes.**
  - "Works deeper, level by level" tells the panel as a story; *levels of depth* is §2.2.1's defined term.
  - The semicolon becomes a full stop.
  - (b)'s appended "and the MTD mechanism…" becomes the sentence's head.
- **The label.** The figure's own arrow label "deeper into the network" should go too, because the levels are already labelled 1–4. That is an edit in the generator (`tools/ch2_fig22_network_model.html`), then a re-render.
- **The short caption.** `The host layer and one host`, the figure's own title.

**Mark:** ok / alt / keep / look —

### 9. Table 2.1 caption (p. 5), K4 figurative wording and K2 appended clause

> The seven MTD mechanisms, from the pool of Brown [brown2023], by the part of the network each reconfigures.

**After:** `The seven MTD mechanisms of MTDSim and what each reconfigures [brown2023].` (−6)

- **What changes.**
  - "The pool of Brown" is figurative: it is a code word, and it reads as Brown's possession.
  - "By the part of the network each reconfigures" was an appended phrase. The table's column header ("What it reconfigures") and its row groups (host layer, service layer, credentials) already show it.
- The caption is now one clause in the table's own words.

**Mark:** ok / alt / keep / look —

### 10. §2.2.1 *impact*, l.806–808 (p. 5), K7 needless definition and K3 appositive

> …and an *impact*, the damage a successful exploit does [brown2023].

**After:** `…and an impact score for the damage a successful exploit does [brown2023].` (+1)

- *Impact* is used twice more, both in chapter 2 (the compromise threshold, and return on attack), so the reader needs the word.
- It does not need the emphasis that marks a term the dissertation will keep using.
- The appositive becomes a plain noun phrase.
- Alt (a): keep as is. The emphasis is defensible because it is used again within the page.

**Mark:** ok / alt / keep / look —

### 11. Table 2.2 caption (p. 6), K3 appositive and K1 colon

> The four deployment strategies: three from Zhang [zhang2023] and MTDShield, the reinforcement-learning agent of Tay [tay2024].

**After:** `The three deployment strategies of Zhang [zhang2023] and Tay's MTDShield [tay2024].` (−6)

- The colon and the appositive go.
- MTDShield is defined in the body two lines above as a reinforcement-learning agent, and the table's row says what it deploys.

**Mark:** ok / alt / keep / look —

### 12. Table 2.3 caption (p. 6), K2 appended clause. Extrapolated: not on Marc's list

> The two attack scenarios of the baseline attacker [brown2023], by the attacker's goal.

**After:** `The two attack scenarios of the baseline attacker and the goal of each [brown2023].` (+1)

- It is the same shape as item 9. Alt (a): cut ", by the attacker's goal" (−4), since the column header says "Goal".

**Mark:** ok / alt / keep / look —

### 13. Table 2.4 caption (p. 7), K8 content the reader does not need

> The configurations the earlier MTDSim studies ran. Times are in seconds; a dash marks a value the study does not state. Tay [tay2024] states none.

**After:** delete `Tay [tay2024] states none.` (−4)

- The sentence explains why a study is absent from the table, which no reader asks.
- **Risk.** Tay is then cited nowhere in this float. That is fine, because §2.2.2 cites Tay for MTDShield.
- The generator is `tools/ch2_lineage_configurations_table.py`. Edit there, then regenerate.

**Mark:** ok / alt / keep / look —

### 14. §3.1.1, l.1229 (p. 8), K7 overclaimed mapping

> Each word of the name stands for one property.

**After:** delete. (−9)

- The claim is not true of the text that follows. It walks four properties (advanced, persistent, low and slow, threat), and "low and slow" is not a word of the name.
- The definition sentence before and *It is advanced…* after join without it.

**Mark:** ok / alt / keep / look —

### 15. Figure 3.1 caption (p. 9), K4 figurative wording

> The MITRE ATT&CK Enterprise matrix (v19.1), with the Initial Access tactic opened down to a Volt Typhoon procedure [mitre2026attackkb].

**After:**

> The MITRE ATT&CK Enterprise matrix (v19.1), and the technique, sub-technique and Volt Typhoon procedure below its Initial Access tactic [mitre2026attackkb].

Δ +2.

- "Opened down to" is a user-interface metaphor.
- The hierarchy's own four terms were defined in the paragraph above.

**Mark:** ok / alt / keep / look —

### 16. §3.1.3 ¶1, l.1593–1596 (p. 9), K3 appositive

> The product of attack profiling, an *attack profile*, can be executed as an attacker in a simulation; Chapter 4 builds its APT attacker model on attack profiles.

**After:**

> Attack profiling produces an *attack profile*. An attack profile can be executed as an attacker in a simulation, and Chapter 4 builds its APT attacker model on attack profiles.

Δ −2.

- The term is defined in a sentence of its own, with no appositive and no semicolon.
- "Attack profile" is then repeated rather than referred back to: repetition beats vagueness.

**Mark:** ok / alt / keep / look —

### 17. §3.1.3 ¶3, l.1706–1709 (p. 10), K3 appositive and the leading order

> This dissertation uses manual attack profiling, with Attack Flow, a language from MITRE's Center for Threat-Informed Defense (CTID) for recording the order of an incident's techniques [ctid2025attackflow].

**After:**

> This dissertation uses manual attack profiling in Attack Flow [ctid2025attackflow]. Attack Flow is a language from MITRE's Center for Threat-Informed Defense (CTID) that records the order of an incident's techniques.

Δ 0.

- The sentence now leads with the choice (manual attack profiling). The definition follows as a copula sentence.
- The definition had been an appositive nested inside a *with* phrase, and the fix takes it out.

**Mark:** ok / alt / keep / look —

### 18. §3.2.1 ¶2, l.2195–2197 (p. 11), K1 colon hinge

> Its attacker is the attacker model its training environment simulates [tay2024, ho2024]: MTDShield's is the baseline attacker of Section 2.2.3 [tay2024].

**After:**

> Its attacker is the attacker model its training environment simulates [tay2024, ho2024]. MTDShield was trained against the baseline attacker (Section 2.2.3) [tay2024].

Δ +1.

- The colon joined a general claim to its instance. The elliptical "MTDShield's is" made the reader carry "attacker" across the colon.
- Two plain sentences replace it.

**Mark:** ok / alt / keep / look —

### 19. §3.4 ¶1, l.3578 (p. 15), K1 calibration: a colon kept

> An MTD evaluation's result depends on its attacker model: the attacker model decides which deployment strategy is optimal (Section 3.2.1) and how effective MTD is (Section 3.2.2).

**After:** keep.

- The colon introduces the two reasons the claim rests on. That is the use every style authority licenses, the amplification of what precedes it.
- Marc read it as acceptable. It is in the ledger as the reference case for a *warranted* colon.

**Mark:** ok / alt / keep / look —

### Ledger total

The 19 items come to about −34 words if every recommendation is taken, or about −50 with item 7's alternative.
