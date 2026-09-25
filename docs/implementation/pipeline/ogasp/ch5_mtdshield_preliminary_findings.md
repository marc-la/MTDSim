---
status: findings — preliminary (100 seeds, 200 s and 2 000 s); prediction written before the corpus read; results §4, floats regenerated 2026-09-25
created: 2026-09-25
topic: "Tay's released MTDShield agent run as released in the chapter 5 defended corpus: the build, the gates, the prediction, and what the agent does against both attackers"
---

# MTDShield in the defended corpus: the preliminary read

**Brief:** [`../../../handoffs/2026-09-25_mtdshield_preliminary_run.md`](../../../handoffs/2026-09-25_mtdshield_preliminary_run.md)
(the E6 handoff's §5.6–§5.7 at preliminary scale). **Workspace:**
`data/results/ch5_defended/` (gitignored): `run_corpus.py` with `SHIELD=1`
appends 3 600 runs to `runs.jsonl` (log `run_shield.log`); `analyse.py` →
`numbers.json`.

## 1. The build

- **Agent:** `mtdsim-weights-archive/main_network_epsilon_0.5_decay_0.99__0848c2e2d5b7.h5`
  (Tay's `f13ed49a`), loaded with `keras.saving.load_model(compile=False)`.
  Input shapes `[None, 8]` + `[None, 3, 1]`, five outputs (no-op + his four).
  ε = 0, attacker sensitivity 1.0, the simulator's loop (single enqueue, random
  forced deployment after 2 000 s idle, the no-op waits for the next tick).
- **Layouts** (`mtdnetwork/mtdai/mtd_ai.py`, `FEATURE_LAYOUTS`; builders in
  `mtd_ai_operation.py`): `live` (5/7, default, unchanged), `tay2024_eval` and
  `tay2024_train`, both restored verbatim from `f13ed49a`. `check_layout`
  fails loudly on a shape mismatch. `MTDAIConfig.feature_layout` carries it.
- **Conditions** (`run_corpus.py`): `mtdshield` (evaluation builder, the
  primary), `random_four` (random over the same four, the matched control),
  `mtdshield_train` (training builder, the input check). The baseline arm now
  builds `MTDAIOperation` for `mtd_ai`, as `tools/mtd_ai_run.py` does. Each
  `mtd_ai` run records its ledger (`mtd_decisions`: time, action, source).

### 1.1 What the dig found beyond the brief

- **The evaluation builder feeds four constant zeros.** `Evaluation.__init__`
  copies the attack and MTD records (`get_record()` builds a fresh DataFrame)
  when `MTDAIOperation` is constructed, at t = 0, when both are empty. So
  `host_compromise_ratio`, `overall_asr_avg`, `overall_mttc_avg` and `mtd_freq`
  read 0 for every decision of every run. Same code at `f13ed49a`, so Tay's own
  evaluations fed the same zeros. The training builder reads them live. The
  "two slots differ" of the brief is therefore **five** inputs differ (those
  four, plus `shortest_path_variability`, which the two builders compute by
  different formulas). Declared, not repaired; Appendix E's limitation bullet
  needs this.
- **The detection input does register the APT attacker model.** The model
  drives the substrate's verb cores, so `attack_type` reads 4, 5, 6 (exploit,
  neighbour scan, brute force) and 7 during dwell. Appendix E's bullet "codes
  only the baseline attacker's actions" is falsified; what is true is that
  dwell reads 7, the same value as a missed detection.
- **The live 5/7 builder crashes against the APT attacker model**
  (`ZeroDivisionError` at `attack_success_rate = compromised_num /
  attack_event_num`: the model compromises hosts without a SCAN_PORT row).
  Pre-existing; out of scope here (MTDShield does not use it). The training
  builder has the same line; any crash under `mtdshield_train` is recorded as a
  dead cell, not repaired.

## 2. Gates

- **Goldens:** `tests/test_mtd_golden_streams.py` fails 7 of 7 **before** this
  work (the goldens predate recent model changes), so it cannot gate. Replaced
  by a before/after digest (scratch script): 4 golden configs, 20 corpus rows
  (both arms × none, IP shuffle, service diversity, random, alternative × seeds
  0–1), and the live `mtd_ai` path: **25 of 25 identical** after the edit.
- **Corpus reproducibility:** four existing `runs.jsonl` rows re-dispatched on
  today's tree are byte-identical, so appending is sound.
- **Hand-trace (V1), seed 0, 200 s, both builders, baseline and `c_agg`:**
  for all 10 traced decisions per run, the ledger's action equals the argmax of
  the agent's Q values on the traced inputs, the source is `greedy`, and the
  executions that follow are that mechanism. 75 decisions, 68–72 executions.
- **Timing:** one forward pass 23 ms; a whole run at 200 s 3–8 s.

## 3. The prediction (E6 handoff §5.6 step 5a, written 2026-09-25 before any run)

- **Predicted:** a near-constant selector that fires service diversity at most
  ticks, with the 2 000 s guard rarely firing; its NCR-reduction column then
  sits with service diversity's for both attackers.
- **Falsifier:** a service-diversity share below 0.7, or a no-op share above
  0.2, at 200 s, in the per-decision ledger.
- *Disclosure:* the seed-0 hand-trace (§2) was read before the corpus. It
  showed service diversity on 91–96 % of decisions and a no-op when the
  detection input reads 4.

## 4. Results

All from `numbers.json` (`s541`, `s542`, `shield`), 100 seeds per cell; the
model is $c_1$–$c_4$ pooled (400 runs). 3 600 runs appended (`runs.jsonl` 33 800
lines); zero errors in `mtdshield` / `random_four`; 445 dead runs, all
`mtdshield_train` on the model arm (§4.4).

### 4.1 NCR reduction (Tables 5.3, 5.4; Figures 5.4, 5.5)

| | model 200 s | baseline 200 s | model 2 000 s | baseline 2 000 s |
|---|---|---|---|---|
| MTDShield | 0.28 [0.23, 0.34], rank 8/11 | 0.70 [0.65, 0.75], rank 3 | 0.03 [−0.04, 0.10] | 0.06 [−0.05, 0.15] |
| random, MTDShield's four | 0.80 [0.78, 0.82], rank 4 | 0.56 [0.50, 0.61], rank 6 | 0.13 [0.06, 0.19] | −0.02 [−0.12, 0.08] |
| random (seven) | 0.75 [0.72, 0.77] | 0.33 [0.26, 0.41] | 0.09 | −0.03 |
| alternative (seven) | 0.72 [0.69, 0.74] | 0.39 [0.31, 0.45] | 0.03 | −0.05 |
| service diversity alone | 0.36 [0.31, 0.41] | 0.91 [0.88, 0.93] | 0.04 | 0.30 |

Read (measurement only, no attribution beyond the ledger):
- **"No AI versus AI" reverses with the attacker at 200 s.** Against the
  baseline attacker MTDShield beats its matched random control (0.70 vs 0.56,
  intervals apart) and ranks third of eleven. Against the APT attacker model it
  is far below it (0.28 vs 0.80) and ranks eighth, under every host-layer
  single and every other execution scheme.
- **It sits where its ledger puts it:** under service diversity alone for both
  attackers (0.28 vs 0.36; 0.70 vs 0.91), consistent with a service-diversity
  selector that does nothing on a quarter of its ticks. H1 (the host/service
  swap between attackers) carries MTDShield with it.
- **At 2 000 s** every scheme is within noise of zero for the baseline
  attacker; for the model, random over the four keeps 0.13 and MTDShield 0.03.
- Random over the four is ≥ random over the seven for both attackers at 200 s
  (0.80 vs 0.75; 0.56 vs 0.33): the four pool carries two host-layer shuffles
  of four, the seven three of seven plus user shuffle.

### 4.2 What the agent chose (the ledger)

| | 200 s baseline | 200 s model | 2 000 s baseline | 2 000 s model |
|---|---|---|---|---|
| service diversity | 0.761 | 0.700 | 0.460 | 0.645 |
| no-op | 0.229 | 0.292 | 0.325 | 0.212 |
| other three together | 0.009 | 0.009 | 0.215 | 0.144 |
| forced (share of decisions) | 0.007 | 0.001 | 0.278 | 0.183 |
| executions per run | 57.9 | 53.1 | 5.4 | 6.3 |

75 decisions per run at 200 s, 8 at 2 000 s; every non-forced decision
`greedy`. The forced draws are uniform over the four (the simulator's rule), so
the "other three" share at 2 000 s is the guard's, not the policy's.

### 4.3 The prediction

Service-diversity share ≥ 0.7 at 200 s: **held** (0.76; 0.70, on the line).
No-op share ≤ 0.2 at 200 s: **failed** (0.23; 0.29). The falsifier fires on its
second clause: the agent does nothing more often than the probe suggested. The
seed-0 trace pairs the no-op with the detection input reading 4 (exploit); that
is one trace, not a measured cause.

### 4.4 The input-definition check (Tay's training builder)

- Baseline attacker: 0.71 [0.67, 0.76] vs 0.70 [0.65, 0.75] at 200 s; 0.08 vs
  0.06 at 2 000 s; service diversity 0.79 vs 0.76. **No measurable difference.**
- APT attacker model: the training builder raises `ZeroDivisionError` in 435 of
  500 runs at 200 s and 10 of 500 at 2 000 s (`compromised_num /
  attack_event_num`, the SCAN_PORT count; the model compromises hosts without
  one). The 47 surviving pooled runs at 200 s read 0.25 [0.11, 0.37], inside the
  evaluation builder's interval, but they are a selected subset.
- So the check licenses "the input definitions do not move the baseline
  arm's result"; for the model arm the training builder cannot run as released.

### 4.5 Owed / for Marc

- The short name for the matched control: "random, MTDShield's four" in the
  floats (proposed; Q7). "random" and "alternative" are over the seven.
- Figures 5.4 and 5.5 are restacked: (a)–(b) singles full width, (c)–(d) the
  four execution schemes per interval side by side (eleven slots in one row
  collide at the figure face). Captions' panel letters updated.
- Appendix E: the "two inputs" and "detection input" limitation bullets are
  corrected (§1.1); E.5 populated. Table E.2 still says 1 000 runs per condition
  (the declared count).
- The live 5/7 builder crashes against the APT attacker model (§1.1): not in
  scope, flagged.
- The goldens fail 7/7 before this work: flagged (someone owes a recapture or
  a reason).
