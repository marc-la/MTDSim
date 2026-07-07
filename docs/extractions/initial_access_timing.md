# Initial-access timing empirics — entry tempo + the TTC distribution caveat (extraction notes)

> Three sources on **how fast the first foothold lands** and — load-bearing for
> the whole timed-model layer — **what distribution time-to-compromise actually
> follows**. Extracted for [`03_initial-access`](../tactic_profiles/03_initial-access.md).
> Holm's finding that the exponential/Poisson TTC assumption is empirically a poor
> fit is a caveat that reaches every SPN/CTMC declared-rate model in the corpus
> (Bland, Rodríguez, the substrate's own exponential exploit timing).
> Source files (all `docs/sources/tactic_profiles/step_d/3_initial_access/`,
> gitignored): `2024-dbir-data-breach-investigations-report.md`,
> `How Low Can You Go_ … Time-to-Exploit Trends _ Google Cloud Blog.md`,
> `A_Large-Scale_Study_of_the_Time_Required_to_Compromise_a_Computer_System.md`.

### Relevance class

**C** (calibration) + **M** (method caveat). DBIR/Mandiant are Tier-2 empirical
entry-tempo anchors; Holm is a distribution-shape caveat for the declared-rate
method.

### Used in lit review

Initial-access §4 timing rows (Step D, 2026-07-06); the method note's
"declared rates are the field norm" caveat gains an empirical counter-point
(exponential is a poor TTC fit).

## Bibliographic anchor

- **Citation keys**: `dbir2024` (Verizon, *2024 Data Breach Investigations
  Report*); `mandiant_tte2023` (Charrier/Weiner, Mandiant, *How Low Can You Go?
  2023 Time-to-Exploit Trends*, Google Cloud blog 2024); `holm2014` (Holm, *A
  Large-Scale Study of the Time Required to Compromise a Computer System*, IEEE
  TDSC 11(1), 2014).
- **Pages cited from**: DBIR phishing figure (median-time-to-click); Mandiant
  §"Time-to-Exploit"; Holm Abstract + §5.2 (TTFC/TBC distribution fits).

## Relevant artefacts

### DBIR 2024 — phishing click in 21 seconds

**Source locator:** phishing section figure ("21 seconds … median time to click;
28 seconds … time to data entry after click")

**Paraphrase:** for a user who falls for a phish, the **median time to click is
21 seconds**, plus **28 seconds to enter data** after the click — i.e. the
human-triggered entry vector, *once the lure lands*, resolves in under a minute
[fetched]. This bounds the *fast* end of the phishing initial-access path and
sharpens §2's "delivery-wait" caveat: the wait is for the lure to *reach* a
willing user, not for the click itself.

**Maps to:** [`03_initial-access`](../tactic_profiles/03_initial-access.md) §4
(phishing entry is near-instant once delivered; the low-and-slow part is the
pre-delivery wait, not the metered action).

**Disposition for this thesis:** verified [fetched] — Tier-2 empirical; a
per-victim click latency, not a per-tactic dwell.

---

### Mandiant 2023 (TTE) — time-to-exploit collapsed 63 → 5 days

**Source locator:** §"Time-to-Exploit"

**Paraphrase:** average **time-to-exploit (TTE)** — the gap between a
vulnerability and its exploitation — fell across editions: **2018–19 = 63 days →
2020–21 = 44 → 2021–22 = 32 → 2023 = 5 days** (47 with outliers retained)
[fetched]. In 2023 the n-day : zero-day ratio shifted to **30:70** (70% first
exploited as zero-days); n-day exploitation is "most likely to occur before the
end of the first month following a patch." So the exploit-shaped entry window is
compressing toward *days*, and attackers "move quickly enough to beat patching
cycles."

**Maps to:** [`03_initial-access`](../tactic_profiles/03_initial-access.md) §4
(the exploit-shaped entry timescale — days from disclosure, and increasingly
zero-day-first) and [`02_resource-development`](../tactic_profiles/02_resource-development.md)
(n-day windows). Complements Durumeric's 24–48 h *scan*-onset
([`internet_scanning_empirics`](internet_scanning_empirics.md)).

**Disposition for this thesis:** verified [fetched] — Tier-2 vendor telemetry.
A disclosure→exploit lag (an entry-window bound), not a per-tactic dwell.

---

### Holm 2014 — TTC is heavy-tailed (Pareto/lognormal), not exponential; and it *decreases*

**Source locator:** Abstract; §5.2.1 (TTFC — Pareto best fit); §5.2.2 (TBC —
exponential poor); §5.3 (TTC decreases with intrusions)

**Paraphrase:** the largest empirical TTC study in the corpus — **203,025
intrusions across 261,757 systems** (2009–2012) [fetched]. Two load-bearing
findings:
- **The exponential/Poisson assumption is a poor fit.** The **Pareto**
  distribution best fits *time-to-first-compromise*; **lognormal** best fits the
  intrusion count and time-between-compromises; **exponential is a poor choice**
  for TBC/overall TTC (it fails to model the heavy tail where days > 80). ~90% of
  first-compromises occur within ≤400 days; ~90% of time-between-compromises
  within <180 days.
- **TTC *decreases* with each successive intrusion** — a compromised system is
  compromised *faster* next time (contrary to "learn from mistakes"): once a
  system is exposed/soft, re-compromise accelerates.

**Emergent (method-level):** this is a direct empirical challenge to the
**exponential-rate assumption** that SPN/CTMC attacker models — and the
substrate's own exponential exploit timing — are built on. It doesn't invalidate
declare-and-sweep (the field norm), but it says the *distribution shape* the
sweep should explore is heavy-tailed, not memoryless.

**Maps to:** [`03_initial-access`](../tactic_profiles/03_initial-access.md) §4
(entry-time distribution — heavy-tailed) and §2; the method note
([`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md))
— a caveat that declared *exponential* rates are empirically suspect;
[`06_privilege-escalation`](../tactic_profiles/06_privilege-escalation.md)
(TTC-lineage).

**Disposition for this thesis:** verified [fetched] — Tier-2 empirical, the
strongest TTC-distribution evidence available. **Contrast:** flags the exponential
assumption as suspect (a claim to resolve with Marc, not to act on unilaterally —
the substrate's exponential timing is inherited D7/C7, out of Step-D scope).

## Open questions / things to verify

- Holm's "TTC decreases with intrusions" is measured on an enterprise
  malware-alarm dataset (opportunistic, not APT-targeted) — the heavy-tail and
  decrease shapes are the transferable finding, not the absolute day-counts.
- Whether to let Holm's heavy-tail finding influence the *sweep distribution*
  (vs the substrate's inherited exponential) is a decision for Marc — flagged,
  not actioned (D5/C7 substrate-timing is read-only here).

## Out of scope for this thesis

DBIR's breach-pattern taxonomy and industry breakdowns; Mandiant's per-vendor
CVE detail and threat-actor attribution; Holm's goodness-of-fit statistics (AIC
tables) and the dependable-computing distribution-theory survey. None set a
tactic dwell.
