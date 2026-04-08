# Attack Graph Design Schema — v0.2 (First Iteration)

**Author:** Marc Labouchardiere (23857377)  
**Supervisor:** Dr Jin B. Hong  
**Date:** April 2026  
**Status:** Design Document — Source of Truth for Implementation  

---

## 1. Purpose and Scope

This document defines the design schema for constructing a **Generalised Attack Profile (GAP)** — a single, global technique-dependency graph derived from MITRE ATT&CK campaign data. The GAP encodes how ATT&CK techniques relate to one another in terms of preconditions and temporal ordering, aggregated across all observed campaigns. It is consumed by the MTD simulator as the adversary module's behaviour model.

**Central question this graph must answer:** Across all MITRE ATT&CK campaigns, what dependency relationships exist between techniques, and how should these be structured so that the simulator can traverse them as a realistic, generalised attack behaviour?

**What this graph is NOT:**
- It is not a per-campaign graph. We do not build separate graphs per campaign and then merge them. We build one graph from the union of all campaign technique memberships, then find dependencies at the technique level globally.
- It is not an NLP pipeline. Edge derivation in the first iteration is primarily structural (tactic ordering) supplemented by manual annotation from documentation. Automated CTI parsing is a future extension.

**Scope (Proof of Concept):**
- Enterprise ATT&CK matrix only (not Mobile, not ICS).
- One global graph. Campaign/group metadata is stored on nodes as provenance, not as separate graph instances.
- First iteration targets structural correctness and a usable visualisation/traversal tool. Probabilistic edge weighting and technique clustering are future work.

---

## 2. Core Design Problem: Deriving Edges

MITRE ATT&CK records that campaigns **use** techniques. It does **not** encode ordering or dependencies between those techniques. The ATT&CK matrix organises techniques under **Tactics** (columns representing tactical goals), but tactics are explicitly unordered in the framework's design.

The fundamental challenge: **how do you produce directed edges (precondition to postcondition) between technique nodes when the source data provides only set membership?**

Because we are building a single global graph rather than per-campaign graphs, the question simplifies from "did technique X precede technique Y in campaign C?" to the more general and more answerable: **"does technique X generally enable or precede technique Y in adversary operations?"**

### 2.1 Edge Derivation Strategy

Two phases, executed sequentially. Phase 1 provides the structural skeleton. Phase 2 refines it with evidence-based edges. Both operate on the single global graph.

#### Phase 1 — Tactic-Layer Structure (Automatic)

Arrange all techniques into layers defined by the canonical ATT&CK tactic ordering:

```
Layer 0:  Reconnaissance
Layer 1:  Resource Development
Layer 2:  Initial Access
Layer 3:  Execution
Layer 4:  Persistence
Layer 5:  Privilege Escalation
Layer 6:  Defense Evasion
Layer 7:  Credential Access
Layer 8:  Discovery
Layer 9:  Lateral Movement
Layer 10: Collection
Layer 11: Command and Control
Layer 12: Exfiltration
Layer 13: Impact
```

This layering is not itself an edge set — it is the **scaffold** that constrains where edges can go. Edges flow from lower-numbered layers to higher-numbered layers (or within the same layer, if Phase 2 evidence supports it). The layering provides the partial order; edges provide the specific dependencies.

**No edges are created in Phase 1.** The output is a layered node set, not a connected graph. This avoids the O(n^2) fully-connected problem from the previous design.

**Justification:**
- Kim et al. (2026) map ATT&CK techniques to CKC phases and evaluate MTD effectiveness per phase (Tables 2–3). Their work demonstrates that tactic ordering is a defensible proxy for attack progression.
- Che Mat et al. (2024, Table 5) map 18 APT groups' TTPs to CKC phases, confirming real campaigns follow broadly sequential tactic progressions.
- Syed et al. (2025) build Caldera adversary profiles as sequential ability chains ordered by tactic (Fig. 4).

**Handling multi-tactic techniques:** Some techniques belong to multiple tactics (e.g., T1548 Abuse Elevation Control Mechanism maps to both Privilege Escalation and Defense Evasion). Assign the node to its **earliest** tactic layer. Store all tactic memberships as metadata. A future iteration could duplicate nodes per tactic if needed.

#### Phase 2 — Dependency Annotation (Manual, Iterative)

With the layered node set in place, add edges by consulting documentation. This is the labour-intensive step that the supervisor identified as "will take time." The process is:

**Step 2a — ATT&CK Technique Documentation**

For each technique in the graph, read its ATT&CK page (https://attack.mitre.org/techniques/TXXXX). Focus on:
- **"Procedure Examples"** section: describes how real groups have used the technique, often revealing what precedes or follows it.
- **"Mitigations"** and **"Detection"** sections: sometimes imply preconditions (e.g., "this technique requires the adversary to have already obtained valid credentials" implies a Credential Access dependency).
- **Technique description** itself: often states prerequisites explicitly (e.g., T1021 Remote Services states the adversary needs valid accounts, linking to T1078 Valid Accounts).

For each identified dependency, record: `(source_technique, target_technique, evidence_url, annotation_note)`.

**Step 2b — Existing Structured Datasets**

Import edges from sources that already encode technique ordering:
1. **MITRE Attack Flow Corpus** (https://github.com/center-for-threat-informed-defense/attack-flow) — machine-readable DAGs for select campaigns. Extract all technique-to-technique edges and add to the global graph.
2. **Syed et al. (2025) Caldera ability sequences** (Table II) — explicit technique orderings for 12 APT profiles (APT41, APT29, APT28, APT10, APT39, APT32, APT5, APT3, Aquatic Panda, Windshift, Dragonfly, APT35). Each sequence directly yields pairwise edges between consecutive techniques.
3. **MITRE Campaign STIX `description` fields** — read for temporal/causal language ("after", "then", "following", "once X was achieved"). Record pairwise dependencies where the language is unambiguous.

**Step 2c — CTI Reports (Selective)**

For high-priority techniques that remain poorly connected after Steps 2a–2b, consult vendor CTI reports (Unit 42, Mandiant, CrowdStrike). This is targeted gap-filling, not exhaustive corpus parsing.

**Edge directionality rule:** An edge source->target means "source is a precondition for, or typically precedes, target." Edges must respect the tactic layer ordering (source layer <= target layer) unless there is strong narrative evidence for a backward dependency (e.g., Discovery feeding back into Lateral Movement). Backward edges are permitted but flagged.

**No NLP in the first iteration.** All annotation is manual reading and recording. This is deliberate: automated CTI parsing (e.g., TTPDrill, AttacKG) is an open research problem and out of scope for this PoC.

---

## 3. Graph Schema

### 3.1 Node Definition

Each node represents a unique ATT&CK **Technique** in the global graph.

```python
@dataclass
class TechniqueNode:
    technique_id: str          # e.g., "T1059"
    technique_name: str        # e.g., "Command and Scripting Interpreter"
    tactics: list[str]         # All mapped tactics, e.g., ["execution"]
    primary_tactic: str        # Earliest tactic in canonical ordering
    tactic_layer: int          # Layer number (0-13)
    platforms: list[str]       # ["Windows", "Linux", ...]
    
    # Provenance metadata (which campaigns/groups use this technique)
    campaign_count: int        # Number of campaigns using this technique
    campaign_ids: list[str]    # MITRE Campaign IDs (e.g., ["C0015", "C0018"])
    group_ids: list[str]       # Associated MITRE Group IDs
    
    # Sub-technique tracking (collapsed but stored)
    sub_technique_ids: list[str]  # e.g., ["T1059.001", "T1059.003"]
```

**Granularity:** Techniques (not sub-techniques) are the default node granularity. Sub-techniques are collapsed to their parent. Where a campaign references T1059.001 (PowerShell), it maps to the T1059 node. Sub-technique IDs are stored for future drill-down. This is configurable.

### 3.2 Edge Definition

Each edge represents a **dependency**: the source technique enables, facilitates, or is a general precondition for the target technique.

```python
@dataclass
class DependencyEdge:
    source_id: str             # Technique ID of precondition
    target_id: str             # Technique ID of postcondition
    evidence_type: str         # "documentation" | "attack_flow" | "caldera_sequence" | "cti_report"
    evidence: list[Evidence]   # Provenance records
    is_backward: bool          # True if target_layer <= source_layer (flagged)

@dataclass
class Evidence:
    source_url: str            # URL or STIX ID
    description: str           # Brief annotation of why this edge exists
    campaigns: list[str]       # Campaign IDs where this transition is observed (if applicable)
```

**Edge types explained:**

| Type | Source | How Produced |
|------|--------|-------------|
| `documentation` | ATT&CK technique pages (Procedure Examples, description) | Manual reading (Phase 2a) |
| `attack_flow` | MITRE Attack Flow corpus JSON files | Automated import (Phase 2b) |
| `caldera_sequence` | Syed et al. (2025) ability sequences | Automated import (Phase 2b) |
| `cti_report` | Vendor blog posts, white papers | Manual reading (Phase 2c) |

**No `tactic_order` edge type.** Unlike v0.1, tactic ordering is used only as a structural constraint (layer assignment), not as an edge generator. Every edge in the graph has explicit evidence behind it. This makes the graph sparser but more defensible.

### 3.3 Graph-Level Structure

```python
@dataclass
class GeneralisedAttackProfile:
    version: str                  # Schema version
    build_date: str               # When the graph was last constructed
    technique_source: str         # e.g., "enterprise-attack v16.1"
    
    nodes: dict[str, TechniqueNode]  # Keyed by technique_id
    edges: list[DependencyEdge]
    
    # Computed properties
    entry_nodes: list[str]        # In-degree 0 (typically Recon/Initial Access)
    objective_nodes: list[str]    # Out-degree 0 (typically Exfiltration/Impact)
    layers: dict[int, list[str]]  # Layer number -> list of technique_ids
    
    # Annotation progress tracking
    annotated_count: int          # Techniques with at least one outgoing edge
    unannotated_count: int        # Techniques with no edges yet
```

The graph is a **DAG** (directed acyclic graph). Backward edges (`is_backward == True`) are permitted but tracked separately. If backward edges create cycles, the graph becomes a DCG (directed cyclic graph); flag these for review and consider removing the weakest-evidence backward edge.

---

## 4. Data Sources and Extraction Pipeline

### 4.1 Node Population: MITRE ATT&CK STIX Bundle

**Source:** https://github.com/mitre/cti (`enterprise-attack.json`, STIX 2.1)

**Extraction steps:**
1. Parse the STIX bundle.
2. Collect all `attack-pattern` objects (techniques). For each, extract: technique ID (external reference), name, `kill_chain_phases` (tactic assignments), platforms.
3. Collect all `campaign` objects and all `relationship` objects where `relationship_type == "uses"` linking campaigns/groups to techniques.
4. Build the node set: one node per unique technique. Populate `campaign_ids`, `group_ids`, `campaign_count` from the relationships.
5. Assign each node to its `tactic_layer` based on its earliest tactic.
6. Collapse sub-techniques to parent technique nodes.

**Output:** A layered node set with no edges. This is the input to Phase 2.

### 4.2 Edge Sources

| Source | Format | Import Method | Priority |
|--------|--------|---------------|----------|
| ATT&CK technique pages | Web / STIX descriptions | Manual reading | Primary — covers all techniques |
| MITRE Attack Flow corpus | JSON (Attack Flow schema) | Script to extract technique pairs | High — authoritative, structured |
| Syed et al. Caldera sequences | Table II in paper | Manual transcription or script | High — 12 APT profiles ready-made |
| MITRE Campaign STIX descriptions | Free text | Manual reading | Medium — patchy temporal language |
| Vendor CTI reports | Blog posts, PDFs | Manual reading (targeted) | Low priority — gap-filling only |

### 4.3 Supplementary References

- **Selmanaj (2024)** *Adversary Emulation with MITRE ATT&CK*: methodological reference for how practitioners sequence techniques into emulation plans. Validates that tactic ordering is standard practice in the industry.
- **Kim et al. (2026)** MTDID framework: provides the ATT&CK-to-CKC-to-digital-artifact mapping (Tables 1–3) that the simulator needs for MTD interaction.

---

## 5. Construction Algorithm

```
ALGORITHM: BuildGAP()

INPUT:  MITRE ATT&CK STIX bundle (enterprise-attack.json)
OUTPUT: GeneralisedAttackProfile

--- PHASE 1: Node Population ---
1. PARSE STIX bundle
2. For each attack-pattern (technique):
     Create TechniqueNode
     Assign tactic_layer from earliest kill_chain_phase
     Collapse sub-techniques to parent
3. For each campaign/group relationship:
     Update node's campaign_ids, group_ids, campaign_count
4. Group nodes into layers dict

--- PHASE 2: Edge Annotation ---
5. IMPORT structured edges:
   a. For each Attack Flow corpus file:
        Extract technique-to-technique pairs
        Create DependencyEdge(evidence_type="attack_flow")
   b. For each Syed et al. Caldera sequence:
        For consecutive pairs (T_i, T_{i+1}):
            Create DependencyEdge(evidence_type="caldera_sequence")

6. MANUAL annotation pass:
   For each technique (prioritised by campaign_count, descending):
     Read ATT&CK technique page
     Identify precondition techniques from description / procedure examples
     Create DependencyEdge(evidence_type="documentation")
     
7. TARGETED gap-filling:
   For techniques with in-degree == 0 AND tactic_layer > 2:
     These are "orphan" techniques that should have preconditions
     Consult CTI reports for edges
     Create DependencyEdge(evidence_type="cti_report")

--- VALIDATION ---
8. FLAG backward edges (target_layer <= source_layer)
9. CHECK for cycles; if found, remove weakest-evidence backward edge
10. COMPUTE entry_nodes, objective_nodes
11. REPORT annotation coverage (annotated_count / total)
12. RETURN GeneralisedAttackProfile
```

**Key difference from v0.1:** No per-campaign graph construction, no transitive reduction step (unnecessary since we're not generating O(n^2) tactic-order edges), no NLP. The algorithm is: populate nodes, import what structured data exists, then manually annotate the rest.

**Prioritisation in Step 6:** Annotate high-campaign-count techniques first. A technique used in 15 campaigns is more important to get right than one used in 1. This ensures the most impactful parts of the graph are correct first, and annotation can be stopped at any point with a usable (if incomplete) graph.

**Step 7 rationale:** A technique at layer 8 (Discovery) with no incoming edges is suspicious — something must have come before it. These orphans indicate annotation gaps and should be prioritised for CTI review.

---

## 6. Visualisation and Traversal Tool

The supervisor specifically requested a tool to visualise and traverse the graph. This is a first-class deliverable, not an afterthought.

### 6.1 Layout

**Layered/hierarchical layout** (Sugiyama-style) where the x-axis represents tactic layers (0–13) and techniques within a layer are arranged vertically. This directly mirrors how ATT&CK is visually presented (tactics as columns) and aligns with Kim et al.'s CKC-phase evaluation tables.

### 6.2 Implementation Stack

- **Graph construction and analysis:** NetworkX (Python). Handles DAG operations, cycle detection, topological sorting.
- **Serialisation:** JSON (node-link format) for both storage and simulator consumption.
- **Static visualisation:** Graphviz DOT via `networkx.drawing.nx_agraph`. Good for thesis figures and reports.
- **Interactive traversal tool:** `pyvis` (Python -> HTML) or a lightweight web app. Must support:
  - Click a node to see its technique details, connected edges, evidence, campaign provenance.
  - Filter by tactic layer, by campaign, by group.
  - Highlight attack paths (connected subgraphs from entry to objective nodes).
  - Show annotation coverage (unannotated nodes in a distinct colour).

### 6.3 Visual Encoding

- **Node colour:** By tactic layer (14-colour categorical palette).
- **Node size:** Scaled by `campaign_count` (more commonly observed = larger).
- **Edge colour:** By `evidence_type` (e.g., blue = documentation, green = attack_flow, orange = caldera_sequence, red = cti_report).
- **Edge style:** Solid for forward edges, dashed for backward edges.

---

## 7. Design Decisions and Justifications

### D1: Single Global Graph, Not Per-Campaign

**Choice:** Build one graph from the union of all campaigns, then annotate dependencies at the technique level.  
**Why:** Per-campaign construction requires solving edge inference N times on sparse data (campaigns often list only 3–10 techniques). A global graph solves it once on a denser node set, where the question "does T_a generally precede T_b?" is more answerable than "did T_a precede T_b in campaign C0024 specifically?" This also directly matches the supervisor's instruction: "amalgamate campaigns, all techniques as nodes by tactic layer, then find dependencies."

### D2: No Automatic Tactic-Order Edges

**Choice:** Tactic ordering defines layer placement only, not edges.  
**Why:** v0.1 generated edges between all cross-layer technique pairs, requiring transitive reduction to tame the O(n^2) explosion. This produced structurally correct but semantically hollow edges — "T1595 Active Scanning precedes T1547 Boot or Logon Autostart Execution" is technically consistent with tactic ordering but is not a meaningful dependency. By requiring every edge to have explicit evidence, the graph is sparser but every edge is defensible. The trade-off is slower construction (manual work), which the supervisor anticipated.

### D3: DAG with Flagged Backward Edges

**Choice:** Permit backward edges (higher layer -> lower layer) but flag them.  
**Why:** Real adversary behaviour includes loops (e.g., Lateral Movement -> Discovery -> Lateral Movement on a new host). A strict DAG cannot represent this. However, cycles complicate simulator traversal. The compromise: allow backward edges, flag them, and break cycles only if they appear. The simulator can handle backward edges as "the adversary returns to an earlier phase."

### D4: Techniques as Default Granularity

**Choice:** Collapse sub-techniques to parent techniques.  
**Why:** Campaign STIX data is inconsistent — some report T1059, others T1059.001. Collapsing avoids fragmentation and keeps the graph manageable. Sub-technique IDs are stored for future drill-down. Configurable.

### D5: Manual Annotation Over NLP

**Choice:** Human reading of ATT&CK documentation and CTI, not automated parsing.  
**Why:** The supervisor explicitly stated this "will take time." Automated CTI extraction (TTPDrill, AttacKG) is itself a research problem. For this PoC, manual annotation with structured import of existing datasets (Attack Flow, Caldera sequences) is more reliable and produces a higher-quality graph. The annotation workload is bounded: prioritise by campaign_count and accept partial coverage.

### D6: Evidence-First Edges

**Choice:** Every edge requires at least one `Evidence` record.  
**Why:** This makes the graph auditable. When the thesis says "T1059 depends on T1190," a reviewer can follow the evidence URL and verify the claim. It also makes the graph incrementally improvable — anyone can add edges by adding evidence, without needing to understand the construction algorithm.

---

## 8. Known Hurdles and Mitigations

### H1: Annotation Workload

**Problem:** There are ~200 Enterprise ATT&CK techniques. Manually annotating dependencies for all of them is time-consuming.  
**Mitigation:** Prioritise by `campaign_count`. The top 50 techniques by campaign usage likely cover >80% of observed adversary behaviour. Start there. The tool should display annotation coverage so progress is visible. Accept partial coverage for the PoC.

### H2: ATT&CK Tactics Are Not Strictly Ordered

**Problem:** MITRE explicitly states tactics are unordered. Adversaries may execute Discovery before or after Execution.  
**Mitigation:** Tactic ordering is used only for **layer placement** (visual layout), not for edge generation. Edges come from evidence. If evidence shows Discovery preceding Execution in some context, that edge is valid regardless of layer positions.

### H3: No Ground-Truth Dependency Dataset

**Problem:** No authoritative dataset labels all technique-to-technique dependencies.  
**Mitigation:** The graph is an informed approximation, built from the best available evidence. Acknowledge this limitation in the thesis. The evidence-first design (D6) makes the approximation transparent and improvable.

### H4: Multi-Tactic Techniques

**Problem:** Some techniques map to 2+ tactics (e.g., T1548 maps to Privilege Escalation and Defense Evasion). Assigning to one layer loses information.  
**Mitigation:** Assign to earliest layer, store all tactic memberships. A future iteration could create duplicate nodes (one per tactic), connected by an internal edge. For now, the metadata preserves the information even if the visual position is simplified.

### H5: Backward Edges and Cycles

**Problem:** Lateral Movement -> Discovery -> Lateral Movement is a natural adversary loop but creates a cycle.  
**Mitigation:** The graph permits backward edges but flags them. If a cycle forms, remove the weakest-evidence backward edge. The simulator can handle acyclic traversal with explicit "repeat" semantics for backward edges.

---

## 9. Integration with MTD Simulator

The GAP feeds into the simulator's adversary module (extending Zhang (2022) and Ho (2024)'s theses). The current simulator models attacks via a CKC action flow (Scan Host -> Enum Host -> Exploit -> ...). The GAP replaces this with a richer, technique-level model:

1. **Technique selection:** At each step, the adversary picks a successor technique from the GAP, conditioned on what has already been executed and the current network state.
2. **Attack sophistication:** The subgraph of techniques reachable from the adversary's current position determines their capability. Different entry points (e.g., Phishing vs. Exploit Public-Facing Application) lead to different traversal paths.
3. **MTD interaction:** Each technique maps to digital artifacts (per Kim et al.'s Table 1). When an MTD operation changes an artifact, techniques targeting that artifact are disrupted. The GAP tells the simulator which techniques are affected at each attack phase.
4. **Future: campaign-specific subgraphs.** The global GAP can be filtered to only the techniques used by a specific campaign/group, producing a campaign-specific attack profile. This is a view over the same graph, not a separate construction.

---

## 10. First Iteration Deliverables

1. **STIX parser** (`stix_parser.py`): Extracts all techniques, campaigns, groups, and relationships from the Enterprise ATT&CK STIX bundle. Outputs the layered node set as JSON.
2. **Structured edge importer** (`edge_importer.py`): Imports edges from Attack Flow corpus and Syed et al. Caldera sequences. Outputs edges as JSON with evidence records.
3. **Manual annotation format**: A simple CSV/JSON schema for hand-recorded edges: `(source_id, target_id, evidence_url, note)`. Loaded by the graph builder alongside automated imports.
4. **Graph builder** (`gap_builder.py`): Combines nodes and edges into the `GeneralisedAttackProfile`. Performs validation (cycle detection, orphan identification, coverage reporting).
5. **Visualisation/traversal tool**: Interactive HTML (via pyvis or similar) allowing node inspection, path highlighting, layer filtering, and coverage display.
6. **JSON export**: The complete GAP in node-link JSON, consumable by the MTD simulator.

**Annotation target for first iteration:** Edges for the top 30 techniques by campaign_count, plus all edges importable from Attack Flow and Caldera datasets.

---

## 11. Future Work (Out of Scope for First Iteration)

As identified by the supervisor:

- **Technique clustering:** Group similar techniques into higher-level "modules" for the `APTAttacker` simulator class. E.g., multiple Credential Access techniques collapse into a single "Credential Harvesting" module.
- **Edge weighting:** Assign probabilities to edges based on co-occurrence frequency across campaigns. Enables probabilistic traversal in the simulator.
- **Blockers:** Model techniques that block or invalidate other techniques (e.g., an MTD operation that invalidates a Persistence technique). Requires bidirectional interaction between the GAP and the MTD module.
- **Automated CTI extraction:** NLP pipeline to parse vendor reports and extract technique ordering. Would dramatically accelerate the annotation step.
- **Sub-technique granularity:** Expand nodes to sub-technique level where campaign data supports it.

---

## References

- Kim, M. et al. (2026). MTD in depth: Multi-phased moving target defense techniques against cyber-attacks based on cyber kill chain. *Future Generation Computer Systems*, 181, 108419.
- Syed, A. et al. (2025). Comprehensive Advanced Persistent Threats Dataset. *IEEE Networking Letters*, 7(2), 150-154.
- Che Mat, N.I. et al. (2024). A systematic literature review on advanced persistent threat behaviors and its detection strategy. *Journal of Cybersecurity*, 10(1), tyad023.
- Selmanaj, D. (2024). *Adversary Emulation with MITRE ATT&CK*. O'Reilly Media.
- MITRE. (2025). MITRE ATT&CK Framework. https://attack.mitre.org/
- MITRE CTID. (2024). Attack Flow. https://center-for-threat-informed-defense.github.io/attack-flow/