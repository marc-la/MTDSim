---
status: open
created: 2026-08-05
---

# Bring the inherited disruption model over to the movement attacker, faithfully — the defence must not know which attacker it is disrupting, and right now it does

**This is the prerequisite for a fair comparison, and it is a wiring job, not a
design job.** Marc's ruling from the Jin discussion, recorded 2026-08-05:

> Disruption should apply the same way regardless of attacker type — the defence
> mechanism doesn't need to know which attacker it's disrupting. Position-based
> disruption (loss of host access, forced re-scan) generalises naturally; the
> open question is really about how well each MTD mechanism's disruption is
> currently wired for the movement attacker, which needs to be run and checked
> rather than assumed.

So the disruption semantics are **settled and inherited** — they are not to be
reinvented, re-derived or re-tuned. What this brief owns is the narrower and
more tractable question: *does the inherited model actually reach the movement
attacker as it reaches the native one, mechanism by mechanism?* Where it does
not, the gap is a wiring defect or a mapping policy, and each one gets a verdict.

**This supersedes boundary review 3**, which asked the open-ended
class-versus-mechanism pricing question. Marc's ruling answers that question —
class-level pricing *is* the intended model — so what survives from that brief is
its verified six-channel inventory (§2), carried forward here as the thing to be
checked rather than re-litigated. The brief itself is retired.

## 1. Goal

Establish, by measurement rather than assumption, that each of the four reported
mechanisms delivers the same disruption to the movement attacker that it delivers
to the native one, given the class-level model. Every asymmetry is either
repaired, or dispositioned as mapping policy with its effect on the comparative
evaluation stated.

The stake is concrete. Two of the four mechanisms in the reported family have
**no live network-state coupling to the attacker at all** — IP Shuffle writes a
field no verb reads (boundary review 1, verified by projection diff), and OS
Diversity's relabel reaches exploitation through nothing (D-19). For those two,
these channels are their *entire* measured effect. If the channels reach the two
arms differently, the comparison is measuring driving mode, not defence.

## 2. The inherited model — six channels, already verified, not to be redesigned

Carried forward verbatim from boundary review 3's survey (code-verified
2026-08-02). Marc's mental model expected one channel; there are six.

1. **The interrupt condition** (`mtd_operation.py:211-258`) — whether a firing
   mechanism interrupts the in-flight action, decided by resource class × current
   verb. `network` interrupts any alive action; `application` only SCAN_PORT /
   EXPLOIT_VULN / BRUTE_FORCE; `reserve` only BRUTE_FORCE (D-07).
2. **The confusion penalty** (`attack_operation.py:161-208`) —
   `exponential_variates(PENALTY=20, 0.5)`, identical for every mechanism and
   both arms by the S3 ruling; absorbed, not stacked, under overlap.
3. **The lost connection / cursor clear** (`:206-208`) — network-class clears the
   host cursor (B-INT-01); application-class costs the service connection only
   (B-INT-02).
4. **Forced re-scan succession** — native hard-codes the recovery verb by class
   (network → SCAN_HOST, application → SCAN_PORT, reserve → EXPLOIT_VULN); the
   movement driver owns its own succession and reads the interrupt as a **failure
   verdict**.
5. **The verdict's downstream consumers** (movement arm only) — the failure
   verdict feeds the outcome overlay's routing, the axis-7 learner's belief
   (which additionally perishes by a declared fraction on every mutation), and
   the interrupt counters.
6. **The unwired observation channel** — `adversary.observed_changes`. Listed for
   inventory completeness. *(Its status is now live under the axis-8 proof of
   concept — see [`2026-08-04_vulnerability_memory_and_swift_mode.md`](2026-08-04_vulnerability_memory_and_swift_mode.md).
   It is still out of scope **here**: this brief is disruption wiring, not
   attacker capability.)*

**Marc's ruling settles the framing question these channels raised.** Channels
1–4 are functions of `resource_type`, so within a class every mechanism buys the
same disruption per trigger. That is now the **documented model**, not an open
question: the defence does not know which attacker it faces, and it does not know
which mechanism within its class it is. What follows from it is a *reporting*
consequence (the family's true cardinality — the OS/Service brief's decision C),
not a substrate change.

## 3. State of play — seven measured asymmetries between the two arms

**These are not hypotheses. Each was measured during the boundary reviews and
their adversarial passes (2026-08-02 to 2026-08-03), and each is a place where
the defence currently *does* behave differently depending on which attacker it is
disrupting.** They are the work list.

| # | Asymmetry | Evidence | Direction of bias |
|---|---|---|---|
| A1 | **EXPLOIT_VULN is uninterruptible in the movement arm.** With a supplied duration (`attack_operation.py:743-747`) the whole cost is one up-front `timeout`, then the vulnerability loop runs with **zero yields**. The native arm yields per vulnerability (`:466-467`), giving up to `SERVICE_TOP_X_VULNS_TO_RETURN` = 5 interrupt windows | code + run | **Against the diversity family** — OS/Service Diversity get materially fewer chances to block an exploit in the arm the headline runs on |
| A2 | **Application-class MTD can never produce a failure verdict on three verbs.** Interrupts are gated out of SCAN_HOST/ENUM_HOST/SCAN_NEIGHBOR (`mtd_operation.py:226-230`) *and* `verdict.py:59-60` reads those verbs as success-unless-interrupted. Measured: 26 `network`/SCAN_NEIGHBOR interrupts, **0** `application`/SCAN_NEIGHBOR | measured | **Against the diversity family** — failure-routing credit on half the verb set is structurally reserved for the network class |
| A3 | **The movement arm absorbs interrupts the native arm never receives.** The driver registers one long-lived process (`attacker.py:318-319`), so `attack_process.is_alive` is true even during the confusion penalty, where the native arm's per-verb process is dead (`attack_operation.py:199-204`). Still tallied, so `mtd_attack_interrupted` is **not comparable across arms** | code + run | Inflates the movement arm's interrupt counts against the native arm's |
| A4 | **Dwell places are interruptible, and the native attacker's equivalents are not.** `attacker.py:598` sets `curr_process="DWELL"`, which is not in the exemption list, so application-class mechanisms interrupt dwell-only tactics — while the native attacker is immune throughout SCAN_HOST/ENUM_HOST/SCAN_NEIGHBOR. Declared at `attacker.py:122-127`, but never classified as an arm asymmetry | code | **Toward the diversity family** — partially offsets A1/A2, which is why the net effect must be measured rather than reasoned |
| A5 | **A network-class mutation arriving during an application-class penalty loses its cursor clear.** `_pay_interrupt_cost` reads `_interrupted_mtd` before the penalty and nulls it after | code | Silently drops channel 3 for the position-destroying family |
| A6 | **The movement record cannot attribute an interrupt to a mechanism.** `attacker.py:552-562` stores `mtd.get_resource_type()` and discards the available `mtd.get_name()`. The substrate's own `AttackStatistics` *does* carry the name (`attack_statistics.py:16`) | measured (6 seeds: network 144, application 114; no mechanism breakdown recoverable) | **Makes the unseparated pairs unfalsifiable in the movement arm** — CTS/IPShuffle and OSD/SD are indistinguishable *by construction of the record* |
| A7 | **The confusion penalty is charged to no record row.** ~10 % of the simulated horizon is spent in `apply_mtd_interrupt_cost` and appears in no `attack_record` row | measured | Invisible to every record-derived metric, on both arms |

**A6 is the one to fix first**, and not because it is the largest. It is the
*instrument*: until an interrupt can be attributed to a mechanism in the movement
arm, none of A1–A5 can be measured per mechanism, and the class-level pricing
model cannot be verified rather than assumed. It is also a pure record-schema
widening with no behaviour change — no golden moves, no attacker state added.

## 4. Two scheduler effects that reach both arms, and bias within a class

Both measured; both mean a mechanism's *trigger frequency* is not equal to its
sibling's, which the class-level model implicitly assumes.

- **The priority queue gives the higher-priority member of each class pair a
  systematic extra firing.** Both class pairs share a capacity-1 SimPy resource;
  because `env.process(...)` defers the request, the occupancy check never sees
  the just-spawned sibling, so contention resolves FIFO in priority order.
  Measured **identically in every one of six movement seeds**: OSDiversity 13 ·
  CompleteTopologyShuffle 13 · ServiceDiversity 12 · IPShuffle 12; natively 80 vs
  70. Seed-invariant, with no defence basis, and it runs **counter** to the
  unseparated-pair finding — it would tend to separate each pair spuriously in
  favour of the higher-priority member.
- **Near-deterministic durations phase-lock which verb each mechanism
  interrupts.** `exponential_variates(loc, scale)` is a *shifted* exponential and
  every call site passes `scale=0.5`, giving CV ≈ 0.001–0.03 against the CV = 1.0
  the lineage specifies. Under `simultaneous` the interrupt victim is degenerate —
  CTS → SCAN_PORT 69/70, IP Shuffle → EXPLOIT_VULN 67/70, Service Diversity →
  SCAN_PORT 70/70 — so *what a mechanism costs the attacker* is decided by
  duration arithmetic and queue position rather than by the defence idea. Diffuse
  under `random`/`alternative`, which is the control that proves it is the
  schedule.

## 5. Recommended approach

**Part A — instrument, then measure. No semantics change.**

1. **Widen `MovementRecord` to carry the interrupting mechanism's name** beside
   its resource class (A6). Schema-only; the value is already in hand at the
   assignment site. Follows the suite's own rule that a schema widening needs
   justification — this is it: without the field the class-level model is
   unfalsifiable on the arm the headline uses.
2. **Build the (mechanism × verb × driving mode) truth table** — for each cell:
   does a trigger interrupt, what does it cost, what state is lost, what signal
   reaches the controller. Verify the load-bearing rows with the unified tracer,
   which was built for exactly this.
3. **Measure realised channel traffic per mechanism, per arm**, from the recorded
   runs first: interrupt counts, penalty time, discard/suspension rates. This
   converts "class-flattening" from a structural claim into a measured one.
4. **Quantify the net of A1–A5**, which is the question that actually matters:
   A1/A2 bias against the diversity family and A4 biases toward it. Report the
   net per mechanism. *Do not assume they cancel.*
5. **Classify each asymmetry** — wiring defect (repair), mapping policy (document
   as a chosen input parameter), or documented model (the S3-R declines, which
   are settled and must not be re-opened).

**Part B — repair only what is dispositioned**, D-05 procedure, regression test
pinning the truth table.

## 6. Validation gate

1. The truth table exists as an implementation record, live-verified, with
   realised per-mechanism traffic from recorded runs — **for both arms**.
2. Every one of A1–A7 and §4's two scheduler effects carries a verdict and, where
   it is a defect, a disposition and a fix under D-05.
3. The net bias of A1–A5 is **measured per mechanism**, not argued.
4. A statement, in `metrics_semantics.md` terms, of what class-level pricing means
   for the reported comparison — the reporting consequence of Marc's ruling.

## 7. Hard constraints

- **The disruption model is inherited and settled.** Class-level pricing is the
  documented model per Marc's ruling. Do not redesign it, do not add a
  mutation-scope term, do not re-tune PENALTY. The job is fidelity of *wiring*.
- **The defence must not know which attacker it faces.** That is the acceptance
  criterion for every repair: after it, the channel behaves identically under both
  driving modes, or the difference is a named mapping policy.
- Channel changes touch both arms and every golden — no change without a
  disposition, the D-05 procedure, and a stated comparability boundary.
- SIM-05 determinism; no recorded experiment re-run; §c classification before any
  "bug" verdict.
- Australian English; branch per session; commit locally; **never push**.

## 8. Reading list

- [`../implementation/attacker_read_surface.md`](../implementation/attacker_read_surface.md)
  §(m3) — where A1–A7 were found and routed here; §(b) for why two of the four
  mechanisms depend on these channels entirely.
- [`../implementation/mtd_write_surfaces.md`](../implementation/mtd_write_surfaces.md)
  — the write side, and the purview/fairness table this completes.
- `mtdnetwork/operation/mtd_operation.py` (`_interrupt_adversary` 211-258;
  scheduling 75-160), `mtdnetwork/operation/attack_operation.py`
  (`apply_mtd_interrupt_cost` + `_handle_interrupt` 161-249; `step()`'s
  interrupt path 743-770).
- `src/mtdsim/l3_simulation/movement/attacker.py` (`_pay_interrupt_cost` 543-562,
  the dwell process 598, the long-lived registration 318-319) and
  `controller/verdict.py`.
- [`../implementation/mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md)
  IS-INT-01..07; the audit's §f rows and D-07.
- [`../implementation/trace_tool.md`](../implementation/trace_tool.md) — the
  three-layer view this boundary was built to expose.

## 9. Out of scope

- **Redesigning disruption semantics.** Settled by Marc's ruling.
- Network-state couplings (boundary review 1's record, closed) and mechanism
  write sets (review 2's record, closed).
- Wiring `observed_changes` — that is the axis-8 proof of concept's job, tracked
  separately.
- The Tay AI defender's reactive path (deferred to the ablation phase).
- Dissertation prose.
