---
tactic: lateral-movement
attack_id: TA0008
attack_url: https://attack.mitre.org/tactics/TA0008/
attack_version: 19.1
status: stub
group_hypothesis: exploit-shaped
tier_hypothesis: 1 substrate
---

# Lateral Movement — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Lateral Movement is defined in the pinned v19.1 bundle as the phase where "the adversary
is trying to move through your environment": entering and controlling remote systems,
typically pivoting through multiple systems and accounts to reach the target, either with
installed remote-access tools or — stealthier — with legitimate credentials and native
network/OS tools ([TA0008](https://attack.mitre.org/tactics/TA0008/)).

Positionally it is the eleventh tactic; the tactic that **expands a single foothold into
estate-wide reach**, tightly coupled to Credential Access (which supplies the material)
and Discovery (which supplies the map), and recurring per hop. Its `exploit-shaped`
`group_hypothesis` reflects that its dominant form is a remote-service login/exploitation
the substrate can price — though the bundle stresses the credential-reuse path is often
chosen precisely because it is quieter than exploitation.

The v19.1 technique surface is comparatively compact (9 parent, 14 sub-techniques). It is
dominated by Remote Services T1021 (190 procedures — RDP/SSH/SMB/VNC/WinRM logons),
followed by alternate-authentication movement (Use Alternate Authentication Material T1550
— pass-the-hash/ticket/token), tool and payload propagation (Lateral Tool Transfer T1570,
Taint Shared Content T1080, Software Deployment Tools T1072), session hijacking (Remote
Service Session Hijacking T1563), removable-media and internal-phishing vectors
(Replication Through Removable Media T1091, Internal Spearphishing T1534), and
remote-service exploitation (Exploitation of Remote Services T1210). Its multi-tactic ties
reflect this dependence on other stages — T1091 is shared with Initial Access, T1072 with
Execution. With 367 procedures across 76 groups it is a smaller, more deliberate technique
set than the enabling tactics (Execution, Stealth, Discovery).

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: exploit-shaped. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0008 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn exploit-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
