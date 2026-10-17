---
status: open
created: 2026-10-16
---

# Claim-by-claim check: every claim true to its source, every needed source present

## State of play

- **The bibliography is done** (2026-10-16). All 74 keys exist and are described correctly, and the report is archived at `~/mtdsim-sources-archive/2026-10-16/bibcheck/`. That check did not test whether any sentence matches its source. This one does.
- **The method** is [`../workflows/claim_check_protocol.md`](../workflows/claim_check_protocol.md): the four outcomes, the sourced evidence on error rates, the decision tree, the agent procedure, the review sheet and the fix gate. Load it before anything below.
- **Tools.**
  - [`tools/claim_inventory.py`](../../tools/claim_inventory.py) splits the submitted text into claim units and routes each to a tier.
  - [`tools/claim_quote_check.py`](../../tools/claim_quote_check.py) builds the page-marked source texts and confirms that every agent quote is verbatim in its own source.
  - Outputs go in `data/claim_check/`. The source texts are in `docs/sources/_text/`, which is gitignored.
- **Scope.** Everything except Appendix A (the original proposal) and the bibliography: pp. 1–54 and 61–75 of the 82-page build.

### The census (2026-10-16 build)

| | Count |
|---|---|
| Claim units (sentences, captions, table rows, equations, worded figure labels) | **1 285** (805 prose sentences, 46 captions, 335 table rows, 15 equations, 84 figure labels) |
| Units that cite at least one source | **206** |
| Source uses (unit × key pairs) | **273** (286 citation instances counting repeats in one unit; 239 `\citep` commands), over all **74** keys |
| **H**: Marc reads each beside two quotes | **98**: R2 supervisor or lineage 61, R1 borrowed number or rule 38, R5 absence or field-wide 18, R3 no text 6 (overlapping) |
| **V2**: two agents, Marc reads only if flagged | **108** |
| **V1**: uncited, screened for a missing source | **243** (92 absence or field-wide claims, 65 attributions or named authors, the rest uncited cells of sourced floats) |
| **M**: our own method, results and cross-references, checked as a bundle | **836** |
| Units under a session-drafted comment trail | 255 (133 in Chapter 3); 29 of the H units |

The **atomic claim** count is not known until the verifiers split each unit; that count lands in the verdict files. Sources with no saved text, so Marc's to check: `cai2016`, `cohen1988statistical`, `efron1994introduction`, `marsan1995`, `engenuitynerve`, `uberbreach2022`. `tay2024code` is checked against the released code.

### The high-risk surfaces, located

- **Sourced floats.** Every cited cell is H or V2, and every uncited cell is asked whether it is our choice:
  - Table 2.4, the lineage configurations;
  - Table 3.1, MTD metrics after Cho;
  - Table 3.2, the eight properties;
  - Tables 3.3 and 6.1, the model scores;
  - Table 4.2, the tactic durations;
  - Table 4.3, the metrics and their sources;
  - Table 5.1, the experimental setup, whose caption reads "Values without a citation are our choice";
  - Tables C.1, C.2, C.4 and D.1.
- **Equations.** The 15 of §4.3 and §4.5, two of them borrowed with pinpoints (`alavizadeh2022` Eq. 13; `royston2013` Eq. 1). The GSPN tuple follows `marsan1995`, which has no saved text.
- **Statistics.**
  - Cohen's d, "negligible within ±0.2", on `cohen1988statistical`, which has no text, so Marc must check it.
  - The equivalence rule on `lakens2018equivalence`.
  - The 1 000 runs "recommended for randomised algorithms" on `arcuri2014hitchhiker`.
  - Clopper–Pearson, bootstrap and Spearman.
- **The supervisor's work and the lineage.** `brown2023` (27 units), `zhang2023` (23), `tay2024` and `tay2024code` (18), `ho2024` (6), `hong2018` (6), `hongkim2012harm`, `hongkim2016`.
- **The gap claims**, which carry the thesis. "No standard set of metrics exists" (`cho2020`), "the most glaring flaw" (`jalowski2026`), and "That MTD attacker models in general lack the properties of an APT attacker is the finding of the two surveys" (`cho2020`, `jalowski2026`).
- **Claims an earlier session wrote from memory** (the bibliography check's group 2): `zhuang2012`, `marsan1984`, `marsan1995`, `cai2016`, `mendonca2023`, `evans2011`, `pendleton2016`, `saltelli2019`, `zaffarano2015`, `cremonini2005`, `hutchins2011`.

### Format findings (IEEE), for a style ruling, not fidelity defects

1. The build prints grouped and compressed brackets (`[5, 29–31]`, `[42–44]`) from `natbib`'s `sort&compress`. The current IEEE Reference Guide writes each number out: `[1], [2], [3]`.
2. Pinpoint forms mix `Sec.` and `Eq.`; IEEE uses `Sect.` and `eq. (n)`.
3. Confidence intervals in square brackets (`[0.10, 0.15]`) sit beside numeric citations in Chapter 5.
4. Author names before a citation appear 17 times. IEEE allows it, and the protocol (§8) says when it earns its place.

## Pilot (2026-10-16)

Wave 1 ran as the pilot: the statistics and metric sources, 9 keys, 15 units, 16 unit–source pairs, with verifier A and adversarial B. The sheet is [`data/claim_check/review_pilot.md`](../../data/claim_check/review_pilot.md).

- **Evidence held.** A gave 27 verdicts and B 29. All 56 quotes were found verbatim in their own source, with no fabricated passages, and the checker's PDF pages agree with the agents' own.
- **Defects.** There was one major: the Lakens citation sits beside a ±0.2 bound that Lakens advises against. One is probable but unchecked: the label "negligible" cited to Cohen seems to come via Tantithamthavorn. There is one method exposure: Arcuri, cited for the 1 000 runs, argues against the d family that §5.1 uses. About six minor defects remain: a locator, "after [x]" on two adapted metrics, "the minimum recommended", and an omitted ln(x+1) step.
- **Calibration.**
  - Both verifiers cleared only 4 of the 16 pairs. B raises a minor point on most units, so the routing rule is now: majors, plus minors both verifiers raise, go on the sheet, and one-sided minors go on a skim list (protocol §5).
  - The rate matches the literature: most citations are right in direction but imprecise, and about one in ten is major.
  - The defects that mattered sat one or two sentences from the citation, so packets now carry two units either side.
- **Fixed in the tools.** The checker's page lookup (it used the first word only), control characters that made grep treat OCR text as binary, and the protocol rules for ligature-tolerant search, printed-against-PDF pages and a `PLACEMENT` verdict.
- **Cost.** About 140–160 k tokens and 7–10 minutes per agent for a 9-source group. Marc's sheet is 7 rows plus a 4-line skim list for 15 units, so the whole run should give roughly 60–90 sheet rows plus the H rows not otherwise flagged.

## Run 1 (2026-10-16 to 17): how it ran, and how to resume

Marc asked for a token-lean run, so run 1 departs from §5's full two-agent pass in one way:

- **Role A on every cited pair.** One verifier per source group verifies each claim, then argues against its own `SUPPORTED` verdicts.
- **An independent adversary (role B) on every H unit only.** V2 units get A's self-adversarial pass but no independent B. A V2 row reaches the sheet on its own major, or through the skim list.

The brief every agent reads is [`data/claim_check/AGENT_BRIEF.md`](../../data/claim_check/AGENT_BRIEF.md), and the assignments are in `data/claim_check/assignments/` (A01–A10, B01–B04, S01–S03). M01 is the mechanical bundle.

**Resuming.**
- Each agent writes `data/claim_check/verdicts/run1/<key>.<A|B>.jsonl`, or `screen_<S>.jsonl`, key by key. A key is done when its file holds a row for every assigned unit.
- To list what remains, compare each assignment with the files, as this session's resume step did.
- `python tools/claim_review_sheet.py` rebuilds `review_sheet.md`, `review_cleared.md` and `stats.md` from whatever is on disk, re-checking every quote. It can be run at any time.

**What run 1 turned up**, before the remaining agents reported. There are 20 majors among the first 246 pairs.

*Numbers and rules from the code, cited to a paper.* The supervisor-lineage paragraphs of §2.2 take these from the MTDSim code but cite Zhang or Brown:
- 20 s minimum deployment time;
- 20 s confusion penalty;
- "never takes back … a stolen credential";
- the RoA formula;
- "15 s × (1 − AC)".

The usual fix is to add `tay2024code`, or move the citation.

*Attributions that overstate.*
- "Added to by Zhang" (Table 2.1), where all seven mechanisms are Brown's.
- "The 38 he trained" (Tay trained at least 49).
- "Four of its eight inputs" (eleven).
- The threats sentence crediting "the two surveys" with finding that attacker models lack "the properties".

*Citations that contradict the sentence.*
- Holm and Madan, cited for exponential tactic delays, both find the exponential a poor fit.
- Brown has user shuffle block credential stuffing, where §2.2 says brute force.
- Lakens is cited beside ±0.2, a bound he advises against.

*Bibliography lead.* The `rodriguez2024` PDF reads 2023, 15:1, doi 10.5753/jisa.2023.3902. This needs the bibliography check's procedure.

## Recommended approach

Run in waves, highest risk first. Each wave is an agent pair (A and adversarial B) per source group, one source per pass, then the quote check and the minority veto.

| Wave | Group | Keys | Units |
|---|---|---|---|
| 1 | Statistics and metric sources (the pilot) | arcuri2014hitchhiker, lakens2018equivalence, royston2013, jung2004, zaffarano2015, alavizadeh2022, clopper1934use, spearman1904proof, tantithamthavorn2017empirical; cohen1988statistical and efron1994introduction to Marc | 17 |
| 2 | Durations and metric lineage | holm2014, zhan2013, mcqueen2006, madan2004, bland2020, chobenasher2018, pendleton2016, rodriguez2024, hong2018, manadhatawing2011tse, cremonini2005, evans2011, mendonca2023, zhuang2012 | 29 |
| 3 | MTDSim lineage | brown2023; zhang2023; tay2024, tay2024code (against the code), ho2024, hongkim2012harm, hongkim2016 | 76 |
| 4 | The gap and the scored models | cho2020 (two splits by chapter); jalowski2026, kim2026, masud2025 (Tables 3.3 and 6.1) | 68 |
| 5 | APT, CTI and ATT&CK | alshamrani2019, cisaaa24038a, mtrends2026, hutchins2011, ghosh2009nitrd, nist2011sp80039, mandiant2013, chemat2024; mitre2026attackkb, mitre2026attackv19, strom2018mitre, ctid2025attackflow, ferraz2026, buchel2025, rahman2025, zhangY2025, alsada2024 | 56 |
| 6 | Formalism and validation | marsan1984, sargent2011, wohlin2012, saltelli2019; cai2016 and marsan1995 to Marc | 6 |
| 7 | Appendix CTI reports: does the report describe that campaign? | cisaaa22138b, the unit42, dfir, talos, cybereason, mcafee, volexity, malwarebytes and cso reports; engenuitynerve and uberbreach2022 to Marc | 21 |
| 8 | Missing-citation screen (V1), one agent per chapter group | ch1–2; ch3; ch4; ch5; ch6–7 and the declaration; appendices | 243 |
| 9 | Mechanical bundle (M) | number-to-float and float-to-data scripts; one cross-reference pass | 836 |

Waves 1–7 make about 22 agents, waves 8–9 about 8. That is above the default workflow size, so a session either launches them by hand in waves, or Marc asks for a workflow.

**Marc's time.** The figures below are estimates until the pilot calibrates them.

| Item | Time |
|---|---|
| The H sheet (98 rows at about a minute each, reading a sentence beside two quotes) | about 1.5–2 h |
| Flagged V2 rows (at the literature's rate, 20–25 of 108) | 30 min |
| V1 `needs-source` rows | 30 min |
| The six no-text sources, which need his own copy or memory | 20 min |
| The M bundle (exceptions only) | 10 min |
| **Total** | **3–3.5 h**, spread over sittings |

Alternatives considered:

- **A sample.** Rejected. At the literature's 15–25 % per-citation fault rate, a sample leaves defects, and the thesis has only 273 source uses.
- **A worksheet of only the bibliography check's groups 1–3** (about 40 rows). Rejected as the whole job: it has no false-negative screen, and it misses the supervisor-lineage and gap-claim surfaces. It is the same work as waves 1, 2 and 6, so it is subsumed.
- **One agent per unit.** Rejected. It loses the one-source-per-pass reading that catches conflation and wrong locators.

## Validation gate

Protocol §10. Every cited unit has two found-quote verdicts or a mark from Marc. Every V1 unit has an answer. The M bundle has no unexplained exception. Marc's rulings are applied. The rebuild's cited-key set is unchanged unless a ruling changed it.

## Hard constraints

- **The edit gate.** Fixes to Chapters 1–5, Chapter 7 and the front matter are proposed and applied only on Marc's ruling; Chapter 6 and the appendices are applied after a ruling. Minimal edits only: a word, a hedge, a moved citation. Never a rewrite.
- **Never assert a paper wrong.** A mismatch is between the sentence and the source; record what each says.
- **Safe file rewrite** for any edit to `dissertation.tex`: read, assert, write to a temporary file, then `os.replace`.
- **Copyright.** `docs/sources/` and `_text/` stay untracked. Verdict files quote short passages only.
- **New sources** go on Marc's to-download list, with bibliographic detail checked by the bibliography check's procedure.

## Reading list

- [`../workflows/claim_check_protocol.md`](../workflows/claim_check_protocol.md): the method.
- `data/claim_check/packets/<key>.md`: the units for one source, with context.
- [`../sources/INDEX.md`](../sources/INDEX.md): which sources have text, and the bibliography check's verdicts.
- [`../workflows/results_section_workflow.md`](../workflows/results_section_workflow.md): the float generators, for wave 9.

## Out of scope

- Rewording for style or voice.
- The proposal (Appendix A).
- Our method against our code, which is already evidenced by the tracer, intent spec and tests.
- The IEEE format rulings above. They are listed for Marc, not applied.
