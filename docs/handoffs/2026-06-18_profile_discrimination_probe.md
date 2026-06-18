---
status: open
created: 2026-06-18
---

# Cheap go/no-go: do the four GASP profiles actually produce *distinguishable* MTD-comparison outcomes — before investing in the L3b binding?

> **Run this before [`./2026-06-18_l3b_execution_semantics.md`](./2026-06-18_l3b_execution_semantics.md).**
> Rationale and framing:
> [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
> §10. This is the make-or-break risk that is *cheaper to test than to assume.*

## State of play

- L3a structural nets are built ([`../../data/ogasp/`](../../data/ogasp/)); the
  L3b executable binding is **not** (and is the expensive part).
- **The risk:** if the four objective-conditioned profiles do not yield
  *distinguishable* attacker behaviour — and hence distinguishable MTD-mechanism
  comparisons — then the whole executable workstream inherits the **L2-synthesis
  negative-result disposition** ([`../notes/2026-05-29_l2_synthesis.md`](../notes/2026-05-29_l2_synthesis.md)
  parking-lot item: "do the four classes produce distinguishable behaviour?").
  The L2 signal is already known to be *thin but present* (technique-JSD ≈ 2.1×
  null; operator-dedup JSD 0.315 vs 0.185,
  [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) §(g)). Whether that
  survives into *behaviour under MTD* is the open question.
- A full L3b binding is **not** needed to get a first answer — a throwaway
  phase-map binding is enough.

## Recommended approach — two tiers, stop at the first clear signal

**Tier 0 — structural proxy (hours, no simulation).** From the L3a nets +
reports, compute per-class *structural* discriminators that a token-traversal
would inherit: reachable-set size from the realistic entry, shortest/longest
entry→objective path length, branching factor, distinct-path count, sink/island
structure. Test whether the four classes separate beyond a null (shuffle the
class→flow assignment, recompute). If the *structure* does not separate, behaviour
under uniform policy cannot either — **early no-go, cheaply.**

**Tier 1 — phase-map simulation probe (1–2 days, throwaway).** Bind each tactic to
one of the 6 substrate phases (the deliberately lossy mapping — note §4 level 1),
drive the inherited SimPy attacker's *phase sequence* from each class net under a
**uniform** policy, and run the existing `MTD-mechanism × {procedural baseline, 4
profiles}` sweep. Measure per-class **MTTC / ASR** distributions (seeded,
repeated). Ask only: *do the class MTTC distributions separate beyond their CIs,
and does any MTD mechanism's ranking change between the procedural baseline and a
CTI profile?*

Keep the binding **disposable** — it is a probe, not L3b. Do not add the
capability contract, timing realism, or the MTD-reset model here; those belong to
L3b and would slow the go/no-go.

*Alternative considered:* skip straight to L3b. Rejected — L3b is weeks of design
+ build; a 1–2 day probe that can return *no-go* (or *go, and here is which
classes/mechanisms move*) is strictly worth it first.

## Validation gate

Done when there is a **recorded go/no-go with a stated threshold**:
- **Tier 0:** per-class structural-discriminator vector + a null (shuffled-label)
  comparison; separation yes/no.
- **Tier 1 (if Tier 0 passes):** seeded per-class MTTC/ASR distributions across the
  MTD mechanisms, with CIs, and an explicit statement of (a) whether classes
  separate and (b) whether any MTD ranking changes vs the procedural baseline.
- A one-paragraph verdict: **GO** (proceed to L3b; name which classes/mechanisms
  carry the signal) or **NO-GO** (the profiles do not separate behaviourally →
  reframe before building; the executable thesis claim needs rethinking).

## Hard constraints

- **Throwaway binding** — do not let the probe harden into L3b; mark the code
  clearly as a probe (or keep it on a scratch path).
- **Deterministic / seeded** (SIM-05) — separation claims need repeated seeded runs
  with CIs, not single runs.
- **Within-substrate comparison only**; report the **DES** MTTC.
- **Do not touch HARM / MTD mechanisms / the orchestrator.**
- The 6-phase baseline must still reproduce the goldens.
- Branch hygiene, **never push without an explicit ask**, Australian English —
  [`../specs/session_workflow.md`](../specs/session_workflow.md).

## Reading list

- [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
  §10 (the risk) + §4 (the phase-map binding to reuse for Tier 1).
- [`../notes/2026-05-29_l2_synthesis.md`](../notes/2026-05-29_l2_synthesis.md) — the
  parking-lot discrimination item this probe resolves.
- [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) §(g) — the existing
  (thin) L2 discrimination signal the probe tests the survival of.
- [`../../data/ogasp/`](../../data/ogasp/) — the structural reports Tier 0 reads.
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  — the phase driver Tier 1 sequences.

## Out of scope (explicitly)

- The full L3b binding (capability contract, timing realism, MTD-reset model).
- Any claim about *absolute* MTTC — the probe is about *separation*, not numbers.
- Touching HARM / MTD / the substrate beyond the throwaway phase driver.
