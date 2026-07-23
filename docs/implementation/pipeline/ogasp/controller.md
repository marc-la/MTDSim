---
status: durable
created: 2026-07-22
updated: 2026-07-22
topic: "L3 controller — the tactic -> MTDSim-phase dispatch map for experiment 1: a CKC-mediated position map, held as a swappable input parameter (not a recovered ground truth); supersedes the M5 tactic->action influence map + the binding investigation"
lineage: rewritten from tactic_action_map.md (the M5 'true tactic->action map'); reframed as an input parameter per Marc's 2026-07-22 direction
---

# The controller — tactic -> MTDSim-phase dispatch (experiment 1)

**Status:** durable. The **controller** is the seam between the class net (which
ATT&CK tactic the attacker token sits on) and the inherited substrate action set
(which of the six MTDSim attack verbs fires). For the first experiment it is a
deliberately **simple, CKC-mediated position map**, and — the load-bearing
framing — it is an **input parameter of the research, not a recovered ground
truth**. There is no single "true" tactic-to-action mapping to discover; the
mapping is a *choice*, and different choices are things the evaluation can vary.

This record supersedes the earlier **M5 tactic->action influence map** and the
**binding investigation** (`binding_design_space.md`, `binding_signoff_summary.md`,
both removed 2026-07-22). Those tried to *justify one correct* many-to-many
mapping per pair, against the tactic profiles' §5 evidence — an over-commitment
that conflicts with the input-parameter framing. The per-verb outcome semantics
they established survive in the code-faithful
[`attacker_phase_catalogue.md`](attacker_phase_catalogue.md) and
[`action_layer_anatomy.md`](action_layer_anatomy.md); only the "one true mapping"
claim is retired.

The mapping drawn here **is** [`../../../../data/ogasp/controller.csv`](../../../../data/ogasp/controller.csv);
the loader/resolver is
[`../../../../src/mtdsim/l3_simulation/controller/`](../../../../src/mtdsim/l3_simulation/controller);
the at-a-glance figure is
[`../../../../data/misc/_viz/controller_mapping.png`](../../../../data/misc/_viz/controller_mapping.png).

---

## 1. The construction — tactic -> CKC -> verb

The controller is a **transitive map through the Cyber Kill Chain**. Two source
mappings compose:

1. **MTDSim verb -> CKC phase**, by **Brown's Fig-3 flow position** (B-ATK-03:
   the attack procedure is "CKC + ATT&CK-inspired"). The six verbs are laid onto
   the first six CKC phases in the order Brown's flowchart runs — host discovery,
   then host preparation/selection, then the port-scan access step, then exploit,
   then the credential-foothold fallback, then the neighbour-reveal Brown itself
   calls "C2 reveals connected hosts". This is a **reconstruction of Brown's
   intent**, not something Brown states verb-by-verb — the code carries no CKC or
   ATT&CK labels at all ([`action_layer_anatomy.md`](action_layer_anatomy.md) §5),
   which is exactly why it is held as a chosen parameter.

   | MTDSim verb | CKC phase |
   |---|---|
   | `SCAN_HOST` | Reconnaissance |
   | `ENUM_HOST` | Weaponization |
   | `SCAN_PORT` | Delivery |
   | `EXPLOIT_VULN` | Exploitation |
   | `BRUTE_FORCE` | Installation |
   | `SCAN_NEIGHBOR` | Command & Control |

2. **ATT&CK tactic -> CKC phase**, by the standard academic ATT&CK->CKC crosswalk
   (the pre-v19.1 Enterprise convention already drawn in
   [`../../../../data/misc/_viz/ckc_layer_viz.py`](../../../../data/misc/_viz/ckc_layer_viz.py),
   here un-collapsed to the full seven Lockheed phases).

**Composition:** a tactic dispatches the verb that shares its CKC phase. Where a
tactic's CKC phase has **no** verb, it dispatches the verb of the **nearest
covered CKC phase** (a "doubled" edge). Only **Actions on Objectives** has no
native verb, so its whole band doubles onto `SCAN_NEIGHBOR` (nearest covered =
Command & Control).

Because the six verbs spread *one per CKC phase* along the kill chain (rather than
bunching by technique, which "best-fit by dominant technique" does — leaving
Weaponization / Installation / C2 empty *and* Actions-on-Objectives ambiguous),
the result is **complete coverage**: every one of the 15 tactics resolves to
**exactly one** verb. This is the property a best-fit mapping fails.

---

## 2. The map (the 15 rows)

`coverage = direct` — the tactic's own CKC phase owns the verb; `= fallback` —
Actions on Objectives, doubled onto the nearest covered phase's verb.

| Tactic | ATT&CK id | CKC phase | -> MTDSim verb | coverage |
|---|---|---|---|---|
| reconnaissance | TA0043 | Reconnaissance | `SCAN_HOST` | direct |
| resource-development | TA0042 | Weaponization | `ENUM_HOST` | direct |
| initial-access | TA0001 | Delivery | `SCAN_PORT` | direct |
| execution | TA0002 | Exploitation | `EXPLOIT_VULN` | direct |
| privilege-escalation | TA0004 | Exploitation | `EXPLOIT_VULN` | direct |
| stealth (defense-evasion) | TA0005 | Exploitation | `EXPLOIT_VULN` | direct |
| defense-impairment | TA0112 | Exploitation | `EXPLOIT_VULN` | direct |
| persistence | TA0003 | Installation | `BRUTE_FORCE` | direct |
| command-and-control | TA0011 | Command & Control | `SCAN_NEIGHBOR` | direct |
| credential-access | TA0006 | Actions on Objectives | `SCAN_NEIGHBOR` | fallback |
| discovery | TA0007 | Actions on Objectives | `SCAN_NEIGHBOR` | fallback |
| lateral-movement | TA0008 | Actions on Objectives | `SCAN_NEIGHBOR` | fallback |
| collection | TA0009 | Actions on Objectives | `SCAN_NEIGHBOR` | fallback |
| exfiltration | TA0010 | Actions on Objectives | `SCAN_NEIGHBOR` | fallback |
| impact | TA0040 | Actions on Objectives | `SCAN_NEIGHBOR` | fallback |

The map is 1:M — many tactics collapse onto one verb (`EXPLOIT_VULN` carries four
tactics, `SCAN_NEIGHBOR` seven). The tactic keys are exactly the aggregate net's
15 tactic-places, so the map feeds the net without gaps or orphans (asserted in
[`../../../../tests/l3_simulation/test_controller.py`](../../../../tests/l3_simulation/test_controller.py)).

**This is coarse on purpose.** The aim for experiment 1 is an end-to-end run, not
a faithful per-tactic behaviour model. Consequences are visible and intended:
`initial-access` fires only the port-scan verb (not the exploit); `lateral-movement`
and `discovery` fire only the neighbour-reveal; the terminal objective tactics
(exfiltration, impact) fire the same neighbour-reveal as a placeholder action.
A finer mapping is a *different value of the same input parameter*, swapped by
editing `controller.csv` — no code change.

---

## 3. Experiment-1 setup — how the controller is used end to end

The controller is one component of the (not-yet-built) movement-layer / profiled
attacker (M7 handoff). The loop, per run:

1. The class net's single token sits on a tactic-place.
2. The controller resolves that tactic to its one MTDSim verb (this map).
3. The movement layer calls that verb through the carved substrate action surface
   (`step(verb)`; [`action_layer_anatomy.md`](action_layer_anatomy.md) §3), which
   runs the verb with its native time cost and returns its branch outcome — the
   substrate stays the **outcome oracle** (M4).
4. The **binary verdict** is read from that verb's outcome (§4 below), and the
   outcome overlay routes the token's next transition (success -> forward,
   failure -> retry/backward), per
   [`success_failure_overlay_design.md`](success_failure_overlay_design.md).

The controller owns only step 2 — *which verb*. Timing, outcome, and net routing
are owned elsewhere; keeping the controller a pure lookup is what makes it a
swappable parameter.

---

## 4. The outcome verdict (per dispatched verb)

Because the controller dispatches a *verb*, the success/failure verdict the
outcome overlay keys on is the **dispatched verb's** readable outcome, not a
per-tactic definition. The six verbs' outcomes are catalogued code-faithfully in
[`attacker_phase_catalogue.md`](attacker_phase_catalogue.md) and
[`action_layer_anatomy.md`](action_layer_anatomy.md) §2; in brief:

| Dispatched verb | Success (forward) | Failure (retry/back) | MTD interrupt |
|---|---|---|---|
| `SCAN_HOST` | non-empty reachable host set | empty (`host_stack` empty) | `network`-layer -> restart at `SCAN_HOST` |
| `ENUM_HOST` | fresh host enumerated | (dispatcher; re-routes) | — |
| `SCAN_PORT` | ports enumerated / reuse hit | interrupt / empty | `application`-layer resets working set |
| `EXPLOIT_VULN` | `EXPLOIT_COMPROMISED` | `EXPLOIT_UNCOMPROMISED` | `EXPLOIT_HALTED` |
| `BRUTE_FORCE` | host compromised (`True`) | not compromised (`False`) | uninterrupted |
| `SCAN_NEIGHBOR` | new neighbours discovered | no new neighbours | `network`-layer -> restart |

**No double-counting (M4):** the verdict is *read* from the substrate's own dice,
never re-rolled. The net supplies movement; the substrate supplies outcome.

---

## 5. Relationship to the rest of L3, and when to update

- **Consumes:** [`action_layer_anatomy.md`](action_layer_anatomy.md) and
  [`attacker_phase_catalogue.md`](attacker_phase_catalogue.md) (the six verbs,
  their outcomes, the carved callable surface); the ATT&CK->CKC crosswalk in
  [`../../../../data/misc/_viz/ckc_layer_viz.py`](../../../../data/misc/_viz/ckc_layer_viz.py).
- **Feeds:** the profiled-attacker / movement-layer build (M7 handoff) and the
  outcome overlay ([`success_failure_overlay_design.md`](success_failure_overlay_design.md)),
  which consumes §4's per-verb verdict; the synthetic overlay
  ([`synthetic_overlay.md`](synthetic_overlay.md)) is the *structural* pre-intrusion
  join and is orthogonal to this dispatch map.
- **Decision provenance:** M5/M6/M2/M3 in the supervisor decision register
  ([`supervisor_decision_register.md`](supervisor_decision_register.md)); the
  input-parameter reframe and the CKC-position construction are Marc's
  2026-07-22 direction (M5's "manual justified map" is relaxed to "one value of a
  swappable parameter").
- **When to update:** if the mapping value changes (edit `controller.csv`; this
  table follows); if a verb's tail-call/outcome changes in
  `attack_operation.py` (§4 re-walked — it is a code snapshot); if the movement
  layer promotes the controller from a static map to a per-run policy.
