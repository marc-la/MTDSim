---
status: durable
created: 2026-09-30
topic: "How one MTD deployment disrupts each attacker, verified against the current code, and the two disruption metrics that follow from it (attack actions blocked; time to resume a blocked action), with dry runs, worked examples and the rulings they need"
---

# How an MTD deployment disrupts each attacker, and the metric that follows

**Why this exists.** Marc, 2026-09-30, on §4.5 round 5: the compromise rate after
an MTD deployment is "so lost … structurally broken"; "we haven't thought through
how disruption occurs in the APT attacker and how it occurs in the baseline
attacker. Once we do, the path forward for a clear metric will become obvious";
and of Figure 5.3, "I cannot derive what you did". This record does the mechanism
first (section 1, evidence in section 6), then derives the metric from it
(sections 2–4). It extends [`disruption_wiring.md`](disruption_wiring.md)
(2026-08-05), whose three channels still hold, with what changed since.

## 1. The mechanism, in the thesis's terms

A deployment acts at the moment it **completes** (its 70–110 s run changes
nothing until then). At that moment three things happen, on both attackers:

1. **The block.** The action the attacker is running is cut off: it ends and
   does not take effect. This is Brown's *attack action blocked* (§III-D: the
   MTD cuts off something the action needed). Only the action in flight is
   blocked. Nothing before or after it is.
2. **The penalty.** The attacker waits about 20 s. It is the same on both
   attackers and every mechanism.
3. **The lost position** (host layer only: IP, complete-topology and
   host-topology shuffle). The attacker loses the host it was working on.

What follows is **recovery**, and here the two attackers differ:

| | Baseline attacker | APT attacker model |
|---|---|---|
| host layer | re-runs scan host → enumerate host → scan port; back on the same host at about 30 s and working on it at about 55 s; nothing later fails | its tactics keep dispatching host actions that cannot run (precondition unmet: 6–9 of them, against 0 with no MTD) until lateral movement restores its position; it runs a host action again only about 375–456 s after the deployment |
| service layer | re-runs scan port; back at about 45 s, **but the exploit progress it had on the host is erased**, so its next compromise comes 2.6× later (640 s against 247 s) | loses no position; nothing is blocked; it pays only through later exploit outcomes |
| user shuffle | interrupts only brute force | the same |

IP shuffle's own write (the host's address) is read by nothing either attacker
does: its whole effect is the block, the penalty and the lost position.

**So a deployment costs an attacker in two ways.** It costs **time**: the attacker
must get back to the work it was doing. And on the service layer it can cost
**progress**: the work is undone. Time is disruption; progress undone shows in
the attack outcome.

## 2. The metrics this gives

**One base event, two readings, no windows, no ratios, no pooled rates.**

- **Attack actions blocked** (Brown 2023, cited): the actions a deployment cuts
  off in flight, **per deployment**. APT model: a record with outcome
  `MTD_INTERRUPT`. Baseline: a record with `interrupted_in` set. An interrupt on
  a dwell-only tactic, or on a dispatch whose precondition was already unmet, cuts
  off no action and is not counted.
- **Time to resume a blocked action** (introduced; the name says what it does):
  from the moment the deployment completes to the start of the attacker's next
  run of the same action that runs on the network. Reported as the median over
  the blocked actions, beside the attacker's **usual gap** between two runs of the
  same action with no MTD. A blocked action never run again counts as longer than
  every resumed one.

This answers Marc's question "what do you count as a blocked action — the tactics
it visits before it comes back?". The blocked action is the one in flight. The
tactics it visits afterwards are the recovery, and their length is the time to
resume.

**What the pair does not record, stated:** progress the deployment undoes (the
baseline's erased exploit progress under service and OS diversity). That is an
outcome, and ASP reduction and NCR reduction record it (baseline, service
diversity: ASP reduction +0.67, NCR reduction +0.30; handoff ruling L).

**Why the compromise rate after an MTD deployment goes.** It measures disruption
through compromises, the rarest event in a run. It therefore has to pool across
thousands of deployments and compare windows before and after, which is what made
it opaque. Its one strength, seeing lasting cost, is already carried by ASP and
NCR reduction.

## 3. Worked examples (from the committed corpus; checkable by hand)

`data/results/ch5_defended/runs.jsonl`, IP shuffle at 2 000 s.

**Baseline attacker, seed 1.** The deployment completes at 6 102.0 s.

```
SCAN_PORT      6097.8–6102.0  interrupted (network)   <- the blocked action
               (20 s penalty: no record)
SCAN_HOST      6122.0–6127.0
ENUM_HOST      6127.0–6132.0
SCAN_PORT      6132.0–6157.0                          <- the same action runs again
```
Time to resume = 6 132.0 − 6 102.0 = **30 s**.

**APT attacker model, seed 0.** The deployment completes at 6 103 s.

```
discovery          SCAN_PORT     MTD_INTERRUPT        6061.4–6123.9   <- blocked (the record carries the 20 s penalty)
impact             (dwell only)                       6123.9–6140.8
discovery          SCAN_PORT     PRECONDITION_UNMET   6140.8–6175.2   <- dispatched, cannot run
stealth            (dwell only)                       6175.2–6196.6
execution          EXPLOIT_VULN  PRECONDITION_UNMET   6196.6–6232.2   <- dispatched, cannot run
lateral-movement   ENUM_HOST     success              6232.2–6233.7   <- position restored
credential-access  BRUTE_FORCE   failure              6233.7–6236.8
lateral-movement   ENUM_HOST     success              6236.8–6237.6
discovery          SCAN_PORT     success              6237.6–6254.3   <- the same action runs again
```
Time to resume = 6 237.6 − 6 103 = **135 s**, with two dispatches on the way
that could not run. (This run is on the aggregate profile; the cell figures
below pool $c_1$–$c_4$.)

## 4. Dry run (100 seeds, 2 000 s interval, $c_1$–$c_4$ pooled)

`data/results/s45_metric_redesign/disruption_from_mechanism.py`; preview
`preview_fig53_resume.png` beside it. Deployments are counted while the attacker is
still acting.

Usual gap between two runs of the same action with no MTD: **APT 136 s**,
**baseline 93 s**.

| mechanism | APT: blocked per deployment | APT: time to resume (median) | baseline: blocked per deployment | baseline: time to resume (median) |
|---|--:|--:|--:|--:|
| IP shuffle | 0.35 | 464 s | 1.00 | 55 s |
| complete topology shuffle | 0.38 | 394 s | 1.00 | 55 s |
| host topology shuffle | 0.39 | 387 s | 1.00 | 55 s |
| port shuffle | 0.16 | 167 s | 0.95 | 45 s |
| OS diversity | 0.15 | 161 s | 0.95 | 45 s |
| service diversity | 0.15 | 156 s | 0.96 | 45 s |
| user shuffle | 0.01 | 169 s | 0.07 | 93 s |

**How it reads.**
- The baseline is always running an action, so almost every deployment blocks
  one. The APT model is in a dwell-only tactic much of the time, so a deployment
  catches an action in only 15–39 % of cases.
- Blocked on the host layer, the APT model takes about three times its usual gap
  to run the action again. This is the retrace the failure matrix produces.
  Blocked on the service layer, it resumes at about its usual gap: the block costs
  it nothing more.
- The baseline resumes within a minute from every mechanism, sooner than its own
  usual gap, because its procedure restarts at once.

**Proposed Figure 5.3** (the preview): (a) host layer, (b) service layer, the share
of blocked actions run again against time since the deployment, each attacker
beside its usual-gap curve with no MTD; (c) the median time to resume per
mechanism, with the two usual gaps as reference lines. Attack actions blocked per
deployment goes in the table beside it.

## 5. Rulings for Marc (recommendation first)

**M1. Replace the compromise rate after an MTD deployment with the time to resume
a blocked action; keep attack actions blocked, now per deployment.** Draft for
§4.5.3, not applied (another session holds §4.5):

```latex
\paragraph{Attack actions blocked.}
Attack actions blocked is Brown's count of the attacker's actions that MTD blocks
\citep[Sec.~IV-A]{brown2023}: the actions a deployment cuts off while they run
(Section~\ref{subsec:runtime-mechanics}), per deployment. A deployment that lands
while the attacker is in a tactic with no action blocks nothing.

\paragraph{Time to resume a blocked action.}
After a block the attacker must get back to the work it was doing. Time to resume
a blocked action is the time from the deployment's completion to the start of the
attacker's next run of the same action, reported as the median over the blocked
actions beside the attacker's usual gap between two runs of the same action with
no MTD. A blocked action the attacker does not run again counts as longer than
every resumed one. What a deployment undoes, such as exploit progress on a host,
shows in ASP reduction and NCR reduction instead.
```

**M2. "Condition" → "the MTD".** Marc: "what is the condition … why don't we just
say MTD mechanism". A condition is no MTD, one MTD mechanism alone, the random or
the alternative deployment strategy, or MTDShield (Table 5.1), so *MTD mechanism*
would misname three of them. Recommend defining once in the §4.5 preamble: "an
*MTD* is one MTD mechanism deployed alone, a deployment strategy over the seven,
or MTDShield (Table 5.1)". Then "ASP under the MTD" pairs with the ratified "no
MTD". Where only single mechanisms apply (the two metrics above are read per
mechanism), say *MTD mechanism*.

**M3. Fix two analyser defects before chapter 5 is regenerated** (both found in
this pass, section 6 D):
- The baseline's `termination_time` is always the 15 000 s horizon, even when its
  target fell earlier. `disruption.py` counts that dead time as live time: 59 of
  157 IP-shuffle deployments in the sample landed after the baseline had
  finished. This biases the current Figure 5.3's baseline curves. Check every
  other reader of `termination_time` on the baseline arm.
- `blocked_resume.py` measured resume time from the blocked record's end. That end
  includes the 20 s penalty on the APT model but not on the baseline. The new
  script measures from the deployment's completion on both.

**Also flagged, not actioned:** the unified tracer prints "ran for all of it" for
an interrupted action (`src/mtdsim/l3_simulation/trace.py:387-390`), which never
ran.

## 6. Evidence: the mechanism, verified against current code

The session's code audit follows, unchanged, with file:line for every claim. Its
"measured" numbers come from an 800-run scratch regeneration (20 seeds) and are
indicative. The table in section 4 is from the committed corpus.


Worktree `/home/marc/GitHub/MTDSim-disruption`, branch `chore/disruption-mechanism` at `1785cf99`, read 2026-09-30.
Every locator is `path:line` in that tree. "Measured" numbers come from a scratch regeneration
(`run_corpus.dispatch`, the core-group configuration: v2_partial, v4_failure_only, retrace on,
fresh-host contract on, targeted objective, shifted regime, 15 000 s horizon; 20 seeds, the four
profiles and the baseline, each single mechanism at the **2 000 s** interval plus no MTD; 800 runs,
a scratch file not kept). They are indicative, not corpus numbers.

### 0. What changed since `disruption_wiring.md` (2026-08-05)

- **The pool is seven, not four** (`d127f443`, 2026-08-27): HostTopologyShuffle, PortShuffle, UserShuffle are live; `run_corpus.py:63-82` runs each alone.
- **The OS gate is back** (D-19, same commit): `services.py:165-167`. An OS-specific vulnerability on a host of another OS is refused with no roll and counts as an attempt. OS diversity now reaches exploitation (the record's diversity numbers predate this).
- **UserShuffle has an interrupt class** (`reserve`): it interrupts only BRUTE_FORCE (`mtd_operation.py:246-264`), and the baseline then restarts at EXPLOIT_VULN (`attack_operation.py:255-264`; D-07).
- **The fresh-host contract** (`ce8739ad`, 2026-08-30) is on in the corpus (`run.py:297`). It changes what the APT model does with an owned cursor. It does **not** help after a cleared cursor, because the guard fires only when `curr_host` is set and owned (`attacker.py:790-792, 865`). See C(iv).
- **Still open, unchanged in code:** D-36, the lost cursor clear when a network mutation arrives during an application penalty (`attack_operation.py:222-224` reads the MTD it was called with). It cannot arise under a single-mechanism condition. D-35: the APT model's exploit is one interrupt window (`attack_operation.py:862`). D-37: no record row carries the penalty.

### A. What each deployment changes, and whether anything the attacker does later reads it

Common facts:
- The write lands when the deployment **completes**: first the execution timeout (`mtd_operation.py:180-181`; means `constants.py:128-136`), then the write (`:188`), then the record (`:197`), then the interrupt (`:199`). Nothing changes during the ~70-110 s the deployment runs.
- **No mechanism un-compromises a host.** Nothing writes `host.compromised` or removes an id from `_compromised_hosts`. HostTopologyShuffle remaps the ids and keeps the instances owned (`adversary.py:129-147`).
- Every mechanism except CompleteTopologyShuffle skips the five internet-facing hosts (`ipshuffle.py:18-19`, `hosttopologyshuffle.py:37`, `osdiversity.py:20-21`, `portshuffle.py:22-23`, `servicediversity.py:16-17`, `usershuffle.py:21-22`; D-23).

| Mechanism (class) | Fields written | Later attacker reads that can fail because of it | Verdict |
|---|---|---|---|
| IPShuffle (network) | `host.ip` (`ipshuffle.py:22`), scorer feed (`:25`) | **None.** No attacker path reads `.ip`. The only readers are the tracer (`trace.py:439`), the MTD-AI observers (`mtd_ai_operation.py:459`, `mtd_ai_training.py:322`) and the scorer refresh in CTS/HTS. | **Reaches nothing.** Its whole effect is the interrupt: the penalty, the cursor clear, and the baseline's forced restart. |
| CompleteTopologyShuffle (network) | Every edge is regenerated, and hosts are re-attached at their ids (`completetopologyshuffle.py:19-21`). `reachable` is rebuilt from the exposed endpoints through owned hosts only (`:22` → `network.py:699-733`). | SCAN_HOST's queue and ENUM_HOST's visibility filter (`attack_operation.py:266-292, 323-331`) read the new graph. An owned host cut off from the endpoints stops giving visibility. SCAN_NEIGHBOR returns new neighbours (`host.py:428-436`). | Reaches the attacker **through the queue**: fewer or different visible targets, and queued targets dropped by the D-28 guard (`attack_operation.py:396-407`). |
| HostTopologyShuffle (network) | Instances swap ids within a layer (`hosttopologyshuffle.py:46-50`). The adversary's id-keyed state is remapped (`adversary.py:136-147`). `reachable` is rebuilt (`hosttopologyshuffle.py:62`). | The same visibility reads as CTS. The attacker's knowledge follows the instances, so what changes is the neighbourhood. | Reaches the attacker **through the queue**, less than CTS: only non-endpoint hosts move, and only within a layer. |
| PortShuffle (application) | Every non-target service node's `port` on internal hosts (`portshuffle.py:24-32`) | EXPLOIT_VULN maps the attacker's scanned `curr_ports` to services by the **current** port numbers (`host.py:312-315`). Stale ports match only the host's own exposed services, which are always re-added (`host.py:299-301`). | **APT model only**, through a later exploit's outcome: its cursor and `curr_ports` survive, so the next exploit on stale ports sees fewer services and fewer vulnerabilities. The baseline always re-scans first (B(iii)), so for the baseline only the interrupt reaches it. |
| OSDiversity (application) | `os_type` and `os_version` (`osdiversity.py:28-29`). Services incompatible with the new OS are redrawn (`:31-44`). | The OS gate refuses OS-specific vulnerabilities (`services.py:165-167`). A redrawn service is unexploited, so progress inside the host is lost on it. `port_scan` only walks inward through exploited services (`host.py:345`), and compromise needs an exploited service next to the target node (`host.py:421-425`). | Reaches **both** attackers through later exploit outcomes: refusals, and lost progress inside the host. |
| ServiceDiversity (application) | Every non-target service on internal hosts is redrawn (`servicediversity.py:18-30`) | The same reads: every partially exploited host loses its progress, and every vulnerability list is new. | Reaches **both** through later exploit outcomes. Owned hosts stay owned. |
| UserShuffle (reserve) | Each internal host's user set, drawn from the same pool (`usershuffle.py:23-28`). Harvested credentials stay valid (D-02). | The credential-reuse check inside SCAN_PORT (`host.py:143-161`) and the BRUTE_FORCE probability (`host.py:166-182`) | Reaches both through **probabilistic** outcomes, in either direction. It interrupts only BRUTE_FORCE. |

### B. The baseline attacker (`mtdnetwork/operation/attack_operation.py`)

**(i) Which actions a deployment catches.** The gate is `_interrupt_adversary` (`mtd_operation.py:217-264`). It needs a live process (`:222`):
- network class: any of the six actions (`:223-231`);
- application class: every action except SCAN_HOST, ENUM_HOST and SCAN_NEIGHBOR (`:232-245`);
- reserve class: BRUTE_FORCE only (`:246-264`).

The baseline's process is dead in three cases, so it cannot be caught then:
- during its own penalty, which runs in a separate process (`attack_operation.py:107`);
- after it gives up for good, when SCAN_HOST finds nothing (`:355-361`);
- after the objective, when the actions stop past `end_event` (`:110-111`).

Measured over live deployments: the host layer catches 100%, the service layer 92-95%, UserShuffle 3%. EXPLOIT_VULN takes 66-78% of the hits, because the baseline's exploit is long: one timeout per vulnerability (`:543-546`), 60-140 s per attempt in the traces.

**(ii) What the interrupt does.**
- The in-flight timeout raises. The action's core never runs (`:105-108`). For EXPLOIT_VULN, the rolls already made on earlier vulnerabilities stand (`:547-554`).
- `_handle_interrupt` writes one row for the verb with `interrupted_in` = the class and `interrupted_by` = the name (`:233-235`; `attack_statistics.py:9-45`). The row's finish time is exactly the landing (checked: difference 0.0 over every sample row).
- The penalty follows: `exponential_variates(20, 0.5)`, 20.0-23 s (`:212`).
- For the network class only, the cursor is cleared (`:222-224`).

**(iii) What it does next.** Its restart point is fixed by the class:
- network: SCAN_HOST (`:244-249`), which rebuilds the queue from the current graph (`:294-347`); ENUM_HOST then re-pops a host, often the same one;
- application: SCAN_PORT on the same host (`:250-254`);
- reserve: EXPLOIT_VULN on the same host and ports (`:255-264`).

**(iv) Which later actions fail, and why.** None fail on a precondition, because the restart order guarantees them. The costs are:
- (a) **Re-paying the procedure.** Host layer: SCAN_HOST 5 s + ENUM_HOST 5 s + SCAN_PORT 25 s. Service layer: SCAN_PORT 25 s (`constants.py:140-148`).
- (b) **One of the host's ten attempts burned** by each host-layer re-pop (`:436-442`). The target is exempt under the targeted objective (`:439`).
- (c) **Service and OS diversity** wipe the exploit progress inside the host. The re-scan sees only the host's outer services, so the exploit has to climb again.
- (d) **CTS and HTS** can shrink or reshape the queue.

**(v) When it is back.** Measured medians, from the landing:

| | Host layer | Service layer |
|---|---|---|
| The next action starts | 20.3 s (the penalty) | 20.3 s |
| The cursor is regained (ENUM_HOST done) | 30 s | — |
| SCAN_PORT done | 55 s | 45 s |
| The interrupted action completes again | 56-57 s | 46-47 s |

The next compromise, against the same seed's no-MTD run at the same clock time: IPShuffle 306 s against 269 s; ServiceDiversity 640 s against 247 s, with 26 of 140 deployments followed by no compromise at all. The baseline's cost is almost hand-derivable from `ATTACK_DURATION`: ≈ 20 + 35 s (host layer) or 20 + 25 s (service layer), plus the lost exploit progress for diversity.

### C. The APT attacker model (`src/mtdsim/l3_simulation/movement/attacker.py`)

**(i) Which actions a deployment catches.** The walk is one long-lived process (`:543-551`), so the gate's `is_alive` check passes all run. What the gate reads is `curr_process`:
- the announced verb, set **before** dispatch, and so also on a blocked dispatch (`:652`);
- `DWELL` at a dwell-only tactic (`:1057`). No class exempts DWELL, so network and application mutations both catch it; reserve does not.

Measured per deployment:

| | Dwell-only tactic | Dispatched action | Blocked dispatch | Nothing caught |
|---|---|---|---|---|
| Host layer | 43-47% | 36-39% | 13-21% | 0% |
| Service layer | 46-51% | 13-15% | 9-11% | 25-30% |
| UserShuffle | — | about 1% | — | 99% |

**(ii) What the interrupt does.**
- **A dispatched action.** `step()` spends one timeout for the tactic's drawn time, then runs the core (`attack_operation.py:862-866, 877-889`). An interrupt lands in the timeout, so the core **never runs**, the exploit included. It is caught at `:909`; `_read_interrupt` pays the substrate's cost through the shared `apply_mtd_interrupt_cost` (`:1018`) and returns verdict **failure** (`:998`; `verdict.py:83-84`).
- **A blocked dispatch or a dwell-only tactic.** `_serve_time` is cut short and pays the same cost (`:1040-1043`). A dwell-only tactic raises **no** verdict and routes on the base weights (`:599`).

The penalty and the cursor clear are identical to the baseline's. **One difference:** the unserved remainder of the drawn time is forfeited. The draws are exponential (`timing.py:11-16`), so the remainder is on average the tactic's mean: 36-45 s for the dwell-only tactics and for discovery and command-and-control (catalogue). That exceeds the ~20.4 s penalty. *Derived:* a dwell interrupt on average ends the visit **sooner** than it would have ended. The direct time cost of an interrupt to the APT model is about zero or negative; its real cost is emergent. This is inferred from code and the memoryless draw; the draw is not recorded, so it is unmeasured.

**(iii) How the token routes after.** A failure is composed with the failure matrix at the **source tactic** (`outcome.py:114-150`), with no knowledge that an MTD caused it:
- at a post-intrusion tactic it keeps the token in its stage (trace: execution | failure → persistence 0.41, stealth 0.28);
- only a failure at initial-access pushes it to reconnaissance (trace: → reconnaissance 0.75).

So a host-layer interrupt at a post-intrusion tactic does **not** send the token back towards the tactics that restore its position.

**(iv) Blocked dispatches afterwards: the "tactics it visits before it comes back".**

*Host layer.* The cursor is cleared (`attack_operation.py:222-224`).
- Only **lateral-movement** (ENUM_HOST) re-sets `curr_host` (`:416-417`). **Reconnaissance** (SCAN_HOST) refills the queue and does not set the cursor (`:294-347`).
- Until lateral-movement fires, every host action fails `assert_action_context`, so it is recorded as blocked (`PRECONDITION_UNMET`, `attacker.py:894-903`): SCAN_PORT, BRUTE_FORCE and SCAN_NEIGHBOR need the cursor, and EXPLOIT_VULN also needs ports (`attack_operation.py:787-800`). These are discovery, credential-access, command-and-control, and initial-access / execution / privilege-escalation.
- The fresh-host guard cannot re-select, because it needs an owned cursor (`attacker.py:790-792`).
- After ENUM_HOST, `curr_ports` is reset (`attack_operation.py:448`), so every exploit tactic stays blocked until **discovery** runs.

The thesis placeholder's "until an enumerate **or scan host** succeeds" (`dissertation.tex`, the commented paragraph after the dwell-only sentences in §4.4.1) is inaccurate: SCAN_HOST alone never restores the cursor.

Measured medians:

| | Host layer | Service layer | No-MTD reference |
|---|---|---|---|
| Blocked dispatches, landing to the first host action that runs | 6-9 (mean 13-31) | 0 | 0 |
| Tactic visits before the cursor is regained | 8-10 | — | — |
| Cursor regained (ENUM_HOST success) | 216-304 s | — | — |
| The first host action that runs | 375-456 s | 104-114 s | 129-131 s at the same clock |
| Share of dispatches blocked in the 500 s after | 55-65% | 25-27% | 26% |

*Service layer.* The cursor and `curr_ports` survive, so nothing is blocked. PortShuffle leaves `curr_ports` stale: the precondition only checks the list is non-empty (`:796`), so the exploit runs on fewer services (A). Service and OS diversity reach it through the next exploit's outcome.

**(v) When it is back.**
- Host layer: at the first host action that runs, median ~375-456 s, about 250-325 s beyond the reference. Trace E3 shows one deployment. The cursor is regained at +157 s, the same host at +265 s, and that host's exploit runs again, and compromises, at +757 s.
- Service layer: no positional loss. The next compromise: 966-1 069 s against ~850 s with no MTD.

### D. What the run records store (`run_corpus.py`) and how to read each outcome

**The APT model** (`run_corpus.py:209-215`). Each row is `[place, verb, outcome, verdict, blocked, interrupted, dwell, start, end, place_class]`.

| What happened | How it reads in the row |
|---|---|
| Ran, success | `verb` set, `verdict=="success"`. Outcome is TRUE / FALSE / NONE / EXPLOIT_COMPROMISED (SCAN_PORT FALSE and SCAN_NEIGHBOR NONE are successes, `verdict.py:74-76, 93-94`) |
| Ran, failure | `verdict=="failure"`, `blocked==0`, `interrupted==0`. Outcome is FALSE (SCAN_HOST, BRUTE_FORCE), EXPLOIT_UNCOMPROMISED, ENUM_EXHAUSTED, SCAN_PORT_EMPTY or NEIGHBORS_NONE_FRESH |
| Interrupted in flight | `outcome=="MTD_INTERRUPT"`, `interrupted==1`, `verdict=="failure"`, `blocked==0` |
| Blocked (precondition unmet) | `outcome=="PRECONDITION_UNMET"`, `blocked==1`, `verdict=="failure"`. `interrupted==1` when a deployment landed during the blocked visit |
| Dwell-only | `place_class=="dwell-only"`, `verb==""`, `outcome=="DWELL_ONLY"`, `verdict==""`. `interrupted` is 0 or 1 |
| Terminal | `outcome` in SIM_END, MAX_EVENTS, SINK_EXHAUSTED, `verdict==""` |

- `interrupted==1` on a ran-success or ran-failure row happens only when a deployment lands during a token hold. Holds are off in the corpus.
- For any interrupted row, `end - start - dwell` = the penalty (checked: 20.0-22.96 s on every interrupted row, 0.0 on every other row).
- The row has **no** mechanism name: `interrupted_by` and `interrupted_by_name` are dropped. The mechanism comes from `condition`, or, under a scheme, from matching `mtd_executions` finish = landing.

**The baseline** (`run_corpus.py:304-313`). Each row is `[name, start, finish, compromise_host|null, compromise_host_uuid, interrupted_in|null]`.
- There is **one row per vulnerability** for EXPLOIT_VULN (`attack_operation.py:563-565`).
- The only outcomes recorded are a compromise (column 3) and an interrupt (column 5 = network / application / reserve). There is no failure verdict, no precondition-unmet row, and no dwell. A failed BRUTE_FORCE is visible only as a row without a compromise, followed by ENUM_HOST.
- The penalty is the gap from an interrupted row's finish to the next row's start (median 20.3 s).
- `interrupted_by` (the name) is dropped.
- The run-level fields `mtd_executions` (`[name, start, finish, duration, layer]`) and `mtd_attack_interrupted` exist for both attackers.

**Analyser caveats found:**
1. **The baseline's `termination_time` is always the horizon** (`run_corpus.py:287, 297`: `env.now` after `run(until=15000)`), even when the target fell at ~5 000 s. `disruption.py:91-96` uses it as T, so deployments after the baseline's run ended count, and their bins count as live time. That was 59 of 157 IPShuffle deployments in the sample. The docstring's "a bin counts only the part of it before the run ended" (`disruption.py:28-31`) does not hold for the baseline. `blocked_resume.py:56` avoids this by using the last action's end.
2. `blocked_resume.py:20-21` counts an APT block only when the outcome is MTD_INTERRUPT. Interrupts on blocked dispatches (13-21% of host-layer deployments) and on dwell-only tactics (43-51%) are excluded. The baseline's interrupted rows are all counted, with consecutive exploit rows collapsed (`:23-28`).
3. The unified tracer prints "ran for all of it" for an interrupted verb (`trace.py:387-390`) although the core never ran. Its CAUGHT line names the announced verb even when that verb was a blocked dispatch (see E3).

### E. Traces

The substrate tracer runs the general objective (it has no `--attack-objective`); the unified tracer runs the corpus configuration. A baseline ATTACKER line is stamped at its action's **completion**.

**E1. Baseline, IPShuffle** (`python -m mtdnetwork.trace --scheme single --mtd IPShuffle --interval 200 --seed 0`)
```
t= 288.0 ATTACKER  SCAN_NEIGHBOR spread out from host 0  queue 4 → 5 · owns 1/50
t= 293.0 ATTACKER  ENUM_HOST     picked host 18  attempt 1/10
t= 300.7 MUTATION  IPShuffle: 45 IP(s) moved · owned 1->1 · visible 1->1 · on host 18      <- lands; writes .ip only
t= 300.7 INTERRUPT CAUGHT        IPShuffle hit the attacker mid-SCAN_PORT                   <- row: SCAN_PORT 293.0-300.7, interrupted_in=network
t= 321.3 INTERRUPT SETBACK       confused 20.5 t/u · restarting at SCAN_HOST                <- penalty; cursor cleared
t= 326.3 ATTACKER  SCAN_HOST     5 host(s) queued                                           <- first success, +25.6 s
t= 331.3 ATTACKER  ENUM_HOST     picked host 18  attempt 2/10                                <- same host back, +30.6 s; one of 10 attempts burned
t= 356.3 ATTACKER  SCAN_PORT     host 18: 3 open port(s)                                    <- the interrupted verb completes, +55.6 s
```
**E2. Baseline, ServiceDiversity** (same, `--mtd ServiceDiversity`)
```
t= 589.2 ATTACKER  EXPLOIT_VULN  host 2: trying 11 vulnerabilities                          <- starts; per-vulnerability timeouts
t= 671.8 MUTATION  ServiceDiversity: 320/320 internal service(s) redrawn · owned 1->1
t= 671.8 INTERRUPT CAUGHT        ServiceDiversity hit the attacker mid-EXPLOIT_VULN         <- earlier rolls stand; the in-flight one is lost
t= 671.8 ATTACKER  EXPLOIT_VULN  host 2: spent 82.6 t/u
t= 692.8 INTERRUPT SETBACK       confused 21.0 t/u · restarting at SCAN_PORT                <- cursor kept
t= 717.8 ATTACKER  SCAN_PORT     host 2: 3 open port(s)                                     <- first success, +46 s
t= 717.8 ATTACKER  EXPLOIT_VULN  host 2: trying 7 vulnerabilities                           <- a new list (the services were redrawn)
t= 794.6 COMPROMISE HOST OWNED   host 2 compromised  owns 2/50                              <- +123 s
```
**E3. APT model, IPShuffle** (`PYTHONPATH=src python -m mtdsim.l3_simulation.trace objective_exfiltration --mapping v2_partial --overlay-version v4_failure_only --retrace --attack-objective targeted --scheme single --mtd IPShuffle --interval 2000 --seed 1`)
```
t=2087.7 STEP  stealth (dwell-only) → execution
t=2101.4 MUTATION IPShuffle · owned 2->2 · on host 24
t=2101.4 CAUGHT   IPShuffle hit the attacker mid-EXPLOIT_VULN       <- announced verb; it was a BLOCKED dispatch
t=2121.9 SETBACK  pays 20.5 t/u · network-layer mutation            <- cursor cleared
t=2121.9 STEP  execution: EXPLOIT_VULN blocked — precondition unmet → persistence   (execution|failure: persistence .41, stealth .28)
t=2252.8 STEP  persistence (dwell-only, 130.9) → credential-access
t=2254.0 STEP  credential-access: BRUTE_FORCE blocked — precondition unmet → lateral-movement
t=2258.1 STEP  lateral-movement: ENUM_HOST -> success [popped host 13]   <- cursor regained, +157 s
t=2332.4 STEP  stealth (dwell-only, 74.3) → initial-access
t=2339.2 STEP  initial-access: EXPLOIT_VULN blocked (no ports) → reconnaissance   (initial-access|failure: reconnaissance .75)
t=2360.3 STEP  reconnaissance: SCAN_HOST -> success
t=2366.6 STEP  lateral-movement: ENUM_HOST -> success [popped host 24]   <- back on the same host, +265 s
t=2367.3 STEP  credential-access: BRUTE_FORCE -> failure                <- the first host action that runs, +266 s
t=2400.1 STEP  execution: EXPLOIT_VULN blocked (discovery not yet run)
  ... 2435-2716: ENUM_HOST ×3, SCAN_NEIGHBOR, IA blocked, SCAN_HOST ...
t=2830.2 STEP  discovery: SCAN_PORT -> success
t=2858.9 STEP  execution: EXPLOIT_VULN -> success                       <- the exploit runs again (and compromises), +757 s
```
**E4. APT model, ServiceDiversity** (same, `--mtd ServiceDiversity --interval 200 --seed 0`)
```
t= 272.2 MUTATION ServiceDiversity · on host 0
t= 272.2 MISSED   attacker was in ENUM_HOST — unaffected by this layer  <- a recon verb is immune; the write reaches nothing now
t=1058.9 STEP  discovery: SCAN_PORT -> success → execution
t=1068.6 STEP  execution: EXPLOIT_VULN -> failure (6 OS-refused)
t=1070.1 DISPATCH execution -> EXPLOIT_VULN
t=1072.3 MUTATION ServiceDiversity: 320/320 redrawn
t=1072.3 CAUGHT   mid-EXPLOIT_VULN · "interrupted after 2.2 t/u"        <- the core never ran
t=1093.1 SETBACK  pays 20.8 t/u · application-layer mutation           <- cursor and ports kept
t=1093.1 STEP  execution: EXPLOIT_VULN -> failure → collection          (execution|failure: persistence .41 ...)
t=1093.7 STEP  collection (dwell-only) → exfiltration
t=1142.0 STEP  exfiltration (dwell-only, 48.3) → command-and-control
t=1206.5 STEP  command-and-control: SCAN_NEIGHBOR -> success            <- first success, +134 s; nothing blocked
```

### F. In one paragraph per attacker, and the events a metric can count

**The baseline attacker.** A deployment costs the baseline a fixed, hand-derivable detour. The attacker re-runs a set part of its procedure:
- **host layer** (IP, complete-topology and host-topology shuffles): the ~20 s penalty, then SCAN_HOST → ENUM_HOST → SCAN_PORT. It is back at the same place about 55 s after the landing, having burned one of the host's ten attempts.
- **service layer** (port shuffle, OS and service diversity): the penalty, then SCAN_PORT. It is back after about 45 s.

The script re-establishes every precondition, so nothing afterwards fails for lack of state. Only service and OS diversity leave a lasting cost: they erase the exploit progress inside the host, so the next compromise comes about 2.6× later (640 s against 247 s). IPShuffle's own write reaches nothing.

**The APT attacker model.** A deployment's direct price is small. The action it catches fails, and the penalty roughly replaces time the attacker would have spent anyway. The cost is emergent:
- **Host layer:** the cursor is lost. Only lateral-movement restores it, and the failure matrix keeps a post-intrusion failure inside its stage. The token wanders through post-intrusion tactics, and every host action there is blocked until lateral-movement, then discovery, come round. The median is 6-9 blocked dispatches and ~250-325 s beyond the reference before a host action runs.
- **Service layer:** it loses no position. It pays only through later exploit outcomes (redrawn services, OS refusals, stale ports).

**Countable events for a disruption metric**, each available on both attackers except where marked:
1. Deployments that land while the attacker is live (the denominator). Use the last action's end, not `termination_time`, for the baseline.
2. **Interrupts per deployment**, split into the action in flight (both), a blocked dispatch (APT only) and a dwell-only tactic (APT only).
3. The penalty, identical at ~20.4 s. It is not a net time cost for the APT model (C(ii)).
4. **Time from landing to the first action that runs** after a disruption. APT: the first row with `verb` set, not blocked and not interrupted. Baseline: the next row's start.
5. **Time from landing until the interrupted action runs again**, same verb (baseline 46-57 s; APT via `t_same`).
6. **Blocked dispatches (PRECONDITION_UNMET) between the landing and the first host action that runs** (APT only; host layer 6-9 against 0). This is the "tactics it visits before it comes back", made countable.
7. **Time to regain a host cursor** (the first ENUM_HOST success). Host layer only.
8. **Time from landing to the next compromise**, against the same seed's no-MTD run at the same clock time.
9. Baseline only: attempts burned on the give-up counter per host-layer interrupt.

The scratch scripts and trace logs behind this audit were session-local and are not kept; section E's excerpts are the evidence, and the trace tool reproduces them.

## 7. Update, Marc's read (2026-09-30)

Marc kept attack actions blocked **per run** and re-defined **time lost per MTD
deployment** as the extra time to the attacker's next compromise, against the same
moment of the no-MTD run. The dry run (`time_to_next_compromise.py`) confirms
section 1:
- The APT model loses 206–313 s per host-layer deployment and about nothing on the
  service layer.
- The baseline loses about nothing on the host layer, and 518 s per
  service-diversity deployment.

The rulings, the table and what to apply are in
[`../handoffs/2026-09-30_disruption_metrics.md`](../handoffs/2026-09-30_disruption_metrics.md).

## 8. Two simplifications tested, and one finding for chapter 6 (2026-09-30)

Marc proposed two ways to drop the restricted mean from time lost per MTD
deployment. Both were tested on the corpus (2 000 s, 100 seeds) and neither removes it.

**Assume a deployment costs the same at every phase of the attack.** The data
contradicts this. Time lost split by whether the attacker had compromised any host
when the deployment completed:

| | before its first compromise | after it |
|---|--:|--:|
| APT model, IP shuffle | 214 s (n = 852) | 350 s (n = 2 272) |
| APT model, host topology shuffle | 159 s (n = 702) | 228 s (n = 2 434) |
| APT model, service diversity | −8 s | 68 s |
| baseline, service diversity | −202 s (n = 99) | 673 s (n = 460) |

This matches section 1: a deployment can take only the position or the exploit
progress the attacker already has. **For chapter 6:** the cost of a deployment depends
on the attacker's phase. Both attackers pay more once they hold a foothold.

**Make the deployment interval very long, so that no wait is cut off.** Even with no
cap at the next deployment, the run's end cuts off the wait. With the MTD, 20–33 %
of the APT model's deployments are never followed by a compromise before the run
ends (22 % with no MTD); for the baseline under service diversity the figure is 13 %
(4 % with no MTD). A cap is therefore needed whatever the interval, and the
restricted mean stays. It would only move from the next deployment to the time
limit, at the cost of new runs at an interval nothing else in chapter 5 uses.
