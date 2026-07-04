---
tactic: execution
attack_id: TA0002
attack_url: https://attack.mitre.org/tactics/TA0002/
attack_version: 19.1
status: stub
group_hypothesis: stealth-low-and-slow
tier_hypothesis: 3 declared
---

# Execution — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Execution is defined in the pinned v19.1 bundle as the phase where "the adversary is
trying to run malicious code": techniques that result in adversary-controlled code
running on a local or remote system
([TA0002](https://attack.mitre.org/tactics/TA0002/)). The definition itself stresses the
tactic's cross-cutting character — execution techniques are "often paired with techniques
from all other tactics" (the bundle's example: a remote-access tool running a PowerShell
script that performs Remote System Discovery).

Positionally it is the fourth tactic, immediately post-foothold, but functionally a
**recurring, cross-cutting** tactic rather than a single stage — code execution underlies
most on-host actions throughout the intrusion. In the narrative it is less a place the
attacker *dwells* than the verb by which other tactical goals are achieved, which is what
makes its dwell character (the `stealth-low-and-slow` `group_hypothesis`) a genuine
question for §2 rather than a substrate-priced given.

The v19.1 technique surface is large (20 parent, 44 sub-techniques) and dominated by
Command and Scripting Interpreter T1059 (1,017 procedure examples — the largest
single-technique count in this study), followed by User Execution T1204, Native API
T1106 and Scheduled Task/Job T1053, then a broad spread across service, IPC, container,
serverless/cloud and CI-CD execution surfaces (System Services T1569, Inter-Process
Communication T1559, Container Administration Command T1609, Serverless/Cloud
Administration T1648/T1651, ESXi Administration Command T1675, Poisoned Pipeline
Execution T1677). It is the most heavily instrumented tactic overall (2,317 procedure
examples across 565 malware families). Its cross-tactic mappings are extensive —
Scheduled Task/Job T1053 (also Persistence, Privilege Escalation), Hijack Execution Flow
T1574 (also Stealth), Software Deployment Tools T1072 (also Lateral Movement), BITS Jobs
T1197 (also Stealth, Persistence) — reflecting that "run code" is the shared mechanism
beneath many other tactics.

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: stealth-low-and-slow. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0002 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn stealth-low-and-slow>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 3 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
