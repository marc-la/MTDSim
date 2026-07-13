# Outkin 2023 — extraction notes

> A. V. Outkin, P. V. Schulz, T. Schulz, T. D. Tarman, A. Pinar. "Defender Policy Evaluation and Resource Allocation With MITRE ATT&CK Evaluations Data." *IEEE Transactions on Dependable and Secure Computing*, vol. published 18 Apr 2022; current version 13 May 2023. Sandia National Laboratories SAND2022-3936 J.
> Source file: `docs/sources/4_outkin2023defender.md` (gitignored).
> Relevance to this thesis: cross-cutting reference for §V — game-theoretic GPLADD approach using MITRE ATT&CK Evaluations data; demonstrates evaluating defender strategies against ATT&CK-derived attack data (in their case APT3) with explicit attack-step durations and a discrete-time Markov-chain solver. A precedent for grounding defender evaluation in ATT&CK-derived adversaries; useful contrast for the dissertation's behaviourally-grounded but non-game-theoretic stance.

## Bibliographic anchor

- **Citation key**: `outkin2023`
- **DOI / URL**: 10.1109/TDSC.2022.3165624
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

## Relevant artefacts

### Relevance class

**C — Contrast / adjacent.** Outkin et al. is cited in §V Synthesis (`LIT_REVIEW.md:217`, `:223`) as the published precedent for *grounding attacker per-step parameters in real MITRE ATT&CK Evaluations data*, contrasted against the surveyed MTD evaluations' CVSS-derived heuristics. The §V role is parameter-grounding precedent, not methodological inheritance: this dissertation's L0→L4 pipeline (architecture §(c)–(g)) varies attacker *behavioural fidelity* on a frozen defender, whereas Outkin varies *defender capability* against a frozen ATT&CK-derived attacker. Both ingest ATT&CK; both target MTD/defence evaluation; the differing axis-of-variation and the differing position on the Pyramid-of-Pain fidelity descriptor make this a contrast boundary the lit review explicitly draws.

### Used in lit review

- [`../sources/LIT_REVIEW.md:217`](../sources/LIT_REVIEW.md) — §V Synthesis, second-strand anchor: *"Outkin et al. [21] address the parameters: they fit an attacker's per-step detection probabilities to real MITRE ATT&CK Evaluations data, where the surveyed models derive theirs from CVSS."* Outkin closes the "where do the numbers come from" half of the §V apparatus pitch.
- [`../sources/LIT_REVIEW.md:223`](../sources/LIT_REVIEW.md) — §V-A Approach, restating the precedent: *"a Bland-style agent enacts it, parameterised against engagement data after Outkin et al."* The cite carries the *parameter-grounding* mechanism into this thesis's approach statement.

### ATT&CK-Evaluations-grounded transition-probability inference (the contrast pipeline)

**Source locator:** §3.5 (Markov chain transition probabilities inference); §5.2 (MITRE ATT&CK Evaluations Analysis); §5.2.1 (Detection probabilities); Table 4 (per-defender per-step detection probabilities); Fig. 2 (the 9-step notional APT3 attack graph); §1 (contributions list — sixth and seventh bullets name the ATT&CK-Evaluations-to-GPLADD mapping). The source markdown carries no page numbers; locators are by section/figure/table.

**Paraphrase:** The pipeline takes a *fixed* ATT&CK-derived attack graph (the 9-step "notional APT3" chain: Start → Email → Link → Exec → IPEW → Msg → MvEW → RTU → Ready) and a *fixed* attacker, and varies the defender. ATT&CK Evaluations APT3 data — vendor-by-vendor detection observations across three detection categories (IOC / Specific Alert / General Alert) — is folded into three defender capability levels (B0 / B1 / B2 distinguished by ambiguity-tolerance) crossed with two attack-chain variants, yielding six "Evaluations" (B10..B22). For each Evaluation, per-step detection probabilities are computed as the ceiling of sub-step detection fractions over twelve participating vendors (§5.2.1); these populate a Markov transition matrix (Equation 3 / Table 5) whose steady-state distribution and first-passage-time-to-Ready distribution constitute the attack-success metrics (§5.2.2). Defender comparison reduces to comparison of steady-state mass on the "Ready" state and the shape of the time-to-success distribution across B0/B1/B2. The pipeline shape — ATT&CK Evaluations data → per-step detection probabilities → transition matrix → Markov-chain metrics — is the published precedent §V cites for parameter-grounding.

**Quote (essential — establishes the data-flow contrast):**
> "In this new work, we leveraged Evaluations data to approximate probabilities of detection to inform the Markov chain simulations of GPLADD models. We effectively associate an attack step with a technique (e.g., gain persistence). This allows hot-swapping techniques for a given tactic to understand the uncertainty associated with options available to the attacker." (§5.2.1)

**Maps to:**
- [`../specs/architecture.md`](../specs/architecture.md) §(c)–(g) (L0→L4 pipeline) — the contrast boundary. This dissertation's pipeline ingests ATT&CK at L0 as Attack-Flow-curated CTI and propagates *behavioural* structure forward (L1 GAP → L2 GASP → L3 OGASP traversal); Outkin ingests ATT&CK Evaluations as per-step *detection-probability* parameters against a fixed attack graph. Different L0 channel out of ATT&CK (Evaluations vendor-vs-technique results vs Attack Flow analyst-curated technique-sequence flows), different downstream commitment (parameter table vs traversable graph), different agent-side variation (defender capability vs attacker behavioural model).
- [`../specs/architecture.md`](../specs/architecture.md) §(j) methodological positioning — the spec's own caveat that *MITRE ATT&CK Evaluations gives EDR-style ground truth, not MTD-specific ground truth* applies directly to the Outkin pipeline: its detection probabilities are EDR-vendor outputs, defensible for EDR-defender evaluation but not transferable to SDR-family MTD without a calibration step that does not exist in the public record. This is *why* §V cites Outkin for the apparatus shape (the data-flow precedent) rather than for the numbers themselves.
- [`../sources/LIT_REVIEW.md:217`](../sources/LIT_REVIEW.md), [`../sources/LIT_REVIEW.md:223`](../sources/LIT_REVIEW.md) — the §V Synthesis claim Outkin anchors.

**Disposition for this thesis:** **contrasted-against.** The data-flow shape (ATT&CK → per-step parameters → metric) is the precedent the §V Synthesis invokes; the pipeline itself is not inherited. Three contrast axes:

1. *Axis of variation.* Outkin holds the attacker fixed at a 9-step linear chain and varies defender capability; this dissertation holds the defender at SDR/AI-selection baseline and varies attacker behavioural model across CTI-derived profiles ([`../specs/architecture.md`](../specs/architecture.md) §(a), §(j)).
2. *Position on the Pyramid-of-Pain fidelity descriptor.* Outkin's attacker is parametric on the lit-review descriptor — per-step detection probabilities are parameters drawn at design time from a probability distribution (§3.5); the attacker has no runtime decision logic beyond Markov-chain progression. The dissertation's contribution targets the procedural and behavioural rungs the cross-section ([[brown2023]], [[tay2024]], [[masud2025]], [[he2025]], [[kim2026]] per `LIT_REVIEW.md` §IV-B) was found not to reach.
3. *ATT&CK ingestion channel.* Outkin uses ATT&CK Evaluations — EDR-vendor performance data against APT3 emulation; the dissertation uses Attack Flow — analyst-curated technique-sequence flows over publicly-reported incidents ([[attackflow]] per `LIT_REVIEW.md` §III-A, §III-D). The two channels expose different facets of ATT&CK and license different downstream claims: Outkin's licenses cross-defender comparison against a fixed attacker; the dissertation's licenses cross-profile attacker comparison against a fixed defender pool.

The §V wording is precise about what transfers: *parameter-grounding-against-engagement-data as a methodological move*, not the GPLADD apparatus, not the game-theoretic frame, not the Markov-chain solver. The dissertation's own parameter grounding is left to the operationalisation seam at L3 ([`../specs/architecture.md`](../specs/architecture.md) §(f)) and is not committed to ATT&CK Evaluations as the parameter source.

---

## Open questions / things to verify

- Outkin's attacker placement on the fidelity descriptor: **parametric**. The Markov-chain transition matrix is populated at design time from time-to-success distributions and detection probabilities (§3.5); the attacker has no runtime decision-making beyond the stochastic transition — *"we therefore can treat a success condition ci as achieved or not achieved"* (§3.4). The Markov-chain mechanism is procedural over *states*, but the *attacker model* is parametric on the lit-review descriptor (per-step decisions are not encoded; only success-or-not-this-tick is, drawn from a parameter table). Resolved in this extraction; no further verification needed.
- Whether the §V citation could be misread as endorsing the game-theoretic frame Marc has de-emphasised. Resolved: §V wording (`LIT_REVIEW.md:217`) carves the *parameter-grounding* mechanism out and leaves the game-theoretic apparatus aside; no rewording action needed here. The extraction's "contrasted-against" disposition makes this scoping explicit.
- Whether the Outkin pipeline's *detection-probability* parameter table can in principle be repurposed as MTD-evaluation input, given the architecture §(j) caveat that ATT&CK Evaluations is EDR-flavoured ground truth, not MTD-flavoured. Noted as a known caveat; no further action — Outkin is cited for the *apparatus shape*, not for the numbers, so the EDR-vs-MTD calibration gap is the contrast boundary, not a defect to be repaired.

## Out of scope for this thesis

- The full game-theoretic apparatus — out of scope per project direction.
