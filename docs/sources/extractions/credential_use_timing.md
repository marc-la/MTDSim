# Credential-use & service-exposure timing (extraction notes)

> A consolidated bundle on **how fast a captured/exposed credential is used**, and
> **how fast an exposed service is compromised** — extracted for
> [`09_credential-access`](../../notes/ch3_design/tactic_profiles/09_credential-access.md) §4 (and
> [`03_initial-access`](../../notes/ch3_design/tactic_profiles/03_initial-access.md), which shares the
> Valid-Accounts entry vector). Two sub-clusters: (a) leaked-credential honeypots
> (time-to-use of a stolen credential); (b) exposed-service honeypots
> (time-to-compromise of an internet-facing service). Both say the same thing — a
> credential/service, once exposed, is used in **seconds to hours**, and the
> credential-theft *act* is fast; the low-and-slow is elsewhere.
> Source files (all `docs/sources/tactic_profiles/step_d/9_cred_access/`,
> gitignored): `2987443.2987475.md`, `s40163-018-0092-6.md`,
> `sensors-25-03676.md`, `deblasio2017_tripwire_imc.md`,
> `bursztein2014_manual_hijacking_imc.md`, `oest2020_sunrise_to_sunset_usenix.md`,
> `akiyama2018_honeycirculator_ijis.md`, `unit42_2021_exposed_services_public_clouds_blog.md`,
> `sophos_2019_cloud_honeypots_press_wayback.md`, `sans_isc_survival_time_2026-07-06.md`.

### Relevance class

**C** (calibration) — Tier-2 empirical time-to-use / time-to-compromise. Fast-end
anchors; the credential/access act is quick, not a dwell.

### Used in lit review

Credential-access / initial-access §4 timing rows (Step D, 2026-07-06); the
"credential-access is exploit-shaped, and its theft-of-material variants are
faster than an exploit" argument.

## Bibliographic anchor

- **Citation keys**: `bursztein2014` (Bursztein et al., *Handcrafted Fraud and
  Extortion: Manual Account Hijacking*, IMC'14); `onaolapo2016` (Onaolapo,
  Mariconti, Stringhini, *What Happens After You Are Pwnd*, IMC'16);
  `bermudez2018` (Bermudez Villalva et al., *Under and over the surface*, Crime
  Science 7:17, 2018); `rabzelj2025` (Rabzelj et al., *Beyond the Leak*, Sensors
  25(12):3676, 2025); `deblasio2017` (DeBlasio et al., *Tripwire*, IMC'17);
  `oest2020` (Oest et al., *Sunrise to Sunset*, USENIX Sec'20); `akiyama2018`
  (Akiyama et al., *HoneyCirculator*, IJIS 17(2), 2018); `unit42_2021_exposed`
  (Jay Chen/Unit 42, *Exposed Services in Public Clouds*, 2021); `sophos2019`
  (Boddy/Sophos, *Cyberattacks on Cloud Honeypots*, 2019); `sans_isc_survival`
  (SANS ISC, *Survival Time*, live metric).
- **Pages cited from**: each source's abstract + headline-figure section.

## Relevant artefacts

### Leaked-credential honeypots — a stolen credential is used in minutes-to-hours

**Source locator:** Bursztein §"decoy credentials"; Onaolapo Abstract; Oest
Abstract + §"Golden Hour"; DeBlasio Abstract; Bermudez/Rabzelj/Akiyama Abstracts

**Paraphrase:** [all fetched]
- **Bursztein 2014 (manual hijacking):** with decoy credentials in phishing pages,
  **criminals accessed 20% of accounts within 30 minutes**; once logged in, they
  spend **~3 minutes profiling** the account before exploiting. Manual hijacking is
  rare (9 per million users/day) but fast once it happens.
- **Oest 2020 (phishing lifecycle):** the average phishing campaign spans **21
  hours** (first→last victim); detection ~9 h after first victim, +7 h to peak
  mitigation ("golden hours"); **7.42% of victims** are compromised.
- **Onaolapo 2016 / Bermudez 2018:** 100 Gmail honey accounts leaked via paste
  sites / forums / malware (Onaolapo, 7-month monitor) and on the Dark Web
  (Bermudez); use *taxonomy* varies by outlet (malware-sourced criminals more
  evasive — Tor, spoofed UA), Dark-Web identity price ~£820.
- **DeBlasio 2017 (Tripwire):** honey accounts at >2,300 sites detected **19 site
  compromises over a year** via password-reuse logins — days-to-attacker-login
  varies widely per site.
- **Rabzelj 2025:** 27 B leaked credentials (~4 B unique) vs 39 honeypots/1 yr —
  nuance: **leaked-dump credentials only *partially* surface in real attacks**;
  attackers lean on wordlists/default-lists (Nmap, Mirai) more than breach dumps.
- **Akiyama 2018 (HoneyCirculator):** ~1-yr monitoring of bait credentials through
  the exploit→credential-collection→fraud cycle.

**Maps to:** [`09_credential-access`](../../notes/ch3_design/tactic_profiles/09_credential-access.md)
§4 (theft-of-material variants run in minutes — the "faster than an exploit"
claim, empirically; the low-and-slow is the campaign around it, not the credential
use) and [`03_initial-access`](../../notes/ch3_design/tactic_profiles/03_initial-access.md) (phishing
21 h lifecycle).

**Disposition for this thesis:** verified [fetched] — Tier-2. Time-to-use of a
credential (fast), not a per-tactic dwell. Rabzelj tempers the "leaked creds =
instant attacks" intuition.

---

### Exposed-service honeypots — an internet-facing service is compromised in seconds-to-hours

**Source locator:** Unit42 §"findings"; Sophos press headline; SANS ISC live
metric

**Paraphrase:** [all fetched]
- **Unit 42 2021:** **80% of 320 honeypots compromised within 24 h, all within a
  week**; SSH most attacked (avg **26 compromises/day**, 169 max); **one actor
  compromised 96% of 80 Postgres honeypots within 30 seconds** — "attackers find
  and compromise in minutes."
- **Sophos 2019:** first attack within **52 seconds** of exposure; ~**13 login
  attempts/min** per honeypot.
- **SANS ISC Survival Time:** a live metric of the average time an exposed,
  unpatched host stays uncompromised — minutes-to-hours on well-targeted networks
  (dated snapshot; exact value network-dependent, `[parse-uncertain]` for a
  specific figure — read the live gauge, not a garbled number).

**Maps to:** [`09_credential-access`](../../notes/ch3_design/tactic_profiles/09_credential-access.md) /
[`03_initial-access`](../../notes/ch3_design/tactic_profiles/03_initial-access.md) §4 (brute-force /
default-credential entry against an exposed service is seconds-to-hours — the fast
exploit-shaped end).

**Disposition for this thesis:** verified [fetched] — Tier-2. Time-to-compromise
of an *exposed* service (opportunistic, internet-facing), not an APT's paced
credential access on an internal estate; the *shape* (fast when exposed) is the
finding.

## Open questions / things to verify

- All are opportunistic / internet-facing measurements (honeypots, phishing) — the
  fast time-to-use/compromise is the *modality* (credential theft/abuse is quick),
  not an APT internal-estate dwell. The mapping to the in-sim credential-access
  state is by modality, not a transplanted number.
- SANS survival-time exact value is a live, network-dependent gauge — cite the
  metric, not a fixed number.

## Out of scope for this thesis

The malicious-use *taxonomies* (spam/financial/espionage splits); Dark-vs-Surface
behavioural differences; Tripwire/HoneyCirculator detection methodology; Rabzelj's
password-composition and generative-algorithm analysis. Only the timing shape is
load-bearing.
