---
status: open
created: 2026-07-15
---

# Pull the first numbers — run the MTD × profile experiment matrix on the coupled attacker, report MTTC/ASR with the M8 expectation on record, run the metrics-gap review, and draft the update to Jin

> **Last in the post-meeting chain — blocked on the profiled-attacker build**
> ([`./2026-07-15_l3_profiled_attacker_build.md`](./2026-07-15_l3_profiled_attacker_build.md)).
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
