---
status: open           # loop fix ruled in 2026-08-30 (step 0); retire when the findings record lands and its numbers have gone to Jin
created: 2026-08-30
---

# The token-hold rule (T1) — build Jin's fix as a declared succession variant, measure it against factor 9, and produce the trace Jin asked for

> **One-line goal.** When the Petri net's draw lands on a tactic whose verb the
> inherited FSM does not license from the current state, **leave the token where
> it is** (Jin, 25 Aug 2026 — register **T1**). Build it, pre-register its
> criteria, run it, and report it beside factors 8 and 9 — whichever way it falls.
>
> **Run this in a fresh session, cold from this brief.**

## State of play

- The ruling and its full annotation are in the register:
  [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
  §T1–T5. Read T1 in full before touching code — it says why this is *not*
  simply "turn α to 1".
- **The near-twin is already built and swept.** The FSM-succession modulator
  (`src/mtdsim/l3_simulation/movement/succession.py`, spec
  [`../implementation/pipeline/ogasp/fsm_succession_overlay.md`](../implementation/pipeline/ogasp/fsm_succession_overlay.md),
  relation `data/ogasp/controller/fsm_succession.json`) multiplies every
  out-edge whose verb the FSM does not license by (1 − α). Its α = 1 point is
  **rejection sampling with dwell-only places transparent**, and it was measured
  DEGENERATE at 2 080 runs
  ([`../implementation/pipeline/ogasp/fsm_succession_prereg.md`](../implementation/pipeline/ogasp/fsm_succession_prereg.md)
  B2–B3, §4): 2.18 hosts (modal 0), 67.6 % of visits on dwell-only places.
  Mechanism: with a narrow licensed set, mass goes to the seven transparent
  dwell-only tactics rather than the one licensed verb — the attacker pivots and
  waits. **Do not re-run this and call it Jin's fix.**
- **What is unmeasured is the opaque hold**: the token is held (a re-dwell at
  the current place, so the hold costs time — the "slower" Jin accepts) until
  the draw lands on a place whose verb *is* licensed; dwell-only places are held
  out too — a draw onto one is a hold, not a visit, so they are never a
  hold-breaking destination. The verb chain becomes the FSM's chain;
  the CTI weights choose only among licensed successors (e.g. after `ENUM_HOST`
  the licensed set is {`ENUM_HOST`, `SCAN_PORT`, `SCAN_HOST`}); the dwell regime
  stays CTI-derived. Plurality will collapse toward the FSM — measure it and say
  so (B4-style entropy row).
- **The ordering is not the only barrier.** Even a perfect FSM order does not
  stop `_do_scan_neighbors` returning already-owned hosts to the stack, which the
  native skip-owned loop absorbs and the movement layer does not — 89 % of
  movement compromise actions re-compromise reachable owned hosts **with no MTD**
  ([`../implementation/pipeline/ogasp/movement_objectives_design.md`](../implementation/pipeline/ogasp/movement_objectives_design.md)
  §2–§3). **Why FSM order alone cannot fix it (Marc's question, 2026-08-30):**
  the native pivot is not an order but a *branch* — `_execute_enum_host` loops
  `ENUM_HOST` while `_do_enum_host()` returns `True` (popped host already owned)
  and only then fires `SCAN_PORT`. The succession relation licenses
  `{ENUM_HOST, SCAN_PORT, SCAN_HOST}` after `ENUM_HOST` because the verdict
  adapter reads `ENUM_HOST` as success-unless-interrupted — the owned branch is
  invisible to routing, so `SCAN_PORT` on an owned host is FSM-legal under the
  hold rule and the churn survives (factor 9 at α = 1: `ENUM_HOST` 57.8 % of
  actions, 2.18 hosts). **The companion is therefore one verdict row, not a new
  policy:** surface `_do_enum_host`'s `True` as an `owned` verdict and license
  only `ENUM_HOST` on it — this reproduces the native loop inside the hold rule
  and is the exclude-owned-and-re-select policy of that record §3 in its minimal
  form (the "re-select" half is load-bearing; a pure block trades one churn for
  another). Run the hold rule **with and without** it.
- **Located-target reach is a different barrier again** (B-i, no host-level
  targeting —
  [`../implementation/pipeline/ogasp/targeted_objective_probe.md`](../implementation/pipeline/ogasp/targeted_objective_probe.md)
  §7.1). The hold rule does not point the attacker at the database hosts. Report
  target reach anyway (the read-only `database_hosts_reached` measurement is
  wired), but pre-register the expectation that it moves little.
- Modulators are **null on the reported configuration** (α declared 0.0). This
  work adds a variant and measures it; it moves no badge and re-baselines no
  golden by itself. Whether the hold rule becomes the reported configuration is
  **Marc's ruling on the numbers**, not this session's.

## Recommended approach

**Marc's ruling (2026-08-30): fix the seam first.** The dropped `ENUM_HOST`
skip-owned loop is a **carve-out bug** under the bug-vs-design instrument —
Brown's chain ends Enum Host in *selection of a target host*
([`../implementation/mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md)
IS-PRC-01, action chain), the native wrapper loops on an owned host, and the
movement layer silently lost that when it took one outcome per visit. Marc
rules the host-selection gate of `movement_objectives_design.md` §6 open for
this: restore the loop (re-pop until a fresh host, or the `owned`-verdict row
licensing only `ENUM_HOST`), re-baseline the movement goldens, and **re-run the
headline** (the 2 400-run matrix) on the fixed attacker — the inversion measured
on a churning attacker is the less defensible number. Steps 0 and 1 below are
therefore ordered: the loop fix stands on its own; the hold rule is layered on
only if the loop fix alone leaves the attacker short of "much better progress".

   *Scope check (2026-08-30, all six wrappers re-read): only `ENUM_HOST`'s
   wrapper carried host-selection semantics beyond dispatch (owned → pop again).
   `SCAN_HOST` filters owned hosts in its core; `SCAN_PORT`, `EXPLOIT_VULN`,
   `BRUTE_FORCE` branch only on their own outcome; `SCAN_NEIGHBOR` has no
   branch. So this is one wrapper's branch plus one verb-time invariant — not a
   recode of the six. The invariant: a compromise verb (`SCAN_PORT` /
   `EXPLOIT_VULN` / `BRUTE_FORCE`) fires only on a fresh, reachable
   `curr_host`; if `curr_host` is owned, re-select via the loop before firing.
   Both halves live movement-side (`_dispatch` / an `ENUM_HOST` path in
   `_walk`), never in the shared cores — filtering `_do_scan_neighbors` would
   change native timing and every inherited golden.*

0. **Restore the loop** as the first, separately committed change: a movement
   `ENUM_HOST` dispatch that re-pops while `_do_enum_host()` returns `True`
   (bounded by the visible stack; empty → `SCAN_HOST`, as the native guard),
   counted in the record as `enum_repops`. Hand-trace it (V1), re-baseline
   goldens with the fixture diff in the commit, run the no-MTD cell at ≥ 350
   seeds against the 5.60-host null, then the headline matrix. Report ρ beside
   −0.893 and annotate the probe record's "structural, not tunable" sentence.
1. **Design the hold-rule variant on the existing seam, not a new one.** Add a declared
   `hold` mode to `FsmSuccessionModulator` (or a sibling modulator registered on
   `AttackerState`): at `_route`, if the sampled next place dispatches a verb
   not in `next_verbs(last_verb, verdict)` (or `after_interrupt(resource)` after
   an interrupt), the token stays at the current place, pays one dwell draw
   (`timing.draw(place)`), emits a visit record tagged `held`, and re-draws.
   Keep factor 9's **abstention rule** (if *no* out-edge is licensed, do not hold
   — a stall must stay structurally impossible) and its **capability fallback**
   (if the licensed successor cannot run in the current capability state, the
   precondition closure's first-step verbs are the targets). Bound the hold:
   after *k* consecutive holds fall through to the plain draw and count it, so
   the run cannot spin; report the fall-through rate.
2. **Pre-register before running** (commit order, as factors 8/9): the
   criteria are factor 9's B1–B4 and its degeneracy guard **verbatim** (hosts vs
   the null 5.60 ± CI; modal hosts; actions-per-run band; entropy; assists 0/7),
   plus target reach, plus **held fraction of routing decisions** and the
   fall-through rate. State the prior: breadth up on the mass objective,
   plurality down, target reach ~unchanged. Name the "better progress" bar Jin
   expects — breadth **above** the α = 0 null with non-overlapping CIs is the
   honest reading of "much better progress".
3. **Run the 2 × 2 × 2:** {hold off, hold on} × {loop fix off, on} × {horizon
   15 000, 30 000 (T2)}, the aggregate profile, no MTD, ≥ 350 seeds per cell
   (probe budget), then the four single mechanisms at 100 seeds for the cell
   that clears the bar, so ρ against the inherited attacker is on the table
   beside factor 9's band (−0.821 … −1.000).
4. **Hand-validate first (V1).** A four-or-five-host network, one seed, trace
   by hand that the held visits are exactly the FSM-illegal draws and nothing
   else; the standing native-transition test in the succession module is the
   oracle for the relation.
5. **The trace for Jin (T5).** `PYTHONPATH=src python -m mtdsim.l3_simulation.trace`
   on one seed, before and after: show the `SCAN_NEIGHBOR → ENUM_HOST`
   progression being skipped, and the re-compromise churn, in the attacker's own
   event stream — Marc reconciles the meeting's procedural account with the
   record's churn account *before* sending it.
6. **Land the findings record** as
   `docs/implementation/pipeline/ogasp/fsm_token_hold_findings.md` (prereg above
   the fold, verdicts below, factor-9 style), annotate the register's T1, and
   return the thesis-framed pointer: which claim moves (headline inversion
   stands or shifts; the "structural not tunable" sentence in the probe record
   is either confirmed or amended), which criterion axis is touched (axis 6
   plurality figures if the variant is ever reported), and what is now sayable.

Alternatives considered: re-running α = 1 (already done, degenerate — no);
zeroing out every non-FSM edge in the net file (Marc's "becomes the baseline";
also a net edit, not a modulator, so it breaks every golden); a substrate-side
rewrite of the movement walk (out of scope — the seam exists).

## Design — the order-independent verb contract (Marc's ask, 2026-08-30)

The target: when the token calls a verb, it **runs from whatever state the
attacker is in, behaves as its native counterpart would from that state, takes
exactly the time the movement layer supplies, and returns one success/failure
verdict**. Three of the four legs already exist on the seam; the fourth (state
invariants) is the gap, and one verdict simplification hides it.

**What exists (do not rebuild):**
- *Timing from the movement layer* — `step(verb, duration=d)` charges the
  caller's `d` once and nothing else (S3-R; `EXPLOIT_VULN` runs its vuln loop
  with `charge_time=False`). Native `ATTACK_DURATION` is the fallback only when
  `d` is `None`, i.e. never on the movement arm.
- *Precondition, not order* — `assert_action_context(verb)` raises when the
  shared state a core assumes is absent (`host_stack` for `ENUM_HOST`,
  `curr_host` for the attack verbs, `curr_ports` for `EXPLOIT_VULN`); the
  movement layer reads that as `PRECONDITION_UNMET` → failure, still charging
  the dwell, and never re-imposes native order to satisfy it (H-coupling).
- *Verdict propagation* — `controller/verdict.py::verdict_for(verb, outcome,
  interrupted)`: interrupt/`EXPLOIT_HALTED` → failure; `EXPLOIT_VULN` and the
  bool verbs read their own outcome.

**What to add — per verb (the contract table):**

| verb | precondition (exists) | state invariant to add (movement-side) | verdict today | verdict to add |
|---|---|---|---|---|
| `SCAN_HOST` | none (root) | none — core already excludes owned hosts | bool | — |
| `ENUM_HOST` | non-empty *visible* stack | **retry-until-fresh**: while `_do_enum_host()` returns `True` (owned), pop again; stop on a fresh host or an exhausted visible stack | success-unless-interrupted | **failure if no fresh host was selected** (stack exhausted → the native "no host → SCAN_HOST" fact becomes a verdict the net routes on) |
| `SCAN_PORT` | `curr_host` set | **fresh-host guard**: if `curr_host` is owned, run the `ENUM_HOST` re-select first; if none fresh → `PRECONDITION_UNMET` | success-unless-interrupted | failure if `curr_ports` empty after the scan (the deferred "richer adapter", one line) |
| `EXPLOIT_VULN` | `curr_host` + `curr_ports` | same fresh-host guard | `EXPLOIT_COMPROMISED`/`UNCOMPROMISED` | — |
| `BRUTE_FORCE` | `curr_host` | same fresh-host guard | bool | — |
| `SCAN_NEIGHBOR` | `curr_host` | none (semantically "from a held host" — owned is *correct* here) | success-unless-interrupted | failure if no host not already owned entered the stack |

Rules that keep it a seam and not a second FSM:
1. **Invariants live in the movement layer's dispatch, never in the shared
   cores** — the native arm and its goldens stay byte-identical.
2. **A guard never changes the verb the token chose.** The fresh-host guard is a
   *pre-step* inside the same place visit (re-select, then fire); if it cannot
   be satisfied the visit fails on `PRECONDITION_UNMET`. The net, not the
   guard, decides what comes next.
3. **One dwell per place visit, whatever the guard did.** The re-select pops
   are clock-free and RNG-free (`_do_enum_host` draws nothing); the supplied
   duration prices the behaviour "select and act", not the pop count. Record
   `enum_repops` per visit so the cost is auditable, and note it as a declared
   divergence from native pricing (native charged `ATTACK_DURATION['ENUM_HOST']`
   per pop).
4. **Verdict is binary and read once** (M2). The three new failure conditions
   are read off state deltas (`curr_host` fresh? `curr_ports` non-empty? stack
   gained a fresh host?) in `verdict_for`, not by re-rolling anything (M4).
5. **Interrupt semantics unchanged** — any MTD interrupt mid-verb → failure,
   the overlay routes.

Implementation surface: `_dispatch` (guard + repop loop, before
`attack_op.step`), `verdict_for` (three rows), `MovementRecord` (`enum_repops`,
`reselected` flags), the standing native-transition test extended with a
"movement arm never fires a compromise verb on an owned host" assertion.
Hand-trace on a five-host network first (V1).

## Validation gate

The findings record exists with prereg committed before the run; the 2 × 2 × 2
table with CIs; the ρ row for the clearing cell; held/fall-through rates;
plurality row; target reach; the hand-trace; the before/after trace sent to
Jin; register T1 annotated with the result; every golden unchanged
(`pytest tests/`); determinism per variant (SIM-05: same config + seed →
identical run).

## Hard constraints

- Additive and declared: default off; the reported configuration is
  bit-identical to before. No golden changes. No net-file edits.
- Determinism (SIM-05); the hold's re-draw consumes the attacker's own RNG
  stream, so document the stream change for the variant.
- The abstention rule and capability fallback stay (a stall must be
  impossible; factor 9 §2.1–2.2 say why).
- Factor 9's stopping rule: this is a **supervisor-directed band point**, not a
  third alignment factor. Do not iterate the design to make it work; report what
  it does.
- Test the ruling; do not confirm it. Jin expects "much better progress" — if
  it does not come, that is the finding, and the register annotation already
  says why it might not.
- Branch/commit/no-push rules per
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md).

## Reading list

1. Register §T1–T5; then
   [`../implementation/pipeline/ogasp/fsm_succession_overlay.md`](../implementation/pipeline/ogasp/fsm_succession_overlay.md)
   §2 (the rule, transparency, abstention, fallback) and
   [`fsm_succession_prereg.md`](../implementation/pipeline/ogasp/fsm_succession_prereg.md)
   below the fold (the degenerate α = 1 point — the thing not to repeat).
2. `src/mtdsim/l3_simulation/movement/succession.py`, `attacker.py`
   (`_walk`, `_route`, `_sample`, `_serve_dwell_only`), `run.py` (arm and
   modulator wiring, `horizon`).
3. [`movement_objectives_design.md`](../implementation/pipeline/ogasp/movement_objectives_design.md)
   §2–§3 (the churn, the re-select policy) and §5–§6 (the Row-B confound and
   the one open supervisor question — the re-select half re-opens scoped work,
   so it is run here *as a measurement*, not adopted).
4. [`targeted_objective_probe.md`](../implementation/pipeline/ogasp/targeted_objective_probe.md)
   §5–§7 and `data/results/targeted_objective_probe/run_probe.py` (harness
   precedent, seed budgets).
5. [`../implementation/trace_tool.md`](../implementation/trace_tool.md).

## Out of scope (explicitly)

- Host-level targeting (`movement_targeted`, barrier B-i) — a separate ruling
  the probe record leaves with Marc.
- Making the *hold rule* the reported configuration or moving any badge —
  Marc rules that on the numbers. (The loop fix, by contrast, **is** ruled in:
  it becomes the reported configuration and the inversion is re-established on
  it.)
- Any change to the inherited attacker or the net files.
