---
status: proposed        # Marc rules the two decisions in §2 before any line is built
created: 2026-08-30
---

# Build brief — encode the targeted objective into the movement attacker

> **One-line goal.** Make `attack_objective="targeted"` do Brown's work on the
> movement attacker — target chosen on the seam, Brown's layer-priority host
> selection, never-give-up on the target, termination on target compromise —
> with the `general` arm and every golden byte-identical, and a verification
> ladder that proves the targeted arm *executes* the rules, not merely carries
> the flag. Proposal first (this brief); build only after §2 is ruled.

## 0. Where this starts from

- The input exists vacuously: `run_movement(attack_objective=...)` →
  `MovementAttacker.attack_objective` → `MovementRunResult.attack_objective`
  (`4e7bf172`), pinned bit-identical to `general` by
  `tests/l3_simulation/test_movement_attack_objective.py::test_targeted_is_vacuous_today_bit_identical_to_general`
  — **that test is retired by this build**.
- The fresh-host contract is the reported configuration (`2497845b`): the
  ENUM_HOST retry-until-fresh loop runs on the movement seam through the
  shared core `_do_enum_host`. Reach on the fixed attacker is 1.4 % at
  15 000 s and 14.6 % at 30 000 s
  ([`../implementation/pipeline/ogasp/targeted_objective_probe.md`](../implementation/pipeline/ogasp/targeted_objective_probe.md)
  §5 annotation) — still degenerate against the 20 % Gate, and the barrier is
  navigation (B-i). This build is the B-i lift.
- The token-hold rule is off, degenerate and spun out; it is a routing-level
  rule and orthogonal to host selection. No interaction to design for.
- The spec: Brown IS-SCN-03 / B-ATK-02 (priority), IS-SCN-04 / B-ATK-06
  (never give up on the target), Brown §III-C(1) (terminate on target). No
  time-domain spec exists (IS-SCN-06): recorded as an **extension**.
- Everything verified about the inherited machinery is in the probe record
  §10; the change list it proposes is §11. This brief makes §11 executable.

## 1. The design, in five parts

### 1.1 The target — chosen on the seam, never in `gen_graph`

Two run inputs beside `attack_objective`:

- `target_layer: int | None = None`. `None` → the target set is
  `frozenset(network.get_database())` (the crown jewels, layer 3 on the
  shipped geometry — the set the probe already measures, so every existing
  reach number stays comparable). An `int` `k` → **one** host drawn from
  `[h for h, l in network.get_layers().items() if l == k]` with a dedicated
  `random.Random(seed)`-derived stream (never the substrate's global stream,
  so construction and the general arm's draws are untouched). This is Brown's
  `TX` sweep.
- Derived, not input: `target_hosts: frozenset[int]` (empty under `general`)
  and `target_layer_resolved: int` (the layer the priority key measures
  distance to; layer 3 when the database set is used).

Both carried on the result (`target_hosts`, `target_layer`) so a row is
self-describing. Keyed on `get_layers()`, never the `db` tag (probe §10.1).

### 1.2 Host priority (T-b) — the one change that makes the attacker targeted

**Decision A (recommended): a sort hook on the shared core.** `AttackOperation`
gains one attribute, `host_sorter`, default `None`; `_do_enum_host` replaces
its direct call with

```python
sorter = self.host_sorter or network.sort_by_distance_from_exposed_and_pivot_host
adversary.set_host_stack(sorter(adversary.get_host_stack(),
                                adversary.get_compromised_hosts(),
                                pivot_host_id=adversary.get_pivot_host_id()))
```

Under `general` the hook is `None` and the line is the old line — the general
arm is byte-identical by construction. The movement layer builds and installs
the targeted sorter (`movement/targeting.py::TargetedSorter`) at
`run_movement`, so the *policy* lives in the movement layer and the substrate
holds only the seam. The sorter:

```python
def __call__(self, stack, compromised, pivot_host_id=-1):
    by_distance = network.sort_by_distance_from_exposed_and_pivot_host(
        stack, compromised, pivot_host_id=pivot_host_id)   # same draws as general
    return sorted(by_distance, key=self.priority)          # stable: distance order kept within class
def priority(self, host):
    if host in self.target_hosts: return 0
    return abs(layers[host] - self.target_layer) + 1
```

Three properties fall out, each tested (§3): Brown's first clause ("attack
only the target if found") is priority 0 sorting first; same-layer hosts
(priority 1) precede adjacent-layer (2) precede far-layer; **within a class the
order is the general attacker's** (nearest-from-foothold, Python's sort is
stable), so the targeted attacker still moves toward the nearest host of the
preferred class. And because the general sort runs first over the *same*
stack, the tiebreak draws exactly as many `random.random()` values as the
general arm would — the D-29 shared-stream discipline is unchanged.

Every pop path — `step("ENUM_HOST")`, `_reselect_fresh_host` under the
fresh-host contract, and the native FSM's own `_execute_enum_host` — goes
through the one core, so the rule holds wherever a host is chosen, and the
inherited baseline can run the same targeted policy for the comparison arm
with no second implementation.

**Decision B (movement-only fallback, if the S2 freeze is held):** narrow the
adversary's `host_stack` to the highest non-empty priority class before the
core pops, and re-append the other classes in priority order after it — a
pre/post wrapper on `_do_enum_host` in the attacker, applied in `_dispatch`
around `step("ENUM_HOST")` (with `try/finally` so an interrupt mid-step still
restores the queue) and inside `_reselect_fresh_host`. Same observable rule,
no substrate line — but three call sites instead of one, the baseline arm
cannot share it, and the tiebreak draw count differs from the general arm's
(fewer hosts in the sorted stack). Recorded here so the freeze question is
answered on its own terms; it is not the recommendation.

### 1.3 Never give up on the target (T-c)

The dead guard at `attack_operation.py:421`
(`network.network_type == 0 and curr_host_id == network.get_target_node()`)
becomes `adversary.get_curr_host_id() in self.target_hosts`, with
`AttackOperation.target_hosts: frozenset[int] = frozenset()` set beside the
sorter. Empty under `general` → identical behaviour. (Under decision B the
movement layer would have to remove the target from `stop_attack` after each
core call — the ugliness is a further argument for A.)

### 1.4 Termination (T-d)

Movement arm: in the record writer (where `_database_held` already computes
the held set), if `attack_objective == "targeted"` and
`held & target_hosts`, call `end_event.succeed()` once. `_walk` reads
`end_event.triggered` at the top of every place visit (`attacker.py:550`), so
the walk ends on the next visit and the terminal record is written by the
existing path. `reached_objective` then means *target reached* under
`targeted`; `TimeNetwork.is_compromised` (the 80 % ratio) stays the `general`
criterion and is never replaced — the comparability bridge to Zhang/Ho/Brown.

Baseline arm (for the comparison experiment only): re-enable the commented
block at `attack_operation.py:732` keyed on `target_hosts`, not `network_type`.

### 1.5 Observability

- `MovementRecord` gains `target_class: int | None` — the priority class of
  the host ENUM_HOST popped (0 = the target itself), `None` on non-ENUM rows.
- The trace tool (`mtdsim.l3_simulation.trace`) prints the objective and the
  target set in its header and, per ENUM row, `popped host 37 (class 1, layer
  2)`; the summary line reports pops per class and whether the run ended on
  the target. This is how a targeted run is *shown* to be targeted.

## 2. The two decisions Marc rules before a line is built

1. **Decision A or B (§1.2).** A writes three default-preserving lines into
   `attack_operation.py` (the sorter hook, the give-up guard, the termination
   block) — the S2 freeze and the host-selection gate of
   [`../implementation/pipeline/ogasp/movement_objectives_design.md`](../implementation/pipeline/ogasp/movement_objectives_design.md)
   §6, the same gate the fresh-host contract just passed through. Recommended.
2. **The target under the headline sweep.** Database set (the probe's
   comparable target, deepest layer) as the default, with `target_layer ∈
   {1, 2, 3}` as Brown's `TX` sweep for the experiment. Recommended as stated.

Everything else in §1 is a routine judgement call and will be built as
written unless ruled otherwise.

## 3. Verification ladder — how "properly executed" is demonstrated

Each rung is a committed artefact; the build is not done until all seven pass.

1. **General-arm bit-identity.** Every movement golden (the 70 re-baselined
   at `ce8739ad`) and every baseline golden unchanged; the vacuous-input test's
   bit-identity assertion is replaced by
   `test_general_arm_unchanged_with_targeted_machinery_present`, which runs
   `general` with the sorter attribute present-but-`None` and compares to the
   golden stream. Full L3 + action-layer suites green.
2. **Sorter unit tests** on a hand-built stack with known layers and a
   pinned RNG: target visible → popped first; target absent → same-layer
   before adjacent before far; within a class, the general order; **the
   number of `random.random()` draws equals the general sort's** on the same
   stack.
3. **Give-up test.** Drive eleven failed attempts on the target: it is never
   appended to `stop_attack`; a non-target host is, at ten.
4. **Termination test.** A targeted run whose walk compromises a target host
   ends with `reached_objective=True`, `compromised_count < 40`, and the
   terminal record's `end_time` equal to `first_database_reach_time` (or the
   drawn target's first-held time).
5. **Determinism (SIM-05).** Same `(profile, seed, target_layer)` twice →
   identical records; `general` and `targeted` at the same seed differ only
   from the first ENUM pop that the priority re-orders (hand-checked on the
   trace).
6. **Hand trace.** `python -m mtdsim.l3_simulation.trace --profile aggregate
   --seed 0 --attack-objective targeted` (and `--target-layer 2`): read every
   ENUM row, confirm class order, confirm the run ends on the target. The
   trace is pasted into the findings record.
7. **Pre-registered Gate 0 re-ask, before any claim.** Unopposed, 350 seeds,
   five profiles + baseline, `target_layer ∈ {1, 2, 3}` and the database set,
   `fresh_host_contract=True`, 15 000 s: reach rate (BCa CI), time-to-target
   (Kaplan–Meier), footprint-at-reach. Criteria and the "better" threshold
   are the probe's §3.2–§3.3 verbatim; the Gate is ≥ 20 % on some profile for
   the shallowest target. Only if the Gate holds does the under-MTD matrix
   (100 seeds, four mechanisms) run, and H2 is re-established on the targeted
   objective, never carried.

## 4. Scope and hard constraints

- Additive only; `general` byte-identical; no golden re-baselined (rung 1 is
  the proof, not an assertion).
- No `gen_graph` repair — B1–B3/B6 stay as recorded; the target is a seam
  choice.
- Brown's knowledge assumption (the attacker knows the target's *layer*
  before it sees the target) is stated in the record as Brown's, not argued.
- The inversion headline is currently spun out
  ([`2026-08-30_headline_on_restored_substrate.md`](2026-08-30_headline_on_restored_substrate.md));
  this build does not touch that line and must not be used to re-establish it.
- Findings go to a new `docs/implementation/pipeline/ogasp/targeted_attacker_findings.md`;
  the probe record's §11 and the dissertation's §2.2.3 M2 item are the
  inbound pointers. This brief retires in the commit that lands rung 7.

## 5. Estimated shape

`movement/targeting.py` (~80 lines), three lines in `attack_operation.py`,
~20 in `run.py` (inputs, sorter install, termination), one record field, the
trace rows, one test file (~150 lines), the pre-registration section of the
findings record. One session to build and verify rungs 1–6; rung 7 is ~10
minutes of compute plus the write-up.
