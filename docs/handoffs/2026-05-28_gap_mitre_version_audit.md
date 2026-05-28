---
status: open
created: 2026-05-28
---

# Audit GAP v0.5's tactic + technique vocabulary against modern MITRE ATT&CK Enterprise — reconcile legacy labels (`defense-impairment`, `stealth`), pin the MITRE version the GAP is calibrated against

The GASP visualisation iteration
([`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md)
§"Visualisation iteration outcomes") surfaced an anomaly: the per-class
tactic FSM for `pure_steal` renders **15 states** even though modern
MITRE ATT&CK Enterprise has only **14 tactics**. A quick enumeration of
`primary_tactic` values across `data/gap/gap_v0.5.json` confirms the
GAP carries **two non-modern-MITRE tactic labels**:

- `stealth` — 11 techniques (T1014, T1027, T1036, T1070, T1140, +6 more — all
  classic Defense Evasion techniques in current Enterprise)
- `defense-impairment` — 2 techniques (T1222 File and Directory Permissions
  Modification; T1553 Subvert Trust Controls — also both Defense Evasion in
  current Enterprise)

Modern Enterprise has `Defense Evasion` (TA0005) instead. The GAP's source —
CTID Attack Flow Builder example flows — uses these alternative labels
verbatim (see e.g. `data/gap/flows/whispergate.yaml`, `mac_malware_steals_crypto.yaml`).
The labels are presumably either (a) a CTID-Attack-Flow-Builder schema
convention, (b) inherited from an older MITRE version, or (c) something the
flow authors chose. **The GAP doesn't pin a MITRE ATT&CK version anywhere**,
so we can't tell which from internal evidence — that's the bigger gap this
handoff closes.

## State of play

**Settled (don't re-derive):**

- GAP v0.5 is built from the CTID Attack Flow Builder example flows
  ([`../specs/01_gap_schema.md`](../specs/01_gap_schema.md);
  [`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)).
  Tactic labels in `gap_v0.5.json` come directly from `data/gap/flows/*.yaml`,
  which in turn come from the CTID source.
- 15 distinct `primary_tactic` values in `gap_v0.5.json`. 13 match modern
  MITRE Enterprise (with the hyphen vs space convention,
  e.g. `lateral-movement` ↔ `Lateral Movement`). 2 don't: `stealth` and
  `defense-impairment`.
- The 2 `defense-impairment` techniques (T1222, T1553) are valid current
  technique IDs in MITRE Enterprise — they just sit under `Defense Evasion`
  in current taxonomy, not under a tactic called "defense-impairment".
- The 11 `stealth` techniques are similarly all current `Defense Evasion`
  techniques in modern MITRE.
- The GAP's `version` field is `0.5` (a GAP-internal version, not a MITRE
  version). No `mitre_attack_version` or `attack_spec_version` field exists
  in `gap_v0.5.json`.
- The L2 / GASP classification scheme (P6 compound-class disjoint) holds
  regardless of how this audit resolves — class membership is sourced from
  analyst-stated objectives, not from tactic mechanics. The audit affects
  *labelling*, not *partitioning*.

**Unsettled (this handoff resolves):**

- Is `stealth` a CTID Attack Flow Builder schema convention, an older MITRE
  tactic name, or a flow-author idiosyncrasy?
- Is `defense-impairment` similarly source-derived, or is it a MITRE-deprecated
  tactic that was once distinct from `Defense Evasion`? (Plausible: very early
  ATT&CK had finer-grained tactics that were later merged.)
- What MITRE ATT&CK Enterprise *version* are the CTID source flows aligned
  with? The CTID `attack-flow-builder` repo may declare this; the GAP needs to
  inherit + record it.
- How should the GAP / GASP reconcile? Three options on the table —
  (a) remap legacy labels to `defense-evasion` in-place (and record the map),
  (b) re-build the GAP at v0.6 from updated source data, (c) freeze the GAP
  at its current MITRE version with a documented `mitre_attack_version: X.Y`
  and a legacy-label glossary.
- Are there *technique-ID* drifts as well? (e.g. deprecated technique IDs,
  renumbered sub-techniques, techniques absent from current Enterprise.)
  This handoff audits both axes.

## Recommended approach

Treat this as a **two-axis audit + a labelling decision**, not a rebuild.
Sequence the work to defer the most expensive option (rebuild) until the
audit motivates it.

### Tasks

1. **Tactic-label audit.** Already partially done; finish it:
   - Confirm the full 15-vs-14 set by enumerating distinct `primary_tactic`
     across `gap_v0.5.json`.
   - Cross-reference against the current MITRE Enterprise tactics list
     (14 of them; TA0001–TA0011 + TA0040 + TA0042 + TA0043). Use
     <https://attack.mitre.org/tactics/enterprise/> as the live source of
     truth, or the `mitreattack-python` library which pulls the STIX bundle.
   - For each non-matching label, walk its techniques back through the
     source YAMLs to identify which flows introduced it.

2. **CTID Attack Flow Builder schema check.** The labels almost certainly
   come from upstream CTID conventions. Check:
   - <https://github.com/center-for-threat-informed-defense/attack-flow>
     — does the schema declare a tactic vocabulary? Does it use
     `defense-impairment` / `stealth` explicitly?
   - The CTID corpus's own README / SPEC for the example flows — does it
     pin a MITRE version?
   - Look at the original STIX 2.1 source of the example flows (the YAMLs
     in `data/gap/flows/` are *distilled* from CTID's `.afb` / `.json`
     bundles — those bundles should have `external_references` to MITRE
     with version numbers).

3. **MITRE changelog research for `defense-impairment`.** The user's
   hypothesis is that defense-impairment is a removed/renamed MITRE tactic.
   Check:
   - The MITRE ATT&CK `attack-stix-data` GitHub repo's release history.
     Tactics may have been renamed/merged over time — the changelog
     between versions should record this.
   - If `defense-impairment` was ever a real MITRE tactic, document the
     version it existed in, the version that removed it, and the reasoning
     in MITRE's release notes.
   - If it was NEVER a real MITRE tactic, document that it's a CTID-specific
     or flow-author label.

4. **Technique-ID drift audit.** Beyond tactics, audit:
   - Total technique IDs in `gap_v0.5.json` — how many resolve to current
     Enterprise STIX? How many are deprecated / revoked?
   - Sub-technique IDs (T-IDs of form `Txxxx.yyy`) — same question.
   - Use `mitreattack-python` (or the STIX bundle directly) to do the
     resolution.

5. **Pin the MITRE version.** Whichever version the CTID corpus is aligned
   with, record it in:
   - [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) §"Pinned
     references" (add this section if absent) — the canonical declaration.
   - `gap_v0.5.json` — add a `mitre_attack_version` field at the top level,
     and a `source_attack_flow_version` for the CTID corpus.
   - [`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)
     — cross-reference for the historical record.

6. **Reconciliation decision.** Three plausible outcomes, choose one with
   justification:
   - **(a) In-place remap.** Rewrite `gap_v0.5.json` to translate `stealth`
     and `defense-impairment` to `defense-evasion`. Pros: cleans up the
     vocabulary, makes the GAP modern-MITRE-compatible. Cons: mutates a
     load-bearing artefact, breaks reproducibility from the source YAMLs.
     If chosen, save the original as `gap_v0.5_pre_remap.json` and document
     the mapping table.
   - **(b) Bump to v0.6 with rebuild.** Re-run the GAP build pipeline
     against the current CTID corpus (which may itself have moved on) and
     produce `gap_v0.6.json` with modern labels. Pros: fully current. Cons:
     large scope; introduces new variables (more flows, different node
     counts, JSD shifts in the L2 partition decision).
   - **(c) Freeze at vintage version + legacy glossary.** Pin the MITRE
     version the GAP is calibrated against, add a legacy-tactic glossary
     mapping `stealth` / `defense-impairment` → modern `Defense Evasion`,
     leave `gap_v0.5.json` unmodified. Pros: zero risk of mutation; clean
     paper trail. Cons: tooling that compares against current MITRE needs
     to apply the map at read-time.

   Marc's prior:
   - Lossless preservation of the source has been the load-bearing
     principle ([`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)
     Decision X). Option (a) violates this. Option (c) preserves it.
   - Option (b) is a scope expansion; not the right move for this handoff.
   - **Recommend (c)** — pin version, add glossary, document the L2 / GASP
     downstream sees the legacy labels as-is. If a future workstream (e.g.
     dissertation chapter 3) wants modern labels, it can apply the map at
     read-time without touching `gap_v0.5.json`.

### Alternatives considered

- *Just rename `stealth` → `defense-evasion` silently.* Rejected — need to
  verify the mapping is semantically correct (not just visually similar)
  and trace the MITRE version this aligns the GAP to.
- *Defer the version pinning indefinitely.* Rejected — the longer this
  goes unresolved, the more drift accumulates. The viz iteration already
  surfaced the symptom; the next dissertation reviewer will too.
- *Treat as out-of-scope; the L2 partition holds.* Partially true (the
  partition is robust to relabelling), but the *defence* of the partition
  in the dissertation will be undermined if reviewers spot the legacy
  labels without an explanation.

## Validation gate

Done when:

1. A short note at `../notes/<date>_gap_mitre_audit.md` (or a section in
   [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)) records:
   - The 15 → 14+2-legacy breakdown with technique counts per label
   - The provenance of each legacy label (CTID schema? early MITRE? flow
     author?) with citations to upstream sources
   - A complete remap from legacy → modern labels
2. The pinned MITRE ATT&CK Enterprise version is recorded in
   [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) and either
   `gap_v0.5.json` itself (preferred) or as a sibling
   `gap_v0.5_provenance.json`.
3. The technique-ID drift audit produces a list: resolved vs deprecated vs
   not-found, with a percentage.
4. A reconciliation decision is taken (a, b, or c above) with reasoning
   recorded.
5. The pinned MITRE version is *cited* from a primary source (MITRE
   release notes or the CTID corpus's own version declaration), not
   inferred.
6. Handoff is deleted in the commit that ships the audit + version pin.

## Hard constraints

- **No destructive changes to `gap_v0.5.json`** without saving the original
  (preservation principle from
  [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)). If you go with
  option (a) or (b), the original is provenance.
- **Cite MITRE primary sources** (release notes, STIX bundle, official
  changelog) for any claim about tactic history. Don't infer reasoning
  from absence; if MITRE's reasoning for a removal isn't documented, say
  so explicitly.
- **No rebuild of the GAP** as part of this handoff. Option (b) is a
  follow-up handoff if the audit finds the GAP is materially out of date.
- **The L2 / GASP partition decision is settled.** Do not propose
  re-running discrimination JSDs or revising the classification because
  the labels change — `defense-impairment` → `defense-evasion` doesn't
  change membership.
- **Branch hygiene per
  [`../specs/session_workflow.md`](../specs/session_workflow.md)** —
  dedicated branch (`audit/gap-mitre-version` or similar), no push.
- **Australian English** in docs (per
  [`../specs/guardrails.md`](../specs/guardrails.md)) — but technique /
  tactic names mirror MITRE's American English (`defense`, `behavior`)
  because they're proper nouns from the upstream taxonomy.

## Reading list

In order:

1. **[`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)** — the GAP
   schema, where the version pin will land. Especially Decision 4
   (per-flow YAMLs as source-fidelity records — touched by option (a)
   debate).
2. **[`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)** —
   how the GAP was assembled from CTID flows; where tactic labels enter.
3. **[`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md)
   §"Visualisation iteration outcomes"** — where the 15-vs-14 anomaly was
   first surfaced; explains why this handoff exists.
4. **A sample CTID flow YAML** — e.g.
   `data/gap/flows/whispergate.yaml`, which contains `tactic: stealth`.
5. **The CTID Attack Flow Builder upstream repo**
   (<https://github.com/center-for-threat-informed-defense/attack-flow>) —
   for schema + version declarations.
6. **MITRE ATT&CK Enterprise tactics list**
   (<https://attack.mitre.org/tactics/enterprise/>) — the 14-tactic
   ground truth. Cross-reference with the `mitreattack-python` library
   or the `attack-stix-data` GitHub repo for historical versions.

## Out of scope (explicitly)

- **Rebuilding the GAP** (option (b) above). If the audit motivates a
  rebuild, open a follow-up handoff.
- **Revising the L2 / GASP classification.** The P6 partition decision is
  settled; labelling changes don't move membership.
- **Touching per-flow YAMLs.** They're source-fidelity records; the
  legacy labels in them are *evidence* of the CTID source's
  vocabulary, not bugs.
- **Updating the L2 / GASP visualisations.** They'll re-render correctly
  once the GAP is updated (if it is); not a separate concern.
- **MITRE ATLAS or MITRE Mobile / ICS.** GAP is Enterprise-only per
  [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) §"Decision 5";
  audit applies only to Enterprise.

## Quick reproducer for the 15-state anomaly

```python
import json
from collections import Counter
gap = json.loads(open('data/gap/gap_v0.5.json').read())
tac = Counter(n.get('primary_tactic') or '(none)'
              for n in gap['nodes'].values())
for t, n in sorted(tac.items(), key=lambda kv: -kv[1]):
    print(f'{t!r:<35s} {n:>3d}')
# Expected output: 15 lines, with `stealth` (11) and
# `defense-impairment` (2) standing out as non-modern-MITRE labels.
```
