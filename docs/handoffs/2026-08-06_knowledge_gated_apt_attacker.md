---
status: open
created: 2026-08-06
---

# The knowledge-gated APT attacker — a learning mechanism with an incentive-shaped decision rule: remember which vulnerabilities have worked, and spend the loud verb only when they say it will pay

> **Retitled 2026-08-07.** This read *"one mechanism across axes 5, 7 and 8 (i),
> with axis 6 contested"*. On the code that over-claims: the capability never
> references the defender, so it is not scheme awareness, and the axis-8 half has
> been split into its own brief. The honest map is §0. The body below still argues
> the old scope in places — read it against §0, which wins.

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

**The three remaining open checks have now also been run (2026-08-07), all
read-only, and two of them change the design.** They were not gated by §2's
rulings, so they were taken first, and they make those rulings better-informed
rather than pre-empting any of them:

| check | where | outcome |
|---|---|---|
| the pool combinatorics, demanded before any sweep | §3.1 | **falsifies** the conjecture that pool size revives primitive (i)'s exact-image form — it is dead across the entire reachable range, not merely at the default |
| does the targeted strategy have anything to drive? | §4.1 | **already answered** by a study on record, and worse than the flag: the deeper blocker is that no profile's objective connects to what the simulator scores at all. Recommendation is to drop that half |
| is the attacker-state seam routing-only? | §4.1 | **holds** — the arc in routing terms needs nothing built on the seam, so the largest engineering item stays off the cost. One uncosted fork surfaced: a *hard* gate trips the seam's `may_zero` rule and owes two obligations a *soft* gate does not |

---

## 0. What this is, where it lives, and what it claims

**Rewritten 2026-08-07** after Marc's architecture correction and the axis
re-scoping. The earlier version of this section mapped the design onto the
criterion's pre-registered slots, which is reverse-fitting a build to badge moves;
that framing is withdrawn.

### The mechanism, in three parts

1. **Memory** — a table `vulnerability id -> (times tried, times it worked)`,
   filled in by reading `vuln.is_exploited()` after an attempt. Keyed on identity,
   **never** on (host, vulnerability): a mutation destroys ~80 % of a *host's*
   vulnerability set while the network-wide pool barely moves (§3, finding 2).
2. **Estimate** — for the host in front of it, compute an expected success from the
   ids it recognises among that host's visible vulnerabilities, with a declared
   prior for ids never seen.
3. **Decision** — spend `EXPLOIT_VULN` when the estimate clears a declared margin;
   otherwise take a reconnaissance action instead.

**Why the target is real rather than notional.** `Vulnerability.network()` succeeds
iff `random() < complexity`; complexity is drawn once at catalogue generation and
every per-host copy of an id keeps it. So `P(this exploit works)` is a genuine
per-id constant, and step 0 measured two-thirds of live ids sitting on more than
one host. The attacker would be estimating something that exists and recurs.

### Where it lives — Marc, 2026-08-07, and this corrects the brief's assumption

**The decision is encoded on `EXPLOIT_VULN` itself, in the substrate, taking the
attacker model's memory as an input.** The verb's outcome is the signal that
returns to the controller layer and the net; **the net decides the next step**.
The mechanism does **not** move the token, and must not: there are no jumps.

That corrects what the rest of this brief assumed — a routing modulator on the
attacker-state seam — and it is a better fit, because the memory is keyed on
*hosts and vulnerabilities* while the seam modulates *tactic routing*. The two
speak different vocabularies, and forcing the gate through the seam was the
impedance mismatch nobody had named.

**One consequence: ruling 3 below is dissolved rather than answered.** The hard-vs-soft
gate question existed only because a hard gate would have zeroed routing weights and
tripped the seam's `may_zero` rule. With the decision on the verb there is no
routing multiplier and no `may_zero` obligation. What replaces it is a smaller,
different question: **when the gate declines, what verdict does the verb return** —
and the answer should be whatever lets the net's *existing* failure routing carry
the attacker to reconnaissance, so that declining to exploit is an outcome the net
already knows how to read.

### What it claims — the honest axis map

| Axis | Verdict |
|---|---|
| **7 learning** | **The core of it.** Knowledge accumulates, behaviour changes as a result, and the credit is *compromise* rather than a routing verdict. Caveat: this is a **second** learning mechanism beside the existing per-place learner, both conditioning on exploit-shaped experience — §9's composition hazard, to be jointly checked and never assumed |
| **6 incentive** | **Real, and stronger than the brief allowed.** The gate weighs an expected payoff against the cost of an attempt. The axis-6 closure's objection was that nothing enters the *capability vocabulary* — a statement about what the old rule could read, not about whether a payoff exists. Compromise does accumulate |
| **5 stealth** | **A measurement that emerges**, on the shipped exposure reader. Fewer loud actions, readable. There is no detector, so it is not evasion, and no mechanism here changes that |
| **8 scheme awareness** | **Not claimed.** The capability never references the defender — it behaves identically with MTD switched off. Cross-target memory that survives shuffling is not recognition of a shuffling scheme. The axis-8 route is the sibling brief, [`2026-08-07_axis8_defender_metric_reasoning.md`](2026-08-07_axis8_defender_metric_reasoning.md) |
| **4 adaptivity** | **No.** The key is chosen *because* vulnerability identity survives mutation, so the memory does not respond to the defence |
| **1 persistence** | Candidate only — a back-loading arc is a shape, not an outcome |
| **3 plurality** | Expected to fall; report it |

So the honest description is **one learning mechanism with an incentive-shaped
decision rule on top** — not one mechanism spanning four axes. The brief's title
still says otherwise and should be read against this table.

### The composition with the axis-8 brief — recorded in both, 2026-08-07

The split is clean on axes but **not** on purpose, and pretending otherwise loses
the argument. The sibling
([`2026-08-07_axis8_defender_metric_reasoning.md`](2026-08-07_axis8_defender_metric_reasoning.md)
§5) suppresses mutation so the network holds still; **this** brief needs the network
to hold still so its knowledge can saturate before it strikes. Stated as the loop:
manoeuvre so the defender reads safe → mutations fall toward their floors → the
coverage curve (§3.1a) saturates → strike before the information set is invalidated
(§4.1's arc).

Two consequences. **Each brief is individually weaker than the pair**, so neither
should be written up as though it stood alone. And §9's composition hazard applies
with force rather than in principle — both mechanisms condition on exploit-shaped
experience, so a joint check is owed and must never be assumed to transfer from the
axis-6 × axis-7 precedent, which found its pair pulling *opposite* ways.

### The rulings

1. **Aim the pre-registration at progress, not friction.** *Recommend yes.* §7
   currently pre-registers successes-per-exploit-attempt, which is friction-shaped;
   axis 7 has been refused a badge twice on friction-shaped evidence and the
   readiness study warns those measures cannot discriminate between representations
   at all. The claim wants **breadth or stage advance against the ablation arm**.
2. **Drop the objective-conditioned half.** *Recommend yes* — B4 (§4.1) shows no
   profile's objective connects to what the simulator scores.
3. ~~Hard gate or soft gate~~ — **dissolved** by the architecture correction above.
   Replaced by: what verdict does a declined exploit return?
4. **The axis-6 reversal's form** (§2.1). Reopened fully by ruling. It still owes a
   dated argument against the closure text; the honest form is the mechanism plus
   the missing-payoff limitation restated, not a claim the premise changed.
5. **Scope now.** Arms 0–2. The axis-8 half is a separate brief and is gated on R-B.

### Two measurements before any build (approved 2026-08-07)

- **Decompose the exploit failures** — coin-flip failure vs MTD interrupt vs
  no-vulnerabilities/precondition. This says which term the memory can move. The
  brief justifies the work with experiment 1's 49–99 % *blocked* fraction, but
  blocked and *the exploit roll failed* are different things and only the second is
  reachable by memory.
- **Sweep the complexity range across the lineage's own disagreement.**
  `VULN_MIN_COMPLEXITY = 0.4` is faithful to **Brown 2023 Table I**, and
  [`../implementation/provenance.md`](../implementation/provenance.md) records that
  **Zhang §4.4.3 specifies [0, 1]**. At [0.4, 1] the mean is 0.7 and nearly
  everything works; at [0, 1] vulnerabilities genuinely differ and knowing which
  ones work is worth something. So widening it is a **lineage-grounded sensitivity,
  not a convenience** — which is the defensible way to answer "the numbers are
  holding the mechanism back". It is a substrate parameter: each setting needs its
  own null arm, and a global change moves goldens.

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
| **R-B** | **Is `mtd_ai` sanctioned as an experimental arm?** — the reuse-vs-retrain half is **dissolved**, see note | Standing direction defers Tay's agent to the ablation phase, and the movement arm has never been run against it. **Without it, (B) has no in-simulation payoff on any defender.** **Narrowed 2026-08-07:** there is no trained Tay agent to sanction — every figure in the paper came from a uniform random selector (`epsilon` defaults to 1.0 and the harness never overrides it), so reuse cannot serve as a control and the project's existing random-scheme arm already replicates Tay's published results. What R-B now asks is whether a **rebuilt** agent is sanctioned. Brief: [`2026-08-07_mtd_ai_cost_calibrated_rebuild.md`](2026-08-07_mtd_ai_cost_calibrated_rebuild.md); evidence: [`../implementation/pipeline/ogasp/mtd_ai_forensics.md`](../implementation/pipeline/ogasp/mtd_ai_forensics.md) §2, §8. |
| **R-C** | **Is mutation-*timing* observation in scope?** | "Knowledge is fresh, i.e. no mutation since I scanned" is axis-8 primitive **(ii) beacon**, which stays excluded — the 2026-08-05 reversal licensed primitive **(i) memoisation only**. Marc's "MTD-aware attacker, will have this observation channel" reaches for (ii). §4's arm ladder is designed to **not need it**, and §5.1 narrows what is actually required: mutation *occurrence* is already observable through the attacker's own failures, and only mutation *targeting* needs (ii). If the endowed-policy form of §5.1 is taken, R-C may not be needed at all — but the axis-8 exclusion still needs a dated amendment either way. |
| **R-D** | **Naming.** Narrowed 2026-08-06: with "swift mode" retired as a mechanism (§4.1) there is no mode to name and no naive/smart *class* split to label. What is left is the capability parameter itself. | The house pattern distinguishes capability *magnitude* (a parameter at zero versus a declared level), not attacker classes — so the ladder already encodes the split. Marc's call, but a smaller one than it was. |

### 2.1 The rulings — Marc, 2026-08-07

**R-A — REOPEN THE ROW FULLY.** Axis 6 is reopened, not merely for arm 4. The
session recommended keeping it closed and Marc overrode that; the decision stands
and this brief proceeds on it. What the ruling **owes**, and it must be paid before
any build commit, is the dated reversal §10 already requires: an argument written
against the closure text, exactly as the axis-8 reversal was.

**The reversal has one thing it must answer, and today's check made it harder
rather than easier.** The closure did not rest on the mechanisms tried; it rested
on a property of the substrate — *"on this substrate the attacker has something to
be rational about but nothing to be rational toward"*, because no payoff is ever
banked. Today's B4 finding (§4.1) confirms that is still exactly true: no profile's
operational objective connects to what the simulator scores, for either arm, so the
*located* payoff the closure named as the precondition still does not exist.
Memory-driven exploit success is a better estimate of whether an action will
*work*, which the closure classes as competence; detectability steering is a payoff
only if `mtd_ai` is sanctioned, which is R-B. A reversal that does not confront
this reads as re-litigating a closed row rather than answering it. The honest forms
available are that arm 4 supplies a payoff located in the *defender's* state rather
than the network's, or that the row reopens on the strength of the mechanism with
the missing-payoff limitation restated — not that the closure's premise has changed.

**R-B — DEFERRED TO A CONCURRENT SESSION.** Marc is probing retraining separately.
Nothing in this brief that depends on `mtd_ai` may open until that returns; arms
0–2 do not depend on it, and the emergent stealth result at arm 2 is within-arm and
stands without it. Context handed to that session is in §5.2.

**R-C — ENDOWED DECLARED POLICY.** The attacker is granted a declared policy
derived from offline analysis of what the defender reads; no runtime learning.
Primitive **(ii) beacon stays excluded** and no R-C reversal is needed for it. The
axis-8 exclusion still needs its dated amendment in the three records §10 names,
covering primitive (i) in its coarse form plus the endowed policy — and **the
granted inference must be written into the badge text**, per §5.1: the limitation
is that the inference is granted, not modelled.

**R-D — NOT PUT.** It has a conventional default and the house pattern already
answers it: a declared capability *magnitude* at zero versus a declared level, as
λ is for axis 6 and κ for axis 7. Proceeding on that unless Marc says otherwise.

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

### 3.1a Knowledge expires by becoming *unusable*, not by decaying — so measure saturation, not retention

**Marc's reframing (2026-08-06), and it improves on what §3 measured.** What
decides whether memory is worth holding is the **cardinality of the knowledge
space relative to what the attacker can see in one campaign**. Remembering IP
addresses is worthless — the space is vast and IP Shuffle is invisible to the
attacker anyway. Remembering which of three operating systems, or which of a small
service set, is worth a great deal. Knowledge does not decay; it **expires by
becoming unusable**, and it is *retained in value* precisely when the thing it
describes recurs.

**So the measurement §3 reports is the wrong shape.** Retention (20 %) and sharing
(58–70 %) are snapshots. What the design needs is a **coverage curve**: what
fraction of the reachable knowledge space has the attacker observed by time *t*,
and does it **saturate** inside the horizon? Saturation is the precondition for the
strike half of the campaign arc (§4.1) — the attacker stops learning because there
is nothing left to learn, and that is what makes striking rational.

**Pre-register the coverage curve, per pool setting**, and report the saturation
point (or its absence) as the finding. An attacker that never saturates has no
principled moment to strike, and the arc will not appear.

### 3.1 The service pool is a design dimension, not a fixed fact (Marc, 2026-08-06)

**Marc's point, and the measurement supports it:** if the service pool is
constrained, the attacker can build a knowledge state that covers it, and the
memory mechanism's effect becomes visible. At the default
`SERVICE_NO_OF_SERVICES_PER_OS = 20` the space is 7 584 (service, version) pairs
and ~790 vulnerability ids, against 3–11 services per host — so cross-host sharing
is already 58–70 %, but nothing like saturation.

**Treat pool size as a swept experimental parameter**, and pre-register what it is
expected to do: as the pool narrows, cross-host sharing rises, the coverage curve
(§3.1a) saturates sooner, and arm 2's gate fires earlier and more often. If arm
1–2's effect **only** appears at a constrained pool, that is itself the finding —
*cross-host exploit memory pays when the estate is homogeneous* — which is a real
and defensible claim about when this capability matters, and matches the
homogeneity of real enterprise estates.

**~~The sweep is finding-generating rather than a sensitivity check~~ — the
combinatorics were computed as this section demanded, and they falsify the
conjecture. RUN 2026-08-07.** The argument was that exact whole-host recurrence is
a combinatorial property of the pool, so **pool size would be the axis along which
primitive (i)'s exact-image form goes from dead to alive** — narrow it far enough
and the attacker sees whole host images again. It is not that axis, and the reason
is structural.

**The binding term is not `services_per_os`.** A host draws its services from the
per-`(os_type, os_version)` catalogue, whose size is `names × versions-per-name`.
The second factor is **16 at every pool setting**, because it is
`len(SERVICE_VERSIONS) // len(OS_VERSION_DICT[os])` = 99 // 6 — fixed by two
constants the sweep does not touch. Only the first factor moves, at
`names ≈ services_per_os × 2.47` (the cross-platform multiplier at 0.5), so the
whole sweep buys a 20-fold narrowing of a space that must shrink by orders of
magnitude to matter: collision probability falls off as `n!/N^n` with `n ≥ 4`.

| `services_per_os` | names/cell | draw space *N* | exact `(name, version)` key | name-only key |
|---|--:|--:|--:|--:|
| 20 (default) | 49.6 | 791 | **0** | **0** |
| 8 | 19.9 | 320 | **0** | **0** |
| 4 | 10.0 | 160 | **0** | **0** |
| 3 | 7.5 | 120 | **0** | 0.015 |
| 2 | 5.0 | 80 | **0** | 0.087 |
| 1 (floor) | 2.5 | 40 | **0** | 1.125 |

Colliding host pairs per network, 400 networks × 50 hosts per setting, drawn off
real catalogues through the substrate's own generation path
(`data/results/stealth_exposure/pool_recurrence_empirical.py`; the analytic
`n!/N^n` cross-check and its brute-force validation are in
`pool_combinatorics.py` alongside).

**Two findings, and the first closes the question.** The exact-image key returns
**zero collisions at every setting including the floor**, over 20 000 host draws —
and at that floor a single collision would need on the order of 10⁵ networks. The
form is not dead *at the default pool*; it is dead **across the entire range the
parameter can reach**, so a sweep for it would scan a region whose answer is
uniformly negative. Primitive (i) in its exact-image form should be reported as
**unreachable by construction** — which §3 already offered as the cheaper of its
two options, and which is now measured rather than predicted.

Second, the **coarser key survives only into a degenerate estate**. Dropping the
version — the "key on something coarser" route §3 finding 3 recommends — revives
recurrence at `services_per_os ≤ 3`, but meaningfully only at the floor: 4.3 % of
hosts share an image with another host at 2.5 service names per OS cell, 0.3 % at
five. An estate with two-and-a-half distinct services per OS is not a homogeneous
enterprise network, it is a degenerate one, and a finding taken there would not
transfer.

**What survives, and it is the half that mattered.** This falsifies the
exact-image revival only. §3.1's *first* argument is untouched and still worth
sweeping: as the pool narrows, cross-host **vulnerability-identity** sharing rises,
the coverage curve (§3.1a) saturates sooner, and arm 2's gate fires earlier and
more often. Arm 1 keys on vulnerability identity, never on host images, and step 0
already measured its traction at two-thirds of live ids. The sweep remains a
sensitivity study over arm 1–2's **effect size**; what it can no longer be is a
route back to primitive (i)'s exact form.

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

   > **CHECKED 2026-08-07, and it holds — the seam change is off the cost.** The
   > seam is routing-only as assumed, verified against its own record
   > ([`../implementation/pipeline/ogasp/attacker_state_seam.md`](../implementation/pipeline/ogasp/attacker_state_seam.md)
   > §1, §5, §9): a modulator returns a per-destination multiplier that
   > `ModulatedOverlay` applies to the composed routing distribution, while
   > `StatefulTiming` only *observes* — it calls `observe_visit(place)` and then
   > delegates `draw` untouched, which is precisely what the bit-identity
   > guarantee requires. Dwell is unreachable from a modulator. So arm 2's gate,
   > expressed as a routing factor over exploit-shaped destinations, needs
   > **nothing built on the seam at all**, and the arc in routing terms is free.
   > A dwell-shaped arc still needs the seam change, unchanged.
   >
   > **One constraint the design has not costed, and it is a real fork.** §4's arm
   > 2 reads as a *hard* gate — "gated on a memory-derived success estimate
   > exceeding a declared margin". A hard gate returns **0.0** for the refused
   > destinations, and the seam refuses an undeclared zero: `modulate` raises
   > `ValueError` unless the modulator declares `may_zero = True`, and that
   > declaration owes **a declared rule licensing the zero and a re-run of the
   > no-stall check across the parameter space** (§2 of the seam record; zeroing
   > an out-set is the one way to manufacture a stall, and stalls are
   > representable but unobserved). A *soft* gate — a margin-scaled multiplier
   > bounded away from zero — owes neither, and is the cheaper build. Which one is
   > wanted should be settled at pre-registration, because it changes both the
   > validation gate and what "gated" means in the claim.
   >
   > A second consequence, in the design's favour: since the dwell-only routing
   > change, **every** routing decision flows through `compose`, including the 7
   > of 15 dwell-only tactics under `v2_partial`. The state therefore observes the
   > whole trajectory, so arm 1's memory sees reconnaissance-shaped places it
   > would otherwise have been blind to.
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
the target, a general profile takes the network down broadly.

> **CHECKED 2026-08-07 — the check was already answered, and the answer is worse
> than the flag.** It needed no new work: a feasibility study on record
> ([`../implementation/pipeline/ogasp/targeted_attacker_feasibility.md`](../implementation/pipeline/ogasp/targeted_attacker_feasibility.md),
> 2026-07-29, commissioned by Marc) spiked the whole question and found **five
> construction blockers**. `IS-SCN-03`'s dead strategy is only the last of them
> (B5). The one that governs this section is **B4**: the targeted termination is
> commented out, `TimeNetwork.is_compromised()` overrides the parent with the
> ratio test and never consults `is_target_compromised()` — which is called from
> nowhere in the repo — so the only live objective for **both** arms is *compromise
> 80 % of the network*, and the movement attacker's `reached_objective` is exactly
> that flag. The study's own sentence is the finding: **"a profile's operational
> objective has no connection whatsoever to what the simulator counts as
> success."**
>
> So "strike according to its objective" has nothing to strike *at*, and this is
> not a gap arm 2 can route around: the profiles differ in which tactics they
> traverse, but every one of them is scored against the same network-wide ratio.
> Repairing it is **substrate work under the S2 freeze** — the study costs it as a
> construction repair (B1–B3), a termination ruling that is explicitly Marc's and
> was flagged for Jin (B4), and an attacker behaviour to write (B5) — and it
> cannot ride on the movement layer's portability argument.
>
> **Recommendation: drop the objective-conditioned half from this design.** The
> accumulate-then-strike arc (§4.1) survives intact without it, because the arc is
> measured on the exploit share of actions rather than on objective attainment.
> Fold the objective binding back into the targeted-attacker study, whose §7
> already sequences it and whose ruling 2 is the one that gates it. Carrying it
> here would import a substrate programme into a movement-layer build.

---

## 5. The `mtd_ai` / defender-metric half — SPLIT OUT 2026-08-07

**Moved in full to
[`2026-08-07_axis8_defender_metric_reasoning.md`](2026-08-07_axis8_defender_metric_reasoning.md)
(Marc's call).** What lived here — the eleven-feature state and its four steerable
levers, the reward that closes the loop, the `action == 0` suppression target and
its two floors, the endowed-vs-learned ruling, the implementation-quirk threat to
validity, and the context handed to the parallel retraining session — is that
brief's §2 to §5. Nothing was dropped.

**Why it split, and the reason is a scoping test worth keeping here.** Ask whether
a capability **references the defender**. The vulnerability memory does not: it
estimates `P(this exploit works)` from its own past attempts and behaves
identically with MTD switched off. That is **learning — axis 7** — and this brief
should claim it as that. Steering what the reactive defender measures *does*
reference the defender, has no referent without one, and is the axis-8 claim. Two
mechanisms, two axes, two briefs.

**What this brief keeps from the split.** Nothing it needs to build. The stealth
result at arm 2 is measured on the exposure reader and is **within-arm**, so it
does not depend on `mtd_ai` and is not gated by R-B.

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
- ~~**The gate's form — hard or soft**~~ — **dissolved 2026-08-07** by the
  architecture correction (§0): the decision lives on `EXPLOIT_VULN`, not on a
  routing modulator, so there are no routing weights to zero and no `may_zero`
  obligation. What replaces it: **what verdict does a declined exploit return**, so
  that the net's existing failure routing carries the attacker to reconnaissance.
- **The gate works** — arm 2 raises successes-per-exploit-attempt against arm 0.
  This is the mechanism's own precondition and a **sanity check only**; if it fails,
  nothing above it means anything.
- **The claim, and it must not be the bullet above.** Successes-per-attempt is
  friction-shaped, and axis 7 has been refused a badge twice on friction-shaped
  evidence — the readiness study warns those measures cannot discriminate at all.
  Pre-register the claim on **compromise breadth or stage advance against the
  ablation arm**, which is what a progress-carrying credit signal has to buy to be
  worth anything.
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
