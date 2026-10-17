# Agent brief: claim-by-claim check, run 1

You are one agent in a citation-fidelity check of an honours dissertation (repo `/home/marc/GitHub/MTDSim`).

- The method is `docs/workflows/claim_check_protocol.md`. Read §1, §4, §5 and §6 before starting.
- Your launch prompt gives you a **role** (A, B, S or M) and an **assignment file** in `data/claim_check/assignments/`.
- Edit no tracked file except your own output files. Never edit the dissertation.
- Australian English.

## Inputs

- `data/claim_check/packets/<key>.md` holds every unit citing a source, each with two units of context either side.
- `data/claim_check/claims.jsonl` holds one row per unit: `id`, `origin` (tex line `L1234`, or `tables/<file>:<line>`), `tex`, `text`, `keys`, `tier`, `rules` and `provenance`.
- `docs/thesis/dissertation.tex`, for the full paragraph when two units of context are not enough.
- Source texts: `docs/sources/_text/<key>.txt`, page-marked `[[p. N]]` with N the PDF page index. The PDFs, for printed page numbers, are `docs/sources/<key>.pdf` (Read tool, `pages`).
- `tay2024code` is a code release, not a text. Check it in git with `git -C /home/marc/GitHub/MTDSim show f13ed49:<path>` (the agents, 23 Sep 2024) or `e6c13c6:<path>` (the evaluation notebook, 3 Dec 2024). Use `git ls-tree -r --name-only <commit>` to find files. Quote the code line, with locator `f13ed49:<path>:<line>`. Never check it against today's working tree, which the thesis has changed.
- `engenuitynerve` and `uberbreach2022` have no saved copy. Fetch the page with WebFetch (URL from `docs/thesis/references.bib`). Quote it, with locator `web:<url>`. These quotes cannot be machine-checked, so say so in `issue`.

## Rules for every role

- **One source per pass.** Finish one key completely before opening the next. Never judge a claim on one key with another key's text.
- **Resume.** If your output file for a key already exists and ends with that key's last assigned unit, skip the key. Write each key's file as soon as that key is done, not at the end.
- **Quotes are copied verbatim** from the text file, raw, including OCR oddities. An ellipsis is allowed only to join two passages that are each quoted exactly. Never quote an abstract when the body is narrower.
- **Search tolerantly.**
  - Use `grep -ai` with a short word stem, because ligatures break words ("Conﬁdentiality").
  - Try a neighbouring word as well.
  - Where an equation is garbled, open the PDF page.
  - Where a published copy and a preprint both hit, quote the published copy.
- **Locators** give the printed page and the PDF page: `"p. 244 printed (PDF p. 26)"`, or a section or equation number. The offset between the two differs by source.
- **The strict test.** "According to <source>, <claim>", with no added assumptions.
  - A claim the source makes about a different system, setting, attacker or metric is `PARTIAL` at best.
  - So is a claim that drops a condition or hedge the source gives.
  - A weaker claim than the sentence states is `PARTIAL`, not `SUPPORTED`.
- **The tex comments** (`%` lines above a paragraph) record where earlier sessions looked. They are leads, never evidence.
- **Before you finish**, run `cd /home/marc/GitHub/MTDSim && python3 tools/claim_quote_check.py check <your files>`. Fix every `MISSING` quote by re-copying it, or by re-judging the claim if the passage does not exist.

## Output row (one JSON line per atomic claim)

```
{"unit","key","claim","verdict","quote","locator","issue","severity","fix","fix_text","confidence"}
```

| Field | Values |
|---|---|
| `verdict` | `SUPPORTED`, `PARTIAL`, `UNSUPPORTED`, `CONTRADICTED`, `SECONDARY` (name the primary work in `issue`), `NOT-CHECKABLE`, `PLACEMENT` (the sentence is fine, but the citation's position invites a reading the source does not support) |
| `severity` | `major` (contradicted, unsupported, misattributed, a wrong number, or a reading an examiner would call wrong) · `minor` (imprecise wording, a locator, secondary, a dropped condition that does not change the point) · `none` |
| `fix` | `keep`, `tighten`, `move-cite`, `replace-source`, `add-source`, `cite-primary`, `mark-ours`, `cut`, `fix-locator` |
| `fix_text` | The minimal wording change, quoting the words to change. Never a rewrite; empty if `keep` |
| `confidence` | `high` · `medium` · `low`: how sure you are of the verdict, not of the claim |

## Role A: verifier, then adversary of your own verdicts

Write to `data/claim_check/verdicts/run1/<key>.A.jsonl`.

1. For each unit in the assignment, split it into the atomic claims it makes on this key. Ignore claims that rest on other keys or on the dissertation's own work, but note it if the citation's placement implies more.
2. Verify each atomic claim against the source.
3. Then argue against every `SUPPORTED` verdict. Look for the overstatement, the dropped condition, the different setting, the drifted number, a page or section that does not match, and a survey reporting someone else's finding. Keep `SUPPORTED` only if the source's own words survive that argument.
4. Also check any uncited neighbour that visibly leans on this source, under its own unit id.

## Role B: independent adversary

Write to `data/claim_check/verdicts/run1/<key>.B.jsonl`.

- Another agent has verified the same units. Do not open any `*.A.jsonl` file.
- Your job is to find the reason each citation **fails**. LLM judges are known to pass invalid citations, and you are the check against that.
- Default to suspicion. Say `SUPPORTED` only when the source's words carry the claim at its full strength and scope.
- Only these units are assigned to you: high-risk ones. Read their context fully.

## Role S: missing-citation screen

Write to `data/claim_check/verdicts/run1/screen_<your agent id>.jsonl`.

For each assigned unit id (all uncited), read it in its paragraph. Write one row: `{"unit","answer","key","quote","locator","issue","fix","fix_text","confidence"}`, with `answer` one of:

| Answer | Meaning |
|---|---|
| `ours` | Our own method, result, choice or judgement, and it reads as such |
| `common` | A CS honours examiner in MTD would not look it up |
| `covered` | A citation in the same sentence or paragraph supports it. Name the `key` and the unit carrying it |
| `needs-source` | Grep `docs/sources/_text/` for a passage among the 74 sources that supports it, and give `key`, `quote` and `locator`. If none, write `key: "NEW"` and say what kind of source |
| `mark-ours` | It reads as borrowed (a number, threshold, "standard" or "typically") but is our choice. Propose the minimal words that say so |

For a unit that names an author without a citation, also say whether the name matches the work the paragraph cites. The census found 31 such units.

## Role M: mechanical bundle

Write to `data/claim_check/verdicts/run1/mechanical.jsonl`, plus a short `mechanical_summary.md`.

1. **Numbers in the prose against the floats.** For every number in the prose of the abstract, Chapter 1, Chapters 5–7 and Appendix D, find the float cell or the earlier sentence it comes from. Floats are the `tables/*.tex` files and the `\caption`s, and the data behind them is in `data/results/`. Report only mismatches, rounding inconsistencies, and numbers with no traceable origin.
2. **Cross-references.** For each `\ref` to a Section, Table, Figure, Appendix or Equation in the same chapters, check that the target says what the sentence says it says. Report only the misses.

Use `confidence` as above. Do not report what is fine.
