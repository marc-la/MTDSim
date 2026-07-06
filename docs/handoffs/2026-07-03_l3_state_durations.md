---
status: open
created: 2026-07-03
updated: 2026-07-04
---

# Build the per-tactic dwell profiles → the state-duration catalogue: operational-validation method, group anchors, and a mechanical research protocol

> **Method / the bar:** [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> **Why the gap is real:** [`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../notes/2026-07-04_tactic_duration_precedent_survey.md).
> **Scaffolding to fill:** [`../tactic_profiles/`](../tactic_profiles/) (README + template + 15 stubs).
> Runs parallel with [`./2026-07-03_l3_weighted_nets_aggregate_profile.md`](./2026-07-03_l3_weighted_nets_aggregate_profile.md);
> both feed [`./2026-07-03_l3_timeline_runner.md`](./2026-07-03_l3_timeline_runner.md).
> MTD-interaction sections feed [`./2026-07-03_l3_binding_scoping.md`](./2026-07-03_l3_binding_scoping.md).

## State of play

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

## Steps remaining (as of 2026-07-06)

Evidence-gathering (Steps A–D) is complete: §1/§2/§4 are filled, reconciled, and
**enriched with the full external-search corpus** for all 15 profiles. Three
things remain, in order:

1. **Step E — fill §3 (MTD interaction / reset verdict), all 15 profiles**
   (detail below). *Don't re-mine the MTD papers* — the §3 evidence is now fully
   staged: the alshamrani2019 per-tactic MTD-effect block + reset-verdict matrix
   (Step B), the Step-C reset inputs, **plus the Step-D §3 evidence carried in each
   profile's §4 rows with a `→§3` pointer** (the strongest new material). The
   Step-D reset verdicts, by tactic:
   - **The governing principle (Step D):** the reset is **per-modality and
     rate-dependent, never a clean wipe** — Evans 2011
     ([`../extractions/evans2011_mtd_effectiveness.md`](../extractions/evans2011_mtd_effectiveness.md)):
     dynamic diversity gives *no* advantage vs circumvention/deputy attacks
     (incl. fileless/script **execution**), ≤2× vs brute-force, significant only vs
     incremental probing *and* only at a high re-randomisation rate (6 orders of
     magnitude across every-4th vs every-100th probe). Set every sweep width from
     the shuffle-interval ÷ attacker-action-time ratio.
   - **recon / discovery force re-scan on a shuffle** — reset governed by
     shuffle-interval ÷ attacker-wait, e⁻¹≈0.63 ceiling, RDAM 96.2% miss
     ([`../extractions/mtd_scan_disruption.md`](../extractions/mtd_scan_disruption.md),
     [`../extractions/internet_scanning_empirics.md`](../extractions/internet_scanning_empirics.md));
   - **credential-access is the clearest reset-*survivor*** — stolen credentials
     survive a topology shuffle *and* largely survive password rotation
     (Zhang-Monrose-Reiter: only 41% offline / 17% online broken —
     [`../extractions/password_rotation_efficacy.md`](../extractions/password_rotation_efficacy.md));
   - **persistence reset is *partial*, rate-dependent** — FlipIt (higher-move-cost
     player → benefit 0), SCIT cleansing-cycle, Sun switch-timing
     ([`../extractions/persistence_reset_models.md`](../extractions/persistence_reset_models.md));
   - **C2 reset is *partial*** — beacon survives connection loss (proxies), switch
     interval is the swept axis ([`../extractions/c2_beaconing.md`](../extractions/c2_beaconing.md));
   - **lateral-movement reset is per-modality** — address mutation kills a
     *scan-based* worm (<1% valid addresses) but a *credential*-move survives
     ([`../extractions/worm_propagation_models.md`](../extractions/worm_propagation_models.md));
   - **impact reset = blast-radius limiting** — MTD contains lateral ransomware
     spread mid-attack (Barach, [`../extractions/ransomware_timing.md`](../extractions/ransomware_timing.md));
   - **resource-development is reset-*immune*** (off-network), unchanged.
2. **Step F — fill §5 (catalogue inputs), all 15 profiles** (detail below):
   group (confirm/overturn the stub hypothesis) + relative multiplier + sweep
   range + tier + one-paragraph justification. Carry the Step-C findings that
   move the bets: group anchors beat per-tactic values (ling2023's shared 6-day
   expert floor); C2/stealth-hiding are Tier-3 *declared* (CVE timing can't price
   them); `execution` and `defense-impairment` stay genuinely unsettled → wide
   sweep; objective tactics anchor to the macro milestone chain (breakout ~29 min,
   access→AD ~3–16 h, access→exfil ~73–79 h, TTR 2 h–328 h, dwell 14 d/122 d/~400 d).
3. **The catalogue — `data/ogasp/tactic_durations.json` + provenance rows**
   (detail under "Then the catalogue" below). Distil §5 into the machine
   artefact; every place-union tactic gets an entry; fill the `pending` regime
   row in [`../specs/provenance.md`](../specs/provenance.md).

Only after all three: flip profiles `stub` → `reconciled` and clear the
Validation gate. **This handoff is deleted in the commit that ships the
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

**Step E — Reason from mechanism (fills §3).** No literature grounds MTD→attacker
effect (the genuine unknown,
[`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md) §5).
Argue from MTD semantics: does an IP/topology shuffle **invalidate** a gain in
this tactic (foothold, C2 channel) or does it **survive** (a stolen credential)?
That reset verdict + its uncertainty set the sweep width. Declared, not claimed.

**Step F — Distil §5.** Group (confirm/overturn the stub's hypothesis) + relative
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
