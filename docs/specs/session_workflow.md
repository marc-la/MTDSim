# Session workflow

**Status:** standing instruction. Applies to every assistant session that touches this repo.

## Branch hygiene (non-negotiable)

- Work on a **dedicated branch** for the session's scope (e.g. `chore/<topic>`, `feat/<topic>`, `fix/<topic>`).
- **Never commit to `main`.**
- **Never push** to any remote without an explicit ask from Marc. Local commits exist for review; pushes are a conversation.
- **Never run destructive git** (`reset --hard`, `clean -fd`, `gc --prune`, `--force` / `--force-with-lease`) without an explicit ask. History rewriting is a conversation, not an action.

If a session starts on `main`, the first action is to create or switch to a session branch.

**Mechanical guard.** A `pre-commit` hook at `.git/hooks/pre-commit` refuses commits on `main`. The hook is not version-controlled (`.git/` is per-clone); install once per fresh clone by writing this body and `chmod +x`-ing it:

```sh
#!/bin/sh
if [ "$(git branch --show-current)" = "main" ]; then
  echo "refuse: commit on main — create a session branch first" >&2
  exit 1
fi
```

## Stage-commit flow (per session)

The convention is **stage-commit per logical unit, push never** (until Marc asks). Run these at meaningful checkpoints — typically once per session, but more often when a session covers multiple discrete changes:

1. **Snapshot state.** `git status --short` to see what's dirty. `git diff` to recall the change.
2. **Stage deliberately, by file.** `git add path/to/file.py path/to/file.md`. Do **not** use `git add -A` or `git add .` — the repo contains files that change for non-session reasons (see "What never gets auto-staged" below).
3. **Write the message.** One line, present tense, focused on the *why*. Match the existing log's tone (`git log -10 --oneline`).
4. **Commit.** Include `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>`.
5. **Stop.** Do not push. Marc reviews the local branch, then pushes (or asks you to) when satisfied.

There is no auto-commit hook. The convention does the work; the hook would just be a foot-gun against the never-push-main rule.

## Handoff workflow

When the current session uncovers work worth doing but that won't fit (a follow-up analysis, a deferred refactor, an audit), spin out a **handoff** rather than carrying it implicitly.

**Where:** [`../handoffs/`](../handoffs/) — naming `YYYY-MM-DD_<topic>.md` (today's date as ISO).

**Lifecycle:**
- **Created** during a session, by you or by Marc's ask.
- **Updated** during the session that picks it up, to reflect what's been done.
- **Deleted** when the work lands — ideally **in the same commit that ships the work**, so the handoffs directory never lags reality. If a separate cleanup commit is unavoidable, take it before any other doc work begins. Git log is the permanent record of "what got shipped" — there is no archive folder.

Cold sessions discover open work via `ls docs/handoffs/` at session start (see § session-start checklist). The directory listing is the source of truth; there is no separate index in `CLAUDE.md` to keep in sync.

**Contents** (use [`../handoffs/_template.md`](../handoffs/_template.md) as the scaffold):
- One-line goal at the top.
- State-of-play (what's already true, what's not).
- Recommended approach + alternatives considered.
- Validation gate (how the next session knows it's done).
- Hard constraints (determinism, the spec, no new deps, etc.).
- Reading list — the 3–5 files the next session must skim.

The next session should be able to start cold from the handoff alone.

## Notes workflow

When the current session surfaces something dissertation-worthy — a mechanism worth describing, a methodological tradeoff worth defending, an observation worth citing later — write it down as a **note**.

**Where:** [`../notes/`](../notes/) — naming `YYYY-MM-DD_<topic>.md`.

**Lifecycle:**
- **Created** in-session when the user asks, or when an observation is clearly thesis material.
- **Updated** when the underlying truth changes and the note would mislead.
- **Kept indefinitely** — these are dissertation source material.

**Contents** (use [`../notes/_template.md`](../notes/_template.md)): plain English aimed at Marc's later self writing the dissertation. Cross-link to specs liberally. Avoid jargon that doesn't already exist in `mtdsim_spec.md`.

## Session-start checklist

At the start of any session that will touch tracked files:

1. `git branch --show-current` — confirm not on `main`.
2. `git status --short` — confirm clean tree (or note what's dirty and why).
3. Skim [`../handoffs/`](../handoffs/) for an open handoff matching today's task. If one exists and the session is to pick it up, read it cold.
4. If the session was triggered by handoff content, treat the handoff as the prompt — don't re-derive from conversation.

## Stale-handoff sweep

At session start, if a handoff exists for completed work, delete it. If it's been superseded, mark `status: superseded by <new-handoff>` in the frontmatter and delete on the next sweep. Don't leave dead handoffs accumulating — the directory should be an accurate inventory of *open* work.

## What never gets staged

- `.env`, `*.key`, `credentials*.json`, anything token-shaped — refuse and warn even if Marc asks.
- Files Marc is concurrently editing (check `git status` at session start; if a file you didn't change shows as modified, leave it alone).
- Generated experiment outputs (`experiments/`, `snapshots/`, `experimental_data/` — already `.gitignore`d but listed for clarity).
- `docs/sources/` — gitignored copyrighted material.

## What never gets committed at all

- Bypassing `--no-verify`. If a pre-commit hook fails, fix the underlying issue and make a new commit. Do not amend after a failed hook (the commit didn't happen; amend would mutate the previous one).
- Force-push to `main`. Not with `--force`, not with `--force-with-lease`, not with `+main`.
