---
status: open — pre-registration committed 2026-08-30; verdicts pending below the fold
created: 2026-08-30
updated: 2026-08-30
handoff: 2026-08-30_fsm_token_hold_rule.md
topic: "The fresh-host contract (Marc's loop-fix ruling) and the token-hold rule (Jin's T1) — what each does to the movement attacker's breadth, plurality, located-target reach and the defence-ranking inversion, pre-registered against factor 9's band and the probe's Gate 0, with the priors and the layering rule fixed before any number was seen"
---

# The fresh-host contract and the token-hold rule — pre-registered, then as found

**Everything above the fold was committed before the runs produced a single
row.** The verdicts land below it in a separate commit, scored against these
criteria without amending them. This record executes the
[`2026-08-30_fsm_token_hold_rule.md`](../../../handoffs/2026-08-30_fsm_token_hold_rule.md)
handoff (register [**T1–T5**](supervisor_decision_register.md), Jin 2026-08-25;
Marc's loop-fix ruling 2026-08-30).

**Neither mechanism scores an axis of the APT criterion, and nothing below may
be reported as one.** The token-hold rule inherits factor 9's three exclusions
verbatim ([`fsm_succession_overlay.md`](fsm_succession_overlay.md) §0): it is
not learning, not adaptivity to the *defender*, and not a fidelity improvement
(at its limit it makes the attacker walk the host simulator's own order). The
fresh-host contract is a **bug fix** under the bug-vs-design instrument, not a
capability: it restores a host-selection invariant the movement layer dropped
when it took one outcome per visit. What *may* move is the reported
configuration — the loop fix is ruled into it — and therefore every figure the
headline rests on, which is why the headline is re-run here.

## 1. The two things measured, and why they are two

**The churn, and the loop that absorbs it natively.** The inherited attacker's
`ENUM_HOST` wrapper loops while the popped host is already owned
(`attack_operation.py:443-450`) and only then fires `SCAN_PORT`; nothing
filters owned hosts out of `_do_scan_neighbors`' output, so the native FSM
relies on that loop to keep compromise verbs on fresh hosts. The movement layer
calls the same core once per place visit and never loops, so its compromise
verbs land on hosts it already owns. This was on record as a one-seed anecdote
(89 % of `EXPLOIT_COMPROMISED` events at seed 0,
[`exploit_learning_findings.md`](exploit_learning_findings.md) §(a)3) and as a
design analysis ([`movement_objectives_design.md`](movement_objectives_design.md)
§2–§3), never measured at scale. **Marc's ruling (2026-08-30):** it is a
*carve-out bug* — Brown's chain ends Enum Host in *selection of a target host*
([`../../mtdsim_intent_spec.md`](../../mtdsim_intent_spec.md) IS-PRC-01), the
native wrapper implements that with the loop, the movement layer lost it
silently — so the host-selection gate of `movement_objectives_design.md` §6 is
opened for exactly this: restore the loop, re-baseline the movement goldens,
re-run the headline on the fixed attacker.

**Jin's rule (T1), and which reading is built.** *"If it's not allowed on this
graph, you leave the token there."* The register's T1 annotation separates two
readings. The *transparent* hold (dwell-only places remain legal destinations)
is rejection sampling from factor 9's α = 1 conditional and was measured
DEGENERATE at 2 080 runs
([`fsm_succession_prereg.md`](fsm_succession_prereg.md) B2–B3, §4: 2.18 hosts,
modal 0, 67.6 % of visits on dwell-only places) — it is not re-run under a new
name. The *opaque* hold (dwell-only places are held out too; the token pays a
re-dwell at the current place until a licensed draw comes up) is unmeasured and
is what this record builds and measures.

**Why two arms of each.** Marc's ruling orders them: the loop fix stands on its
own and becomes the reported configuration; the hold is layered on top *only if
the loop fix alone leaves the attacker short of "much better progress"*. That
ordering is operationalised as a pre-registered layering condition (§3.2) so the
decision to run the hold's headline is made by the numbers, not after them. The
2 × 2 (contract off/on × hold off/on) exists so the hold's effect is measurable
both on the churning attacker Jin saw and on the fixed one.

## 2. The design

### 2.1 What was built (the two declared inputs)

| input | default | what it does | where |
|---|---|---|---|
| `fresh_host_contract` | **on** | (i) the **fresh-host guard**: a compromise verb (`SCAN_PORT` / `EXPLOIT_VULN` / `BRUTE_FORCE`) fires only on a fresh, reachable `curr_host` — if the cursor points at an owned host the retry-until-fresh loop re-selects first, and if it cannot the visit blocks on `PRECONDITION_UNMET`; (ii) the **retry-until-fresh loop** on `ENUM_HOST` itself; (iii) three **state-delta verdict rows** — `ENUM_EXHAUSTED`, `SCAN_PORT_EMPTY`, `NEIGHBORS_NONE_FRESH` — read off the substrate's state after the core ran, never re-rolled | `movement/attacker.py` `_dispatch`; `controller/verdict.py` |
| `token_hold` | **off** | the opaque hold at every routing decision, reading the FSM state an `FsmSuccessionModulator` at α = 0 tracks (the modulator reweights nothing; the hold is the only mechanism). Keeps factor 9's **abstention rule** (no licensed destination → no hold) and **capability fallback**. One declared parameter: the bound on consecutive holds, **20** (`succession_rules.json` §token_hold, declared-judgement; fall-through rate reported) | `movement/succession.py` `TokenHoldRule`; `attacker.py` `_route_with_hold` |

Rules that keep the contract a seam and not a second FSM (handoff §Design):
invariants live in the movement layer's dispatch and never in the shared cores
(the native arm and its goldens are byte-identical — verified, `pytest tests/`);
a guard never changes the verb the token chose; one dwell per place visit
whatever the guard did (the re-pops are clock-free; `enum_repops` on every
record audits the divergence from native per-pop pricing); the verdict is binary
and read once (M2); interrupt semantics unchanged.

**One claim in the handoff brief is false and is corrected here.** The brief
says the re-select pops are "RNG-free (`_do_enum_host` draws nothing)". They
are not: every pop re-sorts the queue through
`sort_by_distance_from_exposed_and_pivot_host`, whose tiebreak draws
`random.random()` per queued internal host from the substrate's **global**
stream (`network.py:901` — the D-29 shared stream). The native loop draws
identically per pop, so the contract moves the movement arm's stream usage
*closer* to native; it is recorded as a stream change, not hidden.

**Two other things the contract changes that are not "the loop".** The three
verdict rows make three verbs fail where they always read success-unless-
interrupted, so the outcome overlay routes backward at places it never did; and
the fresh-host guard converts what was a re-compromise into a *blocked* visit
when it cannot re-select (the "pure block" cost the design warned of, present
only when the visible queue is dry). Both are inside the ruled contract; both
are measurable in the records (`outcome_mix`, `blocked`), and the verdicts
below report them rather than attributing everything to the loop.

**The hold's streams.** The re-draw consumes the token sampler; the hold's
dwell consumes the timing stream — both the attacker's own (SIM-05). An MTD
interrupt mid-hold is paid (the substrate's penalty and lost-cursor semantics,
as a dwell-only interrupt is) and re-keys the licensed set through the
modulator's interrupt table; the composed distribution is not recomposed (the
verdict that produced it was read once). A held visit is one record whose
`dwell` includes the holds (`holds`, `hold_dwell`, `hold_fell_through` on the
record), so every time decomposition on record still holds.

### 2.2 The runs

| input | value | why |
|---|---|---|
| mapping / overlay / sink policy | `v2_partial` / `v3_persistent_backward` / retrace | experiment 2's, factor 9's and the probe's configuration, so every number here sits beside theirs |
| geometry / timing / interval | standard 50-host / S3-R / 200 s | unchanged; the substrate is not a variable |
| modulators | **null** (the hold arm's modulator sits at α = 0) | the reported configuration's routing; the hold is the only new mechanism |
| **stage A** — the 2 × 2 × 2 | arms {null, loop, hold, loop+hold} × horizons {15 000, 30 000 (T2)} × five profiles × **350 seeds**, no MTD; the inherited attacker at both horizons | the probe's power budget; the 30 000 s point is T2's "let the APT attacker use the horizon" |
| **stage B** — the headline | eight conditions × {inherited, null movement, loop movement [, loop+hold movement]} × five profiles × **50 seeds** at 15 000 s (2 400 runs without the hold arm) | experiment 2's E5 statistic at five times its seeds; the null arm is re-run so the "before" is contemporaneous |

**Arms:** `null` = contract off, hold off (the pre-2026-08-30 attacker, every
recorded figure's); `loop` = contract on (the reported configuration); `hold` =
contract off + hold; `loop+hold` = contract on + hold. Seed-matched arms are
independent, not paired (D-29); every cross-arm comparison is unpaired.

**What was seen before this was written, stated so the priors are honest.**
While validating the mechanisms, one seed (aggregate, seed 0, 15 000 s,
unopposed) was run: null 4 hosts with 56 of 122 compromise verbs on owned
hosts; loop 9 hosts, 0 on owned; loop+hold 4 hosts with 525 holds consuming
12 097 of the 15 000 t/u. The priors below are informed by that one seed and
by nothing else.

## 3. The conclusions, each with its criterion fixed in advance

**H0 — the kill criterion (factor 9's B5, verbatim).** In stage B the null
movement arm's Spearman ρ against the inherited attacker's defence ordering
(seven non-`none` conditions, pooled breadth suppression — experiment 2's E5
construction) is **≤ −0.5**. If it fires, no ρ below may be reported as a
statement about the inversion's response to the fix; H2 is then descriptive.
*Expectation: HELD (−0.893 at 10 seeds; factor 9's null −0.821).*

**H1 — breadth, the "much better progress" bar.** Pooled distinct hosts under
no MTD: the `loop` arm is **above the `null` arm with non-overlapping 95 %
CIs at both horizons**. This is the honest operationalisation of Jin's "much
better progress"; the fraction of the gap to the inherited attacker closed is
reported beside it, directly comparable with factor 8's ≤ 7.4 % and factor 9's
−10.4 %. *Expectation: HELD, on the one seed above (4 → 9).* The `hold` arm
against the `null` arm is scored on the same bar and reported as *Jin's rule on
its own*. *Expectation, committed against the rule: MOVED — the hold consumes
most of the horizon holding and lands below the null.*

**H1′ — the layering condition (Marc's ruling, operationalised).** The hold's
headline (stage B `loop+hold`) runs **iff** `loop+hold` is above `loop` with
non-overlapping CIs at both horizons in stage A. Otherwise the hold is *not*
layered onto the reported configuration, its stage-B arm is not run, and that
is recorded as the ruling's outcome — not as a choice made after the numbers.
*Expectation: NOT MET.*

**H2 — the inversion on the fixed attacker.** ρ for the `loop` arm (and
`loop+hold` if H1′ is met), reported beside −0.893 and factor 9's band
[−1.000, −0.821]. The inversion **stands** on an arm iff ρ ≤ −0.5; otherwise it
**shifts**, and the 2 × 2 family contrast (diversity vs severance, both
attackers) is reported whichever way it falls. **The direction is committed
toward the reading that hurts the headline:** the Row-B confound analysis
([`movement_objectives_design.md`](movement_objectives_design.md) §5) argues
that removing the churn removes part of what inflates every defence's apparent
score on the movement arm, so the honest prior is that the inversion *weakens*
on the fixed attacker. *Expectation: ρ rises toward 0 but stays ≤ −0.5 — the
inversion stands, weaker; if it does not, that is the finding.*

**H3 — the degeneracy guard (factor 9's four clauses, verbatim), each arm
against the `null` arm.** Progress-denominated (hosts < half the null's, or
successes per action < half); immobility (modal hosts ≤ 1); defence-assists
(any MTD condition's breadth exceeds no-MTD — stage B); activity (places < 3,
entropy < 0.1 bits, or actions outside [0.5×, 2×] the null's). A degenerate
arm's ρ may not be reported as a statement about the inversion. *Expectation:
`loop` clean; both hold arms fire the activity clause (actions collapse) and
possibly the progress clause.*

**H4 — plurality (B4), committed in the unflattering direction.** Pooled path
entropy: both hold arms sit **below** the `loop` arm at both horizons, reported
beside factor 9's 2.714 → 1.682. The `loop` arm's own figure is reported
whichever way it moves (the contract changes routing through its verdict rows,
so it may move plurality too — that is a cost of the fix and is quoted, not
argued away). *Expectation: HELD; the hold collapses toward the FSM chain.*

**H5 — located-target reach, and the probe's sentence.** Database-host reach
rate per arm with a bootstrap 95 % CI, at both horizons, plus footprint at
reach. The probe's *"structural, not tunable"* sentence
([`targeted_objective_probe.md`](targeted_objective_probe.md) §6.3) is
**confirmed** iff the `loop` arm's aggregate reach at 15 000 s stays below the
probe's Gate 0 bar (20 %), and **amended** otherwise. *Expectation: confirmed —
the contract points the attacker at fresh hosts, not at the database hosts
(barrier B-i); reach moves little.*

**H6 — the hold's own rates (not a criterion; the bound on interpretation).**
Held fraction of routing decisions, holds per decision, share of the run spent
holding, fall-through rate against the declared bound of 20, abstention rate,
capability-fallback rate. A material fall-through rate means the hold's result
is partly the bound's, and is said so.

**H7 — the churn, measured at scale.** The share of compromise verbs fired on
an already-owned host in the `null` arm over 5 profiles × 350 seeds (the
record's 89 % was one seed of one profile and a different denominator), and the
contract arms' re-select and re-pop rates. The contract arms' share is 0 by
construction (asserted in the suite).

## 4. Stopping rule, power, and what this is not

Nothing above is re-specified after a row exists: no arm added, no criterion
relaxed, **the hold bound of 20 not re-tuned** whatever the fall-through rate
says. Factor 9's stopping rule binds — this is a supervisor-directed band point,
not a third alignment factor; if the hold does not produce "much better
progress", that is the finding, and the register's T1 annotation already says
why it might not.

Stage A's 350 seeds support the interval comparisons H1/H5 at the probe's
precision. Stage B's 50 seeds support a **rank comparison** (ρ) at five times
experiment 2's seeds, not a significance test on the ranking; no per-profile ρ
is claimed. Breadth is measured on distinct hosts, an event-wise quantity,
because the two attackers are not comparable on time (S3-R).

**The reported configuration moves.** The loop fix is on by default from this
commit; every movement golden (`baseline/golden_movement/`, 70 streams) is
re-captured under it and the pre-change record streams are pinned as a fixture
(`tests/l3_simulation/fixtures/movement_prechange_2026-08-30.json`) that
`fresh_host_contract=False` must reproduce bit for bit. Whether the *hold*
enters the reported configuration is Marc's ruling on the numbers below.

## 5. Reproduce

```
PYTHONPATH=src python data/results/fsm_token_hold/run_probe.py --stage a --workers 7
PYTHONPATH=src python data/results/fsm_token_hold/run_probe.py --stage b --workers 7 [--with-hold]
PYTHONPATH=src python data/results/fsm_token_hold/analyse.py
PYTHONPATH=src python -m pytest tests/l3_simulation/test_movement_fresh_host.py tests/l3_simulation/test_movement_token_hold.py
PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate --mapping v2_partial --overlay-version v3_persistent_backward --retrace --seed 0 --no-fresh-host   # before
PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate --mapping v2_partial --overlay-version v3_persistent_backward --retrace --seed 0                  # after
PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate --mapping v2_partial --overlay-version v3_persistent_backward --retrace --seed 0 --hold           # the hold
```

---

# The verdict, as found

*Pending — appended in a separate commit after the runs, scored against §3
without amending it.*
