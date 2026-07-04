---
tactic: reconnaissance
attack_id: TA0043
attack_url: https://attack.mitre.org/tactics/TA0043/
attack_version: 19.1
status: stub
group_hypothesis: scan-shaped
tier_hypothesis: 1 substrate
---

# Reconnaissance — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Reconnaissance is defined in the pinned v19.1 bundle as the phase where "the adversary
is trying to gather information they can use to plan future operations": actively or
passively gathering information that supports targeting, spanning details of the victim
organisation, its infrastructure, and its staff/personnel
([TA0043](https://attack.mitre.org/tactics/TA0043/)). The bundle ties the output
forward — gathered information is used to plan and execute Initial Access, to scope and
prioritise post-compromise objectives, and to "drive and lead further Reconnaissance
efforts".

Positionally it is the first tactic in the ATT&CK Enterprise matrix and one of the two
**pre-compromise** tactics (with Resource Development). All 12 parent techniques carry
the single platform tag `PRE`: the activity happens *off* the victim network, treating
the target from the outside rather than operating inside it. In an APT narrative it
opens the campaign, but by the definition's own wording it is recurrent rather than
one-shot — new internal targets surfaced mid-intrusion re-drive it.

The v19.1 technique surface (12 parent, 34 sub-techniques) divides into passive
open-source collection (Search Open Websites/Domains T1593, Search Open Technical
Databases T1596, Search Victim-Owned Websites T1594, Search Closed Sources T1597, Search
Threat Vendor Data T1681), targeted attribute-gathering (Gather Victim
Identity/Network/Org/Host Information, T1589–T1592), active probing (Active Scanning
T1595), interactive elicitation (Phishing for Information T1598), and a v19-era addition
reflecting AI-assisted tradecraft (Query Public AI Services T1682). Of its 170 procedure
examples the attribution is almost entirely to named groups (47) and campaigns (15),
with negligible malware/tool attribution — consistent with reconnaissance being human-
and service-driven and conducted from outside the estate. None of its techniques cross
into another tactic, reinforcing it as a clean pre-compromise stage.

## 2. APT relevance — group-assignment argument

The literature places APT reconnaissance at the **patient, low-and-slow** end, but the
"passive" label needs care. Alshamrani calls APT reconnaissance "passive" in the sense of
*non-exploitative* — "attackers do not exploit a victim, but instead are collecting data
in preparation for the attack" — yet the same passage lists **active** methods among it:
port scanning, service scanning, WHOIS/BGP queries and fingerprinting of open ports, OS
versions, running software and IDS/IPS ([`alshamrani2019`](../extractions/alshamrani2019.md)
§II-C Stage 1) [fetched]. So reconnaissance *does* include the active probing the substrate
models; what makes it low-and-slow is tempo and attribution — conducted over time, from
outside, as human/service tradecraft. Jalowski's 2026 MTD gap-analysis adds the adversarial
sharpening: APTs favour passive reconnaissance "to remain in the shadows and learn mutation
patterns over time", so an active-scanning baseline like Nmap is "too naive" as the *only*
model ([`jalowski2026`](../extractions/jalowski2026.md) §4) [fetched].

This creates a deliberate tension with the `scan-shaped` hypothesis, which the profile
**confirms for the executable model while flagging the divergence.** The substrate prices
reconnaissance as an *active* scan verb (`ATTACK_DURATION`), and the L3a nets model the
in-sim reconnaissance state as that scan — a Tier-1, substrate-anchored action, *not
tuned*. The patient, extended real-world recon the literature reports is not what the
simulator meters; it is effectively folded into off-network preparation
([[02_resource-development]]). Recording this keeps the group honest: reconnaissance stays
scan-shaped *as modelled* — the substrate's active scan is a fair proxy for the port/service
scanning and fingerprinting the literature attributes to recon — but the real activity is
slower, spread over time, and externally staged, a shape-not-scale divergence in *tempo*
the catalogue header should acknowledge rather than hide. No point number is landed here
(deferred to §5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0043 page | 12 parent techniques, all `PRE`; definition + technique list; **no timing** | Establishes off-network, recurrent character; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 1 | APT recon is *non-exploitative* but active (port/service scanning, WHOIS/BGP, fingerprinting), patient and off-network; no duration given | Qualitative low-and-slow *tempo*; the active-scan modality maps to the substrate scan verb — no per-tactic number | [fetched] |
| [`jalowski2026`](../extractions/jalowski2026.md) §4 | APTs use *passive* recon to "remain in the shadows and learn mutation patterns"; Nmap baselines "too naive" | Confirms passive character; motivates the substrate-proxy caveat in §2 | [fetched] |
| [`ferraz2024`](../extractions/ferraz2024.md) §5 | CTI tactic ordering is "used only to organize techniques, rather than to recover an execution timeline" | Gap-confirming: even where recon is documented, the corpus carries no dwell | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn scan-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
