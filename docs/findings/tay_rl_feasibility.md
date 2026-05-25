# Tay RL agent — feasibility for benchmark replication

**Phase:** 2 (recon).  **Date:** 2026-05-25.
**Scope:** `mtdnetwork/mtdai/` + `mtdnetwork/operation/mtd_ai_*.py` on
`chore/phase2-recon` (off `chore/baseline-spec`). Goal: determine what it
costs to make Tay's RL agent runnable for **benchmark replication only** —
not to extend, retrain from scratch, or generalise to new architectures.

> Direction reminder (from CLAUDE.md): "Tay's RL agent and its detection-
> sensitivity machinery are retained only as an inherited **benchmark
> defence mechanism to replicate** — never to extend."

---

## TL;DR — runnable today, with caveats

- **TF imports succeed** on the existing `mtdsim` conda env (TF **2.21.0**,
  Keras **3.14.0**, Python 3.11.15). No env delta required to import or to
  build the model architecture.
- **A fresh DDQN builds cleanly** — `create_network(state_size=7,
  action_size=5, time_series_size=3)` returns a 46,533-param model with
  the two-branch Dense+LSTM+Fusion shape from Tay §4.1.
- **Tay's pretrained weights load** — the four `models_joo_kai/main_network_*.h5`
  files deleted in commit `e5935ab` still load under TF 2.21/Keras 3.14 via
  `tensorflow.keras.models.load_model(..., custom_objects={'mse': mse})`.
  46,661 params (~+128 vs a freshly-built one because the saved model
  carries BN running stats from training).
- **A 2,000 s mtd_ai sim runs end-to-end** with `epsilon=1.0` (random
  policy). 10 MTDs fired, 8/50 hosts compromised at seed 42.
- **`_register_mtd_ai` exposes Tay's 5-action set, not Ho's pairwise
  space** — C4 resolved (§3).
- **Caveat 1 (load-bearing for replication):** Tay's saved model expects
  **8 static + 3 time-series features**. The current `Evaluation.get_metrics`
  returns only **7 static + 3 time-series** — it drops `exposed_endpoints`
  and `attack_type` and substitutes `total_number_of_ports`. To consume
  Tay's pretrained weights you have to **reconstruct the missing two
  static features in the feature pipeline**; otherwise the model errors
  on `(None, 8) ← (None, 7)` shape mismatch at `model.predict`. (§4)
- **Caveat 2 (trust):** the same R1/R2/R3 chain documented in
  [crash_6000s.md](crash_6000s.md) is present in `mtd_ai_operation.py` /
  `mtd_ai_training.py`, but partially mitigated — the `mtd_ai` trigger loop
  does `return` after `succeed()` (line 86, [mtd_ai_operation.py:75-86](../../mtdnetwork/operation/mtd_ai_operation.py#L75-L86)),
  unlike the non-AI loop. The R3 early-return-without-release leak in
  `_mtd_execute_action` is still present in the AI surface
  ([mtd_ai_operation.py:165](../../mtdnetwork/operation/mtd_ai_operation.py#L165)
  / [mtd_ai_training.py:158](../../mtdnetwork/operation/mtd_ai_training.py#L158)). (§5)
- **Caveat 3 (snapshots):** Tay's `experiments/run.py::execute_ai_model`
  defaulted `new_network=False` and *loaded* a pickled `TimeNetwork` snapshot
  from `experiments/snapshots/network_{N}n.pkl`. Those snapshots existed at
  commit `e5935ab^` but were deleted with the rest. **No snapshot →
  `FileNotFoundError`, then a silent `return`**. Replication must rebuild
  the snapshot pool (cheap — one call per network size — but not zero work).
- **Verdict:** safe enough to schedule a *replication* attempt; **don't trust
  the runtime traces of long-horizon AI runs** until the R3 leak is fixed
  on the AI surface as well.

---

## 1. Environment — no delta required

`environment.yml` on `chore/baseline-spec` does not list TensorFlow. Phase-0
finding F-03 records that the deleted `experiments/run.py` imported it at
module top, which was why `experiments/run.py` was un-runnable in the Phase-0
env. The *current* local `mtdsim` conda env *does* have TF installed
(presumably from Marc's earlier MTD-AI work that pre-dated the env-rename
on `feat/replay-viz`, commit `9b4fd3d`).

```text
TF version:    2.21.0
Keras version: 3.14.0
Python:        3.11.15  (mtdsim env)
```

The deleted `experiments/run.py` imported a handful of TF-specific symbols
that the current Keras 3 ABI re-exports unchanged:

```python
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.utils import register_keras_serializable
import tensorflow as tf
```

All five imports succeed under TF 2.21. **No version pin or downgrade is
required** for benchmark-only use.

> **Do not commit TF to `environment.yml`** (per the brief). The current
> env on disk already has it; pinning would couple Phase-0 / Phase-1
> non-AI work to a heavy dep it doesn't need. If Marc wants reproducibility
> for the AI runs specifically, put it in a separate `environment-ai.yml`
> or document the `pip install tensorflow==2.21` step in the replication
> notebook.

---

## 2. Fresh model builds; pretrained loads

```python
from mtdnetwork.mtdai.mtd_ai import create_network
m = create_network(state_size=7, action_size=5, time_series_size=3)
# → Model: 46,533 params, inputs [(None, 7), (None, 3, 1)], output (None, 5)
```

The layer counts match the spec rows **SHD-05** (`Dense 128 → ReLU → BN →
Dense 64 → ReLU → BN → Dropout 30 %`), **SHD-06** (`LSTM 64 → BN → LSTM 32 →
BN → Dropout 30 %`), **SHD-07** (`Concat → Dense 64 → ReLU → BN → Dropout
30 %`), **SHD-08** (`Dense 5`). These rows can be promoted from `unverified`
to `verified (arch)` in the spec.

Loading Tay's deleted `main_network_epsilon_0.5_decay_0.99.h5` from commit
`e5935ab^`:

```python
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import register_keras_serializable
@register_keras_serializable()
def mse(y_true, y_pred): ...
m = load_model('/tmp/tay_model.h5', custom_objects={'mse': mse})
# → 46,661 params, inputs [(None, 8), (None, 3, 1)], output (None, 5)
```

Loaded fine. **One warning** from Keras 3 (`compile_metrics will be empty
until you train or evaluate`) — cosmetic, no behavioural impact.

The `+128` parameter delta vs a fresh build is the four trained BN layers'
`moving_mean` + `moving_variance` weights (each shape `(64,)` or `(32,)`).
Expected.

---

## 3. C4 (action set) — resolved

[mtdnetwork/component/mtd_scheme.py:103-110](../../mtdnetwork/component/mtd_scheme.py#L103-L110):

```python
def _register_mtd_ai(self, mtd_technique):
    ...
    self._mtd_register(mtd=self._mtd_custom_strategies[mtd_technique - 1])
```

[mtdnetwork/operation/mtd_ai_operation.py:95-112](../../mtdnetwork/operation/mtd_ai_operation.py#L95-L112) confirms the call site:

```python
if (self.env.now - self.network.get_last_mtd_triggered_time()) > self.static_degrade_factor:
    action = random.randint(1, len(self.mtd_strategies) + 1)
else:
    action = choose_action(state, time_series, self.main_network, len(self.mtd_strategies) + 1, self.epsilon)
...
if action > 0:    # action == 0 is the no-op
    self._mtd_scheme.register_mtd(mtd_action=action)
```

So with `mtd_strategies = [CompleteTopologyShuffle, IPShuffle, OSDiversity,
ServiceDiversity]`:

- `action_size` passed to the model = **5**
- Action `0` = **no-op** (no MTD scheduled this tick)
- Actions `1 … 4` index into the 4-strategy list

This is **Tay's 5-action set** exactly (§4.1 of Tay 2024 — IPShuffle,
OSDiversity, ServiceDiversity, CompleteTopologyShuffle, no-op). It is
**not** Ho's pairwise space (Ho §3.2.3 specifies `{MTD_1, …,
MTD_{n(n+1)/2}, Null}` — for 4 base MTDs that would be 11 actions).

**C4 verdict:** `divergent` → `verified (Tay)`. Spec rows `SHD-03`
(Tay 5-action) becomes `verified`. `SHD-04` (Ho pairwise) becomes
`out-of-scope (not exposed via _register_mtd_ai)`.

The Phase-1 spec note on `SHD-04` (*"Conflict candidate — `_register_mtd_ai`
indexes into a `_mtd_custom_strategies` list — likely Tay's variant"*) is
now confirmed: Tay's variant, no pairwise wiring anywhere in
`mtd_ai_operation.py` or `mtd_scheme.py`.

---

## 4. Feature-set drift — the load-bearing replication caveat

Tay's `experiments/run_experiment.ipynb` (deleted in `e5935ab`) defined:

```python
static_features = ["host_compromise_ratio", "exposed_endpoints",
                   "attack_path_exposure", "overall_asr_avg", "roa",
                   "shortest_path_variability", "risk", "attack_type"]
time_features  = ["mtd_freq", "overall_mttc_avg", "time_since_last_mtd"]
```

8 static + 3 time-series → matches the pretrained model input shape
`(None, 8)` + `(None, 3, 1)`.

The current `Evaluation.get_metrics`
([evaluation.py:149-199](../../mtdnetwork/statistic/evaluation.py#L149-L199))
returns:

```python
state_array       = [host_compromise_ratio, total_number_of_ports,
                     attack_path_exposure, overall_asr_avg, roa,
                     shortest_path_variability, risk]              # 7
time_series_array = [mtd_freq, overall_mttc_avg, time_since_last_mtd]  # 3
```

**Two missing static features:**

1. **`exposed_endpoints`** — count of exposed-endpoint hosts. Trivially
   recoverable: `len(network.exposed_endpoints)`. **Easy fix.**
2. **`attack_type`** — int code of the current adversary phase. Recoverable
   from `self.attack_dict[self.adversary.get_curr_process()]` — exactly the
   dict used in `mtd_ai_operation.py:54-61`. **Easy fix.**

**One substituted feature:**

3. `total_number_of_ports` was added in place of something Tay didn't use
   (probably this is a Ho 2024 metric — MET-row to confirm). For Tay-only
   replication it should be excluded from the static_features list, or
   re-positioned so the projection logic in
   [mtd_ai_operation.py:430](../../mtdnetwork/operation/mtd_ai_operation.py#L430)
   (`state_array = np.array([value if key in self.features["static"] else 0 for key, value in state_filter.items()])`)
   masks it to zero.

The projection logic does mask non-listed features to zero, so feeding the
pretrained model a state vector that *has* `total_number_of_ports` in
position 1 and zero elsewhere will produce silently-degraded predictions
rather than a shape error. **Either way you need to verify the positional
ordering matches Tay's training-time ordering** before trusting the
inference output.

This is the single highest-effort piece of replication work. Estimate:
half a day to wire up the two missing features + a small alignment test
that runs Tay's pretrained model on a static fixture and compares the
top-1 action to a known-good ground-truth output saved at training time.
(Marc has no such fixture in repo — would need to be derived from the
deleted notebooks if available, or accepted as a "weights load + sim
runs" replication and not a bit-for-bit policy replication.)

---

## 5. Trust audit — same scheduler chain as `crash_6000s.md`

| Defect (from [crash_6000s.md](crash_6000s.md)) | Status in `mtdnetwork/mtdai` + `mtd_ai_operation.py` |
|---|---|
| **R1** (`is_compromised` ignores `terminate_compromise_ratio`) | Same `TimeNetwork.is_compromised` — **same bug**. Same hard-coded 0.25. |
| **R2** (`_mtd_trigger_action` doesn't `return` after `succeed()`) | **Different**: AI surface *does* `return` ([mtd_ai_operation.py:86](../../mtdnetwork/operation/mtd_ai_operation.py#L86)). One of the few places it was done right. |
| **R3** (early-return without resource release in `_mtd_execute_action`) | **Same bug** — see [mtd_ai_operation.py:165](../../mtdnetwork/operation/mtd_ai_operation.py#L165) and [mtd_ai_training.py:158](../../mtdnetwork/operation/mtd_ai_training.py#L158). The leak still happens once at end-of-sim; not a runaway. |

So the AI surface is *less* affected than the procedural one — the R2 fix
doesn't need to be ported here, only R3 does. Combined with the R1 fix
(which is a single location in `time_network.py`), the AI replication
surface becomes trustworthy with the same set of fixes proposed for the
non-AI scheduler.

Other AI-surface oddities surfaced during the smoke run that are worth a
clean-up pass before relying on long traces:

- `mtd_ai_operation.py:118, 121` calls `self.network.scorer.register_mtd(...)`
  twice per loop with the result of the second `register_mtd` call as
  argument — looks like a copy-paste duplication. Marc's `1efac8f` on
  `feat/replay-viz` already removes this in the reorged twin file (cherry-
  pick noted in [replay_viz_inventory.md](replay_viz_inventory.md) §B).
- Loud `print('Filtered State Array:', ...)` debug spew on every tick
  (seen in the smoke run, ~9 prints / 100 sim-seconds). Easy to silence.

---

## 6. Recommended replication path (don't execute — for fix session)

1. **Stage Tay's pretrained model.** Restore `experiments/AI_model/models_joo_kai/main_network_epsilon_0.5_decay_0.99.h5` from `e5935ab^` into `mtdnetwork/mtdai/models/` (or a `.gitignore`d directory) and document the restoration in the replication notebook.
2. **Rebuild the snapshot pool.** Mirror Tay's `create_experiment_snapshots(network_size_list)` call ([deleted run.py:120-125](#)) for the network sizes Tay ran against. Outputs go to `experiments/snapshots/` (already `.gitignore`d).
3. **Add the two missing static features to `Evaluation.get_metrics`.** `exposed_endpoints` (1 line) and `attack_type` (3-line lookup against `self.attack_dict`). Keep the ordering Tay's notebook used.
4. **Land the R1 + R3 fixes** ([crash_6000s.md](crash_6000s.md) §6). R3 needs porting into both `mtd_ai_operation.py::_mtd_execute_action` and `mtd_ai_training.py::_mtd_execute_action`.
5. **Run a single 15 ks replication.** Tay's primary headline (Tay §5.3, Fig 6) is the attacker-detection-rate sensitivity sweep at `sensitivity ∈ [0, 1]`. The current code preserves `attacker_sensitivity` as a constructor arg ([mtd_ai_operation.py:398](../../mtdnetwork/operation/mtd_ai_operation.py#L398)) — exercisable directly.
6. **Compare to Tay's published cutoff ≈ 0.7.** If the replicated sweep crosses near 0.7 the benchmark is faithful enough to use as a baseline for the OGASP evaluation (Stream C).

Total estimated effort, ignoring schedule: ~1-2 days for the bench
replication, mostly dominated by step 3 + a feature-alignment sanity check.
The replication does **not** require retraining, does **not** require
`mtd_ai_training.py` to run, and does **not** touch Marc's GAP/GASP
attacker work.

---

## 7. What this finding does *not* answer

- Whether the trained-model **action distribution** matches Tay's published
  Fig 4/5 histograms. Bench replication can produce a runnable sim but
  doesn't verify it learns the same policy.
- Whether `attacker_sensitivity` is implemented consistently with Tay §5.3
  (the body of `mtd_ai_operation.py:398` is what enforces it; quick read
  suggests it gates observation, not action, which matches Tay — but
  out of scope here).
- Whether `MTDAITraining`'s reward function matches Ho §3.2.4 reward shape
  (the file imports `calculate_reward` from a path that doesn't exist on
  `main` — look at `mtdnetwork/statistic/utils.py` or it will need to be
  pulled back from `e5935ab^`).
