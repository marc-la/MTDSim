---
status: open
created: 2026-10-15
---

# Title, abstract and introduction: the final mile against the seminar's tests

## State of play

Marc counts the title, abstract and introduction as final drafts. Their hedging and claim strength are done (claim-strength sweep, `795bd070`). This pass asks a different question: is this the best framing and presentation? The yardstick is the seminar's tests, now written out in full in [`../notes/_writing_guide.md`](../notes/_writing_guide.md) § *The front three*. Every item below is a **proposal**: ch1 and the front matter sit behind the edit gate, and nothing here has been applied to the tex.

The reading took the seminar speaker's seat: an experienced reviewer working through the filter chain (readable, significant, technical gap, contribution fills it, method, experiments, comparison).

## The reviewer's read, gate by gate

| Gate | Front three today | Verdict |
|---|---|---|
| 1 Readable | Plain register; one term per thing, with one exception (I5) | Pass |
| 2 Significant application | Volt Typhoon, five years in critical infrastructure; MTD as the time-shifting defence | Pass, strongly |
| 3 Technical gap | Abstract: "simplified attackers that follow a fixed sequence of steps". Intro P3: "attacker models far simpler than an APT". **Neither says why a simpler attacker matters.** The speaker's test is that "accuracy is low" is not a gap; why it is low is. Ch3 §3.3 has the why ("MTD that is effective against one attacker may therefore not be effective against an APT attacker", on hong2018); ch1 dropped it | **Weakest gate**: I1 |
| 4 Contribution fills the gap | Contribution 1 (the model, and its property score against three recent models) fills it | Pass |
| 5–7 promised | The method is promised (P5). Comparison is promised (the baseline attacker; three recent attacker models). The scale of the experiments is never stated ("different deployment intervals") | Weak on 6: I4, A2 |
| "So what" | The abstract ends on it. **The introduction never states it.** Contribution 2 repeats P6's last sentence, which the 2026-09-28 design note warned against | Gap: I2 |

## Title: keep it

*Evaluating moving target defence against advanced persistent threat attackers modelled on documented intrusion campaigns*

**Recommendation: no change.** Against the speaker's tests:

- **Problem-first is his own pattern** for work that is the first on its problem ("viewpoint-invariant human action recognition"). Ch3 §3.3 closes on "How MTD performs against APT attackers therefore remains unmeasured". The title names that problem, so the form is licensed, as long as ch3's claim stands.
- **No "using".** The model is not presented as a known tool applied to MTD.
- **Both readerships.** MTD readers find "moving target defence"; APT and CTI readers find "advanced persistent threat" and "intrusion campaigns".
- **The technical contribution is in it** ("attackers modelled on documented intrusion campaigns"), though last.

Its two weaknesses, owned: the lead word, "Evaluating", is its least informative word, and the finding is absent. The keyword permutation gives two alternatives. Neither wins:

| Option | Form | Why not |
|---|---|---|
| Contribution first (his default) | *An advanced persistent threat attacker model from documented intrusion campaigns for evaluating moving target defence* | It makes the model the contribution. The 2026-09-21 ruling, the RQ and the conclusion all place the contribution in MTD evaluation, with the model as the means |
| Topic, colon, finding | *Moving target defence against advanced persistent threat attackers: the most effective mechanism depends on the attacker model* | The 1 000-seed result now supports the finding (the rank-1 groups are disjoint at all six intervals). But a title cannot carry "in MTDSim", so it states more than ch7 does ("can depend"). None of the speaker's examples is a finding sentence. Marc rejected the form on 2026-09-21 ("no meat on the bones") |

## Abstract: three edits, one option

The current text is the base (edit, don't rewrite). The abstract is outside the word count (TC:ignore).

**A1. Headline first, then the instance (recommended).** Today the instance comes before the claim (S6, S7, then S8). The speaker's "one highlight result" and the house rule "important point first" both put S8 first. With S8 first, S6 and S7 can drop the words that repeat it. About −6 words.

> ~~At the default deployment interval, service diversity and port shuffle are the most effective MTD mechanisms against the baseline attacker. Service diversity reduces the number of hosts the baseline attacker compromises by 92 %, but reduces the number of hosts the APT attacker model compromises by 36 %. At every deployment interval, the most effective MTD mechanism differs between the two attackers.~~
>
> At every deployment interval, the most effective MTD mechanism differs between the two attackers. At the default interval, service diversity and port shuffle are the most effective against the baseline attacker. Service diversity reduces the number of hosts the baseline attacker compromises by 92 %, but the number the APT attacker model compromises by 36 %.

P6 must follow, because the abstract's results sentences are ruled to be P6 verbatim (I3).

**A2. "Twice" becomes the scale (recommended).** "We run an existing MTD simulator twice" can be read literally as two runs. It also hides gate 6, the 7 mechanisms × 6 intervals × 1 000 runs. It also leaves "deployment interval" to arrive first in the results. About −1 word.

> ~~We run an existing MTD simulator twice on the same networks, once with its scripted baseline attacker and once with the APT attacker model.~~
>
> We run it and an existing MTD simulator's scripted baseline attacker on the same networks, under seven MTD mechanisms at six deployment intervals.

"It" is S4's subject, the APT attacker model. Seven mechanisms and six intervals come from `tab_5-1a_experiment.tex`. Optionally, name MTDSim (+1 word): precise, and searchable.

**A3. "Attack profiles" leaves the abstract (lean yes).** The term is defined nowhere in the abstract and never used again there. What it carries is that the model's behaviour depends on its objective, which links back to S1's definition of an APT. Plain words carry that with one term fewer:

> ~~…from published reports of real intrusion campaigns, with attack profiles distinguished by objective.~~
>
> …from published reports of real intrusion campaigns, whose order of steps depends on its objective.

This stays within what was built: the order comes from the attack flows that share the objective. The alternative is to keep the term and add the intro's example ("such as stealing data").

**A4. Option: the closer answers the abstract's own gap.** The current closer is advice ("a case for testing MTD against more than one attacker model"). It holds, and it matches ch7's second implication. Two cold reviewers at the seminar found it flat. The alternative closes the ring with S3, in ch7's opening words:

> An MTD evaluation against a simplified attacker may therefore not show how MTD performs against an APT.

Lean: the alternative, because the abstract then answers the research question rather than stopping at a recommendation. It is a framing call, not a defect, so it is Marc's to make.

**Kept on purpose.**
- The application opener (S1, S2): the speaker's "writing for everybody" clause covers an examiner outside the subfield.
- The property score stays cut (2026-10-07): the speaker's brevity rule backs that cut.
- The abstract has no citations, as is normal.

**Assembled (A1–A3; current closer):** 175 words against about 180 now. The text is in the session scratchpad, and the text above is enough to rebuild it.

## Introduction: four edits

Ch1 counts towards the word band, which sits at its ceiling. I1 + I2 add about 34 words. An offset is listed at the end.

**I1. P3 says why a simpler attacker matters (recommended; gate 3).** The speaker's test: name the cause of the shortfall, as feature drift was the cause of low accuracy. Ch3 already has the cause on a citation. This edit borrows it in the conclusion's words ("how MTD is measured to perform"), so the front and the back of the dissertation use the same phrase. +12 words.

> Most tests run in simulation, against attacker models far simpler than an APT \citep{cho2020, jalowski2026}**, and how MTD is measured to perform depends on how the attacker is implemented \citep{hong2018}**. This gap motivates the research question of this dissertation:

This does not take away from contribution 2. Hong says metric values depend on the attacker. The finding is that the mechanism an evaluation would choose changes. **Verify:** hong2018 carries the claim as ch3 uses it (ch3 L2224–2227 cites it for the same sentence).

*Considered and not recommended:* moving contribution 1's property score into P3 as the landmark comparison (the 2026-09-24 design called the ch3 scoring "P3's premise"). It would make P3 the speaker's landmark-to-landmark hop. But "eight properties" needs a definition that ch1 cannot afford, and Marc moved the comparison out of P3 on 2026-10-07.

**I2. Contribution 2 carries the "so what" (recommended; the intro has none).** Today it restates P6's last sentence. The 2026-09-28 design note: "P6 … and this item must not both stand as they are". Ch7's opening paragraph already words the consequence, and it closes the ring with I1's "far simpler than an APT". +22 words.

> We find that, in MTDSim, the most effective MTD mechanism depends on the attacker model**, so an MTD evaluation against an attacker model far simpler than an APT may not show how MTD performs against APT attackers**.

**I3. P6 headline first (follows A1).** This is the same reorder as A1, so the abstract and P6 stay verbatim.

**I4. P5 states the scale (recommended; gate 6; 0 words).**

> …then under each of MTDSim's ~~MTD mechanisms at different deployment intervals~~ **seven MTD mechanisms at six deployment intervals**, how often MTD changes the network.

**I5. The overview uses two terms ch1 never defines (defect, not a seminar test).** "NCR" and "MTD layer" appear only in the chapter 6 sentence. P5 defines performance as the reduction in compromised hosts, and P6 uses "most effective". −3 words.

> …and~\ref{sq:evaluate} by finding which ~~MTD layer reduces each attacker's NCR most~~ **MTD mechanisms are most effective against each attacker**, and proposing why.

**Kept on purpose.**
- P1–P2's case and the definition of MTD. A general examiner needs them, and the lit-review feedback named missing examples as costing marks.
- The RQ and the SQs (ruled; broad on purpose).
- Contribution 1 is the speaker's gate 7, compared with previous methods.
- P5's detail. The speaker would squeeze it, but it was ruled sentence by sentence, and it is the reader's only view of the model before ch4.

**Offset if the band binds (+31 net):** P5's "Each attack profile records the steps drawn in the attack flows with that objective, and how often each step led to the next" (24 words). "Its attack profile decides which comes next" still makes sense without it, but the flows→graph→profiles step that Marc asked to be explicit loses its last link. Offer only if needed.

## A framing to carry into ch6–ch7, not into the front three

The speaker's ramp point fits this thesis exactly. A new benchmark that runs the field's existing methods with the field's metrics, and that still reports on the old benchmark, is a recognised contribution. Here the APT attacker model is the new benchmark, the baseline attacker is the old one, the seven mechanisms are the existing methods, and NCR reduction is the field's metric. "Benchmark" is not a dissertation term, and adding it would break the no-invented-terms rule. The value is in the defence: if an examiner asks whether evaluating existing MTD is a contribution, this is the answer, and §6.4 already argues it.

## Observation outside scope

Ch7 answers the RQ in **layers** ("the host layer reduces the APT attacker model's NCR more than the service layer does"), while the abstract and P6 answer it in **mechanisms**. The seminar's test is that the front three and the conclusion answer each other in the same words. This is either deliberate (the conclusion goes one level up) or a mismatch to settle. Flagged, not actioned.

## Validation gate

- Marc rules on A1–A4 and I1–I5. Ruled edits are applied to `dissertation.tex` with the comment trail, and the build is clean (83 pp, 0 undefined).
- The abstract results and P6 still match verbatim. Ch1 word delta is reported against the Overleaf count.
- I1's hong2018 reading is verified before it lands.

## Out of scope

Hedging and claim strength (done). Ch2–ch6 prose. The ch7 layers/mechanisms alignment (flagged above).

## Round 2 (2026-10-15): rulings, and two option sets

**Applied** (Marc: "happy with all that"): A1, A2, I1–I5. The build is clean, 83 pp, 0 undefined. I1's citation is checked: Hong §2 says "the evaluation results are dictated by the threat model used", of decision-theoretic defence selection, which is the reading ch3 L2224 already makes. **Deferred:** A4 (ch7 is being redrafted). **Open:** A3 wording and the layer reconciliation, below.

### A3: the build sentence

*We build an APT attacker model from published reports of real intrusion campaigns, ___.*

| Option | Words | For | Against |
|---|---|---|---|
| (a) …campaigns, **grouped by objective** | 3 | Shortest. Keeps S1's "objective". No new term | It says how the reports were sorted, not what the model does, so it does not answer S3's "fixed sequence of steps" |
| (b) We build an APT attacker model **that chooses its next step by objective**, from published reports of real intrusion campaigns | 6 | Answers S3 directly: fixed sequence against a chosen next step (the seminar's gate 4, the contribution fills the gap). Within what was built: the Petri net chooses the next tactic at runtime from its attack profile. "It" in S5 can now attach only to the model | "By objective" compresses how the choice is made: from the order of the campaigns with that objective |
| (c) …campaigns, **one attack profile per objective** | 5 | The term ch1 uses | The term is undefined in the abstract and never used again there |
| (d) We build an **objective-dependent** APT attacker model… | 1 | Shortest of all | Reads as jargon, and "dependent" does not say on what or how |

**Recommendation: (b).** It costs three more words than (a). Only (b) makes the build sentence the answer to the gap sentence before it.

### Mechanisms and layers: reconciling the front three with ch5–ch7

**What the terms are.** Ch2 defines the *host layer* (the topology) and the *service layer* (the services on each host) as layers of MTDSim's network model. Each MTD mechanism "reconfigures one part of the network: the host layer, the service layer or the users' credentials" (Table 2.1). Marc's "the layer the MTD operates on" is that definition. "MTD layer" and "MTD operational layer" are compressions that ch2 never defines. Ch6 uses "MTD layer" twice (L8509, L9021); that is flagged for ch6, and is auto-gate.

**How the two relate.** The two are not competing results. The mechanism is what is measured and ranked. The layer is the pattern among the mechanisms that rank first. At every interval, rank 1 against the APT attacker model holds only host-layer mechanisms, and rank 1 against the baseline attacker holds only service-layer mechanisms (ch5 L7793, Table 5.4). "The most effective MTD mechanism differs" is that pattern's consequence. Ch6 and ch7 explain the pattern at the layer level.

| Option | Form | For | Against |
|---|---|---|---|
| L1 Mechanisms in the front, layers from ch2 on (as now) | No change | No words. One term in the front three | Ch7 answers the RQ in words the front three never used (the seminar's same-words test). "Differs" does not say *how* the two attackers differ |
| **L2 The pattern in ch1's own words** (P2's "addresses, layout") | *At every deployment interval, the most effective MTD mechanisms against the APT attacker model change the network's addresses or layout, and those against the baseline attacker change its services. At the default interval, service diversity reduces the number of hosts the baseline attacker compromises by 92 %, but the number the APT attacker model compromises by 36 %.* | More information in fewer words (55 against 57: the "service diversity and port shuffle are the most effective" sentence is no longer needed). The disagreement shows as a pattern. No new term. Ch7's "host layer" is then the same finding in ch2's names | Overturns the 2026-10-07 choice of the bare "differs" as the headline. That ruling's intent holds: nothing wins against both attackers, and no attacker is crowned. "Services" is ch2's word, while P2 says "software" (port shuffle changes ports, not software) |
| L3 As L2, with ch2's terms glossed in ch1 (*"…are always host-layer mechanisms, which change the network's addresses or layout…"*) | ~+10 words on L2 | Exact term match with ch5–ch7 | It defines a term in ch1 that ch2 then defines again (voice §0: never pre-define). Longer |

**Recommendation: L2**, in the abstract and P6 together, so they stay verbatim. Contribution 2 ("depends on the attacker model") and the I5 overview are unchanged. Ch7, still being redrafted, keeps layers: by then ch2 has given the reader the names.

**Claim check for L2.** The rank-1 sets are IP shuffle, host topology shuffle and complete topology shuffle at 50–200 s, and IP shuffle at 500–2 000 s: all addresses or layout. Against the baseline attacker they are service diversity and port shuffle, then service diversity alone: all services (`numbers_reported.json`, `ranking.by_interval.*.*.sk_esd`, as recorded in the P6 comment).
