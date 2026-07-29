---
status: open
created: 2026-07-29
---

# Audit the eight MTD mechanisms for implementation cost, and make the grid cheap enough to iterate on — starting with the one that spends 128 seconds per run solving a linear program that provably decides nothing

**Motivation, from Marc:** results are coming in and iteration speed is now the
binding constraint on the work. Every experiment cycle is currently paying for
implementation defects in the defender side, and one mechanism dominates that bill
so completely that fixing it alone changes what is affordable.

## State of play

Measured on this branch, 2026-07-29: one `aggregate` run, seed 0, `v2_partial`,
15 000 s horizon, single mechanism, 200 s interval, single-threaded.

**Reproduce with `PYTHONPATH=src python tools/mtd_cost_bench.py`** (committed with
this handoff, so the re-measurement the validation gate asks for uses the same
harness these numbers came from).

**Read the absolute seconds, not the ratio column, for the cheap mechanisms.** The
no-MTD baseline is ~0.1 s, so the ratio is noise-dominated below a second or so and
moves with machine load — re-running the harness under contention read IP Shuffle at
3.2× where the table below has 1.0×. Nothing in the argument rests on those rows.
What is robust, and is what the grid arithmetic uses, is the two-orders-of-magnitude
separation between the seven sub-1.3-second mechanisms and the one that takes two
minutes.

| mechanism | wall clock | × no-MTD | interrupts | in default pool |
|---|--:|--:|--:|:--|
| *(no MTD)* | 0.09 s | 1.0 | 0 | — |
| IP Shuffle | 0.10 s | 1.0 | 75 | yes |
| Port Shuffle | 0.14 s | 1.6 | 49 | no |
| Host Topology Shuffle | 0.16 s | 1.7 | 75 | no |
| User Shuffle | 0.16 s | 1.8 | **0** | no |
| Service Diversity | 0.45 s | 4.8 | 50 | yes |
| OS Diversity | 0.63 s | 6.7 | 53 | yes |
| Complete Topology Shuffle | 1.26 s | 13.5 | 75 | yes |
| **OS Diversity Assignment** | **127.73 s** | **1366.6** | 49 | no |

**What that costs a grid.** On the 23-condition × 5-profile × 2-arm × 30-seed
matrix this project last designed, `OSDiversityAssignment` at the 200 s interval is
300 runs at ~128 s ≈ **10.7 hours**, against roughly **1.75 hours for all 6 600
other runs combined**. One mechanism is ~85 % of the bill. It is not in the
inherited default pool, so it only appears when a grid names all eight explicitly —
which the demonstration-arms grid did, and which any per-mechanism table for the
dissertation will want to.

### Why OSDiversityAssignment is slow — profiled, not guessed

`cProfile` over one full run (285 s under profiler overhead; 128 s without):

- `mtd_operation` accounts for **99.7 %** of run time.
- `objective()` is called **75 times** — once per mutation.
- Of that, ~86 s is CBC actually solving, and **~200 s is PuLP building the model
  in Python**: 21.3 million `LpAffineExpression.__init__` calls, 29.6 million
  `addInPlace` calls. A further **42 s is `writeMPS`** — serialising a
  243 000-line MPS file to disk, 75 times.
- The model is **60 544 continuous variables** (`|C|=16` powerset of four OS types
  × `|M|=2` clients × 44×43 ordered node pairs) plus 168 binaries.

**And the solve decides nothing.** CBC's own log, every time:

```
Cgl0004I processed model has 0 rows, 0 columns (0 integer (0 of which binary)) and 0 elements
Cbc3007W No integer variables - nothing to do
```

Presolve annihilates the model. The reason is visible in the formulation: the
binary variables `s[(variant, node)]` — the OS assignment, the thing the Diversity
Assignment Problem exists to choose — appear in **no objective term** and in exactly
one constraint (`exactly one variant per node`). The constraints that would couple
`s` to the flow variables `f` are **commented out** at
[`osdiversityassignment.py:229-233`](../../mtdnetwork/mtd/osdiversityassignment.py#L229-L233)
— and they are constraint 7 in the file's own docstring ("the amount of flow out of
/ into a routing node must be 0 if that node is compromised"). So the returned
assignment is an arbitrary feasible point, and the mechanism pays 128 s per run to
obtain it.

**Three further defects in the same file**, each independently worth the next
session's attention:

1. **The cache never survives.** `mtd_operation` guards the solve behind
   `self.last_result` and a `_checkpoint` ladder, intending to re-solve only when
   the compromise ratio crosses a threshold. But
   [`mtd_scheme.py::_mtd_register`](../../mtdnetwork/component/mtd_scheme.py)
   does `if isinstance(mtd, type): mtd_strategy = mtd(network=self.network)` — a
   **fresh instance per registration** — so `last_result` is `None` at every
   mutation and the ladder resets. That is why `objective()` runs 75 times rather
   than the ≤ 8 the design intends. **This is architectural, not local:** any
   mechanism carrying state across mutations is defeated the same way, including
   `ServiceDiversity`'s `shuffles` parameter and anything added later.
2. **Redundant constraint emission.** Inside `for c in C: for a in M:`, several
   constraints re-bind `a` in their own comprehension
   (`lpSum([f[(c, a, x, a)] for a in M for x in N ...])`), so they do not depend on
   the outer loop and are emitted identically 32 times.
3. **A malformed expression.** Line 222 sums `f[...]` (a variable) with
   `f[...] <= const` (a constraint object) inside one `lpSum`. Whatever that
   evaluates to, it is not the constraint the docstring describes.

### Two other things the measurements turned up

- **Complete Topology Shuffle is 13.5× no-MTD and is in the default pool**, so
  every scheme arm pays it. It calls `network.gen_graph()` (a full regeneration)
  plus `add_attack_path_exposure()` and `add_shortest_path()` on every mutation.
  Whether all three are needed per mutation — and whether the two scorer calls are
  measurement rather than mechanism — is the second-highest-value question here.
- **User Shuffle produces 0 interrupts**, at 200 s, over a full horizon. It is the
  only mechanism that never interrupts the attacker. The recent intent-audit commit
  (`6181305`) claims to have made "User Shuffle finally able to block", so this may
  be a live regression, a scope limit of that fix, or correct behaviour — it is
  **not** established here either way, and it is a *correctness* question that
  happens to have surfaced during a *performance* audit.

## Recommended approach

**Do the classification before the optimisation.** Everything above is substrate
behaviour, so per [`../workflows/guardrails.md`](../workflows/guardrails.md) none of
it is a "bug" until it has been classified against
[`../implementation/mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md)
(§c procedure) and Marc has ruled. The commented-out DAP constraints in particular
look like an *unfinished implementation* rather than a defect — Brown/Zhang lineage
may never have completed that formulation — and the disposition changes what the fix
is. Report the classification first; do not open with a patch.

1. **Establish a behaviour-preserving harness before changing a line.** Capture
   golden `MovementRecord` streams and baseline `AttackStatistics` rows for every
   mechanism × several seeds × both arms, on the current code. Any optimisation is
   then verified by **field-for-field equality** of those streams, not by "the
   numbers look similar". This is the whole safety property: a speed-up that moves a
   result silently invalidates every number this project has published.
2. **Fix the re-instantiation seam first**, because it is cheap, general, and
   unblocks the rest. Register mechanism *instances* once and reuse them, or give
   the scheme an instance cache keyed by class. Verify the golden streams are
   unchanged for the seven stateless mechanisms (they should be, exactly) and
   report the change for `OSDiversityAssignment` as expected-and-explained.
3. **Then decide what `OSDiversityAssignment` should be**, on Marc's disposition,
   from three options the next session should cost and rank rather than assume:
   - **Repair the formulation** — restore the `s`↔`f` coupling so the MIP decides
     something. Most faithful to the cited DAP; also the most work, and it makes the
     mechanism *slower*, not faster, since presolve will no longer annihilate it.
   - **Replace the solve with what it actually computes** — if the assignment is
     arbitrary-feasible today, an explicit round-robin or random assignment is
     behaviourally equivalent, ~1000× faster, and *honest* about being a heuristic.
     Every published number that used this mechanism stays valid.
   - **Withdraw it from the mechanism pool** and record why. It is already outside
     the inherited default pool; the cost of keeping it may exceed its evidential
     value.
   Whichever is chosen, the reasoning belongs in a tracked record — this mechanism
   appears in the dissertation's defence family and an examiner may ask what it does.
4. **Take the cheap wins in the other mechanisms only where they are provably
   behaviour-neutral**: the O(n²) `seen`-list membership tests in
   `HostTopologyShuffle`, the recomputed `max()` inside the per-host loop in
   `calculate_variant_compromise_prob`, and the per-mutation `get_graph_copy()` that
   is discarded unsolved. None of these is worth risking a behaviour change for —
   they are already sub-second — so take them only if the golden streams hold.
5. **Re-measure and publish the table above** as the "what a grid costs" reference,
   so the next experiment can size itself instead of discovering the bill at row 207.

**Alternatives considered.** *Parallelising harder instead of fixing the
mechanisms* — rejected: it buys a constant factor against a 1366× defect, and the
machine has 8 cores. *Caching solves across runs* — rejected: it would couple runs
that must stay independent for SIM-05, and the assignment depends on live network
state. *Shortening the horizon or the seed count to fit the budget* — rejected as
the wrong lever; that trades statistical power for compute when the compute is being
wasted rather than used.

## Validation gate

Done when:

1. Every mechanism's disposition is classified against the intent spec and recorded
   — conforms / conforms-to-superseded-lineage / documented-nowhere — with Marc's
   ruling on the ones that are candidates.
2. Golden record streams exist for all eight mechanisms and are **bit-identical**
   before and after every change made for performance reasons; where a change is
   *intended* to alter behaviour (the DAP repair or replacement), the difference is
   shown, explained and dispositioned rather than absorbed.
3. The per-mechanism cost table is re-measured with `tools/mtd_cost_bench.py` on an
   idle machine and over several seeds, and committed with the grid-cost arithmetic
   that follows from it. If the harness needs changing to answer a question, change
   it there rather than in a throwaway script, so the next re-measurement is
   comparable again.
4. `OSDiversityAssignment`'s fate is ruled and recorded, including what happens to
   the runs already published against it (`experiment_02_findings.md` does not use
   it; the demonstration-arms grid does).
5. The User Shuffle zero-interrupt question is answered — regression, scope limit,
   or correct — with evidence, or explicitly deferred to its own handoff.
6. Full suite green (576 tests at the time of writing), including the substrate
   goldens.

## Hard constraints

- **Speed may never move a number.** Behaviour-preserving is the gate; a faster run
  that changes a record stream is a failed optimisation, not a trade-off.
- **"Bug" is a verdict, not a first impression.** Classify against the intent spec
  before calling any of this a defect; only Marc's disposition makes it fixable.
  This applies with full force to the commented-out DAP constraints.
- **The S2 action-set freeze holds**, and the defender pool is frozen by scope —
  this handoff optimises existing mechanisms and does not add, remove or re-tune
  them. Withdrawing `OSDiversityAssignment` (option 3c) is a scope decision for
  Marc, not for the session.
- Determinism / SIM-05: mechanisms draw from the substrate's seeded dice, so any
  change to draw *order* changes results even when the logic is equivalent. Watch
  for this specifically when removing redundant work.
- Australian English; branch and commit rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.

## Reading list

- `mtdnetwork/mtd/osdiversityassignment.py` — the whole file; §`objective()` for the
  formulation, lines 229–233 for the commented-out coupling, `mtd_operation` for the
  checkpoint ladder that never fires.
- `mtdnetwork/component/mtd_scheme.py` — `_mtd_register`, the re-instantiation that
  defeats every mechanism's per-instance state; also the four mechanisms commented
  out of `_mtd_strategies`.
- `mtdnetwork/mtd/completetopologyshuffle.py` and `mtdnetwork/component/network.py`
  (`add_attack_path_exposure`, `add_shortest_path`, `gen_graph`) — the second cost
  centre.
- [`../implementation/mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md)
  §c — the classification procedure, before anything is called a bug.
- [`../implementation/pipeline/ogasp/demonstration_arms_cross_examination.md`](../implementation/pipeline/ogasp/demonstration_arms_cross_examination.md)
  §6 — where the 128 s figure first surfaced, and the shared-`data/results` hazard
  any re-measurement run should avoid.

## Out of scope (explicitly)

- Adding, removing or re-tuning MTD mechanisms as a *research* choice. This is an
  implementation audit; the defender pool is frozen.
- Tay's `mtd_ai` scheme. It raises in the current wiring (it expects its RL agent to
  supply the technique) and is deferred to the evaluation/ablation phase by standing
  scope.
- Re-running any experiment to new conclusions. Re-measurement here is for the cost
  table and the golden streams, not for findings.
- Attacker-side performance. The movement layer is not the bottleneck: a no-MTD run
  is 0.09 s.
- Dissertation prose.
