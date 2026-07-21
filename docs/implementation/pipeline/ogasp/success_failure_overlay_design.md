---
status: durable
created: 2026-07-21
updated: 2026-07-21
topic: "L3 M2 — the success/failure outcome overlay: the net's policy layer as two declared binary tactic-pair weight treatments, composed with the substrate oracle at runtime, with a defensible authoring framework (CKC as one input, not a runtime layer)"
---

# The success/failure outcome overlay — the M2 policy layer, its composition rule, its authoring framework, and its stepping semantics

**Status:** durable. The design record that turns the **M2** ruling ("binary
outcome selects between conditional weight treatments";
[`supervisor_decision_register.md`](supervisor_decision_register.md) §M2) into an
implementable contract, in the form Marc directed on 2026-07-21: the direction the
token takes on a success or a failure is carried by a **declared policy overlay** —
two binary treatments of each directed tactic-pair, `success` and `failure`,
composed multiplicatively with the D3 base weights and the substrate's verdict
**at runtime** — not by a runtime kill-chain layer (the superseded **M3** reading).
The Cyber Kill Chain (CKC) is demoted to **one input** of the authoring framework
(the structural prior that seeds each pair's default), never the runtime mechanism.

This record is the design; **no stepping or net-build code is written here** (that is
the profiled-attacker build,
[`../../../handoffs/2026-07-15_l3_profiled_attacker_build.md`](../../../handoffs/2026-07-15_l3_profiled_attacker_build.md)).
Its deliverables are this record, the authored overlay data file
[`../../../../data/ogasp/petri/outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json),
and its provenance row ([`../../provenance.md`](../../provenance.md)).

**What this consumes, and does not re-derive.** The per-tactic binary verdict the
overlay keys on (which `_do_*` outcome is success vs failure vs MTD-halt) is fixed
by [`tactic_action_map.md`](tactic_action_map.md) §4 — the M2/M4 oracle contract.
The D3 flow-proportion base weights are fixed and stand
([`../../metrics_semantics.md`](../../metrics_semantics.md) §(f)); the overlay
*conditions* them, never re-derives or re-tunes them. The M6 pre-intrusion join is
a **separate, structural** overlay ([`tactic_action_map.md`](tactic_action_map.md)
§6, [`prefix_join.py`](../../../../src/mtdsim/l3_simulation/petri/prefix_join.py)):
M6 fixes *structure* (a missing edge); this fixes *policy* (which edge fires on
which verdict). The two compose independently and are authored apart.

**The framing this record commits to** (from
[`../../../notes/ch3_design/structure_to_behaviour_binding.md`](../../../notes/ch3_design/structure_to_behaviour_binding.md)):
*structure* = the net's legal-move grammar (D3 nets + M6 join); *policy* = which
enabled move fires on which verdict (**this overlay**); *execution* = one seeded
walk. The overlay is a **declared policy layer, not reverse-engineered weights** —
it is real-world direction knowledge distilled into a file, not a set of weights
solved from the nets to make the token "move right". **Envelope, not actor:** it
encodes *plausible direction*, never a real adversary's policy.

---

## 1. The composition rule (M2)

### 1.1 The rule

The overlay assigns each directed tactic-pair `a → b` two multipliers,
`overlay_success(a→b)` and `overlay_failure(a→b)`, each in `[0, 1]`. When the live
token sits at an **action-bearing** place `a` (§1.2), the driver fires the mapped
verb, reads the substrate's binary verdict `v ∈ {success, failure}`
([`tactic_action_map.md`](tactic_action_map.md) §4), selects that verdict's
multiplier column, and composes it multiplicatively with the base weights, then
renormalises **within the surviving out-set of `a`**:

```
                      base(a→b) · overlay_v(a→b)
    w'_v(a→b)  =  ────────────────────────────────────
                   Σ_b'  base(a→b') · overlay_v(a→b')
```

- **Multiply-then-renormalise preserves the grounded base proportions *within* the
  surviving set.** It never invents a fresh magnitude: two forward edges that the
  corpus weighted 0.3 : 0.1 keep their 3 : 1 ratio after any uniform forward
  multiplier. The overlay changes *which edges survive and their relative
  emphasis across relationship classes*, not the corpus's within-class ordering.
- **`overlay_v = 0` hard-suppresses** an edge (removes it from the surviving set);
  **`overlay_v ∈ (0, 1)` soft-biases** it (down-weights without removing).
  Crucially, failure is **not** a blanket forward-ban (Marc's refinement): forward
  edges survive failure with reduced weight (default 0.3, §2), suppressed to zero
  only where a source justifies it (no source does, today — §2.4).
- The base weight `base(a→b)` is the D3 out-edge-normalised flow proportion from
  the net's `weights` layer (the `operator_dedup` variant is primary; `raw` is the
  robustness arm — the overlay is variant-agnostic, applied to whichever base the
  run selects).

### 1.2 Where the rule applies — action-bearing places only

The overlay is **selected between only at the six action-bearing places** —
`reconnaissance`, `initial-access`, `privilege-escalation`, `credential-access`,
`discovery`, `lateral-movement` — the tactics a substrate verb realises, for which
[`tactic_action_map.md`](tactic_action_map.md) §4 defines a binary verdict. At the
**nine dwell-only places** there is *no oracle call* (no verb prices them; map
§3.3), so there is no verdict to select a column with, and the rule degenerates to
identity:

```
    at a dwell-only place a:   w'(a→b) = base(a→b)      (overlay not applied)
```

This is a deliberate scope decision with a defence: the dwell-only places already
carry a forward bias *for free* from D3, because the corpus is survivorship-biased
toward successful forward campaigns ([`../../metrics_semantics.md`](../../metrics_semantics.md)
§(f)). The policy overlay adds *conditional* direction only where a real verdict
exists to condition on. It also shrinks the authoring surface from all 122
tactic-pairs to the **51 out-edges of the six action-bearing places** (union across
profiles) — a surface small enough to author defensibly and large enough to carry
the behaviour.

### 1.3 Profile independence

One `(success, failure)` pair of values is authored per **directed tactic-pair**,
applied wherever that pair occurs across the five profiles. The policy is a property
of the pair's kill-chain semantics, not of the corpus a profile was built from, so
it does not vary by profile. Each profile applies the subset of the 51 edges its net
contains ([`outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json)
`profiles_covering_each_source`).

### 1.4 Alternatives named and killed

- **Substitute weight-sets** (two independent hand-authored out-distributions per
  place, one for success and one for failure, replacing the base). *Rejected:* it
  discards the D3 grounding entirely — the numbers would be pure declaration, not
  conditioned corpus proportions — and it is high-parameter (two full distributions
  per action-bearing place, per profile). It also violates the hard constraint that
  the base weights stand.
- **Additive bias** (`w' = base + overlay`, then clamp/normalise). *Rejected:* an
  additive term can invert the grounded ordering (a large bias swamps the corpus
  proportion instead of conditioning it) and needs an arbitrary clamp to stay in
  `[0, 1]`; multiplicative composition conditions without re-deriving, which is
  exactly the "conditions them, never re-derives" constraint.
- **Solving the nets for a "correct" weight set** that makes the token move forward
  on success and back on failure. *Rejected on principle:* that would be
  reverse-engineered weights masquerading as grounding. The overlay is declared
  knowledge, composed at runtime — not a fitted solution (hard constraint).

---

## 2. The two treatments and the authoring framework

The overlay data file is **one artefact with a `success` and a `failure` treatment**
(combined, not two files — resolved open question, §7): the composition rule and the
kill-chain band table are shared, so a single artefact keeps them coherent, mirroring
the single-artefact M6 overlay. Each directed pair resolves its two multipliers from
a **default rule keyed on kill-chain relationship**, with a small set of
**per-edge overrides**. This is the low-parameter authoring option (resolved open
question, §7): a per-edge free parameter for 51 edges × 2 treatments has no evidence
to fill it, whereas a relationship rule + grounded overrides is defensible end to end.

### 2.1 The kill-chain band — the structural prior (CKC as input)

Each of the fifteen tactics is assigned a coarse **kill-chain band** (0–4), the CKC
phase ordering used as a *prior*, not a runtime gate:

| Band | Label | Tactics |
|---|---|---|
| 0 | prep | reconnaissance, resource-development |
| 1 | intrusion | initial-access, execution |
| 2 | consolidate | persistence, privilege-escalation, defense-evasion/stealth, defense-impairment, credential-access |
| 3 | expand | discovery, lateral-movement |
| 4 | objective | collection, command-and-control, exfiltration, impact |

Bands are **coarse by design**: fine 1–14 ranks would imply a precision the evidence
does not support (real campaigns interleave consolidate/expand tactics freely), so
same-band moves are treated as lateral rather than forced into a spurious order. The
band assignment follows the conventional MITRE ATT&CK enterprise tactic ordering,
which **ATT&CK itself does not mandate** — imposing kill-chain direction is *an
assumption of this work* (M3), carried here as a declared prior and defensible
because it only *seeds* the numbers a framework then selects and a human reviews.

The **relationship** of a directed pair `a → b` is `r = band(b) − band(a)`:
**forward** (`r ≥ +1`), **lateral** (`r = 0`), **backward** (`r ≤ −1`).

### 2.2 The default rule

| Relationship | `success` | `failure` |
|---|--:|--:|
| forward | 1.0 | 0.3 |
| lateral | 1.0 | 0.8 |
| backward | 0.5 | 1.0 |

- **`success` is gentle.** Forward and lateral edges are untouched (`1.0`): the
  grounded base already encodes success-biased observed workflow, so multiplying
  them further would *double-count* the corpus's own forward bias. Only backward
  edges are trimmed (`0.5`) — a successful attacker rarely regresses, but the
  aggregation over-generates backward edges (a token can stitch one campaign's step
  onto another's; [`structure_to_behaviour_binding.md`](../../../notes/ch3_design/structure_to_behaviour_binding.md)),
  so a mild trim is warranted. The success treatment barely departs from the base —
  which is the point: **on success, trust the grounded structure.**
- **`failure` is aggressive.** Forward edges are soft-suppressed (`0.3`, **not**
  banned — a retry-then-advance or a different forward tactic stays reachable);
  lateral edges are favoured (`0.8`, try a sibling tactic — the exploit failed, try
  the credential path); backward edges are favoured (`1.0`, fall back / re-scan —
  the "back to the drawing board" move). The failure treatment departs hard from the
  base, because the base — being success-biased — does not encode failure behaviour
  at all.

### 2.3 The overrides (success-side only)

Five per-edge overrides, each grounded in an incident AAR or MITRE tactic semantics,
deviate the *success* treatment from the band default:

| Edge | default `success` | override | Grounding |
|---|--:|--:|---|
| initial-access → reconnaissance | 0.5 | **0.2** | A landed foothold is followed by internal discovery / credential access, not a return to external recon (MITRE semantics; Sophos + DFIR AARs) |
| credential-access → reconnaissance | 0.5 | **0.2** | Post-foothold tactics do not route back to external recon on success (DFIR/Sophos AARs) |
| lateral-movement → reconnaissance | 0.5 | **0.2** | Same: internal spread, not external re-recon |
| lateral-movement → credential-access | 0.5 | **0.8** | Lateral movement interleaves with credential re-harvest on the newly owned host (DFIR AARs) |
| discovery → credential-access | 0.5 | **0.8** | Internal discovery feeds credential-access targeting (DFIR AARs) |

The AAR corpus is
[`../../../sources/tactic_profiles/step_c/`](../../../sources/tactic_profiles/step_c/)
(Sophos AARs 2023–2025, the DFIR Report incident write-ups, Mandiant M-Trends,
CrowdStrike GTR) — the same success-pattern evidence the duration profiles draw on.

### 2.4 The evidence-tier asymmetry, made concrete

**`failure` carries no override — every failure value is the bare declared rule.**
This is not an oversight; it is the methodological finding, encoded structurally.
The AAR corpus documents **success** behaviour richly — what worked, in what order —
which is why every override is a success-side deviation an AAR grounds. It documents
**failure** behaviour almost not at all — an incident report rarely records what an
attacker did when a step failed and it "went back to the drawing board". So there is
no report to ground any deviation from the declared failure rule, and the failure
treatment is **declared judgement end to end**. The two treatments therefore sit at
**different evidential tiers**: `success` is base-grounded (D3, from success-biased
CTI) with AAR-grounded overrides; `failure` is a declared envelope prior. The
overlay labels this in-file (`overrides.note`, `default_rule.rationale`), and the
dissertation reports it as a finding, not a gap to apologise for.

---

## 3. The stall rule (resolved)

**The problem.** At an action-bearing place, a failure verdict can leave the token
with nowhere sensible to go: (a) if every out-edge were suppressed to zero the
renormalisation denominator is zero (does not arise under the §2.2 defaults, since no
default is zero — but an override or a future extension could cause it); (b) more
importantly, at the **M6-bridged recon islands** (`double_extortion`,
`infrastructure_setup`) `reconnaissance`'s *only* out-edge is the synthetic-forward
`reconnaissance → initial-access` (map §6), and `reconnaissance`'s every out-edge is
forward in every profile ([`outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json)
`resolved`). A recon *failure* means "nothing left to discover" (`host_stack` empty;
map §4), so routing the token *forward to initial-access* on that failure is
semantically wrong — the attacker has not found a way in yet.

**The rule (recommended): bounded retry-in-place, with a forced-progression cap.**
On a failure verdict at an action-bearing place `a`, if the failure-composed
out-distribution has **zero mass** *or* its **only surviving mass is on
synthetic-forward edges**, the driver **re-fires the mapped verb in place** — the
token does not move — up to an attempt cap `K`. This is legitimate precisely because
the overlay is a *separate policy layer* not bound by the structural build's
self-loop dropping: `build.py` drops intra-tactic self-loops from the *structure*
([README](../../../../data/ogasp/petri/README.md)), but a retry-in-place is a
*stepping-policy* behaviour (the driver re-invokes `step(verb)` on the same place),
not a net edge — so it requires **no** synthetic self-loop transition and keeps
structure and policy cleanly apart. On exhausting `K`, the driver forces progression
along the **least-suppressed forward edge** (the surviving forward mass), which
guarantees termination under the horizon (R4).

**Alternatives named and killed.**
- **(b) Dwell-in-place then re-fire** without a cap — *rejected* as a degenerate of
  the recommended rule with no termination guarantee (an island recon place with a
  persistently empty network stalls forever).
- **(c) Immediate forced progression** (no retry) — *rejected* as the default: it
  discards the "keep looking" behaviour a failed recon/discovery should exhibit, and
  collapses the low-and-slow character the profiles exist to add. It is retained only
  as the **cap backstop** of the recommended rule.
- **A synthetic self-loop transition** added to the net — *rejected:* it would put
  policy behaviour into the structure layer, contradicting the M6/this-overlay
  separation and perturbing the no-synthesis invariant the structural nets pin.

`K` is a declared stepping parameter (recommend `K = 3` as a v0 prior, swept later);
it lives in the build, not this overlay file, since it governs the *stepping loop*
not a tactic-pair weight.

---

## 4. Relationship to the substrate reset model and the MTD interrupt

Two mechanisms move the token on failure, at **different layers**, and the build must
keep them coherent:

1. **The substrate's own reset (mechanical, fires regardless of the overlay).** A
   `network`-layer MTD mutation throws the attacker back to host discovery; an
   `application`-layer mutation resets the exploit working set on the same still-owned
   host; a credential/user mutation raises no interrupt (map §4 interrupt column;
   [`action_layer_anatomy.md`](action_layer_anatomy.md) §2.4). This is substrate
   state (`host_stack`, `curr_ports`), not net state.
2. **The `failure` overlay (policy, net-routing on the binary verdict).** It routes
   the *token* among the net's out-edges.

**Recommended policy: an MTD interrupt reads as the failure verdict**, so the net
falls back — this is exactly the feedback Jin's motivating example wanted (a mutation
that severs the foothold must move the net's state; register §M1). Concretely: when
`step(verb)` at an action-bearing place returns `EXPLOIT_HALTED` (or the scan
equivalent), the driver (i) lets the substrate's mechanical reset apply to substrate
state, and (ii) selects the `failure` column for the token's next transition. The two
layers then agree: the substrate has thrown the *position* back, and the policy
throws the *token* back.

**Named build prerequisite (not assumed).** The carve's `step()` does **not** yet
wire the interrupt through to a driver-visible recovery signal — MTD-interrupt
recovery for a driven run is still routed through the native `_handle_interrupt`
([`action_layer_anatomy.md`](action_layer_anatomy.md) §3 banner / `step()` scope
note; map §4 closing paragraph). Making an interrupt legible to the driver as a
failure verdict is therefore a **prerequisite of the profiled-attacker build**, named
here so it is scheduled, not silently assumed by this design.

**Known scope boundary.** An MTD mutation *during a dwell-only place's dwell* is not
felt by the token: dwell-only places fire no verb, so no interrupt is raised against
them and no verdict is produced. The policy responds to interrupts only at
action-bearing places. This is an honest limitation (it ties to the H-coupling
hypothesis, [`action_layer_anatomy.md`](action_layer_anatomy.md) §6) and is recorded,
not hidden.

---

## 5. Live-stepping lifecycle, determinism, and the per-event record

### 5.1 The token lifecycle inside SimPy

Per step, at the token's current place `a`:

1. **Enter `a`** and **dwell** for its D4 catalogue duration
   ([`tactic_durations.json`](../../../../data/ogasp/tactic_durations.json)).
2. **Branch on place class:**
   - **Action-bearing `a`:** fire the mapped verb(s) via `step(verb)`
     ([`action_layer_anatomy.md`](action_layer_anatomy.md) §3); read the binary
     verdict `v` (success / failure / halt→failure, map §4); select the `overlay_v`
     column; compose + renormalise (§1.1); if the stall condition holds, apply the
     §3 retry-in-place rule.
   - **Dwell-only `a`:** no verb, no verdict; the out-distribution is the base
     weights unconditioned (§1.2).
3. **Sample the next transition** from the composed (or base) out-distribution under
   the run seed; move the token.
4. **Terminate** when the token reaches the profile's **objective set** (the
   objective places encoded per net — command-and-control / exfiltration / impact per
   class; [README](../../../../data/ogasp/petri/README.md)), **or** censor at the
   **simulation horizon** (R4 makes the horizon a free experimental variable, so a
   run that has not reached its objective by the horizon is a right-censored
   observation, not a failure).

### 5.2 Determinism (SIM-05)

The walk is a deterministic function of **run seed + net (structure + M6 overlay) +
outcome overlay + substrate seed**. The overlay is static data; the composition and
sampling are pure given the seed; `step(verb)` reads the substrate's own seeded dice
(no new randomness is layered on the verdict — map §5, no double-counting). Same
inputs → same walk, per SIM-05.

### 5.3 Per-event record schema

The driver emits one record per step, so MTTC / ASR and the M8 metrics review compute
downstream ([`../../../handoffs/2026-07-15_l3_first_numbers.md`](../../../handoffs/2026-07-15_l3_first_numbers.md)):

| Field | Meaning |
|---|---|
| `sim_time` | SimPy clock at the step |
| `place` | the tactic the token sat at |
| `band` | its kill-chain band (0–4) |
| `place_class` | `action-bearing` / `dwell-only` |
| `verb` | the mapped substrate verb fired (or `null` for dwell-only) |
| `verdict` | `success` / `failure` / `halt` / `none` (dwell-only) |
| `overlay_branch` | `success` / `failure` / `none` — which column composed |
| `retry_count` | retries-in-place consumed at this place (§3) |
| `out_distribution` | the composed (or base) out-weights sampled from |
| `transition_taken` | the directed pair the token moved along |

This is the raw material the evaluation chapter's metrics are computed over; it is not
itself a metric.

---

## 6. What this establishes, where it connects, and when to update

This record turns the M2 ruling into: a multiplicative composition rule scoped to the
six action-bearing places (§1), a two-treatment overlay authored from a kill-chain
band rule plus five AAR-grounded success overrides with the failure side left as a
declared envelope prior (§2), a resolved stall rule (retry-in-place with a
forced-progression cap, §3), a two-layer reset/interrupt policy with its build
prerequisite named (§4), and an end-to-end stepping lifecycle with a determinism
statement and a per-event record schema (§5). Its practical output: the
profiled-attacker build has a complete, implementable-cold contract and an authored
data file to compose.

- **Consumes:** [`supervisor_decision_register.md`](supervisor_decision_register.md)
  §M2 (mechanism), M1 (live coupling), R1/R4 (evidence regime, free horizon);
  [`tactic_action_map.md`](tactic_action_map.md) §4 (the verdict oracle) + §6 (the M6
  structural overlay this composes beside);
  [`../../metrics_semantics.md`](../../metrics_semantics.md) §(f) (the base weights
  stand); the AAR corpus
  ([`../../../sources/tactic_profiles/step_c/`](../../../sources/tactic_profiles/step_c/)).
- **Feeds:** the profiled-attacker build
  ([`../../../handoffs/2026-07-15_l3_profiled_attacker_build.md`](../../../handoffs/2026-07-15_l3_profiled_attacker_build.md))
  — the composition rule, stall rule, interrupt policy, lifecycle, and record schema;
  the first-numbers experiment matrix
  ([`../../../handoffs/2026-07-15_l3_first_numbers.md`](../../../handoffs/2026-07-15_l3_first_numbers.md)).
- **Artefact:** [`../../../../data/ogasp/petri/outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json)
  (bands, default rule, overrides, resolved 51-edge table, stall rule); provenance row
  in [`../../provenance.md`](../../provenance.md).
- **When to update:** if Marc revises the band assignment, the default multipliers,
  or the override set; if the interrupt→driver wiring lands (the §4 prerequisite
  becomes done); if the R2 per-action success-rate axis lands (it gates the verb
  *upstream* of the verdict — map §5 — and does not touch this overlay); if richer
  outcome classes replace the binary verdict (a new supervisor ruling; hard
  constraint today). This is a design snapshot dated in the frontmatter.

---

## 7. Resolved open questions

The handoff left three open design questions to resolve in this record:

- **Combined file vs two files → combined.** One
  [`outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json) with a
  `success` and a `failure` treatment. They share the band table, the composition
  rule, and the resolved edge list; splitting them would duplicate that shared
  scaffolding and invite drift. This mirrors the single-artefact M6 overlay.
- **Per-edge authoring vs phase-level with overrides → phase-level with overrides**
  (the low-parameter option). A band relationship rule supplies every value; five
  AAR-grounded overrides deviate where a source justifies it. Per-edge free
  parameters for 51 edges × 2 treatments have no evidence to fill them; the rule +
  overrides is defensible edge by edge.
- **Does resource-development participate in the failure-regression structure → no,
  it stays a documented island** (consistent with the M6 recon-only resolution, map
  §6). resource-development is dwell-only (×0, no verb, no verdict), so the outcome
  overlay never selects at it; and it has no in-edges in the island profiles, so no
  token reaches it. It is out of the overlay's scope by the same reasoning that kept
  it out of the M6 join.

## 8. Hard constraints honoured

- **Binary outcome only (M2)** — the overlay has exactly two treatments; richer
  outcome classes are a named extension, not designed here.
- **Base D3 weights stand** — conditioned multiplicatively, never re-derived,
  re-weighted, or hand-tuned ([`../../metrics_semantics.md`](../../metrics_semantics.md) §(f)).
- **Declared policy layer, not reverse-engineered weights** — provenance-flagged
  synthetic; envelope-not-actor; not solved from the nets.
- **CKC is an input, not a runtime layer** — it seeds the band prior; it does not
  gate transitions at runtime.
- **Attacker-only (D5)** — nothing here touches the network / MTD / statistics
  behaviour; the baseline MTTC event definition is untouched.
- **No simulator or net-build code changed** — design record + one authored data file
  + a provenance row. The composition, stepping, and stall-rule *code* is the
  profiled-attacker build.
