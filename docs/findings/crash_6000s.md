# Crash diagnosis — "~6,000 s crash" at Tay-flagship config

**Phase:** 2 (recon).  **Author:** Marc Labouchardiere.  **Date:** 2026-05-25.
**Branch under test:** `chore/phase2-recon` (off `chore/baseline-spec`, which carries Phase-0 + Phase-1 spec on top of `main` `c706871`).

> **Note.** "Phase-0 config" as used in this finding follows Marc's own usage on
> `feat/replay-viz`, where `viz/replay/config.py` defines `PRIMARY` = Tay's
> flagship `(total_nodes=100, total_endpoints=5, total_subnets=8, total_layers=4,
> total_database=2, terminate_compromise_ratio=0.8)` with `finish_time=15000` —
> *not* the Phase-0 baseline driver's smaller `total_nodes=50` test config in
> [baseline/run_baseline.py](../../baseline/run_baseline.py). The 50-node Phase-0
> driver does not exhibit the symptom (see §5 below).

---

## TL;DR

The "crash" is **not** a Python exception. It is a silent integrity failure of
the MTD scheduler that begins the moment the **hard-coded 0.25 compromise
threshold** ([mtdnetwork/component/time_network.py:50](../../mtdnetwork/component/time_network.py#L50))
fires, which on the PRIMARY (100-node) configuration happens at
**sim_t ≈ 6,500 s** with seed 42. After that:

1. `end_event.succeed()` is called inside `_mtd_trigger_action` but the loop
   **does not `return`** — it keeps scheduling new MTDs against the dead
   simulation.
2. Each subsequent `_mtd_execute_action` hits the post-timeout `is_compromised`
   gate and **returns early without releasing its `simpy.Resource` request slot**
   and without writing a record to `MTDStatistics`.
3. Within ~2 trigger ticks both the `network` and `application` layer resources
   are permanently held; all later MTDs route to the suspension dict (deduped by
   priority → most are discarded). The recorded MTD count stops growing.
4. The attacker keeps running because the driver uses `env.run(until=finish_time)`,
   not `env.run(until=end_event)`. With no effective defence after t≈6,500 s the
   compromise count climbs to ~95/100.

On `main`, this manifests as headline metrics being silently wrong (MTTC,
ASR, MTD execution frequency all reflect a sim where MTD effectively stopped
firing two-thirds of the way through). On `feat/replay-viz` the same chain is
re-exposed by a deliberate event-log linter that fails on `mtd_deployed` with
no matching `mtd_completed` / `mtd_aborted` — that is the "crash" Marc has been
seeing, and the reason `current_state.md` calls it a *resource-allocation /
scheduling* failure rather than an exception.

---

## 1. Minimal repro (no `src/mtdsim/`, no fixes applied)

```python
PYTHONPATH=. python - <<'PY'
import random, time
import numpy as np, simpy
from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.operation.mtd_operation import MTDOperation
from mtdnetwork.statistic.security_metric_statistics import SecurityMetricStatistics

random.seed(42); np.random.seed(42)
env, end = simpy.Environment(), None
end = env.event()
tn = TimeNetwork(total_nodes=100, total_endpoints=5, total_subnets=8, total_layers=4,
                 target_layer=4, total_database=2, terminate_compromise_ratio=0.8)
adv = Adversary(network=tn, attack_threshold=ATTACKER_THRESHOLD)
ao  = AttackOperation(env=env, end_event=end, adversary=adv, proceed_time=0)
ao.proceed_attack()
mo  = MTDOperation(security_metrics_record=SecurityMetricStatistics(),
                   env=env, end_event=end, network=tn, scheme='random',
                   attack_operation=ao, proceed_time=0,
                   mtd_trigger_interval=200, custom_strategies=None, adversary=adv)
mo.proceed_mtd()

for cap in range(500, 15500, 500):
    env.run(until=cap)
    if end.triggered and cap % 500 == 0 and not getattr(env, "_seen", False):
        env._seen = True
        print(f"end_event at sim_t={env.now} comp={len(adv.get_compromised_hosts())}/100")

print("MTDs recorded:", len(tn.get_mtd_stats().get_record()))
print("net users:", len(mo.network_layer_resource.users),
      "app users:", len(mo.application_layer_resource.users),
      "suspended:", sorted(tn.get_suspended_mtd().keys()))
PY
```

Observed (with this Phase-0 environment — Python 3.11, simpy 4.1.1):

```
  t=2000 comp=1/100  MTDs=10  net_users=0 app_users=0 susp=[]
  t=4000 comp=11/100 MTDs=20  net_users=0 app_users=0 susp=[]
  t=6000 comp=24/100 MTDs=30  net_users=0 app_users=0 susp=[]
END_EVENT triggered at sim_t=6500.00 cap=6500 comp=31/100
  t=8000 comp=56/100 MTDs=30  net_users=1 app_users=1 susp=[4]
  t=10000 comp=81/100 MTDs=30 net_users=1 app_users=1 susp=[4]
  t=12000 comp=95/100 MTDs=30 net_users=1 app_users=1 susp=[4]
  t=14000 comp=95/100 MTDs=30 net_users=1 app_users=1 susp=[4]
FINAL  sim_t=15000.00 wallclock=1.34 s  comp=95/100  MTDs=30
```

The signature: `MTDs` and `suspended` both freeze after `end_event` triggers
at ~6.5 ks; resource user-counts go 0→1 once and never come back down; the
trigger loop keeps spinning for another 8.5 ks producing nothing but orphans.

A re-run with `total_nodes=50` (Phase-0 driver default) shows the same chain
but earlier (~3 ks) because the 25 %-of-50 threshold is even easier to reach;
the symptom is therefore present in the baseline golden runs too, but its
*effect* is hidden because the baseline only runs to `finish_time=3000`.

---

## 2. Root cause — three interacting defects

| # | Locator | Defect |
|---|---|---|
| **R1** | [time_network.py:50](../../mtdnetwork/component/time_network.py#L50) | `is_compromised` returns `len(compromised) / total_nodes > 0.25` regardless of `terminate_compromise_ratio` (the constructor arg defaults to `0.8` and is never stored on `self`). This is spec conflict **C6 / MET-15** — Zhang §5 specifies `0.8`. |
| **R2** | [mtd_operation.py:77-79](../../mtdnetwork/operation/mtd_operation.py#L77-L79) | `_mtd_trigger_action` calls `end_event.succeed()` on first `is_compromised` but does **not** `return`. The `while True` loop continues to register and trigger MTDs. The batch (`simultaneous`) variant `_mtd_batch_trigger_action` does `return` at line 119 — the two paths diverge here. |
| **R3** | [mtd_operation.py:172-174](../../mtdnetwork/operation/mtd_operation.py#L172-L174) | `_mtd_execute_action` early-returns on `is_compromised` after acquiring the resource (`request = self._get_mtd_resource(mtd).request(); yield request`) but before `self._get_mtd_resource(mtd).release(request)`. Every triggered-after-compromise MTD leaks one resource slot. The `network` and `application` layer resources each have `capacity=1`, so after 1 leak per layer the resource is permanently held. |

R1 sets the *time* at which the symptom triggers (sim time, not wall time);
R2 is what keeps the trigger loop alive after compromise; R3 is what turns
that into a hard leak. R2+R3 alone would be a one-shot leak per layer; combined
with R1 firing 3× earlier than Zhang's intended ratio, the failure happens early
enough to dominate the simulated horizon.

Marc's `feat/replay-viz` branch already carries a partial fix for **R3** in
commit `c426f1b` ("Ensure MTD resource release and cleanup" — `try`/`finally`
release) and for **R2 + R3** in commit `0d1bdae` (adds `return` after `succeed()`
and `drain_in_flight()` for unclosed deploys at sim end). Neither is on `main`
or `chore/baseline-spec`.

---

## 3. Introducing commits

> Bisect was done by `git log -L` on the two affected functions rather than
> the formal `git bisect run` workflow — both edits are single-commit one-liners,
> the symptom is silent on `main`, and the file moved between `mtdnetwork/event/`
> and `mtdnetwork/operation/` mid-history, which would have broken `bisect run`.

| Defect | First seen | Author / date | Commit subject |
|---|---|---|---|
| **R3** (early-return without release in `_mtd_execute_action`) | `6a7a2907` | moebuta · 2022-09-25 | "refactor adversary/mtd/network to facilitate state saving process." — block was added inside the *same* commit that introduced the function, so this is an "as-built" defect, not a regression. |
| **R2** (`succeed()` without `return` in `_mtd_trigger_action`) | `e369b09` | moebuta · 2023-03-19 | "update experimental files, snapshots, and evaluation metrics" — added the `is_compromised`+`succeed()` block. `0bf6280` (Bsubs · 2024-03-24, "Created first tensorflow model") later wrapped the `succeed()` in `if not self.end_event.triggered:` but still no `return`. |
| **R1** (0.25 threshold) | `6ae1fd4` | **Will Ho** · 2024-09-08 | Commit subject is literally `"debug"`. Replaced the previous `> 0.8` (set in `4b88179` "fix bugs", 2023-03-25 — *itself* a tightening of an even earlier `> 0.7` from `55a1971` "restore parameter values") with `> 0.25`, leaving the old line in as a comment. No PR, no body, no message. See §4. |

So there is **no single "introducing commit"** — the cascade was assembled
across three of moebuta's 2022-23 commits and capped by Will Ho's 2024
`debug` commit. The R1 commit is the one that *exposes* the latent R2/R3 by
moving the trigger time from ~unreachable (compromise > 80 %) to ~6.5 ks
(compromise > 25 %).

---

## 4. C6 provenance — where did 0.25 come from?

Full history of the `is_compromised` return value, oldest → newest:

| Commit | Date | Author | Value | Commit subject |
|---|---|---|---|---|
| `8359b6f` | 2022-11-18 | moebuta | (no return — `super().is_compromised(...); pass`) | "rename folders, amend code structure" |
| `e369b09` | 2023-03-19 | moebuta | `>= 0.9` | "update experimental files, snapshots, and evaluation metrics" |
| `55a1971` | 2023-03-25 | moebuta | `> 0.7` | "restore parameter values" |
| `4b88179` | 2023-03-25 | moebuta | `> 0.8` (comment says "80 % compromise ratio") | "fix bugs" |
| **`6ae1fd4`** | **2024-09-08** | **Will Ho** | **`> 0.25`** (with the previous `> 0.8` left in as a comment) | **`debug`** |

The 0.8 ratio in `4b88179` matches Zhang 2023 §5 ("NCR = 0.8 terminating
condition"). Will Ho's `6ae1fd4` is a five-character commit subject (`debug`),
no body, no PR — it touches CSV outputs, snapshot pickles, and `experiments/run.py`
alongside the threshold change. The natural reading is *a debug-time tweak
that shortened the sim for faster iteration on Ho's MTD-AI experiments and
got committed by accident*. There is no paper-side rationale.

**Disposition for C6:** treat as a **bug** (debug leftover), not a deliberate
divergence. Fix is the obvious one — store `terminate_compromise_ratio` on
`self` in `TimeNetwork.__init__` and use it in `is_compromised`. Marc's
`docs/known_issues.md` on `feat/replay-viz` already says the same thing.

---

## 5. F-06 / F-07 — implicated?

| Finding | Implicated in 6 ks chain? | Notes |
|---|---|---|
| **F-06** — `Network.gen_graph` infinite-loop guard | **No.** | The PRIMARY config (`total_subnets=8, total_layers=4`) is well clear of the `total_subnets >= total_layers + 3` rule of thumb in `docs/known_issues.md`. No infinite-loop spin observed during repro. F-06 is a parameter-validation defect, orthogonal to the compromise-time leak. |
| **F-07** — `Evaluation.__init__` filesystem side-effect | **No, but adjacent.** | `MTDOperation.__init__` constructs an `Evaluation(...)` ([mtd_operation.py:48](../../mtdnetwork/operation/mtd_operation.py#L48)), and `Evaluation.__init__` calls `self.create_directories()` ([evaluation.py:19](../../mtdnetwork/statistic/evaluation.py#L19)) which `mkdir`s `<cwd>/experimental_data/plots/`. This fires *once* per `MTDOperation` instance, not per leak, so it doesn't *cause* the 6 ks chain. It is, however, the same code that any clean fix will touch (the `Evaluation` construction is what would also need to be moved or made event-loggable in Marc's reorg). Worth bundling. |

---

## 6. Recommended fix locations (for the fix session — **do not fix here**)

Listed by smallest-blast-radius first; **all three must land together** because
fixing only R1 makes the symptom disappear at PRIMARY but R2+R3 still leak on
any other config that hits the threshold (e.g. a longer run, a smaller network,
a less-effective MTD scheme). Fixing only R2+R3 leaves the metrics-corrupting
2/3-of-horizon dead time intact.

1. **R1 — honour `terminate_compromise_ratio`.** [mtdnetwork/component/time_network.py:10-22, 47-50](../../mtdnetwork/component/time_network.py#L10-L50).
   Store the constructor arg on `self`; return `>= self._terminate_ratio`.
   Default 0.8 restores Zhang. Touches one file.
2. **R2 — `return` after `succeed()` in the non-batch trigger loop.**
   [mtdnetwork/operation/mtd_operation.py:75-80](../../mtdnetwork/operation/mtd_operation.py#L75-L80).
   Match `_mtd_batch_trigger_action`'s shape ([line 119](../../mtdnetwork/operation/mtd_operation.py#L119)).
3. **R3 — `try`/`finally` release in `_mtd_execute_action`.**
   [mtdnetwork/operation/mtd_operation.py:156-191](../../mtdnetwork/operation/mtd_operation.py#L156-L191).
   Marc's `c426f1b` (`feat/replay-viz`) is the reference shape: wrap from `yield request`
   to end in `try`, release in `finally` if `request in resource.users`, and pop the
   `unfinished_mtd` entry.

A driver-side alternative (orthogonal, not a substitute) is to switch from
`env.run(until=finish_time)` to `env.run(until=simpy.events.AnyOf(env, [end_event, env.timeout(finish_time)]))`
in [baseline/run_baseline.py:221](../../baseline/run_baseline.py#L221). That stops the trigger
loop the moment compromise fires but leaves R1/R2/R3 latent for anyone who
keeps the existing driver shape. Marc's `runner.py` on `feat/replay-viz` already
takes this approach as a belt-and-braces complement to the in-tree fixes.

The Phase-0 golden outputs in `baseline/golden/` were produced at
`finish_time=3000`, which is *before* the threshold trips on the 50-node config,
so applying these three fixes should leave the no-MTD and single-MTD goldens
byte-identical and only perturb the multi-scheme goldens to the extent they
ran past their (now-honoured) 0.8 termination — verify in the fix session.

---

## 7. What this finding does *not* answer

- Whether the same chain exists in `mtd_ai_operation.py` / `mtd_ai_training.py`.
  Both files carry the same R3-shaped early-return pattern
  ([mtd_ai_operation.py:165](../../mtdnetwork/operation/mtd_ai_operation.py#L165),
  [mtd_ai_training.py:158](../../mtdnetwork/operation/mtd_ai_training.py#L158)); their
  trigger-side loops were not inspected because TF isn't installed. Flagged for the
  Tay-RL feasibility finding ([tay_rl_feasibility.md](tay_rl_feasibility.md)).
- Whether the suspension-dict deduplication-by-priority masks any *further* bugs
  (e.g. priority-collision discards that look like leaks). Out of scope here.
