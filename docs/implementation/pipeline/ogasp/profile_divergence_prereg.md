---
status: pre-registration
created: 2026-08-09
topic: "Attack-profile divergence — pre-registered conclusions for the first corpus run of the profile_divergence measure, with its execution-level null band (arms 1–2 of the objective-conditioning ablation; the size-matched control arm is out of scope here)"
---

# Pre-registration — attack-profile divergence on a recorded corpus

**Committed before any run output exists.** The commit order is the audit
trail, per house discipline and the parent handoff
([`../../handoffs/2026-08-09_objective_conditioning_ablation.md`](../../handoffs/2026-08-09_objective_conditioning_ablation.md)
§ Pre-register before running).

## What this study is, and is not

This study instruments and runs the **behavioural half** of the
objective-conditioning ablation: `profile_divergence` (`measures.py` §2) over a
fresh deterministic corpus of the five shipped profiles, plus the
**execution-level null band** that `measurement_suite.md` §(b) records as the
measure's open blind spot. The quantity under test — called **attack-profile
divergence** here — is the pairwise Jensen–Shannon divergence between profiles'
pooled visit distributions and terminal-tactic distributions (L2 convention),
read with particular interest in each class's divergence from `aggregate`, the
partition-off null.

It is **not** the ablation's deciding arm. The size-matched label-blind control
(handoff § Recommended approach, arm 3) has not run, and without it a
class-versus-`aggregate` separation remains confounded with corpus size
(`aggregate` carries 38 flows against the classes' 5–19). **No badge moves on
this study's evidence, in either direction.** A2/A3 of the handoff remain open
and belong to the session that runs the control arm.

## Corpus, fixed in advance

- Five profiles: the four objective classes plus `aggregate`.
- 50 seeds (0–49), horizon 15 000 s, `v2_partial` mapping, synthetic overlay
  on, retrace on — experiment 2's conditions.
- Two MTD conditions: `no_mtd` (primary — profile conditioning unconfounded by
  defence-injected variance) and `random_200` (the operating scheme/interval,
  reported beside it, because the badge's existing evidence lives under MTD).
- Simulated fresh through `run_movement` (SIM-05 determinism; the corpus is
  exactly re-creatable from the script and seeds).

## The null band, fixed in advance

Within-profile split-half JSD: for each profile and condition, its 50 runs are
split into two random halves of 25, the JSD between the halves' pooled
distributions is computed, and the split is repeated over R = 200 seeded draws.
This is the divergence attributable to seed noise alone at this sample size,
derived from the corpus rather than declared. A between-profile figure
**clears the null** for a pair when it exceeds the 97.5th percentile of the two
profiles' pooled null draws, on the same distribution half (visit stream or
terminal).

## Conclusions, criteria, directions

- **P1 — the measure clears its own null (handoff A1).** Every between-class
  pair's visit-stream JSD exceeds the pair's pooled null ceiling (97.5th
  percentile), in the primary condition. *Expected direction: clears — the L2
  structural check discriminated; a failure here would say the runtime walk
  collapses the structural difference, which is reportable and unflattering.*
- **P2 — divergence from the unsegregated profile.** Each class's visit-stream
  JSD to `aggregate` clears the same null. *Direction deliberately
  uncommitted*: a class that fails P2 behaves indistinguishably from the
  unpartitioned attacker at this sample size — evidence toward ablating the
  partition for that class — but the size confound means P2 in either direction
  is **not** the badge verdict; only the size-matched arm can be.
- **P3 — kill criterion (handoff A4, same 0.90 bar as the disengagement and
  exposure studies).** Spearman |ρ| between a class's visit-stream
  JSD-to-`aggregate` and its flow count, across the four classes, is below
  0.90 in the primary condition. At n = 4 the statistic is coarse; the exact
  value is reported with that caveat. *If |ρ| ≥ 0.90 the measure is flagged as
  a re-expression of flow-set size and must not be interpreted as behavioural
  conditioning anywhere downstream.*
- **P4 — the terminal half is reported, not gated.** The terminal-tactic JSD
  is expected noisier (few support points, 50 samples per profile); it is
  reported beside the visit half with its own null band, and no conclusion
  turns on it alone.

**The unflattering directions are committed explicitly.** A P1 failure (runtime
collapse of the structural separation) and a P2 failure (a class
indistinguishable from `aggregate`) are both reportable findings, and the
measure is not re-specified after seeing either.

## Validation gates inherited from the handoff

Readers only — no mechanism, no attacker capability, no declared value.
`tests/l3_simulation` passes; shipped artefacts byte-identical; every aggregate
through `interval_report` where an ordering is claimed; censoring (not
applicable here — no duration measure) n/a; determinism exact.
