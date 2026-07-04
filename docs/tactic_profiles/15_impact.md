---
tactic: impact
attack_id: TA0040
attack_url: https://attack.mitre.org/tactics/TA0040/
attack_version: 19.1
status: stub
group_hypothesis: objective-execution
tier_hypothesis: 2 literature
---

# Impact — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Impact is defined in the pinned v19.1 bundle as the phase where "the adversary is trying
to manipulate, interrupt, or destroy your systems and data": techniques that disrupt
availability or compromise integrity by manipulating business and operational processes,
including destroying or tampering with data — sometimes as the end goal, sometimes as
cover for a confidentiality breach ([TA0040](https://attack.mitre.org/tactics/TA0040/)).

Positionally it is the fifteenth and last tactic; the other **terminal objective** tactic
(with Exfiltration), where an availability-/integrity-focused campaign (ransomware, wiper,
fraud) delivers its payload. Its `objective-execution` `group_hypothesis` (Tier 2) mirrors
Exfiltration's — it is an end-state action whose timing the ransomware/IR literature
characterises even where per-tactic dwell is unpublished.

The v19.1 technique surface (15 parent, 18 sub-techniques) covers availability destruction
(Data Encrypted for Impact T1486 — 84 procedures, the ransomware-encryption technique;
Data Destruction T1485, Disk Wipe T1561, Firmware Corruption T1495), recovery denial and
service disruption (Inhibit System Recovery T1490, Service Stop T1489, System
Shutdown/Reboot T1529, Account Access Removal T1531), denial-of-service (Network/Endpoint
DoS T1498/T1499, Email Bombing T1667), integrity attacks (Data Manipulation T1565,
Defacement T1491), and objective-level abuse (Resource Hijacking T1496 — cryptomining,
Financial Theft T1657). It has no cross-tactic mappings — impact techniques are terminal by
nature. Its footprint is the smallest of the post-compromise tactics (378 procedures across
36 groups and 8 campaigns), and its most-attributed techniques are the ransomware and
destructive-attack primitives (encryption T1486, recovery inhibition T1490, service stop
T1489).

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: objective-execution. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0040 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn objective-execution>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 2 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
