---
status: open
created: 2026-07-03
---

# Build the per-tactic state-duration catalogue — tiered sourcing (substrate / literature / justified estimate), every value with provenance and a sweep range

> **Depends on** [`./2026-07-03_l3_governance_meeting_decisions.md`](./2026-07-03_l3_governance_meeting_decisions.md)
> (the duration *regime* row in [`../specs/provenance.md`](../specs/provenance.md)
> must exist; this handoff fills in the catalogue under it). Runs in parallel
> with [`./2026-07-03_l3_weighted_nets_aggregate_profile.md`](./2026-07-03_l3_weighted_nets_aggregate_profile.md);
> both feed [`./2026-07-03_l3_timeline_runner.md`](./2026-07-03_l3_timeline_runner.md).

## State of play

- **Supervisor decisions this executes:** D4 — the simulator is discrete-event,
  so **every attacker state needs a time attached**; reuse timing values from
  relevant work where they exist; where none exist (e.g. stealth), assign a
  reasonable, **justified** number. Hong explicitly warned: no ready-made
  resource maps MITRE tactics to durations — *define this yourself, with
  justifications*. D10 — timed Petri nets (GSPN/SPN/TPN firing semantics) are
  **deferred**: a duration here is a plain per-state dwell consumed by the
  standalone runner, not a stochastic firing rate.
- The state set is the tactic places of the L3a nets — the ≤15 ATT&CK
  Enterprise tactics appearing across the five nets (four classes +, once
  built, the aggregate): reconnaissance, resource-development, initial-access,
  execution, persistence, privilege-escalation, defence-evasion,
  credential-access, discovery, lateral-movement, collection,
  command-and-control, exfiltration, impact (confirm the exact union against
  [`../../data/ogasp/`](../../data/ogasp/) — per-class place counts are 13–15).
- The substrate already prices its own verbs:
  `ATTACK_DURATION` at [`../../mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py)
  (line ~140) for SCAN_HOST / ENUM_HOST / SCAN_PORT / SCAN_NEIGHBOR /
  EXPLOIT_VULN / BRUTE_FORCE, plus complexity-scaled `exploit_time` on
  vulnerabilities ([`services.py`](../../mtdnetwork/component/services.py)).
  Where a tactic maps onto those verbs, substrate-sourced timing keeps the
  within-substrate MTTC comparison clean.
- Nothing duration-shaped exists yet for tactics. `observation_count` must not
  leak in as a timing signal
  ([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f)).

## Recommended approach

**1 — Fix the tier hierarchy (record it in the catalogue header).**

- **Tier 1 — substrate-sourced.** Tactic maps to substrate action-class(es) →
  duration derived from `ATTACK_DURATION` / `exploit_time` semantics. Best for
  the scan/exploit-shaped tactics (discovery, initial-access,
  privilege-escalation, lateral-movement, credential-access). Preserves
  within-substrate comparability; the natural default wherever the (parallel)
  binding-scoping handoff maps a tactic onto a substrate verb.
- **Tier 2 — literature-sourced.** Scan [`../extractions/`](../extractions/)
  (Mendonça 2023 is the closest analytical-MTD precedent; Bland 2020 the
  executed-SPN precedent; the UWA-lineage four for any phase timings already
  in the substrate's papers) plus targeted adjacent work for defensible
  per-tactic dwell values (e.g. dwell-time / breach-report statistics for
  persistence, C2, exfiltration). **Papers are claims** — record
  paper → value → how it was adapted; reconcile before citing
  ([`../specs/guardrails.md`](../specs/guardrails.md)); mark `unverified` where
  the mapping is a stretch rather than forcing it.
- **Tier 3 — justified estimate.** For tactics with no substrate verb and no
  usable literature value (stealth-shaped: defence-evasion, persistence,
  execution, C2, exfiltration if Tier 2 comes up dry): a stated number with a
  one-paragraph justification (e.g. "long relative to scan verbs because the
  behaviour is low-and-slow by definition; anchored at k× the Tier-1 median").
  This is exactly what Hong authorised — the justification is the deliverable,
  not the number.

**2 — The artefact.** Commit `data/ogasp/tactic_durations.json`: per tactic —
`{duration_s, tier, source (constant-name | extraction-file §ref | rationale),
justification, sweep_range}`. Every tactic in the L3a place-union gets an
entry; no entry without a tier and a justification. Add a matching row block to
[`../specs/provenance.md`](../specs/provenance.md) (value → source → code →
disposition), and a short note if the literature scan surfaces anything
dissertation-worthy (the tactic→time mapping is itself a methodological
contribution Hong flagged — "define this yourself").

**3 — Sweep ranges, not point trust.** Full sensitivity analysis is deferred
(D10), but each value carries a declared range now (default ×½ / ×2 unless the
source justifies tighter) so the timeline runner can expose duration
sensitivity cheaply and nothing hardens into a hidden constant.

*Alternatives considered:* corpus-derived timings (rejected — Attack Flow
carries no timing, and `observation_count` is not a rate); a single uniform
dwell for all tactics (kept only as the runner's degenerate sensitivity case,
not as the catalogue); deferring durations until the binding lands (rejected —
D2's timeline output needs them, and Tier 1 only needs the *draft* tactic→verb
mapping, which the binding-scoping handoff produces early).

## Validation gate

Done when:
1. `data/ogasp/tactic_durations.json` covers **every** tactic-place in the
   L3a union; a mechanical test cross-checks the key set against the
   structural JSONs.
2. Every entry has `tier + source + justification + sweep_range`; no value is
   derived from `observation_count` or any corpus frequency (assert/grep).
3. Tier-2 entries each cite an extraction file section; anything
   unreconcilable is marked `unverified`, not guessed.
4. The provenance rows are in [`../specs/provenance.md`](../specs/provenance.md)
   and approved by Marc.
5. Units are explicit (seconds, matching the substrate's `env.timeout` domain)
   and sane against `ATTACK_DURATION` magnitudes.

## Hard constraints

- **Timing never comes from the corpus** — structure and chaining are CTI's
  contribution; timing is substrate/literature/declared
  ([`../notes/2026-06-18_cti_to_executable_behaviour.md`](../notes/2026-06-18_cti_to_executable_behaviour.md) §5).
- **No GSPN/SPN/TPN semantics** — plain per-state dwell only (D10 deferral).
- **Papers are claims to reconcile, not ground truth**; never guess a locator
  or disposition ([`../specs/guardrails.md`](../specs/guardrails.md)).
- Do not modify `constants.py` or any substrate timing — read, don't write
  (D5: attacker-only, and this layer sits above even that).
- Branch hygiene, **never push without an explicit ask**, Australian English.

## Reading list

- [`./2026-07-03_l3_governance_meeting_decisions.md`](./2026-07-03_l3_governance_meeting_decisions.md)
  — D4/D10 and the provenance regime row this fills.
- [`../../mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py)
  — `ATTACK_DURATION` (~L140) + neighbours: the Tier-1 source.
- [`../../mtdnetwork/component/services.py`](../../mtdnetwork/component/services.py)
  — `exploit_time` / complexity scaling (Tier-1 for exploit-shaped tactics).
- [`../extractions/mendonca2023.md`](../extractions/mendonca2023.md) and
  [`../extractions/bland2020.md`](../extractions/bland2020.md) — first stops
  for Tier 2.
- [`../../data/ogasp/README.md`](../../data/ogasp/README.md) — the place-union
  the catalogue must cover.

## Out of scope (explicitly)

- Executing the timelines (the runner) and the tactic→action binding itself
  (the binding-scoping handoff — only its *draft* tactic→verb table is
  consulted for Tier 1).
- Full sensitivity analysis (deferred, D10) — ranges are declared here, swept
  later.
- Detection/stealth *semantics* — a stealth tactic gets a *time*, not a
  detection model (IDS is culled project-wide).
- Any substrate change.
