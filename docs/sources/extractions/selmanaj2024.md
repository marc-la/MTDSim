# Selmanaj 2024 — extraction notes

> Drinor Selmanaj, *Adversary Emulation with MITRE ATT&CK: Bridging the Gap
> Between the Red and Blue Teams*, O'Reilly Media, April 2024 (1st ed.).
> Source file: `docs/sources/tactic_profiles/step_c/APTProfiling_adversary-emulation-with-mitre-attampck-bridging-the-gap-between-the-red-and-blue-teams-1098143760-9781098143763.md`
> (+ `.pdf`, gitignored).
> Relevance to this thesis: an adversary-emulation textbook whose Ch. 4 walks
> **every ATT&CK tactic's modus operandi** and whose Ch. 2 fixes the
> APT-tempo vocabulary (dwell time, smash-and-grab vs slow-and-deliberate).
> The precedent survey's adversary-emulation-frameworks section noted no
> emulation resource attaches per-phase dwell; this is the canonical emulation
> *textbook* and it confirms that — behaviour and cadence, no per-tactic time.

### Relevance class

**S** (supporting) — broad §2 (group-assignment) evidence across all 15
profiles + the dwell-cadence taxonomy that names the two timing regimes the
catalogue's groups encode. No timing numbers except a re-reported Mandiant
dwell trend.

### Used in lit review

Tactic-profile §2/§4 evidence, all 15 (Step C, 2026-07-05); the
smash-and-grab / slow-and-deliberate dichotomy for the method note's
group framing.

## Bibliographic anchor

- **Citation key**: `selmanaj2024`
- **DOI / URL**: ISBN 978-1-098-14376-3 (O'Reilly)
- **Pages cited from**: Ch. 2 "Advanced Persistent Threats", Ch. 4 "The
  Adversary's Modus Operandi", Ch. 5 opener (md line locators, no print pages
  in parse)

## Relevant artefacts

### The dwell-cadence taxonomy — smash-and-grab vs slow-and-deliberate

**Source locator:** Ch. 2, "APTs can gain unauthorized access…" (md ~L707);
dwell-time definition (~L715)

**Paraphrase:** the book's central tempo claim, and the qualitative axis the
catalogue's timing groups discretise: APTs "employ various operational
cadences" — **smash and grab** ("an accelerated practice, pushing the criminal
to get whatever is possible before the session is lost and without worrying
about creating noise") vs **slow and deliberate** ("fits more APTs' long-term
plans, where it is vital that no alarm is activated and that … they stay
covert until the opportunity shows itself"). Default APT posture on gaining
access: "move undetected for as long as possible". **Dwell time** is defined
as MTTD + MTTR (in days): the elapsed time between initial intrusion and
threat eradication; "the longer the dwell time, the more opportunity the
adversary has to cause harm."

**Maps to:** [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md)
(stealth-low-and-slow vs objective-execution groups) ·
[`../tactic_profiles/README.md`](../tactic_profiles/README.md) (five timing
groups) · corroborates alshamrani2019's low-and-slow backbone with an
emulation-practitioner vocabulary.

**Disposition for this thesis:** verified [fetched] — names the two regimes;
supports modelling tempo as a small set of cadence classes, not per-tactic
free values.

---

### Re-reported Mandiant global-median-dwell trend (Table 2-1)

**Source locator:** Ch. 2, Table 2-1 + surrounding text (~L725–737)

**Paraphrase:** the book reproduces Mandiant's global median dwell time,
2011–2022: **416 days (2011), 243 (2012), 229 (2013), … down to a low of 21
days (2021)** (citing M-Trends 2022). The table body is parse-garbled beyond
the first three columns; the 416→21-day span is stated in running prose and is
legible. Secondary (the book cites Mandiant) — the primary M-Trends PDFs
fetched in this Step C
(`step_c/mandiant_mtrends_2025.pdf`, `..._2026.pdf`) supersede it as the
citable calibration target.

**Maps to:** [`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../notes/2026-07-04_tactic_duration_precedent_survey.md)
(macro-timing table, M-Trends row) — the whole-intrusion dwell observable,
whole-campaign not per-tactic.

**Disposition for this thesis:** [search]-via-textbook → superseded by the
primary M-Trends extraction; keep only as evidence the dwell metric is
standard practitioner vocabulary.

---

### Per-tactic modus operandi — behaviour for all 15 profiles (Ch. 4)

**Source locator:** Ch. 4, one section per tactic (md ~L1518–2124)

**Paraphrase:** Ch. 4 gives a behavioural paragraph per tactic. The
dwell-/reset-relevant content, mapped to each profile:

- **Reconnaissance (TA0043):** passive recon is "the least risky … not
  directly interacting with the target … which is characteristic of an APT
  behavior" but "time-consuming"; active recon "can be detected … generally a
  sign of an ongoing attack"; and recon "can occur at any stage in the attack
  life cycle" (recurrent). → [`01_reconnaissance`](../tactic_profiles/01_reconnaissance.md)
  §2 (patient/off-network default; active modality is the detectable one the
  substrate scan-prices).
- **Resource Development (TA0042):** "takes place outside of the company's
  protection and control. As a result, preventive measures may not be
  effective" — explicitly off-network. → [`02_resource-development`](../tactic_profiles/02_resource-development.md)
  §2/§3 (prep-off-network; an MTD shuffle cannot touch it — near-zero in-sim
  dwell + reset-immune).
- **Initial Access (TA0001):** "the access they gain during initial access may
  be short-lived if the target changes their passwords or otherwise limits the
  attackers' abilities" — foothold fragility. → [`03_initial-access`](../tactic_profiles/03_initial-access.md)
  §3 (a shuffle *invalidates* an IP/topology-bound foothold — reset-vulnerable;
  strengthens the reset verdict).
- **Execution (TA0002):** a fast enabling verb — "Once the attacker has
  successfully executed their code, they can start to carry out their malicious
  goals" (fileless/in-memory, e.g. PowerShell). → [`04_execution`](../tactic_profiles/04_execution.md)
  §2 (the "fast verb in a stealth wrapper" finding flagged unsettled in Step B
  — Selmanaj frames execution as the quick pivot, not a dwell).
- **Persistence (TA0003):** "maintain access … for an extended period" so the
  attacker "can continue to operate … even if the target system is restarted or
  if security measures are taken that would otherwise cut off their access" —
  the beachhead; **Account Manipulation (T1098):** attackers perform "constantly
  updating the password to avoid being detected by password duration policies"
  — an attacker *actively defeating credential-rotation defence*, the closest
  thing in the book to adapting to an MTD-like periodic reset; BITS Jobs create
  "long-standing jobs that persist even after the system reboots". →
  [`05_persistence`](../tactic_profiles/05_persistence.md) §3 (persistence is
  designed to *survive* disruption — a stolen-key-like reset-survivor, low reset
  probability; the account-manipulation-vs-rotation point is the sharpest
  MTD-interaction claim — persistence can adapt around a periodic reset).
- **Privilege Escalation (TA0004):** exploit-shaped ("exploit weaknesses,
  misconfigurations, and vulnerabilities … to gain elevated access"; BYOVD). →
  [`06_privilege-escalation`](../tactic_profiles/06_privilege-escalation.md) §2
  (confirms exploit-shaped, Tier-1 substrate-priced).
- **Defense Evasion (TA0005, "42 techniques"):** the pre-v19.1 umbrella —
  splits cleanly across the two v19.1 successors. **Hiding** goes to
  [`07_stealth`](../tactic_profiles/07_stealth.md): "conceal their presence …
  encryption and obfuscation … abuse trusted processes to hide and disguise
  their malware" (Deobfuscate/Decode, Masquerading, Indirect Command
  Execution). **Disabling** goes to [`08_defense-impairment`](../tactic_profiles/08_defense-impairment.md):
  "uninstalling or disabling security software to prevent it from detecting
  malicious actions." Selmanaj's lead example (Duqu token theft) is a *stealth*
  behaviour, not a disable — consistent with Step B's finding that the corpus's
  evasion-avoidant APT rarely *disables* defences.
- **Credential Access (TA0006):** Mimikatz credential dumping; OS credential
  dumping "used by attackers who have already gained access to a system with
  elevated privileges" (sequenced after PE). → [`09_credential-access`](../tactic_profiles/09_credential-access.md)
  §2/§3 (a stolen credential is the archetypal *reset-survivor* — survives an
  IP/topology shuffle; this is the book's clearest reset-immunity case).
- **Discovery (TA0007):** "the discovery phase can take a long time" — but
  scan-shaped in modality (map OS/software/open ports). → [`10_discovery`](../tactic_profiles/10_discovery.md)
  §2 (scan-shaped as modelled; the "can take a long time" tempers pure
  scan-speed — note the divergence like reconnaissance).
- **Lateral Movement (TA0008):** exploit remote services *or* reuse stolen
  credentials, then "pivot"; air-gap-crossing via removable media (T1091);
  **Use Alternate Authentication Material (T1550)** — Pass the Hash / Pass the
  Ticket / Web Session Cookie / Application Access Token: stolen auth material
  lets attackers "bypass normal access controls and log in as you, even if they
  don't know your password". → [`11_lateral-movement`](../tactic_profiles/11_lateral-movement.md)
  §2 (the fast-exploit↔stolen-credential duality flagged in Step B; reset
  behaviour depends on which — exploit-move is reset-vulnerable; credential-
  *and alternate-auth-material* moves survive a password/topology shuffle,
  sharpening the reset-survivor class beyond dumped passwords).
- **Collection (TA0009):** post-access; "compress and encrypt it before
  exfiltrating" (Archive Collected Data) — staging, objective-execution. →
  [`12_collection`](../tactic_profiles/12_collection.md) §2.
- **Command and Control (TA0011):** "establish C2 channels that mimic normal
  network traffic to avoid detection"; beacon/proxy/CDN-fronting. →
  [`13_command-and-control`](../tactic_profiles/13_command-and-control.md) §3
  (a C2 channel is IP/endpoint-bound — a shuffle can *sever* it, forcing
  re-establishment: reset-vulnerable, a key MTD-interaction claim). **Reset
  nuance (Proxy T1090, ~L2033):** proxies exist precisely to "provide
  resiliency in the face of connection loss" and to "ride over existing trusted
  communications paths"; CDN/domain-fronting routes C2 through legitimate
  shared infra — so C2 architectures are *built to survive connection loss*.
  The reset verdict is therefore **partial, not clean**: a shuffle disrupts but
  does not reliably invalidate C2 → wider sweep, not a hard reset.
- **Exfiltration (TA0010):** the low-and-slow objective mode — **Scheduled
  Transfer (T1029)**: "schedule a specific time or interval to steal the data
  so it looks like normal activity … during peak business hours … If data is
  being exfiltrated at random intervals, it can look suspicious … by scheduling
  the transfer, the attacker can make it appear … part of regular network
  traffic." → [`14_exfiltration`](../tactic_profiles/14_exfiltration.md) §2
  (direct support for the batched-low-and-slow end of the exfil width flagged
  in Step B — deliberately *paced*, not a burst).
- **Impact (TA0040):** the fast/noisy objective mode — ransomware ("Data
  Encrypted for Impact"), endpoint/network DoS, system shutdown/reboot;
  destructive and immediate. → [`15_impact`](../tactic_profiles/15_impact.md)
  §2 (the ransomware-burst end — contrasts with espionage-never; supports the
  wide objective-execution sweep).

**Disposition for this thesis:** verified [fetched] — behavioural/group
evidence for all 15 profiles; **no timing values** (a textbook, not a
measurement study). Each row informs §2 (group) and several inform §3 (reset
verdict); none lands a §4 number.

---

### Emergent idea — the reset verdict has a clean behavioural split in this text

**Source locator:** Ch. 4 synthesis (initial-access/persistence/credential-
access/C2 paragraphs) + Ch. 2 persistence characterisation

**Paraphrase:** reading Ch. 4 through the MTD-reset lens, the book sorts
tactics into two reset classes even though it never mentions MTD: gains that
are **infrastructure-bound and so reset-vulnerable** (initial-access foothold
"short-lived if the target changes…"; C2 channel that must "mimic normal
traffic" over a specific endpoint) vs gains that are **credential/host-bound
and so reset-surviving** (persistence "even if … restarted or if security
measures are taken"; a dumped credential that authenticates regardless of
topology). This is exactly the §3 reset-verdict axis, independently arrived at
from emulation practice — usable as the qualitative backbone for the declared
reset parameters.

**Maps to:** [`../handoffs/2026-07-03_l3_binding_scoping.md`](../handoffs/2026-07-03_l3_binding_scoping.md)
(the reset-verdict → binding) · every profile's §3.

**Disposition for this thesis:** adopted-as-argument (our synthesis; the book
does not frame it as MTD reset).

## Open questions / things to verify

- Table 2-1 body is parse-garbled past column 3 — the 416/243/229 and
  low-of-21 figures are from running prose and are safe; do not quote the
  missing intermediate years without the PDF.
- Selmanaj's per-tactic technique counts and introduction dates are
  ATT&CK-version-specific (the book's Ch. 4 Summary says "**14 tactics, 193
  techniques, 401 sub-techniques**" — pre-v19.1, before the stealth/
  defense-impairment split to 15). Treat counts as texture, not v19.1 truth.
- Chs. 5/9 (in-the-wild atomic procedures; adversary-profile methodology) not
  deep-read — they carry commands and process, not dwell values; revisit only
  if a per-technique command detail is ever needed.

## Out of scope for this thesis

Motivation taxonomy (Ch. 2 accidental/coercion/ideology/…); deception theory
(mimicry/fabrication/camouflage); attribution methodology (STIX/TAXII,
origin attribution, doxing); the framework tour (Ch. 3); the emulation-
operations half (Chs. 8–13: engagement planning, Splunk Attack Range, Prelude
Operator, reporting) — process, not per-tactic dwell evidence.
