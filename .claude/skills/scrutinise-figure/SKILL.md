---
name: scrutinise-figure
description: >
  Settle a dissertation figure (or table) top-down — a results figure, or a
  schematic one (method overview, pipeline, model or architecture diagram):
  define the takeaways the reader must leave with FIRST, then test the float
  against them with independent reviewers — a cold reader who sees only the
  figure, its caption and one introducing sentence, and a context critic who
  reads it against the thesis frame; for a schematic also a figure-only cold
  reader and a diagram auditor who runs the literature-derived pitfall
  catalogue (diagram_best_practice.md) — and rework until none reports a
  blocking defect. Use when Marc says "scrutinise figure X", "critique figure
  X", "does this figure work", "what does the reader take from this figure",
  "is this diagram clear", "critique the overview figure", or before any
  chapter 5 float is ratified. Not for house style alone
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

## Two kinds of figure, one method

- **Results figure** (chapter 5 floats; anything that plots a measure). The
  steps below as written.
- **Schematic figure** — a method overview, model diagram, pipeline, mechanism
  or architecture drawing (Figure 4.1 `fig:pipeline`, the chapter 2 model
  figures, the runtime loop, the Petri gadget). Same steps, with the
  schematic variants marked **[S]** below, and the design reference
  [`diagram_best_practice.md`](diagram_best_practice.md) loaded at step 0: the
  principles from the diagram literature, the corpus norms for an overview
  figure, and the pitfall catalogue with a mechanical test per pitfall. First
  schematic run: Figure 4.1, 2026-09-25 (record in
  `docs/handoffs/2026-09-22_ch4_overview_figure_family.md` §Scrutiny).

## Step 0 — load

- The section's standing context (for chapter 5: the results context handoff
  above; §1 reader, §3 results-paragraph rule and the by-construction test,
  §5 frame and vocabulary).
- `docs/workflows/figure_table_conventions.md`, `terminology.md`.
- **[S]** `diagram_best_practice.md` (this directory), and for an overview
  figure the introduction's approach paragraph and research sub-questions
  (the reader's only prior map of the method) and every section heading the
  figure's parts correspond to.
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

**[S] For a schematic figure** the takeaways are construction facts by nature,
so the by-construction test does not apply. Instead write:
- **The one-sentence restatement** the cold reader must be able to give (for
  an overview: the method, in the introduction's own words and order).
- **The part inventory**: each part the reader must leave knowing, what
  *kind* of thing it is (input data, a derived artefact, an operation, a
  runtime coupling, an existing system the work runs on), and what goes in
  and out. A figure whose parts are of mixed kinds but drawn alike is the
  commonest overview defect (catalogue P3).
- **The altitude test** for every element: does the reader need it *at this
  point* to restate the sentence? If not, it belongs in a zoom figure beside
  the section that explains it (the family ruling, 2026-09-09), not here.
- **The antecedent test**: every word on the figure is either one the reader
  already has (the introduction's terms, fixed thesis-wide) or one the figure
  itself defines by boxing it. A term defined only in the caption fails.

## Step 2 — the session's own critique, and Marc's

Marc usually gives his read first. Check every point of his against the data
and the generator (not against memory), and say upheld or not with the number.
Look in particular for: values hard-coded rather than measured; measures
capped by or dependent on the run count; intervals too small to see;
two units on one axis; axis words with no antecedent in chapters 2 to 4.

**[S] The inventory (do it by counting, before any opinion).** From the
rendered figure and the generator, tabulate: (1) top-level elements and
nested elements; (2) every arrow or line *kind* and the relation it denotes;
more than one relation drawn alike is a finding; (3) every text item with
its word count, and whether it has an antecedent; (4) every visual encoding
(colour, fill, dash, shape, frame, icon) and whether the caption decodes it;
(5) the caption's words, sentences and number of decodes; (6) how many
different visual grammars the figure uses (a graph on an axis, a matrix, a
net, a loop …); (7) whether the parts' names agree with the section
headings, the terminology registry and the introduction. Then run every
pitfall test in [`diagram_best_practice.md`](diagram_best_practice.md) and
record hit or clear for each, with the count that decides it.

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

**[S] Figure-only cold reader (always for a schematic).** A second, separate
cold reader who gets the PNG and the chapter title and NOTHING else: no
caption, no introducing sentence. A schematic figure should explain itself
(Rougier et al. 2014 rule 7 and the literature in the reference file); if this
reader cannot restate the method, the caption is carrying what the drawing
should. Ask them also to redraw it as five to seven boxes in words; the
answer is often the design.

**[S] Diagram auditor (always for a schematic).** A general-purpose agent
given `diagram_best_practice.md`, the PNG, the generator and the caption,
told to run every pitfall test in the catalogue mechanically and report
hit or clear with the count, and then say which three hits matter most for
this figure's reader. It checks the session's inventory independently; it
does not see the session's critique.

For the cold readers on a schematic add these questions: what kind of thing
is each part (data, step, system); what does each kind of arrow mean; what
do the labels' numbers or class words (L0, "level", "stage") suggest; which
words could you not interpret; what is in the figure you did not need.

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
- **[S]** Compare the two cold readers. Where the reader *with* the caption
  gets it and the figure-only reader does not, the caption is doing the
  drawing's job: the fix is a label on the drawing or a zoom, never a longer
  caption. Where both stall on the same element, that element is the first
  amendment. Set their five-to-seven-box redraws beside the part inventory:
  agreement between two cold redraws is strong evidence for the box set.
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
