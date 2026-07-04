---
status: open
created: 2026-07-03
---

# Weight the four L3a nets (flow-proportion, tactic level) and build the fifth aggregate profile as the null model — with a divergence-from-aggregate discrimination report

> **Depends on** [`./2026-07-03_l3_governance_meeting_decisions.md`](./2026-07-03_l3_governance_meeting_decisions.md)
> (the weighting regime must be dispositioned in
> [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f) before
> a normalised weight is committed anywhere). Runs in parallel with
> [`./2026-07-03_l3_state_durations.md`](./2026-07-03_l3_state_durations.md);
> both feed [`./2026-07-03_l3_timeline_runner.md`](./2026-07-03_l3_timeline_runner.md).
>
> **Supersedes** the deleted `2026-06-18_profile_discrimination_probe.md`
> (its Tier-0 structural-discriminator check is absorbed into the divergence
> report below; its Tier-1 phase-map simulation probe is obviated — the
> supervisor greenlit running with the four profiles, and the aggregate
> profile now serves the "do they differ" verification as a measured output
> rather than a go/no-go gate).

## State of play

- The four **un-weighted** structural tactic-place nets are shipped:
  [`../../data/ogasp/`](../../data/ogasp/) (JSON + structural reports), build
  code at [`../../src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri),
  tests at `tests/l3_simulation/`. Places = tactics; transitions = inter-tactic
  tactic-pairs, each tracing to ≥1 GASP technique-edge (the no-synthesis
  invariant); self-loops were dropped at build time.
- **Supervisor decisions this executes (register in the governance note):**
  D3 — edge weights = *proportion of attack flows leaving each node*, at tactic
  level; sparsity accepted as "the only quantitative evidence available".
  D9 — node-level thinness is fine given a coherent start→end path. Marc's
  aggregate-profile proposal (5th baseline/null net; profiles measured as
  divergence from it) is **confirmed** ("no harm in trying" — resolution
  recorded in
  [`../notes/2026-07-03_supervisor_meeting_l3_decisions.md`](../notes/2026-07-03_supervisor_meeting_l3_decisions.md))
  — it doubles as the discrimination verification.
- **Known tradeoff to record, not fix:** aggregating techniques → tactics is
  precisely what makes the weights groundable at this corpus size, and it
  **loses AND-gate/join structure** — that is the accepted mechanism, not a
  defect. State it in the report.
- Inputs: [`../../data/gap/gap_v0.5.json`](../../data/gap/gap_v0.5.json), the
  four [`../../data/gasp/`](../../data/gasp/) class JSONs +
  `classification.csv`. The corpus is ~38 flows raw, **29 operator-deduplicated**
  (the dedup discipline of [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md)
  §(g)); classes are unions of 5–19 flows.

## Recommended approach

**1 — Weight definition (record as a build decision).** Two candidates:

- **W-A (flow-proportion — recommended).** For transition `a→b` in class `c`:
  `w = |F_c(a→b)| / |F_c(a→·)|`, where `F_c(a→b)` = distinct flows in `c`
  contributing ≥1 technique-edge whose source tactic is `a` and target tactic
  is `b`, and the denominator counts flows contributing *any* out-edge from
  `a`. This is literally the minuted wording ("proportion of attack flows
  leaving each node") and is robust to one flow drawing many parallel
  technique-edges.
- **W-B (edge-count proportion).** Normalise summed `observation_count` over
  the technique-edges under each tactic-pair. Finer-grained, but double-counts
  multi-edge flows and leans on `observation_count` magnitudes the corpus
  cannot ground (88 % are 1) — the very thing §(f) warns about.

Take W-A. **Store the raw numerator/denominator beside every normalised
weight** so the thinness stays visible (D9/Hong: "looking thin is fine" — but
only if it *looks* thin). No smoothing; if a smoothing scheme is ever wanted,
that is a new declared decision, not a default.

**2 — Aggregate (null) profile.** Build a fifth net over the **union of all
flows** (the full GAP tactic-quotient), same construction and W-A weighting.
Compute it on the operator-deduplicated corpus (n = 29) as primary, raw
(n = 38) as a robustness column — record both. Same artefact shape:
`data/ogasp/aggregate_structural.json` + viz.

**3 — Weights onto the four class nets.** Extend the existing build
(`build.py`) rather than a parallel script; regenerate the four
`<class>_structural.json` with a `weights` layer per transition
(`{numerator, denominator, weight}` + the flow IDs backing the numerator, for
provenance). Per-place out-weights must sum to 1 (over retained, non-self-loop
transitions); document that in-tactic dwell is the duration catalogue's job,
not a self-loop weight.

**4 — Divergence-from-aggregate report (absorbs the old Tier-0 probe).** Per
class vs the aggregate: per-place out-distribution **Jensen–Shannon
divergence**; weighted structural discriminators (reachable set from each
entry, shortest/longest entry→objective chain, branching factor, distinct-path
count, sink/island structure); and a **shuffled-class-label null** (reassign
flows to classes at random, rebuild, recompute — does the observed divergence
exceed the null band?). One summary table + a short verdict paragraph: do the
four envelopes differ from the aggregate beyond the null, and where? This is
the structural half of the "do they differ" verification; the timeline runner
delivers the behavioural half.

*Alternatives considered:* weighting at technique level (rejected — the thin
corpus can't ground it; tactic aggregation is the point of D3); building the
aggregate as a simple average of the four class nets (rejected — classes
overlap in flows; build from the flow union so the null is corpus-grounded).

## Validation gate

Done when:
1. The five JSONs (four classes + aggregate) carry per-transition
   `{numerator, denominator, weight, backing flow IDs}`; per-place out-weights
   sum to 1 (mechanical test).
2. **No-synthesis holds:** every weighted transition still traces to ≥1 GASP
   technique-edge; no transition gained or lost relative to the shipped
   structural nets (diff test).
3. `observation_count` appears nowhere as a normalised quantity (assert in the
   build; W-A counts flows, not edge weights).
4. The aggregate net has a coherent entry→objective path (D9) and its
   dedup-vs-raw variant is recorded.
5. The divergence report exists (JSD table + discriminators + shuffled null +
   verdict paragraph) and is committed beside the data.
6. Tests under `tests/l3_simulation/` extended and green; viz regenerated
   (no accentuation — edges/cells speak for themselves; uniform thresholds
   across the five nets).

## Hard constraints

- **The §(f) disposition must exist first** — do not commit a normalised
  weight before the governance handoff lands the spec block.
- **No-synthesis invariant** ([`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)
  §(a), [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) §(a)):
  weighting adds metadata to existing transitions; it never invents structure.
- **Weights are workflow-recurrence, never efficacy or actor-likelihood** —
  carry the §(f) survivorship framing and the envelope-not-actor phrasing into
  the report.
- Class memberships consumed unchanged from
  [`../../data/gasp/classification.csv`](../../data/gasp/classification.csv).
- v0.5 data only; do not import from the stale 2026-05-02 primer layout.
- Deterministic builds; branch hygiene; **never push without an explicit
  ask**; Australian English.

## Reading list

- [`./2026-07-03_l3_governance_meeting_decisions.md`](./2026-07-03_l3_governance_meeting_decisions.md)
  — D3/D9 and the §(f) disposition this build executes.
- [`../../data/ogasp/README.md`](../../data/ogasp/README.md) + the four
  structural JSONs — the artefact being extended (note the prefix-gap finding;
  it constrains the entry-side discriminators).
- [`../../src/mtdsim/l3_simulation/petri/build.py`](../../src/mtdsim/l3_simulation/petri/build.py)
  — the build to extend, and its tests.
- [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f) — what
  a weight is allowed to mean.
- [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) §(g) — the
  existing (thin) L2 discrimination signal and the operator-dedup discipline
  the report follows.

## Out of scope (explicitly)

- Durations/timing (the `l3_state_durations` handoff) and any execution of the
  nets (the timeline runner).
- Smoothing, priors, or corpus expansion (open with supervisor; flagged in the
  governance note).
- The recon→initial-access inferred prefix bridge (GAP Decision 6 Option B) —
  still deferred; the weighted nets stay observed-only.
- Any MTDSim/substrate change.
