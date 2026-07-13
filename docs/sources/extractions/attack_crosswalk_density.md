# ATT&CK ↔ CAPEC ↔ CWE ↔ CVE crosswalk density — extraction notes (survey-level)

> The published mappings between MITRE ATT&CK, CAPEC, CWE and CVE (CTID, BRON),
> and the coverage of ATT&CK by attack-graph rule bases (MulVAL, MAL/coreLang).
> Survey-level stub from OA sources via web search (July 2026). Load-bearing for
> the binding investigation's **position on the technique→CAPEC→CWE→CVE→CVSS
> chain** ([`../../implementation/pipeline/ogasp/binding_design_space.md`](../../implementation/pipeline/ogasp/binding_design_space.md)):
> it grounds the "sparse at every hop" verdict in reported coverage numbers
> rather than assumption (the gate-4 requirement).

## Bibliographic anchor

- **Citation keys**: `ctid_attack_cve`, `bron`, `mulval`, `mal_corelang`, `cve2capec`
- **Sources (web, survey-level; verify exact figures against primary before any
  dissertation citation)**:
  - CTID "Mapping ATT&CK to CVE for Impact" methodology + AttackIQ Academy course
    — <https://www.academy.attackiq.com/courses/mapping-mitre-attck-to-cve-for-impact>
  - BRON (bi-directional ATT&CK↔CAPEC↔CWE↔CVE graph), Hemberg et al. — arXiv:2010.00533
  - MulVAL, Ou et al., USENIX Security 2005 (OA) — <https://www.usenix.org/legacy/event/sec05/tech/full_papers/ou/ou.pdf>
  - coreLang (MAL), Katsikeas et al., *Computers & Security* 2024 — ScienceDirect (**PAYWALLED — on Marc's download list**)
  - CVE2CAPEC / Galeax (daily-updated CVE→CWE→CAPEC→ATT&CK DB) — <https://github.com/Galeax/CVE2CAPEC>
- **Acquisition status**: BRON/MulVAL/CVE2CAPEC OA; **coreLang (Computers &
  Security 2024) is paywalled → added to Marc's download list** (institutional
  access faster; see [`../../workflows/guardrails.md`](../../workflows/guardrails.md)
  acquisition split).

## Extraction policy

Survey-level, paraphrase-only; figures are as reported by secondary summaries and
marked **verify-before-citing** (papers-are-claims).

## Relevant artefacts

### Reported coverage figures (the "sparse at every hop" evidence)

- **ATT&CK ↔ CVE (CTID, expert-curated):** the curated mapping set is on the
  order of **~800 mapping objects covering ~419 unique CVEs** (reported against
  ATT&CK v15.1). This is a *tiny* fraction of the ~250 000+ CVEs in NVD — the
  curated join is deliberately narrow (impact-relevant, hand-mapped), not a
  dense automatic bridge. **verify-before-citing.**
- **CAPEC ↔ ATT&CK:** roughly **112 of ~546 CAPEC patterns** carry a direct
  ATT&CK mapping (~20%). **verify-before-citing.**
- **CWE ↔ ATT&CK (via CAPEC):** on the order of **41 CWEs → 89 techniques** in
  the CAPEC-derived path — a thin, indirect bridge. **verify-before-citing.**
- **MulVAL rule coverage of ATT&CK:** reported to cover **less than a quarter**
  of ATT&CK techniques.
- **MAL/coreLang:** the coreLang example implements on the order of **11 ATT&CK
  techniques** — an existence proof of technique→asset precondition modelling,
  not broad coverage.

### Transfer verdict for the technique→CAPEC→CWE→CVE→synthetic-CVSS chain

- **Verdict: DOES NOT TRANSFER as an MVP binding bridge; DEFER to future work.**
  Two independent reasons, either sufficient:
  1. **Terminus problem (decisive).** The chain terminates at a *CVE*, and the
     MTDSim substrate's vulnerabilities are **synthetic — no CVE keys**
     ([`../../implementation/substrate_primer.md`](../../implementation/substrate_primer.md) §(b).3).
     So even a perfect crosswalk yields a *label*, never a *join*: the best it
     can do is stamp a CWE/CAPEC-derived tag onto a synthetic vuln. A tag
     changes nothing behaviourally unless something *reads* it — and what would
     read it is the C3 policy layer, which is post-MVP.
  2. **Density problem (corroborating).** Every hop is sparse (figures above),
     so even the label would be low-confidence and low-coverage — many
     techniques reach no CVE at all through the published crosswalks.
- **Position:** the chain is **dissertation-defensible future work** (or a v1.1
  enrichment *if* the substrate ever adopts NVD CVEs — the trigger the primer
  §(b).3 and ch3 revisit-conditions already name), **not** the MVP semantic
  bridge. The MVP bridge is the direct hand-authored tactic→verb map (D6) plus
  the C2 capability contract. Any future tag overlay must hold the aggregate
  CVSS distribution fixed (metrics_semantics §(d) comparability invariant) so
  baseline MTTC is untouched.
- **What DOES transfer:** BRON/CVE2CAPEC are useful *inspection* tools to gauge,
  per technique, whether any CVE path exists — useful for the future-work
  feasibility check, not for the v1 pipeline (in-scope per the brief: inspect
  density, do not ingest).
