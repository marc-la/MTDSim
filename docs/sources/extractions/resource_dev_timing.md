# Resource-development timing — exploit-dev & infrastructure-prep lags (extraction notes)

> Five sources on **how long off-network preparation takes** — developing an
> exploit, and standing up attack infrastructure (domains) — extracted for
> [`02_resource-development`](../../notes/ch3_design/tactic_profiles/02_resource-development.md). All
> confirm the `prep-off-network` verdict: the timing spans *near-instant* (grab a
> published exploit; use a domain hours after registration) to *weeks* (median
> 0-day development) to *years* (vulnerability creation→disclosure), and **all of
> it happens before the simulator's clock starts**, so the in-sim dwell is a
> candidate for near-zero and the tactic is reset-immune to an in-network MTD.
> Source files (all `docs/sources/tactic_profiles/step_d/2_resource_dev/`,
> gitignored): `RAND_RR1751.md`, `20Sep_Bompos_Konstantinos.md`,
> `lidestri_vul_lifecycle_sam22.md`, `2068816.2068842.md`, `PhishingLandscape2021.md`.

### Relevance class

**C** (calibration) — Tier-2/3 off-network prep timing. Establishes the
*envelope* of resource-development duration and, more importantly, that it is a
pre-compromise dwell the on-network timeline does not meter.

### Used in lit review

Resource-development §4 gap-documenting rows (Step D, 2026-07-06); the
prep-off-network group boundary + near-zero-in-sim-dwell argument.

## Bibliographic anchor

- **Citation keys**: `rand2017` (Ablon & Bogart, *Zero Days, Thousands of
  Nights*, RAND RR-1751, 2017); `bompos2020` (Bompos, *Development Time of
  Zero-Day Cyber Exploits*, NPS thesis 2020); `lidestri2022` (Lidestri & Rowe,
  *Quantifying the Milestones of Cyber Vulnerabilities*, SAM'22); `hao2011` (Hao,
  Feamster, Pandrangi, *Monitoring the Initial DNS Behavior of Malicious
  Domains*, ACM IMC 2011); `interisle2021` (Aaron et al., *Phishing Landscape
  2021*, Interisle Consulting).
- **Pages cited from**: RAND — exec summary + longevity/dev-time sections
  (full-text 48k words, value sections read); Bompos §"Development Time"; Lidestri
  Results (Table 1); Hao Findings 4.1/5.2; Interisle §"Prevalence…" + reg-to-use
  charts.

## Relevant artefacts

### RAND 2017 — 22-day median exploit development; 6.9-year exploit life

**Source locator:** exec summary; "Life Expectancy"/"longevity" (avg 6.9 years);
dev-time ("median time of 22 days")

**Paraphrase:** the landmark study of a real 0-day arsenal [fetched]. Two anchors:
**(i) once an exploitable vulnerability is chosen, an exploit takes a median 22
days to develop** (range days–months); **(ii) a 0-day exploit's average life
expectancy is 6.9 years** before the underlying vulnerability is discovered/
patched. So *acquiring a capability* (Develop/Obtain Capabilities T1587/T1588)
is a weeks-scale off-network effort, and the capability, once held, is durable
for years.

**Quote:**
> "a median time of 22 days" (dev-time section)

**Maps to:** [`02_resource-development`](../../notes/ch3_design/tactic_profiles/02_resource-development.md)
§4 (the capability-development dwell — off-network, weeks-scale, precedes the
foothold) and §2 (confirms prep is a real but pre-clock activity).

**Disposition for this thesis:** verified [fetched] — Tier-2 empirical. An
*off-network* prep duration, so it bounds the real-world tail but supports a
near-zero *in-sim* dwell (the work is done before the simulator starts).

---

### Bompos 2020 — synthesis confirming the 22-day figure

**Source locator:** §"Development Time" (L220)

**Paraphrase:** an NPS thesis consolidating zero-day exploit-development-time
evidence; explicitly reports "**RAND Corporation in 2017 reported that … a median
time of 22 days**" and synthesises surrounding estimates [fetched]. Corroborates
`rand2017` as the citable dev-time anchor rather than adding an independent
number.

**Maps to:** [`02_resource-development`](../../notes/ch3_design/tactic_profiles/02_resource-development.md)
§4 (secondary confirmation of the 22-day capability-development dwell).

**Disposition for this thesis:** verified [fetched] — corroborating synthesis,
not an independent measurement.

---

### Lidestri 2022 — vulnerability lifecycle: exploit tracks disclosure within a day

**Source locator:** Results, Table 1 (∆cd, ∆dp, ∆de, ∆cp medians)

**Paraphrase:** models the four vulnerability-lifecycle durations over 10,912 OS
CVEs (NVD 2018–2021) [fetched]. Medians: **creation→disclosure 1,364 days
(~3.7 yr)**; **disclosure→patch −1 day** (most patched on/before disclosure);
**disclosure→exploit-published +1 day** (n=322); **longevity creation→patch 1,410
days (3.86 yr; Q1 665 d, Q3 2,600 d)**. Emergent point: exploits are
*perishable/transitory* (one-time capability, obsolescence once the vulnerability
is patched) — the flip side of RAND's 6.9-yr life. So *obtaining* a
published exploit is near-instant (tracks disclosure by ~a day), while the
vulnerability's own gestation is measured in years.

**Maps to:** [`02_resource-development`](../../notes/ch3_design/tactic_profiles/02_resource-development.md)
§4 (the *obtain-capability* path is fast — grab a published exploit ~1 day after
disclosure — vs RAND's *develop-capability* 22-day path; the two ends of the
resource-dev tempo).

**Disposition for this thesis:** verified [fetched] — Tier-2 empirical; a
lifecycle-of-the-vulnerability timing, adapted to the capability-acquisition
sub-tactic. Not APT dwell on the victim estate.

---

### Hao 2011 — malicious domains registered "just in time"; used within days

**Source locator:** Finding 4.1 (delay until attack); Finding 5.2 (initial lookup
trends)

**Paraphrase:** studies the DNS behaviour of attack domains from registration
[fetched]. **"More than 55% of the malicious domains appeared in spam campaigns
more than one day after they were registered"** (Finding 4.1); queries "increased
quickly after the domains were registered, and usually reached the peak in the
first **3–4 days**" (Finding 5.2). Miscreants "register these domains 'just in
time' before an attack" — infrastructure acquisition (Acquire Infrastructure
T1583) is a *hours-to-days* off-network activity.

**Maps to:** [`02_resource-development`](../../notes/ch3_design/tactic_profiles/02_resource-development.md)
§4 (infrastructure-prep dwell — domains stood up days before use; the fast,
agile end of resource-development) and [`13_command-and-control`](../../notes/ch3_design/tactic_profiles/13_command-and-control.md)
(domains that back C2).

**Disposition for this thesis:** verified [fetched] — Tier-2 empirical; a
registration→use lag (off-network), consistent with near-zero in-sim dwell.

---

### Interisle 2021 — 65% of phishing domains maliciously registered; used within the year

**Source locator:** §"Prevalence of Maliciously Registered Phishing Domains";
"Days from Domain Registration to Phishing" distribution charts

**Paraphrase:** of 497,949 phishing domains, **322,145 (65%) were *maliciously
registered*** (registered by the criminal, not compromised) [fetched];
"miscreants tend to use their domains within the first year of registration."
The registration→phishing distribution is heavily weighted to the first days
after registration (charted). The precise short-lag percentiles (the manifest's
"~50% within 48 h, 89% within 14 d") live only in the **chart image text, which
is garbled in the md — flag `[parse-uncertain]`; do not cite a specific
percentile without the source figure.**

**Maps to:** [`02_resource-development`](../../notes/ch3_design/tactic_profiles/02_resource-development.md)
§4 (corroborates Hao — attack infrastructure is registered shortly before use;
off-network, days-scale).

**Disposition for this thesis:** verified [fetched] for the 65%-maliciously-registered
figure and the qualitative "used within days/first year"; **`[parse-uncertain]`**
for the exact reg-to-use percentiles (chart only).

## Open questions / things to verify

- Every figure here is an **off-network** prep duration — it bounds the
  real-world tail (weeks for dev, days for infra, years for the vulnerability)
  but does *not* set an in-sim dwell, because resource-development precedes the
  foothold and the simulator's clock. The catalogue verdict it supports is
  near-zero in-sim dwell + reset-immunity, not a transplanted number.
- Interisle's exact reg-to-use percentiles need the original PDF figure to cite
  precisely (chart-text garbled in md).

## Out of scope for this thesis

RAND's zero-day-stockpiling policy discussion; Lidestri's per-OS patch-behaviour
comparison and Weibull-fit parameters; Hao's DNS-based *detection* features
(the paper's main contribution); Interisle's WHOIS-policy / TLD-registrar
advocacy. None bear on tactic dwell.
