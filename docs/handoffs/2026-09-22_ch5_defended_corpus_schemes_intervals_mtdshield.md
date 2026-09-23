---
status: open                  # executes register E6 (and E7's ranking base); supersedes the retired 2026-09-17 defended-runs plan and the 2026-09-15 unopposed plan — their owed items are carried in §4; Q1–Q5 owed, Q5 is "launch the smoke tonight"
created: 2026-09-22
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E6, §E7
companions: ../workflows/results_section_workflow.md (record → read → draw), 2026-09-22_ch5_two_phase_restructure.md (which floats read which cells), 2026-09-22_metrics_provenance_and_instrumentation.md (what the analyser computes)
---

# One new defended corpus: every deployment strategy including MTDShield as released, the deployment interval swept as a range, both attackers, at a thousand seeds

## State of play

**The ruling (E6, E7).** Load the other execution schemes; run Tay's selector as released ("no AI versus AI"; V3: no retraining); sweep the interval as a range in steps rather than 200 s and 2 000 s; the body carries a layer-based aggregation of the change in the success metric against interval, per-mechanism and per-profile panels go to an appendix; the prior evaluations are run, not quoted; rankings are based on the APT attacker model. The periodic timing configuration stands; the simultaneous scheme stays out (Marc's removal, accepted).

**The corpus that exists** (`data/results/ch5_defended/`, 2026-09-17): 30 200 runs — 10 conditions (no defence; seven singles; random and alternative over the seven) × {200, 2 000 s} × 6 arms × 100 seeds, plus the lineage (opportunistic-objective), regime (exponential at 200 s) and verdict-blind arms — in about 40 minutes on seven workers (≈ 12.6 runs/s; 0.12–1.2 s per run, network-layer singles at 200 s the slowest). `run_corpus.py` builds the jobs; `analyse.py` writes `numbers.json`; the generators read it. The no-defence cells are shared with `ch5_s531_unopposed/` bit for bit.

**The seam already takes MTDShield.** `src/mtdsim/l3_simulation/movement/run.py:112-237`: `mtd_scheme="mtd_ai"` with an `MTDAIConfig(main_network=...)`; the driver `tools/mtd_ai_run.py` (greedy ε = 0 by default — Tay's own harness left ε = 1.0, so every published MTDShield figure characterises a random selector, `mtd_ai_forensics.md` §2). Trained heads sit under `mtdsim-weights-archive/*.h5`; which head is canonical is MTDAI-02's disposition (`mtd_ai_cost_calibration.md` §1: the live 5/6 head). MTDShield selects from the lineage's four mechanisms plus no-op (Tay p.14), not the seven — a declared difference, not a defect.

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

## Rulings owed (Marc)

- **Q1** the interval levels (six proposed).
- **Q2** MTDShield: the head, ε = 0, and whether it runs at every interval or two.
- **Q3** drop the exponential timing arm (recommended).
- **Q4** drop the opportunistic-objective lineage arm (recommended; §5.3.3 dissolves).
- **Q5** launch the 100-seed smoke tonight, before Q1–Q4 are all ruled — the smoke is cheap and the cell set is a superset.

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

The figures' design (restructure and figure handoffs); the metric definitions (metrics handoff); any MTD optimised against the APT attacker (declined, E1).
