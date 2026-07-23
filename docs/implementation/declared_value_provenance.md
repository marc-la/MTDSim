---
status: durable
created: 2026-07-23
updated: 2026-07-23
topic: "A precedent for provenance-tracking declared-knowledge values (numbers reasoned from judgement, not measured from a source) and maintaining their justification through adversarial cross-examination — the living value-provenance & scrutiny ledger"
---

# Declared-value provenance — the scrutiny ledger precedent

Some load-bearing numbers in this project are **not measured from a citable
source**. They are **declared knowledge**: values reasoned from domain logic,
practitioner reports, literature, and intuition — an *envelope*, not a recovered
truth. The L3 outcome (policy) overlay is the first of these; there will be more.

Such values cannot be provenance-tracked the way
[`provenance.md`](provenance.md) tracks a constant back to a paper table — there
is no table. Their defensibility instead rests on **the quality of the reasoning
and the adversarial scrutiny it has survived**. This document is the **precedent**
for capturing that: a *living ledger* that travels with the values, records why
each is what it is, at what evidential tier, and how it has been reworked through
successive cross-examinations.

> **Use this when** a value is reasoned/declared (no citable measurement).
> **Use [`provenance.md`](provenance.md) instead when** a value traces to a paper,
> spec row, or the inherited code — that is a different provenance regime
> (source → locator → disposition). The two are complementary, not alternatives.

## 1. The three requirements

A declared value is only defensible if it is **reproducible, tiered, and scrutinised.**

1. **Reproducible, not post-hoc.** Declared values must be **rule-generated from a
   small model**, not hand-set per instance. A generator must reproduce the whole
   set deterministically (e.g. the overlay generator reproduces its 123-pair table
   *0/123* before any edit). This proves the values follow from stated rules rather
   than being fitted after the fact, and it makes a rework a one-line rule change,
   not a mass edit. It also kills the redundancy of storing the same value-and-reason
   per instance: the rationale lives **once per rule**.
2. **Tiered by evidence.** Every value declares its **provenance tier** (below), so
   an examiner sees exactly how grounded each number is. Hiding a weak tier behind a
   confident-looking number is the failure mode this prevents.
3. **Scrutinised adversarially.** Every value carries a **scrutiny record** — which
   review rounds saw it, what was challenged, what survived, and a current
   confidence — plus a **changelog** of how it was reworked. Scrutiny is not a
   one-off sign-off; it is a maintained history.

## 2. Provenance tiers

| Tier | Meaning |
|---|---|
| `corpus-grounded` | derived from CTI / corpus data. *(For a deliberately CTI-independent layer like the overlay, this tier must stay empty — see §5.)* |
| `attested-pattern` | the *behaviour* is documented in reports/literature (get-in/spread sequences, perimeter retry loops); the exact *magnitude* is still declared. Record it as `attested-pattern/declared-magnitude`. |
| `declared-judgement` | reasoned from first-principles logic (here: kill-chain + foothold-dependency); not attested. Reports rarely record it (e.g. what an attacker does *after a step fails*). The honest floor tier. |

Stating the tier is itself a methodological finding, not an apology: a layer whose
weak half is *labelled* weak is more defensible than one that pretends uniform
grounding.

## 3. The ledger schema

The ledger is **machine-readable, embedded with the rules** (rationale sits with
the value it explains). Per rule:

```
id            — the rule identifier (the compiled per-pair view tags each pair with it)
value         — the number
rationale     — why this value; ONE sentence, stored once per rule (never per pair)
provenance_tier — §2
status        — stable | provisional | contested
confidence    — current %, from the latest review round
scrutiny      — which rounds reviewed it, what was challenged, what survived
changelog     — [ round: from → to, and why ] — the rework history
```

A top-level `ledger_meta` block records the shared context: the tier definitions,
the `review_history` (the ordered list of cross-examination rounds), the
`reproducibility` claim (generator + the 0/N reproduction check), and the
`maintenance` protocol (§4).

## 4. The maintenance protocol — reworking through adversarial review

The ledger is **updated by the cross-examination process**, not frozen:

1. **A round runs.** A panel of independent adversarial reviewers (diverse lenses:
   DFIR fidelity, ATT&CK methodology, probabilistic coherence, a hard examiner)
   scrutinises the values, each finding **adversarially refuted** before it counts,
   and grounds claims in re-runnable evidence (routed mass, stepped traces), not
   assertion.
2. **Surviving changes fold in** as **generalising** rule edits — never
   pair-specific or profile-specific hacks (that is overfitting, forbidden). Each
   edit appends a `changelog` entry (round, from → to, evidence) to its rule.
3. **The scrutiny record and confidence update** per rule. A rule whose value moved,
   or that a reviewer contested, is marked `provisional` or `contested` and is
   **re-scrutinised next round** until it earns `stable`.
4. **A confidence panel rates the set** toward an agreed bar (here: 95%). The bar is
   met only when the residuals are *honestly stated in the record* — an unwritten
   limitation is itself a blocker.
5. **Repeat** until a round surfaces no surviving material change and the panel
   clears the bar. Then, and only then, the values are finalised.

This is the same loop whatever the values: fan-out review → adversarial refute →
generalising fold → re-scrutinise → rate. The ledger is its durable memory.

## 5. Guardrails these values must not cross

- **No reverse-engineering from the layers they condition.** A declared layer that
  *conditions* a data-grounded layer (the overlay conditions the CTI-grounded base
  weights) must be authored from declared knowledge **only** — never tuned to fit
  the data it multiplies. Diagnosing a coherence failure *with* the data is allowed;
  choosing a value *to match* the data is reverse-engineering. Keep a bot on this
  (the CTI-independence / scope-creep audit).
- **No overfitting.** Values generalise across instances (pairs) and contexts
  (profiles). Test on a corpus-neutral synthetic case to confirm a value is not
  merely masked by one context's data.
- **Complete coverage.** Author the **whole** value space (every ordered pair), not
  only the cases the current corpus exercises — so a different corpus/CTI that
  introduces a new case is already covered. Which cases *route mass* is a property
  of the data layer, not the declared layer.

## 6. Reference instance — the L3 outcome overlay

The overlay is the worked example of this precedent:

- **Rules (source of truth):**
  [`../../data/ogasp/controller/outcome_rules.json`](../../data/ogasp/controller/outcome_rules.json)
  — the model (bands / enables / foothold) + the 5 success and 9 failure rules,
  each carrying value, rationale, tier, status, confidence, scrutiny, changelog;
  plus the `ledger_meta` block.
- **Compiled views:**
  [`../../data/ogasp/controller/success.json`](../../data/ogasp/controller/success.json)
  and [`failure.json`](../../data/ogasp/controller/failure.json) — the complete
  210-pair space (corpus-agnostic), each pair `{v, rule}`, generated from the rules
  (do not hand-edit).
- **Loader:**
  [`../../src/mtdsim/l3_simulation/controller/outcome.py`](../../src/mtdsim/l3_simulation/controller/outcome.py)
  (`load_outcome_overlay`, `rule_for`).
- **Design + decision record:**
  [`pipeline/ogasp/success_failure_overlay_design.md`](pipeline/ogasp/success_failure_overlay_design.md),
  [`pipeline/ogasp/supervisor_decision_register.md`](pipeline/ogasp/supervisor_decision_register.md).

Its ledger reads: reproducible (0/123), review history **R0→R4 complete** (~90 agents:
initial cross-exam → branching red-team → composed-net validation → stepwise
simulation), all rules `stable`, final finetune synthesis an **empty change set**
(values converged). **R2 finalised 2026-07-23** (Marc greenlit) at a certified 82%; the
82→95% remainder is the dissertation defence of the reasoning, not value uncertainty —
so an honest ceiling, recorded, rather than an open gap. This is the precedent working
end-to-end: a declared-knowledge value layer carried from authoring, through adversarial
rework, to a finalised, evidence-tiered, reproducible artefact with its scrutiny logged.

## 7. Where this sits

- Complements [`provenance.md`](provenance.md) (paper/spec-sourced constants) — this
  precedent covers the *declared-knowledge* regime it cannot.
- Feeds, and is fed by, the decision register
  ([`pipeline/ogasp/supervisor_decision_register.md`](pipeline/ogasp/supervisor_decision_register.md)):
  a ratified modelling call (e.g. keep the C2-hub enables edit) lands as a rule
  changelog entry here.
- **When to update:** every cross-examination round (append scrutiny + changelog);
  when a value is finalised (flip `status`); when a new declared-value layer adopts
  the precedent (add its instance to §6).
