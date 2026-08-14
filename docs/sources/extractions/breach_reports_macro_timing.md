# Vendor breach reports — macro-timing calibration targets (extraction notes)

> Institutional source-bundle. Four vendors' incident-response statistics,
> extracted **as calibration targets for operational validation**, not as
> per-tactic timing. Per
> [`../notes/2026-07-04_operational_validation_the_bar.md`](../../notes/ch4_methods/operational_validation.md),
> breach-report *statistics* are allowed Tier-2 literature (they are **not** the
> Attack Flow corpus / `observation_count`) and are exactly the observable
> campaign-shape patterns the calibrated timeline is fitted to reproduce.
> Source files (all `docs/sources/tactic_profiles/step_c/`, gitignored):
> `mandiant_mtrends_2026_blog.md` / `..._2025_blog.md` (+ full PDFs);
> `crowdstrike_gtr_2026_press.md` / `..._2025_press.md` (+ full PDFs);
> `sophos_aar_2025.md` (+ PDF), `sophos_aar_2023.md`, `..._2024_1h.md`,
> `..._2024_dec.md`, `..._2026.md`; three DFIR case reports
> (`dfir_report_confluence_..._lockbit`, `..._rdp_..._ransomhub`,
> `..._blacksuit_ransomware`).
> This bundle reconciles the precedent survey's `[search]`-flagged macro table
> ([`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../../notes/ch2_background/tactic_duration_precedent_survey.md)).

### Relevance class

**C** (calibration) — Tier-2 macro observables. Whole-campaign or
single-transition granularity; **no vendor publishes a per-ATT&CK-tactic
duration breakdown** (the gap statement holds). Use to set the plausibility
envelope and *relative* structure, never a per-tactic absolute.

### Used in lit review

Precedent-survey macro-timing table (reconciliation); the method note's
calibration targets; tactic-profile §4 rows (Step C, 2026-07-05).

## Bibliographic anchor

- **Citation keys**: `mtrends2026` / `mtrends2025` (Mandiant/Google Cloud
  M-Trends); `crowdstrike_gtr2026` / `..._gtr2025` (CrowdStrike Global Threat
  Report); `sophos_aar2025` / `..._aar2023` (Sophos Active Adversary Report);
  `dfir_<case>` (The DFIR Report case studies).
- **Pages cited from**: blog/press pages + report PDFs; DFIR case exec
  summaries. Access date 2026-07-05.

## Relevant artefacts

### Mandiant M-Trends — global median dwell + the pacing divergence

**Source locator:** `mtrends2026_blog.md` "By the Numbers"; "The Collapse of
the Hand-Off Window"; "Edge Devices … Extreme Persistence"

**Paraphrase:** the headline observable is **global median dwell time = 14
days (2025 data), up from 11 days (2024)** [fetched] — reconciles the survey's
"~14 days" M-Trends figure. Reported splits and transitions:

- **Cyber-espionage + DPRK-IT-worker median dwell: 122 days** — the
  low-and-slow tail, an order of magnitude above the global median.
- **Detection-source dwell split (M-Trends 2025, 2024 data, global median 11
  d):** **26 days when externally notified, 5 days when adversary-notified**
  (ransomware), **10 days when internally discovered** — the closest thing to a
  per-channel dwell distribution; usable to shape the dwell distribution rather
  than a single point.
- **BRICKSTORM edge-device implants: dwell ~400 days**, "persistence that
  routinely survives standard remediation efforts and system reboots" — the
  extreme-persistence end (reset-survivor evidence for persistence/C2).
- **Initial-access → hand-off-to-secondary-group: >8 hours (2022) → 22
  seconds (2025)** — eCrime pre-staging collapses the inter-actor window.
- **Mean time to exploit ≈ −7 days** (exploitation routinely *before* patch).
- Initial infection vectors 2025: exploits 32% (6th year running), voice
  phishing 11%, prior compromise 10% (30% in ransomware).

The report frames 2025 as a **divergence in adversary pacing**: eCrime
optimises for immediate impact + recovery denial; espionage/insider optimise
for extreme persistence. This is the smash-and-grab vs slow-and-deliberate
axis ([`selmanaj2024`](selmanaj2024.md)) quantified.

**Maps to:** whole-intrusion dwell observable → the calibration target the
emergent timeline's dwell shape is fitted to; the 14 d vs 122 d vs 400 d
spread = the *relative* structure across actor classes (not per-tactic).

**Disposition for this thesis:** verified [fetched] — primary Mandiant blog +
PDF; supersedes the Selmanaj-reported Table 2-1 trend as the citable figure.

---

### CrowdStrike GTR — breakout time (initial access → lateral movement)

**Source locator:** `crowdstrike_gtr2026_press.md` (headline + "Fastest
Breakout Time on Record"); `crowdstrike_gtr2025_press.md`

**Paraphrase:** **breakout time** = the single transition **initial access →
lateral movement** for eCrime intrusions. **Average 29 minutes (2025 data,
GTR 2026), fastest observed 27 seconds** [fetched] — a 65% speed increase from
the 2024 figure of **48 minutes avg / 51 seconds fastest** (GTR 2025). One
2026-report intrusion: "**data exfiltration began within four minutes of
initial access**." This reconciles and *updates* the survey's "~29 min avg /
27 s" [search] figure to [fetched] (and confirms the 48 min / 51 s prior).

**Maps to:** the initial-access→lateral-movement transition → a
plausibility bound on the *combined* dwell of the early tactics under a fast
(eCrime) profile; the 4-minute access→exfil case bounds the whole fast chain.

**Independent corroboration — ReliaQuest 2026** (`reliaquest2026`;
`docs/sources/tactic_profiles/step_d/11_lat_movement/reliaquest_2026_annual_threat_report_blog.md`):
a separate vendor's breakout series — **average breakout time 34 minutes (2025
data), fastest 4 minutes** (an 85% YoY acceleration), and **fastest data
exfiltration 6 minutes** [fetched]. Independent of the CrowdStrike series and
consistent with it (29 min / 27 s), reinforcing the fast-eCrime access→lateral
anchor. ReliaQuest also names the two poles explicitly — "machine-speed breakouts
that sprint to exfiltration in minutes, and slow-burn nation-state operations that
persist for months" — the bimodal envelope the calibration must span.

**Disposition for this thesis:** verified [fetched] — first-party CrowdStrike +
ReliaQuest corroboration. Caveat: eCrime, not APT-espionage; the fast end of the
envelope. Breakout start/end anchors differ from Mandiant "dwell" — independent
calibration points, not one timeline.

---

### Sophos Active Adversary Report — the multi-milestone chain (best granularity)

**Source locator:** `sophos_aar_2025.md` L64 (dwell), L190 (time-to-AD), L220
(exfiltration); `sophos_aar_2023.md` (time-to-AD ~16 h)

**Paraphrase:** the finest-grained public breakdown — **named milestones
within a campaign**. Every edition's figure is a *different anchor definition
and year*, so the honest use is the **range across editions**, not a single
point. All [fetched]:

- **Median dwell (all cases):** **3 days (2026 ed., 2025 data)** — IR all-cause
  5.0 d (down 29% YoY), MDR 2.0 d, non-ransomware IR 6.0 d (longest); **2 days
  (2025 ed., 2024 data)** — IR 7 d, ransomware 4 d, non-ransomware 11.5 d; MDR
  ransomware 3 d / non-ransomware 1 d; **8 d IR-overall (2024 1H ed.)**; **6 d
  full-year 2023 median** (mean 18.18, max 289). The 2024-1H dwell deep-dive
  gives the longer-horizon trend (2022-outlier-removed): **2021 median 13 d /
  2022 10 d / 2023 6 d**; non-ransomware 2021 **52.5 d** (high end); one
  legitimate **955-day** outlier case (upper tail). Dwell is trending down but
  the *envelope* spans hours to ~3 years.
- **Initial access → Active Directory compromise: median 3.40 hours (2026 ed.,
  "sped up 70% YoY")**, 0.46 d ≈ **11 h (2025 ed.)**, 17.21 h (2024-1H IR),
  0.64–0.68 d ≈ **~16 h (2023 ed.)** — with a wide per-case spread (negative
  values where AD is compromised before the nominal "attack start"). Reconciles
  the survey's "access→AD ~11 h" [search] → [fetched]; **current anchor ≈ 3–16
  h depending on edition.**
- **Attack start → exfiltration: median 78.83 hours (2026 ed.)**, **72.98 hours
  (3.04 d, 2025 ed.)**; **exfiltration → detection: 1.87 h (2026) / 2.7 h
  (2025)**; **exfiltration → public leak within ~19.5 days** (49% of
  confirmed-exfil ransomware cases, 2026; 28.5 d in 2023). Attack-start →
  ransomware deployment median **3.76 d** (confirmed-exfil cases, 2024-1H);
  exfil → deployment **0.6 d**. Reconciles "access→exfil ~73 h" [search] →
  [fetched].
- **AD-acquisition → detection window: 29.12 h (2024-1H), down from 48.43 h
  (2023)** — how long the attacker holds AD before discovery.
- **Mean-time-to-exploit, the *slow* sign:** vendor advisory → exploited
  **median 322 days**, public PoC → exploited **296.5 days** (2026 ed.) — the
  opposite tail from M-Trends' −7 d (edge-device zero-days); real exploitation
  timing is bimodal.
- **Dwell-floor argument (load-bearing):** "certain actions (for instance,
  exfiltrating the data) cannot go any faster, since they rely on human
  activity, data throughput, or other fairly rigid time frames" — direct
  evidence that exfiltration/collection have a *floor* dwell, not a
  substrate-instant, and that ransomware traditionally needs longer timeframes.

**Maps to:** the **held-out observable** for operational validation — calibrate
the group anchors on M-Trends dwell shape, then check the Sophos
access→AD (~11 h) and access→exfil (~73 h) milestones emerge approximately
right (method note rule 3, "hold out an observable") ·
[`14_exfiltration`](../../notes/ch4_methods/tactic_profiles/14_exfiltration.md) /
[`12_collection`](../../notes/ch4_methods/tactic_profiles/12_collection.md) (the exfil floor);
[`09_credential-access`](../../notes/ch4_methods/tactic_profiles/09_credential-access.md) /
[`11_lateral-movement`](../../notes/ch4_methods/tactic_profiles/11_lateral-movement.md) (the
race-to-AD chain).

**Disposition for this thesis:** verified [fetched] — the best calibration
target; multiple named milestones make it usable for the held-out check.
Enterprise-IT (not ICS), IR/MDR-population — a plausibility envelope, not
ground truth for a synthetic network.

---

### The DFIR Report — three per-case timelines spanning two orders of magnitude

**Source locator:** the three case exec-summaries + timeline sections

**Paraphrase:** per-incident timestamped timelines (the granularity vendors
aggregate away), deliberately spanning tempos — **Time-to-Ransomware (TTR) 2 h
→ 118 h → 328 h**:

- **Confluence → LockBit (fast smash-and-grab): TTR 02:06:14 (~2 h).**
  Confluence RCE → SYSTEM; Mimikatz at **+20 min**; process enum +10 min;
  lateral via RDP/SMB (password reuse enabled instant spread); Rclone exfil to
  MEGA; clear event logs; ransomware — all in 2 hours.
- **RDP password spray → RansomHub (mid-tempo): TTR ~118 h over 6 days.**
  Initial access = **4-hour password spray**; lateral to 2 DCs **~2 h after
  auth**; Mimikatz/Nirsoft credential harvest; **day 3** Rclone exfil over
  SFTP:443; "concluded their operations for the day" (human working-hours
  pacing); ransomware kills VMs, deletes shadow copies, clears logs.
- **BlackSuit (slow-and-deliberate): TTR ~328 h over 15 days.** Cobalt Strike
  beacon → "**no immediate follow-up**"; +6 h discovery (systeminfo, nltest,
  Rubeus AS-REP/Kerberoast, Sharphound); first lateral +10 min (SMB beacon);
  LSASS creds; **"Five days later, the threat actor returned to finalize their
  objectives"** → ADFind, exfil, BlackSuit via SMB C$ + RDP, vssadmin shadow
  deletion. The 5-day dormant gap is the slow-and-deliberate dwell.

**Maps to:** intra-tactic tempo texture — credential-access (Mimikatz) lands
minutes-to-hours post-access; lateral-movement in +10 min to +2 h (matches the
survey's "lateral-move mins–1 h"); the whole-chain 2 h → 328 h spread is the
range operational validation must span across profiles, not a single point.

**Disposition for this thesis:** verified [fetched] — per-case, **not
aggregate**; use as tempo illustrations and to sanity-check intra-tactic
ordering, never as a rate. All ransomware/eCrime; the espionage-never end is
absent by selection.

## Open questions / things to verify

- All figures are **enterprise-IT, IR/MDR-population, mostly eCrime/
  ransomware** — the espionage low-and-slow end shows only in M-Trends' 122 d /
  400 d tails. The substrate network is synthetic, so these bound *shape*, not
  absolute scale (method note, shape-not-scale).
- Cross-vendor anchors are **not commensurable** (each defines dwell/breakout
  start/end differently, over different populations) — treat as independent
  calibration points; do not chain them into one timeline.
- M-Trends/CrowdStrike full-report PDFs (`..._2026.pdf`, `..._gtr2026.pdf`)
  hold per-region/per-sector dwell splits not mined here — pull only if a
  finer calibration split is needed.

## Out of scope for this thesis

Vendor product/recommendation sections; AI-threat narrative (M-Trends AI,
CrowdStrike "AI arms race"); attribution/actor-naming; DFIR per-tool command
detail (Sigma rules, IOCs) beyond the timeline milestones.
