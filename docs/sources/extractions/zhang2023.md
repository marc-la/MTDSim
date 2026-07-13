# Zhang 2023 — extraction notes

> Wenxiao Zhang, *Evaluating Multiple Moving Target Defence in the Time Domain*,
> UWA Masters Thesis, supervised by Jin Hong. Source file:
> `docs/sources/zhang2023.md`.

Zhang extends Brown's `MTDSim` into **`MTDSimTime`** — the time-domain version
that introduces MTTC as the headline metric, time-stamped events, and MTD
execution schemes. Zhang **selects only 4 of Brown's 7 MTD techniques** and
introduces `OSDiversityAssignment` (DAP). The simulator switches from a fixed
`Uniform` MTD trigger to an **exponential** one. Adversary profile is now
explicitly factored into four dimensions.

Throughout, I use **Z-XXX-NN** to namespace artefacts.

---

## Architecture & framework (§4.1)

| ID | Artefact | Locator |
|---|---|---|
| Z-ARCH-01 | Three top-level modules: **Simulated Network**, **MTD Techniques**, **Adversary** | §4.1, Fig 1 |
| Z-ARCH-02 | The Simulated Network module is a graph of nodes (hosts) and edges; each node runs a list of exploitable services | §4.1 |
| Z-ARCH-03 | MTD module performs the **MTD Operation** (set of actions interacting with the network); Adversary module performs the **Attack Operation** (list of attack actions on hosts) | §4.1 |

---

## Network model (§4.2)

| ID | Artefact | Locator |
|---|---|---|
| Z-NET-01 | 3-layer HARM: **AGn** (Host attack graph, Barabasi–Albert), **AGh** (Services-on-Host graph, Watts–Strogatz), **ATs** (Service Attack Tree) | §4.2.1, Fig 2 |
| Z-NET-02 | Per-host attributes: unique IP, OS, set of services, set of user credentials | §4.2.2 |
| Z-NET-03 | **Four OS types** available: Ubuntu, CentOS, Windows, FreeBSD | §4.2.2 |
| Z-NET-04 | **5 users per host**, randomly assigned credentials; some reuse credentials across the network → credential-stuffing risk | §4.2.2 |
| Z-NET-05 | Services generated per OS; **service version ∈ [1, 99]**; older versions more vulnerable | §4.2.3 |
| Z-NET-06 | Same-name services may share vulnerabilities | §4.2.3 |
| Z-NET-07 | **Half** of newly created services are cross-platform | §4.2.3 (matches Brown's 0.5) |

Zhang does *not* repeat Brown's per-vuln AC range, impact range, or the
"version 99 zero-day" rule — but does not contradict them either.

---

## MTD techniques (§4.3.1) — **the selected subset**

Zhang reduces Brown's seven techniques to **four + one new**:

| ID | Artefact | Locator |
|---|---|---|
| Z-MTD-01 | **CompleteTopologyShuffle** — reconfigures the entire topology; all per-host connection statuses change. Generalisation of SDN topology-shuffling work | §4.3.1.1 |
| Z-MTD-02 | **IPShuffle** — randomly changes virtual IPs of involved hosts | §4.3.1.2 |
| Z-MTD-03 | **ServiceDiversity** — randomly re-versions services running on each involved host (each service has 99 versions, each version has a different vuln set) | §4.3.1.3 |
| Z-MTD-04 | **OSDiversity** — re-assigns each involved host's OS, drawn from the four OS types | §4.3.1.4 |
| Z-MTD-05 | **OSDiversityAssignment (DAP)** — optimised variant of `OSDiversity`: solves the Diversity Assignment Problem to maximise network connectivity given OS variant counts. Abstracts the topology to a single endpoint + single database (intermediate hosts as routing nodes), then solves DAP objective + constraint functions | §4.3.1.5, Fig 3 |

The other three Brown techniques (Port Shuffle, User Shuffle, Host Topology
Shuffle) are dropped from this thesis's experimental set; whether they remain
implemented in the codebase is a question for the merge pass.

---

## MTD execution schemes (§4.3.2) — **introduced by Zhang**

All schemes are **time-based proactive** (no reactive variants in this thesis).
General flow (Fig 4):

1. Periodic triggering signal arrives.
2. System registers a new MTD instance into the queue, or triggers an existing
   one from the queue.
3. Highest-priority MTD in the queue is popped and deployed, unless a
   resource is already occupied — see §4.3.3.
4. If suspended, instance goes into a **suspension queue**, which has *higher*
   priority than the MTD queue on the next cycle.

| ID | Artefact | Locator |
|---|---|---|
| Z-SCH-01 | **Random execution** — one randomly-selected MTD registered + triggered per signal | §4.3.2.1, Fig 5a |
| Z-SCH-02 | **Alternative execution** — one MTD registered + triggered per signal, but selected *alternatively* (in `MTDSimTime`, based only on the previously registered instance) | §4.3.2.2, Fig 5b |
| Z-SCH-03 | **Simultaneous execution** — *all* MTD techniques triggered at each signal; higher-priority MTDs deploy first; lower-priority ones go straight into the suspension queue if the resource is busy | §4.3.2.3, Fig 5c |

---

## MTD event model (§4.3.3) — resource occupation + suspension

| ID | Artefact | Locator |
|---|---|---|
| Z-EVT-01 | After being triggered, an MTD identifies whether the resource it serves is **available**; if yes it deploys and occupies the resource until execution completes; if no, it is suspended until the resource is free | §4.3.3, Fig 6 |
| Z-EVT-02 | Each MTD has a **resource layer**: e.g. IPShuffle → network layer; CompleteTopologyShuffle, ServiceDiversity → application layer (per worked example) | §4.3.3 (worked example) |
| Z-EVT-03 | Two MTDs targeting the **same** layer cannot deploy concurrently → suspension. Two MTDs on **different** layers can run concurrently. | §4.3.3 (worked example) |

> Note re Z-EVT-02: the worked example shows `CompleteTopologyShuffle` and
> `ServiceDiversity` both deployed on the *application* layer, while
> `IPShuffle` is on the *network* layer. This is a precise locator to keep —
> any code change that re-routes which layer an MTD occupies will be visible
> in the per-execution-scheme suspension counts.

---

## MTD time model (§4.3.4)

| ID | Artefact | Locator |
|---|---|---|
| Z-TIM-01 | **MTD Interval** is sampled from an **exponential** distribution (Zhang explicitly changes from Brown's `Uniform(1000,5000)`) | §4.3.4 first paragraph |
| Z-TIM-02 | Each MTD technique has its own execution time (mean, std). Values are picked "within a reasonable range based on existing empirical data" + sensitivity analysis | §4.3.4 |
| Z-TIM-03 | **Table 3 — MTD Execution Time** (s): CompleteTopologyShuffle 110/0.5, IPShuffle 100/0.5, OSDiversity 80/0.5, DAP_OSDiversity 80/0.5, ServiceDiversity 70/0.5 | Table 3 |

> **Note re table 3**: the code's `MTD_DURATION` constants (`data/constants.py`)
> for the same technique names are CompleteTopologyShuffle 120, IPShuffle 110,
> OSDiversity 80, ServiceDiversity 70, PortShuffle 70, HostTopologyShuffle 100,
> UserShuffle 20. The CompleteTopologyShuffle and IPShuffle values **differ by
> 10** between thesis and code; record but do not auto-resolve.

---

## Adversary profile (§4.4.1) — four dimensions

| ID | Artefact | Locator |
|---|---|---|
| Z-PROF-01 | **Attack Objectives** — Zhang refactors *only Scenario 1* (general/takeover) for `MTDSimTime`. Brown's Scenario 2 (targeted) is **explicitly out of scope** in this thesis | §4.4.1.1 |
| Z-PROF-02 | **Exploiting Vulnerabilities** — adversary follows a fixed action sequence; "enough services compromised on a host" ⇒ host considered compromised | §4.4.1.2 |
| Z-PROF-03 | **Command and Control Capabilities** — compromised hosts always stay compromised and are *instantly* recognised on path regain, regardless of MTD changes | §4.4.1.3 |
| Z-PROF-04 | **Exploiting User Credentials** — credential stuffing using users of all previously-compromised hosts; if successful, host compromised without exploiting a vuln | §4.4.1.4 |

`Z-PROF-03` softens Brown's `Z-PROF-03`-equivalent: Brown said the monotonic
assumption is *broken by MTD* — Zhang says "always stay compromised". This is
**probably** a simplification for the time-domain refactor; not a contradiction
to flag without checking the code path.

---

## Attack event model (§4.4.2) — three phases

The action flow (Fig 7):

`SCAN_HOST` → `ENUM_HOST` → loop {Phase 1 → Phase 2 → Phase 3} → on success: `SCAN_NEIGHBOR`.

| ID | Artefact | Locator |
|---|---|---|
| Z-EVT-04 | **Phase 1 — `SCAN_PORT` & user-credential exploitation**: port-scan the host and credential-stuff with users from previously compromised hosts | §4.4.2 |
| Z-EVT-05 | **Phase 2 — `EXPLOIT_VULN`**: exploit vulnerabilities in services discovered in Phase 1 | §4.4.2 |
| Z-EVT-06 | **Phase 3 — `BRUTE_FORCE`**: brute-force a user login if Phase 2 fails | §4.4.2 |
| Z-EVT-07 | If any phase succeeds, host is compromised | §4.4.2 |
| Z-EVT-08 | **Network-layer MTDs** (IP Shuffle, Complete Topology Shuffle) — when deployed, **immediately fail** the attack event on host discovery | §4.4.2 |
| Z-EVT-09 | **Application-layer MTDs** (OS Diversity, Service Diversity) — do not block the attack action but **interrupt** it; adversary restarts from Phase 1 | §4.4.2 |
| Z-EVT-10 | Each attack action has a **maximum number of attempts**; once interruptions from application-layer MTDs hit that threshold, the attack event fails and the adversary moves to another host | §4.4.2 |

---

## Adversary time model (§4.4.3)

| ID | Artefact | Locator |
|---|---|---|
| Z-TIM-04 | **Phase 1 time** assumed constant (port-scan speed is constant under a fixed scan strategy) | §4.4.3 first paragraph |
| Z-TIM-05 | **Phase 3 time** has a fixed time limit (brute force is time-bounded) | §4.4.3 first paragraph |
| Z-TIM-06 | **Phase 2 time** varies with: (i) **server side** — attack complexity `ACv ∈ [0, 1]` of the service running on the target host, with 0 = unexploitable, 1 = easiest exploit; (ii) **adversary side** — learning + confusion | §4.4.3 |
| Z-TIM-07 | **Adversary learning**: exploitation time is **halved** for vulnerabilities exploited in *previous* attack operations on previous hosts | §4.4.3 |
| Z-TIM-08 | **Confusion penalty**: a time penalty is added each time the attack event is interrupted/stopped by MTD | §4.4.3 |
| Z-TIM-09 | **`T_Aphase2`** = formula involving `T_Aexploit` (exponential) and `V_exploited` / `V_unexploited` counts (Eqs 1, 2 — figures not extracted in the source dump) | §4.4.3, Eq 1, Eq 2 |

> **`Z-TIM-06` is the head of Conflict C2 with Brown** (`ACv ∈ [0,1]` here vs
> `[0.4, 1]` in Brown Table I). Recorded; do not auto-resolve.

---

## Simulation time model (§4.5)

| ID | Artefact | Locator |
|---|---|---|
| Z-SIM-01 | DES on **SimPy** controls time passing and event processing | §4.5 |
| Z-SIM-02 | **Exponential distribution** selected as the primary time-elapsed PDF (Eq 3); CDF gives `P(x<a) = 1 − e^(−a/µ)` (Eq 4) | §4.5 |
| Z-SIM-03 | Random variable `x` represents either inter-event time (e.g. MTD interval) or action duration; `µ` is the historical average elapsed time | §4.5 |

---

## Evaluation methodology (§5)

| ID | Artefact | Locator |
|---|---|---|
| Z-EVAL-01 | Two-stage evaluation: **single-MTD** (effectiveness, MTD-interval impact, network-size impact) and **multiple-MTD** (pairwise combinations × three execution schemes) | §5 intro |
| Z-EVAL-02 | Test grid: **4 MTD intervals** {50, 100, 150, 200} s × **4 network sizes** {25, 50, 75, 100} nodes; **100 runs** per variable set | §5 intro |
| Z-EVAL-03 | **Network Compromise Ratio (NCR)** = compromised hosts / total hosts. Terminating condition: NCR = **0.8** | §5 intro |
| Z-EVAL-04 | **Primary metric: MTTC** — Mean Time to Compromise. Reported on 0.8 NCR (Fig 8, Fig 10) | §3.4 and §5 |
| Z-EVAL-05 | Other static metrics surveyed: **Attack Cost (AC)**, **Return on Attack (RoA)**, **system risk**, **system availability (SA)** — Zhang lists them but does not report new values | §3.4 |
| Z-EVAL-06 | Dynamic metrics surveyed (inherited from prior work): **APV** (Attack Path Variation), **APE** (Attack Path Exposure), **ACD** (Attack Compromise Duration) — based on T-HARM | §3.4 |
| Z-EVAL-07 | **Table 2 — Network Properties**: Net1 25/0.093/3 endpoints/4 layers; Net2 50/0.052/5/4; Net3 75/0.040/7/4; Net4 100/0.043/10/4 | Table 2 |

---

## Future work / explicit limitations (§6) — **load-bearing for `[ATK-SWAP]`**

| ID | Artefact | Locator |
|---|---|---|
| Z-FW-01 | Adversary's target-selection currently uses **distance to discovered hosts** only — flagged as a simplification. Suggests adding a port-scan-then-difficulty-estimate stage and "other factors" | §6.3 |
| Z-FW-02 | MTD techniques currently execute on **all nodes**. Selective / critical-node reconfiguration is future work — explicit call-out of the QoS gap and the need for traffic profiling / vuln assessment | §6.4 |
| Z-FW-03 | Set of MTD techniques deliberately narrow (2 shuffle + 3 diversity) — generalisability call-out | §6.2 |
| Z-FW-04 | Suspension mechanism not investigated for *deployment frequency vs interval* relationship — confirmed hypothesis missing | §6.1 |

---

## Cross-references to flag at merge

- `Z-TIM-06` ⇄ Brown `B-NET-10`: AC range disagreement (Conflict C2).
- `Z-MTD-01..05` ⇄ Brown `B-MTD-01..06`: technique set differs — Zhang drops
  Port/User/HostTopology shuffles and adds CompleteTopology + DAP-OSDiversity.
- `Z-TIM-03` ⇄ code constants in `data/constants.py`: per-technique durations
  diverge by ≤ 10 s on CompleteTopologyShuffle and IPShuffle. **Code carries
  extra techniques** (PortShuffle, HostTopologyShuffle, UserShuffle) that
  Zhang dropped — record as `divergent` candidates.
- `Z-PROF-01`: targeted-attack scenario (Brown's Scenario 2) is *out of scope*
  in MTDSimTime; the codebase appears to support it via `network_type==0`
  paths in `Network.gen_graph` — likely partial inherited logic from Brown
  era. Worth a code-side check.
