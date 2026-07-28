---
status: open
created: 2026-07-28
---

# Rule MTD-scheme awareness out as future work rather than leaving it merely absent, and discharge the criterion's fired re-score triggers and stale cross-references

**Chain position: wave 5, independent.** Documentation only — no code, no run, no badge
moved on evidence that does not exist. Small, and worth doing early: the criterion is
loaded into **every** session by supervisor direction, so an inaccuracy in it costs more
than an inaccuracy anywhere else in the repo.

## State of play

**Axis 8 needs a disposition, not just a score.** MTD-scheme awareness — Jalowski's three
primitives (state-collision recognition, MTD-event-as-beacon, metadata-shadow invariance) —
is currently badged NOT ADDRESSED, and `architecture.md` §(f) records all three as *pending
encoding*, with an explicit note that each "can be promoted from *pending* to *encoded* or
*out of scope* independently". Marc has now ruled: encoding any of them needs machine
learning or reinforcement learning that the remaining timeframe cannot support, and **they
will not be implemented**. That is a promotion to *out of scope*, and it should be recorded
as a decision rather than left looking like unstarted work. "Not addressed" and "ruled out
with a reason" read very differently to an examiner, and only one of them is true.

One concrete detail worth carrying into the future-work paragraph, because it makes the
argument specific rather than general: `Adversary.observed_changes` is an empty dictionary
declared at `mtdnetwork/component/adversary.py:23` that **nothing in the repository ever
reads or writes**. It is the vestigial hook for exactly the attacker-observes-defender
channel primitive (ii) would need. Meanwhile the substrate does expose everything such a
primitive would consume — per-event MTD records with resource layer and timing, a computed
mutation-execution frequency, the currently-running and suspended mutations, cumulative
interrupt counts — all reachable from the adversary's live network handle without a single
substrate change. So the honest future-work statement is not "the simulator cannot support
it" but "the observation channel exists and is unwired; what is missing is the inference
capability and the time to build and validate it". Per-host mutation counts are the one
thing genuinely absent — no MTD strategy keeps per-target bookkeeping — and a beacon
primitive would have to derive or instrument them.

**Three re-score triggers in §(h) have fired since the criterion was written.**

- **The S3 timing implementation.** §(h) lists it as a standing trigger for axis 5's tempo
  half, and axis 5's body describes S3 as "CONJECTURED: ruled, with design and build
  handoffs open". Both handoffs have shipped: the timing design landed, the build landed,
  and Marc's S3-R reversal then made the movement layer the source of every unit of the
  attacker's time. The axis-5 text is stale on that point and understates what is built.
  Correct the description; **do not move the badge**, because tempo without a consequence
  is still not evasion — that reasoning is unaffected and is the axis's own argument.
- **The rate feasibility study qualified axis 2's evidence.** Axis 2's DEMONSTRATED badge
  rests on failure mode being a property of the profile rather than the seed. The rate study
  tested exactly that and returned "stable for four profiles, indeterminate for one" —
  `pure_steal` flips between horizon and sink termination in twelve cells, with central
  cells splitting seven-three and five-five, which makes its modal mode a coin-toss summary
  of a genuinely bimodal distribution. §(f) already carries one qualification of this badge
  from the S1 sweep; it needs a second. The badge does not fall; its evidence narrows again.
- **The degenerate-region finding constrains every axis scored on success rate.** At the
  200 s mutation interval every published run of this project has used, neither attacker
  completes the objective and the objective only becomes reachable above roughly 1 600 s.
  Inside that region success rate is pinned at zero and cannot discriminate anything. Several
  M8b fields and §(f)'s discussion lean on ASR-shaped reasoning; the criterion should carry
  the constraint once, prominently, rather than leaving each future session to rediscover it.

**Two stale cross-references, and two stale data artefacts.**

- §(f) quotes experiment 1's baseline figures. Those magnitudes are **stale**: the substrate
  was re-baselined and seven defects repaired after experiment 1 published, and the baseline
  now reaches the objective 0/10 under random MTD at 200 s where experiment 1 recorded
  10/10. The *findings* stand; the numbers are no longer a valid comparison target and should
  be marked rather than silently carried.
- Axis 1's M8b field recommends "deepest tactic band reached per run" as a progression
  measure. §(h) already records that this measure is saturated. The recommendation itself
  should be corrected in the axis body, not only annotated in the lifecycle section, since
  §(d) is what a session reads first.
- `data/ogasp/controller/lifecycle_consensus.json` carries a `worked_pairs` block that was
  **not recomputed** when `delta_ratio` moved 0.5 → 0.25 on Marc's persistence ruling. Its
  two backward examples are stale: `exfiltration → initial-access` should read 0.25 and
  `impact → reconnaissance` should read 0.0625. The forward pairs and the within-stage value
  are correct, and the `delta_ratio` field itself was updated with its changelog note — only
  the worked examples lag.
- `docs/implementation/pipeline/ogasp/lifecycle_consensus.md` §6's worked-pairs table has an
  arithmetic slip in the same area: a two-stage backward move under δ = 0.25 is 0.25, not
  0.0625. The three-stage row *is* correct, and the narrative claim that the three-stage
  backward collapse falls under the floor holds — it is the two-stage row that is wrong.

Both artefact issues are examples-only and neither is consumed by the compiler, so no
compiled value is affected and the reproduction check would not catch them. That is exactly
why they need a human pass.

## Recommended approach

1. **Promote axis 8's three primitives from *pending* to *out of scope*** in
   `architecture.md` §(f), using the decision-block form that section already uses (why,
   cost, if revisited). The *why* is the timeframe and the ML/RL requirement; the *cost* is
   that the encoded subset — which bounds the contribution by that section's own argument —
   stays empty on this axis; the *if revisited* is that promotion changes the L3 contract and
   the attacker state space, which §(f) already states.
2. **Rewrite axis 8's "this model today" paragraph** in the criterion so it reads as a ruled
   exclusion with a reason, not as unstarted work. Keep it the bluntest honest negative — that
   framing is correct and valuable — but make the negative deliberate. Fold in the
   `observed_changes` detail and the "the channel exists, the inference does not" framing,
   which is a stronger and more specific future-work statement than the current one.
3. **Correct axis 5's description of the S3 timing state** without moving the badge, and say
   in one clause why the badge does not move.
4. **Add the rate study's qualification to §(f)**, in the same annotated-blockquote form the
   S1 qualification already uses, so the badge's evidence trail reads as a maintained history
   rather than a rewritten claim.
5. **Add the degenerate-region constraint** once, where a session will see it — §(b) beside
   the badge definitions is the natural home, since it governs what evidence *can* move a
   badge at all.
6. **Correct axis 1's M8b depth recommendation** and point it at the replacement measure the
   measurement-suite handoff produces, or at the coverage curve if that handoff has not
   landed yet.
7. **Mark experiment 1's magnitudes as stale where §(f) cites them**, with the reason.
8. **Fix the two lifecycle-consensus worked-example errors** — recompute the JSON's
   `worked_pairs` under δ = 0.25 and correct the doc's §6 table row. Note in the commit that
   no compiled value changes, so no version needs regenerating and no experiment is affected.
9. **Bump `updated` on every file touched**, per the implementation-subtree contract.

**Alternatives considered.** *Fold this into whichever session next edits the criterion* —
rejected: that is how the four stale items above accumulated, and the criterion is the one
implementation file loaded unconditionally every session, so its accuracy compounds.
*Rewrite the axis-8 section wholesale* — rejected: investigation records and scored
instruments are annotated in place rather than rewritten, which is the convention the rest of
the file already follows.

## Validation gate

Done when:

1. `architecture.md` §(f) carries a decision block promoting all three Jalowski primitives to
   *out of scope*, with the reason.
2. Criterion axis 8 reads as a ruled exclusion, and the future-work statement names the
   unwired observation channel specifically.
3. Axis 5's S3 description matches what is built; the badge is unchanged and the reason is
   stated.
4. §(f) carries the rate study's qualification of axis 2, in the existing annotation form.
5. The degenerate-region constraint appears once, near the badge definitions.
6. Axis 1's M8b depth recommendation is corrected.
7. Experiment 1's cited magnitudes are marked stale with the reason.
8. `lifecycle_consensus.json` `worked_pairs` recomputes correctly under δ = 0.25 and the doc's
   §6 row is fixed; `python -m mtdsim.l3_simulation.controller.rules --check` still reports
   zero differing cells for every registered version, confirming nothing compiled moved.
9. `updated` bumped on every file touched.

## Hard constraints

- **No badge moves.** Every change here is descriptive accuracy, a ruled exclusion, or an
  evidence qualification. Badges move on run evidence only, and never to flatter a row (S6).
- **Annotate, do not rewrite.** Investigation records and scored instruments are immutable
  history with status banners; §(f)'s existing qualification blockquote is the pattern.
- **The modest-claim ceiling holds** — envelope, not actor, everywhere the text is touched.
- **Do not "fix" the stale experiment-1 numbers by recomputing them.** They are the record of
  what that run produced; the correction is to mark them as no longer a valid comparison
  target, not to overwrite history.
- Australian English; branch and commit rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.

## Reading list

- `docs/implementation/apt_model_criterion.md` — the whole file, especially §(b) badges,
  §(d) axes 1, 2, 5, 8, §(f) and §(h). It is the artefact being maintained.
- `docs/implementation/architecture.md` §(f) — the three primitives as *pending*, the
  promotion mechanism, and the decision-block form to copy.
- `docs/implementation/pipeline/ogasp/rate_feasibility_study.md` §7 (C3b and C5) — the axis-2
  qualification and the degenerate region.
- `docs/implementation/pipeline/ogasp/lifecycle_consensus.md` §6 and
  `data/ogasp/controller/lifecycle_consensus.json` — the two worked-example errors.
- `mtdnetwork/component/adversary.py` — `observed_changes`, the unwired hook; and
  `mtdnetwork/statistic/mtd_statistics.py` for what a beacon primitive could already read.

## Out of scope (explicitly)

- Implementing any Jalowski primitive. That is the point of the handoff.
- Moving any badge, on any axis.
- Re-running anything, or recomputing experiment 1's numbers.
- Regenerating any overlay version — the worked-example fixes touch documentation values
  only, and if a compiled cell moves, something else is wrong and should be investigated
  rather than committed.
- Dissertation prose.
