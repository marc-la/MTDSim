---
status: open
created: 2026-05-27
---

# Resolve bibliographic anchors flagged across the 19 extraction stubs

Each Pass-1 extraction stub committed in `2b7dc48` carries one or more `TODO` items in its bibliographic anchor or open-questions section — citation forms, DOIs, venues, or first-author/citation-key mismatches that couldn't be resolved without checking the source PDFs / external databases. This handoff is the cleanup pass to settle those items before any Pass-2 deep extraction runs (Pass 2 will treat the citation block as authoritative — settling it once, here, prevents per-paper re-litigation later).

## State of play

- 19 extraction stubs landed in [`docs/extractions/`](../extractions/) in commit `2b7dc48`.
- Each follows [`../extractions/_template.md`](../extractions/_template.md) and carries a "Bibliographic anchor" block: `Citation key` / `DOI / URL` / `Pages cited from`.
- Some anchors are filled in from the visible source-file frontmatter; others say `TODO` because the source didn't expose the venue/DOI in its first lines and a deeper check is needed.
- A handful of stubs surface **substantive** flags (author-order mismatch, citation form, identity of the cited artefact) that need a decision, not just a database lookup.

The four UWA lineage extractions (`brown2023.md`, `zhang2023.md`, `ho2024.md`, `tay2024.md`) are out of scope — they were not stubbed in `2b7dc48` and the per-guardrail rule says they're settled.

## The flagged items, by class

### Class A — substantive (decision needed, not just a lookup)

| # | Stub | Flag | Decision needed |
|---|---|---|---|
| A1 | [`sadlek2022.md`](../extractions/sadlek2022.md) | Lit review cites "Sadlek et al." but the source file lists **Čeleda** as first author (Sadlek is second). | (a) Update the lit-review citation to "Čeleda et al."; or (b) keep "Sadlek et al." with a corrected author order; or (c) the cited claim is in a *different* Sadlek-led paper. Check `docs/sources/2_2_sadlek2022current.md` against the lit-review §III-B references to confirm which work the p.3 quote actually comes from. |
| A2 | [`ghosh2009.md`](../extractions/ghosh2009.md) | NITRD source has no clear author attribution — it's a working-group product. Lit review opens with `[1]` — verify whether `[1]` is this NITRD doc, the Jajodia 2011 *Moving Target Defense* book, or another foundational. | Decide whether to cite as institutional (`NITRD CSIA-IWG, 2009`) or attributed (e.g. to Ghosh as working-group lead). Also confirm whether the lit-review `[1]` and this file are the same artefact at all — they may not be. |
| A3 | [`brown2023.md`](../extractions/brown2023.md) (lineage — read-only) | Lit review cites this as **"Brown et al., 2023"** (plural authors). The extraction file and conformance spec treat Brown 2023 as a **single-author** Master's thesis. | Verify whether the lit review is citing a derived paper with co-authors, or whether the "et al." is a citation error. **Do not edit `brown2023.md`** — the resolution lands in the lit review prose or a new derived-paper extraction. |
| A4 | [`attackflow.md`](../extractions/attackflow.md) | Schema-version pinning is an architecture decision, not a bibliographic one — but the citation needs to match whatever schema version the architecture pins. | Confirm the project's pinned Attack Flow schema version (per `project_context.md` decisions log, when authored) and cite that version explicitly. |

### Class B — database lookup (DOI / venue / publication year)

These are filled `TODO` because the source PDFs in `docs/sources/` don't expose the venue or DOI in the first few lines. A web/CrossRef lookup against the title + author resolves each.

| # | Stub | What's needed |
|---|---|---|
| B1 | [`al-sada2024.md`](../extractions/al-sada2024.md) | Venue + DOI. Title: "MITRE ATT&CK: State of the Art and Way Forward." First author Bader Al-Sada, Hamad Bin Khalifa University. |
| B2 | [`masud2025.md`](../extractions/masud2025.md) | DOI confirm. Citation should be `Computers & Security` 153 (2025) art. 104380 per the source-file header — verify and pin the DOI. |
| B3 | [`ferraz2024.md`](../extractions/ferraz2024.md) | Venue + DOI. Title: "The Procedural Semantics Gap in ATT&CK-in-STIX: Measuring Procedural Sufficiency for APT Emulation." Authors at Aeronautics Institute of Technology / CMU. (Conference unspecified in the source frontmatter.) |
| B4 | [`rahman2024.md`](../extractions/rahman2024.md) | Volume / issue / DOI. Source header says "TRANSACTION OF SOFTWARE ENGINEERING" — confirm IEEE TSE and pin volume/issue. |
| B5 | [`jalowski2026.md`](../extractions/jalowski2026.md) | Venue + DOI. Title: "Rethinking the Security Assurances of MTD: A Gap Analysis for Network Defense." Authors mixed independent / Intel. Confirm publication status (preprint vs. published — the 2026 date suggests it may still be in press). |
| B6 | [`he2025.md`](../extractions/he2025.md) | Venue + DOI. Title: "MTD-AD: Moving Target Defense as Adversarial Defense." Authors He, D. D. Kim, M. R. Asghar. |
| B7 | [`kim2026.md`](../extractions/kim2026.md) | DOI confirm. Citation should be `Future Generation Computer Systems` 181 (2026) art. 108419 per the source-file header — verify and pin. Stub guesses `10.1016/j.future.2026.108419`. |

### Class C — already filled, just spot-check

These were filled from the source-file frontmatter; sanity-check before Pass 2 commits cite them.

- [`cho2020.md`](../extractions/cho2020.md) — DOI `10.1109/COMST.2019.2963791`. (IEEE Comms Surveys & Tutorials 2020.)
- [`hong2018.md`](../extractions/hong2018.md) — DOI `10.1016/j.cose.2018.08.003`. (Computers & Security 2018.)
- [`alshamrani2019.md`](../extractions/alshamrani2019.md) — DOI `10.1109/COMST.2019.2891891`. (IEEE Comms Surveys & Tutorials 2019.)
- [`buechel2025.md`](../extractions/buechel2025.md) — USENIX URL filled; no DOI for USENIX Security proceedings.
- [`rodriguez2024.md`](../extractions/rodriguez2024.md) — DOI `10.5753/jisa.2023.3902`. Filename says 2024, DOI says 2023 — the latter is the publication date per the source header. Confirm the citation-key year matches the DOI year (`rodriguez2023`?) or the volume year (`2024`).
- [`zhang2025attackg.md`](../extractions/zhang2025attackg.md) — DOI guessed `10.1016/j.cose.2024.104220`. Verify.
- [`bianco2013.md`](../extractions/bianco2013.md) — blog URL filled. Pair with `sadlek2022.md` for peer-reviewed corroboration per the lit review.
- [`bland2020.md`](../extractions/bland2020.md) — DOI `10.1016/j.cose.2020.101738`. (Computers & Security 2020.)
- [`outkin2023.md`](../extractions/outkin2023.md) — DOI `10.1109/TDSC.2022.3165624`. (IEEE TDSC; published 2022, current 2023.)

## Recommended approach

A single short session, ~30–45 min, with the lit-review PDF and a browser open.

1. **Open the lit-review prose** at [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) and pull the `References` section (will land when Marc pastes the remainder — currently marked `[REMAINDER PENDING]`). The references list is the source of truth for what each `[N]` citation should resolve to. **Block this handoff until the lit-review references section is in the file** — without it, Class A and B resolutions are guesses against the wrong artefact.
2. **Class A first.** Each item needs a decision recorded inline in the stub's Bibliographic-anchor block, with a one-line note in `Open questions / things to verify` noting the resolution path. The A3 (Brown et al. vs. single-author thesis) and A2 (NITRD attribution) decisions also need to be reflected in the lit-review prose if the citation form changes there.
3. **Class B next.** CrossRef or Google Scholar against `<title> <first-author>` resolves each in one lookup. Pin the DOI and venue in the stub's Bibliographic-anchor block.
4. **Class C last.** A quick read-through to catch any year-mismatch / authority issues (the `rodriguez2024` / `rodriguez2023` filename-vs-DOI tension is the obvious one).
5. **Single commit at the end** — `docs(extractions): resolve bibliographic anchors per handoff <date>_bibliographic_anchors.md`. Branch: `feat/lit-review-landing` if still in progress, otherwise spin a `chore/extraction-anchors` branch off main per session_workflow.

### Alternatives considered

- *Defer to Pass 2 (per-paper sessions).* Rejected: would re-open the same lookup 19 times under 19 different cognitive contexts; the citations are a shared artefact, settle them once.
- *Resolve only the Class A items, leave B as `TODO` until Pass 2.* Possible compromise if A1–A4 turn out to be expensive. But B is cheap (~15 min total for all 7) and bundling them keeps the dissertation bibliography one file diff away rather than twenty.

## Validation gate

- Zero `TODO` markers remain in any `## Bibliographic anchor` block in `docs/extractions/`. (`rg 'TODO' docs/extractions/*.md | grep -i 'doi\|venue\|citation'` returns nothing.)
- Each Class-A item has a resolution recorded inline (the decision, not the question).
- For any A-item that required changing the lit-review citation form (A1, A3 most likely), the lit-review file at `docs/sources/LIT_REVIEW.md` is updated in the same session.
- One commit on the chosen branch, no push.

## Hard constraints

- **Lineage four are read-only.** `brown2023.md` / `zhang2023.md` / `ho2024.md` / `tay2024.md` extractions don't get edited even when the lit-review citation references them. A3 lands in the lit review prose (or in a new derived-paper extraction if Brown 2023 *also* exists as a co-authored conference paper), not by editing `brown2023.md`.
- **Don't fabricate DOIs.** If a CrossRef lookup turns up nothing, leave the DOI line as `TODO — could not resolve; pending lookup` rather than guess. Preprints in particular often have no DOI.
- **Don't assert a paper is wrong.** Per [`../specs/guardrails.md`](../specs/guardrails.md): if a flagged item resists resolution, mark it for Marc, don't decide it unilaterally.
- **Branch / commit / no push** per [`../specs/session_workflow.md`](../specs/session_workflow.md). One commit, descriptive message naming the handoff that closed.
- **`docs/sources/` is gitignored** — any edits to `LIT_REVIEW.md` are local-only and won't appear in `git status` of the eventual commit.

## Reading list

- This handoff (you're reading it).
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) — the lit-review prose, esp. the References section *(blocked: must be pasted in first per the "[REMAINDER PENDING]" marker)*.
- [`../extractions/_template.md`](../extractions/_template.md) — the Bibliographic-anchor block format.
- [`../specs/guardrails.md`](../specs/guardrails.md) — "don't assert any paper is wrong; flag for Marc."
- The 19 extraction stubs themselves (single-file Read each; ~30 lines apiece).

## Out of scope (explicitly)

- Deep extraction of any paper. This handoff stops at the bibliographic anchor; the `Relevant artefacts` sections stay as `TODO — Pass 2`.
- Editing the four UWA lineage extractions.
- Editing `mtdsim_spec.md`, `metrics_semantics.md`, `provenance.md`.
- Resolving any TODOs in extraction `Open questions` sections that *aren't* about citation form / DOI / venue / first-author identity — those are Pass-2 work.
- Pushing the branch.
