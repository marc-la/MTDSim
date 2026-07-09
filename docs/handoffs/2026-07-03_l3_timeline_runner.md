---
status: open
created: 2026-07-03
updated: 2026-07-09
---

# Build the standalone timeline runner — a seeded single-token walk over the weighted nets that emits timed attacker-state sequences (the v1 net-execution artefact)

> **Both upstream dependencies have SHIPPED — this handoff is unblocked.**
> Weights + the aggregate net: the five `data/ogasp/*_structural.json`
> (weighted-nets handoff, landed and deleted; surviving docs =
> [`../../data/ogasp/README.md`](../../data/ogasp/README.md)). Per-state dwell:
> [`../../data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json)
> (shipped 2026-07-09, **v0 uncalibrated**). Its output schema is the input contract for
> [`./2026-07-03_l3_replay_attacker.md`](./2026-07-03_l3_replay_attacker.md)
> and a fixed point for
> [`./2026-07-03_l3_binding_scoping.md`](./2026-07-03_l3_binding_scoping.md).
>
> This is the agreed **v1 execution model** (supervisor decision D2): run the
> Petri net **independently** of the simulator; a **single token** moves
> through the net; record the state at each node; each state consumes its
> duration; output a cumulative timeline of attacker states that is then fed
> into MTDSim. It also delivers D1's second half — "examine the attack
> behaviour based on the petri net generated" — without touching the
> simulator. The closed-form CTMC solve of the deleted
> `2026-06-18_l3_ogasp_petri_implementation.md` is retired to the deferred
> register; Monte-Carlo over this runner is the v1 way the nets are examined.

## State of play

- **Both inputs are on disk (2026-07-09):** five nets (four classes + aggregate)
  with per-transition flow-proportion weights, and the duration catalogue
  (`data/ogasp/tactic_durations.json`, v0). Build code and net
  I/O live at [`../../src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri).
- **Weight-variant fact the run matrix must name:** each net carries **two
  corpus variants** — `operator_dedup` (primary, n = 29) and `raw` (n = 38,
  robustness) — per [`../../data/ogasp/README.md`](../../data/ogasp/README.md).
  The runner's weighted policy reads `operator_dedup` as primary; `raw` is a
  cheap extra matrix arm (or defer it — record which).

### Catalogue facts the runner binds to (shipped after this handoff was written)

- **Shape:** `{meta, anchors, tactics}` — one entry per place-union tactic with
  `group / anchor / relative_multiplier / duration_s / tier / not_tuned /
  sweep_range / source / justification`. Units: **simulated seconds on the
  `env.timeout` clock**. Central dwells: scan-shaped 35, exploit-shaped 4.5,
  stealth-low-and-slow 45, objective-execution 36, prep-off-network 0.
- **Sweep arithmetic (easy to get wrong):** `sweep_range` is a band on
  `relative_multiplier` **in group-anchor units**, bracketing the central
  multiplier — the extreme dwell is `anchors[g].duration_s × sweep_bound`,
  **not** `duration_s × sweep_bound`. (E.g. execution: central ×0.5 → 22.5 s;
  sweep [0.1, 2.0] → extremes 4.5 s and 90 s.) See `meta.sweep_range_units`.
- **`resource-development` dwells 0 s** with a degenerate sweep [0, 0]; its
  profile §5 licenses a token nominal transit *only if the runner needs the
  place visibly traversed* — a runner decision to make and record.
- **The runner is the calibration instrument, not just infrastructure.** The
  catalogue lifecycle is: profiles → v0 (declared priors) → **this runner** →
  calibrate the two tuned anchors (stealth, objective) within their sweep
  ranges against macro milestones → freeze v1. Calibration discipline (the-bar
  note, anti-circularity rules): tune **group anchors only** (never Tier-1),
  calibrate on one observable and **hold one out** — the designated held-out
  milestone is **access→exfiltration** (Sophos AAR ~73–79 h; so named in the
  catalogue's exfiltration entry); the calibration targets are the collection
  (Bromiley ~64% collect+exfil ≤ 5 h) and impact (encryption ~6 min–2 h)
  shapes. Shape-not-scale throughout: match orderings/ratios, never absolute
  hours.
- **Consistency constraint:** the profiles' §5 stay the single source of truth;
  the catalogue and dissertation.tex §3.1 Tables 3.1–3.2 must agree with them.
  v1 calibration moves *anchor values* (not multipliers), so Table 3.2 should
  survive — but check §3.1's worked-example prose in the same commit that
  freezes v1. The per-tactic provenance rows
  ([`../specs/provenance.md`](../specs/provenance.md) § L3 state-duration
  catalogue) **await Marc's approval — do not freeze v1 before that approval**.
- **Test scaffolding to reuse:** `tests/l3_simulation/test_durations.py` shows
  the conventions — `OGASP_DIR` from `mtdsim.l3_simulation.petri.render`,
  catalogue/nets loaded as plain JSON, repo-root `conftest.py` adds `src/`.
  The runner's determinism/no-synthesis tests sit beside it.
- **Entry-point facts that shape the runner** (from
  [`../../data/ogasp/README.md`](../../data/ogasp/README.md)): recon reaches
  initial-access in `pure_steal` / `pure_impediment` only (one thin bridge
  edge each); in `double_extortion` / `infrastructure_setup` recon is an
  island. D8 says test **both** entries — so the recon-seeded arm exists only
  where bridged; the islanded classes record "recon arm impossible on
  observed-only base" (the prefix-bridge overlay stays deferred).
- **Objective/termination facts:** objective tactics are exfiltration
  (`pure_steal`), impact (`pure_impediment`), impact **and** exfiltration
  (`double_extortion` — a single token occupies one place, so "both achieved"
  must be a *visited-set* condition, not a marking condition), and
  `infrastructure_setup` has no objective tactic (absorb on C2-established or
  a dwell cap, per the L3a design). The aggregate net needs a declared
  objective set (union of the four; record the choice).
- Nothing runner-shaped exists. SNAKES has no stochastic simulation engine —
  the walk is plain Python over the committed JSONs (weights + durations);
  SNAKES is only needed if the net objects are re-used for legality checks.

## Recommended approach

**1 — The walk.** Seeded RNG (one seed per run, logged). From the entry
place, repeatedly: dwell for the current tactic's catalogue duration, then
choose the next transition from the current place's out-distribution
(**weighted** policy = the W-A weights; **uniform** policy = the structural
floor, kept as a sensitivity arm). Track the **visited set** alongside the
token position. Terminate on: objective condition met (visited-set covers the
class objective set), or a declared step/dwell cap for non-absorbing walks
(record which). Dead-end places (no out-transitions, non-objective) terminate
the run as `stalled` — a legitimate, recorded outcome of the envelope, not an
error.

**2 — The artefact + schema (the contract downstream binds to).** One JSONL
record per run:
`{run_id, seed, profile, entry, policy, duration_variant, outcome
(objective|cap|stalled), sequence: [{tactic, t_enter, dwell, t_exit,
transition_fired (a→b), backing_flow_ids}]}` — cumulative times exactly as
minuted ("node 1 = 5 s, node 2 = 10 s → timeline 5 s, 15 s, …"). Commit the
**schema document** (and a small committed example); the bulk timelines are
regenerable outputs and stay gitignored alongside the experiment-output
convention. The schema is versioned — the replay attacker pins to it.

**3 — The run matrix.** N seeded runs (N ≥ 100; cheap) per
{5 profiles} × {entry: initial-access always; recon where bridged} ×
{policy: weighted, uniform} × {durations: catalogue central values; the sweep
exercised at the extremes only, computed **in anchor units** per the sweep
arithmetic above — full sensitivity is deferred, D10}. Weight variant:
`operator_dedup` primary (`raw` as a robustness arm or an explicit deferral).
Profile-all-up-front per the minutes: generate the timeline library first,
feed the simulator later.

**4 — The behavioural verification report (light).** Summary statistics per
cell — time-to-objective distribution, outcome mix, sequence length, per-tactic
occupancy — and the class-vs-aggregate comparison on those statistics (the
behavioural half of "do the four profiles differ"; the structural half lives
in the weighting handoff's divergence report). Keep it to summary stats +
one verdict paragraph: the full aggregated variation analysis is **deferred
backlog** (D10). This report is the natural body of the pre-semester progress
update to Dr Hong.

*Alternatives considered:* running the token game inside SNAKES's `simul()`
(no stochastic support — rejected); event-driven co-simulation with SimPy now
(explicitly deferred by D2 — the two-way link is the end goal, not v1);
multiple concurrent tokens (open question, closed as single-token for v1 by
the minutes; the multi-token ↔ concurrent-action-set question returns with
the two-way integration).

## Strategic note (2026-07-07 examiner review — ported from the retired state-durations handoff)

The profiles/catalogue *defend* the thesis's finding but do not *produce* it.
The two objections that can actually fail a viva — **(V1)** the novel object
rests on declared dwell × declared reset fraction; **(V2)** "fidelity changes
the answer" is parameter noise unless the ranking-change *survives its own
sweep band and is distinct from the generic attacker's stable ranking* — are
discharged only by **running this runner's sweep arms + the discrimination
probe** ([`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
§10), not by more prose. That is why the sweep-extremes arm
of the matrix is not optional polish: it is the evidence V2 needs. The
per-modality reset split (capability/credential survives a mutation,
network-position is invalidated) is the strongest genuinely-owned, falsifiable
claim — it lands via the binding handoff, but this runner's timelines are what
make it exercisable. Build the working thing; resist further catalogue prose.

## Validation gate

Done when:
1. **Determinism:** same seed + profile + entry + policy + duration variant →
   byte-identical timeline (SIM-05 discipline extended to the runner; test).
2. **No-synthesis at run time:** every `transition_fired` exists in the
   committed net JSON (test); no transition is ever invented or skipped.
3. **Termination:** every run ends in a declared outcome; no unbounded walks
   (cap enforced and logged).
4. Timeline library generated for the full matrix; schema doc + example
   committed; bulk outputs gitignored.
5. The verification report exists: per-cell summary stats, class-vs-aggregate
   comparison, verdict paragraph on behavioural separation.
6. Recon-arm impossibility for the two islanded classes is recorded as a
   result (not silently skipped).
7. Tests under `tests/l3_simulation/` green.

## Hard constraints

- **The runner never touches MTDSim** — no imports from `mtdnetwork`; the
  coupling is the replay attacker's job (D2: independent execution).
- **Weights are the W-A flow proportions; durations are the catalogue** —
  nothing timing- or probability-shaped from `observation_count` directly
  ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f) as
  dispositioned by the governance handoff).
- **Envelope-not-actor phrasing** in the report: a timeline is one
  instantiation of the class envelope, never "an APT's campaign"; the
  time-to-objective statistic is an envelope statistic, and it is **not** the
  DES MTTC — name it distinctly (e.g. `net time-to-objective`) so the two are
  never conflated.
- Single token, v1 (minutes item 6). No GSPN firing semantics (D10).
- The prefix bridge (GAP Decision 6 Option B) stays deferred — observed-only
  nets.
- Branch hygiene, **never push without an explicit ask**, Australian English.

## Reading list

- [`../notes/2026-07-03_supervisor_meeting_l3_decisions.md`](../notes/2026-07-03_supervisor_meeting_l3_decisions.md)
  — the durable D1–D10 decision register (the governance handoff that used to
  hold this was deleted when its work shipped); D1/D2/D8/D10 are the coupling
  model this implements.
- [`../../data/ogasp/README.md`](../../data/ogasp/README.md) — entries,
  objectives, the prefix gap, per-class shapes, the two weight variants.
- The weighted JSONs + `tactic_durations.json` (both shipped) — the only
  runtime inputs; read the catalogue's `meta` block first (units, sweep
  arithmetic, reset-separation rule).
- [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md)
  — the calibration loop this runner enables (tiers, anti-circularity rules,
  held-out observable, shape-not-scale).
- [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(a)/(d)/(f)
  — the metric-identity discipline (net time-to-objective ≠ DES MTTC).
- [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
  §1/§3 — structure vs policy vs execution; the two readings of one net.

## Out of scope (explicitly)

- Feeding timelines into MTDSim (the replay attacker) and the tactic→action
  binding.
- Full sensitivity analysis over weights/durations (deferred, D10) — extremes
  only.
- The closed-form CTMC solve (retired to the deferred register).
- Adaptive / MTD-conditioned policies (Jalowski beacon — deferred with the
  two-way integration).
- Corpus expansion; the prefix bridge; multi-token concurrency.
