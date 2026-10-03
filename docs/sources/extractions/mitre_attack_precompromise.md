# MITRE ATT&CK — pre-compromise visibility: extraction notes

> The MITRE Corporation. *MITRE ATT&CK*, Enterprise domain, knowledge base, https://attack.mitre.org (pages fetched 2026-10-03).
> Source: the live ATT&CK pages below (open access; no local markdown copy).
> Relevance to this thesis: §4.1 ¶4, the claim that reconnaissance and resource development lie outside what the defender can observe, so CTI rarely records them, which is why the attack graph is sparsest before initial access.

## Bibliographic anchor

- **Citation key**: `mitre2026attackkb` (the pinned v19.1 knowledge-base entry; the bib note forbids per-page cites, so these pages are cited through it)
- **Pages read**: T1595 Active Scanning (last modified 24 Oct 2025); T1583 Acquire Infrastructure (last modified 24 Oct 2025); TA0042 Resource Development (v19, 25 Apr 2025); M1056 Pre-compromise (v1.1, last modified 12 May 2026)

## Extracts

**Outside the defender's controls.** The mitigation text on both a Reconnaissance technique (T1595) and a Resource Development technique (T1583) says:

> "This technique cannot be easily mitigated with preventive controls since it is based on behaviors performed outside of the scope of enterprise defenses and controls." (T1595, T1583, Mitigations: M1056)

**Detection moves to later stages.** On T1583:

> "Detection efforts may be focused on related stages of the adversary lifecycle, such as during Command and Control." (T1583, Detection)

**Scope of the pre-compromise mitigation.** M1056 covers the Reconnaissance (26 techniques) and Resource Development (11 techniques) tactics, and describes them as "the Reconnaissance and Resource Development phases of an attack".

## What it supports, and what it does not

- Supports, as a paraphrase with a plain cite: pre-intrusion activity happens largely outside the scope of the defender's controls, and detection of it falls to later stages of the attack.
- Does **not** say that CTI analysts infer pre-intrusion activity, or how often CTI reports it. "CTI records it only where analysts infer it" (Marc's dictated point, 2026-10-03) needs its own source or stays off the page.
- Checked against the pinned v19.1 STIX bundle (`data/gap/_attack/enterprise-attack-19.1.json`): the "outside of the scope of enterprise defenses and controls" sentence is present, on 88 mitigation relationships. The detection sentence was checked on the live site only.
