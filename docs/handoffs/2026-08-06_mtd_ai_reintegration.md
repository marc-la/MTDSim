---
status: superseded by 2026-08-07_mtd_ai_cost_calibrated_rebuild.md
created: 2026-08-06
---

# Get Tay's reactive `mtd_ai` defender running against the movement attacker — the integration every consequential stealth claim is gated on

> **Superseded 2026-08-07 — read this banner before anything below it.**
> [`../implementation/pipeline/ogasp/mtd_ai_forensics.md`](../implementation/pipeline/ogasp/mtd_ai_forensics.md)
> falsified both of this brief's load-bearing premises. It is kept for its defect
> list (§3), its determinism gate (§4), its wiring seam (§5.3) and its hard
> constraints (§7), all of which survive and are carried forward into
> [`2026-08-07_mtd_ai_cost_calibrated_rebuild.md`](2026-08-07_mtd_ai_cost_calibrated_rebuild.md).
> The two corrections:
>
> - **§1 is falsified as written.** `action == 0` is real and does gate the
>   register-and-trigger block, as verified — but it also gates the
>   `yield self.env.timeout(...)`, so a do-nothing decision advances no simulated
>   time. Under ε-greedy selection it is rejection sampling; under a greedy policy
>   it livelocks. **The do-nothing therefore never produces a stiller network**,
>   and the suppression ceiling quantified here, while arithmetically correct,
>   describes a mechanism unreachable in the code as written (forensics §6).
>   Separately, the root cause is upstream: the reward has **no cost term**, so
>   "always deploy" is optimal and action 0's Q-value is never a TD target
>   (forensics §5).
> - **§2's question is dissolved, not answered.** The reuse arm was proposed as a
>   *control* on the assumption that Tay's reported behaviour is his weights'
>   behaviour. It is not: `epsilon` defaults to 1.0 in `execute_ai_model` and the
>   evaluation harness never overrides it, so **every figure in the paper was
>   produced by a uniform random selector and `predict` was never called**
>   (forensics §2, verified at five commits). The project's existing
>   random-scheme defender over the same four mechanisms already *is* the
>   faithful replication of those results, and is a cheaper and stronger control
>   than the one proposed here.
>
> §6's cheap falsifying run also needs re-reading: it assumed a mutation-choice
> distribution that responds to the attacker. Its generalisation — sweeping the
> declared cost weight and reporting the no-op share — is Stage 3 of the
> successor brief.

**Why this is its own handoff.** The knowledge-gated attacker brief
([`2026-08-06_knowledge_gated_apt_attacker.md`](2026-08-06_knowledge_gated_apt_attacker.md))
needs a defender that *responds to attacker behaviour*, and `mtd_ai` is the only
one in the pool that does. But standing up that agent is a distinct piece of work
with its own defects, its own methodological question and its own determinism
risk — bundling it into the attacker brief would hide all three. **This handoff
delivers a working, trustworthy `mtd_ai` arm; it builds no attacker mechanism.**

**Blocked on a supervisor ruling** (R-B in the attacker brief): Tay's agent is
deferred to the ablation phase by standing project direction, and `mtd_ai` has
**never been run against the movement arm at all**. That ruling is the
prerequisite; everything below assumes it lands.

---

## 1. The one thing that makes this worth doing — the defender can choose to do nothing

Verified in code, `mtd_ai_operation._mtd_trigger_action`:

```python
action = choose_action(state, time_series, self.main_network,
                       len(self.mtd_strategies) + 1, self.epsilon)
...
if action > 0:                      # 0 == DO NOTHING
    ...register / trigger the MTD...
```

**`action == 0` is a real, reachable "do nothing", and it gates the entire
register-and-trigger block.** The action space is `len(strategies) + 1` precisely
to hold it. So an attacker whose behaviour biases the agent's state toward
inaction gets a **materially stiller network** — which is the premise the attacker
brief's design rests on, and it is not speculative.

**Two hard ceilings bound it, and both are quantified.** These are the reason a
claim here can be honest rather than open-ended:

- **`static_degrade_factor = 2000` (default).** When
  `env.now − last_mtd_triggered_time > 2000`, the agent is bypassed and a
  **random deploying action** (1..len) is forced. Note the timer is reset **only
  when `action > 0`**, so consecutive do-nothings accumulate toward it. Against a
  15 000 s horizon that is a floor of roughly **seven forced mutations per run**,
  whatever the attacker does.
- **`choose_action` is ε-greedy.** With probability `epsilon` it returns a
  uniformly random action over the whole space, so a deploying action fires
  regardless of state. **`epsilon` has no default in the constructor signature**
  (`epsilon=None`) — establishing what the run wiring passes, and what Tay used,
  is step 1 below.

Together these give the strategy a measurable ceiling: *the longest still window an
attacker can engineer, and the residual mutation rate it cannot suppress.* Report
both beside any suppression claim.

---

## 2. The methodological question this handoff must put to Marc — reuse or retrain?

**The pretrained weights were trained against the inherited 6-phase attacker.**
Running them against the movement attacker puts the agent **out of distribution**,
and a DDQN off its training distribution can behave arbitrarily. That is not a
detail; it decides what any result means.

| | what it buys | what it costs |
|---|---|---|
| **Reuse as-is** | strictly honours *"replicate, never extend"*; no new training procedure to defend; comparable to Tay's own reported behaviour | the agent is out-of-distribution against the movement arm, so *"the attacker steered the defender"* may be indistinguishable from *"the agent was never trained for this input and is behaving noisily"*. **This is the interpretation-killer** |
| **Retrain against the movement attacker** | the agent is in-distribution and its choices are meaningful | retraining is arguably still replication (same architecture, same reward, new data) rather than extension — **but that is exactly the judgement Marc must make**, not a session. It also breaks comparability with Tay's published figures, and adds a training procedure that must itself be documented and seeded |

**Recommended framing for the ruling, not a decision:** run **both** if the budget
allows, and treat the reused-weights arm as the *control* — if the two agents make
similar mutation-choice distributions against the same attacker, out-of-distribution
noise is not driving the result; if they diverge, the reused arm cannot carry a
claim. That converts the question from a coin-flip into a measurement.

---

## 3. Defects on this path, found by reading and unverified by running

Each needs verifying against an instrumented run before it is treated as real, and
each is a **separate disposition** — none should be repaired as a side effect of
getting the arm running.

1. **Unguarded divide-by-zero.** `attack_success_rate = compromised_num /
   attack_event_num`, where `attack_event_num` counts **`SCAN_PORT` rows only**,
   within the 60 s window. Zero whenever the attacker has not port-scanned
   recently — **which is exactly the quiet-attacker condition this whole
   programme is trying to produce.** Expect it to fire. Decide the disposition
   before it crashes a run, not after.
2. **`roa` and `risk` are single samples, not aggregates** — `[-1]`, the most
   recently exploited vulnerability's. A defender state that swings on one
   vulnerability is fragile, and an attacker steering it is steering one number.
3. **The 60 s compromise window** (`comp_check_interval = 60`) appears nowhere in
   Tay's paper as far as this project's extraction records. Verify against the
   extraction before any claim leans on it.
4. **The attacker-sensitivity path** was fixed (D-13, Marc 2026-07-29) so
   sub-1.0 sensitivity no longer raises `UnboundLocalError`. Confirm the fix is
   live on this path before running the sensitivity arm.

**The honesty constraint that travels with all four.** If the attacker's advantage
turns out to depend on any of these, the claim is *"this attacker exploits a
property of Tay's implementation"* — **not** *"this attacker defeats reactive
MTD"*. That distinction belongs in the results record, not in a footnote, and an
examiner will find it if the record does not state it.

---

## 4. Determinism — the risk that could sink the arm entirely

**SIM-05 requires deterministic, reproducible runs, and this arm introduces a
neural-network forward pass into the decision loop.** Before anything else is
built on it:

- Verify that `main_network.predict(...)` is **bit-reproducible** across runs for
  fixed weights and fixed inputs, under the current TF 2.21 / Keras 3.14 build.
  Thread scheduling and non-deterministic kernels are the usual culprits.
- Verify that `np.random.rand()` inside `choose_action` and the
  `random.randint` in the static-degrade fallback draw from streams the existing
  seeding controls, and that they do not perturb the attacker's own streams —
  D-29 already records that mechanisms and attacker share one RNG stream, so
  **adding draws here shifts the attacker's stream** and every seed-matched
  comparison with it.
- If determinism cannot be established, say so and treat every `mtd_ai` figure as
  distributional over repeated runs rather than as a seeded point. That is a
  legitimate fallback but it changes the seed budgeting for every study
  downstream, so it must be known early.

---

## 5. Recommended order

1. **Establish the parameters.** What `epsilon`, `static_degrade_factor`,
   `attacker_sensitivity` and `features` does a faithful Tay replication use?
   Source them from the extraction, not from the constructor defaults; record any
   that the code and the paper disagree on.
2. **Determinism gate (§4).** If this fails, stop and report — everything after
   it changes shape.
3. **Wire the arm.** The L3 run wiring constructs the time-triggered
   `MTDOperation` directly (`movement/run.py::_maybe_start_mtd`); `mtd_ai` needs
   `MTDAIOperation` with its own constructor arguments. Keep it selectable at the
   same seam every other input is named at — an experiment names its defender, and
   the default must stay what has always run.
4. **Smoke it against the inherited attacker first.** That is the in-distribution
   case and the only one where "the agent behaves sensibly" is checkable.
5. **The cheap falsifying run** — §6.

---

## 6. The cheap falsifying run, before any attacker mechanism is built

**This is the highest-value single output of this handoff**, and the stealth
conceptualisation record's §17 already specifies it: run the **existing** profiled
attacker against `mtd_ai` unchanged. The five profiles already differ in
non-action share by more than a factor of two — a naturally-occurring behavioural
spread, with no new mechanism.

**Report the mutation-choice distribution, not the outcome**, and report it with
three quantities the §1 ceilings make meaningful:

- the **share of decisions where `action == 0`** — the do-nothing rate, which is
  the thing the attacker brief's design claims to move;
- the **realised mutation rate** against the `static_degrade_factor` floor and the
  ε-greedy floor, so suppression is reported against what is achievable rather
  than against zero;
- the **mix over mechanisms** — because the mechanisms are not interchangeable
  against this attacker (a network-class firing delivers 0.92–1.00 of its
  disruption to the movement arm, an application-class one 0.67–0.83), so steering
  the mix is an advantage even if the *rate* never moves.

**If the choice distribution does not differ across that spread, a declared
attacker mechanism will not rescue it, and the cheap run has saved the expensive
one.** That is the whole point of running it first.

---

## 7. Hard constraints

- **Replicate, never extend.** Consuming `mtd_ai` unchanged as a defence arm is
  what R-B would sanction. Wiring any attacker state into `attacker_sensitivity`
  is reverse-modelling detection and stays forbidden, whatever else is ruled.
  Retraining (§2) is the one item where "extend" is genuinely arguable and is
  therefore Marc's call rather than a session's.
- **No defect repaired silently.** §3's four items are dispositions; getting the
  arm running must not quietly fix any of them, because each changes what a result
  means.
- **The `mtd_ai` arm is bounded to the reactive case.** Time-triggered MTD is
  unaffected by attacker tempo, so nothing learned here generalises to the rest of
  the defence pool, and the write-up must say so.
- Determinism (SIM-05, but see §4); envelope-not-actor; within-substrate
  comparability only; Australian English; branch per session; never push.

---

## 8. Reading list

- [`2026-08-06_knowledge_gated_apt_attacker.md`](2026-08-06_knowledge_gated_apt_attacker.md)
  §5 — the four steerable features and the reward that closes the loop; this
  handoff supplies the arm that §5 reasons about.
- [`../implementation/pipeline/ogasp/stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
  §8 (the verification that `mtd_ai` keys on attacker activity), §17 (the four
  prerequisites and the cheap falsifying run this handoff formalises).
- `mtdnetwork/operation/mtd_ai_operation.py` — the trigger loop (§1) and
  `get_state_and_time_series` (§3).
- `mtdnetwork/mtdai/mtd_ai.py` — `choose_action` (ε-greedy) and the reward.
- [`../implementation/architecture.md`](../implementation/architecture.md) §(a),
  Tay decision block — the authoritative reuse-vs-retrain disposition as it
  currently stands, which §2 asks to be revisited.
- [`../implementation/disruption_wiring.md`](../implementation/disruption_wiring.md)
  — the per-class disruption figures that make the mutation *mix* worth steering.

---

## 9. Out of scope

- Any attacker mechanism — that is the knowledge-gated brief.
- Repairing §3's defects, or D-18, or the shared-RNG issue (D-29).
- Extending Tay's agent in any way beyond the retraining question §2 escalates.
- Claims about non-reactive defenders.
- Dissertation prose.
