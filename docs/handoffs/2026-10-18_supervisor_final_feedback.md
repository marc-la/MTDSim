---
status: open
created: 2026-10-18
---

# Supervisor's final feedback: all 13 items closed before submission today

## State of play

Jin's final list has 13 items, the last optional. It predates the bibliography check (2026-10-16) and the claim check (2026-10-17), so each item is first tested against the current text. Each item's verdict is **still applies**, **partly** or **already closed**.

### How the list reads: an examiner's pass, in an examiner's order

An examiner reads the claims first (abstract, contributions, conclusion) and checks that they say the same thing. Next they probe the headline result for an explanation the text does not name. Then they check the self-assessment and the threats, and finally the presentation. Jin's list follows that order, and every item closes a specific way to lose marks.

| # | Item (short) | The mark it protects | Cluster |
|---|---|---|---|
| 1 | Contribution 2, §6.4 ¶1, ch7 ¶1 take the abstract's claim | **Overclaim.** We compared two attacker models. "Far simpler than an APT is not enough" claims that APT-ness causes the difference, which the design cannot show. The abstract already makes the claim the evidence licenses. | A |
| 6 | Choice-of-attack-strategy mark | **Inflated self-score.** A weighted random draw over edges is a choice in a loose sense only. An examiner asks why it scores "full" beside "part" for adaptivity. | A |
| 7 | Appendix B "word for word" | **Misdescribed method.** Row 5 adds a qualifier, so "word for word" is false as printed. | A |
| 2 | Name the mapping in §6.2, point to T2 | **Unnamed alternative explanation.** Part of the host layer's lead is an artefact of our mapping (actions fail for missing preconditions until Lateral Movement), not APT behaviour. | B |
| 3 | Adaptivity point in §6.2 or §6.3 | **Same, on adaptivity.** The model loses 242–324 s per host-layer deployment and does not respond. The lead measures non-adaptation, consistent with adaptivity scored "in part". | B |
| 13 | *(optional)* Run unmapped tactics at 0 s, IP shuffle and service diversity at 200 s | **Untested explanation.** §6.2 attributes the service layer's smaller effect to tactic durations without a test under MTD (T2 says so). | B |
| 4 | Why MTD helps the baseline (204–232 s forward) | **Unexplained anomaly in the results.** It is either designed behaviour (explain it in §5.3.1) or a possible defect (T1). | C |
| 5 | Extend T4: ASP/NCR sign flip; run endings | **Undisclosed counter-evidence.** T4's mitigation says ASP agrees with NCR. The sign flip and the censoring at the time limit qualify that. | D |
| 9 | c4 is a mixed group | **Misreadable design.** A reader takes c1–c4 as four objectives. | D |
| 8 | Scope change from the proposal | **Unexplained divergence** between Appendix A and the dissertation. | D |
| 10 | Notes left in refs [4] [26] [32] [62] | Professionalism. | E |
| 11 | Tay [14] vs Ho [17] entries | **Citation accuracy** on the supervisor's own lineage. | E |
| 12 | Page 29 typeface, unselectable text | Presentation. Probably a figure from the HTML or matplotlib pipeline. | E |

### Clusters and order

1. **C (item 4) and item 13's go/no-go first.** They are the only items that produce evidence. Item 4's finding also decides how §6.2 describes the baseline's time lost, which is item 3's wording.
2. **A: Marc's rulings.** Item 1's wording, item 6's mark, item 7's sentence. The rulings are fast but touch ch1 and ch7, so they need ratifying first.
3. **B: §6.2 and T2.** Written after C. If item 13 runs, after its result.
4. **D: threats and disclosure.** Independent of the others except for word budget.
5. **E: references and presentation, last.** Every text edit moves pages and possibly reference numbers. Rebuild, then fix the page and refs against the final build.
6. **Close.** Rebuild clean, diff the cited keys, check cross-references, count words against the band.

### Cross-cutting constraints

- **Edit gate.** Ch1–5 and ch7 edits are proposed to Marc first. Ch6 and appendix edits are applied after his ruling.
- **Word band.** The dissertation sits near its 15 000 ±10 % ceiling. Prefer replacing to adding, and count the delta per item.
- **One term per thing.** New sentences use the terms already defined: tactic-to-action mapping, time lost per MTD deployment, NCR reduction, ASP reduction, host layer, service layer.
- **No reruns** for item 4. Tracing single seeds is the instrument.

## Register (scoped 2026-10-18; line numbers at HEAD 7960123a)

Five read-only agents scoped the five clusters. Scratch evidence (traces, scripts, extracted rows, scratch builds) is in the session scratchpad: `scope_C/` holds the item 4 traces, `scope_D/` the T4 numbers, `scope_E/` the rebuilt old builds. The scratchpad is not kept; this register is the record.

**Which build Jin read.** His reference numbers match the builds of 2026-10-15/16 and now ([4] ghosh2009nitrd, [14] tay2024, [17] ho2024, [26] rodriguez2024, [32] mcqueen2006, [62] cybereasoncobaltkitty). Page layout is unchanged since then, so his locators can be read against the current build. The send date is not recorded (unverified).

### A. Claims and self-scoring

**1. The abstract's claim in three places. Still applies.**
- The same sentence appears in ch1 contribution 2 (l.597–600), §6.4 ¶1 (l.8960–8961) and the ch7 preamble (l.9743–9746).
- Recommended for ch1: "…depends on the attacker model, so an evaluation against a single attacker model may not show how MTD performs against other attackers."
- Recommended for §6.4 and ch7: "An evaluation against a single attacker model may not show how MTD performs against other attackers." Jin's "therefore" is dropped because the sentence before already has one.
- Delta −18 words. Gate: ch1 and ch7 propose; §6.4 apply.
- Ch1 ¶3's "far simpler than an APT" (l.312) stays. It is the field's gap, and it is cited.
- The validation gate becomes "the same claim": the abstract words it as a recommendation.

**6. Choice-of-attack-strategy mark. Still applies. Marc's ruling, because it overturns 2026-10-08 (13a.5).**
- The case for downgrading to P, with Table B.1's cell set to "rule":
  - the criterion doc says "variety, not strategy" (`apt_model_criterion.md` l.340–366);
  - 5 of 6 cold examiners raised it (2026-10-08);
  - the predicate cannot tell a corpus-weighted draw from a uniform random walk;
  - adaptivity, also an author-set rule, already scores P.
- The model keeps the most properties of any attacker model, and the only objective-specific behaviour.
- Ripple (9 places):
  - Table B.1 row 3 (l.10061)
  - App B ¶2 (l.10031)
  - Table 6.1 (l.8874)
  - §6.3 at l.8896, 8907, 8936
  - **ch1 contribution 1** (l.588): "one in full and four in part; three recent attacker models have at most one in full and two in part"
  - **ch4 opener** (l.3929)
  - **ch7 contribution 1** (l.9776)
- Delta about +12.
- The alternative is to keep "yes" with an App B justification (about +45). Not recommended.

**7. "Word for word" in Appendix B. Still applies, and wider than Jin noted.**
- Row 1's qualifier also adds words ("however many MTD deployments that takes"), and those words set Kim's and Masud's persistence marks.
- Recommended (l.10027–10029): "The predicates are Table 3.2's definitions; rows 1 and 6 split off a qualifier, and row 5 splits at its ``and''. To make them testable, row 1's qualifier adds that the attacker carries on however many MTD deployments it takes, and row 5 adds ``slower than the baseline attacker'' to ``low and slow''."
- Delta +22. Appendix: apply.

### B. Attribution of the host layer's lead

**2. Name the mapping. Partly applies.**
- §6.2 ¶2 (l.8760–8764) already describes the mechanism, but it never names the mapping or points to T2.
- Recommended: after l.8764, add "Part of the host layer's lead therefore comes through the tactic-to-action mapping (\ref{thr:cause})."
- T2's last sentence (l.9194–9196) becomes: "We never varied the tactic-to-action mapping, so we cannot separate its share of what we credit to the order of its tactics, the host layer's lead included."
- Optional: §6.4 l.9062, "we attribute mostly to these two differences".
- Keep "can fail". Jin's "fail … until it reaches Lateral Movement" overstates, because scan host never fails for a missing precondition.
- `\label{thr:mapping}` sits on T5 and is never referenced, so don't point to it.
- Gate: ch6, apply.

**3. Adaptivity. Still applies.**
- The numbers are in §6.2 ¶2 (l.8753), but the conclusion isn't drawn.
- Recommended, after item 2's sentence: "The host layer's lead also reflects a disruption the APT attacker model does not adapt to: without the failure matrix, its time lost per MTD deployment under IP shuffle is unchanged (Section~\ref{subsec:ablation-failure-matrix})."
- Why this wording:
  - it puts the evidence beside the claim;
  - it avoids "rather than", the not-X-but-Y tell, and a second "therefore";
  - it is consistent with adaptivity scored P.
- Don't restate the baseline as "loses none": §5.3.1 says "none", §6.2 says "at or below zero", and item 4 explains why.
- Items 2 and 3 together: about +46. Gate: ch6, apply.

**13. Optional run (unmapped tactics at 0 s, IP shuffle and service diversity at 200 s). Recommended: decline, with the reason recorded.**
- It is feasible. The `unmapped_zero` catalogue is in `run_duration_ablation.py`, and `run_duration_ranking.py` is the MTD harness. It would take 25–70 min of compute and 2.5–3.5 h of session time.
- But Table C.1b's ×0.25 band already lowered service diversity's NCR reduction (0.36 → 0.26). A faster attacker raises its no-MTD NCR, so an ambiguous or undercutting answer for §6.2 ¶3 is likely.
- That result would force rewrites of §6.2 ¶3, T2 and ch7 l.9804, at about +100–150 words, on deadline day.
- T2 already discloses that the duration ablation did not run under MTD.
- Conditional go only if items 1–12 close early and Marc commits before launch to report either way.

### C. The anomaly

**4. Why MTD helps the baseline attacker. Designed behaviour, so explain it in §5.3.1, not T1.**
- What the trace shows:
  - The first deployment lands (at about 100 s) while the baseline attacker exploits its first exposed endpoint.
  - The forced restart sends it straight back to that endpoint. Scan host rebuilds the list with that endpoint first (`attack_operation.py:340-346`), and exploit progress stands (`host.py:345-350`).
  - Its second pass reaches the services behind those it exploited.
  - With no MTD it moves on after one failed pass (`attack_operation.py:659-668`) and returns only when its list runs out.
- How it was checked:
  - Seeds 0, 3 and 12 were traced, and each matches its corpus row exactly.
  - Across 107 seeds, the first compromise is on host 0 in 80/83 runs with MTD against 54 with no MTD.
  - Every step conforms to the intent spec: IS-INT-01/04/07, IS-PRC-01/02/06/07, plus D-23 for service diversity's endpoint exemption.
- Recommended for §5.3.1, after l.7613: "The first deployment lands while the baseline attacker exploits its first exposed endpoint, and its restart takes it straight back to that endpoint. With no MTD, it returns there only after its list of hosts runs out."
- Delta +36. **Gate: ch5, propose.**
- §6.2's "at or below zero" then stands as it is.
- Flagged stale record: `docs/implementation/disruption_mechanism.md` §9 is wrong in three places: the §6.2 pointer, "an attempt it would not otherwise have had", and the omitted D-23. Fix when applying.

### D. Threats and disclosure

**5. Extend T4. Still applies; Jin's list is correct but not complete.**
- Source: `data/results/ch5_defended/numbers_reported.json` `sweep`/`sweep_asp`, which matches Tables F-0a and F-0d.
- Baseline attacker, NCR reduction positive and ASP reduction negative (CI excludes 0):
  - IP shuffle at 500, 1 000 and 2 000 s;
  - complete topology shuffle at 500 s;
  - also OS diversity at 500 s, which is not in Jin's list.
- Host topology shuffle flips the other way at 1 000 and 2 000 s. The APT attacker model has no sign flip outside its CI.
- How runs end:
  - APT attacker model: 91.0 % of runs end at the time limit with no MTD, and 96.7 % pooled under MTD.
  - Baseline attacker: 65.6 % end at a target with no MTD. Under MTD, pooled, it is 38.5 % at a target and 61.5 % at the time limit.
  - **So "mostly end at the target" must say "with no MTD".**
- T4's mitigation sentence ("orders the two layers as NCR reduction does") survives as worded. Ordering holds; only sign flips.
- Recommended (option B, +72): put the run endings in the threat statement and the sign disagreement in what remains, and keep rank 1. Full text, replacing T4 (l.9288–9294):
  > NCR reduction, our main metric, only partially measures how MTD performs: it counts the hosts an attacker compromises, whether or not it reaches a target host in the targeted attack scenario. The two attackers also stop counting at different times: with no MTD, 91\,\% of the APT attacker model's runs end at the time limit, and 66\,\% of the baseline attacker's at a target host. To mitigate this threat, we also computed ASP reduction, and it orders the two layers as NCR reduction does, for both attackers, at every deployment interval (Table~\ref{tab:eff-interval-values-asp}). The threat remains where the two disagree in sign: for the baseline attacker under IP shuffle at 500 to 2\,000\,s, and under complete topology shuffle and OS diversity at 500\,s, NCR reduction is positive while ASP reduction is negative. It also remains for rank~1 against the APT attacker model up to 200\,s, where ASP reduction ties every host-layer mechanism at 1 and only NCR reduction orders them.
- Option A (+54) keeps the mitigation and lists three residuals ("The threat remains in three places …"). Cheaper, but the run endings are left with no "so what".
  - The sign flips may share item 4's mechanism. Under IP shuffle at 500 s the baseline reaches a target more often (0.714 vs 0.656) and sooner. That is measured, not attributed: don't claim it.
- Gate: ch6, apply.

**9. c4 is a mixed group. Partly applies.**
- §4.2 l.4193–4196 lists c4's five flows ("whatever the reason"), but the heading and l.4179 present four objectives.
- What c4 holds: three flows evicted before acting, one positioning, one adware.
- Recommended: replace "whatever the reason:" with "so $c_4$ is a mixed group, not an objective:".
- Delta +6. **Gate: ch4, propose.** The heading stays.

**8. Scope change from the proposal. Still applies.**
- Appendix A has no prose, only the `\includepdf` margin label (l.9978–9995).
- Recommended text (S2, appended to the label): "After submission, changes to the defender were ruled out of scope, so this dissertation pursues only the proposal's first aim, a more capable attacker model, and evaluates MTDShield as released rather than studying its inputs, with no IDS."
- Grounding:
  - Jin, 19 Mar 2026: the defender side ruled out;
  - register V3: no retraining;
  - register V5: one RQ, three SQs.
- Marc to accept "ruled out of scope" as merging two rulings.
- Build check: two lines of `\small` in the top margin.
- Alternative: the same sentence in ch1 after the SQs (gate: propose).
- Interacts with item 12, because the same `\includepdf` changes.

### E. References and presentation

**10. Notes in [4], [26], [32], [62]. Still applies.**

| Ref | Key | Edit |
|---|---|---|
| [4] | ghosh2009nitrd (bib l.47) | `note` keeps only the URL |
| [26] | rodriguez2024 (l.434) | `note` keeps only the URL |
| [32] | mcqueen2006 (l.850) | delete `note` |
| [62] | cybereasoncobaltkitty (l.1081) | `note` keeps the date, archive URL and accessed date |

- The sweep found one more: [37] mitre2026attackv19 (l.581) "; Enterprise: 15 tactics". Cut it.
- The URLs must stay in `note`, because `ieeetr` prints neither `url` nor `doi`.
- Delta about −48 (the reference list counts toward the band).

**11. Tay [14] and Ho [17]. Still applies.**
- Both are `@mastersthesis` with `type = {GENG5512 Engineering Research Project Report}`. Zhang's entry (same unit) prints "Master's thesis".
- Fix: delete both `type` lines, so all three print "Master's thesis, The University of Western Australia". This matches the proposal.
- The near-identical titles are correct. They are two students, one supervisor, one semester, and each title matches its own cover.
- No in-text wording changes.

**12. Page 29. Applies, but the page is unidentified.**
- Neither printed p.29 nor physical p.29 shows the defect in any candidate build.
- The only pages with both symptoms (a different face, unselectable text) are **Appendix A, the proposal** (physical 55–60, printed 49–54). It is Type3 bitmap fonts with no ToUnicode, because it was recompiled 2026-08-20 without cm-super. Best guess: "29" is a misread "49". Only Jin can confirm.
- Fix:
  1. Swap in the original March submission, `/mnt/c/Users/marcl/Downloads/2902212125 - Marc Labouchardiere - 23857377_Proposal_13032026.pdf`. It has Type1 fonts and is selectable, and pages 2–7 are text-identical to the current proposal.pdf.
  2. Change `pages=1` → `2` and `2-` → `3-`.
- It takes about 15 min, and "as submitted" becomes literally true.
- Also: the itemize bullets on printed pp. 2 and 47 are Type3 bitmaps. One preamble line, `\renewcommand\labelitemi{\(\bullet\)}`, fixes them.
- Optional, 2–3 h: the six Chromium/Skia figures (Figs 2.1–2.3, 4.1–4.3, 4.5, C.2) embed Type3 Nimbus Sans. The text is selectable, but haloed labels copy twice. A TrueType font swap would fix them.

### Chains found by scoping

- **Items 4 → 3.** Item 4's explanation lets §6.2 keep "at or below zero"; item 3's sentence doesn't restate the baseline.
- **Items 4 ↔ 5.** The baseline's sign flips may share item 4's mechanism. Don't claim it (measured, not attributed).
- **Items 1 + 6** both edit ch1's contributions list and ch7. Propose them together, as one ch1 and one ch7 diff.
- **Items 8 + 12** both edit Appendix A's `\includepdf`. Apply them together, then build-check the margin label.
- **Items 2 + 13.** If 13 runs, T2 changes twice. Decide 13 before writing T2.

### Word budget

The recommended set nets about **+150 to +170** words of body text: item 1 −18, item 6 +12, item 7 +22, items 2–3 +46, item 4 +36, item 5 +72, item 9 +6, item 8 about +40 in a margin label. That excludes item 13. The reference cuts (−48) count too.
- The last count on record was about 16 518 against the 16 500 ceiling (2026-10-15), and claim-check edits since then are uncounted.
- **Marc reads the Overleaf count after applying.** If the total is over, the cut candidates are T4 option A (+54 instead of +72) and item 7 option C (+12), which is not recommended.

## Validation gate

- Each of the 13 items is marked closed (with commit), already closed (with evidence), or declined (item 13 only, with reason).
- Clean rebuild with no undefined references, the cited-key diff empty except for intended changes, and the word count reported.
- The abstract, contribution 2, §6.4 ¶1 and ch7 ¶1 make one claim, in the same words.

## Reading list

- `docs/thesis/dissertation.tex`: abstract (~182), contributions (~584), §6.2 (~8695), §6.4 (~8949), §6.5 (~9070), ch7 (~9708), Appendix B (~10021)
- `docs/implementation/apt_model_criterion.md`: the yardstick for item 6
- `docs/implementation/mtdsim_intent_spec.md`: the instrument for item 4
- `docs/workflows/threats_terminology.md`: wording for items 2 and 5
