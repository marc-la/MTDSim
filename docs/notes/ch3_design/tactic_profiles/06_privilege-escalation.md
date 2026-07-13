---
tactic: privilege-escalation
attack_id: TA0004
attack_url: https://attack.mitre.org/tactics/TA0004/
attack_version: 19.1
status: reconciled
group_hypothesis: exploit-shaped
tier_hypothesis: 1 substrate
---

# Privilege Escalation — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> Catalogue (the §5 distillation): [`../../data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Privilege Escalation is defined in the pinned v19.1 bundle as the phase where "the
adversary is trying to gain higher-level permissions": gaining elevated access —
SYSTEM/root, local administrator, or a specifically-privileged account — typically by
taking advantage of system weaknesses, misconfigurations, and vulnerabilities
([TA0004](https://attack.mitre.org/tactics/TA0004/)). The bundle explicitly flags that
these techniques "often overlap with Persistence techniques", since persistence
mechanisms frequently execute in an elevated context.

Positionally it is the sixth tactic, but in practice it is **interleaved** with the early
post-compromise loop (execute → persist → escalate → discover) rather than a discrete
stage: the bundle notes an adversary "can often enter and explore a network with
unprivileged access but require elevated permissions to follow through on their
objectives", i.e. escalation happens on demand when an objective needs it. Its
`exploit-shaped` `group_hypothesis` reflects that its purest form (T1068) is a
substrate-priced exploit action.

The v19.1 technique surface (13 parent, 83 sub-techniques) splits into direct
exploitation (Exploitation for Privilege Escalation T1068, Escape to Host T1611),
token/mechanism abuse (Access Token Manipulation T1134, Abuse Elevation Control
Mechanism T1548), and a large block shared with Persistence — 7 of the 13 parents (Boot
or Logon Autostart Execution T1547, Scheduled Task/Job T1053, Create or Modify System
Process T1543, Event Triggered Execution T1546, Account Manipulation T1098, Boot or Logon
Initialization Scripts T1037, plus Valid Accounts T1078). Process Injection T1055 is
shared with Stealth (injecting into a live process both evades defences and can elevate),
and Domain or Tenant Policy Modification T1484 with Defense Impairment. With 1,471
procedure examples across 453 malware families, the heavy overlap set makes
privilege-escalation less a standalone stage than a property acquired through techniques
that also serve persistence and evasion.

## 2. APT relevance — group-assignment argument

The literature **confirms `exploit-shaped`** for the tactic's purest form while noting a
fast, non-exploit path. Alshamrani places privilege escalation inside the interleaved
post-foothold loop — "sometimes this phase involves privilege escalation … the chosen method
depends on the environment of the target system" — and its canonical instance is
vulnerability exploitation: Stuxnet used two Windows zero-days (a keyboard-file flaw and Task
Scheduler) to "gain full control of the machine by performing privilege escalation"
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3, §III-C) [fetched]. That
direct-exploitation form (Exploitation for Privilege Escalation T1068) is exactly what the
substrate's complexity-scaled `exploit_time` prices, so the tactic inherits a Tier-1 anchor
and is *not tuned*.

The caveat, from §1's overlap analysis, is that seven of the thirteen parents are shared
with Persistence and the token/valid-account variants (Access Token Manipulation T1134,
Valid Accounts T1078) are quick *reuse-of-material* acts rather than exploits — closer in
tempo to credential-access than to an exploit. Privilege-escalation's character is therefore
bimodal: an exploit (substrate-priced) or a fast token abuse. The profile keeps it
`exploit-shaped` / Tier 1 — the substrate models the exploit path — while noting the
token-abuse variant runs faster than the anchor implies. No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

Privilege escalation produces an **elevated-permission state** — a *gating capability* that
unlocks an admin-only technique subset (xiong2021: a `userRights` adversary "cannot use a
technique that requires Administrator" until it can "level up … to gain adminRights"). Read
against the reset model it is bimodal, like its sibling exploit-shaped tactics
([[03_initial-access]], [[11_lateral-movement]]). The **token/valid-account path** (Access Token Manipulation T1134, Valid Accounts
T1078) is a capability possession that **survives** a network shuffle — an elevated token is not
location-bound, patterning with [[09_credential-access]]. The **exploit path** (Exploitation for
Privilege Escalation T1068) is a surface-dependent attempt whose working set a surface-mutating
diversity shuffle can reset mid-exploit, patterning with [[03_initial-access]].

The MTD action that bites is application-layer diversity on the exploit path (not the token
path), and its effect is bounded by the observation that **MTD-defeat probability rises with
attacker time/cost** (Maleki — [`mttc_lineage`](../extractions/mttc_lineage.md)): a faster reset
caps escalation success by denying the exploit time to complete. Deception/structure *delays* the
privilege-escalation→domain-admin race but does not *reset* an already-held elevation
([`ad_time_to_domain_admin`](../extractions/ad_time_to_domain_admin.md)). **Reset verdict:
bimodal — the token/valid-account variant survives (narrow sweep), the exploit variant is
disruptable by surface diversity (moderate sweep); overall sweep moderate.**

What is **not captured**: the substrate prices the exploit but does not model the *gating state*
itself distinctly — the xiong-style "elevation unlocks a technique subset" semantics are an
attacker-side addition the L3b binding carries, not a substrate primitive. So privilege
escalation's reset in the substrate is really the reset of its underlying exploit or credential
action; its distinctive contribution (the permission gate) is a modelled precondition, not a
resettable gain.

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0004 page | T1068 exploit + token/mechanism abuse; 7/13 parents shared with Persistence; **no timing** | On-demand elevation; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 3, §III-C | Escalation on demand; Stuxnet 2 Windows 0-days → "full control"; method depends on environment | Exploit form → substrate `exploit_time` (Tier 1); token-abuse variant is faster — no number | [fetched] |
| [`brown2023`](../extractions/brown2023.md) §IV | Substrate prices exploitation by CVSS attack-complexity ∈ [0.4, 1] | The Tier-1 anchor privilege-escalation inherits | [fetched] |
| [`rodriguez2024`](../extractions/rodriguez2024.md) §3 | Tactic-level ATT&CK Petri nets are **untimed** — timestamps only *order* events | Gap-confirming: no per-tactic rate even in a tactic-level model | [fetched] |
| [`xiong2021`](../extractions/xiong2021.md) §5.1.2 | enterpriseLang models PE as a hard permission gate: a `userRights` adversary "cannot use a technique that requires Administrator"; "an adversary can level up through Privilege Escalation … to gain adminRights" | Formal-model precedent for PE as a *gating state* that unlocks an admin-only technique subset — PE dwell is spent before those become reachable; structural, no timing | [fetched] |
| [`ling2023`](../extractions/ling2023.md) Appendix A, Table 7 | PE (Exploitation for Privilege Escalation) → *Authentication* vuln category; expert TTC floor **6 days** | Per-technique empirical shape for exploit-priced escalation; expert floor supports the exploit-shaped group anchor | [fetched] |
| [`mcqueen2006`](../extractions/mcqueen2006.md) §3.1.2 | Easy-exploit compromise mean **1 day**; the no-easy-exploit declared dwell **21 d (expert)** | MTTC-lineage declared value for the exploit-shaped case; a Tier-2 plausibility envelope for escalation dwell | [fetched] |
| [`mttc_lineage`](../extractions/mttc_lineage.md) (Leversage 2008; Zieger 2018; Maleki 2016) | Leversage **Process-1 (known vuln + exploit) mean = 1 day**, skill-scaled (indicator 0–1); Zieger β-TTC folds in CVSS + β-skill; Maleki: MTD-defeat probability *rises with attacker time/cost* | Independent corroboration of the 1-day easy-exploit dwell + a skill range around it; Maleki gives the §3 MTD-effect (faster reset caps success) (**→§3**) | [fetched] |
| [`ad_time_to_domain_admin`](../extractions/ad_time_to_domain_admin.md) (Ngo 2024; Herranz 2023; Munaiah 2019) | Ngo "response time" = first-decoy-trigger→**DA compromise**; Herranz AD lateral = SIR infection, immunization slows spread; Munaiah CPTC'18 = ATT&CK-timed campaign (44 events) | Structures the privesc→DA race: deception/structure *delay* it (not reset); Munaiah confirms even a timestamped ATT&CK campaign gives ordering, not per-tactic dwell (gap) | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** exploit-shaped — **confirmed for the purest form** (T1068, a substrate-priced exploit); the token/valid-account variant is a faster reuse-of-material act, noted as a within-group skew.
- **Relative multiplier:** ×1.0 of the exploit anchor (`exploit_time`, complexity-scaled) — the direct-exploitation path, **not tuned**; the token path runs below the anchor.
- **Sweep range:** ×0.5–×2 (moderate) — bimodal character (slow exploit ↔ fast token abuse) widens it beyond the clean exploit tactics but not to the low-and-slow bands.
- **Tier:** 1 — substrate-anchored (`exploit_time`); not tuned.
- **Justification (one paragraph):** Privilege-escalation's canonical instance is vulnerability exploitation (§2: Stuxnet's two Windows zero-days → "full control"), which the substrate prices directly via `exploit_time`, so it inherits a Tier-1 not-tuned anchor (×1.0). Its distinctive contribution is a **gating capability** (xiong2021: a `userRights` adversary cannot use an admin-only technique until it levels up), but that gate is modelled as an L3b precondition, not a resettable substrate gain — so §3's reset is really the reset of the *underlying* action, and it is bimodal: the token/valid-account variant survives a shuffle (patterning with [[09_credential-access]]), the exploit variant is disruptable by surface diversity mid-attempt (patterning with [[03_initial-access]]), bounded by Maleki's "MTD-defeat probability rises with attacker time/cost". The moderate sweep spans that bimodality; the reset verdict (bimodal, feeding the binding) is separate from the substrate-fixed duration. Tier 1 because the priced path is a substrate exploit, with the faster token path recorded as the within-group skew rather than a separate anchor.
