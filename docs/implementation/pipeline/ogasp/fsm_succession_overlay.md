---
status: durable
created: 2026-08-03
updated: 2026-08-30
topic: "The FSM-succession overlay (composition-register factor 9) — a declared comparability concession to the inherited attacker's rigidity, its verdict-conditioned successor relation cross-examined against three independent sources, and the abstention rule that makes a stall structurally impossible"
---

# The FSM-succession overlay — a concession, not a capability

**This factor scores no axis of the APT criterion, and nothing it produces may be
reported as one.** Axis 6 is closed as DESIGNED with both attempted
implementations recorded as negative results; this is not axis 4, because it
responds to the **substrate** rather than to the defender; and it is not learning,
because there is no accumulation and no update from experience. Nor is it a
fidelity improvement — at its limiting end it makes the attacker behave more like
the host simulator expects, which is the opposite of behavioural independence.

> **Swept 2026-08-03, 2 080 runs, verdicts in
> [`fsm_succession_prereg.md`](fsm_succession_prereg.md) below the fold.** The
> concession does not work, and the negative is the finding. Aligning the CTI
> attacker to the inherited FSM's own order **widens** its breadth disadvantage
> (−10.4 % of the gap at α = 1, monotone) and **strengthens** the defence-ranking
> inversion rather than weakening it (ρ = −0.821 at the null, −1.000 at the limit,
> at or below the null at every band point). Read beside factor 8's ≤ 7.4 %, the
> procedural-confound explanation for the project's headline is refuted from two
> directions. The pathologies this factor was designed to fix are fixed — no MTD
> condition ever assists the attacker (0/7 at every α) and plurality holds far
> better (1.682 bits against factor 8's 1.112) — and a different one appears: the
> dwell-transparency rule composed with a narrow licensed set shifts mass onto
> **dwelling** rather than onto the licensed verb, so the attacker pivots and waits
> instead of acting. α = 1 is degenerate on three of the four pre-registered
> clauses, two of which factor 8's guard did not contain.

What it *is* is a **declared comparability concession**. The substrate carries a
rigid finite-state attacker. A CTI-derived attacker walking a different order is
penalised by that rigidity in ways that have nothing to do with the defence, and
the project's headline result — the defence-ranking inversion — is exposed to
exactly that objection. α buys the penalty off by a declared, swept amount so the
two attackers are relatively comparable, and the null arm reproduces every
recorded figure at full strength.

## 1. Why this supersedes factor 8

Factor 8 asked *"how far is this candidate from being able to act productively?"*
over the precondition relation's capability closure. Its 2 080-run sweep measured
what that target actually rewards
([`fsm_alignment_prereg.md`](fsm_alignment_prereg.md), below the fold): at α = 1
the attacker compromised **exactly one host in 38 of 50 runs**, at the lowest
friction and among the highest per-action success rates in the whole sweep. Once
`curr_host` was held, every attack verb sat at distance 0 while `ENUM_HOST` — the
pivot to a fresh host — sat at 1, so the limiting end zeroed the only move that
creates new opportunity. Being *able* to attack is not the same as getting
anywhere.

**The inherited FSM does not have that defect.** Its successor after a compromise
is `SCAN_NEIGHBOR`, and `SCAN_NEIGHBOR`'s successor is `ENUM_HOST` — it pivots, by
construction, because Brown drew it that way. Conditioning on the FSM's own
succession therefore **inherits a progress structure instead of re-deriving a
worse one**, which is the whole of the design change.

Factor 8 is retired as an instrument but **not deleted**: its sweep is on record,
and its result is the measured negative that motivated this shape.

## 2. The rule

At a routing decision, over the destinations the net gives strictly positive base
mass:

```
    targets  =  the verbs the inherited FSM licenses next, given the verb just
                run and the verdict it returned — or, if that action was
                interrupted, given the mutating resource's layer

    m(a→b)   =  1.0        b dispatches no verb at all
             =  1.0        b's verb is in targets
             =  (1 − α)    otherwise
```

α is a **float** over [0, 1] and nothing privileges the endpoints; intermediate
values are the intended operating region for a concession. At α = 0 the modulator
returns no factors and the run is bit-identical to one with no state attached.

**Dwell-only places are transparent**, and that is the design's second load-bearing
choice. A place that fires no verb cannot violate the succession, so it keeps full
weight and a visit to one does not advance the FSM state. This is what lets the
attacker traverse its own CTI structure *between* FSM-legal actions rather than
being forced onto the bare verb chain — the difference between a dial that biases
the attacker and one that replaces it. Under `v2_partial` seven of fifteen tactics
are dwell-only, so the transparent structure is substantial.

### 2.1 Two controller relations compose, and the seam is declared

The succession says **what comes next**. The precondition relation's capability
closure says **what must happen first** when what comes next cannot run: if no
licensed successor is runnable in the attacker's current capability state, the
targets become the first-step verbs on a shortest route to making one runnable.

Without that fallback the dial drives the token at a dispatch the substrate
refuses — which is precisely the failure factor 8's sweep measured (blocked
fraction 0.93 under the position-destroying family). The fallback is not
decoration: under IP Shuffle at α = 0.25 it fires 131 times in a single run,
because MTD keeps severing the position the FSM's next step assumes.

### 2.2 The abstention rule, and why it is not a patch

Where the net offers **no** FSM-legal move at all, this factor attenuates
nothing. Two reasons, and the second is the substantive one.

It makes a stall **structurally impossible** rather than merely unobserved: the
out-set can never be emptied, because the only configuration that could empty it
is the one in which the factor declines to act. And it is what keeps the mechanism
a concession — where the CTI structure offers nothing the inherited FSM would
sanction, forcing the token through would not align the attacker, it would silence
it.

The rule was earned, not assumed. Without it the exhaustive check returns **47 079
offending cells**, and the reason is legible: **`v1_ckc_total` maps every one of
its fifteen tactics to a verb**, so it has no transparent dwell-only structure to
fall back on and a source whose whole out-set fires off-target verbs is starved.
With the rule the same check returns **0**.

## 3. The relation, cross-examined against three independent sources

The relation is a *transcription*, so it has an oracle, and it was checked against
all three ways the FSM is stated in this repo:
`data/ogasp/controller/fsm_succession.json`, version `v1_brown_fig3`.

| after | verdict | licensed successors | source agreement |
|---|---|---|---|
| `SCAN_HOST` | success | `ENUM_HOST` | code, Fig 3 box 1→2, Zhang Fig 7 |
| `SCAN_HOST` | failure | `SCAN_HOST` | **declared divergence** — the substrate *terminates*; the movement layer cannot, so discovery retries, following Fig 3's box 10→1 |
| `ENUM_HOST` | either | `ENUM_HOST`, `SCAN_PORT`, `SCAN_HOST` | code; verdict cannot distinguish |
| `SCAN_PORT` | either | `SCAN_NEIGHBOR`, `EXPLOIT_VULN` | code (prose branch) **and** Fig 3 (unconditional edge) — the set satisfies both readings |
| `EXPLOIT_VULN` | success | `SCAN_NEIGHBOR` | code, Fig 3 box 7→9, Zhang Fig 7 |
| `EXPLOIT_VULN` | failure | `BRUTE_FORCE` | code, Fig 3 box 7→8 |
| `BRUTE_FORCE` | success | `SCAN_NEIGHBOR` | code, Fig 3 box 8→9 |
| `BRUTE_FORCE` | failure | `ENUM_HOST`, `SCAN_HOST` | code + Fig 3 box 10's two edges |
| `SCAN_NEIGHBOR` | either | `ENUM_HOST` | code, Fig 3 box 9→2, Zhang Fig 7 |
| *interrupt* | network / application / reserve | `SCAN_HOST` / `SCAN_PORT` / `EXPLOIT_VULN` | code `_handle_interrupt`; Zhang Fig 7's two enclosures; Brown §III-D(3) via D-07 |

**Every successor is a set, and that is load-bearing rather than defensive
generality.** The verdict adapter treats `ENUM_HOST`, `SCAN_PORT` and
`SCAN_NEIGHBOR` as *success-unless-interrupted*, so for two of them the
substrate's branch is **not recoverable** from the verdict this modulator sees.
Declaring every reachable successor is more honest than picking the modal one, and
it *widens* the permitted set — so the ambiguity cannot manufacture an alignment
the FSM does not license.

### 3.1 The runtime cross-examination, and the omission it caught

Reading dispatch wrappers is not verification. The relation was therefore checked
against the **native attacker's own observed transitions**, over three MTD
conditions, and that check is now a standing test.

It caught a real omission. The first draft declared `ENUM_HOST` → {`ENUM_HOST`,
`SCAN_PORT`}, and the native attacker was observed taking `ENUM_HOST` →
`SCAN_HOST` ten times: the loop branch re-enters `_enum_host()`, whose own
empty-stack guard falls through to `_scan_host()`. The draft had reasoned about
that guard for `BRUTE_FORCE`'s failure branch and not noticed it applies to
`ENUM_HOST`'s loop branch as well. **With the row corrected, the relation explains
every observed transition under all three conditions, 0 unexplained.**

### 3.2 One observed transition is deliberately excluded

`EXPLOIT_VULN` → `EXPLOIT_VULN` is the single most common transition in the native
record stream (5 605 of 7 856 over six seeds) and is **not** in the relation.
`_do_exploit_vuln` iterates the top-five vulnerabilities and appends one
statistics row *inside* that loop, so one dispatched phase emits up to five rows.
The FSM does not self-loop, and the movement layer takes one outcome per place
visit so it never sees this edge. It is recorded because a naive reading of the
native record stream would add a self-loop that does not exist — which would
license the dial to hold the token on exploitation indefinitely.

## 4. The seam, and one impurity repaired

The **rule** (prefer the tactic the inherited FSM would run next) is portable and
lives on the movement seam as factor 9. The **relation** is a statement about
MTDSim's own attacker and must be rewritten to port, so it lives on the controller
seam beside the mapping (factor 5) and the precondition relation (factor 6).

That also repairs factor 8's recorded impurity: the objective-productive verb set
had to sit as a movement-layer constant because factor 8's brief barred touching
the precondition relation. It is substrate-specific knowledge, so it now lives on
the controller seam in this artefact, where the seam rule says it belongs.

An adopter porting the framework now declares **three** artefacts and changes no
movement-layer code: an action vocabulary, a procedural order, and a succession.

## 5. The honest limits

1. **It is not learning, not axis 4, and not a fidelity improvement** (§0).
2. **Claims are confined to the position-destroying defence family.** Factor 8's
   sweep measured the diversity family producing hosts, distinct places and verb
   share identical to the no-MTD arm to three significant figures while
   interrupting 67 times per run, so the declared capability vocabulary is
   demonstrably blind to what OS and Service Diversity destroy.
3. **The dial's headroom is bounded and measurable.** Abstentions rise with α — 0
   at the null to 64 per run at α = 1 in one spot-checked cell — and every
   abstention is a decision at which the net offered nothing FSM-legal and the
   factor did nothing. That share bounds what the dial can do, and it is reported
   with any result rather than left implicit.
4. **The readiness test is a prediction, not ground truth.** The capability
   fallback fires on the same in-layer prediction the readiness learner uses,
   whose measured accuracy is 1.0000 on `v1_ckc_total` and 0.9169–0.9428 on
   `v2_partial`. The residual is the relation's own recorded optimism.
5. **A concession is not a licence.** Declaring α so two attackers are comparable
   is a stated methodological choice; tuning α until a criterion row improves is
   scoring-driven design and is forbidden by S6. Any reported arm names its α and
   quotes its own plurality figure.

## 6. Validation gates

| gate | status |
|---|---|
| α = 0 is bit-identical, over profiles × seeds × mappings × MTD conditions, as a test | **held** |
| the relation explains every native transition, under MTD and without | **held** — 0 unexplained across three conditions; a standing test |
| the relation matches Brown Fig 3 and Zhang Fig 7 box by box | **held** — asserted per edge, with the two recorded divergences named |
| the stall question is settled and the check re-run across the band | **held** — 0 offending cells with the abstention rule; 47 079 without it, so the check has teeth |
| no new declared magnitude beyond α, with a tier, a band and a sweep | **held** — one parameter, `declared-judgement`, band `[0, 0.25, 0.5, 0.75, 1]`, sweep pre-registered in [`fsm_succession_prereg.md`](fsm_succession_prereg.md) |
| the register gains a row in the same commit | **held** — [`modulator_composition.md`](modulator_composition.md) factor 9 |
| the sweep runs against pre-registered criteria | **held** — 2 080 runs; B5 held, B1/B2/B3 moved, B4 held; the guard fired at α = 1 and the reported band is truncated accordingly |
| reader gates unchanged; no golden moves | **held** — a movement-layer factor plus a new controller artefact; no substrate file touched |

## 7. Reproduce

```
PYTHONPATH=src python -m pytest tests/l3_simulation/test_movement_succession.py
```

## 8. Where this connects

- **Consumes unchanged:** the tactic-to-verb mapping (factor 5) and the
  precondition relation (factor 6).
- **Declares:** the succession relation (`data/ogasp/controller/fsm_succession.json`,
  controller seam) and α (`data/ogasp/movement/succession_rules.json`).
- **Supersedes as an instrument:** factor 8
  ([`fsm_alignment_overlay.md`](fsm_alignment_overlay.md)), which is retained with
  its sweep as the measured negative that motivated this design.
- **Composition bar:** the same bar factor 8 carries against factor 4 applies
  here and for the same reason — both condition on the capability state against
  the same artefact, and two factors that agree may compound where two that
  disagreed did not.
- **A band point beside it, not a repair of it (2026-08-30):** the token-hold
  rule — Jin's T1 fix in its *opaque* reading — reads the FSM state this
  modulator tracks at α = 0 and holds the token instead of reweighting; it is
  pre-registered and measured in
  [`fsm_token_hold_findings.md`](fsm_token_hold_findings.md) against this
  factor's band. Its *transparent* reading is this factor's α = 1 point and is
  not re-run.
- **When to update:** if the succession relation, the mapping registry or the
  overlay registry changes in a way that could move the no-stall check (re-run it
  — it is cheap and exhaustive); when the sweep's verdict lands.
