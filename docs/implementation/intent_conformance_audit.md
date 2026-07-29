---
status: audit record
created: 2026-07-28
updated: 2026-07-28
---

# Intent-spec conformance audit — the substrate against the literature-only yardstick

**What this is.** A row-by-row audit of the current substrate (`mtdnetwork/`) against
[`mtdsim_intent_spec.md`](mtdsim_intent_spec.md), classifying every IS-ID per the spec's
§c procedure: **CONFORMS / CONFORMS-SUPERSEDED / DIVERGES-DOCUMENTED-NOWHERE / UNTESTABLE**.
Code locators live here, never in the intent spec. Nothing was fixed in this audit; the
divergences feed the disposition list at the bottom, and only Marc's disposition makes any
of them a bug (guardrail: "bug is a verdict, not a first impression").

**Method.** All `[config]` rows checked statically against `mtdnetwork/data/constants.py`
and constructor defaults; `[behav]` rows verified by reading the executing code path and,
where observable, by tracer runs (`python -m mtdnetwork.trace`, seed 42, `--scheme none`
and `--scheme simultaneous --finish-time 6000`); `[struct]` rows by module inspection.
The audit targets the **native substrate arm** only. S3-R (2026-07-28) re-homed attacker
timing for the *movement* arm (`step(duration=...)`, `charge_time=False`); those
carve-outs are movement-layer policy, not substrate divergences, and are excluded
throughout.

**Cross-check status.** The prior conformance record [`mtdsim_spec.md`](mtdsim_spec.md)
and [`metrics_semantics.md`](metrics_semantics.md) were read only *after* the
classifications below were complete; the cross-check is §(m).

**Classification tallies** (85 rows, §a–§j below): **70 CONFORMS** (many with recorded
deltas; includes IS-SCN-02, which conforms to Zhang's documented simplification under
precedence), **1 CONFORMS-SUPERSEDED** (IS-TIM-01, Brown's uniform trigger — removed, not
surviving), **9 DIVERGES-DOCUMENTED-NOWHERE** (IS-NET-08, IS-MTD-05, IS-TIM-07, IS-INT-03,
IS-INT-06, IS-PRC-04, IS-PRM-04, IS-AI-05, IS-AI-06), **4 UNTESTABLE** (IS-NET-14,
IS-SCN-05, IS-PRM-05, IS-MET-05), and **1 split row** (IS-NET-10 — complexity sits inside
conflict IS-CFL-01, impact diverges per IS-CFL-07).

---

## a) Architecture and modules (IS-ARC)

| ID | Verdict | Evidence |
|---|---|---|
| IS-ARC-01 | **CONFORMS** | Three entities present as modules: `component/network.py` (+`time_network.py`), `component/adversary.py` + `operation/attack_operation.py`, `mtd/*` + `operation/mtd_operation.py`. |
| IS-ARC-02 | **CONFORMS** (delta) | Host layer = per-network graph (`network.py:159` BA composition); service layer = per-host Watts–Strogatz service graph (`host.py:536`); vulnerability layer = per-service vulnerability *list* (`services.py:237`), not a distinct attack-tree graph. Three conceptual layers present; the third is flattened. Zhang names them AGn/AGh/ATs — ATs-as-list is a representational simplification, recorded not adjudicated. |
| IS-ARC-03 | **CONFORMS** | The flowchart survives as the six-verb FSM in `attack_operation.py` (`proceed_attack`, `_execute_*` tail-calls). Kill-chain-shaped phase order confirmed in trace (seed 42): SCAN_HOST → ENUM_HOST → SCAN_PORT → EXPLOIT_VULN → BRUTE_FORCE / SCAN_NEIGHBOR. |
| IS-ARC-04 | **CONFORMS** | Schemes accept `custom_strategies` (single through full set); all eight technique classes pluggable via `MTDScheme._mtd_strategies` (`mtd_scheme.py:22-31`). |
| IS-ARC-05 | **CONFORMS** | SimPy discrete-event throughout; both MTD interval (`mtd_operation.py:113`) and per-technique execution duration (`mtd_operation.py:175`) are modelled — Zhang's stated fix of Brown's deficiency is present. |

## b) Network model (IS-NET)

| ID | Verdict | Evidence |
|---|---|---|
| IS-NET-01 | **CONFORMS** | `nx.barabasi_albert_graph` per subnet, subnets per layer (`network.py:175`), composed into the host graph — "small subnets in each level of depth" as documented. |
| IS-NET-02 | **CONFORMS** | `nx.connected_watts_strogatz_graph` for the per-host internal service network (`host.py:536`), k = 50 % of services (min 2), rewire p = 0.5. |
| IS-NET-03 | **CONFORMS** (delta) | Inputs: total nodes, endpoints (exposed), layers (`Network.__init__`); layer 0 consists only of the exposed endpoints (`network.py:51,137`); remaining hosts distributed by random increments over layers 1..n (`network.py:143-145`). Extra undocumented inputs: `total_subnets`, `total_database`. |
| IS-NET-04 | **CONFORMS** | Per-host OS, ID, services (`network.py:937-950`); services drawn from per-OS pools (`services.py:355-369`); `HOST_SERVICES_MIN/MAX = 3/11` (`constants.py:67-68`). |
| IS-NET-05 | **CONFORMS** | Host ID ranges map deterministically to layer/subnet blocks (sequential `node_id` offsets, `network.py:168-179`) — as much rule as the underspecified paper row demands. |
| IS-NET-06 | **CONFORMS** | `VULN_PERCENT_CROSS_PLATFORM = 0.5` (`constants.py:83`), applied as a per-service coin flip making the service available on all four OSs (`services.py:427-428`). |
| IS-NET-07 | **CONFORMS** | Versions 1–99 (`constants.py:42-45`); older versions carry strictly more vulnerabilities (`services.py:461`, see IS-NET-08 for the mechanism); same-name services share vulnerabilities by preserved id across per-host copies (`Vulnerability.copy`, `services.py:54-83`). |
| IS-NET-08 | **DIVERGES-DOCUMENTED-NOWHERE** | Brown: each version has a chance of *introducing* a vulnerability, *patched ~10 versions later*. Code: 100 draws at p = 0.10 place a **patch point** at `i + randint(-9, 9)` (`services.py:437-443`); every vulnerability then exists **from version 1** until its patch point (`services.py:461` — active while `key >= sv_index`). There is no introduction point and no ~10-version lifetime; `VULN_PATCH_MEAN = 10` is a dead constant in the live path. The monotone older-more-vulns *outcome* survives; the documented lifecycle mechanism does not. |
| IS-NET-09 | **CONFORMS** | `vulns[99]` unconditionally added (`services.py:446-449`); with the `key >= sv_index` rule it is active in **every** version, satisfying the normative purpose (any service compromisable). |
| IS-NET-10 | **CONFORMS / split by conflict** | Complexity = `0.4 + 0.6·U(0,1)` → Brown's **[0.4, 1]** range (`services.py:24`, `constants.py:89`). But the *semantics* are Zhang's polarity: higher complexity ⇒ higher success probability (`services.py:150`) and shorter exploit time (`services.py:115`). Impact = `U(0,1)·10` → **[0, 10]** (`services.py:27`) — see IS-CFL-07 (diverges from the only documented range). |
| IS-NET-11 | **CONFORMS** | `USER_TOTAL_FOR_EACH_HOST = 5`, `USER_PROB_TO_REUSE_PASS = 0.05` (`constants.py:59-61`); reuse drawn per user at network level (`network.py:687-690`), fuelling credential stuffing. |
| IS-NET-12 | **CONFORMS** | Exactly windows/ubuntu/centos/freebsd (`constants.py:3-8`), each with its own service pool (`services.py:404-471`). |
| IS-NET-13 | **CONFORMS** (oddity noted) | Unique IP per host at setup (`network.py:937-941`); pivoting keyed on graph reachability. Oddity: octets drawn `randint(1, 256)` (`host.py:635`) — 256 is not a valid octet; cosmetic, no paper contact. |
| IS-NET-14 | **UNTESTABLE** | `[intent]` row; noted that it licenses treating parameter deltas as less severe than rule deltas (applied in §h). |

## c) MTD techniques (IS-MTD)

Default live set (`mtd_scheme.py:22-31`): CompleteTopologyShuffle, IPShuffle, OSDiversity,
ServiceDiversity — exactly Zhang's selected four, **minus** Zhang's own DAP addition.
HostTopologyShuffle, PortShuffle, UserShuffle, OSDiversityAssignment exist but are
commented out of the default set. All seven pre-Zhang techniques are implemented — see
IS-CFL-06.

| ID | Verdict | Evidence |
|---|---|---|
| IS-MTD-01 | **CONFORMS** | New random IP for every host **except exposed endpoints** (`ipshuffle.py:14-25`) = Brown's "all internal hosts". Interrupt semantics network-layer (§f). |
| IS-MTD-02 | **CONFORMS** (delta) | `portshuffle.py`: reassigns every service node's port on every **non-exposed host** (target node excepted). Brown says "all exposed services"; code exempts exposed *hosts* entirely (in-code justification comment) and shuffles all services on the rest. Latent (not in default set). |
| IS-MTD-03 | **CONFORMS** | `usershuffle.py`: re-draws each host's users from the network user list. Its *blocking* behaviour diverges — see IS-INT-03. |
| IS-MTD-04 | **CONFORMS** | Same-layer host swap (`hosttopologyshuffle.py:29-55`), pairs drawn within `host_id_list_in_layer`; the same-layer constraint is enforced, exposed endpoints exempted (undocumented but consistent with layer 0 = endpoints). Latent (not in default set). Adversary id-keyed state remapped on swap (`adversary.py:28-60`). |
| IS-MTD-05 | **DIVERGES-DOCUMENTED-NOWHERE** | Zhang (operative): re-configure services **with different versions** — the 99-version pool as diversity space. Code: replaces each service with a **random different service at its latest version** (`servicediversity.py:13-27` → `get_random_service_latest_version`, `services.py:371-385`), and skips exposed hosts. No draw from the version pool; latest-only replacement systematically *reduces* vulnerability count (newest versions carry fewest). Deliberate-looking, self-consistent — candidate design choice, not obviously a bug. |
| IS-MTD-06 | **CONFORMS** (delta) | New OS drawn randomly from the four types; incompatible services replaced (`osdiversity.py:17-41`). Deltas: replacement services are latest-version (same mechanism as IS-MTD-05); exposed hosts exempted; OS *version* keeps the previous version's index. |
| IS-MTD-07 | **CONFORMS** | `completetopologyshuffle.py:15-27`: full `gen_graph()` regeneration with host instances re-attached — Ho's "preserving the hosts" addendum implemented literally. |
| IS-MTD-08 | **CONFORMS** (latent) | `osdiversityassignment.py`: PuLP MIP over a single-source/single-destination reduction (`gen_single_connection_graph`) with exposed endpoints and database nodes as the client classes — Zhang's documented abstraction. Not in the default strategy set; re-solves only at compromise-ratio checkpoints (undocumented optimisation). Reuses OSDiversity's name for duration/priority lookup → inherits 80 s, matching Zhang's DAP_OSDiversity 80 s. |
| IS-MTD-09 | **CONFORMS** | Resource classes: network = {IPShuffle, CompleteTopologyShuffle, HostTopologyShuffle}; application = {OSDiversity, ServiceDiversity, PortShuffle, DAP}; reserve = {UserShuffle} (each strategy's `resource_type`). Matches Zhang's two classes for his four, extends Brown-era techniques consistently with Brown's three interaction classes (Port Shuffle service-level → application; User Shuffle its own class → reserve). Drives both contention (§d) and interrupts (§f). |

## d) Execution schemes and scheduling (IS-SCH)

| ID | Verdict | Evidence |
|---|---|---|
| IS-SCH-01 | **CONFORMS** | Periodic signal loop (`mtd_operation.py:75-114`); register → priority heap (`mtd_scheme.py:59-67`); suspended dict popped **before** the main queue (`mtd_operation.py:91-94`) = higher pop priority for suspended instances. |
| IS-SCH-02 | **CONFORMS** | `_register_mtd_randomly` (`mtd_scheme.py:81-90`): one random technique per signal, single trigger. |
| IS-SCH-03 | **CONFORMS** | `_register_mtd_alternatively` (`mtd_scheme.py:92-98`): deque rotation — fixed order based on previously registered instance. |
| IS-SCH-04 | **CONFORMS** | `_register_mtd_simultaneously` + `_mtd_batch_trigger_action` (`mtd_operation.py:116-159`): all techniques registered and triggered per signal; contended ones suspended to the next cycle. Trace (seed 42) shows all four deploying per cycle with network-layer pair serialised (IPShuffle completes at t=211.2 after CTS at t=110.5). |
| IS-SCH-05 | **CONFORMS** (delta) | `simpy.Resource(capacity=1)` per layer (`mtd_operation.py:44-46`); occupied resource → suspend (`mtd_operation.py:103-110`). Zhang's worked example holds: IPShuffle/CTS mutually exclude; ServiceDiversity independent. Delta: a suspended instance re-enters at the **next trigger signal**, not the instant the resource frees; and a same-priority instance already suspended causes **discard** (undocumented rule). In the batch scheme the resource test happens before `yield request`, so two same-layer MTDs registered in one cycle can both pass the empty-check and serialise on the resource queue instead of via the suspension dict (observed in trace: 0 "held back", yet serialised execution). |
| IS-SCH-06 | **CONFORMS** (as underspecification) | Concrete ordering `MTD_PRIORITY` (`constants.py:117-125`): CTS 1 → HostTopologyShuffle 2 → IPShuffle 3 → OSDiversity 4 → PortShuffle 5 → ServiceDiversity 6 → UserShuffle 7. No paper documents any ordering — an undocumented choice by spec fiat, recorded not adjudicated. |

## e) Time model (IS-TIM)

**The one interpretive fork that matters.** Every stochastic draw in the substrate goes
through `exponential_variates(loc, scale)` = `scipy.stats.expon.rvs(loc, scale)`
(`time_generator.py:8-9`), invoked as `(mean-like value, 0.5)`. That is a **location-shifted
exponential**: draw = loc + Exp(scale 0.5), i.e. mean ≈ loc + 0.5 and standard deviation
exactly 0.5 — *near-deterministic*, not an exponential with mean loc. Whether this matches
Zhang's intent hinges on reading §4.5's "µ is the historical average": µ-as-mean would make
the code diverge everywhere; µ-as-location is the only reading consistent with Zhang's own
Table 3, which quotes each MTD duration as (mean, **standard deviation 0.5**) — an
exponential with mean 110 cannot have σ = 0.5 unless it is exactly this shifted
construction. The audit therefore classifies the *duration* rows as conforming and flags
the fork itself for disposition (D-08) rather than asserting either reading.

| ID | Verdict | Evidence |
|---|---|---|
| IS-TIM-01 | **CONFORMS-SUPERSEDED** (removed) | No uniform trigger anywhere; Brown's `MTD_MIN/MAX_TRIGGER_TIME = 1000/5000` survive only as comments (`constants.py:54-55`). The replacement is documented (Zhang) — nothing Brown-faithful remains to run. |
| IS-TIM-02 | **CONFORMS** (delta) | Trigger interval drawn `exponential_variates(interval, 0.5)` (`mtd_operation.py:113-114`) — exponential-family, subject to the fork above (effective σ 0.5 about the mean). The means themselves — random/alternative **200**, simultaneous **700** (`constants.py:110-114`) — are documented nowhere (Zhang tested 50–200 s but published no per-scheme means); undocumented choices, with 700 outside Zhang's tested range. |
| IS-TIM-03 | **CONFORMS** | `MTD_DURATION` (`constants.py:128-136`): CTS (110, 0.5), IPShuffle (100, 0.5), OSDiversity (80, 0.5), ServiceDiversity (70, 0.5) — Zhang Table 3 exactly; DAP inherits OSDiversity's 80 via the shared name (`osdiversityassignment.py:14-18`). Beyond-paper extras: HostTopologyShuffle (100, 0.5), PortShuffle (70, 0.5), UserShuffle (20, 0.5) — durations for Brown-era techniques documented nowhere. |
| IS-TIM-04 | **CONFORMS** (fork flagged) | The exponential is the sole PDF for MTD intervals, MTD durations, per-vuln exploit time and the confusion penalty — all via `exponential_variates`. The µ-as-location reading (above) is applied uniformly. Weibull/normal/uniform/poisson helpers exist unused (`time_generator.py:12-25`). |
| IS-TIM-05 | **CONFORMS** | Phase 1 constant: SCAN_PORT fixed 25, credential check instantaneous (`constants.py:140-148`, `attack_operation.py:127-133`); Phase 3 fixed budget: BRUTE_FORCE 20; Phase 2 variable per-vulnerability (below). |
| IS-TIM-06 | **CONFORMS** (as far as testable) | Per-vuln exploit duration = `exponential_variates(vuln.exploit_time(host), 0.5)` (`attack_operation.py:455-457`) with base `15·(1 − complexity)` (`services.py:115`) — exponential form ✓, ACv-dependence ✓ (Zhang polarity: easier ⇒ faster); only unexploited vulns are attempted (`Service.get_vulns` filters exploited, `services.py:258-267`), so the exploited/unexploited split participates. The exact Eq 1–2 formula is unrecoverable (spec §q gap) — full conformance cannot be tested beyond these three normative properties. Beyond-paper term: ×2.5 when the vuln is OS-dependent and the host OS mismatches (`services.py:116-117`). |
| IS-TIM-07 | **DIVERGES-DOCUMENTED-NOWHERE** | Zhang's cross-host learning (halve time for vuln *types* exploited on previous hosts) is unimplemented; what exists is a **per-instance** discount — re-exploiting the *same* `Vulnerability` object costs half (`services.py:118-124`) — which cannot express cross-host learning since instances are per-host copies (`Vulnerability.copy`). The per-type form survives only in commented-out code (`services.py:125-130`). |
| IS-TIM-08 | **CONFORMS** | Penalty `exponential_variates(20, 0.5)` on every interrupt (`attack_operation.py:196`), then forced re-scan — SCAN_HOST (network-layer) or SCAN_PORT (application-layer) (`attack_operation.py:228-238`). Trace: every CAUGHT is followed by SETBACK ≈ 20 t/u then the restart phase. Both halves of Brown's intent present. |
| IS-TIM-09 | **CONFORMS** (recorded incoherence) | Code sits on Zhang's seconds-scale: durations 70–110, intervals 200/700, attack actions 5–25. Ho's SDF **2000 ms** is consumed as **2000 sim-units** (`mtd_ai_operation.py:66,95`) — ten trigger intervals — i.e. Ho's millisecond figure imported at Zhang's second scale. The unit incoherence the spec predicted, realised in one live constant. |

## f) MTD–attacker interaction (IS-INT)

| ID | Verdict | Evidence |
|---|---|---|
| IS-INT-01 | **CONFORMS** | Network-layer MTD interrupts any live attack process (`mtd_operation.py:216-225`); cursor cleared (`attack_operation.py:206-208`), restart at SCAN_HOST = forced re-discovery. Trace: "CompleteTopologyShuffle hit the attacker mid-SCAN_PORT … must re-discover … restarting at SCAN_HOST". |
| IS-INT-02 | **CONFORMS** | Application-layer MTD (Service/OS Diversity, Port Shuffle by class) interrupts and forces SCAN_PORT restart (`attack_operation.py:234-238`). Trace: "OSDiversity hit the attacker mid-EXPLOIT_VULN … restarting at SCAN_PORT". |
| IS-INT-03 | **DIVERGES-DOCUMENTED-NOWHERE** (latent) | Brown: User Shuffle blocks *only mid-credential-stuffing*. Code: UserShuffle is `reserve` type and `_interrupt_adversary` handles only network/application (`mtd_operation.py:211-239`) — it can **never** block anything; credential stuffing is an instantaneous check inside SCAN_PORT with no window to interrupt. Latent (not in default set), but the documented narrow-blocking behaviour has no implementation. |
| IS-INT-04 | **CONFORMS** | Zhang's recast: network-layer deployment fails the attack event immediately regardless of phase — unconditional interrupt (`mtd_operation.py:216-218`), penalty, connection lost. |
| IS-INT-05 | **CONFORMS** | Application-layer cannot touch the reconnaissance verbs (`SCAN_HOST/ENUM_HOST/SCAN_NEIGHBOR` excluded, `mtd_operation.py:226-230`) but interrupts the attack verbs and restarts at Phase 1 (SCAN_PORT = Zhang's "Scan Port & Exploit User Credential"). |
| IS-INT-06 | **DIVERGES-DOCUMENTED-NOWHERE** | No MTD-interruption counter exists anywhere; the only per-host abandonment logic is the enumeration-count give-up rule (IS-SCN-04). Zhang's attempts-per-action limit with an interruption threshold is unimplemented (its threshold was unstated anyway). |
| IS-INT-07 | **CONFORMS** | The confusion cost applies on every interrupt via the shared `apply_mtd_interrupt_cost` (`attack_operation.py:161-208`) — penalty + forced re-scan, both restart paths. Trace: 35 catches, 717 t/u total confusion at seed 42/simultaneous. |

## g) Attacker model — scenarios and profile (IS-SCN / IS-ADV)

| ID | Verdict | Evidence |
|---|---|---|
| IS-SCN-01 | **CONFORMS** (vestigial) | The identical-capabilities/two-goals design survives as `network_type` 0/1 plus `TargetNetwork.copy_network` (same generated graph re-tagged, `target_network.py:11-27`). Nothing constructs `TargetNetwork` anywhere in the live tree — consistent with Zhang's narrowing (IS-SCN-06). |
| IS-SCN-02 | **CONFORMS-SUPERSEDED → CONFORMS (Zhang)** | Brown's weakest-host priority is not implemented; host selection sorts by **distance from exposed/pivot** + random tiebreak (`network.py:868-901`, `attack_operation.py:325-329`). That is exactly Zhang's documented simplification (IS-LIM-04), so under precedence the code conforms to the operative (Zhang) intent; Brown's weakest-first rule is the superseded lineage. |
| IS-SCN-03 | **CONFORMS** (via IS-CFL-04 narrowing) | The targeted-scenario *strategy* (attack-only-target / same-level priority) has no live code path: `get_host_id_priority` and `tag_priority` are never called from the attack chain; `network_type == 0` gates only target selection during generation, APE bookkeeping, and give-up protection. Matches Zhang's documented descoping; the remnants are unreachable in `TimeNetwork` (`network_type = 1`). |
| IS-SCN-04 | **CONFORMS** (unit delta) | Give-up threshold 10 (`ATTACKER_THRESHOLD`, `constants.py:106`), applied per host with the target node of a targeted network exempted (`attack_operation.py:346-353`). Delta: the counter ticks per **enumeration** of the host, not per failed exploitation attempt — an enumeration ≈ one attack pass, but a compromised host's re-enumerations also tick. Note: this guard's polarity was restored to Brown's reading in-repo (code comment cites B-ATK-06); the pre-fix inversion never matched any paper. |
| IS-SCN-05 | **UNTESTABLE** ([intent]) | Consistent: no skill differentiation exists (uniform capability). |
| IS-SCN-06 | **CONFORMS** | Only Scenario 1 runs in the time-domain substrate; see IS-SCN-01/03. |
| IS-ADV-01 | **CONFORMS** ([struct]) | All four profile dimensions present as mechanisms (objective = full-network compromise; exploitation; C2/pivot; credentials), none as a configurable parameterisation — exactly the papers' description-not-parameterisation standing. |
| IS-ADV-02 | **CONFORMS** (quantification recorded) | "Enough services" is quantified nowhere in the papers; the code's criterion: a host is compromised when an **exploited service is adjacent to the internal target node** (`host.py:409-420`), where a service counts as exploited when Σ(exploited vuln impact) > `SERVICE_COMPROMISED_THRESHOLD = 7` on the [0, 10] impact scale (`services.py:288-293`, `constants.py:93`). A structural criterion rather than a count — consistent with the vague prose; the concrete threshold + adjacency rule is the undocumented choice the spec row predicted (→ disposition list). |
| IS-ADV-03 | **CONFORMS** | Pivot/C2: `_set_next_pivot_host` (`attack_operation.py:589-602`), reachability grown through compromised chains (`network.py:729-757`), hacker-visible graph = reachable + neighbours (`network.py:952-966`). |
| IS-ADV-04 | **CONFORMS (Zhang side of IS-CFL-02)** | Compromise is never revoked by any MTD (no code path removes from `compromised_hosts`); re-encountering a compromised host re-records control instantly (`attack_operation.py:366-368`); post-MTD reachability recomputed over the *retained* compromised set (`update_reachable_mtd`, `network.py:694-727`). Brown's revocation semantics are absent. The conflict stands for disposition per the spec's instruction. |
| IS-ADV-05 | **CONFORMS** | Compromise yields all host users (`host.py:452-457`); stuffing runs first in SCAN_PORT and compromises without touching any vulnerability (`can_auto_compromise_with_users`, `host.py:143-161`, `attack_operation.py:383-400`). |

## h) Attacker model — procedure (IS-PRC)

| ID | Verdict | Evidence |
|---|---|---|
| IS-PRC-01 | **CONFORMS** | SCAN_HOST discovers exposed endpoints + uncompromised neighbours of compromised hosts, path-checked through the hacker-visible graph (`attack_operation.py:240-293`). Zhang's Scan Host/Enum Host naming intact. |
| IS-PRC-02 | **CONFORMS** | `port_scan` BFS from exposed services, expanding only through exploited services (`host.py:326-351`) — internal services visible only via compromised ones. |
| IS-PRC-03 | **CONFORMS** | Credential stuffing is the first act of SCAN_PORT (Phase 1), exploitation only on its failure (`_do_scan_port`, `attack_operation.py:383-400`). Trace: "no credential reuse — must exploit a vulnerability". |
| IS-PRC-04 | **DIVERGES-DOCUMENTED-NOWHERE** | Brown: one priority stack of all scanned services' vulnerabilities, ordered by RoA. Code: per-service **top-5** by RoA above a threshold (`services.py:258-267`, `SERVICE_TOP_X_VULNS_TO_RETURN = 5`), concatenated in service order sorted by (path-distance-to-target, highest-RoA) **descending** (`host.py:302-324`) — farthest-first, not a global RoA stack. Deliberate-looking (works toward the internal target node); candidate design choice. |
| IS-PRC-05 | **CONFORMS** | On compromise → SCAN_NEIGHBOR, discovered neighbours prepended to the stack (`attack_operation.py:552-587`); visibility expansion via `update_reachable_compromise`. |
| IS-PRC-06 | **CONFORMS** | Exploit failure → BRUTE_FORCE (`_execute_exploit_vuln`, `attack_operation.py:507-520`); success probability scales with compromised-user coverage (`host.py:177-182`, cap `HOST_MAX_PROB_FOR_USER_COMPROMISE = 0.01`); success in any phase compromises the host. |
| IS-PRC-07 | **CONFORMS** | Brute-force failure → ENUM_HOST, next host from the stack (`attack_operation.py:541-550`); interacts with the give-up list as documented. |
| IS-PRC-08 | **CONFORMS** ([struct]) | The native FSM is closed: every `_execute_*` dispatches only to FSM successors; no off-flowchart moves. (The controller-facing `step()` seam is movement-arm surface, out of audit scope.) |

## i) Parameters and configuration (IS-PRM)

| ID | Verdict | Evidence |
|---|---|---|
| IS-PRM-01 | **CONFORMS** (two exceptions) | Brown Table I vs `TargetNetwork` defaults (`target_network.py:6`): hosts 200 ✓, exposed 20 ✓, subnets 20 ✓, layers 5 ✓, services [3, 11] ✓, cross-platform 0.5 ✓, complexity [0.4, 1] ✓, give-up 10 ✓. Exceptions: impact scale [0, 10] not [0, 1] (IS-CFL-07); trigger Uniform(1000, 5000) removed (superseded, IS-TIM-01). |
| IS-PRM-02 | **CONFORMS** (partially checkable) | `TimeNetwork` defaults 50 nodes / 5 endpoints / 4 layers (`time_network.py:10`) = Zhang's 50-node geometry; other geometries constructible by argument. Density values not directly encodable (no density parameter; subnets stand in). |
| IS-PRM-03 | **CONFORMS** (protocol part untestable) | Terminating condition NCR 0.8: `len(compromised)/total > 0.8` (`time_network.py:48-52`; strictly greater-than, so 41/50 not 40/50 — off-by-one nuance recorded). Interval default 200 sits at the top of Zhang's tested 50–200 s. The 100-runs protocol is experiment-harness territory; the original driver was deleted (`experiments/run.py`, see `baseline/run_baseline.py` docstring) — **UNTESTABLE in the substrate**. |
| IS-PRM-04 | **DIVERGES-DOCUMENTED-NOWHERE** (absences) | Ho's finish 15 000 survives only as a tool default (`tools/des_step.py:285`); total nodes 150 is defaulted nowhere (TimeNetwork 50); SDF 2000 present ✓ (unit caveat, IS-TIM-09). Ho's documented **Network Size parameter independent of node count** has no code surface at all — the generator has no size/area input (`snapshot_checkpoint.py`'s "network_size" is a filename key over node count). |
| IS-PRM-05 | **UNTESTABLE** | γ/ε/decay/train-start are caller-supplied constructor arguments (`mtd_ai_training.py:23-25`) with no defaults in the substrate; the training harness that would carry Ho/Tay's values was deleted with the experiments layer. |

## j) Metrics and evaluation (IS-MET) and the AI seam (IS-AI)

| ID | Verdict | Evidence |
|---|---|---|
| IS-MET-01 | **CONFORMS** | Blocked actions counted (`MTDStatistics._total_attack_interrupted`, `mtd_statistics.py:40-41`); attempts per host and cumulative attempts recorded per action row (`attack_statistics.py:24-45`) — Brown's two metrics derivable directly. |
| IS-MET-02 | **CONFORMS** | Checkpoint MTTC = Σ duration of SCAN_PORT/EXPLOIT_VULN/BRUTE_FORCE ÷ their count (`evaluation.py:106-110`), 0-guarded — Ho's mean-duration formula. (A second variant, Σ ÷ compromised-count, coexists in `mean_time_to_compromise_10_timestamp`, `evaluation.py:35-49` — two MTTCs with one name, recorded.) |
| IS-MET-03 | **CONFORMS** | NCR as terminating checkpoint at 0.8 (`time_network.py:48-52`); ratio = compromised/total. |
| IS-MET-04 | **CONFORMS** (three feature deltas) | APE ✓ new-vuln-percent over the shortest path, 0-if-none (`network.py:630-664`). Risk ✓ complexity·impact (`services.py:189-204`). RoA ✓ complexity·impact/exploit-time — AC as time-to-exploit (`services.py:177-187`). HCR ✓ C_t/T_host (`evaluation.py:125-130`). Attack Stage ✓ enum 1–6, default 7 (`mtd_ai_operation.py:64`). MEF ✓ N/(finish−start) (`evaluation.py:72-81`). TSLM ✓ (`mtd_ai_operation.py:352`). Deltas: **ASR** counts attempts as SCAN_PORT events only, not SCAN_PORT+EXPLOIT+BRUTE (`evaluation.py:111-118`); **SAPV** is a path-length delta, not Ho's set difference of consecutive path sets (two further variant formulas coexist: `evaluation.py:174-175`, `mtd_ai_operation.py:327-336`); **NAV** (`ip_variability`) is positional IP comparison normalised by host count (`mtd_ai_operation.py:300-321`) — direction consistent, set construction not Ho's. |
| IS-MET-05 | **UNTESTABLE** (in substrate) | Ho's five-checkpoints → trial-mean → cross-trial-median pipeline, baseline normalisation and equal-weighted score have no surface in `mtdnetwork/`; the checkpoint primitive exists (`evaluation_result_by_compromise_checkpoint`, default nine checkpoints 0.1–0.9, `evaluation.py:83-143`). The pipeline lived in the deleted experiments layer. |
| IS-AI-01 | **CONFORMS** | The AI path deploys **through** the core MTD machinery: same `MTDScheme` registry/queue, same resources, same `_mtd_execute_action` (`mtd_ai_operation.py:44-45, 148-190`) — plugin contract honoured. |
| IS-AI-02 | **CONFORMS** (two caveats) | SDF default 2000 (`mtd_ai_operation.py:24,66`); check runs before the model is consulted, forces a random technique and resets the clock (`mtd_ai_operation.py:95-106`); `TimeNetwork.last_mtd_triggered_time` is the required core-side tracker (`time_network.py:24,66-73`). Caveats: unit mismatch (IS-TIM-09); forced pick draws `randint(1, len+1)` **inclusive**, whose top value indexes past the strategy list → latent IndexError (`mtd_ai_operation.py:96` vs `mtd_scheme.py:103-110`). |
| IS-AI-03 | **CONFORMS (Tay side of IS-CFL-05)** | Action space = len(strategies)+1 Q-outputs, action 0 = no-deploy, k>0 → single technique k−1 (`choose_action`, `mtd_ai.py:51-58`; `_register_mtd_ai`, `mtd_scheme.py:103-110`). With the four live techniques this is exactly Tay's five actions. Ho's pairwise combinations are unimplemented. |
| IS-AI-04 | **CONFORMS** (input-list delta) | Architecture matches Tay layer-for-layer: Dense-128→ReLU→BN→Dense-64→ReLU→BN→Dropout-0.3; LSTM-64(seq)→ReLU→BN→LSTM-32→ReLU→BN→Dropout-0.3; concat→Dense-64→ReLU→BN→Dropout-0.3→Q (`mtd_ai.py:11-44`). Double DQN ✓ (main-net argmax, target-net value, `mtd_ai.py:67-91`; hard and soft target updates both present). Delta: static inputs are {HCR, APE, ASR, RoA, Risk} not Tay's {HCR, #vulns, #exposed vulns, APE}; time-series inputs include SAPV/NAV/attack-type and omit Tay's downtime input (`mtd_ai_operation.py:409-427`). |
| IS-AI-05 | **DIVERGES-DOCUMENTED-NOWHERE** (weights) | Reward = f(N_{t+1}) − f(N_t) ✓ delta-form over features; min-max normalisation against in-memory history ✓; training gated on train-start ✓ (`calculate_reward`, `mtd_ai.py:114-202`; `replay:68-69`). Divergence: weights are **±75 or 0** per feature (`mtd_ai.py:162-179`), not the documented ±1 by direction — and four features are zero-weighted (dropped from reward entirely). |
| IS-AI-06 | **DIVERGES-DOCUMENTED-NOWHERE** (broken below 1.0) | The configurable detection-rate feed exists (`attacker_sensitivity` gates the attack-type feature, `mtd_ai_operation.py:396-400`) — but the failed-draw branch assigns nothing (`current_attack_value` unbound) and the value is consumed unconditionally (`mtd_ai_operation.py:426`), so any sensitivity < 1.0 raises UnboundLocalError on the first failed draw. Tay's 0–100 % sweep is unrunnable against this code as it stands. Candidate bug. |

## k) §o non-features, §p conflicts — where the code actually sits

**Declared non-features (IS-LIM).** All seven hold — no code implements skill levels,
richer confusion, selective deployment, difficulty-aware targeting, QoS effects, or a
second adversary type; target selection is distance-based (IS-LIM-04 confirmed at
`network.py:868-901`). One reading note: MTD "applies to all nodes" (IS-LIM-03) is
systematically narrowed to *all non-exposed nodes* by the exemption in every technique —
a blanket rule, not selective deployment, but worth Marc's eye (D-05).

**Where the code lands on each recorded conflict:**

| Conflict | Code's position |
|---|---|
| IS-CFL-01 (complexity range/polarity) | **Hybrid**: Brown's range [0.4, 1] with Zhang's polarity (higher = easier) — matches neither paper wholly. → disposition D-01. |
| IS-CFL-02 (persistence) | **Zhang**: never revoked, instant re-recognition. Brown's revocation absent. → disposition D-02. |
| IS-CFL-03 (trigger distribution) | **Zhang** (exponential family; see the §e fork). Resolved by precedence. |
| IS-CFL-04 (scenario scope) | **Zhang**: Scenario 1 only; targeted machinery vestigial and unreachable. |
| IS-CFL-05 (AI action space) | **Tay**: singles + no-deploy. Ho's pairwise absent. |
| IS-CFL-06 (technique count) | **Confirmed**: exactly seven pre-DAP techniques implemented (CTS, HostTopology, IP, OS, Port, Service, User) + DAP as the eighth. The seventh beyond Brown's six is **CompleteTopologyShuffle** — Zhang's likely candidate verified in code. |
| IS-CFL-07 (impact range) | **Neither**: [0, 10] (`services.py:27`) vs Brown's [0, 1], no later paper restates. DIVERGES-DOCUMENTED-NOWHERE; the compromise threshold 7 is calibrated to this scale. → disposition D-03. |

## l) Beyond-paper behaviours encountered (no IS-row; recorded for completeness)

Mechanisms with no documented basis in any lineage paper, found while auditing. None
classified — they are outside the spec's rows — but each is a standing undocumented choice:

1. **OS-dependent vulnerabilities**: 80 % chance a cross-platform service's vuln is
   OS-conditional (`VULN_PROB_DEPENDS_ON_OS = 0.8`), costing ×2.5 exploit time on
   mismatch (`services.py:43-47,116-117`).
2. **Dependent vulnerabilities**: 10 % chance a vuln needs an enabler vuln present
   (`services.py:34-38`, `host.py:376-383`).
3. **Exploitability bookkeeping**: `cvss/5.5` seeding and post-compromise halving toward 1
   (`services.py:28-29`, `attack_operation.py:493-501`) — feeds the scorer only.
4. **Per-service top-5 RoA cap** and RoA threshold on vuln disclosure (`services.py:258-267`).
5. **Exposed-endpoint exemption** in IPShuffle (documented: "internal"), PortShuffle,
   OSDiversity, ServiceDiversity, DAP (undocumented for the application-layer four).
6. **Latest-version-only replacement services** in OSDiversity/ServiceDiversity/DAP.
7. **Suspend-or-discard**: a second same-priority instance is discarded, not queued
   (`mtd_operation.py:103-107`).
8. **Dead constants / vestiges**: `VULN_PATCH_MEAN` (unused in the live path),
   `HACKER_ATTACK_ATTEMPT_MULTIPLER` (max-attempts check commented out,
   `attack_operation.py:355-358`), port range `range(1, 65546)` exceeding 65535, IP octets
   drawn 1–256.
9. **DAP re-solve checkpoints**: the MIP re-solves only when the compromise ratio crosses
   0.1–0.7 checkpoints (`osdiversityassignment.py:22-35`).

## m) Post-hoc cross-check against `mtdsim_spec.md` / `metrics_semantics.md`

*Completed after all classifications above were frozen; deltas listed, nothing silently
reconciled. Where the two records disagree about what a **paper** says, the intent spec
wins (built uncontaminated); where they disagree about the **code**, the discrepancy goes
to the disposition list, not into a silent edit of either file.*

**Agreements (strengthen both records).** The two passes agree on: BA/WS generation
(NET-02/03), the [3, 11] services and user constants (NET-06/07), complexity range
[0.4, 1] as a code fact (NET-12/C2), impact [0, 10] + threshold 7 (NET-13/14/C3), NCR 0.8
post-2b (metrics_semantics §b), MTD durations matching Zhang's five time-domain values
(MTD-14), the give-up polarity restoration (ATK-07), the ATK-04a/b split exactly as
metrics_semantics §c states it, persistence sitting on Zhang's side (ATK-06 — and this
audit **closes the prior record's open question**: no code path anywhere removes a host
from `compromised_hosts`), the inert attack cap (ATK-08), distance-based targeting
(ATK-12), the four-active/seven-implemented technique set (MTD-01/C4), scenario-2
unreachability (NET-17 / ATK-07's 2026-07-27 evidence), and the missing final-score
pipeline (MET-17 ↔ IS-MET-05).

**Disagreements with `mtdsim_spec.md` about the code** (for the disposition list, not
reconciled here):

1. **NET-10 vs IS-NET-08 (vulnerability lifecycle).** The prior record marks it
   `verified` on the evidence that `VULN_PATCH_MEAN = 10` / `VULN_PATCH_RANGE = 9`
   *exist*. This audit finds `VULN_PATCH_MEAN` dead in the live generation path and the
   documented introduce-then-patch lifecycle absent (every vuln exists from version 1
   to its patch point). The constants' existence verified the wrong thing. → D-04.
2. **MTD-06 vs IS-MTD-05 (Service Diversity).** Prior record: `verified` (fires in
   goldens). This audit: the *semantics* diverge from Zhang's documented version re-roll
   (random different service, latest version only, exposed hosts exempt). Firing is not
   conformance. → D-05.
3. **ATK-09 vs IS-INT-03 (Brown's three block classes).** Prior record: `verified` —
   "interrupt logic matches Brown's three classes". It matches two of three: User
   Shuffle's class (`reserve`) is unhandled by `_interrupt_adversary`, so Brown's
   blocks-only-mid-credential-stuffing behaviour has no implementation at all. → D-07.
4. **ATK-10 vs IS-INT-06 (interruption threshold).** Prior record verifies the row
   including its "attempt threshold beyond which event fails" clause; no such counter
   exists. The restart behaviour is real; the threshold clause was verified by
   association. → D-09.
5. **MET-15 row is stale.** The prior record's table still shows `0.25 · divergent`
   (and headline risk #1 repeats it); the code has been 0.8 since Phase-2b R1 and
   `metrics_semantics.md` §b records the fix. A doc-maintenance item, not a ruling.

**Paper-side deltas (intent spec wins, per protocol):**

6. **"All seven `MTD_DURATION` entries match Zhang Table 3 verbatim" over-claims**
   (MTD-14 row and metrics_semantics §b both). Zhang's Table 3 documents **five**
   time-domain techniques (CTS, IPShuffle, OSDiversity, DAP, ServiceDiversity —
   IS-TIM-03). The HostTopologyShuffle (100), PortShuffle (70) and UserShuffle (20)
   durations are documented in **no** lineage paper — they are undocumented choices,
   currently latent (techniques not in the default set). The five that Zhang does
   document match verbatim; the claim should be scoped to those five.
7. **C2's framing of Zhang as "imprecise wording" understates the conflict.** The
   intent spec (IS-CFL-01) records Zhang's [0, 1] *and* Zhang's inverted semantics
   (higher = easier) as a real position — and this audit finds the code implements
   **Zhang's polarity** (success probability = complexity; time ∝ 1 − complexity) inside
   **Brown's range**. C2's recommended resolution ("Brown matches code") holds for the
   range only; the semantics side was never checked. → D-01.

**Refinements (same facts, sharper statement):**

8. **C7's "no exponential draw" is imprecise in the letter.** The *base* exploit time is
   deterministic (`services.py:115`), but the call site wraps it in
   `exponential_variates(base, 0.5)` (`attack_operation.py:455-457`) — a location-shifted
   exponential with σ = 0.5. Substantively C7 stands (nothing like Zhang's variance); the
   record should say "near-deterministic (shifted-exponential jitter, σ = 0.5)" rather
   than "no exponential draw". The same construction underlies MTD-11's `verified` —
   which never confronted the σ = 0.5 fork this audit flags as D-08.
9. **MET-02 (ASR)**: the prior record caught the numerator issue (checkpoint target, not
   actual compromises); this audit adds the denominator delta (attempts = SCAN_PORT rows
   only, vs Ho's three event types). Both halves of the formula now have recorded
   deltas. → D-11.
10. **MET-10 (NAV) located.** The prior record left it `unverified` ("likely lives in
    security_metric_statistics"); it lives in `mtd_ai_operation.get_state_and_time_series`
    (`ip_variability`, positional comparison). SAPV likewise has three coexisting variant
    formulas across `evaluation.py` and `mtd_ai_operation.py`, none of them Ho's set
    difference. → D-11 note.
11. **SHD-* rows.** The prior record left the AI seam `unverified` (TF absent). This
    audit's static pass confirms the architecture (SHD-05..08 ↔ IS-AI-04) and turns up
    two candidate bugs the prior record could not reach: the sensitivity-feed crash
    (IS-AI-06 → D-13) and the SDF forced-pick off-by-one (IS-AI-02 → D-14).

## n) Disposition list for Marc

Every DIVERGES-DOCUMENTED-NOWHERE row plus the unresolved conflicts. Nothing here is a
bug until ruled; candidates marked where the evidence leans.

| # | Item | What the code does | What the papers say | Evidence leaning |
|---|---|---|---|---|
| D-01 | **IS-CFL-01** complexity range + polarity | [0.4, 1], higher = easier (success prob = complexity; time ∝ 1−complexity) | Brown: [0.4, 1], higher = harder · Zhang: [0, 1], higher = easier | Hybrid is self-consistent and load-bearing (RoA, exploit time); looks like a design choice, but the polarity inversion silently changes what Brown's 0.4 floor *means* (floor on ease, not difficulty). |
| D-02 | **IS-CFL-02 / IS-ADV-04** persistence | Compromise never revoked; instant re-recognition | Brown: revoke on path disruption · Zhang: keep always | Matches Zhang (operative under precedence), but Zhang never acknowledged the change; ruling requested by the spec itself. |
| D-03 | **IS-CFL-07 / IS-NET-10** impact scale | [0, 10], threshold 7 calibrated to it | Brown: [0, 1]; no later paper restates | **Already ruled** (C3, Phase 2c: keep code [0, 10], document the Brown delta). Audit confirms the facts; no new ruling needed — listed for completeness. |
| D-04 | **IS-NET-08** vulnerability lifecycle | All vulns exist from version 1 until a patch point at draw-index ± 9; no introduction point; `VULN_PATCH_MEAN` dead | Introduced per version, patched ~10 versions later | The outcome Brown wants (older = more vulns) survives; the mechanism does not. Candidate bug *or* simplification — the dead constant suggests drift rather than intent. |
| D-05 | **IS-MTD-05** ServiceDiversity semantics (+ shared latest-version rule, exposed-host exemption — items 5/6 in §l) | Random different service at latest version, non-exposed hosts only | Zhang: re-roll versions from the 99-pool | Latest-only strictly weakens the attacker (fewest vulns) — systematic, looks intended, but inverts Zhang's "diversity space" idea. |
| D-06 | **IS-TIM-07** attacker learning | Per-instance re-exploit discount only (7–42 % of calls per in-repo tests) | Zhang: halve for vuln *types* exploited on previous hosts | **Already ruled** (ATK-04a kept deliberately, Unit C; ATK-04b unimplemented, out of 2c scope). Audit adds one fact: per-type learning is structurally impossible while vulns are per-host copies. Listed for completeness. |
| D-07 | **IS-INT-03** User Shuffle blocking | Can never interrupt (reserve type unhandled); stuffing has no interruptible window | Brown: blocks iff mid-credential-stuffing | Latent (technique not in default set). If User Shuffle is ever re-enabled, this needs a ruling first. |
| D-08 | **IS-TIM-02/04** the exponential fork | All draws = loc + Exp(0.5): mean ≈ µ, σ = 0.5 — near-deterministic | Zhang: "exponential… µ is the historical average" + Table 3 σ = 0.5 | The audit read Table 3's σ = 0.5 as vindicating the shifted construction (only self-consistent reading). If Marc reads µ-as-mean instead, every timing draw in the substrate diverges. This single ruling swings more rows than any other. |
| D-09 | **IS-INT-06** interruption threshold | No interruption counter; give-up counts enumerations | Zhang: attempts limit per action, threshold on MTD interruptions | Absent mechanism; Zhang's threshold value was never stated. Rule whether the enumeration give-up stands in, or the counter is wanted. |
| D-10 | **IS-PRC-04** exploit ordering | Per-service top-5 RoA, services farthest-from-target first | Brown: single global RoA stack | Deliberate-looking (drives toward the internal target); changes which vulns are tried first, so it moves MTTC. |
| D-11 | **IS-MET-04** ASR attempt counting | Attempts = SCAN_PORT events only | Ho: SCAN_PORT + EXPLOIT_VULN + BRUTE_FORCE | One-line delta with direct metric impact; also two coexisting MTTC and three SAPV variants want a canonical pick. |
| D-12 | **IS-AI-05** reward weights | ±75/0; four features zero-weighted | Ho: w_i = ±1 by direction | Magnitude is a free scale (harmless alone); the zero-weights silently drop documented features from the reward. |
| D-13 | **IS-AI-06** sensitivity feed | UnboundLocalError for any sensitivity < 1.0 | Tay: 0–100 % feed, cutoff study at ≈ 0.7 | **Candidate bug** — the documented experiment cannot run; no design reading explains a crash. |
| D-14 | **IS-AI-02** SDF unit + forced-pick bound | 2000 sim-units (= 10 trigger intervals); `randint(1, len+1)` can index past the list | Ho: 2000 **ms**; forced random MTD | Unit: needs a ruling on which scale is meant. Off-by-one: **candidate bug** (latent IndexError). |
| D-15 | **IS-PRM-04** Network-Size parameter | No size/area input independent of node count exists | Ho: Network Size 100/150/200 at fixed 150 nodes (density sweep) | Documented parameter with no code surface — likely lived in the deleted experiments layer; rule whether it is wanted back. |

**Resolved-by-precedence (no ruling needed, listed for the record):** IS-CFL-03
(exponential replaces uniform — documented), IS-CFL-04 (Scenario 1 only — documented),
IS-CFL-05 (code sits on Tay's side), IS-CFL-06 (seventh technique = CompleteTopologyShuffle,
verified).
