---
status: open
created: 2026-07-03
updated: 2026-07-09
---

# The state-duration catalogue — distil the 15 profiles' §5 into `data/ogasp/tactic_durations.json`

> **Method / the bar:** [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md).
> **Why the gap is real:** [`../notes/2026-07-04_tactic_duration_precedent_survey.md`](../notes/2026-07-04_tactic_duration_precedent_survey.md).
> **The reset model every §3 argues from:** [`../specs/substrate_primer.md`](../specs/substrate_primer.md) §(e).
> Feeds [`./2026-07-03_l3_timeline_runner.md`](./2026-07-03_l3_timeline_runner.md);
> the §3 MTD-interaction verdicts feed [`./2026-07-03_l3_binding_scoping.md`](./2026-07-03_l3_binding_scoping.md).

## State of play

**Steps A–F are DONE (2026-07-04 → 2026-07-07; see git log for the per-step
commits).** All 15 `docs/tactic_profiles/*.md` have §1–§5 filled: tactic/role,
group-assignment argument, MTD-interaction reset verdict, timing evidence, and
catalogue inputs. Files stay `status: stub` — the flip **stub → reconciled** ships
*with the catalogue* (validation gate below), not before. The durable outputs of
that work live in the notes/specs, not in this handoff: the method
([operational-validation note](../notes/2026-07-04_operational_validation_the_bar.md)),
the gap ([precedent survey](../notes/2026-07-04_tactic_duration_precedent_survey.md)),
the substrate reset model ([substrate primer](../specs/substrate_primer.md) §(e)),
and the rubric + four-lens review
([thesis backbone rubric](../notes/2026-07-07_thesis_backbone_rubric.md),
[cross-sectional review](../notes/2026-07-07_cross_sectional_review.md)).

**Since 2026-07-09 the profiles also have a thesis consumer:**
`docs/thesis/dissertation.tex` §3.1 (commits `d229a0e`, `eebffed`) distils the
profiles' §1–§5 into dissertation prose, with **Table 3.1 (timing groups) and
Table 3.2 (per-tactic multiplier + reset classification)** mirroring the §5
scheme. The catalogue must agree with those tables (same groups, multipliers,
tiers); if building it surfaces a value the thesis table got wrong, fix **both**
in the same commit — the profiles' §5 stay the single source of truth. Naming
map (thesis → profiles): scan-anchored = scan-shaped; exploit-anchored =
exploit-shaped; stealth-anchored = stealth-low-and-slow; objective-execution =
same; off-network = prep-off-network.

**The §5 scheme the catalogue distils** — 4 group anchors, not 15 free dwells
(identifiability): **scan-shaped** (recon, discovery) + **exploit-shaped**
(initial-access, privesc, credential-access, lateral-movement) are Tier-1
substrate-fixed ×1.0 **not tuned** (`ATTACK_DURATION` scan verbs / complexity-scaled
`exploit_time`); **stealth-low-and-slow** (stealth = reference, persistence, C2, +
execution/DI) is Tier-3 tuned (k× exploit median); **objective-execution**
(collection, exfiltration, impact) is Tier-2 literature-calibratable;
**prep-off-network** (resource-development) is ×0. Within-group ×1.0 except the two
genuinely-unsettled tactics (`execution`, `defense-impairment` at ×0.5, widest
sweeps) and resource-dev ×0. **The §5 sweep is on the *duration*; the §3 reset
verdict (survivor/vulnerable/partial/null + its own band) is a *separate* declared
parameter for the L3b binding — do not fold it into `duration_s`/`sweep_range`.**

**Durable constraints (still load-bearing for the catalogue):**
- The state set is **15 tactics — ATT&CK Enterprise v19.1** (the v19.1 split of
  `defense-evasion` → `stealth` TA0005 + `defense-impairment` TA0112). The catalogue
  key set must match the `data/ogasp/` place-union (mechanical test).
- **Timing never comes from the corpus** — structure/chaining is CTI's contribution;
  timing is substrate/literature/declared. Breach-report *statistics* (Tier-2) are
  allowed; `observation_count` must **never** leak in as a rate
  ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f)).
- **No GSPN/SPN/TPN semantics** — plain per-state dwell only (D10 deferral).
- **Read, don't write substrate timing** — no edits to `constants.py`/`services.py`.
- Group anchors default **uncalibrated** in v0; calibrate within ranges once the
  runner lands; freeze v1.

**Loose ends (sourcing QA — action during the stub→reconciled flip):**
- `S0951832018304125` is a reliability-redundancy/PSO paper, **not** Lalropuia's
  stochastic game — re-fetch the intended source before citing.
- `S0045790626000315` is Davies ransomware benchmarking, **not** a timed model —
  already routed to `ransomware_timing`, but the manifest label is wrong.
- `09_credential-access.md` **§3 line ~89 inverts the rotation figures** —
  it reads "rotation revokes … in only a minority of cases (41%/17%)". Per
  [`../extractions/password_rotation_efficacy.md`](../extractions/password_rotation_efficacy.md)
  (and the profile's own §4 row), 41% offline / 17% online are the fractions
  where the **new credential is derivable from the captured one, i.e. rotation
  *fails***. The thesis prose (dissertation.tex §3.1, credential access) states
  it correctly — fix the profile §3 sentence to match when flipping status.
- The **e⁻¹ ≈ 0.63 expression is flagged VERIFY** in
  [`../extractions/mtd_scan_disruption.md`](../extractions/mtd_scan_disruption.md)
  (value 0.63 + the quoted "37% reduction" are self-consistent; the expression
  is likely 1 − e⁻¹). Catalogue `justification` strings citing that bound must
  cite the **value only**, never the e⁻¹ expression; the same expression is
  propagated in `01_reconnaissance.md` §3/§4/§5 — correct it there once
  confirmed against Carroll §IV-A.

## The remaining step — the catalogue (execution plan, start cold here)

1. **Read** (in order): this handoff; the reading list below; the fifteen
   profiles' **§5 blocks only** (the catalogue inputs); dissertation.tex §3.1
   Tables 3.1–3.2 (the consistency target).
2. **Extract the Tier-1 anchors** from the substrate — `ATTACK_DURATION`
   (`mtdnetwork/data/constants.py` ~L140) and the `exploit_time` formula
   (`mtdnetwork/component/services.py`) — read-only; record the constant names
   and values for the `source` fields.
3. **Write `data/ogasp/tactic_durations.json`**: one entry per place-union
   tactic — `{group, relative_multiplier, duration_s, tier, source
   (constant-name | profile-file §ref | extraction §ref), justification,
   sweep_range}`. `justification`/`source` point back at the profile §5 (the
   single source of truth). Units: seconds, matching `env.timeout`. Group
   anchors stay **uncalibrated v0** (declared values; calibration waits for the
   runner).
4. **Add the key-set test**: catalogue keys == the `data/ogasp/` place-union
   (from the structural JSONs; see `data/ogasp/README.md`). Assert/grep that no
   value derives from `observation_count` or any corpus frequency.
5. **Fill the provenance row** — [`../specs/provenance.md`](../specs/provenance.md)
   L47 (`L3 per-tactic state-duration regime`, `pending`) gets the
   `data/ogasp/tactic_durations.json` pointer; add the per-tactic row block for
   Marc's approval.
6. **Flip the 15 profiles `stub` → `reconciled`**, actioning the loose-end
   corrections above (09 rotation inversion; e⁻¹ expression) and reconciling
   any remaining `[search]` claims in the process.
7. **Delete this handoff in the same commit** that ships the catalogue
   (session-workflow lifecycle). Cross-check the validation gate below first.

*Alternatives considered:* 15 independent point durations (rejected —
unidentifiable against ~3 macro observables; group anchors instead);
`observation_count`-derived timing (rejected — not a rate); absolute-time realism
(rejected — breaks substrate comparability; shape-not-scale instead).

## Strategic note (2026-07-07 examiner review — read before over-investing in the catalogue)

The §5/catalogue *defend* the thesis's finding but do not *produce* it. The two
objections that can actually fail a viva — **(V1)** the novel object rests on
declared dwell × declared reset fraction; **(V2)** "fidelity changes the answer" is
parameter noise unless the ranking-change *survives its own sweep band and is
distinct from the generic attacker's stable ranking* — are discharged only by
**running the discrimination probe + sweep** (downstream:
[`./2026-07-03_l3_timeline_runner.md`](./2026-07-03_l3_timeline_runner.md) +
CTI-note §10 probe), **not** by more prose. The per-modality reset split (the crown
jewel: capability/credential survives a mutation, network-position is invalidated)
is the strongest genuinely-owned, falsifiable claim — foreground it.

## Validation gate

Done when:
1. All 15 `docs/tactic_profiles/*.md` are `status: reconciled` (five sections
   filled, `[search]` claims reconciled, §5 complete; key set matches the
   `data/ogasp/` place-union).
2. `data/ogasp/tactic_durations.json` covers every place-union tactic; a test
   cross-checks the key set against the structural JSONs.
3. Every entry has `group + tier + source + justification + sweep_range`; no value
   derives from `observation_count` or any corpus frequency (assert/grep).
4. Tier-1 tactics trace to a substrate constant and are flagged *not tuned*; tuned
   tactics name their group anchor.
5. Provenance rows in [`../specs/provenance.md`](../specs/provenance.md) approved by
   Marc; units explicit (seconds, matching `env.timeout`), sane vs `ATTACK_DURATION`
   magnitudes.

## Reading list

- [`../tactic_profiles/`](../tactic_profiles/) — the 15 profiles (evidence layer;
  §5 is the catalogue input) + `README.md` (the five groups) + `_template.md`.
- [`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md)
  — the tier hierarchy + anti-circularity rules.
- [`../specs/substrate_primer.md`](../specs/substrate_primer.md) §(e) — the reset model.
- [`../../mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py)
  (`ATTACK_DURATION` ~L140) + [`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
  (`exploit_time`) — the Tier-1 source.
- [`../../data/ogasp/README.md`](../../data/ogasp/README.md) — the place-union the
  catalogue must cover.

## Out of scope

- Executing the timelines (the runner) + the tactic→action binding itself (the
  binding handoff — only its draft tactic→verb table is consulted for Tier 1).
- Full sensitivity analysis (deferred, D10) — ranges declared here, swept later.
- Detection/stealth *semantics* — a stealth tactic gets a *time*, not a detection
  model (IDS is culled).
- Mining DARPA OpTC/TC for empirical per-tactic timing — a heavier, unclassified
  sourcing category; flag for a decision, don't assume it's in scope.
- Any substrate change.
