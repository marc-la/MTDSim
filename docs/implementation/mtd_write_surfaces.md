---
status: durable
created: 2026-08-02
updated: 2026-08-03
topic: "The defender write side — per-mechanism write-set enumeration for all eight MTD mechanisms, live-verified; the purview/fairness table for the reported family; answers to the boundary brief's shared questions"
---

# MTD write surfaces — what each mechanism moves when it fires, verified live

**Status:** the Part A deliverable of the network/defender boundary review
(brief 2 of 3, `docs/handoffs/2026-08-02_boundary_network_defender_integration.md`,
closed 2026-08-03 with all three dispositions ruled — the handoff lives in git
history; its confidence evaluation passed and Part B was empty).
Every write set below was enumerated by reading `mtd_operation()` and then
**verified by firing the mechanism once on a seeded `TimeNetwork`**
(seed 42, the experiments' default 50-node/5-endpoint/8-subnet/4-layer
geometry; one fresh network per mechanism so diffs are attributable) and
diffing the full mutable surface: per-host `ip` / `os_type` / `os_version` /
users / instance identity, per-service-node `port` / service id / vulnerability
`(id, exploited, exploit_attempt)` triples, network edges / node-id set /
`target_node` / `reachable` / `compromised_hosts`, and the three scorer feeds.
Read-side liveness verdicts are cross-filled from brief 1's coupling work (the
indistinguishability record and its repo-scope read searches), not re-derived
here.

## (a) Per-mechanism write sets — enumerated and live-verified

**Default reported family** (`mtd_scheme.py:22-31`): CompleteTopologyShuffle,
IPShuffle, OSDiversity, ServiceDiversity. Latent (commented out of the default
set; in no recorded experiment): HostTopologyShuffle, PortShuffle, UserShuffle,
OSDiversityAssignment. The scheduler always passes the adversary
(`mtd_operation.py:183`), so `adversary`-touching writes are reachable.

| Mechanism | Writes (locators) | Verified diff (seed 42) |
|---|---|---|
| **IPShuffle** | `host.ip` per non-endpoint host (`ipshuffle.py:17-22`); scorer ip-feed (`ipshuffle.py:25` → `scorer.current_hosts_ip`, the list holding only the 45 internal hosts' new IPs — endpoints omitted) | 45/45 internal `ip` moved; 0 endpoint writes; nothing else touched |
| **CompleteTopologyShuffle** | whole `network.graph` regenerated (`completetopologyshuffle.py:19` → `gen_graph`, network.py:101-288: fresh `nx.Graph`, plus `colour_map`, `pos`, `node_per_layer`; **re-selects `target_node` when `network_type == 0`**, network.py:210-212); host instances re-attached by node id (`completetopologyshuffle.py:20-21`); `reachable` rewritten (`:22` → `update_reachable_mtd`, network.py:694-727); scorer feeds (`:26-27, :38`) | all adjacency moved **including endpoint-incident edges** (8 → 5); node-id set unchanged; host instances, `ip`, `os`, services, ports all preserved; `net.compromised_hosts` `[7,8]` survives; `target_node` `None → None` (type-1 network) |
| **OSDiversity** | `host.os_type`/`os_version` per non-endpoint host, version **index** preserved (`osdiversity.py:22-29`); every non-target service node's `"service"` redrawn compatible with the new OS (`osdiversity.py:31-44`; guard inert per D-18 → always fires); scorer feeds (`:46-48`) | every internal host relabelled (31/45 change value — the draw includes the incumbent type); **331/331** non-target service nodes redrawn; version-index preservation verified on all 45; 0 endpoint writes; ports untouched |
| **ServiceDiversity** | every non-target service node's `"service"` on non-endpoint hosts redrawn at a random compatible service and version (`servicediversity.py:18-30`, post-D-05); scorer feeds (`:32-34`). Constructor's `shuffles=50` is dead state (`servicediversity.py:5-6`, read nowhere) | **331/331** non-target service nodes redrawn; 0 endpoint writes; ports, os, users, adjacency untouched |
| **PortShuffle** *(latent)* | every non-target service node's `"port"` on non-endpoint hosts (`portshuffle.py:16-29`) | 331/331 ports moved; services untouched; 0 endpoint writes |
| **UserShuffle** *(latent)* | `host.users` on **every** host — **no endpoint exemption** (`usershuffle.py:15-21`) | users moved on all 50 hosts including the 5 endpoints |
| **HostTopologyShuffle** *(latent)* | pairwise swap of host instances between node ids within a layer (`hosttopologyshuffle.py:44-50`), `host.host_id` swapped (`:46-47`); adversary id-keyed state remapped (`:57` → `adversary.py:28-60`); `reachable` rewritten (`:59`); scorer feeds (`:62-64`) | 44 instance swaps (22 pairs of 45 internal hosts; leftovers stay put); endpoints exempt; adjacency, ips-per-instance, services-per-instance unchanged (the *mapping* moves, not the contents) |
| **OSDiversityAssignment** *(latent)* | as OSDiversity (same exposed/target exemptions, same always-firing guard — it inherits D-18's always-replace behaviour, `osdiversityassignment.py:64-74`) with the OS drawn from the MIP result (arbitrary per D-17); **no derived/scorer refresh calls at all** | every internal host relabelled (30/45 change value); 331/331 services redrawn; no scorer entries |

Geometry caveat for CTS: `gen_graph` has a node floor that can exceed
`total_nodes` (the reconciliation comment at network.py:922-935 records the
crash class); at the default geometry the generator tops up to exactly
`total_nodes` (verified: node-id set unchanged across regeneration), so CTS's
re-attachment is total. A non-default geometry inside the floor band would
leave re-generated nodes with no `"host"` attribute — latent, recorded, not a
current-experiment concern.

## (b) The shared questions of the brief, answered with evidence

1. **The exposed-endpoint exemption is not universal, and where present it is
   endpoint-total.** IPShuffle, OSDiversity, ServiceDiversity, PortShuffle and
   OSDA skip the 5 exposed endpoints entirely (verified: zero endpoint writes).
   UserShuffle does **not** — it re-draws users on every host, which matches its
   own intent row (IS-MTD-03 "each host"). CompleteTopologyShuffle moves the
   endpoints' *adjacency* (endpoint-incident edges changed on firing) while
   preserving the endpoint hosts themselves. Net effect for the reported
   family: the attacker's entry hosts are immutable in ip/os/service/port
   space, but their position in the topology moves under CTS. Documented
   intent covers only IPShuffle ("all internal hosts", IS-MTD-01); for the
   application-layer mechanisms the exemption is beyond-paper (audit §l item
   5) → **D-23, ruled keep-and-document (Marc, 2026-08-03)**: the entry
   surface is deliberately fixed — attackers hold passive-reconnaissance
   access to exposed endpoints regardless, so the exemption grants the
   attacker its foothold and the evaluation's game is disrupting it at the
   discovery level, post-ingress. The exemption is now the documented model
   of the family.
2. **The target-node exemption is structural, not a skipped surface.** The
   target service node carries **no `"service"` and no `"port"` attribute at
   generation** (`host.py:116-127` skips it for both; verified live:
   `"service" in attrs == False`). There is nothing on the target node to
   diversify, and un-skipping it would `KeyError` (OSD reads the attr before
   replacing, `osdiversity.py:35`). The compromise-critical services are those
   *adjacent* to the target node (`host.py:415-426`), and those **are**
   redrawn. No disposition needed: the exemption mirrors the data model.
3. **Ports do not move when services do — and that conforms.** A redrawn
   service keeps its node's port (verified: 0 ports moved under SD/OSD; the
   direct check on a redrawn node shows the same port). Port assignment
   happens only at host generation (`host.py:121-123`) and in PortShuffle
   (`portshuffle.py:25-29`), which is latent. Consequence stated for the
   fairness table: the attacker's discovered ports remain valid addressing
   across every diversity firing — `get_services_from_ports`
   (`host.py:281-324`) keys service discovery by port number, so a service
   redraw changes *what is at* an address, never the address. No IS row
   couples ports to service replacement (IS-MTD-05 replaces services;
   IS-MTD-02 owns ports), so this is CONFORMS, recorded as a granularity
   fact rather than a gap.
4. **Derived state: the refreshes are metric feeds, and in the time-domain arm
   two of them are degenerate.** The attacker-visible derived structure is
   `network.reachable` (feeds `get_hacker_visible_graph`, network.py:952-966):
   only CTS and HTS rewrite it, and they are exactly the mechanisms that
   change what it derives from; the other six change no adjacency, so no
   mechanism leaves `reachable` stale. The remaining "refreshes" feed the
   scorer only: `add_attack_path_exposure` is gated to `network_type == 0`
   and never runs in the time-domain arm (verified: `network_type == 1`);
   `add_shortest_path` **does** run (CTS/OSD/SD/HTS) but with
   `target_node = None`, and `nx.shortest_path(graph, source, None)` returns
   a **dict of all shortest paths from that source** — so each firing appends
   a 50-entry paths-dict to `scorer.shortest_path_record` where a single path
   is expected (verified live for all four callers). Downstream,
   `shortest_path_variability` (`evaluation.py:180-181`) takes `len()` of
   these entries — reachable-node count, not path length — and
   `attack_path_exposure()` (network.py:630-664) iterates the dict as if it
   were a path. No recorded arm consumes the values (`get_metrics` is called
   once at `proceed_mtd`, `mtd_operation.py:60-65`, and its return value is
   discarded; the consumers at `mtd_ai_operation.py:305-331` /
   `mtd_ai_training.py:251-277` are the deferred Tay benchmark) → **D-24**.
   Attacker-side caches (`curr_ports`/`curr_vulns`) are not written by any
   mechanism; their invalidation is the interrupt channel — brief 3's
   purview. What this brief establishes is the object-identity half: a stale
   handle after a redraw points at an **orphaned** instance (see 5), so
   un-invalidated cache entries act on objects no longer attached to the
   network.
5. **A service redraw fully revokes the attacker's standing on that service.**
   `get_random_service` returns a fresh `Service` (new instance, new id)
   whose vulnerabilities are `copy()`s that preserve `id` but reset
   `exploited` and `exploit_attempt` (`services.py:54-83, 242-256, 355-369`).
   Verified live: after marking a vulnerability exploited and firing SD, the
   node's new service instance carries zero exploited flags, zero attempts,
   `is_exploited() == False` — and the ATK-04 per-instance re-exploit
   discount (`services.py:122-123`) is lost with the instance. What
   persists: `host.compromised` (never reversed — D-02, ruled operative) and
   `host.compromised_services` (append-only bookkeeping; readers: none
   beyond its own append at `host.py:421-422`, so stale ids there are
   inert). Prior exploitation **cannot** survive a redraw through shared-id
   copies.
6. **What the reported family can and cannot move.** Component-by-component,
   with the mover named:

   | Component | Mover in the reported family | Mover only in the latent pool |
   |---|---|---|
   | inter-host adjacency | CTS | HTS (mapping only) |
   | host ip | IPShuffle (dead **to the attacker** — brief 1; live to the NAV metric feed and the RL state, corrected 2026-08-02) | — |
   | host os label | OSD (dead surface — D-19) | OSDA |
   | service identity / vulnerability surface | SD, OSD (equal per D-18) | OSDA |
   | ports | **none** | PortShuffle |
   | users / credentials | **none** | UserShuffle |
   | host-internal service topology | **none** | **none** (no mechanism in the pool rewires `host.graph` edges; `gen_internal_network` runs once at construction, `host.py:537+`) |
   | exposed-endpoint membership | **none** (`network.exposed_endpoints` is fixed at `__init__`, network.py:51) | — |
   | node ids / host identity | **none** (ids persist under CTS) | HTS (swaps id↔instance mapping) |

   The reported family therefore has **two live write surfaces** — adjacency
   (CTS) and the service/vulnerability surface (SD = OSD against this
   attacker) — plus two dead ones (ip, os label). Ports, users, host-internal
   topology and the entry set are frozen for every recorded experiment. This
   is decision C's cardinality finding, one level up, now with the frozen
   complement enumerated.

## (c) The purview/fairness table (the brief's required end-state)

Per mechanism: what it moves, what it exempts, what it refreshes, and whether
each moved component is read by the attacker (liveness cross-filled from
brief 1; native FSM and movement arm share the verb cores, so outcome-channel
verdicts hold for both; time-channel entries note the S3-R decline).

| Mechanism | Components moved | Exemptions | Derived/scorer refresh | Liveness of each moved component |
|---|---|---|---|---|
| CompleteTopologyShuffle | all inter-host adjacency (incl. endpoint edges); `reachable` | none (holdings persist by design, D-02; node ids stable) | `update_reachable_mtd`; scorer: SAPV (degenerate, D-24), APE (type-0 only), ip-feed (all 50 old IPs) | **live** — adjacency read by SCAN_HOST/SCAN_NEIGHBOR via `get_hacker_visible_graph`/`get_neighbors` and by path-distance sorting (`attack_operation.py:250-303`) |
| IPShuffle | `host.ip` (45 internal) | exposed endpoints (documented, IS-MTD-01) | scorer ip-feed only (45 internal IPs — endpoints omitted, asymmetric with CTS's 50) | **dead to the attacker** — verified by projection diff: one firing changes *nothing* the six verbs can read. The cross-filled claim of "zero readers repo-wide" is **corrected 2026-08-02** — there are three, all defender-side (`completetopologyshuffle.py:35`; `mtd_ai_operation.py:308` and `mtd_ai_training.py:254`, computing Ho's **NAV**, IS-MET-04, into the RL state vector). The measured effect against the attacker arrives only via brief 3's interrupt channels, and that is **documented** behaviour under IS-INT-04's class-based recast rather than an integration shortfall — [`attacker_read_surface.md`](attacker_read_surface.md) §(f) finding 1 |
| OSDiversity | os label (45 internal); all 331 non-target services (D-18) | exposed endpoints (beyond-paper → D-23); target node (structural, §b2) | scorer: SAPV (degenerate, D-24), APE (type-0 only) | os label **dead** (success gate commented out, D-19; ×2.5 time term native-arm-only, declined under movement by S3-R); service redraw **live** (SCAN_PORT/EXPLOIT_VULN read services and vulns) |
| ServiceDiversity | all 331 non-target services (random service, random version, post-D-05) | exposed endpoints (beyond-paper → D-23); target node (structural) | scorer: SAPV (degenerate, D-24), APE (type-0 only) | **live** — services/vulns read by SCAN_PORT/EXPLOIT_VULN; revocation semantics per §b5; addressing (ports) deliberately unmoved (§b3) |
| PortShuffle *(latent)* | all 331 non-target ports | exposed endpoints; target node (structural — no port exists) | none | ports are the attacker's discovery key (`get_services_from_ports`) — would be live if ever in the default set |
| UserShuffle *(latent)* | users on all 50 hosts | **none** | none | users read by BRUTE_FORCE / credential reuse — would be live |
| HostTopologyShuffle *(latent)* | id↔instance mapping (22 pairs/firing); `host.host_id`; adversary id-keyed state | exposed endpoints; unpaired leftovers stay put (opportunistic pairing, `hosttopologyshuffle.py:39-43` — a delta on IS-MTD-04's "swap **all** hosts", latent) | `update_reachable_mtd`; scorer SAPV (degenerate) | node ids are the attacker's entire host-addressing space (brief 1) — would be live |
| OSDiversityAssignment *(latent)* | os label (MIP-arbitrary, D-17); all 331 services (inherits D-18) | exposed endpoints; target node | **none** (asymmetric with its sibling OSD) | as OSD |

**The fairness statement.** Any ranking claim over the reported family
compares: one mechanism that moves the attacker's path structure (CTS), one
that moves nothing the attacker reads (IPShuffle), and two that are a single
service-surface effect with and without a dead OS relabel (OSD/SD, D-18/D-19,
decision C). The exemption profile is uniform across the four (endpoints
exempt; holdings persist; ports/users/entry-set frozen), so within-family
comparisons are not confounded by differential exemptions — the asymmetries
that matter are the liveness ones already recorded, plus the scorer-feed
asymmetries (ip-feed contents, OSDA's missing refreshes) which no recorded
metric consumes.

## (d) Cross-examination against IS-MTD-01..09 (the §c procedure)

Verdict deltas found by this review — everything not listed matches the
audit's existing rows:

- **IS-MTD-01/-02/-03/-09** — existing verdicts stand; write sets verified as
  documented (03's no-exemption is *conformance* to "each host").
- **IS-MTD-04** (CONFORMS, stands) — one further latent delta recorded: the
  opportunistic pairing leaves unswapped leftovers (§c table), against the
  spec's "swap **all** hosts". Latent mechanism; row not re-classified.
- **IS-MTD-05** (row evidence stale) — the row still describes the pre-D-05
  latest-version behaviour; the fix landed 2026-07-29
  (`servicediversity.py:21-30` now draws random service at random version).
  Annotated in the audit this session.
- **IS-MTD-06** — D-18/D-19 consumed as inputs, not re-opened; the write-set
  verification adds the version-index-preservation confirmation and the
  structural reading of the target-node skip.
- **IS-MTD-07** (CONFORMS, stands) — "changing every involved host's
  connection status" is exactly what fires, endpoints included; holdings
  persistence is D-02's ruled reading, not a CTS defect. **New,
  documented-nowhere, latent:** `gen_graph` re-selects `target_node` on
  `network_type == 0` networks (network.py:210-212), so CTS on a targeted
  network silently moves the attacker's objective — no lineage paper says
  topology regeneration re-sites the target → **D-25**. Inert in every
  recorded experiment (time-domain arm is type 1).
- **IS-MTD-08** — D-17 stands; noted that OSDA also inherits the D-18
  always-replace guard and performs no derived refreshes.

## (e) Findings requiring disposition (opened in the audit's list)

**All three ruled 2026-08-03 (Marc), each as recommended:** D-23
keep-and-document (rationale in §b1 and the audit's ruling banner), D-24
record-only (repair deferred to the Tay RL-benchmark phase as a
precondition), D-25 record-only. Part B is therefore empty — no code or
golden moved — and the review brief closed with the rulings; the table below
stands as the record of the options as they were put.

| # | Finding | Options (costed) | Recommendation |
|---|---|---|---|
| D-23 | Exposed-endpoint exemption undocumented for the application-layer mechanisms (§b1) | **(a) Keep and document** — zero code risk; rationale available (entry surface fixed for external parties, per PortShuffle's own in-code comment; Zhang's "each involved host" is ambiguous). **(b) Remove the exemption** — mechanisms act on endpoints too; moves every golden (D-05 procedure); changes the family's semantics against every recorded run | (a) — the exemption is uniform across the family, so it cannot confound within-family rankings; it needs deciding, not changing |
| D-24 | SAPV/APE metric feeds degenerate in the time-domain arm (§b4): paths-dict recorded as "shortest path"; APE never runs; `shortest_path_variability` measures reachable-count | **(a) Record-only** — zero risk; no recorded consumer; annotate `metrics_semantics.md` when SAPV/APE are next claimed. **(b) Repair the feed** (guard `target_node is None`) — touches scorer only; goldens unaffected in the movement stream but the native CSVs would need checking; only worth it before the Tay-benchmark phase consumes these fields | (a) now; revisit as a precondition of the RL-benchmark phase, whose state vector reads these fields |
| D-25 | CTS re-selects `target_node` on type-0 networks (§d, IS-MTD-07) | **(a) Record-only** — latent (no recorded arm is type 0). **(b) Pin current behaviour or fix** — only meaningful if a targeted-network arm is ever run; fixing before classification would freeze an unclassified divergence | (a); becomes a real decision only if a type-0 arm enters the evaluation |

## (f) Verification method (for Part B's regression tests)

One firing per mechanism on a fresh seeded `TimeNetwork` (seed 42, default
geometry), full-surface snapshot/diff. The assertions Part B should pin, per
dispositioned repair: endpoint columns all-zero (exemption holds as
dispositioned), 331/331 service redraw counts (or the selective count under a
D-18(a) repair), port immobility under SD/OSD, revocation semantics of §b5
(new instance, flags reset), CTS node-id-set stability and holdings survival.
The verification script is session scratch (deliberately not committed —
pinning pre-disposition behaviour would freeze unclassified divergences, the
sibling brief's gate-5 reasoning); this section is its specification.
