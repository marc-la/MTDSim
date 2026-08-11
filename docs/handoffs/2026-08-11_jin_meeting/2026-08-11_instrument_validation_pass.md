---
status: open
created: 2026-08-11
---

# Execute V1 + V4 — hand-traced validation of every presented instrument, and the detectability re-take at steady-state scale

## State of play

The 11-Aug supervisor meeting ruled every presented criterion figure
*preliminary* until hand-validated
([`../../implementation/pipeline/ogasp/supervisor_decision_register.md`](../../implementation/pipeline/ogasp/supervisor_decision_register.md)
§V1), and fixed the protocol: a network small enough to trace manually (four
or five nodes), the metric calculated by hand, checked for sense, then scaled.
The figures this covers: the attack-profile divergence (8–24 % JSD between
profiles), predictability (movement 0.33–0.57; the baseline pin is under
rework in its own handoff), and the detectability band. V4 additionally rules
the detectability run protocol: the presented 10-run band is under-powered,
the early spike is the initial transient and not a finding, and the standard
is steady-state reporting at on the order of a few thousand runs per plotted
point — raw data kept and appended across batches, averaged per point. The
axis-6 and axis-7 instruments do not exist yet and are out of scope here.
This pass gates the methodology draft: no instrument figure is quotable until
it clears.

## Recommended approach

Per instrument, in this order (cheapest first, and predictability last so the
rework lands first):

1. **Divergence (axis 2).** Define a deterministic-seeded 4–5-node
   configuration; run the profile pair; recompute the JSD by hand from the
   recorded distributions; compare. The meeting also asked for a presentation
   rework of the divergence figure (accepted-in-substance item in the V-trail
   preamble) — ride it along here.
2. **Detectability (axis 5).** Hand-trace the decaying exposure level over a
   short trace first (the increment/decay arithmetic is checkable by hand);
   then the V4 re-take: batch the runs with raw data appended, declare the
   convergence / steady-state window rule *before* reading the curve, re-plot
   at scale. The pre-positioning outlier's dwell-poor explanation is stated
   with the plot, not smoothed away.
3. **Predictability (axis 3)** — after the rework handoff resolves the
   baseline pin: hand-trace both arms on the small network, confirm the
   movement figure's arithmetic.

Extend the trace tooling where it cannot show the needed events
([`../../implementation/trace_tool.md`](../../implementation/trace_tool.md) charter:
extend, don't print-debug). Record each check as hand-value vs computed-value
with a match or a diagnosed mismatch — a mismatch is escalated as a finding,
never patched silently, because the ruling's whole point is that a formula
error found late forces a redo of the evaluation.

Alternative considered: validating on the full-size network with spot-checked
traces. Rejected — the ruling specifies the manually-traceable network
precisely so the hand calculation is complete, not sampled.

## Validation gate

A per-instrument validation record (small-network config, hand calculation,
computed value, verdict) committed under `implementation/pipeline/ogasp/`; the
detectability figure re-taken at V4 scale with its declared steady-state
window; register §V1/§V4 annotated executed. Any mismatch surfaced to Marc
with the diagnosis.

## Hard constraints

- Determinism / SIM-05 — the small-network runs must be seed-reproducible.
- Uniform filter thresholds across profiles in any comparison figure;
  per-instance tuning needs justification.
- Diagnostic visualisation carries no accentuation (no arrows / highlights);
  reserve that for dissertation figures.
- No substrate changes (S2 freeze). The formulas being validated are frozen
  during validation — a formula found wrong is a finding for Marc, not an
  in-session fix.
- Branch / commit / never-push rules per
  [`../../workflows/session_workflow.md`](../../workflows/session_workflow.md).

## Reading list

- [`../../implementation/pipeline/ogasp/supervisor_decision_register.md`](../../implementation/pipeline/ogasp/supervisor_decision_register.md) — §V1, §V4
- [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md) — the axes each instrument serves
- [`../../implementation/pipeline/ogasp/predictability.md`](../../implementation/pipeline/ogasp/predictability.md) — banner + construction
- [`../../implementation/pipeline/ogasp/stealth_exposure_metric.md`](../../implementation/pipeline/ogasp/stealth_exposure_metric.md) (and `stealth_spacing_diagnostic.md`) — the detectability reader's declared parameters
- [`../../implementation/trace_tool.md`](../../implementation/trace_tool.md) — the tracers this pass leans on

## Out of scope (explicitly)

Building the axis-6 / axis-7 instruments; any badge move; re-running
experiment 1/2 cells; repairing formulas found wrong (that is a disposition).
