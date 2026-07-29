# Baseline goldens — change log

Every intentional re-baseline lands here with what / why / spec-IDs. The
on-disk goldens are the behavioural oracle for the inherited substrate;
*any* change to their headline numbers must have an entry below or the
diff is a regression to chase, not a re-baseline to accept.

---

## 2026-07-29 — Intent-audit re-baseline: the RoA stack and the diversity version re-roll

**Spec-IDs / audit-IDs:** IS-PRC-04 (D-10, fixed), IS-MTD-05/06 (D-05, fixed),
IS-INT-03 (D-07, fixed — golden-neutral), IS-MET-04 ASR (D-11, fixed —
metrics-only), IS-AI-02/06 (D-13/D-14, fixed — AI path only, not exercised here).

**Why.** The 2026-07-28 intent-spec conformance audit
(`docs/implementation/intent_conformance_audit.md`) classified the substrate
against the literature-only yardstick and produced a disposition list; Marc
approved the fixes 2026-07-29 ("fix any bugs that have surfaced or deviations
that you have spotted", with the Tay AI-seam integration explicitly deferred).
Two of the six fixes move the goldens:

- **D-10** — Brown §III-C(2): the vulnerabilities from all scanned services now
  form one priority stack **globally ordered by RoA** (`host.py get_vulns`),
  replacing the undocumented service-major ordering (farthest-from-target
  service first). Outcome-per-vuln is unchanged (the exploit loop attempts every
  vulnerability either way); what moves is the pairing of seeded RNG draws to
  vulnerabilities, i.e. the trajectory, not the rule's strength.
- **D-05** — Zhang §4.3.1.3/4: Service Diversity and the incompatible-service
  replacement in OS Diversity / DAP now draw a **random compatible service at a
  random version** (the same draw host generation uses), replacing the
  undocumented latest-version-only replacement. Latest-only had been quietly
  strengthening the defence (newest versions carry the fewest vulnerabilities);
  the documented version re-roll lets older, more-vulnerable versions reappear.

| scenario | attacks | MTDs | compromised |
|---|---|---|---|
| no-mtd | 1541 → 1494 | 0 → 0 | 41 → **41** |
| no-mtd_seed1234_repeat | 1541 → 1494 | 0 → 0 | 41 → **41** |
| no-mtd_seed9999 | 1698 → 1688 | 0 → 0 | 39 → **41** |
| single-ipshuffle | 1511 → 1584 | 75 → 75 | 32 → **32** |
| single-osdiversity | 1927 → 2023 | 75 → 75 | 2 → **3** |
| random-multi | 1605 → 1829 | 75 → 75 | 13 → **16** |
| alternative-multi | 1687 → 1814 | 75 → 75 | 11 → **10** |
| simultaneous-multi | 1570 → 1704 | 88 → 88 | 22 → **27** |
| primary-random-15k (100 nodes) | 1698 → 1801 | 75 → 75 | 6 → **6** |

The direction is coherent: the no-MTD control barely moves (D-10 reshuffles the
same work), IP Shuffle — which never touches services — holds at 32, and the
diversity-heavy schemes drift attacker-ward (random-multi 13→16, simultaneous
22→27), which is exactly what withdrawing the latest-version-only advantage
predicts. The defence still discriminates decisively against the 41-host control.

**Metrics note (D-11).** Checkpoint ASR now uses Ho's formula on both sides:
attempts count SCAN_PORT + EXPLOIT_VULN + BRUTE_FORCE events (previously
SCAN_PORT only) and the numerator is the hosts actually compromised in the
checkpoint slice (previously the checkpoint *target*). ASR values in
`evaluation.json` are therefore on a new, smaller scale — not comparable to
pre-2026-07-29 ASR readings.

**Pinned tests updated in the same commit:** the no-MTD headline 1541/41 →
**1494/41** (`test_action_layer_carve.py`, `test_movement_integration.py`,
`test_movement_smoke.py`); the ATK-04 spy counts re-captured (fire-rate range
now 0.7–9.6 %; the mechanism is unchanged, only trajectories moved).

---

## 2026-07-27 — Defect-fix re-baseline: exploitation contagion and the give-up rule

**Spec-IDs:** ATK-04 (counts moved), ATK-05 (fixed), ATK-06/ATK-07 (fixed),
NET-13/NET-14 (unchanged semantics, changed outcomes).

**Why.** The S2 action-layer audit
(`docs/implementation/pipeline/ogasp/action_layer_audit.md`) found defects that the
freeze then barred it from fixing. The supervisor subsequently authorised fixing
verified bugs in the simulator — the freeze being on *adapting the attacker's
phases and verbs to the experiments*, not on repairing defects — and directed that
design intent be taken from Brown 2023. Seven fixes landed (commits `dd8c5ec`,
`53c5e5d`); this entry captures the goldens at the end of that series.

**The dominant driver is one bug.** `Service.copy()` returned a new `Service`
wrapping the **same `Vulnerability` objects**, and every host draws its services
through that method. 68 % of vulnerability instances were shared across hosts (up
to 12 hosts each), and `Vulnerability.exploited` is per-instance — so exploiting a
vulnerability on one host marked it exploited on every host carrying it, and
`Service.is_exploited()` (which sums exploited impact) then reported untouched
hosts' services as compromised. In the seeded no-MTD golden, **86 of 124 services
on hosts the adversary never ran a single exploit against already read as
exploited**. Compromise was substantially free. Each host now owns its
vulnerability instances; the `id` is preserved (hosts genuinely may carry the same
vulnerability), and no RNG is consumed, so generated networks are structurally
identical for a given seed.

**What this did to the numbers.** Attack counts roughly doubled — the attacker now
has to earn every compromise — and, far more importantly, **the MTD techniques
started discriminating**. Before, seven of the nine goldens ended at exactly 41
compromised hosts, the 0.8 termination ratio, *regardless of which defence was
deployed*: contagion handed the attacker the network faster than any MTD could
take it away. The defence signal was being swamped by a bug.

| scenario | attacks | MTDs | compromised |
|---|---|---|---|
| no-mtd | 692 → 1541 | 0 → 0 | 41 → **41** |
| no-mtd_seed1234_repeat | 692 → 1541 | 0 → 0 | 41 → **41** |
| no-mtd_seed9999 | 771 → 1698 | 0 → 0 | 41 → **39** |
| single-ipshuffle | 1228 → 1511 | 75 → 75 | 35 → **32** |
| single-osdiversity | 964 → 1927 | 45 → 75 | 41 → **2** |
| random-multi | 875 → 1605 | 42 → 75 | 41 → **13** |
| alternative-multi | 871 → 1687 | 40 → 75 | 41 → **11** |
| simultaneous-multi | 765 → 1570 | 44 → 88 | 41 → **22** |
| primary-random-15k (100 nodes) | 1366 → 1698 | 65 → 75 | 81 → **6** |

The no-MTD control is unchanged at 41 (the attacker still takes the network when
undefended, it just takes ~2.2x the actions), which is the reassurance that the
spread across the MTD rows is defensive effect and not a broken attacker.

**The other six fixes**, in decreasing order of effect on these numbers:

1. **The give-up rule was inverted against Brown** (B-ATK-06). The guard applied it
   only when `network_type == 0` — the targeted scenario, unreachable in this
   repository — so no host was ever given up and hosts were re-enumerated up to 50
   times against a stated bound of 10. Restored to Brown's polarity: give up after
   10 attempts, except on the target node of a targeted network.
2. **The give-up list leaked through `SCAN_NEIGHBOR`**, which re-queued blacklisted
   hosts.
3. **The movement arm paid no confusion penalty** (B-ATK-07) and never lost its host
   cursor on a network-layer mutation (B-INT-01). Does not affect these goldens —
   they are native-arm — but it is why the two arms were not comparable.
4. **`SCAN_HOST` queued duplicates**, inflating the per-host attempt counter.
5. **A compromise was stamped onto the previous verb's record row** when
   `EXPLOIT_VULN` had nothing to try (13.8 % of compromises under MTD, 0 % without).
6. **`attack_counter[-1]`** was read whenever the host cursor was -1.

**ATK-04 counts moved, and the movement is corroborating.** The pinned per-instance
re-exploit discount now fires on 0.6–9.8 % of `exploit_time` calls, down from
7.3–41.6 %. The mechanism is untouched: it was previously firing on vulnerabilities
that *contagion* had marked exploited, and now fires only on genuine re-attempts of
the same instance on the same host — which is what its docstring always claimed.
New pins in `tests/test_atk04_reexploit_discount.py`.

**Verification.** Behaviour was checked by stepping the discrete-event queue
event-by-event with the new `tools/des_step.py`, against Brown's stated rules:
B-INT-01 (network-layer mutation clears the host cursor, restart at discovery),
B-INT-02 (application-layer keeps the host, re-run the port scan), B-ATK-07 (the
penalty is paid on every block, ~20 t/u), B-ATK-06 (a host is given up at exactly
attempt 10), and no-contagion (every compromise is preceded by a verb run against
that host). Those checks are now tests (`tests/test_des_step.py`), and the tracer
is asserted non-perturbing. Full suite: **264 passed**.

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
mis-executed past sim_t≈6.5 ks (Phase-0 recon; see git log for the
since-retired `docs/findings/crash_6000s.md`). Numbers from those runs
reflect a sim where R1's hard-coded 0.25
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
