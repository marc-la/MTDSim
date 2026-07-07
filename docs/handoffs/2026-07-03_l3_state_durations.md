---
status: open
created: 2026-07-03
updated: 2026-07-07
---

# Build the per-tactic dwell profiles → the state-duration catalogue: operational-validation method, group anchors, and a mechanical research protocol

> **Method / the bar:** [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> **Why the gap is real:** [`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../notes/2026-07-04_tactic_duration_precedent_survey.md).
> **Scaffolding to fill:** [`../tactic_profiles/`](../tactic_profiles/) (README + template + 15 stubs).
> Runs parallel with [`./2026-07-03_l3_weighted_nets_aggregate_profile.md`](./2026-07-03_l3_weighted_nets_aggregate_profile.md);
> both feed [`./2026-07-03_l3_timeline_runner.md`](./2026-07-03_l3_timeline_runner.md).
> MTD-interaction sections feed [`./2026-07-03_l3_binding_scoping.md`](./2026-07-03_l3_binding_scoping.md).

## State of play

- **Step F is DONE (2026-07-07) — §5 filled for all 15 profiles; ONLY THE CATALOGUE REMAINS.**
  Every `docs/tactic_profiles/*.md` now has §5 (catalogue inputs): group
  (confirm/overturn) + relative multiplier + sweep range + tier + a one-paragraph
  justification. **The scheme calibrates 4 group anchors, not 15 free dwells**
  (identifiability, per the method note): **scan-shaped** (recon, discovery) and
  **exploit-shaped** (initial-access, privesc, credential-access, lateral-movement)
  are **Tier-1 substrate-fixed, ×1.0, *not tuned*** (tracing to the
  `ATTACK_DURATION` scan verbs / complexity-scaled `exploit_time`);
  **stealth-low-and-slow** (stealth = reference, persistence, C2, + execution/DI)
  is **Tier-3 tuned** (k× exploit median); **objective-execution** (collection,
  exfiltration, impact) is **Tier-2 literature-calibratable** (macro
  access→exfil / time-to-impact milestones as an *outer envelope*, shape-not-scale);
  **prep-off-network** (resource-development) is **×0 near-zero** (off-clock).
  **Within-group multipliers are ×1.0** except the two **genuinely-unsettled**
  tactics — `execution` and `defense-impairment` at **×0.5** (fast-verb /
  punctuated-decisive reading, widest sweeps skewing toward fast) — and
  resource-dev ×0. **No group hypothesis was overturned; none moved tier.**
  **Sweep ladder:** moderate ×0.5–×2 (substrate-anchored or floor-bounded), wide
  ×0.25–×4 (least-observable stealth tactics + character-wide
  lateral-movement/exfil), widest ×0.1–×4/×5 (`defense-impairment`, `impact`).
  **The §5 sweep is on the *duration*; the §3 reset verdict
  (survivor/vulnerable/partial/null + its own band) is a *separate* declared
  parameter that feeds the L3b binding, not the catalogue** — stated in each
  justification so the two artefacts stay distinct. The crown-jewel per-modality
  split is carried into §5 where it lives ([[09_credential-access]] survivor pole,
  [[01_reconnaissance]]/[[10_discovery]] vulnerable pole,
  [[11_lateral-movement]]/[[12_collection]] split-inside). **Files stay
  `status: stub`** — per this handoff's own rule the flip **stub → reconciled**
  happens *with the catalogue* (validation gate), not at Step F; §5 is complete in
  substance and ready to distil. **Not done:** the catalogue itself
  (`data/ogasp/tactic_durations.json` + provenance rows) — the one remaining step.
- **Step E is DONE (2026-07-07) — §3 written for all 15 profiles.**
  §3 (MTD interaction / reset verdict) is now filled in every
  `docs/tactic_profiles/*.md` as thesis prose, organised on the
  **survivor-vs-vulnerable reset axis** and argued from the substrate primer §(e).
  Structure per profile: what gain the tactic produces (position/knowledge vs
  capability/credential) → its reset direction off the substrate model → which MTD
  action bites + how hard → sweep width → the honest not-captured boundary (rubric
  crit. 3/4/6, with crit. 7 discrimination hooks where they exist). The **crown-jewel
  per-modality split is foregrounded**: [[09_credential-access]] (survivor pole),
  [[01_reconnaissance]]/[[10_discovery]] (vulnerable pole),
  [[11_lateral-movement]]/[[12_collection]] (split *inside* the tactic:
  scan/remote-share hop resets, credential/local-read survives). The three open
  contests are foregrounded, not resolved: [[05_persistence]] (FlipIt rate contest;
  and the literature verdict *diverges* from the substrate, which implements no
  eviction op — recorded), [[13_command-and-control]] (architected to survive
  connection loss; substrate *over-resets* it vs reality), [[04_execution]]
  (circumvention-vs-probing left open). [[02_resource-development]] written as the
  **inert null verdict** (off-network, reset-immune); [[08_defense-impairment]] and
  [[12_collection]] written **mechanism-first** — 08's verdict (host-local disabled
  control survives a shuffle, invalidated only by reimage/OS-diversity-as-reprovision;
  the substrate models *no* defences to disable) folds a background P2-mining agent's
  code-level + literature findings; 12 is the local-survivor/remote-vulnerable split.
  **P0.3 done:** orphan whole-chain macro rows demoted to a labelled
  "operational-validation outer envelope" caption under §4 in 03/04/05/09/11/14/15
  (this also discharges the P3 detection-regime-mismatch examiner hit). **Files stay
  `status: stub`** — §5 (Step F) is still empty, so they are not yet `drafted`; do
  **not** flip status until Step F + the catalogue land (validation gate). What was
  *not* done: no fresh deep P2 mining/extractions for 08/12 beyond the one background
  agent — §3 is declared-from-mechanism and the reset *direction* is substrate-fixed,
  so deeper IR-case grounding remains available if Marc wants it but was judged
  disproportionate per the strategic note (the runner is the load-bearing evidence).
- **Step E reframed + substrate primer written (2026-07-07).** A purpose/rubric/review
  session established that **§3
  (Step E) is the thesis's novel object, not a catalogue chore**: it is the
  per-tactic *APT × dynamic-network interaction* — what a defensive mutation does
  to the attacker's gain — and it is **empty in all 15 profiles**. Three new
  artefacts now govern Step E (read them first):
  - [`../notes/2026-07-07_thesis_backbone_rubric.md`](../notes/2026-07-07_thesis_backbone_rubric.md)
    — the rubric §3 is written to (5 framing claims + 7 per-tactic criteria mapped
    to the five themes: adversarial modelling, attack simulation, APT behaviour,
    MTD, dynamic networks). Also critiques the question set that motivated the reframe.
  - [`../notes/2026-07-07_cross_sectional_review.md`](../notes/2026-07-07_cross_sectional_review.md)
    — a four-lens review (black/grey/white-box + adversarial examiner) of the 15
    profiles: the per-tactic disposition, the prioritised **P0–P3 action list**,
    and the examiner vulnerabilities (V1–V5).
  - [`../specs/substrate_primer.md`](../specs/substrate_primer.md) — the
    non-implementation-specific attacker's-eye view of the substrate. **§(e) is the
    reset model every §3 argues from**; §(d) is the inherited-attacker tradeoffs +
    the improvement-over-prior argument (the "MTD that outpaces smash-and-grab may
    lose to a slow objective-driven attacker" punchline).
  **Crown-jewel finding (three independent reviewers converged):** the reset verdict
  splits by *what kind of gain a tactic produces* — **capability/credential state
  survives a mutation; network-position state is invalidated** — and this is
  **already implemented in the substrate** (network-layer mutation resets
  position/target and forces re-scan; application-layer mutation resets only the
  exploit working set on a *retained* foothold; compromised hosts + harvested
  credentials survive everything). §3 is written *around this axis* and *checked
  against the substrate model*, not as 15 free-floating verdicts. **User decisions
  this session:** §3 prose lives *inside the profile files* (single source of
  truth); the substrate primer was written first (done). The next concrete action
  is the Step-E exemplar — see Steps-remaining item 1.
- **Steps A, B, C & D are DONE (A/B 2026-07-04; C 2026-07-05; D 2026-07-06) —
  resume at Steps E then F.** All 15 `docs/tactic_profiles/*.md` now have **§1
  (tactic & role)** [Step A] plus **§2 (group-assignment argument)** and **§4
  (timing evidence table)** filled and enriched [Steps B+C+D]. Files stay
  `status: stub` — §3 (Step E) and §5 (Step F) are still empty, so they are not
  yet `drafted`.
- **Step D is DONE (2026-07-06).** The full external-search corpus (~60 sources
  in `docs/sources/tactic_profiles/step_d/`, 16 subdirectories) was dissected
  full-text into **17 new consolidated extractions** and folded into all 15
  profiles' §4 (with §2/§3-relevant framing carrying a `→§3` pointer, house style).
  New extractions: `internet_scanning_empirics`, `mtd_scan_disruption`,
  `resource_dev_timing`, `initial_access_timing`, `evans2011_mtd_effectiveness`,
  `ransomware_timing`, `persistence_reset_models`, `apt_campaign_duration`,
  `mttc_lineage`, `ad_time_to_domain_admin`, `mtd_stealth_effectiveness`,
  `password_rotation_efficacy`, `credential_use_timing`, `worm_propagation_models`,
  `collection_exfil_timing`, `c2_beaconing`, `timed_attack_models` (+ ReliaQuest
  folded into `breach_reports_macro_timing`). **Load-bearing new evidence for
  Steps E/F:** (i) the **§3 reset verdict is per-modality and rate-dependent, never
  clean** — Evans 2011 (dynamic diversity gives *no* advantage vs
  circumvention/deputy attacks, incl. fileless/script execution; significant only
  vs incremental probing at a high re-randomisation rate — 6 orders of magnitude
  across every-4th vs every-100th probe), FlipIt (higher-move-cost player →
  benefit 0), Crouse/Carroll (reset governed by shuffle-interval ÷ attacker-wait,
  e⁻¹≈0.63 ceiling), Reti's NASim (interval-25 → scan-agent win-prob 0);
  (ii) **credential-access is the clearest reset-*survivor*** — Zhang-Monrose-Reiter:
  password rotation revokes a captured credential in only a minority (41% offline
  / 17% online broken), and stolen credentials survive a topology shuffle;
  (iii) **empirical timing anchors** — recon scan months→minutes + 24–48 h onset
  (Durumeric); resource-dev 22-day 0-day-dev / days-scale infra (RAND, Hao);
  fast entry (DBIR 21 s click, Mandiant TTE 63→5 days); lateral fast-worm pole
  (Slammer 90% in 10 min; ReliaQuest breakout 34 min/4 min); C2 beacon 2 s–2 h+;
  exfil floor (Equifax 76 d ↔ 1.2 h fastest); ransomware encryption 52 s–~2 h;
  campaign duration 1 d–5 yr / 137 d avg; (iv) **Holm 2014** flags the substrate's
  inherited *exponential* TTC as empirically suspect (heavy-tailed Pareto/lognormal
  fits better) — a claim for Marc, not actioned; (v) **method precedent widened** —
  Madan 2004 semi-Markov MTTSF + the MAL/SPN/CTMC cluster (`timed_attack_models`)
  reinforce declare-per-state-time + sweep-the-interval as the field norm. **Two
  file/manifest mismatches flagged** (not laundered): `S0951832018304125` is a
  reliability-redundancy/PSO paper, not Lalropuia's stochastic game (re-fetch
  needed); `S0045790626000315` is Davies ransomware benchmarking, not a timed model
  (routed to `ransomware_timing`). One `[search]` remains reconciled to primary
  (Bromiley, `12_collection`).
- **Step C is DONE (2026-07-05).** The eight known-but-not-yet-extracted sources
  named in Step C (Selmanaj book, Ling & Ekstedt 2023, McQueen 2006, Xiong 2021,
  plus the macro targets M-Trends, CrowdStrike GTR, Sophos AAR, DFIR Report) were
  fetched to `docs/sources/tactic_profiles/step_c/` (gitignored) and dissected
  full-text into **seven new extractions** —
  [`../extractions/ling2023.md`](../extractions/ling2023.md),
  [`../extractions/mcqueen2006.md`](../extractions/mcqueen2006.md),
  [`../extractions/xiong2021.md`](../extractions/xiong2021.md),
  [`../extractions/selmanaj2024.md`](../extractions/selmanaj2024.md),
  [`../extractions/syed2025.md`](../extractions/syed2025.md),
  [`../extractions/chemat2024.md`](../extractions/chemat2024.md), and the
  consolidated [`../extractions/breach_reports_macro_timing.md`](../extractions/breach_reports_macro_timing.md).
  Five independent completeness-critic agents (ling, xiong, mcqueen, selmanaj,
  macro) re-read the primaries; misses folded in. **New §4 rows added to all 15
  profiles** and the two `[search]` macro rows (exfiltration, impact) reconciled
  to `[fetched]` from the primary vendor reports. **Load-bearing new evidence:**
  (i) the empirical per-technique method (ling2023) **degenerates to a shared
  6-day expert floor** and **structurally cannot price C&C or the hiding half of
  evasion** — reinforcing group anchors over per-tactic values and Tier-3 for
  C2/stealth; (ii) McQueen's **21-day (expert) no-known-vuln dwell** is a
  declared per-stage dwell precedent + order-of-magnitude envelope; (iii) the
  macro milestone chain now anchors the objective tactics — **breakout 29 min /
  27 s** (access→lateral), **access→AD ~3–16 h**, **access→exfil ~73–79 h**,
  **TTR 2 h→328 h**, **dwell 14 d global / 122 d espionage / ~400 d edge**;
  (iv) the **C2 reset verdict softened to *partial*** (proxies/CDN-fronting give
  "resiliency in the face of connection loss"); (v) **persistence can adapt
  around a periodic reset** (account-manipulation defeats password-rotation) —
  both feed Step E's §3. The precedent-survey note is updated (all `[search]`→
  `[fetched]` except Secureworks/IBM/Unit 42, not needed).
- **Step B is DONE (2026-07-04).** §2/§4 filled for all 15 from a full read of the
  in-corpus set (alshamrani2019 read cover-to-cover as the backbone; al-sada2024,
  cho2020, bland2020, rodriguez2024, hong2018, ghosh2009, brown2023, jalowski2026,
  bianco2013, sadlek2022, outkin2023, mendonca2023, he2025, tay2024, attackflow,
  ferraz2024, zhang2025attackg read/triaged). Two independent completeness-critic
  agents re-read alshamrani2019 and cho2020 against the source; their misses were
  folded in (recon "passive" corrected to *non-exploitative* not scan-free; C&C
  beacon cadences, Stuxnet worm-lateral, RSA exfil, pre-OS persistence, and the §V
  synthetic-model caveat added). Every §4 row is `[fetched]`/`[search]`-flagged and
  cites an extraction + section locator; cho2020/outkin2023 locators verified
  against the primary source. **Findings that change the group bets:** `execution`
  and `defense-impairment` are flagged as **genuinely unsettled groups** (execution
  is a fast verb wearing a stealth wrapper; the corpus's evasion-avoidant APT rarely
  *disables* defences) — both carry a **wide sweep** into §5. `lateral-movement` and
  `exfiltration`/`impact` widened (fast-worm↔slow-manual; batched low-and-slow spread;
  ransomware-burst↔espionage-never). The **backbone extraction**
  [`../extractions/alshamrani2019.md`](../extractions/alshamrani2019.md) gained a
  per-tactic dwell/MTD-effect/synthetic-caveat block mapping to all 15 profiles.
  **§3 evidence is already gathered** (MTD reset-verdict table + the alshamrani
  §IV-C-2-B "renders exploratory knowledge useless" money-quote + cho2020 critic's
  inside-attacker/beyond-recon findings) and staged for Step E — see the extraction
  and the session's working matrix; do not re-mine the MTD papers.
- **The gap is confirmed, not assumed.** A four-angle precedent survey
  (2026-07-04) established that **no prior work assigns justified per-ATT&CK-*tactic*
  durations**: the one tactic-level ATT&CK Petri-net model (Rodríguez 2024) is
  *untimed*; timed APT models attach timing at technique/CVE level (Ling &
  Ekstedt 2023) or **declare** their rates (Bland 2020: "arbitrary rates … later
  determined by SMEs", net structure face-validated by 14 experts; McQueen 2006:
  a stage mean set "somewhat arbitrarily"; enterpriseLang/MAL: expert-declared
  per-technique TTC). **Declare-and-sweep is the field norm** — this work executes
  it and adds a calibration step. No adversary-emulation framework (Caldera, ART,
  CTID library, …) attaches per-phase dwell either. Full survey + citations:
  [`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../notes/2026-07-04_tactic_duration_precedent_survey.md).
- **Method decided (operational validation).** Unobservable per-tactic dwells are
  free parameters; calibrate them so the *emergent timeline shape* reproduces
  literature-reported campaign patterns (dwell, breakout, time-to-exfil), then
  sweep. Calibrate **~4 group anchors, not 15 independent dwells** (identifiability).
  Shape-not-scale: literature sets *relative* structure, the substrate anchors
  *absolute* scale. Anti-circularity rules (don't tune the anchor; group; hold out
  an observable; keep the claim modest) are in the method note.
- **The state set is 15 tactics — ATT&CK Enterprise v19.1.** The place-union
  across the five L3a nets is 15 because **v19.1 split `defense-evasion` (TA0005)
  into `stealth` (TA0005) + `defense-impairment` (TA0112)**. Confirmed against
  [`../../data/ogasp/`](../../data/ogasp/). The full keyed list with group/tier
  hypotheses is the [`../tactic_profiles/README.md`](../tactic_profiles/README.md)
  table. Pinned bundle:
  [`../../data/gap/_attack/enterprise-attack-19.1.json`](../../data/gap/_attack/enterprise-attack-19.1.json).
- **Two-stage artefact.** The **profiles** (`docs/tactic_profiles/*.md`) are the
  evidence layer; the **catalogue** (`data/ogasp/tactic_durations.json`) is the
  machine artefact distilled from their §5. Profiles come first.
- **Substrate prices its own verbs** (unchanged): `ATTACK_DURATION`
  ([`../../mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py) ~L140)
  + complexity-scaled `exploit_time`
  ([`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)).
  Scan/exploit-shaped tactics inherit these (Tier 1, *not tuned*).
- `observation_count` must **never** leak in as a timing signal
  ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f)).

## Steps remaining (as of 2026-07-07)

Evidence-gathering (Steps A–D) is complete and **Steps E and F are done** (all five
sections §1–§5 filled for all 15). **One thing remains: the catalogue.**

1. **The catalogue — `data/ogasp/tactic_durations.json` + provenance rows**
   (detail under "Then the catalogue" below). Distil §5 into the machine
   artefact; every place-union tactic gets an entry; fill the `pending` regime
   row in [`../specs/provenance.md`](../specs/provenance.md). The §5 group +
   relative-multiplier + sweep + tier are the direct inputs; the four group
   anchors default **uncalibrated** in v0 (calibrate within ranges when the runner
   lands). Carry the §5 scheme recorded in the Step-F state-of-play bullet: two
   substrate-fixed Tier-1 anchors (scan, exploit, ×1.0, not tuned), the Tier-3
   tuned stealth anchor, the Tier-2 objective anchor, and prep-off-network ×0; the
   two unsettled tactics (`execution`, `defense-impairment`) at ×0.5 with the
   widest sweeps. **The §3 reset verdict is a separate parameter for the L3b
   binding — do not fold it into `duration_s`/`sweep_range`.**

**Strategic note (2026-07-07 examiner review — read before over-investing in prose).**
Step E's §3 and the catalogue *defend* the thesis's finding but do not *produce*
it. The two objections that can actually fail a viva — **(V1)** the novel object
rests on declared dwell × declared reset fraction; **(V2)** "fidelity changes the
answer" is parameter noise unless the ranking-change *survives its own sweep band
and is distinct from the generic attacker's stable ranking* — are discharged only
by **running the discrimination probe + sweep** (downstream:
[`./2026-07-03_l3_timeline_runner.md`](./2026-07-03_l3_timeline_runner.md) + the
CTI-note §10 probe). Write §3 well — it is genuinely the thesis's novel object —
but hold that the runner/probe is the load-bearing *evidence*, not the prose. The
per-modality reset split (the crown jewel) is the strongest genuinely-owned,
falsifiable claim; foreground it.

Only after the catalogue (Step F is done): flip profiles `stub` → `reconciled` and
clear the Validation gate. **This handoff is deleted in the commit that ships the
catalogue** (session-workflow lifecycle).

## Recommended approach

**Do the 15 profiles first (mechanical, below), then distil the catalogue.** The
profiles turn "declare a number" into "synthesise the evidence, then declare a
group + ratio the evidence supports". Then catalogue v0 (uncalibrated priors +
ranges) unblocks the runner; calibrate the group anchors when the runner lands;
freeze v1.

### The mechanical research protocol — run this per tactic

For each `docs/tactic_profiles/NN_<tactic>.md`, work the sources **in this order**
and fill the five sections. Stop when §3 and §5 are complete and §4 has at least
the ATT&CK page + one in-corpus check (a "no direct value" row is a valid,
gap-documenting result). Page limit: 1–2 pages.

**Step A — Primary ATT&CK (fills §1).** **[DONE 2026-07-04 — all 15; committed `cb6da8a`.]** Fetch the tactic's page
`https://attack.mitre.org/tactics/<ID>/` (v19.1). Definition, technique list,
procedure examples. For `stealth` / `defense-impairment`, read *both* and split
the old-`defense-evasion` scope between them (see the v19.1 note in each stub).

**Step B — Mine the in-corpus extractions first (fills §2, §4).** **[DONE 2026-07-04 — all 15;
§2/§4 filled, alshamrani2019 extraction enriched, §3 evidence staged for Step E.]** These are
already reconciled — grep each for the tactic and for any timing/behaviour claim
before searching externally:
- *APT lifecycle & behaviour:* `alshamrani2019` (APT lifecycle survey — prime
  source for phase behaviour/low-and-slow), `al-sada2024`, `cho2020`.
- *Executed / timed attacker models:* `bland2020` (SPN — how it sourced timing),
  `rodriguez2024` (tactic Petri nets — untimed, confirms gap), `tay2024`.
- *MTD mechanism & effect:* `hong2018`, `he2025`, `mendonca2023`, `ghosh2009`,
  `outkin2023`, `sadlek2022` — for §3 (which MTD action disrupts what).
- *CTI structure / adaptivity:* `attackflow`, `zhang2025attackg`, `brown2023`,
  `bianco2013` (pyramid of pain — cost-to-attacker), `jalowski2026` (adaptive).

**Step C — Known-but-not-yet-extracted (fills §4).** **[DONE 2026-07-05 — all 15;
committed `f0e86ed`.]** Selmanaj book, Ling & Ekstedt 2023, McQueen 2006, Xiong 2021
(SoSyM + CSIMQ), and the macro targets (M-Trends, CrowdStrike GTR, Sophos AAR, DFIR
Report) fetched to `docs/sources/tactic_profiles/step_c/` (gitignored) and dissected
full-text into seven extractions — [`../extractions/ling2023.md`](../extractions/ling2023.md),
[`../extractions/mcqueen2006.md`](../extractions/mcqueen2006.md),
[`../extractions/xiong2021.md`](../extractions/xiong2021.md),
[`../extractions/selmanaj2024.md`](../extractions/selmanaj2024.md),
[`../extractions/syed2025.md`](../extractions/syed2025.md),
[`../extractions/chemat2024.md`](../extractions/chemat2024.md), and the consolidated
[`../extractions/breach_reports_macro_timing.md`](../extractions/breach_reports_macro_timing.md).
§4 rows added to all 15; the two `[search]` macro rows reconciled to `[fetched]`.
One `[search]` remains by design (the Bromiley/SANS hacker survey in
[`12_collection`](../tactic_profiles/12_collection.md), second-hand via ling2023).

**Step D — Targeted external search (fills §4).** **[DONE 2026-07-06 — the full
~60-source corpus in `docs/sources/tactic_profiles/step_d/` dissected full-text
into 17 consolidated extractions + folded into all 15 profiles' §4; see the
Step-D bullet in the state-of-play above. Two file/manifest mismatches flagged for
re-fetch.]** Mechanical search strings, substitute `<TACTIC>` (and for the split
tactics, run once for each of "defense evasion", "stealth", "impair defenses"):
- APT behaviour/dwell — `APT "<TACTIC>" dwell OR duration OR "how long" campaign`
- Simulation/emulation — `"<TACTIC>" attack simulation OR emulation MITRE ATT&CK timing`
- MTD interaction — `moving target defense "<TACTIC>" attacker effect OR reset OR shuffle`
- Empirical timing — `"<TACTIC>" time-to OR median hours OR days breach incident report`
- Academic rates — `"<TACTIC>" stochastic petri net OR CTMC OR "mean time" transition rate`
Anything usable that isn't already an extraction → add a `docs/extractions/`
stub and reconcile (papers are claims). Do **not** cite a `[search]` snippet in
§5 without reconciling it first.

**Step E — Reason from mechanism (fills §3). [REFRAMED 2026-07-07 — now the
thesis's novel object; see the top state-of-play bullet + Steps-remaining item 1
for the operative guidance.]** No literature grounds the MTD→attacker *magnitude*
(the genuine unknown,
[`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md) §5),
but the reset *direction* is fixed by the substrate model
([`../specs/substrate_primer.md`](../specs/substrate_primer.md) §(e)). Argue from it
on the **survivor-vs-vulnerable axis**: does the gain this tactic produces
(position/knowledge vs capability/credential) get **invalidated** by a mutation or
**survive** it? That verdict + its uncertainty set the sweep width. Declared, not
claimed — and checked against the substrate's own reset model.

**Step F — Distil §5. [DONE 2026-07-07 — all 15; see the Step-F state-of-play
bullet.]** Group (confirm/overturn the stub's hypothesis) + relative
multiplier + sweep range + tier + a one-paragraph justification. This paragraph
is the deliverable.

### Then the catalogue

Commit `data/ogasp/tactic_durations.json`: per tactic —
`{group, relative_multiplier, duration_s, tier, source (constant-name |
profile-file §ref | extraction §ref), justification, sweep_range}`. The
`justification`/`source` point back at the profile file. Every one of the 15
place-union tactics gets an entry. Add the matching row block to
[`../specs/provenance.md`](../specs/provenance.md) (the regime row is already there,
`pending` — fill the pointer). Group anchors default uncalibrated in v0; calibrate
within ranges once the runner exists; freeze v1.

*Alternatives considered:* 15 independent point durations (rejected —
unidentifiable against ~3 macro observables; group anchors instead); corpus/
`observation_count`-derived timing (rejected — not a rate); absolute-time realism
(rejected — breaks substrate comparability; shape-not-scale instead); deferring
until the binding lands (rejected — the runner needs v0, and Tier-1 needs only the
draft tactic→verb map the binding-scoping handoff produces early).

## Validation gate

Done when:
1. All **15** `docs/tactic_profiles/*.md` are `status: reconciled` — five sections
   filled, `[search]` claims reconciled, §5 complete. Key set matches the
   `data/ogasp/` place-union (mechanical test).
2. `data/ogasp/tactic_durations.json` covers every place-union tactic; a test
   cross-checks the key set against the structural JSONs.
3. Every catalogue entry has `group + tier + source + justification + sweep_range`;
   no value derives from `observation_count` or any corpus frequency (assert/grep).
4. Tier-1 tactics trace to a substrate constant and are flagged *not tuned*;
   tuned tactics name their group anchor.
5. Provenance rows in [`../specs/provenance.md`](../specs/provenance.md), approved
   by Marc. Units explicit (seconds, matching `env.timeout`), sane vs
   `ATTACK_DURATION` magnitudes.

## Hard constraints

- **Timing never comes from the corpus** — structure/chaining is CTI's
  contribution; timing is substrate/literature/declared. Breach-report *statistics*
  (M-Trends etc.) are Tier-2 literature and **are** allowed — that is not the
  corpus ([`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md) §5).
- **No GSPN/SPN/TPN semantics** — plain per-state dwell only (D10 deferral).
- **Papers are claims to reconcile**; never guess a locator/disposition; mark
  `[search]`/`unverified` rather than forcing a mapping
  ([`../specs/guardrails.md`](../specs/guardrails.md)).
- **Read, don't write substrate timing** — no edits to `constants.py`/`services.py`
  (D5: attacker-only; this layer sits above even that).
- Branch hygiene, **never push without an explicit ask**, Australian English (in
  prose; keep ATT&CK identifiers verbatim, incl. American "defense-impairment").

## Reading list

- **[`../notes/2026-07-07_thesis_backbone_rubric.md`](../notes/2026-07-07_thesis_backbone_rubric.md)
  — the rubric §3 is written to (read first).**
- **[`../notes/2026-07-07_cross_sectional_review.md`](../notes/2026-07-07_cross_sectional_review.md)
  — the four-lens review: per-tactic disposition, P0–P3 action list, examiner V1–V5.**
- **[`../specs/substrate_primer.md`](../specs/substrate_primer.md) — §(e) the reset
  model every §3 argues from; §(d) inherited-attacker tradeoffs + improvement-over-prior.**
- [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md)
  — the method and the anti-circularity rules.
- [`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../notes/2026-07-04_tactic_duration_precedent_survey.md)
  — the gap evidence + declare-and-sweep precedents + calibration targets.
- [`../tactic_profiles/README.md`](../tactic_profiles/README.md) and
  [`../tactic_profiles/_template.md`](../tactic_profiles/_template.md) — the 15
  keyed tactics, the five groups, the file shape.
- [`../../mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py)
  (`ATTACK_DURATION` ~L140) + [`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
  (`exploit_time`) — the Tier-1 source.
- [`../../data/ogasp/README.md`](../../data/ogasp/README.md) — the place-union the
  catalogue must cover.

## Out of scope (explicitly)

- Executing the timelines (the runner) and the tactic→action binding itself (the
  binding-scoping handoff — only its *draft* tactic→verb table is consulted for
  Tier 1).
- Full sensitivity analysis (deferred, D10) — ranges declared here, swept later.
- Detection/stealth *semantics* — a stealth tactic gets a *time*, not a detection
  model (IDS is culled).
- Mining DARPA OpTC/TC for empirical per-tactic timing — a heavier, unclassified
  sourcing category; flag for a decision, don't assume it's in scope.
- Any substrate change.
