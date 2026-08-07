---
status: open
created: 2026-08-07
---

# Axis 8 by the other route — an attacker that knows what the defender measures, and steers it

**Split out of
[`2026-08-06_knowledge_gated_apt_attacker.md`](2026-08-06_knowledge_gated_apt_attacker.md)
on 2026-08-07 (Marc), which keeps its §5 material only as a pointer here.** That
brief is a *learning* build — vulnerability memory feeding the exploit decision —
and it kept acquiring an axis-8 half that does not belong to it. The two are
separable and the test that separates them is in §1. Nothing is lost: §5, §5.1 and
§5.2 of that brief are absorbed here in full.

**Gated on R-B**, the `mtd_ai` sanction, which Marc is probing in a parallel
session. Nothing here can run until that returns. **Design only; no code has been
written and none should be.**

---

## 1. Why this is a separate handoff — the test that splits them

Both briefs give the attacker memory, so it is fair to ask why they are two things.
The test is **does the capability reference the defender?**

- The vulnerability memory **does not**. It estimates `P(this exploit works)` from
  its own past attempts, and it would behave identically with MTD switched off.
  That is learning (axis 7), and calling it scheme awareness over-claims.
- This mechanism **does**. It exists only because a defender computes metrics from
  the attacker's own activity and selects mutations from them. Remove the defender
  and the capability has no referent at all.

That is the line, and it is worth stating in both records so the axis-8 claim is
never made by the wrong mechanism.

### What it is *not* — a scoping correction that must not be quietly dropped

**This is not one of Jalowski's three §4.1 primitives.** Those are (i)
state-collision recognition, (ii) MTD-event-as-beacon, (iii) metadata-shadow
invariance. This is closest to (iii) and is not it. The claim rests instead on
Jalowski's **§4.3 corrective** — research must shift toward *"smart, adaptive
attackers who understand the MTD scheme and look for the mathematical logic behind
the movement"* — which is the axis's own framing sentence and which this mechanism
answers directly. Say that plainly rather than filing it under a primitive it does
not satisfy; an examiner who reads §4.1 will check.

Primitives **(ii) beacon** and **(iii) metadata-shadow invariance** remain
excluded, and this brief does not ask for them.

---

## 2. The channel — what the reactive defender's state is actually made of

Read from `mtd_ai_operation.get_state_and_time_series` (lines ~299–438). **This is
a code reading, not a measurement, and every line needs verifying by an
instrumented run before anything is built on it.**

The state is eleven features. The load-bearing ones are attacker-derived, and
**four are directly steerable by attacker behaviour**:

| feature | how it is computed | the lever |
|---|---|---|
| `host_compromise_ratio` | compromised hosts **in the last 60 s** ÷ total hosts | **spacing.** Three compromises inside a minute read 3/50; the same three over five minutes read 1/50 at any instant. Temporal spacing lowers a defender input *mechanically* |
| `roa`, `risk` | the **last** exploited vulnerability's `(complexity·impact)/exploit_time` and `complexity·impact` — `[-1]`, a single sample, not an aggregate | **vulnerability selection.** Preferring low-impact vulnerabilities sets what the defender reads |
| `overall_asr_avg` | `compromised_num / attack_event_num`, denominator counting **`SCAN_PORT` rows only** | **the scan:exploit ratio.** More reconnaissance drives observed ASR down |
| `overall_mttc_avg` | mean **duration** of `SCAN_PORT` / `EXPLOIT_VULN` / `BRUTE_FORCE` rows | **tempo.** Longer actions raise it |

**The training reward closes the loop:** `overall_asr_avg`, `roa` and `risk` carry
**−75**, `overall_mttc_avg` carries **+75**. So an attacker that spaces its
compromises, prefers low-impact vulnerabilities, scans more than it exploits and
moves slowly makes the defender's state read *safe*.

**The suppression target is real and reachable.** `mtd_ai`'s action space includes
`action == 0`, a genuine DO NOTHING that gates the whole register-and-trigger block
([`2026-08-06_mtd_ai_reintegration.md`](2026-08-06_mtd_ai_reintegration.md) §1). So
"bias the defender toward doing nothing" is an action the agent can take and that
attacker behaviour can make more likely — not a metaphor.

### 2.1 Two ceilings, both quantified — report against these, never against zero

`static_degrade_factor = 2000` forces a **random** mutation after 2 000 s of
inaction (≈ 7 forced mutations per 15 000 s run whatever the attacker does), and
`choose_action` is ε-greedy, so a deploying action fires regardless of state.
Any suppression figure quoted against zero is wrong by construction.

---

## 3. The ruling — endowed, not learned (Marc, 2026-08-07)

The capability is **endowed**: the attacker is granted a declared policy derived
from an offline analysis of what the defender reads. It does **not** learn the
input→output relation at runtime.

This matters because the two forms sit on opposite sides of the original axis-8
exclusion. A learner re-engages that exclusion head on — its stated reason was that
the primitives need *"an inference capability — machine learning or reinforcement
learning over observed defender behaviour"*, and a runtime learner is precisely
that. The endowed form is the **envelope, not actor** rule the criterion already
applies everywhere: a run is *"one instantiation of a behavioural envelope under a
declared policy"*. No learning at runtime, one declared family, ablatable to null.

**The limitation is stated, not hidden: the inference is granted, not modelled.**
Marc's own framing — *"we can pretend the smart APT model has successfully used
side-channelling techniques and deduced how to manoeuvre"*. Write that into the
badge text. The claim becomes *"an adversary that has already characterised what
this defender measures behaves thus, and here is what that buys it"*, which is a
claim this project can support. Without that sentence it is an over-claim.

---

## 4. The serious threat to validity — read this before designing anything

**The four levers may be implementation quirks rather than defence properties**,
and an attacker tuned against them is **gaming Tay's implementation, not evading a
defence**. A thesis claim built on that is a claim about a bug. Five specifics, the
first three carried from the parent brief and the last two found 2026-08-07:

1. A **60 s window** on `host_compromise_ratio` that appears nowhere in Tay's paper.
2. `roa` / `risk` read as a **single most recent sample** (`[-1]`), not an aggregate.
3. An **ASR denominator counting only `SCAN_PORT`**, one of the three attack verbs.
4. **The ASR and MTTC features describe a run *prefix*, not a recent window.**
   `sub_record = record[record['cumulative_compromised_hosts'] <= compromised_num]`,
   where `compromised_num` is the last-60 s count — so the filter selects the
   opening stretch of the run during which the *cumulative* total had not yet
   passed the *recent* count. A quiet attacker does not merely lower these
   features, it **re-scopes which part of the run they describe**.
5. **The unguarded divide-by-zero triggers on the mapping, not on tempo.**
   `attack_success_rate = compromised_num / attack_event_num` has no guard, and on
   the movement arm the number of `SCAN_PORT` rows is a function of the
   tactic-to-verb mapping. A profile whose mapping dispatches few `SCAN_PORT` verbs
   zeroes the denominator however loud it is. Check the mapping before running.

**The honest form of the claim, and it should be fixed now rather than negotiated
later:** *behavioural change alters what this reactive agent observes* — never *the
attacker defeats reactive MTD*. State the quirk list as a threat to validity in the
design record so an examiner reads it from you rather than finding it.

---

## 5. Recommended approach — the cheap falsifier first, and it may end the work

**Run the profiled attacker against the reactive selector as it is, with no
attacker mechanism at all.** The five profiles already differ enormously on the
quantities the state actually reads — compromise-derived ones above all: the
profiled attacker compromises 0.5–5 hosts where the inherited one compromises ~39.
That is a naturally-occurring spread, obtained for free.

**Report the mutation-choice distribution, not just the outcome.** The claim is
that attacker behaviour changes *what the defender does*, so the distribution over
chosen actions — including `action == 0` — is the measurement. If the selector's
choices do not differ across a spread that large, no declared policy will rescue
the claim, and one cheap run has saved an expensive build.

**One premise was restated on the exposure reader's evidence and must not revert.**
This route has historically been argued as *a slower attacker presents a different
signal stream*. The slowness half does not survive a per-action reading: counted as
actions rather than attack-record rows the profiled attacker takes **more** steps
per run than the inherited one (463–674 against 371), and at the exposure reader's
tier-null setting the two arms' event tempo does not separate at all. The channel
relocates rather than closing — what the state reads is dominated by
compromise-derived quantities. **Frame it as *does a low-yield attacker change what
the reactive defender does*, never as a tempo claim.**

Only if that returns positive: design the declared policy, one family, ablatable to
null, swept over its band against conclusions committed before any run.

---

## 6. Validation gate

- The cheap falsifier reports a **mutation-choice distribution per profile**, with
  the `action == 0` share called out separately, against the two floors in §2.1.
- Any suppression claim is stated against the forced-mutation floor and the
  ε-greedy floor, never against zero.
- If a mechanism is built: null configuration **bit-identical** to a run without
  it; determinism (SIM-05) held despite the neural forward pass in the decision
  loop; no golden moves; a composition-register entry in the same commit.
- The quirk list of §4 appears in the design record as a stated threat to validity.

## 7. Hard constraints

- **`replicate, never extend`.** Consuming `mtd_ai` unchanged as a defence arm may
  be sanctioned (R-B). Wiring anything of the attacker's into `attacker_sensitivity`
  is reverse-modelling detection and stays **forbidden**.
- **No learned inference over defender behaviour** — no ML, no RL, no value
  function. The endowed form only (§3).
- **Do not repair** the divide-by-zero or any quirk in §4 as part of this work; each
  is a substrate change needing its own disposition.
- Determinism (SIM-05); envelope-not-actor; within-substrate comparability only;
  Australian English; branch per session; never push.

## 8. Reading list

- `mtdnetwork/operation/mtd_ai_operation.py` § `get_state_and_time_series` and
  `mtdnetwork/mtdai/mtd_ai.py` — the state and the reward (§2).
- [`2026-08-06_mtd_ai_reintegration.md`](2026-08-06_mtd_ai_reintegration.md) — the
  integration, its defects, the determinism risk, and reuse-vs-retrain (R-B).
- [`../implementation/pipeline/ogasp/stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
  §2(b), §8, §17 — the route's origin, its four prerequisites, and the restated
  premise.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  axis 8 — the exclusion this amends, and the three primitives this is *not*.
- [`2026-08-06_knowledge_gated_apt_attacker.md`](2026-08-06_knowledge_gated_apt_attacker.md)
  §1, §9 — the sibling build, and the composition hazard if both ever run together.

## 9. Out of scope

- Jalowski primitives **(ii) beacon** and **(iii) metadata-shadow invariance**.
- Any RL / value-function machinery, and any extension of Tay's agent.
- Repairing `mtd_ai`'s divide-by-zero, the 60 s window, or the prefix filter.
- The vulnerability-memory build — that is the sibling handoff, and it is axis 7.
- Dissertation prose.
