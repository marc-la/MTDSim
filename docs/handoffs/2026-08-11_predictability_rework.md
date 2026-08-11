---
status: open
created: 2026-08-11
---

# Resolve V2 — rework the predictability baseline claim and verify the metric's name

## State of play

The 11-Aug supervisor meeting challenged the scripted baseline's P = 1 pin
([`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
§V2): the baseline attacker branches on the exploit verdict — success routes to
scanning, failure routes elsewhere — so "the next state can be called from the
given state" did not survive presentation, and the rework was conceded in the
meeting. [`predictability.md`](../implementation/pipeline/ogasp/predictability.md)
is bannered accordingly. Its own construction pins P = 1 over each model's *own
decision state*, conditioned on every variable the policy consults — so the open
question is whether that construction already answers the challenge (the verdict
is a conditioning variable, and the branch is resolved by conditioning) or the
challenge stands and the baseline figure must be measured rather than asserted.
Separately, "predictability" is likely an established term in the literature;
the name has never been checked.

## Recommended approach

1. **Formalise the baseline FSM's decision process against the code** (the
   inherited attacker's action loop), zero-trust, not against the record's
   summary: enumerate its states and the variables its policy consults at each
   decision, and locate the exploit verdict — is it an input to the *next*
   decision (P = 1 survives; the meeting answer is a presentation fix that
   states the conditioning explicitly) or an outcome revealed only after the
   move is committed (the "by construction" wording is retracted and baseline P
   is measured from traces exactly as the movement attacker's is)?
2. **Hand-trace the answer on a 4–5-node network** (the V1 protocol) so the
   reworked figure arrives pre-validated for the instrument-validation pass.
3. **Literature check on the name** — "predictability" in the MTD, adversary-
   modelling and RL-policy literatures. If the term is established with a
   different meaning, compound or qualify it (e.g. *behavioural predictability*)
   rather than coining fresh; record the collision either way.
4. **Update the record**: replace the banner with a dated resolution, annotate
   register §V2. Annotate — the pre-registered sections' commits predate the
   results and must stay legible as such.

Alternative considered: skip the formal step and just measure baseline P from
traces. Rejected — the dispute is about the *construction*, and only the
formalisation says which side of it is right; a measured 1.0 would not answer
the objection.

## Validation gate

The banner on `predictability.md` is replaced by a dated resolution; the
baseline claim is stated in a form that survives the meeting's objection
(either the conditioning argument written out against the code, or a measured
figure); the name question has a written verdict with sources; register §V2 is
annotated. The instrument-validation pass can consume the result.

## Hard constraints

- The reader-study boundary holds: nothing here moves a badge (axis 3 is
  DEMONSTRATED, axis 4 DESIGNED — the record's own §Status).
- Annotate the record; never rewrite its pre-registration history.
- No substrate changes (S2 freeze).
- Branch / commit / never-push rules per
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md).

## Reading list

- [`../implementation/pipeline/ogasp/predictability.md`](../implementation/pipeline/ogasp/predictability.md) — the pin's construction, the banner, the conditioning table
- [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md) — §V1–V2
- `mtdnetwork/operation/attack_operation.py` — the inherited attacker loop the claim is about (note: under concurrent edit on `feat/exploit-learning-mechanism` — re-verify freshness at session start)
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md) — axis 3

## Out of scope (explicitly)

Re-running the movement-attacker measurements; any change to the metric's
mathematics beyond what the baseline-pin resolution forces; axes 6–7
instrumentation.
