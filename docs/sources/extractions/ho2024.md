# Ho 2024 — extraction notes

> Wai Him Ho, *Using Artificial Intelligence to Automate the Deployment of MTD
> Operation*, UWA, supervised by Jin Hong, October 2024. Source file:
> `docs/sources/ho2024.md`.
>
> Acknowledgement (§Acknowledgements) — the RL model was developed jointly with
> Joo Kai Tay (22489437); Joo Kai mainly built the model, Ho focused on data
> collection. So model architecture overlaps with **Tay 2024**.

Ho's contribution is the **security-metrics suite** (Table 3 + §3.3.2) and a
**DDQN-based selector** that consumes those metrics as features and chooses
from a fixed MTD action set. Time-domain machinery is inherited from Zhang.

`H-XXX-NN` namespace.

---

## Architecture (§3.1, Fig 1)

| ID | Artefact | Locator |
|---|---|---|
| H-ARCH-01 | Two-component system: **AI engine** (the proposed model) and **MTD simulator** (`MTDSimTime` from Zhang) | §3.1, Fig 1 |
| H-ARCH-02 | The simulator's 3-layer HARM (`AGn` + `AGh` + `ATs`) and execution schemes (random / alternative / simultaneous) are inherited unchanged | §3.1.1 |
| H-ARCH-03 | **Static Degrade Factor (SDF)** — default `2000 ms`. If `(now − last_MTD_trigger) > SDF`, the system **forces** a random MTD trigger from the active deployment type and resets the interval counter. Check runs *before* metrics are fed to the AI model | §3.1.2, Fig 2 |

`H-ARCH-03` is a *new behavioural rule* added on top of Zhang's exponential
MTD interval. Worth a code check — the SDF likely lives in a different module
than the MTD scheme itself.

---

## RL model (§3.2)

| ID | Artefact | Locator |
|---|---|---|
| H-RL-01 | **Double Deep Q-network (DDQN)** chosen over single-Q to mitigate Q-value overestimation (two Q-estimates updated independently) | §3.2.1 |
| H-RL-02 | Loss minimised over a neural-net Q approximator (Eq 2 referenced; figure omitted in source dump) | §3.2.1 |
| H-RL-03 | **Two-branch feature fusion**: static branch = `Dense(128, ReLU) → BatchNorm → Dense(64, ReLU) → BatchNorm`; time-series branch = `LSTM(64) → LSTM(32) → activation → normalisation → Dropout(30 %)`; both fused → final `Dense + ReLU` → Q-output layer | §3.2.2, Fig 4 |
| H-RL-04 | **Action space**: `{MTD_1, MTD_2, …, MTD_12, MTD_13, …, MTD_{n(n+1)/2}, Null}` — i.e. individual MTDs **plus pairwise combinations**, plus a `Null` (no-op) action | §3.2.3 |
| H-RL-05 | **Reward**: `R(s_t, a_t, s_{t+1}) = f(N_{t+1}) − f(N_t)`, where `f` is an evaluation function; accumulated as `R = Σ γ^t r_{t+1}`. Multi-metric optimisation uses a weighted sum with `w_i ∈ ±1` per feature direction | §3.2.4 |
| H-RL-06 | **Min-max normalisation** of features against in-memory history before each reward computation; training does not begin until **1000 samples** are collected (`training_start` parameter) | §3.2.4 |

> `H-RL-04` differs from Tay's action set (which is **5 actions: IP shuffle, OS
> Diversity, Service Diversity, Complete Topology Shuffle, no-op**, no pairwise
> combinations). Conflict candidate — see merge.

---

## Fixed parameters (§3.3.1, Tables 1–2)

| ID | Parameter | Value |
|---|---|---|
| H-PAR-01 | Discount γ | 0.95 |
| H-PAR-02 | ε (start) | 1.0 |
| H-PAR-03 | ε_min | 0.01 |
| H-PAR-04 | ε_decay | 0.995 |
| H-PAR-05 | training_start | 1000 |
| H-PAR-06 | episodes | 100 |
| H-PAR-07 | sim start_time | 0 |
| H-PAR-08 | sim finish_time | 15000 |
| H-PAR-09 | total_nodes | 150 |
| H-PAR-10 | Static Degrade Factor | 2000 ms |

---

## Security metrics suite — **the core Ho contribution** (§3.3.2, Table 3)

All metric definitions below are taken verbatim from Ho's prose; equations
are referenced by figure numbers (their actual LaTeX rendering is omitted
from the source dump).

| ID | Metric | Definition (Ho) | Locator |
|---|---|---|---|
| H-MET-01 | **Attack Path Exposure (APE)** | Average new-vulnerability% across the n hosts on the shortest attack path (`V_new(h)` per host) | §3.3.2 (1) |
| H-MET-02 | **Risk (R)** | `R_h(t_k) = CSP(h_i)_{t_k} · AI(h_i)_{t_k}` (compromise success probability × attack impact) | §3.3.2 (2) |
| H-MET-03 | **Return on Attack Cost (RoA)** | `RoAC(h_i) = R(h_i) / AC(h_i)`; **AC defined as the time to exploit** (Eq 3); overall RoA per system in Eq 4 | §3.3.2 (3) |
| H-MET-04 | **Host Compromise Ratio (HCR)** | `C_t / T_host` | §3.3.2 (4) |
| H-MET-05 | **Attack Stage** | Integer enum of the attacker's current phase, range `SCAN_PORT … BRUTE_FORCE`; default value when no attack in flight | §3.3.2 (5) |
| H-MET-06 | **Attack Success Rate (ASR)** | `C_t / A_t`, with `A_t = #{SCAN_PORT, EXPLOIT_VULN, BRUTE_FORCE attempts}`; 0 if no compromise recorded | §3.3.2 (6) |
| H-MET-07 | **MTD Execution Frequency (MEF)** | `N_MTD / (finish_last − start_first)`; 0 if no MTD executions | §3.3.2 (7) |
| H-MET-08 | **Mean Time to Compromise (MTTC)** | Mean duration of `SCAN_PORT`, `EXPLOIT_VULN`, `BRUTE_FORCE` events across relevant hosts; 0 if none | §3.3.2 (8) |
| H-MET-09 | **Time Since Last MTD (TSLM)** | `now − last_MTD_executed_time` | §3.3.2 (9) |
| H-MET-10 | **Shortest Attack Path Variability (SAPV)** | Changes in the set of shortest attack paths between `t_k` and `t_{k−1}` (cardinality of set difference) | §3.3.2 (10) |
| H-MET-11 | **Network Address Variability (NAV)** | Set-difference of network states between two consecutive time points, normalised by state size; value in `[0, 1]` | §3.3.2 (11) |

H-MET-08's definition is **the operative MTTC definition for the codebase**:
mean over only the three attack-action durations, restricted to relevant
hosts. The Phase-0 finding F-10 (`host_compromise_ratio > 1` in
`evaluation_result_by_compromise_checkpoint`) belongs nearby — Ho's HCR
definition is `C_t / T_host`, but the code computes
`compromised_num / (T_host · checkpoint_ratio)` and labels the result
`host_compromise_ratio`. Worth recording as a code-vs-paper divergence.

---

## MTD action set (§3.3.3)

| ID | Artefact | Locator |
|---|---|---|
| H-MTD-01 | **Complete Topology Shuffle** — completely regenerates the network but **preserves the hosts** from the previous network | §3.3.3 |
| H-MTD-02 | **IP Shuffle** — random new IP per host | §3.3.3 |
| H-MTD-03 | **OS Diversity** — switches between OS types and versions across the network | §3.3.3 |
| H-MTD-04 | **Service Diversity** — updates services running on host nodes | §3.3.3 |
| H-MTD-05 | An overarching **"Any MTD"** technique that can deploy any of the four — used as a row in Table 4 | §3.3.3, Table 4 |

Same four techniques as Zhang's selected set (minus DAP-OSDiversity).

---

## Feature combinations (§3.3.4, Tables 4–5)

| ID | Combination | Members |
|---|---|---|
| H-FEAT-01 | **Hybrid** | HCR, APE, ASR, RoA, R, MEF, MTTC, **Attack Stage** |
| H-FEAT-02 | **All Features** | Hybrid + **TSLM**, **SAPV**, **NAV** (called "Host IP Variability" in Table 5) |
| H-FEAT-03 | **Single-metric** rows | One model per `metric × MTD type` cell of Table 4 |

50 models total: each `metric × MTD type` cell trains one model that only
optimises that metric and only deploys that MTD type (or "Any MTD").

---

## Test grid (Tables 6–8)

| ID | Artefact | Value |
|---|---|---|
| H-EVAL-01 | MTD-interval sweep | {50, 100, 200}; Network Size = 150; Nodes = 150 |
| H-EVAL-02 | Network-size sweep | MTD interval = 50; Network Size ∈ {100, 150, 200}; Nodes = 150 |
| H-EVAL-03 | Comparison schemes for headline plots | Random / Alternative / Simultaneous / MTD AI, all at interval=200, size=150, nodes=150 |
| H-EVAL-04 | **5 checkpoints** per trial, mean of checkpoints = trial result, **median** of trials = model result | §3.4.1 |
| H-EVAL-05 | **Final evaluation score** = equal-weighted sum of {ASR, ROA, APE, R}, all scaled by no-MTD baseline so smaller is worse, larger is better | §3.4.2 |

---

## Headline findings (results not load-bearing for the spec, but useful context)

- §4.1 MTD interval has clear inverse correlation with model performance when "Any MTD" is the action — shorter interval ⇒ better.
- §4.3 **MTD-technique choice dominates**: diversity techniques outperform shuffling by up to **140 %** (OS Diversity vs IP Shuffle, hybrid metric, interval=200, size=150).
- §4.4 Hybrid model beats Simultaneous scheme on most metrics by ≥ 30 % overall; Simultaneous still wins on ASR.

---

## Future work / limitations (§5)

| ID | Artefact | Locator |
|---|---|---|
| H-FW-01 | Need for **more complex adversaries** — only one type in the simulator | §5.1 |
| H-FW-02 | Evaluation-metric set is narrow; performance/QoS metrics missing | §5.2 |
| H-FW-03 | MTD-technique set is narrow (4 techniques) — more "advanced or dynamic" needed | §5.3 |
| H-FW-04 | **Need a more reactive RL model** — attack-stage feature is too simplistic to be the reactive signal | §5.4 |
| H-FW-05 | No real-life scenario testing | §5.5 |

`H-FW-01` and `H-FW-04` both map directly onto the lit-review direction
(replacing the attacker with CTI-grounded profiles, IDS/detection seam).

---

## Cross-references to flag at merge

- `H-MET-08` (MTTC) ⇄ Zhang `Z-EVAL-04` and the code's
  `Evaluation.evaluation_result_by_compromise_checkpoint`. Both agree that
  MTTC is the average over `SCAN_PORT / EXPLOIT_VULN / BRUTE_FORCE`
  durations. The code's `time_to_compromise` field is computed this way.
- `H-MET-04` ⇄ code's `host_compromise_ratio` — **divergent** (see F-10).
- `H-RL-04` ⇄ Tay's 5-action set — **conflict candidate** (Ho includes
  pairwise combinations + Null; Tay flattens to 5 actions).
- `H-ARCH-03` (Static Degrade Factor 2000 ms) — *new* code-side rule
  introduced on top of Zhang's exponential interval. Locate in
  `mtdai/mtd_ai.py` / `operation/mtd_ai_operation.py` during merge.
- `H-MET-05` (Attack Stage) — the code's `Adversary.set_curr_process`
  states (`SCAN_HOST`, `ENUM_HOST`, `SCAN_PORT`, `SCAN_NEIGHBOR`,
  `EXPLOIT_VULN`, `BRUTE_FORCE`) are a superset of Ho's stated range
  (`SCAN_PORT … BRUTE_FORCE`). Worth noting whether the AI feature extractor
  exposes the full superset or just the three Ho enumerates.
