# ch3_lit_review — notes feeding the Literature Review chapter

## What this chapter does

The literature review (ch3, after the background chapter) argues from the
literature that MTD has not been evaluated against an attacker that behaves like
an APT after its foothold. Its shape (as of the 2026-09-30 scrutiny, ledger
[`../../handoffs/2026-09-30_ch3_lit_review_scrutiny.md`](../../handoffs/2026-09-30_ch3_lit_review_scrutiny.md)):
three themed strands, each closing on its limitation, then the research gap:

- **§3.1 APT attacker behaviour** (SQ1): the APT and its lifecycle, ATT&CK, attack
  profiling and Attack Flow; closes on what the curated record lacks (tempo) and
  where the apparatus lives (outside MTD evaluation).
- **§3.2 MTD evaluation** (SQ3): defence modelling approaches, metrics
  (Table 3.1, the field map in Cho's frame), evaluation methods.
- **§3.3 Attacker models in MTD** (SQ2): the eight properties of an APT attacker
  that the literature says MTD attacker models lack (Table 3.2, fixed before any
  scoring), and a comparison of the MTDSim lineage, Masud and Kim against them
  (Table 3.3).
- **§3.4 Research gap** (promoted from §3.3.3 on 2026-10-01): the chapter-level
  close, drawn from all three strands.

Tables 3.2 and 3.3 are the chapter's main exports: chapter 4 builds toward the
eight properties and §6.3 scores the APT attacker model on them (Table 7.1). The
genre yardstick is
[`../../workflows/literature_review_conventions.md`](../../workflows/literature_review_conventions.md):
themes at the top with a chronology inside each, a funnel onto the gap (this
reconciles the 2026-08-11 "chronological story" framing with the 2026-09-08
recast); every cited work earns a sentence of evaluation; the scoring table states
its row rule and carries no aggregate. (Whole-document guidance:
[`../_writing_guide.md`](../_writing_guide.md).)

What lands here: *positioning and gap arguments* — research-gap statements, precedent
surveys, related-work framings. The distinction from `ch2_background`: background
describes the platform this work *inherited*; the literature review argues what the
field *is missing*, and occupies that gap. Rubric-gated
([`../../workflows/notes_rubric.md`](../../workflows/notes_rubric.md)).

Current notes: [`post_ingress_mtd_gap.md`](post_ingress_mtd_gap.md) — the thesis's
research-gap statement (the field's coverage bias toward the pre-foothold surface),
which the introduction's motivation compresses. [`tactic_duration_precedent_survey.md`](tactic_duration_precedent_survey.md)
— the precedent survey establishing that no prior work grounds per-tactic attacker
durations, and that declare-and-sweep is the field norm.

**Scope note:** the literature review was deliberately out of the prompt-corpus
mining exercise (2026-08-14) — these two notes were rehomed from `ch2_background/`,
not mined afresh. Populating this chapter from the review corpus is separate work.
