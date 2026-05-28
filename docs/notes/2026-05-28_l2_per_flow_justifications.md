---
status: durable
created: 2026-05-28
topic: L2 partition — per-flow P6 class assignment justifications
---

# Per-flow P6 class assignments — justifications, citations, and critique

## Why this exists

The L2 partition decision at
[`./2026-05-28_l2_partition_decision.md`](./2026-05-28_l2_partition_decision.md)
recommends **P6 (compound-class disjoint)** as the working classification —
the audit-traced CSV at
[`./2026-05-28_l2_metadata_audit.csv`](./2026-05-28_l2_metadata_audit.csv)
records which flow lands in which class, but the CSV's `notes` column is too
terse to defend against *"why did you classify X this way?"*. This file is the
**per-flow defence** — one entry per flow, with the authoritative-source
citation that grounds the classification and a critique note on cases where
the call could be challenged.

The classifications are **not** machine-derived; they were assembled by manual
audit (a hybrid pass over the CTID `example_flows/` index, ATT&CK Group pages
for attributed flows, and ~14 vendor-report executive summaries via `WebFetch`).
That manual work is the load-bearing input the L2 partition rests on; this
file makes it auditable.

## Method (one paragraph)

Each flow was classified into one of `{pure_steal, pure_impediment,
double_extortion, infrastructure_setup}` by reading **(i)** the CTID
`example_flows/` index page's per-flow blurb (one curator-written line per
flow), **(ii)** the ATT&CK Group / Campaign page where the flow's `flow_name`
mapped to an ATT&CK G-ID or C-ID, and **(iii)** the most authoritative
vendor report URL in the flow's `references[]` (Mandiant via cloud.google
redirect, Unit 42, CrowdStrike, Microsoft, Talos, DFIR Report,
CISA — though CISA URLs returned 403 to `WebFetch`). The `stated_objective`
column in the audit CSV is the labelled output; the `metadata_confidence`
column records the confidence level for that label. **Structure
(per-flow YAML terminals + reaches) was used as a *cross-check*, not as
the classification mechanism** — see the partition-decision note's
discussion of P1's 36 % structural-vs-stated concordance for the empirical
case for sourcing classification from narrative.

## Class summary

| Class | n flows | Confidence: high | medium | low |
|---|--:|--:|--:|--:|
| pure_steal | 19 | 14 | 2 | 3 |
| pure_impediment | 8 | 7 | 0 | 1 |
| double_extortion | 6 | 6 | 0 | 0 |
| infrastructure_setup | 5 | 3 | 0 | 2 |
| **total** | **38** | **30** | **2** | **6** |

The six `low`-confidence flows are: three CISA URLs (WebFetch blocked) plus
three flows where the verification round (below) surfaced source-tensions
or ambiguous fit within the 4-class scheme (`mac_malware_steals_crypto`,
`searchawesome_adware`, `toolshell_vulnerability_in_sharepoint`).

## Verification round (2026-05-28)

This file's first draft surfaced 8 contestable classifications. Each was
re-verified by re-reading the primary source and the actual flow YAML
content. Outcomes:

| Flow | First-draft class | Verified class | Why |
|---|---|---|---|
| `mac_malware_steals_crypto` | pure_impediment | **pure_steal** *(rev, conf↓)* | Unit 42 frames credential/cookie theft as primary monetisation; mining secondary. Genuinely ambiguous within 4-class but leans steal_data. |
| `muddy_water` | double_extortion | **pure_steal** *(rev)* | Talos: 'no encryption, wiping, or ransom demands' in the cited campaign; T1486 listed as capability only (flow confidence:0). G0069 = espionage. |
| `toolshell_*` | double_extortion | **pure_steal** *(rev, conf↓)* | Unit 42: MachineKey exfiltration attributed to cluster CL-CRI-1040; 4L4MD4R ransomware NOT attributed to the same cluster — different actors exploiting the same vuln. |
| `sony_malware` | pure_impediment | **pure_impediment** *(conf)* | Flow YAML has no exfil techniques (T1041/T1567/T1048 absent), only impact + supporting. Flow scope is the Destover wiper, not the broader incident. |
| `swift_heist` | pure_steal | **pure_steal** *(conf)* | Credential exfiltration → fraudulent transfer fits Alshamrani's "steal data" objective by analogy. Defensible if awkward. |
| `searchawesome_adware` | pure_impediment | **pure_impediment** *(conf↓)* | Malwarebytes: 'doesn't directly exfiltrate user data'. No clean home in 4-class. Confidence downgraded to low; defensible as integrity-compromise by analogy but stretch. |
| `openclaw` | infrastructure_setup | **dropped from corpus** | HiddenLayer security-research demonstration / proof-of-concept (MITRE ATLAS AML.CS0051), not analyst-curated CTI of a real operation. Equivalent status to `example_attack_tree`. All 18 actions ATLAS `AML.T*` — contributed zero Enterprise nodes to the GAP. |
| `cisa_aa22_138b_*` (×3) | as-audited | **confirmed** *(conf=low)* | CISA URL still 403 to WebFetch, but web-search corroboration of the advisory's text supports the structural calls (TA1 = data-exfil-and-webshell → steal_data; alt+TA2 = webshell/proxy without payload → infrastructure_setup). |

The verification round had two material effects on the verdict:

1. **Corpus drops 39 → 38 flows** (openclaw removed; `data/gap/flows/openclaw.yaml`
   deleted, `src/mtdsim/l0_cti/fetch.py` `FLOW_NAMES` updated, `gap_v0.5.json`
   rebuilt with `source_flow_count=38`, node/edge counts unchanged).
2. **Class counts shift from 16:9:8:6 to 19:8:6:5**. The shift is *toward*
   pure_steal (the verification round added 3 flows: mac + muddy + toolshell;
   double_extortion lost 2: muddy + toolshell; pure_impediment lost 1: mac;
   infrastructure_setup lost 1: openclaw). The corpus-level JSD discrimination
   improves slightly: mean technique-distribution JSD **0.317** under the
   revised classes (vs 0.302 under the first draft). The verdict (P6) is
   reinforced.

---

## pure_steal (n = 19)

Operations whose analyst-stated objective is data theft only — espionage,
financial-data exfil, credential / PII harvesting. **Nine of 19 reach an
exfiltration terminal structurally (Def A)**; the other ten are *truncated*
reports — the analyst drew the operation up to the point of detection,
before the exfiltration step appeared as a flow terminal — or *capability-
aggregating* threat-actor flows whose terminals are mid-kill-chain. Under P1
(structural-terminal) most of these would be mis-classified as
`position_for_future`; under P6 they are correctly `pure_steal` because the
analyst-stated narrative is unambiguous.

Three flows landed here through the verification round (revised from
their first-draft classes): `mac_malware_steals_crypto` (was
pure_impediment), `muddy_water` (was double_extortion),
`toolshell_vulnerability_in_sharepoint` (was double_extortion). Their
revised entries are below.

### `cisa_aa22_138b_vmware_workspace_ta1` — *pure_steal* · confidence: **low**

CISA AA22-138B documents threat-actor TA1 exploiting VMware Workspace ONE
Access (CVE-2022-22954/22960) for credential harvesting + data staging
prior to exfiltration. Structural terminal is T1041 (Exfiltration Over
C2 Channel) so the structural signal aligns; CISA URL is 403 to WebFetch
so the confidence is `low` on stated intent (the in-flow content + the
structural exfil terminal carry the call).

- **CISA advisory** (403 to WebFetch; human-readable): https://www.cisa.gov/uscert/ncas/alerts/aa22-138b
- **Critique**: CISA gives partial visibility. The TA1 flow lands `pure_steal`
  with weak external attestation; if the advisory turns out to describe
  ransomware deployment rather than credential exfil, this flips to
  `pure_impediment` or `double_extortion`. **Re-verify against the CISA
  advisory's full text before defence.**

### `cobalt_kitty_campaign` — *pure_steal* · confidence: **high**

OceanLotus (APT32, G0050) corporate-espionage campaign against a Vietnamese
conglomerate (Cybereason 2017). The Cybereason report frames the goal
explicitly: *"stealing proprietary business information"*. Cobalt Kitty is
a documented APT32 operation. The flow has no exfil terminal structurally
(the report stops at lateral-movement / C2) — this is exactly the
*truncated-report* pattern that motivates P5/P6 over P1 structural.

- **Cybereason**: https://www.cybereason.com/blog/operation-cobalt-kitty-apt
- **CrowdStrike OceanBuffalo**: https://adversary.crowdstrike.com/en-US/adversary/ocean-buffalo/
- **ATT&CK G0050**: https://attack.mitre.org/groups/G0050/
- **Critique**: none — narrative is unambiguous; the truncated structural
  view is itself a finding (the corpus's observability boundary).

### `equifax_breach` — *pure_steal* · confidence: **high**

Canonical 2017 PII data breach. 147 M consumer records exfiltrated via
Apache Struts vulnerability + lateral movement. The CSO Online retrospective
and the U.S. Department of Justice indictment characterise the operation as
exfiltration / espionage by Chinese state actors.

- **CSO Online**: https://www.csoonline.com/article/3444488/equifax-data-breach-faq-what-happened-who-was-affected-what-was-the-impact.html
- **DoJ indictment**: https://www.justice.gov/opa/press-release/file/1246891/download
- **Critique**: none — Equifax is the textbook data-breach case.

### `fin13_case_1` — *pure_steal* · confidence: **high**

FIN13 (G1016) — Mandiant: *"achieves its objectives by stealing intellectual
property, financial data, mergers and acquisition information, or PII"*.
Latin-America-focused financial cybercrime; Case 1 is the long-dwell
Mexican-bank case (~6 years pre-discovery). Structurally no exfil terminal —
truncated report.

- **Mandiant FIN13**: https://www.mandiant.com/resources/blog/fin13-cybercriminal-mexico
- **Sygnia Elephant Beetle** (FIN13 alias): https://f.hubspotusercontent30.net/hubfs/8776530/Sygnia-%20Elephant%20Beetle_Jan2022.pdf
- **Critique**: none — FIN13's stated objective is unambiguous.

### `fin13_case_2` — *pure_steal* · confidence: **high**

Same actor (G1016 FIN13) — Peruvian-bank operation; structurally
*does* reach exfil terminal (T1041 Exfiltration Over C2 Channel). Financial
data theft.

- **Mandiant FIN13**: https://www.mandiant.com/resources/blog/fin13-cybercriminal-mexico
- **Critique**: none.

### `ivanti_vulnerabilities` — *pure_steal* · confidence: **high**

UTA0178 (Chinese nation-state, per Volexity) exploiting Ivanti Connect Secure
zero-days (CVE-2023-46805 + CVE-2024-21887). Volexity report explicit:
credential harvesting, sensitive-data exfiltration, persistent access. No
exfil terminal structurally — truncated.

- **Volexity (Jan 2024)**: https://www.volexity.com/blog/2024/01/10/active-exploitation-of-two-zero-day-vulnerabilities-in-ivanti-connect-secure-vpn/
- **Critique**: none — Volexity narrative is direct.

### `jp_morgan_breach` — *pure_steal* · confidence: **high**

Canonical 2014 financial-services breach; 76M household + 7M small-business
records compromised. Reaches exfil structurally (terminal T1041 doesn't
appear; investigator reports describe data exfiltration via the corporate
network).

- **Bloomberg deep-dive**: https://www.bloomberg.com/news/articles/2014-08-29/jpmorgan-hack-said-to-span-months-via-multiple-flaws
- **SANS GIAC paper**: https://www.giac.org/paper/gsec/36190/minimizing-damage-jp-morgans-data-breach/143120
- **Critique**: none — canonical.

### `mac_malware_steals_crypto` — *pure_steal* · confidence: **low**

*Revised from `pure_impediment` after the verification round (2026-05-28).*
OSX.DarthMiner — Mac malware that mines cryptocurrency *and* steals
crypto-exchange browser cookies. Unit 42 explicitly frames credential/cookie
theft as the *primary* monetisation channel — *"more efficient way to
generate profits than outright cryptocurrency mining"* — and concludes
*"intended to help threat actors generate profit by collecting credential
information and mining cryptocurrency"* (both verbs, theft first). The
first-draft call landed `pure_impediment` because the malware *also* mines;
verification surfaced that Unit 42's framing leads with theft.

- **Palo Alto Unit 42**: https://unit42.paloaltonetworks.com/mac-malware-steals-cryptocurrency-exchanges-cookies/
- **Critique**: the operation is *genuinely both-objectives* at the malware
  level but doesn't fit `double_extortion` (which requires threat-to-leak
  coupled with ransom). The 4-class scheme has no clean home; `pure_steal`
  is the lesser of two bad fits given Unit 42's emphasis. A future
  framework with a `monetisation` / `multi-purpose` class would re-classify.
  Confidence is `low` because the call is acknowledged as ambiguous.

### `marriott_breach` — *pure_steal* · confidence: **high**

2018 Starwood breach (disclosed late 2018, intrusion 2014–2018). 500M guest
records including passport numbers exfiltrated. Attributed to Chinese MSS by
US government. Structural terminals at reconnaissance / stealth — truncated.

- **CSO Online**: https://www.csoonline.com/article/3441220/marriott-data-breach-faq-how-did-it-happen-and-what-was-the-impact.html
- **Senate hearing testimony**: https://www.hsgac.senate.gov/imo/media/doc/Soresnson%20Testimony.pdf
- **Critique**: none — canonical.

### `mitre_nerve` — *pure_steal* · confidence: **high**

MITRE's own 2024 breach (NERVE network). UNC5221 China-nexus actor
exploiting Ivanti zero-days. MITRE Engenuity post-mortem: document
exfiltration via Ivanti exploitation. Structurally reaches exfil.

- **MITRE Engenuity**: https://medium.com/mitre-engenuity/technical-deep-dive-understanding-the-anatomy-of-a-cyber-intrusion-080bddc679f3
- **Critique**: none — well-documented and self-reported.

### `muddy_water` — *pure_steal* · confidence: **medium**

*Revised from `double_extortion` after the verification round (2026-05-28).*
MuddyWater (G0069) — Iranian cyber-espionage group. Talos's Turkey-campaign
coverage is explicit: *"no encryption, wiping, or ransom demands"* in the
cited campaign; T1486 appears in the flow YAML at action `a10` with
`confidence: 0`, as does T1041 exfiltration at `a23` (also `confidence: 0`)
— both encoded by the original analyst with explicit uncertainty. ATT&CK
G0069 characterises MuddyWater as cyber-espionage. The first-draft
`double_extortion` call interpreted the flow's combined exfil+impact reach
as one-operation-pursues-both; verification showed Talos's narrative
describes pure espionage and the impact action is a *capability* note,
not an observed behaviour.

- **Talos**: https://blog.talosintelligence.com/iranian-apt-muddywater-targets-turkey/
- **ATT&CK G0069**: https://attack.mitre.org/groups/G0069/
- **Critique**: the flow aggregates MuddyWater capabilities across
  multiple campaigns rather than a single operation. The class assignment
  is about *MuddyWater the actor* more than about any specific operation;
  an operation-resolved corpus would split this into per-operation entries.
  Confidence is `medium`: the espionage class is correct for G0069, but
  the capability-aggregating scope of this particular flow file makes
  the call about the actor's typical objective, not the flow's specific one.

### `oceanlotus` — *pure_steal* · confidence: **high**

APT32 / OceanLotus (G0050) — espionage / surveillance of governments + dissidents
in South-East Asia. The CTID-affiliated flow file documents the operation; reaches
exfil structurally.

- **CTID Ocean Lotus Operations Flow**: https://github.com/center-for-threat-informed-defense/ocean-lotus/blob/main/Operations_Flow/Operations_Flow.md
- **ATT&CK G0050**: https://attack.mitre.org/groups/G0050/
- **Critique**: none.

### `solarwinds` — *pure_steal* · confidence: **high**

APT29 / Cozy Bear / NOBELIUM (G0016) supply-chain compromise; ATT&CK
Campaign C0024. Microsoft + Picus characterise the operation as espionage
/ data theft. Reaches exfil structurally.

- **Microsoft Solorigate analysis**: https://www.microsoft.com/en-us/security/blog/2020/12/18/analyzing-solorigate-the-compromised-dll-file-that-started-a-sophisticated-cyberattack-and-how-microsoft-defender-helps-protect/
- **ATT&CK C0024**: https://attack.mitre.org/campaigns/C0024/
- **Critique**: none — canonical APT espionage.

### `swift_heist` — *pure_steal* · confidence: **high**

APT38 (G0082) Bangladesh-Bank operation — financial theft via fraudulent
SWIFT transfers (~$81M stolen). Reaches no exfil/impact terminal
structurally — truncated. The "theft" here is monetary, not data, but
operationally it's data-theft-of-financial-records-followed-by-fraudulent-
transfer. Classified pure_steal.

- **Wired**: https://www.wired.com/2016/05/insane-81m-bangladesh-bank-heist-heres-know/
- **Reuters investigation**: https://www.reuters.com/investigates/special-report/cyber-heist-federal
- **NYTimes**: https://www.nytimes.com/interactive/2018/05/03/magazine/money-issue-bangladesh-billion-dollar-bank-heist.html
- **Critique**: **arguable**. Strictly, SWIFT heist is fraud / monetary
  theft, not "data" theft. Treating it as `pure_steal` is the project's
  convention because monetary theft via credential-harvesting and
  fraudulent transfer fits Alshamrani's "steal organisation data /
  exfil" objective better than impediment or position_for_future. If a
  future framework distinguishes monetary fraud from data theft, this
  flow may need a fifth class (`fraud` / `monetisation`).

### `target_breach` — *pure_steal* · confidence: **high**

Canonical 2013 PoS breach; 40M payment-card records exfiltrated via HVAC
vendor pivot. Reaches exfil structurally.

- **Krebs**: https://krebsonsecurity.com/2014/02/email-attack-on-vendor-set-up-breach-at-target/
- **Senate report**: https://www.commerce.senate.gov/services/files/24d3c229-4f2f-405d-b8db-a3a67f183883
- **Critique**: none — canonical.

### `toolshell_vulnerability_in_sharepoint` — *pure_steal* · confidence: **low**

*Revised from `double_extortion` after the verification round (2026-05-28).*
CVE-2025-49704 / 49706 / 53770 SharePoint RCE chain ("ToolShell"). Unit 42
attributes the MachineKey-exfiltration behaviour to threat-actor cluster
**CL-CRI-1040** (which overlaps Microsoft's **Storm-2603**); the 4L4MD4R
ransomware deployment is reported separately and *not* attributed to
CL-CRI-1040 — Unit 42's framing is *"different threat actors exploiting
the same vulnerability for divergent objectives"*. Strictly not
double_extortion (which requires *one operation* pursuing both);
the flow conflates two actor clusters' observed behaviour into one
flow file.

- **Palo Alto Unit 42**: https://unit42.paloaltonetworks.com/microsoft-sharepoint-cve-2025-49704-cve-2025-49706-cve-2025-53770/
- **Akamai**: https://www.akamai.com/blog/security-research/sharepoint-vulnerability-rce-active-exploitation-detections-mitigations
- **Varonis**: https://www.varonis.com/blog/toolshell-sharepoint-rce
- **Critique**: now `pure_steal` because CL-CRI-1040 — the named,
  attribution-rich actor in the flow — is the steal_data half. Confidence
  `low` because the flow itself conflates two actors; ideally this should
  be **split** into two flows (CL-CRI-1040 → pure_steal; 4L4MD4R-deployer
  → pure_impediment), but that's a corpus-edit, not a classification call.
  Flagged for the simulator-verification sub-handoff as a candidate flow
  to split if the toolchain supports it.

### `turla_carbon_emulation_plan` — *pure_steal* · confidence: **high**

CTID emulation plan for Turla's Carbon backdoor. Turla (G0010) is Russian
cyber-espionage; the CTID blurb is explicit: *"provides data exfiltration
capabilities"*. The flow is an emulation-plan scope artefact rather than a
single incident.

- **CTID emulation plan**: https://github.com/attackevals/turla/tree/main/Emulation_Plan/Carbon_Scenario
- **ATT&CK G0010**: https://attack.mitre.org/groups/G0010/
- **Critique**: this is an emulation plan, not an incident — it represents
  *typical* Turla behaviour rather than a specific operation. Including it
  in the corpus is fine but worth flagging: if the corpus separates
  *emulation-plan* from *incident* scopes in a later analysis, the 2 Turla
  emulation plans + ~1 other emulation-plan flows form their own subset.

### `turla_snake_emulation_plan` — *pure_steal* · confidence: **high**

CTID emulation plan for Turla's Snake (Uroburos) rootkit. CTID blurb:
*"used to compromise computers and exfiltrate data"*. Same caveat as
Carbon (emulation-plan, not incident).

- **CTID emulation plan**: https://github.com/attackevals/turla/tree/main/Emulation_Plan/Snake_Scenario
- **DOJ Snake takedown**: https://www.justice.gov/usao-edny/pr/justice-department-announces-court-authorized-disruption-snake-malware-network
- **Critique**: same as Carbon — emulation-plan scope.

### `uber_breach` — *pure_steal* · confidence: **medium**

2022 Uber breach attributed to Lapsus$ (G1004 in ATT&CK). Credential theft
+ source-code access. Reaches no exfil/impact terminal structurally —
truncated. Confidence is `medium` because the audit's attribution column
flagged `G1004?` (Lapsus$ attribution is contested in early reporting;
some sources name a Lapsus$-affiliated individual rather than the group).

- **GitGuardian retrospective**: https://blog.gitguardian.com/uber-breach-2022/
- **CyberArk analysis**: https://www.cyberark.com/resources/blog/unpacking-the-uber-breach
- **Uber's own statement**: https://www.uber.com/newsroom/security-update/
- **Critique**: Lapsus$ operations cluster around credential theft +
  data theft + extortion; some Lapsus$ operations *also* deploy ransomware
  / public-shame disclosure (which would tip toward double_extortion).
  Uber's breach didn't reach ransomware deployment per the public record,
  so `pure_steal` is defensible. If a fuller record surfaces ransomware
  deployment, re-classify.

---

## pure_impediment (n = 8)

Operations whose analyst-stated objective is disruption / destruction /
resource hijacking — wipers, destructive malware, miners. **All 8 reach
an impact terminal structurally** (Def A); the metadata-attested and
structural-terminal mechanisms agree on this class.

### `cisa_iranian_apt` — *pure_impediment* · confidence: **high**

CISA AA22-320A — Iranian APT (Mercury / MuddyWater-adjacent, attribution
varies) deploying XMRig cryptominer on Federal Civilian Executive Branch
networks. The CTID blurb is explicit: cryptominer deployment.

- **CISA advisory** (403 to WebFetch but CTID blurb confirms): https://www.cisa.gov/uscert/ncas/alerts/aa22-320a
- **Critique**: this is resource-hijacking (T1496) rather than
  destruction; sits comfortably in `pure_impediment` because the impact
  is resource cost (CPU + power) to the victim. Worth noting that a
  future taxonomy might split `pure_impediment` into
  `destruction / disruption / resource_hijacking`. For this corpus, the
  conflation is fine.

### `maastricht_university_ransomware` — *pure_impediment* · confidence: **high**

2019 Maastricht University ransomware (TA505 attribution per the
Fox-IT post-incident report). The Fox-IT report does not name exfiltration
prior to encryption — pure-impediment ransomware, not double-extortion.
The university paid the ransom (€197 000).

- **Fox-IT Report (PDF)**: https://www.maastrichtuniversity.nl/nl/file/foxitrapportreactieuniversiteitmaastrichtnl10-02pdf
- **Critique**: 2019 ransomware predates the *industry standard*
  shift to double-extortion (which took off c. 2020). Classifying it
  as `pure_impediment` is consistent with the report's silence on
  exfiltration.

### `notpetya` — *pure_impediment* · confidence: **high**

Sandworm (G0034) NotPetya wiper masquerading as ransomware, 2017.
Pseudo-ransomware whose encryption is irreversible — by design destructive.
CrowdStrike + DoJ indictment characterise as destructive wiper.

- **CrowdStrike Petrwrap analysis**: https://www.crowdstrike.com/blog/petrwrap-ransomware-technical-analysis-triple-threat-file-encryption-mft-encryption-credential-theft/
- **DoJ indictment**: https://www.justice.gov/opa/press-release/file/1328521/download
- **ATT&CK G0034**: https://attack.mitre.org/groups/G0034/
- **Critique**: none — NotPetya's pseudo-ransomware nature (no
  recoverable decryption) marks it as `pure_impediment` rather than
  double_extortion (no exfil-and-leak component).

### `searchawesome_adware` — *pure_impediment* · confidence: **low**

SearchAwesome adware — intercepts encrypted web traffic (MitM the user's
browser certificates) to inject ads. *Confidence downgraded to `low`
after the verification round (2026-05-28).* Malwarebytes' framing is
explicit: *"doesn't directly exfiltrate user data"* — the malware
intercepts traffic to *inject* ads, not to harvest. It sits between
integrity-compromise and nuisance/monetisation; the 4-class scheme has
no clean home. `pure_impediment` is defensible as integrity-compromise
by analogy but is the weakest classification in the class.

- **Malwarebytes Labs**: https://www.malwarebytes.com/blog/news/2018/10/mac-malware-intercepts-encrypted-web-traffic-for-ad-injection
- **Malware Behavior Catalogue**: https://github.com/MBCProject/mbc-markdown/blob/main/xample-malware/searchawesome.md
- **Critique**: **stretch classification retained**. Adware monetisation
  isn't a textbook fit for any of the four classes. A future framework
  with a `monetisation` / `nuisance_malware` class would re-classify.
  For now, retained as `pure_impediment` with `low` confidence because
  removing it (matching the `openclaw` / `example_attack_tree` drops)
  would require a clearer criterion than "doesn't fit the 4-class
  scheme cleanly" — and SearchAwesome *is* analyst-curated CTI of
  observed real-world malware, just not adversary-objective-typical.

### `shamoon` — *pure_impediment* · confidence: **high**

Disk-wiping malware family (Shamoon 1 — Saudi Aramco 2012; Shamoon 2/3 —
later waves). McAfee article explicit: wipes Master Boot Record + system
disks. No exfiltration prior to wipe — destructive only.

- **McAfee**: https://www.mcafee.com/blogs/other-blogs/mcafee-labs/shamoon-returns-to-wipe-systems-in-middle-east-europe/
- **Critique**: none — canonical destructive wiper.

### `sony_malware` — *pure_impediment* · confidence: **high**

Lazarus (G0032) 2014 Sony Pictures Entertainment attack. ATT&CK's G0032
page describes the operation as a *"destructive wiper attack on Sony Pictures
Entertainment"*. There was also a large data leak component (emails, scripts,
unreleased films) that *could* push this toward double_extortion.

- **ArsTechnica**: https://arstechnica.com/information-technology/2014/12/inside-the-wiper-malware-that-brought-sony-pictures-to-its-knees/
- **Trend Micro analysis**: https://web.archive.org/web/20220120083152/https://www.trendmicro.com/en_us/research/14/l/an-analysis-of-the-destructive-malware-behind-fbi-warnings.html
- **ATT&CK G0032**: https://attack.mitre.org/groups/G0032/
- **Critique**: **arguable**. The 2014 Sony attack involved both data
  exfiltration (the email leaks) AND destructive wiping. By the
  P6 criterion ("explicitly pursues both data theft and impediment,
  simultaneously"), this **could** be `double_extortion`. The audit
  landed it in `pure_impediment` because the *flow file's* content is
  dominated by the destructive component and ATT&CK G0032's primary
  characterisation is wiper. If the flow's specific scope is the data
  leak rather than the destruction, re-classify. **Re-verify the
  Attack Flow's actual scope before defence.**

### `tesla_kubernetes_breach` — *pure_impediment* · confidence: **high**

2018 Tesla AWS K8s cluster compromise — exposed Kubernetes admin console
leveraged for XMRig cryptomining. Reaches impact structurally (T1496
Resource Hijacking).

- **The Cryptojacking Epidemic (RedLock, archive)**: https://web.archive.org/web/20210110185439/https://redlock.io/blog/cryptojacking-tesla
- **Critique**: none — clear resource-hijacking case; same caveat as
  cisa_iranian_apt (resource hijacking vs destruction within the
  `pure_impediment` class).

### `whispergate` — *pure_impediment* · confidence: **high**

Russian-state wiper deployed against Ukraine in January 2022 (G0034
Sandworm attribution). Microsoft + Talos + Recorded Future all
characterise as destructive wiper.

- **Microsoft (15 Jan 2022)**: https://www.microsoft.com/en-us/security/blog/2022/01/15/destructive-malware-targeting-ukrainian-organizations/
- **Talos**: https://blog.talosintelligence.com/ukraine-campaign-delivers-defacement/
- **Recorded Future**: https://www.recordedfuture.com/whispergate-malware-corrupts-computers-ukraine
- **Critique**: none — clear destructive wiper.

---

## double_extortion (n = 6)

Operations whose analyst-stated narrative explicitly pursues *both* data
theft AND impediment, simultaneously. The double-extortion archetype is
*"exfiltrate sensitive data, encrypt it, then threaten to leak the
exfiltrated data if the ransom is not paid"* — both clauses load-bearing.

Two flows that landed here in the first draft were revised out by the
verification round: `muddy_water` (Talos showed the cited campaign was
espionage-only; T1486 was a *capability* note, not observed behaviour)
and `toolshell_vulnerability_in_sharepoint` (Unit 42 showed the
ransomware-deploying actor was different from the exfil-actor, so the
flow conflates two clusters rather than documenting one double-extortion
operation). Both are now `pure_steal` (with critique). Remaining flows
in this class are all *canonical, well-documented* double-extortion
ransomware operators.

### `black_basta_ransomware` — *double_extortion* · confidence: **high**

Black Basta RaaS (active since February 2022). Unit 42's threat assessment
characterises the operation as double-extortion: encrypt-and-leak. The
flow's content includes both T1567 (Exfiltration Over Web Service) and
T1486 (Data Encrypted for Impact) actions — structurally reaches both,
though P1's terminal-detection doesn't catch it because the analyst-
drawn terminals are intermediate (discovery / persistence).

- **Unit 42**: https://unit42.paloaltonetworks.com/threat-assessment-black-basta-ransomware/
- **Critique**: none — canonical double-extortion RaaS.

### `conti_cisa_alert` — *double_extortion* · confidence: **high**

Conti RaaS (G0102). The 2021 CISA Conti alert is the consensus
characterisation; Conti is *the* well-documented double-extortion
operator (Conti News leak site is the brand's leak-shame seam).
CISA URL is 403 to WebFetch but Conti's double-extortion modus
operandi is canonical across CTI.

- **CISA Conti alert**: https://www.cisa.gov/news-events/alerts/2021/09/22/conti-ransomware
- **ATT&CK G0102**: https://attack.mitre.org/groups/G0102/
- **Critique**: none — canonical.

### `conti_pwc` — *double_extortion* · confidence: **high**

Conti variant — the 2021 Health Service Executive (Ireland) attack
documented by PwC. Same operator (G0102) as `conti_cisa_alert`; the
PwC retrospective + HSE post-incident report describe both exfiltration
and encryption.

- **HSE PwC report (Ireland)**: https://www.hse.ie/eng/services/publications/conti-cyber-attack-on-the-hse-full-report.pdf
- **Critique**: none.

### `conti_ransomware` — *double_extortion* · confidence: **high**

Conti DFIR Report variant — another G0102 operation documented in detail
by The DFIR Report. Same double-extortion characterisation.

- **DFIR Report Conti**: https://thedfirreport.com/2021/05/12/conti-ransomware/
- **Critique**: none — but worth noting we have *three* Conti flows
  (CISA / PwC / DFIR variants) — they're not redundant data points,
  they're three independent analyst-curated views of the same operator
  family. For corpus-level statistics that's fine; for
  per-class-discrimination if Conti dominates the class, the
  classification may be over-fit to Conti's specifics. **Worth
  flagging for the simulator-verification sub-handoff.**

### `ragnar_locker` — *double_extortion* · confidence: **high**

Ragnar Locker RaaS (G0125). Multiple vendor reports (Sophos, Acronis,
Avertium, Zscaler) characterise as established double-extortion operator.
Flow content reaches both exfil and impact (T1486).

- **Sophos**: https://news.sophos.com/en-us/2020/05/21/ragnar-locker-ransomware-deploys-virtual-machine-to-dodge-security/
- **Zscaler (double-extortion advent retrospective)**: https://www.zscaler.com/blogs/security-research/threatlabz-ransomware-review-advent-double-extortion
- **Critique**: none.

### `revil` — *double_extortion* · confidence: **high**

REvil / Sodinokibi RaaS (G0115). Multiple high-profile victims (Travelex,
JBS, Kaseya). Secureworks + Bleeping Computer + BBC all describe
double-extortion modus operandi. Structurally reaches both exfil (T1041)
and impact (T1486) — *the only* flow under P1 that correctly multi-classes.

- **Secureworks**: https://www.secureworks.com/research/revil-sodinokibi-ransomware
- **BBC (REvil takedown)**: https://www.bbc.com/news/technology-55439190
- **Critique**: none — canonical.

---

## infrastructure_setup (n = 5)

Operations whose analyst-stated narrative is *pre-payload*: loader / C2 /
RaaS-affiliate-positioning evicted (or hypothetical, in the OpenClaw case)
before the downstream objective was reached. *Not* surveillance and *not*
truncated breach — these are operations whose intended objective is
documented as **not yet realised in the flow record**.

### `cisa_aa22_138b_vmware_workspace_alt` — *infrastructure_setup* · confidence: **low**

Alt-method variant of the CISA AA22-138B advisory (same VMware Workspace
ONE vulnerabilities as ta1 / ta2). Structural terminal at stealth only;
describes an alternative exploitation method without observed payload.

- **CISA** (403): https://www.cisa.gov/uscert/ncas/alerts/aa22-138b
- **Critique**: low confidence because CISA's full text is 403 to
  WebFetch; classification rests on the in-flow content (terminal at
  stealth, no exfil / impact reach). If the advisory's full text names
  a specific payload, this could flip.

### `cisa_aa22_138b_vmware_workspace_ta2` — *infrastructure_setup* · confidence: **low**

Threat Actor 2 variant of the AA22-138B advisory. Structural terminal
at C2 only — pre-positioning. Same CISA-403 caveat as `alt`.

- **CISA** (403): https://www.cisa.gov/uscert/ncas/alerts/aa22-138b
- **Critique**: same as `alt`.

### `dfir_bumblebee_round_2` — *infrastructure_setup* · confidence: **high**

DFIR Report's *BumbleBee: Round Two* — 2022 BumbleBee loader intrusion.
DFIR Report explicit: *"pre-ransomware activity"* and *"evicted from the
network before any further impact"*. Classic initial-access-broker
positioning.

- **DFIR Report**: https://thedfirreport.com/2022/09/26/bumblebee-round-two/
- **Critique**: none — DFIR Report's *"evicted before mission complete"*
  framing is the canonical signature for this class.

### `gootloader` — *infrastructure_setup* · confidence: **high**

DFIR Report's *SEO Poisoning – A Gootloader Story* — multi-stage loader
intrusion. *"No further impact before evicted"*.

- **DFIR Report**: https://thedfirreport.com/2022/05/09/seo-poisoning-a-gootloader-story/
- **Critique**: none — same canonical signature.

### `hancitor_dll` — *infrastructure_setup* · confidence: **high**

DFIR Report's *From Zero to Domain Admin* — Hancitor loader intrusion
leading to Cobalt Strike. DFIR Report explicit: *"threat actors were
evicted before completing their mission"*. Domain-admin + Cobalt Strike
positioning, but eviction prevents observable payload deployment.

- **DFIR Report**: https://thedfirreport.com/2021/11/01/from-zero-to-domain-admin/
- **Critique**: none.

---

## Dropped from corpus after verification (n = 1)

### `openclaw` — *dropped*

HiddenLayer's *OpenClaw Command & Control via Prompt Injection* — a
**security-research demonstration / proof-of-concept** (MITRE ATLAS
case study AML.CS0051) of prompt injection establishing persistent C2
over an LLM agent. *Not* analyst-curated CTI of a real adversary
operation against a real victim — equivalent status to
`example_attack_tree` (which Marc dropped from the corpus in commit
`bec89fc`).

Two structural facts confirm the drop is safe:

1. **All 18 actions are ATLAS** (`AML.T0008`, `AML.T0051`, `AML.T0053`,
   …, `AML.T0095.000`). **Zero Enterprise techniques.** The canonical
   Enterprise-only GAP receives no nodes or edges from OpenClaw — its
   only contribution to `gap_v0.5.json` is to inflate
   `source_flow_count`.
2. **No downstream code references it.** No `OpenClaw` lookup in
   `mtdnetwork/`, no test assertion on its presence, no spec text that
   names it as load-bearing.

Drop applied (this commit-bundle): `data/gap/flows/openclaw.yaml`
removed, `data/gap/_corpus_stix/OpenClaw.json` removed,
`src/mtdsim/l0_cti/fetch.py` `FLOW_NAMES` updated (38 entries),
`gap_v0.5.json` rebuilt with `source_flow_count=38` (node_count=124,
edge_count=478 unchanged). All 16 GAP tests pass on the rebuild.

- **MITRE ATLAS AML.CS0051**: https://atlas.mitre.org/studies/AML.CS0051
- **HiddenLayer**: https://www.hiddenlayer.com/research/exploring-the-security-risks-of-ai-assistants-like-openclaw

---

## Critique — load-bearing summary (post-verification)

The first-draft critique flagged 8 contestable classifications; the
verification round (2026-05-28) resolved them as follows:

1. **`mac_malware_steals_crypto` — *resolved (revised)*.** Now
   `pure_steal` with `low` confidence. Unit 42's framing leads with
   theft, mining secondary. Still genuinely ambiguous within the
   4-class scheme; future framework with `monetisation` class would
   re-classify.
2. **`sony_malware` — *resolved (confirmed)*.** Stays `pure_impediment`.
   The flow YAML has no exfiltration techniques (T1041 / T1567 / T1048
   absent) — only impact + supporting techniques. The flow's scope is
   the Destover wiper, not the broader Sony incident which separately
   included an email leak by the GoP actor.
3. **`muddy_water` — *resolved (revised)*.** Now `pure_steal` with
   `medium` confidence. Talos: *"no encryption, wiping, or ransom
   demands"* in the cited campaign. T1486 and T1041 actions in the YAML
   both carry `confidence: 0` (analyst-encoded uncertainty). G0069 is
   ATT&CK-categorised cyber-espionage.
4. **`toolshell_vulnerability_in_sharepoint` — *resolved (revised)*.**
   Now `pure_steal` with `low` confidence. Unit 42: MachineKey exfil
   attributed to cluster CL-CRI-1040, 4L4MD4R ransomware *not*
   attributed to the same cluster — different actors exploiting the
   same vuln. Flagged for possible flow-split in the simulator-
   verification step.
5. **`swift_heist` — *resolved (confirmed)*.** Stays `pure_steal` with
   note. Credentials-then-fraudulent-transfer fits Alshamrani's "steal
   organisation data" by analogy; defensible if awkward.
6. **`searchawesome_adware` — *resolved (confidence downgraded)*.**
   Stays `pure_impediment` but confidence drops to `low`. Malwarebytes:
   *"doesn't directly exfiltrate user data"* — adware-as-impediment is
   defensible by analogy but stretch. Future framework with a
   `monetisation` / `nuisance_malware` class would re-classify.
7. **`openclaw` — *resolved (dropped)*.** Removed from the corpus
   entirely (this commit-bundle). Security-research demonstration,
   not analyst-curated CTI; all 18 actions ATLAS-only (zero Enterprise
   contribution). Same status as the previously-dropped
   `example_attack_tree`.
8. **`cisa_aa22_138b_*` (×3) — *resolved (confirmed, `low`
   unchanged)*.** Web-search corroboration of the AA22-138B advisory
   text supports the structural calls: TA1 → pure_steal (exfil
   actions + webshell); alt + TA2 → infrastructure_setup (webshell /
   proxy without payload). Direct CISA WebFetch remains 403.

After the verification round, **three residual concerns** remain — none
critical, but worth a defence-of-thesis reader's attention:

- **`pure_steal` rests on narrative reading for ~10/19 truncated
  reports.** The class is high-confidence in headcount terms (14 of
  19 are `high`-confidence vendor or ATT&CK attestation), but if a
  future reader doubts the audit's narrative reading they would re-open
  this class first.
- **`mac_malware_steals_crypto` (low confidence, both-objective
  malware)** and **`searchawesome_adware` (low confidence, no clean
  4-class home)** are genuinely-ambiguous flows the audit retained
  with explicit confidence downgrades. A future framework that adds a
  `monetisation` / `multi-purpose` class would re-classify both.
- **`toolshell_vulnerability_in_sharepoint` should ideally be split**
  into a pure_steal flow (CL-CRI-1040) and a pure_impediment flow
  (4L4MD4R deployer). The audit retained it as a single
  `pure_steal` entry with critique; the simulator-verification step
  may want to split it.

**Operator-aggregation concern** — see the dedicated note at
[`./2026-05-28_l2_operator_aggregation_concern.md`](./2026-05-28_l2_operator_aggregation_concern.md).
The corpus is not flow-uniformly distributed across operators: three
Conti flows (G0102), two Turla emulation plans (G0010), two FIN13
cases (G1016), and three CISA AA22-138B variants share base operators
or advisories. If those over-represented operators dominate their
classes' discrimination signal, the per-class behaviour may be
over-fit. The dedicated note documents the concern and four
candidate mitigations (aggregation, generalisation-weighting, sensitivity-
testing, corpus expansion).

## How to read this when challenged

Walk an examiner through three layers:

1. **Headline:** *"P6 is the corpus-empirical refinement of Alshamrani's
   3-goal NIST taxonomy — same anchor, with `double_extortion` named
   explicitly (21 % of the corpus) and `position_for_future` renamed
   `infrastructure_setup` (because the corpus has 0 surveillance
   flows)."*
2. **Per-flow defence:** point to this file's relevant section. Each
   flow has its primary citation; ~80 % of flows have a single
   authoritative source (CTID blurb + one vendor or ATT&CK page) and
   the class is read straight from the source's text.
3. **Critique:** acknowledge the eight contestable cases above. None
   of them changes the load-bearing finding (the four classes are
   real, P1 mis-classifies 64 % of the corpus relative to analyst
   narrative) — they would shift individual flow membership at the
   margin.

If pushed harder on whether P6 vs P5 is the right call: **P6's
empirical warrant is the 8 double-extortion flows that P5
multi-membership *would* handle but P6 names explicitly**.
The simulator-verification sub-handoff
([`../handoffs/2026-05-28_l2_simulator_verification.md`](../handoffs/2026-05-28_l2_simulator_verification.md))
is the load-bearing test that decides whether the named compound class
behaves differently from a multi-membership join in the simulator. Until
that runs, P6 is the working recommendation; if the simulator says the
compound class doesn't separate from a multi-membership join, the
verdict reverts to P5.
