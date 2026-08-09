---
status: open
created: 2026-08-08
---

# The scaled `mtd_ai` training proposal — what a Kaya run would have to specify, costed against a measured CPU baseline

**Scope: this brief is the proposal. It does not run it.** Whether it runs is
Marc's call, and it is a real decision with a real cost, so everything below is
arithmetic against measurements rather than an estimate.

**The calibration passed, so this brief is live.**
[`../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md`](../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md)
§3 returns **GO**: the greedy no-op share rises by +0.732 between the bottom and
top halves of the λ ladder, with the same sign in all three seeds, against a
pre-registered bar of 0.15 — and the instrument's own kill criterion held, with
the λ = 0 agent declining to deploy on 2.1 % of decisions against a bar of 10 %.

**Read that record's verdict section before this brief, not after it**, because
the go is narrow and two of its limits are prerequisites here rather than
caveats. The measured response is a **step, not a gradient**: seventeen of
eighteen agents are near-constant policies and λ selects which constant, which
is the same degeneracy the forensics pass found in Tay's checkpoints,
reappearing under a repaired reward. And the **static-degrade guard supplied 29
of the 31 mutations** that fired at the top of the ladder, so it — not the
policy — is doing the defending in exactly the region the study reports as
success. Items 6 and 7 below exist because of those two findings.

---

## State of play

The rebuild landed. `mtd_ai` is now an agent that *can* decline to move: the
no-op costs simulated time, it stores a transition so its Q-value is a TD
target, moving is charged against a downtime metric, and the replay update is
batched so BatchNorm sees a real variance. The full account is the calibration
record's §1; the defect list it works through is
[`../implementation/pipeline/ogasp/mtd_ai_forensics.md`](../implementation/pipeline/ogasp/mtd_ai_forensics.md)
§9.

**What is deliberately still small.** The calibration ran at Tay's own training
geometry — 100 nodes, 5 000 s horizons, 120 episodes, three seeds — because its
job was to answer a yes/no question as cheaply as possible, not to produce an
agent anyone would report. Nothing in it licenses a claim about a *trained*
defender.

**The measured cost baseline, which is what makes this brief costable.** On the
development box, uncontended and single-threaded, one agent — 120 training
episodes of 5 000 s at 100 nodes with a 200 s decision interval, plus five
greedy evaluation episodes — costs **692 s**, so **≈ 5.8 s per training
episode** end to end. The replay updates dominate: ~25 decisions per episode,
one batched Double-DQN update each.

For contrast, the inherited per-sample replay loop cost 26.5 s per `replay()`
call at batch 64, so a *single* episode's updates would have taken **~11
minutes** and one agent about **22 hours**. The vectorisation is the reason a
scaled proposal is worth writing at all, and it is also why the calibration
itself was affordable: the whole 18-agent ladder ran in well under an hour on
six cores.

Two measurement caveats, so the number is not quoted more precisely than it
deserves. The 692 s figure is the one clean serial cell; the host suspended
during the first attempt at the serial run, which makes every later wall-clock
figure from that attempt meaningless (the discrete-event results are unaffected
— simulated time does not depend on wall time). And the parallel cells that
produced the ladder were contended six ways on eight cores, so their per-cell
times are upper bounds, not measurements.

---

## What the proposal must specify

### 1. Parallel episodes, not GPU throughput

**The bottleneck is a single-threaded SimPy loop, not matrix multiplication.**
The Q-network is 46 661 parameters and the batch size is 32; a GPU buys almost
nothing against that, and the measured profile confirms it — the cost is spread
across many small forward passes and one small update per decision, interleaved
with discrete-event simulation that a GPU cannot touch.

The win is **many concurrent environment workers feeding one learner**. Each
worker runs its own `simpy.Environment` and its own network instance, pushes
transitions into a shared buffer, and periodically pulls fresh weights. Two
things this project already knows constrain the design:

- **Every worker must own its RNG stream.** D-29 records that the mechanisms and
  the attacker share one Python `random` stream, and the determinism gate
  measured that a single extra defender-side draw shifts everything downstream
  by one position. Workers sharing a process-global stream would be
  irreproducible; each needs its own seeded generator, and the seed must be a
  function of (worker id, episode index) so the run is replayable.
- **Reproducibility must be a stated property of the design, not a hope.** The
  gate established that a forward pass and a whole seeded episode are
  bit-reproducible in the single-threaded case. Asynchronous workers give that
  up unless the learner consumes transitions in a deterministic order. Decide
  explicitly whether the scaled run is bit-reproducible or distributional, and
  say which — the answer changes what any figure from it may be compared against.

### 2. Larger networks and longer horizons

Tay's own stated limitation (T-FW-02, §7.2) and the honest justification for
retraining rather than reusing: 100 nodes over 5 000 s is a small network
observed briefly. **300–1 000 nodes** and horizons long enough for the
compromise process to develop are the target.

Two costs to measure before committing, both of which are substrate properties
rather than agent properties:

- **The state head is not free at scale.** `attack_path_exposure` walks the
  shortest path from the exposed endpoints to the target node and enumerates
  every service's vulnerabilities on it, and it is computed **twice per
  decision** (once for the state, once for the next state). Its cost grows with
  the network; at 1 000 nodes it may well exceed the learning update. Measure it
  before assuming the episode cost scales linearly in nodes.
- **Longer horizons change the reachable regime.** The rate feasibility study
  records that the substrate objective only becomes reachable above roughly
  1 600 s of mutation interval, and that at the 200 s operating interval every
  success-rate-shaped measurement is pinned at zero. A longer horizon does not
  by itself escape that region; the interval does. If the scaled run is meant to
  produce success-rate-shaped evidence, the interval has to move too, and the
  comparability argument moves with it.

### 3. An ε schedule sized to the episode budget

Tay's 0.980–0.998 constants are per-*step* rates in the DQN literature he cites
(Mnih et al.; van Hasselt et al.), applied per *episode* over 100 episodes. The
consequence is arithmetic: ε travels from 1.0 to 0.13 at best and to 0.74 at the
gentle end, `epsilon_min = 0.01` is never approached, and the agent never
transitions to exploitation during training at all.

The rebuild decays **per decision** and the calibration used ×0.999 to carry ε
from 1.0 to 0.05 over ~3 000 decisions. A scaled run must recompute this against
its own budget rather than inheriting the constant: state the total decision
count, state the ε you intend at the end of training, and derive the rate.
Whichever is chosen, **record which quantity it is per** — that ambiguity is
what produced the original defect.

### 4. `train_start` against buffer capacity

`train_start = 2000` against `deque(maxlen=2000)` means training begins only
once the buffer is **full** — around episode 80 of 100, so Tay's ablation models
learned across roughly 20 episodes and ~500 transitions. Size the two
independently: the buffer for how much history is worth resampling, the
threshold for how much data is enough to start. The calibration used 200 against
2 000, which starts training in the ninth episode.

### 5. A seeded, documented training procedure

Retraining adds a procedure that must itself be defensible, so the procedure is
part of the deliverable and not an implementation detail. At minimum: the seed
set and how seeds map to workers; the geometry and horizon; every declared
parameter with its justification (the calibration record's §0 table is the
template); the target-sync interval; and the checkpointing policy, including
what is saved and at what cadence, because "the checkpoint on the bar had no
causal influence on the bar" is the failure this whole line of work exists to
avoid repeating.

---

## Validation gate

The proposal is complete when a reader could execute it without asking a
question, and specifically when:

1. **The parallelism design names its reproducibility status** — bit-reproducible
   with a deterministic consumption order, or explicitly distributional with the
   seed budget that implies.
2. **Per-worker RNG ownership is specified**, with the seed derivation written
   down.
3. **The per-episode cost at the target geometry is measured, not extrapolated**,
   with `attack_path_exposure` timed separately.
4. **The ε schedule is derived from the episode budget**, with the per-step /
   per-episode question answered in writing.
5. **`train_start` and buffer capacity are sized independently**, each with a
   reason.
6. **Greedy-policy entropy is a first-class reported outcome** (MTDAI-16). A
   larger network trained the same way will most likely produce a larger
   constant-action policy, and a run that does not measure this cannot tell that
   outcome from success.
7. **The static-degrade factor is swept, or its contribution is separated out**
   (MTDAI-17). It currently sets the upper attractor and supplies almost every
   mutation in the low-movement regime, so any figure that does not separate it
   attributes the guard's behaviour to the agent.
8. **MTDAI-14 and MTDAI-15 are repaired first.** A suspended deployment stores no
   transition, so the deploy action is trained only on the occasions it worked;
   and `done` is hardcoded `False`, so the agent bootstraps across episode
   boundaries. Both bias a long training run more than a short one.
9. **A total wall-clock budget is stated** as workers × episodes × measured
   episode cost, so the ask is a number rather than an intention.

---

## Hard constraints

- **The MTD durations are not tuneable.** `MTD_DURATION` is provenance-badged
  faithful against Zhang 2023 Table 3. Anything swept is swept over the charge,
  never over the durations.
- **Do not reuse any published Tay figure as a comparator.** They characterise a
  uniform random selector (forensics §2). The project's own random-scheme arm
  over the same four mechanisms is the faithful replication of those results and
  is the comparator.
- **The `mtd_ai` arm is bounded to the reactive case.** Time-triggered MTD is
  unaffected by attacker tempo, so nothing learned here generalises to the rest
  of the defence pool, and any write-up must say so.
- **No attacker state may be wired into `attacker_sensitivity`** — that is
  reverse-modelling detection and stays forbidden.
- Envelope-not-actor; within-substrate comparability only; Australian English;
  branch per session; **never push**.

---

## Reading list

- [`../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md`](../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md)
  — **read §3 first**, then §0 for the pre-registration and §2 for the
  determinism verdict this brief's parallelism section is constrained by.
- [`../implementation/pipeline/ogasp/mtd_ai_forensics.md`](../implementation/pipeline/ogasp/mtd_ai_forensics.md)
  §4 — the training regime as Tay actually configured it, which is where items 3
  and 4 above come from.
- `tools/mtd_ai_run.py` and `tools/mtd_ai_lambda_ladder.py` — the single-threaded
  driver a parallel one would replace, and the study that sized its cost.
- [`rate_feasibility_study.md`](../implementation/pipeline/ogasp/rate_feasibility_study.md)
  §7 — the degenerate region, which bounds what a longer horizon can evidence.

---

## Out of scope

- **Running the training.** This brief is the proposal.
- Any attacker mechanism.
- Retuning `MTD_DURATION`, or any sensitivity study over the durations.
- Any claim about non-reactive defenders.
- Dissertation prose.
