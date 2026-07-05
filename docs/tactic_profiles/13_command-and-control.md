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

The literature **confirms `stealth-low-and-slow`** — C2 is a persistent, low-signal channel,
not a discrete act. Alshamrani describes it as a "long-term connection to victims' devices",
carried over HTTP/HTTPS (preferred because "labeled as legal in most enterprise"), IRC, P2P or
custom protocols ([`alshamrani2019`](../extractions/alshamrani2019.md) §II-D) [fetched]. Its
signature is temporal: malware "typically sent beacon … to C&C servers at given intervals"
(Villeneuve & Bennett), with DNS-beaconing studies assuming infected hosts contact C2
"several times per day" (Shalaginov)
([`alshamrani2019`](../extractions/alshamrani2019.md) §IV-A) [fetched]. A channel that lives
for the duration of the intrusion and beacons on a regular cadence is the definition of
low-and-slow.

One counter-tempo sits inside it: the *infrastructure* churns fast — attackers "keep changing
malicious URLs every couple of minutes" (fast-flux) even as the *channel* persists
([`alshamrani2019`](../extractions/alshamrani2019.md) §IV-B) [fetched]. So C2's dwell is
long-lived at the channel level with fast sub-structure, and it is the beacon cadence, not the
channel lifetime, that an MTD move interval competes against (a §3 ratio-game matter). The
profile confirms `stealth-low-and-slow` / Tier 3 (declared) — no substrate verb prices
"maintain a C2 channel". No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0011 page | Application Layer Protocol T1071 (544), Ingress Tool Transfer T1105 (515); most platform-uniform tactic; **no timing** | Persistent channel; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-D, §IV-A, §IV-B | "Long-term connection"; HTTP preferred (blends); beacon "at given intervals" / "several times per day"; fast-flux URL rotation "every couple of minutes" | Long-lived channel + fast sub-cadence; the beacon cadence is the MTD-relevant rate — no per-tactic dwell | [fetched] |
| [`cho2020`](../extractions/cho2020.md) §V-A | Stealthy attackers "stay stealthy until the time comes" | Supports the low-signal persistent character; no per-tactic value | [fetched] |
| [`ling2023`](../extractions/ling2023.md) Appendix A (Command and Control) | **Both C&C techniques are un-categorisable** — "Using common ports … is not exploiting a vulnerability" — so CVE-based timing structurally *cannot price* C&C | Strongest gap evidence for this profile: C&C dwell is a free parameter in any model — exactly the Tier-3 declare-and-sweep territory | [fetched] |
| [`chemat2024`](../extractions/chemat2024.md) §Discussion, Table 5 | HTTPS C&C used by **all 18** surveyed APT groups; but C&C is optional — "Stuxnet can autonomously carry out … activities without … the C&C server" | Web-protocol channel is near-universal yet conditional on connectivity; supports a wide sweep (air-gapped campaigns route around it) | [fetched] |
| [`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4 (C2; Proxy T1090) | C2 "mimic[s] normal network traffic"; but proxies/CDN-fronting give "resiliency in the face of connection loss" and ride shared legitimate infra | Reset verdict is **partial, not clean**: an IP/topology shuffle disrupts the channel but C2 is *architected to survive connection loss* → wider sweep, not a hard reset; no per-tactic number | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn stealth-low-and-slow>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 3 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
