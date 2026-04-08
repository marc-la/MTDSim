# Attack Graph Design Schema — v0.3

**Author:** Marc Labouchardiere (23857377)  
**Supervisor:** Dr Jin B. Hong  
**Date:** April 2026  
**Status:** Design Document — Source of Truth for Implementation  

---

## 1. Purpose and Scope

This document defines the design schema for constructing a **Generalised Attack Profile (GAP)** — a single, global technique-dependency graph derived from MITRE ATT&CK data. The GAP encodes how ATT&CK techniques relate to one another in terms of preconditions and temporal ordering, aggregated across all observed adversary groups and campaigns. It is consumed by the MTD simulator as the adversary module's behaviour model.

**Central question this graph must answer:** Across all MITRE ATT&CK campaigns and groups, what dependency relationships exist between techniques, and how should these be structured so that the simulator can traverse them as a realistic, generalised attack behaviour?

**What this graph is NOT:**
- It is not a per-campaign graph. We build one graph from the union of all technique usage, then derive dependencies at the technique level globally.
- It is not a manually constructed graph. The primary edge set is derived statistically via association rule mining over ATT&CK usage data (following Rahman et al., 2022), with directionality imposed by tactic ordering.
- It is not an NLP pipeline. Automated CTI parsing is a future extension.

**Scope (Proof of Concept):**
- Enterprise ATT&CK matrix only (not Mobile, not ICS).
- One global graph. Campaign/group metadata stored on nodes as provenance.
- First iteration targets structural correctness and a usable visualisation/traversal tool. Technique clustering and simulator integration are future work.

---

## 2. Core Design Problem: Deriving Edges

MITRE ATT&CK records that groups and campaigns **use** techniques. It does **not** encode ordering or dependencies between those techniques. The matrix organises techniques under **Tactics**, but tactics are explicitly unordered in the framework's design.

The fundamental challenge: **how do you produce directed edges between technique nodes when the source data provides only set membership?**

### 2.1 Solution: Co-occurrence Mining + Tactic-Directed Ordering

We decompose the edge problem into two sub-problems and solve each with a different method:

1. **Which techniques are related?** → Association rule mining over ATT&CK group/software usage data reveals statistically significant technique co-occurrences (Rahman et al., 2022).
2. **Which direction does the dependency flow?** → The canonical ATT&CK tactic ordering serves as a proxy for temporal progression, assigning directionality to undirected co-occurrence pairs.

This combination produces a weighted, directed graph where every edge is backed by statistical evidence from real adversary data, and direction is grounded in the established tactic progression model.

**Justification for co-occurrence as the primary method:**
- Rahman et al. (2022) applied association rule mining to 115 groups and 484 software entries from ATT&CK, identifying 37 fine-grained technique associations from APT data and 61 from software data. Their co-occurrence rules achieve high confidence (e.g., T1566 + T1105 → T1204 at 99% confidence).
- This approach is reproducible, automated, and scales to the full ATT&CK corpus without manual reading.
- Co-occurrence captures real-world adversary behaviour patterns rather than theoretical dependencies.

**Justification for tactic ordering as the directionality proxy:**
- Kim et al. (2026) map ATT&CK techniques to CKC phases and evaluate MTD effectiveness per phase (Tables 2–3), demonstrating tactic ordering is a defensible proxy for attack progression.
- Che Mat et al. (2024, Table 5) map 18 APT groups' TTPs to CKC phases, confirming real campaigns follow broadly sequential tactic progressions.
- Syed et al. (2025) build Caldera adversary profiles as sequential ability chains ordered by tactic.
- Choi et al. (2021) compute HMM transition probabilities between ATT&CK tactics and find the dominant flow follows the canonical ordering.
- Zhang et al. (2025, DeepOP) use ontology reasoning to extract causal relationships between techniques and find they align with tactic phase progression.

---

## 3. Edge Derivation: Three-Source Architecture

Edges come from three sources, layered by priority. Sources are combined into a single edge set; edges supported by multiple sources receive higher confidence.

### 3.1 Primary: Co-occurrence Mining (Automated)

Replicates and extends Rahman et al. (2022).

**Input:** Technique usage matrix — rows = ATT&CK groups + software entries, columns = techniques, cells = binary (0/1 usage).

**Method:**
1. Build the usage matrix from STIX `relationship` objects (type `uses`) linking `intrusion-set` and `malware`/`tool` objects to `attack-pattern` objects.
2. Apply FP-Growth association rule mining (via `mlxtend`) with:
   - `min_support = 0.1` (technique pair appears in ≥10% of entities)
   - `min_confidence = 0.6` (given antecedent, consequent appears ≥60% of the time)
3. Extract simple rules: antecedent (single technique) → consequent (single technique).
4. Filter rules to those with confidence ≥ median confidence across all rules.
5. For each rule `(T_a, T_b)`:
   - Look up `tactic_layer(T_a)` and `tactic_layer(T_b)`.
   - If `tactic_layer(T_a) < tactic_layer(T_b)`: create directed edge `T_a → T_b`.
   - If `tactic_layer(T_a) > tactic_layer(T_b)`: create directed edge `T_b → T_a` (reverse the rule direction to respect tactic flow).
   - If `tactic_layer(T_a) == tactic_layer(T_b)`: **intra-tactic pair** — record as undirected for now (see Section 3.4).
6. Edge weight = rule confidence. Store support and lift as metadata.

**Output:** A set of directed, weighted edges with statistical provenance.

### 3.2 Supplementary: Structured Dataset Import (Automated)

Import edges from existing curated sources that encode explicit technique ordering:

**a) MITRE Attack Flow Corpus**
- Source: https://github.com/center-for-threat-informed-defense/attack-flow
- Machine-readable JSON DAGs for select campaigns.
- Extract all technique-to-technique sequencing edges.
- These are the highest-fidelity edges available — manually curated by MITRE's Center for Threat-Informed Defense.

**b) Syed et al. (2025) Caldera Ability Sequences**
- Source: Table II of the paper; 12 APT profiles with explicit technique orderings.
- For each sequence, extract consecutive technique pairs as directed edges.

**c) DeepOP-style Ontology Extraction (Simplified)**
- For each technique in the STIX bundle, parse its `description` text.
- Search for explicit precondition language: "requires", "after", "following", "depends on", "using credentials obtained", "with access to", "once ... is achieved".
- Where such language references another identifiable technique (by name or ATT&CK ID), record a directed edge.
- Low yield expected (perhaps 20–40 edges), but each is high-confidence and documentation-backed.

### 3.3 Tertiary: Manual Annotation (Targeted Gap-Filling)

Manual reading of ATT&CK technique pages and CTI reports, targeted at:
- **Orphan nodes:** Techniques with in-degree == 0 and `tactic_layer > 2` (something should precede them).
- **Intra-tactic pairs** from Section 3.1 step 5 that need directionality resolved.
- **High-campaign-count techniques** that lack edges after automated sources.

This is no longer the primary construction method — it is gap-filling. The co-occurrence mining and structured imports do the heavy lifting.

### 3.4 Unresolved Case: Intra-Tactic Pairs

When two co-occurring techniques share the same tactic, tactic ordering cannot assign direction. These pairs are stored as a separate unresolved set for manual review.

**Options (to be resolved during annotation):**
1. **Omit** — drop intra-tactic edges entirely. Simplest; accepts loss of intra-tactic dependencies.
2. **Bidirectional** — add edges in both directions. Honest but complicates DAG property.
3. **Manual resolution** — read technique documentation to determine which precedes the other. Highest fidelity; bounded workload since intra-tactic pairs are a subset of all co-occurrence rules.

For the first iteration, **omit intra-tactic pairs** and note as a limitation. The number of affected pairs should be reported for transparency.

---

## 4. Graph Schema

### 4.1 Node Definition

```python
@dataclass
class TechniqueNode:
    technique_id: str          # e.g., "T1059"
    technique_name: str        # e.g., "Command and Scripting Interpreter"
    tactics: list[str]         # All mapped tactics, e.g., ["execution"]
    primary_tactic: str        # Earliest tactic in canonical ordering
    tactic_layer: int          # Layer number (0-13)
    platforms: list[str]       # ["Windows", "Linux", ...]
    
    # Provenance metadata
    campaign_count: int        # Number of campaigns using this technique
    campaign_ids: list[str]    # MITRE Campaign IDs
    group_count: int           # Number of groups using this technique
    group_ids: list[str]       # MITRE Group IDs
    software_ids: list[str]    # MITRE Software IDs
    
    # Sub-technique tracking (collapsed but stored)
    sub_technique_ids: list[str]
```

**Granularity:** Techniques (not sub-techniques) are the default node granularity. Sub-techniques collapse to parent. Configurable.

**Tactic layers:**

| Layer | Tactic |
|-------|--------|
| 0 | Reconnaissance |
| 1 | Resource Development |
| 2 | Initial Access |
| 3 | Execution |
| 4 | Persistence |
| 5 | Privilege Escalation |
| 6 | Defense Evasion |
| 7 | Credential Access |
| 8 | Discovery |
| 9 | Lateral Movement |
| 10 | Collection |
| 11 | Command and Control |
| 12 | Exfiltration |
| 13 | Impact |

### 4.2 Edge Definition

```python
@dataclass
class DependencyEdge:
    source_id: str             # Technique ID of precondition
    target_id: str             # Technique ID of postcondition
    evidence_type: str         # Primary source type (see table below)
    confidence: float          # 0.0-1.0 (from co-occurrence rule, or 1.0 for curated sources)
    support: float             # Co-occurrence support (0.0-1.0), or None for non-statistical sources
    lift: float                # Co-occurrence lift, or None
    evidence: list[Evidence]   # Provenance records
    source_count: int          # Number of independent sources supporting this edge
    is_backward: bool          # True if target_layer <= source_layer

@dataclass
class Evidence:
    source_type: str           # "co_occurrence" | "attack_flow" | "caldera_sequence" | "ontology" | "documentation" | "cti_report"
    source_url: str            # URL, STIX ID, or paper reference
    description: str           # Brief annotation
    campaigns: list[str]       # Relevant campaign IDs (if applicable)
```

**Edge evidence types:**

| Type | Source | How Produced | Expected Yield |
|------|--------|-------------|----------------|
| `co_occurrence` | ATT&CK group/software usage data | FP-Growth association rule mining | High — bulk of edges |
| `attack_flow` | MITRE Attack Flow corpus | Automated JSON import | Medium — select campaigns only |
| `caldera_sequence` | Syed et al. (2025) | Automated/manual import | Medium — 12 APT profiles |
| `ontology` | ATT&CK STIX technique descriptions | Keyword-based precondition extraction | Low — 20-40 edges |
| `documentation` | ATT&CK technique pages | Manual reading (gap-filling) | Low — targeted |
| `cti_report` | Vendor reports | Manual reading (gap-filling) | Low — targeted |

**Multi-source edges:** When the same edge (T_a → T_b) appears in multiple sources, all evidence records are merged into a single edge with `source_count` incremented. Higher `source_count` = higher confidence. These "consensus edges" are the backbone of the graph.

### 4.3 Graph-Level Structure

```python
@dataclass
class GeneralisedAttackProfile:
    version: str                  # Schema version ("0.3")
    build_date: str
    technique_source: str         # e.g., "enterprise-attack v16.1"
    
    nodes: dict[str, TechniqueNode]
    edges: list[DependencyEdge]
    
    # Computed properties
    entry_nodes: list[str]        # In-degree 0
    objective_nodes: list[str]    # Out-degree 0
    layers: dict[int, list[str]]  # Layer -> technique_ids
    
    # Quality metrics
    total_techniques: int
    techniques_with_edges: int    # At least one in or out edge
    orphan_techniques: int        # No edges at all
    edge_count: int
    consensus_edge_count: int     # Edges with source_count >= 2
    intra_tactic_unresolved: int  # Co-occurrence pairs dropped due to same tactic
    backward_edge_count: int
    
    # Co-occurrence parameters (reproducibility)
    min_support: float
    min_confidence: float
    confidence_threshold: float   # Median used for filtering
```

---

## 5. Construction Algorithm

```
ALGORITHM: BuildGAP()

INPUT:  MITRE ATT&CK STIX bundle (enterprise-attack.json)
OUTPUT: GeneralisedAttackProfile

--- PHASE 1: Node Population ---
1.  PARSE STIX bundle
2.  For each attack-pattern:
      Create TechniqueNode
      Assign tactic_layer from earliest kill_chain_phase
      Collapse sub-techniques to parent
3.  For each uses-relationship (group->technique, software->technique, campaign->technique):
      Update node provenance metadata
4.  Group nodes into layers dict

--- PHASE 2: Co-occurrence Edge Mining ---
5.  BUILD usage matrix:
      Rows = groups + software entries
      Columns = techniques
      Cells = 1 if entity uses technique, else 0
6.  APPLY FP-Growth (min_support=0.1)
7.  GENERATE association rules (min_confidence=0.6)
8.  COMPUTE median confidence across all rules
9.  FILTER rules to confidence >= median
10. For each rule (T_a -> T_b):
      If tactic_layer(T_a) < tactic_layer(T_b):
          Create edge T_a -> T_b (forward)
      Elif tactic_layer(T_a) > tactic_layer(T_b):
          Create edge T_b -> T_a (reverse to respect tactic flow)
      Else:
          Record as intra-tactic unresolved pair (omit edge)
      Set evidence_type="co_occurrence", confidence=rule_confidence

--- PHASE 3: Supplementary Edge Import ---
11. IMPORT Attack Flow corpus edges (evidence_type="attack_flow")
12. IMPORT Syed et al. Caldera sequences (evidence_type="caldera_sequence")
13. EXTRACT ontology edges from STIX descriptions (evidence_type="ontology")
14. For each imported edge:
      If edge already exists from Phase 2:
          Merge evidence, increment source_count
      Else:
          Create new edge

--- PHASE 4: Manual Gap-Filling (Iterative, Ongoing) ---
15. IDENTIFY orphan techniques (in-degree==0, tactic_layer > 2)
16. IDENTIFY high-campaign-count techniques with no edges
17. Manual annotation targets these; edges added as evidence_type="documentation" or "cti_report"

--- PHASE 5: Validation ---
18. FLAG backward edges (is_backward = target_layer <= source_layer)
19. CHECK for cycles; if found, remove weakest-evidence backward edge
20. COMPUTE quality metrics (coverage, consensus edges, orphans)
21. RETURN GeneralisedAttackProfile
```

**Phase 2 is the core.** It produces the bulk of edges automatically. Phases 3–4 refine and supplement.

**Reproducibility:** All co-occurrence parameters (min_support, min_confidence, median threshold) are stored in the output for reproducibility. Anyone can re-run Phase 2 with the same STIX bundle and get the same edges.

---

## 6. Visualisation and Traversal Tool

### 6.1 Layout

**Layered/hierarchical layout** (Sugiyama-style): x-axis = tactic layers (0–13), techniques within a layer arranged vertically. Mirrors ATT&CK matrix presentation and Kim et al.'s CKC-phase tables.

### 6.2 Implementation Stack

- **Graph construction and analysis:** NetworkX (Python).
- **Serialisation:** JSON (node-link format).
- **Static visualisation:** Graphviz DOT for thesis figures.
- **Interactive traversal tool:** `pyvis` (Python → HTML). Must support:
  - Node click → technique details, edges, evidence, provenance.
  - Filter by tactic layer, campaign, group.
  - Highlight attack paths (entry → objective subgraphs).
  - Toggle edge sources on/off (show only co-occurrence, only attack_flow, etc.).
  - Show orphan nodes in distinct colour.
  - Show consensus edges (source_count ≥ 2) with emphasis.

### 6.3 Visual Encoding

- **Node colour:** By tactic layer (14-colour categorical palette).
- **Node size:** Scaled by `campaign_count`.
- **Node border:** Solid if has edges, dashed if orphan.
- **Edge colour:** By primary `evidence_type`:
  - Blue = co_occurrence
  - Green = attack_flow
  - Orange = caldera_sequence
  - Purple = ontology
  - Grey = documentation / cti_report
- **Edge width:** Proportional to `confidence`.
- **Edge style:** Solid = forward, dashed = backward.
- **Edge glow/emphasis:** `source_count >= 2` edges rendered thicker (consensus).

---

## 7. Design Decisions and Justifications

### D1: Single Global Graph, Not Per-Campaign

**Choice:** One graph from the union of all groups/campaigns.  
**Why:** Per-campaign graphs are sparse (3–10 techniques each). A global graph is denser and supports statistical mining. Matches supervisor instruction: "amalgamate campaigns, all techniques as nodes by tactic layer, then find dependencies."

### D2: Co-occurrence Mining as Primary Edge Source

**Choice:** FP-Growth association rules over ATT&CK usage data, rather than manual annotation or NLP.  
**Why:** Produces a statistically grounded edge set from the full ATT&CK corpus without manual reading. Rahman et al. (2022) validated this approach on 115 groups and 484 software entries. Edges represent real observed adversary co-usage patterns, not theoretical dependencies. Manual annotation is demoted to gap-filling.

### D3: Tactic Ordering for Directionality Only

**Choice:** Tactic ordering assigns direction to undirected co-occurrence pairs. It does not generate edges.  
**Why:** Co-occurrence rules are symmetric ("T_a and T_b co-occur") but attack graphs need direction. Tactic ordering provides a defensible heuristic for "which comes first" without generating spurious edges between unrelated techniques. This is a weaker claim than "T_a causes T_b" — it says "T_a and T_b are observed together, and T_a's tactic typically precedes T_b's tactic." The distinction is acknowledged.

### D4: Intra-Tactic Pairs Omitted (First Iteration)

**Choice:** Drop co-occurrence pairs where both techniques share the same tactic.  
**Why:** No heuristic can assign direction. Manual resolution is possible but bounded to a subset of all rules. Noted as a limitation. The count of omitted pairs is reported for transparency.

### D5: Multi-Source Consensus for Confidence

**Choice:** Edges supported by 2+ independent sources (e.g., co-occurrence AND attack flow) are treated as highest-confidence.  
**Why:** Each source has different biases. Co-occurrence is statistical and may capture incidental co-usage. Attack Flow is curated but covers few campaigns. Caldera sequences are reproducible but cover 12 APTs. Convergent evidence from multiple sources reduces bias. The `source_count` field makes this auditable.

### D6: Evidence-First Design

**Choice:** Every edge requires provenance (source type, URL/reference, description).  
**Why:** Makes the graph auditable and incrementally improvable. A reviewer can verify any edge. Anyone can add edges by adding evidence records.

### D7: Techniques as Default Granularity

**Choice:** Collapse sub-techniques to parent techniques.  
**Why:** STIX data is inconsistent in sub-technique granularity. Collapsing avoids fragmentation. Configurable for future iterations.

### D8: DAG with Flagged Backward Edges

**Choice:** Permit backward edges but flag them; break cycles by removing weakest-evidence backward edge.  
**Why:** Real adversary behaviour includes loops (Lateral Movement → Discovery → Lateral Movement). Strict DAG cannot represent this. The compromise preserves realism while keeping the graph traversable.

---

## 8. Known Hurdles and Mitigations

### H1: Co-occurrence ≠ Causation

**Problem:** Two techniques co-occurring does not mean one causes or enables the other. Some co-occurrences may be incidental (e.g., both are common and appear in many groups independently).  
**Mitigation:** Filter by lift > 1.0 (co-occurrence is more frequent than expected by chance). Require confidence above median. Use consensus with curated sources (Attack Flow, Caldera) to validate. Acknowledge the limitation: edges represent "observed co-usage with directional heuristic" not "proven dependency."

### H2: Tactic Ordering Is an Approximation

**Problem:** MITRE states tactics are unordered. Real attacks may not follow canonical progression.  
**Mitigation:** Tactic ordering is used only for directionality, not edge generation. Backward edges are permitted when curated evidence supports them. The HMM transition analysis (Choi et al., 2021) can validate that the canonical ordering matches dominant real-world flows.

### H3: Intra-Tactic Blind Spot

**Problem:** Co-occurring techniques within the same tactic have no heuristic for directionality, so they are omitted.  
**Mitigation:** Report the count and list of omitted pairs. Flag for future manual resolution. In practice, intra-tactic dependencies are less critical for the simulator than cross-tactic ones (the simulator primarily needs to know "what phase comes next").

### H4: Sparse Co-occurrence for Rare Techniques

**Problem:** Techniques used by only 1–2 groups will not meet the `min_support` threshold and will have no co-occurrence edges.  
**Mitigation:** These are the orphan nodes targeted by Phase 4 manual annotation. The curated sources (Attack Flow, Caldera, ontology extraction) may also cover some.

### H5: Multi-Tactic Techniques

**Problem:** Some techniques map to 2+ tactics. Assigning to the earliest layer may misrepresent their role.  
**Mitigation:** Assign to earliest layer; store all tactic memberships. Co-occurrence mining is unaffected by layer assignment (it operates on the usage matrix, not the layer structure). Directionality assignment may occasionally be wrong for multi-tactic techniques — flagged for review.

---

## 9. Integration with MTD Simulator

The GAP feeds into the simulator's adversary module (extending Zhang (2022) and Ho (2024)'s theses):

1. **Technique selection:** The adversary traverses the GAP, picking successor techniques weighted by edge confidence. Higher-confidence edges are more likely paths.
2. **Attack sophistication:** Different subgraphs represent different threat actor profiles. Filtering the GAP to a specific group's techniques produces a campaign-specific profile.
3. **MTD interaction:** Each technique maps to digital artifacts (per Kim et al.'s Table 1). MTD operations that change an artifact disrupt techniques targeting it. The GAP tells the simulator which techniques are affected at each attack phase.
4. **Probabilistic traversal:** Edge weights (confidence) enable stochastic simulation — the adversary doesn't always take the same path.

---

## 10. First Iteration Deliverables

1. **STIX parser** (`stix_parser.py`): Extracts techniques, campaigns, groups, software, and relationships. Outputs layered node set as JSON.
2. **Co-occurrence miner** (`cooccurrence_miner.py`): Builds usage matrix, runs FP-Growth, generates directed edges with tactic-ordering directionality. Outputs edge set as JSON with full provenance.
3. **Structured edge importer** (`edge_importer.py`): Imports edges from Attack Flow corpus and Syed et al. Caldera sequences. Merges with co-occurrence edges.
4. **Ontology extractor** (`ontology_extractor.py`): Parses STIX technique descriptions for precondition language. Produces supplementary edges.
5. **Graph builder** (`gap_builder.py`): Combines all edge sources, merges multi-source edges, validates (cycles, orphans, backward edges), computes quality metrics.
6. **Visualisation/traversal tool**: Interactive HTML via pyvis. Node/edge inspection, filtering, path highlighting, coverage display.
7. **JSON export**: Complete GAP in node-link format for simulator consumption.
8. **Quality report**: Coverage statistics, consensus edges, orphan list, intra-tactic unresolved pairs.

---

## 11. Future Work (Out of Scope for First Iteration)

- **Intra-tactic edge resolution:** Manual or NLP-based directionality for same-tactic co-occurrence pairs.
- **Technique clustering:** Group similar techniques into simulator modules for `APTAttacker`.
- **Edge weighting refinement:** Incorporate HMM transition probabilities (Choi et al., 2021) as an additional weight signal.
- **Blockers:** Model MTD operations that invalidate specific techniques.
- **Automated CTI extraction:** LLM-based pipeline (AttacKG+, CTI-Thinker) to extract edges from vendor reports.
- **Sub-technique granularity:** Expand to sub-technique level where data supports it.
- **Temporal analysis:** Track how co-occurrence patterns change across ATT&CK versions.

---

## References

- Kim, M. et al. (2026). MTD in depth: Multi-phased moving target defense techniques against cyber-attacks based on cyber kill chain. *Future Generation Computer Systems*, 181, 108419.
- Rahman, Md. R. et al. (2022). Investigating co-occurrences of MITRE ATT&CK Techniques. *arXiv preprint arXiv:2211.06495*.
- Zhang, S. et al. (2025). DeepOP: A Hybrid Framework for MITRE ATT&CK Sequence Prediction via Deep Learning and Ontology. *Electronics*, 14(2), 257.
- Choi, S. et al. (2021). Probabilistic Attack Sequence Generation and Execution Based on MITRE ATT&CK for ICS Datasets. *CSET '21*.
- Zhang, Y. et al. (2025). AttacKG+: Boosting Attack Knowledge Graph Construction with Large Language Models. *Computers & Security*, 150, 104220.
- Syed, A. et al. (2025). Comprehensive Advanced Persistent Threats Dataset. *IEEE Networking Letters*, 7(2), 150-154.
- Che Mat, N.I. et al. (2024). A systematic literature review on advanced persistent threat behaviors and its detection strategy. *Journal of Cybersecurity*, 10(1), tyad023.
- Selmanaj, D. (2024). *Adversary Emulation with MITRE ATT&CK*. O'Reilly Media.
- MITRE. (2025). MITRE ATT&CK Framework. https://attack.mitre.org/
- MITRE CTID. (2024). Attack Flow. https://center-for-threat-informed-defense.github.io/attack-flow/