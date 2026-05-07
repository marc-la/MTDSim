# References — External Candidates

**Source:** Personal curated notes (Adaptive MTD curated source notes, IDS-MTD nexus doc, MITRE ATT&CK / AE / PoP study notes)
**Compiled:** 29 April 2026
**Status:** Pre-screening. Companion to `references_candidates.md` (which extracts the prior-theses bibliographies). This file captures candidates that did NOT appear in any prior thesis bibliography.

> **Scoping note:** Excludes the 26 March meeting candidates (Zhang 2025 IoT Journal, Zang 2026, Rashid & Such 2025, Kim 2026, He 2025) — these were exploratory titles at the time, not endorsed candidates. They may resurface during external search if independently relevant. Excludes most IDS-MTD-specific candidates from the IDS-MTD nexus doc, since IDS will be folded into §1.3 lightly (≤2 paragraphs) rather than driving the lit review.

---

## 1. Foundational / canonical (high priority)

| # | Reference | Section | Notes |
|---|---|---|---|
| X1 | **Ghosh, Pendarakis, Sanders 2009** *Moving Target Defense Co-Chair's Report — National Cyber Leap Year Summit 2009* — NITRD technical report | §1.1 | Genesis of MTD. "Attacks only work once, if at all." Foundational — date irrelevant. Not in any prior thesis bibliography. |
| X2 | **Bianco, D. 2013/2014** *The Pyramid of Pain* — blog post (canonical reference) | §2.2, §3.2 | The PoP origin. Cited everywhere in industry, less in academic MTD work. **Will need careful citation** — is a blog, not peer-reviewed; Jin may want an academic uptake of PoP as the actual citation. |
| X3 | **Hutchins, Cloppert, Amin 2011** "Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains" — Lockheed Martin | §2.1, §2.3 | Cross-confirmed with Ho [20]. The Lockheed Cyber Kill Chain paper. |

---

## 2. CTI-derived attack profiling (§2.4 — currently sparse)

This category is the weakest in the prior theses' bibliographies. Worth direct search to strengthen.

| # | Reference | Section | Notes |
|---|---|---|---|
| X4 | **Rahman, M.R. et al. 2022** Co-occurrence / FP-Growth association rule mining on MITRE ATT&CK techniques | §2.4 | Direct match for "co-occurrence approach to edge derivation" you've been using methodologically. **Citation lookup needed** — confirm full author list, venue, year. |
| X5 | **MITRE Center for Threat-Informed Defense (CTID)** *Attack Flow* — schema and corpus reference | §2.4 | The structured-CTI grammar your GAP edges come from. Likely cite both the schema document and the corpus repo. Multiple possible primary references. |

> **Open gap:** No 2024–2026 CTI-fusion / threat-intelligence-aggregation paper currently identified. **Search target:** one paper for §2.4 strength. Candidates worth Connected-Papers checking: forward-citations on Rahman 2022, recent IEEE TIFS or *Computers & Security* papers on CTI graph construction.

---

## 3. ATT&CK limitations (supporting your §2.1 critical engagement)

Your study notes capture six MITRE limitations (coverage bias, temporal collapse, campaign weighting, ontology assumptions, probabilistic group attribution, observation-only). Each limitation needs a citation source. Most are *your synthesis* and would currently be uncited if asserted directly. Worth either:

- (a) Sourcing each from a published ATT&CK critique paper, or
- (b) Citing the original ATT&CK design papers (Strom et al. 2018) and noting "limitations identified through engagement with the framework" — this is honest and acceptable for honours.

| # | Reference | Section | Notes |
|---|---|---|---|
| X6 | **Strom, B.E. et al. 2018** "MITRE ATT&CK: Design and Philosophy" — MITRE technical report | §2.1 | The canonical ATT&CK design document. Often-cited primary source. |

> **Open gap:** A peer-reviewed *critical* paper on ATT&CK limitations would strengthen this section significantly. **Search target:** one paper. Candidates: critical surveys of MITRE / ATT&CK, possibly in *Computers & Security* or *ACM Computing Surveys*.

---

## 4. Adaptive / observation-driven MTD (§1.3 — selective additions only)

Per scoping note, IDS-MTD will not drive the lit review. Limit additions to one or two papers that genuinely add to §1.3 or §3.3 beyond what the prior theses cover.

| # | Reference | Section | Notes |
|---|---|---|---|
| X7 | **Celdrán, A.H. et al. 2024** RL framework with behavioural fingerprinting + MTD selection on IoT — *IEEE TIFS* | §1.3, §3.3 | Q1 venue. Recent (2024). Real-device deployment (vs simulation) — useful as evidence the field is maturing. Behavioural fingerprinting is closer to your gap argument (behaviour-aware) than most adaptive-MTD work. |
| X8 | **Cho, J.-H. & Ben-Asher, N. 2018** "Cyber Defense in Breadth" — Stochastic Petri Net integrated defence (also Dunstall [4]) | §3.3 | **Petri-net + MTD-adjacent.** Useful methodologically (your formalism choice has prior art) and lit-review-wise (integrated MTD defence with Petri-net evaluation). Cross-confirmed Dunstall. |

> **Excluded** from candidate list (per scoping note): Miehling 2018 POMDP, Hu/Zhu/Liu 2020 learning-POMDP, McAbee 2021, Hammar/Stadler 2022, DIVERGENCE/Yoon 2022, Smith 2016 GECCO, MASON/Chowdhary 2018, Sengupta 2018/2019 Stackelberg IDS-MTD, Mallmann 2021. These are good papers but their relevance hinged on the IDS-centric framing of the older proposal/lit-review plan. May resurface as methodology citations if Petri-net / POMDP framing intersects.

---

## 5. State-of-the-art MTD survey (§1.1 / §1.3)

| # | Reference | Section | Notes |
|---|---|---|---|
| X9 | **TBD — 2025/2026 MTD survey** | §1.1, §1.3 | Cho 2020 is canonical but six years old. A 2025/2026 survey is essential to demonstrate currency. Zhang 2025 *IEEE IoT Journal* is a candidate but venue (mid-tier) and IoT-specific framing may not fit. **Search target:** one paper, ideally in *IEEE COMST* / *ACM CSUR* / *Computer Networks*, 2025–2026, scope = MTD generally (not IoT-only / SDN-only). |

---

## Search budget for next session (~3 hours)

In priority order:

1. **MTD survey 2025–2026** (1 paper) — biggest single gap. ~30 min.
2. **Bianco PoP citation** (X2) — direct lookup. ~5 min.
3. **Rahman 2022 full citation** (X4) — direct lookup. ~5 min.
4. **Attack Flow primary reference** (X5) — CTID materials lookup. ~10 min.
5. **CTI fusion / graph construction paper, 2024–2026** (1 paper) — Connected Papers on Rahman 2022 + targeted search. ~30 min.
6. **ATT&CK critique / limitations paper** (1 paper, optional) — targeted search. ~20 min.
7. **One adaptive-attacker MTD paper, 2025–2026** to stress-test or strengthen the gap argument — Connected Papers on Ben-Asher 2016 (E10 in `references_candidates.md`). ~30 min.

**Buffer / breaks: ~50 min.**

**Stop conditions:** if any single search exceeds 30 minutes, note the gap and move on. If Connected Papers throws up rabbit holes, flag interesting clusters for *next* session and do not chase. Triage-then-search is the discipline; not search-then-search-more.

---

## Anchors confirmed

Per Marc's 29 April note:

- **Cho et al. 2020** (C1 in `references_candidates.md`) — primary canonical anchor
- **Tay 2024** (L1 in `references_candidates.md`) — direct UWA lineage anchor

Connected Papers runs on these two are the highest-leverage discovery moves remaining. **Run before next deep-read session begins.**
