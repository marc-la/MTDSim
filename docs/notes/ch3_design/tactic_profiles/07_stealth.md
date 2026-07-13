---
tactic: stealth
attack_id: TA0005
attack_url: https://attack.mitre.org/tactics/TA0005/
attack_version: 19.1
status: reconciled
group_hypothesis: stealth-low-and-slow
tier_hypothesis: 3 declared
---

# Stealth — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> Catalogue (the §5 distillation): [`../../data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json).
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

Stealth is the **anchor of the `stealth-low-and-slow` group** — the tactic from which the
group takes its name and its character. Alshamrani's entire framing of the APT rests on it:
the "low and slow approach to increase the rate of their success", attackers who "keep low
to go undetected", sustained across months
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-A, §II-C) [fetched]. cho2020 states
the same property formally in its advanced-attacker model — stealthy attackers "do not
exhibit an identifiable attacking behavior all the time … they stay stealthy until the time
comes" ([`cho2020`](../extractions/cho2020.md) §V-A) [fetched]. Concealment is less an action
with a duration than a *tempo* imposed on every other action: obfuscation, masquerading and
in-memory loading exist to stretch the campaign clock without raising alarms. (Per the v19.1
split, this paper's abundant "defense-evasion" evidence is hiding/evasion and allocates
here, not to [[08_defense-impairment]].)

Two consequences for the group. First, stealth confirms `stealth-low-and-slow` by definition
— it is the reference tactic the group anchor multiplier is calibrated to. Second, because
stealth contributes a *pace* rather than a discrete dwell, its modelled duration represents
the low-and-slow spacing it imposes, and the operational-validation caveat bites hardest
here: a synthetic substrate "omits the realistic noise … APT attackers consider to stay
undetected and move low and slow" ([`alshamrani2019`](../extractions/alshamrani2019.md) §V)
[fetched], so stealth's absolute dwell is the least directly observable of all and leans
hardest on the shape-not-scale, sweep-it discipline. No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

Stealth produces a **concealment state** — a knowledge/behavioural gain (detector-free paths,
a blending baseline) rather than a position or a possession. Its reset verdict is dominated by
the single largest **not-captured** in the set: detection is culled from the substrate, where
"caught" means *MTD invalidated progress*, never *an IDS saw you*
([substrate primer](../specs/substrate_primer.md) §(f)). Because there is no detector to hide
from, stealth's gain has **no direct substrate representation** — it is modelled not as a state
but as the low-and-slow *spacing* it imposes on every other action (§2). This is the honest
frame: a stealth tactic gets a *time*, not a detection model.

Where the literature does ground an MTD effect, it is a **partial re-planning reset**: a
detector reshuffle forces a stealthy botnet to re-plan detector-free paths, with MTTC that
**rises with shuffle frequency and falls with attacker skill**
([`mtd_stealth_effectiveness`](../extractions/mtd_stealth_effectiveness.md)), and FlipIt frames
stealthy control as contested by the defender's move-rate. So a shuffle imposes re-work on the
concealment gain rather than invalidating a map or a key. **Reset verdict: partial (re-planning
penalty); sweep width wide** — stealth's absolute dwell is the least observable of all
(Alshamrani §V: synthetic models omit "the realistic noise … [attackers use] to stay
undetected"), so it leans hardest on the shape-not-scale, sweep-it discipline, and its reset
magnitude sweeps on shuffle-rate ÷ attacker-skill.

What is **not captured**, restated for this tactic: detection semantics entirely, and therefore
any *direct* MTD-vs-stealth interaction — the modelled reset is a proxy (spacing re-work), not
the detector-evasion contest the literature describes. Because the gain rides an owned foothold,
whatever concealment state the attacker holds *survives* a network shuffle in the substrate's own
terms; the interesting MTD effect lives in the detection regime the substrate does not model,
which is the boundary the methodology chapter must state openly (P3).

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0005 page | 30 parent techniques (most of any tactic), 3,488 procedures; Obfuscated Files T1027 dominant; **no timing** | Concealment layered on other actions; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-A, §II-C, §IV-A | "Low and slow"; "keep low to go undetected"; evasion set (rootkit, obfuscation, steganography, in-memory, fake certs) | The reference low-and-slow behaviour, the group's namesake; pre-split evasion evidence allocates here — no per-tactic number | [fetched] |
| [`cho2020`](../extractions/cho2020.md) §V-A | Stealthy attackers "stay stealthy until the time comes" | Formal dwell assumption for the group anchor; no per-tactic value | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §V | Synthetic models omit "the realistic noise … [attackers use] to stay undetected and move low and slow" | Methodological caveat: stealth's absolute dwell is least observable → widest reliance on sweep | [fetched] |
| [`selmanaj2024`](../extractions/selmanaj2024.md) Ch. 4 (Defense Evasion) & Ch. 2 | Pre-v19.1 defense-evasion "42 techniques"; the *hiding* half (obfuscation, masquerading; Duqu token-theft) allocates here; APTs use hiding to "lengthen both MTTD and MTTR" (i.e. extend dwell) | Emulation-textbook allocation of the old evasion umbrella's hiding scope to `stealth`, and explicit dwell-extension vocabulary; behaviour only, no per-tactic number | [fetched] |
| [`ling2023`](../extractions/ling2023.md) Appendix A (Evasion) | Evasion is *partially* CVE-priceable (4/6 techniques categorise: Masquerading → Control of Filename/Path, Rootkit → Command Injection, etc.); Indicator Removal "is not a type of vulnerability" | Even the empirical method gives hiding only a partial shape and no dwell — structural support for Tier-3 declared + widest sweep | [fetched] |
| [`mtd_stealth_effectiveness`](../extractions/mtd_stealth_effectiveness.md) (Venkatesan 2016; Sharma 2025) + [`persistence_reset_models`](../extractions/persistence_reset_models.md) (FlipIt) | Detector reshuffle forces a stealthy botnet to re-plan detector-free paths; MTTC **rises with shuffle frequency, falls with attacker skill**; FlipIt: stealthy control is contested by the defender's move-rate | §3 MTD-effect for the group's namesake tactic: a shuffle imposes re-work on the concealment gain — a partial reset whose magnitude sweeps on shuffle-rate ÷ skill (**→§3**) | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** stealth-low-and-slow — **confirmed; this is the group's namesake and reference tactic.** The multiplier the group anchor is calibrated to is defined here.
- **Relative multiplier:** ×1.0 of the stealth anchor — by definition the reference (×1.0); stealth *is* the low-and-slow pace the group expresses.
- **Sweep range:** ×0.25–×4 (wide) — stealth's absolute dwell is the least directly observable of all tactics, so it leans hardest on the shape-not-scale, sweep-it discipline.
- **Tier:** 3 — declared; no substrate verb prices a "hiding" pace, and detection (the thing stealth acts against) is culled from the substrate.
- **Justification (one paragraph):** Stealth is the reference against which the whole low-and-slow group is anchored, so it takes ×1.0 by construction; §2 makes it the namesake (Alshamrani's "low and slow"; cho2020's "stay stealthy until the time comes"), a *pace* imposed on every other action rather than a discrete dwell. Its modelled duration therefore represents that spacing, and the operational-validation caveat bites hardest here — a synthetic substrate "omits the realistic noise … [attackers use] to stay undetected", so the absolute value is the least observable in the set and the wide sweep is mandatory, not optional. §3 records the dominant not-captured: detection is culled ("caught" = MTD invalidated progress, never an IDS saw you), so stealth has **no direct substrate representation** and its concealment gain rides an owned foothold that *survives* a shuffle in the substrate's own terms; the interesting MTD-vs-stealth contest (a re-planning penalty scaling with shuffle-rate ÷ attacker-skill) lives in the detection regime the substrate does not model — the boundary the methodology chapter must state openly (P3). A Tier-3 declared value, swept wide, calibrated as the group anchor when the runner lands.
