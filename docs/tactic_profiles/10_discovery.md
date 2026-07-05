---
tactic: discovery
attack_id: TA0007
attack_url: https://attack.mitre.org/tactics/TA0007/
attack_version: 19.1
status: stub
group_hypothesis: scan-shaped
tier_hypothesis: 1 substrate
---

# Discovery — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Discovery is defined in the pinned v19.1 bundle as the phase where "the adversary is
trying to figure out your environment": techniques to gain knowledge of the system and
internal network so the adversary can observe the environment, orient itself, and decide
how to act, frequently using native operating-system tools
([TA0007](https://attack.mitre.org/tactics/TA0007/)).

Positionally it is the tenth tactic, but functionally a **recurring, cross-cutting**
post-compromise tactic — the adversary re-runs discovery at every new host and privilege
level to shape follow-on behaviour. It sits at the centre of the internal loop (discover →
move → escalate → collect). Its `scan-shaped` `group_hypothesis` pairs it with
Reconnaissance as a substrate-priced enumeration action, the difference being that
discovery runs from *inside* the estate.

The v19.1 technique surface has the **largest parent-technique count of any tactic** (34
parents) but only 15 sub-techniques — i.e. mostly flat, single-action enumerations. They
group into host/OS enumeration (System Information Discovery T1082 — 424 procedures, File
and Directory Discovery T1083, Process Discovery T1057, System Owner/User Discovery T1033,
Query Registry T1012), network and remote-system mapping (System Network
Configuration/Connections Discovery T1016/T1049, Remote System Discovery T1018, Network
Service Discovery T1046, Network Share Discovery T1135), account/permission/domain
enumeration (Account Discovery T1087, Permission Groups Discovery T1069, Domain Trust
Discovery T1482, Group Policy Discovery T1615), and a large cloud/container/virtualisation
block (Cloud Service Discovery T1526, Cloud Infrastructure Discovery T1580, Container and
Resource Discovery T1613, Virtual Machine Discovery T1673). It is one of the most
instrumented tactics (3,320 procedures across 562 malware). Cross-tactic overlaps are
light — Virtualization/Sandbox Evasion T1497 and Debugger Evasion T1622 are shared with
Stealth (the same environment checks serve orientation and evasion), and Network Sniffing
T1040 with Credential Access.

## 2. APT relevance — group-assignment argument

The literature **confirms `scan-shaped`**, distinguishing internal discovery from external
reconnaissance. Alshamrani describes the post-foothold phase as "internal network scanning"
and "internal reconnaissance" — Carbanak's operators captured employee activity (keyloggers,
form-grabbers, even video) and sent it to C&C while searching for data resources and critical
components ([`alshamrani2019`](../extractions/alshamrani2019.md) §II-A, §II-C Stage 3)
[fetched]. Mechanically this is the same enumeration modality as reconnaissance — host,
service and network mapping — run from *inside* the estate, which is why it pairs with
reconnaissance as the scan-shaped, substrate-priced group.

One nuance widens its character. Under the "position for future" objective, discovery is not
a burst but an indefinite mode: the attacker "keep[s] themselves updated with the changes …
studying and understanding the working of the system and the users … while staying
unnoticed", and does not proceed to exfiltration or impact at all
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C) [fetched]. So discovery spans a
fast internal scan (the substrate proxy) at one end and open-ended, low-and-slow watching at
the other. The profile keeps it `scan-shaped` / Tier 1 as modelled, noting the
position-for-future mode is a slower character the substrate scan does not capture. Its
strong MTD-reset property — a topology shuffle invalidates the internal map — is a §3 matter.
No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0007 page | Largest parent count (34), mostly flat enumerations; System Information Discovery T1082 (424); **no timing** | Internal enumeration; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-A, §II-C Stage 3 | Internal network scanning / internal recon (Carbanak keyloggers/video); position-for-future = indefinite passive watching | Scan modality → substrate scan (Tier 1); position-for-future is slower — no number | [fetched] |
| [`rodriguez2024`](../extractions/rodriguez2024.md) §2–3 | The paper's tactic-level example is discovery via Network Service Discovery T1046 (Nmap); the Petri net is **untimed** | Gap-confirming: even the one tactic-level model gives discovery *ordering*, not dwell | [fetched] |
| [`brown2023`](../extractions/brown2023.md) §IV | Substrate models host-discovery + port-scan as timed phases; a shuffle forces re-discovery | The scan-shaped anchor discovery inherits; reset semantics (→§3) | [fetched] |
| [`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4 (Discovery) | "The discovery phase can take a long time"; DFIR BlackSuit case ran discovery (systeminfo/nltest/Sharphound) **~6 h after initial access** | Tempers pure scan-speed with a slower internal-enumeration character (a shape divergence like reconnaissance's); the modality still maps to the substrate scan — no per-tactic number | [fetched] |
| [`ling2023`](../extractions/ling2023.md) Appendix A (Discovery) | Discovery techniques (Remote System Discovery, Network Connection Enumeration) → *Information Leakage* vuln category | Per-technique CVE shape for discovery; no dwell (method needs real CVEs) | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn scan-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
