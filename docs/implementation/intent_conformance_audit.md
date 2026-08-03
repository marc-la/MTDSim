---
status: audit record
created: 2026-07-28
updated: 2026-08-02
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

**The tallies above are the 2026-07-28 original.** Three rows have since been revised in
place with dated annotations and are not re-counted: IS-MTD-08 (2026-07-29, was
CONFORMS-latent → DIVERGES-DOCUMENTED-NOWHERE, §m3 → D-17), IS-MTD-06 (2026-08-02,
was CONFORMS (delta) → DIVERGES-DOCUMENTED-NOWHERE, → D-18), and **IS-PRC-01**
(2026-08-02, was CONFORMS → **split by arm**: CONFORMS native,
DIVERGES-DOCUMENTED-NOWHERE for the movement arm, → D-28). IS-MTD-05 additionally
carries a 2026-08-02 fixed-status annotation (its divergence was ruled a fix, D-05,
2026-07-29) — verdict unchanged, evidence brought up to date; IS-MTD-01, IS-NET-11 and
IS-PRC-06 carry 2026-08-02 evidence extensions with verdicts unchanged.

**A scope note the audit's own method line now needs.** The 2026-07-28 audit
"targets the **native substrate arm** only", treating the movement arm's carve-outs
as movement-layer policy rather than substrate divergences. IS-PRC-01 is the first
row where that boundary does not hold: the divergence is in a **shared verb core**
(`_do_enum_host` has no reachability guard), and it is invisible in the native arm
only because the native FSM's control flow happens to compensate. A native-arm-only
audit cannot see this class of defect. Rows whose invariant is enforced by
succession rather than by a guard should be re-read against both arms.

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
| IS-NET-11 | **CONFORMS** (config), **delta added 2026-08-02** | `USER_TOTAL_FOR_EACH_HOST = 5`, `USER_PROB_TO_REUSE_PASS = 0.05` (`constants.py:59-61`); reuse drawn per user at network level (`network.py:687-690`), fuelling credential stuffing. **Delta (boundary review 1):** the *realised* account count per host is not 5. `users` is a dict built from `random.choices` (`network.py:947`), so duplicate names collapse and hosts routinely carry 4; and `Host.total_users` — the field the brute-force divisor reads — counts only to the first password-reusing account (`host.py:478-494`), differing from `len(users)` on 12 of 50 hosts, live-verified. The constant conforms; the count the code acts on does not → **D-26**. |
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
| IS-MTD-01 | **CONFORMS** (verdict unchanged; evidence extended 2026-08-02) | New random IP for every host **except exposed endpoints** (`ipshuffle.py:14-25`) = Brown's "all internal hosts". Interrupt semantics network-layer (§f). **Extension (boundary review 1):** Brown's clause "interrupts any attacker operating with a **stale IP**" is the only text in the lineage predicating anything on the attacker holding an IP, and it is **unimplemented** — the attacker addresses hosts by node id and reads `host.ip` on no path, in either driving arm (instrumented census; and one IPShuffle firing changes *nothing* in the attacker's readable projection). This is **not** a divergence: Zhang documentedly recasts the interaction as class-based (IS-MTD-09, IS-INT-04 — network-layer MTD fails the attack event immediately, no staleness predicate), so by the precedence rule §b(1) the class-based rule is operative and the code implements exactly it. `host.ip` is also not an unread vestige: it feeds Ho's **NAV** metric and the RL defender's state vector (`mtd_ai_operation.py:305-322, 436`; `mtd_ai_training.py:251`), i.e. IS-MET-04. Evidence in [`attacker_read_surface.md`](attacker_read_surface.md) §(f) finding 1. |
| IS-MTD-02 | **CONFORMS** (delta) | `portshuffle.py`: reassigns every service node's port on every **non-exposed host** (target node excepted). Brown says "all exposed services"; code exempts exposed *hosts* entirely (in-code justification comment) and shuffles all services on the rest. Latent (not in default set). |
| IS-MTD-03 | **CONFORMS** | `usershuffle.py`: re-draws each host's users from the network user list. Its *blocking* behaviour diverges — see IS-INT-03. |
| IS-MTD-04 | **CONFORMS** | Same-layer host swap (`hosttopologyshuffle.py:29-55`), pairs drawn within `host_id_list_in_layer`; the same-layer constraint is enforced, exposed endpoints exempted (undocumented but consistent with layer 0 = endpoints). Latent (not in default set). Adversary id-keyed state remapped on swap (`adversary.py:28-60`). |
| IS-MTD-05 | **DIVERGES-DOCUMENTED-NOWHERE** (ruled a fix via D-05, 2026-07-29; annotated 2026-08-02) | Zhang (operative): re-configure services **with different versions** — the 99-version pool as diversity space. Code: replaces each service with a **random different service at its latest version** (`servicediversity.py:13-27` → `get_random_service_latest_version`, `services.py:371-385`), and skips exposed hosts. No draw from the version pool; latest-only replacement systematically *reduces* vulnerability count (newest versions carry fewest). Deliberate-looking, self-consistent — candidate design choice, not obviously a bug. *(Annotated 2026-08-02, boundary review 2: the evidence to the left describes the pre-fix behaviour, retained as the record that led to D-05. Marc ruled the fix 2026-07-29 and it landed — the executing path now draws a random compatible service at a **random version** (`servicediversity.py:18-30` → `get_random_service`, `services.py:355-369`), goldens re-baselined per `baseline/CHANGELOG.md`. Write set re-verified live 2026-08-02: 331/331 non-target services redrawn on the default geometry, exposed endpoints exempt, ports and addressing untouched — [`mtd_write_surfaces.md`](mtd_write_surfaces.md).)* |
| IS-MTD-06 | **DIVERGES-DOCUMENTED-NOWHERE** (revised 2026-08-02, was CONFORMS (delta) — the prior verdict was reached without the always-replace behaviour in view) | The OS half conforms: new OS drawn randomly from the four types (`osdiversity.py:22-29`). The service half does not: the compatibility guard can never pass, because `service_is_compatible_with_os` (`services.py:387-402`) tests a `Service` **instance** for membership in a list of service-name **strings**, and `Service.__eq__` (`services.py:304-307`) returns `False` for any non-`Service` operand. Verified live 2026-08-02 (0 True in 600 checks; a service drawn from `get_random_service(os, version)` fails against its **own** OS and version, while the name-based membership a repaired test would use returns True). The `if not compatible` branch (`osdiversity.py:36-44`) therefore always fires: **every** non-target service on every non-endpoint host is replaced on every trigger, so the spec's "services **incompatible with the new OS** are also randomly changed" selectivity does not exist in the executing path — the mechanism is ServiceDiversity plus an OS relabel, and the relabel reaches the movement attacker through nothing (success gate inherited commented-out, `services.py:146-148` → D-19; ×2.5 time term declined by the movement layer via `charge_time=False`, S3-R as documented). Measured consequence: indistinguishable from ServiceDiversity against the movement attacker in experiment 2's own interval report and in the 2026-08-02 family sub-study (evidence in `../handoffs/2026-08-02_os_service_diversity_indistinguishability.md`). Prior deltas still stand: exposed hosts exempted; OS *version* keeps the previous version's index (latest-version replacement since fixed by D-05). → D-18. |
| IS-MTD-07 | **CONFORMS** | `completetopologyshuffle.py:15-27`: full `gen_graph()` regeneration with host instances re-attached — Ho's "preserving the hosts" addendum implemented literally. |
| IS-MTD-08 | **DIVERGES-DOCUMENTED-NOWHERE** (revised 2026-07-29, was CONFORMS-latent — see §m3) | `osdiversityassignment.py`: the MIP *scaffolding* matches Zhang's documented abstraction (single-source/single-destination reduction, endpoints + database as client classes), but the formulation is decoupled: the assignment binaries `s` appear in no objective term and in exactly one constraint (one-variant-per-node), because the `s`↔`f` coupling constraints — the docstring's own constraint 7 — are commented out (`osdiversityassignment.py:229-233`). CBC presolve reduces every instance to "0 rows, 0 columns — nothing to do"; the returned assignment is an arbitrary feasible point, so the mechanism does not solve the DAP it is documented to solve. Full evidence and disposition options in §m3 → D-17. Reuses OSDiversity's name for duration/priority lookup → inherits 80 s, matching Zhang's DAP_OSDiversity 80 s. |
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
| IS-PRC-01 | **CONFORMS for the native arm; DIVERGES-DOCUMENTED-NOWHERE for the movement arm** (split 2026-08-02, boundary review 1 — was CONFORMS) | SCAN_HOST discovers exposed endpoints + uncompromised neighbours of compromised hosts, path-checked through the hacker-visible graph (`attack_operation.py:240-293`). Zhang's Scan Host/Enum Host naming intact. **The split:** the "**only if a path exists**" invariant is enforced by *control flow*, not by a guard. SCAN_HOST filters on it (`:285`); ENUM_HOST does not re-check — `sort_by_distance_from_exposed_and_pivot_host` (`network.py:868-901`) only sorts, giving an unreachable host `LARGE_INT` and popping it anyway (`:333-379`). The native FSM is saved by its forced post-interrupt `_scan_host()` (`:228-233`), which rebuilds the stack (measured: **0 of 873** pops outside the visible graph, 20 runs). The movement driver owns succession and declines to re-impose it by design (`attacker.py:456-482`), so the stack is never flushed: **9.7 %** of pops undefended and **22.4 %** defended target a host with *no path* from any exposed endpoint (10 seeds each). The guard is missing from a **shared verb core**, so a repair reaches both arms automatically. Evidence in [`attacker_read_surface.md`](attacker_read_surface.md) §(f) finding 5 → **D-28**. |
| IS-PRC-02 | **CONFORMS** | `port_scan` BFS from exposed services, expanding only through exploited services (`host.py:326-351`) — internal services visible only via compromised ones. |
| IS-PRC-03 | **CONFORMS** | Credential stuffing is the first act of SCAN_PORT (Phase 1), exploitation only on its failure (`_do_scan_port`, `attack_operation.py:383-400`). Trace: "no credential reuse — must exploit a vulnerability". |
| IS-PRC-04 | **DIVERGES-DOCUMENTED-NOWHERE** | Brown: one priority stack of all scanned services' vulnerabilities, ordered by RoA. Code: per-service **top-5** by RoA above a threshold (`services.py:258-267`, `SERVICE_TOP_X_VULNS_TO_RETURN = 5`), concatenated in service order sorted by (path-distance-to-target, highest-RoA) **descending** (`host.py:302-324`) — farthest-first, not a global RoA stack. Deliberate-looking (works toward the internal target node); candidate design choice. |
| IS-PRC-05 | **CONFORMS** | On compromise → SCAN_NEIGHBOR, discovered neighbours prepended to the stack (`attack_operation.py:552-587`); visibility expansion via `update_reachable_compromise`. |
| IS-PRC-06 | **CONFORMS** (verdict unchanged; delta added 2026-08-02) | Exploit failure → BRUTE_FORCE (`_execute_exploit_vuln`, `attack_operation.py:507-520`); success probability scales with compromised-user coverage (`host.py:177-182`, cap `HOST_MAX_PROB_FOR_USER_COMPROMISE = 0.01`); success in any phase compromises the host. **Delta (boundary review 1):** the coverage denominator is `Host.total_users`, which is not the account count → **D-26**. Measured consequence is small — 488 BRUTE_FORCE calls over 60 runs produced 1 compromise, none in any defended arm — so the phase conforms in shape and is very nearly inert in effect. |
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
   mismatch (`services.py:43-47,116-117`). *(Annotated 2026-08-02: the time term is
   the **only** live expression of OS dependency. The success gate in
   `Vulnerability.network()` that would return 0.0 on OS mismatch is inherited
   commented-out code (`services.py:146-148`), so `vuln_os_list` is populated for
   most vulnerabilities and never consulted for success — exploitation succeeds on
   `complexity` alone. The movement arm additionally declines the time term
   (`charge_time=False`, S3-R). Whether the gate is separately dispositionable is
   → D-19.)*
2. **Dependent vulnerabilities**: 10 % chance a vuln needs an enabler vuln present
   (`services.py:34-38`, `host.py:376-383`).
3. **Exploitability bookkeeping**: `cvss/5.5` seeding and post-compromise halving toward 1
   (`services.py:28-29`, `attack_operation.py:493-501`) — feeds the scorer only.
4. **Per-service top-5 RoA cap** and RoA threshold on vuln disclosure (`services.py:258-267`).
5. **Exposed-endpoint exemption** in IPShuffle (documented: "internal"), PortShuffle,
   OSDiversity, ServiceDiversity, DAP (undocumented for the application-layer four).
   *(Annotated 2026-08-02, boundary review 2: live-verified — zero endpoint writes
   for all five; UserShuffle carries **no** exemption, which conforms to
   IS-MTD-03's "each host"; CompleteTopologyShuffle moves endpoint adjacency while
   preserving the endpoint hosts. Put to Marc as **D-23**; evidence in
   [`mtd_write_surfaces.md`](mtd_write_surfaces.md) §b1. Ruled keep-and-document
   2026-08-03 — see the D-23 ruling banner in the disposition list.)*
6. **Latest-version-only replacement services** in OSDiversity/ServiceDiversity/DAP.
   *(Stale as of D-05, 2026-07-29: all three now draw `get_random_service` — a
   random compatible service at a random version. Retained as the pre-fix record.)*
7. **Suspend-or-discard**: a second same-priority instance is discarded, not queued
   (`mtd_operation.py:103-107`).
8. **Dead constants / vestiges**: `VULN_PATCH_MEAN` (unused in the live path),
   `HACKER_ATTACK_ATTEMPT_MULTIPLER` (max-attempts check commented out,
   `attack_operation.py:355-358`), port range `range(1, 65546)` exceeding 65535, IP octets
   drawn 1–256.
9. **DAP re-solve checkpoints**: the MIP re-solves only when the compromise ratio crosses
   0.1–0.7 checkpoints (`osdiversityassignment.py:22-35`).
10. **Per-registration re-instantiation defeats per-instance state** (found by the
    2026-07-29 cost audit): `MTDScheme._mtd_register` does
    `if isinstance(mtd, type): mtd_strategy = mtd(network=self.network)` — a fresh
    instance every registration — so any state a mechanism carries across mutations
    (`OSDiversityAssignment.last_result` / `_checkpoint`, `ServiceDiversity.shuffles`)
    resets every cycle. Measured: `objective()` ran 75 times per 15 000 s run where the
    checkpoint ladder intends ≤ 8. No lineage paper says anything about mechanism
    lifecycle, so there is no IS row to diverge from — but the code's own checkpoint
    design presupposes persistence, making this an internal defect rather than a
    candidate design choice. **Fixed 2026-07-29** under the cost-audit handoff's
    direction (per-scheme instance cache in `_mtd_register`); golden movement streams
    verified bit-identical for the seven stateless mechanisms, with
    `OSDiversityAssignment`'s change expected-and-explained (the cache now works, so
    solves happen at the documented checkpoints only).

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

## m2) Re-examination against the recovered figures and equations (2026-07-29)

Marc supplied five artefacts the audit had recorded as unrecoverable (intent spec §q):
**Brown Fig 3**, **Zhang Figs 1, 4, 7**, and **Zhang Eqs 1–2**. Every row that had been
classified against prose reconstructions of these was re-examined. The paper-side content
is folded into the intent spec (rows + the §j transcriptions); the code-side verdicts are
below. **Four rows move, and one of them reverses a long-standing disposition.**

**The headline: C7/ATK-03 was wrong, and the code is more faithful than recorded.**
Eq 2 reads `T_Aphase2 = [ Σ_{V_unexploited} (1 − AC_vi) + Σ_{V_exploited} (1 − AC_vj)/2 ] ·
T_Aexploit`. The code's per-vulnerability cost is `exponential_variates((1 − complexity) ·
ATTACK_DURATION['EXPLOIT_VULN'], 0.5)` summed over the attempted list — which is Eq 2's
unexploited half **term for term**, with `T_Aexploit` = 15 and §4.5's exponential as the
wrapper. The three properties `metrics_semantics.md` §c called missing (exponential form,
ACv-dependence, the exploited/unexploited split) are all present. That record was built
while the equation images were missing from the source conversion; it has been corrected
in place.

**What genuinely diverges, measured rather than argued.** An entry-state spy on
`exploit_time`, tagged by call site, over the no-MTD golden (seed 1234):

| call site | entry `exploited` | calls |
|---|---|---|
| `roa()` | False | 56 486 |
| `roa()` | **True** | **2 905** |
| `_do_exploit_vuln()` | False | 1 183 |
| `_do_exploit_vuln()` | **True** | **0** |

So Eq 2's `/2` term fires 2 905 times a run and **never once on the duration path** —
`Service.get_vulns` filters exploited vulnerabilities out before the timing loop, leaving
the discount to act on RoA *ordering* instead. Eq 2 would charge those vulnerabilities at
half cost as part of phase 2; this substrate charges nothing for them. That is the whole
of the residual C7, and it becomes **D-16**. (Second, smaller: Eq 2 multiplies one
`T_Aexploit` by the bracket, the code draws per-vulnerability — same expectation, n×
the variance.)

**IS-SCN-02 / ATK-12 re-attributed — Brown contradicts his own prose.** Fig 3 box 2 is
annotated *"prioritises internal hosts that minimise the time it takes for the adversary
to move to a compromised host to target it"*. Distance-to-foothold selection is therefore
**Brown's implemented procedure**, not Zhang's simplification of it; §III-C(1)'s "weakest
host" prose describes a rule his own figure does not. The audit had classified this row
CONFORMS-SUPERSEDED→CONFORMS(Zhang); it is now **CONFORMS (Brown, directly)**, and Zhang's
§6.3 "simplification" is a restatement. Nothing in the code changes — but the substrate's
target selection is now traceable to the primary source rather than to a later concession.

**IS-TIM-07 relocated.** Eq 2 shows the "halving for previously exploited vulnerabilities"
is not a separate learning discount at all — it is the `/2` on Eq 2's `V_exploited` sum,
i.e. the same rule as IS-TIM-06. The prior record's framing of ATK-04a as a Brown-era
mechanism "not Zhang's" is therefore wrong on attribution: the Brown-era commit
implemented Zhang's idea. What survives, and matters more, is the measurement above —
the discount does not shift MTTC magnitude, because it never reaches a duration.

**Rows confirmed exactly (no change, now on figure evidence rather than prose):**

| Row | Recovered artefact | Verdict |
|---|---|---|
| **IS-INT-01/02/04/05** — the conditional interrupt | **Zhang Fig 7** | **Exact.** The figure's green enclosure spans every action and returns to Scan Host; the orange spans only Phases 1–3 and returns to Phase 1. The code's `_interrupt_adversary` gates application-layer interrupts on `curr_process not in {SCAN_HOST, ENUM_HOST, SCAN_NEIGHBOR}` and recovers at SCAN_PORT, network-layer unconditionally recovering at SCAN_HOST. The exclusion set **is** the complement of the orange box. This is the seam Marc flagged; it matches the figure box for box. |
| **IS-SCH-01** — register/trigger flow | **Zhang Fig 4** | **Exact**, including the conditional: registration happens *only* when the MTD queue is empty, and the suspension queue is drained in preference to the main queue. `_mtd_trigger_action`'s three statements are the figure's three decision nodes in order. |
| **IS-ARC-01** — module structure | **Zhang Fig 1** | **Exact**, and the figure elevates the interrupt path: `MTD Operation → Attack Operation` labelled *"interrupt attack actions"* is one of only three labelled edges, alongside resource retrieve/release and discover/compromise. All three are present as distinct code seams. |
| **IS-PRC-01..08** — the attack procedure | **Brown Fig 3** | **Exact on all ten boxes and every arrow**, including the two the prose did not carry: box 9 (Scan Neighbours) returns to box 2 (pick from stack), matching `_execute_scan_neighbors → _enum_host`; and box 10 is the only route back to box 1, matching `_enum_host`'s empty-stack re-route to `_scan_host`. |

**One tension recorded, not resolved.** Fig 3 draws box 4 (credential-reuse check) → box 5
unconditionally, with no success branch; §III-C(2)'s prose says exploitation is reached
only on stuffing's *failure*, and the code short-circuits to SCAN_NEIGHBOR on a reuse hit.
Prose is the more specific statement and the code follows it; the figure is silent rather
than contradictory. No action.

**A dead computation noticed while checking Fig 3 box 5.** `Host.get_vulns` accumulates
`discovery_time` from `service.discover_vuln_time(...)` and never returns or charges it —
`SERVICE_DISCOVER_EACH_VULN_TIME = 10` is inert. Brown draws vulnerability discovery as its
own step (box 5, distinct from box 6's exploitation), which might suggest a missing cost —
but **Eq 2 settles it the other way**: phase-2 duration is the exploit sum alone, with no
discovery term. The variable is dead code, not a missing charge. Recorded in §l, no fix.

## m3) The MTD mechanism cost audit (2026-07-29) — IS-MTD-08 re-examined

The per-mechanism cost audit (`docs/handoffs/2026-07-29_mtd_mechanism_cost_audit.md`;
cost table in [`mtd_mechanism_costs.md`](mtd_mechanism_costs.md)) profiled
`OSDiversityAssignment` at ~128 s per movement run — 1367× the no-MTD baseline —
and the profile led back into the formulation itself. One verdict moves.

**IS-MTD-08 revised: CONFORMS (latent) → DIVERGES-DOCUMENTED-NOWHERE.** The original
audit verified the *scaffolding* (the single-source/single-destination reduction,
the client classes, the PuLP MIP) and stopped there. The cost profile forced a read
of the formulation, which shows the solve is degenerate:

1. **The assignment variables decide nothing.** The binaries `s[(variant, node)]` —
   the thing the Diversity Assignment Problem exists to choose — appear in **no
   objective term** and in exactly **one** constraint (one-variant-per-node,
   `osdiversityassignment.py:209`). The objective and every live constraint range
   over the flow variables `f` alone.
2. **The coupling is commented out.** The constraints that would tie `s` to `f` —
   constraint 7 in the file's own docstring, *"the amount of flow out of / into a
   routing node must be 0 if that node is compromised"* — sit disabled at
   `osdiversityassignment.py:229-233`. As written they were never runnable anyway:
   they apply Python's `min()` to a list of `LpVariable`s, which is not a linear
   construct PuLP can express — evidence this is an **unfinished implementation**,
   not a switched-off feature.
3. **The solver confirms it.** CBC's log on every solve of every run: `processed
   model has 0 rows, 0 columns … No integer variables - nothing to do` — presolve
   annihilates the model. The returned assignment (measured: 42 `(variant, node)`
   pairs on a fresh 50-node network) is whatever one-hot completion CBC's postsolve
   emits — arbitrary, though deterministic for a given alive-node set.
4. **Two further formulation defects**, folded into the same disposition:
   line 222 sums a variable with a *constraint object* inside one `lpSum` (the
   docstring's constraint 6 — whatever the expression evaluates to, it is not that
   constraint); and the constraints at lines 218/220 re-bind the loop variable `a`
   in their own comprehensions, so each is emitted identically once per outer
   `(c, a)` pair — redundant rows that inflate the 243 000-line MPS file the
   mechanism serialises 75 times per run.

Zhang §4.3.1.5 documents the objective *and constraint* functions as taken from the
cited DAP literature (Newell et al.); a formulation whose constraints cannot bind the
assignment matches no paper's documented intent. Per §c this is a **candidate bug**
(evidence leans *unfinished implementation* — the lineage may never have completed
it), and only Marc's disposition makes it fixable → **D-17**.

**Also examined, no verdict change:**

- **IS-MTD-07 (Complete Topology Shuffle, 13.5× no-MTD)** — the cost *is* the
  documented mechanism: `gen_graph()` full regeneration per mutation is exactly what
  Zhang documents (with Ho's host preservation). The two scorer calls in its
  `mtd_operation` (`add_shortest_path`; `add_attack_path_exposure` is gated to
  network-type 0 and never runs in the time-domain arm) are measurement feeds (SAPV),
  deterministic and a negligible share of the 17 ms/mutation. **CONFORMS stands.**
- **IS-INT-03 (User Shuffle, 0 interrupts in the cost table)** — answered with
  evidence, not a regression: under the D-07 fix the reserve class interrupts only
  mid-`BRUTE_FORCE` (Brown's narrow blocking condition). Across the six golden
  movement runs the attacker spends 1.2–1.6 % of sim time in `BRUTE_FORCE`, so at
  75 mutations/run the expected interrupt count is ≈ 1: seeds 0–1 drew 0, seed 2 drew
  exactly 1 in both arms (landing on a `BRUTE_FORCE` completion, verified in the
  golden streams). The handoff's zero was a small-sample outcome of the documented
  narrow gate. **CONFORMS (Brown) stands; no disposition needed.**

## n) Disposition list — ruled 2026-07-29

> **Status.** Marc ruled on this list 2026-07-29: *"I approve any changes required,
> please implement comprehensively … fix any bugs that have surfaced or deviations
> that you have spotted"*, with the Tay AI-seam integration (h5 model loading)
> explicitly deferred a few weeks. Outcome per item:
>
> - **Fixed (commit of this note, goldens re-baselined — see `baseline/CHANGELOG.md`
>   2026-07-29):** D-05 (diversity version re-roll), D-07 (User Shuffle blocks only
>   mid-credential work, recovers to EXPLOIT_VULN), D-10 (global RoA stack), D-11
>   (ASR numerator + denominator to Ho's formula), D-13 (sensitivity else-branch →
>   "no information" value 7), D-14 (SDF forced pick bounded to the strategy list).
> - **Kept, no change — and why:** D-01 (the hybrid matches Zhang's polarity inside
>   Brown's range; moving either direction contradicts one paper — needs a
>   PDF-level ruling); D-02 (Zhang's persistence is operative under precedence);
>   D-04 (a literal introduce-then-patch lifecycle would *break* IS-NET-07's
>   older-more-vulns and IS-NET-09's every-version zero-day — Brown's three
>   statements cannot all hold under a sliding window, so this needs the original
>   Fig-3-era text, not a guess); D-08 (the µ-as-location reading is the only one
>   consistent with Zhang's own Table 3 σ = 0.5; kept as the operative reading);
>   D-09 (Zhang never states the threshold value — implementing it means inventing
>   a constant, which the guardrails forbid).
> - **Already ruled previously, confirmed only:** D-03 (C3/2c), D-06 (Unit C).
> - **Deferred with the AI seam / experiment harness:** D-12 (reward weights),
>   D-15 (Network-Size parameter), plus the SDF *unit* question inside D-14 and
>   the SAPV/NAV variant formulas inside D-11's note.
>
> The original list is retained below unchanged, as the record of what was put to
> Marc. Candidates marked where the evidence leaned.

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

### Opened 2026-07-29 by the recovered equations — awaiting Marc

| # | Item | What the code does | What Zhang's Eq 2 says | Recommendation |
|---|---|---|---|---|
| **D-16** | **Eq 2's `V_exploited` half is not charged into phase-2 duration** | Only unexploited vulnerabilities are attempted and timed; the `/2` branch never reaches the duration path (0 of 1 183 timing calls, measured — it fires 2 905 times inside `roa()` instead, affecting ordering) | Phase-2 cost sums over the service's **whole** list `V`, with already-exploited vulnerabilities contributing `(1 − AC_v)/2` each | **Ask before implementing.** Charging time for vulnerabilities the adversary is *not* attempting is a modelling claim (that re-establishing known access costs something), not an obvious repair — and it lengthens every revisit, so it re-baselines the goldens again. My reading is that Zhang intends exactly that, but this is your call, and it is the last substantive gap between this substrate and her published formula. |
| D-16b | *(same fix, second half)* the exponential is drawn **per vulnerability** rather than once per phase | n draws of σ = 0.5 | one `T_Aexploit` scaling the whole bracket | Cosmetic in expectation, n× in variance. Worth folding into D-16 if D-16 is taken; not worth a change on its own. |

### Opened 2026-07-29 by the mechanism cost audit — awaiting Marc

| # | Item | What the code does | What the papers say | Options, costed |
|---|---|---|---|---|
| **D-17** | **IS-MTD-08** the DAP formulation is decoupled (§m3) | 128 s/run building + solving a MIP whose presolve deletes it; the returned OS assignment is CBC postsolve's arbitrary one-hot completion, deterministic per alive-node set | Zhang §4.3.1.5: solve the DAP — maximise expected client connectivity over OS-variant assignment, objective + constraints from Newell et al. | **(a) Repair** — write constraint 7 fresh (the commented lines were never functional); most faithful to the cited DAP; the real MIP is *slower still* (binaries stop being presolved away; 60 544 flow variables × 168 binaries), needs formulation work + re-baselining of every OSDA stream. Days of work, and the mechanism stays the grid's cost ceiling. **(b) Replace** — drop the solver and assign what today's path effectively assigns; ~1000× faster and honest about being a heuristic; **not automatically stream-identical** (the postsolve completion is arbitrary-but-deterministic; a replacement matches it only if CBC's completion rule is reverse-engineered and pinned, otherwise streams move and OSDA-dependent results re-baseline). **(c) Withdraw** from the pool and record why — zero work, already outside the default set; the demonstration-arms grid is the only published consumer. Ranked recommendation: **(c) ≥ (b) ≫ (a)** for the dissertation's purposes — (a) only if the DAP is to carry evidential weight, which nothing currently published needs. |

**Interim relief regardless of ruling** (shipped with the cost audit): the
re-instantiation fix (§l item 10) restores the checkpoint ladder, so OSDA solves at
most 8 times per run instead of 75 — ~128 s → ~4–15 s — without touching the
formulation question. The D-17 ruling decides what the solve *means*, not whether
the cache works.

### Opened 2026-08-02 by the OS/Service Diversity indistinguishability brief — awaiting Marc

Found while cross-examining the axis-6 redesign; full evidence, the measured
consequence (OS Diversity and Service Diversity indistinguishable against the
movement attacker in two independent data sets) and the companion zero-risk
reporting decision (decision C — the defence family's cardinality in
`pipeline/ogasp/experiment_02_findings.md` §9, with drafted wording) live in
[`../handoffs/2026-08-02_os_service_diversity_indistinguishability.md`](../handoffs/2026-08-02_os_service_diversity_indistinguishability.md).
Neither behaviour has been touched; no recorded conclusion separates the two
mechanisms, so neither ruling corrects a claim.

| # | Item | What the code does | What the papers say | Options, costed |
|---|---|---|---|---|
| **D-18** | **IS-MTD-06** the compatibility test is inert, so OS Diversity always replaces every service (decision A of the brief) | `service_is_compatible_with_os` tests a `Service` instance for membership in a list of name **strings**; `Service.__eq__` rejects non-`Service` operands, so it can never return True (verified live: 0 of 600 checks, including a service against its own OS/version). The guard branch always fires: every non-target service on every non-endpoint host is replaced on every trigger — ServiceDiversity plus an OS relabel | Brown §III-B(6) / Zhang §4.3.1.4: only services **incompatible with the new OS** are also randomly changed | The comparison itself cannot be a design choice in any reading (a type-mismatched test that is False in every reachable state); only the *behaviour it produces* could be — "replace all services" is IS-MTD-05's operative reading and the mechanism is self-consistent under it. **(a) Repair** the test (name-based membership, which verifies True live) so the mechanism becomes selective as documented — makes OS Diversity **less** aggressive than today, moves every golden that includes it; D-05 procedure (deliberate re-baseline, `baseline/CHANGELOG.md`, SIM-05), plus the regression test the brief's gate 5 names (`service_is_compatible_with_os` returns **True** for a service against its own OS and version). **(b) Keep** and record as a documented divergence — zero code risk; the two diversity mechanisms remain one mechanism against the movement attacker and the reporting carries the decision-C qualification. Precedent: the sibling row IS-MTD-05 was the same shape ("deliberate-looking, self-consistent") and Marc ruled it a fix (D-05, 2026-07-29). Either way, no recorded experiment is re-run. |
| **D-19** | **The commented-out OS success gate** in `Vulnerability.network()` (decision B of the brief) | The gate that would return 0.0 when `host.os_type not in vuln_os_list` is inherited commented-out code (`services.py:146-148`); success depends on `complexity` alone, so `vuln_os_list` (populated at p = 0.8) is never consulted for success | **No IS-ID covers it.** The literature check is done: the intent spec contains no OS-dependent-exploitation row at all — OS-dependent vulnerabilities are beyond-paper throughout (§l item 1), and IS-TIM-06 records the ×2.5 time term as a beyond-paper addition | **Not uncommented on this brief's authority.** Uncommenting would *add* an undocumented mechanism, not restore a documented one — no lineage paper documents OS-gated exploitation failure, so the ×2.5 time penalty is the only expression of OS mismatch on any record, and the gate reads as an abandoned alternative to it. It would also change exploit semantics for **both** arms, move every golden, and give the diversity family a second channel that could separate OS Diversity from Service Diversity — a substrate re-design, not a repair. Recommendation: **leave commented and record** (this row is that record); revisit only if a genuine OS-exploitation channel is ever wanted, as its own designed change with a fresh comparability argument. |

### Opened 2026-08-02 (boundary review 2 — the defender write side)

Full evidence — the per-mechanism write-set enumeration, the live-verified
diffs (seed 42, one firing per mechanism) and the purview/fairness table —
lives in [`mtd_write_surfaces.md`](mtd_write_surfaces.md); the review brief is
[`../handoffs/2026-08-02_boundary_network_defender_integration.md`](../handoffs/2026-08-02_boundary_network_defender_integration.md).
Numbering follows boundary review 3's concurrent allocations (D-20..D-22,
same day). Nothing was touched; D-23 asks for a decision on standing
behaviour, D-24 and D-25 are record-grade.

> **Ruled 2026-08-03 (Marc) — all three as recommended.** **D-23: (a) keep and
> document.** The ruling's rationale, in substance: the exposed endpoints are
> not the problem — attackers perform passive reconnaissance continuously, so
> the fixed entry surface is the model's way of granting the attacker its
> foothold, and the game this evaluation plays is disrupting the attacker at
> the discovery level, post-ingress. The exemption is therefore the
> *documented* model of the defence family from here on (this row is that
> record), stated in reporting beside decision C's cardinality qualification.
> **D-24: (a) record-only** — legacy metrics explicitly not a concern; the
> feed repair becomes a precondition of the Tay RL-benchmark phase if that
> phase consumes the fields. **D-25: (a) record-only.** No code moved, no
> goldens moved; brief 2's Part B is empty and its handoff closed with these
> rulings.

| # | Item | What the code does | What the papers say | Options, costed |
|---|---|---|---|---|
| **D-23** | **The exposed-endpoint exemption on the application-layer mechanisms** (§l item 5) — decide it, as documented divergence or as a repair | OSDiversity, ServiceDiversity, PortShuffle and OSDA skip every host in `network.exposed_endpoints` entirely (`osdiversity.py:20-21`, `servicediversity.py:16-17`, `portshuffle.py:19-20`, `osdiversityassignment.py:48-49`; live-verified — zero endpoint writes). The attacker's five entry hosts are therefore immutable in service/vulnerability/port space for the whole reported family; only their adjacency moves (CTS). The exemption is uniform across the family, so it cannot confound within-family rankings | Documented only for IPShuffle (Brown: "all internal hosts", IS-MTD-01; Zhang's "each involved host" is ambiguous). IS-MTD-05/-06 say "all services running on the host" / "each host" with no endpoint carve-out; PortShuffle's in-code comment ("other organisations might require to be fixed") is the only recorded rationale | **(a) Keep and document** (recommended): zero code, zero goldens; the rationale is defensible (fixed entry surface for external parties, IPShuffle-consistent) and the uniformity argument above holds. **(b) Remove the exemption** (mechanisms act on endpoints too): moves every golden that includes any application-layer mechanism (full D-05 procedure), changes the family's semantics against every recorded run, and makes the entry surface mutable — a substrate re-design, not a repair. |
| **D-24** | **The SAPV/APE metric feeds are degenerate in the time-domain arm** | `add_shortest_path` (called by CTS/OSD/SD/HTS) resolves `get_path_from_exposed(target_node=None)`, and `nx.shortest_path(graph, source, None)` returns a **dict of all shortest paths from that source** — each firing appends a 50-entry paths-dict to `scorer.shortest_path_record` where one path is expected (live-verified for all four callers). Downstream, `shortest_path_variability` (`evaluation.py:180-181`) takes `len()` of the entries (= reachable-node count, not path length) and `attack_path_exposure()` (`network.py:630-664`) iterates the dict as if it were a path; `add_attack_path_exposure` itself is gated to `network_type == 0` and never runs in the time-domain arm. No recorded arm consumes the values — `get_metrics` runs once at `proceed_mtd` (`mtd_operation.py:60-65`) and its return value is discarded; the live consumers are the deferred Tay-benchmark paths (`mtd_ai_operation.py:305-331`, `mtd_ai_training.py:251-277`) | SAPV/APE are Ho's metrics, defined against a targeted network with a real shortest path; no lineage paper defines either for a general (no-target) network | **(a) Record-only** (recommended): zero risk, no recorded consumer; annotate `metrics_semantics.md` if SAPV/APE are ever claimed. **(b) Repair the feed** (guard the `target_node is None` case): scorer-only change, movement streams unaffected, but pointless until a consumer exists — and it is a **precondition of the Tay RL-benchmark phase**, whose state vector reads exactly these fields. |
| **D-25** | **CompleteTopologyShuffle re-selects the target node on targeted networks** (flag-grade, latent) | `gen_graph` re-runs the target-selection branch on every regeneration (`network.py:210-212`, gated `network_type == 0`): CTS firing on a targeted network silently re-sites the attacker's objective. Inert in every recorded experiment (the time-domain arm is `network_type == 1`, `target_node` stays `None` — live-verified) | IS-MTD-07: "entirely regenerate the network's topology, changing every involved host's connection status" — nothing about re-siting the target; Ho adds "preserving the hosts". No paper re-sites objectives on shuffle | **(a) Record-only** (recommended — latent; becomes a decision only if a type-0 arm ever enters the evaluation). **(b) Pin or fix** now: premature — fixing before a classification against a live use would freeze an unclassified divergence. |

### Opened 2026-08-02 (boundary review 1 — the attacker read side)

Full evidence — the instrumented read census over both driving arms, the
attacker-visible projection diffs, the compromise-route census and the
verb-by-verb phase review — lives in
[`attacker_read_surface.md`](attacker_read_surface.md); the review brief is
[`../handoffs/2026-08-02_boundary_network_attacker_integration.md`](../handoffs/2026-08-02_boundary_network_attacker_integration.md).
Numbering continues after boundary review 3's concurrent allocations
(D-20..D-22) and review 2's (D-23..D-25), same day. Nothing was touched.

| # | Item | What the code does | What the papers say | Options, costed |
|---|---|---|---|---|
| **D-26** | **`Host.total_users` is the index of the first password-reusing account, not the account count** — and BRUTE_FORCE divides the compromise probability by it | `Host.__init__` sets `total_users = 0` (`host.py:49`); `set_host_users` (`host.py:478-494`) *increments* it inside a loop that `break`s at the first reusing user, so it counts to that user's position and stops. `compromise_with_users` (`host.py:179`) uses it as the divisor of `HOST_MAX_PROB_FOR_USER_COMPROMISE * len(attempt_users) / total_users`. Live-verified: **12 of 50 hosts** on a freshly built network have `total_users != len(users)`, ratios up to 5/2, inflating those hosts' brute-force probability up to 2.5×. Because it increments rather than assigns, repeated `set_host_users` compounds it (latent — UserShuffle only). Separately, duplicate draws in `random.choices` collapse in the users dict, so hosts routinely carry 4 accounts | **IS-NET-11**: "each host has **5 user accounts**". No lineage paper states the brute-force probability formula at all, so the divisor's *intent* is undocumented; what is documented is the account count the divisor is evidently meant to be | **Measured cost of leaving it: near nil** — across 60 runs BRUTE_FORCE was called 488 times and produced **1** compromise (0 in every defended arm), and the per-call probability is bounded by 0.05 even worst-case, so the route cannot move a comparative ranking. **(a) Repair** — assign `total_users = len(self.users)` outside the reuse loop; two lines, but it moves brute-force probability on ~24 % of hosts and therefore **moves every golden** (D-05 procedure), plus a regression test asserting `total_users == len(users)` after one and after two `set_host_users` calls. **(b) Keep and document** — zero risk, and the measurement above is the justification. **(c) Repair *and* restore the 5-account model** (dedupe the draw) — full IS-NET-11 conformance, but a network-generation change that perturbs the seeded topology far more disruptively. Recommendation: **(a)** if a re-baseline is being taken for another ruling anyway, else **(b)**; not **(c)** — the account-count question deserves its own evidence rather than being folded into a divisor repair |
| **D-27** | **The credential channel is structurally unopposed by the reported family** | `host.users` is read on two attacker paths — SCAN_PORT phase-1 reuse (`attack_operation.py:405` → `host.py:143-161`) and BRUTE_FORCE (`:544`) — and is moved by **no** mechanism in the default pool; UserShuffle is commented out (`mtd_scheme.py:22-31`). Measured over 10 seeds × 5 000 t.u. per arm: credential reuse carries **22.8 %** of compromises undefended and **10–20 %** under each reported mechanism. The channel is *not* a defence-immune floor — it falls with the defence (29 → 3–19) because stuffing needs users harvested from an earlier compromise — but no mechanism addresses it directly or differentially | IS-MTD-03 documents User Access Shuffle as the counter to credential stuffing (Brown §III-B(3)); IS-ADV-05 makes credential exploitation a first-class attacker capability. The lineage documents both the attack and its counter; the *default pool* omits the counter, and no paper prescribes the pool | **(a) Keep the family at four and state the boundary** (recommended) — zero risk; record where the family is described that its members contest the vulnerability surface and the path structure, with a credential route none of them addresses. Consistent with the fixed-family scope (`../workflows/project_context.md` § direction). **(b) Add UserShuffle for future runs** — built, write set verified (`mtd_write_surfaces.md` §(a)); no recorded experiment is re-run, so this is a new-experiment decision with its own comparability statement, not a repair. **(c) Record only in the read-surface file** — cheapest, but leaves the headline family described without its scope boundary |
| **D-28** | **ENUM_HOST does not enforce IS-PRC-01's visibility invariant — the movement attacker attacks hosts with no path from any exposed endpoint** *(the one finding of this review that can move a comparative ranking)* | SCAN_HOST path-checks when it builds the queue (`attack_operation.py:285`); ENUM_HOST never re-checks. `sort_by_distance_from_exposed_and_pivot_host` (`network.py:868-901`) only *sorts* — unreachable hosts score `LARGE_INT` and sort last but are never dropped — and `_do_enum_host` (`:333-379`) pops the head regardless. The native FSM is saved by control flow: its forced post-interrupt `_scan_host()` (`:228-233`) rebuilds the stack (**0 of 873** pops outside the visible graph, 20 runs). The movement driver declines to re-impose native succession by design (`attacker.py:456-482`, H-coupling rationale), so the stack is never flushed: **9.7 %** of pops undefended, **22.4 %** defended, target a host with no path from any exposed endpoint (10 seeds each). The rate more than doubles under MTD because MTD is what makes queued hosts unreachable | **IS-PRC-01**: internal hosts are visible "**only if a path exists** through a compromised or exposed internal host". §c names "violates an invariant the papers state" as evidence for *bug* — this does, and only because the carve moved succession out from under an invariant nothing guarded | **Blunts Complete Topology Shuffle specifically — the mechanism whose entire claim is topology — in the arm the headline result runs on** (experiment 2 §9, Row B). **(a) Guard `_do_enum_host`** (recommended, subject to ruling): drop or defer a popped host with no path in the hacker-visible graph. Shared verb core, so it reaches **both** arms automatically via the outcome channel with no controller-mapping change; moves every golden (D-05 procedure); regression test per gate 5 — ENUM_HOST never sets `curr_host` outside `get_hacker_visible_graph()`. **(b) Filter `_host_stack` on each mutation** — equivalent effect, but spreads the invariant across the MTD path instead of keeping it in the verb that breaks it. **(c) Keep and document** — records that the movement attacker's reachability model is weaker than IS-PRC-01 and that recorded topology-mechanism effects are lower bounds. **Honest limit:** the ranking effect is argued from the mechanism, not measured; measuring it needs a new comparative arm on a guarded substrate (permitted — a new substrate version, not a re-run) |
| **D-29** *(record-grade)* | **Mechanism arms do not share the attacker's dice** | Mechanisms and attacker draw from the same global `random` stream — the attacker's exploit-success draw (`services.py:150`), sort jitter (`network.py:896`, `attack_operation.py:292`) and brute-force draw (`host.py:179`) alongside the mechanisms' own. Draws per firing, measured over 10 defended seeds: CTS **134.6**, IPShuffle **180.0**, OSDiversity **999.3**, ServiceDiversity **954.3**. A fixed seed therefore does not replay the same attacker across arms. Realignment noise, not bias. The movement layer's own timing/token streams are isolated (`timing.py:54-77`, `attacker.py:282`), so this is a substrate-stream property present in both arms | Nothing in the lineage specifies stream discipline; this is an experimental-design property rather than a conformance question | **(a) Record** (recommended) in `metrics_semantics.md` beside the existing comparability boundary: seed-matched mechanism arms are **independent**, not paired, so common random numbers are unavailable across them and the standing "ten seeds supports a rank comparison and not a significance test" caveat (APT criterion Row B) is if anything understated. **(b) Isolate the substrate's streams** — moves every golden and buys only variance reduction in future runs |

**Resolved-by-precedence (no ruling needed, listed for the record):** IS-CFL-03
(exponential replaces uniform — documented), IS-CFL-04 (Scenario 1 only — documented),
IS-CFL-05 (code sits on Tay's side), IS-CFL-06 (seventh technique = CompleteTopologyShuffle,
verified).
