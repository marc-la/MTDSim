---
status: durable
created: 2026-08-20
updated: 2026-08-20
---

# Literature conventions — field norms the dissertation follows beyond its figures

**Status:** durable. Companion to [`figure_table_conventions.md`](figure_table_conventions.md) (the visual contract): this file carries the **prose, terminology, and methods-reporting conventions** of the MTD / ATT&CK literature, distilled from the same 2026-08-20 page-level survey of `docs/sources/lit_review/original/`. Load it before drafting or scrutinising methodology/results prose, and before writing anything that names ATT&CK, CVSS, a kill-chain model, or a security metric. Every rule below is anchored to an observed exemplar in the corpus — these are the field's norms, not this repo's inventions.

Division of labour: sentence-level voice is [`voice.md`](voice.md) (first-principles, untouched by this file); figure/table grammar is `figure_table_conventions.md`; metric *semantics* and divergences are [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md); constant provenance is [`../implementation/provenance.md`](../implementation/provenance.md). This file states the conventions; those files hold the content the conventions apply to.

## a) MITRE ATT&CK referencing (the binding rule set)

1. **Full name + citation on first use, `ATT&CK` thereafter.** First mention is "MITRE ATT&CK" with the framework citation (rahman2024: "MITRE corporation introduced ATT&CK [9] in 2013"; brown2023: "MITRE ATT&CK Framework [18]").
2. **State the version once, in methods, with its size.** The field's form is a single declarative sentence: *"We use version 12.1 of MITRE ATT&CK containing 193 techniques."* (rahman2024, p. 7); sadlek2022 likewise: "the Enterprise ATT&CK matrix of version 10.1". **Ours:** the dissertation states the pinned bundle's ATT&CK version (the bundle under `data/gap/`) in ch4 exactly once in this form, and every downstream chapter inherits it. Sessions never write "the current version of ATT&CK" — the pin is the version of record, and derived figures/tables repeat it per `figure_table_conventions.md` §b5.
3. **Technique mention form:** ID + name on first mention — `T1566: Phishing` — ID alone thereafter; sub-techniques as `Txxxx.xxx` (rahman2024 defines the `.xxx` convention explicitly, p. 2). In tables, rows carry `TXXXX. Name` (al-sada2024 Table 1).
4. **Tactic names are proper names when they name ATT&CK tactics** (capitalised in tables/figures: "Lateral Movement", "Defense Evasion" — al-sada2024, rodriguez2024) and common nouns in running prose ("the attacker moves laterally"). Inside ATT&CK proper names, the framework's US spelling stands (see §c1).
5. **TTPs expanded on first use** — "tactics, techniques, and procedures (TTPs)" (rahman2024, p. 2).

## b) Version-stamp every external framework, and justify the choice

The corpus names the version of *anything* versioned it builds on, and justifies the choice when a newer version exists: hong2018 (p. 40): "We use the CVSS version 2, as many of the legacy vulnerabilities do not have the version 3 available yet…". Kill-chain models are named to their variant, not just "the kill chain" — cho2020 (p. 721) distinguishes the Hutchins et al. seven-phase CKC from "MIT Lincoln lab['s] shorter version". **Ours:** any external framework the model leans on (ATT&CK version, CVSS scoring generation via inherited constants, the kill-chain/lifecycle variant behind the tactic axis) is named to its version/variant once, with a reason where a newer one was passed over. The inherited substrate's constants already have this trail in `provenance.md` — the convention is that the *dissertation text* surfaces the version sentence, not only the repo record.

## c) Terminology

1. **Australian spelling is licensed for the field's common nouns.** Australian-authored papers in the corpus write "moving target defence" (masud2025, title: "Vulnerability defence using hybrid moving target defence"; tay2024, title) — so the dissertation keeps AU spelling ("defence", "modelling", "behaviour") throughout, per the standing AU-English guardrail. US spellings survive only inside proper names and titles of cited works: "Defense Evasion" (an ATT&CK tactic), *MTD-AD: Moving Target Defense as Adversarial Defense* (a title). Never "correct" a quoted or cited name.
2. **Acronyms expand at first use, then abbreviate** — universal in the corpus. The field's canon: MTD, APT, CKC, TTP, HARM, SDR, C2 (alshamrani2019 introduces C&C/C2 with both forms). Heading-level acronym rules are Marc's heading conventions (headings avoid acronyms; L0–L4 prefixes stay).
3. **Classify MTD techniques in the field's two canonical framings when introducing them:** the SDR taxonomy (shuffling / diversity / redundancy) and the three design questions (*what to move, how to move, when to move*), both established by cho2020 (pp. 713–714) and used as positioning vocabulary across the corpus (kim2026, jalowski2026). When ch2/ch4 describe the inherited simulator's MTD mechanisms, each gets its SDR class and its what/when/how answers — a literature reader expects that mapping and will notice its absence.
4. **Timeliness vocabulary:** *proactive / reactive / hybrid* for MTD triggering (cho2020 Fig. 3; jalowski2026 "timer-based, event-based, or a combination"). Use these exact terms for trigger semantics, not ad-hoc synonyms.

## d) Metrics

1. **A metric is defined before it is used: name, acronym, formal definition (numbered display equation), and direction.** hong2018 defines its whole metric family this way (pp. 40–41), normalising to [0, 1] and stating the direction in words ("a metric value toward one is making the attack more difficult", p. 45). The convention: no metric appears in a results table that was not first defined with its equation and its better-direction.
2. **The field's canonical metric acronyms are reserved words** — MTTC, MTTF, ASP (attack success probability), RoA (return on attack), AC (attack cost), attack surface (cho2020 Figs. 6–7 catalogue them). **Never reuse a canonical name with divergent semantics silently**: where our internal MTTC diverges (C7, ATK-04), the dissertation says so at the definition site and respects the comparability boundary in `metrics_semantics.md` — a named divergence is a defensible choice, an unnamed one reads as an error.
3. **Symbols are declared at the equation** ("where …" immediately after — hong2018, kim2026 throughout), italic in math, and reused consistently; series names in results figures may then use the declared symbols (kim2026's $S_{vIP}+D_{SW}$; `figure_table_conventions.md` §f).

## e) Methods-reporting genre expectations

What the literature reports about an evaluation, every time — the checklist ch4/ch5 must satisfy:

1. **An explicit attacker/threat-model statement in its own subsection** — hong2018 §6.1.2 "Threat model"; brown2023 §III.C "Modeling the Attacker"; masud2025 likewise. The stake is sharpened by jalowski2026 §4.3, which attacks the MTD literature precisely for "ill-defined attacker models … based on completely unrealistic assumptions" — the genre both expects the section and punishes its absence. Ours additionally answers to the APT-model criterion (`../implementation/apt_model_criterion.md`) — the badge ceiling governs what the threat-model section may claim.
2. **A parameter table plus declared distributions and run counts** — brown2023 TABLE I with `Uniform(1000, 5000)` ms and E(T) stated; bland2020 reports episode counts (100,000) per configuration. Ours: the ch5 setup states parameters (table genre in `figure_table_conventions.md` §e3), the seed/replication scheme, and run counts per cell — numbers flowing from tracked artefacts, never typed.
3. **Position the evaluation method on the field's ladder** — analytical model / simulation / emulation / real testbed, with the pros and cons owned (cho2020 TABLE VI). The dissertation says explicitly that this is simulation, cites the ladder, and owns simulation's cons (parameterisation realism, abstraction) rather than leaving them implicit.
4. **A limitations discussion that owns attacker-realism concessions in the authors' own voice** — brown2023 §V.A/§V.C ("the exploitation skills are not configured to distinguish the skills of adversaries…"). The genre expects the authors to name their model's unrealism before a reviewer does; ch6 carries this, bounded by the criterion badges.
5. **Named scenarios/conditions are bold-defined once and then used verbatim** — brown2023's "General Attack Scenario (Scenario 1)" / "Target Attack Scenario (Scenario 2)" pattern, reused identically in figures and tables. Our profile/arm names follow the same discipline: one defining sentence, then the exact name everywhere (no drifting synonyms between text and figure keys).

## f) Cite the canon for each concept

The field has settled canonical citations, and the corpus's own tier naming already encodes them: MTD's origin → the NITRD framing (ghosh2009); the kill chain → Hutchins et al. (via cho2020's usage); ATT&CK → MITRE; CVSS → its specification; HARM → the Hong/Kim lineage (brown2023 extends "the 2-layer HARM proposed by Alavizadeh et al."). Rule: a concept is cited to its origin, not to whichever survey mentioned it — cite a survey only when the survey's *synthesis* is the claim. (Survey-vs-origin disputes are "to verify" for Marc per the guardrails, never silently resolved.)

## g) Open flags (Marc to ratify before first use)

- **Explicit RQ framing** — rahman2024 and buechel2025 organise findings around numbered RQs ("Findings on RQ1"). Whether ch1 states numbered research questions is a structure ruling (V-series governs); flag, don't adopt unilaterally.
- **Numbered contributions list closing the introduction** — near-universal in the corpus (rahman2024 p. 2); presumed but not yet ratified for ch1.
- **Artefact-availability statement** — the modern norm (rahman2024 open-sources dataset and models; USENIX artifact culture in buechel2025). Whether and how the dissertation points at the repo is Marc's call, entangled with the AI-use declaration rewording.
