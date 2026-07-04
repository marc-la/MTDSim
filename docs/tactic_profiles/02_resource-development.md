---
tactic: resource-development
attack_id: TA0042
attack_url: https://attack.mitre.org/tactics/TA0042/
attack_version: 19.1
status: stub
group_hypothesis: prep-off-network
tier_hypothesis: 3 declared
---

# Resource Development — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Resource Development is defined in the pinned v19.1 bundle as the phase where "the
adversary is trying to establish resources they can use to support operations":
creating, purchasing, or compromising/stealing the infrastructure, accounts, and
capabilities that back an intrusion ([TA0042](https://attack.mitre.org/tactics/TA0042/)).
The bundle makes the downstream links concrete — purchased domains support Command and
Control, email accounts enable phishing for Initial Access, stolen code-signing
certificates aid Defense Evasion (the pre-split label the description still carries).

Positionally it is the second tactic in the matrix and the second **pre-compromise** /
`PRE` tactic (with Reconnaissance); all 9 parent techniques are platform `PRE`, staged
*off* the victim network before and alongside the intrusion. In the campaign narrative
it is preparatory and largely invisible to the target: the adversary is building or
acquiring its own kit, so most activity leaves no trace inside the victim estate. It is
the tactic least coupled to the substrate's on-network model, which is why its
`group_hypothesis` is `prep-off-network`.

The v19.1 technique surface (9 parent, 41 sub-techniques) is organised as
acquire-vs-compromise pairs — infrastructure (Acquire Infrastructure T1583, Compromise
Infrastructure T1584), accounts (Establish Accounts T1585, Compromise Accounts T1586),
and capabilities (Develop Capabilities T1587, Obtain Capabilities T1588) — plus staging
(Stage Capabilities T1608), buying pre-existing access (Acquire Access T1650), and a
v19-era content-generation technique (Generate Content T1683) whose top procedures
reflect AI-assisted persona and content creation. It is the most heavily
group-/campaign-attributed pre-compromise tactic (563 procedure examples across 115
groups and 48 campaigns) with negligible malware attribution — again operator tradecraft
rather than on-host code. No technique crosses into another tactic.

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: prep-off-network. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0042 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn prep-off-network>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 3 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
