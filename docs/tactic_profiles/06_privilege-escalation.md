---
tactic: privilege-escalation
attack_id: TA0004
attack_url: https://attack.mitre.org/tactics/TA0004/
attack_version: 19.1
status: stub
group_hypothesis: exploit-shaped
tier_hypothesis: 1 substrate
---

# Privilege Escalation — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Privilege Escalation is defined in the pinned v19.1 bundle as the phase where "the
adversary is trying to gain higher-level permissions": gaining elevated access —
SYSTEM/root, local administrator, or a specifically-privileged account — typically by
taking advantage of system weaknesses, misconfigurations, and vulnerabilities
([TA0004](https://attack.mitre.org/tactics/TA0004/)). The bundle explicitly flags that
these techniques "often overlap with Persistence techniques", since persistence
mechanisms frequently execute in an elevated context.

Positionally it is the sixth tactic, but in practice it is **interleaved** with the early
post-compromise loop (execute → persist → escalate → discover) rather than a discrete
stage: the bundle notes an adversary "can often enter and explore a network with
unprivileged access but require elevated permissions to follow through on their
objectives", i.e. escalation happens on demand when an objective needs it. Its
`exploit-shaped` `group_hypothesis` reflects that its purest form (T1068) is a
substrate-priced exploit action.

The v19.1 technique surface (13 parent, 83 sub-techniques) splits into direct
exploitation (Exploitation for Privilege Escalation T1068, Escape to Host T1611),
token/mechanism abuse (Access Token Manipulation T1134, Abuse Elevation Control
Mechanism T1548), and a large block shared with Persistence — 7 of the 13 parents (Boot
or Logon Autostart Execution T1547, Scheduled Task/Job T1053, Create or Modify System
Process T1543, Event Triggered Execution T1546, Account Manipulation T1098, Boot or Logon
Initialization Scripts T1037, plus Valid Accounts T1078). Process Injection T1055 is
shared with Stealth (injecting into a live process both evades defences and can elevate),
and Domain or Tenant Policy Modification T1484 with Defense Impairment. With 1,471
procedure examples across 453 malware families, the heavy overlap set makes
privilege-escalation less a standalone stage than a property acquired through techniques
that also serve persistence and evasion.

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: exploit-shaped. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0004 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn exploit-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
