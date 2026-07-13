---
status: open
created: 2026-07-13
---

# Anatomise the ATT&CK → CAPEC → CWE → CVE → CVSS join, reverse-engineer what actually maps, and assess the tractability of grounding MTDSim's vulnerability pool in it — the readings, coverage figures, and visualisations Marc needs to decide *how* attacker techniques meet the substrate (and whether "bind" is even the right frame)

> **This is a decision-support investigation, not a build and not the binding
> decision itself.** Its output is the material — the crosswalk anatomy, the
> honest coverage numbers pulled from the actual mapping data, worked
> technique→CVE→CVSS examples, seeding-tractability math, a reading list, and
> visualisations — that lets Marc choose a join strategy on evidence. It
> **precedes and feeds the re-run** of the binding investigation
> ([`../implementation/pipeline/ogasp/binding_design_space.md`](../implementation/pipeline/ogasp/binding_design_space.md),
> corrected 2026-07-13). Scoping/analysis only; no attacker build.
>
> **The reframe that motivates this handoff (Marc, 2026-07-13).** The binding
> investigation deferred the technique→CVE→CVSS route on a "terminus problem":
> MTDSim's vulns are synthetic (no CVE keys), so techniques have nothing to
> join onto. That reasoning assumed the pool is *fixed*. It is not — per **R4**
> ("simulation settings can be updated to suit the experiments"), comparability
> with the frozen synthetic pool is **secondary**, and re-baselining is an
> accepted operation. So the live move is to **construct** the pool *from* the
> crosswalk — seed real CVE/CWE/CVSS into the substrate — making the join
> native. **The question shifts from "how do I bind two fixed ontologies?" to
> "how, and how far, can I ground the substrate in the CTI ontology so the join
> is native — and where it can't reach, what mediates the gap?"** That last
> clause is why *bind* may be the wrong verb: a **synthesis mapping layer** (a
> designed intermediate representation) is a first-class candidate, not a
> fallback.

## State of play

- **The two ontologies and the missing join key.** The attacker speaks ATT&CK
  tactic/technique; the substrate speaks host/service/vulnerability with a
  **synthetic** CVSS-priced vuln model — `complexity ∈ [0.4,1]`,
  `impact = U[0,10]`, `cvss = (complexity+impact)/2`,
  `exploit_time = 15·(1−complexity)`, plus `dependent_vuln_id` preconditions
  ([`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
  `Vulnerability` / `ServicesGenerator`). No CVE key exists to join on — *today*.
- **The published crosswalks exist but are sparse at every hop** (survey-level,
  verify-before-citing — [`../sources/extractions/attack_crosswalk_density.md`](../sources/extractions/attack_crosswalk_density.md)):
  CTID's curated ATT&CK↔CVE ≈ 419 CVEs; ~112/546 CAPECs map to ATT&CK; a
  CAPEC-derived CWE↔technique path ≈ 41 CWEs → 89 techniques; MulVAL rule bases
  cover < ¼ of ATT&CK; coreLang ≈ 11 techniques. **BRON** is the bidirectional
  ATT&CK↔CAPEC↔CWE↔CVE graph; **CVE2CAPEC** (Galeax) is a daily-updated
  CVE→CWE→CAPEC→ATT&CK database; **NVD** carries CVE→CWE + CVSS vectors; **FIRST**
  owns the CVSS spec. These are the raw material to reverse-engineer.
- **Comparability is now secondary (R4), not a gate.** Zhang/Tay 1:1 comparison
  is already `INVALID` ([`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md)
  §d). Changing the vuln pool means **re-baselining** the goldens on the new
  substrate (a logged, accepted operation —
  [`../../baseline/CHANGELOG.md`](../../baseline/CHANGELOG.md)), not a
  prohibition. The one thing still cheap to preserve is the **6-phase baseline
  attacker as a comparison point** — re-run it on the new pool.
- **What "bind" competes with.** The corrected binding record's material-lever
  analysis stands: tactic→verb mapping (many-to-one or many-to-many) is *not*
  materially different from the phased attacker, because the substrate's verbs
  are data-coupled and only tempo really moves. **Vuln-level selection driven by
  technique is the lever that is genuinely not a re-skin** — which is exactly
  what a CVE-grounded (or synthesis-layer-mediated) pool would enable. That is
  the prize this investigation is sizing.

## Recommended approach

**Deliverable = one investigation record**
(`docs/implementation/pipeline/ogasp/technique_vuln_join_investigation.md` —
codebase-shaped, lives in `implementation/`) **+ committed visualisations**
(regenerable; gitignored `_viz/` for figures, with the generating script
tracked, mirroring the `data/*/​_viz` pattern) **+ extraction stubs** for every
load-bearing source (one per pass; OA fetched, paywalled onto Marc's download
list). Five passes:

**1 — Anatomise the chain, hop by hop.** For each hop
(technique↔CAPEC, CAPEC↔CWE, CWE↔CVE, CVE↔CVSS) record: what the relation
*means*, its cardinality (1:1 / 1:many / many:many), its direction(s), its
authority (MITRE-curated vs inferred vs ML-derived), and its known failure modes
(e.g. `NVD-CWE-noinfo`, un-mapped techniques). The point is a precise mental
model of *what a join actually is* at each hop before counting anything.

**2 — Reverse-engineer the real coverage (the honest yield).** Pull the actual
mapping data (BRON / CTID / CVE2CAPEC — all OA) and compute, don't assume:
- per-hop coverage (what fraction survives each hop), as a **funnel** from the
  ATT&CK technique set down to "techniques reaching ≥1 CVE with a usable CVSS
  base vector";
- the yield **restricted to the techniques this project actually uses** — the
  L3a place-union tactics and the GAP/GASP technique set
  ([`../../data/gap/`](../../data/gap/), [`../../data/gasp/`](../../data/gasp/)) —
  because global coverage is the wrong denominator; what matters is coverage of
  *our* attacker vocabulary;
- where the chain dies (which of *our* techniques reach no CVE), because those
  are exactly the techniques a synthesis layer or hand-authored fallback must
  cover.

**3 — Worked examples + seeding-tractability math.** Trace 3–5 of the project's
techniques end-to-end to concrete CVEs and their CVSS vectors. Then work the
**seeding map**: how a CVSS v3.1 base vector becomes the substrate's
`complexity` / `impact` / `exploit_time` — e.g. Attack-Complexity (L/H) and
Privileges/UI → `complexity`; the ISC impact sub-score → `impact`; and what
`dependent_vuln_id` preconditions could be grounded in (CWE chains? CVSS scope?).
State what is a clean mapping and what is a modelling choice.

**4 — Enumerate the join-strategy candidates and visualise the trade.** At least:
(a) **native CVE-grounded pool** (seed real CVE/CWE/CVSS; re-baseline); (b) **CWE/
technique tag overlay** on the unchanged synthetic pool (comparability-safe,
behaviourally thin — the tag can't correlate with complexity without moving the
distribution); (c) **synthesis mapping layer** (a designed intermediate
representation mediating technique↔vuln, decoupling attacker vocabulary from pool
realism — this is where "bind is the wrong verb" cashes out); (d) **hybrid**
(native where the crosswalk reaches, synthesis-layer where it doesn't). For each:
what it buys behaviourally (does technique-driven vuln selection actually
differentiate classes?), its build cost against the substrate's vuln model
file-by-file, its re-baseline cost, and its coverage ceiling from pass 2.

**5 — The reading list + visual deliverables, packaged for a decision.** The
figures Marc asked for: the **join graph** (the five node-types and their real
edges), the **coverage funnel/heatmap** (technique→CVE yield, ours vs global),
the **CVSS→substrate mapping diagram**, and a **distribution comparison** (the
current synthetic complexity/impact/CVSS distribution vs a CVE-seeded one, so the
re-baseline's magnitude is visible up front). Close with a **tractability verdict
per candidate** and the specific readings (papers/specs/datasets) Marc should do
before deciding — the investigation informs, it does not pre-empt the choice.

*Alternatives considered (for this handoff):* folding the join question back into
the binding re-run — rejected: the join is a deep sub-investigation with its own
data-wrangling and visualisation load; the binding re-run should *consume* its
verdict, not carry it. Skipping straight to seeding CVEs — rejected: coverage may
be too thin to be worth the re-baseline, and that is precisely what pass 2 must
establish before any build.

## Validation gate

Done when:
1. The record anatomises all four hops (meaning, cardinality, authority, failure
   modes) — pass 1.
2. Coverage is **computed from the actual mapping data**, not asserted, and
   reported both globally and **restricted to this project's technique set**, as
   a funnel with the dead-ends named — pass 2.
3. ≥3 techniques are traced end-to-end to concrete CVEs+CVSS, and the
   CVSS→`complexity`/`impact`/`exploit_time` seeding map is worked with each
   step marked *clean mapping* vs *modelling choice* — pass 3.
4. ≥3 join-strategy candidates (native / tag-overlay / synthesis-layer, +hybrid)
   each carry: behavioural payoff (does it beat a re-skin?), file-by-file build
   cost, re-baseline cost, coverage ceiling — pass 4.
5. The four visualisations exist and are regenerable (script tracked); the
   distribution-comparison figure makes the re-baseline magnitude visible.
6. A tractability verdict per candidate + a concrete reading list exist; the
   record explicitly **defers the join choice to the binding re-run**, stating
   what evidence would pick each candidate.
7. Extraction stubs exist for every load-bearing source; paywalled items on the
   download list.
8. Marc has reviewed the record. **No attacker/simulator build; no code beyond
   analysis/visualisation scripts and (optionally) read-only ingestion of the
   OA mapping data into a scratch/gitignored location.**

## Hard constraints

- **Analysis + visualisation only** — no replay attacker, no change to the
  substrate's `Vulnerability` model, no re-baseline *executed* (its cost is
  *estimated* here; the actual re-baseline rides with a future build once a
  candidate is chosen and signed off).
- **Comparability is secondary, not a gate (R4)** — do not resurrect the frozen-
  pool invariant as a blocker; do surface the re-baseline cost honestly so the
  decision is informed. Preserve only the *baseline attacker path* as a
  re-runnable comparison point.
- **Papers/data are claims** — BRON / CTID / CVE2CAPEC / NVD coverage numbers get
  reverse-engineered from the data and cross-checked; nothing external is cited
  without an extraction stub (one source per pass); the crosswalk-density stub's
  figures are survey-level until verified against the primary data.
- **ATT&CK ≠ CVE is a *modelling* boundary, not a prohibition here** — the whole
  point is to study the designed bridge; never silently treat a technique *as* a
  CVE, always through an explicit, coverage-quantified mapping.
- **Ingestion is inspection, not wiring** — pulling the OA mapping data to
  measure coverage and prototype the seeding math is in scope; wiring CVEs into
  the live pipeline is a future build gated on the binding re-run + supervisor
  sign-off.
- Envelope-not-actor phrasing; Australian English; branch hygiene; determinism
  where any script samples; **never push without an explicit ask**.

## Reading list

1. [`../implementation/pipeline/ogasp/binding_design_space.md`](../implementation/pipeline/ogasp/binding_design_space.md)
   — the corrected binding record (read the top **Correction** banner + §8);
   this investigation feeds its re-run.
2. [`../sources/extractions/attack_crosswalk_density.md`](../sources/extractions/attack_crosswalk_density.md)
   — the survey-level coverage figures to verify against real data, and the
   candidate-strategy sketch.
3. [`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
   — the `Vulnerability` / `ServicesGenerator` model the seeding map targets
   (complexity/impact/cvss/exploit_time/dependent_vuln_id).
4. [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md)
   §c/§d — what a pool change moves (exploit_time → MTTC) and why cross-paper
   comparability was already invalid (so re-baselining costs nothing you had).
5. [`../notes/ch3_design/structure_to_behaviour_binding.md`](../notes/ch3_design/structure_to_behaviour_binding.md)
   §"the binding, done properly" — the three binding levels; the
   vulnerability-instance binding this investigation makes tractable.
6. External (OA, fetch as needed): BRON (arXiv:2010.00533 + repo), CTID
   "Mapping ATT&CK to CVE for Impact", CVE2CAPEC (Galeax repo), the FIRST CVSS
   v3.1/​v4.0 specification, NVD CVE→CWE/CVSS schema.

## Out of scope (explicitly)

- **Choosing the join strategy** — that is the binding re-run's call, informed
  by this record. This investigation enumerates and sizes; it does not decide.
- **Building the replay attacker or any pipeline wiring** — deferred
  ([`./2026-07-03_l3_replay_attacker.md`](./2026-07-03_l3_replay_attacker.md)).
- **Executing a re-baseline** — its cost is estimated here; the actual golden
  re-capture rides with the chosen build.
- **R2 success-rate / R3 styles** — the operationalisation handoff
  ([`./2026-07-13_l3_tactic_operationalisation.md`](./2026-07-13_l3_tactic_operationalisation.md)).
- **Timing calibration, detection/IDS, two-way coupling** — standing deferrals
  (R1 / D6 / D2/D10).
