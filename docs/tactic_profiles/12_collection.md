---
tactic: collection
attack_id: TA0009
attack_url: https://attack.mitre.org/tactics/TA0009/
attack_version: 19.1
status: stub
group_hypothesis: objective-execution
tier_hypothesis: 2 literature
---

# Collection — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Collection is defined in the pinned v19.1 bundle as the phase where "the adversary is
trying to gather data of interest to their goal": gathering the information, and the
sources it comes from, that is relevant to following through on the objective — commonly
as a precursor to Exfiltration ([TA0009](https://attack.mitre.org/tactics/TA0009/)). The
bundle notes the usual next step is to steal (exfiltrate) the data or to use it to learn
more about the environment.

Positionally it is the twelfth tactic; a late-stage, **objective-adjacent** tactic that
pairs directly with Exfiltration (collect → stage → exfiltrate). It is where the campaign
begins to act on its purpose rather than merely enabling itself, which is why its
`group_hypothesis` is `objective-execution` (Tier 2 — a candidate for
literature-calibrated timing rather than a substrate constant).

The v19.1 technique surface (17 parent, 24 sub-techniques) divides into source-based
gathering (Data from Local System T1005 — 229 procedures, Data from Network Shared Drive
T1039, Data from Removable Media T1025, Data from Information Repositories T1213, Data from
Cloud Storage T1530, Data from Configuration Repository T1602), capture-based gathering
(Input Capture T1056, Screen Capture T1113, Audio/Video Capture T1123/T1125, Clipboard
Data T1115, Email Collection T1114), staging and packaging (Data Staged T1074, Archive
Collected Data T1560), and interception (Adversary-in-the-Middle T1557, Browser Session
Hijacking T1185). Its cross-tactic overlap is with Credential Access (Input Capture T1056,
Adversary-in-the-Middle T1557 — one capture serves both), reflecting that the same
instrumentation that harvests credentials also harvests data. 1,311 procedures across 347
malware families.

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: objective-execution. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0009 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn objective-execution>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 2 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
