---
status: open
created: 2026-08-13
topic: "Axis 4 — the structural-route probe: a reader-only check of whether post-interrupt terrain carries structure a pivot kernel could exploit, converting the 2026-08-11 closure's parked route into an evidence-backed one"
---

# Axis 4 — probe the structural route before any pivot kernel exists

**Goal (one line):** determine, from existing machinery and seeded reruns only,
whether the terrain in the window after an MTD interrupt systematically rewards
any tactic set over the ordinary weights — the empirical question the
2026-08-11 axis-4 closure parked, and the only route by which a
"pivot-to-recover" mechanism could confer advantage.

## State of play

- The 2026-08-11 disposition (criterion §(d) axis 4) closed the axis's null
  advantage as intractable via attacker-blindness: the **reactive** route is
  closed structurally (every defence in the pool is clocked and
  attacker-blind), **mechanism-shape** is bounded first-principles (same
  one-bit verdict), and the **structural** route — does blockage persist or
  re-randomise — was explicitly *not pursued*. Parked is not falsified.
- Marc's 2026-08-13 objection is the one an examiner can raise: the attacker
  *does* feel the defence (the confusion penalty — `PENALTY = 20`, drawn
  `exponential_variates(20, 0.5)` in `attack_operation.apply_mtd_interrupt_cost`,
  which also clears the host cursor; the movement arm additionally throws the
  net state back, M1). The proposed frame: a declared recovery-tactic set plus
  a temporary weight-transformation kernel on the interrupt event, giving the
  attacker declared "pivot to recover from disruption" behaviour.
- The assessment on which this brief was opened: the kernel is mechanically
  possible and idiomatic (declared family + modulator on the attacker-state
  seam + identity-kernel null giving bit-identity ablation + prereg and
  sweep), but it only *pays* if the post-interrupt terrain differs
  systematically from elsewhere-in-run in a way the recovery set matches.
  Precedent says friction-shaped modulators operate without advantage
  (axes 6, 7). So the probe comes first; the kernel is gated on its result.
- What an interrupt actually destroys, for "recovery" semantics: the position
  cursor and (when the learner is on) a declared fraction of belief — never
  owned hosts. Recovery honestly means re-acquisition of position.

## Recommended approach

1. **Pre-register before any output** (the standing discipline): the window
   definition, the comparison, and the decision rule below, committed before a
   single record is read.
2. **Reader over existing record streams — no mechanism, no new declared
   values.** Regenerate a shipped seeded grid deterministically (the
   experiment-2 arms suffice) and compute, per profile: per-tactic verdict
   profiles (success/failure/blocked shares) inside the *n*-visit post-interrupt
   window against elsewhere-in-run. `interrupt_action_mix` and
   `recovery_times` in `movement/measures.py` are most of the machinery; what
   is new is conditioning the *verdict* profile (not just the mix) on the
   window. Report through `interval_report` as always.
3. **Decision rule (pre-registered):**
   - **No structure** (post-window verdict profiles statistically
     indistinguishable from elsewhere, or distinguishable only in the
     direction the ordinary failure-column weights already route toward) →
     the structural route closes on evidence. Draft a criterion §(d) axis-4
     amendment in the §4.3-amendment style: all three routes now closed —
     reactive structurally, mechanism-shape first-principles, structural
     empirically — and the intractability sentence becomes airtight against
     the pivot-kernel objection. No kernel is built.
   - **Structure present** → the kernel has a target. Before any build: the
     recovery set must be grounded in the ch3 tactic-profile evidence (so it
     lands attested-pattern/declared-magnitude, not pure declared judgement —
     row A cost otherwise), and the build is gated on Marc reopening the
     2026-08-11 disposition (a register/V-trail entry) and on the S2 freeze
     for any reported non-null configuration.
4. **Alternative considered and declined:** building the kernel first and
   letting its sweep answer the terrain question. Declined because a null
   kernel sweep cannot separate "no structure to exploit" from "wrong kernel"
  — the probe answers the terrain question directly and costs no declared
   family.

## Validation gate

Done when the pre-registration and the probe's findings record are committed
(prereg first, findings in a later commit), the decision rule has fired one
way or the other, and either (a) the axis-4 amendment draft exists for Marc's
ratification, or (b) the kernel design brief exists with its corpus-grounding
requirement and its gating rulings named. This handoff is deleted in the
commit that ships whichever record closes it.

## Hard constraints

- Reader-only: no simulation-behaviour change, no new declared magnitudes.
- Determinism: seeded reruns of shipped grids only; the configuration
  described is the configuration measured.
- The 2026-08-11 disposition stands until Marc reopens it; this probe
  informs a ruling, it does not constitute one.
- Quasi-periodic trigger caveat: the substrate's MTD clock is effectively
  periodic (see the sibling axis-8 re-examination handoff), so post-interrupt
  windows are near-evenly spaced — window length must be chosen well inside
  the inter-mutation interval to avoid windows overlapping the next tick.

## Reading list

1. [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md) §(d) axis 4, including the 2026-08-11 disposition (loaded every session anyway).
2. [`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md) §(b) — `interrupt_action_mix`, `recovery_times`, `interval_report` contracts and blind spots.
3. [`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md) — the arms to regenerate, and §11 (the verdict-blind matched control).
4. [`../implementation/boundary_attacker_defender_channels.md`](../implementation/boundary_attacker_defender_channels.md) — what each mechanism class actually destroys (what "recovery" could mean per class).
5. [`../implementation/pipeline/ogasp/axis_instrumentation_method.md`](../implementation/pipeline/ogasp/axis_instrumentation_method.md) — the instrumentation protocol this probe follows.
