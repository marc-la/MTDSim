# Worm / self-propagation rate models — the fast end of lateral movement (extraction notes)

> A consolidated bundle of **self-propagating-malware propagation-rate models and
> measurements**, extracted for [`11_lateral-movement`](../../notes/ch3_design/tactic_profiles/11_lateral-movement.md).
> They establish the **fast-worm end** of lateral movement's bimodal character
> (automated scan-based spread in *seconds-to-minutes*), against which the
> **slow-manual APT** end contrasts — the widened fast↔slow range the profile
> already flags. Also covers the **MTD address-mutation counter to worm spread**
> (cross-refs [`mtd_scan_disruption`](mtd_scan_disruption.md)) and worm
> *containment* (the reset/rate-limit mechanism).
> Source files (all `docs/sources/tactic_profiles/step_d/11_lat_movement/`,
> gitignored): `Inside_the_Slammer_worm.md`, `586110.586130.md` (Zou Code Red),
> `staniford2002_own_the_internet_usenix.md`, `chen2003_aawp_infocom.md`,
> `antonakakis2017_mirai_usenix.md`, `chernikova2023_siidr_epidemiological_ans.md`,
> `shin2012_conficker_empirical_tifs.md`, `zhang2015_conficker_hybrid_epidemics_plos.md`,
> `sellke2008_worm_containment_tdsc.md`, `rohloff2005_random_constant_scanning_worms_icccn.md`,
> `zou2003_monitoring_early_warning_worms_ccs.md`, `chenji2009_network_aware_malware_arxiv.md`,
> `alshaer2012_random_host_mutation_securecomm.md`, `2342441.2342467.md` (Jafarian
> OpenFlow-RHM), `1-s2.0-S0167739X26003109-main.md` (Ma, cloud-native MTD).

### Relevance class

**C** (calibration) — Tier-2 propagation-rate observables for the fast-worm end;
plus **M** (MTD-vs-worm mechanism). No per-tactic APT dwell; the *shape* (worm
spread is seconds-to-minutes; APT lateral is manual and slow).

### Used in lit review

Lateral-movement §4 (the fast-worm rate anchors + the fast↔slow bimodal range);
§3 (address-mutation defeats scan-based spread — cross-ref mtd_scan_disruption).

## Bibliographic anchor

- **Citation keys**: `moore2003_slammer`, `zou2002_codered`, `staniford2002`,
  `chen2003_aawp`, `antonakakis2017_mirai`, `chernikova2023`, `shin2012_conficker`,
  `zhang2015_conficker`, `sellke2008`, `rohloff2005`, `zou2003_earlywarning`,
  `chenji2009`, `alshaer2012_rhm`, `jafarian2012_ofrhm`, `ma2026_cloudnative`.
- **Pages cited from**: each source's abstract + headline-rate section.

## Relevant artefacts

### The fast-worm rate anchors — seconds to minutes

**Source locator:** Slammer §"propagation speed"; Zou/Sellke Code Red;
Staniford §4; Chen §1; Antonakakis Abstract; Chernikova/Shin Abstracts

**Paraphrase:** [all fetched] automated scan-based self-propagation is *fast*:
- **Slammer 2003 (Moore):** the fastest worm in history — **infected >90% of
  vulnerable hosts within 10 minutes**; hit full scanning rate (55M scans/s) in
  ~3 min; two orders of magnitude faster than Code Red. ~75,000 hosts.
- **Code Red 2001 (Zou two-factor model; Sellke):** 359,000 hosts, **~37-minute
  population doubling**; >359,000 machines in <14 h. Zou's *two-factor worm model*
  (epidemic + human countermeasures + congestion) fits the observed curve.
- **Staniford 2002 ("Own the Internet"):** projects, from Code Red data, a
  **Warhol worm** (hit-list + permutation scanning) infecting most/all vulnerable
  "in a few minutes to perhaps an hour", and a **flash worm** in "**10s of
  seconds: so fast that no human-mediated counter-response is possible**."
- **Chen 2003 (AAWP):** discrete-time analytical model for random-scanning worms;
  active worms "can spread across the Internet within seconds."
- **Mirai 2017 (Antonakakis):** **~65,000 IoT devices in the first 20 hours**,
  steady state 200k–300k, peak **600k** over 7 months (Telnet-scan, default
  passwords).
- **Conficker (Shin 2012 / Zhang 2015):** ~7–15M (25M analysed) infected from Nov
  2008; NetBIOS + domain-generation-algorithm; hybrid 3-mode spread.
- **Chernikova 2023 (SIIDR):** a Susceptible-Infected-InfectedDormant-Recovered
  model fit to **15 WannaCry traces** — derives transition rates, outperforms
  SI/SIS/SIR (adds a *dormant* state, matching stealthy self-propagation).

**Maps to:** [`11_lateral-movement`](../../notes/ch3_design/tactic_profiles/11_lateral-movement.md) §4
(the fast-worm end — automated spread is minutes/seconds; the *modality* the
substrate's fast lateral-exploit can proxy) and §2 (the fast pole of the
fast↔slow bimodal range the profile flags).

**Disposition for this thesis:** verified [fetched] — Tier-2. These are *Internet
worm* propagation rates (opportunistic, scan-based), the fast end; APT lateral
movement is manual and slow (the other pole). The bimodal *shape* is the finding,
not a transplanted rate.

---

### Worm containment + MTD-mutation counter — the reset/rate-limit mechanism

**Source locator:** Sellke §3 (branching process; containment cycle); Rohloff
(Markov jump process); Zou 2003 (Kalman early-warning); Al-Shaer/Jafarian RHM;
Ma cloud-native MTD

**Paraphrase:** [all fetched]
- **Sellke 2008:** a stochastic *branching-process* model of early-phase spread —
  it is the **total scans M over a "containment cycle" (weeks)**, not the
  instantaneous rate, that decides whether a worm spreads; capping M (e.g. 10,000
  scans/host) holds Code Red to <360 infected (0.1%). Rohloff (density-dependent
  Markov jump process) and Zou 2003 (Kalman-filter early warning) are companion
  rate-estimation models.
- **Al-Shaer 2012 / Jafarian 2012 (OpenFlow-RHM):** address-mutation MTD vs
  scanning worms — at a modest mutation rate, scanners find **<1% valid addresses**
  (the worm's scan-based target discovery is invalidated — same mechanism as
  [`mtd_scan_disruption`](mtd_scan_disruption.md), applied to lateral spread).
- **Ma 2026 (cloud-native):** selective MTD placement raises attack difficulty
  against lateral movement in cloud-native environments.

**Maps to:** [`11_lateral-movement`](../../notes/ch3_design/tactic_profiles/11_lateral-movement.md) §3
(an address/topology shuffle invalidates a *scan-based* worm's target discovery →
strong reset for the fast-worm modality; weaker against credential-based manual
movement — the reset is per-modality, cf. [`evans2011_mtd_effectiveness`](evans2011_mtd_effectiveness.md)).

**Disposition for this thesis:** verified [fetched] — §3 mechanism (mutation
defeats scan-based spread) + containment (rate-limit). Models/measurements, not
APT dwell.

## Open questions / things to verify

- These are *Internet worms*, not APT lateral movement — the transferable finding
  is the **bimodal shape** (automated scan-spread = minutes/seconds vs manual APT
  = slow) and the **per-modality reset** (mutation kills scan-based spread, not
  credential-based). Absolute worm rates are not an APT lateral dwell.
- `2342441.2342467.md` (Jafarian OpenFlow-RHM) duplicates `p127.md` — same paper.

## Out of scope for this thesis

Worm *detection*/early-warning system design (Zou 2003, Chen monitoring); Mirai
DDoS-victim analysis and IoT-ecosystem commentary; Conficker blacklist-evaluation;
the epidemiological stability proofs. Only the propagation-rate shape and the
MTD/containment mechanism are load-bearing.
