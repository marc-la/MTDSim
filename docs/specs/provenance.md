# Provenance map — load-bearing constants and rules → source → code → disposition

A single cross-link table. For each non-obvious design choice in the
codebase, this names the source (with locator), the file:symbol it lives
at, and the spec disposition. The in-code anchor comments at the listed
file locations point back here and to [`mtdsim_spec.md`](mtdsim_spec.md) /
[`metrics_semantics.md`](metrics_semantics.md).

**Scope.** Entries are restricted to "things a reader would otherwise
wonder where they came from" — i.e. load-bearing values and rules that
have a citeable paper or spec-row source. Obvious or inherited-without-
paper values are not listed.

**Verification.** Every row's source column is taken verbatim from an
existing verified doc in this repo
([`mtdsim_spec.md`](mtdsim_spec.md),
[`../extractions/`](../extractions/),
[`metrics_semantics.md`](metrics_semantics.md),
[`../../baseline/CHANGELOG.md`](../../baseline/CHANGELOG.md)). No source has
been backfilled from outside those.

---

| Concept | Source + locator | Code location (file:symbol) | Disposition |
|---|---|---|---|
| **Network Compromise Ratio (NCR) termination threshold** = 0.8 | Zhang 2023 §5 (NCR terminating condition) | [`mtdnetwork/component/time_network.py`](../../mtdnetwork/component/time_network.py): `TimeNetwork.__init__` default `terminate_compromise_ratio=0.8`; rule applied in `is_compromised` | **faithful** (fixed Phase 2b R1; see mtdsim_spec.md MET-15 / C6) |
| **MTD execution durations** (mean, std) per technique | Zhang 2023 Table 3 (MTD execution time) | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `MTD_DURATION` dict | **faithful** (re-aligned Phase 2c MTD-14; CompleteTopologyShuffle 120→110, IPShuffle 110→100) |
| **MTD trigger interval** = Exponential(µ) per scheme | Zhang 2023 §4.3.4 | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `MTD_TRIGGER_INTERVAL`; sampled via `time_generator.exponential_variates` from [`mtdnetwork/operation/mtd_operation.py`](../../mtdnetwork/operation/mtd_operation.py) | **diverged** from Brown's Uniform(1000, 5000) ms (Brown §IV) — superseded by Zhang's exponential (see mtdsim_spec.md MTD-10 / MTD-11) |
| **Host Compromise Ratio (HCR)** = C_t / T_host | Ho 2024 §3.3.2 (#4) | [`mtdnetwork/statistic/evaluation.py`](../../mtdnetwork/statistic/evaluation.py): `evaluation_result_by_compromise_checkpoint`, `host_comp_ratio = self.compromised_num(record=sub_record) / host_num` | **faithful** (fixed Phase 2c C8 / MET-04; HCR ∈ [0, 1] regression-tested) |
| **Internal MTTC** = mean duration over `SCAN_PORT`, `EXPLOIT_VULN`, `BRUTE_FORCE` rows up to compromise checkpoint | Zhang 2023 §3.4; Ho 2024 §3.3.2 (#8) | [`mtdnetwork/statistic/evaluation.py`](../../mtdnetwork/statistic/evaluation.py): `evaluation_result_by_compromise_checkpoint`, `time_to_compromise = attack_duration_series.sum() / attack_action_count` | **faithful (computation)**; magnitude shifted by C7 + ATK-04 (cross-paper numeric comparison invalid — see metrics_semantics.md §d) |
| **Service-compromise threshold** = 7 (against Σ exploited impact in [0, 10]) | README; not in any source paper at this granularity | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `SERVICE_COMPROMISED_THRESHOLD = 7`; used in [`mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py): `Service.is_exploited` | **faithful** (inherited; threshold and impact range jointly documented, see mtdsim_spec.md NET-14 / C3) |
| **Vuln impact range** = [0, 10] | code (inherited); cf. Brown 2023 Table I [0, 1] | [`mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py): `Vulnerability.__init__`, `self.impact = random.random() * 10` | **diverged** from Brown paper [0, 1]; docs aligned Phase 2c — delta inherited not actioned (would also require recalibrating threshold of 7); see mtdsim_spec.md NET-13 / C3 |
| **Vuln attack complexity range** = [0.4, 1] | Brown 2023 Table I (Brown matches code); cf. Zhang §4.4.3 [0, 1] | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `VULN_MIN_COMPLEXITY = 0.4`; [`mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py): `Vulnerability.__init__` | **faithful (Brown)**; Zhang paper-side wording differs — see mtdsim_spec.md NET-12 / C2 |
| **Per-host attack-attempt limit (give-up rule)** = 10 | Brown 2023 §III-C(2), Table I (=10); §V-C ("never give up on target node in Scenario 2") | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `ATTACKER_THRESHOLD = 10`; applied in [`mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py): `_execute_enum_host` (`_attack_counter == _attack_threshold` ⇒ push to `stop_attack`, unless target host under `network_type==0`) | **faithful**; see mtdsim_spec.md ATK-07 |
| **Global attack-attempt cap** = `5 × total_nodes` | inherited (Brown-era heuristic, not in any paper) | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `HACKER_ATTACK_ATTEMPT_MULTIPLER = 5`; computed in [`mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py): `Adversary.__init__._max_attack_attempts` | **diverged (inert)** — counter is incremented but the guard is commented out (`attack_operation.py:220`); see mtdsim_spec.md ATK-08 |
| **Exploit-time model** — deterministic `ATTACK_DURATION['EXPLOIT_VULN'] * (1 - complexity)` (×2.5 on OS-mismatch; ÷2 on already-exploited *instance*) | (code reality differs from paper) | [`mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py): `Vulnerability.exploit_time` | **diverged (C7 / ATK-03)** — Zhang 2023 §4.4.3 Eq 1-2 specifies an exponential `T_Aexploit` parameterised by `V_exploited`/`V_unexploited`/`ACv`; deterministic form retained as inherited reality, shifts absolute MTTC magnitude (see metrics_semantics.md §c) |
| **Re-exploit time discount — per-instance (active)** | Brown 2021 (commit `a16db997`, 2021-09-04); not in any source paper | [`mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py): `Vulnerability.exploit_time`, `if self.exploited: return exp_time / 2` (lines 90-91) | **active inherited mechanism** — halves the exploit-time cost when re-attempting the *same `Vulnerability` instance*. Brown-era, pre-Zhang. Fires in 7–42 % of `exploit_time` calls across the 9 goldens (pinned by `tests/test_atk04_reexploit_discount.py`). Kept deliberately (Unit C disposition). See metrics_semantics.md §c / mtdsim_spec.md ATK-04. |
| **Attacker learning — per-type (missing)** | Zhang 2023 §4.4.3 | [`mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py): `Vulnerability.exploit_time` — trace at the commented-out `exploit_attempt + 1` line (lines 97-98) | **diverged (ATK-04, missing)** — Zhang's per-vuln-TYPE halving (the cross-instance learning rule) is unimplemented; only the commented-out trace remains. Distinct mechanism from the per-instance discount above. See metrics_semantics.md §c / mtdsim_spec.md ATK-04. |
| **Attack-action enums** (metrics-relevant) = `SCAN_PORT`, `EXPLOIT_VULN`, `BRUTE_FORCE` | Ho 2024 §3.3.2 (MTTC + ASR + Attack Stage) | Used in [`mtdnetwork/statistic/evaluation.py`](../../mtdnetwork/statistic/evaluation.py): `evaluation_result_by_compromise_checkpoint` `name.isin(['SCAN_PORT', 'EXPLOIT_VULN', 'BRUTE_FORCE'])` | **faithful**; see mtdsim_spec.md ATK-13 |
| **Three-phase action timing** (Phase 1 SCAN_PORT + cred stuff; Phase 2 EXPLOIT_VULN; Phase 3 BRUTE_FORCE) | Zhang 2023 §4.4.2, §4.4.3 | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `ATTACK_DURATION` dict; phase rotation in [`mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py) | **faithful (timing constants)**; Phase-2 distribution diverged per C7 above |
| **MTD interrupt + confusion penalty** = `ATTACK_DURATION['PENALTY']` = 20 | Brown 2023 §V-A; Zhang 2023 §4.4.3 | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `ATTACK_DURATION['PENALTY'] = 20`; applied in [`mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py): `_handle_interrupt` flow | **faithful**; see mtdsim_spec.md ATK-05 |
| **Cross-platform vuln chance** = 0.5 | Brown 2023 Table I; restated Zhang §4.2.3 ("half") | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `VULN_PERCENT_CROSS_PLATFORM = 0.5` | **faithful**; see mtdsim_spec.md NET-11 |
| **Patched-version mean / range** = 10 / 9 | Brown 2023 §III-A | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `VULN_PATCH_MEAN = 10`, `VULN_PATCH_RANGE = 9` | **faithful**; see mtdsim_spec.md NET-10 |
| **Services per host** ∈ [3, 11] | Brown 2023 Table I | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `HOST_SERVICES_MIN = 3`, `HOST_SERVICES_MAX = 11` | **faithful**; see mtdsim_spec.md NET-06 |
| **Users per host** = 5; **password-reuse chance** = 0.05 | Brown 2023 §III-B(3); Zhang 2023 §4.2.2 | [`mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py): `USER_TOTAL_FOR_EACH_HOST = 5`, `USER_PROB_TO_REUSE_PASS = 0.05` | **faithful**; see mtdsim_spec.md NET-07 |

---

## Flags — claims worth re-dispositioning

These are observations made during the provenance pass that don't have a
clean disposition in the verified docs and need Marc's call.

- ~~**ATK-04 active code at `services.py:84-85`**~~ — **resolved in Unit C**.
  Both mechanisms now have rows above (per-instance Brown-era discount =
  active and kept; per-type Zhang learning = unimplemented), and the
  in-code anchor comment at `services.py:80-99` and the doc sections at
  [`metrics_semantics.md`](metrics_semantics.md) §c and
  [`mtdsim_spec.md`](mtdsim_spec.md) ATK-04 have been disambiguated.
  Discount-fire counts are pinned across the 9 goldens by
  [`tests/test_atk04_reexploit_discount.py`](../../tests/test_atk04_reexploit_discount.py).

- **Out of this pass's scope (not actioned, just noted)** — every other
  `divergent` / `missing` row in [`mtdsim_spec.md`](mtdsim_spec.md) is
  already named in the spec's "Biggest faithfulness risks" §; this
  document does not duplicate them. The two C8 / MET-04 and MTD-14 fixes
  are reflected here as `faithful` because they are post-2c reality.
