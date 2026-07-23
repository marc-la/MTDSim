---
status: open
created: 2026-07-15
---

# Pull the first numbers — run the MTD × profile experiment matrix on the coupled attacker, report MTTC/ASR with the M8 expectation on record, run the metrics-gap review, and draft the update to Jin

> **Last in the forward chain.** The **controller finalisation is done** — its handoff
> is retired (all five gate items met) and the success/failure outcome overlay is
> **finalised at R2** (see State of play). The remaining upstream piece is the attacker
> Petri → MTDSim build
> ([`./2026-07-22_l3_attacker_petri_to_mtdsim.md`](./2026-07-22_l3_attacker_petri_to_mtdsim.md)).
> Per the meeting: implementation is the last major piece; after it, "pull
> some numbers, then review based on what numbers we get". The M8
> expectation is pre-registered here so the result reads as a finding either
> way: the profiled attacker is **expected to do no better** than the basic
> attacker on pure security metrics — the basic attacker is geared to this
> substrate; APT-shaped behaviour spends effort the current metrics don't
> reward. "It could go either way; we have to run it and see" (Jin).

## State of play

- The matrix shape is standing: `MTD mechanism (SDR family + Tay AI
  selection, existing only) × {6-phase baseline, 4 class profiles,
  aggregate} × N seeds`. Simulation horizon and MTD intervals are free
  experimental variables (R4) — set them to suit the coupled attacker's
  scale, and record the choice.
- Metrics: internal MTTC (primary), ASR, attack-path exposure, RoA
  ([`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md));
  E1 discipline — end-of-sim compromise fraction is a poor discriminator at
  long horizons.
- The M8 metrics-gap question is scheduled *now*, not later: once numbers
  exist, identify what supplementary evasion/stealth-shaped measurements
  would show where APT behaviour matters (measuring stealth is acknowledged
  tricky; this may land as ch5/ch6 material rather than new code).
- Jin expects regular updates in lieu of a fixed meeting slot while his
  semester-2 timetable settles.
- **Runtime model verified (2026-07-23), so this run measures what we think it
  measures.** The pre-experiment cross-examination is closed —
  [`../implementation/pipeline/ogasp/runtime_verification.md`](../implementation/pipeline/ogasp/runtime_verification.md):
  P1–P8 have recorded verdicts, the seams are pinned by tests, and two rulings
  land directly on this run:
  - **P7 sink-termination = accept-and-censor** (Marc, 2026-07-23). A walk that
    reaches a sink stops and is censored (no code change). `pure_steal` (@`impact`),
    `double_extortion` (@`credential-access`) and `infrastructure_setup`/observed
    (@`reconnaissance`) sink early, so they contribute **truncated MTTC windows** —
    **state this when reporting per-profile MTTC** (their denominator is shorter
    than the profiles that run to horizon).
  - **P4 H-coupling is a result to report, not a defect.** The verification pass
    already tabulated the blocked-fraction (`PRECONDITION_UNMET` / events) at
    horizon 15 000, and it spans **0 %–100 %** across profile × arm — carry that
    table (or the CI'd version from this run) into the write-up.
- **The success/failure outcome overlay is FINALISED (R2, 2026-07-23)** — this run
  consumes it as the net's policy layer, so the routing on each verdict is fixed.
  It is now **rule-based and complete**: canonical source
  [`../../data/ogasp/controller/outcome_rules.json`](../../data/ogasp/controller/outcome_rules.json)
  (model + rules, one rationale each), compiled to the full 210-pair
  `success.json` / `failure.json`; the corpus-scoped view is
  [`../../data/ogasp/petri/outcome_overlay.json`](../../data/ogasp/petri/outcome_overlay.json).
  It converged through four adversarial cross-examination rounds (~90 agents; the final
  finetune synthesis proposed zero changes), certified **82%** — the 82→95% remainder is
  the dissertation defence of the reasoning, not value uncertainty. **Carry its honest
  caveats into the write-up** (design
  [`success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  §2.5 + the provenance/scrutiny ledger
  [`../implementation/declared_value_provenance.md`](../implementation/declared_value_provenance.md)):
  the `ia_gate` soft-floor leaves a base-proportional IA-failure residual; a few band-4
  objectives take slightly more failure than success mass; sparse-profile point masses are
  non-conditionable; `enabled = 1.0` is a deliberate flat tier; and `infrastructure_setup`
  carries no exfil/impact node — which **reinforces the P7 sink-censoring**, so score
  objective-reach per profile rather than assuming every profile can terminate at an objective.

## Recommended approach

1. **Run the matrix**, seeded, with CIs; per-cell MTTC/ASR distributions.
2. **Two headline statements**, envelope-relative: (a) do the class
   profiles separate behaviourally *under MTD* (beyond the aggregate null)?
   (b) does any MTD mechanism's **ranking** change between the 6-phase
   baseline and a profiled attacker?
3. **Score against the M8 expectation**, explicitly: where the profiled
   attacker underperforms on pure metrics, say so and say why that was
   predicted; anything that beats the baseline is the surprising result and
   gets scrutinised, not celebrated.
3a. **Report the H-coupling** (P4) as a first-class per-profile finding: the
   blocked-fraction / compromise table, framed as the coupling the coarse
   experiment-1 controller exposes — not hidden as low compromise counts. And
   **state the tactic→verb collapse is a chosen input parameter** (`initial-access`
   → `SCAN_PORT` not exploit; the objective band → `SCAN_NEIGHBOR`), swappable via
   `controller.csv` — a coarseness by design, not a fidelity claim
   ([`../implementation/pipeline/ogasp/controller.md`](../implementation/pipeline/ogasp/controller.md) §2).
4. **The metrics-gap review (M8b):** from the observed records, propose the
   supplementary measurements (e.g. mutations absorbed per objective,
   post-mutation recovery cost, action-visibility mix) that would surface
   APT value — as a written recommendation for Marc/Jin, not as built
   metrics.
5. **Draft the progress update to Jin** (Marc sends): what shipped, the
   headline numbers, the metrics-gap recommendation, next steps.

*Alternatives considered:* folding this into the build handoff — rejected:
the build's gate is mechanical correctness; this one's gate is numbers and
their reading, and the meeting treated them as distinct steps.

## Validation gate

Done when:
1. The full matrix has run, seeded, with CIs, on the horizon/interval
   settings recorded as experiment-design choices (R4).
2. The two headline statements exist with numbers, phrased
   envelope-relative.
3. The M8 expectation is scored against the results in writing.
4. The metrics-gap recommendation exists (candidate measurements + what
   claim each would support).
5. The progress-update draft exists for Marc's review — **draft only; Marc
   sends**.
6. The H-coupling blocked-fraction table is reported per profile, the
   tactic→verb collapse is stated as a chosen parameter, and per-profile MTTC
   carries the sink-censoring caveat (the three P4/P7 carry-ins from the runtime
   verification).

## Hard constraints

- **No tuning in this handoff** — weight/success-rate adjustments are a
  reviewed follow-up (M8a), never a same-session reaction to the numbers.
- **Within-substrate comparability only**; internal MTTC; no cross-paper
  magnitude claims; envelope-not-actor phrasing throughout.
- Existing MTD mechanisms only; Tay's RL run as-is.
- Determinism (SIM-05); branch hygiene; **never push without an explicit
  ask**; Australian English.

## Reading list

- [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md)
  — metric definitions and the comparability boundary.
- [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
  — §M8 and R4.
- The build handoff's smoke-cell results — the shape of the records being
  aggregated.
- [`../../baseline/BASELINE.md`](../../baseline/BASELINE.md) — run
  conventions and seeds.

## Out of scope (explicitly)

- Building new metrics or any evasion/stealth instrumentation — recommend,
  don't build.
- R2/R3 tuning, style design, attacker-studies-MTD adaptivity (future work
  per M8d).
- The dissertation evaluation chapter — this delivers numbers and drafts,
  not chapter prose.
