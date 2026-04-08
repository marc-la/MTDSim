# Attack Graph Design Schema — v0.1 (First Iteration)

   ---

## 1. Purpose and Scope

This document defines the design schema for constructing **Generalised Attack Profiles (GAPs)** from MITRE ATT&CK campaign data. A GAP is a directed acyclic graph (DAG) that encodes the technique-level progression of real-world adversary campaigns, to be consumed by the MTD simulator as the adversary module's behaviour model.

**Central question this graph must answer:** Given a set of MITRE ATT&CK techniques observed in real campaigns, what ordering and dependency relationships exist between those techniques, and how can these be aggregated across multiple campaigns into a single, generalised attack profile?

**Scope (Proof of Concept):**
- Enterprise ATT&CK matrix only (not Mobile, not ICS).
- Campaigns and Groups as the unit of extraction (not Software objects).
- First iteration targets structural correctness; probabilistic weighting is a stretch goal.

---

## 2. Core Design Problem: Deriving Edges

MITRE ATT&CK's data model records that a campaign **uses** a set of techniques. It does **not** natively encode ordering or dependencies between those techniques. The ATT&CK matrix organises techniques under **Tactics** (columns), which represent the adversary's tactical goal at each phase, but tactics are explicitly unordered in the framework's design — unlike the Cyber Kill Chain which imposes a strict sequence.

The fundamental challenge is therefore: **how do you produce directed edges (precondition to postcondition) between technique nodes when the source data provides only set membership?**

### 2.1 Edge Derivation Strategy: Layered Approach

We propose a three-tier strategy, each tier adding fidelity but also complexity. The first iteration should implement Tier 1 fully and Tier 2 partially.

#### Tier 1 — Tactic-Ordering Heuristic (Structural)

Impose a partial order on techniques via their parent tactic, using the canonical ATT&CK tactic ordering as a **proxy for temporal progression**:

```
Reconnaissance -> Resource Development -> Initial Access -> Execution ->
Persistence -> Privilege Escalation -> Defense Evasion -> Credential Access ->
Discovery -> Lateral Movement -> Collection -> Command and Control ->
Exfiltration -> Impact
```

**Edge rule:** For any two techniques T_a and T_b in the same campaign, if tactic(T_a) precedes tactic(T_b) in the ordering above, create a directed edge T_a -> T_b.

**Justification:**
- Kim et al. (2026) explicitly map ATT&CK techniques to CKC phases and use this ordering to evaluate multi-phase MTD effectiveness (Table 2, Table 3 of MTDID paper). Their mapping demonstrates that tactic ordering is a defensible proxy for attack phase ordering.
- Che Mat et al. (2024) construct Table 5 which maps 18 APT groups' TTPs to CKC phases, confirming that real campaigns follow a broadly sequential tactic progression.
- Syed et al. (2025) build Caldera adversary profiles as "a sequence of abilities that form a cybersecurity kill chain" — their APT41 profile (Fig. 4) demonstrates sequential technique execution ordered by tactic.

**Limitation:** Techniques within the **same tactic** have no inherent ordering. For intra-tactic ordering, see Tier 2.

**Handling multi-tactic techniques:** Some techniques belong to multiple tactics (e.g., T1059 Command and Scripting Interpreter maps to Execution). Use the **earliest** tactic in the ordering as the node's position. This is a simplification; a future iteration could duplicate nodes per tactic.

#### Tier 2 — CTI Narrative Extraction (Semantic)

Supplement Tier 1 edges with explicit sequencing extracted from campaign documentation:

**Primary sources (ordered by authority):**
1. **MITRE ATT&CK Campaign descriptions** — The `description` field of each Campaign STIX object often contains temporal language ("after gaining initial access, the group used...", "the actor then deployed..."). Parse for ordering cues.
2. **MITRE ATT&CK Attack Flow Corpus** — MITRE's own Attack Flow project (https://center-for-threat-informed-defense.github.io/attack-flow/) provides machine-readable JSON flows for select campaigns. Where available, these are authoritative.
3. **CTI vendor reports** — Palo Alto Unit 42, Mandiant/Google TAG, CrowdStrike, Recorded Future, Akamai. These provide narrative attack chains. Use only for campaigns already in ATT&CK to maintain provenance.
4. **Syed et al. (2025) adversary profiles** — Their Caldera ability sequences (Table II) for 12 APTs provide explicit, reproducible technique orderings for 23 campaigns.

**Edge extraction from narratives:** For this iteration, manual extraction is acceptable. The process:
1. For each campaign, read the ATT&CK description and any linked CTI report.
2. Identify temporal/causal language ("after", "then", "following", "once X was achieved", "leveraging Y to Z").
3. Record explicit pairwise dependencies: (T_source, T_target, evidence_url).
4. Where narrative evidence contradicts tactic ordering, **prefer the narrative** (Tier 2 overrides Tier 1).

**Justification:** Che Mat et al. (2024) identify that the primary gap in APT detection research is the lack of correlation between attack traces and multi-stage models. Their proposed Module 2 (Alert Correlation) directly requires understanding technique sequencing. Manual CTI extraction, while costly, produces the highest-fidelity edges.

#### Tier 3 — Co-occurrence Frequency (Statistical, Stretch Goal)

Across all campaigns, count how often technique T_a and T_b co-occur with T_a's tactic preceding T_b's. Weight edges by normalised co-occurrence frequency. This produces a probabilistic attack graph. **Deferred to future iteration.**

---

## 3. Graph Schema

### 3.1 Node Definition

Each node represents a single ATT&CK **Technique** (or Sub-technique) instance within the graph.

```python
@dataclass
class TechniqueNode:
    technique_id: str          # e.g., "T1059.001"
    technique_name: str        # e.g., "PowerShell"
    tactic: str                # Primary tactic, e.g., "execution"
    tactic_order: int          # Position in canonical ordering (0-13)
    platforms: list[str]       # ["Windows", "Linux", ...]
    
    # Aggregation metadata
    campaign_count: int        # Number of campaigns using this technique
    campaign_ids: list[str]    # MITRE Campaign IDs (e.g., ["C0015", "C0018"])
    group_ids: list[str]       # Associated MITRE Group IDs
```

**Design choice — Technique, not Sub-technique as default granularity:** Sub-techniques provide more detail but fragment the graph. For this PoC, use techniques as nodes. Where a campaign's STIX data specifies sub-techniques, store them but collapse to parent technique for graph construction. This can be toggled.

### 3.2 Edge Definition

Each edge represents a **precondition relationship**: the source technique enables, facilitates, or temporally precedes the target technique.

```python
@dataclass
class DependencyEdge:
    source_id: str             # Technique ID of precondition
    target_id: str             # Technique ID of postcondition
    edge_type: str             # "tactic_order" | "narrative" | "co_occurrence"
    weight: float              # 0.0-1.0, normalised confidence/frequency
    evidence: list[str]        # URLs or STIX IDs justifying this edge
    campaigns: list[str]       # Campaign IDs where this transition is observed
```

**Edge types explained:**

| Type | Source | Confidence | First Iteration? |
|------|--------|-----------|-----------------|
| `tactic_order` | Canonical ATT&CK tactic sequence | Medium — structural assumption | Yes |
| `narrative` | CTI report / ATT&CK description / Attack Flow | High — explicitly documented | Yes (partial) |
| `co_occurrence` | Statistical aggregation across campaigns | Low-Medium — correlational | No (stretch) |

**Edge reduction rule:** Between techniques in the same tactic (same `tactic_order`), no `tactic_order` edge is created. Only `narrative` edges can connect intra-tactic techniques.

**Transitive reduction:** After construction, apply transitive reduction to remove redundant edges (if A->B and B->C exist, remove A->C unless A->C has independent `narrative` evidence). This keeps the graph interpretable.

### 3.3 Graph-Level Structure

```python
@dataclass
class AttackProfile:
    profile_id: str            # Unique identifier
    name: str                  # e.g., "Generalised_APT41"
    source_campaigns: list[str]
    source_groups: list[str]
    nodes: dict[str, TechniqueNode]
    edges: list[DependencyEdge]
    
    # Structural properties
    entry_nodes: list[str]     # Nodes with in-degree 0 (typically Recon/Initial Access)
    objective_nodes: list[str] # Nodes with out-degree 0 (typically Exfiltration/Impact)
```

The graph is a **DAG** (directed acyclic graph). Cycles should not exist given tactic ordering; if Tier 2 narrative extraction produces a cycle, flag for manual review.

---

## 4. Data Sources and Extraction Pipeline

### 4.1 Primary Data: MITRE ATT&CK STIX Bundle

**Source:** https://github.com/mitre/cti (Enterprise ATT&CK STIX 2.1 JSON)

**Relevant STIX objects:**

| Object Type | Use |
|-------------|-----|
| `attack-pattern` | Techniques — nodes of the graph |
| `campaign` | Campaigns — grouping unit for technique sets |
| `intrusion-set` | Groups (APT names) — links campaigns to threat actors |
| `relationship` (type: `uses`) | Campaign->Technique and Group->Technique mappings |

**Extraction steps:**
1. Parse `enterprise-attack.json` STIX bundle.
2. For each `campaign` object, collect all `relationship` objects where `source_ref` matches the campaign and `relationship_type == "uses"` and `target_ref` is an `attack-pattern`.
3. Resolve technique IDs and tactic assignments from `attack-pattern` objects (via `kill_chain_phases`).
4. Build per-campaign technique sets.

### 4.2 Secondary Data: Attack Flow Corpus

**Source:** https://github.com/center-for-threat-informed-defense/attack-flow

Machine-readable JSON flows that explicitly encode technique ordering. Where a campaign in our dataset has a corresponding Attack Flow, import its edges directly as `narrative`-type edges with high confidence.

### 4.3 Tertiary Data: CTI Reports

For campaigns where Attack Flows don't exist, manually extract ordering from:
- The `description` field of the MITRE Campaign STIX object.
- Linked external references (typically vendor blog posts).
- Syed et al. (2025) Caldera profiles for APT41, APT39, APT32, APT10, APT28, APT5, Aquatic Panda, APT3, Windshift, Dragonfly, APT29, APT35 (Table II).

### 4.4 Supplementary: Selmanaj (2024)

Selmanaj's *Adversary Emulation with MITRE ATT&CK* provides worked examples of building emulation plans from ATT&CK data. Use as methodological reference for how practitioners sequence techniques into coherent attack plans. Not a direct data source but validates the tactic-ordering heuristic.

---

## 5. Graph Construction Algorithm

```
ALGORITHM: BuildAttackProfile(campaign_ids)

INPUT:  Set of MITRE Campaign IDs
OUTPUT: AttackProfile (DAG)

1. EXTRACT technique sets per campaign from STIX data (Section 4.1)
2. UNION all techniques into a single node set
3. For each node, set tactic_order from canonical ordering
4. GENERATE Tier 1 edges:
   For each pair (T_a, T_b) where tactic_order(T_a) < tactic_order(T_b)
   AND at least one campaign contains both T_a and T_b:
       Create edge(T_a, T_b, type="tactic_order",
                   weight=co_occurrence_count / total_campaigns)
5. IMPORT Tier 2 edges:
   For each narrative/Attack Flow dependency (T_a, T_b):
       If edge(T_a, T_b) already exists:
           upgrade type to "narrative", increase weight
       Else:
           create edge(T_a, T_b, type="narrative", weight=1.0)
6. APPLY transitive reduction to tactic_order edges
   (preserve all narrative edges regardless)
7. IDENTIFY entry_nodes (in-degree == 0) and
   objective_nodes (out-degree == 0)
8. VALIDATE: assert graph is acyclic
9. RETURN AttackProfile
```

**Step 6 rationale:** Without transitive reduction, the Tier 1 heuristic creates O(n^2) edges (every earlier-tactic technique connects to every later-tactic technique). This is noise. Transitive reduction preserves reachability while minimising edges. The key insight: we want the graph to represent **direct** preconditions, not all possible preconditions.

**Aggregation modes:**

| Mode | Description | Use Case |
|------|-------------|----------|
| Single-campaign | Build graph from one campaign's techniques | Testing a specific APT scenario |
| Group-aggregate | Union techniques across all campaigns of one APT group | Modelling a specific threat actor |
| Cross-group aggregate | Union techniques across selected groups | Building a generalised attack profile |

---

## 6. Rendering and Visualisation

### 6.1 Layout Strategy

Use a **layered/hierarchical layout** (e.g., Sugiyama) where layers correspond to tactics. This naturally maps to the CKC-style left-to-right progression that Kim et al. (2026) use in their evaluation (Table 3) and that Syed et al. (2025) use for their attack path diagrams (Fig. 4).

### 6.2 Implementation

- **Graph library:** NetworkX (Python) for construction and analysis.
- **Serialisation:** Export as JSON (node-link format) for simulator consumption. Optionally export as STIX 2.1 for interoperability.
- **Visualisation:** Graphviz DOT format via `networkx.drawing.nx_agraph` for static diagrams. For interactive exploration, export to D3.js or use `pyvis`.

### 6.3 Colour Coding

Nodes coloured by tactic category for quick visual identification. Edges coloured by `edge_type` (blue = tactic_order, red = narrative, grey = co_occurrence).

---

## 7. Design Decisions and Justifications

### D1: DAG, not a Tree

**Choice:** Directed Acyclic Graph rather than a strict tree.  
**Why:** Attack trees (as reviewed by Che Mat et al. referencing Lallie et al.) impose a single-root constraint and AND/OR decomposition that doesn't match our data model. Real campaigns have multiple parallel technique chains that converge (e.g., both Discovery and Credential Access feed into Lateral Movement). A DAG naturally captures this fan-in/fan-out structure.

### D2: Tactic Ordering as Primary Heuristic

**Choice:** Use canonical ATT&CK tactic order rather than CKC phases.  
**Why:** ATT&CK has 14 tactics with finer granularity than CKC's 7 phases. Kim et al. (2026, Table 2) already provide a mapping from ATT&CK techniques to CKC phases, confirming the approaches are compatible. Using ATT&CK tactics directly avoids the lossy CKC mapping step and preserves more ordering information.

### D3: Techniques (not Sub-techniques) as Default Granularity

**Choice:** Collapse sub-techniques to parent techniques.  
**Why:** Campaign STIX data is inconsistent in sub-technique granularity. Some campaigns list T1059 (broad), others T1059.001 (PowerShell). Collapsing avoids fragmentation. Configurable toggle for future iterations.

### D4: Manual Tier 2 Extraction (for now)

**Choice:** Human-in-the-loop for narrative edge extraction.  
**Why:** NLP-based extraction of technique ordering from CTI text is an open research problem (Che Mat et al. cite Husari et al.'s TTPDrill as one attempt). For a PoC, manual extraction from a bounded set of campaigns is more reliable. Syed et al.'s Caldera profiles for 12 APTs provide ready-made sequencing data that bypasses NLP entirely.

### D5: Transitive Reduction

**Choice:** Apply transitive reduction to structural edges.  
**Why:** Without it, a campaign using techniques from 5 different tactics produces 10 edges from the Tier 1 heuristic alone. Most are redundant. Kim et al. evaluate MTD against CKC **phases** (not every pairwise phase combination), implicitly assuming only adjacent-phase transitions matter. Transitive reduction formalises this.

---

## 8. Known Hurdles and Mitigations

### H1: ATT&CK Tactics Are Not Strictly Ordered

**Problem:** MITRE explicitly states tactics are unordered. Some techniques span multiple tactics. Adversaries may loop back (e.g., Discovery after Lateral Movement).  
**Mitigation:** The tactic ordering is treated as a heuristic, not ground truth. Tier 2 narrative edges can override it. For the simulator, the graph provides a **feasible** ordering, not the only possible one. The PoC scope accepts this limitation.

### H2: Sparse Campaign Data

**Problem:** Many MITRE campaigns list only 3-5 techniques, producing trivially small graphs.  
**Mitigation:** Group-level aggregation merges techniques across campaigns for the same threat actor, producing richer graphs. Alternatively, cross-reference with Syed et al.'s dataset which covers 83 techniques across 12 APTs.

### H3: No Ground-Truth Dependency Data

**Problem:** No authoritative dataset exists that labels technique-to-technique dependencies across all ATT&CK campaigns.  
**Mitigation:** This is fundamentally why we use the layered approach (Tier 1 + Tier 2). Acknowledge in the thesis that the graph represents an **informed approximation** of adversary behaviour, validated against CTI narratives where available.

### H4: Graph Explosion in Cross-Group Aggregation

**Problem:** Aggregating many groups produces a dense graph where every technique connects to many others.  
**Mitigation:** Filter by minimum campaign co-occurrence threshold (e.g., edge only if both techniques appear in >= 2 campaigns). Apply transitive reduction aggressively.

---

## 9. Integration with MTD Simulator

The output `AttackProfile` feeds into the simulator's adversary module (as described in Zhang (2022) and Ho (2024)'s theses). The simulator currently models attack operations via a CKC-based action flow (Scan Host -> Enum Host -> Exploit -> ...). The GAP graph provides:

1. **Technique selection:** At each step, the adversary selects the next technique from available successors in the DAG, conditioned on current compromised state.
2. **Attack sophistication parameter:** The number and breadth of techniques in the profile determines the adversary's capability level.
3. **MTD interaction:** Each technique node can be mapped to the digital artifacts it targets (per Kim et al.'s Table 1), enabling the MTD module to determine which defences are relevant at each attack phase.

---

## 10. First Iteration Deliverables

1. **Python module** (`attack_graph.py`) implementing `BuildAttackProfile` algorithm.
2. **STIX parser** extracting campaign->technique relationships from Enterprise ATT&CK bundle.
3. **Manual edge annotations** for >= 3 campaigns (e.g., APT41, APT29, APT28) using Syed et al. and CTI reports.
4. **Rendered graph visualisations** for the annotated campaigns.
5. **JSON export format** consumable by the MTD simulator.

---

## References

- Kim, M. et al. (2026). MTD in depth: Multi-phased moving target defense techniques against cyber-attacks based on cyber kill chain. *Future Generation Computer Systems*, 181, 108419.
- Syed, A. et al. (2025). Comprehensive Advanced Persistent Threats Dataset. *IEEE Networking Letters*, 7(2), 150-154.
- Che Mat, N.I. et al. (2024). A systematic literature review on advanced persistent threat behaviors and its detection strategy. *Journal of Cybersecurity*, 10(1), tyad023.
- Selmanaj, D. (2024). *Adversary Emulation with MITRE ATT&CK*. O'Reilly Media.
- MITRE. (2025). MITRE ATT&CK Framework. https://attack.mitre.org/
- MITRE CTID. (2024). Attack Flow. https://center-for-threat-informed-defense.github.io/attack-flow/