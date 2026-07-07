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

Lateral movement is the **showcase for the per-modality reset split** — the crown-jewel finding
inside a single tactic. What a hop produces depends on *how* it moves. A **scan-based hop**
(Exploitation of Remote Services T1210, or worm-style target-discovery) produces a
position/knowledge gain — a target map — and is reset-*vulnerable*: a position-mutating
address/topology shuffle invalidates it, and the empirics are stark, with a mutated address
space leaving a scanner **<1% valid addresses** and worm containment capping total reach
([`worm_propagation_models`](../extractions/worm_propagation_models.md)). A **credential-based
hop** (Use Alternate Authentication Material T1550 — pass-the-hash/ticket, valid accounts) rides
a survivor capability: the credential authenticates against whichever host now answers, so the
*same shuffle that kills the scan-worm leaves the credential-move untouched*
([substrate primer](../specs/substrate_primer.md) §(e)).

The MTD action that bites, therefore, is the position-mutating family — and it bites *one
modality and not the other*. This forces a **bimodal sweep**: the profile carries a wide,
ratio-governed band for the scan modality (magnitude on mutation-rate ÷ scan-rate) and a
near-zero survivor band for the credential modality — and *which dominates is
objective-conditioned* (rubric crit. 7). A credential-first campaign is effectively reset-immune
in this tactic; a scan/exploit-first one is highly disruptable. That is the discrimination the
whole thesis turns on: an MTD that wins against the substrate's scan-based baseline hop may lose
against a credential-driven low-and-slow profile that never exposes the modality the shuffle can
reset ([substrate primer](../specs/substrate_primer.md) §(d)).

What is **not captured**: the substrate prices remote-service exploitation by CVSS but does not,
today, distinguish the two hops' reset behaviour beyond the position-vs-capability split it
already implements; nor does it model an attacker that *recognises* a post-shuffle state
collision and re-routes (adaptivity, deferred — [substrate primer](../specs/substrate_primer.md)
§(f)). **Reset verdict: per-modality — the scan hop is invalidated (wide sweep), the credential
hop survives (narrow sweep).**

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

> **§4 note — operational-validation outer envelope.** The whole-chain macro-milestone rows
> above (breakout, access→AD, access→exfil, campaign dwell, time-to-ransomware) are an
> *operational-validation outer envelope*, not per-tactic timing or reset targets: each is
> defined by *when detection caught the intrusion*, and detection/IDS is culled from this
> substrate ([substrate primer](../specs/substrate_primer.md) §(f)), so they bound the emergent
> timeline's *shape/plausibility*, never an absolute per-tactic dwell. Only the rows that resolve
> dwell-character or reset-verdict feed §3/§5.

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** exploit-shaped — **confirmed** (dominant form is a remote-service login/exploit the substrate prices), but with a character spanning fast-worm to slow-manual that argues a **wider sweep** than the other exploit tactics.
- **Relative multiplier:** ×1.0 of the exploit anchor (`exploit_time`) — one remote-service hop, **not tuned**.
- **Sweep range:** ×0.25–×4 (wide) — the fast-worm (Slammer 90% in 10 min) ↔ slow-manual-pivot span, and the **per-modality reset split**, both widen it.
- **Tier:** 1 — substrate-anchored (`exploit_time`); not tuned.
- **Justification (one paragraph):** Lateral-movement is the **showcase for the per-modality reset split** — the crown-jewel finding *inside a single tactic* — and that is what its §5 must carry. §2 keeps it exploit-shaped for duration (Remote Services T1021 / Exploitation of Remote Services T1210 are substrate-priced, ×1.0, Tier-1, not tuned) but flags a character wide enough (patient manual pivot ↔ automatic worm sweep) to justify the wide sweep. §3 is the load-bearing half: a **scan-based hop** produces a target map and is reset-*vulnerable* (a mutated address space leaves a scanner <1% valid addresses), while a **credential-based hop** rides a survivor capability and the *same shuffle leaves it untouched* — so the tactic is genuinely bimodal, and *which modality dominates is objective-conditioned* (crit. 7). This is the discrimination the whole thesis turns on: an MTD that beats the substrate's scan-based baseline hop may lose against a credential-driven low-and-slow profile that never exposes the resettable modality. The duration multiplier is substrate-fixed; the bimodal reset (wide band for the scan hop, near-zero for the credential hop) feeds the L3b binding.
