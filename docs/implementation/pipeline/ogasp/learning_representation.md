---
status: durable
created: 2026-08-01
updated: 2026-08-01
topic: "L3 criterion axis 7, generalisation — the learner-representation decision: why the destination-only key cannot express a precondition constraint, the ranked candidate keys with their measured per-cell observation budgets, and the ruling that the one-bit precondition-satisfied context is the honest minimum that both expresses the dependency and stays dense"
---

# The learner representation — choosing a key that can express "this tactic pays *here*"

**Status:** durable design record, Part A of the procedural-rigidity handoff
([`../../../handoffs/2026-07-29_learning_under_procedural_rigidity.md`](../../../handoffs/2026-07-29_learning_under_procedural_rigidity.md)).
It settles the representation **before any code is written**, in the shape the
prior sweep studies used: a decision argued against ranked alternatives, with the
sparsity budget measured rather than estimated, and the exploration guarantee
preserved. The build, its pre-registration, and the sweep are separate commits
that follow; this record is the argument they rest on.

**What this record does not do.** It moves no badge, changes no value, and runs no
comparative experiment. It chooses the key the generalised learner will be built
on and states why, so the build is a transcription of a settled decision rather
than a decision taken at the keyboard.

## 1. The problem, stated precisely — it is representational, not a matter of tuning

The axis-7 learner keeps a within-run belief `Q(b)` about whether acting at a
tactic-place `b` pays, keyed on the **destination place alone**
([`learning_capability.md`](learning_capability.md) §3.1). That key can represent
only the *marginal* success rate of a tactic — averaged over every phase-context
the attacker has tried it in. The sweep that built the learner found it operates
and makes the attacker worse: blocked fraction falls from 91 % to 21 % as the
capability rises, while compromise breadth falls from 6.5 hosts to 0.8 and
exploitation falls from 13 % of the attacker's successes to 1 % (§7.6). The
diagnosis there was that the binary routing verdict is not a progress signal; the
diagnosis *here* is the mechanism one layer down, and it is about the key.

Being blocked is a function of **state**: an exploit fails because this host has
not been port-scanned yet. So the quantity the attacker would need to learn is the
success probability of a tactic **conditioned on its current phase-state**. The
destination-only key marginalises over phase-state, and marginalising discards
exactly the variable the precondition depends on. No quantity of runs repairs a
representation that cannot express the dependency — the learner keyed on the
marginal converges to a *correct* marginal that is nonetheless the wrong thing to
condition a routing decision on.

**The measured proof that the marginal conflates two regimes.** The base
traversal (the ablation arm, κ = 0) was run across the pre-registered matrix and
every verdict-bearing action was tallied twice: once under the destination-only
key, and once split by whether the substrate's precondition was satisfied at that
dispatch — ground truth, from the record's `blocked` flag, which is set exactly on
`PRECONDITION_UNMET`. Pooled over profiles, no MTD
([`data/results/learning_representation/`](../../../../data/results/learning_representation/),
`measure_budget.py`):

| mapping | success rate when **ready** | success rate when **not ready** |
|---|--:|--:|
| `v1_ckc_total` | 0.875 (n = 9 640) | **0.000** (n = 11 420) |
| `v2_partial` | 0.809 (n = 11 945) | **0.000** (n = 2 648) |

An unmet precondition is a **deterministic failure** — not-ready pays 0.000 across
more than fourteen thousand observations on both mappings. The marginal a
destination-only learner sees is therefore a mixture of a genuinely-paying regime
(≈ 0.8–0.88) and a certain-failure regime, weighted by how often the attacker
happens to arrive ready. Per-place, on `v2_partial` where the attacker compromises
hosts, the dilution is stark:

| place (aggregate profile) | marginal | ready | not ready |
|---|--:|--:|--:|
| `execution` | 0.34 (n = 471) | 0.61 (n = 260) | 0.00 (n = 211) |
| `initial-access` | 0.11 (n = 200) | 0.42 (n = 52) | 0.00 (n = 148) |
| `privilege-escalation` | 0.40 (n = 247) | 0.65 (n = 153) | 0.00 (n = 94) |
| `command-and-control` | 0.99 (n = 673) | 1.00 (n = 666) | 0.00 (n = 7) |

`execution` pays 0.61 when the host has been scanned and 0.00 when it has not; the
marginal 0.34 is neither, and it is what the current learner downweights
`execution` on — below `command-and-control`'s 0.99, which needs no precondition.
That downweighting is the self-reinforcing loop the freeze record named
([`model_scope_freeze.md`](model_scope_freeze.md) §5): avoiding `execution` drives
the phase-state distribution further from the states in which `execution` would
have worked, which depresses its marginal further. The learner is optimising a
correct estimate of the wrong quantity.

## 2. The candidate keys, ranked coarsest to finest

Four keys, from the one that cannot express the dependency to the ones that can,
with the reason in both directions. The axis is *faithfulness* against
*observation budget per cell*: a finer key represents more, and spends the run's
bounded evidence over more cells, so the Laplace prior that holds an unvisited
cell at 0.5 dominates a sparser table.

### 2a. `(destination tactic)` — today

The marginal. Its whole virtue is density — §3 shows it is the least sparse of the
four — and its fatal defect is §1: it cannot express a state-conditioned
constraint, because the state is exactly what it averages over. Kept in the
ranking as the floor the generalisation must beat, not as a live option.

### 2b. `(previous tactic, destination tactic)` — the pairwise chain form

Key the belief on the *transition* into a place rather than the place. When a
verdict is observed at `b`, credit the pair `(a, b)` where `a` is the place the
token came from; when routing from `a`, consult `Q(a, b)` for each candidate `b`.
The predecessor is already in the state's trajectory, and the composition seam
already carries the source place at every routing decision, so this needs **no new
observation channel and no eligibility trace** — it is one-step, pairwise credit,
not trajectory credit, so it stays inside the no-RL constraint. It is also the
option closest to what a campaign-shaped attacker would plausibly track: "coming
from a port scan, does exploiting pay?"

**Why it can express the dependency, and only partly.** If the walk goes
`discovery → execution`, the pair `(discovery, execution)` accrues the ready-regime
successes; if it goes `command-and-control → execution`, the pair accrues the
not-ready failures. So the pair distinguishes the contexts *to the extent the
immediate predecessor determines readiness*. It does not fully: the substrate's
`curr_ports` survives across intervening tactics until the host changes, so
`discovery → command-and-control → execution` is ready at `execution` although the
immediate predecessor is not `discovery`. The pair mislabels that case. It is a
one-step proxy for a state that has longer memory.

**And it is the sparsest of the three that work** — §3 measures it at roughly four
times the destination-only cell count, with the fraction of near-prior cells
doubled. It pays the most for a faithfulness it delivers only partially.

### 2c. `(destination tactic, current phase)` — the phase table

Key on the destination crossed with the attacker's current lifecycle phase (the
consensus stage, six values). This is the general form the handoff named, and it
can represent phase-dependence directly. Two costs. It is the second-sparsest —
§3 measures ≈ 2× the destination-only cells — because most of the fifteen-by-six
table is unreachable but the reachable part still fragments the budget. And most
of that resolution is wasted on *this* dependency: the precondition is a single
bit (scanned or not), and a six-valued phase spends five degrees of freedom the
constraint does not use. A phase table would earn its cost against a dependency
that varied smoothly with progress; the precondition does not.

### 2d. `(destination tactic, precondition-satisfied?)` — the one-bit context

Key on the destination crossed with a single bit: is the destination's declared
precondition satisfied in the attacker's current phase-state? This is the honest
minimum. §1 measured the bit to be the **exact** variable — not-ready is a
deterministic failure — so one bit captures the whole dependency and a finer key
captures no more of it. The attacker learns "this pays when I am ready for it"
rather than memorising a phase table, which is also the more defensible claim
about what an intruder tracks: an operator knows a service must be examined before
it can be exploited, and knows whether they have examined this one.

**The bit is derived in-layer, which is what keeps it clean.** `ready?(b)` is
computed from the attacker's own trajectory against a **declared** precondition
relation (Part B), not by reading substrate internals. The ordering constraints of
the action layer are constraints on the attacker's own tradecraft, so declaring
them and consulting them is a statement of attacker competence, not privileged
information about the host or the defender — the ruling in the handoff (§B, Marc
2026-07-29) settles this, and nothing here reads the defender, so the
scheme-awareness exclusion is untouched.

## 3. The sparsity budget, measured

Mean distinct cells that receive at least one verdict **per run**, and the
fraction of those cells holding fewer than three observations (the point below
which the Laplace prior still dominates: three all-success observations put `Q` at
0.80, one puts it at 0.67, zero at 0.50). Base traversal, averaged over the five
profiles.

| key | v1 cells | v1 frac < 3 obs | v2 cells | v2 frac < 3 obs |
|---|--:|--:|--:|--:|
| `(dst)` | 13.3 | 0.15 | 7.9 | 0.09 |
| `(dst, ready?)` | 15.0 | 0.16 | 12.1 | 0.19 |
| `(dst, phase)` | 26.0 | 0.29 | 17.1 | 0.26 |
| `(prev, dst)` | 54.6 | 0.32 | 35.2 | 0.29 |

The one-bit key costs almost nothing: it adds one to three cells over the marginal
on both mappings, and the fraction of near-prior cells rises only from 0.15 to 0.16
(v1) and 0.09 to 0.19 (v2). The reason it stays dense is structural — a place is
visited in only one or two of its two possible ready-states in most runs, so the
cross-product barely widens. The phase table doubles the cell count and the
near-prior fraction; the pairwise form roughly quadruples the cells and doubles the
near-prior fraction. Under MTD the pattern holds, with `(dst, ready?)` rising to
16.5 (v1) and 13.1 (v2) cells as forgetting re-opens cells the run had filled — a
mild increase the prior absorbs.

**The budget confirms the ranking the faithfulness argument implied.** The two
finer keys spend two-to-four times the evidence per cell to represent a dependency
the one bit already captures exactly. Sparsity is not the reason to reject them —
the run is long enough that even the pairwise key is not catastrophically sparse —
but there is no faithfulness gain to buy with the density they give up, so the
trade is strictly worse.

## 4. The ruling — `(dst, ready?)`, feeding the learner

**The generalised learner keys its belief on `(destination tactic,
precondition-satisfied?)`.** It is the smallest key that expresses the
constraint, it captures the constraint exactly rather than partially (the bit is
the deterministic variable, §1), and it is the densest of the keys that work
(§3). The pairwise and phase keys are rejected not for sparsity alone but because
they spend density on resolution the dependency does not use.

**It feeds the learner rather than only biasing routing.** The handoff's item 6
distinguishes a static declared bias toward the ready destination from letting the
readiness signal enter the credit counts. The second is the one that generalises
the *capability*: the attacker learns *which contexts pay* from a signal that
carries the precondition, so the belief itself becomes state-conditioned, rather
than a fixed nudge sitting beside an unchanged marginal belief. The first would
ship sooner and generalise nothing. Feeding the learner is chosen, and §1's
measurement supports it — because the ready and not-ready regimes have genuinely
different success rates (0.61 vs 0.00 for `execution`), a belief split by the bit
has real, differently-signed evidence to accumulate in each cell, which a
routing-only bias would leave on the floor.

**What this preserves.** The estimator is unchanged: per cell `(b, ready?)` the
learner keeps Laplace counts of success and failure verdicts and estimates
`Q(b, ready?) = (s + 1)/(s + f + 2)`, so an unvisited cell sits at exactly 0.5 and
is never zeroed — **exploration survives by construction**, the property
[`learning_capability.md`](learning_capability.md) §3.1 depends on, and the
`may_zero = False` claim stays a proof rather than a hope. The composition,
multiplicative-then-renormalised, and the forgetting rule, a uniform decay on every
MTD interrupt, are unchanged; only the cell key gains the bit. At κ = 0 the
modulator still returns no factors, so the generalised learner's null arm is
bit-identical to a run without it, exactly as the destination-only learner's is.

**The honest limit that travels with the ruling.** The bit the learner keys on at
routing time is a *prediction* — `ready?(b)` computed from the trajectory and the
declared precondition relation before the verb runs — whereas §1's split used
ground truth after the fact. A declared relation that mispredicts readiness weakens
the signal in proportion to its error, and measuring that prediction accuracy
against the `blocked` ground truth is a validation gate for Part B, not something
this record can claim. What §1 does establish is the ceiling: a perfectly-declared
bit recovers a deterministic separation, so the representation is worth building; a
mispredicting bit is a weaker version of the same mechanism, never a different one.

## 5. What Part B and Part C inherit from this ruling

- **Part B builds the precondition relation as a declared, versioned, regenerable
  artefact** — the substrate's precondition graph
  ([`attacker_phase_catalogue.md`](attacker_phase_catalogue.md), "Reliance on
  preceding phases") transcribed into a controller artefact under the same
  discipline as the tactic-to-verb mapping, so an adopter porting this framework to
  another simulator declares its action vocabulary **and** its procedural order.
  The learner consults it to compute `ready?(b)` from the attacker's own
  trajectory, reading no substrate state. Its validation gate is the prediction
  accuracy named in §4.
- **Part C's composition record** must record that the reported headline
  configuration still runs with modulators null (the axis-3 plurality evidence was
  earned with them off,
  [`model_scope_freeze.md`](model_scope_freeze.md) §4), and must run the
  joint-composition check the three modulator families have never had. The
  generalised learner narrows traversal for the same reason the destination-only
  one does (it sharpens routing), so any plurality claim names the capability it
  was measured at.
- **The badge does not move on this record.** Per the axis-7 criterion, a
  generalised learner moves axis 7 to DEMONSTRATED only if it raises breadth or
  stage advance against its own ablation arm; lowering the blocked fraction again
  is the same result as before and holds the badge at DESIGNED
  ([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d) axis 7). The
  sweep that decides this is pre-registered in its own commit before any output,
  and reports against its own ablation arm.

## 6. Where this connects

- **Generalises:** [`learning_capability.md`](learning_capability.md) — the
  destination-only learner, its estimator, its forgetting rule, and the sweep that
  found it operates without helping. This record keeps every part of that
  mechanism and changes only the cell key.
- **Builds on:** [`attacker_state_seam.md`](attacker_state_seam.md) (the modulator
  Protocol and the null-equivalence guarantee the generalised learner re-asserts),
  [`attacker_phase_catalogue.md`](attacker_phase_catalogue.md) (the precondition
  graph Part B transcribes).
- **Constrained by:** [`model_scope_freeze.md`](model_scope_freeze.md) §5 (the
  representational diagnosis this record measures and acts on) and the no-RL hard
  constraint (no eligibility trace, no discount factor, no value function — the
  one-bit key and the pairwise alternative both stay inside it; the phase and
  chain forms were not rejected for crossing it).
- **Evidence:** [`data/results/learning_representation/measure_budget.py`](../../../../data/results/learning_representation/measure_budget.py)
  and its `budget.json` (gitignored, regenerable) — the sparsity budget of §3 and
  the ready/not-ready split of §1.
- **When to update:** if the successor artefact's measured prediction accuracy
  (Part B) is poor enough to reconsider the key; if a corpus or mapping revision
  changes which places carry a precondition; and when the generalised sweep's
  verdict lands, at which point this record gains a pointer to it and the badge
  decision is taken there, not here.
