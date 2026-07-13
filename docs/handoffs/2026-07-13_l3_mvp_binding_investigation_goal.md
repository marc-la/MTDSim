---
status: session-seed (companion to 2026-07-13_l3_mvp_binding_investigation.md; not a handoff)
created: 2026-07-13
---

# Goal — one workable, grounded, defensible MVP bind pipeline across the Petri-net→MTDSim gap, argued into existence and packaged for supervisor sign-off

## Mission

Produce and recommend **one end-to-end MVP binding design** — the contract
that turns a class-profiled Petri-net behaviour envelope into executable
attacker behaviour inside MTDSim — such that Marc can defend the choice to
his supervisor in one page, and the deferred replay-attacker build can
implement it without re-deriving a single decision. The procedural brief
(steps, gates, constraints, reading order) is
[`2026-07-13_l3_mvp_binding_investigation.md`](./2026-07-13_l3_mvp_binding_investigation.md);
this file defines the target and the quality bar. Where they conflict, the
brief's hard constraints win.

## The gap, precisely — because "most appropriate" is measured against it

On one side: a **tactic-level behaviour envelope** — a single token walking
a weighted net; ~15 tactic-places; transition weights that are flow
recurrence shares (not rates); dwell times that are declared, swept
estimates (shape-not-scale); termination on per-class objective sets;
backward transitions present; techniques recorded inside places but not
driving traversal. It carries *routing, occupancy, ordering, termination,
and class identity* — and nothing finer.

On the other side: a **host/service/synthetic-vulnerability DES** — six
executable verbs, complexity-priced exploits, no CVE keys, a hardcoded
6-phase attacker as the comparability baseline, and a substrate that is
**malleable within the goldens**: attacker-side additions are fair game;
anything that changes baseline runs byte-for-byte is not.

**The most appropriate binding is the one matched to the information
actually present on both sides.** It must not demand precision the envelope
does not carry (technique-level fidelity, wall-clock realism, actor
attribution), and it must not waste information the envelope *does* carry —
class routing, occupancy structure, objective termination, backward
transitions are the signal; a binding that flattens them back into a fixed
action loop has discarded the entire L0→L3 pipeline and fails.

## What "workable MVP bind pipeline" means — the recommendation must specify all of it

1. **Input contract** — what the bound attacker consumes (`ogasp-timeline/v1`
   or an argued alternative) and the schema-pinning rule.
2. **Per-tactic dispatch** — for every tactic-place in the L3a union: what
   the simulator *does* for that state (verb(s), new capability, or
   cost-only with meaning), as a complete ledger.
3. **Realisation and outcome semantics** — what makes a tactic-state
   succeed/fail against the substrate, how backward transitions read, and
   how "the attack succeeded" is derived (the D7 three-layer override),
   with the MTTC event definition for the 6-phase baseline explicitly
   unchanged.
4. **MTD-interruption policy** — what happens when a mutation fires
   mid-state; one policy recommended, alternatives named.
5. **Record contract** — what per-run records the bound attacker emits so
   the existing statistics pipeline computes MTTC/ASR from them, per class,
   non-degenerately.
6. **Determinism** — same timeline + seed → same records (SIM-05).
7. **Extension hooks, not designs** — where the per-action success-rate
   axis (R2), attacker styles (R3), and the two-way coupling attach later
   without redesign.

## The quality bar — four words, operationalised

- **Grounded.** Every element traces to something real: the substrate's
  actual code paths, the nets' actual contents, a registered supervisor
  ruling (D1–D10, R1–R5), or an extracted external source. The
  technique→CAPEC→CWE→CVE→synthetic-CVSS chain is positioned from what the
  published crosswalks *actually contain*, not from the assumption they are
  dense. No machinery justified only by plausibility.
- **Reasonable to achieve.** Implementable by one person on the existing
  codebase in a small number of sessions, sized honestly file-by-file
  against the D5 boundary; depends on nothing unbuilt (no detection, no
  two-way coupling, no corpus expansion); prefers the path that yields
  preliminary experiment-matrix results early. Pipeline-first, per the
  supervisor's standing MVP principle: get the work down; it need not be
  correct first time.
- **Defensible.** Reads as a dissertation design section: the space
  enumerated, alternatives killed for stated reasons, the trade-offs argued
  rather than averaged, every assumption labelled with its status (ruled /
  assumed / pending supervisor confirmation), comparability to the
  inherited baseline preserved and stated. It survives the examiner's "why
  this and not X?" because X is in the record with its cause of death.
- **Distinguishable — the non-negotiable core of appropriateness.** The
  recommended binding names, in advance, the substrate-observable
  behavioural differences it will produce between operational-objective
  classes and against the 6-phase baseline. A binding that is "simply a
  mapping onto the existing CKC-phased attacker" — however tidy — has been
  done before and yields no meaningful results. If no candidate passes this
  test honestly, *that finding, argued, is an acceptable outcome of the
  session* — a forced recommendation that fakes distinguishability is not.

## Hard digging is part of the goal

The design space must be built from the world as well as the repo: web
search, literature, existing frameworks and open codebases (adversary
emulation, security RL environments, attack-graph and model-driven
formalisms, the ATT&CK↔CVE crosswalk data itself), with
transfers/doesn't-transfer verdicts and extraction stubs for anything
load-bearing. At least one serious end-to-end candidate must be something
that appears in no existing repo document. A session that only rearranges
what the repo already says has not met this goal.

## Not part of this goal

Code. The R2 success-rate model and R3 style vectors (preserve hooks only).
Timing calibration (post-MVP per R1). Detection/IDS. Two-way coupling.
Anything requiring behavioural change to network/MTD/statistics paths or
the goldens.

## Done means

The investigation record + per-tactic ledger + one-page sign-off summary
exist and clear the brief's validation gate; Marc has reviewed them; the
recommendation is ready to put in front of Dr Hong, and the replay-attacker
handoff could be un-deferred against it the day it is confirmed.
