---
status: open
created: 2026-08-07
---

# Rebuild `mtd_ai` into an agent that trades cost against risk, and prove it does before any Kaya time is spent

**Absorbs and replaces the `mtd_ai` reintegration brief** (`2026-08-06`, deleted
in the commit that opened this one; `git log -- docs/handoffs/2026-08-06_mtd_ai_reintegration.md`),
whose two load-bearing premises were falsified by
[`../implementation/pipeline/ogasp/mtd_ai_forensics.md`](../implementation/pipeline/ogasp/mtd_ai_forensics.md)
(2026-08-07) — see that record's §6 and §8 for the falsifications themselves. Its
surviving content — the defect list, the determinism gate, the wiring seam, the
hard constraints — is carried forward here in full, and nothing in it needs to be
read from the deleted file.

**The deliverable is a go/no-go, not a trained model.** This handoff ends at a
CPU-scale calibration result that either shows the agent trading downtime against
security posture, or shows it cannot. Kaya time is spent only after that result
lands. Marc's bar, in his words: *95 % confident that this model does what Tay
said — it attempts to move smartly, which means not moving when the costs
outweigh the risks.*

---

## State of play

**Three things are now settled, and they change the shape of the work.**

1. **Tay's published results were produced by a uniform random selector.**
   `epsilon` defaults to 1.0 in `execute_ai_model` and is never overridden by the
   evaluation harness, so `choose_action` returns `random.randrange(action_size)`
   on every decision and `predict` is never called. Every figure in the paper —
   gamma, epsilon, train start, detection rate, ablation — characterises that
   random selector. Forensics record §2; verified at five commits.

   **Consequence:** there is no reuse-versus-retrain trade-off left. The reused
   weights cannot be a control, because the behaviour they would be controlling
   *for* was never theirs. The project's existing **random-scheme defender over
   the same four mechanisms is the faithful replication of Tay's reported
   results**, and it is a cheaper and stronger control than the one the previous
   brief proposed.

2. **The checkpoints are unusable on three independent grounds.** They expect an
   `8/3 → 5` signature the live state head cannot produce (the 8/3 head is
   commented out at `mtd_ai_operation.py:249-301`); batch-size-1 `fit` has
   collapsed every BatchNorm `moving_variance` to exactly 0, so they saturate at
   inference; and 34 of 55 have a greedy-policy entropy below 0.5 bits. One
   (`parameter_set_10`) never received a gradient step at all. Forensics §1, §3.

3. **The reward has no cost term, and that is the root cause.**
   `calculate_reward` weights every security-posture feature at ±75 and weights
   `mtd_freq` and `time_since_last_mtd` at **0**. Every non-zero term is improved
   by deploying, so **the optimal policy under this reward is "always deploy"**.
   Compounding it: `calculate_reward` is only reached from `_mtd_execute_action`,
   so a no-op stores no transition and action 0's Q-value is never a TD target.
   Forensics §5.

**And one structural defect makes the no-op unreachable as a behaviour.** The
`yield self.env.timeout(...)` in `_mtd_trigger_action` sits *inside* the
`if action > 0:` block, so `action == 0` re-enters the loop with `env.now`
unchanged. Under random selection that is rejection sampling; under a greedy
policy it is an infinite loop. Forensics §6.

**What is already available and does not need building.** Per-mechanism execution
durations exist as `MTD_DURATION` in `mtdnetwork/data/constants.py` — 110 / 100 /
100 / 80 / 70 / 70 / 20 s — sourced from Zhang 2023 Table 3 and badged
**faithful** in [`../implementation/provenance.md`](../implementation/provenance.md).
Every executed mutation already writes `(start_time, finish_time, duration)` into
`mtd_stats`. Resource seizure (`application` / `network` / `reserve`) already
models one mechanism blocking another. The cost side is mostly a derivation, not
a mechanism.

**Marc's rulings carried in, 2026-08-07.** Number of Vulnerabilities / Number of
Exposed Vulnerabilities (T-FX-02) are **low priority — drop them**. Downtime and
operational impact **must** be implemented, swept across the existing mechanisms,
and **lives as a network metric only** — it is not a new defence mechanism and
changes no mutation's behaviour. The seven prerequisites below stand as listed.

---

## Recommended approach

Five stages. **Stages 0–3 are all CPU-scale and local.** Stage 4 is the Kaya
decision and is not this handoff's to take.

### Stage 0 — repairs and the determinism gate

The forensics record's dispositions, in dependency order. Each is a **separate
commit** with its own justification, because each changes what a later result
means. None should be bundled into "getting the arm running".

| # | Repair | Why it blocks everything after |
|---|---|---|
| MTDAI-02 | Restore the `8/3` state head (or declare a replacement set) | Nothing runs until the signature is decided. Note this is a disposition, not housekeeping: the two heads see *different metrics*, not different widths |
| MTDAI-03 | Move the `yield` out of the `action > 0` block; give the no-op its own timeout | Without it a greedy agent livelocks and the no-op cannot manifest as elapsed time |
| MTDAI-04 | Store a transition for `action == 0` | Without it action 0's Q-value is never trained, so no amount of reward design can reach it |
| MTDAI-07 | Batched updates (or LayerNorm) in place of batch-size-1 `fit` | Without it every checkpoint is numerically broken regardless of what it learned |
| MTDAI-08 | Remove the duplicate `register_mtd` | Two MTDs enqueued per decision corrupts every mutation-rate figure |
| MTDAI-12 | `calculate_reward`: stationary normalisation; `item[1]` not `item[5]` | Fold into the Stage 2 rework, not separately |
| — | **Vectorise `replay`** — batched `predict` / `train_on_batch` instead of the per-sample Python loop | Measured 26.5 s per `replay()` call at batch 64. A ~50–100× speedup, and Stage 3 is unaffordable without it |

**Then the determinism gate, before anything is built on the arm** (carried
verbatim from the previous brief's §4, still unrun):

- Is `main_network.predict(...)` bit-reproducible across runs for fixed weights
  and fixed inputs under TF 2.21 / Keras 3.14? Thread scheduling and
  non-deterministic kernels are the usual culprits.
- Do `np.random.rand()` in `choose_action` and `random.randint` in the
  static-degrade fallback draw from streams the existing seeding controls, and
  do they perturb the attacker's stream? **D-29 already records that mechanisms
  and attacker share one stream**, so adding draws here shifts the attacker's
  stream and every seed-matched comparison with it.
- If determinism cannot be established, **stop and report**. Every `mtd_ai`
  figure then becomes distributional over repeated runs rather than a seeded
  point, which changes the seed budget for every study downstream.

### Stage 1 — the downtime / operational-impact metric

Tay §4.1.2 ¶4 names it (T-TS-02) and nothing implements it. Build it as a
**derived network metric only** — no new mechanism, no change to any mutation's
behaviour, per Marc's ruling.

The recommended definition, offered as a starting point rather than a conclusion:
**cumulative availability loss over a trailing window**, derived from the
`mtd_stats` records that already exist —

```
downtime_ratio(w) = Σ over MTD records overlapping [now − w, now] of
                    (overlap duration) / w
```

with `w` the same window the other time-series features use. It composes
naturally with resource seizure (a suspended mechanism costs nothing until it
runs) and it is bounded in `[0, n_resources]`, which matters for the state
vector's conditioning.

Two alternatives worth naming before settling: a **per-mechanism weighted count**
(cheaper, but throws away the concurrency structure the `simpy.Resource` seizure
already models), and a **per-host downtime** measure (closer to Tay's wording
"downtime necessary for replacing each node", but requires per-host attribution
that `mtd_stats` does not currently carry). Recommend the window ratio, and
record why.

**Sweep it across the existing mechanisms.** `MTD_DURATION` supplies the relative
costs already; the sweep Marc asked for is over the *charge*, not over the
durations — the durations are provenance-badged faithful and must not be
retuned. Any sensitivity study over the durations themselves is a separate,
later question.

**Where it lives.** A derived statistic alongside the existing evaluation
metrics, exposed as (i) a network metric readable independently of the agent, and
(ii) a time-series state feature. (i) is what makes it reportable in its own
right — a defence-effort axis the project does not currently measure at all,
which is worth having whether or not the agent ever learns to use it.

### Stage 2 — the cost term in the reward

Add a single charge against the Stage 1 metric and expose its weight as a
declared, swept parameter:

```
reward = Σ security-posture deltas (as now)  −  λ · Δ downtime
```

`λ = 0` must reproduce today's behaviour exactly — that is the null-equivalence
check, and it should be a test.

**Declare the reward.** Tay's paper has none (forensics §5), so this project
supplies its own and must defend it. That means the weights, the normalisation,
the window and `λ`'s sweep range all go into the record with their reasoning
before any training run, not after. There is no literature yardstick to audit
against here; the justification *is* the deliverable, on the same standing as the
per-tactic durations under S3.

### Stage 3 — the calibration run, which is the kill criterion

**This is the one output that decides whether Kaya is worth it.** Train a small
ladder of agents at CPU scale — 100 nodes, short horizons, few seeds — varying
**only** `λ`, and report the **no-op share of decisions** against it.

The claim being tested is exactly Marc's bar: *an agent that moves smartly moves
less when moving costs more.* So:

- **Pass:** the no-op share rises monotonically (or at least materially and
  consistently) with `λ`, and the realised mutation rate falls, against the
  `static_degrade_factor` and ε-greedy floors rather than against zero.
- **Fail:** the no-op share is flat, or noise-dominated, across the whole `λ`
  range. Then the agent is not trading anything off, the architecture or the
  training regime is still broken, **and no amount of Kaya time fixes it.**

Report the **mutation mix** too, not just the rate. Mechanisms are not
interchangeable against the movement arm — a network-class firing delivers
0.92–1.00 of its disruption, an application-class one 0.67–0.83
([`../implementation/disruption_wiring.md`](../implementation/disruption_wiring.md))
— so a `λ` that shifts the *mix* toward cheap mechanisms is a real result even if
the rate never moves. It is also the cheaper prediction, and worth pre-registering
as a secondary outcome so it cannot be found after the fact.

### Stage 4 — the Kaya proposal (scope: write it, do not run it)

Only if Stage 3 passes. What it must specify:

- **Parallel episodes, not GPU throughput.** The bottleneck is a single-threaded
  SimPy loop and a 46 661-parameter network. The win is many concurrent
  environment workers feeding one learner; a GPU buys almost nothing here.
- **Larger networks (300–1000 nodes) and longer horizons**, which is Tay's own
  stated limitation (T-FW-02, §7.2) and the honest justification for retraining
  rather than reusing.
- **An ε schedule sized to the episode budget.** Tay's 0.980–0.998 are per-*step*
  rates in the cited literature applied per *episode* over 100 episodes; `ε` never
  reaches `epsilon_min`. Decide per-step or per-episode explicitly and record it.
- **`train_start` against buffer capacity.** `train_start = 2000` against
  `deque(maxlen=2000)` means training starts only when the buffer saturates —
  around episode 80 of 100. Size them independently.
- A seeded, documented training procedure, since retraining adds a procedure that
  must itself be defensible.

---

## Validation gate

The work is done when **all** of these hold:

1. **Repairs land as separate commits**, each naming its disposition, with the
   existing suite green at no fewer tests than today.
2. **`λ = 0` is null-equivalent** to pre-Stage-2 behaviour, guarded by a test.
3. **The determinism gate has a verdict** — bit-reproducible, or explicitly
   declared distributional with the seed-budget consequence stated.
4. **A greedy (ε = 0) run completes without livelocking** on an agent whose
   policy selects action 0 for some states. This is the direct proof MTDAI-03 is
   repaired; today it hangs.
5. **The `λ` ladder is reported** — no-op share, realised mutation rate against
   both floors, and mutation mix, per `λ`, with seeds.
6. **A go/no-go is stated**, with the pass/fail criterion from Stage 3 applied to
   the numbers rather than to an impression.

A Stage 3 **fail** is a complete and reportable outcome. It kills a large,
expensive branch of the programme cheaply, which is the point of running it
first.

---

## Hard constraints

- **Never repair a defect silently.** Every item in Stage 0 is a disposition;
  each changes what a downstream result means. Separate commits, each justified.
- **The MTD durations are not tuneable.** `MTD_DURATION` is provenance-badged
  faithful against Zhang 2023 Table 3. The sweep is over the *charge* `λ`, never
  over the durations.
- **Downtime is a metric, not a mechanism** (Marc, 2026-08-07). It changes no
  mutation's behaviour and adds nothing to the defence pool.
- **Do not reuse any published Tay figure as a comparator.** Forensics §2 —
  they characterise a random selector. The project's own random-scheme arm is
  the comparator.
- **The `mtd_ai` arm is bounded to the reactive case.** Time-triggered MTD is
  unaffected by attacker tempo, so nothing learned here generalises to the rest
  of the defence pool, and the write-up must say so.
- **No attacker state may be wired into `attacker_sensitivity`** — that is
  reverse-modelling detection and stays forbidden regardless of anything here.
- Determinism (SIM-05, but see Stage 0); envelope-not-actor; within-substrate
  comparability only; Australian English; branch per session; **never push**.

---

## Reading list

- [`../implementation/pipeline/ogasp/mtd_ai_forensics.md`](../implementation/pipeline/ogasp/mtd_ai_forensics.md)
  — **read this first and in full.** §5 (the reward and its missing cost term) and
  §6 (the unreachable no-op) are what this handoff exists to fix; §9 is the
  disposition list Stage 0 works through.
- `mtdnetwork/mtdai/mtd_ai.py` — `create_network`, `choose_action`, `replay`,
  `calculate_reward`. The whole agent is 205 lines.
- `mtdnetwork/operation/mtd_ai_operation.py` — `_mtd_trigger_action` (the yield
  placement, §6) and both `get_state_and_time_series` methods, live and
  commented-out (§1).
- `mtdnetwork/data/constants.py` `MTD_DURATION` + [`../implementation/provenance.md`](../implementation/provenance.md)
  — the per-mechanism costs Stage 1 derives from, and their badge.
- [`../implementation/disruption_wiring.md`](../implementation/disruption_wiring.md)
  §(d) — the per-class disruption figures that make the mutation *mix* worth
  reporting in Stage 3.
- [`../implementation/pipeline/ogasp/stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
  §17 — the cheap falsifying run this handoff's Stage 3 generalises. Note its
  §8 premise (that `mtd_ai` keys on attacker activity) needs re-reading against
  forensics §2.
- `tools/mtd_ai_weights_probe.py` — the read-only probe, if any checkpoint
  question comes up again.

---

## Out of scope (explicitly)

- **Any attacker mechanism** — that is
  [`2026-08-06_knowledge_gated_apt_attacker.md`](2026-08-06_knowledge_gated_apt_attacker.md).
- **Running the Kaya training.** Stage 4 writes the proposal; Marc decides
  whether it runs.
- **Number of Vulnerabilities / Number of Exposed Vulnerabilities** (T-FX-02) —
  ruled low priority, 2026-08-07.
- **Retuning `MTD_DURATION`**, or any sensitivity study over the durations
  themselves.
- Repairing D-18, D-29, or anything else in the audit's list that is not named in
  Stage 0.
- Any claim about non-reactive defenders.
- Dissertation prose.

---

## Return format

Default (see [`../workflows/session_workflow.md`](../workflows/session_workflow.md#handoff-workflow)),
**with one addition this handoff requires**: state the Stage 3 go/no-go
explicitly, with the `λ` ladder's numbers, because that verdict is what Marc is
committing Kaya time against.
