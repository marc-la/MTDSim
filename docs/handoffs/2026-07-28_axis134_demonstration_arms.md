---
status: shipped — awaiting reconciliation
superseded_note: shipped 2026-07-29 — all six gate items discharged by experiment 2 on `feat/exp02-ashen-lynx`; axis 3 moved to DEMONSTRATED, axes 1 and 4 held on their pre-registered criteria. Retire on reconciliation (`2026-07-29_reconcile_stranded_axis_work.md`). Nothing replaces it.
created: 2026-07-28
---

# Pre-register the badge criteria for persistence, strategic plurality and adaptivity, then run the arms that decide them — including the verdict-blind ablation that separates *reacts* from *adapts usefully*

**Chain position: wave 5, after the measurement suite and alongside experiment 2.**
Depends on `2026-07-28_axis_measurement_suite.md` for every measure it reports. Its run
should be **folded into experiment 2** (`2026-07-27_sink_retrace_experiment2.md`) rather
than executed as a separate matrix — experiment 2 already carries the defence-family
sweep, already owes a criterion scoring, and re-running the whole matrix twice buys
nothing. What this handoff adds to that run is one extra arm, a two-dimensional reporting
requirement, and the pre-registered criteria that decide three badges.

## State of play

Three of the criterion's eight axes sit at **DESIGNED**: the mechanism exists but has not
been shown to change an outcome. All three are decidable by measurement plus one
comparison, and none needs a model change or a lifted freeze.

**Axis 1 — persistence.** The 15-place net executes end to end and 100 coupled runs
traversed it, but persistence in *outcome* terms is not evidenced: 0/100 objective reaches,
and an effort-to-breadth ratio an order of magnitude worse than the baseline. The badge is
deliberately held, because a rubric that scored persistence "captured" on structural
grounds alone would be reverse-fitted. What changed since: **`v3_persistent_backward`
landed** (the δ kernel moved 0.5 → 0.25 on Marc's ruling that an attacker persistent enough
to reach exfiltration does not abandon its foothold to re-scan the perimeter), so there is
now a persistence *mechanism* in the weights that has never been run. And the depth measure
the axis's own M8b field recommends is saturated, which is why this handoff cannot proceed
before the measurement suite lands.

**Axis 3 — strategic plurality.** Attacker-side plurality is structural: each class net is
the union of 5–19 analyst-drawn flows, branching per seed. The defender side is plural by
design — eight MTD mechanisms under four schemes, plus Tay's selection. But the plural
*evaluation* has never run: experiment 1 covered one corner (no-MTD against one scheme).
Two things are therefore unevidenced and separable — that traversal actually diversifies
(measurable now), and that outcomes vary over **both** the profile and the defence-family
dimensions rather than one (needs the matrix). The criterion also records the honest
limit: the branching is not *chosen*, only drawn, so plurality here is variety, not
strategy — that boundary must survive into whatever is claimed.

**Axis 4 — adaptivity.** The minimal adaptive loop is built and demonstrably *operates*:
blocked verbs and MTD interrupts read as failure and re-route the token, verified live
(`runtime_verification.md` §P5 records failure swinging `initial-access → reconnaissance`
from 0.004 to 0.643). It demonstrably does not yet *help*: the observable consequence was
churn and friction. **Nothing on record separates those two statements**, because every run
to date has had the loop switched on. That is the gap this handoff's main new arm closes.

**Two findings from the wave-3 sweeps that constrain the run.** The operating mutation
interval of 200 s sits inside a degenerate region where neither attacker completes the
objective, so ASR cannot discriminate there and the objective only becomes reachable above
roughly 1 600 s — experiment 2 must **choose** its interval rather than inherit it. And ten
seeds cannot separate adjacent profiles, established twice over unrelated parameter
families, so any ordering claim needs either more seeds or an explicit statement of which
claims the run is not powered for.

## Recommended approach

**Part A — pre-register, in its own commit, before any output exists.**

This project has run two studies on this discipline and it has paid off both times; do not
depart from it. Write the criteria down and commit them **before** the first run.

1. **Fix the badge criterion for each axis in advance**, in the criterion's own vocabulary
   (`DEMONSTRATED` = evidenced by a run on record; `DESIGNED` = mechanism exists, outcome
   unchanged). Proposed criteria, to be argued or amended but not left implicit:

   - **Axis 4 → DEMONSTRATED** if the verdict-conditioned arm differs from the
     verdict-blind arm on at least one progression measure, with disjoint 95 % intervals,
     in at least two profiles and at two or more defence conditions. If the arms are
     indistinguishable, the honest outcome is that the loop reacts and does not adapt
     usefully — the badge stays DESIGNED and *that becomes a reportable finding*, which is
     more valuable than a soft pass.
   - **Axis 3 → DEMONSTRATED** if per-profile traversal diversity is non-degenerate (path
     entropy bounded away from zero, more than one distinct tactic-sequence prefix across
     seeds) **and** outcomes vary over both the profile and the defence-family dimensions
     — an interaction, not a single main effect. A defence ranking that is identical for
     every profile evidences defender plurality only, and must be reported as such.
   - **Axis 1 → DEMONSTRATED** if sustained staged advance is evidenced on the replacement
     progression measure — deepest *successfully actioned* stage, or foothold retention
     across at least one mutation — in a non-trivial fraction of runs. Otherwise DESIGNED,
     with "the structure runs and does not convert to progress on this substrate" recorded
     as the finding.

2. **State which claims the run is not powered for**, before it runs. If the seed budget
   will not separate adjacent profiles, say so in the pre-registration rather than
   discovering it in the analysis for the third time.

3. **Choose the mutation interval deliberately and justify it.** Running at 200 s means
   reporting the region rather than the attacker. Running above 1 600 s leaves the interval
   every prior run used. Both are defensible; inheriting silently is not. Consider carrying
   both as a tempo dimension, since the degenerate boundary is itself a result worth
   showing.

**Part B — the verdict-blind ablation arm (the axis-4 instrument).**

The composition rule is `w' ∝ base · overlay_v`, renormalised. An overlay whose success and
failure tables are **identical** reduces composition to the renormalised base weights, so
the token routes on observed structure alone and the substrate's verdict has no
consequence. That is precisely "the adaptive loop off", and it is the control the axis-4
claim has always lacked.

4. **Build it as an empty value table, not a new rule.** `OutcomeOverlay.from_values` with
   an empty per-verdict mapping gives factor 1.0 at every pair, because `compose` treats an
   absent pair as passthrough. No change to `rules.py`, no new spec knob, no new compiled
   files. **Assert the identity in a test** — a verdict-blind run must produce the same
   routing distribution as a hypothetical no-overlay run at every place — so the arm is
   demonstrably a null and not a subtly different policy.
5. **Register it in `data/ogasp/controller/overlays/manifest.json` only once a published
   run consumes it**, following the registry's own rule that a version becomes immutable
   when an experiment consumes it. Until then it is an in-memory arm, which is how the S1
   sweep drove its own points.
6. **Hold everything else identical between the arms** — same seeds, same mapping version,
   same timing regime, same geometry. The whole value of the ablation is that one factor
   moved.

**Part C — the two-dimensional matrix (the axis-3 instrument).**

7. **Report the defence dimension by mechanism, not only by condition.** The S1 sweep found
   a ~90 % host-count suppression under `v2_partial` that is stable across the entire weight
   sweep — the most promising thing on the table, and currently only known as
   "MTD on against MTD off". Axis 3 needs it resolved per mechanism, and so does the
   thesis's central divergence claim.
8. **Report the profile dimension and the defence dimension jointly.** The claim is that
   outcomes vary over both. A table of profile main effects beside a table of mechanism
   main effects does not evidence it; a profile × mechanism grid does.
9. **Name both declared inputs at the experiment seam** — the mapping version and the
   overlay version. Per the weight study's most recent statement, the go-forward overlay is
   **`v3_persistent_backward`**, not `v2_lifecycle_distance`; the older figure appears in
   the experiment-2 handoff and the chain README because both predate the ruling. Note that
   `run_movement` currently has **no `overlay_version` parameter** (the trace runner does) —
   either pass a constructed overlay object, or add the parameter beside `mapping_version`
   for symmetry, which is a small and obviously correct refinement.

**Part D — score and promote.**

10. **Score the run against the criterion and move only the badges the pre-registered
    criteria say move.** Never adjust the model, the weights, the mapping or the metrics to
    improve a row — that is the standing S6 constraint and it is the whole reason the
    rubric is worth loading every session.
11. **Promote the findings into a tracked record.** The run workspace is gitignored; a
    result that only lives there does not exist for the next session.

**Alternatives considered.** *A separate matrix rather than folding into experiment 2* —
rejected: duplicated cost, and two runs on possibly different substrate states would not be
poolable. *An ablation that disables the overlay entirely rather than blinding it* —
rejected as the same thing with a code path instead of data; blinding keeps the arm inside
the registry discipline and needs no branch in the driver. *Deciding axis 4 by inspecting
the routing distributions rather than by outcome* — rejected: that re-evidences that the
loop operates, which is already on record, and says nothing about whether it helps.

## Validation gate

Done when:

1. The pre-registration exists as its own commit, dated before the first result file, and
   states the three badge criteria, the powered/unpowered claim list, and the chosen
   mutation interval with its justification.
2. The verdict-blind arm exists, is test-pinned as a genuine null (identical routing to
   base-weight-only), and has been run against the conditioned arm on identical seeds.
3. The profile × mechanism grid exists with intervals, and the ~90 % suppression is either
   confirmed per mechanism or withdrawn.
4. Each of the three axes has a written verdict — moved or held — traceable to its
   pre-registered criterion, with the numbers behind it.
5. `apt_model_criterion.md` is updated only where a criterion was met, with `updated`
   bumped and the §(f) demonstration section extended rather than rewritten.
6. Findings promoted into a tracked record under
   `docs/implementation/pipeline/ogasp/`; the handoff deleted in the commit that ships it.

## Hard constraints

- **Badges move on evidence only.** Never change the model, weights, mapping or metrics to
  improve a row (S6). A disappointing arm is a finding, not a prompt to retune.
- **No tuning in reaction to the numbers.** Parameter adjustment is reviewed work with its
  own handoff, never a same-session response.
- **Envelope, not actor.** Every claim is about a behavioural envelope under a declared
  policy, never a named adversary's campaign.
- **Within-substrate comparability only** — internal timing measures, no cross-paper
  magnitude claims. Experiment 1's published baseline magnitudes are **stale** (the
  substrate was re-baselined and the timing regime changed since), so they are not a valid
  comparison target; re-measure the baseline in the same run.
- **The S2 action-set freeze holds**, and the H-coupling finding must stay visible — an arm
  that quietly routes around unmet preconditions would hide it.
- Determinism / SIM-05; Australian English; branch and commit rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.

## Reading list

- `docs/handoffs/2026-07-27_sink_retrace_experiment2.md` — the run this folds into; read it
  first and treat this handoff as an amendment to its matrix and its reporting.
- `docs/implementation/apt_model_criterion.md` §(d) axes 1, 3, 4 and §(f) — the badges, why
  each is held, and the discrimination check §(f) closes on.
- `docs/implementation/pipeline/ogasp/weight_sensitivity_study.md` §5 — the ~90 %
  suppression to confirm per mechanism, the seed-count constraint, and §3b for why
  experiment 2 should name `v3_persistent_backward`.
- `docs/implementation/pipeline/ogasp/rate_feasibility_study.md` §7 (C5) — the degenerate
  region, which decides the mutation interval.
- `src/mtdsim/l3_simulation/controller/outcome.py` — `compose` (the passthrough-on-absent
  rule the verdict-blind arm relies on), `from_values`, and the registry loader.
- `data/ogasp/controller/overlays/manifest.json` — the registry contract a new version
  would have to satisfy, and the immutability rule.

## Out of scope (explicitly)

- Building the measurement suite. That is `2026-07-28_axis_measurement_suite.md` and this
  handoff consumes it.
- Any new attacker mechanism — stealth, learning, or a cost model. Those are separate
  handoffs and must not enter this comparison, or the ablation stops being a one-factor
  contrast.
- The sink-retrace design and implementation. That is experiment 2's own Part A.
- Axes 2, 5, 6, 7, 8.
- Dissertation prose.
