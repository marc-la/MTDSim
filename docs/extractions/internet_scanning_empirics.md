# Internet-wide scanning empirics — recon/discovery scan tempo (extraction notes)

> Two Internet-telescope measurement papers, extracted **as Tier-2 empirical
> anchors for reconnaissance/discovery *tempo*** — how fast a scan of the whole
> address space runs, and how quickly scanning follows a disclosure. Not
> per-ATT&CK-tactic durations; whole-activity wall-clock observables usable to
> bound the scan-shaped group.
> Source files (both `docs/sources/tactic_profiles/step_d/1_recon/`, gitignored):
> `sec14-paper-durumeric.md`, `3646547.3688409.md`.

### Relevance class

**C** (calibration) — Tier-2 macro observables for the scan-shaped tactics
([`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md),
[`10_discovery`](../tactic_profiles/10_discovery.md)). Confirms the scan verb is
a *fast* action (minutes for the whole IPv4 space) while the campaign-level
recon *tempo* is paced by disclosure→onset lags (hours–days), i.e. the recon
"low-and-slow" is scheduling, not per-scan cost.

### Used in lit review

Recon/discovery §4 timing rows (Step D, 2026-07-06); the scan-shaped group
argument (the substrate scan verb is a fair proxy for a fast active scan).

## Bibliographic anchor

- **Citation keys**: `durumeric2014` (Durumeric, Bailey, Halderman, *An
  Internet-Wide View of Internet-Wide Scanning*, USENIX Security 2014);
  `griffioen2024` (Griffioen, Koursiounis, Smaragdakis, Vroom, *Have you SYN
  me? … Ten Years of Internet Scanning*, ACM IMC 2024).
- **DOI / URL**: Durumeric — USENIX Sec '14 proceedings; Griffioen —
  https://doi.org/10.1145/3646547.3688409
- **Pages cited from**: full text (both).

## Relevant artefacts

### Durumeric 2014 — full-space scan in minutes; disclosure→scan onset in hours

**Source locator:** §1 Introduction; §4 Case Studies (Linksys, Heartbleed, NTP);
§3.7 Estimated Scan Rate

**Paraphrase:** the headline shape is that **ZMap/Masscan reduced the time to
scan the entire IPv4 address space "from months to minutes"** [fetched] — a
scan-shaped action is *fast*, not a dwell. Measured scan rates: ZMap 13 pps –
1.02 Mpps, Masscan 5 pps – 2.2 Mpps (~1.5 Gbps); >90% of scans ran under 100
Mbps, i.e. most attackers don't use the full speed available. The
campaign-tempo anchor is the **disclosure→scan-onset lag**: after the Linksys
backdoor and Heartbleed disclosures, attackers "began scans within 48 hours of
public disclosure" — for Heartbleed, scanning from China within **24 hours**;
comprehensive full-IPv4 scans completed **within 24–48 h** of disclosure.
Almost 80% of non-Conficker scan traffic came from large horizontal scans
(≥1% IPv4). Defensive reaction is near-absent: only ~0.05% of IP space blocks a
persistent scanner, and networks that do block usually "stumble upon" the scan
after *years*, not via automated detection.

**Quote (essential):**
> "attackers began scans within 48 hours of public disclosure" (§4)

**Maps to:** [`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md) §4
(scan verb is fast; recon *tempo* is the disclosure→onset schedule, not per-scan
cost — reinforces the shape-not-scale divergence in §2 that the substrate scan
proxies the modality but not the patient real-world pacing);
[`10_discovery`](../tactic_profiles/10_discovery.md) §4 (internal enumeration is
likewise a fast action); [`02_resource-development`](../tactic_profiles/02_resource-development.md)
/ [`03_initial-access`](../tactic_profiles/03_initial-access.md) (n-day
window: scanning-for-vulnerable-hosts precedes exploitation by ~1–2 days).

**Disposition for this thesis:** verified [fetched] — first-party measurement.
No per-tactic dwell (a whole-activity observable); use only to argue the scan
verb is fast and the recon slowness is scheduling.

---

### Griffioen 2024 — ten-year scan landscape; transient post-disclosure surge, ~daily revisit

**Source locator:** §1 Introduction; §4.3 "Scanning does not have a memory, the
Internet forgets fast" (Fig. 1); §6.6 "Scanners do not come back, except for
institutional ones" (Fig. 6); §5.2 (NMap one-port scan estimate)

**Paraphrase:** a ten-year network-telescope study (2015–2024; three partial /16
blocks; **45 billion SYN packets, 750 million campaigns, 45 million sources**)
[fetched]. **98% of TCP scans are SYN scans**; "it takes only seconds for the
first traffic to arrive" at a fresh public IP. Confirms the months→minutes
tooling shift (ZMap/Masscan scan the whole Internet in minutes; **NMap alone is
estimated at 62.5 days for one port** — the slow-tool baseline). Two findings
that *refine* Durumeric's tempo picture:
- **Post-disclosure scan surges are transient** — a new CVE triggers a sudden
  influx "as reported by [Durumeric]" but "_in the long term_ these trends do
  not continue and activity quickly dies down in a matter of weeks" (Fig. 1),
  overturning the earlier implication that a disclosed port becomes a *permanent*
  scan target. So recon interest in a specific vulnerability is a spike, not a
  plateau.
- **Revisit cadence: recurrent scanners "repeat within one day of the end of the
  last scan"**, but only *institutional* scanners (0.16% of sources, 33% of
  packets) re-scan consistently every day; residential/enterprise scan sources
  are largely single-use ("burned"), so re-scanning is opportunistic, not a
  fixed period. Ecosystem is extremely volatile (>50% of /16s change scan volume
  ≥2× week-on-week).

**Maps to:** [`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md) §4
(recon *is* recurrent, but the re-scan interval is opportunistic — a spike after
new intel, not a metronome; supports modelling recon as a repeatable fast action
re-triggered by new targets rather than a fixed dwell);
[`10_discovery`](../tactic_profiles/10_discovery.md) §4 (re-scan cadence).

**Disposition for this thesis:** verified [fetched] — decade-scale
first-party measurement. Whole-activity cadence, not a per-tactic rate;
independent corroboration + refinement of Durumeric's disclosure→onset shape
(onset fast, surge transient).

## Open questions / things to verify

- Both are *external, Internet-wide* scan measurements — they price the recon
  *modality* (active scanning) and its scheduling, not an APT's internal
  discovery dwell on a specific estate. The mapping to an in-sim recon/discovery
  state is by modality (fast scan verb), not by a transplanted number.
- Griffioen's exact revisit-interval / surge figures were read at abstract +
  section granularity; if a specific number is later cited in §5, pull the
  precise table locator first (papers-are-claims).

## Out of scope for this thesis

Scanner fingerprinting/attribution, geolocation of scan sources, the
blacklisting/exclusion ecosystem, IPv6-scanning open problems, DDoS-amplification
detail — none bear on tactic dwell.
