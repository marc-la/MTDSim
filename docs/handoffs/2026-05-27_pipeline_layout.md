---
status: open
created: 2026-05-27
---

# Reorganise the contribution code into an architecture-aligned (`lN_`) pipeline

Consolidate the profile-construction code into one legible, pipeline-stage tree
under `src/mtdsim/`, named to the architecture's own **L0–L4** levels, with stubs
(+ pointers) for the stages that live in the substrate. Today the L1 GAP code
sits under `src/mtdsim/attacker/gap/` — a *role*-based path that mis-files a
build-time artefact under "attacker" — with its fetch/build split into
`scripts/`. That scatters L1 and conflates the **contribution pipeline**
(stage-organised) with the **substrate** (role-organised).

## State of play

- L1 GAP code: `src/mtdsim/attacker/gap/{schema,attack_flow_parser,attack_stix,aggregate,views,build}.py` + `__init__.py`. Self-contained; imports nothing from the substrate. Importable via root `conftest.py` (adds `src/`) + `PYTHONPATH=src`.
- L0 acquisition + L1 CLI: `scripts/fetch_gap_corpus.py`, `scripts/build_gap.py`.
- Artefacts: `data/gap/` — committed `flows/`, `gap_v0.5.json`, `README.md`; gitignored `_corpus_stix/`, `_attack/`.
- Gate: `tests/gap/test_gap.py` (13 tests, green; deterministic build).
- Substrate: `mtdnetwork/` (inherited MTDSimTime — `component/ mtd/ mtdai/ operation/ statistic/ snapshot/`). This is L3/L4 territory; has goldens + SIM-05 determinism; **left alone**.
- A parallel *role*-based `src/mtdsim/` restructure (`network/ defender/ attacker/ ai/ sim/ stats/`) **and** the superseded v0.4 GAP live on the sibling `feat/attacker-profiling` — not merged.

**Naming decision (this session, with Marc):** directories are `lN_` + a generic
function label — import-safe (a leading letter), self-ordering, mapping to the
architecture's L0–L4, acronym-free. Acronyms (GAP/GASP/OGASP) stay in the docs as
*artefact* names. Rejected: leading-digit dirs (`00_cti` — not importable) and
vague labels ("filter" blurs L2-GASP vs the GAP's support-filter *view*).

## Recommended approach

Target tree (the **scheme** is fixed; exact suffixes are adjustable):

```
src/mtdsim/
  README.md            # the cross-walk table below — the one canonical map
  l0_cti/              # L0  acquire raw CTI (Attack Flow corpus + ATT&CK)
    fetch.py           #     <- scripts/fetch_gap_corpus.py (library half)
  l1_construction/     # L1  build the GAP        [artefact: GAP]
    schema.py  attack_flow_parser.py  attack_stix.py  aggregate.py  views.py  build.py
    __main__.py        #     <- scripts/build_gap.py  (python -m mtdsim.l1_construction)
  l2_subgraph/         # L2  motivation subgraph  [artefact: GASP]   — STUB
  l3_simulation/       # L3  graph-driven attacker in MTDSim [OGASP] — STUB -> seam in mtdnetwork/
  l4_evaluation/       # L4  evaluation                              — STUB -> mtdnetwork/ metrics
```

Cross-walk for `src/mtdsim/README.md` (closes the docs-audit §3 "GAP/GASP/OGASP
code locations" gap — [`../notes/2026-05-27_docs_audit.md`](../notes/2026-05-27_docs_audit.md)):

| dir | level | artefact | architecture § | status | code home |
|---|---|---|---|---|---|
| `l0_cti` | L0 | raw CTI | §(c) | built | here |
| `l1_construction` | L1 | GAP | §(d) | built | here |
| `l2_subgraph` | L2 | GASP | §(e) | stub | here (prior art: v0.4 selectors on `feat/attacker-profiling`) |
| `l3_simulation` | L3 | OGASP | §(f), §(i) | stub | **seam in `mtdnetwork/`** (not greenfield) |
| `l4_evaluation` | L4 | — | §(g) | stub | **`mtdnetwork/` metrics** |

Steps (each behind a green gate):
1. `git mv src/mtdsim/attacker/gap/* src/mtdsim/l1_construction/`; remove the now-empty `attacker/` (GAP was its only content). Split the fetch *library* logic into `l0_cti/fetch.py`.
2. Rewrite imports `mtdsim.attacker.gap.X` → `mtdsim.l1_construction.X`. In `build.py`, `_REPO_ROOT` drops one level (`parents[4]` → `parents[3]`).
3. Make the CLIs module entrypoints (`l1_construction/__main__.py`, an `l0_cti/__main__.py` or a thin `scripts/` shim) — `__main__.py` is not imported by `__init__`, so it sidesteps the `-m` double-import warning that prompted moving the CLI to `scripts/` originally.
4. Add `__init__.py` + a short `README.md` to each stage (its cross-walk row). For `l2`: the architecture §, what it will hold, the v0.4-selector prior-art pointer. For `l3`/`l4`: state plainly they are **substrate seams** — name the `mtdnetwork/` module they attach to, hold no code.
5. Update docs naming the old path: [`01_gap_schema.md`](../specs/01_gap_schema.md) §(f)/§(i), [`architecture.md`](../specs/architecture.md) §(d)–(g) code-location lines, [`data/gap/README.md`](../../data/gap/README.md), and [`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md).
6. Re-run the gate + rebuild; confirm byte-identical artefacts.

**Alternatives considered.**
- *Pipeline as a separate top-level package* (`src/pipeline/lN_…`, substrate keeps `src/mtdsim/`): cleaner axis separation, but the pipeline *is* the project — folding the stages into `src/mtdsim/` as siblings to the future substrate role-modules is simpler and still merge-coherent (stage names `l0_cti…` never clash with role names `network/defender/…`).
- *Reorganise the substrate too* (mtdnetwork → role-based src/mtdsim, adopting attacker-profiling): rejected here — inherited, golden-bearing, and its layout belongs to the attacker-profiling reconciliation, not this simplification.

## Validation gate

- `PYTHONPATH=src pytest tests/ -q` green — gap gate still 13/13; full suite unchanged.
- Rebuild (`python -m mtdsim.l1_construction`, or the `scripts/` shim) reproduces `data/gap/` **byte-identically** (the determinism check in [`data/gap/README.md`](../../data/gap/README.md)).
- `grep -rn "attacker\.gap\|attacker/gap" src tests docs` returns nothing — no dangling references.
- `python -c "import mtdsim.l0_cti, mtdsim.l1_construction"` succeeds.
- `src/mtdsim/README.md` cross-walk lists all five stages with status.

## Hard constraints

- **Do not touch `mtdnetwork/`** — the substrate, its goldens, SIM-05 determinism. Out of scope.
- The move must be **behaviour-neutral**: GAP build determinism + the 13-test gate hold unchanged.
- Keep `data/gap/` artefacts + the `.gitignore` split (inputs ignored; extracts + aggregate committed).
- Branch / commit / **never push** without asking, per [`../specs/session_workflow.md`](../specs/session_workflow.md). The substrate ↔ `feat/attacker-profiling` `src/mtdsim` reconciliation is a *separate, future* decision — do not start it here.

## Reading list

- [`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md) — what L1 produces + its assumptions.
- [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) §(f),(i) — the L1 code-location lines to update.
- [`../specs/architecture.md`](../specs/architecture.md) §(c)–(g),(i) — the L0–L4 levels the dirs mirror + the substrate seam (L3/L4 live in `mtdnetwork/`).
- [`../notes/2026-05-27_docs_audit.md`](../notes/2026-05-27_docs_audit.md) §3 — the code-location gap this closes.
- `src/mtdsim/attacker/gap/build.py` — the `_REPO_ROOT` depth + CLI shape that move.

## Out of scope (explicitly)

- Substrate (`mtdnetwork/`) reorganisation; the `feat/attacker-profiling` merge.
- Building L2/L3/L4 — stubs + pointers only.
- Porting v0.4 selectors / viz / motivation enrichment — pointers only; per the zero-trust stance any future build is fresh, not a port.
