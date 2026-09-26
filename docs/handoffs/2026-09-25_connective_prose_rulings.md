---
status: partially shipped
created: 2026-09-25
updated: 2026-09-26
---

# Ratify the applied connective prose (ch1–5), and rule the held items

## State of play

- **Shipped 2026-09-26.** Marc ruled R1–R4 (recorded in
  [`../workflows/connective_prose.md`](../workflows/connective_prose.md) §f
  and the registry): chapter closes only where the next chapter depends on a
  result; a thesis-structure overview in chapter 1, placed last; section as
  the subject of previews; *axes* → *properties*. Applied in the tex, each
  unit under a `[CONNECTIVE-PROSE PASS 2026-09-26, …]` DRAFT STATE comment,
  ratify on read:
  - ch1: the thesis-structure overview (after the contributions);
  - ch2: opener, §2.2 preamble, the §2.2.2 "IDS" tail, the one-sentence close;
  - ch3: opener, §3.1 preamble term, §3.1 close, §3.2 and §3.3 preambles,
    the §3.3.3 mis-aimed `\ref`, the close (the derived gap handed to ch4);
  - ch4: opener (roadmap re-keyed to all five sections, *properties*, the
    ruled signpost sentence), §4.1, §4.3 and §4.4 bridges, §4.4 preamble
    (connective part only — the 2026-09-25 "four bases" paragraph untouched),
    §4.5 preamble, *this thesis* → *this dissertation* ×3;
  - ch5 (Marc's ask, on the 2026-09-26 plain-description rewrite): opener
    ("replaces it" removed — the 2026-09-24 ruling), §5.2 head, §5.3
    preamble, §5.3.1 close, two closes cut; five false statements corrected
    against the tracked numbers (stealth "higher on both", "Every reduction
    falls", "the one property", "at most two-fifths", "Where one interval is
    reported"); the "has recovered" mechanism replaced by the by-construction
    window; "Eleven conditions:".
- The record: [`../implementation/connective_prose_audit.md`](../implementation/connective_prose_audit.md)
  (every unit's eleven-item check; ch5 is its second critique).

## What is left

### 1. Marc reads and ratifies (or reverts) the applied units

Grep `CONNECTIVE-PROSE PASS 2026-09-26` in `dissertation.tex` (40 sites). On
ratification, replace the comment with `RATIFIED <date>`; on rejection, revert
from git and record the rejection in the unit's comment so no pass re-flags it.

### 2. Held for Marc's ruling (not applied)

- **§5.3.3 heading** "Defence mechanisms and execution schemes" →
  "…and deployment strategies": MTDShield is in the subsection and the
  ratified row never calls it a scheme. Overturns the 2026-09-20 heading
  ruling. Recommend: rename.
- **ch5 S7** "MTDShield stays within 0.12 of service diversity …, which follows
  from its choice of service diversity at most decisions": a mechanism in the
  results. Recommend: delete the *which* clause unless it is Marc's reading.
- **ch5 S20** the MTDShield choice-share sentence beside its result (implies
  the mechanism); at 2 000 s neither MTDShield cell is told apart from zero.
- **ch5 S8** "matches / move together / separates" in §5.3.3 use neither
  declared test (interval excludes zero; shared Scott–Knott rank). Needs the
  per-interval ranks and per-profile intervals — T3.
- **ch5 S23 / §5.1 Runs** "ten times the 100 runs per condition of Zhang":
  decorative now that §4.5.4 grounds the count; overturns E5 (2026-09-23).
- **ch5 S24** no sentence reads $c_{\mathrm{agg}}$ or Figure 5.6's execution
  schemes, though the §5.3 preamble promises $c_{\mathrm{agg}}$ in §5.3.3 —
  one observation each, or drop the preamble clause.
- **§4.4 preamble length.** With the 2026-09-25 "four bases" paragraph it is
  still well over a preamble's scale; whether that paragraph moves into a
  subsection is a structure call.

### 3. Minor ch5 items (T1/T2 in the audit, §3 S9–S22; apply on a blanket accept)

Reversal frame ×3 (S9), "split the same way" (S10), user shuffle stated in two
subsections (S11), the "Because a run ends…" reason (S13), "lower by less"
(S14), "the model" / "This follows" (S15), stacked modifiers (S16), the 125 s
bin wording (S17), *intervals* in two senses (S18), user shuffle filed under
the service layer (S19), an *-ing* tail (S21), and four carried-over §5.1
items (S22: *with* tail, *rather than*, the three-clause lineage sentence,
"run as released: … choosing").

### 4. Flagged content (Marc's; not drafted)

- ch2/ch3: "why the network model is not surveyed" has no home (a ch3 comment
  thinks ch2's preamble carries it).
- ch4 §4.4.1: "our Petri nets can be mapped to anything" — a value close.
- ch4 §4.3 head link: "a data structure to pipe in the attack profiles" is
  weaker than the section's job (Figure 4.1: *make executable*); ruled.
- ch3 §3.1.2 close: "stable enough to model an attacker against" is uncited.
- ch1 contribution 3: "in two phases" (*phase* is reserved for the baseline
  attacker's six) and "two new measures" (the *metric* row) disagree with the
  chapters an examiner reads after it.
- ch6 plan comments point properties 6–7 at the retired
  `subsec:aio-capabilities`; re-point before the ch6 opener is drafted.
- *reference* collision: Marc's 2026-09-24 ruling calls the baseline attacker
  "the reference", ch5 reserves the word for the no-defence runs.

### 5. Re-check when drafted

The ch1 overview's clauses for chapters 6–8 describe their planned jobs; re-run
`connective_prose.md` §e on them, and on the ch6–8 openers, once drafted.

## Validation gate

Every applied unit ratified or reverted; §2 items ruled; the build clean with
no undefined references (`pdflatex` → `bibtex` → `pdflatex` ×2; `latexmk` is
not installed in this environment).

## Hard constraints

- Parallel sessions edit `dissertation.tex`; merge `dev` and re-read a unit
  before touching it (chapter 5 was rewritten under this pass once already).
- Chapters 1–3 impersonal in body prose; *we* from chapter 4.

## Reading list

- [`../workflows/connective_prose.md`](../workflows/connective_prose.md)
- [`../implementation/connective_prose_audit.md`](../implementation/connective_prose_audit.md)
- [`../workflows/evaluation_conventions.md`](../workflows/evaluation_conventions.md) §j (ch5 items)
