---
status: open
created: 2026-06-18
---

# Adopt + record the "behavioural envelope, not actor" framing for the GASP/OGASP attacker

> A small but load-bearing *framing* commitment, not a code task. Rationale:
> [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
> §1. **This flags canonical-spec edits, which are Marc-driven** — the next
> session proposes wording; Marc approves the spec change
> ([`../specs/guardrails.md`](../specs/guardrails.md): scope discipline).

## State of play

- Each GASP class net is the **union of 5–19 attack flows**
  ([`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md)). It is therefore a
  **possibility space** — a token taking a free walk can stitch together a
  technique-chain **no single real actor ever ran** (the note §1). The net
  **over-generates**.
- This is the single strongest line of attack on the workstream at a viva: *"your
  aggregated net is not a real APT; a traversal is a chimera."* It is correct — and
  it is only damaging if the framing pretends otherwise.
- The defensive move is to make it a **stated design choice**, not a flaw someone
  finds: the net is a **behavioural envelope / generative grammar for an
  operational objective**; a single run instantiates *one* behaviour via the
  policy; claims are about the *envelope* and about *fidelity-changing-the-answer*
  (architecture §(j)), never about reproducing a named actor.
- The architecture already says the validation claim is *"behavioural fidelity
  changes the answer", not "the model is true"*
  ([`../specs/architecture.md`](../specs/architecture.md) §(f)/(j)) — this framing
  is the **same discipline, made explicit for the aggregation step.**

## Recommended approach

**1 — State what the framing commits to and rules out.** Draft a short block:
- *Commits to:* the net is a generative grammar / possibility-envelope for an
  objective class; the four classes are *differentiated envelopes*; a simulation
  run is *one instantiation* under a declared policy; the contribution is
  *fidelity-changes-the-answer* over a CTI-grounded envelope, conditioned by
  operational objective.
- *Rules out:* claiming a single traversal *is* a specific named actor; claiming
  the MTTC over the envelope *is* a real campaign's dwell time; reading
  `observation_count`-weighted paths as actor-likelihood
  ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f)).

**2 — Place it where it binds (Marc-driven edits).**
- [`../specs/architecture.md`](../specs/architecture.md) §(j) — extend the
  fidelity-changes-the-answer block with the envelope-not-actor clause.
- [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) — note that the
  OGASP MTTC is an *envelope* statistic, not an actor's dwell, alongside the
  existing comparability boundary.
- [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) — one line at the
  class-definition that the class is an envelope over its flows, not an actor.

**3 — Use it consistently.** Every L3b/L4 claim phrased envelope-relative ("under
the `pure_steal` envelope…"), never actor-relative ("the `pure_steal` APT…").

*Alternative considered:* a *per-flow single-actor* net (one net per campaign, no
aggregation) — that would *be* an actor, but forfeits the objective-class
generalisation the thesis is built on, and re-opens the L2 partition decision.
Rejected as the default; noted as the fallback if a reviewer rejects aggregation
outright.

## Validation gate

Done when:
1. The envelope-not-actor block is **drafted** (commits-to / rules-out) and
   **approved by Marc** for the canonical specs.
2. The clause is **present** in `architecture.md` §(j) (and the one-liners in
   `metrics_semantics.md` / `02_gasp_schema.md`).
3. The L3b handoff and the L4 plan reference it as a hard constraint (already wired
   into [`./2026-06-18_l3b_execution_semantics.md`](./2026-06-18_l3b_execution_semantics.md)).

## Hard constraints

- **Canonical-spec edits are Marc-driven** — propose wording, do not unilaterally
  edit `architecture.md` / `metrics_semantics.md`
  ([`../specs/guardrails.md`](../specs/guardrails.md)).
- Keep it a **framing**, not a model change — it constrains *claims*, not code.
- Branch hygiene, **never push without an explicit ask**, Australian English.

## Reading list

- [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
  §1 — the possibility-space-vs-behaviour argument.
- [`../specs/architecture.md`](../specs/architecture.md) §(f)/(j) — the existing
  fidelity-changes-the-answer claim this extends.
- [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(d)/(f) — the
  comparability boundary + the `observation_count`-is-not-likelihood prohibition.
- [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) — the four classes as
  flow-unions.

## Out of scope (explicitly)

- Re-opening the L2 partition / aggregation decision (the per-flow single-actor
  fallback is noted, not adopted).
- Any model/code change — this is a claims-framing commitment.
