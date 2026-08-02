---
status: open — Part A done 2026-08-02; blocked on Marc's dispositions (D-20, D-21, D-22)
created: 2026-08-02
updated: 2026-08-02
---

# Boundary review 3 of 3 — ATTACKER / DEFENDER: the direct couplings that bypass network state, and whether they price every mechanism's disruption fairly

**Programme framing.** Third of the three boundary briefs Marc directed on
2026-08-02; shared rationale and ownership rule at the head of
[`2026-08-02_boundary_network_attacker_integration.md`](2026-08-02_boundary_network_attacker_integration.md).
This brief owns everything that flows between defender and attacker *without*
passing through network state. Marc's mental model expected this boundary to be
small — "only the confusion penalty ... and any other disruption signals out to
the controller layer". The 2026-08-02 survey found it is **six channels, not
one**, and for at least two mechanisms in the reported family these channels
are their *entire* measured effect — which makes this the boundary where
comparative fairness is most load-bearing, not least.

## 0. Where this stands (Part A session, 2026-08-02, branch `chore/boundary-attacker-defender-review`)

**Part A is complete; no code, golden or experiment record was touched.** The
deliverable is
[`../implementation/boundary_attacker_defender_channels.md`](../implementation/boundary_attacker_defender_channels.md)
— the six-channel inventory with locators, the (class × `curr_process` × arm)
truth table verified by *executing* the real gate and cost functions, the
integration demonstrations at seed 42 in both tracers, the realised channel
traffic extracted from the recorded experiment-2 and frontier data, and the
exposure measurement. Three disposition requests are opened on the audit's
list: **D-20** (ratify class-level pricing as the stated model — the §2
framing decision), **D-21** (ratify the movement arm's interrupt-exposure
profile as mapping policy), **D-22** (flag-grade counter asymmetry under
overlapping mutations). Recommendations in each row; none is a fix request.

Headline results, against this brief's questions:

- **The class flattening is now measured, not structural**: within a class the
  recorded channel traffic is identical (movement-arm interrupts 75.0/75.0 for
  the network pair, 52.7/52.4 for the application pair; penalty/interrupt
  20.49–20.52 in every cell; `forgettings == interrupts` exactly in the
  learner arm). The §c verdict is that class-level pricing **conforms** — the
  class abstraction is the documented model (Brown §III-D, Zhang §4.4.2,
  IS-MTD-09) — so D-20 asks for ratification, not repair.
- **§2's "also in scope" items are answered.** Interrupt exposure under
  movement driving: the structural worry is falsified — dwell-only places are
  deliberately exposed (`DWELL` sentinel, live-demonstrated); the app-immune
  time is the recon-verb share, 17–43 % of clock by profile, giving
  application-class reach 57–83 % (movement) vs ~99 % (native) → D-21.
  Scheduling: suspensions are zero outside the simultaneous scheme (38/run
  there, both arms) and per-mechanism trigger counts are near-equal in every
  multi scheme — no mechanism buys materially fewer channel-1 events → folded
  into D-20's model. Penalty scale: provenance-faithful (Brown §V-A / Zhang
  §4.4.3), same order as the declared dwells, 7–17 % of the movement clock —
  flagged, no re-tune proposed.
- **Adversarial pass:** no seventh defender→attacker channel found; the one
  attacker→defender input (`curr_process`, including the announce-before-dwell
  fix and the `DWELL` sentinel) is recorded as part of channel 1. Channel 6
  re-verified dead repo-wide.

**Confidence evaluation (§5), run 2026-08-02.** Checklist: six channels
inventoried and verified with locators — **yes** (record §(a)–(b)); the truth
table complete and demonstrated — **yes** (executed probe + both tracers);
realised traffic extracted from recorded data — **yes** (record §(c), no
re-run); every flattening dispositioned or D-numbered — **yes** (D-20..D-22
opened; D-07/D-09/D-18/D-19 consumed, not re-opened); adversarial pass found
no seventh channel — **yes**. Residual doubts, named: (i) the exposure
diagnostic ran undefended (current substrate, declared) — defended dynamics
shift the mix slightly, but the recorded defended yields (0.70 vs 0.99)
corroborate the figures, so not ranking-plausible; (ii) stale
`curr_ports`/`curr_vulns` after an application-class mutation on the movement
arm (no forced re-scan refreshes them) is a network-state-mediated effect
owned by briefs 1–2 — it hits both application mechanisms identically, so it
cannot reorder *within* this boundary's question; (iii) the batch-scheme
serialisation delta (IS-SCH-05) affects both arms and all mechanisms alike.
None is ranking-plausible, so the structured judgement is **≥ 95 % that the
direct channels price disruption per the documented class model and that no
unstated channel asymmetry could change a comparative ranking — conditional on
Marc ratifying the model those channels implement (D-20/D-21)**. The gate
therefore passes as a Part A verdict; the handoff stays open only for the
dispositions.

**To close:** Marc rules D-20, D-21, D-22. On (a)-recommendations throughout,
no Part B code exists — land any reporting consequence (decision-C-style
statements ride with the indistinguishability brief's D-18/decision C), then
delete this file. Any (b)-option triggers Part B under §4's discipline.

## 1. Goal

Establish, at 95 % confidence (§6), that the direct attacker/defender channels
price each mechanism's disruption according to its documented defence idea
rather than according to its resource-class label — under both driving modes
of the one substrate attacker (native FSM, and movement-driven via the
controller; see brief 1's operating picture) — or that every class-level
flattening carries a Marc disposition. The stake, concretely: for
the movement attacker, `(complete_topology, ip_shuffle)` are measured identical
*because* their network-state writes are unread (briefs 1/2) and their direct
channels are **class-identical by construction**. If the direct channels
flatten mechanism differences within a resource class, then for any mechanism
whose network write is weakly coupled, the evaluation is comparing resource
classes, not mechanisms.

## 2. State of play — the six channels, code-verified 2026-08-02

1. **The interrupt condition** (`mtd_operation.py:211-258`): whether a firing
   mechanism interrupts the in-flight action at all is decided by resource
   class × current verb — `network` interrupts any alive action;
   `application` only SCAN_PORT / EXPLOIT_VULN / BRUTE_FORCE; `reserve` only
   BRUTE_FORCE (D-07 fix). No per-mechanism term; no check of whether the
   mutation touched the attacker's current host.
2. **The confusion penalty** (`attack_operation.py:161-208`):
   `exponential_variates(ATTACK_DURATION['PENALTY']=20, 0.5)`, identical for
   every mechanism and both arms (deliberately substrate-owned per the S3
   reversal ruling recorded in the docstring); absorbed, not stacked, under
   overlapping mutations.
3. **The lost connection / cursor clear** (`attack_operation.py:206-208`):
   network-class mutations clear the host cursor (B-INT-01); application-class
   cost the service connection only (B-INT-02). Again class-level, not
   mechanism-level.
4. **Forced re-scan succession**: native FSM hard-codes the recovery verb by
   class (network → SCAN_HOST, application → SCAN_PORT, reserve → EXPLOIT_VULN
   path; `attack_operation.py:210-249`); the movement driver owns its own
   succession and reads the interrupt as a **failure verdict** — which is the
   controller-layer disruption signal Marc anticipated.
5. **The verdict's downstream consumers (movement arm only)**: the failure
   verdict feeds the outcome overlay's routing response, the axis-7 learner
   (whose belief additionally **perishes by a declared fraction on every
   mutation** — a defender-to-attacker channel that exists nowhere in the
   substrate), and the interrupt counters the measurement suite reports.
6. **The unwired observation channel**: `adversary.observed_changes`
   (`adversary.py:23`) — the vestigial attacker-observes-defender hook; empty,
   never read or written, and **ruled out of scope** (axis 8 exclusion, Marc
   2026-07-28). It stays unwired; it is listed so the review states the
   boundary's full inventory, not because work is invited.

**The fairness question, sharpened.** Channels 1–4 are functions of
`resource_type`, so within a class every mechanism buys exactly the same
disruption per trigger. That is a *defensible model* (a class abstraction of
"how a defender thwarts") — but combined with brief 1/2 findings it produces
measured equivalences that look like defence facts: CTS (full topology
regeneration) and IPShuffle (a relabel nothing reads) deliver the same
interrupt, the same penalty draw, the same cursor clear. The review must
decide-with-Marc whether class-level pricing is the intended model
(document it as such, and let decision-C-style cardinality statements carry
the consequence) or whether any mechanism-level differentiation is wanted
(e.g. a mutation-scope term), which would be a substrate semantics change
with full golden cost.

**Also in scope, because they gate the channels' reach:**

- **Interrupt exposure under movement driving**: channel 1 keys on the current
  verb of an alive attack process; the profiled traversal spends 37–43 % of
  visits in tactics that dispatch nothing. What can interrupt the substrate
  attacker during non-dispatching dwell, per class? This is a property of how
  the controller mapping holds the process, not of a second attacker — if
  application-class mechanisms structurally cannot reach movement-driven runs
  during most of the clock, that is a mapping-owned pricing asymmetry the
  comparative evaluation inherits. Measure it, then classify it as mapping
  policy to keep, or mapping defect to fix in the seam (a controller-layer
  change, not a substrate one).
- **Scheduling as an implicit channel**: priority ordering (`MTD_PRIORITY`,
  undocumented, IS-SCH-06), suspend-vs-discard (§l item 7), and resource
  contention determine each mechanism's *trigger frequency* under the
  simultaneous scheme — a mechanism discarded more often buys fewer channel-1
  events. Interrupt counts per mechanism should be extracted from existing
  run data before any new run is contemplated.
- **Penalty scale realism** (flag only): PENALTY = 20 against declared tactic
  dwells and 200 s mutation intervals — is a flat 20-unit confusion cost the
  right *order* for both arms? Provenance check, not a re-tune.

## 3. Recommended approach — Part A (review / cross-examination; no code changes)

1. **Inventory and verify the six channels** with locators and a truth table
   per driving mode: for each (mechanism × verb × driving mode), does a
   trigger interrupt, what does it cost, what state is lost, what signal
   reaches the controller. Live-verify the table's load-bearing rows with the unified
   tracer (token / controller / substrate views — this boundary is exactly
   what it was built to expose).
2. **Extract the realised channel traffic from recorded data**: per-mechanism
   interrupt counts, penalty time totals (the tracer already reports
   "attacker time lost to confusion"), and discard/suspension rates from
   experiment 2 and the frontier runs — the class-flattening claim becomes a
   measured statement rather than a structural one.
3. **Classify against the intent spec** (§c): IS-INT-01..06 rows and
   IS-ARC-01's "interrupt attack actions" edge are the documented intent for
   this boundary; the class-level abstraction, the verb gates, the
   absorbed-penalty rule and the movement-arm verdict seam each get a
   verdict: documented intent, documented-nowhere candidate, or S3-R design
   working as recorded (the seam's declines are *not* candidate divergences —
   the indistinguishability brief's §1.2 precedent).
4. **Findings table with costed options** for Marc — including the explicit
   framing decision above (class-level pricing as documented model vs
   mechanism-level differentiation), appended to the audit's disposition
   list. This is the boundary where "keep and document" is likeliest to be
   the right answer; the review's value is making the pricing model a stated
   one.

## 4. Part B (implementation; only after Marc's dispositions)

Identical discipline to briefs 1–2: dispositioned changes only; D-05 procedure
for anything that moves goldens (channel changes move **everything**, both
arms — say so in every option's cost line); SIM-05; regression tests pinning
the dispositioned channel semantics (e.g. the interrupt truth table as a test);
no recorded experiment re-run.

## 5. The A/B cycle and the confidence gate

Same standing instruction as briefs 1–2, with this boundary's question: **"Are
we ≥ 95 % confident that the direct channels' pricing of each mechanism's
disruption is either faithful to its documented defence idea or explicitly
dispositioned as a class-level model — under both driving modes, with
mapping-owned differences dispositioned as mapping policy — and that no
unstated channel asymmetry could change a comparative ranking?"** Checklist: six channels
inventoried and verified; the (mechanism × verb × arm) truth table complete
and demonstrated; realised traffic extracted from recorded data; every
flattening dispositioned or D-numbered; adversarial pass found no seventh
channel. Residual doubts named; a ranking-plausible doubt fails the gate and
scopes the next A/B iteration, recorded in this handoff.

## 6. Validation gate

1. The channel inventory + truth table exist as an implementation record,
   live-verified, with realised-traffic figures from recorded runs.
2. The class-vs-mechanism pricing question is put to Marc with costed options
   and carries his written disposition; any Part B changes landed under the
   D-05 procedure with the truth-table regression test.
3. The arm-asymmetry question (interrupt reach during non-dispatching dwell)
   is answered with measurements, and classified.
4. A passed confidence evaluation written into this handoff's final update.

## 7. Hard constraints

- §c classification first; only Marc's disposition makes anything fixable.
  The S3-R seam's declines are settled design, not candidates — do not
  re-open them; the axis-8 exclusion stands — channel 6 stays unwired.
- Channel changes touch both arms and every golden: no change lands without
  a disposition, the D-05 procedure, and a stated comparability boundary.
- No recorded experiment re-run. Extract from recorded data before running
  anything new; any new diagnostic run is a run of the *current* substrate
  and must say so.
- Australian English; branch per session; commit locally; **never push**.

## 8. Reading list

- `mtdnetwork/operation/mtd_operation.py` (`_interrupt_adversary`, 211-258;
  scheduling/suspension, 75-160) and
  `mtdnetwork/operation/attack_operation.py` (`apply_mtd_interrupt_cost` +
  `_handle_interrupt`, 161-249; `step()`'s interrupt-as-failure path).
- `mtdnetwork/trace.py` (the INTERRUPT event and penalty accounting) and
  `docs/implementation/trace_tool.md` (the movement-run tracer's three views).
- `docs/implementation/mtdsim_intent_spec.md` IS-INT-01..06, IS-ARC-01,
  IS-SCH-05/06; `docs/implementation/intent_conformance_audit.md` §f and the
  D-07 record.
- `docs/implementation/pipeline/ogasp/stochastic_timing_design.md` §4 (the
  penalty-stays-substrate-side ruling) and the S3-R seam records.
- [`2026-08-02_os_service_diversity_indistinguishability.md`](2026-08-02_os_service_diversity_indistinguishability.md)
  §1.2 — the precedent for "seam working as documented ≠ candidate divergence".

## 9. Out of scope (explicitly)

- Network-state couplings (briefs 1 and 2).
- Wiring `observed_changes` or any attacker observation of the defender
  (axis-8 exclusion stands for the life of the project).
- The Tay AI defender's reactive signal path (deferred with the AI seam to
  the ablation phase; it is this boundary's *fourth* party and gets its own
  review if it is ever promoted to current work).
- Re-tuning PENALTY or any constant without a provenance-backed disposition.
- Dissertation prose.
