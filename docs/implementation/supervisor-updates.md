# Supervisor updates (23 Jun – 9 Aug 2026): full text and metrics

Source: six Word documents Marc sent to Dr Jin B. Hong (honours supervisor, UWA) during the thesis
"AI-driven Moving Target Defence under realistic APT attacker profiles" (MTDSim).

This file is a plain-text conversion for Claude Code. Word tables are now Markdown tables. Every
figure (chart, heatmap, screenshot of a table, diagram) has been **transcribed**, not linked. Numbers read
off charts are marked "(read from chart)". Wording in quotes is Marc's original, lightly
cleaned (formatting only). Notes marked **[conversion note]** were added during conversion and are not part of the originals.

---

## 0. Document index (chronological)

| # | Date (2026) | Day | Original file | Type | What it covers | Metrics / tables inside |
|---|---|---|---|---|---|---|
| 1 | 23 Jun | Tue | 23-jun-supervisor-update.docx | Update | Pipeline L0–L5 summary; attack graph from 38 Attack Flows; 4 objective classes; first Petri net | Per-class tactic share heatmap (%), class signatures, edge-weight graph stats |
| 2 | 10 Jul | Fri | 10-jul-supervisor-update.docx | Update | Tactic durations (15-tuple); Petri timelines; termination rules; calibration questions | Tactic dwell-time table; time-to-objective medians; outcome mix (objective/stalled) per profile × routing arm; 20 sample walks per profile |
| 3 | 14 Jul | Tue | 14-jul-meeting-agenda.docx | Meeting agenda | Petri net ↔ MTDSim join; success/failure; pre-ATT&CK; Caldera-style tactic-action set; decisions closed | tactic_action_map.csv (tactic → ATT&CK ID → group); MTDSim fact base |
| 4 | 21 Jul | Tue | 21-jul-supervisor-update.docx | Update | End-to-end join; movement / controller / action layers; MTDSim FSM analysis; synthetic pre-intrusion subnet | MTDSim 6-phase table with timings; tactic → verb coverage matrix; synthetic overlay shares |
| 5 | 03 Aug | Mon | 03-aug-supervisor-update.docx | Update | 8-axis APT fidelity rubric (implemented?); lifecycle stages; success/failure overlay matrices; tactic → verb mapping v2 | 8-axis status table; SUCCESS 15×15 matrix; FAILURE 15×15 matrix; transition counts by stage offset |
| 6 | 09 Aug | Sun | 09-aug-supervisor-update.docx | Update | APT criterion **with instrumentation and results**; methodology outline; experimental design | JSD profile divergence; predictability; detectability; disengagement; experimental dimension table |

**Where the evaluation metrics live:** the evaluation criterion (8 axes) is defined on 03 Aug (§5.1) and
measured on 09 Aug (§6.1). Section 7 at the end collects every numeric table in one place.

---

## 0.1 Naming map (names changed between documents)

| Concept | 23 Jun – 3 Aug name | 09 Aug name (JSD chart) | Code-style name seen in charts |
|---|---|---|---|
| Steal-objective profile | pure steal | exfiltration | `pure_steal` |
| Impediment-objective profile | pure impediment | impact | `pure_impediment` |
| Double-extortion profile | double extortion | exfiltration + impact | `double_extortion` |
| Infrastructure-setup profile | infrastructure setup | positioning (C2) | `infrastructure_setup`, `objective_none_c2` |
| All 38 flows together | aggregate / GAP baseline | unsegregated | `aggregate` |
| Inherited MTDSim attacker | FSM baseline / baseline attacker | baseline (6-phase FSM) | — |
| Marc's attacker | profiled attacker / movement attacker | movement | `profiled_attacker` |

Pipeline levels: L0 raw CTI (MITRE Attack Flow) → L1 aggregate attack graph ("GAP") → L2 objective subgraphs
("GASP") → L3 Petri net ("OGASP" structural net) → L3b controller → L4 MTDSim → L5 evaluation.

Tactic abbreviations used in the 03 Aug matrices: RC reconnaissance, RD resource development, IA initial access,
EX execution, PS persistence, PE privilege escalation, DI defence impairment, ST stealth (defence evasion),
CA credential access, DS discovery, LM lateral movement, C2 command and control, CO collection,
EF exfiltration, IM impact.

Lifecycle stages (from 03 Aug): 0 preparation {RC, RD}; 1 intrusion {IA, EX}; 2 post-intrusion operations
{PS, PE, DI, ST, CA, DS, LM, C2}; 3 objective {CO, EF, IM}.

---

# 1. 23 Jun 2026 (Tuesday): Supervisor update

## 1.1 Summary (pipeline levels; red in original = future work)

| Level | Description | Notes |
|---|---|---|
| 0 | Raw CTI | MITRE **Attack Flow** corpus (per-campaign). |
| 1 | Attack graph | 38 analyst-curated flows → technique-level directed graph. Attack Flow coarseness and dataset limits → GenAI-synthesise more Attack Flows? Every edge is a dependency drawn by a human analyst. 88% of edges belong to one flow (max = 4 flows). Systematically blind to pre-intrusion recon (reports normally start at detection), so reconnaissance → initial-access is basically missing. Direction change: **Attack-Flow-only**; process mining / ontology regex dropped (for now). |
| 2 | Attack subgraphs via motivation | Classification is Claude-derived, 4 classes: 1. Double extortion, 2. Infrastructure setup, 3. Pure impediment, 4. Pure steal. Some overlap; some flows have more than one operational objective. Marc "not too confident"; verification needed (Claude inspected the CTI report of each flow). |
| 3 | Attack subgraph formalism: Petri nets | **Places** = ATT&CK tactics. **Transitions** = tactic pairs. **Arcs** = unclear what to represent; currently bipartite place[a] → T → place[b]. **Tokens** = single token = "where the attack is at", seeded at recon/initial access. Only the structure of the L2 profiles is usable; aggregating 38 flows won't give meaningful edge weights. Recon → initial access largely disconnected. Manual wiring of recon → initial access? No rates, timing, weights or rewards yet. |
| 4 | Operationalise Petri nets | Analyse and execute Petri-net attack profiles in MTDSim. How to bind to MTDSim alongside existing network/attack/defender modules? What MTDSim changes are needed? |
| 5 | Evaluation | Pull out comparative evaluation to write thesis. |

## 1.2 Figures (transcribed)

**Fig 1.1 – Single Attack Flow as a directed graph.** Example: "Black Basta Ransomware · malware · 41 nodes / 48 edges".
Linear technique chain with AND gates, e.g. T1566.001 Spearphishing Attachment → T1140 → T1204.002 → T1059.005 → T1059.001 →
T1574.001 → T1218.010 → (T1543.003 / T1136 / T1484.001 → T1098) → AND → T1573 → T1105 → (T1016, T1219, T1087.002, T1555, T1112,
T1562.004, T1082) → T1021.001 → T1569.002 → (T1622, T1562.001, T1497, T1489) → T1560.001 → T1573 → T1567 → (T1657, T1047, T1490)
→ AND → (T1562.009, T1112) → AND → T1083 → T1486 → T1491.001 → T1070.004. Only techniques, dependencies and logic gates kept.

**Fig 1.2 – Aggregate attack graph at tactic level.** Title: "GAP 0.5 — tactic FSM · 15 states · 52/132 transitions (weight ≥ 4) ·
edge weight = total observations across 38 flows". Node technique counts: initial-access 7, execution 9, persistence 12,
privilege-escalation 4, stealth 11, defense-impairment 2, credential-access 11, discovery 19, lateral-movement 6, collection 8,
command-and-control 10, exfiltration 5, impact 9, resource-development 5, reconnaissance 6.
Heaviest edges (read from chart): command-and-control → discovery 26 (23 edges); discovery → command-and-control 19 (16);
execution → stealth 19 (15); stealth self-loop 15 (13); stealth → discovery 14 (13); execution → persistence 14 (11);
C2 self-loop 14 (11); initial-access → execution 13 (10); execution → discovery 12 (10); discovery self-loop 12 (12).
Reconnaissance, resource-development and defense-impairment have **no edges ≥ 4** (gap at the front of the chain; edges < 4 exist).

**Fig 1.3 – Same graph at technique level, clustered by tactic, all edges.** (Structure only; no numbers to transcribe.)

**Fig 1.4 – GASP class workflow comparison (GAP 0.5, 38 flows).** Per-class tactic share = % of class actions per tactic.

| Class (flows) | RC | RD | IA | EX | PS | PE | ST | DI | CA | DS | LM | CO | C2 | EF | IM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pure steal (19) | 3 | 1 | 9 | 11 | 8 | 3 | 13 | 1 | 7 | 11 | 7 | 5 | 16 | 3 | 0 |
| double extortion (6) | 1 | 2 | 8 | 13 | 6 | 5 | 10 | – | 5 | 18 | 5 | 1 | 9 | 3 | 15 |
| pure impediment (8) | 2 | 2 | 7 | 13 | 8 | 4 | 15 | 2 | 4 | 11 | 6 | 2 | 15 | – | 12 |
| infrastructure setup (5) | 1 | 1 | 2 | 23 | 3 | 3 | 10 | 1 | 5 | 15 | 12 | 3 | 20 | – | – |
| GAP baseline (38) | 2 | 1 | 7 | 13 | 7 | 4 | 13 | 1 | 6 | 13 | 7 | 4 | 16 | 2 | 4 |

("–" = blank cell, i.e. 0.)

Class signature (top 3 over-represented tactics, Δ percentage points vs GAP baseline; exfil/impact share):

| Class | Top over-represented | Exfil share | Impact share |
|---|---|---|---|
| pure steal (19 flows) | collection (+2), credential-access (+1), initial-access (+1) | 3.5% | 0.2% |
| double extortion (6 flows) | impact (+10), discovery (+6), privilege-escalation (+2) | 2.7% | 14.5% |
| pure impediment (8 flows) | impact (+8), stealth (+2), defense-impairment (+1) | 0.0% | 12.0% |
| infrastructure setup (5 flows) | execution (+10), lateral-movement (+5), command-and-control (+5) | 0.0% | 0.0% |

Marc's caption: CTI is execution-, stealth-, discovery- and C2-heavy. Impact depends on motivation. Some variation between profiles; more verification needed.

**Fig 1.5 – Class subgraphs by technique (min_obs ≥ 2).**

| Class | Flows | Techniques | Edges |
|---|---|---|---|
| pure steal | 19 | 34 | 54 |
| double extortion | 6 | 21 | 31 |
| pure impediment | 8 | 27 | 46 |
| infrastructure setup | 5 | 21 | 34 |

**Fig 1.6 – Petri net for the double-extortion grouping.** P = ATT&CK tactics, T = tactic pairs (e.g. `execution__to__discovery`),
F = placeholder arcs (all weight 1), M = one black token in reconnaissance ({1}). Reconnaissance and resource-development are isolated
places. AND/OR gates from Attack Flow are **not** represented (not all flows use them, so their aggregate meaning is ambiguous).

**Fig 1.7 – Same net, "OGASP structural net · double_extortion".** 14 places · 72 transitions · 201 GASP edges · token seeded in
reconnaissance · objective (exfiltration, impact) **NOT reachable** from token · recon → initial-access: **DISCONNECTED**.

## 1.3 Done since last update

Consolidating; thinking about L3/L4.

- **Dropped:** MTDSim visualiser (too much overhead, too much Claude usage). Subgraphing by *motivation*: STIX/ATT&CK/Attack Flow don't record it for APT groups, so pivoted to the (inferred) *operational objective* of each Attack Flow.
- **Deferred:** retraining MTDShield / Joo Kai's RL model for comparative evaluation.

## 1.4 Issues / blockers

Is the idea right?
1. **Premise unverified**: do the four profiles behave differently in the simulator? Sim-level test not run.
2. **Classification needs independent verification**: the four-way split is Claude-derived; some flows have more than one objective.
3. **Corpus thinness**: only 38 flows; 88% of edges appear in a single flow (max 4), so rates can't come from frequency. GenAI-synthesised flows?

Can it get into MTDSim?
4. **Profiles → MTDSim binding unresolved**: no shared join key (Marc's work = ATT&CK technique/tactic; MTDSim = host/service/CVE-CVSS).
5. **Scale of MTDSim changes for the MVP undecided**: substrate is CKC-inspired (6 action classes, synthetic CVSS vulns). How to join T-HARM to ATT&CK?
6. **Recon → initial-access gap**: CTI starts at detection. Hand-wire recon/resource dev, or seed at initial access.

Does the Petri net / SPN formalism hold up?
7. **Petri rates ungrounded**: corpus can't supply firing rates; aggregate effects dominated by "what the analyst drew".
8. **AND gates lost in aggregation**: not necessarily bad (state-space explosion, multiple tokens), but arcs aren't used to full capacity.

## 1.5 Decisions needed from Jin

1. Produce Petri net / SPN / CTMC formalisms and evaluate there, or go further and execute in MTDSim? (Marc presumed the latter.)
2. Weights/timings must come from somewhere other than Attack Flow. Adopt MTDSim timing and vary attacker structure?
3. How much MTDSim change is in scope (attacker only, or attacker + some network)?
4. Entry point: initial access (as in CTI), or curate dependencies back to recon?

## 1.6 Next steps

Sem 2 starts 20 July 2026 (~4 weeks). Proposed meeting Thu 25 Jun 2026. Aim to finish most coding over the break; happy to meet online and send regular updates.

---

# 2. 10 Jul 2026 (Friday): Supervisor update

## 2.1 Summary (adapted from previous update)

| Level | Description | Notes |
|---|---|---|
| 0 | Raw CTI | MITRE Attack Flow corpus (per-campaign). |
| 1 | Attack graph | 38 analyst-curated flows → lossless technique-level directed graph; ~88% of edges backed by one flow. Corpus blind to pre-intrusion recon → recon→initial-access near-missing. Corpus expansion / GenAI-synthesised flows (future). |
| 2 | Attack subgraphs by operational objective | 4 classes (steal, impediment, double extortion, infra setup) + attack graph (aggregate, for comparison). Class = objective **stated by the analyst** in the source report, audit-traced (not inferred). Caveats: small classes, questions over distinctness of profiles. |
| 3a | Petri-net formalism | Places = tactics; transitions = observed tactic pairs; single token = attack position. **Weights resolved:** share of distinct flows per tactic hand-off (recurrence, not counts). Recon still an island in 2 classes → seed at initial access; recon wiring deferred. |
| 3b | Attack timelines | Tactic durations: mix of MTDSim adoption, inference and "educated guesses" = tunable 15-tuple. Profiles differ by termination: steal ends on exfiltration; impediment ends on impact; extortion ends when **both** exfiltration and impact reached. Calibration required. |
| 4 | Operationalise in MTDSim | Implement tactics in MTDSim. |
| 5 | Evaluation | MTD mechanisms vs profile attacker vs FSM baseline (**MTTC, ASR, exposure**); Tay's RL re-enters here. |

## 2.2 Done since last update

**Tactic profiling.** Profiling each tactic so each can be defended in a dissertation section that justifies the durations.
Literature gave little on per-tactic timing, so the search broadened to adversarial modelling, attack simulation, APT attackers and
MTD. Claude drafted a dissertation section (compiled into LaTeX); reads AI-generated; Jin asked to check its shape.

**Timeline implementation.** A 15-number tactic-duration vector was settled on (anchors from MTDSim or picked by a GenAI system):

**Table 2.1 – Tactic dwell times (v0, uncalibrated)** (transcribed from screenshot)

| Tactic | Dwell (s) | How it was set | Why |
|---|---|---|---|
| Reconnaissance | 35 | Taken from simulator constants | Recon is the simulator's scan sequence: scan host (5 s) + scan neighbours (5 s) + scan ports (25 s). |
| Resource development | 0 | Modelling decision | Happens off-network before the attack (weeks–months); attacker arrives equipped, so no simulated time charged. |
| Initial access | 4.5 | Taken from simulator constants | Exploit timer: 15 s scaled by vuln complexity, ~4.5 s for a typical vuln. |
| Execution | 22.5 | Estimated (half the "quiet" time) | Running a payload is quick; slowness is attacker pacing, so half the quiet-operations time. |
| Persistence | 45 | Estimated | Installing backdoors is careful quiet work; no simulator equivalent; given standard quiet-operations time. |
| Privilege escalation | 4.5 | Taken from simulator constants | Usually a vuln exploit, so reuses exploit time. |
| Defence evasion (stealth) | 45 | Estimated — the key free parameter | Baseline "operating quietly" time: 10× an exploit (slower than any priced action, 5–25 s) but below the 200 s average MTD trigger interval, so MTD vs attacker speed stays a live contest. |
| Defence impairment | 22.5 | Estimated | Disabling security tooling is one quick act before the noisy final payload; halved. Least evidence of any tactic. |
| Credential access | 4.5 | Taken from simulator constants | On-host exploitation work; reuses exploit time. |
| Discovery | 35 | Taken from simulator constants | Same as recon but from inside the network; reuses scan time. |
| Lateral movement | 4.5 | Taken from simulator constants | One hop = remote login or remote exploit; exploit time. |
| Collection | 36 | Estimated, checkable against breach reports | Real floor (human effort, data volume). Check: ~64% of victims see collection + exfiltration inside 5 hours. |
| Command & control | 45 | Estimated | Persistent beaconing channel; no vuln data can price it; free parameter at quiet-operations time. |
| Exfiltration | 36 | Estimated, checkable against breach reports | Terminal data-theft act; access-to-exfiltration timing (Sophos median ~3 days) is the held-out validation figure. |
| Impact | 36 | Estimated, checkable against breach reports | Ransomware encryption / destruction has a disk-I/O floor (~6 min–2 h reported). Espionage never reaches it; handled by leaving impact out of those nets, not by zero time. |

"How to read it: everything reduces to four base times. Two come straight from the simulator's existing constants — a scan pass (35 s) and an exploit …" (screenshot cut off). **[conversion note]** The four base values in the table are 35 (scan), 4.5 (exploit), 45 (quiet operations) and 36 (objective floor), with 22.5 = half of quiet and 0 for resource development.

Marc's note: assigning time to recon and resource development is a misnomer (recon is passive and hard for a network to detect).
Starting the Petri net at initial access makes most sense. An alternative might be a parameter for how much the attacker knows
(recon) and its resources relative to its capability (resource dev).

**Fig 2.2 – Net time-to-objective per profile** (initial-access entry · weighted (operator-dedup) · central dwells · 100 seeded runs each; envelope statistic, not the DES MTTC; v0 uncalibrated dwells).

| Profile | Median time-to-objective (s) | Runs reaching objective | Spread (read from chart) |
|---|---|---|---|
| pure_steal | 282 | 91/100 | ~40 – ~1,030 s |
| pure_impediment | 271 | 100/100 | ~70 – ~1,320 s |
| double_extortion | 471 | 80/100 | ~170 – ~2,150 s |
| infrastructure_setup | 140 | 82/100 | ~70 – ~370 s |
| aggregate | 117 | 100/100 | ~50 – ~580 s |

Caption: "Executing each Petri net 100 times, time from source to sink tactic. Some profiles are forced through longer-duration tactics. Tunable?"
Termination: steal on exfiltration; impediment on impact; double extortion on both (hence longer); aggregate on any of C2, exfiltration, impact.
Question to Jin: sensible, or remove termination and run to sim end?

**Fig 2.3 – Outcome mix per profile and routing arm** (initial-access entry, central dwells; share of 100 seeded runs; "stalled" is a legitimate recorded outcome, not an error; "cap" = 0 everywhere).

| Profile | Routing arm | Objective | Stalled |
|---|---|---|---|
| pure_steal | weighted dedup | 91% | 9% |
| pure_steal | weighted raw | 93% | 7% (unlabelled on chart) |
| pure_steal | uniform | 100% | 0% |
| pure_impediment | weighted dedup | 100% | 0% |
| pure_impediment | weighted raw | 100% | 0% |
| pure_impediment | uniform | 100% | 0% |
| double_extortion | weighted dedup | 80% | 20% |
| double_extortion | weighted raw | 75% | 25% |
| double_extortion | uniform | 100% | 0% |
| infrastructure_setup | weighted dedup | 82% | 18% |
| infrastructure_setup | weighted raw | 86% | 14% |
| infrastructure_setup | uniform | 83% | 17% |
| aggregate | weighted dedup | 100% | 0% |
| aggregate | weighted raw | 100% | 0% |
| aggregate | uniform | 100% | 0% |

Caption: green = token reached a sink; some sinks have no fireable out-transition and stall.

**Figs 2.4–2.7 – First 20 seeded walks per profile** (primary cell: initial-access entry · weighted operator-dedup · central dwells). Outcome and end time of each walk:

| Walk | aggregate (any of C2/EF/IM) | double_extortion (EF and IM) | infrastructure_setup (C2) | pure_steal (EF) |
|---|---|---|---|---|
| 000 | objective 300 s | stalled · 13 states | objective 107 s | objective 494 s |
| 001 | objective 107 s | stalled · 4 states | objective 72 s | objective 126 s |
| 002 | objective 50 s | objective 367 s | objective 117 s | objective 228 s |
| 003 | objective 72 s | objective 336 s | objective 116 s | objective 642 s |
| 004 | objective 158 s | objective 565 s | objective 152 s | objective 332 s |
| 005 | objective 130 s | stalled · 22 states | objective 367 s | objective 614 s |
| 006 | objective 72 s | objective 1,036 s | objective 206 s | objective 522 s |
| 007 | objective 50 s | objective 233 s | objective 144 s | stalled · 33 states |
| 008 | objective 230 s | objective 328 s | objective 179 s | objective 166 s |
| 009 | objective 76 s | objective 403 s | stalled · 5 states | objective 122 s |
| 010 | objective 108 s | objective 842 s | objective 340 s | objective 180 s |
| 011 | objective 116 s | stalled · 11 states | objective 194 s | objective 246 s |
| 012 | objective 126 s | stalled · 30 states | objective 179 s | objective 122 s |
| 013 | objective 98 s | stalled · 30 states | objective 72 s | objective 540 s |
| 014 | objective 63 s | objective 413 s | objective 238 s | objective 180 s |
| 015 | objective 94 s | objective 706 s | objective 156 s | objective 192 s |
| 016 | objective 385 s | objective 614 s | objective 171 s | stalled · 6 states |
| 017 | objective 63 s | objective 700 s | objective 72 s | objective 292 s |
| 018 | objective 50 s | objective 223 s | stalled · 3 states | objective 581 s |
| 019 | objective 144 s | objective 166 s | objective 134 s | objective 508 s |

**[conversion note]** The Word file inserts the infrastructure_setup chart twice and has **no pure_impediment walk chart**.
Each bar is colour-coded by tactic (initial access light blue at the start; sink tactic dark red at the end). Resource development dwells 0 s and has no width.

## 2.3 Issues / blockers

Calibration / validation of profiles
1. How to fit profiles to the literature qualitatively? Tunable parameters = tactic dwell times. Some could be 0 (resource dev), some fixed to old simulator times (recon 35 s). No literature on timing; fitting would overfit sparse data.
2. How to fit "what timelines should look like" when many answers are acceptable (ordering, relative dwell, start-to-objective time, which objective reached, campaign length per objective)? Hard to ground in literature.
3. Tuning dwell times easily overfits profiles to expectations; dwell times that suit one profile may not suit others. Weak validation power.

Coupling the finite timeline to the running sim
4. Time validation: timeline scale vs MTD interaction (reactive vs proactive; fixed schedules compete with the attack timeline). Old sims ran 5,000 s; these timelines hit the objective in 200–500 s.
5. Petri timelines end after X s; old FSM attackers cycle phases until sim end.

Implementation queries
6. Tactics carry gains, and MTD tries to deny them, but some can't be denied (resource dev can't be reset; credential access survives IP/topology shuffle). Should this be reasoned into tactic implementations?
7. A tactic = "attacker is attempting this" and may succeed or fail. Encode backward flows as fails and forward as successes? Conflicts with MITRE's no-ordering philosophy (an assumption of this work). Or map CKC onto ATT&CK and use CKC order as forward/backward?
8. Recon and resource dev (formerly PRE-ATT&CK) are outside attacker–network interaction. Should they be a parameter of the attack model?

**Fig 2.8 – CKC ↔ ATT&CK mapping (screenshot of a web answer):**

| Cyber Kill Chain phase | ATT&CK tactics |
|---|---|
| Reconnaissance | Reconnaissance |
| Weaponisation & Delivery | Resource Development, Initial Access |
| Exploitation & Installation | Execution, Persistence, Privilege Escalation, Defense Evasion |
| Command & Control (C2) | Command and Control |
| Actions on Objectives | Credential Access, Discovery, Lateral Movement, Collection, Exfiltration, Impact |

## 2.4 Decisions needed from Jin

Guidance on the three themes above.

## 2.5 Next steps

Flesh out implementation for each tactic; plan capabilities for each action from literature; get sign-off; implement.

---

# 3. 14 Jul 2026 (Tuesday): Meeting agenda

## 3.1 Petri-net ↔ MTDSim join (how much grounding in CTI ontology?)

Working idea: precompute attack timelines, then feed them into a new MTDSim `profiled_attacker` model.

Being in a timeline phase = "attacker is attempting to achieve this goal". Where are success and failure seeded? Timelines advance regardless of what happens in the sim.

- **Where does success rate live?** Possibly at the Petri-net level. ATT&CK encodes none, but CKC could be layered on.
  - **Fig 3.1 – "ATT&CK tactics under the Cyber Kill Chain (pre-v19.1 mapping)"**: CKC phases as a candidate quotient layer over the tactic places. Recon ← Reconnaissance (greyed/dashed); Weaponisation & Delivery ← Resource Development (greyed/dashed), Initial Access; Exploitation & Installation ← Execution, Persistence, Privilege Escalation, Defense Evasion; C2 ← Command & Control; Actions on Objectives ← Credential Access, Discovery, Lateral Movement, Collection, Exfiltration, Impact. Note: PRE-ATT&CK tactics are sparse in the corpus, so the phase layer is poorly defined left of Initial Access.
  - **Fig 3.2 – "Soft CKC ordering as a Petri net"**: places = the 5 CKC phases; token starts in Recon; solid transitions fire on phase success (advance); dashed transitions fire on phase failure (regress / evicted) back to the preceding phase. Deeper regressions (e.g. eviction to Recon) are expressible the same way.
- **Pre-ATT&CK tactics?** Recon/resource dev as pre-attack parameters? E.g. stronger recon/resource-dev → higher success rate, then start at initial access.
- **What practical reports?** What is being pulled from reports (speed/style of executing a tactic)? What does a tactic's "style/shape" mean materially? Some definitional work exists.
  - **Fig 3.3 – `ogasp/timeline/tactic_action_map.csv` (screenshot, dwell column cut off):**

| tactic | attack_tactic_id | group |
|---|---|---|
| reconnaissance | TA0043 | scan-shaped |
| resource-development | TA0042 | prep-off-network |
| initial-access | TA0001 | exploit-shaped |
| execution | TA0002 | stealth-low-and-slow |
| persistence | TA0003 | stealth-low-and-slow |
| privilege-escalation | TA0004 | exploit-shaped |
| stealth | TA0005 | stealth-low-and-slow |
| defense-impairment | TA0112 | stealth-low-and-slow |
| credential-access | TA0006 | exploit-shaped |
| discovery | TA0007 | scan-shaped |
| lateral-movement | TA0008 | exploit-shaped |
| collection | TA0009 | objective-execution |
| command-and-control | TA0011 | stealth-low-and-slow |
| exfiltration | TA0010 | objective-execution |
| impact | TA0040 | objective-execution |

**Fig 3.4 – "FSM ↔ MTDSim ↔ Petri — the layers, and the missing middle"** (diagram):
- Top (REAL · CTI): Petri attack profile, L3 per objective class. Tactic layer = 15 places, ATT&CK v19.1. Example steal net path: recon (island) · initial-access (token) → .31 → execution → .06 → discovery → .33 → collection → .57 → exfiltration (objective); skip arc execution → collection .06. Technique layer carried in transitions: T1078→T1059, T1059→T1018, T1082→T1005, T1005→T1041. "200–500 s · stops at objective". "steal net: 109 transitions · weight = share of flows".
- Middle (MISSING, not in repo): CAPEC (attack patterns) → CWE (weakness classes) → CVE (real vulnerability instances) → CVSS (real scoring) → "no join". Candidate grounding cuts marked at several depths. Tactic → action mapping "= ?".
- Bottom (SYNTHETIC, inherited): MTDSim substrate. "~5000 s · stops when all hosts owned". Attacker 6-verb FSM: SCAN_HOST 5 s, ENUM_HOST 5 s, SCAN_PORT 25 s, EXPLOIT_VULN (per vuln: 15·(1−c) s; succeeds iff rand < c), BRUTE_FORCE 20 s, SCAN_NEIGHBOR 5 s; restart at SCAN_HOST / SCAN_PORT; cycles forever; ≥10 tries on a host → give up. Defender: MTD, 7 schemes (IP/topology shuffle → layer 1; port/OS/service diversity → layer 2; interrupt attacker → penalty). Network = THARM, 3 layers: network (hosts), service (per-host internal graph; names = dictionary words v1–99), vulnerability (synthetic pool: c ~ U[0.4,1), i ~ U[0,10), "cvss" = (c+i)/2, exploitability = cvss/5.5, no CVE-ID; exploit iff rand < c, "pseudo-CVSS"). Service owned when Σ exploited impact > 7.0.

## 3.2 Tactic-action set (before Petri-net ↔ MTDSim grounding)

Open question: what does `profiled_attacker` do at each of the 15 tactics? Each tactic becomes an atomic action with preconditions (prior tactics) and effects (future tactics). Inspired by MITRE Caldera, adapted to a tactic-as-atomic-action model. Adversary profile = Petri nets/timelines (order exists; execution/capability must be reasoned). Abilities and profiles are decoupled so attack profiles are portable.

Questions:
- Ability = "tactic action". Do the techniques aggregated into each tactic feed the ability?
- What facts does the attack model operate on? Must plug into MTDSim's existing facts.
  - **Fig 3.5 – "What facts exist in MTDSim"** (screenshot text): the substrate already carries a Caldera-style fact base in four layers, organised by what an MTD mutation can take back:
    - **A. Attacker-held knowledge (`Adversary`)**. Capability (survives mutation): `_compromised_hosts`, `_compromised_users` (credentials, reused network-wide, never revoked by a shuffle). Position/knowledge (reset by a *network* mutation): `_host_stack`, `_curr_host_id`/`curr_host`, `_pivot_host_id`. Working set (reset by an *application* mutation): `_curr_ports`, `_curr_vulns`. Control (internal): `_curr_process` (six-phase FSM state), `_attack_counter`, `_stop_attack` (deny-list), `observed_changes` (empty hook where MTD-event facts would land; the deferred adaptivity seam).
    - **B. Terrain facts (`Network`)**. Reachability graph (`get_neighbors`), hacker-visible subgraph (reachable ∪ neighbours ∪ exposed), exposed endpoints (never mutated), target node, distance-from-exposed ordering, host↔IP. Topology/IP shuffles mutate these.
    - **C. Host/application facts (`Host`)**. OS type+version, internal Watts–Strogatz service graph, open ports (`port_scan`), services (name/version), compromised-services progress, users + password-reuse flag (`p_u_compromise`), the credential-survivor seam.
    - **D. Service→vulnerability facts (`Vulnerability`)**. Difficulty (`complexity` → success prob + time), value (`impact`/`cvss`), `exploited` flag (per-instance re-exploit discount, the only retained "learning", ATK-04), selection score (`roa`), and two preconditions as data: OS dependency (`vuln_os_list`) and dependent-vuln chain (`dependent_vuln_id`), MulVAL-style.
- Easiest, quickest MVP to get the pipeline done?

## 3.3 Closed (decided in meeting)

- Don't fit to literature timings; assume from practical reports: "observation tactics long, execution quick".
- Predefine profiles; see how their styles react differently against MTD.
- Adjust sim to timelines.
- Leave the relative-gains question.
- Success/failure → tune an attack success-rate parameter. Structural questions remain.

---

# 4. 21 Jul 2026 (Tuesday): Supervisor update

## 4.1 Introduction

Now joined end-to-end. First experiment.

## 4.2 Background: terminology

1. **Movement layer** = everything from CTI (Attack Flow) to attack profiles (Petri net).
2. **Controller layer** = mapping/join between the movement layer and MTDSim (or any MTD sim).
3. **Action layer** = predefined attack behaviour inherited from MTDSim (existing attack module, some changes).

**Fig 4.1 – "How the movement layer joins MTDSim"**: Movement layer (Petri net) ↔ controller (movement ↔ action) ↔ ATTACKER inside MTDSim.
Down: "next transition: which tactic → mapped verb (`step()`)". Up: "action outcome: success/fail → reselects net weights (M2)".
Inside MTDSim: Attacker → Network via the 6-action layer (scan · enum · exploit · brute-force · pivot); Network → Attacker = visible network state (read during actions); Defender → Network = SDR mutation (shuffle/diversity alters terrain); Network → Defender = security metrics → scheme / AI selection. Defender → Attacker = **MTD interrupt** (network/application → phase reset + time penalty), the only defender→attacker coupling. No direct attacker→defender flow. Substrate change stays attacker-only (D5 / M7).

**Fig 4.2 – "How the experiment is wired — movement, controller, action"**: L0 real flows → aggregate (merge shared techniques, weight by frequency) → L1 aggregate graph (edge width = number of campaigns) → split into objective subgraphs → L2: pure_steal n = 19 (selected to run), double_extortion n = 6, pure_impediment n = 8, infrastructure_setup n = 5 → select one → L3 executable net (example: recon not seeded; initial-access (token) → .31 → execution → .06 → discovery → .33 → collection → .57 → exfiltration; skip .06; transitions carry techniques, e.g. T1078→T1059, T1005→T1041). CONTROLLER: maps 15 tactics ⇄ 6 action verbs via `tactic_action_map.csv`; swappable (attack model ⊥ simulator). ACTION: MTDSim attacker FSM (6 verbs, fire-once, gives up after ≥10 tries on a host), network 3-layer HARM (hosts, services, vulnerabilities; synthetic, no CVE-ID), defender MTD (shuffle → host layer; diversity → service layer; redundancy not implemented; interrupt → time penalty).

## 4.3 Changes to MTDSim

**FSM decoupling.** MTDSim phases were hardcoded to call "next phase in sequence"; those lines were deleted and phases run as-is. Edit: the phases do depend heavily on their intended order (see below).

**Table 4.1 – MTDSim phases** (description AI-generated; "My issues" column empty in original)

| Phase | Role | Behaviour (summary of pseudocode) | Function | Limitations |
|---|---|---|---|---|
| SCAN_HOST | Network recon / target selection | Candidates = uncompromised reachable neighbours of compromised hosts (with path from exposed endpoint), ordered by distance_from_exposed + random(); add uncompromised exposed endpoints; drop give-up list → `host_stack`. Non-empty → ENUM_HOST; empty → STOP. | Only source of new targets; reset state after network-layer MTD. | Needs a foothold; visibility = graph reachability, not real scanning. Empty result **ends the attacker's run**; no wait/retry. |
| ENUM_HOST | Pick next host | If stack empty → SCAN_HOST. Re-sort by distance from exposed + pivot; pop nearest → `curr_host`; `attack_counter[host] += 1`; at ATTACKER_THRESHOLD (10) add to give-up list (network type 0 only); reset ports/vulns; set pivot. Already compromised → ENUM_HOST; else → SCAN_PORT. | Loop cursor; enforces give-up-after-10. | Give-up only on network_type == 0; else unbounded retries. "Already compromised" loops without doing anything new. |
| SCAN_PORT | Port scan + credential-reuse check | `curr_ports = port_scan()`; if host auto-compromisable with compromised users → record, → SCAN_NEIGHBOR; else → EXPLOIT_VULN. | Discovers attack surface; models lateral credential reuse. | Reuse is probabilistic and needs a shared username. Empty scan silently turns exploit into a no-op → brute force. |
| EXPLOIT_VULN | Exploit vulnerabilities | For each unexploited vuln (sorted by Return-on-Attack): wait ~exp(exploit_time); if MTD interrupt or sim end → HALTED; apply exploit. If Σ exploited impact ≥ 7 → bump exploitability, record compromise → SCAN_NEIGHBOR; else → BRUTE_FORCE. | Primary compromise mechanism (CVSS/RoA-scored). | Docstring says "top 5" but code iterates **every** qualifying vuln. Only verb with 3-way outcome: MTD interrupt → back to SCAN_PORT/SCAN_HOST + 20-unit confusion penalty. Compromise deterministic once enough impact; no defender-side failure modelling beyond MTD. |
| BRUTE_FORCE | Credential brute force (fallback) | If random() < HOST_MAX_PROB × (matching_users / total_users) → compromised → SCAN_NEIGHBOR; else → ENUM_HOST. | Weak-credential fallback. | One shot per visit. Host with no shared users is effectively immune. Failure abandons the host. |
| SCAN_NEIGHBOUR | Propagation | `found = discover_neighbors()`; push to **front** of `host_stack` → always ENUM_HOST. | Turns one compromise into lateral movement. | Only branch-free verb. Discovery = graph adjacency (no stealth/cost/partial visibility). Already-queued neighbours not re-queued. |

**Fig 4.3 – "MTDSim attacker: the six-verb action layer as one state machine"** (t/u = fixed time cost per verb):

| Verb | Cost (t/u) | Success → | Failure → |
|---|---|---|---|
| SCAN_HOST | 5 | hosts found → ENUM_HOST | no hosts → STOP |
| ENUM_HOST | 5 | fresh host → SCAN_PORT | host already owned → loop ENUM_HOST; host stack empty → SCAN_HOST |
| SCAN_PORT | 25 | cred reuse = owned → SCAN_NEIGHBOR | no cred reuse → EXPLOIT_VULN |
| EXPLOIT_VULN | 15 | compromised → SCAN_NEIGHBOR | exploit failed → BRUTE_FORCE |
| BRUTE_FORCE | 20 | cred guess = owned → SCAN_NEIGHBOR | failed → ENUM_HOST (next host) |
| SCAN_NEIGHBOR | 5 | queue neighbours → always ENUM_HOST | network fully owned → END |

MTD interrupt can hit any timed verb: +20 t/u confusion penalty, then restart (network-layer MTD → SCAN_HOST; application-layer MTD → SCAN_PORT). Every path returns through ENUM_HOST; the only forward motion is a compromise.

**Fig 4.4 – Shared-state preconditions** (producer → consumer): SCAN_HOST produces `host_stack` → ENUM_HOST; SCAN_NEIGHBOR produces `host_stack` → ENUM_HOST; ENUM_HOST produces `curr_host` → SCAN_PORT, EXPLOIT_VULN, BRUTE_FORCE, SCAN_NEIGHBOR (hub: 4 verbs need it); SCAN_PORT produces `curr_ports` → EXPLOIT_VULN. EXPLOIT_VULN and BRUTE_FORCE produce no precondition output. Out of order, `step()` raises `ActionContextError`.

**PRE-ATT&CK synthesised flows.** A Petri "subnet" connecting recon, resource dev and initial access, kept as a separate object and overlaid onto the nets before runtime.

**Fig 4.5 – Synthetic overlay** (artefact `data/ogasp/petri/synthetic_overlay.json`; applied where the corpus leaves the pre-intrusion band detached: double_extortion, infrastructure_setup):

| Synthetic transition | Declared share | Direction |
|---|---|---|
| reconnaissance → resource-development | 1.00 | forward |
| resource-development → initial-access | 1.00 | forward |
| initial-access → reconnaissance | 0.10 | backward (regression bridge) |

Reconnaissance = token seed; resource-development = forward pass-through (×0 dwell).

**Fig 4.6 – Overlay composed onto observed nets** (solid = observed W-A flow-proportion weight, operator-dedup):
- infrastructure_setup (net continues: 57 observed transitions): initial-access → execution 1.00.
- double_extortion (net continues: 72 observed transitions): initial-access → stealth 0.50, → privilege-escalation 0.25, → execution 0.25.

**MTDSim attacker ⇌ Petri net.** A port between tactics and MTDSim phases: at a tactic, the attacker executes the mapped behaviour. 15 tactics, 6 phases.
The first Claude-generated mapping wasn't tractable (not a clean mapping), but showed some tactics have no capability in the sim (e.g. stealth) and some verbs could be split (EXPLOIT_VULN appears many times).

**Table 4.2 – Tactic → verb coverage "as decided"** (✓ = dispatches verb; ▸ = precursor context only: the port scan feeds EXPLOIT_VULN's `curr_ports`, but the verdict-bearing act is the exploit):

| Tactic | SCAN_HOST | SCAN_PORT | EXPLOIT_VULN | BRUTE_FORCE | SCAN_NEIGHBOR |
|---|---|---|---|---|---|
| reconnaissance | ✓ | ✓ | · | · | · |
| resource-development | · | · | · | · | · |
| initial-access | · | ▸ | ✓ | · | · |
| execution | · | · | · | · | · |
| persistence | · | · | · | · | · |
| privilege-escalation | · | ▸ | ✓ | · | · |
| stealth / defense-evasion | · | · | · | · | · |
| defense-impairment | · | · | · | · | · |
| credential-access | · | · | ✓ | ✓ | · |
| discovery | ✓ | ✓ | · | · | ✓ |
| lateral-movement | · | · | ✓ | ✓ | ✓ |
| collection / C2 / exfiltration / impact | · | · | · | · | · |

(ENUM_HOST has no column in this matrix.) This coverage "gets the first numbers in". Some tactics can't be reached, so weights are adjusted at runtime from attacker signals: a tactic→tactic bipartite dictionary with values in [0,1], stored as `SUCCESS.json` and `FAILURE.json`. If the attacker succeeds at a phase, the possible transitions' weights are manipulated by the success set, and vice versa.

## 4.4 Experimental setup / Results / Discussion

Empty in the original.

## 4.5 Open questions

- Does the coverage make sense?
- Refine existing actions? They are so integrated that running them as separate phases makes little sense. More actions? How much refining?
- How to implement dwell-only tactics (e.g. resource development)?
- Where do timings come from: movement layer (Petri) or action layer (MTDSim phases)? Easier to adopt from MTDSim; at runtime it's the same.

---

# 5. 03 Aug 2026 (Monday): Supervisor update

## 5.1 Introduction: APT attack-fidelity rubric

New rubric for "what does my APT attacker model capture that existing models do not", adapted from the lit review. Axes come from literature on what existing MTD-evaluation attack models lack. Question: what is the MVP, given little time left?

**Table 5.1 – Eight fidelity axes: status on 03 Aug**

| # | Axis | Implemented? | Definition | How it is modelled / what was tried |
|---|---|---|---|---|
| 1 | Persistence (multi-stage campaign structure) | Partial | Multi-stage campaign sustained over an extended period (Cho's *persistent*; NIST "pursues its objectives repeatedly over time"). Not ATT&CK's re-access-after-disconnection sense. | Movement layer: token cycles through tactics without ending the campaign; a sink-retrace policy removes dead ends that used to end runs early. MTDSim note: compromise is never revoked; MTD mutations only affect the attacker's stage, not what it has compromised. |
| 2 | Objective conditioning | Yes | Attacker behaviour is directed by its objective. | Profiles partitioned by *analyst-stated* objectives have different Petri-net structures and materially different runtime behaviour. |
| 3 | Strategic plurality (multi-strategy branching) | Yes | Multiple possible moves at a given step. | Petri net with multiple weighted transitions; branching from corpus proportions. |
| 4 | Adaptivity to defender resistance | Yes | Attacker alters behaviour on environmental signals. | Controller layer: static success/failure outcome overlay (fixed tables re-weight out-transitions given MTDSim's verdict). |
| 5 | Stealth (low-and-slow tempo, evasion) | No… partially | Low-and-slow to avoid detection. | No IDS, so nothing to be stealthy against. Most tactics have no action → longer dwell → AI-MTD/MTDShield (which uses network metrics) sees different security metrics → different mutation outcomes (i.e. stealthy tempo). |
| 6 | Incentive-driven rationality | No… partially | Attacker does cost-benefit before its next move; MTD raises cost until engagement isn't worth it. An attacker whose expected payoff falls below attacking another network leaves. | Balanced against downtime/availability metrics calibrated to the sim (cost-of-moving vs risk-of-not-moving). **Negative results:** utility = benefit/cost using time → fast tempo, prefers short tactics, not all MTDSim phases invoked; utility = progress/effort (progress = distance to objective, e.g. 0.8 NCR for general, closeness to target host for targeted) failed because effort is ill-defined; the only usable effort (distance to next progressing tactic) amounts to injecting the next phase into the weights, which became the compromise. Marked future work. **Current mechanism:** attacker-side metric attack utility = progress/effort; if cost gets too high past a threshold the attacker "gives up and goes elsewhere" (partially implemented; needs verification). |
| 7 | Learning capability | No… | Attacker learns what worked on this network and repeats it. | Laplace success/failure weight update: Q(tactic) = (successes + 1) / (successes + failures + 2). Works as proof of concept but makes the attacker worse: biases towards recon/SCAN_HOST (fewest prerequisites). **UPDATE, all failed:** (a) direct weight updates from MTDSim success/failure → favours SCAN_HOST; sensitivity study on belief absorption gave a negative result; (b) replaying successful/failed tactic–tactic chains → failed (cause not yet investigated); (c) tracking whether a tactic's mapped phase has its preconditions satisfied, or whether a tactic progresses the objective → no better than switched off (static weights). Memorised tactic chains would need ML/RL → future work. |
| 8 | MTD-scheme awareness | No | Moves the MTD/attacker interface from black-box to grey-box. | Needs an observation channel and inference on the attacker side. Out of scope; future work. |

Not-implemented axes are future work. No more changes to the underlying attack phases (no time to do it well). Consequence: the movement attacker will be, on a good day, equal to the original MTDSim attacker and, on average, significantly worse.

Empirical analysis aims: (a) what does this APT model capture that prior work does not (table above); (b) how does it improve MTD evaluation; (c) (optional) how practitioners can apply the pipeline to their own attack models.

Because the underlying attack operation is inherited, the movement attacker can only match or underperform the baseline. The assumption is that raw attacker performance is not the main game. The point is **how MTD mechanism / orchestration rankings change under a higher-fidelity attack model**.

Concession for axes 6 and 7: an `fsm_overlay` input injects the shortest paths to the next objective-progressing tactics, on a 0–1 scale (0 = no injection; 1 = constrain Petri transitions to only the next progressive tactics).

**Moving forward.** Claimed: objective conditioning, strategic plurality, adaptivity to defender resistance. Concessionally: stealth (slower tempo, possible effect on network security metrics), persistence (attacker never stops until sim end), incentive rationality (a new metric: if the attack stalls, the attacker would realistically have given up). Future work: MTD-scheme awareness, learning capability.

**Q to Jin:** is this a strong enough foundation for the thesis?

## 5.2 Experimental setup

**Weight changes.** Tactics chunked into 4 attack-lifecycle stages (broadly from literature): 0 preparation, 1 intrusion, 2 post-intrusion operations, 3 objective. Distance between stages decreases the weight of a tactic pairing (pending sensitivity analysis).

**Table 5.2 – Outcome overlay v2: SUCCESS verdict, declared next-tactic weights.** Value = given the verb dispatched at the source returned SUCCESS, the declared likelihood of the destination as next move. Rows = source, columns = destination. "—" = diagonal (self-transition not a value; repeating a tactic is the stepping layer's bounded retry).

| src \ dst | RC | RD | IA | EX | PS | PE | DI | ST | CA | DS | LM | C2 | CO | EF | IM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RC | — | 1 | 1 | .6 | .15 | .15 | .15 | .15 | .15 | .15 | .15 | .15 | 0 | 0 | 0 |
| RD | .5 | — | 1 | .6 | .15 | .15 | .15 | .15 | .15 | .15 | .15 | .15 | 0 | 0 | 0 |
| IA | .1 | .1 | — | 1 | 1 | 1 | .6 | 1 | 1 | 1 | .6 | 1 | .15 | .15 | .15 |
| EX | .1 | .1 | .5 | — | 1 | 1 | .6 | 1 | 1 | 1 | .6 | 1 | .15 | .15 | .15 |
| PS | .05 | .05 | .25 | .25 | — | 1 | .5 | .5 | 1 | 1 | 1 | 1 | .6 | .6 | .6 |
| PE | .05 | .05 | .25 | .25 | 1 | — | 1 | 1 | 1 | 1 | 1 | .5 | 1 | .6 | .6 |
| DI | .05 | .05 | .25 | .25 | .5 | .5 | — | .5 | 1 | 1 | 1 | .5 | 1 | 1 | 1 |
| ST | .05 | .05 | .25 | .25 | .5 | .5 | .5 | — | 1 | 1 | 1 | 1 | 1 | .6 | .6 |
| CA | .05 | .05 | .25 | .25 | 1 | 1 | .5 | .5 | — | 1 | 1 | .5 | 1 | .6 | .6 |
| DS | .05 | .05 | .25 | .25 | .5 | 1 | .5 | .5 | 1 | — | 1 | .5 | 1 | .6 | .6 |
| LM | .05 | .05 | .25 | .25 | 1 | 1 | .5 | .5 | 1 | 1 | — | 1 | 1 | .6 | .6 |
| C2 | .05 | .05 | .25 | 1 | 1 | 1 | .5 | .5 | 1 | 1 | 1 | — | 1 | 1 | 1 |
| CO | .025 | .025 | .125 | .125 | .25 | .25 | .25 | .25 | .25 | .25 | 1 | 1 | — | 1 | .5 |
| EF | .025 | .025 | .125 | .125 | .25 | .25 | .25 | .25 | .25 | .25 | .25 | 1 | 1 | — | 1 |
| IM | .025 | .025 | .125 | .125 | .25 | .25 | .25 | .25 | .25 | .25 | .25 | .25 | .5 | .5 | — |

**Table 5.3 – Outcome overlay v3: FAILURE verdict, declared next-tactic weights.** Same layout.

| src \ dst | RC | RD | IA | EX | PS | PE | DI | ST | CA | DS | LM | C2 | CO | EF | IM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RC | — | .7 | .4 | .05 | .0125 | .0125 | .0125 | .0125 | .0125 | .0125 | .0125 | .0125 | 0 | 0 | 0 |
| RD | .7 | — | .3 | .3 | .075 | .075 | .075 | .075 | .075 | .075 | .075 | .075 | 0 | 0 | 0 |
| IA | .9 | .9 | — | .02 | .02 | .02 | .02 | .02 | .02 | .02 | .02 | .02 | .005 | .005 | .005 |
| EX | .25 | .25 | .7 | — | .35 | .35 | .35 | .35 | .35 | .35 | .35 | .35 | .0875 | .0875 | .0875 |
| PS | .0625 | .0625 | .25 | .35 | — | .7 | .7 | .7 | .7 | .7 | .7 | .7 | .35 | .35 | .35 |
| PE | .0625 | .0625 | .25 | .35 | .7 | — | .7 | .7 | .7 | .7 | .7 | .7 | .35 | .35 | .35 |
| DI | .0625 | .0625 | .25 | .35 | .7 | .7 | — | .7 | .7 | .7 | .7 | .7 | .35 | .35 | .35 |
| ST | .0625 | .0625 | .25 | .35 | .7 | .7 | .7 | — | .7 | .7 | .7 | .7 | .35 | .35 | .35 |
| CA | .0625 | .0625 | .25 | .35 | .7 | .7 | .7 | .7 | — | .7 | .7 | .7 | .35 | .35 | .35 |
| DS | .0625 | .0625 | .25 | .35 | .7 | .7 | .7 | .7 | .7 | — | .7 | .7 | .35 | .35 | .35 |
| LM | .0625 | .0625 | .25 | .35 | .7 | .7 | .7 | .7 | .7 | .7 | — | .7 | .35 | .35 | .35 |
| C2 | .0625 | .0625 | .25 | .35 | .7 | .7 | .7 | .7 | .7 | .7 | .7 | — | .35 | .35 | .35 |
| CO | 0 | 0 | .0625 | .0875 | .9 | .9 | .9 | .9 | .9 | .9 | .9 | .9 | — | .7 | .7 |
| EF | 0 | 0 | .0625 | .0875 | .9 | .9 | .9 | .9 | .9 | .9 | .9 | .9 | .7 | — | .7 |
| IM | 0 | 0 | .0625 | .0875 | .9 | .9 | .9 | .9 | .9 | .9 | .9 | .9 | .7 | .7 | — |

Reading note (from charts): rows/columns grouped by lifecycle stage. Above the diagonal block = forward travel; below = backward; the further from it, the more stages crossed. Order within a stage is ATT&CK reading order and asserts nothing (stage 2 is declared unordered). **[conversion note]** SUCCESS is labelled "v2" and FAILURE "v3" in the original charts.

**Fig 5.3 – Aggregate profile campaign structure by lifecycle stage** (arc width = base weight before outcome conditioning; horizontal span = stage offset Δ read by the distance kernel):

| Stage offset | Transitions carrying mass |
|---|---|
| forward 1 stage | 30 |
| forward 2 stages | 6 |
| within a stage (no distance) | 48 |
| backward 1 stage | 24 |
| backward 2 stages | 6 |
| **Total** | **114** |

No arc spans three columns: the corpus has no preparation ↔ objective transition in either direction, which is why reconnaissance → impact has a declared weight but never routes.

**Table 5.4 – Tactic-to-action mapping change (v2).** Each tactic dispatches at most one verb. 8 tactics dispatch a verb; 7 are dwell-only (consume simulated time, fire no verb, raise no verdict, so the token routes on base weights). Every verb is reachable; only EXPLOIT_VULN serves more than one tactic.

| Tactic | Lifecycle stage | MTDSim verb | Reason |
|---|---|---|---|
| reconnaissance | preparation | SCAN_HOST | surveys the reachable target set |
| resource-development | preparation | — (dwell only) | nothing outside the network is modelled |
| initial-access | intrusion | EXPLOIT_VULN | the verb that takes a host it does not own |
| execution | intrusion | EXPLOIT_VULN | runs adversary code against a service |
| persistence | post-intrusion | — (dwell only) | compromise is permanent; nothing to hold |
| privilege-escalation | post-intrusion | EXPLOIT_VULN | impact accrues toward the control threshold |
| stealth (defense-evasion) | post-intrusion | — (dwell only) | no detection surface to evade |
| defense-impairment | post-intrusion | — (dwell only) | the defence is not attacker-reachable |
| credential-access | post-intrusion | BRUTE_FORCE | T1110 is this verb, literally |
| discovery | post-intrusion | SCAN_PORT | T1046 network service discovery |
| lateral-movement | post-intrusion | ENUM_HOST | pivots onto the next host |
| command-and-control | post-intrusion | SCAN_NEIGHBOR | Brown: C2 reveals connected hosts |
| collection | objective | — (dwell only) | no data objects exist to stage |
| exfiltration | objective | — (dwell only) | no data, and no egress channel |
| impact | objective | — (dwell only) | compromise is the only state change |

**[conversion note]** This replaces the 21 Jul matrix (Table 4.2). Differences: execution now maps to EXPLOIT_VULN; discovery maps only to SCAN_PORT; lateral movement maps to ENUM_HOST; C2 maps to SCAN_NEIGHBOR; each tactic has one verb.

**Changes to experiment conditions.** A token hitting a sink node now retraces its last transition. This removes the issue of some nets discarding a large share of runs by hitting a sink early.

## 5.3 Results

None yet. Pulling results next week alongside code validation and bug fixes.

## 5.4 Discussion: questions for Jin

1. No more major implementations left to try. Is polishing enough? Some lit-review APT criteria aren't met, and a model hitting all of them is hard, given the constraint of not changing the underlying attack operation (possible future work for another student). Could a well-written thesis on this get an HD?
2. For comparing MTD mechanisms/orchestration, all boundaries must be implemented fairly/faithfully (e.g. OSDiversity as a derivative of ServiceDiversity).
3. What do results look like?
   1. Ranking MTD mechanisms? Compare with prior results? How to rank? No redundancy (SDR): effect?
   2. Ranking MTD orchestration too, or hold constant? MTD-AI against this varied attacker would be interesting.
   3. Metrics?

## 5.5 Work planned

- Check component boundaries (ATTACKER–NETWORK, DEFENDER–NETWORK, ATTACKER–DEFENDER) are faithfully and fairly integrated.
- Sensitivity analysis on tactic durations, stochastic exponent, tactic–tactic weights, …
- Ablation study on attack profiles (do they perform differently when filtered by objective?).
- Document as you go; tidy the model; make the repo human-readable.

---

# 6. 09 Aug 2026 (Sunday): Supervisor update

## 6.1 APT criterion and instrumentation (with results)

| # | Axis | Description | Metric | Result |
|---|---|---|---|---|
| 1 | Persistence | Multi-stage campaign over an extended period. Inherited MTDSim already models this well. | N/A | Abstracted by simulation run duration ("persistent campaign"). Attempts at a persistence metric fail: campaign duration is a simulator input, so it can't be instrumented. |
| 2 | Objective conditioning | Behaviour directed by objective (the attack profiles). | **Attack Profile Divergence** (Jensen–Shannon divergence between profiles' runtime behaviour) | Profiles meaningfully produce different runtime behaviour. JSD between objective profiles ranges **0.081–0.237**, i.e. 8–24% of each profile's behaviour is not seen in the others. See Table 6.1. |
| 3 | Strategic plurality | Multiple possible moves per step; Petri net with weighted transitions from aggregated CTI. | **Predictability** = rate at which the model's next move can be called from its own decision state | Predictability(baseline) = **1.00** (by construction). Predictability(movement) = **[0.33, 0.57]**. 1 = fully predictable; the movement attacker is measurably less predictable. |
| 4 | Adaptability to defender resistance | Under active MTD resistance the model redirects rather than repeats or retreats (shifts towards re-establishing lost progress) and should beat a resistance-blind attacker. | N/A | Intractable: all MTD mechanisms are attacker-blind (time-based), so there is no advantage to gain; widening the success/failure signals isn't exploitable either (it only feeds the out-transition set). |
| 5 | Stealth | "Low-and-slow" to avoid detection. No IDS, so detection is abstract; measured relative to baseline. | **Detectability** (tempo-based: invoking an attack phase temporarily raises detectability, which decays over time; many phases in quick succession → higher detectability) | Baseline is louder than the low-and-slow profiles. Outlier: infrastructure setup / pre-positioning (too few dwell tactics in its net). See Table 6.2. |
| 6 | Incentive-driven rationality | Considers campaign cost-benefit; disengages if MTD stalls the attack. | **Disengagement time** (runtime attack utility = progress/effort after each event; below threshold → attacker assumed to have moved on) | Runtime-only characterisation of the campaign. Demonstration in Table 6.3 (impatient vs patient/APT attacker). |
| 7 | Learning capability | Learns which workflows worked and reuses them. Modelled by storing successfully exploited vulnerabilities in attacker state, raising EXPLOIT_VULN success when the same vuln is seen again. | Implemented, minimal effect | **TODO.** The model is only as strong as its weakest link: churn from the FSM's random ordering of attack phases. The attacker can't pivot to neighbours and tends to churn through hosts it has already compromised, so the vuln-memory boost rarely applies. |
| 8 | MTD boundary awareness | Can exploit side-channels in the MTD scheme to improve evasion. | N/A | Attempted. Only MTDShield / Tay 2024 has event-based movement, and it either always prefers "do nothing" or preferentially picks IP shuffle; needs calibrating to Tay's intent. Any simple event-based orchestration added to MTDSim would need calibration, defeating the purpose. Future work. |

**Table 6.1 – Attack profile divergence (JSD, log scale).** Chart labels are ×10⁻³ (e.g. 237 = 0.237).

| Profile pair | JSD | Pair type |
|---|---|---|
| exfiltration + impact vs positioning (C2) | 0.237 | between objective profiles |
| impact vs positioning (C2) | 0.189 | between objective profiles |
| exfiltration vs exfiltration + impact | 0.143 | between objective profiles |
| exfiltration vs impact | 0.124 | between objective profiles |
| exfiltration vs positioning (C2) | 0.111 | between objective profiles |
| exfiltration + impact vs impact | 0.081 | between objective profiles |
| unsegregated vs positioning (C2) | 0.122 | vs aggregate (hollow marker) |
| unsegregated vs exfiltration + impact | 0.067 | vs aggregate |
| unsegregated vs impact | 0.065 | vs aggregate |
| unsegregated vs exfiltration | 0.023 | vs aggregate |

Within-profile null band (grey): roughly 3×10⁻⁴ to 2×10⁻³ (read from chart). Every pair sits well above it.
**[conversion note]** The original caption says "0.81-0.237 JSR". The chart's smallest between-profile value is 0.081, so the range should read 0.081–0.237 (JSD).

**Table 6.2 – Detectability D** (regime R1; window 0–6,000 s where both arms are active; τ = 60 s; verb-level tiers on both arms; CVSS term off; mean over 10 seeds, 250 s bins)

| Arm | Mean D | Notes |
|---|---|---|
| Baseline (6-phase FSM) | 0.37 | Higher than every low-and-slow profile in **22 of 24** bins. The two exceptions are the opening burst, before any profile reaches its first dwell tactic. Binned values ~0.26–0.47 (read from chart). |
| Four movement profiles | 0.23–0.25 | Band ~0.14–0.32 after the first bin (read from chart). |
| `objective_none_c2` (fewest dwell tactics; = positioning / infrastructure setup) | 0.49 | Above baseline throughout; peaks ~0.70 near 5,600 s (read from chart). |

Exceedance curve ("fraction of the run spent above D"; "spends three to four times as much of it loud"), read from chart:

| D level | Baseline | Four movement profiles | objective_none_c2 |
|---|---|---|---|
| 0.2 | ~0.65 | ~0.45–0.50 | ~0.80 |
| 0.4 | ~0.43 | ~0.17–0.19 | ~0.53 |
| 0.6 | ~0.21 | ~0.05–0.07 | ~0.31 |
| 0.8 | ~0.08 | ~0.01–0.02 | ~0.17 |
| 1.0 | ~0.02 | ~0 | ~0.08 |

**Table 6.3 – Disengagement demonstration** (one profiled run, no MTD; k = reservation)

| Reservation k | Outcome | Where |
|---|---|---|
| 1.5 (impatient) | gives up | action 18, holding 0 hosts (projected 2178 > budget 2160) |
| 2.0 | gives up | action 178, holding 2 hosts (projected 2889 > budget 2880) |
| 3.0 (patient / APT) | does not give up within horizon | reaches 6 hosts, never crosses |

## 6.2 Methodology section outline (revised)

**Chapter 3 — Methodology.** Preamble (≤3 paragraphs): the APT threat model restated, not re-argued; scope + proof-of-concept commitment; ruled exclusions; two-sentence map of the workflow.

- **3.1 APT model fidelity criterion**: eight axes as bold-led blocks, stated and cited back to ch. 2; scorecard table as anchor; one paragraph defining the four badges by evidential requirement; state that axes were fixed before scoring.
- **3.2 The inherited MTDSim simulator**: 3.2.1 Network model (terrain at the depth Results needs); 3.2.2 Defence model (mechanisms + RL defence as evaluation conditions, not contributions); 3.2.3 Procedural attacker (how the baseline works; closes with its scorecard against 3.1, the gap 3.3 fills).
- **3.3 Modelling APT attackers**: 3.3.1 L0 campaign corpus (provenance, curation, grounding claim defended); 3.3.2 L1 aggregated technique graph (aggregation decisions); 3.3.3 L2 objective-conditioned profiles (four classes, conditioning, extraction); 3.3.4 L3 executable movement attacker (attacker loop; controller L3b as labelled block; behaviour-changing mechanisms each tied to its 3.1 axis).
- **3.4 Measuring the movement attacker**: no subsections; one-paragraph lead-in on what inherited metrics can't observe; per-axis instrument blocks in 3.1's order, including what a sweep must show for a null to count as a measured negative.

## 6.3 3.5 Experimental setup

RQ: *What does greater attack fidelity imply for current MTD evaluation methods?*

Dimensions:
1. **Prior-model comparison**: baseline vs movement. Prior literature findings can be evaluated here (Brown, Zhang, Ho).
2. **Fresh evaluation**: movement vs network/defender configurations:

| Dimension | Levels | Why it's here |
|---|---|---|
| Attacker arm | inherited scripted; profiled envelope (×5 objective profiles) | the manipulation |
| Defence | no-MTD; each mechanism; shuffle-only; diversity-only; shuffle+diversity; execution schemes | Jin's combinations; Zhang/Ho/Brown headlines stated over exactly these |
| Network scale | small / medium / large | Zhang's factor; the axis each fidelity extension is designed to show or vanish on (e.g. learning) |
| Edge density | held vs varied at fixed node count | settles Zhang's unresolved density confound |
| Mutation regime | operating (~200 s) + relaxed (≥ ~1,600 s) | inversion is regime-dependent; degenerate region lives here |
| Service pool size? | small / medium / large? | see if attacker learning changes the game |

3.5.1 Prior-model comparison: both attackers; test lineage findings: Zhang (shuffle dominates), Ho (diversity dominates), Brown (???).
3.5.2 Evaluation: test the dimensions.

**3.6 Threats to validity**: slim; each threat named with the design decision that bounds it.

---

# 7. Metrics quick reference (all dates)

## 7.1 Evaluation criterion: how each axis evolved

| # | Axis | 03 Aug status | 09 Aug metric | 09 Aug result |
|---|---|---|---|---|
| 1 | Persistence | Partial | none (not instrumentable) | abstracted by run duration |
| 2 | Objective conditioning | Yes | Attack Profile Divergence (JSD) | 0.081–0.237 between profiles; all ≫ within-profile null |
| 3 | Strategic plurality | Yes | Predictability | baseline 1.00; movement 0.33–0.57 |
| 4 | Adaptivity to defender resistance | Yes | none | judged intractable (MTD is attacker-blind) |
| 5 | Stealth | No… partially | Detectability D | mean D baseline 0.37; profiles 0.23–0.25; C2/positioning 0.49 |
| 6 | Incentive rationality | No… partially | Disengagement time | k = 1.5 / 2.0 give up; k = 3.0 never does |
| 7 | Learning capability | No… | (vuln-memory) | implemented, minimal effect; TODO |
| 8 | MTD-scheme / boundary awareness | No | none | future work |

**[conversion note]** Axis 4 moved from "Yes" (03 Aug) to "N/A / intractable" (09 Aug).

## 7.2 Planned outcome metrics (10 Jul)

MTTC (mean time to compromise), ASR (attack success rate), exposure. Compared across MTD mechanisms × profile attacker × FSM baseline.

## 7.3 Where every numeric table is

| Table | Section | Date |
|---|---|---|
| Per-class tactic share (%) and class signatures | Fig 1.4 | 23 Jun |
| Class subgraph sizes (flows, techniques, edges) | Fig 1.5 | 23 Jun |
| Aggregate tactic graph: heaviest edges, node technique counts | Fig 1.2 | 23 Jun |
| Tactic dwell times (15-tuple) | Table 2.1 | 10 Jul |
| Time-to-objective medians + objective counts | Fig 2.2 | 10 Jul |
| Outcome mix per profile × routing arm | Fig 2.3 | 10 Jul |
| First 20 walks per profile (outcome, time/states) | Figs 2.4–2.7 | 10 Jul |
| tactic_action_map.csv (ATT&CK IDs, groups) | Fig 3.3 | 14 Jul |
| MTDSim verb costs and transitions | Fig 4.3 / Table 4.1 | 21 Jul |
| Synthetic pre-intrusion overlay shares | Fig 4.5–4.6 | 21 Jul |
| Tactic → verb matrix v1 | Table 4.2 | 21 Jul |
| SUCCESS / FAILURE overlay matrices (15×15) | Tables 5.2–5.3 | 03 Aug |
| Transition counts by stage offset | Fig 5.3 | 03 Aug |
| Tactic → verb mapping v2 | Table 5.4 | 03 Aug |
| JSD profile divergence | Table 6.1 | 09 Aug |
| Detectability | Table 6.2 | 09 Aug |
| Disengagement demo | Table 6.3 | 09 Aug |
| Experimental dimensions | §6.3 | 09 Aug |

## 7.4 Inconsistencies to be aware of

- **Profile count:** four objective profiles + aggregate = 5 arms. The 09 Aug design says "×5 objective profiles" (counts aggregate/unsegregated as one); the detectability chart shows "four movement profiles" + `objective_none_c2` (also 5).
- **Class sizes:** 23 Jun and 21 Jul give 19 / 6 / 8 / 5 flows (steal / extortion / impediment / infra) = 38. The 10 Jul note mentions "4-flow small classes"; the smallest classes actually have 5–6 flows.
- **Recon seeding:** 23 Jun seeds the token in reconnaissance; 10 Jul onward seeds at initial access; 21 Jul adds the synthetic recon → resource dev → initial access overlay (recon becomes the seed again for double_extortion and infrastructure_setup).
- **Termination:** 10 Jul runs stop at the objective; 03 Aug adds sink-retrace so runs continue; 09 Aug treats persistence as running to sim end.
- **Mapping versions:** Table 4.2 (21 Jul, many-to-many) vs Table 5.4 (03 Aug, one verb per tactic). Table 5.4 is the later one.
- **Overlay versions:** SUCCESS matrix labelled v2, FAILURE labelled v3.
- **JSD caption typo:** "0.81" should be 0.081.
- **10 Jul figures:** the infrastructure_setup walk chart appears twice and the pure_impediment walk chart is missing.