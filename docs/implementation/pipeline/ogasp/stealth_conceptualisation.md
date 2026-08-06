---
status: durable — design record + decision request (design-only; no code, weight, mapping or golden changed)
created: 2026-07-28
updated: 2026-08-06
topic: "Axis 5 stealth — the design record. Leads with the stealthy-versus-baseline contrast (Jin's framing, the primary deliverable), then settles what a stealth STATE would add across the eight questions, records the Tay verification (it keys on attacker activity, so option 1(b) is live), proposes the tempo/evasion badge split, and puts the open items to Marc."
---

# Stealth for a substrate with no detector — the baseline-versus-profiled contrast, and what a stealth state would add on top of it

**Status:** durable design record, and a **decision request**. It answers the
supervisor's stealth question (Jin, 2026-07-28) — *what are the overarching
qualities of the contrast between a stealthy attacker under this model and the
inherited baseline attacker* — and then settles what an explicit stealth *state*
would add on top of that contrast. Its deliverable is a **decision, not code**: no
source file, weight, mapping, catalogue value or golden was changed to produce it.
The build half it specifies must not open until the attacker-state seam
([`../../../handoffs/2026-07-28_attacker_state_seam.md`](../../../handoffs/2026-07-28_attacker_state_seam.md))
lands and Marc rules on the two escalated questions (§13).

The one governing constraint frames the whole record, and it is the crux the
handoff states bluntly: **there is nothing to be stealthy against.** The substrate
has no detection model in either direction — no alert, no attacker-noise concept, no
defender observation of attacker activity in the *movement* arm anywhere in
`mtdnetwork/`. IDS is culled from the research threads by standing project
direction; Tay's detection-sensitivity machinery is retained only as an inherited
benchmark defence, "replicate, never extend", deferred to the ablation phase. So the
ordinary meaning of stealth — reducing the probability of being detected — has **no
referent for the profiled attacker as it stands**, and any mechanism that quietly
assumes one is unbuildable. The project has already written this down twice: the
tactic profile
([`../../../notes/ch3_design/tactic_profiles/07_stealth.md`](../../../notes/ch3_design/tactic_profiles/07_stealth.md)
§3) — *"because there is no detector to hide from, stealth's gain has no direct
substrate representation… a stealth tactic gets a time, not a detection model"* —
and the criterion's axis 5 — *movement through evasion-named tactics carries no
stealth semantics, and tempo alone is still not evasion*
([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d)). This record
argues **with** those two statements, not around them. It also records the one place
the "no detector anywhere" premise turns out to be too strong — Tay's reactive
`mtd_ai` defender (§8) — which is exactly what makes option 1(b) live.

The route around the no-detector wall is Jin's: **do not build a stealth mechanism
first — characterise the contrast that already exists.** That contrast is real,
already separated, and measurable without any detector, because its measures are
properties of the attacker's own behaviour rather than of anything observing it. §1
is therefore the primary deliverable; everything after it is the smaller question of
whether an explicit stealth *state* sharpens a contrast the model's structure may
already carry.

---

## 1. The stealthy-versus-baseline contrast — the primary deliverable

**The two attackers are already distinguished on exactly the axis stealth lives on,
before any stealth state is built.** The baseline 6-phase attacker is fast, loud,
and geared to this substrate; the profiled attacker has a behavioural tempo the
baseline structurally lacks. This section characterises that separation on
**event-wise** measures — the fraction of steps that are non-action, the
distribution over verbs, actions per distinct host, terminal-mode distribution —
which are invariant to how each arm is priced. Time-normalised rates are reported
only with the pricing asymmetry (§1.4) stated in the same breath.

### 1.1 The baseline attacker has no tempo choice at all

The native `proceed_attack` FSM's costs *are* the substrate's `ATTACK_DURATION`
constants. It has no concept of a place that consumes time and dispatches nothing.
On the experiment-1 no-MTD run it turns **~815 successful actions into ~40 distinct
hosts** (~20 actions per host), saturating the network to its 0.8 compromise cap
every run (9/10 reach the objective with MTD off, 10/10 with MTD on)
([`experiment_01_findings.md`](experiment_01_findings.md) §2, §4). Its entire
behavioural signature is a compromise-manufacturing loop that walks the substrate's
own precondition order. **Dwell fraction in non-action places: structurally zero** —
the baseline has no such concept, and that structural zero *is* part of the
contrast, not a missing measurement.

### 1.2 The profiled attacker spends a large fraction of its budget not compromising anything

The profiled attacker has both a tempo axis and a non-action budget. Two things the
baseline never exhibits appear immediately in its records:

- **A non-action step fraction that is positive by construction.** Under
  `v2_partial`, **7 of 15 tactics are dwell-only** (`resource-development`,
  `persistence`, `stealth`, `defense-impairment`, `collection`, `exfiltration`,
  `impact`); a visit to any of them consumes its drawn dwell and dispatches no verb
  ([`../../../../data/ogasp/controller/mappings/v2_partial.csv`](../../../../data/ogasp/controller/mappings/v2_partial.csv)).
  The `stealth` place itself is dwell-only, and the mapping's own reason column names
  it *"the model's stealth gap (criterion axis 5) made explicit"*. So a stealth visit
  today consumes time and dispatches nothing at all — the model already has the tempo
  axis; what it lacks is any consequence attached to it.
- **Effort that does not convert to breadth.** The most active profile,
  `infrastructure_setup`, turns ~460 successful actions into ~2 distinct hosts
  (~210 actions/host, an order of magnitude worse than the baseline's ~20), and
  `pure_steal` converts its budget into zero
  ([`experiment_01_findings.md`](experiment_01_findings.md) §4). The baseline
  *advances*; the profiles *repeat*.

The action-mix and terminal-mode contrast is equally sharp and equally detector-free:
the baseline terminates at the **objective** every run; the profiles terminate at
**horizon** or a **sink**, never the objective, in a mode that is a property of the
profile rather than the seed ([`experiment_01_findings.md`](experiment_01_findings.md)
§3, §5 — the profile-determinism qualified by the S1 sweep for the intermediate
profile, [`weight_sensitivity_study.md`](weight_sensitivity_study.md) §5).

### 1.3 Part of the stealth-shaped result is already on record — filed under timing

The rate feasibility study found the profiled attacker **slower to first compromise
than the baseline in all 130 cells, never once faster** — CI-separated in 107 of
them, holding across every anchor band and under both timing regimes
([`rate_feasibility_study.md`](rate_feasibility_study.md) §7 C1, §10). That is a
stealth-shaped finding ("trades speed for something else") that currently lives under
timing. And the same study found that of the four group anchors swept, **only
`stealth-low-and-slow` moves any outcome**: pooled host breadth runs from
7.82 ± 1.21 at a quarter of its declared value down to 1.78 ± 0.36 at four times it,
both ends CI-separated from the 4.56 ± 0.71 centre, while the scan, exploit and
objective anchors are inert across their bands
([`rate_feasibility_study.md`](rate_feasibility_study.md) §10). **The stealth tempo
dial is already, empirically, where this model's behaviour lives** — which is the
strongest possible opening argument for a stealth design and the reason axis 5 should
not be deferred wholesale.

### 1.4 The pricing asymmetry that bounds every time-normalised reading

Under S3-R the movement layer supplies **every** unit of the profiled attacker's time
and the substrate's own action pricing is retired on that arm, while the baseline
still runs on substrate pricing; the timing design record **withdrew** cross-arm
comparability of internal MTTC rather than defending it
([`stochastic_timing_design.md`](stochastic_timing_design.md) §2 banner, §5 banner).
So "the profiled attacker is slower" is *partly* a consequence of the two arms being
priced by different clocks, and any measure normalised by simulated time inherits
that. The safe version of the contrast is built from **event-wise** quantities — the
fraction of *steps* that are non-action, the distribution over verbs, actions per
distinct host, terminal modes — which are invariant to how each arm is priced. A
time-normalised rate (attack events per unit simulated time, the criterion's own M8b
exposure proxy) may be reported, but only with this asymmetry stated in the same
breath. The measurement suite handoff enforces exactly this in its API
([`../../../handoffs/2026-07-28_axis_measurement_suite.md`](../../../handoffs/2026-07-28_axis_measurement_suite.md)
step 6).

### 1.5 What the contrast is, in one paragraph

The profiled attacker is **not a weaker baseline; it is a different kind of
attacker** — low-and-slow where the baseline is fast-and-loud, spending a large,
positive fraction of its budget on non-action tactics the baseline has no concept of,
converting effort to breadth an order of magnitude worse, terminating away from the
objective in a profile-determined mode, and slower to first compromise in every cell
measured. Every one of those separations is a property of the attacker's own
behaviour, needs no detector, and is the same M8 supplementary measurement the
supervisor asked for by two independent routes (M8(b), and the stealth framing).
**The contrast is a stealth-shaped result the model already produces.** The open
question is whether an explicit stealth *state* sharpens it (§13, item 4).

---

## 2. Question 1 — what is stealth against? (the crux; partly Marc's call)

Three candidate semantics, evaluated in order.

### (a) Stealth as tempo, with exposure reported as a metric — RECOMMENDED buildable baseline

The stealth state slows the attacker (raises dwell means) and lowers a *reported*
exposure figure — attack events per unit simulated time, dwell fraction in non-action
places, tempo response to MTD frequency — which is precisely the criterion's own
axis-5 M8b candidate list. **Nothing in the simulation responds to exposure; it is an
observable, not a mechanism.** This is honest and buildable, and its ceiling must be
stated with it: it moves axis 5a from NOT ADDRESSED to **DESIGNED**, and **cannot
reach DEMONSTRATED on its own**, because a metric nothing responds to has not been
shown to change an outcome (§9). Recommended as the buildable baseline because it is
free of the reverse-engineering trap and requires no ruling beyond the S2/seam
question (§4).

### (b) Stealth with teeth, via a reactive defender — LIVE, and Marc's decision (§13 item 1)

The one existing coupling in this codebase where attacker activity *could* feed
defender behaviour is Tay's reactive selection agent. **The verification (§8)
confirms it does**: the `mtd_ai` scheme's decision state is built predominantly from
attacker-activity-derived metrics (host-compromise ratio, attack success rate,
return-on-attack, risk, mean-time-to-compromise, and the attacker's current phase via
an explicit detection-sensitivity gate). So the honest premise "there is nothing to
be stealthy against" is **too strong for one defender in the pool**: against the
`mtd_ai` defender there *is*. Running the profiled attacker against that defender
**unchanged**, as one of experiment 2's defence families, makes a stealthy tempo
consequential — a slower, lower-throughput, phase-obscured attacker presents a
different signal stream to the reactive defender than a loud one, and the defender's
mutation choices respond to it — **without building any new detector**. This is the
difference between axis 5a reaching DESIGNED and reaching DEMONSTRATED.

Two things gate it, and both are recorded honestly rather than waved through:

- **The sanctioned form is Tay-unchanged, not a wired knob.** The verification found
  a `attacker_sensitivity` parameter — the probability the defender correctly observes
  the attacker's current phase — that reads like a ready-made stealth dial. Wiring the
  attacker's stealth level *into* that parameter would be **reverse-modelling detection
  and extending Tay's machinery**, both forbidden. The clean, sanctioned mechanism is
  the indirect one: attacker stealth changes tempo and action-mix → the substrate
  attack record the `mtd_ai` state reads differs → the defender behaves differently.
  Tay's agent is consumed, never altered.
- **It carries real cost and a governance boundary.** `mtd_ai` is a trained
  Double-DQN and is deferred to the ablation phase; it needs a trained model and an
  integration the movement arm has not yet been run through (experiment 1 used
  `random`-multi MTD, not `mtd_ai`). So 1(b) is a *ruling plus integration work*, not
  a free win — but it is live, and it is the one item worth taking to the supervisor.

### (c) Stealth as a success-rate buff — REJECTED

With no detector for most defenders, stealth raising the probability that an action
succeeds is a free bonus with no mechanism behind it. Nothing in the model would
explain why an attacker would ever choose *not* to be stealthy, and choosing the
buff's magnitude so that stealth "matters" is reverse-engineering a benefit — the
exact thing the declared-value guardrails forbid (S3's "the numbers are inherently
arbitrary, so justifying them is the key"; the outcome overlay's CTI-independence
boundary). Rejected on principle, not on tuning.

**Resolution.** (a) is the recommended buildable baseline; (c) is killed; (b) is
**live** (the Tay premise held) and escalated to Marc as the route to DEMONSTRATED.

---

## 3. Question 2 — what does stealth cost, and is the trade real?

A stealth state that only confers advantage is incoherent. **The defensible cost is
time.** Stealth is low-and-slow, so a higher stealth level raises dwell means. That
makes the trade real and — crucially — makes it interact with the defence **without a
detector at all**: MTD's temporal churn taxes exactly the time budget stealth spends,
so a stealthier attacker eats more mutations. This is the one genuine
stealth-versus-MTD mechanism available against *every* defender in the pool (not just
the reactive one). Cho's framing supports it directly: the stealthy attacker "trades
speed for observation time", which is "precisely the budget MTD's temporal churn is
supposed to tax" ([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(d)
axis 5). The rate study makes the cost concrete: raising the stealth anchor from ×0.25
to ×4 already drives pooled host breadth from 7.82 down to 1.78
([`rate_feasibility_study.md`](rate_feasibility_study.md) §10) — the trade is not
hypothetical, it is the most consequential dial in the model. **Resolved: the cost is
time, and the trade is real and detector-free.**

---

## 4. Question 3 — does a movement-layer stealth state violate the S2 freeze?

S2 forbids adding attacker states
([`supervisor_decision_register.md`](supervisor_decision_register.md) §S2: "no
adding, removing, or altering attacker actions, abilities, or attacker states"). A
within-run stealth level looks like exactly what that forbids. **The argument that a
movement-layer state is not an MTDSim attacker state belongs to
[`../../../handoffs/2026-07-28_attacker_state_seam.md`](../../../handoffs/2026-07-28_attacker_state_seam.md)**,
which makes it in full (the freeze's stated reason is confounding in the *action
layer*; M7 licenses a movement layer that reaches the substrate only through the
existing six verbs; the null configuration is bit-identical to today, so the
conditioned and unconditioned arms are both measurable in one experiment, which is the
opposite of confounding). This record does not re-derive that argument and **does not
proceed as though it is settled**: it is flagged once here, pointed at the seam
handoff, and escalated to Marc with the seam's own S2 question (§13 item 3). No
stealth build opens until the seam lands and the freeze question is ruled.

---

## 5. Question 4 — does stealth modulate routing, dwell, both, or neither?

Routing means the stealth level changes which move comes next; dwell means it changes
how long each takes. These are different claims with different evidence.

- **Dwell is the better-grounded of the two.** The tempo argument (§3) and the rate
  study's finding that the stealth anchor is the model's one consequential dial both
  point at dwell. A stealth level scaling the dwell means is directly grounded and
  directly interacts with MTD.
- **Routing is what Marc's original framing described** (the token lands on `stealth`,
  becomes more stealthy, and that feeds the weight sets). It is the weaker claim on
  this substrate for the *tempo* semantics, because there is no exposure signal for
  routing to optimise against — but note it becomes meaningful under 1(b), where the
  attacker could route toward quieter tactics (§7) to starve the reactive defender's
  signal. If routing is wanted, the hard prerequisite is that under `v2_partial` the
  `stealth` place is **dwell-only and therefore never calls `compose`** (confirmed:
  [`../../../../data/ogasp/controller/mappings/v2_partial.csv`](../../../../data/ogasp/controller/mappings/v2_partial.csv));
  the seam handoff's step-3 dwell-only routing change is required before a modulator
  applies at that place at all).

**Recommended: dwell-primary for the 1(a) baseline; routing added only if 1(b)
opens** (where an ordinal preference for quieter tactics gains a referent).
**Resolved: dwell, with routing conditional on 1(b).**

---

## 6. Question 5 — how does the stealth level rise and fall?

The stealth level is a within-run scalar on the attacker state (the seam's
`AttackerState`). The declared-value discipline governs every number here:
rule-generated, tiered, swept, never fitted.

- **Accrual and decay.** It accrues on each visit to the `stealth` place (the
  mechanism Marc framed), and — the more defensible variant — *decays with each noisy
  action taken*, so a campaign that spends time being stealthy and then acts loudly
  loses the accumulated stealth. The corpus's ordinal noisiness ranking (§7) is the
  natural source for *which* tactics spend stealth: the high-signal tactics (impact,
  defence-impairment, bulk exfiltration, active reconnaissance / exploitation) spend
  it; the low-signal tactics (stealth, command-and-control, credential-access, passive
  reconnaissance) preserve or build it.
- **Bounds.** Bounded to a declared interval (e.g. `[0, 1]`), because an unbounded
  level makes the dwell scaling diverge and can manufacture a stall — which the seam's
  no-zero-out-edge constraint forbids without a declared rule.
- **The honest caveat.** The corpus's ranking is **ordinal, not magnitude** (§7; the
  corpus carries no per-tactic detection probability anywhere). So the accrual rate,
  the decay rate, and the dwell-scaling coefficient are **declared judgement** and must
  be swept, exactly as the timing anchors and the overlay values are. The ordinal
  ranking fixes the *sign and order* of which tactics spend stealth; every magnitude is
  a swept declared value.

**Resolved in shape:** accrue-on-`stealth`-visit, decay-on-noisy-action, ordinal
source from the corpus, every magnitude swept.

> **Amendment, 2026-08-06 — the exposure reader adopted TIME-decay, and the two
> rules are recorded side by side rather than one replacing the other**
> ([`stealth_exposure_metric.md`](stealth_exposure_metric.md); pre-registered in
> [`stealth_exposure_prereg.md`](stealth_exposure_prereg.md) before it ran). This
> section's rule decays the level on the attacker's **next noisy action**; the
> built reader decays it with **elapsed time**, `exp(−Δt / τ)`.
>
> **Why the departure, stated as the argument rather than as a preference.**
> Event-driven decay says only the attacker's own loud acts cost it what it built
> up, so *waiting is inert* — an attacker that pauses for an hour is exactly as
> exposed when it resumes as when it stopped. A low-and-slow claim has nothing to
> rest on under that rule. Time-driven decay says ambient noise erodes any signal
> regardless of what the attacker does next, which is the reading the meeting's
> own framing gave (*"as time passes… you can't link within the timeframe that
> people are monitoring"*), and it is the only one of the two under which patience
> buys the attacker anything.
>
> **This amends the reader's dynamic, not this section's.** The two rules answer
> different questions and the project now has both written down: this section's
> governs a stealth *state* that spends and rebuilds a resource, which is still
> the shape a **mechanism** would take if §13 item 4 is ever built; the reader's
> governs an *observable* over an unmodified run. A successor building the
> mechanism should choose deliberately between them rather than inheriting either,
> and should note that the reader's own study gives no evidence for the time rule
> over the event rule — it was pre-registered, not tested against its alternative.
>
> **One finding from that study bears directly on §1 and belongs here.** The
> reader's E2 predicted the inherited attacker would read louder than every
> profile and found the **opposite in ten cells of ten**, because the tempo
> premise turned out to be an accounting artefact: the substrate writes one
> attack-record row **per vulnerability tried**, inflating that arm's event count
> 3.75×, and counted as *actions* the inherited attacker takes 371 steps per run
> against the profiles' 463–674. §1.1's "~815 successful actions… ~20 actions per
> host" is a row count and the *tempo* half of §1's contrast does not survive a
> per-action reading. §1's other separations — the non-action dwell fraction, the
> terminal-mode contrast, the effort-to-breadth conversion — are unaffected,
> because each is a property the baseline structurally lacks rather than a rate.

---

## 7. The ordinal exposure ranking — from the corpus, no magnitudes

The CTI corpus carries genuine per-tactic *qualitative* observability evidence but
**no magnitudes at all** — no per-tactic detection probability anywhere (confirmed
across all 15 tactic profiles; the numbers the profiles do carry are dwell-time and
MTD-reset-strength figures, never a noisiness probability). The only quantitative
anchors in reach are Jafarian's detectability ratio (defender-side detectability of
scanning) and Outkin's ATT&CK-Evaluations-fitted per-step detection probabilities,
and the extraction for the latter explicitly records it as **not transferable to
SDR-family MTD without a calibration step that does not exist in the public record**.
So the ranking is **ordinal only**, and it fixes the order in which tactics spend or
preserve stealth, never a magnitude.

Presented as tiers, because the evidence supports tiers cleanly but not a strict
total order inside the low-signal cluster. Every rung carries its quoted evidence or
is flagged as a judgement call.

| Tier | Tactics | Evidence (quoted) |
|---|---|---|
| **0 — essentially unobservable** | resource-development | *"leaves no trace inside the victim estate"*, *"largely invisible"*; off-network by construction (01/02 profiles) |
| **1 — defined-stealthy, lowest on-network signal** | stealth; passive reconnaissance; credential-access; command-and-control | stealth *"minimising observable signals… indistinguishable from benign activity"*; passive recon *"the least risky… remain in the shadows"*; credential-access *"make the adversary harder to detect"*; C2 *"low-signal… mimicking normal, expected traffic to avoid detection"* |
| **2 — low-signal cluster (living-off-the-land / blend; internal order soft)** | discovery; collection; execution; lateral-movement (credential-reuse mode) | discovery/collection *"staying unnoticed"* with native OS tools; execution *"keep low to go undetected"*, fileless *"chosen… to evade"*; lateral-movement credential path *"quieter than exploitation"* |
| **3 — discrete detectable events (judgement calls — no direct quote)** | initial-access ⚠; persistence ⚠; privilege-escalation ⚠; active reconnaissance; lateral-movement (exploit mode) | ⚠ these carry **no observability statement** in their profiles; placed by inference (an entry exploit / exploit hop is a discrete detectable event). Active recon *"generally a sign of an ongoing attack"* is quoted |
| **4 — high-signal / noisy** | exfiltration (bulk/burst); defence-impairment; impact | defence-impairment *"a higher-privilege, higher-signal act… punctuated and decisive"* before *"a noisy objective"*; impact *"fast and decisive… burst"*, self-revealing availability destruction; exfiltration paced-but-*"can look suspicious"* in bulk |

**Two bimodal tactics** resist a single slot and must be split by mode if the rule
needs fidelity: **reconnaissance** (passive = tier 1, active = tier 3) and
**lateral-movement** (credential-reuse = tier 2, exploitation = tier 3). **Three
judgement-call placements** (initial-access, persistence, privilege-escalation) rest
on inference, not a quote, and the record flags them so the swept rule can treat them
as the least-anchored — their exposure weight is the first thing a sensitivity sweep
should perturb. The internal order of the tier-2 cluster is soft; the evidence
supports "all low-signal" more than any strict sequence.

**How the rule consumes this.** The stealth modulator does not need a total order — it
needs a *spends-stealth* set (tiers 3–4) and a *preserves-stealth* set (tiers 0–1),
with tier 2 neutral-to-mildly-preserving. That is exactly what the ordinal evidence
supports and no more, which is the honest ceiling on what the corpus can ground.

---

## 8. The Tay verification — does the reactive defender key on any attacker-activity signal?

Question 1(b) lives or dies on this, and it is validation-gate item 3. **Answer:
YES** — verified against the code, not inferred from doc prose.

- **The reactive selector is the `mtd_ai` scheme.** The decision is a Double-DQN
  forward pass in `choose_action`
  ([`../../../../mtdnetwork/mtdai/mtd_ai.py`](../../../../mtdnetwork/mtdai/mtd_ai.py):51-58),
  called from `MTDAIOperation._mtd_trigger_action`
  ([`../../../../mtdnetwork/operation/mtd_ai_operation.py`](../../../../mtdnetwork/operation/mtd_ai_operation.py):100);
  the state it reads is assembled in `get_state_and_time_series`
  (`mtd_ai_operation.py:299-438`). The only non-attacker input to the trigger loop is
  a static-degrade timeout fallback (`mtd_ai_operation.py:95`), not the policy.
- **The load-bearing state features are attacker-derived:** `host_compromise_ratio`
  (compromised-host count from the adversary's attack record), `overall_asr_avg`
  (`compromised_num / attack_event_num`), `overall_mttc_avg` (summed exploit-action
  durations), `roa` and `risk` (from `Vulnerabilities Exploited`), and `attack_type`
  (`self.adversary.get_curr_process()` — the attacker's current phase). Genuinely
  defender/topology-only features (`mtd_freq`, `time_since_last_mtd`, `ip_variability`,
  `shortest_path_variability`, `attack_path_exposure`) sit alongside them but are not
  what carries the signal.
- **There is an explicit attacker-observation gate** (`mtd_ai_operation.py:397-400`):
  a `attacker_sensitivity` probability decides, each decision, whether the defender
  correctly observes the attacker's current phase or degrades it to an "unknown"
  sentinel. This *is* Tay's IDS-sensitivity experiment
  ([`../../mtdsim_spec.md`](../../mtdsim_spec.md):39;
  [`../../architecture.md`](../../architecture.md):488-489), with its documented ≈0.7
  performance cutoff.
- **The training reward is also attacker-driven:** `overall_asr_avg`, `roa`, `risk`
  carry −75 and `overall_mttc_avg` +75 (`mtd_ai.py:162-179`).

**Consequence, stated with its caveat.** The reactive defender consumes attacker
exposure *for free* — so a stealthy attacker that reduces its observable footprint
would starve or corrupt those inputs (fewer detected compromises, degraded
`attack_type`, lower observed ASR/risk), and the defender's mutation choices would
change in response, **with no new detector built**. Option 1(b) does not collapse.
The caveat that keeps this honest: the feature set is caller-configurable
(`self.features`), a run *could* be configured to zero the attacker features, and the
movement arm has not yet been run against `mtd_ai` at all — so 1(b) is a live and
well-founded *route*, contingent on the ablation-phase ruling and an integration, not
a demonstrated result.

---

## 9. Question 6 — is exposure a metric or a mechanism? (the badge ceiling)

This is question 1 restated in the criterion's own vocabulary, and it decides the
badge ceiling — so it is answered explicitly rather than left for the implementation
to decide by accident.

- Under **1(a)**, exposure is a **metric**: the stealth state changes tempo, the tempo
  changes the *reported* exposure figure, and nothing in the simulation reads that
  figure back. A metric nothing responds to has not been shown to change an outcome, so
  axis 5a reaches **DESIGNED** and stops there.
- Exposure becomes a **mechanism** the moment something in the run consumes it. §8
  establishes that on this substrate there **is** such a consumer — the `mtd_ai`
  reactive defender — so under **1(b)** exposure is a mechanism and axis 5a can reach
  **DEMONSTRATED** (subject to the ruling and integration §8 names). The badge ceiling
  is therefore a direct function of which defender the stealth state is evaluated
  against: against the non-reactive families, DESIGNED is the ceiling; against
  `mtd_ai`, DEMONSTRATED is reachable.

**Resolved: exposure is a metric against the non-reactive defenders and a mechanism
against `mtd_ai`.** This is a sharper answer than the handoff anticipated, because the
Tay premise held.

---

## 10. Question 7 — how do three modulators compose?

Stealth, learning and incentive all multiply into the same routing composition (the
seam's generalised rule `w'(a→b) ∝ base · overlay_v · Π_m m(a→b | state)`,
renormalised, every modulator 1.0 in its null configuration). The specific hazard: a
stealth level that **slows** the attacker (raises dwell) interacts with an
incentive/utility factor whose cost term *is* duration — a slower attacker makes every
tactic look more expensive, which is **either a nice emergent coupling or a hidden
double-count.** The record's position: it is a genuine coupling to be *measured*, not
a bug to be engineered away, but the two must not be switched on together until each is
validated alone against the null. The sweep must cross the corner where stealth is high
(long dwells) *and* the incentive cost term is active, because that is where the
double-count, if it is one, is largest. This is flagged for the incentive handoff
([`../../../handoffs/2026-07-28_axis6_incentive_rationality.md`](../../../handoffs/2026-07-28_axis6_incentive_rationality.md))
as a shared-seam interaction, not resolved unilaterally here.

---

## 11. Question 8 — the distribution-shape corner a dwell-raising mechanism moves into

A stealth mechanism that raises dwell means moves the model **into exactly the corner
the rate study flagged.** At long stealth dwells under mutation pressure (stealth
anchor ×4, interval 200 s), a same-mean Erlang-4 costs the attacker roughly two-thirds
of what little breadth it had (0.46 → 0.18 hosts, paired difference −0.28 ± 0.19;
[`rate_feasibility_study.md`](rate_feasibility_study.md) §10). The mechanism: an
exponential's mode-at-zero lets the attacker occasionally complete an action between
mutations; concentrating the same mean around itself removes that short-dwell mass, so
nearly every dwell runs comparable to the interval and is cut short. **The more
behaviourally faithful shape is worse for the attacker, and the exponential's
mode-at-zero — its least realistic feature — is quietly working in the attacker's
favour** ([`stochastic_timing_design.md`](stochastic_timing_design.md) §3.3).

The consequence for a stealth design: **any stealth mechanism that raises dwell has to
address the distribution family rather than wave it through on the mean.** A stealth
level that pushes dwells long enough is precisely the thing that walks the model out of
the region where "the mean is load-bearing" holds. The record's position: the first
stealth build stays on the declared exponential (the go-forward regime), *and* the
stealth sweep must include the same-mean Erlang-4 shape check at its long-dwell corner,
because that is now a live parameter there and cannot be assumed inert. **Resolved: the
shape question is inherited, named, and folded into the stealth sweep rather than
deferred.**

---

## 12. The badge position — the proposed tempo/evasion split

Axis 5 should be **split into two sub-rows**, in the same way axis 8 already carries
Jalowski's three primitives separately:

- **Axis 5a — tempo (low-and-slow).** This half **can** be evidenced from runs. The §1
  contrast already demonstrates a behavioural tempo the baseline lacks; the stealth
  state (1a) makes it an explicit, swept dial (→ **DESIGNED**); and against the `mtd_ai`
  reactive defender (1b) the tempo becomes *consequential*, which is the path to
  **DEMONSTRATED** (§8, §9). Where it lands depends on Marc's ruling on 1(b).
- **Axis 5b — evasion.** Two senses must be separated, and only one is truly
  referent-less. *Detection-evasion* — hiding from an IDS/detector — has **no
  referent**, because no such detector exists; even the reactive `mtd_ai` defender does
  not create one, since the sanctioned coupling there is tempo-mediated (§2b: the
  attacker is quieter, so it *starves* the defender's signal — it is not *evading*).
  *MTD-evasion* — dodging or anticipating the mutations themselves to preserve
  accumulated position — **does** have a referent on this substrate. But two precisions
  keep it off axis 5. First, **the current low-and-slow attacker does not evade MTD; it
  does the opposite**, maximising its exposure by being slow (§3: a stealthier attacker
  eats *more* churn, not less) — it is a victim of the mutation schedule, not an evader
  of it. Second, **deliberate MTD-evasion is a learned capability, not a tempo** —
  timing actions around the mutation schedule, recognising a repeated post-shuffle
  state, reading mutation frequency as a signal — which is attacker **learning** (axis 7,
  "learns mutation patterns over time") and **MTD-scheme awareness** (axis 8, Jalowski's
  three primitives). So evasion's referent is **not absent, it is relocated** to axes 7
  and 8, where it is already scored NOT ADDRESSED / future work (axis 8 has its own
  closure handoff). Axis 5b therefore stays **NOT ADDRESSED**, and the honest reason is
  not "nothing to evade" but *"the thing you would evade is defeated only by the
  learning / scheme-aware attacker the other axes own"* — which is also what stops
  axis 5 quietly annexing the smart-attacker work that belongs to 7 and 8.

This is a **proposal for how to score the axis, put to Marc with the evidence** — not a
unilateral badge move. Writing it down before building is what stops the tempo half
being quietly over-claimed into the evasion half later, and it is the constraint the
criterion's own "does not promise the world" requirement imposes.

---

## 13. The decision request for Marc

Short list, with a recommendation on each.

1. **Question 1(b) — include Tay's reactive `mtd_ai` agent, unchanged, as an
   experiment-2 defence family so a stealthy tempo becomes consequential?**
   Recommendation: **yes, take it to the supervisor.** The verification (§8) confirms
   `mtd_ai` keys on attacker-activity signals, so this is the only route to
   DEMONSTRATED on axis 5a and it uses Tay *unchanged* (the indirect, tempo-mediated
   coupling of §2b — **not** wiring stealth into `attacker_sensitivity`, which would
   extend Tay and model detection, both forbidden). The cost is honest: `mtd_ai` is a
   trained DDQN deferred to the ablation phase and needs an integration the movement arm
   has not yet had. **This is the only item that needs the supervisor.**
2. **The axis-5 tempo/evasion split (§12).** Recommendation: **adopt it.** It needs
   Marc's agreement but not a meeting — a scoring decision that claims the tempo half
   (evidenceable) and disclaims the evasion half (unbuildable).
3. **The S2 freeze question (§4).** Recommendation: **confirm with the supervisor via
   the seam handoff**, which carries the full argument. No stealth build opens until this
   is ruled. Cheap to confirm, expensive to get wrong.
4. **The build default (1a), once 3 clears and 1 is decided.** Recommendation: a
   dwell-primary stealth state, rising on `stealth` visits and decaying on noisy actions,
   scaling dwell means by an ordinal exposure weight rule-generated from the corpus (§7)
   and swept, with the Erlang-4 shape check at its long-dwell corner (§11). Its research
   question is the interesting one: **does an explicit stealth state sharpen the §1
   contrast, or was the contrast already there in the model's structure?** Either answer
   is a result; the second is the more interesting. If 1(b) is sanctioned, the same build
   plus the `mtd_ai` defence arm answers the sharper question — *does the stealthy tempo
   change what the reactive defender does?* — which is the DEMONSTRATED claim.

---

## 14. Alternatives considered and killed

- **Build a minimal detector so stealth has a referent.** Rejected firmly: forbidden by
  standing project direction; it would need a fresh comparability argument against every
  baseline; and Outkin is the only pipeline that could ground per-step detection
  probabilities while its own extraction records it as non-transferable to this defence
  family. (Note this is distinct from 1(b), which builds *no* detector — it consumes the
  one Tay already trained.)
- **Reuse the evasion-named places as stealth without a state.** That is what exists
  now, and the criterion already scores it as carrying no stealth semantics.
- **Stealth as a success-rate buff (1c).** Killed in §2 — reverse-engineering a benefit
  with no mechanism.
- **Wire attacker stealth into `mtd_ai`'s `attacker_sensitivity`.** Rejected: it extends
  Tay's machinery (forbidden) and reverse-models detection (forbidden). The sanctioned
  1(b) uses the indirect tempo-mediated coupling instead (§2b).
- **Defer axis 5 entirely to future work alongside axis 8.** Defensible, and recorded as
  *not taken*: the tempo half is already built and is empirically the model's most
  consequential parameter (§1.3), so leaving it unclaimed *understates* what the model
  does. The split (§12) claims exactly the tempo half that is evidenceable and disclaims
  the evasion half that is not.

---

## 15. Hard constraints (carried, not re-litigated)

- **No IDS, no detector, no detection features.** Standing project direction. The
  constraint the whole design routes around — and 1(b) honours it, because it builds
  nothing and consumes Tay unchanged.
- **Tay's machinery is replicate-never-extend**, deferred to the ablation phase. Using
  `mtd_ai` unchanged as a defence arm may be sanctioned; extending it (including wiring
  stealth into `attacker_sensitivity`) is not.
- **Do not choose a stealth benefit magnitude so that stealth "matters".** The obvious
  temptation on this axis, and reverse-engineering.
- **The S2 freeze question is open**, not settled (§4).
- **Envelope, not actor.** A stealth level is a declared behavioural parameter, never a
  claim about how a real adversary hides.
- Determinism / SIM-05; within-substrate comparability only; Australian English; branch
  and commit rules; never push. Design-only — no code, weight, mapping or golden changed
  to produce this record.

---

## 16. How this connects

- **Answers:** the supervisor's stealth question (Jin, 2026-07-28); axis 5 of
  [`../../apt_model_criterion.md`](../../apt_model_criterion.md).
- **Build depends on:**
  [`../../../handoffs/2026-07-28_attacker_state_seam.md`](../../../handoffs/2026-07-28_attacker_state_seam.md)
  (the state and the generalised modulator composition; the dwell-only routing change)
  and a ruling from Marc (§13).
- **Consumes:** [`rate_feasibility_study.md`](rate_feasibility_study.md) §8, §10 (the
  stealth anchor as the one consequential dial; the distribution-shape corner);
  [`stochastic_timing_design.md`](stochastic_timing_design.md) §3 (the tempo regime, the
  mean-is-load-bearing defence and its measured scope);
  [`success_failure_overlay_design.md`](success_failure_overlay_design.md) §1, §6 (the
  composition rule the stealth modulator generalises);
  [`experiment_01_findings.md`](experiment_01_findings.md) (the contrast's event-wise
  figures);
  [`../../../notes/ch3_design/tactic_profiles/07_stealth.md`](../../../notes/ch3_design/tactic_profiles/07_stealth.md)
  §3 (the project's own position).
- **Feeds:** the measurement suite
  ([`../../../handoffs/2026-07-28_axis_measurement_suite.md`](../../../handoffs/2026-07-28_axis_measurement_suite.md),
  the event-wise exposure measures) and, if a build follows, the experiment-2 arms
  ([`../../../handoffs/2026-07-28_axis134_demonstration_arms.md`](../../../handoffs/2026-07-28_axis134_demonstration_arms.md)).
- **When to update:** when Marc rules on §13; when the seam lands (the build half opens);
  when experiment 2 runs (axis 5a's badge).
- **Shipped from this record, 2026-08-06:** option 1(a)'s *metric* half — the
  post-hoc exposure reader ([`stealth_exposure_metric.md`](stealth_exposure_metric.md),
  pre-registered in [`stealth_exposure_prereg.md`](stealth_exposure_prereg.md)).
  §6 carries its amendment; §17 below is the follow-on it did not cover.

---

## 17. The 1(b) route — the follow-on, absorbed here when the reader shipped

**Rehomed 2026-08-06** from the stealth handoff, which was retired in the commit
that shipped the reader. Retained because 1(b) is the *only* route by which tempo
becomes consequential, and because its case was strengthened rather than weakened
by later work. **Not licensed**; recorded so the argument is not re-derived. §2(b)
states the thesis and §8 verifies its premise against the code; what follows is
what it would actually cost.

**Why the case strengthened.** The cost-model cross-examination established that
under *time-triggered* mutation an attacker minimising declared duration is
already, mechanically, minimising expected mutation encounters (Spearman 0.87
between a tactic's declared cost and its interrupt rate). On a clock, patience is
pure exposure with no compensating benefit — so **a reactive defender is the only
channel through which slowness can ever be rational here**, which is exactly this
route's thesis.

**Four things it needs, in order, and none is cheap.**

1. **A supervisor ruling** sanctioning the reactive defender as an experimental
   arm — that agent is deferred to a later phase by standing project direction
   (§13 item 1).
2. **An integration that does not exist.** The movement arm has never been run
   against the reactive selector at all; the L3 run wiring constructs the
   time-triggered mutation operation directly. This is the real cost.
3. **A defect fixed on that path** — any attacker sensitivity below 1.0 raises an
   unbound-local error, so the documented sensitivity experiment cannot currently
   run. Fix it, or run only at sensitivity 1.0, but decide rather than discover.
4. **A dwell-scaling hook.** The modulator seam is **routing-only**; the timing
   source observes each draw and delegates it unchanged. A dwell-primary stealth
   mechanism needs a seam change, not a new modulator.

**The cheapest form that tests the claim, and it should be run before any
mechanism is built.** Run the profiled attacker against the reactive selector
**as it is**. The profiles already differ in non-action share by more than a
factor of two — a naturally-occurring tempo spread. If the selector's mutation
choices do not differ across that spread, a declared stealth dial will not rescue
the claim and the cheap run has saved the expensive one. If they do differ, that
is the demonstration, obtained with no new attacker mechanism. Report the
**mutation-choice distribution**, not just the outcome: the claim is that tempo
changes *what the defender does*.

> **One premise needs restating before that run, on the exposure reader's
> evidence (2026-08-06).** This route has been argued throughout as *a slower,
> lower-throughput attacker presents a different signal stream*. The slowness half
> does not survive a per-action reading: counted as actions rather than
> attack-record rows, the profiled attacker takes **more** steps per run than the
> inherited one (463–674 against 371), and at the exposure reader's tier-null
> setting the two arms' event tempo does not separate at all
> ([`stealth_exposure_metric.md`](stealth_exposure_metric.md) §3). The channel is
> **not** thereby closed — it relocates. What the `mtd_ai` state actually reads is
> dominated by *compromise-derived* quantities (host-compromise ratio, attack
> success rate, mean time to compromise, RoA, risk; §8), and on those the two arms
> differ enormously and in the direction the route needs: the profiled attacker
> compromises 0.5–5 hosts where the inherited one compromises ~39. So the cheap
> run above is still the right first move, but it should be framed as *does a
> low-**yield** attacker change what the reactive defender does* — not as a tempo
> claim, which the measurement no longer supports.

**Two constraints that survive with it.** Time-triggered MTD is unaffected by
tempo, so any stealth claim is bounded to the reactive arm and the write-up must
say so. And the attacker's stealth level must **never** be wired into the
defender's sensitivity parameter — that is reverse-modelling detection and
extending the inherited reactive machinery, both ruled out (§14). The coupling
stays indirect: tempo changes the record, the record changes the state, the state
changes the choice.

**The badge boundary, unchanged (§12).** A stealth claim here is a **tempo**
claim. Against the reactive selector a quieter attacker *starves* the defender's
signal — it is not evading detection, because nothing is detecting. Evasion (5b)
has no referent and stays NOT ADDRESSED; conflating them would annex the
smart-attacker work belonging to the learning and scheme-awareness axes.
