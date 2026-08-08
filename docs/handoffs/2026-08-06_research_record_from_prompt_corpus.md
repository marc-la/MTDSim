---
status: open
created: 2026-08-06
updated: 2026-08-08
---

# Mine the session transcripts for Marc's own prompts, and land them as a research record — the intent, the reversals, and the abandoned paths that no shipped document holds

> **Stage 0 has run (2026-08-08). Stages 1–3 have not, and this brief cannot be
> fully retired when they do** — see § *Stage 0 — done* and § *Why this stays open
> past Stage 3* below, both of which override the body where they disagree with
> it. The corpus is now backed up and the extractor is committed; the pinned
> sanity figure has been **re-pinned**, because reproducing it uncovered a filter
> the original survey lacked.

## State of play

### What is being asked, and the one thing that has to be settled first

Three and a half months of work with this assistant have left a transcript corpus
outside the repo. Marc's reading of it is correct and is the premise of this brief:
**the prompts are the record of human intent; the assistant's output is an
execution layer.** Where the two disagree about what the research *was*, the
prompts win. The dissertation's design, implementation, evaluation and discussion
chapters all need material that currently exists only there — in particular the
*negative space*: what was tried and abandoned, what was reversed, and why.

The ask was for "a full annal of the research process in `docs/notes` and
`docs/implementation`". Half of that cannot be done as stated, and the next
session should not discover this halfway through. [`../workflows/notes_rubric.md`](../workflows/notes_rubric.md)
says a note is "**not**: a session log, an investigation record, a decision
register with commit hashes, a QA audit, a to-do list", and the placement
criterion in [`../workflows/docs_map.md`](../workflows/docs_map.md) routes audit
trails to `implementation/`. An annal is, definitionally, all of the banned
things. So the deliverable splits:

| Consumer | What lands there | Where |
|---|---|---|
| Future sessions | the annal itself — dated, sourced, chronological, internal vocabulary free to use | **`docs/implementation/research_record/`** (new subtree) |
| The dissertation | only what the mining *earns*: an argument, a defence, a limitation — each clearing the rubric's seven tests | `docs/notes/ch3`–`ch6/` |

This is not a narrowing of the ask. It is the same two-consumer principle
`docs_map.md` is built on, and it protects the notes layer, whose value is
entirely in its entry bar. The annal is the primary source; the notes are what
the primary source supports. Expect the annal to be large and the notes to be
few — perhaps six to ten — and treat a large note count as a symptom that
session-log material has leaked through the gate.

### The corpus, measured

Not estimated — counted, on 2026-08-06, by parsing every transcript. The probe
scripts are reproducible and Stage 0 below turns them into a committed tool.

> **Superseded 2026-08-08 by the committed tool.** The figures below were taken by
> an uncommitted probe and they are not all reproducible; the word mass in
> particular is 5.5 % too high, for a reason that matters. Read § *Stage 0 — done*
> for the corrected table. The claim the table exists to support — that the long
> prompts carry the argument mass — survives unchanged.

| Quantity | Value |
|---|---|
| Top-level session transcripts | **110** (104 in `~/.claude-acc1`, 6 in `~/.claude-acc2`) |
| Nested files (subagent transcripts, tool results) | 343 — **all of it assistant execution detail; excluded** |
| Total on disk | ~230 MB |
| Human-authored records after stripping harness wrappers | 550 |
| Of those, substantive (≥ 15 words) | ~367 |
| **Human prompts ≥ 150 words — the design-argument corpus** | **73, totalling 63 900 words** |
| Distinct git branches touched | 21 |
| Date range (internal timestamps) | 2026-04-19 → 2026-08-06 |

**The 73 are the corpus.** They carry 72 % of the substantive word mass in 20 %
of the records, and the sample read during this survey confirms what the shape
suggests: the long prompts are where scope is set, a supervisor's advice is
metabolised, a design is argued, or a direction is reversed. The short ones are
overwhelmingly steering — "yes", "commit that", "no, do the other one". Sixty
thousand words is a week of careful reading, not a research programme, which is
what makes this brief worth executing rather than deferring.

Their distribution is uneven and that is itself a finding: **8 in April, 48 in
July, 17 in the first six days of August.** July is when the thesis took its
current shape.

### Two things the corpus does not contain

**1. May and June are missing entirely — and this is benign.** `dev` carries
**92 commits** across those two months (84 in May, 8 in June); there are **zero**
transcript records with a May or June timestamp in any of the three account
stores. The account-level `history.jsonl` files are ring buffers of ~20 records
holding only April, so they are not a recovery path. This was checked directly
and is not an artefact of how the files were selected.

It costs this exercise nothing, because **that window was introduction and
literature-review work** (Marc, 2026-08-06), and both chapters are scoped out of
this brief. Record the blackout in the annal as a one-line boundary with its
explanation attached, so a future session does not mistake it for data loss and
go hunting. Do **not** spend a stage reconstructing it from `git log` and quoted
supervisor updates: that would be reconstructing the one part of the thesis this
brief does not serve. The April→July gap in the record is therefore a gap in the
transcripts, not a gap in the research record this brief produces.

**2. The assistant is not a witness to Marc's reasoning, only to its
expression.** A prompt records the intent Marc chose to articulate at a moment.
It is not evidence of what he believed and did not type, and — this is the rule
that matters most for the annal's integrity — **it is not evidence of what is
true now.** Several of the most forceful prompts in the corpus were later
reversed. This is the same principle as the retire-by-evidence rule the handoffs
directory already runs on: a document's self-report is evidence about the day it
was written.

### There is a precedent, and it has a defect worth not repeating

This extraction has been done once, for a different purpose:
`voice_corpus_prompts_2026-07.txt` in the assistant's memory directory — 322 KB,
**142 prompts**, pulled on 2026-07-13 to ground the sentence-level rules in
[`../workflows/voice.md`](../workflows/voice.md). It is a flat dump keyed only by
session filename: **no timestamp, no branch, no triage.** For voice evidence that
was sufficient. For an annal it is not — chronology and branch are exactly what
turn a pile of prompts into a research record, and without them a claim in the
annal cannot be dated or cross-referenced against the commit that acted on it.

Reuse the idea; discard the format. And note the coverage gap: that pull predates
the July 22–23 and all August work, so it covers well under half of what now
exists.

It is a **format precedent only**. That pull mined the corpus for *how Marc
writes*; this one mines it for *what he decided and why*. The extraction
mechanics are shared and the findings are not, so do not treat any conclusion in
the voice record as evidence about content — and do not let a prompt's
stylistic interest earn it a place in the annal.

### The duplication risk, which is the main way this goes wrong

A great deal of this rationale is **already recorded** — often better than the
prompt that prompted it. `architecture.md` carries a decisions log with the
single-RQ and defender-frozen blocks. `intent_conformance_audit.md` carries
D-01..D-38 with costed options. `apt_model_criterion.md` carries the per-axis
badges. The handoffs `README.md` carries the boundary programme's closure. And
this repo's commit messages are unusually substantive — several are three
paragraphs of design argument.

A session that transcribes all 73 prompts into a new document will produce 60 000
words that mostly restate shipped records, and the annal will be worth less than
the sum of its sources. **The mining must be gap-driven.** For every triaged
prompt the question is not "what does this say?" but "**is this rationale already
in a shipped record?**" — and if it is, the entry is a one-line pointer, not a
retelling. What survives that test is the genuinely unrecorded material, and on
the evidence of this survey that will be concentrated in one band: the
abandonments and reversals, which no document in this repo currently owns because
shipped records describe what *is*, not what was discarded on the way.

**But "already recorded" is a two-way test, and the second direction is the more
valuable one.** Ideas developed over three months; the documents that carry them
did not always keep up (Marc, 2026-08-06). So when a prompt and a shipped record
disagree, there are two readings, and the triage must decide between them rather
than defaulting to either:

- the **prompt is superseded** — a position later abandoned, which the record
  correctly reflects. Disposition `already-recorded`; the prompt may still earn
  an annal entry as part of a reversal thread.
- the **record has drifted** — the thinking moved on and the document lagged. The
  prompt is the *later* evidence, and the shipped record is quietly stale.

The second case is a real finding and one this exercise is unusually well placed
to catch, because it is exactly what nobody notices from inside a working
session: staleness is invisible until you read the intent and the artefact side
by side, months apart. Chronology decides it — which is why Stage 0 carries
timestamps and Stage 1 reads in date order. The disposition list below therefore
has **five** entries, not four, and the drift flags are an output of this brief
in their own right.

## Stage 0 — done (2026-08-08)

Both halves of it: the corpus is backed up, and the extractor is committed as
[`../../tools/prompt_corpus.py`](../../tools/prompt_corpus.py) with the filter set
and its provenance in the module docstring rather than in a session's memory.

**The snapshot** is `~/mtdsim-corpus-snapshot/2026-08-08/` — outside `~/.claude*`,
outside the repo, untracked, with a `README.md` and a `MANIFEST.sha256` over all
290 files. 112 top-level transcripts, 237 MB, both account stores including their
nested subagent directories. 105 of the 106 `acc1` transcripts verify
byte-identical against the live store; the one mismatch is the transcript of the
session that took the snapshot, still being written, which is the reason a live
capture can never be perfectly clean.

**The corpus, re-measured** by the committed tool. `stats` reproduces this table
on demand, which is the point of it:

| Quantity | 2026-08-06 survey | 2026-08-08, committed tool |
|---|---|---|
| Top-level transcripts | 110 | **112** |
| Nested files (excluded) | 343 | **355** |
| Human-authored records | 550 | **464** |
| Of those, substantive (≥ 15 words) | ~367 | **313** |
| **Human prompts ≥ 150 words** | **73 / 63 900 words** | **77 / 61 164 words** |
| Distinct git branches touched | 21 | **25** |
| Date range | 2026-04-19 → 2026-08-06 | 2026-04-19 → **2026-08-08** |
| Month distribution, ≥ 150 band | 8 Apr / 48 Jul / 17 Aug | **7 Apr / 47 Jul / 23 Aug** |

The counts that *grew* are the two new sessions; that is the tool working, as the
brief predicted. The counts that *shrank* are the finding.

**The sanity gate is re-pinned, and reproducing it found a filter the survey
lacked.** Over the survey's own date bound the tool measures **73 prompts** — the
same count — but **60 399 words**, 3 501 short of 63 900. The difference is fully
accounted for. Two records in the corpus open `This session is being continued
from a previous conversation`: they are **compaction continuation summaries, which
the assistant writes about itself**, and they carry 2 464 and 1 161 words. Add
them back and the total is 64 024, within 124 words of the survey's figure.

So the survey counted the assistant summarising its own execution as part of
Marc's design-argument corpus — 5.5 % of the word mass it reported, and the single
longest "prompt" of that April. This is the brief's own thesis turning up in its
own measurement instrument, and it is the sharpest available argument for why the
extractor had to be committed rather than re-derived per session. The rule is now
in the tool's `DROP_PREFIXES` with that reasoning attached, and the residual 124
words is wrapper handling that cannot be attributed further, because the probe
that produced 63 900 was never committed.

The gate therefore now reads **73 prompts / 60 399 words at ≥ 150 words, timestamp
≤ 2026-08-06**, and passes identically against the snapshot and the live store —
which is itself the check that the snapshot is faithful. `gate` prints the
superseded figure alongside, so the correction cannot be lost. Re-pin deliberately
if the filter set is extended again, and say why.

**One thing Stage 1 should expect from this.** The filter set was verified in both
directions, not just forwards: none of the 31 task-notification records carries
appended human text, and none of the 61 compaction preambles does either, so
dropping them loses nothing. The corpus the tool emits is therefore clean of
assistant prose as far as this pass could establish — but the two continuation
summaries were found by *reading the length ranking*, not by the filter set, and
that is the technique to repeat when the corpus next grows.

**No new subtree yet, so nothing to register.** `docs/implementation/research_record/`
is Stage 2's to create, and `docs_map.md` gets its entry in that commit, not this
one. An empty registered subtree would be worse than none.

## Why this stays open past Stage 3

**Marc, 2026-08-08:** the implementation is still being finalised over the coming
week — specifically the **per-axis measurement metrics for learning capability
(axis 7), MTD evasion (axis 8) and stealth (axis 5)**, and the **retraining of the
Tay 2024 model** for pulling results. That is the work on the open chain's items
(1), (2), (3) and (5), and it changes this brief's lifecycle rather than only its
timing:

- **Stages 1–3 stay deferred**, on the reasoning already in § *When to run this* —
  which the caveat strengthens rather than replaces. `record-drifted` cannot be
  assessed against records that are still moving, and the three axis metrics are
  exactly the records it would be measured against.
- **A second extraction pass is owed after they land**, and it is not optional
  bookkeeping. Evaluation intent (band 4) is the thinnest band in the corpus
  *because the evaluation has not happened yet*; the prompts that set the axis
  metrics and sanction the retrain are the ones a `ch5_evaluation` note would rest
  on, and they are being written now. Re-run `gate`, then `stats`, and triage only
  the prompts added since — which is what the disposition table is keyed by `uuid`
  for.
- **So completing Stages 1–3 does not retire this brief.** It becomes a brief for
  the delta, and the retirement condition is that the corpus has stopped growing
  in ways the dissertation depends on — not that the annal exists.

Recording this here rather than acting on it: the axis work is out of scope for
this brief in both directions, and a prompt written this week is the weakest
possible warrant for touching the record it comments on.

## Recommended approach

Four stages. **Stage 0 has run** — see above. Stages 1–3 are one session each at
minimum; Stage 1 is likely two.

### When to run this — Stage 0 now, Stages 1–3 in about a week

Marc is holding the analysis until the implementation firms up, with roughly 90 %
of it expected in place and first results being pulled within the week
(2026-08-06). **Restated and narrowed 2026-08-08** — the week's remaining work is
now named, and § *Why this stays open past Stage 3* carries what it changes. That
is the right call and it is a scheduling decision, not a deferral, for three
reasons:

- **The corpus is still being written.** The next week of implementation and the
  first results run will generate some of the most dissertation-relevant prompts
  in the whole record — evaluation intent (band 4) is currently the thinnest
  band, and it is thin because the evaluation has not happened yet. Mining now
  guarantees a second pass later.
- **`record-drifted` needs a settled record to measure drift against.** Running
  the staleness test while the implementation is still moving produces flags that
  are noise about a week-old document rather than findings about a stale one.
- **`ch5_evaluation` notes cannot be written before results exist.** An
  evaluation-framing note whose claim depends on an unrun experiment has to say
  so under the rubric, which is a weak note by construction.

Stage 0 is the exception and should not wait, because it is the only stage that
protects against loss rather than producing analysis — and because the extractor
is re-runnable by design, so running it today costs nothing when the corpus grows.
Expect the re-run to exceed the numbers pinned below; that is the tool working,
not drifting. Re-pin the sanity gate at Stage 1 against the corpus as it stands
that day.

### Stage 0 — snapshot the corpus, then build the extractor (do this first)

> **Done 2026-08-08** — § *Stage 0 — done* carries what it produced and the one
> correction it forced. The rest of this section is kept because it is the
> derivation of the filter set, and a future extension of the tool needs it.

**The corpus is unbacked and lives outside the repo,** in two account-scoped
directories under `~`. A Claude Code reinstall, an account cleanup, or a routine
`~/.claude*` prune destroys three and a half months of irreplaceable primary
source. Nothing else in this brief matters if that happens, so snapshot before
analysing.

Then commit an extractor as `tools/prompt_corpus.py`, matching the existing
`tools/` convention (`des_step.py`, `mtd_cost_bench.py`). It should be a living
tool in the sense [`../implementation/trace_tool.md`](../implementation/trace_tool.md)
means it — extended rather than re-written ad hoc — because it will be re-run as
new sessions accumulate.

Extract one record per human prompt carrying **`timestamp`, `sessionId`,
`gitBranch`, `cwd`, word count, text** — the four fields the voice-corpus pull
omitted. Keep it to a stable JSONL so triage decisions can be attached to records
by `uuid` rather than by line number.

The filter set below is not a guess; each rule was derived from a wrapper
actually found in this corpus, with counts where they matter.

Drop the record when:
- `type != "user"`, or `isSidechain == true` — sidechain records are subagent
  turns, i.e. the assistant talking to itself;
- `message.content` is a list whose blocks are `tool_result` — tool output, not
  speech;
- the text is a `<task-notification>` block (**30 found**) — harness-injected
  subagent completions, which are long and read like prose, and which polluted
  the top of the length ranking on the first pass of this survey;
- the text opens `Base directory for this skill:` (**11 found**) — skill
  preambles, same problem;
- the text opens `Caveat: The messages below` (compaction preamble) or
  `[Request interrupted`.

Strip these wrappers but **keep** the surrounding record, which is Marc's:
`<system-reminder>`, `<local-command-stdout>`, `<command-name|message|args>`,
`<ide_opened_file>`, `<ide_selection>`. Re-test emptiness after stripping.

Sanity gate for the tool: it must reproduce **73 prompts at ≥ 150 words and
63 900 words** on today's corpus. If it does not, the filter set has drifted and
the discrepancy is a bug in the tool, not a new finding.

> **Re-pinned 2026-08-08 to 73 prompts / 60 399 words** at the same bound. The
> instruction above was right in spirit and wrong in one particular: the
> discrepancy turned out to be a bug in the *survey*, not in the tool — the
> survey's word mass includes two assistant-authored compaction summaries. Reaching
> the pinned figure would have meant admitting 3 625 words of the assistant's own
> prose into the record of Marc's intent. The gate now lives in the tool
> (`python tools/prompt_corpus.py gate`) and prints both figures.

### Stage 1 — triage all 73, and record a disposition for every one

Read them in **chronological order**, which is the order the thinking happened
in, and classify each into one of seven bands. The bands are not generic
prompt-mining categories; they are the shape this project's decisions actually
took, drawn from the sample read during this survey.

1. **Direction-setting** — thesis scope, the single-RQ decision, what was culled.
2. **Design rationale** — why a modelling choice was made this way.
3. **Implementation constraint** — "we cannot do X because Y".
4. **Evaluation intent** — which metrics matter and why they were chosen.
5. **Abandonment or reversal** — a path dropped, a ruling overturned. **The
   highest-value band; no shipped record owns it.**
6. **Methodological correction** — Marc correcting the assistant's method rather
   than its output. Several of these have already hardened into standing rules
   (classify against the intent spec before calling anything a bug; a sweep
   licenses what was measured, not why; retire a handoff whose premise is
   falsified). Cross-check against the assistant's memory files before treating
   any as new, and expect this band to *confirm* rather than extend.
7. **Noise** — refactors, context management, git chores, tool wrangling.

Then attach one of five dispositions, and attach one to **every** prompt — a
prompt dropped silently is indistinguishable from a prompt never read, and the
completeness of this table is what makes the annal trustworthy:

- `already-recorded` → cite the file and section; no annal prose.
- `record-drifted` → the prompt post-dates the record and the record did not keep
  up. Cite the file, the prompt's date, and the specific divergence. **Flag for
  Marc; do not edit the record** (see hard constraints).
- `annal-entry` → unrecorded rationale; goes to Stage 2.
- `note-candidate` → carries a dissertation argument; goes to Stage 3.
- `noise` → band 7.

`already-recorded` and `record-drifted` are separated by chronology, not by
confidence: if the prompt is the later evidence and the record does not reflect
it, it is drift, whatever the prompt's tone.

Land this as a table in the new subtree. It is the audit trail for the claim
"the corpus has been read", and it is what lets a future session re-run the
mining against only the prompts added since.

### Stage 2 — the annal, organised by decision thread rather than by date

The instinct is a diary. Resist it: **`git log` is already the chronological
record**, and a second one adds nothing. What `git log` cannot show is a decision
that took six weeks and three reversals to settle, because each commit sees only
its own day.

So: a thin **chronological spine** — one line per session, dated, with the intent
in a clause, and the blackout marked — and thick **thread files**, one per
decision that moved. A thread states what was asked, when; what was decided; what
was abandoned and why; and where it landed. Threads visible in the corpus survey
and the branch names include the abandoned package restructure, the frozen
defender scope, the primary-metric choice, and the outcome-overlay weighting —
Stage 1 will name the rest.

Threads are the right unit because they are what the discussion chapter needs and
what a returning session needs, and because a thread that turns out to be fully
covered by an existing record can be collapsed to a pointer, which a diary entry
cannot.

Register the new subtree in `docs_map.md` **in the same commit that creates it** —
that file's contract requires it.

### Stage 3 — the notes the mining earns

Only band 2–5 material, only where it is an argument.

**Four documents govern this stage, and all four are binding — not one of them is
a suggestion.** Load them before drafting, in this order:

1. [`../notes/_writing_guide.md`](../notes/_writing_guide.md) — **the one to read
   first, and the one most likely to be skipped.** It states the one-line job of
   each part of the dissertation, the drafting order, and how the notes system
   maps onto it. A note drafted without it tends to be well-written material
   aimed at no particular chapter job, which is the most expensive kind of note
   to fix later because nothing about it looks wrong.
2. [`../notes/_template.md`](../notes/_template.md) — **the required shape**, not
   a starting suggestion: frontmatter (`status`, `chapter`, `created`,
   `updated`), then *Position in the dissertation*, *The idea*, *Evidence and
   repo anchors*, *Revisit conditions*. Every note uses these sections, in this
   order. The *Evidence and repo anchors* footer is the **only** place a repo
   path may appear — which matters more here than usual, since this stage's raw
   material is full of file paths and session detail.
3. [`../workflows/notes_rubric.md`](../workflows/notes_rubric.md) — the
   seven-test cross-examination, run before committing each note.
4. [`../workflows/voice.md`](../workflows/voice.md) — the sentence-level
   contract; default for notes, and this is dissertation-bound prose.

Expected homes: design rationale to `ch3_design/`; constraint-driven
choices to `ch4_implementation/`; metric selection to `ch5_evaluation/`;
abandonments and their lessons to `ch6_discussion/`, whose future-work material
rides the *Revisit conditions* of the notes that spawn them.

The transformation, and the reason the rubric's ban is not a mere formality:
**a note is a rough draft of an idea, written an abstraction away from the
session that produced it** (Marc, 2026-08-06). It is not a summary of what
happened. The session's execution detail — the file that was edited, the run
that failed, the tool that was built — is the *occasion* for the idea and almost
never belongs in the note; what belongs is the concept or theme that would
plausibly survive into a chapter, argued in research voice. A useful test on any
Stage 3 draft: if it reads as an account of work, it is annal material that has
escaped Stage 2. Rewrite it as the claim, or send it back.

The chapter map has no `ch1`/`ch7` subdirs by design, and Marc has scoped the
introduction and literature review out of this exercise, so nothing here should
be aimed at them.

### Alternatives considered

- **Feed whole transcripts to a summarising agent.** Rejected: it reproduces the
  exact failure Marc named. The assistant's output would be summarised alongside
  the intent, and the intent is the smaller signal, so it loses. The per-prompt
  unit is the control that keeps the human voice separable.
- **Chronological annal only.** Rejected above — duplicates `git log` and hides
  the multi-session reversals that are the point.
- **Notes only, no `implementation/` record.** Rejected: it either breaks the
  notes rubric or discards 90 % of the material, and probably both.
- **Mine everything, all 550 records.** Rejected as the default. The ≥150-word
  band carries the argument mass; the short prompts are steering. If Stage 1
  finds a thread whose turning point sits in a short prompt, pull that prompt's
  session in full — targeted, not wholesale.
- **Do it directly from memory of the sessions.** Rejected: that is the failure
  mode this exercise exists to fix. Three months is past the point where recall
  is evidence.

## Validation gate

The work is done when all of these hold:

1. ~~`tools/prompt_corpus.py` is committed and reproduces **73 prompts / 63 900
   words at ≥ 150 words** against the 2026-08-06 corpus specifically — a
   regression check on the filter set, run over a pinned date bound, not over
   whatever the corpus has since grown to.~~ **Met 2026-08-08, at a re-pinned
   figure: 73 prompts / 60 399 words**, over the same bound, as
   `python tools/prompt_corpus.py gate`. The word difference is the survey's two
   compaction summaries and is recorded in the tool, not tuned away.
2. ~~A raw snapshot of all 110 transcripts exists outside `~/.claude*`.~~ **Met
   2026-08-08** — all 112, checksummed, at `~/mtdsim-corpus-snapshot/2026-08-08/`.
3. The disposition table covers **every** prompt in the ≥ 150-word band as it
   stands on the day Stage 1 runs — one of the five dispositions each, and a
   named file for both `already-recorded` and `record-drifted`.
4. Every thread file states what was abandoned, not only what was decided — a
   thread with no negative space has not been mined, it has been summarised.
5. The `record-drifted` flags are collected in one list, each naming the record,
   the prompt's date, and the divergence — and **none of them has been actioned**.
6. The May–June blackout is stated in the annal as a one-line boundary with its
   explanation (introduction and literature-review work, out of scope here), and
   no stage has been spent reconstructing it.
7. `docs_map.md` registers the new subtree, in the creating commit.
8. Every new note follows `_template.md`'s section shape exactly, declares its
   chapter job in the terms `_writing_guide.md` sets out, passes the rubric's
   seven-test cross-examination, and reads as a claim rather than an account of
   work. Repo paths appear in the evidence footer and nowhere else. The count is
   small enough to be plausible — if Stage 3 produces twenty notes, the gate has
   failed, not passed.
9. No annal claim contradicts a shipped record without saying so explicitly and
   dating both.

## Hard constraints

- **Third-party content.** The corpus contains pasted supervisor emails, meeting
  agendas and at least one full meeting transcript — one prompt is 42 000
  characters of exactly this. The annal is **tracked in git**. Do not paste
  Dr Hong's words into a tracked file: paraphrase, attribute as dated supervisor
  direction, and keep the verbatim text in the untracked snapshot. The same
  applies to any third party appearing in the corpus.
- **The prompts are dated evidence, never current truth.** Every annal entry
  carries the date of the prompt it rests on. A reversed decision is recorded
  *as* reversed, with both dates. This is the retire-by-evidence rule applied to
  a primary source.
- **Shipped records are dated evidence too.** The rule above cuts both ways: a
  record states what was true when it was written, and three months is long
  enough for one to fall behind the thinking. Neither side wins automatically —
  chronology and evidence decide, and the outcome is a *flag*, never a silent
  edit.
- **The annal does not overrule shipped records.** Where a prompt and a shipped
  record disagree, record both, date both, and flag it — the same standing rule
  that governs papers against the code. Do not "correct" `architecture.md` from a
  prompt: a `record-drifted` flag is a candidate for Marc's disposition, exactly
  as a candidate bug is. A three-month-old prompt is a weak warrant on its own;
  what makes the flag worth raising is that Marc can see the divergence and rule
  on it in one line.
- **No new subtree without registration** in `docs_map.md`, same commit.
- **The four notes documents — writing guide, template, rubric, voice — apply in
  full to Stage 3**, and to nothing in Stage 2. The annal is `implementation/`
  register and may use internal vocabulary freely; a note may not. In particular
  the template's section shape is mandatory and the *Evidence and repo anchors*
  footer is the only place a repo path appears.
- **Never stage `~/.claude*` content into the repo** beyond the paraphrased
  annal. The snapshot is untracked. Transcripts contain absolute home paths and
  arbitrary tool output.
- Australian English throughout. Branch discipline per
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md): this
  brief was written on `docs/research-record-mining`, off `dev`.

## Reading list

- [`../notes/_writing_guide.md`](../notes/_writing_guide.md) and
  [`../notes/_template.md`](../notes/_template.md) — **binding for Stage 3**: the
  job each chapter does and how notes map onto it, and the mandatory section
  shape. Read the guide before drafting anything, not after.
- [`../workflows/notes_rubric.md`](../workflows/notes_rubric.md) — the seven-test
  cross-examination, and the explicit list of what a note is *not*. The gate for
  Stage 3 and the reason Stage 2 exists at all.
- [`../workflows/docs_map.md`](../workflows/docs_map.md) — the placement
  criterion, the subtree-registration contract, and the chapter map.
- [`../implementation/architecture.md`](../implementation/architecture.md) §(a) —
  the existing decisions log. Read it **before** Stage 1, so `already-recorded`
  can be applied on sight rather than rediscovered.
- [`README.md`](README.md) — the open chain and the disposition list it points
  at; the second-largest store of already-recorded rationale.
- `~/.claude-acc1/projects/-home-marc-GitHub-MTDSim/memory/voice_evidence_prompt_corpus_2026-07.md`
  — the precedent extraction's findings, and the format defect not to repeat.
- [`../workflows/voice.md`](../workflows/voice.md) — Stage 3 only, before drafting.

## Out of scope (explicitly)

- **The introduction and literature review chapters.** Marc has scoped this to
  design, implementation, evaluation and discussion/future-work. This is also
  why the May–June transcript blackout costs nothing: that window *was* the
  intro/lit-review work, so **reconstructing it is out of scope**, not deferred.
- **Voice evidence.** That mining was done on 2026-07-13 and its conclusions are
  in `voice.md`. If the new extraction happens to strengthen it, that is a
  separate brief — do not re-open the voice contract here.
- **Acting on anything found.** If the corpus reveals an unactioned decision, a
  contradiction with a shipped record, or a `record-drifted` divergence, it is
  **recorded and flagged**, not fixed — and this includes *documentation* fixes,
  which will feel harmless and are the likeliest scope breach in the whole brief.
  Rulings are Marc's, and a three-month-old prompt is the weakest possible
  warrant for changing today's code or today's records.
- **The other two projects** in the account stores (`304-game`, `CITS4505`).
- ~~**Closing `feat/stealth-exposure-reader`**, which is fully merged into `dev`
  (0 commits ahead) and by the session-start checklist should have been deleted
  when its work landed. Flagged, not actioned — its handoff is still open at
  position 1 of the chain, so the deletion wants Marc's eye rather than a
  passing session's.~~ **Discharged 2026-08-08:** the branch no longer exists, so
  the flag has been resolved by someone else acting on it. Nothing owed.
