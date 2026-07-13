# Collection & exfiltration timing — the objective-execution dwell floor (extraction notes)

> Sources on **how long data collection and exfiltration take**, extracted for
> [`12_collection`](../../notes/ch3_design/tactic_profiles/12_collection.md) and
> [`14_exfiltration`](../../notes/ch3_design/tactic_profiles/14_exfiltration.md). Two poles: a *fast*
> eCrime end (collect-and-exfil in ≤5 h; fastest quartile ~1.2 h) and a *slow*
> espionage end (Equifax exfil over 76 days; low-throughput DNS-exfil by design).
> Together they set the **objective-execution dwell floor** — exfil "cannot go any
> faster" than human/throughput limits (the Sophos AAR argument,
> [`breach_reports_macro_timing`](breach_reports_macro_timing.md)) — and the
> fast↔slow range the group anchor must span.
> Source files (gitignored): `12_collection/2026 Unit 42 Global Incident Response
> Report…md`, `12_collection/Impacket and Exfiltration Tool…CISA.md`,
> `12_collection/bromiley2022_sans_bishopfox_hacker_survey.md`,
> `14_exfil/gao-18-559.md`, `14_exfil/1-s2.0-S0167404818304000-main.md`.

### Relevance class

**C** (calibration) — Tier-2 collection/exfil timing; the objective-execution
group's fast↔slow envelope + the throughput/human dwell floor.

### Used in lit review

Collection/exfil §4 timing rows (Step D, 2026-07-06); the objective-execution
group anchor + the exfil-floor argument (exfil is *not* substrate-instant).

## Bibliographic anchor

- **Citation keys**: `unit42_2026_girr` (Palo Alto Unit 42, *2026 Global Incident
  Response Report*); `cisa2022_impacket` (CISA/FBI/NSA, Alert AA22-277A, *Impacket
  & Exfiltration Tool … DIB Org*, 2022); `bromiley2022` (Bromiley/SANS + Bishop
  Fox, *Think Like a Hacker*, 2022 SANS Ethical Hacking Survey); `gao2018_equifax`
  (US GAO, *Data Protection: … 2017 Equifax Breach*, GAO-18-559); `nadler2019`
  (Nadler, Aminov, Shabtai, *Detection of Malicious and Low Throughput Data
  Exfiltration Over DNS*, Computers & Security 80, 2019).
- **Pages cited from**: Unit42 §"time-to-impact"; CISA §"Threat Actor Activity";
  Bromiley §"collect/exfil" figure; GAO §"How the Attack Occurred" (76 days,
  ~9,000 queries); Nadler §1–2 (low- vs high-throughput classes).

## Relevant artefacts

### The fast end — collect-and-exfil in ≤5 h; fastest quartile ~1.2 h

**Source locator:** Unit42 §"time-to-impact"; Bromiley collect/exfil figure

**Paraphrase:** [both fetched]
- **Unit 42 2026:** the **fastest 25% of intrusions reached exfiltration in 1.2
  hours** (down from 4.8 h the prior year); an AI-assisted attack simulation cut
  time-to-exfiltration to **25 minutes**. (MTTE ~2 days median across all
  intrusions — the fast quartile is the eCrime tail.)
- **Bromiley/SANS 2022:** **~64% of ethical-hacker respondents need ≤5 hours to
  collect and (potentially) exfiltrate data**; the distribution peaks at 1–5 h.
  (This is the Bromiley PRIMARY that [`ling2023`](ling2023.md) cited second-hand —
  closes the last open `[search]` in `12_collection`.)

**Maps to:** [`12_collection`](../../notes/ch3_design/tactic_profiles/12_collection.md) /
[`14_exfiltration`](../../notes/ch3_design/tactic_profiles/14_exfiltration.md) §4 (the fast eCrime
pole — hours, not instant).

**Disposition for this thesis:** verified [fetched] — Tier-2. Whole-activity
(collect+exfil) durations, the fast pole; not a per-tactic dwell.

---

### The slow end — Equifax 76-day exfil; low-throughput DNS exfil by design

**Source locator:** GAO Fig. + §"How the Attack Occurred"; CISA §"Threat Actor
Activity"; Nadler §1–2

**Paraphrase:** [all fetched]
- **GAO Equifax (GAO-18-559):** data extraction **extended over 76 days** (13 May
  → 29 Jul 2017), **~9,000 queries** across 51 databases, "in small increments to
  help avoid detection", using encrypted channels to blend in. The archetypal
  low-and-slow espionage exfil.
- **CISA Impacket (AA22-277A):** an APT performed **mailbox searches within a
  4-hour window** of access, but the *campaign* ran **mid-Jan → mid-Oct 2021**
  (Command Shell collection over 3 days, WinRAR into 3 MB chunks, CovalentStealer
  exfil over months) — collection is quick per-burst, exfil is paced over months.
- **Nadler 2019:** distinguishes **high-throughput DNS tunnelling** from
  **low-throughput exfil malware** (small data points — credentials, keylogging —
  sent slowly to evade). Low-throughput exfil is *slow by design*: a large dataset
  over a deliberately throttled channel converts data volume → a long stealth
  duration.

**Maps to:** [`14_exfiltration`](../../notes/ch3_design/tactic_profiles/14_exfiltration.md) §4 (the
slow espionage pole — days-to-months; the exfil *floor* is set by human/throughput
limits, and stealthy exfil deliberately extends it) and
[`12_collection`](../../notes/ch3_design/tactic_profiles/12_collection.md) §4 (collection bursts vs
paced exfil).

**Disposition for this thesis:** verified [fetched] — Tier-2. Per-case (Equifax)
and mechanism (Nadler); the slow pole. GAO's 76 days is a whole-exfil duration,
not a per-tactic rate; use for the range and the floor argument.

## Open questions / things to verify

- The fast↔slow spread (1.2 h → 76 days) is the objective-execution *range* the
  group anchor must span; the substrate's shape-not-scale means the *ratio*
  (exfil ≫ an exploit action) is what transfers, not the absolute days.
- Bromiley's exact percentiles (41% ≤2 h, 57% end-to-end <1 day per the manifest)
  live in chart images — the ~64% ≤5 h figure is in prose; treat the finer
  percentiles as `[parse-uncertain]` (chart) unless read off the source figure.

## Out of scope for this thesis

CISA's IOC/command detail and CovalentStealer reverse-engineering; GAO's
remediation/policy findings; Nadler's ML detection method (Isolation Forest);
Unit42's AI-threat narrative. Only the timing envelope is load-bearing.
