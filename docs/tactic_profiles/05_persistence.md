---
tactic: persistence
attack_id: TA0003
attack_url: https://attack.mitre.org/tactics/TA0003/
attack_version: 19.1
status: stub
group_hypothesis: stealth-low-and-slow
tier_hypothesis: 3 declared
---

# Persistence — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Persistence is defined in the pinned v19.1 bundle as the phase where "the adversary is
trying to maintain their foothold": techniques that keep access across restarts, changed
credentials, and other interruptions, via any access, action, or configuration change
that preserves the foothold — replacing or hijacking legitimate code, adding startup
code, and the like ([TA0003](https://attack.mitre.org/tactics/TA0003/)).

Positionally it is the fifth tactic; in the narrative it is established once a foothold
exists and then relied upon continuously, recurring whenever the adversary acquires a new
host or account. It is the **durability layer** beneath the whole post-compromise
campaign — the mechanism by which a gain survives the ordinary churn of a live
environment, which is exactly the property an MTD reset is designed to attack (deferred to
§3), and the reason its dwell character (`stealth-low-and-slow`) is load-bearing for the
timeline.

The v19.1 technique surface is one of the largest in the matrix (22 parent, 91
sub-techniques): autostart/boot-logon mechanisms (Boot or Logon Autostart Execution T1547
— 332 procedures, Boot or Logon Initialization Scripts T1037, Create or Modify System
Process T1543, Event Triggered Execution T1546), scheduled execution (Scheduled Task/Job
T1053), credential/account durability (Valid Accounts T1078, Account Manipulation T1098,
Create Account T1136, Modify Authentication Process T1556), server- and
application-level implants (Server Software Component T1505, Office Application Startup
T1137, Software Extensions T1176), and firmware/image/pre-OS footholds (Pre-OS Boot
T1542, Implant Internal Image T1525, Compromise Host Software Binary T1554). It is the
most cross-wired tactic in the matrix: 7 techniques are shared with Privilege Escalation,
4 with Stealth, plus overlaps into Execution, Initial Access, Credential Access, Defense
Impairment and Command and Control — the bundle notes persistence and privilege-escalation
"often overlap", since an OS feature that lets an adversary persist frequently runs in an
elevated context.

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: stealth-low-and-slow. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0003 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn stealth-low-and-slow>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 3 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
