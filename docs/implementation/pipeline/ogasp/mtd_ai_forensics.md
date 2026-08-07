# `mtd_ai` forensics — what Tay's MTDShield agent actually is, before anything is built on it

**Status:** investigation record, 2026-08-07. Read-only throughout: nothing in the
substrate, the archive or the pipeline was modified to produce it.

**Why this exists.** The `mtd_ai` reintegration brief (`docs/handoffs/2026-08-06_mtd_ai_reintegration.md`,
deleted 2026-08-07 once superseded; recoverable via `git log --diff-filter=D --`
on that path) proposed standing up Tay's reactive defender as the arm the
consequential stealth claims are gated on, and offered two routes — reuse the
pretrained weights as a control, or retrain. Marc's prior was that the weights would not behave as the
paper describes, on the grounds that the hyperparameter sensitivity studies read
like an artefact of undertrained models. This record checks that prior against
the archive, the code and the paper. **The prior is confirmed, and the mechanism
is not the one anyone expected.**

The headline is §2: **the neural network was never consulted in any evaluation
reported in the paper.** Everything else follows from, or is independent of,
that.

---

## §0 What was probed, and how to reproduce it

| Artefact | Location |
|---|---|
| The 198 archived checkpoints | `mtdsim-weights-archive/` (gitignored; index at `mtdsim-weights-archive/weights_index.md`) |
| The probe | [`../../../../tools/mtd_ai_weights_probe.py`](../../../../tools/mtd_ai_weights_probe.py) |
| The paper | [`../../../sources/lit_review/tay2024.md`](../../../sources/lit_review/tay2024.md); extraction at [`../../../sources/extractions/tay2024.md`](../../../sources/extractions/tay2024.md) |
| The agent | [`../../../../mtdnetwork/mtdai/mtd_ai.py`](../../../../mtdnetwork/mtdai/mtd_ai.py), [`../../../../mtdnetwork/operation/mtd_ai_operation.py`](../../../../mtdnetwork/operation/mtd_ai_operation.py), [`../../../../mtdnetwork/operation/mtd_ai_training.py`](../../../../mtdnetwork/operation/mtd_ai_training.py) |
| Tay's drivers | **deleted from the tree** (`e5935ab`, `6f235ba`); recovered from history at `62e1ebc` — `experiments/train_models.py`, `experiments/run.py`, `experiments/experiments.ipynb` |

```bash
PYTHONPATH=. python tools/mtd_ai_weights_probe.py mtdsim-weights-archive/ \
    --filter gamma_ epsilon_ train_start_ parameter_set_ static__ time_series__
```

The drivers are the load-bearing recovery. Every claim in §2 and §4 is about code
that is no longer in the working tree, so it must be read at `62e1ebc` (Joo Kai,
*Added ablation studies*, 2024-09-26 — the last commit before submission) rather
than at `HEAD`:

```bash
git show 62e1ebc:experiments/train_models.py
git show 62e1ebc:experiments/run.py
git show 62e1ebc:experiments/experiments.ipynb
```

---

## §1 The archive, and the signature mismatch that blocks reuse outright

194 of the 198 checkpoints load under TF 2.21 / Keras 3.14; 4 fail on legacy LSTM
keyword arguments. Signature is written `static/time-series → actions`.

| Signature | Count | Whose |
|---|---:|---|
| `8/3 → 5` | 102 | Tay's sweeps, and the shared early models |
| `8/3 → 2` | 56 | Ho's per-technique binary heads (`_IPShuffle`, `_OSDiversity`, …) |
| `1/3 → 5` | 9 | Ho, single-feature |
| `2/3 → 5` | 8 | Ho, feature pairs |
| `6/2 → 2`, `6/3 → 2`, `6/2 → 5` | 4 each | Ho, intermediate layouts |
| `5/6 → 2` | 4 | Ho, late layout |
| `7/3 → 5` | 2 | shared |
| `5/6 → 5` | 1 | Ho (`main_network_roa (1)`) |
| load failure | 4 | earliest checkpoints |

**All 55 of Tay's own sweep checkpoints are `8/3 → 5`** — every `gamma_*`,
`epsilon_*_decay_*`, `train_start_*`, `parameter_set_*`, and both ablation models
(`static`, `time_series`). Confirmed independently by his driver, which declares
`state_size = 8`, `time_series_size = 3`, `action_size = 5`.

**The live code cannot feed any of them.** `get_state_and_time_series` at
[`mtd_ai_operation.py:303`](../../../../mtdnetwork/operation/mtd_ai_operation.py)
emits 5 static and 6 time-series values. The method that emits 8 and 3 — the one
Tay's weights were trained against — is the **commented-out block immediately
above it**, at
[`mtd_ai_operation.py:249-301`](../../../../mtdnetwork/operation/mtd_ai_operation.py).
Exactly 5 of the 198 checkpoints match the live signature, and none is Tay's.

Restoring the 8/3 head is therefore step one of any reuse path, and it is a
disposition rather than housekeeping: the two heads differ in *which metrics the
agent sees*, not merely in vector width. The 8/3 layout carries
`exposed_endpoints`, `shortest_path_variability` and `attack_type` as static
inputs; the 5/6 layout moves the latter two into the time-series vector and drops
`exposed_endpoints` entirely.

---

## §2 The headline — no evaluation in the paper consulted the network

Verified by reading, at five separate commits spanning Tay's whole reporting
window (`2f547d2`, `f13ed49`/`d919b45`, `6c94e7d`, `62e1ebc`, and the final merge
`5c0d8e5`). The chain is four links long and every link is in a file recoverable
from history:

1. `experiments.ipynb::Experiment.__init__` stores `self.epsilon` — **and never
   reads it again.** It appears in no call in the class.
2. `Experiment.run_trials('mtd_ai')` submits
   `mtd_ai_simulation(self.file_name, self.model_path, start_time, finish_time,
   total_nodes, new_network, self.mtd_interval, self.network_size,
   self.attacker_sensitivity)` — nine positional arguments, no epsilon.
3. `run.py::mtd_ai_simulation` has **no epsilon parameter**, so its call to
   `execute_ai_model` takes that function's default, `epsilon=1.0`.
4. `mtd_ai.py::choose_action` opens with
   `if np.random.rand() <= epsilon: return random.randrange(action_size)`.
   `np.random.rand()` draws from `[0, 1)`, so at `epsilon = 1.0` the branch is
   taken **unconditionally** and `main_network.predict` is never reached.

**Consequence.** Figure 3 (gamma), Figure 4 (epsilon and decay), Figure 5
(train start), Figure 6 (attacker detection rate) and Figure 7 (module ablation)
were all produced by a **uniform random selector over the five actions**,
including a 1-in-5 no-op. The checkpoint named on each bar had no causal
influence on the bar. The reported spreads — gamma_0.85 at 10.77 against
gamma_0.5 at 9.46, a 12.16 % difference over 100 trials — are Monte-Carlo noise
between repeated runs of one identical policy.

This also explains §5.3 without appeal to the model. `attacker_sensitivity` *is*
forwarded correctly, but the only thing it touches is `current_attack_value` in
the state vector, which is consumed solely by the network. Its one live effect is
the extra `random.random()` draw at
[`mtd_ai_operation.py:401`](../../../../mtdnetwork/operation/mtd_ai_operation.py),
which perturbs the shared RNG stream (see D-29). The paper's finding that
"below 0.7 the performance is no longer correlated with the detection rate" is
correct as far as it goes; what the data cannot support is the implied contrast,
because the 0.7–1.0 range is a 2.60 % spread of the same noise.

**How this should be described.** This is not a claim that the paper's
*architecture* is wrong — §4 is a faithful and clearly written DDQN design, and
[`mtd_ai.py::create_network`](../../../../mtdnetwork/mtdai/mtd_ai.py) implements
it correctly. It is a claim that the evaluation harness did not exercise it.
Under the guardrails' own instrument this is a `documented-nowhere` behaviour in
a *driver*, not in the substrate: the paper describes greedy action selection at
evaluation (§4.1.4, "select the action with the highest Q-value"), the harness
does not do that, and no reading of the literature licenses the harness. It is
recorded here as evidence, and what to *say* about it is Marc's call.

---

## §3 The checkpoints as inference objects — two independent failures

Both were measured with the probe. Both hold regardless of §2.

### (a) BatchNorm collapse, and a free forensic instrument

`replay()` calls `main_network.fit([state, time_series], target, epochs=1)` on a
**single sample**, once per minibatch element
([`mtd_ai.py:87`](../../../../mtdnetwork/mtdai/mtd_ai.py)). A batch of one has a
per-feature variance of exactly 0, so every BatchNormalization layer on the dense
path decays `moving_variance` as `0.99 ** n` toward zero and never recovers.

Measured: `moving_variance` is **exactly 0.0** across every BatchNorm unit in
every trained Tay checkpoint. At inference the layer then computes
`(x - mean) / sqrt(0 + 1e-3)` — a ×31.6 amplification, applied at four stacked
dense-path layers. The observed Q-value gaps of 10⁴–10⁶ are the direct signature
of that saturation. **These checkpoints are numerically broken as inference
objects independently of what they learned.**

The same arithmetic inverts into a gradient-step counter,
`n = ln(moving_variance) / ln(0.99)`, which the probe reports. It yields three
findings the filenames do not:

- **`parameter_set_10` never received a single gradient step.**
  `moving_variance == 1.0` and `moving_mean == 0.0` throughout: it is a randomly
  initialised network that was saved and then evaluated as a "parameter set".
- **`parameter_set_5` received ≈ 128 steps and `parameter_set_8` ≈ 64.**
  `parameter_set_8` is the checkpoint the radar-chart comparisons in
  `experiments.ipynb` headline.
- Every other Tay checkpoint has underflowed the estimator, so all that can be
  said is n > ~10⁴ — which is a count of *fits*, not of distinct transitions.
  §4 bounds the latter, and it is the number that matters.

### (b) Policy degeneracy

Over 400 sampled states in the plausible ranges of the eight static and three
time-series features (`--samples 400 --seed 0`):

- **34 of 55** Tay checkpoints have a greedy-policy entropy below 0.5 bits.
- Several are literally constant: `gamma_0.85` selects action 0 on 100 % of
  sampled states, `train_start_500` selects action 2 on 100 %, `gamma_0.6`
  action 2 on 100 %.

So even on the counterfactual where `predict` had been called, the majority of
these agents are constant-action deployers that do not discriminate between
network states at all.

---

## §4 The training regime as actually configured

From `train_models.py` and `run.py::execute_ai_training` at `62e1ebc`. This is
the authoritative answer to step 1 of the reintegration handoff's §5 ("establish
the parameters"), and it supersedes any reading off the constructor defaults.

| Parameter | Value |
|---|---|
| episode length | `finish_time = 5000`, `mtd_interval = 200` → **~25 transitions per episode** |
| episodes | 100 |
| network | `total_nodes = 100`, `new_network = True` — **a fresh random topology every episode** |
| replay buffer | `deque(maxlen=2000)` |
| `train_start` | 500 (gamma sweep) / 1000 (epsilon sweep) / 500–2000 (train_start sweep) / 2000 (ablations) |
| `batch_size` | 64 (gamma sweep, ablations) / 32 (epsilon, train_start sweeps) |
| `epsilon` during training | **1.0** for the gamma sweep, the train_start sweep and both ablations; swept 0.5–1.0 for the epsilon sweep |
| `epsilon_min` | 0.01 |
| ε decay | applied **once per episode** in `run.py`, not per step |
| target sync | `update_target_model` every 10 episodes — correct, and present |
| machine | `sys.path.append('/home/22489437/Documents/GitHub/MTDSim')` — a local workstation |

Three consequences, in descending order of how much they matter.

**(a) The buffer saturates before training starts.** `train_start = 2000` against
`maxlen = 2000` means training begins only once the buffer is *full*. At ~25
transitions per episode that is around episode 80 of 100 — so the ablation
models and `train_start_2000` learned across roughly **20 episodes, ≈ 500
transitions**. This is Marc's hypothesis, and it holds with the numbers attached.

**(b) The decay schedule is dimensionally wrong for the episode budget.** Decay
constants of 0.980–0.998 are per-*step* rates in the DQN literature the paper
cites (Mnih et al. [28]; van Hasselt et al. [33]). Applied per episode over 100
episodes they carry ε from 1.0 to 0.13 (at 0.98) or 0.74 (at 0.997).
`epsilon_min = 0.01` is never approached in any configuration. The agent
therefore never transitions to exploitation *during training either* — which is
the honest explanation for §6.2's observation that low initial ε "runs contrary
to the epsilon-greedy policies that other reinforcement learning models tend to
favour". It does not run contrary to anything; a lower start is simply the only
way to obtain any exploitation at all inside 100 episodes.

**(c) The inner loop is slow enough to explain the whole shape of the study.**
`replay()` performs three `predict` calls and one `fit` **per minibatch element**,
in a Python loop, all at batch size 1. Measured on the current box: 55 ms per
`predict`, 248 ms per `fit`, so one `replay()` call at batch 64 costs **26.5 s**.
Across ~50 checkpoints this is weeks of single-machine CPU. The design is not
merely slow; it is slow in a way that made the sweep unaffordable, and the
sweep is what the thesis reports.

---

## §5 The reward function — absent from the paper, present in the code, and missing the term that matters

**The paper contains no reward function.** Checked against the full submitted
PDF, figures included: §4.2 gives the Bellman target inline
(`r + γ max_a' Q(s', a')`), Equation 1 gives the optimal action-value function,
and Figure 2 has a box captioned *"Calculate Reward for Action"* with no
definition behind it. §4.2.2 defines the experience packet as
`e_t = (s_t, a_t, r_t, s_{t+1})` and says nothing about how `r_t` arises. There
is no table, equation or figure anywhere in the document that defines it.

**The code has one**, undocumented:
[`mtd_ai.py::calculate_reward`](../../../../mtdnetwork/mtdai/mtd_ai.py). It is a
weighted sum of per-feature deltas between the pre-mutation and post-mutation
state, with the deltas min-max normalised against the current replay buffer:

| Feature | Weight | Direction |
|---|---:|---|
| `attack_path_exposure` | −75 | penalise increases |
| `overall_asr_avg` | −75 | penalise increases |
| `roa` | −75 | penalise increases |
| `risk` | −75 | penalise increases |
| `overall_mttc_avg` | +75 | reward increases |
| `shortest_path_variability` | +75 | reward increases |
| `ip_variability` | +75 | reward increases |
| `host_compromise_ratio` | 0 | inert |
| `mtd_freq` | **0** | inert |
| `time_since_last_mtd` | 0 | inert |
| `attack_type` | 0 | inert |

**This is the root cause, and it is upstream of every defect in §3 and §6.**
Every term with a non-zero weight is improved by deploying a mutation: a mutation
raises `ip_variability` and `shortest_path_variability`, raises MTTC, and lowers
APE, ASR, RoA and Risk. **There is no cost term.** The one feature that could
have priced moving too often — `mtd_freq` — is explicitly weighted zero, as is
`time_since_last_mtd`.

Under this reward, **the optimal policy is to deploy on every decision.** The
no-op has no route to positive value. Two structural facts compound it:

- `calculate_reward` is called only from `MTDAITraining._mtd_execute_action`, so
  a no-op generates **no reward signal and no stored transition at all**. The
  replay buffer contains deploying actions exclusively.
- `replay()` writes `target[0][action] = ...` for the chosen action only, and
  fits against a target that equals the current prediction elsewhere. So the
  Q-value of action 0 receives **no gradient from any TD target, ever**. It
  drifts only through the shared trunk.

This is why the paper's §8 claim — that the system "minimised unnecessary MTD
deployments, which could be costly in terms of system performance and downtime" —
has nothing in the implementation that could produce it. The reward never prices
downtime, and the harness never asked the network.

Three lesser defects in the same function, recorded for completeness: the min-max
normalisation is taken over a *growing* buffer, so the reward scale is
non-stationary across training; `memory_time_series` is built from `item[5]`
(`next_time_series`) where the current-state series is `item[1]`; and
`soft_update_target_model` builds `np.array` over a ragged weight list and would
raise on any modern NumPy — it is dead code, never called.

---

## §6 The no-op costs no simulated time, so it is not reachable as a behaviour

In [`_mtd_trigger_action`](../../../../mtdnetwork/operation/mtd_ai_operation.py#L116-L150)
the `yield self.env.timeout(...)` sits **inside** the `if action > 0:` block. When
`action == 0` the `while True` loop re-enters with `env.now` unchanged.

- Under Tay's ε = 1.0 selection this is harmless rejection sampling: the loop
  redraws, expected 1.25 iterations, and **no simulated time passes**. The
  do-nothing action is silently converted into "redraw until you deploy".
- Under a **greedy** policy — the faithful evaluation — the state is unchanged at
  zero elapsed time, so the argmax is unchanged, and the loop **spins forever**.
  40 of 55 checkpoints select action 0 on at least some sampled states.

The `static_degrade_factor` guard does not rescue this: it keys on
`env.now - last_mtd_triggered_time`, and `env.now` is exactly what is not
advancing.

**This falsifies the premise of the reintegration handoff's §1.** That brief
recorded — correctly — that `action == 0` is real and gates the register-and-
trigger block, and inferred a "materially stiller network". It gates the
timeout as well, so a do-nothing decision never produces stillness; it produces
either an immediate redraw or a hang. The suppression ceiling the brief
quantified (a floor of ~7 forced mutations per 15 000 s horizon from
`static_degrade_factor = 2000`, plus the ε-greedy floor) is arithmetically
correct but describes a mechanism that is not reachable in the code as written.

Also on this path: `register_mtd` is called **twice** per decision
([lines 120 and 122](../../../../mtdnetwork/operation/mtd_ai_operation.py#L120-L122)),
enqueuing two MTDs per trigger.

---

## §7 What Tay's intent is, where the code meets it, and where it stops

Reconciled against the paper per the Brown-2023-style separation: intent from the
document, implementation from the code, divergences named rather than repaired.

**Faithfully implemented.** The four-module architecture and every layer size
(T-FX-01, T-TS-01, T-FF-01, T-Q-01); the five-action space including the no-op
(T-ACT-01); Double DQN with a separately-synced target network (T-TR-01);
experience replay with random minibatches (T-TR-02); baseline normalisation
against a no-MTD run (T-EVAL-01). `create_network` is a clean, correct
transcription of §4.1.

**Named in the paper, absent from the code.**

| Intent | Locator | Status |
|---|---|---|
| **Downtime / Operational Impact for Node Replacement** as a time-series input | §4.1.2 ¶4 (T-TS-02) | **not implemented in any form.** This is the availability half of "when to move" (§2.3), and the only feature that could make the no-op rational |
| Number of Vulnerabilities; Number of Exposed Vulnerabilities as static inputs | §4.1.1 ¶3 (T-FX-02) | not implemented as named; `exposed_endpoints` is the nearest analogue. **Ruled low-priority by Marc, 2026-08-07** |
| Greedy action selection at evaluation | §4.1.4 | not done — §2 |

**In the code, not in the paper.** The reward function (§5); `overall_asr_avg`,
`roa` and `risk` as state inputs; `shortest_path_variability` and
`ip_variability`; the 60 s compromise window (`comp_check_interval = 60`);
`static_degrade_factor`; the ε-greedy evaluation path.

The `Downtime` row is the important one, and the substrate is already most of the
way to it. `MTD_DURATION` in
[`mtdnetwork/data/constants.py`](../../../../mtdnetwork/data/constants.py) gives
per-mechanism execution durations as `(mean, std)` — CompleteTopologyShuffle 110,
HostTopologyShuffle 100, IPShuffle 100, OSDiversity 80, PortShuffle 70,
ServiceDiversity 70, UserShuffle 20 — sourced from Zhang 2023 Table 3 and badged
**faithful** in [`../../provenance.md`](../../provenance.md). Every executed
mutation already writes `(start_time, finish_time, duration)` into `mtd_stats`
via `append_mtd_operation_record`, and the application/network/reserve
`simpy.Resource` seizure already models one mechanism blocking another. What does
not exist is (i) a scalar availability metric derived from those records, (ii) a
state feature carrying it, and (iii) a reward term charging it.

---

## §8 Consequences for the programme

**The reuse-versus-retrain question is dissolved, not answered.** The
reintegration handoff's §2 framed reused weights as the *control* against which a
retrained agent's out-of-distribution risk could be measured. That framing
required Tay's reported behaviour to be the behaviour of his weights. It is not:
his reported behaviour is a uniform random selector over
`{no-op, CompleteTopologyShuffle, IPShuffle, OSDiversity, ServiceDiversity}`.
**The project already has that control** — a random-scheme defender over the same
four mechanisms, in the existing pool, with no neural network and no
out-of-distribution question. It is a cheaper and stronger control than the one
proposed, and it is the honest replication of Tay's published results.

**What may be claimed about Tay's work, precisely.** That the architecture is
specified and implemented faithfully; that the evaluation harness did not
exercise it; and that consequently the reported hyperparameter, detection-rate
and ablation results characterise a random selector rather than a learned policy.
What may **not** be claimed is that the architecture cannot work — nothing here
tests that.

**What this costs the stealth programme.** Every consequential stealth claim was
gated on a reactive defender that responds to attacker behaviour. That defender
does not currently exist in a usable state, and cannot be obtained by loading a
checkpoint. It has to be rebuilt: the state head restored, the no-op made to cost
time, the transition store made to record it, the reward given a cost term, and
the whole thing retrained. That work is scoped in
[`../../../handoffs/2026-08-07_mtd_ai_cost_calibrated_rebuild.md`](../../../handoffs/2026-08-07_mtd_ai_cost_calibrated_rebuild.md).

---

## §9 Dispositions opened

Numbered in a local namespace; Marc folds them into the D-series in
[`../../intent_conformance_audit.md`](../../intent_conformance_audit.md) if and
as he rules on them. None is repaired by this record.

| # | What | Evidence | Recommendation |
|---|---|---|---|
| **MTDAI-01** | The evaluation harness selects uniformly at random (`epsilon` defaults to 1.0 and is never overridden), so no reported figure consulted the network | §2 | Record as a property of the inherited work; do not reuse any published figure as a comparator |
| **MTDAI-02** | The live 5/6 state head cannot feed any Tay checkpoint; the 8/3 head is commented out | §1 | Restore the 8/3 head, or declare a new feature set — a disposition either way, because the two heads see different metrics |
| **MTDAI-03** | The no-op does not advance simulated time; greedy evaluation livelocks | §6 | Repair — the yield belongs outside the `action > 0` block, with its own timeout. Blocks every stealth claim |
| **MTDAI-04** | No transition is stored for `action == 0`, so its Q-value is never a TD target | §5 | Repair alongside MTDAI-03; they are the same defect seen from the learning side |
| **MTDAI-05** | The reward has no cost term (`mtd_freq` and `time_since_last_mtd` weighted 0), so "always deploy" is optimal | §5 | Add a downtime charge; the weight is the calibration knob, and it must be swept |
| **MTDAI-06** | `Downtime / Operational Impact` (T-TS-02) is specified by Tay and implemented nowhere | §7 | Build as a derived network metric over `mtd_stats`; the per-mechanism durations already exist and are provenance-badged |
| **MTDAI-07** | Batch-size-1 `fit` collapses every BatchNorm `moving_variance` to 0 | §3(a) | Repair before any retrain — batched updates, or LayerNorm |
| **MTDAI-08** | `register_mtd` is called twice per decision | §6 | Repair; bounded re-baseline |
| **MTDAI-09** | `attack_success_rate = compromised_num / attack_event_num` is unguarded, and `attack_event_num` counts `SCAN_PORT` rows only within a 60 s window | [`mtd_ai_operation.py:383`](../../../../mtdnetwork/operation/mtd_ai_operation.py) | Was already item 1 of the reintegration handoff's §3. The quiet-attacker condition is exactly what triggers it |
| **MTDAI-10** | `roa` and `risk` are single samples (`[-1]`), not aggregates | [`mtd_ai_operation.py:368-369`](../../../../mtdnetwork/operation/mtd_ai_operation.py) | Already item 2 of that §3. Record before any steering claim leans on them |
| **MTDAI-11** | `comp_check_interval = 60` appears nowhere in Tay's paper | §7 | Documented-nowhere; record as an inherited constant with no source |
| **MTDAI-12** | `calculate_reward` normalises against a growing buffer (non-stationary scale) and reads `item[5]` where `item[1]` is meant | §5 | Repair with the reward rework, not separately |
