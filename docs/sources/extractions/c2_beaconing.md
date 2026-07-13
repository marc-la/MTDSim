# Command-and-control beaconing — check-in cadence + the partial reset (extraction notes)

> Sources on the **C2 beacon cadence** (how often malware calls home) and the
> **MTD switch-timing** decision, extracted for
> [`13_command-and-control`](../../notes/ch3_design/tactic_profiles/13_command-and-control.md). C2's
> timing character *is* the beacon interval — a tunable low-and-slow spacing from
> **seconds to hours** — and its §3 reset is **partial** (proxies/CDN-fronting give
> resiliency; already flagged in [`breach_reports_macro_timing`](breach_reports_macro_timing.md)
> / Selmanaj Step-C).
> Source files (gitignored): `13_c2/cobalt-strike-malleable-c2-profile.md`,
> `13_c2/zhang2023_beaconing_campus_acsac.md`,
> `0_cross_tactic_timed_models/BAYWATCH_…md`, `9_cred_access/2002.10390v1.md`
> (Li, Shen, Zheng — also credential-access).

### Relevance class

**C** (calibration) — the beacon-interval range that characterises C2 dwell +
**M** (MTD switch-timing mechanism). Tier-2/3.

### Used in lit review

C2 §4 (beacon cadence) + §3 (MTD switch-timing; partial reset); the
stealth-low-and-slow group (C2 is a namesake member).

## Bibliographic anchor

- **Citation keys**: `unit42_2021_cobaltstrike` (Sangvikar et al./Unit 42,
  *Cobalt Strike: How Malleable C2 Profiles Make it Difficult to Detect*, 2021);
  `zhang2023_beaconing` (Zhang et al., *Aggregation-based Beaconing Detection
  across Large Campus Networks*, ACSAC'23); `hu2016_baywatch` (Hu, Jang,
  Stoecklin et al., *BAYWATCH: Robust Beaconing Detection*, IEEE/IFIP DSN'16);
  `li2020_stmtd` (Li, Shen, Zheng, *Spatial-Temporal MTD: A Markov Stackelberg
  Game Model*, AAMAS 2020; arXiv:2002.10390).
- **Pages cited from**: Cobalt Strike §"Global options" (sleeptime/jitter);
  Zhang Abstract; BAYWATCH Abstract + §II (interval range); Li Abstract.

## Relevant artefacts

### Beacon cadence — seconds to hours, tunable (Cobalt Strike; BAYWATCH; Zhang)

**Source locator:** Cobalt Strike §"Global options"; BAYWATCH §II; Zhang Abstract

**Paraphrase:** [all fetched] C2's timing character is the periodic beacon:
- **Cobalt Strike (Unit 42 2021):** Beacon's **`sleeptime` + `jitter`** set the
  check-in frequency; the default profile example is **`sleeptime 30000` (30 s)
  with `jitter 20`** (±20%). Attackers customise sleeptime *up* to be quieter, so
  the cadence is a tunable stealth dial.
- **BAYWATCH (Hu 2016):** measured over 30 B+ web-proxy events / 130 k devices /
  5 months — **beaconing observed "every 2–3 seconds as well as every 2 hours or
  even longer"**; "the frequency depends on the attacker's strategy, slow-and-
  stealthy or fast-and-aggressive." The empirical beacon-interval range.
- **Zhang 2023:** over **75 billion connections** (10 months, 2 campus networks);
  "over **90% of malware families manifest periodic behavior**" — beacons are
  "pre-programmed … regularly connect." C2 is *characteristically periodic*, and
  the period is the low-and-slow spacing.

**Maps to:** [`13_command-and-control`](../../notes/ch3_design/tactic_profiles/13_command-and-control.md)
§4 (the C2 dwell *is* the beacon interval — seconds to hours, a tunable
stealth-low-and-slow spacing → Tier-3 declared, wide sweep across the range) and
§2 (C2 is periodic by design).

**Disposition for this thesis:** verified [fetched] — Tier-2 measurement + the
tool's own config. The beacon *interval* is a real, tunable timing character; the
substrate models a C2 *state*, so the interval informs its dwell range, not a point.

---

### Li, Shen & Zheng 2020 — MTD switch-timing vs a persistent C2/foothold

**Source locator:** Abstract; §1 (spatial-temporal MTD)

**Paraphrase:** a Markov Stackelberg game for MTD where the defender chooses both
the **sequence of configurations** and the **optimal timing to switch** [fetched].
Key parameters: a **switching cost** (depends on current + next config) and
**config-dependent attacker exploit times** (different configs take different
amounts of time to exploit). Confirms the C2/persistence §3 lever: the *reset
interval* is the optimised quantity, traded against switch cost — the same
FlipIt-family ratio as [`persistence_reset_models`](persistence_reset_models.md).

**Maps to:** [`13_command-and-control`](../../notes/ch3_design/tactic_profiles/13_command-and-control.md)
§3 (a config switch contests C2, but with a cost; the reset interval is the sweep
axis) and [`09_credential-access`](../../notes/ch3_design/tactic_profiles/09_credential-access.md)
(config-dependent exploit times).

**Disposition for this thesis:** verified [fetched] — §3 switch-timing mechanism.
Game-theoretic, not a dwell; the C2 reset is partial + rate-dependent (proxies
survive — see the Step-C selmanaj finding).

## Open questions / things to verify

- The beacon interval (2 s–2 h+) is the C2 *dwell character*, but the substrate
  models C2 as a state, not a packet stream — the interval bounds the *range* of
  the C2 dwell, not a value to transplant.
- C2 reset is **partial** (Selmanaj/M-Trends: proxies/CDN-fronting give
  "resiliency in the face of connection loss") — so §3 declares a *partial* reset
  + wide sweep, corroborated by Li et al.'s switch-cost trade-off.

## Out of scope for this thesis

Beaconing *detection* algorithms (BAYWATCH's 8-step filter, Zhang's time-series
periodicity, self-training/active-learning); Cobalt Strike's HTTP-indicator
evasion detail; Li et al.'s relative-value-iteration solver. Only the cadence and
the switch-timing mechanism are load-bearing.
