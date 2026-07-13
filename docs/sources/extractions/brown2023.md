# Brown 2023 — extraction notes

> "Evaluating Moving Target Defenses against Realistic Attack Scenarios",
> Alex Brown, Tze-Wen Lee, Jin B. Hong. *2023 IEEE/ACM EnCyCriS*.
> Source file: `docs/sources/brown2023.md`.

This is the **foundational** MTDSim paper. It establishes the modules, the
attacker procedure, the MTD technique set, and the baseline parameter table.
Time domain, MTTC, execution schemes, and security-metric suite are NOT in
this paper — they come later (Zhang / Ho).

`[VERIFY-CODE]` = locator references the paper precisely but I have not yet
walked it through `mtdnetwork/` in detail; flagged for the merge pass.

---

## Network model (HARM)

| ID | Artefact | Locator |
|---|---|---|
| B-NET-01 | 3-layer HARM = Host / Service / Vulnerability graphs (Network is the container, not a layer) | §III-A, Fig 1 |
| B-NET-02 | Hosts split across "levels of depth" (public/DMZ/app/database/…); first level = exposed hosts; rest randomly assigned | §III-A "Host Layer", Fig 2 |
| B-NET-03 | Inter-subnet topology from **Barabasi–Albert** model | §III-A intro |
| B-NET-04 | Per-host internal service network from **Watts–Strogatz** model | §III-A intro |
| B-NET-05 | Services generated per OS; **50 % chance** a service is cross-platform | §III-A "Service Layer"; Table I (`Vulnerability cross-platform = 0.5`) |
| B-NET-06 | Service version ∈ **1–99**; older versions accrue more vulnerabilities; v99 **always** carries a vuln (zero-day proxy, guarantees universal exploitability) | §III-A "Service Layer" (footnote 2 caps at 99) |
| B-NET-07 | A vulnerability has a chance of being introduced per version and is patched **~10 versions later on average** | §III-A "Service Layer" |
| B-NET-08 | Services per host ∈ **[3, 11]** | §III-A; Table I |
| B-NET-09 | Each host has OS, host ID, services; **host ID determines its location on the network** | §III-A "Service Layer" (last sentence) |
| B-NET-10 | Vulnerability attack complexity ∈ **[0.4, 1]**; impact ∈ **[0, 1]** (CVSS-derived) | §III-A "Vulnerability Layer"; Table I |
| B-NET-11 | Total hosts = **200**; exposed hosts = **20**; layers = **5**; subnets = **20** | Table I |

Brown does **not** define a service-level "compromised" threshold here; the
"sum of impacts > 7" rule the README states is from a *later* layer of the
code (or another paper) and is one of the Conflicts (C3).

---

## MTD techniques (§III-B)

| ID | Artefact | Locator |
|---|---|---|
| B-MTD-01 | **IP Shuffle** — random reassignment of all internal-host IPs; interrupts attackers using stale IP | §III-B(1) |
| B-MTD-02 | **Port Shuffle** — reassigns ports of **exposed services**; interrupts attackers using stale port number | §III-B(2) |
| B-MTD-03 | **User Access Shuffle** — regenerates host user accounts; defeats credential stuffing | §III-B(3); each host has **5 users**, each with **5 %** chance of password reuse |
| B-MTD-04 | **Host Topology Shuffle** — swaps hosts with another host **on the same network layer** | §III-B(4) |
| B-MTD-05 | **Service Diversity** — replaces all services on the host; disconnects ongoing service-level attack | §III-B(5) |
| B-MTD-06 | **OS Diversity** — randomly changes OS; also rerolls services incompatible with new OS | §III-B(6) |

Brown does **not** describe "Complete Topology Shuffle". That technique is
introduced later (Ho).

---

## Attacker model (§III-C)

| ID | Artefact | Locator |
|---|---|---|
| B-ATK-01 | **Two attack scenarios**: (1) General/takeover — compromise as much as possible, prioritise weakest hosts; (2) Targeted/APT — compromise a specific host | §III-C(1) |
| B-ATK-02 | Targeted attacker prefers (a) the target if found, (b) hosts on the same level as target, (c) hosts on different levels to traverse toward target level | §III-C(1) Scenario 2 |
| B-ATK-03 | **Attack procedure** (CKC + ATT&CK-inspired, Fig 3): host discovery → host reconnaissance (port scan + credential stuffing first) → select service → priority-stack vulns by **RoA** → exploit → on success: C2 reveals connected hosts/services → on fail: brute force → if all fail: pick another host | §III-C(2), Fig 3 |
| B-ATK-04 | **Monotonic-compromise broken by MTD**: if MTD disrupts an attack path, previously-compromised hosts are no longer controlled | §V-B |
| B-ATK-05 | If a previously-compromised host's path is regained, the attacker **instantly** re-controls it (configs unchanged → trivial re-exploit) | §V-B |
| B-ATK-06 | **Give up after 10 failed attempts** per host (Scenario 1); **never** give up on the target node (Scenario 2) | Table I (`No. of attack attempts before giving up = 10`); §V-C |
| B-ATK-07 | Attacker is given a **time penalty + forced re-scan** whenever blocked by an MTD | §V-A |
| B-ATK-08 | All attackers share the same procedure — exploitation **skill** is not parameterised (called out as future work) | §V-C |

---

## Adversary–MTD interaction (§III-D — three classes of "block")

| ID | Artefact | Locator |
|---|---|---|
| B-INT-01 | **Connection to Host lost** — triggered by IP Shuffle, Host Topology Shuffle → attacker re-runs host discovery | §III-D(1) |
| B-INT-02 | **Connection to Service lost** — triggered by Service Diversity, OS Diversity, Port Shuffle → attacker re-runs port scan | §III-D(2) |
| B-INT-03 | **User Access changed** — triggered by User Shuffle → only blocks credential-stuffing attacks | §III-D(3) |

---

## MTD trigger model (§IV)

| ID | Artefact | Locator |
|---|---|---|
| B-TRIG-01 | MTD trigger time ~ **Uniform(1000, 5000) ms**, E[T] = 3000 ms | §IV (first paragraph); Table I "Defense trigger time" |
| B-TRIG-02 | The uniform distribution randomises timing while keeping the frequency roughly constant across trials (rationale, not separate behaviour) | §IV |

---

## Evaluation (§IV)

Brown's two reported metrics:

| ID | Artefact | Locator |
|---|---|---|
| B-MET-01 | **Total attack actions blocked** | §IV, §IV-A; Fig 4 |
| B-MET-02 | **Average attempts required to compromise** | §IV, §IV-B; Fig 5 |
| B-MET-03 | Brown explicitly *defers* RoA / AC / risk / reliability / probability-of-success because they "depend on other external factors" | §IV last paragraph |

So Brown introduces RoA only as the **internal ordering signal** in the
exploit priority stack (B-ATK-03), not as an output metric.

---

## Parameter table (Table I) — the canonical baseline

| Parameter | Value |
|---|---|
| Total no. of hosts | 200 |
| No. of exposed hosts | 20 |
| No. of layers | **5** |
| No. of subnets | 20 |
| Services per host | [3, 11] |
| Vulnerability cross-platform | 0.5 |
| Vulnerability attack complexity | [0.4, 1] |
| Vulnerability impact | [0, 1] |
| Attack attempts before giving up | 10 |
| Defense trigger time | Uniform(1000, 5000) ms |

**Re. conflict C1 (README "3-layer" vs Brown "5 layers"):** in Brown's text
the "3-layer HARM" refers to the *representation* (Host/Service/Vulnerability
levels). The "5" in Table I is `No. of layers` of the *Host-layer topology*
(network depth: public, DMZ, app, db, …). Two different concepts — *probably*
not a contradiction. Recorded; do not auto-resolve without code check.

---

## Future work / limitations Brown explicitly flags (relevant for `[ATK-SWAP]`)

| ID | Artefact | Locator |
|---|---|---|
| B-FW-01 | Attacker exploitation skill not parameterised — distinguishing skill levels is future work | §V-C |
| B-FW-02 | Randomness of attacker "confusion" beyond fixed time penalty is acknowledged as crude — future work | §V-A |
| B-FW-03 | Realism limit: not all real-system aspects captured; framework deliberately emphasises *attacker* realism over *system* realism | §V-A last paragraph |

These map directly onto the lit-review direction of replacing the attacker
with CTI-grounded adversary profiles.
