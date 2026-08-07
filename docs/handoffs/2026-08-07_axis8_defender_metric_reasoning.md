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
- **Per-host mutation counts** remain the one genuinely absent input; a beacon
  primitive would have to derive or instrument them. Unchanged, still excluded.
