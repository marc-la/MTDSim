---
tactic: stealth
attack_id: TA0005
attack_url: https://attack.mitre.org/tactics/TA0005/
attack_version: 19.1
status: stub
group_hypothesis: stealth-low-and-slow
tier_hypothesis: 3 declared
---

# Stealth — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

> **v19.1 note:** `stealth` reuses id TA0005 but is the *hiding/evasion* half of
> the old `defense-evasion`; the *disabling-defences* half went to
> `defense-impairment` (TA0112). Pre-split literature saying "defense-evasion"
> must be allocated between the two — capture only the hiding/evasion portion here.

## 1. Tactic & role

Stealth is defined in the pinned v19.1 bundle as the phase where "the adversary is trying
to hide and conceal their actions, appearing as normal behavior": reducing detection
likelihood by blending with legitimate activity or minimising observable signals through
concealment behaviours — avoiding, obfuscating, or mimicking normal operations —
explicitly "without modifying security controls or compromising collection and monitoring
feeds", so that the adversary stays indistinguishable from benign activity "while leaving
defensive systems intact" ([TA0005](https://attack.mitre.org/tactics/TA0005/)).

**The v19.1 split.** ATT&CK v19 (released 28 April 2026) split the former Defense Evasion
tactic into two — Stealth (TA0005, reusing the old id) and Defense Impairment (TA0112,
new) — described by MITRE as "the biggest change in ATT&CK v19"
([release notes](https://attack.mitre.org/resources/updates/updates-april-2026/)). The
division is by **adversary intent**: Stealth is behavioural camouflage, where the
defences are intact and simply not seeing the threat, whereas its sibling covers active
interference that breaks or degrades those defences
([ATT&CK blog](https://medium.com/mitre-attack/att-ck-v19-the-defense-evasion-split-ics-sub-techniques-new-ai-social-engineering-coverage-ff329cb65d66)).
Stealth inherited the **concealment** half: obfuscation and encoding (Obfuscated Files or
Information T1027 — 811 procedures, the tactic's dominant technique; Deobfuscate/Decode
T1140), masquerading and artefact-hiding (Masquerading T1036, Hide Artifacts T1564,
Indicator Removal T1070), living-off-the-land/proxy execution (System Binary Proxy
Execution T1218, System Script Proxy Execution T1216, Trusted Developer Utilities T1127),
rootkits and memory-only loading (Rootkit T1014, Reflective Code Loading T1620, Process
Injection T1055), and analysis-evasion (Virtualization/Sandbox Evasion T1497, Debugger
Evasion T1622, Execution Guardrails T1480, Delay Execution T1678). Note Indicator Removal
sits here, not in Defense Impairment: the v19.1 definition scopes it as blending in by
removing one's *own* anomalous artefacts while "leaving sufficient data intact" —
concealment, not tearing down the logging pipeline.

Positionally it is the seventh tactic and, like Execution, a **cross-cutting** tactic
applied continuously rather than a single stage. Its 30 parent techniques are the most of
any tactic and its 3,488 procedure examples the largest count in this study (598 malware
families). Several techniques are multi-tactic (Valid Accounts T1078, Process Injection
T1055, Hijack Execution Flow T1574, BITS Jobs T1197), reflecting that concealment is
layered onto other actions rather than performed in isolation.

## 2. APT relevance — group-assignment argument

<!-- Low-and-slow or fast? Argue the group. Hypothesis to confirm/overturn: stealth-low-and-slow. No point number. -->

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0005 page | <definition / techniques; timing?> | — | [fetched] |
| <in-corpus extraction> | <> | <> | [fetched] |
| <external, if any> | <> | <> | [search] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn stealth-low-and-slow>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 3 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
