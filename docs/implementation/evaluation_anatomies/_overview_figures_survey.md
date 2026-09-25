---
status: durable
created: 2026-09-25
updated: 2026-09-25
---

# Overview figures: how the corpus draws the one figure that shows the whole method

Purpose: the evidence base for critiquing this dissertation's own method-overview figure
(threat-intelligence reports → attack graph → attack profiles → Petri nets → joined to
MTDSim → evaluation metrics). One block per paper, recording how that paper draws its
method-overview / framework / pipeline figure. A paper with no such figure gets one line.

Sources read: the PDFs in `docs/sources/lit_review/original/` and three in
`docs/sources/methodology/`, with captions and naming words checked against the Markdown
conversions in `docs/sources/lit_review/*.md` and `docs/sources/methodology/*.md`. Every
figure below was rendered and viewed (Ghostscript to PNG); nothing is recorded from the
caption alone. Locators are PDF page numbers ("p.N"); a printed page number that differs
is given as "printed N". Box counts are counted from the render. Word counts are caption
words, figure label excluded.

Record first, judgement second: sections 1–2 record what each figure does; the
"Borrow / avoid" line in each block and section 3 are the only evaluative parts.

## 1. Per-paper records: papers with a method-overview figure

### 2.4_zhang2025attackg+ — AttacKG+ (Computers & Security 2025)

- **Figure:** Fig. 3, p.4.
- **Shows:** the four LLM modules that turn a CTI report into the AttacKG+ knowledge graph, with the output graph drawn top right.
- **Top-level boxes:** 5 panels (Rewriter, Parser, Identifier, Summarizer, plus an output panel "Attack Knowledge Graph Construction-AttacKG+"). Nested: yes. Every module panel holds an LLM box, an external template box and an artefact card.
- **Box type:** mixed. Modules are named by role nouns (Rewriter, Parser) *and* by numbered task phrases at the panel foot ("1.Cyber threat intelligence tactical rewrite", "2.Cyber threat behavior extraction" …). Inside the panels are systems (LLM), external resources (MITRE, STIX, D3FEND logos) and artefacts (Behavior Graph, TTP Labels, State Summary).
- **Arrows:** several meanings, all drawn in the same black style with no labels: data flow (report → LLM → sections), knowledge input (template → LLM, drawn upward), a broadcast bus (the rewritten sections feed all three lower modules), and assembly (State Summary → output panel). A dashed arrow inside the graph glyphs means "temporal relation", and it is decoded only in Fig. 1's legend.
- **Mixed abstraction:** yes. Example data sits inside the overview: tactic bars ("Persistence"), technique IDs ("T1176"), P/F/T/I state chips and behaviour-graph glyphs. The output panel repeats Fig. 1's schema in miniature.
- **Naming word:** "components" in the caption; "modules" in the text ("four consecutive modules", md L28; "four modules", md L62). So the figure and its text use two words for the same parts.
- **External system:** the LLM is drawn *inside* every module and carries a snowflake icon that neither the caption nor the text explains. MITRE/STIX/D3FEND appear as side input boxes with their logos.
- **Whole-method input/output:** both are shown (CTI Report icon, AttacKG+ panel).
- **Caption:** 55 words. It lists the four components with a clause of function for each. It decodes the parts but does not state results.
- **Colour/encoding:** green LLM, pastel artefact cards, red/amber tactic and technique bars, blue/grey state chips, green and red triangles. The legend lives in Fig. 1 (p.3), not in this figure, so Fig. 3 needs a legend it does not carry.
- **Borrow / avoid:** avoid. It is the corpus's densest overview: example data, logos, an undecoded icon and four unlabelled arrow meanings. The one thing worth borrowing is the separate legended schema figure (Fig. 1), which does carry an arrow legend with three relation types.

### 2.4_rodriguez2024process — process-mining attacker profiling

- **Figure:** Figure 1, p.4.
- **Shows:** the four-step method from running attacks to reading attacker patterns.
- **Top-level boxes:** 4 step headers (Enactment, Extraction, Discovery, Analysis). Nested: one card under each header holding an icon and a label: "System under attack"; "Sysmon & Zircolite" + "Event log"; "ProM" + "Process model"; "Patterns of attackers' behavior".
- **Box type:** headers are processes (named activities). Cards are tools and artefacts, the same kind in every step.
- **Arrows:** 3 grey block arrows, one meaning: next step.
- **Mixed abstraction:** no. Each step is drawn at the same depth (one card of tool/artefact).
- **Naming word:** "step": "consists of four steps that follow the standard PM methodology" (md L97); "Step 1: Enactment" as section headings (md L209, L523). "phase" also appears once (md L504).
- **External system:** the system under attack is the content of the first step (Enactment). The environment is drawn as a step.
- **Whole-method input/output:** there is no explicit input. The output ("Patterns of attackers' behavior") sits inside the last step.
- **Caption:** 2 words ("Proposed method"). It says only what the figure is.
- **Colour/encoding:** slate headers, grey cards, monochrome icons. No legend needed.
- **Borrow / avoid:** borrow the two-tier step card, with the process name as the header and the product or tool on the card beneath. It names both the verb and the noun at one uniform depth. Avoid putting the environment in as step 1.

### 2.4_ferraz2024procedural — CTI to executable adversary emulation

- **Figure:** Figure 2, p.6 (the method overview). Figure 1, p.2, is a positioning figure and is recorded below.
- **Shows:** three stages turning structured CTI into executable adversary emulation.
- **Top-level boxes:** 5 hexagons: input "Structured CTI", "Stage 1: Structural Modeling", "Stage 2: Technique Translation", "Stage 3: Emulation Integration", and output "Executable Adversary Emulation". Nested: no. A header row above the hexagons gives each one a verb phrase: "CTI entities in STIX", "Normalize into behavioral graph", "Translate missing procedure", "Package and orchestrate", "Reproducible emulation".
- **Box type:** stages are processes (noun-phrase names); the ends are artefacts. The header row puts the verb phrases above the names.
- **Arrows:** 4, one meaning: feeds the next stage.
- **Mixed abstraction:** no. Emphasis comes from colour, not detail: Stage 2 is red and flagged "procedural semantics gap"; Stages 1 and 3 are tagged "Automated".
- **Naming word:** "stage": "Figure 2 illustrates the three conceptual stages. Stage 1 performs…" (md L145); section headings "Stage 3: Emulation Integration" (p.6).
- **External system:** the emulation platform (Caldera) and the Docker SUT are not drawn. They are implied by Stage 3 and the output.
- **Whole-method input/output:** both are shown, and colour sets them apart (blue input, green output).
- **Caption:** 9 words ("Three-stage methodology from descriptive CTI to executable multi-stage emulation."). It says what the figure is and names the input and output.
- **Colour/encoding:** four colours with fixed roles (input, automated stage, gap stage, output). Each is labelled in place, so no legend is needed.
- **Borrow / avoid:** borrow. It is the nearest match to this thesis in content (CTI → executable attacker behaviour on a platform). It uses one arrow meaning, input and output as distinct end shapes, a verb row over the names, colour to mark the one stage that matters, and a 9-word caption.

  *Figure 1, p.2 (positioning, not overview).* Two panels, "PRIOR EMULATION MODEL" (3 boxes) and "TRANSLATION BOUNDARY" (4 boxes: ATT&CK-in-STIX → Technique Translation Layer → SUT Binding → Executable Workflow), plus three red gap tags. The SUT appears as a step in the chain ("SUT Binding"). The caption is 27 words and states the paper's argument ("provides behavioral grounding, but not procedural executability"). It uses a coined term, "procedural semantics gap". So it is a claim figure rather than an overview.

### 2.4_rahman2024mining — ChronoCTI (IEEE TSE)

- **Figure:** Fig. 2, p.4.
- **Shows:** the methodology as an indented outline: RQ → steps → sub-steps, with what each produces.
- **Top-level boxes:** 2 RQ bands; 4 step boxes (S1, S2 under RQ1; S3A, S3B under RQ2); 7 sub-step boxes (S1A–S1D, S2A–S2C). Right-hand braces group them as "Constructing ChronoCTI" and "Applying ChronoCTI".
- **Box type:** processes, each a full verb phrase ("S1: Identify APT attack actions from OSCTI reports").
- **Arrows:** none. Order comes from vertical position and the S-numbering.
- **Mixed abstraction:** the outline is at one depth, but a right-hand column gives each sub-step's output with numbers ("713 OSCTI reports", "11,106 examples mapped to 120 ATT&CK techniques", "Nine categories"). Those numbers are results placed inside the method figure.
- **Naming word:** "step" / "sub-step": "RQ1 consists of two steps. The first step is S1…"; "the sub-steps of S1 and S2" (md L57). "the corresponding output from each step" (md L55).
- **External system:** none drawn (no platform). ATT&CK appears only as an output annotation ("193 MITRE ATT&CK").
- **Whole-method input/output:** framed by the RQs rather than by data. Per-step outputs are in the right column.
- **Caption:** 5 words ("Methodology for RQ1 and RQ2").
- **Colour/encoding:** greys only. No legend.
- **Borrow / avoid:** borrow the per-step output column (what each stage produces, named beside it) but without result numbers. Avoid the arrowless outline for a pipeline whose point is the hand-off between artefacts.

### 3.2_kim2026mtdid — MTD in Depth (FGCS 2026)

- **Figure:** Fig. 1, p.3.
- **Shows:** the paper's three research activities in order.
- **Top-level boxes:** 3 ("Propose a conceptual framework (MTD in Depth)", "Design system, attack, and defense models for case studies", "Evaluate performance and security"). Nested: no.
- **Box type:** processes, as imperative verb phrases.
- **Arrows:** 2, one meaning: then.
- **Mixed abstraction:** no.
- **Naming word:** none. The text walks the boxes as "We first outline… Second, we design… Lastly, we assess" (p.3) and gives bold-italic run-in heads ("MTD in Depth:", "Proposed Model for Case Study:", "Evaluation:").
- **External system:** the SDN testbed is not drawn. It gets its own figure (Fig. 4, p.7).
- **Whole-method input/output:** not shown.
- **Caption:** 3 words ("Our proposed approach.").
- **Colour/encoding:** none.
- **Borrow / avoid:** it is the floor of the genre: a three-box research-activity chain with a 3-word caption. It is readable but carries no artefacts. Borrow the practice of putting the testbed in its own figure rather than in the overview.

### 3.2_he2025MTD-AD — MTD-AD (IEEE TIFS)

- **Figure:** Fig. 2, p.5 (printed 5051).
- **Shows:** training (generate and filter mutated detectors) and execution (random model selection per packet batch).
- **Top-level boxes:** 2 dashed containers (Training, Execution). Training nests 2 solid sub-containers (Model Generation, Model Evaluation). There are 13 leaf elements, including a decision diamond ("Meets Criteria", with Yes/No branches).
- **Box type:** mixed: artefacts (Target NIDS, MTDAD Pool, Incoming Packet Features, Output Decision), processes (three Mutations, Evaluate, Discard, Keep) and a component (Model Selector).
- **Arrows:** several meanings, none labelled apart from Yes/No: data flow, control branch, membership (Keep → Pool), selection (Pool → Selector → Chosen Model) and input.
- **Mixed abstraction:** yes. A flowchart decision diamond sits inside the overview.
- **Naming word:** "stage" and "phase": "The training stage of MTD-AD comprises two main phases: model generation and model evaluation" (p.5); "key components of MTD-AD" (p.5).
- **External system:** the defended NIDS (Kitsune) is the first box ("Target NIDS"). The testbed is not drawn; it has its own figure (Fig. 3).
- **Whole-method input/output:** both are shown (Target NIDS; Output Decision).
- **Caption:** 68 words. It narrates the three numbered steps and states a parameter value ("after processing 1,000 packets") and the abbreviation "FPR".
- **Colour/encoding:** blue for training, green for execution, each labelled by its container title. No legend needed.
- **Borrow / avoid:** borrow the two containers labelled by *when* they happen (build-time vs run-time). That maps onto this thesis's build pipeline vs the simulated run. Avoid the flowchart diamond and the narrating caption.

### 1.3_tay2024using — MTDShield (GENG5512 report, lineage)

- **Figure:** Figure 1, p.13 (printed 13).
- **Shows:** the existing simulator and the added MTDShield plugin, with the loop between them.
- **Top-level boxes:** 2 rounded containers ("System", green; "MTDShield", orange). Nested: 3 boxes in System ((a) Attacker Operations, (b) Network, (c) MTD Operations) and 5 in MTDShield ((d) Feature Extraction Module, (e) Time-Series Analysis Module, (f) Feature Fusion Module, (g) Q-Network Output Layer, (h) Action Selection).
- **Box type:** components (nouns).
- **Arrows:** labelled, several meanings: interactions ("Compromise Hosts", "Reconfigure Network", "Interrupt Attack Actions"), data ("Network Security Metrics", "Static Features", "Temporal Features", "Combined Features", "Processed Features", "Q-Values for Actions") and control ("Selected MTD Action").
- **Mixed abstraction:** yes. The simulator gets 3 boxes; the plugin is drawn down to neural-network layer level ("Q-Network Output Layer").
- **Naming word:** "components" / "module" / "plugin": "three main components: the Network Module (b), MTD module (c) and Attacker module (a)"; "the MTDShield plugin" (p.13).
- **External system:** the simulator is a surrounding container. The new part is a sibling container, and a closed loop joins them. The simulator is not drawn as a step.
- **Whole-method input/output:** not shown (closed loop).
- **Caption:** 5 words ("Overview of MTDShield System Architecture").
- **Colour/encoding:** green = existing simulator, orange = new plugin. This is decoded in the body text ("highlighted in green", "highlighted in orange", p.13), not in the caption. Letters (a)–(h) serve as text anchors.
- **Borrow / avoid:** borrow simulator-as-container, new-part-as-sibling, with an existing/new colour split. It is the lineage precedent for drawing "joined to MTDSim". Avoid drawing the new part in more detail than the old.

### GENG5512Report_Zhang_22792191 — MTDSimTime (lineage)

- **Figure:** Figure 1, p.20 (printed 19).
- **Shows:** how MTD and adversary act on the simulated network.
- **Top-level boxes:** 5, flat (MTD Techniques, MTD Operation, Simulated Network, Attack Operation, Adversary).
- **Box type:** a mix of modules (nouns: MTD Techniques, Simulated Network, Adversary) and operations (process nouns: MTD Operation, Attack Operation).
- **Arrows:** partly labelled, several meanings: "Retrieve / Release Resource for reconfiguration", "Discover / Compromise hosts" (both double-headed), "Interrupt attack actions". Two arrows are unlabelled (MTD Techniques → MTD Operation; Adversary → Attack Operation), and the text reads them as "conduct" and "launch".
- **Mixed abstraction:** mild (modules and operations at one level).
- **Naming word:** "modules": "comprises three key modules: Simulated Network, MTD Techniques, and Adversary, as illustrated in Figure 1" (md L262). The figure draws five boxes, so text and figure disagree on the count of parts.
- **External system:** the figure *is* the simulator.
- **Whole-method input/output:** not shown.
- **Caption:** 4 words ("The Structure of MTDSimTime").
- **Colour/encoding:** blue defence side, red attack side, green network. No legend and no decoding.
- **Borrow / avoid:** avoid letting the count of drawn boxes and the count the text announces differ.

### GENG5512Report_Ho_22701889 — MTD AI (lineage)

- **Figure:** Figure 1, p.14 (printed 13).
- **Shows:** the AI engine and the MTD simulator, and the two signals between them.
- **Top-level boxes:** an outer frame titled "System Overview" holding 2 containers ("MTD simulator", "AI Engine"). Nested: 3 boxes in the simulator (Attack Operations, Network, MTD Operations) and 2 in the engine (Training Data, Model).
- **Box type:** components and one artefact (Training Data).
- **Arrows:** mixed. Three unlabelled arrows form a cycle inside the simulator; two are labelled between containers ("Network Metrics", "MTD Selection"); Training Data → Model is unlabelled (it means "trains").
- **Mixed abstraction:** mild. It is the inverse of Tay: the new part is drawn coarser than the simulator.
- **Naming word:** "system consists of the AI engine and the MTD simulator" (p.14). The simulator is "used as the infrastructure… as a platform" (p.14).
- **External system:** a surrounding container, sibling to the new part (as in Tay).
- **Whole-method input/output:** Training Data is shown as an input; no output.
- **Caption:** 2 words ("System Overview"). It repeats the frame's own title tag inside the figure.
- **Colour/encoding:** pale green simulator, orange Training Data, dark green Model, none of it decoded.
- **Borrow / avoid:** it confirms the container pattern for the simulator. Avoid the redundant in-figure title and colours that carry no meaning.

### methodology/zhuang2012_simulation_mtd — network MTD design scheme

- **Figure:** Figure 3, p.4.
- **Shows:** the adaptation loop between the physical network, two logical models and three engines/tools.
- **Top-level boxes:** about 6: Physical Network, Logical Mission Model (container), Logical Security Model (container), Configuration Manager, Adaptation Engine and MulVAL/SnIPS, plus a "Random" source. Nested: full instance diagrams inside both model containers: a roles/goals graph, and a "Conservative Attack Graph" with named nodes (e.g., "Planner Compromised").
- **Box type:** mixed: systems/tools (red), models (blue containers) and a physical artefact.
- **Arrows:** labelled, several meanings: "reflection", "current state", "security state", "adaptations", "new state", "configuration", "real time events". Inside the models the edges are labelled "assigned", "supports", "value".
- **Mixed abstraction:** yes. It puts worked instance data (named hosts, roles, goals) inside an architecture overview.
- **Naming word:** the figure names "Model", "Engine", "Manager"; the text calls the whole a "design" ("A key concept of our design", p.4).
- **External system:** the third-party tools (MulVAL/SnIPS) sit in the loop as boxes. The physical network is a side box.
- **Whole-method input/output:** not shown.
- **Caption:** 7 words.
- **Colour/encoding:** red for engines, blue for models, orange/green model nodes. Undecoded.
- **Borrow / avoid:** avoid. It shows what happens when the overview also carries the example.

## 2. Papers without a method-overview figure (one line each)

- **2.3_alshamrani2019survey:** a survey with no method overview. Fig. 1, p.3 ("APT attack model.", 3 words) is the object of study, not a method: five boxes, each numbered "Stage 1–5", with one arrow meaning. Its grammar is the plainest linear chain in the corpus.
- **1.2_brown2023evaluating:** no method pipeline. Fig. 1, p.3 ("Overview of the proposed 3-Layer HARM.", 6 words) is three side-by-side model panels with no arrows between them. Fig. 3, p.5, is the attack-procedure flowchart.
- **4_bland2020machine:** no method overview. Fig. 1, p.3 is Sutton and Barto's RL loop (Agent and Environment, with arrows labelled state/reward/action). The environment is a box in the loop.
- **2.4_buechel2025sok:** an SoK with no overview of its own method. Its pipeline figures are generic, one per surveyed family: Fig. 1, p.4 (6 chevron steps, with a worked example sentence drawn above the chevrons) and Fig. 3, p.6 (gLLM pipeline mixing a prompt instance, stores and an LLM box). Captions are 6 words each. Fig. 2, p.5 was not viewed.
- **3.1_jalowski2026rethinking:** a critique with no overview figure. Figs 1–3 illustrate attack vectors and network examples (Fig. 2, p.7).
- **2.1_al-sada2024MITRE:** a survey with no method overview. Fig. 3, p.7 ("ATT&CK, Cyber Kill Chain and STRIDE: Comparison and application scenarios.", 10 words) is an illustrative collage: kill-chain chevrons, clip-art adversary and hosts, ATT&CK matrix thumbnail and STRIDE list.
- **methodology/sengupta2020_survey:** a survey organisation tree, not a method. Fig. 1, p.2 has 15 nodes over 4 levels, arrows mean "divides into", and the 34-word caption states a finding ("a common terminology … naturally emerges").
- **methodology/ward2018_mit_survey:** a taxonomy, not a method. Figure 1, p.14 (printed 2): a layered victim stack with five technique boxes, each arrow meaning "acts on".

## 3. Synthesis

### (a) The modal grammar

The ten method-overview figures fall into two genres, and the genre decides the grammar.

| | Pipeline genre (method papers: Rodriguez F1, Ferraz F2, Rahman F2, Kim F1, AttacKG+ F3, He F2) | Architecture genre (MTDSim lineage + Zhuang: Tay F1, Zhang23 F1, Ho F1, Zhuang F3) |
|---|---|---|
| Layout | left-to-right (or top-down) chain | containers joined in a closed loop |
| Top-level boxes | 3–5 (Kim 3; Ferraz 3 stages + in/out = 5; Rodriguez 4; AttacKG+ 4 + output; He 2 containers / 4 phases) | 2 containers (Tay, Ho) or 5–6 flat boxes (Zhang23, Zhuang) |
| Box type | processes, named as activities or verb phrases; artefacts at the ends or on sub-cards | components (nouns) |
| Arrow semantics | one meaning ("then / feeds") in the clean cases (Rodriguez, Ferraz, Kim); several, unlabelled, in the dense ones (AttacKG+, He) | several meanings, mostly labelled with the signal carried |
| Naming word | "step" (Rodriguez, Rahman), "stage" (Ferraz, He's "training stage"), "phase" (He's sub-parts) | "module" / "component" (Tay, Zhang23, AttacKG+'s text) |
| Caption | 2–9 words in 7 of 10 figures (Rodriguez 2, Ho 2, Kim 3, Zhang23 4, Tay 5, Rahman 5, Zhuang 7, Ferraz 9) and names only what the figure is. The two exceptions decode or narrate (AttacKG+ 55, He 68). | |

The modal overview in this corpus has 3–5 top-level boxes, one arrow meaning, parts called "stage" or "step", whole-method input and output drawn at the two ends, and a caption under ten words that decodes nothing. Legends are almost absent. Colour carries meaning in three figures (Ferraz, Tay, He) and is labelled in place or in the body text, never in a legend box.

### (b) Best two exemplars for this thesis's "whole method in one figure"

1. **Ferraz 2024, Figure 2 (p.6).** Structured CTI → three stages → executable adversary emulation. The content is the closest in the corpus to reports → graph → profiles → Petri nets → execution. The grammar to borrow:
   - input and output drawn as their own end shapes;
   - one arrow meaning;
   - a verb row above each named box, so a box can be a noun (artefact) while the row says what the stage does;
   - one accent colour marking the stage that carries the contribution;
   - a 9-word caption.

   The platform (Caldera) is left out of the chain.
2. **Rodriguez 2024, Figure 1 (p.4).** Four named steps, each a header over one card that names the tool or artefact the step produces, all at one depth, with a 2-word caption. The header-over-card tier fits this thesis's L-levels, where each stage has both a process and a product (attack graph, profiles, Petri nets).

For the one join these two do not cover (the executable models running inside an existing simulator), the corpus's own lineage supplies the pattern. **Tay F1 and Ho F1** draw the simulator as a surrounding container, with the added part as a sibling container and a labelled exchange between them. Neither draws the simulator as a step. Tay also marks existing vs new by colour.

### (c) Corpus figures that commit the named pitfalls

- **Mixed abstraction levels:**
  - AttacKG+ F3: example tactic/technique IDs, state chips and graph glyphs inside the overview.
  - Tay F1: plugin drawn to the Q-network layer, simulator as 3 boxes.
  - He F2: a flowchart decision diamond inside the overview.
  - Zhuang F3: full attack-graph and mission-model instances inside the architecture.
  - Rahman F2 (milder): result counts in the method figure.
- **Arrows with several meanings:**
  - AttacKG+ F3: data, knowledge input, broadcast and assembly, all in one unlabelled style.
  - He F2: data, control branch, membership, selection.
  - Zhang23 F1: labelled interactions plus unlabelled "conducts/launches".
  - Ho F1: unlabelled cycle plus labelled signals plus an unlabelled "trains".
  - Tay F1 and Zhuang F3 also carry several meanings but label every arrow, which is the defensible version.
- **Long decoding caption:**
  - He F2 (68 words: narrates three numbered steps, states a parameter "1,000 packets", uses "FPR").
  - AttacKG+ F3 (55 words: enumerates components).
  - AttacKG+ F1 (36 words: decodes the layers).
  - Sengupta F1 (34 words: states a finding).
  - Ferraz F1 (27 words: states the paper's argument).
- **Internal jargon in the overview:**
  - AttacKG+ F3: P/F/T/I chips and an unexplained snowflake icon; its legend is in a different figure.
  - Tay F1: "Q-Network Output Layer", "Feature Fusion Module".
  - He F2: "MTDAD Pool"; "FPR" in the caption.
  - Ferraz F1: "SUT", and the coined "procedural semantics gap".
- **Simulator / environment drawn as a step:**
  - Rodriguez F1: "System under attack" is the content of step 1, Enactment.
  - Ferraz F1: "SUT Binding" is a box in the chain.
  - Zhuang F3: third-party tools MulVAL/SnIPS as boxes in the loop.
  - He F2: the defended system (Target NIDS) as the first box of the chain.
  - The corpus's counter-examples are Tay F1 and Ho F1 (simulator as container) and Ferraz F2 and Kim F1 (platform left out of the overview and given its own figure: Kim Fig. 4, He Fig. 3).
