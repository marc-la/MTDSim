# Adversary-emulation frameworks — extraction notes (survey-level)

> MITRE Caldera (adversary-emulation platform), Atomic Red Team, MITRE CTID
> adversary-emulation plans. Survey-level stub built from vendor/project
> documentation via web search (July 2026), **not** a deep read — the
> full Caldera dissection is reserved for the tactic-operationalisation
> handoff (`docs/handoffs/2026-07-13_l3_tactic_operationalisation.md`,
> gate 3), which owns the ability/fact model at implementation depth. This
> stub records only the one abstraction the *binding investigation*
> ([`../../implementation/pipeline/ogasp/controller.md`](../../implementation/pipeline/ogasp/controller.md))
> cites: the pre/post-condition ("fact") contract as external precedent
> for the capability-precondition/effect binding (candidate C2).

## Bibliographic anchor

- **Citation keys**: `caldera` (MITRE Caldera), `atomicredteam`, `ctid_emulation_plans`
- **Sources (web, survey-level; not fetched to markdown)**:
  - Caldera project + docs — <https://caldera.mitre.org/>, <https://github.com/mitre/caldera>
  - Starlog, "CALDERA: Building Autonomous Adversary Emulation" — <https://starlog.is/articles/cybersecurity/mitre-caldera>
  - AttackIQ Academy course notes on Caldera abilities/adversaries (survey)
- **Acquisition status**: OA project documentation. No paywalled item. Deep
  extraction deferred to the operationalisation handoff (do not duplicate here).

## Extraction policy

Survey-level, paraphrase-only. No fair-use quotation reproduced; each claim is
attributed to the project docs and marked **survey-level (verify at
implementation depth)** because it derives from secondary summaries, not a
first-hand read of the Caldera source.

## Relevant artefacts

### The ability / fact pre-post-condition model (load-bearing for C2)

- **Claim (survey-level):** A Caldera *ability* is an ATT&CK-technique
  implementation that declares the **facts it requires** (preconditions) and
  the **facts it produces** (postconditions); an *adversary profile* is an
  ordered/над selectable set of abilities; an *operation* runs a profile against
  agents, chaining abilities as their required facts become available (e.g. a
  credential-dumping ability requires `elevated.privileges` and produces
  `discovered.credential`).
- **Transfer verdict: PARTIALLY TRANSFERS (abstraction only, not machinery).**
  The *pre-condition → behaviour → post-condition triple* is the same shape as
  candidate C2's capability contract and as the ch3 precondition/effect binding
  ([`../../notes/ch3_design/structure_to_behaviour_binding.md`](../../notes/ch3_design/structure_to_behaviour_binding.md) §"the binding, done properly").
  What **does not** transfer: Caldera executes *real commands on real agents*;
  it is an emulation platform, not a discrete-event model. In MTDSim the
  "facts" are the substrate's already-tracked capability footprint
  (`compromised_hosts`, `compromised_users`, host-stack map-knowledge), and the
  "abilities" are the six priced verbs — so the contract is a *state-gating
  layer over existing verbs*, never a command executor.
  → C2 in [`controller.md`](../../implementation/pipeline/ogasp/controller.md).
- **Novelty note:** the fact-model precedent is what lets C2 be argued as
  *established practice* rather than invention — Caldera is the existence proof
  that "ATT&CK behaviour = pre/post-condition-gated ability" is a workable
  operational contract.

### Adversary profiles as objective-conditioned ability sets

- **Claim (survey-level):** Caldera adversary profiles bundle abilities to
  emulate a named actor or an *archetype* (initial-access specialist,
  lateral-movement specialist, exfiltration specialist).
- **Transfer verdict: PARTIALLY TRANSFERS.** The archetype-as-ability-set idea
  mirrors the L2 operational-objective classes (each class routes a different
  tactic set). It corroborates that objective-conditioned action *sets* (not
  just parameters) are a real modelling axis — the open question the
  operationalisation handoff owns ("do profiles carry differing action sets?").
  Does not transfer: Caldera profiles are hand-authored per actor; MTDSim's are
  CTI-derived envelopes.
