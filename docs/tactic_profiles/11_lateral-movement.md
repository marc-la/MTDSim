---
tactic: lateral-movement
attack_id: TA0008
attack_url: https://attack.mitre.org/tactics/TA0008/
attack_version: 19.1
status: stub
group_hypothesis: exploit-shaped
tier_hypothesis: 1 substrate
---

# Lateral Movement — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Lateral Movement is defined in the pinned v19.1 bundle as the phase where "the adversary
is trying to move through your environment": entering and controlling remote systems,
typically pivoting through multiple systems and accounts to reach the target, either with
installed remote-access tools or — stealthier — with legitimate credentials and native
network/OS tools ([TA0008](https://attack.mitre.org/tactics/TA0008/)).

Positionally it is the eleventh tactic; the tactic that **expands a single foothold into
estate-wide reach**, tightly coupled to Credential Access (which supplies the material)
and Discovery (which supplies the map), and recurring per hop. Its `exploit-shaped`
`group_hypothesis` reflects that its dominant form is a remote-service login/exploitation
the substrate can price — though the bundle stresses the credential-reuse path is often
chosen precisely because it is quieter than exploitation.

The v19.1 technique surface is comparatively compact (9 parent, 14 sub-techniques). It is
dominated by Remote Services T1021 (190 procedures — RDP/SSH/SMB/VNC/WinRM logons),
followed by alternate-authentication movement (Use Alternate Authentication Material T1550
— pass-the-hash/ticket/token), tool and payload propagation (Lateral Tool Transfer T1570,
Taint Shared Content T1080, Software Deployment Tools T1072), session hijacking (Remote
Service Session Hijacking T1563), removable-media and internal-phishing vectors
(Replication Through Removable Media T1091, Internal Spearphishing T1534), and
remote-service exploitation (Exploitation of Remote Services T1210). Its multi-tactic ties
reflect this dependence on other stages — T1091 is shared with Initial Access, T1072 with
Execution. With 367 procedures across 76 groups it is a smaller, more deliberate technique
set than the enabling tactics (Execution, Stealth, Discovery).

## 2. APT relevance — group-assignment argument

The literature **confirms `exploit-shaped`** but reveals a dwell character spanning fast-worm
to slow-manual. The credential-reuse path Alshamrani foregrounds — pass-the-hash, valid
credentials, "spread over to other systems … access other hosts from a compromised system"
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3) [fetched] — is
deliberate and human-paced, and often chosen (per §1) precisely because it is quieter than
exploitation. At the other extreme, Stuxnet moved *automatically*, worm-style: LNK files via
shared drives, the print-spooler flaw via shared printers, and a hard-coded Siemens Step7
password to reach database servers
([`alshamrani2019`](../extractions/alshamrani2019.md) §III-C) [fetched] — self-propagating
lateral movement at machine speed.

That span is the finding for the group. Lateral movement's dominant form (Remote Services
T1021 logins, Exploitation of Remote Services T1210) is a remote-service login/exploit the
substrate prices, so the tactic sits `exploit-shaped` / Tier 1. But its character is wide — a
patient manual pivot or an automatic worm sweep — which argues for a **wider sweep** than the
other exploit-shaped tactics. Johnson & Hogan model the movement as graph reachability ("how
likely a node is to be reached from another arbitrary node",
[`alshamrani2019`](../extractions/alshamrani2019.md) §IV-C-1) [fetched], the property a
topology shuffle attacks (a §3 matter). No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0008 page | Compact (9 parents); Remote Services T1021 dominant (190 procedures); **no timing** | Pivot per hop; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3, §III-C | Credential-reuse pivot (PtH/valid creds, quieter) vs Stuxnet worm-style auto-propagation (LNK/print-spooler/Step7 pw) | Character spans slow-manual..fast-worm → wider sweep; exploit form → substrate (Tier 1) | [fetched] |
| [`brown2023`](../extractions/brown2023.md) §IV | Substrate prices remote-service exploitation by CVSS complexity; a path shuffle forces re-discovery of reachable hosts | Tier-1 anchor + reset semantics (→§3) | [fetched] |
| [`rodriguez2024`](../extractions/rodriguez2024.md) §3 | Tactic-level ATT&CK Petri nets are **untimed** | Gap-confirming: no per-tactic rate | [fetched] |
| [`breach_reports_macro_timing`](../extractions/breach_reports_macro_timing.md) (CrowdStrike GTR; DFIR) | **Breakout time** *is* initial-access → lateral-movement: avg **29 min** / fastest **27 s** (2026), 48 min / 51 s (2025); DFIR lateral movement at **+10 min to +2 h** post-access | The one macro statistic anchored *to this exact transition*; bounds the fast (eCrime) end of the lateral hop — whole-transition, not a per-tactic dwell | [fetched] |
| [`ling2023`](../extractions/ling2023.md) §Results, Table 7 | Lateral-movement techniques (Exploitation of Remote Services, Lateral Tool Transfer) → *Access Control*; Lateral Tool Transfer TTC = 3594/98/15/**6** d (novice→expert) | Per-technique empirical shape + expert 6-day floor for the exploit-move variant; the credential-/auth-material-move variant has no CVE (reset-survives) | [fetched] |
| [`worm_propagation_models`](../extractions/worm_propagation_models.md) (Slammer; Staniford; Code Red/Zou; Mirai; Chernikova) | Automated scan-based spread is **seconds–minutes**: Slammer **90% in 10 min**, Code Red **37-min doubling**, Warhol "minutes–hour", flash "10s of seconds", Mirai 65k in 20 h | The **fast-worm pole** of the fast↔slow bimodal range — the modality the substrate's fast lateral-exploit proxies; contrasts the slow-manual APT pole | [fetched] |
| [`worm_propagation_models`](../extractions/worm_propagation_models.md) (Al-Shaer/Jafarian OpenFlow-RHM; Sellke; Ma) + [`breach_reports_macro_timing`](../extractions/breach_reports_macro_timing.md) (ReliaQuest 2026) | Address mutation → scanner finds **<1% valid addresses** (worm target-discovery invalidated); worm containment caps total scans; ReliaQuest breakout avg **34 min**/fastest **4 min**, exfil **6 min** | §3 reset for the *scan-based* move (mutation kills it; credential-move survives — per-modality); independent breakout corroboration (**→§3**) | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn exploit-shaped>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 1 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
