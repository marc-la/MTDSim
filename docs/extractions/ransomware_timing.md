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

### Talos 2025 (IR Trends Q4 2024) — ransomware dwell 17–44 days; defence-kill is prevalence

**Source locator:** IR-trends body (dwell times; Interlock; MFA/EDR findings)

**Paraphrase:** Talos IR identified **dwell times of ~17–44 days** across most Q4-2024
ransomware engagements [fetched] — in the **Interlock** incident, **17 days from
initial compromise to encryptor deployment**; a **RansomHub** case ran over a
month (internal scanning, backup-password access, credential harvesting) before
encryption. The *slow* end of the ransomware envelope, opposite Huntress's hours.
Defence-impairment texture: **100% of ransomware-impacted orgs lacked properly
configured MFA or had it bypassed**; EDR misconfigured/missing in >25% of all
incidents; Impair Defenses (T1562.001, disable/modify tools) observed. This is a
**prevalence/rate** phenomenon, **not** a per-phase duration.

**Maps to:** [`08_defense-impairment`](../tactic_profiles/08_defense-impairment.md)
§4 (the gap-documenting result: defence-disabling is measured as %-of-cases, not a
dwell → Tier-3 wide sweep) and [`15_impact`](../tactic_profiles/15_impact.md) /
[`05_persistence`](../tactic_profiles/05_persistence.md) (17–44 d dwell — the slow
ransomware tail).

**Disposition for this thesis:** verified [fetched] — Tier-2 IR. The dwell range
is whole-chain; the MFA/EDR figures are prevalence, not timing.

---

### Huntress 2025 (Time to Ransom) — avg ~17 h access→encryption, fastest ~4 h

**Source locator:** "Time-to-ransom" section (17 h; 4 h; 18 actions)

**Paraphrase:** across incidents, the **average time-to-ransom (initial access →
ransomware deployment) was almost 17 hours**, with some actors averaging **just
over 4 hours** [fetched]; ransomware groups took an **average of 18 actions**
before triggering the payload (Phobos/Maze >30; Conti/Play/Black Basta <10). The
*fast* end of the envelope — hours, not the Talos days — showing the access→deploy
duration is bimodal across actor tempo. (A 2024 Statista figure: victim downtime
averages 24 days — an hours-long attack → weeks-long disruption.)

**Maps to:** [`08_defense-impairment`](../tactic_profiles/08_defense-impairment.md)
/ [`15_impact`](../tactic_profiles/15_impact.md) §4 (fast access→deploy; the
pre-payload "18 actions" include the impair-defenses/lateral steps).

**Disposition for this thesis:** verified [fetched] — Tier-2. A whole-chain
access→deploy duration; the fast end (hours). With Talos (days), brackets the
ransomware envelope.

### Splunk 2022 — per-family encryption speed: 5m50s (LockBit) → ~2h (PYSA)

**Source locator:** encryption-speed comparative table; "Family Median Duration"

**Paraphrase:** benchmarked the *encryption* action across ransomware families on
a fixed testbed [fetched]. Per-family speed/time (for a fixed corpus): **LockBit
2.0 ≈ 373 MB/s (~4m26s)**, LockBit ≈ 266 MB/s (6m16s), **PYSA ≈ 128 MB/s (~13m)**;
the headline range is **~5m50s (fastest family median) to ~1h55m (PYSA)**, overall
median **~42m52s**. The impact *act* (encryption) is minutes-to-a-couple-hours,
and is throughput-bound (a genuine floor — you cannot encrypt faster than disk
I/O).

**Maps to:** [`15_impact`](../tactic_profiles/15_impact.md) §4 (the encryption
action is minutes-to-hours, throughput-bound — the objective-execution act has a
real, non-instant dwell).

**Corroboration — Davies & Macfarlane 2026** (`davies2026`;
`docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/1-s2.0-S0045790626000315-main.md`
— *mis-filed under folder 0; it is a ransomware paper, not a timed-model*): a
benchmark of **29 active crypto-ransomware strains** measuring total execution
time, pre-encryption delay, and encryption performance [fetched]. Headline: **wide
variation in encryption speed, 33 MB/s to 2.79 GB/s**, with distinct preparatory
vs encryption sequences and frequent **intermittent encryption** (encrypt part of
each file) to accelerate impact and evade detection. Independently corroborates
Splunk's "encryption is fast but throughput-bound, with large per-family spread."

**Disposition for this thesis:** verified [fetched] — Tier-2 benchmark. A
per-family *encryption-speed* datum (the impact act), not a whole-campaign dwell.

---

### Hou 2024 (MarauderMap) & Secureworks 2024 & Barach 2026 — corpus, dwell, MTD-vs-ransomware

**Source locator:** Hou Abstract; Secureworks §"Dwell Times"; Barach Abstract + §1

**Paraphrase:** [all fetched]
- **Hou 2024 (MarauderMap, ICSE):** 7,796 active ransomware samples executed in
  isolated testbeds (1.98 TiB logs); phases = data reconnaissance → tampering →
  exfiltration; mitigation strategies raise detection +41–69%. Confirms the
  ransomware impact-chain has distinct, instrumentable phases (not one instant).
- **Secureworks 2024:** median ransomware **dwell ~28 hours**, straddling two
  clusters (well below / well above the median); **as short as 7 hours**;
  multi-site events increasingly rare — corroborates the fast eCrime dwell (with
  IBM/Huntress) vs the Talos 17–44 d slow tail.
- **Barach 2026 (MTD-HR, CMC):** an MTD framework (container mutation + IP hopping
  + runtime service rotation, Kubernetes) tested on WannaCry/Locky/Ryuk — reports
  **mean-time-to-containment 91.4 s** and encryption reduced to 13.2% of baseline
  by blocking lateral ransomware spread. The §3 MTD-vs-ransomware effect: shuffling
  the runtime surface contains lateral spread mid-attack.

**Maps to:** [`15_impact`](../tactic_profiles/15_impact.md) §4 (dwell ~7–28 h;
encryption phases) and §3 (Barach: MTD contains lateral ransomware spread → a
reset that limits blast radius); [`05_persistence`](../tactic_profiles/05_persistence.md)
(dwell).

**Disposition for this thesis:** verified [fetched] — Tier-2. Hou/Secureworks =
corpus + dwell; Barach = an MTD-effect on ransomware impact (§3). Cloud/HR domain
for Barach — a *shape* result (MTD limits spread), not a transplant.

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
