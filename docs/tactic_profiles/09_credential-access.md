---
tactic: credential-access
attack_id: TA0006
attack_url: https://attack.mitre.org/tactics/TA0006/
attack_version: 19.1
status: stub
group_hypothesis: exploit-shaped
tier_hypothesis: 1 substrate
---

# Credential Access — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Credential Access is defined in the pinned v19.1 bundle as the phase where "the adversary
is trying to steal account names and passwords": techniques for stealing credential
material such as account names and passwords, via keylogging, credential dumping and
related methods ([TA0006](https://attack.mitre.org/tactics/TA0006/)). The bundle notes the
payoff — legitimate credentials give access, make the adversary harder to detect, and
enable creating further accounts.

Positionally it is the ninth tactic; in the narrative it is a **post-compromise enabler**
tightly coupled to Lateral Movement and Privilege Escalation — stolen credentials are the
currency that turns a single foothold into movement and elevation — and it recurs whenever
a new host or identity store is reached. Its `exploit-shaped` `group_hypothesis` reflects
that dumping/cracking is an on-host action the substrate can price, though several of its
techniques (theft/forgery of tokens and tickets) are quicker, reuse-of-material acts.

The v19.1 technique surface (17 parent, 50 sub-techniques) covers dumping and
store-raiding (OS Credential Dumping T1003 — 201 procedures, Credentials from Password
Stores T1555, Unsecured Credentials T1552), capture (Input Capture T1056, Network Sniffing
T1040, Adversary-in-the-Middle T1557), guessing (Brute Force T1110), token/ticket theft
and forgery (Steal or Forge Kerberos Tickets T1558, Steal Application Access Token T1528,
Steal Web Session Cookie T1539, Forge Web Credentials T1606, Steal or Forge Authentication
Certificates T1649), and MFA-directed techniques (MFA Interception T1111, MFA Request
Generation T1621). Cross-tactic mappings tie it to Collection (Input Capture T1056,
Adversary-in-the-Middle T1557 — the same capture serves both credential theft and data
gathering), Discovery (Network Sniffing T1040), and Persistence/Defense-Impairment (Modify
Authentication Process T1556). Its 876 procedures span 215 malware and a notably high 37
tools, reflecting the Mimikatz-class utility ecosystem.

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: exploit-shaped. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0006 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn exploit-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
