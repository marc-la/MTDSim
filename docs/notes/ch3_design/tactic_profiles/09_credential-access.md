---
tactic: credential-access
attack_id: TA0006
attack_url: https://attack.mitre.org/tactics/TA0006/
attack_version: 19.1
status: reconciled
group_hypothesis: exploit-shaped
tier_hypothesis: 1 substrate
---

# Credential Access — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../operational_validation.md).
> Catalogue (the §5 distillation): [`../../data/ogasp/tactic_durations.json`](../../../../data/ogasp/tactic_durations.json).
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
movement" ([`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C Stage 3, §VIII)
[fetched]. Dumping and cracking are on-host actions the substrate can price as work, which
supports the `exploit-shaped` hypothesis.

But the tactic is bimodal in tempo. Dumping and brute force (OS Credential Dumping T1003,
Brute Force T1110) are effortful; token/ticket/cookie theft and forgery (Steal or Forge
Kerberos Tickets T1558, Steal Web Session Cookie T1539) are quick *reuse-of-material* acts
closer to a lookup than an exploit. The RSA SecurID intrusion shows the enabling role
concretely — after a backdoor the attackers "harvested credentials of several employees"
before escalating and exfiltrating
([`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §III-D) [fetched]. The profile keeps
credential-access `exploit-shaped` / Tier 1 (the dumping path is the substrate-priceable
one), noting the theft-of-material variants run faster. Its load-bearing property — that a
stolen credential is not location-bound and so *survives* an IP/topology shuffle — is a §3
(MTD-reset) matter, deferred there. No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

Credential access produces the archetypal **capability/conquest gain**: a harvested
credential is a *standing possession*, not a position on the map
([substrate primer](../../../implementation/substrate_primer.md) §(d)/§(e)). Read against the substrate's
reset model, it is the **clearest reset-*survivor*** in the set, and it sits on the survivor
pole of the survivor-vs-vulnerable axis, exactly opposite [[01_reconnaissance]] and
[[10_discovery]]. A position-mutating (network-layer) IP/topology shuffle relocates hosts and
erases the attacker's map, but a stolen credential is not location-bound — it authenticates
against whichever host now answers, so the shuffle leaves it wholly intact. A surface-mutating
(application-layer) diversity shuffle rewrites service/OS versions but not the validity of a
captured secret. This per-modality reset is the strongest, most falsifiable claim the profile
owns: the *same* shuffle that resets a scanning tactic does nothing to a credential.

The only MTD family that bites is **credential-mutating** rotation/re-sampling — which the
substrate holds in reserve rather than in the default Shuffle/Diversity roster
([substrate primer](../../../implementation/substrate_primer.md) §(c)) — and even that is *leaky*: the
replacement credential is derivable from the captured one for 41% of accounts under offline
attack / 17% online, i.e. rotation *fails to revoke* in that fraction of cases
([`password_rotation_efficacy`](../../../sources/extractions/password_rotation_efficacy.md)), and
account-manipulation persistence adapts around a periodic rotation. So the one mechanism that
*could* reset the gain does so only partially. **Reset verdict: survives; sweep width narrow** —
the direction is unusually firm and the magnitude is bounded near zero (a small, leaky
credential-rotation fraction, swept tight), unlike the wide, ratio-governed bands the
position-vulnerable tactics carry.

What is **not captured**: the substrate's reset model already treats credentials as *never*
revoked by a shuffle ([substrate primer](../../../implementation/substrate_primer.md) §(e)), so the declared
leaky-rotation fraction is, if anything, more generous to the defender than the substrate
currently is — a literature-argued verdict that mildly *diverges* from the substrate's
(recorded per §(e).1); MFA, credential-store structure, and the fast token/ticket-theft
variants are not modelled distinctly (a harvested credential is simply a durable reusable key).
The discrimination payoff (rubric crit. 7) is direct: the generic six-phase attacker reuses
credentials only opportunistically, whereas a credential-first low-and-slow profile leans on
precisely the modality MTD cannot reset — the behaviour most likely to separate a genuinely
strong MTD from one that merely outpaces a sprint
([substrate primer](../../../implementation/substrate_primer.md) §(d)).

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0006 page | OS Credential Dumping T1003 (201 procedures); Mimikatz-class tool ecosystem; **no timing** | On-host credential theft; no duration to inherit | [fetched] |
| [`alshamrani2019`](../../../sources/extractions/alshamrani2019.md) §II-C Stage 3, §VIII, §III-D | "Stolen legitimate credentials"; mimikatz/WCE/LSA; "dumping most common for lateral movement"; RSA harvest-then-escalate | Dumping → substrate-priceable (Tier 1); theft-of-material variants faster — no number | [fetched] |
| [`brown2023`](../../../sources/extractions/brown2023.md) §IV | Substrate's attack procedure includes a credential-stuffing/reuse step from previously compromised hosts | The enabling role credential-access plays in the substrate loop | [fetched] |
| [`breach_reports_macro_timing`](../../../sources/extractions/breach_reports_macro_timing.md) (Sophos AAR; DFIR) | Initial access → **Active Directory compromise: median ~3–16 h** across Sophos 2023–2026 editions (3.4 h in 2026, "sped up 70% YoY"; 11 h in 2025); DFIR fast case ran **Mimikatz +20 min after initial access** | Tier-2 macro anchor for how fast credential-access + the race-to-AD lands post-entry — whole-transition and per-case, not a per-tactic rate | [fetched] |
| [`selmanaj2024`](../../../sources/extractions/selmanaj2024.md) Ch. 4 (Credential Access; T1550) | Mimikatz/OS dumping "used by attackers who have already gained access … with elevated privileges" (sequenced after PE); alternate auth material (Pass-the-Hash/Ticket, session cookies) authenticates "even if they don't know your password" | Behavioural evidence that stolen credentials *and* auth material are the archetypal **reset-survivor** (survive an IP/topology or password shuffle); no per-tactic number | [fetched] |
| [`password_rotation_efficacy`](../../../sources/extractions/password_rotation_efficacy.md) (Zhang-Monrose-Reiter 2010; Chiasson 2015) | A captured password survives rotation: **41% of accounts broken offline, 17% online (<5 guesses)** from the old password (7,700 accounts); expiration benefit "partial and minor"; once used for persistence, rotation is moot | The direct empirical §3 reset-verdict: a credential-rotation reset is *leaky* → credential-access is a strong **reset-survivor** (narrow sweep on the reset) (**→§3**) | [fetched] |
| [`credential_use_timing`](../../../sources/extractions/credential_use_timing.md) (Bursztein 2014; Unit42 2021; Sophos 2019; Oest 2020) | Stolen credential used fast — **20% of accounts accessed within 30 min**, ~3 min profiling; exposed services compromised in **seconds–24 h** (Postgres 96% in 30 s; first attack in 52 s); phishing lifecycle 21 h | Empirical fast-tempo for the theft-of-material/brute-force variants — "faster than an exploit"; opportunistic time-to-use, not an APT internal dwell | [fetched] |

> **§4 note — operational-validation outer envelope.** The whole-chain macro-milestone rows
> above (breakout, access→AD, access→exfil, campaign dwell, time-to-ransomware) are an
> *operational-validation outer envelope*, not per-tactic timing or reset targets: each is
> defined by *when detection caught the intrusion*, and detection/IDS is culled from this
> substrate ([substrate primer](../../../implementation/substrate_primer.md) §(f)), so they bound the emergent
> timeline's *shape/plausibility*, never an absolute per-tactic dwell. Only the rows that resolve
> dwell-character or reset-verdict feed §3/§5.

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** exploit-shaped — **confirmed for the dumping path** (OS Credential Dumping T1003 is substrate-priceable); token/ticket/cookie theft is a faster reuse-of-material act, noted as a within-group skew.
- **Relative multiplier:** ×1.0 of the exploit anchor (`exploit_time`) — the dumping/cracking action, **not tuned**; theft-of-material variants run below it.
- **Sweep range:** ×0.5–×2 (moderate) on the *duration*; the **reset band is narrow (≈0)** — the survivor direction is unusually firm.
- **Tier:** 1 — substrate-anchored (`exploit_time` for the dumping path); not tuned.
- **Justification (one paragraph):** Credential-access is the **survivor pole of the crown-jewel axis** and the profile's strongest genuinely-owned claim. §2 keeps it exploit-shaped for duration — dumping/cracking is on-host work the substrate can price (×1.0, Tier-1, not tuned), with fast token/ticket theft as the within-group skew. §3 is the load-bearing half: a harvested credential is a *standing possession*, not a position, so the **same shuffle that resets a scanning tactic does nothing to it** — the clearest reset-*survivor* in the set. The only family that bites is credential-rotation (held in reserve, not in the default roster) and even that is *leaky* (Zhang-Monrose-Reiter: 41% offline / 17% online broken from the old password), so the reset fraction is bounded near zero with a narrow band — unlike the wide, ratio-governed position-vulnerable tactics. The discrimination payoff (crit. 7) is direct and is why this tactic matters most: the generic sprint reuses credentials only opportunistically, whereas a credential-first low-and-slow profile leans on exactly the modality MTD cannot reset — the behaviour most likely to separate a genuinely strong MTD from one that merely outpaces a weak attacker. The duration's moderate sweep and the reset's narrow band feed different artefacts (the catalogue vs the L3b binding).
