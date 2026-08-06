---
status: durable
created: 2026-08-06
topic: "The axis-5 exposure reader's pre-registration — five conclusions with criteria fixed, a kill criterion on whether the curve is a repackaged event counter, a decomposition that separates tempo from action mix, and the reporting shape fixed before any output existed"
---

# Stealth exposure — conclusions committed before the numbers

**Status:** durable pre-registration. **Written and committed before the reader
produced a single reported row**; the git history is the audit trail. The
analysis computes a held/moved verdict per conclusion from the recorded runs
rather than asserting one, every aggregate goes through `interval_report` with
disjointness as the gate, and every verdict is reported across the declared
sweep rather than at one setting.

**What this measures, and why it exists.** The model has a tempo axis and no
consequence attached to it: seven of fifteen tactics consume time and dispatch
nothing, and the criterion's axis 5 scores the model NOT ADDRESSED because
tempo without a referent is not evasion. This reader supplies the missing
*observable* — a per-run detectability level that rises when the attacker acts
and erodes while it does not — so that the tempo the model already has can be
reported as a number instead of argued for. It is the buildable baseline the
parent design record recommends
([`stealth_conceptualisation.md`](stealth_conceptualisation.md) §2(a)), and its
badge ceiling is fixed in advance by that record's §9: a metric nothing responds
to reaches **DESIGNED** and stops there.

**It is a reader and it stays one.** `D(t)` is computed over an unmodified run's
own recorded stream. Nothing in the simulation consumes it — not routing, not
dwell, not any mutation selector — no attacker state is added, and therefore no
S2 question arises. The runs it reads are runs that would have happened anyway,
which is what stops the measure building in its own conclusion.

## 1. The quantity

At each **place visit** — every record that consumed the attacker's time or
dispatched a verb, the denominator `visit_distribution` already uses:

```
    D(i) = D(i−1) · exp(−Δ(i) / τ)  +  d(i) ,      D(0⁻) = 0
```

`Δ(i)` is simulated time since the previous visit began; `d(i)` is the visit's
detection increment (§2); `τ` is the declared decay constant (§3). The level
starts at zero: before its first act the attacker has generated no signal, which
is the honest null rather than a choice.

**The unit is the visit, not the attempted action, and the handoff's own
increment rule forces it.** The increment's fallback source is the corpus's
ordinal noisiness ranking over all fifteen tactics, and under the `v2_partial`
mapping the three *loudest* tactics on that ranking — exfiltration,
defence-impairment, impact — dispatch no verb at all. Scoring only attempted
actions would leave the ranking's entire top rung inert, and would score a
campaign that spends its time at the objective as having done nothing. Bare
terminal markers are excluded: they name the place the run ended at, consumed
nothing and dispatched nothing.

**Time-decay, not decay-on-next-noisy-action.** The parent record's §6 decays the
level when the attacker next acts loudly. This reader decays it with elapsed
time. The two express different intuitions and are not interchangeable:
event-driven decay says only the attacker's own loud acts cost it what it built
up, time-driven decay says ambient noise erodes any signal regardless of what the
attacker does next. The second is the one a tempo claim needs — an attacker that
waits must *gain* something by waiting, and under event-driven decay waiting is
inert. **This is a design choice pre-registered here, not a resolved fact**; if
it survives, it is proposed back into `stealth_conceptualisation.md` §6 as an
amendment rather than left as a second, silently divergent stealth dynamic.

**`D` has no units and only its comparisons mean anything.** Its absolute scale is
set by the declared increment band and the declared decay constant, neither of
which is calibrated against anything outside this model. No absolute figure is
reportable; a ratio between two arms or two profiles at a common setting is.

## 2. The detection increment — two sources, neither universal

```
    d(i) = ρ^(4 − tier(place(i)))  ·  m(i)
```

### 2.1 The tier term — the corpus's ordinal ranking, complete over 15 tactics

[`stealth_conceptualisation.md`](stealth_conceptualisation.md) §7 ranks the
fifteen tactics into five observability tiers from quoted corpus evidence. That
ranking is **ordinal and carries no magnitudes**, so this reader takes from it
exactly what it supports — an order — and supplies the magnitude as one declared
parameter with a null in its band.

| tier | tactics | this reader's assignment |
|---|---|---|
| 0 — essentially unobservable | resource-development | — |
| 1 — defined-stealthy | stealth; credential-access; command-and-control; **reconnaissance** | reconnaissance is §7's bimodal row (passive 1 / active 3); tier 1 is the declared primary **by Marc's ruling, 2026-08-06**, following his meeting framing that a scan-shaped act is near-silent. Swept to tier 3 |
| 2 — low-signal cluster | discovery; collection; execution; **lateral-movement** | lateral-movement is §7's other bimodal row (credential-reuse 2 / exploit 3); under `v2_partial` it maps to `ENUM_HOST`, which dispatches no exploit, so tier 2 is the declared primary. Swept to tier 3 |
| 3 — discrete detectable events | initial-access ⚠; persistence ⚠; privilege-escalation ⚠ | all three are §7's flagged judgement calls, carrying no observability quote |
| 4 — high-signal / noisy | exfiltration; defence-impairment; impact | — |

**Two ⚠ classes of weakness travel with this table and are named rather than
smoothed.** The two bimodal tactics cannot be split, because the net carries one
place per tactic and no mode dimension exists to split on; each takes one slot and
both are swept. The three tier-3 placements rest on inference rather than on a
quote, and §7 names them as the first thing a sensitivity sweep should perturb.

**The increment is geometric in the tier, with the null in the band.**
`d_tier = ρ^(4 − tier)`, `ρ ∈ (0, 1]`. At **ρ = 1 every tier scores 1.0** — every
act equally loud, which is exactly the placeholder Marc proposed in the meeting
("same weight for all six for now") and is the reader's exact ablation: the curve
becomes a decayed count of acts and the ranking does nothing. The declared value
is **ρ = 0.5**: a one-rung step doubles the footprint, the smallest interpretable
statement an ordinal ranking can be given, putting a factor of 16 between the
extremes. Band `{1.0, 0.75, 0.5, 0.25}`.

### 2.2 The CVSS term — only where a vulnerability was actually attempted

The substrate generates a synthetic `cvss = (complexity + impact) / 2` and
`exploitability = cvss / 5.5` per vulnerability instance
([`services.py:24-29`](../../../../mtdnetwork/component/services.py)) — the
"synthetic CSV we normalise" of the meeting. It exists **only for the
vulnerabilities an `EXPLOIT_VULN` dispatch attempted**, and has no reading for the
other five verbs or for the seven dwell-only tactics, so it modulates the tier
term rather than replacing it:

```
    m(i) = 1 − δ + 2δ·x(i)         x = 1 − e   (inverse)   or   x = e   (direct)
    m(i) = 1                       for every visit that attempted no vulnerability
```

`e` is the mean **initial** exploitability over the vulnerabilities that action
attempted. Initial, not live: the substrate mutates a vulnerability's
`exploitability` upward when the host it sits on falls
([`attack_operation.py:568-571`](../../../../mtdnetwork/operation/attack_operation.py)),
so the live attribute at read time is a defender-side scoring artefact rather than
a property of the act. `cvss` is never mutated, so `cvss / 5.5` recovers the value
the act was taken against, exactly.

`δ` is declared **0.5**, band `{0, 0.25, 0.5, 1.0}`; **δ = 0 is the tier-only
ablation**, so the CVSS term's whole contribution is measurable by subtraction.

**Direction is a declared judgement, not a fact, and both are computed.** The
inverse reading is Marc's ("a more easily exploitable vulnerability needs a
smaller footprint"); the direct reading is its opposite (a higher-impact exploit
is noisier). Neither is attested. §5's E3 fixes in advance what the reader does
with the pair.

### 2.3 One instrumentation change, with its burden of proof discharged

`e` is **not recoverable post hoc** from an unmodified run: `MovementRecord`
carries no vulnerability identity, the adversary's `curr_vulns` is overwritten by
the next exploit action, and the substrate's own scorer channel records only the
vulnerabilities of *compromise-causing* actions. The suite's standing preference
is to extend the reader rather than widen the record, so the widening is argued
rather than assumed: no reader can recover this, and exploit-dispatching actions
are **25–30 %** of the profiled attacker's attempted actions on a pilot set, so
the omission is material rather than marginal.

`MovementRecord` therefore gains **one float**, `exploitability`, sampled in-layer
and read by nothing the walk decides on. It is an *observation*, not behaviour, so
it is popped from the golden serialisation exactly as `n_compromised` and
`interrupted_by_name` are, on that file's own principle that only behaviour may
move a digest. **No golden moves.** (Ruling: Marc, 2026-08-06.)

## 3. The values — one anchored, two declared, all swept

| | value | status | tier | band |
|---|---|---|---|---|
| `τ` decay constant | **15 s** | **anchored within-substrate**: the profiled attacker's own pooled median inter-visit interval, 14.76 s over 5 profiles × 3 **pilot** seeds, rounded | declared-judgement (the quantity it names — a monitoring window — has no referent in this substrate at all) | ×{0.25, 1, 4, 16, 64} → {3.75, 15, 60, 240, 960} s |
| `ρ` tier ratio | **0.5** | declared | declared-judgement (the *order* is corpus-grounded; the ratio is not) | {1.0, 0.75, 0.5, 0.25}; **1.0 is the null** |
| `δ` CVSS weight | **0.5** | declared | declared-judgement | {0, 0.25, 0.5, 1.0}; **0 is the ablation** |
| direction | **inverse** | declared judgement, decided by E3 | declared-judgement | {inverse, direct} |
| recon tier | **1** | Marc's ruling, 2026-08-06 | corpus-grounded order, contested placement | {1, 3} |

**Why τ is anchored to the attacker's own tempo and to nothing else.** τ names the
window over which a monitor could link two events, and this substrate contains no
monitor — that absence is axis 5's entire problem, and it means no honest external
anchor exists. What the anchor has to do instead is keep the instrument
non-degenerate: far below the inter-visit gap the level is memoryless and `D`
collapses to `d`, far above it never decays and `D` collapses to a running count.
The attacker's own tempo is the only within-substrate scale that sits between
those, so it sets the *centre*, and the band spans a factor of 256 so that **both
degeneracies are inside it**. Anchoring to the mutation interval was rejected
outright: it would make the instrument a function of the defence condition being
compared.

**The pilot set is not the reporting set.** τ₀ is measured on seeds 0–2; the study
reports seeds 0–9. The anchor is a scale, not a fitted value, and it is still read
off runs that are not the ones it is applied to.

**No conclusion is reported at one setting.** Every verdict below is computed at
every point of the declared bands, and a verdict that holds at the declared centre
but not across the band is reported as **setting-dependent**, never as held.

## 4. The reporting shape, fixed now

- **Arm:** the **no-MTD arm only**, both attackers. MTD arms are deliberately out
  of scope: mutation churn would confound tempo with interrupt recovery, and the
  cleaner contrast is the one the parent record's §1 already established.
- **Runs:** 5 profiles × 10 seeds movement (`v2_partial`, retrace on, 15 000 s
  horizon) + 10 baseline seeds. One run set yields the entire sweep, because every
  declared value is read off the same recorded stream — the reader's cheapness
  property, inherited from the disengagement measure.
- **Statistics, three per run, and the second two exist to keep the first honest:**
  - `mean_exposure` — the mean of `D` over the run's visits. **The headline**, and
    the "running average" of the meeting's own description.
  - `time_average_exposure` — `(1/T)∫D dt`, closed-form between visits. The
    density-invariant companion: it does not reward an arm for sampling itself
    more often. **Where the two disagree, the disagreement is the finding.**
  - `mean_increment` — the mean of `d` with no decay at all. Clock-free and
    therefore the only one of the three that is cross-arm safe without caveat; it
    is what separates *what the attacker does* from *how fast it does it*.
- **The pricing asymmetry is stated with every cross-arm figure, not footnoted.**
  Under S3-R the movement layer prices all of that arm's time while the baseline
  runs on substrate pricing, so `D` and its time average are time-denominated
  quantities compared across two clocks. The parent record's §1.4 permits this
  **only** with the asymmetry stated in the same breath; the reader's own type
  carries the clock name so a consumer cannot drop it.
- **The baseline's event definition is corrected before it is compared, and this
  is measured rather than assumed.** `_do_exploit_vuln` appends one attack-record
  row **per vulnerability tried**, not per action, so the native record inflates
  against the movement arm's per-action records by a pilot-measured factor of
  **3.81** (3 748 rows against 983 actions over three seeds). Consecutive
  `EXPLOIT_VULN` rows uninterrupted by another verb are therefore collapsed into
  one action; the collapse is exact, because the native FSM never dispatches
  `EXPLOIT_VULN` twice in succession (`_execute_exploit_vuln` routes a compromise
  to `SCAN_NEIGHBOR` and a failure to `BRUTE_FORCE`). Uncollapsed, the baseline
  would be handed a ~3.8× louder exposure by an accounting artefact, and E2 would
  be won by bookkeeping.
- **The baseline arm has no CVSS term**, structurally: its rows carry no
  vulnerability figure. Cross-arm figures are therefore primary at **δ = 0**, and
  the CVSS variants are movement-arm only. This mirrors how the suite already
  reports the baseline's structural zeros rather than omitting the row.
- **The baseline's tiers are assigned charitably to the baseline**, on purpose: a
  verb's tier is the **minimum** over the tactics that map to it under
  `v2_partial` (so `EXPLOIT_VULN` scores 2, not 3). If the baseline still reads
  louder under the assumption most favourable to it, the finding is stronger than
  the construction that produced it.

## 5. The conclusions

Committed before any output. E4 is the kill criterion, and it is committed in the
direction that would embarrass the measure.

| | Conclusion | Criterion | Verdict |
|---|---|---|---|
| **E1** | The curve is **non-degenerate across profiles** | at the declared setting, `interval_report` over the five profiles' per-run `mean_exposure` yields **at least one CI-disjoint adjacent pair**; the max/min ratio of profile means is reported beside it. Full ordering is *not* required — two independent sweeps have already established that ten seeds cannot separate five profiles | |
| **E2** | The **baseline separates from every profile**, and reads louder | the baseline's interval is disjoint from, and above, each of the five profiles' `mean_exposure` intervals, **at every τ in the band and at both recon-tier settings**. This is a **prediction** (the baseline has no non-action dwell to let `D` decay between events), reported whichever way it falls; a separation holding at some τ and not others is reported as setting-dependent, not as held | |
| **E3** | The **CVSS direction is decided by evidence, not asserted** | both directions computed at every setting. **If the two agree on E1, E2 and E4**, the inverse reading is adopted as primary and the choice is recorded as *inconsequential* — which is the strongest available statement about an unattested judgement. **If they disagree on any verdict**, neither is adopted: both are reported, and the direction is recorded as **load-bearing**, i.e. a result that turns on a declared judgement with no source. Either way it is flagged in the value-provenance ledger | |
| **E4** | **KILL CRITERION** — the curve is **not a repackaged event counter** | \|Spearman\| between per-run `mean_exposure` and per-run visit count is **< 0.90** over the 50 movement runs at the declared setting. At ≥ 0.90 the reader reports nothing the measurement suite already lacked, and the honest conclusion is that a decayed count of acts is what it is. **If this moves, the stopping rule fires: nothing is re-specified, and the result is reported as the negative it is** | |
| **E5** | Any arm separation is **tempo-borne, not mix-borne** | held when the two arms' `mean_increment` intervals **overlap** while their `mean_exposure` intervals are disjoint — the separation survives removing the action-mix difference, which is what makes it a claim about tempo. **Moved** when `mean_increment` also separates: that is a legitimate result and a real contrast, but it is a statement about *what the attacker does*, not about *how fast*, and axis 5 may not claim it as tempo | |

**The stopping rule.** If E4 moves, the study reports the negative and stops; no
criterion is relaxed, no band re-centred, no arm added after the fact. This is the
rule the disengagement measure honoured when its own kill criterion fired, and it
exists because a measure motivated by an axis the project wants to claim is
exactly where criteria drift.

## 6. What this cannot conclude, fixed in advance

- **No badge move past DESIGNED.** The parent record's §9 fixes the ceiling: a
  metric nothing responds to has not been shown to change an outcome. Even E1, E2
  and E5 all holding does not move axis 5 past DESIGNED, and axis 5b (evasion)
  is untouched in every case.
- **No detection claim.** `D` is a declared observable, not a probability of being
  detected, and no threshold on it is computed. A binary "detected" verdict is a
  separate decision-rule build, deliberately not made here.
- **No cross-paper comparison.** Within-substrate only, as everywhere.
- **Envelope, not actor.** A tier is a declared behavioural parameter, never a
  claim about how a real adversary hides.

## 7. Evidence and anchors

- [`stealth_conceptualisation.md`](stealth_conceptualisation.md) — the parent
  design record: §1 (the baseline-versus-profiled contrast this extends), §2(a)
  (the recommended buildable baseline this *is*), §6 (the decay rule this
  pre-registers a departure from), §7 (the ordinal ranking §2.1 consumes), §9 (the
  badge ceiling).
- [`attacker_disengagement_prereg.md`](attacker_disengagement_prereg.md) and
  [`attacker_disengagement.md`](attacker_disengagement.md) — the reader-pattern
  precedent this follows exactly, including the stopping rule.
- [`../../declared_value_provenance.md`](../../declared_value_provenance.md) — the
  ledger `ρ`, `δ` and `τ` are registered in.
- [`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 5 — the
  badge this reader can move to DESIGNED, and cannot move past.
