---
status: durable
created: 2026-07-27
updated: 2026-07-27
topic: "Experiment 1 (movement attacker vs 6-phase baseline) — setup, headline numbers, the two failure modes, and the rulings the result triggered; the tracked promotion of the untracked run workspace"
lineage: promoted from data/results/exp01_movement_vs_baseline/README.md (gitignored workspace, regenerable); closes docs/handoffs/2026-07-15_l3_first_numbers.md
---

# Experiment 1 — the movement attacker against the inherited baseline

> **Retired class labels.** This record is investigation history and is left as
> written: it reports the pre-2026-08-06 labels `pure_steal` / `pure_impediment` /
> `double_extortion` / `infrastructure_setup`, which the objective-tactic rename
> replaced with `objective_exfiltration` / `objective_impact` /
> `objective_exfiltration_impact` / `objective_none_c2`. Rewriting them would
> re-attribute evidence to labels that did not exist when it was taken. Crosswalk:
> [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

**Status:** durable. The first end-to-end numbers from the coupled L3 attacker,
run head-to-head against the inherited 6-phase attacker on the same substrate.
This record is the **tracked** account: the run workspace at
`data/results/exp01_movement_vs_baseline/` is gitignored by design (regenerable —
runner, numbers, figures), and the repo's convention is to promote a finished
result into `docs/` when it needs to survive. The numbers below drove the
supervisor rulings **S1–S6**
([`supervisor_decision_register.md`](supervisor_decision_register.md)), so they
need to be citable without the workspace.

**Reproduce:** `PYTHONPATH=src python data/results/exp01_movement_vs_baseline/run_experiment.py`,
then `… make_figures.py`. Landed at commit `c27409f`; the loop it exercises
landed at `48471b8` and was verified against the runtime model first
([`runtime_verification.md`](runtime_verification.md)).

## 1. Setup

| | |
|---|---|
| **arms** | baseline = the native `proceed_attack` FSM, untouched · movement = `MovementAttacker`, overlay-on (seeded at reconnaissance), one run per GASP class plus the aggregate null |
| **matrix** | 2 attackers × {no MTD, random-multi MTD @ 200 s} × 10 seeds = 140 runs |
| **horizon** | 15 000 s (a free experimental variable per R4; matches the baseline golden) |
| **metrics** | reached-objective, distinct hosts compromised, time-to-first-compromise, and the action budget decomposed into blocked / failed / recon-success / compromise-success — identical definitions on both arms, keyed on the single substrate procedure that appends to `compromised_hosts` (P8) |

**Comparability.** Within-substrate only; internal MTTC; no cross-paper
magnitude claims. Ten seeds is a reconnaissance sample, not a powered study.

## 2. Headline — M8 confirmed without qualification

Across **all 100 movement runs** (5 profiles × 2 conditions × 10 seeds) the
profiled attacker reached the substrate objective **zero** times (ASR 0.00). The
baseline reached it in 9/10 runs with no MTD and 10/10 under MTD, saturating the
network to its 0.8 compromise cap (~40 hosts) every time.

| arm : profile | ASR | hosts (mean ± 95 %) | MTTC s (n) | actions/run | blocked % | terminal |
|---|---:|---:|---:|---:|---:|---|
| baseline | 0.90 | 39.8 ± 2.4 | 238 (10) | 815 | 0 | objective |
| movement : aggregate | 0.00 | 0.4 ± 0.4 | 5294 (3) | 480 | 76 | horizon |
| movement : pure_steal | 0.00 | 0.0 | — (0) | 210 | 95 | sink |
| movement : double_extortion | 0.00 | 0.7 ± 0.3 | 168 (7) | 74 | 0 | sink |
| movement : pure_impediment | 0.00 | 1.2 ± 0.4 | 4889 (9) | 427 | 37 | horizon |
| movement : infrastructure_setup | 0.00 | 2.2 ± 0.8 | 1177 (10) | 502 | 0 | horizon |

(No-MTD condition; the random-MTD condition is in the workspace's
`numbers/summary.json`.) The **M8** expectation — that the profiled attacker
would do *no better* than the baseline on pure security metrics — holds
emphatically: it does dramatically worse. The content is in the shape of the
failure, not its magnitude.

## 3. Finding 1 — two distinct failure modes, and profile decides which

The movement attacker spends a run's worth of actions and gets almost nowhere,
but the *reason* splits cleanly in two, and which mode a profile lands in is a
property of the profile rather than of the seed.

- **Friction (blocked).** `pure_steal` (95 % of actions blocked) and `aggregate`
  (76 %) spend most of their budget attempting verbs the substrate refuses. The
  net routes them into tactics whose verb needs state a *different* tactic order
  would have established (`curr_host`, `curr_ports`); the verb never runs, the
  driver records `PRECONDITION_UNMET`, and the token is routed back. This is the
  **H-coupling** quantified at P4: walking CTI tactic-order instead of the
  substrate's native precondition-order manufactures failure that the baseline —
  which *is* that native order — never encounters.
- **Churn (busy but not spreading).** `infrastructure_setup` and
  `double_extortion` are blocked 0 % of the time and still fail. They accumulate
  hundreds of *successful* actions (`infrastructure_setup`: 502 actions/run)
  that are overwhelmingly reconnaissance and neighbour-reveal on a foothold they
  never expand — **931 host-compromise events over 10 runs landing on just 22
  distinct hosts**, the same couple of hosts re-compromised ~40 times each.

`pure_impediment` sits between the two (37 % blocked). The structural point: the
profiled attacker has **two failure surfaces** — one where the substrate stops
it, one where its own routing loops it — and neither is visible as anything but
"low compromise count" unless the action budget is decomposed.

## 4. Finding 2 — effort does not convert to breadth

The baseline turns ~815 successful actions into ~40 distinct hosts (~20
actions/host). The most active profile, `infrastructure_setup`, turns ~460
successful actions into ~2 hosts (~210 actions/host, an order of magnitude
worse), and `pure_steal` turns its budget into zero. The baseline *advances*;
the profiles *repeat*. Read from the other side this is the churn of Finding 1:
the baseline's scripted order is a compromise-manufacturing loop, and the
CTI-derived order is not — on this substrate, under this controller.

## 5. Finding 3 — some profiles walk into a dead end and stop

`pure_steal` (9/10 runs) and `double_extortion` (10/10) terminate early at a
**sink** — a tactic-place with no onward routing (`impact`,
`credential-access`). Their nets reach an objective-band tactic that, under the
coarse controller, dispatches a placeholder neighbour-reveal and has nowhere to
go next. These profiles therefore observe a **truncated window** (74–210
actions/run against ~500 for the horizon-runners), so their per-profile MTTC
denominator is shorter than the profiles that run the full 15 000 s. This is the
accept-and-censor consequence P7 predicted, and it is the direct motivation for
**S5** (retrace rather than discard).

## 6. Finding 4 — MTD does not change the verdict, which is the interesting part

Adding MTD (random-multi @ 200 s) changes neither side's outcome: the baseline
still saturates (40 → 41 hosts), the profiled attacker still reaches nothing
(0.9 → 0.9 hosts pooled). The one metric that moves is the baseline's
time-to-first-compromise (238 → 356 s, ~+50 %) — directional rather than clean
at ten seeds, with overlapping CIs, and consistent with the E1 finding that
end-of-sim compromise fraction is a poor discriminator at long horizons.

The framing that matters: **the security metric that responds to MTD is defined
on the baseline-shaped attacker.** The profiled attacker sits outside that
measurement frame — not because it resists MTD, but because it never gets far
enough for MTD to bite. This is the M8 metrics gap made concrete rather than
asserted, and it is the empirical half of the S6 criterion question.

## 7. Caveats that travel with every reading of these numbers

- **The tactic→verb map is a chosen input parameter, not a fidelity claim.** The
  experiment-1 controller collapses 15 tactics onto 6 verbs (`initial-access` →
  port-scan rather than exploit; the whole Actions-on-Objectives band →
  neighbour-reveal). That coarseness *is* much of what produces both the
  blocking and the churn ([`controller.md`](controller.md) §2). S4 replaces it.
- **Sink-censoring** truncates the MTTC window for two profiles (§5).
- **One MTD scheme, not the family.** No-MTD vs random-multi only; the question
  of whether an MTD *mechanism ranking* shifts under a profiled attacker needs
  the full SDR sweep and is carried by the experiment-2 handoff.
- **Ten seeds.** Directional, not powered.

## 8. What this triggered

The result is the input to the post-experiment-1 rulings
([`supervisor_decision_register.md`](supervisor_decision_register.md) §S1–S6).
The reading agreed with the supervisor is that **the two failure modes are
attributable to two separable causes that are ours to address** — the inherited
phases' tight integration (substrate, frozen under S2 to refinement and bug
fixes only) and the deliberately coarse tactic→verb collapse (controller,
replaced under S4) — with the large-jump weighting (S1) and the sink policy (S5)
as contributing factors. The honest summary the meeting settled on: the profiled
attacker is not a weaker attacker, it is a **different kind** of attacker, and
this substrate and metric suite currently only know how to score the baseline's
kind.

## 9. Where this connects, and when to update

- **Verified before it ran:** [`runtime_verification.md`](runtime_verification.md)
  (P4 blocked-fraction table, P7 sink enumeration, P8 comparability).
- **The layers it exercises:** [`controller.md`](controller.md) (dispatch),
  [`success_failure_overlay_design.md`](success_failure_overlay_design.md)
  (routing policy), [`synthetic_overlay.md`](synthetic_overlay.md)
  (pre-intrusion structure).
- **The burden it does not yet discharge:**
  [`../../../notes/ch4_methods/evaluation_burden.md`](../../../notes/ch4_methods/evaluation_burden.md)
  — stability and divergence both remain untested; this run establishes neither.
- **When to update:** when experiment 2 runs (this record stays as the
  experiment-1 account and gains a pointer, rather than being rewritten — it is
  the baseline the refinements are measured against). If the workspace is
  regenerated with different settings, the numbers here stop matching and the
  §1 setting block must be re-read before citing them.
