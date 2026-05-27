# `l0_cti` — L0 raw-CTI acquisition

| level | artefact | architecture § | status | code home |
|---|---|---|---|---|
| L0 | raw CTI (Attack Flow corpus + ATT&CK Enterprise) | [§(c)](../../../docs/specs/architecture.md) | **built** | here |

Acquires the **gitignored** upstream inputs the L1 build consumes: the 40 MITRE
CTID Attack Flow corpus flows (as STIX bundles) and the ATT&CK Enterprise STIX
bundle. Pins live in [`fetch.py`](fetch.py); per
[`01_gap_schema.md`](../../../docs/specs/01_gap_schema.md) Decision 4, only the
distilled extracts + aggregate (under [`data/gap/`](../../../data/gap/)) are
committed — never these inputs.

```sh
PYTHONPATH=src python -m mtdsim.l0_cti [--force]   # -> data/gap/_corpus_stix/, _attack/
```

- [`fetch.py`](fetch.py) — library: `fetch_corpus()` + the pinned provenance constants.
- [`__main__.py`](__main__.py) — the CLI runner.
