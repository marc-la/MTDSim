# Rodríguez 2024 — extraction notes

> M. Rodríguez, G. Betarte, D. Calegari. "A process mining-based method for attacker profiling using the MITRE ATT&CK taxonomy." *Journal of Internet Services and Applications*, vol. 15, no. 1, 2024. doi:10.5753/jisa.2023.3902.
> Source file: `docs/sources/2_4_rodriguez2024process.md` (gitignored).
> Relevance to this thesis: the process-mining exemplar in lit review §III-D (the [7] citation) — recovers attacker process structure (Petri nets) from labelled runtime event logs, shifting the manual cost from narrative curation to authoring/maintaining technique-labelling rules.

## Bibliographic anchor

- **Citation key**: `rodriguez2024`
- **DOI / URL**: 10.5753/jisa.2023.3902
- **Pages cited from**: full text

## Extraction policy

Quote sparingly, paraphrase liberally. Each excerpt below sits under copyright fair use:
- **Quoted material**: kept in `>` blockquote with explicit section / page locator.
- **Paraphrase**: prose that summarises rather than reproduces — preferred for everything that can be paraphrased without losing technical precision.
- **Cross-link**: every extract that maps to a spec row or note carries a `→ [`...`]` link.

### Relevance class

**L — Load-bearing on methodology.** Cited as the process-mining exemplar in lit review §III-D and supplies the attacker-trait framing the L2 GASP layer encodes (architecture §(e)); also the named methodological precedent against which architecture §(j) draws its four-axes contrast — so the disposition here directly backs §(j) and retires the docs-audit "Rodríguez four-axes" finding.

## Relevant artefacts

### Concept 1 — The four-stage process-mining pipeline (Enactment → Extraction → Discovery → Analysis)

**Source locator:** §3 ("A method for attacker profiling"), pp. — / lines 95–202 of source markdown (PDF page numbers not preserved by extraction); summarised in Figure 1 on §3.

**Paraphrase:** The paper proposes a four-stage method that follows the standard PM methodology. *Enactment* executes attack strategies inside the target system (e.g., a honeypot or an isolated lab). *Extraction* gathers low-level system events (Sysmon on Windows; `auditd` / Snoopy on Linux), pushes them through a labelling tool (Zircolite running SIGMA rules) that tags each event with the corresponding MITRE ATT&CK tactic, and builds a CSV event log with case-ID, activity, and timestamp columns. *Discovery* feeds the event log to a process-discovery algorithm — specifically the *Inductive Miner (IMf)* implemented in the ProM tool — to produce a Petri-net / process-tree model whose nodes are ATT&CK tactics. *Analysis* interprets the discovered model qualitatively (with expert input), with fitness and precision used to compare a given trace to the discovered model.

**Quote (if essential):**
> "Our current research proposes a four-stage method that employs PM to uncover process models of observed attack strategies. […] To increase the level of abstraction for attacker profiling, we use the MITRE ATT&CK framework to semantically lift events." (§1, source line 31)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(j) (methodological positioning — the published precedent the §(j) four-axes contrast is drawn against); [`../specs/architecture.md`](../specs/architecture.md) §(e) L2 GASP (the *input class* and *temporal stance* axes are the structural difference).

**Disposition for this thesis:** **contrasted-against.** This thesis takes the opposite temporal stance: it constructs an a-priori behavioural profile from curated CTI (Attack Flow + ATT&CK group descriptions, the L0→L1 GAP build) and traverses it during simulation (L3 OGASP). Rodríguez's pipeline is post-hoc — it discovers a model from telemetry already produced by a running attack. The two pipelines are complementary, not competing, and the §(j) "four-axes" formulation makes that explicit; see Concept 4 below.

---

### Concept 2 — Attacker-trait framing: "objectives, knowledge, and modus operandi"

**Source locator:** §7 ("Discussion"), source line 695. The abstract uses adjacent phrasing — "cyber adversaries' capabilities, intentions, and behaviors" (source line 11).

**Paraphrase:** The discussion opens by asserting that an attacker's *objectives, knowledge, and modus operandi* together dictate which tactics and techniques are used and the order in which they are applied — the framing that motivates process-mining as the right tool for recovering that ordered behaviour. The abstract's "capabilities, intentions, and behaviors" formulation lands on the same three-axis idea from a different angle.

**Quote (if essential):**
> "The attacker's objectives, knowledge, and modus operandi significantly impact a cyber attack, dictating the tactics and techniques used and the order in which they are applied." (§7, source line 695)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(e) L2 GASP (the *motivation specifier* is the architectural surface that encodes this trait-axis framing; the "objectives / knowledge / modus operandi" triple back-stops the more general L2 design intent that subgraphs differ in *non-trivial ways* across motivation specifiers); [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §III-D line 131.

**Disposition for this thesis:** **adopted-as-baseline (with flagged paraphrase mismatch).** The thesis adopts the framing that adversaries are characterised along these axes, and L2 GASP operationalises one of them (motivation, via the terminal-node-ancestor proxy of §(e)). **Concern:** the lit review's §III-D opening sentence at [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md):131 attributes "objectives, **motivations**, and knowledge" to [7], whereas Rodríguez's text at source line 695 reads "objectives, knowledge, and **modus operandi**". The lit-review formulation appears to be a paraphrastic substitution — *motivations* in place of *modus operandi* — that makes the trait set align more cleanly with the project's L2 GASP "motivation specifier" vocabulary. This is a reasonable paraphrase of an attacker-trait set in *spirit* (an attacker's choice of techniques is shaped by what they want, what they know, and how they prefer to operate), but the exact wording is not from Rodríguez. See Concern 1 in `## Open questions` below.

---

### Concept 3 — The labelling-rule layer (Zircolite + SIGMA) shifts manual cost from narrative curation to rule authoring

**Source locator:** §3.1.2 "Labeling of events" (source lines 125–135); §4.2.2 (source lines 229–293); §7.2 "Event classification" (source lines 705–713).

**Paraphrase:** Process mining over raw system telemetry only yields ATT&CK-level behaviour because of the labelling step: each low-level Sysmon event is matched against a corpus of SIGMA detection rules (via the Zircolite engine), and each matched rule contributes an ATT&CK-tactic tag to the event. The rule corpus is community-maintained but informal — SIGMA does not *require* a tactic/technique tag, so rule authors omit it freely, and rules sometimes match in ways that are technicality-sensitive (the paper notes a missed-detection where `arp -a` had a double-space and the SIGMA rule required a single space). The paper concludes that the soundness of the discovered model is bounded by the soundness of the labelling rule set, and that maintaining this rule set — including hand-filling missing tactic tags — is the manual cost the pipeline shifts to.

**Quote (if essential):**
> "Our results are limited by how the tactics are associated with ATT&CK. The labeling process relies on how the techniques are connected to each of the rules used during the extraction phase and the formality of the mapping process." (§7.2, source line 713)

**Maps to:** [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) §III-D line 137 ("the manual cost shifts from narrative curation to authoring and maintaining the technique-labelling rules") — this is the lit-review claim Rodríguez most directly anchors.

**Disposition for this thesis:** **contrasted-against.** This thesis does not need a labelling rule corpus: its L1 GAP pipeline consumes already-structured ATT&CK technique IDs from Attack Flow records and group descriptions. The manual cost in MTDSim is at the CTI-curation layer (selection / scoping of Attack Flow corpus + group descriptions), not at the rule-authoring layer. Recording this contrast precisely is what allows the §(j) "input class" axis to be defended.

---

### Concept 4 — Petri-net / process-tree output is interpretive, not executable

**Source locator:** §3.2 "Discovery" (source lines 177–189); §4.3 (source lines 302–340); §4.4.2 "Model analysis" (source lines 408–423); §8 "Conclusion and future work" (source lines 746–758).

**Paraphrase:** The discovery step's output is a process model rendered in a process-modelling language (Petri-net, BPMN, or process-tree) and read in the ProM GUI. It is used for two downstream purposes only: (1) qualitative expert interpretation — describing the attacker's *modus operandi* in tactical terms — and (2) conformance / deviation checking via fitness and precision metrics, used to score whether a given event-log trace conforms to the discovered model. The paper does not propose running the model as an attacker simulator and explicitly frames the work as supporting "defense teams to identify the characteristics of attacker actions" (§8). Future work mentioned includes generating Attack Flow-format models for sharing (§8) but not executable replay.

**Quote (if essential):**
> "Experimentation has proven that PM can be an effective tool for defense teams to identify the characteristics of attacker actions, especially the sequence of events." (§8, source line 752)

**Maps to:** [`../specs/architecture.md`](../specs/architecture.md) §(j) — specifically the *output use* axis (Rodríguez: process model for forensic interpretation; this thesis: sampling-ready behavioural profile driving MTD evaluation); also §(l) where the open question of whether GASP should be encoded as a Petri net is noted as a *separate workstream*, not a Rodríguez-style methodology.

**Disposition for this thesis:** **contrasted-against.** Resolves the Open Question previously listed in this stub — "whether the Petri-net output is operationalisable as a simulator-runnable attacker process". The paper does not operationalise it that way; the model is an interpretive artefact for human analysts and a reference for conformance checking, not a process to execute. This thesis's L3 OGASP layer goes the other direction: it consumes a structured profile (GASP) as an *executable* traversal inside the substrate.

---

### Used in lit review

Exact `LIT_REVIEW.md` line locator(s) where this paper is cited as `[7]`:

- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md):26 (§I introduction) — used to anchor the umbrella claim that attack profiling reconstructs adversary behaviour as structured TTP-level representations.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md):97 (§III-A MITRE ATT&CK) — used as the source of the tactic/technique/sub-technique/procedure hierarchy definition (see source line 73 of the paper, §2.2).
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md):131 (§III-D Attack Profiling, opening sentence) — anchors the attacker-trait framing; see Concept 2 for the paraphrase-mismatch flag.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md):137 (§III-D, PM family) — names Rodríguez as the PM-based extraction exemplar, "discover[ing] attacker process models from labelled runtime event logs, recovering process structure in formalisms such as Petri nets"; see Concept 3 + Concept 4.
- [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md):215 (§V Synthesis) — grouped citation `[7], [16], [17]` for the three automated-extraction exemplars (PM / NLP / LLM), supporting the claim that the means to close the procedural-semantic gap already exist in MTD-adjacent literatures.

---

## Open questions / things to verify

- **Citation-key year — resolved.** Citation key `rodriguez2024` tracks the publication date (01 August 2024) rather than the DOI suffix `2023` (which reflects the journal volume's opening year — vol 15 opened 2023). Marc-confirmed: publication year is the canonical disambiguator across the project's citation keys.
- **Petri-net operationalisability — resolved.** Rodríguez's output is interpretive (qualitative expert reading) and conformance-check input, not an executable process; see Concept 4. The architecture §(l) open question of Petri-net encoding for GASP is a *separate* design decision for L2/L3, not a fidelity claim against Rodríguez.
- **§III-D opening sentence wording — resolved with flag.** The exact Rodríguez phrasing is "objectives, knowledge, and modus operandi" (§7, source line 695), not "objectives, motivations, and knowledge" as paraphrased in [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md):131. The lit-review phrasing is a defensible paraphrase in spirit but substitutes "motivations" for "modus operandi" — recommended action either (a) tighten the §III-D sentence to track Rodríguez verbatim, or (b) retain the paraphrase and drop the trailing `[7]` citation so the substitution is not attributed to the paper. Out of scope for this extraction; flagged for the lit-review editing pass.
- **Concern — does this extraction *retire* the docs-audit "Rodríguez four-axes" finding?** Yes for the four axes named in architecture §(j) (input class / temporal stance / output use / validation): each axis is now grounded against a specific Rodríguez locator (input class against §3.1 source line 109; temporal stance against §4 / §5 source lines 203 / 500; output use against §3.2 + §8 source lines 179 / 752; validation against §4.4 + §5.4 source lines 342 / —). The "this is just process mining" reviewer reading is now answered. The separate paraphrase concern flagged in the bullet above is *not* the audit finding — that is a lit-review-prose issue for a different pass.

## Out of scope for this thesis

- Process-mining theory beyond what's needed to assess applicability.
