---
status: open
created: 2026-08-06
---

# The knowledge-gated APT attacker — one mechanism across axes 5, 7 and 8 (i), with axis 6 contested: recon quietly, remember what works, and spend the loud verb only when it will pay

**This handoff absorbs and replaces
`2026-08-04_vulnerability_memory_and_swift_mode.md`**, deleted in the commit that
opens this one. That brief's cross-service exploit memory becomes **arm 1** here
and its "swift mode" is **retired as a mechanism** (§4.1); its axis-8 scope
decision, its reversal argument, its composition hazard and its hard constraints
are carried forward in full (§9, §10). Nothing from it is lost and nothing of it
should be re-derived.

**Design only. No code, weight, mapping or golden has been changed, and none
should be until §2's rulings land.** §3's prerequisite check **has** been run
(2026-08-06) and its answers are folded in — it was a read-only probe over fresh
runs, added no mechanism and moved nothing.

---

## 1. The idea, and the one reframe that makes it defensible

**Marc's framing (2026-08-06).** The attacker builds a knowledge state through
cheap, quiet reconnaissance; remembers which services and vulnerabilities it has
successfully exploited; and fires `EXPLOIT_VULN` — the loud, expensive verb —
**only when that knowledge says it will probably work**, at a moment of its own
choosing. Stealth, incentive rationality, learning and scheme-awareness all meet
in one mechanism.

**The reframe.** Two claims are tangled in that description and separating them
decides whether the result is publishable:

- **(A) Efficiency.** Gate the loud verb on a knowledge-derived success estimate.
  The payoff is *in the simulation*: fewer blocked attempts, better
  progress-per-effort. Experiment 1 measured a 49–99 % blocked fraction, so the
  headroom is real.
- **(B) Stealth.** Fewer, better-timed loud actions produce a lower detectability
  curve. On every defender **except** `mtd_ai`, this has no in-simulation payoff.

**Build (A) and *measure* (B).** If detectability enters the attacker's own loss
function and is then used to score it, "the smart attacker is less detectable"
becomes **true by construction** — the same definitional trap the disengagement
measure was built to avoid ("an attacker that actually stopped would make 'MTD
causes disengagement' definitional"). Built as (A) and measured as (B), the
stealth result is **emergent**: *an attacker optimising for progress happens to
become quieter, and here is how much.* That is a far stronger sentence and it is
the register the criterion already works in.

The exposure reader for (B) is **already built and validated**
([`../implementation/pipeline/ogasp/stealth_dutycycle.md`](../implementation/pipeline/ogasp/stealth_dutycycle.md)),
so this work inherits its scoring instrument rather than needing one.

### 1.1 Why this also dissolves the measurement problem that blocked axis 5

The exposure work ended with a kill criterion firing: the movement-versus-baseline
tempo comparison **flips** depending on whether the inherited attacker's exploit
attempts are counted as one invocation or as the 15–18 the substrate spreads
across the clock. That is the S3-R pricing asymmetry and it is not cheaply fixable.

**It only bites on cross-arm comparisons.** This design's interesting comparison is
**movement-versus-movement** — null arm against knowledge-gated arm, same clock,
same pricing, same substrate — so the confound is structurally absent. The claim
becomes *"this attacker capability lowers detectability"* rather than *"CTI
attackers are quieter than FSM attackers"*. The first is defensible on this
substrate; the second may not be recoverable at all.

**This is the strongest single argument for the direction** and it should be
stated in the design record the build produces.

---

## 2. The rulings this needs before a build opens

| # | Ruling | Why it is not a session's call |
|---|---|---|
| **R-A** | **Reopen axis 6?** Marc's position (2026-08-06): there is now something to be rational *around* — maximising exploit success via memory, and minimising detectability by runtime steering. | The axis-6 **final disposition** (Marc, 2026-08-02) closed the row: *"this row is DESIGNED, and that is where it ends for this project."* More sharply, its stated reasoning **pre-rejects a readiness gate**: *"readiness — whether the next action can run — is real, state-dependent and conditionable, but it is competence, not incentive… a decision rule built on readiness would be a competence model wearing this row's name."* Arms 1–3 below **are** readiness. Only arm 4 is incentive-shaped, and arm 4 is the one with the definitional problem. A reversal must be dated and argued against that text, exactly as the axis-8 reversal was. |
| **R-B** | **Is `mtd_ai` sanctioned as an experimental arm?** | Standing direction defers Tay's agent to the ablation phase, and the movement arm has never been run against it. This is the long-open §13 item 1 of the stealth conceptualisation record. **Without it, (B) has no in-simulation payoff on any defender** and arms 3–4 are measured, not demonstrated. |
| **R-C** | **Is mutation-*timing* observation in scope?** | "Knowledge is fresh, i.e. no mutation since I scanned" is axis-8 primitive **(ii) beacon**, which stays excluded — the 2026-08-05 reversal licensed primitive **(i) memoisation only**. Marc's "MTD-aware attacker, will have this observation channel" reaches for (ii). §4's arm ladder is designed to **not need it**; if it is wanted, it needs its own reversal. |
| **R-D** | **Naming.** Narrowed 2026-08-06: with "swift mode" retired as a mechanism (§4.1) there is no mode to name and no naive/smart *class* split to label. What is left is the capability parameter itself. | The house pattern distinguishes capability *magnitude* (a parameter at zero versus a declared level), not attacker classes — so the ladder already encodes the split. Marc's call, but a smaller one than it was. |

---

## 3. Step 0 — RUN, 2026-08-06. The check the design rested on, and its answer

**Measured** (`data/results/stealth_exposure/key_stability.py`, 2 seeds × 3
conditions, 200 s sampling over a 15 000 s run, 50 hosts). Regenerable; read the
script critically before extending it.

| | no-MTD | ServiceDiversity | OSDiversity |
|---|--:|--:|--:|
| catalogue vulnerability ids | 787–802 | — same — | — same — |
| catalogue (service, version) pairs | 7 584 | — | — |
| distinct vulnerability ids live on the network | 486 / 479 | 450 / 480 | 458 / 464 |
| **live ids present on more than one host** | **58 % / 64 %** | **70 % / 65 %** | **65 % / 67 %** |
| vulnerability-id retention across one 200 s interval | 100 % | **20.8 % / 21.6 %** | **19.3 % / 20.0 %** |
| whole-host fingerprint repeat rate | 98.67 % | **9.87 %** | **9.87 %** |

**Three findings, and they separate the arms cleanly.**

1. **Arm 1 has real traction — cross-host memory is worth having.** Roughly
   **two-thirds of live vulnerability ids sit on more than one host**. Marc's
   *"most hosts pretty much identical… five different services in a cycle"* is
   confirmed as a number. The catalogue is generated once and every replacement
   draws from it, so the identity pool is closed: a vulnerability the attacker has
   beaten **will** be met again elsewhere.
2. **Per-host memory dies at the first mutation; per-identity memory survives.** A
   diversity firing destroys **~80 %** of a host's vulnerability set (retention
   19–22 %), while the network-wide pool barely moves. That is precisely the
   distinction the absorbed handoff drew, now measured: **key on
   service/vulnerability identity, never on (host, vulnerability)**. The no-MTD
   100 % row is the sanity check that the instrument reads what it claims to.
3. **Exact whole-host recurrence is ZERO, and the 9.87 % is an artefact.** Both
   diversity mechanisms skip `exposed_endpoints` — 5 of 50 hosts — and 5 hosts ×
   74 repeat-snapshots ÷ 3 750 snapshots = **9.87 % exactly**. The apparent
   recurrence is entirely the five hosts that are never mutated. **No mutated host
   ever returns to a previously-seen configuration.**

**Consequence for axis 8, and it is a scope correction rather than a setback.**
Primitive (i) *state-collision recognition in its exact-image form is dead on this
substrate* — there is nothing to collide with. The absorbed handoff predicted this
and it is now settled. Either primitive (i) keys on something **coarser** than an
exact image (a single service, a vulnerability id, an OS — which is what arm 1
already does), or it is reported as **unreachable by construction**, which is a
legitimate finding and a cheaper one than building toward it.

**Two caveats on the measurement.** It is taken under **D-18** (OS Diversity's
compatibility guard is inert, so it replaces every service rather than only
incompatible ones), so the retention figures would change if D-18 is repaired —
which is exactly why the two mechanisms read almost identically here. And
fingerprints are sampled every 200 s against a 200 s mutation interval, so the
sampler and the defender are synchronised; a successor wanting sub-interval
structure should desynchronise them.

### 3.1 The service pool is a design dimension, not a fixed fact (Marc, 2026-08-06)

**Marc's point, and the measurement supports it:** if the service pool is
constrained, the attacker can build a knowledge state that covers it, and the
memory mechanism's effect becomes visible. At the default
`SERVICE_NO_OF_SERVICES_PER_OS = 20` the space is 7 584 (service, version) pairs
and ~790 vulnerability ids, against 3–11 services per host — so cross-host sharing
is already 58–70 %, but nothing like saturation.

**Treat pool size as a swept experimental parameter**, and pre-register what it is
expected to do: as the pool narrows, cross-host sharing rises, the attacker's
memory covers more of the network sooner, and arm 2's gate should fire earlier and
more often. If arm 1–2's effect **only** appears at a constrained pool, that is
itself the finding — *cross-host exploit memory pays when the estate is
homogeneous* — which is a real and defensible claim about when this capability
matters, and matches the homogeneity of real enterprise estates.

Two constraints on how that sweep is built:

- **`VULN_PERCENT_CROSS_PLATFORM` is already a parked sensitivity study**
  ([`README.md`](README.md) § Parked), and it interacts: lowering the
  cross-platform share **alone restructures sharing rather than reducing it**,
  because the per-OS catalogue shrinks with it. A joint move with
  `services_per_os` is needed. Coordinate with that parked item rather than
  duplicating it.
- **Pool size changes the network the attacker faces, not the attacker.** So every
  pool setting needs its own arm-0 null, and no cross-pool comparison is valid
  without one. This is a substrate parameter, so a pool sweep re-baselines nothing
  but also compares to nothing outside itself.

---

## 4. The recommended shape — a layered ablation ladder

One mechanism, five arms, each adding exactly one thing, each separately ablatable
and separately claimable. The ladder exists so that a four-way interaction never
has to be untangled after the fact, and so the definitional risk is contained to
one labelled arm.

| arm | what it adds | axis | claim status |
|---|---|---|---|
| **0** | null — bit-identical to today | — | the ablation, and it must be **exact**, not approximate |
| **1** | cross-host service/vulnerability memory, keyed on **vulnerability identity, never on (host, vulnerability)** — §3 finding 2 | 8 (i), coarse form only | scoped 2026-08-05; **step 0 confirms it has traction** (two-thirds of live ids are shared across hosts) |
| **2** | `EXPLOIT_VULN` gated on a memory-derived success estimate exceeding a declared margin | 7 / 4 | **competence** |
| ~~3~~ | **retired — see §4.1.** The accumulate-then-strike arc is not a mechanism and gets no arm; it is *measured* on arm 2 | **5**, **1** | an emergent **finding**, not an input |
| **4** | a detectability / network-impact estimate enters the decision explicitly | 6 (contested, R-A) | **definitional risk — label it** |

**Exposure is measured on every arm.** Pre-register that the stealth finding is
*interesting* at arm 2, where it is unoptimised and emergent, and **suspect at arm
4**, where the attacker optimises the thing being scored. If arm 4 buys nothing
beyond arm 2 — which the axis-6 precedent suggests — that is a clean negative that
costs nothing, because arm 2 carries the result.

### 4.1 "Swift mode" is not a mode — and that removes machinery rather than adding it

**Marc's correction (2026-08-06):** *swift mode* is endearing shorthand for **the
latter half of the campaign**, when the APT attacker decides it is time to strike
for impact. It is **not a discrete state** the attacker flips into.

The absorbed handoff specified it as a mode — *"a declared idle-threshold (no new
key discovered for N actions) flipping a state that scales dwell down"*. **That
specification is withdrawn.** Three things follow, and all three are
simplifications:

1. **No new declared parameter.** The idle-threshold `N` disappears. This family
   was heading for four declared magnitudes; it now needs the gate's margin and
   nothing else.
2. **No new machinery, and the biggest engineering item may vanish with it.** The
   arc comes out of arm 2's *existing* gate: early in a run the attacker knows
   little, the gate mostly refuses, and it routes to reconnaissance instead; as
   memory accumulates the gate starts passing, and exploitation rises. **That is
   pure routing**, which the attacker-state seam already supports. The seam is
   routing-only, so a *dwell*-scaling tempo shift would have needed a seam change
   — the single largest piece of engineering in the earlier shape. **If routing
   alone produces the arc, that work is not needed.** Check it before assuming
   either way: if the arc is wanted in *dwell* terms as well, the seam change
   returns and should be costed then.
3. **The arc becomes a result rather than an input**, which is strictly better for
   the thesis. A declared mode-flip would make "the attacker has two phases" true
   by construction. Emerging from the gate, it is something you *measure* — and
   this project has repeatedly found that turning a built thing into a measured
   thing is where the defensible claims come from.

**What to measure instead of building it** (candidate; sharpen at
pre-registration): the exploit share of actions over run quartiles, against arm
0's. The claim is a **knee** — a run whose exploitation is back-loaded relative to
the null. Report the continuum, not a phase label; there is no threshold to
declare and none should be invented.

**This reaches a second axis.** Axis 1 (persistence, multi-stage campaign
structure) sits at DESIGNED precisely because *"the structure is real and runs;
sustained staged advance is not yet on record"*. An accumulate-then-strike arc is
staged advance **in outcome terms**, which is the evidence that row has been
missing. Do not claim it without measuring it, but pre-register it as a candidate.

**The objective-conditioned half, per Marc:** once knowledge is sufficient the
attacker strikes *according to its objective* — a target-seeking profile drives at
the target, a general profile takes the network down broadly. **Flag before
building:** `IS-SCN-03` records the inherited **targeted strategy as having no
live code path**, so "swiftly go for the target" may have nothing to drive. This
was *not* covered by step 0 and remains an open check.

---

## 5. The `mtd_ai` channel — what its state is actually made of

Marc asked how the reactive defender's network metrics are computed, with a view
to the attacker reasoning about the impact it has on them. Read from
`mtd_ai_operation.get_state_and_time_series` (lines ~299–438). **This is a code
reading, not a measurement, and every line of it needs verifying by an
instrumented run before anything is built on it.**

The state is eleven features. The load-bearing ones are attacker-derived, and
**four are directly steerable by the behaviour this design proposes**:

| feature | how it is computed | the lever |
|---|---|---|
| `host_compromise_ratio` | compromised hosts **in the last 60 s** ÷ total hosts | **spacing.** Three compromises inside a minute read 3/50; the same three spread over five minutes read 1/50 at any instant. Temporal spacing lowers a defender input *mechanically* |
| `roa`, `risk` | the **last** exploited vulnerability's `(complexity·impact)/exploit_time` and `complexity·impact` — `[-1]`, a single sample, not an aggregate | **vulnerability selection.** Preferring low-impact vulnerabilities sets what the defender reads. This is Marc's "network impact" term, literally |
| `overall_asr_avg` | `compromised_num / attack_event_num`, where the denominator counts **`SCAN_PORT` rows only** | **the scan:exploit ratio.** More reconnaissance drives observed ASR down |
| `overall_mttc_avg` | mean **duration** of `SCAN_PORT`/`EXPLOIT_VULN`/`BRUTE_FORCE` rows | **tempo.** Longer actions raise it |

And the training reward closes the loop: `overall_asr_avg`, `roa`, `risk` carry
**−75** while `overall_mttc_avg` carries **+75**. So an attacker that spaces its
compromises, picks low-impact vulnerabilities, scans more than it exploits and
moves slowly makes the defender's state read *safe*.

**This is the concrete form of option 1(b), and it is far more specific than the
conceptualisation record's "a slower attacker presents a different signal
stream".** It names four levers, each mechanically connected to a feature.

**Three warnings that travel with it, and the first is the serious one.**

- **These may be implementation quirks rather than defence properties.** A 60 s
  window that appears nowhere in Tay's paper; `roa`/`risk` read as a single most
  recent sample rather than an aggregate; an ASR whose denominator counts only one
  of the three attack verbs. An attacker tuned against these is **gaming Tay's
  implementation, not evading a defence**, and a thesis claim built on it would be
  a claim about a bug. This is a threat to validity and must be stated in the
  design record, not discovered by an examiner. The honest form of the claim is
  *behavioural change alters what this reactive agent observes* — never *the
  attacker defeats reactive MTD*.
- **A latent divide-by-zero.** `attack_success_rate = compromised_num /
  attack_event_num` has no guard, and `attack_event_num` is zero whenever no
  `SCAN_PORT` row exists in the window. A quiet attacker is *exactly* the
  condition that produces it. Verify before running, and treat any fix as a
  substrate change needing its own disposition.
- **`replicate, never extend`.** Consuming `mtd_ai` unchanged as a defence arm may
  be sanctioned (R-B); wiring anything of the attacker's into
  `attacker_sensitivity` is reverse-modelling detection and stays forbidden.

---

### 5.1 Mutation avoidance does NOT tick axis 8 — the expected claim needs narrowing

**Marc's expectation (2026-08-06):** the attacker will be heavily optimised to
avoid AI-MTD mutations, and reasoning about the MTD boundary that way ticks axis 8.

**Three different things are being run together here, and only one of them is
axis 8.** The distinction decides whether a badge move is defensible or an
over-claim, so it is drawn before any build rather than after a result:

1. **Timing actions to fall between mutations.** This *is* scheme awareness — and
   it requires observing mutation timing, which is primitive **(ii) beacon** and
   is **excluded** (R-C). The criterion also records that per-host mutation counts
   *do not exist* in the substrate: no MTD strategy keeps per-target bookkeeping,
   so a beacon primitive would have to instrument them first.
2. **Holding knowledge that survives mutations.** This is what arm 1 does, and
   step 0 shows why it works — the identity pool is closed, so what the attacker
   learnt is still true after a shuffle. **This is not scheme awareness at all.**
   It is a durable knowledge representation that happens to be robust.
3. **Starving the reactive defender's inputs so it behaves differently.** This is
   the §5 channel. The attacker neither observes nor models the scheme; it behaves
   in a way that changes what the defender computes. §12 of the stealth
   conceptualisation record already rules on the analogous case: a quieter
   attacker *starves* the signal — *"it is not evading detection, because nothing
   is detecting."* The same reasoning applies here.

**So axis 8 moves off NOT ADDRESSED via arm 1 — primitive (i) in its coarse
form — and via nothing else in this design.** Mutation avoidance, as such, is
either excluded (1) or is not scheme awareness (3).

**And there is a structural reason (1) may be unavailable regardless.** Under
time-triggered mutation the schedule is a clock and attacker behaviour cannot move
it. Under `mtd_ai` the agent chooses **which** mutation to deploy; whether the
attacker can change *whether* one fires at all is unverified and should not be
assumed.

**Which points at the sharper and more measurable version of Marc's intuition.**
Not *avoid* mutations — **shift the defender's mutation mix**. The evaluation
already knows the mechanisms are not interchangeable against this attacker: a
network-class firing delivers 0.92–1.00 of its disruption to the movement arm and
an application-class one 0.67–0.83
([`../implementation/disruption_wiring.md`](../implementation/disruption_wiring.md)),
and IP Shuffle is documented as **invisible to the attacker** — no lineage paper
gives it an IP-addressing model. So if the attacker's behaviour steers `mtd_ai`
toward deploying mechanisms that cannot touch it and away from those that can,
**that is a real, quantified adversarial advantage**, obtained with no new
attacker mechanism and no scheme model.

Report it as the **mutation-choice distribution**, not as an outcome — which is
exactly what §17 of the stealth conceptualisation record already demands of the
cheap falsifying run. This should be run **before** anything is built, for the
same reason that record gives: if the choice distribution does not move across the
profiles' existing spread, no declared mechanism will rescue it.

---

## 6. Where the honest claims land

- **Axis 5 → DESIGNED is genuinely reachable at arm 2**, and for the first time on
  real grounds: the model would have a stealth *mechanism* (tempo chosen from
  state) rather than tempo that merely exists. **DEMONSTRATED still requires R-B**,
  because it needs something in the run to punish detectability, and only `mtd_ai`
  does.
- **Axis 7 may genuinely move, and this is underrated.** Its M8b field says what is
  missing is *"a learner whose credit signal carries progress rather than the
  routing verdict"*. A success-gated exploit decision is progress-shaped. That is
  the specific thing the badge has been waiting for.
- **Axis 8 (i)** proceeds as scoped 2026-08-05, in the **coarse** form step 0
  leaves available. **Mutation avoidance does not add to it** (§5.1), and the
  exact-image form of primitive (i) is measured dead.
- **Axis 6 must not be claimed** without R-A and a separable arm 4.
- **Axis 3 (plurality) will probably fall**, as it has under every modulator so
  far. Pre-register that expectation rather than discovering it.

Two of eight axes moving from one mechanism is a strong return for the remaining
time — **provided the claims stay this narrow**.

---

### 6.1 What this feeds in the discussion — and it is the better-evidenced thesis line

**Marc's framing (2026-08-06):** APT attackers are a latent risk to these
networks; existing systems may not be moving frequently enough, or with the
capability, to disrupt them; so **what to move, how to move and when to move** is
an optimisation question posed by APT risk, and moving *smartly and
cost-effectively* is what matters.

**Recorded here because the second half is the strongest-evidenced claim this
project has, and it is better evidenced than any stealth claim.** Four results
already on record support it, none of which needed this build:

- **What to move is threat-model-dependent, measurably.** Experiment 2 found the
  defence ordering nearly reversed between the inherited and profiled attackers
  (ρ = −0.893), with a different top-ranked mechanism on each. An evaluator would
  deploy a different defence depending solely on which attacker the evaluation
  carried. That is Row B's RECOMMENDATION grade and it is precisely *"what to
  move"* as an open question.
- **How to move has a measured differential.** Network-class firings deliver
  0.92–1.00 of their disruption to the movement attacker, application-class
  0.67–0.83, in every scheme at every seed.
- **Some movement is wasted.** IP Shuffle changes nothing the attacker reads, by
  documented design rather than by integration defect. Cost without effect is the
  cleanest possible instance of *"cost-effective"* having real content.
- **The defender's own cost is already instrumented.** The disruption ledger
  (occupancy, churn tempo, contention) exists precisely so suppression can be
  reported as a **priced trade** rather than an unpriced benefit — the frontier
  the framing asks for is already buildable.

**One clause needs correcting before it is written down, and it inverts.** *"Not
moving frequently enough"* is not supported: at the 200 s operating interval the
defence is so effective that **neither** attacker completes the objective, and the
objective only becomes reachable above roughly 1 600 s (the degenerate region, and
the rate feasibility study's C5). The measured problem is not too little movement
— it is movement that is **expensive and undifferentiated**. So the defensible
form is Marc's own second half: **not *move more*, but *move better***. Stated the
first way an examiner has a counter-example from this project's own data.

**Where it belongs.** This is `ch6_discussion` material and it is **not yet a
note** — it needs the rubric's cross-examination and it should cite the four
results above rather than assert them. Flagged here so the framing is not
re-derived, and so whoever drafts it knows which clause the evidence refuses.

---

## 7. Pre-registration shape (commit before any run, per house discipline)

Candidates, to be sharpened by the session that builds:

- **Ablation exactness** — arm 0 is bit-identical to today's model.
- **The gate works** — arm 2 raises successes-per-exploit-attempt against arm 0.
  This is the mechanism's own precondition; if it fails, nothing above it means
  anything.
- **The emergent stealth claim** — arm 2's exposure is lower than arm 0's, on the
  duty-cycle statistics, *without* detectability appearing in the decision rule.
- **The campaign arc** — arm 2's exploitation is back-loaded against arm 0's
  (§4.1). Committed as a candidate axis-1 claim, measured as a continuum.
- **A kill criterion**, committed to embarrass the design: the exposure reduction
  is **not** merely a consequence of the attacker doing fewer actions overall. If
  arm 2 is quieter only because it is slower and achieves less, it has bought
  nothing an idle attacker would not also buy — report progress and exposure
  together or not at all.
- **Arm 4 separability** — does an explicit detectability term change anything arm
  2 has not already delivered?
- **Axis-3 plurality** — expected to fall; measured either way.

---

## 8. Validation gates

Unchanged in shape from every prior axis build: unit gate on hand-built streams;
determinism (SIM-05); **no golden may move** (movement-layer only); an
off-switch exactness assertion; a composition-register entry in the same commit
that builds the mechanism; full `tests/l3_simulation` plus substrate / carve /
golden suites unchanged.

---

## 9. The composition hazard — carried forward from the absorbed handoff

This mechanism conditions on prior experience at exploit-shaped tactics. **Axis
7's learner already does exactly that, at a different key.** Composing them
without a joint check is precisely the hidden double-count the composition
register exists to catch
([`../implementation/pipeline/ogasp/modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md)
§3). The precedent is the axis-6 × axis-7 joint check
([`../implementation/pipeline/ogasp/learning_readiness_findings.md`](../implementation/pipeline/ogasp/learning_readiness_findings.md)
§6) — and it **must not be assumed to transfer**: that check found the two pulling
*opposite* ways, which is not guaranteed for a different pair.

The ladder in §4 contains this by construction, since each arm adds one thing.

---

## 10. Hard constraints

- **No *learned* inference over defender behaviour.** The 2026-08-05 scope decision
  licenses configuration **memoisation** — deterministic bookkeeping over the
  attacker's own observations — and nothing beyond it. No ML, no RL, no
  eligibility trace, no discount factor, no value function. Primitives (ii) beacon
  and (iii) metadata-shadow invariance stay excluded pending R-C.
- **Record the axis-8 reversal before building.** Three records carry the
  exclusion and each needs a dated amendment in the commit that starts the work:
  [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(d) axis 8, [`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md),
  and [`../implementation/architecture.md`](../implementation/architecture.md) §(f).
  If R-A lands, the axis-6 final disposition needs the same treatment.
- **No new declared family without checking existing artefacts first** — the
  duration catalogue, the benefit family and the learning family all exist; reuse
  before declaring, as the disengagement measure's "no second catalogue" rule
  requires.
- **Detectability must not be both optimised and scored** without the arm-4 label
  (§1).
- **This is a mechanism change to a frozen model** — no build before the §2
  rulings.
- Determinism (SIM-05); envelope-not-actor; within-substrate comparability only;
  Australian English; branch per session; never push.

---

## 11. Reading list

- [`../implementation/pipeline/ogasp/stealth_dutycycle.md`](../implementation/pipeline/ogasp/stealth_dutycycle.md)
  and [`stealth_exposure_metric.md`](../implementation/pipeline/ogasp/stealth_exposure_metric.md)
  — the scoring instrument this inherits, and why cross-arm tempo claims are
  blocked while within-arm ones are not.
- [`../implementation/pipeline/ogasp/stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
  §2(b), §8, §17 — the `mtd_ai` route, its verification, and its four
  prerequisites.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  axes 5, 6 (final disposition), 7, 8 — the four rows this touches and the two
  rulings that gate them.
- [`../implementation/pipeline/ogasp/learning_capability.md`](../implementation/pipeline/ogasp/learning_capability.md)
  and [`learning_representation.md`](../implementation/pipeline/ogasp/learning_representation.md)
  — the existing per-place learner, and the key-choice discipline any new key must
  follow.
- [`../implementation/pipeline/ogasp/attacker_state_seam.md`](../implementation/pipeline/ogasp/attacker_state_seam.md)
  — the seam every modulator reuses. It is **routing-only**: §4.1 argues the
  campaign arc needs nothing more, which is what removes the seam change from this
  design's cost. Verify that before relying on it.
- `mtdnetwork/operation/mtd_ai_operation.py` §`get_state_and_time_series` and
  `mtdnetwork/mtdai/mtd_ai.py` — the state and the reward (§5).
- `mtdnetwork/component/services.py`, `mtdnetwork/mtd/servicediversity.py`,
  `mtdnetwork/mtd/osdiversity.py` — what replacement does and does not preserve
  (§3).

---

## 12. Out of scope

- Axis-8 primitives **(ii) beacon** and **(iii) metadata-shadow invariance**,
  pending R-C.
- Any RL / value-function machinery.
- Extending Tay's agent in any way, including wiring attacker state into
  `attacker_sensitivity`.
- Re-running any recorded experiment under the new mechanism.
- Repairing the `mtd_ai` divide-by-zero or D-18 as part of this work — both are
  separate dispositions.
- Dissertation prose.
