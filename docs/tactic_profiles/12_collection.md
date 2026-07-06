---
tactic: collection
attack_id: TA0009
attack_url: https://attack.mitre.org/tactics/TA0009/
attack_version: 19.1
status: stub
group_hypothesis: objective-execution
tier_hypothesis: 2 literature
---

# Collection — APT × adversary-simulation × MTD dwell profile

> **Purpose (read once):** reconciled synthesis terminating in **(a) dwell character**
> and **(b) MTD disruption**. Trim anything that changes neither how long nor whether
> the attacker repeats it. 1–2 pages. Method:
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> How to fill: [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md).
> Template: [`_template.md`](_template.md).

## 1. Tactic & role

Collection is defined in the pinned v19.1 bundle as the phase where "the adversary is
trying to gather data of interest to their goal": gathering the information, and the
sources it comes from, that is relevant to following through on the objective — commonly
as a precursor to Exfiltration ([TA0009](https://attack.mitre.org/tactics/TA0009/)). The
bundle notes the usual next step is to steal (exfiltrate) the data or to use it to learn
more about the environment.

Positionally it is the twelfth tactic; a late-stage, **objective-adjacent** tactic that
pairs directly with Exfiltration (collect → stage → exfiltrate). It is where the campaign
begins to act on its purpose rather than merely enabling itself, which is why its
`group_hypothesis` is `objective-execution` (Tier 2 — a candidate for
literature-calibrated timing rather than a substrate constant).

The v19.1 technique surface (17 parent, 24 sub-techniques) divides into source-based
gathering (Data from Local System T1005 — 229 procedures, Data from Network Shared Drive
T1039, Data from Removable Media T1025, Data from Information Repositories T1213, Data from
Cloud Storage T1530, Data from Configuration Repository T1602), capture-based gathering
(Input Capture T1056, Screen Capture T1113, Audio/Video Capture T1123/T1125, Clipboard
Data T1115, Email Collection T1114), staging and packaging (Data Staged T1074, Archive
Collected Data T1560), and interception (Adversary-in-the-Middle T1557, Browser Session
Hijacking T1185). Its cross-tactic overlap is with Credential Access (Input Capture T1056,
Adversary-in-the-Middle T1557 — one capture serves both), reflecting that the same
instrumentation that harvests credentials also harvests data. 1,311 procedures across 347
malware families.

## 2. APT relevance — group-assignment argument

The literature **confirms `objective-execution`** — collection is where the campaign begins
to act on its purpose. Alshamrani places it in Stage 4 as the gathering that precedes theft —
"actions comprising retrieving and sending this data to the attackers' command and control
center" — and Carbanak's operators collected employee-activity recordings (video, keylogger,
form-grabber output) staged for exfiltration
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 4, §III-E) [fetched]. The
RSA intrusion shows the same collect-then-package pattern — data "compressed and encrypted …
before sending" ([`alshamrani2019`](../extractions/alshamrani2019.md) §III-D) [fetched]. This
is objective-adjacent work rather than campaign enablement, which places it with exfiltration
and impact in the tuned objective-execution group rather than with the substrate-priced
enabling tactics.

Its dwell character has two ends. A targeted grab of a known repository is quick; the
"position for future" objective ([[10_discovery]]) turns collection into indefinite passive
harvesting — "gaining as much information as they can while staying unnoticed"
([`alshamrani2019`](../extractions/alshamrani2019.md) §II-C) [fetched]. The profile confirms
`objective-execution` / Tier 2 — the breach literature characterises the collect→exfil chain
even without a per-tactic dwell — noting collection runs from a fast grab to a slow harvest.
No point number (§5).

## 3. MTD interaction — reasoned from mechanism (declared)

<!-- Which MTD action (shuffle / diversity / redundancy) disrupts this tactic?
     Reset verdict (does a shuffle invalidate a gain here or survive it?) + the sweep-width it justifies. -->

## 4. Timing evidence

| Source | Claim (value / behaviour) | How adapted | Confidence |
|---|---|---|---|
| ATT&CK TA0009 page | Data from Local System T1005 (229 procedures); staging/archive techniques; **no timing** | Precursor to exfil; no duration to inherit | [fetched] |
| [`alshamrani2019`](../extractions/alshamrani2019.md) §II-C Stage 4, §III-D, §III-E | "Retrieving and sending this data"; Carbanak video/keylogger capture; RSA compress+encrypt before send; position-for-future = indefinite harvest | Objective-adjacent; fast grab..slow harvest — no per-tactic number | [fetched] |
| [`outkin2023`](../extractions/outkin2023.md) §1 (Introduction) | "Ready-residence time" = fraction of time in the completed-but-not-yet-executed "Ready" state before acting on objectives | Conceptual dwell-before-objective; parameterised, not empirical per-tactic — no value | [fetched] |
| [`breach_reports_macro_timing`](../extractions/breach_reports_macro_timing.md) (Sophos AAR) | Objective actions like collection/exfil "cannot go any faster, since they rely on human activity, data throughput, or other fairly rigid time frames" — a **dwell floor** | Tier-2 evidence that collection has a *floor* dwell (not substrate-instant); supports a non-trivial objective-execution anchor; no per-tactic number | [fetched] |
| [`ling2023`](../extractions/ling2023.md) §Discussion (SANS hacker survey) | Ethical hackers report they can **collect data within 1–5 h of gaining access** (Bromiley 2022, via Ling & Ekstedt) | Hour-scale enterprise-IT anchor for collection-after-access; second-hand — **now reconciled to the primary (row below)** | [search] |
| [`collection_exfil_timing`](../extractions/collection_exfil_timing.md) (Bromiley 2022 PRIMARY; Unit42 2026; CISA 2022) | **~64% collect+exfil in ≤5 h** (Bromiley primary — closes the ling2023 `[search]`); fastest quartile reached exfil in **1.2 h**; but a CISA APT ran mailbox-search in a 4 h window inside a *months*-long campaign | The collection act is hours (fast eCrime) — reconciles the second-hand Bromiley figure to `[fetched]`; the slow end is the paced APT campaign around it | [fetched] |

## 5. Catalogue inputs — feeds `tactic_durations.json`

- **Group:** <confirm/overturn objective-execution>
- **Relative multiplier:** <×k of group anchor>
- **Sweep range:** <e.g. ×½ / ×2>
- **Tier:** 2 — <why>
- **Justification (one paragraph):** <the §2–§4 synthesis that makes group+multiplier non-arbitrary>
