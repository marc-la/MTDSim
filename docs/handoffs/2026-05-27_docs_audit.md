---
status: open
created: 2026-05-27
---

# Audit `docs/`, `.claude/`, and `CLAUDE.md` for critical-evaluation gaps

Produce a **findings document** that critiques the existing doc system, not a
description of it. Marc's framing: *lots of writing, not lots of evaluating* —
the docs have accumulated faster than they've been pressure-tested. This handoff
hires a session to do the pressure-testing.

## State of play

- **Specs** (`docs/specs/`, 7 + the new `architecture.md`): `guardrails.md`
  (22 L), `session_workflow.md` (83), `project_context.md` (31),
  `repo_conventions.md` (34), `mtdsim_spec.md` (241), `metrics_semantics.md`
  (222), `provenance.md` (67), `architecture.md` (484, Pass 1 scaffold landed
  today as `76ca7f6`).
- **Open handoffs** (`docs/handoffs/`): this one;
  [`2026-05-27_architecture_prepopulation.md`](2026-05-27_architecture_prepopulation.md)
  (status `partially shipped`, Pass 2 outstanding);
  [`2026-05-27_bibliographic_anchors.md`](2026-05-27_bibliographic_anchors.md)
  (status `open`).
- **Notes** (`docs/notes/`): empty (template only). Per
  [`session_workflow.md`](../specs/session_workflow.md#L49) notes are
  dissertation-worthy observations; nothing has been promoted there yet.
- **Extractions** (`docs/extractions/`, 22 papers + template): the four lineage
  papers (Brown / Zhang / Ho / Tay) are fleshed-out (136–213 L); the 18 adjacent
  papers are stubs (≈40 L each), created today by the concurrent
  `feat/lit-review-landing` session.
- **Sources** (`docs/sources/`): gitignored corpus + `LIT_REVIEW.md`, not in
  scope for audit content — only whether the extractions and architecture
  reference it sanely.
- **`.claude/`**: contains only `settings.local.json` (165 bytes — five `allow`
  Bash entries: `conda list`, `sudo apt-get`, `python3 -c`, `pip install`).
  No hooks, no agent definitions, no slash commands, no shared `settings.json`.
- **`CLAUDE.md`**: 32 lines. Updated today to mention `architecture.md` in the
  spec list and flip the architecture handoff to `partially shipped`.

The substrate-side specs (`mtdsim_spec.md`, `metrics_semantics.md`,
`provenance.md`) plus the lineage extractions came out of a focused Phase 2c
re-baseline — they have been pressure-tested. The methodology-side material
(`architecture.md`, `project_context.md`'s direction-and-scope section, adjacent
extractions, and the lit-review-stage handoffs) is newer, was written under
deadline pressure for the lit-review landing, and **has not been read against
itself yet**. That is the audit's primary target.

## Recommended approach

A single audit session. Output is one findings file —
**`docs/notes/2026-05-27_docs_audit.md`** (notes subtree because the findings
should survive as dissertation source about the doc system; not a handoff,
because nothing's been shipped yet). Structure the findings per the dimensions
below, with concrete line-references and severity tags.

### Audit dimensions

1. **Structural integrity** — does every file sit in the subtree whose
   lifecycle matches its content? (Per
   [`repo_conventions.md`](../specs/repo_conventions.md#L9): specs durable, handoffs
   live and deleted-when-shipped, notes durable dissertation-source, extractions
   durable per-paper.) Anything in the wrong subtree is a finding.

2. **Cross-doc consistency** — pairwise read of the 8 specs against each other.
   Concrete checks:
   - Does `architecture.md` §(i) substrate seam match
     [`project_context.md`](../specs/project_context.md#L17) verbatim on the
     attacker-module seam?
   - Does `architecture.md` §(k) validation strategy match
     [`metrics_semantics.md`](../specs/metrics_semantics.md) §d on the
     comparability boundary?
   - Does `project_context.md` L10 (Tay deferred, no retrain) match
     `repo_conventions.md` L34 (same content, second source)? Is the duplication
     load-bearing or drift-risk?
   - Do the two open handoffs reference each other's scope correctly?

3. **Coverage gaps** — what's load-bearing in the project but undocumented in
   any spec? Candidates to test: the Attack Flow `.afb` parser entrypoint (named
   only in `architecture.md` §(c) as an open question); the actual MTD-family
   taxonomy (SDR named in `project_context.md`/`architecture.md`, never defined
   beyond the acronym); the network topology default (called "generic" but
   never pinned).

4. **Drift / staleness** — anything referencing decommissioned threads
   (`feat/replay-viz`, the visualiser, IDS-as-RQ, the 4-section lit-review
   structure)?
   [`guardrails.md`](../specs/guardrails.md#L9) still mentions `feat/replay-viz`
   as an active cherry-pick source — is that still true?

5. **Critical-evaluation quality** — Marc's primary concern. For each spec
   section that makes a *claim*, is the claim *justified*? Specific patterns
   to look for:
   - **Design presented as fact** — e.g. `architecture.md` L2 currently uses
     a terminal-node-ancestor proxy; is the proxy → motivation conflation
     surfaced sharply enough?
   - **Decisions without `If revisited:`** — `architecture.md` enforces this
     contract; do the older specs (`project_context.md`, `metrics_semantics.md`)
     have decisions baked in without revisit-criteria?
   - **Claims that depend on the lit review but cite nothing** — the
     "behaviourally grounded" framing, the "Pyramid of Pain" argument, the
     "dominant evaluation pattern" claim — each appears in
     `architecture.md` §(a)/§(j); none cite an extraction yet. Pass 2 will
     fix this, but the audit should record the unsupported-claim count.
   - **Architectural decisions without consequence statements** — e.g. "no
     novel RL training" — what does that *cost* in evaluation power?
     Currently stated as scope, not as a tradeoff.

6. **Entry-point quality** — `CLAUDE.md`. Read it cold (imagine no
   conversation context). Can a fresh session orient from the read-order alone?
   Test specifically:
   - Does the read-first list (guardrails → workflow → context → conventions)
     get a cold session to "knows enough to not break anything" in <10 min?
   - Is the "spec files (load when relevant)" tier obviously distinct from
     read-first?
   - Is `architecture.md`'s position in the tier correct?
   - Are the session-start checks actually performable from
     `CLAUDE.md` alone, or do they require reading `session_workflow.md` first?

7. **`.claude/` alignment** — given the workflow described in `session_workflow.md`
   (stage-commit-no-push, never-touch-main, never-skip-hooks), is anything that
   *should* be enforced via `.claude/settings.json` or `.claude/hooks/`
   missing? Specific candidates:
   - A pre-commit / pre-push hook against `main`.
   - A permissions allowlist for the docs-touching tools (Read, Edit, Write on
     `docs/**`) given the high volume of doc work, to reduce prompt friction.
   - The current `allow` list is package-management commands only — does the
     working session's actual tool usage justify expanding it?
   - Is the absence of `.claude/settings.json` (shared, version-controlled) a
     deliberate choice or an oversight?

8. **Handoff hygiene** — three open handoffs as of today (this one + two
   others). Per [`session_workflow.md`](../specs/session_workflow.md#L70)
   stale-handoff-sweep, anything that should be marked superseded or deleted?
   Are the validation gates concrete enough that "done" is unambiguous?

### Output format

`docs/notes/2026-05-27_docs_audit.md`. One section per audit dimension above.
For every finding within a section:

```
- **[severity]** <file>:<line> — <one-sentence finding> Recommendation: <one
  sentence>
```

Severities: `must-fix` (correctness; the doc misleads), `should-fix` (gap; a
cold session would stumble), `nice-to-have` (polish; the doc is correct but
could be sharper). End each section with a count by severity.

End the document with an overall scoreboard: total findings per dimension,
total per severity, and a one-paragraph "headline" describing the doc system's
current health.

### Alternatives considered

- **Edit-in-place fixes during the audit.** Rejected: conflates audit output
  with action. The findings doc is the deliverable; Marc decides which to
  action and when. Some fixes are also coupling decisions (e.g. *where* the
  MTD-family taxonomy lives) that need Marc's call.
- **Per-spec-file audit handoffs.** Rejected: too granular; the value of this
  audit is cross-doc consistency, which a per-file decomposition would lose.
- **Skip `.claude/` audit, do docs only.** Rejected: `.claude/` is part of the
  workflow scaffolding Marc explicitly named; auditing docs without it would
  miss the hooks-vs-prose tension (rules in docs that aren't enforced).

## Validation gate

Done when:

1. `docs/notes/2026-05-27_docs_audit.md` exists, follows the format above,
   covers all 8 audit dimensions.
2. Every finding has a concrete file:line reference (no "the docs are
   inconsistent" — *which* line of *which* file).
3. Every finding has a severity *and* a one-line recommendation.
4. The scoreboard at the bottom totals correctly.
5. `CLAUDE.md`'s open-handoffs section is updated: this handoff marked
   shipped (delete it) and the findings file linked under "Open handoffs" or
   "Spec files" as appropriate to drive follow-up.
6. **No spec, handoff, or extraction is edited.** The audit produces
   findings, not fixes — fix-cycles are separate sessions.

## Hard constraints

- **Read-only on the doc system.** Findings file is the only write. Don't
  edit specs, handoffs, extractions, or `CLAUDE.md` (except the open-handoff
  pointer at gate completion).
- **Don't touch `docs/sources/`** — gitignored, copyright. Reference filenames
  only.
- **Don't touch the four locked specs**' substantive content
  (`mtdsim_spec.md`, `metrics_semantics.md`, `provenance.md`, lineage
  extractions). They may *appear* as findings (e.g. "their decisions lack
  `If revisited:` lines"), but the audit doesn't edit them.
- **Don't touch code.** The audit is about the doc system.
- **Branch + commit + don't push**, per
  [`session_workflow.md`](../specs/session_workflow.md#L7). Likely branch:
  `chore/docs-audit`.
- **Substance over form.** Marc explicitly wants critique, not copy-editing.
  "Section X could be clearer" is not a finding; "section X's claim Y is
  not supported by Z, and the lit-review section that would support it
  cites nothing" is.
- **No new specs.** If the audit identifies a missing spec, that's a finding
  (severity *should-fix* or *must-fix*) with a recommendation — not a
  prompt to write the spec.
- **Don't merge or push any branch.**

## Reading list

Skim cold before doing anything (in this order):

- [`../../CLAUDE.md`](../../CLAUDE.md) — entry point under audit
- [`../specs/repo_conventions.md`](../specs/repo_conventions.md) — the contract the audit checks against
- [`../specs/session_workflow.md`](../specs/session_workflow.md) — workflow rules; check `.claude/` against these
- [`../specs/guardrails.md`](../specs/guardrails.md) — the rules to obey *during* the audit
- [`../specs/project_context.md`](../specs/project_context.md) — what the project actually is
- [`../specs/architecture.md`](../specs/architecture.md) — newest spec, biggest cross-doc surface
- [`../specs/mtdsim_spec.md`](../specs/mtdsim_spec.md), [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md), [`../specs/provenance.md`](../specs/provenance.md) — locked substrate specs
- [`2026-05-27_architecture_prepopulation.md`](2026-05-27_architecture_prepopulation.md), [`2026-05-27_bibliographic_anchors.md`](2026-05-27_bibliographic_anchors.md) — the other open handoffs
- One representative adjacent extraction (e.g. [`../extractions/jalowski2026.md`](../extractions/jalowski2026.md)) — to read stub quality without auditing every one

## Out of scope (explicitly)

- Fixing anything the audit finds. The follow-up sessions do that.
- Re-deriving any architecture from substrate code.
- Auditing `docs/sources/` content (it's gitignored).
- Extending or critiquing the four lineage extractions' *content* (locked
  substrate). Their consistency *with the new specs* is in scope; their
  internal accuracy is not.
- Writing new specs.
- Reviewing the lit review's prose — `LIT_REVIEW.md` is gitignored; this
  audit checks the doc system, not the dissertation draft.
- Touching code or running the substrate.
- Auditing extraction stubs' *content* — only their *existence and structure*
  against the template. (Their content is Pass 2 of the architecture handoff,
  one paper per pass per [`../specs/guardrails.md`](../specs/guardrails.md#L17).)
