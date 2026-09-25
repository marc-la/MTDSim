---
status: durable
created: 2026-09-25
updated: 2026-09-25
---

# Method-section heading survey (corpus) — 2026-09-25

Question: what grammatical form do method / approach / model sections in this repo's
literature corpus use for their subsection headings? Settles the chapter 4 heading
form once the L-prefixes go.

## Scope and method

- Sources: `docs/sources/lit_review/*.md`, `docs/sources/methodology/*.md` (not
  `figure_design/`), and `docs/implementation/evaluation_anatomies/*.md` for papers
  whose primary is not in the repo or whose md lost its `#` headings.
- Unit counted: the **second-level subsections** (x.y, or Roman-section letter A, B…)
  of each paper's method / approach / model / formalisation / metrics-definition
  sections. That is the level our §4.1–§4.5 sit at. Deeper headings (x.y.z) are
  recorded where they show a form not seen at x.y, but tallied separately.
- Excluded: surveys and position papers with no method section of their own (cho2020,
  alshamrani2019, al-sada2024, sadlek2022, jalowski2026, sengupta2020, ward2018), and
  simulation-methodology guideline papers (grimm2020, lee2015, tenbroeke2016, hoad,
  rossow, saltelli, pianosi, iooss, sargent, vanderkouwe). jafarian2015 and
  wang2017rdam: method subsection headings not recorded in their anatomy files or md.
- Forms: **N** noun phrase naming an artefact/component; **NP-proc** nominalised
  process noun phrase ("… construction", "… generation", "Extraction"; "X of Y" with a
  nominalised head counted here too); **G** gerund phrase ("Modelling the network");
  **S** "Stage/Step N: X"; **Q/other** anything else. Where S wraps another form, the
  inner form is noted in brackets.
- Case is as printed (journal styles impose title case or small caps); the tally is
  about grammatical form, not case.

## Per-paper skeletons (verbatim, with locators)

Locators: `L<n>` = md line in the named file; `md:<n>` / `:<n>` = line as recorded in the
anatomy file; `p.<n>` = PDF page as recorded in the anatomy file.

### Pipeline / CTI-method papers

**ferraz2024** — `lit_review/2_4_ferraz2024procedural.md`
- `5 Methodology` L141
  - `5.1 Stage 1: Automated Structural Modeling` L149 — S [NP-proc]
  - `5.2 Stage 2: Technique Translation Layer` L157 — S [N]
  - `5.3 Stage 3: Emulation Integration` L178 — S [NP-proc]
- `7 Emulation Setup` L286 — N (top level)

**rodriguez2024** — `lit_review/2_4_rodriguez2024process.md`
- `3 A method for attacker profiling` L95
  - `3.1 Extraction` L103 — NP-proc
    - `3.1.1 Event collection and organization` L107 — NP-proc
    - `3.1.2 Labeling of events` L125 — NP-proc (gerund + of)
    - `3.1.3 Building the event log` L167 — G
  - `3.2 Discovery` L177 — NP-proc
  - `3.3 Analysis` L191 — NP-proc
- Application sections (not tallied as method, but they are headings):
  `4.1 Step 1: Enactment` L209, `4.2 Step 2: Extraction` L217, `4.3 Step 3: Discovery`
  L302, `4.4 Step 4: Analysis` L342; `5.1 Step 1: Enactment` L523, `5.2 Step 2:
  Extraction` L529, `5.3 Step 3: Discovery` L571, `5.4 Step 4: Analysis` L579 — all S [NP-proc].

**zhang2025 (AttacKG+)** — `lit_review/2_4_zhang2025attackg_.md`
- Title: `AttacKG + : Boosting attack graph construction with Large Language Models` L11
- `3. Task definition` L100 (top level, no subsections)
- `4. Approach` L114
  - `4.1. AttacKG + threat extraction` L120 — NP-proc
  - `4.2. AttacKG + prompt design` L156 — NP-proc
    - `4.2.1. CTI reports rewrite based on tactic` L172 — NP-proc
    - `4.2.2. CTI reports parser` L188 — N
  - `4.3. Technology identifier for CTI reports` L206 — N
  - `4.4. CTI reports state summarizer` L222 — N

**rahman2024** — `lit_review/2_4_rahman2024mining.md`
- `3 METHODOLOGY` L53 — **no numbered subsections**. Steps are bold run-in labels,
  S + imperative verb phrase (not headings; tallied separately):
  `S1A: Select a taxonomy of attack actions:` L59; `S1B: Construct a dataset of CTI
  reports:` L92; `S1C: Construct a dataset of attack actions in text:` L110; `S1D: Train
  supervised classifiers for predicting attack actions from text:` L114; `S2A: Construct a
  dataset of temporal relations:` L122; `S2B: Identify temporal features from text` L124;
  `S2C: Train supervised classifiers for predicting temporal relations` L183; `S3A: Apply
  ChronoCTI on a large corpus of CTI reports` L218; `S3B: Categorize the identified
  temporal patterns` L220.
- Results sections are headed by research question: `4 FINDINGS ON RQ1` L222, `5 FINDINGS ON RQ2` L332.

**buechel2025** — `lit_review/2_4_buechel2025sok.md` (SoK; its empirical setup only)
- `3 Empirical Analysis: Setup` L216
  - `3.1 Ontology` L220 — N
  - `3.2 Datasets` L238 — N
  - `3.3 Metrics` L246 — N
- `4.1 Methods and Adaptations` L254 — N (repeated as `5.1 Methods and Adaptation` L299, `6.1` L353)

**hutchins2011** — `lit_review/hutchins2011killchain.md`
- `3 Intelligence-driven Computer Network Defense` L114
  - `3.1 Indicators and the Indicator Life Cycle` L128 — N
  - `3.2 Intrusion Kill Chain` L160 — N
  - `3.3 Courses of Action` L203 — N
  - `3.4 Intrusion Reconstruction` L274 — NP-proc
  - `3.5 Campaign Analysis` L320 — NP-proc

### MTD evaluations (lineage and review-cited)

**brown2023** — `lit_review/brown2023.md`
- `III. MTD EVALUATION FRAMEWORK` L49
  - `A. modeling the Network` L53 — G (lower-case "m" as printed in the md)
  - `B. Modeling Defense` L77 — G
  - `C. Modeling the Attacker` L101 — G
  - `D. Defense and Adversary interaction` L117 — NP-proc

**zhang2023** — `lit_review/zhang2023.md`
- `4 Methodology` L256
  - `4.1 Overview of the Simulation Framework` L260 — N
  - `4.2 Modelling the Network` L264 — G
    - `4.2.1 Network Generation` L270, `4.2.2 Host Generation` L278, `4.2.3 Service Generation` L282 — NP-proc
  - `4.3 Modelling the MTD` L286 — G
    - `4.3.1 Modelling MTD Techniques` L290, `4.3.2 Modelling MTD Execution Scheme` L313, `4.3.3 Modelling MTD Event` L338 — G
    - `4.3.4 Simulating Time for MTD` L348 — G
  - `4.4 Modelling the Adversary` L356 — G
    - `4.4.1 Modelling Adversary Profiles` L360, `4.4.2 Modelling Attack Event` L372 — G
    - `4.4.3 Simulating Time for Adversary` L384 — G
  - `4.5 Modelling Simulation Time` L400 — G

**ho2024** — `lit_review/ho2024.md`
- `3 Methodology` L232
  - `3.1 System Overview` L234 — N (`3.1.1 Environment and Players` L240, `3.1.2 Static Degrade Factor` L244 — N)
  - `3.2 Model` L250 — N (`3.2.1 Double Deep Q-network learning` L254, `3.2.2 Neural Network Architecture` L266, `3.2.3 Actions` L274, `3.2.4 Rewards` L278 — N)
  - `3.3 Experiment Setup` L290 — N (`3.3.1 Fixed Parameters` L292, `3.3.2 Features` L316 — N; `3.3.3 MTD Selection` L402 — NP-proc)
  - `3.4 Evaluation Method` L475 — N (`3.4.1 Results collection pipeline` L477 — N; `3.4.2 Evaluation metrics calculation` L481 — NP-proc)

**tay2024** — `lit_review/tay2024.md`
- `4 Methodology` L202
  - `4.1 MTDShield` L212 — N (`4.1.1 Feature Extraction Module` L228, `4.1.2 Time Series Analysis Module` L240, `4.1.3 Feature Fusion Module` L252, `4.1.4 Q-Network Output Module` L256 — N)
  - `4.2 Model Training` L262 — NP-proc (`4.2.1 Double DQN Action Selection` L272 — NP-proc; `4.2.2 Experience Replay` L276 — N)

**hong2018** — `lit_review/1_2_hong2018dynamic.md`
- `3. Categorization of attack and defense efforts` L83
  - `3.1. Categorization of attack efforts` L87 — NP-proc
  - `3.2. Categorization of defense efforts` L102 — NP-proc
- `4. Temporal graphical security model` L106
  - `4.1. Network states` L110 — N
  - `4.2. T-HARM` L131 — N
  - `4.3. MTD technique characteristics and definitions` L155 — N (`4.3.1. Shuffle` L163, `4.3.2. Diversity` L173, `4.3.3. Redundancy` L177 — N)
- `5. Dynamic security metrics` L216
  - `5.1. Attack efforts metrics` L222 — N
  - `5.2. Defense efforts metrics` L286 — N
  - `5.3. Application of dynamic security metric modules` L336 — NP-proc
  - `5.4. Dynamic metric quantification` L467 — NP-proc

**masud2025** — `lit_review/1_3_masud2025vulnerability.md` (md order scrambled; PDF order per anatomy)
- `3. Network configurations` L152
  - `3.1. Threat model` L186 — N
  - `3.2. The proposed framework for implementing MTD for vulnerability de-fence` L166–168 — N
  - `3.3. Experimental environment, parameters and validation` L248 — N
  - `3.4. Proposed method- three-layer THARM` L301 — N
  - `3.5. IoT network security metrics calculation` L394 — NP-proc
  - `3.6. Security-driven MTD model` L452 — N (`3.6.6. Integrating shuffle, diversity, and redundancy` L552 — G; `3.6.2. MTD shuffling strategy` L504 — N)

**kim2026** — `lit_review/3_2_kim2026mtdid.md`
- `3. Proposed approach` L99 (no subsections)
- `4. MTD in depth` L113
  - `4.1. Ontology` L117 — N
  - `4.2. New digital artifacts in an SDN network` L135 — N
  - `4.3. Offensive techniques in ATT&CK and CKC` L139 — N
  - `4.4. Conceptual MTD framework based on CKC` L157 — N
- `5. Case studies` L258
  - `5.1. System model` L262 — N
  - `5.2. Attack model` L278 — N
  - `5.3. Defense model` L280 — N (`5.3.1. Combination of MTD techniques` L294 — NP-proc)

**he2025** — `lit_review/3_2_he2025MTD-AD.md`
- `III. PRACTICAL ADVERSARIAL ATTACKS AGAINST ANOMALY-BASED NIDS MODELS` L91
  - `A. Threat Model` L97 — N
  - `B. Practical Adversarial Attacks` L93 — N
- `IV. MTD AS ADVERSARIAL DEFENCE` L141
  - `A. Defence Model` L145 — N
  - `B. MTD-AD` L161 — N
- `V. EXPERIMENT SETUP` L209
  - `A. Dataset` L211 — N
  - `B. Attack & Defence Metrics` L225 — N

**sharma2025** — `lit_review/sharma2025.md` (plain-text headings)
- `3. System Model` L125: `3.1. Network Model` L130, `3.2. Threat Model` L158, `3.3. Defense Model` L181 — N
- `4. Proposed Approach` L204: `4.1. Time-to-Compromise Metrics` L230, `4.2. Security Risks Metrics` L335 — N

**mendonca2023** — `lit_review/added_mendonca2023.md`
- `3. System models` L287: `3.1. Network model` L340, `3.2. Performance models` L385, `3.3. Cost model` L630 — N
- `4. Numerical analysis and discussion` L711: `4.1. Experimental setup` L719, `4.2. Metrics` L744 — N

**alavizadeh2022** — `lit_review/alavizadeh2022.md` (small caps, spaces lost in md) + `evaluation_anatomies/alavizadeh2022.md`
- `III. DEFINITIONS AND FORMALIZATION` (p.4–7)
  - `A. E-HEALTH CLOUD MODEL` L219 — N
  - `B. HARM CONSTRUCTION` L191 (md: "B. HARMCONSTRUCTION") — NP-proc
  - `C. IMPORTANCE MEASURES` L270 — N
  - `D. SECURITY METRICS` L251 — N
  - `E. MTD FORMALISM` L363 — N

**chobenasher2018** — `lit_review/chobenasher2018.md` (plain-text headings)
- `3. System model` L381: `3.1. Attack model` L442, `3.2. Defense model` L493 — N
- `4. Performance model` L557: `4.1. Stochastic Petri Nets` L558, `4.2. Metrics` L709 — N
  (4.1 walks the net under bold run-ins, e.g. "Access by an attacker", "Defense by MTD", md:583–708 per anatomy)

**zaffarano2015** — `evaluation_anatomies/zaffarano2015.md` (md headings garbled)
- `2. OVERALL APPROACH` (md L69); `3. EXPERIMENTAL FRAMEWORK` (md L82)
  - `3.1 Automated Topology Generation` (md L155) — NP-proc
  - `3.2 Activity Models` (md L147) — N (`3.2.1 Mission Representation` md L230, `3.2.2 Attacker Representation` md L255 — NP-proc)
- `4. METRICS` (md L289): `4.1 Productivity` L310, `4.2 Success` L377, `4.3 Confidentiality` L383, `4.4 Integrity` L407, `4.5 Overall Metrics` L436 — N

**manadhatawing2011tse** — `evaluation_anatomies/manadhatawing2011tse.md`
- `3 FORMAL MODEL FOR A SYSTEM'S ATTACK SURFACE` (md L145): `3.1 I/O Automata Model` (md L154), `3.2 Damage Potential and Effort` (md L343), `3.3 A Quantitative Metric` (md L453) — N
- `4 EMPIRICAL ATTACK SURFACE MEASUREMENTS` (md L508): `4.1 Identification of Entry Points and Exit Points, Channels, and Untrusted Data Items`, `4.2 Estimation of Damage Potential-Effort Ratio` — NP-proc; `4.3 Attack Surface Measurements and Their Usage` — N

**zhuang2012** — `methodology/zhuang2012_simulation_mtd.md` (plain-text headings)
- `2 MTD design principles` L119: `2.1 Proof-of-concept MTD system` L197, `2.2 Conservative Attack Graph` L430 — N (`2.1.1 Resource Mapping System` L380 — N)
- `3 Simulation-based Experiments` L522: `3.1 Simulation Assumptions` L535, `3.2 Moving mechanisms and attacks` L577 — N

### Formal-model cousins (primaries not in repo; headings from the anatomy files)

**bland2020** — `lit_review/4_bland2020machine.md`
- `4. Petri Net Models of Cyberattacks` L535 — N (no subsections)
- `5. Machine Learning in Cyberattack Models` L574 — N (no subsections)
- (background) `2.1. Petri Net with Players, Strategies, and Costs` L81 — N

**outkin2023** — `lit_review/4_outkin2023defender.md`
- `3 APPROACH` L205
  - `3.1 GPLADD Games` L197 — N
  - `3.2 PLADD - Building Blocks for GPLADD` L221 — N
  - `3.3 Transitions on Attack Graph` L249 — N
  - `3.4 Discrete-Time Markov Chain Approximation` L267 — NP-proc
  - `3.5 Markov Chain Transition Probabilities Inference` L349 — NP-proc
- `4 SIMPLIFIED APT3 ATTACK DEFINITION` L361: `4.1` L363 (title lost in md), `4.2 Attacker Strategy` L369, `4.3 Defender Strategy` L395 — N

**anderson2016** — `evaluation_anatomies/anderson2016.md`
- `III. MODEL` (line 67): `A. Closed-Form Mathematical Model` (75), `B. Stochastic Petri Net` (81) — N

**torquato2022** — `evaluation_anatomies/torquato2022.md`
- `III. VM MIGRATION AS REJUVENATION AND MTD` (85): `A. Virtualized system and software rejuvenation strategy` (87) — N
- [IV. PROPOSED MODELS, heading lost]: `A. Availability-related model perspective` (123), `B. Security-related model perspective` (175) — N; `C. Metrics computation` (187) — NP-proc

**maleki2016** — `evaluation_anatomies/maleki2016.md`
- `4. MTD GAMES EXAMPLES` (131): `4.1 Single-Target Hiding` (141), `4.2 Multiple-Target Hiding` (168) — N (scheme names)

**venkatesan2016** — `evaluation_anatomies/venkatesan2016.md`
- Top level all N: `3. PRELIMINARIES`, `4. THREAT MODEL`, `5. DEFENDER'S MODEL`, `6. METRICS`, `7. DEFENDER'S STRATEGIES` (md:55–223)
- `6.1 Minimum Detection Probability` (md:167), `6.2 Attacker's Uncertainty` (md:215) — N

**carroll2014** — `evaluation_anatomies/carroll2014.md`
- `III. MODELS FOR NETWORK SHUFFLING DEFENSES` (:61): `A. Urn-Based Models` (:81) — N; `B. Modeling Static Addresses` (:89), `C. Modeling Perfect Address Shuffling` (:99) — G

**crouse2015** — `evaluation_anatomies/crouse2015.md`
- `3. RECONNAISSANCE PERFORMANCE MODELS` (:49): `3.1 Undefended Model` (:78), `3.2 Honeypot Defense Model` (:92), `3.3 Shuffling Defense Model` (:110) — N

**reti2022** — `evaluation_anatomies/reti2022.md`
- `3 METHODOLOGY` (:79): `3.1 Attacker Model` (:83) — N
- `4 SIMULATION ENVIRONMENT` (:139): `4.1 NASim` (:143) — N; `4.2 Implementation of Honeypots and Network Address Mutation` (:153) — NP-proc

## Tally (second-level method subsections, 28 papers + bland2020 at top level)

| Form | Headings | Papers using it |
|---|---:|---:|
| N — artefact/component noun phrase | 90 | 25 (26 with bland2020's two top-level method sections) |
| NP-proc — nominalised process | 22 | 13 |
| G — gerund phrase | 9 | 3 (brown2023, zhang2023, carroll2014) |
| S — "Stage/Step N: X" | 3 | 1 (ferraz2024); 11 headings / 2 papers counting rodriguez2024's application sections |
| Q/other | 0 | 0 |
| **Total** | **124** | |

Separately: rahman2024's nine bold run-in step labels are S + imperative verb
("S1A: Select a taxonomy of attack actions:"); they are not headings.

Observations:

1. **N is modal by a wide margin** (≈73% of headings; used by 25 of 28 papers). The
   dominant N sub-patterns are "X model" (`System model`, `Attack model`, `Defense
   model`, `Threat Model`, `Network model`, `Performance models`, `Cost model`) and bare
   "Metrics" / "X metrics".
2. **NP-proc is second** (≈18%), and it is where the process-shaped sections sit:
   construction, extraction, identification, estimation, integration, computation,
   calculation. It mixes freely with N among siblings (outkin2023, hong2018, AttacKG+,
   tay2024, alavizadeh2022, torquato2022, ho2024 all mix N and NP-proc in one section).
3. **G is rare, and every second-level G heading uses one verb, "Model(l)ing"**
   (`Modeling the Attacker`, `Modelling the Network`, `Modeling Static Addresses`).
   zhang2023's gerunds follow brown2023's template (lineage). Gerunds with varied,
   action-describing verbs appear only at the third level and only three times:
   `3.1.3 Building the event log` (rodriguez2024 L167), `3.6.6. Integrating shuffle,
   diversity, and redundancy` (masud2025 L552), `4.3.4 Simulating Time for MTD` /
   `4.4.3 Simulating Time for Adversary` (zhang2023 L348, L384). So a set of five
   gerund headings each with its own verb has no precedent in the corpus.
4. **Numbered stage labels in headings are rare**: ferraz2024 (Stage 1–3) and
   rodriguez2024's application sections (Step 1–4) only; rahman2024 numbers its steps
   as run-in labels. They are used by the two papers whose method is literally a
   sequence of stages. The thesis registry already reserves *stage*, *step*, *phase*,
   *level* and *tier* for other objects (`docs/workflows/terminology.md` L47), so S is
   out regardless.
5. Existing house rule: `docs/workflows/voice.md` L55 — "Headings state what the section
   is on — nothing more"; a heading that performs is over-dressed for the register.
   Consistent with the N/NP-proc corpus norm.

## Closest-content examples (verbatim)

- Graph construction: `B. HARM CONSTRUCTION` (alavizadeh2022, md L191); `4.1. AttacKG + threat extraction` (zhang2025, L120); `5.1 Stage 1: Automated Structural Modeling` (ferraz2024, L149); `2.2 Conservative Attack Graph` (zhuang2012, L430); `3.3 Transitions on Attack Graph` (outkin2023, L249).
- Profiling / partitioning: `3 A method for attacker profiling` (rodriguez2024, L95); `3.1. Categorization of attack efforts` (hong2018, L87); `4.4.1 Modelling Adversary Profiles` (zhang2023, L360).
- Formalism / model: `4.1. Stochastic Petri Nets` (chobenasher2018, L558); `B. Stochastic Petri Net` (anderson2016, anatomy line 81); `4. Petri Net Models of Cyberattacks` (bland2020, L535); `E. MTD FORMALISM` (alavizadeh2022, L363); `3.4 Discrete-Time Markov Chain Approximation` (outkin2023, L267).
- Integration with a simulator / emulator: `5.3 Stage 3: Emulation Integration` (ferraz2024, L178); `4.2 Implementation of Honeypots and Network Address Mutation` (reti2022, anatomy :153); `D. Defense and Adversary interaction` (brown2023, L117).
- Metrics: `4.2. Metrics` (chobenasher2018, L709); `C. Metrics computation` (torquato2022, anatomy 187); `3.4.2 Evaluation metrics calculation` (ho2024, L481); `B. Attack & Defence Metrics` (he2025, L225); `5. Dynamic security metrics` (hong2018, L216).
