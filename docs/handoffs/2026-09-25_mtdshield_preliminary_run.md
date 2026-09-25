---
status: open
created: 2026-09-25
executes: the MTDShield half of 2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md (§5.1, §5.6, §5.7), at preliminary scale only
---

# Get Tay's MTDShield running as released, add it to the existing 100-seed corpus at 200 s and 2 000 s, and show it in §5.3.1–§5.3.3

**Why:** Marc wants a first look at how MTDShield runs before the six-interval, 1 000-seed corpus. Its trained agent goes in as one more execution-scheme column in the §5.3 floats. **No training.** The agent is Tay's own, run as released.

## State of play

- **Ruled (Marc, 2026-09-25):** run the released agent `mtdsim-weights-archive/main_network_epsilon_0.5_decay_0.99__0848c2e2d5b7.h5`, Tay's highest-scoring agent, at ε = 0. MTDAI-02 is overturned. No retraining. The inputs go in as measured at every interval, not rescaled.
- **The blocker:**
  - The agent takes inputs of shape `[None, 8]` + `[None, 3, 1]`, but the live builder (`mtdnetwork/mtdai/mtd_ai.py:147-163`, `get_state_and_time_series` in `mtdnetwork/operation/mtd_ai_operation.py`) builds 5 + 7.
  - Tay's 8/3 evaluation builder is commented out at `mtd_ai_operation.py:~314-362`. It matches his evaluation code at commit `f13ed49` (l.240-283 there).
  - It reads state only, and makes one `random.random()` draw per decision, the same as the live builder.
- **Already in place:**
  - the movement arm's seam, `src/mtdsim/l3_simulation/movement/run.py:112-237` (`mtd_scheme="mtd_ai"`, `MTDAIConfig`);
  - the per-decision ledger (`decision_log`, with the source of each decision: greedy / random / forced);
  - the no-op waiting for the next tick (MTDAI-03).
- **Not wired:** the baseline arm. `data/results/ch5_defended/run_corpus.py::_baseline` builds the substrate's `MTDOperation`. For `mtd_ai` it needs `MTDAIOperation`, built the way `tools/mtd_ai_run.py:205` builds it.
- **The corpus to extend:** `data/results/ch5_defended/` (100 seeds, 200 s and 2 000 s, 6 arms, 10 conditions). `analyse.py` writes `numbers.json`; `disruption.py` writes `disruption_numbers.json`.
- **Appendix E** (`\label{app:mtdshield}`) is already drafted in the tex. Its §E.5 is a placeholder this work fills.

## Steps

1. **Input layout switch.**
   - Add Tay's 8/3 builder as a named layout: state `[host_compromise_ratio, exposed_endpoints, attack_path_exposure, overall_asr_avg, roa, shortest_path_variability, risk, attack_type]`, time series `[mtd_freq, overall_mttc_avg, time_since_last_mtd]`.
   - Build it exactly as the commented block does; restore it, do not rewrite it. The live 5/7 stays the default.
   - Add `feature_layout` to `MTDAIConfig`.
   - On loading the weights, assert the input shapes match the layout.
   - Leave the decision loop alone: the single enqueue and the random forced deployment are the simulator's (Appendix E.3).
2. **Wire both arms.**
   - Add two conditions to `run_corpus.py::CONDITIONS`:
     - `mtdshield`: scheme `mtd_ai`, the four-mechanism pool (complete topology shuffle, IP shuffle, OS diversity, service diversity), the 8/3 layout, ε = 0, attacker sensitivity 1;
     - `random_four`: scheme `random` over the same four mechanisms.
   - Wire `mtd_ai` into `_baseline` via `MTDAIOperation`.
   - Record per run: the decision ledger's action shares, the forced share, `n_executed`.
3. **Gates, before any corpus run.**
   - The goldens re-run unchanged.
   - One seeded run per attacker at 200 s. Hand-trace the first ten decisions of the ledger (V1): inputs, chosen action, deployed mechanism.
   - Time one decision step, and time a whole run at 200 s.
4. **Run.**
   - 2 conditions × {200, 2 000 s} × 6 arms × 100 seeds = 2 400 runs, appended to the existing `runs.jsonl`. Seeds 0–99; the other pins as the corpus's.
   - **The input-definition check:** `mtdshield` at 200 s with the training builder's two slots (`attack_success_rate`, `overall_time_to_compromise`, from `mtd_ai_training.py` at `f13ed49`), 6 arms × 100 seeds.
5. **Analyse.**
   - Extend `analyse.py` and `disruption.py`; do not fork them. Regenerate `numbers.json` and `disruption_numbers.json`.
   - Before reading anything, write down the prediction and its falsifier (from the E6 handoff §5.6 step 5a) in the findings record. The prediction: a near-constant service-diversity selector, whose line tracks the service-layer line. The falsifier: a service-diversity share below 0.7, or a no-op share above 0.2, at 200 s.
6. **Floats.** Add MTDShield, and random over the four, as scheme columns or bars:
   - **§5.3.2:** `fig:eff-cross-arm` and `tab:eff-orderings` (`tools/ch5_effectiveness_figures.py --only fig56 / tab56`);
   - **§5.3.3:** `fig:eff-suppression-profiles` and `tab:eff-conditions` (`--only fig55 / tab55`);
   - **§5.3.1:** `fig:aio-adaptivity` (`tools/ch5_disruption_figure.py`). Its panel (c) is per mechanism. Add MTDShield as a scheme bar only if it reads; otherwise put the number in the findings record and ask Marc.
   - Labels: *MTDShield* and a short name for random over the four (propose one; Marc rules). Keep "preliminary" on everything. Rebuild the PDF.
7. **Record.**
   - Fill Appendix E.5: action shares per interval and attacker, the forced share, the input-definition check, whether the prediction held.
   - Findings go to `docs/implementation/pipeline/ogasp/ch5_s54_effectiveness_findings.md` (or a sibling).
   - Update `FLOATS.md`.

## Validation gate

- The shape assert passes, and the goldens are unchanged.
- The ledger shows greedy decisions (source `greedy`), not random ones.
- 2 400 + 600 runs complete, with zero errors in `run.log`.
- `numbers.json` carries both new conditions for every arm and both intervals.
- The three floats are regenerated with the two columns.
- The PDF builds with no errors and no undefined references.
- Appendix E.5 is populated, and the prediction's outcome is stated.

## Hard constraints

- **No training, no rescaling, no repairs** to the agent (Appendix E.4 lists what is left as found).
- **No change to the simulation** outside the layout option. The 5/7 path and every other scheme must be bit-identical (goldens).
- **Determinism:** shared seeds. The arms are independent, not paired (D-29).
- **Concurrent sessions edit `dissertation.tex` and the ch5 generators** (Tables 5.3 and 5.4 were reworked 2026-09-25). Re-read before editing, and commit only your own hunks.
- **Git:** branch, local commits, never push. `runs.jsonl` stays gitignored.

## Reading list

- `docs/handoffs/2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md` §5.1, §5.6 (the build; the prediction; why the inputs are not rescaled).
- `mtdnetwork/operation/mtd_ai_operation.py` (the loop, and the commented 8/3 block); `mtdnetwork/mtdai/mtd_ai.py`.
- `tools/mtd_ai_run.py` (how `MTDAIOperation` is built; the ledger).
- `data/results/ch5_defended/run_corpus.py`, `analyse.py`, `disruption.py`.
- `docs/implementation/pipeline/ogasp/mtd_ai_forensics.md` §2–§4 (what the release is).

## Out of scope

- The six-interval sweep and the 1 000-seed run (the E6 handoff).
- The headline line chart's redesign (E6 handoff §5.4; Q8–Q10).
- Retraining, or any interval-aware variant.
- The §5.1 sentence and Table 5.1 rows (staged in the tex, applied when the 1 000-seed corpus lands).

## Open for Marc

- **Q7:** the random-over-four condition is run here because it is cheap. It stays in the floats only if Marc keeps it.
- **The forced deployment:** the simulator's random draw is kept (recommended); Tay's release forced complete topology shuffle.
- **The licence:** Tay's repo has no licence file (for the Appendix E note; ask Jin).
