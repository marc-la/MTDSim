---
status: open
created: 2026-08-11
---

# Design a strategic-objective layer for the movement attacker — `movement_general` (frontier discipline) and `movement_targeted` (located objective) — to cure the out-of-order-FSM churn independently of the tactic net

## State of play

The movement (profiled) attacker is **comparatively worse than the inherited FSM
attacker, and the cause is now dissected** ([`../implementation/pipeline/ogasp/exploit_learning_findings.md`](../implementation/pipeline/ogasp/exploit_learning_findings.md)
§c). Same network, 15 000 t/u, no MTD: the native FSM reaches **41/50 hosts at 0%
churn and terminates**; the movement attacker reaches **3–9 at 89% re-compromise
churn** and does not. It wastes nine-tenths of its actions re-compromising hosts it
already owns, enumerates ~23 fresh hosts and takes only 3, and under a poorly
aligned mapping (`v1_ckc_total`) it bounces **95% of dispatches** off unmet
preconditions and compromises **nothing**.

The root cause is Marc's framing, confirmed on the code: the inherited attacker is
a rigid **phase-dependency FSM** (`SCAN_HOST → ENUM_HOST → SCAN_PORT →
EXPLOIT_VULN → SCAN_NEIGHBOR`, looping ENUM_HOST to skip hosts it already owns).
The movement layer deliberately **decoupled the six verbs** so a CTI tactic net
could drive succession — but that decoupling **never propagated to the strategic
objective**. Brown's FSM governed *host-selection* through its hardcoded
succession (always advance to a fresh frontier host); the movement layer removed
the succession and left host-selection ungoverned, so it churns.

**The architectural key, verified 2026-08-11:** host-selection lives **entirely in
the substrate verbs**; the movement/controller layer only picks tactics and
*reads* the compromised list (`src/mtdsim/l3_simulation/movement/attacker.py` has
no host-selection seam — it reads `len(adversary.get_compromised_hosts())` for
metrics only). So *which host* and *which tactic* are already separate concerns in
the code. A strategic-objective layer that governs host-selection is therefore
**cleanly independent of the tactic net**, exactly as the proposal requires — and
it is a **different seam from the one that already failed**: the FSM-succession
overlay ([`../implementation/pipeline/ogasp/fsm_succession_overlay.md`](../implementation/pipeline/ogasp/fsm_succession_overlay.md))
tried to align *tactic* order to the FSM and worsened breadth via dwell. The churn
lives at the *host-selection* seam, which that overlay never touched.

This handoff carries **two** objectives to design, both governing host-selection,
both orthogonal to the tactic net.

## Recommended approach

### `movement_general` — frontier discipline (do this first; high-leverage, moderate scope)

Give the general movement attacker the FSM's frontier discipline as a
**substrate-level, objective-gated host-selection policy**: never dwell on an
owned host, always advance to a fresh frontier target. Default-off so the native
attacker and all goldens stay **byte-identical** (the pattern
[`../implementation/pipeline/ogasp/exploit_learning.md`](../implementation/pipeline/ogasp/exploit_learning.md)
established).

- **Hook point:** the substrate host-selection path — `_do_enum_host`'s pop, the
  `host_stack` maintenance in `_do_scan_host` / `_do_scan_neighbors`, and
  `Network.sort_by_distance_from_exposed_and_pivot_host`. The frontier-BFS ordering
  primitive already exists (the sort is distance-from-exposed/pivot, which is what
  "general" wants); the churn comes from compromised hosts re-entering the stack
  (`_do_scan_neighbors` filters `stop_attack` but **not** `compromised_hosts`) and
  from ENUM_HOST landing on owned hosts without the FSM's skip-loop. The minimal
  policy is: **exclude compromised hosts from the selectable stack, and ensure an
  attack verb never runs on an owned `curr_host`** — objective-gated.
- **Why it is the right lever:** the native FSM *proves* frontier discipline
  converts to breadth (41/50 at 0% churn). Restoring it should let the movement
  attacker convert effort to breadth for the first time.
- **What it will not fix:** verb-order precondition-blocking (a mapping-quality
  issue, ~5% at `v2_partial` vs the 89% churn). Out of scope here; the mapping owns
  it.

**Alternative considered and rejected:** fixing the muddle at the tactic layer
(the FSM-succession overlay) — already tried, worsened breadth. The host-selection
seam is the correct one.

### `movement_targeted` — located objective (second; larger, already partly spiked)

A general attacker is indifferent about which host it takes next; a targeted
attacker cannot substitute, so a mutation costs it *progress toward the one thing
it wants* — a **located incentive MTD can act on**, which the declared axis-6
benefit table could only fake. This is the valuable half.

**But it is not a configuration change.** The prior spike
([`../implementation/pipeline/ogasp/targeted_attacker_feasibility.md`](../implementation/pipeline/ogasp/targeted_attacker_feasibility.md),
2026-07-29) found **five construction blockers** — forcing `network_type=0`
*crashes* (target_node stays None → TypeError in `gen_graph`); the shipped geometry
cannot select a target at all (`target_layer=4` but the layer loop reaches only 3);
construction is seed-dependent (the `j==1` subnet condition); plus B4–B5 and a cost
in that record. So `movement_targeted` = **clear those five blockers + build a
target-directed host-selection variant** (the substrate has the primitives —
`get_path_from_exposed(target_node)`, the `target_layer` distance term — so the
sort can be re-keyed toward the target), and **re-enable the commented-out targeted
termination** (`attack_operation.py` ~L714). Read that feasibility record first;
do not re-derive it.

**Honest axis placement (from the prior study, do not quietly upgrade):** a
targeted attacker is **axis-2 evidence** (objective conditioning reaching *which
host*, which axis 2 currently lacks) — axis 2 is already DEMONSTRATED, so this
deepens rather than moves it. It is the *substrate on which an axis-6 claim
becomes possible*, not the claim itself; an axis-6 claim still needs the attacker
to **trade** (e.g. abandon a target whose realised cost outran its payoff — the
give-up rule generalised from a fixed 10 to a cost/benefit comparison).

### The shared design: a strategic × operational objective structure

Both are one idea: restore the **strategic** objective (general = breadth, targeted
= a located host) that Brown had, as a declared host-selection optimiser, composed
with the **operational** CTI objective (exfiltration / impact / c2 / …) that the
model already carries as tactic-flow. Two orthogonal objective axes — strategic
governs *where*, operational governs *what tactics* — reuniting Brown's split with
the CTI contribution. Design the seam once (a host-selection policy on the
adversary/attacker-state, objective-gated) and let both objectives instantiate it.

## Validation gate

Design deliverable (this is a design handoff, not a build): a record
(`movement_objectives_design.md` under `implementation/pipeline/ogasp/`) that pins,
for `movement_general` and `movement_targeted`: the exact host-selection hook, the
objective-gating that keeps goldens byte-identical when off, the composition with
the CTI operational objective, and the re-baseline/re-experiment plan. The design
is done when a build session could start cold from it.

If a build follows: `movement_general` is **shipped** when (i) the general
movement attacker's re-compromise churn falls from ~89% toward the native's ~0%
and its breadth rises materially, (ii) with the objective off, all goldens are
byte-identical and SIM-05 holds, and (iii) **experiment 2 is re-run against the
competent attacker as a Row-B robustness test** — the load-bearing measurement,
because the current ranking inversion may depend partly on the profiled attacker's
incompetence (see Hard constraints). `movement_targeted` is shipped when the five
construction blockers are cleared, a targeted network builds deterministically
across the seed grid, and the target-directed attacker reaches (or measurably
approaches) its located objective.

## Hard constraints

- **Objective-gated, default-off, golden byte-identity.** The native scripted
  attacker and all goldens must stay byte-identical with the objective off. Prove
  it; do not assert it. This is what lets the change land without a forced
  re-baseline — if it can't hold, stop and get Marc's disposition.
- **Row-B risk is the reason to re-run experiment 2, not a footnote.** Making the
  profiled attacker competent moves it toward the native at the *host* level; the
  defence-ranking inversion (Row B, the thesis headline) may weaken or shift. It
  should survive on *tactic-mix* grounds, but that is an empirical question and
  `movement_general` is the strong form of the standing "how much of the inversion
  is corpus vs mapping" test. Treat the re-run as decisive either way: survival
  strengthens Row B; collapse means the inversion was a churn artefact.
- **Honest re-frame required.** This evolves the model from *objective-conditioned
  envelope* to *strategically-optimised + tactically-varied*. The strategic
  optimiser is a **declared added layer**, not CTI-derived — say so. It is arguably
  an upgrade (toward the behavioural rung; answers axis 3's "variety, not
  strategy"), but it is a model evolution, not a tweak.
- **Re-baseline is a Marc disposition**, per the guardrails — a host-selection
  change moves movement behaviour. Do not re-baseline goldens to accommodate it
  without an explicit ruling; the default-off gate is what avoids it.
- **`movement_targeted` inherits IS-SCN-06:** Zhang refactored only Scenario 1 into
  the time domain; the targeted scenario has **no time-domain spec**. Building it is
  a deliberate extension beyond the documented lineage — record it as such, never as
  a fidelity restoration.
- Branch / commit / never-push rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md). Australian
  English.

## Reading list

- [`../implementation/pipeline/ogasp/exploit_learning_findings.md`](../implementation/pipeline/ogasp/exploit_learning_findings.md)
  §c — the churn/out-of-order diagnosis and the native-vs-movement contrast that
  motivate this.
- [`../implementation/pipeline/ogasp/targeted_attacker_feasibility.md`](../implementation/pipeline/ogasp/targeted_attacker_feasibility.md)
  — the five construction blockers and the axis placement for `movement_targeted`.
  Do not re-derive it.
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  — the six verb cores; `_do_enum_host` (the pop + give-up), `_do_scan_host` /
  `_do_scan_neighbors` (host_stack maintenance; note `_do_scan_neighbors` does not
  filter `compromised_hosts`), the commented-out targeted termination (~L714).
- [`../../mtdnetwork/component/network.py`](../../mtdnetwork/component/network.py)
  — `sort_by_distance_from_exposed_and_pivot_host`, `get_path_from_exposed`,
  `network_type`/`target_node`/`target_layer` (the targeted scaffolding).
- [`../implementation/pipeline/ogasp/fsm_succession_overlay.md`](../implementation/pipeline/ogasp/fsm_succession_overlay.md)
  — the tactic-layer attempt that failed; read it to see why the host-selection
  seam is the right one instead.

## Out of scope (explicitly)

- Fixing verb-order precondition-blocking — that is the tactic→verb mapping's
  concern, and it is minor at `v2_partial`.
- Re-imposing the FSM's tactic succession on the movement layer — tried, worse.
- Any base-capability "stretch" (lowering `VULN_MIN_COMPLEXITY` to make a mechanism
  show) — ruled out as reverse-fitting.
- Building either objective in this handoff — it is a **design** brief. The build is
  a separate, gated step.
