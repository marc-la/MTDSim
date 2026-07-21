---
status: in-progress — map + ledger shipped; M6 application + Marc's review remain
created: 2026-07-15
updated: 2026-07-21
---

> **Executed 2026-07-21 — record + ledger shipped; M6 application gated.** The
> deliverable landed as the implementation record
> [`../implementation/pipeline/ogasp/tactic_action_map.md`](../implementation/pipeline/ogasp/tactic_action_map.md)
> plus the revised ledger
> [`../../data/ogasp/tactic_action_map.csv`](../../data/ogasp/tactic_action_map.csv)
> (long-form, 12 influenced pairs + 9 dwell-only rows; new hoisted path — the
> prior `timeline/` CSV is retained as the superseded binding investigation's
> ledger). Gate status: items 1, 2, 4, 6 ✅; **item 3 (M6) specified to a code
> seam but not applied** — it regenerates review-gated net artefacts and extends
> the load-bearing no-synthesis invariant test, so per item 5 it awaits Marc's
> review of the map first (record §6, §8). One open judgement for Marc: whether
> off-clock resource-development is bridged into the net or left a documented
> island. Callability update folded in: the §3.3 carve **landed** (2026-07-21),
> so the handoff's "conditional on carve" row-class is discharged — only
> "callable-with-context" remains (record §1). **Delete this handoff when M6 is
> applied and the map is signed off.**

# Produce the M5 tactic→action influence map — inventory the substrate's attacker actions and their binary outcome signals, map the 15 tactics onto them with per-pair justification, and curate the M6 pre-intrusion synthetic join

> **Re-sequenced (2026-07-16): now second in the chain, behind the
> action-layer anatomy — complete, now the record**
> ([`../implementation/pipeline/ogasp/action_layer_anatomy.md`](../implementation/pipeline/ogasp/action_layer_anatomy.md)),
> which absorbed this handoff's step 1: the map's per-pair verdicts are only
> meaningful once each verb's callability class (callable-as-is /
> callable-with-context / chain-bound) and the reordering-freedom result are
> known. Map rows must carry the anatomy record's callability constraint —
> a tactic mapped onto a chain-bound verb is a *conditional* mapping until
> the specified carve/context-synthesis exists. The 14-Jul meeting
> ([`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
> §M1–M8) settled the execution model: the net runs live in the simulation
> (M1), the substrate's existing attack machinery is the binary outcome
> oracle (M2/M4), and the join is a **manual, justified tactic→action
> influence map** (M5). This handoff produces that map plus the two things
> the downstream design and build consume: the **outcome-signal inventory**
> (what "success" and "failure" concretely are, per action) and the **M6
> pre-intrusion curation** (recon/resource-development joined synthetically
> at the front of the net).

## State of play

- **The action vocabulary exists and is small.** The inherited attacker
  drives six executable verbs — SCAN_HOST / ENUM_HOST / SCAN_PORT /
  EXPLOIT_VULN / BRUTE_FORCE / SCAN_NEIGHBOR — in
  [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py),
  against hosts/services with CVSS-priced synthetic vulnerabilities
  ([`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)).
  Jin's ruling: these existing behaviours are the starting vocabulary; the
  movement layer calls them as an API and reads the result out ("this is
  your API — you get the result out, and it feeds the movement of the
  attacker"). Enrichment (an evade or persistence action) comes *after* the
  loop closes, only if the numbers demand it.
- **The substrate already rolls its own dice.** Exploit success is priced
  off vulnerability complexity/CVSS, brute force has its own chance, and
  the per-host attempt limit is a give-up rule. The M2 binary outcome is
  *read from* these mechanisms, not layered on top of them — the
  double-counting trap the retired operationalisation handoff flagged is
  avoided by construction, but only if the inventory states precisely which
  event constitutes the binary verdict for each action.
- **A prior ledger exists as raw material, not authority:**
  [`../../data/ogasp/timeline/tactic_action_map.csv`](../../data/ogasp/timeline/tactic_action_map.csv)
  (from the superseded binding investigation, whose C1→C2 recommendation
  was decided over —
  [`../implementation/pipeline/ogasp/binding_design_space.md`](../implementation/pipeline/ogasp/binding_design_space.md)
  banner). Fold it in; re-derive the verdicts under M5's framing
  ("which tactics does each action influence"), don't inherit them.
- **The 15 per-tactic profiles**
  ([`../notes/ch3_design/tactic_profiles/`](../notes/ch3_design/tactic_profiles/))
  are the single source of truth for what each tactic *attempts* — the
  justification column of the map cites them.
- **The pre-intrusion gap is now a curation task (M6).** The corpus is
  blind to recon/resource-development, so those places are islands in two
  class nets. The ruling: connect them **manually** at the front (recon
  enables initial access — "if you cannot recon anything, you can't gain
  initial access"), defensible because nothing detects pre-intrusion
  activity. This supersedes the start-at-initial-access workaround and the
  attacker-knowledge-parameter idea from the 10-Jul update.

## Recommended approach

**Deliverable = one implementation record**
(`docs/implementation/pipeline/ogasp/tactic_action_map.md`) **+ the revised
ledger** (`data/ogasp/tactic_action_map.csv` or successor — let the record
decide the columns) **+ the M6 edge curation** (a documented edit to the net
build inputs, not hand-edited artefacts).

1. **Consume the anatomy record** (`action_layer_anatomy.md`) — the action
   inventory, callability classes, precondition/coupling graph, and
   affordance register now live there; do not re-derive them. Where this
   handoff's mapping needs something the anatomy didn't capture, extend the
   anatomy record, not this one.
2. **Map the 15 tactics onto the actions, binary in/out per pair (M5).**
   For each tactic × action: influenced or not, with a one-sentence
   justification citing the tactic's profile §5 block, **and the anatomy
   record's callability constraint on the row** (unconditional / conditional
   on carve / conditional on context synthesis). Expect many-to-many
   (exploitation touches several tactics). Tactics with no plausible action
   (the old cost-only set) get an explicit "no action — dwell only" row;
   R5 already sanctions this. Where the affordance register exposes a
   legitimate tunable, the row may also carry a *parameterisation* (e.g.
   scan invoked with a different duration at recon-shaped tactics) — actions
   and parameters are both controller vocabulary.
3. **Define the binary verdict per tactic.** For each tactic with mapped
   actions: which substrate event constitutes success (e.g. exploit lands /
   host compromised / scan completes with new reachable set) and which
   constitutes failure (attempt limit hit, no vulnerable service, interrupt).
   This is the oracle contract the feedback-net design consumes.
4. **Curate the M6 join.** Propose the synthetic recon/resource-development
   edges (which places, which transitions, what weight treatment given no
   flow evidence — a declared uniform/manual weight, flagged as synthetic in
   provenance), applied through the net build code so the artefacts
   regenerate.

*Alternatives considered:* extending the action set first (new evade/
persistence verbs) — rejected: M5/M7 say existing vocabulary first,
enrich only after the loop closes. Automating the map from technique
metadata — rejected: Jin explicitly sanctioned a manual, justified mapping;
the corpus-to-substrate vocabulary gap makes automation false precision.

## Validation gate

Done when:
1. The record inventories every attacker action with its state effect,
   pricing, native chance mechanism, and readable outcome event.
2. All 15 tactics have a complete row set: mapped actions (or explicit
   dwell-only), per-pair justification citing the profile §5 block, and a
   defined binary success/failure verdict.
3. The M6 synthetic edges are specified (places, transitions, weight
   treatment, provenance flag) and regenerate through the build code —
   no hand-edited artefacts.
4. No double-counting: the record states, per tactic, that the verdict is
   read from existing substrate dice, and where a new probability would
   act if R2 tuning arrives later (hook named, not designed).
5. Marc has reviewed the map before the feedback-net design consumes it.
6. **No simulator behaviour changes** — analysis, record, ledger, and net
   build-input edits only.

## Hard constraints

- **Existing action vocabulary only (M5/M7)** — no new verbs, no edits to
  `attack_operation.py` behaviour.
- **Profiles are the behaviour authority** — the map cites
  `tactic_profiles/` §5 blocks; it never forks them.
- **Synthetic edges are labelled synthetic** — M6 curation carries a
  provenance flag distinguishing it from flow-derived structure
  ([`../implementation/provenance.md`](../implementation/provenance.md)).
- **R2 (success-rate tuning) is a hook, not a design** — post-first-numbers.
- Determinism (SIM-05) for anything that regenerates artefacts; branch
  hygiene; **never push without an explicit ask**; Australian English.

## Reading list

- [`../implementation/pipeline/ogasp/action_layer_anatomy.md`](../implementation/pipeline/ogasp/action_layer_anatomy.md)
  — the callability classes, coupling graph, affordance register, and ATT&CK
  coverage map this map consumes; read first.
- [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
  — §M1–M8 (the rules this executes) + D3/D4/R5 for the standing regimes.
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  + [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  — the API surface being inventoried.
- [`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
  — where the native dice live (complexity/CVSS pricing).
- [`../../data/ogasp/timeline/tactic_action_map.csv`](../../data/ogasp/timeline/tactic_action_map.csv)
  — the prior ledger to fold in without presuming it right.
- Two or three [`../notes/ch3_design/tactic_profiles/`](../notes/ch3_design/tactic_profiles/)
  files — the §5 evidence convention the justifications cite.

## Out of scope (explicitly)

- The conditional-weight/direction design (the feedback-net design handoff).
- Any attacker build (the profiled-attacker build handoff).
- New actions, evasion/persistence enrichment, R2 tuning, R3 styles.
- CVE/CWE/CVSS grounding of the vulnerability pool — dead per M4.
