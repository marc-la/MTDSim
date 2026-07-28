# Conformance audit: test the current substrate against the intent spec

**Goal.** Audit the current MTDSim substrate (`mtdnetwork/`) row by row against
[`../implementation/mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md),
producing a four-way classification per IS-ID and a disposition list for Marc. This
is the second half of the 2026-07-28 session that built the spec; Marc stated the
intent to run it "in the next prompt".

## Why this exists (state of play)

- Marc's standing concern: past "bug fixes" may have overwritten design choices,
  and he cannot always adjudicate from the implementation alone. The intent spec
  is the independent instrument — literature only, zero code contamination.
- The spec is complete: Brown 2023 read line by line (primary); Zhang 2023, Ho
  2024, Tay 2024 folded in as documented extensions (one paper per pass). ~90
  rows across §d–§n, plus declared non-features (§o), inter-paper conflicts (§p),
  and extraction gaps (§q).
- The existing [`../implementation/mtdsim_spec.md`](../implementation/mtdsim_spec.md)
  is a *different* artefact (conformance record with code dispositions already
  merged). Do not treat its dispositions as pre-answers — the point of this audit
  is an independent pass. Where the two disagree about what a *paper* says, the
  intent spec wins (built uncontaminated); flag the delta.

## Recommended approach

1. Follow the audit protocol at the bottom of the intent spec (§ "Audit protocol
   for the next session"): section by section, `[config]` rows first (static
   constant checks), then `[behav]` via the tracers
   (`python -m mtdnetwork.trace`), then `[struct]`.
2. Classify each row: **CONFORMS / CONFORMS-SUPERSEDED /
   DIVERGES-DOCUMENTED-NOWHERE / UNTESTABLE** (definitions in spec §c).
3. Record the audit in a new `docs/implementation/` file (e.g.
   `intent_conformance_audit.md`), keyed by IS-IDs, with code locators on the
   audit side only — never edit locators back into the intent spec.
4. Cross-check finished classifications against `mtdsim_spec.md` dispositions
   *afterwards*: agreements strengthen both; disagreements go on Marc's
   disposition list, not silently reconciled.
5. End with the disposition list: every `DIVERGES-DOCUMENTED-NOWHERE` row plus
   the unresolved conflicts IS-CFL-01/02/05/06 — Marc rules; nothing gets "fixed"
   in this audit.

## Hard constraints

- **Audit only — change no simulator behaviour.** Output is a record + list.
- Guardrails apply: papers are claims, not ground truth; never guess a
  disposition; the new guardrails bullet ("Bug is a verdict, not a first
  impression") is the governing rule.
- Note that S3-R (2026-07-28) re-homed attacker timing for the *movement* arm —
  the audit targets the **native substrate arm**; don't mark movement-arm
  carve-outs as substrate divergences.

## Validation gate

Done when every IS-ID in spec §d–§n carries a classification with evidence
(constant value, trace excerpt, or code locator), and the disposition list for
Marc exists. Delete this handoff in the commit that ships the audit record.

## Reading list

1. `docs/implementation/mtdsim_intent_spec.md` — the instrument (read §a–§c in full).
2. `docs/workflows/guardrails.md` — working standards incl. the new bug-verdict bullet.
3. `docs/implementation/mtdsim_spec.md` — the prior conformance record (for the *post-hoc* cross-check only).
4. `docs/implementation/trace_tool.md` — how to drive the tracers for `[behav]` rows.
5. `docs/implementation/metrics_semantics.md` — existing divergence records (C7, ATK-04) the audit will re-encounter.
