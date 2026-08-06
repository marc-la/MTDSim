---
status: durable
created: 2026-08-06
topic: "The duty-cycle study's pre-registration — Marc's two rulings on what scores and how the arms are compared, the spacing-sensitive statistics the first study lacked, a kill criterion that isolates the S3-R pricing confound, and a full disclosure of which numbers were already visible when the criteria were fixed"
---

# Detectability as a duty cycle — criteria fixed before the ruled measure was computed

**Status:** durable pre-registration, and the second on this measure. It exists
because the first study
([`stealth_exposure_prereg.md`](stealth_exposure_prereg.md),
[`stealth_exposure_metric.md`](stealth_exposure_metric.md)) answered a question
nobody asked: it reported two summaries that are **provably insensitive to when
the attacker acts**, so a measure built around a decay term could not express the
one claim the decay term exists for.

## 0. Disclosure — what was already visible when these criteria were fixed

Pre-registration means nothing if the numbers were already on screen, so this
section states exactly what was, and the reader may discount accordingly.

**Already computed and seen** (post-hoc diagnostics, `why_inverted.py`,
`duty_cycle.py`):

- The mean-over-events and time-average summaries under the **superseded**
  convention, at every swept setting — the first study's whole output.
- Duty-cycle statistics (time-grid median, quiet fraction, peak/median) under the
  **superseded** convention, for both baseline granularities. Under it the
  uncollapsed baseline is elevated 77 % of the run against the profiles' ~52 %,
  and the collapsed baseline is the *burstiest* arm of all (peak/median 24.6
  against the profiles' 4.5–4.9). **These two point in opposite directions**, and
  which one is right is a granularity question §2 rules on.
- Mean-over-events under dispatching-only scoring: 3 of 5 profiles fall below the
  baseline.

**Not computed, and the subject of this document:** the **ruled** measure — the
dwell-only exclusion and the verb-level cross-arm rule of §1 — under
spacing-sensitive statistics. No cell of that configuration has been produced.

**One consequence of the disclosure, stated rather than buried.** The collapsed
figure above suggests D2 below may well **fail**, and fail in the direction
opposite to the hypothesis that motivated the whole exercise. It is committed
anyway, in the form that can fail.

## 1. The two rulings this measure is rebuilt on (Marc, 2026-08-06)

**R1 — the increment fires on a tactic's invocation of a verb.** A dwell-only
visit contributes **elapsed time and no increment**. The underlying attack model
is not being changed, so what raises detectability is the tactic actually
invoking a substrate verb, and a tactic that dispatches nothing raises nothing.

The first study did the opposite and it is what broke it: 56–62 % of four
profiles' exposure came from tactics that dispatch nothing, so the measure scored
modelled behaviour the simulator never executed. Under R1 those tactics become
what the low-and-slow argument always wanted them to be — **silent time, during
which the level decays**.

R1's cost, stated: under `v2_partial` only eight tactics dispatch, and their
declared tiers span **1–3 only**. Tier 0 (resource-development) and the whole of
tier 4 (exfiltration, defence-impairment, impact) are dwell-only and drop out of
the movement arm's scoring entirely. The corpus's ordinal ranking is therefore
used over a **narrowed range**, and any claim resting on the ranking must say so.

**R2 — verb-level tiers across arms, tactic-level within.** With dwell-only
scoring gone, the reverse verb→tactic mapping became the main cross-arm
difference: movement `EXPLOIT_VULN` scores 0.5 when invoked by initial-access or
privilege-escalation and 0.25 via execution, while the baseline's always scored
0.25 under the charitable min-rule. That residual gap is a property of the
mapping, not of behaviour. So:

- **Cross-arm (the tempo claim):** one tier per verb, identical for both arms.
  Every `EXPLOIT_VULN` scores the same on both sides, so a difference between
  arms can only be *when*, never *what*. This is the configuration every
  arm-versus-arm conclusion below is scored at.
- **Within the movement arm (the CTI claim):** tactic-level tiers, where the
  corpus grounding is the entire point and there is no second arm to confound.

## 2. The unit — one invocation, both arms

Under R1 the scored event is **one invocation of a verb**. The native
`_do_exploit_vuln` loops over up to 15–18 vulnerabilities *inside* one
invocation, exactly as the movement arm's does inside one dispatch, so those
per-vulnerability rows are **internal to one event on both arms**. The collapsed
form is therefore the like-for-like unit, and it is the primary.

This is a reversal of the granularity the diagnostics leaned on, and the reversal
is what makes the comparison fair rather than what makes it come out a particular
way: under R1 the two arms' event counts land in the same range (baseline ~371
invocations per run against the profiles' ~280–570 dispatching visits), where the
first study compared 371 against 463–674.

**The uncollapsed baseline is retained as the sensitivity arm, not as the
primary**, because it is the only handle on the confound in §4.

## 3. The statistics — three, and none adds a declared value

The first study's two summaries are retired **for this question** with the reason
stated, because both are provably blind to spacing:

- **mean over events** samples `D` only at the instants the attacker acts — that
  is, at the top of every spike. The troughs are never sampled.
- **time-average** satisfies `∫D dt = τ·Σd` exactly (verified against the
  recorded runs at ratios 0.9933–1.0000), because each event contributes `d·τ` to
  the integral **whatever its spacing**. It is a rate wearing a decay costume.

What replaces them, sampled on a uniform 1 s time grid:

| | statistic | what it is for |
|---|---|---|
| **primary** | `p90/p50` of `D` over time | **scale-free**. Does the level come back to the floor between actions? A patient attacker's peaks tower over its typical level; a relentless one's do not. Dimensionless, so it is the summary least disturbed by the confound in §4 |
| secondary | `p50` of `D` over time | the level a monitor would see at a typical moment — the "how elevated is this network normally" reading |
| reporting axis | quiet fraction over a **swept** threshold | fraction of the run with `D` below θ·(that run's peak), reported as a **frontier over θ** rather than at a declared value — the same move the disengagement measure made with patience `k` |

**No new declared magnitude enters the family.** `p90/p50` and `p50` are
threshold-free; the quiet fraction's threshold is a reporting axis, never a
declared value. The family keeps exactly the three parameters it has (`τ`, `ρ`,
`δ`) and their bands.

## 4. The confound, named before any result

The baseline spreads its 15–18 per-vulnerability attempts across simulated time,
each charged its own exploit draw. The movement arm runs the identical loop with
`charge_time=False`, so its 4.5 attempts (7.4–9.6 when it has any) land at a
**single instant** — not because that attacker is stealthier, but because S3-R
took the substrate's per-vulnerability clock off that arm.

So a *level* comparison across arms is part behaviour and part pricing regime.
Two things follow and both are built into the design rather than added as
caveats: the scale-free `p90/p50` is the primary, and **D4 below is the kill
criterion that tests the confound directly**.

## 5. The conclusions

Committed before the ruled configuration was computed (§0). D4 is the kill
criterion and D2 is committed in the form that can fail.

| | Conclusion | Criterion |
|---|---|---|
| **D1** | the duty-cycle statistic is **non-degenerate** | at the declared setting, `p90/p50` varies across the five profiles by more than its own dispersion — at least one CI-disjoint adjacent pair, with the max/min ratio reported beside it |
| **D2** | **the prediction** — the profiled attacker returns to the floor between actions and the inherited attacker does not | `p90/p50` is higher for **every** profile than for the baseline, CI-disjoint, cross-arm at verb-level tiers, at **every** `τ` in the band. Reported whichever way it falls; a result holding at some `τ` and not others is **setting-dependent**, never held |
| **D3** | the level claim — a typical moment is quieter under the profiled attacker | `p50` is lower for every profile than for the baseline, on the same configuration and the same all-`τ` requirement. D3 may fail while D2 holds and that combination is meaningful: it would say the profiles are **burstier but not quieter**, which is a shape claim without a level claim |
| **D4** | **KILL CRITERION** — the result is not an artefact of the S3-R pricing asymmetry | D2's verdict must be **unchanged** when the baseline is scored on its uncollapsed per-vulnerability rows instead of on invocations. The two granularities bracket the confound: collapsed treats the baseline as the movement arm is structurally treated, uncollapsed lets it spread as the substrate actually prices it. **If D2 holds on one and not the other, the finding is a property of the granularity choice and must be reported as one** — not as a behavioural result |
| **D5** | the ranking is not doing the work | D2's verdict is **unchanged at `ρ = 1`**, where every invocation scores identically and the curve is pure tempo. This is what separates a genuine duty-cycle result from the first study's outcome, which was carried entirely by the increment term |

**The stopping rule, unchanged.** If D4 fires, the study reports the granularity
dependence and stops; no criterion is relaxed, no band re-centred, no arm added.
The first study honoured this when its own prediction inverted, and the
temptation is larger here because the hypothesis under test is one the project
would like to be true.

## 6. What cannot be concluded, fixed in advance

- **No badge move.** Axis 5 stays NOT ADDRESSED. This is still a reader, and a
  reader is not a mechanism — the reasoning the first study and the disengagement
  measure both declined a badge on.
- **No detection claim.** `D` remains a declared observable with no units; no
  threshold on it is a detection verdict, and the quiet-fraction threshold is a
  reporting axis rather than a claim about what a monitor would see.
- **No claim over the ranking's full range.** R1 narrows the movement arm's
  realised tiers to 1–3 (§1); tier 0 and tier 4 are unreachable, so nothing here
  evidences the ranking's extremes.
- **Nothing about the first study's verdicts.** E1–E5 were scored against a
  different instrument and stand as recorded history. This does not re-read them.

## 7. Evidence and anchors

- [`stealth_exposure_prereg.md`](stealth_exposure_prereg.md) /
  [`stealth_exposure_metric.md`](stealth_exposure_metric.md) — the first study,
  whose defect this one exists to repair.
- [`stealth_conceptualisation.md`](stealth_conceptualisation.md) §1, §6, §7 — the
  contrast this tests, the decay rule, the ordinal ranking.
- `data/ogasp/movement/exposure_rules.json` — the declared family, amended for
  R1 and R2 in the commit that ships this.
- [`attacker_disengagement.md`](attacker_disengagement.md) §1.3 — the
  frontier-over-a-reporting-axis precedent the quiet fraction follows.
