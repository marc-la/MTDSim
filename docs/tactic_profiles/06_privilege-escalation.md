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

The literature **confirms `exploit-shaped`** for the tactic's purest form while noting a
fast, non-exploit path. Alshamrani places privilege escalation inside the interleaved
post-foothold loop — "sometimes this phase involves privilege escalation … the chosen method
depends on the environment of the target system" — and its canonical instance is
vulnerability exploitation: Stuxnet used two Windows zero-days (a keyboard-file flaw and Task
Scheduler) to "gain full control of the machine by performing privilege escalation"
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3, §III-C) [fetched]. That
direct-exploitation form (Exploitation for Privilege Escalation T1068) is exactly what the
substrate's complexity-scaled `exploit_time` prices, so the tactic inherits a Tier-1 anchor
and is *not tuned*.

The caveat, from §1's overlap analysis, is that seven of the thirteen parents are shared
with Persistence and the token/valid-account variants (Access Token Manipulation T1134,
Valid Accounts T1078) are quick *reuse-of-material* acts rather than exploits — closer in
tempo to credential-access than to an exploit. Privilege-escalation's character is therefore
bimodal: an exploit (substrate-priced) or a fast token abuse. The profile keeps it
`exploit-shaped` / Tier 1 — the substrate models the exploit path — while noting the
token-abuse variant runs faster than the anchor implies. No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0004 page | T1068 exploit + token/mechanism abuse; 7/13 parents shared with Persistence; **no timing** | On-demand elevation; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3, §III-C | Escalation on demand; Stuxnet 2 Windows 0-days → "full control"; method depends on environment | Exploit form → substrate `exploit_time` (Tier 1); token-abuse variant is faster — no number | [fetched] |
| [`brown2023`](../extractions/brown2023.md) §IV | Substrate prices exploitation by CVSS attack-complexity ∈ [0.4, 1] | The Tier-1 anchor privilege-escalation inherits | [fetched] |
| [`rodriguez2024`](../extractions/rodriguez2024.md) §3 | Tactic-level ATT&CK Petri nets are **untimed** — timestamps only *order* events | Gap-confirming: no per-tactic rate even in a tactic-level model | [fetched] |
| [`xiong2021`](../extractions/xiong2021.md) §5.1.2 | enterpriseLang models PE as a hard permission gate: a `userRights` adversary "cannot use a technique that requires Administrator"; "an adversary can level up through Privilege Escalation … to gain adminRights" | Formal-model precedent for PE as a *gating state* that unlocks an admin-only technique subset — PE dwell is spent before those become reachable; structural, no timing | [fetched] |
| [`ling2023`](../extractions/ling2023.md) Appendix A, Table 7 | PE (Exploitation for Privilege Escalation) → *Authentication* vuln category; expert TTC floor **6 days** | Per-technique empirical shape for exploit-priced escalation; expert floor supports the exploit-shaped group anchor | [fetched] |
| [`mcqueen2006`](../extractions/mcqueen2006.md) §3.1.2 | Easy-exploit compromise mean **1 day**; the no-easy-exploit declared dwell **21 d (expert)** | MTTC-lineage declared value for the exploit-shaped case; a Tier-2 plausibility envelope for escalation dwell | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn exploit-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
