# Guardrails

**Status:** durable, always-on. These rules hold across every session. Task-specific scope from a session prompt (e.g. "audit only, don't change code") refines but never relaxes them.

## Always-on

- **Git:** work on a dedicated branch; never commit to `main`; commit locally for my review; **never push** without asking; never run destructive git (`reset --hard`, `clean -fd`, `gc --prune`, force-push). Keep the session's terminal parked on its own branch for the session's duration. The per-turn stage-commit-push flow is in [`session_workflow.md`](session_workflow.md).
- **Scope:** stay inside the task's defined scope. *Flag* out-of-scope findings — don't action them. Prefer small, reviewable, line-level diffs over wholesale rewrites; ask before expanding scope or restructuring.
- **`feat/replay-viz`:** do not merge it wholesale. Pull only substrate-relevant fixes, as individually reviewed cherry-picks. Take only the substrate slice of any pick that drags unrelated hunks. Visualisation and GAP/GASP commits are deferred (Stream A/B).

## Working standards

- **Papers are claims to reconcile with the code, not ground truth about it.** When a paper and the code disagree, record both; correct neither without a disposition from me.
- Distinguish an **inherited divergence** (the code's reality, to parameterise or document) from a **bug** (unintended; violates an invariant, or — as with C6 — entered via an unexplained "debug" commit with no paper basis). Fix bugs; don't preserve them as "inherited reality".
- **Never guess** a disposition or a locator. If you can't verify it, mark `unverified` / `verify` and state why.
- Don't assert that a paper is wrong (or that one paper contradicts another) — flag it "to verify" for me to resolve.
- When working across multiple papers, extract **one paper per pass** before merging, to prevent cross-attribution.
- Keep **inherited artefacts** distinct from **my own editorial/design choices**; track them separately.

## Australian English

Throughout, in docs and code comments.
