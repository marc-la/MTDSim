---
status: durable
created: 2026-10-16
updated: 2026-10-16
---

# Claim-by-claim check — protocol

**Status:** durable. How a session checks that every claim in the dissertation says what its source says, that every claim needing a source has one, and that no citation is decoration. Built for the near-final draft (2026-10-16), after the bibliography check had confirmed that every one of the 74 entries exists and is described correctly. The open run is [`../handoffs/2026-10-16_claim_by_claim_check.md`](../handoffs/2026-10-16_claim_by_claim_check.md).

The bibliography check answers *does this source exist, and is it described right?* This check answers *does this sentence say what that source says?* The second is where the risk sits: human-written papers get it wrong 15–25 % of the time, and AI-assisted text is worse (§2).

## 1. What can go wrong: the four outcomes

Every claim unit falls in one cell. The check exists to find the two error cells.

| | The claim needs this source, and the source supports it | The claim does not need a source, or this source does not support it |
|---|---|---|
| **Cited** | **True positive.** Keep | **False positive.** Decorative (attached, does no work), overstated (scope widened, hedge dropped, number drifted), misattributed (right claim, wrong paper), secondary (the source only reports another work's finding), or contradicted |
| **Uncited** | **False negative.** A claim the examiner "would have to look up" with no source: a number, threshold, definition, method, or a claim about the field or another work | **True negative.** Our own method, result or judgement, common knowledge for the reader, or covered by a citation in the same sentence or paragraph |

The checker makes errors too, and they are not symmetric. An agent that wrongly says *unsupported* costs Marc a minute. An agent that wrongly says *supported* lets a defect through, and LLM judges make exactly this error: they accept most invalid citations (§2). Every rule in §5 is there to push the checker's errors onto the cheap side.

## 2. What the literature says

Sources fetched 2026-10-16 unless marked *(snippet)*: seen only in search results, so not to be quoted in the dissertation.

- **Baseline rate, human writers.** A meta-analysis of 28 studies puts quotation errors at 25.4 % of citations, 11.9 % major: "the reference contradicted, failed to substantiate, or was irrelevant to the author's assertion" (Jergas & Baethge 2015, *PeerJ* 3:e1364). Secondary references were under a sixth of problems and counted as minor. In Nature, Science and PNAS, 25 % of 250 citations were faulty (Smith & Cumberledge 2020, *Proc. R. Soc. A*, *(snippet)*). Only about 20 % of citers read the original, estimated from misprints copied between citations (Simkin & Roychowdhury 2003, *Complex Systems*).
- **AI-assisted text.** GPT-4 fabricated 18 % of its references, and 24 % of its real ones carried substantive errors (Walters & Wilder 2023, *Sci. Rep.* 13:14045). Across 58 000 statement–source pairs, 50–90 % of LLM responses were "not fully supported, and sometimes contradicted" by the sources they cited. The typical failure is that unsupported statements "only partially deviate from their source" (Wu et al. 2025, *Nat. Commun.* 16:3615). That is the plausible paraphrase that overstates. Only 74.5 % of generative-search citations supported their sentence (Liu, Zhang & Liang 2023, Findings of EMNLP). A citation attached after the claim was written is *post-rationalisation*: the source fits the claim without having produced it (Wallat et al. 2024, arXiv 2412.18004).
- **This repo's AI-specific vectors.** Four come from the drafting history, not the literature:
  - The AI Use Declaration says Claude proposed the sentences of the abstract and Chapters 1 and 5–7.
  - Earlier sessions wrote some claims from memory (the old `VERIFY` comments).
  - Cites were "carried" through up to 44 redraft rounds while the sentence around them changed.
  - Some claims rest on a survey's report of a primary study, such as Carter's finding via Cho et al.
- **LLMs as judges.** LLM judges catch valid outputs ("True Positive Rate 96 %") but are "remarkably poor at identifying invalid ones (i.e., True Negative Rate <25 %)". Majority voting does not fix this; a minority veto helps (Jain et al. 2025, arXiv 2510.11822). Even a validated automated verifier agreed with expert consensus only 88.7 % of the time (Wu et al. 2025).
- **The test to apply.** A claim is attributable if a reader would affirm "According to P, s", applied "strictly, without making further assumptions" (Rashkin et al., *Measuring Attribution in NLG Models*, arXiv 2112.12870, §3.3.1). SciFact's verdicts each name the rationale sentences they rest on (Wadden et al. 2020, EMNLP, *(snippet)*).
- **What needs a citation.** Common knowledge is "information that the average, educated reader would accept as reliable without having to look it up". Statistics never are, and field knowledge counts only for that field's readers. "When in doubt, cite your source" (MIT, *Academic Integrity at MIT*, "What is common knowledge").
- **What examiners do.** Examiners "will be irritated by … references that are omitted or misreported … and citations and quotations that are misused". Once suspicious, they "will begin to check references, figures, spelling and quotations" (Golding, Sharmini & Lazarovitch 2014, *Assess. Eval. High. Educ.* 39(5), p. 569).
- **Policy.**
  - UWA's student AI guide makes it "the responsibility of the student to check the accuracy of all information generated by AI study tools". It also asks for "a clear indication of where in an assignment AI-generated material is used" (*Using AI Tools at UWA: A Guide for Students*, 2023, p. 4; the 2026 link was dead).
  - IEEE requires AI-generated content to be disclosed, with the sections and level of use identified (IEEE Author Guidelines for AI-Generated Text).
  - COPE: authors "are fully responsible for the content of their manuscript, even those parts produced by an AI tool" *(snippet)*.

**Implication.** Check exhaustively, not by sample. Expect roughly one cited unit in five to need some change and one in ten a major one. Treat no agent "supported" as final without a verbatim passage behind it and an adversarial second read.

## 3. The units, and the inventory

A **claim unit** is one prose sentence, caption, table row, equation or worded TikZ label in the submitted text. Scope is everything except Appendix A (the original proposal, an included PDF with its own references) and the bibliography. Comments are stripped first.

```
python tools/claim_inventory.py census          # counts by chapter, kind and tier
python tools/claim_inventory.py write           # data/claim_check/claims.jsonl + packets/<key>.md
python tools/claim_quote_check.py texts         # docs/sources/_text/<key>.txt, page-marked (gitignored)
python tools/claim_quote_check.py check V.jsonl # every agent quote found in its own source, or MISSING
```

A packet holds every unit citing one source, plus every uncited unit that names the source's first author. That second list is where misattribution and missing citations show up. A unit can hold several atomic claims. The verifying agent splits each unit into them, in the manner of FActScore's atomic facts, and gives each its own verdict. The census counts units; the verdict file counts claims.

Figures drawn as images from HTML (the chapter 2 figures and the Chapter 4 overview) are not in the inventory. Their text is checked by eye against the caption and §2.2 in the mechanical bundle (§7).

## 4. The decision tree: who checks what, and how hard

The tool assigns a provisional tier from surface features. An agent may raise a unit's tier but never lower it.

```
Cited unit?
├─ yes ─ borrowed number, threshold, rule, equation or pinpoint?  (R1) ─┐
│        cites the supervisor's work or the MTDSim lineage?         (R2) ─┤
│        source has no saved text to quote?                         (R3) ─┼─ any → H
│        claims an absence, a first, or what the field does?        (R5) ─┘
│        otherwise: cell of a sourced float (R4) or qualitative claim (R6) → V2
└─ no ── absence or field-wide claim?                               (R7) ─┐
         names a source's author, or reports a finding?             (R8) ─┼─ any → V1
         uncited cell of a sourced float: our choice or missing?    (R4) ─┘
         otherwise: our own method, result or cross-reference       (R9) → M
```

| Tier | Who checks | Marc reads it when | Why this tier |
|---|---|---|---|
| **H** | agent A + adversarial agent B, both quote | always, beside the quotes | the examiner checks these first, the supervisor knows these sources, or a mismatch is a number anyone can spot |
| **V2** | agent A + adversarial agent B, both quote | either says other than SUPPORTED, or a quote fails the check | qualitative claims, where overstatement hides |
| **V1** | one agent: does this need a source? | the agent says yes, or names a source | the false-negative screen |
| **M** | scripts plus one agent pass | only as a bundled exception list | our own floats, data, code and cross-references; checked against the artefact, not the literature |

Within a tier, take session-drafted units first: those whose comment trail says `SESSION-DRAFTED`, `ratify on read` or `VERIFY` (the `provenance` field of `claims.jsonl`), then units in the abstract and Chapters 1 and 5–7.

## 5. Verifying a cited unit (tiers H and V2)

**One source per pass.** An agent verifies one source's packet at a time, with that source's text open. This is the guardrails rule against cross-attribution. Several small packets may share an agent, but each gets its own pass and its own output. A large packet (`cho2020`, `brown2023`, `zhang2023`) is split by chapter.

**What agent A returns**, one JSON line per atomic claim, to `data/claim_check/verdicts/<key>.A.jsonl`:

```json
{"unit": "U0000", "key": "<bib key>", "claim": "<one atomic claim the unit makes on this source>",
 "verdict": "PARTIAL", "quote": "<verbatim from the source>", "locator": "p. 25 (printed)",
 "issue": "<what the source says that the claim does not, in one line>",
 "severity": "major", "fix": "tighten", "fix_text": "<minimal wording change, or empty>"}
```

- **Verdicts.**
  - `SUPPORTED`: the passage says it, at the claim's strength and scope.
  - `PARTIAL`: right direction, but overstated, scope widened, hedge dropped, number or unit drifted, or two papers conflated.
  - `UNSUPPORTED`: the source does not say it.
  - `CONTRADICTED`: the source says otherwise.
  - `SECONDARY`: the source says it only by reporting another work. Name that work.
  - `NOT-CHECKABLE`: no saved text, or the passage falls outside the saved copy.
  - `PLACEMENT`: the sentence's own claim is fine, but where the citation sits invites a reading the source does not support. For example, a citation beside a threshold the source never gives (pilot: `lakens2018equivalence` beside ±0.2, where the bound is Cohen's, one paragraph up). The usual fix is `move-cite`, or `keep` with the reason given.
  - `COVERED`, for an uncited unit in a packet that names the source's author: a citation nearby carries it. Name that unit.
- **Severity.** `major` is contradicted, unsupported, misattributed, or a wrong number. `minor` is partial wording, a wrong locator, or a secondary citation (Jergas & Baethge's split).
- **Fix codes.** Every fix is a proposal for Marc:
  - `keep`
  - `tighten` (say only what the source says)
  - `move-cite` (onto the clause it supports)
  - `replace-source`, or `add-source` (one of the 74, or a new one for Marc's to-download list)
  - `cite-primary`
  - `mark-ours` (reword as our choice or judgement)
  - `cut`
  - `fix-locator`
- **Quote rules.** The quote is copied from `docs/sources/_text/<key>.txt`, never paraphrased or tidied. An ellipsis is allowed only to join two passages that are each quoted exactly. A pinpoint in the dissertation (`p.~8`, `Eq.~13`) is checked against the *printed* page or number, which may differ from the PDF index the text cache marks. Never quote the abstract when the body says something narrower.
- **Strictness.** Apply the "According to [source], [claim]" test with no added assumptions. A source that makes the claim about a different system, attacker, metric or setting does not support it. A citation that would support a weaker version of the sentence makes it `PARTIAL`, not `SUPPORTED`.
- **Search tolerantly.** PDF text keeps ligatures ("Conﬁdentiality" will not match `grep confid`), splits words across lines, and garbles equations. Search with `grep -i` on a word stem short enough to avoid the ligature, or on a neighbouring word. Where an equation is garbled in the text, open the PDF page (the Read tool's `pages`) and quote the prose around it. Several texts hold a published copy and a preprint, so hits come in pairs; quote the published copy.
- **Printed pages.** The text cache marks PDF page indices; the dissertation's pinpoints use printed pages, and the offset differs by source (pilot: Arcuri +218, Alavizadeh +1 771, Lakens +258, Spearman +70). Give both in `locator`: "p. 244 printed (PDF p. 26)". The checker reports the PDF page it found the quote on, a cross-check on the agent's own.
- **Neighbours that lean on the citation.** A packet shows two units either side. If an uncited neighbour rests on this source, check it too, and record it under its own unit id.
- **The comment trail is a lead, never evidence.** Comments in the tex such as "Cho Sec. VI-A, l.477" say where an earlier session looked. Go there first, but quote the source.

**Agent B, the adversarial pass.** B gets the same unit and source text, but not A's verdict. Its instruction is to find the reason the citation fails: the overstatement, the different setting, the missing hedge, the secondary report. B returns the same format to `<key>.B.jsonl`.

**Then, mechanically:**

1. `claim_quote_check.py check` on both files. A `MISSING` quote voids that verdict, and the unit is re-run. This is the deterministic guard against an invented quote, and it also catches cross-attribution, since a quote must be found in *that* key's text.
2. **Minority veto, calibrated on the pilot.** A unit is cleared only if both A and B say `SUPPORTED` with found quotes. Any `major` from either verifier goes on Marc's sheet, and so does any `minor` that both verifiers raise. A `minor` that only one raises goes on a skim list beneath the sheet. In the pilot the adversarial pass raised a minor point on 12 of 16 unit–source pairs, so a raw veto would bury the one major under eleven minors. H units go on the sheet whatever the verdicts.
3. `NOT-CHECKABLE` units (no saved text: `cai2016`, `cohen1988statistical`, `efron1994introduction`, `marsan1995`, `engenuitynerve`, `uberbreach2022`) go to Marc with the claim and what he needs to look up. `tay2024code` claims are checked against the release as cited, at commits `f13ed49` (the agents) and `e6c13c6` (the evaluation notebook), with `git show <commit>:<path>`, never against today's working tree, which the thesis has changed; the locator is `<commit>:<path>:<line>`, and the quote check verifies it there.

## 6. The missing-citation screen (tier V1)

One agent per chapter reads every V1 unit in context, with the paragraph and its citations. It answers one of:

- `ours`: our method, result, choice or judgement, and says so or plainly reads so;
- `common`: the dissertation's reader (a CS honours examiner in MTD) would not look it up;
- `covered`: a citation in the same sentence or paragraph supports it, with the key named;
- `needs-source`: the agent greps `docs/sources/_text/` for a passage among the 74 that would support it, and quotes it, or says `new source needed`;
- `mark-ours`: a borrowed-looking claim (a number, a threshold, a "standard" practice) that is in fact our choice, and should say so.

Every R4 uncited cell of a sourced float is asked whether it is our choice. Table 5.1's caption states the rule: "Values without a citation are our choice". The check makes the caption true.

## 7. The mechanical track (tier M), reported as a bundle

Marc does not read these one by one. A session runs them and reports only the exceptions.

- **Our numbers.** Every number in the prose of Chapters 5–7, the abstract and Chapter 1 appears in a float or in the data the float's generator reads. Each float regenerates byte-identically from `data/results/` (the generators named in [`results_section_workflow.md`](results_section_workflow.md)).
- **Cross-references.** Each `Section~\ref`, `Table~\ref` and `Appendix~\ref` points at content that says what the sentence says it says (one agent pass over the 836 units, looking only at the pointers).
- **Our method against our code.** Out of scope here. It was evidenced by the tracer, the intent spec and the tests ([`../implementation/trace_tool.md`](../implementation/trace_tool.md), §6.5 T-items). Any M unit an agent reads as a claim about the literature is raised to V1.

## 8. IEEE in-text conventions: what to check

These come from the IEEE Reference Guide (V 3.28.2025, §I) and the IEEE Editorial Style Manual for Authors (2024), and are checked once, mechanically.

- **Author names are optional.** "As shown by Brown [4]" or "Wood et al. [7]" is grammatical, and so is a bare "[7]". Name the author only when the sentence reports that author's claim, method or words, as with a direct quote, a disagreement, or a method adopted. The name and number then refer to the same work. "et al." is used for three or more authors.
- **No year in the text.** IEEE in-text citation carries no year. A year column in a comparison table (Tables 3.3 and 6.1) is data, not citation, and is fine.
- **Pinpoints** read `[3, p. 5]`, `[3, Sect. 4.5]`, `[3, eq. (2)]`, `[3, Fig. 1]`, `[3, Table 3]`. The dissertation's `Sec.` and `Eq.` are close variants; harmonise them to one form. Under the house rule (memory: citation pinpoints), a pinpoint goes only on a direct quote or a borrowed equation, table, figure, algorithm or value.
- **A borrowed or adapted float** carries the reference number at the end of its caption.
- **Grouped references.** IEEE now writes every number out: `[1], [2], [3]`, not `[1]–[3]`. The build prints `[5, 29–31]` and `[42–44]`, because natbib's `sort&compress` groups into one bracket and compresses runs. Whether to change this is Marc's style ruling, not a fidelity defect.
- **Intervals.** Confidence intervals printed as `[0.10, 0.15]` share the citation's square brackets. A reader of Chapter 5 sees both. This is for Marc to rule on under [`results_presentation_standard.md`](results_presentation_standard.md).

## 9. Marc's review sheet, and the fix gate

The output is one sheet per tier, written to `data/claim_check/review_<tier>.md`. Each row carries:

- the unit and its location (chapter, section, tex line);
- the sentence;
- the source, with A's and B's quotes and printed locators side by side;
- the verdicts, the severity and the proposed fix.

Marc marks each row `ok`, `fix` (as proposed), `fix-other`, or `look` (he reads the source).

Fixes follow the edit gate. Chapters 1–5 and 7 and the front matter are proposed first and applied only on Marc's ruling; Chapter 6 and the appendices are applied after a ruling without a second round. Every fix is the minimal edit that makes the sentence true to the source: a word, a hedge, a moved citation. It is never a rewrite, and never drafted toward marks. A fix that changes a ratified claim's meaning is flagged as such on the row.

## 10. Done when

- Every cited unit has two found-quote verdicts, or has been marked by Marc.
- Every V1 unit has a screen answer, and every `needs-source` answer has been ruled on.
- The M bundle has zero unexplained exceptions.
- Marc has marked every row of the H sheet and every flagged V2 and V1 row, and the rulings are applied.
- The final rebuild still cites the same keys, unless a ruling added or dropped one. If one was added, it went through the bibliography check's procedure.
- The AI Use Declaration's sentence "I have read, checked and revised every sentence" is now backed by a record (`data/claim_check/`).
