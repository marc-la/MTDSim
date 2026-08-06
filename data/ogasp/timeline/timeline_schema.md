# `ogasp-timeline/v1` — the timeline-runner artefact contract

The output schema of the standalone timeline runner
([`src/mtdsim/l3_simulation/timeline/`](../../../src/mtdsim/l3_simulation/timeline)),
the v1 net-execution artefact under supervisor decision D2: the Petri net
runs **independently** of the simulator; a **single token** walks the
committed weighted net; each state consumes its catalogue dwell; the output
is a cumulative timeline of attacker states that the replay attacker later
feeds into MTDSim. This document is the contract downstream binds to — the
replay attacker pins to the schema version; any field or semantics change
bumps it.

- **Inputs (the only ones):** the five committed
  [`../petri/<profile>_structural.json`](../petri/README.md) nets (shape +
  W-A weights) and [`../tactic_durations.json`](../tactic_durations.json)
  (v0 per-state dwell).
  The runner never re-derives the nets, never imports `mtdnetwork`, and
  never fires a transition absent from the committed JSONs (the
  no-synthesis invariant, tested).
- **Units:** simulated seconds on the `env.timeout` clock (the catalogue's
  units). Dwells are the **v0 uncalibrated** catalogue — absolute values are
  shape-not-scale placeholders; only orderings/ratios carry meaning until v1
  calibration freezes.
- **Naming discipline:** the time statistic is the **net
  time-to-objective**, an envelope statistic over one instantiation of a
  class envelope. It is **not** the DES MTTC and is never comparable to it
  ([`docs/implementation/metrics_semantics.md`](../../../docs/implementation/metrics_semantics.md)
  §(a)/(d)). A timeline is never "an APT's campaign".

## Regenerate

```sh
PYTHONPATH=src python -m mtdsim.l3_simulation.timeline   # library + example + report + _viz/ figures
PYTHONPATH=src python -m pytest tests/l3_simulation/test_timeline.py
```

Bulk timelines land under the gitignored `_timelines/` (one JSONL per
run-matrix cell + `manifest.json`), and the awareness figures under the
gitignored `_viz/` (regenerable, diagnostic-quality); the committed artefacts
are this contract, [`timeline_example.jsonl`](timeline_example.jsonl) (the
shortest record of each outcome kind) and
[`timeline_report.md`](timeline_report.md) / `.json` (the behavioural
verification report). The library and report are deterministic — rerunning
reproduces every byte; there is no wall-clock anywhere.

## Record schema (one JSON object per line)

| Field | Type | Semantics |
|---|---|---|
| `schema` | str | `"ogasp-timeline/v1"` — the version downstream pins to |
| `run_id` | str | `<profile>--<entry>--<arm>--<duration_variant>--<index>`; unique across the library |
| `seed` | int | `int.from_bytes(sha256(run_id)[:8], 'big')` — the run's whole RNG stream; (seed, cell) fixes the timeline byte-for-byte. **Content-addressed on `run_id`, which embeds the profile name — so renaming a profile re-seeds every run in that profile's cells** (see *Re-seeded by the 2026-08-06 rename* below) |
| `profile` | str | one of the four GASP classes or `aggregate` (the null profile) |
| `entry` | str | seed place: `initial-access` always; `reconnaissance` only where the prefix gap is bridged (D8) |
| `policy` | str | `weighted` (samples the W-A out-distribution; only weight > 0 transitions fireable) or `uniform` (the structural floor: uniform over *all* committed out-transitions, weights unread) |
| `weight_variant` | str\|null | `operator_dedup` (primary, n = 29) or `raw` (n = 38, robustness) for `weighted`; `null` for `uniform` |
| `duration_variant` | str | `central` (catalogue `duration_s`), `sweep_low` / `sweep_high` (the sweep exercised at the extremes only — full sensitivity deferred, D10) |
| `objective_rule` | str | `all` (class nets: visited set must cover every declared objective tactic — for `objective_exfiltration_impact` the both-achieved condition) or `any` (aggregate: first union objective ends the walk — recorded choice; the null envelope has no single operational objective) |
| `objective_tactics` | [str] | the profile's declared objective set (from the committed net report) |
| `outcome` | str | `objective` \| `cap` \| `stalled` — every run ends in a declared outcome |
| `stall_reason` | str\|null | `no_structural_out_transitions` (sink place) or `no_weight_supported_out_transitions` (out-transitions exist but none has weight > 0 under the active variant); `stalled` is a legitimate, recorded envelope outcome, not an error |
| `completed_objectives` | [str] | objective tactics in the visited set at termination (shows *which* objective ended an aggregate any-rule run, and partial completion on stalls/caps) |
| `objective_first_visit_s` | {str: float} | first-visit exit time per objective tactic visited |
| `net_time_to_objective_s` | float\|null | cumulative clock at objective completion (the completing state's dwell included); null unless `outcome == "objective"`. **Not the DES MTTC.** |
| `n_states` | int | states entered (= `len(sequence)`); capped at 128 |
| `total_duration_s` | float | the walk's final cumulative clock |
| `sequence` | [state] | the timeline, in order; cumulative times exactly as minuted ("node 1 = 5 s, node 2 = 10 s → timeline 5 s, 15 s, …") |

Per state in `sequence`:

| Field | Type | Semantics |
|---|---|---|
| `tactic` | str | the place occupied (an ATT&CK tactic) |
| `t_enter_s` | float | cumulative clock on entering (0.0 for the seeded first state) |
| `dwell_s` | float | the catalogue dwell under the active duration variant |
| `t_exit_s` | float | `t_enter_s + dwell_s`; equals the next state's `t_enter_s` |
| `transition_fired` | str\|null | the committed transition name (`a__to__b`) that produced this state; null for the seeded first state; always present in the profile's committed net (no-synthesis) |
| `backing_flow_ids` | [str] | the fired transition's backing attack flows under the active weight variant (provenance, D9). The uniform arm reports the `operator_dedup` ids — possibly empty for a weight-unsupported transition the structural floor traversed (thinness left visible) |

## Declared walk semantics (the runner decisions of record)

- **The walk:** from the entry place, repeatedly consume the current
  tactic's dwell, check the objective condition against the **visited set**
  (never a marking condition — a single token occupies one place), then
  fire one out-transition per the policy. Randomness is routing only;
  dwells are deterministic per duration variant.
- **Sweep arithmetic:** `sweep_range` is a band on `relative_multiplier`
  **in group-anchor units** — the extreme dwell is
  `anchors[group].duration_s × sweep_bound`, never `duration_s ×
  sweep_bound` (catalogue `meta.sweep_range_units`; execution: central
  ×0.5 → 22.5 s, sweep [0.1, 2.0] → extremes 4.5 s and 90 s).
- **`resource-development` dwells 0 s in every variant** (degenerate sweep
  [0, 0]). The token still traverses the place visibly — the zero-dwell
  state appears in `sequence` — so the profile §5 licence for a token
  nominal transit is **not** taken up (recorded runner decision).
- **Step cap 128** states per walk — generous against the nets' diameter
  (longest committed entry→objective simple path: 15 places), so `cap`
  signals genuine wandering. It also bounds walks through the zero-dwell
  place: steps, not time, are capped.
- **Run matrix:** {5 profiles} × {entries per D8: `initial-access` always,
  `reconnaissance` where bridged} × {`weighted-operator_dedup`,
  `weighted-raw`, `uniform`} × {3 duration variants} × 100 seeded runs
  = 72 cells / 7 200 runs. The recon arm on `objective_exfiltration_impact` and
  `objective_none_c2` is **impossible** on the observed-only base (the
  prefix gap; the inferred prefix bridge stays deferred — GAP Decision 6
  Option B) and is recorded as a result in the manifest and the report,
  not silently skipped.

## Boundaries

- Nothing timing- or probability-shaped derives from `observation_count`
  or any corpus frequency: weights are the W-A flow proportions, durations
  are the catalogue
  ([`docs/implementation/metrics_semantics.md`](../../../docs/implementation/metrics_semantics.md)
  §(f) as dispositioned).
- The runner is also the **calibration instrument**: the catalogue
  lifecycle (v0 → runner → calibrate the two tuned group anchors within
  their sweep ranges against macro milestones, holding out
  access→exfiltration → freeze v1) runs over this library. v1 calibration
  is a separate, approval-gated step — not part of this artefact.
- Feeding timelines into MTDSim (the replay attacker), the tactic→action
  binding, GSPN firing semantics, multi-token concurrency and the full
  sensitivity sweep are out of scope here (D2/D10 deferrals).

## Re-seeded by the 2026-08-06 rename

**The objective-tactic class rename re-seeded this entire library, and the
committed report's numbers moved with it.** This is a property of the seed
derivation rather than a behavioural change: seeds are content-addressed on
`run_id`, `run_id` embeds the profile name, so renaming `pure_steal` to
`objective_exfiltration` changes every seed in that profile's cells. The
mechanism is confirmed by the one profile whose name did **not** change —
`aggregate` reproduces bit-for-bit across the rename, while all four renamed
profiles re-drew. Nothing about the walk semantics, the nets, the weights or
the duration catalogue moved; 1 121 scalar values in
`timeline_report.json` did.

**One committed conclusion flipped, and the flip is itself the finding.**
`ordering_stable_across_sweep_extremes` was `false` and is now `true`. The old
report recorded the profile ranking by median net time-to-objective as unstable
across the sweep extremes solely because, at `sweep_high`, the residual class
and the aggregate profile sat 12.5 s apart — 459.0 s against 471.5 s, a 2.7 %
margin at 100 runs per cell. Under the new seeds the residual class draws
529.0 s and the pair no longer crosses. The honest reading is that the original
instability was never a structural property of the profiles: it was a near-tie
resolved by Monte-Carlo noise, and a re-seed was always going to be able to
settle it either way. **Neither the old `false` nor the new `true` should be
quoted as a finding about profile ordering** — the two profiles are not
separated at this sample size, and any claim that depends on their order needs
more runs or a stated confidence interval, not a re-run.

Recorded per Marc's ruling of 2026-08-06 (accept the re-seed, record the
fragility) rather than by pinning the seeds to the retired labels, which would
have frozen the old coinage into the seed derivation permanently.
