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
| **L3 transition-weight regime** — tactic-pair transition weight = out-edge-normalised **flow proportion** (proportion of attack flows leaving the source tactic along that pair); technique-level `observation_count` stays recorded, un-normalised | Supervisor decision D3 (Jin Hong working session, July 2026; register at [`../notes/2026-07-03_supervisor_meeting_l3_decisions.md`](../notes/2026-07-03_supervisor_meeting_l3_decisions.md)); operative disposition in [`metrics_semantics.md`](metrics_semantics.md) §(f) | [`src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri/) (build); shipped as the weight layer of [`data/ogasp/*_structural.json`](../../data/ogasp/README.md) (two corpus variants: `operator_dedup` n = 29 primary, `raw` n = 38); gate in [`tests/l3_simulation/test_weights.py`](../../tests/l3_simulation/test_weights.py) | **dispositioned, built** — the closed-world assumption and survivorship framing of metrics_semantics.md §(f) are mandatory wherever a weight is cited |
| **L3 per-tactic state-duration regime** — tiered sourcing: (1) substrate verbs (`ATTACK_DURATION`) where a tactic maps onto them, (2) literature timing values where they exist, (3) reasonable **justified estimate** otherwise (e.g. stealth); every value carries provenance + a sweep range | Supervisor decision D4 (same session; no ready-made MITRE-tactic→time resource exists — defined here, with justifications); method + tier bar in [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md); evidence layer in [`../tactic_profiles/`](../tactic_profiles/) §5 | [`data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json) (v0 uncalibrated); gate in [`tests/l3_simulation/test_durations.py`](../../tests/l3_simulation/test_durations.py) (key set = place-union; corpus-frequency guard; anchor arithmetic; magnitude sanity) | **dispositioned, built (v0 uncalibrated)** — plain per-state dwell consumed by the standalone runner, *not* a stochastic firing rate (timed-net semantics deferred per D10); tuned anchors calibrate within their sweep ranges once the runner lands, then freeze v1. **Per-tactic rows below await Marc's approval.** |

---

## L3 state-duration catalogue — per-tactic rows (**pending Marc's approval**)

The row-level detail behind the D4 regime row above. Values are the
`v0-uncalibrated` catalogue ([`data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json));
each traces to its profile's §5 block (the single source of truth) and must
stay consistent with dissertation.tex §3.1 Tables 3.1–3.2. Units: simulated
seconds (the `env.timeout` clock). `duration_s` = multiplier × group anchor.
Anchors: **scan-shaped** 35 s (`ATTACK_DURATION` `SCAN_HOST` 5 + `SCAN_NEIGHBOR` 5
+ `SCAN_PORT` 25 — one enumeration pass; Tier 1, not tuned); **exploit-shaped**
4.5 s (median `exploit_time` = `EXPLOIT_VULN` 15 × (1 − complexity), complexity
~ U[0.4, 1]; Tier 1, not tuned); **stealth-low-and-slow** 45 s (declared v0:
10 × exploit median — an order of magnitude above the priced verbs, below the
200 s MTD trigger-interval mean; Tier 3); **objective-execution** 36 s (declared
v0: 8 × exploit median; Tier 2, calibratable against Bromiley/Sophos/ransomware-IR
milestones); **prep-off-network** 0 s. The §3 reset verdicts are a separate
declared parameter for the L3b binding — deliberately not in this catalogue.

| Tactic | Group | × | `duration_s` | Tier | Sweep (× anchor) | Source |
|---|---|--:|--:|:--:|---|---|
| `reconnaissance` | scan-shaped | 1.0 | 35.0 | 1 | 0.5–2 | `ATTACK_DURATION` scan verbs; [01 §5](../tactic_profiles/01_reconnaissance.md) |
| `resource-development` | prep-off-network | 0 | 0.0 | 3 | degenerate (0) | declared off-clock; [02 §5](../tactic_profiles/02_resource-development.md) |
| `initial-access` | exploit-shaped | 1.0 | 4.5 | 1 | 0.5–2 | `exploit_time`; [03 §5](../tactic_profiles/03_initial-access.md) |
| `execution` | stealth-low-and-slow | 0.5 | 22.5 | 3 | 0.1–2 | declared (group unsettled); [04 §5](../tactic_profiles/04_execution.md) |
| `persistence` | stealth-low-and-slow | 1.0 | 45.0 | 3 | 0.25–4 | declared; [05 §5](../tactic_profiles/05_persistence.md) |
| `privilege-escalation` | exploit-shaped | 1.0 | 4.5 | 1 | 0.5–2 | `exploit_time`; [06 §5](../tactic_profiles/06_privilege-escalation.md) |
| `stealth` | stealth-low-and-slow | 1.0 | 45.0 | 3 | 0.25–4 | declared (group reference); [07 §5](../tactic_profiles/07_stealth.md) |
| `defense-impairment` | stealth-low-and-slow | 0.5 | 22.5 | 3 | 0.1–4 (widest) | declared (group unresolved); [08 §5](../tactic_profiles/08_defense-impairment.md) |
| `credential-access` | exploit-shaped | 1.0 | 4.5 | 1 | 0.5–2 | `exploit_time` (dumping path); [09 §5](../tactic_profiles/09_credential-access.md) |
| `discovery` | scan-shaped | 1.0 | 35.0 | 1 | 0.5–2 | `ATTACK_DURATION` scan verbs; [10 §5](../tactic_profiles/10_discovery.md) |
| `lateral-movement` | exploit-shaped | 1.0 | 4.5 | 1 | 0.25–4 (wide) | `exploit_time`; [11 §5](../tactic_profiles/11_lateral-movement.md) |
| `collection` | objective-execution | 1.0 | 36.0 | 2 | 0.5–2 | [`collection_exfil_timing`](../extractions/collection_exfil_timing.md); [12 §5](../tactic_profiles/12_collection.md) |
| `command-and-control` | stealth-low-and-slow | 1.0 | 45.0 | 3 | 0.25–4 | declared (un-priceable by CVE data); [13 §5](../tactic_profiles/13_command-and-control.md) |
| `exfiltration` | objective-execution | 1.0 | 36.0 | 2 | 0.25–4 | [`breach_reports_macro_timing`](../extractions/breach_reports_macro_timing.md) (held-out milestone); [14 §5](../tactic_profiles/14_exfiltration.md) |
| `impact` | objective-execution | 1.0 | 36.0 | 2 | 0.1–5 (widest) | [`ransomware_timing`](../extractions/ransomware_timing.md); [15 §5](../tactic_profiles/15_impact.md) |

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
