---
status: review record (boundary review 3 of 3)
created: 2026-08-02
updated: 2026-08-02
topic: "The direct attacker/defender channels — inventory, executed truth table, realised traffic from recorded runs, and the class-vs-mechanism pricing question put to Marc (D-20..D-22)"
---

# The attacker/defender boundary — the six direct channels, verified and measured

**What this is.** The Part A record of boundary review 3
(`docs/handoffs/2026-08-02_boundary_attacker_defender_integration.md`): the
channels through which the defence reaches the attacker *without* passing
through network state, inventoried with locators, verified by **executing** the
deciding code rather than reading it, and quantified from the recorded run
data. It ends in three disposition requests (D-20..D-22 on the
[audit's](intent_conformance_audit.md) list); nothing was changed.

**The operating picture (Marc, 2026-08-02, brief 1).** One attacker model, in
the substrate, driven two ways: the native six-verb FSM, and the movement layer
driving the same verb cores through `step()`. Every claim below states its
reach under both driving modes. The S3-R seam's declines (supplied pricing,
driver-owned succession) are settled design, not candidates — the
indistinguishability brief's §1.2 precedent.

**Method.** Code read with locators (never from paper memory); the deciding
functions executed directly against stub collaborators (§c below — the real
`MTDOperation._interrupt_adversary` and
`AttackOperation.apply_mtd_interrupt_cost`, not reimplementations); integration
behaviour demonstrated with the two tracers at seed 42; realised traffic
extracted from the recorded experiment-2 and frontier data
(`data/results/expo02_ashen_lynx/runs.jsonl`,
`data/results/frontier_disruption/runs.jsonl` — no recorded experiment
re-run); exposure measured by a 50-run diagnostic of the **current** substrate
(profiles × 10 seeds, undefended, experiment 2's `v2_partial` mapping),
declared as such.

## (a) The six channels, with locators

| # | Channel | Locator | Keyed on | Reach: native arm | Reach: movement arm |
|---|---|---|---|---|---|
| 1 | The interrupt condition | `mtd_operation.py:211-258` | resource class × `curr_process` | yes | yes (`register_for_interrupts`, `attacker.py:313-320`) |
| 2 | The confusion penalty | `attack_operation.py:161-208` (`apply_mtd_interrupt_cost`) | nothing — flat draw | yes (`_handle_interrupt`) | yes (`_read_interrupt` → `_pay_interrupt_cost`, `attacker.py:520-562`) |
| 3 | Lost connection / cursor clear | `attack_operation.py:206-208` | resource class (network only) | yes | yes (same call) |
| 4 | Forced re-scan succession | `attack_operation.py:228-248` (`_handle_interrupt`) | resource class | yes | **no — by design**: the driver owns succession (S3-R; the carve's purpose) |
| 5 | The verdict's downstream consumers | `attacker.py:507-541` (interrupt-as-failure); `learning.py:197-216` and `learning_readiness.py:223-244` (belief decay ρ, phase-state severance); overlay routing | movement layer's declared families | n/a | yes — movement-only, all declared and swept |
| 6 | The unwired observation hook | `adversary.py:23` (`observed_changes`) | — | dead | dead (axis-8 exclusion, Marc 2026-07-28 — stays unwired) |

Channel 6 re-verified 2026-08-02: repo-wide, the attribute is written nowhere
and read nowhere (the only other occurrence is an attribute-name list in
`tests/l3_simulation/test_movement_smoke.py:142`).

One **attacker→defender** input completes the boundary's inventory and belongs
to channel 1 rather than beside it: the gate reads `adversary.curr_process` to
decide whether an application-class mutation interrupts. The movement driver
deliberately writes that signal — the verb is announced *before* its time is
spent (`attacker.py:400-414`; previously the gate judged a stale verb on 27 %
of application-layer decisions), and a dwell-only place announces the `DWELL`
sentinel (`attacker.py:118-128`), which the gate reads as interruptible. No
seventh defender→attacker channel was found in an adversarial pass over
`mtd/*`, the two operation files, and the movement/controller layers; the
defender-side statistics the attacker *could* reach through its network handle
are exactly the axis-8 surface, ruled out for the life of the project.

## (b) The truth table, executed

Verified by running the real gate and cost functions across the full grid
(scratchpad probe `gate_probe.py`, 2026-08-02; stub collaborators, real
methods). `curr_process` values are what each arm actually presents: the six
verbs (either arm) and `DWELL` (movement arm, dwell-only places; blocked
dispatches present their announced verb).

| `curr_process` | network | application | reserve |
|---|---|---|---|
| SCAN_HOST | INTERRUPT | — | — |
| ENUM_HOST | INTERRUPT | — | — |
| SCAN_PORT | INTERRUPT | INTERRUPT | — |
| SCAN_NEIGHBOR | INTERRUPT | — | — |
| EXPLOIT_VULN | INTERRUPT | INTERRUPT | — |
| BRUTE_FORCE | INTERRUPT | INTERRUPT | INTERRUPT |
| DWELL *(movement only)* | INTERRUPT | INTERRUPT | — |

What an interrupt then costs, executed on the same probe and confirmed in both
tracers:

- **Penalty (channel 2):** one `exponential_variates(PENALTY = 20, 0.5)` draw
  — measured 20.0–20.7 per interrupt in the probe, 20.49–20.52 mean per
  interrupt across every recorded (arm × mechanism) cell (§(d)). Identical for
  every mechanism, every class, both arms. Provenance **faithful** (Brown
  §V-A, Zhang §4.4.3; [`provenance.md`](provenance.md) row "MTD interrupt +
  confusion penalty"; single-charge pinned by
  `tests/test_action_layer_dispositions.py`).
- **Cursor clear (channel 3):** network class only — `curr_host_id = -1`,
  `curr_host = None`. Application and reserve clear nothing; the native arm's
  "service connection lost" is expressed as the forced SCAN_PORT restart
  (channel 4), which the movement arm by design does not receive — an
  application interrupt costs the movement attacker the penalty plus a failure
  verdict, and nothing structural.
- **Overlap absorption:** a second interrupt landing mid-penalty is absorbed,
  not stacked (probe: absorbed at t = 20.8 with no second draw). The native
  arm is structurally immune for the penalty window instead (its interrupted
  process is dead, and the gate guards on `is_alive`), so **neither arm ever
  pays twice** — but the *counter* semantics differ: the movement arm's
  absorbed hit increments `add_total_attack_interrupted` (the gate fired) while
  the native arm's never registers. Measured: movement `simultaneous` stats
  counter 127.3 vs 127.0 interrupt-bearing movement records per run (≈ 0.3
  absorbed counts/run); the native arm shows no such split. → D-22.
- **Succession (channel 4):** native only — network → SCAN_HOST, application →
  SCAN_PORT, reserve → EXPLOIT_VULN (the D-07 fix). Demonstrated in the
  substrate tracer at seed 42 (`--scheme single --mtd OSDiversity`:
  "restarting at SCAN_PORT"; `--mtd CompleteTopologyShuffle`: "restarting at
  SCAN_HOST"). The movement arm reads the interrupt as a failure verdict and
  routes (unified tracer, same seed: "VERDICT SCAN_HOST: failure — MTD
  interrupt reads as failure").

Live integration demonstrations (unified tracer, `aggregate`, `v2_partial`,
`--scheme simultaneous --seed 42`): an application-class interrupt landing on a
dwell-only place ("OSDiversity hit the attacker mid-DWELL", t = 80.2); a
network-class one likewise (t = 110.5); per-event penalties of ~20 each;
verdict block "127 step(s) interrupted by MTD (20 mid-verb, 107 mid-dwell),
each read as a failure verdict"; total confusion cost 2 605 t/u = 17 % of the
run's clock.

## (c) Realised traffic, from the recorded data

**Interrupts and penalty time per run** (experiment 2,
`expo02_ashen_lynx/runs.jsonl`, interval 200, 15 ks horizon; means):

| condition | baseline interrupts | movement interrupts | movement penalty total (t/u) | penalty / interrupt |
|---|--:|--:|--:|--:|
| complete_topology | 74.8 | 75.0 | 1 538 | 20.51 |
| ip_shuffle | 74.6 | 75.0 | 1 539 | 20.52 |
| os_diversity | 74.2 | 52.7 | 1 080 | 20.49 |
| service_diversity | 74.3 | 52.4 | 1 073 | 20.49 |
| alternative_multi | 73.8 | 64.5 | 1 322 | 20.50 |
| random_multi | 73.9 | 54.9 | 1 125 | 20.51 |
| simultaneous_multi | 149.2 | 127.0 | 2 606 | 20.51 |

(`mtd_penalty_total` is instrumented on the movement arm only; a baseline cell
of 0.0 is non-measurement, not immunity — the native arm's per-interrupt
penalty is visible in the tracer and pinned by the single-charge test.)

The class flattening is a **measured statement**: within a class the two
mechanisms' channel traffic is identical to the seed stream (75.0 = 75.0
network) or near-identical (52.7 vs 52.4 application), and the penalty per
interrupt is the same 20.5 in every cell. The between-class difference *is*
live and large on the movement arm — network-class conditions interrupt on
every trigger and clear the cursor; application-class ones interrupt on ~70 %
of triggers and clear nothing — and it is what separates the two effect-pairs
in the recorded outcome data (0.64/0.72 hosts vs 3.46/3.70, the
indistinguishability brief §1.3). In the learner arm (`movement_learn`),
`forgettings == interrupts` exactly in every cell (channel 5's ρ-decay fires
once per interrupt regardless of class or mechanism, as
`learning.py:197-216` declares).

**Scheduling as an implicit channel** (frontier data, per run at 200 s):
executions are 75.0 for every single-mechanism condition on both arms;
suspensions are **zero everywhere except the simultaneous scheme** (38.0/run,
both arms); per-mechanism trigger counts inside every multi scheme are
near-equal (simultaneous 37/37/38/38; alternative 19/19/19/18; random
18.1–20.7). At the recorded settings, no mechanism buys materially fewer
channel-1 events from priority ordering (`MTD_PRIORITY`, IS-SCH-06) or from
suspend/discard (IS-SCH-05, including its recorded batch-serialisation delta).
The scheduling layer flattens *across* mechanisms rather than differentiating
them — consistent with the class-level pricing model, and covered by the same
D-20 framing decision.

## (d) Interrupt exposure under movement driving — measured, and the brief's worry falsified

The brief asked what can interrupt the attacker during the 37–43 % of visits
that dispatch nothing. Answer, live-verified: **everything except the reserve
class** — the `DWELL` sentinel is deliberately exposed to both network and
application classes (§(b) table; "a dwell-only place does not become a
cost-free hiding spot from MTD", `attacker.py:118-128`). The immune time is
instead the **recon-verb share** of the clock: the tactics `v2_partial` maps
to SCAN_HOST / ENUM_HOST / SCAN_NEIGHBOR (reconnaissance, lateral-movement,
command-and-control).

Time-weighted exposure, 50-run diagnostic of the current substrate
(10 seeds × 5 profiles, `v2_partial`, S3 timing, undefended so no penalty time
perturbs the denominators):

| profile | recon-verb (app-immune) | attack-verb | BRUTE_FORCE share | dwell-only | **application-exposed** | network-exposed |
|---|--:|--:|--:|--:|--:|--:|
| pure_steal | 28.4 % | 20.9 % | 1.7 % | 50.8 % | **71.6 %** | 100 % |
| pure_impediment | 29.9 % | 20.8 % | 0.5 % | 49.4 % | **70.1 %** | 100 % |
| double_extortion | 16.8 % | 27.5 % | 0.2 % | 55.7 % | **83.2 %** | 100 % |
| infrastructure_setup | 42.7 % | 29.5 % | 2.1 % | 27.9 % | **57.3 %** | 100 % |
| aggregate | 26.3 % | 21.1 % | 1.2 % | 52.6 % | **73.7 %** | 100 % |

The recorded defended runs corroborate: application-class interrupt yield
52.7/75.0 ≈ 0.70 on the movement arm (aggregate) against ≈ 0.99 on the native
arm, whose clock is almost entirely EXPLOIT_VULN. The asymmetry the
comparative evaluation inherits is therefore: **application-class mechanisms
reach the native attacker ~99 % of the clock and the movement attacker
57–83 % (profile-dependent)**, because the profiled attacker genuinely spends
time in reconnaissance-shaped tactics the interrupt gate has always exempted
(IS-INT-05's documented exclusion), while the native attacker effectively
never does. This is the same gate applying the same documented semantics to a
different behavioural mix — a **mapping-owned pricing consequence, not a gate
change**, and it is put to Marc as mapping policy (D-21). The reserve class
reaches the movement attacker 0.2–2.1 % of the clock (and the native arm
comparably little); with UserShuffle latent this is a dead channel in
practice (D-07's record stands; nothing new to rule).

## (e) Classification against the intent spec (§c procedure)

| Behaviour | IS row(s) | Verdict |
|---|---|---|
| Network-class unconditional interrupt + re-discovery | IS-INT-01/04, IS-ARC-01 ("interrupt attack actions" edge) | **CONFORMS** (audit §f rows stand) |
| Application-class verb-gated interrupt + Phase-1 restart | IS-INT-02/05 (Zhang Fig 7 exact, audit §j) | **CONFORMS** |
| Reserve class interrupts only BRUTE_FORCE | IS-INT-03 | **CONFORMS under the D-07 disposition** (Marc, 2026-07-29); latent |
| Flat per-interrupt penalty, both arms, one call | IS-INT-07 (B-ATK-07) | **CONFORMS**; provenance faithful; substrate-side by the S3-§4 ruling |
| **Class-level pricing with no per-mechanism term** | IS-INT-01..05, IS-MTD-09 ("classing drives attacker-interaction semantics") | **CONFORMS — the class abstraction *is* the documented model.** No lineage paper prices disruption per mechanism or conditions interruption on mutation scope; a mechanism-scope term would be a beyond-paper addition. Ratification requested so the model is *stated*, → D-20 |
| Interruption-attempt threshold | IS-INT-06 | DIVERGES-DOCUMENTED-NOWHERE — already open as **D-09**; consumed, not re-opened |
| Suspend/discard + priority ordering | IS-SCH-05/06 | CONFORMS (delta) / underspecification, as audited; realised traffic shows no per-mechanism skew (§(c)) |
| Movement arm declines channel 4; interrupt-as-failure verdict | — (S3-R seam) | **Settled design working as recorded** (indistinguishability §1.2 precedent) — not a candidate |
| `DWELL` sentinel judged interruptible | — (no paper models a non-dispatching state) | Beyond-spec **movement-layer design choice, recorded in code only** (`attacker.py:118-128`); this record is now its documentation → ratify as mapping policy, D-21 |
| Penalty absorption vs native immune window; counter asymmetry | — (papers silent on overlapping mutations) | Effects are arm-parallel by construction (neither pays twice); the *counter* divergence is documented-nowhere → D-22 (flag-grade) |
| ρ-decay per interrupt, uniform across class and mechanism | — (movement layer) | Declared, tiered, swept ([`pipeline/ogasp/learning_capability.md`](pipeline/ogasp/learning_capability.md)); the class-faithful refinement is named as a considered alternative in `learning.py` — already carries its declaration |
| `observed_changes` unwired | — | Axis-8 exclusion stands (Marc, 2026-07-28); verified dead |

## (f) Findings and costed options (the disposition requests)

**D-20 — the framing decision the brief exists to force: is class-level
pricing the intended model?** The evidence: channels 1–4 are functions of
`resource_type` alone; within a class, every mechanism buys the same
interrupt, the same 20.5 penalty, the same (non-)clear — measured identical in
every recorded data set. Combined with the dead network-state writes
(briefs 1–2, D-18/D-19), `(complete_topology, ip_shuffle)` and
`(os_diversity, service_diversity)` are each one mechanism against this
attacker, so the comparative evaluation currently compares **resource classes,
not mechanisms**, wherever a mechanism's network write is unread.
*Options:* **(a) Ratify class-level pricing as the documented model**
(recommended): zero code, zero golden movement; the §c verdict above says the
papers document exactly this abstraction; the reporting consequence is
decision-C-style cardinality statements (already drafted for experiment 2 in
the indistinguishability brief §8). **(b) Add mechanism-level
differentiation** (e.g. a mutation-scope term — interrupt only if the mutation
touched the attacker's current host/service): a beyond-paper substrate
semantics change to both arms; every golden moves (full D-05 procedure);
weakens every mechanism against both attackers; creates a new comparability
boundary; and it would *separate* the pairs only in conjunction with the
D-18/D-19 rulings, so it should not be taken independently of them.

**D-21 — ratify the movement arm's interrupt-exposure profile as mapping
policy.** Two mapping-owned choices set the movement attacker's exposure:
the `DWELL` sentinel (exposed to network + application — the conservative
reading, code-recorded) and the recon-verb tactic assignments (app-immune
17–43 % of clock by profile, §(d)). *Options:* **(a) Keep** (recommended):
the gate's semantics are untouched and documented (IS-INT-05); the profiled
attacker's greater immune share is a behavioural fact of doing
reconnaissance, and the DWELL exposure prevents the opposite unfairness (a
57 %-of-clock hiding spot). Cost: none; this record states the asymmetry
beside any cross-arm comparison. **(b) Make dwell-only places app-immune**
(map DWELL into the recon set): a one-line controller-seam change, no
substrate/golden cost, but it would shield 28–56 % of the movement attacker's
clock from half the defence family and shrink application-class yield from
~0.70 to ~0.21–0.30 — a large, hard-to-defend flattering of the profiled
attacker. **(c) Re-map tactics to change the immune share**: a mapping
version decision, owned by the mapping-sensitivity programme, not this
boundary.

**D-22 — the interrupt-counter asymmetry under overlapping mutations
(flag-grade).** The movement arm counts absorbed mid-penalty hits in
`Total attack interrupted`; the native arm's immune window means it never
registers them (≈ 0.3 counts/run at `simultaneous`, zero at single-mechanism
conditions). Neither arm double-pays; only the counter's meaning drifts.
*Options:* **(a) Keep and document** (recommended — this record plus a line in
[`metrics_semantics.md`](metrics_semantics.md) if the counter is ever compared
cross-arm). **(b) Suppress the count when the penalty absorbs the hit**: a
substrate change to `_interrupt_adversary`/`apply_mtd_interrupt_cost`
coordination; moves goldens that include `simultaneous` stats; not worth it
unless cross-arm interrupt counts become a reported metric.

**Penalty scale (flag only, no disposition sought).** PENALTY = 20 is
provenance-faithful (Brown §V-A, Zhang §4.4.3) and lands at the same order as
the declared tactic dwells (catalogue means 4.5–45 s) and a tenth of the
200 s trigger interval; realised confusion time is 7–17 % of the movement
attacker's clock at the operating interval — material but not dominant, and
identically priced on both arms. No re-tune is proposed; re-tuning without a
provenance-backed disposition is out of scope by the brief's own rule.

## (g) Reproduction

```
# the executed truth table + cost semantics (stub collaborators, real methods)
python3 <scratchpad>/gate_probe.py                       # 2026-08-02 probe

# integration demonstrations (seed 42)
PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate \
    --mapping v2_partial --scheme simultaneous --seed 42     # DWELL interrupts, verdicts
python -m mtdnetwork.trace --scheme single --mtd OSDiversity --seed 42
python -m mtdnetwork.trace --scheme single --mtd CompleteTopologyShuffle --seed 42

# realised traffic (recorded data, no re-run)
#   data/results/expo02_ashen_lynx/runs.jsonl   (interrupts, mtd_penalty_total, forgettings)
#   data/results/frontier_disruption/runs.jsonl (mtd_executed, mtd_suspended, n_by_mechanism)
```

The exposure diagnostic (§(d)) is `run_movement(profile, seed=s,
mapping_version="v2_partial", mtd_scheme=None, retrace_sinks=True)` over
5 profiles × 10 seeds, classifying each `MovementRecord`'s span by the
`curr_process` it presented to the gate.
