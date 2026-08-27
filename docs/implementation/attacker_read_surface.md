---
status: durable
created: 2026-08-02
updated: 2026-08-03
topic: "The attacker read side — every mutable network component censused against the six verbs by instrumented run, both driving modes, with expression channel and movement-driving reach; the verb-by-verb phase review; and the finding that IP Shuffle's invisibility to the attacker is documented behaviour rather than an integration artefact"
---

# The attacker read surface — what the substrate attacker perceives, verified by running it

**Status:** the Part A deliverable of the network/attacker boundary review
(brief 1 of 3 of the boundary programme, **retired 2026-08-05** — this file is
the surviving record; the open dispositions live in the audit's list).
It owns the **read side** of the coupling matrix; the write side is
[`mtd_write_surfaces.md`](mtd_write_surfaces.md) (brief 2, landed the same day),
whose mover columns are cross-filled here rather than re-derived. Couplings that
reach the attacker without passing through network state — the interrupt penalty,
the host-cursor clear — are brief 3's and are named here only where a verdict
depends on them.

**The object under review is the substrate attacker**, the six-verb operation in
`mtdnetwork/operation/attack_operation.py`. The movement layer is not a second
attacker: it drives the same verb cores through `step()`, so every read verdict
below is a property of the shared cores. What differs between the two driving
modes is *pricing*, not perception — the movement driver supplies its own
durations and passes `charge_time=False` (`attack_operation.py:746-747`,
docstring at `:445-454`, S3-R), so a coupling that expresses only through the
substrate's own time model does not reach movement-driven runs. Every row below
therefore carries an **expression channel** (outcome / time / signal) and its
**reach under movement driving**.

## (a) Method — the census, and why it is a run and not a grep

Read-side claims in this programme have so far been made by repository search.
Search establishes that a symbol is absent; it cannot establish that a live code
path is never taken, and it mis-reports a component that is read through three
levels of helper. Both failure modes matter here, and one of them has already
produced a wrong claim on record (§(e)).

Each component was therefore instrumented with a **read-only counter** and the
simulation was run. Plain instance attributes (`host.ip`, `host.os_type`,
`host.os_version`, `Service.name`, `Service.version`) were replaced with counting
properties that record the calling frame and delegate unchanged; method-level
surfaces (`port_scan`, `get_vulns`, `can_auto_compromise_with_users`,
`compromise_with_users`, `discover_neighbors`, `get_hacker_visible_graph`,
`get_path_from_exposed`, `sort_by_distance_from_exposed_and_pivot_host`,
`get_neighbors`, `Vulnerability.network`, `Vulnerability.exploit_time`) were
wrapped the same way. The instrumentation draws no randomness and writes no
simulator state, per the tracer's own contract
([`trace_tool.md`](trace_tool.md) § design invariants), so a censused run is the
run it censuses.

Two arms were censused, both defended with the full reported family:

- **native FSM** — `run_trace(scheme="simultaneous", seed=1234, finish_time=3000)`;
- **movement arm** — `run_movement("aggregate", seed=0, mtd_scheme="simultaneous", mtd_interval=200, mapping_version="v2_partial", retrace_sinks=True)`, experiment 2's configuration.

Four further probes supplied the run-level demonstrations gate (ii) requires:
a **projection diff** (the whole attacker-readable state before and after one
firing of each mechanism, §(b)); a **compromise-route census** over 60 runs
(§(c) BRUTE_FORCE, §(f) finding 2); and a **counterfactual measurement** of what
a repaired compatibility guard would replace (§(g)).

## (b) The coupling matrix

Rows are the mutable network components. **Read-by** names the verb and the
locator at which the read happens. **Channel** is how the coupling expresses:
*outcome* (it changes success/failure, discovery, or compromise state), *time*
(it changes only the substrate's pricing of an attempt), *signal* (brief 3).
**Movement reach** is *automatic* where the coupling rides the shared verb cores,
*declined* where it rides substrate pricing. **Mover** is cross-filled from
brief 2 §(a). Counts are from the census runs above; `native` / `driven` are the
two arms.

| Component | Read by (locator) | Channel | Movement reach | Mover (reported family) | Verdict |
|---|---|---|---|---|---|
| **inter-host adjacency / neighbour sets** | SCAN_HOST (`attack_operation.py:280`), SCAN_NEIGHBOR (`:581` → `host.py:428-436`), pivot selection (`:605`) | outcome | automatic | CompleteTopologyShuffle | **LIVE** — `get_neighbors` 29 native / 41 driven; `discover_neighbors` 8 / 12 |
| **`network.reachable` → hacker-visible graph** | SCAN_HOST (`:268` → `network.py:952-966`), ENUM_HOST distance sort (`network.py:882`) | outcome | automatic | CompleteTopologyShuffle (`update_reachable_mtd`) | **LIVE** — 39 native / 55 driven |
| **path-from-exposed distances** | SCAN_HOST reachability filter and ordering (`:285`, `:292`), ENUM_HOST (`network.py:855`) | outcome | automatic | CompleteTopologyShuffle (implicitly, via adjacency) | **LIVE** — 250 native / 63 driven |
| **exposed-endpoint set** | SCAN_HOST (`:283`, `:295-299`), all path queries (`network.py:832`) | outcome | automatic | **none** — fixed at `network.py:51` | **LIVE but immobile.** Sharpened: the endpoints are exactly what SCAN_HOST *unconditionally* appends to the stack (`:295-299`), and every mechanism in the pool either exempts them (IPShuffle, OSDiversity, ServiceDiversity — D-23) or preserves them by construction (CTS), so the attacker's guaranteed re-entry path is untouched by the whole reported family |
| **node ids / host identity** | every verb; the attacker's entire addressing space | outcome | automatic | **none** in the reported family (ids persist under CTS); HostTopologyShuffle latent | **LIVE but immobile** |
| **the host's pooled vulnerability stack** (incl. `exploited`, `exploit_attempt`) | EXPLOIT_VULN (`:141`, `:732` → `host.py:353-389`), SCAN_PORT traversal (`host.py:326-351`) | outcome | automatic | OSDiversity, ServiceDiversity (equal — D-18) | **LIVE, with two bounds** — `get_vulns` 20 native / 4 driven; `vuln.network` 225 / 37. **(i)** the coupling unit is the *host's pooled RoA stack*, not the per-service set: `get_vulns` pools every discovered service's vulnerabilities and then applies `can_exploit_with_dependent_vuln` against the whole pool (`host.py:376-382` → `services.py:99-104`), so replacing service A can gate or ungate a vulnerability on untouched service B (33 of 112 gated vulnerabilities dropped by the test, seed 42, all 50 hosts). **(ii)** the reset only bites on hosts **not yet compromised** — `host.compromised` is never reversed (D-02, ruled operative) and `_do_enum_host` reads it directly (`:376`), so a diversity firing that clears every `exploited` flag on an already-owned host does not un-own it |
| **ports** | SCAN_PORT (`:404` → `host.py:326-351`), service discovery key (`host.py:281-324`) | outcome | automatic | **none** — `setup_network` runs once per host at generation (50 calls, both arms); PortShuffle latent | **LIVE but immobile** |
| **users / credentials** | SCAN_PORT phase 1 (`:405` → `host.py:143-161`), BRUTE_FORCE (`:544` → `host.py:166-182`), harvest on compromise (`:630`) | outcome | automatic | **none** — UserShuffle latent | **LIVE but immobile** — see §(f) finding 2 |
| **`host.os_type`** | **success path: never** *(until 2026-08-27 — gate reinstated by ruling D-19; the row below is the pre-repair reading)* — the gate is inherited commented-out code (`services.py:146-148`, D-19). Only live read is the ×2.5 mismatch multiplier (`services.py:116-117`, IS-TIM-06 beyond-paper) | **time** | **declined** — 159 reads native, **0 driven** | OSDiversity | **DEAD to outcome; time-only, native-arm only** |
| **`host.os_version`** | **nothing on any attacker path, in either arm.** The ×2.5 term reads `os_type` alone | — | — | OSDiversity | **DEAD** — reads only from host generation, OSDiversity/ServiceDiversity's own draw, and the scorer |
| **`host.ip`** | **nothing on any attacker path, in either arm.** Readers are all defender-side: `completetopologyshuffle.py:35`, and the NAV metric feed at `mtd_ai_operation.py:308` / `mtd_ai_training.py:254` | — (attacker); metric (defender) | — | IPShuffle | **DEAD to the attacker — and that is documented behaviour**, §(f) finding 1 |
| **service identity (`Service.name`, `.version`)** | **nothing attacker-facing.** Reads are `services.py:copy` only (3 723 native / 24 672 driven); `Service.__eq__` was never called in either run | — | — | OSDiversity, ServiceDiversity | **DEAD** — diversity reaches the attacker *only* through the vulnerability set the replacement instance carries |
| **`network.tags` / `tag_priority` / `get_host_id_priority`** | nothing — `get_host_id_priority` (`network.py:759-779`) has no caller | — | — | none | **DEAD and immobile** — no ranking consequence |
| **`target_node`** | ENUM_HOST give-up guard (`:359-360`), gated on `network_type == 0` | outcome | automatic | none in the reported family (CTS re-sites it on type-0 — D-25, latent) | **UNREACHABLE** — every recorded arm is `network_type == 1`, so `target_node is None` |
| **host-internal service graph** | SCAN_PORT traversal, `check_compromised` adjacency-to-target (`host.py:415-426`) | outcome | automatic | **none** — `gen_internal_network` runs once at construction | **LIVE but immobile** |

**Every cell carries a locator and a verdict; every LIVE verdict carries a
run-level count from both arms.** No cell was filled from paper memory or from a
prior audit.

## (c) Run-level demonstration — the projection diff

The counts above show a component is *read*. What gate (ii) additionally needs is
that a mechanism's write *changes what the attacker would read*. The whole
attacker-readable projection — edges, node set, exposed set, `reachable`, and per
host the ports, vulnerability-id sets, exploited-service flags, users and
neighbours — was captured before and after one firing of each mechanism on a
fresh seeded network (seed 7, the experiments' geometry), with in-host exploit
progress seeded first so there was standing for a mechanism to revoke.

| Mechanism | Network-level fields changed | Hosts: ports | vuln set | exploit progress lost | users | neighbours |
|---|---|---|---|---|---|---|
| CompleteTopologyShuffle | `edges`, `reachable` | 0 | 0 | 0 | 0 | **50** |
| IPShuffle | **none** | 0 | 0 | 0 | 0 | 0 |
| OSDiversity | none | 0 | **45** | **5** | 0 | 0 |
| ServiceDiversity | none | 0 | **45** | **5** | 0 | 0 |

Three results, all of them load-bearing:

1. **IPShuffle changes nothing in the attacker's readable projection — not one
   field.** This is the strongest available form of the brief's §1.4 claim: not
   "no reader was found by search" but "the entire perceptual surface is
   bit-identical across the firing".
2. **OSDiversity and ServiceDiversity produce identical signatures** — the same
   45 hosts, the same 331 service nodes, the same revocation of standing. They
   are not merely statistically indistinguishable in the recorded data; they are
   indistinguishable *in what they present to the attacker*, before any run
   statistics are computed. (They are not bit-identical runs: OSDiversity
   consumes extra draws for the relabel, which is why the recorded means differ
   in the third significant figure while the blocked fractions agree to three
   decimal places.)
3. **CompleteTopologyShuffle is the only reported mechanism that moves the
   attacker's path structure**, and it moves every host's neighbour set.

A robustness check ran alongside: 75 consecutive CompleteTopologyShuffle firings
(a 15 ks run at the 200 s interval) held the node count at 50 throughout with
zero nodes left without a `host` attribute, so the host-reattachment the
mechanism relies on (`completetopologyshuffle.py:20-21`) does not degrade. Clean
negative, recorded so it is not re-checked.

## (d) The verb-by-verb attack-phase review

Marc's explicit ask: for each verb, what network state it *should* plausibly
consult for the interaction to be realistic, what it does consult, and the §c
classification of any gap.

| Verb | Consults | Should plausibly consult | Gap | §c verdict |
|---|---|---|---|---|
| **SCAN_HOST** | visible graph, compromised-host adjacency, path-from-exposed distances, exposed endpoints, `stop_attack` (`:250-303`) | the same — host discovery is a topology operation in every lineage paper | none. IS-PRC-01's "internal hosts visible only if a path exists through a compromised or exposed host" is implemented exactly, by the visible-graph subgraph plus the path test at `:285` | **CONFORMS** |
| **ENUM_HOST** | host stack, distance-and-pivot sort, per-host attempt counter, give-up list, `target_node` (dead branch) | the same. Brown Fig 3 box 2 prioritises proximity to the foothold (IS-SCN-02 as corrected by the recovered figure), which is what `sort_by_distance_from_exposed_and_pivot_host` computes | none | **CONFORMS** |
| **SCAN_PORT** | ports via the exploited-service traversal, the services at those ports, host users vs compromised users (`:404-405`) | the same — IS-PRC-02 (exposed services, plus internal services adjacent to an already-compromised service) and IS-PRC-03 (credential stuffing first) | none | **CONFORMS** |
| **EXPLOIT_VULN** | the globally RoA-ordered top-5 unexploited vulnerabilities, `complexity` (`:457-515`); receives the host and ignores it | IS-PRC-04's RoA priority stack over **all** scanned services — implemented since D-10 | the host's OS is passed and unread (`services.py:146-148`) | **the RoA behaviour CONFORMS**; the OS gate is covered by **no IS-ID at all** and is already open as **D-19** — consumed, not re-litigated |
| **BRUTE_FORCE** | host users ∩ compromised users, and `host.total_users` as the divisor (`host.py:166-182`) | IS-PRC-06: brute-force a login from harvested credentials, time-limited. No lineage paper gives the probability formula | `total_users` is **not the number of accounts on the host** — §(f) finding 3 | **DIVERGES-DOCUMENTED-NOWHERE** (candidate) → **D-26** |
| **SCAN_NEIGHBOR** | the current host's neighbours, filtered by `stop_attack` (`:579-589`) | IS-PRC-05: on compromise, assume C2 — connected hosts and services become visible | none | **CONFORMS** |

**The structural verdict (IS-PRC-08, "no off-flowchart behaviour").** The verb
set consults topology, services-and-vulnerabilities, and credentials. It consults
no host *label* — not IP, not OS type, not OS version, not service name or
version. That is the single sentence that characterises this boundary, and §(f)
establishes that it is very largely the documented design rather than an
integration shortfall.

## (e) The OS-layer question, answered

The brief asked that "was it ever intended to be read?" be treated as an open
classification question rather than a presumed regression. The answer, from the
intent spec by IS-ID rather than from paper memory:

- **No lineage paper documents OS-gated exploitation success.** The intent spec
  contains no OS-dependent-exploitation row; OS-dependent vulnerabilities are
  beyond-paper throughout (audit §l item 1), and IS-TIM-06 records the ×2.5 time
  term as a beyond-paper addition. This is D-19's finding and it stands.
  *Reclassified 2026-08-27 (Marc): Brown §III-B(6) — OS diversity "avoiding any
  OS-specific exploits" — is read as documenting the success channel; the gate is
  reinstated. The read is live from that date.*
- **The OS's *only* documented channel to the attacker is IS-MTD-06's service
  selection** — "services **incompatible with the new OS** are also randomly
  changed". The OS is meant to decide *which services exist on the host*
  (IS-NET-04: "the OS decides which services can be found on the host"), and the
  attacker then meets the OS only through the service and vulnerability surface.
- So the honest classification is **not** that OS integration regressed. The OS
  was never wired to exploitation success in any lineage; it was wired to the
  service catalogue. What is broken is that one documented wire — the
  compatibility guard — and that is D-18, already open.

**This changes the cost/benefit of the open D-18 decision, and §(g) quantifies
it.** The brief's framing was that OS Diversity's relabel "reaches the attacker
through nothing". Correct today; but the reason is D-18, not an absent design.

## (f) Findings

### Finding 1 — IP Shuffle's invisibility to the attacker is documented behaviour, not an integration artefact. *(Partial inversion of the programme's premise for this pair.)*

The programme opened on the reading that both unseparated pairs in experiment 2
are "integration artefacts, not defence facts". For `(os_diversity,
service_diversity)` that reading survives — D-18 is a broken documented wire. For
`(complete_topology, ip_shuffle)` the evidence does not support it, on three
grounds:

1. **`host.ip` is not an unread vestige. It has a documented consumer.** It feeds
   `ip_variability` at `mtd_ai_operation.py:305-322` and `mtd_ai_training.py:251`,
   which is Ho's **NAV** — "address changes normalised by state size, ∈ [0, 1]"
   (IS-MET-04) — and enters the RL defender's state vector at
   `mtd_ai_operation.py:436`. The IP surface exists to be *measured*, and to be
   *observed by the defender*, not to be read by the attacker.
2. **No lineage paper gives the attacker an IP-addressing model.** The only text
   that predicates anything on the attacker holding an IP is Brown's IS-MTD-01
   ("interrupts any attacker operating with a stale IP"). Zhang explicitly
   documents the recast — IS-MTD-09 classes techniques by resource layer, and
   IS-INT-04 states that network-layer MTD "makes the attack event fail
   immediately … adversary blocked from connecting", with no staleness predicate.
   By the spec's precedence rule §b(1) Zhang's class-based rule is the operative
   intent, and the code implements exactly it: the interrupt fires on resource
   class, and `apply_mtd_interrupt_cost` clears the host cursor for the `network`
   class (`attack_operation.py:206-208`).
3. **Therefore the pair is unseparated for a documented reason.** IS-INT-04 makes
   the attacker-facing effect of network-layer MTD *class-uniform*. Complete
   Topology Shuffle and IP Shuffle are both `resource_type='network'`, so they
   deliver the same documented interaction; Complete Topology Shuffle
   additionally moves adjacency, which the attacker does read, and IP Shuffle
   moves a label only the defender's own metric reads.

**Verdict: CONFORMS.** Brown's staleness predicate is unimplemented and
superseded, not divergent. No disposition is requested. What is requested is a
**correction to two records** (§(h)): the handoff's premise sentence, and brief
2's cross-filled claim that `host.ip` "has zero readers repo-wide".

The consequence for the evaluation is real but different from the one the
programme expected: `(complete_topology, ip_shuffle)` being unseparated is not
evidence that IP Shuffle was under-integrated. It is evidence that **the
substrate models network-layer MTD as a single attacker-facing effect**, so a
comparative evaluation over that class can distinguish its members only by what
they *additionally* move. The four-mechanism family carries two effects because
the *model* has two attacker-facing effects, and stating that is stronger than
attributing it to a defect.

### Finding 2 — the credential channel carries a fifth to a quarter of all compromises, and no mechanism in the reported family can touch it.

`host.users` is read on two attacker paths (SCAN_PORT phase-1 reuse, BRUTE_FORCE)
and moved by **no** mechanism in the reported family; UserShuffle, the only
mechanism that would, is commented out of the default pool
(`mtd_scheme.py:22-31`). Brief 2 recorded the immobility; this brief measures
what rides on it. Compromise routes, 10 seeds × 5 000 t.u. per arm, native FSM,
each reported mechanism run singly:

| Arm | via vulnerability | via credential reuse | via brute force | credential share |
|---|--:|--:|--:|--:|
| none | 97 | 29 | 1 | 22.8 % |
| CompleteTopologyShuffle | 78 | 19 | 0 | 19.6 % |
| IPShuffle | 80 | 11 | 0 | 12.1 % |
| OSDiversity | 27 | 3 | 0 | 10.0 % |
| ServiceDiversity | 30 | 6 | 0 | 16.7 % |
| simultaneous (all four) | 47 | 10 | 0 | 17.5 % |

Two readings, and the second is the one that matters:

- The credential route is **not** a defence-immune floor. It falls with the
  defence (29 → 3–19), because credential stuffing requires users harvested from
  an already-compromised host, so suppressing the first compromise suppresses the
  cascade. The evaluation is therefore not floored by an unopposed channel, and
  the pre-emptive worry is answered in the negative.
- But the channel is **structurally unopposed**: every one of the four mechanisms
  attacks it only indirectly, and none of them differentially. It cannot invert a
  ranking, and it does compress the family's measurable range — the reported
  family is a contest over the vulnerability surface and the path structure, with
  a credential route running underneath it that none of them addresses.

Recorded as a disposition request, **D-27**, because the decision it poses —
whether the reported family stays at four with this stated, or gains UserShuffle
for future runs — is a scoping decision only Marc can take, and it bears on how
the headline family is described.

### Finding 3 — `Host.total_users` is not the number of user accounts on the host, and BRUTE_FORCE divides by it.

`Host.__init__` sets `total_users = 0` (`host.py:49`); `set_host_users`
(`host.py:478-494`) then **increments** it inside a loop that `break`s at the
first password-reusing user:

```python
for user_reuse in self.users.values():
    self.total_users += 1
    if user_reuse:
        self.p_u_compromise = True
        break
```

So `total_users` is the 1-based index of the first reusing account, not the
account count. `compromise_with_users` (`host.py:179`) uses it as the divisor of
the brute-force probability:
`random.random() < HOST_MAX_PROB_FOR_USER_COMPROMISE * len(attempt_users) / self.total_users`.

Verified live: on a freshly built 50-host network (seed 99), **12 of 50 hosts**
have `total_users != len(users)`, with ratios up to 5/2 — those hosts' brute-force
probability is inflated by up to 2.5×. A second, independent departure from
IS-NET-11 ("each host has **5 user accounts**") rides alongside: `users` is a
dict built from `random.choices`, so duplicate draws collapse and hosts routinely
carry 4 rather than 5 accounts. Because `set_host_users` increments rather than
assigns, repeated calls compound — latent today, since only UserShuffle calls it
again.

**Ranking-relevance, measured rather than argued.** Across the 60 runs in finding
2, BRUTE_FORCE was called **488** times and produced **one** compromise, all arms
combined; in the defended arms, zero. With `HOST_MAX_PROB_FOR_USER_COMPROMISE =
0.01` and at most five accounts, the per-call probability is bounded by 0.05 even
in the worst inflated case (against 0.01 with a correct divisor), so the route
this defect governs is very nearly inert. It cannot move a comparative ranking. It is nonetheless a value the
attacker reads that does not mean what its name and its reader assume, and no
lineage paper documents the formula or the count.

**§c verdict: DIVERGES-DOCUMENTED-NOWHERE** (candidate; evidence for "bug": the
counting increment is caught inside a loop whose `break` exists to set a
different flag — the shape of an unintended defect, not a self-consistent design
choice). → **D-26**.

### Finding 4 — service identity is invisible; the diversity mechanisms reach the attacker only through the vulnerability set.

`Service.name` and `Service.version` are read in the whole system only by
`Service.copy` (`services.py:256`) — 3 723 native / 24 672 driven reads, all
internal cloning — and by `Service.__eq__`, which was **not called once** in
either censused run. The attacker never observes what a service *is*; it observes
the ports the services sit behind and the vulnerabilities they carry
(`host.py:281-324` sorts by `get_highest_roa_vuln()`, never by identity).

Two consequences. First, Service Diversity's documented "re-configure services
with different versions" (IS-MTD-05) reaches this attacker as *a fresh
vulnerability draw with reset exploitation state*, and by nothing else — which is
why brief 2's revocation semantics (§b5 there) are the whole of its effect.
Second, the absence of any `Service.__eq__` call independently corroborates D-18
from the other side: the inert compatibility test short-circuits at the
`isinstance` guard (`services.py:304-307`) and never reaches a name comparison,
so it fails before it can even be wrong about identity.

No disposition — this is recorded as the mechanism behind an already-open row.

### Finding 5 — the attacker attacks hosts it cannot reach, and only in the movement arm. *(Found by the adversarial pass; measured here. The one finding that can move a ranking.)*

**IS-PRC-01 states a visibility invariant**: internal hosts are visible "**only
if a path exists** through a compromised or exposed internal host". SCAN_HOST
enforces it when it builds the queue (`attack_operation.py:285` drops any
neighbour with no path in the visible graph). **ENUM_HOST does not re-check it.**
`sort_by_distance_from_exposed_and_pivot_host` (`network.py:868-901`) only
*sorts* — an unreachable host scores `LARGE_INT` and sorts last, but is never
dropped — and `_do_enum_host` (`:333-379`) pops the head of `_host_stack` and
attacks it whatever its reachability.

In the native FSM this never bites, because the invariant is enforced by
**control flow** rather than by a guard: a network-class interrupt runs
`_handle_interrupt` → `_scan_host()` (`:228-233`), which rebuilds the stack from
the *current* visible graph and flushes stale entries. Measured: **0 of 873**
ENUM_HOST pops over 20 native runs (10 seeds undefended, 10 defended) popped a
host outside the visible graph.

The movement driver owns its own succession and **deliberately does not
re-impose the native order** after an interrupt — it reads the interrupt as a
failure verdict and lets the controller route (`attacker.py:456-482`, the
H-coupling rationale). SCAN_HOST is therefore never forced, `_host_stack` is
never flushed, and the invariant has nothing enforcing it. Measured over 10
seeds each:

| Movement arm | ENUM_HOST pops | popped host with **no path** from any exposed endpoint |
|---|--:|--:|
| undefended | 382 | **37 (9.7 %)** |
| defended, all four mechanisms | 411 | **92 (22.4 %)** |

**The rate more than doubles under MTD, which is the point.** MTD is what makes
queued hosts unreachable, and the attacker goes on attacking them regardless. The
mechanism whose entire claim is topology disruption — Complete Topology Shuffle —
is precisely the one this blunts, and it blunts it in **the arm the project's
headline result is computed on** (experiment 2 §9, Row B of the APT criterion).

**Why this is a substrate finding and how a repair would propagate.** The missing
guard is in `_do_enum_host`, a **shared verb core**. The couplings it governs are
outcome-channel, so a guard added there reaches movement-driven runs
automatically, with no controller-mapping change — the propagation statement the
brief's hard constraints require. No movement-layer change is implied, and none
should be made: the driver's refusal to re-impose native succession is the
declared design.

**§c verdict: DIVERGES-DOCUMENTED-NOWHERE**, and unusually well-evidenced as a
candidate *bug* rather than a design choice, on §c's own test — it "violates an
invariant the papers state" (IS-PRC-01), and it does so only because the carve
moved succession out from under an invariant that was never guarded. → **D-28**.

**What is not established.** The undefended 9.7 % has a second source that this
review did not diagnose; only the MTD-induced increment (9.7 → 22.4 %) is
attributed. And the effect on the *ranking* is argued, not measured: no arm has
been re-run with a guard in place, and none may be under the no-re-run
constraint. Both are carried into the confidence evaluation as residual doubts.

### Finding 6 — mechanism arms do not share the attacker's dice, so seed-matched arms are not paired.

Also from the adversarial pass, verified here. The MTD mechanisms and the
attacker draw from the **same global `random` stream** — the attacker's
exploit-success draw (`services.py:150`), its sort jitter (`network.py:896`,
`attack_operation.py:292`) and its brute-force draw (`host.py:179`) all come from
stdlib `random`, as do the mechanisms' own draws. Consumption per firing differs
by nearly an order of magnitude (10 seeds, defended, native arm):

| Mechanism | firings | draws | draws per firing |
|---|--:|--:|--:|
| CompleteTopologyShuffle | 130 | 17 492 | **134.6** |
| IPShuffle | 120 | 21 600 | **180.0** |
| OSDiversity | 130 | 129 909 | **999.3** |
| ServiceDiversity | 120 | 114 516 | **954.3** |

So at a fixed seed the four arms do **not** replay the same attacker: choosing a
mechanism realigns the attacker's own dice. This is realignment noise, not bias —
it does not systematically favour any mechanism — but it means **common random
numbers do not work across mechanism arms**, and a seed-matched comparison is an
independent-sample comparison rather than a paired one. That raises the seed
count needed to separate two mechanisms, which is directly relevant to the
standing "ten seeds supports a rank comparison and not a significance test"
caveat (APT criterion Row B): the caveat is, if anything, understated.

The movement layer's own timing and token streams are isolated
(`timing.py:54-77`, `attacker.py:282`), so this is a substrate-stream property
present in both arms. Recorded, not dispositioned: no code change is proposed,
because isolating the substrate's streams would move every golden and the honest
remedy is a statement about the experimental design rather than a repair. →
recorded in §(i) as **D-29 (record-grade)**.

## (g) New evidence bearing on the open D-18 decision (not a re-litigation)

D-18 asks whether to repair `service_is_compatible_with_os`. The
indistinguishability brief costed the options but could not say **how much
separation a repair would buy**, because that turns on the service catalogue's
structure. Measured (seed 42 generator, 5 000 simulated service-vs-new-OS checks
reproducing OSDiversity's own draw at `osdiversity.py:25-26`):

- Of 80 distinct service names, **42 (52.5 %) are cross-platform** and available
  on all four OS types, 38 are single-OS — the direct expression of IS-NET-06's
  50 % cross-platform rule.
- Because cross-platform services appear in *every* OS catalogue, they dominate
  any one OS's catalogue (~48–54 names per OS, ~42 of them cross-platform), so a
  service drawn for a host is only ~19 % likely to be OS-specific.
- Under a name-based repair, **13.9 %** of services would be judged incompatible
  and replaced per firing, against ServiceDiversity's 100 %.

Two things follow for the ruling, both new:

1. **A repair separates the diversity pair decisively** — roughly a sevenfold
   difference in write volume per firing, not a marginal one. D-18(a) is the
   option that restores the family to four distinguishable mechanisms, and
   decision C's cardinality question would be answered by construction rather
   than by qualification.
2. **`os_version` would remain inert even after the repair.** The name set is
   *identical across all six versions* of each OS (verified: one distinct name
   set per OS type), so a name-based guard keys on `os_type` alone. Any repair
   that is meant to make the OS *version* load-bearing would need to be a
   different, larger change — worth knowing before choosing wording for the fix.

Recorded for Marc's D-18 ruling; nothing here re-opens it.

## (h) Corrections to records currently on file

1. **`host.ip` does not have "zero readers repo-wide".** It has three, all
   defender-side: `completetopologyshuffle.py:35`, `mtd_ai_operation.py:308`,
   `mtd_ai_training.py:254` — the last two implementing NAV (IS-MET-04). The
   claim appears in the boundary handoff's programme framing and is cross-filled
   into [`mtd_write_surfaces.md`](mtd_write_surfaces.md) §(c) (IPShuffle row) and
   §(b)6. The *attacker-facing* conclusion is unchanged and is now verified by
   projection diff rather than by search; the repo-scope claim is withdrawn, and
   with it the "vestigial surface" reading — see finding 1.
2. **`host.os_type` and `host.os_version` are not one component with two
   channels.** `os_version` has **no** channel to the attacker at all — not even
   the time channel, since the ×2.5 multiplier tests `host.os_type` alone
   (`services.py:116`). The indistinguishability brief's §1.2 treats the pair
   jointly; the sharper statement belongs on the record because it bears on D-18
   (§(g) point 2).

## (i) Findings requiring disposition

Numbering continues after boundary review 3's concurrent allocation (D-20..D-22)
and boundary review 2's (D-23..D-25), same day. Nothing was changed in code.

| # | Finding | Options (costed) | Recommendation |
|---|---|---|---|
| **D-26** | **`Host.total_users` is the index of the first password-reusing account, not the account count** (§(f) finding 3); BRUTE_FORCE divides the compromise probability by it, inflating it up to 2.5× on 12 of 50 hosts. Compounds on repeated `set_host_users` (latent — UserShuffle only). Also: duplicate-name collapse means hosts carry 4 rather than IS-NET-11's 5 accounts | **(a) Repair** — assign `self.total_users = len(self.users)` outside the reuse loop; a two-line change, but it moves the brute-force probability on ~24 % of hosts and therefore **moves every golden** (D-05 procedure: deliberate re-baseline, `baseline/CHANGELOG.md`, SIM-05 re-verified), plus a regression test asserting `total_users == len(users)` after `set_host_users` and after a second call. **(b) Keep and document** — zero risk; the route it governs produced 1 compromise in 388 calls, so the measured cost of leaving it is close to nil. **(c) Repair and also make the account count 5** (dedupe the `random.choices` draw) — restores IS-NET-11 fully, but is a network-generation change that moves the seeded topology and every golden far more disruptively | **(a)**, if a golden re-baseline is being taken for another ruling anyway; otherwise **(b)**. Not **(c)** — the account-count question is an IS-NET-11 conformance matter that should be decided on its own evidence, not folded into a divisor repair |
| **D-27** | **The credential channel is structurally unopposed by the reported family** (§(f) finding 2): `host.users` is read by SCAN_PORT phase 1 and BRUTE_FORCE, moved by no mechanism in the default pool, and carries 10–23 % of all compromises | **(a) Keep the family at four and state it** — zero risk; add the unopposed-channel fact where the family is described, so the evaluation's scope is explicit. **(b) Add UserShuffle to the reported family** for future runs — it is built and its write set is verified (brief 2 §(a)); no recorded experiment is re-run, so this is a new-experiment decision, not a repair; it would give the family a mechanism attacking a channel currently addressed only indirectly, and would need its own comparability statement. **(c) Record only in this file** — cheapest, but leaves the headline family described without its scope boundary | **(a)**. The project's scope is existing mechanisms and a fixed family (`project_context.md` § direction); the finding is a boundary on what the comparative result *means*, and stating it strengthens the record. **(b)** is a genuine option but is a new experiment, and the evidence does not show the channel confounding any ranking |
| **D-28** | **ENUM_HOST does not enforce IS-PRC-01's visibility invariant, so the movement attacker attacks hosts with no path from any exposed endpoint — 9.7 % of pops undefended, 22.4 % defended** (§(f) finding 5). The native arm is unaffected (0 of 873) because its forced post-interrupt SCAN_HOST flushes the stack; the movement driver declines to re-impose that succession by design | **This is the one finding that can move a comparative ranking**, and it blunts Complete Topology Shuffle specifically, in the arm the headline result runs on. **(a) Guard `_do_enum_host`** — drop (or defer) a popped host with no path in the hacker-visible graph. It is a shared verb core, so the repair reaches **both** arms automatically through the outcome channel, no controller-mapping change; it moves every golden (D-05 procedure) and would change the movement arm's measured MTD effect in the direction of *strengthening* the topology mechanisms. Regression test per gate 5: assert ENUM_HOST never sets `curr_host` to a host outside `get_hacker_visible_graph()`. **(b) Guard at the queue instead** — filter `_host_stack` on every mutation; equivalent effect, but spreads the invariant across the MTD path rather than keeping it in the verb that violates it. **(c) Keep and document** — records that the movement attacker's reachability model is weaker than IS-PRC-01, and that recorded topology-mechanism effects are therefore lower bounds | **(a)**, subject to Marc's ruling. The §c evidence for "bug" is unusually strong — it violates an invariant the papers state, and it exists only because the carve moved succession out from under an invariant nothing guarded. Note the honest limit: the ranking effect is argued from the mechanism, not measured, and cannot be measured without a run that the no-re-run constraint does not forbid but this brief did not take |
| **D-29** *(record-grade)* | **Mechanism arms do not share the attacker's dice** (§(f) finding 6): mechanisms and attacker draw from the same global `random` stream, and consumption per firing ranges 134.6 (CTS) to 999.3 (OSDiversity), so a fixed seed does not replay the same attacker across arms | No code change proposed — isolating the substrate's streams would move every golden for no gain in fidelity. **(a) Record** in `metrics_semantics.md` alongside the existing comparability boundary, so that seed-matched arms are described as independent rather than paired samples. **(b) Isolate the streams** — large, golden-moving, and buys only variance reduction in future runs | **(a)**. It sharpens rather than contradicts the standing ten-seeds caveat (APT criterion Row B): common random numbers are unavailable across mechanism arms, so that caveat is if anything understated |

## (j) The adversarial pass, and what it changed

Gate (v) of the brief requires a fresh look that actively hunts for a coupling
the matrix missed. It was run as an independent red-team pass against the
completed matrix, briefed to falsify rather than confirm, with the matrix's
verdicts stated to it as claims to break. **It found new material**, which is
recorded here rather than absorbed silently, because the fact that it found
things is itself the confidence evaluation's most important input.

What it confirmed (clean negatives, now doubly sourced): no read path from any
verb, from `step()`, or from the movement layer reaches `host.ip`,
`host.os_version`, `Service.name` or `Service.version`; `host.os_type` reaches
the attacker through exactly one call site (`attack_operation.py:466`) and only
when `charge_time=True`; no pool mechanism writes a port or a credential; no pool
mechanism reads the `adversary` argument at all.

What it added, and where each landed:

| Red-team finding | Disposition here |
|---|---|
| ENUM_HOST gates on nothing — topology is a sort key, not a filter | **Finding 5 / D-28** — measured in-run by this review; native arm 0 %, movement arm 9.7 → 22.4 % |
| Mechanisms and attacker share the global RNG stream | **Finding 6 / D-29** — draw counts measured in-run |
| The vulnerability coupling is cross-service, not per-service | matrix row sharpened (pooled RoA stack) |
| Diversity cannot un-compromise a host, so the reset bites only on unowned hosts | matrix row sharpened (bound (ii)) |
| The entry surface is invariant under the whole pool | matrix row sharpened (exposed-endpoint set) |
| `gen_graph` also rewrites `subnet`/`layer`/`colour_map`/`pos`/`node_per_layer` | write-column completion → **brief 2**; all dead on the attacker path (`get_host_id_priority` has no callers) |
| IPShuffle's uniqueness set excludes endpoints; its scorer feed carries 45 entries against CTS's 50 | → **brief 2** (metric-feed asymmetry, adjacent to D-24) |
| IPShuffle alone never calls `add_shortest_path` / `add_attack_path_exposure` | → **brief 2** (would differentiate mechanisms the moment metrics are sampled per mutation; latent under D-24) |
| Movement arm interrupts dwell places and absorbs interrupts the native arm never receives; a network-class MTD arriving during an application-class penalty loses its cursor-clear | → **brief 3** (interrupt channel), flagged as arm-comparability material |
| EXPLOIT_VULN is uninterruptible in the movement arm (one up-front timeout, no per-vuln yields) so diversity gets fewer blocking windows there | → **brief 3**, and a genuine arm asymmetry |
| Application-class interrupts force a fresh SCAN_PORT that re-buys provably unchanged information | → **brief 3** (time tax with no state basis) |

The three items routed to briefs 2 and 3 are flagged, not actioned, per the
programme's ownership rule and the scope guardrail.

## (k) Confidence evaluation — **the gate does not pass**

The brief's question: *are we ≥ 95 % confident that no undispositioned dead,
partial, or mapping-declined coupling remains at this boundary that could change
a comparative MTD ranking?* The figure is a structured judgement against the
brief's checklist, not a computed statistic. Answering honestly:

| Criterion | Status |
|---|---|
| (i) every matrix cell has a locator, an expression-channel verdict, and its movement-driving reach | **met** — §(b) |
| (ii) every live verdict has a run-level demonstration | **met** — census counts per arm plus the §(c) projection diffs |
| (iii) every dead verdict has a disposition or an open D-number | **met** — `ip` resolved as CONFORMS (finding 1); `os_type`/`os_version`/service identity ride D-18/D-19; new candidates opened as D-26..D-29 |
| (iv) every unseparated mechanism pair has a code-level cause on record | **met, and strengthened** — both pairs now have causes verified by projection diff, and both reproduce in a third independent measurement (§(f) finding 2's per-mechanism table) |
| (v) an adversarial pass found nothing new | **NOT MET** — §(j). It found two ranking-relevant items, three matrix sharpenings, and six items belonging to the sibling briefs |

**The gate fails on (v), and the failure is substantive rather than
bookkeeping.** D-28 is exactly the class of thing this programme exists to catch:
an unexamined read-gap that blunts one named mechanism, in the arm the headline
result is computed on, and the completed matrix did not contain it. A matrix that
missed that cannot support a 95 % claim on the strength of having been checked
once.

**Residual doubts, named, as the residual-doubt rule requires:**

1. **D-28's ranking effect is argued, not measured.** The mechanism is verified
   and quantified (22.4 % of pops); the consequence for Complete Topology
   Shuffle's measured rank is inferred from it. *Could plausibly move a ranking —
   fails the gate on its own.*
2. **A second adversarial pass has not run.** The first one found things after
   the matrix was believed complete; the base rate for a second finding nothing
   is not established. *Unquantified.*
3. **The undefended 9.7 % in finding 5 is undiagnosed.** Only the MTD-induced
   increment is attributed. *Bears on how much of D-28 is an MTD-interaction
   effect versus a standing modelling weakness.*
4. **The census covered one seed per arm and one geometry.** Read *presence* is
   structural and unlikely to be seed-dependent, but read *counts* — and the
   zero-count claims that carry the dead verdicts — were taken at one seed each.
   The projection diffs and the route census used further seeds; the census
   itself did not. *Low risk, cheap to close.*
5. **Sibling-brief items are flagged, not resolved.** Two of them (movement-arm
   interrupt asymmetries, EXPLOIT_VULN's missing blocking windows) are
   arm-comparability facts that could bear on the diversity mechanisms' measured
   effect. *Owned elsewhere, but open.*

**Cycle 2, scoped to exactly these doubts** (per §5 of the brief): re-run the
adversarial pass against the *updated* matrix (doubt 2); diagnose the undefended
9.7 % (doubt 3); repeat the census at three further seeds and confirm every zero
stays zero (doubt 4); and — only if Marc rules D-28 actionable — measure rather
than argue the ranking effect by running the guarded substrate as a *new*
comparative arm, which the no-re-run constraint permits because it creates a new
substrate version rather than re-running a recorded experiment (doubt 1). Doubt 5
closes when briefs 2 and 3 consume their flagged items.

## (l) Cycle 2 (2026-08-03) — Part B landed, four doubts closed, one defect class enumerated

Marc ruled D-28 a fix ("CTS disconnected hosts from the attacker, so implementing
it faithfully is a given"). Cycle 2 implemented it and ran the four doubts that
did not depend on a further ruling.

### (l1) Part B — the guard

`AttackOperation.visible_host_stack` applies the **same predicate SCAN_HOST uses
when it builds the queue**, in the shared verb core, asserted by both `_enum_host`'s
raise and `assert_action_context`. Both arms inherit it; no controller-mapping
change. Full D-05 procedure in `baseline/CHANGELOG.md` (2026-08-03): 67 of 69
movement goldens re-captured, **the nine native goldens bit-identical**, SIM-05
re-verified on both arms, suite green, nine-case regression test in
`tests/test_enum_host_visibility.py`.

The native goldens not moving is the re-baseline's own confirmation of the
diagnosis: the defect was measured at 0 of 873 native pops, so the native oracle
had to stay put, and it did.

### (l2) Doubt 1 — CLOSED, and it falsified the prediction

Cycle 1 argued the guard would *strengthen* the topology mechanisms. Measured (new
comparative arm, 10 seeds, movement arm, guard patched off to reproduce the
pre-guard substrate — permitted, since it creates a new arm rather than re-running
a recorded experiment):

| condition | unguarded | guarded | Δ |
|---|--:|--:|--:|
| none | 5.60 | 5.60 | +0.00 |
| complete_topology | 0.90 | 0.80 | −0.10 |
| ip_shuffle | 0.80 | 0.80 | +0.00 |
| os_diversity | 3.10 | **4.70** | **+1.60** |
| service_diversity | 3.60 | **4.30** | **+0.70** |
| simultaneous | 1.20 | 1.50 | +0.30 |

**The prediction was wrong in its mechanism and right in its conclusion.** The
topology mechanisms did not strengthen — they barely moved. What happened is that
the *diversity* mechanisms weakened, because a dropped target **redirects** the
attacker rather than stopping it: the movement layer reads the blocked dispatch as
a routing failure and spends the action elsewhere. The family-level contrast
nevertheless widens from ≈40 points to ≈65, so the inversion Row B rests on is
strengthened — by a different route than the one argued. Recorded as a falsified
prediction rather than quietly rewritten, because the residual-doubt rule exists
to catch exactly this.

### (l3) Doubt 3 — CLOSED, and it opened D-33

The undefended 9.7 % is **SCAN_NEIGHBOR dispatched from an uncompromised host**.
IS-PRC-05 makes neighbour discovery what compromise *grants* ("assume C2
functionality"), and Brown Fig 3 box 9 names the host "Recently Compromised". The
native FSM reaches SCAN_NEIGHBOR only from a compromise branch; the controller can
dispatch it whenever `curr_host` is set, and `assert_action_context` requires only
that. `_do_scan_neighbors`' own docstring already states the precondition the code
does not assert: *"semantically only meaningful on a just-compromised host"*.

Measured: **166 of 345 SCAN_NEIGHBOR calls (48 %) fire from an uncompromised host
in the movement arm, against 0 of 71 natively.** → **D-33**.

### (l4) Doubt 4 — CLOSED

The census was repeated at three further seeds per arm (native 11/12/13, movement
5/6/7). Every zero held: no attacker-path read of `host.ip`, `host.os_version`,
`Service.name` or `Service.version` in either arm, and `exploit_time(host=…)`
called 755 times natively against **0** driven — the time-channel decline
reproduces.

### (l5) Doubt 2 — the second adversarial pass found nothing new *at this boundary*

An independent pass ran against the updated matrix, briefed to assume the obvious
was covered and to hunt the statistics path, time accounting, the scheduler, the
verdict adapter, and cross-mutation state. **It surfaced no attacker read of
network state that the matrix lacks.** What it did surface is a substantial set of
findings at *other* layers, recorded in §(m) and routed rather than actioned.

### (l6) The defect class, enumerated and closed

D-28 and D-33 are the same defect: **an invariant the native FSM enforced by call
order, which the carve dropped when it moved succession out.** Rather than keep
discovering members one at a time, all six verbs were swept — what did native call
order guarantee, and does `assert_action_context` assert it?

| Verb | Native-order guarantee | Asserted? | Movement arm | Native arm | Kind |
|---|---|---|--:|--:|---|
| ENUM_HOST | target still visible (IS-PRC-01) | **now yes** (D-28) | was 22.4 % | 0 | **semantic** |
| SCAN_NEIGHBOR | host is compromised (IS-PRC-05) | no | **48 %** | 0 of 71 | **semantic** → D-33 |
| BRUTE_FORCE | exploitation attempted first (IS-PRC-06) | no | 60 of 61 | 0 of 71 | procedural |
| SCAN_PORT | host not already compromised | no | 4 of 60 | 0 of 175 | procedural |
| SCAN_HOST | none (root verb) | n/a | — | — | — |
| EXPLOIT_VULN | curr_host + ports from *this* host's scan | **yes** | — | — | — |

**The class divides on a principle, and that is what closes it.** A *semantic*
guarantee is about what the attacker can see or has earned — IS-PRC-01 states a
visibility condition, IS-PRC-05 states what compromise grants; neither is a
statement about order, so a driving layer that varies order must still honour
them. A *procedural* guarantee is a sequencing statement — IS-PRC-06's "on exploit
failure, commence brute force" — and varying it is precisely what the movement
layer exists to do; re-imposing it would "manufacture the very coupling the
evaluation tests for" (the H-coupling rationale, `attacker.py:456-482`). So the two
procedural rows are **CONFORMS by design**, not defects, and the class has exactly
two members: one fixed, one open as D-33.

Every member occurs in the movement arm and **none** in the native arm, which is
the signature the diagnosis predicts and a further reason to treat the class as
closed rather than sampled.

### (l7) D-33's ranking effect — measured before it is put to Marc

The same counterfactual technique as (l2), gating SCAN_NEIGHBOR on compromise:

| condition | ungated | gated | Δ |
|---|--:|--:|--:|
| none | 5.60 | 7.80 | +2.20 |
| complete_topology | 0.80 | 0.80 | +0.00 |
| ip_shuffle | 0.80 | 0.70 | −0.10 |
| os_diversity | 4.70 | 7.00 | +2.30 |
| service_diversity | 4.30 | 6.70 | +2.40 |
| simultaneous | 1.50 | **0.70** | **−0.80** |

**The ranking changes**: `simultaneous` moves from third to first. And as in (l2),
gating *raises* the attacker's compromise count everywhere except the
position-destroying conditions — the same redirection effect. So D-33 is a doubt
that demonstrably moves a ranking, which is why it is put to Marc rather than
implemented on this brief's authority: it is a far larger behavioural change than
D-28 (48 % of dispatches), and Marc has not ruled it.

## (m) Findings routed to other owners (flagged, not actioned)

The second adversarial pass surfaced material outside this boundary. Per the scope
guardrail these are flagged, not actioned. **One is more ranking-critical than
anything at this boundary and no brief in the programme owns it.**

### (m1) The metric named "internal MTTC" ranks the mechanisms perversely — **unowned, and this review recommends its own brief**

`evaluation.py:110` computes `attack_duration_series.sum() / attack_action_count`
— attack-action time over the **number of attack actions**. That is a **mean
action duration**, not a time to compromise. A sibling function at
`evaluation.py:47` divides by `compromised_num` (the name-faithful quantity) and
nothing consumes it.

**The code matches its documentation**: `metrics_semantics.md` §(a) states the
definition accurately and quotes the implementation. So this is *not* a code/doc
divergence. What it is, is a quantity that does not behave like the thing its name
and its use imply. Verified by this review directly from the committed goldens, at
the **first** checkpoint where every scenario sits at the identical compromise
depth (`host_compromise_ratio` = 0.06), so the differing-slice-depth confound is
removed:

| golden scenario | `time_to_compromise` | `attack_success_rate` |
|---|--:|--:|
| single-ipshuffle | **9.938** | 0.0252 |
| alternative-multi | 9.061 | 0.0156 |
| no-mtd_seed9999 | 8.810 | 0.0122 |
| no-mtd | 8.738 | 0.0156 |
| random-multi | 8.690 | 0.0155 |
| simultaneous-multi | 8.655 | **0.0278** |
| primary-random-15k | 7.782 | 0.0058 |
| single-osdiversity | **7.594** | 0.0055 |

**IP Shuffle — the mechanism this review verified changes not one field of the
attacker's readable projection — scores best.** OS Diversity, which genuinely
moves the vulnerability surface, scores worst, below no defence at all. And the
four-mechanism `simultaneous` arm carries the *highest* attack success rate of any
scenario, above undefended.

**Calibration, so this is neither overstated nor understated.** It does **not**
carry the headline: experiment 2 §9's ranking and Row B's inversion are computed
on compromise suppression in the movement arm, and cross-arm MTTC was explicitly
withdrawn under S3-R (`experiment_02_findings.md` §255). The movement arm defines
its own MTTC as first-compromise time, which is sound. But
`../workflows/project_context.md` names internal MTTC **the project's primary
metric**, and `metrics_semantics.md` §(d) asserts that within-substrate
cross-configuration deltas are "**Valid** — the delta between them is
informative". That assertion is what these numbers put in question, for the
MTD-comparison use it is invoked for.

**Owner: none.** Brief 1 owns the attacker's reads, brief 2 the defender's writes,
brief 3 the direct couplings. The evaluation/metrics layer is outside all three.
Recommendation: its own brief, before any ch5 prose leans on internal MTTC.

### (m2) Routed to brief 2 (defender write side / scheduling)

- **Priority-queue asymmetry.** Both class pairs share a capacity-1 resource and
  contention resolves FIFO in priority order, so the higher-priority member gets a
  systematic extra firing — seed-invariant. Reported as OSDiversity 13 ·
  CompleteTopologyShuffle 13 · ServiceDiversity 12 · IPShuffle 12 in every one of
  six movement seeds, and 80 vs 70 firings natively. It would tend to separate each
  unseparated pair *spuriously*, in favour of the higher-priority member.
- **Near-deterministic durations.** `exponential_variates(loc, scale)` is a
  *shifted* exponential and every call site passes `scale=0.5`, giving CV ≈ 0.001–0.03
  against the CV = 1.0 the lineage specifies. Under `simultaneous` this phase-locks
  which verb each mechanism interrupts (CTS → SCAN_PORT 69/70; IP Shuffle →
  EXPLOIT_VULN 67/70; Service Diversity → SCAN_PORT 70/70), so what a mechanism
  costs the attacker is decided by duration arithmetic rather than by the defence
  idea. Diffuse under `random`/`alternative`, which is the control.
- **D-24's premise needs revisiting.** `get_metrics` is *also* called once per
  checkpoint inside `evaluation_result_by_compromise_checkpoint`, and five of its
  outputs are written into `baseline/golden/*/evaluation.json`. The ruling was taken
  on "no recorded arm consumes the values".

### (m3) Routed to brief 3 (direct attacker/defender couplings)

- **The movement record downgrades interrupt attribution from mechanism to
  resource class** (`attacker.py:552-562` keeps `get_resource_type()` and discards
  the available `get_name()`), so CTS/IP Shuffle and OS/Service Diversity are
  indistinguishable *by construction of the record* — a second, measurement-side
  cause of the unseparated pairs, which would have to be removed before the
  substrate-side cause could be tested in the headline arm.
- **The confusion penalty is charged to no record row**, so ~10 % of the simulated
  horizon is invisible to every record-derived metric.
- **Application-class interrupts are gated out of SCAN_HOST/ENUM_HOST/SCAN_NEIGHBOR**
  and the verdict adapter reads those verbs as success-unless-interrupted, so OS and
  Service Diversity can never produce a failure verdict on them.
- **EXPLOIT_VULN is uninterruptible in the movement arm** (one up-front timeout, no
  per-vulnerability yields), so the diversity mechanisms get fewer blocking windows
  there than natively.

## (n) Confidence evaluation, cycle 2 — **still short of the gate, and now for a bounded reason**

| Criterion | Cycle 1 | Cycle 2 |
|---|---|---|
| (i) every cell has locator, channel, movement reach | met | met |
| (ii) every live verdict run-demonstrated | met | met, now at four seeds per arm |
| (iii) every dead verdict dispositioned or D-numbered | met | met (D-33 added) |
| (iv) every unseparated pair has a code-level cause | met | met |
| (v) adversarial pass found nothing new **at this boundary** | **failed** | **met** |

**What improved.** The matrix survived an independent second pass. Three of five
residual doubts are closed by measurement, not argument, and one of those
measurements *falsified* the prediction cycle 1 had made — which is the process
working. The defect class behind D-28 was enumerated across all six verbs and
divided on a principle (semantic versus procedural guarantees), so it is closed
rather than sampled: exactly two members, one fixed, one open.

**Why the gate still does not pass.** Two reasons, both narrower than cycle 1's.

1. **D-33 is measured to move a ranking and is undispositioned.** The gate's
   question is precisely whether such a thing remains. It does, pending Marc.
2. **The discovery process has not gone dry at the programme level.** Cycle 1 found
   a ranking-mover, cycle 2 found another. The class enumeration in §(l6) is the
   first structural reason to expect convergence — it bounds where further members
   of *this* class can hide — but one clean round is not two.

**Residual doubts, cycle 2:**

1. **D-33, undispositioned**, ranking effect measured. *Fails the gate on its own.*
2. **The class enumeration rests on the semantic/procedural distinction**, which is
   this review's judgement, not a paper's. If Marc reads IS-PRC-06 as semantic, the
   class gains a member.
3. **(m1) is unowned and is more ranking-critical than anything at this boundary.**
   Out of scope here, but it bears on the same question the programme asks.
4. **Sibling-brief items** in §(m2)/§(m3) are routed, not resolved — several bear on
   the unseparated pairs this brief's criterion (iv) reports as explained.
5. **Ranking effects are measured on a new comparative arm** (10 seeds,
   `compromised_count`), not on experiment 2's own measure. Direction is
   established; magnitude is not transferable to Row B.

**Cycle 3, scoped:** Marc rules D-26, D-27, D-29, D-33 and the semantic/procedural
reading in doubt 2; a third adversarial pass targeted at the *precondition class*
specifically; and — the recommendation this review would make above all others —
open a brief for (m1) before any chapter prose leans on internal MTTC.

## (o) Reproduction

The census and probes are scratch instrumentation, not repository code, and were
run from the repo root under `PYTHONPATH=src`. Each installs read-only counting
proxies as described in §(a) and re-runs the two arms named there. The
substantive checks, for a session that wants to re-verify rather than re-derive:

- **read census, both arms** — counting properties on `Host.ip` / `os_type` /
  `os_version` / `Service.name` / `.version` plus wrapped read methods; assert
  `exploit_time(host=…)` call count is non-zero native and **zero** driven, and
  that `Vulnerability.network`'s host argument is read on neither.
- **projection diff** — snapshot `{edges, nodes, exposed, reachable}` plus per
  host `{ports, vuln ids, exploited services, users, neighbours}`; fire one
  mechanism; diff. IPShuffle must produce an empty diff; OSDiversity and
  ServiceDiversity must produce equal diffs.
- **compromise-route census** — wrap `can_auto_compromise_with_users`,
  `compromise_with_users` and `check_compromised`; run each mechanism singly via
  `run_trace(scheme="single", custom_strategies=Mechanism)`.
- **repaired-guard counterfactual** — name-based membership against
  `os_services[os][version]`, over OSDiversity's own OS redraw.

Part B, if any of D-26/D-27 is ruled actionable, lands the regression tests these
checks imply — the gate-5 template: assert the property whose absence let the
defect survive.
