---
status: open
created: 2026-08-13
topic: "Axis 8 timing channel — the planned memorylessness closure inverted on verification: the substrate's 'exponential' clocks are loc-shifted (quasi-deterministic), the MTD schedule is trivially inferable, and a candidate timing-distribution divergence (documented nowhere) awaits Marc's disposition before any criterion amendment can be written"
---

# Axis 8 — the timing-channel closure inverted, and the divergence it uncovered

**Goal (one line):** carry the verified facts that falsified the planned
"memoryless trigger" closure of axis 8's timing half, get the underlying
timing-distribution divergence classified and dispositioned by Marc, and only
then amend the criterion's axis-8 prose in whichever direction the disposition
licenses.

## What happened

A 2026-08-13 design discussion (axes 4/8 intractability) produced a candidate
structural closure for axis 8's timing channel: *if* the MTD trigger is
exponential, it is memoryless — no phase to exploit, schedule knowledge worth
nothing beyond the mean, and the mean-response (duration-sensitivity) already
built and measured null as the axis-6 utility modulator. The closure carried
one pre-stated verification gate: the shape of `exponential_variates`.

**The gate fired.** `mtdnetwork/component/time_generator.py:8` is

```python
def exponential_variates(loc, scale):
    return expon.rvs(loc=loc, scale=scale, size=1)[0]
```

and every call site passes `(mean, 0.5)` — the constants file even comments
the tuples `# scheme : (mean, std)`. Under scipy's parameterisation this is a
**shifted exponential, `mean + Exp(0.5)`**: mean ≈ the nominal value + 0.5,
standard deviation 0.5. For the trigger at the operating interval that is
**200 + Exp(0.5)** — a quasi-periodic clock with ~0.25 % jitter, the opposite
of memoryless. The planned amendment is therefore **not writable**, and the
"axis 8's timing half is structurally intractable" sentence must not appear in
any prose until this handoff resolves.

## Blast radius (verified call sites)

All substrate stochastic times flow through the same wrapper with `scale=0.5`:

| Quantity | Call site | Effective behaviour |
|---|---|---|
| MTD trigger interval (all schemes, incl. `mtd_ai` and training) | `mtd_operation.py:113,158`, `mtd_ai_operation.py:191`, `mtd_ai_training.py:177` | nominal mean + Exp(0.5) — quasi-periodic |
| MTD execution time | `mtd_operation.py:178`, `mtd_ai_operation.py:209`, `mtd_ai_training.py:215` | Zhang Table-3 mean + Exp(0.5) — quasi-deterministic |
| Exploit time per vulnerability (native arm) | `attack_operation.py:527` via `services.exploit_time` | `(1−complexity)·15` + Exp(0.5) |
| Confusion penalty | `attack_operation.py:201` | 20 + Exp(0.5) |

**The movement arm is the asymmetry:** its per-tactic dwell
(`movement/timing.py:87`) uses `random.Random.expovariate(1.0/mean)` — a true
exponential with the declared mean. So the fresh L3 code implements the GSPN
semantics it declares, while the substrate's nominal exponentials are
effectively their means with ±0.5 jitter.

## The classification (per the intent-spec procedure — no verdict here)

- **Intent:** IS-TIM-02 (Zhang's documented replacement of Brown's uniform
  trigger with an exponential distribution, argued as more realistic) and
  IS-TIM-04 (the exponential is the primary PDF for inter-event times and
  action durations, µ the historical mean). An Exponential(µ) has σ = µ and
  is memoryless; the code's σ = 0.5 on means of 15–700 is neither.
- **Code:** the shifted form above. **Documented nowhere** as a distributional
  choice — which under the §c procedure makes it a *candidate* divergence/bug;
  only Marc's disposition makes it either.
- **Family resemblance:** this generalises C7 (deterministic exploit time,
  retained as inherited reality). The natural disposition is the same —
  retain + document, since a repair to true Exponential(µ) moves every golden
  and every timing figure on record — but that is a recommendation, not a
  ruling. Suggested audit row: next free D-number in
  `intent_conformance_audit.md`'s open list (D-39 as of this writing).
- **Two records drift if retained undocumented** (flag only, per the standing
  rule — annotate, never rewrite): `provenance.md`'s trigger row describes the
  code as "Exponential(µ) per scheme", and `metrics_semantics.md` §(c) credits
  the wrapper with Zhang's "exponential form" (it states σ = 0.5 without
  drawing the distributional consequence). Both should carry the corrected
  description once the disposition lands.

## What each disposition means for axis 8 (the fork this handoff exists to hold)

- **Retained (expected):** the trigger is quasi-periodic, so the schedule is
  trivially inferable by the attacker — observe two interrupts, add the
  period; no ML, no inference capability required. The timing half of axis 8
  is then **not** intractable-by-structure, and the 2026-07-28 ruled
  exclusion's stated ground ("requires an inference capability the timeframe
  cannot support") does not cover it. The honest closure becomes: channel
  open-but-unencoded, declined on S2/scope, with the exploitable value
  **bounded and already partly priced** — one interrupt lands per mutation
  regardless (the walk always has a visit in flight, and dwell visits are
  interruptible too, so the ~20 t/u penalty is unavoidable); what schedule
  awareness could salvage is the truncated-work loss and the *placement* of
  what is in flight at the tick (protecting long/valuable visits), further
  narrowed by D-35 (EXPLOIT_VULN is already uninterruptible on the movement
  arm) and computable from the cost ledger's confusion + re-work decomposition
  (D-37: 8.0–17.7 % of the clock). A bounded-value paragraph, not an
  intractability one.
- **Repaired:** the memorylessness closure becomes available exactly as
  originally argued (constant hazard → no phase; mean-response =
  duration-sensitivity = axis-6, measured null) — at the cost of a full
  re-baseline and restatement of every timing figure. Nothing in the current
  programme motivates paying that for a stronger sentence.

Either way the **badge does not move** (NOT ADDRESSED, by ruled exclusion);
what changes is the *reason* the write-up gives, which is exactly the
distinction the criterion's own §4.3 amendment models.

## Validation gate

Done when (a) Marc has dispositioned the timing-distribution divergence (an
intent-conformance-audit row exists for it), (b) the criterion's axis-8
section carries a dated amendment stating the timing-half reason consistent
with that disposition, and (c) the two drifted records are annotated. This
handoff is deleted in the commit that ships the amendment.

## Hard constraints

- No code change to `time_generator.py` or any call site without Marc's
  explicit disposition — this is a paper-code mismatch, and the burden of
  proof rule applies in full.
- The criterion file is not edited until the disposition exists.
- Any prose drafted meanwhile must avoid both unlicensed sentences: neither
  "the timing channel is memoryless, hence intractable" (falsified as stated)
  nor "the attacker could exploit the schedule" as a demonstrated claim (it
  is an in-principle bound, nothing is built or measured).

## Reading list

1. `mtdnetwork/component/time_generator.py` + `mtdnetwork/data/constants.py` (`MTD_TRIGGER_INTERVAL`, `PENALTY`) — the two-minute read that settles the fact.
2. [`../implementation/mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md) IS-TIM-02/04, IS-CFL-03 — the operative intent.
3. [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md) §(c) and [`../implementation/provenance.md`](../implementation/provenance.md) trigger row — the two drifted descriptions.
4. [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md) §(d) axis 8 + its 2026-08-09 amendment — the closure style the eventual amendment follows.
5. [`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md) — where the new D-row lands.
