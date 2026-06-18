---
status: durable
created: 2026-06-18
topic: from CTI structure to executable attacker behaviour — the ontology gap, the binding layer, and "envelope not actor"
---

# Carrying CTI into the simulator — how a Petri-net profile becomes attacker *behaviour*, and where the real gap is

## Why this is worth recording

This is the conversation that located the **make-or-break seam** of the whole
attack-profiling-for-MTD thesis, and it is almost entirely methodological — the
kind of thing that is obvious in hindsight, invisible in the code, and fatal if
left implicit. The L3a structural Petri nets
([`../../data/ogasp/`](../../data/ogasp/)) are *shape only*; the question
"how do you turn that shape into an attacker that behaves inside MTDSim?" is
where most graph-based-attacker work stops — people define the formalism well
and never execute it, because the execution is system-specific, underspecified,
and unglamorous. This note pins down (a) the **ontology gap** between the GASP
profiles and the substrate that makes "just plug the net in" impossible, (b) the
**binding layer** that closes it (the actual contribution), (c) the honest
framing — **behavioural *envelope*, not *actor*** — that the design must commit
to up front, and (d) what the profile actually *buys* over the inherited
procedural attacker. It is the backbone of the methodology chapter and the brief
the next build works from. Three handoffs spin out of it:
[`../handoffs/2026-06-18_l3b_execution_semantics.md`](../handoffs/2026-06-18_l3b_execution_semantics.md)
(build the binding layer),
[`../handoffs/2026-06-18_profile_discrimination_probe.md`](../handoffs/2026-06-18_profile_discrimination_probe.md)
(check the profiles even separate, first),
[`../handoffs/2026-06-18_envelope_not_actor_framing.md`](../handoffs/2026-06-18_envelope_not_actor_framing.md)
(adopt the framing).

## The substance

### 1. Three levels, one confusion dissolved: structure vs policy vs execution

The recurring question — *"is the simulation execution the behaviour?"* — has a
clean answer once three things are kept apart:

- **Structure** — the Petri net (L3a). The *grammar* of which moves are legal.
- **Policy** — which enabled transition fires, and when. The *behaviour*.
- **Execution** — one walk through the grammar under the policy, against the
  world. The *trace*.

The execution **realises** behaviour; it is not itself the behaviour. Behaviour
lives in the **policy**, about which the structural net says nothing. That is why
"the nets only have shape" feels unfinished — it is. The net is necessary, not
sufficient.

The sharper, less comfortable consequence — and the honest answer to *"what
tradeoff persists with the attack-flow→Petri call?"* — is that **the aggregated
per-class net is a *possibility space*, not a behaviour.** Each class net is the
*union* of 5–19 attack flows. A token taking a free walk can stitch
technique-A-from-Conti onto technique-B-from-Turla and produce a chain **no real
actor ever ran**. The strength (real, analyst-drawn technique dependencies) and
the limitation (aggregation over-generates) are the *same fact*. The net is a
**behavioural envelope for an operational objective**, not an actor's policy.
That phrase is both the caveat and the defensible framing —
[`../handoffs/2026-06-18_envelope_not_actor_framing.md`](../handoffs/2026-06-18_envelope_not_actor_framing.md).

### 2. The ontology gap — why you cannot "plug the net in as-is" (the heart of it)

The substrate and the profile are **two graphs over two different node-types
with no shared join key.** Grounded in the actual code:

- **Substrate (the "green"/network, a 3-layer HARM):**
  [`Network`](../../mtdnetwork/component/network.py) →
  [`Host`](../../mtdnetwork/component/host.py) (an internal Watts–Strogatz
  service graph) → [`Service`](../../mtdnetwork/component/services.py) →
  [`Vulnerability`](../../mtdnetwork/component/services.py). A vuln carries
  `complexity`, `cvss = (complexity + impact)/2`,
  `exploit_time = ATTACK_DURATION·(1 − complexity)`, and **precondition
  chaining** (`dependent_vuln_id` / `can_exploit_with_dependent_vuln`). The
  inherited attacker ([`Adversary`](../../mtdnetwork/component/adversary.py) +
  [`AttackOperation`](../../mtdnetwork/operation/attack_operation.py)) lives
  *entirely* here: scan→enum→scan-port→exploit-vuln/brute→pivot, with success
  and timing from **CVSS/complexity** — taxonomy-agnostic.
- **Profile (the L3a Petri net):** nodes are **tactics**, transitions are
  **technique-pairs**; success, timing, and host have *no representation*.

| | nodes | atomic action | success / time from | provenance |
|---|---|---|---|---|
| **Substrate (HARM)** | host / service / **vulnerability** | exploit *this vuln* on *this service* | CVSS / `complexity` | synthetic (random) |
| **Profile (Petri)** | **technique / tactic** | perform technique T (tactic A→B) | — (no notion) | real CTI |

An ATT&CK technique (T1190) is **not** a vulnerability (a CVE); it is a *class of
behaviour* that, in a concrete network, would be *realised by* exploiting some
vuln. **ATT&CK ≠ CVE.** There is no host in a tactic-token and no technique in a
substrate exploit. So "map the net to the substrate" is not a relabel — it is
**defining a contract between two ontologies that were never built to meet**, and
that contract is the missing layer. This is precisely where graph-attacker work
stalls: the theory is the net; the execution is the binding; the binding is
system-specific and therefore absent from the literature. **Naming this gap
precisely is half the methodological contribution.**

### 3. Two readings of one net — analytical vs executable

The same L3a net supports two operationalisations, and the thesis must not
conflate them:

- **Analytical** — solve the net as a CTMC for closed-form MTTC/ASR. This is the
  [`l3_ogasp_petri_implementation`](../handoffs/2026-06-18_l3_ogasp_petri_implementation.md)
  roadmap (D4/D2/D3), and the feasibility study
  ([`./2026-06-18_l3_petri_feasibility.md`](./2026-06-18_l3_petri_feasibility.md))
  judged it **GO-conditional**. It is *parallel/secondary*: a second analytical
  substrate, not comparable in magnitude to the DES.
- **Executable** — bind the net to MTDSim so the profile *drives the SimPy
  attacker's behaviour*. This is the **primary** track for the thesis's stated
  goal (MTD comparison under behaviourally-grounded attackers), and it is what
  L3b is about.

They are the two readings I keep circling: solve it, or run it. The structural
net feeds both.

### 4. State binding, done properly

"Binding tactics to the HARM layers" is close but slightly mis-aimed. The binding
is not *tactic → HARM-layer*; it is a **precondition/effect contract** between the
net's transitions and the substrate's *capability state*. Three levels, cheapest
to most faithful:

1. **Phase-map (cheap, lossy).** Collapse each tactic onto one of the 6 existing
   substrate phases; the net only *re-sequences* native actions. Quick, but ~14
   tactics onto ~6 phases throws the CTI structure away. Use only for the
   discrimination probe (§10), not the real attacker.
2. **Capability precondition/effect (the right target).** Each technique declares
   a *precondition* (capability/state needed — a foothold, a credential, a
   reachable service) and an *effect* (capability granted). The **marking becomes
   a capability set**, and a technique fires only when *both* the net enables it
   *and* its precondition holds in the substrate. This is non-rigid (the substrate
   can block a CTI-legal move), it is **exactly GAP Decision 2**
   ([`../specs/01_gap_schema.md`](../specs/01_gap_schema.md): conditions→places,
   actions→transitions), and it is the classic logical-attack-graph
   (MulVAL-style) precondition model.
3. **Vuln-instance (most faithful, infeasible here).** technique → CVE → vuln.
   Needs *real* CVEs; the substrate's vulns are synthetic, so there is nothing to
   join on. The real-world bridge exists — **BRON** (Hemberg et al.,
   ATT&CK↔CAPEC↔CWE↔CVE↔CPE) and MITRE/CTID's ATT&CK↔CVE mappings — but it
   requires NVD-sourced vulns in the substrate. Future, not MVP.

So the MVP binding is: **the marking is a product — (position in the net) ×
(capability footprint in the substrate).** The net says *what is plausible next*;
the substrate says *whether it is possible here*; the policy chooses among the
legal-and-possible. "Robust and non-rigid" = the substrate is allowed to refuse a
CTI-legal move.

### 5. The encoding ledger — where each piece actually lives

| Question | Where it lives | The call |
|---|---|---|
| **Exploits** | substrate (vuln on service) | Stay native. Techniques map to action-*classes*; do not write new exploit code. |
| **P(success)** | substrate (CVSS / `complexity`) | Substrate-sourced. CTI cannot supply it (the corpus is "what the analyst drew", not efficacy). Same logic as timing. |
| **Chaining** | **the net** (precondition/effect) | **The value-add.** CTI-grounded "which technique enables which", per objective. |
| **Getting caught** | out of scope | IDS is culled. "Caught" = MTD invalidates progress, not detection. Keep it. |
| **MTD → attacker effect** | **inferred → declared** | The genuine unknown (no public logs; we know attacker→MTD better than MTD→attacker). Model as a *reset fraction* of capability state on shuffle; **declare and sweep** it (sensitivity band), never hide it. |
| **MITRE-coding the substrate** | behaviour layer only | Code the *attacker* in ATT&CK; you **cannot** join ATT&CK to the synthetic vulns (no CVEs). Conflating the two taxonomies is the trap. |

The through-line: **timing and success come from the substrate; structure and
chaining come from the CTI; nothing load-bearing comes from `observation_count`**
(which is "how often the analyst drew it", not a probability —
[`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f)).

### 6. What the profile buys over the inherited procedural attacker

The 6-phase loop is objective-agnostic, taxonomy-free, smash-and-grab — and it
*was the right call* for the original work: simple, non-taxonomy-specific, enough
to compare MTD mechanisms. Its known weakness is exactly why APTs were brought in:
an MTD that merely *outpaces* a fast generic attacker wins by default, so "MTD A
beats MTD B" can be an artefact of attacker triviality. The Petri profile buys
three things the loop structurally cannot express:

1. **Objective-conditioning** — `pure_steal` / `pure_impediment` /
   `double_extortion` / `infrastructure_setup` traverse *different intrusion
   sets*; the attacker's behaviour differs *by campaign goal*.
2. **CTI-grounded chaining** — analyst-drawn dependency order, not a generic
   scan→exploit→pivot cycle.
3. **Low-and-slow stress** — a campaign over many tactics and a long horizon, vs
   the MTTC-incentivised smash-and-grab.

The thesis punchline lives in (3): **MTD mechanisms that win by simply outpacing
the smash-and-grab attacker may lose against a slow, objective-driven,
CTI-grounded one.** Demonstrating that advances MTD *evaluation methodology* —
the stated goal — without touching MTD or the HARM model.

### 7. Does HARM capture the "quintessential network"? Yes — and that is good news

The host/service/vuln HARM captures the **network/target** side well
(reachability, services, vulns, precondition chains). What it does *not* capture
— campaign objective, attacker memory/learning, capability state,
MTD-conditioning — is **attacker-side**, not network-side; it does not belong in
HARM. So **HARM need not be touched** (honouring the no-reinvent-the-substrate
constraint); the entire contribution sits in the attacker representation layered
on top. The cleanest possible scoping.

### 8. The four APT properties, distributed across the three knobs

"Advanced, adaptive, persistent, with capabilities and objectives" is not one
encoding — it decomposes cleanly across the design knobs, which also says what is
MVP vs deferred:

| APT property | Where it is encoded | MVP? |
|---|---|---|
| Specific **objective** over a campaign | the GASP profile (done) | ✅ |
| **Capabilities** / preconditions | the L3b precondition/effect contract | ✅ |
| **Low-and-slow** / persistent | the timing policy (long dwell vs short timeout) | ✅ |
| **Adaptive** / learns from interaction | branch policy conditioned on MTD events (Jalowski "beacon" primitive, architecture §(f)) | ⛔ defer — the one genuinely hard encoding |

### 9. The pipeline restructure this implies

The instinct "L3 is subsumed by L3a; the layer becomes the formal representation
of baseline behaviour" is right. Make the missing layer explicit:

| layer | what it is | status |
|---|---|---|
| **L1 GAP** | lossless technique-dependency structure | built |
| **L2 GASP** | objective-conditioned profiles | built |
| **L3a** | formal Petri net = the *behavioural grammar* (shape only) | **built** ([`../../data/ogasp/`](../../data/ogasp/)) |
| **L3b** | **execution semantics / binding layer** — precondition/effect contract + branch policy + timing binding + MTD-reset semantics | **the new work** |
| **L3(c) OGASP** | the *executed* attacker in MTDSim → timed technique-level traces | unbuilt |
| **L4** | evaluation: MTD-mechanism × attacker-profile × metric | unbuilt |

The old "L3 graph-driven attacker seam" *is* L3b+L3c; L3a is the formal
baseline-behaviour artefact they execute. **L3b is the layer where everyone
stops** — defining it is the methodological move.

### 10. L4 state of play, and the risk that matters more than the encoding

- **Strong:** metrics defined (MTTC/ASR/RoA/path-exposure), corrected substrate +
  goldens, within-substrate comparability discipline
  ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(d)).
- **Fuzzy / must-resolve:**
  1. **The discrimination check is a bigger risk than the encoding.** Do the four
     profiles produce *distinguishable* MTD-comparison outcomes at all? If not,
     the workstream inherits the L2-synthesis negative-result disposition
     ([`./2026-05-29_l2_synthesis.md`](./2026-05-29_l2_synthesis.md) parking-lot).
     **Test this cheaply, first** —
     [`../handoffs/2026-06-18_profile_discrimination_probe.md`](../handoffs/2026-06-18_profile_discrimination_probe.md).
  2. **Metric identity** — the CTMC-MTTC is not the DES-MTTC even on the same net
     (feasibility study §6.3). Keep them named apart.
  3. **MTD→attacker reset** — the declared, swept parameter from §5.
- **The experiment that yields a result:** `MTD-mechanism × {procedural baseline,
  four CTI profiles} → MTTC/ASR`. The finding: *does behaviourally-grounded,
  objective-conditioned profiling change the MTD ranking vs the generic
  attacker?* Bounded, honest, publishable — and the honest claim is
  *fidelity-changes-the-answer* (architecture §(j)), never "the model is true".

### 11. The MVP cut, stated plainly

One targeted substrate addition (the L3b binding), nothing else touched: the net
drives **technique selection + chaining**; **capability preconditions** gate it
against substrate state (non-rigid); **timing + success stay substrate-native**;
**MTD-reset is a declared, swept parameter**. Start the branch policy **uniform**
(structural floor) and ask whether even a uniform walk over CTI-grounded,
objective-conditioned structure moves the MTD comparison. That alone is a
defensible honours result; weighted/adaptive policies are upside, not
prerequisite.

## How it connects

- **To the spec.** Sits under [`../specs/architecture.md`](../specs/architecture.md)
  §(f) (L3 OGASP — the technique→tactic→action bridge named there *is* L3b) and
  §(j) (the fidelity-changes-the-answer claim the envelope framing protects);
  governed by [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md)
  §(a) (DES MTTC, which the executable trace produces) and §(f) (the
  not-a-Markov-chain / `observation_count`-is-not-a-rate prohibition); the binding
  is the executable reading of [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)
  Decision 2.
- **To the L3a build.** Consumes the structural nets at
  [`../../data/ogasp/`](../../data/ogasp/) and the code at
  [`../../src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri).
- **To the substrate.** [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py),
  [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  (the procedural attacker the graph-driven one runs *alongside*),
  [`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
  (vuln/CVSS/exploit-time/dependency), [`../../mtdnetwork/component/mtd_scheme.py`](../../mtdnetwork/component/mtd_scheme.py)
  (the MTD orchestrator the reset semantics attach to).
- **To the lit review.** Closest executable precedent: **Bland 2020**
  ([`../extractions/bland2020.md`](../extractions/bland2020.md)) — SPN + RL agent,
  run Monte-Carlo, *executed* not solved. Closest CTI-structure precedent:
  **Rodríguez 2024** ([`../extractions/rodriguez2024.md`](../extractions/rodriguez2024.md))
  — tactic-level discovered nets, but *not* executable. The binding bridge is
  **BRON** (Hemberg et al.) / MITRE CTID ATT&CK↔CVE and **MulVAL** (Ou et al.)
  logical attack graphs — *not yet extracted*; reconcile before citing (papers are
  claims, [`../specs/guardrails.md`](../specs/guardrails.md)). The adaptive primitive
  is **Jalowski** (architecture §(f)).
- **To open work.** The three handoffs above; the analytical track at
  [`../handoffs/2026-06-18_l3_ogasp_petri_implementation.md`](../handoffs/2026-06-18_l3_ogasp_petri_implementation.md).

## When this would need updating

- If the **discrimination probe** shows the four profiles do not separate under
  MTD — the executable track inherits the negative-result disposition and §6/§11
  are rewritten around it.
- If the **substrate adopts real (NVD) CVEs** — the vuln-instance binding (§4
  level 3, BRON) becomes feasible and the capability-level binding is no longer
  the ceiling.
- If the **envelope-not-actor framing is rejected** by Marc/supervisor in favour
  of a per-flow single-actor net — §1's possibility-space argument and the whole
  aggregation tradeoff are re-opened.
- If **HARM is changed** (it should not be) — §7's "attacker-side gap, network
  untouched" scoping no longer holds.
