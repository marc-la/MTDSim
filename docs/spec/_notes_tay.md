# Tay 2024 — extraction notes

> Joo Kai Tay (22489437), *Using Artificial Intelligence to Automate the Deployment
> of Moving Target Defence Operations*, UWA Engineering Research Project Part 2
> (GENG5512), supervised by Jin Hong, 12 October 2024. Source file:
> `docs/sources/tay2024.md`.
>
> Ho 2024's acknowledgements credit Joo Kai with "mainly responsible for the
> model development" of the shared DDQN; this thesis is the model-side write-up.

Tay packages the joint model as **MTDShield** — a reactive RL plugin that
sits on top of `MTDSimTime` and converts it from a purely time-scheduled
defender into one that consumes network security posture and (when warranted)
selects a technique to deploy. Five discrete actions including a **no-op**.

`T-XXX-NN` namespace.

---

## Architecture (§4.1, Fig 1)

| ID | Artefact | Locator |
|---|---|---|
| T-ARCH-01 | **MTDShield** is a plugin on top of the inherited 3-module simulator (Network / MTD / Attacker) — converts MTDSimTime from purely time-scheduled to **reactive** | §4 intro; §4.1; Fig 1 |
| T-ARCH-02 | MTDShield internal pipeline: **(d) Feature Extraction Module → (e) Time Series Analysis Module → (f) Feature Fusion Module → (g) Q-Network Output Module** | §4.1, Fig 1 |
| T-ARCH-03 | Decision flow: receives network posture in real time → decides whether an MTD should trigger → if yes, **selects which technique** from the 5-action set → deploys via MTD-operations module | §4 intro; §4.1 |

---

## Action set (§4.1) — **the load-bearing thing**

| ID | Artefact | Locator |
|---|---|---|
| T-ACT-01 | **5 MTD actions** total: `IPShuffle`, `OSDiversity`, `ServiceDiversity`, `CompleteTopologyShuffle`, **no-op (do not deploy)** | §4.1 (action paragraph); §4.1.4 ("five Q-values, one for each MTD technique plus the option to do nothing") |

This is the canonical resolution for **Conflict C4** in the seed:
- Brown's 6 techniques include `PortShuffle`, `UserShuffle`, `HostTopologyShuffle`.
- Zhang's experimental subset = 4 (the four above without no-op) + DAP.
- Tay's RL agent gets `{IPShuffle, OSDiversity, ServiceDiversity, CompleteTopologyShuffle, no-op}`.
- Ho's action space additionally includes **pairwise combinations** (`H-RL-04`).

I.e. the inherited code likely has more techniques than the RL agent
exposes. To verify against the merged spec.

---

## Feature Extraction Module (§4.1.1) — static features

| ID | Artefact | Locator |
|---|---|---|
| T-FX-01 | Architecture: `Dense(128) → ReLU → BatchNorm → Dense(64) → ReLU → BatchNorm → Dropout(30%)` | §4.1.1 |
| T-FX-02 | Named static features the module is *designed* to handle: **Host Compromise Ratio (HCR)**, **Number of Vulnerabilities**, **Number of Exposed Vulnerabilities**, **Attack Path Exposure Score** | §4.1.1 paragraphs 2–5 |

---

## Time Series Analysis Module (§4.1.2)

| ID | Artefact | Locator |
|---|---|---|
| T-TS-01 | Architecture: `LSTM(64, return_sequences=True) → ReLU → BatchNorm → LSTM(32) → ReLU → BatchNorm → Dropout(30%)` | §4.1.2 |
| T-TS-02 | Named time-series features: **Mean Time to Compromise (MTTC)**, **Downtime/Operational Impact for Node Replacement**, **Time Since Last MTD (TSLM)** | §4.1.2 paragraphs 3–5 |

---

## Feature Fusion Module (§4.1.3)

| ID | Artefact | Locator |
|---|---|---|
| T-FF-01 | Concatenate feature-extraction output + time-series output → `Dense(64) → ReLU → BatchNorm → Dropout(30%)` | §4.1.3 |

---

## Q-Network Output Module (§4.1.4)

| ID | Artefact | Locator |
|---|---|---|
| T-Q-01 | Output dense layer with **5 units** (= the action set size); each Q-value = expected future reward for that action | §4.1.4 |

---

## Training (§4.2)

| ID | Artefact | Locator |
|---|---|---|
| T-TR-01 | **Double DQN**: separate main + target networks, target network updated every n steps to break correlation between action selection and value estimation | §4.2, §4.2.1, Fig 2 |
| T-TR-02 | **Experience Replay**: per-step packet `e_t = (s_t, a_t, r_t, s_{t+1})` stored in replay memory; minibatches drawn randomly during back-prop | §4.2.2 |

---

## Evaluation methodology (§5)

| ID | Artefact | Locator |
|---|---|---|
| T-EVAL-01 | **5 evaluation metrics**: ASR, MTTC, APE, ROA, Risk. Each model's scores are **normalised against a no-MTD baseline** (multiple of the baseline value) → enables direct cross-model comparison | §5.1 |
| T-EVAL-02 | Hyperparameter sweeps: gamma `{0.5, 0.55, …, 0.99}`; epsilon `{0.5, 0.6, 0.7, 0.8, 0.9, 1.0}` × decay `{0.980, 0.985, 0.990, 0.995, 0.998}`; train_start `{500, 1000, 1500, 2000}` | §5.2 |
| T-EVAL-03 | Best gamma was **0.85** (range 0.75–0.90 best); best epsilon was low-start (0.5–0.7) + decay 0.99; best train_start was **2000** | §5.2.1, §5.2.2, §5.2.3 |
| T-EVAL-04 | **Attacker Detection Rate Evaluation** = IDS-style information-supply experiment: feed the model varying fractions of attacker-action information (0 % – 100 %) during training | §5.3 |
| T-EVAL-05 | **Detection-sensitivity cutoff at 0.7**: between 0.7–1.0 sensitivity, performance improves monotonically with detection; below 0.7, performance becomes uncorrelated with detection (looks like 0 %) | §5.3, §6.4, Fig 6 |
| T-EVAL-06 | **Ablation studies** removing either the feature-extraction or the time-series module: complete model wins by 6–8 % overall but **under-performs in APE** by 4–13 % vs the incomplete models | §5.4, §6.5, Fig 7 |

`T-EVAL-05` is the precise locus for the lit-review's IDS-seam direction:
the detection-sensitivity knob is *already* a parameter in the codebase, and
0.7 is the empirical performance cliff Tay identifies.

---

## Future work / explicit limitations (§7)

| ID | Artefact | Locator |
|---|---|---|
| T-FW-01 | Testing on **real-world datasets** — integrate external intrusion datasets | §7.1 |
| T-FW-02 | Increased runtime + larger networks — current results may not generalise; gamma/epsilon optima may be artifacts of small simulation space | §7.2 |
| T-FW-03 | Individual metric ablation — only module-level ablations done; per-feature ablations are future work | §7.3 |

---

## **Important correction to the seed spec**

The seed (`docs/sources/MTDSIM_SPEC.md`) lists `SHD-07` "Federated training of
the selection policy" with locator "Tay §4" and tags it `[PERIPH]`. **Tay
does *not* implement federated training in this thesis.** §3.3 cites
Kreischer [21] as related literature only; the methodology, model training,
and evaluation chapters never mention federated training. Recommendation:
remove `SHD-07` from the merged spec (or re-attribute it as a *cited
reference*, not an artefact of MTDShield).

---

## Cross-references to flag at merge

- `T-ACT-01` (5 actions incl. no-op) resolves **C4** as far as Tay's agent is
  concerned; Ho's `H-RL-04` (pairwise combinations) is a **conflict candidate**.
- `T-FX-02` + `T-TS-02` overlap with Ho's metrics suite but use slightly
  different names. In particular Tay names **"Number of Vulnerabilities"** and
  **"Number of Exposed Vulnerabilities"** as static inputs — these are *not*
  in Ho's Table 3 enumeration. Worth a code check: are these features
  computed somewhere distinct from Ho's `Risk`/`RoA` chain?
- `T-EVAL-05` — the **0.7 sensitivity cutoff** is concrete and falsifiable;
  worth tagging as `[IDS-SEAM] Y` in the merged spec.
- `T-ARCH-01` reactive-vs-time-scheduled — the code carries both. The
  `MTDOperation` class is time-driven (Zhang); the `MTDAIOperation` class
  is the reactive plugin. The merge pass should record this as **two
  parallel execution surfaces in the same codebase**.
