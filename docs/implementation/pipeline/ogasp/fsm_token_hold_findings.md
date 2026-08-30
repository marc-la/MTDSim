---
status: durable — pre-registered 2026-08-30 (042afc5f), verdicts landed 2026-08-30; the headline finding (H0) is spun out to 2026-08-30_headline_on_restored_substrate.md
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

*Everything above the fold was committed before the runs existed (`042afc5f`).
Everything below reports against those criteria without amending them. One
arithmetic slip above is corrected rather than edited: stage B without the hold
arm is 4 400 runs (8 conditions × 50 seeds × [1 inherited + 2 arms × 5
profiles]), not 2 400.*

**The runs.** Stage A: 14 700 runs, zero errored cells. Stage B: 4 400 runs,
zero errored cells; the hold arm was not run (H1′ NOT MET, below).
`data/results/fsm_token_hold/` (untracked, as every results directory is);
`analyse.py` regenerates `verdict.txt` / `verdicts.json`.

## H1 — HELD. The loop fix is "much better progress"; the hold rule is not

Pooled distinct hosts under no MTD, five profiles × 350 seeds, 95 % CI:

| arm | 15 000 s | 30 000 s | gap to the inherited attacker closed |
|---|--:|--:|--:|
| inherited attacker | 33.18 ± 0.90 | 35.83 ± 0.92 | — |
| `null` (contract off, hold off — the pre-2026-08-30 attacker) | 5.13 ± 0.11 | 9.01 ± 0.19 | 0 |
| **`loop` (the reported configuration)** | **7.92 ± 0.20** | **14.49 ± 0.37** | **+9.9 % / +20.5 %** |
| `hold` (Jin's rule on the old attacker) | 2.66 ± 0.13 | 4.38 ± 0.20 | −8.8 % / −17.3 % |
| `loop+hold` | 3.26 ± 0.18 | 5.18 ± 0.25 | −6.7 % / −14.3 % |

On the `aggregate` profile alone (the probe's denominator): 5.62 → 9.11 at
15 000 s, 10.61 → 18.47 at 30 000 s.

Read beside the alignment programme's two instruments, this is the third
answer to the same question and the first positive one: factor 8 closed
≤ 7.4 % of the breadth gap, factor 9 *widened* it by 10.4 %, the loop fix
closes **9.9 % at the operating horizon and 20.5 % when the attacker is given
T2's longer one**. The two negatives were procedural-*order* instruments; the
positive is a host-*selection* repair — which is what
[`movement_objectives_design.md`](movement_objectives_design.md) §1 argued the
objective actually lives on.

**Jin's rule does not produce "much better progress" — it produces less.** The
opaque hold on its own lands below the null with disjoint CIs at both horizons,
and layered on the loop fix it takes back most of what the fix bought. **H1′
NOT MET**, so the hold is not layered onto the reported configuration and its
headline arm was not run — the ruling's ordering, executed by the numbers. The
mechanism is in H6: the hold consumes **77 % of the run** holding, at 2.1 holds
per consulted decision, and the FSM-legal share of the CTI out-sets is small
enough that 42 % of decisions are held at all. The "slower" Jin accepted is
most of the clock.

One profile is the exception worth naming rather than averaging away:
`objective_exfiltration_impact` gains nothing from the loop fix (6.24 → 7.96
at 15 000 s but 9.67 → 8.85 at 30 000 s) and is the only profile the hold does
not crush (6.64 / 9.73). Its net routes through the compromise verbs rarely
enough that host selection is not its bind; it is the profile on which every
one of these instruments has always been closest to the null.

## H3 — the guard: `loop` clean, both hold arms DEGENERATE

| arm @ horizon | hosts (modal) | succ/act | actions | places | entropy | verdict |
|---|--:|--:|--:|--:|--:|---|
| `null` @15k | 5.13 (5) | 0.659 | 325.4 | 13.12 | 2.805 | ok |
| `loop` @15k | 7.92 (6) | 0.487 | 325.9 | 13.16 | 2.803 | ok |
| `hold` @15k | 2.66 (**0**) | 0.202 | 309.7 | 9.97 | 0.731 | **DEGENERATE** — succ/act < half, immobile |
| `loop+hold` @15k | 3.26 (**0**) | 0.166 | 314.3 | 10.04 | 0.771 | **DEGENERATE** — succ/act < half, immobile |
| `null` @30k | 9.01 (10) | 0.669 | 649.3 | 13.24 | 2.811 | ok |
| `loop` @30k | 14.49 (10) | 0.441 | 648.9 | 13.31 | 2.806 | ok |
| `hold` @30k | 4.38 (**0**) | 0.197 | 629.6 | 10.77 | 0.682 | **DEGENERATE** — hosts < half, succ/act < half, immobile |
| `loop+hold` @30k | 5.18 (**0**) | 0.139 | 641.9 | 10.79 | 0.735 | **DEGENERATE** — succ/act < half, immobile |

The prior was wrong about *which* clause: the activity clause did not fire
(actions per run barely move, because holds are counted as time inside a visit,
not as actions), the immobility clause did — **the modal hold run compromises
nothing**, the exact signature factor 8's α = 1 and factor 9's α = 1 showed.
Every reading of Jin's rule now has a measured degenerate point: transparent
(factor 9's α = 1, 2.18 hosts, modal 0) and opaque (here, 2.66 hosts, modal 0).
The defence-assists clause, scored in stage B, is 0/7 on both arms run.

Two costs of the contract itself, quoted rather than argued away: the `loop`
arm's **blocked fraction rises from 15.3 % to 25.4 %** (the fresh-host guard
converts a would-be re-compromise into a blocked visit when the visible queue is
dry — the "pure block" cost the design warned of, now measured at ~10 points),
and its successes-per-action falls from 0.659 to 0.487 for the same reason plus
the three verdict rows now reading failure where they always read success. The
attacker acts less "successfully" per action and owns more hosts: the old
figure was counting re-compromises as successes.

## H4 — HELD. Plurality collapses under the hold, not under the fix

Pooled path entropy (bits) / distinct places per run: `null` 2.805 / 13.12,
`loop` 2.803 / 13.16, `hold` 0.731 / 9.97, `loop+hold` 0.771 / 10.04 at
15 000 s (2.811 / 2.806 / 0.682 / 0.735 at 30 000 s). **The loop fix costs
plurality nothing** — the contract changes which host a verb acts on, not which
tactic the token walks to — so axis 3's demonstrated badge is untouched by the
reported-configuration change. The hold takes the attacker from 2.80 bits to
0.73, far below factor 9's already-degenerate 1.682: the verb chain has become
the FSM's chain, as the T1 annotation said it would, and the record says so.

## H5 — the probe's "structural, not tunable" sentence: CONFIRMED, with a rider

| arm | reach @15k (aggregate) | reach @30k (aggregate) | footprint at reach @30k |
|---|--:|--:|--:|
| inherited | 0.611 | 0.700 | 28.3 |
| `null` | 0.000 | 0.017 | 11.5 |
| `loop` | **0.014** [0.003, 0.029] | **0.146** [0.111, 0.183] | 17.9 |
| `hold` | 0.003 | 0.003 | 5.7 |
| `loop+hold` | 0.003 | 0.014 | 12.6 |

At the operating horizon the fixed attacker reaches the crown jewels in 1.4 %
of unopposed runs against the probe's 20 % Gate 0 bar: the located objective
stays degenerate on the movement arm, and the sentence in
[`targeted_objective_probe.md`](targeted_objective_probe.md) §6.3 stands.
The rider: at 30 000 s the fixed attacker's reach is **14.6 %** (pooled 9.5 %)
— an order of magnitude above the null's at the same horizon and within reach
of the bar. The barrier is still B-i (no navigation toward the target — the
footprint at reach, 17.9 hosts, says the reaches are still frontier collisions),
but the fix has removed enough of B-iii's breadth cap that horizon alone now
moves reach materially. What a `movement_targeted` host-selection variant would
add is now a sharper question than the probe could pose.

## H6 — the hold's own rates (the bound on what it could have done)

| arm @ horizon | decisions | held | holds / decision | share of run holding | fell through (bound 20) | abstained | capability fallbacks |
|---|--:|--:|--:|--:|--:|--:|--:|
| `hold` @15k | 564 843 | 41.8 % | 2.10 | **77.2 %** | 1.18 % | 43.8 % | 0.77 % |
| `loop+hold` @15k | 577 412 | 41.0 % | 2.05 | 76.1 % | 1.13 % | 44.8 % | 0.75 % |
| `hold` @30k | 1 141 262 | 42.3 % | 2.12 | 77.5 % | 1.18 % | 43.4 % | 0.38 % |
| `loop+hold` @30k | 1 175 551 | 41.1 % | 2.05 | 76.1 % | 1.12 % | 44.8 % | 0.37 % |

The bound acted at ~1.2 % of decisions, so the result is the rule's, not the
backstop's. The abstention rate — **44 % of routing decisions offered no
FSM-legal destination at all** — is the number that explains why "leave the
token there" cannot do what the meeting expected: at nearly half the decisions
the CTI out-set contains nothing the inherited FSM would run next, the rule
declines to act (the alternative is a stall), and the token moves off-chain
anyway; at the other half it pays, on average, two extra dwells to get back on
it. The CTI structure and the FSM's chain are not two orderings of the same
verbs; they mostly do not overlap.

## H7 — the churn, at scale

In the `null` arm **44.7 %** of compromise verbs fire on a host already owned at
15 000 s (51.7 % at 30 000 s; 40–52 % by profile). The record's 89 % was one
seed of one profile on a different denominator (`EXPLOIT_COMPROMISED` events
only, where a re-compromise is "successful" by construction); the per-verb
figure is the honest one and it is still close to half the attacker's offensive
actions. The `loop` arm's share is 0 by construction (the invariant is asserted
in the suite); it re-selects 33 times and re-pops 25 owned hosts per 15 000 s
run to keep it so. The `hold` arm's churn falls to 9.5 % without any guard —
the FSM chain pivots after a compromise — but at the cost above.

## H0 — FIRED. The inversion on record does not reproduce on the restored substrate — on the *unfixed* attacker

This is the finding of the record, and it is not about either mechanism.

Stage B, eight conditions × 50 seeds × eleven arms (4 400 runs, 0 errored),
pooled breadth suppression at 200 s, experiment 2's E5 construction verbatim:

| mechanism | inherited (exp. 2, 2026-07-29) | **inherited (today)** | `null` movement | `loop` movement |
|---|--:|--:|--:|--:|
| Service Diversity | 90.4 % | **93.6 %** | 28.9 % | 38.5 % |
| OS Diversity | 88.8 % | **58.0 %** | 8.2 % | 10.5 % |
| IP Shuffle | 22.1 % | **67.5 %** | 93.0 % | 95.2 % |
| Complete Topology Shuffle | 18.2 % | **55.5 %** | 91.4 % | 94.3 % |
| random / simultaneous / alternative multi | — | 66.6 / 65.2 / 65.8 % | 72.3 / 90.1 / 72.7 % | 81.1 / 93.5 / 80.8 % |
| no-MTD breadth | 38.40 | 32.96 ± 2.49 | 5.03 ± 0.29 | 7.62 ± 0.51 |

**ρ(`null`) = −0.071** against a kill criterion of ≤ −0.5, experiment 2's
−0.893 and factor 9's band [−1.000, −0.821]. The pre-registered consequence
applies: **no ρ in this record is a statement about the inversion's response
to the fix**, and H2 is descriptive — ρ(`loop`) = −0.036, the two movement
orderings differing only in the `random` / `alternative` tie. Defence-assists:
0/7 on both arms.

**Where it went.** The movement attacker's ordering is the one on record —
severance crushes it (IP Shuffle 93 %, Complete Topology 91 %), diversity
barely touches it (OS 8 %, Service 29 %) — and the fix does not move it. What
moved is the **inherited attacker**: OS Diversity's suppression of it fell from
89 % to 58 % and IP Shuffle's rose from 22 % to 68 %, so its ordering is now
Service Diversity ≫ everything else ≈ 55–68 %, and the two attackers no longer
disagree about the family that matters. Every artefact the −0.893 rests on
predates the **2026-08-27 substrate restoration** (`d127f443`: OS Diversity
made a selective redraw under D-18, the OS-gated exploit channel reinstated
under D-19, the MTD pool restored to seven mechanisms, every substrate golden
re-baselined) — experiment 2's rows are dated 2026-07-29, factor 9's
2026-08-03, the probe's 2026-08-25 — and no record re-measured the inherited
attacker's defence response after it. **This record is the first to, and the
inversion is not there.** The multi-mechanism conditions are also no longer the
same conditions: the schemes now draw from the restored seven-mechanism pool,
so `random` / `simultaneous` / `alternative` here are not experiment 2's.

**What this record may and may not say.** It may say: the loop fix does not
change the movement attacker's defence ordering (the two movement columns
agree to a tie), and the movement attacker's severance-versus-diversity pattern
is robust to the fix. It may not say that the inversion stands or shifts,
because the phenomenon it was pre-registered to decompose is absent from the
null arm. Whether the inversion returns under a decomposition of `d127f443`
(which repair moved the inherited attacker — the selective OS redraw, the OS
gate, or the enlarged pool behind the multi schemes) is a re-establishment of
experiment 2, not a fix to this record, and it is spun out:
[`2026-08-30_headline_on_restored_substrate.md`](../../../handoffs/2026-08-30_headline_on_restored_substrate.md).

## What this leaves

1. **The reported configuration is the fixed attacker, and it costs nothing
   the criterion scores.** Breadth +54 % at the operating horizon (5.13 →
   7.92) and +61 % at 30 000 s, plurality unchanged (2.805 → 2.803 bits), the
   defence ordering unchanged, the churn gone (45 % → 0 of compromise verbs).
   Axis 3's DEMONSTRATED badge is untouched; no badge moves.
2. **Jin's rule is a measured negative in both of its readings.** The
   transparent hold was factor 9's α = 1 (2.18 hosts, modal 0); the opaque hold
   is 2.66 hosts, modal 0, 77 % of the run spent holding, plurality 0.73 bits.
   The standing question for Jin (which reading he meant) is answered by
   measuring both: neither produces progress, because at 44 % of routing
   decisions the CTI out-set contains nothing the inherited FSM would run next.
   Under T5 — under-performing is acceptable, not progressing is not — the
   fixed attacker progresses (H1) and the held one does not (H3); the
   procedural-order confound is now refuted three ways (factors 8, 9, and the
   hold) and the host-selection repair is what progress actually needed.
3. **The located objective stays degenerate at the operating horizon (1.4 %)
   and is no longer hopeless at T2's (14.6 %).** The probe's fork (§7.3 there)
   is sharpened, not decided: B-i is still the bind, B-iii is materially lifted.
4. **The headline inversion is currently unsayable on the current substrate**
   — not because of this work, and it would have been unsayable whether or not
   the loop fix landed. That is the item to put to Jin with these numbers,
   before the results-outline review (T4).
