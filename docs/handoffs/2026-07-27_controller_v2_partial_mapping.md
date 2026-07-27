---
status: open
created: 2026-07-27
---

# Rebuild the controller as a partial mapping — a tactic dispatches zero or one action, unmappable tactics become dwell-only, and every mapping tried is kept in a versioned registry with what it produced

**Chain position: wave 2 — after the action-layer refinement.** Not a hard
dependency, but the audit tells you which verbs are worth mapping to and what
each genuinely requires, which is exactly the input this design needs. Executes
**S4**.

## State of play

**The ruling.** Not every tactic needs an action. A tactic maps to **[0, 1]
actions**; several tactics may map to the **same** action; and where no mapping
makes sense the tactic becomes a **non-action ("dwell-only") tactic** that
consumes simulation time without dispatching a verb. This is extensible — a
tactic gains an action if and when one exists for it. And because the controller
is **the application layer the experiments vary**, the mappings that have been
tried and what each produced must be **maintained and version-controlled**
rather than overwritten.

**What the current mapping is, and why it is being replaced.** The experiment-1
controller is a *total* map: all fifteen tactics onto exactly one of six verbs,
composed transitively through the kill chain, with the whole Actions-on-Objectives
band doubled onto the neighbour-reveal verb because nothing else covered it.
Complete coverage was the property it was built to guarantee — and S4 removes the
requirement. That coarseness is much of what produced experiment 1's two failure
modes: `initial-access` firing a port scan rather than an exploit, and six
objective-band tactics all firing the same placeholder. The map is not wrong; it
was one value of an input parameter, chosen to get the loop running. This handoff
chooses a better value and builds the machinery for choosing more.

**The runtime already tolerates unmapped places — this is the load-bearing
compatibility fact.** The routing-policy record states it directly: a place with
no mapped verb produces no verdict, so it is not conditioned and routes on the
base weights. Dwell-only places also already exist structurally —
`resource-development` is a first-class place with a zero dwell and no mapped
action. So S4 is mostly a **data and loader** change plus the loosening of one
test invariant, not a redesign of the stepping loop. Confirm this before
designing around it, but design on the assumption that it holds.

**The one invariant that must change.** The controller test currently asserts
complete coverage — every tactic resolves to a verb. The real invariant after S4
is weaker and more honest: **every tactic either resolves to exactly one verb or
is declared dwell-only, and no tactic is silently absent.** Silence must stay an
error; declared absence must become legal.

**The verb vocabulary is fixed** while the action-set freeze holds, so this
handoff maps onto the six inherited verbs or onto nothing. That constraint is
what makes dwell-only a modelling stance rather than an admission.

## Recommended approach

1. **Decide each tactic on its merits, and write the reason down per row.** Three
   outcomes per tactic: mapped (name the verb and why the verb's actual effect is
   a defensible stand-in for the tactic), dwell-only (name why no verb fits, and
   what a future action would have to do), or — for the objective tactics —
   mapped to a verb that genuinely approximates the objective act if one exists.
   Do not fill a row because a row looks empty; the point of S4 is that empty is
   an answer.
2. **Start from the tactics where a mapping is obvious and work outward.**
   Reconnaissance and discovery to the scan verbs, lateral movement to the
   neighbour-reveal and host-enumeration path, execution and privilege-escalation
   to the exploit verb, credential-access to the brute-force path. The contested
   ones are `initial-access` (port scan versus exploit — the single most
   criticised cell in the current map), the concealment and impairment tactics
   (no substrate analogue exists — strong dwell-only candidates), and the
   terminal objective tactics, which currently fire a placeholder.
3. **Respect the substrate's own pivot pattern.** Experiment 1's churn mode had a
   specific mechanism: the substrate spreads by a neighbour-reveal *followed by*
   host enumeration, and the profiles fired the first without the second, so the
   attack never pivoted. Any mapping that hopes to spread must let that pair
   occur. This is the sharpest single lesson available from the first run.
4. **Build the registry as data, not as a code branch.** One file per mapping
   version under a mappings directory, plus a manifest recording each version's
   name, date, rationale, and which experiment consumed it. The runtime selects a
   version by name; the default is the current one. The experiment-1 mapping is
   registered as version 1 unchanged, so its numbers stay reproducible.
5. **Make dwell-only observable in the records.** A dwell-only step must emit an
   event with its place, its dwell, and an explicit marker that no verb fired and
   no verdict was produced. Without that, an analysis cannot distinguish "spent
   time thinking" from "did nothing", and the action-budget decomposition that
   made experiment 1 legible would break.

*Alternatives considered:* keeping total coverage and simply choosing better
verbs — rejected, it is what S4 overrules, and it forces placeholder mappings
whose behaviour is uninterpretable. Letting a tactic map to *several* verbs in
sequence — rejected for now: it is a genuine modelling option, but it makes a
tactic a mini-plan, which changes what a verdict means and belongs to a later
decision, not this one.

## Validation gate

Done when:

1. Every one of the fifteen tactics has a row stating mapped-to-verb or
   dwell-only, each with a written reason; no silent rows.
2. The registry holds at least two versions — the experiment-1 mapping and the
   new one — with provenance, and switching between them is a data selection
   rather than a code edit.
3. The relaxed invariant is test-pinned: a tactic resolving to nothing *and* not
   declared dwell-only is still an error.
4. A dwell-only place is demonstrated end to end in a seeded smoke run: time
   advances, no verb fires, no verdict is produced, the routing falls back to the
   base weights, and the event record says so.
5. Determinism holds — the same seed and the same mapping version give the same
   walk.
6. The controller record is updated to describe version 2 as the live value while
   retaining version 1's description as the experiment-1 arm.

## Hard constraints

- **The action set is frozen (S2).** Map onto the six existing verbs or onto
  nothing. No new verb, no verb split, no new attacker state.
- **The mapping is an input parameter, not a recovered truth.** There is no
  correct mapping to discover; every version is a choice, and the registry exists
  so that choices are comparable rather than lost.
- **Do not re-impose the substrate's native call order** to reduce blocking. The
  H-coupling is a finding, and a mapping that hides it is worse than a coarse one
  that exposes it.
- **Experiment 1 must stay reproducible** — its mapping version is immutable once
  registered.
- Determinism (SIM-05); attacker-only changes (D5); Australian English; branch
  hygiene; never push without an explicit ask.

## Reading list

- [`../implementation/pipeline/ogasp/controller.md`](../implementation/pipeline/ogasp/controller.md)
  — the current map, its construction, and §4's per-verb verdict semantics, which
  carry forward unchanged.
- [`../implementation/pipeline/ogasp/attacker_phase_catalogue.md`](../implementation/pipeline/ogasp/attacker_phase_catalogue.md)
  — what each verb actually does and requires; the input to every mapping call.
- [`../implementation/pipeline/ogasp/experiment_01_findings.md`](../implementation/pipeline/ogasp/experiment_01_findings.md)
  §3 — the two failure modes this mapping is trying not to reproduce.
- [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  §3 — why an unmapped place is already safe at runtime.
- [`../implementation/pipeline/ogasp/synthetic_overlay.md`](../implementation/pipeline/ogasp/synthetic_overlay.md)
  §2 — the existing precedent for a live place with no mapped action.

## Out of scope (explicitly)

- Adding actions to cover the unmappable tactics — frozen under S2, and the
  reason dwell-only exists.
- Changing what a dwell-only tactic *costs*. This handoff makes such tactics
  legal and observable; the timing handoffs decide how their time is drawn.
- Re-running the full experiment matrix. A seeded smoke run is the gate here; the
  comparative run is experiment 2.
- Touching the transition weights.
