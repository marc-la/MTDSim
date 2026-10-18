# A: claims and self-scoring (items 1, 6, 7)

> **Marc's rulings (2026-10-18, round 1).**
> - Item 1: Rec. accepted (verb kept, object changed), in 1a, 1b and 1c alike. Reason: "is not enough to show" is about evidence and holds whether or not a ranking transfers; "may not show" predicts an outcome and stacks a second hedge.
> - Item 6: 6a, 6b, 6c, 6f, 6g, 6h and 6i accepted. **6d revised** to move "in part" off the sentence end: "That order gives it two properties in part, choice of attack strategy and objective-specific behaviour (Table~\ref{tab:fidelity-verdict})." **6e revised** to Marc's simplification, parallel to the adaptivity sentence: "The Petri net's draw of its next tactic, at random in proportion to the edge weights, is also a fixed rule of ours, so choice of attack strategy is in part." It keeps ¶3's "so … is in part" ending, which every mark sentence in ¶3 shares.
> - Item 7: accepted.
> - **Awaiting Marc's confirmation of the 6d and 6e revisions.**

> **Reviewer notes (main session, 2026-10-18).** Two choices for Marc; everything else is ready to apply as drafted.
> 1. **Item 1's verb.** The sheet keeps your ratified "is not enough to show" and changes only its object, to "a single attacker model … other attackers". Jin's example uses "may (therefore) not show". The sheet argues the stacked hedge: you cut "may not" from this exact ch7 sentence on 2026-10-15. Jin called his wording an example, so either version answers him: what he objected to was the object. **Recommend the sheet's Rec.**
> 2. **6e's wording.** "Chooses its next tactic by a fixed rule of ours, at random" puts "chooses" and "at random" in one clause. A tighter option keeps §6.1's words and the parallel with the adaptivity sentence: **"The Petri net draws its next tactic at random, in proportion to the edge weights, also a fixed rule of ours, so choice of attack strategy is in part."** (+25, against +29). **Recommend this.**
>
> Word count: the sheet treats the appendices as outside the band (tex l.175–177), so item 7 costs nothing.

**The rule.** *Purpose:* an examiner reads the claims first, then the self-score, and checks that each one says no more than the evidence does. Item 1 takes out a causal overclaim, item 6 takes out an inflated mark, and item 7 takes out a misdescribed method. *Context:* the evidence is the current tex at `74033db9` (re-read on 2026-10-18; the file is unchanged since `1ec65b22`), Table 6.1 and Table B.1, `apt_model_criterion.md` l.340–366 ("variety, not strategy"), and the register's scoping. *Audience:* the examiner, through ch1's contributions, §6.3–§6.4, ch7's preamble and contribution 1, and Appendix B. A fourth-year student reads the same lines as the dissertation's claims. **Gate:** ch1, ch4 and ch7 are **PROPOSE**; ch6 and Appendix B are **APPLY ON RULING**.

---

## Item 1: the abstract's claim in three places (ruled: do it)

The abstract's claim is "These results make a case for testing MTD against more than one attacker model" (l.228–229). The three sentences below should say that claim, word for word with each other. The abstract keeps its recommendation form, and ch1 ¶3's cited "far simpler than an APT" (l.312) stays, because it states the field's gap.

| # | Location (section, tex line) | Before | After | Why | Risk |
|---|---|---|---|---|---|
| 1a | Ch1 contribution 2 (l.597–600). **PROPOSE** | We find that, in MTDSim, the most effective MTD mechanism depends on the attacker model, so an evaluation against an attacker model far simpler than an APT is not enough to show how MTD performs against APT attackers. | **Rec.:** …depends on the attacker model, so an evaluation against **a single attacker model** is not enough to show how MTD performs against **other attackers**.<br>**Alt. (register / Jin):** …so an evaluation against a single attacker model **may not show** how MTD performs against other attackers. | Jin's objection is the *object* of the sentence. "Far simpler than an APT … APT attackers" says that APT-ness causes the difference, and a comparison of two attacker models cannot show that. Both versions fix the object. The Rec. keeps Marc's ratified verb, "is not enough to show", for three reasons. (1) In §6.4 and ch7 the sentence before it already says "can therefore depend", so "may not" would put two modals in consecutive sentences. Marc cut "may not" from this ch7 preamble on 2026-10-15 as "a second hedge" (tex comment l.9733–9736). (2) §6.4's comment (l.8962–8966) defines the sentence as the evidence reading: an evaluation against one attacker model carries no evidence that its ranking holds for another. It says the house "may" does not apply to that reading. (3) "A single … is not enough" is the abstract's "more than one attacker model" stated as a finding. | The Rec. departs from Jin's verb, though not from his object. If Marc wants Jin's words exactly, take the Alt. in all three places. The ring with ch1 ¶3 now closes on P3's second clause, "how well MTD performs depends on the attacker it faces [hong2018]", not on "far simpler than an APT". That is the clause the finding actually tests. Update the provenance comment at l.591–596. |
| 1b | §6.4 ¶1, last sentence (l.8960–8961). **APPLY ON RULING** | An evaluation against an attacker model far simpler than an APT is not enough to show how MTD performs against APT attackers. | **Rec.:** An evaluation against **a single attacker model** is not enough to show how MTD performs against **other attackers**.<br>**Alt.:** An evaluation against a single attacker model may not show how MTD performs against other attackers. | Same as 1a. Jin's "therefore" is dropped in both versions, because the sentence before already has one. | The next sentence opens "This section says what that means…". "That" still refers back cleanly. §6.4 ¶2 already uses "generalises to other attackers" (l.8994), so the term is the thesis's own. |
| 1c | Ch7 preamble, last sentence (l.9743–9746). **PROPOSE** | An evaluation against an attacker model far simpler than an APT is not enough to show how MTD performs against APT attackers. | **Rec.:** identical to 1b.<br>**Alt.:** identical to 1b's Alt. | The preamble answers the research question in sentences 2–4; sentence 5 states what the answer means. "How MTD performs against other attackers" repeats the research question's own frame ("how MTD performs against APT attackers"), so the close still points back to the question. | The ch7 preamble is verbatim with ch1 contribution 2, by design (validation gate). That is a conscious exception to conclusion_conventions (d1)'s "repeats chapter 1" test, and it is unchanged from today. Update the comment at l.9731–9736. |

## Item 6: choice of attack strategy, full → in part (ruled: downgrade)

**This overturns** the 2026-10-08 ruling (handoff 2026-10-07 §12b: "the full mark on choice of attack strategy is KEPT"; §13a.5). It is overturned on merit. The predicate is "chooses among several sequences of techniques toward the same objective". The threat reports give the APT attacker model those sequences. But the Petri net picks among them "at random, in proportion to the edge weights" (§6.1, l.8645–8647). Table B.1 calls that a fixed rule its authors set, which is exactly what its *rule* cell means. The same holds for adaptivity, which is already "in part". The criterion's own badge says "variety, not strategy". The new reason uses the "fixed rule" wording that ch3 gives for the baseline attacker's in-part mark on the same property ("a fixed rule sets the order in which it tries them", l.3390). Marc's 2026-10-08 point was that the sequences are "an aggregate of documented behaviour". That point survives: ¶2 still credits the order to the threat reports, and only the draw is ours.

The counts after the change come from Table 6.1. The APT attacker model has 1 property in full (persistence) and 4 in part (2, 3, 4, 5). The baseline attacker has 1 in full and 2 in part, Masud et al. 0 and 1, and Kim et al. 0 and 2. The APT attacker model's mark is still at least every other model's mark on every property, so "more of the eight properties" still holds.

| # | Location (section, tex line) | Before | After | Why | Risk |
|---|---|---|---|---|---|
| 6a | Table B.1 row 3 (l.10061–10062). **APPLY ON RULING** | `\emph{3 Choice of attack strategy} & \propstandin & \propnone & \propnone & \propmet \\`<br>`… toward the same objective & rule & no & no & yes \\` | `… & \propstandin & \propnone & \propnone & **\propstandin** \\`<br>`… toward the same objective & rule & no & no & **rule** \\` | The caption defines *rule* as "only a fixed rule its authors set makes it true" (l.10042–10044). The weighted draw is our rule, as the failure matrix is in row 4, which is already *rule*. The caption's mark rule then gives \propstandin. | None; the caption needs no change. |
| 6b | Table 6.1, APT attacker model row (l.8874). **APPLY ON RULING** | `& 2026 & \propmet & \propstandin & \propmet & \propstandin & \propstandin & \propnone & \propnone & \propnone \\` | `& 2026 & \propmet & \propstandin & **\propstandin** & \propstandin & \propstandin & \propnone & \propnone & \propnone \\` plus one comment line: `% [2026-10-18, Marc: 3 tick -> in part (supervisor item 6): the Petri net's draw is a fixed rule of ours, Table B.1 "rule"; overturns 2026-10-08 §12b.]` | Must agree with Table B.1. | The SYNC comment concerns Table 3.3's three prior rows. Table 3.3 has no APT attacker model row, so nothing needs re-copying. |
| 6c | §6.3 ¶1, sentence 2 (l.8896–8898). **APPLY ON RULING** | It is the only attacker model with choice of attack strategy in full or with any objective-specific behaviour, which it has in part. | It is the only attacker model with any objective-specific behaviour, which it has in part. | Its first "only" fact is no longer true: the baseline attacker also has choice of attack strategy in part. The second fact still stands. | ¶1 now carries one "only" fact beside "more of the eight properties". That is still true and still first. |
| 6d | §6.3 ¶2, sentence 2 (l.8907–8909). **APPLY ON RULING** | That order gives it choice of attack strategy in full and objective-specific behaviour in part (Table~\ref{tab:fidelity-verdict}). | That order gives it choice of attack strategy **and objective-specific behaviour, both in part** (Table~\ref{tab:fidelity-verdict}). | The answer to SQ1 keeps its logic: the threat reports give the order, and the order gives both properties. ¶2 has never explained objective-specific behaviour's "in part"; ¶3 does. After 6e, ¶3 explains choice of attack strategy too, so the two read alike and nothing turns back. | ¶2 now credits the threat reports with two partial marks, not one full mark. Its last sentence, "grounded in threat reports for the order of its tactics", still stands. |
| 6e | §6.3 ¶3, after the adaptivity sentence (after l.8937 "…adaptivity is in part (Table~\ref{tab:fidelity-verdict})."). **APPLY ON RULING** | *(no sentence)* | **Rec.:** **The Petri net also chooses its next tactic by a fixed rule of ours, at random in proportion to the edge weights, so choice of attack strategy is in part.**<br>**Alt.:** …by a fixed rule of ours, **in proportion to the share of attack flows that take it**, so choice of attack strategy is in part. | This is the reason for mark 3 that the register asks for. It sits beside adaptivity's reason because both are "a fixed rule of ours". "Chooses" repeats the paragraph opener's "a Petri net that chooses its next tactic at runtime". It says the choice is ours, so the opener and this sentence agree. "At random, in proportion to the edge weights" repeats §6.1 (l.8645–8647) word for word. The Alt. leads with the threat-report grounding (T5's "share of attack flows that draw it", l.9327), which answers Marc's 2026-10-08 concern that "a random draw" undersells the corpus. It costs the verbatim repeat of §6.1. | +29 words, the largest cost in item 6. The paragraph's mark order becomes 1, 4, 3, 2, 5, which is acceptable because the marks are grouped by cause. "Edge weights" is §6.1's term; ch4's defined term is "base weight", and after a failure the weights are scaled by the failure matrix, so "edge weights" is the accurate cover term. |
| 6f | Appendix B ¶2 (l.10031–10032). **APPLY ON RULING** | Distinct openings (Equation~\ref{eq:apv}) backs the APT attacker model's full mark for choice of attack strategy (Section~\ref{sec:disc-behaviour}). | Distinct openings (Equation~\ref{eq:apv}) backs the APT attacker model's mark for choice of attack strategy (Section~\ref{sec:disc-behaviour}). | Delete "full". Distinct openings shows that the behaviour holds (several sequences). It does not show who chooses among them. Table B.1, directly below, shows *rule*. | None. The recount sentence is unchanged. |
| 6g | Ch1 contribution 1 (l.587–590). **PROPOSE** | Of eight properties an attacker model needs to model an APT attacker, the APT attacker model has two in full and three in part; three recent attacker models have at most one in full. | …the APT attacker model has **one in full and four in part**; three recent attacker models have at most one in full **and two in part**. | With the old ending, "at most one in full", the APT attacker model would now tie the field on full marks, and the contrast would vanish. Adding "and two in part" shows the actual gap: 5 properties against at most 3 (the baseline attacker's 1 + 2). | The numbers must agree with Table 6.1 and the ch4 opener (6h). +4 words. |
| 6h | Ch4 opener (l.3930). **PROPOSE** | …they also cap what it gains, so it has two properties in full and three in part (Section~\ref{sec:fidelity-verdict}). | …they also cap what it gains, so it has **one property in full and four in part** (Section~\ref{sec:fidelity-verdict}). | The count changes and nothing else. The one property in full is the persistence the sentence before says it keeps. | Before and after, the "so" credits every in-part mark to the attack actions' cap. Adaptivity's and choice of attack strategy's in-part marks come from our rules, not the cap. The old wording was equally loose, and §6.3 gives the exact causes, so it is not re-opened here. 0 words. |
| 6i | Ch7 contribution 1, last sentence (l.9776–9779). **PROPOSE** | Of the four attacker models in Table~\ref{tab:fidelity-verdict}, it is the only one with choice of attack strategy in full, and the only one with any objective-specific behaviour. | **Rec.:** Of the four attacker models in Table~\ref{tab:fidelity-verdict}, it is the only one with any objective-specific behaviour.<br>**Alt.:** …it has the most of the eight properties, and is the only one with any objective-specific behaviour. | The sentence traces to §6.3 ¶1 (6c), which keeps one "only" fact. The Rec. cuts the false fact and adds nothing. The Alt. brings back §6.3 ¶1's count verdict, which Marc reverted on 2026-10-15 in favour of naming the properties (comment l.9763–9765). It is offered only because the evidence is now one fact. | With the Rec., the contribution's evidence is one fact. Its bound, "none of which models actions on objectives", is already in the sentence before, so the paragraph still closes on the bound. −11 words (Rec.), −3 (Alt.). |

## Item 7: "word for word" in Appendix B (ruled: ratify recommendation)

Checked against Table 3.2 (l.3073–3082) and Table B.1 (l.10055–10070):
- Rows 3, 4, 7 and 8 are Table 3.2's definitions word for word.
- Row 2 drops the example "such as exfiltration or impediment".
- Row 6's split rewords "each technique … its cost … its benefit" as "techniques … their cost … their benefit", with the qualifier "for each technique". The meaning is unchanged.
- Row 5 splits at "and", drops "such as passive reconnaissance", shortens "intrusion detection system (IDS)" to "IDS", and **adds "slower than the baseline attacker"**.
- Row 1 splits off "over an extended period" as its qualifier and **adds "until it reaches its objective, however many MTD deployments that takes"**.

The two additions are the only changes in meaning. Row 1's addition decides Masud et al.'s qualifier cell: its attack paths are computed afresh every interval (l.3418–3419).

| # | Location (section, tex line) | Before | After | Why | Risk |
|---|---|---|---|---|---|
| 7 | Appendix B ¶1, last sentence (l.10027–10029). **APPLY ON RULING** | The predicates are Table~\ref{tab:attacker-properties}'s definitions word for word; rows 1 and 6 split off a qualifier, row 5 splits at its ``and''. | The predicates are Table~\ref{tab:attacker-properties}'s definitions; rows 1 and 6 split off a qualifier, row 5 splits at its ``and''. **To make ``over an extended period'' and ``low and slow'' testable, row 1 adds ``until it reaches its objective, however many MTD deployments that takes'', and row 5 adds ``slower than the baseline attacker''.** | This is what Jin asked for: say that the words were added to make "low and slow" testable. The same reason, and the same disclosure, covers row 1's addition. The added sentence opens on its purpose, and it quotes the added words so that the examiner can find them in the table directly below. The register's Rec. paraphrased row 1 ("carries on however many MTD deployments it takes"). Here it is quoted, because a paraphrase of a predicate is the kind of mismatch this item fixes. | Appendix words are outside the word count (tex comment l.175–177), so the +33 words here cost nothing in the band. The first sentence keeps Marc's comma form, "…a qualifier, row 5 splits…". |

---

## In place

Changed words are in **bold**. ~~Struck~~ words are the ones cut, shown only where a cut leaves no bold word.

### Ch1 contributions list, after items 1 and 6 (PROPOSE)

> This dissertation makes the following contributions:
> - We build an APT attacker model that any study using MTDSim can run in place of the baseline attacker.[^1] Of eight properties an attacker model needs to model an APT attacker, the APT attacker model has **one in full and four in part**; three recent attacker models have at most one in full **and two in part**.
> - We find that, in MTDSim, the most effective MTD mechanism depends on the attacker model, so an evaluation against **a single attacker model** is not enough to show how MTD performs against **other attackers**.
>
> [^1]: The APT attacker model and the experiment scripts are publicly available at https://github.com/marc-la/MTDSim.

*(Alt. for item 1: "…so an evaluation against a single attacker model **may not show** how MTD performs against other attackers.")*

*Ring check.* Ch1 ¶3 ends "…against attacker models far simpler than an APT [cho2020, jalowski2026], and how well MTD performs depends on the attacker it faces [hong2018]." Contribution 2 now delivers the second clause, scoped to MTDSim. "Far simpler than an APT" still motivates the research question and contribution 1.

### Ch4 opener (PROPOSE)

> This chapter defines an APT attacker model built for three of the eight properties of Section~\ref{subsec:attacker-criterion}: objective-specific behaviour, choice of attack strategy and adaptivity. It takes the same attack actions as the baseline attacker, but the Petri net of its attack profile chooses its next tactic at runtime. With those attack actions it keeps the baseline attacker's campaign persistence; they also cap what it gains, so it has **one property in full and four in part** (Section~\ref{sec:fidelity-verdict}). It is a proof of concept: it tests whether an attacker with more of an APT's properties changes what an MTD evaluation measures. It avoids detection only through its tactic durations, which make it slower than the baseline attacker.

### §6.3 ¶1 (APPLY ON RULING)

> The APT attacker model has more of the eight properties than any of the three MTD attacker models of Section~\ref{subsec:recent-threat-models} (Table 6.1). It is the only attacker model with ~~choice of attack strategy in full or with~~ any objective-specific behaviour, which it has in part. All four attacker models lack cost–benefit reasoning, learning and deployment-strategy awareness.

### §6.3 ¶2 (APPLY ON RULING)

> In answer to SQ1, the attack flows drawn from threat reports give the APT attacker model the order of its tactics for each objective. That order gives it choice of attack strategy **and objective-specific behaviour, both in part** (Table 6.1). Threat reports time only whole intrusions, so the attack flows almost never record how long a step took (Section~\ref{subsec:dwell-times}). Drawn from incidents that succeeded, they never record what the attacker did after a step failed (Section~\ref{subsec:failure-matrix}). In MTDSim, MTD disrupts the APT attacker model at these two points: its tactic durations set how likely a deployment is to cut an attack action short and fail it, and its failure matrix sets which tactic it takes after an attack action fails (Section~\ref{subsec:runtime-mechanics}). The APT attacker model is therefore grounded in threat reports for the order of its tactics, and rests on our judgement where MTD disrupts it.

### §6.3 ¶3 (APPLY ON RULING)

> In answer to SQ2, the APT attacker model executes the order of its tactics inside an existing simulator, MTDSim, as a Petri net that chooses its next tactic at runtime, mapping eight of the 15 tactics onto MTDSim's six attack actions (Section~\ref{subsec:tactic-verb-mapping}). It shares the baseline attacker's attack actions and MTD deployments, so it keeps the baseline attacker's campaign persistence. Any difference between the two attackers comes from what the APT attacker model adds: the order of its tactics and four parts we declared (Section~\ref{sec:execution}). Two of those parts, the tactic durations and the failure matrix, fill what the threat reports do not record. The failure matrix makes the APT attacker model's response to failure a fixed rule of ours, so adaptivity is in part (Table 6.1). **The Petri net also chooses its next tactic by a fixed rule of ours, at random in proportion to the edge weights, so choice of attack strategy is in part.** The same attack actions cap the APT attacker model, because the other seven tactics are unmapped. Three of them are Collection, Exfiltration and Impact, the tactics of actions on objectives, so objective-specific behaviour is in part. MTDSim has no IDS, so the APT attacker model avoids detection only by proxy, through its tactic durations, and detection avoidance is in part. The APT attacker model is therefore comparable with the baseline attacker, and limited to what MTDSim's attack actions do: find and compromise hosts, with no actions on objectives.

*Read-aloud check.* §6.3 still makes one argument with no U-turn. ¶1 says it has more of the properties than the field, and is the only one with any objective-specific behaviour. ¶2 says the threat reports give the order, which gives two properties in part, and our judgement covers timing and failure. ¶3 says the simulator and our rules set the rest: our rules for adaptivity and choice of attack strategy, and the attack actions' cap for objective-specific behaviour and detection avoidance. "Chooses … by a fixed rule of ours" continues the opener's "chooses its next tactic at runtime" and does not contradict it.

### §6.4 ¶1 (APPLY ON RULING)

> In MTDSim, at every deployment interval, the most effective MTD mechanism differs between the two attackers (Table~\ref{tab:rank-one-intervals}). Which MTD mechanism an MTD evaluation finds most effective can therefore depend on its attacker model. An evaluation against **a single attacker model** is not enough to show how MTD performs against **other attackers**. This section says what that means for each of the three parts of an MTD evaluation that use the attacker model (Section~\ref{sec:mtd-evaluation-survey}): MTD modelling approaches, metrics and evaluation methods.

### Ch7 preamble and contribution 1, after items 1 and 6 (PROPOSE)

> This dissertation asked how MTD performs against APT attackers. In MTDSim, MTD performs differently against the APT attacker model than against the baseline attacker. At every deployment interval, the host layer reduces the APT attacker model's NCR most, and the service layer reduces the baseline attacker's NCR most. Which MTD mechanism an MTD evaluation finds most effective can therefore depend on its attacker model. An evaluation against **a single attacker model** is not enough to show how MTD performs against **other attackers**.
>
> **7.1 Contributions**
>
> The first contribution is an APT attacker model that any study using MTDSim can run in place of the baseline attacker, answering SQ1 and SQ2. Every earlier MTDSim study evaluated MTD solely against the baseline attacker. Threat reports record the order of an attack's tactics, but not how long each took or what followed a failure, so the APT attacker model's timing and response to failure, where MTD disrupts it, rest on our judgement. In MTDSim, the APT attacker model uses a Petri net to choose its next tactic at runtime, and maps each tactic onto one of the baseline attacker's six attack actions, none of which models actions on objectives. Of the four attacker models in Table 6.1, it is the only one with ~~choice of attack strategy in full, and the only one with~~ any objective-specific behaviour.

*Read-aloud check.* The preamble asks about APT attackers, answers for the APT attacker model in MTDSim, and ends on what any single-model evaluation can show. "Other attackers" mirrors the question's "how MTD performs against … attackers" without claiming that APT-ness caused the difference. Two modals in two sentences ("can … depend", "is not enough") is one hedge, not a stack. With the Alt. ("can … depend", "may not show"), it would be the stack Marc cut on 2026-10-15.

### Appendix B ¶1 and ¶2 (APPLY ON RULING)

> Table B.1 gives the predicates behind each mark of Tables 3.3 and 6.1. Its cells judge the APT attacker model from Chapter 4 and the three MTD attacker models from their papers. The predicates are Table 3.2's definitions; rows 1 and 6 split off a qualifier, row 5 splits at its ``and''. **To make ``over an extended period'' and ``low and slow'' testable, row 1 adds ``until it reaches its objective, however many MTD deployments that takes'', and row 5 adds ``slower than the baseline attacker''.**
>
> Distinct openings (Equation~\ref{eq:apv}) backs the APT attacker model's ~~full~~ mark for choice of attack strategy (Section~\ref{sec:disc-behaviour}). It counts tactics for the APT attacker model and attack actions for the baseline attacker; counted in attack actions for both, the attack profiles still have 190 to 844 distinct openings against the baseline attacker's 3.

### Table B.1 row 3 and Table 6.1 row (APPLY ON RULING)

> **3 Choice of attack strategy:** baseline attacker \propstandin, Masud \propnone, Kim \propnone, APT attacker model **\propstandin**
> behaviour: chooses among several sequences of techniques toward the same objective: rule, no, no, **rule**
>
> Table 6.1, APT attacker model: 1 \propmet, 2 \propstandin, 3 **\propstandin**, 4 \propstandin, 5 \propstandin, 6–8 \propnone

---

## Considered, no change

- **Abstract (l.209, l.228–229).** "Chooses its next step by objective" is still true, since the model has choice of attack strategy in part. "Make a case for testing MTD against more than one attacker model" states the same claim as a recommendation. Per the register, the validation gate reads "the same claim".
- **Ch1 ¶3 "far simpler than an APT" (l.312).** It is the field's gap, and it is cited. Kept, per the register.
- **Ch1 P5 "its attack profile decides which comes next" (l.446).** The attack profile's weights do decide it; this is no mark claim.
- **Ch3 Table 3.3 and the "Finding" paragraph (l.3475–3479).** They score only the three prior models, and none of their marks changes.
- **Ch3 "by predicates taken from each definition" (l.3237).** "Taken from" stays true with the two additions, which Appendix B now discloses.
- **Ch4 §4.3 "an immediate transition models its choice of the next tactic" (l.4307) and §4.5 distinct openings (l.5448–5463).** They describe the mechanism and the metric, not the mark. The GSPN's "probability proportional to its weight" (l.4317) is the rule 6e names.
- **§6.1 choice-of-attack-strategy paragraph (l.8643–8651).** It already says "picks the next tactic at random, in proportion to the edge weights", so 6e repeats it and nothing contradicts it. §6.1's "differs … on choice of attack strategy" (l.8592, l.8692) is a measured difference, not a mark.
- **T6 thr:yardstick (l.9353–9366).** It says we "cross-checked our marks against language models that blindly scored all four attacker models", and it claims no agreement. Flag for Marc: the 2026-10-08 record (H-E) says the blind re-score gave the full mark, so our mark now differs from it on property 3. The sentence stays true; no change is recommended.
- **Ch7 future work (l.9830–9873).** No item claims to lift property 3. Adding one would be new material that item 6 does not need.
- **Item 7: the dropped examples (rows 2 and 5) and "IDS" for "intrusion detection system (IDS)".** Once "word for word" is gone, "the predicates are Table 3.2's definitions" is true: an example is not a condition that a predicate tests. If Marc wants the sentence exact, add ", without their examples" after "definitions" (+3 words, outside the count).
- **Item 7: naming that row 1's addition decides Masud et al.'s mark.** The qualifier row of Table B.1, directly below the sentence, shows it. Saying it again would add a nuance the reader can see.
- **`docs/implementation/apt_model_criterion.md` axis 3.** It already reads "variety, not strategy". The session that applies item 6 may want a one-line dated note there that the thesis mark is now "in part". That is outside this sheet's scope.

## Net

Hand count, chapters 1–7 only. The appendices are outside the band (tex l.175–177).

| Item | Change | Words |
|---|---|---|
| 1 (Rec.) | three sentences, −4 each | −12 |
| 1 (Alt.) | three sentences, −6 each | (−18) |
| 6 | ch1 +4, ch4 0, §6.3 ¶1 −8, ¶2 −1, ¶3 +29, ch7 −11 (Rec.) | +13 |
| 7 | Appendix B only (+33 in the appendix, uncounted) | 0 |
| **Total (Recs)** | | **+1** (−5 with item 1's Alt.; +21 with 6i's Alt.) |

**Citations:** none added, moved or removed.
