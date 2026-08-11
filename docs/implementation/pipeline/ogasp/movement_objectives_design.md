---
status: partial
created: 2026-08-11
topic: "movement_general / movement_targeted design — the conceptual crux (the objective is a host-selection property, not a tactic-ordering one) and the governance state that licenses shipping the current attacker; build-ready specifics still open"
handoff: 2026-08-11_movement_objectives.md
---

# A strategic-objective layer for the movement attacker — design groundwork

**Status: partial.** This is the design deliverable the
[`movement_objectives`](../../../handoffs/2026-08-11_movement_objectives.md)
handoff commissions, at the conceptual-and-governance stage. What is settled here:
*where* the objective lives, *why* the churn happens, the *shape* of the policy,
and the *ruling state* that decides whether any of it must be built before the
write-up. What is **not** yet done to the handoff's bar ("a build session could
start cold from it"): the exact hook lines, the byte-identity proof for the
default-off gate, the composition detail, and the re-baseline/re-experiment plan.
Those are enumerated in §7. Everything above §7 is the workshop output of
2026-08-11.

## 1. The crux: the objective is a *host-selection* property, not a tactic-ordering one

The baseline FSM's objective (breadth / frontier progression) reads as "emergent
from the verb ordering", but that framing hides a false step. Mechanically the
objective is produced by **host-selection**, which the FSM merely *expresses
through* state transitions — so it wears an ordering costume. The three things
that actually produce frontier discipline are all statements about `host_stack`
and `curr_host`, none about the order SCAN_PORT / EXPLOIT / BRUTE run in:

- `_do_scan_host` builds the queue from uncompromised, reachable hosts sorted by
  distance-from-exposed ([`attack_operation.py:303-335`](../../../../mtdnetwork/operation/attack_operation.py#L303-L335)) — *which hosts are selectable*.
- the ENUM_HOST skip-owned self-loop ([`attack_operation.py:438-440`](../../../../mtdnetwork/operation/attack_operation.py#L438-L440)) — *don't make an owned host the subject*.
- `_do_scan_neighbors` prepends fresh neighbours ([`attack_operation.py:652-661`](../../../../mtdnetwork/operation/attack_operation.py#L652-L661)) — *which hosts enter the frontier*.

**Consequence for the design.** Because the objective lives on the *host* axis and
the movement layer's contribution lives on the *tactic* axis, the two are
orthogonal. Reinstating the strategic objective does **not** touch the tactic net,
and it is a **different seam** from the FSM-succession overlay
([`fsm_succession_overlay.md`](fsm_succession_overlay.md)), which operated on the
verb-state graph (tactic order) and worsened breadth. This seam operates on the
host graph. The three design options the handoff and the workshop weighed —
"minor tweaks", "emergent-regardless-of-ordering", "an independent controller
that instruments the phases" — collapse into one once the objective is located on
host-selection: they are the same policy at the same seam.

## 2. Why the movement attacker churns — structural, not disruption or tempo

The churn is **structural**, measured at 15 000 t/u with **no MTD at all**
([`exploit_learning_findings.md`](exploit_learning_findings.md) §c): native 41/50
at 0 % churn, movement 3–9 at 89 %. So it is not caused by a mutation disrupting
the attacker, and it is not caused by slow tempo. Tempo limits *how far* the
attacker gets (fewer actions in the window); structure sets *what fraction is
wasted* (the 89 %). The FSM-succession overlay already showed that pushing on
tempo/dwell makes breadth worse — a separate lever from this one.

This is also distinct from the **D-28** stale-target problem
(`_do_enum_host` docstring): D-28 was owned hosts *unreachable after a topology
shuffle* surviving in the queue (an MTD-interaction bug, since guarded). The churn
here is re-compromising *reachable owned* hosts with no MTD in play.

**The pivot is not missing — the loop is.** `step()` dispatches ENUM_HOST to the
shared `_do_enum_host` core, which sets `pivot_host_id` for *both* arms
([`attack_operation.py:436`](../../../../mtdnetwork/operation/attack_operation.py#L436)) and
re-keys the distance sort with it. So the movement attacker *has* a pivot pointer.
What it lacks is the tight EXPLOIT(success) → SCAN_NEIGHBOR → ENUM_HOST loop that
makes the pivot mean "advance from here"; and even the pivot's sort is defeated
downstream because `_do_scan_neighbors` returns compromised hosts to the stack
(it filters `stop_attack` but not `compromised_hosts`), which the native
skip-owned loop absorbs and the movement layer does not.

## 3. The policy shape: exclude-owned **and re-select** (not block)

The minimal strategic invariant, checked when a compromise verb is about to run,
independent of what the movement layer selected:

> A compromise verb (SCAN_PORT / EXPLOIT_VULN / BRUTE_FORCE) only ever acts on a
> not-yet-compromised, still-reachable frontier host. Owned hosts leave the
> selectable set; when `curr_host` is exhausted, host-selection **advances** to
> the next frontier target *before* the verb fires.

The "advance" half is load-bearing: a pure **block** (refuse the verb on an owned
host) just trades re-compromise churn for spin churn — the action is spent doing
nothing. Exclude-owned-from-stack **+** re-point-`curr_host`-to-fresh is the pair;
the second half is what turns a guard that stalls into an objective that
progresses, and it is order-independent by construction.

Because it is a guard at execution time (not a property of the sequence),
progression becomes monotone: every compromise verb either takes a fresh host or
advances toward one, and re-compromise is not representable. Breadth termination
(`is_compromised` → `end_event`) then becomes reachable — the reason the movement
attacker "does not terminate" today is only that it churns short of it.

**What this does not fix:** verb-order precondition-blocking (EXPLOIT before
SCAN_PORT), which is the tactic→verb mapping's concern (~5 % at `v2_partial`), a
different failure mode on a different seam.

## 4. Composition — strategic × operational, two orthogonal axes

In this substrate all six verbs are compromise-oriented, so the CTI "operational
objective" is not a set of new verbs; it is the *distribution and timing over the
same six*. Operational governs the tactic histogram (the variety, the
contribution); strategic governs which host (the invariant in §3). They compose
because they touch different state. This reunites Brown's split — his FSM fused
both axes into one verb machine; the movement layer freed the operational axis and
dropped the strategic one; this restores only the strategic one, leaving the model
strictly more expressive than the baseline (baseline-strategic **+**
movement-operational), not a retreat toward it.

## 5. Complete Topology Shuffle interaction — a Row-B confound, not a defeat

Filtering compromised hosts out of the selectable stack does **not** defeat CTS.
CTS shuffles topology/reachability; compromise is persistent (backdoored hosts
stay owned across a shuffle), so excluding owned hosts from *attack selection*
leaves CTS's whole job intact. But it does remove churn that currently *inflates*
CTS's (and every defence's) apparent score — the defence looks effective partly
because it induces re-compromise waste. Removing the churn measures the defence
against a competent attacker for the first time. This is exactly the Row-B risk:
the defence-ranking inversion may weaken or shift.

**Classification (per the bug-vs-design rubric):** the un-filtered
`_do_scan_neighbors` is *not a bug* — in the native FSM it is harmless (the
skip-owned loop absorbs it), so the baseline is correct as written. The policy is
a **declared added layer** (the strategic axis), objective-gated and default-off
so the baseline and all goldens stay byte-identical. Not a fidelity restoration; a
model evolution.

## 6. Governance — what is ruled, and the one thing that is not

The `model_scope_freeze` is **stale as a gate** (axes 6/7 left its perimeter; the
2026-08-11 handoffs reopen things it parked). Do not cite it as authority. Its
load-bearing content survives via the live **2026-08-11 V-trail**
([`supervisor_decision_register.md`](supervisor_decision_register.md) §V1–V7):

- **V5** — the research question is "How does MTD perform against APT attackers?",
  with evaluation benchmarked against the inherited baseline. The weaker attacker
  is the *axis of comparison*, not a defect. This is the current home of the
  freeze's §1 "not a better attacker" sentence.
- **V6** — sensitivity analysis is the *sanctioned regime* for arbitrary
  parameters: sweep min-to-max, "low values mapping to weak-attacker expectations
  and high values to capable-attacker ones". This is the ruling that reaches the
  competence-robustness question — you discharge it by sweeping, **not** by
  rebuilding the attacker.

**The honest gap in V6.** V6 brackets competence *parametrically* (timing / target
durations named). The churn is *structural* — no dwell value switches it off — so a
V6 sweep does not reach it. Therefore:

- if the inversion is robust on **tactic-mix** grounds (experiment 2's
  mapping-sensitivity framing), V6 + that study discharge it — no `movement_general`
  build needed;
- if the churn is **load-bearing** on the inversion, that confound is outside V6,
  and clearing it means the `movement_general` build — which re-opens scoped future
  work and is **not ruled**. That is the single open supervisor question from this
  workshop.

Phase-layer rework as future work (freeze §3 item 4) is uncontested by the
V-trail; it stays future work.

## 7. Remaining design work (to reach the handoff's "start cold" bar)

Not done in this session:

1. **The exact host-selection hook.** Pin the precise lines: the `_do_enum_host`
   pop and skip guard, the `host_stack` maintenance in `_do_scan_host` /
   `_do_scan_neighbors` (the `compromised_hosts` filter), and how the objective
   gate is threaded so both are no-ops when off.
2. **The byte-identity proof for default-off.** Demonstrate (not assert) that with
   the objective off the native FSM and every golden stay byte-identical and
   SIM-05 holds — the gate that avoids a forced re-baseline.
3. **`movement_targeted`.** Read
   [`targeted_attacker_feasibility.md`](targeted_attacker_feasibility.md) first;
   the five construction blockers + the target-directed host-selection variant
   (re-key the sort toward `target_node` via `get_path_from_exposed`) + re-enabling
   the commented-out targeted termination (`attack_operation.py` ~L714). Inherits
   IS-SCN-06 (no time-domain spec for the targeted scenario) — record as extension,
   not restoration.
4. **The re-baseline / re-experiment plan.** Experiment 2 re-run against the
   competent attacker as the Row-B robustness test (§5), gated on Marc's
   disposition since a host-selection change moves movement behaviour and re-opens
   scoped work.

## 8. Positioning note for the write-up

The apparent weakness is a **finding worth claiming**, not an apology: an inherited
FSM attacker *conflates two separable objectives* (strategic host-selection +
operational tactic-flow), and cleanly decoupling the operational axis exposes that
the strategic competence was riding inside the verb order all along. Keep two
things in separate registers: a **model limitation** (shallow penetration; fixable
by future phase-layer work — scopable) versus a **threat to the validity of the
Row-B headline** (the inversion might depend on the churn — *not* fully dischargeable
by a future-work note; it is the §6 open question). Extensibility is a virtue of
the architecture; it does not discharge the validity question about the current
numbers.
