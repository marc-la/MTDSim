---
status: open
created: 2026-08-13
topic: "Validation triage — the contribution inventory organised on the capture/model/evaluate spine, with each item flagged by existing verification strength; the manual-review queue for Marc, ordered by claim-bearing weight"
---

# Validation triage — what was built, what is already verified, what needs Marc's eyes

**Goal (one line):** give the validation pass a map — every contribution
enumerated on the thesis spine, each carrying its existing verification
artefacts, so manual review spends itself on the items where a machine check
cannot substitute for a human one.

**The triage principle.** An item is *low-touch* when its correctness is held by
an oracle that would fail loudly if it broke: a golden stream, a bit-identity
ablation, a hand-worked unit expectation, a Marc ratification on record, or a
pre-registration that predates the output. An item is *manual-review* when its
correctness is a **semantic judgement** — a declared magnitude, a mapping
choice, a cross-arm comparability assumption — that no test can arbitrate,
or when it is a large AI-authored surface whose claims feed the criterion
badges. The suite currently collects **1,109 tests**; test counts below are
per-file `def test` counts as of today.

---

## 1. The contribution inventory, on the capture / model / evaluate spine

### Capture — CTI → structured campaign data (L0–L2)

| # | Contribution | Where | Existing verification |
|---|---|---|---|
| C1 | L0 CTI acquisition: Attack Flow corpus fetch, pinned ATT&CK STIX bundle | `src/mtdsim/l0_cti/` | pinned bundle = reproducible input |
| C2 | L1 GAP: lossless Attack-Flow-only attack graph — parser, schema, aggregation, views | `src/mtdsim/l1_construction/`; `gap_schema.md` | `tests/gap/`; deterministic rebuild from pinned inputs |
| C3 | L2 GASP: four objective classes, audit-traced to analyst-stated objectives; dedup; selector | `src/mtdsim/l2_subgraph/`; `gasp_schema.md`; `data/gasp/metadata_audit.csv` | `tests/l2_subgraph/`; JSD discrimination check (§g); per-flow citations ratified |

### Model — the movement attacker (L3)

| # | Contribution | Where | Existing verification |
|---|---|---|---|
| M1 | Petri-net construction: class nets from GASP, flow-proportion transition weights, synthetic pre-intrusion overlay, divergence/analysis/render | `l3_simulation/petri/` (`build`, `weights`, `synthetic_overlay`) | `test_petri` (17), `test_weights` (13); `weight_sensitivity_study.md`; `synthetic_overlay.md` |
| M2 | Movement runtime: `RoutingNet`, the `MovementAttacker` driver walk, attacker-state seam, per-tactic exponential dwell (S3/S3-R — movement layer is the profiled arm's sole timekeeper) | `movement/net.py`, `attacker.py`, `state.py`, `timing.py`; `data/ogasp/tactic_durations.json` | `runtime_verification.md` (per-proposition cross-examination, P1–P7); `test_seam_invariants`, `test_movement_*` (net 12, state 11, timing 20, attacker 6, driver regressions 4, integration 7, smoke 7) |
| M3 | Outcome overlay: verdict-conditioned success/failure weight-set switch | `controller/outcome.py`; `data/ogasp/controller/outcome_rules.json` | `test_controller_outcome` (8); reproducible generator, 0/75 reproduction; **values provisional** (see §2) |
| M4 | Controller: tactic→verb map v1 (total) and `v2_partial` (S4, seven dwell-only rows), verdict adapter, rules | `controller/`; `controller.md`, `controller_mapping_v2.md` | v2 ratified row-by-row by Marc 2026-07-28; `test_controller*` (18+21+9+8); version-pinned selectable data |
| M5 | Modulators: utility (axis 6, λ), learning + readiness re-key (axis 7), compound exploit learning (axis 7, substrate-hosted, default-off), each declared/banded/swept | `movement/utility.py`, `learning.py`, `learning_readiness.py`; exploit learner in the substrate (`mtdnetwork/component/adversary.py`, `operation/attack_operation.py`, `component/services.py`, `component/network.py`) with movement wiring in `movement/run.py` and drivers in `tools/exploit_learning_{sweep,analyse}.py` | bit-identity ablations at the null point (λ=0, zero capability, default-off safety properties proven); pre-registered sweeps (1,800 / 2,400 / 4,600 / 800 / 4,200 runs); `test_movement_utility` (18), `test_movement_learning` (20), `test_movement_learning_readiness` (25), `test_exploit_learning` (12), `test_verdict_blind_arm` (9) |
| M5a | The exploit-learning **yield ledger** (2026-08-13): read-only attribution of each learning-bought exploit success by probability mass at the roll site, split fresh-host vs re-compromise, plus concentration/conversion reads; produced the shipped null finding (gains absorbed on the learner's own terrain) | lazily-attached ledger in `adversary.py` + roll-site record in `attack_operation.py`; `movement/run.py`; `exploit_learning_yield_{prereg,findings}.md` | prereg committed before any output and the committed null branch fired; byte-identical records with vs without the ledger across λ ∈ {None, 0, 1, 2}; goldens, ATK-04 pins and movement/trace suites green |
| M6 | FSM-side overlays: succession, alignment (baseline-arm comparability structure) | `movement/succession.py` (572), `alignment.py` (706) | preregs + `test_movement_succession` (21), `test_movement_alignment` (20) |
| M7 | Substrate joins: MTD interrupt → state throw-back, attacker read surface discipline, MTD-AI wiring | driver + `mtdnetwork` seams | `runtime_verification.md`; `test_movement_mtd_ai_wiring` (8), `test_interrupt_channel_semantics`; boundary records (`attacker_read_surface.md`, `disruption_wiring.md`) |

### Evaluate — instrumentation, experiments, findings (L3/L4)

| # | Contribution | Where | Existing verification |
|---|---|---|---|
| E1 | The axis-measurement suite: coverage/depth/retention, path entropy, JSD divergence + split-half nulls, interrupt mixes, cost ledger, disruption ledger, disengagement frontier (PCE algebra) | `movement/measures.py` (2,619 lines); `measurement_suite.md` | `test_movement_measures` (96, hand-worked expectations + two seeded integration checks); per-measure blind spots recorded |
| E2 | Standalone instruments: predictability, plural preference, stealth exposure + spacing readers | `movement/exposure.py`; `predictability.md`, `plural_preference.md`, `stealth_*` records | pre-registered with kill criteria (several fired and are honoured); `test_movement_exposure` (25) |
| E3 | Experiments 1–2 and the modulator sweeps; findings records with pre-registrations throughout | `experiment_0{1,2}_findings.md` + prereg/findings pairs | conclusions committed before outputs; ten-seed interval discipline (`interval_report`) |
| E4 | Timeline + trace tooling (diagnostic, not claim-bearing) | `l3_simulation/timeline/`, `trace.py`; `mtdnetwork/trace.py` | `test_timeline` (12), `test_movement_trace` (8), `test_trace` |
| E5 | L4 evaluation layer — **placeholder only** (`l4_evaluation/__init__.py`); evaluation currently lives in E1–E3 | `src/mtdsim/l4_evaluation/` | nothing to validate yet; note it so the enumeration is honest |

### Substrate stewardship — the inherited simulator made evaluable

| # | Contribution | Where | Existing verification |
|---|---|---|---|
| S1 | Crash fix (R1–R3 silent integrity failure), C6 compromise-ratio fix, golden re-baseline, SIM-05 determinism | `mtdnetwork/`; `baseline/` | `test_crash_fix_regressions`, `test_mtd_golden_streams`, golden oracle + `BASELINE.md`/`CHANGELOG.md` |
| S2 | Intent spec (literature-only) + row-level conformance audit; metrics semantics (C7, ATK-04, comparability boundary); provenance of load-bearing constants | `mtdsim_intent_spec.md`, `intent_conformance_audit.md`, `metrics_semantics.md`, `provenance.md` | audit method (four-way classification, code locators); D-01..D-15 open dispositions are *known* open, not unvalidated |
| S3 | Boundary programme: read surface, write surfaces, disruption channels + wiring | four boundary records | `test_mtd_write_surfaces`, `test_action_layer_*` |

### Method — instruments that are themselves contributions

| # | Contribution | Where | Existing verification |
|---|---|---|---|
| X1 | The APT criterion instrument: axes fixed from literature before scoring, badge vocabulary, rows A/B appended pre-scoring | `apt_model_criterion.md` | anti-reverse-fit provenance is documented in-file; supervisor-directed (S6) |
| X2 | The supervisor decision register + V trail; pre-registration protocol; axis-instrumentation method | `supervisor_decision_register.md`, `axis_instrumentation_method.md` | process artefacts; validated by use |

---

## 2. The manual-review queue, ordered by claim-bearing weight

These are the items where validation is a judgement no oracle holds, or where
the AI-authored surface is large and feeds badges. Work top-down.

1. **The declared-value families (the weight parameterisation).** The row-A
   scorecard already concedes ≈ three-fifths of magnitudes are declared
   judgement. Re-walk each family against its generator and its band: the
   outcome-overlay success/failure weights (**mechanism certified, values
   explicitly provisional pending your greenlight** — `runtime_verification.md`
   preamble), `tactic_durations.json`, the `attacker_utility` benefit family
   (R2 double-penalty history), the learning magnitudes and decay, the exposure
   increments (order corpus-derived, magnitude declared). The dissertation must
   defend every one of these as a *declared* choice; the validation act is
   confirming each is generated, banded, swept, and carries a null in its band.
2. **The controller/verdict join semantics.** The mapping mechanics are tested
   and v2 is ratified; what deserves eyes is the *meaning* carried across the
   seam: what `verdict_of` collapses a substrate outcome into, what a blocked
   verb signifies, the interrupt→throw-back scope (M1), and the `v2_partial`
   dwell-only consequences (e.g. the objective band holding no verdict, capping
   `deepest_successful_stage` at 2). Read `controller.md` → `verdict.py` (66
   lines) → the P-verdicts in `runtime_verification.md` in one sitting.
3. **Cross-arm comparability adapters.** The single most dangerous surface:
   baseline-arm row adapters (`comparable_from_baseline` / `_movement`), the
   per-vulnerability vs per-invocation counting asymmetry (the 3.75× event
   inflation that inverted a pre-registered stealth prediction), the S3-R clock
   asymmetry ("time fields are movement-arm-only"), and the baseline's
   deduplicated-identity vs sampled-count progress measures. Every cross-arm
   figure in ch5/ch6 flows through these.
4. **`measures.py`, claim-bearing subset first.** 2,619 lines, 96 tests —
   review not line-by-line but measure-by-measure for the ones badges and
   findings cite: `path_entropy`, `profile_divergence` + split-half null,
   `deepest_successful_stage`, `foothold_retentions`, the disengagement algebra
   (`T(t) = t + (W − h(t))/r(t)` and `A(k)` censoring), and the disruption
   ledger's three known undercounts. Check each against its stated blind spot
   in `measurement_suite.md` §(b) — the blind-spot column is the review
   checklist.
5. **The stealth readers** (`exposure.py` + spacing diagnostic). The D4
   granularity confound is unresolved by record; the 2026-08-09 spacing claims
   (1.5–1.8× spacing, 45 % level reduction, the ablation attributing the margin
   to non-action tactics) will be quoted in prose — verify the statistic
   definitions in code match the record's sentences.
6. **The composition overlays**: `synthetic_overlay.py` (pre-intrusion
   structure into the nets) and the FSM-side `succession.py` / `alignment.py`.
   Tested and pre-registered, but they are joins between corpus structure and
   inherited FSM semantics — the classic convoluted-integration shape. Spot-walk
   one profile end-to-end with the movement tracer.

## 3. Flagged low-touch (spot-check only, don't re-derive)

- C2/C3 (GAP/GASP builders) — deterministic, schema-tested, audit ratified.
- S1 substrate fixes — golden-stream oracle; any regression fails loudly.
- M5 modulator *wiring* — the bit-identity-at-null ablations prove the
  mechanisms are cleanly separable; what needs review is their declared values
  (item 1 above), not their plumbing.
- M4 controller *mechanics* — ratified data + version pinning; item 2 covers
  the semantic half.
- E3 findings integrity — protected by pre-registration; the honoured kill
  criteria and declined badges are evidence the discipline held.
- E4 tooling — diagnostic only; validate opportunistically while using it for
  items 2 and 6.

## 4. Validation gate

Done when: (a) every declared-value family in item 1 has a recorded
Marc-greenlight (or a recorded reservation) — the outcome-overlay values being
the known outstanding one; (b) items 2–3 have been read end-to-end with any
divergence between code and record either fixed or logged as a disposition;
(c) the item-4 claim-bearing measures have each been checked against their
blind-spot row; (d) anything found is routed per the standing rule — bug vs
design choice classified against the intent spec before any fix.

## 5. Reading list for the picking-up session

1. `docs/implementation/pipeline/ogasp/runtime_verification.md` — the seam model and what is already certified.
2. `docs/implementation/pipeline/ogasp/measurement_suite.md` — per-measure definitions + blind spots (the checklist for item 4).
3. `docs/implementation/pipeline/ogasp/controller_mapping_v2.md` + `controller.md` — the join semantics (item 2).
4. `docs/implementation/apt_model_criterion.md` — which claims each surface carries (loaded every session anyway).
5. `docs/implementation/trace_tool.md` — the spot-walk instrument for items 2 and 6.
