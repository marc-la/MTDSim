# C + D: the anomaly, the threats, and the disclosures (items 4, 5, 9, 8)

> **Reviewer notes (main session, 2026-10-18).** Ready to rule. Three points:
> 1. **Item 5 is the biggest word cost on any sheet: +100 (Rec.) against +73 (Alt.).** The Rec. is worth it, because its second sentence is the "so what" Jin's two points lack. If the baseline attacker reaches a target sooner under MTD, its runs end sooner with fewer hosts. NCR reduction then rises while ASP reduction falls, which is exactly the sign flip. That one sentence explains every cell the next sentence lists. **Recommend the Rec.** If the band forces a cut, drop the host topology shuffle clause first (about −10) before taking the Alt.
> 2. **Item 8: put the proposal's aim in quotation marks**, ``a more sophisticated adversarial module''. Unquoted, "sophisticated" reads as our claim about our own model; quoted, it is the proposal's words, which is the point.
> 3. **Item 4** uses only §2.2's words. It describes what MTDSim does and says nothing about why it was designed that way, which keeps it within the ch5 rule.

**Status:** sheet for Marc's ruling, 2026-10-18. Nothing here has touched the tex. Quotes were re-read against HEAD `74033db9`, where `dissertation.tex` is unchanged since the register was scoped.

**The rule.** Explain or disclose what an examiner would otherwise find without help, using only words the thesis already defines.
- **Purpose:** each item closes one way to lose marks. Item 4 is an unexplained anomaly in the results. Item 5 is counter-evidence that T4's mitigation leaves unsaid. Item 9 is a design a reader can misread (c4 read as the positioning objective). Item 8 is an unexplained gap between Appendix A and the dissertation.
- **Context:** the evidence is the register's scoping (traces for item 4), plus checks this session ran again itself:
  - `numbers_reported.json` `sweep` / `sweep_asp`, every number printed below;
  - `time_lost_first_deployment.py` and its JSON, which give 2 000 s as the interval behind 204–232 s;
  - `mtd_operation.py`, whose trigger loop fires the first deployment at t = 0 at every interval;
  - Tables F-0a and F-0d as built;
  - `proposal.tex` §Aim;
  - `architecture.md` §(a).
- **Audience:** item 4 is read by everyone who reads §5.3.1. Items 5 and 8 are read by the examiner checking the threats and the appendix. Item 9 is read by anyone reading Chapter 4's design.

---

## Item 4. Why MTD helps the baseline attacker (§5.3.1). PROPOSE

| # | Location | Before | After | Why | Risk |
|---|---|---|---|---|---|
| 4 | §5.3.1, ¶ "On adaptivity", after l. 7613 ("… `\prelim{232}\,s forward.`") | `Under every host-layer and service-layer mechanism, the first deployment of each run brings the baseline attacker's first compromise \prelim{204} to \prelim{232}\,s forward. After the first MTD deployment, each later …` | **Rec.** Insert between the two sentences: `The first deployment disrupts the baseline attacker while it exploits its first exposed endpoint, and sends it straight back to that endpoint. With no MTD, it returns there only after its list of hosts runs out (Section~\ref{subsec:attacker-model}).`<br>**Alt.** The same in one sentence: `With MTD, the first deployment sends the baseline attacker straight back to the exposed endpoint it is exploiting, where with no MTD it returns only after its list of hosts runs out (Section~\ref{subsec:attacker-model}).` | Jin asked for the explanation in §5.3.1 if the behaviour is designed. The scoping traced it as designed: the forced restart conforms to IS-INT-01/05/07 and IS-PRC-01/02/06/07, and D-23 exempts the endpoints. **Terms:**<br>- "exposed endpoint" is §2.2.1's, which also says no MTD mechanism changes the endpoints. That is why the return pays off, and the reader already has it.<br>- "disrupts" and "sends it … back" are §2.2.3's verbs for a deployment.<br>- "its list" and "runs out" are §2.2.3's ("the next host on its list. When the list runs out").<br>- I dropped the register's "lands" and "its restart": neither is a thesis term.<br>- The pointer is to the section that states the rule, so the text reads as designed behaviour without "by design".<br>**Interval:** 204–232 s is measured at 2 000 s, the interval the paragraph names. The first deployment is triggered at t = 0 and completes at about 100 s at every interval, so the explanation holds at the interval reported. | **Ch5 rule** (plain description, no method philosophy): the two sentences describe what MTDSim does, and say no "because" and nothing about design intent. Jin's request overrides the cut-mechanism habit here.<br>**Inference left to the reader:** the second attempt comes earlier, so the compromise comes forward. This is one step, which §2.2.3 equips.<br>**Ripple:** "after its list of hosts runs out" glosses §2.2.3's "its list". It is not a new term.<br>**Word band:** +38. |

**In place.** The paragraph starts at l. 7598. The `%` lines between l. 7604 and l. 7610 do not break it.

> On adaptivity, the two attackers lose time to different MTD mechanisms (Figure 5.2(b)). The APT attacker model loses 242 to 324 s per host-layer deployment, and the baseline attacker none, though every host-layer deployment blocks its attack action. The baseline attacker loses 493 s per service-diversity deployment, and the APT attacker model 60 s. Under every other MTD mechanism, the APT attacker model loses 26 s or less. The baseline attacker's time lost is at or below zero under every MTD mechanism but service diversity. Under every host-layer and service-layer mechanism, the first deployment of each run brings the baseline attacker's first compromise 204 to 232 s forward. **The first deployment disrupts the baseline attacker while it exploits its first exposed endpoint, and sends it straight back to that endpoint. With no MTD, it returns there only after its list of hosts runs out (Section 2.2.3).** After the first MTD deployment, each later host-layer or port-shuffle deployment costs it 18 to 32 s.

The paragraph reads straight on: the fact, then what happens, then the later deployments. "The first deployment" is repeated verbatim on purpose, following the one-term rule.

---

## Item 5. Extend T4 (thr:ncr, §6.5). APPLY ON RULING

**Numbers (checked against `numbers_reported.json` this session, and against Tables F-0a and F-0d as printed).**

| Baseline attacker | Interval | NCR reduction (F-0a) | ASP reduction (F-0d) |
|---|---|---|---|
| IP shuffle | 500 / 1 000 / 2 000 s | 0.39 / 0.30 / 0.19 | −0.09 / −0.11 / −0.10 |
| complete topology shuffle | 500 s | 0.09 | −0.23 |
| OS diversity | 500 s | 0.04 (interval 0.007–0.075) | −0.11 |
| host topology shuffle (reverse) | 1 000 / 2 000 s | −0.08 / −0.11 | 0.08 / 0.12 |

- **Which cells count as a disagreement:** a cell counts only where neither 95 % interval includes zero, so neither cell is grey. Port shuffle at 500 s (0.10 against −0.02, the ASP cell grey) is not a disagreement.
- **The APT attacker model** has no disagreement whose intervals exclude zero.
- **How runs end, with no MTD:**
  - APT attacker model: ASP 0.090 ± 0.009, so 91 % of runs end at the time limit.
  - Baseline attacker: ASP 0.656 ± 0.029, so 66 % end at a target host.
  - These match the 0.09 and 0.66 that Tables 5.x, E and F-1 print (P1 precision).
- **Pooled under MTD** (all 66 conditions): 96.7 % of the APT attacker model's runs and 61.5 % of the baseline attacker's end at the time limit. The pooled shares are not printed (see Considered).
- **Layer order** holds under ASP reduction for both attackers at all six intervals: host before service for the APT attacker model, service before host for the baseline attacker. The mitigation sentence therefore stands as worded.
- **Rank 1 up to 200 s:** all three host-layer mechanisms are exactly 1.0 against the APT attacker model at 50, 100 and 200 s.

| # | Location | Before | After | Why | Risk |
|---|---|---|---|---|---|
| 5 | §6.5, T4, l. 9288–9294 | `NCR reduction, our main metric, only partially measures how MTD performs: it counts the hosts an attacker compromises, whether or not it reaches a target host in the targeted attack scenario. To mitigate this threat, we also computed ASP reduction, and it orders the two layers as NCR reduction does, for both attackers, at every deployment interval (Table~\ref{tab:eff-interval-values-asp}). The threat remains for rank~1 against the APT attacker model up to 200\,s, where ASP reduction ties every host-layer mechanism at 1 and only NCR reduction orders them.` | **Rec.** Full T4 below. It adds two sentences to the threat and one to what remains.<br>**Alt.** The register's option B, verbatim (+73). It gives the run endings with no "so what", and omits host topology shuffle's reverse. | **"Flesh it out" means three moves** (threat, then mitigation, then what remains, per `threats_terminology.md` (a)):<br>(i) **Threat.** NCR is counted when the run ends, and the two attackers' runs end at different points. For the baseline attacker, an MTD mechanism that helps it reach a target host ends its runs sooner, which can raise NCR reduction. This is definitional (§4.5's "when a run ends"; Table 5.1's end of run), so it is stated with one hedge ("can") and is not attributed to item 4's mechanism.<br>(ii) **Mitigation.** Unchanged and still true.<br>(iii) **What remains.** The sign disagreements, then rank 1, kept.<br>**Host topology shuffle's reverse belongs** in what remains. It is the same threat run the other way (fewer runs at a target, so longer runs and more hosts). It sits non-grey in the same two tables the item points to. Leaving it out would recreate the defect this item exists to close, undisclosed counter-evidence an examiner finds by comparing F-0a with F-0d. It costs about 10 words.<br>**"with no MTD"** is required. Under MTD, pooled, 61.5 % of the baseline attacker's runs end at the time limit, so Jin's "mostly end at the target" is true only with no MTD.<br>**"disagree in sign"** gives NCR's sign by implication. Only ASP's sign is printed, which saves about 6 words over naming both. | **Word band:** +100 (Rec., counted by script, a `\ref` = 1 word) against +73 (Alt.). This is the largest single cost on the sheet. If the Overleaf count is over, the Alt. is the cut.<br>**Pointer:** I considered adding Table F-0a beside F-0d in what remains, since the flips show only by comparing the two. I left it out: F-0d's caption says "laid out as Table F-0a", and Appendix D prints them together. Add `(Tables~\ref{tab:eff-interval-values} and~\ref{tab:eff-interval-values-asp})` (+5) if you want it explicit.<br>**Attribution trap:** the item 4 link (IP shuffle at 500 s raises the baseline attacker's ASP from 0.656 to 0.714) is not claimed. "can raise" states what the metric allows, not what caused these cells.<br>**Type:** construct validity, unchanged. "only partially measures" is the file's construct form. |

**In place (Rec.).**

> \item\label{thr:ncr} NCR reduction, our main metric, only partially measures how MTD performs: it counts the hosts an attacker compromises, whether or not it reaches a target host in the targeted attack scenario. **It counts them when the run ends: with no MTD, 91\,\% of the APT attacker model's runs end at the time limit, and 66\,\% of the baseline attacker's at a target host. An MTD mechanism that helps the baseline attacker reach a target host can therefore raise NCR reduction by ending the attacker's runs sooner.** To mitigate this threat, we also computed ASP reduction, and it orders the two layers as NCR reduction does, for both attackers, at every deployment interval (Table~\ref{tab:eff-interval-values-asp}). The threat remains **where the two disagree in sign, all for the baseline attacker: ASP reduction is negative under IP shuffle at 500 to 2\,000\,s and under complete topology shuffle and OS diversity at 500\,s, and positive under host topology shuffle at 1\,000 and 2\,000\,s. It also remains** for rank~1 against the APT attacker model up to 200\,s, where ASP reduction ties every host-layer mechanism at 1 and only NCR reduction orders them.

**In place (Alt., register option B).**

> NCR reduction, our main metric, only partially measures how MTD performs: it counts the hosts an attacker compromises, whether or not it reaches a target host in the targeted attack scenario. **The two attackers also stop counting at different times: with no MTD, 91\,\% of the APT attacker model's runs end at the time limit, and 66\,\% of the baseline attacker's at a target host.** To mitigate this threat, we also computed ASP reduction, and it orders the two layers as NCR reduction does, for both attackers, at every deployment interval (Table~\ref{tab:eff-interval-values-asp}). The threat remains **where the two disagree in sign: for the baseline attacker under IP shuffle at 500 to 2\,000\,s, and under complete topology shuffle and OS diversity at 500\,s, NCR reduction is positive while ASP reduction is negative. It also remains** for rank~1 against the APT attacker model up to 200\,s, where ASP reduction ties every host-layer mechanism at 1 and only NCR reduction orders them.

"the time limit" is already given by §6.5's opening paragraph ("a time limit of 15\,000\,s") and by Table 5.1.

---

## Item 9. c4 is a mixed group (§4.2). PROPOSE

| # | Location | Before | After | Why | Risk |
|---|---|---|---|---|---|
| 9 | §4.2 ¶2, l. 4193–4194 | `The five attack flows of $c_4$ did neither, whatever the reason: three attackers were removed …` | **Rec.** `… did neither, so $c_4$ is a mixed group, not a single objective: three attackers were removed …`<br>**Alt.** The register's `… so $c_4$ is a mixed group, not an objective:` (one word shorter). | **Jin's words** are "a mixed group of attack flows, not a single objective". **The misreading is specific:** the same paragraph says positioning has no action of its own and gets no question, so a reader takes the no/no profile to be positioning. The colon list (three evicted, one positioning, one adware) then shows the mix. **"single" over the register's "an":** the section is "Attack profiles by objective" and l. 4179 "split it by objective into four attack profiles". "Not an objective" sits against both. "Not a single objective" agrees with them: c4 is the split's remainder, holding more than one. | **Contrast form:** "a mixed group, not a single objective" is an X-not-Y tail. It is kept because it names the exact misreading. Cutting the tail ("so $c_4$ is a mixed group:", +3) loses the correction Jin asked for.<br>**Word band:** +7. |

**In place.**

> Section 3.1.1 gives three objectives. Data exfiltration and impediment each have an action in actions on objectives: the attacker steals data, or it impedes the victim's systems by encrypting, destroying or hijacking them. Positioning for future operations has no action of its own, because the attacker stays in post-intrusion operations. We therefore asked two questions of each attack flow: did the attacker steal data, and did it impede the victim's systems? Their yes-or-no answers give the four attack profiles of Table 4.1. An attack flow that did both belongs to $c_3$ alone, so no edge weight counts it twice. Six of the seven attack flows of $c_3$ are ransomware that stole data and then encrypted the systems. The five attack flows of $c_4$ did neither, **so $c_4$ is a mixed group, not a single objective**: three attackers were removed from the network before they acted, one positioned for future operations, and one ran an adware campaign.

---

## Item 8. The change of scope from the proposal (Appendix A). APPLY ON RULING

**What the reader can see.** The proposal's §Aim lists four aims:
1. "Develop a more sophisticated adversarial module";
2. "Systematically explore AI-MTD input parameters and configurations";
3. "Analyse and characterise the relationship between configuration choices and performance";
4. "(Stretch) Design and integrate an IDS observation module".

**The dated reasons** (`architecture.md` §(a)):
- the defender side was ruled out ("large can of worms", Jin, 19 March 2026, six days after the 13 March submission);
- IDS is not a research thread;
- Tay's RL agent is reused, not retrained (register V3).

| # | Location | Before | After | Why | Risk |
|---|---|---|---|---|---|
| 8 | App. A, `\includepdf` `pagecommand` margin label, l. 9993–9994 | `\noindent{\small\textsc{Appendix~\thechapter}\quad Original honours proposal, as submitted in March 2026}` | **Rec.** `\noindent{\small\textsc{Appendix~\thechapter}\quad Original honours proposal, as submitted in March 2026. After submission, work on the defender was ruled out of scope, so this dissertation pursues only the first of the proposal's four aims, a more sophisticated adversarial module, and runs MTDShield as released, with no IDS.}`<br>**Alt.** The same sentence in Chapter 1, after the sub-questions (l. ~397). That location is gated PROPOSE. | **The margin label is the only place the reader meets the proposal.** No body text cites `app:proposal`, so the explanation belongs where the divergence shows.<br>**Changes from the register's S2:**<br>- "rather than studying its inputs" is cut (Marc's dislike). "runs MTDShield as released" carries aims 2–3, and "as released" is T3's and §5.1's wording.<br>- "a more capable attacker model" becomes the proposal's own words for aim 1, so the reader can match it on the page.<br>- "four aims" lets the reader count what was dropped.<br>- "work on the defender" replaces "changes to the defender": aims 2–3 study the defender's inputs, they do not change it, so "changes" did not cover them.<br>**Alt. weighed:** Chapter 1 is read by everyone, but it spends body words on a point only the appendix raises, and it puts a scope history in the introduction. | **Term clash:** the proposal says "the *MTDShield* simulation framework", while the dissertation uses MTDShield for Tay's deployment strategy. The label uses the dissertation's sense. That is correct for this document, but a reader moving from label to proposal may notice. Acceptable: the label is in the dissertation's voice.<br>**"ruled out of scope"** merges two rulings (19 March, V3). The register flagged this for Marc to accept.<br>**Build:** about 2–3 lines of `\small` in the top margin above the proposal's title. Check that it clears the title.<br>**Item 12** swaps the PDF and offsets `pages=1`→`2`, `2-`→`3-`. The label rides on whichever page `pagecommand` decorates. Apply both together, then build-check.<br>**Word band:** +36 (margin label). Whether it counts depends on Overleaf's counter. |

**In place (as rendered, top margin of the proposal's first page).**

> APPENDIX A  Original honours proposal, as submitted in March 2026. **After submission, work on the defender was ruled out of scope, so this dissertation pursues only the first of the proposal's four aims, a more sophisticated adversarial module, and runs MTDShield as released, with no IDS.**

---

## Considered, no change

**Item 4**
- **l. 7600, "and the baseline attacker none":** "loses none" is true of a time lost at or below zero, and two sentences later the same paragraph gives the sign ("at or below zero"). No contradiction, so no edit.
- **§6.2 l. 8754, "at or below zero":** agrees with l. 7610. It stands, as the register said.
- **§6.2 ¶2 (scan host, scan port):** explains the later deployments by layer. It needs no first-deployment pointer, because §5.3.1 now carries the explanation.
- **T1 (thr:code):** the behaviour conforms to the intent spec, so it is not a defect candidate, and T1 is untouched.
- **Figure 5.2's caption:** it already names 2 000 s, the interval behind the 204–232 s. The first deployment's time (about 100 s) is not needed in the text.
- **`docs/implementation/disruption_mechanism.md` §9 is stale:**
  - its "How it is reported" line points the mechanism to §6.2;
  - it says "an attempt it would not otherwise have had";
  - it omits D-23.

  This is a repo record, not dissertation text. Fix it when applying (register note).

**Item 5**
- **§6.4 l. 9016,** "Ranking on ASP reduction orders the two layers as NCR reduction does, for each attacker": still true, because layer order holds at all six intervals for both attackers.
- **Appendix D l. 10381,** "At 200 s, ASP reduction shows the order of NCR reduction": still true. There is no sign disagreement at 200 s, and the two rankings correlate at ρ = 0.93 (baseline attacker) and 0.98 (APT attacker model).
- **Pooled-under-MTD run endings (96.7 %; 38.5 / 61.5 %):** not printed. "with no MTD" is exact, and the threat sentence already says MTD moves the baseline attacker's run end.
- **Layer-mean disagreement** (baseline host layer at 500 and 1 000 s: NCR reduction 0.16 / 0.06, ASP reduction −0.10 / −0.06): made up of the mechanism cells listed. The mechanism-level list follows Jin's wording and covers it.
- **Port shuffle at 500 s:** the ASP interval includes zero, so it is not a disagreement.
- **Item 4's mechanism as the cause of the flips:** measured, not attributed, so not claimed.

**Item 9**
- **§4.2 heading "Attack profiles by objective":** the profiles come from the two objective questions, and c4 is the "neither" answer. The heading holds, and "not a single objective" fits it.
- **l. 4179, "split it by objective into four attack profiles":** same reason.
- **Table 4.1 caption, "The four attack profiles.":** its columns show the yes/no answers. No change.
- **l. 4260 ("none of $c_4$ reaches Impact") and §6.1 l. 8620 ("neither in $c_4$"):** consistent with a mixed group.

**Item 8**
- **`proposal.tex` / `proposal.pdf`:** untouched. The proposal stays as submitted.
- **The appendix comment block (l. 9978–9988):** no reader-facing text.

## Net

Words were counted by script over the tex (a `\ref` = 1 word, `\,` joined). These are hand-checkable.

| Item | Rec. | Alt. |
|---|---|---|
| 4 (ch5, propose) | +38 | +34 |
| 5 (ch6, apply) | +100 | +73 |
| 9 (ch4, propose) | +7 | +6 |
| 8 (App. A margin label, apply) | +36 | +36 in ch1 |
| **Total** | **+181** (+145 in body text, excluding the margin label) | **+149** |

- **Against the register:** its estimate for these four items was about +154. The difference is item 5's "flesh it out" (+27 over option B).
- **Citations:** none added, moved or removed.
- **Cross-references:** item 4 adds one section reference (§2.2.3); item 5's optional second table pointer is not in Rec.
