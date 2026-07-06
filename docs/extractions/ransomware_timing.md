# Ransomware attack-chain timing — access→deploy, dwell, encryption speed (extraction notes)

> A consolidated bundle of ransomware IR-timeline and encryption-speed sources,
> extracted **as Tier-2 macro anchors for the objective-execution tactics** —
> [`04_execution`](../tactic_profiles/04_execution.md) (deploy = run the payload),
> [`08_defense-impairment`](../tactic_profiles/08_defense-impairment.md) (EDR-kill
> prevalence + pre-encryption dwell), [`15_impact`](../tactic_profiles/15_impact.md)
> (encryption speed). Ransomware is the one attack type with published *per-stage*
> timing, so it is the richest calibration target for the fast (eCrime) end of the
> envelope — the espionage low-and-slow end is elsewhere ([`breach_reports_macro_timing`](breach_reports_macro_timing.md)).
> Source files (gitignored): `4_exec/Countdown to Ransomware…IBM.md`;
> `15_impact/Gone in 52 Seconds…Splunk.md`, `..._hou2024_maraudermap_icse.md`,
> `..._secureworks_2024_ransomware_dwell_blog_wayback.md`, `..._TSP_CMC_71705.md`
> (Barach MTD); `8_defence_impair/talos_ir_trends_q4_2024_blog.md`,
> `..._huntress_2025_time_to_ransom_blog.md`.

### Relevance class

**C** (calibration) — Tier-2 macro observables. Whole-chain and per-stage
ransomware timing; the fast, human-plus-throughput-bounded end of the envelope.

### Used in lit review

Execution / defense-impairment / impact §4 timing rows (Step D, 2026-07-06); the
objective-execution group anchor + the exfil/impact "dwell floor" argument.

## Bibliographic anchor

- **Citation keys**: `ibm2022_countdown` (Dwyer/IBM X-Force, *Countdown to
  Ransomware*, 2022); `splunk2022_surge` (Davis/Splunk SURGe, *Gone in 52
  Seconds…and 42 Minutes*, 2022); `hou2024` (Hou et al., *MarauderMap*, ICSE'24);
  `secureworks2024` (Secureworks CTU, *State of the Threat: dwell 24 h*, 2024);
  `barach2026` (Barach, *Ransomware Resilience via MTD*, CMC 86(2), 2026);
  `talos2025_ir` (Cisco Talos IR Trends Q4 2024); `huntress2025` (Huntress,
  *Time to Ransom is Money*, 2025).
- **Pages cited from**: per-source blog/report bodies (access dates 2026-07-06).

## Relevant artefacts

### IBM 2022 (Countdown to Ransomware) — access→deployment collapsed 60 d → 3.85 d

**Source locator:** "Key highlights" + §"speed and efficiency" (2019/2020/2021
figures)

**Paraphrase:** IR analysis of enterprise ransomware (initial-access-broker →
deployment) across 2019–2021 [fetched]. The **average duration from initial
access to ransomware deployment** fell:
- **2019: 2+ months** (~60 days; TrickBot→Ryuk path),
- **2020: 9.5 days** (−85.96% YoY; ZeroLogon CVE-2020-1472 for AD, Cobalt Strike C2),
- **2021: 3.85 days** (−94.34% total; BazarLoader/IcedID → Conti).

Notably the *TTPs did not change* — only the *speed* of transferring
broker-access to an interactive session and reaching AD. Five-stage pattern:
Initial Access → Post-Exploitation Foothold → Recon/Cred-Harvest/Lateral → Data
Collection & Exfil → Ransomware Deployment.

**Maps to:** [`04_execution`](../tactic_profiles/04_execution.md) §4 (deployment =
running the payload — the whole-chain access→deploy bounds the summed dwell of the
intervening tactics under a fast eCrime profile) and
[`15_impact`](../tactic_profiles/15_impact.md) §4.

**Disposition for this thesis:** verified [fetched] — Tier-2 vendor IR. A
whole-chain (access→deploy) duration, not a per-tactic dwell; the fast end.

<!-- Splunk / Hou / Secureworks / Barach (folder 15) and Talos / Huntress
     (folder 8) blocks are appended when those folders are dissected. -->

## Open questions / things to verify

- All figures are **eCrime/ransomware, IR-population** — the fast end of the
  envelope. The espionage low-and-slow end is absent by selection (see
  [`breach_reports_macro_timing`](breach_reports_macro_timing.md) M-Trends 122 d /
  400 d tails). Bounds *shape*, not absolute scale (shape-not-scale).
- IBM's per-stage sub-timings (Interactive Session → 1st Lateral, in hours) are in
  a table partly garbled in the md — if a per-stage number is needed, pull the
  original figure first (`[parse-uncertain]` on the exact hour counts).

## Out of scope for this thesis

Vendor mitigation/product recommendations (MFA rollout, detection tooling);
per-family IOC/TTP detail beyond the timeline milestones; ransomware-economics
narrative (RaaS, broker pricing).
