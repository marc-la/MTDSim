---
status: durable
created: 2026-05-28
topic: L2 assembly audit — outcome of the post-land coherence check
---

# L2 assembly audit — outcome

> **Provenance banner.** Audit outcome (PASS / FIX / DEFER), not
> investigation history. Spec:
> [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md).

- **§1 Cross-links.** FIX `1069bc0`, `231b197` — stale "implementation
  pending" pointers in spec/arch/`src/mtdsim` README; missing
  `02_gasp_schema.md` in `repo_conventions.md` specs row.
- **§2 File locations.** PASS.
- **§3 Project context.** FIX `fabcdbb`, `08ecfb2` — `motivation` →
  `operational-objective` in project_context L16, arch §(a)/§(k),
  `01_gap_schema.md`; §(j) gained an audit-trace pointer.
- **§4 Notes.** FIX `6605b65` — four notes referenced now-deleted
  simulator-verification / partition-investigation handoffs; added
  "Status update" banner to each. MEMORY: no stale L2 entries.
- **§5 Test + build.** FIX `43d1740` — operator-dedup JSD null was
  non-deterministic (set iteration × seeded shuffle); sorted before
  seed. 20/20 tests pass, build byte-stable, viz regenerates clean.
- **§6 Simplifications.** PASS on duplication + v0.4-ref provenance.
  DEFER: audit-CSV ↔ code name asymmetry (4-name rename > one-line
  budget). DEFER: CISA AA22-138B 403 on legacy + canonical URLs with
  browser UA; `low` confidence stays.
- **§7 Provenance.** PASS — P1/P2/P3/P4/P5/P7 each named with mechanism
  + drop reason; rubric and Def A/B/D recorded.
- **Architecture decision-block (critique 3).** FIX `08ecfb2` — added
  *operational-objective axis* decision block to arch §(e).

No DEFERs are critical-path.
