---
tactic: exfiltration
attack_id: TA0010
attack_url: https://attack.mitre.org/tactics/TA0010/
attack_version: 19.1
status: stub
group_hypothesis: objective-execution
tier_hypothesis: 2 literature
---

# Exfiltration — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Exfiltration is defined in the pinned v19.1 bundle as the phase where "the adversary is
trying to steal data": techniques for removing data from the network, often after
packaging it (compression, encryption) to avoid detection, typically over the
command-and-control channel or an alternate channel and sometimes with transfer-size
limits ([TA0010](https://attack.mitre.org/tactics/TA0010/)).

Positionally it is the fourteenth tactic; a **terminal objective** tactic (with Impact)
that consumes the output of Collection and rides the Command-and-Control channel. In a
data-theft campaign it is the endpoint the whole intrusion serves, which is why its
`group_hypothesis` is `objective-execution` (Tier 2 — a candidate for
literature-calibrated timing, since the breach literature reports access→exfil milestones
even though it reports no per-tactic dwell).

The v19.1 technique surface is one of the smallest in the matrix (9 parent, 10
sub-techniques), and channel choice dominates it: Exfiltration Over C2 Channel T1041 (201
procedures — over half the tactic's total), Exfiltration Over Alternative Protocol T1048,
Exfiltration Over Web Service T1567, Exfiltration Over Other Network Medium T1011,
Exfiltration Over Physical Medium T1052, and Transfer Data to Cloud Account T1537 — plus
shaping/automation techniques (Automated Exfiltration T1020, Scheduled Transfer T1029, Data
Transfer Size Limits T1030). It has no cross-tactic mappings — exfiltration techniques are
exfiltration-only — but is tightly semantically coupled to C2 (T1041 exfiltrates over the
same channel as T1071/T1105). 396 procedures across 215 malware families, a smaller
footprint than the enabling tactics.

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: objective-execution. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0010 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn objective-execution>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 2 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
