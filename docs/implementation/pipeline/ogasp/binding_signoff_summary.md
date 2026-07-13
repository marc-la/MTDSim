---
status: durable
created: 2026-07-13
updated: 2026-07-13
topic: "L3b binding — one-page sign-off summary for Dr Jin Hong"
---

# L3b binding — one-page recommendation for sign-off

*Companion to the full investigation
[`binding_design_space.md`](binding_design_space.md) and the per-tactic ledger
[`tactic_action_map.csv`](../../../../data/ogasp/timeline/tactic_action_map.csv).
Everything below is **pending your confirmation** before any implementation.*

## The question

How should the class-profiled Petri-net timelines (`ogasp-timeline/v1`) drive an
attacker inside MTDSim, such that the four operational-objective classes produce
**visibly different** simulator behaviour — from each other and from the
inherited 6-phase attacker — rather than the same phase loop with new labels
(the anti-goal)?

## The recommendation

**Stage C1 → C2, built inside the C3 dispatch architecture.**

- **C1 (the v1 spine, fastest to results):** the attacker *replays* the timeline —
  for each tactic-state it waits the state's dwell and fires the mapped substrate
  verb(s); run success is read off the class objective. **What differs from the
  baseline:** the classes follow a CTI-grounded *order* at a CTI-grounded *tempo*
  (low-and-slow vs sprint), so against a fixed MTD schedule they absorb different
  numbers of mutations and yield different MTTC/ASR.
- **C2 (the immediate next increment, the anti-goal's real answer):** each tactic
  gains a *capability* precondition/effect (foothold, credentials, map, C2
  channel). Because the substrate **already** makes credentials survive a shuffle
  while a scanned map does not, a *credential-first* class recovers from a
  network mutation by reusing its key while a *scan-first* class is thrown back to
  re-scanning — **a second, independent axis of class separation that does not
  depend on the nets being far apart.**
- **C3 (the architecture, not a separate deliverable):** build the dispatch as a
  class-conditioned *selection* point, so the R2 success-rate axis, the R3 style
  vectors, and the eventual two-way coupling attach **without a rewrite**.

Nothing touches the network, the MTD mechanisms, the vulnerability pool, or the
statistics maths (D5). The baseline path stays byte-identical, so the goldens are
untouched. The whole change is a new attacker-side operation class plus a
dispatch module.

## Why not the alternatives

- **A plain re-skin (map each tactic to a verb, let the greedy loop run)** —
  rejected: the timeline would be decorative and every class would produce the
  baseline's greedy walk. This is the anti-goal; it is dead on the
  distinguishability test.
- **The technique → CAPEC → CWE → CVE → CVSS chain as the bridge** — rejected for
  MVP, positioned as future work: the substrate's vulnerabilities are synthetic
  (no CVE keys), so the chain yields a *label*, not a *join*; and the published
  crosswalks are sparse at every hop (~419 CVEs curated to ATT&CK; ~112/546
  CAPECs mapped). It only becomes worthwhile if the substrate ever adopts real
  NVD CVEs. **This is the item most needing your explicit confirmation.**
- **Full two-way coupling (the net stepping inside the simulator)** — rejected for
  v1 per D2; it stays the deferred end goal, and C3 keeps the on-ramp to it.

## Decisions I need from you

1. **Confirm C1→C2 staged** as the MVP binding (or redirect). In particular:
   confirm that bringing the **capability contract forward into v1** is right —
   the earlier scoping deferred it to the two-way upgrade, but it is cheap here
   (the substrate already implements the survival split) and it is the design's
   best defence against the classes separating only weakly at the routing level
   (all four sit below the shuffled-label null — a real risk).
2. **Confirm the CVE-chain is future work**, not the MVP bridge (reason above).
3. **Confirm cost-only** for the nine no-network-state / stealth / objective
   tactics (R5 already points this way) and **objective-read success** for the
   terminal tactics — coexisting with, not changing, the baseline's MTTC.
4. **Confirm the MTD-interruption policy**: the bound attacker *inherits* the
   substrate's existing interrupt handling (position resets, capability survives),
   rather than a timeline-rigid "resume where you left off".

## The honest caveat

The classes currently separate only weakly at the net-routing level. C1 alone may
under-separate them; C2's survival axis is the hedge, which is why it is staged
immediately behind C1 rather than deferred. If C1+C2 still do not separate the
classes under MTD, that negative result — argued — is itself a legitimate finding
of the evaluation, not a failure of the binding.
