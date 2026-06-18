---
status: open
created: 2026-06-18
---

# Build the four GASP classes as a layered Petri-net substrate (D4 analytical + D2 cross-validator + D3 floor)

> The *why*, the literature, the four candidate encodings, the five-lens
> critique and the GO-CONDITIONAL verdict are in the feasibility study at
> [`../notes/2026-06-18_l3_petri_feasibility.md`](../notes/2026-06-18_l3_petri_feasibility.md).
> This handoff is the build plan that study justifies. **Read the study first —
> do not re-derive the design here.**

## State of play

- **Decided:** all four GASP classes; analytical CTMC evaluation is the primary
  payoff (so tractability is the binding constraint). Verdict: **GO-CONDITIONAL**.
- **The recommended substrate is layered, not one net:**
  - **D4** — one shared Stochastic Reward Net on the ≤15-tactic quotient of the
    shared GAP substrate; the four classes are four rate/reward vectors over one
    reachability graph. **Primary analytical deliverable.**
  - **D2** — the faithful per-flow workflow-net (GAP Decision 2), in its
    single-token reduced projection, as the **fidelity cross-validator**.
  - **D3** — per-technique single-token CTMC on a mechanical high-recurrence
    slice, as a **sanity floor** for `pure_steal` and `pure_impediment` only.
- **Nothing is built.** The 2026-05-02 SNAKES primer (on `feat/replay-viz`) is
  prior art only — its concepts are reusable, its code/numbers are stale (GAP
  v0.4, `edge.confidence`, co-occurrence edges that v0.5 dropped). Do not lift it.
- **Branch:** `feat/l3-ogasp-petri` (this work). The L3 pipeline pointer
  [`../../src/mtdsim/l3_simulation/`](../../src/mtdsim/l3_simulation) currently
  holds no code.
- **An independent adversarial pass is recoverable.** The design workflow's
  judge/critique/revise phases failed on a session limit; the script
  `.claude/wf_ogasp_petri.js` can be re-run with
  `resumeFromRunId: wf_26c7a45f-647` once the limit resets, to cross-check the
  §6 critique against an independent panel before committing to the build.

## Recommended approach — staged, with gates

**Stage 0 — Governance before numbers (go-conditions 1, 2, 4; Marc-driven).**
Do not quote a single MTTC until these land.
- Write the **structural-MTTC / notional-rate regime** into
  [`../specs/provenance.md`](../specs/provenance.md): the corpus cannot ground
  rates even ordinally (88 % of edges are `observation_count = 1`), so the
  baseline is **uniform rates with the MTTC read as a structural metric**
  (steps-to-absorption over the corpus-grounded topology); `observation_count`
  admitted at most as a cosmetic `1 / 2 / ≥3` tie-break (never normalised — it is
  *not* a transition probability per
  [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f)); a
  *timing* MTTC requires exogenous (Outkin-style) rates, declared and swept;
  every metric a sensitivity band. (study §6.2)
- Pre-register the **discrimination-as-input** framing (D4 output is sensitivity
  analysis, not prediction).
- Re-position **`architecture.md` §(f)/(i)/(j)** from "parallel-not-primary" to
  "explicit parallel analytical column," stating the second-substrate
  comparability boundary.

**Stage 1 — The base artefact: four *un-weighted structural* nets (the baseline,
GO-unconditional).** This is the deliverable the task names — "just the shape."
Build the ≤15 tactic-places over the all-class union; one transition per distinct
inter-tactic GAP edge; AND-join / OR-choice as immediate transitions; 1-safe
achieved-set marking; the shared `ABSORB` place + class-parameterised absorb
guard (objective-tactic for three classes; eviction / C2-established / max-dwell
for `infrastructure_setup`). **No rates, no rewards, no timing yet.** Ship the
structural analyses you get for free with no weighting: reachability (is each
class's objective reachable?), boundedness/safeness, deadlock-freedom, distinct
attack-path count, shortest/longest technique chain to objective, AND-join
synchronisation points. Every element traces to a GAP edge / GASP node
(no-synthesis check, mechanical).

**Stage 2 — Add the rates (the parameterisation layer) + closed-form solve.**
Layer timing onto the Stage-1 skeleton. **Rate source is a hierarchy (study §6.2),
NOT the corpus:** tier 1 = **uniform** (all `λ` equal → a *structural* MTTC,
steps-to-absorption; needs nothing, do this first); tier 2 = **substrate-sourced**
(each transition's rate = the MTDSim action duration its technique maps to, via
the technique→action bridge — `ATTACK_DURATION`/`MTD_DURATION`/`time_generator`;
the natural OGASP baseline, depends on the L3 mapping); tier 3 = exogenous
engagement data (optional). `observation_count` is **not** a rate. Add reward
vectors `r_c` for RoA/path-exposure; assemble four generators `Q_c` over the one
transient/absorbing partition; solve `τ_c = −Q_T,c⁻¹·1` (MTTC),
`(e^{Q_c T})_{M0,ABSORB}` (ASR), `Σ rᵢπᵢ` (SRN reward). Sweep the base rate; report
bands. **MTD-reset transition decision (Mendonça 2023 —
[`../extractions/mendonca2023.md`](../extractions/mendonca2023.md)):** the SDR
schedule is *periodic*, so a faithful reset is a **deterministic** transition → a
**DSPN** (no clean CTMC; TimeNET/Mercury). Start by approximating it as
exponential (clean CTMC + SNAKES/custom solve), *declare the approximation*; flag
DSPN as the fidelity upgrade. (study §6.3)

**Stage 3 — Fidelity cross-validation (go-condition 3; THE gate).** Build D2's
single-token reduced workflow-net on ≥ 1 class (start with `pure_impediment` —
it carries the Tesla three-input AND-golden, so it exercises the AND-synchronisation
D4 discards), and compare its MTTC to D4's analytical MTTC. Report the gap.

**Stage 4 — D3 sanity floor.** Mechanical highest-recurrence corridor
(`obs ≥ 2` spine → stated objective terminus) for `pure_steal` and
`pure_impediment`; closed-form MTTC should bracket D4's class MTTC.

**Stage 5 — Metric semantics + write-up.** Name the Petri-CTMC MTTC as its own
metric (not the DES MTTC — §6.3 of the study); report the four classes as
within-substrate sensitivity-robust orderings; surface the D4-vs-D2
abstraction-error gap as a finding.

*Alternatives considered and rejected (see study §5):* D2-as-primary (explodes
to ~10¹⁸ for `pure_steal` under faithful concurrency); D3-as-the-four-class-
answer (fails on `double_extortion` and `infrastructure_setup`); D1 (dominated
by D4 — same tactic-quotient, weaker F1 alignment, no SRN reward layer).

## Validation gate

The build is done when:
1. The four `Q_c` are assembled on one shared reachability set (~10³–10⁴ states),
   and `τ_c`, `ASR_c(T)`, reward are computed in **closed form** (no
   Monte-Carlo) for **all four** classes, with `infrastructure_setup` absorbing
   on its non-objective condition.
2. The net is verified **1-safe, bounded, deadlock-free, properly terminating**
   (so the CTMC is finite and absorption is well-defined) — a mechanical test.
3. **Stage-3 gate:** the D4-vs-D2 MTTC gap on the cross-validated class is
   **smaller than the inter-class MTTC deltas** D4 reports. If it is larger, the
   tactic-quotient is distorting the very quantity being compared → **stop**,
   record NO-GO-at-tactic-granularity, fall back to per-class hand-curated slices
   (study §8).
4. Every MTTC/ASR is reported as a **sensitivity band over `λ₀`**, and the class
   orderings are shown stable across the operator-deduplicated corpus (n = 29).
5. No transition exists that is not a GAP edge (no-synthesis check, mechanical);
   `observation_count` appears nowhere as a normalised probability.

## Hard constraints

- **No-synthesis invariant** ([`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)
  §(a), [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) §(a)): every
  place/transition traces to a GAP node/edge; no invented structure. Class
  memberships consumed unchanged from the audit CSV.
- **`observation_count` is not a rate, and cannot even ground an ordinal**
  ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f); study
  §6.2): 88 % of edges are `observation_count = 1`. Baseline = uniform/notional
  rates with a **structural MTTC** (steps-to-absorption); `observation_count` at
  most a cosmetic `1 / 2 / ≥3` tie-break, never sum-normalised. No absolute timing
  MTTC is claimed without exogenous, declared, swept rates.
- **Within-substrate comparability only** (§(d)): the Petri-CTMC MTTC is a second
  substrate's metric — not comparable in magnitude to the DES MTTC or to
  Zhang/Tay numbers. State it.
- **MTD stays exogenous** to the analytical net for the baseline (an exogenous
  competing detection/reset transition), per Jin's scoping of Petri-net to
  *behaviour capture* — the full MTD system stays in SimPy.
- **Tooling:** SNAKES has no CTMC solver / no stochastic `simul()` / no GSPN
  priority scheduling — budget custom `scipy.sparse` generator-assembly + matrix-
  exponential, or a PNML export to GreatSPN/Möbius. v0.5 data only
  ([`../../data/gap/gap_v0.5.json`](../../data/gap/gap_v0.5.json) + the four
  [`../../data/gasp/`](../../data/gasp/) JSONs); do **not** import from the
  primer's `mtdsim.attacker.gap` layout or `gap_v0.4_latest.json` (gone).
- **Determinism, branch hygiene, never-push** per
  [`../specs/session_workflow.md`](../specs/session_workflow.md); Australian
  English throughout.

## Reading list

- [`../notes/2026-06-18_l3_petri_feasibility.md`](../notes/2026-06-18_l3_petri_feasibility.md)
  — the study: design, critique, verdict (read in full first).
- [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) — the four classes,
  the `SubgraphView` boundary object, §(h) open question 4 (tractability).
- [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(a) (MTTC
  definition the Petri metric must *not* be conflated with) and §(f) (the
  not-a-Markov-chain prohibition that governs rates).
- [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) Decision 2 (the
  intended operator-preserving encoding D2 implements) + §(d) (edge metadata:
  `observation_count`, `occurrences[]` join/branch).
- [`../extractions/mendonca2023.md`](../extractions/mendonca2023.md) — the
  closest precedent (analytical DSPN comparison of time-based MTD); the
  DSPN-vs-CTMC choice (Stage 1) and the declare-and-sweep parameterisation
  stance (Stage 0).
- [`../../data/gasp/`](../../data/gasp/) — the four `gasp_<class>.json` and
  `classification.csv` (the build inputs); the 2026-05-02 primer notebook on
  `feat/replay-viz` for the SNAKES API + CTMC recipe (concepts only — code stale).

## Out of scope (explicitly)

- The full **faithful concurrent D2** net (it is simulation-only; only its
  reduced single-token projection is in scope, as a cross-validator).
- **MTD-system modelling inside the net** beyond one exogenous competing
  transition — the defender system stays in SimPy.
- The **L4 evaluation matrix** itself (MTD family × profile × interval) — that is
  downstream; this handoff delivers the analytical attacker substrate, not the
  experiment.
- **The recon → initial-access prefix bridge** (the inferred `source: inferred`
  overlay, GAP Decision 6 Option B). The base net is observed-only and
  structurally blind to the pre-intrusion prefix (study §4). Per Marc's intent,
  **build and inspect the observed-only base first**, then decide the bridge off
  what it shows — it is a *separate, provenance-tagged, literature-grounded*
  overlay surfaced via the `corpus+inferred` view, never merged into the
  canonical net. Anticipated, deferred — not a base-artefact step.
- **Editing the canonical specs** beyond the Stage-0 governance entries — the
  architecture decision-block changes are flagged in the study §9 for Marc to
  drive, not actioned here.
- IDS / detection features; retraining Tay's RL agent (both out of scope
  project-wide).
