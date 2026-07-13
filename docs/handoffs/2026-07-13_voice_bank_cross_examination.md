---
status: open
created: 2026-07-13
---

# Cross-examine voice.md against Marc's authored academic prose recovered from his chat history

## State of play

[`../workflows/voice.md`](../workflows/voice.md) is live (created 2026-07-13): argumentation rules (§c) grounded in the ratified prose corpus **and** Marc's typed prompt history; sentence rules (§d) grounded in ratified prose only. The known epistemic weakness, stated in this session and accepted by Marc: ratification is weaker evidence than authorship, so §d may partly encode assistant house style Marc tolerates rather than his own prose instincts. The missing evidence class is **Marc-authored formal academic prose** — likely recoverable from his claude.ai / ChatGPT history from the lit-review semester (S1 2026, CITS4010), when his then-active AI-principles constraint meant he drafted prose himself and asked for critique rather than generation.

Marc has been given a self-contained retrieval prompt (§ "The Desktop prompt" below) to run in Claude Desktop (and optionally adapted in ChatGPT). Its output is a markdown evidence report: authored passages verbatim with provenance confidence, plus a rule-by-rule cross-examination verdict table against voice.md §c/§d/§h.

The prompt-corpus analysis that grounded the current §c rules is persisted (with the extracted corpus) in the assistant memory directory (`~/.claude-acc1/projects/-home-marc-GitHub-MTDSim/memory/voice_evidence_prompt_corpus_2026-07.md`) — untracked by design; Marc's raw prompt verbatims stay out of the repo.

## Recommended approach

When Marc supplies the evidence report (pasted or as a file):

1. Load [`../workflows/voice.md`](../workflows/voice.md) in full, plus the persisted prompt-corpus analysis for cross-reference.
2. **Audit the report's authorship forensics before believing it.** Only passages classified Marc-authored at medium-or-better confidence are admissible for §d; AI-drafted-Marc-ratified passages are corroboration only (they duplicate the existing evidence class). If the report's provenance reasoning is thin, discount rather than ingest.
3. Apply verdicts per §g's evidence layering:
   - **CONFIRMED** rules: annotate nothing; optionally note corroboration in the commit message.
   - **CONTRADICTED** rules: amend or remove — authored evidence outranks ratified evidence at the sentence level; only assessor/supervisor feedback outranks authored evidence.
   - **NO EVIDENCE** rules: leave standing but do not strengthen.
   - New trait candidates: admit only with ≥3 independent occurrences across ≥2 conversations, schematised first-principles (no thesis-content bindings — Marc's standing ruling).
4. Bump `updated` in voice.md frontmatter; commit; delete this handoff in the same commit.

Alternative considered: having the Desktop session output a voice.md diff directly. Rejected — Desktop lacks the repo, the §g evidence rules, and the first-principles constraint; a repo session must stay the gatekeeper.

## Validation gate

- Every §c/§d/§h rule has received an explicit verdict (confirmed / contradicted / no-evidence) recorded in the session, and every voice.md change traces to a quoted authored passage or an explicit Marc ruling in the report.
- voice.md remains first-principles: zero bindings to thesis content, framings, or named files.
- This handoff deleted in the shipping commit.

## Hard constraints

- **Genre firewall holds:** conversational fillers/typos in recovered material are not prose evidence even when Marc-authored — only his *academic-register* attempts count for §d.
- Marc's raw chat verbatims are not committed to the repo; quote minimally in commit messages.
- Branch/commit rules per [`../workflows/session_workflow.md`](../workflows/session_workflow.md); Australian English.

## Reading list

- [`../workflows/voice.md`](../workflows/voice.md) — the contract under examination.
- `~/.claude-acc1/projects/-home-marc-GitHub-MTDSim/memory/voice_evidence_prompt_corpus_2026-07.md` — the existing evidence base and its caveats.
- [`../workflows/notes_rubric.md`](../workflows/notes_rubric.md) — register boundaries voice.md defers to.

## Out of scope (explicitly)

- Re-mining Claude Code transcripts (done 2026-07-13; diminishing returns until a new project phase).
- Drafting any dissertation prose.
- Encoding Tim French's *annotated* lit-review report — separate evidence event when Marc obtains it; it outranks everything here and warrants its own pass.

## The Desktop prompt

The verbatim prompt Marc runs in Claude Desktop (adapt the first line for ChatGPT). Kept here so the retrieval is reproducible:

```text
I want you to search my past conversations exhaustively and recover every fragment of formal academic writing that I authored myself, then cross-examine a set of writing rules against that evidence. This is forensic work: the distinction between what I wrote and what an AI wrote is the entire point.

CONTEXT
I am a UWA honours student (computer science, Moving Target Defence research). I maintain a "voice file" that governs AI-assisted writing for my dissertation. Its argumentation rules are grounded in my prompt history; its sentence-level rules are grounded only in AI-drafted prose I approved — which risks encoding an AI house style I merely tolerate. The missing evidence is academic prose I wrote MYSELF. During semester 1 2026 I wrote a literature review (unit CITS4010) under a self-imposed rule that discouraged asking AI to edit or improve my work — so my history from roughly February–June 2026 likely contains drafts I typed or pasted for critique, not generation. That is the gold. My research area vocabulary: Moving Target Defence, MTD, MTDSim, MITRE ATT&CK, attack graphs, APT, honours, thesis, literature review.

STEP 1 — RETRIEVE (be exhaustive, iterate until dry)
Search my conversation history with many angles, not one: "literature review", "lit review", "my draft", "I wrote", "critique my", "feedback on my paragraph", "does this read", "reword", "my writing", "CITS4010", "supervisor", "thesis", "dissertation", "abstract", "introduction", plus my research vocabulary above. Follow every hit into its conversation and read enough context to judge authorship. Keep searching with new terms suggested by what you find until two consecutive searches surface nothing new.

STEP 2 — AUTHORSHIP FORENSICS (the critical step)
Classify every candidate passage:
  A. MARC-AUTHORED: I typed or pasted it as my own writing. Markers: I introduce it ("here is my draft", "I wrote this", "critique this"); it carries my typo fingerprint (dropped apostrophes, lowercase openers, comma splices, transcription typos); it predates any AI draft of the same content in the thread.
  B. MARC-EDITED AI: an AI draft I visibly reworked — only my changed words are evidence.
  C. AI-DRAFTED, MARC-APPROVED: not new evidence; note it exists, do not analyse.
  D. UNCERTAIN: cannot establish provenance — mark it and set aside.
Only class A (and the deltas in B) count. When in doubt, downgrade to D. State your confidence (high/medium/low) per passage and WHY.

STEP 3 — EXTRACT
For every class-A passage: quote it VERBATIM (typos included), with conversation title, approximate date, and surrounding context (what I asked for). Do not clean it up. Do not paraphrase.

STEP 4 — CROSS-EXAMINE THESE RULES
Test each rule below against the class-A evidence only. Verdict per rule: CONFIRMED (≥2 authored passages exhibit it), CONTRADICTED (authored passages consistently do otherwise — quote them), or NO EVIDENCE. Do not be agreeable: a contradiction is a more valuable finding than a confirmation.

Argumentation rules: (1) paragraphs open with their claim; (2) enumerations are announced then walked in order; (3) alternatives are ranked on an explicit axis and the choice justified from both directions; (4) claims carry their mechanism and every inferential step is walked; (5) limitations are conceded up front, sometimes as "the strength and the limitation are the same fact"; (6) what the argument does NOT claim is stated explicitly; (7) claims stop at what evidence carries (designed ≠ demonstrated ≠ true); (8) abstract claims are grounded with examples, numbers, or figures; (9) success criteria are stated before the thing judged against them; (10) circularity/overfitting risks are named and defused.

Sentence rules: paired opposition (antithesis across a semicolon; "X, not Y" compressions); em-dash interpolations that add an argumentative turn; long build sentences landing on short verdict sentences; present tense, active voice, cited authors as sentence subjects; at most one vivid plain-English compression per section; headings that state the topic and nothing more; evaluation vocabulary "grounded / defensible / tradeoff / distil"; sparse semantic emphasis; Australian English.

Banned-tell rules (check whether I EVER do these in authored prose): hype adjectives on own work (novel, comprehensive, significant, robust); "it is important to note"; Moreover/Furthermore/Additionally chains; three-adjective triads; bold-term listicles; stacked hedges; empty signposting ("in this section we will discuss"); rhetorical questions as transitions; identical paragraph openers.

STEP 5 — REPORT (single markdown artifact I can download)
Structure: 1. Retrieval log (searches run, conversations examined, dead ends). 2. Class-A passages, verbatim, with provenance and confidence. 3. Rule-by-rule verdict table with quoted evidence. 4. New trait candidates: recurring habits in my authored prose that the rules above do NOT capture (≥3 occurrences across ≥2 conversations, quoted). 5. Honest sample-size caveat: how much authored prose you actually found and what layers it can and cannot evidence.
End the artifact with a section titled "FOR THE REPO SESSION" containing one paragraph: instructions to cross-examine docs/workflows/voice.md against this report under its §(g) evidence rules, amending contradicted rules and admitting new traits only at ≥3 occurrences, schematised without thesis-content bindings.

Do not flatter me. Where my authored prose is weak, say so — weaknesses are evidence about what the rules should guard against, not things to soften.
```
