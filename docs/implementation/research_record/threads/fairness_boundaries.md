# The fairness/boundary programme — "a fair contest" (pointer-collapsed)

**Span:** 2026-07-22 → 2026-08-05. **Prompts:** #31, #63, #68. Fully recorded:
[`../../attacker_read_surface.md`](../../attacker_read_surface.md),
[`../../mtd_write_surfaces.md`](../../mtd_write_surfaces.md),
[`../../boundary_attacker_defender_channels.md`](../../boundary_attacker_defender_channels.md),
[`../../disruption_wiring.md`](../../disruption_wiring.md).

Only the motivation and one early question are unrecorded. The programme's
charter (#63, 2026-08-02) was evaluative fairness, in Marc's words: "all of MTD
mechanism comparative evaluation comes from the well-oiled MTDSim integration
here … not all MTD mechanisms are implemented in a way that the attacker
interacts with … the MTD mechanisms should be fairly implemented **for a fair
contest**" — three seams (network/attacker, network/defender,
attacker/defender), each audited in its own session, design and implementation
split A/B, iterated to a 95 % confidence gate. The suspicion that seeded it (OS
diversity as a late addition never properly integrated with the attack
operation) is also #63's.

The earlier question (#31, 2026-07-22) — should the defender manipulate attacker
state *directly*, or only via the network state? — prefigures the six-channel
survey's whole taxonomy. And the closure (#68, 2026-08-05) records the
disruption-uniformity resolution in paraphrase of the 4-Aug discussion: the
defence does not need to know which attacker it is disrupting; position-based
disruption generalises; what needed *checking* was whether each mechanism's
disruption actually arrives at the movement arm — which is exactly what
`disruption_wiring.md` then measured.

**Negative space:** none abandoned; the programme ran to completion and retired
its own handoffs. It is this record's cleanest example of the audit-then-build
pattern applied to inherited machinery rather than to new mechanisms.
