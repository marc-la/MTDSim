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

### TODO — Pass 2

(awaiting Pass-2 deep extraction)

Sections to lift in Pass 2:
- The GPLADD framework — generalised PLADD with explicit attack-step durations.
- The use of MITRE ATT&CK Evaluations APT3 data as input — a model of how ATT&CK data flows into a defender-evaluation pipeline; contrast with this dissertation's L0→L1→L2 pipeline.
- The "physics of attacks" framing — time-as-physical-constraint argument.
- The return-on-detection-investment evaluation — relate to MTD's RoA / attack-cost metrics.

---

## Open questions / things to verify

- Whether Outkin's attacker model places at procedural or behavioural on the lit review's fidelity descriptor — likely procedural (Markov-chain over ATT&CK steps) but worth confirming in Pass 2.
- This paper is game-theoretic and Marc has explicitly de-emphasised game-theoretic framings in the project; verify the citation is for contrast / methodological precedent rather than methodological inheritance.

## Out of scope for this thesis

- The full game-theoretic apparatus — out of scope per project direction.
