---
status: open                  # executes register E6 (and E7's ranking base); supersedes the retired 2026-09-17 defended-runs plan and the 2026-09-15 unopposed plan — their owed items are carried in §4; Q1–Q5 owed, Q5 is "launch the smoke tonight"; 2026-09-25 adds the §5.3.2 figure critique (§5) and Q6–Q10, Q6 RULED 2026-09-25 (MTDAI-02 overturned: restore Tay's 8/3 path, build in §5.6)
created: 2026-09-22
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E6, §E7
companions: ../workflows/results_section_workflow.md (record → read → draw), the two-phase restructure, landed 2026-09-23 (the headline §5.3.2 reads the interval sweep aggregated by layer, the depth §5.3.3 reads per mechanism with MTDShield as a scheme column; `docs/thesis/FLOATS.md`), 2026-09-24_s45_instrumenting_mtdsim.md (what each metric is; the metrics design handoff retired 2026-09-24)
---

# One new defended corpus: every deployment strategy including MTDShield as released, the deployment interval swept as a range, both attackers, at a thousand seeds

## State of play

**The ruling (E6, E7).** Load the other execution schemes; run Tay's selector as released ("no AI versus AI"; V3: no retraining); sweep the interval as a range in steps rather than 200 s and 2 000 s; the body carries a layer-based aggregation of the change in the success metric against interval, per-mechanism and per-profile panels go to an appendix; the prior evaluations are run, not quoted; rankings are based on the APT attacker model. The periodic timing configuration stands; the simultaneous scheme stays out (Marc's removal, accepted).

**The corpus that exists** (`data/results/ch5_defended/`, 2026-09-17): 30 200 runs — 10 conditions (no defence; seven singles; random and alternative over the seven) × {200, 2 000 s} × 6 arms × 100 seeds, plus the lineage (opportunistic-objective), regime (exponential at 200 s) and verdict-blind arms — in about 40 minutes on seven workers (≈ 12.6 runs/s; 0.12–1.2 s per run, network-layer singles at 200 s the slowest). `run_corpus.py` builds the jobs; `analyse.py` writes `numbers.json`; the generators read it. The no-defence cells are shared with `ch5_s531_unopposed/` bit for bit.

**The seam already takes MTDShield** — *falsified 2026-09-25, see §5.1: no released head loads into the live state builder; restore ruled 2026-09-25, §5.6.* `src/mtdsim/l3_simulation/movement/run.py:112-237`: `mtd_scheme="mtd_ai"` with an `MTDAIConfig(main_network=...)`; the driver `tools/mtd_ai_run.py` (greedy ε = 0 by default — Tay's own harness left ε = 1.0, so every published MTDShield figure characterises a random selector, `mtd_ai_forensics.md` §2). Trained heads sit under `mtdsim-weights-archive/*.h5`; which head is canonical is MTDAI-02's disposition (`mtd_ai_cost_calibration.md` §1: the live 5/6 head). MTDShield selects from the lineage's four mechanisms plus no-op (Tay p.14), not the seven — a declared difference, not a defect.

## 1. The cell set — for acceptance

| Factor | Levels | Why |
|---|---|---|
| Arm | **6**: the baseline attacker; the APT attacker model on $c_1$–$c_4$ and $c_{\mathrm{agg}}$ | body = both attackers, layer-aggregated; appendix = per profile |
| Condition | **11**: no defence; the seven mechanisms alone; random; alternative; **MTDShield as released** | E6 |
| Deployment interval | **50, 100, 200, 500, 1 000, 2 000 s** (Q1) | 50–200 s is the range Zhang and Ho swept; 2 000 s is the chapter's long interval; six points draw a line. **Marc 2026-09-23:** 2 000 s is defended as the top of a range, not by precedent — 50 s to 2 000 s so the results carry the interval on the x axis; when this lands, rewrite §5.1's interval sentence to that (the wording is in the tex comment under the Defence unit) and give Table 5.1's row the six levels |
| Timing distribution | near-periodic only (Q3) | Jin: unlikely to change the results; the exponential arm and Table 5.1's row go, or stay at 200 s only |
| Objective | targeted (held) | ruled 2026-09-20; the opportunistic lineage arm goes with §5.3.3 (Q4) |
| Time limit | 15 000 s; plus the **60 000 s no-defence extension**, both arms | the pace sentence ruled for Table 5.3 (2026-09-22) needs it at the reported seed count |
| Seeds | **100 first (smoke), then 1 000** | seed-count protocol: preliminary floats from 100, the reported numbers from 1 000 |

**Cost.** 10 defended × 6 intervals × 6 arms + 6 no-defence = 366 cells. At 1 000 seeds, 366 000 runs ≈ 8 h on seven workers at the measured rate; the smoke at 100 seeds ≈ 50 min and doubles as the preliminary pass. **MTDShield is unpriced**: a TensorFlow forward pass per decision tick could dominate — the smoke prices it, and if it does, MTDShield runs at 200 s and 2 000 s only (Q2). The 60 000 s cells are cheap (no defence).

## 2. Pins (Table 5.1 → the seam)

As the retired plan: `v2_partial`, `overlay_version="v4_failure_only"`, retrace on, the fresh-host contract on, modulators off, targeted objective on the database set, `substrate_timing_regime="shifted"`, seeds 0–999 shared across arms (D-29: two shared RNG streams — the arms are independent, not paired; state it once where the cross-arm test is named). For MTDShield: `MTDAIConfig` with the canonical head, ε = 0, its four-mechanism pool, the tick declared. The baseline arm through the substrate driver with the same pins.

## 3. What the analyser adds

- The field's success metric per cell (the metrics handoff decides: attack success rate at the objective; network compromise ratio at the time limit; MTTC to first compromise) — the *before/after pair*, no *suppression*.
- The **sweep table**: metric × interval × condition × arm, and its **layer aggregation** (host layer / service layer / credentials, Table 2.4's words) for the body figure.
- The **ranking** per arm at each interval, based on the APT attacker model with the baseline attacker as the comparison (E7); no footnote.
- The **schemes panel**: random, alternative, MTDShield against the best single, both arms — "no AI versus AI".
- The reinstated **stealth and detectability** readings on the no-defence cells (metrics handoff), from the readers the records name.
- Cost quantities only if the restructure keeps them (R3).

Every number through `analyse.py` → `numbers.json` → the generators (`results_section_workflow.md`); nothing hand-typed.

## 4. Carried from the two retired run plans

- **Q1 of the old plan** (random / alternative over the seven, where the lineage pool is four): keep the seven, declared in Table 5.1's condition row.
- **The 60 000 s defended extension** (interval × 4): not run before; still not run unless a ruling asks — the no-defence 60 000 s cells are enough for the pace sentence.
- **User shuffle's negative effect** on the model (the D-32 ratchet) and **complete topology's at 2 000 s** on the baseline: attributions owed to the body text; the record is `ch5_s54_effectiveness_findings.md`.
- **The interrupt-tally cross-check** (`mtd_attack_interrupted` against the ledger): still owed.
- **Q5 of the old plan** (Zhang / Brown claim locators): moot if Table 5.6 dissolves (R4); else verify against the extractions.
- **The Overleaf push** needs the dissertation project's ID and git token (Marc's; the only configured project is the literature review).
- **The Appendix C sensitivity corpus** at 1 000 seeds (owed since 2026-09-20; `ch5_s51_sensitivity/analyse.py`) — a separate launch, same night if the workers are free.

## 5. The headline figure (§5.3.2), a design critique (2026-09-25)

Marc's account of Jin (2026-09-25): the data are fine, extend them in the E6 ways, and **draw them better**. Put the MTD interval on the x axis and the NCR reduction on the y axis as a line chart over 50 s to 2 000 s. Draw a line for every mechanism and execution scheme, plus MTDShield. Then you can see which lines fall more and which fall less. That fits E6 (a line per mechanism; the per-mechanism and per-profile detail in an appendix; a layer aggregation in the body) as long as the lines split across the two levels: **the body draws layers and schemes; the appendix draws every mechanism and every profile.** The critique below covers today's Figure 5.3 (`fig:eff-cross-arm`) and Table 5.4 (`tab:eff-orderings`) and what replaces them. Takeaways come first, per the scrutinise-figure method. Nothing here is ratified.

### 5.1 MTDShield cannot run "as released" in the current tree (the blocker)

- **The best head is `epsilon_0.5_decay_0.99`.** It has the highest summed normalised score in Tay's hyperparameter sweeps (11.00, `tay2024.md` l.314, Fig. 4; next are `gamma_0.85` at 10.77 and `train_start_2000` at 10.39). The upstream repo agrees: `bsubs/MTDSim` `experiments.ipynb` loads exactly this model for its Fig. 6 runs, and the weights are committed under `experiments/AI_model/models_joo_kai/`. The local copy is `mtdsim-weights-archive/main_network_epsilon_0.5_decay_0.99__0848c2e2d5b7.h5`.
- **Its input shapes are `[None, 8]` + `[None, 3, 1]`** (read from the file 2026-09-25). The live builder is `mtdnetwork/mtdai/mtd_ai.py:147-163`. It makes 5 static and 7 time-series features; commit `a39e7850` (2026-08-08, MTDAI-05/12) added the seventh, `downtime_ratio`. **No released head fits.** `mtd_ai_cost_calibration.md` §1's "live 5/6 head" is now 5/7. Tay's 8/3 block survives commented out at `mtd_ai_operation.py:314-362`.
- So MTDShield needs Tay's released 8/3 feature path restored as a selectable layout. The 5/7 path stays as it is. That is a change inside `mtdnetwork/`, and §Hard constraints forbids one. **Q6.**
- **The interval is its decision tick, not its deployment period.** The same `mtd_interval` knob sets it (`run.py:196`). At each tick it deploys one mechanism or does nothing. A 2 000 s staleness guard forces a random deploy (`mtd_ai_operation.py:110`). Tay trained at 200 s, on 100 nodes, with 5 000 s episodes (`train_models.py:38-41`, upstream `62e1ebc`). Every other x position is outside what he trained on. Two of the three time-series inputs (`mtd_freq`, `time_since_last_mtd`) scale with the interval.
- **What to expect, not to report.** A weights probe on synthetic states picks service diversity for 91 % of them (entropy 0.48 bits). It is a probe, not simulator states, so it predicts nothing. But if the probe holds, MTDShield's line will track the service-layer line. That is what the recorder's executions per run (below) will show. The forensics record also has every normalisation layer's variance at exactly 0 (`mtd_ai_forensics.md` §3(a)). That is a declared property of the release, not something to fix (V3).
- **Its pool is four mechanisms** (complete topology shuffle, IP shuffle, OS diversity, service diversity) plus a no-op. That is two host-layer and two service-layer mechanisms, with no credentials mechanism. Random and alternative draw from seven. **So "no AI versus AI" is only a clean comparison against random over the same four** (Q7). That arm is also what every published MTDShield figure measured, because Tay's harness left ε = 1.0 (forensics §2).

### 5.2 The x axis at the short end

Deployment takes 70–110 s for every mechanism except user shuffle, which takes 20 s (`MTD_DURATION`, Zhang 2023 Table 3). A trigger that fires while the layer's resource is busy is suspended (`mtd_operation.py:101-111`). So at 50 s and 100 s the x value is the configured interval, not the realised one: a host-layer single saturates at about one deployment per 100 s. The schemes spread their deployments across two resources (the network and application layers), so they saturate differently from singles. **Keep 50 s** (it is the bottom of the range Zhang and Ho swept; the locator is still to verify), and keep the axis as the interval a defender configures. The corpus already records `executions_per_run` and suspensions (`analyse.py` l.432, 851). Put them in the appendix table, and give the body one sentence on saturation. The cost estimate in §1 comes from 200 s and 2 000 s runs. At 50 s a run has four times as many deployments as at 200 s, so the smoke run is what prices the sweep.

### 5.3 Takeaways the figure must carry (proposed)

| # | Takeaway | 100-seed support (200 s and 2 000 s only) |
|---|---|---|
| H1 | Against the APT attacker model the host layer reduces NCR most and the service layer least. Against the baseline attacker the order swaps. The sweep tests whether the swap holds across the range. | 200 s: model host 0.96, service 0.21; baseline host 0.49, service 0.82 |
| H2 | Every line falls as the interval grows. At 2 000 s everything but the model's host layer (0.22) is near zero. Name where the lines meet, not "why". | 2 000 s: model host 0.22, service 0.01; baseline host −0.01, service 0.10 |
| H3 | No AI versus AI: MTDShield against random over the same four, for each attacker, and where both sit relative to the layer lines. | not yet run |
| H4 | Exception, marked, not explained: user shuffle is at or below zero for both attackers. | model −0.14, baseline −0.07 at 200 s |

H1 is the §5.3.2 headline and the E10(ii) set-up. The figure should make it visible as **lines changing places between the two attacker panels**. A scratch mock-up from the two intervals already run shows exactly that, and cleanly.

### 5.4 The figure (proposed spec)

- **Genre:** a line chart with a marker at each point, the conventions' sweep genre (§f; hong2018 Fig. 5, kim2026 Fig. 8).
- **Panels, 2 × 2:** columns are the attacker, with **the APT attacker model on the left** (E7 makes it the base) and the baseline attacker on the right. Rows are **mechanisms by layer** (host, service, credentials: three lines) over **execution schemes** (random and alternative over seven, random over MTDShield's four, MTDShield: four lines). All four panels share one y range. This keeps the float contract's rule that singles and schemes get separate panels, and it holds every panel to four lines or fewer. One panel per attacker would carry seven lines, with random and alternative lying on top of each other (0.75 and 0.72; 0.09 and 0.03). That one-panel form is the alternative (Q8).
- **x:** the deployment interval in s, **log scale**, ticks at the six levels (1 000 and 2 000 with a thin space). On a linear scale 50–500 s would be squashed into the first quarter of the axis.
- **y:** NCR reduction, fixed at about −0.2 to 1.0. The zero rule is the no-defence reference, named once in the caption.
- **Lines:** a layer line is **the mean of its mechanisms each deployed alone**. That equals 1 − pooled NCR / no-defence NCR, because every mechanism has the same number of runs. The bootstrap resamples the pooled runs. A layer line is not a defence anyone can deploy, and the caption says so in one clause. The credentials "layer" is user shuffle alone, so label that line **user shuffle**. Put direct labels at the **left end (50 s)**, where the lines spread out; at 2 000 s they meet near zero. With four series or fewer, the legend goes.
- **Encoding:** the profile hues already mean $c_1$–$c_4$ in §5.3.3. Reusing them here would give one colour two meanings within one section. So use **greys with a distinct marker per line, and the house accent on MTDShield only**, the element Jin added (Q9). Dashes stay binary: dashed means a scheme, solid means a mechanism.
- **Uncertainty:** 95 % bootstrap whiskers at each point, as in the rest of chapter 5, with a small horizontal offset on the log axis. No bands. At 1 000 seeds the whiskers are about a third as long.
- **Caption:** decode only (the Figure 5.4 pass, 8h-2): which panel is which attacker, what each row holds, what a layer line is, zero as no defence, the whiskers. The current caption's interpretation ("the mechanism behind any difference is structural …", "the chapter's central comparison") moves to the body or is cut. MTDShield's 200 s training interval, its pool and ε = 0 go in Table 5.1 and the text, not on the axes (supervisor 2026-09-22: no definitions in captions or axes).
- **Appendix (E6):** the same form for every one of the seven mechanisms (the user's "every single mechanism") plus the four schemes, one figure per profile $c_1$–$c_4$ and $c_{\mathrm{agg}}$. Add a table of executions per run for each cell (§5.2).

### 5.5 Table 5.4 (the orderings)

- As drawn it ranks the baseline attacker first, with a long footnote. Both break E7.
- Six intervals turn today's two blocks into six. Proposal: a **rank grid**. Rows are the 11 conditions, ordered by the APT attacker model's rank at 200 s. Columns are the six intervals for the model, then the six for the baseline. Cells hold ranks only; the NCR values are in the appendix table. The last row is Spearman's ρ per interval. No footnote.
- The alternative is to keep two anchor intervals and let the figure carry the sweep (Q10).

### 5.6 MTDShield: the ruling and the build (2026-09-25)

**Ruled (Marc, 2026-09-25):** MTDAI-02 is overturned (`mtd_ai_cost_calibration.md` §1). Tay's released model is run as released; in Marc's words it is "more defensible to do something", and he is "winding back that ruling". This settles Q6 and Q2: the head is `epsilon_0.5_decay_0.99` at ε = 0, run at all six intervals, with the 200 s training interval declared.

**Retraining was considered and rejected**, and the costs are on record so the question does not come back. Compute is not what rules it out. The repaired harness (`tools/mtd_ai_run.py`) takes about 4.5 s per 25-decision episode on a CPU, so an agent at Tay's settings trains in about 10 minutes, and one trained across all six intervals in about an hour; no Kaya needed. What rules it out:
- In the August calibration, 17 of 18 retrained agents learned a near-constant policy (MTDAI-16). Under Tay's own reward (λ = 0) the agent fired IP shuffle on 100 % of its deployments.
- MTDAI-14 and MTDAI-15 are still unrepaired.
- A retrained agent is the thesis's own model, not prior work, and brings its own training questions to defend.
- Jin ruled against retraining twice: V3 ("just use the model as is") and E6 ("used as-is").

An interval-aware retrained variant is future work, beside the declined phase three (E1).

**Build (about a day, no training):**
1. **Restore the 8/3 layout as a switch.** Tay's static and time-series vectors come back from `mtd_ai_operation.py:314-362` as a named layout beside the live 5/7 one, which stays the default. Record the feature order beside `STATE_FEATURE_ORDER` / `TIME_FEATURE_ORDER` in `mtd_ai.py`. Wire the choice through `MTDAIConfig`, and add `feature_layout` to `run.py` l.112-139.
2. **Use Tay's evaluation path, at the commit that produced the head.** *(Corrected 2026-09-25: MTDAI-13's ÷ 10 does not apply. Ho added it on 2024-10-09 (`602b9ffe`), after this head was trained.)*
   - Joo Kai Tay added `main_network_epsilon_0.5_decay_0.99.h5` on 2024-09-23 (`f13ed49a`).
   - At that commit, his two builders differ in two slots:
     - the training builder feeds `attack_success_rate` (compromises per SCAN_PORT event) and `overall_time_to_compromise` (a cumulative sum of action durations);
     - the evaluation builder (`mtd_ai_operation.py` l.280-283 at `f13ed49a`, the block now commented out) feeds `overall_asr_avg` and `overall_mttc_avg` (averages over the compromise checkpoints).
   - **Primary run: the evaluation builder as he ran it.** Reusing a released model means running the authors' released inference code. The mismatch is a property of the release; declare it in the appendix item and do not repair it.
   - **One check at 200 s:** the training builder in those two slots, 6 arms × 100 seeds. It shows whether the mismatch moves the line.
   - At that commit the training builder leaves `current_attack_value` unbound when the detection draw fails. So training must have run at attacker sensitivity 1.0 (an inference; verify against `train_models.py` at `62e1ebc`).
   - **Pin sensitivity to what his Fig. 4 evaluation used** (the notebook, cell 1). The APT attacker model's actions are not in `attack_dict`, so for that arm the input always reads 7, "nothing detected". Declare that too.
   - Neither builder changes the simulation. Each reads state and makes one `random.random()` draw per decision, the same count as the live head.
3. **Check it loads.** The head's input shapes `[None, 8]` + `[None, 3, 1]` must match the built vectors; if not, fail loudly.
4. **Gates:**
   - the goldens re-run unchanged, since the default layout is untouched;
   - one seeded episode per attacker at 200 s, with the per-decision ledger (greedy / forced) hand-traced over its first ten decisions (V1);
   - the time for one decision step, which prices the corpus arm;
   - the executions per run and the share of forced deployments, per interval.
5. **Declare** it in Table 5.1 and `FLOATS.md`: head, ε = 0, the four-mechanism pool plus no-op, trained at 200 s against the baseline attacker, the BatchNorm variance-zero property (forensics §3(a)), and Tay's "best" = the highest summed normalised score (`tay2024.md` l.286, 314). The margin over the runner-up (11.00 against 10.77; the same head scored 10.78 in his Fig. 6) is stated once.
5′. **The appendix item (Marc 2026-09-25: the background introduces execution schemes and MTDShield; the appendix says why this model and how it was run; the defended thing is the choice, not a model of ours).** One subsection, in five parts. Each part follows a reuse convention of the field.
   - **(i) Released artefact, not a re-implementation.** Tay's own weights and his own inference code, at the commit that produced them (`f13ed49a`).
   - **(ii) The authors' selection rule, not ours.** "Best" is his: the highest summed normalised score (`tay2024.md` l.286). The head is `epsilon_0.5_decay_0.99`, 11.00 (l.314). His notebook's own choice agrees. The margin over the runner-up is inside his own run-to-run spread (10.77 against 10.78 for the same head), stated once.
   - **(iii) Evaluated greedily.** The standard for evaluating a trained DQN is the learned policy with exploration off or near off. *Verify* the evaluation ε in Mnih et al., Tay's [28]; recalled as 0.05, and if so ε = 0 is declared as the deterministic end. His harness evaluated at ε = 1.0, so his published figures describe a random selector (forensics §2). Running his model greedily is what "run it, don't quote it" (E6) requires.
   - **(iv) What had to change to run it at all, and nothing else.**
     - the trigger loop's no-op fix (MTDAI-03): under a greedy policy Tay's loop never advances the clock;
     - the input layout switch (step 1).
   - **(v) Declared, not repaired:**
     - the training/evaluation input mismatch (step 2);
     - BatchNorm variance 0;
     - the value of doing nothing never trained;
     - trained at 200 s, against the baseline attacker, on 100-node networks (the corpus runs 50 hosts, and one input, `exposed_endpoints`, counts with network size);
     - the IDS input reads "nothing detected" for the APT attacker model.

   Then **the matched control** (Q7) and why it is there. This is also what makes it an execution scheme like the others, so every §5.3 float that reads the corpus can carry it as a condition (§5.3.2's headline; §5.3.3's scheme column).
5a. **Prediction, written before the smoke run (the calibration record's discipline).**
   - **How the head was trained:** `train_start` 1 000 in a 2 000 buffer at about 25 transitions per episode, so learning starts around episode 40 and runs for about 60 episodes, batch 32.
   - **Exploration:** ε went from 0.5 to about 0.18, decayed per episode. The head was never trained under exploitation.
   - **Known defects:**
     - BatchNorm variance is 0 (MTDAI-07);
     - no no-op transition was ever stored, so the value of doing nothing was never trained (MTDAI-04);
     - it picks service diversity on 91 % of synthetic probe states (entropy 0.48 bits).
   - **Predicted:** a near-constant selector that fires service diversity at most ticks, with the 2 000 s guard rarely firing. Its line then tracks the service-layer line for both attackers.
   - **Would falsify it:** in the per-decision ledger, a service-diversity share below 0.7 at 200 s, or a no-op share above 0.2. Either means the real states land elsewhere than the probe's, and that is the finding.
5b. **The interval (considered, not adopted for the body).** Two of the 11 inputs scale directly with the interval:
   - `time_since_last_mtd` is about the interval at each tick;
   - `mtd_freq` is about 1 / interval.
   Rescaling them by 200 / interval would give the model its training-time values. But that is an adapter the thesis would have to defend. It fixes 2 of 11 inputs: the security metrics still change by a different amount between ticks. And it tells the model its last deployment was 200 s ago when it was 2 000 s ago. **The body runs it unadapted at all six intervals, with the 200 s training interval declared.** The rescaled run is an appendix check only if the unadapted line's shape away from 200 s differs from random over the same four (Q7).
6. **Add the arm and Q7's matched control** (random over the same four) to `run_corpus.py`. Both join the 100-seed smoke.

### 5.7 Where MTDShield lands in the dissertation (RULED and APPLIED 2026-09-25: Marc accepted items 1-5; item 1 and Appendix E are in the tex, item 2 is staged as a tex comment in §5.1 until the condition runs, items 3-4 follow the run)

**Applied, and what it found beyond this plan.**
- **Tay's scores were produced with ε = 1.0.** The release's `execute_ai_model` defaults it and the notebook's `mtd_ai_simulation` does not forward it; with the no-op re-entry, every scored run deployed a mechanism drawn uniformly from the four at every tick. So the 38 scores (9.46-11.00) are one random selector's run-to-run spread, and the designation is adopted as Tay's, with no measured superiority. §E.1 says so, and that is why Q7's matched arm is argued there.
- **The release's decision loop differs from the live loop in two further places:** the guard forced complete topology shuffle (action 1), where the live form is Ho's random draw (`408882b`); and each decision enqueued twice (MTDAI-08). §E.3 keeps the simulator's loop for every condition. The guard is **flagged for Marc** in the appendix's head comment.
- **Alternatives ranked in §E.1:** designation (taken) / re-scoring his 38 greedily (rejected: it makes the selection the thesis's, a step towards optimising the defence) / retraining (rejected: not prior work).

**The rule that sets the placement:** the background describes prior work, §5.1 states the choice, and the appendix holds the evidence for it. Each place carries only its own job, and nothing is said twice.

1. **Chapter 2 (background), about 1 sentence added.** Table 2.5 and the paragraph after it (tex l.816-870) already introduce MTDShield as prior work. Add the fact the choice rests on: Tay released the trained agents from his hyperparameter study and named a best one by a summed score normalised to no defence (`tay2024` §5.1). No selection and no defects here; the background describes, it does not choose. The paragraph's "the interval … is 200 s" stays: it is the simulator's default. The sweep is §5.1's.
2. **§5.1 (setup), 1 sentence plus two table rows.**
   - The sentence: MTDShield is run as released, as Tay's best-scoring agent acting greedily, with its selection, configuration and the release's known properties in Appendix E.
   - Table 5.1's condition row gains *MTDShield* and *random over MTDShield's four*.
   - The interval row gets the six levels (§1).
3. **§5.3.2 and §5.3.3:** MTDShield is one more scheme line or column, with no prose about the release. The one reading sentence is what the line shows.
4. **Chapter 6:**
   - E10(ii) may use the line: a selector tuned against the baseline attacker, measured against the APT attacker model.
   - The limitations paragraph points to Appendix E in one sentence.
5. **Appendix E "MTDShield as run"** (a new appendix chapter, after "Supplementary sensitivity analyses"). The code is cited once, by repository and release commit, in the bibliography. Paper claims are cited by section and figure. **No line numbers in the dissertation**; they stay in the repo records (`mtd_ai_forensics.md`), which carry them already.
   - **E.1 Selection.** One paragraph and Table E.1: the winner of each of Tay's three sweeps with its summed score (11.00, 10.77, 10.39; his Figs. 3-5) and the one run. The criterion is his; the margin is inside his run-to-run spread, said once.
   - **E.2 Configuration.** Table E.2, *parameter | Tay's training | Tay's evaluation | this thesis | source*, one row each: head, ε, pool, decision tick, attacker sensitivity, 2 000 s guard, network size, horizon, attacker. **This table carries the defence.** The side-by-side columns show where the thesis departs from the training conditions. They also show that Tay's own evaluation departed too (150 nodes and 15 000 s against training at 100 and 5 000; verify against the notebook's cell 1), so running outside training follows his own practice.
   - **E.3 The two changes needed to run it.** The no-op loop (MTDAI-03) and the input layout switch. Each with why, and the fact that neither changes the simulation (both read state; one random draw per decision, as before).
   - **E.4 Properties of the release.** Table E.3, *property | evidence | what it means for the reading | handling (declared / checked)*. Five rows: the training/evaluation input mismatch (with the 200 s check's result); BatchNorm variance 0; the value of doing nothing never trained; ε = 1.0 in the published figures; the IDS input never registering the APT attacker model. Neutral register: facts with sources, no evaluative adjectives. It describes a release, not a verdict on Tay's year.
   - **E.5 Behaviour observed.** Written after the run, from the per-decision ledger: action shares per interval per attacker, and the share of deployments the guard forced. If the model mostly fires one mechanism, that is reported here as what it does, against the prediction in §5.6 step 5a.
   - **E.6 (only if triggered)** The input-rescaling check (§5.6 step 5b).

## Rulings owed (Marc)

- **Q1** the interval levels (six proposed).
- **Q2** MTDShield: the head, ε = 0, and whether it runs at every interval or two.
- **Q3** drop the exponential timing arm (recommended).
- **Q4** drop the opportunistic-objective lineage arm (recommended; §5.3.3 dissolves).
- **Q5** launch the 100-seed smoke tonight, before Q1–Q4 are all ruled — the smoke is cheap and the cell set is a superset. *(2026-09-25: the smoke can still launch without the MTDShield arm, which waits on Q6.)*
- ~~**Q6**~~ **RULED 2026-09-25 — restore; see §5.6.** Restore Tay's released 8/3 feature path as a selectable layout in `mtdnetwork/mtdai/`, the head `epsilon_0.5_decay_0.99`, ε = 0 (§5.1). This lifts the no-substrate-change constraint for that path only; the goldens must re-run untouched. **Recommended**: it reinstates the code that was released rather than changing the simulator. Without it, the "AI" in "no AI versus AI" cannot run. It also settles Q2: all six intervals, because the tick is the same knob the schemes use, with the 200 s training interval declared.
- **Q7** Add **random over MTDShield's four mechanisms** as a condition: 6 intervals × 6 arms = 36 cells, cheap. **Recommended**: it is the like-for-like "no AI" arm, and it is what Tay's published figures measured.
- **Q8** Figure layout: 2 × 2 (attacker × mechanisms/schemes; **recommended**) or one panel per attacker with seven lines.
- **Q9** Encoding: greys with one marker per line and the accent on MTDShield (**recommended**), or a new colour contract for conditions.
- **Q10** Table 5.4: a rank grid over all six intervals (**recommended**) or two anchor intervals.
- **Tell Jin (carried):** the y axis is NCR reduction, not the change in attack success rate he said on 2026-09-22. Marc's 2026-09-25 account already says NCR reduction. If Jin has agreed to it, record that here and close the item.

## Validation gate

`runs.jsonl` complete for every cell at 1 000 seeds, zero errors in `run.log`; `numbers.json` carries every quantity the restructure's float tree reads; the smoke's floats and the thousand-seed floats agree in direction; every ch5 float regenerated at 1 000 with "preliminary" nowhere; the MTDShield arm's ε, head and pool declared in Table 5.1 and `FLOATS.md`.

## Hard constraints

- No substrate change; no retraining (V3); goldens untouched.
- Determinism: shared seeds; the RNG-stream fact (D-29) stated once.
- The hand-trace protocol (V1) for any metric that is new to the analyser.
- `runs.jsonl` is gitignored (2 GB last time); `numbers.json` and `summaries.pkl` are what the generators need.

## Reading list

- `data/results/ch5_defended/run_corpus.py`, `analyse.py` — extend, do not fork.
- `src/mtdsim/l3_simulation/movement/run.py` l.112–237 — the MTDShield seam.
- `tools/mtd_ai_run.py`; `docs/implementation/pipeline/ogasp/mtd_ai_forensics.md` §2, §9; `mtd_ai_cost_calibration.md` §1 (MTDAI-02).
- `docs/implementation/pipeline/ogasp/ch5_s54_effectiveness_findings.md`, `ch5_s55_efficiency_findings.md` — the readings the old floats made.
- `docs/workflows/results_section_workflow.md`.

## Out of scope

The design of the other figures (§5.3.2's is now §5 here, 2026-09-25); the metric definitions (metrics handoff); any MTD optimised against the APT attacker (declined, E1).

## Carried from the retired metrics design (2026-09-24)

- **Tell Jin before week 9 (E11):** E6's interval line chart will read **NCR reduction** against the interval, not the change in attack success rate he asked for, because the APT attacker model's ASP is floored at zero under most defences and cannot order them.
- §5.3.1's own reads come from `data/results/ch5_defended/disruption.py` (not `analyse.py`); rerun it on the 1 000-seed corpus with the rest, then `tools/ch5_disruption_figure.py`.
