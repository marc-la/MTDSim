---
status: durable
created: 2026-07-21
updated: 2026-07-21
topic: "L3 action layer — per-verb catalogue of the inherited attacker action set (pseudocode, time cost, branch outcome, precondition), plus the FSM/coupling/patchwork figures for supervisor use"
---

# The inherited attacker action set — per-verb catalogue

**Status:** durable. A **concise, code-faithful reference** to the six-verb action
set as it stands (`SCAN_HOST`, `ENUM_HOST`, `SCAN_PORT`, `EXPLOIT_VULN`,
`BRUTE_FORCE`, `SCAN_NEIGHBOR`) — one short description and basic pseudocode per
verb, with its fixed time cost, branch outcome, and precondition. This is the
quick-lookup complement to the implementation-deep
[`action_layer_anatomy.md`](action_layer_anatomy.md): the anatomy record is the
full coupling graph / callable surface / affordance register; this catalogue is
the at-a-glance "what does each phase do, and what does it rely on."

**Ground truth.** [`mtdnetwork/operation/attack_operation.py`](../../../../mtdnetwork/operation/attack_operation.py)
(`proceed_attack` + the six `_do_*`/`_execute_*` pairs, `_handle_interrupt`,
`assert_action_context`), the host/service helpers in
[`mtdnetwork/component/host.py`](../../../../mtdnetwork/component/host.py) and
[`services.py`](../../../../mtdnetwork/component/services.py), and the durations in
[`mtdnetwork/data/constants.py`](../../../../mtdnetwork/data/constants.py)
(`ATTACK_DURATION`).

**Figures** (regenerable via
[`data/misc/_viz/attacker_fsm_viz.py`](../../../../data/misc/_viz/attacker_fsm_viz.py)):

- `data/misc/_viz/attacker_fsm_transitions.{png,svg}` — the whole state machine, all
  outcome-labelled succession arcs. Reads as heavily interconnected: every path
  returns through `ENUM_HOST`, the only forward motion is a compromise, MTD
  interrupts cut across every timed verb.
- `data/misc/_viz/attacker_fsm_dependencies.{png,svg}` — the precondition graph
  (producer → consumer of the shared adversary state). Makes the reliance on
  preceding phases explicit — no verb runs on its own.
- `data/misc/_viz/attacker_fsm_carve_patchwork.{png,svg}` — the carve as a
  patchwork decoupling: `step()` severs the hardcoded tail-call succession, but
  every precondition, the fixed timing, and interrupt recovery persist.

---

## What the action layer is

The attacker is a **six-verb finite state machine** driven inside a SimPy
discrete-event loop. Each verb consumes a fixed amount of simulated time
(`ATTACK_DURATION`, below), performs one concrete action against a target host,
and — in the native code — **hard-calls its own successor** (the "tail-call")
based on a binary/ternary outcome. There is no planner: the *order* of actions is
baked into the branch structure, not chosen. `proceed_attack` dispatches by the
adversary's `curr_process`; the `_execute_*` wrappers encode the succession.

Fixed durations (arbitrary time units, `t/u`):

| Verb            | Cost | Note |
|-----------------|------|------|
| `SCAN_HOST`     | 5    | |
| `ENUM_HOST`     | 5    | |
| `SCAN_NEIGHBOR` | 5    | |
| `SCAN_PORT`     | 25   | |
| `EXPLOIT_VULN`  | 15   | **per vulnerability**, drawn `exp(mean = vuln.exploit_time)`; not a single outer timeout |
| `BRUTE_FORCE`   | 20   | |
| `PENALTY`       | 20   | MTD-interrupt confusion delay, `exp(mean = 20)` — not a verb |

---

## 1. `SCAN_HOST` — network reconnaissance / target selection

Builds the queue of hosts to attack. Looks at everything reachable from
already-compromised hosts (plus the exposed endpoints), drops hosts on the
give-up list, orders them by hop-distance from the entry point (random
tie-breaker), and stores that as `host_stack`.

```
SCAN_HOST:                                            # cost 5 t/u
    candidates = []
    for c in compromised_hosts:
        candidates += uncompromised reachable neighbours of c
                       (must have a path from an exposed endpoint)
    order candidates by (distance_from_exposed + random())   # nearest-first, jittered
    candidates += exposed_endpoints not yet compromised
    host_stack = [h for h in candidates if h not in give_up_list]
    return (host_stack is non-empty)
        True  -> ENUM_HOST
        False -> STOP           # "cannot discover new hosts" -> attack terminates
```

- **Precondition:** none — it manufactures its own `host_stack` from network state
  (the root of the machine).
- **Limitations:** needs an existing foothold (a compromised host or exposed
  endpoint) to see anything — visibility is graph-reachability, not real scanning.
  An empty result **ends the whole run**; no wait-and-retry. Also the restart state
  after a network-layer MTD wipes the attacker's position.

## 2. `ENUM_HOST` — pick the next host off the queue

Pops the nearest host from the stack, makes it `curr_host`, resets per-host
working state, sets a pivot, and increments that host's attempt counter (feeding
the give-up rule).

```
ENUM_HOST:                                            # cost 5 t/u
    if host_stack empty: SCAN_HOST; return            # re-route, not a branch
    re-sort host_stack by distance from exposed + current pivot
    curr_host = host_stack.pop(0)
    attack_counter[curr_host] += 1
    if attack_counter[curr_host] == ATTACKER_THRESHOLD (10):
        add curr_host to give_up_list                 # targeted networks (type 0) only
    reset curr_ports, curr_vulns; set pivot host
    return (curr_host already compromised?)
        True  -> ENUM_HOST                            # re-own / loop to next
        False -> SCAN_PORT                            # begin the attack proper
```

- **Precondition:** a non-empty `host_stack` (raise re-routes to `SCAN_HOST`
  otherwise).
- **Limitations:** the loop cursor — **every** path returns here. The give-up
  threshold only feeds `give_up_list` on `network_type == 0`; other network types
  can retry a host without bound. "Already compromised" short-circuits back into
  the loop.

## 3. `SCAN_PORT` — port scan + credential-reuse check (Phase 1)

Enumerates open ports on `curr_host` (walking outward through already-exploited
services), then checks whether a stolen credential is reused here — a free
compromise if so.

```
SCAN_PORT:                                            # cost 25 t/u
    curr_ports = curr_host.port_scan()                # reachable open ports
    if curr_host.can_auto_compromise_with_users(compromised_users):
        record compromise
        return True  -> SCAN_NEIGHBOR                 # owned via reused creds
    return False    -> EXPLOIT_VULN                   # must exploit a vuln
```

- **Precondition:** `curr_host` set (by `ENUM_HOST`).
- **Limitations:** the reuse check is probabilistic and only fires if the host
  shares a username with the compromised set. `curr_ports` **must** be populated
  before `EXPLOIT_VULN` can find anything — an empty scan silently collapses the
  exploit phase into a no-op that falls straight to brute force.

## 4. `EXPLOIT_VULN` — exploit vulnerabilities (Phase 2)

Takes the vulnerabilities exposed by the scanned ports (each service pre-sorts its
vulns by **Return-on-Attack** descending), spends per-vuln exploit time attempting
each, then checks whether accumulated exploited impact crossed the host's
compromise threshold.

```
EXPLOIT_VULN(vulns):                                  # vulns sorted by RoA, unexploited
    for vuln in vulns:
        wait ~exp(mean = vuln.exploit_time)           # each vuln costs its own time
        if MTD interrupt or sim ended: return HALTED  # dispatch NOTHING
        vuln.network(host)                            # apply exploit effect
    if curr_host.check_compromised():                 # Σ exploited impact >= 7
        bump exploitability of the vulns that worked
        record compromise
        return COMPROMISED   -> SCAN_NEIGHBOR
    return UNCOMPROMISED     -> BRUTE_FORCE
```

- **Precondition:** `curr_host` set (by `ENUM_HOST`) **and** `curr_ports` populated
  (by `SCAN_PORT`); empty `curr_ports` yields no vulns and degenerates to
  `BRUTE_FORCE` silently.
- **Limitations:** the only three-way outcome (`COMPROMISED` / `UNCOMPROMISED` /
  `HALTED`). Despite a legacy "top 5" docstring, the code iterates **every**
  discovered unexploited vuln above the RoA threshold, so cost scales with vuln
  count. An MTD interrupt mid-exploit halts it (no successor) and routes recovery
  through `_handle_interrupt` (+20 t/u penalty, then `SCAN_PORT`/`SCAN_HOST`).
  Compromise is deterministic once enough impact is exploited — no defender-side
  exploit-failure modelling beyond MTD movement.

## 5. `BRUTE_FORCE` — credential brute force (Phase 3, fallback)

Last resort when exploitation failed. A single probabilistic attempt to guess a
valid login using the pool of already-compromised usernames.

```
BRUTE_FORCE:                                          # cost 20 t/u
    if random() < HOST_MAX_PROB * (matching_users / total_users):
        set compromised; record
        return True  -> SCAN_NEIGHBOR
    return False    -> ENUM_HOST                      # give up this host, take next
```

- **Precondition:** `curr_host` set (by `ENUM_HOST`).
- **Limitations:** one shot per visit — no iterative guessing; success probability
  rises only with how many of the host's users are already compromised, so a host
  with no shared users is effectively immune to this verb. Failure abandons the
  host entirely (back to `ENUM_HOST`).

## 6. `SCAN_NEIGHBOR` — lateral expansion

Runs only after a host is owned. Reads the newly-owned host's graph neighbours and
pushes them to the **front** of the queue, so the attacker fans out from fresh
footholds first.

```
SCAN_NEIGHBOR:                                        # cost 5 t/u
    found = curr_host.discover_neighbors()            # graph neighbours
    host_stack = found + [h in host_stack not already in found]
    return None  -> ENUM_HOST                         # always; no branch
```

- **Precondition:** `curr_host` set (and semantically only meaningful on a
  just-compromised host).
- **Limitations:** the only branch-free verb (always → `ENUM_HOST`). "Discovery" is
  just reading graph adjacency — no stealth, cost, or partial visibility.
  Neighbours already queued aren't re-added.

---

## The state machine as a whole

```
SCAN_HOST ──found──> ENUM_HOST ──fresh host──> SCAN_PORT ──reuse hit──────────┐
    │  (none)            │  (already owned)         │  (no reuse)              │
    ▼                    └──loop back──┘             ▼                         │
  STOP                                        EXPLOIT_VULN ──compromised──> SCAN_NEIGHBOR
                                                   │  (failed)                 │
                                                   ▼                           ▼
                                              BRUTE_FORCE ──success────────> (SCAN_NEIGHBOR)
                                                   │  (failed)
                                                   └──> ENUM_HOST
  [any timed verb] ──MTD interrupt──> PENALTY(20) ──> SCAN_PORT (app-layer)
                                                  └──> SCAN_HOST (network-layer)

  any compromise also checks "whole network owned?" -> if so, END.
```

**The interconnection, stated plainly** (see `attacker_fsm_transitions.png`):

- `ENUM_HOST` is the **hub** — every non-terminal path returns through it.
- The **only forward motion is a compromise** (the three green "= owned" edges into
  `SCAN_NEIGHBOR`); every non-compromise outcome either advances one step in a
  fixed chain or falls back to an earlier verb.
- **MTD interrupts cut across every timed verb**, adding a penalty and restarting at
  `SCAN_PORT` (application-layer MTD) or `SCAN_HOST` (network-layer MTD).
- Two terminals: `STOP` (no new hosts discoverable) and `END` (whole network
  compromised, checked at each compromise inside `update_compromise_progress`).

## Reliance on preceding phases (preconditions)

Each verb consumes shared adversary state that an earlier verb had to populate (see
`attacker_fsm_dependencies.png`). `assert_action_context` enforces these; driving a
verb out of order raises `ActionContextError`.

| Verb            | Requires (shared state) | Produced by |
|-----------------|-------------------------|-------------|
| `SCAN_HOST`     | — (seeds from network)  | — |
| `ENUM_HOST`     | `host_stack`            | `SCAN_HOST`, `SCAN_NEIGHBOR` |
| `SCAN_PORT`     | `curr_host`             | `ENUM_HOST` |
| `EXPLOIT_VULN`  | `curr_host`, `curr_ports` | `ENUM_HOST`, `SCAN_PORT` |
| `BRUTE_FORCE`   | `curr_host`             | `ENUM_HOST` |
| `SCAN_NEIGHBOR` | `curr_host`             | `ENUM_HOST` |

`ENUM_HOST` is the linchpin: four verbs need the `curr_host` it sets.

## Structural limitations of the action set

- **No agency in ordering.** The "action set" is really a fixed FSM: each verb's
  successor is determined by its outcome, not selected. The carve (`_do_*` cores +
  `step()`, below) exposes the verbs as an independently drivable set, but the six
  native verbs encode a single recon → exploit → brute-force → spread script.
- **Compromise is near-deterministic.** Given ports and vulns, `EXPLOIT_VULN`
  succeeds once summed exploited impact ≥ 7 (`SERVICE_COMPROMISED_THRESHOLD`); the
  only stochastic verbs are `BRUTE_FORCE` and the credential-reuse check. The
  defender's leverage is almost entirely MTD-induced interrupts and give-up
  thresholds, not exploit failure.
- **Visibility = graph reachability.** Every "scan" reads network structure
  directly — no false negatives, scan noise, or attacker detection.
- **Terminal fragility.** An empty `SCAN_HOST` ends the run; a host hitting 10
  attempts is blacklisted (targeted nets only). No back-off or strategy change.
- **Time is fixed per verb** (except `EXPLOIT_VULN`, per-vuln exponential); costs
  don't respond to host difficulty beyond vuln count.

## The carve is a patchwork decoupling

The controller work (`step()` + the `_do_*` cores + `assert_action_context`) is the
third lever from [`action_layer_anatomy.md`](action_layer_anatomy.md) §3.3: it lets
a controller drive the six verbs one at a time, choosing the successor itself
instead of the native tail-call choosing it. But it is deliberately **partial** (see
`attacker_fsm_carve_patchwork.png`):

- **Cut:** the hardcoded tail-call succession. Each `_do_*` core returns its branch
  outcome and dispatches nothing; the `_execute_*` wrapper that hard-called the
  successor is bypassed.
- **Intact:** the preconditions (`assert_action_context` still guards every verb),
  the shared mutable adversary state (`host_stack` / `curr_host` / `curr_ports`),
  the fixed `ATTACK_DURATION` timing, and MTD-interrupt recovery (still routed
  through the native `_handle_interrupt`).

So a driver is free to choose the next verb, yet still boxed into exactly the legal
orderings the preconditions already imposed — the coupling that made the native
ordering necessary is untouched. Removing the hardcoded ordering is not the same as
removing the dependence on it.

---

## ATT&CK / kill-chain positioning

The verbs map to ATT&CK tactics in [`action_layer_anatomy.md`](action_layer_anatomy.md)
§5 and the controller dispatch map in
[`controller.md`](controller.md); the kill-chain framing (and why the
PRE-ATT&CK side is sparsely observed) is in the CKC figures under
[`data/misc/_viz/`](../../../../data/misc/_viz/). This catalogue stays at the level
of the code verbs; those documents carry the tactic-level semantics.
