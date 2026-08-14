---
tactic: reconnaissance
attack_id: TA0043
attack_url: https://attack.mitre.org/tactics/TA0043/
attack_version: 19.1
status: reconciled
group_hypothesis: scan-shaped
tier_hypothesis: 1 substrate
---

# Reconnaissance — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../operational_validation.md).
> Catalogue (the §5 distillation): [`../../data/ogasp/tactic_durations.json`](../../../../data/ogasp/tactic_durations.json).
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
versions, running software and IDS/IPS ([`alshamrani2019`](../../../sources/extractions/alshamrani2019.md)
§II-C Stage 1) [fetched]. So reconnaissance *does* include the active probing the substrate
models; what makes it low-and-slow is tempo and attribution — conducted over time, from
outside, as human/service tradecraft. Jalowski's 2026 MTD gap-analysis adds the adversarial
sharpening: APTs favour passive reconnaissance "to remain in the shadows and learn mutation
patterns over time", so an active-scanning baseline like Nmap is "too naive" as the *only*
model ([`jalowski2026`](../../../sources/extractions/jalowski2026.md) §4) [fetched].

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
the catalogue header should acknowledge rather than hide. The external-scan empirics sharpen
this: a full-space scan runs in *minutes* with modern tooling and follows a disclosure within
24–48 h ([`internet_scanning_empirics`](../../../sources/extractions/internet_scanning_empirics.md)) [fetched],
so the *modality* is fast and the low-and-slow character is scheduling, not per-scan cost —
even as recon consumes a reported ~45% of attacker effort overall
([`mtd_scan_disruption`](../../../sources/extractions/mtd_scan_disruption.md), Carroll 2014 §I) [fetched].
No point number is landed here (deferred to §5).

## 3. MTD interaction — reasoned from mechanism (declared)

Reconnaissance produces a **map** — a pure position/knowledge gain (the external attack
surface: reachable hosts, open ports, service/OS fingerprints). Read against the substrate's
reset model it is the **canonical reset-*vulnerable*** tactic, the survivor axis's opposite
pole to [[09_credential-access]]. A position-mutating (network-layer) IP/topology shuffle is
exactly the mutation that invalidates it: it re-addresses and re-links the terrain the map
described, so the accumulated reconnaissance is thrown away and the attacker is forced to
re-scan. This is Alshamrani's "the rearrangement of network or software components renders the
exploratory knowledge of the attacker useless"
([substrate primer](../../../implementation/substrate_primer.md) §(e)) made concrete.

*How hard* the shuffle bites is bounded by the scan-disruption literature, and it sets the
sweep width. A perfect shuffle caps attacker scan-success at **≈0.63 (1 − e⁻¹)** when vulnerable
hosts are sparse, RDAM misses **96.2%** of domain-name scans, and DRL mutation adds
**26–58.7%** scan time — but the effect is governed by a **mutation-rate ÷ scan-rate ratio**,
so the magnitude spans near-total reset (fast mutation) to modest (slow)
([`mtd_scan_disruption`](../../../sources/extractions/mtd_scan_disruption.md)). **Reset verdict: invalidated;
sweep width wide** — the *direction* is firm but the magnitude rides that ratio. One structural
limit tempers it: exposed endpoints are never mutated
([substrate primer](../../../implementation/substrate_primer.md) §(c)), so reconnaissance of the *perimeter*
(the route in) survives — it is the *interior* map that resets.

What is **not captured**: the low-and-slow, off-network, mutation-pattern-learning
reconnaissance the literature attributes to APTs (Jalowski: passive recon to "learn mutation
patterns over time"). The substrate meters reconnaissance as a fast active scan and cannot
represent an attacker who *learns the shuffle schedule* and times around it — the adaptivity
deferral ([substrate primer](../../../implementation/substrate_primer.md) §(f)). So the modelled reset is a
worst-case for a naive scanner; a schedule-aware recon attacker would reset less, which the
sweep's upper (attacker-favourable) bound gestures at without modelling.

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0043 page | 12 parent techniques, all `PRE`; definition + technique list; **no timing** | Establishes off-network, recurrent character; no duration to inherit | [fetched] |
| [`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C Stage 1 | APT recon is *non-exploitative* but active (port/service scanning, WHOIS/BGP, fingerprinting), patient and off-network; no duration given | Qualitative low-and-slow *tempo*; the active-scan modality maps to the substrate scan verb — no per-tactic number | [fetched] |
| [`jalowski2026`](../../../sources/extractions/jalowski2026.md) §4 | APTs use *passive* recon to "remain in the shadows and learn mutation patterns"; Nmap baselines "too naive" | Confirms passive character; motivates the substrate-proxy caveat in §2 | [fetched] |
| [`ferraz2024`](../../../sources/extractions/ferraz2024.md) §5 | CTI tactic ordering is "used only to organize techniques, rather than to recover an execution timeline" | Gap-confirming: even where recon is documented, the corpus carries no dwell | [fetched] |
| [`selmanaj2024`](../../../sources/extractions/selmanaj2024.md) Ch. 4 (Reconnaissance) | Passive recon is "the least risky … characteristic of an APT behavior" but "time-consuming"; active recon "generally a sign of an ongoing attack"; recon "can occur at any stage" | Emulation-textbook confirmation of the patient/off-network default; the active modality is what the substrate scan-prices — no per-tactic number | [fetched] |
| [`internet_scanning_empirics`](../../../sources/extractions/internet_scanning_empirics.md) (Durumeric 2014 §1/§4; Griffioen 2024 §4.3/§6.6) | ZMap/Masscan scan the whole IPv4 space "from months to minutes"; attackers scan **within 24–48 h of disclosure**; post-disclosure surge is **transient** (dies in weeks); recurrent scanners "repeat within one day", but only institutional scanners re-scan daily | Empirical Tier-2 anchor: the scan *verb* is fast (minutes), so recon slowness is *scheduling* (opportunistic re-scan on new intel), not per-scan cost — reinforces the §2 shape-not-scale tempo divergence | [fetched] |
| [`mtd_scan_disruption`](../../../sources/extractions/mtd_scan_disruption.md) (Carroll 2014 §IV; Crouse 2015 §5; Jafarian 2015 §V; Wang 2017 §5.1; Zhang-DRL 2023; Ferguson-Walter 2021 §6) | Recon ≈ **45% of attacker time**; perfect shuffle caps attacker success at **≈0.63 (1 − e⁻¹; −37%)** when vulnerables are sparse; RDAM misses **96.2%** of domain-name scans; reset strength governed by **mutation-rate ÷ scan-rate ratio**; DRL mutation adds **26–58.7%** scan time; decoys **halve** red-team exfil | MTD-reset evidence for recon: a shuffle/obfuscation invalidates recon gains → forced re-scan (**→§3**); the ratio law + magnitudes set the sweep width | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** scan-shaped — **confirmed as modelled.** The substrate prices reconnaissance as an active scan verb; the patient, off-network, schedule-learning recon the literature reports is a recorded *tempo* divergence (§2), folded into off-network prep, not a separate metered dwell.
- **Relative multiplier:** ×1.0 of the scan-verb anchor (`ATTACK_DURATION` `SCAN_HOST`/`SCAN_NEIGHBOR` 5 s, `SCAN_PORT` 25 s) — one enumeration pass, **not tuned**.
- **Sweep range:** ×0.5–×2 (moderate) — the scan verb is substrate-fixed, but the un-metered low-and-slow scheduling (§2) warrants a modest robustness band on the modelled value.
- **Tier:** 1 — substrate-anchored (the scan verb prices it directly); not tuned.
- **Justification (one paragraph):** Reconnaissance is the scan-shaped pole the whole survivor-vs-vulnerable axis is defined against. §2 confirms the group: Alshamrani's recon is *non-exploitative but active* (port/service scanning, fingerprinting), and that active modality is exactly what the substrate's scan verb meters, so the central duration is the inherited scan constant (Tier 1, ×1.0, not tuned) rather than a tuned value. §3 makes it the canonical **reset-*vulnerable*** tactic — a position-mutating shuffle erases the map and forces a re-scan, magnitude riding the mutation-rate ÷ scan-rate ratio (the ≈0.63 = 1 − e⁻¹ ceiling) — and that reset verdict + its wide band feed the L3b binding, not the duration. The moderate duration sweep reflects the honest shape-not-scale gap: the *modelled* value is the fixed scan verb while the *real* tempo is slower and externally staged (§2), and exposed endpoints being shuffle-exempt means perimeter recon survives even as the interior map resets.
