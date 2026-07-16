---
status: durable
created: 2026-07-16
updated: 2026-07-16
topic: "L3 action layer — anatomy of the inherited attack FSM (the 'before' state), its coupling graph, callable surface, affordances, and the two performance hypotheses"
---

# The action layer, as inherited — coupling graph, callable surface, affordance register, and pre-registered hypotheses

**Status:** durable. The implementation-deep, **read-only** record of the inherited
attack module *as it stands before any controller work* — the "before" state.
It is the code-level complement to the attacker's-eye account in
[`../../substrate_primer.md`](../../substrate_primer.md) §(d)/§(e): the primer says
what the attacker *is* as an adversary over the terrain; this record says what the
attacker *is as a machine* — what each verb reads, mutates, and calls next; what a
controller can and cannot invoke; what is tunable and what is welded shut.

**Two sources, kept separate** (per the guardrails' inherited-vs-editorial and
paper-vs-code rules). The attacker's *design intent* is Brown 2023
([`../../../sources/extractions/brown2023.md`](../../../sources/extractions/brown2023.md);
lit-review markdown `docs/sources/lit_review/brown2023.md`) — the flowchart, the
two scenarios, the stated realism boundary. The *implementation* is the code in
[`../../../../mtdnetwork/operation/attack_operation.py`](../../../../mtdnetwork/operation/attack_operation.py)
and [`../../../../mtdnetwork/component/adversary.py`](../../../../mtdnetwork/component/adversary.py).
Where the two diverge, both are recorded; neither is "corrected". §1 is the
reconciliation; §§2–4 are the code; §5 pre-registers what the numbers will test.

**Scope.** The action layer only. Substrate mechanics reached *through* it (how
`get_vulns` ranks by return-on-attack, how `check_compromised` sums impact) are
named at their seam and flagged substrate-side, not re-documented — those live in
[`../../mtdsim_spec.md`](../../mtdsim_spec.md) and the primer.

---

## 1. Design intent (Brown 2023) vs realisation (the code)

Brown specifies the attacker as a **flowchart** (Fig 3): a single decision
procedure, inspired by the Cyber Kill Chain and MITRE ATT&CK, that every attacker
agent follows to choose its next move (B-ATK-03). The intent is deliberately
generic — *"All attacker agents in the simulation will always follow the attack
procedure"* (Brown §V-A), and exploitation skill is explicitly **not** parameterised,
called out as future work (B-ATK-08 / B-FW-01). The flowchart is the design; the
un-differentiated single procedure is a design *commitment*, stated as such.

The code realises that flowchart as a **self-propagating, tightly-coupled state
machine over six verbs** — `SCAN_HOST`, `ENUM_HOST`, `SCAN_PORT`, `SCAN_NEIGHBOR`,
`EXPLOIT_VULN`, `BRUTE_FORCE`. The realisation adds structure the flowchart does not
mention, and that added structure — not the flowchart — is what a controller must
be built against:

| Brown's intent (Fig 3 / §III-C) | Realisation in `attack_operation.py` | Note |
|---|---|---|
| Host discovery → reconnaissance → exploit → C2/brute → next host, as a linear decision flow (B-ATK-03) | Six `_execute_*` cores, each of which **tail-calls its own successor** (`_execute_scan_host` → `_enum_host`; `_execute_enum_host` → `_scan_port`; …) | The succession is *in* the cores, not in a driver. The flowchart's arrows became hard-coded calls. |
| "The attacker will commence with the host discovery phase" (§III-C-2) | `Adversary.__init__` seeds `_curr_process = 'SCAN_HOST'`; the run calls `proceed_attack()` **once** ([`run_baseline.py:204`](../../../../baseline/run_baseline.py)) | Fire-once. After the single kick the machine drives itself — see §3. |
| Give up on a host after 10 failed attempts (B-ATK-06; Table I) | `_execute_enum_host` increments `attack_counter[host]`; at `attack_threshold` (`ATTACKER_THRESHOLD = 10`) it appends the host to `stop_attack` (marks it unattackable) **only when** `network_type == 0` **and** the host is not the target node | `network_type == 0` is the *targeted* network (`TargetNetwork`); `== 1` is the general one (`Network`). So this realises "never give up on the target" (Scenario 2) — but the give-up fires *only* in the targeted network; in the general network no host is ever given up by this path. Flagged `verify` — see §4.2. |
| Blocked by MTD → time penalty + forced re-scan (B-ATK-07; §III-D) | `_handle_interrupt` applies a `PENALTY` draw, then **hard-codes** the restart phase by MTD resource type: `network` → `_scan_host`, `application` → `_scan_port` | The three interaction classes (B-INT-01/02/03) are realised as two restart targets plus a no-op — §2.4. |
| Priority-stack vulnerabilities by return-on-attack (B-ATK-03) | Reached at the seam: `_exploit_vuln` calls `curr_host.get_vulns(curr_ports)`; the RoA ranking and top-*X* cut live substrate-side (`SERVICE_TOP_X_VULNS_TO_RETURN = 5`) | Substrate-side; named here, owned by the host/service layer. |
| One procedure, all attackers; skill not parameterised (B-ATK-08) | No per-agent parameterisation exists anywhere in the module — durations, thresholds, and orderings are module-global constants | This is the boundary the CTI-grounded controller pushes against. It is Brown's *acknowledged* limit, not a defect. |

**The load-bearing divergence.** Brown's flowchart is silent on *how phases hand
off*. The code answers that silence with tail-calls through shared mutable adversary
state — and that answer is invisible at the flowchart altitude. Reading Brown tells
you what the attacker decides; only reading the code tells you that the decisions
are welded into a machine that re-imposes its own order. The rest of this record is
that machine.

---

## 2. The coupling graph

### 2.1 How a verb is structured

Every verb is a pair: a **raise** method (`_scan_host`, `_enum_host`, …) that sets
`curr_process` and schedules a SimPy process, and an **execute core**
(`_execute_scan_host`, …) that runs *after* the verb's time cost elapses and then
tail-calls the next verb. Five of the six raises route through one wrapper,
`_execute_attack_action(time, core)`, which times out for `time`, and on completion
either (a) returns early if `end_event.triggered` (the R2-attacker termination
gate), (b) spawns `_handle_interrupt` on `simpy.Interrupt`, or (c) records the
operation and calls the core. `EXPLOIT_VULN` is the exception: it bypasses the
wrapper for its own per-vulnerability timeout loop in `_execute_exploit_vuln`.

### 2.2 Per-verb reads / mutations / tail-calls / preconditions

Read this as the adjacency list of the machine. "Mutates" is adversary state unless
noted; "tail-call" is the *only* way control leaves the core.

- **`SCAN_HOST`** (`_execute_scan_host`) — the root.
  - *Reads:* `compromised_hosts`, `stop_attack`, the hacker-visible graph, network
    neighbours, exposed endpoints, path-from-exposed.
  - *Mutates:* `pivot_host_id ← -1`; `host_stack ← discovered_hosts` (uncompromised
    reachable hosts, RoA-agnostic, sorted by distance-from-exposed + jitter, then the
    exposed endpoints, minus `stop_attack`).
  - *Tail-call:* `host_stack` non-empty → **`_enum_host`**; empty → **terminate**
    (silent return, "cannot discover new hosts").
  - *Precondition:* none. It manufactures its own `host_stack` from network state.

- **`ENUM_HOST`** (`_execute_enum_host`) — the hub.
  - *Reads:* `host_stack`, `compromised_hosts`, `pivot_host_id`, `attack_counter`,
    `attack_threshold`, target node, `network_type`.
  - *Mutates:* re-sorts and **pops** `host_stack` into `curr_host_id` / `curr_host`;
    `attack_counter[curr_host_id] += 1` (and → `stop_attack` at threshold **only** in
    the targeted network and only for non-target hosts — §1, flagged `verify` in §4.2);
    clears `curr_ports`, `curr_vulns`; sets `pivot_host_id` via `_set_next_pivot_host`.
  - *Tail-call:* `curr_host.compromised` already true → `update_compromise_progress`
    then **`_enum_host`** (loop to the next host); else **`_scan_port`**.
  - *Precondition:* **`host_stack` non-empty** — and the raise `_enum_host` enforces
    it defensively: with an empty stack it calls **`_scan_host`** instead. This is the
    coupling the motivation flagged — *`ENUM_HOST` pops a stack only `SCAN_HOST` fills.*

- **`SCAN_PORT`** (`_execute_scan_port`) — surface recon.
  - *Reads:* `curr_host`, `compromised_users`.
  - *Mutates:* `curr_ports ← curr_host.port_scan()`.
  - *Tail-call:* credential reuse hits (`can_auto_compromise_with_users`) →
    `update_compromise_progress` then **`_scan_neighbors`** (return); else
    **`_exploit_vuln`**.
  - *Precondition:* `curr_host` set (non-`None`). Set only by `ENUM_HOST`.

- **`EXPLOIT_VULN`** (`_execute_exploit_vuln`) — the compromise attempt.
  - *Reads:* `curr_host`, `curr_ports` (via `get_vulns(curr_ports)` in the raise),
    each vuln's `exploit_time`.
  - *Mutates:* per vuln, `vuln.network(host)` (marks exploited) and
    `curr_attempts += 1`; on success, bumps `vuln.exploitability` and records a
    scorer entry.
  - *Tail-call:* `curr_host.check_compromised()` → `update_compromise_progress` then
    **`_scan_neighbors`**; else **`_brute_force`**.
  - *Precondition:* `curr_host` set **and** `curr_ports` populated. `curr_ports` is set
    only by `SCAN_PORT`; with it empty, `get_vulns([])` yields no vulns, the loop is a
    no-op, `check_compromised()` fails, and control falls to `_brute_force` — a silent
    degeneration, not an error (see §3.3).

- **`BRUTE_FORCE`** (`_execute_brute_force`) — the fallback.
  - *Reads:* `curr_host`, `compromised_users`.
  - *Mutates:* via `curr_host.compromise_with_users` (may compromise the host).
  - *Tail-call:* success → `update_compromise_progress` then **`_scan_neighbors`**;
    failure → **`_enum_host`** (abandon this host, take the next).
  - *Precondition:* `curr_host` set.

- **`SCAN_NEIGHBOR`** (`_execute_scan_neighbors`) — post-compromise expansion.
  - *Reads:* `curr_host.discover_neighbors()`, `host_stack`.
  - *Mutates:* `host_stack ← found_neighbors + existing` (new neighbours pushed to the
    front).
  - *Tail-call:* **`_enum_host`**, always.
  - *Precondition:* `curr_host` set and just compromised (it is only ever reached
    after an `update_compromise_progress`).

**Shared-state channels (the coupling substrate).** The verbs never pass arguments to
each other; they communicate entirely through adversary fields:
`host_stack` (the work queue — filled by `SCAN_HOST`/`SCAN_NEIGHBOR`, drained by
`ENUM_HOST`), `curr_host_id`/`curr_host` (the cursor — set by `ENUM_HOST`, read by all
of `SCAN_PORT`/`EXPLOIT_VULN`/`BRUTE_FORCE`/`SCAN_NEIGHBOR`), `curr_ports` (set by
`SCAN_PORT`, read by `EXPLOIT_VULN`), `curr_vulns`, `pivot_host_id`,
`attack_counter`/`stop_attack`, and `compromised_hosts`/`compromised_users`. Every
precondition above is a statement about which of these a verb assumes is already
populated. **No verb validates its inputs; the call order is the only guarantee.**

### 2.3 The termination condition

`update_compromise_progress` is the single win test: whenever it records a newly
compromised host it calls `network.is_compromised(compromised_hosts)`, and on success
fires `end_event.succeed()`, ending the run. There is no other terminal state except
`SCAN_HOST` exhausting the network (empty `host_stack` → silent return). The
commented-out `target_compromised` block shows an earlier target-only termination that
is no longer wired.

### 2.4 The transition diagram (with the interrupt and terminal edges)

```
                   proceed_attack()  [fired once; dispatches on curr_process]
                          │
                          ▼
   ┌──────────────► SCAN_HOST ──(stack empty)──► TERMINATE (no hosts)
   │                    │
   │              (stack non-empty)
   │                    ▼
   │  (stack empty ► ENUM_HOST ◄─────────────────────┐  (re-routes to SCAN_HOST
   │   re-route)        │                            │   if stack empty)
   │                    ├──(curr_host already compromised)──► loop ENUM_HOST
   │            (fresh host)                          │
   │                    ▼                             │
   │               SCAN_PORT ──(cred reuse)──► SCAN_NEIGHBOR ──► ENUM_HOST
   │                    │                             ▲
   │             (no reuse)                           │
   │                    ▼                             │
   │             EXPLOIT_VULN ──(compromised)─────────┤
   │                    │                             │
   │              (not compromised)                   │
   │                    ▼                             │
   │              BRUTE_FORCE ──(compromised)─────────┘
   │                    │
   │              (failed) ──► ENUM_HOST
   │
   │   ┌───────────────────────────────────────────────────────────┐
   └───│  _handle_interrupt (on simpy.Interrupt, after PENALTY draw): │
       │   MTD resource == 'network'      → clear curr_host → SCAN_HOST │
       │   MTD resource == 'application'  → keep curr_host  → SCAN_PORT │
       │   MTD resource == 'reserve'/user → (no interrupt raised)       │
       └───────────────────────────────────────────────────────────┘
```

The interrupt is raised by the defender, not the attacker: `mtd_operation.py`'s
`_interrupt_adversary` calls `attack_process.interrupt()` for a `network`-layer
mutation against *any* live phase, and for an `application`-layer mutation **only**
when `curr_process ∉ {SCAN_HOST, ENUM_HOST, SCAN_NEIGHBOR}` (i.e. only the
surface-dependent phases `SCAN_PORT`/`EXPLOIT_VULN`/`BRUTE_FORCE`). A `reserve`/user
mutation raises no interrupt at all. This is the code-level embodiment of the primer's
reset model (§(e)): position-mutation throws the attacker back to discovery;
surface-mutation throws it back to port re-enumeration on the *same* still-owned host;
credential-mutation does not interrupt the action chain.

**Verdict: the graph is strongly coupled and self-driving.** Every core has exactly
one place it can send control, chosen by a local success test; there is no dispatcher
that could send it elsewhere. `SCAN_HOST` and `ENUM_HOST` are mutually reachable, and
every compromise routes back through `ENUM_HOST`, so the six verbs form one strongly
connected component with `ENUM_HOST` as its hub.

---

## 3. The callable surface

### 3.1 The decisive fact — fire-once, not step-callable

`proceed_attack()` is called **exactly once** per run, from the harness, and it does
nothing but dispatch to the raise matching the adversary's *current* `curr_process`
(seeded `SCAN_HOST`). After that single call the machine runs itself to termination or
interrupt via the tail-calls in §2. **There is no external driver loop that pulls one
phase at a time.** This is the central constraint on any controller: the action layer
is not a library of independently-callable verbs — it is a machine you start.

Consequently a controller has, without touching `mtdnetwork/`, exactly two levers:

1. **Choose the entry phase.** Set `curr_process` and call `proceed_attack()` to enter
   the chain at a chosen verb. But entry does not buy *ordering* — the entered verb
   tail-calls its native successor, and the machine proceeds in its own order from
   there. You choose where the ball is dropped; the slope is fixed.
2. **Pre-populate the shared state a verb assumes.** Because preconditions are
   unvalidated, a controller can synthesise `host_stack`, `curr_host`, `curr_ports`
   etc. before entering. This is how a mid-chain verb is made to run at all — and it is
   also how a controller would have to *simulate* an order the tail-calls do not offer.

### 3.2 Per-verb classification

Classifying each verb by what a controller must do to invoke it in isolation:

| Verb | Class | What invocation requires |
|---|---|---|
| `SCAN_HOST` | **callable-as-is** | Nothing. It is the root; it builds its own `host_stack` from network state. |
| `ENUM_HOST` | **callable-with-context** | A non-empty `host_stack`; otherwise the raise re-routes to `SCAN_HOST` (a no-op as a standalone call). |
| `SCAN_PORT` | **chain-bound** | `curr_host` set. With `curr_host = None` the core throws on `port_scan()`. |
| `EXPLOIT_VULN` | **chain-bound** | `curr_host` **and** `curr_ports` set. With `curr_ports` empty it degenerates to `BRUTE_FORCE` silently. |
| `BRUTE_FORCE` | **chain-bound** | `curr_host` set. |
| `SCAN_NEIGHBOR` | **chain-bound** | `curr_host` set (and semantically only meaningful on a just-compromised host). |

Only `SCAN_HOST` is a clean entry point. `ENUM_HOST` is callable if its queue is
pre-filled. The other four are chain-bound: they assume a cursor (`curr_host`) and,
for `EXPLOIT_VULN`, a working set (`curr_ports`) that only the *preceding* verb
produces.

### 3.3 Reordering freedom — the honest ceiling

**A controller has essentially no reordering freedom over the verbs as written.** The
tail-calls hard-code succession, so any order a controller imposes at entry is
overwritten by the machine within one step. Three concrete outcomes, all verified
against the code:

- **Safe (native) orders only.** The sole orders that run without state synthesis are
  the ones the tail-calls already produce. "Impose a different order" reduces to
  "choose an entry phase and then watch the native order resume".
- **No-op degenerations.** Enter at `ENUM_HOST` with an empty `host_stack` → the raise
  bounces to `SCAN_HOST`. Enter at `EXPLOIT_VULN` with empty `curr_ports` → the vuln
  loop does nothing and control falls to `BRUTE_FORCE`. The machine quietly returns to
  its own path rather than honouring the requested phase.
- **Breaks.** Enter at any chain-bound verb with `curr_host = None` → an
  `AttributeError` inside the substrate. These are not graceful refusals; they are
  crashes, because nothing validates the precondition.

**The carve, specified (not performed).** To make a verb genuinely orderable, its
*executable core* must be separated from its *tail-call*. Concretely, each
`_execute_*` would split into a pure action (do the scan / attempt the exploit, mutate
state, return an outcome) and a separate successor-selection the controller owns —
i.e. delete the trailing `self._<next>()` from every core and return its branch
condition instead, letting a controller (the net/movement layer) decide the next verb.
This is the minimal change that converts the machine into a callable surface. **It is
specified here and belongs to the build, gated on Marc's review — not done in this
record** (hard constraint: the action layer is read, never edited).

---

## 4. Affordance and limitations register

### 4.1 Tunables the action layer exposes

Every knob a per-tactic controller could turn *without* editing behaviour, with its
location. All are module-global (Brown's un-differentiated design, B-ATK-08), so
tuning them is uniform across the run unless a controller sets them per invocation.

| Tunable | Location | What a controller could legitimately do |
|---|---|---|
| `ATTACK_DURATION` (per-verb times: `SCAN_HOST/ENUM_HOST/SCAN_NEIGHBOR = 5`, `SCAN_PORT = 25`, `EXPLOIT_VULN = 15`, `BRUTE_FORCE = 20`) | [`constants.py:140`](../../../../mtdnetwork/data/constants.py) | Set per-tactic tempo — a "slow, careful" profile lengthens recon/exploit times; a "fast" profile shortens them. This is the cleanest lever for the low-and-slow contrast the thesis needs. |
| `PENALTY = 20` (the MTD confusion penalty, drawn `exponential_variates(PENALTY, 0.5)`) | `constants.py:147`, applied in `_handle_interrupt` | Model how badly a class is set back by a mutation. |
| `ATTACKER_THRESHOLD = 10` (per-host give-up cap) | `constants.py:106` | Set a class's persistence — a patient class raises it. Caveat: the give-up it drives (`stop_attack`) only fires in the targeted network, and the target-node exception is already wired (§4.2). |
| `HACKER_ATTACK_ATTEMPT_MULTIPLER = 5` (→ `max_attack_attempts = 5 × nodes`) | `constants.py:102`, read in `Adversary.__init__` | Global effort ceiling; currently the cap is computed but the enforcing block is commented out — see §4.2. |
| `SERVICE_TOP_X_VULNS_TO_RETURN = 5`, `roa_threshold` | `constants.py:95`; reached via `curr_host.get_vulns(curr_ports)` | RoA selectivity of the exploit set. **Substrate-side** (host/service layer) — reachable through the seam but not owned by the action layer. |
| `EXPLOIT_VULN` timing model (`exponential_variates(vuln.exploit_time(host), 0.5)`) | `_execute_exploit_vuln` | Per-vuln, CVSS/complexity-priced; a controller cannot re-price a vuln but can choose whether to enter `EXPLOIT_VULN` at all. |

### 4.2 Wanted-but-absent affordances (named limitations)

Each is a controller capability the current action layer *cannot* express without a
behaviour edit — the honest ceiling of the tactic→action map, and direct
future-work material (ch4 design constraints / ch6 future work).

- **Per-invocation scan boosting is impossible.** A verb's duration is read from the
  module-global `ATTACK_DURATION` at schedule time; there is no per-call parameter. A
  controller cannot say "this class scans faster *at recon* and slower *at
  exploitation*" within one run without either mutating the global between phases
  (a race across the single shared adversary) or a carve that threads a duration
  argument. *Cost:* small if the carve in §3.3 is taken (add a `time` parameter to the
  raises); impossible without it.
- **Per-tactic exploitation care is not expressible.** "Slower, careful exploitation"
  vs "smash-and-grab" differs only in the exploit-time draw and the give-up threshold,
  both module-global. Without per-invocation parameters a class cannot carry its own
  exploitation temperament.
- **No branch override.** A controller cannot make `SCAN_PORT` proceed to
  `SCAN_NEIGHBOR` instead of `EXPLOIT_VULN`, or make `EXPLOIT_VULN` retry instead of
  falling to `BRUTE_FORCE` — the branch is decided inside the core by a substrate test.
  Expressing a different policy requires the §3.3 carve.
- **The give-up rule is only half-wired — flagged `verify`.** Two give-up mechanisms
  exist, and neither is active in the general scenario. The per-host `stop_attack` list
  is populated **only** in the targeted network (`network_type == 0`, non-target hosts);
  in the general network (`network_type == 1`) no host is ever given up by this path. The
  global `max_attack_attempts` ceiling is computed in `Adversary.__init__` but its
  enforcement is commented out in both `_execute_enum_host` and `_exploit_vuln`. So a
  general-scenario attacker, as inherited, does **not** honour Brown's "give up after 10"
  (Table I) — whether that is an intended divergence or a defect is an
  inherited-vs-editorial disposition for Marc, recorded here, not resolved (guardrails:
  don't guess a disposition). A controller relying on the give-up affordance in §4.1
  must know it only bites in the targeted network today.
- **Substrate-side wants (out of boundary — D5).** Re-pricing a vulnerability,
  changing what `check_compromised` sums, or making credentials revocable are
  substrate-behavioural and fall outside the attacker-only boundary; named here,
  flagged as future work, not actioned.

---

## 5. Two performance hypotheses — pre-registered, kept distinct

Two mechanisms could explain a profiled/APT attacker underperforming the inherited
baseline on the substrate's metrics. They are **different mechanisms with different,
separable result signatures**, and the provenance of each is kept distinct
(guardrails: inherited-vs-editorial). The first numbers
([`../../../handoffs/2026-07-15_l3_first_numbers.md`](../../../handoffs/2026-07-15_l3_first_numbers.md))
are to be read against this section.

- **H-metric — the metrics don't reward APT-shaped behaviour.** *Provenance:*
  supervisor-registered, M8, 2026-07-14 working session
  ([`supervisor_decision_register.md`](supervisor_decision_register.md) §M8). *Claim:*
  the profiled attacker genuinely behaves differently (spends effort on
  evasion/stealth-shaped behaviour) but the current metrics — geared to the smash-and-grab
  baseline — do not credit it, so it scores no better. *Result signature:* profiled
  behaviour **differs** from baseline in the observable action sequences / target
  selection / timing, **yet** MTTC and attack-success land at or below baseline. The
  behaviour is visible; the scoreboard is blind.

- **H-coupling — the action layer resists reordering.** *Provenance:* Marc's
  hypothesis, 2026-07-16, recorded in the anatomy handoff. *Claim:* the coupling
  documented in §2–§3 forces the controller back toward the FSM's native sequence, so
  the net-imposed order degenerates into the tail-call order and the classes lose the
  distinguishability the pipeline exists to add — the anti-goal
  ([`binding_design_space.md`](binding_design_space.md)) reached through the back door.
  *Result signature:* profiled action sequences are **near-identical** to baseline
  (the imposed order collapsed), and MTTC ≈ baseline for that reason.

**The discriminator is one observable: do the action sequences differ from baseline?**
If they differ but the numbers do not move → H-metric (behaviour is real, metrics
miss it). If they do not differ → H-coupling (the machine flattened the behaviour).
The two are not mutually exclusive — coupling could flatten *some* of the divergence
while metrics miss the rest — so the reading is *which dominates*, evidenced by how
much of the profiled behaviour survives as a visible sequence difference. Both must be
on the record before the numbers arrive, so neither is retrofitted to whatever the
first run shows.

---

## 6. What this establishes, and where it connects

This record turns "the action layer is suspected to be a strongly-coupled FSM" into a
diagram with named edges (§2.4), a per-verb precondition ledger (§2.2), a callability
classification (§3.2), a stated reordering ceiling (§3.3), a tunable/limitation
register (§4), and two falsifiable hypotheses (§5). Its practical output for the build:
the controller layer is **"the best we can do with the tools at hand"**, and §3–§4 are
the honest inventory of those tools — either the controller drives the machine by
entry-phase + state synthesis (no carve, minimal change, low reordering freedom), or
the §3.3 carve is taken (more change, genuine callability). That decision, and any
carve, are gated on Marc's review.

- **Complements:** [`../../substrate_primer.md`](../../substrate_primer.md) §(d) (the
  attacker as adversary) and §(e) (the reset model this record's §2.4 embodies).
- **Feeds:** the tactic→action influence map
  ([`../../../handoffs/2026-07-15_l3_tactic_action_influence_map.md`](../../../handoffs/2026-07-15_l3_tactic_action_influence_map.md)),
  whose per-pair verdicts are only meaningful once callability (§3) is known; and the
  feedback-net design
  ([`../../../handoffs/2026-07-15_l3_feedback_net_design.md`](../../../handoffs/2026-07-15_l3_feedback_net_design.md)).
- **Speaks to:** the anti-goal / distinguishability bar in
  [`binding_design_space.md`](binding_design_space.md) — §5's H-coupling is that
  anti-goal reached from the action-layer side.
- **Intent source:** [`../../../sources/extractions/brown2023.md`](../../../sources/extractions/brown2023.md)
  (B-ATK-01…08, B-INT-01…03, B-FW-01).
- **Reading:** [`attack_operation.py`](../../../../mtdnetwork/operation/attack_operation.py),
  [`adversary.py`](../../../../mtdnetwork/component/adversary.py),
  [`constants.py`](../../../../mtdnetwork/data/constants.py),
  [`mtd_operation.py`](../../../../mtdnetwork/operation/mtd_operation.py) `_interrupt_adversary`.

## When this would need updating

- If the §3.3 carve is taken — the callability classification (§3.2) and the
  reordering ceiling (§3.3) are re-derived against the carved surface.
- If the first numbers arrive — §5's hypotheses are resolved (which mechanism
  dominates), and the record is annotated with the verdict rather than rewritten.
- If the interrupt restart targets or the tail-call succession change in
  `attack_operation.py` — §2 is re-walked (it is a code snapshot, dated in the
  frontmatter).
