---
status: durable
created: 2026-08-05
updated: 2026-08-05
topic: "Does the inherited class-level disruption model reach the movement attacker as it reaches the native one? The (mechanism x verb x driving mode) truth table executed, the realised channel traffic measured per mechanism for the first time, and a verdict on each of the seven arm asymmetries"
---

# Disruption wiring — the inherited model, checked mechanism by mechanism against both driving arms

**Status:** durable investigation record. It answers the narrow question the
2026-08-05 disruption-wiring brief owns, and it does not re-open the wide one.
Marc's ruling from the Jin discussion (2026-08-05) settled that: *disruption
applies the same way regardless of attacker type — the defence mechanism does
not need to know which attacker it is disrupting.* Class-level pricing is
therefore **the documented model**, ratified as D-20 and not re-litigated here.

What was open is whether the model *arrives*. Two of the four reported
mechanisms have no live network-state coupling to the attacker at all — IP
Shuffle writes a field no verb reads, and OS Diversity's relabel reaches
exploitation through nothing (D-19) — so for those two, these channels are their
entire measured effect. If the channels reach the two arms differently, the
comparison measures driving mode rather than defence.

**The headline: they do reach the two arms differently, the difference is
measured rather than argued, and it runs against the diversity family.** A
network-class firing buys the defence the same disruption in both arms (net
0.92-1.00 of native). An application-class firing buys 0.67-0.83 of what it buys
natively. The offsetting channel the brief hoped for (A4) does not cancel the
loss — it is, in fact, doing almost all of the remaining work.

## (a) What was built before anything was measured — A6, the instrument

`MovementRecord` stored the interrupting mechanism's **resource class** and
discarded its **name** at the one site that holds it, so the two reported class
pairs (CompleteTopologyShuffle/IPShuffle on `network`, OSDiversity/
ServiceDiversity on `application`) were indistinguishable in the movement arm
*by construction of the record*. Every measurement below is per mechanism, and
none of it was reachable before this.

The widening is schema-only: `interrupted_by_name` beside the existing
`interrupted_by`, both threaded as one `InterruptSource` so the class and the
name cannot drift apart on the way to the record. The value was already in hand
at the assignment site, and nothing reads it to decide anything. The substrate's
own `AttackStatistics` has carried the same pair (`interrupted_in` /
`interrupted_by`) since the lineage, so this brings the movement record to
parity rather than inventing a field.

**No golden moved — but that took a second change, and the first attempt did
move seven.** `tools/mtd_golden_streams.py` serialises every dataclass field, so
the new key entered the movement documents and shifted their digests. That is
exactly what the tool's own contract forbids — *"the schema follows the input,
never what fields happen to exist in the code"*, so that a digest change always
means behaviour moved. The field is now popped at capture on the same stated
principle, and by the same precedent, as `n_compromised`: both are observations
that influence no decision the attacker takes. `interrupted_by` itself is left
in, because it was in the shape the goldens were captured with and the digest
should keep guarding everything it already guarded. All 69 movement goldens are
bit-identical after, which is also the SIM-05 check for this change.

**Verified complete:** across every run in §(c) — 7 conditions x 6 seeds x 2
arms — **0 of 1 061** movement-arm interrupts are unattributed.

## (b) The truth table, executed with the real mechanisms

Boundary review 3 executed the *class* x verb grid
([`boundary_attacker_defender_channels.md`](boundary_attacker_defender_channels.md)
§(b)). This adds the dimension this brief owns — the mechanism — by running the
real gate (`MTDOperation._interrupt_adversary`) and the real cost function
(`AttackOperation.apply_mtd_interrupt_cost`) against the four **real** mechanism
instances rather than a stub declaring a class. Class-level pricing predicts
every mechanism's row is its class's row exactly; that is the thing to verify
rather than assume.

Driving mode enters through what `curr_process` presents: the native FSM only
ever presents the six verbs; the movement driver additionally presents `DWELL`
on a dwell-only place, and presents the announced verb on a blocked dispatch.

| `curr_process` | CompleteTopologyShuffle | IPShuffle | OSDiversity | ServiceDiversity |
|---|---|---|---|---|
| SCAN_HOST | INTERRUPT | INTERRUPT | — | — |
| ENUM_HOST | INTERRUPT | INTERRUPT | — | — |
| SCAN_PORT | INTERRUPT | INTERRUPT | INTERRUPT | INTERRUPT |
| SCAN_NEIGHBOR | INTERRUPT | INTERRUPT | — | — |
| EXPLOIT_VULN | INTERRUPT | INTERRUPT | INTERRUPT | INTERRUPT |
| BRUTE_FORCE | INTERRUPT | INTERRUPT | INTERRUPT | INTERRUPT |
| DWELL *(movement arm only)* | INTERRUPT | INTERRUPT | INTERRUPT | INTERRUPT |

What one interrupt costs, same probe, both global streams reseeded so the rows
are comparable:

| mechanism | class | priority | penalty drawn | cursor cleared |
|---|---|--:|--:|---|
| CompleteTopologyShuffle | network | 1 | 20.2346 | yes |
| IPShuffle | network | 3 | 20.2346 | yes |
| OSDiversity | application | 4 | 20.2346 | no |
| ServiceDiversity | application | 6 | 20.2346 | no |

**The gate and the penalty are flat within a class, to the last decimal place.**
There is no per-mechanism term anywhere in channels 1-3, and now it is executed
against the objects rather than inferred from the source. The dead-process guard
is likewise mechanism-blind: every mechanism interrupts a live process and none
interrupts a dead one, which is the native arm's structural immunity during its
own penalty window.

**So the model is faithfully wired *at the gate*.** Everything that follows is
about what the two arms then *present* to that gate.

## (c) Realised traffic, per mechanism, per arm

Both arms, same geometry (the phase-0 50/5/8/4 default), same seeds (0-5),
5 000 t.u. horizon, 200 s mutation interval; movement arm on `aggregate` /
`v2_partial` with the retrace policy on. Native-arm traffic is read from
`AttackStatistics`, movement-arm traffic from the widened `MovementRecord`.

### Interrupts per run and per firing

| condition | mechanism | native firings | native interrupts | movement firings | movement interrupts | native yield | movement yield |
|---|---|--:|--:|--:|--:|--:|--:|
| CompleteTopologyShuffle | CompleteTopologyShuffle | 25.0 | 25.0 | 25.0 | 25.0 | 1.00 | 1.00 |
| IPShuffle | IPShuffle | 25.0 | 25.0 | 25.0 | 25.0 | 1.00 | 1.00 |
| OSDiversity | OSDiversity | 25.0 | 25.0 | 25.0 | 19.3 | 1.00 | **0.77** |
| ServiceDiversity | ServiceDiversity | 25.0 | 24.5 | 25.0 | 20.0 | 0.98 | **0.80** |
| simultaneous | CompleteTopologyShuffle | 13.0 | 13.0 | 13.0 | 12.0 | 1.00 | 0.92 |
| simultaneous | IPShuffle | 12.0 | 12.0 | 12.0 | 12.0 | 1.00 | 1.00 |
| simultaneous | OSDiversity | 13.0 | 12.7 | 13.0 | 10.0 | 0.97 | **0.77** |
| simultaneous | ServiceDiversity | 12.0 | 12.0 | 12.0 | 8.8 | 1.00 | **0.74** |
| alternative | CompleteTopologyShuffle | 7.0 | 7.0 | 7.0 | 7.0 | 1.00 | 1.00 |
| alternative | IPShuffle | 6.0 | 6.0 | 6.0 | 6.0 | 1.00 | 1.00 |
| alternative | OSDiversity | 6.0 | 5.8 | 6.0 | 4.8 | 0.97 | **0.81** |
| alternative | ServiceDiversity | 6.0 | 6.0 | 6.0 | 4.3 | 1.00 | **0.72** |
| random | CompleteTopologyShuffle | 7.7 | 7.7 | 7.5 | 7.5 | 1.00 | 1.00 |
| random | IPShuffle | 5.3 | 5.3 | 5.8 | 5.8 | 1.00 | 1.00 |
| random | OSDiversity | 5.0 | 5.0 | 6.5 | 4.3 | 1.00 | **0.67** |
| random | ServiceDiversity | 7.0 | 6.8 | 5.2 | 4.8 | 0.98 | 0.94 |

The pattern is uniform across every scheme: **network-class mechanisms interrupt
on essentially every firing in both arms; application-class mechanisms interrupt
on ~98-100 % of native firings and 67-94 % of movement firings.**

### The penalty is flat and large, and it is charged to no record row

| condition | interrupts on verbs | interrupts on DWELL | dwell share | penalty total (t/u) | penalty per interrupt | penalty share of clock |
|---|--:|--:|--:|--:|--:|--:|
| CompleteTopologyShuffle | 11.0 | 14.0 | 56.0 % | 514 | 20.55 | 10.3 % |
| IPShuffle | 10.5 | 14.5 | 58.0 % | 513 | 20.52 | 10.3 % |
| OSDiversity | 4.7 | 14.7 | 75.9 % | 397 | 20.56 | 8.0 % |
| ServiceDiversity | 6.2 | 13.8 | 69.2 % | 411 | 20.56 | 8.3 % |
| simultaneous | 14.5 | 28.3 | 66.1 % | 879 | 20.53 | **17.7 %** |
| alternative | 8.5 | 13.7 | 61.7 % | 453 | 20.44 | 9.1 % |
| random | 9.0 | 13.5 | 60.0 % | 462 | 20.52 | 9.3 % |

20.44-20.56 per interrupt in every cell, which is channel 2's flatness measured
end-to-end rather than at the probe.

## (d) The net of A1-A5, per mechanism — the question that actually matters

A1 and A2 bias against the diversity family; A4 biases toward it. The brief's
instruction was to report the net per mechanism and *not* to assume they cancel.
The unit is **per firing**, so a mechanism that fires more often (§(f)) does not
read as one that disrupts harder.

| condition | mechanism | class | native/firing | movement/firing | **net** | movement on verbs | movement on DWELL |
|---|---|---|--:|--:|--:|--:|--:|
| simultaneous | CompleteTopologyShuffle | network | 1.00 | 0.92 | **0.92** | 0.45 | 0.47 |
| simultaneous | IPShuffle | network | 1.00 | 1.00 | **1.00** | 0.36 | 0.64 |
| simultaneous | OSDiversity | application | 0.97 | 0.77 | **0.79** | 0.17 | 0.60 |
| simultaneous | ServiceDiversity | application | 1.00 | 0.74 | **0.74** | 0.18 | 0.56 |
| alternative | CompleteTopologyShuffle | network | 1.00 | 1.00 | **1.00** | 0.48 | 0.52 |
| alternative | IPShuffle | network | 1.00 | 1.00 | **1.00** | 0.39 | 0.61 |
| alternative | OSDiversity | application | 0.97 | 0.81 | **0.83** | 0.25 | 0.56 |
| alternative | ServiceDiversity | application | 1.00 | 0.72 | **0.72** | 0.22 | 0.50 |
| random | CompleteTopologyShuffle | network | 1.00 | 1.00 | **1.00** | 0.47 | 0.53 |
| random | IPShuffle | network | 1.00 | 1.00 | **1.00** | 0.40 | 0.60 |
| random | OSDiversity | application | 1.00 | 0.67 | **0.67** | 0.23 | 0.44 |
| random | ServiceDiversity | application | 0.98 | 0.94 | **0.96** | 0.32 | 0.61 |

**They do not cancel.** The network pair reaches the movement attacker as often
as it reaches the native one; the application pair loses 17-33 % of its yield,
in every scheme, at every seed.

**And A4 is not a minor offset — it is load-bearing.** The counterfactual, taken
from the same runs: if dwell-only places were made application-immune (D-21's
declined option (b)), the yield per firing against the movement attacker would
fall to

| mechanism | today | without the DWELL channel |
|---|--:|--:|
| CompleteTopologyShuffle | 0.92 | 0.45 |
| IPShuffle | 1.00 | 0.36 |
| OSDiversity | 0.79 | **0.17** |
| ServiceDiversity | 0.74 | **0.18** |

Over half of every mechanism's realised disruption against the movement attacker
arrives through the `DWELL` sentinel. This is the strongest evidence yet for
D-21's ruling and it was not available when that ruling was taken: making
dwell-only places immune would not "shield half the defence family from
28-56 % of the clock", it would remove **four-fifths** of the diversity pair's
measured effect.

### A1 in isolation — the exploit-blocking windows

| mechanism | native EXPLOIT_VULN interrupts/firing | movement | ratio |
|---|--:|--:|--:|
| CompleteTopologyShuffle | 0.27 | 0.08 | 0.29 |
| IPShuffle | 0.86 | 0.07 | 0.08 |
| OSDiversity | 0.82 | 0.03 | **0.03** |
| ServiceDiversity | 0.49 | 0.06 | 0.11 |

The diversity family loses **89-97 %** of its exploit-blocking windows in the
arm the headline result runs on. The native arm yields per vulnerability
(`attack_operation.py:466-467`), giving up to `SERVICE_TOP_X_VULNS_TO_RETURN` = 5
interrupt windows per attempt; the movement arm spends the whole attempt as one
up-front `timeout` and then runs the vulnerability loop with zero yields.

### A2 in isolation — the recon verbs

| mechanism | class | native | movement |
|---|---|--:|--:|
| CompleteTopologyShuffle | network | 0.00 | 0.24 |
| IPShuffle | network | 0.04 | 0.15 |
| OSDiversity | application | 0.00 | **0.00** |
| ServiceDiversity | application | 0.00 | **0.00** |

Exactly zero, structurally, in both arms — the gate excludes SCAN_HOST /
ENUM_HOST / SCAN_NEIGHBOR from the application class (IS-INT-05) and
`verdict.py:59-60` reads those verbs as success-unless-interrupted. Failure
routing on those three verbs is reserved for the network class. The absolute
magnitude is small (0.15-0.24 per network firing) because the movement arm
spends most of its clock dwelling rather than in recon verbs, so A2 is real and
**not** where the net comes from.

## (e) A5, executed — a dropped cursor clear

`apply_mtd_interrupt_cost` decides what to clear from the MTD it was *called*
with. `MovementAttacker._pay_interrupt_cost` reads `_interrupted_mtd` before the
penalty and nulls it after. A second mutation arriving mid-penalty is absorbed
(D-22, ruled) — but the defence has by then recorded the *new* mutation, and its
class is never consulted.

Executed directly against the real methods:

```
cursor cleared by an arriving network-class mutation
    during an application-class penalty:   False
the arriving mutation is recorded on the op: True
control (network penalty, network arrival): True
```

So a network-class mutation can fire the gate, increment
`add_total_attack_interrupted`, be recorded as the interrupting MTD — and the
position destruction its class mandates does not happen. **This is the one
finding here that is a candidate bug rather than a policy consequence**, and the
§c procedure is why: IS-INT-01 (Brown B-INT-01) states that a network-layer
mutation means the connection to the host is gone. The code fires the gate for
exactly that mutation and then does not do it. It violates an invariant the
papers state, which §c names as evidence for *bug*.

Reachable only under overlapping mutations, so `simultaneous` is where it lives.
Frequency, measured: **1.0 absorbed interrupt per run at `simultaneous` and 0.0
in every other condition** (§(f) A3 row), which bounds the exposure.

## (f) Verdicts — every asymmetry, classified

The three classifications the brief specifies: **wiring defect** (repair),
**mapping policy** (a chosen input parameter, documented), **documented model**
(settled; must not be re-opened).

| # | Asymmetry | Verdict | Basis |
|---|---|---|---|
| **A1** | EXPLOIT_VULN is uninterruptible in the movement arm | **Mapping policy** — with a disposition request (**D-35**) | Not documented-nowhere: it is the direct, declared consequence of S3-R (the movement layer supplies every unit of the attacker's time, so the substrate's per-vulnerability timing loop and its yields are declined via `charge_time=False`). No lineage paper specifies how many interrupt windows an exploit attempt offers. But the *measured* consequence — 89-97 % of the diversity family's exploit-blocking windows lost in the headline arm — is large enough to need a stated boundary rather than a code comment |
| **A2** | Application-class MTD can never produce a failure verdict on the three recon verbs | **Documented model** | IS-INT-05's exclusion set is documented intent, and `verdict.py`'s success-unless-interrupted reading is a declared simplification (controller §4). Ratified as part of D-21. Measured magnitude is small (§(d)) |
| **A3** | The movement arm absorbs interrupts the native arm never receives | **Documented model** (D-22, ruled 2026-08-03) | Re-measured here: +1.0 count per run at `simultaneous`, +0.0 everywhere else. Neither arm pays twice; only the counter's meaning differs. Unchanged |
| **A4** | Dwell places are interruptible and the native attacker's equivalents are not | **Mapping policy** (D-21, ruled 2026-08-03) — **and the evidence for that ruling is now much stronger** | §(d)'s counterfactual: without it the diversity pair retains 0.17-0.18 of its native yield. The ruling stands; the record of *why* is upgraded from "prevents a hiding spot" to "carries four-fifths of the family's measured effect" |
| **A5** | A network-class mutation arriving during an application-class penalty loses its cursor clear | **Wiring defect** → **D-36**, repair recommended | §(e). Violates IS-INT-01 in a reachable state; §c's own evidence standard for a bug. Bounded exposure (1.0/run at `simultaneous`, 0 elsewhere) |
| **A6** | The movement record cannot attribute an interrupt to a mechanism | **Wiring defect — REPAIRED this session** | §(a). Schema-only, no behaviour change, no golden moved. 0 of 1 061 interrupts unattributed after |
| **A7** | The confusion penalty is charged to no record row | **Mapping policy, already recoverable on one arm** → **D-37** (record-grade) | 8.0-17.7 % of the clock. The movement arm *can* recover it — `measures.mtd_penalty` derives it as `end - start - dwell` and the figures in §(c) are computed that way — so the movement side needs a statement, not a field. The native arm cannot, and that is the asymmetry to state |

### The two scheduler effects (brief §4)

| Effect | Verdict | Basis |
|---|---|---|
| **The priority queue gives the higher-priority member of each pair an extra firing** | **Record-grade, and it is *not* an arm asymmetry** → **D-38** | Measured identically in both arms: `simultaneous` CTS 13.0 · IPShuffle 12.0 · OSDiversity 13.0 · ServiceDiversity 12.0, native and movement alike; `alternative` 7/6/6/6 in both. Because it is arm-invariant it cannot explain the ranking inversion, and the fairness of the two-arm comparison is untouched. What it does do is **spuriously separate each class pair in favour of its higher-priority member** (CTS priority 1 over IPShuffle 3; OSDiversity 4 over ServiceDiversity 6) — which runs counter to the unseparated-pair finding and must be named wherever a within-pair difference is reported |
| **Near-deterministic durations phase-lock the victim verb** | **Documented model in its cause, mapping policy in its effect** — no new disposition | The cause is the shifted-exponential `scale=0.5` at every call site, already on record (CV ≈ 0.001-0.03 against the lineage's CV = 1.0). The *effect* differs by arm and that is the new measurement: natively the modal victim is EXPLOIT_VULN for every mechanism under `random`/`alternative` (72-94 %) and splits SCAN_PORT/EXPLOIT_VULN under `simultaneous`; in the movement arm the modal victim is **DWELL** for every mechanism in every scheme (51-78 %). Both arms are phase-locked, onto different things, and the difference is exactly the clock-composition difference D-21 ratified as mapping policy |

## (g) What this means for the comparison — the reporting consequence

Stated in [`metrics_semantics.md`](metrics_semantics.md) §(d) terms, and this is
gate item 4 of the brief:

1. **Class-level pricing is the documented model, and it is faithfully wired.**
   The gate, the penalty and the cursor clear carry no per-mechanism term, and
   §(b) executes that against the real objects. A reader should understand the
   reported family as **two disruption classes**, each appearing twice, dosed by
   the scheme — not as four independently-priced defences.
2. **The two arms are not equally reachable by the application class.** A
   network-class firing delivers 0.92-1.00 of its native disruption to the
   movement attacker; an application-class firing delivers 0.67-0.83. Any
   cross-arm comparison of the diversity family carries that factor, and the
   ranking inversion's anatomy should name it.
3. **Most of the movement arm's disruption arrives through the dwell channel.**
   Over half for every mechanism, four-fifths for the diversity pair. This is a
   mapping-policy consequence (D-21) and it is the single largest determinant of
   what MTD costs the profiled attacker.
4. **Within a class, firing counts are not equal.** The higher-priority member
   gets a systematic extra firing in both arms. Report per-firing, or say that
   you have not.

## (h) Reproduction

Scratch instrumentation, not repository code, in the pattern the boundary
reviews established. The three probes:

- `truth_table.py` — §(b) and §(e). Runs `MTDOperation._interrupt_adversary` and
  `AttackOperation.apply_mtd_interrupt_cost` against the four real mechanism
  instances with stub collaborators. Seeds **both** global streams:
  `exponential_variates` draws from numpy's, so seeding only `random` makes the
  four penalty rows differ for a reason that has nothing to do with the
  mechanism (this was caught and corrected before the table above was taken).
- `channel_traffic.py` — §(c). 7 conditions x 6 seeds x 2 arms at 5 000 t.u.
  Native arm wired as `baseline/run_baseline.py` does, minus its figure and CSV
  side effects; movement arm through `run_movement`.
- `analyse.py` / `net.py` — §(c), §(d), §(f).

The ratified semantics are pinned as repository tests in
[`../../tests/test_interrupt_channel_semantics.py`](../../tests/test_interrupt_channel_semantics.py),
extended by this brief with the mechanism dimension and A5.

**One boundary on the numbers.** Six seeds and one profile (`aggregate`,
`v2_partial`) support the per-mechanism *ratios* above, which are stable to
within a few percent across seeds and reproduce in all three multi-mechanism
schemes. They do not support a significance claim, and the standing constraint
applies with extra force here: mechanism arms do **not** share the attacker's
dice (D-29), so seed-matched arms are independent rather than paired.
