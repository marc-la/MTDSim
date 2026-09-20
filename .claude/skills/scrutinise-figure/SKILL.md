---
name: scrutinise-figure
description: >
  Settle a dissertation results figure (or table) top-down: define the
  takeaways the reader must leave with FIRST, then test the float against
  them with independent reviewers — a cold reader who sees only the figure,
  its caption and one introducing sentence, and a context critic who reads it
  against the thesis frame — and rework until neither reports a blocking
  defect. Use when Marc says "scrutinise figure X", "critique figure X",
  "does this figure work", "what does the reader take from this figure", or
  before any chapter 5 float is ratified. Not for house style alone
  (figure_table_conventions.md), not for drafting the body text that reads
  the figure (Marc dictates it; this skill only hands over content points),
  and not for populating a float from a fresh corpus
  (results_section_workflow.md).
---

# Scrutinise a figure — takeaways first, then independent readers

First run: Figure 5.1, 2026-09-20 (record: results context §8,
`docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md`). Three designs; the
reviewers killed two. What they caught that the session and Marc had not: a
panel that was a construction fact drawn as a figure, a curve whose direction
ran against its claim, and a cross-model comparison counted in two different
units (which changed the baseline's result from "fixed" to "22 % branch").

## The rule the skill exists for

A figure is right when a reader who was not in the room takes from it the
takeaway it was built for, and nothing in it is true by construction. The
session that built the figure cannot test either; it knows too much. So the
test is delegated to agents that know less.

## Step 0 — load

- The section's standing context (for chapter 5: the results context handoff
  above; §1 reader, §3 results-paragraph rule and the by-construction test,
  §5 frame and vocabulary).
- `docs/workflows/figure_table_conventions.md`, `terminology.md`.
- The float: its tex environment (caption, label), its generator under
  `tools/`, the numbers file it reads, and a rendered PNG (the shell has no
  `pdftoppm`; use `gs -sDEVICE=png16m -r200` into the scratchpad).

## Step 1 — define the takeaways (before looking at the float critically)

Write a small table for the SUBSECTION, not the figure: each takeaway the
reader must leave with, in one plain sentence a computer science student could
repeat, and which float or body sentence carries it. Test each takeaway:

- Does it answer the subsection's question and tie to the research question?
- Could it have come out otherwise? A takeaway that is true by construction
  (a vocabulary size, a membership list, a declared input) is a body sentence,
  never a figure's job.
- Is every takeaway carried by exactly one place?

Marc agrees the takeaways before any redesign. They are the pass criterion.

## Step 2 — the session's own critique, and Marc's

Marc usually gives his read first. Check every point of his against the data
and the generator (not against memory), and say upheld or not with the number.
Look in particular for: values hard-coded rather than measured; measures
capped by or dependent on the run count; intervals too small to see;
two units on one axis; axis words with no antecedent in chapters 2 to 4.

## Step 3 — the reviewers (launch together, foreground, in one message)

**Cold reader (always).** A general-purpose agent told it is a final-year
computer science student, forbidden from reading anything but the one PNG.
It gets, pasted into the prompt and nowhere else: three or four sentences of
what the thesis has told the reader by this point, the one body sentence that
introduces the figure (content, as the thesis would have it), and the caption
verbatim. Ask: what do you see and take away from each panel; is the direction
(high or low, good for whom) clear; the figure's message in one sentence; what
it leaves unanswered; concrete fixes. Tell it not to be polite and not to
invent problems. NEVER give it the intended takeaways — the test is whether it
arrives at them.

**Context critic (always).** A general-purpose agent, read-only, given the
context file, the PNG, the caption's location in the tex, the numbers file,
the review history, Marc's scope rulings, and the author's doubts stated as
things to TEST rather than echo. Ask for a verdict per panel (passes, or one
named fix) tied to the context file's own rules; whether each takeaway is
delivered; whether any comparison is like for like; vocabulary and antecedent
breaches; whether the caption stays within "how to read it". Require it to
decide, and on a re-review to verify the previous fix independently from the
raw runs.

**Add when relevant:**
- *Numbers auditor* — when a measure is new or a value looks hard-coded:
  recompute every plotted value from the raw runs and diff against the
  numbers file and the drawing.
- *Convention reader* — when the figure's genre is in doubt: check it against
  `figure_table_conventions.md` and the corpus anatomies
  (`docs/implementation/evaluation_anatomies/`) for whether the field draws
  this kind of exhibit this way.
- *Sceptical examiner* — before a figure that carries a headline claim is
  ratified: what would an examiner attack (fairness of the comparison,
  sample size, what the control is)?

## Step 4 — align

Compare the cold reader's one-sentence message with the takeaways from step 1.
- It matches: the panel delivers.
- It is a different, true message: either the takeaway was wrong or the panel
  answers another question. Say which; do not bend the takeaway to the panel.
- It is "this could be a sentence": the panel is a construction fact. Demote
  it to the body text and find the measured quantity behind it (for Figure 5.1
  the entry matrix gave way to the share of steps per tactic).
Every reviewer finding is checked against the data before it is accepted;
reviewers are evidence, not authority.

## Step 5 — design amendments, ruling, apply

Give Marc the amendments as a short list (what is plotted, axis wording in
registered terms, direction, what leaves the figure and where it goes) with one
recommendation. He rules. Apply through the generator and the analyser, never
by hand in the tex; the caption says what the panels are and how to read them
and states no result. Session-written captions are marked DRAFT STATE for
ratification. Respect scope rulings (one float at a time unless told).

## Step 6 — repeat until clean

Re-render, re-run the cold reader (a FRESH agent, never the previous one; it
must stay cold) and the critic. Stop when neither reports a blocking defect.
Non-blocking remarks become content points for the body text.

## Step 7 — record and close

In the section's context file: the takeaways table, what was rejected and why,
the final panel definitions, the unit and fairness argument, the motivating
sentence the body text owes (content, not prose), exceptions to mark and not
explain, open checks. Update `FLOATS.md` and the findings record if a number
or measure changed. Build check, stage by file, commit on a session branch,
merge to `dev`, never push.

## What this skill never does

- Write the body text that reads the figure. It hands over content points.
- Explain a result. Reasons that are not true by construction are chapter 6's.
- Accept a reviewer's claim, or the session's own, without the number.
