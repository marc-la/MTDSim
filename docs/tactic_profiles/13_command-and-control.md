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

Command and control produces a **channel** — a gain that is *part capability, part position*.
The beacon rides an owned foothold (capability, survives), but the channel resolves to an
address and a route that a position-mutating shuffle can disturb (position, disruptable). C2 is
therefore the profile's **secondary open contest**, and its distinguishing property is that the
channel is *architected to survive connection loss*: Fallback Channels T1008, proxy/CDN-fronting,
and Dynamic Resolution/DGA T1568 exist precisely so that losing one route does not sever control
([`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4). So an IP/topology shuffle **degrades
but may not sever** the channel — a **partial reset**, not a clean invalidation, whose outcome
depends on beacon-cadence vs move-interval and on whether fallback infrastructure is modelled.

The MTD-relevant rate is the **beacon interval**, not the channel lifetime: check-in cadence is
seconds-to-hours and tunable (Cobalt Strike default 30 s ± jitter; observed 2 s to 2 h+ —
[`c2_beaconing`](../extractions/c2_beaconing.md)), and a defender optimises a config sequence and
**switch timing against a switch cost** (Li/Shen/Zheng spatial-temporal MTD). The swept axis is
that switch-interval ÷ beacon-cadence ratio, traded against switch cost — so the sweep is wide.
**Reset verdict: partial (architected to survive); sweep width wide.**

What is **not captured**: the fallback/proxy/DGA resilience itself. The substrate would treat a
C2 route more simply than the architected-resilient reality, so a modelled shuffle *over-resets*
C2 relative to the literature — the divergence direction worth recording
([substrate primer](../specs/substrate_primer.md) §(e).1): here the substrate is *harsher* on
the attacker than reality, the opposite of the credential/persistence survivors. Air-gapped or
C2-optional campaigns route around the channel entirely (chemat2024: Stuxnet operated without a
C2 server), which the objective-conditioning (crit. 7) can express as a campaign that simply
does not depend on the resettable gain.

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0011 page | Application Layer Protocol T1071 (544), Ingress Tool Transfer T1105 (515); most platform-uniform tactic; **no timing** | Persistent channel; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-D, §IV-A, §IV-B | "Long-term connection"; HTTP preferred (blends); beacon "at given intervals" / "several times per day"; fast-flux URL rotation "every couple of minutes" | Long-lived channel + fast sub-cadence; the beacon cadence is the MTD-relevant rate — no per-tactic dwell | [fetched] |
| [`cho2020`](../extractions/cho2020.md) §V-A | Stealthy attackers "stay stealthy until the time comes" | Supports the low-signal persistent character; no per-tactic value | [fetched] |
| [`ling2023`](../extractions/ling2023.md) Appendix A (Command and Control) | **Both C&C techniques are un-categorisable** — "Using common ports … is not exploiting a vulnerability" — so CVE-based timing structurally *cannot price* C&C | Strongest gap evidence for this profile: C&C dwell is a free parameter in any model — exactly the Tier-3 declare-and-sweep territory | [fetched] |
| [`chemat2024`](../extractions/chemat2024.md) §Discussion, Table 5 | HTTPS C&C used by **all 18** surveyed APT groups; but C&C is optional — "Stuxnet can autonomously carry out … activities without … the C&C server" | Web-protocol channel is near-universal yet conditional on connectivity; supports a wide sweep (air-gapped campaigns route around it) | [fetched] |
| [`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4 (C2; Proxy T1090) | C2 "mimic[s] normal network traffic"; but proxies/CDN-fronting give "resiliency in the face of connection loss" and ride shared legitimate infra | Reset verdict is **partial, not clean**: an IP/topology shuffle disrupts the channel but C2 is *architected to survive connection loss* → wider sweep, not a hard reset; no per-tactic number | [fetched] |
| [`c2_beaconing`](../extractions/c2_beaconing.md) (Cobalt Strike 2021; BAYWATCH 2016; Zhang 2023) | Beacon check-in cadence is **seconds to hours, tunable** — Cobalt Strike default **30 s ±20% jitter**; BAYWATCH observed **every 2–3 s up to every 2 h+**; **>90% of malware families are periodic** (75 B connections) | The C2 dwell *is* the beacon interval — a tunable stealth spacing → Tier-3 declared, wide sweep across the range; §2 periodic-by-design | [fetched] |
| [`c2_beaconing`](../extractions/c2_beaconing.md) (Li, Shen, Zheng 2020) | Spatial-temporal MTD: defender optimises the config **sequence + switch timing** against a **switch cost** and **config-dependent exploit times** | Confirms the reset interval is the swept axis, traded against switch cost — the partial-reset verdict's sweep lever (**→§3**) | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** stealth-low-and-slow — **confirmed** (a persistent, low-signal channel that beacons on a regular cadence, not a discrete act).
- **Relative multiplier:** ×1.0 of the stealth anchor — the long-lived channel dwell; the MTD-relevant sub-rate is the beacon interval, expressed in the sweep.
- **Sweep range:** ×0.25–×4 (wide) — the beacon cadence spans seconds to hours+ (Cobalt Strike 30 s ± jitter; observed 2 s–2 h+), and the reset is partial/architected-to-survive.
- **Tier:** 3 — declared; Ling & Ekstedt show C&C is **un-priceable by CVE data** ("using common ports … is not exploiting a vulnerability"), so it is a free parameter in any model.
- **Justification (one paragraph):** C2 is the **secondary open contest**. §2 confirms low-and-slow — a long-term channel beaconing at intervals, with fast infrastructure sub-churn (fast-flux) — so it takes the stealth anchor at ×1.0, and the MTD-relevant rate is the *beacon interval* (seconds-to-hours, tunable), which is what an MTD move-interval competes against and what the wide sweep spans. §3's distinguishing property is that the channel is **architected to survive connection loss** (Fallback Channels T1008, proxy/CDN-fronting, DGA T1568), so an IP/topology shuffle **degrades but may not sever** it — a *partial* reset whose outcome rides switch-interval ÷ beacon-cadence traded against a switch cost. The divergence worth recording (substrate-primer §(e).1) runs the *opposite* way to the credential/persistence survivors: the substrate would model a C2 route more simply than architected reality, so a modelled shuffle **over-resets** C2 relative to the literature — the substrate is *harsher* on the attacker here. Tier-3 declared because CVE-based timing structurally cannot price C&C; the wide sweep and the partial-reset fraction feed the catalogue and the binding respectively, and air-gapped/C2-optional campaigns (crit. 7) route around the resettable gain entirely.
