# Claim check, run 1: the front page

Read this first, then [`review_sheet.md`](review_sheet.md) (every item, with the quotes). Generated 2026-10-17 from `verdicts/`.

## Where the dissertation stands

| | Count |
|---|---|
| Claim–source pairs verified | 269 of the 273 in the inventory. The other 4 are the no-text sources (Cai, Ajmone Marsan 1995, Efron, Cohen), on your sheet |
| Pairs checked by both verifiers | 147: every high-risk unit, plus the pilot |
| Quotes | 617 found verbatim in their own source, 20 found only in an appended markdown copy (re-check), 14 with no quote (absence claims, or the ATT&CK bundle), 5 web-only |
| **Pairs carrying a major defect** | **27 (8.1 %)**. The human baseline is 11.9 % major (Jergas & Baethge 2015) |
| Pairs with only minor issues | about 150: dropped hedges, a citation on the wrong clause, "after [x]" missing |
| Uncited claims screened | 243: 166 ours, 45 covered, 4 common knowledge, **26 needs-source**, 2 mark-ours |
| Mechanical exceptions | 14: one wrong number, rounding, pointers |

### Confidence against your 10 % target

- **Pairs both verifiers checked.** A found 9 majors and B found 14; they agree on 6. The capture–recapture (Chapman) estimate is about 20 majors in those pairs, so **about 3 were missed by both**. That figure assumes the two verifiers are independent. They are the same model, so the true number is probably somewhat higher.
- **Pairs only A checked** (the V2 tier).
  - A flagged about 71 % of the issues that A and B together found on the double-checked pairs, but rated many of them minor where B said major.
  - The V2 skim list may therefore hide a few majors rated minor.
  - The cheapest remedy is that you read the skim list's issue lines (86 one-liners).
- **After your rulings**, the expected residual is roughly 3–8 undetected majors in 273 pairs, about 1–3 %. That is well under your 10 % target and under the human baseline. It is an estimate, not a measurement, and this is why: the double-checked pairs are the high-risk ones, so their miss rate need not carry over to the rest.

## The 27 majors, grouped by cause: one ruling per group

Items marked ✔ the session re-verified against the source or the ATT&CK bundle itself.

**G1. A value from MTDSim's code, cited to a paper.** All are in §2.2, on your supervisor's lineage. One ruling would settle the group: cite `tay2024code` wherever the value is the code's.

| Unit | What is cited where |
|---|---|
| U0082 | 20–110 s deployment, cited to Zhang. Zhang gives 70–110 s; the 20 s is the code's |
| U0126 | ~20 s confusion penalty, cited to Zhang. Zhang gives no value; it is `constants.py:147` |
| U0127 | Stolen credentials kept after a deployment, cited to Zhang. Zhang has no user shuffle |
| U0116 | The RoA formula, cited to Brown. Brown gives no formula |
| U0121 | "15 s × (1 − AC)", cited to Brown. Brown gives no exploit duration |

The same pattern shows at minor or screen level: U0124, U0095, Table C.2's "MTDSim's time" column (9 cells), U0077, and U0091 (the internal-host exemptions are D-23, not Brown).

**G2. Our adaptation of a metric, credited bare to its source.** One ruling would settle the group: "this dissertation, after [x]", the form Table 4.3 already uses for Royston.

| Unit | Metric |
|---|---|
| U0520, U0566 | Attack actions blocked *per MTD deployment*: Brown reports a total |
| U0519, U0513 | NCR reduction (Alavizadeh) and attack confidentiality (Zaffarano), from the pilot |

Minors in the same group: U0516, U0512 and U0543 (Zhan's rate is attacks *arriving*), U0560.

**G3. Survey and gap claims that say more than the source.** These carry the thesis's motivation.

| Unit | Where | What the source says |
|---|---|---|
| U0016 | Ch1 ¶2 | Cho never lists credentials as something MTD changes |
| U0019, U0211, U0791 | Ch1, §3.2.2, ch6 | Hong 2018 says comparing MTD needs knowledge of attacker capabilities. It does not show that measured performance depends on how the attacker is implemented. This is the supervisor's paper |
| U0841 | §6.5 | "The finding of the two surveys" that attacker models "lack the properties" of an APT: Cho covers several properties, not all eight. Proposed fix: "lack several properties" |
| U0168 | §3.1 | Rodríguez profiles from host event logs, not CTI |
| U0458 | §4.4.2 | Mendonça times no attack step |

Minors in the same group: U0209 (a 2020 survey for a present-tense "no standard exists"; add Jalowski p. 4), and U0226 and U0299 (Jalowski calls itself a gap analysis, not a survey).

**G4. A citation whose source argues against the sentence.**

| Unit | Where | Conflict |
|---|---|---|
| U0442 | §4.4.2 | Holm and Madan, cited for the exponential tactic delays, both find the exponential a poor fit for attacker behaviour. Proposed fix: cite them for "attack time is random" only, and keep Bland and the Petri-net reason for the exponential. Optional: one §6.5 line |
| U0613 | §5.1 | Lakens ✔, cited beside ±0.2, a benchmark bound he calls "the weakest possible justification". Linked: U0606, where "negligible" may be Tantithamthavorn's word ✔, not Cohen's (check your Cohen) |
| U0125 | §2.2 | Brown has user shuffle block credential *stuffing*; the sentence says brute force |
| U0067 | §2.2 | Hong & Kim 2012 define a *two*-layer HARM. The three-layer version is Brown's, so add brown2023 |

**G5. Wrong facts and numbers.** Mostly mechanical once ruled.

| Item | Wrong | Right |
|---|---|---|
| U1202, Fig. 3.1 title | "254 techniques" | v19.1 Enterprise has **222** ✔; 254 counts technique–tactic slots |
| U0964, Table C.1 | Ragnar Locker G0125 (HAFNIUM) | ATT&CK v19.1 links it to G0061 FIN8 ✔ |
| U0957, Table C.1 | WhisperGate G0034 (Sandworm) | ATT&CK v19.1 links it to G1003 Ember Bear ✔ |
| U0083, Table 2.1 caption | "added to by Zhang" | All seven mechanisms are Brown's; cut it |
| U1024, App. D.1 | "the 38 he trained" | At least 49. Proposed fix: "of the 38 in his hyperparameter evaluation" |
| U1034, App. D.1 | "four of its eight inputs" | Four of its eleven |
| U0546, §4.5 | The Pendleton citation | The sentence exists only in the arXiv v1, not the published version the bib cites |

The first three come from the classification data and the figure generator, so a fix goes through `data/gasp/metadata_audit.csv` and `tools/attack_matrix_figure.py`. Check the blast radius on the one-flow-per-group rule before changing a group ID.

## Rulings the checks cannot make

1. **Credential theft as "stole data".** Appendix C counts Mac Malware's credential theft as stealing data, but not BumbleBee's, TA2's or Gootloader's. This needs one rule.
2. **ToolShell (Unit 42) "did not impede".** It holds only by reading the attack flow, which §4.2 says the answers do not do. The report leads with ransomware.
3. **§3.3's promise** that each attacker-model paragraph "cites the evidence from its paper for each mark". About a dozen mark sentences carry no citation. Add the key, or say "gives".
4. **Arcuri and Cohen's d.** Arcuri, cited for the 1 000 runs, argues that the d family does not suit randomised algorithms. Should §6.5 own this in one line?
5. **The Masud/Kim asymmetry in Tables 3.3 and 6.1.** Kim's assumed evasion scores "in part", while Masud's stated RoA prioritisation scores "none". It is defensible under the predicate test, and both verifiers saw it.
6. **Bibliography leads.**
   - `rodriguez2024`: the PDF reads 2023, 15:1, doi 10.5753/jisa.2023.3902.
   - `mitre2026attackkb`: the saved copy postdates v20; re-save it from v19.1, or let the pinned bundle stand as the copy.
   - `ghosh2009nitrd`: its markdown is a different document from the cited report.
   - `ctid2025attackflow`: the PDF and HTML are v4.0, but the bib says v3.2.0.

## The mechanical exceptions to fix first

- L7615 "19 to 32 s" → **18 to 32 s**.
- L935 "more than 80 %" → **80 %** (Zhang and Table 2.4).
- L8597 and L9192: "about two thirds" against 0.63 (0.61, 0.65), an interval that excludes 2/3.
- L7856–7859: "the host-layer mechanisms … 0.96 or more" holds only for the layer averages.

The other ten are in the sheet. The two interval-format slips are already fixed.

## Already applied (your IEEE and interval rulings, 2026-10-16)

- Each reference number in its own bracket.
- The `Sect.` and `eq. (n)` pinpoint forms.
- 95 % intervals in parentheses, with Table 5.2's MTTC run counts reading "n runs".
