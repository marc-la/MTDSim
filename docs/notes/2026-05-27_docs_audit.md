---
status: durable
created: 2026-05-27
topic: docs-audit
---

# Audit of `docs/`, `.claude/`, and `CLAUDE.md` — findings

Read-only audit produced under the
[`2026-05-27_docs_audit`](../handoffs/2026-05-27_docs_audit.md) handoff (now
shipped — this note is the deliverable). Pressure-tests the doc system across
the 8 dimensions the handoff names. **No specs, handoffs, or extractions were
edited; CLAUDE.md was touched only to retire the audit handoff pointer and to
link this file.** Follow-up sessions land the fixes.

The audit is **critical**: where the doc system is good, the finding is "no
issues at this severity"; where the doc system is correct but unsupported, the
finding records the unsupported-claim count. Section-level counts and an
overall scoreboard sit at the end.

## How to read a finding

```
- **[severity]** <file>:<line> — one-sentence finding. Recommendation: one sentence.
```

Severities:
- `must-fix` — correctness; the doc actively misleads (a cold session would
  draw the wrong conclusion).
- `should-fix` — gap; a cold session would stumble (the missing thing is
  load-bearing for the doc's stated purpose).
- `nice-to-have` — polish; the doc is correct but could be sharper.

---

## 1 — Structural integrity

Does every file sit in the subtree whose lifecycle matches its content
([`repo_conventions.md`](../specs/repo_conventions.md#L9)):
*specs* durable; *handoffs* live & deleted-when-shipped; *notes* durable
dissertation-source; *extractions* durable per-paper.

- **[nice-to-have]** [`docs/extractions/attackflow.md`](../extractions/attackflow.md) — the file
  documents the **CTID Attack Flow specification** (an institutional artefact),
  not an author-year paper, so it does not fit the extraction
  [`_template.md`](../extractions/_template.md)'s `<Author Year>` opening or
  citation-key contract. The handoff
  [`bibliographic_anchors`](../handoffs/2026-05-27_bibliographic_anchors.md#L28)
  already flags this implicitly under A4. Recommendation: either keep it where
  it is and add a one-line "non-paper sources use institutional citation"
  variant to the template, or split institutional/spec sources to a sibling
  `docs/extractions/_specs/` subtree.
- **[nice-to-have]** [`docs/notes/`](../notes/) — directory contains only
  `_template.md` despite (a) the substrate-side re-baseline producing
  dissertation-worthy decisions in Phase 2c (NCR repair, HCR fix, ATK-04
  disambiguation) and (b)
  [`metrics_semantics.md`](../specs/metrics_semantics.md) §c being the only
  prose record of the ATK-04a/b split. Recommendation: not the audit's job to
  fix, but flag that the notes subtree is under-used relative to its stated
  purpose; the Phase-2c findings are the obvious candidate for promotion.

**Section count:** 0 must-fix · 0 should-fix · 2 nice-to-have.

---

## 2 — Cross-doc consistency

Pairwise reads across the 8 specs, plus the two non-audit open handoffs.

- **[should-fix]** [`repo_conventions.md`:34](../specs/repo_conventions.md#L34)
  vs [`project_context.md`:10](../specs/project_context.md#L10) — both
  encode the "Tay deferred, no retrain" decision, but with very different
  levels of detail (L34 carries the feature-pipeline mismatch detail; L10
  carries only the high-level deferral). The detailed copy lives in a
  *conventions* spec (where the lifecycle is "update when the docs tree or
  environment changes"), not in a *project_context* one (where direction
  decisions belong). Two-source-of-truth ⇒ drift risk on the next Tay
  decision change. Recommendation: promote the L34 detail into
  `project_context.md` (or a dedicated decision row in
  [`architecture.md`](../specs/architecture.md) §(a) — there's already a
  Tay-reuse decision there at L70-77, with no mention of the
  feature-pipeline mismatch); collapse `repo_conventions.md` L34 to a
  one-line pointer.
- **[should-fix]** [`architecture.md`:33-34](../specs/architecture.md#L33)
  and [`architecture.md`:359](../specs/architecture.md#L359) name "Tay's AI
  selection" as part of the existing-defender pool, but the §(i) substrate
  seam table's RL-benchmark row says "Reused as benchmark defence, not
  extended" — which is the project_context.md L10 framing of Tay-as-deferred
  *benchmark*, not as part of the active defender pool. The two framings
  point at the same code but assign it different roles. Recommendation:
  one-sentence reconciliation in §(a) — Tay is *both* (i) inherited
  benchmark-defence to replicate, and (ii) one of the L4 comparison points,
  not just (i) — so the reader can tell whether Tay shows up at L4 as a
  comparator or only as a baseline trace.
- **[should-fix]**
  [`architecture.md`:82-98](../specs/architecture.md#L82-L98) (ASCII pipeline
  diagram) is the *only* visual representation of the L0→L4 pipeline, and
  it elides what
  [`metrics_semantics.md`](../specs/metrics_semantics.md) §d names as the
  comparability boundary (within-substrate valid; cross-paper invalid).
  Without that, a reader looking at the diagram and the L4 metric list
  ("MTTC | ASR | ...") would not be cued that the numbers are
  within-substrate-only. Recommendation: footnote the L4 column with a
  one-line "metric values are within-substrate; see metrics_semantics §d".
- **[should-fix]**
  [`architecture.md`:21-27](../specs/architecture.md#L21) names L0–L4 with the
  acronyms (GAP / GASP / OGASP) **before**
  [`architecture.md`:316-344](../specs/architecture.md#L316) defines them in
  the glossary (§(h)). A cold reader hits "GAP", "GASP", "OGASP" in §(a)–(b)
  with no expansion until ~270 lines later. Recommendation: parenthesise the
  expansion on first use ("L1 GAP (Generalised APT Profile)") in §(a).
- **[nice-to-have]**
  [`architecture.md`:121-130](../specs/architecture.md#L121) (Attack Flow
  schema decision) repeats material that
  [`architecture.md`:448-450](../specs/architecture.md#L448) (open question
  #1) also names. The decision-block already records the unresolved state;
  the open-question item re-states it as "open" — two rows on the same
  unresolved fact. Recommendation: have §(l)'s item link to §(c)'s decision
  block rather than re-stating it.
- **[no-issue]** [`architecture.md`:347-364](../specs/architecture.md#L347)
  §(i) substrate-seam table matches
  [`project_context.md`:17](../specs/project_context.md#L17) on the
  attacker-module seam ("graph-driven … *alongside* … not replacing"). The
  cross-reference holds.
- **[no-issue]**
  [`architecture.md`:412-438](../specs/architecture.md#L412) §(k) validation
  strategy item 4 cites
  [`metrics_semantics.md`](../specs/metrics_semantics.md) §d for the
  comparability boundary and does so verbatim-consistently with §d's table.
- **[no-issue]** The two non-audit open handoffs cross-reference each other's
  scope correctly (architecture handoff Pass-2 step 3 names the stubs that
  bibliographic-anchors then settles).

**Section count:** 0 must-fix · 4 should-fix · 1 nice-to-have · 3 no-issue.

---

## 3 — Coverage gaps

What's load-bearing in the project but undocumented in any spec.

- **[must-fix]** Attack Flow `.afb` **parser entrypoint** — named only in
  [`architecture.md`:111-113](../specs/architecture.md#L111) (L0 inputs
  description) and as
  [`architecture.md`:448-450](../specs/architecture.md#L448) open question
  #1. The handoff's audit dimension #3 flagged this. The parser is L1's
  *only* path from corpus to graph; without a spec, every Pass-2 session
  that touches L1 is re-deriving the schema-vs-parser contract from
  scratch. Recommendation: a single block at the end of §(c) — current
  in-tree `.afb` location (`notebooks/attack-flow/`, per the handoff's
  carry-forward note), schema version pinned, fields parsed. Not a new
  spec, just a 5-line block in `architecture.md`.
- **[should-fix]** **SDR taxonomy detail.** Defined as the acronym
  expansion in
  [`architecture.md`:335-337](../specs/architecture.md#L335) — *"shuffle
  / diversity / redundancy, the canonical MTD taxonomy"* — but the three
  primitives are never characterised (no "shuffling rearranges, diversity
  varies implementations, redundancy replicates"). The closest text is in
  the (gitignored) lit review and in the
  [`cho2020.md`](../extractions/cho2020.md) stub. Since SDR is the
  defender side of the load-bearing comparison axis, the docs should
  carry at least a two-sentence characterisation rather than relying on
  the lit review. Recommendation: extend the §(h) glossary entry to three
  one-line definitions; do **not** create a dedicated spec.
- **[should-fix]** **Network topology default — "generic" but never
  pinned.** [`project_context.md`](../specs/project_context.md) names
  "generic" implicitly via the "no thesis-specific topology" framing;
  [`architecture.md`:354](../specs/architecture.md#L354) says "Generic by
  design"; [`architecture.md`:455-459](../specs/architecture.md#L455)
  open question #5 records the gap; but
  [`mtdsim_spec.md`:62-64](../specs/mtdsim_spec.md#L62) NET-04/05 say the
  *defaults* are Brown-divergent (`50/5/4/8` instead of Brown's `200/20/5/20`).
  The substrate's "generic" is *not* generic to Brown's — it's a divergent
  default. A reader of `architecture.md` alone would not know this.
  Recommendation: a single cross-link from §(i)'s "Network model" row to
  [`mtdsim_spec.md`](../specs/mtdsim_spec.md) NET-04/05.
- **[should-fix]** **GAP / GASP / OGASP code locations.** All three are
  described in `architecture.md` §(d)–(f) at the conceptual level, but
  none of them point at *where in `mtdnetwork/` they will be hooked* or
  *whether the v0.4 GAP implementation is in-tree*. The §(d) status line
  says "v0.4 implementation exists" without naming a path. A cold session
  would `grep -r "GAP"` and find nothing. Recommendation: one line per
  section — "implemented at `<path>` (when present)" or "not yet
  hooked into the substrate". Cross-link to
  [`provenance.md`](../specs/provenance.md) for any constants the L1 step
  carries.
- **[nice-to-have]** **Motivation specifier enumeration.**
  [`architecture.md`:177-178](../specs/architecture.md#L177) says
  *"e.g. espionage, disruption, financial"* — "e.g." suggests the set is
  open; nothing pins the canonical three. The L4 evaluation matrix
  ([`architecture.md`:460-463](../specs/architecture.md#L460) open
  question #6) cannot be pinned without this. Recommendation: enumerate
  the set (even as "TBD, expected ≈ 3") in §(e); state explicitly whether
  the set is open or closed.

**Section count:** 1 must-fix · 3 should-fix · 1 nice-to-have.

---

## 4 — Drift / staleness

References to decommissioned threads or out-of-date state.

- **[must-fix]** [`guardrails.md`:9](../specs/guardrails.md#L9) — "**`feat/replay-viz`:** do
  not merge it wholesale. Pull only substrate-relevant fixes, as
  individually reviewed cherry-picks." This rule predates the Phase-2c
  re-baseline and the lit-review landing. No recent commit
  (`git log --oneline -30 -- guardrails.md` shows nothing referring to
  cherry-picks from `feat/replay-viz`); the architecture-prepopulation
  handoff Pass-1 commit already noted "stale items (replay-viz
  visualiser, …) were dropped silently". The guardrails rule reads as
  active enforcement when it's effectively dormant. Recommendation:
  either confirm the cherry-pick source is still live and add a
  one-line "last pick: <date>" timestamp; or retire the bullet and move
  its substance to a one-line note about deferred Stream A/B work.
- **[must-fix]**
  [`2026-05-27_architecture_prepopulation.md`:26](../handoffs/2026-05-27_architecture_prepopulation.md#L26)
  — Pass-2 "still owes" bullet says "Adjacent-paper extraction stubs
  (CTI standards, behavioural-attacker work, adjacent MTD evaluation) —
  **none created yet**; Marc to supply the title list at Pass 2 start."
  This is **stale as of today (2026-05-27)**: 18 adjacent stubs landed
  in commit `2b7dc48` ([`docs/extractions/`](../extractions/) is now 22
  files = 4 lineage + 18 adjacent stubs + template). The handoff
  contradicts the working tree. Recommendation: edit the handoff's
  Pass-2 section to mark the stub-creation bullet shipped and replace
  with the Pass-2 deep-extraction expectation (one paper per session).
- **[must-fix]**
  [`2026-05-27_bibliographic_anchors.md`:1-3](../handoffs/2026-05-27_bibliographic_anchors.md#L1)
  — handoff frontmatter still says `status: open` despite the work
  shipping in commit `56c7a02` ("docs(extractions): resolve
  bibliographic anchors per handoff …", landed earlier in this session
  by a concurrent run). The handoff file should have been deleted (per
  [`session_workflow.md`:32-35](../specs/session_workflow.md#L32) —
  "Deleted when the work lands") and CLAUDE.md (which never listed it
  to begin with — cross-listed as a §8 finding) should reflect a
  shipped state. Index now under-reports closed work as open work.
  Recommendation: delete the handoff file in a follow-up commit;
  consider whether the commit that closes a handoff should also
  delete it (a one-line addition to
  [`session_workflow.md`:32-35](../specs/session_workflow.md#L32)
  would settle this).
- **[no-issue]** [`project_context.md`:10](../specs/project_context.md#L10)
  ("IDS is **not** a research thread") is consistent with
  [`architecture.md`:56-61](../specs/architecture.md#L56)
  (Decision — IDS is not a research thread) and with
  [`mtdsim_spec.md`:22](../specs/mtdsim_spec.md#L22) (the
  `[IDS-SEAM]` retirement note). No drift; the IDS culling is fully
  reconciled.
- **[no-issue]** "6,000s crash" — resolved per
  [`project_context.md`:21](../specs/project_context.md#L21) and not
  re-stated in `architecture.md` (the prepopulation handoff explicitly
  dropped it from the scaffold). No drift.
- **[no-issue]** "4-section lit-review structure" — referenced via the
  source-file naming convention in
  [`2026-05-27_architecture_prepopulation.md`:114-126](../handoffs/2026-05-27_architecture_prepopulation.md#L114),
  not as an active workstream. The naming convention's structure matches
  the source-tree listing (1_1_, 1_2_, ..., 4_); no drift.

**Section count:** 3 must-fix · 0 should-fix · 0 nice-to-have · 3 no-issue.

---

## 5 — Critical-evaluation quality

Marc's primary concern: when a spec makes a claim, is the claim justified?
This section records the **unsupported-claim count** rather than fixing
them in-line. Pass 2 of the architecture prepopulation is the formal
fix-cycle — every "no extraction backs this" finding below is recorded for
that pass to retire.

### Unsupported claims (claims that depend on the lit review but cite nothing)

- **[should-fix]**
  [`architecture.md`:383-385](../specs/architecture.md#L383) — *"the
  dominant MTD evaluation pattern … is single-mechanism, single-network
  optimisation against procedurally-scripted attackers."* Cites only
  `project_context.md` L27 (the **codebase lineage**, not the wider
  literature). "Dominant" is a literature-pattern claim; the codebase
  lineage is four papers, not "the literature". Recommendation (Pass 2):
  cite at least two adjacent extractions (`he2025`, `kim2026`, plus a
  third from §IV-B) as evidence of "dominant".
- **[should-fix]**
  [`architecture.md`:385-386](../specs/architecture.md#L385) — *"Attacker
  fidelity sits at the bottom of the Pyramid of Pain (hashes, IPs,
  artefacts) even though MTD's claimed defensive value extends upward to
  TTPs."* No citation. The Pyramid is named in
  [`bianco2013.md`](../extractions/bianco2013.md) (stub) and the
  peer-reviewed corroboration in
  [`sadlek2022.md`](../extractions/sadlek2022.md) (stub). Recommendation
  (Pass 2): cross-link both extractions in §(j) once they're fleshed.
- **[should-fix]**
  [`architecture.md`:387-392](../specs/architecture.md#L387) — *"This
  work sits at the intersection of (a), (b), (c)"* — three literatures
  named, zero extractions cited. Recommendation (Pass 2): one extraction
  per literature, in-line.
- **[should-fix]**
  [`architecture.md`:397-399](../specs/architecture.md#L397) — *"MITRE
  ATT&CK Evaluations gives EDR-style ground truth, not MTD-specific
  ground truth."* No citation; ATT&CK Evaluations is not in
  [`docs/extractions/`](../extractions/). Recommendation (Pass 2):
  either add an ATT&CK-Evaluations extraction stub, or recast as
  "no MTD-specific ground truth exists in any public CTI corpus that we
  surveyed (see §IV of the lit review)".
- **[should-fix]**
  [`architecture.md`:399-407](../specs/architecture.md#L399) — the
  four-axes comparison against **Rodríguez et al. 2024** rests on a
  stub [`rodriguez2024.md`](../extractions/rodriguez2024.md), so the
  axes (input class / temporal stance / output use / validation) are
  asserted without backing. Recommendation (Pass 2): Pass-2 deep
  extraction of `rodriguez2024.md` is the highest-leverage fix here —
  the "this is just process mining" reading is the single most
  defensible critique a reviewer would make.
- **[should-fix]**
  [`architecture.md`:249-256](../specs/architecture.md#L249) — the three
  Jalowski primitives (state-collision recognition, beacon
  conditioning, metadata-invariance) are named as the operationalisation
  of "behaviourally grounded" but rest on a stub
  [`jalowski2026.md`](../extractions/jalowski2026.md). Recommendation
  (Pass 2): Pass-2 of `jalowski2026` is the second-highest leverage fix
  — the §(f) decision block is the load-bearing claim that "behavioural
  grounding" is a definable thing.

**Unsupported-claim count (architecture.md only): 6.**

### Design presented as fact

- **[no-issue]**
  [`architecture.md`:179-200](../specs/architecture.md#L179) — L2 GASP's
  terminal-node-ancestor proxy *is* surfaced sharply: the §(e) opening
  marks "Status: partially built (terminal-node-ancestor proxy
  implemented; the 'true' motivation-attribution method is
  unfinalised)"; the decision block at L191-200 explicitly calls the
  proxy *"a structural surrogate for motivation"* and lists what swapping
  to NLP would change. The proxy-vs-motivation conflation that the audit
  handoff worried about is *not* present. (This is the rare dimension
  where the docs are doing the critical-evaluation work the audit was
  testing for.)

### Decisions without `If revisited:` lines

- **[should-fix]**
  [`project_context.md`:20](../specs/project_context.md#L20) — the
  *"internal/lineage preset was evaluated and DROPPED"* decision has no
  `If revisited:` line. It is recoverable from
  [`metrics_semantics.md`:185-210](../specs/metrics_semantics.md#L185)
  §(e), which says "Resurrecting the preset would mean re-introducing
  maintained divergence-flags in the substrate — large reverse-step."
  But that consequence sits in a different spec from where the decision
  is recorded. Recommendation: add a one-line "If revisited: see
  metrics_semantics §(e) for the reverse-step cost" to L20.
- **[should-fix]**
  [`project_context.md`:9](../specs/project_context.md#L9) — *"Single
  RQ. No sub-problems."* has no revisit criterion. Architecture's §(a)
  L40-47 carries the decision block with both `Why:` and `If revisited:`,
  but that copy sits behind a load-only spec. Recommendation: make
  `project_context.md` L9 a one-line link to `architecture.md` §(a)
  rather than restating the decision.
- **[should-fix]**
  [`project_context.md`:18](../specs/project_context.md#L18) — *"No new
  defender mechanisms; no training novel RL agents from scratch."* —
  same issue: architecture's §(a) L49-54 has both `Why:` and `If
  revisited:`, project_context restates the rule without revisit
  criteria. Same recommendation.
- **[should-fix]** [`metrics_semantics.md`](../specs/metrics_semantics.md)
  — none of the §(b)/§(c)/§(d) decisions ("kept deliberately",
  "single-canonical substrate", "comparability boundary is asymmetric")
  carry an `If revisited:` line. §(c) ATK-04a in particular says
  *"Kept deliberately (Marc, Unit C). Cutting it is a behavioural change
  requiring a golden re-baseline — a separate, deliberate decision"* —
  which is **the revisit criterion**, but it's not labelled as one.
  Recommendation: add explicit `If revisited:` labels to the existing
  prose (no new content, just structure).

### Decisions without consequence statements

- **[should-fix]**
  [`architecture.md`:70-77](../specs/architecture.md#L70) — *"Tay's RL
  agent is reused as benchmark defence, not retrained."* The `Why:`
  block argues *"no research payoff"*. The `If revisited:` block argues
  *"fall back to 'reference RL benchmark unavailable' rather than
  retraining"*. Neither states the **cost in evaluation power**: a
  retrained Tay would let L4 distinguish "MTD-AI selection learns on
  this corrected substrate" from "MTD-AI selection is inherited as-is,
  not optimised for this comparison". The current decision says it's
  not retrained; it doesn't say what that costs the evaluation.
  Recommendation: a one-line addition to the `Why:` block — "Cost:
  L4 cannot disentangle MTD-AI's per-substrate optimisation from
  Tay's published policy; reported as an inherited-policy result, not
  an optimised-policy result."
- **[should-fix]**
  [`architecture.md`:49-54](../specs/architecture.md#L49) — *"defence
  side is existing mechanisms only"* — no consequence statement. The
  cost is that any L4 finding of the form "Y is the best MTD" is
  bounded by the SDR-family plus Tay's AI selection; a defender-novelty
  paper would not be able to read off "this is the best MTD" from the
  results. Recommendation: a one-line "Cost: comparative claims at L4
  are scoped to the existing-MTD pool; novel-defender claims are out
  of evaluation reach."
- **[should-fix]**
  [`architecture.md`:155-162](../specs/architecture.md#L155) (decision
  on L1 graph-driven traversal vs. linear amplification) has a clean
  `Why:` / `If revisited:` pair but no consequence: the graph-driven
  path *forecloses* the cheap PoC comparison against the linear
  baseline. Recommendation: a one-line "Cost: no linear-amplification
  comparator at L4; the procedural 6-phase baseline carries the
  comparator role on its own."

**Section count:** 0 must-fix · 12 should-fix · 0 nice-to-have ·
1 no-issue. **Unsupported-claim count: 6 (all in `architecture.md` §(a)
+ §(f) + §(j)) — Pass 2 of the prepopulation handoff is the formal
fix-cycle.**

---

## 6 — Entry-point quality

`CLAUDE.md` read cold (imagining no conversation context, no memory).

- **[should-fix]** [`CLAUDE.md`:23-26](../../CLAUDE.md#L23) — the
  session-start checks list only two commands (`git branch
  --show-current` and `ls docs/handoffs/`), but
  [`session_workflow.md`:60-67](../specs/session_workflow.md#L60) names
  *four* checks (also `git status --short` for a clean tree, and "treat
  the handoff as the prompt if the session was triggered by one"). A
  cold session that read `CLAUDE.md` and stopped would skip the clean-
  tree check — the audit session today actually hit this case: the
  current branch is `chore/extraction-anchors`, not `main`, with four
  in-flight uncommitted files. The fuller checklist would have flagged
  it; the CLAUDE.md subset did not. Recommendation: either inline all
  four session_workflow checks in CLAUDE.md, or change L23 to "Run the
  session-start checklist in session_workflow.md §session-start
  checklist" (and remove the partial list).
- **[should-fix]** [`CLAUDE.md`](../../CLAUDE.md) — no mention of
  `.claude/` anywhere. The entry-point file orients new sessions but
  does not acknowledge that a harness-configuration directory exists,
  let alone that the only file in it
  (`.claude/settings.local.json` — 165 bytes, four `Bash` allows for
  package management) is the entire harness configuration. A cold
  session would not know whether a tool action is constrained by
  settings or by guardrail prose. Recommendation: a one-line
  "Harness config lives in [`.claude/`](.claude/); the rules that the
  harness *should* enforce live in
  [`docs/specs/`](docs/specs/) — for now, the harness only carries
  permission allowlists."
- **[should-fix]** [`CLAUDE.md`:11](../../CLAUDE.md#L11) — the
  read-first list opens with `guardrails.md` (the rules), followed by
  `session_workflow.md` (the flow), and only reaches
  `project_context.md` (what the project **is**) at step 3. A cold
  session is asked to internalise rules and flow before knowing what
  the project is. The current order is correct for *behavioural
  safety* (rules first) but unhelpful for *orientation*. Recommendation:
  not change the order, but add a one-line preamble — "If you only
  read one of these, read `project_context.md` for context; the rest
  govern behaviour." — so the read-first list signals which file is
  the orientation document.
- **[nice-to-have]** [`CLAUDE.md`:18](../../CLAUDE.md#L18) — describes
  `architecture.md` as "Pass 1 scaffold; methodological positioning
  still to flesh." This is correct as of today, but the marker will
  become stale the moment Pass 2 lands. Recommendation: shift the
  "scaffold / Pass 2 outstanding" status into the architecture.md
  frontmatter (it already lives in
  [`architecture.md`:3-9](../specs/architecture.md#L3)); have
  CLAUDE.md L18 point at the spec's own status line rather than
  restating it.
- **[no-issue]** The "Spec files (load when relevant)" tier
  ([`CLAUDE.md`:16-21](../../CLAUDE.md#L16)) is visually distinct from
  the read-first tier — separate header, separate framing. A cold
  session would not confuse them.
- **[no-issue]** `architecture.md`'s position in the spec-files tier
  (first, ahead of `mtdsim_spec.md`) is correct: it is the newest and
  most cross-cutting, and the others slot under it.

**Section count:** 0 must-fix · 3 should-fix · 1 nice-to-have · 2 no-issue.

---

## 7 — `.claude/` alignment

`session_workflow.md` and `guardrails.md` carry rules of the form *X must
hold*. Which of those rules could (or should) be enforced via `.claude/`
hooks or settings rather than relying on prose?

- **[should-fix]** **No `.claude/settings.json` (shared,
  version-controlled).** Only [`settings.local.json`](../../.claude/settings.local.json)
  exists. The four `Bash` allowlist entries are
  package-management commands — useful for the local user, but the
  team-wide / cross-session rules
  (never-commit-to-main, never-push, never `--no-verify`,
  never-touch-`docs/sources/`) live in prose in
  [`session_workflow.md`](../specs/session_workflow.md) and
  [`guardrails.md`](../specs/guardrails.md) with no corresponding
  harness enforcement. The asymmetry is the load-bearing finding here:
  the rules are spec'd, not enforced. Recommendation: create
  `.claude/settings.json` (committed) carrying the shared allowlist;
  keep `settings.local.json` for the per-user package-management
  layer.
- **[should-fix]** **No pre-commit / pre-push hook against `main`.**
  [`session_workflow.md`:7-12](../specs/session_workflow.md#L7) names
  *never commit to `main`* as non-negotiable; the audit session today
  is also operating under this rule. The repo has
  [`.git/hooks/`](../../.git/hooks) with the standard `*.sample` files
  (none renamed/activated). The rule is enforced by social contract,
  not by mechanism. Recommendation: install a one-line `pre-commit`
  hook (`[ "$(git branch --show-current)" = "main" ] && {
  echo "refuse: commit on main"; exit 1; }`) — single foot-gun fix.
- **[should-fix]** **No allowlist for the docs-touching tool set.**
  The current `Bash` allows are all package management
  ([`settings.local.json`](../../.claude/settings.local.json)). Doc
  sessions (this one, the architecture prepopulation, the
  bibliographic anchors) make heavy use of `git status`, `git diff`,
  `git log`, `find docs/`, `ls docs/`, `wc -l docs/` etc. — every one
  prompts. Recommendation: extend the allowlist with the read-only
  `git status:*`, `git diff:*`, `git log:*`, `ls:*`, `find docs:*`,
  `wc:*`, `grep:*` patterns. **Not Read/Edit/Write on `docs/**`** —
  those should remain prompt-gated because the never-push rule has
  to start from somewhere visible.
- **[nice-to-have]** **No `.claude/hooks/` at all.** Hooks could
  enforce other guardrails (e.g. *never edit
  `docs/extractions/{brown,zhang,ho,tay}2023*.md`*) but adding hooks
  on the basis of a single audit is premature. Recommendation: don't
  add hooks until a specific incident motivates one; record this as a
  *capability gap* rather than a *deficiency*.

**Section count:** 0 must-fix · 3 should-fix · 1 nice-to-have.

---

## 8 — Handoff hygiene

`session_workflow.md` §stale-handoff-sweep:
*"if a handoff exists for completed work, delete it. If it's been
superseded, mark `status: superseded by <new-handoff>` … Don't leave
dead handoffs accumulating."*

- **[must-fix]**
  [`2026-05-27_architecture_prepopulation.md`:26](../handoffs/2026-05-27_architecture_prepopulation.md#L26)
  — the Pass-2 "still owes" bullet about adjacent-paper extraction
  stubs is stale (already covered as a drift finding in §4 above; the
  duplication is deliberate — handoff hygiene and drift are different
  framings of the same problem). Recommendation (same as §4):
  edit the handoff bullet.
- **[should-fix]**
  [`2026-05-27_bibliographic_anchors.md`](../handoffs/2026-05-27_bibliographic_anchors.md)
  — validation gate is concrete (item 1: `rg 'TODO' …` returns nothing;
  item 4: one commit on the chosen branch). One unambiguity: gate item
  3 says *"For any A-item that required changing the lit-review
  citation form (A1, A3 most likely), the lit-review file at
  `docs/sources/LIT_REVIEW.md` is updated in the same session."* But
  `docs/sources/` is gitignored, so the "same session" update is not
  reviewable from git — the handoff doesn't say how Marc verifies the
  lit-review update without seeing a diff. Recommendation: gate item 3
  should require the changed citation form to be quoted *in the
  commit message* (or in a `docs/notes/` companion file) so review is
  possible without leaving the repo.
- **[should-fix]**
  [`2026-05-27_architecture_prepopulation.md`](../handoffs/2026-05-27_architecture_prepopulation.md)
  validation gate item 1: *"a cold session can read it +
  `project_context.md` and answer: 'what does this project do,
  end-to-end, with what inputs and what outputs?' …"* This is a
  subjective gate ("can answer"). The audit session today tested
  approximately this — reading the two files cold *does* answer the
  question — but the gate doesn't pin "answers" to a tangible artefact.
  Recommendation: rewrite the gate as "Pass 2 closes when a fleshed §(j)
  cites at least the four lit-review extractions named under §IV-A/B
  and the audit's six unsupported-claim findings (§5 of
  [`2026-05-27_docs_audit.md`](../notes/2026-05-27_docs_audit.md)) are
  retired."
- **[must-fix]** [`CLAUDE.md`'s open-handoffs section](../../CLAUDE.md#L28)
  (pre-audit state) omitted the
  [`bibliographic_anchors`](../handoffs/2026-05-27_bibliographic_anchors.md)
  handoff — the directory carried three open handoffs (architecture,
  bibliographic, audit) but the index listed only two
  (architecture, audit). A cold session reading CLAUDE.md alone would
  not know the bibliographic-anchors work was open. (This finding stood
  pre-audit; this audit's gate-completion edit retires only the audit
  pointer and the findings link, not the bibliographic-anchors gap —
  flagged here for a follow-up edit, per the handoff hard constraint
  that the audit not edit `CLAUDE.md` beyond the gate pointer.)
  Recommendation: a single-line addition to the open-handoffs section
  for the bibliographic-anchors handoff. Procedurally this also
  reveals that the architecture-prepopulation handoff (which created
  the bibliographic gap by spinning out the cleanup work) did not
  update CLAUDE.md when it spawned its child handoff — worth a
  one-line "when you spin a handoff, update CLAUDE.md" addition to
  [`session_workflow.md`](../specs/session_workflow.md#L26)'s
  handoff workflow.

**Section count:** 2 must-fix · 2 should-fix · 0 nice-to-have · 0 no-issue.

---

## Scoreboard

| Dimension | must-fix | should-fix | nice-to-have | no-issue |
|---|---:|---:|---:|---:|
| 1. Structural integrity | 0 | 0 | 2 | — |
| 2. Cross-doc consistency | 0 | 4 | 1 | 3 |
| 3. Coverage gaps | 1 | 3 | 1 | — |
| 4. Drift / staleness | 3 | 0 | 0 | 3 |
| 5. Critical-evaluation quality | 0 | 12 | 0 | 1 |
| 6. Entry-point quality (CLAUDE.md) | 0 | 3 | 1 | 2 |
| 7. `.claude/` alignment | 0 | 3 | 1 | — |
| 8. Handoff hygiene | 2 | 2 | 0 | 0 |
| **Total** | **6** | **27** | **6** | **9** |

**Unsupported-claim count (architecture.md, claims that depend on the lit
review but cite no extraction): 6.** All in §(a) + §(f) + §(j); all
retire-able via Pass 2 of the architecture-prepopulation handoff.

### Headline

The doc system is **substantively correct but evaluatively thin**. Of 39
total findings, **6 are `must-fix` correctness issues** — two are
drift (`feat/replay-viz`; stale Pass-2 bullet, double-counted as a
handoff-hygiene must-fix per the cross-listing in §8), one is a
coverage gap that's already been flagged (`.afb` parser), one is the
index gap (CLAUDE.md silently omitted the bibliographic-anchors
handoff throughout its life), and **two cluster on handoff hygiene
that broke during this very session**: the bibliographic-anchors work
shipped in `56c7a02` without deleting its handoff (the file still says
`status: open` despite a closing commit), and CLAUDE.md's index never
listed the handoff to begin with — both reveal that the
handoff-lifecycle rules in
[`session_workflow.md`](../specs/session_workflow.md#L26)
are not self-enforcing across concurrent sessions. The substrate-
side specs (`mtdsim_spec.md`, `metrics_semantics.md`, `provenance.md`) and
the four lineage extractions show no `must-fix` issues at all — they were
pressure-tested through the Phase-2c re-baseline and that work shows.

The **28 `should-fix` findings cluster heavily in dimension 5
(critical-evaluation quality, 12 findings)**, which is exactly Marc's
framing of the audit: "lots of writing, not lots of evaluating." The
newer methodological material — `architecture.md` §(a)/§(f)/§(j),
`project_context.md`'s decision lines without revisit criteria — was
written under deadline pressure for the lit-review landing and **has
not been read against itself**, in the sense that decisions are stated
without consequence statements and claims are made without extractions
backing them. The six unsupported claims in `architecture.md` §(j)
"methodological positioning" are the single highest-leverage cluster:
Pass 2 of the prepopulation handoff retires them as a unit, and the
two most load-bearing fleshes (Jalowski's primitives,
Rodríguez's process-mining comparison) cover three of the six. The
`If revisited:` and consequence-statement gaps in older specs
(`project_context.md`, `metrics_semantics.md`) are mechanical to fix —
the substance is already in the prose, just not labelled.

The **3 `should-fix` findings on `.claude/`** (no shared
`settings.json`; no pre-commit hook against `main`; no doc-tool
allowlist) reveal a more structural pattern: the doc system has
codified what *should* hold — the rules are clear in
`session_workflow.md` and `guardrails.md` — but **does not enforce** any
of it via the harness layer. That gap is a deliberate design choice
worth Marc's explicit attention, not just an oversight worth patching;
the docs-as-prose / harness-as-config dichotomy is itself a thesis-
adjacent observation about how research-code conventions get
codified.
