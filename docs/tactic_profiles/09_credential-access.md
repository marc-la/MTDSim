---
tactic: credential-access
attack_id: TA0006
attack_url: https://attack.mitre.org/tactics/TA0006/
attack_version: 19.1
status: stub
group_hypothesis: exploit-shaped
tier_hypothesis: 1 substrate
---

# Credential Access — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Credential Access is defined in the pinned v19.1 bundle as the phase where "the adversary
is trying to steal account names and passwords": techniques for stealing credential
material such as account names and passwords, via keylogging, credential dumping and
related methods ([TA0006](https://attack.mitre.org/tactics/TA0006/)). The bundle notes the
payoff — legitimate credentials give access, make the adversary harder to detect, and
enable creating further accounts.

Positionally it is the ninth tactic; in the narrative it is a **post-compromise enabler**
tightly coupled to Lateral Movement and Privilege Escalation — stolen credentials are the
currency that turns a single foothold into movement and elevation — and it recurs whenever
a new host or identity store is reached. Its `exploit-shaped` `group_hypothesis` reflects
that dumping/cracking is an on-host action the substrate can price, though several of its
techniques (theft/forgery of tokens and tickets) are quicker, reuse-of-material acts.

The v19.1 technique surface (17 parent, 50 sub-techniques) covers dumping and
store-raiding (OS Credential Dumping T1003 — 201 procedures, Credentials from Password
Stores T1555, Unsecured Credentials T1552), capture (Input Capture T1056, Network Sniffing
T1040, Adversary-in-the-Middle T1557), guessing (Brute Force T1110), token/ticket theft
and forgery (Steal or Forge Kerberos Tickets T1558, Steal Application Access Token T1528,
Steal Web Session Cookie T1539, Forge Web Credentials T1606, Steal or Forge Authentication
Certificates T1649), and MFA-directed techniques (MFA Interception T1111, MFA Request
Generation T1621). Cross-tactic mappings tie it to Collection (Input Capture T1056,
Adversary-in-the-Middle T1557 — the same capture serves both credential theft and data
gathering), Discovery (Network Sniffing T1040), and Persistence/Defense-Impairment (Modify
Authentication Process T1556). Its 876 procedures span 215 malware and a notably high 37
tools, reflecting the Mimikatz-class utility ecosystem.

## 2. APT relevance — group-assignment argument

The literature **confirms `exploit-shaped`** while flagging that much of the tactic is
faster than an exploit. Alshamrani places credential access at the heart of the post-foothold
pivot — "most often, stolen legitimate credentials are used during this stage" — via
credential dumping with mimikatz ("the most widely used"), WCE and LSA extraction, and
Ussath's finding that "dumping credentials is the most common chosen method for lateral
movement" ([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3, §VIII)
[fetched]. Dumping and cracking are on-host actions the substrate can price as work, which
supports the `exploit-shaped` hypothesis.

But the tactic is bimodal in tempo. Dumping and brute force (OS Credential Dumping T1003,
Brute Force T1110) are effortful; token/ticket/cookie theft and forgery (Steal or Forge
Kerberos Tickets T1558, Steal Web Session Cookie T1539) are quick *reuse-of-material* acts
closer to a lookup than an exploit. The RSA SecurID intrusion shows the enabling role
concretely — after a backdoor the attackers "harvested credentials of several employees"
before escalating and exfiltrating
([`alshamrani2019`](../extractions/alshamrani2019.md) §III-D) [fetched]. The profile keeps
credential-access `exploit-shaped` / Tier 1 (the dumping path is the substrate-priceable
one), noting the theft-of-material variants run faster. Its load-bearing property — that a
stolen credential is not location-bound and so *survives* an IP/topology shuffle — is a §3
(MTD-reset) matter, deferred there. No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0006 page | OS Credential Dumping T1003 (201 procedures); Mimikatz-class tool ecosystem; **no timing** | On-host credential theft; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3, §VIII, §III-D | "Stolen legitimate credentials"; mimikatz/WCE/LSA; "dumping most common for lateral movement"; RSA harvest-then-escalate | Dumping → substrate-priceable (Tier 1); theft-of-material variants faster — no number | [fetched] |
| [`brown2023`](../extractions/brown2023.md) §IV | Substrate's attack procedure includes a credential-stuffing/reuse step from previously compromised hosts | The enabling role credential-access plays in the substrate loop | [fetched] |
| [`breach_reports_macro_timing`](../extractions/breach_reports_macro_timing.md) (Sophos AAR; DFIR) | Initial access → **Active Directory compromise: median ~3–16 h** across Sophos 2023–2026 editions (3.4 h in 2026, "sped up 70% YoY"; 11 h in 2025); DFIR fast case ran **Mimikatz +20 min after initial access** | Tier-2 macro anchor for how fast credential-access + the race-to-AD lands post-entry — whole-transition and per-case, not a per-tactic rate | [fetched] |
| [`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4 (Credential Access; T1550) | Mimikatz/OS dumping "used by attackers who have already gained access … with elevated privileges" (sequenced after PE); alternate auth material (Pass-the-Hash/Ticket, session cookies) authenticates "even if they don't know your password" | Behavioural evidence that stolen credentials *and* auth material are the archetypal **reset-survivor** (survive an IP/topology or password shuffle); no per-tactic number | [fetched] |
| [`password_rotation_efficacy`](../extractions/password_rotation_efficacy.md) (Zhang-Monrose-Reiter 2010; Chiasson 2015) | A captured password survives rotation: **41% of accounts broken offline, 17% online (<5 guesses)** from the old password (7,700 accounts); expiration benefit "partial and minor"; once used for persistence, rotation is moot | The direct empirical §3 reset-verdict: a credential-rotation reset is *leaky* → credential-access is a strong **reset-survivor** (narrow sweep on the reset) (**→§3**) | [fetched] |
| [`credential_use_timing`](../extractions/credential_use_timing.md) (Bursztein 2014; Unit42 2021; Sophos 2019; Oest 2020) | Stolen credential used fast — **20% of accounts accessed within 30 min**, ~3 min profiling; exposed services compromised in **seconds–24 h** (Postgres 96% in 30 s; first attack in 52 s); phishing lifecycle 21 h | Empirical fast-tempo for the theft-of-material/brute-force variants — "faster than an exploit"; opportunistic time-to-use, not an APT internal dwell | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn exploit-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
