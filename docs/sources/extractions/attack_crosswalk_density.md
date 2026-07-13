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

### Transfer verdict for the technique→CAPEC→CWE→CVE→CVSS chain

> **Corrected 2026-07-13 (Marc):** the earlier "DOES NOT TRANSFER / decisive
> terminus problem" verdict is **withdrawn.** It assumed the substrate's vuln
> pool is a *fixed synthetic set to join onto*. If the pool is instead
> **constructed from** the crosswalk (seed real CVE/CWE/CVSS into MTDSim's
> `Vulnerability` model), the terminus problem dissolves — the join is native.
> And comparability with the frozen synthetic pool is now **secondary** (R4),
> not a gate. See the crosswalk-join investigation handoff.

- **Revised verdict: LIVE CANDIDATE, tractability-gated.** The chain is a real
  binding route once the substrate is *grounded in* the CTI ontology rather than
  joined onto a synthetic pool. What remains open is **not** feasibility of the
  idea but two empirical questions the join investigation must answer:
  1. **Coverage/tractability.** Every hop is sparse (figures above): how much of
     the ATT&CK technique set actually reaches a CVE *with a usable CVSS vector*
     through the published crosswalks (BRON / CTID / CVE2CAPEC)? The yield sets
     how much of the attacker's technique vocabulary can bind natively vs needs
     a fallback (hand-authored map or a **synthesis mapping layer**).
  2. **Seeding mechanics.** How a CVE's CVSS base vector maps onto the
     substrate's `complexity` / `impact` / `exploit_time` model
     ([`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)) —
     e.g. Attack-Complexity → `complexity`, impact metrics → `impact`.
- **Alternatives to the direct chain (also for the join investigation):** the
  **CWE/technique tag overlay** on an unchanged synthetic pool (comparability-
  safe but behaviourally thin — the tag can't correlate with complexity without
  moving the distribution); and a **synthesis mapping layer** (a designed
  intermediate representation mediating technique↔vuln, decoupling the attacker
  vocabulary from the pool's realism). Which is right is the join investigation's
  question, not settled here.
- **What DOES transfer:** BRON/CVE2CAPEC are useful *inspection* tools to gauge,
  per technique, whether any CVE path exists — useful for the future-work
  feasibility check, not for the v1 pipeline (in-scope per the brief: inspect
  density, do not ingest).
