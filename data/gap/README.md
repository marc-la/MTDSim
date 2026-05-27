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

### Nodes without Enterprise metadata

The corpus is heterogeneous: a few flows reference ATLAS (adversarial-ML,
`AML.T####`) or ICS (`T0###`) techniques, and some use Enterprise ids that
ATT&CK v19.1 has since **revoked** (e.g. `T1562`). These appear as GAP nodes
(they are real, analyst-drawn observations) but carry empty name/tactics, since
Enterprise v19.1 does not define them. They are kept **as drawn** — never
remapped or dropped — to uphold the §a no-synthesis invariant; a future
"Enterprise-only" view could filter them. This is a property of the corpus ×
pinned-ATT&CK pairing, not a build error.

## Licensing / attribution

The Attack Flow corpus is licensed **Apache-2.0** by MITRE Engenuity CTID
(document numbers CT0040, CT0122, 25-2036). The committed per-flow extracts
reproduce structural elements of the corpus flows (ATT&CK technique IDs, the
action/operator/condition topology, condition descriptions, and source
references); this reuse is within the Apache-2.0 grant, and this notice
preserves the required attribution. MITRE ATT&CK® is used per the ATT&CK Terms
of Use; ATT&CK is a registered trademark of The MITRE Corporation.
