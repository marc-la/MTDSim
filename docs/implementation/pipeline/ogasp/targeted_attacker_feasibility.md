---
status: durable
created: 2026-07-29
topic: "Feasibility study — can Brown's targeted attacker (Scenario 2) be run on the time-domain substrate, and would binding it to the GASP operational objectives demonstrate criterion axis 6? Records what incentive rationality actually is, why the targeted attacker is axis-2 evidence rather than axis-6 evidence, the five construction blockers found by spike (the targeted network is not merely unexercised — it is not constructible), and the one measured result that makes the direction worth pursuing anyway."
updated: 2026-07-29
---

# The targeted attacker — feasibility study

**Status:** feasibility study, commissioned by Marc 2026-07-29 after the axis-6
utility modulator was shown to be a static reweighting incapable of responding
to MTD ([`incentive_rationality.md`](incentive_rationality.md) §6.3, and the
collapse test in §2 below). The question put: *would running Brown's targeted
attacker instead of the general one — with the attack objective made
configurable and bound to the GASP operational objectives — demonstrate
incentive rationality in a proof-of-concept sense?*

**Short answer, in three parts.** (1) It is **not** primarily axis-6 evidence —
the criterion already files Brown's scenarios under axis 2, and Brown's targeted
attacker contains no cost/benefit reasoning; on one reading it is *less*
cost-rational than the general one. (2) It is nonetheless the **most valuable
direction identified so far**, because it supplies the one thing the axis-6
mechanism was missing — an incentive *located in the environment*, which MTD can
act on — and because it dissolves the degenerate region that has blocked
success-shaped claims project-wide. (3) It is **not a configuration change**. The
targeted network is not merely unexercised; on the phase-0 geometry it **cannot
be constructed at all**, and construction is seed-dependent for every geometry
tested. Costed at §5.

## 1. What incentive-driven rationality actually is

Cho et al. define the sophisticated attacker as "a rational actor that is
sensitive to incentives, such as attack success with minimum cost" (§V-A). Three
separable components hide in that sentence, and keeping them apart is what makes
the axis tractable:

| Component | What it means | Where this project stands |
|---|---|---|
| **The incentive** | a payoff the attacker values — *what counts as winning* | declared as a benefit table (axis-6 build); **not located anywhere in the environment** |
| **Cost awareness** | a model of what actions cost | the duration catalogue, reused as the cost term — built |
| **Sensitivity** | behaviour *changes* with the payoff/cost structure | built, but as a static function, so it cannot change with anything the defence does |

The axis-6 build did the second and third over a **declared, environment-free**
first. That is why it failed: an incentive that lives in a JSON file cannot be
threatened by a defence that shuffles a network. Brown's general/targeted split
is the first component done properly — the incentive is **structural and
located**: Scenario 2's payoff sits at a specific host, and the attacker's cost
to reach it is a property of the topology, which MTD mutates.

**This is the crux of Marc's intuition, and it is correct.** A *located* payoff
gives MTD a channel to the attacker's incentive that a declared payoff never
had. A general attacker is nearly indifferent about which host it takes next —
every host is worth the same — so relocating hosts costs it time and nothing
else. A targeted attacker **cannot substitute**, so the same mutation costs it
progress toward the only thing it wants. That asymmetry is mechanically real,
and it is measurable.

## 2. Why the axis-6 build failed, restated (the finding this study starts from)

The utility modulator's factor is `(u(b)/ū)^λ` over declared constants and a
fixed out-set, so it is a lookup table indexed by (profile, source,
destination). Proven, not argued: the factor table was precomputed with no
simulation running and no state object in existence, folded into a plain
overlay, and run with `attacker_state=None` — **30 of 30 runs bit-identical** to
the stateful run (`data/results/axis6_rationality/collapse_test.py`).

So the mechanism is structurally a third static overlay. The MTD condition is
not among its inputs, and no amount of parameter choice could have made it
respond to MTD. The proportional-tax finding (§6.3 of the axis-6 record) is a
true *second* reason, not the first.

**Correction owed to that record:** §6.3 claims the negative "survives the
obvious fix", on the evidence that re-pricing each tactic at its run-averaged
realised cost barely reorders preferences. That tests one candidate fix, not the
space of them, and it was overstated into a general result. Measured here for
contrast, on the unconditioned attacker under `v2_partial`:

| Signal MTD could offer the attacker | Spread across tactics | Survives normalisation? |
|---|---|---|
| cost (confusion penalty ÷ declared dwell) | ~9 % surcharge, near-uniform | **no** — a proportional inflation cancels in a ratio |
| success rate (MTD ÷ no-MTD) | **0.08 → 1.02, a 13-fold spread** | **yes** |

MTD barely touches `lateral-movement` (0.98× success) while nearly erasing
`initial-access` (0.08×) and `execution` (0.10×). The cost channel is closed;
the realised-*success* channel is wide open. That correction stands independently
of whether the targeted attacker is built.

## 3. Which axis does a targeted attacker actually score?

**The criterion already answers this, against the proposal.** Axis 2's
prior-work row states that no paper in the cross-section conditions attacker
behaviour on an operational objective, and that "objectives appear only as
scenario labels (**Brown's general vs targeted scripts**)". The criterion's own
classification of Brown's scenarios is therefore *axis 2, in its degenerate
form*.

Reading the intent spec confirms it. Brown's targeted strategy (IS-SCN-03) is a
fixed three-tier preference — attack the target if found; else prioritise hosts
on the target's level; else move toward that level — with **no cost term and no
trade-off**. And IS-SCN-04 makes it *anti*-cost-rational in the one place it
differs on persistence: the general attacker gives up on a host after ten failed
attempts, while the targeted attacker **never gives up on the target node**.
That is payoff overriding cost without weighing it.

**The honest placement**, stated so it cannot be quietly upgraded later:

- A targeted attacker on its own is **axis 2 evidence** — and specifically the
  kind axis 2 currently lacks, since today's objective conditioning reaches
  tactic mix and dwell but never *which host the attacker goes after*. Axis 2 is
  already DEMONSTRATED, so this strengthens an axis that does not need it.
- The **give-up rule is a genuine, if crude, axis-6 primitive**: "stop spending
  on this host after ten failures" is a cost bound, and the targeted exception is
  a declaration that one payoff outranks that bound. Brown's own framing supports
  it — he observes that fewer attack actions are blocked in Scenario 2 "because
  the total number of hosts compromised in scenario 2 is much smaller to achieve
  the attack goal", which is *attack success with minimum cost* in Cho's exact
  sense. But it is one binary rule, not a decision model.
- The load-bearing point: **a targeted attacker is the substrate on which an
  axis-6 claim becomes possible, not the claim itself.** It supplies the located
  incentive the declared benefit table faked. An axis-6 claim would still need
  the attacker to *trade* — for example, to abandon a target whose realised cost
  has outrun its payoff, which is precisely the give-up rule generalised from a
  fixed count of ten to a cost/benefit comparison.

So: pursue it for what it is, and do not book it against axis 6 on arrival.

## 4. Feasibility — five blockers, found by spike

The proposal assumed existing infrastructure plus a configuration change. It is
not that. Evidence is from reading and from running, both recorded.

**B1 — the targeted network cannot be constructed on the phase-0 geometry.**
`Network.__init__` hardcodes `network_type = 1`. Forcing it to 0 does not
produce a targeted network; it produces a **crash**. Target selection fires only
at `i == target_layer and j == 1` inside `gen_graph`, and `gen_graph` then
unconditionally executes `self.colour_map[self.target_node] = "red"` for
`network_type == 0`. When selection does not fire, `target_node` is `None` and
graph generation raises `TypeError`.

**B2 — the shipped geometry makes selection impossible even in principle.** The
default `GEOMETRY` sets `target_layer = 4`, but the layer loop index reaches only
`layers - 1 = 3` (`node_per_layer = [5, 19, 15, 11]`). No iteration can ever
satisfy `i == 4`.

**B3 — construction is seed-dependent for every geometry, because of the `j == 1`
condition.** The target is taken from *subnet index 1* of the target layer, so a
target layer that generates only one subnet on a given seed silently fails
selection and then crashes at B1. Measured over three seeds, phase-0 geometry:

| `target_layer` | constructed | target nodes seen |
|---|---|---|
| 0 | 0/3 | — |
| 1 | 2/3 | 11, 13 |
| 2 | **3/3** | 26, 33, 37 |
| 3 | 1/3 | 40 |
| 4 | 0/3 | — |

A run matrix built on this would die on a seed-dependent subset of cells. The
condition is the defect: the target should be drawn from the target layer's node
set, not from a subnet index that may not exist.

**B4 — there is no targeted objective, because the termination is commented
out.** In `attack_operation.update_compromise_progress` the block that would set
`target_compromised` and fire `end_event` for a targeted network is commented
out. `TimeNetwork.is_compromised()` overrides the parent with the NCR ratio and
never consults `is_target_compromised()`, which exists and is **called from
nowhere in the repo**. The only live objective for both arms today is *compromise
80 % of the network* — including for the movement attacker, whose
`reached_objective` is exactly that flag. **A profile's operational objective has
no connection whatsoever to what the simulator counts as success.**

**B5 — the targeted *strategy* has no live code path.** Turning `network_type`
on would give a target node, attack-path-exposure recomputation, and give-up
protection for the target. It would **not** give an attacker that pursues the
target: host choice is `sort_by_distance_from_exposed_and_pivot_host` (nearest
from exposed/pivot, plus a random tiebreak) for every scenario, and Brown's
same-level / toward-the-level preference (`get_host_id_priority`, `tag_priority`)
is never called from the attack chain. The conformance audit already records this
as vestigial. **The targeted attacker's defining behaviour has to be written, not
switched on.**

One thing that is *not* a blocker, and is an asset: the four MTD strategies'
`network_type == 0` branches only recompute attack-path exposure. They do not
change what the defence does, so turning targeting on does not perturb the
defence side.

### 4b. A latent trap worth recording separately

Because `target_node` is `None` in every run to date, `get_path_from_exposed`
falls into a bare `except: pass` and `attack_path_exposure()` returns a
degenerate **1.0**. With a real target node it returns a meaningful value (0.963
for target 49 on seed 0). Attack-path exposure is one of the four evaluation
metrics the project names as mattering, and it is currently meaningless.

It is **not corrupting any published number** — no experiment code in
`src/mtdsim/` or the results workspaces consumes APE or SAPV; only the
substrate's scorer computes them. So this is a trap for whoever turns it on, not
a live error. Recorded here because a targeted attacker is exactly what would
turn it on.

## 5. What it would buy — the one measured result that justifies the work

The strongest argument for this direction is not conceptual. Measured over seven
seeds at the 15 000 s horizon and the 200 s operating interval, asking whether a
*located* objective discriminates where the NCR objective cannot:

| Arm | condition | hosts compromised | database hosts reached (of 2) | deepest host id |
|---|---|---|---|---|
| baseline | no MTD | 37.4 | **1.43** | 47.1 |
| baseline | random MTD | 13.1 | **0.00** | 24.6 |
| `pure_steal` (movement) | either | 0.3 | — | — |
| `infrastructure_setup` (movement) | no MTD / MTD | 5.4 / 1.0 | — | — |

**This is the finding.** Under the NCR objective, ASR is pinned at zero for every
arm at the operating interval — the degenerate region the rate feasibility study
recorded, which has blocked every success-shaped claim in this project. Under a
*database-targeted* objective the baseline goes from reaching the crown jewels in
most runs to **never reaching them at all**. That is total discrimination, at the
interval the project actually operates at, on a metric that currently
discriminates nothing.

Two honest qualifications, because they bound the claim:

- **The cross-arm contrast would not flatter the movement attacker.** It
  compromises 0.3–5.4 hosts and would essentially never reach a deep target, so
  a database-targeted objective would show it doing *worse* than the baseline,
  not differently-and-interestingly. That is the H-coupling finding again in a
  new metric.
- **The way to make the contrast informative is per-profile objective depth**, which
  is also the route with literature backing: Brown sweeps target depth (`TX`, the
  target in the Xth layer) as an experimental variable. Bind
  `infrastructure_setup` to a shallow objective (C2 established on any
  foothold — achievable in 1–5 hosts, which the movement attacker *does* reach)
  and `pure_steal` to a deep one (a database host), and the question becomes
  whether MTD's effect scales with objective depth differently for a profiled
  attacker than for the inherited one. That is a real experiment, and it is
  Brown's own design.

## 6. Scope and collision risks

- **Experiment 2 does not authorise this.** Its handoff plans sink-retrace plus
  the defence-family sweep, with arms baseline-vs-profiled; it mentions no
  targeted attacker, and it holds the S2 action-set freeze. A targeted attacker
  is a new arm and needs its own ruling.
- **S2 is the live constraint.** B1–B5 are all *substrate* changes
  (`mtdnetwork/`), which is exactly what S2 freezes and what the movement layer
  has so far avoided touching. This cannot ride on the seam's M7 argument — that
  argument turns on the movement layer being portable and the substrate
  untouched.
- **No objective→substrate-target mapping exists in any document**, and the
  controller mapping says why: exfiltration and impact are declared dwell-only
  because "the substrate has no data — nothing to take, nowhere to send it".
  Binding `pure_steal` to a database host would be the first such mapping, is a
  declared value, and inherits the declared-value discipline in full.
- **Comparability.** The baseline's published numbers are all NCR-objective. A
  located objective is a different success criterion, so nothing cross-references
  without restatement.

## 7. Recommendation

**Worth doing, on a corrected premise, and not as an axis-6 build.**

The premise to correct: this is not "change the objective in config". It is a
substrate repair (B1–B3), a termination decision (B4), an attacker behaviour to
write (B5), and a declared objective→target mapping that does not yet exist.
Call it a substrate capability, then decide separately what it evidences.

Sequenced, cheapest-first:

1. **Repair construction** (B1–B3) — make the target drawn from the target
   layer's node set rather than subnet index 1, and refuse an out-of-range
   `target_layer` loudly instead of crashing later. Small, self-contained, and
   testable without any attacker change.
2. **Rule the objective** (B4) — Marc's call, and it is the load-bearing one:
   does reaching the target end the run, and does the movement attacker's
   `reached_objective` become its *profile's* objective rather than NCR 0.8? This
   is worth taking to Jin alongside the S2 question the seam already owes, since
   both are "may the attacker's own goal be changed" questions.
3. **Then**, and only then, decide whether to write Brown's targeted strategy
   (B5) or to bind the GASP objectives to substrate targets — they are separable,
   and the second is the one that serves this project's thesis.

What I would **not** do: treat the targeted attacker as the axis-6 answer. On the
evidence in §3 it is axis-2 evidence with one crude axis-6 primitive attached.
The axis-6 route that the measurements actually point at is the realised-success
channel in §2 — a utility that conditions on what MTD has *actually* denied the
attacker per tactic, which is the one signal a proportional cost surcharge does
not cancel. That collides with the axis-7 learning modulator (both would read the
same running success estimate) and the boundary needs settling before either is
built on top of the other.

## 8. Evidence

- Collapse test (§2): `data/results/axis6_rationality/collapse_test.py` — 30/30
  bit-identical.
- Success-channel and cost-channel spreads (§2): the axis-6 workspace's
  `mtd_tax_anatomy.py` plus a per-tactic success-rate probe over five profiles ×
  seven seeds.
- Construction blockers (§4): `mtdnetwork/component/network.py` (`network_type`
  init, `gen_graph` target selection and the `colour_map` write),
  `mtdnetwork/component/time_network.py` (`is_compromised` override),
  `mtdnetwork/operation/attack_operation.py` (the commented-out targeted
  termination; the give-up rule and its `is_protected_target` guard),
  `mtdnetwork/component/target_network.py` (`TargetNetwork` extends `Network`,
  not `TimeNetwork`).
- Construction matrix (§4, B3): spike over `target_layer` 0–4 × three seeds.
- Discrimination probe (§5): seven seeds, both MTD conditions, baseline and two
  movement profiles.
- Documentation side: intent spec IS-SCN-01..04 and IS-SCN-06/IS-CFL-04
  (targeted scenario has no time-domain spec), `mtdsim_spec.md` NET-17 / ATK-07 /
  the scenario-coverage table, `intent_conformance_audit.md` IS-SCN-01..03,
  `apt_model_criterion.md` axis 2's prior-work row.
