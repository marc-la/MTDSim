# Baseline goldens — change log

Every intentional re-baseline lands here with what / why / spec-IDs. The
on-disk goldens are the behavioural oracle for the inherited substrate;
*any* change to their headline numbers must have an entry below or the
diff is a regression to chase, not a re-baseline to accept.

---

## 2026-05-25 — Phase 2c: metric-faithfulness re-baseline

**Spec-IDs:** MTD-14 (fixed), MET-04 / C8 (fixed), MET-08 (deferred), NET-13 / C3 (docs-fixed).

**What changed.** Replaced the contents of `baseline/golden/` in place; the
Phase-2b goldens are *not* preserved in a parallel archive because the 2c
fixes ride on top of the same corrected substrate (the `golden_phase0_buggy/`
archive remains the meaningful "before"). Three code-level fixes drove the
movement (one logical fix per commit; goldens captured at the end):

1. **MTD-14** (commit `f767349`) — `MTD_DURATION` for
   `CompleteTopologyShuffle` (120→110) and `IPShuffle` (110→100) brought
   into line with Zhang 2023 Table 3. Other techniques (HostTopologyShuffle,
   OSDiversity, PortShuffle, ServiceDiversity, UserShuffle) already matched.
2. **C8 / MET-04** (commit `8d4b8c3`) — `host_compromise_ratio` in
   `evaluation_result_by_compromise_checkpoint` now divides by `host_num`
   (Ho 2024's `C_t / T_host`), not by the checkpoint target. Phase-0 finding
   F-10 is closed; HCR is now bounded in [0, 1] at every checkpoint. A
   regression test (`tests/test_crash_fix_regressions.py::test_c8_*`)
   asserts the invariant.
3. **MET-08** (commit `eb0475b`) — *no code change*; spec disposition
   re-stated as `deferred` after recon showed the time-based scheduling
   path never updates `last_mtd_triggered_time` (only the Tay RL paths
   do). No golden movement attributable.
4. **NET-13 / C3** (commit `2032273`) — docs-only; README + spec
   re-aligned to the code's `[0, 10]` impact range. No golden movement.

**Per-fix headline movement (seed=1234, finish_time=15000, 50-node geometry
unless noted).** Pre-column = Phase-2b goldens; post-column = Phase-2c.

| scenario              | attacks 2b → 2c | MTDs 2b → 2c | compromised 2b → 2c | summary HCR 2b → 2c |
|-----------------------|-----------------|--------------|---------------------|---------------------|
| `no-mtd`              | 692 → 692       | 0 → 0        | 41 → 41             | 0.82 → 0.82         |
| `no-mtd_seed1234_rep` | 692 → 692       | 0 → 0        | 41 → 41             | 0.82 → 0.82         |
| `no-mtd_seed9999`     | 771 → 771       | 0 → 0        | 41 → 41             | 0.82 → 0.82         |
| `single-ipshuffle`    | 997 → **1228**  | 52 → **75**  | 41 → **35**         | 0.82 → **0.70**     |
| `single-osdiversity`  | 964 → 964       | 45 → 45      | 41 → 41             | 0.82 → 0.82         |
| `random-multi`        | 994 → 875       | 47 → 42      | 41 → 41             | 0.82 → 0.82         |
| `alternative-multi`   | 946 → 871       | 44 → 40      | 41 → 41             | 0.82 → 0.82         |
| `simultaneous-multi`  | 777 → 765       | 44 → 44      | 41 → 41             | 0.82 → 0.82         |
| `primary-random-15k` (100n, seed=42) | 1477 → 1366 | 75 → 65 | 81 → 81       | 0.81 → 0.81         |

**Per-column attribution:**

- **Attack/MTD counts** moved on every scenario that uses
  `CompleteTopologyShuffle` or `IPShuffle` in its scheme — i.e. every multi
  scheme and `single-ipshuffle`. Attribution: **MTD-14**. Scenarios that
  exercise neither (`no-mtd`, `single-osdiversity`) show **0-event
  movement**, which is the sanity check that no unintended regression
  crept in.
- **Summary `host_compromise_ratio`** (= `len(compromised) / total_nodes`,
  computed in `baseline/run_baseline.py`) is unchanged on every scenario
  *except* `single-ipshuffle`. There, faster IPShuffles (mean 100 ms vs
  110 ms) fit 75 MTDs into the 15 ks window instead of 52, enough to keep
  the attacker below the 0.8 NCR cutoff for the full sim — so the run
  terminates at the time bound (`fin=15000`) rather than at compromise
  threshold, leaving HCR at 0.70. Attribution: **MTD-14** propagating
  through the defence effectiveness curve.
- **`evaluation.json` `host_compromise_ratio` column** — every entry across
  every scenario was previously > 1 (pre-2c values: `[1.20, 1.20, 1.07,
  1.10, 1.04]`-shape across the `[0.05, 0.1, 0.15, 0.2, 0.25]` checkpoint
  list). Post-2c those values are `[0.06, 0.12, 0.16, 0.22, 0.26]`-shape
  (i.e. ≈ checkpoint ratio, occasionally one host over). Attribution:
  **C8**. The invariant `HCR ∈ [0, 1]` holds at every checkpoint of every
  scenario after the fix — directly verified.
- **`time_to_compromise` and `attack_success_rate` columns** shift
  slightly on scenarios where MTD-14 changed the attack/MTD interleaving
  (e.g. `random-multi` ckpt-4 TTC 9.24 → 8.76; `single-ipshuffle` TTCs
  rise as more MTDs interrupt). Attribution: **MTD-14** (timing
  redistribution). MTTC values for scenarios with no MTD-14 effect
  (`no-mtd`, `single-osdiversity`) are unchanged.
- **No movement attributable to MET-08 or C3** — MET-08 is deferred (no
  code change), C3 is docs-only.

**Determinism (SIM-05).** Verified: `baseline/golden/no-mtd` and
`baseline/golden/no-mtd_seed1234_repeat` have byte-identical
`attack_record.csv`, `mtd_record.csv`, and `evaluation.json`. The
seed=9999 counter-case still produces a different attack trajectory (771
attacks instead of 692), confirming the seed is load-bearing.

**Provenance.** No new archive directory created (per 2c discipline:
`golden_phase0_buggy/` stays the meaningful "before"; this CHANGELOG
carries the 2b→2c delta). Phase-2b's row above and this row together
narrate the substrate's full state movement from the buggy Phase-0
baseline through the corrected 2b substrate to the metric-faithful 2c
substrate.

---

## 2026-05-25 — Phase 2b: corrected-substrate re-baseline

**Spec-IDs:** SIM-05, R1, R2, R2-attacker, R3.

**What changed.** Replaced the contents of `baseline/golden/` and moved
the prior Phase-0 goldens to `baseline/golden_phase0_buggy/` for
provenance. The new goldens were produced on the post-Phase-2b
substrate (commit `aed80c1`..`a458f9a` on `feat/crash-fix`) and:

- All Phase-0 matrix scenarios now run to `finish_time=15000` (was
  `3000`). The Phase-0 horizon was too short to exercise the
  termination path on the buggy substrate; on the corrected substrate it
  terminates at NCR=0.8 well before 15 ks for every scenario.
- Added `primary-random-15k/` for the Tay-flagship PRIMARY config
  (100 nodes / 8 subnets / 4 layers / seed 42 / scheme=random /
  finish_time=15000). This is the canonical comparison point for any
  future substrate-affecting work and the headline target for §5.

**Why.** The Phase-0 goldens were captured on a substrate that silently
mis-executed past sim_t≈6.5 ks (recon: `docs/findings/crash_6000s.md`).
Numbers from those runs reflect a sim where R1's hard-coded 0.25
threshold tripped early, R2's missing `return` kept the MTD trigger
loop spinning, and R3's missing `release()` permanently parked both
layer simpy resources after the first leak. The Phase-2b corrections
restore the intended behaviour, so the goldens have to be re-captured.
Keeping `golden_phase0_buggy/` makes the supersession auditable.

**Headline movement (seed=1234, finish_time=15000 unless noted):**

| scenario             | old (Phase-0 buggy)              | new (Phase-2b corrected)         |
|----------------------|----------------------------------|----------------------------------|
| `no-mtd` (50n)       | 384 attacks · 0 MTDs · 17/50 (HCR 0.34) · fin=3000 | 692 attacks · 0 MTDs · 41/50 (HCR 0.82) |
| `random-multi` (50n) | 359 attacks · 15 MTDs · 7/50 (HCR 0.14) · fin=3000 | 994 attacks · 47 MTDs · 41/50 (HCR 0.82) |
| `primary-random-15k` (100n, seed=42) | n/a (PRIMARY not captured Phase-0) | 1477 attacks · 75 MTDs · 81/100 (HCR 0.81) |

`random-multi` last-checkpoint MTTC moves from 8.75 (buggy substrate,
truncated at 0.14 HCR) to 9.24 (corrected substrate, full 0.82 HCR run).
Direction-of-change is the only thing comparable here — the old run
never reached the same compromise checkpoints, so the MTTCs are not
on the same axis.

**Determinism (SIM-05).** UUIDs are now seed-derived
(`uuid.UUID(int=random.getrandbits(128), version=4)`), so a fixed seed
produces byte-identical CSVs across repeat runs. Verified:
`baseline/golden/no-mtd` and `baseline/golden/no-mtd_seed1234_repeat`
have byte-identical `attack_record.csv`, `mtd_record.csv`, and
`evaluation.json`. `no-mtd_seed9999` is the seed-sensitivity counter-case.

**Scenario inventory (`baseline/golden/`):**

```
alternative-multi/        single-ipshuffle/         no-mtd_seed1234_repeat/
no-mtd/                   single-osdiversity/       no-mtd_seed9999/
random-multi/             simultaneous-multi/       primary-random-15k/
```

**Provenance.** Old goldens preserved verbatim in
`baseline/golden_phase0_buggy/`. Re-baselines on the corrected substrate
go in `baseline/golden/`. The `internal` / `lineage` preset split is
under review in 2c; if `lineage` is dropped (likely, since C6 turned out
to be a bug not a divergence), `golden_lineage/` will never be created.
