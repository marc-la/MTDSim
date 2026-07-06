---
tactic: initial-access
attack_id: TA0001
attack_url: https://attack.mitre.org/tactics/TA0001/
attack_version: 19.1
status: stub
group_hypothesis: exploit-shaped
tier_hypothesis: 1 substrate
---

# Initial Access — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Initial Access is defined in the pinned v19.1 bundle as the phase where "the adversary
is trying to get into your network": the entry-vector techniques that gain the first
foothold, from targeted spearphishing to exploiting weaknesses on public-facing servers
([TA0001](https://attack.mitre.org/tactics/TA0001/)). The bundle notes the foothold's
durability varies — some vectors yield continued access (valid accounts, external remote
services), others are limited-use (e.g. a password that later changes).

Positionally it is the third tactic and the **first on-network tactic** — the boundary
the campaign crosses from `PRE` into the enterprise estate. In the APT narrative it is
the hinge between off-network preparation (reconnaissance, resource-development) and
every post-compromise action that follows; it is where the substrate's exploit-priced
model first engages, hence the `exploit-shaped` `group_hypothesis`.

The v19.1 technique surface (11 parent, 11 sub-techniques) covers social-engineering
delivery (Phishing T1566 — the single most-observed technique here at 262 procedures),
credential-based entry (Valid Accounts T1078), server- and client-side exploitation
(Exploit Public-Facing Application T1190, Drive-by Compromise T1189), trusted-path abuse
(Trusted Relationship T1199, Supply Chain Compromise T1195), remote-service, hardware and
RF vectors (External Remote Services T1133, Hardware Additions T1200, Wi-Fi Networks
T1669, Replication Through Removable Media T1091), and content injection (T1659).
Several techniques are explicitly multi-tactic — Valid Accounts T1078 spans Initial
Access, Persistence, Privilege Escalation and Stealth; External Remote Services T1133
spans Initial Access and Persistence; T1091 reaches Lateral Movement and T1659 reaches
Command and Control — encoding how an entry vector doubles as a persistence or movement
mechanism. Heavily attributed overall: 635 procedures across 143 groups and 128 malware
families.

## 2. APT relevance — group-assignment argument

The literature **confirms `exploit-shaped` for the server-side path, with a caveat for the
human-triggered vectors.** Alshamrani's Stage 2 enumerates the APT entry set — exploitation
of *known* vulnerabilities (the majority, per Ussath), spear-phishing (the single most
common initial-compromise vector), zero-day (rare), watering-hole and web download
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 2, §VIII) [fetched]. The
server-side exploitation half (Exploit Public-Facing Application T1190, Exploitation of
Remote Services) is exactly what the substrate's complexity-scaled `exploit_time` prices,
so those techniques inherit a Tier-1 anchor and are *not tuned*.

The caveat is that the phishing/watering-hole half carries a behaviour the exploit model
does not capture: after delivery, "attackers patiently wait for the malware to run within
the organization's network" — a human-triggered, potentially long wait for a user to open
the attachment ([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 2)
[fetched]. This is the closest initial-access comes to a low-and-slow dwell, and it sits
uneasily inside an exploit-priced state. The profile keeps initial-access `exploit-shaped`
/ Tier 1 (the substrate models entry as an exploit), but records the delivery-wait as a
shape divergence: the modelled action is a fast exploit, the literature vector is often a
patient wait. No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0001 page | 11 parent techniques; Phishing T1566 dominant (262 procedures); **no timing** | First on-network tactic; models entry as an exploit — no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 2, §VIII | Entry via *known*-vuln exploit (majority), spear-phishing (most common), zero-day rare; post-delivery the attacker "patiently wait[s]" for user-triggered execution | Server-side half → substrate `exploit_time` (Tier 1); the delivery-wait is a shape divergence, not a metered dwell | [fetched] |
| [`bland2020`](../extractions/bland2020.md) §2.1, §4 | Timed SPN models spear-phishing (CAPEC 163) and XSS (CAPEC 63/66); transition rates "notional … randomly selected between one and ten", realistic rates deferred to SMEs | Declare-and-sweep precedent for this tactic's timing; SME face-validation legitimises a declared value | [fetched] |
| [`brown2023`](../extractions/brown2023.md) §IV | Substrate prices exploitation by CVSS attack-complexity ∈ [0.4, 1] | The Tier-1 anchor initial-access inherits (complexity-scaled `exploit_time`) | [fetched] |
| [`breach_reports_macro_timing`](../extractions/breach_reports_macro_timing.md) (CrowdStrike GTR) | eCrime **breakout time** (initial access → lateral movement) avg **29 min** / fastest **27 s** (2026 ed.); 48 min / 51 s (2025 ed.); one case **exfil began within 4 min of initial access** | Tier-2 macro bound on the *fast (eCrime) end* of the early-chain dwell that starts at initial-access; whole-transition, not per-tactic | [fetched] |
| [`mcqueen2006`](../extractions/mcqueen2006.md) §3.1.2, Fig. 9 | Process-1 (known vuln + ready exploit) mean = **1 day (8 h)**, skill-independent; the no-known-vuln declared dwell is 21 d (expert) → 193 d (novice) | The MTTC-lineage declared value for an exploit-shaped entry: an easy-exploit foothold is ~a working day, badged Tier-2 declared + swept | [fetched] |
| [`ling2023`](../extractions/ling2023.md) Appendix A, Table 7 | Initial-Access techniques map to *Access Control* / *Web* vuln categories; expert TTC floor **6 days** across all combinations | Per-technique empirical shape for exploit-priced entry; the constant expert floor supports a group anchor over per-tactic values | [fetched] |
| [`initial_access_timing`](../extractions/initial_access_timing.md) (DBIR 2024; Mandiant TTE 2023) | Phishing **click in 21 s** (+28 s to data entry); average time-to-exploit collapsed **63 → 44 → 32 → 5 days** (2018→2023), 70% first exploited as zero-days | Fast-end empirical anchors: the metered exploit/click action is seconds-to-days; the low-and-slow is pre-delivery, not the action (sharpens §2) | [fetched] |
| [`initial_access_timing`](../extractions/initial_access_timing.md) (Holm 2014 §5.2–5.3) | TTC over **203k intrusions / 262k systems** is **heavy-tailed (Pareto/lognormal), not exponential**; TTC *decreases* with each successive intrusion | Distribution-shape caveat: a declared entry-time sweep should explore a heavy tail, not memoryless — flags the substrate's inherited exponential as suspect (for Marc, not actioned) | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn exploit-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
