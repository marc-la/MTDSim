---
tactic: initial-access
attack_id: TA0001
attack_url: https://attack.mitre.org/tactics/TA0001/
attack_version: 19.1
status: stub
group_hypothesis: exploit-shaped
tier_hypothesis: 1 substrate
---

# Initial Access — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Initial Access is defined in the pinned v19.1 bundle as the phase where "the adversary
is trying to get into your network": the entry-vector techniques that gain the first
foothold, from targeted spearphishing to exploiting weaknesses on public-facing servers
([TA0001](https://attack.mitre.org/tactics/TA0001/)). The bundle notes the foothold's
durability varies — some vectors yield continued access (valid accounts, external remote
services), others are limited-use (e.g. a password that later changes).

Positionally it is the third tactic and the **first on-network tactic** — the boundary
the campaign crosses from `PRE` into the enterprise estate. In the APT narrative it is
the hinge between off-network preparation (reconnaissance, resource-development) and
every post-compromise action that follows; it is where the substrate's exploit-priced
model first engages, hence the `exploit-shaped` `group_hypothesis`.

The v19.1 technique surface (11 parent, 11 sub-techniques) covers social-engineering
delivery (Phishing T1566 — the single most-observed technique here at 262 procedures),
credential-based entry (Valid Accounts T1078), server- and client-side exploitation
(Exploit Public-Facing Application T1190, Drive-by Compromise T1189), trusted-path abuse
(Trusted Relationship T1199, Supply Chain Compromise T1195), remote-service, hardware and
RF vectors (External Remote Services T1133, Hardware Additions T1200, Wi-Fi Networks
T1669, Replication Through Removable Media T1091), and content injection (T1659).
Several techniques are explicitly multi-tactic — Valid Accounts T1078 spans Initial
Access, Persistence, Privilege Escalation and Stealth; External Remote Services T1133
spans Initial Access and Persistence; T1091 reaches Lateral Movement and T1659 reaches
Command and Control — encoding how an entry vector doubles as a persistence or movement
mechanism. Heavily attributed overall: 635 procedures across 143 groups and 128 malware
families.

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: exploit-shaped. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0001 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn exploit-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
