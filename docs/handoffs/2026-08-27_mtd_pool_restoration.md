---
status: open                  # feasibility ruled in chat 2026-08-27; awaits Marc's two rulings, then an implementing session
created: 2026-08-27
---

# Restoring the MTD pool — bring the latent mechanisms to a working, faithful state

**Marc's direction (2026-08-27):** the evaluation is stronger with every
mechanism the lineage implemented in a working state, faithfully to the four
papers, so that "which mechanisms dominate, which lag, and is that stable
across the lineage's own conditions" is answered over the full pool rather
than Zhang's four. The pool is Brown's, *restored* rather than extended — no
novel defender (architecture.md decision stands).

Assessment source: the code as read this session (`hosttopologyshuffle.py`,
`usershuffle.py`, `portshuffle.py`, `adversary.py:106-`, `host.py:170-185,
281-324, 480-500`) and the standing records
([`../implementation/mtd_write_surfaces.md`](../implementation/mtd_write_surfaces.md) §(c),
[`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md) D-17/D-31/D-32).

## Verdict per mechanism

| Mechanism | Verdict | Work |
|---|---|---|
| HostTopologyShuffle | **fixed ✓ 2026-08-27** (D-31 closed; 9/9 write-surface tests; tracer-verified) | D-31: remap in place, not rebind; remap every id-keyed structure (`network.compromised_hosts`, `reachable`, scorer series, ip-feed) then `update_reachable_mtd`. Keep D-02: compromised hosts stay compromised; the foothold's new neighbours become reachable. Swap stays within a *level* (the `layer` node attribute is depth, Brown's "same network layer") — subnet-constraining not required. Interrupt: already network-class (D-20), nothing to wire |
| UserShuffle | **fixed ✓ 2026-08-27** (D-32 + D-26 repaired; R1 = same pool, R2 = endpoints exempt, both ruled) | D-32: reset `total_users` and `p_u_compromise` in `set_host_users`. Disruption is already implicit (brute-force and auto-compromise read `host.users`). Ruling R1 below on pool semantics; ruling R2 on endpoints |
| PortShuffle | **activated as-is — ruled 2026-08-27; hygiene fix applied ✓** (exemption keyed on the graph key, `portshuffle.py`; `tests/test_mtd_write_surfaces.py` 9 passed) | Live through the stale-`curr_ports` channel and the application-class interrupt only; entry services (`host.exposed_endpoints`) are auto-injected into every scan at their current port, so the shuffle hides internal service ports only — the model, not a defect. See "Port shuffle — what its row measures" below |
| OSDiversityAssignment | **withdrawn — ruled 2026-08-27, recorded** ✓ (D-17 c; ruling banner in the audit §n, marker in `mtd_write_surfaces.md` §(a)/(c), header comment in `osdiversityassignment.py`) | Solver broken (constraint 7 never written) and the idea is unpriced: OS choice affects no attacker outcome (D-18/D-19), and the DAP needs a server class the untargeted arm lacks. Record why; leave commented out |

Result: seven working mechanisms — the lineage four plus HTS, UserShuffle,
PortShuffle.

## Port shuffle — what its row measures (ch6 discussion material)

Marc's ruling (2026-08-27): PortShuffle is activated as-is. It is faithful to
Brown 2023 and its limits are Brown's design, to be carried into the
discussion, not fixed. The assessment, verified against the code:

- `Host.port_scan` (`host.py:326-351`) is not a port-space scan. It returns
  the *current* port numbers of the services the attacker can structurally
  see — the host's exposed services (`host.exposed_endpoints`, the
  service-graph entry nodes) plus services reachable through an
  already-exploited service. Discovery is structural; ports are only the key
  `get_services_from_ports` (`host.py:281-324`) matches on later, and that
  lookup re-injects the exposed services at their current ports.
- A firing therefore bites in one way only: `adversary.curr_ports` goes
  stale, so the EXPLOIT_VULN lookup finds fewer internal services (exposed
  services are never lost); and, being application-class, the firing
  interrupts the attacker and forces a SCAN_PORT, which returns the new
  ports and ends the effect. No service, vulnerability or exploit changes.
- This is Brown's design and Brown's finding. §III-B(2): "reassigning the
  ports … interrupting any attacker performing operations using an incorrect
  port number" (`docs/sources/lit_review/brown2023.md:87`). §V: IP and port
  shuffle "generate more blocks than the other techniques" yet perform
  "similarly or worse" on attempts-to-compromise, "because when the attacker
  is blocked, the attacker simply needs to reconnect and then exploit the
  same vulnerabilities" (`brown2023.md:168`). A pure interrupt mechanism.
- Consequence for the evaluation: PortShuffle's row measures the
  application-class interrupt channel alone (D-20 class-level pricing), as
  IPShuffle's row measures the network-class interrupt alone. The pairing is
  a ch6 discussion point, not a defect — note:
  [`../notes/ch6_discussion/pure_interrupt_pair.md`](../notes/ch6_discussion/pure_interrupt_pair.md).
- Ruled out: cost-bearing port discovery (a port-space search so that a
  shuffle wastes reconnaissance time) — beyond every lineage paper, changes
  the attacker on both arms, mechanism-level pricing against D-20. Future
  work at most.
- The auto-injection of entry-service ports into every scan is the model
  (exposed services are exposed by definition), not a defect.

Records: `mtd_write_surfaces.md` §(a)/(c) PortShuffle rows;
`intent_conformance_audit.md` IS-MTD-02 pointer.

## Rulings — all made 2026-08-27 (R1 (a) same pool; R2 family rule; D-26 (a) repair; golden streams kept and re-baselined, not retired)

- **R1 — UserShuffle pool semantics.** (a) *as coded / Brown*: redraw from the
  same `users_list`, so a harvested credential stays valid wherever that
  account re-seats (leaky rotation; realistic per Zhang–Monrose–Reiter).
  (b) draw fresh identities, invalidating harvested credentials — a different
  mechanism, documented nowhere. **Recommend (a), stated.**
- **R2 — UserShuffle endpoint exemption.** Brown says "each host"; the
  family's ruled model (D-23) exempts endpoints. **Recommend the family rule**,
  for uniform exemptions across the pool.

## Constraints on the implementing session — state 2026-08-27: 1 done (`MTDScheme.MTD_POOLS`, `pool=` kwarg through `MTDOperation`); 3 done (provenance.md rows); 4 done for HTS/User; 5 done by trace (per-mechanism, both arms — section below; a seeded disruption_wiring.md-style measurement is still owed before any ranking is published); golden root cause: ca6cd72c added two movement-record fields, schema-only drift

1. **Two named pools, not one widened default.** `random` / `alternative` /
   `simultaneous` draw from `_mtd_strategies`; widening it moves every
   lineage-arm golden and breaks ch5's family-1 re-runs. Keep the four as the
   `lineage` pool; add `full` (seven). Goldens for the four are untouched;
   new streams are baselined for the additions only (`baseline/CHANGELOG.md`,
   SIM-05).
2. **The reactive selector stays at five actions** (Tay's 5-unit output);
   the added mechanisms are outside its action space by construction. The
   reactive arm compares against the lineage pool; say so in ch4.
3. **Declare the undocumented parameters.** `MTD_DURATION` for HTS / Port /
   User (100 / 70 / 20 s) and `MTD_PRIORITY` for all seven exist in code but
   no paper documents them (IS-TIM-03, IS-SCH-06). Each becomes a declared
   value with a provenance row.
4. **Regression tests** extend `tests/test_mtd_write_surfaces.py`: per
   mechanism, the write set, the exemption profile, and (HTS) that
   `network.compromised_hosts is adversary._compromised_hosts` survives a
   firing and `reachable` contains the swapped foothold's new neighbours.
5. **Verify with the tracer** (`python -m mtdnetwork.trace`;
   `PYTHONPATH=src python -m mtdsim.l3_simulation.trace`) on both arms — the
   interrupt classes must reach the movement attacker as they do the native
   one (disruption_wiring.md §(a) per-mechanism measurement, extended to the
   three).

## Traced verification — every mechanism, both arms (2026-08-27)

Run with the extended tracers (measured write sets on every MUTATION line;
`docs/implementation/trace_tool.md` extension log). Substrate arm:
`python -m mtdnetwork.trace --scheme single --mtd <M> --seed 42 --finish-time 3000`;
movement arm: `PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate
--mapping v2_partial --scheme single --mtd <M> --seed 0 --horizon 4000`.
Control (substrate, seed 42): foothold t=961, 7/50 owned.

| Mechanism | Per firing wrote (measured, both arms) | Explicit disruption (interrupt) | Implicit disruption (state the attacker reads) | Level | Verdict |
|---|---|---|---|---|---|
| IPShuffle | 45 IPs; 0 endpoint writes | network class: 15/15 firings caught the native attacker, position lost every time; movement arm 20 interrupts (3 mid-verb, 17 mid-dwell) | none — scanned ports never stale, target never moved; the IP is read by no verb | host layer (address) | as documented: pure network-class interrupt |
| CompleteTopologyShuffle | 83–134 edges rewired; node ids stable; 0 endpoint *host* writes (endpoint adjacency moves, by design) | as IPShuffle (15/15; movement 20) | visible set changes (5→6); paths re-sorted; foothold kept (owned n→n every firing) | host layer (adjacency) | as documented |
| **HostTopologyShuffle** (D-31 repaired) | 42–44 hosts swapped position; 0 endpoint writes; **compromised set intact and network/adversary lists agree on every firing** | as IPShuffle (15/15; movement 20) | **12/15 firings swapped the attacker's target host away and invalidated all its scanned ports**; visible set moves (6→5 once — a foothold left the visible subgraph, the CTS-like consequence flagged) | host layer (id↔instance) | **working, faithful** (IS-MTD-04 + D-02) |
| **PortShuffle** (activated) | 320–331 ports; services untouched; 0 endpoint writes | application class: 14/15 caught natively, none cost position; movement 16 (1 mid-verb, 15 mid-dwell) — identical to OSD/SD, i.e. D-20 class pricing exactly | **scanned ports in hand go stale on every firing that finds the attacker holding any (12/15)** — the one channel Brown designed; entry ports never lost | service layer (addressing) | working, as Brown: a pure interrupt plus a re-scan |
| **UserShuffle** (D-32/D-26 repaired, R2) | 45 hosts' user sets; 0 endpoint writes (was 50, pre-R2) | reserve class, mid-BRUTE_FORCE only (IS-INT-03): native 1/15 at seed 42, 1–6 across seeds 1–6; movement arm 0 in 4000 t/u (the walker rarely sits on BRUTE_FORCE) | credential reuse and brute force read `host.users` live; seed sweep 1–6 vs unopposed: owned 25→23, 20→15, 22→21, 13→14, 17→16, 23→21 — small, consistent with D-26's measured near-nil brute-force route | credential (Brown's third interaction class) | working, faithful; its effect is mostly implicit and small by the model's design |
| OSDiversity | 32–36 OS relabels + all 331 services (D-18: every service, not "incompatible" ones); 0 endpoint writes | application class (15/15 native; movement 16) | ports never stale (ports untouched, by design); services redrawn are what SCAN_PORT/EXPLOIT read | service layer | as documented; ServiceDiversity plus a dead relabel |
| ServiceDiversity | 331 services; 0 endpoint writes | as OSDiversity | as OSDiversity | service layer | as documented |

**Integration reading.** All seven fire through the existing `MTDScheme` →
`MTDOperation` → `_interrupt_adversary` path; the three restored mechanisms
enter it under the resource class they already carried (`network` /
`application` / `reserve`) and get exactly the class-level interrupt every
sibling gets (D-20) — the movement-arm interrupt counts are identical within
each class. No new disruption path was built. Exposed endpoints are untouched
by all seven; the compromised set survives every firing of every mechanism.

**Rulings this produced, none new:** HTS's foothold-leaves-visibility case is
the substrate's visibility model (CTS has it too) and should be stated in
ch2/ch4; UserShuffle's explicit channel is rare by design (IS-INT-03) and its
row will read as an implicit-only mechanism against the movement attacker.

## OS diversity made distinct — ruled 2026-08-27 (Marc: "implement recommendation one")

**Why.** Traced, OS diversity was service diversity plus a dead relabel: the
compatibility guard was inert (D-18: every service redrawn) and the OS label
decided nothing (D-19: the success gate commented out; the ×2.5 time term is
native-arm-only and the movement arm declines it under S3-R). The diversity
axis was therefore priced only through the service population, never through
the OS — while Brown §III-B(6) defines OS diversity as "avoiding any
OS-specific exploits", an exploit-applicability channel. Marc's reading: the
OS label should be encoded into the attack operation's success, so that moving
the OS disrupts the attacker implicitly; the commented-out gate is that link.

**Ruling — option 1, both parts, because the gate alone does not separate the
pair** (both mechanisms redraw every service, so the filter acts on a fresh set
either way):
- **D-19 → reinstate** the gate in `Vulnerability.network`: an OS-dependent
  vulnerability returns 0.0 on a host whose OS is not in its list. Reclassified
  from "abandoned alternative" to documented intent on Brown's sentence. Design
  detail ruled on recommendation: the refused attempt **counts** as a failed
  attempt (so a host whose vulns are all OS-gated cannot absorb attempts for
  free) and **draws no RNG**.
- **D-18 → repair** `service_is_compatible_with_os` (name-based membership), so
  OS diversity redraws only the services made incompatible by the new OS; the
  vulnerabilities the attacker already knew on surviving services stop working
  because the OS moved under them. Zhang §4.3.1.4's stated behaviour.

**Expected effect, pre-registered:** OSD separates from SD (a partial redraw
plus an applicability shift vs a full redraw); the diversity family as a whole
gets harder for the attacker (~40 % of vulnerabilities carry an OS list —
cross-platform services × 0.8). Both arms move by design; every golden
re-baselines (SIM-05, changelog). Comparability: the family sub-study of
2026-08-02 and experiment 2's diversity numbers predate this and are not
comparable to post-ruling runs — ch4 carries one sentence.

**Generality check owed:** nothing may hard-code the OS count — the OS list
sample and the diversity draw must derive from `constants.OS_TYPES` (Marc:
"what if I wanted 10 OS types").

**Tracer:** an `EXPLOIT REFUSED` attacker event and an `exploits_refused_by_os`
tally, so the channel is visible in the log.

**Implemented and measured (agent report, 2026-08-27).** Full suite 899 passed.
Gate reinstated (`services.py`, refused attempt counts, no RNG); guard repaired
by service-name membership (600/600 True live; OSD now redraws e.g. 49/331 at
seed 43, 4/331 at seed 42, all survivors compatible, all redraws incompatible).
No hard-coded OS count anywhere (every draw derives from `constants.OS_TYPES`;
one pre-existing assumption: `OS_VERSION_DICT` entries must have equal length
for version-index preservation). Both golden sets re-captured (9/9 native,
69/69 movement), changelog entry written, five headline tests re-pinned.

Measured separation — movement goldens, compromised hosts summed over configs,
old → new: OSDiversity 24 → 33, ServiceDiversity 47 → 36 (mtd_executions
unchanged everywhere). Substrate seed 42: OSD 2/50 owned, 161 refusals, 4/331
services per firing; SD 5/50, 98 refusals, 331/331. **The pair now separates,
and in the direction pre-registered only for SD** — OSD got *easier* for the
attacker (24 → 33) because it redraws far fewer services; the diversity family
as a whole did not uniformly harden. Refusals fire in the no-MTD control too
(vulnerabilities carry OS lists from generation), so every scenario moved:
native no-MTD HCR 0.82 → 0.68, single-ipshuffle 0.64 → 0.18, single-osdiversity
0.06 → 0.38. This is the pre-registered expectation half-confirmed; the family
sub-study needs re-running before any diversity ranking is quoted.

**Two decisions no paper documents — both ruled by Marc the same day:**
(1) compatibility is the **(name, version) pair** (the version is implicit in
the service identity; the name-only reading under-stated incompatibility) —
applied, OSD/OSDA goldens re-captured a second time; (2) the refused attempt
**does** feed the native per-host give-up threshold, so OS-gated hosts are
abandoned faster — confirmed as implemented.

**Reading the separation, plainly (Marc's question).** OSD did not get weaker
than SD: 33 vs 36 compromised against a no-MTD 58. It lost part of its former
lead (24 vs 47) because the guard repair turned it from a total service reset
(the bug: 331/331 redrawn) into the faithful partial reset (4–49/331) plus an
applicability shift; the interrupt is unchanged. SD did not change — the
terrain did: the gate reads OS lists that every vulnerability has carried since
generation, so refusals fire with or without a defence, and every baseline
moved (no-MTD HCR 0.82 → 0.68).

**Records touched 2026-08-27 (main session):** audit (D-18/D-19 rows, IS-MTD-06,
§l item 1, the 2026-08-02 section header, D-17 banner note),
`mtd_write_surfaces.md` (§(b) table, OSD row, fairness statement, §(d)),
`attacker_read_surface.md` (os_type row, §(f) finding), `disruption_wiring.md`
(headline caveat), `boundary_attacker_defender_channels.md` (lever note),
`provenance.md` (two rows). The code, tests, goldens and changelog are the
implementing agent's; its report lands here on completion.

## Consequences for the documents

- **ch2 §2.2.2:** the roster becomes seven with a one-clause note that the
  DAP variant is withdrawn; the layer-landing reading gains a third landing —
  UserShuffle rewrites credentials (Brown's third interaction class), neither
  host nor service layer. Do not draft until the pool is landed.
- **Figure 2.1:** roster box gains three entries; the defence→network arrows
  gain the credential landing. Regenerate via `tools/mtdsim_model_figure.py`.
- **Table 2.1:** Brown's row's *what this thesis inherits* widens to the
  full pool.
- **ch6:** the IP-shuffle / port-shuffle pair isolates the two interrupt
  classes — each mechanism reaches the attacker through its class's interrupt
  channel and nothing else (IPShuffle network-class, PortShuffle
  application-class), so their rows read as the price of the interrupt
  channel alone, against Brown's own §V reading. Note staged in
  `notes/ch6_discussion/pure_interrupt_pair.md`.
- **ch4:** the comparability boundary gains a sentence — family-1 re-runs use
  the lineage pool; the fresh evaluation uses the full pool.
- **Records to update on landing:** `mtd_write_surfaces.md` §(a)/(c) (move
  three rows from latent to reported), `intent_conformance_audit.md`
  (D-17 ruled — **done 2026-08-27**; D-31/D-32 closed), `provenance.md` (the declared values).

## Out of scope

Retraining or widening the selector (V3); any mechanism not in Brown/Zhang;
mechanism-level pricing of disruption (D-20 stands).
