---
status: durable
created: 2026-07-21
updated: 2026-07-21
topic: "L3 M2 — the outcome (policy) overlay: a ground-up conditional-likelihood weighting over the whole directed tactic-pair set, composed multiplicatively with the base weights and the substrate's binary verdict at runtime"
---

# The outcome (policy) overlay — a ground-up success/failure conditional-likelihood weighting over the whole tactic-pair set

**Status:** durable. The design record that turns the **M2** ruling ("binary
outcome selects between conditional weight treatments";
[`supervisor_decision_register.md`](supervisor_decision_register.md) §M2) into an
implementable contract, in the form Marc directed on 2026-07-21. The direction the
token takes after an action is carried by a **declared policy overlay**: a
**ground-up conditional-likelihood weighting of the whole directed tactic-pair
set**. For every directed pair `a → b` and each verdict `v ∈ {success, failure}`,
the overlay declares a value in `[0, 1]` answering, *per pair*:

> given the attacker's action at tactic `a` came back `v`, how likely is `b` as the
> next move — **0 = will not happen, 1 = the most likely next course of action**.

At runtime these values **manipulate the existing base edges**: the value multiplies
the D3 base weight and the source place's out-set is renormalised, so the observed
structure is tilted live by the success/failure signal the substrate returns.

This record is the design; **no stepping or net-build code is written here** (that is
the profiled-attacker build,
[`../../../handoffs/2026-07-15_l3_profiled_attacker_build.md`](../../../handoffs/2026-07-15_l3_profiled_attacker_build.md)).
Its deliverables are this record, the authored overlay
[`../../../../data/ogasp/petri/outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json),
and its provenance row ([`../../provenance.md`](../../provenance.md)).

**What this is, and is not.** It is **structure = the net's legal-move grammar**
(the D3 nets + the synthetic overlay); **policy = which enabled move fires on which
verdict** (*this overlay*); **execution = one seeded walk**
([`../../../notes/ch3_design/structure_to_behaviour_binding.md`](../../../notes/ch3_design/structure_to_behaviour_binding.md)).
It is a **declared knowledge layer, not reverse-engineered weights** — real-world
conditional-likelihood knowledge distilled into a file, not weights solved from the
nets to make the token move a certain way. **Envelope, not actor:** it encodes
*plausible* next-move likelihoods, never a real adversary's policy. It **conditions**
the D3 base weights and never re-derives or re-tunes them
([`../../metrics_semantics.md`](../../metrics_semantics.md) §(f)); the per-tactic
binary verdict it keys on is fixed by [`tactic_action_map.md`](tactic_action_map.md)
§4 (the M2/M4 oracle) and read, never re-rolled. It is a **second, distinct** layer
from the *structural* synthetic overlay
([`synthetic_overlay.md`](synthetic_overlay.md)): that one adds edges, this one
weights them by verdict.

---

## 1. The composition rule (M2)

At a source place `a` whose action returned verdict `v`, the overlay conditions the
base out-distribution multiplicatively and renormalises within the source's out-set:

```
                      base(a→b) · overlay_v(a→b)
    w'_v(a→b)  =  ────────────────────────────────────      v ∈ {success, failure}
                   Σ_b'  base(a→b') · overlay_v(a→b')
```

- **Multiply-then-renormalise conditions without re-deriving.** It preserves the
  grounded base proportions *within* any set of edges the overlay treats alike, and
  never invents a fresh magnitude. The overlay changes *which edges carry the mass
  and how it redistributes across the verdict* — not the corpus's within-class
  ordering.
- **`overlay_v = 0` removes an edge under verdict `v`; `(0,1)` down-weights it.** The
  base weight `base(a→b)` is the D3 out-edge-normalised flow proportion (the
  `operator_dedup` variant is primary, `raw` the robustness arm — the overlay is
  variant-agnostic). Synthetic-overlay edges (the pre-intrusion chain and the
  backward regression bridge) are ordinary structure to the composition — they carry
  overlay values like any other pair (the backward bridge `initial-access →
  reconnaissance` is exactly the edge the failure treatment amplifies in the island
  profiles).

**Alternatives named and killed.** *Substitute weight-sets* (two independent
hand-authored out-distributions per place) — rejected: discards the D3 grounding and
is unbounded-parameter. *Additive bias* (`base + overlay`) — rejected: can invert the
grounded ordering and needs an arbitrary clamp; multiplicative conditioning respects
"conditions, never re-derives". *Solving the nets* for weights that move the token
"correctly" — rejected on principle: that is reverse-engineering, not declared
knowledge.

---

## 2. The value semantics and the ground-up authoring model

Each pair's two values are reasoned **from the tactic-pair's semantics — not a coarse
band bucket** — via three named factors, so the value varies pair by pair within any
band. The model is machine-readable in the artefact (`model` block); this is its
rationale.

### 2.1 The three factors

1. **Kill-chain relationship** — the coarse structural prior. Each tactic carries a
   band (0 prep, 1 intrusion, 2 consolidate, 3 expand, 4 objective); `relationship =
   forward / lateral / backward` by band distance. ATT&CK imposes no ordering — the
   band is a declared assumption (M3), used only as a prior a per-pair rule refines.
2. **Capability enablement** (`enables`) — does a **success** at `a` confer the
   capability or position `b` needs next? Each tactic has an `enables` set drawn from
   MITRE tactic semantics and the get-in/spread patterns the DFIR/Sophos incident
   AARs document (e.g. a landed foothold *enables* discovery, credential access,
   execution, escalation — so those are the strong next moves, not a return to
   external recon).
3. **Foothold dependency** — does `b`'s action require an established network
   position? Reconnaissance, resource-development and initial-access do not
   (pre-foothold); every post-intrusion tactic does. Used on the **failure** side: a
   move that needs a foothold the failure just denied is implausible next.

### 2.2 The success treatment — "given success at `a`, how likely is `b` next"

- `b` specifically **enabled** by `a`'s success → **1.0** (the modal next move).
- else **forward** (kill-chain progress) → **0.6**; **lateral** (same-phase sibling)
  → **0.5**; **backward** → **0.25**, and **0.1** if regressing to a *pre-intrusion*
  tactic (you do not re-recon after succeeding deeper).

Success leans on the grounded structure: the base weights already encode
success-biased observed workflow, and the `enables` boost sharpens the specific
next-steps the AARs attest.

### 2.3 The failure treatment — "given failure at `a`, how likely is `b` next"

- **Gate (dependency):** if `a = initial-access` failed, every **foothold-dependent**
  `b` → **0.1** (no foothold, so a post-intrusion move is out of reach); the mass
  concentrates on falling back (`initial-access → reconnaissance` = 0.9, the synthetic
  regression bridge). If `a = reconnaissance` failed ("nothing found"), a deep
  post-intrusion `b` → **0.15** and `initial-access` → **0.4** (breaking in is weaker
  but not impossible) — the sane move is to keep preparing.
- else by relationship: **backward** → **0.9** ("back to the drawing board" — the
  natural regress/retry); **lateral** → **0.7** (try a sibling tactic, an alternative
  route to the same objective); **forward** → **0.3**, or **0.35** for a
  foothold-to-foothold retry-then-advance. Forward on failure is soft-suppressed,
  **not banned** (Marc's refinement) — a retry-then-advance stays reachable.

### 2.4 Worked examples (per-pair, not band-uniform)

| Pair | rel. | success | failure | reading |
|---|---|--:|--:|---|
| initial-access → discovery | forward | **1.0** | **0.1** | foothold enables discovery; on failure there is no foothold to discover from |
| initial-access → reconnaissance | backward | **0.1** | **0.9** | do not re-recon after getting in; on failure, fall back to recon (the regression bridge) |
| initial-access → lateral-movement | forward | 0.6 | 0.1 | forward but not directly enabled (discover first); foothold-gated on failure |
| lateral-movement → credential-access | backward | **1.0** | 0.9 | a hop enables credential re-harvest; on failure fall back to the survivor credential path |
| discovery → collection | forward | **1.0** | 0.35 | discovery enables staging; on failure a retry-then-advance is possible, not modal |
| reconnaissance → initial-access | forward | **1.0** | 0.4 | recon enables entry; recon failure weakens (not bans) breaking in |

The values differ *within* the same relationship class (both `initial-access →
discovery` and `initial-access → lateral-movement` are forward, yet 1.0 vs 0.6),
which is the point: the value is the pair's conditional likelihood, reasoned from its
semantics, not its band.

---

## 3. Whole-space coverage, extensibility, and runtime consumption

**The overlay weights the whole directed tactic-pair set** the nets contain (the
union across profiles) **plus the synthetic-overlay edges** — every source tactic
(including today's dwell-only ones and resource-development), forward and backward.
This is deliberate: **the action set is extensible.** Today only six tactics carry a
substrate verb and therefore a verdict ([`tactic_action_map.md`](tactic_action_map.md)
§4); tomorrow a verb may be mapped to more (resource-development, execution,
persistence…). Authoring the *whole* space now means the policy is ready the moment a
verb is added — no re-derivation, no scoping cliff.

**Runtime consumption tracks verdict availability.** The composition rule fires at a
place only when its action returns a success/failure verdict. A place with no mapped
verb produces no verdict, so it is **not** conditioned and routes on the base weights
— but its overlay values already exist, waiting for the verb. Authoring is
whole-space; consumption grows with the action vocabulary. (This is the reconciliation
of "weight the whole set" with "conditioned by the substrate signal": the values are
universal, the *conditioning event* is per-action.)

---

## 4. The evidence-tier asymmetry

The two treatments sit at **different evidential tiers**, by construction, and the
record says so. **Success** is the more grounded side: the `enables` relations come
from MITRE tactic semantics and the get-in/spread sequences the DFIR/Sophos AARs
([`../../../sources/tactic_profiles/step_c/`](../../../sources/tactic_profiles/step_c/))
document richly — reports say what worked, in what order. **Failure** is declared
judgement: an incident report almost never records what an attacker did when a step
*failed* and it "went back to the drawing board", so the failure treatment is reasoned
from kill-chain and foothold-dependency logic, not attested. This gap is itself a
methodological finding, not a hole to apologise for; the dissertation reports it as
one and the artefact flags it (`evidence_tiers`).

---

## 5. Relationship to the substrate reset model and the MTD interrupt

Two mechanisms move the token on failure, at **different layers**; the build keeps
them coherent. (a) **The substrate's own reset** — a `network`/`application` mutation
throws substrate state (`host_stack`, `curr_ports`) back mechanically, regardless of
the overlay (map §4 interrupt column;
[`action_layer_anatomy.md`](action_layer_anatomy.md) §2.4). (b) **The overlay's
failure treatment** — net-token routing on the verdict.

**Recommended: an MTD interrupt reads as the failure verdict**, so the net falls back
(the feedback Jin's motivating example wanted; register §M1) while the substrate's
mechanical reset applies to substrate state. **Named build prerequisite:** the carve's
`step()` does not yet surface the interrupt to the driver as a verdict — wiring it is
the profiled-attacker build's job ([`action_layer_anatomy.md`](action_layer_anatomy.md)
§3 / map §4), named here, not assumed. **Scope boundary:** a mutation during a
dwell-only place's dwell raises no verdict and is not felt by the token — an honest
limitation (ties to the H-coupling hypothesis, anatomy §6).

---

## 6. Live-stepping lifecycle, determinism, and the per-event record

### 6.1 Lifecycle

Per step at the token's place `a`: **enter** and **dwell** (D4 duration,
[`tactic_durations.json`](../../../../data/ogasp/tactic_durations.json)); if `a`'s
action is available, **fire** the mapped verb via `step(verb)`, **read** the binary
verdict, **select** the `success`/`failure` column, **compose + renormalise** (§1);
else route on base weights. **Sample** the next transition under the run seed and move
the token. **Terminate** on reaching the profile's objective set, or **censor** at the
simulation horizon (R4 makes the horizon a free experimental variable).

**The degenerate case (renormalisation denominator → 0).** Because the composition
renormalises across every out-edge and the verdict values are almost never all zero,
a place with any out-edge keeps positive mass — the elaborate stall machinery an
earlier draft carried is unnecessary. The one residual case: if a verdict genuinely
zeroes every out-edge (no default rule does this today), the driver re-fires in place
(bounded retry) rather than moving — a stepping-loop detail for the build, not a net
edge. This is the only place a "stall" can arise and it is handled by a bounded retry,
not a special structure.

### 6.2 Determinism (SIM-05)

The walk is a deterministic function of **run seed + net (structure + synthetic
overlay) + outcome overlay + substrate seed**. The overlay is static data; composition
and sampling are pure given the seed; `step(verb)` reads the substrate's own seeded
dice (no new randomness on the verdict — map §5). Same inputs → same walk.

### 6.3 Per-event record schema

One record per step so MTTC/ASR and the M8 review compute downstream: `sim_time`,
`place`, `band`, `place_class` (action-bearing / dwell-only), `verb` (or `null`),
`verdict` (`success`/`failure`/`halt`/`none`), `overlay_branch`
(`success`/`failure`/`none`), `out_distribution` (the composed or base out-weights),
`transition_taken`. Raw material for the metrics, not itself a metric.

---

## 7. Resolved design questions and hard constraints

**Resolved.** *Combined vs two files* → one
[`outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json) with a
`success` and a `failure` value per pair (shared model + composition). *Per-edge vs
phase-level authoring* → **ground-up per-pair**, reasoned from tactic-pair semantics
(the coarse band rule is retired). *Resource-development* → **in the overlay** and in
the structural synthetic overlay (bridged, not an island — [`synthetic_overlay.md`](synthetic_overlay.md)),
weighted like every other source. *Coverage* → the **whole** directed tactic-pair set
(§3), not a scoped subset.

**Hard constraints honoured.** Binary outcome only (M2); base D3 weights stand
(conditioned, never re-derived — §(f)); declared policy layer, not reverse-engineered
weights (envelope-not-actor); CKC is an input (the band prior), not a runtime layer;
attacker-only (D5), baseline MTTC untouched; **no simulator or net-build code changed**
— design record + one authored data file + a provenance row; the composition/stepping
code is the profiled-attacker build.

---

## 8. Where this connects, and when to update

- **Consumes:** [`supervisor_decision_register.md`](supervisor_decision_register.md)
  §M2/M1/R1/R4; [`tactic_action_map.md`](tactic_action_map.md) §4 (verdict oracle);
  [`synthetic_overlay.md`](synthetic_overlay.md) (the structure it weights);
  [`../../metrics_semantics.md`](../../metrics_semantics.md) §(f); the AAR corpus.
- **Feeds:** the profiled-attacker build (composition, lifecycle, record schema) and
  the first-numbers matrix.
- **Artefact:** [`outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json)
  (value semantics, composition rule, the model, the resolved 123-pair table);
  provenance row in [`../../provenance.md`](../../provenance.md).
- **When to update:** if Marc revises the bands, the `enables` sets, or the
  success/failure rules; if a substrate verb is mapped to a new tactic (that place
  starts consuming its overlay values); if the interrupt→driver wiring lands (§5
  prerequisite done); if the R2 success-rate axis lands (it gates the verb upstream of
  the verdict — map §5 — and does not touch this overlay); if richer outcome classes
  replace the binary verdict (a new ruling). A design snapshot dated in the frontmatter.
