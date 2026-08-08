---
status: investigation record
created: 2026-08-08
updated: 2026-08-08
topic: "Rebuilding Tay's mtd_ai defender so that not-moving is an action it can take and moving has a price, and the λ ladder that decides whether the rebuilt agent trades one against the other"
---

# The `mtd_ai` cost calibration — can the agent be made to trade downtime against risk, and does it

**Status:** investigation record. Companion to
[`mtd_ai_forensics.md`](mtd_ai_forensics.md), which established what the
inherited agent actually is; this record is what was built on top of that
finding and what the building returned.

**The deliverable is a go/no-go, not a trained model.** The question is whether
any amount of large-scale training time is worth committing, and it is answered
at CPU scale before any of that time is spent. Marc's bar, in his words: *95 %
confident that this model does what Tay said — it attempts to move smartly,
which means not moving when the costs outweigh the risks.*

---

## §0 Pre-registration

**Committed before the ladder was run.** The commit that introduces this section
contains no results; the results land in a later commit. That ordering is the
audit trail, and it is the same discipline every swept study in this project has
used.

### What is being tested

One sentence: *an agent that moves smartly moves less when moving costs more.*
The ladder varies **only** the reward's cost weight λ — seed, geometry, horizon,
architecture, exploration schedule and every other parameter held fixed — and
reads the agent's willingness to do nothing against it.

### The measurement

Per λ and per seed, one agent is trained from scratch and then evaluated under a
**strictly greedy policy** (ε = 0) on fresh networks. The headline statistic is
the **no-op share of greedy decisions**. Training-time shares are recorded but
are not the verdict: at any ε above zero the no-op share is floored at ε/5
whatever the policy has learned, so a ladder read off the training share would
report the exploration schedule rather than the policy. This is the same
mechanism by which every figure in Tay's paper reports a uniform random
selector, and it is not going to be repeated.

Two floors bound the greedy share, and both are reported beside it rather than
subtracted out:

- the **static-degrade guard** forces a deployment whenever the network has gone
  2 000 s without one, so at a 200 s decision interval a policy that never
  chooses to deploy still deploys once in ten decisions — a ceiling of ≈ 0.9 on
  the no-op share, not 1.0;
- the **uniform random selector** — the thing Tay's published figures actually
  characterise — sits at 0.2, one no-op among five actions.

### The conclusions, fixed in advance

**C1 — primary; this is the go/no-go.** The greedy no-op share rises with λ.
Held if the share is monotone non-decreasing across the ladder, or (weaker, and
the operative test) if the mean over the top half of the ladder exceeds the mean
over the bottom half by **at least 0.15 absolute** with the same sign in **all
three seeds**. Failed if the top-to-bottom difference is under 0.05, or if the
sign is inconsistent across seeds. A failure means the agent is trading nothing
off, and no amount of additional training time fixes that.

**C2 — the rate follows the share.** The realised mutation rate falls as λ
rises, read against the static-degrade floor rather than against zero. C2 is
expected to follow from C1 mechanically; reported separately because a share
that rises while the rate does not would mean the guard is doing the deploying,
which is a different finding.

**C3 — secondary, and the cheaper prediction.** The mutation *mix* shifts toward
the cheap mechanisms as λ rises: the mean execution duration of the mutations
fired falls, and the share drawn from ServiceDiversity (70 s) and OSDiversity
(80 s) rises against CompleteTopologyShuffle (110 s) and IPShuffle (100 s).
Mechanisms are not interchangeable — a network-class firing delivers 0.92–1.00
of its disruption to the movement attacker against an application-class firing's
0.67–0.83 ([`../../disruption_wiring.md`](../../disruption_wiring.md)) — so a λ
that shifts the mix is a real result **even if the rate never moves**. Recorded
now precisely so that it cannot be found afterwards and presented as the thing
that was being looked for.

**C4 — the instrument's own kill criterion.** At λ = 0 the greedy no-op share
must sit near the floor. The λ = 0 reward has no cost term at all and every
non-zero weight in it is improved by deploying, so its optimal policy is to
deploy on every decision; an agent that is already declining to deploy at λ = 0
is not being driven by the reward, and no verdict may be read off a ladder whose
zero point does not behave. Held if the λ = 0 greedy no-op share is **below
0.10**.

**C5 — a negative control, explicitly not a pass condition.** Compromise breadth
is reported per λ. This study measures whether the agent trades cost against
risk, **not** whether the trade is good for security. A ladder that raises the
no-op share and also raises compromise passes C1 and produces a finding for the
discussion; reading it as a failure would be scoring the agent against a claim
nobody made.

### What a pass and a fail each license

- **Pass on C1** (with C4 held): the architecture and the training regime are
  capable of expressing a cost/risk trade-off, and a scaled-up training
  proposal is worth writing. It licenses nothing about whether the trade-off is
  *good*, and nothing about non-reactive defenders.
- **Fail on C1**: a complete and reportable outcome. It kills a large and
  expensive branch of the programme cheaply, which is the point of running it
  first.
- **Fail on C4**: no verdict either way; the ladder is uninterpretable and the
  reward or the training regime is still broken.

### The declared parameters

There is no literature yardstick for any of these — Tay's paper contains no
reward function at all (forensics §5) — so the justification is the deliverable
and it is recorded here before the run rather than after.

| Parameter | Value | Why this value |
|---|---|---|
| λ ladder | 0, 25, 50, 100, 200, 400 | From a pilot at λ = 0: mean \|reward\| per transition ≈ 46, and the mean Δdowntime separating a no-op (−0.35) from a deployment (+0.15) is ≈ 0.5. So λ·0.5 spans ≈ 12 (clearly sub-dominant to the security terms) to ≈ 200 (clearly dominant). A ladder that failed to bracket the security reward's own magnitude could not distinguish "the agent ignores cost" from "the cost was never large enough to notice" |
| downtime window | 200 s | The mutation trigger interval. The reading then answers "how much of the last decision cycle was the network down for", and a single 70–110 s mutation reads as a fraction rather than saturating |
| reward feature scales | fixed divisors, one per feature | Replaces the inherited min-max against a *growing* replay buffer, which priced early and late transitions by different rulers while both sat in the same buffer. Each divisor is the feature's full-scale range under the substrate's own constants — risk ≤ 10 (complexity × impact), roa ≤ 1 (risk / minimum exploit time), overall_mttc_avg ≤ 25 s (the largest attack-action duration), the rest already ratios |
| security-posture weights | ±75, unchanged | Inherited from Tay's implementation. Kept rather than re-derived so that the only deliberate change to the reward is the cost term |
| seeds | 11, 22, 33 | Three. D-29 records that the mechanisms and the attacker share one RNG stream, and the determinism gate below confirms that arms differing in how many draws the defender takes are **independent, not paired** — so seeds are replicates, not matched pairs |
| episodes | 120 per agent | ~25 decisions per 5 000 s episode → ~3 000 transitions, against a 2 000-transition buffer that starts training at 200. Sized so that training begins early rather than at the point of buffer saturation, which is the defect that left Tay's ablation models learning across ~20 episodes |
| ε schedule | 1.0 → 0.05, ×0.999 **per decision** | Per-step, which is what the 0.980–0.998 constants mean in the literature Tay cites. Applied per episode over 100 episodes, as his harness did, ε never approaches ε_min and the agent never exploits during training either |
| geometry / horizon | 100 nodes, 5 000 s, 200 s interval | Tay's own training configuration, so the CPU-scale result is comparable to the regime the inherited work was produced in |

### What is deliberately not swept

The **per-mechanism execution durations**. `MTD_DURATION` is provenance-badged
faithful against Zhang 2023 Table 3; the sweep is over the *charge*, never over
the durations. Any sensitivity study over the durations themselves is a separate
question.

---

## §1 What was built

Seven repairs and two additions, each landed as its own commit with its own
justification, because each changes what a downstream result means.

### The repairs (Stage 0)

| # | What was wrong | What was done |
|---|---|---|
| MTDAI-02 | The live 5/6 state head cannot feed any of Tay's checkpoints; the 8/3 head they were trained against is commented out | **Declared** the live head canonical rather than restoring 8/3. Restoring it only ever bought checkpoint compatibility, and the checkpoints are unusable on three independent grounds; of the three inputs 8/3 carries and 5/6 does not, two are present in 5/6 as time-series features and differ only in placement, and the third (`exposed_endpoints`) is the analogue of the T-FX-02 feature Marc dropped on 2026-08-07 |
| MTDAI-03 | The trigger `yield` sat inside `if action > 0:`, so a no-op re-entered the loop at an unchanged `env.now` — rejection sampling under ε = 1.0, an infinite loop under a greedy policy | The no-op draws the same trigger interval as a deployment. Two dead selections on the training path went with it: one whose result was overwritten, one an unbounded redraw loop against a hardcoded 2 000 |
| MTDAI-04 | `calculate_reward` was reachable only from `_mtd_execute_action`, so the buffer held deploying actions exclusively and action 0's Q-value was never a TD target | The no-op stores its own transition, with its next state read after its interval elapses — the same measurement point a deployment's transition uses |
| MTDAI-07 | Batch-size-1 `fit` collapsed every BatchNorm `moving_variance` to exactly 0, and cost 26.5 s per `replay()` call at batch 64 | One vectorised Double-DQN update over the minibatch. Measured: ~4.5 s per 25-decision episode end to end, against a per-sample loop that would have spent ~11 minutes on the replay calls of a single episode |
| MTDAI-08 | The scorer registration took `register_mtd(...)` as its *argument*, enqueuing two MTDs per decision and naming every scorer entry `"None"` | Register once; name the entry after the strategy enqueued |
| MTDAI-12 | Min-max normalisation against a growing buffer (non-stationary reward scale); `item[5]` read where `item[1]` was meant | Fixed per-feature divisors replace the buffer-derived normaliser outright. The index defect dissolves with the normaliser that had it |
| **MTDAI-13** | **New.** The training head divided `overall_mttc_avg` by 10 and the otherwise-identical evaluation head did not, so the agent was trained on a feature scaled ten times smaller than the one it is evaluated on | Removed. Nothing in the paper licenses either scaling; what it cannot be is two different ones |

Two supporting changes are not repairs and are recorded as such. The **state
vocabularies moved into `mtd_ai.py`** as ordered lists that both operation
classes build their vectors from and the reward indexes back — the inherited
code built the vector from a dict literal in one file and indexed it by the
caller's selection list in another, which agreed only because the selection was
always the whole vocabulary. And a **per-decision ledger** records every
decision's action and its provenance (`greedy` / `random` / `forced`), because
the execution records cannot supply it: they hold only mutations that ran, so a
forced decision, an explored one and a chosen one are indistinguishable after
the fact.

### The driver

Nothing in the tree could run `mtd_ai` at all — Tay's `experiments/run.py` and
`experiments/train_models.py` were deleted in `e5935ab` / `6f235ba`.
[`../../../../tools/mtd_ai_run.py`](../../../../tools/mtd_ai_run.py) is a fresh
driver, not a restoration, and it differs from his in four declared ways:
evaluation is **greedy by default** (his harness never overrode
`execute_ai_model`'s `epsilon=1.0`, which is why no published figure consulted
the network); everything is **seeded**; `custom_strategies` is passed
**explicitly** rather than relying on `MTDScheme` substituting its own list; and
the exploration schedule is **per-step and declared** rather than per-episode by
accident of where the multiply sat.

### The downtime metric (Stage 1)

Tay's §4.1.2 ¶4 names *Downtime / Operational Impact for Node Replacement*
(T-TS-02) as a time-series input and nothing in the inherited code implements it
in any form. It is the availability half of the when-to-move question and the
only quantity that could make the no-op rational. The paper supplies no
definition, so this one is the project's:

```
downtime_ratio(w) = Σ over mutations overlapping [now − w, now]
                    of (overlap duration) / w
```

computed over the `(start_time, finish_time, duration)` records the substrate
already writes, **plus any mutation still in flight**, charged up to `now`.
Three properties earn it over the alternatives, and all three are pinned by
test:

- **Overlap accounting, not event counting.** A mutation half inside the window
  is charged half.
- **Concurrency survives.** Two mutations running at once on different resource
  layers are charged twice, which is the structure the `simpy.Resource` seizure
  already models and which a per-mechanism weighted count would discard.
- **Bounded by the number of layers, not by the horizon.** Which keeps it
  conditioned alongside a state vector whose other entries are ratios.

The in-flight term is not a detail: execution records are written only at
*finish*, and mutation durations (70–110 s) are a large fraction of the 200 s
window, so without it the metric would read zero precisely while the network is
down — the state the agent most needs to see.

Per Marc's ruling of 2026-08-07 it **lives as a network metric only**. It
changes no mutation's behaviour, adds nothing to the defence pool, and is
readable under any scheme through `Evaluation.downtime_ratio` — a defence-effort
axis the project does not otherwise measure at all, worth having whether or not
any agent learns to use it. A **per-host** measure would be closer to Tay's
wording ("downtime necessary for replacing each node") but the execution records
carry no per-host attribution, and inventing one would be a substrate change
rather than a derived metric.

### The cost term (Stage 2)

```
reward = Σ security-posture deltas (unchanged)  −  λ · Δ downtime_ratio
```

The charge is on the *change* in downtime rather than its level, which keeps it
dimensionally the same kind of quantity as every other term in the sum:
recovering availability is worth precisely what losing it cost, rather than the
agent paying a standing tax for having ever moved. At λ = 0 the term contributes
exactly zero, so the ablation against the reward without it is exact rather than
approximate; that is a test, not an assertion.

---

## §2 The determinism gate

Run before anything was built on the arm, per the handoff's Stage 0, across
fresh processes under TF 2.21 / Keras 3.14.

**Q1 — is a forward pass bit-reproducible for fixed weights and fixed inputs?**
**Yes.** Three fresh processes produced byte-identical initial weights from the
seed (SHA-256 `e71d55eb…`) and byte-identical outputs over a fixed 64-row input
batch (`9f32c41b…`). Thread scheduling and non-deterministic kernels, the usual
culprits, do not bite here.

**Q2 — is a whole seeded episode reproducible?** **Yes.** Three fresh processes
at one seed, with the policy pinned so the result cannot turn on an untrained
argmax tie, agreed on decision count (20), decision timestamps (identical to the
float), mutations executed (20) and hosts compromised (7).

**Q3 — do the draws the agent adds perturb the attacker's stream?** **Yes, and
this is the consequential answer.** A single extra draw from the shared Python
`random` stream shifts every subsequent value by one position — measured
directly: without the extra draw the next three values are 0.403978, 0.200075,
0.178802; with it, 0.200075, 0.178802, 0.248431. D-29 already recorded that the
mechanisms and the attacker share one stream; what this adds is that the no-op
repair *changes how many draws the defender takes*, since a deploying decision
draws an execution time and a mutation's own randomness where a no-op does not.

Two streams are shared, not one, and the repair touches both. The Python
`random` stream carries the forced-deploy draw, the exploration draw's action
choice and the detection-sensitivity draw on the defender side, and the
attacker's host-ordering tie-break on the other. The **numpy/scipy** stream
carries every `exponential_variates` call — which is what the no-op repair adds
per decision, and which the attacker also draws its action durations and its
confusion penalty from. D-29's finding is therefore wider than its wording, and
the practical consequence is the same either way.

**Verdict: deterministic, but not paired.** Every figure below is a seeded point
that reproduces exactly, so SIM-05 holds and the seed budget does not inflate.
What does **not** hold is seed-matching across arms: two λ arms at the same seed
consume different numbers of draws and therefore face different attacker
realisations. They are **independent samples, not matched pairs**, and every
comparison in this record is an across-seed comparison rather than a
seed-matched difference. This is the same status D-29 gives every other
defender-side comparison in the project, so it changes no existing practice —
but it does mean three seeds is a floor rather than a comfortable budget, and it
is why C1's threshold is stated as a sign-consistency requirement across all
three rather than as a pooled mean.

---

## §3 Results

Eighteen agents — six λ points × three seeds — each trained from scratch for 120
episodes and then evaluated over five greedy episodes on fresh networks. 90
evaluation episodes, 2 250 greedy decisions. Raw output and the analysis script
are in the gitignored workspace `data/results/mtd_ai_cost_calibration/`.

**A note on how it was run.** The ladder ran as six parallel single-λ processes
rather than one serial sweep, after the host suspended for nine hours during a
first serial attempt. Every cell is seeded independently of every other, so the
restructure cannot change a result, and the λ = 0 seed 11 cell **reproduced the
serial run's greedy no-op share to three decimal places** (0.064), which is the
check that says so rather than the assertion.

### The ladder

Means over three seeds. `no-op (chosen)` excludes decisions the static-degrade
guard forced; `forced` is the share of decisions the guard took over.

| λ | no-op (all) | no-op (chosen) | forced | mutations / 1 000 s | downtime ratio | mean mutation duration (s) | hosts compromised |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.021 | 0.021 | 0.000 | 4.89 | 0.470 | 99.9 | 9.27 |
| 25 | 0.000 | 0.000 | 0.000 | 5.00 | 0.453 | 90.0 | 7.07 |
| 50 | 0.000 | 0.000 | 0.000 | 5.00 | 0.441 | 90.1 | 6.40 |
| 100 | 0.379 | 0.405 | 0.027 | 3.11 | 0.275 | 93.2 | 7.00 |
| 200 | 0.917 | 0.994 | 0.077 | 0.41 | 0.000 | 93.5 | 10.13 |
| 400 | 0.920 | 0.992 | 0.072 | 0.40 | 0.000 | 88.7 | 9.67 |

Per seed, which is what C1 turns on:

| seed | λ=0 | λ=25 | λ=50 | λ=100 | λ=200 | λ=400 |
|---|---:|---:|---:|---:|---:|---:|
| 11 | 0.064 | 0.000 | 0.000 | 0.216 | 0.912 | 0.920 |
| 22 | 0.000 | 0.000 | 0.000 | 0.000 | 0.920 | 0.920 |
| 33 | 0.000 | 0.000 | 0.000 | 0.920 | 0.920 | 0.920 |

### The pre-registered conclusions, applied

**C4 — the instrument holds.** The λ = 0 greedy no-op share is **0.021**,
against a bar of below 0.10. The cost-free reward's optimal policy is to deploy
on every decision, and that is what the agent trained under it does. The zero
point behaves, so a verdict is readable off the ladder.

**C1 — HELD, and not marginally.** Top-half minus bottom-half greedy no-op
share is **+0.732**, against a bar of 0.15, with the same sign in every seed
(+0.661, +0.613, +0.920). The agent moves less when moving costs more.

**C2 — held.** The realised mutation rate falls from **4.89 to 0.40 per
1 000 s**, and the residue is the guard's floor rather than the policy: at
λ ≥ 200, **29 of the 31 mutations that fired across fifteen evaluation episodes
were forced deployments**, so the policy is contributing almost nothing to the
rate. The downtime metric follows it to 0.000, which is the metric the charge is
levied on doing what the charge asks.

**C3 — passes its own arithmetic and is NOT interpretable. Recorded as not
held.** Mean mutation duration falls 99.9 → 88.7 s and the cheap-mechanism share
rises 0.003 → 0.567, which is what C3 asked for. Both readings are artefacts,
and the ladder's own bookkeeping says which:

- At the **top** of the ladder the mutations are overwhelmingly *forced*, and
  the guard draws uniformly over the four mechanisms by construction. The pooled
  λ = 400 mix is 0.23 / 0.20 / 0.33 / 0.23 — a uniform draw to within sampling
  noise on 30 events. A "cheap share" of 0.567 there is the guard's coin, not a
  preference.
- At the **bottom** the policy is degenerate: λ = 0 fires **IPShuffle on 100 %**
  of 367 mutations across all three seeds. A mean duration of 99.9 s is the
  duration of IPShuffle, not an average over a choice.
- Per seed the cheap share is wildly inconsistent at fixed λ — 0.009 / 0.000 /
  0.000 at λ = 0, but 0.928 / 0.000 / 0.096 at λ = 50 — which is the direct
  evidence that nothing in the mix is tracking cost.

**C5 — no reliable movement, as pre-registered it was never a pass condition.**
Compromise breadth reads 9.27 → 9.67 across the ladder with a dip to 6.40 at
λ = 50, but the per-seed means at fixed λ swing far more than the ladder does
(9.6 / 3.4 / 8.2 at λ = 25; 3.2 / 8.0 / 8.0 at λ = 50), and the pooled
per-episode standard deviation is 2.3–3.8 hosts. Nothing here separates at three
seeds and no directional claim should be read off it.

### The finding the pass conceals, and it matters more than the pass

**The response is a step, not a gradient.** Every one of the eighteen cells sits
at one of two attractors: a greedy no-op share of ≈ 0.000, or ≈ 0.920 — which is
exactly the static-degrade guard's ceiling, one forced deployment per ten
decisions. Only one cell in eighteen (λ = 100, seed 11, at 0.216) is anywhere in
between. Where the flip happens moves with the seed — seed 33 flips at λ = 100,
seeds 11 and 22 between 100 and 200 — but each individual agent is
near-constant.

So what has been demonstrated is that **the cost term reaches the policy and can
flip it**, not that the agent balances cost against risk at the margin. The
agents are essentially constant-action policies, and λ selects which constant.
This is the same policy degeneracy the forensics pass measured in Tay's own
checkpoints — 34 of 55 below 0.5 bits of greedy-policy entropy, several
literally constant — reappearing in a rebuilt agent under a repaired reward,
which is evidence that the degeneracy is a property of the training regime
rather than of those particular runs.

**A second finding, and the one worth carrying into the discussion.** The λ = 0
agent — the one whose reward is Tay's, unmodified — deploys at the maximum
available rate and pins to **IPShuffle**, the single mechanism this project has
separately verified changes nothing the attacker can read
([`../../attacker_read_surface.md`](../../attacker_read_surface.md)). It
compromises 9.27 hosts. The λ = 400 agent barely deploys at all and compromises
9.67. Maximal movement into the attacker's blind spot buys, on this evidence,
approximately what not moving buys. That is not a claim the ladder was built to
test and the seeds do not separate it, but it is the shape of the thing and it
bears directly on what "minimising unnecessary MTD deployments" could ever have
meant here.

### Verdict

**GO, with the scope of the go stated narrowly.**

C1 holds by a wide margin with C4 intact, so the pre-registered rule returns a
pass: the rebuilt agent's willingness to do nothing is driven by the price of
moving, and the architecture and training regime can express that. A scaled
training proposal is therefore worth writing, and it is
[`../../../handoffs/2026-08-08_mtd_ai_scaled_training_proposal.md`](../../../handoffs/2026-08-08_mtd_ai_scaled_training_proposal.md).

**What the go does not license, and each of these is measured rather than
cautionary:**

- **Not graded cost sensitivity.** The ladder measured a threshold. An agent that
  is either always-deploy or never-deploy is not "moving smartly"; it is picking
  one of two constants. Any scaled run has to report policy entropy as a first-
  class outcome, because a bigger network trained the same way will most likely
  produce a bigger constant-action policy.
- **Nothing about the mutation mix.** C3 is not interpretable, so the claim that
  a cost-aware agent shifts *which* mechanism it fires is untested here.
- **Nothing about security.** C5 does not separate. The trade-off is
  demonstrated; whether the trade is a good one is not.
- **Nothing about non-reactive defenders**, and no comparison to any published
  Tay figure — those characterise a uniform random selector, and the project's
  own random-scheme arm is the comparator.

**The cheapest next thing, if the scaled run is approved,** is not a bigger
network. It is to find out whether the step can be made a gradient at CPU scale
— by sweeping the static-degrade factor (which currently *sets* the upper
attractor), by reporting greedy-policy entropy per cell, and by putting ladder
points between 100 and 200 where the flip actually happens. That is a day's
compute against the several this brief's own proposal would cost.

---

## §4 Dispositions opened here

Numbered in the `MTDAI-` namespace the forensics record opened; none is repaired.

| # | What | Evidence | Recommendation |
|---|---|---|---|
| **MTDAI-14** | A deploying decision whose mutation is *suspended* by resource occupation never reaches `_mtd_execute_action`, so it stores no transition. The deploy action's Q-value is trained only on the occasions when deploying worked — the learning-side analogue of MTDAI-04, one step out | §1 | Repair before any scaled run; it biases the agent toward believing deployment always succeeds |
| **MTDAI-15** | `done` is hardcoded `False` on every stored transition, so no episode boundary is terminal and the agent bootstraps across the end of one episode into an unrelated one | §1 | Repair before any scaled run |
| **MTDAI-16** | The trained policies are near-constant: 17 of 18 cells sit at one of two attractors, and λ selects which. This reproduces the degeneracy measured in Tay's checkpoints under a *repaired* reward, so it is a property of the training regime | §3 | Report policy entropy as a first-class outcome; investigate at CPU scale before scaling up |
| **MTDAI-17** | The static-degrade guard both **sets** the upper attractor (0.920 = one forced deployment in ten) and **supplies 29 of 31 mutations** at the top of the ladder, so it is doing the defending in exactly the region the study reports as success | §3 | Sweep it. Until then, no figure at λ ≥ 200 may be attributed to the policy |

**One methodological item, recorded not actioned.** λ, the downtime window and
the reward's per-feature divisors are declared values in the sense
[`../../declared_value_provenance.md`](../../declared_value_provenance.md)
means it. Their reasoning is in §0 of this record, which satisfies the handoff's
requirement, but they are **not** entered in that ledger's machine-readable
form with a generator and a scrutiny history. Whether they should be is Marc's
call; the divisors are rule-derived from substrate constants and would pass the
reproducibility requirement, and λ is swept rather than declared at a point.
