---
tactic: command-and-control
attack_id: TA0011
attack_url: https://attack.mitre.org/tactics/TA0011/
attack_version: 19.1
status: stub
group_hypothesis: stealth-low-and-slow
tier_hypothesis: 3 declared
---

# Command And Control — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Command and Control is defined in the pinned v19.1 bundle as the phase where "the
adversary is trying to communicate with compromised systems to control them": techniques
for communicating with systems under the adversary's control within a victim network,
commonly mimicking normal, expected traffic to avoid detection
([TA0011](https://attack.mitre.org/tactics/TA0011/)). The bundle notes C2 spans "various
levels of stealth depending on the victim's network structure and defenses".

Positionally it is the thirteenth tactic, but functionally a **cross-cutting channel**
maintained continuously from shortly after the foothold through to exfiltration — the
connective tissue of the intrusion rather than a discrete stage. Exfiltration Over C2
Channel (T1041) makes it the literal conduit for the objective, and its
`stealth-low-and-slow` `group_hypothesis` reflects that a C2 channel is a persistent,
low-signal presence whose survival across an MTD reset is a central §3 question.

The v19.1 technique surface (18 parent, 27 sub-techniques) covers protocol-blending
channels (Application Layer Protocol T1071 — 544 procedures, Non-Application Layer Protocol
T1095, Web Service T1102, Non-Standard Port T1571), payload transfer (Ingress Tool
Transfer T1105 — 515 procedures), traffic concealment (Encrypted Channel T1573, Data
Obfuscation T1001, Data Encoding T1132, Protocol Tunneling T1572, Hide Infrastructure
T1665), channel resilience (Fallback Channels T1008, Multi-Stage Channels T1104, Dynamic
Resolution T1568 — DGA), and interactive tooling (Remote Access Tools T1219). Notably every
one of its 18 parent techniques covers Windows, Linux and macOS — the most platform-uniform
tactic in the matrix, consistent with C2 being an OS-agnostic network behaviour. 2,317
procedures across 563 malware families; cross-tactic overlap is light (Content Injection
T1659 with Initial Access, Traffic Signaling T1205 with Persistence and Stealth).

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: stealth-low-and-slow. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0011 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn stealth-low-and-slow>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 3 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
