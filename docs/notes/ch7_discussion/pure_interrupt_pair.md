---
status: durable
chapter: ch7_discussion
created: 2026-08-27
updated: 2026-08-27
---

# IP shuffle and port shuffle reach the attacker through the interrupt alone, so the pair prices what an interrupt is worth at each layer

## Position in the dissertation

A discussion-chapter reading of two rows of the evaluation. It explains why the
IP-shuffle and port-shuffle results should be read together as a measurement of
the interrupt channel by itself, one per layer, rather than as two mechanisms
that happened to perform weakly.

## The idea

Two of the seven defences in the restored pool change nothing the attacker
subsequently reads. That is a property of the simulator's attacker, not of the
defences as deployed systems, and it is worth stating exactly. The attacker
addresses hosts by their identity in the network graph, never by IP address, so
an IP shuffle rewrites forty-five addresses that no attacker step consults. The
attacker discovers services structurally rather than by searching a port space:
a port scan returns the current port numbers of the services it can already see
(the host's entry services, and services reachable through one it has already
exploited), and those numbers serve only as the key a later lookup matches on.
A port shuffle therefore makes the attacker's held port list stale for one step,
until the next scan returns the new numbers, and it hides nothing the attacker
could not re-see at once. Neither defence alters a service, a vulnerability, or
an exploit.

What both defences do reach is the interrupt. In this simulator, every defence
belongs to a resource class, and the class alone fixes how a firing disrupts the
attacker: a network-class firing interrupts the attacker and sends it back to
host discovery; an application-class firing interrupts it and sends it back to
port scanning; both charge the same time penalty. Within a class every mechanism
buys the identical interrupt, and the lineage prices disruption at no finer
grain than this (Zhang et al. 2023 for the class semantics; Brown et al. 2023
for the three interaction classes they extend). IP shuffle is network-class and
port shuffle is application-class. Each is thus a defence whose entire measured
effect is its class's interrupt, and the pair spans both classes. Read together,
the two rows answer a question the evaluation could not otherwise pose: what is
an interrupt worth, on its own, at the network layer and at the application
layer, once the surface it would ordinarily accompany is held fixed?

This is a reading Brown's own results already support. Brown et al. (2023)
report that IP shuffle and port shuffle generate more blocked actions than the
other techniques yet perform similarly or worse on attempts to compromise,
because a blocked attacker "simply needs to reconnect and then exploit the same
vulnerabilities", where diversity techniques present new vulnerabilities to
exploit. The mechanism named there is precisely the one recorded here: the
interrupt is real and counts as a block, and it is the whole of the effect. The
present evaluation carries the finding one step further by making the
separation explicit. Diversity mechanisms deliver an interrupt *and* a changed
surface; the shuffle pair delivers the interrupt alone. The difference between a
diversity row and the shuffle row of the same class is therefore an estimate of
what the surface change adds over the interrupt, and the shuffle rows are the
baseline that makes the estimate readable.

The concession comes with the strength. Port shuffle in the lineage is a pure
interrupt mechanism because the attacker's port discovery is free; a defender
who reads the row as evidence that port randomisation is worthless would be
reading a fact about the attacker model as a fact about the defence. The
alternative was considered and set aside. Making port discovery cost-bearing, so
that a shuffle wastes reconnaissance time, would price disruption per mechanism
rather than per class, would alter the attacker on both arms of the comparison,
and has no basis in any of the four lineage papers. It belongs to future work,
and the rows are reported under the class-level model with this limit stated.
The same holds for the entry services: the attacker always sees a host's
exposed services at their current ports, because exposed services are exposed
by definition, so the shuffle hides internal ports only. That is the model, and
it is Brown's.

## What this does not claim

It does not claim that IP or port shuffle would be ineffective against a real
adversary; the rows measure a simulated attacker whose discovery is free and
whose addressing is by graph identity. It does not claim the interrupt is
small: the shuffle rows report it, whatever its size. And it does not rank the
two interrupt classes against each other beyond what the rows show, since the
network-class interrupt also clears the attacker's current host and the
application-class interrupt does not, so the pair differs in restart depth as
well as in layer.

## Evidence and repo anchors

- The per-mechanism write sets and the port-shuffle liveness analysis (the
  structural discovery model, the stale-port channel, the interrupt channel,
  Marc's ruling of 2026-08-27):
  [`../../implementation/mtd_write_surfaces.md`](../../implementation/mtd_write_surfaces.md) §(a), §(c).
- Class-level pricing of disruption (D-20, ruled 2026-08-03) and the six
  channels: [`../../implementation/intent_conformance_audit.md`](../../implementation/intent_conformance_audit.md),
  [`../../implementation/boundary_attacker_defender_channels.md`](../../implementation/boundary_attacker_defender_channels.md).
- IP shuffle dead to the attacker's read surface (IS-MTD-01 extension):
  [`../../implementation/attacker_read_surface.md`](../../implementation/attacker_read_surface.md) §(f).
- Brown's design and finding: `docs/sources/lit_review/brown2023.md` §III-B(2)
  (line 87) and §V (line 168); extraction
  [`../../sources/extractions/brown2023.md`](../../sources/extractions/brown2023.md).
  The Zhang class-semantics citation is an anchor to reconcile against the
  extraction before drafting.
- Code: `mtdnetwork/component/host.py:281-351` (`get_services_from_ports`,
  `port_scan`), `mtdnetwork/mtd/portshuffle.py`, `mtdnetwork/mtd/ipshuffle.py`.
- Related note: [`state_bounds_measurable_disruption.md`](state_bounds_measurable_disruption.md)
  (the general form: a defence destroys only the state the attacker carries).
- Pool-restoration brief: retired 2026-08-30, `git show d127f443:docs/handoffs/2026-08-27_mtd_pool_restoration.md`.

## Revisit conditions

If port discovery were made cost-bearing, or disruption priced per mechanism
rather than per class, the shuffle rows would no longer isolate the interrupt
and this reading lapses. If the restored pool's evaluation shows the two
shuffle rows differing from their class's diversity rows by less than run
noise, the "surface change adds over the interrupt" estimate is null and the
note's second half should say so. If the attacker were changed to address
hosts by IP, IP shuffle would gain a second channel and leave the pair.
