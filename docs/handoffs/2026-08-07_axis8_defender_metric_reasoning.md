---
status: open
created: 2026-08-07
---

# Axis 8 by the other route — what triggers a mutation, what avoids one, and an attacker that has worked it out

**Split out of
[`2026-08-06_knowledge_gated_apt_attacker.md`](2026-08-06_knowledge_gated_apt_attacker.md)
on 2026-08-07 (Marc), absorbing its §5 / §5.1 / §5.2 in full.** That brief is a
*learning* build — vulnerability memory feeding the exploit decision — and it kept
acquiring an axis-8 half that does not belong to it. §2 has the test that separates
them.

**Cross-examined against the originating prompt, 2026-08-07**, after a first draft
lost five things. What that pass restored is marked ⟲ ; what it added new is marked
✚. Recorded so the next cross-examination knows what was already checked.

**Gated on R-B**, the `mtd_ai` sanction, which Marc is probing in a parallel
session. **Design only; no code written, none should be.**

---

## 0. Amendment, 2026-08-08 — the premise is now conditional, and the arm it needs is wired but blocked

**Read this section before any other.** It was written after the
`feat/mtd-ai-cost-calibrated` rebuild landed, which this brief predates by one
day and which moves the ground under §4, §7 and §8. Three things changed: the
premise acquired a gate, the design acquired a hard constraint, and the arm
acquired a blocker. Nothing below §0 has been rewritten — the corrections are
recorded here so the original reasoning stays legible against them.

### 0.1 There is no "no-op threshold", and under Tay's reward there is no no-op at all

The brief is written as though the attacker could stay *below* a level at which
the defender acts. **It cannot, because no such level exists.** The defender is
an `argmax` over five Q-values (`mtd_ai_operation.py` ~line 119), not a
threshold test. "Sliding under the no-op" is not a bar to stay beneath; it is
the region of state-space in which `Q(s, 0)` happens to be the maximum, and
whether that region is non-empty is an empirical property of a *specific set of
trained weights* — not a structural property of the defender.

**Under the inherited reward that region is empty by construction.**
`calculate_reward`'s own docstring now states it: every non-zero weight is
improved by deploying, and the two features that could have priced moving too
often — `mtd_freq` and `time_since_last_mtd` — are weighted exactly 0. The
calibration record pre-registers this as **C4**: the greedy no-op share at
λ = 0 must sit **below 0.10**, and anything higher means the instrument is
broken rather than the agent thoughtful.

So the side-channel premise in §4 is **false at λ = 0**. There is nothing to
hide beneath. The mechanism has a target only if the cost-calibrated agent at
λ > 0 opens one, which is exactly **C1** — and
[`../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md`](../implementation/pipeline/ogasp/mtd_ai_cost_calibration.md)
§3 is still unwritten. **That verdict is the gate on this entire brief.** If C1
fails, no declared attacker policy rescues it, because there is no no-op region
to steer the defender into.

### 0.2 Three corrections to §4's channel table

- **The reward is now on *deltas*, minus a downtime charge** — `Σ weighted
  security-posture deltas − λ·Δdowntime_ratio`. §4's closing paragraph ("the
  training reward closes the loop") describes the pre-rework reward and should
  be read as history.
- ⚠ **The two levers §4 calls sharpest carry weight exactly 0.**
  `host_compromise_ratio` and `attack_type` are both `0` in `SECURITY_WEIGHTS`.
  Spacing compromises and choosing the verb move the **policy input** — the
  Q-network consumes the level vector — but contribute **nothing to the training
  signal**. The distinction matters: the attacker manipulates levels, the agent
  was trained on deltas, and only `overall_asr_avg`, `roa`, `risk`,
  `overall_mttc_avg`, `shortest_path_variability` and `ip_variability` are live
  in the reward at all.
- **§7.6's degenerate `attack_path_exposure` is config-dependent, not
  universal.** `target_node` defaults to `None` (`network.py:79`) but *is*
  assigned when `network_type == 0` (`network.py:210–211`). Where it is constant
  its −75 weight contributes exactly zero, since a constant has zero delta. Still
  owed the instrumented run §4 asked for; do not quote it either way until then.

### 0.3 ✚ The design constraint that decides the build — inherited from axis 6's failure

§6 rules for the endowed form and §8 recommends a declared policy. **The obvious
implementation of that — a static per-tactic "metric footprint" table — is
already known to fail on this seam**, and the reason is measured rather than
argued.

[`../implementation/pipeline/ogasp/incentive_rationality.md`](../implementation/pipeline/ogasp/incentive_rationality.md)
§6.3 records why the axis-6 build died: the modulator was *"a pure function of
declared data and the current place, so its factor table is precomputable"* — a
spike folded it into a plain overlay and reproduced the stateful run **30/30
bit-identical**. *"The MTD condition is not among its inputs, so no parameter
choice could have made it respond to MTD."*

A static footprint table has exactly that shape. It would reference the defender
nowhere and would **fail this brief's own §2 test**, the one that separates axis
8 from axis 7. Two consequences, both binding:

1. **The factor must depend on something that varies within the run as a
   function of the defender's actual behaviour.** The seam already provides it:
   `observe_mtd_interrupt` (`movement/state.py`) reports every mutation the
   attacker absorbs, *before* the routing decision that follows. An attacker
   belief updated by mutations it has actually taken is defender-conditioned in a
   way no precomputation can capture. That hook is the mechanism's justification
   for existing on this axis.
2. **The acceptance gate is that the collapse test must *fail*.** Fold the
   factor table into a static overlay; if the run reproduces bit-identically, the
   mechanism is not axis 8 and must not be reported as it. Reuse
   `data/results/axis6_rationality/collapse_test.py`. **Add this to §9.**

A second inherited caution: a ratio normalised over the out-set is invariant to
anything scaling uniformly across it, which is the other half of why axis 6
died. Check the footprint is not near-proportional to declared dwell before
committing, or the null reappears for the same reason.

### 0.4 The dumb / smart split, and what must *not* go in the same mechanism

The split is **one parameter**. λ = 0 is the exact null and is bit-identical to
today, so the "dumb" APT is the current attacker for free and the ablation is
exact; λ > 0 is the "smart" one. One declared family, one band, swept — the
discipline the utility modulator already passed.

⚠ **The accumulate-then-strike arc is a second mechanism and must not be folded
into the first.** Constant λ buys suppression only. The arc needs λ gated on
accumulated knowledge, which is the sibling brief's quantity — and with both in
one modulator no effect can be attributed to either. §5's composition hazard
applies exactly here. Note also the collision already on record
([`../implementation/pipeline/ogasp/targeted_attacker_feasibility.md`](../implementation/pipeline/ogasp/targeted_attacker_feasibility.md)
§7): a realised-success channel and the axis-7 learning modulator would read the
same running estimate, and that boundary is owed *before* either is built on the
other.

### 0.5 ✚ What was built this session — the arm, and the blocker it exposed

**The arm did not exist.** `tools/mtd_ai_run.py` builds the inherited
`Adversary`, so there was no configuration in which the movement attacker faced
the reactive defender at all — the falsifier §8 asks for was unrunnable. It is
now wired:

- `run_movement(..., mtd_scheme="mtd_ai", mtd_ai=MTDAIConfig(main_network=...))`
  starts `MTDAIOperation` against the movement walk. The defender is given the
  **bare** attack operation, never the state-seam proxy.
- The action space and the canonical 5/6 feature head moved to
  `mtdnetwork.mtdai.mtd_ai` (`mtd_action_space()`, `CANONICAL_FEATURES`) and both
  drivers now read them from there, so no run can re-point action 1 at a
  different mechanism than the agent was trained to deploy. The import is
  deferred so the movement path does not load TensorFlow.
- The per-decision ledger is carried onto the run result (`mtd_decisions`), and
  `decision_summary()` reports the choice distribution with the **greedy** no-op
  share separated from the pooled one — which is §9's first bullet, now
  computable.

**Verified end to end**: `objective_exfiltration_impact`, two seeds, 15 decisions
each, ledger and mutation mix flowing. With an *untrained* agent at ε = 0 the
greedy no-op share is 0.0 and every decision is action 1 — the degenerate
constant argmax an untrained network should give, and an instrument check only.

⚠ **BLOCKER, for Marc's disposition — §7.5 confirmed, and worse than predicted.**
Two of the three profiles tried **crash the run outright** with
`ZeroDivisionError` on `attack_success_rate = compromised_num / attack_event_num`
(`mtd_ai_operation.py` ~line 448). Measured trigger, at the **first decision**
(t = 200.1 s):

| | value at crash |
|---|---|
| record rows | 1 |
| `compromised_num` (60 s) | 0 |
| `attempt_hosts` | **0** |
| verbs in record | `{SCAN_HOST: 1}` |

**§7.5 attributed this to a profile dispatching few `SCAN_PORT` verbs. The
measurement refines that**: the proximate cause is `attempt_hosts == 0` — the
walk has run only *host-independent* recon (`SCAN_HOST` writes
`current_host_uuid = -1`), so the denominator never accumulates. Any profile
whose opening stretch is host-independent trips it, and the inherited attacker
escapes only because its phase order reaches a host-scoped verb before t = 200.

This makes the blocker **flaky rather than categorical** — one profile in three
survived — which is the worse failure mode, because a study could be run without
noticing which arms were silently unrunnable.

**Not repaired here**, per §10: this is a substrate change and needs its own
disposition. It is now the **hard prerequisite for the §8 falsifier**, which
cannot report a per-profile distribution while most profiles cannot complete a
run.

### 0.6 Revised order of work

1. **Write the C1 / C4 verdict** into the calibration record §3. Everything else
   is downstream; a C1 failure kills this brief.
2. **Disposition the §7.5 divide-by-zero** (0.5). Until then the falsifier covers
   only whichever profiles happen to survive, which is not a per-profile
   distribution.
3. **Then run the §8 falsifier** — now much cheaper than when §8 was written,
   because the per-decision ledger and `decision_summary()` exist and are exactly
   its instrument.
4. **Only then design the policy** — and write the collapse test (0.3) *before*
   the modulator, not after.

---

## 1. The question, in the terms it was actually posed

> *"The attacker doesn't see the model/scheme of the MTD, but can see whether the
> MTD makes a move or not — i.e. this opens up MTD to side-channel attacks. **What
> can the attacker leverage to trigger MTD mutations? What can it do to avoid
> them?** … we can pretend the smart APT model has successfully used
> side-channelling techniques and deduced how to manoeuvre in the network in a way
> to **maintain the same network for as long as possible, to build up its knowledge
> space**, and hopefully launching its swift arc of network compromise **before its
> information set is invalidated**."* — Marc

⟲ **The bidirectional question is the brief.** Not "can the attacker be quiet" but
**what does it leverage to trigger a mutation, and what does it do to avoid one**.
Both directions matter, and the second is the one with a purpose attached.

⟲ **The purpose is not stealth for its own sake — it is time.** Suppressing
mutation preserves the network long enough for the attacker's knowledge to
saturate, and the payoff is the strike that follows. That makes this mechanism the
*enabler* of the sibling brief rather than a parallel one: knowledge is only worth
accumulating if it survives long enough to use, and this is the mechanism that buys
that time. **Neither brief is worth much without the other**, and the composition
must be stated in both (§5).

---

## 2. Why this is a separate handoff — the test that splits them

Both briefs give the attacker memory, so it is fair to ask why they are two things.
The test is **does the capability reference the defender?**

- Vulnerability memory **does not**. It estimates `P(this exploit works)` from its
  own past attempts and behaves identically with MTD switched off. That is learning
  (axis 7); calling it scheme awareness over-claims.
- This mechanism **does**. It exists only because a defender computes metrics from
  the attacker's activity and selects mutations from them. Remove the defender and
  the capability has no referent.

### What it is *not* — a scoping correction that must not be quietly dropped

**This is not one of Jalowski's three §4.1 primitives** — (i) state-collision
recognition, (ii) MTD-event-as-beacon, (iii) metadata-shadow invariance. It is
closest to (iii) and is not it. The claim rests instead on Jalowski's **§4.3
corrective**: research must shift toward *"smart, adaptive attackers who understand
the MTD scheme and look for the mathematical logic behind the movement"*. Say that
plainly rather than filing it under a primitive it does not satisfy — an examiner
who reads §4.1 will check. Primitives (ii) and (iii) stay excluded and are not
asked for here.

---

## 3. ⟲ The side-channel premise — what the attacker can already observe

**The attacker can detect that a mutation happened, today, with no new channel.**
It experiences the consequences directly: a network-layer firing clears its host
cursor, an application-layer one interrupts its action, and a re-scan after a
diversity firing returns different services. **The axis-7 learner already consumes
exactly this signal**, forgetting on every `apply_mtd_interrupt_cost`.

What remains unavailable: *which* host was mutated while the attacker was
elsewhere, per-host mutation counts (no strategy keeps them), and the schedule.

**The boundary is the useful one: mutation *occurrence* is observable, mutation
*targeting* is not.** A design that stays on the observable side needs no new
observation channel and no reversal of the beacon exclusion. That is what makes
this route buildable at all, and it is the literal form of Marc's *"can see whether
the MTD makes a move or not"*.

---

## 4. The channel — all eleven features, and which the attacker can move

Read from `mtd_ai_operation.get_state_and_time_series` (lines ~299–443). **A code
reading, not a measurement; every line needs an instrumented run before anything is
built on it.**

✚ **The state splits exactly as Marc's prompt does** — the code has a `state_filter`
("static") and a `time_series_filter` ("time"), five and six features. Both are
**filtered at use**: `value if key in self.features["static"] else 0`. So the
configured feature set decides which levers are live at all, and **an ablation over
`features` is available for free** — a lever the design should exploit rather than
discover.

| # | feature | group | computed from | can the attacker move it? |
|---|---|---|---|---|
| 1 | `host_compromise_ratio` | static | compromised hosts **in the last 60 s** ÷ total | **yes — spacing.** Three compromises in a minute read 3/50; the same three over five minutes read 1/50 at any instant |
| 2 | `attack_path_exposure` | static | `network.attack_path_exposure()` | ✚ **no — it is a constant.** `target_node` is `None` in every run, so `get_path_from_exposed` falls into a bare `except: pass` and this returns a degenerate **1.0**. One of five static features carries no information |
| 3 | `overall_asr_avg` | static | `compromised_num / attack_event_num`, denominator counting **`SCAN_PORT` rows only** | **yes — the scan:exploit ratio.** More reconnaissance drives observed ASR down |
| 4 | `roa` | static | the **last** exploited vulnerability's `(complexity·impact)/exploit_time` — `[-1]`, a single sample | **yes — vulnerability selection** |
| 5 | `risk` | static | the last exploited vulnerability's `complexity·impact` | **yes — vulnerability selection** |
| 6 | `mtd_freq` | time | mutations ÷ elapsed, from the defender's own record | indirectly — it is the *output* this mechanism suppresses, fed back as input |
| 7 | `overall_mttc_avg` | time | mean **duration** of `SCAN_PORT`/`EXPLOIT_VULN`/`BRUTE_FORCE` rows | **yes — tempo.** Longer actions raise it |
| 8 | `time_since_last_mtd` | time | the defender's own clock | no |
| 9 | `shortest_path_variability` | time | the scorer's shortest-path record | topology-derived; attacker moves it only by compromising |
| 10 | `ip_variability` | time | host IP list against the previous one | no — and note the asymmetry: **IP Shuffle is invisible to the attacker but visible to the defender's own state** |
| 11 | `attack_type` | time | ✚ **the verb the attacker is running right now**, via `attack_dict` → `{SCAN_HOST:1, ENUM_HOST:2, SCAN_PORT:3, EXPLOIT_VULN:4, SCAN_NEIGHBOR:5, BRUTE_FORCE:6}`, default **7 = no information**, gated by a `random() <= attacker_sensitivity` draw | ✚ **yes, and this is the most direct lever of all** |

✚ **`attack_type` is the sharpest channel and the first draft missed it entirely.**
The attacker's *choice of verb* is literally a defender input, sampled each time the
state is read. That is the most exact answer available to *"what can the attacker
leverage to trigger MTD mutations, what can it do to avoid them"* — the verb it runs
is read directly. Two riders: the encoding is an **arbitrary ordinal** (the network
sees `EXPLOIT_VULN`=4 as numerically between `SCAN_PORT`=3 and `SCAN_NEIGHBOR`=5,
which means nothing), and the channel is **stochastic** — below sensitivity 1.0 the
defender gets 7, "no information", so the attacker is partly hidden for free.

**The training reward closes the loop:** `overall_asr_avg`, `roa` and `risk` carry
**−75**, `overall_mttc_avg` carries **+75**. An attacker that spaces its
compromises, prefers low-impact vulnerabilities, scans more than it exploits and
moves slowly makes the defender's state read *safe*.

**The suppression target is real and reachable.** `mtd_ai`'s action space includes
`action == 0`, a genuine DO NOTHING gating the whole register-and-trigger block
([`2026-08-06_mtd_ai_reintegration.md`](2026-08-06_mtd_ai_reintegration.md) §1).

### 4.1 Two ceilings, both quantified — report against these, never against zero

`static_degrade_factor = 2000` forces a **random** mutation after 2 000 s of
inaction (≈ 7 forced mutations per 15 000 s run whatever the attacker does), and
`choose_action` is ε-greedy, so a deploying action fires regardless of state. Any
suppression figure quoted against zero is wrong by construction.

---

## 5. ⟲ What the suppression is *for* — the composition with the sibling brief

The point of biasing the defender toward doing nothing is **not** a lower
detectability curve. It is to **hold the network still long enough for the
attacker's knowledge to become usable**, then strike before that knowledge is
invalidated.

Stated as the loop it is:

1. Manoeuvre so the defender's state reads safe → mutations are suppressed toward
   the two floors in §4.1.
2. The configuration holds still → the attacker's knowledge space **saturates**
   (the coverage curve of the sibling brief's §3.1a).
3. Strike while the information set is still valid → the accumulate-then-strike arc
   (sibling §4.1), measured rather than declared.

**This is the strongest reason the two briefs exist**, and it is also the sharpest
risk: each is individually weak and the pair is what makes the argument. Record the
dependency in both, and note that **§9's composition hazard applies with force** —
two mechanisms both conditioning on exploit-shaped experience must be jointly
checked, never assumed to add.

⚠ **One premise of that loop is already measured false at the granularity it was
argued at, and it must not be re-derived.** The originating framing was that
constrained diversity would let the attacker *"use its remembered image of the host
and use its workflow that worked previously"*. The combinatorics say no: exact
whole-host image recurrence is **zero at every reachable service-pool setting**,
because the per-`(os, version)` draw space is `names × 16` and the 16 is fixed by
`len(SERVICE_VERSIONS) // len(OS_VERSION_DICT[os])`, which no pool parameter
touches (sibling §3.1). The **reasoning survives at a coarser grain** — per-service
and per-vulnerability identity recur heavily, two-thirds of live ids on more than
one host — so the loop above holds with *identity* memory and not with *host-image*
memory. Build to that grain.

---

## 6. ⟲ Learned or endowed — the fork, and the ruling

| how it is built | axis 8? | licensed? |
|---|---|---|
| the attacker **learns** the input→output relation at runtime | **yes** | **no.** This re-engages the original exclusion head on — its stated reason was that the primitives need *"an inference capability — machine learning or reinforcement learning over observed defender behaviour"*, and this is exactly that. Unlike memoisation it does not narrow the exclusion; it asks for it to be lifted |
| the attacker is **endowed** with a declared policy derived from an offline analysis of what the defender reads | **yes, and defensibly** | **yes**, on the house's own discipline — the *envelope, not actor* rule: a run is "one instantiation of a behavioural envelope under a declared policy". No runtime learning, one declared family, ablatable to null |

**RULED (Marc, 2026-08-07): the endowed form.**

⟲ **And the narrative it stands in for is the trial-and-error one.** Marc's framing
is that the attacker *"has figured out how the MTD makes its decisions by trial and
error"* — that is the fiction the declared policy encodes, and precisely what is
**granted rather than modelled**. Write that into the badge text. The claim becomes
*"an adversary that has already characterised what this defender measures behaves
thus, and here is what that buys it"*. Without that sentence it is an over-claim;
with it, it is the honest axis-8 move.

---

## 7. The serious threat to validity — read before designing anything

**The levers may be implementation quirks rather than defence properties**, and an
attacker tuned against them is **gaming Tay's implementation, not evading a
defence**. A thesis claim built on that is a claim about a bug.

1. A **60 s window** on `host_compromise_ratio` appearing nowhere in Tay's paper.
2. `roa` / `risk` as a **single most recent sample** (`[-1]`), not an aggregate.
3. An **ASR denominator counting only `SCAN_PORT`**, one of three attack verbs.
4. ✚ **The ASR and MTTC features describe a run *prefix*, not a recent window.**
   `sub_record = record[record['cumulative_compromised_hosts'] <= compromised_num]`
   with `compromised_num` the last-60 s count, so the filter selects the opening
   stretch during which the *cumulative* total had not passed the *recent* count. A
   quiet attacker does not merely lower these features — it **re-scopes which part
   of the run they describe**.
5. ✚ **The unguarded divide-by-zero triggers on the mapping, not on tempo.**
   `attack_success_rate = compromised_num / attack_event_num` has no guard, and on
   the movement arm the `SCAN_PORT` row count is a function of the tactic-to-verb
   mapping. A profile dispatching few `SCAN_PORT` verbs zeroes the denominator
   however loud it is.
6. ✚ **`attack_path_exposure` is a degenerate constant 1.0** (§4, row 2). A feature
   the agent was trained against carries no information in any run on this substrate.
7. ✚ **`attack_type`'s ordinal encoding is arbitrary** — an ordering the network
   will read as magnitude and which means nothing.
8. ✚ **The reward's positive term rides an open ruling.** `overall_mttc_avg` is a
   per-**row** mean and `_do_exploit_vuln` writes one row per vulnerability tried,
   so the two arms do not write rows alike — the same accounting that inverted the
   duty-cycle verdict (`README.md` § Decisions waiting on Marc).

**The honest claim form, fixed now rather than negotiated later:** *behavioural
change alters what this reactive agent observes* — never *the attacker defeats
reactive MTD*. State the quirk list as a threat to validity in the design record so
an examiner reads it from you rather than finding it.

---

## 8. Recommended approach — the cheap falsifier first

**Run the profiled attacker against the reactive selector as it is, with no
attacker mechanism.** The five profiles already differ enormously on what the state
reads — the profiled attacker compromises 0.5–5 hosts where the inherited one
compromises ~39. That is a free, naturally-occurring spread.

**Report the mutation-choice distribution, not just the outcome**, with the
`action == 0` share called out. If the selector's choices do not differ across a
spread that large, no declared policy will rescue the claim and one cheap run has
saved an expensive build.

✚ **Add the feature ablation, which is nearly free** (§4). Because the state is
filtered by `self.features`, the same run can report which features the agent's
choices actually depend on — which tells you which levers are worth declaring a
policy over, before declaring one.

**One premise must not revert.** This route was historically argued as *a slower
attacker presents a different signal stream*. The slowness half does not survive a
per-action reading: counted as actions rather than attack-record rows the profiled
attacker takes **more** steps per run than the inherited one (463–674 against 371),
and at the exposure reader's tier-null setting the arms' event tempo does not
separate at all. The channel relocates rather than closing — what the state reads is
dominated by compromise-derived quantities. **Frame it as *does a low-yield attacker
change what the reactive defender does*, never as a tempo claim.**

Only then: design the declared policy — one family, ablatable to null, swept over
its band against conclusions committed before any run.

---

## 9. Validation gate

- The cheap falsifier reports a **mutation-choice distribution per profile**, the
  `action == 0` share separately, against both floors in §4.1.
- The feature ablation reports which of the eleven the agent's choices depend on.
- Any suppression claim is stated against the forced-mutation and ε-greedy floors,
  never against zero.
- If a mechanism is built: null configuration **bit-identical** to a run without it;
  determinism (SIM-05) held despite the neural forward pass in the decision loop; no
  golden moves; a composition-register entry in the same commit, and the §5 joint
  check against the sibling mechanism.
- §7's quirk list appears in the design record as a stated threat to validity.

## 10. Hard constraints

- **`replicate, never extend`.** Consuming `mtd_ai` unchanged as a defence arm may
  be sanctioned (R-B). Wiring anything of the attacker's into `attacker_sensitivity`
  is reverse-modelling detection and stays **forbidden**. The coupling stays
  indirect: behaviour changes the record, the record changes the state, the state
  changes the choice.
- **No learned inference over defender behaviour** — no ML, no RL, no value
  function, no eligibility trace. The endowed form only (§6).
- **Record the axis-8 amendment before building.** Three records carry the
  exclusion and each needs a dated amendment in the commit that starts the work:
  [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(d) axis 8, [`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md),
  and [`../implementation/architecture.md`](../implementation/architecture.md) §(f).
  *(Obligation moved here 2026-08-07 with the axis-8 scope; the sibling brief no
  longer owns it.)*
- **Do not repair** the divide-by-zero, the prefix filter, the degenerate
  `attack_path_exposure`, or any §7 quirk as part of this work — each is a substrate
  change needing its own disposition.
- Determinism (SIM-05); envelope-not-actor; within-substrate comparability only;
  Australian English; branch per session; never push.

## 11. Reading list

- `mtdnetwork/operation/mtd_ai_operation.py` § `get_state_and_time_series` (the
  eleven features and the `features` filter) and `mtdnetwork/mtdai/mtd_ai.py` (the
  reward) — §4.
- [`2026-08-06_mtd_ai_reintegration.md`](2026-08-06_mtd_ai_reintegration.md) — the
  integration, its defects, the determinism risk, reuse-vs-retrain (R-B).
- [`../implementation/pipeline/ogasp/stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
  §2(b), §8, §17 — the route's origin, its four prerequisites, the restated premise.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  axis 8 — the exclusion this amends, and the three primitives this is *not*.
- [`2026-08-06_knowledge_gated_apt_attacker.md`](2026-08-06_knowledge_gated_apt_attacker.md)
  §0, §3.1, §3.1a, §4.1, §9 — the sibling build, the falsified host-image premise,
  the saturation curve, the arc, and the composition hazard.

## 12. Out of scope

- Jalowski primitives **(ii) beacon** and **(iii) metadata-shadow invariance**.
- Any RL / value-function machinery, and any extension of Tay's agent.
- Repairing any §7 quirk.
- The vulnerability-memory build — sibling handoff, and it is axis 7.
- Dissertation prose.

## 13. Ideas parked here rather than lost

- ✚ **`mtd_ai` is needed for the evaluation, not only for this brief.** Marc's
  framing is *"so that we can get the AI-MTD up and running for our results
  pulling"* — the reactive defender is a **defence arm the results want**
  independently of any attacker mechanism. That widens R-B's stakes: even if this
  brief is never built, the reintegration has its own justification, and handoff (3)
  should be read as serving the evaluation rather than serving this.
- ✚ **The feature-filter ablation** (§4, §8) is a study in its own right — *which of
  the eleven inputs does the reactive defender's behaviour actually depend on?* — and
  it needs no attacker mechanism at all. If this brief dies at the falsifier, that
  question survives it.
- ⟲ **Retraining removes the *inherited* status the benchmark's value rests on** —
  restored here 2026-08-07, having been lost in the split. The out-of-distribution
  argument for retraining is well known: the weights were trained against the
  inherited attacker, so against the movement arm the agent is out of distribution
  and *"the attacker steered the defender"* is indistinguishable from *"the agent was
  never trained for this"*. The less-discussed cost is the other direction. Standing
  direction retains Tay's agent as an **inherited benchmark to replicate**
  ([`../workflows/project_context.md`](../workflows/project_context.md)); a retrained
  agent is a **new defender**, not a replicated one, and the defender-frozen position
  in [`../implementation/architecture.md`](../implementation/architecture.md) §(a)
  should be re-read *before* the run rather than after. Whichever way R-B lands, the
  write-up must say which agent it ran and why — the two choices support different
  sentences.
- **Per-host mutation counts** remain the one genuinely absent input; a beacon
  primitive would have to derive or instrument them. Unchanged, still excluded.
