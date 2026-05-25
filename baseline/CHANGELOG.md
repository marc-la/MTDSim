# Baseline goldens — change log

Every intentional re-baseline lands here with what / why / spec-IDs. The
on-disk goldens are the behavioural oracle for the inherited substrate;
*any* change to their headline numbers must have an entry below or the
diff is a regression to chase, not a re-baseline to accept.

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
