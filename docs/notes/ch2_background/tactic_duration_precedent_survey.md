---
status: durable
chapter: ch2_background
created: 2026-07-04
updated: 2026-07-13
lineage: 2026-07-04_tactic_duration_precedent_survey.md
---

# No prior work assigns justified per-tactic durations — the gap is real, and the field norm is "declare and sweep"

## Position in the dissertation

The precedent survey behind the background chapter's gap statement for the timing layer, and the citable answer to an examiner's "did you look?". It also supplies the positioning claim the methodology chapter leans on: the declare-and-sweep discipline this thesis adopts *is* the field norm, and the calibration step goes further than that norm, not less far.

## The idea

This project attaches a dwell time to every MITRE ATT&CK tactic so that a discrete-event simulator can execute a behaviourally-grounded attacker. The claim that no ready-made resource maps tactics to durations — the supervisor's justification for defining them ourselves — is here checked rather than assumed, by a four-way survey of the modelling literature, public incident corpora, adversary-emulation frameworks, and vendor breach reporting.

### The verdict

**Per-ATT&CK-tactic durations with justification: no precedent exists.** The one tactic-level ATT&CK Petri-net model in the literature (Rodríguez et al. 2024) is *untimed* — its process-mined nets use log timestamps only to order events, never as rates or dwells. Every timed adversary model that carries ATT&CK labels either attaches timing at the *technique/CVE* level or declares its rates outright. The layer this thesis builds — a justified, tiered, calibrated tactic-to-duration catalogue — is genuinely open ground.

### Where timed-model numbers actually come from

The dominant practice, across the stochastic attack-modelling literature, is to **declare the rates and sweep them**: the standard defence is "the true rate is unknowable, so we report sensitivity over the assumed value". Genuinely empirical timing is the exception and lives only at vulnerability/exploit granularity — CVSS/NVD-derived or testbed-measured — never at the tactic level. Calibrating declared values against observed behaviour is essentially absent. Three precedents carry the argument:

- **Bland et al. (2020)**, the closest executed stochastic-Petri-net precedent, states verbatim that "for the purpose of the example arbitrary rates are used and would later have to be determined by subject matter experts" — while the net's *structure* was face-validated by fourteen security practitioners. This is direct prior art both for declared-and-justified values and for face-validation as an acceptable standard.
- **McQueen et al. (2006)**, the root of the time-to-compromise lineage, openly blends expert elicitation, thin empirical anchoring, and admitted arbitrariness: one sub-process mean is set "somewhat arbitrarily" at 8 hours while another is anchored empirically at 5.8 days. Its declared per-skill dwell for compromising a component with no known vulnerability (21 days for an expert, 193 for a novice) is the closest thing in the lineage to a declared per-stage dwell.
- **Xiong, Hacks and Lagerström (2021)** ship the flagship ATT&CK-wide simulation language (enterpriseLang) *untimed* — the underlying framework supports per-step time distributions, but the published language does not assign them; a companion paper assigns distributions by converting a systematic literature review into probability distributions — still declared-class sourcing, not empirically fitted rates.

The one clean per-technique positive, **Ling and Ekstedt (2023)**, estimates time-to-compromise for ATT&CK-for-ICS *techniques* from empirical CVE data (2,740 ICS vulnerabilities, exploit availability, advisory dates). It does not close the gap: it is per-technique, ICS-specific, and requires real vulnerability instances to attach to — which this simulator's synthetic vulnerabilities cannot supply. Two of its findings matter directly here: under an expert-attacker assumption its per-technique estimates degenerate toward a shared six-day floor (empirical support for calibrating a few *group anchors* rather than fifteen independent values), and CVE-based timing structurally cannot price command-and-control or the concealment half of evasion, because neither exploits a vulnerability — those tactics are free parameters in *any* model.

### Corpora and emulation frameworks: sequence yes, timing no

Public incident corpora encode *order*, not *tempo*. The Attack Flow schema defines optional per-action start and end timestamps — the exact intended home for this data — but the public corpus leaves them empty, because breach reports rarely contain machine-usable timestamps. ATT&CK campaign records carry only month-granularity first/last-seen dates. A Caldera-executed APT dataset (Syed et al. 2025; 23 campaigns across 12 groups) curates pure technique sequences whose timestamps measure testbed execution latency, not adversary dwell. Across eight adversary-emulation frameworks surveyed (Caldera, Atomic Red Team, the CTID emulation library, and five others), no framework attaches a per-phase dwell or time budget to its phase-to-ability mapping; the only temporal fields anywhere are beacon cadence, per-command kill-timers, and post-hoc recorded timestamps. A per-phase ability catalogue that *additionally* assigns each phase a justified dwell has no identified public analogue — an absence worth stating in the thesis. The only genuinely per-stage-timed public sources are raw host-event datasets with red-team ground truth (DARPA OpTC and Transparent Computing), from which per-tactic timing is *derivable* by binning timestamped actions — a real but heavy empirical option, recorded as out of scope unless deliberately taken up.

### Empirical macro-timing: whole-campaign or single-transition, never per-tactic

No vendor breach or incident-response report publishes a per-tactic duration breakdown; they report whole-campaign aggregates or single named transitions. The usable calibration targets:

| Source | Latest figure | Metric | Granularity |
|---|---|---|---|
| Mandiant M-Trends | 14 days global median dwell (2026 ed.); espionage splits to ~122 d | dwell | whole intrusion |
| CrowdStrike GTR | 29 min average / 27 s fastest (2026 ed.) | breakout time | one transition: initial access → lateral movement |
| Sophos Active Adversary | dwell 2–3 d; access→AD ~3.4 h; access→exfiltration ~73–79 h | multi-milestone chain | best industry granularity — named milestones |
| The DFIR Report | per-case times to ransomware of 2 h / 118 h / 328 h; credential dumping +20 min after access | per-incident timestamps | per-technique but per-case |

The first four vendors' figures are reconciled against their primary reports; a further tail (Secureworks, IBM X-Force, Unit 42) remains search-level and is not used as a calibration target. Cross-report comparability is weak — each vendor defines dwell and its start/end anchors differently, over different incident populations — so these are independent calibration points, never one consistent timeline. That weakness *reinforces* the shape-not-scale decision defended in the operational-validation note: the honest use of macro timing is to set relative structure and a plausibility envelope, not absolute per-tactic times.

### What the survey licenses

The gap statement ("no justified per-tactic duration catalogue exists") stands, and the method this thesis adopts is positioned *above* the field norm rather than below it: the norm is declare-and-sweep; this work declares, justifies per-tactic from behavioural literature, badges each value's validity tier, calibrates group anchors against macro observables, and sweeps. The survey is web-search-bounded, not a systematic review, and the gap claim is worded accordingly ("no identified precedent", not "provably none").

## Evidence and repo anchors

- Extractions behind each named source: [`rodriguez2024`](../../sources/extractions/rodriguez2024.md), [`bland2020`](../../sources/extractions/bland2020.md), [`mcqueen2006`](../../sources/extractions/mcqueen2006.md), [`xiong2021`](../../sources/extractions/xiong2021.md), [`ling2023`](../../sources/extractions/ling2023.md), [`syed2025`](../../sources/extractions/syed2025.md), [`selmanaj2024`](../../sources/extractions/selmanaj2024.md), [`chemat2024`](../../sources/extractions/chemat2024.md), [`timed_attack_models`](../../sources/extractions/timed_attack_models.md) (the wider declare-and-sweep precedent cluster), [`breach_reports_macro_timing`](../../sources/extractions/breach_reports_macro_timing.md) (the reconciled macro table), [`attackflow`](../../sources/extractions/attackflow.md), [`mendonca2023`](../../sources/extractions/mendonca2023.md).
- The method this survey legitimises: [`../ch4_methods/operational_validation.md`](../ch4_methods/operational_validation.md).
- The catalogue it grounds: [`../../../data/ogasp/tactic_durations.json`](../../../data/ogasp/tactic_durations.json) and the profiles at [`../ch4_methods/tactic_profiles/`](../ch4_methods/tactic_profiles/).
- Unreconciled tail (do not cite without primary-source reconciliation): Secureworks ~28 h median ransomware dwell (2024); IBM X-Force <4 d access→ransomware (2023); Unit 42 median exfiltration ~2 d (2025).

## Revisit conditions

- If a per-tactic timed ATT&CK model surfaces, the gap statement weakens to "near-absent" and reframes as positioning against that precedent.
- If the DARPA OpTC/TC mining option is taken up, an empirical tier enters the catalogue and the sourcing-category decision must be recorded first.
- If the simulator adopts real (NVD) CVEs, Ling and Ekstedt's per-technique method becomes directly applicable and the frontier moves.
- If any search-level figure fails primary-source reconciliation, drop or correct it before it hardens into a calibration target.
