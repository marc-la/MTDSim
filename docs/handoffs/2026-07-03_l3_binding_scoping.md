---
status: open
created: 2026-07-03
---

# Scope the tactic→substrate binding (no build): the tactic→action map, cost-only dispositions, the state-over-impact success model, and the CVE→synthetic-CVSS reconciliation design

> **Scoping only** — the minutes are explicit ("Scope how each state/tactic
> maps to simulator actions and how attack behaviour overrides the current
> impact-based success logic (3 layers) — *scoping only this week*"). The
> deliverables are a design note + a draft mapping table; the build is
> [`./2026-07-03_l3_replay_attacker.md`](./2026-07-03_l3_replay_attacker.md).
>
> **Depends on** the D5/D6/D7 scope decisions, now registered durably in
> [`../notes/2026-07-03_supervisor_meeting_l3_decisions.md`](../notes/2026-07-03_supervisor_meeting_l3_decisions.md)
> (the governance handoff that held them was deleted when its work shipped). Can start immediately after it — in parallel
> with the weighting/durations/runner chain — but **finalises against the
> runner's committed timeline schema** (soft dependency: the binding consumes
> that schema — now shipped:
> [`../../data/ogasp/timeline/timeline_schema.md`](../../data/ogasp/timeline/timeline_schema.md),
> `ogasp-timeline/v1`). Its draft tactic→verb table is also what the durations
> handoff's Tier-1 sourcing consults — produce the draft table early.
>
> **Supersedes** the deleted `2026-06-18_l3b_execution_semantics.md`: its five
> open supervisor questions are answered by the meeting (single token; v1
> one-way coupling; attacker-only scope; both entries; adaptive policy
> deferred), and its capability precondition/effect contract moves to the
> two-way-integration upgrade path rather than the v1 contract.

## State of play

- **The ontology gap is the reason this layer exists** (the note
  [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
  §2, still fully current): the profile speaks ATT&CK tactic/technique; the
  substrate speaks host/service/vulnerability (synthetic CVSS). No shared join
  key. The binding is the contract between the two — and it is the part the
  literature always leaves unbuilt.
- **What changed at the meeting:** v1 is a **one-way replay** (D2), so the v1
  binding is simpler than the old capability-contract design — it must answer
  "when the timeline says the attacker is in tactic X for [t₁,t₂), what does
  the simulator *do*, and what does that make the outcome mean?" The
  precondition/effect capability contract is now the *upgrade path* for the
  deferred two-way integration, not the MVP.
- **The substrate's executable verbs** (the only things that can actually
  happen): SCAN_HOST / ENUM_HOST / SCAN_PORT / EXPLOIT_VULN / BRUTE_FORCE /
  SCAN_NEIGHBOR — [`attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  (`_execute_attack_action` dispatch, L48; the six `_scan_host`…`_scan_neighbors`
  methods), priced by `ATTACK_DURATION`
  ([`constants.py`](../../mtdnetwork/data/constants.py) ~L140).
- **Five tactics have no network-state to act on** (Execution,
  Defence-Evasion, Persistence, Command-and-Control, Exfiltration) — some
  exist precisely to introduce stealth and only become meaningful with a
  detection state. **IDS is culled project-wide**
  ([`../specs/project_context.md`](../specs/project_context.md)), so the MVP
  disposition is **cost-only** (the state consumes time and produces a record,
  acts on nothing) — this executes D6 ("manually define reasonable
  connections/values as a starting point; detection/evasion later"). Record
  that cost-only-vs-proto-IDS was the open question and why cost-only is the
  only spec-compliant answer.
- **The CVE gap:** the nets' techniques imply real-world exploitation; the
  substrate's vulnerabilities are synthetic (no CVE keys). Marc's proposed
  reconciliation: **tactic → technique → CAPEC → CWE → CVE → synthetic-CVSS**,
  the last hop being a **tag/label over the synthetic pool** with the
  aggregate CVSS distribution held fixed so MTTC stays comparable. Approach
  awaits explicit supervisor confirmation — design it; flag it.

## Recommended approach

**Deliverable = one scoping note** (`docs/notes/2026-07-XX_l3_binding_scoping.md`)
**+ one draft mapping CSV** (`data/ogasp/timeline/tactic_action_map.csv`), covering four
sections:

**1 — Tactic → action-class map (the "~15 actions" question, answered
conservatively).** Map each of the ≤15 tactic-places onto the existing six
substrate verbs (one-to-many allowed) or `COST_ONLY`. Recommended stance: the
"new ~15 actions" are **tactic-level wrappers over existing verbs, not new
exploit code** — exploits stay native, techniques map to action *classes*
(the note §5 ledger). Sketch: discovery → SCAN_HOST/ENUM_HOST/SCAN_PORT;
initial-access / privilege-escalation → EXPLOIT_VULN; credential-access →
BRUTE_FORCE; lateral-movement → SCAN_NEIGHBOR + EXPLOIT_VULN; reconnaissance /
resource-development → COST_ONLY (pre-intrusion); execution, defence-evasion,
persistence, C2, exfiltration → COST_ONLY (D6); collection / impact → decide
and justify (candidates: COST_ONLY vs a compromise-consolidation read).
Every row: tactic, verb(s), rationale, cost-only?, and the two-way upgrade
note (what capability precondition/effect it would carry later). Concurrency:
single token (v1) → strictly sequential actions; the concurrent ~15-action
set is explicitly the multi-token/two-way question, deferred.

**2 — The three-layer success model (D7 scoping).** Layer 1: timeline state
(which tactic, when). Layer 2: simulator action(s) the state triggers.
Layer 3: outcome — where the current impact-score success logic gets
overridden by state ("keep the same routes, but let the attack behaviour/state
decide the outcome"). Scope the options concretely: (a) **gating** — substrate
events only count when the state licenses them (no exploit outside an
exploit-shaped state; an attacker in a stealth state does not launch the
expected exploit); (b) **objective-read success** — "attack succeeded" derived
from the class objective (exfiltration/impact visited *and* substrate-realised)
rather than raw impact score; (c) hybrid. Recommend one, with the comparability
consequence for MTTC spelled out (the compromise-time event definition in
[`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(a) must
keep meaning the same thing for the procedural baseline).

**3 — CVE → synthetic-CVSS reconciliation design.** Specify the mapping
pipeline: technique → CAPEC → CWE via the published MITRE crosswalks (BRON /
CTID ATT&CK↔CVE mappings — *not yet extracted*; reconcile before citing,
papers-are-claims), terminating in a **CWE-derived tag assigned to synthetic
vulnerabilities** (synthetic vulns carry no CVE key; the tag is a label over
the existing pool, assignment rule to be designed — e.g. partition the pool by
tag with per-tag CVSS strata matched to the pool's existing distribution).
**Invariant: the aggregate CVSS distribution of the pool is unchanged**, so
baseline MTTC is untouched and within-substrate comparability holds. Scope
what the tag buys v1 (an exploit-shaped state prefers tag-matching vulns) vs
what it defers (real-CVE substrate). **Flag: supervisor confirmation of the
whole binding approach is still pending** — present this as the design to
confirm.

**4 — MTD-interruption semantics (scoped, not built).** The replay attacker
will face MTD interrupts mid-state; name the candidate policies
(retry-within-window / state-fails-and-timeline-advances / dwell-extension)
and recommend one for the replay handoff to implement. Keep the old
capability-reset-fraction idea in the two-way upgrade path section.

*Alternatives considered:* full capability precondition/effect contract now
(rejected for v1 — D2 made the coupling one-way; it returns with two-way);
phase-map binding of tactics onto the six *phases* (rejected — lossier than
verb-mapping and no longer needed since the discrimination probe was retired);
holding out for a real-CVE substrate (rejected — out of scope and the
synthetic-tag design keeps MTTC comparable).

## Validation gate

Done when:
1. The scoping note exists with all four sections, each ending in a concrete
   recommendation the replay handoff can implement without re-deriving.
2. `data/ogasp/timeline/tactic_action_map.csv` covers every tactic-place in the L3a
   union; every row has a rationale; every `COST_ONLY` row records why (no
   network-state / pre-intrusion / stealth-pending-detection).
3. The three-layer success model names its recommended option and states the
   MTTC-comparability consequence explicitly.
4. The CVE-reconciliation section states the fixed-CVSS-distribution invariant
   and is marked **pending supervisor confirmation**.
5. Marc has reviewed the note (it feeds a canonical-spec block later —
   architecture §(f) — which stays Marc-driven).
6. **No code changes** anywhere.

## Hard constraints

- **Scoping only** — no simulator code, no substrate edits, no new actions
  implemented.
- **Attacker-only scope (D5)**; HARM / network / MTD mechanisms untouched by
  the eventual build; the design must not require touching them.
- **No IDS / detection features** — cost-only is the stealth disposition;
  detection-conditioned meaning is deferred with D6/D10.
- **ATT&CK ≠ CVE** — never join techniques directly onto synthetic vulns; the
  tag pipeline is the only sanctioned bridge, and the pool's aggregate CVSS
  distribution is invariant.
- **Papers are claims**: BRON / CTID / MulVAL are unextracted — reconcile
  before citing ([`../specs/guardrails.md`](../specs/guardrails.md)).
- Envelope-not-actor phrasing throughout; Australian English; branch hygiene;
  **never push without an explicit ask**.

## Reading list

- [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
  — §2 (ontology gap), §4 (binding levels), §5 (encoding ledger), §8 (APT
  properties → knobs). The conceptual base; this handoff re-cuts it for the
  one-way v1.
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  + [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  — the verbs and the phase loop being wrapped.
- [`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
  — the synthetic vuln model (complexity/cvss/exploit_time/dependent_vuln_id)
  the tag design overlays.
- [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(a) — the
  MTTC event definition the success model must not silently change.
- [`../../data/ogasp/timeline/timeline_schema.md`](../../data/ogasp/timeline/timeline_schema.md)
  (+ committed example) — the timeline schema this binding consumes
  (finalise against it; shipped 2026-07-09).

## Out of scope (explicitly)

- Building the replay attacker (next handoff) or any code.
- The capability precondition/effect contract and MTD-capability-reset
  modelling — documented only as the two-way upgrade path.
- Acquiring/ingesting BRON or NVD data — design the pipeline; ingestion is a
  follow-up once the supervisor confirms.
- Detection/IDS, adaptive policies, multi-token concurrency.
