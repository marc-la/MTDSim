---
status: durable
chapter: ch4_methods
created: 2026-06-18
updated: 2026-07-13
lineage: 2026-06-18_cti_to_executable_behaviour.md
---

# From intelligence structure to executable behaviour — the ontology gap, the binding layer, and "envelope, not actor"

## Position in the dissertation

The backbone of the methodology chapter's execution-model section: why a technique graph derived from threat intelligence cannot simply be "plugged into" a network simulator, what the missing layer between them is, and the honest framing the whole design commits to. This is where most graph-based attacker work in the literature stops — defining the formalism well and never executing it — so naming the gap precisely is itself half the methodological contribution.

## The idea

### Structure, policy, execution — one confusion dissolved

The objective-conditioned profiles, encoded as Petri nets, are *shape only*: a grammar of which moves are legal for a campaign with a given objective. A recurring question — "is the simulation run itself the behaviour?" — dissolves once three things are kept apart. **Structure** is the net: the grammar of legal moves. **Policy** is which enabled move fires, and when: the behaviour. **Execution** is one walk through the grammar under the policy, against the simulated world: the trace. An execution *realises* behaviour; the behaviour lives in the policy, about which the structural net says nothing. That is why "the nets only have shape" feels unfinished — it is; the net is necessary but not sufficient.

A less comfortable consequence follows from how the profiles were built. Each profile is the *union* of five to nineteen analyst-drawn incidents, so a token walking it freely can stitch one campaign's technique onto another campaign's next step and produce a chain **no real actor ever ran**. The strength (real, analyst-drawn technique dependencies) and the limitation (aggregation over-generates) are the same fact. The profile is therefore a **behavioural envelope for an operational objective — a space of plausible campaign behaviour — not any actor's policy**, and the design claims nothing more. "Envelope, not actor" is simultaneously the caveat and the defensible framing, and it is adopted up front rather than conceded under examination.

### The ontology gap — why the net cannot be plugged in as-is

The simulator and the profile are two graphs over different node types with **no shared join key**. The simulated network is a layered model — hosts connected by reachability; each host running services; each service carrying priced, synthetic vulnerabilities whose difficulty sets both exploit success and exploit time, with the inherited attacker operating entirely in that vocabulary (scan, enumerate, exploit-this-vulnerability-on-this-service, pivot). The profile's nodes are ATT&CK *techniques and tactics*; success, timing, and location have no representation in it at all. And an ATT&CK technique is **not** a vulnerability: "Exploit Public-Facing Application" is a *class of behaviour* that, in any concrete network, would be realised by exploiting some particular flaw. There is no host in a tactic, and no technique in a simulated exploit.

"Map the net onto the simulator" is therefore not a relabelling exercise but the definition of a **contract between two ontologies that were never built to meet** — and that contract is the missing layer. It is precisely where graph-based attacker work stalls: the theory is the net; the execution is the binding; the binding is system-specific and therefore absent from the literature.

### The binding, done properly

Three bindings are possible, from cheapest to most faithful. A **phase mapping** collapses each tactic onto one of the simulator's six native attack phases, so the net merely re-sequences native actions — quick, but it discards most of the intelligence-derived structure; useful only for cheap sanity probes. A **vulnerability-instance binding** maps technique → real CVE → concrete vulnerability; it is the most faithful and is infeasible here, because the simulator's vulnerabilities are synthetic and offer nothing to join real CVE identifiers onto (the public bridges between ATT&CK and CVE exist, but they presuppose NVD-sourced vulnerabilities).

The right target is the middle: a **capability precondition/effect contract**. Each technique declares a precondition (the capability or state it needs — a foothold, a credential, a reachable service) and an effect (the capability it grants). The attacker's state becomes a product: *position in the net* × *capability footprint in the simulated network*. A technique fires only when the net enables it *and* its precondition holds in the world — so the net says what is plausible next, the simulator says whether it is possible here, and the policy chooses among the legal-and-possible. The binding is deliberately non-rigid: the simulated world is allowed to refuse an intelligence-legal move. This is the classic logical-attack-graph precondition model, and it is the executable reading of the same conditions-and-actions structure the technique graph already preserves from the incident diagrams.

### The encoding ledger — where each modelled quantity comes from

The design's through-line is a strict division of labour. **Timing and success probabilities come from the simulator** (its priced vulnerabilities), because the intelligence corpus cannot supply them — an incident diagram records what an analyst drew, not how likely it was to work. **Structure and chaining come from the intelligence**, because that is its unique contribution: which technique enables which, per campaign objective. **Nothing load-bearing comes from the corpus's observation counts**, which measure how often analysts drew a step, not any rate. Exploit mechanics stay native to the simulator — techniques map to classes of existing actions, and no new exploit code is written. Detection is out of scope by prior decision: "caught" in this study means a defensive mutation invalidated progress, never that a sensor fired. The one genuine unknown is the **effect of a defensive mutation on an attacker's accumulated gains** — no public logs ground it in either direction — so it is modelled as a declared, per-tactic reset fraction and swept as a sensitivity band rather than hidden (the per-tactic profiles argue each direction from mechanism).

### What the profile buys over the inherited attacker

The inherited six-phase attacker is objective-agnostic, taxonomy-free, and fast — and it was the right call for the original line of work: simple, general, sufficient to compare defence mechanisms. Its known weakness is exactly why behavioural profiles were brought in: a defence that merely *outpaces* a fast generic attacker wins by default, so "mechanism A beats mechanism B" can be an artefact of attacker triviality. The profile adds three things the loop structurally cannot express: **objective conditioning** (campaigns with different goals traverse different technique sets), **intelligence-grounded chaining** (analyst-drawn dependency order rather than a generic scan-exploit-pivot cycle), and **low-and-slow stress** (a long-horizon campaign rather than a sprint incentivised by the time-to-compromise metric). The thesis's punchline lives in the third: a defence that wins by outpacing the smash-and-grab may lose against a slow, objective-driven, intelligence-grounded campaign — an advance in MTD *evaluation methodology* that requires touching neither the defences nor the network model.

That scoping is itself a result of the gap analysis: the inherited network model captures the *target* side well (reachability, services, vulnerabilities, precondition chains), and everything it lacks — campaign objective, attacker memory, capability state, mutation-awareness — is *attacker-side* and does not belong in the network model. The network is left untouched; the entire contribution sits in the attacker representation layered on top. Of the four properties packed into "advanced persistent threat" — objective-driven, capable, low-and-slow, adaptive — the first three are encoded by the profile, the binding contract, and the timing policy respectively; the fourth (an attacker who learns the mutation schedule and adapts) is the one genuinely hard encoding, and it is explicitly deferred, not quietly dropped.

### The risk that outranks the encoding

Two readings of the same net must not be conflated: an *analytical* reading (solve it as a Markov chain for closed-form metrics — a parallel, secondary track with its own feasibility record) and the *executable* reading described here, which is primary. For the executable track, the risk that matters more than any encoding choice is **discrimination**: do the four objective profiles produce distinguishable evaluation outcomes at all? If they do not, the work inherits the negative-result disposition declared at the partition stage. The cheap probe comes first; the full burden of proof — ranking stability across the swept parameters, and divergence from the baseline attacker's ranking — is specified in the evaluation chapter's companion note. Until those experiments run, this design is defended, not demonstrated, and the claim stays *fidelity changes the answer*, never "the model is true".

## Evidence and repo anchors

- The structural nets and their weighting: `data/ogasp/` (per-objective Petri nets; weights from flow proportions at tactic level); pipeline position and the layer naming (L3a grammar / L3b binding / L3c executed attacker): [`../../implementation/architecture.md`](../../implementation/architecture.md) §(f), §(j).
- The precondition/effect structure the binding executes: [`../../implementation/pipeline/gap/gap_schema.md`](../../implementation/pipeline/gap/gap_schema.md) Decision 2; the substrate's terrain and reset model: [`../../implementation/substrate_primer.md`](../../implementation/substrate_primer.md).
- Observation-counts-are-not-rates and metric-identity boundaries: [`../../implementation/metrics_semantics.md`](../../implementation/metrics_semantics.md) §(a), §(f).
- The analytical track's feasibility verdict: [`../../implementation/pipeline/ogasp/petri_feasibility.md`](../../implementation/pipeline/ogasp/petri_feasibility.md); the supervisor decision register that fixed the v1 execution model: [`../../implementation/pipeline/ogasp/supervisor_decision_register.md`](../../implementation/pipeline/ogasp/supervisor_decision_register.md).
- Inherited attacker code: `mtdnetwork/component/adversary.py`, `mtdnetwork/operation/attack_operation.py`; external precedents to reconcile before citing: Bland 2020 ([`bland2020`](../../sources/extractions/bland2020.md)), Rodríguez 2024 ([`rodriguez2024`](../../sources/extractions/rodriguez2024.md)), BRON / MulVAL (not yet extracted).
- Siblings: [`objective_partition_findings.md`](objective_partition_findings.md) (what the profiles are), [`operational_validation.md`](operational_validation.md) (how the timing layer is defended), [`../ch5_experimental_setup/evaluation_burden.md`](../ch5_experimental_setup/evaluation_burden.md) (the proof burden).

## Revisit conditions

- If the discrimination probe shows the profiles do not separate — the executable track inherits the negative-result disposition and the "what the profile buys" section is rewritten around it.
- If the simulator adopts real (NVD) CVEs — the vulnerability-instance binding becomes feasible and the capability-level contract is no longer the ceiling.
- If the envelope-not-actor framing is rejected in favour of per-incident single-actor nets — the aggregation tradeoff re-opens from the start.
- If the network model is ever changed — the "attacker-side only" scoping no longer holds and must be re-argued.
- If concurrent tactics are wanted (a multi-token net) — the single-token walk was a constraint this work placed on its own parameters, not a property of the formalism (Marc, 2026-08-18); a multi-token GSPN would make the AND-join structure the technique graph preserves usable again, at the state-space cost the feasibility study records. A future-work candidate for ch7, riding here per the ch7 README convention.
