---
status: complete-pending-merge
created: 2026-08-11
---

# Retire: the disengagement frontier is not axis 7's instrument (session complete, branch has a merge dependency)

## What this is

A **completed** session, recorded here only because its branch cannot merge to
`dev` independently and an open branch without a handoff reads as work in flight.
Nothing to do except merge it at the right time (below).

## What the session settled

Swept the disengagement frontier (the workshopped disengage metric) as a candidate
**instrument for validating axis 7 (learning)** against the compound-exploit-learning
mechanism. All four pre-registered conclusions fail; the λ = 0 negative control
reads bit-identical. On the profiled attacker the projection is a near-perfect
re-expression of breadth (Spearman +0.965, over the 0.90 kill), so it ranks
defences by breadth damage rather than by whether they attack the learned quantity.
The frontier is **retired as an axis-7 instrument**, on evidence, by its own kill
criterion; the constraint is **substrate, not a fixable instrument defect** — the
same wall axis 6 hit. Axes 6 and 7 stay DESIGNED; no badge moves.

The full record, including the backup "runtime characterisation" framing, how the
reservation is implemented (an external `budget` argument, *not* an attacker
capability, and not Brown's `ATTACKER_THRESHOLD`), the concrete demonstration arm,
and the axis-7 validation path this narrows to (cross-mutation retention against a
matched control), is in
[`../implementation/pipeline/ogasp/exploit_learning_disengagement_findings.md`](../implementation/pipeline/ogasp/exploit_learning_disengagement_findings.md).
Pre-registration:
[`../implementation/pipeline/ogasp/exploit_learning_disengagement_prereg.md`](../implementation/pipeline/ogasp/exploit_learning_disengagement_prereg.md).

## The merge dependency — read before merging to `dev`

- Branch: **`feat/axis7-disengagement-clean`** (prereg 6624720 + findings, two doc
  files only, no code).
- It is based on **`55f5094`** (the compound-exploit-learning landing), which is
  **on `feat/exploit-learning-mechanism`, not yet on `dev`**. So merging this
  branch to `dev` would drag the mechanism in prematurely. **Merge it into `dev`
  only after — or together with — `feat/exploit-learning-mechanism`.**
- Its only code dependency is the shipped `exploit_learning_rate` hook, already in
  `55f5094`; the sweep harness lives under `data/results/exploit_learning_disengagement/`
  (gitignored, regenerable via `run_sweep.py` + `analyse.py`).

## Concurrent-session git note (Marc's call, not actioned)

This session collided on a shared working tree with the parallel pool-experiment
session (HEADs swapped mid-task; reflog-confirmed). Consequences, all
content-safe:

- My work was rebuilt cleanly onto `feat/axis7-disengagement-clean`; the polluted
  intermediate branch was deleted (content preserved).
- **Two of my commits are buried in `feat/exploit-learning-mechanism`'s history**
  — findings `0ec01d2` and documentation `e75b761`, both landed there when the
  concurrent session swapped HEAD mid-commit (twice). Both are content-identical to
  the copies now on this branch (`c201409`, `06e1131`), so a `dev` merge is
  conflict-free, but that branch carries duplicates of my commits under its own
  trail. Dropping them would be a history rewrite on an actively-used branch —
  **left for Marc**, not actioned.

## Retirement

Delete this handoff when `feat/axis7-disengagement-clean` lands in `dev`. Never
push; the branch is local for review.
