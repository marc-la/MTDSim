---
status: open
created: 2026-08-06
---

# Mine the session transcripts for Marc's own prompts, and land them as a research record — the intent, the reversals, and the abandoned paths that no shipped document holds

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

**1. May and June are missing entirely.** `dev` carries **92 commits** across
those two months (84 in May, 8 in June); there are **zero** transcript records
with a May or June timestamp in any of the three account stores. The
account-level `history.jsonl` files are ring buffers of ~20 records and hold only
April, so they are not a recovery path. This was checked directly and is not an
artefact of how the files were selected.

Do not paper over this. The annal must carry the blackout as a stated boundary,
because May is not a quiet month in this project's history — it is where a large
share of the substrate correction work landed. Two partial reconstructions are
available and should be used rather than a shrug: `git log dev` for that window,
and the supervisor updates *quoted inside* later prompts, which reference dates
in May and June and summarise what had been done by then.

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

## Recommended approach

Four stages. Stage 0 is cheap and should be done immediately, for a reason given
below. Stages 1–3 are one session each at minimum; Stage 1 is likely two.

### Stage 0 — snapshot the corpus, then build the extractor (do this first)

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

Then attach one of four dispositions, and attach one to **every** prompt — a
prompt dropped silently is indistinguishable from a prompt never read, and the
completeness of this table is what makes the annal trustworthy:

- `already-recorded` → cite the file and section; no annal prose.
- `annal-entry` → unrecorded rationale; goes to Stage 2.
- `note-candidate` → carries a dissertation argument; goes to Stage 3.
- `noise` → band 7.

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

Only band 2–5 material, only where it is an argument. Run the rubric's
cross-examination before committing each note, and load
[`../workflows/voice.md`](../workflows/voice.md) first — this is dissertation-bound
prose. Expected homes: design rationale to `ch3_design/`; constraint-driven
choices to `ch4_implementation/`; metric selection to `ch5_evaluation/`;
abandonments and their lessons to `ch6_discussion/`, whose future-work material
rides the *Revisit conditions* of the notes that spawn them.

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

1. `tools/prompt_corpus.py` is committed and reproduces **73 prompts / 63 900
   words at ≥ 150 words** on the 2026-08-06 corpus.
2. A raw snapshot of all 110 transcripts exists outside `~/.claude*`.
3. The disposition table covers **73 of 73** prompts, each with one of the four
   dispositions and, for `already-recorded`, a named file.
4. Every thread file states what was abandoned, not only what was decided — a
   thread with no negative space has not been mined, it has been summarised.
5. The May–June blackout is stated in the annal, with `git log dev` for that
   window and the quoted supervisor updates used as the partial reconstruction.
6. `docs_map.md` registers the new subtree, in the creating commit.
7. Every new note passes the rubric's seven-test cross-examination, and the count
   is small enough to be plausible — if Stage 3 produces twenty notes, the gate
   has failed, not succeeded.
8. No annal claim contradicts a shipped record without saying so explicitly and
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
- **The annal does not overrule shipped records.** Where a prompt and a shipped
  record disagree, record both and flag it — the same standing rule that governs
  papers against the code. Do not "correct" `architecture.md` from a prompt.
- **No new subtree without registration** in `docs_map.md`, same commit.
- **Notes rubric and voice contract** apply in full to Stage 3, and to nothing in
  Stage 2 — the annal is `implementation/` register and may use internal
  vocabulary freely.
- **Never stage `~/.claude*` content into the repo** beyond the paraphrased
  annal. The snapshot is untracked. Transcripts contain absolute home paths and
  arbitrary tool output.
- Australian English throughout. Branch discipline per
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md): this
  brief was written on `docs/research-record-mining`, off `dev`.

## Reading list

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
  design, implementation, evaluation and discussion/future-work.
- **Voice evidence.** That mining was done on 2026-07-13 and its conclusions are
  in `voice.md`. If the new extraction happens to strengthen it, that is a
  separate brief — do not re-open the voice contract here.
- **Acting on anything found.** If the corpus reveals an unactioned decision or a
  contradiction with a shipped record, it is **recorded and flagged**, not
  fixed. Rulings are Marc's, and a three-month-old prompt is the weakest possible
  warrant for changing today's code.
- **The other two projects** in the account stores (`304-game`, `CITS4505`).
- **Closing `feat/stealth-exposure-reader`**, which is fully merged into `dev`
  (0 commits ahead) and by the session-start checklist should have been deleted
  when its work landed. Flagged, not actioned — its handoff is still open at
  position 1 of the chain, so the deletion wants Marc's eye rather than a
  passing session's.
