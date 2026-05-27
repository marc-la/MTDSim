---
status: open
created: 2026-05-27
---

# Pass-2 deep extraction across the 19 paper stubs (batched, parallel)

Each of the 19 Pass-1 extraction stubs in [`docs/extractions/`](../extractions/) carries a `### TODO — Pass 2` placeholder where the deep artefact extraction should live. This handoff fleshes them out, using parallel subagents (one paper per agent) batched by relevance class. Output: each stub's `Relevant artefacts` section replaced with concrete extractions — quotes, paraphrases, locators, spec/methodology cross-links, and a per-paper disposition — calibrated against the dissertation's methodology direction so that low-relevance papers stay short and high-relevance papers get the careful treatment they need.

The bibliographic-anchor pass (commits `56c7a02` → `c741815`) settled citation form, DOI, venue, and citation-key year for every stub in scope. Pass 2 inherits a clean citation layer and does not re-litigate it.

## State of play

- 19 extraction stubs at [`docs/extractions/`](../extractions/) (excluding lineage four — `brown2023.md`, `zhang2023.md`, `ho2024.md`, `tay2024.md` — which are read-only per the existing guardrail).
- Each stub's `## Bibliographic anchor` block is fully resolved as of `c741815`.
- Each stub's `## Relevant artefacts` section currently contains a `### TODO — Pass 2` placeholder with a 2–5 bullet "Sections to lift in Pass 2" hint already authored at stub-creation time. **These hints are the starting scope per paper** — agents do not need to discover what to extract from scratch.
- Architecture spec [`../specs/architecture.md`](../specs/architecture.md) §(j) methodological positioning is currently a two-paragraph scaffold; §(l) open architectural questions still has six unresolved items. Both fall under the *separate* architecture-prepopulation handoff's Pass 2 — out of scope here.
- Lit review at [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) is still truncated at line 191 (`[REMAINDER PENDING]`). For §IV-B papers (Tay, Masud, He, Kim) the Table II rating + per-paper discussion is essential to extract "how the paper is used in the lit review" — this is the hard pre-condition below.

## Pre-conditions before kickoff

1. **Lit-review §IV-B continuation + Table II + §V Synthesis pasted in.** The References list is no longer needed (anchors are resolved). Without §IV-B tail, agents for Tay/Masud/He/Kim are extracting against an incomplete picture of how the paper is used in the prose.
2. **Working methodology direction confirmed.** Default: agents calibrate against architecture §(c)–(g) (L0→L4 pipeline) + the existing §(j) two-paragraph scaffold, as the working methodology. §(j) does not need to be fully fleshed first — Pass 2 of paper extractions and Pass 2 of §(j) bootstrap each other. The trade-off: when §(j) firms up later, only the *relevance dispositions* need a quick re-check, not the artefact extractions themselves.
3. **Branch.** Cut `chore/pass2-extractions` off `main`. Single branch for the whole handoff; commit cadence below.

If pre-condition (1) is not met when the session opens, restrict the batch to non-§IV-B papers (15 papers minus Tay/Masud/He/Kim = 11 papers; Tay is lineage so already excluded → 14 in batch, 4 deferred).

## The batch design

One subagent per paper. Subagents fire in parallel within each batch; batches fire sequentially (so the parent context doesn't melt under 19 concurrent agents). Each agent's prompt is fully scoped — paper source, lit-review citation locator(s), methodology direction summary, relevance hypothesis, output spec, hard constraints. Agents do not see each other's context.

**Cross-attribution guardrail interpretation.** [`../specs/guardrails.md:17`](../specs/guardrails.md#L17) reads "extract one paper per pass before merging" — parallel subagents satisfy the spirit (each agent's *pass* is one paper, in isolation) without satisfying a literal "one session" reading. The risk the guardrail addresses is cross-attribution within a single working thread; parallel-isolated agents have no shared context to leak across. Acceptable here. Backstopped by the validation gate below.

### Batches by relevance hypothesis

The starting hypothesis below is *not gospel* — agents validate / adjust per paper and declare a final class in their extraction. The hypothesis exists so each agent's prompt can be calibrated (extraction depth, quote budget, disposition framing).

**Relevance classes** (each Pass-2 extraction declares one):

- **L — Load-bearing on methodology.** Directly informs an architectural or methodological decision (e.g., a metric definition, a substrate primitive, a framing the L0→L4 pipeline inherits). Full extraction: 2–5 artefact sections, multiple quotes/paraphrases with locators, spec cross-links.
- **S — Supporting-argument.** Anchors a claim in the lit review but doesn't drive a methodology choice (e.g., naming the attacker-modelling gap; corroborating the Pyramid-of-Pain ordering). Short extraction: 1–2 artefact sections, one quote at most, disposition focused on what the paper *establishes* rhetorically.
- **C — Contrast / adjacent.** Cited to show what this thesis explicitly does *not* do (e.g., Caldera as Ferraz's substrate vs MTDSim here). One artefact section, disposition focused on the contrast boundary.
- **M — Mentioned-only.** Paper appears in citations but doesn't shape any specific extraction. Single disposition line, no artefact section. **Rare in this corpus** — if a paper earned its way into a stub, it probably isn't class M; default to S if uncertain.

**Batch 1 — Load-bearing on methodology (hypothesis: L)** [~6 papers]
- `cho2020.md` — metrics partition (Table I); attacker-model characteristics (Cho's four traits)
- `hong2018.md` — network-state-dynamic metrics (APV / APN / APE)
- `bianco2013.md` — Pyramid of Pain (foundational to §IV-B fidelity descriptor)
- `attackflow.md` — substrate primitives the L1/L2 build pipeline consumes
- `rodriguez2024.md` — process-mining exemplar; framing of attacker objectives / motivations / knowledge that L2 GASP encodes
- `ferraz2024.md` (citation key now `ferraz2025`) — procedural-semantics-gap framing (closest paper to this dissertation's own framing per the Pass-1 stub)

**Batch 2 — Supporting-argument (hypothesis: S)** [~7 papers]
- `sadlek2022.md` — peer-reviewed corroboration of PoP ordering
- `ghosh2009.md` (citation key now `nitrd2009`) — foundational MTD framing
- `al-sada2024.md` — ATT&CK vocabulary establishment
- `alshamrani2019.md` — APT class characterisation
- `jalowski2026.md` — naming-the-gap survey (2026, 6 years on from Cho 2020)
- `buechel2025.md` — SoK on TTP-extraction quality (bounds what L1 automation can achieve)
- `rahman2024.md` (citation key now `rahman2025`) — ChronoCTI exemplar (NLP-based extraction)

**Batch 3 — Cross-section / contrast / less-mapped** [~6 papers]
- `masud2025.md` — §IV-B cross-section point (Hybrid IoT MTD)
- `he2025.md` — §IV-B cross-section point (ML NIDS adversarial defence)
- `kim2026.md` — §IV-B cross-section point (CKC-aware MTD)
- `zhang2025attackg.md` — AttacKG+ as LLM-based extraction pipeline (relates to §III-D)
- `bland2020.md` — relevance to methodology TBD; agent validates hypothesis (likely S or C)
- `outkin2023.md` — relevance to methodology TBD; agent validates hypothesis (likely S or C)

Batches 1 → 2 → 3 sequentially. Within each batch, all agents in parallel.

## Output spec per extraction

For each stub, the agent replaces the `### TODO — Pass 2` placeholder with:

1. **`### Relevance class`** — one of L / S / C / M, with a one-sentence justification linking to a specific architecture section or lit-review claim.
2. **`### Relevant artefacts`** — N concept sections per the existing [`_template.md`](../extractions/_template.md), where N is governed by the relevance class:
   - L: 2–5 sections
   - S: 1–2 sections
   - C: 1 section
   - M: zero sections (skip to disposition)
   Each section has: **Source locator** (§ / page), **Paraphrase**, **Quote** (if essential, short, with locator), **Maps to** (spec row or methodology section), **Disposition** (verified / divergent / unimplemented / adopted-as-baseline / contrasted-against — and why).
3. **`### Used in lit review`** — exact `LIT_REVIEW.md` line locator(s) where this paper is cited, and a one-line gloss of the claim each citation anchors.
4. **`## Open questions / things to verify`** — refined; carry forward only items that genuinely remain. Resolve where possible inline.

The existing `## Bibliographic anchor`, top-of-file blockquote, and `## Out of scope` sections are not in scope for editing — Pass 1 + the anchor cleanup pass settled them.

## Hard constraints

- **Lineage four are read-only.** `brown2023.md` / `zhang2023.md` / `ho2024.md` / `tay2024.md` are not in this batch. Per the existing guardrail.
- **No cross-attribution.** Each agent quotes / paraphrases *only* from its assigned source file. If an agent needs to compare against another paper, it cites the other paper by `[[citation-key]]` link to the extraction stub — it does not quote the other paper directly.
- **Quote sparingly.** Per the template's extraction policy. Paraphrase liberally. Fair-use boundary: short verbatim quote only when the exact phrasing matters; otherwise paraphrase with locator.
- **Don't assert a paper is wrong.** Per guardrails. If a paper's claim conflicts with the dissertation's methodology, mark `contrasted-against` and explain — don't say the paper is mistaken.
- **Don't fabricate locators.** § / page numbers must come from the source file. If the source markdown doesn't expose page numbers (markdown-extracted PDFs often don't), use § / heading instead and note the format.
- **Don't pollute the relevance.** A class-M paper gets a one-line disposition and no artefact section. A class-S paper gets 1–2 sections, not 5. **Tangential papers ballooning into multi-section extractions is the failure mode this handoff exists to prevent.**
- **Australian English.**
- **Don't push, don't commit from inside the agent** — the parent process commits per the cadence below.

## Commit cadence

**Default**: one commit per batch (so 3 commits total), each titled `docs(extractions): Pass-2 deep extraction batch <N>/3 — <relevance-class>`. Rationale: one diff per relevance-class batch is reviewable in one sitting (~6 stubs × ~50 lines each = ~300-line diff per commit). Easier than 19 micro-commits, smaller than one monolithic 1000-line commit.

**Alternative** (Marc-decision at session start): one commit per paper, if Marc wants finer-grained review history.

## Validation gate

- Every Pass-1 stub's `### TODO — Pass 2` placeholder is replaced (zero remaining): `rg '### TODO — Pass 2' docs/extractions/*.md` returns nothing.
- Every Pass-2 extraction declares a `### Relevance class` and a `### Used in lit review` block.
- **Cross-attribution check.** For each stub, every quote (`>` line) traces to a §/page in the *same* paper's source markdown. Spot-check with: `for f in docs/extractions/*.md; do echo "== $f =="; grep -n '^>' "$f"; done` and visual audit.
- No `mtdsim_spec.md`, `metrics_semantics.md`, or `provenance.md` edits unless an extraction surfaces a genuine spec gap — in which case **flag, don't edit** (separate handoff).
- One commit per batch (or per paper per the alternative), on `chore/pass2-extractions`. No push.

## Out of scope (explicitly)

- Editing the four lineage extraction stubs.
- Editing the lit review prose (only the §IV-B-tail paste-in is needed, by Marc, before kickoff).
- Editing `mtdsim_spec.md`, `metrics_semantics.md`, `provenance.md`, or `project_context.md`.
- Resolving architecture §(j) methodological positioning (separate handoff: architecture-prepopulation Pass 2).
- Resolving architecture §(l) open architectural questions (same).
- Adding new extraction stubs for papers not already in `docs/extractions/`.
- Pushing the branch.

## Knock-on to the architecture-prepopulation handoff

Once this handoff ships, the architecture-prepopulation handoff's "Pass 2 still owes" list reduces from three items to two:
- ~~Adjacent-paper extraction stubs deep extraction~~ → shipped by this handoff.
- §(j) methodological positioning flesh-out — remains.
- §(l) open architectural questions — remains.

Add a one-line cross-reference to the architecture-prepopulation handoff when closing this one.

## Reading list

- This handoff.
- [`../extractions/_template.md`](../extractions/_template.md) — the artefact-section format.
- [`../specs/architecture.md`](../specs/architecture.md) §(a)–(g), §(j), §(k) — the methodology direction agents calibrate against.
- [`../specs/guardrails.md`](../specs/guardrails.md) — esp. the "one paper per pass" and "don't assert any paper is wrong" lines.
- [`../specs/mtdsim_spec.md`](../specs/mtdsim_spec.md), [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) — for the `Maps to:` cross-links in extractions.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) — for the `Used in lit review` blocks.
- Per-paper source markdown at `../sources/<N_x_>...md`.
- The 19 in-scope extraction stubs themselves.
