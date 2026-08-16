---
status: durable
created: 2026-08-16
updated: 2026-08-16
---

# The drafting pipeline — how every unit of dissertation prose gets written

**Status:** durable. Ratified in practice on §4.2.1 (2026-08-16, the L0–L1
pilot) and adopted by Marc for **all** future dissertation drafting. Load this
before any session that touches dissertation prose, alongside
[`draft_scrutiny.md`](draft_scrutiny.md) (the content contract it inherits)
and [`voice.md`](voice.md) (the rationale: AI-flattened voice cost marks once;
this pipeline is the structural fix).

## The property that makes it safe

**No pass after draft 1 writes prose.** Draft 1 is spoken by Marc; everything
after is deletion, splitting, flagging, and one scrutiny command. The only
judgement calls a session makes arrive as named gaps with grounding documents
Marc wrote earlier — the system is Marc checking his draft against his own
record, with the session as the index. If a session is ever composing a new
sentence, it has left the rails (the sole exception: edits Marc explicitly
authorises, assembled from his own dictated words and marked for his
ratification).

## The five passes, per unit

| # | Pass | Who | What |
|---|---|---|---|
| 1 | **Speak** | Marc | Dictate the unit's argument long (~2–3× the word budget), from a noun-stub cue card (numbers/terms/anchors only — never copied clauses, which would smuggle document-voice into the run-through). Transcribe raw. |
| 2+3a | **Repair + register sweep** | session | The `repair-dictation` skill: STT repair (technical vocabulary hardest — mangle dictionary in the skill), disfluencies dropped, pads deleted, run-ons split at conjunctions, meta-narration beheaded, hedges flagged `[3b]` never resolved. Returns verify watchlist + change log. |
| 3b | **Marker walk** | Marc | Each `[3b]` marker is one binary or one word choice; plus the globals (contractions, second person, I/we) and the read-aloud check — sounds like Marc being careful, not a journal. |
| 4 | **Content scrutiny** | session | The `scrutinise-draft` skill against the chapter's pack row (`draft_scrutiny.md` §c): ≤3 prioritised moves, each grounded. Runs after 3b, before compression; re-run cheaply if compression cuts more than half. Inline `[comment]` format on request. |
| 5 | **Compress** | Marc | Per sentence, one binary: "does the unit still answer its question without this?" Cut order: duplicates → re-explanations → second examples → qualifiers a citation/appendix already carries. Never cut: must-carry disclosure sentences, numbers, citations. Sentence fusion only once whole-sentence cuts stall. |

Iteration inside a pass is normal (a unit may loop dictation→scrutiny several
times before converting); the pass boundaries and their owners do not move.

## Sequencing across units

**Pilot one unit through all five passes first** (calibrates what a
unit-sized argument feels like, so later dictations start tighter), **then
batch passes 1–2 across the remaining units while warm** (speaking is the
scarce, high-energy mode; converting can be done tired, any day), **then
convert in a run.** Units that interlock (shared disclosures, forward
pointers) should be spoken close together, while moving an argument between
them is still cheap.

## The gates

- A unit is done when its must-carry disclosures are present **as sentences**
  (the skeleton comment above the unit is the authority), the scrutiny pass
  has returned and been ruled on, and the word count is at budget — or the
  overdraft is claimed **explicitly** on the writing-guide ledger, naming what
  funds it. Subsubsection headings are unit claims; paragraphs are free.
- Cuts that remove a disclosure or a coined term other units point at are
  flagged by the session and ruled by Marc — rulings are recorded in the
  active drafting handoff (and the skeleton comments) so no future pass
  re-flags them.
- Drafting state lives **in the `.tex`** as `% DRAFT STATE` comments above the
  unit; cross-session obligations (owed appendix entries, homeless
  disclosures, flags for later units) live in the active drafting handoff.

## Where the pieces live

- Passes 2+3a: [`../../.claude/skills/repair-dictation/SKILL.md`](../../.claude/skills/repair-dictation/SKILL.md)
  (carries the living mangle dictionary, minimal-pair list, and pad inventory
  — append new observations there, not in chat).
- Pass 4: [`../../.claude/skills/scrutinise-draft/SKILL.md`](../../.claude/skills/scrutinise-draft/SKILL.md)
  + [`draft_scrutiny.md`](draft_scrutiny.md) (question set + corpus map).
- Voice and prose-quality layers: [`voice.md`](voice.md),
  [`critique_protocol.md`](critique_protocol.md) — below this pipeline, loaded
  when the task reaches sentences.
- Unit budgets and the ledger: the skeleton comments in
  [`../thesis/dissertation.tex`](../thesis/dissertation.tex) and
  [`../notes/_writing_guide.md`](../notes/_writing_guide.md).
