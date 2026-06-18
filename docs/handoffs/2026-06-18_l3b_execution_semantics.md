---
status: open
created: 2026-06-18
---

# Define + build L3b — the execution-semantics / binding layer that lets a CTI Petri-net profile drive the attacker's behaviour inside MTDSim

> **This is the executable track and the thesis's primary path.** It is distinct
> from the *analytical* track
> ([`./2026-06-18_l3_ogasp_petri_implementation.md`](./2026-06-18_l3_ogasp_petri_implementation.md),
> which solves the same net as a CTMC for closed-form MTTC). The conceptual
> groundwork — the ontology gap, the binding levels, the marking-as-capability
> product, the "envelope not actor" framing — is the note at
> [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md).
> **Read that note first; this handoff is the build/design brief it justifies.**
>
> **Supervisor discussion needed before building** — the "Open questions for the
> supervisor" section lists the decisions that change the contract.

## State of play

- **L3a is built** ([`../../data/ogasp/`](../../data/ogasp/),
  [`../../src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri)):
  four un-weighted structural tactic-place Petri nets, single moving token, the
  *grammar* of plausible technique-chains per operational objective. **Shape
  only** — no policy, no timing, no substrate binding.
- **The substrate is a 3-layer HARM** with a CVSS-grounded attacker:
  [`Network`](../../mtdnetwork/component/network.py) → `Host` → `Service` →
  `Vulnerability` (`complexity`/`cvss`/`exploit_time`/`dependent_vuln_id`); the
  inherited 6-phase attacker ([`Adversary`](../../mtdnetwork/component/adversary.py)
  + [`AttackOperation`](../../mtdnetwork/operation/attack_operation.py)) is a
  hand-coded *timed token-game* already (`_curr_process` = marking;
  `_execute_attack_action` = fire-with-`env.timeout`; MTD = interrupt).
- **The gap (why this layer is needed).** The profile speaks ATT&CK
  technique/tactic; the substrate speaks host/service/**vulnerability** (CVE/CVSS).
  No shared join key. "Plug the net in" is impossible; the binding *is* the work.
  Full argument: the note §2.
- **Nothing of L3b is built.** The architecture names the seam
  ([`../specs/architecture.md`](../specs/architecture.md) §(f): "technique → tactic
  → attacker action … alongside the inherited 6-phase attacker, selection per-run,
  not by inheritance"); no code exists.
- **Branch** `feat/l3-ogasp-petri`.

## Recommended approach

Build the binding as **five named components**. The marking is a **product:
(position in the net) × (capability footprint in the substrate)** — the net says
what is plausible next, the substrate says whether it is possible here, the policy
chooses among the legal-and-possible.

**1 — Technique → substrate action-class map.** Bind each ATT&CK technique to one
of the substrate's executable action-classes (the `ATTACK_DURATION` verbs:
SCAN_HOST / ENUM_HOST / SCAN_PORT / SCAN_NEIGHBOR / EXPLOIT_VULN / BRUTE_FORCE, or
a small extended set if justified). This is *execution* binding only — it decides
how a technique *runs* (and so its timing/success), not what it *means*.

**2 — Capability precondition/effect contract (the core).** Each technique
declares a *precondition* (capability/state it needs — a foothold on a host, a
credential, a reachable service, a prior tactic achieved) and an *effect*
(capability it grants). A transition is **enabled** only when the net permits it
*and* its precondition holds in the substrate. This is the non-rigid join: the
substrate can refuse a CTI-legal move. It is the executable reading of GAP
Decision 2 ([`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)) and a
MulVAL-style logical-attack-graph precondition model. Keep the capability
vocabulary **small and explicit** (e.g. `foothold(host)`, `cred(user)`,
`reachable(service)`, `tactic_done(t)`) — it is the contract's whole surface.

**3 — Branch policy (the "weights" debate — make it a swappable knob).** When
several transitions are enabled, *something* chooses. Implement as a strategy
object so the experiment can swap it:
- **uniform** (structural floor — start here; needs nothing);
- **weighted** (declared, swept; *not* `observation_count`-normalised —
  [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f));
- **adaptive** (MTD-event-conditioned — Jalowski beacon; **defer**).

**4 — Timing (substrate-sourced).** A fired technique consumes the substrate
duration of its action-class (`ATTACK_DURATION` / `time_generator` /
complexity-scaled `exploit_time`), inside SimPy, interruptible by MTD. **Not
corpus-sourced** (the note §5). Low-and-slow = a long-dwell timing policy vs the
inherited short timeout.

**5 — MTD-reset semantics (declared + swept).** On an MTD shuffle, invalidate a
*fraction* of the attacker's capability footprint (e.g. lose `foothold`/`reachable`
state on shuffled hosts/ports). The fraction is the genuine unknown (no public
logs); make it an **explicit parameter with a sensitivity band**, never a hidden
constant. Attaches to [`mtd_scheme.py`](../../mtdnetwork/component/mtd_scheme.py)
events.

**Wiring.** The graph-driven attacker lives *alongside* `Adversary`, selected
per-run (architecture §(f)) — both must keep working; the 6-phase baseline must
still reproduce the goldens. Reuse the SimPy driver; the difference is the
*transition structure* (GASP-net) and the *selection policy*, not the execution
machinery.

*Alternatives considered:* **phase-map binding** (tactics → 6 phases) — too lossy
for the real attacker (~14→6), but it *is* the right cheap tool for the
discrimination probe
([`./2026-06-18_profile_discrimination_probe.md`](./2026-06-18_profile_discrimination_probe.md)),
do it there first. **Vuln-instance binding** (technique→CVE→vuln, BRON) — most
faithful but needs real CVEs the synthetic substrate lacks; flag as future.

## Open questions for the supervisor

These change the contract and should be settled before building:

1. **Binding granularity** — capability precondition/effect (recommended) vs the
   cheaper phase-map vs holding out for a real-CVE substrate. How much fidelity is
   worth how much substrate change, given the honours scope?
2. **Marking semantics** — should the token literally move on the tactic net while
   a separate capability set tracks substrate state (the product), or should the
   capability set *be* the marking (1-safe achieved-set, no tactic token)?
3. **MTD-reset model** — fraction-of-capability-lost is one choice; alternatives
   are full-foothold-reset, or per-mechanism reset profiles (IP-shuffle invalidates
   `reachable`, OS-diversity invalidates an exploit). How fine?
4. **Entry/prefix** — the L3a finding is that recon is islanded in 2 of 4 classes;
   should the executable attacker seed at `initial-access` (the corpus's real
   entry) and treat recon as out-of-band, or wait on the inferred recon→IA bridge
   (GAP Decision 6 Option B)?
5. **Scope of "adaptive"** — is the Jalowski MTD-beacon primitive in or out for the
   honours MVP?

## Validation gate

L3b is done when:
1. A graph-driven attacker runs inside MTDSim on a given GASP profile and produces
   **non-degenerate, timed, technique-level attack records** (architecture §(f)
   output contract), distinct per class.
2. The **precondition contract actually gates**: there exists a CTI-legal
   transition the substrate refuses (a mechanical test of a blocked move), and no
   technique fires without its precondition met.
3. **Timing + success are substrate-sourced** (assert no rate/probability is read
   from `observation_count` or the corpus).
4. The **MTD-reset is a single declared parameter**, swept in at least one run set.
5. The **6-phase baseline still reproduces the post-2c goldens**
   ([`../../baseline/golden/`](../../baseline/golden/)) — the graph-driven attacker
   is added *alongside*, not in place of it.
6. **Deterministic** under a fixed seed (SIM-05); same seed + profile → same trace.

## Hard constraints

- **Do not touch HARM / the network model / the MTD mechanisms** — the gap is
  attacker-side (note §7); the contribution is the attacker layer only.
- **Timing and success come from the substrate; structure and chaining from the
  CTI; nothing load-bearing from `observation_count`**
  ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f)).
- **"Envelope, not actor"** — the net is a possibility-space for an objective, not
  a named actor; phrase every claim accordingly
  ([`./2026-06-18_envelope_not_actor_framing.md`](./2026-06-18_envelope_not_actor_framing.md)).
- **No-synthesis invariant** — every transition still traces to a GASP edge; the
  binding adds preconditions, it does not invent net structure.
- **Within-substrate comparability only**; the DES trace yields the **DES** MTTC
  ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(a),(d)) — not
  the analytical-track CTMC MTTC.
- Determinism, branch hygiene, **never push without an explicit ask**, Australian
  English — [`../specs/session_workflow.md`](../specs/session_workflow.md).

## Reading list

- [`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md)
  — the ontology gap, binding levels, the framing (read first).
- [`../specs/architecture.md`](../specs/architecture.md) §(f) — the L3 OGASP
  contract and the alongside-not-replace decision.
- [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  + [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  — the procedural attacker = the existing timed token-game to mirror.
- [`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
  — vuln `complexity`/`cvss`/`exploit_time`/`dependent_vuln_id` (success + timing +
  the substrate's *own* precondition model to align the contract with).
- [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) Decision 2 — the
  precondition/effect encoding intent the contract realises; Decision 6 — the
  recon→IA prefix question (open q 4).
- [`../../data/ogasp/`](../../data/ogasp/) — the L3a nets this layer parameterises.

## Out of scope (explicitly)

- The **analytical CTMC solve** (that is the other track —
  [`./2026-06-18_l3_ogasp_petri_implementation.md`](./2026-06-18_l3_ogasp_petri_implementation.md)).
- **The L4 evaluation matrix** (MTD family × profile × interval) — downstream; this
  delivers the executable attacker, not the experiment.
- **Touching HARM / network generation / MTD mechanisms / the orchestrator.**
- **The adaptive (Jalowski-beacon) policy** unless promoted in supervisor q 5.
- **The recon→initial-access inferred bridge** — pending the entry decision (q 4);
  build on the observed-only base first.
- **IDS / detection**; retraining Tay's RL agent (project-wide out of scope).
