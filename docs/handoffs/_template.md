---
status: open                  # open | partially shipped | superseded by <link>
created: YYYY-MM-DD
---

# <One-line goal — the thing the next session ships>

## State of play

What's already true. What's not. The minimum a cold-start session needs to orient before doing anything.

## Recommended approach

The path you'd take if you were the next session. Name the alternatives you considered and why this one wins — the next session has a brain and might disagree, but they should disagree from your shortlist, not from scratch.

## Validation gate

How the next session knows the work is done. A passing test, a green CI step, a visible behaviour, a number in the goldens — be concrete. "Looks good" is not a gate.

## Hard constraints

Things that *must* hold and might not be obvious from the code:
- determinism / SIM-05
- spec rows that pin behaviour
- inherited divergences not to "fix"
- branch / commit / push rules from [`../specs/session_workflow.md`](../specs/session_workflow.md)

## Reading list

The 3–5 files the next session must skim before touching anything:
- `path/to/file.py` — why
- `docs/specs/<spec>.md` — what row to read

## Out of scope (explicitly)

What this handoff is *not* asking for. Use this to pre-empt scope creep.
