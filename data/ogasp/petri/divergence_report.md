# Divergence-from-aggregate report — do the four class envelopes differ from the null profile?

The structural half of the profile-discrimination verification (the
behavioural half is the timeline runner's). Weights are the W-A
flow-proportion layer (D3): out-edge-normalised distinct-flow counts
on the **operator-deduplicated corpus (n = 29)** as primary, raw
(n = 38) as the robustness column. JSD convention matches the L2 gate:
`scipy jensenshannon(p, q, base=2) ** 2` (divergence in [0, 1]),
per comparable place (a place where both nets have a flow-backed
out-distribution), summarised as the unweighted mean per class.

**Reading frame (metrics_semantics.md §(f)):** weights are
workflow-recurrence over a survivorship-biased corpus. Each class net
is a behavioural **envelope** for an operational objective — never an
actor's policy, never step efficacy, never adversary optimality. Every
claim below is envelope-relative.

**Recorded tradeoff (accepted mechanism, not a defect):** aggregating
techniques → tactics is precisely what makes these weights groundable
at ~38 flows, and it **loses AND-gate/join structure** — the
technique-level operator/join metadata stays in the GAP, untouched.

## Divergence vs the shuffled-class-label null

Null: 200 trials (seed 20260703); flows
reassigned to the four labels at random with class sizes preserved on
the deduplicated corpus; each trial's per-class quotient is scored
against the fixed aggregate exactly as the observed classes are.

| Class | flows (raw → dedup) | mean JSD vs aggregate (dedup) | raw robustness | null p50 | null p95 | exceeds null p95? |
|---|---|--:|--:|--:|--:|---|
| `objective_exfiltration` | 19 → 14 | 0.1876 | 0.1371 | 0.1580 | 0.2248 | **no** |
| `objective_impact` | 7 → 6 | 0.3330 | 0.3325 | 0.3256 | 0.4466 | **no** |
| `objective_exfiltration_impact` | 7 → 5 | 0.2894 | 0.3125 | 0.3560 | 0.4781 | **no** |
| `objective_none_c2` | 5 → 4 | 0.3348 | 0.3246 | 0.3870 | 0.5101 | **no** |

Aggregate (null profile): 38 → 29 flows; its dedup-vs-raw self-divergence is mean JSD **0.0401** (robustness of the null profile to the dedup discipline).

## Per-place JSD vs the aggregate (dedup primary)

| Place | `objective_exfiltration` | `objective_impact` | `objective_exfiltration_impact` | `objective_none_c2` |
|---|--:|--:|--:|--:|
| collection | 0.1138 | — | 0.4934 | 0.6100 |
| command-and-control | 0.1217 | 0.1551 | 0.1080 | 0.1949 |
| credential-access | 0.0502 | 0.7287 | — | 0.3928 |
| defense-impairment | 0.3113 | — | — | 0.3113 |
| discovery | 0.1790 | 0.3147 | 0.4659 | 0.2175 |
| execution | 0.1454 | 0.2347 | 0.1827 | 0.1164 |
| exfiltration | 0.3958 | — | 0.2365 | — |
| impact | — | 0.4300 | 0.0793 | — |
| initial-access | 0.0703 | 0.2282 | 0.3685 | 0.4465 |
| lateral-movement | 0.2069 | 0.3059 | 0.5570 | 0.2664 |
| persistence | 0.0870 | 0.1553 | 0.4362 | 0.3309 |
| privilege-escalation | 0.2016 | 0.3161 | 0.1296 | — |
| reconnaissance | 0.1909 | 0.4591 | — | — |
| resource-development | 0.4591 | 0.4591 | — | 0.4591 |
| stealth | 0.0939 | 0.2086 | 0.1258 | 0.3376 |

A `—` means the place has no flow-backed out-distribution in that
class on the deduplicated corpus (thinness left visible, per D9).

## Weighted structural discriminators (positive-weight support, dedup)

Computed over the transitions a weighted traversal can actually take
(primary weight > 0). Zero-weight structural transitions are retained
in the nets; they are excluded from these statistics only.

| Profile | supported / total transitions | reach from recon seed | reach from initial-access | objective from IA | shortest entry→obj | longest entry→obj | branching | distinct entry→obj paths | sinks | islands |
|---|---|--:|--:|---|---|---|--:|--:|---|---|
| `objective_exfiltration` | 74 / 109 | 14 | 14 | exfiltration: yes | 0 hops (exfiltration → exfiltration) | 13 hops (resource-development → exfiltration) | 5.29 | 198,774 | impact | — |
| `objective_impact` | 43 / 76 | 12 | 12 | impact: yes | 1 hops (command-and-control → impact) | 10 hops (resource-development → impact) | 3.58 | 1,192 | collection | — |
| `objective_exfiltration_impact` | 47 / 72 | 1 | 12 | exfiltration: yes, impact: yes | 1 hops (command-and-control → exfiltration) | 10 hops (initial-access → exfiltration) | 4.27 | 2,968 | credential-access, reconnaissance, resource-development | reconnaissance, resource-development |
| `objective_none_c2` | 39 / 57 | 1 | 13 | command-and-control: yes | 0 hops (command-and-control → command-and-control) | 8 hops (initial-access → command-and-control) | 3.55 | 192 | privilege-escalation, reconnaissance | — |
| `aggregate` | 114 / 122 | 15 | 15 | command-and-control: yes, exfiltration: yes, impact: yes | 0 hops (command-and-control → command-and-control) | 14 hops (resource-development → command-and-control) | 7.60 | 45,665,097 | — | — |

## Verdict

No class envelope diverges from the aggregate beyond the shuffled-label null p95 — the structural weight layer alone does not discriminate the envelopes at this corpus size; the behavioural (timeline-runner) half of the verification carries the question. 
Where a class's mean JSD sits relative to its null band is the
class-size-honest reading: smaller classes (4 flows deduplicated)
have wider null bands, so an identical JSD magnitude is weaker
evidence for them — the table reports the bands rather than a single
pooled threshold. The dedup-vs-raw robustness column and the
aggregate's self-divergence bound how much the operator-dedup
discipline itself moves the numbers.

