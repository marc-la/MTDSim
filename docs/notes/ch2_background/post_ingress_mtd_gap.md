---
status: durable
created: 2026-07-07
topic: "the post-ingress MTD gap — why MTD's research-to-production gap and its pre-ingress phase-bias are the thesis's motivation, and where AMTD does and doesn't help"
---

# The post-ingress MTD gap — what the field defends, what it doesn't, and why that is this thesis's reason to exist

## Why this is worth recording

This is the **motivation paragraph** of the whole thesis, arrived at as an
epiphany and worth pinning before it dissolves back into ambient intuition. It
names two linked facts about the state of MTD — (A) a persistent gap between MTD
*research* and MTD in *production*, and (B) a phase-coverage bias: the field's
centre of mass sits *before* the attacker's foothold (defeating reconnaissance
and exploitation), leaving the *post-ingress* campaign comparatively
under-defended by MTD — and it observes that (B) is where this thesis lands. The
reason to record it now is that it is not a free-floating opinion: prong (B) has
a **mechanistic underpinning already surfaced in our own evidence** (the
reset-verdict split — capability/credential state survives a network mutation,
only network-position state is invalidated), so the epiphany and the strongest
finding in the tactic-profile review turn out to be *the same claim at two
altitudes*. That convergence is the argument the introduction should open with
and the discussion should close on. This note fixes the framing, the
terminology, and — per the guardrails — flags every empirical sub-claim as a
citation anchor to reconcile against the lit review rather than asserting it as
settled.

## The substance

### Prong A — the research-to-production gap, and its causes

MTD reads well on paper and deploys rarely. The gap is not primarily a doubt
about *efficacy* — it is about *deployability*, and the diagnosis is three
operational realities of real networks:

1. **Networks are fragile.** Shuffling live configuration (addresses, ports,
   routes, OS/service instances) risks breaking working services; the churn MTD
   depends on is exactly what a production operator is paid to avoid.
2. **The attack surface is unknown.** You cannot systematically move a surface
   you cannot fully enumerate. Real estates have unmapped hosts, shadow services,
   and undocumented dependencies; MTD's clean "shift the surface" abstraction
   assumes a surface that is knowable in the first place.
3. **Legacy systems.** Much of the installed base cannot tolerate — or be
   instrumented for — the reconfiguration MTD imposes. The systems most in need
   of defence are the least able to host the mechanism.

These are **cost/fragility barriers, not efficacy barriers**, and that
distinction matters: it means the field's response has (rightly) been to attack
the *cost* side. That response is AMTD (below). *(Citation anchor — verify: MTD
deployment/adoption-gap framing and the overhead/fragility/legacy barriers are
survey-level claims; reconcile against the MTD-survey extractions — candidates
[`../extractions/hong2018.md`](../extractions/hong2018.md),
[`../extractions/alshamrani2019.md`](../extractions/alshamrani2019.md) — before
citing. Do not assert as fact until anchored.)*

### Prong B — the phase-coverage bias (the load-bearing one)

What classic MTD actually moves is the **configuration attack surface** — IP /
port / OS / topology / route randomisation. Trace what that *defeats* along the
kill chain:

- It invalidates the attacker's **reconnaissance** — surface intel gathered
  before a shuffle is stale after it.
- It defeats **exploitation of a known configuration** — a weaponised exploit
  aimed at a specific address/port/version misses a rotated target.

Both of those live *before or at the foothold*. In Lockheed-Martin kill-chain
terms that is **Reconnaissance → Weaponisation → Delivery → Exploitation**; in
MITRE ATT&CK terms it is **Reconnaissance / Resource Development / Initial
Access**. So the field's mass sits **pre-ingress**: beat the adversary before or
at the moment they get in.

What is comparatively under-served is everything **initial-access onwards** —
the *post-ingress* campaign: Execution, Persistence, Privilege Escalation,
Defence Evasion, Credential Access, Discovery, Lateral Movement, Collection,
Command-and-Control, Exfiltration, Impact. MTD as a *response to an in-progress
intrusion* at these stages — moving the target *under the feet of an adversary
who already has a foothold* — is the thin part of the literature. That is the
gap the epiphany names, and it is the gap this thesis operationalises.
*(Citation anchor — verify: the claim that the MTD technique corpus predominantly
targets the recon/exploitation surface should be evidenced from
[`../extractions/evans2011_mtd_effectiveness.md`](../extractions/evans2011_mtd_effectiveness.md),
[`../extractions/mtd_scan_disruption.md`](../extractions/mtd_scan_disruption.md),
and [`../extractions/mtd_stealth_effectiveness.md`](../extractions/mtd_stealth_effectiveness.md);
the "post-ingress is under-served" claim is a coverage claim about the field —
support it from an MTD taxonomy/survey, don't assert it.)*

### Where AMTD helps — and where it doesn't

The field's named forward direction is **AMTD — Automated (Gartner's coinage,
2023) / Adaptive Moving Target Defence**: automate *when* and *what* to shuffle so
the cost is paid only when warranted, rather than on a blind timer. AMTD is a
direct and correct answer to **prong A** — it attacks the fragility/overhead
barrier that keeps MTD out of production.

But — and this is the hinge of the epiphany — **automation changes the
*responsiveness* of MTD, not its *phase reach*.** Adaptive surface-shifting is
still surface-shifting; it is still aimed at reconnaissance and exploitation.
Automating the coverage does not extend the coverage. So the opportunity in prong
(B) is **orthogonal to AMTD**: the move is to push MTD's *phase reach* into the
post-ingress campaign, not merely to make its pre-ingress reaction smarter. A
field that automates the wrong (or incomplete) coverage is faster at the same
thing. *(Citation anchor — verify: characterisation of AMTD's scope; candidate
recent extractions
[`../extractions/masud2025.md`](../extractions/masud2025.md),
[`../extractions/syed2025.md`](../extractions/syed2025.md),
[`../extractions/kim2026.md`](../extractions/kim2026.md) may support or refine
this — read before attributing; do not guess their contents.)*

### Why (A) and (B) are the same story — and the mechanism we already have

The two prongs are not independent gripes; a single mechanism ties them, and we
have already surfaced it. The tactic-profile cross-sectional review
([`./2026-07-07_cross_sectional_review.md`](./2026-07-07_cross_sectional_review.md))
found — from three independent lenses — that the reset behaviour of an attacker
against a network mutation **splits by what kind of gain the tactic produces:**

> **Capability / credential state *survives* a shuffle; network-position state is
> *invalidated* by it.**

That is precisely why surface-shifting MTD structurally under-defends the
post-ingress phase. The gains a post-ingress campaign banks — a stolen
credential, an established persistence mechanism, a working C2 channel — are
**shuffle-durable**: the very mutation that invalidates a pre-ingress
reconnaissance leaves an already-footholded adversary largely untouched. So MTD's
pre-ingress bias (B) is not an accident of research fashion; it is what the
mechanism is *good at*. And the same durability is part of why post-ingress MTD
is hard to build and deploy (A): to move the target under a footholded adversary
you must be willing to invalidate *capability* state, which is far more disruptive
to the live system than rotating an address. **The epiphany (motivation) and the
reset-split (evidence) are one claim at two altitudes** — the introduction states
it, the discussion proves it with our own timelines.

This is also the sharper form of the punchline already recorded at
[`./2026-06-18_cti_to_executable_behaviour.md`](./2026-06-18_cti_to_executable_behaviour.md)
§6: *an MTD that wins by out-pacing a smash-and-grab attacker may lose against a
slow, objective-driven, post-ingress campaign.* "Post-ingress" is the name for
the phase where that reversal lives.

### Terminology discipline (so the dissertation stays consistent)

Two kill-chain vocabularies are in play and they must not be blurred in the
prose:

- **Lockheed-Martin Cyber Kill Chain:** Recon → Weaponisation → Delivery →
  Exploitation → Installation → C2 → Actions on Objectives.
- **MITRE ATT&CK Enterprise tactics:** the 14 the tactic profiles are built on
  ([`../tactic_profiles/`](../tactic_profiles/)).

Fix **"post-ingress" = initial-access onwards** (ATT&CK Initial Access and every
tactic after it) as the boundary term and use it consistently; introduce the
kill-chain mapping once, then stay in ATT&CK because that is the taxonomy the rest
of the pipeline (L1 GAP → L2 GASP → the 15 profiles) speaks.

### What this note does *not* claim

Per the guardrails (papers are claims to reconcile, never assert a paper wrong,
never guess a locator):

- It does **not** claim post-ingress MTD does not exist — only that it is the
  **minority / under-served** region of the field. That is a coverage claim,
  verifiable against a survey, and must be cited not asserted.
- It does **not** claim the MTD literature is empirically wrong about anything.
- It does **not** yet carry settled citations. Every `Citation anchor — verify`
  above is a to-do against [`../extractions/`](../extractions/) / the gitignored
  lit review, not a fact in evidence.

## How it connects

- **To the thesis's central object.** This is the *why* for the object defined in
  [`./2026-07-07_thesis_backbone_rubric.md`](./2026-07-07_thesis_backbone_rubric.md):
  the per-tactic APT × dynamic-network interaction. The rubric says *what* each
  profile must deliver; this note says *why the whole subsection matters* — it is
  the post-ingress evaluation the field is missing.
- **To the evidence.** The reset-verdict split in
  [`./2026-07-07_cross_sectional_review.md`](./2026-07-07_cross_sectional_review.md)
  is the mechanism under prong (B); the durability of capability/credential gains
  is why post-ingress resists surface-shifting MTD.
- **To the punchline.**
  [`./2026-06-18_cti_to_executable_behaviour.md`](./2026-06-18_cti_to_executable_behaviour.md)
  §6 (out-pace-the-smash-and-grab) is the same reversal, now phase-named.
- **To the profiles.** [`../tactic_profiles/`](../tactic_profiles/) 03–15 *are*
  the post-ingress phase; profiles 01–02 are the pre-ingress surface MTD already
  targets. The imbalance this note names is visible in which tactics the substrate
  even has a verb for.
- **To the spec.** Sits upstream of
  [`../specs/architecture.md`](../specs/architecture.md) §(j) (the
  *fidelity-changes-the-answer* claim — the honest form of this motivation) and
  [`../specs/project_context.md`](../specs/project_context.md) (the single RQ:
  evaluate existing MTD against behaviourally-grounded CTI profiles — i.e.
  post-ingress campaigns).
- **To the lit review.** The citation anchors above are the reconciliation
  worklist: MTD deployment-gap survey (A); MTD-technique phase-coverage taxonomy
  (B); AMTD scope (masud2025 / syed2025 / kim2026, verify). None cited until
  anchored.

## When this would need updating

- If a survey shows **post-ingress MTD is a well-populated area**, not a gap —
  prong (B) softens from "the field is missing this" to "the field does this
  differently", and the introduction reframes around *behavioural grounding* as
  the contribution rather than *phase coverage*.
- If the **discrimination probe / timeline runner shows the profiles do not
  separate** under MTD — the post-ingress reversal is undemonstrated and the
  motivation must retreat to a purely qualitative claim (inherits the
  negative-result disposition noted across the L3 handoffs).
- If **AMTD is found to already extend into post-ingress** (adaptive response to
  in-progress intrusions) — the "automation ≠ phase reach" argument is wrong and
  the gap this thesis fills narrows to the *CTI-grounded evaluation method*, not
  the phase.
- If Marc/supervisor **reject "post-ingress" as the framing term** in favour of a
  kill-chain-native phrasing — the terminology-discipline section is rewritten
  and the profiles' section headers follow.
