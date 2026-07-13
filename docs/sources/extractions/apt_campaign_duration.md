# APT campaign duration — decade-long landscape (extraction notes)

> One source, extracted **as a cross-tactic whole-campaign duration bound** — it
> prices the *outermost envelope* the emergent timeline must be able to span, not
> a per-tactic dwell. Feeds the persistence/objective tactics' §4
> ([`05_persistence`](../tactic_profiles/05_persistence.md),
> [`06_privilege-escalation`](../tactic_profiles/06_privilege-escalation.md),
> [`14_exfiltration`](../tactic_profiles/14_exfiltration.md),
> [`15_impact`](../tactic_profiles/15_impact.md)) as the espionage long-and-slow
> counterpart to the fast ransomware envelope ([`ransomware_timing`](ransomware_timing.md)).
> Source file: `docs/sources/tactic_profiles/step_d/5_persist/2509.07457v2.md`
> (gitignored).

### Relevance class

**C** (calibration) — Tier-2 macro observable; the whole-campaign duration
distribution across a decade of APT dossiers.

### Used in lit review

Persistence/privesc/exfil/impact §4 campaign-duration rows (Step D, 2026-07-06);
the operational-validation plausibility envelope (the outer bound the timeline
must reach for espionage actors).

## Bibliographic anchor

- **Citation key**: `yuldoshkhujaev2025`
- **DOI / URL**: https://doi.org/10.1145/3719027.3765085 (ACM CCS 2025;
  arXiv:2509.07457)
- **Pages cited from**: Abstract; §1 (findings ③); §4 (common traits — duration).

## Relevant artefacts

### APT campaign duration: 1 day to ~5 years, 137 days on average

**Source locator:** Abstract; §1 finding ③; §4 (concealment traits)

**Paraphrase:** a longitudinal analysis of a decade of public APT dossiers (154
countries, 446 threat actors) [fetched]. The load-bearing figure: "**APT campaign
duration varies widely, from a single day to nearly five years (137 days on
average)**" — the whole-intrusion lifetime distribution for *espionage-class*
actors, complementing M-Trends' 122 d / 400 d tails
([`breach_reports_macro_timing`](breach_reports_macro_timing.md)). Two supporting
findings: many APT attacks "do not need to rely on zero-day vulnerabilities"
(n-day/known-vuln entry is the norm — echoes Ussath via
[`alshamrani2019`](alshamrani2019.md)); and APT activity "frequently coincided
with political events … indicating that attackers had already performed target
reconnaissance and were waiting for an opportune time to act" — direct evidence
of the *patient-wait* persistence character (recon done, foothold held, action
deferred).

**Maps to:** [`05_persistence`](../tactic_profiles/05_persistence.md) §4
(campaign-duration envelope — the foothold is held for a 137-day mean, up to
years; the reset-survivor character quantified) and §2 (patient-wait);
privesc/exfil/impact §4 (the same whole-campaign bound caps the summed dwell).

**Disposition for this thesis:** verified [fetched] — Tier-2 macro, the largest
longitudinal APT-duration dataset in the corpus. A whole-campaign lifetime, **not
a per-tactic dwell** — it sets the *outer* plausibility bound (espionage end)
the operational-validation timeline must be able to reach, against which the
group anchors are checked.

## Open questions / things to verify

- "137 days on average" is a whole-campaign duration estimated from public
  dossiers (reporting/estimation bias toward discovered, documented campaigns) —
  a *shape* bound (the espionage tail exists and is months-to-years), not a scale
  to transplant. Consistent with M-Trends 122 d espionage median.

## Out of scope for this thesis

Victim-country / target-sector / threat-actor attribution analysis; the CVE
severity and YARA/CTI-record statistics; the political-event correlation study;
the LLM-assisted dossier-mining methodology. Only the duration distribution is
load-bearing here.
