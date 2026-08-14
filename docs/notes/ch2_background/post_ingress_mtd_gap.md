---
status: durable
chapter: ch2_background
created: 2026-07-07
updated: 2026-07-13
lineage: 2026-07-07_post_ingress_mtd_gap.md
---

# The post-ingress gap in Moving Target Defence — what the field defends, what it does not, and why that is this thesis's reason to exist

## Position in the dissertation

The research-gap statement of the background chapter, and the motivation the introduction opens with. The dissertation's Chapter 2 "Research Gap" section carries a placeholder pointing at exactly this argument.

## The idea

Two linked observations about the state of Moving Target Defence (MTD) motivate this thesis. The first is a deployment gap: MTD reads well on paper and deploys rarely. The second — the load-bearing one — is a coverage bias: the field's centre of mass sits *before* the attacker's foothold, leaving the post-foothold campaign comparatively under-defended. The two turn out to be a single claim viewed at two altitudes, connected by a mechanism this project's own evidence surfaces independently. The introduction should open with the claim; the discussion should close on the mechanism.

### The deployment gap, and its causes

MTD's research-to-production gap is not primarily a doubt about *efficacy*; it is about *deployability*, and the diagnosis is three operational realities of production networks. First, networks are fragile: shuffling live configuration — addresses, ports, routes, service instances — risks breaking working services, and the churn MTD depends on is exactly what an operator is paid to avoid. Second, the attack surface is unknown: a surface cannot be systematically moved if it cannot be fully enumerated, and real estates carry unmapped hosts, shadow services, and undocumented dependencies. Third, legacy systems: much of the installed base can neither tolerate nor be instrumented for the reconfiguration MTD imposes, and the systems most in need of defence are the least able to host the mechanism. These are cost-and-fragility barriers, not efficacy barriers, and the distinction matters because the field's response has rightly been to attack the cost side — that response is AMTD, discussed below. *(Citation anchor — to reconcile: the deployment-gap framing and the overhead/fragility/legacy barriers are survey-level claims; anchor to an MTD survey before citing.)*

### The coverage bias

What classic MTD actually moves is the *configuration* attack surface: IP address, port, operating system, topology, and route randomisation. Tracing what that defeats along the kill chain, it invalidates the attacker's **reconnaissance** — surface intelligence gathered before a shuffle is stale after it — and it defeats **exploitation of a known configuration**, since a weaponised exploit aimed at a specific address, port, or version misses a rotated target. Both effects live before or at the foothold: in Lockheed-Martin kill-chain terms, Reconnaissance through Exploitation; in MITRE ATT&CK terms, Reconnaissance, Resource Development, and Initial Access.

What is comparatively under-served is everything from initial access onwards — the *post-ingress* campaign: execution, persistence, privilege escalation, defence evasion, credential access, discovery, lateral movement, collection, command-and-control, exfiltration, impact. MTD as a response to an intrusion already in progress — moving the target under the feet of an adversary who already holds a foothold — is the thin part of the literature, and it is the part this thesis operationalises and evaluates. *(Citation anchor — to reconcile: "the technique corpus predominantly targets the reconnaissance/exploitation surface" is a coverage claim about the field; support it from an MTD taxonomy or survey, not by assertion.)*

### Where adaptive MTD helps, and where it does not

The field's named forward direction is AMTD — *automated* (Gartner's coinage, 2023) or *adaptive* moving target defence: automate *when* and *what* to shuffle, so the cost of mutation is paid only when warranted rather than on a blind timer. AMTD is a direct and correct answer to the deployment gap, because it attacks the fragility-and-overhead barrier keeping MTD out of production. But — and this is the hinge of the argument — **automation changes MTD's responsiveness, not its phase reach**. Adaptive surface-shifting is still surface-shifting; it is still aimed at reconnaissance and exploitation. Automating the coverage does not extend the coverage, so the opportunity in the coverage bias is *orthogonal* to AMTD: the move is to push MTD's reach into the post-ingress campaign, not merely to make its pre-ingress reaction smarter. A field that automates incomplete coverage is faster at the same thing. *(Citation anchor — to reconcile: characterisation of AMTD's scope; candidate recent sources are listed in the anchors below and must be read before being attributed.)*

### Why the two observations are one claim — the mechanism

The deployment gap and the coverage bias are not independent complaints; a single mechanism ties them, and this project surfaced it independently while profiling adversary behaviour tactic-by-tactic (Chapter 3). Reviewing how each ATT&CK tactic's gains respond to a defensive mutation, three independent review passes converged on the same split:

> **Capability and credential state survives a network mutation; network-position state is invalidated by it.**

A stolen credential, an established persistence mechanism, a working command-and-control channel — the gains a post-ingress campaign banks — are not bound to any location, so the very mutation that invalidates a reconnaissance map leaves a footholded adversary largely untouched. This is precisely why surface-shifting MTD structurally under-defends the post-ingress phase: the bias is not an accident of research fashion but a consequence of what the mechanism is *good at*. And the same durability explains part of the deployment gap: to move the target under a footholded adversary, a defender must be willing to invalidate *capability* state — evict footholds, rotate credentials, rebuild hosts — which is far more disruptive to a live system than rotating an address. The motivating intuition and the strongest finding of the behavioural profiling are one claim at two altitudes; the introduction states it, and the evaluation is designed to exercise it: an MTD that wins by out-pacing a fast smash-and-grab attacker may lose against a slow, objective-driven campaign operating in exactly the phase the mechanism cannot reach.

### Terminology discipline

Two kill-chain vocabularies are in play and must not blur. The Lockheed-Martin Cyber Kill Chain (Reconnaissance → Weaponisation → Delivery → Exploitation → Installation → C2 → Actions on Objectives) is used once, to introduce the mapping; thereafter the prose stays in MITRE ATT&CK's enterprise tactics, the taxonomy the rest of the pipeline speaks. The boundary term is fixed as **post-ingress = ATT&CK Initial Access and every tactic after it**, used consistently.

### What this argument does not claim

It does not claim post-ingress MTD does not exist — only that it is the minority, under-served region of the field; that is a coverage claim, verifiable against a survey, and must be cited rather than asserted. It does not claim the MTD literature is empirically wrong about anything. And it does not yet carry settled citations: every citation anchor above is an open reconciliation task against the literature extracts, not a fact in evidence.

## Evidence and repo anchors

- The reset-split evidence: the per-tactic profiles at [`../ch4_methods/tactic_profiles/`](../ch4_methods/tactic_profiles/) (§3 blocks) and the substrate reset model in [`../../implementation/substrate_primer.md`](../../implementation/substrate_primer.md) §(e).
- The same reversal, argued from the modelling side: [`../ch4_methods/structure_to_behaviour_binding.md`](../ch4_methods/structure_to_behaviour_binding.md).
- Citation-anchor reconciliation targets: [`hong2018`](../../sources/extractions/hong2018.md), [`alshamrani2019`](../../sources/extractions/alshamrani2019.md) (deployment gap); [`evans2011_mtd_effectiveness`](../../sources/extractions/evans2011_mtd_effectiveness.md), [`mtd_scan_disruption`](../../sources/extractions/mtd_scan_disruption.md), [`mtd_stealth_effectiveness`](../../sources/extractions/mtd_stealth_effectiveness.md) (phase coverage); [`masud2025`](../../sources/extractions/masud2025.md), [`syed2025`](../../sources/extractions/syed2025.md), [`kim2026`](../../sources/extractions/kim2026.md) (AMTD scope — read before attributing).
- Governing claim in the specs: [`../../implementation/architecture.md`](../../implementation/architecture.md) §(j); single research question in [`../../workflows/project_context.md`](../../workflows/project_context.md).

## Revisit conditions

- If a survey shows post-ingress MTD is a well-populated area, the gap softens from "the field is missing this" to "the field does this differently", and the introduction reframes around *behavioural grounding* as the contribution rather than phase coverage.
- If the evaluation's discrimination and sweep experiments (see [`../ch4_methods/evaluation_burden.md`](../ch4_methods/evaluation_burden.md)) do not demonstrate the reversal, the motivation retreats to a qualitative claim under the negative-result disposition.
- If AMTD is found to already extend into post-ingress response, the "automation ≠ phase reach" argument fails and the gap narrows to the CTI-grounded evaluation method.
- If the supervisor rejects "post-ingress" as the framing term, the terminology section is rewritten and dependent headers follow.
