# CISA AA24-038A (Volt Typhoon) — extraction notes

> Joint Cybersecurity Advisory **AA24-038A**, *PRC State-Sponsored Actors Compromise and Maintain Persistent Access to U.S. Critical Infrastructure*. Authoring agencies: CISA, NSA, FBI, with DOE, EPA, TSA, ASD's ACSC, CCCS, NCSC-UK, NCSC-NZ. First published 8 February 2024.
> Source file: `docs/sources/advisories/cisaaa24038a.md` (gitignored; captured from the ASD's ACSC republication — cisa.gov returns HTTP 403 to automated retrieval).
> Relevance to this thesis: the **latest-slot APT evidence** for ch3 §3.1.1 (GAP G5 — long dwell, objective-driven pacing, living-off-the-land) and the **sole source** for the hand-curated Attack Flow at [`../../../data/gap/hand_curated/`](../../../data/gap/hand_curated/).

## Bibliographic anchor

- **Citation key**: `cisaaa24038a`
- **DOI / URL**: https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a (grey literature; no DOI)
- **Advisory identifier**: AA24-038A (canonical for CISA alerts)
- **Version / date cited from**: first published 8 February 2024; ATT&CK mapping is against **ATT&CK v14** (advisory's own note)

## Extraction policy

Quote sparingly, paraphrase liberally; each excerpt sits under copyright fair use. Quoted material in `>` blocks with a locator; paraphrase preferred; every mapped extract carries a `→` cross-link.

## Relevant artefacts

### Relevance class

**L — Load-bearing.** This is the primary evidence for the ch3 §3.1.1 "latest" APT slot, and the source from which a faithful Attack Flow was hand-authored. It is grey literature (a government advisory), not a peer-reviewed paper: cite it for *what a well-documented APT campaign looks like at technique resolution and on what timescale*, not as an analytic claim about MTD.

---

### Concept 1 — The intrusion lifecycle as a stated, ordered backbone

**Source locator:** "Overview of Activity"; "Observed TTPs" (Reconnaissance → Command and Control).

**Paraphrase:** The advisory narrates a single "typical" behavioural pattern the agencies observed across multiple confirmed compromises, with explicit ordering. Volt Typhoon conducts extensive pre-compromise reconnaissance; gains initial access by exploiting known or zero-day vulnerabilities in public-facing appliances (Fortinet, Ivanti, NETGEAR, Citrix, Cisco), and *then* connects over VPN for follow-on activity; obtains administrator credentials (priv-esc vulnerabilities, or credentials insecurely stored on the appliance); uses valid administrator credentials to move laterally to the domain controller over RDP; and achieves full domain compromise by extracting the Active Directory database. The NTDS.dit extraction is given as an ordered procedure: move laterally to the DC via RDP; execute `vssadmin` to create a volume shadow copy; use WMIC/`ntdsutil` to copy NTDS.dit and the SYSTEM hive from the shadow copy; and exfiltrate both to crack offline. Elevated credentials are then used to reach OT-adjacent assets.

**Quote (if essential):**

> "Volt Typhoon typically gains initial access to the IT network by exploiting known or zero-day vulnerabilities in public-facing network appliances … and then connects to the victim's network via VPN for follow on activities." (Overview of Activity)

> "Volt Typhoon achieves full domain compromise by extracting the Active Directory database (NTDS.dit) from the DC." (Overview of Activity)

**Maps to:** [`../../../data/gap/hand_curated/`](../../../data/gap/hand_curated/) — this backbone is the flow's stated spine (edge ledger `kind: stated`); [`../../implementation/pipeline/gap/gap_schema.md`](../../implementation/pipeline/gap/gap_schema.md) §c (per-flow extract).

**Disposition for this thesis:** adopted as the evidence artefact's source. The advisory carries *more* explicit inter-technique ordering than most CTID corpus source reports — which is why a faithful flow could be built from it at all — yet still leaves 16 of 73 flow edges to `inferred` (the residual prose→structure gap the chapter argues).

---

### Concept 2 — Dwell and pacing: the long-persistence evidence (G5)

**Source locator:** Summary; "Overview of Activity"; "Review Application, Security, and System Event Logs".

**Paraphrase:** The advisory is direct about timescale. The agencies observed Volt Typhoon **maintaining access and footholds within some victim IT environments for at least five years**. Persistence is validated repeatedly rather than exploited immediately: in one compromise NTDS.dit was likely extracted from three domain controllers over a four-year period; in another, twice from a single victim over nine months. Following credential dumping the actors are largely silent on the network, performing discovery but not exfiltrating bulk data — behaviour consistent with maintaining persistence rather than immediate action.

**Quote (if essential):**

> "the U.S. authoring agencies have recently observed indications of Volt Typhoon actors maintaining access and footholds within some victim IT environments for at least five years." (Summary)

**Maps to:** [`breach_reports_macro_timing.md`](breach_reports_macro_timing.md) (macro dwell evidence); [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md) (the dwell/pacing axes); ch3 §3.1.1 G5.

**Disposition for this thesis:** cited as current-campaign evidence that APT dwell is measured in months-to-years and that pacing is objective-driven — the empirical warrant for modelling an attacker whose value scales with multi-step commitment, distinct from commodity smash-and-grab.

---

### Concept 3 — Living-off-the-land and valid accounts as a behavioural class

**Source locator:** Summary; "Execution"; "Defense Evasion"; "Discovery".

**Paraphrase:** LOTL — native binaries and hands-on-keyboard command-line activity ("LOLBins"), plus reliance on valid accounts and log deletion — is described as the hallmark of the campaign, the mechanism of both stealth and long persistence, and the reason conventional atomic IOCs are largely absent. The advisory frames detection as necessarily behavioural (baselines, anomaly detection, proactive hunting) rather than indicator-based.

**Quote (if essential):**

> "the use of living off the land (LOTL) techniques is a hallmark of Volt Typhoon actors' malicious cyber activity … The group also relies on valid accounts and leverage strong operational security, which combined, allows for long-term undiscovered persistence." (Summary)

**Maps to:** ch3 §3.1.1 (TTP durability over atomic indicators — pairs with `sadlek2022` on indicator decay); the hand-curated flow's `T1078` / `T1218` / `T1070.*` nodes.

**Disposition for this thesis:** supports the "model behaviour at technique/tactic resolution, not indicators" argument; corroborating grey-literature instance, not the primary analytic source.

---

### Concept 4 — Objective-driven restraint: pre-positioning without destructive action

**Source locator:** "Overview of Activity" (assessment); "Collection and Exfiltration".

**Paraphrase:** The agencies assess with high confidence that the actors are **pre-positioning** on IT networks to enable disruption of OT functions in a future crisis, and that this target choice and behavioural pattern is *not* consistent with traditional espionage. Critically, the observed activity stops at capability: the actors were positioned to reach OT assets and collected OT documentation (SCADA diagrams, relays, switchgear), but the advisory reports no execution of destructive OT action — the objective is durable, stealthy access.

**Quote (if essential):**

> "After successfully gaining access to legitimate accounts, Volt Typhoon actors exhibit minimal activity within the compromised environment (except discovery …), suggesting their objective is to maintain persistence rather than immediate exploitation." (Overview of Activity)

**Maps to:** the hand-curated flow's terminal `attack-condition` end-state (a prepositioning objective, deliberately **not** an Impact technique); [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md) (goal-directedness axis).

**Disposition for this thesis:** a faithfulness anchor — the flow models restraint because the source reports restraint. Useful in ch3 as an instance of objective-directed APT behaviour that a purely opportunistic attacker model cannot express.

---

### Concept 5 — Technique coverage (Appendix C)

**Source locator:** Appendix C, Tables 5–17.

**Paraphrase:** The advisory formally maps the campaign to **67 ATT&CK (v14) techniques across 13 tactics** (reconnaissance through exfiltration; no Impact technique). This is a union across multiple victims, not a single ordered incident — a distinction the hand-curated flow respects (technique set = Appendix C; ordering only where the narrative states it).

**Maps to:** the hand-curated flow's node inventory (67 actions == Appendix C); the ATT&CK v14→v19.1 deltas are recorded in [`../../../data/gap/hand_curated/README.md`](../../../data/gap/hand_curated/README.md) (`T1070.001` revoked; TA0005 renamed).

**Disposition for this thesis:** the coverage-cost illustration — a heavily reported state campaign is mappable at technique resolution, yet the CTID corpus carries no flow for it; building one is analyst labour the corpus has not spent.

---

## Open questions / things to verify

- **Full title / co-seal list at submission** — read here from the ASD's ACSC republication, not cisa.gov (403 to automated retrieval). Confirm the co-sealing agency list and exact title against the CISA PDF before final submission. (Bib entry `cisaaa24038a` carries the same provenance note.)
- **ATT&CK version** — the advisory maps to v14; the repo pins v19.1. If any technique is cited in prose, check for a v14→v19.1 rename/revocation (the flow README lists the two that bite: `T1070.001`, TA0005).

## Out of scope for this thesis

Detection/hunting guidance (ESENT event IDs, `gait`/Zeek, impossible-travel), the full incident-response/eviction playbook, and the IOC hashes (Appendix B) — operational defender material with no bearing on the attacker model or the flow.
