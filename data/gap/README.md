# `data/gap/` — L1 GAP artefacts

The Generalised APT Profile (L1): a lossless, Attack-Flow-only technique
dependency graph. Data model and design decisions:
[`docs/specs/01_gap_schema.md`](../../docs/specs/01_gap_schema.md). Build code:
[`src/mtdsim/l1_construction/`](../../src/mtdsim/l1_construction).

## Contents

| Path | Tracked? | What |
|---|---|---|
| `flows/<flow_id>.yaml` | **committed** | one lossless per-flow extract per Attack Flow (§c) — the seam for hand-authored incidents |
| `gap_v0.5.json` | **committed** | the aggregated GAP (§d) — the canonical artefact |
| `_corpus_stix/*.json` | gitignored | upstream Attack Flow corpus, as STIX bundles (build input) |
| `_attack/enterprise-attack-*.json` | gitignored | ATT&CK Enterprise STIX, for node metadata (build input) |

## Rebuild

```sh
PYTHONPATH=src python -m mtdsim.l0_cti           # acquire the gitignored inputs
PYTHONPATH=src python -m mtdsim.l1_construction  # write flows/ + gap_v0.5.json
PYTHONPATH=src python -m pytest tests/gap/       # validation gate
```

The build is deterministic: a rebuild is byte-identical save the `build_date`.

## Provenance

- **Attack Flow corpus** — MITRE Center for Threat-Informed Defense (CTID),
  *Attack Flow*, release **v3.1.1** (package version 3.2.0; STIX 2.1 extension
  schema 2.0.0). The corpus ships `.afb` Builder files; the STIX bundles used
  here are CTID's own lossless export, retrieved from the project's published
  site (`center-for-threat-informed-defense.github.io/attack-flow/corpus/`).
- **MITRE ATT&CK** — Enterprise ATT&CK STIX, version **19.1**
  (`mitre-attack/attack-stix-data`), used only for technique node metadata
  (names, tactics, platforms) and the tactic-layer ordering.

### Enterprise-only scope (non-Enterprise techniques dropped)

The corpus is heterogeneous: a few flows reference ATLAS (adversarial-ML,
`AML.*`) or ICS (`T0###`) techniques, and some use Enterprise ids that ATT&CK
v19.1 has **revoked** (e.g. `T1562`) or removed. The GAP is scoped to Enterprise
(§a / [`01_gap_schema.md`](../../docs/specs/01_gap_schema.md) Decision 5): such
nodes are **dropped from the aggregated GAP**, together with their edges —
*removed, never bridged*, so no dependency is synthesised across a dropped node
(the §a no-synthesis invariant). The per-flow extracts under `flows/` stay
**lossless** and keep these techniques as the analyst drew them; the scope is
applied only at aggregation. At v0.5 this dropped 22 of 146 candidate nodes
(15 ATLAS, 2 ICS, 5 revoked/absent), leaving 124 fully-labelled Enterprise
nodes. This is a deliberate scope, not a build error.

## Licensing / attribution

The Attack Flow corpus is licensed **Apache-2.0** by MITRE Engenuity CTID
(document numbers CT0040, CT0122, 25-2036). The committed per-flow extracts
reproduce structural elements of the corpus flows (ATT&CK technique IDs, the
action/operator/condition topology, condition descriptions, and source
references); this reuse is within the Apache-2.0 grant, and this notice
preserves the required attribution. MITRE ATT&CK® is used per the ATT&CK Terms
of Use; ATT&CK is a registered trademark of The MITRE Corporation.
