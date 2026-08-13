---
status: durable
created: 2026-08-13
updated: 2026-08-13
topic: "The axis-4 structural-route probe — a reader-only, pre-registered check of whether the terrain in the window after an MTD interrupt systematically rewards any tactic set over the ordinary weights; §1–§8 are the pre-registration, committed before a single record was read"
---

# The axis-4 structural-route probe — does post-interrupt terrain reward anything?

**Status:** durable. **§1–§8 are a pre-registration**: the window definition,
the grid, the statistics, the null, the census gate, the direction clause and
the decision rule were written and committed **before a single record
existed**. The findings are appended below the line in a later commit, against
these criteria and without amending them. The commissioning brief is
`docs/handoffs/2026-08-13_axis4_structural_route_probe.md` (deleted in the
commit that ships whichever record closes it); the standing method is
[`axis_instrumentation_method.md`](axis_instrumentation_method.md).

## 1. What the probe is for

The 2026-08-11 axis-4 disposition
([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d) axis 4)
closed the axis's null advantage as intractable via attacker-blindness on two
of its three routes: **reactive** closed structurally (every defence in the
pool is clocked and attacker-blind), **mechanism-shape** bounded
first-principles (a richer function of the same one-bit verdict has the same
ceiling). The **structural** route — does the blockage an interrupt creates
persist or re-randomise, i.e. does the post-interrupt terrain carry structure
a "pivot-to-recover" kernel could exploit — was explicitly *not pursued*.
Parked is not falsified, and Marc's 2026-08-13 objection is the one an
examiner can raise: the attacker demonstrably *feels* the defence (the ~20 t/u
confusion penalty on every interrupt; the cursor clear on network-class
interrupts; the movement arm's state throw-back), so a declared
recovery-tactic set with a temporary weight-transformation kernel on the
interrupt event is mechanically possible and idiomatic.

The kernel only *pays* if the terrain in the post-interrupt window differs
from elsewhere-in-run in a way a recovery set could match. Precedent says
friction-shaped modulators operate without advantage (axes 6, 7). So the probe
comes first, and the kernel is gated on its result: this probe **informs a
ruling; it does not constitute one**, and the 2026-08-11 disposition stands
until Marc reopens it.

What an interrupt actually destroys, per the executed boundary record
([`../../boundary_attacker_defender_channels.md`](../../boundary_attacker_defender_channels.md)
§(b)): a **network-class** interrupt charges the penalty and clears the host
cursor (position destroyed); an **application-class** interrupt charges the
penalty and clears nothing; owned hosts are never revoked. "Recovery"
therefore honestly means re-acquisition of *position*, and the class split is
carried through every statistic below.

## 2. The question, made precise

**Window.** For each interrupted visit at index *i* in a run's visit stream
(`visit_records`, sequence order), the post-interrupt window is the next
**n = 3** visits (`visits[i+1 : i+4]`), **truncated at the next interrupted
visit** — a window never crosses the following tick, which discharges the
quasi-periodic-trigger caveat structurally (the substrate's trigger is
loc-shifted, `mean + Exp(0.5)`, so ticks are near-evenly spaced; the sibling
axis-8 handoff carries that record). The interrupted visit itself belongs to
no window. n = 3 is chosen from recorded tempo, not from this probe's output:
the recorded experiment-2 aggregates give **7.4 visits per inter-interrupt
gap** on network-class conditions at the 200 s interval (10.5 on
application-class), so n = 3 is well inside the gap where n = 5 would tile
two-thirds of the run and destroy the contrast class. **Sensitivity windows
n = 1 and n = 5** are computed and reported; they carry no decision weight.

**Elsewhere.** Every visit in neither any window nor itself interrupted.
Interrupted visits belong to neither side: they are the conditioning events,
and their verdict is mechanically `failure` by the interrupt-as-failure rule,
so counting them anywhere would manufacture exactly the difference the probe
is testing for.

**Verdict classes.** Over *attempted actions* (records with a dispatched
verb): `success`; `blocked` (precondition unmet); `failure` (failed,
unblocked). Dwell-only visits carry no verdict and enter only the visit-mix
statistic (S1), where thinking is part of the mix.

**The two arms, and what each answers.** The **verdict-blind arm**
(`movement_blind`, the §11 control: an empty overlay value table, factor 1.0
everywhere) routes on base weights alone, so its post-interrupt walk *is* the
ordinary-weights walk — it measures the **terrain**, uncontaminated by any
conditioned response. The **main arm** (`movement`) routes the interrupt as a
failure verdict through the declared failure column — it measures what the
ordinary weights **already do** with the window. The terrain claim is decided
on the blind arm; the main arm is its mirror, reported beside it.

## 3. The grid — a seeded regeneration of experiment-2 arms

Reader-only throughout: no simulation-behaviour change, no new declared
magnitude, no schema change. The runs are deterministic seeded regenerations
under experiment 2's declared inputs
([`experiment_02_findings.md`](experiment_02_findings.md) §2):

| input | value |
|---|---|
| controller mapping | `v2_partial` |
| outcome overlay | `v3_persistent_backward` (blind arm: empty table) |
| sink policy | **`retrace_sinks=True` — the landed S5 implementation** |
| timing regime | S3-R stochastic |
| horizon | 15 000 s |
| geometry | the standard 50-host network |
| seeds | 0–9 |
| intervals | 200 s (operating; decision interval), 2 000 s (secondary) |
| conditions | the four single mechanisms: CompleteTopologyShuffle, IPShuffle (network class); OSDiversity, ServiceDiversity (application class) |
| arms | `movement`, `movement_blind`; modulators null |
| profiles | all five (`aggregate`, `objective_exfiltration`, `objective_impact`, `objective_exfiltration_impact`, `objective_none_c2`) |

2 arms × 5 profiles × 4 conditions × 2 intervals × 10 seeds = **800 runs**.
The `none` condition has no interrupts and nothing to condition on; the multi
schemes mix classes within a run and add nothing the four singles do not give
more cleanly.

**One named divergence from the recorded experiment-2 traces.** The recorded
main matrix ran the pre-reconciliation sink implementation (retrace with no
edge suppression); the landed `retrace_sinks` adds a one-shot suppression of
the edge into the sink, so regenerated traces of the three sink-bearing
profiles diverge from the recorded ones wherever the policy fired — the
reconciliation note in `experiment_02_findings.md` §1 records this, bounds it
(sink in-edge mass ≤ 0.111), and the open re-take ruling rides with it. This
probe runs the **landed** implementation, because the configuration described
must be the configuration measured, and the current code is what any future
kernel would run on. No probe figure is pooled with a recorded experiment-2
figure.

Workspace: `data/results/axis4_structural_probe/` (gitignored, regenerable:
runner, numbers). This record is the tracked account.

## 4. The statistics, the null, and the census gate

All statistics are computed **per cell** — (arm, profile, condition,
interval) — pooling counts across the cell's ten seeds.

- **S1 (visit mix).** JSD (`jsd`, the L2 convention) between the in-window
  and elsewhere tactic-visit distributions over all visits (support: the 15
  tactic-places; dwell-only visits count under their tactic).
- **S2 (joint verdict profile).** JSD between the in-window and elsewhere
  joint (tactic × verdict-class) distributions over attempted actions.
- **S3 (per-tactic reward — the decision statistic).** For each tactic *j*:
  Δ_j = (success share of attempted actions at *j* in-window) − (success
  share at *j* elsewhere). **Rewarded** means Δ_j exceeds the tactic's own
  null ceiling (below) *and* the tactic passes the census gate. The
  definition is deliberately one-sided: on network-class conditions the
  cursor clear mechanically depresses in-window success for host-dependent
  verbs until position is re-acquired, and an elevated in-window *blocked*
  share is that bookkeeping, not exploitable structure — a recovery kernel
  needs a tactic that pays *better* than usual after the tick, not one that
  fails worse.

**The null is measured, not declared — a cyclic time-rotation.** For each
null draw, each run's real interrupt *times* are rotated by a single uniform
offset u ~ U(0, T) modulo the run's termination time T; each rotated time
maps to the visit whose span contains it; pseudo-windows and
pseudo-elsewhere are built by the identical rules (same truncation, same
exclusions) and the identical statistics computed on the pooled cell.
**200 seeded draws** (seed 0), ceiling at the **97.5th percentile**
(q = 0.975, the `divergence_report` convention). Rotation preserves the
interrupt count, the near-even spacing, *and* the duration-biased sampling
of visits — a tick lands in a visit with probability proportional to its
duration, so the known degenerate reading of any windowed contrast (windows
follow *long* visits, and the next visits differ by Markov structure alone)
is reproduced inside the null rather than argued away. An index-uniform
placement null was considered and rejected for exactly that reason.
**Self-test:** a rotation at offset u = 0 must reproduce the real partition
bit-identically; the reader asserts it per run before any draw.

**Census gate.** A tactic enters S3 in a cell only with **≥ 30 attempted
actions on each side** (in-window and elsewhere, pooled over the ten seeds).
The census table is reported before any headline; a cell in which no tactic
passes is reported as unestimable, never as a null result. Expected false
exceedances under pure noise ≈ 2.5 % of census-passing (cell × tactic)
instances at this ceiling; the count is reported beside the verdict.

**Truncation and coverage are reported as data:** the fraction of windows
truncated below n visits, and the fraction of all visits inside windows, per
cell.

## 5. The direction clause, operationalised

The decision rule's second branch closes the route if the terrain is
distinguishable "only in the direction the ordinary failure-column weights
already route toward". Operationally, for each rewarded (cell, tactic *t*)
instance on the blind arm:

For every interrupted place *p* in the cell's real records (weighted by its
share w_p of the cell's interrupts), take the profile's base out-distribution
b_p (the routing net's `base_out_weights`, synthetic-overlay arm), and form
the two composed routing distributions F_p ∝ b_p · v_failure(p, ·) and
S_p ∝ b_p · v_success(p, ·) from the declared `v3_persistent_backward`
columns, each renormalised over b_p's support. Tactic *t* is
**already-favoured** iff Σ_p w_p F_p(t) ≥ Σ_p w_p S_p(t) — the ordinary
failure response already shifts routing mass toward *t* at the places where
interrupts actually land. Every quantity in this computation is a declared
artefact or a recorded frequency; nothing is fitted.

## 6. The pre-registered conclusions and the decision rule

Verdicts are reported **CONFIRMED / NOT CONFIRMED** (never "moved").

**P1 — terrain structure exists.** On the **blind arm at 200 s, n = 3**: at
least one rewarded tactic (S3, census-gated, above the rotation-null
ceiling) in **≥ 2 profiles and ≥ 2 conditions** (the E2 bar's shape).
Expectation, recorded for honesty: NOT CONFIRMED — every friction-shaped
probe on this substrate has returned no exploitable structure, and the
learner already found that verdicts are not progress.

**P2 — the structure escapes the failure column.** Evaluated only if P1 is
CONFIRMED: at least one rewarded instance is **not** already-favoured under
§5. If every rewarded tactic is one the declared failure column already
routes toward, the ordinary weights already harvest the structure and a
kernel has no target beyond them.

**The decision rule (the handoff's, made mechanical):**

- **P1 NOT CONFIRMED, or P1 CONFIRMED and P2 NOT CONFIRMED → the structural
  route closes on evidence.** The deliverable is a criterion §(d) axis-4
  amendment **draft** in the §4.3-amendment style — all three routes closed:
  reactive structurally, mechanism-shape first-principles, structural
  empirically — placed in this record for Marc's ratification (the criterion
  file is not edited; the disposition is his). No kernel is built.
- **P1 and P2 CONFIRMED → the kernel has a target.** The deliverable is a
  kernel design brief carrying the corpus-grounding requirement (the
  recovery set must land attested-pattern/declared-magnitude against the ch3
  tactic-profile evidence, not pure declared judgement) and its two gates:
  Marc reopening the 2026-08-11 disposition (a register/V-trail entry), and
  the S2 freeze for any reported non-null configuration. No kernel is built
  in this session either way.

**Characterisations reported with no decision weight:** the class contrast
(structure, if any, is expected on the network class, where something is
actually destroyed; a rewarded set confined to the application class would
be examined as artefact and said so); the main-arm mirror of S3 (what the
failure column already does with the window); S1/S2 against their null
ceilings (does the window differ *at all*, before asking whether it
rewards); the n = 1 and n = 5 sensitivity windows; and the 2 000 s cells,
where 63–97 visits per gap make the window definition unstrained but 5–8
interrupts per run thin the census.

**What the probe is not powered for, stated before it runs:** any
significance claim (ten seeds; exceedance of a measured null band is the
only inferential statement made); any ordering of profiles; any cross-arm
time comparison (event- and share-shaped statistics only); any claim about
what a kernel would *achieve* — the probe prices the terrain, and the
learner precedent (success verdicts are not progress) bounds in advance how
much a verdict-denominated reward can promise.

## 7. Hard constraints carried

Reader-only (no simulation-behaviour change, no new declared values, no
schema change); determinism (seeded regeneration of the declared grid; the
configuration described is the configuration measured); the 2026-08-11
disposition stands throughout; badges do not move on this probe in either
direction.

## 8. Reproduce

```
PYTHONPATH=src python data/results/axis4_structural_probe/run_probe.py --workers 6
PYTHONPATH=src python data/results/axis4_structural_probe/analyse.py
```

---

# The verdict, as found

*Everything above the line was committed before the run existed (`0fe4d77`).
Everything below reports against those criteria without amending them.*

**The run.** 800 runs, zero errored cells,
`data/results/axis4_structural_probe/`. The rotation self-test passed on all
800 runs (an offset-zero rotation reproduces the real partition
bit-identically), and the analysis is the committed reader executed once.

## 9. The decision — P1 NOT CONFIRMED; the structural route closes on evidence

At the pre-registered decision configuration (blind arm, 200 s, n = 3):
**zero rewarded tactics across 138 census-passing (cell × tactic) instances**,
where noise alone at the 97.5th-percentile ceiling would be expected to
produce ≈ 3.5 false exceedances. No profile and no condition contributes an
instance, so the ≥ 2 × ≥ 2 bar is not approached, let alone met. P2 is not
evaluated (its gate is P1). The pre-registered expectation held, and the
branch that fires is the first: **the structural route closes on evidence,
and no kernel is built.**

## 10. What the post-interrupt window actually is

The window is *distinguishable* — and the distinction is a penalty, not a
prize. Pooled over the decision cells:

| condition class | success share in-window | elsewhere |
|---|--:|--:|
| network (position destroyed) | **0.119** (n = 13 368) | 0.196 (n = 17 242) |
| application (nothing destroyed) | 0.664 (n = 10 245) | 0.614 (n = 21 188) |

On the network class the post-interrupt terrain is roughly 40 % *worse* in
relative success terms — the cursor clear depressing every position-dependent
verb until re-acquisition, which is the blockage-persistence half of the
question answered in the direction that pays no kernel. On the application
class, where an interrupt destroys nothing but time, the window is
statistically indistinguishable tactic-by-tactic (mean census Δ +0.005, no
exceedance). The class contrast lands exactly where the executed boundary
record prices it: structure follows what the mechanism destroys, and the
only structure present is punitive.

The global statistics agree: S2 (the joint tactic × verdict profile) exceeds
its null ceiling in 9 of 20 blind-arm cells at the decision configuration —
the window differs, in the depressed-success direction the ordinary
failure-column weights already route on. This is the decision rule's second
flavour arriving via the first branch: what distinguishes the window is
precisely what the interrupt-as-failure verdict already responds to.

## 11. The sweep-wide census is itself sub-noise

Across the entire reported sweep — three window lengths × two arms × two
intervals, 947 census-passing instances — there are **16 exceedances, 1.7 %,
against the 23.7 (2.5 %) that pure noise would produce.** The probe did not
merely fail to find structure at the decision configuration; the whole grid
under-fires its own false-positive budget.

Four of the sixteen are a named degenerate artefact: `reconnaissance` at
Δ = 0.0 "exceeding" a *negative* ceiling. Its success share is saturated at
1.0 on both sides in those cells, and the ceiling goes negative only through
a null asymmetry recorded here for any future user of this reader: **a
rotation cannot un-interrupt a visit**, so really-interrupted visits enter
the pseudo-partitions as ordinary failure-verdict visits, biasing null
success shares downward. For reward detection that asymmetry is
anti-conservative — it *lowers* ceilings — so the observed zero at the
decision configuration holds a fortiori.

## 12. The n = 5 sensitivity lead, recorded and bounded

The discipline cuts both ways, so the one thing in the grid that looks like
structure is recorded rather than buried. At **n = 5** (no decision weight,
pre-registered as sensitivity only), `lateral-movement` exceeds its ceiling
on **both** network conditions in `objective_impact` (Δ 0.108 and 0.083)
and marginally in `objective_none_c2` under Complete Topology Shuffle
(Δ 0.072 against a 0.068 ceiling). Had n = 5 been the decision window, the
bar arithmetic would have been met — and three bounds say why it was not and
should not be read as terrain reward:

1. **The contrast class evaporates at wide windows.** At the 200 s interval
   the walk makes ~7.4 visits per inter-interrupt gap, so n = 5 tiles most
   of the run: in the `objective_impact` cells the elsewhere side shrinks
   from 162 to 87–88 attempts, and it is the *elsewhere* rate that moves
   (0.648 → 0.591) while the window rate barely does (0.691 → 0.699). The
   quasi-periodic-trigger caveat the window definition exists to respect is
   exactly this failure mode.
2. **The verb is the re-acquisition act itself.** Under `v2_partial`,
   `lateral-movement` dispatches `ENUM_HOST` — pop the next host, make it
   current, set the pivot. Elevated late-window success for it is the
   ordinary scan-then-re-acquire sequence completing after a cursor clear,
   behaviour the walk already performs with no kernel.
3. **The direction check closes 2 of 3.** The declared failure column
   already routes toward `lateral-movement` at the interrupted places in
   both `objective_impact` instances (already-favoured); the
   `objective_none_c2` instance escapes by a 0.0012 routing-mass margin on
   a 0.004 exceedance — noise-grade on both sides of the comparison.

If anyone wants this lead, it requires its own pre-registration on a fresh
grid; nothing is claimed from it here.

## 13. The remaining characterisations

- **Main-arm mirror (n = 3, 200 s):** three exceedances, the largest
  `initial-access` in `aggregate` under OS Diversity (Δ 0.240 against a
  0.116 ceiling) — one profile × one condition, below any bar, and the main
  arm's windows are populated by the failure-column response itself, so its
  exceedances confound terrain with the response the ordinary weights
  already make.
- **2 000 s cells:** census-thin as pre-registered (33 instances on the
  decision arm), zero exceedances.
- **Window bookkeeping:** 4–14.5 % of windows truncated below n = 3;
  window coverage 19–43 % of visits per cell — the contrast class existed
  everywhere the decision was taken.

## 14. What this licenses, and what it does not

The empirical sentence the 2026-08-11 disposition could not yet say: **the
terrain in the window after an MTD interrupt rewards no tactic set over the
ordinary weights — it is either indistinguishable (application class) or
systematically punitive (network class) — so a pivot-to-recover kernel has
no target on this substrate.** With the reactive route closed structurally
(every defence in the pool clocked and attacker-blind) and mechanism-shape
bounded first-principles (any kernel is a richer function of the same
one-bit verdict), all three routes to adaptive advantage are now closed,
the third by measurement.

Boundaries that travel with it: measured on the four single-mechanism
conditions at both intervals with the decision at the 200 s operating
interval, ten seeds, the landed sink implementation, exceedance-of-a-
measured-null as the only inferential statement; the n = 5 lead of §12 is
on record; and the ceiling is verdict-denominated — even a rewarded tactic
would have promised success *verdicts*, which the learning study showed are
not progress. Nothing here moves the axis-4 badge (DESIGNED, unchanged),
constitutes a ruling, or touches the MTD-AI future-work reservation: a
reactive defender would reopen the reactive route, and this probe says
nothing about that regime.

## 15. The amendment, drafted for Marc's ratification

The 2026-08-11 disposition stands until Marc reopens or extends it; the
criterion file is deliberately not edited by this probe. The following
paragraph is the §4.3-amendment-style text ready to land under
`apt_model_criterion.md` §(d) axis 4 on ratification:

> #### Amendment, 2026-08-13 — the structural route was probed, and closed on evidence
>
> **The badge does not change. What changes is the closure's third leg,
> which is now measured rather than parked.** The 2026-08-11 disposition
> closed the reactive route structurally and bounded mechanism-shape
> first-principles, leaving the structural route — does post-interrupt
> terrain carry structure a pivot-to-recover kernel could exploit —
> explicitly not pursued. A pre-registered, reader-only probe over a seeded
> regeneration of the experiment-2 arms
> ([`pipeline/ogasp/axis4_structural_probe.md`](pipeline/ogasp/axis4_structural_probe.md);
> 800 runs, verdict-blind and conditioned arms, cyclic time-rotation null,
> census-gated) found **zero post-interrupt-rewarded tactics in 138
> census-passing instances at the decision configuration** (≈ 3.5 expected
> from noise), and 16 of 947 (1.7 %, below the 2.5 % noise budget) across
> the whole sensitivity grid. The window is distinguishable — success
> depressed ~40 % relative on the position-destroying class,
> indistinguishable on the application class — but the distinction is
> punitive, in exactly the direction the declared failure column already
> routes on. All three routes to adaptive advantage are therefore closed:
> **reactive structurally, mechanism-shape first-principles, structural
> empirically.** The intractability claim no longer rests on a parked
> question, and the pivot-kernel objection is answered with a measurement:
> a "pivot to recover from disruption" mechanism has no terrain to pay it
> on this substrate. Boundaries: decision at the 200 s operating interval
> over the four single mechanisms at ten seeds; one sensitivity-window
> lead recorded and bounded in the probe record §12; the closure is
> verdict-denominated; MTD-AI evaluation remains the named future work
> that would reopen the reactive route.

## 16. Reproduce

As §8; the analysis is deterministic given `runs.jsonl` (seeded rotations),
and the runner regenerates `runs.jsonl` exactly (seeded grid, landed
substrate).
