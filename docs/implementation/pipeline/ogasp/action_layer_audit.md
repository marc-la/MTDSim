---
status: durable
created: 2026-07-27
updated: 2026-07-27
topic: "L3 action layer — the S2 defect audit: every verb and the carve dispositioned bug / inherited divergence / by design, with the two fixes taken, the fixes deliberately declined, and the four decisions escalated to Marc"
lineage: closes docs/handoffs/2026-07-27_action_layer_refinement_under_freeze.md (S2)
---

# The action-layer defect audit — what is broken, what is merely inherited, and what stays broken on purpose

**Status:** durable investigation record; immutable history. Annotate with status
banners rather than rewriting.

**Why this exists.** The S2 change freeze
([`supervisor_decision_register.md`](supervisor_decision_register.md) §S2) permits
only *refinement of existing code and bug fixes*. Experiment 2 is meant to measure
the **model**, which requires knowing the **plumbing** is not what is failing. This
audit walked the six inherited verbs and the carve looking for genuine defects — a
thing the two anatomy records were not doing, because they were describing
behaviour rather than judging it.

**The distinction every row turns on** (from
[`../../../workflows/guardrails.md`](../../../workflows/guardrails.md)): an
**inherited divergence** is the code's reality, to document or parameterise, never
to "correct"; a **bug** is unintended — it violates an invariant, or entered
through an unexplained change with no basis in the source papers. Fixing inherited
reality is as much an error as leaving a bug.

**Method.** Three independent audits over disjoint surfaces (the queue/cursor verbs;
the exploit/record seam; the carve and driver), each required to verify every claim
empirically against a seeded run rather than by reading. Every finding below was
then re-verified first-hand before being recorded; the counts quoted are from that
second pass, not the first. The audits' combined base is roughly 200 instrumented
runs. The seeded no-MTD golden (**692 records / 41 hosts**) was the instrumentation
check throughout.

---

## The headline

**Twenty-two observations. Two fixed, sixteen dispositioned, four escalated.**

The two fixes were both in the **carve and driver — code this project wrote**, and
both are golden-neutral. That asymmetry is the finding: almost nothing was wrong
with *our* layer, and what is wrong with the *inherited* layer is either unreachable,
outside the boundary, or too entangled with the goldens to touch under a freeze.

**The precondition blocking observed in experiment 1 was not examined as a defect.**
It is deliberate, verified (P4), and is a result to report
([`runtime_verification.md`](runtime_verification.md) §P4).

### The four decisions this audit cannot make

Ranked by how much they threaten experiment 2. Each is cheap to decide now and
expensive to discover afterwards.

1. **E2 — vulnerability objects are shared between hosts, so exploitation spreads by
   contagion.** 68 % of vulnerability instances are shared across more than one host;
   in the seeded golden, **86 of 124 services on hosts the attacker never ran a
   single exploit against already read as exploited**. This inflates compromise
   throughout every result to date. Substrate-side (D5) and golden-rewriting, so it
   is not this audit's to fix — but it is the largest validity question in the
   codebase and it should not wait for the freeze to lift.
2. **F1 — the movement arm's MTD interrupt gate is decided against the wrong verb**
   for the duration of every dwell, flipping **27 %** of application-layer interrupt
   decisions. Entangled with dwell semantics, which S3 owns.
3. **B3 — the movement arm pays no MTD confusion penalty** (0.0 against the native
   arm's 1 964–2 536 t/u per run) **and never resets its host cursor** after a
   network-layer mutation. Owned by S3.
4. **A1 — `SCAN_HOST` queues duplicates**, inflating the per-host attempt counter
   under MTD. Fixing it moves every MTD golden, so it is a re-baseline call.

---

## 1. Fixed (2 rows)

Both in the carve/driver, both leaving all nine `baseline/golden` scenarios
byte-identical, both with a regression test verified to fail without the fix
([`tests/l3_simulation/test_movement_driver_regressions.py`](../../../../tests/l3_simulation/test_movement_driver_regressions.py)).

### D1 — the compromise that ended the run was thrown away

`MovementAttacker._dispatch` inferred "the sim ended mid-verb" from
`end_event.triggered`. But `step()` runs the verb's core *before* returning, and
three cores (`_do_exploit_vuln`, `_do_scan_port`, `_do_brute_force`) call
`update_compromise_progress`, which fires `end_event` once the objective is met. A
verb that **ran, succeeded, and completed the run** was therefore reclassified as an
abort and its outcome discarded.

*The damage* was a structural inconsistency between the two headline metrics: the run
counted toward **ASR** (which reads `end_event`) while contributing nothing to
**MTTC** (which reads compromise events). The single most important event in the run
was the one event the reader could never see. Reproduced with a 1-host objective,
seed 42: `objective=True, compromised=1`, yet `first_compromise_time() is None` and
the last record read `SIM_END` with an empty verdict.

*The fix* makes the abort explicit instead of inferred: `step()` returns a new
`STEP_ABORTED` sentinel, and `_dispatch` tests the outcome rather than the flag. This
also resolves the latent ambiguity that `_do_scan_neighbors` legitimately returns
`None`. Invisible in experiment 1 only because the 0.8 compromise ratio is
unreachable for the movement arm (max observed: 5 hosts) — so the fix changes no
experiment-1 number, and prevents a real inconsistency the moment experiment 2's
sink-retrace and richer mapping make the objective reachable.

### D2 — an interrupted dwell was recorded as if fully served

On an MTD interrupt the driver abandons the remaining dwell but wrote the full
catalogue value into the record anyway. **15–17 %** of records under live MTD claimed
more dwell than the whole event occupied — e.g. an event spanning 21.0 t/u recording
a dwell of 35.0 — making the derived verb-time (`elapsed − dwell`) spuriously
negative. The `MovementRecord.start_time` field comment was also simply false
("after dwell"; it is taken before).

*The fix* records the dwell actually consumed on the interrupted path only, so the
~85 % of events whose dwell runs to completion still carry the catalogue value
bit-for-bit and no prior analysis of clean events shifts. Corrects the field comments
in the same change.

---

## 2. Declined — genuine bugs the freeze or the boundary puts out of reach (9 rows)

Each row states the exclusion that blocks it. "Golden-safe" means a fix would leave
all nine goldens byte-identical.

| # | Locus | Observation | Golden-safe? | Why declined |
|---|---|---|---|---|
| **A1** | `_do_scan_host` (`:206-227`) | `host_stack` accumulates one entry per compromised neighbour with no dedup, so `attack_counter` double-counts | **No** | Re-baseline (Marc) |
| **A2** | `_do_scan_neighbors` (`:457-463`) | Does not filter `stop_attack`, so a given-up host re-enters the queue | Yes (no-op today) | Conditional on Marc's give-up disposition |
| **A3** | `_do_enum_host` (`:286`) | Unguarded `curr_host.compromised`; small geometries generate host-less graph nodes | Yes | D5 — root cause is network construction |
| **A4** | `attack_statistics.py:28-29` | `attack_counter[-1]` negative-index read whenever `curr_host_id == -1` | **No** | D5 (statistics) **and** golden-moving |
| **A5** | `hosttopologyshuffle.py:57` | Host swap remaps `_compromised_hosts` only; four other id-keyed fields go stale | Yes | D5 (MTD layer); strategy is dormant |
| **E1** | `_do_exploit_vuln` (`:387-397`) | A compromise is stamped onto the **previous verb's** record row when the vuln list is empty | **No** | D5 (statistics) **and** golden-moving |
| **E2** | `services.py:215` `Service.copy()` | Vulnerability objects shared between hosts — exploitation spreads by contagion | **No** | D5 (service layer); rewrites every result |
| **E3** | `host.py:361-375` `get_vulns` | Can hand the same `Vulnerability` object to the exploit loop twice | **No** | D5 (host layer) |
| **E5** | `host.py:291` | Service-graph node ids concatenated into a port-number list (type confusion) | Yes | D5 (host layer); latent — inert at this geometry |

### A1 — `SCAN_HOST` enqueues duplicates, and the give-up counter believes them

`_do_scan_host` accumulates `network.graph.neighbors(c_host)` for **each**
compromised host without deduplicating, so a host adjacent to *k* compromised hosts
is queued *k* times; `_do_enum_host` then ticks `attack_counter` once per pop.

The tell that this is a defect rather than a design choice is **local
inconsistency**: the exposed-endpoint append later in the same function filters, and
`_do_scan_neighbors`'s merge filters. Only this loop does not.

| scheme | SCAN_HOST fired | scans producing duplicates | worst multiplicity |
|---|--:|--:|--:|
| no MTD | 1 | 0 | 0 |
| simultaneous | 63 | 48 | 6 |
| random | 21 | 13 | 3 |

Multiplicity matched the number of compromised neighbours in 841/841 sampled cases,
and peaked at **10** — one scan able to consume a host's entire give-up budget.

*Declined because* the no-MTD golden is untouched (`SCAN_HOST` fires once, at t = 5,
against an empty compromised set — hence the long invisibility) but **every MTD
golden would move**. That is a re-baseline: Marc's call, its own changelog entry,
never an audit's side effect.

### A2 — the give-up list leaks through `SCAN_NEIGHBOR`

`stop_attack` is consulted at exactly **one** site (`:225`). `_do_scan_neighbors`
prepends raw `discover_neighbors()` output, so a blacklisted host re-enters the queue
— the give-up invariant violated by a sibling verb. With `network_type` forced to 0
so the rule is live: 25 enumerations of a blacklisted host across 20 runs, 8 of them
fresh attacks.

*Declined because* it is **latent** — `stop_attack` is always empty in every
reachable configuration (B1) — and because it is half of a mechanism whose activation
is an open disposition for Marc. Repairing one half of a rule nobody has decided to
keep would be guessing a disposition. **If the give-up rule is ever activated, this
must be fixed in the same change.**

### A3 — small geometries generate host-less nodes

`gen_graph`'s node floor can exceed `total_nodes`, but hosts are attached only for
`range(total_nodes)`, so `get_host()` returns `None` and `_do_enum_host:286` derefs
it.

| requested `total_nodes` | clamped to | graph nodes | host-less ids |
|--:|--:|--:|---|
| 10 | 16 | 19 | 16, 17, 18 |
| 16 | 16 | 19 | 16, 17, 18 |
| 18 | 18 | 19 | 18 |
| 19 | 19 | 19 | — |
| 50 | 50 | 50 | — |

`TimeNetwork.__init__` clamps `total_nodes` up to `2 × total_subnets` = 16, so **any
request below 16 lands squarely in the broken band** and the run dies with
`AttributeError: 'NoneType' object has no attribute 'compromised'`. No experiment is
affected — every run uses the 50-node geometry. Related to the existing F-06
`gen_graph` loop-guard note. *Declined because* the root cause is network
construction (D5); guarding attacker-side would mask a substrate defect.

### A4 — the attack record reports another host's attempt counter

`attack_statistics.py` indexes `attack_counter[curr_host_id]` unguarded, and
`_handle_interrupt:174` sets `curr_host_id = -1` after a network-layer MTD — so the
record silently reports the **last node's** counter. Seed 7: 6 of 54 such rows leaked
values; seed 8: 12 of 52; and one sweep found 8 rows reporting `current_host_attempt
= 3` for `current_host = -1`, exactly matching node 49's counter. Found independently
by two audits. The tell that it is unintended: the `uuid` field two lines above **is**
guarded with `if adversary.get_curr_host()`. *Declined because* it is doubly excluded
— statistics layer (D5) and golden-moving. Impact is record fidelity only, but the
record is the research artefact.

### E1 — a compromise stamped onto the wrong verb's row

`update_compromise_host` back-patches `_attack_operation_record[-1]`, which is only
correct under the invariant *"the verb calling it has just appended its own row."*
`_do_exploit_vuln` appends its row **inside** the per-vuln loop — so when the vuln
list is empty the loop never runs, no row is appended, `check_compromised()` can
still return `True`, and the compromise is stamped onto the preceding **`SCAN_PORT`**
row. Since `EXPLOIT_VULN` is only reached after `SCAN_PORT` returned `False`, every
such row asserts a compromise for a `SCAN_PORT` that explicitly failed.

227 of 1 640 host compromises (**13.8 %**) across 40 MTD runs are mis-stamped, with
the right host but the wrong phase — and **0** in the no-MTD golden. So it is an
**MTD-only bias in exactly the phase attribution the outcome overlay depends on**.

### E2 — vulnerability objects are shared between hosts (the contagion)

`Service.copy()` returns a new `Service` wrapping **the same** `Vulnerability`
objects, and `get_random_service` hands those copies to every host from a shared
pool. `Vulnerability.exploited` is per-instance, and `Service.is_exploited()` sums
exploited impact — so exploiting a vuln on host A flips service state on host B.

Verified directly in the seeded 50-node network:

- **307 of 451 (68.1 %)** vulnerability instances sit on services belonging to more
  than one host; the maximum is **12** hosts sharing a single instance.
- `Service` objects themselves are **never** shared (0 of 373) — which is exactly
  what disguises the aliasing.
- Causal demonstration: a vuln shared by hosts {0, 3, 6, 7, 22, 25, 30, 31, 33, 41,
  44, 48} reads `exploited=False`; exploiting it **on host 0** makes **host 3** read
  the same vuln as exploited.
- In the seeded golden run the attacker ran `EXPLOIT_VULN` against 34 hosts, yet
  **86 of 124 services on the hosts it never touched already read
  `is_exploited() == True`**.

The tell that this is unintended: `Host.get_all_vulns` **does** dedup by instance, so
aliasing was on the original author's radar — but the path the attacker actually
uses, `Host.get_vulns`, has no equivalent, and `copy()`'s own docstring promises "a
copy of this service instance".

*Declined because* it is the host/service layer (D5) and fixing it would change every
number this project has produced. **Escalated as decision 1** — it inflates compromise
throughout, and it is what generates E1's empty vuln lists in the first place.

---

## 3. Dispositioned as inherited divergence or by design (11 rows)

The three the handoff named — **B1** the give-up rule, **B2** the inert cap, **B3**
the confusion penalty — are dispositioned in full, with their evidence, in the
anatomy record's limitations register
([`action_layer_anatomy.md`](action_layer_anatomy.md) §4.2), and the conformance-spec
rows `ATK-05` / `ATK-07` / `ATK-08` plus two `provenance.md` rows were
re-dispositioned against them. In brief:

- **B1 — the give-up rule is unreachable, not merely inactive.** `TargetNetwork` is
  never instantiated and `copy_network` (the only setter of `network_type = 0`) is
  never called, so Brown's Table I bound cannot fire in any configuration this
  repository can construct. `stop_attack` was empty in all nine sampled cells while
  hosts exceeded the bound — one host enumerated **50** times. `ATK-07` moved from
  `verified` to `divergent (unreachable)`; provenance's "faithful" likewise.
- **B2 — the global attempt cap is inert and genuinely overrun** (481 attempts
  against a cap of 250 in the seeded golden; 474–713 across MTD cells). Kept inert on
  purpose: paper-free origin, and restoring the guard would truncate every run.
- **B3 — the confusion penalty is paid by one arm only.** Native: **1 964–2 536** t/u
  across 96–124 interrupts per 15 ks run (13–17 % of the horizon). Movement: 74–108
  interrupts, **0.0** t/u. The driven arm also **never resets its host cursor**, so it
  resumes exploiting the same host immediately after a topology or IP shuffle, where
  the native arm restarts at `SCAN_HOST`. Owned by **S3**.

### The remaining eight

| # | Observation | Disposition |
|---|---|---|
| **C1** | `attack_counter` counts **enumerations**, not attempts — 47 % of enumerations tick it for an already-compromised host | inherited divergence; the give-up rule reads it as though it were attempts |
| **C2** | `SCAN_NEIGHBOR`'s documented prepend is mostly inert — `_do_enum_host` re-sorts before popping, so the prepended head survives in only 28 % of cases | inherited divergence; the distance-and-pivot sort is the real priority function |
| **C3** | Half of `_set_next_pivot_host`'s work is immediately overwritten by `update_compromise_progress` (48 of 102 enumerations) | by design; redundant, harmless |
| **C4** | The attacker is **un-interruptible for the whole confusion penalty** — `_attack_process` is never repointed at the `_handle_interrupt` process. 4.5 % of would-be interrupts are dropped, and they are also missing from `add_total_attack_interrupted` | inherited divergence; the `is_alive` guard is deliberate but the resulting ceiling on MTD effectiveness (13.3 % of sim time immune) and the undercount are undocumented |
| **C5** | A zero-vuln `EXPLOIT_VULN` returns `EXPLOIT_COMPROMISED` at **zero** time cost (89 of 94 dispatches in one cell), because the host's flag is already set | inherited (identical pre-carve). **Interpretive caveat:** the reader's "compromise events" therefore run 20–60× the distinct-host count, so the P4 table's compromise-event column is not a compromise count. `first_compromise_time()` was separately verified sound in 18/18 cells |
| **F1** | `curr_process` is stale for the whole dwell, so the MTD interrupt gate is decided against the **previous** verb while the record attributes the interrupt to the pending one. 88 % of interrupt decisions are taken while no verb is running; **27 %** of application-layer decisions flip if judged on the pending verb (494 missed, 124 spurious) | **defect, declined** — the resolution (pending verb vs a neutral value) is a dwell-semantics decision S3 owns. **Escalated as decision 2** |
| **F2** | The driven arm appends **no** attack-operation record on an MTD interrupt (1 954 interrupts, 0 attributed rows), where the native arm appends one for every single interrupt | parity gap, declined — verified to have **no** downstream consumer for the movement arm today; recorded so a future cross-arm comparison on that record does not silently differ |
| **F3** | The `EXPLOIT_VULN` docstring still claims "top 5 vulnerabilities"; the cap is genuinely applied **per service**, so the verb receives >5 vulns in 65 % of invocations (max 54) | documentation defect; already correct in [`attacker_phase_catalogue.md`](attacker_phase_catalogue.md), only the code docstring is stale |

### What came back clean

Eight hypothesised defects were hunted and **disproved** — recorded so they are not
re-litigated. Most notable: the `vulns`-parameter vs `get_curr_vulns()` divergence in
the exploitability-bump loop is **impossible** (identity-checked, 0 mismatches; no
interleaving can occur because the interrupt terminates the generator before
`_handle_interrupt` is scheduled); the float-equality guard
`exploitability == cvss / 5.5` is **exact**, never drifts (10 738 fires, 816 skips, 0
skips with |diff| < 1e-9); and `_handle_interrupt`'s `_interrupted_mtd` **cannot** go
stale on any of the three hypothesised paths (0 occurrences in 140 MTD runs each).
Also clean: `attack_counter` can never raise `IndexError` (sized from the id space,
not `total_nodes`); the give-up threshold's `==` cannot be stepped over; process
registration is sound (`set_attack_process` called exactly once, no native raise ever
fires during a movement run); interrupt delivery is exact (1 954 issued = 1 954
observed); and seam invariant 3 holds — the driver forks no controller semantics.

---

## 4. What this means for experiment 2

The handoff's purpose was to make experiment 2's failures attributable to the model
rather than the plumbing. The answer, stated plainly:

- **The plumbing carries four known distortions into experiment 2** — E2 (compromise
  inflated by contagion), F1 (a quarter of application-layer MTD interrupts decided on
  the wrong verb), B3 (the movement arm neither paying the penalty nor losing its
  host cursor), and A1/E1 (attempt counts and phase attribution skewed under MTD).
- **None is a silent unknown any more.** Each is measured, attributed to an owner, and
  pinned by a test wherever it is pinnable.
- **Two of them bias the comparison in the movement arm's favour** (B3) **and one
  inflates both arms alike** (E2) — so they do not cancel, and the direction of each
  is known.

The honest-negatives column of the APT-model criterion
([`../../apt_model_criterion.md`](../../apt_model_criterion.md), landed by S6 the same
day) should carry B1 (an attacker that never gives up) and B2 (an attacker with no
effort ceiling) as *modelled* limitations rather than accidents: both are now
deliberate.

## 5. Where the evidence lives

- Characterisation tests pinning B1 / B2 / B3:
  [`tests/test_action_layer_dispositions.py`](../../../../tests/test_action_layer_dispositions.py).
- Regression tests for the two fixes:
  [`tests/l3_simulation/test_movement_driver_regressions.py`](../../../../tests/l3_simulation/test_movement_driver_regressions.py).
- The carve's own gate: [`tests/test_action_layer_carve.py`](../../../../tests/test_action_layer_carve.py).
- Nine-scenario golden reproduction: [`tests/test_atk04_reexploit_discount.py`](../../../../tests/test_atk04_reexploit_discount.py).
- Behaviour descriptions (not judgements): [`action_layer_anatomy.md`](action_layer_anatomy.md),
  [`attacker_phase_catalogue.md`](attacker_phase_catalogue.md).
- Why precondition blocking is not on this list: [`runtime_verification.md`](runtime_verification.md) §P4.

## When this would need updating

- If Marc rules on E2, A1, E1 or A4 — the re-baseline lands and those rows become
  *fixed*, with a changelog entry.
- If the give-up rule is activated — A2 must ship in the same change.
- If S3 lands — B3's characterisation test goes red by design and is replaced, and F1
  is resolved one way or the other.
- If `HostTopologyShuffle` is re-enabled — A5 must be fixed first.
- If the freeze lifts — the exclusion classes stop binding and the declined rows are
  re-triaged against the new scope.
