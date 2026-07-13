---
status: durable
chapter: ch3_design
created: 2026-05-28
updated: 2026-07-13
lineage: 2026-05-28_cti_ages_critique.md
---

# Threat intelligence ages — but the useful frame is taxonomy drift, not staleness

## Position in the dissertation

A methodology-chapter defence (with a tail in the discussion chapter's limitations): why building the attacker model from a *pinned snapshot* of a threat-intelligence corpus is a legitimate research choice, and how the dissertation's claims are scoped so that "your data is stale" has no purchase.

## The idea

An intuition worth taking seriously says that cyber threat intelligence "ages, becomes stale, and always needs updating". The intuition packages four distinct properties with different half-lives, different mitigations, and different consequences for what this thesis may claim; conflating them produces either over-engineering (rebuild the corpus every six months) or under-engineering (the corpus is fine forever). Unpacked:

**Taxonomy drift — real, and mitigated by version pinning on both sides.** The *encoding language* of threat intelligence evolves: MITRE ATT&CK adds tactics, renames them, and deprecates or merges techniques (most recently splitting the former Defense Evasion tactic into Stealth and Defense Impairment, v19, 2026). The corpus artefacts here therefore pin their ATT&CK version explicitly and derive their vocabulary from the pinned bundle rather than from any hard-coded table. Crucially the drift is two-sided: the artefact can lag upstream (mitigation: re-pin and rebuild), and the *reader* can lag the artefact — a reader carrying the classic fourteen-tactic mental model will misread a correctly-pinned fifteen-tactic artefact as anomalous. An episode of exactly this shape occurred during the project: an audit was nearly commissioned to "reconcile legacy tactic labels" that were in fact current, three weeks after the pin had updated. The mitigation is to surface the version field at a glance, so the reader notices when *they* have drifted.

**Incident historicity — does not age.** That a 2017 campaign unfolded the way it did is permanent historical truth; a reader in 2026 learns the same thing a 2017 reader did. Old incident reports are not wrong, merely *about older events*. Historical incident corpora are archival data, not forecasts, and need no refresh.

**Operational relevance — decays, but this is a scoping question, not a data-maintenance one.** What worked for attackers in 2017 may not work today; an old report is correct about its time without predicting the present. The mitigation is to scope claims explicitly — "this analysis characterises documented incident patterns from the corpus's window", never "this predicts next year's attacker behaviour". Technique-level operational detail decays over a few years; the high-level patterns this thesis actually leans on (data theft as an objective; the phase structure of campaigns) decay over decades.

**Coverage — does not degrade, and does not grow by itself.** A corpus snapshotted at time T covers what was reported by T. Later, its *fraction* of the world's incidents has shrunk, but the corpus itself has not degraded — the most frequently confused case. Extension matters only if the dissertation's claims require current-day coverage, which they do not: the architectural contribution (the intelligence-to-simulator pipeline) and the methodological one (does objective partitioning discriminate?) are properties of the method, not of 2026 operations.

**What "always needs updating" gets wrong.** The phrase implies a living artefact under continuous maintenance. For research, a snapshot pinned to a stated corpus version, a stated taxonomy version, and a stated build date is *more* defensible than a rolling artefact: it is reproducible, and continuous rebuilding sacrifices reproducibility for an illusion of currency while imposing a Sisyphean maintenance burden that competes with the actual contribution. The metaphor that survives: threat intelligence is not milk but a topographic map — the question is never "how old is it?" but "have the cliffs moved enough to mislead?". For this corpus, the only cliff that has moved is MITRE's tactic vocabulary, which pinning addresses once.

The weaker claim that survives critique, and that the dissertation adopts: **intelligence encoded in a versioned taxonomy needs its taxonomy version pinned, or downstream comparison against newer versions produces spurious anomalies** — and the dissertation's scoping language is tightened accordingly ("the documented attacker behaviour in the corpus, 2017–2024, encoded against ATT&CK Enterprise v19.1"), heading off staleness objections by scoping rather than refreshing.

## Evidence and repo anchors

- The three version pins the graph carries (`corpus_ref`, `attack_source`, `build_date`): [`../../implementation/pipeline/gap/gap_schema.md`](../../implementation/pipeline/gap/gap_schema.md) §(d).
- The drift audit run when the reader-side episode was resolved: 124/124 parent technique IDs active against v19.1; three revoked sub-techniques all collapse to active parents, leaving the aggregate graph unaffected (recorded in this note's lineage version, git history).
- The snapshot-vs-stream assumption at architecture level: [`../../implementation/architecture.md`](../../implementation/architecture.md).
- The v19.1 tactic split's research consequence (allocating pre-split literature between Stealth and Defense Impairment): [`tactic_profiles/README.md`](tactic_profiles/README.md).

## Revisit conditions

- If ATT&CK restructures fundamentally (a paradigm shift rather than renames), pin-and-document becomes insufficient and the analysis re-derives under the new structure.
- If the dissertation's claims ever expand to *predictive* statements about post-corpus attacker behaviour, the operational-relevance case stops being scopeable and demands actual corpus extension.
- If the upstream corpus project is deprecated or re-schemed, the corpus pin becomes a compatibility burden rather than a clean reference.
