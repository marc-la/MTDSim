---
status: durable
created: 2026-07-05
updated: 2026-07-13
---

# Substrate primer — MTDSim as an adversarial environment

**Status:** durable. The conceptual, **non-implementation-specific** view of the
inherited MTDSim substrate, written from the attacker's side: what the network
*is* as terrain, what the MTD mechanisms *do* to that terrain, what the attacker
*knows and holds*, and — the load-bearing part — what a defensive mutation
*does to the attacker's gains*. It exists so the per-tactic profiles
([`../tactic_profiles/`](../notes/ch4_methods/tactic_profiles/)) and the thesis chapters can
reference one durable account of the substrate instead of re-deriving it, and so
that a refactor, a renamed class, or an inherited bug does **not** propagate into
the argument. Where a claim is a *design principle* (durable) it is stated as
such; where it is a *current-implementation embodiment* (mutable) it is flagged.

Row-level conformance detail (exact constants, NET/ATK dispositions) is **not**
restated here — that is [`mtdsim_spec.md`](mtdsim_spec.md). The pipeline this
substrate sits under is [`architecture.md`](architecture.md); the ontology gap
between this substrate and the CTI profiles is
[`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/ch4_methods/structure_to_behaviour_binding.md).

---

## (a) What the substrate is, and how to read this primer

MTDSim (a fork of MTDSimTime; lineage Brown 2023 → Zhang 2023 → Ho 2024 →
Tay 2024) is a **discrete-event simulator** for evaluating Moving Target Defence.
A defender fires MTD *mutations* on a schedule; an attacker traverses the network
trying to reach a target before the mutations wear its progress down; the run
yields time-to-compromise and related metrics. The research question the substrate
serves is comparative — *how do existing MTD mechanisms perform against
behaviourally-grounded adversarial profiles* — so the substrate is deliberately
**generic** (not thesis-tuned) and **frozen on the defender side**; the whole
contribution lives in the attacker layer ([`architecture.md`](architecture.md) §(a)).

**The three durable objects.** Everything below reduces to: a **network** (the
terrain), a set of **MTD mutations** (terrain change), and an **attacker** (a
knowledge-accumulating agent moving over the terrain). The thesis's novel object
is the *interaction* of the third with the second — how a mutation disturbs what
the attacker has learned or gained. That interaction is §(e), the heart of this
primer.

## (b) The network as terrain — the three-layer HARM

The network is a **Hierarchical Attack Representation Model (HARM)** — a graph of
graphs, in three layers (Hong & Kim's HARM lineage; the substrate's own model):

- **Network layer** — hosts as nodes, reachability as edges. A small set of hosts
  are **exposed endpoints** (the ingress); the rest are internal. There is a
  designated **target**. This layer answers *"what can reach what"*.
- **Host / application layer** — each host is itself a small **internal service
  graph** (a Watts–Strogatz graph) with an internal target node. Compromising a
  host means exploiting services until enough impact accumulates adjacent to that
  internal target. This layer answers *"what runs on this host, and how do I own
  it"*.
- **Service → vulnerability** — each service carries **vulnerabilities**, and each
  vulnerability is priced: a **complexity/CVSS** value sets *both* how likely an
  exploit is to succeed *and* how long it takes; some vulnerabilities are gated by
  a **precondition** (another vulnerability, or an OS match) that must be satisfied
  first. This is the classic logical-attack-graph precondition/effect model
  (MulVAL-style) realised at service granularity.

Three properties of this terrain are load-bearing for everything downstream:

1. **Reachability is earned, not given.** The attacker never sees the whole
   topology. Its visibility is the **hacker-visible subgraph** — the exposed
   endpoints, the hosts it has compromised, and their immediate neighbours.
   Visibility grows outward from footholds. *"Where am I and what is adjacent"* is
   itself a gain the attacker accumulates. (This is why a topology mutation is so
   disruptive — see §(e).)
2. **Difficulty is priced per vulnerability, from CVSS/complexity.** Exploit
   success probability and exploit time both derive from the vulnerability's
   complexity/CVSS. *Design principle:* exploitation is substrate-priced and
   taxonomy-agnostic — the attacker does not need ATT&CK to act. *Do not* enshrine
   the exact functional form (the specific complexity→time relation is an
   implementation detail; Holm 2014's critique that the inherited exponential
   time-to-compromise is empirically suspect is flagged for Marc, not baked in
   here).
3. **The vulnerabilities are synthetic — there are no real CVEs.** IDs are
   generated, not drawn from NVD. This is the single most consequential fact for
   binding CTI to the substrate: an **ATT&CK technique is not a CVE**, and because
   the substrate's vulns are synthetic there is nothing to join a technique *to* at
   the vuln level. The attacker must be coded in ATT&CK terms at the *behaviour*
   layer, never by mapping a technique onto a specific substrate vuln
   ([`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/ch4_methods/structure_to_behaviour_binding.md) §2/§5).
   *If the substrate ever adopts NVD CVEs*, the technique→CVE→vuln binding (BRON /
   MITRE CTID) becomes possible and this constraint lifts.

The good news the HARM gives the thesis: it captures the **network/target side**
well (reachability, services, vulns, precondition chains) and therefore needs no
change — everything the profiles add (campaign objective, capability state,
MTD-conditioning) is **attacker-side**, so HARM stays untouched (D5;
[`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/ch4_methods/structure_to_behaviour_binding.md) §7).

## (c) The MTD mechanisms — terrain mutation, by what they invalidate

MTD is conventionally taxonomised **Shuffle / Diversity / Redundancy** (the "SDR"
family; Cho 2020 §III-B, Hong 2018). The right way to read the mechanisms for this
thesis is **not** by their SDR label but by *which layer of the terrain they mutate
and therefore which attacker gain they threaten*:

- **Position-mutating (network layer) — the Shuffle family that touches
  reachability/addressing.** Regenerating the topology, permuting host placement,
  or reassigning host addresses. These change *where things are and what reaches
  what* — they attack the attacker's **map**.
- **Surface-mutating (application layer) — Diversity + port/service shuffles.**
  Reassigning OS/service versions or ports. These change *what an exploit must
  match on a host you have already reached* — they attack the attacker's
  **exploit working set**, not its position.
- **Credential-mutating (reserve) — user/credential re-sampling.** Changes *which
  credentials are valid*.

**Honest scope note — Redundancy is not implemented.** Despite the SDR taxonomy
the substrate carries **only Shuffle and Diversity mechanisms**; there is no
redundant-host / spare-replica mechanism. Claims about redundancy belong to the
literature, not to what this substrate can evaluate. *(Current-implementation
fact, stated so the thesis does not over-claim the defence pool.)*

**Two durable design facts about how mutations are applied:**

1. **Exposed endpoints are never mutated.** The ingress is a permanent fixture —
   an attacker's route *in* is not something MTD takes away. Mutation protects the
   interior, not the perimeter.
2. **Only a subset of mechanisms is active by default, chosen by a scheme**
   (simultaneous / random / alternating / single / AI-selected). *Which* mechanism
   fires *when* is the defender's comparison axis at L4; the roster and cadence are
   parameters, not fixed truths. Tay's AI selection is one such scheme, reused as a
   benchmark, not extended ([`architecture.md`](architecture.md) §(a)).

Where the literature grounds each mechanism's *effect* (its strength and its
limit) is developed per tactic in the profiles; the substrate-relevant anchors:
diversity's effectiveness is **attack-class-dependent** (Evans 2011 — no help
against circumvention/fileless, significant only against incremental probing at a
high mutation rate); address/topology shuffle's effect on scanning obeys a
**mutation-rate ÷ attacker-rate ratio law** with an e⁻¹≈0.63 success ceiling under
a perfect shuffle (the scan-disruption family); and credential mutation is
**leaky** (rotation revokes a captured credential in only a minority of cases —
Zhang-Monrose-Reiter). These are the strengths *and* limits an attacker faces, and
they map directly onto the reset model below.

## (d) The attacker — the inherited baseline, its tradeoffs, and what the profile improves

**The inherited procedural attacker.** The baseline attacker is a **procedural
six-phase loop** — scan for hosts, pick and enumerate a target, scan its ports,
exploit a vulnerability (or brute-force with reused credentials), then discover a
newly-owned host's neighbours and repeat. *Design principle:* it advances by
**reachability and CVSS alone** — **objective-agnostic and taxonomy-free**, a
smash-and-grab. It was the right tool for the original MTD-comparison work (simple,
general, enough to *rank* mechanisms) and it is **retained unchanged as the
procedural baseline** the behaviourally-grounded attacker is measured against
([`architecture.md`](architecture.md) §(f)). It is *not* a straw man — it is the
inherited state of the art in this lineage, and preserving it is what makes the
comparison fair.

**Its implementation tradeoffs — stated as design choices with consequences,
because the improvement argument is defined against them:**

- **No objective.** It races toward *the* target; it cannot express that different
  campaigns traverse *different intrusion sets*. Every run is the same greedy walk.
- **No behavioural altitude.** Success and timing come from CVSS/complexity, never
  from a technique or tactic — so attacker fidelity sits at the *bottom of the
  Pyramid of Pain* (hashes/IPs/artefacts), exactly where MTD's disruptive value is
  cheapest to route around, while MTD's claim to raise cost at the *TTP* level is
  never actually stressed (Bianco 2013; [`architecture.md`](architecture.md) §(j)).
- **MTTC-incentivised, no low-and-slow.** The loop is a sprint: no patient mode, no
  waiting-out a mutation, and it abandons a host after a bounded give-up threshold.
  There is no strategic tempo to trade against the MTD interval.
- **Near-zero adaptivity.** Its only "learning" is a thin re-exploit discount on a
  vulnerability instance it revisits; it does **not** condition on MTD events (a
  beacon/criticality signal — Jalowski), recognise post-shuffle state collisions,
  or read metadata invariants (ATK-04 "no attacker learning" is a documented
  substrate divergence). The properties that make an adversary *advanced under MTD*
  are precisely the ones it lacks.
- **Capability used opportunistically, not strategically.** It harvests and reuses
  credentials, but only as a fallback — it never runs a *credential-first*
  campaign, even though (per §(e)) credentials are exactly the gain that **survives**
  a mutation. **The generic attacker under-uses the one modality MTD cannot reset.**
- **Generic chaining.** A fixed scan→exploit→pivot cycle, not an analyst-drawn
  dependency order.

**The consequence that motivates the whole thesis.** Because the baseline is a fast
sprint, **an MTD that merely *outpaces* it wins by default** — so a ranking "MTD A
beats MTD B" can be an artefact of *attacker triviality*, not defensive quality.
A fast generic attacker cannot distinguish a genuinely-good MTD from one that is
simply faster than a weak adversary. That confound is the gap the profile exists to
close.

**What the attacker knows and holds** — the state a mutation can take away, and the
state the improvement acts on. Two kinds of gain, and the distinction is the whole
ballgame:

- **Position / knowledge gains** — the current target, the in-progress action, the
  discovered-but-not-yet-owned frontier, the working set of ports and vulns on the
  host under attack. All expressed *relative to the currently-visible subgraph* and
  **contingent on the terrain staying still**.
- **Capability / conquest gains** — the hosts already compromised, and the
  **credentials harvested** from them (reused network-wide). **Standing
  possessions**, not tied to a position on the map.

This is the substrate's realisation of the "attacker with degrees of knowledge":
one that has *succeeded at reconnaissance/discovery* holds a **map**
(position/knowledge); one that has *succeeded at credential-access* holds a **key**
(capability). The two degrade completely differently under mutation — §(e). The
attacker's knowledge is **local and earned**, never global ground truth — which is
why MTD can degrade it at all, and why a recon-informed attacker (Jalowski: APTs
favour passive recon to *learn the mutation pattern*; Tularosa: deception impedes
even a knowing attacker at every kill-chain stage) is the interesting adversary.

**What the behaviourally-grounded profile improves** — three things the loop
*structurally cannot express* ([`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/ch4_methods/structure_to_behaviour_binding.md) §6/§8):

1. **Objective-conditioning** — the four operational-objective envelopes traverse
   different intrusion sets; behaviour differs *by campaign goal*.
2. **CTI-grounded chaining** — analyst-drawn technique dependencies, per objective,
   not a generic cycle.
3. **Low-and-slow stress** — a long-horizon campaign whose tempo can be *set against
   the MTD interval*, and which can lean on the reset-*survivor* modalities
   (credentials, persistence) the sprint ignores.

**The punchline — the thesis's actual result:** *MTD mechanisms that win by
outpacing the smash-and-grab attacker may **lose** against a slow, objective-driven,
CTI-grounded one* — which de-confounds attacker-triviality from MTD-quality and
advances MTD **evaluation methodology** without touching MTD or HARM. The honest
bound: only two of the four APT properties (objective, capability preconditions)
plus low-and-slow are encoded, and **adaptivity is deferred** — so the claim is
*fidelity-changes-the-answer*, never "the attacker model is true", and "APT" names
the source-genre of the CTI, not full-spectrum fidelity (§(f)).

## (e) The interaction — the reset model (the heart of it)

This is the section the per-tactic §3 reset verdicts reference. **The substrate
already implements a reset model, and that model *is* the survivor-vs-vulnerable
axis** the thesis argues. State it as a design principle, because it is the most
important durable fact in this primer:

> **A defensive mutation invalidates the attacker's *position/knowledge* gains and
> imposes a time penalty, but the attacker's *capability/conquest* gains —
> compromised hosts and harvested credentials — survive it.** The reset is
> **partial and layered**, never a clean wipe.

Concretely, by which layer the mutation touches:

- **A position-mutating (network-layer) mutation** invalidates the attacker's
  **current target and in-progress action outright** and throws it back to
  host-discovery: the map it was navigating is gone, and it must re-scan and
  re-approach. This is why **reconnaissance, discovery, and the scan-based half of
  lateral movement are reset-*vulnerable*** — their entire gain is a map that a
  topology/address shuffle erases (Alshamrani's "the rearrangement of network or
  software components renders the exploratory knowledge of the attacker useless";
  the scan-disruption ratio law bounds *how much*).
- **A surface-mutating (application-layer) mutation** invalidates only the
  **exploit working set on the host under attack** — the ports and vulns it had
  enumerated may no longer match — and throws it back to port/vuln re-enumeration
  **on the same, still-owned foothold**. It bites the *attempt*, not the
  *possession*. Its effect is attack-class-dependent (Evans): a fresh-exploit
  attempt is disrupted; a circumvention/fileless action largely is not.
- **Persistent conquest survives everything.** Compromised hosts stay owned;
  harvested **credentials are never revoked by a shuffle** and remain reusable
  network-wide. This is why **credential-access is the clearest reset-*survivor***
  (a stolen key is not location-bound; even deliberate rotation is leaky —
  Zhang-Monrose-Reiter), and why **persistence** survival is a *rate contest* (a
  foothold is contested but not cleanly evicted by a periodic mutation — the
  FlipIt move-rate ÷ re-compromise-rate law, with a genuine "no fixed answer"
  region).

Two consequences the thesis leans on:

1. **The reset verdict is per-modality, never global** — the same shuffle that
   kills a scan-based worm (its target map is invalid) leaves a credential-based
   lateral move untouched. A tactic's verdict depends on *what kind of gain the
   tactic produces*, and some tactics (lateral movement, C2) are split inside
   themselves. This per-modality split is the strongest, most falsifiable claim in
   the work — and it is grounded in *what the substrate actually does*, not only in
   the MTD literature. Each profile's §3 states its verdict **against this model**,
   and where a literature-argued verdict *diverges* from the substrate's, that
   divergence is itself a finding to record.
2. **The genuine unknown lives in the *magnitude*, not the direction.** The
   substrate fixes the *direction* of each reset (what survives, what does not);
   the literature bounds the *width* (the rate laws, the leakiness fractions); but
   no public logs ground the exact MTD→attacker effect. So the reset **fraction**
   per tactic is **declared and swept**, with the sweep width set by the §3
   uncertainty ([`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/ch4_methods/structure_to_behaviour_binding.md) §5;
   [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/ch4_methods/operational_validation.md)).

*Current-implementation embodiments (flagged as mutable, not load-bearing):* the
exact confusion/time penalty applied on interruption, the precise set of phases an
application-layer mutation interrupts, and the relabel-vs-reset handling of a
placement permutation are parameters of the current build — the *principle*
(position resets, capability survives, penalty on interruption) is the durable
part.

## (f) Substrate-side vs attacker-side — the contribution boundary

What is fixed terrain (substrate-side, **left alone** — [`architecture.md`](architecture.md) §(i)):
the HARM network, the MTD mechanism pool and scheduler, the CVSS-priced exploit
model, the metrics pipeline, the reset *direction*.

What the thesis adds (attacker-side, the seam): a **campaign objective**
conditioning which techniques are in play; **capability preconditions** gating
techniques against substrate state (non-rigid — the substrate may refuse a
CTI-legal move); **per-tactic timing** (low-and-slow vs fast); and the **declared,
swept reset fraction** layered onto the substrate's reset direction.

**The substrate-level fidelity boundary — what is deliberately *not* modelled:**
real CVEs (synthetic vulns; no technique→vuln join); redundancy MTD (not
implemented); detection/IDS ("caught" means *MTD invalidated progress*, never
*an IDS saw you* — IDS is culled); and attacker adaptivity/learning across
mutations (deferred — the one genuinely hard encoding). Naming these at the
substrate level is what keeps "APT" honest: within this substrate the profiled
attacker is a **slow, objective-conditioned, credential-and-foothold-accumulating
traversal**, and "APT" names the **source-genre of the CTI it is grounded in**,
not a claim of full-spectrum (adaptive, detection-evading) APT fidelity.

## (g) How this primer is used

- Every profile's **§3 (MTD interaction / reset verdict)** argues from §(e): state
  what gain the tactic produces (position vs capability), read its reset direction
  off the substrate model, bound its magnitude from the §4 literature, and declare
  the sweep width.
- The **duration catalogue** and the **L3b binding**
  ([`../handoffs/2026-07-03_l3_binding_scoping.md`](../handoffs/2026-07-03_l3_binding_scoping.md))
  consume the substrate-side facts in §(b)/§(d): which tactics inherit a native
  substrate verb (Tier 1) vs need a declared dwell.
- The **methodology chapter** draws its "why HARM is untouched", "why the reset is
  partial", and "why synthetic vulns force behaviour-layer coding" arguments from
  §(b)/§(e)/§(f).

## (h) Related specs and notes

- [`mtdsim_spec.md`](mtdsim_spec.md) — authoritative row-level substrate
  dispositions (the exact constants/behaviours this primer abstracts).
- [`architecture.md`](architecture.md) — the L0→L4 pipeline and the substrate-seam
  map; §(f) the L3 attacker seam, §(i) the "left alone" ledger.
- [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/ch4_methods/structure_to_behaviour_binding.md)
  — the ontology gap, the encoding ledger, MTD-reset-is-the-unknown, HARM-captures-
  the-network-side.
- [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/ch4_methods/operational_validation.md)
  — why the reset fraction is declared-and-swept, not measured.
- [`../notes/2026-07-07_thesis_backbone_rubric.md`](../notes/ch4_methods/tactic_profiles/_rubric.md)
  and [`../notes/2026-07-07_cross_sectional_review.md`](../notes/ch5_experimental_setup/evaluation_burden.md)
  — the rubric this primer serves and the review that scoped it.
- [`metrics_semantics.md`](metrics_semantics.md) — MTTC and the comparability
  boundary; §(f) the `observation_count`-is-not-a-rate prohibition.

## When this would need updating

- If the substrate **adopts real (NVD) CVEs** — §(b).3 lifts and the technique→vuln
  binding becomes feasible.
- If a **redundancy mechanism** is implemented — §(c)'s honest scope note is
  removed and the defence pool widens.
- If the substrate's **reset semantics change** (e.g. credentials become
  revocable on a shuffle) — §(e)'s survivor/vulnerable directions are re-derived
  and every profile §3 is re-checked against the new model.
- If **detection/IDS** is restored as a research thread — §(f)'s "caught = MTD
  reset" reframes.
