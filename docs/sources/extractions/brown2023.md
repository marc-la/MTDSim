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

---

## Eight-property verification (2026-09-07, independent pass for Table 3.3)

Source read in full (`lit_review/brown2023.md`, l.1–200), scored against Table 3.2's definitions; framing recorded separately from execution. Marks: FULL = has the property as defined; HALF = the executed attacker does something under the heading that falls short of the definition; NONE. Line numbers are the source markdown's; PDF printed page = physical page throughout.

Executed attacker: a fixed-flowchart agent (host discovery → port scan → credential stuffing from harvested accounts → RoA-ranked exploit stack → brute force → next host), two goal variants on one 200-host HARM — Scenario 1 weakest-first to compromise everything; Scenario 2 the target if seen, else same-level hosts, else other-level, never giving up on the target — every MTD block costing a time penalty and a forced re-scan; previously compromised hosts regained instantly.

| # | Property | Mark | Evidence | Reason |
|---|---|---|---|---|
| 1 | Persistence | HALF (borderline FULL) | "The attacker will commence with the host discovery phase… Host reconnaissance is performed next… Once the attacker has successfully compromised a host, they will assume command and control functionality" (l.115, §III.C.2); "never give up on the target node" (l.196, §V.C) | multi-stage per-host loop continued across hosts and through MTD disruptions; no dwell or extended-period quantity — the period is whatever the run takes |
| 2 | Objective conditioning | HALF (borderline FULL) | "In case of the target host is found, the attacker will only attack the target host. If the target host is not found… prioritize attacking hosts that exhibit similar characteristics with the target host (i.e., … same level…)" (l.109–111, §III.C.1); "two attack scenarios with the same capabilities but with different goals" (l.103) | post-foothold host preference and the give-up rule differ by goal and are executed; a fixed per-scenario priority rule set at design time, not a runtime evaluation of the objective |
| 3 | Strategic plurality | HALF | "first attempt to perform a credentialstuffing attack… Next, a service… selected for exploitation… If the attack fails, they will then commence a brute force attack. If all attack options fail, they will then choose another host" (l.115, §III.C.2) | three vectors and plural hosts/paths, tried in a fixed fallback order — never a branch chosen among alternatives |
| 4 | Adaptivity | HALF | "forced to re-perform the host discovery phase" (l.121, §III.D.1); "force them to re-perform a port scan" (l.123, §III.D.2); "forcing them to look for vulnerabilities on the host" (l.135, §III.D.3); "a time penalty whenever the attacker is blocked… and forces them to re-scan" (l.186, §V.A) | three distinct scripted responses to the three block types, plus instant regain (l.192); the paper's own words are "forced" — a simulator-imposed restart of a fixed procedure, not a change of strategy |
| 5 | Stealth | NONE | silent; closest "performing a scan on the network to discover all exposed hosts… running port scans" (l.115) | active, unconstrained scanning; no detection model, no evasion |
| 6 | Incentive-driven rationality | HALF (borderline FULL) | "The vulnerabilities from all the services scanned will be put into a priority stack based on their return on attack (RoA) [13]" (l.115); RoA from CVSS complexity [0.4, 1] and impact [0, 1] (l.73, §III.A) | a per-step cost/benefit ordering of exploits within a host; host choice is by scenario rule, no abstention or cost-based stopping (the 10-attempt cap is a counter, l.133) |
| 7 | Learning | NONE (borderline HALF) | silent on learning; closest "credentialstuffing attack using user account information from previously compromised hosts" (l.115); instant regain of previously compromised hosts (l.192) | within-run memory of credentials and footholds; nothing about the defender learned, nothing retained across runs |
| 8 | Scheme awareness | NONE | silent; closest "uncertain of the status of the hosts" (l.121); "impractical to program the randomness of confusion accurately" (l.186) | no model of which MTD runs, its Uniform(1000, 5000) ms trigger (l.133, l.139) or its logic; the restart is technique-agnostic |

Framing vs execution: "theoretically intelligent adversary" (l.51, §III) vs "All attacker agents… will always follow the attack procedure (as shown in Figure 3)" (l.184, §V.A); Scenario 2 "like APT-style attacks" (l.109) vs HARM-level knowledge only; abstract/intro "realistic attack scenarios… derived using Cyber Kill Chain and MITRE ATT&CK" vs l.184's concession that the framework is inspiration for the flowchart. Skill differentiation is explicitly future work (l.196).

Locators verified against the PDF: "the exploitation skills are not configured to distinguish the different skills of adversaries" — p.7, §V.C (l.196). Also p.4 for the RoA priority stack (l.115) and the Scenario 2 rule (l.109–111); p.5 Table I; p.7 for l.186/192/196. Fig. 3 is an image with no text layer.
