---
status: open
created: 2026-07-21
supersedes: 2026-07-15_l3_feedback_net_design.md
---

> **Executed 2026-07-21, then reworked on Marc's feedback — awaiting review
> (gate item 6).** The design record is
> [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
> with the authored artefact
> [`../../data/ogasp/petri/outcome_overlay.json`](../../data/ogasp/petri/outcome_overlay.json)
> and a provenance row. **The first pass was corrected on three counts and
> re-authored:** (1) the overlay is now a **ground-up conditional-likelihood
> weighting of the whole directed tactic-pair set** (per-pair "given verdict at
> `a`, how likely is `b` next", 0–1) — the coarse band-rule-plus-overrides model
> was retired; (2) **full coverage**, not the six action-bearing places (the
> action set is extensible — authored whole-space, consumed as verbs are added);
> (3) resource-development and backward edges are in. Separately, the **structural
> pre-intrusion layer was renamed the *synthetic overlay*** (its own record
> [`../implementation/pipeline/ogasp/synthetic_overlay.md`](../implementation/pipeline/ogasp/synthetic_overlay.md))
> and made **bidirectional** (forward chain recon → resource-development →
> initial-access + backward regression bridge initial-access → reconnaissance),
> reversing the recon-only resolution — committed 1a91adb.
> **Remaining:** Marc reviews the bands, the `enables` sets, and the
> success/failure rules; then the profiled-attacker build consumes it. Delete this
> handoff when that review lands.

# Design and author the success/failure outcome overlay — the net's *policy layer* as two declared binary tactic-pair weight files, composed with the substrate oracle at runtime, with a defensible framework for authoring and verifying the numbers (CKC becomes one input, not a runtime layer)

> **Supersedes the feedback-net design handoff (2026-07-15), reframed on Marc's
> direction (2026-07-21).** The mechanism is unchanged from M2 — a binary
> success/failure outcome selects between conditional weight treatments — but the
> *direction* no longer comes from a runtime CKC-phase layer (M3). Instead it is
> carried by **two hand-authored overlay files**, `SUCCESS` and `FAILURE`, each
> mapping a directed tactic-pair to a value in [0,1], applied multiplicatively to
> the existing base weights at runtime. This is the **policy layer** the binding
> note names as the missing piece
> ([`../notes/ch3_design/structure_to_behaviour_binding.md`](../notes/ch3_design/structure_to_behaviour_binding.md):
> *structure* = the net's legal-move grammar; *policy* = which enabled move fires
> and when — "the behaviour lives in the policy, about which the structural net
> says nothing"; *execution* = the walk). CKC becomes **one input among several**
> to a defensible authoring framework, not the runtime ordering itself.

## Why this reframe (the decision on record)

- **It is still M2, made concrete.** Register M2
  ([`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)):
  "binary outcome selects between conditional weight sets." Two multiplier files
  applied on the substrate's verdict *is* that mechanism; Jin sanctioned
  hand-authored numbers for now ("a binary pairing is fine — come up with some
  numbers; how you come up with them is up to you"). This handoff is not a
  departure from the minuted model — it is the M2 instantiation.
- **CKC as input, not runtime layer (reframes M3).** M3's CKC was only ever "an
  assumption of this work" for supplying forward/backward direction. A rigid
  runtime CKC layer with a blanket forward-ban on failure is too coarse. The
  overlay makes direction a **per-edge declared value** that a framework
  *selects and verifies* — and CKC is one contributor to that value (alongside
  MITRE tactic semantics, practical incident reports, literature, reasoned
  judgement), not the mechanism.
- **It is a declared knowledge layer, not reverse-engineered weights.** The
  overlay does **not** solve the nets for a "mathematically correct" set of
  weights that make the token move right on success and back on failure. It is
  real-world knowledge distilled into two files, composed with the corpus base
  weights and the substrate oracle **at runtime**, to produce the behaviour the
  dissertation measures. Envelope-not-actor holds: it encodes *plausible
  direction*, never a real actor's policy.

## State of play

- **Fixed and consumed as-is:** M2 binary outcome; the substrate is the outcome
  oracle (M4); the D3 flow-proportion **base weights stand** — the overlay
  *conditions* them, never re-derives or re-tunes them
  ([`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md) §(f)).
- **The oracle signal already exists.** The per-tactic binary success/failure
  verdict the overlay keys on is defined in
  [`../implementation/pipeline/ogasp/tactic_action_map.md`](../implementation/pipeline/ogasp/tactic_action_map.md)
  §4 (the M2/M4 contract): which `_do_*` outcome is success vs failure vs
  MTD-halt, per tactic. This handoff consumes those verdicts; it does not
  re-derive them.
- **The nets + duration + M6 overlay exist.** The five weighted structural nets
  ([`../../data/ogasp/petri/`](../../data/ogasp/petri/)), the dwell catalogue
  ([`../../data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json)),
  and the M6 synthetic pre-intrusion join (now applied as a composed overlay,
  `prefix_join.py` / `prefix_join_overlay.json` — map §6). The success/failure
  overlay is a **second, distinct** overlay: M6 fixes *structure* (a missing
  edge); this fixes *policy* (which edge fires on which verdict).
- **The evidence asymmetry is real and load-bearing.** Incident/campaign reports
  (the Sophos + DFIR AARs already in
  [`../sources/tactic_profiles/step_c/`](../sources/tactic_profiles/step_c/))
  document **success** patterns richly — what worked, in what order. They say
  almost nothing about **failure** behaviour — what an attacker does when a step
  fails and it "goes back to the drawing board." So the `SUCCESS` file is
  report-groundable and the `FAILURE` file is mostly declared judgement. Treat
  them as **different evidential tiers** and say so — the gap is itself a
  methodological finding.
- **Prior-handoff reality** (correcting "they're all executed"): the tactic→action
  map is executed (record + ledger + M6), pending Marc's map sign-off;
  **feedback_net_design is superseded by this handoff** (its live material folded
  in below); `2026-07-15_l3_profiled_attacker_build.md` (the two-way attacker) and
  `2026-07-15_l3_first_numbers.md` remain open and **downstream** of this.

## Recommended approach

**Deliverable = one design record**
(`docs/implementation/pipeline/ogasp/success_failure_overlay_design.md`) **+ the
two authored overlay files** (data, e.g.
`data/ogasp/petri/outcome_overlay.json` with `success`/`failure` blocks, or two
files — let the record decide) **+ their per-value provenance.** No stepping
*code* — that is the profiled-attacker build. Sections:

1. **The composition rule (M2).** Per place, per verdict:
   `w'(a→b) = base(a→b) × overlay_v(a→b) / Σ_b [base × overlay_v]`, `v ∈
   {success, failure}`. Multiply-then-renormalise preserves the grounded base
   proportions *within* the surviving set (never invents fresh magnitudes). An
   overlay value of `0` hard-suppresses an edge; values in `(0,1)` soft-bias it —
   **not** a blanket forward-ban on failure (Marc's refinement): forward edges may
   survive failure, suppressed selectively where a source justifies it. Name and
   kill the alternatives (substitute weight-sets; additive bias).
2. **The two files + the authoring framework.** Directed tactic-pair → [0,1], one
   `success`, one `failure`. Specify the **defensible framework that selects and
   verifies each number**: CKC phase ordering as the structural prior
   (forward-default vs backward-default), MITRE tactic semantics, the practical
   AARs (success side), literature, reasoned judgement — each value carries a
   **provenance tag** naming its source(s). Encode the evidence-tier asymmetry:
   `success` values cite report/CKC grounding; `failure` values are flagged
   declared-judgement with the failure-behaviour evidence gap stated. Label the
   whole artefact **synthetic / declared** (not flow-derived) with its own
   provenance row ([`../implementation/provenance.md`](../implementation/provenance.md)).
3. **The stall rule (Marc flagged this — genuinely open).** When the `failure`
   overlay suppresses every out-edge at a place — or the only out-edge is a
   synthetic-forward one (the M6-bridged recon islands: map §6) — the token has
   nowhere to go. Options to choose among and specify: (a) the overlay
   re-introduces a **bounded self-loop / retry** — legitimate precisely because
   the overlay is a *separate layer* not bound by the structural build's
   self-loop dropping (`build.py` drops intra-tactic self-loops; the policy layer
   need not); (b) dwell-in-place for another duration then re-fire; (c) an
   attempt-cap → forced progression. Recommend one; note the self-loop-dropping
   constraint so the choice is made knowingly.
4. **Relationship to the substrate reset model + MTD interrupt.** Two things move
   the token on failure, at **different layers**, and the record must keep them
   coherent: (a) the substrate's own reset — a `network`/`application`/credential
   mutation throws the attacker back differently (map §4 interrupt column;
   substrate-mechanical, fires regardless of the overlay); (b) the `failure`
   overlay — the net-routing policy on the binary verdict. Recommend: an MTD
   interrupt **reads as the failure verdict** so the net falls back (the feedback
   Jin's motivating example wanted) — but note the dependency: the carve's
   `step()` does **not** yet wire interrupt→driver recovery (anatomy §3 scope
   note), so this is a **build prerequisite** to name, not assume.
5. **Live-stepping, determinism, records (folded from the superseded design).**
   Token lifecycle inside SimPy: enter place → dwell (D4 duration) → fire the
   mapped action(s) via `step()` → read the binary verdict → select the overlay →
   compose + renormalise → sample the next transition under the run seed. Specify
   per-class termination (objective set reached) and horizon censoring (R4 makes
   the horizon a free experimental variable). Determinism (SIM-05): seed + net +
   overlay + substrate seed → the same walk. The per-event record schema (place,
   action, verdict, overlay branch used, transition taken, sim time) so MTTC/ASR
   and the M8 metrics review compute downstream.

*Open design questions to resolve in the record (not blockers):* whether
resource-development participates in the failure-regression structure or stays a
documented island (map §6 left it recon-only); combined file vs two files;
whether `success`/`failure` values are authored per-edge or at a phase level with
per-edge overrides (the low-parameter option).

## Validation gate

Done when:
1. The composition rule, stall rule, and interrupt policy are each specified with
   alternatives named and killed in prose — no place's failure behaviour left
   implicit.
2. Both overlay files are authored, every value provenance-tagged, with the
   success/failure evidence-tier asymmetry stated explicitly.
3. The stepping lifecycle is specified end-to-end (enter → dwell → act → verdict →
   compose → transition), including termination and horizon censoring, and the
   interrupt→failure build prerequisite is named.
4. The determinism statement and per-event record schema exist.
5. The record is implementable cold by the profiled-attacker build author, and the
   overlay is labelled a declared/synthetic policy layer (envelope-not-actor), not
   corpus-derived weights.
6. Marc has reviewed it. **No simulator or net-build code changes** — design
   record + authored data files only; the composition/stepping *code* is the build.

## Hard constraints

- **Binary outcome only (M2)** — richer outcome classes are a named extension.
- **Base D3 weights stand** — the overlay conditions the grounded proportions
  multiplicatively; never re-derive, re-weight, or hand-tune the base
  ([`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md) §(f)).
- **The overlay is a declared policy layer, not reverse-engineered weights** —
  provenance-flagged synthetic; envelope-not-actor; it is *not* solved from the
  nets.
- **Attacker-only (D5)**; the baseline MTTC event definition is untouched.
- **CKC is an input, not a runtime layer** — its ordering may seed default values;
  it does not gate transitions at runtime.
- Determinism (SIM-05); branch hygiene; **never push without an explicit ask**;
  Australian English.

## Reading list

- [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
  — §M1–M3 (the mechanism), R1 (evidence regime: "observations are long-term,
  execution is very quick"; assume from practical reports where papers don't
  exist), R4 (horizon is free).
- [`../implementation/pipeline/ogasp/tactic_action_map.md`](../implementation/pipeline/ogasp/tactic_action_map.md)
  §4 (the verdict oracle this overlay keys on) + §6 (the M6 overlay + the stall
  precedent at the bridged recon islands).
- [`../notes/ch3_design/structure_to_behaviour_binding.md`](../notes/ch3_design/structure_to_behaviour_binding.md)
  — structure / policy / execution; envelope-not-actor; the division of labour
  (timing + success from the substrate, structure from the corpus, direction is
  the declared policy).
- [`../implementation/pipeline/ogasp/action_layer_anatomy.md`](../implementation/pipeline/ogasp/action_layer_anatomy.md)
  §3 — `step()` and the interrupt→driver scope note (the point 4 build prerequisite).
- [`../sources/tactic_profiles/step_c/`](../sources/tactic_profiles/step_c/) —
  the Sophos + DFIR incident AARs: the success-pattern evidence for the `success`
  file (and the source of the failure-behaviour gap).
- The feedback-net design handoff (superseded, now deleted) — its
  composition/stepping/determinism material is folded into the design record's
  §1/§4/§5; git log is the lineage record.

## Out of scope (explicitly)

- The build — stepping/composition code is
  [`2026-07-15_l3_profiled_attacker_build.md`](2026-07-15_l3_profiled_attacker_build.md).
- R2 success-rate tuning, R3 attacker styles, the C2 capability contract, richer
  outcome classes — named extension hooks, not designed here.
- Re-weighting the base nets, duration calibration, corpus expansion.
- The standalone analytical timeline track (D1) — untouched; it stays decoupled.
