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

The literature **confirms `objective-execution`** — impact is the terminal payload of an
availability-/integrity-focused campaign. Alshamrani's Stage 4 covers the impediment case
directly: "when the attackers' goal is to undermine critical components, actions comprising
disabling or destroying the critical components", the canonical instance being Stuxnet's
sabotage of Iran's uranium centrifuges
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 4, §III-C) [fetched].
Unlike the enabling tactics, impact is where the campaign spends its accumulated access, so it
belongs with collection and exfiltration in the tuned objective-execution group.

Its dwell character is the most bimodal in the set, split by actor type. A ransomware or wiper
actor's impact is fast and decisive — encryption or destruction executed in a burst once
positioned (the WannaCry pattern; al-sada2024's per-tactic technique table lists impact as
Data Encrypted for Impact / Inhibit System Recovery / Service Stop,
[`al-sada2024`](../extractions/al-sada2024.md) §2 Table 1) [fetched]. An espionage actor with
a "position for future" goal may never reach impact at all
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C) [fetched]. And the dwell ceiling
is a *decision*, not a duration — an APT's campaign "ends when … the funding organization gets
all the data it needs" ([`alshamrani2019`](../extractions/alshamrani2019.md) §I, §II-C Stage
5) [fetched]. The profile confirms `objective-execution` / Tier 2 (the ransomware/IR literature
characterises time-to-impact) with a **wide range** spanning burst-impact to never. No point
number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0040 page | Data Encrypted for Impact T1486 (84); ransomware/destruction primitives; no cross-tactic mappings; **no timing** | Terminal payload; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 4, §III-C, §I | Disabling/destroying components (Stuxnet); dwell ceiling sponsor-bounded ("ends when the org gets the data it needs") | Objective-execution; burst-impact..never — no per-tactic number | [fetched] |
| [`al-sada2024`](../extractions/al-sada2024.md) §2 Table 1 | WannaCry impact = Data Encrypted for Impact / Inhibit System Recovery / Service Stop | Ransomware = fast decisive impact (contrast to espionage never-reaching) — technique map, no timing | [fetched] |
| Breach-report milestones (via [precedent survey](../notes/2026-07-04_tactic_duration_precedent_survey.md)) | ransomware dwell ~28 h median (Secureworks 2024); <4 d access→ransomware (IBM X-Force 2023) | Tier-2 macro anchor for the fast-impact end; reconcile before citing | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn objective-execution>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 2 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
