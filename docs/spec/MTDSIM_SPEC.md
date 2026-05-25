# MTDSim Conformance Spec

**Status:** Phase-1 merge of the four source works against the Phase-0 baseline.
**Lineage:** Brown 2023 (foundational) → Zhang 2023 (MTDSimTime, time domain) → Ho 2024 (metrics + RL) → Tay 2024 (MTDShield).
**Primary source:** Brown 2023. **Direction-only source:** `LIT_REVIEW.md` (not an artefact source).
**Baseline:** `baseline/BASELINE.md` and `baseline/golden/*`, commit `chore/baseline-spec`.

---

## How to read this file

1. Each artefact has a stable **ID** (`NET-XX`, `ATK-XX`, `MTD-XX`, `SHD-XX`, `MET-XX`, `SIM-XX`, `CFG-XX`) and a **Disposition** against the running baseline:
   - `verified` — paper claim observed in the code (or in the golden outputs).
   - `divergent` — code and paper disagree on a specific value or rule. Both recorded.
   - `missing` — paper artefact has no code counterpart.
   - `out-of-scope` — known not to exist in this baseline by design (e.g. Tay's reactive plugin in a non-MTDShield run).
   - `unverified` — could not be checked without running additional scenarios not in the baseline.
2. **Lineage** column reads as `introduced by / modified by` — overlap is evolution, not contradiction.
3. **Relevance tags**: `[CORE]` faithful baseline behaviour · `[ATK-SWAP]` load-bearing for replacing the attacker with CTI-grounded profiles · `[IDS-SEAM]` load-bearing for an IDS/detection signal feeding the MTD agent · `[PERIPH]` peripheral.
4. **Test? column** = candidate for a golden-master / faithfulness test (Y/N).
5. Per-paper extraction notes live in `_notes_brown.md`, `_notes_zhang.md`, `_notes_ho.md`, `_notes_tay.md` and are the source of truth for paper-side locators.

---

## Provenance — what each work contributes

- **Brown 2023 — foundational MTDSim** (`docs/sources/brown2023.md`). Establishes the discrete-event simulator on a 3-layer HARM (Host / Service / Vulnerability — the *Network* is the container, not a layer; this resolves the surface of conflict C1). Defines the three modules (Network, Attacker, MTD), the Cyber-Kill-Chain-+-ATT&CK-inspired attacker procedure (Fig 3), six MTD techniques (IP / Port / User / Host-Topology shuffle + Service / OS diversity), two scenarios (general vs targeted), and the baseline parameter table (Table I). Reports two metrics: actions blocked, average attempts per compromise.
- **Zhang 2023 — MTDSimTime (time domain)** (`docs/sources/zhang2023.md`). Refactors Brown into a SimPy-based discrete-event time simulator. Introduces MTTC as the headline metric, three MTD **execution schemes** (random / alternative / simultaneous), the three-phase attack-action model (`SCAN_PORT` + cred stuff / `EXPLOIT_VULN` / `BRUTE_FORCE`), adversary-profile dimensions (objectives / vulns / C2 / user creds), exponential-distribution time models for both MTD interval and attack-action duration, an attacker-learning rule (halved exploit time for previously-exploited vulns) + confusion penalty, and a resource-occupation + suspension queue for the MTD scheduler. **Reduces** Brown's six techniques to four selected + DAP-optimised OS diversity. **Drops** Brown's targeted scenario from the experimental scope (still present in code).
- **Ho 2024 — security-metrics suite + DDQN selector** (`docs/sources/ho2024.md`). Catalogues 11 metrics (Table 3 + §3.3.2: APE, Risk, RoA, HCR, Attack Stage, ASR, MEF, MTTC, TSLM, SAPV, NAV) with explicit formulas. Builds a DDQN whose action space is single-MTD + pairwise combinations + Null. Introduces a **Static Degrade Factor** (default 2000 ms) that forces a random MTD trigger if the network has been static too long. Co-developed with Tay 2024.
- **Tay 2024 — MTDShield (reactive plugin)** (`docs/sources/tay2024.md`). Packages the joint DDQN model as a **plugin** that converts MTDSimTime from purely time-scheduled to reactive. Five-action set: `IPShuffle`, `OSDiversity`, `ServiceDiversity`, `CompleteTopologyShuffle`, **no-op**. Two-branch neural-net architecture (static features + time-series LSTM, feature fusion, Q-output). Defines an **attacker-detection-rate (IDS-sensitivity)** experiment with a measured **performance cutoff at ≈ 0.7**.

> **Correction to the seed scaffold:** the seed listed `SHD-07 = Federated training of the selection policy` attributed to Tay §4. Tay 2024 cites Kreischer 2023 [21] as related literature only; the methodology / model / evaluation sections never mention federated training. Removed from this revision.

---

## Conflicts to disposition (resolve with Marc — do not auto-reconcile)

| # | Conflict | Sources | Phase-0 evidence | Status |
|---|---|---|---|---|
| **C1** | "Layers" = 3 vs 5 | README & Brown §III-A say *3-layer* HARM (representation: Host/Service/Vulnerability); Brown Table I lists *No. of layers = 5* (network depth) | Code uses both: `total_layers` is the topology depth (default 4 in `time_network.py:10`); the 3-layer HARM is the *modelling* concept | **Two different concepts**, not a contradiction. Recommend folding into the spec as separate IDs rather than as a conflict. |
| **C2** | Attack-complexity range | Brown Table I & README: `[0.4, 1]`; Zhang §4.4.3: `ACv ∈ [0, 1]` | `constants.VULN_MIN_COMPLEXITY = 0.4` + `services.py:23` `self.complexity = VULN_MIN_COMPLEXITY + (1 − VULN_MIN_COMPLEXITY) * random()` → range **[0.4, 1]** in code | **Brown matches code; Zhang's `[0, 1]` is paper-side only.** Leave as `to verify` for Marc, but the code-side resolution is clear. |
| **C3** | Service-compromise threshold & impact range | README: vuln impact ∈ `[0,1]`, service compromised when Σ impacts > **7**; Brown Table I: impact `[0,1]` | `services.py:26` `self.impact = random.random() * 10` → impact ∈ **[0, 10]** in code; `SERVICE_COMPROMISED_THRESHOLD = 7` against that range. **README and Brown are wrong about the impact range.** | **Code-paper divergence.** With impact ∈ [0, 10], the threshold of 7 is sensible (≈ one near-max-impact vuln, or 2-3 medium ones). |
| **C4** | MTD technique set | Brown 6; Zhang's experimental set 4 + DAP; Tay's RL action set 5 (4 + no-op); Ho's includes pairwise combinations + Null | All 7 MTD classes exist in `mtdnetwork/mtd/`; `MTDScheme._mtd_strategies` default list contains 4 active (`CompleteTopologyShuffle, IPShuffle, OSDiversity, ServiceDiversity`); the other 3 (`PortShuffle`, `HostTopologyShuffle`, `UserShuffle`) and `OSDiversityAssignment` are **implemented but commented out of the default registration** | **Resolved.** Code carries Brown's full set; default scheme is Zhang's subset; Tay/Ho expose 4 + no-op to the agent. |
| **C5** | Zero-day vs cross-platform | README: "version 99" zero-day **always** assigned; Brown Table I: vuln cross-platform = 0.5 | `services.py:392` comment `Adding Vuln at version 99 to ensure there is a vuln in every version` (zero-day rule); `constants.VULN_PERCENT_CROSS_PLATFORM = 0.5` (cross-platform rule). **Two independent rules**, not one. | **Not a real conflict.** Cross-platform = 0.5 says half of vulns are cross-OS; version-99 zero-day says every version-99 service gets a vuln. Both implemented. |
| **C6 (new)** | Network-compromise termination ratio | Zhang §5: NCR = **0.8** as terminating condition | `time_network.py:47` `is_compromised` returns `len(compromised) / total_nodes > 0.25` | **Code-paper divergence**: code uses 0.25, Zhang's paper uses 0.8. Has a comment showing 0.8 was the original value, swapped at some point. |

---

## Network model

| ID | Artefact & intended behaviour | Source · locator | Lineage | Phase-0 evidence | Disposition | Test? | Relevance |
|---|---|---|---|---|---|---|---|
| **NET-01** | **3-layer HARM** (Host / Service / Vulnerability) as the *modelling* abstraction — Network is the container, not a layer | Brown §III-A, Fig 1; Zhang §4.2.1, Fig 2 | Brown / restated Zhang | `mtdnetwork/component/{network, host, services}.py` exist and form three classes | verified | N | [CORE] |
| **NET-02** | **Inter-subnet topology = Barabasi–Albert** | Brown §III-A; Zhang §4.2.1 (`AGn`) | Brown / Zhang | `network.py:175` `subgraph = nx.barabasi_albert_graph(s_nodes, m)` | verified | Y | [CORE] |
| **NET-03** | **Per-host internal service graph = Watts–Strogatz** | Brown §III-A; Zhang §4.2.1 (`AGh`) | Brown / Zhang | `host.py` `gen_internal_network(k_nearest_neighbors_percent=0.5, prob_strogatz_rewire=0.5)` | verified | N | [CORE] |
| **NET-04** | Total hosts = **200**; exposed = **20** (Brown's headline parameters) | Brown Table I | Brown | Defaults differ: `TimeNetwork.__init__` defaults to `total_nodes=50, total_endpoints=5`; the deleted driver and Phase-0 driver both use **50/5** | divergent (defaults) | N | [CORE] |
| **NET-05** | **Network topology depth = 5 layers; 20 subnets** (Brown's headline parameters) | Brown Table I | Brown | `TimeNetwork.__init__` defaults `total_layers=4, total_subnets=8`; Phase-0 baseline used `4/8` | divergent (defaults) | N | [CORE] |
| **NET-06** | **Services per host ∈ [3, 11]**; OS determines compatible service set | Brown §III-A, Table I | Brown | `constants.HOST_SERVICES_MIN=3, HOST_SERVICES_MAX=11`; `host.py:52` `random.randint(HOST_SERVICES_MIN, HOST_SERVICES_MAX)` | verified | Y | [CORE] |
| **NET-07** | **5 users per host** with **5 %** password-reuse chance | Brown §III-B(3); Zhang §4.2.2 | Brown / restated Zhang | `constants.USER_TOTAL_FOR_EACH_HOST = 5`, `USER_PROB_TO_REUSE_PASS = 0.05` | verified | N | [ATK-SWAP] |
| **NET-08** | **4 OS types** (Ubuntu / CentOS / Windows / FreeBSD) | Zhang §4.2.2 | Zhang | `constants.OS_TYPES = ["windows", "ubuntu", "centos", "freebsd"]` + per-OS version dict | verified | N | [CORE] |
| **NET-09** | **Service version ∈ [1, 99]**; older versions accumulate more vulns; version 99 **always** carries a vuln | Brown §III-A, footnote 2; restated Zhang §4.2.3 | Brown | `constants.SERVICE_VERSIONS = [1..99]`; `services.py:392` comment confirms v99 zero-day rule | verified | Y | [CORE] |
| **NET-10** | A vuln has a chance to be introduced per version and is **patched ~10 versions later** on average | Brown §III-A | Brown | `constants.VULN_PATCH_MEAN = 10`, `VULN_PATCH_RANGE = 9` | verified | N | [PERIPH] |
| **NET-11** | **Cross-platform vuln chance = 0.5** | Brown Table I; restated Zhang §4.2.3 ("half") | Brown / Zhang | `constants.VULN_PERCENT_CROSS_PLATFORM = 0.5` | verified | N | [PERIPH] |
| **NET-12** | **Vuln attack complexity ∈ [0.4, 1]** *(see C2)* | Brown Table I; cf. Zhang §4.4.3 `[0,1]` | Brown / disputed by Zhang | `services.py:23` uses `VULN_MIN_COMPLEXITY (=0.4) + (1−0.4)*random()` → **[0.4, 1]** | verified (matches Brown, not Zhang) | Y | [CORE] |
| **NET-13** | **Vuln impact ∈ [0, 1]** *(see C3)* | README; Brown §III-A "Vulnerability Layer" | Brown | `services.py:26` `self.impact = random.random() * 10` → **[0, 10]** in code | **divergent** (paper `[0,1]`, code `[0,10]`) | Y | [CORE] |
| **NET-14** | **Service compromised when Σ exploited impact > 7** *(see C3)* | README; not in any paper at this granularity | inherited | `services.py:240` `return self.exploit_value > constants.SERVICE_COMPROMISED_THRESHOLD` with threshold = **7** | verified — but the threshold is meaningful only against impacts in [0, 10] (see C3) | Y | [CORE] |
| **NET-15** | Host ID **determines its location** on the network (level/exposure) | Brown §III-A | Brown | `network.py:51` `self.exposed_endpoints = [n for n in range(total_endpoints)]` — host IDs 0..(total_endpoints−1) are exposed; level assignment is positional | verified | N | [CORE] |
| **NET-16** | Each host has a unique UUID (`uuid.uuid4()`) in addition to its host ID | inherited | inherited (added during Zhang/Ho/Tay timeline) | `host.py:50` `self.uuid = str(uuid.uuid4())`. **Not seeded** (uses `os.urandom`); this is the source of Phase-0 finding F-05. | verified, but **`uuid4` breaks full byte-determinism** — see Conflict-of-determinism note below | Y | [CORE] |
| **NET-17** | Two scenarios: (1) general/untargeted; (2) targeted on a specific host | Brown §III-C; Zhang §4.4.1.1 (Scenario 2 dropped from experiments) | Brown / partial-drop Zhang | `Network.network_type` defaults to **1** (general); `network_type==0` paths exist for the targeted scenario (`network.py:210, 272, 1024`, `attack_operation.py:216`). Phase-0 baseline only exercised the general case. | verified (general); unverified (targeted) | Y | [CORE] |

---

## Attacker module

| ID | Artefact & intended behaviour | Source · locator | Lineage | Phase-0 evidence | Disposition | Test? | Relevance |
|---|---|---|---|---|---|---|---|
| **ATK-01** | **Attack procedure (CKC + ATT&CK-inspired)**: scan → enum/recon → port-scan + credential stuffing → exploit vuln → on success: C2 reveals connected hosts (`SCAN_NEIGHBOR`) → on fail: brute force → if all fail: pick another host | Brown §III-C(2), Fig 3; Zhang §4.4.2, Fig 7 | Brown / time-extended Zhang | `Adversary._curr_process` cycle in `attack_operation.py` exercises `SCAN_HOST → ENUM_HOST → SCAN_PORT → EXPLOIT_VULN → SCAN_NEIGHBOR`, with `BRUTE_FORCE` as fallback. Confirmed in golden `attack_record.csv` (e.g. `baseline/golden/no-mtd/attack_record.csv`) | verified | Y | [ATK-SWAP] |
| **ATK-02** | **Three-phase action model & timing**: Phase 1 (`SCAN_PORT` + cred stuff, constant time); Phase 2 (`EXPLOIT_VULN`, exponential with `ACv`); Phase 3 (`BRUTE_FORCE`, time-limited) | Zhang §4.4.2, §4.4.3 | Zhang | `constants.ATTACK_DURATION = {SCAN_PORT: 25, EXPLOIT_VULN: 15, BRUTE_FORCE: 20, …}`; phases visible in attack_record's `name` column | verified | Y | [ATK-SWAP] |
| **ATK-03** | **`TAexploit` formula** (Zhang Eq 1-2): `T_Aphase2` derived from exponential `T_Aexploit` with `V_exploited` / `V_unexploited` counts and `ACv` | Zhang §4.4.3, Eq 1–2 | Zhang | `services.py:80` exploit time = `ATTACK_DURATION['EXPLOIT_VULN'] * (1 - self.complexity)`. **Not the exponential form Zhang prescribes** — uses deterministic scaling by complexity, no `V_exploited` factor | divergent (deterministic vs paper's exponential) | Y | [ATK-SWAP] |
| **ATK-04** | **Adversary learning**: exploit time **halved** for previously-exploited vuln types | Zhang §4.4.3 | Zhang | No clear implementation; `services.py:87` has a commented-out line referencing `exploit_attempt + 1`. Not in active code. | **missing** | Y | [ATK-SWAP] |
| **ATK-05** | **Confusion / time penalty** on every MTD interruption; forced re-scan | Brown §V-A; Zhang §4.4.3 | Brown / Zhang | `attack_operation.py` `_handle_interrupt` flow + `ATTACK_DURATION['PENALTY'] = 20`; network-layer MTD triggers `_attack_process.interrupt()` (`mtd_operation.py:208`) | verified | Y | [CORE] |
| **ATK-06** | **Monotonic compromise broken by MTD**; **instant re-control** if path regained | Brown §V-B; Zhang §4.4.1.3 (instant re-control statement) | Brown / softened Zhang | Hosts stay in `Adversary._compromised_hosts` once added. *Whether* MTD removes them is not obvious in code — IP/host-topology shuffle interrupts the *current* action but does not strip the compromised flag. | divergent (code has Zhang's "always compromised" rather than Brown's "MTD-broken") | Y | [CORE] |
| **ATK-07** | **Give-up rule**: per-host attempt limit (= `ATTACKER_THRESHOLD` constant); **never** give up on the target node in Scenario 2 | Brown §III-C(2), Table I (=10); Brown §V-C ("never give up") | Brown | `constants.ATTACKER_THRESHOLD = 10`; `attack_operation.py:214` `_attack_counter[curr_host_id] == _attack_threshold` ⇒ push host into `stop_attack` unless `network_type==0 and curr_host_id == target_node` | verified | Y | [CORE] |
| **ATK-08** | **Global attack-attempt cap**: `5 × total_nodes` | inherited (not from any paper) | inherited (Brown-era heuristic) | `Adversary.__init__`: `_max_attack_attempts = HACKER_ATTACK_ATTEMPT_MULTIPLER (=5) * total_nodes`. **Used:** `_curr_attempts` is incremented (`attack_operation.py:283`); the guard at line 220 is **commented out**. | divergent (computed but unused) | N | [PERIPH] |
| **ATK-09** | **MTD-block responses by category**: host-connection lost (IP/Host-Topology shuffle → re-discover); service-connection lost (OS/Service diversity, Port shuffle → re-port-scan); user-access changed (User shuffle → blocks only credential stuffing) | Brown §III-D(1–3) | Brown | Resource types per MTD: `mtd_operation.py:194-198` — `network` → host-conn class; `application` → service-conn class. Interrupt logic at `mtd_operation.py:200-228` matches Brown's three classes | verified | Y | [CORE] |
| **ATK-10** | **Application-layer MTD interrupts** the attack but does not block; adversary restarts from Phase 1; attempt threshold beyond which event fails and host is dropped | Zhang §4.4.2 | Zhang | `mtd_operation.py:215-228` interrupts only when `curr_process ∉ {SCAN_HOST, ENUM_HOST, SCAN_NEIGHBOR}` for application-layer MTDs. Restart-from-Phase-1 is the behaviour after interrupt | verified | Y | [CORE] |
| **ATK-11** | **Adversary-profile dimensions**: attack objectives / exploit-vulnerability behaviour / C2 capabilities / user-credential exploitation | Zhang §4.4.1.1–4.4.1.4 | Zhang | Currently *one* adversary profile in code (`Adversary` class). The four dimensions are present *as behaviours* but not parameterised. The lit-review direction is to expose them as configurable profiles. | unverified (dimensions implicit, not parameterised) | N | [ATK-SWAP] |
| **ATK-12** | **Target selection by distance** to discovered hosts (Zhang flags as simplification) | Zhang §6.3 | Zhang | `attack_operation.py:204-208` calls `network.sort_by_distance_from_exposed_and_pivot_host(host_stack, pivot_host_id)` — confirms Zhang's description | verified (and a `[ATK-SWAP]` upgrade point) | N | [ATK-SWAP] |
| **ATK-13** | **Attack-action enums** for metrics-relevant events: `SCAN_PORT`, `EXPLOIT_VULN`, `BRUTE_FORCE` | Ho §3.3.2 (MTTC + ASR + Attack Stage definitions) | Ho | `attack_record.csv` `name` column has these plus `SCAN_HOST`, `ENUM_HOST`, `SCAN_NEIGHBOR`. Ho's metrics restrict to the three explicit ones. | verified | Y | [CORE] |

---

## MTD module

| ID | Artefact & intended behaviour | Source · locator | Lineage | Phase-0 evidence | Disposition | Test? | Relevance |
|---|---|---|---|---|---|---|---|
| **MTD-01** | **Technique set** *(see C4)* — code carries: `IPShuffle`, `PortShuffle`, `UserShuffle`, `HostTopologyShuffle`, `OSDiversity`, `ServiceDiversity`, `CompleteTopologyShuffle`, `OSDiversityAssignment` (8 classes) | Brown §III-B (6); Zhang §4.3.1 (4 + DAP); Ho §3.3.3 (4 + "Any"); Tay §4.1 (4 + no-op) | Brown / refined per paper | All 8 classes exist (`mtd/*.py`); default `MTDScheme._mtd_strategies` = 4 active (`CompleteTopologyShuffle, IPShuffle, OSDiversity, ServiceDiversity`); other 4 commented out (see `mtd_scheme.py:22-31`) | verified (full set in code; default subset narrower) | Y | [CORE] |
| **MTD-02** | **IP Shuffle** — random new internal-host IPs; interrupts attackers using stale IP | Brown §III-B(1); Zhang §4.3.1.2 | Brown / restated Zhang | `mtd/ipshuffle.py` calls `network.get_host(host_id).ip = ...` (network-layer resource); golden run `single-ipshuffle` has 15 MTD events triggering full interrupts | verified | Y | [CORE] |
| **MTD-03** | **Port Shuffle** — reassign ports of **exposed services**; interrupts attacker using stale port | Brown §III-B(2) | Brown | `mtd/portshuffle.py` exists; **not** in the default scheme list (`mtd_scheme.py:22-31` commented) | verified (impl) / not exercised in baseline | N | [CORE] |
| **MTD-04** | **User Access Shuffle** — regenerate host user accounts; defeats credential stuffing | Brown §III-B(3) | Brown | `mtd/usershuffle.py` exists; not in default scheme list | verified (impl) / not exercised in baseline | N | [CORE] |
| **MTD-05** | **Host Topology Shuffle** — swap hosts with another host **in the same network layer** | Brown §III-B(4) | Brown | `mtd/hosttopologyshuffle.py` exists; not in default scheme list | verified (impl) / not exercised in baseline | N | [CORE] |
| **MTD-06** | **Service Diversity** — replace services on the host; disconnects ongoing service-level attack | Brown §III-B(5); Zhang §4.3.1.3 | Brown / restated Zhang | `mtd/servicediversity.py` in default scheme list; golden `random-multi` and `simultaneous-multi` events fire it | verified | Y | [CORE] |
| **MTD-07** | **OS Diversity** — randomly change OS; re-rolls services incompatible with new OS | Brown §III-B(6); Zhang §4.3.1.4 | Brown / restated Zhang | `mtd/osdiversity.py` in default scheme list; golden `single-osdiversity` exercises it | verified | Y | [CORE] |
| **MTD-08** | **Complete Topology Shuffle** — regenerate entire topology, **preserve hosts** | Zhang §4.3.1.1; Ho §3.3.3 | Zhang / restated Ho | `mtd/completetopologyshuffle.py` in default scheme list | verified | Y | [CORE] |
| **MTD-09** | **OS Diversity Assignment (DAP)** — DAP-optimised OS allocation (max-connectivity under variant counts) | Zhang §4.3.1.5, Fig 3 | Zhang | `mtd/osdiversityassignment.py` exists; **not** in default scheme list; uses `pulp` LP solver | verified (impl) / not exercised in baseline | N | [PERIPH] |
| **MTD-10** | **MTD trigger time = Uniform(1000, 5000) ms, E[T] = 3000 ms** | Brown §IV; Brown Table I "Defense trigger time" | Brown | Code does **not** use a uniform trigger. `MTD_TRIGGER_INTERVAL` table is `(mean, std)` for `simultaneous: (700, 0.5)`, `random: (200, 0.5)`, `alternative: (200, 0.5)`. The trigger is **exponential** via `time_generator.exponential_variates` (`mtd_operation.py:107-109, 152-154`). **Replaced by MTD-11 below.** | **divergent (Brown's Uniform replaced by Zhang's exponential)** | N | [CORE] |
| **MTD-11** | **MTD trigger time = Exponential(µ)** per scheme; µ from `MTD_TRIGGER_INTERVAL` table or user override | Zhang §4.3.4 | Zhang | `mtd_operation.py:108-109, 152-154` `env.timeout(exponential_variates(interval, std))` | verified | Y | [CORE] |
| **MTD-12** | **MTD execution schemes**: random / alternative / simultaneous | Zhang §4.3.2.1–3, Figs 4–5 | Zhang | `mtd_scheme.py:_init_mtd_scheme` dispatches to `_register_mtd_randomly / _alternatively / _simultaneously`; **plus** `single`, `mtd_ai`, `None` schemes for non-paper use cases. All three Zhang schemes exercised in baseline. | verified (+ extra non-paper schemes) | Y | [CORE] |
| **MTD-13** | **Resource-occupation + suspension queue** for MTD scheduling (network vs application layer) | Zhang §4.3.3, Fig 6 | Zhang | `MTDOperation` holds three `simpy.Resource(env, 1)` slots (`application_layer_resource`, `network_layer_resource`, `reserve_resource`); `mtd_scheme.suspend_mtd` populates the per-priority suspension dict. Worked example matches Zhang's. | verified | Y | [CORE] |
| **MTD-14** | **Per-technique execution duration** (mean, std) | Zhang Table 3 | Zhang | `constants.MTD_DURATION`: `CompleteTopologyShuffle:(120,0.5)`, `IPShuffle:(110,0.5)`, `OSDiversity:(80,0.5)`, `PortShuffle:(70,0.5)`, `ServiceDiversity:(70,0.5)`, `HostTopologyShuffle:(100,0.5)`, `UserShuffle:(20,0.5)`. **CompleteTopologyShuffle and IPShuffle values are off by +10 vs Zhang Table 3** (110/100). | divergent (Zhang 110/100 vs code 120/110) | N | [CORE] |
| **MTD-15** | **Reconfiguration applied to all nodes**; selective / critical-node deployment is future work | Zhang §6.4 | Zhang (future-work flag) | All MTD techniques operate on the full host list (no `node_filter` parameter anywhere in `mtd/*.py`) | verified (status quo matches Zhang's "all nodes" baseline) | N | [PERIPH] |

---

## MTDShield / adaptive selection (Tay + Ho)

> The baseline runs **do not exercise this module**. Disposition is therefore
> static (code presence) only, not behavioural.

| ID | Artefact & intended behaviour | Source · locator | Lineage | Phase-0 evidence | Disposition | Test? | Relevance |
|---|---|---|---|---|---|---|---|
| **SHD-01** | **Reactive RL plugin**: reads network posture → decides whether to trigger → selects technique | Tay §4 intro, Fig 1; §4.1 | Tay | `mtdnetwork/mtdai/mtd_ai.py` (DDQN model code), `operation/mtd_ai_operation.py` (the operation surface) and `operation/mtd_ai_training.py` exist | verified (impl present); behavioural unverified | Y | [CORE] |
| **SHD-02** | **RL formulation**: MDP + **Double DQN** (Eq 1, Fig 2) with experience replay | Tay §4.1, §4.2 | Tay / Ho (joint dev) | `mtd_ai.py` imports TensorFlow / Keras; build uses Dense + LSTM + Dropout layers consistent with `T-FX-01` / `T-TS-01` | unverified (TF not installed; not exercised) | N | [CORE] |
| **SHD-03** | **Action set: 5** = `IPShuffle`, `OSDiversity`, `ServiceDiversity`, `CompleteTopologyShuffle`, **no-op** | Tay §4.1, §4.1.4 | Tay | `mtd_scheme.py` `_register_mtd_ai` path indexes into a `_mtd_custom_strategies` list — passed via the AI driver. The fifth "no-op" action is the *absence* of a register call. | unverified | Y | [CORE] |
| **SHD-04** | **Pairwise + Null action space** (Ho variant) — `{MTD_1, …, MTD_{n(n+1)/2}, Null}` | Ho §3.2.3 | Ho | Not directly observed; conflicts with `SHD-03`. **Conflict candidate** (see "Conflicts" §). | unverified | N | [CORE] |
| **SHD-05** | **Static-feature branch** (`Dense 128 + ReLU + BN + Dense 64 + ReLU + BN + Dropout 30 %`); inputs incl. **HCR, Number of Vulnerabilities, Number of Exposed Vulnerabilities, Attack Path Exposure Score** | Tay §4.1.1 | Tay | Architecture in `mtdai/mtd_ai.py` matches Tay's layer counts; feature list expects metrics defined in `statistic/security_metric_statistics.py` and `statistic/utils.py` | unverified | N | [IDS-SEAM] |
| **SHD-06** | **Time-series branch** (`LSTM 64 → BN → LSTM 32 → BN → Dropout 30 %`); inputs incl. **MTTC, Downtime/Operational Impact, Time Since Last MTD** | Tay §4.1.2 | Tay | Same as `SHD-05` — architecture present; not exercised in baseline | unverified | N | [IDS-SEAM] |
| **SHD-07** | **Feature fusion** (concat → `Dense 64 + ReLU + BN + Dropout 30 %`) | Tay §4.1.3 | Tay | Architecture present in `mtd_ai.py` | unverified | N | [CORE] |
| **SHD-08** | **Q-Network output** = 5-unit dense layer | Tay §4.1.4 | Tay | Architecture present in `mtd_ai.py` | unverified | N | [CORE] |
| **SHD-09** | **Reward** = `f(N_{t+1}) − f(N_t)`; multi-metric via weighted sum (w_i ∈ ±1 by feature direction); min-max normalisation against in-memory history; training starts after 1000 samples | Ho §3.2.4 | Ho | `mtd_ai_training.py` carries the reward + replay-buffer logic; specific reward formula unverified | unverified | N | [CORE] |
| **SHD-10** | **Static Degrade Factor (SDF) = 2000 ms** — if `now − last_MTD > SDF`, force a random MTD; check runs *before* metrics feed into the agent | Ho §3.1.2, Fig 2 | Ho | Look for `static_degrade_factor` / `SDF` in `mtdai/mtd_ai.py` and `mtd_ai_operation.py` — code path exists in `operation/mtd_ai_operation.py` | unverified | Y | [IDS-SEAM] |
| **SHD-11** | **Hyperparameter defaults** (Ho/Tay agree): γ=0.95, ε=1.0, ε_min=0.01, ε_decay=0.995, training_start=1000, episodes=100; sim finish_time=15000, total_nodes=150 | Ho Table 1–2 | Ho | Defaults consistent across `mtd_ai_training.py` and the deleted `experiments/run.py` (commits `e5935ab`) | unverified | N | [PERIPH] |
| **SHD-12** | **Best hyperparameter regions** (Tay's evaluation): γ ∈ [0.75, 0.90], ε ∈ [0.5, 0.7] with decay 0.99, train_start = 2000 | Tay §5.2.1–3, §6.1–3 | Tay | Not in baseline | unverified | N | [PERIPH] |
| **SHD-13** | **Attacker-detection-rate (IDS sensitivity) experiment** — feed model varying fractions of attacker-action information (0–100 %); **performance cutoff ≈ 0.7** | Tay §5.3, §6.4, Fig 6 | Tay | Look for `attacker_sensitivity` / `detection_rate` params in `mtd_ai_operation.py` (`execute_ai_model` in the deleted driver had an `attacker_sensitivity` kwarg) | unverified (parameter present, behaviour not run) | Y | [IDS-SEAM] |

---

## Metrics & evaluation

| ID | Artefact & intended behaviour | Source · locator | Lineage | Phase-0 evidence | Disposition | Test? | Relevance |
|---|---|---|---|---|---|---|---|
| **MET-01** | **MTTC** = mean duration over `SCAN_PORT`, `EXPLOIT_VULN`, `BRUTE_FORCE` events for relevant hosts; 0 if none | Zhang §3.4; Ho §3.3.2 (#8) | Zhang / restated Ho | `statistic/evaluation.py:106-108` — exactly that calc | verified | Y | [CORE] |
| **MET-02** | **Attack Success Rate (ASR)** = compromised / attempts (`SCAN_PORT + EXPLOIT_VULN + BRUTE_FORCE`) | Ho §3.3.2 (#6) | Ho | `evaluation.py:109-116` computes `attack_success_rate = comp_num / attack_event_num` per checkpoint. Note: numerator is the *checkpoint target*, not actually-compromised — possible Phase-0 finding | divergent (numerator semantics) | Y | [IDS-SEAM] |
| **MET-03** | **MTD Execution Frequency (MEF)** = `N_MTD / (finish_last − start_first)` | Ho §3.3.2 (#7) | Ho | `evaluation.py:73-80` exactly that | verified | Y | [IDS-SEAM] |
| **MET-04** | **Host Compromise Ratio (HCR)** = `C_t / T_host` | Ho §3.3.2 (#4) | Ho | The `host_compromise_ratio` field in `evaluation_result_by_compromise_checkpoint` is `compromised_num / comp_num` where `comp_num = T_host × checkpoint_ratio` — **not** `C_t / T_host`. Values > 1 in golden outputs (e.g. `1.2`). | divergent (paper `C_t / T_host`, code `C_t / (T_host × checkpoint)`) — Phase-0 finding F-10 | Y | [IDS-SEAM] |
| **MET-05** | **Attack Path Exposure (APE)** = mean new-vuln% across hosts on the shortest attack path | Ho §3.3.2 (#1) | Ho | `evaluation.py:120-131` populates `attack_path_exposure` from `network.attack_path_exposure()` | verified (formula present); semantics not yet checked against Ho's `V_new(h)` definition | N | [IDS-SEAM] |
| **MET-06** | **Risk (R)** = `CSP(h) · AI(h)` | Ho §3.3.2 (#2) | Ho | `evaluation.py:163-164` reads `risk` from the scorer's per-vuln risk list; computed in `services.py` `risk()` method | verified (presence); paper formula vs code formula not yet aligned | Y | [CORE] |
| **MET-07** | **Return on Attack (RoA)** = Risk / AC; AC = time to exploit | Ho §3.3.2 (#3), Eqs 3-4 | Ho | `services.py:144, 164` `roa()` formulas use `complexity * impact / exploit_time` — consistent in shape with Ho | verified (shape) | Y | [CORE] |
| **MET-08** | **Time Since Last MTD (TSLM)** = `now − last_MTD_executed_time` | Ho §3.3.2 (#9) | Ho | `time_network.py` carries `last_mtd_triggered_time`; computed in `evaluation.py:188-189` but with `time_since_last_mtd = 1` hard-coded (commented-out env-dependent calc above it) | divergent (hard-coded to 1) | Y | [IDS-SEAM] |
| **MET-09** | **Shortest Attack Path Variability (SAPV)** = cardinality of set difference between consecutive shortest-path sets | Ho §3.3.2 (#10) | Ho | `evaluation.py:167-168` computes `shortest_path_variability` from `scorer.shortest_path_record` | verified (shape) | N | [IDS-SEAM] |
| **MET-10** | **Network Address Variability (NAV)** = address changes / state size; ∈ [0, 1] | Ho §3.3.2 (#11) | Ho | Not visibly computed in `evaluation.py`. Likely lives in `statistic/security_metric_statistics.py` or `utils.py`. | unverified | N | [IDS-SEAM] |
| **MET-11** | **Attack Stage** = integer enum of the current attacker process (Ho restricts to `SCAN_PORT … BRUTE_FORCE`) | Ho §3.3.2 (#5) | Ho | The full set in code is `SCAN_HOST, ENUM_HOST, SCAN_PORT, SCAN_NEIGHBOR, EXPLOIT_VULN, BRUTE_FORCE`. Ho's RL feature would project to the smaller set. | verified (superset present); projection unverified | N | [IDS-SEAM] |
| **MET-12** | **Static security metrics** from earlier work (carried through): Attack Cost, Return on Attack, System Risk, Reliability | Brown §IV ("other metrics"); Zhang §3.4; Ho §2.3 | Brown / Zhang / Ho | Risk, RoA, AC partially implemented in `scorer.py` `VulnStatistics`; Reliability not present | verified (partial) | N | [CORE] |
| **MET-13** | **Dynamic security metrics** (T-HARM lineage): MAPL, NAP, APV, ESP, AI | Ho §2.3.2 (literature reference) | Ho (review only) | Not implemented as named outputs; only APE/SAPV/NAV are exposed | **missing** | N | [PERIPH] |
| **MET-14** | **Evaluation designs**: single-MTD (effectiveness × interval × network size) and multiple-MTD (pairwise combinations × execution scheme) | Zhang §5; Ho §3.3 (Tables 4-8) | Zhang | Phase-0 driver exercises single (`single-ipshuffle`, `single-osdiversity`) and the three multi-MTD schemes (`random-multi`, `alternative-multi`, `simultaneous-multi`) | verified | N | [CORE] |
| **MET-15** | **Network Compromise Ratio (NCR) terminating condition = 0.8** | Zhang §5 | Zhang | `time_network.py:47` `is_compromised` uses **0.25**, not 0.8 *(see C6)* | divergent | Y | [CORE] |
| **MET-16** | **Network properties** (Zhang Table 2): {25, 50, 75, 100} nodes; per-network endpoint + layer counts | Zhang §5, Table 2 | Zhang | Not encoded as defaults; phase-0 used Zhang's Net2 row (50 nodes, 5 endpoints, 4 layers) | verified (one row); rest not exercised | N | [CORE] |
| **MET-17** | **Final-score normalisation** against no-MTD baseline (equal-weighted ASR + ROA + APE + Risk) | Ho §3.4.2; Tay §5.1 | Ho / Tay | Logic lives in the deleted `experiments/run.py`'s `construct_average_result`; not present in current code | **missing** | N | [PERIPH] |

---

## Simulation engine & IO

| ID | Artefact & intended behaviour | Source · locator | Lineage | Phase-0 evidence | Disposition | Test? | Relevance |
|---|---|---|---|---|---|---|---|
| **SIM-01** | **Discrete-event simulation** on **SimPy** | Zhang §4.5; Tay §4 (inherited) | Zhang | `simpy.Environment` used in `MTDOperation`, `AttackOperation`; `env.run(until=...)` drives time advance | verified | Y | [CORE] |
| **SIM-02** | **Exponential** distribution for inter-event time + action duration | Zhang §4.5, Eq 3–4 | Zhang | `time_generator.py:8-9` `exponential_variates` (used by MTD trigger interval, MTD exec time, exploit time). Other distributions present but unused. | verified | N | [CORE] |
| **SIM-03** | **Time-based proactive MTD scheduling** + reactive MTDShield plugin running in parallel | Zhang §4.3 (time-based); Tay §4 (reactive) | Zhang / Tay | Two parallel surfaces: `MTDOperation` (time-based, exercised in baseline) and `MTDAIOperation` (reactive, in `operation/mtd_ai_operation.py`, not exercised) | verified (time-based); reactive presence verified, behaviour unverified | Y | [CORE] |
| **SIM-04** | **Snapshot capability** for network + adversary state, keyed by size or time | inherited (Brown era, retained by Zhang) | Brown / Zhang | `snapshot/snapshot_checkpoint.py` exists with `save_snapshots_by_network_size`, `load_snapshots_by_time`. Phase-0 baseline did not exercise this. | verified (impl); unverified (behaviour) | N | [PERIPH] |
| **SIM-05** | **RNG / seeding** — central seed plumbing | (not stated by any paper) | inherited gap | No central seeding; `Network.__init__` has a `seed=None` kwarg honoured only when passed; `TimeNetwork.__init__` does **not** forward it; `numpy.random` never seeded internally. Phase-0 driver seeds both `random` and `np.random` externally. UUID-only non-determinism remains (F-05). | **divergent (missing central plumbing)** | Y | [CORE] |
| **CFG-01** | **Run entry point** (`run.py` / CLI / `--help`) | Brown README (text); Zhang & Ho via inherited `experiments/run.py` | Brown / inherited | **Missing on `main`** (deleted in `e5935ab`). Replaced by `baseline/run_baseline.py` for Phase 0. | **missing** | Y | [CORE] |
| **CFG-02** | **Output artefacts**: network figure, attack record, MTD record, evaluation JSON | Brown README; Zhang §4 + figures | Brown | All produced by Phase-0 driver (`baseline/golden/*/{network_initial.png, attack_record.csv, attack_record.png, mtd_record.csv, mtd_record.png, evaluation.json}`). Note: `Evaluation.visualise_*` methods in `statistic/evaluation.py` have broken `plt.savefig` calls (tuples instead of paths) — F-08. | verified (via driver); built-in helpers `divergent` (broken) | N | [CORE] |
| **CFG-03** | **Configurable Network Properties** (Zhang Table 2) and **MTD Execution Time** (Zhang Table 3) tables | Zhang Tables 2-3 | Zhang | MTD durations: `constants.MTD_DURATION` (drift from Table 3 — see MTD-14). Network properties: hard-coded defaults in `TimeNetwork.__init__`, not driven from a config table. | divergent (no config-table mechanism; constants drift) | N | [CORE] |

---

## What runs vs what doesn't (Phase-0 summary)

| Scenario | Lineage | Status in baseline |
|---|---|---|
| No MTD | Brown / Zhang | runs ✓ |
| Single MTD: IP shuffle | Brown / Zhang | runs ✓ |
| Single MTD: OS diversity | Brown / Zhang | runs ✓ |
| Multi MTD: random / alternative / simultaneous | Zhang | runs ✓ (all three) |
| Targeted attack (`network_type==0`) | Brown Scenario 2 | code present, not exercised |
| Multi MTD: DAP-optimised OS diversity | Zhang | code present, not registered |
| Port / User / Host-Topology shuffles | Brown | code present, commented out of default scheme list |
| MTDShield reactive plugin | Tay | code present, requires TensorFlow (not installed in baseline env) |
| Federated training | none (not in Tay) | not implemented |
| Snapshot load/save | inherited | code present, not exercised |

---

## Biggest faithfulness risks (highlights of the divergence column)

1. **MET-15 / C6** — `is_compromised` threshold `0.25` in code vs `0.8` in Zhang. Termination behaviour is **3× more lenient** than Zhang's, meaning baseline MTTC numbers stop being comparable to her figures.
2. **NET-13 / C3** — vulnerability impact is `random()*10` (range `[0, 10]`) in code, `[0, 1]` per README/Brown. The threshold `SERVICE_COMPROMISED_THRESHOLD = 7` is interpretable only on the `[0, 10]` scale. **README is wrong.**
3. **ATK-03** — Zhang's `T_Aphase2` formula (exponential with `V_exploited`/`V_unexploited`) is *not* the formula the code uses; code uses a simpler deterministic `ATTACK_DURATION × (1 − complexity)`.
4. **ATK-04** — "exploit time halved for previously-exploited vuln types" is **missing** from active code.
5. **MET-04 / F-10** — code's `host_compromise_ratio` field is `C_t / (T_host × checkpoint_ratio)`, not `C_t / T_host`. Several golden runs show ratios > 1. Multiple papers cite this name.
6. **SHD-04** — Ho's pairwise-action-space vs Tay's 5-action no-op set is unresolved; the code path that exposes actions to the RL agent is `mtd_scheme._register_mtd_ai` which indexes into `_mtd_custom_strategies` — likely Tay's variant.
7. **MTD-14** — `CompleteTopologyShuffle` duration in code (`120`) and `IPShuffle` (`110`) differ from Zhang Table 3 (`110`, `100`) by `+10` each.
8. **SIM-05** — no central RNG plumbing; only the Phase-0 driver seeds anything; UUIDs use unseeded `os.urandom`.
9. **CFG-01** — there is no entry point on `main`.
10. **MET-08 (TSLM)** — code hard-codes `time_since_last_mtd = 1` rather than computing the time since last MTD; the env-dependent line is commented out.

---

## Top conflicts for Marc to disposition

| # | Conflict | Recommended next step |
|---|---|---|
| C1 | "3-layer HARM" vs "5 layers" | **Probably not a conflict** — split into two artefacts (NET-01 = HARM, NET-05 = topology depth). |
| C2 | AC range `[0.4, 1]` (Brown / code) vs `[0, 1]` (Zhang) | Treat Brown + code as ground truth; flag Zhang §4.4.3 as imprecise wording. |
| C3 | Impact range `[0, 1]` (papers + README) vs `[0, 10]` (code) | Pick a side; README is the easiest to fix (and is internally inconsistent: it states `[0, 1]` and threshold `7` in the same paragraph). |
| C4 | MTD technique-set membership across papers | **Resolved** by spec (MTD-01); code carries 8 classes; the *exposed* set is paper-dependent. |
| C5 | Zero-day v99 + cross-platform = 0.5 | **Not a conflict.** Two independent rules. |
| C6 | NCR termination ratio (0.25 in code vs 0.8 in Zhang) | **Bug or deliberate change?** Either way, every baseline metric depends on this. Top priority to disposition. |
| C7 (new) | ATK-03 — exploit-time formula | Decide whether to faithfully reimplement Zhang's exponential `T_Aexploit`, or treat the deterministic implementation as the inherited reality. |
| C8 (new) | MET-04 — HCR field semantics | The field `host_compromise_ratio` is used by downstream code (and possibly the RL feature pipeline). Fixing its semantics is small but ripples. |

---

## Coverage gaps to close in follow-up passes

- Re-run Phase-0 with the **targeted attack scenario** (`network_type = 0`, target_layer set) to disposition NET-17 / ATK-07 / ATK-12 against real outputs.
- Exercise the **MTDShield (`mtd_ai`) execution scheme** with TF installed to disposition all `SHD-*` rows.
- Exercise the **`OSDiversityAssignment` (DAP)** technique to disposition `MTD-09`.
- Confirm `MET-10` (NAV) computation lives in `statistic/security_metric_statistics.py` and matches Ho's set-difference formula.
- Walk `ATK-06` (MTD-broken monotonic-compromise rule) through the code path — does any MTD remove a host from `Adversary._compromised_hosts`? My quick scan said no. If confirmed, Brown's foundational rule is `divergent`.

---

## Relationship to baseline

- **Golden outputs** live in `baseline/golden/`. Any change that re-touches the simulator should regenerate them and diff against the existing values; large changes to MTTC distribution, attack-record event counts, or scheme-specific MTD-event counts (e.g. 15 for random-multi at finish_time=3000, seed=1234) are the immediate signal.
- **Determinism** is full-byte except for the UUID column (NET-16 / SIM-05 / F-05). A faithfulness test that compares `attack_record.csv` byte-for-byte should mask the UUID column.
- Every artefact marked `Test? Y` is a candidate for a small assertion in `tests/` once the test scaffolding exists.
