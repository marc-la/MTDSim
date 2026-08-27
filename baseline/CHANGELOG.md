# Baseline goldens — change log

Every intentional re-baseline lands here with what / why / spec-IDs. The
on-disk goldens are the behavioural oracle for the inherited substrate;
*any* change to their headline numbers must have an entry below or the
diff is a regression to chase, not a re-baseline to accept.

---

## 2026-08-27 (follow-up, same day) — OS-compatibility granularity ruled (name, version); OSD-bearing goldens re-captured

Marc ruled the agent's flagged decision: a service is compatible with an OS
version when that OS version carries the service at its **name and version**,
not by name alone (`services.py:service_is_compatible_with_os`). Re-captured:
`baseline/golden_movement` OSDiversity / OSDiversityAssignment streams (18) and
`baseline/golden` `single-osdiversity`, `random-multi`, `alternative-multi`,
`simultaneous-multi`, `primary-random-15k`. Full suite 899 passed after the
re-capture, with the ATK-04 (calls, fires) pins unchanged — the stricter test
moved no pinned headline at these seeds. Also confirmed by Marc: a refused
attempt feeds the native per-host give-up threshold (as implemented).

---

## 2026-08-27 — OS Diversity made a distinct mechanism: the OS-gated exploit channel reinstated (D-19) and the inert compatibility guard repaired (D-18); every golden re-baselined, both arms

**Ruling (Marc, 2026-08-27, "option 1").** OS Diversity becomes a faithful,
distinct mechanism through two changes, both under the D-05 procedure
(deliberate re-baseline, this entry, SIM-05):

- **(A) The OS-gated exploit success channel is on** —
  `Vulnerability.network` (`mtdnetwork/component/services.py`) now refuses an
  OS-dependent vulnerability on a host whose `os_type` is outside its
  `vuln_os_list`, returning 0.0 before any roll. This closes **D-19** as
  documented-intent-unimplemented: Brown 2023 §III-B(6) states OS Diversity
  "changes the OS on the device, avoiding any OS-specific exploits"
  (`docs/sources/lit_review/brown2023.md:97`); the gate was inherited
  commented-out. Design decision ruled on recommendation: a refused attempt
  **counts as a failed attempt** (`exploit_attempt += 1`), so a host whose
  vulnerabilities are all OS-gated cannot absorb attempts for free — but it
  **draws no randomness**, so a refusal shifts no downstream draw. The
  exploit-time ×2.5 mismatch term is untouched (native arm only; the movement
  arm still declines it via `charge_time=False`, S3-R).
- **(B) `service_is_compatible_with_os` repaired** — the inherited test
  compared a `Service` instance against the service-name strings keyed under
  the OS, and `Service.__eq__` rejects non-`Service` operands, so it was
  False in every reachable state and `OSDiversity` replaced every non-target
  service on every firing (**D-18**). Compatibility is now membership by
  service name (True for a service against its own OS/version, 600/600 live
  and pinned), so OS Diversity redraws **only the services the new OS cannot
  run** — measured 4 of 331 per firing at seed 42 (49/331 at seed 43) against
  ServiceDiversity's 331/331. Exposed-endpoint and target-node exemptions,
  version-index preservation and port immobility are unchanged.
  ServiceDiversity is untouched; OSDiversityAssignment (withdrawn, D-17 c)
  inherits the repaired helper and nothing else.

**Both arms are affected by design.** The gate sits at the one exploit call
site both attackers share (`attack_operation.py`, `vuln.network(...)`), and
vulnerabilities carry OS dependencies from generation
(`VULN_PROB_DEPENDS_ON_OS` = 0.8 on cross-platform services), so **every**
scenario moves — the no-MTD controls included — not only those with OS
Diversity in the pool. The OS relabel now reaches the attacker through
exploit success as well as the ×2.5 time term.

**Native goldens (`baseline/golden`, 9/9 moved; seed 1234, 15 ks unless
noted), attacks · MTDs · HCR old → new:**

| scenario | old | new |
|---|---|---|
| `no-mtd` (+ `_seed1234_repeat`) | 1494 · 0 · 0.82 | 1676 · 0 · 0.68 |
| `no-mtd_seed9999` | 1688 · 0 · 0.82 | 1684 · 0 · 0.76 |
| `single-ipshuffle` | 1584 · 75 · 0.64 | 1315 · 75 · 0.18 |
| `single-osdiversity` | 2023 · 75 · 0.06 | 1456 · 75 · 0.38 |
| `random-multi` | 1829 · 75 · 0.32 | 1708 · 75 · 0.22 |
| `alternative-multi` | 1814 · 75 · 0.20 | 1771 · 75 · 0.18 |
| `simultaneous-multi` (int. 700) | 1704 · 88 · 0.54 | 1639 · 88 · 0.46 |
| `primary-random-15k` (100n, seed 42) | 1801 · 75 · 0.06 | 1833 · 75 · 0.08 |

Re-captured with `baseline/run_baseline.py` per scenario (`--finish-time
15000`; `primary-random-15k` = `random-multi --seed 42 --total-nodes 100`).
Pins moved with them: the seed-1234 no-MTD headline (1494/41 → 1676/34) in
`tests/test_action_layer_carve.py` G1, `tests/test_action_layer_dispositions.py`
(ATK-08 cap still inert; the run now ends at the horizon on 34, not at the
objective), `tests/l3_simulation/test_movement_integration.py` and
`tests/l3_simulation/test_movement_smoke.py`; and the nine
`tests/test_atk04_reexploit_discount.py` (calls, discount_fires) pairs.

**Movement goldens (`baseline/golden_movement`, 69/69 moved), summed over
each mechanism's streams, old → new:**

| mechanism (streams) | compromised | interrupts | mtd_executions |
|---|---|---|---|
| no-mtd (9) | 67 → 58 | 0 → 0 | 0 → 0 |
| IPShuffle (9) | 4 → 4 | 675 → 675 | 675 → 675 |
| OSDiversity (6) | 24 → 33 | 341 → 336 | 450 → 450 |
| ServiceDiversity (9) | 47 → 36 | 526 → 523 | 675 → 675 |
| OSDiversityAssignment (9, withdrawn oracle) | 42 → 60 | 527 → 516 | 675 → 675 |
| PortShuffle (6) | 31 → 32 | 331 → 341 | 450 → 450 |
| UserShuffle (9) | 71 → 56 | 3 → 3 | 675 → 675 |
| HostTopologyShuffle (6) | 2 → 1 | 450 → 450 | 450 → 450 |
| CompleteTopologyShuffle (6) | 2 → 2 | 450 → 450 | 450 → 450 |

`mtd_executions` is unchanged everywhere (the scheduler is untouched); the
moves are in exploit outcomes and the walk they drive. Re-captured with
`PYTHONPATH=src python tools/mtd_golden_streams.py capture`.

**Tracer.** Both tracers now narrate `EXPLOIT REFUSED` (ATTACKER) with the
vulnerability's OS list against the host's OS, tally
`exploits_refused_by_os` in the verdict, and report a diversity firing's
service writes as a fraction of the internal pool (`4/331 internal
service(s) redrawn`). Substrate arm, seed 42, 3000 t/u: OSDiversity 2/50
owned, 15 interrupts, 161 refused; ServiceDiversity 5/50, 13, 98.
Movement arm (`aggregate`, `v2_partial`, seed 0, 4000 t/u): 1/50 owned and
16 interrupts under both, 108 vs 110 refused — the two mechanisms now
separate on the native arm; on the movement arm at this seed/horizon the
walk does not get past its foothold under either, so the separation must be
read off the goldens above (OSDiversity 24 → 33 vs ServiceDiversity 47 →
36), not this single trace.

**Spec-IDs / audit-IDs:** IS-MTD-06 (now conforms), D-18 (repaired), D-19
(closed: documented-intent-unimplemented → implemented), SIM-05.

## 2026-08-27 — MTD pool restoration: all 69 movement goldens re-captured; 55 schema-only, 14 behavioural under ruled repairs

**Schema drift (55 streams, not a re-baseline).** Commit `ca6cd72c`
(crown-jewel reach, 2026-08-20) added `database_held` to every
`MovementRecord` and `database_hosts_reached` / `first_database_reach_time`
to the run summary. The serialiser writes every dataclass field, so every
digest moved while every behavioural field stayed byte-identical — verified
by stripping the three keys and comparing all 69 documents against `HEAD`.
Root-caused by bisection over the 97 commits since the 2026-08-17 capture.

**Behavioural moves (14 streams), each under a ruling of 2026-08-27
(`docs/handoffs/2026-08-27_mtd_pool_restoration.md`):**

- `UserShuffle_*` (9): **D-32** repaired (`set_host_users` recomputes
  `total_users` / `p_u_compromise` per call) and **R2** applied (exposed
  endpoints exempt, graph-keyed, family rule D-23). R1 keeps the same-pool
  redraw.
- `HostTopologyShuffle_seed0_overlay` (1): **D-31** repaired — in-place
  remap keeps the `network.compromised_hosts` alias; `reachable` rebuilt
  from the moved set; ip-feed refreshed. The other five HTS streams were
  bit-identical, i.e. no swap in them touched a foothold.
- `OSDiversity_seed1_observed`, `ServiceDiversity_seed1_observed`,
  `no-mtd_seed1_overlay_retrace`, `no-mtd_seed2_overlay` (4): **D-26**
  repaired (`total_users = len(users)`, the brute-force divisor) — moves
  only streams in which BRUTE_FORCE rolled against a host whose count was
  wrong.

**Headline counts unchanged in all 69** (`compromised`, `interrupts`,
`mtd_executions`, `retraces` equal old vs new); the behavioural moves are
in-record draws, not outcomes — consistent with D-26's measured near-nil
effect (1 brute-force compromise in 488 calls).

Withdrawn by ruling D-17(c) the same day: OSDiversityAssignment stays in the
golden set as a regression oracle for code that remains in the tree, but is
in no pool. New named pools: `lineage` (default, the four) and `full`
(Brown's seven); the goldens run `single`, so the pool change moves nothing.

---

## 2026-08-06 — GASP class rename: the 15 retrace goldens re-captured, label-only; **not** a re-baseline

**What changed and why.** The four GASP class labels were renamed to
objective-tactic labels (`pure_steal` → `objective_exfiltration`,
`pure_impediment` → `objective_impact`, `double_extortion` →
`objective_exfiltration_impact`, `infrastructure_setup` →
`objective_none_c2`). `RETRACE_PROFILE` in `tools/mtd_golden_streams.py` names
one of them, so the 15 `*_retrace` configurations carry the new string in their
`movement_records[].profile` field and had to be re-captured.

**Why this is not a re-baseline.** The re-captured streams are byte-identical to
the committed ones once the profile label is substituted — verified
field-for-field across all 15, with zero differences beyond the label. The
manifest's only changes are the 15 `sha256` digests; **every behavioural field —
`compromised`, `interrupts`, `mtd_executions`, `retraces` — is unchanged**. The
other 55 golden configurations were not rewritten at all: they run under
`PROFILE = "aggregate"`, whose name did not move. No headline number changed, so
this entry records a relabelling, not an accepted behavioural diff.

**Not to be confused with the timeline re-seed.** The *timeline* library genuinely
did move numbers under the same rename, because its seeds are content-addressed
on a `run_id` that embeds the profile name. That is recorded separately in
`data/ogasp/timeline/timeline_schema.md` § *Re-seeded by the 2026-08-06 rename*.
The goldens here are unaffected by that mechanism — their seeds are passed
explicitly.

**Spec-IDs / audit-IDs:** none. Vocabulary refactor only; membership, weights and
walk semantics untouched.

---

## 2026-08-03 — D-28: ENUM_HOST enforces IS-PRC-01's visibility invariant; movement goldens re-baselined, native goldens untouched

**What changed and why.** `_do_enum_host` popped and attacked whatever sat at the
head of `_host_stack`, whether or not a path to it still existed.
`sort_by_distance_from_exposed_and_pivot_host` only *sorts* — an unreachable host
scores `LARGE_INT` and sorts last, but was never dropped — so IS-PRC-01's "visible
**only if a path exists** through a compromised or exposed internal host" was
enforced by control flow rather than by a guard: the native FSM's forced
post-interrupt `_scan_host()` rebuilt the queue and flushed stale entries. A
driving layer that owns its own succession does not re-scan, so the movement
attacker went on attacking hosts a topology shuffle had just disconnected —
**9.7 % of ENUM_HOST pops undefended and 22.4 % under MTD** (10 seeds each),
against **0 of 873** on the native arm. Ruled a fix by Marc (2026-08-03: faithful
Complete Topology Shuffle is a given). Evidence:
`docs/implementation/attacker_read_surface.md` §(f) finding 5.

The guard lives in the **shared verb core** (`AttackOperation.visible_host_stack`,
applied in `_do_enum_host`, and asserted by both `_enum_host`'s raise and
`assert_action_context`), so both driving arms inherit it with no
controller-mapping change; a driven caller reads it through its existing
`PRECONDITION_UNMET` path. An all-unreachable queue routes to host discovery,
which is Brown Fig 3 box 10 → box 1.

**What moved.** `baseline/golden_movement/`: **67 of 69** configurations
re-captured (`IPShuffle_seed2_overlay_retrace` and `UserShuffle_seed0_overlay_retrace`
were already bit-identical). `baseline/golden/` — the nine native scenarios — is
**untouched and verified bit-identical**, which is the re-baseline's own
confirmation of the diagnosis: the native arm never exhibited the defect, so its
oracle must not move, and it did not (`tests/test_action_layer_carve.py` G1, 1494
attack events / 41 compromised on seed 1234, passes unchanged).

**Determinism (SIM-05) re-verified** on both arms after the change: movement arm
seed 3 record-for-record identical across repeat runs; native arm seed 1234 event
stream identical (226 events). Full suite green; no `--no-verify`.

**New regression test:** `tests/test_enum_host_visibility.py` — nine cases pinning
the assertion whose absence let this survive (ENUM_HOST never sets `curr_host`
outside the hacker-visible graph, asserted over whole runs of **both** arms
defended and undefended), plus the precondition, the native re-route, and the
filter's read-only/inert properties.

**Measured consequence for the evaluation** (new comparative arm, 10 seeds,
movement arm — not a re-run of any recorded experiment): the guard leaves the
position-destroying mechanisms essentially unchanged (Complete Topology Shuffle
0.90 → 0.80 hosts, IP Shuffle 0.80 → 0.80) and **weakens the diversity
mechanisms** (OS Diversity 3.10 → 4.70, Service Diversity 3.60 → 4.30), because a
dropped target redirects the attacker rather than stopping it. The family-level
contrast therefore *widens* (≈40 points to ≈65). Note this **falsifies the
direction predicted before the measurement** — the prediction was that the
topology mechanisms would strengthen; they did not move, and the diversity
mechanisms weakened instead.

**Spec-IDs / audit-IDs:** IS-PRC-01 (split by arm — CONFORMS native,
DIVERGES-DOCUMENTED-NOWHERE movement; → D-28, fixed).

---

## 2026-08-01 — Schema follows the input: legacy movement goldens restored to their original bytes; retrace golden set added

**What changed and why.** The reconciliation merges added the S5 sink-retrace
flag to `MovementRecord`, and the 2026-08-01 recapture (`fda79db`) re-baselined
all 54 movement goldens for a field that no legacy run ever sets — a schema
change tripping a behaviour net. Ruled instead (Marc): **a golden document's
schema is a function of the run's declared inputs.** `one_golden_run` now takes
`retrace_sinks` (and a profile) as declared inputs; a run that does not name the
retrace input serialises in the pre-retrace record shape. Under that rule the
**original** goldens (as first captured 2026-07-29) pass unmodified, so this
entry *restores* their bytes rather than re-baselining them — behaviour never
moved, and the recapture is retired as unnecessary.

**What's new.** Fifteen `*_retrace` configurations: `retrace_sinks=True` on
`objective_exfiltration_impact` (the aggregate profile has no sinks, so the
policy would be inert there), no-MTD + one mechanism per resource class + the stateful
mechanism, seeds 0–2, overlay arm. Every config records 3–8 retraces
(`manifest.json` carries the count), so the set genuinely exercises the policy.
The suite subset gains three retrace cases and a schema-rule test pinning both
shapes.

**Spec-IDs / audit-IDs:** IS-MTD-08 (revised → D-17, awaiting ruling),
intent_conformance_audit §l item 10 (re-instantiation seam, fixed).

**What's new.** `baseline/golden_movement/` — per-mechanism behaviour streams for
the movement arm (all eight techniques + no-MTD × seeds 0–2 × both overlay arms),
captured and checked by `tools/mtd_golden_streams.py` under the cost-bench
configuration (aggregate / v2_partial / 15 000 s / single / 200 s). A subset runs
in the suite (`tests/test_mtd_golden_streams.py`). These are the
behaviour-preservation gate for the MTD mechanism cost audit: any defender-side
performance change must leave them field-for-field identical.

**One intentional re-baseline.** `MTDScheme._mtd_register` constructed a fresh
instance per registration, resetting `OSDiversityAssignment`'s checkpoint cache
every cycle — 75 MIP solves per run where its design intends ≤ 8 (~128 s/run).
Fixed with a per-scheme instance cache. The seven stateless mechanisms and no-MTD
were verified **bit-identical** across all 48 configs before/after the fix; the six
OSDiversityAssignment configs moved (first divergences are mid-run exploit-outcome
flips — the assignment applied between checkpoints is now the cached solve rather
than a fresh per-mutation one) and were re-captured at ~2.3 s/run, ~50× cheaper.
The native-arm goldens under `baseline/golden/` are untouched (no default-pool
scenario registers a stateful mechanism).

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
