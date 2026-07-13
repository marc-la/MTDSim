---
status: open
created: 2026-07-13
---

# Investigate the Petri-net→MTDSim binding design space impartially — enumerate and cross-examine candidate bindings, position the technique→CAPEC→CWE→CVE→CVSS chain, size the substrate rework, and recommend an MVP binding that is *not* a re-skin of the phased attacker

> **Run this in a fresh session.** This brief is deliberately written for a
> session with no prior investment in any binding design. The predecessor
> handoff (`2026-07-03_l3_binding_scoping.md`, now superseded) pre-committed
> to a recommended stance before the design space was examined; this brief's
> job is the examination. **Impartiality protocol:** enumerate your own
> candidate space from the substrate code, the committed nets, and precedent
> (§ approach, steps 1–2) *before* opening the superseded handoff; then fold
> its material in as one more set of candidates and raw sections, with no
> presumption it was right. If your independent enumeration converges on its
> verb-wrapping stance, that convergence is evidence; if it doesn't, say so.
>
> **The deliverable is a scaffold for supervisor sign-off, not code.** Marc
> presents the recommended binding to Dr Hong before anything is
> implemented. Scoping only, throughout.

## State of play

- **What exists on each side of the seam.** Upstream: four weighted
  operational-objective Petri nets + an aggregate null
  ([`../../data/ogasp/README.md`](../../data/ogasp/README.md)) and a shipped
  timeline library — seeded, timed attacker-state sequences, contract
  [`../../data/ogasp/timeline/timeline_schema.md`](../../data/ogasp/timeline/timeline_schema.md)
  (`ogasp-timeline/v1`). Downstream: the inherited substrate — a 6-phase
  CKC-shaped attacker
  ([`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py))
  driving six executable verbs (SCAN_HOST / ENUM_HOST / SCAN_PORT /
  EXPLOIT_VULN / BRUTE_FORCE / SCAN_NEIGHBOR,
  [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py))
  against hosts/services carrying **synthetic vulnerabilities**: no CVE keys,
  random impact ∈ [0,10], complexity-priced `exploit_time`
  ([`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)).
  The two sides share no join key — the ontology gap
  ([`../notes/ch3_design/structure_to_behaviour_binding.md`](../notes/ch3_design/structure_to_behaviour_binding.md)
  §2) is the reason this layer exists.
- **The governing decisions.** D1/D2 (one-way v1 coupling, timed state
  sequence into the simulator), D5 (attacker-only change), D6 (manually
  defined reasonable connections as a starting point), D7 (net state →
  simulator action → outcome; state decides the outcome) — plus the
  2026-07-10 written rulings R1 (practical-report timing regime), R4
  (simulation settings are free experimental variables), R5 (tactics no MTD
  can influence are acceptable; confirms cost-only). All in
  [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md).
- **The anti-goal, from Marc (2026-07-13), and it is load-bearing:** the MVP
  binding must **not** be "simply a mapping from the Petri nets to the
  existing CKC-phased attacker". That has been done before and yields no
  meaningful results — if the bound attacker's substrate-visible behaviour
  is the old phase loop with new state labels, the whole L0→L3 pipeline adds
  nothing an examiner can see. Every candidate must pass a
  **distinguishability test**: name the substrate-observable behaviour
  (action sequence, target selection, timing structure, outcome semantics)
  that would differ between two objective classes, and between any class and
  the 6-phase baseline. A candidate that cannot name one is dead on arrival,
  however clean its implementation story.
- **The MVP criterion, from the supervisor (standing):** get the pipeline
  down end-to-end — it should be *the* hard work; it need not be correct
  first time; prefer the path that yields preliminary results early.
  Practicality and early results outrank fidelity for v1.
- **Success/fail is currently a traversal notion.** In the nets, forward
  traversal ≈ progress and the objective set defines termination; the
  timeline records state occupancy, not achievement. What "the attacker
  succeeded at tactic X" *means* against the substrate is undesigned — and
  interacts with the planned per-action success-rate axis (R2), which is
  out of scope here but must not be precluded (extension point, not design).

## Recommended approach

**Deliverable = one investigation record**
(`docs/implementation/pipeline/ogasp/binding_design_space.md` — it is
codebase-shaped cross-examination, so it lives in `implementation/`, not
`notes/`) **+ a per-tactic ledger scaffold** (draft
`data/ogasp/timeline/tactic_action_map.csv` or equivalent table inside the
record — the investigation may conclude the ledger needs different columns
than the old handoff assumed; that conclusion is itself a finding) **+ a
one-page sign-off summary** Marc can put in front of Dr Hong.

**1 — Enumerate the design space from first principles.** Before reading any
prior recommendation: from the substrate code, the net/timeline contracts,
and precedent, enumerate candidate bindings across at least these axes
(widen where the material suggests it):

- **Binding altitude:** tactic→verb wrapping (each tactic-place triggers
  existing verbs); tactic→technique→action synthesis (techniques inside the
  place, not just the place, select behaviour); new tactic-native actions
  (greenfield per-tactic capabilities); hybrids per tactic group.
- **Semantic bridge:** direct hand-authored tactic→verb map (D6);
  technique→CAPEC→CWE→CVE→synthetic-CVSS chain terminating in a tag/label
  over the synthetic vuln pool (Marc's proposal — position it: is it the MVP
  bridge, a v1.1 enrichment, or dissertation-defensible future work? What
  does the tag *buy* behaviourally at each altitude?); capability
  precondition/effect contract (known two-way upgrade path — how much of it,
  if any, pays for itself in v1?).
- **Sequencing authority:** timeline-replay, schedule-authoritative
  (actions run inside the state's window); event-authoritative (timeline
  gives order, substrate gives duration); net-driven in-SimPy stepping
  (nominally the deferred two-way coupling — but check whether a *degenerate*
  in-SimPy walk of the net is actually simpler than replay before dismissing
  it; D2 sanctions the timeline, it does not forbid comparing).
- **Success semantics (traversal-level only):** what substrate condition
  realises a tactic-state — action completion, state-gated outcome
  (D7), objective-read success (objective tactics visited *and*
  substrate-realised); how backward transitions in the net should read
  against the substrate (failure/retry? cost only?).
- **Substrate rework:** for each candidate, the **minimal change set**,
  file-by-file, and whether the synthetic vuln model (no CVE keys, random
  impact, complexity pricing) needs rework at all — versus an overlay —
  versus deferral. Any pool-touching design states its comparability
  invariant (the aggregate CVSS distribution stays fixed so baseline MTTC is
  untouched, per [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md)).

**2 — Cross-examine every candidate against five criteria, argued in prose,
kill/keep verdict each:** (a) **distinguishability** — the anti-goal test
above, the first gate; (b) **MVP practicality** — effort to preliminary
results, honestly sized; (c) **academic richness** — is there a defensible
design argument (a dissertation section), or only plumbing?; (d) **substrate
blast radius** — D5 attacker-only, goldens untouched, size of the minimal
change set; (e) **extensibility** — does it admit R2 success rates, R3
styles, and the two-way upgrade without redesign? Where criteria conflict
(they will — richness vs practicality above all), argue the trade explicitly
rather than averaging.

**3 — Only now read the superseded handoff**
([`./2026-07-03_l3_binding_scoping.md`](./2026-07-03_l3_binding_scoping.md))
and fold in: its four-section skeleton, its CVE-reconciliation sketch, its
MTD-interruption policy candidates, its cost-only reasoning (now
R5-confirmed). Record where your independent enumeration agreed and
disagreed with its stance — that record is the impartiality evidence.

**4 — Recommend one MVP binding + ledger scaffold.** The per-tactic ledger:
every tactic-place in the L3a union, with (at minimum) its bound
action/behaviour, realisation condition, cost-only rationale where
applicable (R5), MTD-interruption disposition, and the R2/R3/two-way
extension hooks — but let the investigation decide the final column set.
State what the recommendation defers and what it forecloses. Write the
one-page sign-off summary last: the recommendation, the two or three
strongest rejected alternatives and why, the decisions Jin must confirm.

*Alternatives considered (for this brief itself):* patching the superseded
handoff in place — rejected: its recommendation-first structure is the
problem, not its content; a fresh cross-examination cannot be run inside a
document that opens with the answer. Skipping straight to implementation
conceptualisation — rejected: Marc requires the binding scaffold signed off
first, and [`./2026-07-13_l3_tactic_operationalisation.md`](./2026-07-13_l3_tactic_operationalisation.md)
builds on this record's output.

## Validation gate

Done when:
1. The investigation record enumerates the design space across all five axes
   with **at least three materially distinct end-to-end candidates** (not
   variations on one), each with a kill/keep verdict argued against the five
   criteria.
2. **Every candidate carries the distinguishability test** — the named
   substrate-observable behaviour separating classes from each other and
   from the 6-phase baseline — and no re-skin survives.
3. The technique→CAPEC→CWE→CVE→CVSS chain has an explicit position (MVP /
   v1.1 / future work) with the comparability invariant stated if it touches
   the vuln pool, and marked **pending supervisor confirmation**.
4. The substrate minimal-change set is stated file-by-file for the
   recommended candidate, and it respects D5 (attacker-only; no behavioural
   change to network/MTD/statistics paths).
5. The per-tactic ledger scaffold covers every tactic-place in the L3a
   union, with rationale per row and R5 recorded on every cost-only row.
6. The one-page sign-off summary exists; Marc has reviewed the record before
   it goes to Jin.
7. The impartiality evidence exists: the record states what was enumerated
   before the superseded handoff was read, and where they diverged.
8. **No code changes anywhere.**

## Hard constraints

- **Scoping only** — no simulator code, no substrate edits, no new actions.
- **Attacker-only scope (D5)** — the recommended design must not require
  touching HARM / network / MTD mechanisms / `mtdnetwork/statistic/` maths;
  the post-2c goldens ([`../../baseline/golden/`](../../baseline/golden/))
  remain the untouched oracle.
- **No IDS / detection** — cost-only is the confirmed disposition (R5);
  detection-conditioned meaning stays deferred (D6/D10).
- **ATT&CK ≠ CVE** — never join techniques directly onto synthetic vulns; a
  designed bridge (tag/label or better) is the only sanctioned path, and any
  pool-touching design states its fixed-distribution invariant.
- **R2 (success rate) and R3 (styles) are out of scope** — extension points
  to preserve, not axes to design; they belong to the
  tactic-operationalisation handoff.
- **Papers are claims** — BRON / CTID crosswalks / Caldera internals are
  unextracted; reconcile before citing
  ([`../workflows/guardrails.md`](../workflows/guardrails.md)).
- Envelope-not-actor phrasing; Australian English; branch hygiene; **never
  push without an explicit ask**.

## Reading list (in this order — the order is the impartiality mechanism)

1. [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
   — D1–D10 + R1–R5; the rules of the game.
2. [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py),
   [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py),
   [`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
   — the substrate's verbs, phase loop, and synthetic vuln model, first-hand.
3. [`../../data/ogasp/timeline/timeline_schema.md`](../../data/ogasp/timeline/timeline_schema.md)
   + [`../../data/ogasp/README.md`](../../data/ogasp/README.md) — what the
   upstream actually emits.
4. [`../notes/ch3_design/structure_to_behaviour_binding.md`](../notes/ch3_design/structure_to_behaviour_binding.md)
   — the ontology-gap argument and encoding ledger (conceptual base, not a
   binding decision).
5. [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md)
   — §(a) the MTTC event definition no success model may silently change;
   §(d) comparability boundary.
6. **Last, after your own enumeration:**
   [`./2026-07-03_l3_binding_scoping.md`](./2026-07-03_l3_binding_scoping.md)
   — the superseded predecessor, as candidate material.

## Out of scope (explicitly)

- Any implementation — the replay attacker
  ([`./2026-07-03_l3_replay_attacker.md`](./2026-07-03_l3_replay_attacker.md))
  stays deferred until this and the operationalisation scaffold are signed
  off.
- Designing the R2 success-rate model or R3 style vectors
  ([`./2026-07-13_l3_tactic_operationalisation.md`](./2026-07-13_l3_tactic_operationalisation.md)).
- Acquiring/ingesting BRON, CTID mappings, or NVD data — position the chain;
  ingestion follows supervisor confirmation.
- Detection/IDS, adaptive policies, multi-token concurrency, two-way
  coupling (upgrade-path notes only).
- Timing calibration (re-sequenced post-MVP per R1; see the re-sequenced
  operational-objective-criteria handoff).
