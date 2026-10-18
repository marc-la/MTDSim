# Clausing check: brief for one cluster agent

You own one cluster of the final register pass on Marc's honours dissertation, `docs/thesis/dissertation.tex`; generated floats are in `docs/thesis/tables/`. Your work list is `data/clausing_check/worklists/<CLUSTER>.jsonl`. Each row gives:
- `origin`: a tex line `L<n>`, or `tables/<file>:<line>`;
- `flags`: why the thresholds picked the row;
- `text`: the plain text. Cross-references show as `1`, citations are stripped and maths shows as `x`.

**Read first:**
1. `docs/workflows/clausing_check.md` in full. It sets the classes K1–K8, what is *not* a defect, and the §4 seamless-edit rules.
2. In `docs/handoffs/2026-10-18_final_register_pass.md`, the calibration items 6–19 only. They are the format and judgement exemplar, and Marc read them as "about right".
3. `docs/workflows/voice.md`: §0, §d and §h only.

**How to work:**
- **A flag is a reason to read, never a reason to change.** Before judging a row, read its context in the tex (`sed -n` a few lines around the origin), not the whole file.
- **Expect to keep many rows.** Propose only where a named class rule clearly applies and the *after* is plainly better. Keep the rest, and record the warrant in one line.
- **Seamless edits (§4):**
  - rearrange the sentence's own words first;
  - the word delta is ≤ 0 where possible;
  - no new terms; use the words the body already uses;
  - never add a comma, colon or semicolon;
  - split a two-idea sentence rather than adding a connective;
  - keep every fact, number and citation;
  - add no new tells: no "not X but Y", no triads, no "serves as", no em-dashes.
- **House rules:**
  - Chapters 1–3 are impersonal (no *we*); *we* is licensed from chapter 4 on.
  - Numbers above ten are written as numerals.
  - Australian spelling.
  - Do not touch equations, citation keys or `\ref`s.
  - Sentence-case headings, with no acronyms other than APT and MTD.
- **Overlap:** if a row also has a defect owned by another cluster, fix it in the same *after*. Never return the same sentence twice.
- **Token economy:** Marc's budget is tight. Be terse. Read the minimum, and write no prose outside the file format.

**Output.** Write `data/clausing_check/clusters/<CLUSTER>.md` in exactly this form:

```
## <Cluster letter>. <cluster name>

**Rule.** <1–2 sentences: what the literature prescribes, with the source as cited in clausing_check.md §2.>

**The cluster-wide move.** <2–3 options for handling this cluster as a whole (e.g. split / reconnect / keep), each with one line of pros and cons, then **Recommended:** one, and why in a line.>

**Kept as warranted (<n>).** <one line each: `L<n>` — <warrant, ≤10 words>>

**Proposals (<n>).**

### <letter>.<k> · L<n> · <section name> · K<x>
> <before: the full sentence as printed>

**After:** <the full sentence as it would print>
Δ <words> · <why, one line naming the rule>. <Alt: only when the move is not obvious, one line.>
**Mark:** ok / alt / keep / look —
```

Order the proposals by line. The final message back to the orchestrator is three lines at most: counts kept and proposed, and anything you could not judge.
